# -*- coding: utf-8 -*-
"""Workflow 执行引擎.

支持 dry-run；节点执行结果统一封装为 WorkflowResult。

2026-08-31 精简：
  - 移除伪 fallback（原 `use_fallback` 只返回 fallback_cli 字符串、从不真正执行，
    且 fallback_cli 指向的 scripts/batch_simulator.py 等路径均不存在）——节点内部
    已各自返回详细错误，fallback 属死代码。
  - 移除 save_checkpoint/load_checkpoint（无调用方，且与节点内 upsert_ledger 重复）。
"""
from __future__ import annotations

import json
import logging
import time
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional

from .registry import get_registry

logger = logging.getLogger(__name__)


@dataclass
class WorkflowResult:
    """Workflow 执行结果."""
    success: bool
    node: str
    params: Dict[str, Any]
    output: Any = None
    error: Optional[str] = None
    duration_sec: float = 0.0
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    dry_run: bool = False
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "success": self.success,
            "node": self.node,
            "params": self.params,
            "output": self.output,
            "error": self.error,
            "duration_sec": self.duration_sec,
            "timestamp": self.timestamp,
            "dry_run": self.dry_run,
            "metadata": self.metadata,
        }


class WorkflowExecutor:
    """Workflow 执行引擎."""

    def __init__(self, db_path: Optional[str] = None):
        self.registry = get_registry()
        self.db_path = db_path or "data/wqb.db"
        self._store = None

    @property
    def store(self):
        """延迟加载 DB store."""
        if self._store is None:
            try:
                from wqb.store.campaign import CampaignStore
                self._store = CampaignStore(self.db_path)
            except Exception as e:
                logger.warning(f"Failed to init CampaignStore: {e}")
        return self._store

    def execute(
        self,
        node_name: str,
        params: Dict[str, Any],
        dry_run: bool = False,
    ) -> WorkflowResult:
        """执行 workflow 节点.

        Args:
            node_name: 节点名称
            params: 参数字典
            dry_run: 是否干跑（不执行实际写操作，仅验证参数与流程）

        Returns:
            WorkflowResult
        """
        start_time = time.time()

        # 验证节点存在
        node_func = self.registry.get(node_name)
        meta = self.registry.get_meta(node_name)

        if not node_func or not meta:
            return WorkflowResult(
                success=False,
                node=node_name,
                params=params,
                error=f"Unknown workflow node: {node_name}",
                duration_sec=time.time() - start_time,
            )

        # 验证参数
        missing = self.registry.validate_params(node_name, params)
        if missing:
            return WorkflowResult(
                success=False,
                node=node_name,
                params=params,
                error=f"Missing required params: {missing}",
                duration_sec=time.time() - start_time,
            )

        # 干跑模式：返回执行计划（不调用节点函数）
        if dry_run:
            return WorkflowResult(
                success=True,
                node=node_name,
                params=params,
                output={
                    "plan": f"Would execute {node_name} with params: "
                            f"{json.dumps(params, ensure_ascii=False)}",
                },
                duration_sec=time.time() - start_time,
                dry_run=True,
                metadata={"category": meta.category, "phase": meta.phase},
            )

        # 执行节点
        try:
            # 注入执行上下文
            params["_context"] = {
                "dry_run": dry_run,
                "store": self.store,
                "registry": self.registry,
            }

            output = node_func(**params)

            return WorkflowResult(
                success=True,
                node=node_name,
                params=params,
                output=output,
                duration_sec=time.time() - start_time,
                metadata={"category": meta.category, "phase": meta.phase},
            )

        except Exception as e:
            logger.exception(f"Workflow node {node_name} failed")
            return WorkflowResult(
                success=False,
                node=node_name,
                params=params,
                error=str(e),
                duration_sec=time.time() - start_time,
            )

    def execute_chain(
        self,
        chain: List[Dict[str, Any]],
        dry_run: bool = False,
        stop_on_failure: bool = True,
    ) -> List[WorkflowResult]:
        """执行节点链.

        Args:
            chain: [{"node": "name", "params": {...}}, ...]
            dry_run: 是否干跑
            stop_on_failure: 失败时是否停止

        Returns:
            List[WorkflowResult]
        """
        results = []
        for step in chain:
            node = step.get("node")
            params = step.get("params", {})

            result = self.execute(node, params, dry_run=dry_run)
            results.append(result)

            if not result.success and stop_on_failure:
                logger.error(f"Chain stopped at node {node}: {result.error}")
                break

        return results


# 便捷函数
_default_executor: Optional[WorkflowExecutor] = None


def get_executor() -> WorkflowExecutor:
    """获取默认执行器."""
    global _default_executor
    if _default_executor is None:
        _default_executor = WorkflowExecutor()
    return _default_executor


def execute(node_name: str, params: Dict[str, Any], **kwargs) -> WorkflowResult:
    """执行 workflow 节点的便捷函数."""
    return get_executor().execute(node_name, params, **kwargs)


def execute_chain(chain: List[Dict[str, Any]], **kwargs) -> List[WorkflowResult]:
    """执行节点链的便捷函数."""
    return get_executor().execute_chain(chain, **kwargs)
