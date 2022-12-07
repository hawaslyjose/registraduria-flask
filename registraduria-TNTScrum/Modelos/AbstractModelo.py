"""
Importación de módulo para definir una clase abstracta
"""
from abc import ABCMeta

"""
Clase para declarar la clase abstracta
"""
class AbstractModelo(metaclass=ABCMeta):
    """
    Método para inicializar la clase abstracta mediante llave-valor
    """
    def __init__(self,data):
        for llave, valor in data.items():
            setattr(self, llave, valor)
