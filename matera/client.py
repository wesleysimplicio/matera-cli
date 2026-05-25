"""HTTP client for Matera API."""

import json
import urllib.error
import urllib.parse
import urllib.request
from typing import Any, Dict, Optional

API_BASE = "https://api_mp.matera.com.br"


class MateraAPIError(Exception):
    def __init__(self, status: int, body: str):
        self.status = status
        self.body = body
        super().__init__(f"[{status}] {body[:200]}")


def api_request(
    method: str,
    path: str,
    token: Optional[str] = None,
    data: Optional[dict] = None,
    params: Optional[dict] = None,
    content_type: str = "application/json",
    extra_headers: Optional[dict] = None,
) -> dict:
    """Faz requisição à API Matera."""
    url = f"{API_BASE}{path}"

    if params:
        qs = urllib.parse.urlencode(params)
        url = f"{url}?{qs}"

    headers = {
        "User-Agent": "matera-cli/1.0",
        "Accept": "application/json",
    }
    if token:
        headers["Authorization"] = token
    if extra_headers:
        headers.update(extra_headers)
    if data is not None:
        headers["Content-Type"] = content_type

    body = None
    if data is not None:
        if content_type == "application/x-www-form-urlencoded":
            body = urllib.parse.urlencode(data).encode()
        else:
            body = json.dumps(data).encode()

    req = urllib.request.Request(url, data=body, headers=headers, method=method)

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            raw = resp.read().decode()
            if raw.strip():
                return json.loads(raw)
            return {}
    except urllib.error.HTTPError as e:
        raw = e.read().decode() if e.fp else ""
        raise MateraAPIError(e.code, raw)
    except urllib.error.URLError as e:
        raise MateraAPIError(0, f"Erro de conexão: {e.reason}")