"""
Importación de las clases InterfaceRepositorio Y Modelo Partidos
"""
from Repositorios.InterfaceRepositorio import InterfaceRepositorio
from Modelos.Partidos import Partidos

"""
Clase repositorio que hereda de la interfaz que lleva a cabo la asignación de la colección y resultados de los JSON
"""
class RepositorioPartidos(InterfaceRepositorio[Partidos]):
    pass