# app/frontend/screens/repetidos.py

import customtkinter as ctk
from app.frontend.styles import COLORS, FONTS
from app.frontend.components import TabelaInterativa
from app.tools.periodos import obter_meses_disponiveis, formatar_mes, obter_primeiro_ultimo_dia_mes
from app.tools.ordem_servivo.count_os_tecnico import listar_repetidos_periodo
from app.controller.ordem_servico_controller import OrdemServicoController
from app.controller.produto_controller import ProdutoController
from app.controller.cliente_controller import ClienteController
from app.controller.endereco_controller import EnderecoController
from app.controller.tecnico_controller import TecnicoController
from app.bd.cliente_endereco_repository import ClienteEnderecoRepository


class RepetidosScreen(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")
        self.pack(fill="both", expand=True)
        
        self.meses = []
        self.meses_labels = []
        self.dados_repetidos = []
        
        self.create_widgets()
        self.carregar_meses()
    
    def create_widgets(self):
        # Frame de seleção
        select_frame = ctk.CTkFrame(self, fg_color=COLORS['bg_card'], corner_radius=12, border_width=1, border_color=COLORS['border'])
        select_frame.pack(fill="x", pady=10, padx=10)
        
        label = ctk.CTkLabel(
            select_frame,
            text="Selecione o mês:",
            font=FONTS['body_bold'],
            text_color=COLORS['text_primary']
        )
        label.pack(side="left", padx=15, pady=12)
        
        self.mes_var = ctk.StringVar()
        self.mes_combo = ctk.CTkComboBox(
            select_frame,
            values=[],
            variable=self.mes_var,
            width=250,
            state="readonly"
        )
        self.mes_combo.pack(side="left", padx=10, pady=12)
        
        btn = ctk.CTkButton(
            select_frame,
            text="Gerar",
            command=self.gerar_relatorio,
            fg_color=COLORS['primary'],
            hover_color=COLORS['primary_dark'],
            width=100
        )
        btn.pack(side="left", padx=10, pady=12)
        
        # Frame principal com dois cards
        main_frame = ctk.CTkFrame(self, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Card esquerdo - Tabela de Repetidos
        self.table_card = ctk.CTkFrame(main_frame, fg_color=COLORS['bg_card'], corner_radius=12, border_width=1, border_color=COLORS['border'])
        self.table_card.pack(side="left", fill="both", expand=True, padx=(0, 5))
        
        # Card direito - Detalhes
        self.detail_card = ctk.CTkFrame(main_frame, fg_color=COLORS['bg_card'], corner_radius=12, border_width=1, border_color=COLORS['border'])
        self.detail_card.pack(side="right", fill="both", expand=True, padx=(5, 0))
        
        # Títulos dos cards
        table_title = ctk.CTkLabel(
            self.table_card,
            text="🔄 OS Repetidas",
            font=FONTS['subtitle'],
            text_color=COLORS['primary']
        )
        table_title.pack(pady=10)
        
        detail_title = ctk.CTkLabel(
            self.detail_card,
            text="📄 Detalhes da Comparação",
            font=FONTS['subtitle'],
            text_color=COLORS['primary']
        )
        detail_title.pack(pady=10)
        
        # Frame para a tabela
        self.tabela_frame = ctk.CTkFrame(self.table_card, fg_color="transparent")
        self.tabela_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.mensagem = ctk.CTkLabel(
            self.tabela_frame,
            text="Selecione um mês e clique em Gerar",
            font=FONTS['body'],
            text_color=COLORS['text_secondary']
        )
        self.mensagem.pack(expand=True)
        
        # Frame para detalhes
        self.detalhes_frame = ctk.CTkScrollableFrame(self.detail_card, fg_color="transparent")
        self.detalhes_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.detalhe_vazio = ctk.CTkLabel(
            self.detalhes_frame,
            text="Clique em uma OS repetida para ver a comparação",
            font=FONTS['body'],
            text_color=COLORS['text_secondary']
        )
        self.detalhe_vazio.pack(expand=True)
    
    def carregar_meses(self):
        self.meses = obter_meses_disponiveis()
        self.meses_labels = [formatar_mes(ano, mes) for ano, mes in self.meses]
        self.mes_combo.configure(values=self.meses_labels)
        if self.meses_labels:
            self.mes_combo.set(self.meses_labels[0])
    
    def gerar_relatorio(self):
        if not self.meses or not self.meses_labels:
            return
        
        try:
            idx = self.meses_labels.index(self.mes_var.get())
        except ValueError:
            return
        
        ano, mes = self.meses[idx]
        
        data_inicio, data_fim = obter_primeiro_ultimo_dia_mes(ano, mes)
        resultado = listar_repetidos_periodo(data_inicio, data_fim)
        
        # Limpar tabela
        for widget in self.tabela_frame.winfo_children():
            widget.destroy()
        
        self.dados_repetidos = resultado['dados']
        
        if not self.dados_repetidos:
            msg = ctk.CTkLabel(
                self.tabela_frame,
                text="Nenhuma OS repetida encontrada no período",
                font=FONTS['body'],
                text_color=COLORS['text_secondary']
            )
            msg.pack(expand=True)
            
            # Limpar detalhes
            for widget in self.detalhes_frame.winfo_children():
                widget.destroy()
            vazio = ctk.CTkLabel(
                self.detalhes_frame,
                text="Nenhuma OS repetida encontrada",
                font=FONTS['body'],
                text_color=COLORS['text_secondary']
            )
            vazio.pack(expand=True)
            return
        
        # Criar tabela
        headers = ["Nº BD Rep", "Data", "WAN/Piloto", "Cliente", "Causa Raiz"]
        larguras = [100, 90, 130, 180, 200]
        
        self.tabela = TabelaInterativa(self.tabela_frame, headers, larguras, self.mostrar_comparacao)
        self.tabela.pack(fill="both", expand=True)
        
        for item in self.dados_repetidos:
            self.tabela.adicionar_linha([
                item['numero_bd_repetido'],
                item['data_repetido'],
                item['wan_piloto'][:14],
                item['cliente'][:18],
                item['causa_raiz_repetido'][:25]
            ])
        
        # Limpar detalhes
        for widget in self.detalhes_frame.winfo_children():
            widget.destroy()
        vazio = ctk.CTkLabel(
            self.detalhes_frame,
            text="Clique em uma OS repetida para ver a comparação",
            font=FONTS['body'],
            text_color=COLORS['text_secondary']
        )
        vazio.pack(expand=True)
    
    def buscar_os_completa(self, numero_bd):
        """Busca todos os detalhes de uma OS pelo número BD"""
        os_controller = OrdemServicoController()
        produto_controller = ProdutoController()
        cliente_controller = ClienteController()
        endereco_controller = EnderecoController()
        tecnico_controller = TecnicoController()
        cliente_endereco_repo = ClienteEnderecoRepository()
        
        ordens = os_controller.listar_ordens()
        os_encontrada = None
        for o in ordens:
            if str(o.number_bd) == str(numero_bd):
                os_encontrada = o
                break
        
        if not os_encontrada:
            return None
        
        # Buscar técnico
        tecnicos = tecnico_controller.listar_tecnicos()
        nome_tecnico = "-"
        for t in tecnicos:
            if t.id == os_encontrada.id_tecnico:
                nome_tecnico = t.nome
                break
        
        # Buscar produto
        produtos = produto_controller.listar_produtos()
        produto_info = None
        for p in produtos:
            if p.id_produto == os_encontrada.id_produto:
                produto_info = p
                break
        
        # Buscar cliente e endereço
        clientes = cliente_controller.listar_clientes()
        relacionamentos = cliente_endereco_repo.listar()
        enderecos = endereco_controller.listar_enderecos()
        
        nome_cliente = "-"
        endereco_cliente = "-"
        
        if produto_info:
            for rel in relacionamentos:
                if rel.id == produto_info.id_cliente_endereco:
                    for c in clientes:
                        if c.id_cliente == rel.id_cliente:
                            nome_cliente = c.nome
                    for e in enderecos:
                        if e.id_endereco == rel.id_endereco:
                            endereco_cliente = f"{e.logradouro}, {e.cidade}/{e.estado}"
                    break
        
        return {
            'numero_bd': os_encontrada.number_bd,
            'tipo': os_encontrada.tipo if os_encontrada.tipo else "-",
            'status': "Concluída" if os_encontrada.concluida else "Em andamento",
            'data_abertura': os_encontrada.data_criacao[:10] if os_encontrada.data_criacao else "-",
            'data_conclusao': os_encontrada.data_conclusao[:10] if os_encontrada.data_conclusao else "-",
            'tecnico': nome_tecnico,
            'cliente': nome_cliente,
            'endereco': endereco_cliente,
            'produto_desc': produto_info.descricao if produto_info else "-",
            'produto_designador': produto_info.designador if produto_info else "-",
            'produto_wan': produto_info.wan_piloto if produto_info else "-",
            'causa_raiz': os_encontrada.causa_raiz if os_encontrada.causa_raiz else "-",
            'acao': os_encontrada.acao if os_encontrada.acao else "-",
            'contato': os_encontrada.contato_responsavel if os_encontrada.contato_responsavel else "-",
            'observacoes': os_encontrada.observacoes if os_encontrada.observacoes else "-"
        }
    
    def mostrar_comparacao(self, index):
        """Mostra a comparação entre a OS repetida e a OS de referência"""
        if index >= len(self.dados_repetidos):
            return
        
        item = self.dados_repetidos[index]
        
        # Limpar frame de detalhes
        for widget in self.detalhes_frame.winfo_children():
            widget.destroy()
        
        # Buscar dados completos
        dados_repetido = self.buscar_os_completa(item['numero_bd_repetido'])
        dados_ref = self.buscar_os_completa(item['numero_bd_referencia'])
        
        # ==================== TOPO: CLIENTE, ENDEREÇO, PRODUTO ====================
        top_frame = ctk.CTkFrame(self.detalhes_frame, fg_color=COLORS['bg_card'], corner_radius=10, border_width=1, border_color=COLORS['border'])
        top_frame.pack(fill="x", pady=(0, 10))
        
        # Cliente
        cliente_frame = ctk.CTkFrame(top_frame, fg_color="transparent")
        cliente_frame.pack(fill="x", padx=15, pady=(10, 5))
        
        cliente_icon = ctk.CTkLabel(cliente_frame, text="🏢", font=("Inter", 14), text_color=COLORS['primary'])
        cliente_icon.pack(side="left", padx=(0, 5))
        
        cliente_label = ctk.CTkLabel(
            cliente_frame, 
            text=f"CLIENTE: {dados_repetido['cliente'] if dados_repetido else item['cliente']}",
            font=FONTS['body_bold'],
            text_color=COLORS['text_primary']
        )
        cliente_label.pack(side="left")
        
        # Endereço
        endereco_frame = ctk.CTkFrame(top_frame, fg_color="transparent")
        endereco_frame.pack(fill="x", padx=15, pady=5)
        
        endereco_icon = ctk.CTkLabel(endereco_frame, text="📍", font=("Inter", 14), text_color=COLORS['primary'])
        endereco_icon.pack(side="left", padx=(0, 5))
        
        endereco_texto = dados_repetido['endereco'] if dados_repetido and dados_repetido['endereco'] != "-" else "Endereço não informado"
        endereco_label = ctk.CTkLabel(
            endereco_frame,
            text=f"ENDEREÇO: {endereco_texto}",
            font=FONTS['body'],
            text_color=COLORS['text_secondary']
        )
        endereco_label.pack(side="left")
        
        # Produto
        produto_frame = ctk.CTkFrame(top_frame, fg_color="transparent")
        produto_frame.pack(fill="x", padx=15, pady=5)
        
        produto_icon = ctk.CTkLabel(produto_frame, text="📦", font=("Inter", 14), text_color=COLORS['primary'])
        produto_icon.pack(side="left", padx=(0, 5))
        
        if dados_repetido:
            produto_texto = f"PRODUTO: {dados_repetido['produto_desc']} ({dados_repetido['produto_designador']}) - WAN: {dados_repetido['produto_wan']}"
        else:
            produto_texto = f"PRODUTO: {item['wan_piloto']}"
        
        produto_label = ctk.CTkLabel(
            produto_frame,
            text=produto_texto,
            font=FONTS['body'],
            text_color=COLORS['text_secondary']
        )
        produto_label.pack(side="left")
        
        # Separador
        sep = ctk.CTkFrame(self.detalhes_frame, height=1, fg_color=COLORS['border'])
        sep.pack(fill="x", pady=10)
        
        # ==================== CARDS LADO A LADO ====================
        columns_frame = ctk.CTkFrame(self.detalhes_frame, fg_color="transparent")
        columns_frame.pack(fill="both", expand=True, pady=5)
        
        columns_frame.grid_columnconfigure(0, weight=1)
        columns_frame.grid_columnconfigure(1, weight=1)
        
        # ==================== CARD ESQUERDO - REPETIDO (AMARELO) ====================
        left_frame = ctk.CTkFrame(columns_frame, fg_color=COLORS['warning_bg'], corner_radius=10)
        left_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 5))
        
        left_title = ctk.CTkLabel(
            left_frame,
            text=f"🟡 OS REPETIDA\n{item['numero_bd_repetido']}",
            font=FONTS['body_bold'],
            text_color=COLORS['warning']
        )
        left_title.pack(pady=10)
        
        sep_left = ctk.CTkFrame(left_frame, height=1, fg_color=COLORS['warning'])
        sep_left.pack(fill="x", padx=10, pady=5)
        
        left_scroll = ctk.CTkScrollableFrame(left_frame, fg_color="transparent")
        left_scroll.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Causa Raiz
        self.adicionar_secao_detalhe(left_scroll, "⚠️ CAUSA RAIZ", "warning")
        causa_repetido = dados_repetido['causa_raiz'] if dados_repetido else item['causa_raiz_repetido']
        self.adicionar_linha_detalhe(left_scroll, causa_repetido, "warning")
        
        # Observações
        self.adicionar_secao_detalhe(left_scroll, "📝 OBSERVAÇÕES", "warning")
        obs_repetido = dados_repetido['observacoes'][:200] + ("..." if len(dados_repetido['observacoes']) > 200 else "") if dados_repetido and dados_repetido['observacoes'] else "-"
        self.adicionar_linha_detalhe(left_scroll, obs_repetido, "warning")
        
        # Ação Realizada
        self.adicionar_secao_detalhe(left_scroll, "🔧 AÇÃO REALIZADA", "warning")
        acao_repetido = dados_repetido['acao'] if dados_repetido else "-"
        self.adicionar_linha_detalhe(left_scroll, acao_repetido, "warning")
        
        # Contato Responsável
        self.adicionar_secao_detalhe(left_scroll, "📞 CONTATO RESPONSÁVEL", "warning")
        contato_repetido = dados_repetido['contato'] if dados_repetido else "-"
        self.adicionar_linha_detalhe(left_scroll, contato_repetido, "warning")
        
        # ==================== CARD DIREITO - REFERÊNCIA (VERDE) ====================
        right_frame = ctk.CTkFrame(columns_frame, fg_color=COLORS['success_bg'], corner_radius=10)
        right_frame.grid(row=0, column=1, sticky="nsew", padx=(5, 0))
        
        right_title = ctk.CTkLabel(
            right_frame,
            text=f"🟢 OS REFERÊNCIA\n{item['numero_bd_referencia']}",
            font=FONTS['body_bold'],
            text_color=COLORS['success']
        )
        right_title.pack(pady=10)
        
        sep_right = ctk.CTkFrame(right_frame, height=1, fg_color=COLORS['success'])
        sep_right.pack(fill="x", padx=10, pady=5)
        
        right_scroll = ctk.CTkScrollableFrame(right_frame, fg_color="transparent")
        right_scroll.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Causa Raiz
        self.adicionar_secao_detalhe(right_scroll, "⚠️ CAUSA RAIZ", "success")
        causa_ref = dados_ref['causa_raiz'] if dados_ref else item['causa_raiz_referencia']
        self.adicionar_linha_detalhe(right_scroll, causa_ref, "success")
        
        # Observações
        self.adicionar_secao_detalhe(right_scroll, "📝 OBSERVAÇÕES", "success")
        obs_ref = dados_ref['observacoes'][:200] + ("..." if len(dados_ref['observacoes']) > 200 else "") if dados_ref and dados_ref['observacoes'] else "-"
        self.adicionar_linha_detalhe(right_scroll, obs_ref, "success")
        
        # Ação Realizada
        self.adicionar_secao_detalhe(right_scroll, "🔧 AÇÃO REALIZADA", "success")
        acao_ref = dados_ref['acao'] if dados_ref else "-"
        self.adicionar_linha_detalhe(right_scroll, acao_ref, "success")
        
        # Contato Responsável
        self.adicionar_secao_detalhe(right_scroll, "📞 CONTATO RESPONSÁVEL", "success")
        contato_ref = dados_ref['contato'] if dados_ref else "-"
        self.adicionar_linha_detalhe(right_scroll, contato_ref, "success")
    
    def adicionar_secao_detalhe(self, parent, titulo, cor_tipo):
        """Adiciona um título de seção nos cards de detalhe"""
        cor = COLORS['warning'] if cor_tipo == "warning" else COLORS['success']
        lbl = ctk.CTkLabel(
            parent,
            text=titulo,
            font=FONTS['body_bold'],
            text_color=cor
        )
        lbl.pack(anchor="w", pady=(10, 5))
    
    def adicionar_linha_detalhe(self, parent, valor, cor_tipo):
        """Adiciona uma linha de detalhe formatada"""
        cor = COLORS['warning'] if cor_tipo == "warning" else COLORS['success']
        
        frame = ctk.CTkFrame(parent, fg_color="transparent")
        frame.pack(fill="x", pady=3)
        
        # Ponto colorido
        ponto = ctk.CTkLabel(frame, text="•", font=("Inter", 12, "bold"), text_color=cor, width=20, anchor="w")
        ponto.pack(side="left")
        
        # Valor
        lbl_valor = ctk.CTkLabel(
            frame,
            text=valor,
            font=FONTS['body'],
            text_color=COLORS['text_primary'],
            anchor="w",
            wraplength=280,
            justify="left"
        )
        lbl_valor.pack(side="left", padx=(0, 10), fill="x", expand=True)