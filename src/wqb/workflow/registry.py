# -*- coding: utf-8 -*-
"""Workflow 节点注册中心.

管理所有可用 workflow 节点的注册、发现与元数据查询。
"""

from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional
import logging

logger = logging.getLogger(__name__)


@dataclass
class NodeMeta:
    """Workflow 节点元数据."""
    name: str
    description: str
    category: str  # batch / submit / superalpha / judge / gem / campaign
    phase: int  # 1-4，对应实施 Phase
    required_params: List[str] = field(default_factory=list)
    optional_params: List[str] = field(default_factory=list)


class WorkflowRegistry:
    """Workflow 节点注册中心（单例）."""

    _instance: Optional["WorkflowRegistry"] = None

    def __init__(self):
        self._nodes: Dict[str, Callable] = {}
        self._meta: Dict[str, NodeMeta] = {}
        self._initialized = False

    @classmethod
    def get_instance(cls) -> "WorkflowRegistry":
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def register(self, name: str, func: Callable, meta: NodeMeta) -> None:
        """注册 workflow 节点."""
        self._nodes[name] = func
        self._meta[name] = meta
        logger.debug(f"Registered workflow node: {name} (phase={meta.phase})")

    def get(self, name: str) -> Optional[Callable]:
        """获取节点函数."""
        return self._nodes.get(name)

    def get_meta(self, name: str) -> Optional[NodeMeta]:
        """获取节点元数据."""
        return self._meta.get(name)

    def list_nodes(self, category: Optional[str] = None, phase: Optional[int] = None) -> List[str]:
        """列出所有节点，可按 category/phase 过滤."""
        result = []
        for name, meta in self._meta.items():
            if category and meta.category != category:
                continue
            if phase and meta.phase != phase:
                continue
            result.append(name)
        return sorted(result)

    def list_categories(self) -> List[str]:
        """列出所有类别."""
        return sorted(set(m.category for m in self._meta.values()))

    def validate_params(self, name: str, params: Dict[str, Any]) -> List[str]:
        """验证参数，返回缺失的必填参数列表."""
        meta = self._meta.get(name)
        if not meta:
            return [f"Unknown node: {name}"]
        missing = [p for p in meta.required_params if p not in params]
        return missing

    def _auto_discover(self) -> None:
        """自动发现 nodes/ 目录下的所有节点."""
        if self._initialized:
            return
        self._initialized = True

        # 手动注册 Phase 1-4 的核心节点
        # 避免动态导入的复杂性，显式注册更可靠
        self._register_core_nodes()

    def _register_core_nodes(self) -> None:
        """注册核心节点（延迟导入避免循环依赖）."""
        # Phase 1: batch_track / submit_alpha
        try:
            from .nodes import batch_track
            self.register(
                "batch_track",
                batch_track.run,
                NodeMeta(
                    name="batch_track",
                    description="S3 批量回测与跟踪（等价包装 brain-simAlphasinBatch-and-track；并发纪律见 wqb-concurrency §8）",
                    category="batch",
                    phase=1,
                    required_params=["region", "wave", "dataset"],
                    optional_params=["concurrency", "max_rounds", "dry_run", "output_csv"],
                )
            )
        except ImportError as e:
            logger.warning(f"Failed to register batch_track: {e}")

        try:
            from .nodes import submit_alpha
            self.register(
                "submit_alpha",
                submit_alpha.run,
                NodeMeta(
                    name="submit_alpha",
                    description="提交路由与状态确认（等价包装 worldquant-submit-alpha；403 盲区判定权威 = tools/submit_verdict.py）",
                    category="submit",
                    phase=1,
                    required_params=["alpha_id"],
                    optional_params=["name", "color", "tags", "descriptions", "force", "confirm_submit", "verify_timeout"],
                )
            )
        except ImportError as e:
            logger.warning(f"Failed to register submit_alpha: {e}")

        # Phase 2: superalpha / judge
        try:
            from .nodes import superalpha
            self.register(
                "superalpha",
                superalpha.run,
                NodeMeta(
                    name="superalpha",
                    description="SuperAlpha 构建与提交（等价包装 wq-brain-superalpha）",
                    category="superalpha",
                    phase=2,
                    required_params=["region", "components"],
                    optional_params=["selection", "combo", "neutralization", "confirm_submit", "dry_run"],
                )
            )
        except ImportError as e:
            logger.warning(f"Failed to register superalpha: {e}")

        try:
            from .nodes import judge
            self.register(
                "judge",
                judge.run,
                NodeMeta(
                    name="judge",
                    description="Alpha 六步闸门判定（等价包装 brain-alpha-judge 评审参考，非提交判定权威；提交判定走 tools/submit_verdict.py）",
                    category="judge",
                    phase=2,
                    required_params=["alpha_id"],
                    optional_params=["trend_window_days", "llm_enabled", "confirm_submit"],
                )
            )
        except ImportError as e:
            logger.warning(f"Failed to register judge: {e}")

        # Phase 4: gem / campaign / feature_engineering
        try:
            from .nodes import gem
            self.register(
                "gem",
                gem.run,
                NodeMeta(
                    name="gem",
                    description="GEM 表达式生成（等价包装 brain-makeSomeGem headless_runner）",
                    category="gem",
                    phase=4,
                    required_params=["region", "dataset_id", "delay", "universe"],
                    optional_params=["data_category", "instrument_type", "data_type", "priors_file", "detached"],
                )
            )
        except ImportError as e:
            logger.warning(f"Failed to register gem: {e}")

        try:
            from .nodes import campaign
            self.register(
                "campaign",
                campaign.run,
                NodeMeta(
                    name="campaign",
                    description="S1-S6 战役阶段执行（包装 wq-brain-campaign-toolkit）",
                    category="campaign",
                    phase=4,
                    required_params=["region", "stage"],
                    optional_params=["dataset", "wave", "subcommand", "extra_args"],
                )
            )
        except ImportError as e:
            logger.warning(f"Failed to register campaign: {e}")

        try:
            from .nodes import feature_engineering
            self.register(
                "feature_engineering",
                feature_engineering.run,
                NodeMeta(
                    name="feature_engineering",
                    description="S1-S3 特征工程流程（字段理解→筛选→预处理决策）[实验性节点，未接 MCP 暴露，勿依赖]",
                    category="feature_engineering",
                    phase=4,
                    required_params=["region", "dataset_id", "delay", "universe"],
                    optional_params=["data_category", "force_regen"],
                )
            )
        except ImportError as e:
            logger.warning(f"Failed to register feature_engineering: {e}")


def get_registry() -> WorkflowRegistry:
    """获取注册中心单例."""
    registry = WorkflowRegistry.get_instance()
    registry._auto_discover()
    return registry
