import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
import os, shutil

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:8080"}})


# Connexió a la base de dades
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="toor123!",
    database="yolo"
)
cursor = conn.cursor(dictionary=True)

# ---------------------- USUARIO ----------------------
@app.route("/usuarios", methods=["GET"])
def get_usuarios():
    cursor.execute("SELECT * FROM Usuario")
    return jsonify(cursor.fetchall())

@app.route("/usuarios", methods=["POST"])
def add_usuario():
    data = request.json
    cursor.execute("INSERT INTO Usuario (Nik, contraseña, correo) VALUES (%s, %s, %s)",
                   (data["Nik"], data["contraseña"], data["correo"]))
    conn.commit()
    return jsonify({"message": "Usuario creado"}), 201

@app.route("/usuarios/<int:id>", methods=["PUT"])
def update_usuario(id):
    data = request.json
    cursor.execute("UPDATE Usuario SET Nik=%s, contraseña=%s, correo=%s WHERE ID=%s",
                   (data["Nik"], data["contraseña"], data["correo"], id))
    conn.commit()
    return jsonify({"message": "Usuario actualizado"})

@app.route("/usuarios/<int:id>", methods=["DELETE"])
def delete_usuario(id):
    cursor.execute("DELETE FROM Usuario WHERE ID=%s", (id,))
    conn.commit()
    return jsonify({"message": "Usuario eliminado"})

# ---------------------- CAMARA ----------------------
@app.route("/camaras", methods=["GET"])
def get_camaras():
    cursor.execute("SELECT * FROM Camara")
    return jsonify(cursor.fetchall())

@app.route("/camaras", methods=["POST"])
def add_camara():
    data = request.json
    cursor.execute("INSERT INTO Camara (IDUsuario, Nombre, ciudad, pais, latitud, longitud) VALUES (%s, %s, %s, %s, %s, %s)",
                   (data["IDUsuario"], data["Nombre"], data["ciudad"], data["pais"], data["latitud"], data["longitud"]))
    conn.commit()
    return jsonify({"message": "Camara creada"}), 201

@app.route("/camaras/<int:id>", methods=["PUT"])
def update_camara(id):
    data = request.json
    cursor.execute("UPDATE Camara SET IDUsuario=%s, Nombre=%s, ciudad=%s, pais=%s, latitud=%s, longitud=%s WHERE ID=%s",
                   (data["IDUsuario"], data["Nombre"], data["ciudad"], data["pais"], data["latitud"], data["longitud"], id))
    conn.commit()
    return jsonify({"message": "Camara actualizada"})

@app.route("/camaras/<int:id>", methods=["DELETE"])
def delete_camara(id):
    cursor.execute("DELETE FROM Camara WHERE ID=%s", (id,))
    conn.commit()
    return jsonify({"message": "Camara eliminada"})

# ---------------------- ESPECIE ----------------------
@app.route("/especies", methods=["GET"])
def get_especie_by_name():
    nombre = request.args.get("nombre")
    if nombre:
        cursor.execute("SELECT * FROM Especie WHERE nom_comu = %s", (nombre,))
        especie = cursor.fetchone()
        if especie:
            return jsonify(especie)
        else:
            return jsonify({"error": "Especie no trobada"}), 404
    else:
        return jsonify({"error": "Cal proporcionar el paràmetre 'nombre'"}), 400

@app.route("/especies/<int:id_especie>", methods=["GET"])
def get_nom_comu_by_id(id_especie):
    cursor.execute("SELECT nom_comu FROM Especie WHERE IDEspecie = %s", (id_especie,))
    especie = cursor.fetchone()
    
    if especie:
        return jsonify({"IDEspecie": id_especie, "nom_comu": especie["nom_comu"]})
    else:
        return jsonify({"error": "Espècie no trobada"}), 404

@app.route("/especies", methods=["POST"])
def add_especie():
    data = request.json
    cursor.execute("INSERT INTO Especie (nom_cientific, nom_comu, familia, foto) VALUES (%s, %s, %s, %s)",
                   (data["nom_cientific"], data["nom_comu"], data["familia"], data["foto"]))
    conn.commit()
    return jsonify({"message": "Especie creada"}), 201

@app.route("/especies/<int:id>", methods=["PUT"])
def update_especie(id):
    data = request.json
    cursor.execute("UPDATE Especie SET nom_cientific=%s, nom_comu=%s, familia=%s, foto=%s WHERE ID=%s",
                   (data["nom_cientific"], data["nom_comu"], data["familia"], data["foto"], id))
    conn.commit()
    return jsonify({"message": "Especie actualizada"})

@app.route("/especies/<int:id>", methods=["DELETE"])
def delete_especie(id):
    cursor.execute("DELETE FROM Especie WHERE ID=%s", (id,))
    conn.commit()
    return jsonify({"message": "Especie eliminada"})

# ---------------------- VIDEOS ----------------------
@app.route("/videos", methods=["GET"])
def get_videos():
    cursor.execute("SELECT * FROM Video")
    return jsonify(cursor.fetchall())

@app.route("/videos/usuari/<int:id_usuari>", methods=["GET"])
def get_videos_by_usuari(id_usuari):
    cursor.execute("SELECT * FROM Video WHERE IDUsuario = %s", (id_usuari,))
    return jsonify(cursor.fetchall())

@app.route("/videos", methods=["POST"])
def add_video():
    data = request.json
    cursor.execute("INSERT INTO Video (IDUsuario, IDCamara, Nombre, Dia, ruta_video) VALUES (%s, %s, %s, %s, %s)",
                   (data["IDUsuario"], data["IDCamara"], data["Nombre"], data["Dia"], data["ruta_video"]))
    conn.commit()
    return jsonify({"message": "Vídeo creat correctament", "ID": cursor.lastrowid}), 201

@app.route("/videos/<int:id>", methods=["PUT"])
def update_video(id):
    data = request.json
    cursor.execute("UPDATE Video SET IDUsuario=%s, IDCamara=%s, Nombre=%s, Dia=%s, ruta_video=%s WHERE ID=%s",
                   (data["IDUsuario"], data["IDCamara"], data["Nombre"], data["Dia"], data["ruta_video"], id))
    conn.commit()
    return jsonify({"message": "Video actualizado"})

@app.route("/videos/<int:id>", methods=["DELETE"])
def delete_video(id):
    cursor.execute("DELETE FROM Video WHERE ID=%s", (id,))
    conn.commit()
    return jsonify({"message": "Video eliminado"})

# ---------------------- AVISTAMENTS ----------------------
@app.route("/avistaments", methods=["GET"])
def get_avistaments():
    cursor.execute("SELECT * FROM Avistaments")
    return jsonify(cursor.fetchall())

    #GET /avistaments/video/5?temps=132.5
@app.route("/avistaments/video/<int:id_video>", methods=["GET"])
def get_avistaments_in_range(id_video):
    try:
        temps = float(request.args.get("temps"))

        cursor.execute("""
            SELECT * FROM Avistaments
            WHERE IDVideo = %s
            AND inicio_video_segons >= %s
            AND final_video_segons <= %s
        """, (id_video, temps, temps))
        
        return jsonify(cursor.fetchall())
    except (TypeError, ValueError):
        return jsonify({"error": "Has d'especificar els paràmetres 'inici' i 'final' com a nombres."}), 400

@app.route("/avistaments", methods=["POST"])
def add_avistament():
    data = request.json
    cursor.execute("""
        INSERT INTO Avistaments (
            IDVideo, IDEspecie, fecha_aparicion, fecha_desaparicion,
            inicio_video_segons, final_video_segons, es_audio, confianza
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """, (
        data["IDVideo"],
        data["IDEspecie"],
        data["fecha_aparicion"],
        data.get("fecha_desaparicion"),
        data.get("inicio_video_segons"),
        data.get("final_video_segons"),
        data.get("es_audio", False),
        data.get("confianza")
    ))
    conn.commit()
    
    # 🔁 Obtenir l'ID generat automàticament
    id_avistament = cursor.lastrowid

    return jsonify({"message": "Avistament creat", "ID": cursor.lastrowid}), 201

@app.route("/avistaments/<int:id>", methods=["PUT"])
def update_avistament(id):
    print(f"🔁 PUT rebut per actualitzar ID {id}")
    data = request.json
    cursor.execute("""
        UPDATE Avistaments SET 
            fecha_desaparicion = %s,
            final_video_segons = %s
        WHERE ID = %s
    """, (data["fecha_desaparicion"], data["final_video_segons"], id))
    conn.commit()
    return jsonify({"message": "Avistament actualitzat"})


@app.route("/avistaments/<int:id>", methods=["DELETE"])
def delete_avistament(id):
    cursor.execute("DELETE FROM Avistaments WHERE ID=%s", (id,))
    conn.commit()
    return jsonify({"message": "Avistament eliminat"})

#-------------------------- CARPETES ----------------------
UPLOAD_FOLDER_DIRECTE = "uploads/directes"
UPLOAD_FOLDER_VIDEO = "uploads/videos"

os.makedirs(UPLOAD_FOLDER_DIRECTE, exist_ok=True)
os.makedirs(UPLOAD_FOLDER_VIDEO, exist_ok=True)

@app.route("/upload_video", methods=["POST"])
def upload_video():
    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    tipus = request.form.get("tipus", "normal")

    # decideix carpeta
    if tipus == "directe":
        folder = UPLOAD_FOLDER_DIRECTE +"/"+request.form.get("IDCamara", 0)
    else:
        folder = UPLOAD_FOLDER_VIDEO+"/"+request.form.get("IDUsuario", 0)

    os.makedirs(folder, exist_ok=True)
    
    filepath = os.path.join(folder, file.filename)
    file.save(filepath)

    # opcional: només guarda a BD si és un .mp4 final, no cada .ts
    if filepath.endswith(".mp4") and tipus != "directe":
        cursor.execute("""
            INSERT INTO Video (IDUsuario, IDCamara, Nombre, Dia, ruta_video)
            VALUES (%s, %s, %s, %s, %s)
        """, (
            request.form.get("IDUsuario", 0),
            request.form.get("IDCamara", 0),
            file.filename,
            datetime.now().date().isoformat(),
            filepath
        ))
        conn.commit()

    return jsonify({"message": "Fitxer pujat correctament", "ruta": filepath}), 201

# ------------------- ENDPOINT RESET DIRECTE -------------------
@app.route("/reset_directe/<int:id_camara>", methods=["POST"])
def reset_directe(id_camara):
    folder = os.path.join(UPLOAD_FOLDER_DIRECTE, str(id_camara))
    try:
        if os.path.exists(folder):
            shutil.rmtree(folder)
        os.makedirs(folder, exist_ok=True)
        return jsonify({"message": f"♻️ Directe reiniciat per càmera {id_camara}"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

#-------------------------- INICI DE L'APLICACIÓ ----------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
