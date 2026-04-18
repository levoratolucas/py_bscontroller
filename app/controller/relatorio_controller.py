from app.bd.conexao import Conexao
from datetime import datetime, timedelta

class RelatorioController:
    def __init__(self):
        self.con = Conexao()
    
    # ==================== MÉTODOS AUXILIARES ====================
    
    def _get_periodo_mes(self, mes, ano):
        """Retorna data_inicio e data_fim do mês"""
        primeiro_dia = datetime(int(ano), int(mes), 1)
        if mes == 12:
            ultimo_dia = datetime(int(ano) + 1, 1, 1) - timedelta(days=1)
        else:
            ultimo_dia = datetime(int(ano), int(mes) + 1, 1) - timedelta(days=1)
        return primeiro_dia.strftime("%Y-%m-%d"), ultimo_dia.strftime("%Y-%m-%d")
    
    def _get_tipo_nome(self, tipo):
        tipos = {1: "Apoio", 2: "Reparo", 3: "Ativação"}
        return tipos.get(tipo, "Desconhecido")
    
    def get_tecnicos(self):
        """Retorna lista de técnicos para dropdown"""
        conn = self.con.conectar()
        c = conn.cursor()
        c.execute("SELECT id, nome FROM tecnicos ORDER BY nome")
        dados = c.fetchall()
        conn.close()
        return [{'id': row[0], 'nome': row[1]} for row in dados]
    
    # ==================== 1. RESUMO DO PERÍODO ====================
    
    def get_resumo_periodo(self, data_inicio, data_fim, id_tecnico=None):
        """Retorna resumo das OS no período"""
        conn = self.con.conectar()
        c = conn.cursor()
        
        # Converter id_tecnico
        if id_tecnico and id_tecnico != "todos" and id_tecnico != "" and id_tecnico != "Todos":
            if isinstance(id_tecnico, str):
                try:
                    id_tecnico = int(id_tecnico)
                except:
                    id_tecnico = None
        
        query = """
            SELECT 
                COUNT(*) as total_os,
                SUM(CASE WHEN status = 1 THEN 1 ELSE 0 END) as concluidos,
                SUM(CASE WHEN status = 0 THEN 1 ELSE 0 END) as suspensos
            FROM ordem_servico o
            WHERE o.data BETWEEN ? AND ?
        """
        params = [data_inicio, data_fim]
        
        if id_tecnico and id_tecnico != "todos":
            query += " AND o.id_tecnico = ?"
            params.append(id_tecnico)
        
        c.execute(query, params)
        row = c.fetchone()
        total_os = row[0] if row[0] else 0
        concluidos = row[1] if row[1] else 0
        suspensos = row[2] if row[2] else 0
        
        # Calcular repetições com filtro (busca anterior fora do período)
        repeticoes = self._calcular_repeticoes_periodo(data_inicio, data_fim, id_tecnico)
        ofensor = round((repeticoes / total_os * 100), 1) if total_os > 0 else 0
        
        conn.close()
        
        return {
            'total_os': total_os,
            'concluidos': concluidos,
            'suspensos': suspensos,
            'repeticoes': repeticoes,
            'ofensor': ofensor
        }
    
    def _calcular_repeticoes_periodo(self, data_inicio, data_fim, id_tecnico=None):
        """Calcula o número de repetições no período (considera OS anterior fora do período)"""
        conn = self.con.conectar()
        c = conn.cursor()
        
        # Converter id_tecnico
        if id_tecnico and id_tecnico != "todos" and id_tecnico != "" and id_tecnico != "Todos":
            if isinstance(id_tecnico, str):
                try:
                    id_tecnico = int(id_tecnico)
                except:
                    id_tecnico = None
        
        # Buscar TODAS as OS com WAN (sem filtro de data para a anterior)
        query = """
            SELECT 
                o.id_os,
                o.wan_piloto, 
                o.data, 
                o.inicio_execucao,
                o.id_tecnico
            FROM ordem_servico o
            WHERE o.wan_piloto IS NOT NULL 
              AND o.wan_piloto != ''
        """
        params = []
        
        if id_tecnico and id_tecnico != "todos":
            query += " AND o.id_tecnico = ?"
            params.append(id_tecnico)
        
        query += " ORDER BY o.wan_piloto, o.data, o.inicio_execucao"
        
        c.execute(query, params)
        dados = c.fetchall()
        conn.close()
        
        if not dados:
            return 0
        
        # Agrupar por WAN
        wans_dict = {}
        for row in dados:
            wan = row[1]
            if wan not in wans_dict:
                wans_dict[wan] = []
            
            data_str = row[2]
            hora_str = row[3] if row[3] else "00:00"
            datetime_str = f"{data_str} {hora_str}:00"
            
            wans_dict[wan].append({
                'id_os': row[0],
                'datetime': datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S"),
                'data': data_str,
                'id_tecnico': row[4]
            })
        
        # Converter período para datetime
        inicio_periodo = datetime.strptime(data_inicio, "%Y-%m-%d")
        fim_periodo = datetime.strptime(data_fim, "%Y-%m-%d")
        
        # Contar repetições
        repeticoes = 0
        
        for wan, registros in wans_dict.items():
            if len(registros) <= 1:
                continue
            
            # Ordenar por data/hora
            registros.sort(key=lambda x: x['datetime'])
            
            for i in range(len(registros)):
                data_atual = registros[i]['datetime']
                
                # Verificar se a OS atual está dentro do período
                if not (inicio_periodo <= data_atual <= fim_periodo):
                    continue
                
                # Procurar OS anterior (pode estar fora do período)
                for j in range(i-1, -1, -1):
                    data_anterior = registros[j]['datetime']
                    dias_diferenca = (data_atual - data_anterior).days
                    
                    if dias_diferenca <= 30:
                        repeticoes += 1
                        break  # Conta apenas uma repetição por OS
        
        return repeticoes
    
    # ==================== 2. MÉTRICAS PARA GRÁFICOS ====================
    
    def get_metricas_radar(self, data_inicio, data_fim, id_tecnico=None):
        """Retorna métricas para os gráficos"""
        conn = self.con.conectar()
        c = conn.cursor()
        
        # Converter id_tecnico
        if id_tecnico and id_tecnico != "todos" and id_tecnico != "" and id_tecnico != "Todos":
            if isinstance(id_tecnico, str):
                try:
                    id_tecnico = int(id_tecnico)
                except:
                    id_tecnico = None
        
        # Buscar todas OS para calcular repetições
        query_os = """
            SELECT 
                o.id_os,
                o.numero,
                o.id_tecnico,
                t.nome as tecnico,
                o.wan_piloto,
                o.data,
                o.inicio_execucao,
                o.status,
                o.tipo,
                o.fim_execucao
            FROM ordem_servico o
            LEFT JOIN tecnicos t ON t.id = o.id_tecnico
            WHERE o.wan_piloto IS NOT NULL 
              AND o.wan_piloto != ''
        """
        params = []
        
        if id_tecnico and id_tecnico != "todos":
            query_os += " AND o.id_tecnico = ?"
            params.append(id_tecnico)
        
        query_os += " ORDER BY o.wan_piloto, o.data, o.inicio_execucao"
        
        c.execute(query_os, params)
        todas_os = c.fetchall()
        
        # Agrupar por WAN
        wans_dict = {}
        for row in todas_os:
            wan = row[4]
            if wan not in wans_dict:
                wans_dict[wan] = []
            
            data_str = row[5]
            hora_str = row[6] if row[6] else "00:00"
            datetime_str = f"{data_str} {hora_str}:00"
            
            wans_dict[wan].append({
                'id_os': row[0],
                'numero': row[1],
                'id_tecnico': row[2],
                'tecnico': row[3],
                'wan': wan,
                'data': data_str,
                'datetime': datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S")
            })
        
        # Identificar quais OS são repetidas (considerando anterior fora do período)
        inicio_periodo = datetime.strptime(data_inicio, "%Y-%m-%d")
        fim_periodo = datetime.strptime(data_fim, "%Y-%m-%d")
        
        os_repetidas = set()
        for wan, registros in wans_dict.items():
            if len(registros) <= 1:
                continue
            registros.sort(key=lambda x: x['datetime'])
            
            for i in range(len(registros)):
                data_atual = registros[i]['datetime']
                
                # Verificar se está no período
                if not (inicio_periodo <= data_atual <= fim_periodo):
                    continue
                
                for j in range(i-1, -1, -1):
                    data_anterior = registros[j]['datetime']
                    dias_diferenca = (data_atual - data_anterior).days
                    if dias_diferenca <= 30:
                        os_repetidas.add(registros[i]['id_os'])
                        break
        
        # Buscar estatísticas por técnico
        query_stats = """
            SELECT 
                t.id,
                t.nome as tecnico,
                COUNT(o.id_os) as total_os,
                SUM(CASE WHEN o.status = 1 THEN 1 ELSE 0 END) as concluidos,
                ROUND(AVG(CASE 
                    WHEN o.tipo = 2 AND o.status = 1 AND o.inicio_execucao IS NOT NULL AND o.fim_execucao IS NOT NULL
                    AND o.inicio_execucao != '' AND o.fim_execucao != ''
                    THEN (strftime('%s', o.data || ' ' || o.fim_execucao) - 
                          strftime('%s', o.data || ' ' || o.inicio_execucao)) / 3600.0
                    ELSE NULL 
                END), 2) as tmr,
                ROUND(100.0 * SUM(CASE WHEN o.status = 1 THEN 1 ELSE 0 END) / COUNT(*), 1) as efetividade,
                ROUND(100.0 * SUM(CASE WHEN o.tipo = 1 THEN 1 ELSE 0 END) / COUNT(*), 1) as adp,
                ROUND(1.0 * SUM(CASE WHEN o.status = 1 THEN 1 ELSE 0 END) / 
                      NULLIF(COUNT(DISTINCT o.data), 0), 2) as apu
            FROM ordem_servico o
            LEFT JOIN tecnicos t ON t.id = o.id_tecnico
            WHERE o.data BETWEEN ? AND ?
        """
        params_stats = [data_inicio, data_fim]
        
        if id_tecnico and id_tecnico != "todos":
            query_stats += " AND o.id_tecnico = ?"
            params_stats.append(id_tecnico)
        
        query_stats += " GROUP BY t.id, t.nome HAVING COUNT(o.id_os) > 0 ORDER BY t.nome"
        
        c.execute(query_stats, params_stats)
        dados = c.fetchall()
        
        # Contar repetições por técnico
        repeticoes_por_tecnico = {}
        for os in todas_os:
            if os[0] in os_repetidas:
                id_tec = os[2]
                if id_tec:
                    repeticoes_por_tecnico[id_tec] = repeticoes_por_tecnico.get(id_tec, 0) + 1
        
        conn.close()
        
        # Montar resultado
        resultado = []
        for row in dados:
            id_tec = row[0] if row[0] else 0
            resultado.append({
                'id_tecnico': id_tec,
                'tecnico': row[1] if row[1] else 'Sem técnico',
                'total_os': row[2] if row[2] else 0,
                'concluidos': row[3] if row[3] else 0,
                'tmr': row[4] if row[4] else 0,
                'efetividade': row[5] if row[5] else 0,
                'adp': row[6] if row[6] else 0,
                'apu': row[7] if row[7] else 0,
                'ofensor': repeticoes_por_tecnico.get(id_tec, 0)
            })
        
        return resultado
    
    # ==================== 3. OS REPETIDAS (APENAS AS REPETIDAS) ====================
    
    def get_os_repetidas_apenas(self, data_inicio, data_fim, id_tecnico=None):
        """Retorna APENAS as OS repetidas (exclui a primeira/Original)"""
        conn = self.con.conectar()
        c = conn.cursor()
        
        # Converter id_tecnico
        if id_tecnico and id_tecnico != "todos" and id_tecnico != "" and id_tecnico != "Todos":
            if isinstance(id_tecnico, str):
                try:
                    id_tecnico = int(id_tecnico)
                except:
                    id_tecnico = None
        
        # Buscar TODAS as OS com a mesma WAN (sem filtro de data)
        query = """
            SELECT 
                o.id_os,
                o.numero,
                o.wan_piloto,
                t.nome as tecnico,
                o.data,
                o.inicio_execucao,
                o.fim_execucao,
                o.status,
                o.carimbo,
                o.id_tecnico
            FROM ordem_servico o
            LEFT JOIN tecnicos t ON t.id = o.id_tecnico
            WHERE o.wan_piloto IS NOT NULL 
              AND o.wan_piloto != ''
              AND o.wan_piloto IN (
                  SELECT DISTINCT wan_piloto 
                  FROM ordem_servico 
                  WHERE wan_piloto IS NOT NULL 
                    AND wan_piloto != ''
                    AND data BETWEEN ? AND ?
              )
        """
        params = [data_inicio, data_fim]
        
        if id_tecnico and id_tecnico != "todos":
            query += " AND o.id_tecnico = ?"
            params.append(id_tecnico)
        
        c.execute(query, params)
        todas_os_wan = c.fetchall()
        conn.close()
        
        if not todas_os_wan:
            return []
        
        # Agrupar por WAN
        wans_dict = {}
        for row in todas_os_wan:
            wan = row[2]
            if wan not in wans_dict:
                wans_dict[wan] = []
            
            data_str = row[4]
            hora_str = row[5] if row[5] else "00:00"
            datetime_str = f"{data_str} {hora_str}:00"
            
            wans_dict[wan].append({
                'id_os': row[0],
                'numero': row[1],
                'wan_piloto': wan,
                'tecnico': row[3] if row[3] else '-',
                'data': row[4],
                'inicio_execucao': row[5] if row[5] else '-',
                'fim_execucao': row[6] if row[6] else '-',
                'status': row[7],
                'status_nome': 'Concluído' if row[7] == 1 else 'Suspenso',
                'carimbo': row[8] if row[8] else '',
                'id_tecnico': row[9],
                'datetime': datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S")
            })
        
        # Converter período para datetime
        inicio_periodo = datetime.strptime(data_inicio, "%Y-%m-%d")
        fim_periodo = datetime.strptime(data_fim, "%Y-%m-%d")
        
        # Identificar repetições
        resultado = []
        
        for wan, registros in wans_dict.items():
            if len(registros) <= 1:
                continue
            
            # Ordenar por data/hora
            registros.sort(key=lambda x: x['datetime'])
            
            for i in range(len(registros)):
                data_atual = registros[i]['datetime']
                
                # Verificar se a OS atual está dentro do período filtrado
                if not (inicio_periodo <= data_atual <= fim_periodo):
                    continue
                
                # Procurar OS anterior (pode estar fora do período)
                for j in range(i-1, -1, -1):
                    data_anterior = registros[j]['datetime']
                    dias_diferenca = (data_atual - data_anterior).days
                    
                    if dias_diferenca <= 30:
                        resultado.append({
                            'id_os': registros[i]['id_os'],
                            'numero': registros[i]['numero'],
                            'wan_piloto': registros[i]['wan_piloto'],
                            'tecnico': registros[i]['tecnico'],
                            'data': registros[i]['data'],
                            'inicio_execucao': registros[i]['inicio_execucao'],
                            'fim_execucao': registros[i]['fim_execucao'],
                            'status_nome': registros[i]['status_nome'],
                            'carimbo': registros[i]['carimbo'],
                            'observacao': f'Repetida (anterior em {registros[j]["data"]} {registros[j]["inicio_execucao"]})',
                            'dias_desde_anterior': dias_diferenca,
                            'id_tecnico': registros[i]['id_tecnico']
                        })
                        break  # Encontrou a anterior, para de procurar
        
        return resultado
    
    # ==================== 4. OS ANTERIOR (REFERÊNCIA) ====================
    
    def get_os_anterior(self, wan_piloto, data_atual, hora_atual, data_inicio, data_fim, id_tecnico=None):
        """Retorna a OS imediatamente anterior de um WAN (pode estar fora do período)"""
        conn = self.con.conectar()
        c = conn.cursor()
        
        datetime_atual = datetime.strptime(f"{data_atual} {hora_atual}:00", "%Y-%m-%d %H:%M:%S")
        
        query = """
            SELECT 
                o.id_os,
                o.numero,
                o.wan_piloto,
                t.nome as tecnico,
                o.data,
                o.inicio_execucao,
                o.fim_execucao,
                o.status,
                o.carimbo,
                o.data || ' ' || o.inicio_execucao || ':00' as datetime_completo
            FROM ordem_servico o
            LEFT JOIN tecnicos t ON t.id = o.id_tecnico
            WHERE o.wan_piloto = ?
        """
        params = [wan_piloto]
        
        if id_tecnico and id_tecnico != "todos":
            query += " AND o.id_tecnico = ?"
            params.append(id_tecnico)
        
        query += " ORDER BY o.data, o.inicio_execucao"
        
        c.execute(query, params)
        rows = c.fetchall()
        conn.close()
        
        # Procurar a OS anterior mais próxima
        os_anterior = None
        data_mais_proxima = None
        
        for row in rows:
            datetime_registro = datetime.strptime(row[9], "%Y-%m-%d %H:%M:%S")
            if datetime_registro < datetime_atual:
                if data_mais_proxima is None or datetime_registro > data_mais_proxima:
                    data_mais_proxima = datetime_registro
                    os_anterior = {
                        'id_os': row[0],
                        'numero': row[1],
                        'wan_piloto': row[2],
                        'tecnico': row[3] if row[3] else '-',
                        'data': row[4],
                        'inicio_execucao': row[5] if row[5] else '-',
                        'fim_execucao': row[6] if row[6] else '-',
                        'status_nome': 'Concluído' if row[7] == 1 else 'Suspenso',
                        'carimbo': row[8] if row[8] else ''
                    }
        
        return os_anterior
    
    # ==================== 5. ESTATÍSTICAS POR TIPO ====================
    
    def get_estatisticas_por_tipo(self, data_inicio, data_fim):
        """Retorna quantidade de OS por tipo no período"""
        conn = self.con.conectar()
        c = conn.cursor()
        
        c.execute("""
            SELECT 
                o.tipo,
                COUNT(*) as total,
                SUM(CASE WHEN o.status = 1 THEN 1 ELSE 0 END) as concluidos
            FROM ordem_servico o
            WHERE o.data BETWEEN ? AND ?
            GROUP BY o.tipo
        """, (data_inicio, data_fim))
        
        dados = c.fetchall()
        conn.close()
        
        resultado = {
            'apoio': 0, 'reparo': 0, 'ativacao': 0,
            'apoio_concluidos': 0, 'reparo_concluidos': 0, 'ativacao_concluidos': 0
        }
        
        for row in dados:
            if row[0] == 1:
                resultado['apoio'] = row[1]
                resultado['apoio_concluidos'] = row[2]
            elif row[0] == 2:
                resultado['reparo'] = row[1]
                resultado['reparo_concluidos'] = row[2]
            elif row[0] == 3:
                resultado['ativacao'] = row[1]
                resultado['ativacao_concluidos'] = row[2]
        
        return resultado
    
    # ==================== 6. APU INDIVIDUAL ====================
    
    def get_apu_individual(self, data_inicio, data_fim, id_tecnico=None):
        """Retorna a tabela de APU por técnico"""
        conn = self.con.conectar()
        c = conn.cursor()
        
        query = """
            SELECT 
                t.nome as tecnico,
                COUNT(DISTINCT o.data) as dias_trabalhados,
                COUNT(o.id_os) as total_concluidos,
                ROUND(COUNT(o.id_os) * 1.0 / COUNT(DISTINCT o.data), 2) as apu
            FROM ordem_servico o
            LEFT JOIN tecnicos t ON t.id = o.id_tecnico
            WHERE o.data BETWEEN ? AND ?
            AND o.status = 1
        """
        params = [data_inicio, data_fim]
        
        if id_tecnico:
            query += " AND o.id_tecnico = ?"
            params.append(id_tecnico)
        
        query += " GROUP BY t.id, t.nome ORDER BY apu DESC"
        
        c.execute(query, params)
        dados = c.fetchall()
        conn.close()
        
        resultado = []
        for row in dados:
            resultado.append({
                'tecnico': row[0] if row[0] else '-',
                'dias_trabalhados': row[1] if row[1] else 0,
                'total_concluidos': row[2] if row[2] else 0,
                'apu': row[3] if row[3] else 0
            })
        return resultado
    
    # ==================== 7. TOTAL DE OS NO PERÍODO ====================
    
    def get_total_os_periodo(self, data_inicio, data_fim, id_tecnico=None):
        """Retorna o total de OS no período"""
        conn = self.con.conectar()
        c = conn.cursor()
        
        query = "SELECT COUNT(*) FROM ordem_servico WHERE data BETWEEN ? AND ?"
        params = [data_inicio, data_fim]
        
        if id_tecnico:
            query += " AND id_tecnico = ?"
            params.append(id_tecnico)
        
        c.execute(query, params)
        total = c.fetchone()[0]
        conn.close()
        
        return total if total else 0
    
    
    
    # Adicione este método ao RepetidoController

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
    
        
        
        # Adicione este método ao RelatorioController

    def get_wans_repetidos_resumo(self, data_inicio, data_fim, id_tecnico=None):
        """
        Retorna resumo das WANs repetidas no período (calculado dinamicamente)
        """
        conn = self.con.conectar()
        c = conn.cursor()
        
        query = """
            SELECT 
                wan_piloto,
                COUNT(*) as total,
                MIN(data) as primeira_data,
                MAX(data) as ultima_data
            FROM ordem_servico
            WHERE wan_piloto IS NOT NULL 
            AND wan_piloto != ''
            AND data BETWEEN ? AND ?
            GROUP BY wan_piloto
            HAVING COUNT(*) > 1
            ORDER BY total DESC
        """
        params = [data_inicio, data_fim]
        
        if id_tecnico:
            query = """
                SELECT 
                    o.wan_piloto,
                    COUNT(*) as total,
                    MIN(o.data) as primeira_data,
                    MAX(o.data) as ultima_data
                FROM ordem_servico o
                WHERE o.wan_piloto IS NOT NULL 
                AND o.wan_piloto != ''
                AND o.data BETWEEN ? AND ?
                AND o.id_tecnico = ?
                GROUP BY o.wan_piloto
                HAVING COUNT(*) > 1
                ORDER BY total DESC
            """
            params = [data_inicio, data_fim, id_tecnico]
        
        c.execute(query, params)
        dados = c.fetchall()
        conn.close()
        
        resultado = []
        for row in dados:
            resultado.append({
                'wan': row[0],
                'total': row[1],
                'primeira_data': row[2],
                'ultima_data': row[3]
            })
        
        return resultado