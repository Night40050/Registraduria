from Repositorios.RepositorioMesa import RepositorioMesa
from Modelos.Mesa import Mesa

class ControladorMesa():
    def __init__(self):
        self.RepositorioMesa = RepositorioMesa()

    def index(self):
        return self.RepositorioMesa.findAll()
    def create(self, infoMesa):
        nuevaMesa = Mesa(infoMesa)
        return self.RepositorioMesa.save(nuevaMesa)
    def show(self, id):
        laMesa = Mesa(self.RepositorioMesa.findById(id))
        return laMesa.__dict__

    def update(self, id, infoMesa):
        mesaActual = Mesa(self.RepositorioMesa.findById(id))
        mesaActual.numero = infoMesa["numero"]
        mesaActual.cantidad_inscritos = infoMesa["cantidad_inscritos"]
        return self.RepositorioMesa.save(mesaActual)

    def delete(self, id):
        return self.RepositorioMesa.delete(id)
