import customtkinter as ctk
from tkinter import ttk
from app.view.frontend.styles import COLORS
from app.view.frontend.screens.ordem_servico.widgets.botoes import BotoesOrdemServico
from app.view.frontend.screens.ordem_servico.widgets.seletor import SeletorOrdemServico
from app.view.frontend.screens.ordem_servico.controllers.dados import DadosOrdemServico


class OrdemServicoScreen(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent, fg_color="transparent")
        self.pack(fill="both", expand=True)
        
        self.app = app
        self.dados = DadosOrdemServico()
        self.tipo_atual = 'todos'  # todos, ativacao, reparo, apu
        
        self.setup_ui()
        self.carregar_tecnicos()
        self.carregar_periodos_producao()
        self.atualizar_tudo()

    def setup_ui(self):
        main_frame = ctk.CTkFrame(self, fg_color="#0a0a0a")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Título
        ctk.CTkLabel(
            main_frame,
            text="📋 ORDENS DE SERVIÇO",
            font=('Arial', 22, 'bold'),
            text_color="#00ff88"
        ).pack(anchor="w", pady=(0, 20))

        # Botões
        self.botoes = BotoesOrdemServico(
            main_frame,
            on_todos_click=lambda: self.mudar_tipo('todos'),
            on_ativacao_click=lambda: self.mudar_tipo('ativacao'),
            on_reparo_click=lambda: self.mudar_tipo('reparo'),
            on_apu_click=lambda: self.mudar_tipo('apu')
        )
        
        # Seletor
        self.seletor = SeletorOrdemServico(main_frame)
        self.seletor.set_on_change(self.on_filtro_mudou)
        
        # Container principal (2 colunas)
        main_container = ctk.CTkFrame(main_frame, fg_color="transparent")
        main_container.pack(fill="both", expand=True)
        
        main_container.grid_columnconfigure(0, weight=50)
        main_container.grid_columnconfigure(1, weight=50)
        main_container.grid_rowconfigure(0, weight=1)
        
        # ================= TABELA ESQUERDA =================
        self.tabela_esquerda = self.criar_tabela_os(main_container, 0, "LISTA DE ORDENS")
        
        # ================= CARD DIREITO =================
        self.card_direito = ctk.CTkFrame(main_container, fg_color="#0f0f0f", corner_radius=12, 
                                          border_width=1, border_color="#2a2a2a")
        self.card_direito.grid(row=0, column=1, sticky="nsew", padx=(10, 0), pady=0)
        
        # Container do card direito
        self.card_direito_content = ctk.CTkFrame(self.card_direito, fg_color="transparent")
        self.card_direito_content.pack(fill="both", expand=True, padx=15, pady=15)

    def criar_tabela_os(self, parent, col, titulo):
        """Cria uma tabela de OS"""
        wrapper = ctk.CTkFrame(parent, fg_color="#0f0f0f", corner_radius=12, border_width=1, border_color="#2a2a2a")
        wrapper.grid(row=0, column=col, sticky="nsew", padx=(0 if col == 0 else 10, 10 if col == 0 else 0), pady=0)
        
        ctk.CTkLabel(
            wrapper,
            text=f"📋 {titulo}",
            font=('Arial', 12, 'bold'),
            text_color="#00ff88"
        ).pack(anchor="w", padx=15, pady=(10, 5))
        
        container = ctk.CTkFrame(wrapper, fg_color="transparent")
        container.pack(fill="both", expand=True, padx=10, pady=10)
        
        columns = ("Nº OS", "Técnico", "WAN/Piloto", "Data", "Tipo", "Status")
        tree = ttk.Treeview(container, columns=columns, show="headings", height=20, style="Custom.Treeview")
        
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
        
        for col_name in columns:
            tree.heading(col_name, text=col_name)
            if col_name == "Técnico":
                tree.column(col_name, width=150)
            elif col_name == "WAN/Piloto":
                tree.column(col_name, width=120)
            else:
                tree.column(col_name, width=80)
        
        tree.pack(side="left", fill="both", expand=True)
        
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=tree.yview)
        scrollbar.pack(side="right", fill="y")
        tree.configure(yscrollcommand=scrollbar.set)
        
        # Bind duplo clique
        tree.bind("<Double-1>", self.on_linha_duplo_clique)
        
        return tree

    def carregar_tecnicos(self):
        tecnicos = self.dados.get_tecnicos()
        self.seletor.carregar_tecnicos(tecnicos)

    def carregar_periodos_producao(self):
        """Carrega os períodos de produção no seletor"""
        periodos = self.dados.get_periodos_producao()
        self.seletor.carregar_periodos_producao(periodos)

    def obter_filtros(self):
        if self.seletor.get_modo() == "mes":
            mes = self.seletor.get_seletor('mes').get()
            ano = self.seletor.get_seletor('ano').get()
            data_inicio, data_fim = self.dados.obter_periodo(mes=mes, ano=ano, modo="mes")
        else:
            periodo_nome = self.seletor.get_seletor('periodo').get()
            data_inicio, data_fim = self.dados.obter_periodo(modo="producao", periodo_nome=periodo_nome)
        
        tecnico_val = self.seletor.get_seletor('tecnico').get()
        status = self.seletor.get_status_filtro()
        
        id_tecnico = None
        if tecnico_val != "Todos":
            tecnicos = self.dados.get_tecnicos()
            for t in tecnicos:
                if t['nome'] == tecnico_val:
                    id_tecnico = t['id']
                    break
        
        return data_inicio, data_fim, id_tecnico, status

    def on_filtro_mudou(self):
        """Quando o seletor muda, atualiza tudo"""
        self.atualizar_tudo()

    def atualizar_tudo(self):
        """Atualiza botões, tabela esquerda e conteúdo do card direito"""
        data_inicio, data_fim, id_tecnico, status = self.obter_filtros()
        
        # Atualizar valores dos botões
        quantidades = self.dados.get_quantidades_por_tipo(data_inicio, data_fim, id_tecnico)
        self.botoes.set_valores(quantidades['total'], quantidades['ativacao'], quantidades['reparo'])
        
        # Atualizar APU
        apu_geral = self.dados.calcular_apu_geral(data_inicio, data_fim, id_tecnico)
        self.botoes.set_apu_valor(apu_geral)
        
        # Atualizar tabela esquerda
        tipo_filtro = None
        if self.tipo_atual == 'ativacao':
            tipo_filtro = 3
        elif self.tipo_atual == 'reparo':
            tipo_filtro = 2
        
        os_lista = self.dados.get_os_por_filtro(data_inicio, data_fim, id_tecnico, tipo_filtro, status)
        
        for item in self.tabela_esquerda.get_children():
            self.tabela_esquerda.delete(item)
        
        for i, os in enumerate(os_lista):
            tag = 'even' if i % 2 == 0 else 'odd'
            self.tabela_esquerda.insert("", "end", values=(
                os['numero'],
                os['tecnico'],
                os['wan_piloto'],
                os['data'],
                os['tipo'],
                os['status']
            ), tags=(tag,))
        
        self.tabela_esquerda.tag_configure('even', background='#0f0f0f')
        self.tabela_esquerda.tag_configure('odd', background='#1a1a2e')
        
        # Atualizar card direito
        self.atualizar_card_direito()

    def mudar_tipo(self, tipo):
        """Muda o tipo exibido na tabela esquerda e no card direito"""
        self.tipo_atual = tipo
        self.atualizar_tudo()

    def atualizar_card_direito(self):
        """Atualiza o conteúdo do card direito"""
        # Limpar card direito
        for widget in self.card_direito_content.winfo_children():
            widget.destroy()
        
        data_inicio, data_fim, id_tecnico, status = self.obter_filtros()
        
        if self.tipo_atual == 'apu':
            # Mostrar APU individual
            dados = self.dados.calcular_apu_individual(data_inicio, data_fim, id_tecnico)
            
            ctk.CTkLabel(
                self.card_direito_content,
                text="📊 APU POR TÉCNICO",
                font=('Arial', 12, 'bold'),
                text_color="#ff3333"
            ).pack(anchor="w", pady=(0, 10))
            
            container = ctk.CTkFrame(self.card_direito_content, fg_color="transparent")
            container.pack(fill="both", expand=True)
            
            columns = ("Técnico", "Dias", "Concluídos", "APU")
            tree = ttk.Treeview(container, columns=columns, show="headings", height=15, style="Apu.Treeview")
            
            style = ttk.Style()
            style.configure("Apu.Treeview.Heading",
                            background="#1a1a2e",
                            foreground="#ff3333",
                            font=('Arial', 10, 'bold'),
                            borderwidth=0)
            style.configure("Apu.Treeview",
                            background="#0f0f0f",
                            foreground="#cccccc",
                            fieldbackground="#0f0f0f",
                            rowheight=28,
                            borderwidth=0,
                            font=('Arial', 10))
            style.map("Apu.Treeview",
                      background=[('selected', '#ff3333')])
            
            for col in columns:
                tree.heading(col, text=col)
                tree.column(col, width=100)
            tree.column("Técnico", width=180)
            
            for i, item in enumerate(dados):
                tag = 'even' if i % 2 == 0 else 'odd'
                tree.insert("", "end", values=(
                    item['tecnico'],
                    item['dias_trabalhados'],
                    item['total_concluidos'],
                    item['apu']
                ), tags=(tag,))
            
            tree.tag_configure('even', background='#0f0f0f')
            tree.tag_configure('odd', background='#1a1a2e')
            
            tree.pack(side="left", fill="both", expand=True)
            
            scrollbar = ttk.Scrollbar(container, orient="vertical", command=tree.yview)
            scrollbar.pack(side="right", fill="y")
            tree.configure(yscrollcommand=scrollbar.set)
            
        else:
            # Mostrar resumo por técnico
            tipo_filtro = None
            cor = "#ff6b00"
            titulo = "RESUMO POR TÉCNICO"
            
            if self.tipo_atual == 'ativacao':
                tipo_filtro = 3
                cor = "#0088ff"
                titulo = "ATIVAÇÕES POR TÉCNICO"
            elif self.tipo_atual == 'reparo':
                tipo_filtro = 2
                cor = "#00cc66"
                titulo = "REPAROS POR TÉCNICO"
            
            dados = self.dados.get_os_por_tecnico(data_inicio, data_fim, tipo_filtro, status, id_tecnico)
            
            # Totalizador
            total_os = sum(item['total_os'] for item in dados)
            total_concluidos = sum(item['concluidos'] for item in dados)
            
            frame_total = ctk.CTkFrame(self.card_direito_content, fg_color="transparent")
            frame_total.pack(fill="x", pady=(0, 15))
            
            ctk.CTkLabel(
                frame_total,
                text=f"📊 TOTAL: {total_os} OS",
                font=('Arial', 14, 'bold'),
                text_color=cor
            ).pack(side="left")
            
            ctk.CTkLabel(
                frame_total,
                text=f"✅ Concluídos: {total_concluidos}",
                font=('Arial', 12),
                text_color="#cccccc"
            ).pack(side="right")
            
            # Tabela por técnico
            container = ctk.CTkFrame(self.card_direito_content, fg_color="transparent")
            container.pack(fill="both", expand=True)
            
            columns = ("Técnico", "Total OS", "Concluídos", "Suspensos")
            tree = ttk.Treeview(container, columns=columns, show="headings", height=15, style="Tecnico.Treeview")
            
            style = ttk.Style()
            style.configure("Tecnico.Treeview.Heading",
                            background="#1a1a2e",
                            foreground=cor,
                            font=('Arial', 10, 'bold'),
                            borderwidth=0)
            style.configure("Tecnico.Treeview",
                            background="#0f0f0f",
                            foreground="#cccccc",
                            fieldbackground="#0f0f0f",
                            rowheight=28,
                            borderwidth=0,
                            font=('Arial', 10))
            style.map("Tecnico.Treeview",
                      background=[('selected', cor)])
            
            for col in columns:
                tree.heading(col, text=col)
                if col == "Técnico":
                    tree.column(col, width=180)
                else:
                    tree.column(col, width=100)
            
            for i, item in enumerate(dados):
                tag = 'even' if i % 2 == 0 else 'odd'
                tree.insert("", "end", values=(
                    item['tecnico'],
                    item['total_os'],
                    item['concluidos'],
                    item['suspensos']
                ), tags=(tag,))
            
            tree.tag_configure('even', background='#0f0f0f')
            tree.tag_configure('odd', background='#1a1a2e')
            
            tree.pack(side="left", fill="both", expand=True)
            
            scrollbar = ttk.Scrollbar(container, orient="vertical", command=tree.yview)
            scrollbar.pack(side="right", fill="y")
            tree.configure(yscrollcommand=scrollbar.set)

    def on_linha_duplo_clique(self, event):
        """Abre um dialog com os detalhes completos da OS ao dar duplo clique"""
        selection = self.tabela_esquerda.selection()
        if not selection:
            return
        
        valores = self.tabela_esquerda.item(selection[0], 'values')
        if not valores:
            return
        
        numero_os = valores[0]
        
        from app.controller.ordem_servico_controller import OrdemServicoController
        os_controller = OrdemServicoController()
        os = os_controller.buscar_por_numero(numero_os)
        
        if not os:
            from tkinter import messagebox
            messagebox.showerror("Erro", f"OS {numero_os} não encontrada!")
            return
        
        # Criar dialog
        dialog = ctk.CTkToplevel(self)
        dialog.title(f"Detalhes da OS {numero_os}")
        dialog.geometry("700x600")
        dialog.transient(self)
        dialog.grab_set()
        
        # Centralizar
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (700 // 2)
        y = (dialog.winfo_screenheight() // 2) - (600 // 2)
        dialog.geometry(f"+{x}+{y}")
        
        # Frame principal
        main_frame = ctk.CTkFrame(dialog, fg_color="#0a0a0a")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Título
        ctk.CTkLabel(
            main_frame,
            text=f"📋 OS Nº {numero_os}",
            font=('Arial', 18, 'bold'),
            text_color="#00ff88"
        ).pack(anchor="w", pady=(0, 15))
        
        # Frame de informações
        info_frame = ctk.CTkFrame(main_frame, fg_color="#1a1a2e", corner_radius=12)
        info_frame.pack(fill="x", pady=(0, 15))
        
        info_frame.grid_columnconfigure(0, weight=1)
        info_frame.grid_columnconfigure(1, weight=1)
        
        campos = [
            ("Nº OS:", str(os['numero'])),
            ("Técnico:", os['tecnico_nome']),
            ("WAN/Piloto:", os['wan_piloto']),
            ("Data:", os['data']),
            ("Início Execução:", os['inicio_execucao']),
            ("Fim Execução:", os['fim_execucao']),
            ("Tipo:", os['tipo_nome']),
            ("Status:", os['status_nome'])
        ]
        
        for i, (label, valor) in enumerate(campos):
            ctk.CTkLabel(info_frame, text=label, font=('Arial', 12, 'bold'), text_color="#ff6b00").grid(row=i, column=0, sticky="w", padx=15, pady=8)
            ctk.CTkLabel(info_frame, text=valor, font=('Arial', 12), text_color="#cccccc").grid(row=i, column=1, sticky="w", padx=15, pady=8)
        
        # Frame do carimbo
        carimbo_frame = ctk.CTkFrame(main_frame, fg_color="#1a1a2e", corner_radius=12)
        carimbo_frame.pack(fill="both", expand=True)
        
        ctk.CTkLabel(
            carimbo_frame,
            text="📝 CARIMBO",
            font=('Arial', 12, 'bold'),
            text_color="#00ff88"
        ).pack(anchor="w", padx=15, pady=(10, 5))
        
        text_carimbo = ctk.CTkTextbox(carimbo_frame, font=('Arial', 11), fg_color="#0f0f0f")
        text_carimbo.pack(fill="both", expand=True, padx=15, pady=10)
        text_carimbo.insert("1.0", os['carimbo'])
        text_carimbo.configure(state="disabled")
        
        # Botão fechar
        ctk.CTkButton(
            main_frame,
            text="Fechar",
            fg_color="#ff3333",
            hover_color="#cc0000",
            width=100,
            command=dialog.destroy
        ).pack(pady=15)