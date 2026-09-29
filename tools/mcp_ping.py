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
  python tools/mcp_ping.py --timeout 30             # 每次请求等待上限（秒）
输出：人读表格或完整 JSON；0=通过，1=失败，2=参数错误或显式调用超时。
显式调用超时携带 outcome_unknown / retry_safe=false；先查任务及 DB，禁止自动重发。
"""
import argparse
import json
import os
import queue
import subprocess
import sys
import threading
import time
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))
import _pyenv  # noqa: E402  ${VAR:-default} 展开（tools/_pyenv.py）

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


class McpCallTimeout(TimeoutError):
    """No response is not proof that a dispatched tool did not execute."""

    def __init__(self, method, request_id, tool=None):
        self.method, self.request_id, self.tool = method, request_id, tool
        self.outcome_unknown = method == "tools/call"
        super().__init__(f"等待 {method} 响应超时；连接不可复用，先核对任务/数据库再决定重试")


class McpStdioClient:
    """极简 MCP stdio 客户端：JSON-RPC over 子进程 stdin/stdout。"""

    def __init__(self, command, args, env, timeout=30):
        self.timeout = timeout
        self.proc = None
        self._id = 0
        self._timed_out = False
        full_env = {**os.environ, **(env or {})}
        self.proc = subprocess.Popen(
            [command] + list(args),
            stdin=subprocess.PIPE, stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,  # 日志走 stderr，避免污染协议流
            env=full_env, cwd=str(REPO_ROOT),
        )

    def _send(self, method, params=None, timeout=None):
        if self._timed_out:
            raise RuntimeError("MCP connection timed out; reconcile the previous request before retrying")
        self._id += 1
        req = {"jsonrpc": "2.0", "id": self._id, "method": method,
               "params": params or {}}
        replies = queue.Queue(maxsize=1)

        def exchange():
            # Pipe write/flush and readline can both block. Bound the entire
            # exchange from the caller; a timed-out connection is never reused.
            try:
                self.proc.stdin.write((json.dumps(req) + "\n").encode("utf-8"))
                self.proc.stdin.flush()
                while True:
                    line = self.proc.stdout.readline()
                    if not line:
                        raise ConnectionError("stdout 关闭（服务进程退出）")
                    try:
                        resp = json.loads(line)
                    except (ValueError, UnicodeError):
                        continue
                    if isinstance(resp, dict) and resp.get("id") == req["id"]:
                        replies.put((True, resp))
                        return
            except Exception as exc:
                replies.put((False, exc))

        threading.Thread(target=exchange, daemon=True, name="mcp-exchange").start()
        try:
            ok, value = replies.get(timeout=self.timeout if timeout is None else timeout)
        except queue.Empty:
            self._timed_out = True
            raise McpCallTimeout(method, req["id"], (params or {}).get("name")) from None
        if not ok:
            raise value
        return value

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
                    self.proc.wait(timeout=5)
        except Exception:
            pass


def load_services():
    if not MCP_CONFIG.is_file():
        print(f"[error] 未找到 {MCP_CONFIG}")
        sys.exit(2)
    cfg = json.loads(MCP_CONFIG.read_text(encoding="utf-8"))
    # .mcp.json 用 ${VAR:-default} 做跨平台（2026-09-29）：与 Claude Code 同语法展开
    return _pyenv.expand_env(cfg.get("mcpServers", {}))


def run_calls(spec, calls, timeout=30):
    """Execute explicit MCP calls over one connection; return full results."""
    client = McpStdioClient(spec["command"], spec.get("args", []), spec.get("env"), timeout)
    try:
        client.initialize()
        registered = {item["name"] for item in client.list_tools()}
        if any(call["tool"] not in registered for call in calls):
            raise ValueError("Unregistered tool in call list")
        failed = False
        for call in calls:
            response = client._send("tools/call", {
                "name": call["tool"], "arguments": call.get("args", {})})
            result = response.get("result", {})
            failed = failed or "error" in response or bool(result.get("isError"))
            print(json.dumps({"tool": call["tool"], "result": result,
                              **({"error": response["error"]} if "error" in response else {})},
                             ensure_ascii=False), flush=True)
        return 1 if failed else 0
    except McpCallTimeout as exc:
        print(json.dumps({"error": str(exc), "method": exc.method,
                          "tool": exc.tool, "request_id": exc.request_id,
                          "outcome_unknown": exc.outcome_unknown,
                          "retry_safe": False}, ensure_ascii=False), flush=True)
        return 2
    finally:
        client.close()


def main():
    ap = argparse.ArgumentParser(description="MCP 连通性与调用时长测试")
    ap.add_argument("--service", help="只测指定服务（缺省全部）")
    ap.add_argument("--full", action="store_true", help="附全工具注册完整性检查（tools/list 全量）")
    ap.add_argument("--timeout", type=int, default=30, help="握手/调用超时秒数（默认 30）")
    call_group = ap.add_mutually_exclusive_group()
    call_group.add_argument("--call", help="调用单个工具，完整 JSON 结果写 stdout；须指定 --service")
    call_group.add_argument("--calls-file", help="UTF-8 JSON 列表 [{tool,args}]；复用同一 MCP 连接")
    ap.add_argument("--args-file", help="--call 的 UTF-8 JSON 参数对象（缺省 {}）")
    a = ap.parse_args()

    calls = None
    if a.call or a.calls_file:
        if not a.service:
            ap.error("调用工具必须指定 --service")
        try:
            if a.calls_file:
                if a.args_file:
                    ap.error("--args-file 仅能与 --call 搭配")
                calls = json.loads(Path(a.calls_file).read_text(encoding="utf-8-sig"))
            else:
                args = json.loads(Path(a.args_file).read_text(encoding="utf-8-sig")) if a.args_file else {}
                calls = [{"tool": a.call, "args": args}]
            if not isinstance(calls, list) or not calls or any(
                not isinstance(c, dict) or not isinstance(c.get("tool"), str)
                or not isinstance(c.get("args", {}), dict) for c in calls
            ):
                raise ValueError("Expected a nonempty list of {tool: string, args: object}")
        except (OSError, ValueError) as exc:
            ap.error(str(exc))
    elif a.args_file:
        ap.error("--args-file 需要 --call")

    services = load_services()
    if a.service:
        if a.service not in services:
            print(f"[error] 服务 {a.service} 不在 .mcp.json（可用: {sorted(services)}）")
            sys.exit(2)
        services = {a.service: services[a.service]}

    if calls is not None:
        try:
            sys.exit(run_calls(services[a.service], calls, a.timeout))
        except Exception as exc:
            print(json.dumps({"error": str(exc)}, ensure_ascii=False))
            sys.exit(1)

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
