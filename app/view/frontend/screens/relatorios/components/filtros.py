import customtkinter as ctk
from datetime import datetime
from app.view.frontend.styles import COLORS, FONTS

class FiltrosWidget:
    def __init__(self, parent, on_filtrar_callback=None, on_limpar_callback=None):
        """
        Componente de filtros (técnico, período, mês/produção)
        
        Parâmetros:
            parent: widget pai
            on_filtrar_callback: função chamada ao filtrar
            on_limpar_callback: função chamada ao limpar filtros
        """
        self.parent = parent
        self.on_filtrar_callback = on_filtrar_callback
        self.on_limpar_callback = on_limpar_callback
        
        self.meses = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", 
                     "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]
        
        self.modo = "mes"  # mes ou producao
        self.periodos_producao = []
        
        self.setup_ui()
    
    def setup_ui(self):
        """Cria a interface de filtros"""
        self.filtros_frame = ctk.CTkFrame(self.parent, fg_color="#1a1a2e", corner_radius=12)
        self.filtros_frame.pack(fill="x", pady=(0, 20))
        
        filtros_content = ctk.CTkFrame(self.filtros_frame, fg_color="transparent")
        filtros_content.pack(fill="x", padx=15, pady=10)
        
        row_filtros = ctk.CTkFrame(filtros_content, fg_color="transparent")
        row_filtros.pack(fill="x")
        
        # Técnico
        ctk.CTkLabel(row_filtros, text="Técnico:", font=('Arial', 12), text_color="#cccccc").pack(side="left", padx=(0, 10))
        
        self.tecnico_var = ctk.StringVar(value="Todos")
        self.tecnico_combo = ctk.CTkComboBox(
            row_filtros, 
            values=["Todos"],
            width=220,
            state="readonly"
        )
        self.tecnico_combo.pack(side="left", padx=(0, 20))
        
        # Período
        ctk.CTkLabel(row_filtros, text="Período:", font=('Arial', 12), text_color="#cccccc").pack(side="left", padx=(0, 10))
        
        # Frame para os selects
        self.selects_frame = ctk.CTkFrame(row_filtros, fg_color="transparent")
        self.selects_frame.pack(side="left")
        
        # Select de Mês (padrão)
        self.mes_combo = ctk.CTkComboBox(self.selects_frame, values=self.meses, width=130, state="readonly")
        self.mes_combo.pack(side="left", padx=(0, 10))
        self.mes_combo.set(self.meses[datetime.now().month - 1])
        
        ano_atual = datetime.now().year
        anos = [str(ano_atual - 1), str(ano_atual), str(ano_atual + 1)]
        self.ano_combo = ctk.CTkComboBox(self.selects_frame, values=anos, width=90, state="readonly")
        self.ano_combo.pack(side="left")
        self.ano_combo.set(str(ano_atual))
        
        # Select de Período de Produção (inicialmente oculto)
        self.periodo_combo = ctk.CTkComboBox(self.selects_frame, values=[], width=250, state="readonly")
        
        # Botão Mês/Produção
        self.modo_btn = ctk.CTkButton(
            row_filtros,
            text="📅 Mês Corrido",
            fg_color="#1a1a2e",
            border_width=1,
            border_color="#00ff88",
            width=120,
            command=self.toggle_modo
        )
        self.modo_btn.pack(side="left", padx=(20, 0))
        
        # Botão Filtrar
        ctk.CTkButton(
            row_filtros, 
            text="🔍 Filtrar", 
            fg_color="#ff6b00", 
            hover_color="#cc5500",
            font=('Arial', 12),
            width=100,
            command=self.filtrar
        ).pack(side="left", padx=(20, 0))
        
        # Botão Limpar Filtro
        ctk.CTkButton(
            row_filtros,
            text="🗑️ Limpar Filtro",
            fg_color="#555555",
            hover_color="#333333",
            width=120,
            command=self.limpar_filtro
        ).pack(side="left", padx=(20, 0))
    
    def carregar_tecnicos(self, tecnicos):
        """Carrega a lista de técnicos no combobox"""
        valores = ["Todos"] + [t['nome'] for t in tecnicos]
        self.tecnico_combo.configure(values=valores)
    
    def carregar_periodos_producao(self, periodos):
        """Carrega os períodos de produção"""
        self.periodos_producao = periodos
        self.periodo_combo.configure(values=[p['nome'] for p in periodos])
        if periodos:
            self.periodo_combo.set(periodos[0]['nome'])
    
    def toggle_modo(self):
        """Alterna entre modo Mês Corrido e Produção"""
        if self.modo == "mes":
            self.modo = "producao"
            self.modo_btn.configure(text="📊 Produção", border_color="#ff6b00", text_color="#ff6b00")
            self.mes_combo.pack_forget()
            self.ano_combo.pack_forget()
            self.periodo_combo.pack(side="left")
        else:
            self.modo = "mes"
            self.modo_btn.configure(text="📅 Mês Corrido", border_color="#00ff88", text_color="#00ff88")
            self.periodo_combo.pack_forget()
            self.mes_combo.pack(side="left", padx=(0, 10))
            self.ano_combo.pack(side="left")
        
        self.filtrar()
    
    def obter_periodo(self):
        """Retorna data_inicio e data_fim conforme o modo"""
        from datetime import datetime, timedelta
        
        if self.modo == "mes":
            mes = self.mes_combo.get()
            ano = int(self.ano_combo.get())
            mes_numero = self.meses.index(mes) + 1
            
            primeiro_dia = datetime(ano, mes_numero, 1)
            
            if mes_numero == 12:
                ultimo_dia = datetime(ano + 1, 1, 1) - timedelta(days=1)
            else:
                ultimo_dia = datetime(ano, mes_numero + 1, 1) - timedelta(days=1)
            
            return primeiro_dia.strftime("%Y-%m-%d"), ultimo_dia.strftime("%Y-%m-%d")
        else:
            nome_periodo = self.periodo_combo.get()
            for p in self.periodos_producao:
                if p['nome'] == nome_periodo:
                    return p['inicio'], p['fim']
            return self.periodos_producao[0]['inicio'], self.periodos_producao[0]['fim']
    
    def obter_id_tecnico(self):
        """Retorna o ID do técnico selecionado"""
        tecnico = self.tecnico_var.get()
        if tecnico == "Todos":
            return None
        return tecnico  # Retorna o nome, será convertido depois
    
    def filtrar(self):
        """Dispara o callback de filtro"""
        if self.on_filtrar_callback:
            data_inicio, data_fim = self.obter_periodo()
            tecnico = self.tecnico_var.get()
            self.on_filtrar_callback(data_inicio, data_fim, tecnico, self.modo)
    
    def limpar_filtro(self):
        """Limpa o filtro e dispara callback"""
        self.tecnico_var.set("Todos")
        if self.on_limpar_callback:
            self.on_limpar_callback()
        self.filtrar()
    
    def get_frame(self):
        """Retorna o frame dos filtros"""
        return self.filtros_frame