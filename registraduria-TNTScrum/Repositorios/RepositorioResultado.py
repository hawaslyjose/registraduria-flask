"""
Importación de las clases InterfaceRepositorio Y Modelo Resultados
"""
from Repositorios.InterfaceRepositorio import InterfaceRepositorio
from Modelos.Resultado import Resultado
from bson import ObjectId
"""
Clase repositorio que hereda de la interfaz que lleva a cabo la asignación de la colección y resultados de los JSON
"""


class RepositorioResultado(InterfaceRepositorio[Resultado]):
    def getMayorNotaPorVotos(self):
        query1 = {
            "$group":
            {
                "_id": "$resultado",
                "max": {
                    "$max": "$numero_votos"
                },
                "doc": {
                    "$first": "$$ROOT"
                }
            }
        }
        pipeline = [query1]
        return self.queryAggregation(pipeline)

    def getMayorNotaPorVotos2(self):
        query1 = {
            
                '$match': {
                    'mesa.$id': ObjectId('63576728e2cd02fa1951a27d')
                }
        }
        query2={
                '$sort': {
                    'numero_votos': -1
                }
            
        }
        pipeline = [query1,query2]
        return self.queryAggregation(pipeline)

    def getVotosPorCandidato(self):
        query1 = {
            '$match': {
                'candidato.$id': ObjectId('63576789e2cd02fa1951a27e')
        }
    }
        query2 = {
            '$sort': {
                'numero_votos': -1
            }
    }
        pipeline = [query1,query2]
        return self.queryAggregation(pipeline)

    


        