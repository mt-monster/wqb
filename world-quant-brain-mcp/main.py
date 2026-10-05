#!/usr/bin/env python3
"""main — WorldQuant BRAIN MCP 服务器入口 (2026-08-13 工具层已按域拆分).

结构: brain_api.py (API 客户端) + mcp_core.py (FastMCP 实例/瘦身辅助)
      + tools_*.py (10 个域工具模块, 副作用注册) + 本文件 (组装 + 启动)。
"""
import os, sys

# ---运行环境兜底（2026-10-05，HTTP 模式必备）---------------------------
# stdio 模式下这些 env 由客户端在 `.mcp.json` 里注入；**HTTP 模式下客户端只连
# URL、不再负责起进程**，那些 env 就没人提供了 —— 工具层读不到会静默走默认值
# （例：`WQ_TOOLKIT_DIR` 缺失 → `campaign_intel` 找不到 toolkit 脚本）。
# 故在此按「仓库根上溯 + setdefault」兜底：显式设置仍优先，不覆盖调用方口径。
_REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault("WQ_TOOLKIT_DIR", os.path.join(_REPO_ROOT, "Claude", "skills",
                                                  "wq-brain-campaign-toolkit", "scripts"))
os.environ.setdefault("WQ_VALIDATOR_DIR", os.path.join(_REPO_ROOT, "Claude", "skills",
                                                    "alpha-expression-verifier", "scripts"))
# 提交闸：stdio 模式此前由 .mcp.json 给 "1"。HTTP 模式同样需要，
# 否则 `workflow_submit_alpha` 的 `ALLOW_ALPHA_SUBMIT` 闸会 fail-closed 拦下提交。
# ⚠ 这是「允许提交」的开关，不是「自动提交」—— 真正提交仍需
# confirm_submit=True + 用户明确确认（AGENTS.md §7 提交纪律）。
os.environ.setdefault("WQB_ALLOW_ALPHA_SUBMIT", "1")
# -----------------------------------------------------------------------

import redis

from brain_api import brain_client, load_config
from mcp_core import mcp

# 工具层注册 (副作用: @mcp.tool 装饰器在 import 时完成)
import tools_config    # noqa: F401,E402  manage_config
import tools_labs      # noqa: F401,E402  authenticate_brainlabs/emit/ingest
import tools_account   # noqa: F401,E402  账号/活动/比赛/金字塔/支付
import tools_sim       # noqa: F401,E402  仿真 (单发/批量/诊断)
import tools_alpha     # noqa: F401,E402  Alpha 查询/属性
import tools_data      # noqa: F401,E402  数据集/字段/算子/表达式校验
import tools_submit    # noqa: F401,E402  提交/配额
import tools_corr      # noqa: F401,E402  相关性
import tools_forum     # noqa: F401,E402  论坛/消息
import tools_spc       # noqa: F401,E402  SPC
import tools_workflow  # noqa: F401,E402  Workflow 引擎节点
import tools_ops      # noqa: F401,E402  运维/审计（operator_audit/batch_status/submit_verdict/sa_probe/submit_batch）

# --- Main entry point ---
if __name__ == "__main__":
    print("running the server", file=sys.stderr)
    
    # Validate critical environment setup
    config = load_config()
    creds = config.get("credentials", {})
    if not creds.get("email") or not creds.get("password"):
        print("[WARNING] No BRAIN credentials found in config. Authentication will fail until credentials are provided.", file=sys.stderr)
    
    # Verify Redis connectivity
    if brain_client.redis_client:
        print("[INFO] Redis connection established successfully", file=sys.stderr)
    else:
        # 2026-09-01 降噪：Redis 为可选缓存，不可用时 INFO 一行即可（见 brain_mixin_transport）
        print("[INFO] Redis not available - caching disabled (optional)", file=sys.stderr)

    # Run using configured transport:
    #   MCP_TRANSPORT=streamable-http -> HTTP server (DEFAULT now)
    #   MCP_TRANSPORT=stdio           -> stdio (legacy / IDE auto-start)
    #   Default: streamable-http (HTTP server on MCP_HOST:MCP_PORT = 0.0.0.0:8000)
    # 2026-08-13 fix: mcp.run() MUST stay inside this guard — forum_functions.py
    # does `from brain_api import brain_client` from within a running event loop,
    # and a module-level mcp.run() re-enters anyio.run → "Already running
    # asyncio in this thread" (forum search/read were completely broken).
    transport = os.environ.get("MCP_TRANSPORT", "streamable-http")
    if transport == "streamable-http":
        # 显式传 host/port：FastMCP(settings) 在构造时定下，改 env 已太晚。
        # wq-brain-http 用 8000；wqb-db 用 8001（见 wqb_db_mcp.py 的 MCP_PORT）。
        _host = os.environ.get("MCP_HOST", "127.0.0.1")
        _port = int(os.environ.get("MCP_PORT", "8000"))
        try:
            mcp.settings.host = _host
            mcp.settings.port = _port
        except Exception as e:  # noqa: BLE001 — 不因改端口起不来
            print(f"[WARN] 设置 host/port 失败，用默认监听：{e}", file=sys.stderr)
    try:
        mcp.run(transport=transport)
    except TypeError:
        # Fallback if signature differs
        mcp.run(transport)
