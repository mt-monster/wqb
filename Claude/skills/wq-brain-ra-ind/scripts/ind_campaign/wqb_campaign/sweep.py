# -*- coding: utf-8 -*-
"""设置轴补扫：近闸集换 decay / neutralization / nanHandling 复测（缺陷1 回溯）。

变体表按区域在 `config.SWEEP_VARIANTS`（IND 不含无效的 u2500，见 config 注释）。
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
from .transport import dispatch, harvest_until_done, row6
from .audit import fetch_codes
from .generate import (FAMILIES, RESIDUAL_TPL, ROBUST_TPL, robust_decay)
from .persist import save_ckpt, save_results, beat
from .bad_tokens import note_bad_tokens
from .report import emit_digest


# 非 ATOM 族：残差族吃 PV 的 returns（组腿），pp/tl 是后处理/门控形态（构造可能来自残差）。
# 近闸集扫设置时**先 ATOM**：非 ATOM 腿的复测命中率再高也不产出 ATOM 成品。
_NON_ATOM_TPL = set(RESIDUAL_TPL) | {"pp", "tl"}


def _is_atom_row(a):
    t = (a.get("tpl") or "")
    return t not in _NON_ATOM_TPL and not t.startswith("sw_")


def _base_decay(tpl):
    """候选项的「基座 decay」：robust 几何族按结构分档；其余走区域缺省（IND=4）。"""
    if tpl in ROBUST_TPL:
        return robust_decay(tpl)
    return int(str(REGION_SETTINGS.get("decay", "4")))


def _pick_pairs(cand):
    """ATOM 优先 + **同批必须同基座 decay**，返回 (top2, base_decay)。

    `dispatch` 一个调用只带一套 settings ⇒ 两条候选若基座 decay 不同，就只能拆成
    n=1 的两批，而单条批必为 `COMPLETE children=0`（2026-10-22 实测，结果永远收不到）。
    故先按基座 decay 分组，取「含最高 S 候选且有 ≥2 条」的那组；组内 ATOM 优先、S 降序。
    """
    ranked = sorted(cand, key=lambda a: (not _is_atom_row(a), -(a.get("s") or -9)))
    groups = collections.defaultdict(list)
    for a in ranked:
        groups[_base_decay(a.get("tpl"))].append(a)
    for dec, lst in sorted(groups.items(),
                           key=lambda kv: -max((x.get("s") or -9) for x in kv[1])):
        if len(lst) >= 2:
            return lst[:2], dec
    return [], None


def _variants_for(cat):
    """.SWEEP_VARIANTS + 事件/向量类的 nanHandling=ON（2 条/变体）。"""
    vs = list(SWEEP_VARIANTS)
    if (cat or "").upper() in NAN_ON_CATS and NAN_ON_VARIANT not in vs:
        vs.append(NAN_ON_VARIANT)
    return vs


def settings_sweep(ds, all_alphas, ck, res, max_s, cat=None):
    """1.2 ≤ max_S < 1.58 的「近闸」集，自动补跑设置变体。

    归因依据（2026-10-22/23/26 实测）：
      · **decay 是可扫维度**：凸族 rg_grdev_p3_sec decay6（58jPrvZ1 S1.64 全闸过）、
        lvvol 族 decay2（gJWnrZgg S2.14 全闸过），而主派发是 4；
      · neutralization=SUBINDUSTRY 把 sub 0.78→0.93、rob 0.55→1.13，几乎不损 S；
      · 论坛实测同内核换 CROWDING 可把 2Y 从 1.15 抬到 2.17；
      · nanHandling=ON 对 behavioral_signals 有 2.19 vs 0.46 的先例（只对事件/向量类）。
    ⚠ IND 的 universe 只有 TOP500 ⇒ 旧 u2500 变体是白烧（见 config 的变体表）。
    成本：3–4 变体 × 2 条表达式 = 6–8 条仿真；目标**先 ATOM**，基座 decay 按结构钉住。
    """
    if not (1.2 <= max_s < 1.58) or not all_alphas:
        return max_s, {}
    pairs_c, base_dec = _pick_pairs([a for a in all_alphas if a.get("s") is not None])
    if len(pairs_c) < 2:
        print("  [sweep] 凑不出 ≥2 条同基座 decay 的候选（单条批必为空批），跳过设置轴扫描")
        return max_s, {}
    n_atom = sum(1 for a in pairs_c if _is_atom_row(a))
    print(f"  [sweep] 目标 {n_atom}/{len(pairs_c)} 条 ATOM，基座 decay={base_dec}")
    codes = fetch_codes([a["alpha"] for a in pairs_c])
    pairs = [(a["tpl"], codes[a["alpha"]]) for a in pairs_c if codes.get(a["alpha"])]
    if len(pairs) < 2:
        print("  [sweep] 取不到 ≥2 条表达式，跳过设置轴扫描")
        return max_s, {}
    out = {}
    for tag, var in _variants_for(cat):
        # 基座 decay 按结构钉住（robust 族不再是全局 10）：换中性化/事件开关时若丢掉
        # 结构自己的 decay，S 的变化会被「设置 × 结构」两个变量混在一起。
        st = {"decay": base_dec}
        st.update(var)
        if "decay" in var and int(var["decay"]) == base_dec:
            print(f"  [sweep] {tag}: 与基座 decay={base_dec} 相同，跳过")
            continue
        key = f"{ds}@sw_{tag}"
        prev = [tuple(x) for x in (ck.get("sims", {}).get(key) or []) if x and x[0]]
        if prev:
            sims = prev
            print(f"  [sweep] {tag}: 复用已派发 {len(sims)} 批")
        else:
            print(f"  [sweep] {tag}: 派发 {len(pairs)} 条（覆写 {var}，基座 decay={base_dec}）")

            def _persist(p, _k=key):
                ck["sims"][_k] = list(p); save_ckpt(ck)

            # ⚠ 同一变体的所有表达式必须打**同一个标签**：`dispatch` 按标签分批，
            # 若按源模板打（lvl_sc_d6 / lvl_tr_d6），每个标签只有 1 条 ⇒ 平台必返
            # `COMPLETE children=0`，结果永远收不到（2026-10-26 实测：旧版 sweep
            # 一直是这样，`settings_sweep` 从没出过结果）。源模板命中后由 src_tpl 回填。
            sims = dispatch([(f"sw_{tag}", e) for _, e in pairs], ds, f"sw_{tag}",
                            on_batch=_persist, settings=st)
            ck["sims"][key] = sims
            save_ckpt(ck)
        rows_all = []
        for sid, tpl, bi in sims:
            if not sid:
                continue
            rows, errs, state = harvest_until_done(sid, ds, tag=f"sw_{tag}_{bi}")
            note_bad_tokens(errs)
            for _row in (rows or []):
                r6 = row6(_row)
                if not r6:
                    continue
                aid, sv, fv, y2, sub, rob = r6
                rows_all.append({"alpha": aid, "tpl": f"sw_{tag}", "s": sv, "f": fv,
                                 "y2": y2, "sub": sub, "rob": rob, "batch": f"sw_{tag}",
                                 "src_tpl": None})
        if not rows_all:
            print(f"  [sweep] {tag}: 无结果")
            continue
        # 批量标签丢了源模板 ⇒ 按「表达式逐字相等」回填（一次 GET/alphas，≤2 条）
        try:
            _expr_tpl = {e: t for t, e in pairs}
            _codes = fetch_codes([r["alpha"] for r in rows_all])
            for r in rows_all:
                r["src_tpl"] = _expr_tpl.get(_codes.get(r["alpha"]))
        except Exception as e:
            print(f"  [sweep] {tag}: src_tpl 回填失败（不影响指标）: {type(e).__name__}: {e}")
        if not rows_all:
            print(f"  [sweep] {tag}: 无结果")
            continue
        # ⚠ 2026-10-26 实测：`--sweep-done` 重跑会**复用**已派发的变体断点，而收割回来的是
        # 同一批 alpha ⇒ 旧写法直接 extend 会让同一个 alpha id 在 `res[ds]["alphas"]` 里出现
        # 两次（本轮 nanon 的 E56Z8wYm 就重复了）。指标取 max 不受影响，但下游「候选数 /
        # 族计数 / 去重表」都会虚高，故按 alpha id 去重后再并入。
        _known = {a.get("alpha") for a in all_alphas if a.get("alpha")}
        all_alphas.extend([r for r in rows_all if r.get("alpha") not in _known])
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

    旧流程这些集是在单一设置点（区域缺省 decay4 / 单一中性化）上判的 DEAD/BORDERLINE，
    而 decay 6/2、SUBINDUSTRY、CROWDING 都可能直接过闸（2026-10-26 两颗成品的实证）。
    目标选择与闸位重算**先 ATOM**：非 ATOM 腿复测再好也不产出 ATOM 成品。
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
            max_s, sweep = settings_sweep(ds, alphas, ck, res, v["max_s"],
                                          cat=cat_map.get(ds))
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
        # 闸位重算也先 ATOM（非 ATOM 腿的 S 再高，也只会把集判成「假 ALIVE」）
        ba = max((a for a in alphas if a.get("s") is not None),
                 key=lambda a: (_is_atom_row(a), a["s"]), default=None)
        # 区域闸位与 pipeline 同口径（2026-10-26 补）：IND 的 2Y 是 1.0、sub 绝对 1.0、
        # robust 固定 1.0。旧实现把 2Y 写死 1.58，会让 IND 的复测集永远算不出过闸。
        _G2Y = 1.0 if REGION == "IND" else 1.58
        _GSUB = 1.0 if REGION == "IND" else None
        _GROB = 1.0 if REGION == "IND" else None
        joint = [a for a in alphas if (a["s"] or 0) >= 1.5
                 and (a.get("f") or 0) >= 1.0 and (a["y2"] or 0) >= _G2Y
                 and (_GSUB is None or (a.get("sub") or 0) >= _GSUB)]
        v["n_joint"] = len(joint)
        v["verdict"] = ("ALIVE" if joint else
                        ("BORDERLINE" if max_s >= 1.3 else "DEAD"))
        if ba:
            def _g(x, lim):
                return None if x is None else round(max(0.0, lim - float(x)) / lim, 3)
            v["gates"] = {
                "S": {"value": ba["s"], "limit": 1.58, "gap": _g(ba["s"], 1.58)},
                "F": {"value": ba.get("f"), "limit": 1.0, "gap": _g(ba.get("f"), 1.0)},
                "2Y": {"value": ba.get("y2"), "limit": _G2Y, "gap": _g(ba.get("y2"), _G2Y)},
                "prod": {"value": v.get("prod_top"), "limit": 0.7,
                         "gap": (None if v.get("prod_top") is None
                                 else round(max(0.0, v["prod_top"] - 0.7), 3))},
            }
            if _GSUB is not None:
                v["gates"]["sub"] = {"value": ba.get("sub"), "limit": _GSUB,
                                     "gap": _g(ba.get("sub"), _GSUB)}
            if _GROB is not None:
                # 旧行 rob=None（收割脚本此前不读该指标）⇒ gap=None，deliverable 自然 fail-closed
                v["gates"]["robust"] = {"value": ba.get("rob"), "limit": _GROB,
                                        "gap": _g(ba.get("rob"), _GROB)}
            v["deliverable"] = bool(ba["s"] >= 1.58 and (ba.get("f") or 0) >= 1.0
                                    and (ba.get("y2") or 0) >= _G2Y
                                    and (_GSUB is None or (ba.get("sub") or 0) >= _GSUB)
                                    and (_GROB is None or (ba.get("rob") or 0) >= _GROB)
                                    and v.get("prod_top") is not None
                                    and v["prod_top"] < 0.7)
        res["results"][ds] = v
        save_results(res)
        beat(ds, note="sweep-done")
        emit_digest(ds, cat_map.get(ds), res, ck, len(ck.get("done") or []))
    print("\n[sweep-done] 完成")
