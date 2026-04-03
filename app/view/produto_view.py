from app.controller.produto_controller import ProdutoController

def menu_produto():
    produto_controller = ProdutoController()
    
    while True:
        print("\n--- GERENCIAR PRODUTOS ---")
        print("1 - Inserir Produto")
        print("2 - Listar Produtos")
        print("0 - Voltar")
        
        op = input("Escolha: ")
        
        if op == "1":
            descricao = input("Descrição: ")
            designador = input("Designador: ")
            wan_piloto = input("WAN/Piloto: ")
            
            print("\n⚠️  Será solicitado o ID do relacionamento Cliente-Endereço")
            id_cliente_endereco = int(input("ID Cliente_Endereço: "))
            
            resultado = produto_controller.inserir_produto(
                descricao,
                designador,
                wan_piloto,
                id_cliente_endereco
            )
            print(f"✅ {resultado}")
            
        elif op == "2":
            produtos = produto_controller.listar_produtos()
            if produtos:
                print("\n📋 LISTA DE PRODUTOS:")
                print("-" * 60)
                for p in produtos:
                    print(f"ID: {p.id_produto} | Desc: {p.descricao} | Designador: {p.designador} | WAN: {p.wan_piloto}")
            else:
                print("Nenhum produto cadastrado.")
                
        elif op == "0":
            break
        else:
            print("Opção inválida!")