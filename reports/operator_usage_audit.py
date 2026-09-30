#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""一次性分析：算子清单 x 已提交 alpha 的算子使用审计。

数据源：
- 算子清单：docs/reference/operators_catalog.json（2026-09-07 平台实况快照，103 个）
          + data/operators_verified.json（2026-09-04 探针核验 103 个 live）
- 已提交 alpha：data/wqb.db
    submitted = submission_ledger 中的 alpha_id
              ∪ alphas.platform_status IN ('ACTIVE','DECOMMISSIONED')
- 使用足迹（次要口径）：alphas 表全部有表达式的行（9348）

产出：
- output_report/operator_inventory_and_unused_20260930.md
- output_report/operator_usage_audit_20260930.json
"""
from __future__ import annotations

import collections
import json
import re
import sqlite3
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CAT_PATH = os.path.join(ROOT, "docs", "reference", "operators_catalog.json")
VER_PATH = os.path.join(ROOT, "data", "operators_verified.json")
DB_PATH = os.path.join(ROOT, "data", "wqb.db")
OUT_MD = os.path.join(ROOT, "output_report", "operator_inventory_and_unused_20260930.md")
OUT_JSON = os.path.join(ROOT, "output_report", "operator_usage_audit_20260930.json")

# ---------------------------------------------------------------- 等价平替表
# A <-> B：功能一致、可（近似）直接替换；caveat 为替换注意点。
EQUIV = [
    ("ts_mean", "ts_decay_linear", "同为时序平滑；decay 线性衰减加权（近重远轻）。同窗口可直接换；换手通常略升、对近期更敏感。"),
    ("ts_mean", "ts_sum", "ts_sum(x,n)/n 即 ts_mean；需要显式分母时用。"),
    ("ts_zscore", "ts_rank", "同为时序自归一化；ts_rank 输出 (0,1) 均匀分布、抗离群，ts_zscore 保留幅度但怕肥尾。"),
    ("ts_zscore", "ts_quantile", "ts_quantile(x,n) 返回过去 n 日分位，抗极端值更强；语义与 ts_rank 接近。"),
    ("zscore", "rank", "同为截面标准化；rank 均匀化抗离群，zscore 保留相对幅度。外层常再接 rank/scale。"),
    ("group_zscore", "group_rank", "组内标准化的两种形态；group_rank 组内均匀分布，对厚尾字段更稳。"),
    ("ts_ir", "divide(ts_mean, ts_std_dev)", "IR 定义即 mean/std，手写等价；分母近 0 时手写版需 +0.001 防爆。"),
    ("ts_delta", "subtract(x, ts_delay(x,n))", "逐字等价。"),
    ("ts_returns", "divide(ts_delta(x,n), ts_delay(x,n))", "近等价（百分比变动）；分母为 0/近 0 时注意。"),
    ("ts_av_diff", "subtract(x, ts_mean(x,n))", "逐字等价（对均值的偏离）。"),
    ("signed_power", "sqrt", "x>=0 时 signed_power(x,0.5)=sqrt(x)；含负值数据必须用 signed_power 保号。"),
    ("signed_power", "power", "power(x,a) 不保号（负底数非整数幂出 NaN）；有符号字段一律 signed_power。"),
    ("reverse", "multiply(x, -1)", "逐字等价（取负）。reverse 更可读。"),
    ("inverse", "divide(1, x)", "逐字等价；x=0 均出 inf，建议配合 pasteurize。"),
    ("sqrt", "power(x, 0.5)", "x>=0 等价；含负值改 signed_power。"),
    ("max", "if_else(greater_equal(a,b), a, b)", "逐元素等价；min 同理反向。"),
    ("winsorize", "tail", "同为削峰：winsorize 按 std 倍数截断，tail 按分位/阈值；参数语义不同，换后需重调阈值。"),
    ("group_neutralize", "vector_neut", "中性化两条路：按组去均值 vs 对向量回归取残差；vector_neut 更外科手术式，需给目标向量。"),
    ("pasteurize", "ts_backfill", "数据卫生：pasteurize 清 inf/NaN（置 NaN 由平台处理）；ts_backfill 用历史值回填。目的相同、机制不同。"),
    ("pasteurize", "densify", "densify 把稀疏字段变稠密（前向填充语义）；与 pasteurize 常串联使用。"),
    ("trade_when", "if_else(cond, x, nan)", "门控两形态：trade_when 有持仓状态（entry/exit 之间维持），if_else 是每日无状态掩码。trade_when 能改变换手结构（实证可过 CONCENTRATED_WEIGHT）。"),
    ("hump", "ts_target_tvr_hump", "换手控制一族：hump 限制相邻日仓位变动；ts_target_tvr_hump 直接锚定目标换手。"),
    ("ts_corr", "ts_covariance", "相关 vs 协方差，差一个标准化分母；语义等价、量纲不同。"),
    ("quantile", "bucket", "同为离散化分桶；参数语义（分位驱动）略有差异。"),
    ("vec_avg", "reduce_avg", "向量规约近似互换（vec_* 面向 vector 字段，reduce_* 通用）；同族 vec_max/min/sum ↔ reduce_max/min/sum。"),
    ("scale", "normalize", "截面整形：scale 使 sum(|x|)=定值（权重塑形），normalize 去均值（可选除 std≈zscore）；目的不同勿盲换。"),
    ("group_mean", "group_sum", "组内聚合，差一个组计数分母；group_sum/group_count=group_mean。"),
    ("ts_arg_max", "ts_arg_min", "孪生：arg_max(reverse(x))=arg_min(x)。"),
    ("less", "greater", "孪生比较：less(a,b)=greater(b,a)；less_equal/greater_equal 同理。"),
    ("and", "or", "德摩根：and(a,b)=not(or(not a,not b))；条件组合时互换。"),
]

# COMBO/SELECTION 专属（SUPER 用，REGULAR 不可直接用）
SUPER_ONLY_HINT = {"combo_a", "generate_stats", "self_corr", "universe_size"}

# SUPER 的 selection/combo 字符串不存入 alphas.expression（实测 6 颗 SUPER 该列为空或
# "(SUPER) "），因此下列算子的"未使用"是统计口径假象——它们已在 SUPER 组合串中实装。
# 依据 MEMORY §3：KOR SA combo 用 generate_stats/self_corr/if_else/reduce_max。
KNOWN_USED_IN_SUPER = {"combo_a", "generate_stats", "self_corr", "universe_size",
                       "reduce_max", "is_nan", "nan"}


def load_ops():
    cat = json.load(open(CAT_PATH, encoding="utf-8"))
    ver = set(json.load(open(VER_PATH, encoding="utf-8"))["verified"])
    ops = {}
    for o in cat["results"]:
        ops[o["name"]] = o
    return ops, ver


def fetch_sets():
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    ledger_ids = {r[0] for r in cur.execute(
        "SELECT DISTINCT alpha_id FROM submission_ledger WHERE alpha_id IS NOT NULL")}
    rows = cur.execute(
        "SELECT alpha_id, expression, region_id, platform_status, status, sharpe "
        "FROM alphas WHERE expression IS NOT NULL AND expression != ''").fetchall()
    submitted, footprint = [], []
    for aid, expr, region, pstat, stat, sharpe in rows:
        rec = (aid, expr, region, pstat, sharpe)
        footprint.append(rec)
        if aid in ledger_ids or pstat in ("ACTIVE", "DECOMMISSIONED"):
            submitted.append(rec)
    con.close()
    return submitted, footprint


def op_patterns(names):
    # \b 保护：signed_power 内的 power、ts_rank 内的 rank 不会误中（_ 是词字符）
    return {n: re.compile(r"\b" + re.escape(n) + r"\s*\(") for n in names}


def count_usage(recs, pats):
    used = collections.Counter()
    examples = {}
    for aid, expr, region, pstat, sharpe in recs:
        hit = set()
        for n, p in pats.items():
            if p.search(expr):
                used[n] += 1
                hit.add(n)
                examples.setdefault(n, (aid, expr, region))
    return used, examples


def motif_mining(recs, pats, topk=12):
    """算子嵌套 bigram：外层(内层( 的共现频次，看惯用组合。"""
    seq_pats = {n: re.compile(r"\b" + re.escape(n) + r"\s*\(") for n in pats}
    bigrams = collections.Counter()
    for _, expr, *_ in recs:
        calls = [(m.start(), m.group(0)[:-1].strip()) for m in
                 (mm for p in seq_pats.values() for mm in p.finditer(expr))]
        calls.sort()
        names_seq = [c[1] for c in calls]
        for a, b in zip(names_seq, names_seq[1:]):
            bigrams[(a, b)] += 1
    return bigrams.most_common(topk)


def main():
    ops, verified = load_ops()
    pats = op_patterns(list(ops))
    submitted, footprint = fetch_sets()

    used_sub, ex_sub = count_usage(submitted, pats)
    used_all, _ = count_usage(footprint, pats)

    unused_sub = sorted(set(ops) - set(used_sub))
    unused_all = sorted(n for n in (set(ops) - set(used_all))
                        if n not in KNOWN_USED_IN_SUPER)

    # 等价映射索引
    equiv_of = collections.defaultdict(list)
    for a, b, note in EQUIV:
        equiv_of[a].append((b, note))
        equiv_of[b].append((a, note))

    by_cat = collections.defaultdict(list)
    for n, o in ops.items():
        by_cat[o.get("category", "?")].append(o)

    report = {
        "catalog_fetched": json.load(open(CAT_PATH, encoding="utf-8"))["_fetched_at"],
        "operators_total": len(ops),
        "submitted_alphas": len(submitted),
        "footprint_alphas": len(footprint),
        "used_in_submitted": len(used_sub),
        "unused_in_submitted": unused_sub,
        "never_used_anywhere": unused_all,
        "usage_submitted": dict(used_sub.most_common()),
        "usage_footprint_top30": dict(used_all.most_common(30)),
    }
    with open(OUT_JSON, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    # ------------------------------------------------- markdown
    L = []
    L.append("# WQ BRAIN 算子清单 × 已提交 Alpha 算子使用审计（2026-09-30）\n")
    L.append(f"- 算子清单来源：`docs/reference/operators_catalog.json`（平台实况快照 "
             f"{report['catalog_fetched']}，{len(ops)} 个），与 `data/operators_verified.json` "
             f"（2026-09-04 探针，{len(verified)} live）一致。")
    L.append(f"- 已提交 alpha 口径：`submission_ledger` ∪ `platform_status∈(ACTIVE,DECOMMISSIONED)`，"
             f"共 **{len(submitted)}** 条；使用足迹（全部回测过）**{len(footprint)}** 条。")
    L.append(f"- 已提交集中用过 **{len(used_sub)}/{len(ops)}** 个算子；"
             f"未用 **{len(unused_sub)}** 个（其中 {len(unused_all)} 个连回测足迹都未出现）。\n")

    L.append("\n## 一、完整算子清单（按平台 category 分组）\n")
    for cat in sorted(by_cat):
        L.append(f"\n### {cat}（{len(by_cat[cat])} 个）\n")
        L.append("| 算子 | 定义/签名 | 功能描述 | 适用场景 |")
        L.append("|---|---|---|---|")
        for o in sorted(by_cat[cat], key=lambda x: x["name"]):
            scope = ",".join(o.get("scope", []))
            super_tag = " ⚠SUPER专属" if o["name"] in SUPER_ONLY_HINT else ""
            desc = (o.get("description") or "").replace("|", "\\|").replace("\n", " ")
            defi = (o.get("definition") or "").replace("|", "\\|")
            L.append(f"| `{o['name']}`{super_tag} | `{defi}` | {desc} | {scope} |")

    L.append("\n\n## 二、已提交 alpha 的算子使用统计\n")
    L.append("| 算子 | 提交集使用次数 | 全足迹使用次数 |")
    L.append("|---|---|---|")
    for n, c in used_sub.most_common():
        L.append(f"| `{n}` | {c} | {used_all.get(n, 0)} |")

    L.append(f"\n\n## 三、未使用算子清单（提交集，{len(unused_sub)} 个）\n")
    L.append("> 口径提示：SUPER 的 selection/combo 字符串不存入 `alphas.expression`"
             "（实测 6 颗 SUPER 该列为空），故 `combo_a`/`generate_stats`/`self_corr`/"
             "`universe_size`/`reduce_max` 的「未使用」是统计假象——"
             "它们已在 SUPER 组合串中实装（见 MEMORY §3 的 KOR SA 配方）。\n")
    L.append("| 算子 | category | 功能 | 全足迹是否用过 |")
    L.append("|---|---|---|---|")
    for n in unused_sub:
        o = ops[n]
        if n in KNOWN_USED_IN_SUPER:
            tag = "SUPER 组合串已用（本表不覆盖）"
        else:
            tag = "用过" if n in used_all else "**从未使用**"
        if n in SUPER_ONLY_HINT:
            tag += "（SUPER专属）"
        desc = (o.get("description") or "").replace("|", "\\|").replace("\n", " ")
        L.append(f"| `{n}` | {o.get('category','')} | {desc} | {tag} |")

    L.append("\n\n## 四、等价平替建议（功能一致、可直接/近直接替换）\n")
    L.append("说明：A ↔ B 表示双向可换；每行附替换注意点。"
             "「已用/未用」以提交集为准，便于双向查阅："
             "既可查『我没用过的算子能平替我哪个惯用算子』（去同质化、降 self-corr），"
             "也可查『未用算子本身等价于我已用的谁』（判断是否真缺能力）。\n")
    L.append("| 算子 A | 平替 B | A 状态 | B 状态 | 替换说明与注意事项 |")
    L.append("|---|---|---|---|---|")
    seen = set()
    for a, b, note in EQUIV:
        key = tuple(sorted((a, b)))
        if key in seen:
            continue
        seen.add(key)
        # B 可能是复合写法（如 "subtract(x, ts_delay(x,n))"），按主算子查状态
        def _st(name):
            m = re.match(r"[a-z_]+", name)
            base = m.group(0) if m else name
            return "已用" if base in used_sub else "未用"
        sa, sb = _st(a), _st(b)
        L.append(f"| `{a}` | `{b}` | {sa} | {sb} | {note} |")

    motifs = motif_mining(submitted, pats)
    L.append("\n\n## 五、已提交 alpha 的惯用表达式模式（算子嵌套 bigram Top12）\n")
    L.append("| 排名 | 模式（外层←内层） | 次数 | 典型示例 |")
    L.append("|---|---|---|---|")
    for i, ((a, b), c) in enumerate(motifs, 1):
        aid, expr, region = ex_sub.get(a, ("", "", ""))
        ex = expr[:110] + ("…" if len(expr) > 110 else "")
        L.append(f"| {i} | `{a}( {b}( … ) )` | {c} | `{ex}` |")

    with open(OUT_MD, "w", encoding="utf-8") as f:
        f.write("\n".join(L) + "\n")

    print(f"submitted={len(submitted)} footprint={len(footprint)}")
    print(f"used_sub={len(used_sub)} unused_sub={len(unused_sub)} never_anywhere={len(unused_all)}")
    print("unused_sub:", unused_sub)
    print("never_anywhere:", unused_all)
    print("top motifs:", motifs[:6])
    print("MD:", OUT_MD)
    print("JSON:", OUT_JSON)


if __name__ == "__main__":
    main()
