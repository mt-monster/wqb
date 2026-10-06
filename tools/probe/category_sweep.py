#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""category_sweep.py — L0 类别普查：指定 region 遍历**全部** category，产出每类的字段池。

与既有工具的分工（**不要重复实现，也不要混用**）：
  - ``category_field_triage.py``：数据集级**判死**分诊（两源判死 + 族连坐 + 拥挤）。
    它的甜点判据（``alpha_count ∈ [10,50]``）与真实产出**矛盾**——DEU ``model28``
    甜点=0 却出 12 条 RA-clean；``predictive_starmine`` 被族连坐判死却出 27 条（全区最高）。
    本工具**不复用它的判级**，只把它当「族连坐提示」用。
  - ``field_signal_mine.py``：字段级历史 |sharpe| 先验。本工具的种子排序沿用其方法论。
  - 本工具：category 级**普查**——回答「这个区有哪些类、每类有多少可挖的字段、
    历史上出过什么」，不做判死、不做 ideas。

★ 三条设计铁律（2026-10-06 DEU 193 集实测得出，违反即失效）：
  1. **`alpha_count` 不做入选判据，只做拥挤排除闸**。它是拥挤度（prod 墙）指标，
     不是信号强度指标。实测 S1.3~1.58 的「次强」条全库有 851 条，严格口径会全扔。
     仅保留 ``alpha_count > --crowd-ac``（默认 1000）判拥挤——这条与 prod 墙实测吻合。
  2. **必须有 NULL 兜底桶**。``datasets`` 表全库有 184 行 ``category IS NULL``；
     DEU 有 6 集 category 为 NULL、**其中 3 集有 RA-clean 产出**。按 category 分发时
     这批集会整体消失，故 ``(未分类)`` 永远作为一个桶参与遍历。
  3. **族连坐只降权不判死**。假阳性代价（封掉 27 条产出）远高于漏检代价。
     故 ``--family-sim`` 命中只打 ``family_risk`` 标签并排到本类**末位**，不剔除。

用法：
    python tools/probe/category_sweep.py --region DEU
    python tools/probe/category_sweep.py --region DEU --json out.json --top 8
    python tools/probe/category_sweep.py --region DEU --seed-fields --json seeds.json
    python tools/probe/category_sweep.py --region GBR --min-signal 0.5# 排种子用的历史信号下限

输出（每类一行）：
  category / 集数 / 字段数 / 可用字段数 / 荒地率 / 历史达标条数 / 苗头候选字段数 / 判定
判定四态：``★苗头``（有历史达标且有候选字段）/ ``待探``（有候选字段无历史） /
``贫瘠``（候选字段 < --min-fields）/ ``已枯``（历史有产出但当前无候选字段）

⚠ 边界：
  - **点塔状态不在此判定**（塔 ≠ ``datasets.category``），开波前仍须 ``get_pyramid_alphas``。
  - 本工具**零回测零 API**，产物是「字段池」，**不是 ideas**，禁止直接注入 GEM。
  - ``alpha_count``/``coverage`` 是本地 catalog 快照，**存在性只信平台**
    （``get_datafields``）；类型/拥挤度可本地粗筛。
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from typing import Any, Dict, List, Optional, Tuple

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(os.path.dirname(_HERE))
if os.path.join(_ROOT, "src") not in sys.path:
    sys.path.insert(0, os.path.join(_ROOT, "src"))

# 只读工具必须传 readonly=True（wqb.db_conn 契约：置 True 走 mode=ro URI，
# 跳过 PRAGMA journal_mode=WAL，避免「不写任何行也改库文件字节」）。
# 白名单外禁止裸 sqlite3.connect（守卫 test_db_write_guards::TestNoNakedSqliteConnect）。
from wqb.db_conn import connect as db_connect  # noqa: E402

DB = os.path.join(_ROOT, "data", "wqb.db")

#: 未分类兜底桶名（datasets.category 为 NULL/空/未知值时归入此桶）
NULL_BUCKET = "(未分类)"

#: 本地 catalog 里出现过、但 config.PLATFORM_CATEGORIES 未列的类别。
#: 实测 SOCIALMEDIA(23 集) / BROKER(1 集) 不在 17 类里——**遍历必须显式带上**，
#: 否则这批集永远扫不到。UNKNOWN 里其余名字按「未知但真实存在」处理，一并遍历。
KNOWN_EXTRA_CATEGORIES = ("SOCIALMEDIA", "BROKER")

#: 表达式 token → 字段的停用表（保守集合，抄自 field_signal_mine 的 _STOPWORDS 思路）。
#: 用于从历史回测表达式里回抽字段名。**保守宁多勿漏**：抽错的字段只是多一个候选。
_STOPWORDS = {
    "abs", "add", "subtract", "multiply", "divide", "sign", "log", "power", "sqrt",
    "rank", "zscore", "quantile", "scale", "normalize", "winsorize", "vector_neut",
    "group_neutralize", "group_rank", "group_zscore", "group_backfill", "group_mean",
    "group_scale", "group_count", "group_sum", "bucket", "vector_avg", "vector_sum",
    "vec_avg", "vec_sum", "trade_when", "days_from_last_change", "ts_rank", "ts_zscore",
    "ts_mean", "ts_sum", "ts_std_dev", "ts_delta", "ts_delay", "ts_decay_linear",
    "ts_ir", "ts_quantile", "ts_max", "ts_min", "ts_corr", "ts_regression",
    "ts_entropy", "ts_argmax", "ts_argmin", "regression_neut", "hump", "signed_power",
    "reverse", "indneutralize", "to_nan", "replace", "is_nan", "not",
    "true", "false", "on", "off", "nan", "inf",
    "sector", "industry", "subindustry", "country", "market", "exchange",
    "stvi", "currency", "asset", "returns", "volume", "close", "open", "high", "low",
}

#: 表达式里的 token 候选（标识符形态）
_TOKEN_RE = re.compile(r"[A-Za-z_][A-Za-z0-9_]*")


def _norm_cat(raw: Optional[str]) -> str:
    """category 归一：None/空/未知值 → NULL_BUCKET；否则大写去空白。"""
    s = (raw or "").strip().upper()
    return s or NULL_BUCKET


def extract_fields(expression: str) -> List[str]:
    """从表达式文本回抽候选字段名（去停用词、去重、保序）。"""
    out: List[str] = []
    seen = set()
    for tok in _TOKEN_RE.findall(expression or ""):
        low = tok.lower()
        if low in _STOPWORDS or tok in seen:
            continue
        # 纯数字/单字母（分组变量常用单字母）不视为字段
        if len(tok) < 3:
            continue
        seen.add(tok)
        out.append(tok)
    return out


def load_categories(conn, region: str) -> List[str]:
    """列出该region 在本地 catalog 里出现的**全部** category 桶（含 NULL 兜底桶）。

    ⚠ 不按 ``config.PLATFORM_CATEGORIES`` 裁剪——那17 类是「平台已知口径」，
    本地快照可能多出新类（socialmedia/broker）或漏掉。遍历要的是**本地真实全集**，
    再由调用方与平台对齐。
    """
    rows = conn.execute(
        "SELECT DISTINCT d.category FROM datasets d JOIN regions r ON r.id=d.region_id "
        "WHERE r.name=?",
        (region.upper(),),
    ).fetchall()
    return sorted({_norm_cat(r[0]) for r in rows})


def load_field_stats(conn, region: str) -> Dict[str, Dict[str, Any]]:
    """按字段名聚合该region 的字段画像（跨集同名字段合并，取覆盖/拥挤的保守值）。

    返回 ``{field_name: {...}}``；同一字段出现在多集时：
    - ``dataset_ids`` 累积（探针要按数据集派发，不能丢归属）
    - ``coverage`` 取 **最小值**（保守：低覆盖字段最可能挂 CW）
    - ``alpha_count`` 取 **最大值**（保守：最拥挤的那个集代表 prod 墙风险）
    """
    sql = """
      SELECT f.field_name, f.field_type, f.coverage, f.alpha_count, f.user_count,
             f.description, d.name AS ds_name, d.id AS ds_id, d.category
      FROM fields f
      JOIN datasets d ON d.id = f.dataset_id
      JOIN regions r ON r.id = d.region_id
      WHERE r.name=? AND f.field_name IS NOT NULL AND TRIM(f.field_name)<>''
    """
    out: Dict[str, Dict[str, Any]] = {}
    for (fname, ftype, cov, ac, uc, desc, ds_name, ds_id, cat) in conn.execute(sql, (region.upper(),)):
        cov = float(cov) if cov is not None else 0.0
        ac = int(ac or 0)
        uc = int(uc or 0)
        rec = out.get(fname)
        if rec is None:
            out[fname] = {
                "field_name": fname,
                "field_type": ftype or "UNKNOWN",
                "coverage": cov,
                "alpha_count": ac,
                "user_count": uc,
                "description": (desc or "").strip(),
                "dataset_ids": [ds_id],
                "datasets": [ds_name],
                "categories": {_norm_cat(cat)},
            }
            continue
        rec["coverage"] = min(rec["coverage"], cov)
        rec["alpha_count"] = max(rec["alpha_count"], ac)
        rec["user_count"] = max(rec["user_count"], uc)
        if ds_id not in rec["dataset_ids"]:
            rec["dataset_ids"].append(ds_id)
            rec["datasets"].append(ds_name)
            rec["categories"].add(_norm_cat(cat))
        if not rec["description"] and desc:
            rec["description"] = desc.strip()
        # 类型冲突（同名既 MATRIX 又 VECTOR）→ 标UNKNOWN，交探针阶段人工裁决
        if rec["field_type"] != (ftype or "UNKNOWN"):
            rec["field_type"] = "CONFLICT"
    return out


def load_field_signal(conn, region: str, min_abs: float) -> Dict[str, Dict[str, Any]]:
    """字段级历史信号先验（零回测，从 ``backtest_results`` 表达式文本反挖）。

    口径：``sharpe >= min_abs`` 记为强信号，``|sharpe| >= min_abs`` 记为强信号（含反向）。
    返回 ``{field_name: {n, n_hit, max_abs, best_fitness, datasets, sample}}``。
    """
    sql = """
      SELECT b.expression_text, b.sharpe, b.fitness, b.dataset, b.region
      FROM backtest_results b
      WHERE b.region=? AND b.sharpe IS NOT NULL
    """
    # 不同部署列名可能不同（expression / expression_text / payload），容错取第一个可用
    cols = {r[1] for r in conn.execute("PRAGMA table_info(backtest_results)")}
    expr_col = next((c for c in ("expression_text", "expression", "code") if c in cols), None)
    if expr_col is None:
        return {}
    sql = sql.replace("expression_text", expr_col)

    out: Dict[str, Dict[str, Any]] = {}
    for expr, sharpe, fitness, ds, _rg in conn.execute(sql, (region.upper(),)):
        s = float(sharpe)
        if abs(s) < min_abs:
            continue
        for f in extract_fields(str(expr or "")):
            rec = out.setdefault(f, {"n": 0, "n_hit": 0, "max_abs": 0.0,
                                    "best_fitness": None, "datasets": set(), "sample": None})
            rec["n"] += 1
            rec["n_hit"] += 1
            if abs(s) > rec["max_abs"]:
                rec["max_abs"] = abs(s)
                rec["sample"] = str(expr or "")[:200]
            if fitness is not None:
                fb = float(fitness)
                rec["best_fitness"] = fb if rec["best_fitness"] is None else max(rec["best_fitness"], fb)
            if ds:
                rec["datasets"].add(ds)
    for rec in out.values():
        rec["datasets"] = sorted(rec["datasets"])
    return out


def load_category_yield(conn, region: str) -> Dict[str, Dict[str, Any]]:
    """category 级历史产出（严格口径：``sharpe>=1.58`` 且 RA 全清）。"""
    sql = """
      SELECT COALESCE(d.category,'(未分类)') cat, COUNT(*) n, MAX(b.sharpe) mx,
             COUNT(DISTINCT b.dataset) nd
      FROM backtest_results b
      JOIN datasets d ON d.name=b.dataset
      JOIN regions r ON r.id=d.region_id AND r.name=b.region
      WHERE b.region=? AND b.sharpe>=1.58
        AND COALESCE(TRIM(b.ra_failed_checks),'') IN ('','[]')
      GROUP BY 1
    """
    out = {}
    for cat, n, mx, nd in conn.execute(sql, (region.upper(),)):
        out[_norm_cat(cat)] = {"clean_hits": int(n or 0), "max_sharpe": float(mx or 0.0),
                               "datasets": int(nd or 0)}
    return out


def load_registry_dead(conn, region: str,
                       known_datasets: Optional[set] = None) -> Dict[str, Dict[str, Any]]:
    """读 ``registry_empirical`` 的 ``dead_end`` 层 → ``{数据集名: {dead_id, family, rule, reason}}``。

    ★ 这是 L2 闭环的**关键缺口修补**（2026-10-06 实测）：本工具初版完全不读 registry，
    导致已判死的数据集仍被推为可探候选——实测 DEU/KOR 共 **11 个**已死集被重推，
    其中 ``DEU sentiment7`` 的 dead_end 写明「6 波 48 探针 / 天花板 0.71」
    仍被 L0 标成 ``★苗头``。

    **两路提取**（缺一不可，实测各覆盖一半）：
      ① **结构化键**（``dataset`` / ``datasets`` / ``sets`` / ``datasets_dead_today`` /
         ``r105_legacy_dead``）—— 显式列名的批次，命中率高但只覆盖部分条目。
      ② **全值子串匹配**（拿本区已知数据集名去payload 全文 + ``family`` +
         ``entry_id`` 里找）—— 覆盖 ``DEU pattern_scores`` 这类**只写在 family 文本里**
         的条目（实测其 payload 键只有 id/family/reason/rule/...，
         ``family="pattern_scores 图表形态相似度"``，结构化键一个都没有）。

    ``known_datasets`` 传入本区数据集名集合后启用第②路；未传则只走第①路
    （避免误把 ``family`` 里的任意词当数据集名）。
    """
    out: Dict[str, Dict[str, Any]] = {}
    try:
        rows = conn.execute(
            "SELECT entry_id, family, payload FROM registry_empirical "
            "WHERE region=? AND layer='dead_end'",
            (region.upper(),),
        ).fetchall()
    except Exception:
        return out

    ds_keys = ("dataset", "datasets", "sets", "datasets_dead_today",
               "r105_legacy_dead", "legacy_dead")
    known = {str(x) for x in (known_datasets or set())}

    def _collect(p: Dict[str, Any]):
        found = set()
        for k in ds_keys:
            v = p.get(k)
            if isinstance(v, str):
                found.add(v)
            elif isinstance(v, list):
                found.update(str(x) for x in v)
            elif isinstance(v, dict):
                found.update(str(x) for x in v.keys())
        return found

    for entry_id, family, payload in rows:
        try:
            p = json.loads(payload or "{}")
        except Exception:
            p = {}
        if not isinstance(p, dict):
            p = {}
        names = _collect(p)
        # ② 全值子串匹配：把已知数据集名在 payload 的**值** + family + entry_id 里找。
        #    ⚠️ **跳过说明性键**——实测 ``DEU-EMPTY-COVERAGE-S0-PICKS-20260919`` 的
        #    ``control_group`` 里写着「shortinterest3 字段级 coverage 0.63-0.98（对照组）」，
        #    扫payload 全文会把**对照组**误判成死集（它实际列的是 option1/pv20/fundamental17）。
        _SKIP_TEXT_KEYS = (
            "control_group", "method", "risk", "note", "reason", "rule",
            "reuse_rule", "evidence", "summary", "reusability", "salvage",
            "exhausted_channels", "probed_fields", "concepts_probed",
            "cross_region_prior", "best_assets", "best_atom", "best_alpha",
            "best_expr", "best_metrics", "probed", "profile", "gate", "finding",
            "action", "wall", "assets", "probes", "cw_killer", "fast_kill",
            "id", "entry_id", "family", "source", "wave", "wave_ref", "region",
        )
        if known:
            parts = [str(family or ""), str(entry_id or "")]
            for k, v in p.items():
                if k in _SKIP_TEXT_KEYS:
                    continue
                parts.append(v if isinstance(v, str) else json.dumps(v, ensure_ascii=False))
            hay = " ".join(parts)
            for ds in known:
                if ds and ds in hay:
                    names.add(ds)

        if not names:
            continue
        for ds in names:
            # 同一数据集多条死路时，保留信息量最大的一条（含 rule 的优先）
            prev = out.get(ds)
            cand = {
                "dead_id": entry_id,
                "family": family or p.get("family"),
                "rule": p.get("rule") or p.get("reuse_rule") or "",
                "reason": (p.get("reason") or p.get("summary") or "")[:200],
            }
            if prev is None or (cand["rule"] and not prev["rule"]):
                out[ds] = cand
    return out


def load_family_risk(conn, region: str, sim_threshold: float) -> Dict[str, str]:
    """族级连坐**提示**（铁律 ③：只提示不判死）。

    复用 ``category_field_triage`` 的签名思想但独立实现（避免耦合它的判级）：
    以「数据集名+字段 description 关键词签名」的Jaccard 相似度找出同族。
    为控制开销与复杂度，这里退化为**字段名前缀签名**（``_family_signature`` 的轻量版）：
    取字段名``_<前缀>_`` 段做签名，同前缀即同族。
    """
    rows = conn.execute(
        r"""
        SELECT DISTINCT substr(f.field_name, 1,
                 CASE WHEN instr(substr(f.field_name,2),'_')>0
                      THEN instr(substr(f.field_name,2),'_') ELSE 4 END) sig,
               d.name
        FROM fields f JOIN datasets d ON d.id=f.dataset_id
        JOIN regions r ON r.id=d.region_id
        WHERE r.name=? AND instr(f.field_name,'_')>0
        """,
        (region.upper(),),
    ).fetchall()
    sig2ds: Dict[str, set] = {}
    for sig, ds in rows:
        if not sig:
            continue
        sig2ds.setdefault(sig.lower(), set()).add(ds)
    risk: Dict[str, str] = {}
    for sig, dss in sig2ds.items():
        if len(dss) >= 2:                     # 同前缀跨集 → 疑似同族（模型版本差异）
            for ds in dss:
                risk[ds] = f"前缀族:{sig}(跨{len(dss)}集)"
    return risk


def pick_seed_fields(
    fields: Dict[str, Dict[str, Any]],
    signals: Dict[str, Dict[str, Any]],
    fam_risk: Dict[str, str],
    top: int,
    min_coverage: float,
    crowd_ac: int,
    min_fields: int,
    dead: Optional[Dict[str, Dict[str, Any]]] = None,
    skip_dead: bool = True,
) -> List[Dict[str, Any]]:
    """从一类里挑「苗头候选字段」。

    排序键（**不把 alpha_count 当入选条件**，只用它做拥挤排除）：
      1. **registry 已判死的数据集排末位**（``skip_dead=True`` 时剔除「有 rule 的」，
         见下方★）
      2. 有历史强信号（``n_hit>0``）优先——这是唯一被实测验证过的信号来源
      3. 历史 ``max_abs`` 大者优先
      4. 覆盖率达标（>= ``--min-coverage``）
      5. ``alpha_count`` 小者优先（避 prod 墙，但仅作**排除**闸 ``> crowd_ac``）

    族连坐命中的字段**不剔除**，只排到末位（铁律 ③）。

    ★ **只有带``rule`` 的 dead_end 才做强排除**。registry 契约要求 dead_end 带
    ``rule``（「下次怎么办」），实测``DEU-SI3-CW-STRUCTURAL``（``shortinterest3``
    CW 墙）的 rule **是空的**——它记录了现象但没给行动指引。
    若把这类也当硬排除，会把 DEU 产出最好的集之一（``shortinterest3`` 有 25 条
    RA-clean、25/25 全区最高）直接判成「已枯(registry)」。
    ⇒无 ``rule`` 的条目**降级为提示**（排末位 + 打 ``dead_weak`` 标签），不剔除。
    """
    dead = dead or {}
    pool = []
    n_dead_skip = 0
    for f in fields:
        fname = f["field_name"]
        if f["coverage"] < min_coverage:
            continue
        # registry 死路命中：按字段归属的第一个数据集判定
        ds0 = f["datasets"][0] if f["datasets"] else None
        dead_hit = dead.get(ds0) if ds0 else None
        # ★ 只有带 rule 的才硬排除；无 rule 的降级为提示
        if dead_hit and skip_dead and dead_hit.get("rule"):
            n_dead_skip += 1
            continue
        crowded = f["alpha_count"] > crowd_ac
        sig = signals.get(fname)
        pool.append({
            "field": fname,
            "field_type": f["field_type"],
            "coverage": f["coverage"],
            "alpha_count": f["alpha_count"],
            "user_count": f["user_count"],
            "datasets": f["datasets"],
            "categories": sorted(f["categories"]),
            "hist_hit": int(sig["n_hit"]) if sig else 0,
            "hist_max_abs": round(float(sig["max_abs"]), 3) if sig else 0.0,
            "hist_sample": sig["sample"] if sig else None,
            "family_risk": fam_risk.get(ds0) if ds0 else None,
            "dead_end": ({"dead_id": dead_hit["dead_id"],
                          "family": dead_hit["family"],
                          "weak": not bool(dead_hit.get("rule"))} if dead_hit else None),
            "crowded": crowded,
            "description": f["description"][:160],
        })
    # registry 死路排最末 → 其次族连坐 → 拥挤；都不剔除（除上面已剔的）
    pool.sort(key=lambda x: (
        bool(x["dead_end"]),                # False 先（含 weak，弱死路也排末位但不剔）
        bool(x["family_risk"]),             # False 先
        x["crowded"],# False 先
        -x["hist_hit"],
        -x["hist_max_abs"],
        x["alpha_count"],
    ))
    pick_seed_fields.last_skipped_dead = n_dead_skip        # type: ignore[attr-defined]
    return pool[:top]


def allocate_quota(rows: List[Dict[str, Any]], total_probe: int,
                    mode: str = "yield") -> Dict[str, int]:
    """★ L2 深挖配额分配：**按各类历史产出率分配，不均分**。

    实测依据（全库 13 区 754 波）：各类产出率相差 25 倍（MEA 19.9% vs ASI 1.6%），
    均分会把配额压在无产出的类上。

    两种mode：
      - ``yield``（默认）：权重 = 历史达标数 + ``prior``，按权重比例分配。
        历史 0 产出的「待探」类给``prior`` 保底（默认 1）——否则处女地永远拿不到探针。
      - ``equal``：均分（仅作对照，便于量化 yield 模式的价值）。

    返回 ``{category: 探针条数}``，总和不超 ``total_probe``。
    """
    hot = [r for r in rows if r["verdict"] in ("★苗头", "待探")]
    if not hot:
        return {}
    if mode == "equal":
        base = max(1, total_probe // len(hot))
        return {r["category"]: base for r in hot}

    # 权重：历史达标数（0 产的给保底权重 1）+ 「有历史强信号字段」加成
    weights = {}
    for r in hot:
        w = float(r["clean_hits"]) + (1.0 if r["clean_hits"] == 0 else 0.0)
        if r["n_hist_hit_fields"] > 0:
            w += 0.5            # 有历史强信号字段的类略加权（实测唯一被验证的先验）
        weights[r["category"]] = max(w, 0.5)
    tot_w = sum(weights.values())
    out: Dict[str, int] = {}
    for r in hot:
        raw = total_probe * weights[r["category"]] / tot_w
        out[r["category"]] = max(1, int(raw))    # 每类至少 1 条（否则处女地永远没机会）
    # 总量校正：从权重最大的类削超额，保证不超预算
    while sum(out.values()) > total_probe:
        big = max(out, key=lambda k: out[k])
        if out[big] <= 1:
            break
        out[big] -= 1
    return out


def sweep(conn, region: str, args) -> Dict[str, Any]:
    categories = load_categories(conn, region)
    fields = load_field_stats(conn, region)
    signals = load_field_signal(conn, region, args.min_signal)
    yields = load_category_yield(conn, region)
    fam_risk = load_family_risk(conn, region, args.family_sim)
    dead = load_registry_dead(
        conn, region, known_datasets={d for f in fields.values() for d in f["datasets"]})

    # 字段 → category 反查（字段可能跨类，取首个；探针派发按 dataset_ids 而非 category）
    buckets: Dict[str, List[Dict[str, Any]]] = {c: [] for c in categories}
    for f in fields.values():
        for c in f["categories"]:
            buckets.setdefault(c, []).append(f)

    rows: List[Dict[str, Any]] = []
    for cat in sorted(buckets):
        fs = buckets[cat]
        seeds = pick_seed_fields(
            fs, signals, fam_risk, args.top,
            args.min_coverage, args.crowd_ac, args.min_fields,
            dead=dead, skip_dead=not args.keep_dead,
        )
        n_dead_skipped = int(getattr(pick_seed_fields, "last_skipped_dead", 0))
        n_field = len(fs)
        desert = sum(1 for f in fs if f["alpha_count"] == 0 and f["user_count"] == 0)
        desert_ratio = (desert / n_field) if n_field else 0.0
        y = yields.get(cat, {"clean_hits": 0, "max_sharpe": 0.0, "datasets": 0})
        hist_hit = sum(1 for s in seeds if s["hist_hit"] > 0)
        # 本类还剩几个**未被 registry 强排除**的数据集（判「已枯(registry)」的依据）。
        # ★ 只算「带 rule 的」死路——无 rule 的只降级为提示（见 pick_seed_fields 的★）。
        all_ds = {d for f in fs for d in f["datasets"]}
        dead_strong = {d for d in (all_ds & set(dead)) if (dead.get(d) or {}).get("rule")}
        live_ds = all_ds - dead_strong
        # ⚠ 桶内0 字段但有历史达标 ⇒ 该桶是**本地登记的组合/合成集**（如 ``mix_2leg``、
        #   ``grtransform``、``lean_le89``、``_unknown``），字段本身归属别的具名类。
        #   实测 DEU NULL 桶6 集全属此类、合计 19 条达标——既不是「贫瘠机会」也不是
        #   「平台类别」，判``已枯(归他类)`，避免它占一个探针位。
        synthetic = (n_field == 0 and y["clean_hits"] > 0)
        if synthetic:
            verdict = "已枯(归他类)"
        elif n_field < args.min_fields:
            verdict = "贫瘠"
        elif not live_ds:
            verdict = "已枯(registry)"      # ★ 本类数据集全部已在 registry 判死
        elif y["clean_hits"] > 0 and seeds:
            verdict = "★苗头"
        elif seeds:
            verdict = "待探"
        else:
            verdict = "已枯"
        rows.append({
            "category": cat,
            "n_datasets": len({d for f in fs for d in f["datasets"]}),
            "n_live_datasets": len(live_ds),
            "n_dead_datasets": len(dead_strong),
            "n_fields": n_field,
            "n_seed_fields": len(seeds),
            "n_dead_fields_skipped": n_dead_skipped,
            "n_hist_hit_fields": hist_hit,
            "desert_ratio": round(desert_ratio, 3),
            "clean_hits": y["clean_hits"],
            "max_sharpe": round(y["max_sharpe"], 3),
            "verdict": verdict,
            "synthetic_only": synthetic,
            "seeds": seeds,
        })

    # 排序：★苗头 → 待探 → 贫瘠 → 已枯 → 已枯(registry/归他类)；同类按历史产出与种子数
    order = {"★苗头": 0, "待探": 1, "贫瘠": 2, "已枯": 3,
             "已枯(registry)": 4, "已枯(归他类)": 5}
    rows.sort(key=lambda r: (order.get(r["verdict"], 9), -r["clean_hits"], -r["n_seed_fields"]))

    covered = sum(r["n_datasets"] for r in rows)
    quota = allocate_quota(rows, args.probe_budget, args.quota_mode)
    return {
        "region": region.upper(),
        "generated_by": "tools/probe/category_sweep.py",
        "params": {
            "min_coverage": args.min_coverage, "crowd_ac": args.crowd_ac,
            "min_fields": args.min_fields, "top": args.top,
            "min_signal": args.min_signal, "family_sim": args.family_sim,
            "keep_dead": args.keep_dead, "probe_budget": args.probe_budget,
            "quota_mode": args.quota_mode,
        },
        "coverage": {
            "n_categories": len(rows),
            "n_null_bucket": sum(1 for r in rows if r["category"] == NULL_BUCKET),
            "n_datasets": covered,
            "n_fields": sum(r["n_fields"] for r in rows),
            "n_seed_fields": sum(r["n_seed_fields"] for r in rows),
        },
        "dead_registry": {
            "n_dead_datasets": len({d for d, v in dead.items() if v.get("rule")}),
            "n_weak_dead": len({d for d, v in dead.items() if not v.get("rule")}),
            "n_fields_skipped": sum(r["n_dead_fields_skipped"] for r in rows),
            "datasets": sorted(dead),
        },
        "quota": quota,
        "categories": rows,
    }


def print_report(result: Dict[str, Any]) -> None:
    p, cv = result["params"], result["coverage"]
    print(f"=== category_sweep · region={result['region']} ===")
    print(f"口径: cov>={p['min_coverage']} crowd_ac={p['crowd_ac']} min_fields={p['min_fields']} "
          f"top/cat={p['top']} min|S|={p['min_signal']}")
    print(f"覆盖: {cv['n_categories']} 类（含未分类桶 {cv['n_null_bucket']} 个）/ "
          f"{cv['n_datasets']} 集 / {cv['n_fields']} 字段 → 种子 {cv['n_seed_fields']} 个")
    print()
    hdr = (f"  {'category':<16}{'集':>4}{'活':>4}{'字段':>7}{'种子':>5}{'荒地':>7}"
           f"{'达标':>5}{'maxS':>7}{'配额':>5}  判定")
    print(hdr)
    print("  " + "-" * (len(hdr) + 6))
    quota = result.get("quota") or {}
    for r in result["categories"]:
        print(f"  {r['category']:<16}{r['n_datasets']:>4}{r.get('n_live_datasets', 0):>4}"
              f"{r['n_fields']:>7}"
              f"{r['n_seed_fields']:>5}{r['desert_ratio']*100:>6.0f}%"
              f"{r['clean_hits']:>5}{r['max_sharpe']:>7.2f}"
              f"{quota.get(r['category'], 0):>5}  {r['verdict']}")
    print()
    hot = [r for r in result["categories"] if r["verdict"] in ("★苗头", "待探")]
    synth = [r for r in result["categories"] if r.get("synthetic_only")]
    deadr = [r for r in result["categories"] if r["verdict"] == "已枯(registry)"]
    print(f"  可探类别 {len(hot)}/{len(result['categories'])}: "
          + ", ".join(f"{r['category']}({r['n_seed_fields']})" for r in hot[:12]))
    if quota:
        print(f"  深挖配额（{result['params'].get('quota_mode')} 分配，"
              f"总预算 {result['params'].get('probe_budget')}）: "
              + ", ".join(f"{k}={v}" for k, v in sorted(quota.items(), key=lambda kv: -kv[1])[:12]))
    dr = result.get("dead_registry") or {}
    if dr.get("n_dead_datasets"):
        print(f"  [registry 闭环] 本区强排除（带 rule）{dr['n_dead_datasets']} 个数据集 → "
              f"已从种子池剔除 {dr.get('n_fields_skipped', 0)} 个字段；"
              f"另 {dr.get('n_weak_dead', 0)} 个无 rule 死路仅降级为提示"
              + ("（--keep-dead：全部保留复查）" if result['params'].get('keep_dead') else ""))
    if deadr:
        print(f"  [已枯registry] {len(deadr)} 个类因全部数据集已判死而不探: "
              + ", ".join(r["category"] for r in deadr[:8]))
    if synth:
        print(f"  [已归他类] {len(synth)} 个组合集桶（字段归属别的类，不占探针位）: "
              + ", ".join(r["category"] for r in synth[:8]))
    print("  ⚠ 荒地率仅供判读（高荒地不必剔除：DEU other455 荒地90% 却出 14 条达标）")


def main() -> int:
    ap = argparse.ArgumentParser(
        description="L0 类别普查：region × 全 category × 字段池（零回测零 API）")
    ap.add_argument("--region", required=True)
    ap.add_argument("--min-coverage", type=float, default=0.30,
                    help="字段覆盖下限（默认 0.30；低于此值的字段多为废地）")
    ap.add_argument("--crowd-ac", type=int, default=1000,
                    help="拥挤排除闸：alpha_count 超过此值不删但排末位（默认 1000）")
    ap.add_argument("--min-fields", type=int, default=5,
                    help="候选字段数下限，低于此判「贫瘠」（默认 5）")
    ap.add_argument("--top", type=int, default=8, help="每类取几个种子字段（默认 8）")
    ap.add_argument("--min-signal", type=float, default=1.58,
                    help="历史强信号判定下限 |sharpe|（默认 1.58，与提交线同口径）")
    ap.add_argument("--family-sim", type=float, default=0.70,
                    help="族连坐提示阈值（仅影响排序，不剔除）")
    ap.add_argument("--keep-dead", action="store_true",
                    help="保留 registry 已判死的数据集（默认剔除；复查时用）")
    ap.add_argument("--probe-budget", type=int, default=64,
                    help="L1/L2 探针总预算（条），按产出率分配到各类（默认 64）")
    ap.add_argument("--quota-mode", default="yield", choices=("yield", "equal"),
                    help="配额分配模式：yield=按历史产出率（默认）；equal=均分（对照）")
    ap.add_argument("--dead-detail", action="store_true",
                    help="打印 registry 已判死数据集明细")
    ap.add_argument("--seed-fields", action="store_true",
                    help="同时输出扁平化种子字段清单（供 L1 探针消费）")
    ap.add_argument("--json", dest="json_out", help="完整结果写此JSON")
    args = ap.parse_args()

    conn = db_connect(DB, readonly=True)
    try:
        result = sweep(conn, args.region, args)
    finally:
        conn.close()

    print_report(result)
    if args.dead_detail:
        dr = result.get("dead_registry") or {}
        print(f"\n  registry 已判死数据集明细（{dr.get('n_dead_datasets', 0)} 个）:")
        for name in dr.get("datasets", [])[:60]:
            print(f"    - {name}")
    if args.seed_fields:
        seeds = []
        for r in result["categories"]:
            if r["verdict"] not in ("★苗头", "待探"):
                continue          # 只导出可探类别，贫瘠/已枯/归他类不占L1 探针位
            for s in r["seeds"]:
                seeds.append({"category": r["category"], "verdict": r["verdict"], **s})
        result["seed_fields_flat"] = seeds
        print(f"\n  种子字段合计 {len(seeds)} 个（仅可探类别，--seed-fields）")
    if args.json_out:
        with open(args.json_out, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=1)
        print(f"  [json] {args.json_out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())