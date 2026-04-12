import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime, timedelta
from app.view.frontend.styles import COLORS, FONTS
from app.view.frontend.components.card_widget import CardWidget
from app.controller.relatorio_controller import RelatorioController


class RelatoriosScreen(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent, fg_color="transparent")
        self.pack(fill="both", expand=True)
        
        self.app = app
        self.relatorio_controller = RelatorioController()
        
        self.setup_ui()
        self.carregar_dados()

    def setup_ui(self):
        main_frame = ctk.CTkFrame(self, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Título
        ctk.CTkLabel(
            main_frame,
            text="Relatórios - Repetidos",
            font=FONTS['title'],
            text_color=COLORS['primary']
        ).pack(anchor="w", pady=(0, 20))

        # Cards
        cards_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        cards_frame.pack(fill="x", pady=(0, 20))
        
        for i in range(3):
            cards_frame.grid_columnconfigure(i, weight=1)
        
        # Card REPETIDO (clicável)
        self.card_repetido = CardWidget(cards_frame, "🔄 REPETIDO", "0", 0)
        self.card_repetido.set_clicavel(cor=COLORS['warning'])
        self.card_repetido.bind("<Button-1>", self.on_repetido_click)
        
        self.card_total_os = CardWidget(cards_frame, "📋 Total OS", "0", 1)
        self.card_ofensor = CardWidget(cards_frame, "⚠️ Ofensor %", "0", 2)

        # Label para mostrar o clique
        self.click_label = ctk.CTkLabel(
            main_frame,
            text="Clique no card REPETIDO para ver os detalhes",
            font=FONTS['normal'],
            text_color=COLORS['text_secondary']
        )
        self.click_label.pack(pady=10)

    def carregar_dados(self):
        hoje = datetime.now()
        primeiro_dia = datetime(hoje.year, hoje.month, 1)
        
        if hoje.month == 12:
            ultimo_dia = datetime(hoje.year + 1, 1, 1) - timedelta(days=1)
        else:
            ultimo_dia = datetime(hoje.year, hoje.month + 1, 1) - timedelta(days=1)
        
        data_inicio = primeiro_dia.strftime("%Y-%m-%d")
        data_fim = ultimo_dia.strftime("%Y-%m-%d")
        
        resumo = self.relatorio_controller.get_resumo_periodo(data_inicio, data_fim)
        
        self.card_repetido.set_valor(resumo['repeticoes'])
        self.card_total_os.set_valor(resumo['total_os'])
        self.card_ofensor.set_valor(f"{resumo['ofensor']}%")

    def on_repetido_click(self, event):
        """Ação ao clicar no card REPETIDO"""
        valor = self.card_repetido.get_valor()
        titulo = self.card_repetido.get_titulo()
        
        # Mensagem na tela
        self.click_label.configure(
            text=f"✅ CLICOU! {titulo}: {valor} repetições no mês",
            text_color=COLORS['success']
        )
        
        # Também mostra um popup
        messagebox.showinfo(
            "Card Clicado",
            f"Você clicou no card REPETIDO!\n\nTotal de repetições no mês: {valor}"
        )