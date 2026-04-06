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
        
        # Card direito - Detalhes (Repetido vs Referência)
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
            text="📄 Comparação: Repetido x Referência",
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
    
    def mostrar_comparacao(self, index):
        """Mostra a comparação entre a OS repetida e a OS de referência"""
        if index >= len(self.dados_repetidos):
            return
        
        item = self.dados_repetidos[index]
        
        # Limpar frame de detalhes
        for widget in self.detalhes_frame.winfo_children():
            widget.destroy()
        
        # Título da comparação
        title = ctk.CTkLabel(
            self.detalhes_frame,
            text=f"Comparação: OS {item['numero_bd_repetido']} → OS {item['numero_bd_referencia']}",
            font=FONTS['subtitle'],
            text_color=COLORS['primary']
        )
        title.pack(pady=10)
        
        # Frame para as duas colunas (lado a lado)
        columns_frame = ctk.CTkFrame(self.detalhes_frame, fg_color="transparent")
        columns_frame.pack(fill="both", expand=True, pady=10)
        
        # ==================== COLUNA ESQUERDA - REPETIDO (AMARELO) ====================
        left_frame = ctk.CTkFrame(columns_frame, fg_color=COLORS['warning_bg'], corner_radius=10)
        left_frame.pack(side="left", fill="both", expand=True, padx=(0, 5))
        
        left_title = ctk.CTkLabel(
            left_frame,
            text="🔄 OS REPETIDA",
            font=FONTS['body_bold'],
            text_color=COLORS['warning']
        )
        left_title.pack(pady=10)
        
        # Separador
        sep_left = ctk.CTkFrame(left_frame, height=1, fg_color=COLORS['warning'])
        sep_left.pack(fill="x", padx=10, pady=5)
        
        # Buscar dados completos da OS repetida
        dados_completos_repetido = self.buscar_os_completa(item['numero_bd_repetido'])
        
        if dados_completos_repetido:
            self.montar_detalhes_os(left_frame, dados_completos_repetido)
        else:
            # Fallback com dados básicos
            dados_repetido = [
                ("Nº BD:", item['numero_bd_repetido']),
                ("Data:", item['data_repetido']),
                ("WAN/Piloto:", item['wan_piloto']),
                ("Cliente:", item['cliente']),
                ("Causa Raiz:", item['causa_raiz_repetido'])
            ]
            for label, valor in dados_repetido:
                self.adicionar_linha_detalhe(left_frame, label, valor)
        
        # ==================== COLUNA DIREITA - REFERÊNCIA (VERDE) ====================
        right_frame = ctk.CTkFrame(columns_frame, fg_color=COLORS['success_bg'], corner_radius=10)
        right_frame.pack(side="right", fill="both", expand=True, padx=(5, 0))
        
        right_title = ctk.CTkLabel(
            right_frame,
            text="📋 OS REFERÊNCIA",
            font=FONTS['body_bold'],
            text_color=COLORS['success']
        )
        right_title.pack(pady=10)
        
        # Separador
        sep_right = ctk.CTkFrame(right_frame, height=1, fg_color=COLORS['success'])
        sep_right.pack(fill="x", padx=10, pady=5)
        
        # Buscar dados completos da OS referência
        dados_completos_ref = self.buscar_os_completa(item['numero_bd_referencia'])
        
        if dados_completos_ref:
            self.montar_detalhes_os(right_frame, dados_completos_ref)
        else:
            # Fallback com dados básicos
            dados_referencia = [
                ("Nº BD:", item['numero_bd_referencia']),
                ("Data:", item['data_referencia']),
                ("Técnico:", item['tecnico_referencia']),
                ("Causa Raiz:", item['causa_raiz_referencia'])
            ]
            for label, valor in dados_referencia:
                self.adicionar_linha_detalhe(right_frame, label, valor)
    
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
            'materiais': os_encontrada.materiais_utilizados if os_encontrada.materiais_utilizados else "-",
            'acao': os_encontrada.acao if os_encontrada.acao else "-",
            'contato': os_encontrada.contato_responsavel if os_encontrada.contato_responsavel else "-",
            'observacoes': os_encontrada.observacoes if os_encontrada.observacoes else "-"
        }
    
    def montar_detalhes_os(self, parent, dados):
        """Monta a exibição dos detalhes da OS"""
        
        # Informações Gerais
        secao = ctk.CTkLabel(
            parent,
            text="📋 Informações Gerais",
            font=FONTS['body_bold'],
            text_color=COLORS['text_primary']
        )
        secao.pack(anchor="w", padx=10, pady=(10, 5))
        
        gerais = [
            ("Nº BD:", dados['numero_bd']),
            ("Tipo:", dados['tipo']),
            ("Status:", dados['status']),
            ("Data Abertura:", dados['data_abertura']),
            ("Data Conclusão:", dados['data_conclusao'])
        ]
        
        for label, valor in gerais:
            self.adicionar_linha_detalhe(parent, label, valor)
        
        # Responsáveis
        secao = ctk.CTkLabel(
            parent,
            text="👥 Responsáveis",
            font=FONTS['body_bold'],
            text_color=COLORS['text_primary']
        )
        secao.pack(anchor="w", padx=10, pady=(10, 5))
        
        self.adicionar_linha_detalhe(parent, "Técnico:", dados['tecnico'])
        self.adicionar_linha_detalhe(parent, "Cliente:", dados['cliente'])
        if dados['endereco'] != "-":
            self.adicionar_linha_detalhe(parent, "Endereço:", dados['endereco'])
        
        # Produto
        secao = ctk.CTkLabel(
            parent,
            text="📦 Produto",
            font=FONTS['body_bold'],
            text_color=COLORS['text_primary']
        )
        secao.pack(anchor="w", padx=10, pady=(10, 5))
        
        produto = [
            ("Descrição:", dados['produto_desc']),
            ("Designador:", dados['produto_designador']),
            ("WAN/Piloto:", dados['produto_wan'])
        ]
        
        for label, valor in produto:
            self.adicionar_linha_detalhe(parent, label, valor)
        
        # Informações da OS
        secao = ctk.CTkLabel(
            parent,
            text="📝 Informações da OS",
            font=FONTS['body_bold'],
            text_color=COLORS['text_primary']
        )
        secao.pack(anchor="w", padx=10, pady=(10, 5))
        
        info_os = [
            ("Causa Raiz:", dados['causa_raiz']),
            ("Materiais:", dados['materiais']),
            ("Ação:", dados['acao']),
            ("Contato:", dados['contato'])
        ]
        
        for label, valor in info_os:
            self.adicionar_linha_detalhe(parent, label, valor)
        
        # Observações (se houver)
        if dados['observacoes'] and dados['observacoes'] != "-":
            self.adicionar_linha_detalhe(parent, "Observações:", dados['observacoes'][:200] + ("..." if len(dados['observacoes']) > 200 else ""))
    
    def adicionar_linha_detalhe(self, parent, label, valor):
        """Adiciona uma linha de detalhe formatada"""
        frame = ctk.CTkFrame(parent, fg_color="transparent")
        frame.pack(fill="x", padx=10, pady=3)
        
        lbl_label = ctk.CTkLabel(
            frame,
            text=label,
            font=FONTS['body_bold'],
            text_color=COLORS['text_secondary'],
            width=100,
            anchor="w"
        )
        lbl_label.pack(side="left")
        
        lbl_valor = ctk.CTkLabel(
            frame,
            text=valor,
            font=FONTS['body'],
            text_color=COLORS['text_primary'],
            anchor="w",
            wraplength=280,
            justify="left"
        )
        lbl_valor.pack(side="left", padx=(10, 0), fill="x", expand=True)