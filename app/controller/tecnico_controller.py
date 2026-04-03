from app.bd.tecnico_repository import TecnicoRepository
from app.model.tecnico import Tecnico

class TecnicoController:
    def __init__(self):
        self.repo = TecnicoRepository()
        self.repo.criar_tabela()

    def inserir_tecnico(self, nome, matricula):
        tecnico = Tecnico(id=None, nome=nome, matricula=matricula)
        self.repo.inserir(tecnico)

    def listar_tecnicos(self):
        return self.repo.listar()