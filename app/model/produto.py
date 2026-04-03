class Produto:
    def __init__(self,  descricao, designador, wan_piloto, id_cliente_endereco, id = None):
        self.id_produto = id
        self.descricao = descricao
        self.designador = designador
        self.wan_piloto = wan_piloto
        self.id_cliente_endereco = id_cliente_endereco