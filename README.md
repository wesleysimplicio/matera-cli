# Matera CLI

CLI para API **Matera Edge Services** — pagamentos, conta, transações, PIX e mais.

## Instalação

```bash
cd ~/Projetos/Contribuicao/Brasil/matera-cli
pip install -e .
```

## Uso

```bash
# Autenticar
matera login --username SEU_EMAIL --username SUA_SENHA

# Dados do usuário
matera me

# Saldo
matera balance

# Extrato
matera statement

# Transações
matera transactions --limit 10

# Pagamento
matera payment --amount 150.00 --description "Cliente XYZ"

# Listar bancos
matera banks

# Saque
matera draft --value 100.00

# Config
matera config set --key account_id --value 12345
matera config list
```

## Comandos

| Comando | Descrição |
|---|---|
| `login` | Autenticar na API |
| `logout` | Remover token salvo |
| `me` | Dados do usuário logado |
| `balance` | Saldo da conta |
| `statement` | Extrato da conta |
| `transactions` | Listar transações |
| `payment` | Realizar pagamento |
| `banks` | Listar bancos |
| `draft` | Solicitar saque |
| `wallet` | Carteira de cartões |
| `permissions` | Permissões do usuário |
| `device-info` | Informações do dispositivo |
| `timeline` | Timeline da conta |
| `coupons` | Cupons |
| `settings` | Configurações do sistema |
| `client-info` | Dados completos do cliente |
| `config` | Gerenciar configurações |

## Documentação da API

- [Matera Edge Services API](https://doc-api-redoc-mtr.neocities.org/)
- Base URL: `https://api_mp.matera.com.br`

## Estrutura

```
matera-cli/
├── pyproject.toml       # Config do pacote
├── setup.py             # Fallback para instalação
├── README.md            # Esta documentação
├── matera/              # Módulo Python
│   ├── __init__.py
│   ├── __main__.py      # python -m matera
│   ├── cli.py           # CLI principal
│   ├── client.py        # HTTP client
│   └── config.py        # Config management
└── skill/               # Skill Hermes Agent
    └── SKILL.md
```

## Integração com Agentes

Este CLI é o motor. Use a **Skill Hermes** em `skill/SKILL.md` para que o Hermes Agent consuma a API diretamente.