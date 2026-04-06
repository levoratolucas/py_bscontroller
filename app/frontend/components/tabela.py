# app/frontend/components/tabela.py

import customtkinter as ctk
from app.frontend.styles import COLORS, FONTS


class TabelaInterativa(ctk.CTkFrame):
    def __init__(self, parent, headers, larguras=None, on_click=None):
        super().__init__(parent, fg_color=COLORS['bg_card'], corner_radius=12, border_width=1, border_color=COLORS['border'])
        
        self.headers = headers
        self.larguras = larguras or [100] * len(headers)
        self.on_click = on_click
        self.dados = []
        self.linhas = []
        
        # Frame com scroll
        self.scroll_frame = ctk.CTkScrollableFrame(self, fg_color="transparent", height=350)
        self.scroll_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Configurar grid
        for col, largura in enumerate(self.larguras):
            self.scroll_frame.grid_columnconfigure(col, weight=1, minsize=largura)
        
        # Criar cabeçalho
        self.criar_cabecalho()
    
    def criar_cabecalho(self):
        header_frame = ctk.CTkFrame(self.scroll_frame, fg_color=COLORS['bg_table_header'], corner_radius=0)
        header_frame.grid(row=0, column=0, columnspan=len(self.headers), sticky="ew", padx=1, pady=1)
        
        for col, header in enumerate(self.headers):
            lbl = ctk.CTkLabel(
                header_frame,
                text=header,
                font=FONTS['table_header'],
                text_color=COLORS['text_primary'],
                anchor="w"
            )
            lbl.grid(row=0, column=col, padx=10, pady=8, sticky="w")
    
    def adicionar_linha(self, valores, tag=None):
        row = len(self.dados) + 1
        bg_color = COLORS['bg_table_row_even'] if row % 2 == 0 else COLORS['bg_table_row_odd']
        
        if tag == "repetido":
            bg_color = COLORS['repetido_even'] if row % 2 == 0 else COLORS['repetido_odd']
        
        linha_cells = []
        
        for col, (val, largura) in enumerate(zip(valores, self.larguras)):
            cell_frame = ctk.CTkFrame(self.scroll_frame, fg_color=bg_color, corner_radius=0)
            cell_frame.grid(row=row, column=col, padx=1, pady=1, sticky="nsew")
            
            lbl = ctk.CTkLabel(
                cell_frame,
                text=str(val),
                font=FONTS['table_cell'],
                text_color=COLORS['text_primary'],
                anchor="w",
                wraplength=largura - 20
            )
            lbl.pack(padx=10, pady=6, fill="both", expand=True)
            
            if self.on_click:
                def on_enter(e, cf=cell_frame):
                    cf.configure(fg_color=COLORS['bg_table_hover'])
                    for lc in linha_cells:
                        lc.configure(fg_color=COLORS['bg_table_hover'])
                
                def on_leave(e, cf=cell_frame, cor=bg_color):
                    cf.configure(fg_color=cor)
                    for lc in linha_cells:
                        lc.configure(fg_color=cor)
                
                def on_click_cell(e, r=row-1):
                    self.on_click(r)
                
                cell_frame.bind("<Enter>", on_enter)
                cell_frame.bind("<Leave>", on_leave)
                cell_frame.bind("<Button-1>", on_click_cell)
                lbl.bind("<Enter>", on_enter)
                lbl.bind("<Leave>", on_leave)
                lbl.bind("<Button-1>", on_click_cell)
                
                cell_frame.configure(cursor="hand2")
                lbl.configure(cursor="hand2")
            
            linha_cells.append(cell_frame)
        
        self.dados.append(valores)
        self.linhas.append(linha_cells)
    
    def carregar_dados(self, dados, tags=None):
        self.limpar()
        for i, valores in enumerate(dados):
            tag = tags[i] if tags and i < len(tags) else None
            self.adicionar_linha(valores, tag)
    
    def limpar(self):
        for widget in self.scroll_frame.winfo_children():
            row = widget.grid_info().get('row', 0)
            if row > 0:
                widget.destroy()
        # Recriar cabeçalho
        self.criar_cabecalho()
        self.dados = []
        self.linhas = []
    
    def get_dado(self, index):
        if 0 <= index < len(self.dados):
            return self.dados[index]
        return None