"""Config management for Matera CLI."""

import json
import os
from configparser import ConfigParser
from pathlib import Path
from typing import Optional

CONFIG_DIR = Path.home() / ".hermes2" / "scripts" / "matera-cli"
CONFIG_FILE = CONFIG_DIR / "config.ini"
TOKEN_FILE = CONFIG_DIR / "token.json"


def ensure_config():
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    if not CONFIG_FILE.exists():
        cfg = ConfigParser()
        cfg["auth"] = {"username": "", "password": ""}
        cfg["defaults"] = {"account_id": ""}
        with open(CONFIG_FILE, "w") as f:
            cfg.write(f)


def read_config() -> ConfigParser:
    ensure_config()
    cfg = ConfigParser()
    cfg.read(CONFIG_FILE)
    return cfg


def write_config(cfg: ConfigParser):
    ensure_config()
    with open(CONFIG_FILE, "w") as f:
        cfg.write(f)


def save_token(token_data: dict):
    ensure_config()
    token_data["_saved_at"] = __import__("datetime").datetime.now().isoformat()
    with open(TOKEN_FILE, "w") as f:
        json.dump(token_data, f, indent=2)


def load_token() -> Optional[dict]:
    if TOKEN_FILE.exists():
        try:
            with open(TOKEN_FILE) as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError):
            return None
    return None


def clear_token():
    if TOKEN_FILE.exists():
        TOKEN_FILE.unlink()