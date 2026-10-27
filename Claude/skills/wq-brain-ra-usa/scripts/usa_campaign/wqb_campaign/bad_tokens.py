# -*- coding: utf-8 -*-
"""平台拒绝过的表达式名全局拉黑（unknown variable / inaccessible operator / 单位不符）。"""
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


BAD_TOKEN_FILE = os.path.join(ROOT, "cache", "bad_tokens.json")
BAD_TOKENS = set()

# ⛔ 禁止拉黑的「结构算子」。2026-10-25 事故：`note_bad_tokens` 从一条报错里误抽出
# `ts_backfill` 并持久化，而**几乎所有模板族都以 ts_backfill 开头** ⇒ 下一个集起
# `filter_bad` 把全部表达式丢掉，n_alphas=0 判 NO_DATA。06:57 起 72 个集因此全部作废
# （06:56 done=42 → 07:06 done=134，10 分钟"跑完"92 个集就是这个原因）。
# 判据：算子是平台内置的通用件，报错几乎总是**输入**的问题（事件型字段、单位不符），
# 不是算子不存在 ⇒ 把算子名拉黑必然误伤全库，一律拒绝。
PROTECTED_TOKENS = {
    "ts_backfill", "ts_delta", "ts_decay_linear", "ts_ir", "ts_zscore", "ts_quantile",
    "ts_rank", "ts_scale", "ts_mean", "ts_std_dev", "ts_sum", "ts_max_diff",
    "ts_av_diff", "ts_regression", "ts_count_nans", "ts_target_tvr_decay",
    "vec_avg", "vec_sum", "vec_stddev", "vec_count", "rank", "quantile", "normalize",
    "divide", "add", "subtract", "multiply", "if_else", "greater", "less_equal", "and",
    "or", "abs", "signed_power", "winsorize", "bucket", "trade_when", "hump",
    "group_rank", "group_zscore", "group_neutralize", "group_scale",
    "vector_neut", "inst_pnl", "convert",
}


def load_bad_tokens():
    global BAD_TOKENS
    try:
        BAD_TOKENS = set(json.load(open(BAD_TOKEN_FILE, encoding="utf-8")))
    except Exception:
        BAD_TOKENS = set()
    # 历史污染的名单在加载时也要清掉结构算子，否则一次失误永久生效
    hurt = BAD_TOKENS & PROTECTED_TOKENS
    if hurt:
        BAD_TOKENS -= hurt
        print(f"  [preflight] 从黑名单剔除结构算子 {sorted(hurt)}（否则会误伤全库）")
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
    refused = new & PROTECTED_TOKENS
    if refused:
        print(f"  [preflight] 拒绝拉黑结构算子 {sorted(refused)}"
              f"（算子存在，报错来自输入；拉黑会误伤全库）")
        new -= PROTECTED_TOKENS
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
    """丢掉含黑名单名字的表达式 → (保留列表, 丢弃数)。防止一条坏式毒死整批。

    ★ 2026-10-25 加「批量否决」护栏：若某次过滤会丢掉 ≥50%（且总数 ≥4），
    说明黑名单本身有问题（典型是被污染的通用名），此时**拒绝过滤并告警**。
    宁可让一条坏式毒死一批（有 n_fail_batches 兜底），也不能让一个坏名单静默清零整集。
    """
    if not BAD_TOKENS:
        return list(exprs), 0
    keep = [(t, e) for t, e in exprs if not any(tk and tk in e for tk in BAD_TOKENS)]
    n_bad = len(exprs) - len(keep)
    # 全丢：任何规模都拒绝（批被清空 = 该集直接 NO_DATA，比一条坏式毒死整批更糟）
    if exprs and n_bad == len(exprs):
        print(f"  [preflight] ⛔ 黑名单会丢掉全部 {n_bad} 条 ⇒ 拒绝过滤，"
              f"请检查 {sorted(BAD_TOKENS)}")
        return list(exprs), 0
    # 丢 ≥50% 且规模 ≥4：几乎必然是黑名单被污染
    if len(exprs) >= 4 and n_bad / len(exprs) >= 0.5:
        print(f"  [preflight] ⛔ 黑名单会丢掉 {n_bad}/{len(exprs)} 条（≥50%）⇒ "
              f"拒绝过滤，请检查 {sorted(BAD_TOKENS)}")
        return list(exprs), 0
    return keep, n_bad


def norm_tpl(tpl):
    """补派/重派批的族名带 _f/_r/_rp 后缀，统计时并回原族。"""
    for suf in ("_rp", "_cx", "_f", "_r"):
        if tpl.endswith(suf) and len(tpl) > len(suf):
            return tpl[:-len(suf)]
    return tpl
