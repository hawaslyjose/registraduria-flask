"""
Importación de las clases RespositorioPartidos y Modelo de Partidos
"""
from Modelos.Partidos import Partidos
from Repositorios.RepositorioPartidos import RepositorioPartidos

"""
Clase controladora que administra los métodos del modelo a la base de datos
"""
class ControladorPartidos():
    def __init__(self):
        self.repositorioPartidos = RepositorioPartidos()

        """
    Método para hacer un GETALL
    @return método para encontrar todos los Partidos
    """
    def index(self):
        return self.repositorioPartidos.findAll()

    """
    Método que hace un POST 
    @param infoPartidos: información del Prtido
    @return método para guardar el nuevo Partido
    """
    def create(self,infoPartidos):
        nuevoPartido=Partidos(infoPartidos)
        return self.repositorioPartidos.save(nuevoPartido)

    """
    Método que hace un GETBYID 
    @param id: id del Partido impuesto por defecto en mongo
    @return método para encontrar un Partido por su Id
    """
    def show(self,id):
        elPartido=Partidos(self.repositorioPartidos.findById(id))
        return elPartido.__dict__

    """
    Método que hace un PUT
    @param infoPartidos: información del Partido
    @param id: id de las Mesasimpuesto por defecto en mongo
    @return método para guardar una Mesa en el mismo lugar que la encontró
    """
    def update(self,id,infoPartidos):
        partidoActual=Partidos(self.repositorioPartidos.findById(id))
        partidoActual.nombre=infoPartidos["nombre"]
        partidoActual.lema= infoPartidos["lema"]
        return self.repositorioPartidos.save(partidoActual)

    """
    Método que hace un DELETE
    @param id: id del Partido impuesto por defecto en mongo
    @return método que elimina al Partido mediante su id
    """
    def delete(self,id):
        return self.repositorioPartidos.delete(id)