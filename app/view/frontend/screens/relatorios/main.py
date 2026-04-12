import customtkinter as ctk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
from app.view.frontend.styles import COLORS, FONTS
from app.controller.relatorio_controller import RelatorioController
from app.controller.ordem_servico_controller import OrdemServicoController
from app.view.frontend.screens.relatorios.exportar import ExportadorRelatorio


class RelatoriosScreen(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent, fg_color="transparent")
        self.pack(fill="both", expand=True)
        
        self.app = app
        self.relatorio_controller = RelatorioController()
        self.os_controller = OrdemServicoController()
        self.dados_atuais = []
        self.modo = "mes"
        self.periodos_producao = []
        self.meses = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", 
                     "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]
        
        self.setup_ui()
        self.carregar_tecnicos()
        self.carregar_periodos_producao()
        self.carregar_dados()

    def setup_ui(self):
        # ================= MAIN FRAME =================
        main_frame = ctk.CTkFrame(self, fg_color="#0a0a0a")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # ================= TÍTULO =================
        titulo_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        titulo_frame.pack(fill="x", pady=(0, 20))
        
        ctk.CTkLabel(
            titulo_frame,
            text="📊 RELATÓRIOS - REPETIDOS",
            font=('Arial', 22, 'bold'),
            text_color="#00ff88"
        ).pack(anchor="w")
        
        ctk.CTkLabel(
            titulo_frame,
            text="Análise de WANs repetidos e ofensores",
            font=('Arial', 12),
            text_color="#666666"
        ).pack(anchor="w")

        # ================= BOTÃO GERAR RELATÓRIO =================
        btn_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        btn_frame.pack(fill="x", pady=(0, 15))
        
        self.btn_gerar_relatorio = ctk.CTkButton(
            btn_frame,
            text="📊 Gerar Relatório",
            fg_color="#00cc66",
            hover_color="#009944",
            font=('Arial', 13, 'bold'),
            width=180,
            height=38,
            command=self.abrir_janela_relatorio
        )
        self.btn_gerar_relatorio.pack(side="right")

        # ================= 4 CARDS NO TOPO =================
        cards_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        cards_frame.pack(fill="x", pady=(0, 25))
        
        for i in range(4):
            cards_frame.grid_columnconfigure(i, weight=1)
        
        # Card 1 - REPETIDO (amarelo)
        card1 = ctk.CTkFrame(cards_frame, fg_color="#1a1a2e", corner_radius=12, border_width=1, border_color="#ff6b00")
        card1.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        
        ctk.CTkLabel(card1, text="🔄", font=('Arial', 40), text_color="#ff6b00").pack(pady=(15, 5))
        ctk.CTkLabel(card1, text="REPETIDO", font=('Arial', 16, 'bold'), text_color="#ffffff").pack()
        self.card_repetido_valor = ctk.CTkLabel(card1, text="0", font=('Arial', 32, 'bold'), text_color="#ff6b00")
        self.card_repetido_valor.pack(pady=(5, 15))
        
        # Card 2 - TOTAL OS (azul)
        card2 = ctk.CTkFrame(cards_frame, fg_color="#1a1a2e", corner_radius=12, border_width=1, border_color="#0088ff")
        card2.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
        
        ctk.CTkLabel(card2, text="📋", font=('Arial', 40), text_color="#0088ff").pack(pady=(15, 5))
        ctk.CTkLabel(card2, text="TOTAL OS", font=('Arial', 16, 'bold'), text_color="#ffffff").pack()
        self.card_total_valor = ctk.CTkLabel(card2, text="0", font=('Arial', 32, 'bold'), text_color="#0088ff")
        self.card_total_valor.pack(pady=(5, 15))
        
        # Card 3 - OFENSOR % (vermelho)
        card3 = ctk.CTkFrame(cards_frame, fg_color="#1a1a2e", corner_radius=12, border_width=1, border_color="#ff3333")
        card3.grid(row=0, column=2, sticky="nsew", padx=5, pady=5)
        
        ctk.CTkLabel(card3, text="⚠️", font=('Arial', 40), text_color="#ff3333").pack(pady=(15, 5))
        ctk.CTkLabel(card3, text="OFENSOR %", font=('Arial', 16, 'bold'), text_color="#ffffff").pack()
        self.card_ofensor_valor = ctk.CTkLabel(card3, text="0%", font=('Arial', 32, 'bold'), text_color="#ff3333")
        self.card_ofensor_valor.pack(pady=(5, 15))
        
        # Card 4 - TÉCNICOS (verde)
        card4 = ctk.CTkFrame(cards_frame, fg_color="#1a1a2e", corner_radius=12, border_width=1, border_color="#00cc66")
        card4.grid(row=0, column=3, sticky="nsew", padx=5, pady=5)
        
        ctk.CTkLabel(card4, text="👤", font=('Arial', 40), text_color="#00cc66").pack(pady=(15, 5))
        ctk.CTkLabel(card4, text="TÉCNICOS", font=('Arial', 16, 'bold'), text_color="#ffffff").pack()
        self.card_tecnicos_valor = ctk.CTkLabel(card4, text="0", font=('Arial', 32, 'bold'), text_color="#00cc66")
        self.card_tecnicos_valor.pack(pady=(5, 15))

        # ================= FILTROS =================
        filtros_frame = ctk.CTkFrame(main_frame, fg_color="#1a1a2e", corner_radius=12)
        filtros_frame.pack(fill="x", pady=(0, 20))
        
        filtros_content = ctk.CTkFrame(filtros_frame, fg_color="transparent")
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
        
        # Frame para os selects (Mês e Produção)
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
        
        # Botão Filtrar
        ctk.CTkButton(
            row_filtros, 
            text="🔍 Filtrar", 
            fg_color="#ff6b00", 
            hover_color="#cc5500",
            font=('Arial', 12),
            width=100,
            command=self.aplicar_filtro
        ).pack(side="left", padx=(20, 0))
        
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

        # ================= CONTAINER PRINCIPAL =================
        main_container = ctk.CTkFrame(main_frame, fg_color="transparent")
        main_container.pack(fill="both", expand=True)
        
        main_container.grid_columnconfigure(0, weight=30)
        main_container.grid_columnconfigure(1, weight=70)
        main_container.grid_rowconfigure(0, weight=1)
        
        # ================= TABELA (30%) =================
        table_wrapper = ctk.CTkFrame(main_container, fg_color="#0f0f0f", corner_radius=12, border_width=1, border_color="#2a2a2a")
        table_wrapper.grid(row=0, column=0, sticky="nsew", padx=(0, 10), pady=0)
        
        ctk.CTkLabel(
            table_wrapper,
            text="📋 Histórico de Repetições",
            font=('Arial', 12, 'bold'),
            text_color="#00ff88"
        ).pack(anchor="w", padx=15, pady=(10, 5))
        
        table_container = ctk.CTkFrame(table_wrapper, fg_color="transparent")
        table_container.pack(fill="both", expand=True, padx=10, pady=10)
        
        columns = ("Nº OS", "WAN/Piloto", "Técnico", "Data", "Início", "Fim", "Status", "Observação")
        
        self.tree = ttk.Treeview(table_container, columns=columns, show="headings", height=18, style="Custom.Treeview")
        
        style = ttk.Style()
        style.theme_use("clam")
        
        style.configure("Custom.Treeview.Heading",
                        background="#1a1a2e",
                        foreground="#00ff88",
                        font=('Arial', 10, 'bold'),
                        borderwidth=0)
        
        style.configure("Custom.Treeview",
                        background="#0f0f0f",
                        foreground="#cccccc",
                        fieldbackground="#0f0f0f",
                        rowheight=28,
                        borderwidth=0,
                        font=('Arial', 10))
        
        style.map("Custom.Treeview",
                  background=[('selected', '#ff6b00')],
                  foreground=[('selected', '#ffffff')])
        
        for col in columns:
            self.tree.heading(col, text=col)
            if col == "WAN/Piloto":
                self.tree.column(col, width=110)
            elif col == "Técnico":
                self.tree.column(col, width=140)
            elif col == "Observação":
                self.tree.column(col, width=100)
            else:
                self.tree.column(col, width=80)
        
        self.tree.pack(side="left", fill="both", expand=True)
        
        scrollbar = ttk.Scrollbar(table_container, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Bind clique na tabela
        self.tree.bind("<<TreeviewSelect>>", self.on_linha_selecionada)
        
        # ================= ÁREA DOS CARIMBOS (70%) =================
        carimbos_wrapper = ctk.CTkFrame(main_container, fg_color="#0f0f0f", corner_radius=12, border_width=1, border_color="#2a2a2a")
        carimbos_wrapper.grid(row=0, column=1, sticky="nsew", padx=(10, 0), pady=0)
        
        ctk.CTkLabel(
            carimbos_wrapper,
            text="📝 DETALHES DA OS",
            font=('Arial', 14, 'bold'),
            text_color="#00ff88"
        ).pack(anchor="w", padx=15, pady=(10, 5))
        
        carimbos_container = ctk.CTkFrame(carimbos_wrapper, fg_color="transparent")
        carimbos_container.pack(fill="both", expand=True, padx=15, pady=10)
        
        # Frame para OS Selecionada (borda amarela)
        self.frame_selecionada = ctk.CTkFrame(carimbos_container, fg_color="#1a1a2e", corner_radius=12, border_width=2, border_color="#ffaa00")
        self.frame_selecionada.pack(fill="x", pady=(0, 15))
        
        ctk.CTkLabel(
            self.frame_selecionada,
            text="🟡 OS SELECIONADA",
            font=('Arial', 13, 'bold'),
            text_color="#ffaa00"
        ).pack(anchor="w", padx=10, pady=(5, 0))
        
        self.texto_selecionada = ctk.CTkTextbox(self.frame_selecionada, height=200, font=('Arial', 12), fg_color="#1a1a2e", border_width=0)
        self.texto_selecionada.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Frame para OS Referência (borda verde)
        self.frame_referencia = ctk.CTkFrame(carimbos_container, fg_color="#1a1a2e", corner_radius=12, border_width=2, border_color="#00cc66")
        self.frame_referencia.pack(fill="x", pady=(0, 0))
        
        ctk.CTkLabel(
            self.frame_referencia,
            text="🟢 OS REFERÊNCIA",
            font=('Arial', 13, 'bold'),
            text_color="#00cc66"
        ).pack(anchor="w", padx=10, pady=(5, 0))
        
        self.texto_referencia = ctk.CTkTextbox(self.frame_referencia, height=200, font=('Arial', 12), fg_color="#1a1a2e", border_width=0)
        self.texto_referencia.pack(fill="both", expand=True, padx=10, pady=5)

    def carregar_tecnicos(self):
        """Carrega a lista de técnicos no combobox"""
        tecnicos = self.relatorio_controller.get_tecnicos()
        valores = ["Todos"] + [t['nome'] for t in tecnicos]
        self.tecnico_combo.configure(values=valores)

    def carregar_periodos_producao(self):
        """Carrega os períodos de produção"""
        hoje = datetime.now()
        for i in range(12):
            data_fim = datetime(hoje.year, hoje.month, 1) - timedelta(days=i * 30)
            
            if data_fim.day >= 21:
                data_inicio = datetime(data_fim.year, data_fim.month, 21)
            else:
                if data_fim.month > 1:
                    data_inicio = datetime(data_fim.year, data_fim.month - 1, 21)
                else:
                    data_inicio = datetime(data_fim.year - 1, 12, 21)
            
            data_fim = data_inicio + timedelta(days=30)
            data_fim = datetime(data_fim.year, data_fim.month, 20)
            
            nome = f"{data_inicio.strftime('%d/%m/%Y')} a {data_fim.strftime('%d/%m/%Y')}"
            self.periodos_producao.append({
                'nome': nome,
                'inicio': data_inicio.strftime("%Y-%m-%d"),
                'fim': data_fim.strftime("%Y-%m-%d")
            })
        
        self.periodo_combo.configure(values=[p['nome'] for p in self.periodos_producao])
        if self.periodos_producao:
            self.periodo_combo.set(self.periodos_producao[0]['nome'])

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
        
        self.aplicar_filtro()

    def obter_periodo(self):
        """Retorna data_inicio e data_fim conforme o modo"""
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

    def carregar_dados(self, data_inicio=None, data_fim=None, id_tecnico=None):
        """Carrega os dados da tabela e atualiza os cards"""
        if data_inicio is None or data_fim is None:
            data_inicio, data_fim = self.obter_periodo()
        
        resumo = self.relatorio_controller.get_resumo_periodo(data_inicio, data_fim)
        
        self.card_repetido_valor.configure(text=str(resumo['repeticoes']))
        self.card_total_valor.configure(text=str(resumo['total_os']))
        self.card_ofensor_valor.configure(text=f"{resumo['ofensor']}%")
        
        tecnicos = self.relatorio_controller.get_tecnicos()
        self.card_tecnicos_valor.configure(text=str(len(tecnicos)))
        
        self.dados_atuais = self.relatorio_controller.get_os_repetidas_apenas(data_inicio, data_fim, id_tecnico)
        
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        for i, item in enumerate(self.dados_atuais):
            tag = 'even' if i % 2 == 0 else 'odd'
            self.tree.insert("", "end", values=(
                item.get('numero', '-'),
                item.get('wan_piloto', '-'),
                item.get('tecnico', '-'),
                item.get('data', '-'),
                item.get('inicio_execucao', '-'),
                item.get('fim_execucao', '-'),
                item.get('status_nome', '-'),
                item.get('observacao', '-')
            ), tags=(tag,), iid=str(i))
        
        self.tree.tag_configure('even', background='#0f0f0f')
        self.tree.tag_configure('odd', background='#1a1a2e')

    def on_linha_selecionada(self, event):
        """Quando seleciona uma linha, mostra os carimbos"""
        selection = self.tree.selection()
        if not selection:
            return
        
        item_id = selection[0]
        valores = self.tree.item(item_id, 'values')
        
        if not valores:
            return
        
        os_selecionada = None
        for os in self.dados_atuais:
            if str(os.get('numero')) == str(valores[0]):
                os_selecionada = os
                break
        
        if not os_selecionada:
            return
        
        data_inicio, data_fim = self.obter_periodo()
        wan = os_selecionada.get('wan_piloto')
        
        os_referencia = self.relatorio_controller.get_os_anterior(
            wan, 
            os_selecionada.get('data'), 
            os_selecionada.get('inicio_execucao', '00:00'),
            data_inicio, 
            data_fim
        )
        
        carimbo_selecionada = self.buscar_carimbo_por_numero(os_selecionada.get('numero'))
        texto_selecionada = f"📝 CARIMBO:\n{carimbo_selecionada}"
        
        if os_referencia:
            carimbo_referencia = self.buscar_carimbo_por_numero(os_referencia.get('numero'))
            texto_referencia = f"📌 OS: {os_referencia['numero']} | 👤 {os_referencia['tecnico']} | 📅 {os_referencia['data']}\n\n📝 CARIMBO:\n{carimbo_referencia}"
        else:
            texto_referencia = "Nenhuma OS de referência encontrada"
        
        self.texto_selecionada.delete("1.0", "end")
        self.texto_selecionada.insert("1.0", texto_selecionada)
        
        self.texto_referencia.delete("1.0", "end")
        self.texto_referencia.insert("1.0", texto_referencia)

    def buscar_carimbo_por_numero(self, numero):
        """Busca APENAS o carimbo completo de uma OS pelo número"""
        os = self.os_controller.buscar_por_numero(numero)
        if os:
            return os['carimbo']
        return f"Carimbo não encontrado para OS {numero}"

    def aplicar_filtro(self):
        """Aplica os filtros selecionados"""
        tecnico = self.tecnico_var.get()
        data_inicio, data_fim = self.obter_periodo()
        
        id_tecnico = None
        if tecnico != "Todos":
            tecnicos = self.relatorio_controller.get_tecnicos()
            for t in tecnicos:
                if t['nome'] == tecnico:
                    id_tecnico = t['id']
                    break
        
        self.tecnico_combo.configure(border_color="#00ff88")
        self.carregar_dados(data_inicio, data_fim, id_tecnico)
        
        self.texto_selecionada.delete("1.0", "end")
        self.texto_referencia.delete("1.0", "end")
        
        self.after(2000, lambda: self.tecnico_combo.configure(border_color="#2a2a2a"))

    # ================= JANELA DE RELATÓRIO =================
    
    def abrir_janela_relatorio(self):
        """Abre a janela para gerar relatório"""
        dialog = ctk.CTkToplevel(self)
        dialog.title("Exportar Relatório")
        dialog.geometry("600x550")
        dialog.transient(self)
        dialog.grab_set()
        
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (600 // 2)
        y = (dialog.winfo_screenheight() // 2) - (550 // 2)
        dialog.geometry(f"+{x}+{y}")
        
        main_frame = ctk.CTkFrame(dialog, fg_color="#0a0a0a")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        ctk.CTkLabel(
            main_frame,
            text="📊 EXPORTAR RELATÓRIO",
            font=('Arial', 20, 'bold'),
            text_color="#00ff88"
        ).pack(anchor="w", pady=(0, 20))
        
        # ================= TIPO DE EXPORTAÇÃO =================
        ctk.CTkLabel(
            main_frame,
            text="Tipo de Exportação:",
            font=('Arial', 14, 'bold'),
            text_color="#cccccc"
        ).pack(anchor="w", pady=(0, 5))
        
        tipo_var = ctk.StringVar(value="pdf")
        
        tipo_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        tipo_frame.pack(fill="x", pady=(0, 15))
        
        ctk.CTkRadioButton(tipo_frame, text="📄 PDF (Relatório Completo)", variable=tipo_var, value="pdf").pack(anchor="w", pady=2)
        ctk.CTkRadioButton(tipo_frame, text="📊 CSV (Lista de OS)", variable=tipo_var, value="csv_os").pack(anchor="w", pady=2)
        ctk.CTkRadioButton(tipo_frame, text="📈 CSV (Médias - APU/Ofensor)", variable=tipo_var, value="csv_medias").pack(anchor="w", pady=2)
        
        # ================= PERÍODO =================
        ctk.CTkLabel(
            main_frame,
            text="Período:",
            font=('Arial', 14, 'bold'),
            text_color="#cccccc"
        ).pack(anchor="w", pady=(0, 5))
        
        periodo_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        periodo_frame.pack(fill="x", pady=(0, 15))
        
        self.periodo_rel_mes = ctk.CTkButton(
            periodo_frame,
            text="📅 Mês Corrido",
            fg_color="#ff6b00",
            width=140,
            command=lambda: self._toggle_periodo_rel('mes')
        )
        self.periodo_rel_mes.pack(side="left", padx=(0, 10))
        
        self.periodo_rel_producao = ctk.CTkButton(
            periodo_frame,
            text="📊 Produção",
            fg_color="#1a1a2e",
            border_width=1,
            border_color="#00ff88",
            width=140,
            command=lambda: self._toggle_periodo_rel('producao')
        )
        self.periodo_rel_producao.pack(side="left")
        
        # ================= SELETORES =================
        self.rel_selects_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        self.rel_selects_frame.pack(fill="x", pady=(0, 15))
        
        # Select de Mês
        self.rel_mes_frame = ctk.CTkFrame(self.rel_selects_frame, fg_color="transparent")
        
        ctk.CTkLabel(self.rel_mes_frame, text="Mês:", font=('Arial', 12), text_color="#cccccc").pack(side="left", padx=(0, 5))
        
        self.rel_mes_combo = ctk.CTkComboBox(self.rel_mes_frame, values=self.meses, width=130, state="readonly")
        self.rel_mes_combo.pack(side="left", padx=(0, 15))
        self.rel_mes_combo.set(self.meses[datetime.now().month - 1])
        
        ctk.CTkLabel(self.rel_mes_frame, text="Ano:", font=('Arial', 12), text_color="#cccccc").pack(side="left", padx=(0, 5))
        
        ano_atual = datetime.now().year
        anos = [str(ano_atual - 1), str(ano_atual), str(ano_atual + 1)]
        self.rel_ano_combo = ctk.CTkComboBox(self.rel_mes_frame, values=anos, width=90, state="readonly")
        self.rel_ano_combo.pack(side="left")
        self.rel_ano_combo.set(str(ano_atual))
        
        self.rel_mes_frame.pack(side="left")
        
        # Select de Período de Produção
        self.rel_producao_frame = ctk.CTkFrame(self.rel_selects_frame, fg_color="transparent")
        
        ctk.CTkLabel(self.rel_producao_frame, text="Período:", font=('Arial', 12), text_color="#cccccc").pack(side="left", padx=(0, 5))
        
        self.rel_periodo_combo = ctk.CTkComboBox(self.rel_producao_frame, values=[p['nome'] for p in self.periodos_producao], width=250, state="readonly")
        self.rel_periodo_combo.pack(side="left")
        if self.periodos_producao:
            self.rel_periodo_combo.set(self.periodos_producao[0]['nome'])
        
        self.rel_producao_frame.pack_forget()
        
        # ================= TÉCNICO =================
        ctk.CTkLabel(
            main_frame,
            text="Técnico:",
            font=('Arial', 14, 'bold'),
            text_color="#cccccc"
        ).pack(anchor="w", pady=(0, 5))
        
        tecnicos = self.relatorio_controller.get_tecnicos()
        tecnicos_nomes = ["Todos"] + [t['nome'] for t in tecnicos]
        
        self.rel_tecnico_combo = ctk.CTkComboBox(main_frame, values=tecnicos_nomes, width=300, state="readonly")
        self.rel_tecnico_combo.pack(anchor="w", pady=(0, 20))
        self.rel_tecnico_combo.set("Todos")
        
        # ================= BOTÕES =================
        btn_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        btn_frame.pack(fill="x")
        
        ctk.CTkButton(
            btn_frame,
            text="📄 Exportar",
            fg_color="#00cc66",
            hover_color="#009944",
            font=('Arial', 13, 'bold'),
            width=150,
            command=lambda: self.exportar_relatorio(dialog, tipo_var.get())
        ).pack(side="left", padx=(0, 10))
        
        ctk.CTkButton(
            btn_frame,
            text="Cancelar",
            fg_color="#ff3333",
            hover_color="#cc0000",
            font=('Arial', 13, 'bold'),
            width=150,
            command=dialog.destroy
        ).pack(side="left")
        
        self.periodo_rel_tipo = 'mes'

    def _toggle_periodo_rel(self, tipo):
        """Alterna entre os períodos na janela de relatório"""
        if tipo == 'mes':
            self.periodo_rel_mes.configure(fg_color="#ff6b00")
            self.periodo_rel_producao.configure(fg_color="#1a1a2e")
            self.rel_mes_frame.pack(side="left")
            self.rel_producao_frame.pack_forget()
            self.periodo_rel_tipo = 'mes'
        else:
            self.periodo_rel_mes.configure(fg_color="#1a1a2e")
            self.periodo_rel_producao.configure(fg_color="#ff6b00")
            self.rel_mes_frame.pack_forget()
            self.rel_producao_frame.pack(side="left")
            self.periodo_rel_tipo = 'producao'

    def exportar_relatorio(self, dialog, tipo):
        """Exporta o relatório conforme o tipo selecionado"""
        # Obter dados do período
        if self.periodo_rel_tipo == 'mes':
            mes = self.rel_mes_combo.get()
            ano = self.rel_ano_combo.get()
            periodo_nome = None
        else:
            mes = None
            ano = None
            periodo_nome = self.rel_periodo_combo.get()
        
        tecnico_nome = self.rel_tecnico_combo.get()
        
        # Usar o exportador
        exportador = ExportadorRelatorio(self, self.relatorio_controller, self.os_controller)
        exportador.carregar_periodos_producao()
        
        dados = exportador.obter_dados_periodo(
            self.periodo_rel_tipo, mes, ano, periodo_nome, tecnico_nome
        )
        
        dialog.destroy()
        
        if tipo == "pdf":
            exportador.gerar_pdf(dados)
        elif tipo == "csv_os":
            exportador.exportar_csv_os(dados)
        elif tipo == "csv_medias":
            exportador.exportar_csv_medias(dados)