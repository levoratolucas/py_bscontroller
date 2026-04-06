# app/tools/ordem_servico/count_os_tecnico.py

from datetime import datetime
from collections import defaultdict
from app.controller.ordem_servico_controller import OrdemServicoController
from app.controller.tecnico_controller import TecnicoController
from app.controller.produto_controller import ProdutoController
from app.controller.cliente_controller import ClienteController
from app.bd.cliente_endereco_repository import ClienteEnderecoRepository


def contar_os_concluidas_por_tecnico(data_inicio, data_fim):
    """
    Conta OS concluídas (sem APOIO) por técnico em um período
    Período: 21 de um mês a 20 do próximo mês
    
    Args:
        data_inicio (datetime): Data inicial do período
        data_fim (datetime): Data final do período
    
    Returns:
        dict: {
            'periodo': {'inicio': str, 'fim': str, 'inicio_formatado': str, 'fim_formatado': str},
            'dados': [{'tecnico_id': int, 'tecnico_nome': str, 'quantidade': int}],
            'total_os': int
        }
    """
    os_controller = OrdemServicoController()
    tecnico_controller = TecnicoController()
    
    ordens = os_controller.listar_ordens()
    tecnicos = {t.id: t.nome for t in tecnico_controller.listar_tecnicos()}
    
    contagem = defaultdict(int)
    
    for os in ordens:
        if not os.concluida:
            continue
        if os.tipo == "APOIO":
            continue
        
        data_os = datetime.strptime(os.data_criacao[:10], "%Y-%m-%d")
        if not (data_inicio <= data_os <= data_fim):
            continue
        
        contagem[os.id_tecnico] += 1
    
    dados = []
    for tecnico_id, qtd in sorted(contagem.items(), key=lambda x: x[1], reverse=True):
        dados.append({
            'tecnico_id': tecnico_id,
            'tecnico_nome': tecnicos.get(tecnico_id, "Desconhecido"),
            'quantidade': qtd
        })
    
    return {
        'periodo': {
            'inicio': data_inicio.strftime("%Y-%m-%d"),
            'fim': data_fim.strftime("%Y-%m-%d"),
            'inicio_formatado': data_inicio.strftime("%d/%m/%Y"),
            'fim_formatado': data_fim.strftime("%d/%m/%Y")
        },
        'dados': dados,
        'total_os': sum(contagem.values())
    }


def listar_os_por_tecnico_periodo(id_tecnico, data_inicio, data_fim):
    """
    Lista OS concluídas (sem APOIO) por técnico em um período específico
    Período: 21 de um mês a 20 do próximo mês
    
    Args:
        id_tecnico (int): ID do técnico
        data_inicio (datetime): Data inicial do período
        data_fim (datetime): Data final do período
    
    Returns:
        dict: {
            'tecnico': {'id': int, 'nome': str, 'matricula': str},
            'periodo': {'inicio': str, 'fim': str},
            'dados': [...],
            'total_os': int
        }
    """
    os_controller = OrdemServicoController()
    tecnico_controller = TecnicoController()
    produto_controller = ProdutoController()
    cliente_controller = ClienteController()
    cliente_endereco_repo = ClienteEnderecoRepository()
    
    # Buscar técnico
    tecnicos = tecnico_controller.listar_tecnicos()
    tecnico = None
    for t in tecnicos:
        if t.id == id_tecnico:
            tecnico = t
            break
    
    if not tecnico:
        return {
            'tecnico': None,
            'periodo': {
                'inicio': data_inicio.strftime("%d/%m/%Y"),
                'fim': data_fim.strftime("%d/%m/%Y")
            },
            'dados': [],
            'total_os': 0
        }
    
    # Buscar OS do período
    ordens = os_controller.listar_ordens()
    produtos = {p.id_produto: p for p in produto_controller.listar_produtos()}
    clientes = {c.id_cliente: c for c in cliente_controller.listar_clientes()}
    relacionamentos = cliente_endereco_repo.listar()
    
    # Mapear produto para cliente
    produto_cliente = {}
    for rel in relacionamentos:
        for p_id, p in produtos.items():
            if p.id_cliente_endereco == rel.id:
                produto_cliente[p_id] = rel.id_cliente
    
    # Filtrar OS
    dados = []
    
    for os in ordens:
        if os.id_tecnico != id_tecnico:
            continue
        if not os.concluida:
            continue
        if os.tipo == "APOIO":
            continue
        
        data_os = datetime.strptime(os.data_criacao[:10], "%Y-%m-%d")
        if not (data_inicio <= data_os <= data_fim):
            continue
        
        produto = produtos.get(os.id_produto)
        
        nome_cliente = "-"
        if produto:
            id_cliente = produto_cliente.get(produto.id_produto)
            if id_cliente:
                cliente = clientes.get(id_cliente)
                if cliente:
                    nome_cliente = cliente.nome
        
        dados.append({
            'numero_bd': os.number_bd,
            'tipo': os.tipo if os.tipo else "-",
            'data_abertura': os.data_criacao[:10],
            'data_conclusao': os.data_conclusao[:10] if os.data_conclusao else "-",
            'cliente': nome_cliente,
            'produto_desc': produto.descricao if produto else "-",
            'produto_wan': produto.wan_piloto if produto else "-",
            'causa_raiz': os.causa_raiz if os.causa_raiz else "-"
        })
    
    return {
        'tecnico': {
            'id': tecnico.id,
            'nome': tecnico.nome,
            'matricula': tecnico.matricula
        },
        'periodo': {
            'inicio': data_inicio.strftime("%d/%m/%Y"),
            'fim': data_fim.strftime("%d/%m/%Y")
        },
        'dados': dados,
        'total_os': len(dados)
    }


def listar_repetidos_periodo(data_inicio, data_fim):
    """
    Lista OS repetidas em um período (mês civil)
    Apenas REPARO e ATIVAÇÃO (concluídas)
    Considera repetido se mesmo WAN/Piloto com diferença <= 30 dias
    
    Args:
        data_inicio (datetime): Data inicial do período (01/MM/AAAA)
        data_fim (datetime): Data final do período (último dia do mês)
    
    Returns:
        dict: {
            'periodo': {'inicio': str, 'fim': str},
            'dados': [
                {
                    'numero_bd_repetido': str,
                    'wan_piloto': str,
                    'causa_raiz_repetido': str,
                    'cliente': str,
                    'data_repetido': str,
                    'numero_bd_referencia': str,
                    'tecnico_referencia': str,
                    'data_referencia': str,
                    'causa_raiz_referencia': str
                }
            ],
            'total_repetidos': int
        }
    """
    os_controller = OrdemServicoController()
    produto_controller = ProdutoController()
    cliente_controller = ClienteController()
    tecnico_controller = TecnicoController()
    cliente_endereco_repo = ClienteEnderecoRepository()
    
    # Buscar dados
    ordens = os_controller.listar_ordens()
    produtos = {p.id_produto: p for p in produto_controller.listar_produtos()}
    clientes = {c.id_cliente: c for c in cliente_controller.listar_clientes()}
    tecnicos = {t.id: t.nome for t in tecnico_controller.listar_tecnicos()}
    relacionamentos = cliente_endereco_repo.listar()
    
    # Mapear produto para cliente
    produto_cliente = {}
    for rel in relacionamentos:
        for p_id, p in produtos.items():
            if p.id_cliente_endereco == rel.id:
                produto_cliente[p_id] = rel.id_cliente
    
    # Filtrar apenas REPARO, ATIVAÇÃO e concluídas
    ordens_filtradas = []
    for os in ordens:
        if os.tipo not in ["REPARO", "ATIVAÇÃO"]:
            continue
        if not os.concluida:
            continue
        ordens_filtradas.append(os)
    
    # Ordenar por data (mais antiga primeiro)
    ordens_filtradas.sort(key=lambda x: x.data_criacao)
    
    # Agrupar por WAN/Piloto
    os_por_wan = {}
    for os in ordens_filtradas:
        produto = produtos.get(os.id_produto)
        if not produto:
            continue
        
        wan = produto.wan_piloto
        if not wan or wan == "-":
            continue
        
        if wan not in os_por_wan:
            os_por_wan[wan] = []
        
        os_por_wan[wan].append({
            'os': os,
            'data': datetime.strptime(os.data_criacao[:10], "%Y-%m-%d"),
            'numero_bd': os.number_bd,
            'wan_piloto': wan,
            'produto_id': os.id_produto,
            'tecnico_id': os.id_tecnico,
            'causa_raiz': os.causa_raiz if os.causa_raiz else "-"
        })
    
    # Identificar repetidos no período
    dados = []
    
    for wan, lista in os_por_wan.items():
        for i in range(1, len(lista)):
            dias_diff = (lista[i]['data'] - lista[i-1]['data']).days
            if dias_diff <= 30:
                if data_inicio <= lista[i]['data'] <= data_fim:
                    produto = produtos.get(lista[i]['produto_id'])
                    nome_cliente = "-"
                    if produto:
                        id_cliente = produto_cliente.get(produto.id_produto)
                        if id_cliente:
                            cliente = clientes.get(id_cliente)
                            if cliente:
                                nome_cliente = cliente.nome
                    
                    dados.append({
                        'numero_bd_repetido': lista[i]['numero_bd'],
                        'wan_piloto': lista[i]['wan_piloto'],
                        'causa_raiz_repetido': lista[i]['causa_raiz'],
                        'cliente': nome_cliente,
                        'data_repetido': lista[i]['data'].strftime("%d/%m/%Y"),
                        'numero_bd_referencia': lista[i-1]['numero_bd'],
                        'tecnico_referencia': tecnicos.get(lista[i-1]['tecnico_id'], "-"),
                        'data_referencia': lista[i-1]['data'].strftime("%d/%m/%Y"),
                        'causa_raiz_referencia': lista[i-1]['causa_raiz']
                    })
    
    return {
        'periodo': {
            'inicio': data_inicio.strftime("%d/%m/%Y"),
            'fim': data_fim.strftime("%d/%m/%Y")
        },
        'dados': dados,
        'total_repetidos': len(dados)
    }