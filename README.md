     1|# Matera CLI 🏦
     2|
     3|**CLI + Skill Hermes Agent para API Matera Edge Services**
     4|
     5|Interface de linha de comando em Python para consumir a [API Matera Edge Services](https://doc-api-redoc-mtr.neocities.org/), com skill nativa para **Hermes Agent** — permitindo que agentes de IA conversacionais executem operações bancárias, consultas de saldo, pagamentos e mais, tudo via terminal.
     6|
     7|---
     8|
     9|## 📋 Índice
    10|
    11|- [Sobre o Projeto](#sobre-o-projeto)
    12|- [API Mapeada](#api-mapeada)
    13|- [Instalação](#instalação)
    14|- [Uso Básico](#uso-básico)
    15|- [Comandos](#comandos)
    16|- [Integração com LLMs e Agentes](#integração-com-llms-e-agentes)
    17|  - [Hermes Agent (Skill Nativa)](#hermes-agent-skill-nativa)
    18|  - [Claude Code / Codex](#claude-code--codex)
    19|  - [Futuro: MCP Server](#futuro-mcp-server)
    20|- [Estrutura do Projeto](#estrutura-do-projeto)
    21|- [Casos de Uso](#casos-de-uso)
    22|- [Contribuição](#contribuição)
    23|- [Licença](#licença)
    24|
    25|---
    26|
    27|## 🎯 Sobre o Projeto
    28|
    29|A **Matera** é uma provedora de tecnologia bancária B2B no Brasil (core banking, pagamentos, crédito, PIX). Diferente de fintechs como Nubank ou Stone, a Matera não expõe APIs públicas — sua documentação é acessível via contrato.
    30|
    31|Este projeto nasceu da necessidade de **criar uma ponte entre a API Matera e o ecossistema de agentes de IA**.
    32|
    33|Em vez de depender de SDKs proprietários ou portais fechados, construímos:
    34|
    35|1. **Um CLI Python completo** — cobrindo todos os 41 endpoints documentados
    36|2. **Uma skill Hermes Agent** — permitindo que o agente execute operações bancárias via linguagem natural
    37|3. **Um padrão replicável** — CLI como motor, skill como interface de agente
    38|
    39|O ganho real: **qualquer LLM ou agente (Hermes, Claude Code, Codex, Cursor) pode agora operar a API Matera sem precisar de integração customizada por endpoint.**
    40|
    41|---
    42|
    43|## 🔌 API Mapeada
    44|
    45|**Base URL:** `https://api_mp.matera.com.br`  
    46|**Documentação:** [doc-api-redoc-mtr.neocities.org](https://doc-api-redoc-mtr.neocities.org/)  
    47|**Autenticação:** Bearer token (obtido via `/v1/edge/login`)  
    48|**Endpoints mapeados:** 41
    49|
    50|### Categorias de Endpoints
    51|
    52|| Categoria | Endpoints | Descrição |
    53||---|---|---|
    54|| 🔐 **Autenticação** | 5 | Login, logout, reset de senha, validação de token |
    55|| 👤 **Cadastro** | 5 | Criar conta, atualizar, documentos, foto de perfil |
    56|| 📊 **Dados do Usuário** | 6 | Perfil, saldo, permissões, timeline, client info |
    57|| 💰 **Operações** | 4 | Saque (draft), liquidação, depósito, habilitar usuários |
    58|| 📋 **Transações** | 3 | Listar transações, consultar |
    59|| 💳 **Pagamentos** | 3 | Criar pagamento (boleto, cartão, débito), rejeitar |
    60|| 🎴 **Carteira (Wallet)** | 4 | Adicionar cartão, listar, atualizar alias, remover |
    61|| 📱 **Ativação** | 4 | Validação SMS, PIN, push, verificar telefone |
    62|| 🏦 **Dados Bancários** | 2 | Listar bancos |
    63|| 🎫 **Cupons** | 1 | Listar cupons da conta |
    64|| ⚙️ **Configurações** | 2 | Settings do sistema, device info |
    65|| 📬 **Push** | 1 | Registro de push notification |
    66|| 🎞️ **Timeline** | 1 | Timeline da conta |
    67|
    68|---
    69|
    70|## ⚡ Instalação
    71|
    72|### Pré-requisitos
    73|
    74|- Python 3.9+
    75|- Acesso à API Matera (credenciais B2B)
    76|
    77|### Instalar
    78|
    79|```bash
    80|git clone https://github.com/wesleysimplicio/matera-cli.git
    81|cd matera-cli
    82|pip install -e .
    83|```
    84|
    85|Verificar instalação:
    86|
    87|```bash
    88|matera --help
    89|```
    90|
    91|---
    92|
    93|## 🚀 Uso Básico
    94|
    95|### 1. Autenticar
    96|
    97|```bash
    98|matera login --username SEU_EMAIL --password SUA_SENHA
    99|```
   100|
   101|O token é salvo automaticamente em `~/.hermes2/scripts/matera-cli/token.json`.
   102|
   103|### 2. Consultar Saldo
   104|
   105|```bash
   106|matera balance
   107|```
   108|
   109|### 3. Ver Extrato
   110|
   111|```bash
   112|matera statement
   113|```
   114|
   115|### 4. Listar Transações
   116|
   117|```bash
   118|matera transactions --limit 10
   119|```
   120|
   121|### 5. Fazer um Pagamento
   122|
   123|```bash
   124|matera payment --amount 150.00 --description "Serviço de consultoria"
   125|```
   126|
   127|### 6. Listar Bancos
   128|
   129|```bash
   130|matera banks
   131|```
   132|
   133|---
   134|
   135|## 📖 Comandos
   136|
   137|| Comando | Descrição | Exemplo |
   138||---|---|---|
   139|| `login` | Autenticar na API | `matera login --username user --password pass` |
   140|| `logout` | Remover token | `matera logout` |
   141|| `me` | Dados do usuário logado | `matera me` |
   142|| `balance` | Saldo da conta | `matera balance` |
   143|| `statement` | Extrato bancário | `matera statement --account 12345` |
   144|| `transactions` | Listar transações | `matera transactions --limit 20` |
   145|| `payment` | Criar pagamento | `matera payment --amount 299.90 --description "Cliente" --type boleto` |
   146|| `banks` | Listar bancos | `matera banks --type ALL` |
   147|| `draft` | Solicitar saque | `matera draft --value 200.00` |
   148|| `wallet` | Carteira de cartões | `matera wallet` |
   149|| `permissions` | Permissões do usuário | `matera permissions` |
   150|| `device-info` | Info do dispositivo | `matera device-info` |
   151|| `timeline` | Timeline da conta | `matera timeline` |
   152|| `coupons` | Cupons disponíveis | `matera coupons` |
   153|| `settings` | Configs do sistema | `matera settings` |
   154|| `client-info` | Dados do cliente | `matera client-info` |
   155|| `config` | Gerenciar config | `matera config set --key account_id --value 54321` |
   156|
   157|---
   158|
   159|## 🤖 Integração com LLMs e Agentes
   160|
   161|### Hermes Agent (Skill Nativa)
   162|
   163|Este projeto inclui uma **skill Hermes Agent** registrada. Uma vez carregada, o agente pode executar qualquer operação da API Matera via linguagem natural.
   164|
   165|**Carregar a skill:**
   166|
   167|```python
   168|skill_view(name='matera-br')
   169|```
   170|
   171|**Exemplos de interação:**
   172|
   173|```
   174|👤 Usuário: "Qual meu saldo atual?"
   175|🤖 Agente: (carrega skill, executa `terminal("matera balance")`, retorna o saldo)
   176|
   177|👤 Usuário: "Faz um pagamento de R$ 200 pra conta de luz"
   178|🤖 Agente: (executa `terminal("matera payment --amount 200.00 --description "Conta de luz"")`)
   179|```
   180|
   181|**Fluxos pré-definidos na skill:**
   182|
   183|| Pergunta do Usuário | Ação do Agente |
   184||---|---|
   185|| "Qual meu saldo?" | `matera balance` |
   186|| "Quero ver o extrato" | `matera statement` |
   187|| "Lista as últimas transações" | `matera transactions --limit 10` |
   188|| "Faz um pagamento de R$ X" | `matera payment --amount X --description "..." ` |
   189|| "Quero sacar R$ X" | `matera draft --value X` |
   190|| "Mostra meus cartões" | `matera wallet` |
   191|| "Quais bancos estão disponíveis?" | `matera banks` |
   192|
   193|### Claude Code / Codex
   194|
   195|O CLI pode ser chamado diretamente por qualquer agente via subprocesso:
   196|
   197|```bash
   198|# Claude Code
   199|claude -p "Execute matera balance e me diga o saldo"
   200|
   201|# Codex CLI
   202|codex -p "Rode matera transactions --limit 5 e resuma"
   203|```
   204|
   205|### Futuro: MCP Server
   206|
   207|O mesmo CLI pode ser wrappado como um **MCP Server** (Model Context Protocol), permitindo que qualquer ferramenta compatível com MCP (Claude Desktop, Cursor, VS Code) consuma a API Matera como ferramentas nativas.
   208|
   209|---
   210|
   211|## 🏗️ Estrutura do Projeto
   212|
   213|```
   214|matera-cli/
   215|├── pyproject.toml           # Configuração do pacote Python
   216|├── setup.py                 # Fallback para instalação
   217|├── README.md                # Esta documentação
   218|├── .gitignore
   219|├── matera/                  # Módulo Python principal
   220|│   ├── __init__.py
   221|│   ├── __main__.py          # Suporte a python -m matera
   222|│   ├── cli.py               # CLI: argumentos, dispatch, 16 comandos
   223|│   ├── client.py            # HTTP client: requisições à API Matera
   224|│   └── config.py            # Config management + cache de token
   225|└── skill/
   226|    └── SKILL.md             # Skill Hermes Agent
   227|```
   228|
   229|### Arquitetura
   230|
   231|```
   232|┌─────────────┐     ┌──────────────┐     ┌─────────────────┐
   233|│  Usuário    │────▶│  Hermes      │────▶│  CLI (matera)   │
   234|│  (Discord)  │     │  Agent       │     │  Python         │
   235|└─────────────┘     └──────────────┘     └────────┬────────┘
   236|                                                   │
   237|                                                   ▼
   238|                                           ┌─────────────────┐
   239|                                           │  API Matera     │
   240|                                           │  Edge Services  │
   241|                                           │  api_mp.matera  │
   242|                                           └─────────────────┘
   243|```
   244|
   245|---
   246|
   247|## 💼 Casos de Uso
   248|
   249|### Para Negócios
   250|
   251|- **Consultoria de Imagem** — automatizar recebimentos de clientes
   252|- **FinOps** — consultar saldos e extrato sem abrir portal
   253|- **Automação de Cobrança** — disparar pagamentos recorrentes via agente
   254|- **Conciliação** — cruzar transações com dados de outras plataformas
   255|
   256|### Para Agentes de IA
   257|
   258|- **Suporte ao Cliente** — agente consulta extrato e responde em tempo real
   259|- **Orquestração Financeira** — pipeline multi-etapas com validação humana
   260|- **Dashboards Automáticos** — agente coleta dados e gera relatórios
   261|
   262|---
   263|
   264|## 🤝 Contribuição
   265|
   266|Projeto aberto para contribuição da comunidade. Sinta-se à vontade para:
   267|
   268|- Reportar issues
   269|- Sugerir novos endpoints
   270|- Criar MCP Server a partir do CLI
   271|- Adicionar suporte a PIX (quando disponível na API)
   272|
   273|---
   274|
   275|## 📄 Licença
   276|
   277|MIT
   278|
   279|---
   280|
   281|<p align="center">Feito com ☕ e 🦾 para o ecossistema Open Source Brasil</p>

## 🔌 API & Endpoints

**API Documentada:** Matera Edge Services API

**Quantidade de Endpoints:** 41

**Base URL:** `https://api.matera.com/edge/v1`

**Documentação Oficial:** https://docs.matera.com/

**Cobertura de Endpoints:**
Contas, pagamentos, transferências, boletos, webhooks, autenticação

**Autenticação:**
- OAuth 2.0 / Client Credentials (padrão Open Finance / bancos)
- Tokens gerenciados automaticamente pelo CLI
- Configuração via variáveis de ambiente ou arquivo de config

**Exemplo de uso:**
```bash
# Listar endpoints disponíveis
matera --help

# Exemplo de chamada (ajustar conforme CLI)
# matera account list
```
