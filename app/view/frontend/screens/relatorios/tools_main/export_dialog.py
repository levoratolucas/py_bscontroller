import customtkinter as ctk
from datetime import datetime
from app.view.frontend.styles import COLORS, FONTS
from app.view.frontend.screens.relatorios.exportar import ExportadorRelatorio
from app.view.frontend.screens.relatorios.tools_main.csv import CSVExportador
from app.view.frontend.screens.relatorios.tools_main.pdf import PDFExportador

class ExportDialog:
    """Gerencia o diálogo de exportação de relatório"""
    
    def __init__(self, parent, relatorio_controller, os_controller, dados_relatorio):
        self.parent = parent
        self.relatorio_controller = relatorio_controller
        self.os_controller = os_controller
        self.dados_relatorio = dados_relatorio
        self.dialog = None
        self.periodo_rel_tipo = 'mes'
    
    def abrir(self):
        self.dialog = ctk.CTkToplevel(self.parent)
        self.dialog.title("Exportar Relatório")
        self.dialog.geometry("600x550")
        self.dialog.transient(self.parent)
        self.dialog.grab_set()
        
        self.dialog.update_idletasks()
        x = (self.dialog.winfo_screenwidth() // 2) - (600 // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (550 // 2)
        self.dialog.geometry(f"+{x}+{y}")
        
        main_frame = ctk.CTkFrame(self.dialog, fg_color="#0a0a0a")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        ctk.CTkLabel(
            main_frame,
            text="📊 EXPORTAR RELATÓRIO",
            font=('Arial', 20, 'bold'),
            text_color="#00ff88"
        ).pack(anchor="w", pady=(0, 20))
        
        # Tipo de exportação
        self._criar_tipo_exportacao(main_frame)
        
        # Período
        self._criar_periodo(main_frame)
        
        # Técnico
        self._criar_tecnico(main_frame)
        
        # Botões
        self._criar_botoes(main_frame)
        
        self.periodo_rel_tipo = 'mes'
    
    def _criar_tipo_exportacao(self, parent):
        ctk.CTkLabel(
            parent,
            text="Tipo de Exportação:",
            font=('Arial', 14, 'bold'),
            text_color="#cccccc"
        ).pack(anchor="w", pady=(0, 5))
        
        self.tipo_var = ctk.StringVar(value="pdf")
        
        tipo_frame = ctk.CTkFrame(parent, fg_color="transparent")
        tipo_frame.pack(fill="x", pady=(0, 15))
        
        ctk.CTkRadioButton(tipo_frame, text="📄 PDF (Relatório Completo)", variable=self.tipo_var, value="pdf").pack(anchor="w", pady=2)
        ctk.CTkRadioButton(tipo_frame, text="📊 CSV (Lista de OS)", variable=self.tipo_var, value="csv_os").pack(anchor="w", pady=2)
        ctk.CTkRadioButton(tipo_frame, text="📈 CSV (Médias - APU/Ofensor)", variable=self.tipo_var, value="csv_medias").pack(anchor="w", pady=2)
    
    def _criar_periodo(self, parent):
        ctk.CTkLabel(
            parent,
            text="Período:",
            font=('Arial', 14, 'bold'),
            text_color="#cccccc"
        ).pack(anchor="w", pady=(0, 5))
        
        periodo_frame = ctk.CTkFrame(parent, fg_color="transparent")
        periodo_frame.pack(fill="x", pady=(0, 15))
        
        self.periodo_rel_mes = ctk.CTkButton(
            periodo_frame,
            text="📅 Mês Corrido",
            fg_color="#ff6b00",
            width=140,
            command=lambda: self._toggle_periodo('mes')
        )
        self.periodo_rel_mes.pack(side="left", padx=(0, 10))
        
        self.periodo_rel_producao = ctk.CTkButton(
            periodo_frame,
            text="📊 Produção",
            fg_color="#1a1a2e",
            border_width=1,
            border_color="#00ff88",
            width=140,
            command=lambda: self._toggle_periodo('producao')
        )
        self.periodo_rel_producao.pack(side="left")
        
        # Seletor de mês
        self.rel_mes_frame = ctk.CTkFrame(periodo_frame, fg_color="transparent")
        self.rel_mes_frame.pack(side="left", padx=(20, 0))
        
        ctk.CTkLabel(self.rel_mes_frame, text="Mês:", font=('Arial', 12), text_color="#cccccc").pack(side="left", padx=(0, 5))
        
        meses = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", 
                "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]
        
        self.rel_mes_combo = ctk.CTkComboBox(self.rel_mes_frame, values=meses, width=130, state="readonly")
        self.rel_mes_combo.pack(side="left", padx=(0, 15))
        self.rel_mes_combo.set(meses[datetime.now().month - 1])
        
        ctk.CTkLabel(self.rel_mes_frame, text="Ano:", font=('Arial', 12), text_color="#cccccc").pack(side="left", padx=(0, 5))
        
        ano_atual = datetime.now().year
        anos = [str(ano_atual - 1), str(ano_atual), str(ano_atual + 1)]
        self.rel_ano_combo = ctk.CTkComboBox(self.rel_mes_frame, values=anos, width=90, state="readonly")
        self.rel_ano_combo.pack(side="left")
        self.rel_ano_combo.set(str(ano_atual))
        
        # Seletor de período de produção (oculto inicialmente)
        self.rel_producao_frame = ctk.CTkFrame(periodo_frame, fg_color="transparent")
        
        ctk.CTkLabel(self.rel_producao_frame, text="Período:", font=('Arial', 12), text_color="#cccccc").pack(side="left", padx=(0, 5))
        
        periodos = self.dados_relatorio.get_periodos_producao()
        self.rel_periodo_combo = ctk.CTkComboBox(self.rel_producao_frame, values=[p['nome'] for p in periodos], width=250, state="readonly")
        self.rel_periodo_combo.pack(side="left")
        if periodos:
            self.rel_periodo_combo.set(periodos[0]['nome'])
        
        self.rel_producao_frame.pack_forget()
    
    def _criar_tecnico(self, parent):
        ctk.CTkLabel(
            parent,
            text="Técnico:",
            font=('Arial', 14, 'bold'),
            text_color="#cccccc"
        ).pack(anchor="w", pady=(0, 5))
        
        tecnicos = self.dados_relatorio.get_tecnicos()
        tecnicos_nomes = ["Todos"] + [t['nome'] for t in tecnicos]
        
        self.rel_tecnico_combo = ctk.CTkComboBox(parent, values=tecnicos_nomes, width=300, state="readonly")
        self.rel_tecnico_combo.pack(anchor="w", pady=(0, 20))
        self.rel_tecnico_combo.set("Todos")
    
    def _criar_botoes(self, parent):
        btn_frame = ctk.CTkFrame(parent, fg_color="transparent")
        btn_frame.pack(fill="x")
        
        ctk.CTkButton(
            btn_frame,
            text="📄 Exportar",
            fg_color="#00cc66",
            hover_color="#009944",
            font=('Arial', 13, 'bold'),
            width=150,
            command=self._exportar
        ).pack(side="left", padx=(0, 10))
        
        ctk.CTkButton(
            btn_frame,
            text="Cancelar",
            fg_color="#ff3333",
            hover_color="#cc0000",
            font=('Arial', 13, 'bold'),
            width=150,
            command=self._fechar
        ).pack(side="left")
    
    def _toggle_periodo(self, tipo):
        if tipo == 'mes':
            self.periodo_rel_mes.configure(fg_color="#ff6b00")
            self.periodo_rel_producao.configure(fg_color="#1a1a2e")
            self.rel_mes_frame.pack(side="left", padx=(20, 0))
            self.rel_producao_frame.pack_forget()
            self.periodo_rel_tipo = 'mes'
        else:
            self.periodo_rel_mes.configure(fg_color="#1a1a2e")
            self.periodo_rel_producao.configure(fg_color="#ff6b00")
            self.rel_mes_frame.pack_forget()
            self.rel_producao_frame.pack(side="left", padx=(20, 0))
            self.periodo_rel_tipo = 'producao'
    
    def _exportar(self):
        if self.periodo_rel_tipo == 'mes':
            mes = self.rel_mes_combo.get()
            ano = self.rel_ano_combo.get()
            periodo_nome = None
        else:
            mes = None
            ano = None
            periodo_nome = self.rel_periodo_combo.get()
        
        tecnico_nome = self.rel_tecnico_combo.get()
        
        exportador = ExportadorRelatorio(self.parent, self.relatorio_controller, self.os_controller)
        exportador.carregar_periodos_producao()
        
        dados = exportador.obter_dados_periodo(
            self.periodo_rel_tipo, mes, ano, periodo_nome, tecnico_nome
        )
        
        self._fechar()
        
        if self.tipo_var.get() == "pdf":
            PDFExportador.exportar_relatorio(dados)
        elif self.tipo_var.get() == "csv_os":
            CSVExportador.exportar_os(dados)
        elif self.tipo_var.get() == "csv_medias":
            data_inicio = dados['data_inicio']
            data_fim = dados['data_fim']
            id_tecnico = dados['id_tecnico']
            
            apu_individual = self.relatorio_controller.get_apu_individual(data_inicio, data_fim, id_tecnico)
            metricas = self.relatorio_controller.get_metricas_radar(data_inicio, data_fim, id_tecnico)
            resumo = self.relatorio_controller.get_resumo_periodo(data_inicio, data_fim, id_tecnico)
            
            CSVExportador.exportar_medias(apu_individual, metricas, resumo)
    
    def _fechar(self):
        if self.dialog:
            self.dialog.destroy()