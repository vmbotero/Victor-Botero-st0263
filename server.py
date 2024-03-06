import sqlite3
from flask import Flask, request, jsonify

app = Flask(__name__)
DATABASE = 'p2p.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row 
    return conn

def init_db():
    with app.app_context():
        db = get_db_connection()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

@app.route('/', methods=['GET'])
def master():
    return jsonify({"message": "Hello World!"}), 200

@app.route('/login', methods=['POST'])
def login():
    username = request.json['username']
    password = request.json['password']
    conn = get_db_connection()
    peer = conn.execute('SELECT * FROM peers WHERE username = ?', (username,)).fetchone()
    if peer:
        if peer['password'] == password:
            return jsonify({"message": "Login éxitoso", "result": True}), 200
        else:
            return jsonify({"message": "Login fallido", "result": False}), 500 
    else:
        url = request.json['url']
        conn.execute('INSERT INTO peers (username, password, url) VALUES (?, ?, ?)', (username, password, url))
        conn.commit()
        return jsonify({"message": "Registro éxitoso", "result": True}), 200 

@app.route('/logout', methods=['POST'])
def logout():
    username = request.json['username']
    conn = get_db_connection()
    peer = conn.execute('SELECT * FROM peers WHERE username = ?', (username,)).fetchone()
    conn.close()
    message = ""
    result = False
    if peer:
        message = "Sesión cerrada con éxito"
        result = True
    else:
        message = "Peer inexistente"
    return jsonify({"message": message, "result": result}), 200

@app.route('/indexar', methods=['POST'])
def index():
    username = request.json['username']
    files = request.json['files']
    conn = get_db_connection()
    peer = conn.execute('SELECT * FROM peers WHERE username = ?', (username,)).fetchone()
    message = ""
    result = []
    if peer:
        for file in files:
            existing_file = conn.execute('SELECT * FROM files WHERE filename = ? AND peer = ?', (file, username)).fetchone()
            if not existing_file:
                conn.execute('INSERT INTO files (filename, peer) VALUES (?, ?)', (file, username))
                conn.commit()
                result.append(file)
        message = "Archivos añadidos con éxito"
    else:
        message = "Peer inexistente"
    conn.close()
    return jsonify({"message": message, "files": result}), 200

@app.route('/buscar', methods=['POST'])
def search():
    files = request.json['files']
    conn = get_db_connection()
    result = []
    message = ""
    if len(files) > 0:
        for file in files:
            file_configuracion = conn.execute('SELECT * FROM files WHERE filename = ?', (file,)).fetchall()
            for record in file_configuracion:
                result.append({
                    "filename": record['filename'],
                    "peer": record['peer'],
                })
        message = "Archivos encontrados con éxito"
    else:
        message = "Archivos no encontrados"
    conn.close()
    return jsonify({"message": message, "files": result}), 200


def getPeerInfo(username):
    conn = get_db_connection()
    peer_info = conn.execute('SELECT * FROM peers WHERE username = ?', (username,)).fetchone()
    conn.close()
    return peer_info

def saveFiles(peer, files):
    conn = get_db_connection()
    added = []
    for file in files:
        prev_file = conn.execute('SELECT * FROM files WHERE filename = ? AND peer = ?', (file, peer['username'])).fetchone()
        if not prev_file:
            conn.execute('INSERT INTO files (filename, peer, url) VALUES (?, ?, ?)', (file, peer['username'], peer['url']))
            conn.commit()
            added.append(file)
    conn.close()
    return added

def searchFiles(files):
    conn = get_db_connection()
    result = []
    for file in files:
        file_configuracion = conn.execute('SELECT * FROM files WHERE filename = ?', (file,)).fetchall()
        for record in file_configuracion:
            result.append({
                "filename": record['filename'],
                "peer": record['peer'],
                "url": record['url']
            })
    conn.close()
    return result

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
