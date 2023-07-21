from abc import ABCMeta
#esta clase abstracta es el padre de todas las clases de tipo modelo
class AbstractModelo(metaclass=ABCMeta):
    def __init__(self, data):
        for llave, valor in data.items():
            setattr(self, llave, valor)
