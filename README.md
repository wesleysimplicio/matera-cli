![Matera CLI — hero editorial com referência aos 7 projetos financeiros](https://d2p7pg.cachecloud.net/output/cb4bd4b1-359f-4f9e-8a63-c99c3ea0d7f3-u2_dee34e58-b01c-4f7e-b713-4bea010a1b02.jpeg)

# Matera CLI 🏦

CLI em Python para a **API Matera Edge Services**, com foco em operações bancárias, contas, transações, pagamentos e dados do cliente.

Além do CLI, o projeto inclui uma **skill Hermes** para que agentes de IA possam executar essas ações via linguagem natural, usando a mesma base de comandos.

## O que já foi feito aqui

Este repositório já passou pela primeira camada de estruturação para agentes e engenharia:

- mapeamento com `llm-project-mapper`
- arquivos de contexto para agentes: `AGENTS.md`, `CLAUDE.md`, `INIT.md`
- estrutura de apoio com `.agents/`, `.skills/` e `.specs/`
- README reorganizado para leitura humana e por agentes
- documentação orientada a onboarding, API e uso prático
- imagem temática no topo para identificação rápida do projeto
- repositório público sincronizado no GitHub

## Automação vs equipe humana

A comparação abaixo é uma **estimativa conservadora** para a fase de descoberta, documentação e padronização inicial.

| Abordagem | Pessoas típicas | Tempo de setup inicial | Observações |
|---|---:|---:|---|
| Time manual | PM + engenheiro(a) + QA + DevOps + técnico(a) de documentação | 2 a 5 dias úteis | exige alinhamento, reuniões e revisão cruzada |
| Fluxo automatizado | 1 engenheiro(a) orquestrando agentes | 1 a 3 horas | reaproveita contexto, reduz retrabalho e padroniza saída |

**Economia estimada:** entre **70% e 90%** do tempo de setup e documentação inicial, dependendo do estado original do projeto.

## Para engenheiros e mantenedores

Se você vai continuar evoluindo este projeto:

1. Leia `AGENTS.md` antes de editar qualquer coisa.
2. Use a skill do projeto para entender o vocabulário e os fluxos esperados.
3. Mantenha o README, a skill e a implementação sincronizados.
4. Prefira mudanças pequenas, auditáveis e fáceis de revisar.
5. Não exponha credenciais, tokens ou dados de sessão.
6. Quando fizer uma mudança relevante, atualize também a documentação de API e os exemplos de uso.

## Visão geral

- **Nome do pacote:** `matera-cli`
- **Comando instalado:** `matera`
- **Runtime:** Python 3.9+
- **API base:** `https://api_mp.matera.com.br`
- **Documentação da API:** https://doc-api-redoc-mtr.neocities.org/
- **Endpoints mapeados:** 41
- **Auth:** Bearer token via `Authorization`
- **Cache local de sessão:** `~/.hermes2/scripts/matera-cli/`

## Onboarding para agentes 🤖

Se você é um agente lendo este repositório, siga este fluxo:

1. Leia `AGENTS.md` antes de editar qualquer coisa.
2. Use a skill **`matera-br`** para entender os fluxos esperados.
3. Evite commitar credenciais; o CLI já salva token e config localmente.
4. Prefira mudanças pequenas e verificáveis.
5. Antes de publicar ou automatizar, valide o comportamento real do CLI.

### Skill do Hermes

```python
skill_view(name='matera-br')
```

### Regras importantes

- O projeto roda como **CLI + skill**, não como backend web.
- O token é salvo localmente pelo CLI em `~/.hermes2/scripts/matera-cli/token.json`.
- A configuração local fica em `~/.hermes2/scripts/matera-cli/config.ini`.
- O projeto usa a API Matera real; alguns endpoints dependem de conta/credenciais válidas.

## Recursos principais

- Login e logout
- Consulta de perfil e cliente
- Saldo e extrato
- Transações
- Pagamentos
- Bancos disponíveis
- Saque/draft
- Carteira
- Permissões
- Configurações do sistema
- Timeline da conta
- Cupons
- Informações do dispositivo

## Instalação

### Pré-requisitos

- Python 3.9 ou superior
- Acesso a uma conta Matera válida

### Instalar localmente

```bash
git clone https://github.com/wesleysimplicio/matera-cli.git
cd matera-cli
pip install -e .
```

### Verificar a instalação

```bash
matera --help
```

## Uso rápido

### 1) Fazer login

```bash
matera login --username SEU_USUARIO --password SUA_SENHA
```

### 2) Definir conta padrão

```bash
matera config set --key defaults.account_id --value 12345
```

### 3) Consultar saldo

```bash
matera balance
```

### 4) Ver extrato

```bash
matera statement
```

### 5) Listar transações

```bash
matera transactions --limit 10
```

## Comandos disponíveis

| Comando | O que faz |
|---|---|
| `matera login` | Autentica e salva a sessão localmente |
| `matera logout` | Remove o token salvo |
| `matera me` | Mostra os dados do usuário logado |
| `matera balance` | Consulta o saldo |
| `matera statement` | Lista o extrato da conta |
| `matera transactions` | Lista transações da conta |
| `matera payment` | Cria um pagamento |
| `matera banks` | Lista bancos disponíveis |
| `matera draft` | Solicita saque/draft |
| `matera wallet` | Mostra a carteira de cartões |
| `matera permissions` | Lista permissões do usuário |
| `matera device-info` | Exibe informações do dispositivo |
| `matera timeline` | Mostra a timeline da conta |
| `matera coupons` | Lista cupons da conta |
| `matera settings` | Exibe configurações do sistema |
| `matera client-info` | Exibe dados do cliente |
| `matera config set|get|list` | Gerencia a configuração local |

## Exemplos úteis

### Pagamento

```bash
matera payment \
  --amount 150.00 \
  --description "Serviço de consultoria" \
  --type boleto
```

### Listar bancos

```bash
matera banks --type ALL
```

### Solicitar saque

```bash
matera draft --value 200.00
```

### Trocar conta padrão

```bash
matera config set --key defaults.account_id --value 54321
```

### Ler configuração

```bash
matera config list
matera config get --key defaults.account_id
```

## Integração com agentes

### Hermes Agent

A skill `matera-br` permite que o Hermes execute ações como:

- consultar saldo
- listar extrato
- criar pagamento
- listar transações
- consultar cliente
- operar configurações locais

### Claude Code / Codex

O CLI também pode ser chamado diretamente por agentes via subprocesso:

```bash
claude -p "Rode matera balance e me diga o saldo"
codex -p "Rode matera transactions --limit 5 e resuma"
```

## Estrutura do projeto

```text
matera-cli/
├── matera/
│   ├── __init__.py
│   ├── __main__.py
│   ├── cli.py
│   ├── client.py
│   └── config.py
├── skill/
│   └── SKILL.md
├── pyproject.toml
├── setup.py
└── README.md
```

## API mapeada

### Base URL

`https://api_mp.matera.com.br`

### Autenticação

- Login: `POST /v1/edge/login`
- Header: `Authorization: <token>`

### Principais grupos

| Grupo | Exemplos |
|---|---|
| Autenticação | login, logout, reset de senha, validação de token |
| Cadastro | criação e atualização de conta/dados do cliente |
| Dados do usuário | perfil, saldo, permissões, client info |
| Operações | saque/draft, depósito, habilitações |
| Transações | consultas e listagens |
| Pagamentos | boleto, cartão e débito |
| Carteira | cartões e aliases |
| Ativação | SMS, PIN, push e validação de telefone |
| Bancos | lista de bancos por tipo |
| Cupons | cupons da conta |
| Configurações | settings e device info |
| Timeline | histórico temporal da conta |

## Troubleshooting

### Token não encontrado

Se o CLI reclamar de autenticação, faça login novamente:

```bash
matera login --username SEU_USUARIO --password SUA_SENHA
```

### Conta padrão ausente

Se `statement`, `timeline` ou `draft` pedirem account ID, defina a conta padrão:

```bash
matera config set --key defaults.account_id --value 12345
```

### Erro de conexão

Verifique se o endpoint da Matera está acessível e se as credenciais estão corretas.

## Contribuição

1. Crie uma branch curta e descritiva.
2. Faça mudanças pequenas e testáveis.
3. Mantenha o README, a skill e o CLI alinhados.
4. Evite expor tokens, senhas ou dados de sessão.

## Licença

MIT.
