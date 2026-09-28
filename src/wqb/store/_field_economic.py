# -*- coding: utf-8 -*-
"""字段经济学含义归类器：按字段名/description 的经济学含义分簇。

2026-09-25 落地：解决 GEM 字段池只按"主体 token"分簇、无经济学约束的问题。
model109 542 字段实证：按主体 token 分簇导致 GEM 收到 30 个随机字段自由组合，
产物全是模板扫参（0 DIRECT / 0 COMBO）。按经济学含义归类后，GEM 可按类别
生成有经济含义的概念（价值×成长、质量×动量等），而非随机拼接。
"""
from __future__ import annotations

import re
from typing import Any, Dict, List, Optional, Tuple

# 经济学类别定义：类别名 → (关键词列表, 权重, 描述)
# 权重用于字段质量评分时的类别加成（高权重类别优先入池）
ECONOMIC_CATEGORIES: Dict[str, Dict[str, Any]] = {
    "value": {
        "keywords": [
            "value", "valuation", "pe", "pb", "ps", "p/e", "p/b", "p/s",
            "ev", "ebitda", "book_value", "price_to", "enterprise_value",
            "earnings_yield", "dividend_yield", "fcf_yield", "b/p", "e/p",
            "s/p", "cash_flow_yield", "earnings_price", "book_price",
        ],
        "weight": 1.2,
        "description": "价值类：估值比率、收益率、价格相对基本面",
    },
    "growth": {
        "keywords": [
            "growth", "cagr", "revenue_change", "eps_change", "sales_growth",
            "earnings_growth", "profit_growth", "expansion", "acceleration",
            "momentum", "trend", "increase", "decrease", "change_percent",
        ],
        "weight": 1.1,
        "description": "成长类：收入/利润/资产增长率、加速度",
    },
    "quality": {
        "keywords": [
            "quality", "roe", "roa", "roi", "margin", "profitability",
            "accruals", "earnings_quality", "debt_to_equity", "current_ratio",
            "quick_ratio", "interest_coverage", "operating_margin", "pretax_margin",
            "net_margin", "gross_margin", "return_on", "efficiency",
        ],
        "weight": 1.15,
        "description": "质量类：盈利能力、财务稳健性、运营效率",
    },
    "size": {
        "keywords": [
            "size", "market_cap", "market_capitalization", "total_assets",
            "shares_outstanding", "enterprise_value", "float", "volume_weighted",
            "large_cap", "small_cap", "mid_cap", "scale",
        ],
        "weight": 0.9,
        "description": "规模类：市值、资产规模、股本规模",
    },
    "momentum": {
        "keywords": [
            "momentum", "reversal", "ts_delta", "ts_returns", "price_change",
            "return_", "trend", "moving_average", "ma_", "breakout",
            "continuation", "reversion", "mean_reversion", "oversold", "overbought",
        ],
        "weight": 1.0,
        "description": "动量/反转类：价格趋势、均值回归、突破",
    },
    "sentiment": {
        "keywords": [
            "sentiment", "news", "social", "analyst_sentiment", "emotion",
            "buzz", "hype", "attention", "popularity", "trending",
            "media", "press", "coverage", "mention",
        ],
        "weight": 1.05,
        "description": "情绪类：新闻情绪、社交媒体、分析师情绪",
    },
    "risk": {
        "keywords": [
            "risk", "volatility", "beta", "credit", "debt", "leverage",
            "default", "bankruptcy", "distress", "downside", "drawdown",
            "var", "cvar", "sharpe", "sortino", "treynor",
        ],
        "weight": 1.0,
        "description": "风险类：波动率、信用风险、杠杆、下行风险",
    },
    "liquidity": {
        "keywords": [
            "liquidity", "volume", "turnover", "trading", "bid_ask",
            "spread", "depth", "impact", "slippage", "amihud",
            "illiquidity", "volume_weighted", "dollar_volume",
        ],
        "weight": 0.95,
        "description": "流动性类：成交量、换手率、买卖价差",
    },
    "event": {
        "keywords": [
            "earnings", "dividend", "split", "insider", "acquisition",
            "merger", "buyback", "ipo", "seo", "announcement",
            "guidance", "conference", "call", "meeting", "event",
        ],
        "weight": 1.1,
        "description": "事件类：财报、分红、拆股、内部人交易、并购",
    },
    "macro": {
        "keywords": [
            "macro", "economic", "gdp", "inflation", "interest", "rate",
            "monetary", "fiscal", "policy", "central_bank", "yield_curve",
            "bond", "treasury", "currency", "fx", "exchange_rate",
        ],
        "weight": 0.85,
        "description": "宏观类：经济指标、利率、汇率、政策",
    },
    "analyst": {
        "keywords": [
            "analyst", "estimate", "revision", "forecast", "consensus",
            "target_price", "rating", "upgrade", "downgrade", "recommendation",
            "eps_estimate", "revenue_estimate", "ebitda_estimate",
        ],
        "weight": 1.15,
        "description": "分析师类：盈利预测、评级修正、目标价",
    },
    "fundamental": {
        "keywords": [
            "fundamental", "financial", "balance_sheet", "income_statement",
            "cash_flow", "assets", "liabilities", "equity", "revenue",
            "income", "expense", "cost", "profit", "earnings",
        ],
        "weight": 1.0,
        "description": "基本面类：财务报表科目、资产负债、收入支出",
    },
}

# 类别优先级（用于字段池构建时的排序）
CATEGORY_PRIORITY = [
    "analyst", "value", "quality", "growth", "event", "sentiment",
    "momentum", "risk", "liquidity", "fundamental", "size", "macro",
]


def _normalize_text(text: str) -> str:
    """标准化文本用于关键词匹配。"""
    return re.sub(r"[^a-z0-9]+", "_", str(text).lower()).strip("_")


def classify_field(field: Dict[str, Any]) -> List[Tuple[str, float]]:
    """对单个字段做经济学含义归类。

    返回 [(类别, 置信度), ...]，按置信度降序。置信度 = 匹配关键词数 / 该类总关键词数。
    """
    name = str(field.get("id") or field.get("field_name") or field.get("name") or "")
    desc = str(field.get("description") or "")
    text = _normalize_text(name + " " + desc)

    scores: List[Tuple[str, float]] = []
    for cat, info in ECONOMIC_CATEGORIES.items():
        keywords = info["keywords"]
        matched = sum(1 for kw in keywords if kw in text)
        if matched > 0:
            confidence = matched / len(keywords)
            # 名称匹配权重高于描述匹配
            name_matched = sum(1 for kw in keywords if kw in _normalize_text(name))
            if name_matched > 0:
                confidence *= 1.5
            scores.append((cat, min(confidence, 1.0)))

    scores.sort(key=lambda x: -x[1])
    return scores


def classify_fields(fields: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
    """对字段列表做经济学含义聚类。

    返回 {类别: [字段列表]}，每类内按质量评分降序。
    """
    from ._field_catalog import FieldCatalogMixin  # 避免循环导入

    clusters: Dict[str, List[Dict[str, Any]]] = {}
    for field in fields:
        name = FieldCatalogMixin._field_name(field)
        if not name:
            continue
        scores = classify_field(field)
        if not scores:
            # 未匹配到任何类别 → 归入 "other"
            clusters.setdefault("other", []).append(field)
            continue
        # 取最高置信度类别
        best_cat = scores[0][0]
        field["_economic_category"] = best_cat
        field["_economic_confidence"] = scores[0][1]
        field["_economic_all"] = scores
        clusters.setdefault(best_cat, []).append(field)

    # 每类内按质量评分降序
    for cat in clusters:
        clusters[cat].sort(key=lambda f: FieldCatalogMixin._quality_score(f), reverse=True)

    return clusters


def build_economic_field_pool(
    fields: List[Dict[str, Any]],
    max_fields: int = 30,
    min_per_category: int = 2,
    max_per_category: int = 8,
) -> Tuple[List[str], Dict[str, Any]]:
    """按经济学含义构建字段池。

    策略：
    1. 按经济学含义聚类
    2. 每类按质量评分取 top-k（min_per_category ~ max_per_category）
    3. 按类别优先级轮转，保证跨类别多样性
    4. 返回 (字段名列表, 聚类统计)

    与旧 _pick_cross_cluster 的区别：
    - 旧：按"主体 token"分簇（mean_ask_price → ask），无经济学含义
    - 新：按经济学类别分簇（value/growth/quality/...），有经济学约束
    """
    from ._field_catalog import FieldCatalogMixin

    clusters = classify_fields(fields)
    if not clusters:
        return [], {"error": "no fields classified"}

    # 计算每类应取数量（按类别优先级和质量分布）
    total_quality = sum(
        sum(FieldCatalogMixin._quality_score(f) for f in fields)
        for fields in clusters.values()
    )
    if total_quality == 0:
        total_quality = 1

    pool: List[str] = []
    seen = set()
    stats: Dict[str, Any] = {
        "total_fields": len(fields),
        "categories": {},
        "pool_size": 0,
    }

    # 第一轮：每类取 min_per_category（保证覆盖）
    for cat in CATEGORY_PRIORITY:
        if cat not in clusters:
            continue
        cat_fields = clusters[cat]
        taken = 0
        for f in cat_fields:
            name = FieldCatalogMixin._field_name(f)
            if name and name not in seen and taken < min_per_category:
                seen.add(name)
                pool.append(name)
                taken += 1
        stats["categories"][cat] = {
            "total": len(cat_fields),
            "taken": taken,
            "top_quality": FieldCatalogMixin._quality_score(cat_fields[0]) if cat_fields else 0,
        }

    # 第二轮：按类别优先级和质量补齐到 max_fields
    for cat in CATEGORY_PRIORITY:
        if len(pool) >= max_fields:
            break
        if cat not in clusters:
            continue
        cat_fields = clusters[cat]
        current_taken = stats["categories"].get(cat, {}).get("taken", 0)
        max_take = min(max_per_category, len(cat_fields))
        for f in cat_fields:
            if len(pool) >= max_fields:
                break
            name = FieldCatalogMixin._field_name(f)
            if name and name not in seen and current_taken < max_take:
                seen.add(name)
                pool.append(name)
                current_taken += 1
        stats["categories"][cat]["taken"] = current_taken

    # 处理未匹配的 "other" 类
    if "other" in clusters and len(pool) < max_fields:
        for f in clusters["other"]:
            if len(pool) >= max_fields:
                break
            name = FieldCatalogMixin._field_name(f)
            if name and name not in seen:
                seen.add(name)
                pool.append(name)
        stats["categories"]["other"] = {
            "total": len(clusters["other"]),
            "taken": sum(1 for f in clusters["other"] if FieldCatalogMixin._field_name(f) in seen),
            "top_quality": FieldCatalogMixin._quality_score(clusters["other"][0]) if clusters["other"] else 0,
        }

    stats["pool_size"] = len(pool)
    stats["categories_covered"] = len([c for c in stats["categories"] if stats["categories"][c]["taken"] > 0])
    return pool, stats


def generate_economic_concepts(
    clusters: Dict[str, List[Dict[str, Any]]],
    max_concepts: int = 10,
) -> List[Dict[str, Any]]:
    """基于经济学聚类生成概念模板。

    每对类别组合生成一个概念：
    - value × growth: 低估值高增长（GARP）
    - quality × momentum: 高质量动量
    - sentiment × event: 情绪驱动事件
    - ...

    返回 [{concept, categories, fields, rationale}, ...]
    """
    concepts: List[Dict[str, Any]] = []

    # 预定义高价值类别对
    high_value_pairs = [
        ("value", "growth", "GARP：低估值高增长"),
        ("quality", "momentum", "高质量动量：盈利能力强且趋势向上"),
        ("analyst", "value", "分析师低估：评级上修但估值仍低"),
        ("event", "sentiment", "事件驱动情绪：并购/财报引发的情绪变化"),
        ("risk", "value", "风险调整价值：低波动低估值"),
        ("liquidity", "momentum", "流动性动量：高换手趋势延续"),
        ("size", "value", "小盘价值：规模因子与价值因子交互"),
        ("quality", "event", "质量事件：高质量公司财报超预期"),
        ("growth", "sentiment", "成长情绪：高增长伴随情绪升温"),
        ("macro", "value", "宏观价值：利率周期中的估值修复"),
    ]

    for cat1, cat2, rationale in high_value_pairs:
        if len(concepts) >= max_concepts:
            break
        if cat1 not in clusters or cat2 not in clusters:
            continue
        fields1 = [f for f in clusters[cat1][:3]]  # 每类取 top3
        fields2 = [f for f in clusters[cat2][:3]]
        if not fields1 or not fields2:
            continue
        concepts.append({
            "concept": f"{cat1}_x_{cat2}",
            "categories": [cat1, cat2],
            "fields": [f.get("id") or f.get("field_name") for f in fields1 + fields2],
            "rationale": rationale,
            "field_count": len(fields1) + len(fields2),
        })

    return concepts
