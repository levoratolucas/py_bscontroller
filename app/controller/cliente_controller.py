from app.bd.cliente_repository import ClienteRepository
from app.model.cliente import Cliente

class ClienteController:
    def __init__(self):
        self.repo = ClienteRepository()
        self.repo.criar_tabela()

    def inserir_cliente(self, nome):
        # Verificar se cliente já existe
        cliente_existente = self.buscar_cliente_por_nome(nome)
        if cliente_existente:
            print(f"⚠️ Cliente '{nome}' já existe com ID {cliente_existente.id_cliente}")
            return cliente_existente
        
        cliente = Cliente(nome=nome, id=None)
        self.repo.inserir(cliente)
        return cliente

    def buscar_cliente_por_nome(self, nome):
        clientes = self.repo.listar()
        for cliente in clientes:
            if cliente.nome.lower() == nome.lower():  # Case insensitive
                return cliente
        return None

    def listar_clientes(self):
        return self.repo.listar()