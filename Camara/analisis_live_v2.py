import os
import cv2
import time
import shutil
import subprocess
import threading
import requests
import signal
from datetime import datetime
from ultralytics import YOLO
import numpy as np
from sort import Sort
from moviepy import VideoFileClip, concatenate_videoclips
from flask import Flask, send_from_directory
from flask_cors import CORS

# ---------------------- CONFIG ----------------------
#Usuario
ID_USUARIO = 2  # ID d'usuari a la BD
ID_CAMARA = 1   # ID de càmera a la BD

# Font de càmera: pot ser 0, "/dev/video0", o "rtsp://..." segons dispositiu
RTSP_OR_CAMERA = 0

# HLS output (local web folder)
HLS_DIR = "directe"           # ffmpeg escriu aquí (index.m3u8 + segments .ts)
HLS_M3U8_NAME = "stream.m3u8"

# Carpeta per guardar segments detectats
DETECCIONS_NORMAL = "deteccions/normal"   # es guarden .ts originals aquí
DETECCIONS_YOLO = "deteccions/yolo"       # es guarden .mp4 amb caixes aquí
RESULTATS_DIR = "resultats"               # vídeos finals
RAW_DIR = "video"                    # vídeo complet guardat (opcional)

# Models
DETECTOR_MODEL_PATH = "yolov8n.pt"   # model per detecció
IDENT_MODEL_PATH = "best.pt"         # model d'identificació d'espècies (si aplicable)
DETECTION_CLASS = 14               # filtrar per classe 14 (ocells). Si poses (None) idetificara totes.

# Thresholds
CONF_THRESHOLD = 0.5      # detecció per marcador inicial
ID_CONF_THRESHOLD = 0.85  # identificació per considerar espècie

# API
API_BASE = "http://127.0.0.1:5000"   # canvia a la teva API
UPLOAD_ENDPOINT = f"{API_BASE}/upload_video"  # s'intenta pujar segments aquí
AVISTAMENTS_ENDPOINT = f"{API_BASE}/avistaments"
VIDEOS_ENDPOINT = f"{API_BASE}/videos"
RESET_ENDPOINT = f"{API_BASE}/reset_directe/{ID_CAMARA}"

# Misc
FPS_FF = 60                 # fps que li diem a ffmpeg si fem piping (només si s'usa stdin)
HLS_SEGMENT_TIME = 5        # segons per segment HLS
POLL_INTERVAL = 1.5         # secs per mirar la carpeta HLS
KEEP_PROCESSED_SET = True   # recorda quins .ts ja s'han processat (evita doble processament)
UPLOAD_ON_DETECT = True     # pujar segments detectats al servidor
SAVE_RAW_FULL_VIDEO = True  # guarda un .mp4 sencer local a RAW_DIR (opcional)

# ------------------- DIRECTORIES SETUP -------------------
os.makedirs(HLS_DIR, exist_ok=True)
os.makedirs(DETECCIONS_NORMAL, exist_ok=True)
os.makedirs(DETECCIONS_YOLO, exist_ok=True)
os.makedirs(RESULTATS_DIR, exist_ok=True)
os.makedirs(RAW_DIR, exist_ok=True)

# ------------------- MODELS & TRACKER -------------------
detector = YOLO(DETECTOR_MODEL_PATH)
try:
    identificador = YOLO(IDENT_MODEL_PATH)
except Exception:
    identificador = None

tracker = Sort()

# ------------------- FLASK HLS SERVER (opcional) -------------------
app = Flask(__name__)
CORS(app)

@app.route('/hls/<path:filename>')
def serve_hls(filename):
    return send_from_directory(HLS_DIR, filename)

def run_flask_server():
    # Serveix HLS per clients locals si cal
    app.run(host='0.0.0.0', port=8080, debug=False)

# ------------------- FFMPEG: CREA HLS (des de stdin) -------------------

def start_ffmpeg_hls(frame_w, frame_h, fps):
    """
    Inicia un procés ffmpeg que llegeix rawvideo per stdin i escriu HLS (index.m3u8 + .ts).
    Retorna subprocess.Popen object i el path complet del m3u8.
    """
    m3u8_path = os.path.join(HLS_DIR, HLS_M3U8_NAME)
    # Comanda similar a la que feies:
    cmd = [
        'ffmpeg', '-y',
        '-f', 'rawvideo',
        '-pix_fmt', 'bgr24',
        '-s', f"{frame_w}x{frame_h}",
        '-r', str(fps),
        '-i', '-',  # stdin
        '-c:v', 'libx264',
        '-preset', 'veryfast',
        '-tune', 'zerolatency',
        '-pix_fmt', 'yuv420p',
        '-f', 'hls',
        '-hls_time', str(HLS_SEGMENT_TIME),
        '-hls_list_size', '5',
        '-hls_flags', 'delete_segments+append_list',
        '-hls_segment_type', 'mpegts',
        m3u8_path
    ]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return proc, m3u8_path

# ------------------- UTILS: pujar segment, crear resum -------------------
def upload_segment(filepath, idvideo=None, idcamara=None, tipus="normal"):
    if not UPLOAD_ON_DETECT:
        return
    try:
        with open(filepath, "rb") as f:
            files = {"file": f}
            data = {"IDVideo": idvideo or 0, "IDCamara": idcamara or 0, "tipus": tipus}
            r = requests.post(UPLOAD_ENDPOINT, files=files, data=data, timeout=120)
            try:
                print("upload_segment:", filepath, "->", r.status_code, r.text)
            except:
                print("upload_segment:", filepath, "-> response not printable")
    except Exception as e:
        print("❌ Error uploading", filepath, e)

def concat_normal_ts_to_mp4(ts_dir, out_path):
    """Crea un fitxer de llista i usa ffmpeg concat per produir mp4 sense recodificar."""
    listfile = os.path.join(RESULTATS_DIR, "normal_list.txt")
    with open(listfile, "w") as f:
        for ts in sorted(os.listdir(ts_dir)):
            if ts.endswith(".ts"):
                f.write(f"file '{os.path.abspath(os.path.join(ts_dir, ts))}'\n")
    if os.path.getsize(listfile) == 0:
        print("No hi ha segments .ts per concatenar (normal).")
        return False
    cmd = f"ffmpeg -f concat -safe 0 -i {listfile} -c copy {out_path}"
    print("Exec:", cmd)
    os.system(cmd)
    return True

def concat_yolo_mp4s(mp4_dir, out_path):
    """Concatena amb MoviePy i re-encoda si cal."""
    files = sorted([os.path.join(mp4_dir, f) for f in os.listdir(mp4_dir) if f.endswith(".mp4")])
    if not files:
        print("No hi ha MP4s YOLO per concatenar.")
        return False
    clips = [VideoFileClip(f) for f in files]
    final = concatenate_videoclips(clips, method="compose")
    final.write_videofile(out_path, codec="libx264")
    for c in clips:
        c.close()
    final.close()
    return True

def generar_resum_final():
    """Genera els dos vídeos finals i imprimeix el resultat."""
    out_normal = os.path.join(RESULTATS_DIR, "ocells_detectats.mp4")
    out_yolo = os.path.join(RESULTATS_DIR, "ocells_detectats_yolo.mp4")

    ok1 = concat_normal_ts_to_mp4(DETECCIONS_NORMAL, out_normal)
    ok2 = concat_yolo_mp4s(DETECCIONS_YOLO, out_yolo)
    print("Resums generats:", ok1, ok2, out_normal, out_yolo)

# ------------------- THREAD: MONITORA HLS .ts I PROCESSA -------------------
class HLSMonitor(threading.Thread):
    def __init__(self, hls_dir, process_fn, poll=POLL_INTERVAL):
        super().__init__(daemon=True)
        self.hls_dir = hls_dir
        self.process_fn = process_fn
        self.poll = poll
        self._stop = threading.Event()
        self.processed = set()

    def run(self):
        print("📡 HLSMonitor: vigilant", self.hls_dir)
        while not self._stop.is_set():
            try:
                for fname in sorted(os.listdir(self.hls_dir)):
                    if not fname.endswith(".ts"):
                        continue
                    if fname in self.processed:
                        continue
                    ts_path = os.path.join(self.hls_dir, fname)
                    # Ensure file is stable (ffmpeg might be writing). Wait a bit if file size is changing.
                    stable = self._wait_stable(ts_path, timeout=4)
                    if not stable:
                        continue
                    # process
                    try:
                        got = self.process_fn(ts_path)
                        if got:
                            # if detected, optionally upload
                            normal_dest = os.path.join(DETECCIONS_NORMAL, fname)
                            # copy done inside process_fn; upload both
                            upload_segment(normal_dest, tipus="normal")
                            # yolo mp4 path:
                            yolo_mp4_name = fname.replace(".ts", ".mp4")
                            yolo_mp4_path = os.path.join(DETECCIONS_YOLO, yolo_mp4_name)
                            if os.path.exists(yolo_mp4_path):
                                upload_segment(yolo_mp4_path, tipus="yolo")
                    except Exception as e:
                        print("⚠️ Error processant ts:", ts_path, e)
                    self.processed.add(fname)
            except FileNotFoundError:
                pass
            except Exception as e:
                print("HLSMonitor error:", e)
            time.sleep(self.poll)

    def stop(self):
        self._stop.set()

    def _wait_stable(self, path, timeout=4):
        """
        Wait until file size is stable for a short period to avoid reading incomplete .ts.
        """
        try:
            last_size = -1
            elapsed = 0
            while elapsed < timeout:
                if not os.path.exists(path):
                    return False
                size = os.path.getsize(path)
                if size == last_size and size > 0:
                    return True
                last_size = size
                time.sleep(0.5)
                elapsed += 0.5
            return True
        except Exception:
            return False

# ------------------- PROCESS ONE TS: analitza TOTS els frames i crea copy + yolo mp4 -------------------
def process_ts_full(ts_path, conf_thresh=CONF_THRESHOLD):
    """
    Llegeix tots els frames del .ts. Si detecta ocells en algun frame:
      - copia .ts a DETECCIONS_NORMAL
      - crea un .mp4 amb les caixes a DETECCIONS_YOLO
    Retorna True si s'ha detectat i guardat.
    """
    cap = cv2.VideoCapture(ts_path)
    if not cap.isOpened():
        print("❌ No s'ha pogut obrir", ts_path)
        return False

    w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS) or 25.0

    fname = os.path.basename(ts_path)
    yolo_out_name = fname.replace(".ts", ".mp4")
    yolo_out_path = os.path.join(DETECCIONS_YOLO, yolo_out_name)

    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    out_yolo = cv2.VideoWriter(yolo_out_path, fourcc, fps, (w, h))

    detected_any = False
    frame_count = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frame_count += 1

        try:
            # Use detector on frame
            res = detector(frame, conf=conf_thresh)
            boxes = res[0].boxes
            if boxes and len(boxes) > 0:
                detected_any = True
                for box in boxes:
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    conf = float(box.conf[0])
                    cls = int(box.cls[0])
                    # Només seguim si és ocell (classe 14 a COCO)
                    if DETECTION_CLASS is not None and cls != DETECTION_CLASS:
                        continue

                    label = "Bird"

                    # Intentar identificar espècie amb el model best.pt
                    roi = frame[y1:y2, x1:x2]
                    if identificador is not None and roi.size != 0:
                        try:
                            r_id = identificador(roi, conf=ID_CONF_THRESHOLD)
                            if r_id and len(r_id[0].boxes) > 0:
                                clsid = int(r_id[0].boxes[0].cls[0])
                                conf_ident = float(r_id[0].boxes[0].conf[0])
                                if conf_ident >= ID_CONF_THRESHOLD:
                                    especie = identificador.names[clsid]
                                    label = f"{especie} {conf_ident:.2f}"
                        except Exception as e:
                            pass

                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0,255,0), 2)
                    cv2.putText(frame, label, (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 2)
        except Exception as e:
            print("Error detectant frame:", e)

        # write frame into yolo mp4 (even if no boxes; if none overall, we'll remove file later)
        out_yolo.write(frame)

    cap.release()
    out_yolo.release()

    if detected_any:
        # copy original .ts to deteccions normal
        try:
            dest = os.path.join(DETECCIONS_NORMAL, fname)
            shutil.copy(ts_path, dest)
            print(f"✅ Copiat {fname} a {DETECCIONS_NORMAL} (frames processats: {frame_count})")
            return True
        except Exception as e:
            print("⚠️ Error copiant .ts:", e)
            # keep yolo file maybe for debug
            return True
    else:
        # No deteccions: eliminem el mp4 creat per estalviar espai
        try:
            if os.path.exists(yolo_out_path):
                os.remove(yolo_out_path)
        except Exception:
            pass
        print(f"ℹ️ No deteccions a {fname}")
        return False

# ------------------- RESET LOCALS + API -------------------
def reset_hls_local():
    """Esborra carpeta HLS local i la recrea"""
    try:
        shutil.rmtree(HLS_DIR)
    except FileNotFoundError:
        pass
    os.makedirs(HLS_DIR, exist_ok=True)
    print("♻️ Reiniciat HLS local (Edge).")

def reset_stream():
    """Atura ffmpeg + monitor, neteja locals i API, i reinicia"""
    global ffmpeg_proc, hls_monitor
    print("🔁 Reiniciant stream...")

    if ffmpeg_proc:
        ffmpeg_proc.kill()
        ffmpeg_proc = None
    if hls_monitor:
        hls_monitor.stop()
        hls_monitor = None

    reset_hls_local()

    try:
        r = requests.post(RESET_ENDPOINT, timeout=10)
        print("📤 Reset API:", r.status_code, r.text)
    except Exception as e:
        print("⚠️ Error reset API:", e)

# ------------------- MAIN: captura, detecció en temps real i monitor HLS -------------------
running = True
ffmpeg_proc = None
hls_monitor = None

def signal_handler(sig, frame):
    global running
    print("📴 Senyal d'aturada rebut. S'aturarà tot correcte...")
    running = False

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

def main():
    global ffmpeg_proc, hls_monitor, running

    # 1) Obrir càmera amb OpenCV (com a source principal per detecció real time)
    cap = cv2.VideoCapture(RTSP_OR_CAMERA)
    if not cap.isOpened():
        print("❌ Error: no s'ha pogut obrir la càmera/RTSP.")
        return

    frame_w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS) or FPS_FF

    # 2) Inicia ffmpeg per HLS (stdin)
    ffmpeg_proc, m3u8_path = start_ffmpeg_hls(frame_w, frame_h, fps=fps)
    print("📡 FFmpeg HLS iniciat ->", m3u8_path)

    # 3) Inicia el servidor Flask en background per servir HLS
    flask_thread = threading.Thread(target=run_flask_server, daemon=True)
    flask_thread.start()
    time.sleep(0.5)

    # 4) Inicia monitor de HLS per processar .ts
    hls_monitor = HLSMonitor(HLS_DIR, process_ts_full, poll=POLL_INTERVAL)
    hls_monitor.start()

    # 5) Opcional: crea entrada a la BD per aquest vídeo (com feies)
    video_start_ts = datetime.now()
    if SAVE_RAW_FULL_VIDEO:
        video_name = f"video_{video_start_ts.strftime('%Y%m%d_%H%M%S')}"
        raw_video_path = os.path.join(RAW_DIR, f"{video_name}.mp4")
        # No gravem per OpenCV; ffmpeg rebre stdin. Si vols guardar raw complet, es podria fer un segon ffmpeg, però
        # per simplicitat avui no implementem un doble piping. Pots desar fragments ja processats.
    else:
        raw_video_path = None

    print("▶️ Iniciant bucle principal: detecció en temps real i enviament a ffmpeg... (prem Ctrl+C per aturar)")

    # dades per tracking/avistaments
    video_start_timestamp = datetime.now()
    tracking_info = {}
    fragments_list = []
    ID_VIDEO = None

    # Crea entrada Video a la BD
    if API_BASE:
        try:
            video_payload = {
                "IDUsuario": ID_USUARIO,
                "IDCamara": ID_CAMARA,
                "Nombre": f"stream_{video_start_timestamp.strftime('%Y%m%d_%H%M%S')}",
                "Dia": video_start_timestamp.date().isoformat(),
                "ruta_video": raw_video_path or ""
            }
            r = requests.post(VIDEOS_ENDPOINT, json=video_payload, timeout=10)
            if r.ok:
                jsonr = r.json()
                ID_VIDEO = jsonr.get("ID") or jsonr.get("id") or None
                print("✅ Entrada Video creada a API, ID_VIDEO=", ID_VIDEO)
            else:
                print("⚠️ No s'ha pogut crear Video a l'API:", r.status_code, r.text)
        except Exception as e:
            print("⚠️ Error creant entrada video a l'API:", e)

    last_ff_write = 0.0
    cycle_start = time.time()
    CYCLE_HOURS = 24
    try:
        while running:
            ret, frame = cap.read()
            if not ret:
                print("⚠️ Frame no rebut, esperant...")
                time.sleep(0.5)
                continue

            #Envia frame a ffmpeg stdin per generar HLS
            try:
                if ffmpeg_proc and ffmpeg_proc.stdin:
                    ffmpeg_proc.stdin.write(frame.tobytes())
                    last_ff_write = time.time()
            except Exception as e:
                print("⚠️ Error escrivint a ffmpeg stdin:", e)

            #Processament YOLO + SORT en temps real (com a deteccio.py)
            try:
                res = detector(frame, conf=CONF_THRESHOLD)
                boxes = res[0].boxes
                detections_per_sort = []
                if boxes and len(boxes) > 0:
                    for box in boxes:
                        x1, y1, x2, y2 = box.xyxy[0].tolist()
                        conf = float(box.conf[0])
                        detections_per_sort.append([x1, y1, x2, y2, conf])
                    dets_arr = np.array(detections_per_sort)
                else:
                    dets_arr = np.empty((0,5))

                tracks = tracker.update(dets_arr)

                # manage tracks like your previous code: create avistament entries on new tracks
                current_time = datetime.now()
                elapsed_seconds = int((current_time - video_start_timestamp).total_seconds())
                ids_current = set()

                for tr in tracks:
                    x1, y1, x2, y2, sort_id = tr
                    sort_id = int(sort_id)
                    ids_current.add(sort_id)
                    if sort_id not in tracking_info:
                        # new track: attempt identification with identificador
                        roi = frame[int(y1):int(y2), int(x1):int(x2)]
                        IDEspecie = None
                        conf_ident = None
                        if identificador is not None and roi.size != 0:
                            try:
                                r_id = identificador(roi, conf=CONF_THRESHOLD)
                                if r_id and len(r_id[0].boxes) > 0:
                                    clsid = int(r_id[0].boxes[0].cls[0])
                                    conf_ident = float(r_id[0].boxes[0].conf[0])
                                    if conf_ident >= ID_CONF_THRESHOLD:
                                        IDEspecie = identificador.names[clsid]
                            except Exception as e:
                                pass

                        # register tracking_info and optionally send avistament
                        tracking_info[sort_id] = {
                            "inicio": elapsed_seconds,
                            "final": elapsed_seconds,
                            "IDEspecie": IDEspecie,
                            "confianza": conf_ident or 0,
                            "id_avistament": None
                        }

                        # send initial avistament (if we have IDEspecie)
                        if API_BASE:
                            payload = {
                                "IDVideo": ID_VIDEO or 0,
                                "IDEspecie": IDEspecie or 0,
                                "fecha_aparicion": current_time.isoformat(),
                                "fecha_desaparicion": current_time.isoformat(),
                                "inicio_video_segons": elapsed_seconds,
                                "final_video_segons": elapsed_seconds,
                                "es_audio": False,
                                "confianza": tracking_info[sort_id]["confianza"]
                            }
                            try:
                                rr = requests.post(AVISTAMENTS_ENDPOINT, json=payload, timeout=10)
                                if rr.ok:
                                    tracking_info[sort_id]["id_avistament"] = rr.json().get("ID")
                                    # print("Avistament creat:", rr.json())
                            except Exception as e:
                                pass
                    else:
                        tracking_info[sort_id]["final"] = elapsed_seconds
                        # optional: update avistament end time periodically
                        aid = tracking_info[sort_id].get("id_avistament")
                        if aid:
                            try:
                                update_payload = {
                                    "fecha_desaparicion": current_time.isoformat(),
                                    "final_video_segons": tracking_info[sort_id]["final"]
                                }
                                requests.put(f"{AVISTAMENTS_ENDPOINT}/{aid}", json=update_payload, timeout=5)
                            except Exception:
                                pass

                # detect disappeared tracks
                previous_ids = set(tracking_info.keys())
                disappeared = previous_ids - ids_current
                for did in disappeared:
                    info = tracking_info.get(did)
                    if info:
                        dur = info["final"] - info["inicio"]
                        if dur > 0:
                            fragments_list.append((info["inicio"], info["final"]))
                        del tracking_info[did]

            except Exception as e:
                print("⚠️ Error processing frame realtime:", e)
            time.sleep(0.001)
            if time.time() - cycle_start > CYCLE_HOURS * 3600:
                print("⏰ Fi de cicle, reiniciant...")
                break   # surt del while -> entra al finally -> generar_resum_final() + reset_stream()

    finally:
        print("🔁 Sortint bucle principal — netejant...")
        # tancar ffmpeg stdin per tancar la creació HLS
        try:
            if ffmpeg_proc and ffmpeg_proc.stdin:
                ffmpeg_proc.stdin.close()
        except Exception:
            pass
        # donar temps que ffmpeg finalitzi segments
        time.sleep(1.0)
        # atura monitor i flask
        if hls_monitor:
            hls_monitor.stop()
        time.sleep(0.3)
        # finalize generation of resums
        generar_resum_final()
        reset_stream()
        cap.release()
        print("✅ Finalitzat i reiniciat.")
        main()

if __name__ == "__main__":
    main()
