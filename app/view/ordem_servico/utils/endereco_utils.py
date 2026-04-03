def cadastrar_novo_endereco(endereco_controller):
    """Cadastrar um novo endereço"""
    print("\n--- CADASTRO DE NOVO ENDEREÇO ---")
    logradouro = input("Logradouro: ")
    cidade = input("Cidade: ")
    estado = input("Estado: ")
    
    endereco = endereco_controller.inserir_endereco(logradouro, cidade, estado)
    
    if endereco and endereco.id_endereco is not None:
        print(f"✅ Endereço '{logradouro}' cadastrado com sucesso!")
        return endereco.id_endereco
    else:
        print("❌ Erro ao cadastrar endereço")
        return None