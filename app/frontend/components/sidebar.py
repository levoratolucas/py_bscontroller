# app/frontend/components/sidebar.py

import customtkinter as ctk
from app.frontend.styles import COLORS, FONTS


class Sidebar(ctk.CTkFrame):
    def __init__(self, parent, on_navigate):
        super().__init__(
            parent, 
            width=240, 
            corner_radius=0, 
            fg_color=COLORS['bg_sidebar']
        )
        self.on_navigate = on_navigate
        self.grid_propagate(False)
        
        self.create_widgets()
    
    def create_widgets(self):
        # Logo
        logo_frame = ctk.CTkFrame(self, fg_color="transparent")
        logo_frame.pack(pady=30, padx=20)
        
        logo_label = ctk.CTkLabel(
            logo_frame,
            text="📡 VIVO OS",
            font=("Inter", 20, "bold"),
            text_color=COLORS['primary']
        )
        logo_label.pack()
        
        subtitle = ctk.CTkLabel(
            logo_frame,
            text="Ordem de Serviço",
            font=FONTS['small'],
            text_color=COLORS['text_secondary']
        )
        subtitle.pack()
        
        # Separador
        separator = ctk.CTkFrame(self, height=1, fg_color=COLORS['primary_dark'])
        separator.pack(fill="x", padx=20, pady=10)
        
        # Menu items
        menu_items = [
            ("📊 Dashboard", "dashboard"),
            ("➕ Nova OS", "nova_os"),
            ("🔍 Consultar", "consultar"),
            ("📈 Relatórios", "relatorios"),
            ("⚙️ Admin", "admin")
        ]
        
        for text, page in menu_items:
            btn = ctk.CTkButton(
                self,
                text=text,
                font=FONTS['body'],
                fg_color="transparent",
                text_color=COLORS['text_light'],
                hover_color=COLORS['primary_dark'],
                anchor="w",
                height=40,
                corner_radius=8
            )
            btn.pack(fill="x", padx=15, pady=5)
            btn.configure(command=lambda p=page: self.on_navigate(p))