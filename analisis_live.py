from ultralytics import YOLO
import cv2
import numpy as np

# Cargar el modelo YOLO
model = YOLO("yolov8n.pt")

# Configurar la recepción del stream UDP
UDP_IP = "0.0.0.0"  # Escucha en todas las interfaces
UDP_PORT = 1234
cap = cv2.VideoCapture(f"udp://@{UDP_IP}:{UDP_PORT}", cv2.CAP_FFMPEG)

if not cap.isOpened():
    print("Error: No se pudo abrir el stream UDP.")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: Frame no recibido.")
        break

    # Detección con YOLO
    results = model(frame)

    # Dibujar bounding boxes
    for result in results:
        boxes = result.boxes.xyxy
        classes = result.boxes.cls
        confidences = result.boxes.conf

        for box, cls, conf in zip(boxes, classes, confidences):
            x1, y1, x2, y2 = map(int, box)
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            label = f"{model.names[int(cls)]} {conf:.2f}"
            cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

    cv2.imshow("Live Tracking", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()