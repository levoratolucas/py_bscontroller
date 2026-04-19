class DataLoader:
    """Gerencia o carregamento de dados"""
    
    def __init__(self, dados_relatorio, evento_controller):
        self.dados_relatorio = dados_relatorio
        self.evento_controller = evento_controller
        self.dados_atuais = []
    
    def carregar(self, data_inicio, data_fim, id_tecnico, filtro_status):
        dados_tabela, estatisticas = self.dados_relatorio.carregar_dados_tabela(
            data_inicio, data_fim, id_tecnico, filtro_status
        )
        
        self.dados_atuais = dados_tabela
        self.evento_controller.set_dados(dados_tabela)
        
        return dados_tabela, estatisticas
    
    def get_dados_atuais(self):
        return self.dados_atuais