import customtkinter as ctk
from app.view.frontend.styles import COLORS, FONTS

class BotoesAcao:
    def __init__(self, parent, on_exportar_callback=None):
        """
        Componente de botões de ação
        
        Parâmetros:
            parent: widget pai
            on_exportar_callback: função chamada ao clicar em exportar
        """
        self.parent = parent
        self.on_exportar_callback = on_exportar_callback
        
        self.setup_ui()
    
    def setup_ui(self):
        """Cria os botões de ação"""
        self.btn_frame = ctk.CTkFrame(self.parent, fg_color="transparent")
        self.btn_frame.pack(fill="x", pady=(0, 15))
        
        self.btn_exportar = ctk.CTkButton(
            self.btn_frame,
            text="📊 Gerar Relatório",
            fg_color="#00cc66",
            hover_color="#009944",
            font=('Arial', 13, 'bold'),
            width=180,
            height=38,
            command=self.exportar
        )
        self.btn_exportar.pack(side="right")
    
    def exportar(self):
        """Dispara o callback de exportação"""
        if self.on_exportar_callback:
            self.on_exportar_callback()
    
    def get_frame(self):
        """Retorna o frame dos botões"""
        return self.btn_frame