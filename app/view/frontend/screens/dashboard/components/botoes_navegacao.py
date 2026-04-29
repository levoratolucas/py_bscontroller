import customtkinter as ctk
from app.view.frontend.styles import COLORS, FONTS

class BotoesNavegacao:
    def __init__(self, parent, callbacks):
        self.parent = parent
        self.callbacks = callbacks
        self.botoes = []
        self.criar_botoes()
    
    def criar_botoes(self):
        for i, (titulo, desc, comando) in enumerate(self.callbacks):
            if i < 3:
                self.botoes.append(self._criar_botao(titulo, desc, comando, i))
    
    def _criar_botao(self, titulo, desc, comando, col):
        card = ctk.CTkFrame(self.parent, fg_color=COLORS['bg_card'], corner_radius=12, 
                             border_width=1, border_color=COLORS['border'])
        card.grid(row=0, column=col, sticky="nsew", padx=5, pady=5)
        
        ctk.CTkLabel(card, text=titulo, font=FONTS['subtitle'], text_color=COLORS['primary']).pack(anchor="w", padx=15, pady=(10, 0))
        ctk.CTkLabel(card, text=desc, font=FONTS['small'], text_color=COLORS['text_secondary']).pack(anchor="w", padx=15, pady=(0, 5))
        ctk.CTkButton(card, text="Acessar →", fg_color="transparent", text_color=COLORS['primary'], command=comando).pack(fill="x", padx=15, pady=(0, 10))
        
        return card
    
    def get_botoes(self):
        return self.botoes