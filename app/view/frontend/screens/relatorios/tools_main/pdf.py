from tkinter import filedialog, messagebox
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.units import cm

class PDFExportador:
    """Gerencia a exportação de dados para PDF"""
    
    @staticmethod
    def exportar_relatorio(dados, nome_arquivo_sugerido="relatorio_vivo_os"):
        """Gera um PDF com o relatório completo"""
        arquivo = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf")],
            title="Salvar PDF",
            initialfile=f"{nome_arquivo_sugerido}.pdf"
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