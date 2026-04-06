# app/frontend/screens/relatorios.py

import customtkinter as ctk
from app.frontend.styles import COLORS, FONTS
from app.frontend.screens.contagem_tecnico import ContagemTecnicoScreen
from app.frontend.screens.os_tecnico import OSTecnicoScreen
from app.frontend.screens.repetidos import RepetidosScreen


class RelatoriosScreen(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color=COLORS['bg_main'])
        self.pack(fill="both", expand=True)
        
        self.current_screen = None
        self.create_widgets()
    
    def create_widgets(self):
        # Título
        title = ctk.CTkLabel(
            self,
            text="📈 Relatórios",
            font=FONTS['title'],
            text_color=COLORS['text_light']
        )
        title.pack(anchor="w", padx=30, pady=(30, 10))
        
        # Subtítulo
        subtitle = ctk.CTkLabel(
            self,
            text="Selecione o tipo de relatório abaixo:",
            font=FONTS['body'],
            text_color=COLORS['text_secondary']
        )
        subtitle.pack(anchor="w", padx=30, pady=(0, 20))
        
        # Botões de seleção
        buttons_frame = ctk.CTkFrame(self, fg_color="transparent")
        buttons_frame.pack(fill="x", padx=30, pady=10)
        
        btn1 = ctk.CTkButton(
            buttons_frame,
            text="📊 Contagem por Técnico",
            font=FONTS['button'],
            fg_color=COLORS['bg_card'],
            text_color=COLORS['text_primary'],
            hover_color=COLORS['bg_table_hover'],
            border_width=1,
            border_color=COLORS['border'],
            height=45,
            corner_radius=10,
            command=lambda: self.mostrar_relatorio("contagem")
        )
        btn1.pack(side="left", padx=10, expand=True, fill="x")
        
        btn2 = ctk.CTkButton(
            buttons_frame,
            text="📋 OS por Técnico",
            font=FONTS['button'],
            fg_color=COLORS['bg_card'],
            text_color=COLORS['text_primary'],
            hover_color=COLORS['bg_table_hover'],
            border_width=1,
            border_color=COLORS['border'],
            height=45,
            corner_radius=10,
            command=lambda: self.mostrar_relatorio("os_tecnico")
        )
        btn2.pack(side="left", padx=10, expand=True, fill="x")
        
        btn3 = ctk.CTkButton(
            buttons_frame,
            text="🔄 OS Repetidas",
            font=FONTS['button'],
            fg_color=COLORS['bg_card'],
            text_color=COLORS['text_primary'],
            hover_color=COLORS['bg_table_hover'],
            border_width=1,
            border_color=COLORS['border'],
            height=45,
            corner_radius=10,
            command=lambda: self.mostrar_relatorio("repetidos")
        )
        btn3.pack(side="left", padx=10, expand=True, fill="x")
        
        # Área de conteúdo
        self.content_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.content_frame.pack(fill="both", expand=True, padx=30, pady=20)
        
        # Mensagem inicial
        self.mensagem = ctk.CTkLabel(
            self.content_frame,
            text="Clique em um botão acima para gerar o relatório",
            font=FONTS['body'],
            text_color=COLORS['text_secondary']
        )
        self.mensagem.pack(expand=True)
    
    def mostrar_relatorio(self, tipo):
        # Limpar conteúdo anterior
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        if tipo == "contagem":
            ContagemTecnicoScreen(self.content_frame)
        elif tipo == "os_tecnico":
            OSTecnicoScreen(self.content_frame)
        elif tipo == "repetidos":
            RepetidosScreen(self.content_frame)