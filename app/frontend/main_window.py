# app/frontend/main_window.py

import customtkinter as ctk
from app.frontend.styles import COLORS, setup_theme
from app.frontend.components import Sidebar, TopBar
from app.frontend.screens import DashboardScreen, RelatoriosScreen


class MainWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        setup_theme()
        
        self.title("VIVO OS - Sistema de Ordem de Serviço")
        self.geometry("1300x750")
        self.minsize(1100, 600)
        
        # Configurar grid da janela principal
        self.grid_rowconfigure(0, weight=0)  # TopBar
        self.grid_rowconfigure(1, weight=1)  # Conteúdo
        self.grid_columnconfigure(0, weight=0)  # Sidebar
        self.grid_columnconfigure(1, weight=1)  # Conteúdo
        
        # Top bar
        self.topbar = TopBar(self)
        self.topbar.grid(row=0, column=0, columnspan=2, sticky="ew")
        
        # Sidebar
        self.sidebar = Sidebar(self, self.navigate_to)
        self.sidebar.grid(row=1, column=0, sticky="nsew")
        
        # Content area
        self.content_frame = ctk.CTkFrame(self, fg_color=COLORS['bg_main'])
        self.content_frame.grid(row=1, column=1, sticky="nsew")
        self.content_frame.grid_columnconfigure(0, weight=1)
        self.content_frame.grid_rowconfigure(0, weight=1)
        
        # Start with dashboard
        self.current_screen = None
        self.navigate_to("dashboard")
    
    def navigate_to(self, page):
        # Destroy current screen
        if self.current_screen:
            self.current_screen.destroy()
        
        # Update topbar title
        titles = {
            "dashboard": "Dashboard",
            "nova_os": "Nova Ordem de Serviço",
            "consultar": "Consultar OS",
            "relatorios": "Relatórios",
            "admin": "Administração"
        }
        self.topbar.set_title(titles.get(page, page))
        
        # Create new screen
        if page == "dashboard":
            self.current_screen = DashboardScreen(self.content_frame, self.navigate_to)
        elif page == "relatorios":
            self.current_screen = RelatoriosScreen(self.content_frame)
        else:
            # Placeholder para outras telas
            self.current_screen = ctk.CTkFrame(self.content_frame, fg_color=COLORS['bg_main'])
            self.current_screen.pack(fill="both", expand=True)
            
            label = ctk.CTkLabel(
                self.current_screen,
                text=f"📄 {titles.get(page, page)}\n\nEm desenvolvimento...",
                font=("Inter", 20),
                text_color=COLORS['text_secondary']
            )
            label.pack(expand=True)