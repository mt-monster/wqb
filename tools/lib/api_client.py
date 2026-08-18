# -*- coding: utf-8 -*-
"""api_client.py - 通用 BRAIN API 客户端（从 kor_fetch_metrics.py 提取）。"""
import base64
import http.cookiejar
import json
import os
import urllib.request

BASE = "https://api.worldquantbrain.com"


def load_creds():
    p = os.path.expanduser("~/.brain_credentials")
    d = json.load(open(p, encoding="utf-8"))
    if isinstance(d, list) and len(d) >= 2:
        return d[0], d[1]
    cfg = json.load(open(os.environ.get("MCP_CONFIG_FILE") or os.path.expanduser("~/.brain_mcp_config.json"), encoding="utf-8"))
    c = cfg.get("credentials", {})
    return c.get("email"), c.get("password")


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
