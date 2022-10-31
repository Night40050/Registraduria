from flask import Flask
from flask import jsonify
from flask import request
from flask_cors import CORS
from flask_cors import cross_origin
import json
from waitress import serve

#instancia del servidor y CORS (para el intercambio de recursos cruzados)
app=Flask(__name__)
cors = CORS(app)

from Controladores.ControladorPartido import ControladorPartido
miControladorPartido=ControladorPartido()

#se declara los servicios de prueba con la ruta a la que el servidosr contestara para partido
@app.route("/partido",methods=['GET'])
def getPartido():
    json=miControladorPartido.index()
    return jsonify(json)
@app.route("/partido",methods=['POST'])
def crearPartido():
    data = request.get_json()
    json=miControladorPartido.create(data)
    return jsonify(json)
@app.route("/partido/<string:id>",methods=['GET'])
def getPartido(id):
    json=miControladorPartido.show(id)
    return jsonify(json)
@app.route("/partido/<string:id>",methods=['PUT'])
def modificarPartido(id):
    data = request.get_json()
    json=miControladorPartido.update(id,data)
    return jsonify(json)

@app.route("/partido/<string:id>",methods=['DELETE'])
def eliminarEstudiante(id):
    json=miControladorPartido.delete(id)
    return jsonify(json)

@app.route("/",methods=['GET'])
def test():
    json = {}
    json["message"]="Server running ..."
    return jsonify(json)

#metodo que lee el archivo de configuracion
def loadFileConfig():
    with open('config.json') as f:
        data = json.load(f)
    return data

#primeras lineas en ejecutarse cargando la configuracion e instancia del servidor
if __name__=='__main__':
    dataConfig = loadFileConfig()
    print("Server running : "+"http://"+dataConfig["url-backend"]+":" + str(dataConfig["port"]))
    serve(app,host=dataConfig["url-backend"],port=dataConfig["port"])