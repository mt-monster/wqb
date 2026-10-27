# -*- coding: utf-8 -*-
"""负向强信号镜像（P0-2）：把「S 显著为负」的 ATOM 结构性候选整式取反，复测成正向候选。

依据 `reports/ind_campaign_template_eval_20261026.md` §3.3。数学前提（逐条可验）：
整条表达式取反 `multiply(-1, code)` ⇒ 权重 w → −w ⇒ PnL 精确取负
⇒ S/F/2Y/sub/rob 全部取负，而**换手与集中度不变**（Σ|Δw|、Σ|w| 与整体符号无关）。

⚠ 三件必须记住的事（否则会把镜像读成"白捡"）：
  ① 取反**不改变量级**。「−4.35 的票镜像后 +4.35」是恒等式，不是新发现；真正的价值
     只在「同一结构反向是否也可提交」，而**换手不跟着变** —— 源 TO 0.87 ⇒ 镜像仍 0.87，
     `HIGH_TURNOVER(limit 0.4)` 照旧拦。故每条镜像都带 `tvr` 与 `turnover_blocked`。
  ② 只有**奇对称**结构才谈得上「反向信号」（白名单 `generate.MIRROR_TPL`；`dw`/`pp`/`tl`/
     `dsp_rk`/`rg_lvvol*`/`res|reslag` 被结构性地排除，理由见该常量上方注释）。
  ③ 镜像行**不并入** `all_alphas`：`max_s` / `joint` / `near_gate` / `pick_prod_target` /
     `settings_sweep` 全部保持「正向电池」口径。旧计划的写法会让 `sweep` 的
     `1.2 <= max_s < 1.58` 判据被「−4.35 镜像出的 +4.35」直接抑制，等于把设置轴扫描关掉。
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
from .generate import is_mirror_tpl
from .transport import dispatch, harvest_until_done, fetch_alpha_meta
from .audit import fetch_codes, check_prod
from .persist import save_ckpt
from .bad_tokens import note_bad_tokens


NEG_GATE = 1.58        # 源侧「强负」门槛：镜像后 S 至少够 1.58 才值得占槽位
MIRROR_CAP = 2         # 每集最多镜像几条源（成本上限 2 条仿真/集）
MIRROR_PROBE = 6       # 取元数据的上限（越负越优先；ATOM / 设置闸会筛掉一部分）
TURNOVER_MAX = 0.40    # 平台 HIGH_TURNOVER 的 limit；镜像不改换手 ⇒ 源超了镜像必超
NEG_PROD_CAP = 1       # 每集最多为几条 joint 镜像测 prod（异步相关队列很贵）

_env = (os.environ.get("WQB_NEG_MIRROR") or "").strip().lower()
if _env in ("0", "false", "off", "no"):
    NEG_MIRROR = False
elif _env in ("1", "true", "on", "yes"):
    NEG_MIRROR = True
else:
    NEG_MIRROR = (REGION == "IND")     # 缺省：IND 的 ATOM 电池专用（EUR 行为不变）


def neg_stats(all_alphas):
    """负向统计（只看前向电池；`_neg` 行不计）。

    `max_neg_s` 是**负向簇的上沿**：它 < 0 表示该集整体偏负（正向电池一个正值都没有），
    这正是「镜像可能翻出成果」的形态；≈0 则说明正负混杂，镜像只是补充。
    """
    svals = [a.get("s") for a in (all_alphas or [])
             if not a.get("neg") and a.get("s") is not None]
    if not svals:
        return {"min_s": None, "max_abs_s": None, "max_neg_s": None, "n_strong": 0}
    negs = [s for s in svals if s < 0]
    return {
        "min_s": round(min(svals), 3),
        "max_abs_s": round(max(svals, key=abs), 3),
        "max_neg_s": round(max(negs), 3) if negs else None,
        "n_strong": sum(1 for s in svals if s <= -NEG_GATE),
    }


def _pick_sources(all_alphas):
    """可镜像的强负源：奇对称族 + S ≤ −NEG_GATE，越负越优先。"""
    cand = [a for a in (all_alphas or [])
            if not a.get("neg")
            and is_mirror_tpl(a.get("tpl"))
            and a.get("s") is not None and a["s"] <= -NEG_GATE]
    cand.sort(key=lambda a: a["s"])
    return cand


def _dispatch_settings(meta):
    """镜像必须逐字复现源设置（除 code 反向）。

    只覆写 decay 是不够的：源可能来自设置轴扫描（CROWDING / SUBINDUSTRY / decay 6）
    或 robust 几何批（decay 10/6/2）。设置不一致时「镜像」就不是精确取负，
    而是一个同时换了方向与设置的新实验 —— 指标不可归因。
    """
    st = dict(meta.get("settings") or {})
    dec = meta.get("decay")
    if dec is not None:
        st["decay"] = str(dec)
    return st


def _val(v):
    if v is None:
        return None
    try:
        x = float(v)
    except (TypeError, ValueError):
        return None
    return None if x <= -90 else x


def _joint(a, g2y, gsub=None, grob=None):
    return ((a.get("s") or -9) >= 1.58
            and (a.get("f") or 0) >= 1.0
            and (a.get("y2") or -9) >= g2y
            and (gsub is None or (a.get("sub") or -9) >= gsub)
            and (grob is None or (a.get("rob") or -9) >= grob))


def _norm_expr(e):
    return re.sub(r"\s+", "", e or "")


def run_neg_mirror(ds, all_alphas, ck, g2y, gsub=None, grob=None):
    """对本集的强负 ATOM 源派镜像批 → 返回 `neg` 块（**不改** all_alphas / per_tpl）。

    返回键：`min_s` / `max_abs_s` / `max_neg_s` / `n_strong`（负向统计，恒有）
           `sources`（源清单）/ `mirrors`（镜像结果，含 tvr 与闸位）/ `joint`（镜像里过闸的）
           `turnover_blocked`（被换手拦下但指标全过的条数）/ `prod_top` / `skipped`（选源被拒原因）
    """
    out = dict(neg_stats(all_alphas))
    out.update({"sources": [], "mirrors": [], "joint": 0,
                "turnover_blocked": 0, "prod_top": None, "skipped": []})
    if not NEG_MIRROR:
        return out
    cand = _pick_sources(all_alphas)
    if not cand:
        return out
    probe = cand[:MIRROR_PROBE]
    meta = fetch_alpha_meta([a["alpha"] for a in probe]) if probe else {}
    picked = []
    for a in probe:
        m = meta.get(a["alpha"])
        if not m:
            out["skipped"].append({"alpha": a["alpha"], "why": "元数据不可得"})
            continue
        if not m.get("atom"):
            out["skipped"].append({"alpha": a["alpha"],
                                   "why": "非 ATOM（平台单数据集判据：需 LOW_2Y_SHARPE 且无 IS_LADDER_SHARPE）"})
            continue
        if not m.get("code"):
            out["skipped"].append({"alpha": a["alpha"], "why": "无 regular.code"})
            continue
        if m.get("decay") is None:
            out["skipped"].append({"alpha": a["alpha"], "why": "无 settings.decay"})
            continue
        picked.append({"src": a, "meta": m, "st": _dispatch_settings(m),
                       "tvr": m.get("tvr")})
        if len(picked) >= MIRROR_CAP:
            break
    if not picked:
        print(f"  [neg] {ds}: 强负源 {len(cand)} 条，但无可镜像 ATOM"
              + (f"（{len(out['skipped'])} 条被筛）" if out["skipped"] else ""))
        return out
    for p in picked:
        p["expr"] = f"multiply(-1, {p['meta']['code']})"
    out["sources"] = [{"alpha": p["src"]["alpha"], "tpl": p["src"].get("tpl"),
                       "s": p["src"].get("s"), "tvr": p["tvr"],
                       "decay": p["meta"]["decay"],
                       "settings": p["st"], "code": p["meta"]["code"]}
                      for p in picked]
    print(f"  [neg] {ds}: 强负源 {len(cand)} 条 → 镜像 {len(picked)} 条"
          f"（S={[p['src'].get('s') for p in picked]}，"
          f"TO={[p['tvr'] for p in picked]}）")

    # 一个 dispatch 调用只能带一套 settings ⇒ 按「完整设置」分组（正常只有 decay 4 一组）
    groups = collections.OrderedDict()
    for p in picked:
        groups.setdefault(json.dumps(p["st"], sort_keys=True), []).append(p)
    used = collections.Counter()
    mir_rows = []      # (aid, S, F, 2Y, sub, rob)
    for sig, grp in groups.items():
        st = dict(grp[0]["st"])
        dec = st.get("decay") or "?"
        key = f"{ds}@ng_d{dec}"
        used[key] += 1
        if used[key] > 1:          # 同 decay 不同设置（罕见）→ 后缀区分，避免断点互覆盖
            key = f"{key}_{used[key]}"
        prev = [tuple(x) for x in (ck.get("sims", {}).get(key) or []) if x and x[0]]
        if prev:
            print(f"  [neg] {key}: 复用已派发 {len(prev)} 批")
            sims = prev
        else:
            exprs = [(f"{p['src'].get('tpl')}_neg", p["expr"]) for p in grp]
            print(f"  [neg] {key}: 派发 {len(exprs)} 条（覆写 {st}）")

            def _persist(pp, _k=key):
                ck["sims"][_k] = list(pp)
                save_ckpt(ck)

            sims = dispatch(exprs, ds, f"ng_d{dec}", on_batch=_persist, settings=st)
            ck["sims"][key] = sims
            save_ckpt(ck)
        for sid, tpl, bi in sims:
            if not sid:
                continue
            rows, errs, state = harvest_until_done(sid, ds, tag=f"neg_{tpl}_{bi}")
            note_bad_tokens(errs)
            if not rows:
                print(f"  [neg] {tpl}_{bi} 无结果（state={state}，err={errs[:1]}）")
                continue
            for _row in rows:
                r6 = tuple(_row)
                if len(r6) >= 6:
                    mir_rows.append((r6[0], r6[1], r6[2], r6[3], r6[4], _val(r6[5])))
                elif len(r6) == 5:
                    mir_rows.append((r6[0], r6[1], r6[2], r6[3], r6[4], None))
    if not mir_rows:
        return out

    # 按「表达式逐字相等」回填源（批量标签丢了源；MIRROR_CAP 很小，一次 GET 足够）
    expr2src = {_norm_expr(p["expr"]): p for p in picked}
    try:
        codes = fetch_codes([r[0] for r in mir_rows])
    except Exception as e:
        print(f"  [neg] 回填源失败（不影响指标）：{type(e).__name__}: {e}")
        codes = {}
    for aid, sv, fv, y2, sub, rob in mir_rows:
        p = expr2src.get(_norm_expr(codes.get(aid) or ""))
        if p is None and len(picked) == 1:
            p = picked[0]
        tvr = (p or {}).get("tvr")
        rec = {"alpha": aid, "of": (p or {}).get("src", {}).get("alpha"),
               "tpl": (p or {}).get("src", {}).get("tpl"),
               "s": sv, "f": fv, "y2": y2, "sub": sub, "rob": rob,
               "tvr": tvr,
               "joint": False, "turnover_blocked": False}
        rec["joint"] = _joint(rec, g2y, gsub, grob)
        rec["turnover_blocked"] = bool(rec["joint"] and tvr is not None
                                       and tvr > TURNOVER_MAX)
        out["mirrors"].append(rec)
    out["mirrors"].sort(key=lambda r: -(r.get("s") or -9))
    out["joint"] = sum(1 for r in out["mirrors"] if r["joint"])
    out["turnover_blocked"] = sum(1 for r in out["mirrors"] if r["turnover_blocked"])

    # 只对「指标全过且没被换手拦」的镜像测 prod：ALIVE_NEG 要可行动，否则等于没结论
    act = [r for r in out["mirrors"] if r["joint"] and not r["turnover_blocked"]]
    if act and NEG_PROD_CAP > 0:
        tgt = act[0]
        print(f"  [neg] 测镜像候选 {tgt['alpha']}（S={tgt['s']}，TO={tgt['tvr']}）的 prod…")
        try:
            out["prod_top"] = check_prod(tgt["alpha"])
        except Exception as e:
            print(f"  [neg] prod 探测失败：{type(e).__name__}: {e}")
        if out["prod_top"] is not None:
            print(f"  [neg] {tgt['alpha']} prod={out['prod_top']:.3f}"
                  + ("  ✗ prod>0.7 死局" if out["prod_top"] >= 0.7 else "  ✓ prod 过线"))
    for r in out["mirrors"][:4]:
        print(f"     {r['alpha']}(of {r['of']}) S={r['s']} F={r['f']} 2Y={r['y2']} "
              f"sub={r['sub']} rob={r['rob']} TO={r['tvr']}"
              + ("  ✓ 全闸" if r["joint"] else "")
              + ("  ✗ 换手超限" if r["turnover_blocked"] else ""))
    return out
