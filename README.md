# 🐦 Sistema de Detecció i Identificació Automàtica d'Ocells

Aquest projecte està format per dos mòduls principals:

1. **Camara/** → Sistema d’adquisició i processament de vídeo en temps real amb detecció d’ocells mitjançant **YOLOv8** i el tracker **SORT**.  
2. **Server/** → Aplicació web que combina un **frontend React** amb una **API Flask**, permetent visualitzar el vídeo i consultar dades de detecció.

---

## 🎯 Objectiu

El sistema permet:
- Detectar ocells en temps real amb models YOLO.  
- Fer **tracking** de les deteccions amb l’algoritme **SORT**.  
- Generar **streaming HLS (.m3u8 + .ts)** per retransmetre el vídeo processat.  
- Exposar una **API Flask** per comunicar les deteccions al servidor.  
- Oferir un **frontend React** per visualitzar el flux i la informació associada. 
