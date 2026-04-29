from datetime import datetime, timedelta
from app.controller.ordem_servico_controller import OrdemServicoController
from app.controller.relatorio_controller import RelatorioController
from app.view.frontend.screens.dashboard.tools_main.metricas import MetricasHelper
from app.view.frontend.screens.dashboard.tools_main.rankings import RankingsHelper

class DadosDashboard:
    def __init__(self):
        self.os_controller = OrdemServicoController()
        self.relatorio_controller = RelatorioController()
    
    def get_periodo_atual(self):
        """Retorna o período do mês atual"""
        hoje = datetime.now()
        primeiro_dia = datetime(hoje.year, hoje.month, 1)
        
        if hoje.month == 12:
            ultimo_dia = datetime(hoje.year + 1, 1, 1) - timedelta(days=1)
        else:
            ultimo_dia = datetime(hoje.year, hoje.month + 1, 1) - timedelta(days=1)
        
        return primeiro_dia.strftime("%Y-%m-%d"), ultimo_dia.strftime("%Y-%m-%d")
    
    def carregar_estatisticas_os(self, data_inicio, data_fim):
        """Carrega estatísticas de OS do período"""
        return self.os_controller.get_estatisticas_periodo(data_inicio, data_fim)
    
    def carregar_metricas_tecnicos(self, data_inicio, data_fim):
        """Carrega métricas dos técnicos"""
        metricas = self.relatorio_controller.get_metricas_radar(data_inicio, data_fim)
        return MetricasHelper.calcular_percentual_ofensor(metricas)
    
    def carregar_todos_dados(self, data_inicio, data_fim):
        """Carrega todos os dados do dashboard"""
        stats_os = self.carregar_estatisticas_os(data_inicio, data_fim)
        metricas = self.carregar_metricas_tecnicos(data_inicio, data_fim)
        
        total_os = stats_os.get('total', 0)
        total_repeticoes = MetricasHelper.calcular_total_repeticoes(metricas)
        percentual_repeticoes = MetricasHelper.calcular_percentual_repeticoes(total_repeticoes, total_os)
        media_apu = MetricasHelper.calcular_media_apu(metricas)
        
        ranking_ofensores = RankingsHelper.ranking_ofensores(metricas)
        ranking_apu = RankingsHelper.ranking_apu(metricas)
        medalhas = RankingsHelper.medalhas()
        
        return {
            'stats_os': stats_os,
            'metricas': metricas,
            'total_os': total_os,
            'total_repeticoes': total_repeticoes,
            'percentual_repeticoes': percentual_repeticoes,
            'media_apu': media_apu,
            'ranking_ofensores': ranking_ofensores,
            'ranking_apu': ranking_apu,
            'medalhas': medalhas
        }