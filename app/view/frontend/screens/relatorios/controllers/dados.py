from datetime import datetime, timedelta
from app.controller.relatorio_controller import RelatorioController

class DadosRelatorio:
    def __init__(self):
        self.controller = RelatorioController()
    
    def get_periodo_atual(self):
        hoje = datetime.now()
        primeiro_dia = datetime(hoje.year, hoje.month, 1)
        
        if hoje.month == 12:
            ultimo_dia = datetime(hoje.year + 1, 1, 1) - timedelta(days=1)
        else:
            ultimo_dia = datetime(hoje.year, hoje.month + 1, 1) - timedelta(days=1)
        
        return primeiro_dia.strftime("%Y-%m-%d"), ultimo_dia.strftime("%Y-%m-%d")
    
    def get_dados_periodo(self, data_inicio, data_fim):
        resumo = self.controller.get_resumo_periodo(data_inicio, data_fim)
        wans = self.controller.get_wans_repetidos_resumo(data_inicio, data_fim)
        
        return {
            'repetidos': resumo['repeticoes'],
            'total_os': resumo['total_os'],
            'ofensor': resumo['ofensor'],
            'wans': wans
        }