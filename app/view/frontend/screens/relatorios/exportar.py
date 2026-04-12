import csv
from datetime import datetime
from tkinter import filedialog, messagebox
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.units import cm


class ExportadorRelatorio:
    def __init__(self, parent, relatorio_controller, os_controller):
        self.parent = parent
        self.relatorio_controller = relatorio_controller
        self.os_controller = os_controller
        self.meses = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", 
                     "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]
        self.periodos_producao = []
    
    def carregar_periodos_producao(self):
        """Carrega os períodos de produção"""
        from datetime import datetime, timedelta
        hoje = datetime.now()
        for i in range(12):
            data_fim = datetime(hoje.year, hoje.month, 1) - timedelta(days=i * 30)
            
            if data_fim.day >= 21:
                data_inicio = datetime(data_fim.year, data_fim.month, 21)
            else:
                if data_fim.month > 1:
                    data_inicio = datetime(data_fim.year, data_fim.month - 1, 21)
                else:
                    data_inicio = datetime(data_fim.year - 1, 12, 21)
            
            data_fim = data_inicio + timedelta(days=30)
            data_fim = datetime(data_fim.year, data_fim.month, 20)
            
            nome = f"{data_inicio.strftime('%d/%m/%Y')} a {data_fim.strftime('%d/%m/%Y')}"
            self.periodos_producao.append({
                'nome': nome,
                'inicio': data_inicio.strftime("%Y-%m-%d"),
                'fim': data_fim.strftime("%Y-%m-%d")
            })
    
    def obter_dados_periodo(self, periodo_tipo, mes, ano, periodo_nome, tecnico_nome):
        """Obtém os dados conforme o período selecionado"""
        from datetime import datetime, timedelta
        
        if periodo_tipo == 'mes':
            mes_numero = self.meses.index(mes) + 1
            data_inicio = datetime(int(ano), mes_numero, 1).strftime("%Y-%m-%d")
            if mes_numero == 12:
                data_fim = datetime(int(ano) + 1, 1, 1) - timedelta(days=1)
            else:
                data_fim = datetime(int(ano), mes_numero + 1, 1) - timedelta(days=1)
            data_fim = data_fim.strftime("%Y-%m-%d")
            periodo_nome_exibicao = f"{mes}/{ano}"
        else:
            for p in self.periodos_producao:
                if p['nome'] == periodo_nome:
                    data_inicio = p['inicio']
                    data_fim = p['fim']
                    periodo_nome_exibicao = periodo_nome
                    break
        
        # Obter técnico
        id_tecnico = None
        if tecnico_nome != "Todos":
            tecnicos = self.relatorio_controller.get_tecnicos()
            for t in tecnicos:
                if t['nome'] == tecnico_nome:
                    id_tecnico = t['id']
                    break
        
        # Buscar OS do período
        ordens = self.os_controller.listar_por_periodo(data_inicio, data_fim, id_tecnico)
        
        return {
            'data_inicio': data_inicio,
            'data_fim': data_fim,
            'periodo_nome': periodo_nome_exibicao,
            'tecnico_nome': tecnico_nome,
            'id_tecnico': id_tecnico,
            'ordens': ordens
        }
    
    def gerar_pdf(self, dados):
        """Gera um PDF com o relatório completo"""
        arquivo = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf")],
            title="Salvar PDF"
        )
        
        if not arquivo:
            return False
        
        try:
            doc = SimpleDocTemplate(arquivo, pagesize=A4, topMargin=1*cm, bottomMargin=1*cm)
            story = []
            
            styles = getSampleStyleSheet()
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=16,
                textColor=colors.HexColor('#00ff88'),
                alignment=0,
                spaceAfter=20
            )
            
            # Título
            story.append(Paragraph("RELATÓRIO VIVO OS", title_style))
            story.append(Spacer(1, 0.5*cm))
            
            # Informações do período
            info_text = f"""
            <b>Período:</b> {dados['periodo_nome']}<br/>
            <b>Data:</b> {dados['data_inicio']} a {dados['data_fim']}<br/>
            <b>Técnico:</b> {dados['tecnico_nome']}<br/>
            <b>Data de geração:</b> {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}
            """
            story.append(Paragraph(info_text, styles['Normal']))
            story.append(Spacer(1, 0.5*cm))
            
            # Tabela de OS
            story.append(Paragraph("📋 LISTA DE ORDENS DE SERVIÇO", styles['Heading2']))
            story.append(Spacer(1, 0.3*cm))
            
            # Dados da tabela
            table_data = [["Nº OS", "Técnico", "WAN/Piloto", "Data", "Início", "Fim", "Tipo", "Status"]]
            
            for os in dados['ordens']:
                table_data.append([
                    os.get('numero', '-'),
                    os.get('tecnico_nome', '-'),
                    os.get('wan_piloto', '-')[:20],
                    os.get('data', '-'),
                    os.get('inicio_execucao', '-'),
                    os.get('fim_execucao', '-'),
                    os.get('tipo_nome', '-'),
                    os.get('status_nome', '-')
                ])
            
            table = Table(table_data, repeatRows=1)
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1a1a2e')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor('#00ff88')),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
                ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#0f0f0f')),
                ('TEXTCOLOR', (0, 1), (-1, -1), colors.HexColor('#cccccc')),
                ('FONTSIZE', (0, 1), (-1, -1), 8),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#2a2a2a')),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ]))
            
            story.append(table)
            doc.build(story)
            
            messagebox.showinfo("Sucesso", f"PDF gerado com sucesso!\n{arquivo}")
            return True
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao gerar PDF: {str(e)}")
            return False
    
    def exportar_csv_os(self, dados):
        """Exporta lista de OS para CSV"""
        arquivo = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv")],
            title="Salvar CSV"
        )
        
        if not arquivo:
            return False
        
        try:
            with open(arquivo, 'w', newline='', encoding='utf-8-sig') as f:
                writer = csv.writer(f, delimiter=';')
                
                writer.writerow([
                    "Nº OS", "Técnico", "WAN/Piloto", "Data", 
                    "Início", "Fim", "Tipo", "Status", "Carimbo"
                ])
                
                for os in dados['ordens']:
                    writer.writerow([
                        os.get('numero', '-'),
                        os.get('tecnico_nome', '-'),
                        os.get('wan_piloto', '-'),
                        os.get('data', '-'),
                        os.get('inicio_execucao', '-'),
                        os.get('fim_execucao', '-'),
                        os.get('tipo_nome', '-'),
                        os.get('status_nome', '-'),
                        os.get('carimbo', '-').replace('\n', ' ').replace(';', ',')
                    ])
            
            messagebox.showinfo("Sucesso", f"CSV gerado com sucesso!\n{arquivo}")
            return True
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao gerar CSV: {str(e)}")
            return False
    
    def exportar_csv_medias(self, dados):
        """Exporta médias (APU, Ofensor, etc.) para CSV"""
        arquivo = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv")],
            title="Salvar CSV de Médias"
        )
        
        if not arquivo:
            return False
        
        try:
            data_inicio = dados['data_inicio']
            data_fim = dados['data_fim']
            id_tecnico = dados['id_tecnico']
            
            # Buscar dados de APU individual
            apu_individual = self.relatorio_controller.get_apu_individual(data_inicio, data_fim, id_tecnico)
            resumo = self.relatorio_controller.get_resumo_periodo(data_inicio, data_fim, id_tecnico)
            metricas = self.relatorio_controller.get_metricas_radar(data_inicio, data_fim, id_tecnico)
            
            with open(arquivo, 'w', newline='', encoding='utf-8-sig') as f:
                writer = csv.writer(f, delimiter=';')
                
                # Resumo Geral
                writer.writerow(["RESUMO GERAL"])
                writer.writerow(["Total OS", resumo['total_os']])
                writer.writerow(["Concluídos", resumo['concluidos']])
                writer.writerow(["Suspensos", resumo['suspensos']])
                writer.writerow(["Repetições", resumo['repeticoes']])
                writer.writerow(["Ofensor %", f"{resumo['ofensor']}%"])
                writer.writerow([])
                
                # APU por Técnico
                writer.writerow(["APU POR TÉCNICO"])
                writer.writerow(["Técnico", "Dias Trabalhados", "Total Concluídos", "APU"])
                for item in apu_individual:
                    writer.writerow([
                        item['tecnico'],
                        item['dias_trabalhados'],
                        item['total_concluidos'],
                        item['apu']
                    ])
                writer.writerow([])
                
                # Métricas por Técnico
                writer.writerow(["MÉTRICAS POR TÉCNICO"])
                writer.writerow(["Técnico", "Total OS", "Efetividade %", "TMR (h)", "ADP %", "APU", "Ofensor"])
                for item in metricas:
                    writer.writerow([
                        item['tecnico'],
                        item['total_os'],
                        item['efetividade'],
                        item['tmr'],
                        item['adp'],
                        item['apu'],
                        item['ofensor']
                    ])
            
            messagebox.showinfo("Sucesso", f"CSV de médias gerado com sucesso!\n{arquivo}")
            return True
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao gerar CSV de médias: {str(e)}")
            return False