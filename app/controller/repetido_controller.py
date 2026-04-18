from app.bd.conexao import Conexao
from app.model.repetido import Repetido
from app.bd.repetido_repository import RepetidoRepository
from datetime import datetime, timedelta

class RepetidoController:
    def __init__(self):
        self.repo = RepetidoRepository()
        self.con = Conexao()
    
    def atualizar_tabela_repetidos(self):
        """
        Varre todas as OS e alimenta a tabela repetidos
        Baseado na regra dos 30 dias
        """
        print("🔄 Iniciando varredura para identificar repetidos...")
        
        # Buscar todas as OS com WAN válida
        conn = self.con.conectar()
        c = conn.cursor()
        
        c.execute("""
            SELECT 
                o.id_os,
                o.numero,
                o.wan_piloto,
                o.data,
                o.inicio_execucao,
                o.status,
                o.carimbo
            FROM ordem_servico o
            WHERE o.wan_piloto IS NOT NULL 
              AND o.wan_piloto != ''
            ORDER BY o.wan_piloto, o.data, o.inicio_execucao
        """)
        
        todas_os = c.fetchall()
        conn.close()
        
        if not todas_os:
            print("⚠️ Nenhuma OS encontrada!")
            return
        
        # Agrupar por WAN
        wans_dict = {}
        for row in todas_os:
            wan = row[2]
            if wan not in wans_dict:
                wans_dict[wan] = []
            
            data_str = row[3]
            hora_str = row[4] if row[4] else "00:00"
            datetime_str = f"{data_str} {hora_str}:00"
            
            wans_dict[wan].append({
                'id_os': row[0],
                'numero': row[1],
                'wan': wan,
                'data': row[3],
                'hora': row[4] if row[4] else "00:00",
                'datetime': datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S"),
                'status': row[5],
                'carimbo': row[6] if row[6] else ''
            })
        
        # Limpar tabela repetidos antes de recriar
        self._limpar_tabela()
        
        # Identificar repetidos
        novos_repetidos = []
        
        for wan, registros in wans_dict.items():
            if len(registros) <= 1:
                continue
            
            # Ordenar por data/hora
            registros.sort(key=lambda x: x['datetime'])
            
            for i in range(len(registros)):
                os_atual = registros[i]
                data_atual = os_atual['datetime']
                
                # Procurar OS anterior (até 30 dias)
                for j in range(i-1, -1, -1):
                    os_anterior = registros[j]
                    data_anterior = os_anterior['datetime']
                    dias_diferenca = (data_atual - data_anterior).days
                    
                    if dias_diferenca <= 30:
                        # mes_referencia é o mês da OS ANTERIOR (referência)
                        mes_referencia = data_anterior.strftime("%Y-%m")
                        
                        repetido = Repetido(
                            id_os=os_atual['id_os'],
                            id_os_referencia=os_anterior['id_os'],
                            procedente=0,  # 0 = pendente de análise
                            mes_referencia=mes_referencia
                        )
                        novos_repetidos.append(repetido)
                        
                        print(f"   🔁 Repetido encontrado: OS {os_atual['numero']} "
                              f"(WAN: {wan}) → referência OS {os_anterior['numero']} "
                              f"(diferença: {dias_diferenca} dias) | Mês Ref: {mes_referencia}")
                        break  # Encontrou a anterior mais próxima
        
        # Inserir no banco
        for repetido in novos_repetidos:
            self.repo.inserir(repetido)
        
        print(f"✅ Varredura concluída! {len(novos_repetidos)} repetidos identificados.")
        return len(novos_repetidos)
    
    def _limpar_tabela(self):
        """Limpa a tabela repetidos"""
        conn = self.con.conectar()
        c = conn.cursor()
        c.execute("DELETE FROM repetidos")
        conn.commit()
        conn.close()
        print("🗑️ Tabela repetidos limpa.")
    
    def get_repetidos_por_mes(self, mes_referencia):
        """Retorna todos os repetidos de um determinado mês"""
        return self.repo.buscar_por_mes_referencia(mes_referencia)
    
    def get_repetidos_com_detalhes(self, mes_referencia):
        """
        Retorna repetidos com detalhes das OS (para exibir na tela)
        """
        conn = self.con.conectar()
        c = conn.cursor()
        
        query = """
            SELECT 
                r.id,
                r.id_os,
                r.id_os_referencia,
                r.procedente,
                r.mes_referencia,
                os1.numero as numero_repetido,
                os1.wan_piloto,
                os1.data as data_repetido,
                os1.inicio_execucao as hora_repetido,
                os1.carimbo as carimbo_repetido,
                os1.status as status_repetido,
                t1.nome as tecnico_repetido,
                os2.numero as numero_referencia,
                os2.data as data_referencia,
                os2.inicio_execucao as hora_referencia,
                os2.carimbo as carimbo_referencia,
                t2.nome as tecnico_referencia
            FROM repetidos r
            LEFT JOIN ordem_servico os1 ON os1.id_os = r.id_os
            LEFT JOIN ordem_servico os2 ON os2.id_os = r.id_os_referencia
            LEFT JOIN tecnicos t1 ON t1.id = os1.id_tecnico
            LEFT JOIN tecnicos t2 ON t2.id = os2.id_tecnico
            WHERE r.mes_referencia = ?
            ORDER BY os1.data DESC, os1.inicio_execucao DESC
        """
        
        c.execute(query, (mes_referencia,))
        dados = c.fetchall()
        conn.close()
        
        resultado = []
        for row in dados:
            resultado.append({
                'id': row[0],
                'id_os': row[1],
                'id_os_referencia': row[2],
                'procedente': row[3],
                'mes_referencia': row[4],
                'numero_repetido': row[5],
                'wan_piloto': row[6],
                'data_repetido': row[7],
                'hora_repetido': row[8],
                'carimbo_repetido': row[9],
                'status_repetido': row[10],
                'tecnico_repetido': row[11] if row[11] else '-',
                'numero_referencia': row[12],
                'data_referencia': row[13],
                'hora_referencia': row[14],
                'carimbo_referencia': row[15],
                'tecnico_referencia': row[16] if row[16] else '-'
            })
        
        return resultado
    
    def atualizar_procedente(self, id_repetido, procedente):
        """
        Atualiza o status de procedência de um repetido
        procedente: 0 = pendente, 1 = procede, 2 = não procede
        """
        conn = self.con.conectar()
        c = conn.cursor()
        
        c.execute("""
            UPDATE repetidos 
            SET procedente = ? 
            WHERE id = ?
        """, (procedente, id_repetido))
        
        conn.commit()
        conn.close()
        
        status_texto = {0: "pendente", 1: "procede", 2: "não procede"}
        print(f"✅ Repetido {id_repetido} atualizado para: {status_texto.get(procedente, 'desconhecido')}")
    
    # ================= MÉTODOS PARA O POPUP =================
    
    def salvar_repetido(self, id_os, id_os_referencia, procedente, mes_referencia):
        """Salva um repetido na tabela com o mês de referência correto"""
        print(f"DEBUG - Salvando repetido: id_os={id_os}, id_os_referencia={id_os_referencia}, "
              f"procedente={procedente}, mes_referencia={mes_referencia}")
        
        if id_os is None or id_os_referencia is None:
            print("ERRO: id_os ou id_os_referencia é None!")
            return None
        
        repetido = Repetido(
            id_os=id_os,
            id_os_referencia=id_os_referencia,
            procedente=procedente,
            mes_referencia=mes_referencia
        )
        return self.repo.inserir(repetido)
    
    def get_ids_os_analisados(self):
        """Retorna os IDs das OS que já foram analisadas"""
        return self.repo.get_ids_os_analisados()
    
    # ================= MÉTODOS AUXILIARES =================
    
    def _get_tecnico_id_por_nome(self, nome):
        """Retorna o ID do técnico pelo nome"""
        conn = self.con.conectar()
        c = conn.cursor()
        c.execute("SELECT id FROM tecnicos WHERE nome = ?", (nome,))
        row = c.fetchone()
        conn.close()
        return row[0] if row else None
    
    # ================= ESTATÍSTICAS =================
    
    def get_estatisticas_repetidos(self, mes_referencia, id_tecnico=None):
        """
        Retorna estatísticas de repetidos por mês
        """
        repetidos = self.get_repetidos_com_detalhes(mes_referencia)
        
        # Filtrar por técnico se necessário
        if id_tecnico:
            repetidos = [r for r in repetidos if r.get('tecnico_repetido') and 
                        self._get_tecnico_id_por_nome(r['tecnico_repetido']) == id_tecnico]
        
        total_repetidos = len(repetidos)
        
        # Contar por status
        pendentes = len([r for r in repetidos if r.get('procedente') == 0])
        procedem = len([r for r in repetidos if r.get('procedente') == 1])
        nao_procedem = len([r for r in repetidos if r.get('procedente') == 2])
        
        # Contar por WAN
        wans_count = {}
        for r in repetidos:
            wan = r.get('wan_piloto', 'Desconhecido')
            wans_count[wan] = wans_count.get(wan, 0) + 1
        
        # Top 5 WANs mais repetidas
        top_wans = sorted(wans_count.items(), key=lambda x: x[1], reverse=True)[:5]
        
        return {
            'total': total_repetidos,
            'pendentes': pendentes,
            'procedem': procedem,
            'nao_procedem': nao_procedem,
            'top_wans': [{'wan': wan, 'total': total} for wan, total in top_wans]
        }
    
    def get_estatisticas_completas_periodo(self, data_inicio, data_fim, id_tecnico=None):
        """
        Retorna estatísticas completas do período usando a tabela repetidos
        """
        conn = self.con.conectar()
        c = conn.cursor()
        
        # 1. Contar total de OS no período (da tabela ordem_servico)
        query_total_os = """
            SELECT COUNT(*) as total
            FROM ordem_servico o
            WHERE o.data BETWEEN ? AND ?
        """
        params = [data_inicio, data_fim]
        
        if id_tecnico:
            query_total_os += " AND o.id_tecnico = ?"
            params.append(id_tecnico)
        
        c.execute(query_total_os, params)
        total_os = c.fetchone()[0] or 0
        
        # 2. Buscar repetidos do período (da tabela repetidos)
        mes_referencia = datetime.strptime(data_inicio, "%Y-%m-%d").strftime("%Y-%m")
        
        query_repetidos = """
            SELECT 
                r.id,
                r.id_os,
                r.id_os_referencia,
                r.procedente,
                r.mes_referencia,
                os1.data as data_repetido,
                os1.id_tecnico as id_tecnico_repetido
            FROM repetidos r
            LEFT JOIN ordem_servico os1 ON os1.id_os = r.id_os
            WHERE r.mes_referencia = ?
        """
        params_repetidos = [mes_referencia]
        
        c.execute(query_repetidos, params_repetidos)
        repetidos_raw = c.fetchall()
        conn.close()
        
        # Filtrar repetidos por técnico se necessário
        repetidos_filtrados = []
        for row in repetidos_raw:
            if id_tecnico is None or row[6] == id_tecnico:
                repetidos_filtrados.append({
                    'id': row[0],
                    'id_os': row[1],
                    'id_os_referencia': row[2],
                    'procedente': row[3],
                    'mes_referencia': row[4],
                    'data_repetido': row[5],
                    'id_tecnico_repetido': row[6]
                })
        
        total_repetidos = len(repetidos_filtrados)
        
        # Contar por status
        procedentes = len([r for r in repetidos_filtrados if r['procedente'] == 1])
        nao_procedentes = len([r for r in repetidos_filtrados if r['procedente'] == 2])
        pendentes = len([r for r in repetidos_filtrados if r['procedente'] == 0])
        
        # Calcular percentuais
        ofensor = round((total_repetidos / total_os * 100), 1) if total_os > 0 else 0
        percentual_procedente = round((procedentes / total_repetidos * 100), 1) if total_repetidos > 0 else 0
        
        # Buscar nome do técnico
        nome_tecnico = "Todos"
        if id_tecnico:
            conn = self.con.conectar()
            c = conn.cursor()
            c.execute("SELECT nome FROM tecnicos WHERE id = ?", (id_tecnico,))
            row = c.fetchone()
            if row:
                nome_tecnico = row[0]
            conn.close()
        
        return {
            'total_os': total_os,
            'total_repetidos': total_repetidos,
            'procedentes': procedentes,
            'nao_procedentes': nao_procedentes,
            'pendentes': pendentes,
            'ofensor': ofensor,
            'percentual_procedente': percentual_procedente,
            'periodo': {
                'inicio': data_inicio,
                'fim': data_fim
            },
            'tecnico': nome_tecnico,
            'id_tecnico': id_tecnico
        }
    
    def get_os_concluidas_periodo(self, data_inicio, data_fim, id_tecnico=None):
        """
        Retorna o total de OS concluídas no período
        """
        conn = self.con.conectar()
        c = conn.cursor()
        
        query = """
            SELECT COUNT(*) as total
            FROM ordem_servico o
            WHERE o.data BETWEEN ? AND ?
            AND o.status = 1
        """
        params = [data_inicio, data_fim]
        
        if id_tecnico:
            query += " AND o.id_tecnico = ?"
            params.append(id_tecnico)
        
        c.execute(query, params)
        total = c.fetchone()[0] or 0
        conn.close()
        
        return total
    
    def get_os_por_tecnico_periodo(self, data_inicio, data_fim):
        """
        Retorna estatísticas agrupadas por técnico no período
        """
        conn = self.con.conectar()
        c = conn.cursor()
        
        mes_referencia = datetime.strptime(data_inicio, "%Y-%m-%d").strftime("%Y-%m")
        
        # Buscar todos os técnicos
        c.execute("SELECT id, nome FROM tecnicos ORDER BY nome")
        tecnicos = c.fetchall()
        
        resultado = []
        
        for id_tec, nome_tec in tecnicos:
            # Total de OS do técnico no período
            c.execute("""
                SELECT COUNT(*) FROM ordem_servico 
                WHERE data BETWEEN ? AND ? AND id_tecnico = ?
            """, (data_inicio, data_fim, id_tec))
            total_os = c.fetchone()[0] or 0
            
            if total_os == 0:
                continue
            
            # Repetidos do técnico
            c.execute("""
                SELECT COUNT(*) FROM repetidos r
                LEFT JOIN ordem_servico os ON os.id_os = r.id_os
                WHERE r.mes_referencia = ? AND os.id_tecnico = ?
            """, (mes_referencia, id_tec))
            total_repetidos = c.fetchone()[0] or 0
            
            # Procedentes
            c.execute("""
                SELECT COUNT(*) FROM repetidos r
                LEFT JOIN ordem_servico os ON os.id_os = r.id_os
                WHERE r.mes_referencia = ? AND os.id_tecnico = ? AND r.procedente = 1
            """, (mes_referencia, id_tec))
            procedentes = c.fetchone()[0] or 0
            
            # Não procedentes
            c.execute("""
                SELECT COUNT(*) FROM repetidos r
                LEFT JOIN ordem_servico os ON os.id_os = r.id_os
                WHERE r.mes_referencia = ? AND os.id_tecnico = ? AND r.procedente = 2
            """, (mes_referencia, id_tec))
            nao_procedentes = c.fetchone()[0] or 0
            
            # Pendentes
            pendentes = total_repetidos - procedentes - nao_procedentes
            
            ofensor = round((total_repetidos / total_os * 100), 1) if total_os > 0 else 0
            
            resultado.append({
                'id_tecnico': id_tec,
                'tecnico': nome_tec,
                'total_os': total_os,
                'total_repetidos': total_repetidos,
                'procedentes': procedentes,
                'nao_procedentes': nao_procedentes,
                'pendentes': pendentes,
                'ofensor': ofensor
            })
        
        conn.close()
        
        # Ordenar por total de repetidos (maiores primeiro)
        resultado.sort(key=lambda x: x['total_repetidos'], reverse=True)
        
        return resultado