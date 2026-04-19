import customtkinter as ctk
from app.controller.relatorio_controller import RelatorioController
from app.controller.ordem_servico_controller import OrdemServicoController
from app.controller.repetido_controller import RepetidoController
from app.view.frontend.screens.relatorios.dados import DadosRelatorio
from app.view.frontend.screens.relatorios.controllers import EventoController
from app.view.frontend.screens.relatorios.tools_main import (
    UIBuilder, DataLoader, EventHandlers, ExportDialog
)


class RelatoriosScreen(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent, fg_color="transparent")
        self.pack(fill="both", expand=True)
        
        self.app = app
        self.relatorio_controller = RelatorioController()
        self.os_controller = OrdemServicoController()
        self.repetido_controller = RepetidoController()
        self.dados_relatorio = DadosRelatorio()
        
        self.setup_ui()
        self.inicializar_dados()
    
    def setup_ui(self):
        # Main frame
        self.main_frame = ctk.CTkFrame(self, fg_color="#0a0a0a")
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Título
        UIBuilder.criar_titulo(self.main_frame)
        
        # Botão exportar
        self.botoes = UIBuilder.criar_botoes(self.main_frame, self.abrir_exportacao)
        
        # Cards
        callbacks = {
            'pendente': lambda: self.event_handlers.on_card_click("pendentes"),
            'repetido': lambda: self.event_handlers.on_card_click("todos"),
            'procede': lambda: self.event_handlers.on_card_click("procedem"),
            'improcedente': lambda: self.event_handlers.on_card_click("nao_procedem")
        }
        self.cards, _ = UIBuilder.criar_cards(self.main_frame, callbacks)
        
        # Filtros
        tecnicos = self.dados_relatorio.get_tecnicos()
        periodos = self.dados_relatorio.get_periodos_producao()
        self.filtros = UIBuilder.criar_filtros(self.main_frame, self.on_filtrar, tecnicos, periodos)
        
        # Container principal
        _, container_tabela, container_detalhes = UIBuilder.criar_container_principal(self.main_frame)
        
        # Tabela
        self.tabela = UIBuilder.criar_tabela(container_tabela, self.on_selecionar_linha, self.on_duplo_clique)
        
        # Detalhes
        self.detalhes = UIBuilder.criar_detalhes(container_detalhes)
        
        # Controladores
        self.evento_controller = EventoController(
            parent=self,
            repetido_controller=self.repetido_controller,
            relatorio_controller=self.relatorio_controller,
            os_controller=self.os_controller,
            aplicar_filtro_callback=self.on_filtrar
        )
        self.evento_controller.set_obter_periodo_callback(self.filtros.obter_periodo)
        
        # Data Loader
        self.data_loader = DataLoader(self.dados_relatorio, self.evento_controller)
        
        # Event Handlers
        self.event_handlers = EventHandlers(
            evento_controller=self.evento_controller,
            data_loader=self.data_loader,
            detalhes=self.detalhes,
            cards=self.cards,
            tabela=self.tabela,
            filtros=self.filtros
        )
    
    def inicializar_dados(self):
        self.event_handlers.on_filtrar()
    
    def on_filtrar(self):
        self.event_handlers.on_filtrar()
    
    def on_selecionar_linha(self, valores):
        self.event_handlers.on_selecionar_linha(valores)
    
    def on_duplo_clique(self, valores):
        self.event_handlers.on_duplo_clique(valores)
    
    def abrir_exportacao(self):
        dialog = ExportDialog(self, self.relatorio_controller, self.os_controller, self.dados_relatorio)
        dialog.abrir()