from app.bd.conexao import Conexao
from app.bd.database import Database
from datetime import datetime

class OrdemServicoController:
    def __init__(self):
        self.con = Conexao()
        self.db = Database()
    
    def _get_tipo_nome(self, tipo):
        tipos = {1: "Apoio", 2: "Reparo", 3: "Ativação"}
        return tipos.get(tipo, "Reparo")
    
    def _get_status_nome(self, status):
        return "Concluído" if status == 1 else "Suspenso"
    
    def listar(self, limite=20):
        conn = self.con.conectar()
        c = conn.cursor()
        c.execute("""
            SELECT os.id_os, os.numero, os.id_tecnico, t.nome as tecnico_nome, 
                   os.wan_piloto, os.carimbo, os.tipo, os.status, os.data_criacao,
                   os.data, os.inicio_execucao, os.fim_execucao
            FROM ordem_servico os
            LEFT JOIN tecnicos t ON os.id_tecnico = t.id
            ORDER BY os.data_criacao DESC
            LIMIT ?
        """, (limite,))
        dados = c.fetchall()
        conn.close()
        
        resultado = []
        for row in dados:
            resultado.append({
                'id_os': row[0],
                'numero': row[1] if row[1] else "-",
                'id_tecnico': row[2],
                'tecnico_nome': row[3] if row[3] else "-",
                'wan_piloto': row[4] if row[4] else "-",
                'carimbo': row[5] if row[5] else "-",
                'tipo': row[6] if row[6] else 2,
                'tipo_nome': self._get_tipo_nome(row[6]) if row[6] else "Reparo",
                'status': row[7] if row[7] else 1,
                'status_nome': self._get_status_nome(row[7]) if row[7] else "Concluído",
                'data_criacao': row[8] if row[8] else "-",
                'data': row[9] if row[9] else "-",
                'inicio_execucao': row[10] if row[10] else "-",
                'fim_execucao': row[11] if row[11] else "-"
            })
        return resultado
    
    def inserir(self, numero, id_tecnico, wan_piloto=None, carimbo=None, 
                tipo=2, status=1, data=None, inicio_execucao=None, fim_execucao=None):
        
        data_criacao = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        conn = self.con.conectar()
        c = conn.cursor()
        c.execute("""
            INSERT INTO ordem_servico 
            (numero, id_tecnico, wan_piloto, carimbo, tipo, status, data_criacao, data, inicio_execucao, fim_execucao)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (numero, id_tecnico, wan_piloto, carimbo, tipo, status, data_criacao, data, inicio_execucao, fim_execucao))
        
        id_os = c.lastrowid
        conn.commit()
        conn.close()
        return id_os
    
    def buscar_por_numero(self, numero):
        conn = self.con.conectar()
        c = conn.cursor()
        c.execute("""
            SELECT os.id_os, os.numero, os.id_tecnico, t.nome as tecnico_nome, 
                   os.wan_piloto, os.carimbo, os.tipo, os.status, os.data_criacao,
                   os.data, os.inicio_execucao, os.fim_execucao
            FROM ordem_servico os
            LEFT JOIN tecnicos t ON os.id_tecnico = t.id
            WHERE os.numero = ?
        """, (numero,))
        row = c.fetchone()
        conn.close()
        
        if row:
            return {
                'id_os': row[0],
                'numero': row[1],
                'id_tecnico': row[2],
                'tecnico_nome': row[3] if row[3] else "-",
                'wan_piloto': row[4] if row[4] else "-",
                'carimbo': row[5] if row[5] else "-",
                'tipo': row[6],
                'tipo_nome': self._get_tipo_nome(row[6]),
                'status': row[7],
                'status_nome': self._get_status_nome(row[7]),
                'data_criacao': row[8] if row[8] else "-",
                'data': row[9] if row[9] else "-",
                'inicio_execucao': row[10] if row[10] else "-",
                'fim_execucao': row[11] if row[11] else "-"
            }
        return None
    
    def get_estatisticas(self):
        conn = self.con.conectar()
        c = conn.cursor()
        
        c.execute("SELECT COUNT(*) FROM ordem_servico")
        total = c.fetchone()[0]
        
        c.execute("SELECT COUNT(*) FROM ordem_servico WHERE status = 1")
        concluidos = c.fetchone()[0]
        
        c.execute("SELECT COUNT(*) FROM ordem_servico WHERE status = 0")
        suspensos = c.fetchone()[0]
        
        c.execute("SELECT COUNT(*) FROM ordem_servico WHERE tipo = 1")
        apoio = c.fetchone()[0]
        
        c.execute("SELECT COUNT(*) FROM ordem_servico WHERE tipo = 2")
        reparo = c.fetchone()[0]
        
        c.execute("SELECT COUNT(*) FROM ordem_servico WHERE tipo = 3")
        ativacao = c.fetchone()[0]
        
        c.execute("SELECT COUNT(*) FROM tecnicos")
        tecnicos = c.fetchone()[0]
        
        conn.close()
        
        return {
            'total': total,
            'concluidos': concluidos,
            'suspensos': suspensos,
            'apoio': apoio,
            'reparo': reparo,
            'ativacao': ativacao,
            'tecnicos': tecnicos
        }
        
        
    def get_estatisticas_periodo(self, data_inicio, data_fim):
        """Retorna estatísticas do período"""
        conn = self.con.conectar()
        c = conn.cursor()
        
        c.execute("""
            SELECT 
                COUNT(*) as total,
                SUM(CASE WHEN status = 1 THEN 1 ELSE 0 END) as concluidos,
                SUM(CASE WHEN status = 0 THEN 1 ELSE 0 END) as suspensos,
                SUM(CASE WHEN tipo = 1 THEN 1 ELSE 0 END) as apoio,
                SUM(CASE WHEN tipo = 2 THEN 1 ELSE 0 END) as reparo,
                SUM(CASE WHEN tipo = 3 THEN 1 ELSE 0 END) as ativacao,
                SUM(CASE WHEN tipo = 1 AND status = 1 THEN 1 ELSE 0 END) as apoio_concluidos,
                SUM(CASE WHEN tipo = 1 AND status = 0 THEN 1 ELSE 0 END) as apoio_suspensos,
                SUM(CASE WHEN tipo = 2 AND status = 1 THEN 1 ELSE 0 END) as reparo_concluidos,
                SUM(CASE WHEN tipo = 2 AND status = 0 THEN 1 ELSE 0 END) as reparo_suspensos,
                SUM(CASE WHEN tipo = 3 AND status = 1 THEN 1 ELSE 0 END) as ativacao_concluidos,
                SUM(CASE WHEN tipo = 3 AND status = 0 THEN 1 ELSE 0 END) as ativacao_suspensos
            FROM ordem_servico
            WHERE data BETWEEN ? AND ?
        """, (data_inicio, data_fim))
        
        row = c.fetchone()
        conn.close()
        
        return {
            'total': row[0] or 0,
            'concluidos': row[1] or 0,
            'suspensos': row[2] or 0,
            'apoio': row[3] or 0,
            'reparo': row[4] or 0,
            'ativacao': row[5] or 0,
            'apoio_concluidos': row[6] or 0,
            'apoio_suspensos': row[7] or 0,
            'reparo_concluidos': row[8] or 0,
            'reparo_suspensos': row[9] or 0,
            'ativacao_concluidos': row[10] or 0,
            'ativacao_suspensos': row[11] or 0
        }
        
        
        
    def get_estatisticas_periodo(self, data_inicio, data_fim):
        """Retorna estatísticas do período"""
        conn = self.con.conectar()
        c = conn.cursor()
        
        c.execute("""
            SELECT 
                COUNT(*) as total,
                SUM(CASE WHEN status = 1 THEN 1 ELSE 0 END) as concluidos,
                SUM(CASE WHEN status = 0 THEN 1 ELSE 0 END) as suspensos,
                SUM(CASE WHEN tipo = 1 THEN 1 ELSE 0 END) as apoio,
                SUM(CASE WHEN tipo = 2 THEN 1 ELSE 0 END) as reparo,
                SUM(CASE WHEN tipo = 3 THEN 1 ELSE 0 END) as ativacao,
                SUM(CASE WHEN tipo = 1 AND status = 1 THEN 1 ELSE 0 END) as apoio_concluidos,
                SUM(CASE WHEN tipo = 1 AND status = 0 THEN 1 ELSE 0 END) as apoio_suspensos,
                SUM(CASE WHEN tipo = 2 AND status = 1 THEN 1 ELSE 0 END) as reparo_concluidos,
                SUM(CASE WHEN tipo = 2 AND status = 0 THEN 1 ELSE 0 END) as reparo_suspensos,
                SUM(CASE WHEN tipo = 3 AND status = 1 THEN 1 ELSE 0 END) as ativacao_concluidos,
                SUM(CASE WHEN tipo = 3 AND status = 0 THEN 1 ELSE 0 END) as ativacao_suspensos
            FROM ordem_servico
            WHERE data BETWEEN ? AND ?
        """, (data_inicio, data_fim))
        
        row = c.fetchone()
        conn.close()
        
        return {
            'total': row[0] or 0,
            'concluidos': row[1] or 0,
            'suspensos': row[2] or 0,
            'apoio': row[3] or 0,
            'reparo': row[4] or 0,
            'ativacao': row[5] or 0,
            'apoio_concluidos': row[6] or 0,
            'apoio_suspensos': row[7] or 0,
            'reparo_concluidos': row[8] or 0,
            'reparo_suspensos': row[9] or 0,
            'ativacao_concluidos': row[10] or 0,
            'ativacao_suspensos': row[11] or 0
        }
        
        
    def get_estatisticas_periodo(self, data_inicio, data_fim):
        """Retorna estatísticas do período"""
        conn = self.con.conectar()
        c = conn.cursor()
        
        try:
            c.execute("""
                SELECT 
                    COUNT(*) as total,
                    SUM(CASE WHEN status = 1 THEN 1 ELSE 0 END) as concluidos,
                    SUM(CASE WHEN status = 0 THEN 1 ELSE 0 END) as suspensos,
                    SUM(CASE WHEN tipo = 1 THEN 1 ELSE 0 END) as apoio,
                    SUM(CASE WHEN tipo = 2 THEN 1 ELSE 0 END) as reparo,
                    SUM(CASE WHEN tipo = 3 THEN 1 ELSE 0 END) as ativacao,
                    SUM(CASE WHEN tipo = 1 AND status = 1 THEN 1 ELSE 0 END) as apoio_concluidos,
                    SUM(CASE WHEN tipo = 1 AND status = 0 THEN 1 ELSE 0 END) as apoio_suspensos,
                    SUM(CASE WHEN tipo = 2 AND status = 1 THEN 1 ELSE 0 END) as reparo_concluidos,
                    SUM(CASE WHEN tipo = 2 AND status = 0 THEN 1 ELSE 0 END) as reparo_suspensos,
                    SUM(CASE WHEN tipo = 3 AND status = 1 THEN 1 ELSE 0 END) as ativacao_concluidos,
                    SUM(CASE WHEN tipo = 3 AND status = 0 THEN 1 ELSE 0 END) as ativacao_suspensos
                FROM ordem_servico
                WHERE data BETWEEN ? AND ?
            """, (data_inicio, data_fim))
            
            row = c.fetchone()
            
            # Se não houver dados, retorna zeros
            if not row or row[0] is None:
                conn.close()
                return {
                    'total': 0, 'concluidos': 0, 'suspensos': 0,
                    'apoio': 0, 'reparo': 0, 'ativacao': 0,
                    'apoio_concluidos': 0, 'apoio_suspensos': 0,
                    'reparo_concluidos': 0, 'reparo_suspensos': 0,
                    'ativacao_concluidos': 0, 'ativacao_suspensos': 0
                }
            
            conn.close()
            
            return {
                'total': row[0] or 0,
                'concluidos': row[1] or 0,
                'suspensos': row[2] or 0,
                'apoio': row[3] or 0,
                'reparo': row[4] or 0,
                'ativacao': row[5] or 0,
                'apoio_concluidos': row[6] or 0,
                'apoio_suspensos': row[7] or 0,
                'reparo_concluidos': row[8] or 0,
                'reparo_suspensos': row[9] or 0,
                'ativacao_concluidos': row[10] or 0,
                'ativacao_suspensos': row[11] or 0
            }
            
        except Exception as e:
            print(f"Erro em get_estatisticas_periodo: {e}")
            conn.close()
            return {
                'total': 0, 'concluidos': 0, 'suspensos': 0,
                'apoio': 0, 'reparo': 0, 'ativacao': 0,
                'apoio_concluidos': 0, 'apoio_suspensos': 0,
                'reparo_concluidos': 0, 'reparo_suspensos': 0,
                'ativacao_concluidos': 0, 'ativacao_suspensos': 0
            }
            
            
    def listar_por_periodo(self, data_inicio, data_fim, id_tecnico=None, tipo=None):
        """Lista todas as OS por período"""
        conn = self.con.conectar()
        c = conn.cursor()
        
        query = """
            SELECT 
                o.numero,
                t.nome as tecnico_nome,
                o.wan_piloto,
                o.data,
                o.inicio_execucao,
                o.fim_execucao,
                o.tipo,
                o.status,
                o.carimbo
            FROM ordem_servico o
            LEFT JOIN tecnicos t ON t.id = o.id_tecnico
            WHERE o.data BETWEEN ? AND ?
        """
        params = [data_inicio, data_fim]
        
        if id_tecnico:
            query += " AND o.id_tecnico = ?"
            params.append(id_tecnico)
        
        if tipo:
            tipo_map = {"Apoio": 1, "Reparo": 2, "Ativação": 3}
            tipo_id = tipo_map.get(tipo)
            if tipo_id:
                query += " AND o.tipo = ?"
                params.append(tipo_id)
        
        query += " ORDER BY o.data DESC"
        
        c.execute(query, params)
        dados = c.fetchall()
        conn.close()
        
        resultado = []
        for row in dados:
            tipo_nome = {1: "Apoio", 2: "Reparo", 3: "Ativação"}.get(row[6], "-")
            status_nome = "Concluído" if row[7] == 1 else "Suspenso"
            
            resultado.append({
                'numero': row[0],
                'tecnico_nome': row[1] if row[1] else '-',
                'wan_piloto': row[2] if row[2] else '-',
                'data': row[3] if row[3] else '-',
                'inicio_execucao': row[4] if row[4] else '-',
                'fim_execucao': row[5] if row[5] else '-',
                'tipo': row[6],
                'tipo_nome': tipo_nome,
                'status': row[7],
                'status_nome': status_nome,
                'carimbo': row[8] if row[8] else '-'
            })
        
        return resultado