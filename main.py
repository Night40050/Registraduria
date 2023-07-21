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

#implementacionn de  conntroladores
from Controladores.ControladorPartido   import ControladorPartido
from Controladores.ControladorCandidato import ControladorCandidato
from Controladores.ControladorMesa      import ControladorMesa
from Controladores.ControladorResultado import ControladorResultado
miControladorPartido=   ControladorPartido()
miControladorCandidato= ControladorCandidato()
miControladorMesa=      ControladorMesa()
miControladorResultado= ControladorResultado()

#se declaran los servicios de prueba con la ruta a la que el servidor contestara para la ruta especifica
@app.route("/",methods=['GET'])
def test():
    json = {}
    json["message"]="Server running ..."
    return jsonify(json)

"""Rutas para partido"""
@app.route("/partido",methods=['GET'])
def getPartido1():
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
def eliminarPartido(id):
    json=miControladorPartido.delete(id)
    return jsonify(json)

"""Rutas para candidato"""
@app.route("/candidato",methods=['GET'])
def getCandidato1():
    json=miControladorCandidato.index()
    return jsonify(json)
@app.route("/candidato",methods=['POST'])
def crearCandidato():
    data = request.get_json()
    json=miControladorCandidato.create(data)
    return jsonify(json)
@app.route("/candidato/<string:id>",methods=['GET'])
def getCandidato(id):
    json=miControladorCandidato.show(id)
    return jsonify(json)
@app.route("/candidato/<string:id>",methods=['PUT'])
def modificarCandidato(id):
    data = request.get_json()
    json=miControladorCandidato.update(id,data)
    return jsonify(json)
@app.route("/candidato/<string:id>",methods=['DELETE'])
def eliminarCandidato(id):
    json=miControladorCandidato.delete(id)
    return jsonify(json)
"""ruta para asociar candidato a partido"""
@app.route("/candidatos/<string:id>/partido/<string:id_partido>",methods=['PUT'])
def asignarPartidoACandidato(id,id_partido):
    json= miControladorCandidato.asignarPartido(id,id_partido)
    return jsonify(json)

""" Rutas para mesa"""
@app.route("/mesa",methods=['GET'])
def getMesa1():
    json=miControladorMesa.index()
    return jsonify(json)
@app.route("/mesa",methods=['POST'])
def crearMesa():
    data = request.get_json()
    json=miControladorMesa.create(data)
    return jsonify(json)
@app.route("/mesa/<string:id>",methods=['GET'])
def getMesa(id):
    json=miControladorMesa.show(id)
    return jsonify(json)
@app.route("/mesa/<string:id>",methods=['PUT'])
def modificarMesa(id):
    data = request.get_json()
    json=miControladorMesa.update(id,data)
    return jsonify(json)
@app.route("/mesa/<string:id>",methods=['DELETE'])
def eliminarMesa(id):
    json=miControladorMesa.delete(id)
    return jsonify(json)

"""Rutas para resultado"""
@app.route("/resultado",methods=['GET'])
def getResultado1():
    json=miControladorResultado.index()
    return jsonify(json)

@app.route("/resultado/<string:id>",methods=['GET'])
def getResultado(id):
    json=miControladorResultado.show(id)
    return jsonify(json)

@app.route("/resultado/mesa/<string:id_mesa>/candidato/<string:id_candidato>",methods=['POST'])
def crearResultado(id_mesa, id_candidato):
    data = request.get_json()
    json=miControladorResultado.create(data, id_mesa, id_candidato)
    return jsonify(json)

@app.route("/resultado/<string:id_resultado>/mesa/<string:id_mesa>/candidato/<string:id_candidato>",methods=['PUT'])
def modificarResultado(id_resultado, id_mesa, id_candidato):
    data = request.get_json()
    json=miControladorResultado.update(id_resultado, data, id_mesa, id_candidato)
    return jsonify(json)
@app.route("/resultado/<string:id>",methods=['DELETE'])
def eliminarResultado(id):
    json=miControladorResultado.delete(id)
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
    serve(app, host=dataConfig["url-backend"], port=dataConfig["port"])
