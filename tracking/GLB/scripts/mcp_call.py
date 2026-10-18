#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""mcp_call.py — 最小 MCP streamable-HTTP 客户端（复用已运行的 wq-brain MCP 服务，免凭据）。

用法:
    python mcp_call.py get_datafields '{"region":"GLB","universe":"MINVOL1M","dataset_id":"intraday_pv_feats","delay":1}'
    python mcp_call.py get_datasets '{"region":"GLB","universe":"TOPDIV3000","delay":1}'
输出: JSON 结果到 stdout（可重定向到文件）。
"""
from __future__ import annotations
import json
import sys
import urllib.request
import urllib.error

BASE = "http://127.0.0.1:8000/mcp"


def _post(session_id: str | None, payload: dict) -> tuple[int, dict, str]:
    body = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(BASE, data=body, method="POST")
    req.add_header("Content-Type", "application/json")
    req.add_header("Accept", "application/json, text/event-stream")
    if session_id:
        req.add_header("mcp-session-id", session_id)
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            raw = resp.read().decode("utf-8", "replace")
            sid = resp.headers.get("mcp-session-id") or session_id
            return resp.status, {"sid": sid}, raw
    except urllib.error.HTTPError as e:
        raw = e.read().decode("utf-8", "replace")
        sid = e.headers.get("mcp-session-id") if e.headers else None
        return e.code, {"sid": sid or session_id}, raw


def _parse(raw: str) -> dict:
    raw = raw.strip()
    if not raw:
        return {}
    if raw.startswith("event:") or raw.startswith("data:"):
        # SSE: 取最后一个 data: 行的 JSON
        data_lines = [l[5:].strip() for l in raw.splitlines() if l.startswith("data:")]
        for d in reversed(data_lines):
            try:
                return json.loads(d)
            except Exception:
                continue
        return {}
    try:
        return json.loads(raw)
    except Exception:
        return {"_raw": raw[:2000]}


def call(tool: str, args: dict, port: int = 8000) -> dict:
    global BASE
    BASE = f"http://127.0.0.1:{port}/mcp"
    st, meta, raw = _post(None, {
        "jsonrpc": "2.0", "id": 1, "method": "initialize",
        "params": {"protocolVersion": "2024-11-05", "capabilities": {},
                   "clientInfo": {"name": "mcp_call", "version": "1.0"}}})
    sid = meta.get("sid")
    _post(sid, {"jsonrpc": "2.0", "method": "notifications/initialized"})
    st2, _, raw2 = _post(sid, {
        "jsonrpc": "2.0", "id": 2, "method": "tools/call",
        "params": {"name": tool, "arguments": args}})
    out = _parse(raw2)
    if "error" in out:
        return {"_error": out["error"]}
    res = out.get("result", {})
    # tools/call 结果: {"content":[{"type":"text","text":"..."}], "isError":bool}
    texts = [c.get("text", "") for c in res.get("content", []) if c.get("type") == "text"]
    blob = "\n".join(texts)
    try:
        return json.loads(blob)
    except Exception:
        return {"_raw": blob[:5000], "_isError": res.get("isError")}


if __name__ == "__main__":
    tool = sys.argv[1]
    args = json.loads(sys.argv[2]) if len(sys.argv) > 2 else {}
    port = int(sys.argv[3]) if len(sys.argv) > 3 else 8000
    print(json.dumps(call(tool, args, port), ensure_ascii=False))
