#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""field_semantic_classify.py — 数据集字段的经济含义归类（S1 补做环节）。

背景（2026-09-28 KOR/fundamental17 实证）：
  步 3 只做了 scan_fields（typed catalog = 类型/覆盖/users），**没做语义归类**，
  直接进 GEM。结果 348 条产物里 49.4% 落在「货币代码 / 汇率叉乘」这类
  **非信号字段**上（三角套汇恒等式、字符串分类码），71% 是废产物。
  typed catalog 只回答「这字段是什么类型、覆盖多少」，不回答
  「这字段能不能当信号」——后者必须由语义归类给出。

用途：
  1. 产出**信号字段白名单 / 非信号黑名单**（供 GEM 字段池约束、表达式过滤）；
  2. 按经济大类分桶，供后续「每类至少N槽」的多样性配给；
  3. ⚠ 产出是**字段池**，不是 ideas —— 禁止当 ideas.md 注入 GEM
     （SOP 2026-09-17 P3-11：确定性模板渲染会让 GEM 退化为「每字段套 rank」）。

用法:
    python tools/field_semantic_classify.py --region KOR --dataset fundamental17
    python tools/field_semantic_classify.py --region KOR --dataset fundamental17 --write-ledger

运行环境: 任意 Python（只读 DB；--write-ledger 时写库走规范工厂）。
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from wqb.db_conn import connect as db_connect  # 规范工厂（禁裸 sqlite3.connect）


# 非信号字段：标识符 / 分类码 / 标签 / 汇率换算 / 计数口径 —— 无论覆盖多高都不得当信号输入
#
# ⚠ 2026-09-28 修复（重要）：原规则里 `is_` / `_flag$` 用**未锚定的名字子串**匹配，
# 结果把 `oth466_is_ebit_oper_q`（**Income Statement** EBIT，users=248）这类字段当
# 「布尔标志位」误杀 —— other466 上 39/177（22%）被误判，且被杀的恰是 users 最高的
# 利润表核心字段。教训：**缩写歧义（is = Income Statement vs is_ 标志）不能靠名字判，
# 必须看描述文**。故标志位/分类码改由 `desc` 判定；名字规则只保留无歧义的强标识符。
NON_SIGNAL_PATTERNS = [
    (r"currency_code|cur_code", "货币/报表币种代码"),
    (r"^fnd17_\d+_(usdtorep|reptoprc|repto|ustorep)", "汇率换算（叉乘多为恒等式）"),
    (r"exrate|exchange_rate", "汇率（叉乘多为恒等式）"),
    (r"^fx_|_fx_|_fx$", "汇率（叉乘多为恒等式）"),
    (r"gvkey|cusip|isin|sedol|ticker|iso_country|country_code|exchange_code|region_code",
     "标识符/国别交易所代码"),
    (r"fiscal_year_end|report_date|period_end|_date$|_dt$", "日期/期间口径"),
    (r"shares_outstanding_class|_share_class_", "股份类别标签"),
]

# 描述文驱动的非信号判定：布尔标志 / 分类标签 / 纯代码（名字规则无法可靠识别时用）
#
# ⚠ 2026-09-28 第二次修复：初版用裸 `\bindicator\b` / `\bflag\b` / `whether`，
# 把「技术分析指标」也误杀 —— model109 的 Bollinger Bands / Negative Volume Index /
# **Altman Z-score** / Chaikin Money Flow / Money Flow Index / Stochastic Oscillator
# 描述里都含 "indicator"，51/539 被误判为布尔标志。
# 正解：**必须出现显式布尔措辞**（"indicator denoting whether"、"equals 1"、
# "dummy variable"、"1 if ... 0 otherwise"），仅出现 indicator/flag 名词不算。
NON_SIGNAL_DESC_PATTERNS = [
    (r"indicator\s+(?:denoting|indicating|that indicates|for)\s+whether|"
     r"flag\s+(?:showing|denoting|indicating|that indicates)\s+whether|"
     r"denotes?\s+whether|"
     r"whether\s+[^.]{0,80}?\b(?:equals?|is)\s+1\b|"
     r"\bdummy\s+variable\b|\bindicator\s+variable\b|\bbinary\s+(?:variable|flag)\b|"
     r"\b1\s+if\b[^.]{0,80}?\b0\s+otherwise\b",
     "布尔标志/指示变量（描述文判定）"),
    (r"three[- ]letter\s+iso\s+(?:currency|country)\s+code|\biso\s+(?:currency|country)\s+code\b|"
     r"compustat\s+global\s+company\s+identifier|\bcompany\s+identifier\b",
     "分类码/标识符（描述文判定）"),
]

# 经济大类（按描述关键词命中，顺序 = 优先级）
ECON_CATEGORIES = [
    ("valuation", r"price[- ]to[- ]|enterprise value|market cap|ev[ /_]|p/[esb]|yield|multiple|ratio of .* to price", "估值倍数"),
    ("profitability", r"margin|return on|roe|roa|roic|roi|profit|ebit|ebitda|net income|earnings per|eps|operating income", "盈利能力"),
    ("growth", r"growth|cagr|trend|percent change|change in .* versus|year[- ]over[- ]year|yoy|qoq", "成长/趋势"),
    ("cash_quality", r"cash flow|free cash|fcf|accrual|cash conversion|cfo", "现金流质量"),
    ("leverage_solvency", r"debt|leverage|solvency|coverage|interest expense|current ratio|quick ratio|debt[- ]to[- ]", "偿债/杠杆"),
    ("efficiency", r"turnover|asset use|inventory|receivable|days (sales|payable|inventory)|working capital", "运营效率"),
    ("liquidity_risk", r"beta|volatility|volume as|liquidity|trading volume", "流动性/风险"),
    ("size_level", r"total assets|revenue|sales|book value|equity|shares outstanding|market value", "规模/水平"),
    ("per_share", r"per share|per[- ]share|/share", "每股口径"),
    ("dividend", r"dividend|payout|buyback|repurchase", "分红/回购"),
]


def classify(desc: str, name: str):
    d = (desc or "").lower()
    n = (name or "").lower()
    for pat, why in NON_SIGNAL_PATTERNS:
        if re.search(pat, n):
            return None, f"非信号：{why}"
    # 描述文驱动的标志位/分类码判定（名字规则无法可靠区分 is=Income Statement 等歧义缩写）
    for pat, why in NON_SIGNAL_DESC_PATTERNS:
        if re.search(pat, d):
            return None, f"非信号：{why}"
    for cat, pat, label in ECON_CATEGORIES:
        if re.search(pat, d):
            return cat, label
    return "other", "未归类"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--region", required=True)
    ap.add_argument("--dataset", required=True)
    ap.add_argument("--write-ledger", action="store_true")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()

    conn = db_connect(readonly=True)
    rows = conn.execute(
        """SELECT f.field_name, f.field_type, f.coverage, f.user_count, f.alpha_count, f.description
           FROM fields f JOIN datasets d ON d.id=f.dataset_id
           WHERE d.name=? AND d.region_id=(SELECT id FROM regions WHERE name=?)
           ORDER BY COALESCE(f.alpha_count,0) DESC, COALESCE(f.user_count,0) DESC""",
        (args.dataset, args.region),
    ).fetchall()
    conn.close()
    if not rows:
        print(f"[WARN] 无字段：{args.region}/{args.dataset}")
        return 1

    signal, blocked = [], []
    by_cat = defaultdict(list)
    for name, ftype, cov, users, ac, desc in rows:
        cat, label = classify(desc, name)
        item = {"field": name, "cat": cat, "label": label, "type": ftype,
                "cov": round(cov, 4) if cov is not None else None,
                "users": users if users is not None else 0,
                "alpha_count": ac if ac is not None else 0,
                "desc": (desc or "")[:110]}
        if cat is None:
            blocked.append(item)
        else:
            signal.append(item)
            by_cat[cat].append(item)

    n = len(rows)
    print(f"\n=== {args.region}/{args.dataset} 字段经济归类（共 {n}）===")
    print(f"信号字段 {len(signal)} ({100*len(signal)/n:.1f}%)  |  非信号黑名单 {len(blocked)} ({100*len(blocked)/n:.1f}%)")
    print("\n-- 经济大类分布（信号字段）--")
    for cat, items in sorted(by_cat.items(), key=lambda kv: -len(kv[1])):
        cold = sum(1 for i in items if i["users"] <= 9)
        print(f"  {cat:<18} {len(items):>4}  (冷门 users<=9: {cold:>3}, {100*cold/len(items):.0f}%)")
    print("\n-- 非信号黑名单（不得当信号输入）--")
    for why in sorted({i["label"] for i in blocked}):
        sub = [i for i in blocked if i["label"] == why]
        print(f"  {why:<28} {len(sub):>3}  例: {', '.join(i['field'] for i in sub[:3])}")

    out = {
        "region": args.region, "dataset": args.dataset, "total_fields": n,
        "signal_field_count": len(signal),
        "blocked_field_count": len(blocked),
        "signal_fields": [i["field"] for i in signal],
        "blocked_fields": [{"field": i["field"], "reason": i["label"]} for i in blocked],
        "by_category": {k: [i["field"] for i in v] for k, v in by_cat.items()},
        "category_stats": {k: {"n": len(v), "cold_users_le_9": sum(1 for i in v if i["users"] <= 9)}
                           for k, v in by_cat.items()},
        "note": "产出是字段池（field pool），不是 ideas —— 禁止当 ideas.md 注入 GEM（SOP 2026-09-17 P3-11）",
    }
    p = args.out or f"cache/{args.region.lower()}_{args.dataset}_semantic.json"
    Path(p).write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n[写出] {p}")

    if args.write_ledger:
        key = f"s1_semantic_{args.dataset}"
        conn = db_connect()
        try:
            import datetime
            now = datetime.datetime.now().isoformat(timespec="seconds")
            v = json.dumps(out, ensure_ascii=False)
            r = conn.execute("SELECT id FROM ledger_kv WHERE region=? AND key=?", (args.region, key)).fetchone()
            if r:
                conn.execute("UPDATE ledger_kv SET value=?, updated_at=? WHERE id=?", (v, now, r[0]))
            else:
                conn.execute("INSERT INTO ledger_kv(region,key,value,created_at,updated_at) VALUES(?,?,?,?,?)",
                             (args.region, key, v, now, now))
            conn.commit()
            print(f"[ledger] {args.region}/{key}")
        finally:
            conn.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
