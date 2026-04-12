import customtkinter as ctk
from datetime import datetime
from app.view.frontend.styles import COLORS, FONTS


class SeletorOrdemServico:
    def __init__(self, parent):
        self.parent = parent
        self.widgets = {}
        self.on_change_callback = None
        self.modo = "mes"  # "mes" ou "producao"
        
        self.setup_ui()
    
    def setup_ui(self):
        frame = ctk.CTkFrame(self.parent, fg_color="#1a1a2e", corner_radius=12)
        frame.pack(fill="x", pady=(0, 20))
        
        content = ctk.CTkFrame(frame, fg_color="transparent")
        content.pack(fill="x", padx=15, pady=10)
        
        # ================= LINHA 1: BOTÕES DE TROCA =================
        botoes_frame = ctk.CTkFrame(content, fg_color="transparent")
        botoes_frame.pack(fill="x", pady=(0, 10))
        
        self.btn_mes = ctk.CTkButton(
            botoes_frame,
            text="📅 Mês Corrido",
            fg_color="#ff6b00",
            width=140,
            height=35,
            font=('Arial', 12, 'bold'),
            command=self.ativar_mes
        )
        self.btn_mes.pack(side="left", padx=(0, 10))
        
        self.btn_producao = ctk.CTkButton(
            botoes_frame,
            text="📊 Produção",
            fg_color="#1a1a2e",
            border_width=1,
            border_color="#00ff88",
            width=140,
            height=35,
            font=('Arial', 12, 'bold'),
            command=self.ativar_producao
        )
        self.btn_producao.pack(side="left")
        
        # ================= LINHA 2: SELECTS =================
        self.selects_frame = ctk.CTkFrame(content, fg_color="transparent")
        self.selects_frame.pack(fill="x", pady=(10, 10))
        
        # Selects de Mês (padrão)
        self.mes_frame = ctk.CTkFrame(self.selects_frame, fg_color="transparent")
        
        ctk.CTkLabel(self.mes_frame, text="Mês:", font=('Arial', 12), text_color="#cccccc", width=40).pack(side="left", padx=(0, 5))
        
        self.meses = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", 
                     "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]
        
        self.mes_combo = ctk.CTkComboBox(self.mes_frame, values=self.meses, width=120, state="readonly")
        self.mes_combo.pack(side="left", padx=(0, 15))
        self.mes_combo.set(self.meses[datetime.now().month - 1])
        
        ctk.CTkLabel(self.mes_frame, text="Ano:", font=('Arial', 12), text_color="#cccccc", width=40).pack(side="left", padx=(0, 5))
        
        ano_atual = datetime.now().year
        anos = [str(ano_atual - 1), str(ano_atual), str(ano_atual + 1)]
        self.ano_combo = ctk.CTkComboBox(self.mes_frame, values=anos, width=90, state="readonly")
        self.ano_combo.pack(side="left")
        self.ano_combo.set(str(ano_atual))
        
        self.mes_frame.pack(side="left")
        
        # Select de Período de Produção (inicialmente oculto)
        self.producao_frame = ctk.CTkFrame(self.selects_frame, fg_color="transparent")
        
        ctk.CTkLabel(self.producao_frame, text="Período:", font=('Arial', 12), text_color="#cccccc", width=60).pack(side="left", padx=(0, 5))
        
        self.periodo_combo = ctk.CTkComboBox(self.producao_frame, values=[], width=250, state="readonly")
        self.periodo_combo.pack(side="left")
        
        # ================= LINHA 3: TÉCNICO E STATUS =================
        filtros_frame = ctk.CTkFrame(content, fg_color="transparent")
        filtros_frame.pack(fill="x", pady=(0, 10))
        
        # Técnico
        tec_frame = ctk.CTkFrame(filtros_frame, fg_color="transparent")
        tec_frame.pack(side="left", padx=(0, 20))
        
        ctk.CTkLabel(tec_frame, text="Técnico:", font=('Arial', 12), text_color="#cccccc", width=60).pack(side="left", padx=(0, 5))
        
        self.tecnico_combo = ctk.CTkComboBox(tec_frame, values=["Todos"], width=180, state="readonly")
        self.tecnico_combo.pack(side="left")
        
        # Status
        status_frame = ctk.CTkFrame(filtros_frame, fg_color="transparent")
        status_frame.pack(side="left")
        
        ctk.CTkLabel(status_frame, text="Status:", font=('Arial', 12), text_color="#cccccc", width=50).pack(side="left", padx=(0, 5))
        
        self.status_var = ctk.StringVar(value="Ambos")
        self.status_combo = ctk.CTkComboBox(
            status_frame, 
            values=["Ambos", "Concluído", "Suspenso"],
            width=120,
            state="readonly"
        )
        self.status_combo.pack(side="left")
        
        # ================= LINHA 4: BOTÃO APLICAR =================
        aplicar_frame = ctk.CTkFrame(content, fg_color="transparent")
        aplicar_frame.pack(fill="x", pady=(5, 0))
        
        self.btn_aplicar = ctk.CTkButton(
            aplicar_frame,
            text="🔍 Aplicar Filtros",
            fg_color="#ff6b00",
            hover_color="#cc5500",
            width=150,
            height=35,
            font=('Arial', 12, 'bold'),
            command=self.on_change
        )
        self.btn_aplicar.pack(side="right")
        
        # Bind dos eventos (apenas para atualizar os selects, não aplica automaticamente)
        self.mes_combo.bind("<<ComboboxSelected>>", self.on_select_change)
        self.ano_combo.bind("<<ComboboxSelected>>", self.on_select_change)
        self.periodo_combo.bind("<<ComboboxSelected>>", self.on_select_change)
        self.tecnico_combo.bind("<<ComboboxSelected>>", self.on_select_change)
        self.status_combo.bind("<<ComboboxSelected>>", self.on_select_change)
    
    def on_select_change(self, event=None):
        """Apenas marca que algo mudou, mas não aplica (só visual)"""
        pass
    
    def ativar_mes(self):
        self.modo = "mes"
        self.btn_mes.configure(fg_color="#ff6b00")
        self.btn_producao.configure(fg_color="#1a1a2e", border_color="#00ff88")
        
        self.mes_frame.pack(side="left")
        self.producao_frame.pack_forget()
    
    def ativar_producao(self):
        self.modo = "producao"
        self.btn_mes.configure(fg_color="#1a1a2e")
        self.btn_producao.configure(fg_color="#ff6b00", border_color="#ff6b00")
        
        self.mes_frame.pack_forget()
        self.producao_frame.pack(side="left")
    
    def carregar_periodos_producao(self, periodos):
        """Carrega os períodos de produção"""
        self.periodo_combo.configure(values=[p['nome'] for p in periodos])
        if periodos:
            self.periodo_combo.set(periodos[0]['nome'])
    
    def carregar_tecnicos(self, tecnicos):
        """Carrega a lista de técnicos"""
        valores = ["Todos"] + [t['nome'] for t in tecnicos]
        self.tecnico_combo.configure(values=valores)
        self.tecnico_combo.set("Todos")
    
    def get_seletor(self, nome):
        if nome == 'mes':
            return self.mes_combo
        elif nome == 'ano':
            return self.ano_combo
        elif nome == 'tecnico':
            return self.tecnico_combo
        elif nome == 'periodo':
            return self.periodo_combo
        elif nome == 'status':
            return self.status_combo
        return None
    
    def get_status_filtro(self):
        status = self.status_var.get()
        if status == "Concluído":
            return 1
        elif status == "Suspenso":
            return 0
        return None
    
    def get_modo(self):
        return self.modo
    
    def set_on_change(self, callback):
        self.on_change_callback = callback
    
    def on_change(self, event=None):
        if self.on_change_callback:
            self.on_change_callback()