# -*- coding: utf-8 -*-
"""DiversityMixin: diversity potential, ranking, checkpoint, rules, reviews, ideas."""
from __future__ import annotations

from typing import Any, Dict, Optional

from ._common import _loads


class DiversityMixin:
    """Diversity potential, ranking, checkpoint, methodology, review, idea methods."""

    def upsert_diversity(self, region: str, dataset: str, data: Dict[str, Any]) -> None:
        """写入 diversity 分析结果。

        数据统一存入 ledger_kv (key=diversity_{dataset})，
        diversity_potential 表已废弃，不再写入。
        """
        self.upsert_ledger(region, f"diversity_{dataset}", data)

    save_diversity_potential = upsert_diversity

    def get_diversity(self, region: str, dataset: str) -> Optional[Dict[str, Any]]:
        """读取 diversity 分析结果（统一从 ledger_kv 获取）。"""
        cached = self.get_ledger(region, f"diversity_{dataset}")
        if isinstance(cached, dict):
            return cached
        return None

    load_diversity_potential = get_diversity

    def upsert_ranking(self, region: str, payload: Dict[str, Any]) -> None:
        self.upsert_ledger(region, "s0_ranking", payload)

    def get_ranking(self, region: str) -> Optional[Dict[str, Any]]:
        val = self.get_ledger(region, "s0_ranking")
        return val if isinstance(val, dict) else None

    def upsert_checkpoint(self, region: str, wave: str, ck: Dict[str, Any]) -> None:
        self.upsert_ledger(region, f"ckpt_w{wave}", ck)

    def get_checkpoint(self, region: str, wave: str) -> Optional[Dict[str, Any]]:
        val = self.get_ledger(region, f"ckpt_w{wave}")
        return val if isinstance(val, dict) else None

    def upsert_methodology_rules(self, region: str, data: Dict[str, Any]) -> None:
        self.upsert_ledger(region, "methodology_rules", data)

    def get_methodology_rules(self, region: str) -> Optional[Dict[str, Any]]:
        val = self.get_ledger(region, "methodology_rules")
        return val if isinstance(val, dict) else None

    def upsert_review(self, region: str, tag: str, payload: Dict[str, Any]) -> None:
        self.upsert_ledger(region, f"review_{tag}", payload)

    def upsert_idea(self, region: str, dataset: str, delay: int, idea: Dict[str, Any]) -> None:
        self.upsert_ledger(region, f"s2_{dataset}_d{delay}_idea", idea)

    def get_idea(self, region: str, dataset: str, delay: int) -> Optional[Dict[str, Any]]:
        val = self.get_ledger(region, f"s2_{dataset}_d{delay}_idea")
        return val if isinstance(val, dict) else None
