# app/view/ordem_servico_view.py

from app.tools.ordem_servivo.count_os_tecnico import (
    obter_periodos_disponiveis,
    contar_os_concluidas_por_tecnico
)


def exibir_resultado_contagem(resultado):
    """Exibe o resultado da contagem de OS por técnico"""
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


def listar_os_concluidas_por_tecnico():
    """Função que orquestra a listagem (busca dados e exibe)"""
    
    periodos = obter_periodos_disponiveis()
    
    if not periodos:
        print("\n❌ Nenhuma OS concluída encontrada!")
        return
    
    print("\n📅 SELECIONE O PERÍODO DE CONCLUSÃO:")
    for i, (data_inicio, data_fim) in enumerate(periodos, 1):
        print(f"{i} - {data_inicio.strftime('%d/%m')} a {data_fim.strftime('%d/%m')}")
    print("0 - Voltar")
    
    try:
        opcao = int(input("\nEscolha: "))
        if opcao == 0:
            return
        if 1 <= opcao <= len(periodos):
            data_inicio, data_fim = periodos[opcao - 1]
            resultado = contar_os_concluidas_por_tecnico(data_inicio, data_fim)
            exibir_resultado_contagem(resultado)
            input("\nPressione Enter para continuar...")
        else:
            print("Opção inválida!")
    except ValueError:
        print("Opção inválida!")