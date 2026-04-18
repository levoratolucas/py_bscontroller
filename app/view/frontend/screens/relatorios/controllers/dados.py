from datetime import datetime, timedelta
from app.controller.relatorio_controller import RelatorioController
from app.controller.repetido_controller import RepetidoController

class DadosRelatorio:
    def __init__(self):
        self.controller = RelatorioController()
        self.repetido_controller = RepetidoController()
    
    def get_periodo_atual(self):
        """Retorna o período do mês atual (primeiro e último dia)"""
        hoje = datetime.now()
        primeiro_dia = datetime(hoje.year, hoje.month, 1)
        
        if hoje.month == 12:
            ultimo_dia = datetime(hoje.year + 1, 1, 1) - timedelta(days=1)
        else:
            ultimo_dia = datetime(hoje.year, hoje.month + 1, 1) - timedelta(days=1)
        
        return primeiro_dia.strftime("%Y-%m-%d"), ultimo_dia.strftime("%Y-%m-%d")
    
    def get_periodo_mes(self, ano, mes):
        """Retorna o período de um mês específico"""
        primeiro_dia = datetime(int(ano), int(mes), 1)
        
        if int(mes) == 12:
            ultimo_dia = datetime(int(ano) + 1, 1, 1) - timedelta(days=1)
        else:
            ultimo_dia = datetime(int(ano), int(mes) + 1, 1) - timedelta(days=1)
        
        return primeiro_dia.strftime("%Y-%m-%d"), ultimo_dia.strftime("%Y-%m-%d")
    
    def get_dados_periodo(self, data_inicio, data_fim, id_tecnico=None):
        """
        Retorna dados do período usando a tabela repetidos
        
        Parâmetros:
            data_inicio: data inicial (YYYY-MM-DD)
            data_fim: data final (YYYY-MM-DD)
            id_tecnico: ID do técnico (opcional)
        
        Retorna:
            {
                'repetidos': total de repetidos,
                'total_os': total de OS no período,
                'ofensor': percentual de repetidos,
                'procedentes': quantos foram marcados como PROCEDE,
                'nao_procedentes': quantos foram marcados como NÃO PROCEDE,
                'pendentes': quantos estão pendentes,
                'percentual_procedente': percentual de procedentes sobre repetidos,
                'periodo': {'inicio': ..., 'fim': ...},
                'tecnico': nome do técnico ou 'Todos'
            }
        """
        # Usar a função do RepetidoController
        estatisticas = self.repetido_controller.get_estatisticas_completas_periodo(
            data_inicio, data_fim, id_tecnico
        )
        
        return {
            'repetidos': estatisticas['total_repetidos'],
            'total_os': estatisticas['total_os'],
            'ofensor': estatisticas['ofensor'],
            'procedentes': estatisticas['procedentes'],
            'nao_procedentes': estatisticas['nao_procedentes'],
            'pendentes': estatisticas['pendentes'],
            'percentual_procedente': estatisticas['percentual_procedente'],
            'periodo': estatisticas['periodo'],
            'tecnico': estatisticas['tecnico']
        }
    
    def get_estatisticas_por_tecnico(self, data_inicio, data_fim):
        """
        Retorna estatísticas agrupadas por técnico no período
        
        Retorna:
            [
                {
                    'id_tecnico': 1,
                    'tecnico': 'João Silva',
                    'total_os': 20,
                    'total_repetidos': 3,
                    'procedentes': 2,
                    'nao_procedentes': 0,
                    'pendentes': 1,
                    'ofensor': 15.0
                },
                ...
            ]
        """
        return self.repetido_controller.get_os_por_tecnico_periodo(data_inicio, data_fim)
    
    def get_wans_repetidos(self, data_inicio, data_fim, id_tecnico=None):
        """
        Retorna a lista de WANs repetidas no período
        
        Retorna:
            [
                {
                    'wan': '192.168.1.1',
                    'total': 3,
                    'primeira_data': '2026-03-10',
                    'ultima_data': '2026-03-25'
                },
                ...
            ]
        """
        mes_referencia = datetime.strptime(data_inicio, "%Y-%m-%d").strftime("%Y-%m")
        repetidos_mes = self.repetido_controller.get_repetidos_com_detalhes(mes_referencia)
        
        # Filtrar por técnico se necessário
        if id_tecnico:
            repetidos_mes = [r for r in repetidos_mes if r.get('tecnico_repetido') and 
                            self._get_tecnico_id_por_nome(r['tecnico_repetido']) == id_tecnico]
        
        # Agrupar por WAN
        wans_dict = {}
        for item in repetidos_mes:
            wan = item.get('wan_piloto', 'Desconhecido')
            if wan not in wans_dict:
                wans_dict[wan] = {
                    'wan': wan,
                    'total': 0,
                    'primeira_data': item.get('data_referencia', '-'),
                    'ultima_data': item.get('data_repetido', '-')
                }
            wans_dict[wan]['total'] += 1
        
        # Ordenar por total decrescente
        resultado = sorted(wans_dict.values(), key=lambda x: x['total'], reverse=True)
        
        return resultado
    
    def get_detalhes_repetidos(self, data_inicio, data_fim, id_tecnico=None, status_filter=None):
        """
        Retorna os detalhes completos dos repetidos no período
        
        Parâmetros:
            data_inicio: data inicial
            data_fim: data final
            id_tecnico: ID do técnico (opcional)
            status_filter: 'todos', 'pendentes', 'procedem', 'nao_procedem'
        
        Retorna:
            [
                {
                    'id': 1,
                    'id_os': 49,
                    'numero_repetido': '1233000',
                    'wan_piloto': 'abb',
                    'data_repetido': '2026-04-12',
                    'hora_repetido': '17:00',
                    'tecnico_repetido': 'João',
                    'numero_referencia': '1230000',
                    'data_referencia': '2026-03-30',
                    'tecnico_referencia': 'Maria',
                    'procedente': 0,
                    'status_texto': 'Pendente'
                },
                ...
            ]
        """
        mes_referencia = datetime.strptime(data_inicio, "%Y-%m-%d").strftime("%Y-%m")
        repetidos = self.repetido_controller.get_repetidos_com_detalhes(mes_referencia)
        
        # Filtrar por técnico se necessário
        if id_tecnico:
            repetidos = [r for r in repetidos if r.get('tecnico_repetido') and 
                        self._get_tecnico_id_por_nome(r['tecnico_repetido']) == id_tecnico]
        
        # Filtrar por status
        if status_filter and status_filter != 'todos':
            status_map = {'pendentes': 0, 'procedem': 1, 'nao_procedem': 2}
            status_valor = status_map.get(status_filter)
            if status_valor is not None:
                repetidos = [r for r in repetidos if r.get('procedente') == status_valor]
        
        # Adicionar texto do status
        status_texto = {0: 'Pendente', 1: 'Procede', 2: 'Não Procede'}
        for r in repetidos:
            r['status_texto'] = status_texto.get(r.get('procedente', 0), 'Desconhecido')
        
        return repetidos
    
    def get_dashboard_data(self, data_inicio, data_fim, id_tecnico=None):
        """
        Retorna dados completos para o dashboard
        
        Retorna:
            {
                'resumo': {...},
                'metricas': [...],
                'estatisticas_tipo': {...},
                'apu_individual': [...],
                'wans_repetidos': [...],
                'detalhes_repetidos': [...]
            }
        """
        # Resumo do período
        resumo = self.get_dados_periodo(data_inicio, data_fim, id_tecnico)
        
        # Métricas para gráficos
        metricas = self.controller.get_metricas_radar(data_inicio, data_fim, id_tecnico)
        
        # Estatísticas por tipo
        estatisticas_tipo = self.controller.get_estatisticas_por_tipo(data_inicio, data_fim)
        
        # APU individual
        apu_individual = self.controller.get_apu_individual(data_inicio, data_fim, id_tecnico)
        
        # WANs repetidos
        wans_repetidos = self.get_wans_repetidos(data_inicio, data_fim, id_tecnico)
        
        # Detalhes dos repetidos
        detalhes_repetidos = self.get_detalhes_repetidos(data_inicio, data_fim, id_tecnico)
        
        return {
            'resumo': resumo,
            'metricas': metricas,
            'estatisticas_tipo': estatisticas_tipo,
            'apu_individual': apu_individual,
            'wans_repetidos': wans_repetidos,
            'detalhes_repetidos': detalhes_repetidos
        }
    
    def _get_tecnico_id_por_nome(self, nome):
        """Retorna o ID do técnico pelo nome"""
        tecnicos = self.controller.get_tecnicos()
        for t in tecnicos:
            if t['nome'] == nome:
                return t['id']
        return None