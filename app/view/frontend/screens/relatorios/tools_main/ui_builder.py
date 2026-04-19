import customtkinter as ctk
from app.view.frontend.styles import COLORS, FONTS
from app.view.frontend.screens.relatorios.cards import (
    CardPendente, CardRepetido, CardProcede, CardImprocedente
)
from app.view.frontend.screens.relatorios.components import (
    TabelaRepetidos, FiltrosWidget, BotoesAcao, AreaDetalhes
)

class UIBuilder:
    """Construtor da interface do usuário"""
    
    @staticmethod
    def criar_titulo(parent):
        titulo_frame = ctk.CTkFrame(parent, fg_color="transparent")
        titulo_frame.pack(fill="x", pady=(0, 20))
        
        ctk.CTkLabel(
            titulo_frame,
            text="📊 RELATÓRIOS - REPETIDOS",
            font=('Arial', 22, 'bold'),
            text_color="#00ff88"
        ).pack(anchor="w")
        
        ctk.CTkLabel(
            titulo_frame,
            text="Análise de WANs repetidos | Clique nos cards para filtrar | Duplo clique apenas em PENDENTES",
            font=('Arial', 12),
            text_color="#666666"
        ).pack(anchor="w")
        
        return titulo_frame
    
    @staticmethod
    def criar_cards(parent, callbacks):
        cards_frame = ctk.CTkFrame(parent, fg_color="transparent")
        cards_frame.pack(fill="x", pady=(0, 25))
        
        for i in range(4):
            cards_frame.grid_columnconfigure(i, weight=1)
        
        cards = {
            'pendente': CardPendente(cards_frame, 0, 0, callback=callbacks.get('pendente')),
            'repetido': CardRepetido(cards_frame, 0, 1, callback=callbacks.get('repetido')),
            'procede': CardProcede(cards_frame, 0, 2, callback=callbacks.get('procede')),
            'improcedente': CardImprocedente(cards_frame, 0, 3, callback=callbacks.get('improcedente'))
        }
        
        return cards, cards_frame
    
    @staticmethod
    def criar_container_principal(parent):
        container = ctk.CTkFrame(parent, fg_color="transparent")
        container.pack(fill="both", expand=True)
        
        container.grid_columnconfigure(0, weight=30)
        container.grid_columnconfigure(1, weight=70)
        container.grid_rowconfigure(0, weight=1)
        
        container_tabela = ctk.CTkFrame(container, fg_color="transparent")
        container_tabela.grid(row=0, column=0, sticky="nsew", padx=(0, 10), pady=0)
        
        container_detalhes = ctk.CTkFrame(container, fg_color="transparent")
        container_detalhes.grid(row=0, column=1, sticky="nsew", padx=(10, 0), pady=0)
        
        return container, container_tabela, container_detalhes
    
    @staticmethod
    def criar_tabela(parent, on_select, on_double_click):
        return TabelaRepetidos(parent, on_select_callback=on_select, on_double_click_callback=on_double_click)
    
    @staticmethod
    def criar_detalhes(parent):
        return AreaDetalhes(parent)
    
    @staticmethod
    def criar_filtros(parent, on_filtrar, tecnicos, periodos):
        filtros = FiltrosWidget(parent, on_filtrar_callback=on_filtrar)
        filtros.carregar_tecnicos(tecnicos)
        filtros.carregar_periodos_producao(periodos)
        return filtros
    
    @staticmethod
    def criar_botoes(parent, on_exportar):
        return BotoesAcao(parent, on_exportar_callback=on_exportar)