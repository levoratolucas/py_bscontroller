# Cores e estilos
COLORS = {
    'primary': '#2c3e50',
    'secondary': '#34495e',
    'success': '#27ae60',
    'danger': '#e74c3c',
    'warning': '#f39c12',
    'info': '#3498db',
    'light': '#ecf0f1',
    'dark': '#2c3e50',
    'white': '#ffffff'
}

FONTS = {
    'title': ('Arial', 16, 'bold'),
    'subtitle': ('Arial', 12, 'bold'),
    'normal': ('Arial', 10),
    'small': ('Arial', 9)
}

def configurar_estilos():
    """Configurar estilos para o ttk"""
    from tkinter import ttk
    style = ttk.Style()
    
    style.theme_use('clam')
    
    style.configure('TButton', font=FONTS['normal'], padding=5)
    style.configure('TLabel', font=FONTS['normal'])
    style.configure('TEntry', font=FONTS['normal'])
    style.configure('TFrame', background=COLORS['light'])
    style.configure('TLabelframe', font=FONTS['subtitle'])
    style.configure('Treeview', font=FONTS['normal'], rowheight=25)
    style.configure('Treeview.Heading', font=FONTS['subtitle'])