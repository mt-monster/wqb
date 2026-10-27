# -*- coding: utf-8 -*-
"""按平台「当季金字塔」统计我方提交数 / category，满 3 颗即点亮（选区降权依据）。

★ 2026-10-25 用户裁定：旧口径是「拉全部 stage=OS alpha 的历史累计」，与平台不一致。
  平台 `get_pyramid_alphas()` **默认取当季**（`brain_mixin_correlation.py:1021-1040`），
  三格塔**当季满 3 颗**才点亮。历史累计会把「早已点亮、但当季还没补满」的塔长期判为亮：
  IND/D1 实测 FUNDAMENTAL 历史 5 / 当季 2、RISK 6 / 1、INSTITUTIONS 4 / 1
  ⇒ 平台实际还差 1 / 2 / 2 颗，旧口径却把它们排除在第一波外（`[lit]` 首屏可复核）。

  口径要点：
  - 数据源：`GET /users/self/activities/pyramid-alphas`（不传日期 = 平台按当季取）；
  - 只认 `pyramids[REGION]["D<n>"]` 这一桶（本流水线固定 D1，见 config.DELAY）；
  - 计数为 0 的类别不入缓存（消费方 `counts.get(cat, 0)` 等价于 0）。
"""
import os
import sys
import json
import asyncio
import time

from .config import *            # noqa: F401,F403
from .config import _WQB_SCRIPTS_DIR, DELAY  # noqa: F401

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

# 缓存格式版本：口径变更必须换版本，旧缓存自动失效（不能拿历史累计冒充当季）
LIT_METRIC = "pyramid_alphas_quarter_v1"
DELAY_KEY = f"D{DELAY}"


def counts_from_pyramid(data, region, delay_key=DELAY_KEY):
    """从平台 `pyramid-alphas` 响应抽取某区域某 delay 的当季计数（纯函数，便于单测）。

    必须兼容**两种形态**（同一份数据，客户端与 MCP 层各一种）：
      ① 客户端原始（`brain_api.get_pyramid_alphas` 直接返回，list）：
         {"pyramids": [{"category": {"id": "pv"}, "region": "IND",
                        "delay": 1, "alphaCount": 8}, ...]}
      ② MCP `_slim_pyramids()` 重排后（dict）：{"pyramids": {"IND": {"D1": {"pv": 8}}}}
    只保留 n>0 的类别；结构异常一律返回 {}（按无点亮处理，不猜）。
    """
    if not isinstance(data, dict):
        return {}
    pyl = data.get("pyramids")
    reg = str(region or "").upper()

    # ① 原始 list 形态
    if isinstance(pyl, list):
        try:
            want_delay = int(str(delay_key).lstrip("Dd"))
        except (TypeError, ValueError):
            want_delay = None
        out = {}
        for p in pyl:
            if not isinstance(p, dict):
                continue
            if str(p.get("region") or "").upper() != reg:
                continue
            try:
                if want_delay is None or int(p.get("delay")) != want_delay:
                    continue
            except (TypeError, ValueError):
                continue
            cat = p.get("category")
            cat_id = cat.get("id") if isinstance(cat, dict) else cat
            if not cat_id:
                continue
            try:
                n = int(p.get("alphaCount") or 0)
            except (TypeError, ValueError):
                continue
            if n > 0:
                out[str(cat_id).upper()] = n
        return out

    # ② MCP 重排后的 dict 形态
    if isinstance(pyl, dict):
        per_delay = (pyl.get(reg) or {}).get(delay_key)
        if not isinstance(per_delay, dict):
            return {}
        out = {}
        for cat, n in per_delay.items():
            try:
                n = int(n or 0)
            except (TypeError, ValueError):
                continue
            if n > 0:
                out[str(cat).upper()] = n
        return out
    return {}


def compute_lit(region=None, ttl_h=12, refresh=False):
    """返回 {CAT: 当季我方已提交数}；满 LIT_THRESHOLD(=3) 颗即该塔点亮。

    ⚠ 必须走平台 `pyramids`（本地 datasets.category 有大量 NULL，会低估）。
    ⚠ 失败时返回 {}（「无点亮」），不写缓存 —— 免得一次网络抖动在 ttl 内被当成事实。
    """
    region = (region or REGION).upper()
    try:
        if not refresh and os.path.isfile(LIT_CACHE):
            j = json.load(open(LIT_CACHE, encoding="utf-8"))
            ent = j.get(region) or {}
            fresh = time.time() - (ent.get("ts") or 0) < ttl_h * 3600
            if fresh and ent.get("metric") == LIT_METRIC and ent.get("delay") == DELAY_KEY:
                return ent["counts"]
    except Exception:
        pass

    async def _fetch():
        sys.path.insert(0, os.path.join(ROOT, "world-quant-brain-mcp"))
        from brain_api import brain_client
        await brain_client.ensure_authenticated()
        # 不传日期 = 平台默认当季（与里程碑口径一致）
        return await brain_client.get_pyramid_alphas()

    try:
        data = asyncio.run(_fetch())
    except Exception as e:
        print(f"[lit] 平台当季金字塔统计失败（{type(e).__name__}: {e}），本轮按无点亮处理")
        return {}
    cnt = counts_from_pyramid(data, region)
    if not cnt:
        print(f"[lit] 平台当季金字塔未返回 {region}/{DELAY_KEY} 计数，本轮按无点亮处理")
        return {}
    try:
        os.makedirs(os.path.dirname(LIT_CACHE), exist_ok=True)
        old = json.load(open(LIT_CACHE, encoding="utf-8")) if os.path.isfile(LIT_CACHE) else {}
        old[region] = {"ts": time.time(), "metric": LIT_METRIC,
                       "delay": DELAY_KEY, "counts": cnt}
        tmp = LIT_CACHE + ".tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(old, f, ensure_ascii=False, indent=1)
        os.replace(tmp, LIT_CACHE)
    except Exception:
        pass
    return cnt
