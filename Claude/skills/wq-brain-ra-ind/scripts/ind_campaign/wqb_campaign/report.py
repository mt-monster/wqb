# -*- coding: utf-8 -*-
"""汇报层：digest 追加/替换 + progress.json + 总体情况块。"""
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


def _rob_ok(v):
    """robust 闸（限值固定 1.0）：None/-99 哨兵一律 False（不可验证 ⇒ 不算过闸）。"""
    try:
        return float(v) >= 1.0
    except (TypeError, ValueError):
        return False


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
    # 2026-10-26：闸位按区域取（IND 2Y=1.0、sub 绝对 1.0、robust 1.0；EUR 2Y=1.58、sub≥0.53×S）。
    # 旧实现把 2Y≥1.58 写死 ⇒ IND 的 near-delivery 长期空转，robust 更是从未进入汇报。
    _G2Y = 1.0 if REGION == "IND" else 1.58
    _GSUB = 1.0 if REGION == "IND" else None
    _GROB = 1.0 if REGION == "IND" else None
    cands = []
    for k, v in ranked:
        for a in (v.get("alphas") or []):
            s, y2 = a.get("s"), a.get("y2")
            if s is not None and y2 is not None and s >= 1.5 and y2 >= _G2Y:
                _sub = a.get("sub")
                _rob = a.get("rob")
                cands.append({"ds": k, "alpha": a.get("alpha"), "S": s, "F": a.get("f"),
                              "2Y": y2, "sub": _sub, "rob": _rob, "tpl": a.get("tpl"),
                              "fragile": bool((v.get("year_profile") or {}).get("fragile")),
                              "sub_ok": (_sub is not None and (
                                  _sub >= _GSUB if _GSUB is not None else _sub >= 0.53 * s)),
                              "rob_ok": (_rob_ok(_rob) if _GROB is not None else True)})
    cands.sort(key=lambda x: -x["S"])
    near = cands

    _yp = cur.get("year_profile") or {}
    _frag = ("frag=✗" if _yp.get("fragile") else ("frag=✓" if _yp else "frag=?"))
    _gr = (cur.get("gates") or {}).get("robust") or {}
    _rob = f" rob={_gr.get('value')}" if _gr else ""
    # P0-2：负向强源与镜像结果必须在 digest 里可见 —— 否则 `DEAD_NEG` 与 `DEAD`
    # 在跨会话复核时长得一模一样，下一波会把「数据有强反应」的集误当「没信号」搁置。
    _ng = cur.get("neg") or {}
    _neg_txt = ""
    if _ng and (_ng.get("n_strong") or _ng.get("mirrors")):
        _neg_txt = (f" neg[min={_ng.get('min_s')} strong={_ng.get('n_strong')}"
                    f" mirror={len(_ng.get('mirrors') or [])}"
                    f" joint={_ng.get('joint')} TO✗={_ng.get('turnover_blocked')}"
                    + (f" prod={_ng.get('prod_top')}" if _ng.get("prod_top") is not None else "")
                    + "]")
    line = (f"- {datetime.now():%m-%d %H:%M} **{ds}**({cat}) → {cur.get('verdict')} "
            f"S={cur.get('max_s')} 2Y={cur.get('max_2y')} joint={cur.get('n_joint')} "
            f"n={cur.get('n_alphas')} prod={cur.get('prod_top')}{_rob} {_frag}"
            + (f" y0={_yp.get('first_year')} top={_yp.get('top_share')}" if _yp else "")
            + _neg_txt)
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
    n_robok = sum(1 for c in near if c.get("rob_ok"))
    print(f"  │ 距交付最近(S≥1.5&2Y≥{_G2Y} 逐 alpha) {len(near)} 颗，其中 sub 过闸 {n_subok} 颗"
          + (f"、robust 过闸 {n_robok} 颗" if _GROB is not None else "")
          + (": " + ", ".join(
              f"{c['ds']}/{c['alpha']}(S{c['S']},2Y{c['2Y']}"
              f"{'' if c.get('sub_ok') else ',sub✗'}"
              f"{'' if c.get('rob_ok') else ',rob✗'})" for c in near[:4]) if near else ""))
    print(f"  └─ 本集 {ds}: {cur.get('verdict')}  S={cur.get('max_s')}  "
          f"2Y={cur.get('max_2y')}  joint={cur.get('n_joint')}  prod={cur.get('prod_top')}\n")
