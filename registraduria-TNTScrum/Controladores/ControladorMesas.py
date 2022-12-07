"""
Importación de las clases RespositorioMesas y Modelo de Mesas
"""
from Repositorios.RepositorioMesas import RepositorioMesas
from Modelos.Mesas import Mesas

"""
Clase controladora que administra los métodos del modelo a la base de datos
"""
class ControladorMesas():
    def __init__(self):
        self.repositorioMesas = RepositorioMesas()

        """
    Método para hacer un GETALL
    @return método para encontrar todos las Mesas
    """
    def index(self):
        return self.repositorioMesas.findAll()

    """
    Método que hace un POST 
    @param infoMesas: información de las Mesas
    @return método para guardar la nueva Mesa
    """
    def create(self,infoMesas):
        nuevoMesas=Mesas(infoMesas)
        return self.repositorioMesas.save(nuevoMesas)

    """
    Método que hace un GETBYID 
    @param id: id de las Mesas impuesto por defecto en mongo
    @return método para encontrar la Mesa por su Id
    """
    def show(self,id):
        elMesas=Mesas(self.repositorioMesas.findById(id))
        return elMesas.__dict__

    """
    Método que hace un PUT
    @param infoMesas: información de las Mesas
    @param id: id de las Mesas impuesto por defecto en mongo
    @return método para guardar una Mesa en el mismo lugar que la encontró
    """
    def update(self,id,infoMesas):
        MesasActual=Mesas(self.repositorioMesas.findById(id))
        MesasActual.numero_mesa=infoMesas["numero_mesa"]
        MesasActual.cantidad_inscritos = infoMesas["cantidad_inscritos"]
        
        return self.repositorioMesas.save(MesasActual)

    """
    Método que hace un DELETE
    @param id: id de la Mesa impuesto por defecto en mongo
    @return método que elimina la Mesa mediante su id
    """
    def delete(self,id):
        return self.repositorioMesas.delete(id)