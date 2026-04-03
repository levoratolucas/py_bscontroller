import tkinter as tk
from tkinter import ttk, messagebox
from app.controller.ordem_servico_controller import OrdemServicoController
from app.controller.tecnico_controller import TecnicoController
from app.controller.produto_controller import ProdutoController
from app.controller.cliente_controller import ClienteController
from app.controller.endereco_controller import EnderecoController
from app.bd.cliente_endereco_repository import ClienteEnderecoRepository
from app.model.cliente_endereco import ClienteEndereco
from app.view.gui.styles import COLORS, FONTS
from datetime import datetime

class OSFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        
        # Controllers
        self.os_controller = OrdemServicoController()
        self.tecnico_controller = TecnicoController()
        self.produto_controller = ProdutoController()
        self.cliente_controller = ClienteController()
        self.endereco_controller = EnderecoController()
        self.cliente_endereco_repo = ClienteEnderecoRepository()
        
        # Variáveis para armazenar IDs selecionados
        self.id_tecnico_selecionado = None
        self.id_cliente_selecionado = None
        self.id_endereco_selecionado = None
        self.id_produto_selecionado = None
        self.id_relacionamento_selecionado = None
        
        self.criar_widgets()
        self.listar_ordens()
        self.carregar_combos()
    
    def criar_widgets(self):
        # ==================== PAINEL DE BUSCA RÁPIDA ====================
        busca_frame = ttk.LabelFrame(self, text="🔍 Busca Rápida por WAN/Piloto", padding=10)
        busca_frame.pack(fill=tk.X, padx=10, pady=5)
        
        busca_row = ttk.Frame(busca_frame)
        busca_row.pack(fill=tk.X)
        
        ttk.Label(busca_row, text="WAN/Piloto:", font=FONTS['subtitle']).pack(side=tk.LEFT, padx=(0, 10))
        self.busca_wan_entry = ttk.Entry(busca_row, width=30, font=FONTS['normal'])
        self.busca_wan_entry.pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(busca_row, text="🔎 Buscar", command=self.buscar_por_wan).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(busca_row, text="🗑️ Limpar Busca", command=self.limpar_busca).pack(side=tk.LEFT)
        
        # ==================== PAINEL DO CLIENTE ====================
        cliente_frame = ttk.LabelFrame(self, text="👤 CLIENTE", padding=10)
        cliente_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Selecionar ou cadastrar
        cliente_row1 = ttk.Frame(cliente_frame)
        cliente_row1.pack(fill=tk.X, pady=5)
        
        ttk.Label(cliente_row1, text="Selecionar existente:", font=FONTS['normal']).pack(side=tk.LEFT, padx=(0, 10))
        self.cliente_combo = ttk.Combobox(cliente_row1, width=40, font=FONTS['normal'])
        self.cliente_combo.pack(side=tk.LEFT, padx=(0, 10))
        self.cliente_combo.bind("<<ComboboxSelected>>", self.on_cliente_selecionado)
        
        ttk.Button(cliente_row1, text="➕ Novo Cliente", command=self.abrir_cadastro_cliente).pack(side=tk.LEFT)
        
        # Dados do cliente (auto preenchidos)
        cliente_row2 = ttk.Frame(cliente_frame)
        cliente_row2.pack(fill=tk.X, pady=5)
        
        ttk.Label(cliente_row2, text="Cliente:", font=FONTS['subtitle']).pack(side=tk.LEFT, padx=(0, 10))
        self.cliente_nome_label = ttk.Label(cliente_row2, text="-", font=FONTS['normal'], foreground=COLORS['primary'])
        self.cliente_nome_label.pack(side=tk.LEFT)
        
        # ==================== PAINEL DO ENDEREÇO ====================
        endereco_frame = ttk.LabelFrame(self, text="📍 ENDEREÇO", padding=10)
        endereco_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Selecionar ou cadastrar
        endereco_row1 = ttk.Frame(endereco_frame)
        endereco_row1.pack(fill=tk.X, pady=5)
        
        ttk.Label(endereco_row1, text="Selecionar existente:", font=FONTS['normal']).pack(side=tk.LEFT, padx=(0, 10))
        self.endereco_combo = ttk.Combobox(endereco_row1, width=50, font=FONTS['normal'])
        self.endereco_combo.pack(side=tk.LEFT, padx=(0, 10))
        self.endereco_combo.bind("<<ComboboxSelected>>", self.on_endereco_selecionado)
        
        ttk.Button(endereco_row1, text="➕ Novo Endereço", command=self.abrir_cadastro_endereco).pack(side=tk.LEFT)
        
        # Dados do endereço
        endereco_row2 = ttk.Frame(endereco_frame)
        endereco_row2.pack(fill=tk.X, pady=5)
        
        ttk.Label(endereco_row2, text="Endereço:", font=FONTS['subtitle']).pack(side=tk.LEFT, padx=(0, 10))
        self.endereco_texto_label = ttk.Label(endereco_row2, text="-", font=FONTS['normal'], foreground=COLORS['primary'])
        self.endereco_texto_label.pack(side=tk.LEFT)
        
        # ==================== PAINEL DO PRODUTO ====================
        produto_frame = ttk.LabelFrame(self, text="📦 PRODUTO", padding=10)
        produto_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Selecionar ou cadastrar
        produto_row1 = ttk.Frame(produto_frame)
        produto_row1.pack(fill=tk.X, pady=5)
        
        ttk.Label(produto_row1, text="Selecionar existente:", font=FONTS['normal']).pack(side=tk.LEFT, padx=(0, 10))
        self.produto_combo = ttk.Combobox(produto_row1, width=50, font=FONTS['normal'])
        self.produto_combo.pack(side=tk.LEFT, padx=(0, 10))
        self.produto_combo.bind("<<ComboboxSelected>>", self.on_produto_selecionado)
        
        ttk.Button(produto_row1, text="➕ Novo Produto", command=self.abrir_cadastro_produto).pack(side=tk.LEFT)
        
        # Dados do produto
        produto_row2 = ttk.Frame(produto_frame)
        produto_row2.pack(fill=tk.X, pady=5)
        
        ttk.Label(produto_row2, text="Descrição:", font=FONTS['subtitle']).pack(side=tk.LEFT, padx=(0, 10))
        self.produto_desc_label = ttk.Label(produto_row2, text="-", font=FONTS['normal'], foreground=COLORS['primary'])
        self.produto_desc_label.pack(side=tk.LEFT, padx=(0, 20))
        
        ttk.Label(produto_row2, text="Designador:", font=FONTS['subtitle']).pack(side=tk.LEFT, padx=(0, 10))
        self.produto_designador_label = ttk.Label(produto_row2, text="-", font=FONTS['normal'], foreground=COLORS['primary'])
        self.produto_designador_label.pack(side=tk.LEFT, padx=(0, 20))
        
        ttk.Label(produto_row2, text="WAN/Piloto:", font=FONTS['subtitle']).pack(side=tk.LEFT, padx=(0, 10))
        self.produto_wan_label = ttk.Label(produto_row2, text="-", font=FONTS['normal'], foreground=COLORS['primary'])
        self.produto_wan_label.pack(side=tk.LEFT)
        
        # ==================== PAINEL DO TÉCNICO ====================
        tecnico_frame = ttk.LabelFrame(self, text="🔧 TÉCNICO RESPONSÁVEL", padding=10)
        tecnico_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tecnico_row1 = ttk.Frame(tecnico_frame)
        tecnico_row1.pack(fill=tk.X, pady=5)
        
        ttk.Label(tecnico_row1, text="Selecionar existente:", font=FONTS['normal']).pack(side=tk.LEFT, padx=(0, 10))
        self.tecnico_combo = ttk.Combobox(tecnico_row1, width=40, font=FONTS['normal'])
        self.tecnico_combo.pack(side=tk.LEFT, padx=(0, 10))
        self.tecnico_combo.bind("<<ComboboxSelected>>", self.on_tecnico_selecionado)
        
        ttk.Button(tecnico_row1, text="➕ Novo Técnico", command=self.abrir_cadastro_tecnico).pack(side=tk.LEFT)
        
        # Dados do técnico
        tecnico_row2 = ttk.Frame(tecnico_frame)
        tecnico_row2.pack(fill=tk.X, pady=5)
        
        ttk.Label(tecnico_row2, text="Técnico:", font=FONTS['subtitle']).pack(side=tk.LEFT, padx=(0, 10))
        self.tecnico_nome_label = ttk.Label(tecnico_row2, text="-", font=FONTS['normal'], foreground=COLORS['primary'])
        self.tecnico_nome_label.pack(side=tk.LEFT, padx=(0, 20))
        
        ttk.Label(tecnico_row2, text="Matrícula:", font=FONTS['subtitle']).pack(side=tk.LEFT, padx=(0, 10))
        self.tecnico_matricula_label = ttk.Label(tecnico_row2, text="-", font=FONTS['normal'], foreground=COLORS['primary'])
        self.tecnico_matricula_label.pack(side=tk.LEFT)
        
        # ==================== PAINEL DA ORDEM DE SERVIÇO ====================
        dados_frame = ttk.LabelFrame(self, text="📝 DADOS DA ORDEM DE SERVIÇO", padding=10)
        dados_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Causa Raiz
        ttk.Label(dados_frame, text="Causa Raiz:*", font=FONTS['subtitle']).grid(row=0, column=0, sticky=tk.W, pady=5)
        self.causa_entry = ttk.Entry(dados_frame, width=80, font=FONTS['normal'])
        self.causa_entry.grid(row=0, column=1, padx=(10, 0), pady=5)
        
        # Materiais Utilizados
        ttk.Label(dados_frame, text="Materiais Utilizados:", font=FONTS['subtitle']).grid(row=1, column=0, sticky=tk.W, pady=5)
        self.materiais_entry = ttk.Entry(dados_frame, width=80, font=FONTS['normal'])
        self.materiais_entry.grid(row=1, column=1, padx=(10, 0), pady=5)
        
        # Ação Realizada
        ttk.Label(dados_frame, text="Ação Realizada:", font=FONTS['subtitle']).grid(row=2, column=0, sticky=tk.W, pady=5)
        self.acao_entry = ttk.Entry(dados_frame, width=80, font=FONTS['normal'])
        self.acao_entry.grid(row=2, column=1, padx=(10, 0), pady=5)
        
        # Contato Responsável
        ttk.Label(dados_frame, text="Contato Responsável:", font=FONTS['subtitle']).grid(row=3, column=0, sticky=tk.W, pady=5)
        self.contato_entry = ttk.Entry(dados_frame, width=80, font=FONTS['normal'])
        self.contato_entry.grid(row=3, column=1, padx=(10, 0), pady=5)
        
        # Observações
        ttk.Label(dados_frame, text="Observações:", font=FONTS['subtitle']).grid(row=4, column=0, sticky=tk.W, pady=5)
        self.obs_text = tk.Text(dados_frame, width=70, height=4, font=FONTS['normal'])
        self.obs_text.grid(row=4, column=1, padx=(10, 0), pady=5)
        
        # Status
        status_frame = ttk.Frame(dados_frame)
        status_frame.grid(row=5, column=0, columnspan=2, pady=10)
        
        ttk.Label(status_frame, text="Status:", font=FONTS['subtitle']).pack(side=tk.LEFT, padx=(0, 10))
        self.status_var = tk.StringVar(value="1")
        ttk.Radiobutton(status_frame, text="🟡 Em andamento", variable=self.status_var, value="1").pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(status_frame, text="✅ Concluída", variable=self.status_var, value="2").pack(side=tk.LEFT, padx=5)
        
        # Botões de ação
        botoes_frame = ttk.Frame(dados_frame)
        botoes_frame.grid(row=6, column=0, columnspan=2, pady=15)
        
        ttk.Button(botoes_frame, text="💾 Criar Ordem de Serviço", command=self.criar_os, width=25).pack(side=tk.LEFT, padx=5)
        ttk.Button(botoes_frame, text="🗑️ Limpar Formulário", command=self.limpar_formulario, width=20).pack(side=tk.LEFT, padx=5)
        
        # ==================== LISTA DE ORDENS ====================
        lista_frame = ttk.LabelFrame(self, text="📋 ORDENS DE SERVIÇO", padding=10)
        lista_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Treeview
        columns = ("ID", "Técnico", "Cliente", "Produto", "WAN/Piloto", "Status", "Data Abertura")
        self.tree = ttk.Treeview(lista_frame, columns=columns, show="headings", height=10)
        
        for col in columns:
            self.tree.heading(col, text=col)
        
        self.tree.column("ID", width=50)
        self.tree.column("Técnico", width=120)
        self.tree.column("Cliente", width=150)
        self.tree.column("Produto", width=150)
        self.tree.column("WAN/Piloto", width=120)
        self.tree.column("Status", width=100)
        self.tree.column("Data Abertura", width=130)
        
        scrollbar = ttk.Scrollbar(lista_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Botão concluir
        btn_frame = ttk.Frame(lista_frame)
        btn_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(btn_frame, text="✅ Concluir OS Selecionada", command=self.concluir_os_selecionada).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="🔄 Atualizar Lista", command=self.listar_ordens).pack(side=tk.LEFT, padx=5)
    
    # ==================== MÉTODOS DE CARREGAMENTO ====================
    
    def carregar_combos(self):
        """Carregar todos os comboboxes"""
        self.carregar_tecnicos()
        self.carregar_clientes()
        self.carregar_produtos()
    
    def carregar_tecnicos(self):
        tecnicos = self.tecnico_controller.listar_tecnicos()
        self.tecnico_combo['values'] = [f"{t.id} - {t.nome}" for t in tecnicos]
    
    def carregar_clientes(self):
        clientes = self.cliente_controller.listar_clientes()
        self.cliente_combo['values'] = [f"{c.id_cliente} - {c.nome}" for c in clientes]
    
    def carregar_enderecos(self, id_cliente=None):
        """Carregar endereços baseado no cliente selecionado"""
        if id_cliente:
            relacionamentos = self.cliente_endereco_repo.buscar_por_cliente(id_cliente)
            enderecos = self.endereco_controller.listar_enderecos()
            enderecos_dict = {e.id_endereco: e for e in enderecos}
            
            valores = []
            for rel in relacionamentos:
                end = enderecos_dict.get(rel.id_endereco)
                if end:
                    valores.append(f"{rel.id} - {end.logradouro}, {end.cidade}/{end.estado}")
            self.endereco_combo['values'] = valores
        else:
            self.endereco_combo['values'] = []
        
        self.endereco_combo.set('')
    
    def carregar_produtos(self, id_cliente=None, id_endereco=None):
        """Carregar produtos baseado no cliente e endereço"""
        if id_cliente and id_endereco:
            # Buscar relacionamento
            relacionamentos = self.cliente_endereco_repo.listar()
            id_rel = None
            for rel in relacionamentos:
                if rel.id_cliente == id_cliente and rel.id_endereco == id_endereco:
                    id_rel = rel.id
                    break
            
            if id_rel:
                produtos = self.produto_controller.listar_produtos()
                valores = [f"{p.id_produto} - {p.descricao}" for p in produtos if p.id_cliente_endereco == id_rel]
                self.produto_combo['values'] = valores
            else:
                self.produto_combo['values'] = []
        else:
            # Mostrar todos os produtos
            produtos = self.produto_controller.listar_produtos()
            self.produto_combo['values'] = [f"{p.id_produto} - {p.descricao}" for p in produtos]
        
        self.produto_combo.set('')
    
    # ==================== EVENTOS DE SELEÇÃO ====================
    
    def on_cliente_selecionado(self, event):
        """Quando um cliente é selecionado"""
        if self.cliente_combo.get():
            self.id_cliente_selecionado = int(self.cliente_combo.get().split(" - ")[0])
            
            # Buscar dados do cliente
            clientes = self.cliente_controller.listar_clientes()
            for c in clientes:
                if c.id_cliente == self.id_cliente_selecionado:
                    self.cliente_nome_label.config(text=c.nome)
                    break
            
            # Carregar endereços deste cliente
            self.carregar_enderecos(self.id_cliente_selecionado)
    
    def on_endereco_selecionado(self, event):
        """Quando um endereço é selecionado"""
        if self.endereco_combo.get():
            self.id_relacionamento_selecionado = int(self.endereco_combo.get().split(" - ")[0])
            
            # Buscar endereço
            relacionamentos = self.cliente_endereco_repo.listar()
            enderecos = self.endereco_controller.listar_enderecos()
            enderecos_dict = {e.id_endereco: e for e in enderecos}
            
            for rel in relacionamentos:
                if rel.id == self.id_relacionamento_selecionado:
                    self.id_endereco_selecionado = rel.id_endereco
                    end = enderecos_dict.get(rel.id_endereco)
                    if end:
                        self.endereco_texto_label.config(text=f"{end.logradouro}, {end.cidade}/{end.estado}")
                    break
            
            # Carregar produtos
            self.carregar_produtos(self.id_cliente_selecionado, self.id_endereco_selecionado)
    
    def on_produto_selecionado(self, event):
        """Quando um produto é selecionado"""
        if self.produto_combo.get():
            self.id_produto_selecionado = int(self.produto_combo.get().split(" - ")[0])
            
            # Buscar dados do produto
            produtos = self.produto_controller.listar_produtos()
            for p in produtos:
                if p.id_produto == self.id_produto_selecionado:
                    self.produto_desc_label.config(text=p.descricao)
                    self.produto_designador_label.config(text=p.designador)
                    self.produto_wan_label.config(text=p.wan_piloto)
                    break
    
    def on_tecnico_selecionado(self, event):
        """Quando um técnico é selecionado"""
        if self.tecnico_combo.get():
            self.id_tecnico_selecionado = int(self.tecnico_combo.get().split(" - ")[0])
            
            # Buscar dados do técnico
            tecnicos = self.tecnico_controller.listar_tecnicos()
            for t in tecnicos:
                if t.id == self.id_tecnico_selecionado:
                    self.tecnico_nome_label.config(text=t.nome)
                    self.tecnico_matricula_label.config(text=t.matricula)
                    break
    
    # ==================== BUSCA POR WAN/PILOTO ====================
    
    def buscar_por_wan(self):
        """Buscar produto por WAN/Piloto e preencher tudo automaticamente"""
        wan = self.busca_wan_entry.get().strip()
        
        if not wan:
            messagebox.showwarning("Aviso", "Digite o WAN/Piloto para buscar!")
            return
        
        # Buscar produto
        produtos = self.produto_controller.listar_produtos()
        produto_encontrado = None
        
        for p in produtos:
            if p.wan_piloto and p.wan_piloto.lower() == wan.lower():
                produto_encontrado = p
                break
        
        if not produto_encontrado:
            messagebox.showwarning("Não Encontrado", f"Produto com WAN/Piloto '{wan}' não encontrado!")
            return
        
        # Buscar relacionamento
        relacionamentos = self.cliente_endereco_repo.listar()
        rel_encontrado = None
        
        for rel in relacionamentos:
            if rel.id == produto_encontrado.id_cliente_endereco:
                rel_encontrado = rel
                break
        
        if not rel_encontrado:
            messagebox.showerror("Erro", "Produto não está vinculado a nenhum cliente/endereço!")
            return
        
        # Preencher cliente
        clientes = self.cliente_controller.listar_clientes()
        for c in clientes:
            if c.id_cliente == rel_encontrado.id_cliente:
                self.id_cliente_selecionado = c.id_cliente
                self.cliente_nome_label.config(text=c.nome)
                # Selecionar no combo
                self.cliente_combo.set(f"{c.id_cliente} - {c.nome}")
                break
        
        # Preencher endereço
        enderecos = self.endereco_controller.listar_enderecos()
        for e in enderecos:
            if e.id_endereco == rel_encontrado.id_endereco:
                self.id_endereco_selecionado = e.id_endereco
                self.id_relacionamento_selecionado = rel_encontrado.id
                self.endereco_texto_label.config(text=f"{e.logradouro}, {e.cidade}/{e.estado}")
                # Selecionar no combo
                self.endereco_combo.set(f"{rel_encontrado.id} - {e.logradouro}, {e.cidade}/{e.estado}")
                break
        
        # Preencher produto
        self.id_produto_selecionado = produto_encontrado.id_produto
        self.produto_desc_label.config(text=produto_encontrado.descricao)
        self.produto_designador_label.config(text=produto_encontrado.designador)
        self.produto_wan_label.config(text=produto_encontrado.wan_piloto)
        self.produto_combo.set(f"{produto_encontrado.id_produto} - {produto_encontrado.descricao}")
        
        # Carregar endereços e produtos nos combos
        self.carregar_enderecos(self.id_cliente_selecionado)
        self.carregar_produtos(self.id_cliente_selecionado, self.id_endereco_selecionado)
        
        messagebox.showinfo("Encontrado", f"Produto localizado!\nCliente: {self.cliente_nome_label.cget('text')}\nProduto: {produto_encontrado.descricao}")
    
    def limpar_busca(self):
        """Limpar campo de busca"""
        self.busca_wan_entry.delete(0, tk.END)
    
    # ==================== CADASTROS RÁPIDOS ====================
    
    def abrir_cadastro_tecnico(self):
        """Janela para cadastrar novo técnico"""
        self.janela_cadastro = tk.Toplevel(self)
        self.janela_cadastro.title("Cadastrar Novo Técnico")
        self.janela_cadastro.geometry("400x250")
        self.janela_cadastro.configure(bg=COLORS['light'])
        
        frame = ttk.Frame(self.janela_cadastro, padding=20)
        frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(frame, text="Nome:", font=FONTS['subtitle']).pack(anchor=tk.W, pady=5)
        nome_entry = ttk.Entry(frame, width=40, font=FONTS['normal'])
        nome_entry.pack(fill=tk.X, pady=5)
        
        ttk.Label(frame, text="Matrícula:", font=FONTS['subtitle']).pack(anchor=tk.W, pady=5)
        matricula_entry = ttk.Entry(frame, width=40, font=FONTS['normal'])
        matricula_entry.pack(fill=tk.X, pady=5)
        
        def salvar():
            nome = nome_entry.get().strip()
            matricula = matricula_entry.get().strip()
            
            if not nome or not matricula:
                messagebox.showwarning("Aviso", "Preencha todos os campos!")
                return
            
            self.tecnico_controller.inserir_tecnico(nome, matricula)
            messagebox.showinfo("Sucesso", "Técnico cadastrado!")
            self.carregar_tecnicos()
            self.janela_cadastro.destroy()
        
        ttk.Button(frame, text="Salvar", command=salvar).pack(pady=20)
    
    def abrir_cadastro_cliente(self):
        """Janela para cadastrar novo cliente"""
        self.janela_cadastro = tk.Toplevel(self)
        self.janela_cadastro.title("Cadastrar Novo Cliente")
        self.janela_cadastro.geometry("400x200")
        self.janela_cadastro.configure(bg=COLORS['light'])
        
        frame = ttk.Frame(self.janela_cadastro, padding=20)
        frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(frame, text="Nome do Cliente:", font=FONTS['subtitle']).pack(anchor=tk.W, pady=5)
        nome_entry = ttk.Entry(frame, width=40, font=FONTS['normal'])
        nome_entry.pack(fill=tk.X, pady=5)
        
        def salvar():
            nome = nome_entry.get().strip()
            
            if not nome:
                messagebox.showwarning("Aviso", "Preencha o nome!")
                return
            
            self.cliente_controller.inserir_cliente(nome)
            messagebox.showinfo("Sucesso", "Cliente cadastrado!")
            self.carregar_clientes()
            self.janela_cadastro.destroy()
        
        ttk.Button(frame, text="Salvar", command=salvar).pack(pady=20)
    
    def abrir_cadastro_endereco(self):
        """Janela para cadastrar novo endereço"""
        if not self.id_cliente_selecionado:
            messagebox.showwarning("Aviso", "Selecione um cliente primeiro!")
            return
        
        self.janela_cadastro = tk.Toplevel(self)
        self.janela_cadastro.title("Cadastrar Novo Endereço")
        self.janela_cadastro.geometry("450x300")
        self.janela_cadastro.configure(bg=COLORS['light'])
        
        frame = ttk.Frame(self.janela_cadastro, padding=20)
        frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(frame, text="Logradouro:", font=FONTS['subtitle']).pack(anchor=tk.W, pady=5)
        logradouro_entry = ttk.Entry(frame, width=40, font=FONTS['normal'])
        logradouro_entry.pack(fill=tk.X, pady=5)
        
        ttk.Label(frame, text="Cidade:", font=FONTS['subtitle']).pack(anchor=tk.W, pady=5)
        cidade_entry = ttk.Entry(frame, width=30, font=FONTS['normal'])
        cidade_entry.pack(fill=tk.X, pady=5)
        
        ttk.Label(frame, text="Estado:", font=FONTS['subtitle']).pack(anchor=tk.W, pady=5)
        estado_entry = ttk.Entry(frame, width=5, font=FONTS['normal'])
        estado_entry.pack(anchor=tk.W, pady=5)
        
        def salvar():
            logradouro = logradouro_entry.get().strip()
            cidade = cidade_entry.get().strip()
            estado = estado_entry.get().strip().upper()
            
            if not all([logradouro, cidade, estado]):
                messagebox.showwarning("Aviso", "Preencha todos os campos!")
                return
            
            endereco = self.endereco_controller.inserir_endereco(logradouro, cidade, estado)
            
            # Criar relacionamento
            relacionamento = ClienteEndereco(self.id_cliente_selecionado, endereco.id_endereco)
            self.cliente_endereco_repo.inserir(relacionamento)
            
            messagebox.showinfo("Sucesso", "Endereço cadastrado e vinculado ao cliente!")
            self.carregar_enderecos(self.id_cliente_selecionado)
            self.janela_cadastro.destroy()
        
        ttk.Button(frame, text="Salvar", command=salvar).pack(pady=20)
    
    def abrir_cadastro_produto(self):
        """Janela para cadastrar novo produto"""
        if not self.id_relacionamento_selecionado:
            messagebox.showwarning("Aviso", "Selecione um cliente e endereço primeiro!")
            return
        
        self.janela_cadastro = tk.Toplevel(self)
        self.janela_cadastro.title("Cadastrar Novo Produto")
        self.janela_cadastro.geometry("500x350")
        self.janela_cadastro.configure(bg=COLORS['light'])
        
        frame = ttk.Frame(self.janela_cadastro, padding=20)
        frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(frame, text="Descrição:", font=FONTS['subtitle']).pack(anchor=tk.W, pady=5)
        descricao_entry = ttk.Entry(frame, width=50, font=FONTS['normal'])
        descricao_entry.pack(fill=tk.X, pady=5)
        
        ttk.Label(frame, text="Designador:", font=FONTS['subtitle']).pack(anchor=tk.W, pady=5)
        designador_entry = ttk.Entry(frame, width=30, font=FONTS['normal'])
        designador_entry.pack(anchor=tk.W, pady=5)
        
        ttk.Label(frame, text="WAN/Piloto:", font=FONTS['subtitle']).pack(anchor=tk.W, pady=5)
        wan_entry = ttk.Entry(frame, width=30, font=FONTS['normal'])
        wan_entry.pack(anchor=tk.W, pady=5)
        
        def salvar():
            descricao = descricao_entry.get().strip()
            designador = designador_entry.get().strip()
            wan = wan_entry.get().strip()
            
            if not all([descricao, designador, wan]):
                messagebox.showwarning("Aviso", "Preencha todos os campos!")
                return
            
            self.produto_controller.inserir_produto(descricao, designador, wan, self.id_relacionamento_selecionado)
            messagebox.showinfo("Sucesso", "Produto cadastrado!")
            self.carregar_produtos(self.id_cliente_selecionado, self.id_endereco_selecionado)
            self.janela_cadastro.destroy()
        
        ttk.Button(frame, text="Salvar", command=salvar).pack(pady=20)
    
    # ==================== CRIAÇÃO DA OS ====================
    
    def criar_os(self):
        """Criar nova ordem de serviço"""
        # Validações
        if not self.id_tecnico_selecionado:
            messagebox.showwarning("Aviso", "Selecione ou cadastre um técnico!")
            return
        
        if not self.id_relacionamento_selecionado:
            messagebox.showwarning("Aviso", "Selecione ou cadastre um cliente e endereço!")
            return
        
        if not self.id_produto_selecionado:
            messagebox.showwarning("Aviso", "Selecione ou cadastre um produto!")
            return
        
        causa = self.causa_entry.get().strip()
        if not causa:
            messagebox.showwarning("Aviso", "Preencha a causa raiz!")
            return
        
        materiais = self.materiais_entry.get().strip()
        acao = self.acao_entry.get().strip()
        contato = self.contato_entry.get().strip()
        observacoes = self.obs_text.get("1.0", tk.END).strip()
        concluida = (self.status_var.get() == "2")
        
        # Criar OS
        ordem = self.os_controller.inserir_ordem(
            self.id_tecnico_selecionado,
            self.id_produto_selecionado,
            causa,
            materiais,
            acao,
            contato,
            observacoes,
            concluida
        )
        
        if ordem and ordem.id_os:
            messagebox.showinfo("Sucesso", f"✅ Ordem de Serviço Nº {ordem.id_os} criada com sucesso!")
            self.limpar_formulario()
            self.listar_ordens()
        else:
            messagebox.showerror("Erro", "Erro ao criar Ordem de Serviço!")
    
    # ==================== LISTAGEM E CONCLUSÃO ====================
    
    def listar_ordens(self):
        """Listar todas as ordens de serviço"""
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        ordens = self.os_controller.listar_ordens()
        tecnicos = {t.id: t.nome for t in self.tecnico_controller.listar_tecnicos()}
        produtos = {p.id_produto: p for p in self.produto_controller.listar_produtos()}
        clientes = {c.id_cliente: c.nome for c in self.cliente_controller.listar_clientes()}
        relacionamentos = self.cliente_endereco_repo.listar()
        
        # Mapear produto para cliente
        produto_cliente = {}
        for rel in relacionamentos:
            for p in produtos.values():
                if p.id_cliente_endereco == rel.id:
                    produto_cliente[p.id_produto] = clientes.get(rel.id_cliente, "N/A")
        
        for os in ordens:
            produto = produtos.get(os.id_produto)
            status = "✅ Concluída" if os.concluida else "🟡 Em andamento"
            
            self.tree.insert("", tk.END, values=(
                os.id_os,
                tecnicos.get(os.id_tecnico, "N/A"),
                produto_cliente.get(os.id_produto, "N/A"),
                produto.descricao if produto else "N/A",
                produto.wan_piloto if produto else "N/A",
                status,
                os.data_criacao
            ))
    
    def concluir_os_selecionada(self):
        """Concluir a OS selecionada na lista"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Aviso", "Selecione uma OS para concluir!")
            return
        
        item = self.tree.item(selection[0])
        id_os = item['values'][0]
        
        os = self.os_controller.buscar_ordem(id_os)
        if os.concluida:
            messagebox.showwarning("Aviso", f"OS {id_os} já está concluída!")
            return
        
        if messagebox.askyesno("Confirmar", f"Concluir OS Nº {id_os}?"):
            self.os_controller.concluir_ordem(id_os)
            messagebox.showinfo("Sucesso", f"✅ OS {id_os} concluída!")
            self.listar_ordens()
    
    def limpar_formulario(self):
        """Limpar todo o formulário"""
        # Limpar combos
        self.cliente_combo.set('')
        self.endereco_combo.set('')
        self.produto_combo.set('')
        self.tecnico_combo.set('')
        
        # Limpar labels
        self.cliente_nome_label.config(text="-")
        self.endereco_texto_label.config(text="-")
        self.produto_desc_label.config(text="-")
        self.produto_designador_label.config(text="-")
        self.produto_wan_label.config(text="-")
        self.tecnico_nome_label.config(text="-")
        self.tecnico_matricula_label.config(text="-")
        
        # Limpar variáveis
        self.id_cliente_selecionado = None
        self.id_endereco_selecionado = None
        self.id_relacionamento_selecionado = None
        self.id_produto_selecionado = None
        self.id_tecnico_selecionado = None
        
        # Limpar campos de texto
        self.causa_entry.delete(0, tk.END)
        self.materiais_entry.delete(0, tk.END)
        self.acao_entry.delete(0, tk.END)
        self.contato_entry.delete(0, tk.END)
        self.obs_text.delete("1.0", tk.END)
        self.busca_wan_entry.delete(0, tk.END)
        
        # Reset status
        self.status_var.set("1")