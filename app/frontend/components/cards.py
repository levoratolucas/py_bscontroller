# app/frontend/components/cards.py

import customtkinter as ctk
from app.frontend.styles import COLORS, FONTS


class KPICard(ctk.CTkFrame):
    def __init__(self, parent, title, value, icon, color):
        super().__init__(
            parent,
            corner_radius=12,
            fg_color=COLORS['bg_card'],
            border_width=1,
            border_color=COLORS['border']
        )
        self.pack(side="left", padx=10, pady=10, fill="both", expand=True)
        
        # Icon
        icon_label = ctk.CTkLabel(
            self,
            text=icon,
            font=('Inter', 32),
            text_color=color
        )
        icon_label.pack(pady=(15, 5))
        
        # Value
        value_label = ctk.CTkLabel(
            self,
            text=str(value),
            font=('Inter', 28, 'bold'),
            text_color=COLORS['text_primary']
        )
        value_label.pack()
        
        # Title
        title_label = ctk.CTkLabel(
            self,
            text=title,
            font=FONTS['small'],
            text_color=COLORS['text_secondary']
        )
        title_label.pack(pady=(0, 15))


class ActionCard(ctk.CTkFrame):
    def __init__(self, parent, title, description, icon, command):
        super().__init__(
            parent,
            corner_radius=12,
            fg_color=COLORS['bg_card'],
            border_width=1,
            border_color=COLORS['border']
        )
        self.pack(side="left", padx=10, pady=10, fill="both", expand=True)
        
        self.bind("<Button-1>", lambda e: command())
        
        # Icon
        icon_label = ctk.CTkLabel(
            self,
            text=icon,
            font=('Inter', 40),
            text_color=COLORS['primary']
        )
        icon_label.pack(pady=(20, 10))
        icon_label.bind("<Button-1>", lambda e: command())
        
        # Title
        title_label = ctk.CTkLabel(
            self,
            text=title,
            font=FONTS['subtitle'],
            text_color=COLORS['text_primary']
        )
        title_label.pack()
        title_label.bind("<Button-1>", lambda e: command())
        
        # Description
        desc_label = ctk.CTkLabel(
            self,
            text=description,
            font=FONTS['small'],
            text_color=COLORS['text_secondary'],
            wraplength=180
        )
        desc_label.pack(pady=(5, 20))
        desc_label.bind("<Button-1>", lambda e: command())
        
        # Cursor de mão
        self.configure(cursor="hand2")
        icon_label.configure(cursor="hand2")
        title_label.configure(cursor="hand2")
        desc_label.configure(cursor="hand2")