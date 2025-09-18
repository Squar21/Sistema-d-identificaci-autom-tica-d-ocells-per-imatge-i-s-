# 📹 Camara - Detecció d'Ocells en Directe

Aquest projecte executa detecció d’ocells en temps real fent servir **YOLOv8** i el tracker **SORT**.  
El sistema processa el flux de vídeo de la càmera, aplica detecció i genera un streaming en format **HLS (.m3u8 + .ts)**, a més de guardar resultats.

---

## 🚀 Requisits

- Python 3.9+  
- Virtualenv recomanat  
- Models YOLO (`yolov8n.pt`, `best.pt`) ja inclosos  

---

## 📦 Instal·lació

```bash
# Crear entorn virtual
python -m venv venv
source venv/bin/activate   # Linux / Mac
venv\Scripts\activate      # Windows

# Instal·lar dependències
pip install -r requirements.txt

# Instal·lar dependències del tracker SORT
pip install -r sort/requirements.txt
```

---

## ▶️ Execució

Per iniciar la detecció en directe:

```bash
python analisis_live_v2.py
```

El sistema genera:
- Flux HLS en la carpeta `directe/` (`stream.m3u8` i segments `.ts`)  
- Resultats en `resultats/`  
- Vídeos de deteccions a `deteccions/yolo/`

---

## 📁 Estructura

```
Camara/
├── analisis_live_v2.py      # Script principal
├── best.pt                  # Model YOLO entrenat
├── yolov8n.pt               # Model YOLO base
├── sort/                    # Submòdul SORT
├── directe/                 # Sortida HLS streaming
├── deteccions/              # Vídeos amb deteccions
└── resultats/               # Fitxers de resultats
```

---

## ✨ Notes

- Pots substituir `best.pt` pel teu propi model entrenat.  
- Per retransmetre en un servidor, connecta la carpeta `directe/` al teu backend o frontend.  
