"""
Importación de módulos / dependencias para ejecutar la aplicación y evitar fallos de seguridad y formateo de datos
"""
from flask import Flask
from flask import jsonify
from flask import request
from flask_cors import CORS
import json
from waitress import serve

app=Flask(__name__)
cors = CORS(app)
"""
Importación de controladores
"""
from Controladores.ControladorMesas import ControladorMesas
from Controladores.ControladorResultado import ControladorResultado
from Controladores.ControladorCandidatos import ControladorCandidatos
from Controladores.ControladorPartidos import ControladorPartidos
"""
Declaración del atributo miControladores de la clases de la carpeta Controladores
"""
miControladorMesas=ControladorMesas()
miControladorResultado=  ControladorResultado()
miControladorCandidato = ControladorCandidatos()
miControladorPartidos= ControladorPartidos()

###################################################################################
"""
Método de testeo con un GET que nos indica que la app está corriendo
"""
@app.route("/",methods=['GET'])
def test():
    json = {}
    json["message"]="Server running ..."
    return jsonify(json)
########################mesas###########################################################
"""
Método que obtiene toda la lista de mesas
@return json con la lista de objetos
"""
@app.route("/mesas",methods=['GET'])
def getEstudiantes():
    json=miControladorMesas.index()
    return jsonify(json)
@app.route("/mesas",methods=['POST'])
def crearEstudiante():
    data = request.get_json()
    json=miControladorMesas.create(data)
    return jsonify(json)
@app.route("/mesas/<string:id>",methods=['GET'])
def getEstudiante(id):
    json=miControladorMesas.show(id)
    return jsonify(json)
@app.route("/mesas/<string:id>",methods=['PUT'])
def modificarEstudiante(id):
    data = request.get_json()
    json=miControladorMesas.update(id,data)
    return jsonify(json)
@app.route("/mesas/<string:id>",methods=['DELETE'])
def eliminarEstudiante(id):
    json=miControladorMesas.delete(id)
    return jsonify(json)
############################partidos#######################################################
@app.route("/partidos",methods=['GET'])
def getPartidos():
    json=miControladorPartidos.index()
    print("get partido conseguido")
    return jsonify(json)
@app.route("/partidos/<string:id>",methods=['GET'])
def getPartidosid(id):
    json=miControladorPartidos.show(id)
    return jsonify(json)
@app.route("/partidos",methods=['POST'])
def crearPartidos():
    data = request.get_json()
    json=miControladorPartidos.create(data)
    return jsonify(json)
@app.route("/partidos/<string:id>",methods=['PUT'])
def modificarPartidos(id):
    data = request.get_json()
    json=miControladorPartidos.update(id,data)
    return jsonify(json)
@app.route("/partidos/<string:id>",methods=['DELETE'])
def eliminarPartidos(id):
    json=miControladorPartidos.delete(id)
    return jsonify(json)
################################candidatos###################################################
"""
Método que lanza una lista de los candidatos insertados
@return retorna un json
"""
@app.route("/candidatos",methods=['GET'])
def getMaterias():
    json=miControladorCandidato.index()
    print("Get conseguido")
    return jsonify(json)

"""
Método que lanza una lista de los candidatos insertados filtrados por ID
@params id: identificador por defecto proporcionado por MongoDB
@return retorna un json
"""
@app.route("/candidatos/<string:id>",methods=['GET'])
def getMateria(id):
    json=miControladorCandidato.show(id)
    print("Get by id conseguido")
    return jsonify(json)

"""
Método que permite insertar un candidato
"""
@app.route("/candidatos",methods=['POST'])
def crearMateria():
    data = request.get_json()
    json=miControladorCandidato.create(data)
    print("Post conseguido")
    return jsonify(json)

"""
Método que permite hacer una actualización del candidato seleccionado por id
@params id: identificador del candidato por defecto proporcionado por MongoDB
@return retorna un json
"""
@app.route("/candidatos/<string:id>",methods=['PUT'])
def modificarMateria(id):
    data = request.get_json()
    json=miControladorCandidato.update(id,data)
    print("Put conseguido")
    return jsonify(json)

"""
Método que elimina a un candidato mediante su id
@params id: identificador del candidato por defecto proporcionado por MongoDB
@return retorna un json
"""
@app.route("/candidatos/<string:id>",methods=['DELETE'])
def eliminarMateria(id):
    json=miControladorCandidato.delete(id)
    print("Delete conseguido")
    return jsonify(json)
"""
Método que relaciona a un candidato mediante su id con un partido
@params id: identificador del candidato por defecto proporcionado por MongoDB
@param id_partidos: id de los partidos impuestos por defectos en mongo
@return retorna un json
"""
@app.route("/candidatos/<string:id>/partidos/<string:id_partidos>",methods=['PUT'])
def asignarCandidatoAPartidos(id,id_partidos):
    json=miControladorCandidato.asignarPartido(id,id_partidos)
    print(json)
    return jsonify(json)

@app.route("/candidatos/partidos/<string:id_partidos>",methods=['GET'])
def candidatosenpartido(id_partidos):
    json=miControladorCandidato.listarCandidatosenPartidos(id_partidos)
    return jsonify(json)


##################################resultados#################################################
@app.route("/resultados",methods=['GET'])
def getResultados():
    json=miControladorResultado.index()
    return jsonify(json)

@app.route("/resultados/orden",methods=['GET'])
def getResultados2():
    json=miControladorResultado.indexAll()
    return jsonify(json)

@app.route("/resultados/<string:id>",methods=['GET'])
def getResultado(id):
    json=miControladorResultado.show(id)
    return jsonify(json)
@app.route("/resultados/candidatos/<string:cedula_candidato>/mesas/<string:numero_mesa>",methods=['POST'])
def crearResultado(numero_mesa,cedula_candidato):
    data = request.get_json()
    json=miControladorResultado.create(data,numero_mesa,cedula_candidato)
    return jsonify(json)

@app.route("/resultados/notas_mayores",methods=['GET'])
def getNotasMayores():
    json=miControladorResultado.notasMasAltasPorVotos()
    print(json)
    return jsonify(json)

@app.route("/resultados/notas_mayores2",methods=['GET'])
def getNotasMayores2():
    json=miControladorResultado.notasMasAltasPorVotos2()
    print(json)
    return jsonify(json)
'''@app.route("/Resultados/<string:id>/estudiante/<string:id_estudiante>/materia/<string:id_materia>",methods=['PUT'])
def modificarInscripcion(id_inscripcion,id_estudiante,id_materia):
    data = request.get_json()
    json=miControladorResultado.update(id,data,numero_mesa,cedula_candidato,numero_votos)
    return jsonify(json)
@app.route("/inscripciones/<string:id_inscripcion>",methods=['DELETE'])
def eliminarInscripcion(id_inscripcion):
    json=miControladorInscripcion.delete(id_inscripcion)
    return jsonify(json)'''
###################################################################################
def loadFileConfig():
    with open('config.json') as f:
        data = json.load(f)
    return data

if __name__=='__main__':
    dataConfig = loadFileConfig()
    print("Server running : "+"http://"+dataConfig["url-backend"]+":" + str(dataConfig["port"]))
    serve(app,host=dataConfig["url-backend"],port=dataConfig["port"])