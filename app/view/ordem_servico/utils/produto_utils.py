def buscar_produto_por_wan(produto_controller, wan_piloto):
    """Buscar produto por WAN/Piloto"""
    todos_produtos = produto_controller.listar_produtos()
    
    for p in todos_produtos:
        if p.wan_piloto and p.wan_piloto.lower() == wan_piloto.lower():
            return p
    return None


def cadastrar_novo_produto(produto_controller, id_cliente, id_endereco, cliente_endereco_repo):
    """Cadastrar um novo produto para o relacionamento atual"""
    # Buscar o relacionamento cliente-endereço
    relacionamentos = cliente_endereco_repo.listar()
    id_relacionamento = None
    
    for rel in relacionamentos:
        if rel.id_cliente == id_cliente and rel.id_endereco == id_endereco:
            id_relacionamento = rel.id
            break
    
    if not id_relacionamento:
        print("❌ Relacionamento cliente-endereço não encontrado!")
        return None
    
    print("\n--- CADASTRO DE PRODUTO ---")
    descricao = input("Descrição: ")
    designador = input("Designador: ")
    wan_piloto = input("WAN/Piloto: ")
    
    produto = produto_controller.inserir_produto(
        descricao, designador, wan_piloto, id_relacionamento
    )
    
    if produto and produto.id_produto is not None:
        print(f"✅ Produto '{descricao}' cadastrado com sucesso!")
        return produto.id_produto
    else:
        print("❌ Erro ao cadastrar produto")
        return None


def selecionar_produto_existente(produto_controller, id_cliente, cliente_endereco_repo):
    """Selecionar produto existente do cliente (qualquer endereço)"""
    # Buscar TODOS os relacionamentos deste cliente
    relacionamentos = cliente_endereco_repo.listar()
    relacionamentos_cliente = [rel for rel in relacionamentos if rel.id_cliente == id_cliente]
    ids_relacionamentos = [rel.id for rel in relacionamentos_cliente]
    
    # Buscar produtos do cliente
    todos_produtos = produto_controller.listar_produtos()
    produtos_cliente = [p for p in todos_produtos if p.id_cliente_endereco in ids_relacionamentos]
    
    if not produtos_cliente:
        print("❌ Nenhum produto cadastrado para este cliente.")
        return None
    
    print(f"\n📋 PRODUTOS DO CLIENTE:")
    print("-" * 50)
    
    for p in produtos_cliente:
        print(f"ID: {p.id_produto} | {p.descricao} | Designador: {p.designador} | WAN: {p.wan_piloto}")
    
    try:
        id_produto = int(input("\nID do Produto: "))
        
        for p in produtos_cliente:
            if p.id_produto == id_produto:
                return id_produto
        
        print("❌ Produto não encontrado!")
        return None
    except ValueError:
        print("❌ ID inválido!")
        return None