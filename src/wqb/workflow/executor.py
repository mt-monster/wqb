# -*- coding: utf-8 -*-
"""Workflow 执行引擎.

支持 dry-run、断点续跑、状态持久化到 DB。
"""

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
    fallback_used: bool = False
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
            "fallback_used": self.fallback_used,
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
        use_fallback: bool = False,
    ) -> WorkflowResult:
        """执行 workflow 节点.

        Args:
            node_name: 节点名称
            params: 参数字典
            dry_run: 是否干跑（不执行实际写操作）
            use_fallback: 是否使用 fallback CLI

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

        # 干跑模式：返回执行计划
        if dry_run:
            return WorkflowResult(
                success=True,
                node=node_name,
                params=params,
                output={
                    "plan": f"Would execute {node_name} with params: {json.dumps(params, ensure_ascii=False)}",
                    "fallback_cli": meta.fallback_cli,
                },
                duration_sec=time.time() - start_time,
                dry_run=True,
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

            # 尝试 fallback
            if use_fallback and meta.fallback_cli:
                return WorkflowResult(
                    success=False,
                    node=node_name,
                    params=params,
                    error=str(e),
                    duration_sec=time.time() - start_time,
                    fallback_used=True,
                    metadata={"fallback_cli": meta.fallback_cli},
                )

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

    def save_checkpoint(self, key: str, data: Dict[str, Any]) -> None:
        """保存 checkpoint 到 DB."""
        if self.store:
            try:
                self.store.upsert_ledger("WORKFLOW", f"ckpt_{key}", data)
            except Exception as e:
                logger.warning(f"Failed to save checkpoint: {e}")

    def load_checkpoint(self, key: str) -> Optional[Dict[str, Any]]:
        """从 DB 加载 checkpoint."""
        if self.store:
            try:
                return self.store.get_ledger("WORKFLOW", f"ckpt_{key}")
            except Exception as e:
                logger.warning(f"Failed to load checkpoint: {e}")
        return None


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
