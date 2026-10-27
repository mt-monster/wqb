#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""EUR 全数据集 · 全模板族流水线（带断点续跑）

每个数据集执行：
  1. 维度地图（semantic_family / sem_type 分组）
  2. 每维度取 3 个代表字段（优先高覆盖 + 名字去重前缀）
  3. 8 个模板族 × 频率匹配窗口 + VECTOR 自动聚合
  4. 派发（≤10/批，同一设置：FAST/decay4/TopCS1600/trunc0.08）
  5. 收割 → 记录每模板 max_S / max_2Y / 全局 max_S → 判 verdict
  6. 写 checkpoint（原子写）

用法：
  python tools/full_template_campaign.py                 # 从断点继续
  python tools/full_template_campaign.py --datasets risk60 predictive_starmine
  python tools/full_template_campaign.py --limit 10      # 只跑 EV 榜前 10
  WQB_CAMPAIGN_FRESH=1 python tools/full_template_campaign.py   # 忽略断点全新跑
"""
import os
import sys
import json
import re
import asyncio
import sqlite3
import subprocess
import collections
import time
from datetime import datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB = os.path.join(ROOT, "data", "wqb.db")
VENV_PY = os.path.join(ROOT, "world-quant-brain-mcp", ".venv", "Scripts", "python.exe")

# 连接一律走规范工厂（2026-10-27）。本文件被 `export_fields_for_tagging.py` 当模块 import，
# 故把 src 自举放在模块级，两个入口共享同一份路径处理（AGENTS.md §8.4 第 11 项）。
sys.path.insert(0, os.path.join(ROOT, "src"))
from wqb.db_conn import connect as db_connect  # noqa: E402
# wqb-scripts/ 按仓库铁律住在仓库外，路径由 $WQB_SCRIPTS 或 ~/wqb-scripts/ 推导，禁硬编码本机盘符
_WQB_SCRIPTS_DIR = os.environ.get("WQB_SCRIPTS") or os.path.join(os.path.expanduser("~"), "wqb-scripts")
WQB_TOOLS = os.path.join(_WQB_SCRIPTS_DIR, "wqb_tools.py")
CKPT = os.path.join(ROOT, "results", "full_template_campaign_checkpoint.json")
LOG = os.path.join(ROOT, "results", "full_template_campaign_results.json")
DIGEST = os.path.join(ROOT, "results", "campaign_digest.md")
PROGRESS = os.path.join(ROOT, "results", "campaign_progress.json")
HEARTBEAT = os.path.join(ROOT, "cache", "campaign_heartbeat.json")


def emit_digest(ds, cat, res, ck, total):
    """每个集跑完 → 追加一行 digest + 重写 progress.json，并打印「总体情况」块。"""
    rs = res.get("results") or {}
    cur = rs.get(ds) or {}
    done_set = set(ck.get("done") or []) or set(rs)
    # 只统计本 campaign 的 done 集（results.json 里可能残留历史批次）
    rs = {k: v for k, v in rs.items() if k in done_set}
    vc = collections.Counter(v.get("verdict") for v in rs.values() if isinstance(v, dict))
    ranked = [(k, v) for k, v in rs.items()
              if isinstance(v, dict) and v.get("max_s") is not None]
    ranked.sort(key=lambda kv: -(kv[1].get("max_s") or -9))
    # 距交付最近：**逐 alpha 判**（不能拿集级 max_S × max_2Y 拼，那是两颗不同 alpha）
    cands = []
    for k, v in ranked:
        for a in (v.get("alphas") or []):
            s, y2 = a.get("s"), a.get("y2")
            if s is not None and y2 is not None and s >= 1.5 and y2 >= 1.58:
                cands.append({"ds": k, "alpha": a.get("alpha"), "S": s, "F": a.get("f"),
                              "2Y": y2, "sub": a.get("sub"), "tpl": a.get("tpl"),
                              "fragile": bool((v.get("year_profile") or {}).get("fragile")),
                              # EUR 区域闸：sub_universe ≥ 0.53×S
                              "sub_ok": (a.get("sub") is not None and a["sub"] >= 0.53 * s)})
    cands.sort(key=lambda x: -x["S"])
    near = cands

    _yp = cur.get("year_profile") or {}
    _frag = ("frag=✗" if _yp.get("fragile") else ("frag=✓" if _yp else "frag=?"))
    line = (f"- {datetime.now():%m-%d %H:%M} **{ds}**({cat}) → {cur.get('verdict')} "
            f"S={cur.get('max_s')} 2Y={cur.get('max_2y')} joint={cur.get('n_joint')} "
            f"n={cur.get('n_alphas')} prod={cur.get('prod_top')} {_frag}"
            + (f" y0={_yp.get('first_year')} top={_yp.get('top_share')}" if _yp else ""))
    try:
        # 缺陷6修复：同一集重跑时**替换**原行，不追加（否则 digest 行数 ≠ done 数，汇报口径污染）
        keep = []
        if os.path.exists(DIGEST):
            with open(DIGEST, encoding="utf-8") as f:
                keep = [l for l in f if f"**{ds}**(" not in l]
        keep.append(line + "\n")
        tmp = DIGEST + ".tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            f.writelines(keep)
        os.replace(tmp, DIGEST)
    except Exception:
        pass

    prog = {
        "updated_at": datetime.now().isoformat(timespec="seconds"),
        "last_dataset": ds, "last_category": cat,
        "last": {k: cur.get(k) for k in ("verdict", "max_s", "max_2y", "n_joint",
                                         "n_alphas", "prod_top", "coverage")},
        "done": len(ck.get("done") or []), "total": total,
        "verdicts": dict(vc),
        "near_delivery": near[:10],
        "top_s": [{"ds": k, "S": v.get("max_s"), "2Y": v.get("max_2y"),
                   "prod": v.get("prod_top"), "verdict": v.get("verdict")}
                  for k, v in ranked[:10]],
    }
    try:
        tmp = PROGRESS + ".tmp"
        json.dump(prog, open(tmp, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        os.replace(tmp, PROGRESS)
    except Exception:
        pass

    top3 = "  ".join(f"{k}:{v.get('max_s')}" for k, v in ranked[:3])
    print(f"\n  ┌─ 总体情况（{len(ck.get('done') or [])}/{total} 个集完成）")
    print(f"  │ 判定分布 " + " ".join(f"{k}={n}" for k, n in sorted(vc.items(), key=lambda x: -x[1])))
    print(f"  │ 全局最高 S  {top3}")
    n_subok = sum(1 for c in near if c.get("sub_ok"))
    print(f"  │ 距交付最近(S≥1.5&2Y≥1.58 逐 alpha) {len(near)} 颗，其中 sub 过闸 {n_subok} 颗"
          + (": " + ", ".join(f"{c['ds']}/{c['alpha']}(S{c['S']},2Y{c['2Y']}{'' if c.get('sub_ok') else ',sub✗'})" for c in near[:4]) if near else ""))
    print(f"  └─ 本集 {ds}: {cur.get('verdict')}  S={cur.get('max_s')}  "
          f"2Y={cur.get('max_2y')}  joint={cur.get('n_joint')}  prod={cur.get('prod_top')}\n")

# ---------------- 分层模板架构（2026-10-21 修复）----------------
# 修复：旧 8 族把 L1（信号提取）× L2（归一化）焊死（cs=zscore+power、rk=rank 不交叉），
# 且缺 L4（截面处理）层。现拆层：L1×L2 交叉采样为 12 族；L4 由阶段 2 后处理电池接管。
L1_EXTRACT = {
    "lvl": "ts_backfill({F}, {BF})",                                   # 水平
    "d1": "ts_delta(ts_backfill({F}, {BF}), {W1})",                     # 一阶差分
    "d2": "ts_delta(ts_delta(ts_backfill({F}, {BF}), {W1}), {W1})",     # 二阶差分
    "ed": "ts_decay_linear(ts_backfill({F}, 252), 63)",                 # 事件衰减
    "ir": "ts_ir(ts_backfill({F}, {BF}), {ZW})",                        # 信噪比
    "dsp": "ts_backfill(vec_stddev({FR}), {BF})",                       # 组内离散度（仅 VECTOR）
}
L2_NORM = {
    "rk": "rank({X})",
    "zs": "ts_zscore({X}, {ZW})",
    "qt": "ts_quantile({X}, {ZW})",
    "tr": "ts_rank({X}, {ZW})",
    "sc": "ts_scale({X}, {ZW})",
}
# 组合表（标定实证筛选）：(L1, L2)；va=波动调整特例；dw=L3 特殊结构
FAMILIES = [
    ("lvl", "rk"), ("lvl", "zs"), ("lvl", "qt"), ("lvl", "tr"), ("lvl", "sc"),
    ("d1", "rk"), ("d1", "va"),
    ("d2", "rk"),
    ("ed", "rk"),
    ("ir", None),
    ("dsp", "rk"),
]
DW_TPL = "multiply(rank(ts_mean(ts_backfill({F}, {BF}), {WS})), rank(ts_mean(ts_backfill({F}, {BF}), {WL})))"
VA_TPL = "divide(ts_delta(ts_backfill({F}, {BF}), {W1}), add(ts_std_dev(ts_backfill({F}, {BF}), {ZW}), 0.0001))"

FREQ_WIN = {  # backfill, short, long, zwindow, delta_win
    "daily":   (22, 5, 66, 126, 22),
    "weekly":  (66, 21, 126, 252, 21),
    "monthly": (66, 21, 126, 252, 21),
    "quarterly": (252, 63, 252, 504, 63),
    "semi-annual": (252, 126, 504, 504, 126),
    "annual":  (252, 126, 504, 504, 126),
    "unknown": (66, 21, 126, 252, 21),
}

DS_FREQ = {  # 从数据集画像推断
    "intraday_pv_feats": "daily", "pv1": "daily", "pv20": "daily", "pv13": "weekly",
    "pv87": "daily", "risk60": "daily", "risk68": "daily",
    "news17": "monthly", "news20": "monthly",
}

# ---- 字段语义层（2026-10-24 拆至 campaign_semantics.py，单一事实源）----
# ⚠ 必须先把本文件所在目录插进 sys.path：直接 `python tools/xxx.py` 运行时
#   sys.path[0] 就是 tools/，但用 importlib.spec_from_file_location 加载本模块时
#   （分析脚本 / 单测都这么干）sys.path 里没有 tools/，会 ModuleNotFoundError。
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from campaign_semantics import (  # noqa: E402,F401
    LIT_THRESHOLD, VIRGIN_AC, VIRGIN_VS, VIRGIN_MIN_COV, is_virgin, exposure_profile,
    NAME_META, is_name_metadata, classify_desc,
    FORM_FAMILIES, GATED_CATS, GATE_Q, POSTPROC_Q, PER_DIM, MIN_FIELDS_TOTAL,
    FULL_FIELD_CAP, BLACKBOX_FAMILIES, field_tier,
    FAMILY_EXPOSURE, EXPOSURE_VOCAB, EXPR_EXPOSURE, field_exposure_hint,
    CONCEPT_FAMILIES, CONCEPT_ZH, field_concepts, concept_families,
    PP_VOCAB, parse_preprocessing, load_s1_preprocessing, apply_preprocessing,
    _DESC_NOISE, clean_desc, _load_form_overrides, _load_llm_tags, LLM_CONF_MIN,
    FORM_EVIDENCE, field_form, print_form_audit,
    all_datasets,  # 2026-10-27：L1339 调用了但未导入，每次启动必 NameError 崩溃
)

# ---------------------------------------------------------------- 断点


def load_ckpt():
    if os.environ.get("WQB_CAMPAIGN_FRESH"):
        return {"done": [], "sims": {}}
    if os.path.exists(CKPT):
        try:
            return json.load(open(CKPT, encoding="utf-8"))
        except Exception:
            pass
    return {"done": [], "sims": {}}


def save_ckpt(ck):
    os.makedirs(os.path.dirname(CKPT), exist_ok=True)
    tmp = CKPT + ".tmp"
    json.dump(ck, open(tmp, "w", encoding="utf-8"), ensure_ascii=False)
    os.replace(tmp, CKPT)


def load_results():
    if os.path.exists(LOG):
        try:
            return json.load(open(LOG, encoding="utf-8"))
        except Exception:
            pass
    return {"results": {}}


def save_results(res):
    """原子写回 results 台账。

    ★ 2026-10-27 防覆盖（P0）：`main()` 只在启动时 `load_results()` **一次**，
    之后每次 save 都把内存快照整体写回。长跑期间任何**其它进程**对本文件的
    写入（提交脚本补条目、repair 脚本恢复受损集、人工修台账）都会在下一次
    save 时被静默抹掉——10-27 实测：campaign 14:04 启动，14:07 由外部插入的
    `starmine_pv_hybrid`（已提交候选 JjeMlmXA）在首次 save 时即被删除。
    `campaign_guard` 依赖本文件判定「alpha 是否经流水线评估」，丢条目会让
    合法候选被拒提交，属不可逆损失。

    修复：写前**重读磁盘**，把本次运行未触及的数据集条目原样保留，只让
    本次产生/更新的集覆盖。同时把合并结果回灌内存态，避免后续 save 又
    基于旧快照。
    """
    try:
        disk = load_results()
    except Exception:
        disk = {"results": {}}
    merged = dict(disk)
    merged_results = dict(disk.get("results") or {})
    merged_results.update(res.get("results") or {})
    merged["results"] = merged_results
    for k, v in res.items():
        if k != "results":
            merged[k] = v

    tmp = LOG + ".tmp"
    json.dump(merged, open(tmp, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    os.replace(tmp, LOG)

    # 回灌内存态：调用方的 res 与磁盘保持一致，后续 save 不会回退到旧快照
    res.clear()
    res.update(merged)

def compute_lit(region="EUR", ttl_h=12, refresh=False):
    """按平台 pyramids 统计「我方已提交数 / category」，返回 {CAT: n}。>3 即已点亮。

    口径（用户明令 2026-10-22）：只认我方提交计数，与平台 alpha_count / 本地挖没挖过无关。
    ⚠ 必须走平台 `pyramids`（或 ra.pyramid_short），本地 datasets.category 有大量 NULL，会低估。
    """
    import time
    try:
        if not refresh and os.path.isfile(LIT_CACHE):
            j = json.load(open(LIT_CACHE, encoding="utf-8"))
            ent = j.get(region) or {}
            if time.time() - (ent.get("ts") or 0) < ttl_h * 3600:
                return ent["counts"]
    except Exception:
        pass

    async def _fetch():
        sys.path.insert(0, os.path.join(ROOT, "world-quant-brain-mcp"))
        from brain_api import brain_client
        await brain_client.ensure_authenticated()
        al, off = [], 0
        while True:
            r = await brain_client.get_user_alphas(stage="OS", limit=100, offset=off) or {}
            res = r.get("results") or []
            al += res
            off += len(res)
            if not res or len(res) < 100:
                break
        return al

    try:
        alphas = asyncio.run(_fetch())
    except Exception as e:
        print(f"[lit] 平台统计失败（{type(e).__name__}），本轮按无点亮处理")
        return {}
    cnt = {}
    for a in alphas:
        if ((a.get("settings") or {}).get("region") or "") != region:
            continue
        p = a.get("pyramids")
        lst = p.get("list") if isinstance(p, dict) else (p if isinstance(p, list) else [])
        cats = {str(x.get("name", "")).split("/")[-1].upper() for x in lst
                if isinstance(x, dict) and x.get("name")}
        if not cats:
            ps = (a.get("ra") or {}).get("pyramid_short") or ""
            cats = {c.strip().upper() for c in ps.split("/") if c.strip()}
        for c in cats:
            cnt[c] = cnt.get(c, 0) + 1
    try:
        os.makedirs(os.path.dirname(LIT_CACHE), exist_ok=True)
        old = json.load(open(LIT_CACHE, encoding="utf-8")) if os.path.isfile(LIT_CACHE) else {}
        old[region] = {"ts": time.time(), "counts": cnt}
        tmp = LIT_CACHE + ".tmp"
        json.dump(old, open(tmp, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        os.replace(tmp, LIT_CACHE)
    except Exception:
        pass
    return cnt

PLAT_CACHE = {}


def platform_fields(ds):
    """平台真实字段集（带本地缓存）。本地库有幽灵字段（平台不存在），派发前必须过滤。"""
    if ds in PLAT_CACHE:
        return PLAT_CACHE[ds]
    import asyncio
    sys.path.insert(0, os.path.join(ROOT, "world-quant-brain-mcp"))
    from brain_api import brain_client

    async def _pull():
        await brain_client.ensure_authenticated()
        r = await brain_client.get_datafields(
            instrument_type="EQUITY", region="EUR", delay=1,
            universe="TOPCS1600", dataset_id=ds)
        j = r if isinstance(r, dict) else {}
        return {it.get("id") for it in (j.get("results") or [])}

    try:
        got = asyncio.run(_pull())
    except Exception as e:
        print(f"  [plat] {ds} 字段校验失败: {str(e)[:60]}（不过滤，按本地库派发）")
        got = None
    PLAT_CACHE[ds] = got
    return got


def _family_key(name, ds):
    """字段家族键：去掉数据集名前缀 + 去窗口数字。

    旧写法 `re.sub(r"[0-9]+","", name.split("_")[0])` 会把 `oth571_*`、`star_*`、`mdl219_*`
    这类共用数据集前缀的字段全归成同一族，导致整集只选出 1 个字段被判「字段不足」。
    """
    s = name
    if ds and s.startswith(ds + "_"):
        s = s[len(ds) + 1:]
    s = re.sub(r"(_?\d+)+$", "", s)      # 尾部窗口数字：_96 / _0
    s = re.sub(r"\d+", "", s)            # 中间数字
    return s.strip("_") or name
def select_fields(con, ds, field_min_cov=0.5, only_names=None, keep_fields=None):
    q = f"""SELECT f.field_name, f.field_type, f.coverage, st.sem_type,
                   COALESCE(f.description,'') AS descr
           FROM fields f JOIN datasets d ON f.dataset_id=d.id JOIN regions r ON d.region_id=r.id
           LEFT JOIN field_semantic_type st ON st.region='EUR' AND st.dataset=d.name AND st.field=f.field_name
           WHERE r.name='EUR' AND d.name=? AND f.coverage>={field_min_cov}
             AND f.field_type != 'GROUP'"""
    rows = [dict(x) for x in con.execute(q, (ds,))]
    # ★ 语义改判：sem_type 缺失/unknown 时按 description 分类；metadata 组直接丢弃（不参与选代表）
    n_meta = 0
    for r in rows:
        st0 = (r.get("sem_type") or "").lower()
        if is_name_metadata(r["field_name"]) or classify_desc(r.get("descr")) == "metadata":
            r["sem_type"] = "metadata"          # 名字/描述即元数据（不看语义表给什么）
        elif st0 in ("identifier", "temporal_meta"):
            r["sem_type"] = "metadata"          # 语义表已判为标识符/时间元数据
        elif st0 in ("", "unknown", "none"):
            r["sem_type"] = classify_desc(r.get("descr"), r["field_name"])
        if (r.get("sem_type") or "").lower() == "metadata":
            n_meta += 1
    kept = [r for r in rows if (r.get("sem_type") or "").lower() != "metadata"]
    if n_meta and len(kept) >= MIN_FIELDS_TOTAL:
        rows = kept
        print(f"  [sem] {ds}: 按 description 丢弃元数据字段 {n_meta} 个"
              f"（剩 {len(rows)} 个可挖字段）")
    elif n_meta:
        print(f"  [sem] {ds}: 元数据字段 {n_meta} 个，但丢弃后可挖不足 {MIN_FIELDS_TOTAL} 个 ⇒ 回退不丢弃")
    plat = platform_fields(ds)
    keep = {x.lower() for x in (keep_fields or [])}
    if plat is not None:
        n0 = len(rows)
        # --keep-fields 白名单跳过幽灵过滤：平台 /data-fields 清单有时漏掉可用字段
        # （2026-10-22 实证：ern6_actual_eps / ern6_estimated_eps 不在清单里但仿真正常）
        gone, kept_rows = [], []
        for r in rows:
            if r["field_name"] in plat or r["field_name"].lower() in keep:
                kept_rows.append(r)
            else:
                gone.append(r["field_name"])
        rows = kept_rows
        if len(rows) < n0:
            print(f"  [plat] {ds}: 过滤幽灵字段 {n0 - len(rows)} 个"
                  f"（本地 {n0} → 平台认证 {len(rows)}）: {gone[:8]}")
    if only_names:
        # 续跑：沿用断点里记录的字段清单，保证同一数据集各模板族字段覆盖一致
        keep = set(only_names)
        rows = [r for r in rows if r["field_name"] in keep]
        for r in rows:
            r["dim"] = r["sem_type"] or "unknown"
        # ⚠ 2026-10-23：续跑集也必须吃 A 方案的字段上限。
        # 旧实现在这里直接 return，导致已锁定字段的集（如 risk62 的 19 个字段）绕过 FULL_FIELD_CAP，
        # 仍然派发 134 条 → 把提速又抵消掉。
        if len(rows) > FULL_FIELD_CAP:
            _n0 = len(rows)
            _by = sorted(rows, key=lambda r: -(r["coverage"] or 0))
            _keep, _dims = [], set()
            for r in _by:
                if r["dim"] not in _dims:
                    _dims.add(r["dim"]); _keep.append(r)
            for r in _by:
                if len(_keep) >= FULL_FIELD_CAP:
                    break
                if r not in _keep:
                    _keep.append(r)
            rows = _keep[:FULL_FIELD_CAP]
            print(f"  [budget] {ds}: 续跑集字段 {_n0} → {len(rows)}（上限 {FULL_FIELD_CAP}）")
        for r in rows:
            r.setdefault("tier", "full")
        return rows

    by = collections.defaultdict(list)
    for r in rows:
        by[r["sem_type"] or "unknown"].append(r)
    sel = []
    for dim, fl in by.items():
        fl.sort(key=lambda x: -(x["coverage"] or 0))
        picked, seen = [], set()
        # 第一轮：每族取 1 个（族 = 去掉数据集名前缀 + 去掉窗口数字）
        for r in fl:
            fam = _family_key(r["field_name"], ds)
            if fam in seen:
                continue
            seen.add(fam)
            picked.append(r)
            if len(picked) >= PER_DIM:
                break
        # 第二轮：族数不足 PER_DIM 时同族补位（不同窗口），否则整个集会被判「字段不足」而跳过。
        # 旧实现只做第一轮且族键取 split("_")[0] ⇒ oth571_*/star_* 这类共用数据集前缀的集
        # 全部字段被归成 1 族 ⇒ 只选 1 个 ⇒ SKIPPED_TOO_FEW_FIELDS（2026-10-22 复核）。
        if len(picked) < PER_DIM:
            chosen = {id(x) for x in picked}
            for r in fl:
                if id(r) in chosen:
                    continue
                picked.append(r)
                if len(picked) >= PER_DIM:
                    break
        for r in picked:
            r["dim"] = dim
        sel += picked

    # ★ 去重同源副本（2026-10-22 实测）：`ern6_actual_eps` 与 `ern6_actual_eps_274` 是平台同一列的两个 id，
    # 表达式不同但仿真结果指向**同一个 alpha_id**（children 里出现重复 alpha）⇒ 每批白白丢 2/10 的名额。
    # 规则：去掉尾部 `_NNN` 后同名者只留第一个（覆盖率最高的那个）。
    _uniq, _seen = [], set()
    for r in sel:
        b = re.sub(r"_\d+$", "", r["field_name"]).lower()
        if b in _seen:
            continue
        _seen.add(b)
        _uniq.append(r)
    if len(_uniq) < len(sel):
        print(f"  [dedup] {ds}: 同源副本字段 -{len(sel) - len(_uniq)}（{len(sel)} → {len(_uniq)}）")
    sel = _uniq

    # 保底：降采样后若总数不足 3（如只有 1 个维度且该维度只有 2 个字段），
    # 从剩余候选里按覆盖率补齐，避免把本可测的集判成 SKIPPED_TOO_FEW_FIELDS。
    if len(sel) < MIN_FIELDS_TOTAL:
        chosen = {id(x) for x in sel}
        extra = [r for r in rows if id(r) not in chosen]
        extra.sort(key=lambda x: -(x["coverage"] or 0))
        for r in extra[: MIN_FIELDS_TOTAL - len(sel)]:
            r["dim"] = r["sem_type"] or "unknown"
            sel.append(r)

    # ★ 2026-10-23（用户指出「选字段缺口」）：**不再丢弃未入选字段**，改为 full / probe 两层。
    # 根因：旧逻辑按「语义维 × PER_DIM」硬裁（sentiment26 的 19 个字段只留 9 个，10 个静默消失），
    # 而唯一能出货的结构（pp）只跑在 top3 字段上 ⇒ 结构性缺口完全不可见。
    #   full  : 全 12 族（原精选集合）
    #   probe : 只跑 1 条最便宜探针（lvl_rk）；收割后由 carrier_expand() 把本集最强结构补跑一遍
    # A. 全族字段裁剪：每维先各留 1 个（保证维度多样性），再按覆盖率补满 FULL_FIELD_CAP
    if len(sel) > FULL_FIELD_CAP:
        _n0 = len(sel)
        _by_cov = sorted(sel, key=lambda r: -(r["coverage"] or 0))
        _keep, _dims = [], set()
        for r in _by_cov:
            d = r["dim"]
            if d not in _dims:
                _dims.add(d)
                _keep.append(r)
        for r in _by_cov:
            if len(_keep) >= FULL_FIELD_CAP:
                break
            if r not in _keep:
                _keep.append(r)
        sel = _keep[:FULL_FIELD_CAP]
        print(f"  [budget] {ds}: 全族字段 {_n0} → {len(sel)}（上限 {FULL_FIELD_CAP}）")

    full_names = {r["field_name"] for r in sel}
    for r in sel:
        r["tier"] = "full"
    _pw = {re.sub(r"_\d+$", "", r["field_name"]).lower() for r in sel}
    probe = []
    for r in rows:
        if r["field_name"] in full_names:
            continue
        b = re.sub(r"_\d+$", "", r["field_name"]).lower()
        if b in _pw:
            continue
        _pw.add(b)
        r["dim"] = r["sem_type"] or "unknown"
        r["tier"] = "probe"
        probe.append(r)
    if len(probe) > PROBE_FIELD_CAP:
        probe = sorted(probe, key=lambda r: -(r["coverage"] or 0))[:PROBE_FIELD_CAP]
    if probe:
        print(f"  [fields] {ds}: full {len(sel)} + probe {len(probe)}"
              f"（探针上限 {PROBE_FIELD_CAP}）")
    return sel + probe


def build_one_family(tpl, r, freq):
    """把指定族的结构套在某个字段上（载体扩散用）。"""
    BF, WS, WL, ZW, W1 = FREQ_WIN.get(freq, FREQ_WIN["unknown"])
    F, FR = wrap(r), r["field_name"]
    if tpl == "dw":
        return DW_TPL.format(F=F, BF=BF, WS=WS, WL=WL)
    if tpl == "pp":
        # pp 不是独立模板，而是「dw 结构 + 0.85 稀疏门控」（sentiment26/wp99v7qv 的成品形态）
        dw = DW_TPL.format(F=F, BF=BF, WS=WS, WL=WL)
        return f"if_else(greater(rank({dw}), 0.85), {dw}, 0)"
    if tpl.endswith("_pl"):
        l1, l2 = tpl[:-3], None
    elif "_" in tpl:
        l1, l2 = tpl.split("_", 1)
    else:
        l1, l2 = tpl, None
    if l1 not in L1_EXTRACT:
        return None
    if l2 == "va":
        return VA_TPL.format(F=F, BF=BF, ZW=ZW, W1=W1)
    x = L1_EXTRACT[l1].format(F=F, FR=FR, BF=BF, ZW=ZW, W1=W1)
    if l2:
        x = L2_NORM[l2].format(X=x, ZW=ZW)
    return x


def batch_field_coverage(ds, field_names, tpls=None):
    """扫本集所有已派发批文件 → {field: set(族)}。审计「哪些字段从没跑过哪些结构」。"""
    cov = collections.defaultdict(set)
    import glob
    for fn in glob.glob(os.path.join(ROOT, "cache", f"_camp_{ds}_*.txt")):
        base = os.path.basename(fn)[len(f"_camp_{ds}_"):-4]
        tpl = re.sub(r"_\d+$", "", base)
        if tpls and tpl not in tpls:
            continue
        try:
            lines = [l.strip() for l in open(fn, encoding="utf-8") if l.strip()]
        except Exception:
            continue
        for line in lines:
            for fname in field_names:
                if fname in line:
                    cov[fname].add(tpl)
    return cov


def carrier_expand(ds, sel, best, freq, ck, total_tpls):
    """载体结构扩散（堵住 sentiment26 式缺口）：本集最强族 ≥1.2 时，把该结构补跑所有 probe 字段。

    归因：pp 结构在 sentiment26 只跑过 2 个字段就出了 S1.54，而另外 10 个字段一次都没跑过该结构；
    旧流程永远发现不了这种「结构好但字段没铺开」的浪费。
    """
    cand = [(t, v) for t, v in best.items()
            if (v.get("max_s") or 0) >= 1.2 and not t.startswith("sw_")]
    if not cand:
        return []
    tpl = max(cand, key=lambda kv: kv[1]["max_s"])[0]
    names = [r["field_name"] for r in sel]
    cov = batch_field_coverage(ds, names, tpls={tpl})
    todo = [r for r in sel if r.get("tier") == "probe" and tpl not in cov.get(r["field_name"], set())]
    if not todo:
        return []
    exprs = []
    for r in todo:
        e = build_one_family(tpl, r, freq)
        if e:
            exprs.append((f"{tpl}_cx", e))
    if len(exprs) < 2:
        print(f"  [carrier] {tpl} 待扩散字段只有 {len(exprs)} 个（<2，空批风险），跳过")
        return []
    print(f"  [carrier] 载体族 {tpl}（max_S={dict(cand)[tpl]['max_s']}）"
          f"从未跑过该结构的 probe 字段 {len(exprs)} 个 → 补跑")
    key = ds + "@cx"
    prev = [tuple(x) for x in (ck.get("sims", {}).get(key) or []) if x and x[0]]
    if prev:
        print(f"  [carrier] 复用已派发 {len(prev)} 批")
        return prev

    def _persist(pp, _k=key):
        ck["sims"][_k] = list(pp); save_ckpt(ck)

    sims = dispatch(exprs, ds, "cx", on_batch=_persist)
    ck["sims"][key] = sims
    save_ckpt(ck)
    return sims


def wrap(r):
    if r["field_type"] != "VECTOR":
        return r["field_name"]
    return f"vec_sum({r['field_name']})" if r["sem_type"] == "count" else f"vec_avg({r['field_name']})"

PROBE_FIELD_CAP = 12   # 探针层字段上限（每个只跑 1 条 lvl_rk）


def check_prod(alpha_id, max_wait=240):
    """测单个 alpha 的 prod 相关性（端点异步排队：先触发再轮询取值）。

    2026-10-22 教训：两个强集（sentiment26 0.755、ai_equity_alpha 0.7775）都是
    「S 看着行、prod 已死」的假阳性——判定环节不测 prod 会一直白挖。
    2026-10-22 二修：响应结构是 `{schema:{max:...}, records:[...]}`，
    旧实现只读顶层 `max`/`max_correlation` ⇒ 全部返回 None（本 campaign 前 14 集 prod 全空的原因）。
    """
    import asyncio
    sys.path.insert(0, os.path.join(ROOT, "world-quant-brain-mcp"))
    from brain_api import brain_client

    def _parse(j):
        if not isinstance(j, dict):
            return None
        sch = j.get("schema") or {}
        for v in ((sch or {}).get("max"), j.get("max"), j.get("max_correlation")):
            if v is not None:
                try:
                    return float(v)
                except (TypeError, ValueError):
                    pass
        mx = None
        for row in (j.get("records") or []):
            for v in (row if isinstance(row, (list, tuple)) else list(row.values())):
                if isinstance(v, (int, float)) and (mx is None or v > mx):
                    mx = float(v)
        return mx

    async def _go():
        await brain_client.ensure_authenticated()
        for _ in range(max(3, max_wait // 10)):
            try:
                j = await brain_client.get_production_correlation(alpha_id)
            except Exception:
                j = None
            mx = _parse(j)
            if mx is not None:
                return mx
            await asyncio.sleep(10)
        return None
    try:
        return asyncio.run(_go())
    except Exception:
        return None


def year_profile(alpha_id, max_wait=60):
    """年度画像（2026-10-23 用户指出「回测前三年都没数」后新增）。

    实测案例：sentiment26 的 alpha 2014-2016 **零持仓**（数据 2017-01 才有），
    2020 一年贡献 51% 净 PnL、2021 是 −0.91 Sharpe ⇒ 这类「靠单一年份/单一 regime」的 alpha
    即使六闸全过也不该交付：全期 Sharpe 是被一年撑起来的，OS 大概率不复现。

    返回：{first_year, n_years, top_year, top_share, ex_top_ret, late_start, fragile}
      top_share   = max|pnl_y| / sum|pnl_y|      （>0.5 ⇒ 单年主导）
      ex_top_ret  = 剔除 top_year 后的年均收益
      late_start  = 首个有持仓年份比回测起点晚 ≥2 年
      fragile     = late_start or n_years<6 or top_share>0.5 or ex_top_ret<=0
    """
    import asyncio
    sys.path.insert(0, os.path.join(ROOT, "world-quant-brain-mcp"))
    if _WQB_SCRIPTS_DIR not in sys.path:
        sys.path.insert(0, _WQB_SCRIPTS_DIR)
    from brain_api import brain_client
    from wqb_tools import _get_json

    async def _go():
        await brain_client.ensure_authenticated()
        return await _get_json(brain_client, f"/alphas/{alpha_id}/recordsets/yearly-stats",
                               tries=2, base_sleep=1.0)

    try:
        j = asyncio.run(_go())
    except Exception:
        return None
    recs = (j or {}).get("records") or []
    if not recs:
        return None
    # 端点的 records 是**数组**（按 schema.properties 顺序），不是 dict —— 两种都兼容
    props = [x.get("name") for x in ((j or {}).get("schema") or {}).get("properties") or []]
    idx = {n: i for i, n in enumerate(props)} or {
        "year": 0, "pnl": 1, "longCount": 3, "shortCount": 4, "returns": 7}
    rows = []
    for r in recs:
        try:
            def g(key, default=0.0):
                if isinstance(r, dict):
                    v = r.get(key)
                else:
                    i = idx.get(key)
                    v = r[i] if i is not None and i < len(r) else None
                return default if v is None else v
            rows.append({"year": int(g("year")), "pnl": float(g("pnl")),
                         "ret": float(g("returns")),
                         "pos": float(g("longCount")) + float(g("shortCount"))})
        except (TypeError, ValueError):
            continue
    live = [r for r in rows if r["pos"] > 0]
    if not live:
        return None
    tot_abs = sum(abs(r["pnl"]) for r in live) or 1.0
    top = max(live, key=lambda r: abs(r["pnl"]))
    ex = [r for r in live if r is not top]
    ex_ret = sum(r["ret"] for r in ex) / len(ex) if ex else 0.0
    # 近期断裂（2026-10-23：predictive_starmine 教训）——历史 10 年全正，但 2022 −0.72 / 2023 −0.81。
    # 「样本健康」不等于「现在还有效」，必须单独把它标出来，否则 fragile 会漏掉「正在死」的族。
    last2 = sorted(live, key=lambda r: r["year"])[-2:]
    recent_break = bool(len(last2) == 2 and sum(r["ret"] for r in last2) <= 0)
    first_y = min(r["year"] for r in live)
    start_y = min(r["year"] for r in rows)
    return {
        "first_year": first_y, "start_year": start_y, "n_years": len(live),
        "top_year": top["year"], "top_share": round(abs(top["pnl"]) / tot_abs, 3),
        "ex_top_ret": round(ex_ret, 4),
        "late_start": (first_y - start_y) >= 2,
        "recent_break": recent_break,
        "last2_ret": round(sum(r["ret"] for r in last2), 4) if last2 else None,
        "fragile": bool((first_y - start_y) >= 2 or len(live) < 6
                        or abs(top["pnl"]) / tot_abs > 0.5 or ex_ret <= 0
                        or recent_break),
    }


def fetch_codes(alpha_ids):
    """按 alpha id 取回表达式（用于阶段 2）。"""
    import asyncio
    sys.path.insert(0, os.path.join(ROOT, "world-quant-brain-mcp"))
    # wqb_tools 住在仓库外的 wqb-scripts/（$WQB_SCRIPTS 或 ~/wqb-scripts/），不在默认 sys.path 上
    if _WQB_SCRIPTS_DIR not in sys.path:
        sys.path.insert(0, _WQB_SCRIPTS_DIR)
    from brain_api import brain_client
    from wqb_tools import _get_json

    async def _all():
        await brain_client.ensure_authenticated()
        out = {}
        for aid in alpha_ids:
            try:
                j = await _get_json(brain_client, f"/alphas/{aid}", tries=2, base_sleep=1.0)
                out[aid] = (j.get("regular") or {}).get("code") or ""
            except Exception:
                pass
        return out

    return asyncio.run(_all())


def build_postproc(code):
    """对最佳构造套后处理电池（稀疏化 / 分组 / 压缩 / tvr）。"""
    out = []
    # ⚠ 统一用 tpl="pp"：若按变体名分组（pp_sp/pp_gr/pp_spw），后两者各只有 1 条 ⇒
    #   落成单条批 ⇒ COMPLETE children=0 收不到结果（2026-10-22 实测）。同一 tpl 会合并成一批。
    for q in POSTPROC_Q:
        out.append(("pp", f"if_else(greater(rank({code}), {q}), {code}, 0)"))
    out.append(("pp", f"group_rank({code}, market)"))
    out.append(("pp", f"signed_power({code}, 0.7)"))
    return out

def build_exprs(sel, freq, cat=None, ds=None, _force_full=False, pp_map=None):
    """分层生成：L1 提取 × L2 归一化 交叉（12 族）+ L3 双窗。

    2026-10-24 起叠加三层（借鉴 brain-data-feature-engineering skill）：
      ① 字段透明度分档 —— 黑盒字段不信形态分类，走「无先验多样族」BLACKBOX_FAMILIES；
      ② preprocessing 受控词表 —— `pp_map[字段]` 命中则给字段原子套预处理（有序）；
      ③ Expected Exposure —— 每条表达式记暴露到 `EXPR_EXPOSURE`，供数据集末统计。
    """
    BF, WS, WL, ZW, W1 = FREQ_WIN.get(freq, FREQ_WIN["unknown"])
    pp_map = pp_map or {}
    out = []
    _gated = (cat or "").upper() in GATED_CATS
    _full_cross = len(FAMILIES) + 1        # 全交叉时每字段的族数（含 dw）
    for r in sel:
        FR = r["field_name"]
        # ② 收益来源先验：字段语义优先（探针层也要用，否则 12 条探针全被错标成 value）
        _hint = field_exposure_hint(r, cat)
        if r.get("tier") == "probe":
            # 探针层：只跑最便宜的 lvl_rk，1 条/字段（成本 ≈ 剩余字段数 × 1）
            _x = L1_EXTRACT["lvl"].format(F=FR, FR=FR, BF=BF, ZW=ZW, W1=W1)
            _e = L2_NORM["rk"].format(X=_x, ZW=ZW)
            out.append(("lvl_rk", _e))
            EXPR_EXPOSURE[_e] = _hint if _hint != "value" else FAMILY_EXPOSURE.get("lvl_rk", "other")
            continue
        _form = r.get("form") or field_form(r, ds)
        r["form"] = _form
        if _form == "skip":
            continue
        # ② 透明度分档：黑盒 ⇒ 不信形态减法；半透明/透明 ⇒ 仍信 FORM_FAMILIES
        _tier = r.get("ftier") or field_tier(r, cat, ds)
        r["ftier"] = _tier
        if _tier == "blackbox":
            # 黑盒：机制驱动。概念推不出才退回校准过的固定多样族
            _cf = concept_families(r, cat, ds)
            _allow = _cf if _cf else set(BLACKBOX_FAMILIES)
            _gated_f = True               # 黑盒也开 pp/tl 门控（实测 pp 是 other 形态最强族）
        else:
            _allow = None if _force_full else FORM_FAMILIES.get(_form)
            if _allow is None and not _force_full:
                # form=other ⇒ 形态分类器失效，用概念补（2026-10-24）
                _cf = concept_families(r, cat, ds)
                if _cf:
                    _allow = _cf
            _gated_f = _gated
        # 概念留痕：汇报与后续校准都要用
        r["concepts"] = field_concepts(r, cat, ds)
        # ② preprocessing：只对受控词表命中的字段生效（自由文本已在 parse 阶段丢弃）。
        #   在族内套，以便跳过与模板自身 L2 重复的归一（如预处理说 rank 而模板就是 rank）。
        F0 = wrap(r)
        _toks = pp_map.get(FR)
        for l1, l2 in FAMILIES:
            if _allow is not None and f"{l1}_{l2 or 'pl'}" not in _allow:
                continue
            if l1 == "dsp" and r["field_type"] != "VECTOR":
                continue
            F = apply_preprocessing(F0, _toks, FR, BF, ZW, l2) if _toks else F0
            if l2 == "va":
                x = VA_TPL.format(F=F, BF=BF, ZW=ZW, W1=W1)
            else:
                x = L1_EXTRACT[l1].format(F=F, FR=FR, BF=BF, ZW=ZW, W1=W1)
                if l2:
                    x = L2_NORM[l2].format(X=x, ZW=ZW)
            _fam = f"{l1}_{l2 or 'pl'}"
            out.append((_fam, x))
            EXPR_EXPOSURE[x] = _hint if _hint != "value" else FAMILY_EXPOSURE.get(_fam, "other")
        _Fdw = apply_preprocessing(F0, _toks, FR, BF, ZW, None) if _toks else F0
        if _allow is None or "dw" in _allow:
            _dw = DW_TPL.format(F=_Fdw, BF=BF, WS=WS, WL=WL)
            out.append(("dw", _dw))
            EXPR_EXPOSURE[_dw] = _hint if _hint != "value" else FAMILY_EXPOSURE.get("dw", "other")
        # 稀疏门控一等模板（之前只在 build_postproc 对 top3 生效 ⇒ sentiment26 的 pp 只覆盖 2/19 字段）
        if _gated_f and (_allow is None or "pp" in _allow):
            _dw = DW_TPL.format(F=_Fdw, BF=BF, WS=WS, WL=WL)
            _pp = f"if_else(greater(rank({_dw}), {GATE_Q}), {_dw}, 0)"
            out.append(("pp", _pp))
            EXPR_EXPOSURE[_pp] = _hint if _hint != "value" else FAMILY_EXPOSURE.get("pp", "other")
            _m = f"rank(ts_mean(ts_backfill({_Fdw}, {BF}), {WS}))"
            _tl = f"tail({_m}, lower=0, upper={GATE_Q}, newval=0)"
            out.append(("tl", _tl))
            EXPR_EXPOSURE[_tl] = _hint if _hint != "value" else FAMILY_EXPOSURE.get("tl", "other")

    # 安全阀（2026-10-23）：形态映射只做「减法」，但减错会丢族。
    # 判据：非探针字段的规模若被压到全交叉的 <50%，说明分类器在该集上不可信 ⇒ 退回全交叉。
    _nonprobe = [r for r in sel if r.get("tier") != "probe" and r.get("form") != "skip"]
    if not _force_full and _nonprobe:
        _expect = len(_nonprobe) * _full_cross
        # 阈值 35%：正常的 level_ratio(8/12)/count(3/12) 映射本就会压到 50% 左右，
        # 用 50% 会频繁误触（news20 实测 44/96 被误判）。35% 只拦真正的病态收窄（如 16/98）。
        if len(out) < 0.35 * _expect:
            print(f"  [form] ⚠ 映射后仅 {len(out)}/{_expect} 条（<35%）⇒ 该集分类不可信，退回全交叉")
            return build_exprs(sel, freq, cat=cat, ds=ds, _force_full=True, pp_map=pp_map)
    return out


# ---------------------------------------------------------------- 派发/收割

MAX_INFLIGHT = 7      # 用户设定（2026-10-23 上调 4→7）：平台并发上限约 10，留 3 个机动位
                      # 给交互式探针 / prod 复核。提高后 429 由 submit_batch 退避重试兜底。
_TERMINAL = {"COMPLETE", "FAIL", "ERROR", "CANCELLED"}
GATE_TIMEOUT = 2400   # 缺陷4修复：FULL 模式单批常 >20min，旧 1200s 超时放行会突破并发上限
_FORCED_RELEASE = 0

# ---- 缺陷2修复：平台拒绝过的名字全局拉黑（unknown variable / inaccessible operator / 单位不符）----
BAD_TOKEN_FILE = os.path.join(ROOT, "cache", "bad_tokens.json")
BAD_TOKENS = set()


def load_bad_tokens():
    global BAD_TOKENS
    try:
        BAD_TOKENS = set(json.load(open(BAD_TOKEN_FILE, encoding="utf-8")))
    except Exception:
        BAD_TOKENS = set()
    return BAD_TOKENS


def note_bad_tokens(errs, verbose=True):
    """从平台错误消息提取「被拒的名字」并持久化拉黑，后续批次直接过滤。

    覆盖本次战役实测三类毒化源（每条都会让**整批** CANCELLED）：
      ① unknown variable "X"                        —— 幽灵字段（如 earnings_volatility_trend）
      ② inaccessible or unknown operator "X"        —— 赛季未解锁算子（如 rank_by_side）
      ③ Incompatible unit for input of "group_rank" —— 单位不符（如 group_rank(x, sign(x))）
    """
    global BAD_TOKENS
    new = set()
    for e in errs or []:
        for pat in (r'unknown variable "([^"]+)"',
                    r'inaccessible or unknown operator "([^"]+)"',
                    r'Incompatible unit for input of "([^"]+)"'):
            for name in re.findall(pat, e or "", flags=re.I):
                new.add(name.strip())
    new -= BAD_TOKENS
    if not new:
        return set()
    BAD_TOKENS |= new
    try:
        tmp = BAD_TOKEN_FILE + ".tmp"
        json.dump(sorted(BAD_TOKENS), open(tmp, "w", encoding="utf-8"), ensure_ascii=False)
        os.replace(tmp, BAD_TOKEN_FILE)
    except Exception:
        pass
    if verbose:
        print(f"  [preflight] 拉黑平台拒绝的名字 {sorted(new)}（累计 {len(BAD_TOKENS)}）")
    return new


def filter_bad(exprs):
    """丢掉含黑名单名字的表达式 → (保留列表, 丢弃数)。防止一条坏式毒死整批。"""
    if not BAD_TOKENS:
        return list(exprs), 0
    keep = [(t, e) for t, e in exprs if not any(tk and tk in e for tk in BAD_TOKENS)]
    return keep, len(exprs) - len(keep)


def norm_tpl(tpl):
    """补派/重派批的族名带 _f/_r/_rp 后缀，统计时并回原族。"""
    for suf in ("_rp", "_cx", "_f", "_r"):
        if tpl.endswith(suf) and len(tpl) > len(suf):
            return tpl[:-len(suf)]
    return tpl


def beat(ds=None, note=""):
    """缺陷6修复：心跳文件，外部 watchdog 据此判断进程是否还活着。"""
    try:
        tmp = HEARTBEAT + ".tmp"
        json.dump({"ts": datetime.now().isoformat(timespec="seconds"),
                   "epoch": time.time(), "pid": os.getpid(), "dataset": ds,
                   "note": note, "argv": sys.argv[1:]},
                  open(tmp, "w", encoding="utf-8"), ensure_ascii=False)
        os.replace(tmp, HEARTBEAT)
    except Exception:
        pass


def sims_terminal(sim_id):
    """该 multisim 的子任务是否全部终态（COMPLETE/FAIL/…）。用于限制在飞作业数。"""
    import asyncio
    sys.path.insert(0, os.path.join(ROOT, "world-quant-brain-mcp"))
    from brain_api import brain_client

    async def _go():
        await brain_client.ensure_authenticated()
        resp = await brain_client._request(
            "GET", f"{brain_client.base_url}/simulations/{sim_id}")
        try:
            j = resp.json()
        except Exception:
            return False
        kids = j.get("children") or []
        if not kids:
            return str(j.get("status") or "").upper() in _TERMINAL
        return all(str((k.get("status") or "")).upper() in _TERMINAL for k in kids)

    try:
        return asyncio.run(_go())
    except Exception:
        return False


def wait_slot(pending, timeout=None):
    """在飞数到上限时，等最早那批跑完腾出名额（pending 原地修改）。

    缺陷4修复：默认超时 1200s → GATE_TIMEOUT(2400s)。旧值下 FULL 批次频繁超时放行，
    实际在飞会到 5–8 个（日志连续「强制放行」即此），并发上限形同虚设。
    """
    global _FORCED_RELEASE
    timeout = timeout or GATE_TIMEOUT
    while len(pending) >= MAX_INFLIGHT:
        sid = pending[0]
        t0 = time.time()
        done = False
        while time.time() - t0 < timeout:
            if sid is None or sims_terminal(sid):
                done = True
                break
            time.sleep(15)
        pending.pop(0)
        if done:
            continue
        _FORCED_RELEASE += 1
        print(f"  [gate] {sid} 等待 {timeout}s 超时，强制放行"
              f"（累计超限放行 {_FORCED_RELEASE} 次，实际并发可能 >{MAX_INFLIGHT}）")


def dispatch(exprs, ds, label, on_batch=None, settings=None):
    """模板优先派发：每个模板单独分批（≤10/批）→ [(sim_id, template, batch_idx)]。

    ⚠ 2026-10-22 实测：n=1 的批次提交后必为 ``COMPLETE children=0``，结果永远收不到
    （用已知有效表达式复现同样如此）。故分批改为**均分**，杜绝出现单条批：
    11 条 → 6+5 而不是 10+1。

    ★ 2026-10-22 用户设定：同时最多 MAX_INFLIGHT=4 个作业在跑。
    ★ 2026-10-23 修复：
      - `settings` 可覆写设置（设置轴扫描用：universe / neutralization / decay / truncation）；
      - 派发前按 BAD_TOKENS 过滤（一条坏式会毒死整批，实测 4 次）；
      - wait_slot 超时提到 2400s，并发上限真正生效。
    """
    exprs, n_bad = filter_bad(exprs)
    if n_bad:
        print(f"  [preflight] {ds}/{label}: 丢弃 {n_bad} 条（命中平台黑名单 {sorted(BAD_TOKENS)}）")
    st = {"universe": "TOPCS1600", "decay": "4",
          "neutralization": "FAST", "truncation": "0.08"}
    if settings:
        st.update({k: str(v) for k, v in settings.items()})
    by_tpl = collections.defaultdict(list)
    for tpl, e in exprs:
        by_tpl[tpl].append(e)
    sims = []
    pending = []
    for tpl, elist in by_tpl.items():
        n = len(elist)
        nb = max(1, -(-n // 10))                   # ceil 批数（每批 ≤10）
        base, rem = divmod(n, nb)                  # 均分：rem 批 base+1，其余 base
        sizes = [base + 1] * rem + [base] * (nb - rem)
        batches, pos = [], 0
        for s in sizes:
            batches.append(elist[pos:pos + s])
            pos += s
        for bi, b in enumerate(batches):
            wait_slot(pending)                     # ★ 在飞上限 = --max-inflight（默认见 MAX_INFLIGHT），满了先等最早那批终态
            fn = os.path.join(ROOT, "cache", f"_camp_{ds}_{tpl}_{bi}.txt")
            with open(fn, "w", encoding="utf-8") as fh:
                fh.write("\n".join(b) + "\n")
            cmd = [VENV_PY, WQB_TOOLS, "dispatch", fn,
                   "--label", f"camp_{ds}_{label}_{tpl}_{bi}",
                   "--region", "EUR", "--universe", st["universe"], "--decay", st["decay"],
                   "--neutralization", st["neutralization"], "--truncation", st["truncation"],
                   "--nan-handling", "ON", "--max-trade", "ON",
                   # ⚠ 2026-10-22 撤回 QUICK：实测 QUICK↔FULL 失真不可预测（-0.18~+0.87，
                   # E5VmWRnL QUICK 1.60→FULL 0.73），连相对排序都不可信 ⇒ 回退 FULL。
                   "--simulation-mode", "FULL",
                   "--force", "--allow-probe-repeat"]
            try:
                out = subprocess.run(cmd, capture_output=True, text=True, timeout=600).stdout
                m = re.search(r'"sim_id": "([^"]+)"', out)
                sims.append((m.group(1) if m else None, tpl, bi))
            except Exception as e:
                # 2026-10-27：超时/异常时该批**可能已在平台上跑**，但本地没拿到 sim_id。
                # 记一条孤儿线索，避免下次续跑盲目重派（重复派发是 2026-10-22 事故的成因）。
                sims.append((None, tpl, bi))
                print(f"  [dispatch] {tpl}_{bi} error: {e}")
                try:
                    _orph = os.path.join(ROOT, "cache", f"_orphan_{tpl}_{bi}.json")
                    json.dump({"template": tpl, "batch_index": bi, "dataset": ds,
                               "error": str(e), "ts": time.strftime("%Y-%m-%dT%H:%M:%S"),
                               "cmd": " ".join(str(c) for c in cmd)},
                              open(_orph, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
                except Exception as _e2:  # noqa: BLE001
                    print(f"  [dispatch] 孤儿线索写入失败（不阻断）: {_e2}")
            pending.append(sims[-1][0])
            # 每批落一次断点：进程被杀时已派发的批次不会丢（否则重启会整集重派，
            # 2026-10-22 news_sentiment_dl 因此重复派发 216 条）
            if on_batch:
                try:
                    on_batch(list(sims))
                except Exception as e_cb:  # noqa: BLE001
                    # 2026-10-27：此前 `except: pass` 静默吞掉 ⇒ 断点写失败无声，
                    # 下次续跑会整集重派。断点是防重复派发的唯一凭据，必须响。
                    print(f"  [checkpoint][WARN] on_batch 保存断点失败（{ds}/{tpl}_{bi}）："
                          f"{type(e_cb).__name__}: {e_cb} —— 该批可能重复派发")
    return sims


def harvest(sim_id, ds):
    """收割一个批次 → 返回 (rows, errors, state)

    rows : [(alpha_id, S, F, 2Y, sub)]
    errors: 子任务错误消息（用于分类）
    state: ok      = COMPLETE 且 rows 覆盖全部 children
           partial = COMPLETE 但有 children 没收到（平台限流/详情查询失败）→ 可重试补齐
           running = 还没跑完
           empty   = COMPLETE 且 children=0（结构性空批，等也没用）
           error   = 查询本身失败（429/网络）
    """
    cmd = [VENV_PY, os.path.join(ROOT, "cache", "_harvest_safe.py"), sim_id, ds, "camp"]
    try:
        out = subprocess.run(cmd, capture_output=True, text=True, timeout=600).stdout
    except Exception:
        return None, [], "error"
    rows, errors = [], []
    for line in out.splitlines():
        m = re.match(r"\s*\+\s+(\w+)\s+S=([-\d.]+)\s+F=([-\d.]+).*?2Y=([-\d.]+)\s+sub=([-\d.]+)", line)
        if m:
            rows.append((m.group(1), float(m.group(2)), float(m.group(3)),
                         float(m.group(4)), float(m.group(5))))
            continue
        me = re.match(r"\s*x\s+\S+\s+.*?msg=(.+)$", line)
        if me:
            errors.append(me.group(1).strip()[:100])

    # ⚠ 三类空结果必须区分（2026-10-22 实测）：
    #   ① running：/simulations/{id} 只返回 {"progress":0.35}，脚本打成 status=None children=0
    #   ② empty  ：status=COMPLETE 且 children=0（单条批）—— 再等也没用
    #   ③ partial：COMPLETE 且 children>0 但 rows 少 —— 平台对 alpha 详情端点限流，
    #              整批会被打成 0 行，若当成 running 会白等 4 分钟、若当成空批就永久丢结果
    md = re.search(r"status=(\w+) children=(\d+)", out)
    if not md:
        return rows or None, errors, "error", None
    st, nch = md.group(1), int(md.group(2))
    # ERROR/FAIL 是终态：整批表达式在平台侧跑不起来（如该数据集的字段/设置不兼容）。
    # 若当成 running 会白等 8×3min/批（2026-10-22 price_signal_dl 实测：22 批要耗 8 小时）。
    if st in ("ERROR", "FAIL"):
        return rows or None, errors, "fail", nch
    if st != "COMPLETE":
        return None, errors, "running", nch
    if nch == 0:
        return None, errors, "empty", 0
    if len(rows) < nch:
        return (rows or None), errors, "partial", nch
    return rows, errors, "ok", nch


PARTIAL_TRIES = 3     # partial（限流缺子任务）最多重试轮数，之后接受已收结果
WAIT_TRIES = 8        # running/error 最多等待轮数（约 8×3min）


def harvest_until_done(sim_id, ds, tag=""):
    """反复收割一批直到拿全子任务结果 → (rows, errs, state)。

    设计要点（2026-10-22 实测教训）：
    - partial 只重试 PARTIAL_TRIES 轮：若某个子任务本身没有 alpha，无限重试会拖死整轮；
    - 每轮结果按 alpha id 跨轮合并：partial 每轮缺的未必是同一条；
    - running/error 用 3 分钟退避，给平台排队时间。
    """
    rows, errs, state, nch = None, [], None, None
    part = waited = 0
    delay = 0
    while True:
        if delay:
            time.sleep(delay)
        got, errs, state, nch = harvest(sim_id, ds)
        if got:
            seen = {r[0] for r in (rows or [])}
            rows = list(rows or []) + [r for r in got if r[0] not in seen]
        if state in ("ok", "empty", "fail"):
            return rows, errs, state
        if state == "partial" and nch and len(rows) >= nch:
            return rows, errs, "ok"
        if state == "partial":
            part += 1
            if part >= PARTIAL_TRIES:
                return rows, errs, "partial"
            delay = 20
        else:
            waited += 1
            if waited >= WAIT_TRIES:
                return rows, errs, state
            delay = 180
        print(f"  [harvest] {tag} {state}（已收 {len(rows or [])}/{nch}）第 {part + waited} 次重试")


# ---------------- 设置轴扫描（缺陷1：单一设置点判死 = 最大假阴性来源）

SWEEP_VARIANTS = [
    ("u2500", {"universe": "TOP2500"}),
    ("subind", {"neutralization": "SUBINDUSTRY"}),
    ("crowd", {"neutralization": "CROWDING"}),
]


def settings_sweep(ds, all_alphas, ck, res, max_s):
    """1.2 ≤ max_S < 1.58 的「近闸」集，自动补跑 3 个设置变体。

    归因依据（2026-10-22/23 实测）：
      · 同一表达式 TOPCS1600 S1.30 → TOP2500 **1.81**（+0.51）；
      · neutralization=SUBINDUSTRY 把 sub 0.78→0.93、rob 0.55→1.13，几乎不损 S；
      · 论坛实测同内核换 CROWDING 可把 2Y 从 1.15 抬到 2.17。
    旧流程只在 TOPCS1600/FAST/decay4 一个点上判生死 ⇒ 已判 DEAD 的集里必然混着「换设置就过闸」的。
    成本：3 变体 × 2 条表达式 = 6 条仿真。
    """
    if not (1.2 <= max_s < 1.58) or not all_alphas:
        return max_s, {}
    cand = sorted((a for a in all_alphas if a.get("s") is not None),
                  key=lambda a: -a["s"])[:2]      # n=1 的批必为空批，必须 ≥2 条
    codes = fetch_codes([a["alpha"] for a in cand])
    pairs = [(a["tpl"], codes[a["alpha"]]) for a in cand if codes.get(a["alpha"])]
    if len(pairs) < 2:
        print("  [sweep] 取不到 ≥2 条表达式，跳过设置轴扫描")
        return max_s, {}
    out = {}
    for tag, st in SWEEP_VARIANTS:
        key = f"{ds}@sw_{tag}"
        prev = [tuple(x) for x in (ck.get("sims", {}).get(key) or []) if x and x[0]]
        if prev:
            sims = prev
            print(f"  [sweep] {tag}: 复用已派发 {len(sims)} 批")
        else:
            print(f"  [sweep] {tag}: 派发 {len(pairs)} 条（覆写 {st}）")

            def _persist(p, _k=key):
                ck["sims"][_k] = list(p); save_ckpt(ck)

            sims = dispatch([(f"{t}_{tag}", e) for t, e in pairs], ds, f"sw_{tag}",
                            on_batch=_persist, settings=st)
            ck["sims"][key] = sims
            save_ckpt(ck)
        rows_all = []
        for sid, tpl, bi in sims:
            if not sid:
                continue
            rows, errs, state = harvest_until_done(sid, ds, tag=f"sw_{tag}_{bi}")
            note_bad_tokens(errs)
            for aid, sv, fv, y2, sub in (rows or []):
                rows_all.append({"alpha": aid, "tpl": f"sw_{tag}", "s": sv, "f": fv,
                                 "y2": y2, "sub": sub, "batch": f"sw_{tag}"})
        if not rows_all:
            print(f"  [sweep] {tag}: 无结果")
            continue
        all_alphas.extend(rows_all)                  # 让后面 prod/候选判定看到
        sm = max((r["s"] for r in rows_all if r["s"] is not None), default=None)
        s2 = max((r["y2"] for r in rows_all if r["y2"] is not None), default=None)
        out[tag] = {"max_s": sm, "max_2y": s2, "n": len(rows_all), "settings": st}
        print(f"  [sweep] {tag}: max_S={sm} max_2Y={s2} n={len(rows_all)}")
        if sm is not None and sm > max_s:
            max_s = sm
    return max_s, out


def audit_fields(con, ck, res, dss):
    """字段 × 族 覆盖审计：打印每个集哪些字段从没跑过哪些结构（不跑仿真）。"""
    all_tpl = [f"{a}_{b or 'pl'}" for a, b in FAMILIES] + ["dw", "pp"]
    for ds in dss:
        v = (res.get("results") or {}).get(ds) or {}
        sel = None
        # 优先用 checkpoint 锁定的字段（与已跑结果同源）
        locked = (ck.get("fields") or {}).get(ds)
        if locked:
            sel = [{"field_name": f} for f in locked]
        cat = dict(con.execute(
            "SELECT dataset, category FROM dataset_profile WHERE region='EUR'"))
        print(f"\n=== audit {ds} ({cat.get(ds)}) verdict={v.get('verdict')} max_S={v.get('max_s')} ===")
        if not sel:
            print("  未锁定字段（该集尚未开跑）")
            continue
        names = [r["field_name"] for r in sel]
        cov = batch_field_coverage(ds, names)
        print(f"  {'field':34s} " + " ".join(f"{t[:6]:>6s}" for t in all_tpl))
        for f in names:
            got = set(cov.get(f, set()))
            row = "".join(f"{'✓' if t in got else '·':>7s}" for t in all_tpl)
            print(f"  {f:34s}{row}")
        total = len(names) * len(all_tpl)
        cells = sum(len(set(cov.get(f, set())) & set(all_tpl)) for f in names)
        print(f"  覆盖 {cells}/{total} 格（{cells/ total:.0%}）")
    print("")


def sweep_done_sets(con, ck, res):
    """缺陷1 回溯：对**已判完**且 1.2<=max_S<1.58、prod 未爆的集补扫设置轴。

    旧流程这些集是在单一设置点（TOPCS1600/FAST/decay4）上判的 DEAD/BORDERLINE，
    换 universe/neutralization 完全可能直接过闸（实测 +0.51 S 的先例）。
    """
    rs = res.get("results") or {}
    cands = []
    for ds, v in rs.items():
        if not isinstance(v, dict):
            continue
        sv, pr = v.get("max_s"), v.get("prod_top")
        if sv is None or not (1.2 <= sv < 1.58):
            continue
        if pr is not None and pr >= 0.7:      # prod 已爆，抬 S 也无意义
            continue
        if len(v.get("alphas") or []) < 2:    # 取不到 2 条表达式就没法派发
            continue
        cands.append((ds, v))
    cands.sort(key=lambda kv: -kv[1]["max_s"])
    print(f"[sweep-done] 待扫 {len(cands)} 集: {[c[0] for c in cands]}")
    cat_map = dict(con.execute(
        "SELECT dataset, category FROM dataset_profile WHERE region='EUR'"))
    for ds, v in cands:
        alphas = list(v.get("alphas") or [])
        print(f"\n=== sweep {ds} (max_S={v['max_s']}, 原 verdict={v.get('verdict')}) ===")
        try:
            max_s, sweep = settings_sweep(ds, alphas, ck, res, v["max_s"])
        except Exception as e:
            print(f"  [sweep-done] {ds} 异常：{type(e).__name__}: {e}")
            continue
        if not sweep:
            continue
        v["settings_sweep"] = sweep
        v["alphas"] = alphas
        v["max_s"] = round(max_s, 3)
        ys = [x["max_2y"] for x in sweep.values() if x.get("max_2y") is not None]
        if ys:
            v["max_2y"] = round(max((v.get("max_2y") or -9), max(ys)), 3)
        ba = max((a for a in alphas if a.get("s") is not None),
                 key=lambda a: a["s"], default=None)
        joint = [a for a in alphas if (a["s"] or 0) >= 1.5
                 and (a.get("f") or 0) >= 1.0 and (a["y2"] or 0) >= 1.58]
        v["n_joint"] = len(joint)
        v["verdict"] = ("ALIVE" if joint else
                        ("BORDERLINE" if max_s >= 1.3 else "DEAD"))
        if ba:
            def _g(x, lim):
                return None if x is None else round(max(0.0, lim - float(x)) / lim, 3)
            v["gates"] = {
                "S": {"value": ba["s"], "limit": 1.58, "gap": _g(ba["s"], 1.58)},
                "F": {"value": ba.get("f"), "limit": 1.0, "gap": _g(ba.get("f"), 1.0)},
                "2Y": {"value": ba.get("y2"), "limit": 1.58, "gap": _g(ba.get("y2"), 1.58)},
                "prod": {"value": v.get("prod_top"), "limit": 0.7,
                         "gap": (None if v.get("prod_top") is None
                                 else round(max(0.0, v["prod_top"] - 0.7), 3))},
            }
            v["deliverable"] = bool(ba["s"] >= 1.58 and (ba.get("f") or 0) >= 1.0
                                    and (ba.get("y2") or 0) >= 1.58
                                    and v.get("prod_top") is not None
                                    and v["prod_top"] < 0.7)
        res["results"][ds] = v
        save_results(res)
        beat(ds, note="sweep-done")
        emit_digest(ds, cat_map.get(ds), res, ck, len(ck.get("done") or []))
    print("\n[sweep-done] 完成")


# ---------------------------------------------------------------- 主流程

def main():
    global MAX_INFLIGHT
    only = None
    limit = None
    priority_cats = None
    only_cats = None         # --only-cats OTHER,PV：只跑这些类目（硬锁定，非排序）
    priority_min_cov = 0.8   # B 方案（2026-10-23 用户批准）：覆盖率门槛 0.5→0.8，低覆盖集直接跳过
    skip_lit = False
    keep_fields = None       # --keep-fields a,b：这些字段跳过「平台字段清单」过滤（清单常漏掉可用字段）
    audit_ds = None          # --audit a,b：只打印字段×族覆盖矩阵，不跑仿真
    sweep_done = False       # --sweep-done：只对已判完的近闸集补扫设置轴，然后退出
    for i, a in enumerate(sys.argv):
        if a == "--datasets":
            only = sys.argv[i + 1].split(",")
        if a == "--limit":
            limit = int(sys.argv[i + 1])
        if a == "--priority-cats":
            priority_cats = sys.argv[i + 1].split(",")
        if a == "--only-cats":
            only_cats = sys.argv[i + 1].split(",")
        if a == "--priority-min-cov":
            priority_min_cov = float(sys.argv[i + 1])
        if a == "--skip-lit":
            skip_lit = True
        if a == "--keep-fields":
            keep_fields = [x.strip() for x in sys.argv[i + 1].split(",") if x.strip()]
        if a == "--max-inflight":
            MAX_INFLIGHT = max(1, int(sys.argv[i + 1]))
        if a == "--sweep-done":
            sweep_done = True
        if a == "--audit":
            audit_ds = sys.argv[i + 1].split(",")

    con = db_connect(DB, readonly=True)   # 本流程只读台账（写库都在 campaign 子进程里）
    con.row_factory = sqlite3.Row

    load_bad_tokens()
    if BAD_TOKENS:
        print(f"[preflight] 已加载平台黑名单 {len(BAD_TOKENS)} 个：{sorted(BAD_TOKENS)}")
    beat(note="start")

    # 已点亮判定（同一 category 下我方已提交 > 3 ⇒ 不优先）
    counts = compute_lit("EUR")
    lit_cats = {c: n for c, n in counts.items() if n > LIT_THRESHOLD}
    cats_all = [r[0] for r in con.execute(
        "SELECT DISTINCT category FROM dataset_profile WHERE region='EUR' AND category IS NOT NULL")]
    unlit = {c: counts.get(c.upper(), 0) for c in cats_all
             if counts.get(c.upper(), 0) <= LIT_THRESHOLD}
    print(f"[lit] 已点亮(>{LIT_THRESHOLD} 个提交，降权): "
          + (", ".join(f"{c}={n}" for c, n in sorted(lit_cats.items(), key=lambda x: -x[1])) or "无"))
    print(f"[lit] 未点亮(可挖): "
          + (", ".join(f"{c}={n}" for c, n in sorted(unlit.items())) or "无"))
    print(f"[gate] 同时在飞作业上限 = {MAX_INFLIGHT}（--max-inflight 可调）")

    ds_list = all_datasets(con, only=only, limit=limit, priority_cats=priority_cats,
                           lit_cats=counts, skip_lit=skip_lit)
    if only_cats:
        oc = {c.upper() for c in only_cats}
        before = len(ds_list)
        ds_list = [d for d in ds_list if (d.get("category") or "").upper() in oc]
        print(f"[only-cats] 锁定 {sorted(oc)}：{before} → {len(ds_list)} 个集")
    ck = load_ckpt()
    res = load_results()

    if audit_ds:
        audit_fields(con, ck, res, audit_ds)
        return

    if sweep_done:
        sweep_done_sets(con, ck, res)
        return

    print(f"[campaign] 数据集总数 {len(ds_list)}｜已完成 {len(ck['done'])}")
    for d in ds_list:
        ds = d["dataset"]
        if ds in ck["done"]:
            continue
        cov = d["cov"] or 0
        cat_u = (d.get("category") or "").upper()
        pri = priority_cats and cat_u in {c.upper() for c in priority_cats}
        eff_min = priority_min_cov if pri else 0.8
        if is_virgin(d):
            eff_min = min(eff_min, VIRGIN_MIN_COV)
        if cov < eff_min:
            print(f"[skip] {ds} coverage {cov:.2f} < {eff_min}"
                  + ("（优先类别放宽门槛）" if pri else ""))
            ck["done"].append(ds)
            res["results"][ds] = {"verdict": "SKIPPED_LOW_COV", "coverage": cov}
            save_ckpt(ck); save_results(res)
            emit_digest(ds, d["category"], res, ck, len(ds_list))
            continue

        print(f"\n=== {ds} ({d['category']}) fields={d['n_fields']} cov={cov:.2f} vs={d['vs']} ===")
        beat(ds, note="dataset-start")
        prev_fields = (ck.get("fields") or {}).get(ds)
        sel = select_fields(con, ds, field_min_cov=eff_min, only_names=prev_fields,
                            keep_fields=keep_fields)
        # 2026-10-24：处女地集字段级门槛也自适应。equity_conc_metrics 实测 18 个 VECTOR 字段
        # 覆盖率清一色 0.197，在 0.35 下取不到任何字段 ⇒ 整集被 SKIPPED_TOO_FEW_FIELDS 挡死，
        # 而它恰恰是处女地里暴露最多样（4 种）的集。DEU 实证：cov 0.27–0.34 的字段平台全部
        # 可仿真，只是 max|S| 约 0.48 ⇒ 低覆盖是「预算筛选器」不是「平台限制」。
        if len(sel) < 3 and is_virgin(d) and eff_min > 0.1:
            for _mc in (0.1, 0.0):
                sel = select_fields(con, ds, field_min_cov=_mc, only_names=prev_fields,
                                    keep_fields=keep_fields)
                if len(sel) >= 3:
                    print(f"  [cov] {ds}: 处女地字段级门槛 {eff_min} → {_mc}（原门槛下 0 字段）")
                    break
        if len(sel) < 3:
            print(f"  字段不足（<3，字段级门槛 {eff_min}），跳过")
            ck["done"].append(ds)
            res["results"][ds] = {"verdict": "SKIPPED_TOO_FEW_FIELDS", "coverage": cov}
            save_ckpt(ck); save_results(res)
            emit_digest(ds, d["category"], res, ck, len(ds_list))
            continue

        # 字段选择持久化：同一集续跑必须沿用同一套字段。否则筛选器一改，已派发族用旧字段、
        # 新派发族用新字段，族间不可比（2026-10-22 修筛选器时发现）。
        if not prev_fields:
            ck.setdefault("fields", {})[ds] = [x["field_name"] for x in sel]
            save_ckpt(ck)
            print(f"  [fields] 锁定代表字段 {len(sel)} 个")

        print_form_audit(ds, sel)
        # 2026-10-24 ①：打印透明度分档，肉眼抽查「黑盒集是否还在被形态分类器假装懂」
        _tiers = collections.Counter(r.get("ftier") or field_tier(r, d["category"], ds) for r in sel)
        print(f"  [tier] {ds}: " + " ".join(f"{k}={v}" for k, v in sorted(_tiers.items())))
        # 2026-10-24 ①：机制概念分布（8 问路径）。命中率即「机制驱动选路」的覆盖面
        _cons = collections.Counter()
        _n_hit = 0
        for r in sel:
            cs = field_concepts(r, d["category"], ds)
            if cs:
                _n_hit += 1
            for c in (cs or ["<无概念>"]):
                _cons[c] += 1
        print(f"  [concept] {ds}: 机制命中 {_n_hit}/{len(sel)} 字段 → "
              + " ".join(f"{CONCEPT_ZH.get(k, k)}={v}" for k, v in _cons.most_common()))
        # 2026-10-24 ③：本地读 S1 台账的 preprocessing（受控词表；自由文本不采信）
        pp_map = load_s1_preprocessing(con, ds)
        if pp_map:
            print(f"  [pp] {ds}: S1 预处理命中 {len(pp_map)} 个字段："
                  + ", ".join(f"{k}→{'+'.join(v)}" for k, v in list(pp_map.items())[:5]))
        freq = DS_FREQ.get(ds, "quarterly" if d["category"] in (
            "ANALYST", "FUNDAMENTAL", "INSIDERS", "INSTITUTIONS", "EARNINGS", "MACRO") else "daily")
        exprs = build_exprs(sel, freq, cat=d["category"], ds=ds, pp_map=pp_map)
        print(f"  代表字段 {len(sel)}（维度 {len(set(x['dim'] for x in sel))}）× 模板族 = {len(exprs)} 条")
        # 2026-10-24 ②：Expected Exposure 分布 —— 收益来源多样性是 prod 相关性的结构性解。
        # 单暴露集 = 与既有同源 alpha 高相关的结构性风险，S/2Y 再高也难独立过 prod。
        _exp = collections.Counter(EXPR_EXPOSURE.get(e, "other") for _t, e in exprs)
        print(f"  [expo] {ds}: {len(_exp)} 种暴露 → "
              + " ".join(f"{k}={v}" for k, v in sorted(_exp.items(), key=lambda kv: -kv[1])))
        if len(_exp) <= 2:
            _dom = _exp.most_common(1)[0]
            print(f"  [expo] ⚠ {ds} 仅 {len(_exp)} 种暴露（{_dom[0]} 占 {_dom[1]}/{len(exprs)}）"
                  f"⇒ 低多样性，prod 相关性结构性风险，优先度下调")

        # 续跑：**按模板族**复用已派发批次，缺哪个族就只派哪个族。
        # ⚠ 三坑（2026-10-22 全踩过）：
        #   ① 不能用 tpl != "cs" 判新旧：旧架构还有 d1/ed/d2/dw 等短名族，会误复用；
        #   ② 不能「有复用就整体跳过派发」：sentiment27 只有 dw 族命中旧批 → 144 条只收 2 条就判 DEAD；
        #   ③ 同名的旧族表达式可能与新架构不同 → 逐批校验「批内表达式 ⊆ 本次该族的表达式」才准复用。
        cur_by_tpl = collections.defaultdict(list)
        for tpl, e in exprs:
            cur_by_tpl[tpl].append(e)
        prev_by_tpl = collections.defaultdict(list)
        for x in (ck.get("sims", {}).get(ds) or []):
            if x and x[0] and x[1] in cur_by_tpl:
                prev_by_tpl[x[1]].append(tuple(x))
        sims, need = [], []
        for tpl, elist in cur_by_tpl.items():
            lst = prev_by_tpl.get(tpl) or []
            want = set(elist)
            reuse_ok = bool(lst)
            if reuse_ok:
                for _sid, _t, bi in lst:
                    fn = os.path.join(ROOT, "cache", f"_camp_{ds}_{tpl}_{bi}.txt")
                    if not os.path.exists(fn):
                        reuse_ok = False
                        break
                    got = {l.strip() for l in open(fn, encoding="utf-8") if l.strip()}
                    if not got <= want:      # 旧批内容 ≠ 新架构该族 → 不能复用
                        reuse_ok = False
                        break
            if reuse_ok:
                sims += lst
                # 缺陷3修复：子集判据会静默丢表达式——复用后必须算差集并补派。
                covered = set()
                for _sid, _t, _bi in lst:
                    fn = os.path.join(ROOT, "cache", f"_camp_{ds}_{_t}_{_bi}.txt")
                    try:
                        covered |= {l.strip() for l in open(fn, encoding="utf-8") if l.strip()}
                    except Exception:
                        pass
                missing = [e for e in elist if e not in covered]
                if missing:
                    print(f"  [resume] {tpl}: 旧批只覆盖 {len(covered)}/{len(elist)} 条 → 补派 {len(missing)} 条")
                    need.append((tpl + "_f", missing))
            else:
                need.append((tpl, elist))
        if sims:
            print(f"  [resume] 复用已派发 {len(sims)} 批（覆盖 {len(cur_by_tpl) - len(need)}/{len(cur_by_tpl)} 族）")
        if need:
            print(f"  [dispatch] 派发 {sum(len(e) for _, e in need)} 条（{len(need)} 族未覆盖）")
            _base = list(sims)

            def _persist(partial, _ds=ds, _base=_base):
                ck["sims"][_ds] = _base + list(partial)
                save_ckpt(ck)

            new_sims = dispatch([(tpl, e) for tpl, elist in need for e in elist], ds, "t",
                                on_batch=_persist)
            ck["sims"][ds] = sims + new_sims
            save_ckpt(ck)
            sims += new_sims

        # 单条批修复：历史断点里 n=1 的批次提交后必为 COMPLETE/children=0（2026-10-22 实测），
        # 结果永远收不到。把这些孤儿表达式合并成均分整批（≤10/批）重派一次。
        orphan = []
        for _sid, tpl, bi in sims:
            if tpl == "rep":
                continue
            fn = os.path.join(ROOT, "cache", f"_camp_{ds}_{tpl}_{bi}.txt")
            if not os.path.exists(fn):
                continue
            lines = [l.strip() for l in open(fn, encoding="utf-8") if l.strip()]
            if len(lines) == 1:
                orphan.append(lines[0])
        if orphan:
            rep_key = ds + "@rep"
            prev_rep = [tuple(x) for x in (ck.get("sims", {}).get(rep_key) or []) if x and x[0]]
            if prev_rep:
                print(f"  [repair] 复用已重派 {len(prev_rep)} 批")
                sims = list(sims) + prev_rep
            else:
                print(f"  [repair] 单条批孤儿 {len(orphan)} 条 → 合并重派（均分 ≤10/批）")
                def _persist_rep(partial, _k=rep_key):
                    ck["sims"][_k] = list(partial)
                    save_ckpt(ck)

                rep = dispatch([("rep", e) for e in orphan], ds, "rep", on_batch=_persist_rep)
                ck["sims"][rep_key] = rep
                save_ckpt(ck)
                sims = list(sims) + rep

        # 收割（允许部分未完成）
        per_tpl = collections.defaultdict(list)
        all_alphas = []
        err_msgs = []
        n_fail = 0          # 平台侧 FAIL 的批次数（整批跑不起来，非"没结果"）
        failed_batches = []  # (tpl, bi) 整批 FAIL/ERROR → 剔除黑名单后重派（缺陷2 自愈）
        for sim_id, tpl, bi in sims:
            if not sim_id:
                continue
            rows, errs, state = harvest_until_done(sim_id, ds, tag=f"{tpl}_{bi}")
            if state == "empty":
                print(f"  [harvest] {tpl}_{bi} COMPLETE children=0（结构性空批），放弃")
            elif state == "fail":
                n_fail += 1
                failed_batches.append((tpl, bi))
                note_bad_tokens(errs)
                print(f"  [harvest] {tpl}_{bi} 平台侧 FAIL（整批跑不起来）err={errs[:1]}")
                # 同一数据集所有族共用字段与设置：前两批即 FAIL，后面必然同样 FAIL
                if n_fail >= 2 and not all_alphas:
                    print("  [abort] 前 2 批均 FAIL 且无任何结果 → 跳过本集剩余收割")
                    break
                continue
            elif rows and state != "ok":
                print(f"  [harvest] {tpl}_{bi} 部分收割 {len(rows)} 条（state={state}）")
            if not rows:
                print(f"  [harvest] {tpl}_{bi} 无结果（err={errs[:1]}）")
                for e in errs[:1]:
                    err_msgs.append(e)
                continue
            for aid, sv, fv, y2, sub in rows:
                per_tpl[norm_tpl(tpl)].append((aid, sv, y2, sub))
                all_alphas.append({"alpha": aid, "tpl": norm_tpl(tpl), "s": sv, "f": fv,
                                   "y2": y2, "sub": sub, "batch": tpl})

        # ---------- 毒化自愈：整批 FAIL 的表达式剔除黑名单后重派一次（缺陷2）----------
        if failed_batches:
            rep = []
            for _t, _bi in failed_batches:
                fn = os.path.join(ROOT, "cache", f"_camp_{ds}_{_t}_{_bi}.txt")
                try:
                    rep += [(f"{_t}_rp", l.strip()) for l in open(fn, encoding="utf-8") if l.strip()]
                except Exception:
                    pass
            rep, _nbad = filter_bad(rep)
            if len(rep) < 2:
                print(f"  [repair] 剔除黑名单后仅 {len(rep)} 条（<2，空批风险），放弃重派")
            else:
                print(f"  [repair] {len(failed_batches)} 批失败 → 剔除 {_nbad} 条后重派 {len(rep)} 条")
                _key = ds + "@rp"
                _prev = [tuple(x) for x in (ck.get("sims", {}).get(_key) or []) if x and x[0]]
                if _prev:
                    _sims = _prev
                    print(f"  [repair] 复用已重派 {len(_sims)} 批")
                else:
                    def _persist_rp(pp, _k=_key):
                        ck["sims"][_k] = list(pp); save_ckpt(ck)
                    _sims = dispatch(rep, ds, "rp", on_batch=_persist_rp)
                    ck["sims"][_key] = _sims
                    save_ckpt(ck)
                for _sid, _t2, _b2 in _sims:
                    if not _sid:
                        continue
                    _rows, _errs, _st = harvest_until_done(_sid, ds, tag=f"rp_{_b2}")
                    note_bad_tokens(_errs)
                    for aid, sv, fv, y2, sub in (_rows or []):
                        per_tpl[norm_tpl(_t2)].append((aid, sv, y2, sub))
                        all_alphas.append({"alpha": aid, "tpl": norm_tpl(_t2), "s": sv,
                                           "f": fv, "y2": y2, "sub": sub, "batch": _t2})

        best = {}
        max_s = -9
        max_2y = -9
        for tpl, lst in per_tpl.items():
            ms = max((x[1] for x in lst), default=None)
            m2 = max((x[2] for x in lst), default=None)
            best[tpl] = {"max_s": ms, "max_2y": m2}
            if ms is not None:
                max_s = max(max_s, ms)
            if m2 is not None:
                max_2y = max(max_2y, m2)

        # ---------------- 阶段 2：后处理电池（对 S≥0.8 的 top3 构造）----------------
        tops = sorted((a for a in all_alphas if a["s"] is not None),
                      key=lambda a: -a["s"])[:3]
        tops = [a for a in tops if a["s"] >= 0.8]
        if tops:
            print(f"  [stage2] 后处理电池：top{len(tops)} 构造 × 5 变体")
            codes = fetch_codes([a["alpha"] for a in tops])
            pp = []
            for a in tops:
                c = codes.get(a["alpha"])
                if c:
                    pp += build_postproc(c)
            if pp:
                pp_key = ds + "@pp"
                prev_pp = [tuple(x) for x in (ck.get("sims", {}).get(pp_key) or []) if x and x[0]]
                if prev_pp:
                    sims2 = prev_pp
                    print(f"  [resume] 复用已派发后处理 {len(sims2)} 批")
                else:
                    def _persist_pp(partial, _k=pp_key):
                        ck["sims"][_k] = list(partial)
                        save_ckpt(ck)

                    sims2 = dispatch(pp, ds, "pp", on_batch=_persist_pp)
                    ck["sims"][pp_key] = sims2
                    save_ckpt(ck)
                for sim_id, tpl, bi in sims2:
                    if not sim_id:
                        continue
                    rows, errs, state = harvest_until_done(sim_id, ds, tag=f"pp_{bi}")
                    if state == "empty":
                        print(f"  [harvest] {tpl}_{bi} COMPLETE children=0（结构性空批），放弃")
                    elif rows and state != "ok":
                        print(f"  [harvest] {tpl}_{bi} 部分收割 {len(rows)} 条（state={state}）")
                    if not rows:
                        continue
                    for aid, sv, fv, y2, sub in rows:
                        per_tpl[norm_tpl(tpl)].append((aid, sv, y2, sub))
                        all_alphas.append({"alpha": aid, "tpl": norm_tpl(tpl), "s": sv, "f": fv,
                                           "y2": y2, "sub": sub, "batch": tpl})
                # 阶段2后重算 per-template best
                for tpl, lst in per_tpl.items():
                    best[tpl] = {"max_s": max((x[1] for x in lst), default=None),
                                 "max_2y": max((x[2] for x in lst), default=None)}
                max_s = max((b["max_s"] for b in best.values() if b["max_s"] is not None), default=max_s)
                max_2y = max((b["max_2y"] for b in best.values() if b["max_2y"] is not None), default=max_2y)

        # ---------- 载体结构扩散：本集最强族补跑未覆盖的 probe 字段 ----------
        try:
            _cx = carrier_expand(ds, sel, best, freq, ck, len(best))
            for _sid, _tc, _bc in _cx:
                if not _sid:
                    continue
                _rows, _errs, _st = harvest_until_done(_sid, ds, tag=f"cx_{_bc}")
                note_bad_tokens(_errs)
                for aid, sv, fv, y2, sub in (_rows or []):
                    per_tpl[norm_tpl(_tc)].append((aid, sv, y2, sub))
                    all_alphas.append({"alpha": aid, "tpl": norm_tpl(_tc), "s": sv,
                                       "f": fv, "y2": y2, "sub": sub, "batch": _tc})
            if _cx:
                for tpl_n, lst in per_tpl.items():
                    best[tpl_n] = {"max_s": max((x[1] for x in lst), default=None),
                                   "max_2y": max((x[2] for x in lst if x[2] is not None), default=None)}
                max_s = max((b["max_s"] for b in best.values() if b["max_s"] is not None), default=max_s)
                max_2y = max((b["max_2y"] for b in best.values() if b["max_2y"] is not None), default=max_2y)
        except Exception as e:
            print(f"  [carrier] 异常，跳过：{type(e).__name__}: {e}")

        # ---------- 字段 × 族 覆盖矩阵（审计：哪些格子从没跑过）----------
        field_cov = {}
        try:
            _names = [r["field_name"] for r in sel]
            _all_tpl = {t for t, _ in FAMILIES} | {"dw", "pp"}
            _cov = batch_field_coverage(ds, _names)
            field_cov = {f: sorted(v) for f, v in _cov.items()}
            _cells = sum(len(set(v) & _all_tpl) for v in _cov.values())
            _tot = len(_names) * len(_all_tpl)
            _untested = [f for f in _names if len(set(_cov.get(f, set())) & _all_tpl) < 3]
            print(f"  [matrix] 字段 {len(_names)} × 族 {len(_all_tpl)} → 覆盖 {_cells}/{_tot} 格"
                  + (f"；薄覆盖字段 {len(_untested)} 个: {_untested[:5]}" if _untested else ""))
        except Exception as e:
            print(f"  [matrix] 统计失败：{type(e).__name__}: {e}")

        # 联合判定：S 与 2Y 必须同时过闸（旧版只看 max_S，会把 2Y=0 的假阳性判 ALIVE）
        # 联合判据含 F（2026-10-21 用户指出）：S≥1.5 且 F≥1.0 且 2Y≥1.58
        joint = [a for a in all_alphas if (a["s"] or 0) >= 1.5
                 and (a.get("f") or 0) >= 1.0 and (a["y2"] or 0) >= 1.58]
        n_unknown = sum(1 for e in err_msgs if "unknown variable" in e.lower())

        # ---------- 缺陷1修复：近闸集（1.2<=S<1.58）自动扫设置轴 ----------
        sweep = {}
        try:
            max_s, sweep = settings_sweep(ds, all_alphas, ck, res, max_s)
            if sweep:
                ys = [v["max_2y"] for v in sweep.values() if v.get("max_2y") is not None]
                if ys:
                    max_2y = max([max_2y] + ys)
                joint = [a for a in all_alphas if (a["s"] or 0) >= 1.5
                         and (a.get("f") or 0) >= 1.0 and (a["y2"] or 0) >= 1.58]
                pt = collections.defaultdict(list)
                for a in all_alphas:
                    if a.get("s") is not None:
                        pt[a["tpl"]].append((a["alpha"], a["s"], a.get("y2"), a.get("sub")))
                for tpl_n, lst in pt.items():
                    best[tpl_n] = {"max_s": max((x[1] for x in lst), default=None),
                                   "max_2y": max((x[2] for x in lst if x[2] is not None), default=None)}
        except Exception as e:
            print(f"  [sweep] 异常，跳过：{type(e).__name__}: {e}")

        # 近闸/入闸候选测 prod（死局预警：S 高但 prod 高 = 白挖）。
        # 只对 max_S>=1.2 的集测最优那颗，避免无谓占用 prod 异步队列。
        prod_top = None
        best_alpha = (max((a for a in all_alphas if a["s"] is not None),
                          key=lambda a: a["s"], default=None) if all_alphas else None)
        yp = None
        if best_alpha is not None and max_s >= 1.4:
            try:
                yp = year_profile(best_alpha["alpha"])
                if yp:
                    print(f"  [year] {best_alpha['alpha']} 首个持仓年 {yp['first_year']}"
                          f"（起点 {yp['start_year']}）｜有效 {yp['n_years']} 年｜"
                          f"单年集中 {yp['top_share']:.0%}（{yp['top_year']}）｜"
                          f"剔除后年均 {yp['ex_top_ret']:+.1%}"
                          + ("  ✗ FRAGILE" if yp["fragile"] else "  ✓"))
            except Exception as e:
                print(f"  [year] 画像失败：{type(e).__name__}: {e}")

        if best_alpha is not None and max_s >= 1.2:
            print(f"  [prod] 测最优候选 {best_alpha['alpha']}（S={best_alpha['s']}）的 prod 相关性…")
            prod_top = check_prod(best_alpha["alpha"])
            if prod_top is not None:
                tag = "✗ prod>0.7 死局" if prod_top >= 0.7 else "✓ prod 过线"
                print(f"  [prod] {best_alpha['alpha']} prod={prod_top:.3f} {tag}")

        if not all_alphas:
            verdict = "SIM_FAIL" if n_fail else ("ERROR" if err_msgs else "NO_DATA")
        elif joint:
            verdict = "ALIVE"
        elif max_s >= 1.3:
            verdict = "BORDERLINE"
        else:
            verdict = "DEAD"

        # ---------- 缺陷5修复：verdict 之外给出逐闸距离 + 可交付标记 ----------
        def _gap(v, lim):
            if v is None:
                return None
            return round(max(0.0, lim - float(v)) / lim, 3)

        b_s = best_alpha["s"] if best_alpha else None
        b_f = best_alpha.get("f") if best_alpha else None
        b_y2 = best_alpha.get("y2") if best_alpha else (max_2y if max_2y > -9 else None)
        gates = {
            "S":    {"value": b_s, "limit": 1.58, "gap": _gap(b_s, 1.58)},
            "F":    {"value": b_f, "limit": 1.0, "gap": _gap(b_f, 1.0)},
            "2Y":   {"value": b_y2, "limit": 1.58, "gap": _gap(b_y2, 1.58)},
            "prod": {"value": prod_top, "limit": 0.7,
                     "gap": (None if prod_top is None else round(max(0.0, prod_top - 0.7), 3))},
        }
        deliverable = bool(b_s and b_s >= 1.58 and (b_f or 0) >= 1.0
                           and (b_y2 or 0) >= 1.58
                           and prod_top is not None and prod_top < 0.7
                           and not (yp and yp.get("fragile")))   # 年度画像脆弱 ⇒ 一票否决
        deliv_score = max([g["gap"] for g in gates.values() if g.get("gap") is not None] or [1.0])

        res["results"][ds] = {
            "coverage": cov, "n_fields": d["n_fields"], "n_sel": len(sel),
            "n_dims": len(set(x["dim"] for x in sel)), "freq": freq,
            "per_template": best, "max_s": round(max_s, 3) if max_s > -9 else None,
            "max_2y": round(max_2y, 3) if max_2y > -9 else None,
            "n_joint": len(joint), "n_alphas": len(all_alphas),
            "n_unknown_field_err": n_unknown, "n_fail_batches": n_fail,
            "prod_top": prod_top, "settings_sweep": sweep, "field_coverage": field_cov,
            "year_profile": yp,
            "gates": gates, "deliverable": deliverable, "deliv_score": deliv_score,
            "verdict": verdict, "alphas": all_alphas,
        }
        ck["done"].append(ds)
        save_ckpt(ck); save_results(res)
        sw_txt = ("  sweep=" + ",".join(f"{k}:{v['max_s']}" for k, v in (sweep or {}).items())
                  if sweep else "")
        print(f"  → verdict={verdict}  max_S={max_s:.2f}  max_2Y={max_2y:.2f}  "
              f"joint(S>=1.5&2Y>=1.58)={len(joint)}  n_alphas={len(all_alphas)}  "
              f"unknown_field_err={n_unknown}  deliv={deliverable}"
              f"(score={deliv_score}){sw_txt}")
        for tpl, b in sorted(best.items(), key=lambda kv: -(kv[1]["max_s"] or -9)):
            print(f"     {tpl:3s}  S={b['max_s'] if b['max_s'] is not None else '—'}  2Y={b['max_2y'] if b['max_2y'] is not None else '—'}")
        beat(ds, note="dataset-done")
        emit_digest(ds, d["category"], res, ck, len(ds_list))

    print(f"\n[campaign] 本轮完成，累计 {len(ck['done'])}/{len(ds_list)}")


if __name__ == "__main__":
    main()
