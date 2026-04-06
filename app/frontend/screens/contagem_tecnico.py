# app/frontend/screens/contagem_tecnico.py

import customtkinter as ctk
from app.frontend.styles import COLORS, FONTS
from app.frontend.components import TabelaInterativa
from app.tools.periodos import obter_periodos_disponiveis, formatar_periodo
from app.tools.ordem_servivo.count_os_tecnico import contar_os_concluidas_por_tecnico


class ContagemTecnicoScreen(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")
        self.pack(fill="both", expand=True)
        
        self.periodos = []
        self.periodos_labels = []
        
        self.create_widgets()
        self.carregar_periodos()
    
    def create_widgets(self):
        # Frame de seleção
        select_frame = ctk.CTkFrame(self, fg_color=COLORS['bg_card'], corner_radius=12, border_width=1, border_color=COLORS['border'])
        select_frame.pack(fill="x", pady=10, padx=10)
        
        label = ctk.CTkLabel(
            select_frame,
            text="Selecione o período:",
            font=FONTS['body_bold'],
            text_color=COLORS['text_primary']
        )
        label.pack(side="left", padx=15, pady=12)
        
        self.periodo_var = ctk.StringVar()
        self.periodo_combo = ctk.CTkComboBox(
            select_frame,
            values=[],
            variable=self.periodo_var,
            width=250,
            state="readonly"
        )
        self.periodo_combo.pack(side="left", padx=10, pady=12)
        
        btn = ctk.CTkButton(
            select_frame,
            text="Gerar",
            command=self.gerar_relatorio,
            fg_color=COLORS['primary'],
            hover_color=COLORS['primary_dark'],
            width=100
        )
        btn.pack(side="left", padx=10, pady=12)
        
        # Frame para resultados
        self.result_frame = ctk.CTkFrame(self, fg_color=COLORS['bg_card'], corner_radius=12, border_width=1, border_color=COLORS['border'])
        self.result_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.mensagem = ctk.CTkLabel(
            self.result_frame,
            text="Selecione um período e clique em Gerar",
            font=FONTS['body'],
            text_color=COLORS['text_secondary']
        )
        self.mensagem.pack(expand=True)
    
    def carregar_periodos(self):
        self.periodos = obter_periodos_disponiveis(filtrar_concluidas=True, excluir_apoio=True)
        self.periodos_labels = [formatar_periodo(di, df) for di, df in self.periodos]
        self.periodo_combo.configure(values=self.periodos_labels)
        if self.periodos_labels:
            self.periodo_var.set(self.periodos_labels[0])
    
    def gerar_relatorio(self):
        if not self.periodos or not self.periodos_labels:
            return
        
        try:
            idx = self.periodos_labels.index(self.periodo_var.get())
        except ValueError:
            return
        
        data_inicio, data_fim = self.periodos[idx]
        
        resultado = contar_os_concluidas_por_tecnico(data_inicio, data_fim)
        
        # Limpar resultado anterior
        for widget in self.result_frame.winfo_children():
            widget.destroy()
        
        # Título
        title = ctk.CTkLabel(
            self.result_frame,
            text=f"📊 OS Concluídas por Técnico\n{data_inicio.strftime('%d/%m/%Y')} a {data_fim.strftime('%d/%m/%Y')}",
            font=FONTS['subtitle'],
            text_color=COLORS['primary']
        )
        title.pack(pady=15)
        
        if not resultado['dados']:
            label = ctk.CTkLabel(
                self.result_frame,
                text="Nenhuma OS encontrada no período",
                font=FONTS['body'],
                text_color=COLORS['text_secondary']
            )
            label.pack(expand=True)
            return
        
        # Tabela
        headers = ["Técnico", "Quantidade"]
        larguras = [300, 100]
        
        tabela = TabelaInterativa(self.result_frame, headers, larguras)
        tabela.pack(fill="both", expand=True, padx=10, pady=10)
        
        for item in resultado['dados']:
            tabela.adicionar_linha([item['tecnico_nome'], str(item['quantidade'])])
        
        # Total
        total = ctk.CTkLabel(
            self.result_frame,
            text=f"TOTAL: {resultado['total_os']} OS",
            font=FONTS['body_bold'],
            text_color=COLORS['success']
        )
        total.pack(pady=10)