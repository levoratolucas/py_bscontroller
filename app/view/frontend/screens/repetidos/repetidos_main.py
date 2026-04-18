import customtkinter as ctk
from tkinter import ttk, messagebox
from datetime import datetime
from app.view.frontend.styles import COLORS, FONTS
from app.controller.repetido_controller import RepetidoController

class RepetidosScreen(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent, fg_color=COLORS['bg_dark'])
        self.app = app
        self.repetido_controller = RepetidoController()
        self.dados_atuais = []
        
        self.setup_ui()
        self.carregar_dados()
    
    def setup_ui(self):
        # Container principal
        main_frame = ctk.CTkFrame(self, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Título
        titulo_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        titulo_frame.pack(fill="x", pady=(0, 20))
        
        ctk.CTkLabel(
            titulo_frame,
            text="🔁 REPETIDOS",
            font=FONTS['title'],
            text_color=COLORS['primary']
        ).pack(anchor="w")
        
        ctk.CTkLabel(
            titulo_frame,
            text="WANs/Pilotos que repetiram dentro de 30 dias",
            font=FONTS['small'],
            text_color=COLORS['text_secondary']
        ).pack(anchor="w")
        
        # ================= FILTRO =================
        filtro_frame = ctk.CTkFrame(main_frame, fg_color=COLORS['bg_card'], corner_radius=12)
        filtro_frame.pack(fill="x", pady=(0, 20))
        
        filtro_content = ctk.CTkFrame(filtro_frame, fg_color="transparent")
        filtro_content.pack(fill="x", padx=15, pady=10)
        
        # Linha de filtros
        row = ctk.CTkFrame(filtro_content, fg_color="transparent")
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
        
        # Data atual nos combos
        self.mes_combo.set(self.meses[datetime.now().month - 1])
        self.ano_combo.set(str(ano_atual))
        
        # ================= TABELA =================
        table_frame = ctk.CTkFrame(main_frame, fg_color=COLORS['bg_card'], corner_radius=12)
        table_frame.pack(fill="both", expand=True)
        
        ctk.CTkLabel(
            table_frame,
            text="📋 LISTA DE REPETIDOS",
            font=FONTS['subtitle'],
            text_color=COLORS['primary']
        ).pack(anchor="w", padx=15, pady=(10, 5))
        
        # Container da tabela
        table_container = ctk.CTkFrame(table_frame, fg_color="transparent")
        table_container.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Treeview
        columns = ("ID", "Nº OS", "WAN/Piloto", "Técnico", "Data", "Status", "OS Referência", "Diferença (dias)")
        
        self.tree = ttk.Treeview(table_container, columns=columns, show="headings", height=15, style="Custom.Treeview")
        
        # Configurar estilo
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Custom.Treeview.Heading",
                        background=COLORS['bg_card'],
                        foreground=COLORS['primary'],
                        font=('Arial', 10, 'bold'))
        style.configure("Custom.Treeview",
                        background=COLORS['bg_dark'],
                        foreground=COLORS['text_light'],
                        fieldbackground=COLORS['bg_dark'],
                        rowheight=28)
        style.map("Custom.Treeview",
                  background=[('selected', COLORS['primary'])])
        
        # Configurar colunas
        for col in columns:
            self.tree.heading(col, text=col)
        
        self.tree.column("ID", width=40)
        self.tree.column("Nº OS", width=100)
        self.tree.column("WAN/Piloto", width=150)
        self.tree.column("Técnico", width=150)
        self.tree.column("Data", width=100)
        self.tree.column("Status", width=100)
        self.tree.column("OS Referência", width=100)
        self.tree.column("Diferença (dias)", width=100)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(table_container, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def carregar_dados(self, mes=None, ano=None):
        """Carrega os dados dos repetidos"""
        if mes is None:
            mes = datetime.now().month
        if ano is None:
            ano = datetime.now().year
        
        mes_str = f"{ano}-{str(mes).zfill(2)}"
        
        # Buscar repetidos do mês
        dados = self.repetido_controller.get_repetidos_com_detalhes(mes_str)
        
        # Limpar tabela
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Preencher tabela
        for item in dados:
            # Calcular dias de diferença
            dias = "-"
            try:
                data_ref = datetime.strptime(item['data_referencia'], "%Y-%m-%d")
                data_rep = datetime.strptime(item['data_repetido'], "%Y-%m-%d")
                dias = (data_rep - data_ref).days
            except:
                pass
            
            # Status
            status_map = {0: "Pendente", 1: "Procede", 2: "Não Procede"}
            status = status_map.get(item['procedente'], "Desconhecido")
            
            # Inserir na tabela
            self.tree.insert("", "end", values=(
                item['id'],
                item['numero_repetido'],
                item['wan_piloto'],
                item['tecnico_repetido'],
                item['data_repetido'],
                status,
                item['numero_referencia'],
                dias
            ))
        
        # Atualizar contador
        total = len(dados)
        self.titulo_count = ctk.CTkLabel(
            self,
            text=f"Total de repetidos: {total}",
            font=FONTS['small'],
            text_color=COLORS['text_secondary']
        )
        
        print(f"✅ {total} repetidos encontrados para {mes_str}")
    
    def filtrar(self):
        """Aplica o filtro selecionado"""
        mes_nome = self.mes_combo.get()
        mes_numero = self.meses.index(mes_nome) + 1
        ano = int(self.ano_combo.get())
        
        self.carregar_dados(mes_numero, ano)
    
    def recalcular(self):
        """Recalcula a tabela de repetidos"""
        if messagebox.askyesno("Recalcular", "Deseja recalcular todos os repetidos? Isso pode levar alguns segundos."):
            self.repetido_controller.atualizar_tabela_repetidos()
            messagebox.showinfo("Atualizado", "Tabela de repetidos recalculada com sucesso!")
            self.filtrar()