# app/frontend/screens/os_tecnico.py

import customtkinter as ctk
from app.frontend.styles import COLORS, FONTS
from app.frontend.components import TabelaInterativa
from app.tools.periodos import obter_periodos_disponiveis, formatar_periodo
from app.tools.ordem_servivo.count_os_tecnico import listar_os_por_tecnico_periodo
from app.controller.tecnico_controller import TecnicoController
from app.controller.ordem_servico_controller import OrdemServicoController
from app.controller.produto_controller import ProdutoController
from app.controller.cliente_controller import ClienteController
from app.controller.endereco_controller import EnderecoController
from app.bd.cliente_endereco_repository import ClienteEnderecoRepository


class OSTecnicoScreen(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")
        self.pack(fill="both", expand=True)
        
        self.tecnicos = []
        self.periodos = []
        self.periodos_labels = []
        self.dados_os = []
        
        self.create_widgets()
        self.carregar_tecnicos()
        self.carregar_periodos()
    
    def create_widgets(self):
        # Frame de seleção
        select_frame = ctk.CTkFrame(self, fg_color=COLORS['bg_card'], corner_radius=12, border_width=1, border_color=COLORS['border'])
        select_frame.pack(fill="x", pady=10, padx=10)
        
        # Técnico
        label_tec = ctk.CTkLabel(
            select_frame,
            text="Técnico:",
            font=FONTS['body_bold'],
            text_color=COLORS['text_primary']
        )
        label_tec.grid(row=0, column=0, padx=15, pady=12, sticky="w")
        
        self.tecnico_var = ctk.StringVar()
        self.tecnico_combo = ctk.CTkComboBox(
            select_frame,
            values=[],
            variable=self.tecnico_var,
            width=250,
            state="readonly"
        )
        self.tecnico_combo.grid(row=0, column=1, padx=10, pady=12)
        
        # Período
        label_per = ctk.CTkLabel(
            select_frame,
            text="Período:",
            font=FONTS['body_bold'],
            text_color=COLORS['text_primary']
        )
        label_per.grid(row=0, column=2, padx=15, pady=12, sticky="w")
        
        self.periodo_var = ctk.StringVar()
        self.periodo_combo = ctk.CTkComboBox(
            select_frame,
            values=[],
            variable=self.periodo_var,
            width=200,
            state="readonly"
        )
        self.periodo_combo.grid(row=0, column=3, padx=10, pady=12)
        
        btn = ctk.CTkButton(
            select_frame,
            text="Gerar",
            command=self.gerar_relatorio,
            fg_color=COLORS['primary'],
            hover_color=COLORS['primary_dark'],
            width=100
        )
        btn.grid(row=0, column=4, padx=20, pady=12)
        
        # Frame principal com dois cards
        main_frame = ctk.CTkFrame(self, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Card esquerdo - Tabela
        self.table_card = ctk.CTkFrame(main_frame, fg_color=COLORS['bg_card'], corner_radius=12, border_width=1, border_color=COLORS['border'])
        self.table_card.pack(side="left", fill="both", expand=True, padx=(0, 5))
        
        # Card direito - Detalhes
        self.detail_card = ctk.CTkFrame(main_frame, fg_color=COLORS['bg_card'], corner_radius=12, border_width=1, border_color=COLORS['border'])
        self.detail_card.pack(side="right", fill="both", expand=True, padx=(5, 0))
        
        # Títulos dos cards
        table_title = ctk.CTkLabel(
            self.table_card,
            text="📋 Lista de OS",
            font=FONTS['subtitle'],
            text_color=COLORS['primary']
        )
        table_title.pack(pady=10)
        
        detail_title = ctk.CTkLabel(
            self.detail_card,
            text="📄 Detalhes da OS",
            font=FONTS['subtitle'],
            text_color=COLORS['primary']
        )
        detail_title.pack(pady=10)
        
        # Frame para a tabela
        self.tabela_frame = ctk.CTkFrame(self.table_card, fg_color="transparent")
        self.tabela_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.mensagem = ctk.CTkLabel(
            self.tabela_frame,
            text="Selecione técnico, período e clique em Gerar",
            font=FONTS['body'],
            text_color=COLORS['text_secondary']
        )
        self.mensagem.pack(expand=True)
        
        # Frame para detalhes
        self.detalhes_frame = ctk.CTkScrollableFrame(self.detail_card, fg_color="transparent")
        self.detalhes_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.detalhe_vazio = ctk.CTkLabel(
            self.detalhes_frame,
            text="Clique em uma OS para ver os detalhes",
            font=FONTS['body'],
            text_color=COLORS['text_secondary']
        )
        self.detalhe_vazio.pack(expand=True)
    
    def carregar_tecnicos(self):
        tecnico_controller = TecnicoController()
        self.tecnicos = tecnico_controller.listar_tecnicos()
        valores = [f"{t.id} - {t.nome}" for t in self.tecnicos]
        self.tecnico_combo.configure(values=valores)
        if valores:
            self.tecnico_combo.set(valores[0])
    
    def carregar_periodos(self):
        self.periodos = obter_periodos_disponiveis(filtrar_concluidas=True, excluir_apoio=True)
        self.periodos_labels = [formatar_periodo(di, df) for di, df in self.periodos]
        self.periodo_combo.configure(values=self.periodos_labels)
        if self.periodos_labels:
            self.periodo_combo.set(self.periodos_labels[0])
    
    def gerar_relatorio(self):
        if not self.periodos or not self.periodos_labels:
            return
        
        if not self.tecnico_var.get():
            return
        
        try:
            idx = self.periodos_labels.index(self.periodo_var.get())
        except ValueError:
            return
        
        data_inicio, data_fim = self.periodos[idx]
        
        try:
            tecnico_id = int(self.tecnico_var.get().split(" - ")[0])
        except (ValueError, IndexError):
            return
        
        resultado = listar_os_por_tecnico_periodo(tecnico_id, data_inicio, data_fim)
        
        # Limpar tabela
        for widget in self.tabela_frame.winfo_children():
            widget.destroy()
        
        self.dados_os = resultado['dados']
        
        if not self.dados_os:
            msg = ctk.CTkLabel(
                self.tabela_frame,
                text="Nenhuma OS encontrada no período",
                font=FONTS['body'],
                text_color=COLORS['text_secondary']
            )
            msg.pack(expand=True)
            return
        
        # Criar tabela
        headers = ["Nº BD", "Tipo", "Data", "Cliente", "WAN"]
        larguras = [100, 80, 100, 180, 120]
        
        # Guardar referência para a tabela
        self.tabela = TabelaInterativa(self.tabela_frame, headers, larguras, self.mostrar_detalhes)
        self.tabela.pack(fill="both", expand=True)
        
        for item in self.dados_os:
            self.tabela.adicionar_linha([
                item['numero_bd'],
                item['tipo'],
                item['data_abertura'],
                item['cliente'][:18],
                item['produto_wan'][:12]
            ])
    
    def mostrar_detalhes(self, index):
        """Mostra os detalhes da OS selecionada"""
        if index >= len(self.dados_os):
            return
        
        os = self.dados_os[index]
        
        # Limpar frame de detalhes
        for widget in self.detalhes_frame.winfo_children():
            widget.destroy()
        
        # Buscar detalhes completos da OS
        os_controller = OrdemServicoController()
        produto_controller = ProdutoController()
        cliente_controller = ClienteController()
        endereco_controller = EnderecoController()
        cliente_endereco_repo = ClienteEnderecoRepository()
        
        # Encontrar a OS completa
        ordens = os_controller.listar_ordens()
        os_completa = None
        for o in ordens:
            if str(o.number_bd) == str(os['numero_bd']):
                os_completa = o
                break
        
        if not os_completa:
            # Fallback: mostrar dados básicos
            self.mostrar_detalhes_basicos(os)
            return
        
        # Buscar produto
        produtos = produto_controller.listar_produtos()
        produto_info = None
        for p in produtos:
            if p.id_produto == os_completa.id_produto:
                produto_info = p
                break
        
        # Buscar cliente e endereço
        clientes = cliente_controller.listar_clientes()
        relacionamentos = cliente_endereco_repo.listar()
        enderecos = endereco_controller.listar_enderecos()
        
        nome_cliente = os['cliente'] if os['cliente'] != "-" else "-"
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
        
        # Criar layout de detalhes
        detalhes = [
            ("📋 INFORMAÇÕES GERAIS", ""),
            ("Nº BD:", os_completa.number_bd),
            ("Tipo:", os_completa.tipo if os_completa.tipo else "-"),
            ("Status:", "✅ Concluída" if os_completa.concluida else "🟡 Em andamento"),
            ("Data Abertura:", os_completa.data_criacao[:10] if os_completa.data_criacao else "-"),
            ("Data Conclusão:", os_completa.data_conclusao[:10] if os_completa.data_conclusao else "-"),
            ("", ""),
            ("👥 CLIENTE", ""),
            ("Nome:", nome_cliente),
            ("Endereço:", endereco_cliente),
            ("", ""),
            ("📦 PRODUTO", ""),
            ("Descrição:", produto_info.descricao if produto_info else "-"),
            ("Designador:", produto_info.designador if produto_info else "-"),
            ("WAN/Piloto:", produto_info.wan_piloto if produto_info else "-"),
            ("", ""),
            ("📝 INFORMAÇÕES DA OS", ""),
            ("Causa Raiz:", os_completa.causa_raiz if os_completa.causa_raiz else "-"),
            ("Materiais Utilizados:", os_completa.materiais_utilizados if os_completa.materiais_utilizados else "-"),
            ("Ação Realizada:", os_completa.acao if os_completa.acao else "-"),
            ("Contato Responsável:", os_completa.contato_responsavel if os_completa.contato_responsavel else "-"),
            ("Observações:", (os_completa.observacoes[:300] + "...") if os_completa.observacoes and len(os_completa.observacoes) > 300 else (os_completa.observacoes if os_completa.observacoes else "-"))
        ]
        
        for titulo, valor in detalhes:
            if titulo == "":
                continue
            if valor == "":
                lbl = ctk.CTkLabel(
                    self.detalhes_frame,
                    text=titulo,
                    font=FONTS['body_bold'],
                    text_color=COLORS['primary']
                )
                lbl.pack(anchor="w", pady=(10, 5))
            else:
                frame = ctk.CTkFrame(self.detalhes_frame, fg_color="transparent")
                frame.pack(fill="x", pady=2)
                
                lbl_tit = ctk.CTkLabel(
                    frame,
                    text=titulo,
                    font=FONTS['body_bold'],
                    text_color=COLORS['text_secondary'],
                    width=140,
                    anchor="w"
                )
                lbl_tit.pack(side="left")
                
                lbl_val = ctk.CTkLabel(
                    frame,
                    text=valor,
                    font=FONTS['body'],
                    text_color=COLORS['text_primary'],
                    anchor="w",
                    wraplength=350,
                    justify="left"
                )
                lbl_val.pack(side="left", padx=(10, 0))
    
    def mostrar_detalhes_basicos(self, os):
        """Fallback: mostrar dados básicos quando não encontra a OS completa"""
        detalhes = [
            ("📋 INFORMAÇÕES GERAIS", ""),
            ("Nº BD:", os['numero_bd']),
            ("Tipo:", os['tipo']),
            ("Data Abertura:", os['data_abertura']),
            ("", ""),
            ("👥 CLIENTE", ""),
            ("Nome:", os['cliente']),
            ("", ""),
            ("📦 PRODUTO", ""),
            ("WAN/Piloto:", os['produto_wan']),
        ]
        
        for titulo, valor in detalhes:
            if titulo == "":
                continue
            if valor == "":
                lbl = ctk.CTkLabel(
                    self.detalhes_frame,
                    text=titulo,
                    font=FONTS['body_bold'],
                    text_color=COLORS['primary']
                )
                lbl.pack(anchor="w", pady=(10, 5))
            else:
                frame = ctk.CTkFrame(self.detalhes_frame, fg_color="transparent")
                frame.pack(fill="x", pady=2)
                
                lbl_tit = ctk.CTkLabel(
                    frame,
                    text=titulo,
                    font=FONTS['body_bold'],
                    text_color=COLORS['text_secondary'],
                    width=140,
                    anchor="w"
                )
                lbl_tit.pack(side="left")
                
                lbl_val = ctk.CTkLabel(
                    frame,
                    text=valor,
                    font=FONTS['body'],
                    text_color=COLORS['text_primary'],
                    anchor="w",
                    wraplength=350,
                    justify="left"
                )
                lbl_val.pack(side="left", padx=(10, 0))