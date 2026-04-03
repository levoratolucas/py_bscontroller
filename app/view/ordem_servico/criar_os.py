from app.view.ordem_servico.utils import (
    selecionar_ou_criar_tecnico,
    selecionar_cliente_existente,
    cadastrar_novo_cliente,
    cadastrar_novo_produto,
    selecionar_produto_existente,
    buscar_produto_por_wan
)
from datetime import datetime

def capturar_multilinhas(mensagem):
    """Captura múltiplas linhas de texto. Digite 'FIM' em uma linha vazia para finalizar."""
    print(f"\n{mensagem}")
    print("(Digite 'FIM' em uma linha vazia para finalizar)")
    print("-" * 50)
    linhas = []
    while True:
        linha = input()
        if linha.strip() == "FIM":
            break
        linhas.append(linha)
    print("-" * 50)
    return "\n".join(linhas)


def criar_ordem_servico(os_controller, tecnico_controller, produto_controller, 
                        cliente_controller, endereco_controller, cliente_endereco_repo):
    
    print("\n" + "="*60)
    print("       NOVA ORDEM DE SERVIÇO")
    print("="*60)
    
    # 1. Perguntar se quer buscar por WAN/Piloto
    print("\n--- LOCALIZAR PRODUTO ---")
    print("1 - Buscar produto por WAN/Piloto")
    print("2 - Cadastrar tudo do zero (cliente, endereço, produto)")
    
    opcao_inicial = input("Escolha: ")
    
    id_produto = None
    id_cliente = None
    id_endereco = None
    id_tecnico = None
    
    # ==================== BUSCAR POR WAN/PILOTO ====================
    if opcao_inicial == "1":
        wan_piloto = input("\nDigite o WAN/Piloto do produto: ")
        produto_encontrado = buscar_produto_por_wan(produto_controller, wan_piloto)
        
        if not produto_encontrado:
            print(f"❌ Produto com WAN/Piloto '{wan_piloto}' não encontrado!")
            print("Vamos cadastrar um novo produto...")
            opcao_inicial = "2"
        else:
            print(f"\n✅ Produto encontrado!")
            print(f"   ID: {produto_encontrado.id_produto}")
            print(f"   Descrição: {produto_encontrado.descricao}")
            print(f"   Designador: {produto_encontrado.designador}")
            print(f"   WAN/Piloto: {produto_encontrado.wan_piloto}")
            
            # Buscar relacionamento
            relacionamentos = cliente_endereco_repo.listar()
            id_relacionamento = produto_encontrado.id_cliente_endereco
            
            for rel in relacionamentos:
                if rel.id == id_relacionamento:
                    id_cliente = rel.id_cliente
                    id_endereco = rel.id_endereco
                    break
            
            if id_cliente and id_endereco:
                clientes = cliente_controller.listar_clientes()
                enderecos = endereco_controller.listar_enderecos()
                
                cliente_info = next((c for c in clientes if c.id_cliente == id_cliente), None)
                endereco_info = next((e for e in enderecos if e.id_endereco == id_endereco), None)
                
                print(f"\n📋 DADOS DO CLIENTE:")
                print(f"   Cliente: {cliente_info.nome if cliente_info else 'Não encontrado'}")
                print(f"   Endereço: {endereco_info.logradouro if endereco_info else 'Não encontrado'}, "
                      f"{endereco_info.cidade if endereco_info else ''}/{endereco_info.estado if endereco_info else ''}")
                
                id_produto = produto_encontrado.id_produto
                print("\n✅ Produto localizado com sucesso!")
                print("Continuando com a criação da OS...")
            else:
                print("❌ Erro: Produto não está vinculado a nenhum cliente/endereço!")
                print("Vamos cadastrar um novo produto...")
                opcao_inicial = "2"
    
    # ==================== CADASTRAR TUDO DO ZERO ====================
    if opcao_inicial == "2":
        # Selecionar ou criar técnico
        id_tecnico = selecionar_ou_criar_tecnico(tecnico_controller)
        if not id_tecnico:
            print("❌ Operação cancelada!")
            return
        
        print("\n--- CLIENTE ---")
        print("1 - Selecionar cliente existente")
        print("2 - Cadastrar novo cliente")
        
        opcao_cliente = input("Escolha: ")
        novo_cadastro = False
        
        if opcao_cliente == "1":
            # Selecionar cliente existente (agora pode retornar produto também)
            resultado = selecionar_cliente_existente(
                cliente_controller, endereco_controller, cliente_endereco_repo, produto_controller
            )
            if resultado[0] is None:
                return
            id_cliente, id_endereco, id_produto, novo_cadastro = resultado
            
            if id_produto:
                # Já veio com produto selecionado
                print(f"\n✅ Produto já selecionado! ID: {id_produto}")
            elif novo_cadastro:
                print("\n🆕 Vamos cadastrar o produto agora.")
                id_produto = cadastrar_novo_produto(produto_controller, id_cliente, id_endereco, cliente_endereco_repo)
            else:
                # Não tem produto e não é novo cadastro, vai para seleção normal
                print("\n--- PRODUTO ---")
                print("1 - Selecionar produto existente")
                print("2 - Cadastrar novo produto")
                
                opcao_produto = input("Escolha: ")
                
                if opcao_produto == "1":
                    id_produto = selecionar_produto_existente(produto_controller, id_cliente, cliente_endereco_repo)
                elif opcao_produto == "2":
                    id_produto = cadastrar_novo_produto(produto_controller, id_cliente, id_endereco, cliente_endereco_repo)
                else:
                    print("Opção inválida!")
                    return
                
        elif opcao_cliente == "2":
            # Cadastrar novo cliente
            resultado = cadastrar_novo_cliente(cliente_controller, endereco_controller, cliente_endereco_repo)
            if resultado[0] is None:
                return
            id_cliente, id_endereco, novo_cadastro = resultado
            
            if novo_cadastro:
                print("\n🆕 NOVO CLIENTE/ENDEREÇO DETECTADO!")
                print("Vamos cadastrar o produto agora.")
                id_produto = cadastrar_novo_produto(produto_controller, id_cliente, id_endereco, cliente_endereco_repo)
        else:
            print("Opção inválida!")
            return
        
        if not id_produto:
            print("❌ Operação cancelada - Produto não definido!")
            return
    
    # ==================== VEIO DA BUSCA POR WAN/PILOTO ====================
    elif opcao_inicial == "1" and id_produto:
        id_tecnico = selecionar_ou_criar_tecnico(tecnico_controller)
        if not id_tecnico:
            print("❌ Operação cancelada!")
            return
    else:
        print("❌ Operação cancelada!")
        return
    
    # ==================== DADOS DA OS ====================
    print("\n--- DADOS DA ORDEM DE SERVIÇO ---")
    number_bd = input("Numero do bd: ")
    tipo = input("Reparo ou ativação: ")
    causa_raiz = input("Causa Raiz do Problema: ")
    materiais_utilizados = input("Materiais Utilizados: ")
    acao = input("Ação Realizada: ")
    contato_responsavel = input("Contato do Responsável: ")
    
    # Observações com múltiplas linhas
    observacoes = capturar_multilinhas("OBSERVAÇÕES (Digite 'FIM' para finalizar):")
    
    # ==================== STATUS E DATAS ====================
    print("\n--- STATUS E DATAS DA OS ---")
    print("1 - Em andamento")
    print("2 - Concluída")
    
    status_opcao = input("Escolha o status: ")
    concluida = (status_opcao == "2")
    
    # Função para solicitar data completa
    def solicitar_data_completa(nome_data):
        print(f"\n📅 {nome_data}")
        while True:
            try:
                ano = input("   Ano (YYYY): ").strip()
                if not ano:
                    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                mes = input("   Mês (MM): ").strip()
                dia = input("   Dia (DD): ").strip()
                hora = input("   Hora (HH): ").strip()
                minuto = input("   Minuto (MM): ").strip()
                
                # Validar se são números
                if not (ano.isdigit() and mes.isdigit() and dia.isdigit() and hora.isdigit() and minuto.isdigit()):
                    print("   ❌ Todos os campos devem ser números! Tente novamente.")
                    continue
                
                # Validar ranges
                if not (1 <= int(mes) <= 12):
                    print("   ❌ Mês inválido (1-12)! Tente novamente.")
                    continue
                
                if not (1 <= int(dia) <= 31):
                    print("   ❌ Dia inválido (1-31)! Tente novamente.")
                    continue
                
                if not (0 <= int(hora) <= 23):
                    print("   ❌ Hora inválida (0-23)! Tente novamente.")
                    continue
                
                if not (0 <= int(minuto) <= 59):
                    print("   ❌ Minuto inválido (0-59)! Tente novamente.")
                    continue
                
                # Formatar data
                data_formatada = f"{ano}-{mes.zfill(2)}-{dia.zfill(2)} {hora.zfill(2)}:{minuto.zfill(2)}:00"
                print(f"   ✅ Data definida: {data_formatada}")
                return data_formatada
                
            except Exception as e:
                print(f"   ❌ Erro: {e}. Tente novamente.")
    
    # Função para solicitar apenas horário
    def solicitar_horario(nome_data, data_base):
        print(f"\n📅 {nome_data} (mesmo dia da abertura)")
        while True:
            try:
                data_parts = data_base.split(" ")[0]
                
                hora = input("   Hora (HH): ").strip()
                minuto = input("   Minuto (MM): ").strip()
                
                if not (hora.isdigit() and minuto.isdigit()):
                    print("   ❌ Hora e minuto devem ser números! Tente novamente.")
                    continue
                
                if not (0 <= int(hora) <= 23):
                    print("   ❌ Hora inválida (0-23)! Tente novamente.")
                    continue
                
                if not (0 <= int(minuto) <= 59):
                    print("   ❌ Minuto inválido (0-59)! Tente novamente.")
                    continue
                
                data_formatada = f"{data_parts} {hora.zfill(2)}:{minuto.zfill(2)}:00"
                print(f"   ✅ Data definida: {data_formatada}")
                return data_formatada
                
            except Exception as e:
                print(f"   ❌ Erro: {e}. Tente novamente.")
    
    # Solicitar data de abertura
    data_criacao = solicitar_data_completa("DATA DE ABERTURA")
    
    # Solicitar data de conclusão se concluída
    data_conclusao = None
    if concluida:
        print("\n--- DATA DE CONCLUSÃO ---")
        print("1 - Mesmo dia da abertura")
        print("2 - Data diferente")
        
        opcao_conclusao = input("Escolha: ")
        
        if opcao_conclusao == "1":
            data_conclusao = solicitar_horario("DATA DE CONCLUSÃO", data_criacao)
        else:
            data_conclusao = solicitar_data_completa("DATA DE CONCLUSÃO")
    
    # ==================== CRIAR OS ====================
    ordem = os_controller.inserir_ordem(
        id_tecnico, 
        id_produto, 
        causa_raiz, 
        materiais_utilizados,
        acao, 
        contato_responsavel, 
        observacoes,
        number_bd,
        tipo,
        concluida,
        data_criacao,
        data_conclusao
    )
    
    if ordem and ordem.id_os:
        print("\n" + "="*60)
        print("✅ ORDEM DE SERVIÇO CRIADA COM SUCESSO!")
        print("="*60)
        print(f"   Número OS: {number_bd}")
        print(f"   Data de Abertura: {data_criacao}")
        if concluida:
            print(f"   Data de Conclusão: {data_conclusao}")
        print(f"   Status: {'CONCLUÍDA' if concluida else 'EM ANDAMENTO'}")
        print("="*60)
    else:
        print("❌ Erro ao criar Ordem de Serviço!")