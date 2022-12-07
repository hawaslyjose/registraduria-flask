"""
Importación de las clases InterfaceRepositorio Y Modelo Mesas
"""
from Repositorios.InterfaceRepositorio import InterfaceRepositorio
from Modelos.Mesas import Mesas

"""
Clase repositorio que hereda de la interfaz que lleva a cabo la asignación de la colección y resultados de los JSON
"""
class RepositorioMesas(InterfaceRepositorio[Mesas]):
    pass

