from datetime import datetime

def buscar_os_por_id(os_controller, tecnico_controller, produto_controller,
                    cliente_controller, endereco_controller, cliente_endereco_repo):
    try:
        id_os = int(input("\nNúmero da OS: "))
    except ValueError:
        print("❌ ID inválido!")
        return
    
    os = os_controller.buscar_ordem(id_os)
    
    if not os:
        print(f"❌ Ordem de Serviço {id_os} não encontrada!")
        return
    
    tecnicos = {t.id: t for t in tecnico_controller.listar_tecnicos()}
    produtos = {p.id_produto: p for p in produto_controller.listar_produtos()}
    clientes = {c.id_cliente: c for c in cliente_controller.listar_clientes()}
    enderecos = {e.id_endereco: e for e in endereco_controller.listar_enderecos()}
    relacionamentos = cliente_endereco_repo.listar()
    
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
    
    status = "CONCLUÍDA" if os.concluida else "EM ANDAMENTO"
    
    print("\n" + "="*70)
    print(f"           ORDEM DE SERVIÇO Nº {os.id_os}")
    print("="*70)
    print(f"Status: {status}")
    print(f"\n📅 DATAS E HORÁRIOS:")
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
    
    print(f"\n--- DADOS DO TÉCNICO ---")
    print(f"Nome: {tecnico.nome if tecnico else 'Não encontrado'}")
    print(f"Matrícula: {tecnico.matricula if tecnico else 'Não encontrado'}")
    
    print(f"\n--- DADOS DO CLIENTE ---")
    print(f"Cliente: {nome_cliente}")
    print(f"Endereço: {endereco_cliente}")
    
    print(f"\n--- DADOS DO PRODUTO ---")
    if produto:
        print(f"Descrição: {produto.descricao}")
        print(f"Designador: {produto.designador}")
        print(f"WAN/Piloto: {produto.wan_piloto}")
    
    print(f"\n--- INFORMAÇÕES DA OS ---")
    print(f"Causa Raiz: {os.causa_raiz}")
    print(f"Materiais Utilizados: {os.materiais_utilizados}")
    print(f"Ação Realizada: {os.acao}")
    print(f"Contato Responsável: {os.contato_responsavel}")
    print(f"Observações: {os.observacoes}")
    print("="*70)