# 🌐 Server - Frontend i API per al Sistema de Detecció

Aquest projecte combina:  
1. Una aplicació **React** (frontend) per visualitzar el vídeo i informació.  
2. Un servidor **Flask** (`web/flask_api_endpoints.py`) que actua com a API per comunicar-se amb el sistema de càmeres.

---

## 🚀 Requisits

- Node.js 18+  
- npm o yarn  
- Python 3.9+ (per a l’API Flask)

---

## 📦 Instal·lació

### 🔹 Backend (Flask API)
```bash
cd web

# Crear entorn virtual
python -m venv venv
source venv/bin/activate   # Linux / Mac
venv\Scripts\activate      # Windows

# Instal·lar dependències
pip install -r ../requirements.txt

# Iniciar API
python flask_api_endpoints.py
```

La API Flask s’executarà a `http://localhost:5000`.

---

### 🔹 Frontend (React)
```bash
# A la carpeta Server
cd web
python3 -m http.server 8080
```

El frontend React s’executarà a `http://localhost:3000`.

---

## 📁 Estructura

```
Server/
├── package.json             # Dependències React
├── src/                     # Codi font React
├── public/                  # Arxius públics
└── web/
    ├── flask_api_endpoints.py  # API Flask
    ├── index.html
    └── assets/                 # CSS + JS
```

---

## ✨ Notes

- El frontend React consumeix dades de l’API Flask.  
- Pots adaptar els endpoints dins `flask_api_endpoints.py` per connectar-lo amb la base de dades o el mòdul de detecció.  
