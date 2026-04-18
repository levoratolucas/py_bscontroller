import customtkinter as ctk
from app.view.frontend.styles import COLORS, FONTS

class FiltroWidget(ctk.CTkFrame):
    def __init__(self, parent, on_filtrar=None):
        super().__init__(parent, fg_color=COLORS['bg_card'], corner_radius=12, border_width=1, border_color=COLORS['border'])
        self.on_filtrar = on_filtrar
        
        self.setup_ui()
    
    def setup_ui(self):
        self.pack(fill="x", pady=(0, 20))
        
        content = ctk.CTkFrame(self, fg_color="transparent")
        content.pack(fill="x", padx=15, pady=10)
        
        # Título
        ctk.CTkLabel(
            content,
            text="🔍 FILTRAR REPETIDOS",
            font=FONTS['subtitle'],
            text_color=COLORS['primary']
        ).pack(anchor="w", pady=(0, 10))
        
        # Linha de filtros
        row = ctk.CTkFrame(content, fg_color="transparent")
        row.pack(fill="x")
        
        # Mês
        ctk.CTkLabel(row, text="Mês:", font=FONTS['normal'], text_color=COLORS['text_secondary']).pack(side="left", padx=(0, 10))
        
        self.meses = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", 
                     "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]
        
        self.mes_combo = ctk.CTkComboBox(row, values=self.meses, width=120, state="readonly")
        self.mes_combo.pack(side="left", padx=(0, 15))
        
        # Ano
        ctk.CTkLabel(row, text="Ano:", font=FONTS['normal'], text_color=COLORS['text_secondary']).pack(side="left", padx=(0, 10))
        
        ano_atual = datetime.now().year
        anos = [str(ano_atual - 1), str(ano_atual), str(ano_atual + 1)]
        self.ano_combo = ctk.CTkComboBox(row, values=anos, width=80, state="readonly")
        self.ano_combo.pack(side="left", padx=(0, 15))
        
        # Status
        ctk.CTkLabel(row, text="Status:", font=FONTS['normal'], text_color=COLORS['text_secondary']).pack(side="left", padx=(0, 10))
        
        self.status_combo = ctk.CTkComboBox(
            row, 
            values=["Todos", "Pendente", "Procede", "Não Procede"],
            width=120,
            state="readonly"
        )
        self.status_combo.pack(side="left", padx=(0, 15))
        
        # Botão Filtrar
        self.btn_filtrar = ctk.CTkButton(
            row,
            text="🔍 Filtrar",
            fg_color=COLORS['primary'],
            width=100,
            command=self.filtrar
        )
        self.btn_filtrar.pack(side="left")
        
        # Botão Atualizar (recalcular repetidos)
        self.btn_atualizar = ctk.CTkButton(
            row,
            text="🔄 Recalcular",
            fg_color=COLORS['warning'],
            width=100,
            command=self.recalcular
        )
        self.btn_atualizar.pack(side="left", padx=(10, 0))
        
        # Data atual
        from datetime import datetime
        self.mes_combo.set(self.meses[datetime.now().month - 1])
        self.ano_combo.set(str(ano_atual))
        self.status_combo.set("Todos")
    
    def filtrar(self):
        if self.on_filtrar:
            mes_nome = self.mes_combo.get()
            mes_numero = self.meses.index(mes_nome) + 1
            ano = self.ano_combo.get()
            status = self.status_combo.get()
            
            self.on_filtrar(mes_numero, ano, status)
    
    def recalcular(self):
        if self.on_filtrar:
            from app.controller.repetido_controller import RepetidoController
            controller = RepetidoController()
            controller.atualizar_tabela_repetidos()
            messagebox.showinfo("Atualizado", "Tabela de repetidos recalculada com sucesso!")
            self.filtrar()