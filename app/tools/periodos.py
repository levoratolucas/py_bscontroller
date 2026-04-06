# app/tools/periodos.py

from datetime import datetime, timedelta
from app.controller.ordem_servico_controller import OrdemServicoController


def obter_periodos_disponiveis(filtrar_concluidas=True, excluir_apoio=True):
    """
    Retorna lista de períodos disponíveis baseados nas OS
    Período: 21 de um mês a 20 do próximo mês
    
    Args:
        filtrar_concluidas (bool): Se True, considera apenas OS concluídas
        excluir_apoio (bool): Se True, exclui OS do tipo APOIO
    
    Returns:
        list: Lista de tuplas (data_inicio, data_fim) ordenadas por data mais recente
    """
    os_controller = OrdemServicoController()
    ordens = os_controller.listar_ordens()
    
    periodos = set()
    
    for os in ordens:
        if filtrar_concluidas and not os.concluida:
            continue
        if excluir_apoio and os.tipo == "APOIO":
            continue
        
        data_os = datetime.strptime(os.data_criacao[:10], "%Y-%m-%d")
        ano = data_os.year
        mes = data_os.month
        dia = data_os.day
        
        if dia >= 21:
            data_inicio = datetime(ano, mes, 21)
            if mes == 12:
                data_fim = datetime(ano + 1, 1, 20)
            else:
                data_fim = datetime(ano, mes + 1, 20)
        else:
            if mes == 1:
                data_inicio = datetime(ano - 1, 12, 21)
                data_fim = datetime(ano, 1, 20)
            else:
                data_inicio = datetime(ano, mes - 1, 21)
                data_fim = datetime(ano, mes, 20)
        
        periodos.add((data_inicio, data_fim))
    
    return sorted(list(periodos), key=lambda x: x[1], reverse=True)


def obter_meses_disponiveis():
    """
    Retorna lista de meses disponíveis baseados nas OS concluídas de REPARO e ATIVAÇÃO
    Período: mês civil (01 a último dia do mês)
    
    Returns:
        list: Lista de tuplas (ano, mes) ordenadas por data mais recente
    """
    os_controller = OrdemServicoController()
    ordens = os_controller.listar_ordens()
    
    meses = set()
    
    for os in ordens:
        if os.tipo not in ["REPARO", "ATIVAÇÃO"]:
            continue
        if not os.concluida:
            continue
        
        data = datetime.strptime(os.data_criacao[:10], "%Y-%m-%d")
        meses.add((data.year, data.month))
    
    return sorted(list(meses), key=lambda x: (x[0], x[1]), reverse=True)


def formatar_periodo(data_inicio, data_fim):
    """Formata o período para exibição curta (21/03 a 20/04)"""
    return f"{data_inicio.strftime('%d/%m')} a {data_fim.strftime('%d/%m')}"


def formatar_periodo_completo(data_inicio, data_fim):
    """Formata o período para exibição completa (21/03/2026 a 20/04/2026)"""
    return f"{data_inicio.strftime('%d/%m/%Y')} a {data_fim.strftime('%d/%m/%Y')}"


def formatar_mes(ano, mes):
    """Formata o mês para exibição (Abril/2026)"""
    from datetime import date
    return date(ano, mes, 1).strftime("%B/%Y")


def obter_primeiro_ultimo_dia_mes(ano, mes):
    """Retorna o primeiro e último dia do mês"""
    data_inicio = datetime(ano, mes, 1)
    if mes == 12:
        data_fim = datetime(ano + 1, 1, 1) - timedelta(days=1)
    else:
        data_fim = datetime(ano, mes + 1, 1) - timedelta(days=1)
    return data_inicio, data_fim