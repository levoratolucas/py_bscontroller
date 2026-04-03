import tkinter as tk
from tkinter import ttk, messagebox
from app.controller.endereco_controller import EnderecoController
from app.view.gui.styles import COLORS, FONTS

class EnderecoFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.controller = EnderecoController()
        self.criar_widgets()
        self.listar_enderecos()
    
    def criar_widgets(self):
        # Frame do formulário
        form_frame = ttk.LabelFrame(self, text="Cadastro de Endereço", padding=10)
        form_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Logradouro
        ttk.Label(form_frame, text="Logradouro:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.logradouro_entry = ttk.Entry(form_frame, width=50)
        self.logradouro_entry.grid(row=0, column=1, padx=(10, 0), pady=5)
        
        # Cidade
        ttk.Label(form_frame, text="Cidade:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.cidade_entry = ttk.Entry(form_frame, width=30)
        self.cidade_entry.grid(row=1, column=1, padx=(10, 0), pady=5, sticky=tk.W)
        
        # Estado
        ttk.Label(form_frame, text="Estado:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.estado_entry = ttk.Entry(form_frame, width=5)
        self.estado_entry.grid(row=2, column=1, padx=(10, 0), pady=5, sticky=tk.W)
        
        # Botões
        btn_frame = ttk.Frame(form_frame)
        btn_frame.grid(row=3, column=0, columnspan=2, pady=10)
        
        ttk.Button(btn_frame, text="Salvar", command=self.salvar_endereco).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Limpar", command=self.limpar_formulario).pack(side=tk.LEFT, padx=5)
        
        # Frame da lista
        list_frame = ttk.LabelFrame(self, text="Lista de Endereços", padding=10)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Treeview
        columns = ("ID", "Logradouro", "Cidade", "Estado")
        self.tree = ttk.Treeview(list_frame, columns=columns, show="headings", height=15)
        
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150)
        
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    def salvar_endereco(self):
        logradouro = self.logradouro_entry.get().strip()
        cidade = self.cidade_entry.get().strip()
        estado = self.estado_entry.get().strip().upper()
        
        if not all([logradouro, cidade, estado]):
            messagebox.showwarning("Aviso", "Preencha todos os campos!")
            return
        
        endereco = self.controller.inserir_endereco(logradouro, cidade, estado)
        messagebox.showinfo("Sucesso", f"Endereço cadastrado com sucesso!")
        self.limpar_formulario()
        self.listar_enderecos()
    
    def limpar_formulario(self):
        self.logradouro_entry.delete(0, tk.END)
        self.cidade_entry.delete(0, tk.END)
        self.estado_entry.delete(0, tk.END)
    
    def listar_enderecos(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        enderecos = self.controller.listar_enderecos()
        for e in enderecos:
            self.tree.insert("", tk.END, values=(e.id_endereco, e.logradouro, e.cidade, e.estado))