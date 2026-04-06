# app/view/test_view.py

from datetime import datetime, timedelta
from app.tools import (
    obter_periodos_disponiveis,
    obter_meses_disponiveis,
    formatar_periodo,
    formatar_mes,
    obter_primeiro_ultimo_dia_mes,
    contar_os_concluidas_por_tecnico,
    listar_os_por_tecnico_periodo,
    listar_repetidos_periodo
)
from app.controller.tecnico_controller import TecnicoController


# ==================== FUNÇÃO 1: EXIBIR CONTAGEM ====================

def exibir_contagem(resultado):
    """Exibe a contagem de OS por técnico"""
    print("\n" + "="*60)
    print(f"📊 OS CONCLUÍDAS (SEM APOIO)")
    print(f"   Período: {resultado['periodo']['inicio_formatado']} a {resultado['periodo']['fim_formatado']}")
    print("="*60)
    print(f"\n{'Técnico':<35} {'Quantidade':<10}")
    print("-"*60)
    
    if not resultado['dados']:
        print("   Nenhuma OS encontrada no período")
    else:
        for item in resultado['dados']:
            nome = item['tecnico_nome'][:33] if len(item['tecnico_nome']) > 33 else item['tecnico_nome']
            print(f"{nome:<35} {item['quantidade']:<10}")
    
    print("-"*60)
    print(f"\n📊 TOTAL: {resultado['total_os']} OS")
    print("="*60)


def executar_contagem():
    """Executa a contagem de OS por técnico"""
    periodos = obter_periodos_disponiveis(filtrar_concluidas=True, excluir_apoio=True)
    
    if not periodos:
        print("\n❌ Nenhum período disponível!")
        return
    
    print("\n📅 SELECIONE O PERÍODO:")
    for i, (data_inicio, data_fim) in enumerate(periodos, 1):
        print(f"{i} - {formatar_periodo(data_inicio, data_fim)}")
    print("0 - Voltar")
    
    try:
        opcao = int(input("\nEscolha: "))
        if opcao == 0:
            return
        if 1 <= opcao <= len(periodos):
            data_inicio, data_fim = periodos[opcao - 1]
            resultado = contar_os_concluidas_por_tecnico(data_inicio, data_fim)
            exibir_contagem(resultado)
            input("\nPressione Enter para continuar...")
        else:
            print("Opção inválida!")
    except ValueError:
        print("Opção inválida!")


# ==================== FUNÇÃO 2: LISTAR OS POR TÉCNICO ====================

def exibir_lista_os(resultado):
    """Exibe a lista de OS por técnico e período"""
    
    if not resultado['tecnico']:
        print("\n❌ Técnico não encontrado!")
        return
    
    print("\n" + "="*110)
    print(f"📋 OS CONCLUÍDAS DO TÉCNICO: {resultado['tecnico']['nome']}")
    print(f"   Período: {resultado['periodo']['inicio']} a {resultado['periodo']['fim']}")
    print("="*110)
    
    if resultado['total_os'] == 0:
        print("\n   Nenhuma OS encontrada no período")
    else:
        print(f"\n{'Nº BD':<10} {'Tipo':<12} {'Data Abertura':<12} {'Data Conclusão':<12} {'Cliente':<25} {'WAN/Piloto':<18}")
        print("-"*110)
        
        for item in resultado['dados']:
            cliente = item['cliente'][:23] if len(item['cliente']) > 23 else item['cliente']
            print(f"{item['numero_bd']:<10} {item['tipo']:<12} {item['data_abertura']:<12} {item['data_conclusao']:<12} {cliente:<25} {item['produto_wan']:<18}")
    
    print("-"*110)
    print(f"\n📊 TOTAL: {resultado['total_os']} OS")
    print("="*110)


def selecionar_tecnico():
    """Seleciona um técnico da lista"""
    tecnico_controller = TecnicoController()
    tecnicos = tecnico_controller.listar_tecnicos()
    
    if not tecnicos:
        print("\n❌ Nenhum técnico cadastrado!")
        return None
    
    print("\n📋 TÉCNICOS DISPONÍVEIS:")
    for t in tecnicos:
        print(f"   {t.id} - {t.nome}")
    
    try:
        id_tecnico = int(input("\nID do técnico: "))
        for t in tecnicos:
            if t.id == id_tecnico:
                return id_tecnico
        print("❌ Técnico não encontrado!")
        return None
    except ValueError:
        print("❌ ID inválido!")
        return None


def executar_listagem():
    """Executa a listagem de OS por técnico"""
    id_tecnico = selecionar_tecnico()
    if not id_tecnico:
        return
    
    periodos = obter_periodos_disponiveis(filtrar_concluidas=True, excluir_apoio=True)
    
    if not periodos:
        print("\n❌ Nenhum período disponível!")
        return
    
    print("\n📅 SELECIONE O PERÍODO:")
    for i, (data_inicio, data_fim) in enumerate(periodos, 1):
        print(f"{i} - {formatar_periodo(data_inicio, data_fim)}")
    print("0 - Voltar")
    
    try:
        opcao = int(input("\nEscolha: "))
        if opcao == 0:
            return
        if 1 <= opcao <= len(periodos):
            data_inicio, data_fim = periodos[opcao - 1]
            resultado = listar_os_por_tecnico_periodo(id_tecnico, data_inicio, data_fim)
            exibir_lista_os(resultado)
            input("\nPressione Enter para continuar...")
        else:
            print("Opção inválida!")
    except ValueError:
        print("Opção inválida!")


# ==================== FUNÇÃO 3: LISTAR REPETIDOS ====================

def exibir_repetidos(resultado):
    """Exibe a lista de OS repetidas"""
    
    print("\n" + "="*200)
    print(f"📋 OS REPETIDAS (MESMO PRODUTO EM ATÉ 30 DIAS)")
    print(f"   Período: {resultado['periodo']['inicio']} a {resultado['periodo']['fim']}")
    print("="*200)
    
    if resultado['total_repetidos'] == 0:
        print("\n   Nenhuma OS repetida encontrada no período")
    else:
        print(f"\n{'Nº BD Rep':<12} {'Data':<12} {'WAN/Piloto':<18} {'Cliente':<22} {'Causa Raiz Rep':<30} {'Nº BD Ref':<12} {'Técnico Ref':<20} {'Data Ref':<12} {'Causa Raiz Ref':<30}")
        print("-"*200)
        
        for item in resultado['dados']:
            cliente = item['cliente'][:20] if len(item['cliente']) > 20 else item['cliente']
            wan = item['wan_piloto'][:16] if len(item.get('wan_piloto', '-')) > 16 else item.get('wan_piloto', '-')
            causa_repetido = item['causa_raiz_repetido'][:28] if len(item['causa_raiz_repetido']) > 28 else item['causa_raiz_repetido']
            causa_ref = item['causa_raiz_referencia'][:28] if len(item['causa_raiz_referencia']) > 28 else item['causa_raiz_referencia']
            
            print(f"{item['numero_bd_repetido']:<12} {item['data_repetido']:<12} {wan:<18} {cliente:<22} {causa_repetido:<30} {item['numero_bd_referencia']:<12} {item['tecnico_referencia']:<20} {item['data_referencia']:<12} {causa_ref:<30}")
    
    print("-"*200)
    print(f"\n📊 TOTAL DE REPETIDOS: {resultado['total_repetidos']}")
    print("="*200)


def selecionar_mes():
    """Seleciona um mês da lista"""
    meses = obter_meses_disponiveis()
    
    if not meses:
        print("\n❌ Nenhum mês disponível!")
        return None, None
    
    print("\n📅 SELECIONE O MÊS:")
    for i, (ano, mes) in enumerate(meses, 1):
        print(f"{i} - {formatar_mes(ano, mes)}")
    print("0 - Voltar")
    
    try:
        opcao = int(input("\nEscolha: "))
        if opcao == 0:
            return None, None
        if 1 <= opcao <= len(meses):
            ano, mes = meses[opcao - 1]
            data_inicio, data_fim = obter_primeiro_ultimo_dia_mes(ano, mes)
            return data_inicio, data_fim
        print("Opção inválida!")
        return None, None
    except ValueError:
        print("Opção inválida!")
        return None, None


def executar_repetidos():
    """Executa a listagem de OS repetidas"""
    data_inicio, data_fim = selecionar_mes()
    if not data_inicio:
        return
    
    resultado = listar_repetidos_periodo(data_inicio, data_fim)
    exibir_repetidos(resultado)
    input("\nPressione Enter para continuar...")


# ==================== MENU PRINCIPAL ====================

def menu_teste_principal():
    """Menu principal de teste"""
    while True:
        print("\n" + "="*50)
        print("       SISTEMA DE TESTE")
        print("="*50)
        print("1 - CONTAGEM DE OS POR TÉCNICO")
        print("2 - LISTAR OS POR TÉCNICO E PERÍODO")
        print("3 - LISTAR OS REPETIDAS")
        print("0 - SAIR")
        print("-"*50)
        
        opcao = input("Escolha: ")
        
        if opcao == "1":
            executar_contagem()
        elif opcao == "2":
            executar_listagem()
        elif opcao == "3":
            executar_repetidos()
        elif opcao == "0":
            print("\n✅ Saindo...")
            break
        else:
            print("Opção inválida!")