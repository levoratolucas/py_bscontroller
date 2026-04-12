# Cores do sistema
COLORS = {
    # Cores principais
    'primary': '#2196F3',
    'primary_dark': '#1976D2',
    'primary_light': '#64B5F6',
    
    # Fundos
    'bg_dark': '#1e1e1e',
    'bg_main': '#1e1e1e',      # Fundo principal (igual ao bg_dark)
    'bg_card': '#2d2d2d',
    'bg_input': '#3d3d3d',
    'bg_topbar': '#252526',
    'bg_sidebar': '#1e1e1e',
    'bg_hover': '#3d3d3d',      # <-- ADICIONAR ESTA LINHA
    'bg_button': '#2196F3',
    
    # Textos
    'text_light': '#ffffff',
    'text_secondary': '#b0b0b0',
    'text_dark': '#333333',
    'text_muted': '#808080',
    'white': '#ffffff',          # <-- ADICIONAR ESTA LINHA
    
    # Bordas
    'border': '#4d4d4d',
    'border_light': '#3d3d3d',
    
    # Status
    'success': '#4CAF50',
    'success_dark': '#388E3C',
    'warning': '#FFC107',
    'warning_dark': '#FFA000',
    'danger': '#f44336',
    'danger_dark': '#D32F2F',
    'info': '#2196F3',
    'info_dark': '#1976D2',
    
    # Ícones
    'icon_primary': '#2196F3',
    'icon_success': '#4CAF50',
    'icon_warning': '#FFC107',
    'icon_danger': '#f44336',
}

# Fontes do sistema
FONTS = {
    'title': ('Segoe UI', 20, 'bold'),
    'subtitle': ('Segoe UI', 16, 'bold'),
    'heading': ('Segoe UI', 14, 'bold'),
    'normal': ('Segoe UI', 12),
    'small': ('Segoe UI', 10),
    'small_bold': ('Segoe UI', 10, 'bold'),
}

# Tamanhos
SIZES = {
    'sidebar_width': 250,
    'topbar_height': 60,
    'border_radius': 12,
    'border_radius_small': 8,
    'padding': 20,
    'padding_small': 10,
    'margin': 10,
}

# Configuração de estilo para CustomTkinter
def configurar_estilos():
    """Configura os estilos padrão do CustomTkinter"""
    import customtkinter as ctk
    
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")