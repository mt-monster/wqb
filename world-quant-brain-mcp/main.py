#!/usr/bin/env python3
"""main — WorldQuant BRAIN MCP 服务器入口 (2026-08-13 工具层已按域拆分).

结构: brain_api.py (API 客户端) + mcp_core.py (FastMCP 实例/瘦身辅助)
      + tools_*.py (10 个域工具模块, 副作用注册) + 本文件 (组装 + 启动)。
"""
import os, sys

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
        print("[WARNING] Redis connection failed - caching disabled", file=sys.stderr)

    # Run using configured transport:
    #   MCP_TRANSPORT=stdio       -> stdio (auto-started by ZCode/client)
    #   MCP_TRANSPORT=streamable-http -> HTTP server (Docker/manual start)
    #   Default: streamable-http (backward compatible with Docker)
    # 2026-08-13 fix: mcp.run() MUST stay inside this guard — forum_functions.py
    # does `from brain_api import brain_client` from within a running event loop,
    # and a module-level mcp.run() re-enters anyio.run → "Already running
    # asyncio in this thread" (forum search/read were completely broken).
    transport = os.environ.get("MCP_TRANSPORT", "streamable-http")
    try:
        mcp.run(transport=transport)
    except TypeError:
        # Fallback if signature differs
        mcp.run(transport)
