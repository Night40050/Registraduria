from Modelos.Partido import Mesa
class ControladorPartido():
#constructor del controlador
    def __init__(self):
        print("Creando ControladorPartido")

    def index(self):
        print("Listar todos los partidos")
        unPartido = {
            "id": "abc123",
            "nombre": "Partido xxxxxxxx",
            "lema": "Lorem ipsum..."
        }
        return [unPartido]

    def create(self,infoPartido):
        print("Crear un partido")
        elPartido = Mesa(infoPartido)
        return elPartido.__dict__

    def show(self,id):
        print("Mostrando partido con id ", id)
        elPartido = {
            "id": id,
            "nombre": "Partido xxxxxxxx",
            "lema": "Lorem ipsum..."
        }
        return elPartido

    def update(self, id, infoPartido):
        print("Actualizando partido con el id ", id)
        elPartido = Mesa(infoPartido)
        return elPartido.__dict__

    def delete(self, id):
        print("Elimiando Partido con el id ", id)
        return {"deleted_count": 1}