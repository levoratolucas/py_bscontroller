# app/frontend/main_window.py

import customtkinter as ctk
from app.frontend.dashboard import DashboardScreen

# Cores
COLORS = {
    'primary': '#6B37FF',
    'primary_dark': '#4B1FB0',
    'dark': '#1A1A2E',
    'dark_card': '#16213E',
    'white': '#FFFFFF',
    'gray': '#6C6C8A'
}

class MainWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("VIVO OS - Sistema de Ordem de Serviço")
        self.geometry("1200x700")
        self.minsize(1000, 600)
        
        # Configurar tema
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")
        
        # Frame principal
        self.main_frame = ctk.CTkFrame(self, fg_color=COLORS['dark'])
        self.main_frame.pack(fill="both", expand=True)
        
        # Top bar
        self.create_top_bar()
        
        # Sidebar
        self.create_sidebar()
        
        # Content area
        self.content_frame = ctk.CTkFrame(self.main_frame, fg_color=COLORS['dark'])
        self.content_frame.pack(side="right", fill="both", expand=True)
        
        # Mostrar dashboard
        self.show_dashboard()
    
    def create_top_bar(self):
        top_bar = ctk.CTkFrame(
            self.main_frame,
            height=60,
            fg_color=COLORS['primary_dark'],
            corner_radius=0
        )
        top_bar.pack(fill="x")
        top_bar.pack_propagate(False)
        
        logo = ctk.CTkLabel(
            top_bar,
            text="📡 VIVO OS",
            font=("Inter", 20, "bold"),
            text_color=COLORS['white']
        )
        logo.pack(side="left", padx=20, pady=10)
    
    def create_sidebar(self):
        sidebar = ctk.CTkFrame(
            self.main_frame,
            width=200,
            fg_color=COLORS['dark_card'],
            corner_radius=0
        )
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)
        
        menu_items = [
            ("📊 Dashboard", self.show_dashboard),
            ("➕ Nova OS", self.show_nova_os),
            ("🔍 Consultar", self.show_consultar),
            ("📈 Relatórios", self.show_relatorios),
            ("⚙️ Admin", self.show_admin)
        ]
        
        for text, command in menu_items:
            btn = ctk.CTkButton(
                sidebar,
                text=text,
                font=("Inter", 14),
                fg_color="transparent",
                hover_color=COLORS['primary'],
                anchor="w",
                height=45,
                corner_radius=10
            )
            btn.pack(fill="x", padx=15, pady=5)
            btn.configure(command=command)
    
    def clear_content(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()
    
    def show_dashboard(self):
        self.clear_content()
        DashboardScreen(self.content_frame)
    
    def show_nova_os(self):
        self.clear_content()
        label = ctk.CTkLabel(
            self.content_frame,
            text="Nova OS - Em desenvolvimento",
            font=("Inter", 24, "bold"),
            text_color=COLORS['white']
        )
        label.pack(expand=True)
    
    def show_consultar(self):
        self.clear_content()
        label = ctk.CTkLabel(
            self.content_frame,
            text="Consultar OS - Em desenvolvimento",
            font=("Inter", 24, "bold"),
            text_color=COLORS['white']
        )
        label.pack(expand=True)
    
    def show_relatorios(self):
        self.clear_content()
        label = ctk.CTkLabel(
            self.content_frame,
            text="Relatórios - Em desenvolvimento",
            font=("Inter", 24, "bold"),
            text_color=COLORS['white']
        )
        label.pack(expand=True)
    
    def show_admin(self):
        self.clear_content()
        label = ctk.CTkLabel(
            self.content_frame,
            text="Administração - Em desenvolvimento",
            font=("Inter", 24, "bold"),
            text_color=COLORS['white']
        )
        label.pack(expand=True)