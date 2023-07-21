import pymongo
import certifi
from bson import DBRef
from bson.objectid import ObjectId
from typing import TypeVar, Generic, List, get_origin, get_args
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import json

T = TypeVar('T')

class InterfaceRepositorio(Generic[T]):

#metodo connstructor para configurar la conexion a MongoDB
    def __init__(self):
        ca = certifi.where()
        dataConfig = self.loadFileConfig()
        uri = dataConfig["data-db-connection"]
        client = MongoClient(uri, server_api=ServerApi('1'))
        self.baseDatos = client[dataConfig["name-db"]]
        theClass = get_args(self.__orig_bases__[0])
        self.coleccion = theClass[0].__name__.lower()

# abre el archivo config.json para cargar su contenido usando la biblioteca de json y devuelve la configuracion como objeto de py
    def loadFileConfig(self):
        with open('config.json') as f:
            data = json.load(f)
        return data

#se encarga de guardar un objeto 'item' en la coleccion especificada o actualizar
    def save(self, item: T):
        laColeccion = self.baseDatos[self.coleccion]            #accede a la coleccion en la bd
        elId = ""
        item = self.transformRefs(item)                         #transforma las referencias del objeto item
        if hasattr(item, "_id") and item._id != "":             #validar si el objeto tiene un atributo '_id' y verifica si el atributo esta vacio
            elId = item._id                                     #se asigna el valor del atributo _id
            _id = ObjectId(elId)                                #crea un objeto a partir de 'elId'
            laColeccion = self.baseDatos[self.coleccion]       #se actualiza asegurando que apunta a la coleccion correcta en la bd
            delattr(item, "_id")                                #eliminna el atributo _id del objeto item
            item = item.__dict__                                #convierte el objeto item en un diccionario
            updateItem = {"$set": item}                         #diccionario que contiene la operación de actualización ($set) junto con el diccionario item para ser actualizado en la colección.
            x = laColeccion.update_one({"_id": _id}, updateItem)#actualiza el documento en la coleccion con el _id prporcionado
        else:
            _id = laColeccion.insert_one(item.__dict__)         #inserta el diccionnario en la coleccion y devuelve el objeto _id generado para el documento insertado
            elId = _id.inserted_id.__str__()                    #se asigna con la representación en cadena del _id insertado

        x = laColeccion.find_one({"_id": ObjectId(elId)})       #busca el documento de la coleccion con el _id proporcionnado
        x["_id"] = x["_id"].__str__()                           #convierte el _id en un string
        return self.findById(elId)                              #busca el documento por su _id

#elimina de la coleccion toda la info que coincida con id devuelve un diccionnario conn el contador de eliminacion
    def delete(self, id):
        laColeccion = self.baseDatos[self.coleccion]
        cuenta = laColeccion.delete_one({"_id": ObjectId(id)}).deleted_count
        return {"deleted_count": cuenta}

#actualiza el documento en la coleccion segun el id devolviendo un diccionario co la cantidad de elementos actualizados
    def update(self, id, item: T):
        _id = ObjectId(id)
        laColeccion = self.baseDatos[self.coleccion]
        delattr(item, "_id")
        item = item.__dict__
        updateItem = {"$set": item}
        x = laColeccion.update_one({"_id": _id}, updateItem)
        return {"updated_count": x.matched_count}

#busca y devuelve un documento de la coleccion segun su id
    def findById(self, id):
        laColeccion = self.baseDatos[self.coleccion]
        x = laColeccion.find_one({"_id": ObjectId(id)})
        x = self.getValuesDBRef(x)
        if x == None:
            x = {}
        else:
            x["_id"] = x["_id"].__str__()
        return x

#busca y devuelve todos los documentos de la coleccion
    def findAll(self):
        laColeccion = self.baseDatos[self.coleccion]
        data = []
        for x in laColeccion.find():
            x["_id"] = x["_id"].__str__()
            x = self.transformObjectIds(x)
            x = self.getValuesDBRef(x)
            data.append(x)
        return data

#realiza una consulta especifica con la sintaxis de monngoDB en la coleccion y devuelve los documenntos que coinnciden con la connsulta
    def query(self, theQuery):
        laColeccion = self.baseDatos[self.coleccion]
        data = []
        for x in laColeccion.find(theQuery):
            x["_id"] = x["_id"].__str__()
            x = self.transformObjectIds(x)
            x = self.getValuesDBRef(x)
            data.append(x)
        return data

#realiza una agregacion en la coleccion utilizando una cosulta especifica y devuelve los resultados de agregacion
    def queryAggregation(self, theQuery):
        laColeccion = self.baseDatos[self.coleccion]
        data = []
        for x in laColeccion.aggregate(theQuery):
            x["_id"] = x["_id"].__str__()
            x = self.transformObjectIds(x)
            x = self.getValuesDBRef(x)
            data.append(x)
        return data

#procesamiento recursivo de los valores del diccionnario para obtenner los valores referenciados por el metodo y remplazarlos en el diccionario
#consulta la info de las referencias que posee un objeto consultado
    def getValuesDBRef(self, x):
        keys = x.keys()                                                 #se obtienen todas las claves del diccionario y se almacena en la lista key
        for k in keys:
            if isinstance(x[k], DBRef):                                 #si el valor correspondiente a la clave 'k' es una instancia de 'DBRef'
                laColeccion = self.baseDatos[x[k].collection]           #obtiene la coleccion referennciada por la instacia de 'DBRef'
                valor = laColeccion.find_one({"_id": ObjectId(x[k].id)})#consulta en la coleccionn referenciada para obtener el documento con '_id'
                valor["_id"] = valor["_id"].__str__()
                x[k] = valor                                            #el valor en x[k] se remplaza por el documento obtenido en la consulta
# se realiza una llamada recursiva al mismo metodo para procesar los valores internos del documento obtenido para manejar referencias anidadas en documentos referenciados
                x[k] = self.getValuesDBRef(x[k])
# Si el valor correspondiente a la clave k es una lista no vacía, se verifica si contiene elementos que podrían ser instancias de DBRef.
            elif isinstance(x[k], list) and len(x[k]) > 0:
                x[k] = self.getValuesDBRefFromList(x[k])                #procesa los elementos de la lista y maneja referencias a documentos
#Si el valor correspondiente a la clave k es un diccionario, se realiza una llamada recursiva a getValuesDBRef para procesar los valores internos del diccionario.
            elif isinstance(x[k], dict) :
                x[k] = self.getValuesDBRef(x[k])
        return x                                                        #se devuelve el diccionario x procesado y actualizado con los valores referenciados por DBRef

#procesa los elementos de la lista para obtener los valores referenciados por DBRef devolviendo una lista con los valores remplazados
    def getValuesDBRefFromList(self, theList):
        newList = []
        laColeccion = self.baseDatos[theList[0]._id.collection]     #se obtiene la coleccion referenciada por el primer elemento de la lista que se recibe
        for item in theList:
            value = laColeccion.find_one({"_id": ObjectId(item.id)})#consulta en la coleccion para obtener el documento con cierto'_id'
            value["_id"] = value["_id"].__str__()
            newList.append(value)                                   # El documento obtenido de la consulta se agrega a la nueva lista newList.
        return newList

#transforma los valores de tipo ObjectId en un diccionario 'x' en su representacion de cadena
    def transformObjectIds(self, x):
        for attribute in x.keys():                                #Se itera sobre las claves (atributos) del diccionario x
            if isinstance(x[attribute], ObjectId):                #si el valor correspondiente al atributo es de tipo ObjectId
                x[attribute] = x[attribute].__str__()             #Se asigna el valor del atributo convirtiéndolo a su representación de cadena
            elif isinstance(x[attribute], list):                  #Si el valor del atributo es de tipo lista
                x[attribute] = self.formatList(x[attribute])      #Se llama al método formatList para formatear y transformar los valores de la lista
            elif isinstance(x[attribute], dict):                  #Si el valor del atributo es de tipo diccionario
                x[attribute]=self.transformObjectIds(x[attribute])#Se llama recursivamente al método transformObjectIds para transformar los valores del diccionario interno.
        return x

#formatear una lista x, reemplazando los elementos de tipo ObjectId por su representación de cadena
    def formatList(self, x):
        newList = []
        for item in x:
            if isinstance(item, ObjectId):
                newList.append(item.__str__())
        if len(newList) == 0:
            newList = x
        return newList

#transforma referencias de objetos en un diccionario theDict dentro de un objeto item
    def transformRefs(self, item):
        theDict = item.__dict__                                 #Se obtiene el diccionario que representa los atributos y valores del objeto item
        keys = list(theDict.keys())                             # Se obtiene una lista de las claves (atributos) presentes en el diccionario
        for k in keys:
            if theDict[k].__str__().count("object") == 1:       # si el valor asociado a la clave es una referencia a un objeto. Esto se determina comprobando si la representación de cadena del valor contiene la cadena "object"
# Se llama al método ObjectToDBRef para transformar el objeto de referencia a un DBRef. El objeto de referencia se obtiene utilizando getattr(item, k) para acceder al valor asociado a la clave k en el objeto item
                newObject = self.ObjectToDBRef(getattr(item, k))
                setattr(item, k, newObject)                     #Se asigna el nuevo objeto DBRef al atributo correspondiente en el objeto item utilizando setattr
        return item

#convierte un objeto item en un objeto DBRef de MongoDB
    def ObjectToDBRef(self, item: T):
#Se obtiene el nombre de la colección asociada al objeto item. Esto se hace accediendo a la clase del objeto (item.__class__), luego al nombre de la clase (__name__), y finalmente se convierte en minúsculas (lower()). El nombre de la colección se utiliza como parte del DBRef
        nameCollection = item.__class__.__name__.lower()
#Se crea un nuevo objeto DBRef utilizando el nombre de la colección obtenido en el paso anterior y el valor del atributo _id del objeto item. El _id se convierte en un objeto ObjectId utilizando ObjectId(item._id). El objeto DBRef resultante se devuelve como resultado
        return DBRef(nameCollection, ObjectId(item._id))
