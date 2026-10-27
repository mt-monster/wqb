# -*- coding: utf-8 -*-
"""设置轴补扫：近闸集换 universe / neutralization 复测（缺陷1 回溯）。"""
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
from .fields import batch_field_coverage
from .transport import dispatch, harvest_until_done
from .audit import fetch_codes
from .generate import FAMILIES, RESIDUAL_TPL
from .persist import save_ckpt, save_results, beat
from .bad_tokens import note_bad_tokens
from .report import emit_digest


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
    all_tpl = [f"{a}_{b or 'pl'}" for a, b in FAMILIES] + ["dw", "pp"] + list(RESIDUAL_TPL)
    for ds in dss:
        v = (res.get("results") or {}).get(ds) or {}
        sel = None
        # 优先用 checkpoint 锁定的字段（与已跑结果同源）
        locked = (ck.get("fields") or {}).get(ds)
        if locked:
            sel = [{"field_name": f} for f in locked]
        cat = dict(con.execute(
            f"SELECT dataset, category FROM dataset_profile WHERE region='{REGION}'"))
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
        f"SELECT dataset, category FROM dataset_profile WHERE region='{REGION}'"))
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
