from datetime import datetime

def listar_todas_os(os_controller, tecnico_controller, produto_controller,
                              cliente_controller, endereco_controller, cliente_endereco_repo):
    """Lista todas as OS com informações completas"""
    ordens = os_controller.listar_ordens()
    
    if not ordens:
        print("\n❌ Nenhuma Ordem de Serviço encontrada!")
        return
    
    print("\n" + "="*80)
    print("                     LISTA COMPLETA DE ORDENS DE SERVIÇO")
    print("="*80)
    
    # Buscar dados relacionados
    tecnicos = {t.id: t for t in tecnico_controller.listar_tecnicos()}
    produtos = {p.id_produto: p for p in produto_controller.listar_produtos()}
    clientes = {c.id_cliente: c for c in cliente_controller.listar_clientes()}
    enderecos = {e.id_endereco: e for e in endereco_controller.listar_enderecos()}
    relacionamentos = cliente_endereco_repo.listar()
    
    for os in ordens:
        tecnico = tecnicos.get(os.id_tecnico)
        produto = produtos.get(os.id_produto)
        
        # Buscar cliente e endereço do produto
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
        
        print(f"\n{'='*70}")
        print(f"🔧 OS Nº: {os.id_os}")
        print(f"{'='*70}")
        print(f"   Status: {status}")
        print(f"\n📅 DATAS:")
        print(f"   Abertura: {os.data_criacao}")
        if os.concluida and os.data_conclusao:
            print(f"   Conclusão: {os.data_conclusao}")
            # Calcular tempo total
            from datetime import datetime
            data_abertura = datetime.strptime(os.data_criacao, "%Y-%m-%d %H:%M:%S")
            data_conclusao = datetime.strptime(os.data_conclusao, "%Y-%m-%d %H:%M:%S")
            tempo_total = data_conclusao - data_abertura
            horas = tempo_total.total_seconds() / 3600
            print(f"   Tempo total: {horas:.1f} horas")
        elif not os.concluida:
            from datetime import datetime
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

def listar_os_por_tecnico(os_controller, tecnico_controller, produto_controller,
                         cliente_controller, endereco_controller, cliente_endereco_repo):
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
    
    print(f"\n📋 ORDENS DE SERVIÇO DO TÉCNICO: {tecnico.nome if tecnico else 'Desconhecido'}")
    print("="*70)
    
    produtos = {p.id_produto: p for p in produto_controller.listar_produtos()}
    clientes = {c.id_cliente: c for c in cliente_controller.listar_clientes()}
    relacionamentos = cliente_endereco_repo.listar()
    
    for os in ordens:
        produto = produtos.get(os.id_produto)
        
        nome_cliente = "Não encontrado"
        if produto:
            for rel in relacionamentos:
                if rel.id == produto.id_cliente_endereco:
                    cliente = clientes.get(rel.id_cliente)
                    if cliente:
                        nome_cliente = cliente.nome
                    break
        
        status = "✅ CONCLUÍDA" if os.concluida else "🟡 EM ANDAMENTO"
        
        print(f"\n🔧 OS Nº: {os.id_os} - {status}")
        print(f"   Cliente: {nome_cliente}")
        print(f"   Produto: {produto.descricao if produto else 'Não encontrado'}")
        if produto and produto.wan_piloto:
            print(f"   WAN/Piloto: {produto.wan_piloto}")
        print(f"   Data Abertura: {os.data_criacao}")
        if os.concluida and os.data_conclusao:
            print(f"   Data Conclusão: {os.data_conclusao}")
        print("-"*70)