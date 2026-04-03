import tkinter as tk
from tkinter import ttk, messagebox
from app.view.gui.styles import COLORS, FONTS, configurar_estilos
from app.view.gui.frames.tecnico_frame import TecnicoFrame
from app.view.gui.frames.cliente_frame import ClienteFrame
from app.view.gui.frames.endereco_frame import EnderecoFrame
from app.view.gui.frames.produto_frame import ProdutoFrame
from app.view.gui.frames.os_frame import OSFrame

class MainWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Sistema de Ordem de Serviço")
        self.root.geometry("1200x700")
        self.root.configure(bg=COLORS['light'])
        
        # Configurar estilos
        configurar_estilos()
        
        # Frame principal
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Título
        self.criar_titulo()
        
        # Menu lateral
        self.criar_menu()
        
        # Área de conteúdo
        self.content_frame = ttk.Frame(self.main_frame)
        self.content_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))
        
        # Frame atual
        self.current_frame = None
        
        # Mostrar frame inicial
        self.mostrar_frame("tecnicos")
        
        self.root.mainloop()
    
    def criar_titulo(self):
        """Criar título da aplicação"""
        title_frame = ttk.Frame(self.main_frame)
        title_frame.pack(fill=tk.X, pady=(0, 10))
        
        title_label = tk.Label(
            title_frame,
            text="📋 SISTEMA DE ORDEM DE SERVIÇO",
            font=FONTS['title'],
            bg=COLORS['light'],
            fg=COLORS['primary']
        )
        title_label.pack()
    
    def criar_menu(self):
        """Criar menu lateral"""
        menu_frame = ttk.Frame(self.main_frame, width=200)
        menu_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        menu_frame.pack_propagate(False)
        
        # Botões do menu
        botoes = [
            ("👤 Técnicos", "tecnicos"),
            ("👥 Clientes", "clientes"),
            ("📍 Endereços", "enderecos"),
            ("📦 Produtos", "produtos"),
            ("🔧 Ordens de Serviço", "os")
        ]
        
        for texto, valor in botoes:
            btn = tk.Button(
                menu_frame,
                text=texto,
                font=FONTS['normal'],
                bg=COLORS['primary'],
                fg=COLORS['white'],
                relief=tk.FLAT,
                padx=10,
                pady=10,
                cursor="hand2",
                command=lambda v=valor: self.mostrar_frame(v)
            )
            btn.pack(fill=tk.X, pady=5)
        
        # Botão Sair
        tk.Button(
            menu_frame,
            text="🚪 Sair",
            font=FONTS['normal'],
            bg=COLORS['danger'],
            fg=COLORS['white'],
            relief=tk.FLAT,
            padx=10,
            pady=10,
            cursor="hand2",
            command=self.sair
        ).pack(fill=tk.X, pady=(20, 0))
    
    def mostrar_frame(self, frame_name):
        """Mostrar o frame selecionado"""
        # Limpar frame atual
        if self.current_frame:
            self.current_frame.destroy()
        
        # Criar novo frame
        frames = {
            "tecnicos": TecnicoFrame,
            "clientes": ClienteFrame,
            "enderecos": EnderecoFrame,
            "produtos": ProdutoFrame,
            "os": OSFrame
        }
        
        if frame_name in frames:
            self.current_frame = frames[frame_name](self.content_frame)
            self.current_frame.pack(fill=tk.BOTH, expand=True)
    
    def sair(self):
        """Sair da aplicação"""
        if messagebox.askyesno("Sair", "Deseja realmente sair?"):
            self.root.destroy()