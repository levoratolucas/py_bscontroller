from app.bd.endereco_repository import EnderecoRepository
from app.model.endereco import Endereco

class EnderecoController:
    def __init__(self):
        self.repo = EnderecoRepository()
        self.repo.criar_tabela()

    def inserir_endereco(self, logradouro, cidade, estado):
        endereco = Endereco(id=None, logradouro=logradouro, cidade=cidade, estado=estado)
        self.repo.inserir(endereco)

    def listar_enderecos(self):
        return self.repo.listar()