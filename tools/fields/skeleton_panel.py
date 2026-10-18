#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""skeleton_panel.py — 骨架多样性面板（2026-10-09 用户明令纪律的工具化）。

【纪律来源】用户批评：「你为什么总是用同一套骨架，一定要看多样性」。
实测佐证：GBR 1,004 个被测字段中 **64%（645 个）只见过 1 种骨架**；
top8 模板 ≈34% 且全是同一套 house 骨架变体 ⇒ 「DEAD/弱」判定实为「该骨架下不行」。

【两条硬规则】
  R1 字段初筛（screening）必须走骨架面板：同一批里每个字段至少配 2~3 个**不同族**骨架；
     只有「方向深挖/参数扫」（已锁定字段，扫同族变体）才允许同模板成批。
  R2 发批前必须过 `audit`：单模板占比 >60% 或 8 条里不同骨架族 <3 ⇒ 拒绝发批
     （与 expr-lint / op-arity 同级，属发批七闸之一）。

【用法】
  $WQ_PY tools/fields/skeleton_panel.py audit --path cache/_wave.txt        # 发批前审计
  $WQ_PY tools/fields/skeleton_panel.py gen --dataset analyst7 --region GBR \
      --verdict UNTESTED --limit 8 --out cache/_div_wave.txt                # 多样化初筛生成
  $WQ_PY tools/fields/skeleton_panel.py list                                # 列出骨架族
"""
from __future__ import annotations
import argparse, collections, json, os, re, sqlite3, sys

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, REPO)
DB = os.path.join(REPO, "data", "wqb.db")

TV = "lambda_min=0, lambda_max=1, target_tvr=0.13"


def _b(f, n=500):            # backfill 包装
    return "ts_backfill(%s,%d)" % (f, n)


# ── 骨架族面板（10 族；inner 按字段语义可替换）────────────────────────────
# 每族 = (族名, 说明, 构造函数 fn(field_expr) -> expr)
PANEL = [
    ("level_rank",   "水平直排（house 基准）",
     lambda x: "group_rank(ts_target_tvr_decay(winsorize(rank(%s),std=0.2), %s), sector)" % (x, TV)),
    ("delta",        "时序差分（变化量纲）",
     lambda x: "group_rank(ts_target_tvr_decay(winsorize(rank(ts_delta(%s,66)),std=0.2), %s), sector)" % (x, TV)),
    ("ts_rank",      "时序分位（自身历史定位）",
     lambda x: "group_rank(ts_target_tvr_decay(winsorize(rank(ts_rank(%s,252)),std=0.2), %s), sector)" % (x, TV)),
    ("ts_zscore",    "时序标准化",
     lambda x: "group_rank(ts_target_tvr_decay(winsorize(rank(ts_zscore(%s,252)),std=0.2), %s), sector)" % (x, TV)),
    ("decay_linear", "线性衰减（替代换手压法）",
     lambda x: "group_rank(ts_decay_linear(rank(%s), 5), sector)" % x),
    ("gn_first",     "原始信号先去组内共同成分",
     lambda x: "group_rank(ts_target_tvr_decay(winsorize(rank(group_neutralize(%s, sector)),std=0.2), %s), sector)" % (x, TV)),
    ("av_diff",      "与自身均值偏离",
     lambda x: "group_rank(ts_av_diff(%s,22), sector)" % x),
    ("double_window", "双窗合成 add（合规形态）",
     lambda x: "group_rank(ts_target_tvr_decay(winsorize(rank(add(ts_mean(%s,1), ts_mean(%s,120))),std=0.2), %s), sector)" % (x, x, TV)),
    ("hump",         "目标换手 hump 族",
     lambda x: "group_rank(ts_target_tvr_hump(winsorize(rank(%s),std=0.2), %s), sector)" % (x, TV)),
    ("quantile",     "时序分位 ts_quantile",
     lambda x: "group_rank(ts_target_tvr_decay(winsorize(rank(ts_quantile(%s,252)),std=0.2), %s), sector)" % (x, TV)),
    # ★ v2（2026-10-09 审核点②，用户裁决通过）：数据实证新增两族
    ("gate",         "trade_when 门控（unknown×gate 实测 2.07 / percentile×gate 2.37）",
     lambda x: "trade_when(ts_rank(%s,252) > 0.7, group_rank(ts_target_tvr_decay(winsorize(rank(%s),std=0.2), %s), sector), -1)" % (x, x, TV)),
    ("divide",       "自身均值比率化 divide(x, ts_mean)",
     lambda x: "group_rank(ts_target_tvr_decay(winsorize(rank(divide(%s, ts_mean(%s,252))),std=0.2), %s), sector)" % (x, x, TV)),
]
PANEL_MAP = {n: fn for n, _, fn in PANEL}

# ★★ 语义→优选骨架族 v2（2026-10-09 审核点②，用户裁决认可）
# 依据：GBR 2,614 条实测的「sem_type × 骨架族 → maxS」矩阵
# （output_report/GBR_skeleton_mapping_review_20261009.md）。每条注释为实测证据。
SEM_PREFERRED = {
    # subtract(对偶差) 1.96(n=138) / quantile 1.96 / gn_first 1.95 / decay_linear 1.90 ｜ level_rank 仅 1.36 降级
    "count":           ["subtract_pair", "quantile", "gn_first", "decay_linear"],
    # delta 2.15 / av_diff 2.02 远超 level_rank 1.62；ts_rank 0.86 弱 ⇒ 移出
    "ratio":           ["delta", "av_diff", "quantile", "level_rank"],
    # delta 2.61（全矩阵最高）/ gn_first 1.91 / double_window 1.71 ｜ gate 2.37(n=5) 用户裁决入选
    "percentile":      ["delta", "gn_first", "double_window", "gate", "level_rank"],
    # delta 1.90 ✓ ｜ ts_rank 1.79(n=23) > ts_zscore 1.60(n=3) ⇒ 换序
    "estimate_level":  ["delta", "ts_rank", "level_rank"],
    # delta 1.80 最强；ts_rank 从未试过 ⇒ 移出
    "probability":     ["delta", "level_rank", "av_diff"],
    # level_rank 1.61 是唯一出过 ALIVE 的族；quantile 未验证（待证，列末位）
    "score":           ["level_rank", "ts_rank", "quantile"],
    # 数据打脸初版：delta 1.78 强 / ts_zscore 0.65(29) 弱 ⇒ ts_zscore 降为对照族
    "level_amount":    ["delta", "level_rank"],
    # quantile 1.75 是唯一 ALIVE 族；delta 0.57 弱 ⇒ 降级
    "sentiment":       ["quantile", "level_rank"],
    # level_rank 1.62 ✓ ｜ decay_linear 1.50 ｜ delta 0.30 弱 ⇒ 移出
    "revision_change": ["level_rank", "decay_linear", "ts_rank"],
    # 无任何族出过 ALIVE（delta 1.01 最高）⇒ 全族低置信待证
    "dispersion":      ["delta", "divide"],
    # 兜底：gate 2.07 / decay_linear 1.77 / quantile 1.76 / gn_first 1.75 / level_rank 1.68 都出过
    "unknown":         ["level_rank", "delta", "decay_linear", "gate"],
}
DEFAULT_PREF = ["level_rank", "delta", "decay_linear"]


def _sem_of(region: str, dataset: str, field: str) -> str:
    con = sqlite3.connect(DB); con.execute("PRAGMA busy_timeout=60000"); con.row_factory = sqlite3.Row
    r = con.execute("SELECT sem_type FROM field_semantic_type WHERE region=? AND dataset=? AND field=?",
                    (region, dataset, field)).fetchone()
    con.close()
    return (r["sem_type"] if r and r["sem_type"] else "unknown")


def _is_vector(region: str, dataset: str, field: str) -> bool:
    con = sqlite3.connect(DB); con.execute("PRAGMA busy_timeout=60000"); con.row_factory = sqlite3.Row
    r = con.execute("""SELECT f.field_type FROM fields f JOIN datasets d ON d.id=f.dataset_id
                       JOIN regions rg ON rg.id=d.region_id
                       WHERE rg.name=? AND d.name=? AND f.field_name=?""",
                    (region, dataset, field)).fetchone()
    con.close()
    return bool(r and (r["field_type"] or "").upper() == "VECTOR")


# count 语义的对偶字段差（用户裁决 2026-10-09：count 最强形态是 subtract(rank(raised),rank(lowered))=1.96）
_DUAL_TOKENS = [("raisednum", "lowerednum"), ("raised", "lowered"),
                ("numup", "numdown"), ("_up", "_down"), ("buy", "sell")]


def _dual_of(region: str, dataset: str, field: str) -> Optional[str]:
    """找同数据集内的对偶字段（raised↔lowered 等）；无则 None。"""
    cand = None
    for a, b in _DUAL_TOKENS:
        if a in field:
            cand = field.replace(a, b, 1); break
        if b in field:
            cand = field.replace(b, a, 1); break
    if not cand:
        return None
    con = sqlite3.connect(DB); con.execute("PRAGMA busy_timeout=60000"); con.row_factory = sqlite3.Row
    r = con.execute("""SELECT 1 FROM fields f JOIN datasets d ON d.id=f.dataset_id
                       JOIN regions rg ON rg.id=d.region_id
                       WHERE rg.name=? AND d.name=? AND f.field_name=? LIMIT 1""",
                    (region, dataset, cand)).fetchone()
    con.close()
    return cand if r else None


def _subtract_pair_expr(fa: str, fb: str) -> str:
    return ("group_rank(ts_target_tvr_decay(winsorize(rank(subtract(rank(%s), rank(%s))),std=0.2), %s), sector)"
            % (_b(fa), _b(fb), TV))


def build_for_field(region: str, dataset: str, field: str, k: int = 3) -> list:
    """为一个字段生成 k 条**不同族**骨架的表达式（R1 的实现）。

    ★ v2（2026-10-09 审核点②）：count 语义优先尝试对偶字段差 subtract_pair（实测 1.96 最强）。
    """
    sem = _sem_of(region, dataset, field)
    x = _b("vec_avg(%s)" % field) if _is_vector(region, dataset, field) else _b(field)
    fams = SEM_PREFERRED.get(sem, DEFAULT_PREF)
    out, seen = [], set()
    for fam in fams + [n for n, _, _ in PANEL]:          # 先优选族，再全局面板补足 k
        if fam in seen:
            continue
        if fam == "subtract_pair":
            dual = _dual_of(region, dataset, field)
            if not dual:
                continue                                 # 无对偶字段 ⇒ 跳过该族
            seen.add(fam)
            out.append((fam, _subtract_pair_expr(field, dual)))
            continue
        if fam not in PANEL_MAP:
            continue
        seen.add(fam)
        out.append((fam, PANEL_MAP[fam](x)))
        if len(out) >= k:
            break
    return out


# ── audit：模板归一 + 多样性统计 ──────────────────────────────────────────
_OPSET = None
def _opset() -> set:
    global _OPSET
    if _OPSET is None:
        p = os.path.join(REPO, "research-data", "operators_platform_20260904.json")
        d = json.load(open(p, encoding="utf-8"))
        ops = d if isinstance(d, list) else d.get("operators", [])
        _OPSET = {o["name"] for o in ops}
    return _OPSET


def template(code: str) -> str:
    """把字段名/分组名/数字归一为占位符 ⇒ 骨架模板串。"""
    ops = _opset()
    toks = re.findall(r"[A-Za-z_][A-Za-z0-9_]*|\d+\.?\d*|\(|\)|,", code or "")
    out = []
    for t in toks:
        if t in ops or t in "(),":          out.append(t)
        elif re.fullmatch(r"\d+\.?\d*", t): out.append("N")
        else:                               out.append("F")
    return " ".join(out)


def cmd_audit(a):
    lines = [l.strip() for l in open(a.path, encoding="utf-8") if l.strip()]
    tm = collections.Counter(template(l) for l in lines)
    n = len(lines)
    top_share = tm.most_common(1)[0][1] / max(1, n)
    print("[audit] %s：%d 条，%d 种骨架模板" % (a.path, n, len(tm)))
    for t, c in tm.most_common(6):
        print("   %4.0f%%  %s" % (100 * c / n, t[:100]))
    ok = len(tm) >= a.min_families and top_share <= a.max_share
    if not ok and getattr(a, "param_sweep", False):
        print("[audit] ⚠ 多样性不足（模板 %d 种），但已显式声明 --param-sweep（深挖/参数扫，R1 例外），放行。"
              % len(tm))
        return 0
    if not ok:
        print("[audit] ✗ 多样性不足：不同模板 %d（需≥%d）｜最大单模板占比 %.0f%%（需≤%.0f%%）"
              % (len(tm), a.min_families, 100 * top_share, 100 * a.max_share))
        print("[audit] ⇒ 违反 R2（发批七闸之骨架多样性闸），禁止发批。")
        return 1
    print("[audit] ✓ 通过（模板 %d 种，最大占比 %.0f%%）" % (len(tm), 100 * top_share))

    # ★ v2（审核点③）：字段级检查 —— 防止「8 字段 × 8 不同族」这种绕过波级审计的假多样
    # （每个字段仍只见过 1 族，违反 R1「每字段 ≥2~3 族」）。
    if a.region and not getattr(a, "param_sweep", False):
        import sqlite3 as _sq
        con = _sq.connect(DB); con.row_factory = _sq.Row
        flds = {r["field_name"] for r in con.execute(
            """SELECT f.field_name FROM fields f JOIN datasets d ON d.id=f.dataset_id
               JOIN regions rg ON rg.id=d.region_id WHERE rg.name=?""", (a.region,))}
        con.close()
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        from field_profile import skeleton_family_of  # 与画像同源的族分类器
        per = collections.defaultdict(set)
        nlines = collections.Counter()
        for l in lines:
            fam = skeleton_family_of(l)
            toks = set(re.findall(r"[A-Za-z_][A-Za-z0-9_]*", l)) & flds
            for tok in toks:
                per[tok].add(fam)
                nlines[tok] += 1
        # ★ 对偶差里的「配料字段」豁免：只出现 1 次、且那一条里含 ≥2 个字段 ⇒ 它是 subtract_pair 的对偶腿，
        # 不是本波的复测对象（2026-10-09 审核点④实测发现）。
        _nfield = {i: len(set(re.findall(r"[A-Za-z_][A-Za-z0-9_]*", l)) & flds) for i, l in enumerate(lines)}
        _seen_line = {}
        for i, l in enumerate(lines):
            for tok in set(re.findall(r"[A-Za-z_][A-Za-z0-9_]*", l)) & flds:
                _seen_line.setdefault(tok, i)
        ingredient = {t for t in per if nlines[t] == 1 and _nfield.get(_seen_line.get(t, -1), 0) >= 2}
        bad = {f: s for f, s in per.items() if len(s) < a.per_field_min and f not in ingredient}
        if ingredient:
            print("[audit] 字段级：%d 个字段（%d 个对偶配料豁免）" % (len(per), len(ingredient)))
        else:
            print("[audit] 字段级：%d 个字段" % len(per))
        if bad:
            print("[audit] ✗ 字段级多样性不足（R1）：")
            for f, s in list(bad.items())[:8]:
                print("    %s 只见过 %s" % (f, "/".join(sorted(s))))
            return 1
        print("[audit] ✓ 字段级通过（每字段 ≥%d 族）" % a.per_field_min)
    return 0


def gap_families_of(region: str, dataset: str, field: str) -> list:
    """该字段「应配但未见过」的优选骨架族（缺口驱动，供复活补测）。"""
    con = sqlite3.connect(DB); con.execute("PRAGMA busy_timeout=60000"); con.row_factory = sqlite3.Row
    r = con.execute("SELECT skeleton_fams FROM field_profile_perf WHERE region=? AND dataset=? AND field=?",
                    (region, dataset, field)).fetchone()
    con.close()
    seen = set((r["skeleton_fams"] or "").split(",")) if r and r["skeleton_fams"] else set()
    sem = _sem_of(region, dataset, field)
    req = SEM_PREFERRED.get(sem, DEFAULT_PREF)
    alias = {"subtract_pair": "subtract"}
    return [f for f in req if f not in seen and alias.get(f, f) not in seen]


def build_gap_exprs(region: str, dataset: str, field: str, k: int = 2) -> list:
    """只生成缺口族的表达式（复活补测专用）。

    ★ 缺口不足 k 族时，从全局面板里补「没见过的次优族」凑足 ——
    R1 要求每字段 ≥k 族证据，缺口只剩 1 族时不能让它单族上阵（2026-10-09 审核点④实测发现）。
    """
    con = sqlite3.connect(DB); con.execute("PRAGMA busy_timeout=60000"); con.row_factory = sqlite3.Row
    r = con.execute("SELECT skeleton_fams FROM field_profile_perf WHERE region=? AND dataset=? AND field=?",
                    (region, dataset, field)).fetchone()
    con.close()
    seen = set((r["skeleton_fams"] or "").split(",")) if r and r["skeleton_fams"] else set()
    gap = gap_families_of(region, dataset, field)
    topup = [n for n, _, _ in PANEL if n not in seen and n not in gap]
    fams = (gap + topup)[:k]
    if not fams:
        return []
    x = _b("vec_avg(%s)" % field) if _is_vector(region, dataset, field) else _b(field)
    out = []
    for fam in fams:
        if fam == "subtract_pair":
            dual = _dual_of(region, dataset, field)
            if dual:
                out.append((fam, _subtract_pair_expr(field, dual)))
            continue
        if fam in PANEL_MAP:
            out.append((fam, PANEL_MAP[fam](x)))
    return out


def cmd_gen(a):
    con = sqlite3.connect(DB); con.execute("PRAGMA busy_timeout=60000"); con.row_factory = sqlite3.Row
    rows = [dict(r) for r in con.execute(
        """SELECT dataset, field FROM field_profile_perf
           WHERE region=? AND verdict=? AND dataset=?
           ORDER BY coverage DESC LIMIT ?""",
        (a.region, a.verdict, a.dataset, a.limit))]
    exprs, fams = [], []
    for r in rows:
        got = build_for_field(a.region, r["dataset"], r["field"], k=a.per_field)
        for fam, e in got:
            exprs.append(e); fams.append(fam)
    with open(a.out, "w", encoding="utf-8") as f:
        f.write("\n".join(exprs) + "\n")
    print("[gen] %d 字段 × %d 骨架 = %d 条 → %s" % (len(rows), a.per_field, len(exprs), a.out))
    print("[gen] 骨架族分布:", dict(collections.Counter(fams)))
    return 0


def cmd_gap_report(a):
    """审核点①：字段 → 语义 → 应配骨架族 → 已见 → 缺口；含 DEAD 置信度重分布。"""
    con = sqlite3.connect(DB); con.execute("PRAGMA busy_timeout=60000"); con.row_factory = sqlite3.Row
    q = """SELECT p.dataset, p.field, p.ftype, p.verdict, p.n_tests, p.best_s, p.n_skeletons,
                  p.skeleton_fams, COALESCE(s.sem_type,'?') sem
           FROM field_profile_perf p
           LEFT JOIN field_semantic_type s
             ON s.region=p.region AND s.dataset=p.dataset AND s.field=p.field
           WHERE p.region=?"""
    rows = [dict(r) for r in con.execute(q, (a.region,))]

    tested = [r for r in rows if (r["n_tests"] or 0) > 0]
    dead_like = [r for r in tested if r["verdict"] in ("DEAD", "DEAD_STATIC", "DEAD_TURNOVER", "DEAD_COUNT")]
    low = [r for r in dead_like if (r["n_skeletons"] or 0) <= 1]
    print("=== DEAD 系列置信度重分布（%s）===" % a.region)
    print("  DEAD 系列合计 %d：高置信（见过≥2族）%d ｜ **低置信（只见1族）%d（%.0f%%）**"
          % (len(dead_like), len(dead_like) - len(low), len(low), 100 * len(low) / max(1, len(dead_like))))
    for v in ("DEAD", "DEAD_STATIC", "DEAD_TURNOVER", "DEAD_COUNT"):
        sub = [r for r in dead_like if r["verdict"] == v]
        if sub:
            l1 = sum(1 for r in sub if (r["n_skeletons"] or 0) <= 1)
            print("    %-14s %4d（低置信 %d，%.0f%%）" % (v, len(sub), l1, 100 * l1 / len(sub)))

    gap_rows = []
    for r in tested:
        req = SEM_PREFERRED.get(r["sem"], DEFAULT_PREF)
        seen = set((r["skeleton_fams"] or "").split(",")) if r["skeleton_fams"] else set()
        # 族别名：要求的 subtract_pair（对偶差）与历史分类器产出的 subtract 视为同族
        _alias = {"subtract_pair": "subtract"}
        gap = [f for f in req if f not in seen and _alias.get(f, f) not in seen]
        gap_rows.append((r, req, seen, gap))
    full = [g for g in gap_rows if not g[3]]
    partial = [g for g in gap_rows if g[3]]
    print("\n=== 应配骨架覆盖（按 sem_type 的优选族）===")
    print("  已测字段 %d：优选族**全覆盖** %d（%.0f%%）｜ **有缺口** %d（%.0f%%）"
          % (len(tested), len(full), 100 * len(full) / max(1, len(tested)),
             len(partial), 100 * len(partial) / max(1, len(tested))))

    for ds in (a.datasets or []):
        sub = [g for g in gap_rows if g[0]["dataset"] == ds][: a.per_ds]
        if not sub:
            continue
        print("\n=== 样本：%s ===" % ds)
        for r, req, seen, gap in sub:
            print("  %-46s %-13s verdict=%-6s S=%s" % (r["field"][:46], r["sem"], r["verdict"],
                  ("%.2f" % r["best_s"]) if r["best_s"] is not None else "-"))
            print("      应配 %s ｜ 已见 %s ｜ **缺口 %s**"
                  % ("/".join(req), "/".join(sorted(seen)) or "-", "/".join(gap) or "无"))
    return 0


def cmd_list(_a):
    for n, d, _ in PANEL:
        print("  %-14s %s" % (n, d))
    print("\n语义→优选族:")
    for k, v in SEM_PREFERRED.items():
        print("  %-16s %s" % (k, " / ".join(v)))
    return 0


def main():
    ap = argparse.ArgumentParser(description="骨架多样性面板（R1 初筛多样化 / R2 发批多样性闸）")
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("audit", help="发批前骨架多样性审计")
    p.add_argument("--path", required=True)
    p.add_argument("--min-families", type=int, default=3)
    p.add_argument("--max-share", type=float, default=0.60)
    p.add_argument("--region", default=None, help="给该值即启用字段级检查（R1：每字段 ≥per-field-min 族）")
    p.add_argument("--per-field-min", type=int, default=2, help="字段级检查：每字段至少见过的族数")
    p.add_argument("--param-sweep", action="store_true",
                   help="显式声明本批是深挖/参数扫（R1 例外），多样性不足时放行")
    p.set_defaults(fn=cmd_audit)
    p = sub.add_parser("gen", help="多样化初筛波生成")
    p.add_argument("--region", required=True); p.add_argument("--dataset", required=True)
    p.add_argument("--verdict", default="UNTESTED")
    p.add_argument("--limit", type=int, default=8)
    p.add_argument("--per-field", type=int, default=2)
    p.add_argument("--out", required=True)
    p.set_defaults(fn=cmd_gen)
    p = sub.add_parser("gap-report", help="审核点①：骨架缺口与 DEAD 置信度重分布")
    p.add_argument("--region", required=True)
    p.add_argument("--datasets", nargs="*", default=[])
    p.add_argument("--per-ds", type=int, default=5)
    p.set_defaults(fn=cmd_gap_report)
    p = sub.add_parser("list", help="列出骨架族与语义映射")
    p.set_defaults(fn=cmd_list)
    sys.exit(main2(ap.parse_args()))


def main2(a):
    return a.fn(a)


if __name__ == "__main__":
    main()
