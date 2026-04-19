import csv
from tkinter import filedialog, messagebox

class CSVExportador:
    """Gerencia a exportação de dados para CSV"""
    
    @staticmethod
    def exportar_os(dados, nome_arquivo_sugerido="relatorio_os"):
        """Exporta lista de OS para CSV"""
        arquivo = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv")],
            title="Salvar CSV",
            initialfile=f"{nome_arquivo_sugerido}.csv"
        )
        
        if not arquivo:
            return False
        
        try:
            with open(arquivo, 'w', newline='', encoding='utf-8-sig') as f:
                writer = csv.writer(f, delimiter=';')
                
                # Cabeçalho
                writer.writerow([
                    "Nº OS", "Técnico", "WAN/Piloto", "Data", 
                    "Início", "Fim", "Tipo", "Status", "Carimbo"
                ])
                
                # Dados
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
    
    @staticmethod
    def exportar_medias(dados_apu, dados_metricas, resumo, nome_arquivo_sugerido="relatorio_medias"):
        """Exporta médias (APU, Ofensor, etc.) para CSV"""
        arquivo = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv")],
            title="Salvar CSV de Médias",
            initialfile=f"{nome_arquivo_sugerido}.csv"
        )
        
        if not arquivo:
            return False
        
        try:
            with open(arquivo, 'w', newline='', encoding='utf-8-sig') as f:
                writer = csv.writer(f, delimiter=';')
                
                # Resumo Geral
                writer.writerow(["RESUMO GERAL"])
                writer.writerow(["Total OS", resumo.get('total_os', 0)])
                writer.writerow(["Concluídos", resumo.get('concluidos', 0)])
                writer.writerow(["Suspensos", resumo.get('suspensos', 0)])
                writer.writerow(["Repetições", resumo.get('repeticoes', 0)])
                writer.writerow(["Ofensor %", f"{resumo.get('ofensor', 0)}%"])
                writer.writerow([])
                
                # APU por Técnico
                writer.writerow(["APU POR TÉCNICO"])
                writer.writerow(["Técnico", "Dias Trabalhados", "Total Concluídos", "APU"])
                for item in dados_apu:
                    writer.writerow([
                        item.get('tecnico', '-'),
                        item.get('dias_trabalhados', 0),
                        item.get('total_concluidos', 0),
                        item.get('apu', 0)
                    ])
                writer.writerow([])
                
                # Métricas por Técnico
                writer.writerow(["MÉTRICAS POR TÉCNICO"])
                writer.writerow(["Técnico", "Total OS", "Efetividade %", "TMR (h)", "ADP %", "APU", "Ofensor"])
                for item in dados_metricas:
                    writer.writerow([
                        item.get('tecnico', '-'),
                        item.get('total_os', 0),
                        item.get('efetividade', 0),
                        item.get('tmr', 0),
                        item.get('adp', 0),
                        item.get('apu', 0),
                        item.get('ofensor', 0)
                    ])
            
            messagebox.showinfo("Sucesso", f"CSV de médias gerado com sucesso!\n{arquivo}")
            return True
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao gerar CSV de médias: {str(e)}")
            return False