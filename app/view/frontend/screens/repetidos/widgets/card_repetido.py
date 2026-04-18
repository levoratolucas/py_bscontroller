import customtkinter as ctk
from app.view.frontend.styles import COLORS, FONTS

class CardRepetido(ctk.CTkFrame):
    def __init__(self, parent, dados, on_status_change=None):
        """
        dados: {
            'id': 1,
            'id_os': 49,
            'id_os_referencia': 48,
            'procedente': 0,
            'numero_repetido': '1233000',
            'wan_piloto': 'abb',
            'data_repetido': '2026-04-12',
            'hora_repetido': '17:00',
            'carimbo_repetido': '...',
            'tecnico_repetido': 'João',
            'numero_referencia': '1230000',
            'data_referencia': '2026-03-30',
            'hora_referencia': '17:00',
            'carimbo_referencia': '...',
            'tecnico_referencia': 'Maria',
            'dias_diferenca': 13
        }
        """
        super().__init__(parent, fg_color=COLORS['bg_card'], corner_radius=12, border_width=1, border_color=COLORS['border'])
        self.dados = dados
        self.on_status_change = on_status_change
        
        self.setup_ui()
    
    def setup_ui(self):
        # Container principal
        self.pack(fill="x", pady=8, padx=5)
        
        # Cabeçalho com WAN e diferença de dias
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.pack(fill="x", padx=15, pady=(10, 5))
        
        # WAN/Piloto
        ctk.CTkLabel(
            header_frame,
            text=f"🌐 {self.dados['wan_piloto']}",
            font=FONTS['subtitle'],
            text_color=COLORS['warning']
        ).pack(side="left")
        
        # Dias de diferença
        dias = self.dados.get('dias_diferenca', '?')
        cor_dias = COLORS['success'] if dias <= 15 else COLORS['warning'] if dias <= 25 else COLORS['danger']
        ctk.CTkLabel(
            header_frame,
            text=f"⚠️ {dias} dias desde anterior",
            font=FONTS['small'],
            text_color=cor_dias
        ).pack(side="right")
        
        # Linha divisória
        ctk.CTkFrame(self, height=1, fg_color=COLORS['border']).pack(fill="x", padx=15, pady=5)
        
        # Conteúdo: OS Repetida vs OS Referência
        content_frame = ctk.CTkFrame(self, fg_color="transparent")
        content_frame.pack(fill="x", padx=15, pady=10)
        
        # Colunas
        content_frame.grid_columnconfigure(0, weight=1)
        content_frame.grid_columnconfigure(1, weight=0)
        content_frame.grid_columnconfigure(2, weight=1)
        
        # === OS REPETIDA (esquerda) ===
        repetido_frame = ctk.CTkFrame(content_frame, fg_color=COLORS['bg_dark'], corner_radius=8)
        repetido_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10), pady=5)
        
        ctk.CTkLabel(
            repetido_frame,
            text="🔴 OS REPETIDA",
            font=FONTS['small_bold'],
            text_color=COLORS['danger']
        ).pack(anchor="w", padx=10, pady=(5, 0))
        
        ctk.CTkLabel(
            repetido_frame,
            text=f"Nº: {self.dados['numero_repetido']}",
            font=FONTS['normal'],
            text_color=COLORS['text_light']
        ).pack(anchor="w", padx=10, pady=2)
        
        ctk.CTkLabel(
            repetido_frame,
            text=f"Data: {self.dados['data_repetido']} {self.dados['hora_repetido']}",
            font=FONTS['small'],
            text_color=COLORS['text_secondary']
        ).pack(anchor="w", padx=10, pady=2)
        
        ctk.CTkLabel(
            repetido_frame,
            text=f"Técnico: {self.dados['tecnico_repetido']}",
            font=FONTS['small'],
            text_color=COLORS['text_secondary']
        ).pack(anchor="w", padx=10, pady=2)
        
        # Carimbo (se tiver)
        if self.dados.get('carimbo_repetido'):
            carimbo_text = self.dados['carimbo_repetido'][:100] + "..." if len(self.dados['carimbo_repetido']) > 100 else self.dados['carimbo_repetido']
            ctk.CTkLabel(
                repetido_frame,
                text=f"📝 {carimbo_text}",
                font=FONTS['small'],
                text_color=COLORS['text_muted'],
                wraplength=300,
                justify="left"
            ).pack(anchor="w", padx=10, pady=(5, 10))
        
        # === SETA (centro) ===
        seta_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        seta_frame.grid(row=0, column=1, sticky="nsew")
        
        ctk.CTkLabel(
            seta_frame,
            text="▶",
            font=('Arial', 24),
            text_color=COLORS['primary']
        ).pack(expand=True)
        
        # === OS REFERÊNCIA (direita) ===
        referencia_frame = ctk.CTkFrame(content_frame, fg_color=COLORS['bg_dark'], corner_radius=8)
        referencia_frame.grid(row=0, column=2, sticky="nsew", padx=(10, 0), pady=5)
        
        ctk.CTkLabel(
            referencia_frame,
            text="🟢 OS REFERÊNCIA",
            font=FONTS['small_bold'],
            text_color=COLORS['success']
        ).pack(anchor="w", padx=10, pady=(5, 0))
        
        ctk.CTkLabel(
            referencia_frame,
            text=f"Nº: {self.dados['numero_referencia']}",
            font=FONTS['normal'],
            text_color=COLORS['text_light']
        ).pack(anchor="w", padx=10, pady=2)
        
        ctk.CTkLabel(
            referencia_frame,
            text=f"Data: {self.dados['data_referencia']} {self.dados['hora_referencia']}",
            font=FONTS['small'],
            text_color=COLORS['text_secondary']
        ).pack(anchor="w", padx=10, pady=2)
        
        ctk.CTkLabel(
            referencia_frame,
            text=f"Técnico: {self.dados['tecnico_referencia']}",
            font=FONTS['small'],
            text_color=COLORS['text_secondary']
        ).pack(anchor="w", padx=10, pady=2)
        
        if self.dados.get('carimbo_referencia'):
            carimbo_text = self.dados['carimbo_referencia'][:100] + "..." if len(self.dados['carimbo_referencia']) > 100 else self.dados['carimbo_referencia']
            ctk.CTkLabel(
                referencia_frame,
                text=f"📝 {carimbo_text}",
                font=FONTS['small'],
                text_color=COLORS['text_muted'],
                wraplength=300,
                justify="left"
            ).pack(anchor="w", padx=10, pady=(5, 10))
        
        # === BOTÕES DE AÇÃO (procedente) ===
        botoes_frame = ctk.CTkFrame(self, fg_color="transparent")
        botoes_frame.pack(fill="x", padx=15, pady=(0, 10))
        
        status_atual = self.dados.get('procedente', 0)
        
        # Botão PROCEDE
        self.btn_procede = ctk.CTkButton(
            botoes_frame,
            text="✅ PROCEDE",
            fg_color=COLORS['success'] if status_atual == 1 else COLORS['bg_input'],
            hover_color=COLORS['success_dark'],
            width=100,
            command=lambda: self.atualizar_status(1)
        )
        self.btn_procede.pack(side="left", padx=5)
        
        # Botão NÃO PROCEDE
        self.btn_nao_procede = ctk.CTkButton(
            botoes_frame,
            text="❌ NÃO PROCEDE",
            fg_color=COLORS['danger'] if status_atual == 2 else COLORS['bg_input'],
            hover_color=COLORS['danger_dark'],
            width=120,
            command=lambda: self.atualizar_status(2)
        )
        self.btn_nao_procede.pack(side="left", padx=5)
        
        # Botão PENDENTE (reset)
        self.btn_pendente = ctk.CTkButton(
            botoes_frame,
            text="⏳ PENDENTE",
            fg_color=COLORS['warning'] if status_atual == 0 else COLORS['bg_input'],
            hover_color=COLORS['warning_dark'],
            width=100,
            command=lambda: self.atualizar_status(0)
        )
        self.btn_pendente.pack(side="left", padx=5)
        
        # Status atual
        status_texto = {0: "Pendente", 1: "Procede", 2: "Não Procede"}
        status_cor = {0: COLORS['warning'], 1: COLORS['success'], 2: COLORS['danger']}
        
        ctk.CTkLabel(
            botoes_frame,
            text=f"Status: {status_texto.get(status_atual, 'Desconhecido')}",
            font=FONTS['small_bold'],
            text_color=status_cor.get(status_atual, COLORS['text_secondary'])
        ).pack(side="right", padx=10)
    
    def atualizar_status(self, novo_status):
        """Atualiza o status do repetido"""
        if self.on_status_change:
            self.on_status_change(self.dados['id'], novo_status)
        
        # Atualizar cores dos botões
        self.btn_procede.configure(fg_color=COLORS['success'] if novo_status == 1 else COLORS['bg_input'])
        self.btn_nao_procede.configure(fg_color=COLORS['danger'] if novo_status == 2 else COLORS['bg_input'])
        self.btn_pendente.configure(fg_color=COLORS['warning'] if novo_status == 0 else COLORS['bg_input'])
        
        self.dados['procedente'] = novo_status