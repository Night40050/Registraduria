from Repositorios.RepositorioPartido import RepositorioPartido
from Modelos.Partido import Partido

class ControladorPartido():

    def __init__(self):
        self.RepositorioPartido = RepositorioPartido()

    def index(self):
        return self.RepositorioPartido.findAll()

    def create(self, infoPartido):
        nuevoPartido = Partido(infoPartido)
        return self.RepositorioPartido.save(nuevoPartido)

    def show(self, id):
        elPartido = Partido(self.RepositorioPartido.findById(id))
        return elPartido.__dict__

    def update(self, id, infoPartido):
        partidoActual = Partido(self.RepositorioPartido.findById(id))
        partidoActual.nombre = infoPartido["nombre"]
        partidoActual.lema = infoPartido["lema"]
        return self.RepositorioPartido.save(partidoActual)

    def delete(self, id):
        return self.RepositorioPartido.delete(id)
