# -*- coding: utf-8 -*-
"""体检与画像：相关性实测 / 逐年画像（样本有效性）/ 取表达式源码。"""
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


def _api_get_json(client, path, tries=2, base_sleep=1.0):
    """GET `{base_url}{path}` 并回 JSON；429/5xx 退避重试。

    ★ 2026-10-26 内联：原先 `from wqb_tools import _get_json`，而 `wqb_tools` 住在
    仓库外 `~/wqb-scripts/`（未跟踪、无备份）。该文件消失后，`fetch_codes`（阶段 2
    取源码）与 `year_profile`（十年数据校验）同时 ImportError，被各自的 `except`
    吞成"无数据"——两个关键校验静默失效，战役照跑。只依赖仓库内 `brain_api`。
    """
    async def _go():
        last = None
        for i in range(max(1, tries)):
            r = await client._request("GET", f"{client.base_url}{path}")
            if r.status_code == 200:
                try:
                    return r.json()
                except Exception:
                    return None
            last = r
            if r.status_code in (429, 500, 502, 503, 504) and i + 1 < tries:
                await asyncio.sleep(base_sleep * (i + 1))
                continue
            break
        if last is not None:
            print(f"  [api] GET {path} -> {last.status_code} "
                  f"{(getattr(last, 'text', '') or '')[:120]}")
        return None

    return _go()


def check_prod(alpha_id, max_wait=240):
    """测单个 alpha 的 prod 相关性（端点异步排队：先触发再轮询取值）。

    2026-10-22 教训：两个强集（sentiment26 0.755、ai_equity_alpha 0.7775）都是
    「S 看着行、prod 已死」的假阳性——判定环节不测 prod 会一直白挖。
    2026-10-22 二修：响应结构是 `{schema:{max:...}, records:[...]}`，
    旧实现只读顶层 `max`/`max_correlation` ⇒ 全部返回 None（本 campaign 前 14 集 prod 全空的原因）。
    """
    import asyncio
    sys.path.insert(0, os.path.join(ROOT, "world-quant-brain-mcp"))
    from brain_api import brain_client

    def _parse(j):
        if not isinstance(j, dict):
            return None
        sch = j.get("schema") or {}
        for v in ((sch or {}).get("max"), j.get("max"), j.get("max_correlation")):
            if v is not None:
                try:
                    return float(v)
                except (TypeError, ValueError):
                    pass
        mx = None
        for row in (j.get("records") or []):
            for v in (row if isinstance(row, (list, tuple)) else list(row.values())):
                if isinstance(v, (int, float)) and (mx is None or v > mx):
                    mx = float(v)
        return mx

    async def _go():
        await brain_client.ensure_authenticated()
        # 2026-10-25 修：get_production_correlation 的缺省内轮询是 900s，
        # 外层再乘 max(3, max_wait//10) 次 ⇒ 单颗 alpha 最坏能耗数小时
        # （实测 gJWlvd0v：412 循环 907s 超时后又立刻重开一轮，campaign 卡死近 1 小时）。
        # 显式把单次内轮询限到 ≤60s，并用总截止时间守住 max_wait。
        loop = asyncio.get_running_loop()
        deadline = loop.time() + max(30, max_wait)
        while loop.time() < deadline:
            remaining = max(10.0, deadline - loop.time())
            try:
                j = await brain_client.get_production_correlation(
                    alpha_id, max_wait_seconds=min(60.0, remaining))
            except Exception:
                j = None
            mx = _parse(j)
            if mx is not None:
                return mx
            await asyncio.sleep(10)
        return None
    try:
        return asyncio.run(_go())
    except Exception:
        return None


def year_profile(alpha_id, max_wait=60):
    """年度画像（2026-10-23 用户指出「回测前三年都没数」后新增）。

    实测案例：sentiment26 的 alpha 2014-2016 **零持仓**（数据 2017-01 才有），
    2020 一年贡献 51% 净 PnL、2021 是 −0.91 Sharpe ⇒ 这类「靠单一年份/单一 regime」的 alpha
    即使六闸全过也不该交付：全期 Sharpe 是被一年撑起来的，OS 大概率不复现。

    返回：{first_year, n_years, top_year, top_share, ex_top_ret, late_start, fragile}
      top_share   = max|pnl_y| / sum|pnl_y|      （>0.5 ⇒ 单年主导）
      ex_top_ret  = 剔除 top_year 后的年均收益
      late_start  = 首个有持仓年份比回测起点晚 ≥2 年
      fragile     = late_start or n_years<6 or top_share>0.5 or ex_top_ret<=0
    """
    import asyncio
    sys.path.insert(0, os.path.join(ROOT, "world-quant-brain-mcp"))
    from brain_api import brain_client

    async def _go():
        await brain_client.ensure_authenticated()
        return await _api_get_json(brain_client, f"/alphas/{alpha_id}/recordsets/yearly-stats",
                                   tries=2, base_sleep=1.0)

    try:
        j = asyncio.run(_go())
    except Exception:
        return None
    recs = (j or {}).get("records") or []
    if not recs:
        return None
    # 端点的 records 是**数组**（按 schema.properties 顺序），不是 dict —— 两种都兼容
    props = [x.get("name") for x in ((j or {}).get("schema") or {}).get("properties") or []]
    idx = {n: i for i, n in enumerate(props)} or {
        "year": 0, "pnl": 1, "longCount": 3, "shortCount": 4, "returns": 7}
    rows = []
    for r in recs:
        try:
            def g(key, default=0.0):
                if isinstance(r, dict):
                    v = r.get(key)
                else:
                    i = idx.get(key)
                    v = r[i] if i is not None and i < len(r) else None
                return default if v is None else v
            rows.append({"year": int(g("year")), "pnl": float(g("pnl")),
                         "ret": float(g("returns")),
                         "pos": float(g("longCount")) + float(g("shortCount"))})
        except (TypeError, ValueError):
            continue
    live = [r for r in rows if r["pos"] > 0]
    if not live:
        return None
    tot_abs = sum(abs(r["pnl"]) for r in live) or 1.0
    top = max(live, key=lambda r: abs(r["pnl"]))
    ex = [r for r in live if r is not top]
    ex_ret = sum(r["ret"] for r in ex) / len(ex) if ex else 0.0
    # 近期断裂（2026-10-23：predictive_starmine 教训）——历史 10 年全正，但 2022 −0.72 / 2023 −0.81。
    # 「样本健康」不等于「现在还有效」，必须单独把它标出来，否则 fragile 会漏掉「正在死」的族。
    last2 = sorted(live, key=lambda r: r["year"])[-2:]
    recent_break = bool(len(last2) == 2 and sum(r["ret"] for r in last2) <= 0)
    first_y = min(r["year"] for r in live)
    start_y = min(r["year"] for r in rows)
    return {
        "first_year": first_y, "start_year": start_y, "n_years": len(live),
        "top_year": top["year"], "top_share": round(abs(top["pnl"]) / tot_abs, 3),
        "ex_top_ret": round(ex_ret, 4),
        "late_start": (first_y - start_y) >= 2,
        "recent_break": recent_break,
        "last2_ret": round(sum(r["ret"] for r in last2), 4) if last2 else None,
        "fragile": bool((first_y - start_y) >= 2 or len(live) < 6
                        or abs(top["pnl"]) / tot_abs > 0.5 or ex_ret <= 0
                        or recent_break),
    }


def fetch_codes(alpha_ids):
    """按 alpha id 取回表达式（用于阶段 2）。"""
    import asyncio
    sys.path.insert(0, os.path.join(ROOT, "world-quant-brain-mcp"))
    from brain_api import brain_client

    async def _all():
        await brain_client.ensure_authenticated()
        out = {}
        for aid in alpha_ids:
            try:
                j = await _api_get_json(brain_client, f"/alphas/{aid}", tries=2, base_sleep=1.0)
                out[aid] = (j.get("regular") or {}).get("code") or ""
            except Exception:
                pass
        return out

    return asyncio.run(_all())
