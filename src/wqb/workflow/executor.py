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

import inspect
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


def _extract_error(output: Dict[str, Any]) -> Optional[str]:
    """从节点输出提取失败原因。

    2026-09-05 修复：campaign / superalpha / feature_engineering 等节点把
    error 放进 result["steps"][-1]，顶层只写 success=False —— 旧实现只读顶层
    error/reason/message，导致 WorkflowResult.error 为 None，execute_chain
    静默中断且无可诊断信息（实测：`campaign success=False error=None`）。
    现按「顶层 → steps 末个失败步 → 兜底」三级回捞。
    """
    for key in ("error", "reason", "message"):
        value = output.get(key)
        if value:
            return str(value)

    steps = output.get("steps")
    if isinstance(steps, list):
        for step in reversed(steps):
            if not isinstance(step, dict) or step.get("success", True):
                continue
            for key in ("error", "reason", "message"):
                value = step.get(key)
                if value:
                    name = step.get("step")
                    return f"[{name}] {value}" if name else str(value)
            name = step.get("step")
            if name:
                return f"Step failed: {name}"

    return "Node reported success=False without an error message"


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

        # 组装调用参数：注入执行上下文 +（节点签名接受 dry_run 时）透传 dry_run。
        # 2026-09-01 缺陷修复（3 类）：
        #   A. submit_alpha/judge/gem/feature_engineering 未读 _context.dry_run →
        #      现已在各节点内短路（network/subprocess/写库前即停）。
        #   B. batch_track/superalpha 有 dry_run 形参但 executor 从不透传 →
        #      现按 inspect.signature 检测并透传 dry_run。
        #   C. executor 干跑分支无条件 success=True 吞掉节点真实 success/error →
        #      现统一按节点返回 dict 的 success 字段真值传播。
        # 不原地修改调用方 params，避免 _context 泄漏回 WorkflowResult.params。
        call_params = dict(params)
        call_params["_context"] = {
            "dry_run": dry_run,
            "store": self.store,
            "registry": self.registry,
        }
        try:
            sig = inspect.signature(node_func)
        except (TypeError, ValueError):
            sig = None
        if sig is not None and "dry_run" in sig.parameters:
            call_params["dry_run"] = dry_run

        try:
            output = node_func(**call_params)
        except Exception as e:
            logger.exception(f"Workflow node {node_name} failed")
            return WorkflowResult(
                success=False,
                node=node_name,
                params=params,
                error=str(e),
                duration_sec=time.time() - start_time,
                dry_run=dry_run,
            )

        # 真值传播：节点返回 dict 且带 success 字段时，以节点判定为准；
        # 否则（非 dict 或未声明 success）视为成功。
        success = True
        error = None
        if isinstance(output, dict):
            success = bool(output.get("success", True))
            if not success:
                error = _extract_error(output)

        return WorkflowResult(
            success=success,
            node=node_name,
            params=params,
            output=output,
            error=error,
            duration_sec=time.time() - start_time,
            dry_run=dry_run,
            metadata={"category": meta.category, "phase": meta.phase},
        )

    def execute_chain(
        self,
        chain: List[Dict[str, Any]],
        dry_run: bool = False,
        stop_on_failure: bool = True,
        join_async: bool = True,
        join_timeout_sec: float = 1800.0,
    ) -> List[WorkflowResult]:
        """执行节点链.

        2026-09-06：补 async join。gem / batch_track / campaign /
        feature_engineering 都是"启动即返回"，而本方法此前只是顺序调用，
        节点之间既不传数据、也不等待 —— 于是文档里那条
        `campaign → feature_engineering → gem` 一旦实跑，就是上游后台任务
        刚起步、下游立刻读到空库。链只在 dry-run 下"看着通"。

        现在：某步返回 task_id 时，默认阻塞等它到终态再走下一步，任务失败
        即按该步失败处理。dry_run 下不 join（没有真任务）。

        Args:
            chain: [{"node": "name", "params": {...}}, ...]
            dry_run: 是否干跑
            stop_on_failure: 失败时是否停止
            join_async: 异步节点是否等待完成后再进入下一步（默认 True）
            join_timeout_sec: 单步等待上限，超时按失败处理

        Returns:
            List[WorkflowResult]
        """
        results = []
        for step in chain:
            node = step.get("node")
            params = step.get("params", {})

            result = self.execute(node, params, dry_run=dry_run)

            if result.success and join_async and not dry_run:
                self._join_async(result, join_timeout_sec)

            results.append(result)

            if not result.success and stop_on_failure:
                logger.error(f"Chain stopped at node {node}: {result.error}")
                break

        return results

    @staticmethod
    def _extract_task_id(output: Any) -> Optional[str]:
        """从节点输出里找后台任务 id（顶层或 steps 里）。"""
        if not isinstance(output, dict):
            return None
        task_id = output.get("task_id")
        if task_id:
            return str(task_id)
        steps = output.get("steps")
        if isinstance(steps, list):
            for step in steps:
                if isinstance(step, dict) and step.get("task_id"):
                    return str(step["task_id"])
        return None

    def _join_async(self, result: WorkflowResult, timeout_sec: float) -> None:
        """等待某步的后台任务到终态，把结论并回 WorkflowResult（原地修改）。"""
        task_id = self._extract_task_id(result.output)
        if not task_id:
            return

        try:
            from .tasks import wait_for_task
        except ImportError as e:  # pragma: no cover
            logger.warning(f"async join unavailable: {e}")
            return

        logger.info(f"[chain] joining async task {task_id} (node={result.node})")
        task = wait_for_task(task_id, timeout_sec=timeout_sec)
        result.metadata["async_task"] = {
            "task_id": task_id,
            "status": task.get("status"),
            "timed_out": task.get("timed_out", False),
        }

        if task.get("timed_out"):
            result.success = False
            result.error = (
                f"后台任务 {task_id} 在 {timeout_sec:.0f}s 内未结束"
                f"（当前状态 {task.get('status')}）；"
                f"用 workflow_task_status(task_id=\"{task_id}\") 继续跟踪"
            )
        elif task.get("status") == "failed":
            result.success = False
            tail = (task.get("stderr_tail") or "").strip()[-400:]
            result.error = (
                f"后台任务 {task_id} 失败"
                + (f"：{task.get('error')}" if task.get("error") else "")
                + (f"；stderr: {tail}" if tail else "")
            )


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
