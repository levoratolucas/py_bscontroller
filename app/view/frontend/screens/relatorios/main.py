import customtkinter as ctk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
from app.view.frontend.styles import COLORS, FONTS
from app.controller.relatorio_controller import RelatorioController
from app.controller.ordem_servico_controller import OrdemServicoController
from app.controller.repetido_controller import RepetidoController
from app.view.frontend.screens.relatorios.exportar import ExportadorRelatorio
from app.view.frontend.screens.relatorios.popup_analise import PopupAnalise
from app.view.frontend.screens.relatorios.cards import (
    CardPendente, CardRepetido, CardProcede, CardImprocedente
)


class RelatoriosScreen(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent, fg_color="transparent")
        self.pack(fill="both", expand=True)
        
        self.app = app
        self.relatorio_controller = RelatorioController()
        self.os_controller = OrdemServicoController()
        self.repetido_controller = RepetidoController()
        self.dados_atuais = []
        self.modo = "mes"
        self.periodos_producao = []
        self.meses = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", 
                     "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]
        self.filtro_status_atual = "todos"  # todos, pendentes, procedem, improcedem
        
        self.cards = {}
        
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
            text="Análise de WANs repetidos | Clique nos cards para filtrar | Duplo clique apenas em PENDENTES",
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
        
        # Card 1 - PENDENTE (laranja)
        self.cards['pendente'] = CardPendente(
            cards_frame, 0, 0,
            callback=lambda: self.filtrar_por_status("pendentes")
        )
        
        # Card 2 - REPETIDO (amarelo)
        self.cards['repetido'] = CardRepetido(
            cards_frame, 0, 1,
            callback=lambda: self.filtrar_por_status("todos")
        )
        
        # Card 3 - PROCEDE (verde)
        self.cards['procede'] = CardProcede(
            cards_frame, 0, 2,
            callback=lambda: self.filtrar_por_status("procedem")
        )
        
        # Card 4 - IMPROCEDENTE (vermelho)
        self.cards['improcedente'] = CardImprocedente(
            cards_frame, 0, 3,
            callback=lambda: self.filtrar_por_status("nao_procedem")
        )

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
        
        # Botão Limpar Filtro de Status
        ctk.CTkButton(
            row_filtros,
            text="🗑️ Limpar Filtro",
            fg_color="#555555",
            hover_color="#333333",
            width=120,
            command=self.limpar_filtro_status
        ).pack(side="left", padx=(20, 0))

        # ================= CONTAINER PRINCIPAL =================
        main_container = ctk.CTkFrame(main_frame, fg_color="transparent")
        main_container.pack(fill="both", expand=True)
        
        main_container.grid_columnconfigure(0, weight=30)
        main_container.grid_columnconfigure(1, weight=70)
        main_container.grid_rowconfigure(0, weight=1)
        
        # ================= TABELA (30%) =================
        table_wrapper = ctk.CTkFrame(main_container, fg_color="#0f0f0f", corner_radius=12, border_width=1, border_color="#2a2a2a")
        table_wrapper.grid(row=0, column=0, sticky="nsew", padx=(0, 10), pady=0)
        
        self.titulo_tabela = ctk.CTkLabel(
            table_wrapper,
            text="📋 Histórico de Repetições (Duplo clique apenas em PENDENTES)",
            font=('Arial', 12, 'bold'),
            text_color="#00ff88"
        )
        self.titulo_tabela.pack(anchor="w", padx=15, pady=(10, 5))
        
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
        
        # Binds da tabela
        self.tree.bind("<<TreeviewSelect>>", self.on_linha_selecionada)
        self.tree.bind("<Double-1>", self.abrir_popup_analise)
        
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

    def filtrar_por_status(self, status):
        """Filtra a tabela pelo status do card clicado"""
        self.filtro_status_atual = status
        self.carregar_dados_com_filtro()
        
        # Destacar o card selecionado
        self.destacar_card_selecionado(status)
    
    def destacar_card_selecionado(self, status):
        """Destaca o card clicado com borda mais grossa"""
        # Resetar bordas de todos os cards
        for card in self.cards.values():
            card.destacar(False)
        
        # Destacar o card selecionado
        if status == "pendentes":
            self.cards['pendente'].destacar(True)
            self.titulo_tabela.configure(text="📋 Histórico de Repetições - PENDENTES (⏳)")
        elif status == "todos":
            self.cards['repetido'].destacar(True)
            self.titulo_tabela.configure(text="📋 Histórico de Repetições - TODOS (🔄)")
        elif status == "procedem":
            self.cards['procede'].destacar(True)
            self.titulo_tabela.configure(text="📋 Histórico de Repetições - PROCEDEM (✅)")
        elif status == "nao_procedem":
            self.cards['improcedente'].destacar(True)
            self.titulo_tabela.configure(text="📋 Histórico de Repetições - IMPROCEDEM (❌)")
    
    def limpar_filtro_status(self):
        """Limpa o filtro de status e mostra todos"""
        self.filtro_status_atual = "todos"
        self.carregar_dados_com_filtro()
        self.destacar_card_selecionado("todos")
    
    def carregar_dados_com_filtro(self):
        """Carrega os dados aplicando o filtro de status atual"""
        data_inicio, data_fim = self.obter_periodo()
        tecnico = self.tecnico_var.get()
        
        id_tecnico = None
        if tecnico != "Todos":
            tecnicos = self.relatorio_controller.get_tecnicos()
            for t in tecnicos:
                if t['nome'] == tecnico:
                    id_tecnico = t['id']
                    break
        
        mes_referencia = datetime.strptime(data_inicio, "%Y-%m-%d").strftime("%Y-%m")
        
        # Buscar repetidos da tabela (já analisados)
        repetidos_analisados = self.repetido_controller.get_repetidos_com_detalhes(mes_referencia)
        
        # Filtrar por técnico se necessário
        if id_tecnico:
            repetidos_analisados = [r for r in repetidos_analisados if r.get('tecnico_repetido') and 
                                    self._get_tecnico_id_por_nome(r['tecnico_repetido']) == id_tecnico]
        
        # Buscar OS pendentes (não analisadas)
        os_pendentes = self.relatorio_controller.get_os_repetidas_apenas(data_inicio, data_fim, id_tecnico)
        ids_analisados = self.repetido_controller.get_ids_os_analisados()
        os_pendentes = [os for os in os_pendentes if os.get('id_os') not in ids_analisados]
        
        # Contar por status
        total_pendentes = len(os_pendentes)
        total_procedem = len([r for r in repetidos_analisados if r.get('procedente') == 1])
        total_improcedem = len([r for r in repetidos_analisados if r.get('procedente') == 2])
        total_repetidos = total_pendentes + total_procedem + total_improcedem
        
        # Atualizar cards
        self.cards['pendente'].set_valor(total_pendentes)
        self.cards['repetido'].set_valor(total_repetidos)
        self.cards['procede'].set_valor(total_procedem)
        self.cards['improcedente'].set_valor(total_improcedem)
        
        # Preparar dados para a tabela conforme o filtro
        if self.filtro_status_atual == "pendentes":
            dados_tabela = []
            for os in os_pendentes:
                dados_tabela.append({
                    'numero': os.get('numero', '-'),
                    'wan_piloto': os.get('wan_piloto', '-'),
                    'tecnico': os.get('tecnico', '-'),
                    'data': os.get('data', '-'),
                    'inicio_execucao': os.get('inicio_execucao', '-'),
                    'fim_execucao': os.get('fim_execucao', '-'),
                    'status_nome': os.get('status_nome', '-'),
                    'observacao': '⏳ Pendente',
                    'pendente': True,
                    'id_os': os.get('id_os')
                })
        elif self.filtro_status_atual == "procedem":
            dados_tabela = []
            for r in repetidos_analisados:
                if r.get('procedente') == 1:
                    dados_tabela.append({
                        'numero': r.get('numero_repetido', '-'),
                        'wan_piloto': r.get('wan_piloto', '-'),
                        'tecnico': r.get('tecnico_repetido', '-'),
                        'data': r.get('data_repetido', '-'),
                        'inicio_execucao': r.get('hora_repetido', '-'),
                        'fim_execucao': '-',
                        'status_nome': 'Concluído' if r.get('status_repetido') == 1 else 'Suspenso',
                        'observacao': '✅ Procede',
                        'pendente': False,
                        'id_os': r.get('id_os'),
                        'numero_referencia': r.get('numero_referencia'),
                        'tecnico_referencia': r.get('tecnico_referencia'),
                        'data_referencia': r.get('data_referencia'),
                        'carimbo_referencia': r.get('carimbo_referencia'),
                        'carimbo_repetido': r.get('carimbo_repetido')
                    })
        elif self.filtro_status_atual == "nao_procedem":
            dados_tabela = []
            for r in repetidos_analisados:
                if r.get('procedente') == 2:
                    dados_tabela.append({
                        'numero': r.get('numero_repetido', '-'),
                        'wan_piloto': r.get('wan_piloto', '-'),
                        'tecnico': r.get('tecnico_repetido', '-'),
                        'data': r.get('data_repetido', '-'),
                        'inicio_execucao': r.get('hora_repetido', '-'),
                        'fim_execucao': '-',
                        'status_nome': 'Concluído' if r.get('status_repetido') == 1 else 'Suspenso',
                        'observacao': '❌ Não Procede',
                        'pendente': False,
                        'id_os': r.get('id_os'),
                        'numero_referencia': r.get('numero_referencia'),
                        'tecnico_referencia': r.get('tecnico_referencia'),
                        'data_referencia': r.get('data_referencia'),
                        'carimbo_referencia': r.get('carimbo_referencia'),
                        'carimbo_repetido': r.get('carimbo_repetido')
                    })
        else:  # "todos" - mostrar todos (pendentes + analisados)
            dados_tabela = []
            for os in os_pendentes:
                dados_tabela.append({
                    'numero': os.get('numero', '-'),
                    'wan_piloto': os.get('wan_piloto', '-'),
                    'tecnico': os.get('tecnico', '-'),
                    'data': os.get('data', '-'),
                    'inicio_execucao': os.get('inicio_execucao', '-'),
                    'fim_execucao': os.get('fim_execucao', '-'),
                    'status_nome': os.get('status_nome', '-'),
                    'observacao': '⏳ Pendente',
                    'pendente': True,
                    'id_os': os.get('id_os')
                })
            for r in repetidos_analisados:
                status_texto = {1: "✅ Procede", 2: "❌ Não Procede"}
                dados_tabela.append({
                    'numero': r.get('numero_repetido', '-'),
                    'wan_piloto': r.get('wan_piloto', '-'),
                    'tecnico': r.get('tecnico_repetido', '-'),
                    'data': r.get('data_repetido', '-'),
                    'inicio_execucao': r.get('hora_repetido', '-'),
                    'fim_execucao': '-',
                    'status_nome': 'Concluído' if r.get('status_repetido') == 1 else 'Suspenso',
                    'observacao': status_texto.get(r.get('procedente', 0), 'Desconhecido'),
                    'pendente': False,
                    'id_os': r.get('id_os'),
                    'numero_referencia': r.get('numero_referencia'),
                    'tecnico_referencia': r.get('tecnico_referencia'),
                    'data_referencia': r.get('data_referencia'),
                    'carimbo_referencia': r.get('carimbo_referencia'),
                    'carimbo_repetido': r.get('carimbo_repetido')
                })
        
        self.dados_atuais = dados_tabela
        
        # Limpar treeview
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Preencher treeview
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

    def _get_tecnico_id_por_nome(self, nome):
        """Retorna o ID do técnico pelo nome"""
        tecnicos = self.relatorio_controller.get_tecnicos()
        for t in tecnicos:
            if t['nome'] == nome:
                return t['id']
        return None

    def carregar_dados(self, data_inicio=None, data_fim=None, id_tecnico=None):
        """Carrega os dados da tabela e atualiza os cards"""
        if data_inicio is None or data_fim is None:
            data_inicio, data_fim = self.obter_periodo()
        
        mes_referencia = datetime.strptime(data_inicio, "%Y-%m-%d").strftime("%Y-%m")
        
        # Buscar repetidos da tabela (já analisados)
        repetidos_analisados = self.repetido_controller.get_repetidos_com_detalhes(mes_referencia)
        
        # Filtrar por técnico se necessário
        if id_tecnico:
            repetidos_analisados = [r for r in repetidos_analisados if r.get('tecnico_repetido') and 
                                    self._get_tecnico_id_por_nome(r['tecnico_repetido']) == id_tecnico]
        
        # Buscar OS pendentes (não analisadas)
        os_pendentes = self.relatorio_controller.get_os_repetidas_apenas(data_inicio, data_fim, id_tecnico)
        ids_analisados = self.repetido_controller.get_ids_os_analisados()
        os_pendentes = [os for os in os_pendentes if os.get('id_os') not in ids_analisados]
        
        # Contar por status
        total_pendentes = len(os_pendentes)
        total_procedem = len([r for r in repetidos_analisados if r.get('procedente') == 1])
        total_improcedem = len([r for r in repetidos_analisados if r.get('procedente') == 2])
        total_repetidos = total_pendentes + total_procedem + total_improcedem
        
        # Atualizar cards
        self.cards['pendente'].set_valor(total_pendentes)
        self.cards['repetido'].set_valor(total_repetidos)
        self.cards['procede'].set_valor(total_procedem)
        self.cards['improcedente'].set_valor(total_improcedem)
        
        # Preparar dados para a tabela conforme o filtro atual
        if self.filtro_status_atual == "pendentes":
            dados_tabela = []
            for os in os_pendentes:
                dados_tabela.append({
                    'numero': os.get('numero', '-'),
                    'wan_piloto': os.get('wan_piloto', '-'),
                    'tecnico': os.get('tecnico', '-'),
                    'data': os.get('data', '-'),
                    'inicio_execucao': os.get('inicio_execucao', '-'),
                    'fim_execucao': os.get('fim_execucao', '-'),
                    'status_nome': os.get('status_nome', '-'),
                    'observacao': '⏳ Pendente',
                    'pendente': True,
                    'id_os': os.get('id_os')
                })
        elif self.filtro_status_atual == "procedem":
            dados_tabela = []
            for r in repetidos_analisados:
                if r.get('procedente') == 1:
                    dados_tabela.append({
                        'numero': r.get('numero_repetido', '-'),
                        'wan_piloto': r.get('wan_piloto', '-'),
                        'tecnico': r.get('tecnico_repetido', '-'),
                        'data': r.get('data_repetido', '-'),
                        'inicio_execucao': r.get('hora_repetido', '-'),
                        'fim_execucao': '-',
                        'status_nome': 'Concluído' if r.get('status_repetido') == 1 else 'Suspenso',
                        'observacao': '✅ Procede',
                        'pendente': False,
                        'id_os': r.get('id_os'),
                        'numero_referencia': r.get('numero_referencia'),
                        'tecnico_referencia': r.get('tecnico_referencia'),
                        'data_referencia': r.get('data_referencia'),
                        'carimbo_referencia': r.get('carimbo_referencia'),
                        'carimbo_repetido': r.get('carimbo_repetido')
                    })
        elif self.filtro_status_atual == "nao_procedem":
            dados_tabela = []
            for r in repetidos_analisados:
                if r.get('procedente') == 2:
                    dados_tabela.append({
                        'numero': r.get('numero_repetido', '-'),
                        'wan_piloto': r.get('wan_piloto', '-'),
                        'tecnico': r.get('tecnico_repetido', '-'),
                        'data': r.get('data_repetido', '-'),
                        'inicio_execucao': r.get('hora_repetido', '-'),
                        'fim_execucao': '-',
                        'status_nome': 'Concluído' if r.get('status_repetido') == 1 else 'Suspenso',
                        'observacao': '❌ Não Procede',
                        'pendente': False,
                        'id_os': r.get('id_os'),
                        'numero_referencia': r.get('numero_referencia'),
                        'tecnico_referencia': r.get('tecnico_referencia'),
                        'data_referencia': r.get('data_referencia'),
                        'carimbo_referencia': r.get('carimbo_referencia'),
                        'carimbo_repetido': r.get('carimbo_repetido')
                    })
        else:  # "todos" - mostrar todos
            dados_tabela = []
            for os in os_pendentes:
                dados_tabela.append({
                    'numero': os.get('numero', '-'),
                    'wan_piloto': os.get('wan_piloto', '-'),
                    'tecnico': os.get('tecnico', '-'),
                    'data': os.get('data', '-'),
                    'inicio_execucao': os.get('inicio_execucao', '-'),
                    'fim_execucao': os.get('fim_execucao', '-'),
                    'status_nome': os.get('status_nome', '-'),
                    'observacao': '⏳ Pendente',
                    'pendente': True,
                    'id_os': os.get('id_os')
                })
            for r in repetidos_analisados:
                status_texto = {1: "✅ Procede", 2: "❌ Não Procede"}
                dados_tabela.append({
                    'numero': r.get('numero_repetido', '-'),
                    'wan_piloto': r.get('wan_piloto', '-'),
                    'tecnico': r.get('tecnico_repetido', '-'),
                    'data': r.get('data_repetido', '-'),
                    'inicio_execucao': r.get('hora_repetido', '-'),
                    'fim_execucao': '-',
                    'status_nome': 'Concluído' if r.get('status_repetido') == 1 else 'Suspenso',
                    'observacao': status_texto.get(r.get('procedente', 0), 'Desconhecido'),
                    'pendente': False,
                    'id_os': r.get('id_os'),
                    'numero_referencia': r.get('numero_referencia'),
                    'tecnico_referencia': r.get('tecnico_referencia'),
                    'data_referencia': r.get('data_referencia'),
                    'carimbo_referencia': r.get('carimbo_referencia'),
                    'carimbo_repetido': r.get('carimbo_repetido')
                })
        
        self.dados_atuais = dados_tabela
        
        # Limpar treeview
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Preencher treeview
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
        """Quando seleciona uma linha, mostra os carimbos (para todas as OS)"""
        selection = self.tree.selection()
        if not selection:
            return
        
        item_id = selection[0]
        valores = self.tree.item(item_id, 'values')
        
        if not valores:
            return
        
        # Buscar a OS selecionada
        os_selecionada = None
        for os in self.dados_atuais:
            if str(os.get('numero')) == str(valores[0]):
                os_selecionada = os
                break
        
        if not os_selecionada:
            return
        
        data_inicio, data_fim = self.obter_periodo()
        wan = os_selecionada.get('wan_piloto')
        
        # Verificar se é pendente ou já analisada
        is_pendente = os_selecionada.get('pendente', False)
        
        if is_pendente:
            # Buscar OS de referência para pendentes (dinamicamente)
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
        else:
            # OS já analisada - usar os dados já salvos na tabela repetidos
            carimbo_selecionada = os_selecionada.get('carimbo_repetido', 'Carimbo não disponível')
            texto_selecionada = f"📝 CARIMBO:\n{carimbo_selecionada}"
            
            if os_selecionada.get('numero_referencia'):
                texto_referencia = f"📌 OS: {os_selecionada.get('numero_referencia', '-')} | 👤 {os_selecionada.get('tecnico_referencia', '-')} | 📅 {os_selecionada.get('data_referencia', '-')}\n\n📝 CARIMBO:\n{os_selecionada.get('carimbo_referencia', 'Carimbo não disponível')}"
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

    # ================= POPUP DE ANÁLISE =================
    
    def abrir_popup_analise(self, event=None):
        """Abre popup para análise do repetido (apenas para pendentes)"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Aviso", "Selecione um repetido para analisar!")
            return
        
        item_id = selection[0]
        valores = self.tree.item(item_id, 'values')
        
        if not valores:
            return
        
        # Buscar a OS selecionada
        os_selecionada = None
        for os in self.dados_atuais:
            if str(os.get('numero')) == str(valores[0]):
                os_selecionada = os
                break
        
        if not os_selecionada:
            messagebox.showerror("Erro", "OS não encontrada!")
            return
        
        # VERIFICAR SE É PENDENTE (apenas pendentes podem ser analisadas)
        if not os_selecionada.get('pendente', False):
            messagebox.showwarning("Aviso", "Esta OS já foi analisada! Apenas OS pendentes podem ser analisadas.")
            return
        
        # Verificar se tem id_os
        if not os_selecionada.get('id_os'):
            messagebox.showerror("Erro", "ID da OS não encontrado!")
            return
        
        # Buscar a OS de referência
        data_inicio, data_fim = self.obter_periodo()
        wan = os_selecionada.get('wan_piloto')
        
        os_referencia = self.relatorio_controller.get_os_anterior(
            wan, 
            os_selecionada.get('data'), 
            os_selecionada.get('inicio_execucao', '00:00'),
            data_inicio, 
            data_fim
        )
        
        if not os_referencia:
            messagebox.showerror("Erro", "Não foi possível encontrar a OS de referência!")
            return
        
        # Verificar se tem id_os_referencia
        if not os_referencia.get('id_os'):
            messagebox.showerror("Erro", "ID da OS referência não encontrado!")
            return
        
        # Obter o mês de referência baseado no período selecionado no filtro
        mes_referencia = datetime.strptime(data_inicio, "%Y-%m-%d").strftime("%Y-%m")
        
        # Abrir popup
        PopupAnalise(
            parent=self,
            dados_os={
                'os_selecionada': os_selecionada,
                'os_referencia': os_referencia
            },
            repetido_controller=self.repetido_controller,
            callback_atualizar=self.aplicar_filtro,
            mes_referencia=mes_referencia
        )

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
        if self.periodo_rel_tipo == 'mes':
            mes = self.rel_mes_combo.get()
            ano = self.rel_ano_combo.get()
            periodo_nome = None
        else:
            mes = None
            ano = None
            periodo_nome = self.rel_periodo_combo.get()
        
        tecnico_nome = self.rel_tecnico_combo.get()
        
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