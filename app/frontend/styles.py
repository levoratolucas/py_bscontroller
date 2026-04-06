# app/frontend/styles.py

import customtkinter as ctk

# Cores do tema Vivo
COLORS = {
    'primary': '#6B37FF',      # Roxo Vivo
    'primary_light': '#8B5FFF',
    'primary_dark': '#4B1FB0',
    'secondary': '#00BFFF',     # Azul neon
    'success': '#00E5A0',       # Verde neon
    'warning': '#FFB800',
    'danger': '#FF4757',
    'dark': '#1A1A2E',
    'dark_card': '#16213E',
    'dark_sidebar': '#0F0F23',
    'light': '#E0E0E0',
    'white': '#FFFFFF',
    'gray': '#6C6C8A'
}

# Fontes
FONTS = {
    'title': ('Inter', 24, 'bold'),
    'subtitle': ('Inter', 16, 'bold'),
    'body': ('Inter', 12, 'normal'),
    'small': ('Inter', 10, 'normal'),
    'button': ('Inter', 14, 'bold')
}

# Configurações do tema
def setup_theme():
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")
    
    # Configurar cores personalizadas
    ctk.ThemeManager.theme['CTkFrame']['fg_color'] = COLORS['dark']
    ctk.ThemeManager.theme['CTkButton']['fg_color'] = COLORS['primary']
    ctk.ThemeManager.theme['CTkButton']['hover_color'] = COLORS['primary_light']