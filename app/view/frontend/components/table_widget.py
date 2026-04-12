import customtkinter as ctk
from tkinter import ttk
from app.view.frontend.styles import COLORS, FONTS

class TableWidget(ctk.CTkFrame):
    def __init__(self, parent, titulo, colunas, height=15, **kwargs):
        super().__init__(parent, fg_color=COLORS['bg_card'], corner_radius=12, **kwargs)
        self.pack(fill="both", expand=True)
        
        ctk.CTkLabel(self, text=titulo, font=FONTS['subtitle'], 
                     text_color=COLORS['primary']).pack(anchor="w", padx=15, pady=(10, 5))
        
        container = ctk.CTkFrame(self, fg_color="transparent")
        container.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.tree = ttk.Treeview(container, columns=colunas, show="headings", height=height)
        
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
    
    def inserir(self, valores):
        self.tree.insert("", "end", values=valores)
    
    def on_double_click(self, callback):
        self.tree.bind("<Double-1>", callback)
    
    def get_selecionado(self):
        selection = self.tree.selection()
        if selection:
            return self.tree.item(selection[0])['values']
        return None