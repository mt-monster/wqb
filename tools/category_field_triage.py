#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""category_field_triage.py — 一个 region×category 下所有数据集的「字段分诊」总表。

把人工要跑的六步（类别景观 → 类型轴 / 语义轴 / 质量轴 / 冷热轴 → 判死 → 历史先验）
压缩成**一条本地命令**，零回测、零 API，输出「这个 category 还值不值得开波、能开在哪个集」。

背景（2026-09-30 KOR/RISK 走查实证）：
  手工走一遍 RISK 分类的结论是「整个 category 不值得开波」——但前提是要同时做到三件事，
  而这三件事靠人做必漏：
  ① 判死查**两源**（`registry_empirical` + `ledger_kv` 的 `*_dead`）。作者第一版只查了
     registry，把 sentiment21 / institutions6 误判成存活。
  ② **族级连坐**：risk88 判死的是「Barra 风格载荷 ri_* 族」，而 risk70 的字段是
     `mfm2_asetrd_*`——同一经济族、只差模型版本号。数据集级判死只封 risk88，
     risk70（96 字段 / 3 甜点 / 跨区 GLB maxS 2.16）会被 s0-select 当优质候选推出去。
     本工具用**字段 description 的关键词签名做 Jaccard** 自动连坐。
  ③ 甜点字段（alphaCount 10~50）与荒地（ac=0 且 uc=0）分开数——57% 的字段是荒地，
     把荒地当机会是已记录的死法。

用法：
    python tools/category_field_triage.py --region KOR --category RISK
    python tools/category_field_triage.py --region KOR --all
    python tools/category_field_triage.py --region KOR --category NEWS,SENTIMENT --json out.json
    python tools/category_field_triage.py --region KOR --all --write-ledger

判级优先级（先命中先定）：
    仅条件腿（字段 < --min-fields） → 判死（两源任一） → 族连坐 → 拥挤（acmax > --crowd-ac）
    → 无甜点字段（ac 10~50 个数为 0） → ★可开波

⚠️ 边界：
  - 纯本地只读（除 --write-ledger）。点塔状态仍须查平台 `get_pyramid_alphas`，
    `datasets.category` ≠ 金字塔塔归属，本工具的 --category 用的是前者。
  - 跨区先验仅作**参考标签**，不参与判级（2026-09-30 P1 实测无预测力）。
  - 产物是「字段池决策」，不是 ideas，禁止当 ideas.md 注入 GEM。
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_HERE)
sys.path.insert(0, os.path.join(_ROOT, "src"))

# 2026-09-30：此处**不得**写 try/except 兜底成裸 sqlite3.connect ——
# ① 兜底会把 readonly=True 原样传给 sqlite3.connect 而当场 TypeError，看似"降级"实则必炸；
# ② 裸连接无 timeout/WAL 统一契约（database is locked 事故根因之一），
#    仓库有静态闸 test_db_write_guards 专门拦这个。导入失败就该响亮失败。
from wqb.db_conn import connect as db_connect  # 规范工厂（唯一连接入口）


DB = os.path.join(_ROOT, "data", "wqb.db")

RA_CLEAN = ("(ABS(COALESCE(sharpe,0))>=? AND COALESCE(fitness,0)>=? "
            "AND COALESCE(TRIM(ra_failed_checks),'') IN ('','[]'))")

# 族签名：丢通用词与**地理/币种词**（否则 risk88 的 "in ASI region" 会把 asi 带进签名，
# 与 risk70 的签名错开，连坐失效），保留 style/factor/loading 这类真正构成族身份的词
_STOP = {"the", "a", "an", "of", "in", "for", "and", "or", "to", "is", "on", "by",
         "with", "region", "regions", "this", "that", "per", "as", "at", "from",
         "be", "are", "it", "its", "not", "no", "all", "any", "total", "net",
         # 地理 / 币种 / 模型版本号（与族身份无关）
         "asi", "asia", "ase", "asean", "us", "usa", "usd", "eur", "europe",
         "jpn", "japan", "kor", "korea", "chn", "china", "hkg", "hong", "kong",
         "twn", "taiwan", "gbr", "uk", "deu", "germany", "amr", "america",
         "glb", "global", "ind", "india", "mea", "apac", "dollars", "dollar"}


def _tokens(text: str):
    return {t for t in re.split(r"[^a-z]+", (text or "").lower())
            if len(t) > 2 and t not in _STOP and not t.isdigit()}


def _doc_freq(descs_map):
    """token 的**文档频率**（出现在多少个数据集里），用于剔除通用词。

    2026-09-30 修正（C 阶段上闸前实测发现的误伤）：族签名若直接取高频词，会把
    **分类级通用词**当成族身份。KOR 实测 DF：
        score 51% / value 48% / company 45% / earnings 32% / model 33%
        ← 这些词遍布各类数据集，不构成任何族的身份；
        loading 2% / style 4% / factor 15%
        ← 这些才是 risk 族的判别词。
    后果：news18/news46/news20/news48 全被连坐到 news50、news17 连坐到 news79 ——
    **整个 NEWS 分类被塌缩成「一族」**，把此前手工分诊里质量最优的 news18 也封掉。
    故按 DF 上限剔除通用词（TF-IDF 的 IDF 侧），只留判别词。
    """
    df = {}
    for _ds, descs in descs_map.items():
        for t in _tokens(" ".join(descs)):
            df[t] = df.get(t, 0) + 1
    return df


def _family_signature(descriptions, df=None, n_docs=0, df_max=0.25, top_n=8):
    """字段 description 的高频关键词集合 = 数据集的『经济族签名』。

    用 description 而非字段名：字段名带数据集私有前缀与模型版本号
    （risk88 的 `rsk88_mfm_ase1_ri_*` vs risk70 的 `rsk70_mfm2_asetrd_*`），
    字符串层面完全不重叠；但 description 都是 "Style Factor Loading"，能连坐。

    df/n_docs 给定时按文档频率剔除通用词（见 _doc_freq）；缺省不剔除（保持旧行为）。
    """
    freq = {}
    for d in descriptions:
        for t in _tokens(d):
            freq[t] = freq.get(t, 0) + 1
    if not freq:
        return set()
    if df and n_docs and df_max:
        freq = {t: c for t, c in freq.items()
                if (df.get(t, 0) / n_docs) <= df_max}
        if not freq:
            return set()
    n = max(len(descriptions), 1)
    keep = sorted(freq.items(), key=lambda kv: (-kv[1], kv[0]))[:top_n]
    return {t for t, c in keep if c / n >= 0.15}


def _jaccard(a, b):
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


def _containment(a, b, min_overlap=3, min_side=3):
    """连坐用**包含度**而非 Jaccard。

    risk70 签名 8 词（factor/loading/industry/style + exposure/model/risk/sector），
    risk88 签名 3 词（factor/loading/industry）→ Jaccard 仅 0.33 会被稀释掉，
    但 risk88 的族内容确实**完全落在** risk70 的族里，包含度 = 1.0。
    连坐的语义正是「小族内容被大族覆盖」，所以用包含度。
    守卫：较小一侧 ≥ min_side 个词、交集 ≥ min_overlap 个词，避免小签名乱套。
    """
    if not a or not b:
        return 0.0
    inter = len(a & b)
    if inter < min_overlap or min(len(a), len(b)) < min_side:
        return 0.0
    return inter / min(len(a), len(b))


def load_rows(conn, region, categories, sharpe_min, fitness_min,
              sweet_lo, sweet_hi):
    cur = conn.cursor()
    sql = """
      SELECT d.name, COALESCE(d.category,'(null)'),
             COUNT(f.id),
             AVG(COALESCE(f.coverage,0)),
             SUM(CASE WHEN f.field_type='MATRIX' THEN 1 ELSE 0 END),
             SUM(CASE WHEN f.field_type='VECTOR' THEN 1 ELSE 0 END),
             SUM(CASE WHEN f.field_type='GROUP'  THEN 1 ELSE 0 END),
             MAX(COALESCE(f.alpha_count,0)),
             SUM(CASE WHEN COALESCE(f.alpha_count,0) BETWEEN ? AND ? THEN 1 ELSE 0 END),
             SUM(CASE WHEN COALESCE(f.alpha_count,0)=0 AND COALESCE(f.user_count,0)=0
                      THEN 1 ELSE 0 END)
      FROM datasets d JOIN regions r ON r.id=d.region_id
      LEFT JOIN fields f ON f.dataset_id=d.id
      WHERE r.name=? {cat_filter}
      GROUP BY d.name, d.category
    """
    args = [sweet_lo, sweet_hi, region]
    if categories:
        ph = ",".join("?" * len(categories))
        sql = sql.format(cat_filter=f"AND UPPER(d.category) IN ({ph})")
        args += [c.upper() for c in categories]
    else:
        sql = sql.format(cat_filter="")
    cur.execute(sql, args)
    out = []
    for name, cat, nf, cov, m, v, g, acmax, sweet, desert in cur.fetchall():
        out.append({"dataset": name, "category": cat, "n_fields": nf or 0,
                    "cov": cov or 0.0, "matrix": m or 0, "vector": v or 0,
                    "group": g or 0, "acmax": acmax or 0, "sweet": sweet or 0,
                    "desert": desert or 0})
    return out


def load_descriptions(conn, region):
    cur = conn.cursor()
    cur.execute("""
      SELECT d.name, f.description FROM fields f
      JOIN datasets d ON d.id=f.dataset_id JOIN regions r ON r.id=d.region_id
      WHERE r.name=?""", (region,))
    m = {}
    for name, desc in cur.fetchall():
        m.setdefault(name, []).append(desc)
    return m


def load_dead(conn, region):
    """判死两源：registry_empirical（模糊命中）+ ledger_kv 的 *_dead（精确键）。

    ⚠ 2026-09-30 修复（C 阶段上闸前实测抓到）：此前 `SELECT entry_id, payload
    FROM registry_empirical WHERE region=?` **完全没过滤 layer**，把 win /
    campaign / orphan 层条目一律当成判死命中。KOR 实测 118 条里只有 77 条是
    dead_end，其余 41 条（含 9 条 **win**）被误判 —— 后果：other466 有 3 条
    win 记录（ACTIVE alpha wpZkk1Mp / A1NXddRw）却被判死，而它正是 KOR 唯一
    近期 ACTIVE alpha 的来源集。**过滤 layer 是正确性的前提，不是优化。**
    """
    cur = conn.cursor()
    cur.execute("""SELECT entry_id, payload FROM registry_empirical
                   WHERE region=? AND LOWER(COALESCE(layer,'')) LIKE '%dead%'""",
                (region,))
    rows = cur.fetchall()
    led = {k[:-5] for (k,) in cur.execute(
        "SELECT key FROM ledger_kv WHERE region=? AND key LIKE '%_dead'", (region,))}
    return {"registry_rows": rows, "ledger": led}


def load_alive(conn, region, sharpe_min, fitness_min):
    """「已有实证产出」的集：本地 ra_clean>0，或 registry 有 win 层记录命中该集。

    为什么需要这个（2026-09-30 实测，是本工具最重要的一条防线）：
    **判死记录是族级的，不是集级的。** payload 的 rule 写得清清楚楚——
    「analyst44 **一致预期类**字段…不再投任何变体」「analyst10 **innovation_score 族**…」，
    同一数据集的其他族照样活着。KOR 实证：3 个有 ra_clean 产出的集
    （other466=16 / analyst44=8 / analyst10=5）**全是判死**，若无条件硬拦，
    会 100% 误杀 KOR 的全部历史产出（29/29 条 ra_clean）。
    故：有实证产出的集**一律不阻断**，只把判死标签摆出来给人看。
    """
    cur = conn.cursor()
    cur.execute(f"""SELECT dataset, SUM(CASE WHEN {RA_CLEAN} THEN 1 ELSE 0 END) c
                    FROM backtest_results WHERE region=? AND dataset IS NOT NULL
                    GROUP BY dataset""", (sharpe_min, fitness_min, region))
    ra = {ds: (c or 0) for ds, c in cur.fetchall()}
    cur.execute("""SELECT COALESCE(entry_id,'') || ' ' || COALESCE(payload,'')
                   FROM registry_empirical
                   WHERE region=? AND LOWER(COALESCE(layer,'')) LIKE '%win%'""",
                (region,))
    win_blob = " ".join(r[0] for r in cur.fetchall())
    return ra, win_blob


def load_local(conn, region, sharpe_min, fitness_min):
    cur = conn.cursor()
    cur.execute(f"""
      SELECT dataset, COUNT(*), MAX(ABS(COALESCE(sharpe,0))),
             SUM(CASE WHEN {RA_CLEAN} THEN 1 ELSE 0 END)
      FROM backtest_results WHERE region=? AND dataset IS NOT NULL
      GROUP BY dataset""", (sharpe_min, fitness_min, region))
    return {r[0]: {"bt": r[1], "maxS": r[2] or 0.0, "ra_clean": r[3] or 0}
            for r in cur.fetchall()}


def load_cross(conn, region, sharpe_min, fitness_min, xr_min_bt, xr_weak_sharpe):
    cur = conn.cursor()
    cur.execute(f"""
      SELECT dataset, region, COUNT(*), MAX(ABS(COALESCE(sharpe,0))),
             SUM(CASE WHEN {RA_CLEAN} THEN 1 ELSE 0 END)
      FROM backtest_results WHERE region<>? AND dataset IS NOT NULL
      GROUP BY dataset, region""", (sharpe_min, fitness_min, region))
    out = {}
    for ds, reg, bt, mx, rc in cur.fetchall():
        e = out.setdefault(ds, {"weak": [], "strong": []})
        if (rc or 0) > 0:
            e["strong"].append(f"{reg}:{rc}")
        elif bt >= xr_min_bt and (mx or 0) < xr_weak_sharpe:
            e["weak"].append(f"{reg}:{(mx or 0):.2f}@{bt}")
    return out


def triage(conn, region, categories, args):
    rows = load_rows(conn, region, categories, args.sharpe_min, args.fitness_min,
                     args.sweet_lo, args.sweet_hi)
    descs = load_descriptions(conn, region)
    dead = load_dead(conn, region)
    local = load_local(conn, region, args.sharpe_min, args.fitness_min)
    ra_hist, win_blob = load_alive(conn, region, args.sharpe_min, args.fitness_min)
    cross = load_cross(conn, region, args.sharpe_min, args.fitness_min,
                       args.xr_min_bt, args.xr_weak_sharpe)

    # ---- 族签名 → 判死数据集的连坐 ----
    df = _doc_freq(descs)
    n_docs = len(descs)
    sigs = {r["dataset"]: _family_signature(descs.get(r["dataset"], []),
                                            df, n_docs, args.df_max_ratio)
            for r in rows}
    dead_set, dead_reason = set(), {}
    for r in rows:
        ds = r["dataset"]
        hits = [e for e, p in dead["registry_rows"] if ds in e or ds in str(p)]
        if ds in dead["ledger"]:
            hits.append("ledger:<ds>_dead")
        if hits:
            dead_set.add(ds)
            dead_reason[ds] = hits

    contagion = {}
    for r in rows:
        ds = r["dataset"]
        if ds in dead_set:
            continue
        best = (0.0, None)
        for src in dead_set:
            s = _containment(sigs.get(ds, set()), sigs.get(src, set()))
            if s > best[0]:
                best = (s, src)
        if best[0] >= args.family_sim:
            contagion[ds] = best

    # ---- 判级 ----
    for r in rows:
        ds, nf = r["dataset"], r["n_fields"]
        tags = []
        if nf < args.min_fields:
            verdict = "仅条件腿"
            tags.append(f"fields<{args.min_fields}")
        elif ds in dead_set:
            verdict = "判死"
            tags.append(f"判死×{len(dead_reason[ds])}")
        elif ds in contagion:
            sim, src = contagion[ds]
            verdict = "族连坐"
            tags.append(f"同族({src},包含={sim:.2f})")
        elif r["acmax"] > args.crowd_ac:
            verdict = "拥挤"
            tags.append(f"acmax={r['acmax']}(prod墙)")
        elif r["sweet"] == 0:
            verdict = "无甜点字段"
        else:
            verdict = "★可开波"
        loc = local.get(ds)
        if loc:
            tags.append(f"bt={loc['bt']},maxS={loc['maxS']:.2f},ra={loc['ra_clean']}")
        xr = cross.get(ds)
        if xr:
            if xr["weak"]:
                tags.append("跨区弱(参考):" + ",".join(xr["weak"][:2]))
            if xr["strong"]:
                tags.append("跨区强(参考):" + ",".join(xr["strong"][:2]))
        if r["n_fields"] and r["desert"] / r["n_fields"] >= args.desert_ratio:
            tags.append(f"荒地{r['desert']/r['n_fields']:.0%}")
        # 「已有实证产出」豁免：判死是族级的，同集其他族仍可能活（见 load_alive 注释）。
        n_ra = ra_hist.get(ds, 0)
        has_win = ds in win_blob
        if n_ra > 0 or has_win:
            tags.append("实证产出(ra=%d%s)" % (n_ra, ",win" if has_win else ""))
        block = (verdict != "★可开波") and not (n_ra > 0 or has_win)
        r.update({"verdict": verdict, "tags": tags, "local": loc, "block": block,
                  "dead_hits": dead_reason.get(ds, []),
                  "contagion": contagion.get(ds),
                  "family_sig": sorted(sigs.get(ds, set()))})
    order = {"★可开波": 0, "拥挤": 1, "无甜点字段": 2, "族连坐": 3, "判死": 4, "仅条件腿": 5}
    rows.sort(key=lambda x: (not x["block"], order.get(x["verdict"], 9), -x["n_fields"]))
    return rows


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--region", required=True)
    ap.add_argument("--category", default=None,
                    help="逗号分隔，如 RISK,NEWS；缺省全部分类")
    ap.add_argument("--all", dest="all_cat", action="store_true",
                    help="扫全部 category（缺省行为，显式写出更清楚）")
    ap.add_argument("--min-fields", type=int, default=5,
                    help="字段数低于此值判「仅条件腿」（默认 5）")
    ap.add_argument("--crowd-ac", type=int, default=1000,
                    help="acmax 超过此值判「拥挤」（默认 1000）")
    ap.add_argument("--sweet-lo", type=int, default=10)
    ap.add_argument("--sweet-hi", type=int, default=50,
                    help="甜点区间 alphaCount∈[lo,hi]（默认 10~50）")
    ap.add_argument("--desert-ratio", type=float, default=0.6,
                    help="荒地字段占比超过此值打标签（默认 0.6）")
    ap.add_argument("--family-sim", type=float, default=0.7,
                    help="族签名包含度阈值，≥此值即连坐（默认 0.7；见 _containment 注释）")
    ap.add_argument("--df-max", dest="df_max_ratio", type=float, default=0.25,
                    help="族签名剔除通用词的文档频率上限（默认 0.25）：出现在超过该比例的"
                         "数据集里的词视为分类级通用词，不作族身份。"
                         "KOR 实测 score=51%%/value=48%%/earnings=32%%（通用）vs "
                         "loading=2%%/style=4%%（判别）；不过滤会把整个 NEWS 塌缩成一族")
    ap.add_argument("--sharpe-min", type=float, default=1.58)
    ap.add_argument("--fitness-min", type=float, default=1.0)
    ap.add_argument("--xr-min-bt", type=int, default=16)
    ap.add_argument("--xr-weak-sharpe", type=float, default=1.0)
    ap.add_argument("--top", type=int, default=60, help="最多打印几行")
    ap.add_argument("--survivors-only", action="store_true")
    ap.add_argument("--write-ledger", action="store_true",
                    help="写 ledger s1_triage_<region>")
    ap.add_argument("--json", dest="json_out")
    a = ap.parse_args()

    cats = [c.strip() for c in a.category.split(",") if c.strip()] if a.category else None
    conn = db_connect(db=DB, readonly=True)  # 规范工厂；只读契约
    rows = triage(conn, a.region, cats, a)
    conn.close()

    shown = [r for r in rows if r["verdict"] == "★可开波"] if a.survivors_only else rows
    print(f"=== 字段分诊 {a.region}"
          f"{'/'+','.join(cats) if cats else '（全分类）'} ===")
    print(f"{'dataset':24s} {'cat':13s} {'字段':>5} {'覆盖':>6} {'VEC':>5} "
          f"{'acmax':>6} {'甜点':>5} {'荒地':>5}  verdict   备注")
    for r in shown[:a.top]:
        print(f"{r['dataset'][:24]:24s} {r['category'][:13]:13s} {r['n_fields']:>5} "
              f"{r['cov']:>6.3f} {r['vector']:>5} {r['acmax']:>6} {r['sweet']:>5} "
              f"{r['desert']:>5}  {r['verdict']:10s} {'; '.join(r['tags'])[:56]}")

    surv = [r["dataset"] for r in rows if r["verdict"] == "★可开波"]
    print(f"\n扫描 {len(rows)} 集 → 存活 {len(surv)} 集")
    if surv:
        print("存活:", ", ".join(surv))
    else:
        print("[WARN] 无可开波数据集 —— 建议换 category 或换区域，不要在已耗尽的池子里打磨",
              file=sys.stderr)
    cont = [r for r in rows if r["verdict"] == "族连坐"]
    if cont:
        print(f"\n[族级连坐 {len(cont)} 集] 数据集级判死漏网、靠族签名抓到的：")
        for r in cont:
            sim, src = r["contagion"]
            print(f"  {r['dataset']:22s} ← 同族 {src} (包含度={sim:.2f}) "
                  f"族签名={r['family_sig'][:5]}")

    if a.json_out:
        os.makedirs(os.path.dirname(a.json_out) or ".", exist_ok=True)
        json.dump({"region": a.region, "categories": cats, "rows": rows,
                   "survivors": surv}, open(a.json_out, "w", encoding="utf-8"),
                  ensure_ascii=False, indent=2)
        print(f"\n[out] {a.json_out}")

    if a.write_ledger:
        # 规范写入口 = CampaignStore.upsert_ledger（唯一 ledger_kv 写路径，见
        # tools/field_profile_from_labs.py:73 同款用法）。
        # ⚠️ 2026-09-30 修正：初版写的是 `from wqb.ledger import upsert_ledger_key`
        # —— 该模块不存在，except 兜底后只打 WARN 并返回 0，形成「假成功」：
        # 用户以为台账写了、下游 C 阶段去读 s1_triage_<region> 却永远读不到。
        # 写入口不可达必须**失败退出**（非 0），不能降级。
        try:
            import os as _os_sc
            # 与 campaign_intel/wave_gate/scan_fields 等 6 处同款：启动自检每进程只打一次
            # （ensure_schema 会打 wave-key/wave-ttl 告警，与本工具的分诊结论无关，
            #  混在报告尾部易被误读成分诊输出）
            _os_sc.environ.setdefault("WQB_STARTUP_CHECKS", "once")
            from wqb.store.campaign import CampaignStore
            store = CampaignStore.from_workspace(_ROOT)
        except Exception as e:
            print(f"[ERROR] 台账写入口不可达，未写入：{e}", file=sys.stderr)
            return 2
        try:
            import datetime as _dt
            key = f"s1_triage_{a.region.lower()}"
            # ⚠ verdicts 是**全量判级表**（不只 survivors）——步 3 入口闸 TRI 靠它判定：
            # 数据集不在表里 = unknown，按 fail-closed 阻断（只存 survivors 会让
            # "表里没有"和"不是存活"两种状态无法区分，闸就只能放行，等于没闸）。
            store.upsert_ledger(a.region, key, {
                "generated_by": "tools/category_field_triage.py",
                "generated_at": _dt.datetime.now().isoformat(timespec="seconds"),
                "region": a.region,
                "categories": cats, "scanned": len(rows),
                "survivors": surv,
                "contagion": {r["dataset"]: {"from": r["contagion"][1],
                                             "sim": r["contagion"][0]}
                              for r in cont},
                "verdicts": {r["dataset"]: {"verdict": r["verdict"],
                                            "tags": "; ".join(r["tags"]),
                                            # 闸的判定依据：只有 block=True 才阻断
                                            "block": bool(r["block"])}
                             for r in rows},
            })
            print(f"[ledger] {a.region}/{key} 已写入")
        finally:
            store.close()
    return 0


if __name__ == "__main__":
    main()
