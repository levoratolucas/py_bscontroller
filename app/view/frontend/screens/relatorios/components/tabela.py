import customtkinter as ctk
from tkinter import ttk
from app.view.frontend.styles import COLORS, FONTS

class TabelaRepetidos:
    def __init__(self, parent, on_select_callback=None, on_double_click_callback=None):
        """
        Componente de tabela para listar repetidos
        
        Parâmetros:
            parent: widget pai
            on_select_callback: função chamada ao selecionar uma linha
            on_double_click_callback: função chamada ao dar duplo clique
        """
        self.parent = parent
        self.on_select_callback = on_select_callback
        self.on_double_click_callback = on_double_click_callback
        self.tree = None
        self.dados = []
        
        self.criar_tabela()
    
    def criar_tabela(self):
        """Cria a estrutura da tabela"""
        # Frame wrapper
        self.wrapper = ctk.CTkFrame(self.parent, fg_color="#0f0f0f", corner_radius=12, 
                                     border_width=1, border_color="#2a2a2a")
        self.wrapper.pack(fill="both", expand=True)
        
        # Título
        self.titulo_label = ctk.CTkLabel(
            self.wrapper,
            text="📋 Histórico de Repetições",
            font=('Arial', 12, 'bold'),
            text_color="#00ff88"
        )
        self.titulo_label.pack(anchor="w", padx=15, pady=(10, 5))
        
        # Container da tabela
        container = ctk.CTkFrame(self.wrapper, fg_color="transparent")
        container.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Colunas
        columns = ("Nº OS", "WAN/Piloto", "Técnico", "Data", "Início", "Fim", "Status", "Observação")
        
        # Treeview
        self.tree = ttk.Treeview(container, columns=columns, show="headings", height=18, style="Custom.Treeview")
        
        # Estilos
        style = ttk.Style()
        style.theme_use("clam")
        
        style.configure("Custom.Treeview.Heading",
                        background="#1a1a2e",
                        foreground="#00ff88",
                        font=('Arial', 10, 'bold'),
                        borderwidth=0)
        
        style.configure("Custom.Treeview",
                        background="#0f0f0f",
                        foreground="#cccccc",
                        fieldbackground="#0f0f0f",
                        rowheight=28,
                        borderwidth=0,
                        font=('Arial', 10))
        
        style.map("Custom.Treeview",
                  background=[('selected', '#ff6b00')],
                  foreground=[('selected', '#ffffff')])
        
        # Configurar colunas
        for col in columns:
            self.tree.heading(col, text=col)
            if col == "WAN/Piloto":
                self.tree.column(col, width=110)
            elif col == "Técnico":
                self.tree.column(col, width=140)
            elif col == "Observação":
                self.tree.column(col, width=100)
            else:
                self.tree.column(col, width=80)
        
        self.tree.pack(side="left", fill="both", expand=True)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Binds
        self.tree.bind("<<TreeviewSelect>>", self._on_select)
        self.tree.bind("<Double-1>", self._on_double_click)
    
    def _on_select(self, event):
        """Callback ao selecionar uma linha"""
        if self.on_select_callback:
            selection = self.tree.selection()
            if selection:
                item_id = selection[0]
                valores = self.tree.item(item_id, 'values')
                if valores:
                    self.on_select_callback(valores)
    
    def _on_double_click(self, event):
        """Callback ao dar duplo clique"""
        if self.on_double_click_callback:
            selection = self.tree.selection()
            if selection:
                item_id = selection[0]
                valores = self.tree.item(item_id, 'values')
                if valores:
                    self.on_double_click_callback(valores)
    
    def set_titulo(self, texto):
        """Altera o título da tabela"""
        self.titulo_label.configure(text=texto)
    
    def limpar(self):
        """Limpa todos os itens da tabela"""
        for item in self.tree.get_children():
            self.tree.delete(item)
    
    def adicionar(self, valores, tag='even'):
        """Adiciona uma linha na tabela"""
        self.tree.insert("", "end", values=valores, tags=(tag,))
    
    def carregar(self, dados, alternar_cores=True):
        """
        Carrega uma lista de dados na tabela
        
        Parâmetros:
            dados: lista de dicionários com as chaves:
                - numero, wan_piloto, tecnico, data, inicio_execucao, 
                  fim_execucao, status_nome, observacao
            alternar_cores: se True, alterna cores das linhas
        """
        self.limpar()
        
        for i, item in enumerate(dados):
            tag = 'even' if i % 2 == 0 else 'odd' if alternar_cores else ''
            
            self.tree.insert("", "end", values=(
                item.get('numero', '-'),
                item.get('wan_piloto', '-'),
                item.get('tecnico', '-'),
                item.get('data', '-'),
                item.get('inicio_execucao', '-'),
                item.get('fim_execucao', '-'),
                item.get('status_nome', '-'),
                item.get('observacao', '-')
            ), tags=(tag,))
        
        # Configurar cores das linhas
        self.tree.tag_configure('even', background='#0f0f0f')
        self.tree.tag_configure('odd', background='#1a1a2e')
    
    def get_selecionado(self):
        """Retorna o valor da linha selecionada"""
        selection = self.tree.selection()
        if selection:
            return self.tree.item(selection[0], 'values')
        return None
    
    def get_frame(self):
        """Retorna o frame wrapper da tabela"""
        return self.wrapper