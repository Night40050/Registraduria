from Modelos.Mesa import Mesa
class ControladorMesa():
#constructor del controlador
    def __init__(self):
        print("Creando ControladorMesa")

    def index(self):
        print("Listar todas las mesas")
        unaMesa = {
            "numero": "123",
            "cantidad_inscritos": "123"
        }
        return [unaMesa]

    def create(self, infoMesa):
        print("Crear una mesa")
        laMesa = Mesa(infoMesa)
        return laMesa.__dict__

    def show(self,id):
        print("Mostrando mesa con id ", id)
        laMesa = {
            "numero": "123",
            "cantidad_inscritos": "123"
        }
        return laMesa

    def update(self, numero, infoMesa):
        print("Actualizando mesa numero" , numero)
        laMesa = Mesa(infoMesa)
        return laMesa.__dict__

    def delete(self, numero):
        print("Elimiando mesa numero ", numero)
        return {"deleted_count": 1}