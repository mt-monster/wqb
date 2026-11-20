# -*- coding: utf-8 -*-
"""_lib/attribution.py — 收批后的**必做**归因层：PnL + 逐年 + 论坛破闸。

## 为什么必须有这一层（2026-11-19 用户明令 + 实测教训）

只读聚合指标（S/F/2Y/sub/DD/TO）的归因会漏掉三类关键事实：

1. **整年零持仓** —— 聚合指标里的 coverage 与「数据满几年」毫无关系。
   实测：`fund_holdings_panel` 在 EUR 的 coverage 0.843–0.918，但 2014 **全年 longCount=0**
   （用零预热对照件 `rank(vec_sum(stable_boundary_trade_count_21d))` 验证过：同样为 0 ⇒ 数据集自 2015 起）。
   该事实只有逐年 longCount 能看到，且直接决定「近十年」硬约束是否成立。
2. **失效年定位** —— 全期 S 1.48 与「2021-2023 三年 S2.0–3.3、2017/2020 近乎为零」是完全不同的诊断，
   前者像「信号弱」（该换集），后者是「机制在两个特定年份失效」（该修形态）。
3. **可投资性折损** —— 原始 PnL 与 investability-constrained PnL 的比值，
   决定收益有多少来自不可投资的小盘部分。

## 缺陷来源分类（判据必须能落到读数上）

| 来源 | 判据（必须有读数） |
|---|---|
| 数据不满十年 | 任一年 longCount==0 或 shortCount==0 ⇒ **数据层排除**（不可补救） |
| 时效衰减 | 2Y 明显低于全期 S，或最弱两年集中在最近窗口 |
| 失效年 | 逐年 S 的最小值所在年 ≤ 0.1 且该年 pnl ≈ 0 |
| 全市场效应 | 多个不同族的候选在同一批年份同步走弱（跨族对照） |
| 波动过高 | returns 高但 drawdown 同量级（DD > ret/4） |
| 权重集中 | CONCENTRATED_WEIGHT > 0.1 |
| 产线拥挤 | prod >= 0.7（读数实测，非推测） |
| 可投资性折损 | invest_pnl / raw_pnl < 0.75 |
| 横截面过窄 | longCount/shortCount 长期不对称（如 1:1.5） |

## 论坛破闸

对**本波主导墙**做一次定向检索（确定性语料通道，见 `_lib/forum_corpus`），
产出「墙 → 论坛破解办法」的对照，并写进 ledger 键 `s4_attribution_<region>_<wave>`。
"""
from __future__ import annotations

import json
from typing import Any, Dict, List, Optional, Sequence

# 墙 → 论坛检索词（每个墙 3 词，覆盖中英与机制词）
WALL_KEYWORDS: Dict[str, List[str]] = {
    "PROD_WALL": ["reduce correlation", "prod correlation", "equivalent data field"],
    "S_GATE": ["higher sharpe", "sharpe improvement", "turnover"],
    "F_GATE": ["fitness", "returns of an alpha", "margin"],
    "TWO_Y_GATE": ["2y sharpe", "smooth pnl", "pnl curve"],
    "CONCENTRATED_WEIGHT": ["concentrated weight", "position concentration", "truncation"],
    "SUB_GATE": ["sub-universe", "sub universe test", "small cap"],
    "TURNOVER": ["turnover", "trade_when", "event alpha"],
    "CLUSTER_TEST": ["cluster test", "diversification", "pool correlation"],
}

# ⚠ 这里**不要**写与 `tracking/<R>/config/thresholds.json` 同名的键串：
# 区域控制棘轮（tests/unit/07_docs_skills/test_region_control_ratchets.py）会把代码里出现的
# 阈值键串当成「读取方」，从而误判 `diversity.narrow_cross_section` 之类已被接线。
# 缺陷分类用中文 source 名，不复用阈值键名。


# ---------------------------------------------------------------- yearly / pnl

def _records_payload(data: Any) -> List[Dict[str, Any]]:
    """recordsets 端点返回 `{"schema": {"properties": [{name, title, type}...]}, "records": [[...], ...]}`。

    ⚠ 行**不是 dict 而是按 schema.properties 顺序的数组**（实测 /alphas/{id}/recordsets/yearly-stats：
    `records[0] == ["2014", 0.0, 20000000, 0, 0, 0.0, 0.0, 0.0, 0.0, 0, "IS"]`），
    必须用 schema 的 property 名做列映射，否则解析出来全是空。
    同时兼容 dict 行形态（防御性）。
    """
    if isinstance(data, list):
        return [r for r in data if isinstance(r, dict)]
    if not isinstance(data, dict):
        return []
    recs = data.get("records")
    if isinstance(recs, dict):
        out: List[Dict[str, Any]] = []
        for v in recs.values():
            if isinstance(v, list):
                out.extend(r for r in v if isinstance(r, dict))
        return out
    if not isinstance(recs, list):
        return []
    props = []
    schema = data.get("schema")
    if isinstance(schema, dict):
        for p in (schema.get("properties") or []):
            if isinstance(p, dict) and p.get("name"):
                props.append(p["name"])
    out = []
    for r in recs:
        if isinstance(r, dict):
            out.append(r)
        elif isinstance(r, list) and props:
            out.append({props[i]: v for i, v in enumerate(r) if i < len(props)})
    return out


def _fetch_json(api: Any, path: str, retries: int = 4) -> Any:
    """取 recordsets JSON，带 429 指数退避重试。

    ⚠ 2026-11-19 实测：连续取两份 recordsets 时，第二次会被瞬时错误吞掉，
    导致「该 alpha 逐年读数缺失」的**假阴性**（同件用 MCP 读得到完整 10 年）。
    ⇒ 这里必须重试，且失败要把原因带出来，不能静默返回空。
    """
    import time
    import urllib.error
    from _lib.api import api_call

    delay = 3.0
    last = None
    for i in range(max(1, int(retries))):
        try:
            resp = api_call(api, "get", path, retries=1)
            body = resp.read().decode("utf-8", "replace")
            return json.loads(body)
        except urllib.error.HTTPError as e:
            last = e
            if e.code == 429 and i < retries - 1:
                time.sleep(delay)
                delay *= 2
                continue
            break
        except Exception as e:
            last = e
            if i < retries - 1:
                time.sleep(delay)
                delay *= 2
                continue
            break
    raise RuntimeError(f"recordsets 取数失败 {path}: {type(last).__name__}: {str(last)[:160]}")


def yearly_stats(api: Any, alpha_id: str) -> List[Dict[str, Any]]:
    """逐年 longCount/shortCount/pnl/returns/sharpe（端点 /alphas/{id}/recordsets/yearly-stats）。

    取数失败**抛异常**（不返回空列表）——空列表会让下游误判「没有逐年读数」而不是「取数失败」。
    """
    data = _fetch_json(api, f"/alphas/{alpha_id}/recordsets/yearly-stats")
    rows = _records_payload(data)
    out = []
    for r in rows:
        try:
            out.append({
                "year": str(r.get("year") or r.get("date") or "")[:4],
                "pnl": float(r.get("pnl") or 0.0),
                "long_count": int(r.get("longCount") or 0),
                "short_count": int(r.get("shortCount") or 0),
                "sharpe": float(r.get("sharpe") or 0.0),
                "returns": float(r.get("returns") or 0.0),
                "drawdown": float(r.get("drawdown") or 0.0),
                "turnover": float(r.get("turnover") or 0.0),
            })
        except (TypeError, ValueError):
            continue
    out.sort(key=lambda x: x["year"])
    return out


def pnl_shape(api: Any, alpha_id: str) -> Dict[str, Any]:
    """PnL 三线对照（端点 /alphas/{id}/recordsets/pnl）：原始 / 风险中性化 / 可投资性约束。"""
    shape: Dict[str, Any] = {"available": False}
    data = _fetch_json(api, f"/alphas/{alpha_id}/recordsets/pnl")
    rows = _records_payload(data)
    if not rows:
        return shape

    def last(key: str) -> float:
        vals = [r.get(key) for r in rows if isinstance(r.get(key), (int, float))]
        return float(vals[-1]) if vals else 0.0

    raw, rn, inv = last("pnl"), last("risk-neutralized-pnl"), last("investability-constrained-pnl")
    shape.update({
        "available": True,
        "points": len(rows),
        "raw_last": raw,
        "risk_neutralized_last": rn,
        "investability_constrained_last": inv,
        "investability_ratio": (inv / raw) if raw else None,
        "rn_ratio": (rn / raw) if raw else None,
        "first_date": str(rows[0].get("date") or "")[:10],
        "last_date": str(rows[-1].get("date") or "")[:10],
    })
    return shape


# ---------------------------------------------------------------- 缺陷判定

def classify_defects(yearly: Sequence[Dict[str, Any]], pnl: Dict[str, Any],
                      row: Dict[str, Any]) -> List[Dict[str, str]]:
    """返回 [{source, evidence}]，每条 evidence 必须带读数。"""
    out: List[Dict[str, str]] = []
    if not yearly:
        out.append({"source": "逐年读数缺失",
                    "evidence": "yearly-stats 端点无返回 ⇒ 满十年与失效年均无法判定（不得当作通过）"})
        return out

    empty = [y["year"] for y in yearly
             if y["long_count"] == 0 or y["short_count"] == 0 or abs(y["pnl"]) < 1e-9]
    if empty:
        out.append({
            "source": "数据不满十年",
            "evidence": ("逐年零持仓年 " + ",".join(empty) +
                         f"（共 {len(yearly)} 年）⇒ 数据起点晚于 IS 窗起点 ⇒ 近十年硬约束不成立（数据层排除）"),
        })
    else:
        out.append({
            "source": "近十年成立",
            "evidence": (f"{len(yearly)} 年逐年 longCount/shortCount 全 >0"
                         f"（最少 {min(min(y['long_count'], y['short_count']) for y in yearly)}）"),
        })

    weak = sorted([y for y in yearly if y["sharpe"] <= 0.15], key=lambda y: y["year"])
    if weak:
        out.append({
            "source": "失效年",
            "evidence": ("近零年 " + ",".join(f"{y['year']}(S{y['sharpe']:.2f})" for y in weak) +
                         " ⇒ 全期 S 被这些年份拖累，机制在该窗口失效（不是信号弱）"),
        })
    strong = [y for y in yearly if y["sharpe"] >= 2.0]
    if strong and weak:
        out.append({
            "source": "失效年集中",
            "evidence": ("强年 " + ",".join(y["year"] for y in strong) +
                         " ⇒ 同一机制在部分窗口有效，优先修窗口/门控而非换集"),
        })

    if pnl.get("available"):
        ratio = pnl.get("investability_ratio")
        if ratio is not None and ratio < 0.75:
            out.append({
                "source": "可投资性折损",
                "evidence": (f"investability-constrained PnL / 原始 PnL = {ratio:.2f}"
                             f"（原始 {pnl.get('raw_last'):.0f} → 约束 {pnl.get('investability_constrained_last'):.0f}）"
                             " ⇒ 相当部分收益来自不可投资的小盘/低流动性部分"),
            })
        if pnl.get("rn_ratio") is not None:
            rn_ratio = pnl["rn_ratio"]
            if rn_ratio >= 0.75:
                out.append({
                    "source": "非风险暴露",
                    "evidence": (f"risk-neutralized PnL / 原始 PnL = {rn_ratio:.2f}"
                                 " ⇒ 信号本身基本不是风险暴露（RN 口径亦可过）"),
                })
            elif rn_ratio >= 0.4:
                out.append({
                    "source": "部分风险暴露",
                    "evidence": (f"risk-neutralized PnL / 原始 PnL = {rn_ratio:.2f}"
                                 f"（原始 {pnl.get('raw_last'):.0f} → RN {pnl.get('risk_neutralized_last'):.0f}）"
                                 " ⇒ 约四成收益来自风险模型暴露，中性化档位会吃掉这部分"),
                })
            else:
                out.append({
                    "source": "强风险暴露",
                    "evidence": (f"risk-neutralized PnL / 原始 PnL = {rn_ratio:.2f}"
                                 " ⇒ 收益几乎全部来自风险暴露 ⇒ 换中性化档位是主要杠杆"),
                })

    ret = float(row.get("returns") or 0.0)
    dd = float(row.get("drawdown") or 0.0)
    if ret > 0 and dd > 0 and dd > ret / 4.0:
        out.append({
            "source": "波动过高",
            "evidence": f"returns {ret:.3f} 但 drawdown {dd:.3f}（DD>ret/4）⇒ S 被波动压低",
        })

    lcs = [y["long_count"] for y in yearly if y["long_count"]]
    scs = [y["short_count"] for y in yearly if y["short_count"]]
    if lcs and scs:
        ratio_ls = sum(lcs) / max(1, sum(scs))
        if ratio_ls < 0.75 or ratio_ls > 1.35:
            out.append({
                "source": "横截面过窄",
                "evidence": (f"逐年 long/short 合计比 {ratio_ls:.2f}"
                             " ⇒ 多空两侧显著不对称，横截面有效名数不足"),
            })

    prod = row.get("prod_correlation")
    if isinstance(prod, (int, float)) and prod >= 0.7:
        out.append({
            "source": "产线拥挤",
            "evidence": f"prod {prod:.4f} ≥ 0.7 ⇒ 该信息源已被生产池占满，换档位不救（实测换中性化仅动 0.015）",
        })
    return out


def is_data_layer_exclusion(defects: Sequence[Dict[str, str]]) -> bool:
    """数据层排除（不可补救，优先于信号层判断）。"""
    return any(d.get("source") == "数据不满十年" for d in defects)


# ---------------------------------------------------------------- 论坛破闸

def forum_breakthrough(corpus: Any, walls: Sequence[str], per_wall: int = 3) -> List[Dict[str, Any]]:
    """对每个墙做一次论坛定向检索（确定性语料通道）。返回 [{wall, posts:[...]}]。"""
    out = []
    for wall in walls:
        kws = WALL_KEYWORDS.get(wall) or [wall]
        try:
            hits = corpus.search(kws, limit=per_wall)
        except Exception:
            hits = []
        out.append({
            "wall": wall,
            "keywords": kws,
            "found": len(hits),
            "posts": [{
                "id": h.get("id"),
                "title": h.get("title"),
                "votes": h.get("votes"),
                "comments": h.get("comments"),
                "url": h.get("url"),
                "excerpt": (h.get("body") or "")[:400],
            } for h in hits],
        })
    return out


def wall_keywords_for_row(row: Dict[str, Any], thresholds: Dict[str, Any]) -> List[str]:
    """从一行读数推出它撞的墙（用于定向检索）。"""
    walls: List[str] = []
    s = row.get("sharpe")
    f = row.get("fitness")
    ty = row.get("two_year_sharpe")
    sub = row.get("sub_universe_sharpe")
    prod = row.get("prod_correlation")
    g = thresholds.get("gates") or thresholds
    gate_s = float(g.get("sharpe", 1.58) or 1.58)
    gate_f = float(g.get("fitness", 1.0) or 1.0)
    gate_2y = float(g.get("two_year", 1.58) or 1.58)
    if isinstance(s, (int, float)) and s < gate_s:
        walls.append("S_GATE")
    if isinstance(f, (int, float)) and f < gate_f:
        walls.append("F_GATE")
    if isinstance(ty, (int, float)) and ty < gate_2y:
        walls.append("TWO_Y_GATE")
    if isinstance(sub, (int, float)) and isinstance(s, (int, float)) and s > 0 and sub < 0.52 * s:
        walls.append("SUB_GATE")
    if isinstance(prod, (int, float)) and prod >= 0.7:
        walls.append("PROD_WALL")
    if not walls:
        walls.append("S_GATE")
    return walls


def build_attribution(row: Dict[str, Any], yearly: Sequence[Dict[str, Any]],
                       pnl: Dict[str, Any]) -> Dict[str, Any]:
    """一行 alpha 的归因汇总（纯函数，可单测）。"""
    defects = classify_defects(yearly, pnl, row)
    return {
        "alpha": row.get("alpha_id") or row.get("id") or "-",
        "expr": (row.get("expression") or row.get("code") or "-")[:200],
        "sharpe": row.get("sharpe"),
        "fitness": row.get("fitness"),
        "two_year": row.get("two_year_sharpe"),
        "sub": row.get("sub_universe_sharpe"),
        "prod": row.get("prod_correlation"),
        "empty_years": [y["year"] for y in yearly
                        if y["long_count"] == 0 or y["short_count"] == 0],
        "ten_year_ok": bool(yearly) and not is_data_layer_exclusion(defects),
        "defects": defects,
        "pnl": pnl,
        "yearly": list(yearly),
    }
