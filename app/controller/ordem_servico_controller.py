from app.bd.ordem_servico_repository import OrdemServicoRepository
from app.model.ordem_servico import OrdemServico

class OrdemServicoController:
    def __init__(self):
        self.repo = OrdemServicoRepository()
        self.repo.criar_tabela()

    def inserir_ordem(self, id_tecnico, id_produto, causa_raiz, materiais_utilizados, acao, contato_responsavel, observacoes, data_criacao, concluida, data_conclusao):
        ordem = OrdemServico(
            id_os=None,
            id_tecnico=id_tecnico,
            id_produto=id_produto,
            causa_raiz=causa_raiz,
            materiais_utilizados=materiais_utilizados,
            acao=acao,
            contato_responsavel=contato_responsavel,
            observacoes=observacoes,
            data_criacao=data_criacao,
            concluida=concluida,
            data_conclusao=data_conclusao
        )
        self.repo.inserir(ordem)

    def listar_ordens(self):
        return self.repo.listar()