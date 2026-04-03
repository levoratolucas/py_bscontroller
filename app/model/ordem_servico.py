class OrdemServico:
    def __init__(self,  id_tecnico, id_produto, causa_raiz, materiais_utilizados, acao, contato_responsavel, observacoes, data_criacao, concluida, data_conclusao=None, id_os = None):
        self.id_os = id_os
        self.id_tecnico = id_tecnico
        self.id_produto = id_produto
        self.causa_raiz = causa_raiz
        self.materiais_utilizados = materiais_utilizados
        self.acao = acao
        self.contato_responsavel = contato_responsavel
        self.observacoes = observacoes
        self.data_criacao = data_criacao
        self.concluida = concluida  # Booleano indicando se está concluído
        self.data_conclusao = data_conclusao  # Opcional, data em que foi concluída