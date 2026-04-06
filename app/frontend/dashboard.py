# app/frontend/screens/dashboard.py

import customtkinter as ctk
from datetime import datetime
from app.tools.periodos import obter_periodos_disponiveis
from app.tools.ordem_servivo.count_os_tecnico import contar_os_concluidas_por_tecnico
from app.controller.ordem_servico_controller import OrdemServicoController
from app.controller.tecnico_controller import TecnicoController
from app.controller.cliente_controller import ClienteController
from app.frontend.styles import COLORS, FONTS

class DashboardScreen(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color=COLORS['dark'])
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
        
        # Calcular OS do período atual
        periodos = obter_periodos_disponiveis(filtrar_concluidas=True, excluir_apoio=True)
        if periodos:
            data_inicio, data_fim = periodos[0]
            resultado = contar_os_concluidas_por_tecnico(data_inicio, data_fim)
            self.os_periodo = resultado['total_os']
            self.periodo_desc = f"{data_inicio.strftime('%d/%m')} a {data_fim.strftime('%d/%m')}"
        else:
            self.os_periodo = 0
            self.periodo_desc = "Sem dados"
        
        self.total_tecnicos = len(tecnico_controller.listar_tecnicos())
        self.total_clientes = len(cliente_controller.listar_clientes())
        
        # Últimas 5 OS
        self.ultimas_os = sorted(ordens, key=lambda x: x.data_criacao, reverse=True)[:5]
    
    def create_widgets(self):
        # Header
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=30, pady=(30, 20))
        
        title = ctk.CTkLabel(
            header,
            text="Dashboard",
            font=FONTS['title'],
            text_color=COLORS['white']
        )
        title.pack(side="left")
        
        # KPI Cards
        kpi_frame = ctk.CTkFrame(self, fg_color="transparent")
        kpi_frame.pack(fill="x", padx=30, pady=10)
        
        self.create_kpi_card(kpi_frame, "Total OS", self.total_os, "📊", COLORS['primary'])
        self.create_kpi_card(kpi_frame, "Concluídas", self.concluidas, "✅", COLORS['success'])
        self.create_kpi_card(kpi_frame, "Em andamento", self.em_andamento, "🟡", COLORS['warning'])
        self.create_kpi_card(kpi_frame, f"OS no período\n{self.periodo_desc}", self.os_periodo, "📈", COLORS['secondary'])
        
        # Cards de ação
        actions_frame = ctk.CTkFrame(self, fg_color="transparent")
        actions_frame.pack(fill="x", padx=30, pady=20)
        
        self.create_action_card(actions_frame, "Nova OS", "Criar ordem de serviço", "➕", COLORS['primary'])
        self.create_action_card(actions_frame, "Consultar", "Buscar OS por número", "🔍", COLORS['secondary'])
        self.create_action_card(actions_frame, "Relatórios", "Análise de dados", "📈", COLORS['warning'])
        
        # Últimas OS
        self.create_ultimas_os_table()
    
    def create_kpi_card(self, parent, title, value, icon, color):
        card = ctk.CTkFrame(parent, corner_radius=15, fg_color=COLORS['dark_card'])
        card.pack(side="left", padx=10, fill="both", expand=True)
        
        icon_label = ctk.CTkLabel(card, text=icon, font=('Inter', 32), text_color=color)
        icon_label.pack(pady=(15, 5))
        
        value_label = ctk.CTkLabel(card, text=str(value), font=('Inter', 28, 'bold'), text_color=COLORS['white'])
        value_label.pack()
        
        title_label = ctk.CTkLabel(card, text=title, font=FONTS['small'], text_color=COLORS['gray'])
        title_label.pack(pady=(0, 15))
    
    def create_action_card(self, parent, title, description, icon, color):
        card = ctk.CTkFrame(parent, corner_radius=15, fg_color=COLORS['dark_card'])
        card.pack(side="left", padx=10, fill="both", expand=True)
        
        icon_label = ctk.CTkLabel(card, text=icon, font=('Inter', 40), text_color=color)
        icon_label.pack(pady=(20, 10))
        
        title_label = ctk.CTkLabel(card, text=title, font=FONTS['subtitle'], text_color=COLORS['white'])
        title_label.pack()
        
        desc_label = ctk.CTkLabel(card, text=description, font=FONTS['small'], text_color=COLORS['gray'])
        desc_label.pack(pady=(5, 20))
    
    def create_ultimas_os_table(self):
        frame = ctk.CTkFrame(self, fg_color="transparent")
        frame.pack(fill="both", expand=True, padx=30, pady=10)
        
        label = ctk.CTkLabel(frame, text="📋 Últimas Ordens de Serviço", font=FONTS['subtitle'], text_color=COLORS['white'])
        label.pack(anchor="w", pady=(0, 10))
        
        table_frame = ctk.CTkFrame(frame, corner_radius=15, fg_color=COLORS['dark_card'])
        table_frame.pack(fill="both", expand=True)
        
        headers = ["Nº BD", "Data", "Status"]
        for i, header in enumerate(headers):
            lbl = ctk.CTkLabel(table_frame, text=header, font=FONTS['button'], text_color=COLORS['primary'], width=150)
            lbl.grid(row=0, column=i, padx=10, pady=10, sticky="w")
        
        for row, os in enumerate(self.ultimas_os, 1):
            status = "✅ Concluída" if os.concluida else "🟡 Em andamento"
            status_color = COLORS['success'] if os.concluida else COLORS['warning']
            
            values = [os.number_bd, os.data_criacao[:10], status]
            
            for col, value in enumerate(values):
                if col == 2:
                    lbl = ctk.CTkLabel(table_frame, text=value, font=FONTS['body'], text_color=status_color, width=150)
                else:
                    lbl = ctk.CTkLabel(table_frame, text=value, font=FONTS['body'], text_color=COLORS['light'], width=150)
                lbl.grid(row=row, column=col, padx=10, pady=5, sticky="w")