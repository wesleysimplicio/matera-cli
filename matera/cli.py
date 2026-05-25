"""CLI principal — Matera Edge Services."""

import argparse
import hashlib
import json
import sys
from datetime import datetime
from typing import Optional

from matera.client import MateraAPIError, api_request
from matera.config import (
    clear_token,
    load_token,
    read_config,
    save_token,
    write_config,
)

# ─── Output helpers ────────────────────────────────────────────────────────

C_GREEN = "\033[92m"
C_YELLOW = "\033[93m"
C_RED = "\033[91m"
C_CYAN = "\033[96m"
C_RESET = "\033[0m"


def _pjson(data):
    """Print JSON formatado."""
    d = data.get("data", data) if isinstance(data, dict) else data
    print(json.dumps(d, indent=2, ensure_ascii=False))


def _ok(msg):
    print(f"{C_GREEN}✓{C_RESET} {msg}")


def _err(msg):
    print(f"{C_RED}✗{C_RESET} {msg}", file=sys.stderr)


def _warn(msg):
    print(f"{C_YELLOW}⚠{C_RESET} {msg}", file=sys.stderr)


def _info(msg):
    print(f"{C_CYAN}ℹ{C_RESET} {msg}")


# ─── Auth helpers ──────────────────────────────────────────────────────────

def _ensure_auth(token: Optional[str] = None) -> str:
    """Garante token válido: argumento > cache > config -> login."""
    if token:
        return token

    saved = load_token()
    if saved and saved.get("token"):
        return saved["token"]

    cfg = read_config()
    username = cfg.get("auth", "username", fallback="")
    password = cfg.get("auth", "password", fallback="")
    if username and password:
        result = _cmd_login(username, password)
        return result["token"]

    _err("Nenhum token. Use: matera login --username X --password Y")
    sys.exit(1)


def _get_holder_id(token: str) -> str:
    try:
        resp = api_request("GET", "/v1/edge/me", token=token)
        data = resp.get("data", resp)
        return data.get("accountHolderId", "")
    except MateraAPIError:
        return ""


def _get_default_account(token: str) -> str:
    cfg = read_config()
    aid = cfg.get("defaults", "account_id", fallback="")
    if aid:
        return aid
    try:
        resp = api_request("GET", "/v1/edge/me", token=token)
        data = resp.get("data", resp)
        accounts = data.get("accounts", [])
        if accounts:
            return accounts[0].get("accountId", "")
    except MateraAPIError:
        pass
    return ""


def _get_holder_and_account(token: str):
    holder = _get_holder_id(token)
    account = _get_default_account(token)
    if not holder:
        _err("Não foi possível obter accountHolderId")
        sys.exit(1)
    return holder, account


# ─── Commands ──────────────────────────────────────────────────────────────

def _cmd_login(username: str, password: str) -> dict:
    data = {"username": username, "password": password}
    resp = api_request("POST", "/v1/edge/login",
                       data=data, content_type="application/x-www-form-urlencoded")
    token = resp.get("data", {}).get("token", "")
    if token:
        save_token({"token": token, "username": username})
        cfg = read_config()
        cfg["auth"]["username"] = username
        cfg["auth"]["password"] = password
        write_config(cfg)
        _ok(f"Login: {username}")
        _info(f"Token: {token[:20]}...")
    return resp.get("data", resp)


def cmd_login(args):
    _cmd_login(args.username, args.password)


def cmd_logout(args):
    clear_token()
    _ok("Sessão encerrada")


def cmd_me(args):
    t = _ensure_auth(args.token)
    resp = api_request("GET", "/v1/edge/me", token=t)
    _pjson(resp)


def cmd_balance(args):
    t = _ensure_auth(args.token)
    holder, _ = _get_holder_and_account(t)
    resp = api_request("GET", f"/v1/edge/client/{holder}/balance", token=t)
    _pjson(resp)


def cmd_statement(args):
    t = _ensure_auth(args.token)
    aid = args.account or _get_default_account(t)
    if not aid:
        _err("Informe --account ou configure account_id")
        return
    resp = api_request("GET", f"/v1/edge/accounts/{aid}/statement", token=t)
    _pjson(resp)


def cmd_transactions(args):
    t = _ensure_auth(args.token)
    holder, aid = _get_holder_and_account(t)
    aid = args.account or aid
    params = {}
    if args.limit:
        params["limit"] = str(args.limit)
    resp = api_request("GET",
                       f"/v1/edge/client/{holder}/account/{aid}/transaction",
                       token=t, params=params)
    _pjson(resp)


def cmd_payment(args):
    t = _ensure_auth(args.token)
    data = {
        "totalAmount": args.amount,
        "transactionType": args.tx_type,
        "senderComment": args.description or f"Pagamento R${args.amount:.2f}",
    }
    extra = {
        "S-transaction": hashlib.md5(
            str(datetime.now().timestamp()).encode()
        ).hexdigest()[:16],
    }
    resp = api_request("POST", "/v1/edge/payments",
                       token=t, data=data, extra_headers=extra)
    _pjson(resp)


def cmd_banks(args):
    t = _ensure_auth(args.token)
    resp = api_request("GET", f"/v1/edge/banks/type/{args.type}", token=t)
    _pjson(resp)


def cmd_draft(args):
    t = _ensure_auth(args.token)
    aid = args.account or _get_default_account(t)
    if not aid:
        _err("Informe --account ou configure account_id")
        return
    data = {
        "value": args.value,
        "externalIdentifier": f"draft-{int(datetime.now().timestamp())}",
        "currency": "BRL",
    }
    resp = api_request("POST", f"/v1/edge/account/{aid}/draft", token=t, data=data)
    _pjson(resp)


def cmd_wallet(args):
    t = _ensure_auth(args.token)
    holder, aid = _get_holder_and_account(t)
    resp = api_request("GET",
                       f"/v1/edge/client/{holder}/account/{aid}/wallet",
                       token=t)
    _pjson(resp)


def cmd_permissions(args):
    t = _ensure_auth(args.token)
    resp = api_request("GET", "/v1/edge/permissions", token=t)
    _pjson(resp)


def cmd_device(args):
    t = _ensure_auth(args.token)
    resp = api_request("GET", "/v1/edge/device-info", token=t)
    _pjson(resp)


def cmd_timeline(args):
    t = _ensure_auth(args.token)
    aid = args.account or _get_default_account(t)
    if not aid:
        _err("Informe --account")
        return
    resp = api_request("GET", f"/v1/edge/timeline/{aid}", token=t)
    _pjson(resp)


def cmd_coupons(args):
    t = _ensure_auth(args.token)
    holder, aid = _get_holder_and_account(t)
    resp = api_request("GET",
                       f"/v1/edge/client/{holder}/account/{aid}/coupon",
                       token=t)
    _pjson(resp)


def cmd_settings(args):
    t = _ensure_auth(args.token)
    resp = api_request("GET", "/v1/edge/settings", token=t)
    _pjson(resp)


def cmd_client_info(args):
    t = _ensure_auth(args.token)
    holder, _ = _get_holder_and_account(t)
    resp = api_request("GET", f"/v1/edge/client/{holder}", token=t)
    _pjson(resp)


def cmd_config(args):
    cfg = read_config()
    if args.config_action == "set":
        section, key = (args.key.split(".", 1) if "." in args.key
                        else ("auth", args.key))
        if section not in cfg:
            cfg[section] = {}
        cfg[section][key] = args.value
        write_config(cfg)
        _ok(f"{section}.{key} = {args.value}")
    elif args.config_action == "get":
        section, key = (args.key.split(".", 1) if "." in args.key
                        else ("auth", args.key))
        val = cfg.get(section, {}).get(key, "")
        print(val)
    elif args.config_action == "list":
        for section in cfg.sections():
            print(f"[{section}]")
            for k, v in cfg[section].items():
                if k == "password":
                    v = "****"
                print(f"  {k} = {v}")


# ─── CLI dispatch ──────────────────────────────────────────────────────────

COMMANDS = {
    "login": cmd_login,
    "logout": cmd_logout,
    "me": cmd_me,
    "balance": cmd_balance,
    "statement": cmd_statement,
    "transactions": cmd_transactions,
    "payment": cmd_payment,
    "banks": cmd_banks,
    "draft": cmd_draft,
    "wallet": cmd_wallet,
    "permissions": cmd_permissions,
    "device-info": cmd_device,
    "timeline": cmd_timeline,
    "coupons": cmd_coupons,
    "settings": cmd_settings,
    "client-info": cmd_client_info,
    "config": cmd_config,
}


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="matera",
        description="CLI para API Matera Edge Services",
        epilog="https://doc-api-redoc-mtr.neocities.org/",
    )
    p.add_argument("--token", help="Token (opcional, usa cache)")
    p.add_argument("--json", action="store_true", help="JSON puro")

    sub = p.add_subparsers(dest="command", required=True)

    # login
    x = sub.add_parser("login", help="Autenticar")
    x.add_argument("--username", required=True)
    x.add_argument("--password", required=True)

    sub.add_parser("logout", help="Remover token")
    sub.add_parser("me", help="Dados do usuário")
    sub.add_parser("balance", help="Saldo")

    # statement
    x = sub.add_parser("statement", help="Extrato")
    x.add_argument("--account")

    # transactions
    x = sub.add_parser("transactions", help="Transações")
    x.add_argument("--account")
    x.add_argument("--limit", type=int, default=20)

    # payment
    x = sub.add_parser("payment", help="Pagamento")
    x.add_argument("--amount", type=float, required=True)
    x.add_argument("--description", default="")
    x.add_argument("--type", dest="tx_type", default="boleto",
                   choices=["boleto", "creditCard", "directDebt"])

    # banks
    x = sub.add_parser("banks", help="Bancos")
    x.add_argument("--type", default="ALL")

    # draft
    x = sub.add_parser("draft", help="Saque")
    x.add_argument("--account")
    x.add_argument("--value", type=float, required=True)

    sub.add_parser("wallet", help="Carteira")
    sub.add_parser("permissions", help="Permissões")
    sub.add_parser("device-info", help="Dispositivo")
    sub.add_parser("coupons", help="Cupons")
    sub.add_parser("settings", help="Configs do sistema")
    sub.add_parser("client-info", help="Dados do cliente")

    # timeline
    x = sub.add_parser("timeline", help="Timeline")
    x.add_argument("--account")

    # config
    x = sub.add_parser("config", help="Config")
    cs = x.add_subparsers(dest="config_action", required=True)
    cs_set = cs.add_parser("set", help="Definir")
    cs_set.add_argument("--key", required=True)
    cs_set.add_argument("--value", required=True)
    cs_get = cs.add_parser("get", help="Ler")
    cs_get.add_argument("--key", required=True)
    cs.add_parser("list", help="Listar")

    return p


def main():
    from matera.config import ensure_config
    ensure_config()

    parser = build_parser()
    args = parser.parse_args()

    try:
        if args.command == "config":
            cmd_config(args)
        else:
            COMMANDS[args.command](args)
    except MateraAPIError as e:
        _err(f"HTTP {e.status}: {e.body[:300]}")
        sys.exit(1)
    except Exception as e:
        _err(f"Erro: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()