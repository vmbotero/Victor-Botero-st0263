from flask import Flask, request, jsonify
import requests
import json
import grpc
import configuracion_pb2
import configuracion_pb2_grpc
import sqlite3

app = Flask(__name__)
DATABASE = 'p2p.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/login', methods=['POST'])
def login():
    username = request.json['username']
    password = request.json['password']
    conn = get_db_connection()
    peer = conn.execute('SELECT * FROM peers WHERE username = ?', (username,)).fetchone()
    conn.close()
    if peer and peer['password'] == password:
        body = {
            "username": username,
            "password": password,
            "url": request.json.get('url', '')
        }
        result = executeLogin(body)
        message = "Login éxitoso"
    else:
        message = "Login fallido"
    return jsonify({"message": message}), 200

@app.route('/logout', methods=['POST'])
def logout():
    username = request.json['username']
    body = {
       "username": username,
    }
    result = executeLogout(body)
    return jsonify({"message": result['message']}), 200

@app.route('/indexar', methods=['POST'])
def index():
    username = request.json['username']
    files = request.json['files']
    stub = []
    body = {
       "username": username,
       "files": files
    }
    result = executeIndex(body)
    if result:
        for f in result['files']:
            stub.append(grpc_client_upload(f))
    return jsonify({"message": result['message'], "files": result['files'], "operation": stub}), 200

@app.route('/buscar', methods=['POST'])
def search():
    files = request.json['files']
    body = {
        "files": files
    }
    stub = []
    result = executeSearch(body)
    if result:
        for f in result['files']:
            stub.append(grpc_client_download(f['filename']))
    return jsonify({"message": result['message'], "files": result['files'], "operation": stub}), 200

def grpc_client_upload(filename):
    with grpc.insecure_channel('localhost:3000') as channel:
        stub = configuracion_pb2_grpc.FileServiceStub(channel)
        try:
            request = configuracion_pb2.UploadRequest(filename=filename)
            response = stub.Upload(request)
            return response.message
        except grpc.RpcError as e:
            return f"Error during upload: {e.code()} - {e.details()}"
        finally:
            channel.close()

def grpc_client_download(filename):
    with grpc.insecure_channel('localhost:3000') as channel:
        stub = configuracion_pb2_grpc.FileServiceStub(channel)
        try:
            request = configuracion_pb2.DownloadRequest(filename=filename)
            response = stub.Download(request)
            return response.file.content
        except grpc.RpcError as e:
            return f"Error during download: {e.code()} - {e.details()}"
        finally:
            channel.close()
    
def executeLogin(body):
    headers = {'Content-Type': 'application/json'}
    response = requests.post('http://127.0.0.1:5000/login', data=json.dumps(body), headers=headers)
    return response.json()

def executeLogout(body):
    headers = {'Content-Type': 'application/json'}
    response = requests.post('http://127.0.0.1:5000/logout', data=json.dumps(body), headers=headers)
    return response.json()

def executeIndex(body):
    headers = {'Content-Type': 'application/json'}
    response = requests.post('http://127.0.0.1:5000/indexar', data=json.dumps(body), headers=headers)
    return response.json()

def executeSearch(body):
    headers = {'Content-Type': 'application/json'}
    response = requests.post('http://127.0.0.1:5000/buscar', data=json.dumps(body), headers=headers)
    return response.json()

if __name__ == '__main__':
    app.run(debug=True, port=5001)
