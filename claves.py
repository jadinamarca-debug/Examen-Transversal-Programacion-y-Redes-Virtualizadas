import sqlite3
import hashlib
from flask import Flask, request, jsonify

app = Flask(__name__)

# 1. Función para inicializar la base de datos (SQLite)
def init_db():
    conn = sqlite3.connect('usuarios.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# 2. Función auxiliar para convertir contraseñas a Hash SHA-256
def generar_hash(password):
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

# 3. Ruta Raíz (Sitio web)
@app.route('/')
def index():
    return "Servidor de Gestión de Claves Operativo - Puerto 7500"

# 4. Ruta para verificar las credenciales mediante JSON
@app.route('/login', methods=['POST'])
def login():
    datos = request.get_json()
    if not datos:
        return jsonify({"status": "Error", "mensaje": "Faltan parámetros"}), 400
        
    usuario = datos.get('nombre')
    password_plana = datos.get('password')

    hash_ingresado = generar_hash(password_plana)

    conn = sqlite3.connect('usuarios.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM usuarios WHERE nombre = ? AND password_hash = ?', (usuario, hash_ingresado))
    resultado = cursor.fetchone()
    conn.close()

    if resultado:
        return jsonify({"status": "Éxito", "mensaje": f"Bienvenido {usuario}, acceso concedido"}), 200
    else:
        return jsonify({"status": "Error", "mensaje": "Credenciales inválidas"}), 401

# 5. Insertar a los integrantes del grupo automáticamente
def insertar_integrantes():
    integrantes = [
        ('Javier', generar_hash('claveSegura123')),
        ('Damian', generar_hash('redes456')),
	('Bastian', generar_hash('network789'))
    ]
    conn = sqlite3.connect('usuarios.db')
    cursor = conn.cursor()
    for nombre, text_hash in integrantes:
        try:
            cursor.execute('INSERT INTO usuarios (nombre, password_hash) VALUES (?, ?)', (nombre, text_hash))
        except sqlite3.IntegrityError:
            pass # Ignorar si ya existen
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    insertar_integrantes()
    # Ejecución en puerto 7500 y threaded=False para estabilidad de la VM DEVASC
    app.run(host="0.0.0.0", port=7500, threaded=False)
