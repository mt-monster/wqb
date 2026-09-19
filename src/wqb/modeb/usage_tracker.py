# -*- coding: utf-8 -*-
"""Mode B 算子使用频率追踪器.

追踪每个算子的使用次数、成功次数、最后使用波次，支持全算子轮换机制.
"""

import json
import os
from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import Dict, List, Optional


@dataclass
class OperatorStats:
    """单个算子的统计信息."""
    usage_count: int = 0
    success_count: int = 0
    last_used_wave: int = 0
    total_sharpe_delta: float = 0.0
    total_fitness_delta: float = 0.0
    total_turnover_delta: float = 0.0
    regions: Dict[str, int] = field(default_factory=dict)

    @property
    def success_rate(self) -> float:
        """胜率."""
        return self.success_count / max(self.usage_count, 1)

    @property
    def avg_sharpe_delta(self) -> float:
        """平均 Sharpe 变化."""
        return self.total_sharpe_delta / max(self.usage_count, 1)

    @property
    def avg_fitness_delta(self) -> float:
        """平均 Fitness 变化."""
        return self.total_fitness_delta / max(self.usage_count, 1)

    @property
    def avg_turnover_delta(self) -> float:
        """平均 Turnover 变化."""
        return self.total_turnover_delta / max(self.usage_count, 1)


class OperatorUsageTracker:
    """算子使用频率追踪器."""

    def __init__(self, persist_path: Optional[str] = None):
        """初始化追踪器.

        Args:
            persist_path: 持久化文件路径（JSON）
        """
        self.persist_path = persist_path
        self._stats: Dict[str, OperatorStats] = {}
        self._load()

    def _load(self) -> None:
        """从文件加载统计."""
        if not self.persist_path or not os.path.exists(self.persist_path):
            return
        try:
            with open(self.persist_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            for name, stats_dict in data.get("operators", {}).items():
                self._stats[name] = OperatorStats(**stats_dict)
        except Exception:
            pass

    def _save(self) -> None:
        """保存统计到文件."""
        if not self.persist_path:
            return
        try:
            os.makedirs(os.path.dirname(self.persist_path), exist_ok=True)
            data = {
                "updated_at": datetime.now().isoformat(),
                "operators": {
                    name: asdict(stats) for name, stats in self._stats.items()
                },
            }
            with open(self.persist_path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception:
            pass

    def record_usage(
        self,
        operator: str,
        wave: int,
        success: bool = False,
        sharpe_delta: float = 0.0,
        fitness_delta: float = 0.0,
        turnover_delta: float = 0.0,
        region: Optional[str] = None,
    ) -> None:
        """记录算子使用.

        Args:
            operator: 算子名称
            wave: 当前波次
            success: 是否成功（指标提升且过闸）
            sharpe_delta: Sharpe 变化
            fitness_delta: Fitness 变化
            turnover_delta: Turnover 变化
            region: 区域
        """
        if operator not in self._stats:
            self._stats[operator] = OperatorStats()

        stats = self._stats[operator]
        stats.usage_count += 1
        stats.last_used_wave = wave
        if success:
            stats.success_count += 1
        stats.total_sharpe_delta += sharpe_delta
        stats.total_fitness_delta += fitness_delta
        stats.total_turnover_delta += turnover_delta
        if region:
            stats.regions[region] = stats.regions.get(region, 0) + 1

        self._save()

    def get_usage_count(self, operator: str) -> int:
        """获取使用次数."""
        return self._stats.get(operator, OperatorStats()).usage_count

    def get_success_rate(self, operator: str) -> float:
        """获取胜率."""
        return self._stats.get(operator, OperatorStats()).success_rate

    def get_avg_sharpe_delta(self, operator: str) -> float:
        """获取平均 Sharpe 变化."""
        return self._stats.get(operator, OperatorStats()).avg_sharpe_delta

    def get_last_used_wave(self, operator: str) -> int:
        """获取最后使用波次."""
        return self._stats.get(operator, OperatorStats()).last_used_wave

    def get_all_stats(self) -> Dict[str, OperatorStats]:
        """获取所有统计."""
        return self._stats.copy()

    def get_underused_operators(
        self,
        all_operators: List[str],
        current_wave: int,
        usage_threshold: float = 0.5,
        unused_waves_threshold: int = 5,
    ) -> List[str]:
        """获取低使用率算子.

        Args:
            all_operators: 所有算子列表
            current_wave: 当前波次
            usage_threshold: 使用率阈值（低于此值视为低使用）
            unused_waves_threshold: 未使用波次阈值

        Returns:
            低使用率算子列表（按使用率升序）
        """
        if not self._stats:
            return all_operators.copy()

        total_usage = sum(s.usage_count for s in self._stats.values())
        avg_usage = total_usage / max(len(self._stats), 1)

        underused = []
        for op in all_operators:
            stats = self._stats.get(op, OperatorStats())

            # 条件 1：从未使用
            if stats.usage_count == 0:
                underused.append((op, 0))
                continue

            # 条件 2：使用率低于平均值
            usage_rate = stats.usage_count / max(total_usage, 1)
            if usage_rate < usage_threshold:
                underused.append((op, usage_rate))
                continue

            # 条件 3：长时间未使用
            waves_since_last_use = current_wave - stats.last_used_wave
            if waves_since_last_use > unused_waves_threshold:
                underused.append((op, usage_rate))

        # 按使用率升序排序
        underused.sort(key=lambda x: x[1])
        return [op for op, _ in underused]

    def get_high_winrate_operators(
        self,
        min_usage: int = 3,
        top_k: int = 10,
    ) -> List[str]:
        """获取高胜率算子.

        Args:
            min_usage: 最小使用次数
            top_k: 返回数量

        Returns:
            高胜率算子列表（按胜率降序）
        """
        candidates = [
            (op, stats.success_rate)
            for op, stats in self._stats.items()
            if stats.usage_count >= min_usage
        ]
        candidates.sort(key=lambda x: x[1], reverse=True)
        return [op for op, _ in candidates[:top_k]]

    def get_rotation_candidates(
        self,
        all_operators: List[str],
        current_wave: int,
        count: int = 3,
    ) -> List[str]:
        """获取轮换候选算子（保底机制）.

        优先选择：
        1. 从未使用的算子
        2. 长时间未使用的算子
        3. 使用率最低的算子

        Args:
            all_operators: 所有算子列表
            current_wave: 当前波次
            count: 返回数量

        Returns:
            轮换候选算子列表
        """
        # 按优先级分组
        never_used = []
        long_unused = []
        low_usage = []

        total_usage = sum(s.usage_count for s in self._stats.values())

        for op in all_operators:
            stats = self._stats.get(op, OperatorStats())

            if stats.usage_count == 0:
                never_used.append(op)
            elif current_wave - stats.last_used_wave > 5:
                long_unused.append(op)
            elif total_usage > 0:
                usage_rate = stats.usage_count / total_usage
                if usage_rate < 0.1:  # 使用率 < 10%
                    low_usage.append((op, usage_rate))

        # 按优先级合并
        result = never_used[:count]
        remaining = count - len(result)

        if remaining > 0:
            result.extend(long_unused[:remaining])
            remaining = count - len(result)

        if remaining > 0:
            low_usage.sort(key=lambda x: x[1])
            result.extend([op for op, _ in low_usage[:remaining]])

        return result[:count]

    def get_coverage_report(self, all_operators: List[str]) -> Dict:
        """获取覆盖度报告.

        Args:
            all_operators: 所有算子列表

        Returns:
            覆盖度统计
        """
        used = set(self._stats.keys())
        all_set = set(all_operators)

        return {
            "total_operators": len(all_operators),
            "used_operators": len(used),
            "never_used": list(all_set - used),
            "coverage_rate": len(used) / max(len(all_operators), 1),
            "total_usage": sum(s.usage_count for s in self._stats.values()),
            "total_success": sum(s.success_count for s in self._stats.values()),
            "overall_success_rate": (
                sum(s.success_count for s in self._stats.values()) /
                max(sum(s.usage_count for s in self._stats.values()), 1)
            ),
        }
