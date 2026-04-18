import customtkinter as ctk
from app.view.frontend.styles import COLORS, FONTS
from app.view.frontend.screens.repetidos.widgets.card_repetido import CardRepetido

class ListaRepetidos(ctk.CTkScrollableFrame):
    def __init__(self, parent, on_status_change=None):
        super().__init__(parent, fg_color="transparent", scrollbar_fg_color=COLORS['border'])
        self.on_status_change = on_status_change
        self.cards = []
        
        self.setup_ui()
    
    def setup_ui(self):
        self.pack(fill="both", expand=True)
        
        # Label quando vazio
        self.empty_label = ctk.CTkLabel(
            self,
            text="📭 Nenhum repetido encontrado para o período selecionado",
            font=FONTS['normal'],
            text_color=COLORS['text_secondary']
        )
    
    def carregar(self, dados):
        """Carrega a lista de repetidos"""
        # Limpar cards existentes
        for card in self.cards:
            card.destroy()
        self.cards.clear()
        
        if not dados:
            self.empty_label.pack(pady=50)
            return
        
        self.empty_label.pack_forget()
        
        # Criar cards
        for item in dados:
            card = CardRepetido(self, item, on_status_change=self.on_status_change)
            self.cards.append(card)