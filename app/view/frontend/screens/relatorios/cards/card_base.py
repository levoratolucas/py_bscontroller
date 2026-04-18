import customtkinter as ctk

class CardBase:
    def __init__(self, parent, row, col, texto, icone, cor, callback=None):
        self.parent = parent
        self.row = row
        self.col = col
        self.texto = texto
        self.icone = icone
        self.cor = cor
        self.callback = callback
        
        self.frame = None
        self.label_valor = None
        self.criar_card()
    
    def criar_card(self):
        self.frame = ctk.CTkFrame(
            self.parent,
            fg_color="#1a1a2e",
            corner_radius=12,
            border_width=1,
            border_color=self.cor,
            cursor="hand2" if self.callback else ""
        )
        self.frame.grid(row=self.row, column=self.col, sticky="nsew", padx=5, pady=5)
        
        if self.callback:
            self.frame.bind("<Button-1>", lambda e: self.callback())
        
        ctk.CTkLabel(self.frame, text=self.icone, font=('Arial', 40), text_color=self.cor).pack(pady=(15, 5))
        ctk.CTkLabel(self.frame, text=self.texto, font=('Arial', 16, 'bold'), text_color="#ffffff").pack()
        self.label_valor = ctk.CTkLabel(self.frame, text="0", font=('Arial', 32, 'bold'), text_color=self.cor)
        self.label_valor.pack(pady=(5, 15))
    
    def set_valor(self, valor):
        self.label_valor.configure(text=str(valor))
    
    def destacar(self, destacado=True):
        if destacado:
            self.frame.configure(border_width=3)
        else:
            self.frame.configure(border_width=1)