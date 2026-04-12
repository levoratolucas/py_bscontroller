import customtkinter as ctk
from tkinter import ttk
from app.view.frontend.styles import COLORS, FONTS

class TabelaRelatorio:
    def __init__(self, parent):
        self.parent = parent
        self.tree = None
        self.criar_tabela()
    
    def criar_tabela(self):
        frame = ctk.CTkFrame(self.parent, fg_color=COLORS['bg_card'], corner_radius=12)
        frame.pack(fill="both", expand=True)
        
        ctk.CTkLabel(
            frame,
            text="WANs Repetidos",
            font=FONTS['subtitle'],
            text_color=COLORS['primary']
        ).pack(anchor="w", padx=15, pady=(10, 5))
        
        container = ctk.CTkFrame(frame, fg_color="transparent")
        container.pack(fill="both", expand=True, padx=10, pady=10)
        
        colunas = ("WAN/Piloto", "Total OS", "Primeira OS", "Última OS", "Dias")
        self.tree = ttk.Treeview(container, columns=colunas, show="headings", height=15)
        
        for col in colunas:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120)
        
        self.tree.pack(side="left", fill="both", expand=True)
        
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=scrollbar.set)
    
    def limpar(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
    
    def adicionar(self, valores):
        self.tree.insert("", "end", values=valores)
    
    def on_double_click(self, callback):
        self.tree.bind("<Double-1>", callback)
    
    def get_selecionado(self):
        selection = self.tree.selection()
        if selection:
            return self.tree.item(selection[0])['values']
        return None