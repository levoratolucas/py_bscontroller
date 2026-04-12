import customtkinter as ctk
from tkinter import messagebox, simpledialog
from app.view.frontend.styles import COLORS, FONTS
from app.controller.ordem_servico_controller import OrdemServicoController
from app.controller.tecnico_controller import TecnicoController
from app.controller.relatorio_controller import RelatorioController
from datetime import datetime, timedelta
import math


class DashboardScreen(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent, fg_color="transparent")
        self.pack(fill="both", expand=True)
        
        self.app = app
        self.os_controller = OrdemServicoController()
        self.tecnico_controller = TecnicoController()
        self.relatorio_controller = RelatorioController()
        
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
        self.card_os = self._criar_card_os(cards_frame, 0)
        
        # Card 2: Repetidos
        self.card_repetidos = self._criar_card_repetidos(cards_frame, 1)
        
        # Card 3: APU
        self.card_apu = self._criar_card_apu(cards_frame, 2)

        # ================= GRÁFICO DE BARRAS =================
        graficos_frame = ctk.CTkFrame(self.main_frame, fg_color=COLORS['bg_card'], corner_radius=12, border_width=1, border_color=COLORS['border'])
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

        self.graficos_canvases = []

        # ================= BOTÕES DE NAVEGAÇÃO =================
        botoes_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        botoes_frame.pack(fill="x", pady=(0, 20))

        for i in range(3):
            botoes_frame.grid_columnconfigure(i, weight=1)

        self._criar_botao_navegacao(botoes_frame, "📝 Nova OS", "Cadastrar ordem de serviço", self.nova_os, 0)
        self._criar_botao_navegacao(botoes_frame, "🔍 Consultar", "Buscar OS por número", self.consultar, 1)
        self._criar_botao_navegacao(botoes_frame, "📈 Relatórios", "Análise de dados", self.relatorios, 2)

    def _criar_card_os(self, parent, col):
        """Card 1: Ordem de Serviço"""
        card = ctk.CTkFrame(parent, fg_color=COLORS['bg_card'], corner_radius=12, border_width=1, border_color=COLORS['border'])
        card.grid(row=0, column=col, sticky="nsew", padx=5, pady=5)

        ctk.CTkLabel(card, text="📋 ORDEM DE SERVIÇO", font=FONTS['subtitle'], text_color=COLORS['primary']).pack(anchor="w", padx=15, pady=(10, 5))

        self.os_total_label = ctk.CTkLabel(card, text="TOTAL: 0", font=('Arial', 28, 'bold'), text_color=COLORS['primary'])
        self.os_total_label.pack(anchor="w", padx=15, pady=(0, 10))

        # Ativação
        ativ_frame = ctk.CTkFrame(card, fg_color="transparent")
        ativ_frame.pack(fill="x", padx=15, pady=2)
        ctk.CTkLabel(ativ_frame, text="🚀 ATIVAÇÃO:", font=FONTS['normal'], width=90).pack(side="left")
        self.ativacao_total_label = ctk.CTkLabel(ativ_frame, text="0", font=FONTS['normal'], width=30)
        self.ativacao_total_label.pack(side="left")
        self.ativacao_ok_label = ctk.CTkLabel(ativ_frame, text=" ✅ OK: 0", font=FONTS['small'], text_color=COLORS['success'])
        self.ativacao_ok_label.pack(side="left", padx=(5, 0))
        self.ativacao_pend_label = ctk.CTkLabel(ativ_frame, text=" ⏸️ Pend: 0", font=FONTS['small'], text_color=COLORS['warning'])
        self.ativacao_pend_label.pack(side="left", padx=(5, 0))

        # Reparo
        reparo_frame = ctk.CTkFrame(card, fg_color="transparent")
        reparo_frame.pack(fill="x", padx=15, pady=2)
        ctk.CTkLabel(reparo_frame, text="🔧 REPARO:", font=FONTS['normal'], width=90).pack(side="left")
        self.reparo_total_label = ctk.CTkLabel(reparo_frame, text="0", font=FONTS['normal'], width=30)
        self.reparo_total_label.pack(side="left")
        self.reparo_ok_label = ctk.CTkLabel(reparo_frame, text=" ✅ OK: 0", font=FONTS['small'], text_color=COLORS['success'])
        self.reparo_ok_label.pack(side="left", padx=(5, 0))
        self.reparo_pend_label = ctk.CTkLabel(reparo_frame, text=" ⏸️ Pend: 0", font=FONTS['small'], text_color=COLORS['warning'])
        self.reparo_pend_label.pack(side="left", padx=(5, 0))

        # Apoio
        apoio_frame = ctk.CTkFrame(card, fg_color="transparent")
        apoio_frame.pack(fill="x", padx=15, pady=2)
        ctk.CTkLabel(apoio_frame, text="🛟 APOIO:", font=FONTS['normal'], width=90).pack(side="left")
        self.apoio_total_label = ctk.CTkLabel(apoio_frame, text="0", font=FONTS['normal'], width=30)
        self.apoio_total_label.pack(side="left")
        self.apoio_ok_label = ctk.CTkLabel(apoio_frame, text=" ✅ OK: 0", font=FONTS['small'], text_color=COLORS['success'])
        self.apoio_ok_label.pack(side="left", padx=(5, 0))
        self.apoio_pend_label = ctk.CTkLabel(apoio_frame, text=" ⏸️ Pend: 0", font=FONTS['small'], text_color=COLORS['warning'])
        self.apoio_pend_label.pack(side="left", padx=(5, 0))

        return card

    def _criar_card_repetidos(self, parent, col):
        """Card 2: Repetidos"""
        card = ctk.CTkFrame(parent, fg_color=COLORS['bg_card'], corner_radius=12, border_width=1, border_color=COLORS['border'])
        card.grid(row=0, column=col, sticky="nsew", padx=5, pady=5)

        ctk.CTkLabel(card, text="🔄 REPETIDOS", font=FONTS['subtitle'], text_color=COLORS['warning']).pack(anchor="w", padx=15, pady=(10, 5))

        self.repetidos_total_label = ctk.CTkLabel(card, text="TOTAL: 0", font=('Arial', 24, 'bold'), text_color=COLORS['warning'])
        self.repetidos_total_label.pack(anchor="w", padx=15, pady=(0, 5))
        
        self.repetidos_percent_label = ctk.CTkLabel(card, text="", font=FONTS['normal'], text_color=COLORS['text_secondary'])
        self.repetidos_percent_label.pack(anchor="w", padx=15, pady=(0, 10))

        self.repetidos_ranking_frame = ctk.CTkFrame(card, fg_color="transparent")
        self.repetidos_ranking_frame.pack(fill="x", padx=15, pady=(0, 15))

        self.repetidos_labels = []
        for i in range(3):
            label = ctk.CTkLabel(self.repetidos_ranking_frame, text="", font=FONTS['normal'], anchor="w")
            label.pack(fill="x", pady=5)
            self.repetidos_labels.append(label)

        return card

    def _criar_card_apu(self, parent, col):
        """Card 3: APU"""
        card = ctk.CTkFrame(parent, fg_color=COLORS['bg_card'], corner_radius=12, border_width=1, border_color=COLORS['border'])
        card.grid(row=0, column=col, sticky="nsew", padx=5, pady=5)

        ctk.CTkLabel(card, text="⚡ APU", font=FONTS['subtitle'], text_color=COLORS['success']).pack(anchor="w", padx=15, pady=(10, 5))

        self.apu_media_label = ctk.CTkLabel(card, text="MÉDIA GERAL: 0,0", font=('Arial', 22, 'bold'), text_color=COLORS['success'])
        self.apu_media_label.pack(anchor="w", padx=15, pady=(0, 10))

        self.apu_ranking_frame = ctk.CTkFrame(card, fg_color="transparent")
        self.apu_ranking_frame.pack(fill="x", padx=15, pady=(0, 15))

        self.apu_labels = []
        for i in range(3):
            label = ctk.CTkLabel(self.apu_ranking_frame, text="", font=FONTS['normal'], anchor="w")
            label.pack(fill="x", pady=5)
            self.apu_labels.append(label)

        return card

    def _criar_botao_navegacao(self, parent, titulo, desc, comando, col):
        """Cria um botão de navegação"""
        card = ctk.CTkFrame(parent, fg_color=COLORS['bg_card'], corner_radius=12, border_width=1, border_color=COLORS['border'])
        card.grid(row=0, column=col, sticky="nsew", padx=5, pady=5)
        
        ctk.CTkLabel(card, text=titulo, font=FONTS['subtitle'], text_color=COLORS['primary']).pack(anchor="w", padx=15, pady=(10, 0))
        ctk.CTkLabel(card, text=desc, font=FONTS['small'], text_color=COLORS['text_secondary']).pack(anchor="w", padx=15, pady=(0, 5))
        ctk.CTkButton(card, text="Acessar →", fg_color="transparent", text_color=COLORS['primary'], command=comando).pack(fill="x", padx=15, pady=(0, 10))

    def carregar_dados(self):
        """Carrega todos os dados do dashboard"""
        hoje = datetime.now()
        primeiro_dia = datetime(hoje.year, hoje.month, 1)
        
        if hoje.month == 12:
            ultimo_dia = datetime(hoje.year + 1, 1, 1) - timedelta(days=1)
        else:
            ultimo_dia = datetime(hoje.year, hoje.month + 1, 1) - timedelta(days=1)
        
        data_inicio = primeiro_dia.strftime("%Y-%m-%d")
        data_fim = ultimo_dia.strftime("%Y-%m-%d")
        
        # 1. Carregar estatísticas do período
        stats = self.os_controller.get_estatisticas_periodo(data_inicio, data_fim)
        total = stats.get('total', 0)
        
        self.os_total_label.configure(text=f"TOTAL: {total}")
        self.ativacao_total_label.configure(text=str(stats.get('ativacao', 0)))
        self.ativacao_ok_label.configure(text=f" ✅ OK: {stats.get('ativacao_concluidos', 0)}")
        self.ativacao_pend_label.configure(text=f" ⏸️ Pend: {stats.get('ativacao_suspensos', 0)}")
        self.reparo_total_label.configure(text=str(stats.get('reparo', 0)))
        self.reparo_ok_label.configure(text=f" ✅ OK: {stats.get('reparo_concluidos', 0)}")
        self.reparo_pend_label.configure(text=f" ⏸️ Pend: {stats.get('reparo_suspensos', 0)}")
        self.apoio_total_label.configure(text=str(stats.get('apoio', 0)))
        self.apoio_ok_label.configure(text=f" ✅ OK: {stats.get('apoio_concluidos', 0)}")
        self.apoio_pend_label.configure(text=f" ⏸️ Pend: {stats.get('apoio_suspensos', 0)}")
        
        # 2. Carregar métricas dos técnicos
        metricas = self.relatorio_controller.get_metricas_radar(data_inicio, data_fim)
        
        # Calcular percentual de repetições
        for m in metricas:
            total_tecnico = m.get('total_os', 0)
            ofensor = m.get('ofensor', 0)
            percentual_ofensor = round((ofensor / total_tecnico * 100), 1) if total_tecnico > 0 else 0
            m['percentual_ofensor'] = percentual_ofensor
        
        # Totais de repetições
        total_repeticoes = sum(m.get('ofensor', 0) for m in metricas)
        percent_repeticoes = round((total_repeticoes / total * 100), 1) if total > 0 else 0
        
        self.repetidos_total_label.configure(text=f"TOTAL: {total_repeticoes}  ({percent_repeticoes}% do total)")
        
        # Ranking ofensores
        ofensores = sorted(metricas, key=lambda x: x.get('percentual_ofensor', 0), reverse=True)
        medalhas = ["🥇", "🥈", "🥉"]
        for i, label in enumerate(self.repetidos_labels):
            if i < len(ofensores):
                of = ofensores[i]
                percentual = of.get('percentual_ofensor', 0)
                if percentual > 0:
                    label.configure(text=f"{medalhas[i]} {of['tecnico']}: {percentual}% ({of.get('ofensor', 0)} repetições)")
                else:
                    label.configure(text=f"{medalhas[i]} {of['tecnico']}: 0%")
            else:
                label.configure(text="")
        
        # APU
        apu_validos = [m.get('apu', 0) for m in metricas if m.get('apu', 0) > 0]
        media_apu = round(sum(apu_validos) / len(apu_validos), 2) if apu_validos else 0
        self.apu_media_label.configure(text=f"MÉDIA GERAL: {media_apu}")
        
        apu_lista = sorted(metricas, key=lambda x: x.get('apu', 999))
        for i, label in enumerate(self.apu_labels):
            if i < len(apu_lista):
                ap = apu_lista[i]
                label.configure(text=f"{medalhas[i]} {ap['tecnico']}: {ap.get('apu', 0)}")
            else:
                label.configure(text="")
        
        # 3. Desenhar gráficos de barras
        self.desenhar_barras_tecnicos(metricas)

    def desenhar_barras_tecnicos(self, metricas):
        """Desenha gráfico de barras horizontais para comparar técnicos"""
        # Limpar gráficos existentes
        for grafico_info in self.graficos_canvases:
            grafico_info['canvas'].destroy()
        self.graficos_canvases.clear()
        
        if not metricas:
            return
        
        # Filtrar técnicos com OS
        tecnicos_validos = [m for m in metricas if m.get('total_os', 0) > 0]
        
        if not tecnicos_validos:
            return
        
        # Métricas a serem exibidas
        metricas_nomes = ['Efetividade', 'TMR', 'APU', 'ADP']
        metricas_cores = {
            'Efetividade': COLORS['success'],
            'TMR': COLORS['warning'],
            'APU': COLORS['info'],
            'ADP': COLORS['primary']
        }
        
        # Ordenar técnicos por nome
        tecnicos_validos.sort(key=lambda x: x['tecnico'])
        
        # Configurar grid - 2 por linha
        cols = 2
        chart_width = 550
        chart_height = 320
        
        for idx, tecnico in enumerate(tecnicos_validos):
            row = idx // cols
            col = idx % cols
            
            # Frame para cada técnico
            chart_card = ctk.CTkFrame(self.graficos_grid_frame, fg_color=COLORS['bg_hover'], corner_radius=10)
            chart_card.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
            
            # Nome do técnico
            nome_tecnico = tecnico['tecnico']
            if len(nome_tecnico) > 25:
                nome_tecnico = nome_tecnico[:22] + "..."
            
            ctk.CTkLabel(
                chart_card, 
                text=f"📊 {nome_tecnico}", 
                font=FONTS['subtitle'],
                text_color=COLORS['primary']
            ).pack(pady=(10, 5))
            
            # Canvas para o gráfico
            canvas = ctk.CTkCanvas(
                chart_card, 
                width=chart_width, 
                height=chart_height, 
                bg=COLORS['bg_hover'],
                highlightthickness=0
            )
            canvas.pack(pady=5, padx=10)
            
            # Configurações do gráfico
            margin_left = 90
            margin_right = 50
            margin_top = 40
            margin_bottom = 50
            chart_area_width = chart_width - margin_left - margin_right
            chart_area_height = chart_height - margin_top - margin_bottom
            
            # Valores do técnico
            valores = {
                'Efetividade': tecnico.get('efetividade', 0),
                'TMR': tecnico.get('tmr', 0),
                'APU': tecnico.get('apu', 0),
                'ADP': tecnico.get('adp', 0)
            }
            
            # Encontrar valor máximo para escala
            max_valor = max(valores.values()) or 100
            
            # Desenhar título do gráfico
            canvas.create_text(
                chart_width // 2, 
                margin_top - 15, 
                text="Métricas de Desempenho", 
                fill=COLORS['text_secondary'], 
                font=('Arial', 10)
            )
            
            # Desenhar eixo X (linha horizontal)
            canvas.create_line(
                margin_left - 5, 
                margin_top + chart_area_height, 
                margin_left + chart_area_width + 5, 
                margin_top + chart_area_height, 
                fill=COLORS['border'], 
                width=1
            )
            
            # Desenhar eixo Y (linha vertical)
            canvas.create_line(
                margin_left - 5, 
                margin_top, 
                margin_left - 5, 
                margin_top + chart_area_height, 
                fill=COLORS['border'], 
                width=1
            )
            
            # Desenhar grades e labels do eixo X (valores)
            num_grades = 5
            for i in range(num_grades + 1):
                x = margin_left - 5
                y = margin_top + chart_area_height - (i / num_grades) * chart_area_height
                valor = round((i / num_grades) * max_valor, 1)
                
                canvas.create_line(x - 3, y, x, y, fill=COLORS['border'], width=1)
                canvas.create_text(x - 10, y, text=str(valor), fill=COLORS['text_secondary'], font=('Arial', 8), anchor='e')
                
                # Linha de grade horizontal
                canvas.create_line(margin_left, y, margin_left + chart_area_width, y, fill=COLORS['border'], width=0.5, dash=(2, 2))
            
            # Espaçamento entre barras
            bar_width = (chart_area_width - 20) / len(metricas_nomes) - 15
            bar_width = max(bar_width, 45)
            
            # Desenhar barras
            for i, metrica in enumerate(metricas_nomes):
                valor = valores[metrica]
                altura = (valor / max_valor) * chart_area_height
                altura = min(altura, chart_area_height)
                
                x = margin_left + i * (bar_width + 15) + 10
                y = margin_top + chart_area_height - altura
                
                cor = metricas_cores.get(metrica, COLORS['primary'])
                
                # Barra com gradiente visual
                canvas.create_rectangle(x, y, x + bar_width, margin_top + chart_area_height, fill=cor, outline='', width=0)
                canvas.create_rectangle(x, y, x + bar_width, margin_top + chart_area_height, outline=cor, width=1)
                
                # Valor no topo da barra
                canvas.create_text(x + bar_width / 2, y - 8, text=str(valor), fill=cor, font=('Arial', 9, 'bold'))
                
                # Label da métrica
                canvas.create_text(x + bar_width / 2, margin_top + chart_area_height + 15, text=metrica, fill=COLORS['text_light'], font=('Arial', 9))
            
            # Informações adicionais
            info_text = f"Total OS: {tecnico['total_os']} | Concluídos: {tecnico['concluidos']} | TMR: {tecnico['tmr']}h"
            ctk.CTkLabel(
                chart_card, 
                text=info_text, 
                font=FONTS['small'], 
                text_color=COLORS['text_secondary']
            ).pack(pady=(0, 10))
            
            # Armazenar referência
            self.graficos_canvases.append({
                'canvas': canvas,
                'tecnico': tecnico['tecnico'],
                'frame': chart_card
            })
        
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