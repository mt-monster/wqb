# -*- coding: utf-8 -*-
"""wqb.workflow — Skills Workflow 化迁移引擎.

将高频 PowerShell/脚本流程固化为可编排节点，消除临时脚本与命令模板。

架构：
- nodes/: 各 workflow 节点实现（batch_track/submit_alpha/superalpha/judge/gem/campaign）
- registry.py: 节点注册中心
- executor.py: 执行引擎（支持 dry-run / 断点续跑 / 状态持久化）

Usage:
    from wqb.workflow import execute

    result = execute("batch_track", {
        "region": "KOR",
        "wave": "36A",
        "dataset": "model219",
        "concurrency": 5
    })
"""

from .registry import WorkflowRegistry, get_registry
from .executor import WorkflowExecutor, execute, execute_chain

__all__ = [
    "WorkflowRegistry",
    "get_registry",
    "WorkflowExecutor",
    "execute",
    "execute_chain",
]

__version__ = "0.1.0"
