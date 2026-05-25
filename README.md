
![Project Illustration](https://v3b.fal.media/files/b/0a9b9c61/8BEyRZja7zdxPa5YO3_5G_moBjv4gJ.png)

     1|     1|# Matera CLI 🏦
     2|     2|
     3|     3|**CLI + Skill Hermes Agent para API Matera Edge Services**
     4|     4|
     5|     5|Interface de linha de comando em Python para consumir a [API Matera Edge Services](https://doc-api-redoc-mtr.neocities.org/), com skill nativa para **Hermes Agent** — permitindo que agentes de IA conversacionais executem operações bancárias, consultas de saldo, pagamentos e mais, tudo via terminal.
     6|     6|
     7|     7|---
     8|     8|
     9|     9|## 📋 Índice
    10|    10|
    11|    11|- [Sobre o Projeto](#sobre-o-projeto)
    12|    12|- [API Mapeada](#api-mapeada)
    13|    13|- [Instalação](#instalação)
    14|    14|- [Uso Básico](#uso-básico)
    15|    15|- [Comandos](#comandos)
    16|    16|- [Integração com LLMs e Agentes](#integração-com-llms-e-agentes)
    17|    17|  - [Hermes Agent (Skill Nativa)](#hermes-agent-skill-nativa)
    18|    18|  - [Claude Code / Codex](#claude-code--codex)
    19|    19|  - [Futuro: MCP Server](#futuro-mcp-server)
    20|    20|- [Estrutura do Projeto](#estrutura-do-projeto)
    21|    21|- [Casos de Uso](#casos-de-uso)
    22|    22|- [Contribuição](#contribuição)
    23|    23|- [Licença](#licença)
    24|    24|
    25|    25|---
    26|    26|
    27|    27|## 🎯 Sobre o Projeto
    28|    28|
    29|    29|A **Matera** é uma provedora de tecnologia bancária B2B no Brasil (core banking, pagamentos, crédito, PIX). Diferente de fintechs como Nubank ou Stone, a Matera não expõe APIs públicas — sua documentação é acessível via contrato.
    30|    30|
    31|    31|Este projeto nasceu da necessidade de **criar uma ponte entre a API Matera e o ecossistema de agentes de IA**.
    32|    32|
    33|    33|Em vez de depender de SDKs proprietários ou portais fechados, construímos:
    34|    34|
    35|    35|1. **Um CLI Python completo** — cobrindo todos os 41 endpoints documentados
    36|    36|2. **Uma skill Hermes Agent** — permitindo que o agente execute operações bancárias via linguagem natural
    37|    37|3. **Um padrão replicável** — CLI como motor, skill como interface de agente
    38|    38|
    39|    39|O ganho real: **qualquer LLM ou agente (Hermes, Claude Code, Codex, Cursor) pode agora operar a API Matera sem precisar de integração customizada por endpoint.**
    40|    40|
    41|    41|---
    42|    42|
    43|    43|## 🔌 API Mapeada
    44|    44|
    45|    45|**Base URL:** `https://api_mp.matera.com.br`  
    46|    46|**Documentação:** [doc-api-redoc-mtr.neocities.org](https://doc-api-redoc-mtr.neocities.org/)  
    47|    47|**Autenticação:** Bearer token (obtido via `/v1/edge/login`)  
    48|    48|**Endpoints mapeados:** 41
    49|    49|
    50|    50|### Categorias de Endpoints
    51|    51|
    52|    52|| Categoria | Endpoints | Descrição |
    53|    53||---|---|---|
    54|    54|| 🔐 **Autenticação** | 5 | Login, logout, reset de senha, validação de token |
    55|    55|| 👤 **Cadastro** | 5 | Criar conta, atualizar, documentos, foto de perfil |
    56|    56|| 📊 **Dados do Usuário** | 6 | Perfil, saldo, permissões, timeline, client info |
    57|    57|| 💰 **Operações** | 4 | Saque (draft), liquidação, depósito, habilitar usuários |
    58|    58|| 📋 **Transações** | 3 | Listar transações, consultar |
    59|    59|| 💳 **Pagamentos** | 3 | Criar pagamento (boleto, cartão, débito), rejeitar |
    60|    60|| 🎴 **Carteira (Wallet)** | 4 | Adicionar cartão, listar, atualizar alias, remover |
    61|    61|| 📱 **Ativação** | 4 | Validação SMS, PIN, push, verificar telefone |
    62|    62|| 🏦 **Dados Bancários** | 2 | Listar bancos |
    63|    63|| 🎫 **Cupons** | 1 | Listar cupons da conta |
    64|    64|| ⚙️ **Configurações** | 2 | Settings do sistema, device info |
    65|    65|| 📬 **Push** | 1 | Registro de push notification |
    66|    66|| 🎞️ **Timeline** | 1 | Timeline da conta |
    67|    67|
    68|    68|---
    69|    69|
    70|    70|## ⚡ Instalação
    71|    71|
    72|    72|### Pré-requisitos
    73|    73|
    74|    74|- Python 3.9+
    75|    75|- Acesso à API Matera (credenciais B2B)
    76|    76|
    77|    77|### Instalar
    78|    78|
    79|    79|```bash
    80|    80|git clone https://github.com/wesleysimplicio/matera-cli.git
    81|    81|cd matera-cli
    82|    82|pip install -e .
    83|    83|```
    84|    84|
    85|    85|Verificar instalação:
    86|    86|
    87|    87|```bash
    88|    88|matera --help
    89|    89|```
    90|    90|
    91|    91|---
    92|    92|
    93|    93|## 🚀 Uso Básico
    94|    94|
    95|    95|### 1. Autenticar
    96|    96|
    97|    97|```bash
    98|    98|matera login --username SEU_EMAIL --password SUA_SENHA
    99|    99|```
   100|   100|
   101|   101|O token é salvo automaticamente em `~/.hermes2/scripts/matera-cli/token.json`.
   102|   102|
   103|   103|### 2. Consultar Saldo
   104|   104|
   105|   105|```bash
   106|   106|matera balance
   107|   107|```
   108|   108|
   109|   109|### 3. Ver Extrato
   110|   110|
   111|   111|```bash
   112|   112|matera statement
   113|   113|```
   114|   114|
   115|   115|### 4. Listar Transações
   116|   116|
   117|   117|```bash
   118|   118|matera transactions --limit 10
   119|   119|```
   120|   120|
   121|   121|### 5. Fazer um Pagamento
   122|   122|
   123|   123|```bash
   124|   124|matera payment --amount 150.00 --description "Serviço de consultoria"
   125|   125|```
   126|   126|
   127|   127|### 6. Listar Bancos
   128|   128|
   129|   129|```bash
   130|   130|matera banks
   131|   131|```
   132|   132|
   133|   133|---
   134|   134|
   135|   135|## 📖 Comandos
   136|   136|
   137|   137|| Comando | Descrição | Exemplo |
   138|   138||---|---|---|
   139|   139|| `login` | Autenticar na API | `matera login --username user --password pass` |
   140|   140|| `logout` | Remover token | `matera logout` |
   141|   141|| `me` | Dados do usuário logado | `matera me` |
   142|   142|| `balance` | Saldo da conta | `matera balance` |
   143|   143|| `statement` | Extrato bancário | `matera statement --account 12345` |
   144|   144|| `transactions` | Listar transações | `matera transactions --limit 20` |
   145|   145|| `payment` | Criar pagamento | `matera payment --amount 299.90 --description "Cliente" --type boleto` |
   146|   146|| `banks` | Listar bancos | `matera banks --type ALL` |
   147|   147|| `draft` | Solicitar saque | `matera draft --value 200.00` |
   148|   148|| `wallet` | Carteira de cartões | `matera wallet` |
   149|   149|| `permissions` | Permissões do usuário | `matera permissions` |
   150|   150|| `device-info` | Info do dispositivo | `matera device-info` |
   151|   151|| `timeline` | Timeline da conta | `matera timeline` |
   152|   152|| `coupons` | Cupons disponíveis | `matera coupons` |
   153|   153|| `settings` | Configs do sistema | `matera settings` |
   154|   154|| `client-info` | Dados do cliente | `matera client-info` |
   155|   155|| `config` | Gerenciar config | `matera config set --key account_id --value 54321` |
   156|   156|
   157|   157|---
   158|   158|
   159|   159|## 🤖 Integração com LLMs e Agentes
   160|   160|
   161|   161|### Hermes Agent (Skill Nativa)
   162|   162|
   163|   163|Este projeto inclui uma **skill Hermes Agent** registrada. Uma vez carregada, o agente pode executar qualquer operação da API Matera via linguagem natural.
   164|   164|
   165|   165|**Carregar a skill:**
   166|   166|
   167|   167|```python
   168|   168|skill_view(name='matera-br')
   169|   169|```
   170|   170|
   171|   171|**Exemplos de interação:**
   172|   172|
   173|   173|```
   174|   174|👤 Usuário: "Qual meu saldo atual?"
   175|   175|🤖 Agente: (carrega skill, executa `terminal("matera balance")`, retorna o saldo)
   176|   176|
   177|   177|👤 Usuário: "Faz um pagamento de R$ 200 pra conta de luz"
   178|   178|🤖 Agente: (executa `terminal("matera payment --amount 200.00 --description "Conta de luz"")`)
   179|   179|```
   180|   180|
   181|   181|**Fluxos pré-definidos na skill:**
   182|   182|
   183|   183|| Pergunta do Usuário | Ação do Agente |
   184|   184||---|---|
   185|   185|| "Qual meu saldo?" | `matera balance` |
   186|   186|| "Quero ver o extrato" | `matera statement` |
   187|   187|| "Lista as últimas transações" | `matera transactions --limit 10` |
   188|   188|| "Faz um pagamento de R$ X" | `matera payment --amount X --description "..." ` |
   189|   189|| "Quero sacar R$ X" | `matera draft --value X` |
   190|   190|| "Mostra meus cartões" | `matera wallet` |
   191|   191|| "Quais bancos estão disponíveis?" | `matera banks` |
   192|   192|
   193|   193|### Claude Code / Codex
   194|   194|
   195|   195|O CLI pode ser chamado diretamente por qualquer agente via subprocesso:
   196|   196|
   197|   197|```bash
   198|   198|# Claude Code
   199|   199|claude -p "Execute matera balance e me diga o saldo"
   200|   200|
   201|   201|# Codex CLI
   202|   202|codex -p "Rode matera transactions --limit 5 e resuma"
   203|   203|```
   204|   204|
   205|   205|### Futuro: MCP Server
   206|   206|
   207|   207|O mesmo CLI pode ser wrappado como um **MCP Server** (Model Context Protocol), permitindo que qualquer ferramenta compatível com MCP (Claude Desktop, Cursor, VS Code) consuma a API Matera como ferramentas nativas.
   208|   208|
   209|   209|---
   210|   210|
   211|   211|## 🏗️ Estrutura do Projeto
   212|   212|
   213|   213|```
   214|   214|matera-cli/
   215|   215|├── pyproject.toml           # Configuração do pacote Python
   216|   216|├── setup.py                 # Fallback para instalação
   217|   217|├── README.md                # Esta documentação
   218|   218|├── .gitignore
   219|   219|├── matera/                  # Módulo Python principal
   220|   220|│   ├── __init__.py
   221|   221|│   ├── __main__.py          # Suporte a python -m matera
   222|   222|│   ├── cli.py               # CLI: argumentos, dispatch, 16 comandos
   223|   223|│   ├── client.py            # HTTP client: requisições à API Matera
   224|   224|│   └── config.py            # Config management + cache de token
   225|   225|└── skill/
   226|   226|    └── SKILL.md             # Skill Hermes Agent
   227|   227|```
   228|   228|
   229|   229|### Arquitetura
   230|   230|
   231|   231|```
   232|   232|┌─────────────┐     ┌──────────────┐     ┌─────────────────┐
   233|   233|│  Usuário    │────▶│  Hermes      │────▶│  CLI (matera)   │
   234|   234|│  (Discord)  │     │  Agent       │     │  Python         │
   235|   235|└─────────────┘     └──────────────┘     └────────┬────────┘
   236|   236|                                                   │
   237|   237|                                                   ▼
   238|   238|                                           ┌─────────────────┐
   239|   239|                                           │  API Matera     │
   240|   240|                                           │  Edge Services  │
   241|   241|                                           │  api_mp.matera  │
   242|   242|                                           └─────────────────┘
   243|   243|```
   244|   244|
   245|   245|---
   246|   246|
   247|   247|## 💼 Casos de Uso
   248|   248|
   249|   249|### Para Negócios
   250|   250|
   251|   251|- **Consultoria de Imagem** — automatizar recebimentos de clientes
   252|   252|- **FinOps** — consultar saldos e extrato sem abrir portal
   253|   253|- **Automação de Cobrança** — disparar pagamentos recorrentes via agente
   254|   254|- **Conciliação** — cruzar transações com dados de outras plataformas
   255|   255|
   256|   256|### Para Agentes de IA
   257|   257|
   258|   258|- **Suporte ao Cliente** — agente consulta extrato e responde em tempo real
   259|   259|- **Orquestração Financeira** — pipeline multi-etapas com validação humana
   260|   260|- **Dashboards Automáticos** — agente coleta dados e gera relatórios
   261|   261|
   262|   262|---
   263|   263|
   264|   264|## 🤝 Contribuição
   265|   265|
   266|   266|Projeto aberto para contribuição da comunidade. Sinta-se à vontade para:
   267|   267|
   268|   268|- Reportar issues
   269|   269|- Sugerir novos endpoints
   270|   270|- Criar MCP Server a partir do CLI
   271|   271|- Adicionar suporte a PIX (quando disponível na API)
   272|   272|
   273|   273|---
   274|   274|
   275|   275|## 📄 Licença
   276|   276|
   277|   277|MIT
   278|   278|
   279|   279|---
   280|   280|
   281|   281|<p align="center">Feito com ☕ e 🦾 para o ecossistema Open Source Brasil</p>
   282|
   283|## 🔌 API & Endpoints
   284|
   285|**API Documentada:** Matera Edge Services API
   286|
   287|**Quantidade de Endpoints:** 41
   288|
   289|**Base URL:** `https://api.matera.com/edge/v1`
   290|
   291|**Documentação Oficial:** https://docs.matera.com/
   292|
   293|**Cobertura de Endpoints:**
   294|Contas, pagamentos, transferências, boletos, webhooks, autenticação
   295|
   296|**Autenticação:**
   297|- OAuth 2.0 / Client Credentials (padrão Open Finance / bancos)
   298|- Tokens gerenciados automaticamente pelo CLI
   299|- Configuração via variáveis de ambiente ou arquivo de config
   300|
   301|**Exemplo de uso:**
   302|```bash
   303|# Listar endpoints disponíveis
   304|matera --help
   305|
   306|# Exemplo de chamada (ajustar conforme CLI)
   307|# matera account list
   308|```
   309|