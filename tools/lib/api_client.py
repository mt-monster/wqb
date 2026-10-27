# -*- coding: utf-8 -*-
"""api_client.py - 通用 BRAIN API 客户端（从 kor_fetch_metrics.py 提取）。"""
import base64
import http.cookiejar
import json
import os
import time
import urllib.error
import urllib.request

BASE = "https://api.worldquantbrain.com"


class PaginationError(RuntimeError):
    """A paginated pull could not be proven complete (all-or-error)."""


def _load_from_mcp_env():
    """从项目 MCP 服务的 .env 读取凭证（CREDENTIALS_EMAIL/PASSWORD）。

    仅按行解析，不打印、不入库、不进 git。作为 ~/.brain_credentials 缺失时的兜底。
    """
    root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    p = os.path.join(root, "world-quant-brain-mcp", ".env")
    if not os.path.exists(p):
        return None, None
    email = pwd = None
    for ln in open(p, encoding="utf-8"):
        ln = ln.strip()
        if not ln or ln.startswith("#") or "=" not in ln:
            continue
        k, v = ln.split("=", 1)
        k, v = k.strip(), v.strip().strip('"').strip("'")
        if k == "CREDENTIALS_EMAIL":
            email = v
        elif k == "CREDENTIALS_PASSWORD":
            pwd = v
    return email, pwd


def load_creds():
    """按优先级发现凭证：~/.brain_credentials → ~/.brain_mcp_config.json → MCP .env。"""
    p = os.path.expanduser("~/.brain_credentials")
    if os.path.exists(p):
        d = json.load(open(p, encoding="utf-8"))
        if isinstance(d, list) and len(d) >= 2:
            return d[0], d[1]
    cfg_path = os.environ.get("MCP_CONFIG_FILE") or os.path.expanduser("~/.brain_mcp_config.json")
    if os.path.exists(cfg_path):
        cfg = json.load(open(cfg_path, encoding="utf-8"))
        c = cfg.get("credentials", {})
        if c.get("email"):
            return c.get("email"), c.get("password")
    return _load_from_mcp_env()


class Api:
    def __init__(self):
        self.jar = http.cookiejar.CookieJar()
        self.op = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(self.jar))

    def post(self, path, payload=None, headers=None):
        data = json.dumps(payload).encode() if payload is not None else None
        h = {"Content-Type": "application/json"}
        if headers:
            h.update(headers)
        req = urllib.request.Request(BASE + path, data=data, headers=h)
        return self.op.open(req, timeout=60)

    def get(self, path):
        req = urllib.request.Request(BASE + path)
        return self.op.open(req, timeout=60)

    def login(self, email, password):
        enc = base64.b64encode(("%s:%s" % (email, password)).encode()).decode()
        req = urllib.request.Request(BASE + "/authentication", data=b"",
                                     headers={"Authorization": "Basic " + enc})
        self.op.open(req, timeout=60)


def _get_json(api, path, retries=5, base_delay=1.0):
    """GET + JSON with bounded retries for 429/5xx/transient/parse failures."""
    delay = base_delay
    last_exc = None
    for attempt in range(retries):
        try:
            with api.get(path) as resp:
                return json.load(resp)
        except urllib.error.HTTPError as e:
            last_exc = e
            if e.code not in (429, 500, 502, 503, 504) or attempt == retries - 1:
                raise
        except (urllib.error.URLError, TimeoutError, ConnectionError,
                json.JSONDecodeError) as e:
            last_exc = e
            if attempt == retries - 1:
                raise
        time.sleep(delay)
        delay = min(delay * 2, 10.0)
    raise last_exc  # pragma: no cover - loop always returns or raises


def paginate_all(api, base, *, limit=50, max_items=None, sleep=0.3,
                 retries=5, strict=True):
    """Fetch every row of a paginated BRAIN list endpoint.

    Pagination contract (verified live 2026-10-20, ``/data-fields``):
    - page size is hard-capped at ``limit=50`` (``limit=100`` -> HTTP 400);
    - ``dataset.id=`` queries paginate to any depth, so the pull is
      all-or-error: ending short of the platform-declared ``count`` raises
      :class:`PaginationError` instead of silently returning a partial catalog
      (the 2026-10-18 analyst7 profile recorded 299/1111 fields this way);
    - ``search=`` queries are window-limited at ``offset+limit <= 100`` and
      their ``count`` is the *unfiltered* total, so a search can only expose
      the first 100 matches. Never build a catalog from a search.

    ``base`` is the full path + query string *without* ``limit`` / ``offset``.
    ``max_items`` is an explicit, caller-owned cap (reported as
    ``truncated_reason="max_items_cap"``), not a silent default.

    Returns ``{"items", "platform_count", "complete", "pages",
    "truncated_reason"}``.
    """
    sep = "" if base.endswith(("?", "&")) else ("&" if "?" in base else "?")
    has_search = "search=" in base
    window = 100 if has_search else None
    cap = max(1, int(max_items)) if max_items else None

    out = []
    seen = set()
    platform_count = None
    pages = 0
    offset = 0
    reached_end = False
    truncated_reason = None

    while True:
        if window is not None and offset >= window:
            truncated_reason = "search_window_capped"
            break
        if cap is not None and len(out) >= cap:
            break
        path = "%s%slimit=%d&offset=%d" % (base, sep, limit, offset)
        try:
            data = _get_json(api, path, retries=retries)
        except urllib.error.HTTPError as e:
            if has_search and e.code == 400 and offset > 0:
                # Platform rejects search pages beyond the 100-result window.
                truncated_reason = "search_window_capped"
                break
            raise
        page = data.get("results") or []
        pages += 1
        if platform_count is None:
            platform_count = data.get("count")

        new_items = 0
        for idx, item in enumerate(page):
            key = item.get("id") if isinstance(item, dict) else None
            key = key or "_anon_%d_%d" % (offset, idx)
            if key in seen:
                continue
            seen.add(key)
            out.append(item)
            new_items += 1

        if len(page) < limit:
            reached_end = True
        if cap is not None and len(out) >= cap:
            if len(out) > cap:
                del out[cap:]
            if platform_count is None or len(out) < platform_count:
                truncated_reason = "max_items_cap"
            break
        if reached_end:
            break
        if window is None and platform_count is not None \
                and len(out) >= platform_count:
            break
        if window is not None and len(out) >= window:
            truncated_reason = "search_window_capped"
            break
        if new_items == 0 and window is None:
            raise PaginationError(
                "pagination made no progress at offset=%d (%d/%s rows) for %r"
                % (offset, len(out), platform_count, base)
            )
        offset += limit
        time.sleep(sleep)

    if window is not None:
        complete = reached_end and not truncated_reason
    elif platform_count is None:
        complete = reached_end and not truncated_reason
    else:
        complete = len(out) >= platform_count

    if strict and not truncated_reason and not complete:
        raise PaginationError(
            "incomplete pull for %r: got %d/%s rows across %d pages"
            % (base, len(out), platform_count, pages)
        )

    return {
        "items": out,
        "platform_count": platform_count,
        "complete": complete,
        "pages": pages,
        "truncated_reason": truncated_reason,
    }
