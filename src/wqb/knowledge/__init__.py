# -*- coding: utf-8 -*-
"""wqb.knowledge — 回测经验闭环（记录 → 蒸馏 → 复用 → 验证）。

模块边界：
- `classify`  纯函数：把一条回测事实解释成 primary_wall / failure_class / outcome；
- `versions`  知识版本指纹（priors_sha / rules_sha / knowledge_version）；
- `capture`   唯一写入方：事实表 → `attempt_knowledge` 索引（可幂等重建）；
- `distill`   波级 / 区域级统计蒸馏（P2）。

事实源永远是 `backtest_results` / `expressions` / `wave_results`；本包只生产**派生解释**。
"""
from __future__ import annotations

__all__ = [
    "classify", "versions", "capture", "distill", "select",
    "lifecycle", "templates", "yield_report", "digest",
]
