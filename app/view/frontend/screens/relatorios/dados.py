from datetime import datetime
from app.controller.repetido_controller import RepetidoController
from app.controller.relatorio_controller import RelatorioController

class DadosRelatorio:
    def __init__(self):
        self.repetido_controller = RepetidoController()
        self.relatorio_controller = RelatorioController()
    
    def carregar_estatisticas(self, data_inicio, data_fim, id_tecnico=None):
        """Carrega estatísticas do período"""
        estatisticas = self.repetido_controller.get_estatisticas_completas_periodo(
            data_inicio, data_fim, id_tecnico
        )
        return estatisticas
    
    def carregar_dados_tabela(self, data_inicio, data_fim, id_tecnico=None, filtro_status="todos"):
        """
        Carrega os dados para a tabela conforme o filtro
        
        Retorna:
            dados_tabela: lista de dicionários com os dados formatados
            estatisticas: dicionário com totais
        """
        mes_referencia = datetime.strptime(data_inicio, "%Y-%m-%d").strftime("%Y-%m")
        
        # Buscar repetidos da tabela (já analisados)
        repetidos_analisados = self.repetido_controller.get_repetidos_com_detalhes(mes_referencia)
        
        # Filtrar por técnico se necessário
        if id_tecnico:
            repetidos_analisados = [r for r in repetidos_analisados if r.get('tecnico_repetido') and 
                                    self._get_tecnico_id_por_nome(r['tecnico_repetido']) == id_tecnico]
        
        # Buscar OS pendentes (não analisadas)
        os_pendentes = self.relatorio_controller.get_os_repetidas_apenas(data_inicio, data_fim, id_tecnico)
        ids_analisados = self.repetido_controller.get_ids_os_analisados()
        os_pendentes = [os for os in os_pendentes if os.get('id_os') not in ids_analisados]
        
        # Contar por status
        total_pendentes = len(os_pendentes)
        total_procedem = len([r for r in repetidos_analisados if r.get('procedente') == 1])
        total_improcedem = len([r for r in repetidos_analisados if r.get('procedente') == 2])
        total_repetidos = total_pendentes + total_procedem + total_improcedem
        
        estatisticas = {
            'total_repetidos': total_repetidos,
            'pendentes': total_pendentes,
            'procedentes': total_procedem,
            'nao_procedentes': total_improcedem
        }
        
        # Montar dados da tabela conforme filtro
        dados_tabela = self._montar_dados_tabela(os_pendentes, repetidos_analisados, filtro_status)
        
        return dados_tabela, estatisticas
    
    def _montar_dados_tabela(self, os_pendentes, repetidos_analisados, filtro_status):
        """Monta os dados da tabela conforme o filtro"""
        dados_tabela = []
        
        if filtro_status == "pendentes":
            for os in os_pendentes:
                dados_tabela.append({
                    'numero': os.get('numero', '-'),
                    'wan_piloto': os.get('wan_piloto', '-'),
                    'tecnico': os.get('tecnico', '-'),
                    'data': os.get('data', '-'),
                    'inicio_execucao': os.get('inicio_execucao', '-'),
                    'fim_execucao': os.get('fim_execucao', '-'),
                    'status_nome': os.get('status_nome', '-'),
                    'observacao': '⏳ Pendente',
                    'pendente': True,
                    'id_os': os.get('id_os')
                })
        elif filtro_status == "procedem":
            for r in repetidos_analisados:
                if r.get('procedente') == 1:
                    dados_tabela.append({
                        'numero': r.get('numero_repetido', '-'),
                        'wan_piloto': r.get('wan_piloto', '-'),
                        'tecnico': r.get('tecnico_repetido', '-'),
                        'data': r.get('data_repetido', '-'),
                        'inicio_execucao': r.get('hora_repetido', '-'),
                        'fim_execucao': '-',
                        'status_nome': 'Concluído' if r.get('status_repetido') == 1 else 'Suspenso',
                        'observacao': '✅ Procede',
                        'pendente': False,
                        'id_os': r.get('id_os'),
                        'numero_referencia': r.get('numero_referencia'),
                        'tecnico_referencia': r.get('tecnico_referencia'),
                        'data_referencia': r.get('data_referencia'),
                        'carimbo_referencia': r.get('carimbo_referencia'),
                        'carimbo_repetido': r.get('carimbo_repetido')
                    })
        elif filtro_status == "nao_procedem":
            for r in repetidos_analisados:
                if r.get('procedente') == 2:
                    dados_tabela.append({
                        'numero': r.get('numero_repetido', '-'),
                        'wan_piloto': r.get('wan_piloto', '-'),
                        'tecnico': r.get('tecnico_repetido', '-'),
                        'data': r.get('data_repetido', '-'),
                        'inicio_execucao': r.get('hora_repetido', '-'),
                        'fim_execucao': '-',
                        'status_nome': 'Concluído' if r.get('status_repetido') == 1 else 'Suspenso',
                        'observacao': '❌ Não Procede',
                        'pendente': False,
                        'id_os': r.get('id_os'),
                        'numero_referencia': r.get('numero_referencia'),
                        'tecnico_referencia': r.get('tecnico_referencia'),
                        'data_referencia': r.get('data_referencia'),
                        'carimbo_referencia': r.get('carimbo_referencia'),
                        'carimbo_repetido': r.get('carimbo_repetido')
                    })
        else:  # "todos"
            for os in os_pendentes:
                dados_tabela.append({
                    'numero': os.get('numero', '-'),
                    'wan_piloto': os.get('wan_piloto', '-'),
                    'tecnico': os.get('tecnico', '-'),
                    'data': os.get('data', '-'),
                    'inicio_execucao': os.get('inicio_execucao', '-'),
                    'fim_execucao': os.get('fim_execucao', '-'),
                    'status_nome': os.get('status_nome', '-'),
                    'observacao': '⏳ Pendente',
                    'pendente': True,
                    'id_os': os.get('id_os')
                })
            for r in repetidos_analisados:
                status_texto = {1: "✅ Procede", 2: "❌ Não Procede"}
                dados_tabela.append({
                    'numero': r.get('numero_repetido', '-'),
                    'wan_piloto': r.get('wan_piloto', '-'),
                    'tecnico': r.get('tecnico_repetido', '-'),
                    'data': r.get('data_repetido', '-'),
                    'inicio_execucao': r.get('hora_repetido', '-'),
                    'fim_execucao': '-',
                    'status_nome': 'Concluído' if r.get('status_repetido') == 1 else 'Suspenso',
                    'observacao': status_texto.get(r.get('procedente', 0), 'Desconhecido'),
                    'pendente': False,
                    'id_os': r.get('id_os'),
                    'numero_referencia': r.get('numero_referencia'),
                    'tecnico_referencia': r.get('tecnico_referencia'),
                    'data_referencia': r.get('data_referencia'),
                    'carimbo_referencia': r.get('carimbo_referencia'),
                    'carimbo_repetido': r.get('carimbo_repetido')
                })
        
        return dados_tabela
    
    def _get_tecnico_id_por_nome(self, nome):
        """Retorna o ID do técnico pelo nome"""
        tecnicos = self.relatorio_controller.get_tecnicos()
        for t in tecnicos:
            if t['nome'] == nome:
                return t['id']
        return None
    
    def get_tecnicos(self):
        """Retorna lista de técnicos"""
        return self.relatorio_controller.get_tecnicos()
    
    def get_periodos_producao(self):
        """Calcula os períodos de produção"""
        from datetime import datetime, timedelta
        
        periodos = []
        hoje = datetime.now()
        
        for i in range(12):
            data_fim = datetime(hoje.year, hoje.month, 1) - timedelta(days=i * 30)
            
            if data_fim.day >= 21:
                data_inicio = datetime(data_fim.year, data_fim.month, 21)
            else:
                if data_fim.month > 1:
                    data_inicio = datetime(data_fim.year, data_fim.month - 1, 21)
                else:
                    data_inicio = datetime(data_fim.year - 1, 12, 21)
            
            data_fim = data_inicio + timedelta(days=30)
            data_fim = datetime(data_fim.year, data_fim.month, 20)
            
            nome = f"{data_inicio.strftime('%d/%m/%Y')} a {data_fim.strftime('%d/%m/%Y')}"
            periodos.append({
                'nome': nome,
                'inicio': data_inicio.strftime("%Y-%m-%d"),
                'fim': data_fim.strftime("%Y-%m-%d")
            })
        
        return periodos