from Repositorios.RepositorioResultado import RepositorioResultado
from Repositorios.RepositorioCandidato import RepositorioCandidato
from Repositorios.RepositorioMesa      import RepositorioMesa
from Modelos.Resultado import Resultado
from Modelos.Candidato import Candidato
from Modelos.Mesa      import Mesa

class ControladorResultado():
    def __init__(self):
        self.RepositorioResultado = RepositorioResultado()
        self.RepositorioCandidato = RepositorioCandidato()
        self.RepositorioMesa = RepositorioMesa()

    def index(self):
        return self.RepositorioResultado.findAll()

    """Asignacion mesa y candidato a resultado"""
    def create(self, infoResultado, id_mesa, id_candidato):
        nuevoResultado = Resultado(infoResultado)
        laMesa=Mesa(self.RepositorioMesa.findById(id_mesa))
        elCandidato=Candidato(self.RepositorioCandidato.findById(id_candidato))
        nuevoResultado.mesa = laMesa
        nuevoResultado.candidato = elCandidato
        return self.RepositorioResultado.save(nuevoResultado)

    def show(self, id):
        elResultado = Resultado(self.RepositorioResultado.findById(id))
        return elResultado.__dict__

    """modificacion de resultado (mesa candidato)"""
    def update(self, id, infoResultado, id_mesa, id_candidato):
        resultadoActual = Resultado(self.RepositorioResultado.findById(id))
        resultadoActual.fecha = infoResultado["fecha"]
        resultadoActual.nVotantes = infoResultado["nVotantes"]
        laMesa = Mesa(self.RepositorioMesa.findById(id_mesa))
        elCandidato = Candidato(self.RepositorioCandidato.findById(id_candidato))
        resultadoActual.mesa = laMesa
        resultadoActual.candidato = elCandidato
        return self.RepositorioResultado.save(resultadoActual)

    def delete(self, id):
        return self.RepositorioResultado.delete(id)