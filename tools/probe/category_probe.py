#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""category_probe.py — L1 苗子探针：为 L0 筛出的类别生成**机制多样**的探针表达式。

上游：``tools/probe/category_sweep.py --seed-fields --json <out>``（L0 类别普查）
下游：产物是 ``--out-exprs`` 的逐行表达式清单，喂给派发仿真通道
      （``tools/submit_batch.py --path`` / MCP ``submit_batch``）跑 QUICK，收割后
      用 :func:`classify` 判苗头。**本工具自己不派发仿真**（保持零配额、可dry-run）。

★★ 为什么探针「条数不是首要变量，机制多样性才是」（2026-10-06 实测）：
  历史命中率中位仅 7%（ASI 1.6% ~ MEA 19.9%），8 条的期望命中数 0.13~1.59 条。
  **但DEU 164 条达标只来自 73 个独立表达式**（去重比 2.2x），单集去重比更高：
  ``grtransform`` 10 条来自 **1 个**表达式、``model216`` 8 条 1 个、
  ``other455`` 14 条 2 个、``model28`` 12 条 2 个。
  ⇒ 若 8 条探针里掺了设置变体/同族表达式，**独立机制样本可能只剩 3 个**，
  统计上无意义。所以硬约束 ``--min-mechanism-diversity``：一条探针 = 一个新机制，
  同一字段可复用但**算子骨架必须不同**。

★ 宽松判据（L1 用）与严格判据（L2 用）分离：
  L1 只判「这个类有没有活的东西」，口径宽召回——``sharpe>=--min-sharpe``(默认 1.58)
  **或** ``2Y>=--min-2y``(默认 1.58) **或** ``sharpe>=--seed-sharpe``(默认 1.30)。
  实测 S1.3~1.58 的「次强」条全库 851 条，严格口径会全扔；放宽后各区命中率
  提升 1.4~2.2 倍（DEU 10.4%→19.8%、KOR 6.8%→17.5%、USA 2.2%→7.8%）。
  **RA 全清留给 L2 深挖再筛**，探针阶段不要求。

⚠ 合规红线（沿用 CLAUDE.md「禁止混信号调参」）：
  - **禁止任何两条独立信号腿相加**（``add(rank(A),rank(B))`` / 中缀 ``+`` / ``multiply``
    两腿）——探针也遵守。组合腿若要用，只能条件/分组/残差三式。
  - **禁混信号**、算子数 < 10。
  - 每字段包一层 ``rank`` 是**允许**的（探针是测量仪器，不是提交候选池；
    与「每字段套 rank」禁令的适用范围一致，见 field_signal_mine 的同款声明）。

用法：
    # 1) 生成探针（dry-run，不落库不派发）
    python tools/probe/category_probe.py --region DEU --sweep results/cat_sweep_DEU.json \\
        --categories MODEL,SHORTINTEREST --n 8 --out-exprs results/probe_DEU.txt

    # 2) 收割后判苗头（读backtest_results）
    python tools/probe/category_probe.py --region DEU --classify --min-sharpe 1.58

    # 只探一个类、强制机制多样
    python tools/probe/category_probe.py --region DEU --sweep <json> --categories RISK \\
        --n 6 --min-mechanism-diversity 0.8
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from typing import Any, Dict, List, Optional, Tuple

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(os.path.dirname(_HERE))
if os.path.join(_ROOT, "src") not in sys.path:
    sys.path.insert(0, os.path.join(_ROOT, "src"))

from wqb.db_conn import connect as db_connect  # noqa: E402

DB = os.path.join(_ROOT, "data", "wqb.db")

#: 探针骨架库。每个骨架是一个 ``(名称, 模板, 需要的时间窗列表)``。
#: **刻意做成互不相同的几何**：截面 rank / 时序 zscore / 时序 delta / 变化率 /
#: 相对位置 / 去均值 / 秩后裁剪 …——每个骨架探的是**不同机制**，
#: 而非同一机制换设置。禁在此清单内出现 ``add`` 两腿组合。
PROBE_SKELETONS: List[Tuple[str, str, List[int]]] = [
    ("xs_rank",        "rank({f})",                          []),
    ("ts_zscore",      "ts_zscore({f}, {w})",[252, 66, 504]),
    ("ts_delta",       "ts_delta({f}, {w})",                 [22, 66, 252]),
    ("ts_pctchg",      "ts_delta({f}, {w}) / ts_delay({f}, {w})", [22, 66]),
    ("ts_rank_w",      "ts_rank({f}, {w})",                  [1260, 252, 504]),
    ("decay",          "ts_decay_linear({f}, {w})",          [22, 66]),
    ("ts_mean",        "ts_mean({f}, {w})",                  [5, 22, 66]),
    ("ts_std_norm",    "ts_zscore(ts_mean({f}, {w}), {w2})", [22, 66]),
    ("quantile",       "quantile({f})",                      []),
    ("winsor",         "winsorize({f}, 4)",                  []),
    ("zscore_xs",      "zscore({f})",                        []),
]

#: 合规自检：这些 token 不得出现在探针里（两腿相加 = 混信号）
_FORBIDDEN_TOKENS = ("add(", "multiply(", "+rank(", "rank(A)+rank(B)")


def _render(tpl: str, fname: str, w: int) -> str:
    """渲染模板。``{w2}``（若存在）取 ``w`` 的 4 倍作第二窗口。

    多占位符骨架（如 ``ts_zscore(ts_mean(f, w), w2)``）用同一窗口会退化成单窗机制，
    故第二窗口按 4x 派生，保证几何确实不同。
    """
    if "{w2}" in tpl:
        return tpl.format(f=fname, w=w, w2=w * 4)
    if "{w}" in tpl:
        return tpl.format(f=fname, w=w)
    return tpl.format(f=fname)


def _pick_windows(sk: Tuple[str, str, List[int]], det) -> int:
    """按骨架的窗口候选确定性取一个（无候选则返回 0）。"""
    name, _tpl, wins = sk
    if not wins:
        return 0
    return int(wins[int(det() * len(wins)) % len(wins)])


class _Det:
    """极简确定性 LCG（避免引入 random 的全局状态，也让测试可复现）。"""

    def __init__(self, seed: int):
        self.s = (seed or 1) & 0xFFFFFFFF

    def __call__(self) -> float:
        self.s = (1103515245 * self.s + 12345) & 0x7FFFFFFF
        return self.s / 0x7FFFFFFF


def skeleton_key(expr: str) -> str:
    """提取表达式的「算子骨架」——用于机制多样性去重。

    **只抽掉字段名与数字字面量，保留算子名**。否则 ``ts_zscore(f,22)`` 与
    ``ts_delta(f,22)`` 会被抽成同一个 ``<F>(<F>,<N>)`` 而误判同机制（实测踩过：
    10 个骨架塌成 4 个，每类只出 4 条而非 8 条）。
    字段识别：出现在**函数调用参数位置**的标识符视为字段；裸标识符（小写单词）
    是算子/分组名。
    """
    import re
    # 1) 先把 "func(ARG" 的ARG 里裸标识符替换为 <F>（仅参数区，括号内）
    def _sub_args(m):
        inner = m.group(1)
        # 逗号分层：只替换顶层逗号分隔的标识符，嵌套括号内的另行处理（简化：逐层）
        return m.group(0)
    # 逐字符扫描，深度>0 时遇到的裸标识符 = 字段
    out = []
    depth = 0
    i = 0
    n = len(expr)
    while i < n:
        ch = expr[i]
        if ch == "(":
            depth += 1
            out.append(ch)
            i += 1
            continue
        if ch == ")":
            depth = max(0, depth - 1)
            out.append(ch)
            i += 1
            continue
        if depth > 0 and (ch.isalpha() or ch == "_"):
            j = i
            while j < n and (expr[j].isalnum() or expr[j] == "_"):
                j += 1
            tok = expr[i:j]
            # 分组变量（小写短词）与 true/false 不算字段
            if tok in ("sector", "industry", "subindustry", "market", "country",
                       "exchange", "currency", "asset", "true", "false"):
                out.append(tok)
            else:
                out.append("<F>")
            i = j
            continue
        out.append(ch)
        i += 1
    s = "".join(out)
    s = re.sub(r"[-+]?\d+(\.\d+)?", "<N>", s)   # 抽数字字面量
    return re.sub(r"\s+", " ", s).strip()


def _hist_of(seeds: List[Dict[str, Any]], field_name: str) -> int:
    """取某字段的历史强信号次数（0 =无先验）。"""
    for s in seeds:
        if s["field"] == field_name:
            return int(s.get("hist_hit", 0) or 0)
    return 0


def generate_probes(
    category: str,
    seeds: List[Dict[str, Any]],
    n: int,
    min_div: float,
    max_ops: int = 10,
) -> List[Dict[str, Any]]:
    """为一个类别生成 ``n`` 条**机制多样**的探针。

    策略：轮转骨架 × 轮转字段，**骨架不重复直到用完**（保证机制多样性）；
    同一字段可跨骨架复用（不同机制探同一字段是合理的），但要轮转字段避免
    整个探针押在一个字段上。
    """
    det = _Det(seed=abs(hash(category)) % (2 ** 31))
    rng_idx = 0
    used_skeletons: set = set()
    probes: List[Dict[str, Any]] = []
    fields_pool = [s["field"] for s in seeds] or []

    if not fields_pool:
        return probes

    # 骨架按「有历史强信号的字段优先」重排：有 hist_hit 的字段先配更多骨架
    ranked_fields = [s["field"] for s in seeds if s.get("hist_hit", 0) > 0]
    other_fields = [s["field"] for s in seeds if s.get("hist_hit", 0) <= 0]
    fields_pool = ranked_fields + other_fields

    # 骨架按「有历史强信号的字段优先」重排：有 hist_hit 的字段先配更多骨架
    ranked_fields = [s["field"] for s in seeds if s.get("hist_hit", 0) > 0]
    other_fields = [s["field"] for s in seeds if s.get("hist_hit", 0) <= 0]
    fields_pool = ranked_fields + other_fields

    # 字段按**数据集**均衡轮转（避免探针退化成「单数据集探针」）。
    # 实测：未做均衡时 8 个可探类里 5 个的种子 100% 落在同一数据集
    # （MODEL 62%、SHORTINTEREST/OTHER/FUNDAMENTAL/INSIDERS/PV 各 100%）——
    # 骨架虽不同，但数据集单一会让「苗子」结论只代表那一个集。
    by_ds: Dict[str, List[str]] = {}
    for s in seeds:
        # 一个字段可能属多集，取它的**第一个**数据集做归属（探针按单一集派发）
        ds_key = (s["datasets"][0] if s["datasets"] else "?")
        by_ds.setdefault(ds_key, []).append(s["field"])

    # 组间轮转：让不同数据集的字段交替出现；组内按历史信号强度排序
    groups: List[List[str]] = []
    ds_order = sorted(
        by_ds,
        key=lambda k: (-max((s["hist_hit"] for s in seeds
                             if (s["datasets"][0] if s["datasets"] else "?") == k), default=0), k),
    )
    for k in ds_order:
        grp = sorted(by_ds[k], key=lambda fn: -_hist_of(seeds, fn))
        groups.append(grp)

    attempts = 0
    max_attempts = n * 8
    gi = 0                # 当前数据集组
    offset = 0            # 组内游标
    while len(probes) < n and attempts < max_attempts:
        if not groups:
            break
        grp = groups[gi % len(groups)]
        if offset >= len(grp):          # 该组用完 → 换下一组
            gi += 1
            offset = 0
            if gi >= len(groups) * 2:   # 所有组都轮过一遍仍不够 → 允许组内复用
                gi = gi % len(groups)
                offset = 0
            continue
        fname = grp[offset]
        offset += 1
        attempts += 1

        sk = PROBE_SKELETONS[rng_idx % len(PROBE_SKELETONS)]
        rng_idx += 1
        sk_name, tpl, wins = sk
        w = _pick_windows(sk, det)

        expr = _render(tpl, fname, w)
        # 合规自检：两腿相加一律不出（模板本身已保证，这里是防御性断言）
        if any(tok in expr for tok in _FORBIDDEN_TOKENS):
            continue

        key = skeleton_key(expr)
        # ★ 机制多样性闸：一**几何**只出 1 条；用尽后按 (骨架 × 窗口) 展开新变体，
        #   而不是 break —— 否则按产出率配额（实测 MODEL 分到 28 条）时，10 个骨架
        #   出尽就停，实际只能出 10 条、预算浪费 18 条。
        #   变体必须**窗口不同**（skeleton_key 含 <N>，故 key 不同 ⇒ 真的换了机制参数）。
        if key in used_skeletons:
            # 该几何已用尽 → 尝试换个窗口展开；若窗口候选已用尽则换下一骨架
            if not wins:
                if rng_idx >= len(PROBE_SKELETONS):
                    break
                continue
            # 找该骨架还没用过的窗口
            alt = None
            for w2 in wins:
                e2 = _render(tpl, fname, w2)
                k2 = skeleton_key(e2)
                if k2 not in used_skeletons:
                    alt = (w2, e2, k2)
                    break
            if alt is None:
                if rng_idx >= len(PROBE_SKELETONS):
                    break
                continue
            w, expr, key = alt
        used_skeletons.add(key)

        # 简单算子数上限（合规）
        ops = expr.count("(")
        if ops > max_ops:
            continue

        ds_of_field = next(
            (s["datasets"][0] for s in seeds
             if s["field"] == fname and s["datasets"]), "?")
        probes.append({
            "category": category,
            "field": fname,
            "datasets": [ds_of_field] if ds_of_field != "?" else [],
            "skeleton": sk_name,
            "skeleton_key": key,
            "expression": expr,
            "ops": ops,
        })

    return probes


def check_diversity(probes: List[Dict[str, Any]]) -> Dict[str, Any]:
    """算机制多样性指标：唯一骨架数 / 总数，以及字段/数据集集中度。"""
    keys = {p["skeleton_key"] for p in probes}
    flds = [p["field"] for p in probes]
    uniq_f = len(set(flds))
    ds = [p["datasets"][0] if p.get("datasets") else "?" for p in probes]
    ds_cnt: Dict[str, int] = {}
    for d in ds:
        ds_cnt[d] = ds_cnt.get(d, 0) + 1
    top_ds, top_ds_n = (max(ds_cnt.items(), key=lambda kv: kv[1]) if ds_cnt else ("?", 0))
    return {
        "n": len(probes),
        "n_skeletons": len(keys),
        "diversity": round(len(keys) / len(probes), 2) if probes else 0.0,
        "n_fields": uniq_f,
        "field_concentration": round(uniq_f / len(probes), 2) if probes else 0.0,
        "n_datasets": len(ds_cnt),
        "top_dataset": top_ds,
        "top_dataset_share": round(top_ds_n / len(probes), 2) if probes else 0.0,
    }


def classify(
    region: str,
    categories: Optional[List[str]],
    min_sharpe: float,
    min_2y: float,
    seed_sharpe: float,
) -> Dict[str, Any]:
    """从 ``backtest_results`` 收割后判苗头（宽召回）。"""
    conn = db_connect(DB, readonly=True)
    try:
        cols = {r[1] for r in conn.execute("PRAGMA table_info(backtest_results)")}
        ds_col = "dataset"
        where = ["b.region=?"]
        params: List[Any] = [region.upper()]
        if categories:
            where.append(f"b.{ds_col} IN ({','.join('?' * len(categories))})")
            params += categories
        sql = f"""
          SELECT b.dataset, b.sharpe, b.two_year_sharpe, b.ra_failed_checks,
                 b.expression_id, b.region
          FROM backtest_results b
          WHERE {' AND '.join(where)}
        """
        rows = conn.execute(sql, params).fetchall()
    finally:
        conn.close()

    hit = mid = 0
    for r in rows:
        s = r[1]
        s2 = r[2]
        strong = (s is not None and s >= min_sharpe) or (s2 is not None and s2 >= min_2y)
        weak = s is not None and seed_sharpe <= s < min_sharpe
        if strong:
            hit += 1
        elif weak:
            mid += 1
    return {
        "region": region.upper(),
        "categories": categories or "(全部)",
        "n_scored": len(rows),
        "strong_hits": hit,
        "seed_hits": mid,
        "verdict": "★苗头" if hit > 0 else ("待探" if mid > 0 else "已枯"),
        "note": (
            f"强命中 {hit}（sharpe>={min_sharpe} 或 2Y>={min_2y}）→ 建议进 L2 深挖；"
            f"次强 {mid}（{seed_sharpe}<=sharpe<{min_sharpe}）→ 苗头偏弱，可选"
        ),
    }


def main() -> int:
    ap = argparse.ArgumentParser(
        description="L1 苗子探针：为 L0 筛出的类别生成机制多样的探针表达式（零配额）")
    ap.add_argument("--region", required=True)
    ap.add_argument("--sweep", help="L0 category_sweep 的 --json 产物")
    ap.add_argument("--categories", default="", help="只探这些类（逗号分隔；缺省=全部可探类）")
    ap.add_argument("--n", type=int, default=8, help="每类探针条数（默认 8）")
    ap.add_argument("--min-mechanism-diversity", dest="min_div", type=float, default=0.6,
                    help="每类机制多样性下限（唯一骨架/条数，低于此值告警；默认 0.6）")
    ap.add_argument("--out-exprs", help="逐行表达式写此文件（可直接喂派发仿真）")
    ap.add_argument("--use-quota", action="store_true",
                    help="按 L0 算好的产出率配额分配各类条数（替代 --n 统一条数）")
    # classify 模式
    ap.add_argument("--classify", action="store_true", help="收割模式：从 backtest_results 判苗头")
    ap.add_argument("--min-sharpe", type=float, default=1.58)
    ap.add_argument("--min-2y", type=float, default=1.58)
    ap.add_argument("--seed-sharpe", type=float, default=1.30)
    args = ap.parse_args()

    cats = [c.strip().upper() for c in args.categories.split(",") if c.strip()]

    if args.classify:
        res = classify(args.region, cats or None, args.min_sharpe, args.min_2y, args.seed_sharpe)
        print(json.dumps(res, ensure_ascii=False, indent=2))
        return 0

    if not args.sweep:
        ap.error("生成模式需要 --sweep <L0 json>")

    with open(args.sweep, encoding="utf-8") as f:
        sweep = json.load(f)

    by_cat = {c["category"]: c for c in sweep["categories"]}
    targets = cats or [c for c, v in by_cat.items() if v["verdict"] in ("★苗头", "待探")]
    # ★ L2 配额：L0 已按历史产出率算好每类该分几条（`sweep["quota"]`）。
    # 缺省仍用 `--n` 统一条数；给了 --use-quota 就按产出率分配（不均分）。
    quota = sweep.get("quota") or {}
    use_quota = args.use_quota and bool(quota)

    all_probes: List[Dict[str, Any]] = []
    lines: List[str] = []
    mode = (f"按产出率配额（总预算 {sum(quota.values())}）" if use_quota
            else f"统一 {args.n} 条/类")
    print(f"=== L1 苗子探针 · region={args.region.upper()} · {mode} ===")
    print(f"类别来源: {len(targets)} 个（{'指定' if cats else 'L0 可探类'}）\n")

    for cat in targets:
        info = by_cat.get(cat)
        n_for_cat = int(quota.get(cat, args.n)) if use_quota else args.n
        if not info:
            print(f"  {cat:<16} [skip] L0 结果里无此类")
            continue
        probes = generate_probes(cat, info["seeds"], n_for_cat, args.min_div)
        if not probes:
            print(f"  {cat:<16} [skip] 无可用种子字段")
            continue
        div = check_diversity(probes)
        warns = []
        if n_for_cat > len(PROBE_SKELETONS) and div["n_skeletons"] < len(PROBE_SKELETONS):
            warns.append(f"骨架已用尽（{div['n_skeletons']}/{len(PROBE_SKELETONS)}），"
                         f"超出部分靠换字段而非换机制")
        if div["diversity"] < args.min_div:
            warns.append(f"机制多样性 {div['diversity']}<{args.min_div}（加 n 或补字段）")
        if div["top_dataset_share"] >= 0.6:
            warns.append(f"数据集集中 {div['top_dataset_share']:.0%} 于 {div['top_dataset']}"
                         f"（该集字段最多所致；结论只代表这一个集）")
        warn = ("  ⚠ " + "；".join(warns)) if warns else ""
        all_probes += probes
        lines += [p["expression"] for p in probes]
        print(f"  {cat:<16} {div['n']} 条 / {div['n_skeletons']} 骨架 "
              f"(div={div['diversity']}, 字段 {div['n_fields']}, 数据集 {div['n_datasets']}){warn}")

    print(f"\n合计 {len(all_probes)} 条探针 / {len(set(p['skeleton_key'] for p in all_probes))} 个不同骨架")

    # 合规自检汇总
    bad = [p for p in all_probes if any(tok in p["expression"] for tok in _FORBIDDEN_TOKENS)]
    if bad:
        print(f"  [FAIL] {len(bad)} 条含混信号 token，已剔除")
    else:
        print("  [合规] 无混信号两腿相加；算子数均 < 10")

    if args.out_exprs and lines:
        with open(args.out_exprs, "w", encoding="utf-8") as f:
            for ln in lines:
                f.write(ln + "\n")
        print(f"  [out] {args.out_exprs}（{len(lines)} 行，可喂 tools/submit_batch.py --path）")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())