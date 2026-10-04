# -*- coding: utf-8 -*-
"""区域 × 类别拆分（2026-10-04）：生效画像解析、类别卡、组合控制文件、证据同步、区域 skill 渲染。

层次（后者覆盖前者，锁定表兜底）：
  全局缺省 → 类别卡（category_cards.json，跨区）→ 区域（tracking/<R>/config/settings.json、thresholds.json、
  ra-pipeline 区域 profile）→ 组合（tracking/<R>/config/cells.json）→ 锁定表（locked.py）

命令行：`$WQ_PY -m wqb.profiles {explain,check,sync-cells,render,audit} ...`（`--help` 看参数）。
方案与决策：docs/plans/2026-10-04-ra-region-category-split.md。
"""
from .resolver import backtest_pins, check_region, explain_text, resolve  # noqa: F401
from .taxonomy import card_of, dataset_category, normalize_category  # noqa: F401

__all__ = ["resolve", "explain_text", "backtest_pins", "check_region",
           "card_of", "dataset_category", "normalize_category"]
