"""
Importación de módulos / dependencias para la conexión y peticiones a mongo database
"""
import pymongo
import certifi
from bson import DBRef
from bson.objectid import ObjectId
from typing import TypeVar, Generic, List, get_origin, get_args
import json

"""
Declaración de variable para establecer un parámetro genérico
"""
T = TypeVar('T')

"""Clase interface encargada de darle nombre a la base de datos, a la colección y ejecutar los querys"""
class InterfaceRepositorio(Generic[T]):
    """
    Método que inicializa la url de la base de datos, el nombre de la base de datos y la colección 
    """
    def __init__(self):
        ca = certifi.where()
        dataConfig = self.loadFileConfig()
        client = pymongo.MongoClient(dataConfig["data-db-connection"], tlsCAFile=ca)
        self.baseDatos = client[dataConfig["name-db"]]
        theClass = get_args(self.__orig_bases__[0])
        self.coleccion = theClass[0].__name__.lower()
    
    """
    Método que carga las configuraciones de la base de datos, como la url y la contraseña
    @return data: la data que contiene la configuración
    """
    def loadFileConfig(self):
        with open('config.json') as f:
            data = json.load(f)
        return data
    
    """
    Método que se encarga de guardar en la base de datos (insertar)
    @param item: variable de tipo genérico
    @return búsqueda por Id que saque de la inserción
    """
    def save(self, item: T):
        laColeccion = self.baseDatos[self.coleccion]
        elId = ""
        item = self.transformRefs(item)
        if hasattr(item, "_id") and item._id != "":
            elId = item._id
            _id = ObjectId(elId)
            laColeccion = self.baseDatos[self.coleccion]
            delattr(item, "_id")
            item = item.__dict__
            updateItem = {"$set": item}
            x = laColeccion.update_one({"_id": _id}, updateItem)
        else:
            _id = laColeccion.insert_one(item.__dict__)
            elId = _id.inserted_id.__str__()

        x = laColeccion.find_one({"_id": ObjectId(elId)})
        x["_id"] = x["_id"].__str__()
        return self.findById(elId)
    
    """
    Método que borra un objeto
    @param id: mediante el id borramos todo el objeto
    @return mensaje de que se borró
    """
    def delete(self, id):
        laColeccion = self.baseDatos[self.coleccion]
        cuenta = laColeccion.delete_one({"_id": ObjectId(id)}).deleted_count
        return {"deleted_count": cuenta}
    
    """
    Método que actualiza el objeto dado
    @param id: para poner en la url al actualizar
    @param item: variable de tipo genérica
    @return mensaje de que acutalizó
    """
    def update(self, id, item: T):
        _id = ObjectId(id)
        laColeccion = self.baseDatos[self.coleccion]
        delattr(item, "_id")
        item = item.__dict__
        updateItem = {"$set": item}
        x = laColeccion.update_one({"_id": _id}, updateItem)
        return {"updated_count": x.matched_count}
    
    """
    Método que busca por id al objeto
    @param id: identificador a buscar
    @return el objeto
    """
    def findById(self, id):
        laColeccion = self.baseDatos[self.coleccion]
        x = laColeccion.find_one({"_id": ObjectId(id)})
        x = self.getValuesDBRef(x)
        if x == None:
            x = {}
        else:
            x["_id"] = x["_id"].__str__()
        return x
    
    def findByIdResultado(self):
        laColeccion = self.baseDatos[self.coleccion]
        data = []
        for x in laColeccion.find().sort("numero_votos", pymongo.DESCENDING):
            x["_id"] = x["_id"].__str__()
            x = self.transformObjectIds(x)
            x = self.getValuesDBRef(x)
            data.append(x)
        return data
    
    
    """
    Método que encuentra toda la lista insertada de la colección
    @return lista de objetos
    """
    def findAll(self):
        laColeccion = self.baseDatos[self.coleccion]
        data = []
        for x in laColeccion.find():
            x["_id"] = x["_id"].__str__()
            x = self.transformObjectIds(x)
            x = self.getValuesDBRef(x)
            data.append(x)
        return data
    
    """
    Método que lleva a cabo el query
    @param theQuery: el query a hacer
    @return el query hecho
    """
    def query(self, theQuery):
        laColeccion = self.baseDatos[self.coleccion]
        data = []
        for x in laColeccion.find(theQuery):
            x["_id"] = x["_id"].__str__()
            x = self.transformObjectIds(x)
            x = self.getValuesDBRef(x)
            data.append(x)
        return data
    
    def queryAggregation(self, theQuery):
        laColeccion = self.baseDatos[self.coleccion]
        data = []
        for x in laColeccion.aggregate(theQuery):
            x["_id"] = x["_id"].__str__()
            x = self.transformObjectIds(x)
            x = self.getValuesDBRef(x)
            data.append(x)
        return data
    
    """
    Método que obtiene los valores de la base de datos
    @return x valor obtenido
    """
    def getValuesDBRef(self, x):
        keys = x.keys()
        for k in keys:
            if isinstance(x[k], DBRef):

                laColeccion = self.baseDatos[x[k].collection]
                valor = laColeccion.find_one({"_id": ObjectId(x[k].id)})
                valor["_id"] = valor["_id"].__str__()
                x[k] = valor
                x[k] = self.getValuesDBRef(x[k])
            elif isinstance(x[k], list) and len(x[k]) > 0:
                x[k] = self.getValuesDBRefFromList(x[k])
            elif isinstance(x[k], dict) :
                x[k] = self.getValuesDBRef(x[k])
        return x
    
    """
    Método que obtiene los valores de la lista
    @param theList: la lista
    @return una nueva lista
    """
    def getValuesDBRefFromList(self, theList):
        newList = []
        laColeccion = self.baseDatos[theList[0]._id.collection]
        for item in theList:
            value = laColeccion.find_one({"_id": ObjectId(item.id)})
            value["_id"] = value["_id"].__str__()
            newList.append(value)
        return newList
    
    """
    Método que transforma los id de un objeto
    @return x: el id transformado
    """
    def transformObjectIds(self, x):
        for attribute in x.keys():
            if isinstance(x[attribute], ObjectId):
                x[attribute] = x[attribute].__str__()
            elif isinstance(x[attribute], list):
                x[attribute] = self.formatList(x[attribute])
            elif  isinstance(x[attribute], dict):
                x[attribute]=self.transformObjectIds(x[attribute])
        return x
    
    """
    Método que formatea la lista
    @return una nueva lista
    """
    def formatList(self, x):
        newList = []
        for item in x:
            if isinstance(item, ObjectId):
                newList.append(item.__str__())
        if len(newList) == 0:
            newList = x
        return newList
    
    """
    Método que transformaRefs
    @param item
    @return item
    """
    def transformRefs(self, item):
        theDict = item.__dict__
        keys = list(theDict.keys())
        for k in keys:
            if theDict[k].__str__().count("object") == 1:
                newObject = self.ObjectToDBRef(getattr(item, k))
                setattr(item, k, newObject)
        return item

    def ObjectToDBRef(self, item: T):
        nameCollection = item.__class__.__name__.lower()
        return DBRef(nameCollection, ObjectId(item._id))
