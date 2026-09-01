# -*- coding: utf-8 -*-
"""MCP 工具提示装饰器：标记节点应优先使用 MCP 工具而非手写脚本.

规约来源：AGENTS.md §5 层 0 — 结构化数据读写首选 wqb-db MCP 工具。

2026-08-31 精简：
  - 原 MCP_TOOLS 大清单（60+ 工具名硬编码）与 NODE_MCP_REQUIREMENTS 无消费方、
    check_mcp_tools 的 check_passed 恒 True（纯空转），且随工具增减必然漂移。
  - 现仅保留装饰器：执行节点前打印一条 INFO 日志提示，实际工具可用性由 MCP
    客户端在调用时验证，不做假校验。
"""
from __future__ import annotations

import functools
import logging
from typing import Callable

logger = logging.getLogger(__name__)


def require_mcp_tools(node_name: str):
    """装饰器：标记节点需要 MCP 工具，执行前打印提示日志.

    Usage:
        @require_mcp_tools("batch_track")
        def run(...):
            ...
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            logger.info(
                f"[MCP Hint] {node_name}: 结构化数据读写优先走 wqb-db MCP 工具，"
                f"平台交互优先走 wq-brain-http MCP 工具（AGENTS.md §5 层 0）"
            )
            return func(*args, **kwargs)
        return wrapper
    return decorator
