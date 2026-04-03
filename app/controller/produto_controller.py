from app.bd.produto_repository import ProdutoRepository
from app.model.produto import Produto

class ProdutoController:
    def __init__(self):
        self.repo = ProdutoRepository()

    def inserir_produto(self, descricao, designador, wan_piloto, id_cliente_endereco):
        # Verificar se produto já existe (opcional - pela descrição)
        produto_existente = self.buscar_produto_por_descricao(descricao)
        if produto_existente:
            print(f"⚠️ Produto '{descricao}' já existe!")
            return produto_existente
        
        produto = Produto(
            descricao=descricao,
            designador=designador,
            wan_piloto=wan_piloto,
            id_cliente_endereco=id_cliente_endereco,
            id=None
        )
        self.repo.inserir(produto)
        return produto

    def buscar_produto_por_descricao(self, descricao):
        produtos = self.repo.listar()
        for produto in produtos:
            if produto.descricao.lower() == descricao.lower():
                return produto
        return None

    def listar_produtos(self):
        return self.repo.listar()