"""通过本地 MCP HTTP 端点跑一次提交预检（MCP 客户端故障时的兜底通道）。

用途：WorkBuddy 侧的 MCP 客户端连接损坏（`fetch failed`）、但 8000 端口服务仍在运行时，
用标准库直接走 Streamable HTTP 协议完成 `initialize → initialized → tools/call`。
只用 urllib，不依赖 requests / pydantic（本机 venv 缺这两个包，`_get_brain_client()` 起不来）。

**只读预检**：默认强制 `confirm_submit=False`，不会 POST 提交、不改属性。

用法：
    python tools/gates/mcp_preflight_once.py 786wl6b8
    python tools/gates/mcp_preflight_once.py 786wl6b8 --port 8000 --json

注意：MCP 服务每次重启会清空所有 session（`Session not found`），故本脚本在
**一次进程内**连续完成握手与调用，避免中间被重启窗口打断。
"""
from __future__ import annotations

import argparse
import json
import sys
import urllib.error
import urllib.request

PROTO = "2024-11-05"


def _post(url: str, payload: dict, sid: str | None = None, timeout: int = 280):
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, method="POST")
    req.add_header("Content-Type", "application/json")
    req.add_header("Accept", "application/json, text/event-stream")
    if sid:
        req.add_header("Mcp-Session-Id", sid)
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        body = resp.read().decode("utf-8", "replace")
        return resp.headers.get("mcp-session-id"), body


def _parse_sse(body: str):
    """取最后一条 data: 行解析成 dict（Streamable HTTP 每帧一个 event）。"""
    out = None
    for line in body.splitlines():
        line = line.strip()
        if not line.startswith("data:"):
            continue
        try:
            out = json.loads(line[5:].strip())
        except json.JSONDecodeError:
            continue
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("alpha_id")
    ap.add_argument("--port", type=int, default=8000)
    ap.add_argument("--json", action="store_true", help="输出完整 JSON")
    ap.add_argument("--confirm", action="store_true",
                    help="危险：真正提交。默认只预检")
    args = ap.parse_args()

    url = f"http://127.0.0.1:{args.port}/mcp"
    try:
        sid, body = _post(url, {
            "jsonrpc": "2.0", "id": 1, "method": "initialize",
            "params": {"protocolVersion": PROTO, "capabilities": {},
                       "clientInfo": {"name": "preflight", "version": "1"}},
        }, timeout=30)
    except urllib.error.URLError as e:
        print(f"[fail] 连不上 MCP {url}：{e}", file=sys.stderr)
        return 2
    if not sid:
        print("[fail] 未取到 mcp-session-id", file=sys.stderr)
        return 2

    _post(url, {"jsonrpc": "2.0", "method": "notifications/initialized"}, sid=sid, timeout=20)

    try:
        _, body = _post(url, {
            "jsonrpc": "2.0", "id": 2, "method": "tools/call",
            "params": {"name": "workflow_execute", "arguments": {
                "node": "submit_alpha",
                "params": {"alpha_id": args.alpha_id,
                           "confirm_submit": bool(args.confirm)},
            }},
        }, sid=sid)
    except urllib.error.URLError as e:
        print(f"[fail] 调用失败：{e}", file=sys.stderr)
        return 2

    msg = _parse_sse(body)
    if not msg:
        print("[fail] 无法解析响应", file=sys.stderr)
        return 2
    res = msg.get("result") or {}
    if res.get("isError"):
        print("[tool error] " + json.dumps(res, ensure_ascii=False)[:600], file=sys.stderr)
        return 1
    content = res.get("structuredContent") or {}
    if not content:
        text = ((res.get("content") or [{}])[0] or {}).get("text") or "{}"
        try:
            content = json.loads(text)
        except json.JSONDecodeError:
            content = {"raw": text[:800]}
    out = content.get("output") or content
    # 兼容两种包装：{"output": {...}} 与 {"result": {"output": {...}}}
    if isinstance(out, dict) and isinstance(out.get("result"), dict):
        out = out["result"].get("output") or out["result"]

    if args.json:
        print(json.dumps(out, ensure_ascii=False, indent=2))
        return 0

    print(f"alpha={out.get('alpha_id')} success={out.get('success')} "
          f"blocked={out.get('blocked')} status={out.get('final_status')}")
    if out.get("reason"):
        print(f"reason: {out['reason']}")
    for s in out.get("steps") or []:
        step = s.get("step")
        if step == "mix_audit":
            print(f"  mix_audit      kind={s.get('kind')} legs={s.get('legs')} "
                  f"path={s.get('path')} blocked={s.get('blocked')}")
        elif step == "marginal_contribution":
            d = (s.get("delta") or {}).get("sharpe")
            print(f"  marginal       available={s.get('available')} partition={s.get('partition')} "
                  f"dSharpe={d if d is None else round(d, 4)}")
        elif step == "diversity_audit":
            print(f"  diversity      level={s.get('level')} self={s.get('self_corr')} "
                  f"source={s.get('self_source')} dS={s.get('delta_sharpe')} "
                  f"blocked={s.get('blocked')}")
            if s.get("note"):
                print(f"                 {s['note']}")
    if out.get("diversity_warning"):
        print("  [warn] " + str(out["diversity_warning"].get("note")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
