import customtkinter as ctk
from app.view.frontend.styles import COLORS, FONTS

class GraficoBarras:
    def __init__(self, parent, tecnico, metricas):
        self.parent = parent
        self.tecnico = tecnico
        self.metricas = metricas
        self.canvas = None
        self.frame = None
        self.criar_grafico()
    
    def criar_grafico(self):
        # Configurações
        chart_width = 550
        chart_height = 320
        margin_left = 90
        margin_right = 50
        margin_top = 40
        margin_bottom = 50
        chart_area_width = chart_width - margin_left - margin_right
        chart_area_height = chart_height - margin_top - margin_bottom
        
        # Frame para cada técnico
        self.frame = ctk.CTkFrame(self.parent, fg_color=COLORS['bg_hover'], corner_radius=10)
        self.frame.pack(pady=10, padx=10, fill="x")
        
        # Nome do técnico
        nome = self.tecnico['tecnico']
        if len(nome) > 25:
            nome = nome[:22] + "..."
        
        ctk.CTkLabel(self.frame, text=f"📊 {nome}", font=FONTS['subtitle'], 
                     text_color=COLORS['primary']).pack(pady=(10, 5))
        
        # Canvas para o gráfico
        self.canvas = ctk.CTkCanvas(self.frame, width=chart_width, height=chart_height, 
                                     bg=COLORS['bg_hover'], highlightthickness=0)
        self.canvas.pack(pady=5, padx=10)
        
        # Valores do técnico
        valores = {
            'Efetividade': self.tecnico.get('efetividade', 0),
            'TMR': self.tecnico.get('tmr', 0),
            'APU': self.tecnico.get('apu', 0),
            'ADP': self.tecnico.get('adp', 0)
        }
        
        # Encontrar valor máximo para escala
        max_valor = max(valores.values()) or 100
        
        # Desenhar título
        self.canvas.create_text(chart_width // 2, margin_top - 15, text="Métricas de Desempenho", 
                                 fill=COLORS['text_secondary'], font=('Arial', 10))
        
        # Desenhar eixos
        self.canvas.create_line(margin_left - 5, margin_top + chart_area_height, 
                                 margin_left + chart_area_width + 5, margin_top + chart_area_height, 
                                 fill=COLORS['border'], width=1)
        self.canvas.create_line(margin_left - 5, margin_top, margin_left - 5, 
                                 margin_top + chart_area_height, fill=COLORS['border'], width=1)
        
        # Desenhar grades
        num_grades = 5
        for i in range(num_grades + 1):
            y = margin_top + chart_area_height - (i / num_grades) * chart_area_height
            valor = round((i / num_grades) * max_valor, 1)
            
            self.canvas.create_line(margin_left - 8, y, margin_left - 5, y, fill=COLORS['border'], width=1)
            self.canvas.create_text(margin_left - 15, y, text=str(valor), fill=COLORS['text_secondary'], 
                                     font=('Arial', 8), anchor='e')
            self.canvas.create_line(margin_left, y, margin_left + chart_area_width, y, 
                                     fill=COLORS['border'], width=0.5, dash=(2, 2))
        
        # Desenhar barras
        metricas_nomes = ['Efetividade', 'TMR', 'APU', 'ADP']
        metricas_cores = {
            'Efetividade': COLORS['success'],
            'TMR': COLORS['warning'],
            'APU': COLORS['info'],
            'ADP': COLORS['primary']
        }
        
        bar_width = max((chart_area_width - 20) / len(metricas_nomes) - 15, 45)
        
        for i, metrica in enumerate(metricas_nomes):
            valor = valores[metrica]
            altura = min((valor / max_valor) * chart_area_height, chart_area_height)
            
            x = margin_left + i * (bar_width + 15) + 10
            y = margin_top + chart_area_height - altura
            cor = metricas_cores.get(metrica, COLORS['primary'])
            
            self.canvas.create_rectangle(x, y, x + bar_width, margin_top + chart_area_height, fill=cor, outline='', width=0)
            self.canvas.create_rectangle(x, y, x + bar_width, margin_top + chart_area_height, outline=cor, width=1)
            self.canvas.create_text(x + bar_width / 2, y - 8, text=str(valor), fill=cor, font=('Arial', 9, 'bold'))
            self.canvas.create_text(x + bar_width / 2, margin_top + chart_area_height + 15, text=metrica, 
                                     fill=COLORS['text_light'], font=('Arial', 9))
        
        # Informações adicionais
        info_text = f"Total OS: {self.tecnico['total_os']} | Concluídos: {self.tecnico['concluidos']} | TMR: {self.tecnico['tmr']}h"
        ctk.CTkLabel(self.frame, text=info_text, font=FONTS['small'], 
                     text_color=COLORS['text_secondary']).pack(pady=(0, 10))
    
    def get_frame(self):
        return self.frame
    
    def get_canvas(self):
        return self.canvas