# -*- coding: utf-8 -*-
"""字段选择：语义分类 / 幽灵字段过滤 / 维度取代表 / full+probe 分层。"""
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

from .config import *            # noqa: F401,F403
from .config import _WQB_SCRIPTS_DIR  # noqa: F401

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from campaign_semantics import (  # noqa: E402,F401
    LIT_THRESHOLD, VIRGIN_AC, VIRGIN_VS, VIRGIN_MIN_COV, VIRGIN_COV_FLOOR,
    is_virgin, all_datasets, exposure_profile,
    NAME_META, is_name_metadata, classify_desc,
    FORM_FAMILIES, GATED_CATS, GATE_Q, POSTPROC_Q, PER_DIM, MIN_FIELDS_TOTAL,
    FULL_FIELD_CAP, BLACKBOX_FAMILIES, field_tier,
    FAMILY_EXPOSURE, EXPOSURE_VOCAB, EXPR_EXPOSURE, field_exposure_hint,
    CONCEPT_FAMILIES, CONCEPT_ZH, field_concepts, concept_families,
    PP_VOCAB, parse_preprocessing, load_s1_preprocessing, apply_preprocessing,
    _DESC_NOISE, clean_desc, _load_form_overrides, _load_llm_tags, LLM_CONF_MIN,
    FORM_EVIDENCE, field_form, print_form_audit,
)
from .generate import (build_one_family, PROBE_FIELD_CAP, FAMILIES,
                       RESIDUAL_TPL, RESIDUAL_DECAY,
                       ROBUST_TPL, ROBUST_DECAY, robust_decay)

# 车道级字段上限覆写：WQB_CAMPAIGN_FULL_CAP=12 ⇒ 本进程每集多测 50% 字段。
# 动机（2026-10-25）：FULL_FIELD_CAP=8 让 risk70 的 87 个字段只测了 8 个（9%），
# 而「一个集只出 1 席」的瓶颈常常就是字段覆盖太窄。仅影响本进程，不干扰其它车道。
try:
    _cap_env = int(os.environ.get("WQB_CAMPAIGN_FULL_CAP", "0"))
except ValueError:
    _cap_env = 0
if _cap_env > 0:
    FULL_FIELD_CAP = _cap_env
    print(f"[lane] 字段上限覆写 FULL_FIELD_CAP={FULL_FIELD_CAP}")
from .persist import save_ckpt, save_results
from .transport import dispatch


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
            instrument_type="EQUITY", region=REGION, delay=1,
            # 2026-10-25：此前写死 universe="TOPCS1600"（EUR 档）⇒ IND 下平台查不到字段，
            # 整集被误判「幽灵字段」（本地 N → 平台认证 0），6 个集全部 SKIPPED_TOO_FEW_FIELDS。
            # 必须取区域配置里的合法 universe（IND=TOP500）。
            universe=REGION_SETTINGS["universe"], dataset_id=ds)
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


def _query_fields(con, ds, min_cov=None, names=None):
    """取本集字段行。

    ``min_cov=None`` ⇒ **不过覆盖率闸**（`--keep-fields` 定向复挖用）。
    ``names`` 限定字段名（小写比对，SQLite 的 LOWER 只处理 ASCII，字段名都是 ASCII）。
    """
    q = f"""SELECT f.field_name, f.field_type, f.coverage, st.sem_type,
                   COALESCE(f.description,'') AS descr
           FROM fields f JOIN datasets d ON f.dataset_id=d.id JOIN regions r ON d.region_id=r.id
           LEFT JOIN field_semantic_type st ON st.region='{REGION}' AND st.dataset=d.name AND st.field=f.field_name
           WHERE r.name='{REGION}' AND d.name=? AND f.field_type != 'GROUP'"""
    params = [ds]
    if min_cov is not None:
        q += " AND f.coverage>=?"
        params.append(min_cov)
    if names:
        _nl = sorted({n.lower() for n in names})
        q += f" AND LOWER(f.field_name) IN ({','.join('?' * len(_nl))})"
        params += _nl
    cur = con.execute(q, params)
    cols = [c[0] for c in cur.description]
    return [dict(zip(cols, row)) for row in cur.fetchall()]


def select_fields(con, ds, field_min_cov=0.5, only_names=None, keep_fields=None):
    rows = _query_fields(con, ds, min_cov=field_min_cov)
    keep = {x.strip().lower() for x in (keep_fields or []) if x and x.strip()}
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
    # ★ 2026-10-26：`--keep-fields` 强制纳入——用户点名的字段不受覆盖率闸 / 元数据丢弃影响。
    # 动机：定向复挖 ATOM 时点名 6 个 analyst_consensus 字段，实测只有 2 个过覆盖率闸，
    # 其余被降级成单条 lvl_rk 探针 ⇒ robust 几何族只跑在 2 个字段上，
    # 「新结构到底能不能破 robust 墙」的结论会被字段覆盖不足污染。
    if keep:
        _have = {r["field_name"].lower() for r in rows}
        _miss = sorted(keep - _have)
        if _miss:
            _got = _query_fields(con, ds, names=_miss)
            for r in _got:
                st0 = (r.get("sem_type") or "").lower()
                if st0 in ("", "unknown", "none", "metadata"):
                    r["sem_type"] = classify_desc(r.get("descr"), r["field_name"])
                if (r.get("sem_type") or "").lower() in ("", "unknown", "none", "metadata"):
                    r["sem_type"] = "value"   # 用户点名 ⇒ 即便像元数据也照跑
                r["_forced"] = True
            rows += _got
            _found = {r["field_name"].lower() for r in _got}
            _nowhere = [n for n in _miss if n not in _found]
            print(f"  [keep] {ds}: 强制纳入 {len(_got)} 个未过覆盖率闸/元数据闸的字段"
                  + (f"；本地库无此字段 {_nowhere}" if _nowhere else ""))
    plat = platform_fields(ds)
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
    # 定向复挖时 keep 是「必须跑到」的字段集：上限不少于它的规模，排序也让它优先。
    _cap_eff = max(FULL_FIELD_CAP, len(keep))

    def _prio(rs):
        """keep 字段优先（False < True），同档按覆盖率降序。"""
        return sorted(rs, key=lambda r: (r["field_name"].lower() not in keep,
                                        -(r["coverage"] or 0)))

    def _budget_trim(rs, cap):
        """裁到 cap：① keep 点名全留 → ② 语义维各 1 → ③ 覆盖率补满。

        ⚠ 2026-10-26：旧顺序是「每维各 1 → 覆盖率补满」，而 keep 字段常同属一个语义维
        （analyst_consensus 的 6 个点名件都是 eps_estimate）⇒ 维代表先占位，6 个 keep 只进来 4 个，
        另外 2 个被挤掉，定向复挖又一次只跑在部分字段上。用户点名的优先级必须高于维度多样性。
        """
        _by = _prio(rs)
        out, dims = [], set()
        for r in _by:
            if len(out) >= cap:
                return out
            if r["field_name"].lower() in keep:
                dims.add(r["dim"])
                out.append(r)
        for r in _by:
            if len(out) >= cap:
                return out
            if r not in out and r["dim"] not in dims:
                dims.add(r["dim"])
                out.append(r)
        for r in _by:
            if len(out) >= cap:
                break
            if r not in out:
                out.append(r)
        return out

    if only_names:
        # 续跑：沿用断点里记录的字段清单，保证同一数据集各模板族字段覆盖一致。
        # ⚠ 断点清单**不并进 keep**：它含 probe 字段（最多 20 个），并进去会把上限撑大、
        # 让 probe 全部升成 full ⇒ 续跑派发量暴涨。只有用户显式 --keep-fields 才扩大上限。
        _only = {x.lower() for x in only_names if x}
        _names = _only | keep
        rows = [r for r in rows if r["field_name"].lower() in _names]
        for r in rows:
            r["dim"] = r["sem_type"] or "unknown"
        # ⚠ 2026-10-23：续跑集也必须吃 A 方案的字段上限。
        # 旧实现在这里直接 return，导致已锁定字段的集（如 risk62 的 19 个字段）绕过 FULL_FIELD_CAP，
        # 仍然派发 134 条 → 把提速又抵消掉。
        if len(rows) > _cap_eff:
            _n0 = len(rows)
            rows = _budget_trim(rows, _cap_eff)
            print(f"  [budget] {ds}: 续跑集字段 {_n0} → {len(rows)}（上限 {_cap_eff}）")
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

    # ★ keep 字段无条件进精选集：PER_DIM 取样与同源去重都可能把它们裁掉。
    # 同源冲突时**用 keep 那个副本替换**（用户点名的才是要跑的），不是两边都留 ——
    # 同源两份会指向同一个 alpha_id，白烧一个槽位。
    if keep:
        _bmap = {re.sub(r"_\d+$", "", r["field_name"]).lower(): i
                 for i, r in enumerate(sel)}
        _add = _rep = 0
        for r in rows:
            if r["field_name"].lower() not in keep:
                continue
            r["dim"] = r.get("dim") or r["sem_type"] or "unknown"
            b = re.sub(r"_\d+$", "", r["field_name"]).lower()
            if b in _bmap:
                if sel[_bmap[b]]["field_name"].lower() not in keep:
                    sel[_bmap[b]] = r
                    _rep += 1
            else:
                _bmap[b] = len(sel)
                sel.append(r)
                _add += 1
        if _add or _rep:
            print(f"  [keep] {ds}: 指定字段进精选集 +{_add} 替换同源 {_rep}")

    # ★ 2026-10-23（用户指出「选字段缺口」）：**不再丢弃未入选字段**，改为 full / probe 两层。
    # 根因：旧逻辑按「语义维 × PER_DIM」硬裁（sentiment26 的 19 个字段只留 9 个，10 个静默消失），
    # 而唯一能出货的结构（pp）只跑在 top3 字段上 ⇒ 结构性缺口完全不可见。
    #   full  : 全 12 族（原精选集合）
    #   probe : 只跑 1 条最便宜探针（lvl_rk）；收割后由 carrier_expand() 把本集最强结构补跑一遍
    # A. 全族字段裁剪：每维先各留 1 个（保证维度多样性），再按覆盖率补满 FULL_FIELD_CAP
    if len(sel) > _cap_eff:
        _n0 = len(sel)
        sel = _budget_trim(sel, _cap_eff)
        print(f"  [budget] {ds}: 全族字段 {_n0} → {len(sel)}（上限 {_cap_eff}）")

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
        e = build_one_family(tpl, r, freq, ds=ds)
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

    # 设置必须跟着结构走：残差族实测 decay=126，robust 几何族实测**按结构分档**
    # （z/rank/dev 10 · 居中凸 6 · lvvol 2），robust 几何族每一档的实测证据不同；
    # 扩散时带错档跑出来的是未验证组合，还会把「结构有效」误判成「结构无效」。
    if tpl in ROBUST_TPL:
        _st = {"decay": robust_decay(tpl)}
    elif tpl in RESIDUAL_TPL:
        _st = {"decay": RESIDUAL_DECAY}
    else:
        _st = None
    sims = dispatch(exprs, ds, "cx", on_batch=_persist, settings=_st)
    ck["sims"][key] = sims
    save_ckpt(ck)
    return sims
