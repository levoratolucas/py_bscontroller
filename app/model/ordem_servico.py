from datetime import datetime

class OrdemServico:
    def __init__(self, id_tecnico, id_produto, causa_raiz, materiais_utilizados, 
                 acao, contato_responsavel, observacoes, number_bd=None, tipo=None,
                 data_criacao=None, concluida=False, data_conclusao=None, id_os=None):
        self.id_os = id_os
        self.id_tecnico = id_tecnico
        self.id_produto = id_produto
        self.causa_raiz = causa_raiz
        self.number_bd = number_bd
        self.tipo = tipo
        self.materiais_utilizados = materiais_utilizados
        self.acao = acao
        self.contato_responsavel = contato_responsavel
        self.observacoes = observacoes
        self.data_criacao = data_criacao if data_criacao else datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.concluida = concluida
        self.data_conclusao = data_conclusao
    
    def concluir(self):
        """Método para concluir a OS com data/hora atual"""
        self.concluida = True
        self.data_conclusao = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def __str__(self):
        status = "CONCLUÍDA" if self.concluida else "EM ANDAMENTO"
        return f"OS {self.id_os} - {status} - Abertura: {self.data_criacao}"