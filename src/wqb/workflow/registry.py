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
    phase: int  # 实施 Phase：1=批量/提交，2=组合/判定，4=生成/战役/特征工程
    #: 注：历史上没有 phase 3（该批节点已并入 phase 4），list_nodes(phase=3) 恒为空
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

        # 手动注册核心节点（phase 1/2/4；无 phase 3，见 NodeMeta.phase 注释）
        # 避免动态导入的复杂性，显式注册更可靠
        self._register_core_nodes()

    def _register_core_nodes(self) -> None:
        """注册核心节点（延迟导入避免循环依赖）.

        约定（2026-09-05）：required_params / optional_params 必须与节点 run()
        签名一致（`_context` 与 `dry_run` 除外——前者由 executor 注入，后者是
        全节点统一的执行开关）。workflow_list_nodes 把这份元数据当 API 文档直接
        暴露给 Agent，漂移即误导。回归由 tests/unit/test_skill_integrity.py
        的 test_registry_meta_matches_node_signature 守护。
        """
        # Phase 1: batch_track / submit_alpha
        try:
            from .nodes import batch_track
            self.register(
                "batch_track",
                batch_track.run,
                NodeMeta(
                    name="batch_track",
                    description="S3 批量回测与跟踪（等价包装 brain-sim-alphas-in-batch-and-track；并发纪律见 wqb-concurrency §8）",
                    category="batch",
                    phase=1,
                    required_params=["region", "wave", "dataset"],
                    optional_params=["concurrency", "max_rounds", "output_csv",
                                     "campaign_dir", "detached", "submit",
                                     "skip_diversity_gate", "datasets_extra"],
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
                    optional_params=["selection", "combo", "neutralization", "confirm_submit"],
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
                    description="Alpha 六步闸门判定（等价包装 brain-alpha-judge 评审参考，非提交判定权威且不执行提交；提交判定走 submit_verdict，提交动作走 submit_alpha 节点）",
                    category="judge",
                    phase=2,
                    required_params=["alpha_id"],
                    optional_params=["trend_window_days", "llm_enabled"],
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
                    description="GEM 表达式生成（等价包装 brain-make-some-gem headless_runner）",
                    category="gem",
                    phase=4,
                    required_params=["region", "dataset_id", "delay", "universe"],
                    optional_params=["data_category", "instrument_type", "data_type",
                                     "priors_file", "priors_from_db", "ideas_file", "detached",
                                     "launch_only", "pipeline_mode", "batch_size",
                                     "require_operators", "require_count"],
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
                    optional_params=["dataset", "wave", "subcommand", "extra_args", "calibrate"],
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
                    description="S1-S3 特征工程流程（字段理解→筛选→预处理决策）",
                    category="feature_engineering",
                    phase=4,
                    required_params=["region", "dataset_id", "delay", "universe"],
                    optional_params=["data_category", "force_regen"],
                )
            )
        except ImportError as e:
            logger.warning(f"Failed to register feature_engineering: {e}")

        # Phase 4: wave_gate（ra-pipeline 步 5 门禁；2026-09-11 新增，此前步 5 无节点）
        try:
            from .nodes import wave_gate
            self.register(
                "wave_gate",
                wave_gate.run,
                NodeMeta(
                    name="wave_gate",
                    description="S2→S3 门禁（语法 + gate.py 8 闸 + 体检硬门 + 多样性，落盘 gate_results）",
                    category="gate",
                    phase=4,
                    required_params=["region", "dataset", "wave"],
                    optional_params=["exprs_file", "candidates", "expr", "from_db",
                                     "skip_diversity_gate", "fix", "campaign_dir",
                                     "inspect_mode"],
                )
            )
        except ImportError as e:
            logger.warning(f"Failed to register wave_gate: {e}")

        try:
            from .nodes import hypothesis_round
            self.register(
                "hypothesis_round",
                hypothesis_round.run,
                NodeMeta(
                    name="hypothesis_round",
                    description="饱和数据集假设优先实验轮次（每假设 4 条：主假设/消融/对照/变体；纯本地零平台成本）",
                    category="research",
                    phase=2,
                    required_params=["dataset_id"],
                    optional_params=["catalog_path", "max_hypotheses", "region",
                                     "delay", "session_id", "save_ledger"],
                )
            )
        except ImportError as e:
            logger.warning(f"Failed to register hypothesis_round: {e}")

        # Phase 2: structural_reconstruct（结构重构变体生成与效果追踪）
        try:
            from .nodes import structural_reconstruct
            self.register(
                "structural_reconstruct",
                structural_reconstruct.run,
                NodeMeta(
                    name="structural_reconstruct",
                    description="结构重构变体生成与效果追踪（解决 sharpe vs fitness/2Y 结构性权衡；合规约束：禁止 add(A,B) 混信号调参）",
                    category="research",
                    phase=2,
                    required_params=["action"],
                    optional_params=["base_signal", "conflict_signal", "strategy", "region",
                                     "wave", "variant_id", "original_expr", "variant_expr",
                                     "alpha_id", "metrics", "status", "expression"],
                )
            )
        except ImportError as e:
            logger.warning(f"Failed to register structural_reconstruct: {e}")

        # Phase 4: step_metrics —— 已于 2026-09-17 整体下线（归档 attic/step_metrics_20260917/）
        # 原因：唯一自动采集入口 collect_from_checkpoint() 是 TODO 空壳（无数据源）；
        # 9 个质量指标可从既有表推导（写新表=双真相源）；6 个增益指标是反事实估算无客观来源；
        # 五张表恒 0 行。替代方案 = tools/step_funnel.py（只读推导）。
        # 复活步骤见 attic/step_metrics_20260917/README.md。

        # Phase 4: inventory_scan（自动化库存盘点，S-PRE 增强）
        try:
            from .nodes import inventory_scan
            self.register(
                "inventory_scan",
                inventory_scan.run,
                NodeMeta(
                    name="inventory_scan",
                    description="自动化库存盘点（S-PRE 增强）：枚举已有 IS alpha + 资格门复算 + 写回过闸率先验 + 去参数网格 + OS 撞车预筛 + 篮内正交 + 平台复核",
                    category="inventory",
                    phase=4,
                    required_params=["region"],
                    optional_params=["target", "regions"],
                )
            )
        except ImportError as e:
            logger.warning(f"Failed to register inventory_scan: {e}")

        # Phase 4: field_understanding（自动化字段理解，S1 增强）
        try:
            from .nodes import field_understanding
            self.register(
                "field_understanding",
                field_understanding.run,
                NodeMeta(
                    name="field_understanding",
                    description="自动化字段理解（S1 增强）：分析字段特征 + 生成字段理解报告 + 自动分类字段 + 识别高价值字段",
                    category="field",
                    phase=4,
                    required_params=["region", "dataset"],
                    optional_params=["delay", "auto_classify", "identify_high_value"],
                )
            )
        except ImportError as e:
            logger.warning(f"Failed to register field_understanding: {e}")

        # Phase 4: gem_wave（合并选波到 GEM 生成，S2 增强）
        try:
            from .nodes import gem_wave
            self.register(
                "gem_wave",
                gem_wave.run,
                NodeMeta(
                    name="gem_wave",
                    description="合并选波到 GEM 生成（S2 增强）：GEM 生成 + 自动去重 + 自动分桶 + 自动骨架配给 + 自动选波",
                    category="gem",
                    phase=4,
                    required_params=["region", "dataset_id", "delay", "universe"],
                    optional_params=["data_type", "wave", "auto_dedup", "auto_bucket", "auto_skeleton", "auto_select",
                                     "max_per_skeleton", "source"],
                )
            )
        except ImportError as e:
            logger.warning(f"Failed to register gem_wave: {e}")

        # Phase 4: unified_gate（合并重复门禁检查，S2→S3 增强）
        try:
            from .nodes import unified_gate
            self.register(
                "unified_gate",
                unified_gate.run,
                NodeMeta(
                    name="unified_gate",
                    description="合并重复门禁检查（S2→S3 增强）：幽灵算子硬闸 + 多样性守卫 + 体检→表达式硬门 + 8 闸预检",
                    category="gate",
                    phase=4,
                    required_params=["region", "dataset", "wave"],
                    optional_params=["exprs_file", "from_db", "skip_diversity_gate"],
                )
            )
        except ImportError as e:
            logger.warning(f"Failed to register unified_gate: {e}")

        # Phase 4: auto_harvest（自动化收批，S3 增强）
        try:
            from .nodes import auto_harvest
            self.register(
                "auto_harvest",
                auto_harvest.run,
                NodeMeta(
                    name="auto_harvest",
                    description="自动化收批（S3 增强）：自动收批 multisim 结果 + 自动关联 expressions + 自动写回 backtest_results + 自动生成收批报告",
                    category="harvest",
                    phase=4,
                    required_params=["region", "wave"],
                    optional_params=["multisim_id", "auto_link", "auto_upsert", "auto_report"],
                )
            )
        except ImportError as e:
            logger.warning(f"Failed to register auto_harvest: {e}")

        # Phase 4: auto_review（自动化评审，S4 增强）
        try:
            from .nodes import auto_review
            self.register(
                "auto_review",
                auto_review.run,
                NodeMeta(
                    name="auto_review",
                    description="自动化评审（S4 增强）：自动 S4 预筛 + 自动 walls 诊断 + 自动卡闸辅助腿检索 + 自动生成评审报告",
                    category="review",
                    phase=4,
                    required_params=["region", "wave"],
                    optional_params=["dataset", "auto_prescreen", "auto_walls", "auto_salvage", "auto_report"],
                )
            )
        except ImportError as e:
            logger.warning(f"Failed to register auto_review: {e}")

        # Phase 4: auto_pyramid（自动化点塔进度回写，S6 增强）
        try:
            from .nodes import auto_pyramid
            self.register(
                "auto_pyramid",
                auto_pyramid.run,
                NodeMeta(
                    name="auto_pyramid",
                    description="自动化点塔进度回写（S6 增强）：自动查询点塔进度 + 自动嵌入 wave_result.key_findings + 自动生成点塔报告",
                    category="pyramid",
                    phase=4,
                    required_params=["region", "wave"],
                    optional_params=["delay", "auto_embed", "auto_report"],
                )
            )
        except ImportError as e:
            logger.warning(f"Failed to register auto_pyramid: {e}")

        # Phase 4: modeb_improve（Mode B 想法层改进，S4 增强）
        try:
            from .nodes import modeb_improve
            self.register(
                "modeb_improve",
                modeb_improve.run,
                NodeMeta(
                    name="modeb_improve",
                    description="Mode B 想法层改进（S4 增强）：4 阶段改进策略（条件化/残差/交互/时间结构），生成改进表达式并入库",
                    category="research",
                    phase=4,
                    required_params=["region", "dataset", "base_field"],
                    optional_params=["phase", "wave", "start_wave"],
                )
            )
        except ImportError as e:
            logger.warning(f"Failed to register modeb_improve: {e}")

        # Phase 4: alpha_booster（通用 Alpha 短板提升，S4 增强）
        try:
            from .nodes import alpha_booster
            self.register(
                "alpha_booster",
                alpha_booster.run,
                NodeMeta(
                    name="alpha_booster",
                    description="通用 Alpha 短板提升（S4 增强）：自动诊断 2y_sharpe/sub_universe/turnover 短板，基于论坛实证算子库生成改进变体并入库",
                    category="review",
                    phase=4,
                    required_params=["region", "wave"],
                    optional_params=["dataset", "alpha_id", "max_variants_per_alpha",
                                     "auto_insert", "forum_refresh"],
                )
            )
        except ImportError as e:
            logger.warning(f"Failed to register alpha_booster: {e}")


def get_registry() -> WorkflowRegistry:
    """获取注册中心单例."""
    registry = WorkflowRegistry.get_instance()
    registry._auto_discover()
    return registry
