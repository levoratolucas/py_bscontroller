import tkinter as tk
from tkinter import ttk, messagebox
from app.controller.tecnico_controller import TecnicoController
from app.view.gui.styles import COLORS, FONTS

class TecnicoFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.controller = TecnicoController()
        self.criar_widgets()
        self.listar_tecnicos()
    
    def criar_widgets(self):
        # Frame do formulário
        form_frame = ttk.LabelFrame(self, text="Cadastro de Técnico", padding=10)
        form_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Nome
        ttk.Label(form_frame, text="Nome:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.nome_entry = ttk.Entry(form_frame, width=40)
        self.nome_entry.grid(row=0, column=1, padx=(10, 0), pady=5)
        
        # Matrícula
        ttk.Label(form_frame, text="Matrícula:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.matricula_entry = ttk.Entry(form_frame, width=40)
        self.matricula_entry.grid(row=1, column=1, padx=(10, 0), pady=5)
        
        # Botões
        btn_frame = ttk.Frame(form_frame)
        btn_frame.grid(row=2, column=0, columnspan=2, pady=10)
        
        ttk.Button(btn_frame, text="Salvar", command=self.salvar_tecnico).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Limpar", command=self.limpar_formulario).pack(side=tk.LEFT, padx=5)
        
        # Frame da lista
        list_frame = ttk.LabelFrame(self, text="Lista de Técnicos", padding=10)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Treeview
        columns = ("ID", "Nome", "Matrícula")
        self.tree = ttk.Treeview(list_frame, columns=columns, show="headings", height=15)
        
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150)
        
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Bind de seleção
        self.tree.bind("<<TreeviewSelect>>", self.on_selecionar)
    
    def salvar_tecnico(self):
        nome = self.nome_entry.get().strip()
        matricula = self.matricula_entry.get().strip()
        
        if not nome or not matricula:
            messagebox.showwarning("Aviso", "Preencha todos os campos!")
            return
        
        resultado = self.controller.inserir_tecnico(nome, matricula)
        messagebox.showinfo("Sucesso", resultado)
        self.limpar_formulario()
        self.listar_tecnicos()
    
    def limpar_formulario(self):
        self.nome_entry.delete(0, tk.END)
        self.matricula_entry.delete(0, tk.END)
    
    def listar_tecnicos(self):
        # Limpar treeview
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Inserir dados
        tecnicos = self.controller.listar_tecnicos()
        for t in tecnicos:
            self.tree.insert("", tk.END, values=(t.id, t.nome, t.matricula))
    
    def on_selecionar(self, event):
        selection = self.tree.selection()
        if selection:
            item = self.tree.item(selection[0])
            values = item['values']
            self.nome_entry.delete(0, tk.END)
            self.nome_entry.insert(0, values[1])
            self.matricula_entry.delete(0, tk.END)
            self.matricula_entry.insert(0, values[2])