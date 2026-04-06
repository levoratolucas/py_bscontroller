# app/frontend/styles.py

import customtkinter as ctk

# Cores - Tema Híbrido (Fundo escuro, Conteúdo claro)
COLORS = {
    # Cores principais
    'primary': '#6B37FF',           # Roxo Vivo
    'primary_light': '#8B5FFF',
    'primary_dark': '#4B1FB0',
    
    # Fundos (escuros)
    'bg_main': '#1A1A2E',           # Fundo principal - escuro
    'bg_sidebar': '#0F0F23',        # Sidebar - mais escuro
    'bg_topbar': '#4B1FB0',         # Topbar - roxo escuro
    
    # Cards e elementos de conteúdo (claros)
    'bg_card': '#FFFFFF',           # Cards - branco
    'bg_table_header': '#F0F0F0',   # Cabeçalho tabela - cinza claro
    'bg_table_row_even': '#FFFFFF', # Linha par - branca
    'bg_table_row_odd': '#F8F8F8',  # Linha ímpar - cinza muito claro
    'bg_table_hover': '#E3F2FD',    # Hover - azul bem claro
    
    # Textos
    'text_primary': '#1A1A2E',      # Texto principal - escuro (para fundo claro)
    'text_secondary': '#6C6C8A',    # Texto secundário - cinza
    'text_light': '#FFFFFF',        # Texto claro (para fundos escuros)
    'text_dark': '#1A1A2E',         # Texto escuro (para fundos claros)
    
    # Bordas e divisores
    'border': '#E0E0E0',            # Bordas - cinza claro
    'divider': '#EEEEEE',           # Divisores - cinza bem claro
    
    # Status
    'success': '#00E5A0',           # Verde
    'success_bg': '#E8F8F5',        # Fundo verde claro
    'warning': '#FFB800',           # Amarelo
    'warning_bg': '#FFF8E1',        # Fundo amarelo claro
    'danger': '#FF4757',            # Vermelho
    'danger_bg': '#FFEBEE',         # Fundo vermelho claro
    
    # Repetidos (amarelo suave)
    'repetido_even': '#FFF8E1',
    'repetido_odd': '#FFFDE7',
    
    # Botões
    'button_primary': '#6B37FF',    # Botão primário - roxo
    'button_primary_hover': '#8B5FFF',
    'button_secondary': '#F0F0F0',  # Botão secundário - cinza claro
    'button_secondary_hover': '#E0E0E0',
}

# Fontes
FONTS = {
    'title': ('Inter', 24, 'bold'),
    'subtitle': ('Inter', 16, 'bold'),
    'body': ('Inter', 12, 'normal'),
    'body_bold': ('Inter', 12, 'bold'),
    'small': ('Inter', 10, 'normal'),
    'button': ('Inter', 14, 'bold'),
    'table_header': ('Inter', 12, 'bold'),
    'table_cell': ('Inter', 11, 'normal'),
}


def setup_theme():
    """Configurar tema do CustomTkinter"""
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")
    
    ctk.set_widget_scaling(1.0)
    ctk.set_window_scaling(1.0)