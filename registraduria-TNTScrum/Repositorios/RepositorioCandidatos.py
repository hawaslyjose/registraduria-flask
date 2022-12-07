"""
Importación de las clases InterfaceRepositorio Y Modelo Candidatos
"""
from Repositorios.InterfaceRepositorio import InterfaceRepositorio
from Modelos.Candidatos import Candidatos
from bson import ObjectId
"""
Clase repositorio que hereda de la interfaz que lleva a cabo la asignación de la colección y resultados de los JSON
"""
class RepositorioCandidatos(InterfaceRepositorio[Candidatos]):
    def getListadoCandidatoEnPartido(self, id_partidos):
        theQuery = {"partido.$id": ObjectId(id_partidos)}
        return self.query(theQuery)

    def Partidosporcandidato(self):
        query1 = {
            '$match': {
                'partido.$id': ObjectId('63573d7d5ddb9880f8b61d4a')
        }
    }
        query2 = {
            '$sort': {
                'cedula': 1
        }
    }
        pipeline = [query1,query2]
        return self.queryAggregation(pipeline)
