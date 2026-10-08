# -*- coding: utf-8 -*-
"""field_semantic_type.py — 基于 **description** 的字段语义类型分类（GBR/全区通用）。

定位（2026-10-08，用户指令「用 description 确认语义的方式重新做字段画像」）：
    `field_profile.py` 的 verdict 只回答「这个字段测出来强不强」；
    本工具回答「这个字段**是什么量**」—— 且**以 description 为准，名字只作对照**。
    两者交叉才能给出正确的「机制 → 骨架」建议。

产物：表 `field_semantic_type`（主键 region+dataset+field）
      列：sem_type / evidence / name_guess / conflict / weightlessness

用法：
    python tools/fields/field_semantic_type.py --build --region GBR
    python tools/fields/field_semantic_type.py --report --region GBR
    python tools/fields/field_semantic_type.py --report --region GBR --dataset analyst7
"""
from __future__ import annotations

import argparse
import collections
import os
import re
import sqlite3
import sys
from typing import Dict, List, Optional, Tuple

_REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if _REPO not in sys.path:
    sys.path.insert(0, _REPO)
# ★ 走 wqb.db_conn（唯一规范连接工厂：WAL / busy_timeout / foreign_keys / synchronous
#   pragma 都在这里），**禁止裸 sqlite3.connect** —— 由
#   tests/unit/01_store_db/test_db_write_guards.py::TestNoNakedSqliteConnect 白名单守卫。
if os.path.join(_REPO, "src") not in sys.path:
    sys.path.insert(0, os.path.join(_REPO, "src"))
from wqb.db_conn import connect as _db_connect  # noqa: E402

TABLE = "field_semantic_type"

# ── description 优先的语义类型规则（顺序即优先级）────────────────────────
# 每条: (sem_type, 正则, 骨架建议)
RULES: List[Tuple[str, str, str]] = [
    # ① 非信号类（先排除，避免被后面的通用词误吸）
    ("temporal_meta", r"(utc|timestamp|date when|start time|end time|reporting (start|end) time|"
                      r"record date|reference date|collection timestamp|milliseconds elapsed|"
                      r"elapsed between|time of day|was announced)", "禁用（时间元数据）"),
    ("identifier", r"(iso[- ]?3166|country code|currency code|ticker|identifier|\bid of\b|"
                   r"return code|sequence number|numeric code representing|\bcode\b)", "禁用（标识/代码）"),
    ("text", r"(headline|summary text|short text|\btext of the\b|free text|article text)", "禁用（文本）"),
    ("cluster_label", r"(cluster assignment|grouping level|assignment label|statistical industry cluster|"
                      r"assign(ed|ment) .{0,24}(cluster|bucket))", "只作分组轴（GROUP/ bucket 包装）"),
    # ② 信号类
    ("probability", r"(probabilit|prob\b|odds|confidence level)", "比率型：rank/group_zscore 直用"),
    ("correlation", r"(correlation between|correlat)", "比率型：直用（勿再套 ts_zscore）"),
    ("dispersion", r"(standard deviation|volatilit|dispersion|coefficient of variation|"
                   r"range of values|kurtosis|skewness|variability)", "★比率型：divide(x, ts_mean(x)) 或 ts_std_dev"),
    ("novelty_time", r"(number of days since|days since|how new|\bnovelty\b|recency|age of the|"
                     r"time since|last observed|last change)", "★时效型：reverse(rank(ts_arg_max(x,w)))"),
    ("percentile", r"(percentile|quantile|decile|z-?score|zscore|standardized|"
                   r"\brank\s*\(?\s*1\s*[-–]\s*\d+|\b1\s*[-–]\s*100\b|\bpercentile rank\b)", "分位型：直用或 ts_quantile"),
    # ★ 2026-10-08 自我审查 #5 新增：技术指标（名字与描述最脱节的一类，必须按 description 认）
    ("indicator_name", r"(relative strength|\brsi\b|macd|williams\s*%?\s*r|chaikin|bollinger|"
                       r"stochastic|\batr\b|average true range|money flow index|\bmfi\b|\bcci\b|"
                       r"commodity channel|parabolic sar|\bobv\b|on[- ]balance volume|aroon|"
                       r"\bdpo\b|detrended price|keltner|donchian|ichimoku|\brtn\b|"
                       r"oscillator|momentum indicator|turnover ratio)", "技术指标：直用或先 rank（勿按名字猜语义）"),
    # ★ 自我审查 #5 新增：方向/增减（与 continuous 变化率区分）
    ("direction", r"(^|\b)(increase[sd]?|decrease[sd]?|upward|downward|rising|falling|\bhigher\b|\blower\b)", "方向型：rank 后直用（注意符号）"),
    ("ratio", r"(ratio|percentage|percent|per cent|fraction|share of|divided by|per share|"
              r"per unit|as a %|normalized|normalised|scaled|\bmargin\b|churn rate|expense ratio|"
              r"per available seat|\brate at which\b|calculated by dividing|\bmetric calculated\b)", "比率型：直用"),
    ("count", r"(number of|count of|\bcounts?\b|how many|breadth|number of analysts|"
              r"number of estimates|number of transactions|number of accounts)", "★计数型：先 group_neutralize 去共同成分，勿直接 ts_*"),
    ("sentiment", r"(sentiment|tone|polarity|positive or negative|classifier)", "情绪型：水平 → ts_delta/ts_rank"),
    ("revision_change", r"(revision|change in|revised|delta|difference|growth|momentum|trend|"
                        r"deteriorat|improv)", "变化型：ts_delta/ts_rank 直用"),
    ("score", r"(\bscore\b|\bindex\b|rating|rank(ing)?)", "分值型：水平 → rank 后直用"),
    ("estimate_level", r"(estimate of|analyst estimate|forecast of|consensus|"
                       r"expect(ed)?\s+(annual|forward|fiscal|\d|the\s+next))", "水平型：ts_delta 取修正"),
    ("level_amount", r"(dollar value|market value|\bamount\b|total value|in usd|\busd\b|\bprice\b|"
                      r"\bvalue\b|\bcapitalization\b)", "水平型：先 rank/scale 再直用"),
]

_COMPILED = [(t, re.compile(p, re.I), skel) for t, p, skel in RULES]

# ── 复合表述优先层（2026-10-08 自我审查 #2 新增）────────────────────────
# 问题：earliest-match 原则对**复合名词**失效 ——
#   "price-to-revenue ratio" 的主量词是 **ratio**（词尾），但 `level_amount` 的 `\bprice\b`
#   出现在句首 ⇒ 被判成 level_amount。实测 `predictive_starmine.smest_price_ratio_*` 全家 8 个
#   字段（含 4 个 ALIVE）被误判。
# 修法：先扫一遍「复合模式」，命中即返回，优先于单量词扫描。
COMPOUND_RULES: List[Tuple[str, str]] = [
    ("ratio", r"\b\w+[- ]to[- ]\w+\s+ratio|\b\w+\s*/\s*\w+\s+ratio|ratio of\b|"
              r"\b(price|pe|pb|ps|ev)[- ]to[- ]\w+|\bprice[- ]?(earnings|book|sales|revenue|"
              r"cash|ebitda|fcf)\b|\b\w+[- ]to[- ](earnings|ebitda|revenue|book|sales|equity)\b"),
    ("count", r"(number of|count of)\b"),
]
_COMPOUND = [(t, re.compile(p, re.I)) for t, p in COMPOUND_RULES]

# 名字侧的粗判（仅用于对照/报冲突，不参与决策）
NAME_GUESS = [
    ("count", re.compile(r"(raisednum|lowerednum|surprisenum|_num|count)", re.I)),
    ("percentile", re.compile(r"(rank|percentile|quantile|zscore|z_score)", re.I)),
    ("ratio", re.compile(r"(ratio|pct|percent|_per_|share)", re.I)),
    ("dispersion", re.compile(r"(std|stddev|vol|volatility|dispersion|kurtosis|skew)", re.I)),
    ("probability", re.compile(r"(prob|probability|confidence)", re.I)),
    ("temporal_meta", re.compile(r"(_date|_time|timestamp|utc)", re.I)),
    ("identifier", re.compile(r"(_id|_code|curcd|ticker)", re.I)),
]

#: 骨架建议表（sem_type → 建议构造；与 docs/reference 的「骨架-量类型匹配」同源）
SKELETON_HINT: Dict[str, str] = {t: s for t, _, s in RULES}
SKELETON_HINT["unknown"] = "无描述：先补 description 再判（勿按名字拍骨架）"


def _db() -> sqlite3.Connection:
    return _db_connect(os.path.join(_REPO, "data", "wqb.db"), row_factory=sqlite3.Row)


def classify(desc: Optional[str], fld: str) -> Tuple[str, str, Optional[str], bool]:
    """返回 (sem_type, evidence, name_guess, conflict)。

    ★ 判据原则（2026-10-08 自我审查后修正）：
      **以 description 中「最靠前的主量词」为准**，而不是固定规则优先级 ——
      因为英文描述的**主语量词通常在句首**（"Number of raised analyst estimates of GAAP
      earnings per share …" 的主量是「家数」，"per share" 只是被估计指标的单位）。
      旧实现按 RULES 顺序返回第一个命中，导致该例被 `ratio`(per share) 抢先误判为 ratio。
      现改为：所有规则都扫一遍，取 **match.start() 最小** 者；起点相同再按 RULES 顺序（=具体度）。
    """
    d = (desc or "").strip()
    name_guess = None
    for t, p in NAME_GUESS:
        if p.search(fld):
            name_guess = t
            break
    if not d:
        return "unknown", "(无 description)", name_guess, False
    # ① 复合表述优先（"X-to-Y ratio" / "Number of ..." 等主语量词在词尾/句首的复合名词）
    for t, p in _COMPOUND:
        m = p.search(d)
        if m:
            ev = d[max(0, m.start() - 20): m.end() + 26].replace("\n", " ").strip()
            return t, ev, name_guess, bool(name_guess and name_guess != t)
    # ② 单量词：取「最靠前」者
    best = None  # (start, rule_idx, sem_type, match)
    for i, (t, p, _skel) in enumerate(_COMPILED):
        m = p.search(d)
        if m is None:
            continue
        key = (m.start(), i)
        if best is None or key < best[0]:
            best = (key, t, m)
    if best is None:
        return "unknown", d[:60], name_guess, bool(name_guess)
    _key, t, m = best
    ev = d[max(0, m.start() - 24): m.end() + 24].replace("\n", " ").strip()
    conflict = bool(name_guess and name_guess != t)
    return t, ev, name_guess, conflict


def ensure_table(con: sqlite3.Connection) -> None:
    con.execute(
        f"""CREATE TABLE IF NOT EXISTS {TABLE} (
            region TEXT NOT NULL, dataset TEXT NOT NULL, category TEXT,
            field TEXT NOT NULL, ftype TEXT, coverage REAL,
            sem_type TEXT, evidence TEXT, name_guess TEXT,
            conflict INTEGER DEFAULT 0,
            verdict TEXT, best_s REAL, n_tests INTEGER,
            PRIMARY KEY (region, dataset, field))""")
    con.commit()


def build(con: sqlite3.Connection, region: str, category: Optional[str] = None) -> int:
    ensure_table(con)
    rid = con.execute("SELECT id FROM regions WHERE name=?", (region,)).fetchone()
    if not rid:
        print(f"[error] 区域 {region} 不存在")
        return 2
    rid = rid[0]
    cat_clause = "AND lower(d.category)=lower(?)" if category else ""
    params: List = [rid] + ([category] if category else [])
    rows = con.execute(
        f"""SELECT d.name ds, d.category cat, f.field_name fld, f.field_type ftype,
                   MAX(f.coverage) cov, MAX(f.description) descr
            FROM fields f JOIN datasets d ON f.dataset_id=d.id
            WHERE d.region_id=? {cat_clause}
            GROUP BY d.name, d.category, f.field_name, f.field_type""", params).fetchall()
    prof = {}
    for r in con.execute(
            f"""SELECT dataset, field, verdict, best_s, n_tests FROM field_profile_perf
                WHERE region=?""", (region,)):
        prof[(r["dataset"], r["field"])] = (r["verdict"], r["best_s"], r["n_tests"])
    out = []
    for r in rows:
        t, ev, ng, cf = classify(r["descr"], r["fld"])
        v, bs, nt = prof.get((r["ds"], r["fld"]), (None, None, None))
        out.append((region, r["ds"], r["cat"], r["fld"], r["ftype"], r["cov"],
                    t, ev, ng, 1 if cf else 0, v, bs, nt))
    seg = f"DELETE FROM {TABLE} WHERE region=?" + (" AND category=?" if category else "")
    con.execute(seg, params[:1] + ([category] if category else []))
    con.executemany(
        f"""INSERT OR REPLACE INTO {TABLE}
            (region,dataset,category,field,ftype,coverage,sem_type,evidence,name_guess,
             conflict,verdict,best_s,n_tests) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)""", out)
    con.commit()
    cc = collections.Counter(r[6] for r in out)
    print(f"[build] {region} → {len(out)} 行 写入 {TABLE}")
    for k, v in cc.most_common():
        print(f"   {k:<16} {v}")
    cf = sum(1 for r in out if r[9])
    print(f"   ★ 名字/描述语义冲突 = {cf}（{100*cf/max(1,len(out)):.1f}%）")
    return 0


def report(con: sqlite3.Connection, region: str, dataset: Optional[str]) -> int:
    w, p = ["region=?"], [region]
    if dataset:
        w.append("dataset=?"); p.append(dataset)
    rows = con.execute(f"SELECT * FROM {TABLE} WHERE {' AND '.join(w)}", p).fetchall()
    if not rows:
        print("[report] 表为空，先跑 --build")
        return 1
    print(f"\n===== {region} 语义类型 × platform category =====")
    cats = sorted({r["category"] or "(None)" for r in rows})
    types = [t for t, _ in collections.Counter(r["sem_type"] for r in rows).most_common()]
    hdr = f"{'category':<14}" + "".join(f"{t[:9]:>11}" for t in types) + f"{'合计':>9}"
    print(hdr)
    for c in cats:
        cnt = collections.Counter(r["sem_type"] for r in rows if (r["category"] or "(None)") == c)
        tot = sum(cnt.values())
        print(f"{c:<14}" + "".join(f"{cnt.get(t,0):>11}" for t in types) + f"{tot:>9}")
    print()
    print("===== ALIVE / WEAK 的语义类型分布（description 确认）=====")
    for v in ("ALIVE", "WEAK"):
        sub = [r for r in rows if r["verdict"] == v]
        c = collections.Counter(r["sem_type"] for r in sub)
        print(f"  {v}（{len(sub)}）：" + "  ".join(f"{k}={n}" for k, n in c.most_common()))
    print()
    print("===== ★ 名字/描述语义冲突的 ALIVE/WEAK（名字会骗人的直接证据）=====")
    for r in rows:
        if r["conflict"] and r["verdict"] in ("ALIVE", "WEAK"):
            print(f"  [{r['verdict']:<5}] {r['dataset']}.{r['field']}  名字像「{r['name_guess']}」→ 实为「{r['sem_type']}」")
            print(f"         evidence: {str(r['evidence'])[:96]}")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="基于 description 的字段语义类型分类")
    ap.add_argument("--build", action="store_true")
    ap.add_argument("--report", action="store_true")
    ap.add_argument("--region", default="GBR")
    ap.add_argument("--category")
    ap.add_argument("--dataset")
    a = ap.parse_args()
    con = _db()
    if a.build:
        return build(con, a.region, a.category)
    if a.report:
        return report(con, a.region, a.dataset)
    ap.print_help()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
