# 📌 Sistema de Ordem de Serviço (CLI - Python + SQLite)

## 📖 Descrição

Este projeto é um sistema simples de cadastro e gerenciamento de informações para atividades B2B, utilizando **Python (MVC)** e **SQLite**.

A aplicação funciona via terminal (CLI) e permite cadastrar e listar:

* Técnicos
* Clientes
* Endereços
* Relacionamentos Cliente ↔ Endereço
* Produtos vinculados ao cliente/endereço

---

## 🏗️ Arquitetura

O projeto segue o padrão **MVC (Model - View - Controller)**:

```
app/
 ├── model/        # Entidades (classes)
 ├── controller/   # Regras de negócio
 ├── bd/           # Acesso ao banco (repositories)
 └── view/         # Interface (CLI/menu)
```

---

## 🧠 Conceitos aplicados

### 🔹 Banco de dados

* SQLite
* Tabelas com `id` auto incremental
* Relacionamentos:

  * Cliente ↔ Endereço (N:N)
  * Produto → Cliente_Endereço
  * Ordem de Serviço → Produto + Técnico

---

### 🔹 Padrões usados

* Repository Pattern (acesso ao banco)
* MVC
* Separação de responsabilidades

---

## 📂 Entidades

### 👨‍🔧 Técnico

* id
* nome
* matricula

---

### 🏢 Cliente

* id
* nome

---

### 📍 Endereço

* id
* logradouro
* cidade
* estado

---

### 🔗 Cliente_Endereço

Relaciona cliente com endereço

* id
* id_cliente
* id_endereco

---

### 📡 Produto

* id
* descricao
* designador
* wan_piloto
* id_cliente_endereco

---

### 📄 Ordem de Serviço

* id
* id_tecnico
* id_produto
* causa_raiz
* materiais_utilizados
* acao
* contato_responsavel
* observacoes
* data_criacao
* concluida (boolean)
* data_conclusao

---

## ⚙️ Regras importantes

### 🔥 ID AUTO INCREMENT

* Nunca enviar `id` ao criar objetos
* O banco gera automaticamente
* O `id` só existe após salvar

✔ Correto:

```python
cliente = Cliente("Empresa X")
```

❌ Errado:

```python
cliente = Cliente(id=1, nome="Empresa X")
```

---

## 🖥️ Funcionalidades

Menu principal:

```
1 - Criar Técnico
2 - Listar Técnicos
3 - Criar Cliente
4 - Listar Clientes
5 - Criar Endereço
6 - Listar Endereços
7 - Relacionar Cliente x Endereço
8 - Criar Produto
9 - Listar Produtos
0 - Sair
```

---

## ▶️ Como executar

```bash
python main.py
```

---

## 🚀 Fluxo recomendado

1. Criar técnico
2. Criar cliente
3. Criar endereço
4. Relacionar cliente ↔ endereço
5. Criar produto vinculado
6. (futuro) criar ordem de serviço

---

## ⚠️ Problemas resolvidos durante o desenvolvimento

### ❌ Erro: unexpected keyword argument 'id'

✔ Solução:

* Ajustar `__init__` dos models
* Não passar `id` na criação

---

### ❌ Erro: atributo id não existe

✔ Solução:

* Garantir que model possui `self.id`
* Ajustar retorno do repository

---

### ❌ Erro: parâmetros faltando no produto

✔ Solução:

* Corrigir assinatura do controller
* Passar todos os campos obrigatórios

---

## 🔮 Próximos passos

* [ ] Criar tela de Ordem de Serviço integrada
* [ ] Automatizar busca/relacionamentos
* [ ] Criar camada Service
* [ ] Criar API (FastAPI ou Flask)
* [ ] Interface web

---

## 👨‍💻 Autor

Lucas Levorato

---

## 💡 Observação final

Projeto focado em aprendizado de:

* Banco de dados relacional
* Organização de código (MVC)
* Boas práticas em Python

---
