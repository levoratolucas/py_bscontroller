# 📡 VIVO OS - Sistema de Ordem de Serviço

Sistema desktop para gerenciamento de Ordens de Serviço, desenvolvido em Python com foco em reparos e ativações de clientes.

![Versão](https://img.shields.io/badge/version-1.0.0-blue)
![Python](https://img.shields.io/badge/python-3.11+-green)
![License](https://img.shields.io/badge/license-MIT-orange)

---

## 📋 Índice

- [Funcionalidades](#-funcionalidades)
- [Arquitetura](#-arquitetura)
- [Tecnologias](#-tecnologias)
- [Instalação](#-instalação)
- [Banco de Dados](#-banco-de-dados)
- [Screenshots](#-screenshots)
- [Próximos Passos](#-próximos-passos)
- [Autor](#-autor)

---

## ✨ Funcionalidades

### 🎯 Gestão de OS
| Funcionalidade | Status | Descrição |
|----------------|--------|------------|
| Criar OS | ✅ | Cadastro com técnico, cliente, endereço e produto |
| Buscar por WAN/Piloto | ✅ | Auto preenchimento de cliente e endereço |
| Concluir OS | ✅ | Registro automático de data/hora |
| Consultar OS | ✅ | Por número, cliente, técnico ou período |

### 📊 Relatórios
| Relatório | Status | Descrição |
|-----------|--------|------------|
| Contagem por técnico | ✅ | Período 21/MM a 20/MM |
| Listagem detalhada | ✅ | OS por técnico e período |
| OS repetidas | ✅ | Mesmo produto em até 30 dias |

### 🔧 Cadastros
| Módulo | Status | Operações |
|--------|--------|-----------|
| Técnicos | ✅ | Criar, Listar |
| Clientes | ✅ | Criar, Listar, Buscar |
| Endereços | ✅ | Criar, Listar |
| Produtos | ✅ | Criar, Listar |

### 🎨 Interface
- ✅ Dashboard com KPIs em tempo real
- ✅ Cards de ação para navegação rápida
- ✅ Tabela com últimas OS
- ✅ Tema Vivo (roxo neon)

---

## 🏗️ Arquitetura

```
app/
├── bd/                          # Repositórios (acesso ao SQLite)
│   ├── conexao.py
│   ├── cliente_repository.py
│   ├── cliente_endereco_repository.py
│   ├── endereco_repository.py
│   ├── produto_repository.py
│   ├── tecnico_repository.py
│   └── ordem_servico_repository.py
│
├── controller/                  # Controladores (lógica de negócio)
│   ├── cliente_controller.py
│   ├── endereco_controller.py
│   ├── produto_controller.py
│   ├── tecnico_controller.py
│   └── ordem_servico_controller.py
│
├── model/                       # Modelos de dados
│   ├── cliente.py
│   ├── cliente_endereco.py
│   ├── endereco.py
│   ├── produto.py
│   ├── tecnico.py
│   └── ordem_servico.py
│
├── tools/                       # Ferramentas reutilizáveis
│   ├── periodos.py              # Cálculo de períodos
│   └── ordem_servico/
│       └── count_os_tecnico.py  # Relatórios de OS
│
├── view/                        # Views do console (testes)
│   └── test_view.py
│
└── frontend/                    # Interface gráfica
    ├── main_window.py           # Janela principal
    └── dashboard.py             # Dashboard
```

---

## 🛠️ Tecnologias

| Tecnologia | Versão | Finalidade |
|------------|--------|------------|
| Python | 3.11+ | Linguagem principal |
| SQLite3 | - | Banco de dados embutido |
| CustomTkinter | 5.2+ | Interface gráfica moderna |
| Pillow | 10.0+ | Processamento de imagens |

---

## 📦 Instalação

### 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/vivo-os.git
cd vivo-os
```

### 2. Crie um ambiente virtual (opcional)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python -m venv venv
source venv/bin/activate
```

### 3. Instale as dependências

```bash
pip install customtkinter pillow
```

### 4. Execute o sistema

```bash
python main_frontend.py
```

### 5. Para testes no console

```bash
python main_teste.py
```

---

## 📊 Banco de Dados

### Diagrama de Relacionamento

```
┌─────────────┐     ┌─────────────────────┐     ┌─────────────┐
│  tecnicos   │     │   ordem_servico     │     │  produtos   │
├─────────────┤     ├─────────────────────┤     ├─────────────┤
│ id (PK)     │◄───│ id_tecnico (FK)     │     │ id_produto  │
│ nome        │     │ id_produto (FK)    ──┼────►│ (PK)        │
│ matricula   │     │ number_bd           │     │ descricao   │
└─────────────┘     │ tipo                │     │ designador  │
                    │ data_criacao        │     │ wan_piloto  │
                    │ concluida           │     │ id_cliente_ │
                    │ data_conclusao      │     │ endereco(FK)│
                    └─────────────────────┘     └──────┬──────┘
                                                        │
                    ┌─────────────────────┐            │
                    │ cliente_endereco    │◄───────────┘
                    ├─────────────────────┤
                    │ id (PK)             │
                    │ id_cliente (FK)    ──┼───┐
                    │ id_endereco (FK)   ──┼───┼───┐
                    └─────────────────────┘   │   │
                           │                  │   │
                           ▼                  ▼   ▼
                    ┌─────────────┐     ┌─────────────┐
                    │  clientes   │     │  enderecos  │
                    ├─────────────┤     ├─────────────┤
                    │ id_cliente  │     │ id_endereco │
                    │ (PK)        │     │ (PK)        │
                    │ nome        │     │ logradouro  │
                    └─────────────┘     │ cidade      │
                                        │ estado      │
                                        └─────────────┘
```

### Scripts de Criação

```sql
-- Técnicos
CREATE TABLE tecnicos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT,
    matricula TEXT
);

-- Clientes
CREATE TABLE clientes (
    id_cliente INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT
);

-- Endereços
CREATE TABLE enderecos (
    id_endereco INTEGER PRIMARY KEY AUTOINCREMENT,
    logradouro TEXT,
    cidade TEXT,
    estado TEXT
);

-- Relacionamento Cliente-Endereço
CREATE TABLE cliente_endereco (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_cliente INTEGER,
    id_endereco INTEGER,
    FOREIGN KEY (id_cliente) REFERENCES clientes (id_cliente),
    FOREIGN KEY (id_endereco) REFERENCES enderecos (id_endereco)
);

-- Produtos
CREATE TABLE produtos (
    id_produto INTEGER PRIMARY KEY AUTOINCREMENT,
    descricao TEXT,
    designador TEXT,
    wan_piloto TEXT,
    id_cliente_endereco INTEGER,
    FOREIGN KEY (id_cliente_endereco) REFERENCES cliente_endereco (id)
);

-- Ordens de Serviço
CREATE TABLE ordem_servico (
    id_os INTEGER PRIMARY KEY AUTOINCREMENT,
    id_tecnico INTEGER,
    id_produto INTEGER,
    number_bd TEXT,
    tipo TEXT,
    causa_raiz TEXT,
    materiais_utilizados TEXT,
    acao TEXT,
    contato_responsavel TEXT,
    observacoes TEXT,
    data_criacao TEXT,
    concluida INTEGER,
    data_conclusao TEXT,
    FOREIGN KEY (id_tecnico) REFERENCES tecnicos (id),
    FOREIGN KEY (id_produto) REFERENCES produtos (id_produto)
);
```

---

## 📸 Screenshots

### Dashboard Principal

```
================================================================================
                        VIVO OS - Dashboard
================================================================================

┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│   📊         │ │   ✅         │ │   🟡         │ │   👤         │
│   Total OS   │ │  Concluídas  │ │ Em andamento │ │   Técnicos   │
│     23       │ │     23       │ │      0       │ │      5       │
└──────────────┘ └──────────────┘ └──────────────┘ └──────────────┘

┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│   ➕         │ │   🔍         │ │   📈         │ │   ⚙️         │
│   Nova OS    │ │  Consultar   │ │  Relatórios  │ │    Admin     │
└──────────────┘ └──────────────┘ └──────────────┘ └──────────────┘

📋 Últimas Ordens de Serviço
┌─────────────────────────────────────────────────────────────┐
│ Nº BD      │ Data        │ Status                           │
├─────────────────────────────────────────────────────────────┤
│ 6645869    │ 02/04/2026  │ ✅ Concluída                     │
│ 59081419   │ 02/04/2026  │ ✅ Concluída                     │
│ 6641346    │ 02/04/2026  │ ✅ Concluída                     │
│ 6643775    │ 02/04/2026  │ ✅ Concluída                     │
│ 6628239    │ 26/03/2026  │ ✅ Concluída                     │
└─────────────────────────────────────────────────────────────┘
```

### Relatório de OS Repetidas

```
================================================================================
📋 OS REPETIDAS (MESMO PRODUTO EM ATÉ 30 DIAS)
   Período: 01/04/2026 a 30/04/2026
================================================================================

Nº BD Rep  Data       WAN/Piloto     Cliente              Causa Raiz Rep        
--------------------------------------------------------------------------------
6641660    01/04/2026 187.9.51.69    IDT Brasil           NÃO HÁ                
6646239    04/04/2026 187.9.51.69    IDT Brasil           PERDA DE PACOTES      
6641346    02/04/2026 1968210        PUMATRONIX           TROCA POSTE           
--------------------------------------------------------------------------------

📊 TOTAL DE REPETIDOS: 3
================================================================================
```

---

## 🚀 Próximos Passos

- [ ] Tela completa de criação de OS
- [ ] Tela de consulta com filtros avançados
- [ ] Relatórios gráficos (matplotlib)
- [ ] Exportação de dados para CSV/Excel
- [ ] Dashboard com gráficos
- [ ] Sistema de backup
- [ ] Autenticação de usuários
- [ ] Modo noturno/claro

---

## 👤 Autor

**Seu Nome**

- GitHub: [@seu-usuario](https://github.com/seu-usuario)
- LinkedIn: [seu-linkedin](https://linkedin.com/in/seu-perfil)

---

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

---

## 🙏 Agradecimentos

- Vivo pelo tema inspirador
- Comunidade CustomTkinter
- Todos os contribuidores

---

⭐️ Se gostou do projeto, deixe uma estrela no GitHub!