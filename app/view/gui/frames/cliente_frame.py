import tkinter as tk
from tkinter import ttk, messagebox
from app.controller.cliente_controller import ClienteController
from app.view.gui.styles import COLORS, FONTS

class ClienteFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.controller = ClienteController()
        self.criar_widgets()
        self.listar_clientes()
    
    def criar_widgets(self):
        # Frame do formulário
        form_frame = ttk.LabelFrame(self, text="Cadastro de Cliente", padding=10)
        form_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Nome
        ttk.Label(form_frame, text="Nome:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.nome_entry = ttk.Entry(form_frame, width=50)
        self.nome_entry.grid(row=0, column=1, padx=(10, 0), pady=5)
        
        # Botões
        btn_frame = ttk.Frame(form_frame)
        btn_frame.grid(row=1, column=0, columnspan=2, pady=10)
        
        ttk.Button(btn_frame, text="Salvar", command=self.salvar_cliente).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Limpar", command=self.limpar_formulario).pack(side=tk.LEFT, padx=5)
        
        # Frame da lista
        list_frame = ttk.LabelFrame(self, text="Lista de Clientes", padding=10)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Treeview
        columns = ("ID", "Nome")
        self.tree = ttk.Treeview(list_frame, columns=columns, show="headings", height=15)
        
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=200)
        
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    def salvar_cliente(self):
        nome = self.nome_entry.get().strip()
        
        if not nome:
            messagebox.showwarning("Aviso", "Preencha o nome do cliente!")
            return
        
        # Verificar se já existe
        cliente_existente = self.controller.buscar_cliente_por_nome(nome)
        if cliente_existente:
            messagebox.showwarning("Aviso", f"Cliente '{nome}' já existe!")
            return
        
        cliente = self.controller.inserir_cliente(nome)
        messagebox.showinfo("Sucesso", f"Cliente '{nome}' cadastrado com sucesso!")
        self.limpar_formulario()
        self.listar_clientes()
    
    def limpar_formulario(self):
        self.nome_entry.delete(0, tk.END)
    
    def listar_clientes(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        clientes = self.controller.listar_clientes()
        for c in clientes:
            self.tree.insert("", tk.END, values=(c.id_cliente, c.nome))