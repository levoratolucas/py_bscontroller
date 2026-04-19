import customtkinter as ctk
from app.view.frontend.styles import COLORS, FONTS

class AreaDetalhes:
    def __init__(self, parent):
        """
        Componente de área de detalhes (OS Selecionada e OS Referência)
        
        Parâmetros:
            parent: widget pai
        """
        self.parent = parent
        self.texto_selecionada = None
        self.texto_referencia = None
        
        self.setup_ui()
    
    def setup_ui(self):
        """Cria a área de detalhes"""
        self.wrapper = ctk.CTkFrame(self.parent, fg_color="#0f0f0f", corner_radius=12, 
                                     border_width=1, border_color="#2a2a2a")
        self.wrapper.pack(fill="both", expand=True)
        
        ctk.CTkLabel(
            self.wrapper,
            text="📝 DETALHES DA OS",
            font=('Arial', 14, 'bold'),
            text_color="#00ff88"
        ).pack(anchor="w", padx=15, pady=(10, 5))
        
        container = ctk.CTkFrame(self.wrapper, fg_color="transparent")
        container.pack(fill="both", expand=True, padx=15, pady=10)
        
        # Frame para OS Selecionada (borda amarela)
        self.frame_selecionada = ctk.CTkFrame(container, fg_color="#1a1a2e", corner_radius=12, 
                                               border_width=2, border_color="#ffaa00")
        self.frame_selecionada.pack(fill="x", pady=(0, 15))
        
        ctk.CTkLabel(
            self.frame_selecionada,
            text="🟡 OS SELECIONADA",
            font=('Arial', 13, 'bold'),
            text_color="#ffaa00"
        ).pack(anchor="w", padx=10, pady=(5, 0))
        
        self.texto_selecionada = ctk.CTkTextbox(self.frame_selecionada, height=200, 
                                                 font=('Arial', 12), fg_color="#1a1a2e", border_width=0)
        self.texto_selecionada.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Frame para OS Referência (borda verde)
        self.frame_referencia = ctk.CTkFrame(container, fg_color="#1a1a2e", corner_radius=12, 
                                              border_width=2, border_color="#00cc66")
        self.frame_referencia.pack(fill="x", pady=(0, 0))
        
        ctk.CTkLabel(
            self.frame_referencia,
            text="🟢 OS REFERÊNCIA",
            font=('Arial', 13, 'bold'),
            text_color="#00cc66"
        ).pack(anchor="w", padx=10, pady=(5, 0))
        
        self.texto_referencia = ctk.CTkTextbox(self.frame_referencia, height=200, 
                                                font=('Arial', 12), fg_color="#1a1a2e", border_width=0)
        self.texto_referencia.pack(fill="both", expand=True, padx=10, pady=5)
    
    def set_detalhes(self, texto_selecionada, texto_referencia):
        """Atualiza os textos de detalhes"""
        self.texto_selecionada.delete("1.0", "end")
        self.texto_selecionada.insert("1.0", texto_selecionada)
        
        self.texto_referencia.delete("1.0", "end")
        self.texto_referencia.insert("1.0", texto_referencia)
    
    def limpar(self):
        """Limpa os textos"""
        self.texto_selecionada.delete("1.0", "end")
        self.texto_referencia.delete("1.0", "end")
    
    def get_frame(self):
        """Retorna o frame wrapper"""
        return self.wrapper