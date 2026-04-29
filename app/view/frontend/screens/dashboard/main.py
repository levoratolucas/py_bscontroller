import customtkinter as ctk
from tkinter import messagebox, simpledialog
from app.view.frontend.styles import COLORS, FONTS
from app.controller.ordem_servico_controller import OrdemServicoController
from app.controller.tecnico_controller import TecnicoController
from app.controller.relatorio_controller import RelatorioController
from app.view.frontend.screens.dashboard.dados import DadosDashboard
from app.view.frontend.screens.dashboard.cards import CardOS, CardRepetidos, CardAPU
from app.view.frontend.screens.dashboard.components import GraficoBarras, BotoesNavegacao
from app.view.frontend.screens.dashboard.tools_main import FormatadorDashboard


class DashboardScreen(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent, fg_color="transparent")
        self.pack(fill="both", expand=True)
        
        self.app = app
        self.os_controller = OrdemServicoController()
        self.tecnico_controller = TecnicoController()
        self.dados_dashboard = DadosDashboard()
        
        self.graficos = []
        
        self.setup_ui()
        self.carregar_dados()

    def setup_ui(self):
        # Frame principal
        self.main_frame = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Título
        ctk.CTkLabel(
            self.main_frame,
            text="📊 DASHBOARD - VIVO OS",
            font=FONTS['title'],
            text_color=COLORS['primary']
        ).pack(anchor="w", pady=(0, 20))

        # ================= 3 CARDS PRINCIPAIS =================
        cards_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        cards_frame.pack(fill="x", pady=(0, 20))

        cards_frame.grid_columnconfigure(0, weight=1)
        cards_frame.grid_columnconfigure(1, weight=1)
        cards_frame.grid_columnconfigure(2, weight=1)

        # Card 1: Ordem de Serviço
        self.card_os = CardOS(cards_frame, 0)
        
        # Card 2: Repetidos
        self.card_repetidos = CardRepetidos(cards_frame, 1)
        
        # Card 3: APU
        self.card_apu = CardAPU(cards_frame, 2)

        # ================= GRÁFICO DE BARRAS =================
        graficos_frame = ctk.CTkFrame(self.main_frame, fg_color=COLORS['bg_card'], corner_radius=12, 
                                       border_width=1, border_color=COLORS['border'])
        graficos_frame.pack(fill="x", pady=(0, 20))

        ctk.CTkLabel(
            graficos_frame,
            text="📊 MÉTRICAS POR TÉCNICO",
            font=FONTS['subtitle'],
            text_color=COLORS['primary']
        ).pack(anchor="w", padx=15, pady=(10, 5))

        ctk.CTkLabel(
            graficos_frame,
            text="Comparativo de Efetividade, TMR, APU e ADP",
            font=FONTS['small'],
            text_color=COLORS['text_secondary']
        ).pack(anchor="w", padx=15, pady=(0, 10))

        # Container para os gráficos em grid
        self.graficos_grid_frame = ctk.CTkFrame(graficos_frame, fg_color="transparent")
        self.graficos_grid_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # ================= BOTÕES DE NAVEGAÇÃO =================
        botoes_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        botoes_frame.pack(fill="x", pady=(0, 20))

        for i in range(3):
            botoes_frame.grid_columnconfigure(i, weight=1)

        callbacks = [
            ("📝 Nova OS", "Cadastrar ordem de serviço", self.nova_os),
            ("🔍 Consultar", "Buscar OS por número", self.consultar),
            ("📈 Relatórios", "Análise de dados", self.relatorios)
        ]
        self.botoes_nav = BotoesNavegacao(botoes_frame, callbacks)

    def carregar_dados(self):
        """Carrega todos os dados do dashboard"""
        data_inicio, data_fim = self.dados_dashboard.get_periodo_atual()
        
        dados = self.dados_dashboard.carregar_todos_dados(data_inicio, data_fim)
        
        # Atualizar cards
        self.card_os.atualizar(dados['stats_os'])
        self.card_repetidos.atualizar(
            dados['total_repeticoes'], 
            dados['percentual_repeticoes'],
            dados['ranking_ofensores'],
            dados['medalhas']
        )
        self.card_apu.atualizar(dados['media_apu'], dados['ranking_apu'], dados['medalhas'])
        
        # Desenhar gráficos
        self.desenhar_graficos(dados['metricas'])

    def desenhar_graficos(self, metricas):
        """Desenha gráfico de barras horizontais para comparar técnicos"""
        # Limpar gráficos existentes
        for grafico in self.graficos:
            grafico.get_frame().destroy()
        self.graficos.clear()
        
        if not metricas:
            return
        
        # Filtrar técnicos com OS
        tecnicos_validos = [m for m in metricas if m.get('total_os', 0) > 0]
        
        if not tecnicos_validos:
            return
        
        # Ordenar técnicos por nome
        tecnicos_validos.sort(key=lambda x: x['tecnico'])
        
        # Configurar grid - 2 por linha
        cols = 2
        for idx, tecnico in enumerate(tecnicos_validos):
            row = idx // cols
            col = idx % cols
            
            # Criar gráfico
            grafico = GraficoBarras(self.graficos_grid_frame, tecnico, metricas)
            grafico.get_frame().grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
            self.graficos.append(grafico)
        
        # Ajustar tamanho das colunas do grid
        for i in range(cols):
            self.graficos_grid_frame.grid_columnconfigure(i, weight=1)

    def nova_os(self):
        self.app.mostrar_tela("nova_os")
    
    def consultar(self):
        numero = simpledialog.askstring("Consultar OS", "Digite o Nº da OS:")
        if numero:
            os = self.os_controller.buscar_por_numero(numero)
            if os:
                msg = f"Nº OS: {os['numero']}\n"
                msg += f"Técnico: {os['tecnico_nome']}\n"
                msg += f"WAN/Piloto: {os['wan_piloto']}\n"
                msg += f"Tipo: {os['tipo_nome']}\n"
                msg += f"Status: {os['status_nome']}\n"
                msg += f"Data: {os['data']}\n"
                msg += f"Início: {os['inicio_execucao']}\n"
                msg += f"Fim: {os['fim_execucao']}\n"
                msg += f"Carimbo: {os['carimbo'][:200]}"
                messagebox.showinfo("OS Encontrada", msg)
            else:
                messagebox.showwarning("Não encontrado", f"OS {numero} não encontrada!")
    
    def relatorios(self):
        self.app.mostrar_tela("relatorios")