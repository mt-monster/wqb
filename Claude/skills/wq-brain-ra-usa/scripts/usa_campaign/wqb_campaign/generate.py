# -*- coding: utf-8 -*-
"""模板族架构与表达式构造：L1 提取 × L2 归一交叉采样 + 载体扩散 + 后处理电池。"""
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
    # 2026-10-24 补：**截面**分位归一化（原矩阵只有时序 ts_quantile，缺截面版）。
    # 用户指出 + GEM 实证（EUR 3515 条里 quantile 使用率 3%）。
    # 对 discrete_rating（字段本身即百分位秩）语义匹配：截面重归一而非时序分位。
    "qc": "quantile({X})",
}
# 组合表（标定实证筛选）：(L1, L2)；va=波动调整特例；dw=L3 特殊结构
FAMILIES = [
    ("lvl", "rk"), ("lvl", "zs"), ("lvl", "qt"), ("lvl", "tr"), ("lvl", "sc"),
    ("d1", "rk"), ("d1", "va"),
    ("d2", "rk"),
    ("ed", "rk"),
    ("ir", None),
    ("dsp", "rk"),
    ("lvl", "qc"), ("d2", "qc"),
]


_L1_LAYER = {"lvl": "lvl", "d1": "diff", "d2": "diff", "ed": "event", "ir": "level_ratio",
             "dsp": "disp"}


def ensure_l1_coverage(allow):
    """保证模板族并集覆盖 L1 的「水平」与「差分」两类；缺层则补（L2 用 rk，最便宜）。"""
    if not allow:
        return allow
    layers = {_L1_LAYER.get(f.split("_")[0]) for f in allow}
    out = set(allow)
    if "lvl" not in layers:
        out.add("lvl_rk")
    if "diff" not in layers:
        out.add("d1_rk")
    return out


# ★★★★★ 2026-10-25：`ts_backfill` **不能用于事件型字段**（平台报
#   `Operator ts_backfill does not support event inputs`，整批 FAIL）。
#   KOR 的 news 系集全是事件流，导致首个集就连着 FAIL；EUR 也有 3 个 SIM_FAIL 同源。
#   开关：WQB_NO_BACKFILL=1 ⇒ 把 L1 模板里的 ts_backfill 全部剥掉（保留其余结构）。
#   为什么不在报错后自动拉黑算子：算子本身合法，是**输入类型**不兼容，
#   拉黑会误伤全库（EUR 已踩过，见 bad_tokens.PROTECTED_TOKENS）。
if os.environ.get("WQB_NO_BACKFILL"):
    L1_EXTRACT = {_k: _v.replace("ts_backfill({F}, {BF})", "{F}")
                      .replace("ts_backfill({F}, 252)", "{F}")
                      .replace("ts_backfill(vec_stddev({FR}), {BF})", "vec_stddev({FR})")
                  for _k, _v in L1_EXTRACT.items()}
    _orig_dw = None

DW_TPL = "multiply(rank(ts_mean(ts_backfill({F}, {BF}), {WS})), rank(ts_mean(ts_backfill({F}, {BF}), {WL})))"
if os.environ.get("WQB_NO_BACKFILL"):
    DW_TPL = DW_TPL.replace("ts_backfill({F}, {BF})", "{F}")
VA_TPL = "divide(ts_delta(ts_backfill({F}, {BF}), {W1}), add(ts_std_dev(ts_backfill({F}, {BF}), {ZW}), 0.0001))"


# ---------------- 残差化族（2026-10-25 接入）----------------
# IND 唯一被证实能过 prod 墙的配方（docs/reference/IND/institutions6_field_profile.md §2.1）：
#   rank(-ts_regression(ts_zscore(returns, W), ts_zscore(F, W), W, rettype=0))，W=252；decay=126
# wave232 实测该结构 10/10 RA 全过（E5VNe67L S3.20 / KPmvEYeE S3.07 / vRO9nG3w S2.90）。
# 增强轴（同文件 §2.3，均 RA failed=0）：字段滞后 21 天 2.98→3.10；W=252 最强（63 明显偏弱）。
# 合规：locked.py `mixed_signal_ban` 明确允许「第二个数据集只以条件 / 分组 / 残差入场」。
# ⚠ 窗口 21 不在 STANDARD_WINDOWS，按「带实测证据的例外」使用（§2.3 数据即证据）。
# ⚠ 该族必须用 decay=RESIDUAL_DECAY 派发：IND 基础 decay=4 复现不了实测结果
#   （wave232 的 10 颗全部 decay=126）⇒ 由 pipeline 单独一批派发，不混进主派发。
RESIDUAL_TPL = {
    "res": "rank(-ts_regression(ts_zscore(returns, 252), ts_zscore({X}, 252), 252, rettype=0))",
    "reslag": ("rank(-ts_regression(ts_zscore(returns, 252), "
               "ts_zscore(ts_delay({X}, 21), 252), 252, rettype=0))"),
}
RESIDUAL_DECAY = 126


def build_residual(sel, cat=None):
    """残差化族：returns 对字段（reslag 变体再滞后 21 天）回归取残差后取反。

    只给非探针、非 skip、非 returns 自身的字段（探针层遵守 1 条/字段成本纪律）。
    VECTOR 字段先用 wrap() 聚合成截面量；矩阵字段原样进 ts_zscore。
    """
    out = []
    for r in sel:
        if r.get("tier") == "probe" or r.get("form") == "skip":
            continue
        if r["field_name"] == "returns":
            continue                       # returns 对自身回归退化
        X = wrap(r)
        _hint = field_exposure_hint(r, cat)
        for tpl, tmpl in RESIDUAL_TPL.items():
            e = tmpl.format(X=X)
            out.append((tpl, e))
            EXPR_EXPOSURE[e] = _hint if _hint != "value" else FAMILY_EXPOSURE.get(tpl, "other")
    return out


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


PROBE_FIELD_CAP = 12   # 探针层字段上限（每个只跑 1 条 lvl_rk）


def strip_backfill(code, F, FR, BF):
    """VECTOR / 事件型字段兼容改写：剥掉 ts_backfill，保留其余结构。

    2026-10-25 IND option1 实测：平台报
      `Operator ts_backfill does not support event inputs`
    且该 multisim 10 个子任务**全部 ERROR/CANCELLED（连坐）**。
    option1 全是 VECTOR 字段 ⇒ 对 VECTOR 字段改写成无 backfill 版本；
    矩阵字段行为不变（EUR 依赖 backfill 补稀疏，不能全局关，见 WQB_NO_BACKFILL）。
    """
    if not code or "ts_backfill" not in code:
        return code
    for _a in {F, FR}:
        code = code.replace(f"ts_backfill({_a}, {BF})", _a)
        code = code.replace(f"ts_backfill({_a}, 252)", _a)
    # dsp 模板的载体是 vec_stddev(FR)，不是 wrap(r) ⇒ 单独剥一次
    code = code.replace(f"ts_backfill(vec_stddev({FR}), {BF})", f"vec_stddev({FR})")
    code = code.replace(f"ts_backfill(vec_stddev({FR}), 252)", f"vec_stddev({FR})")
    return code


def build_one_family(tpl, r, freq):
    """把指定族的结构套在某个字段上（载体扩散用）。"""
    BF, WS, WL, ZW, W1 = FREQ_WIN.get(freq, FREQ_WIN["unknown"])
    F, FR = wrap(r), r["field_name"]

    def _fin(x):
        return strip_backfill(x, F=F, FR=FR, BF=BF) if r.get("field_type") == "VECTOR" else x

    if tpl in RESIDUAL_TPL:
        # 载体扩散到 residual 结构：用同一 W=252/lag 变体，派发方负责带 decay=126
        return _fin(RESIDUAL_TPL[tpl].format(X=F))
    if tpl == "dw":
        return _fin(DW_TPL.format(F=F, BF=BF, WS=WS, WL=WL))
    if tpl == "pp":
        # pp 不是独立模板，而是「dw 结构 + 0.85 稀疏门控」（sentiment26/wp99v7qv 的成品形态）
        dw = DW_TPL.format(F=F, BF=BF, WS=WS, WL=WL)
        return _fin(f"if_else(greater(rank({dw}), 0.85), {dw}, 0)")
    if tpl.endswith("_pl"):
        l1, l2 = tpl[:-3], None
    elif "_" in tpl:
        l1, l2 = tpl.split("_", 1)
    else:
        l1, l2 = tpl, None
    if l1 not in L1_EXTRACT:
        return None
    if l2 == "va":
        return _fin(VA_TPL.format(F=F, BF=BF, ZW=ZW, W1=W1))
    x = L1_EXTRACT[l1].format(F=F, FR=FR, BF=BF, ZW=ZW, W1=W1)
    if l2:
        x = L2_NORM[l2].format(X=x, ZW=ZW)
    return _fin(x)


def wrap(r):
    if r["field_type"] != "VECTOR":
        return r["field_name"]
    return f"vec_sum({r['field_name']})" if r["sem_type"] == "count" else f"vec_avg({r['field_name']})"


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
            # VECTOR 字段必须用 vec_* 包裹且不能 backfill（2026-10-25 IND option1 实测）
            _Fp = wrap(r)
            _x = L1_EXTRACT["lvl"].format(F=_Fp, FR=FR, BF=BF, ZW=ZW, W1=W1)
            _e = L2_NORM["rk"].format(X=_x, ZW=ZW)
            if r.get("field_type") == "VECTOR":
                _e = strip_backfill(_e, F=_Fp, FR=FR, BF=BF)
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
            _allow = ensure_l1_coverage(_cf if _cf else set(BLACKBOX_FAMILIES))
            _gated_f = True               # 黑盒也开 pp/tl 门控（实测 pp 是 other 形态最强族）
        else:
            _allow = None if _force_full else FORM_FAMILIES.get(_form)
            if _allow is None and not _force_full:
                # form=other ⇒ 形态分类器失效，用概念补（2026-10-24）
                _cf = concept_families(r, cat, ds)
                if _cf:
                    _allow = _cf
            # ★ L1 覆盖保证：补上缺失的时间导数层（治「形态≠导数层」的系统性盲区）
            _allow = ensure_l1_coverage(_allow)
            _gated_f = _gated
        # 概念留痕：汇报与后续校准都要用
        r["concepts"] = field_concepts(r, cat, ds)
        # ② preprocessing：只对受控词表命中的字段生效（自由文本已在 parse 阶段丢弃）。
        #   在族内套，以便跳过与模板自身 L2 重复的归一（如预处理说 rank 而模板就是 rank）。
        F0 = wrap(r)
        _toks = pp_map.get(FR)
        _is_vec = r.get("field_type") == "VECTOR"
        if _is_vec and _toks:
            # VECTOR/事件字段不接受 ts_backfill ⇒ 预处理里的 backfill 令牌必须摘掉
            _toks = [t for t in _toks if t != "backfill"]
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
            if _is_vec:
                x = strip_backfill(x, F=F, FR=FR, BF=BF)
            out.append((_fam, x))
            EXPR_EXPOSURE[x] = _hint if _hint != "value" else FAMILY_EXPOSURE.get(_fam, "other")
        _Fdw = apply_preprocessing(F0, _toks, FR, BF, ZW, None) if _toks else F0
        if _allow is None or "dw" in _allow:
            _dw = DW_TPL.format(F=_Fdw, BF=BF, WS=WS, WL=WL)
            if _is_vec:
                _dw = strip_backfill(_dw, F=_Fdw, FR=FR, BF=BF)
            out.append(("dw", _dw))
            EXPR_EXPOSURE[_dw] = _hint if _hint != "value" else FAMILY_EXPOSURE.get("dw", "other")
        # 稀疏门控一等模板（之前只在 build_postproc 对 top3 生效 ⇒ sentiment26 的 pp 只覆盖 2/19 字段）
        if _gated_f and (_allow is None or "pp" in _allow):
            _dw = DW_TPL.format(F=_Fdw, BF=BF, WS=WS, WL=WL)
            _pp = f"if_else(greater(rank({_dw}), {GATE_Q}), {_dw}, 0)"
            if _is_vec:
                _pp = strip_backfill(_pp, F=_Fdw, FR=FR, BF=BF)
            out.append(("pp", _pp))
            EXPR_EXPOSURE[_pp] = _hint if _hint != "value" else FAMILY_EXPOSURE.get("pp", "other")
            _m = (f"rank(ts_mean({_Fdw}, {WS}))" if _is_vec
                  else f"rank(ts_mean(ts_backfill({_Fdw}, {BF}), {WS}))")
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
