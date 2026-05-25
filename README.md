# Matera CLI 🏦

**CLI + Skill Hermes Agent para API Matera Edge Services**

Interface de linha de comando em Python para consumir a [API Matera Edge Services](https://doc-api-redoc-mtr.neocities.org/), com skill nativa para **Hermes Agent** — permitindo que agentes de IA conversacionais executem operações bancárias, consultas de saldo, pagamentos e mais, tudo via terminal.

---

## 📋 Índice

- [Sobre o Projeto](#sobre-o-projeto)
- [API Mapeada](#api-mapeada)
- [Instalação](#instalação)
- [Uso Básico](#uso-básico)
- [Comandos](#comandos)
- [Integração com LLMs e Agentes](#integração-com-llms-e-agentes)
  - [Hermes Agent (Skill Nativa)](#hermes-agent-skill-nativa)
  - [Claude Code / Codex](#claude-code--codex)
  - [Futuro: MCP Server](#futuro-mcp-server)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Casos de Uso](#casos-de-uso)
- [Contribuição](#contribuição)
- [Licença](#licença)

---

## 🎯 Sobre o Projeto

A **Matera** é uma provedora de tecnologia bancária B2B no Brasil (core banking, pagamentos, crédito, PIX). Diferente de fintechs como Nubank ou Stone, a Matera não expõe APIs públicas — sua documentação é acessível via contrato.

Este projeto nasceu da necessidade de **criar uma ponte entre a API Matera e o ecossistema de agentes de IA**.

Em vez de depender de SDKs proprietários ou portais fechados, construímos:

1. **Um CLI Python completo** — cobrindo todos os 41 endpoints documentados
2. **Uma skill Hermes Agent** — permitindo que o agente execute operações bancárias via linguagem natural
3. **Um padrão replicável** — CLI como motor, skill como interface de agente

O ganho real: **qualquer LLM ou agente (Hermes, Claude Code, Codex, Cursor) pode agora operar a API Matera sem precisar de integração customizada por endpoint.**

---

## 🔌 API Mapeada

**Base URL:** `https://api_mp.matera.com.br`  
**Documentação:** [doc-api-redoc-mtr.neocities.org](https://doc-api-redoc-mtr.neocities.org/)  
**Autenticação:** Bearer token (obtido via `/v1/edge/login`)  
**Endpoints mapeados:** 41

### Categorias de Endpoints

| Categoria | Endpoints | Descrição |
|---|---|---|
| 🔐 **Autenticação** | 5 | Login, logout, reset de senha, validação de token |
| 👤 **Cadastro** | 5 | Criar conta, atualizar, documentos, foto de perfil |
| 📊 **Dados do Usuário** | 6 | Perfil, saldo, permissões, timeline, client info |
| 💰 **Operações** | 4 | Saque (draft), liquidação, depósito, habilitar usuários |
| 📋 **Transações** | 3 | Listar transações, consultar |
| 💳 **Pagamentos** | 3 | Criar pagamento (boleto, cartão, débito), rejeitar |
| 🎴 **Carteira (Wallet)** | 4 | Adicionar cartão, listar, atualizar alias, remover |
| 📱 **Ativação** | 4 | Validação SMS, PIN, push, verificar telefone |
| 🏦 **Dados Bancários** | 2 | Listar bancos |
| 🎫 **Cupons** | 1 | Listar cupons da conta |
| ⚙️ **Configurações** | 2 | Settings do sistema, device info |
| 📬 **Push** | 1 | Registro de push notification |
| 🎞️ **Timeline** | 1 | Timeline da conta |

---

## ⚡ Instalação

### Pré-requisitos

- Python 3.9+
- Acesso à API Matera (credenciais B2B)

### Instalar

```bash
git clone https://github.com/wesleysimplicio/matera-cli.git
cd matera-cli
pip install -e .
```

Verificar instalação:

```bash
matera --help
```

---

## 🚀 Uso Básico

### 1. Autenticar

```bash
matera login --username SEU_EMAIL --password SUA_SENHA
```

O token é salvo automaticamente em `~/.hermes2/scripts/matera-cli/token.json`.

### 2. Consultar Saldo

```bash
matera balance
```

### 3. Ver Extrato

```bash
matera statement
```

### 4. Listar Transações

```bash
matera transactions --limit 10
```

### 5. Fazer um Pagamento

```bash
matera payment --amount 150.00 --description "Serviço de consultoria"
```

### 6. Listar Bancos

```bash
matera banks
```

---

## 📖 Comandos

| Comando | Descrição | Exemplo |
|---|---|---|
| `login` | Autenticar na API | `matera login --username user --password pass` |
| `logout` | Remover token | `matera logout` |
| `me` | Dados do usuário logado | `matera me` |
| `balance` | Saldo da conta | `matera balance` |
| `statement` | Extrato bancário | `matera statement --account 12345` |
| `transactions` | Listar transações | `matera transactions --limit 20` |
| `payment` | Criar pagamento | `matera payment --amount 299.90 --description "Cliente" --type boleto` |
| `banks` | Listar bancos | `matera banks --type ALL` |
| `draft` | Solicitar saque | `matera draft --value 200.00` |
| `wallet` | Carteira de cartões | `matera wallet` |
| `permissions` | Permissões do usuário | `matera permissions` |
| `device-info` | Info do dispositivo | `matera device-info` |
| `timeline` | Timeline da conta | `matera timeline` |
| `coupons` | Cupons disponíveis | `matera coupons` |
| `settings` | Configs do sistema | `matera settings` |
| `client-info` | Dados do cliente | `matera client-info` |
| `config` | Gerenciar config | `matera config set --key account_id --value 54321` |

---

## 🤖 Integração com LLMs e Agentes

### Hermes Agent (Skill Nativa)

Este projeto inclui uma **skill Hermes Agent** registrada. Uma vez carregada, o agente pode executar qualquer operação da API Matera via linguagem natural.

**Carregar a skill:**

```python
skill_view(name='matera-br')
```

**Exemplos de interação:**

```
👤 Usuário: "Qual meu saldo atual?"
🤖 Agente: (carrega skill, executa `terminal("matera balance")`, retorna o saldo)

👤 Usuário: "Faz um pagamento de R$ 200 pra conta de luz"
🤖 Agente: (executa `terminal("matera payment --amount 200.00 --description "Conta de luz"")`)
```

**Fluxos pré-definidos na skill:**

| Pergunta do Usuário | Ação do Agente |
|---|---|
| "Qual meu saldo?" | `matera balance` |
| "Quero ver o extrato" | `matera statement` |
| "Lista as últimas transações" | `matera transactions --limit 10` |
| "Faz um pagamento de R$ X" | `matera payment --amount X --description "..." ` |
| "Quero sacar R$ X" | `matera draft --value X` |
| "Mostra meus cartões" | `matera wallet` |
| "Quais bancos estão disponíveis?" | `matera banks` |

### Claude Code / Codex

O CLI pode ser chamado diretamente por qualquer agente via subprocesso:

```bash
# Claude Code
claude -p "Execute matera balance e me diga o saldo"

# Codex CLI
codex -p "Rode matera transactions --limit 5 e resuma"
```

### Futuro: MCP Server

O mesmo CLI pode ser wrappado como um **MCP Server** (Model Context Protocol), permitindo que qualquer ferramenta compatível com MCP (Claude Desktop, Cursor, VS Code) consuma a API Matera como ferramentas nativas.

---

## 🏗️ Estrutura do Projeto

```
matera-cli/
├── pyproject.toml           # Configuração do pacote Python
├── setup.py                 # Fallback para instalação
├── README.md                # Esta documentação
├── .gitignore
├── matera/                  # Módulo Python principal
│   ├── __init__.py
│   ├── __main__.py          # Suporte a python -m matera
│   ├── cli.py               # CLI: argumentos, dispatch, 16 comandos
│   ├── client.py            # HTTP client: requisições à API Matera
│   └── config.py            # Config management + cache de token
└── skill/
    └── SKILL.md             # Skill Hermes Agent
```

### Arquitetura

```
┌─────────────┐     ┌──────────────┐     ┌─────────────────┐
│  Usuário    │────▶│  Hermes      │────▶│  CLI (matera)   │
│  (Discord)  │     │  Agent       │     │  Python         │
└─────────────┘     └──────────────┘     └────────┬────────┘
                                                   │
                                                   ▼
                                           ┌─────────────────┐
                                           │  API Matera     │
                                           │  Edge Services  │
                                           │  api_mp.matera  │
                                           └─────────────────┘
```

---

## 💼 Casos de Uso

### Para Negócios

- **Consultoria de Imagem** — automatizar recebimentos de clientes
- **FinOps** — consultar saldos e extrato sem abrir portal
- **Automação de Cobrança** — disparar pagamentos recorrentes via agente
- **Conciliação** — cruzar transações com dados de outras plataformas

### Para Agentes de IA

- **Suporte ao Cliente** — agente consulta extrato e responde em tempo real
- **Orquestração Financeira** — pipeline multi-etapas com validação humana
- **Dashboards Automáticos** — agente coleta dados e gera relatórios

---

## 🤝 Contribuição

Projeto aberto para contribuição da comunidade. Sinta-se à vontade para:

- Reportar issues
- Sugerir novos endpoints
- Criar MCP Server a partir do CLI
- Adicionar suporte a PIX (quando disponível na API)

---

## 📄 Licença

MIT

---

<p align="center">Feito com ☕ e 🦾 para o ecossistema Open Source Brasil</p>