from Repositorios.RepositorioCandidato import RepositorioCandidato
from Repositorios.RepositorioPartido import RepositorioPartido
from Modelos.Candidato import Candidato
from Modelos.Partido import Partido
class ControladorCandidato():
    def __init__(self):
        self.RepositorioCandidato = RepositorioCandidato()
        self.RepositorioPartido = RepositorioPartido()

# Relacion Candidato - Partido
    def asignarPartido(self, id, id_partido):
        candidatoActual = Candidato(self.RepositorioCandidato.findById(id))
        partidoActual = Partido(self.RepositorioPartido.findById(id_partido))
        candidatoActual.partido = partidoActual
        return self.RepositorioCandidato.save(candidatoActual)

#lista todos los candidatos registrados
    def index(self):
        return self.RepositorioCandidato.findAll()

#crea un nuevo registro de candidato
    def create(self, infoCandidato):
        nuevoCandidato = Candidato(infoCandidato)
        return self.RepositorioCandidato.save(nuevoCandidato)

#retorna un diccionario con la informacion de un candidato basado en su id
    def show(self, id):
        elCandidato = Candidato(self.RepositorioCandidato.findById(id))
        return elCandidato.__dict__

    def update(self, id, infoCandidato):
        CandidatoActual = Candidato(self.RepositorioCandidato.findById(id))
        CandidatoActual.cedula = infoCandidato["cedula"]
        CandidatoActual.numero_resolucion = infoCandidato["numero_resolucion"]
        CandidatoActual.nombre = infoCandidato["nombre"]
        CandidatoActual.apellido = infoCandidato["apellido"]
        return self.RepositorioCandidato.save(CandidatoActual)

    def delete(self, id):
        return self.RepositorioCandidato.delete(id)