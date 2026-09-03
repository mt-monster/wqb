# -*- coding: utf-8 -*-
"""mcp_ping.py - MCP 服务连通性与调用时长测试工具（2026-09-01）。

对 .mcp.json 注册的 MCP 服务做端到端体检：
  1. 服务启动（stdio 子进程）+ initialize 握手 + tools/list —— 测服务可用性与工具数；
  2. 逐个调用预置的【只读探针】工具 —— 测真实调用时长（P50 不适用单次，给单次毫秒）；
  3. 可选 --full：对服务注册的全部工具做 tools/list schema 抽取（不调用，只验证注册完整性）。

探针原则：只选无副作用的只读工具（不消耗回测/提交配额，不写库）。

用法：
  python tools/mcp_ping.py                          # 全部服务 + 默认探针
  python tools/mcp_ping.py --service wqb-db         # 单服务
  python tools/mcp_ping.py --full                   # 含全工具注册完整性检查
  python tools/mcp_ping.py --timeout 30             # 握手超时（秒）
输出：人读表格 + 退出码（0=全部通过，1=有失败，2=配置错误）
"""
import argparse
import json
import os
import subprocess
import sys
import time
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
MCP_CONFIG = REPO_ROOT / ".mcp.json"

# 只读探针（无副作用）：service -> [(tool, args)]
PROBES = {
    "wq-brain-http": [
        ("get_operators", {}),
        ("get_documentations", {}),
        ("value_factor_trendScore", {"start_date": "2026-08-01", "end_date": "2026-09-01"}),
    ],
    "wqb-db": [
        ("get_region_overview", {}),
        ("get_cross_region_lessons", {}),
        ("get_dead_ends", {"region": "EUR"}),
        ("get_ledger_key", {"region": "EUR", "key": "s0_whitelist"}),
    ],
}


class McpStdioClient:
    """极简 MCP stdio 客户端：JSON-RPC over 子进程 stdin/stdout。"""

    def __init__(self, command, args, env, timeout=30):
        self.timeout = timeout
        self.proc = None
        self._id = 0
        full_env = {**os.environ, **(env or {})}
        self.proc = subprocess.Popen(
            [command] + list(args),
            stdin=subprocess.PIPE, stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,  # 日志走 stderr，避免污染协议流
            env=full_env, cwd=str(REPO_ROOT),
        )

    def _send(self, method, params=None, timeout=None):
        self._id += 1
        req = {"jsonrpc": "2.0", "id": self._id, "method": method,
               "params": params or {}}
        self.proc.stdin.write((json.dumps(req) + "\n").encode("utf-8"))
        self.proc.stdin.flush()
        deadline = time.time() + (timeout or self.timeout)
        # 逐行读 stdout 找到匹配 id 的响应（服务可能插发 notification，跳过）
        while time.time() < deadline:
            line = self.proc.stdout.readline()
            if not line:
                raise ConnectionError("stdout 关闭（服务进程退出）")
            line = line.strip()
            if not line:
                continue
            try:
                resp = json.loads(line)
            except json.JSONDecodeError:
                continue
            if resp.get("id") == self._id:
                return resp
        raise TimeoutError(f"等待 {method} 响应超时")

    def initialize(self):
        """MCP initialize 握手（protocolVersion 用 2024-11-05，兼容主流实现）。"""
        r = self._send("initialize", {
            "protocolVersion": "2024-11-05",
            "capabilities": {},
            "clientInfo": {"name": "mcp_ping", "version": "1.0"},
        })
        if "error" in r:
            raise RuntimeError(f"initialize 失败: {r['error']}")
        # initialized notification（单向，不期待响应）
        self.proc.stdin.write((json.dumps({
            "jsonrpc": "2.0", "method": "notifications/initialized", "params": {}
        }) + "\n").encode("utf-8"))
        self.proc.stdin.flush()
        return r.get("result", {})

    def list_tools(self):
        r = self._send("tools/list", {})
        if "error" in r:
            raise RuntimeError(f"tools/list 失败: {r['error']}")
        return r.get("result", {}).get("tools", [])

    def call_tool(self, name, args):
        t0 = time.perf_counter()
        r = self._send("tools/call", {"name": name, "arguments": args})
        ms = (time.perf_counter() - t0) * 1000
        if "error" in r:
            return False, ms, str(r["error"].get("message", r["error"]))[:120]
        result = r.get("result", {})
        # MCP tool 错误约定：result.isError = true
        if result.get("isError"):
            text = ""
            for c in result.get("content", []):
                if isinstance(c, dict) and c.get("type") == "text":
                    text = c.get("text", "")[:120]
                    break
            return False, ms, text or "tool returned isError"
        return True, ms, None

    def close(self):
        try:
            if self.proc and self.proc.poll() is None:
                self.proc.terminate()
                try:
                    self.proc.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    self.proc.kill()
        except Exception:
            pass


def load_services():
    if not MCP_CONFIG.is_file():
        print(f"[error] 未找到 {MCP_CONFIG}")
        sys.exit(2)
    cfg = json.loads(MCP_CONFIG.read_text(encoding="utf-8"))
    return cfg.get("mcpServers", {})


def main():
    ap = argparse.ArgumentParser(description="MCP 连通性与调用时长测试")
    ap.add_argument("--service", help="只测指定服务（缺省全部）")
    ap.add_argument("--full", action="store_true", help="附全工具注册完整性检查（tools/list 全量）")
    ap.add_argument("--timeout", type=int, default=30, help="握手/调用超时秒数（默认 30）")
    a = ap.parse_args()

    services = load_services()
    if a.service:
        if a.service not in services:
            print(f"[error] 服务 {a.service} 不在 .mcp.json（可用: {sorted(services)}）")
            sys.exit(2)
        services = {a.service: services[a.service]}

    all_ok = True
    summary = []
    for name, spec in services.items():
        print(f"\n══ {name} ══")
        cmd = spec.get("command")
        if not cmd or not Path(cmd).is_file():
            print(f"  [SKIP] 命令不存在: {cmd}")
            all_ok = False
            summary.append((name, "SKIP", "command not found"))
            continue
        client = None
        try:
            t0 = time.perf_counter()
            client = McpStdioClient(cmd, spec.get("args", []), spec.get("env"), a.timeout)
            info = client.initialize()
            init_ms = (time.perf_counter() - t0) * 1000
            server = info.get("serverInfo", {})
            print(f"  [OK] 握手 {init_ms:.0f}ms  server={server.get('name','?')} v{server.get('version','?')}")

            tools = client.list_tools()
            print(f"  [OK] tools/list {len(tools)} 个工具")

            if a.full:
                names = sorted(t.get("name", "?") for t in tools)
                print(f"       工具清单: {', '.join(names)}")

            for tool, args in PROBES.get(name, []):
                if tool not in {t.get("name") for t in tools}:
                    print(f"  [SKIP] {tool}: 未注册（探针不适用）")
                    continue
                ok, ms, err = client.call_tool(tool, args)
                mark = "OK  " if ok else "FAIL"
                print(f"  [{mark}] {tool}: {ms:7.0f}ms" + (f"  {err}" if err else ""))
                if not ok:
                    all_ok = False
            summary.append((name, "OK", f"init {init_ms:.0f}ms / {len(tools)} tools"))
        except Exception as e:
            print(f"  [FAIL] {type(e).__name__}: {str(e)[:160]}")
            all_ok = False
            summary.append((name, "FAIL", str(e)[:80]))
        finally:
            if client:
                client.close()

    print("\n══ 汇总 ══")
    for name, status, note in summary:
        print(f"  {name:16s} {status:5s} {note}")
    print(f"\n结论: {'全部通过' if all_ok else '存在失败项'}")
    sys.exit(0 if all_ok else 1)


if __name__ == "__main__":
    main()
