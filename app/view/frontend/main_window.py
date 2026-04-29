import customtkinter as ctk
from app.view.frontend.styles import COLORS
from app.view.frontend.screens.dashboard.main import DashboardScreen
from app.view.frontend.screens.ordem_servico import OrdemServicoScreen
from app.view.frontend.screens.nova_os import NovaOsScreen
from app.view.frontend.screens.admin import AdminScreen
from app.view.frontend.screens.relatorios.main import RelatoriosScreen
from app.view.frontend.screens.repetidos.repetidos_main import RepetidosScreen

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class MainWindow:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("LEVORATECH - VIVO OS")
        self.root.geometry("1280x720")
        self.root.minsize(1024, 600)
        
        # Frame principal
        self.main_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        self.main_frame.pack(fill="both", expand=True)
        
        # Sidebar
        self.criar_sidebar()
        
        # Content area
        self.content_frame = ctk.CTkFrame(self.main_frame, fg_color=COLORS['bg_main'], corner_radius=0)
        self.content_frame.pack(side="right", fill="both", expand=True)
        
        # Tela atual
        self.current_screen = None
        
        # Mostrar dashboard inicial
        self.mostrar_tela("ordem_servico")
        
        self.root.mainloop()
    
    def criar_sidebar(self):
        sidebar = ctk.CTkFrame(self.main_frame, width=250, corner_radius=0, fg_color=COLORS['primary'])
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)
        
        # Logo
        ctk.CTkLabel(
            sidebar,
            text="VIVO OS",
            font=('Arial', 24, 'bold'),
            text_color=COLORS['white']
        ).pack(pady=(30, 20))
        
        # Botões do menu
        botoes = [
            ("📝 Inserir OS", "nova_os"),
            ("📋 Ordem Serviço", "ordem_servico"),
            ("📈 Relatórios", "relatorios"),
            ("🔧 Admin", "admin")
        ]
        
        for texto, pagina in botoes:
            btn = ctk.CTkButton(
                sidebar,
                text=texto,
                fg_color="transparent",
                text_color=COLORS['white'],
                anchor="w",
                font=('Arial', 14),
                command=lambda p=pagina: self.mostrar_tela(p)
            )
            btn.pack(fill="x", padx=20, pady=5)
        
        # Sair
        ctk.CTkButton(
            sidebar,
            text="🚪 Sair",
            fg_color=COLORS['danger'],
            text_color=COLORS['white'],
            command=self.sair
        ).pack(side="bottom", fill="x", padx=20, pady=20)
    
    def mostrar_tela(self, nome_tela):
        if self.current_screen:
            self.current_screen.destroy()
        
        if nome_tela == "nova_os":
            self.current_screen = NovaOsScreen(self.content_frame, self)
        elif nome_tela == "ordem_servico":
            self.current_screen = OrdemServicoScreen(self.content_frame, self)
        elif nome_tela == "relatorios":
            self.current_screen = RelatoriosScreen(self.content_frame, self)
        elif nome_tela == "repetidos":
            self.current_screen = RepetidosScreen(self.content_frame, self)
        elif nome_tela == "admin":
            self.current_screen = AdminScreen(self.content_frame, self)
        
        if self.current_screen:
            self.current_screen.pack(fill="both", expand=True)
    
    def sair(self):
        self.root.destroy()