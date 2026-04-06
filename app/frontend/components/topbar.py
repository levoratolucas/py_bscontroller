# app/frontend/components/topbar.py

import customtkinter as ctk
from app.frontend.styles import COLORS, FONTS


class TopBar(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(
            parent,
            height=60,
            corner_radius=0,
            fg_color=COLORS['bg_topbar']
        )
        self.grid_propagate(False)
        
        self.create_widgets()
    
    def create_widgets(self):
        # Título da página
        self.title_label = ctk.CTkLabel(
            self,
            text="Dashboard",
            font=FONTS['subtitle'],
            text_color=COLORS['text_light']
        )
        self.title_label.place(relx=0.5, rely=0.5, anchor="center")
        
        # Usuário
        user_frame = ctk.CTkFrame(self, fg_color="transparent")
        user_frame.place(relx=0.98, rely=0.5, anchor="e")
        
        user_icon = ctk.CTkLabel(
            user_frame,
            text="👤",
            font=("Inter", 16),
            text_color=COLORS['text_light']
        )
        user_icon.pack(side="left", padx=5)
        
        user_name = ctk.CTkLabel(
            user_frame,
            text="Administrador",
            font=FONTS['small'],
            text_color=COLORS['text_light']
        )
        user_name.pack(side="left")
    
    def set_title(self, title):
        self.title_label.configure(text=title)