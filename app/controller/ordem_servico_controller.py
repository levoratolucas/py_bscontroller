from app.bd.ordem_servico_repository import OrdemServicoRepository
from app.model.ordem_servico import OrdemServico
from datetime import datetime

class OrdemServicoController:
    def __init__(self):
        self.repo = OrdemServicoRepository()

    def inserir_ordem(self, id_tecnico, id_produto, causa_raiz, materiais_utilizados, 
                  acao, contato_responsavel, observacoes, number_bd=None, tipo=None,
                  concluida=False, data_criacao=None, data_conclusao=None):
    
        if not data_criacao:
            data_criacao = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        if concluida and not data_conclusao:
            data_conclusao = data_criacao
        
        ordem = OrdemServico(
            id_tecnico=id_tecnico,
            id_produto=id_produto,
            causa_raiz=causa_raiz,
            number_bd=number_bd,
            tipo=tipo,
            materiais_utilizados=materiais_utilizados,
            acao=acao,
            contato_responsavel=contato_responsavel,
            observacoes=observacoes,
            data_criacao=data_criacao,
            concluida=concluida,
            data_conclusao=data_conclusao
        )
        
        return self.repo.inserir(ordem)

    def listar_ordens(self):
        return self.repo.listar()
    
    def buscar_ordem(self, id_os):
        return self.repo.buscar_por_id(id_os)
    
    def concluir_ordem(self, id_os, data_conclusao=None):
        if not data_conclusao:
            data_conclusao = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.repo.atualizar_status(id_os, True, data_conclusao)
        return f"Ordem {id_os} concluída em {data_conclusao}"
    
    def listar_ordens_por_tecnico(self, id_tecnico):
        return self.repo.buscar_por_tecnico(id_tecnico)
    
    # ==================== FUNÇÕES PARA DADOS FORMATADOS ====================
    
    def get_dados_completos(self, tecnicos_dict, produtos_dict, clientes_dict, 
                            enderecos_dict, relacionamentos_list):
        """
        Retorna uma lista de dicionários com todas as informações das OS
        """
        ordens = self.listar_ordens()
        dados_completos = []
        
        for os in ordens:
            tecnico = tecnicos_dict.get(os.id_tecnico)
            produto = produtos_dict.get(os.id_produto)
            
            nome_cliente = "Não encontrado"
            endereco_cliente = "Não encontrado"
            
            if produto:
                for rel in relacionamentos_list:
                    if rel.id == produto.id_cliente_endereco:
                        cliente = clientes_dict.get(rel.id_cliente)
                        endereco = enderecos_dict.get(rel.id_endereco)
                        if cliente:
                            nome_cliente = cliente.nome
                        if endereco:
                            endereco_cliente = f"{endereco.logradouro}, {endereco.cidade}/{endereco.estado}"
                        break
            
            dados_completos.append({
                'id_os': os.id_os,
                'status': os.concluida,
                'data_criacao': os.data_criacao,
                'data_conclusao': os.data_conclusao,
                'number_bd': os.number_bd,
                'tipo': os.tipo,
                'tecnico_nome': tecnico.nome if tecnico else "Não encontrado",
                'tecnico_matricula': tecnico.matricula if tecnico else "Não encontrado",
                'cliente_nome': nome_cliente,
                'cliente_endereco': endereco_cliente,
                'produto_descricao': produto.descricao if produto else "Não encontrado",
                'produto_designador': produto.designador if produto else "Não encontrado",
                'produto_wan': produto.wan_piloto if produto else "Não encontrado",
                'causa_raiz': os.causa_raiz,
                'materiais': os.materiais_utilizados,
                'acao': os.acao,
                'contato': os.contato_responsavel,
                'observacoes': os.observacoes
            })
        
        return dados_completos
    
    
    def get_dados_resumidos(self, tecnicos_dict, produtos_dict, clientes_dict, relacionamentos_list):
        """
        Retorna uma lista de dicionários com dados resumidos (number_bd, designador, wan/piloto, cliente, técnico, data conclusão)
        """
        ordens = self.listar_ordens()
        dados_resumidos = []
        
        for os in ordens:
            tecnico = tecnicos_dict.get(os.id_tecnico)
            produto = produtos_dict.get(os.id_produto)
            
            nome_cliente = "-"
            wan_piloto = "-"
            if produto:
                wan_piloto = produto.wan_piloto if produto.wan_piloto else "-"
                for rel in relacionamentos_list:
                    if rel.id == produto.id_cliente_endereco:
                        cliente = clientes_dict.get(rel.id_cliente)
                        if cliente:
                            nome_cliente = cliente.nome
                        break
            
            designador = produto.designador if produto and produto.designador else "-"
            nome_tecnico = tecnico.nome if tecnico else "-"
            data_conclusao = os.data_conclusao if os.concluida and os.data_conclusao else "-"
            
            # Garantir que number_bd seja uma string
            number_bd = str(os.number_bd) if os.number_bd else "-"
            
            dados_resumidos.append({
                'number_bd': number_bd,
                'designador': designador,
                'wan_piloto': wan_piloto,
                'cliente': nome_cliente,
                'tecnico': nome_tecnico,
                'data_conclusao': data_conclusao,
                'concluida': os.concluida,
                'tipo': os.tipo if os.tipo else "-"
            })
        
        return dados_resumidos
    
    # ========================
    def get_estatisticas(self):
        """
        Retorna estatísticas das OS
        """
        ordens = self.listar_ordens()
        total = len(ordens)
        concluidas = len([os for os in ordens if os.concluida])
        em_andamento = total - concluidas
        
        return {
            'total': total,
            'concluidas': concluidas,
            'em_andamento': em_andamento
        }
        
        
        
        
    def get_dados_resumidos_por_tecnico(self, id_tecnico, tecnicos_dict, produtos_dict, 
                                        clientes_dict, relacionamentos_list):
        """
        Retorna dados resumidos das OS de um técnico específico
        """
        ordens = self.listar_ordens_por_tecnico(id_tecnico)
        dados_resumidos = []
        
        for os in ordens:
            produto = produtos_dict.get(os.id_produto)
            
            nome_cliente = "-"
            wan_piloto = "-"
            if produto:
                wan_piloto = produto.wan_piloto if produto.wan_piloto else "-"
                for rel in relacionamentos_list:
                    if rel.id == produto.id_cliente_endereco:
                        cliente = clientes_dict.get(rel.id_cliente)
                        if cliente:
                            nome_cliente = cliente.nome
                        break
            
            designador = produto.designador if produto and produto.designador else "-"
            data_conclusao = os.data_conclusao if os.concluida and os.data_conclusao else "-"
            
            # Garantir que number_bd seja uma string
            number_bd = str(os.number_bd) if os.number_bd else "-"
            
            dados_resumidos.append({
                'number_bd': number_bd,
                'designador': designador,
                'wan_piloto': wan_piloto,
                'cliente': nome_cliente,
                'data_conclusao': data_conclusao,
                'concluida': os.concluida,
                'tipo': os.tipo if os.tipo else "-"
            })
        
        return dados_resumidos