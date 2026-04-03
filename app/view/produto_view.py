from app.controller.produto_controller import ProdutoController
from app.controller.cliente_controller import ClienteController
from app.controller.endereco_controller import EnderecoController
from app.bd.cliente_endereco_repository import ClienteEnderecoRepository

def menu_produto():
    produto_controller = ProdutoController()
    cliente_controller = ClienteController()
    endereco_controller = EnderecoController()
    cliente_endereco_repo = ClienteEnderecoRepository()
    
    while True:
        print("\n--- GERENCIAR PRODUTOS ---")
        print("1 - Inserir Produto")
        print("2 - Listar Produtos")
        print("3 - Listar Produtos por Cliente")
        print("0 - Voltar")
        
        op = input("Escolha: ")
        
        if op == "1":
            # Mostrar relacionamentos disponíveis
            relacionamentos = cliente_endereco_repo.listar()
            
            if not relacionamentos:
                print("\n❌ Nenhum relacionamento cliente-endereço encontrado!")
                print("Primeiro cadastre um cliente com endereço.")
                continue
            
            print("\n📋 RELACIONAMENTOS CLIENTE-ENDEREÇO DISPONÍVEIS:")
            print("-" * 60)
            
            # Buscar informações completas
            clientes = cliente_controller.listar_clientes()
            enderecos = endereco_controller.listar_enderecos()
            
            # Criar dicionários
            clientes_info = {c.id_cliente: c.nome for c in clientes}
            enderecos_info = {e.id_endereco: f"{e.logradouro}, {e.cidade}/{e.estado}" for e in enderecos}
            
            # Mostrar relacionamentos
            for rel in relacionamentos:
                nome_cliente = clientes_info.get(rel.id_cliente, "Desconhecido")
                endereco_str = enderecos_info.get(rel.id_endereco, "Endereço não encontrado")
                print(f"ID: {rel.id} | Cliente: {nome_cliente} | Endereço: {endereco_str}")
            
            try:
                id_cliente_endereco = int(input("\nID do relacionamento Cliente-Endereço: "))
            except ValueError:
                print("❌ ID inválido!")
                continue
            
            print("\n--- DADOS DO PRODUTO ---")
            descricao = input("Descrição: ")
            designador = input("Designador: ")
            wan_piloto = input("WAN/Piloto: ")
            
            produto = produto_controller.inserir_produto(
                descricao,
                designador,
                wan_piloto,
                id_cliente_endereco
            )
            
            if produto and produto.id_produto is not None:
                print(f"\n✅ Produto '{descricao}' cadastrado com sucesso!")
                print(f"   ID: {produto.id_produto}")
                print(f"   Designador: {designador}")
                print(f"   WAN/Piloto: {wan_piloto}")
            else:
                print("❌ Erro ao cadastrar produto")
                
        elif op == "2":
            produtos = produto_controller.listar_produtos()
            
            if not produtos:
                print("\nNenhum produto cadastrado.")
                continue
            
            print("\n📋 LISTA DE PRODUTOS:")
            print("=" * 80)
            
            # Buscar relacionamentos para mostrar o cliente associado
            relacionamentos = cliente_endereco_repo.listar()
            clientes = cliente_controller.listar_clientes()
            enderecos = endereco_controller.listar_enderecos()
            
            clientes_info = {c.id_cliente: c.nome for c in clientes}
            enderecos_info = {e.id_endereco: f"{e.logradouro}, {e.cidade}/{e.estado}" for e in enderecos}
            
            for p in produtos:
                # Buscar o relacionamento
                rel = None
                for r in relacionamentos:
                    if r.id == p.id_cliente_endereco:
                        rel = r
                        break
                
                if rel:
                    nome_cliente = clientes_info.get(rel.id_cliente, "Desconhecido")
                    endereco_str = enderecos_info.get(rel.id_endereco, "Desconhecido")
                    cliente_info = f"{nome_cliente} - {endereco_str}"
                else:
                    cliente_info = "Relacionamento não encontrado"
                
                print(f"\n🆔 ID: {p.id_produto}")
                print(f"   📝 Descrição: {p.descricao}")
                print(f"   🔖 Designador: {p.designador}")
                print(f"   🌐 WAN/Piloto: {p.wan_piloto}")
                print(f"   👥 Cliente/Endereço: {cliente_info}")
                print("-" * 40)
                
        elif op == "3":
            # Listar produtos por cliente específico
            clientes = cliente_controller.listar_clientes()
            
            if not clientes:
                print("\n❌ Nenhum cliente cadastrado.")
                continue
            
            print("\n📋 CLIENTES DISPONÍVEIS:")
            for c in clientes:
                print(f"ID: {c.id_cliente} | Nome: {c.nome}")
            
            try:
                id_cliente = int(input("\nID do cliente: "))
            except ValueError:
                print("❌ ID inválido!")
                continue
            
            # Buscar relacionamentos do cliente
            relacionamentos = cliente_endereco_repo.buscar_por_cliente(id_cliente)
            
            if not relacionamentos:
                print(f"\n❌ Nenhum endereço encontrado para este cliente.")
                continue
            
            # Pegar os IDs dos relacionamentos
            ids_relacionamentos = [rel.id for rel in relacionamentos]
            
            # Buscar produtos desses relacionamentos
            todos_produtos = produto_controller.listar_produtos()
            produtos_cliente = [p for p in todos_produtos if p.id_cliente_endereco in ids_relacionamentos]
            
            if not produtos_cliente:
                print(f"\n❌ Nenhum produto encontrado para este cliente.")
                continue
            
            # Buscar nome do cliente
            cliente = None
            for c in clientes:
                if c.id_cliente == id_cliente:
                    cliente = c
                    break
            
            print(f"\n📋 PRODUTOS DO CLIENTE: {cliente.nome if cliente else 'Desconhecido'}")
            print("=" * 60)
            
            for p in produtos_cliente:
                print(f"\n🆔 ID: {p.id_produto}")
                print(f"   📝 Descrição: {p.descricao}")
                print(f"   🔖 Designador: {p.designador}")
                print(f"   🌐 WAN/Piloto: {p.wan_piloto}")
                
        elif op == "0":
            break
        else:
            print("Opção inválida!")