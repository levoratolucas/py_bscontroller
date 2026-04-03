from datetime import datetime

def listar_todas_os_completo(os_controller, tecnico_controller, produto_controller,
                              cliente_controller, endereco_controller, cliente_endereco_repo):
    """Lista todas as OS com informações completas"""
    ordens = os_controller.listar_ordens()
    
    if not ordens:
        print("\n❌ Nenhuma Ordem de Serviço encontrada!")
        return
    
    print("\n" + "="*80)
    print("                     LISTA COMPLETA DE ORDENS DE SERVIÇO")
    print("="*80)
    
    tecnicos = {t.id: t for t in tecnico_controller.listar_tecnicos()}
    produtos = {p.id_produto: p for p in produto_controller.listar_produtos()}
    clientes = {c.id_cliente: c for c in cliente_controller.listar_clientes()}
    enderecos = {e.id_endereco: e for e in endereco_controller.listar_enderecos()}
    relacionamentos = cliente_endereco_repo.listar()
    
    for os in ordens:
        tecnico = tecnicos.get(os.id_tecnico)
        produto = produtos.get(os.id_produto)
        
        nome_cliente = "Não encontrado"
        endereco_cliente = "Não encontrado"
        
        if produto:
            for rel in relacionamentos:
                if rel.id == produto.id_cliente_endereco:
                    cliente = clientes.get(rel.id_cliente)
                    endereco = enderecos.get(rel.id_endereco)
                    if cliente:
                        nome_cliente = cliente.nome
                    if endereco:
                        endereco_cliente = f"{endereco.logradouro}, {endereco.cidade}/{endereco.estado}"
                    break
        
        status = "✅ CONCLUÍDA" if os.concluida else "🟡 EM ANDAMENTO"
        numero_os = os.number_bd if os.number_bd else os.id_os
        
        print(f"\n{'='*70}")
        print(f"🔧 OS Nº: {numero_os}")
        print(f"{'='*70}")
        print(f"   Status: {status}")
        print(f"   Tipo: {os.tipo if os.tipo else 'Não informado'}")
        print(f"\n📅 DATAS:")
        print(f"   Abertura: {os.data_criacao}")
        if os.concluida and os.data_conclusao:
            print(f"   Conclusão: {os.data_conclusao}")
            data_abertura = datetime.strptime(os.data_criacao, "%Y-%m-%d %H:%M:%S")
            data_conclusao = datetime.strptime(os.data_conclusao, "%Y-%m-%d %H:%M:%S")
            tempo_total = data_conclusao - data_abertura
            horas = tempo_total.total_seconds() / 3600
            print(f"   Tempo total: {horas:.1f} horas")
        elif not os.concluida:
            data_abertura = datetime.strptime(os.data_criacao, "%Y-%m-%d %H:%M:%S")
            agora = datetime.now()
            tempo_aberto = agora - data_abertura
            horas = tempo_aberto.total_seconds() / 3600
            print(f"   Tempo em aberto: {horas:.1f} horas")
        
        print(f"\n👤 TÉCNICO:")
        print(f"   Nome: {tecnico.nome if tecnico else 'Não encontrado'}")
        print(f"   Matrícula: {tecnico.matricula if tecnico else 'Não encontrado'}")
        
        print(f"\n👥 CLIENTE:")
        print(f"   Nome: {nome_cliente}")
        print(f"   Endereço: {endereco_cliente}")
        
        print(f"\n📦 PRODUTO:")
        if produto:
            print(f"   Descrição: {produto.descricao}")
            print(f"   Designador: {produto.designador}")
            print(f"   WAN/Piloto: {produto.wan_piloto}")
        else:
            print(f"   Produto não encontrado")
        
        print(f"\n📝 INFORMAÇÕES DA OS:")
        print(f"   Causa Raiz: {os.causa_raiz}")
        print(f"   Materiais Utilizados: {os.materiais_utilizados}")
        print(f"   Ação Realizada: {os.acao}")
        print(f"   Contato Responsável: {os.contato_responsavel}")
        print(f"   Observações: {os.observacoes}")


def listar_todas_os_resumido(os_controller, tecnico_controller, produto_controller,
                              cliente_controller, endereco_controller, cliente_endereco_repo):
    """Lista todas as OS de forma resumida"""
    
    tecnicos = {t.id: t for t in tecnico_controller.listar_tecnicos()}
    produtos = {p.id_produto: p for p in produto_controller.listar_produtos()}
    clientes = {c.id_cliente: c for c in cliente_controller.listar_clientes()}
    relacionamentos = cliente_endereco_repo.listar()
    
    dados_resumidos = os_controller.get_dados_resumidos(
        tecnicos, produtos, clientes, relacionamentos
    )
    
    if not dados_resumidos:
        print("\n❌ Nenhuma Ordem de Serviço encontrada!")
        return
    
    print("\n" + "="*130)
    print("                     LISTA RESUMIDA DE ORDENS DE SERVIÇO")
    print("="*130)
    print(f"{'Nº OS':<12} {'Tipo':<12} {'Designador':<20} {'WAN/Piloto':<18} {'Cliente':<25} {'Técnico':<18} {'Data Conclusão':<12}")
    print("-"*130)
    
    for item in dados_resumidos:
        numero_os = str(item['number_bd'])[:10] if item['number_bd'] != "-" else "-"
        tipo = item['tipo'][:10] if len(item['tipo']) > 10 else item['tipo']
        designador = item['designador'][:18] if len(item['designador']) > 18 else item['designador']
        wan_piloto = item['wan_piloto'][:16] if len(item.get('wan_piloto', '-')) > 16 else item.get('wan_piloto', '-')
        cliente = item['cliente'][:24] if len(item['cliente']) > 24 else item['cliente']
        tecnico = item['tecnico'][:16] if len(item['tecnico']) > 16 else item['tecnico']
        
        data_conclusao = item['data_conclusao']
        if data_conclusao != "-" and data_conclusao:
            try:
                data_obj = datetime.strptime(data_conclusao, "%Y-%m-%d %H:%M:%S")
                data_conclusao = data_obj.strftime("%d/%m/%Y")
            except:
                data_conclusao = "-"
        else:
            data_conclusao = "-"
        
        print(f"{numero_os:<12} {tipo:<12} {designador:<20} {wan_piloto:<18} {cliente:<25} {tecnico:<18} {data_conclusao:<12}")
    
    print("="*130)
    
    stats = os_controller.get_estatisticas()
    print(f"\n📊 ESTATÍSTICAS:")
    print(f"   Total de OS: {stats['total']}")
    print(f"   ✅ Concluídas: {stats['concluidas']}")
    print(f"   🟡 Em andamento: {stats['em_andamento']}")


def listar_os_por_tecnico_completo(os_controller, tecnico_controller, produto_controller,
                                    cliente_controller, endereco_controller, cliente_endereco_repo):
    """Lista OS por técnico com informações completas"""
    tecnicos = tecnico_controller.listar_tecnicos()
    
    if not tecnicos:
        print("❌ Nenhum técnico cadastrado!")
        return
    
    print("\n📋 TÉCNICOS DISPONÍVEIS:")
    for t in tecnicos:
        print(f"ID: {t.id} | Nome: {t.nome} | Matrícula: {t.matricula}")
    
    try:
        id_tecnico = int(input("\nID do Técnico: "))
    except ValueError:
        print("❌ ID inválido!")
        return
    
    ordens = os_controller.listar_ordens_por_tecnico(id_tecnico)
    
    if not ordens:
        print(f"❌ Nenhuma OS encontrada para este técnico!")
        return
    
    tecnico = next((t for t in tecnicos if t.id == id_tecnico), None)
    
    print(f"\n{'='*80}")
    print(f"   ORDENS DE SERVIÇO DO TÉCNICO: {tecnico.nome if tecnico else 'Desconhecido'}")
    print(f"{'='*80}")
    
    produtos = {p.id_produto: p for p in produto_controller.listar_produtos()}
    clientes = {c.id_cliente: c for c in cliente_controller.listar_clientes()}
    enderecos = {e.id_endereco: e for e in endereco_controller.listar_enderecos()}
    relacionamentos = cliente_endereco_repo.listar()
    
    for os in ordens:
        produto = produtos.get(os.id_produto)
        
        nome_cliente = "Não encontrado"
        endereco_cliente = "Não encontrado"
        
        if produto:
            for rel in relacionamentos:
                if rel.id == produto.id_cliente_endereco:
                    cliente = clientes.get(rel.id_cliente)
                    endereco = enderecos.get(rel.id_endereco)
                    if cliente:
                        nome_cliente = cliente.nome
                    if endereco:
                        endereco_cliente = f"{endereco.logradouro}, {endereco.cidade}/{endereco.estado}"
                    break
        
        status = "✅ CONCLUÍDA" if os.concluida else "🟡 EM ANDAMENTO"
        numero_os = os.number_bd if os.number_bd else os.id_os
        
        print(f"\n{'='*70}")
        print(f"🔧 OS Nº: {numero_os}")
        print(f"{'='*70}")
        print(f"   Status: {status}")
        print(f"   Tipo: {os.tipo if os.tipo else 'Não informado'}")
        print(f"\n📅 DATAS:")
        print(f"   Abertura: {os.data_criacao}")
        if os.concluida and os.data_conclusao:
            print(f"   Conclusão: {os.data_conclusao}")
            data_abertura = datetime.strptime(os.data_criacao, "%Y-%m-%d %H:%M:%S")
            data_conclusao = datetime.strptime(os.data_conclusao, "%Y-%m-%d %H:%M:%S")
            tempo_total = data_conclusao - data_abertura
            horas = tempo_total.total_seconds() / 3600
            print(f"   Tempo total: {horas:.1f} horas")
        elif not os.concluida:
            data_abertura = datetime.strptime(os.data_criacao, "%Y-%m-%d %H:%M:%S")
            agora = datetime.now()
            tempo_aberto = agora - data_abertura
            horas = tempo_aberto.total_seconds() / 3600
            print(f"   Tempo em aberto: {horas:.1f} horas")
        
        print(f"\n👥 CLIENTE:")
        print(f"   Nome: {nome_cliente}")
        print(f"   Endereço: {endereco_cliente}")
        
        print(f"\n📦 PRODUTO:")
        if produto:
            print(f"   Descrição: {produto.descricao}")
            print(f"   Designador: {produto.designador}")
            print(f"   WAN/Piloto: {produto.wan_piloto}")
        else:
            print(f"   Produto não encontrado")
        
        print(f"\n📝 INFORMAÇÕES DA OS:")
        print(f"   Causa Raiz: {os.causa_raiz}")
        print(f"   Materiais Utilizados: {os.materiais_utilizados}")
        print(f"   Ação Realizada: {os.acao}")
        print(f"   Contato Responsável: {os.contato_responsavel}")
        print(f"   Observações: {os.observacoes}")


def listar_os_por_tecnico_resumido(os_controller, tecnico_controller, produto_controller,
                                    cliente_controller, endereco_controller, cliente_endereco_repo):
    """Lista OS por técnico de forma resumida"""
    tecnicos = tecnico_controller.listar_tecnicos()
    
    if not tecnicos:
        print("❌ Nenhum técnico cadastrado!")
        return
    
    print("\n📋 TÉCNICOS DISPONÍVEIS:")
    for t in tecnicos:
        print(f"ID: {t.id} | Nome: {t.nome} | Matrícula: {t.matricula}")
    
    try:
        id_tecnico = int(input("\nID do Técnico: "))
    except ValueError:
        print("❌ ID inválido!")
        return
    
    produtos = {p.id_produto: p for p in produto_controller.listar_produtos()}
    clientes = {c.id_cliente: c for c in cliente_controller.listar_clientes()}
    relacionamentos = cliente_endereco_repo.listar()
    
    dados_resumidos = os_controller.get_dados_resumidos_por_tecnico(
        id_tecnico, tecnicos, produtos, clientes, relacionamentos
    )
    
    if not dados_resumidos:
        print(f"❌ Nenhuma OS encontrada para este técnico!")
        return
    
    tecnico = next((t for t in tecnicos if t.id == id_tecnico), None)
    
    print("\n" + "="*130)
    print(f"   ORDENS DE SERVIÇO DO TÉCNICO: {tecnico.nome if tecnico else 'Desconhecido'}")
    print("="*130)
    print(f"{'Nº OS':<12} {'Tipo':<12} {'Designador':<20} {'WAN/Piloto':<18} {'Cliente':<25} {'Status':<15} {'Data Conclusão':<12}")
    print("-"*130)
    
    for item in dados_resumidos:
        numero_os = str(item['number_bd'])[:10] if item['number_bd'] != "-" else "-"
        tipo = item['tipo'][:10] if len(item['tipo']) > 10 else item['tipo']
        designador = item['designador'][:18] if len(item['designador']) > 18 else item['designador']
        wan_piloto = item['wan_piloto'][:16] if len(item.get('wan_piloto', '-')) > 16 else item.get('wan_piloto', '-')
        cliente = item['cliente'][:24] if len(item['cliente']) > 24 else item['cliente']
        status = "✅ Concluída" if item['concluida'] else "🟡 Em andamento"
        
        data_conclusao = item['data_conclusao']
        if data_conclusao != "-" and data_conclusao:
            try:
                data_obj = datetime.strptime(data_conclusao, "%Y-%m-%d %H:%M:%S")
                data_conclusao = data_obj.strftime("%d/%m/%Y")
            except:
                data_conclusao = "-"
        else:
            data_conclusao = "-"
        
        print(f"{numero_os:<12} {tipo:<12} {designador:<20} {wan_piloto:<18} {cliente:<25} {status:<15} {data_conclusao:<12}")
    
    print("="*130)


def listar_os_por_tecnico_resumido_original(os_controller, tecnico_controller, produto_controller,
                                             cliente_controller, endereco_controller, cliente_endereco_repo):
    """Lista OS por técnico de forma resumida (versão original sem tipo)"""
    tecnicos = tecnico_controller.listar_tecnicos()
    
    if not tecnicos:
        print("❌ Nenhum técnico cadastrado!")
        return
    
    print("\n📋 TÉCNICOS DISPONÍVEIS:")
    for t in tecnicos:
        print(f"ID: {t.id} | Nome: {t.nome} | Matrícula: {t.matricula}")
    
    try:
        id_tecnico = int(input("\nID do Técnico: "))
    except ValueError:
        print("❌ ID inválido!")
        return
    
    produtos = {p.id_produto: p for p in produto_controller.listar_produtos()}
    clientes = {c.id_cliente: c for c in cliente_controller.listar_clientes()}
    relacionamentos = cliente_endereco_repo.listar()
    
    dados_resumidos = os_controller.get_dados_resumidos_por_tecnico(
        id_tecnico, tecnicos, produtos, clientes, relacionamentos
    )
    
    if not dados_resumidos:
        print(f"❌ Nenhuma OS encontrada para este técnico!")
        return
    
    tecnico = next((t for t in tecnicos if t.id == id_tecnico), None)
    
    print("\n" + "="*120)
    print(f"   ORDENS DE SERVIÇO DO TÉCNICO: {tecnico.nome if tecnico else 'Desconhecido'}")
    print("="*120)
    print(f"{'Nº OS':<12} {'Designador':<20} {'WAN/Piloto':<18} {'Cliente':<25} {'Status':<15} {'Data Conclusão':<12}")
    print("-"*120)
    
    for item in dados_resumidos:
        numero_os = str(item['number_bd'])[:10] if item['number_bd'] != "-" else "-"
        designador = item['designador'][:18] if len(item['designador']) > 18 else item['designador']
        wan_piloto = item['wan_piloto'][:16] if len(item.get('wan_piloto', '-')) > 16 else item.get('wan_piloto', '-')
        cliente = item['cliente'][:24] if len(item['cliente']) > 24 else item['cliente']
        status = "✅ Concluída" if item['concluida'] else "🟡 Em andamento"
        
        data_conclusao = item['data_conclusao']
        if data_conclusao != "-" and data_conclusao:
            try:
                data_obj = datetime.strptime(data_conclusao, "%Y-%m-%d %H:%M:%S")
                data_conclusao = data_obj.strftime("%d/%m/%Y")
            except:
                data_conclusao = "-"
        else:
            data_conclusao = "-"
        
        print(f"{numero_os:<12} {designador:<20} {wan_piloto:<18} {cliente:<25} {status:<15} {data_conclusao:<12}")
    
    print("="*120)


# Funções de menu para listagem
def menu_listar_todas(os_controller, tecnico_controller, produto_controller,
                      cliente_controller, endereco_controller, cliente_endereco_repo):
    """Submenu para escolher como listar todas as OS"""
    print("\n--- LISTAR TODAS AS OS ---")
    print("1 - Listagem Completa (detalhada)")
    print("2 - Listagem Resumida")
    print("0 - Voltar")
    
    opcao = input("Escolha: ")
    
    if opcao == "1":
        listar_todas_os_completo(os_controller, tecnico_controller, produto_controller,
                                 cliente_controller, endereco_controller, cliente_endereco_repo)
    elif opcao == "2":
        listar_todas_os_resumido(os_controller, tecnico_controller, produto_controller,
                                 cliente_controller, endereco_controller, cliente_endereco_repo)
    elif opcao == "0":
        return
    else:
        print("Opção inválida!")


def menu_listar_por_tecnico(os_controller, tecnico_controller, produto_controller,
                            cliente_controller, endereco_controller, cliente_endereco_repo):
    """Submenu para escolher como listar OS por técnico"""
    print("\n--- LISTAR OS POR TÉCNICO ---")
    print("1 - Listagem Completa (detalhada)")
    print("2 - Listagem Resumida")
    print("0 - Voltar")
    
    opcao = input("Escolha: ")
    
    if opcao == "1":
        listar_os_por_tecnico_completo(os_controller, tecnico_controller, produto_controller,
                                       cliente_controller, endereco_controller, cliente_endereco_repo)
    elif opcao == "2":
        listar_os_por_tecnico_resumido(os_controller, tecnico_controller, produto_controller,
                                       cliente_controller, endereco_controller, cliente_endereco_repo)
    elif opcao == "0":
        return
    else:
        print("Opção inválida!")