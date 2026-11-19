#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""向 WorldQuant BRAIN 中文论坛发一篇帖子（HTML 正文）。

凭据仅从 world-quant-brain-mcp/.env 读取（CREDENTIALS_EMAIL / CREDENTIALS_PASSWORD），
不打印、不记录凭据值。发帖成功后打印 status 与 post id。

用法:
  python tools/forum_post.py --title "标题" --body-file body.html --topic-id 12913416465431
  python tools/forum_post.py --probe        # 只读探测：验证认证/会话链路，不发帖

链路（⚠ 2026-11-19 更正：此处原写「复刻现役 MCP BrainApiClient.create_forum_post」——
      **该说法已过期**：MCP 包内已无 create_forum_post 方法，发帖方向 MCP 无对应工具，
      故本脚本是当前唯一发帖实现；它是**登记在册的例外**（不是隐形旁路），见
      docs/reference/forum_and_doc_tools_guide.md 顶部「一处登记在册的例外（写方向）」，
      机械闸 tests/unit/08_forum_recon/test_forum_single_way_gate.py 逐个登记）:
  POST  api.worldquantbrain.com/authentication        (Basic) -> 201, 拿 t cookie
  GET   api.worldquantbrain.com/authentication/support        -> 200, 换 zendesk cookies
  GET   support.worldquantbrain.com/hc/<locale>/community/topics -> 200, bootstrap 会话
  GET   support.worldquantbrain.com/api/v2/help_center/sessions.json -> csrf_token
  POST  support.worldquantbrain.com/api/v2/community/posts.json       -> 201
"""
from __future__ import annotations

import argparse
import base64
import json
import os
import sys
from pathlib import Path

import requests


def _bootstrap():
    for parent in Path(__file__).resolve().parents:
        if (parent / "pyproject.toml").exists() and (parent / "src" / "wqb").is_dir():
            return parent
    raise RuntimeError("仓库根未找到（向上未见 pyproject.toml + src/wqb 双标记）")


REPO = str(_bootstrap())
ENV_PATH = os.path.join(REPO, "world-quant-brain-mcp", ".env")
API = "https://api.worldquantbrain.com"
SUPPORT = "https://support.worldquantbrain.com"
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36")
SSO_ACCESS = (
    "https://worldquantbrain.zendesk.com/access"
    "?brand_id=1500000894061&locale=zh-cn"
    f"&return_to={SUPPORT}/hc/zh-cn"
)


def load_creds():
    creds = {}
    with open(ENV_PATH, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            creds[k.strip()] = v.strip().strip('"').strip("'")
    email = creds.get("CREDENTIALS_EMAIL")
    password = creds.get("CREDENTIALS_PASSWORD")
    if not (email and password):
        raise RuntimeError("credentials missing in .env (CREDENTIALS_EMAIL / CREDENTIALS_PASSWORD)")
    return email, password


def _bootstrap(session: requests.Session) -> str:
    """访问社区页建立 _zendesk_* cookies；优先 zh-cn，退回 en-us。"""
    last = 0
    for loc in ("zh-cn", "en-us"):
        r = session.get(f"{SUPPORT}/hc/{loc}/community/topics", timeout=60)
        last = r.status_code
        if r.status_code == 200:
            return loc
    raise RuntimeError(f"support bootstrap failed: {last}")


def build_session() -> tuple:
    """认证 + 建立 support 会话，返回 (session, csrf_token, locale)。"""
    email, password = load_creds()
    s = requests.Session()
    s.headers.update({"User-Agent": UA})

    enc = base64.b64encode(f"{email}:{password}".encode()).decode()
    r = s.post(f"{API}/authentication", headers={"Authorization": f"Basic {enc}"}, timeout=60)
    if r.status_code == 401:
        raise RuntimeError("auth 401: 该账号可能需要生物识别(persona)二次验证，脚本不处理")
    if r.status_code != 201:
        raise RuntimeError(f"BRAIN auth failed: {r.status_code} {r.text[:160]}")

    # 主路径：JWT exchange；失败则退回现役 forum_functions 用的 zendesk /access SSO
    exchanged = False
    try:
        ex = s.get(f"{API}/authentication/support", timeout=60, allow_redirects=True)
        exchanged = ex.status_code == 200
    except requests.RequestException:
        exchanged = False
    if not exchanged:
        sso = s.get(SSO_ACCESS, timeout=60, allow_redirects=True,
                    headers={"Accept": "text/html,application/xhtml+xml,*/*;q=0.8"})
        if sso.status_code >= 400:
            raise RuntimeError(f"support SSO handshake failed: {sso.status_code}")

    loc = _bootstrap(s)
    csrf = get_csrf(s)
    return s, csrf, loc


def get_csrf(session: requests.Session) -> str:
    r = session.get(f"{SUPPORT}/api/v2/help_center/sessions.json", timeout=60)
    if r.status_code != 200:
        raise RuntimeError(f"sessions lookup failed: {r.status_code} {r.text[:160]}")
    token = (r.json().get("current_session") or {}).get("csrf_token")
    if not token:
        raise RuntimeError("sessions response missing csrf_token")
    return token


def post(session: requests.Session, csrf: str, loc: str, topic_id: int,
         title: str, details: str) -> requests.Response:
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Origin": SUPPORT,
        "Referer": f"{SUPPORT}/hc/{loc}/community/topics",
        "X-CSRF-Token": csrf,
        "X-Requested-With": "XMLHttpRequest",
    }
    payload = {"post": {"topic_id": topic_id, "title": title, "details": details}}
    return session.post(f"{SUPPORT}/api/v2/community/posts.json",
                        json=payload, headers=headers, timeout=60)


def read_body(path: str) -> str:
    candidates = [path]
    if not os.path.isabs(path):
        candidates.append(os.path.join(REPO, path))
    for p in candidates:
        if os.path.exists(p):
            with open(p, encoding="utf-8") as f:
                return f.read()
    raise RuntimeError(f"body file not found: {path}")


def main() -> int:
    ap = argparse.ArgumentParser(description="发一篇 HTML 正文到 WQ BRAIN 中文论坛")
    ap.add_argument("--title")
    ap.add_argument("--body-file")
    ap.add_argument("--topic-id", type=int, default=12913416465431)
    ap.add_argument("--probe", action="store_true", help="只验证会话链路，不发帖")
    a = ap.parse_args()

    try:
        s, csrf, loc = build_session()
    except Exception as e:
        print(f"[forum_post] session failed: {e}", file=sys.stderr)
        print(json.dumps({"status": "session_failed", "error": str(e)}, ensure_ascii=False))
        return 1

    if a.probe:
        print(json.dumps({"status": "probe_ok", "locale": loc,
                          "csrf_acquired": bool(csrf), "cookies": len(s.cookies)},
                         ensure_ascii=False))
        return 0

    if not (a.title and a.body_file):
        print("[forum_post] --title / --body-file required (or use --probe)", file=sys.stderr)
        return 2
    details = read_body(a.body_file)

    # 最多 2 次：403 时刷新 csrf 再试一次
    resp = None
    for attempt in (1, 2):
        resp = post(s, csrf, loc, a.topic_id, a.title, details)
        if resp.status_code == 201:
            break
        if resp.status_code == 403 and attempt == 1:
            csrf = get_csrf(s)
            continue
        break

    status = resp.status_code
    out = {"status": status, "title": a.title, "topic_id": a.topic_id}
    try:
        body = resp.json().get("post") or {}
        out["post_id"] = body.get("id")
        out["post_url"] = body.get("html_url") or body.get("url")
    except Exception:
        out["resp_excerpt"] = resp.text[:200]
    print(json.dumps(out, ensure_ascii=False))
    return 0 if status == 201 else 1


if __name__ == "__main__":
    sys.exit(main())
