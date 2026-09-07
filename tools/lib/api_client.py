# -*- coding: utf-8 -*-
"""api_client.py - 通用 BRAIN API 客户端（从 kor_fetch_metrics.py 提取）。"""
import base64
import http.cookiejar
import json
import os
import urllib.request

BASE = "https://api.worldquantbrain.com"


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
