# -*- coding: utf-8 -*-
"""断点/结果的原子读写 + 心跳。所有落盘必须走这里，禁止散落 open('w')。"""
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
    os.makedirs(os.path.dirname(LOG), exist_ok=True)   # 自定义 STATE_DIR 时保险
    tmp = LOG + ".tmp"
    json.dump(res, open(tmp, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    os.replace(tmp, LOG)


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
