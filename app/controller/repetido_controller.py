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
                        # É uma repetição!
                        mes_referencia = data_atual.strftime("%Y-%m")
                        
                        repetido = Repetido(
                            id_os=os_atual['id_os'],
                            id_os_referencia=os_anterior['id_os'],
                            procedente=0,  # 0 = pendente de análise
                            mes_referencia=mes_referencia
                        )
                        novos_repetidos.append(repetido)
                        
                        print(f"   🔁 Repetido encontrado: OS {os_atual['numero']} "
                              f"(WAN: {wan}) → referência OS {os_anterior['numero']} "
                              f"(diferença: {dias_diferenca} dias)")
                        break  # Encontrou a anterior mais próxima
        
        # Inserir no banco
        for repetido in novos_repetidos:
            self.repo.inserir(repetido)
        
        print(f"✅ Varredura concluída! {len(novos_repetidos)} repetidos identificados.")
        return len(novos_repetidos)
    
    def _limpar_tabela(self):
        """Limpa a tabela repetidos (opcional: pode ser truncate)"""
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