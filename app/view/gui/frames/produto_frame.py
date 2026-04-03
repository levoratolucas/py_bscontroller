import tkinter as tk
from tkinter import ttk, messagebox
from app.controller.produto_controller import ProdutoController
from app.controller.cliente_controller import ClienteController
from app.controller.endereco_controller import EnderecoController
from app.bd.cliente_endereco_repository import ClienteEnderecoRepository
from app.view.gui.styles import COLORS, FONTS

class ProdutoFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.produto_controller = ProdutoController()
        self.cliente_controller = ClienteController()
        self.endereco_controller = EnderecoController()
        self.cliente_endereco_repo = ClienteEnderecoRepository()
        self.criar_widgets()
        self.listar_produtos()
        self.carregar_relacionamentos()
    
    def criar_widgets(self):
        # Frame do formulário
        form_frame = ttk.LabelFrame(self, text="Cadastro de Produto", padding=10)
        form_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Relacionamento Cliente-Endereço
        ttk.Label(form_frame, text="Cliente/Endereço:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.relacionamento_combo = ttk.Combobox(form_frame, width=50)
        self.relacionamento_combo.grid(row=0, column=1, padx=(10, 0), pady=5)
        
        # Descrição
        ttk.Label(form_frame, text="Descrição:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.descricao_entry = ttk.Entry(form_frame, width=50)
        self.descricao_entry.grid(row=1, column=1, padx=(10, 0), pady=5)
        
        # Designador
        ttk.Label(form_frame, text="Designador:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.designador_entry = ttk.Entry(form_frame, width=30)
        self.designador_entry.grid(row=2, column=1, padx=(10, 0), pady=5, sticky=tk.W)
        
        # WAN/Piloto
        ttk.Label(form_frame, text="WAN/Piloto:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.wan_entry = ttk.Entry(form_frame, width=30)
        self.wan_entry.grid(row=3, column=1, padx=(10, 0), pady=5, sticky=tk.W)
        
        # Botões
        btn_frame = ttk.Frame(form_frame)
        btn_frame.grid(row=4, column=0, columnspan=2, pady=10)
        
        ttk.Button(btn_frame, text="Salvar", command=self.salvar_produto).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Limpar", command=self.limpar_formulario).pack(side=tk.LEFT, padx=5)
        
        # Frame da lista
        list_frame = ttk.LabelFrame(self, text="Lista de Produtos", padding=10)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Treeview
        columns = ("ID", "Descrição", "Designador", "WAN/Piloto")
        self.tree = ttk.Treeview(list_frame, columns=columns, show="headings", height=15)
        
        self.tree.heading("ID", text="ID")
        self.tree.heading("Descrição", text="Descrição")
        self.tree.heading("Designador", text="Designador")
        self.tree.heading("WAN/Piloto", text="WAN/Piloto")
        
        self.tree.column("ID", width=50)
        self.tree.column("Descrição", width=250)
        self.tree.column("Designador", width=150)
        self.tree.column("WAN/Piloto", width=150)
        
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    def carregar_relacionamentos(self):
        relacionamentos = self.cliente_endereco_repo.listar()
        clientes = {c.id_cliente: c for c in self.cliente_controller.listar_clientes()}
        enderecos = {e.id_endereco: e for e in self.endereco_controller.listar_enderecos()}
        
        opcoes = []
        for rel in relacionamentos:
            cliente = clientes.get(rel.id_cliente)
            endereco = enderecos.get(rel.id_endereco)
            if cliente and endereco:
                texto = f"{cliente.nome} - {endereco.logradouro}, {endereco.cidade}"
                opcoes.append((rel.id, texto))
        
        self.relacionamento_combo['values'] = [f"{id} - {texto}" for id, texto in opcoes]
    
    def salvar_produto(self):
        if not self.relacionamento_combo.get():
            messagebox.showwarning("Aviso", "Selecione um cliente/endereço!")
            return
        
        id_rel = int(self.relacionamento_combo.get().split(" - ")[0])
        descricao = self.descricao_entry.get().strip()
        designador = self.designador_entry.get().strip()
        wan = self.wan_entry.get().strip()
        
        if not all([descricao, designador, wan]):
            messagebox.showwarning("Aviso", "Preencha todos os campos!")
            return
        
        produto = self.produto_controller.inserir_produto(descricao, designador, wan, id_rel)
        messagebox.showinfo("Sucesso", f"Produto '{descricao}' cadastrado!")
        self.limpar_formulario()
        self.listar_produtos()
    
    def limpar_formulario(self):
        self.relacionamento_combo.set('')
        self.descricao_entry.delete(0, tk.END)
        self.designador_entry.delete(0, tk.END)
        self.wan_entry.delete(0, tk.END)
    
    def listar_produtos(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        produtos = self.produto_controller.listar_produtos()
        for p in produtos:
            self.tree.insert("", tk.END, values=(p.id_produto, p.descricao, p.designador, p.wan_piloto))