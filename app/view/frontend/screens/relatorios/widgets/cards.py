import customtkinter as ctk
from app.view.frontend.styles import COLORS, FONTS
from app.view.frontend.components.card_widget import CardWidget

class CardsRelatorio:
    def __init__(self, parent):
        self.parent = parent
        self.cards = {}
        self.criar_cards()
    
    def criar_cards(self):
        cards_frame = ctk.CTkFrame(self.parent, fg_color="transparent")
        cards_frame.pack(fill="x", pady=(0, 20))
        
        for i in range(3):
            cards_frame.grid_columnconfigure(i, weight=1)
        
        # Card REPETIDO (clicável)
        self.cards['repetido'] = CardWidget(cards_frame, "🔄 REPETIDO", "0", 0)
        
        self.cards['total_os'] = CardWidget(cards_frame, "📋 Total OS", "0", 1)
        self.cards['ofensor'] = CardWidget(cards_frame, "⚠️ Ofensor %", "0", 2)
    
    def get_card(self, nome):
        return self.cards.get(nome)
    
    def atualizar(self, repetidos, total_os, ofensor):
        self.cards['repetido'].set_valor(repetidos)
        self.cards['total_os'].set_valor(total_os)
        self.cards['ofensor'].set_valor(f"{ofensor}%")