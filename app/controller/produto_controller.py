from app.bd.produto_repository import ProdutoRepository
from app.model.produto import Produto

class ProdutoController:
    def __init__(self):
        self.repo = ProdutoRepository()
        self.repo.criar_tabela()

    def inserir_produto(self, descricao, designador, wan_piloto, id_cliente_endereco):
        produto = Produto(id=None, descricao=descricao, designador=designador, wan_piloto=wan_piloto, id_cliente_endereco=id_cliente_endereco)
        self.repo.inserir(produto)

    def listar_produtos(self):
        return self.repo.listar()