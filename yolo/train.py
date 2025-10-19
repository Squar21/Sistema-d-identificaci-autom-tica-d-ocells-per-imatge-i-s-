from ultralytics import YOLO
import os

# ------------------------------
# CONFIGURACIÓ DEL CAMÍ DEL MODEL I DEL DATASET
# ------------------------------

# Ruta al fitxer de configuració 'data.yaml'
DATASET_PATH = os.path.abspath('BirdsDatasetSplit/data.yaml')  # Canvia si el teu path és diferent

# Ruta per guardar els resultats
PROJECT_DIR = 'runs/detect'  # Carpeta on es guardaran els resultats d'entrenament
EXPERIMENT_NAME = 'bird457_yolov8n'  # Nom que vols donar a l'entrenament

# ------------------------------
# CONFIGURACIÓ DEL MODEL I ENTRENAMENT
# ------------------------------

# Càrrega del model base YOLOv8n (pots canviar per yolov8s/m/l/x segons el teu hardware)
model = YOLO('runs/detect/bird457_yolov8n10/weights/best.pt')  #runs/detect/bird457_yolov8n/weights/last.pt yolov8n.pt Usa yolov8s.pt o més gran si tens GPU potent

# Entrenament
model.train(
    data=DATASET_PATH,        # Fitxer data.yaml
    epochs=100,               # Número d'èpoques
    imgsz=640,                # Mida de la imatge (640 és estàndard)
    batch=16,                 # Batch size (ajusta segons GPU/VRAM)
    name=EXPERIMENT_NAME,     # Nom de l'experiment
    project=PROJECT_DIR,      # Carpeta base
    workers=4,                # Threads per carregar dades
    patience=20,              # Early stopping (20 èpoques sense millora)
    val=True,                  # Fa validació automàtica després de cada època

    freeze=10,              # Congela les capes del model base per entrenar només les capes noves
    translate=0.3,          # Augmentació de traducció (0.3 és un valor comú per augmentar la robustesa del model)
    scale=0.7,              # Augmentació d'escala (0.7 és un valor comú per augmentar la robustesa del model)
    fliplr=0.5,            # Augmentació de flip vertical (0.1 és un valor comú)
    mosaic=True,          # Habilita l'augment de mosaic (millora la robustesa del model)
    close_mosaic=50, 
    cutmix=True,          # Habilita CutMix (millora la robustesa del model)
    erasing=0.4
)
