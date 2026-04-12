from datetime import datetime, timedelta
from app.controller.relatorio_controller import RelatorioController


class DadosOrdemServico:
    def __init__(self):
        self.relatorio_controller = RelatorioController()
        self.periodos_producao = []
        self.carregar_periodos_producao()
    
    def carregar_periodos_producao(self):
        """Carrega os períodos de produção (21 de um mês a 20 do próximo)"""
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
    
    def get_periodos_producao(self):
        return self.periodos_producao
    
    def obter_periodo(self, mes=None, ano=None, modo="mes", periodo_nome=None):
        """Retorna data_inicio e data_fim conforme o modo"""
        if modo == "producao" and periodo_nome:
            for p in self.periodos_producao:
                if p['nome'] == periodo_nome:
                    return p['inicio'], p['fim']
        
        # Modo mês (padrão)
        if mes is None or ano is None:
            mes = "Abril"
            ano = str(datetime.now().year)
        
        meses = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", 
                 "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]
        mes_numero = meses.index(mes) + 1
        
        primeiro_dia = datetime(int(ano), mes_numero, 1)
        
        if mes_numero == 12:
            ultimo_dia = datetime(int(ano) + 1, 1, 1) - timedelta(days=1)
        else:
            ultimo_dia = datetime(int(ano), mes_numero + 1, 1) - timedelta(days=1)
        
        return primeiro_dia.strftime("%Y-%m-%d"), ultimo_dia.strftime("%Y-%m-%d")
    
    def get_tecnicos(self):
        return self.relatorio_controller.get_tecnicos()
    
    def get_os_por_filtro(self, data_inicio, data_fim, id_tecnico=None, tipo=None, status=None):
        """Retorna OS conforme filtros"""
        conn = self.relatorio_controller.con.conectar()
        c = conn.cursor()
        
        query = """
            SELECT 
                o.numero,
                t.nome as tecnico,
                o.wan_piloto,
                o.data,
                o.inicio_execucao,
                o.fim_execucao,
                CASE o.tipo 
                    WHEN 1 THEN 'Apoio'
                    WHEN 2 THEN 'Reparo'
                    WHEN 3 THEN 'Ativação'
                END as tipo,
                CASE o.status WHEN 1 THEN 'Concluído' ELSE 'Suspenso' END as status
            FROM ordem_servico o
            LEFT JOIN tecnicos t ON t.id = o.id_tecnico
            WHERE o.data BETWEEN ? AND ?
        """
        params = [data_inicio, data_fim]
        
        if id_tecnico:
            query += " AND o.id_tecnico = ?"
            params.append(id_tecnico)
        
        if tipo:
            query += " AND o.tipo = ?"
            params.append(tipo)
        
        if status is not None:
            query += " AND o.status = ?"
            params.append(status)
        
        query += " ORDER BY o.data DESC"
        
        c.execute(query, params)
        dados = c.fetchall()
        conn.close()
        
        resultado = []
        for row in dados:
            resultado.append({
                'numero': row[0] if row[0] else '-',
                'tecnico': row[1] if row[1] else '-',
                'wan_piloto': row[2] if row[2] else '-',
                'data': row[3] if row[3] else '-',
                'inicio': row[4] if row[4] else '-',
                'fim': row[5] if row[5] else '-',
                'tipo': row[6] if row[6] else '-',
                'status': row[7] if row[7] else '-'
            })
        return resultado
    
    def get_quantidades_por_tipo(self, data_inicio, data_fim, id_tecnico=None):
        """Retorna quantidade de OS por tipo para os botões"""
        conn = self.relatorio_controller.con.conectar()
        c = conn.cursor()
        
        query = """
            SELECT 
                COUNT(*) as total,
                SUM(CASE WHEN tipo = 3 THEN 1 ELSE 0 END) as ativacao,
                SUM(CASE WHEN tipo = 2 THEN 1 ELSE 0 END) as reparo
            FROM ordem_servico
            WHERE data BETWEEN ? AND ?
        """
        params = [data_inicio, data_fim]
        
        if id_tecnico:
            query += " AND id_tecnico = ?"
            params.append(id_tecnico)
        
        c.execute(query, params)
        row = c.fetchone()
        conn.close()
        
        return {
            'total': row[0] if row[0] else 0,
            'ativacao': row[1] if row[1] else 0,
            'reparo': row[2] if row[2] else 0
        }
    
    def get_os_por_tecnico(self, data_inicio, data_fim, tipo=None, status=None, id_tecnico=None):
        """Retorna OS agrupadas por técnico para exibição no card direito"""
        conn = self.relatorio_controller.con.conectar()
        c = conn.cursor()
        
        query = """
            SELECT 
                t.nome as tecnico,
                COUNT(o.id_os) as total_os,
                SUM(CASE WHEN o.status = 1 THEN 1 ELSE 0 END) as concluidos,
                SUM(CASE WHEN o.status = 0 THEN 1 ELSE 0 END) as suspensos
            FROM ordem_servico o
            LEFT JOIN tecnicos t ON t.id = o.id_tecnico
            WHERE o.data BETWEEN ? AND ?
        """
        params = [data_inicio, data_fim]
        
        if id_tecnico:
            query += " AND o.id_tecnico = ?"
            params.append(id_tecnico)
        
        if tipo:
            query += " AND o.tipo = ?"
            params.append(tipo)
        
        if status is not None:
            query += " AND o.status = ?"
            params.append(status)
        
        query += " GROUP BY t.id, t.nome ORDER BY total_os DESC"
        
        c.execute(query, params)
        dados = c.fetchall()
        conn.close()
        
        resultado = []
        for row in dados:
            resultado.append({
                'tecnico': row[0] if row[0] else '-',
                'total_os': row[1] if row[1] else 0,
                'concluidos': row[2] if row[2] else 0,
                'suspensos': row[3] if row[3] else 0
            })
        return resultado
    
    def calcular_apu_geral(self, data_inicio, data_fim, id_tecnico=None):
        """Calcula a média geral de APU do período"""
        conn = self.relatorio_controller.con.conectar()
        c = conn.cursor()
        
        query = """
            SELECT 
                ROUND(AVG(apu_por_tecnico), 2) as apu_geral
            FROM (
                SELECT 
                    t.id,
                    COUNT(DISTINCT o.data) as dias_trabalhados,
                    COUNT(o.id_os) as total_concluidos,
                    ROUND(COUNT(o.id_os) * 1.0 / COUNT(DISTINCT o.data), 2) as apu_por_tecnico
                FROM ordem_servico o
                LEFT JOIN tecnicos t ON t.id = o.id_tecnico
                WHERE o.data BETWEEN ? AND ?
                  AND o.status = 1
        """
        params = [data_inicio, data_fim]
        
        if id_tecnico:
            query += " AND o.id_tecnico = ?"
            params.append(id_tecnico)
        
        query += " GROUP BY t.id, t.nome) sub"
        
        c.execute(query, params)
        row = c.fetchone()
        conn.close()
        
        return row[0] if row and row[0] else 0
    
    def calcular_apu_individual(self, data_inicio, data_fim, id_tecnico=None):
        """Retorna a tabela de APU por técnico"""
        conn = self.relatorio_controller.con.conectar()
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