# -*- coding: utf-8 -*-
"""build_cluster_variants.py — 生成"刻意版"Cluster 变体（低门槛区优先）。

依据（2026-09-19 学习帖 43562853669655《Cluster Alpha Research》§3–4）：
- **cluster 建房式 = `rank(group_mean(信号, 权重, 分组))`**：`group_mean` 聚合+广播造行业信号，
  再用**市场级** `rank`（**不是** group 算子）跨行业打分。
- **反例**：`group_rank`/`group_zscore`/`group_scale` 是"行业内选股"，不是 cluster；
  `group_neutralize` 与 **INDUSTRY/SUBINDUSTRY 中性化**会按构造删掉行业结构 →
  本工具产出的 settings **强制 neutralization=MARKET**（否则前功尽弃）。
- 门槛两档：**KOR/JPS/TWN/HKG/IND/GBR/DEU ≥1.0**，其余 ≥1.58。
- 实证动机：账号里 73 条 alpha 有 `cluster_test` 值、**60 条达标**，但其中**没有一条**
  用 `group_mean` —— 即徽章此前都是"顺带"拿到的；本工具补的是**刻意版**。

配方（`--recipes`）：
  cross   横截面轮动：rank(group_mean(SIG, cap, industry))
  equal   等权行业（M&G 1999：等权把行业动量 0.43→0.81%/月）：
          rank(group_normalize(group_mean(SIG, cap, industry), industry))
  guard   防薄行业（<5 只的"行业"是噪声）：
          trade_when(group_count(SIG, industry) > 5, rank(group_mean(SIG, cap, industry)), -1)
  timing  区域级轮动×择时（不依赖源信号，每区只出 1 条）：
          rank(group_mean(ts_delta(close, 126), cap, industry))
            * (ts_mean(group_mean(returns, cap, industry), 22) > 0)

产出前**逐条过当前门禁**（`gate.check_one`，注入 `_region` 以触发闸2b 区域 group 字段校验），
只输出通过者，并报告拒绝原因 —— 避免把注定被拦的候选喂给回测。
**JPN 已排除**：闸2b 实测 JPN 不支持 industry/sector/subindustry（平台 Invalid data field，整批连坐）。

用法：
  python tools/build_cluster_variants.py --region IND --limit 40 \
      --out logs/ind_cluster_variants.json --settings-json logs/ind_cluster_settings.json
  python tools/mcp_7slot_batch.py --alpha-json logs/ind_cluster_variants.json \
      --settings-json logs/ind_cluster_settings.json --output-csv tracking/IND/results/cluster_reps.csv
"""
import sys as _sys, os as _os
_sys.path.insert(0, str(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..', '..', 'src')))
from wqb.db_conn import connect as db_connect  # 规范工厂（2026-09-20 L1 收口）
import argparse
import json
import os
import sqlite3
import sys

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
TK = os.path.join(REPO, "Claude", "skills", "wq-brain-campaign-toolkit", "scripts")

#: 低门槛区（文章：Cluster Sharpe ≥1.0）；JPN 因闸2b 已排除
LOW_BAR_REGIONS = ("IND", "DEU", "GBR", "KOR", "HKG", "JPS", "TWN")
#: 闸2b 明确禁用 group 字段的区域（platform_constraints.region_invalid_group_fields）
BLOCKED_GROUP_REGIONS = ("JPN",)

PER_SOURCE_RECIPES = {
    "cross": "rank(group_mean({sig}, cap, industry))",
    "equal": "rank(group_normalize(group_mean({sig}, cap, industry), industry))",
    "guard": "trade_when(group_count({sig}, industry) > 5, "
             "rank(group_mean({sig}, cap, industry)), -1)",
}
REGION_RECIPES = {
    # 轮动 × 择时（文章 §4.2 的合成式）；不依赖源信号，每区一条
    "timing": "rank(group_mean(ts_delta(close, 126), cap, industry))"
              " * (ts_mean(group_mean(returns, cap, industry), 22) > 0)",
}


def load_gate():
    sys.path.insert(0, TK)
    import gate  # noqa: PLC0415
    pc_path = os.path.join(TK, "..", "config", "platform_constraints.json")
    with open(pc_path, encoding="utf-8") as f:
        pc = json.load(f)
    return gate, pc


def verify(expr, dataset, region, gate, pc, wl_cache, ctx):
    """逐条过门禁；返回 (ok, issues)。注入 `_region` 以启用闸2b 区域校验。"""
    import contextlib
    import io as _io
    pc2 = dict(pc)
    pc2["_region"] = region
    if dataset not in wl_cache:
        try:
            with contextlib.redirect_stdout(_io.StringIO()):
                wl_cache[dataset] = gate.load_whitelist(ctx, dataset)
        except Exception:
            wl_cache[dataset] = None
    wl = wl_cache[dataset]
    if wl is None:
        return False, ["[CATALOG] 数据集无 typed catalog"]
    out = gate.check_one(expr, wl, dataset, [], pc2)
    return bool(out.get("pass")), out.get("issues") or []


def main():
    ap = argparse.ArgumentParser(description="生成刻意版 Cluster 变体（只读源 + 门禁预检）")
    ap.add_argument("--region", required=True)
    ap.add_argument("--status", default="gated", help="源信号状态（默认 gated：过闸未回测）")
    ap.add_argument("--per-skeleton", type=int, default=1, help="每个骨架取几条源信号")
    ap.add_argument("--limit", type=int, default=40, help="最多用多少条源信号（0=不限）")
    ap.add_argument("--recipes", default="cross,equal,guard,timing")
    ap.add_argument("--out", required=True, help="产出 JSON（可直接喂 mcp_7slot_batch --alpha-json）")
    ap.add_argument("--settings-json", required=True, help="产出公共 settings（neutralization 强制 MARKET）")
    ap.add_argument("--db", default=os.path.join(REPO, "data", "wqb.db"))
    a = ap.parse_args()

    region = a.region.upper()
    if region in BLOCKED_GROUP_REGIONS:
        raise SystemExit(f"[拒绝] {region} 在闸2b 名单内（不支持 industry/sector/subindustry，"
                         f"平台 Invalid data field 会整批连坐）→ cluster 线不适用")

    recipes = [r.strip() for r in a.recipes.split(",") if r.strip()]
    conn = db_connect(a.db)
    src = conn.execute(
        "SELECT expression, dataset, skeleton FROM expressions "
        "WHERE region=? AND status=? AND expression IS NOT NULL AND expression<>'' "
        "ORDER BY id", (region, a.status)).fetchall()
    conn.close()

    seen_sk, sources = set(), []
    for expr, ds, sk in src:
        if sk in seen_sk:
            continue
        seen_sk.add(sk)
        sources.append((expr, ds or ""))
        if a.limit and len(sources) >= a.limit:
            break
    print(f"{region}/{a.status} 源信号：候选骨架去重后取 {len(sources)} 条")

    # 载入门禁与战役上下文
    gate, pc = load_gate()
    from _lib.common import CampaignContext
    import contextlib
    import io as _io
    cdir = os.path.join(REPO, "tracking", region)
    with contextlib.redirect_stdout(_io.StringIO()):
        ctx = CampaignContext(cdir)
    wl_cache = {}

    emitted, rejected = [], []
    seen_expr = set()

    for recipe in recipes:
        if recipe in REGION_RECIPES:
            expr = REGION_RECIPES[recipe]
            ok, issues = verify(expr, sources[0][1] if sources else "", region,
                                gate, pc, wl_cache, ctx)
            rec = {"expression": expr, "dataset": sources[0][1] if sources else "",
                   "recipe": recipe, "source": "(region-level)"}
            (emitted if ok else rejected).append(rec if ok else {**rec, "issues": issues})
            seen_expr.add(expr)
            continue
        tpl = PER_SOURCE_RECIPES.get(recipe)
        if not tpl:
            print(f"  ⚠ 未知配方 {recipe}，跳过")
            continue
        for sexpr, sds in sources:
            expr = tpl.format(sig=sexpr)
            if expr in seen_expr:
                continue
            seen_expr.add(expr)
            ok, issues = verify(expr, sds, region, gate, pc, wl_cache, ctx)
            rec = {"expression": expr, "dataset": sds, "recipe": recipe,
                   "source_expression": sexpr}
            if ok:
                emitted.append(rec)
            else:
                rejected.append({**rec, "issues": issues})

    print(f"\n门禁预检：通过 {len(emitted)} / 拒绝 {len(rejected)}")
    reasons = {}
    for r in rejected:
        for i in r.get("issues") or []:
            tag = str(i).split("]")[0].replace("[", "")
            reasons[tag] = reasons.get(tag, 0) + 1
    if reasons:
        print("  拒绝原因:", reasons)
    for r in rejected[:3]:
        print(f"   ✗ [{r['recipe']}] {str(r['issues'])[:110]}")

    with open(a.out, "w", encoding="utf-8") as f:
        json.dump(emitted, f, ensure_ascii=False, indent=1)
    print(f"\n已写入 {a.out}（{len(emitted)} 条）")
    for r in emitted[:5]:
        print(f"   → [{r['recipe']}] {r['expression'][:110]}")

    # settings：继承区域设置，但 neutralization 强制 MARKET（文章 §3.4：行业中性化=自毁）
    s_path = os.path.join(cdir, "config", "settings.json")
    with open(s_path, encoding="utf-8") as f:
        st = json.load(f)
    st["neutralization"] = "MARKET"
    st["_note"] = ("cluster 变体专用：neutralization 覆盖为 MARKET —— "
                   "INDUSTRY/SUBINDUSTRY 会按构造删除行业结构（帖 43562853669655 §3.4）")
    with open(a.settings_json, "w", encoding="utf-8") as f:
        json.dump(st, f, ensure_ascii=False, indent=1)
    print(f"已写入 {a.settings_json}（neutralization=MARKET，原值={json.load(open(s_path, encoding='utf-8')).get('neutralization')}）")


if __name__ == "__main__":
    main()
