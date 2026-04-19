class EventHandlers:
    """Gerencia os handlers de eventos"""
    
    def __init__(self, evento_controller, data_loader, detalhes, cards, tabela, filtros):
        self.evento_controller = evento_controller
        self.data_loader = data_loader
        self.detalhes = detalhes
        self.cards = cards
        self.tabela = tabela
        self.filtros = filtros
        self.filtro_status_atual = "todos"
    
    def on_card_click(self, status):
        self.filtro_status_atual = status
        self._destacar_card(status)
        self.on_filtrar()
    
    def _destacar_card(self, status):
        for card in self.cards.values():
            card.destacar(False)
        
        mapa = {
            "pendentes": self.cards['pendente'],
            "todos": self.cards['repetido'],
            "procedem": self.cards['procede'],
            "nao_procedem": self.cards['improcedente']
        }
        
        if status in mapa:
            mapa[status].destacar(True)
    
    def on_filtrar(self):
        data_inicio, data_fim = self.filtros.obter_periodo()
        tecnico_nome = self.filtros.tecnico_var.get()
        
        from app.view.frontend.screens.relatorios.tools_main.filtros import FiltroHelper
        from app.view.frontend.screens.relatorios.dados import DadosRelatorio
        
        dados_relatorio = DadosRelatorio()
        id_tecnico = None
        if tecnico_nome != "Todos":
            tecnicos = dados_relatorio.get_tecnicos()
            id_tecnico = FiltroHelper.get_id_tecnico_por_nome(tecnicos, tecnico_nome)
        
        dados_tabela, estatisticas = self.data_loader.carregar(data_inicio, data_fim, id_tecnico, self.filtro_status_atual)
        
        # Atualizar cards
        self.cards['pendente'].set_valor(estatisticas['pendentes'])
        self.cards['repetido'].set_valor(estatisticas['total_repetidos'])
        self.cards['procede'].set_valor(estatisticas['procedentes'])
        self.cards['improcedente'].set_valor(estatisticas['nao_procedentes'])
        
        # Atualizar tabela
        self.tabela.carregar(dados_tabela)
        self.detalhes.limpar()
        
        # Atualizar título
        titulos = {
            "pendentes": "📋 Histórico de Repetições - PENDENTES (⏳)",
            "todos": "📋 Histórico de Repetições - TODOS (🔄)",
            "procedem": "📋 Histórico de Repetições - PROCEDEM (✅)",
            "nao_procedem": "📋 Histórico de Repetições - IMPROCEDEM (❌)"
        }
        self.tabela.set_titulo(titulos.get(self.filtro_status_atual, titulos["todos"]))
    
    def on_selecionar_linha(self, valores):
        resultado = self.evento_controller.on_selecionar(valores)
        if resultado:
            texto_selecionada, texto_referencia = resultado
            self.detalhes.set_detalhes(texto_selecionada, texto_referencia)
    
    def on_duplo_clique(self, valores):
        self.evento_controller.on_duplo_clique(valores)