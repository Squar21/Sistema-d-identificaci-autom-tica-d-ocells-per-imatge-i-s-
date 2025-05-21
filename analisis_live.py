from ultralytics import YOLO
import cv2
import numpy as np
from flask import Flask, Response
import threading
import time
from sort import Sort  # Asegúrate de tener esta carpeta

app = Flask(__name__)

# Cargar el modelo YOLO
model = YOLO("best.pt")

# Configuración del stream UDP
UDP_IP = "0.0.0.0"
UDP_PORT = 1234

# Variable global para el frame actual
current_frame = None
lock = threading.Lock()
stream_active = False

# Tracker SORT y umbral de confianza
tracker = Sort()
CONFIDENCE_THRESHOLD = 0.65

class_names = [
    "Abellerol comú", "Abellerol de Pèrsia", "Agró blanc", "Agró roig", "Aligot calçat", "Aligot comú",
    "Aligot rogenc", "Aligot vesper europeu", "Alosa banyuda", "Alosa becuda", "Alosa eurasiàtica",
    "Aratinga mitrada", "Arpella cendrosa", "Arpella comuna", "Arpella pàl·lida comuna", "Arpella pàl·lida russa",
    "Astor comú", "Aufrany comú", "Baldriga balear", "Baldriga capnegra", "Baldriga cendrosa atlàntica",
    "Baldriga cendrosa mediterrània", "Baldriga grisa", "Baldriga mediterrània", "Ballester comú",
    "Balquer", "Batallaire", "Bec d'alena comú", "Bec de coral cuanegre", "Bec de coral del Senegal",
    "Bec de serra gros", "Bec de serra mitjà", "Bec de serra petit", "Becada eurasiàtica", "Becadell comú",
    "Becadell gros", "Becadell sord", "Becplaner comú", "Becut eurasiàtic", "Bernat pescaire", "Bitxac comú",
    "Bitxac rogenc", "Bitxac siberià", "Bitó comú", "Bitó nord-americà", "Blauet comú", "Boscaler comú",
    "Boscaler pintat gros", "Boscarla d'aigua", "Boscarla d'arrossar", "Boscarla de canyar", "Boscarla dels joncs",
    "Boscarla dels matolls", "Boscarla menjamosquits", "Boscarla mostatxuda", "Bosquerola zebrada",
    "Botxí ibèric", "Botxí septentrional", "Bruel eurasiàtic", "Busqueta bruna", "Busqueta comuna",
    "Busqueta icterina", "Cabusset comú", "Cabussó collnegre", "Cabussó emplomallat", "Cabussó gris",
    "Cabussó orellut", "Cadernera europea", "Calàbria agulla", "Calàbria grossa", "Calàbria petita",
    "Calàndria comuna", "Camallarga comú", "Capsigrany bru", "Capsigrany comú", "Capsigrany pàl·lid",
    "Capó reial", "Cargolet eurasiàtic", "Cercavores alpí", "Cigne cantaire", "Cigne mut", "Cigne negre",
    "Cigne petit", "Cigonya blanca", "Cigonya negra", "Cogullada comuna", "Cogullada fosca", "Colltort comú",
    "Colom roquer", "Corb comú", "Corb marí emplomallat", "Corb marí gros", "Corb marí pigmeu",
    "Cornella emmantellada", "Cornella negra", "Corredor del desert", "Corriol camanegre", "Corriol de Leschenault",
    "Corriol gros", "Corriol petit", "Corriol pit-roig", "Cotoliu", "Cotorra de Kramer", "Cotorreta pitgrisa",
    "Cotxa blava", "Cotxa cua-roja", "Cotxa cuablava", "Cotxa diademada", "Cotxa fumada", "Cruixidell",
    "Cuaenlairat rogenc", "Cucut comú", "Cucut reial europeu", "Cuereta blanca", "Cuereta citrina",
    "Cuereta de Txukotka", "Cuereta groga", "Cuereta torrentera", "Curroc comú", "Còlit del desert",
    "Còlit gris", "Còlit negre", "Còlit pàl·lid", "Còlit ros occidental", "Daurada americana",
    "Daurada del Pacífic", "Daurada grossa", "Duc eurasiàtic", "Durbec comú", "Elani comú",
    "Enganyapastors europeu", "Escorxador comú", "Escuraflascons becfí", "Escuraflascons becgròs",
    "Escuraflascons de Wilson", "Esmirla", "Esparver comú", "Esplugabous", "Estornell comú",
    "Estornell negre", "Estornell rosat", "Faisà comú", "Falciot cuablanc petit", "Falciot negre",
    "Falciot pàl·lid", "Falcó cama-roig", "Falcó d'Elionor", "Falcó llaner", "Falcó mostatxut europeu",
    "Falcó pelegrí", "Falcó sacre", "Flamenc menut", "Flamenc rosat", "Fotja banyuda", "Fotja comuna",
    "Fraret atlàntic", "Fredeluga cuablanca", "Fredeluga europea", "Fredeluga gregària", "Fumarell alablanc",
    "Fumarell carablanc", "Fumarell negre", "Gafarró europeu", "Gaig blau comú", "Gaig eurasiàtic",
    "Gall fer comú", "Gamarús eurasiàtic", "Gamba groga petita", "Gamba roja comuna", "Gamba roja pintada",
    "Gamba verda", "Ganga eurasiàtica", "Garsa de mar eurasiàtica", "Garsa eurasiàtica", "Gavina capblanca",
    "Gavina capnegra americana", "Gavina capnegra mediterrània", "Gavina cendrosa", "Gavina corsa",
    "Gavina de Bonaparte", "Gavina de Delaware", "Gavina de Franklin", "Gavina menuda", "Gavina riallera",
    "Gavineta cuaforcada", "Gavineta de tres dits", "Gavinot atlàntic", "Gavinot polar",
    "Gavià argentat de potes roses", "Gavià caspi", "Gavià de potes grogues", "Gavià fosc", "Gavot",
    "Gralla becgroga", "Gralla becvermella", "Gralla occidental", "Grasset de costa", "Grasset de muntanya",
    "Gratapalles", "Graula", "Griva cerdana", "Griva comuna", "Grua europea", "Grèvol comú", "Guatlla comuna",
    "Guatlla maresa eurasiàtica", "Hortolà comú", "Ibis sagrat africà", "Junco fosc", "Leiòtrix bec-roig",
    "Llucareta europea", "Lluer eurasiàtic", "Mallerenga blava eurasiàtica", "Mallerenga carbonera",
    "Mallerenga cuallarga eurasiàtica", "Mallerenga d'aigua", "Mallerenga de bigotis",
    "Mallerenga emplomallada europea", "Mallerenga petita", "Malvasia capblanca", "Malvasia de Jamaica",
    "Martinet blanc comú", "Martinet de nit comú", "Martinet dels esculls", "Martinet menut comú",
    "Martinet ros comú", "Mascarell atlàntic", "Mascarell bru", "Mascarell cama-roig", "Mastegatatxes",
    "Merla blava", "Merla comuna", "Merla d'aigua europea", "Merla de pit blanc", "Merla roquera comuna",
    "Milà negre", "Milà reial", "Morell buixot", "Morell cap-roig", "Morell d'ulls grocs", "Morell de collar",
    "Morell de plomall", "Morell menut", "Morell xocolater", "Mosquiter boreal", "Mosquiter comú",
    "Mosquiter de Hume", "Mosquiter de doble ratlla", "Mosquiter de passa", "Mosquiter fosc",
    "Mosquiter ibèric", "Mosquiter pàl·lid occidental", "Mosquiter reietó", "Mosquiter verdós",
    "Mosquiter xiulaire", "Mussol banyut", "Mussol comú", "Mussol emigrant", "Mussol pirinenc",
    "Mussolet eurasiàtic", "Oca comuna", "Oca d'Egipte", "Oca de bec curt", "Oca de collar",
    "Oca de galta blanca", "Oca del Canadà", "Oca pradenca de taigà", "Oca pradenca de tundra",
    "Oca riallera grossa", "Ocell de tempesta de Leach", "Ocell de tempesta europeu",
    "Ocell de tempesta oceànic", "Ocell sedós europeu", "Oreneta comuna", "Oreneta cua-rogenca",
    "Oreneta cuablanca comuna", "Oreneta de ribera comuna", "Oriol eurasiàtic", "Papamosques de collar",
    "Papamosques gris", "Papamosques mediterrani", "Papamosques menut", "Pardal comú", "Pardal d'ala blanca",
    "Pardal de bardissa europeu", "Pardal de passa", "Pardal roquer", "Pardal xarrec", "Paràsit cuaample",
    "Paràsit cuallarg", "Paràsit cuapunxegut", "Paràsit gros boreal", "Passerell eurasiàtic",
    "Passerell gorjanegre", "Pela-roques", "Pelicà blanc comú", "Perdiu blanca", "Perdiu de mar europea",
    "Perdiu roja", "Perdiu xerra", "Pica-soques eurasiàtic", "Picot garser gros", "Picot garser mitjà",
    "Picot garser petit", "Picot negre eurasiàtic", "Picot verd comú", "Picot verd ibèric", "Pigarg cuablanc",
    "Pigre gris", "Pinsà borroner eurasiàtic", "Pinsà carminat", "Pinsà comú", "Pinsà mec", "Pinsà trompeter",
    "Pioc salvatge eurasiàtic", "Pit-roig", "Piula de Hodgson", "Piula dels arbres", "Piula gorja-roja",
    "Piula grossa", "Polit cantaire", "Polla blava comuna", "Polla blava d'Allen", "Polla d'aigua comuna",
    "Polla menuda", "Polla pintada", "Puput comuna", "Rasclet europeu", "Rascletó", "Rascló occidental",
    "Raspinell comú", "Raspinell pirinenc", "Reietó eurasiàtic", "Remena-rocs comú", "Repicatalons de Lapònia",
    "Repicatalons eurasiàtic", "Repicatalons petit", "Repicatalons rústic", "Roquerol eurasiàtic",
    "Rossinyol blau", "Rossinyol bord comú", "Rossinyol comú", "Siboc", "Siseta cendrosa", "Siseta comuna",
    "Sisó comú", "Sit blanc", "Sit capblanc", "Sit capnegre", "Sit gorjablanc", "Sit negre",
    "Somorgollaire comú", "Tallareta comuna", "Tallareta cuallarga", "Tallareta sarda", "Tallarol capnegre",
    "Tallarol de Moltoni", "Tallarol de casquet", "Tallarol de garriga occidental",
    "Tallarol de garriga oriental", "Tallarol emmascarat occidental", "Tallarol gros", "Tallarol trencamates",
    "Tallarol xerraire", "Teixidor eurasiàtic", "Terrerola comuna", "Terrerola cuabarrada",
    "Terrerola rogenca mediterrània", "Territ becadell", "Territ becllarg", "Territ camallarg",
    "Territ cuablanc", "Territ de Baird", "Territ de Temminck", "Territ de tres dits", "Territ fosc",
    "Territ gros", "Territ menut comú", "Territ menut del Canadà", "Territ pectoral", "Territ rogenc",
    "Territ variant", "Tetolet becllarg", "Tetolet gris", "Titella", "Tord ala-roig", "Tord comú",
    "Tord de Naumann", "Torlit comú", "Trenca", "Trencalòs", "Trencanous eurasiàtic", "Trencapinyes comú",
    "Trist", "Trobat", "Tudó", "Tètol cuabarrat", "Tètol cuanegre", "Tórtora del Senegal",
    "Tórtora eurasiàtica", "Tórtora turca", "Valona", "Verderola", "Verdum europeu", "Vireó ullvermell",
    "Voltor comú", "Voltor de Rüppell", "Voltor negre", "Xarrasclet", "Xarxet alablau", "Xarxet americà",
    "Xarxet comú", "Xarxet marbrenc", "Xatrac becllarg", "Xatrac bengalí", "Xatrac comú", "Xatrac elegant",
    "Xatrac embridat", "Xatrac gros", "Xatrac menut comú", "Xatrac reial africà", "Xatrac reial americà",
    "Xatrac rosat", "Xatrac àrtic", "Xibec cap-roig", "Xivita comuna", "Xivitona comuna", "Xivitona maculada",
    "Xixella", "Xoriguer comú", "Xoriguer petit", "Xot eurasiàtic", "Xurra", "Àguila calçada comuna",
    "Àguila cridanera", "Àguila cuabarrada", "Àguila daurada", "Àguila imperial ibèrica", "Àguila marcenca",
    "Àguila pescadora", "Àguila pomerània", "Ànec blanc", "Ànec canyella", "Ànec collverd", "Ànec cuallarg",
    "Ànec cullerot comú", "Ànec fosc eurasiàtic", "Ànec glacial", "Ànec griset", "Ànec mandarí",
    "Ànec negre comú", "Ànec negrós", "Ànec xiulador eurasiàtic", "Èider comú", "Èider reial",
    "Òliba comuna", "bird"
]

def create_blank_frame():
    frame = np.zeros((480, 640, 3), dtype=np.uint8)
    text = "No video signal"
    font = cv2.FONT_HERSHEY_SIMPLEX
    text_size = cv2.getTextSize(text, font, 1, 2)[0]
    text_x = (frame.shape[1] - text_size[0]) // 2
    text_y = (frame.shape[0] + text_size[1]) // 2
    cv2.putText(frame, text, (text_x, text_y), font, 1, (255, 255, 255), 2)
    return frame

def process_frames():
    global current_frame, stream_active
    cap = None
    last_retry_time = 0
    retry_delay = 5

    while True:
        current_time = time.time()

        if cap is None or not stream_active:
            if current_time - last_retry_time > retry_delay:
                print("Intentando conectar al stream UDP...")
                try:
                    if cap is not None:
                        cap.release()
                    cap = cv2.VideoCapture(f"udp://@{UDP_IP}:{UDP_PORT}?fifo_size=5000000&overrun_nonfatal=1", cv2.CAP_FFMPEG)
                    if cap.isOpened():
                        print("Conexión establecida con el stream UDP")
                        stream_active = True
                    else:
                        print("Error: No se pudo abrir el stream UDP")
                except Exception as e:
                    print(f"Error al conectar: {str(e)}")
                last_retry_time = current_time

        if stream_active and cap is not None:
            ret, frame = cap.read()
            if not ret:
                print("Error: Frame no recibido. Stream puede estar caído.")
                stream_active = False
                with lock:
                    current_frame = cv2.imencode('.jpg', create_blank_frame())[1].tobytes()
                continue

            try:
                results = model(frame)[0]
                boxes = results.boxes.xyxy.cpu().numpy()
                confs = results.boxes.conf.cpu().numpy()
                classes = results.boxes.cls.cpu().numpy()
                
                # Filtrar per confiança
                mask = confs > CONFIDENCE_THRESHOLD
                boxes = boxes[mask]
                confs = confs[mask]
                classes = classes[mask]
                
                # Preparar deteccions per SORT (format [x1,y1,x2,y2,score])
                detections = np.column_stack((boxes, confs))
                
                # Actualitzar tracker
                tracks = tracker.update(detections).astype(int)
                
                # Dibuixar resultats
                for track in tracks:
                    x1, y1, x2, y2, track_id = track
                    # Buscar la classe corresponent a la bbox més propera
                    # (SORT no manté la classe, així que busquem la bbox més propera)
                    class_name = ""
                    if len(boxes) > 0:
                        ious = []
                        for box in boxes:
                            # IOU simple per trobar la bbox més propera
                            xx1 = max(x1, int(box[0]))
                            yy1 = max(y1, int(box[1]))
                            xx2 = min(x2, int(box[2]))
                            yy2 = min(y2, int(box[3]))
                            w = max(0, xx2 - xx1)
                            h = max(0, yy2 - yy1)
                            inter = w * h
                            area1 = (x2 - x1) * (y2 - y1)
                            area2 = (int(box[2]) - int(box[0])) * (int(box[3]) - int(box[1]))
                            union = area1 + area2 - inter
                            ious.append(inter / union if union > 0 else 0)
                        idx = np.argmax(ious)
                        class_id = int(classes[idx])
                        class_name = class_names[class_id] if class_id < len(class_names) else str(class_id)
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.putText(frame, f"ID:{track_id} {class_name}", (x1, y1 - 10), 
                               cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

                with lock:
                    current_frame = cv2.imencode('.jpg', frame)[1].tobytes()

            except Exception as e:
                print(f"Error procesando frame: {str(e)}")
                stream_active = False
                with lock:
                    current_frame = cv2.imencode('.jpg', create_blank_frame())[1].tobytes()

        if not stream_active:
            with lock:
                current_frame = cv2.imencode('.jpg', create_blank_frame())[1].tobytes()

        time.sleep(0.03)

@app.route('/video_feed')
def video_feed():
    def generate():
        global current_frame
        while True:
            with lock:
                if current_frame is not None:
                    yield (b'--frame\r\n'
                           b'Content-Type: image/jpeg\r\n\r\n' + current_frame + b'\r\n')
            time.sleep(0.05)
    return Response(generate(), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    threading.Thread(target=process_frames, daemon=True).start()
    app.run(host='0.0.0.0', port=5000)
