import customtkinter as ctk
from app.view.frontend.styles import COLORS, FONTS

class CardWidget(ctk.CTkFrame):
    def __init__(self, parent, titulo, valor="0", col=0, **kwargs):
        super().__init__(parent, fg_color=COLORS['bg_card'], corner_radius=12, **kwargs)
        self.grid(row=0, column=col, sticky="nsew", padx=5, pady=5)
        
        self.titulo = titulo
        self.valor = valor
        
        self.label_titulo = ctk.CTkLabel(self, text=titulo, font=FONTS['small'], 
                                          text_color=COLORS['text_secondary'])
        self.label_titulo.pack(anchor="w", padx=15, pady=(10, 0))
        
        self.label_valor = ctk.CTkLabel(self, text=str(valor), font=('Arial', 28, 'bold'), 
                                         text_color=COLORS['primary'])
        self.label_valor.pack(anchor="w", padx=15, pady=(5, 10))
    
    def set_valor(self, valor):
        self.valor = valor
        self.label_valor.configure(text=str(valor))
    
    def set_clicavel(self, cor=None):
        """Torna o card clicável com cursor de mão"""
        self.configure(cursor="hand2")
        if cor:
            self.label_valor.configure(text_color=cor)
            self.label_titulo.configure(text_color=cor)
    
    def get_valor(self):
        return self.valor
    
    def get_titulo(self):
        return self.titulo