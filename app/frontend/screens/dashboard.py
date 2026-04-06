# app/frontend/screens/dashboard.py

import customtkinter as ctk
from app.frontend.styles import COLORS, FONTS
from app.frontend.components import KPICard, ActionCard
from app.controller.ordem_servico_controller import OrdemServicoController
from app.controller.tecnico_controller import TecnicoController
from app.controller.cliente_controller import ClienteController


class DashboardScreen(ctk.CTkFrame):
    def __init__(self, parent, on_navigate):
        super().__init__(parent, fg_color=COLORS['bg_main'])
        self.on_navigate = on_navigate
        self.pack(fill="both", expand=True)
        
        self.load_data()
        self.create_widgets()
    
    def load_data(self):
        os_controller = OrdemServicoController()
        tecnico_controller = TecnicoController()
        cliente_controller = ClienteController()
        
        ordens = os_controller.listar_ordens()
        self.total_os = len(ordens)
        self.concluidas = len([os for os in ordens if os.concluida])
        self.em_andamento = self.total_os - self.concluidas
        self.total_tecnicos = len(tecnico_controller.listar_tecnicos())
        self.total_clientes = len(cliente_controller.listar_clientes())
        
        # Últimas 5 OS
        self.ultimas_os = sorted(ordens, key=lambda x: x.data_criacao, reverse=True)[:5]
    
    def create_widgets(self):
        # Scrollable frame para todo o conteúdo
        scroll_frame = ctk.CTkScrollableFrame(self, fg_color="transparent")
        scroll_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Título
        title = ctk.CTkLabel(
            scroll_frame,
            text="Dashboard",
            font=FONTS['title'],
            text_color=COLORS['text_light']
        )
        title.pack(anchor="w", pady=(0, 20))
        
        # KPIs
        kpi_frame = ctk.CTkFrame(scroll_frame, fg_color="transparent")
        kpi_frame.pack(fill="x", pady=10)
        
        KPICard(kpi_frame, "Total OS", self.total_os, "📊", COLORS['primary'])
        KPICard(kpi_frame, "Concluídas", self.concluidas, "✅", COLORS['success'])
        KPICard(kpi_frame, "Em andamento", self.em_andamento, "🟡", COLORS['warning'])
        KPICard(kpi_frame, "Técnicos", self.total_tecnicos, "👤", COLORS['primary'])
        
        # Ações rápidas
        actions_frame = ctk.CTkFrame(scroll_frame, fg_color="transparent")
        actions_frame.pack(fill="x", pady=20)
        
        ActionCard(
            actions_frame,
            "Nova OS",
            "Criar uma nova ordem de serviço",
            "➕",
            lambda: self.on_navigate("nova_os")
        )
        
        ActionCard(
            actions_frame,
            "Consultar OS",
            "Buscar OS por número ou cliente",
            "🔍",
            lambda: self.on_navigate("consultar")
        )
        
        ActionCard(
            actions_frame,
            "Relatórios",
            "Análise de dados e estatísticas",
            "📈",
            lambda: self.on_navigate("relatorios")
        )
        
        ActionCard(
            actions_frame,
            "Administração",
            "Gerenciar técnicos e clientes",
            "⚙️",
            lambda: self.on_navigate("admin")
        )
        
        # Últimas OS
        ultimas_frame = ctk.CTkFrame(scroll_frame, fg_color="transparent")
        ultimas_frame.pack(fill="both", expand=True, pady=20)
        
        label = ctk.CTkLabel(
            ultimas_frame,
            text="📋 Últimas Ordens de Serviço",
            font=FONTS['subtitle'],
            text_color=COLORS['text_light']
        )
        label.pack(anchor="w", pady=(0, 10))
        
        # Tabela de últimas OS
        table_frame = ctk.CTkFrame(ultimas_frame, fg_color=COLORS['bg_card'], corner_radius=12, border_width=1, border_color=COLORS['border'])
        table_frame.pack(fill="both", expand=True)
        
        # Headers
        headers_frame = ctk.CTkFrame(table_frame, fg_color=COLORS['bg_table_header'], corner_radius=0)
        headers_frame.pack(fill="x")
        
        headers = ["Nº BD", "Data", "Status"]
        for i, header in enumerate(headers):
            lbl = ctk.CTkLabel(
                headers_frame,
                text=header,
                font=FONTS['table_header'],
                text_color=COLORS['text_primary'],
                width=200
            )
            lbl.pack(side="left", padx=10, pady=8)
        
        # Dados
        for os in self.ultimas_os:
            row_frame = ctk.CTkFrame(table_frame, fg_color="transparent", corner_radius=0)
            row_frame.pack(fill="x")
            
            status = "✅ Concluída" if os.concluida else "🟡 Em andamento"
            status_color = COLORS['success'] if os.concluida else COLORS['warning']
            
            valores = [os.number_bd, os.data_criacao[:10], status]
            cores = [COLORS['text_primary'], COLORS['text_secondary'], status_color]
            
            for i, (val, cor) in enumerate(zip(valores, cores)):
                lbl = ctk.CTkLabel(
                    row_frame,
                    text=val,
                    font=FONTS['table_cell'],
                    text_color=cor,
                    width=200
                )
                lbl.pack(side="left", padx=10, pady=5)
            
            # Separador
            if os != self.ultimas_os[-1]:
                sep = ctk.CTkFrame(table_frame, height=1, fg_color=COLORS['divider'])
                sep.pack(fill="x")