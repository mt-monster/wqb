#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""mcp_http_caller.py — 直连 HTTP MCP 服务，手工调用**单个工具**（session 管理 + SSE 解析）。

来历（2026-10-14 布局审计，`reports/project_layout_audit_20261014.md` §2 C-3）：
原名 `tools/mcp_py`，**没有扩展名**。缺 `.py` 让它对所有 `*.py` 取面的闸门完全隐形 ——
S4（硬编码盘符）扫不到它、S14（CLI 必须登记 tools/README.md）扫不到它，于是它同时带着
一处 `D:\\...\\wqb-share-03` 绝对路径和一个已不存在的 `127.0.0.1:8876` 端点长期躺在顶层，
默认即坏、无人知。本轮补扩展名并拆掉这两处硬编码：

  - 服务地址：默认从仓库根 `.mcp.json` 按 `--service` 解析（`wq-brain-http` / `wqb-db`），
    不再硬编码端口；仍可用 `--uri` 或 `WQB_MCP_URI` 覆盖；
  - session 文件：默认落 `cache/_mcp_http_caller_session`（gitignore 运行期区），
    可用 `--session-file` 或 `WQB_MCP_SESSION_FILE` 覆盖。

与 `tools/mcp_ping.py` 的分工：ping 是**连通性体检**（多服务 × 只读探针 × 时长 × 退出码语义）；
本脚本是**单工具直调**，用于 MCP 客户端侧不可用、或要绕开 Agent 参数包装时手工发一次请求。

用法：
  python tools/mcp_http_caller.py --service wqb-db list_ledger_keys '{}'
  python tools/mcp_http_caller.py --service wq-brain-http get_events @args.json   # §5 引号规避：文件通道
  python tools/mcp_http_caller.py --list-tools                                    # 只看工具注册面
  python tools/mcp_http_caller.py --uri http://127.0.0.1:8001/mcp <tool> <json>
退出码：0 成功 / 1 调用失败或服务不可达 / 2 参数错误。

⚠ **只用来调只读工具**。回测与提交类动作请走 MCP 工具链（那里有 waiver 台账与用户确认闸），
别用本脚本硬发——它不理解任何业务闸。
"""
import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path


def _bootstrap_src() -> None:
    """把 `src/` 放上 sys.path：向上探测双标记，**与文件层数无关**
    （AGENTS.md §8.13 禁止新增 `parents[N]` / `dirname(dirname())` 这类层数硬编码）。
    """
    for parent in Path(__file__).resolve().parents:
        if (parent / "pyproject.toml").exists() and (parent / "src" / "wqb").is_dir():
            src = str(parent / "src")
            if src not in sys.path:
                sys.path.insert(0, src)
            return
    raise RuntimeError("仓库根未找到（向上未见 pyproject.toml + src/wqb 双标记）")


_bootstrap_src()
from wqb.paths import find_repo_root  # noqa: E402

REPO_ROOT = find_repo_root(__file__)
PROTOCOL_VERSION = "2024-11-05"


def service_uri(service: str) -> str:
    """从 `.mcp.json` 取该 server 的 HTTP url（唯一权威源，AGENTS.md §8.3）。"""
    cfg = REPO_ROOT / ".mcp.json"
    if not cfg.is_file():
        raise SystemExit(f"2 仓库根 .mcp.json 不存在：{cfg}")
    servers = json.loads(cfg.read_text(encoding="utf-8")).get("mcpServers", {})
    entry = servers.get(service)
    if not entry:
        raise SystemExit(f"2 .mcp.json 里没有 server「{service}」（可选：{', '.join(sorted(servers))}）")
    url = entry.get("url")
    if not url:
        raise SystemExit(f"2 server「{service}」不是 HTTP 形态（无 url，stdio 遗留？）：{entry}")
    return url


class McpHttpClient:
    """最小 streamable-HTTP MCP 客户端：initialize → notifications/initialized → tools/call。

    session id 落盘复用（同一服务反复调用不必每次握手）；HTTPError 视为 session 失效，
    重握手一次再重试（与改名前的行为一致）。
    """

    def __init__(self, uri: str, session_file: Path, timeout: int = 1800):
        self.uri = uri
        self.session_file = Path(session_file)
        self.timeout = timeout

    # ---- 传输 ----
    def _post(self, payload: dict, sid: str | None = None, expect_body: bool = True):
        body = json.dumps(payload).encode()
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json, text/event-stream",
        }
        if sid:
            headers["mcp-session-id"] = sid
        req = urllib.request.Request(self.uri, data=body, headers=headers)
        resp = urllib.request.urlopen(req, timeout=self.timeout)
        return resp if expect_body else None

    # ---- session ----
    def new_session(self) -> str:
        resp = self._post({
            "jsonrpc": "2.0", "id": 1, "method": "initialize",
            "params": {
                "protocolVersion": PROTOCOL_VERSION,
                "capabilities": {},
                "clientInfo": {"name": "mcp_http_caller", "version": "1.0"},
            },
        })
        sid = resp.headers.get("mcp-session-id")
        if not sid:
            raise RuntimeError("响应头里没有 mcp-session-id（服务是否以 streamable-http 启动？）")
        try:
            self._post({"jsonrpc": "2.0", "method": "notifications/initialized"}, sid=sid)
        except Exception:
            pass  # 通知类失败不致命，与改名前一致
        self.session_file.parent.mkdir(parents=True, exist_ok=True)
        self.session_file.write_text(sid, encoding="utf-8")
        return sid

    def session(self) -> str:
        try:
            sid = self.session_file.read_text(encoding="utf-8").strip()
            return sid or self.new_session()
        except OSError:
            return self.new_session()

    # ---- 解析：SSE 里取最后一个 data: 帧 ----
    @staticmethod
    def parse(content: str) -> dict | None:
        result = None
        for line in content.splitlines():
            if line.startswith("data: "):
                try:
                    result = json.loads(line[6:])
                except json.JSONDecodeError:
                    continue
        return result

    # ---- 调用 ----
    def list_tools(self) -> list:
        resp = self._post({"jsonrpc": "2.0", "id": 2, "method": "tools/list"}, sid=self.session())
        payload = self.parse(resp.read().decode()) or {}
        return payload.get("result", {}).get("tools", [])

    def call_tool(self, tool_name: str, arguments: dict):
        payload_req = {"jsonrpc": "2.0", "id": 999, "method": "tools/call",
                       "params": {"name": tool_name, "arguments": arguments}}
        sid = self.session()
        try:
            resp = self._post(payload_req, sid=sid)
        except urllib.error.HTTPError:
            sid = self.new_session()          # session 陈旧：重握手后重试一次
            resp = self._post(payload_req, sid=sid)
        payload = self.parse(resp.read().decode())
        if payload is None:
            return {"error": "响应里没有可解析的 data: 帧"}
        if "error" in payload:
            return {"error": payload["error"]}
        res = payload.get("result", {})
        text = "".join(c.get("text", "") for c in res.get("content", []))
        if res.get("isError"):
            return {"error": text}
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            return {"raw": text}


def resolve_args(raw: str | None) -> dict:
    """参数通道：JSON 字面量，或 `@path.json` 文件（AGENTS.md §5 规约 2，根治引号三层嵌套）。"""
    if not raw:
        return {}
    if raw.startswith("@"):
        p = Path(raw[1:])
        if not p.is_file():
            raise SystemExit(f"2 参数文件不存在：{p}")
        return json.loads(p.read_text(encoding="utf-8"))
    return json.loads(raw)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="直连 HTTP MCP 服务调用单个工具（只读用途）")
    ap.add_argument("tool", nargs="?", help="工具名（--list-tools 时可省）")
    ap.add_argument("arguments", nargs="?", default="{}",
                    help="JSON 字面量，或 @path.json 文件通道")
    ap.add_argument("--service", default="wqb-db",
                    help="`.mcp.json` 里的 server 名（默认 wqb-db；优先级低于 --uri）")
    ap.add_argument("--uri", default=os.environ.get("WQB_MCP_URI"),
                    help="直接指定端点，覆盖 --service（env WQB_MCP_URI）")
    ap.add_argument("--session-file", default=os.environ.get("WQB_MCP_SESSION_FILE"),
                    help="session id 落盘位（默认 cache/_mcp_http_caller_session；env WQB_MCP_SESSION_FILE）")
    ap.add_argument("--timeout", type=int, default=1800, help="单次请求等待上限（秒）")
    ap.add_argument("--new-session", action="store_true", help="丢弃已存 session，强制重新握手")
    ap.add_argument("--list-tools", action="store_true", help="只列已注册工具（名字 + 描述首行）")
    ns = ap.parse_args(argv)

    uri = ns.uri or service_uri(ns.service)
    sess = Path(ns.session_file) if ns.session_file else REPO_ROOT / "cache" / "_mcp_http_caller_session"
    client = McpHttpClient(uri, sess, timeout=ns.timeout)
    if ns.new_session:
        try:
            sid = client.new_session()
        except Exception as exc:
            print(f"1 握手失败：{exc}（服务没起？先 python tools/start_wq_mcp.py --all）")
            return 1
        print(f"[session] {sid} → {sess}")
        if not ns.tool and not ns.list_tools:
            return 0

    try:
        if ns.list_tools:
            tools = client.list_tools()
            for t in tools:
                desc = (t.get("description") or "").strip().splitlines()
                print(f"{t.get('name')}  —  {desc[0] if desc else ''}")
            print(f"\n[{uri}] 共 {len(tools)} 个工具")
            return 0 if tools else 1
        if not ns.tool:
            print("2 需要给工具名（或用 --list-tools）")
            return 2
        out = client.call_tool(ns.tool, resolve_args(ns.arguments))
        print(json.dumps(out, ensure_ascii=False, indent=1, default=str))
        return 1 if isinstance(out, dict) and "error" in out else 0
    except urllib.error.HTTPError as exc:
        print(f"1 HTTP {exc.code}：{exc.reason}（读一下 body 里的 detail）\n{exc.read().decode(errors='replace')[:400]}")
        return 1
    except Exception as exc:
        print(f"1 调用失败：{type(exc).__name__}: {exc}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
