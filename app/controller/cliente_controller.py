# app/controller/cliente_controller.py

from app.bd.cliente_repository import ClienteRepository
from app.model.cliente import Cliente

class ClienteController:
    def __init__(self):
        self.repo = ClienteRepository()
        self.repo.criar_tabela()

    def inserir_cliente(self, nome):
        cliente = Cliente(nome)  # sem id
        self.repo.inserir(cliente)

    def listar_clientes(self):
        return self.repo.listar()