#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""build_gate_prior_from_inventory.py — 用账户历史 alpha 库存反哺 GEM 先验。

背景（2026-09-08）：
  `wins` / `dead_ends` / `skeleton_field_matrix` 的样本源是 campaign registry
  （registry_empirical 数百行）。而账户已有 **三万条以上**已回测 IS alpha，
  其中约 11% 通过 IS 硬闸——这是一份现成的、大两个数量级的监督样本，
  且同账户、同设置习惯，外推风险低。本工具把它变成可消费的先验。

产出两样东西：
  1. **候选池**（`--emit-candidates`）：failed_ra_count==0 且 type==REGULAR
     且 status==UNSUBMITTED 且有表达式的 alpha —— 直接可进 select_ra_basket.py。
  2. **条件过闸率先验**（`--write-priors`）：按 region × (中性化 / universe /
     算子数分箱 / decay / 字段族) 统计过闸率，写入 ledger `region_kb.gate_priors`，
     由 assemble-priors 并入 priors，最终由 economic_priors.compact_priors_text 渲染进
     GEM prompt。

平台限制（实测，见 ledger GLOBAL/API-LIMITS-user-alphas-pagination-20260907）：
  - `offset > 1000` 返回 HTTP 400 且响应体是 **list 不是 dict**
    （["Cannot display more than the first 1,000 alphas..."]），直接 j.get() 会抛
    AttributeError。故必须按 settings.region 分区，每区最多翻 1000 条。
  - 响应里的 `count` 封顶 10000，不是真实总数。
  - 真正的服务端过滤只有 settings.region / dateCreated> / dateCreated< / order /
    stage / hidden / type。`region` 与 `status` 在 MCP 包装层是客户端过滤，
    写进 params 会被平台忽略——本工具直接打平台端点，故用 settings.region。

用法:
    python tools/build_gate_prior_from_inventory.py --regions all \
        --emit-candidates candidates.json --write-priors
    python tools/build_gate_prior_from_inventory.py --regions KOR,IND --per-region 500

运行环境: MCP venv（$WQ_PY / world-quant-brain-mcp/.venv）。
"""
from __future__ import annotations

import argparse
import asyncio
import json
import os
import re
import sqlite3
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "world-quant-brain-mcp"))
DB = REPO_ROOT / "data" / "wqb.db"

PAGE = 100
OFFSET_CAP = 1000          # 平台硬限
SLEEP = 0.6
DEFAULT_REGIONS = ["HKG", "CHN", "GBR", "ASI", "KOR", "IND", "GLB", "EUR", "USA"]

#: 平台已禁区域——既不新挖也不提交存量（见 ledger MEA/region_disabled）
BANNED_REGIONS = {"MEA"}

#: RA 资格门计数的 check 名集合。与 world-quant-brain-mcp/mcp_core.py::_RA_CHECK_NAMES
#: 保持一致；`.WITH_RATIO` 变体是 2026-09-08 补入的（平台以 FAIL 拦 REGULAR 提交）。
RA_CHECK_NAMES = frozenset([
    "HIGH_TURNOVER", "LOW_TURNOVER", "LOW_FITNESS", "LOW_RETURNS", "LOW_SHARPE",
    "LOW_GLB_AMER_SHARPE", "LOW_GLB_APAC_SHARPE", "LOW_GLB_EMEA_SHARPE",
    "LOW_ASI_JPN_SHARPE", "IS_LADDER_SHARPE", "LOW_2Y_SHARPE",
    "LOW_SUB_UNIVERSE_SHARPE", "LOW_ROBUST_UNIVERSE_SHARPE",
    "LOW_ROBUST_UNIVERSE_SHARPE.WITH_RATIO",
    "LOW_AFTER_COST_ILLIQUID_UNIVERSE_SHARPE",
    "LOW_INVESTABILITY_CONSTRAINED_SHARPE",
    "LOW_ROBUST_UNIVERSE_RETURNS", "CONCENTRATED_WEIGHT",
])
RA_2Y_NAMES = ("LOW_2Y_SHARPE", "IS_LADDER_SHARPE")

OP_CALL_RE = re.compile(r"\b([a-z][a-z0-9_]{2,})\s*\(")
FIELD_TOKEN_RE = re.compile(r"\b([a-z][a-z0-9_]{3,})\b")

#: 算子名（用于把字段 token 从表达式里剥离）
_KNOWN_OPS = set("""
rank add multiply subtract divide group_rank group_zscore group_neutralize group_mean group_sum
group_count group_scale group_std_dev group_backfill ts_mean ts_delta ts_zscore ts_rank ts_backfill
ts_decay_linear ts_std_dev ts_sum ts_max ts_min ts_corr ts_covariance ts_regression ts_av_diff
ts_arg_max ts_arg_min ts_product ts_quantile ts_count_nans ts_scale ts_step ts_returns ts_ir
ts_delay ts_kurtosis ts_max_diff vec_avg vec_sum vec_max vec_min vec_stddev vec_count vec_range
winsorize scale normalize signed_power quantile power reverse zscore abs log sign sqrt inverse
densify pasteurize hump kth_element trade_when if_else bucket greater less equal and or not is_nan
not_equal less_equal greater_equal max min days_from_last_change last_diff_value
industry sector subindustry market country exchange std range rettype driver
returns close open high low volume vwap cap adv20 sharesout
""".split())


def ra_bad(result) -> bool:
    """WebDataScope 口径：result 既非 PASS 也非 PENDING 即计入失败（WARNING/ERROR 都算）。"""
    return result != "PASS" and result != "PENDING"


def screen_checks(alpha: dict):
    """返回 (failed_ra_count, 失败项名列表, 额外指标 dict, 金字塔 dict)。"""
    n, names, extra, pyr = 0, [], {}, None
    for c in (alpha.get("is") or {}).get("checks") or []:
        if not isinstance(c, dict):
            continue
        nm, res, val = c.get("name"), c.get("result"), c.get("value")
        if nm == "MATCHES_PYRAMID":
            pyr = {"effective": c.get("effective"),
                   "list": [p.get("name") for p in (c.get("pyramids") or []) if isinstance(p, dict)]}
        if nm in RA_2Y_NAMES and val is not None:
            extra["two_year_sharpe"] = val
        elif nm == "LOW_SUB_UNIVERSE_SHARPE" and val is not None:
            extra["sub_universe_sharpe"] = val
        elif nm == "LOW_ROBUST_UNIVERSE_SHARPE" and val is not None:
            extra["robust_universe_sharpe"] = val
        if nm in RA_CHECK_NAMES and ra_bad(res):
            n += 1
            names.append(nm)
    return n, names, extra, pyr


def field_family(code: str) -> str:
    """把表达式归到一个字段族：取首个非算子 token 的字母前缀（mdl39_x -> mdl，
    ep_yield_pct_smest_fy1_3 -> ep）。用于统计「哪些字段族过闸率高」。"""
    for t in FIELD_TOKEN_RE.findall(code or ""):
        if t in _KNOWN_OPS or t.isdigit():
            continue
        m = re.match(r"^([a-z]+)", t)
        return m.group(1) if m else t
    return "?"


def op_count(code: str) -> int:
    return len(OP_CALL_RE.findall(code or ""))


def op_bin(n: int) -> str:
    if n <= 4:
        return "<=4"
    if n <= 8:
        return "5-8"
    return ">8"


async def fetch_region(brain, region: str, per_region: int, verbose=True):
    """翻某区的 IS alpha（order=-is.fitness），最多 per_region 条（受平台 1000 上限约束）。"""
    rows, off = [], 0
    limit = min(per_region, OFFSET_CAP)
    while off < limit:
        page = min(PAGE, limit - off)
        j = None
        for attempt in range(6):
            try:
                r = await brain._request(
                    "GET", f"{brain.base_url}/users/self/alphas",
                    params={"limit": page, "offset": off, "stage": "IS",
                            "settings.region": region, "order": "-is.fitness"})
                if r.status_code == 429:
                    await asyncio.sleep(10)
                    continue
                jj = r.json()
                if not isinstance(jj, dict):
                    # 越过 offset 硬限，或错误体（平台返回 list）
                    j = None
                    break
                j = jj
                break
            except Exception as e:
                if attempt == 5:
                    print(f"  [err] {region} off={off}: {e}", flush=True)
                    break
                await asyncio.sleep(4)
        if j is None:
            break
        arr = j.get("results") or []
        if not arr:
            break
        rows.extend(arr)
        if len(arr) < page:
            break
        off += page
        await asyncio.sleep(SLEEP)
    if verbose:
        print(f"[{region}] 取回 {len(rows)} 条", flush=True)
    return rows


def summarize(records: list) -> dict:
    """按维度统计条件过闸率。records 每项含 passed/neut/universe/decay/opbin/family。"""
    def rate_table(key):
        agg = defaultdict(lambda: [0, 0])   # [过闸数, 总数]
        for r in records:
            k = r.get(key)
            if k in (None, ""):
                continue
            agg[str(k)][1] += 1
            if r["passed"]:
                agg[str(k)][0] += 1
        out = {}
        for k, (p, t) in agg.items():
            if t >= 15:            # 样本太小的格子不进先验，避免噪声当规律
                out[k] = {"rate": round(p / t, 4), "n": t}
        return out

    tables = {
        "by_neutralization": rate_table("neut"),
        "by_universe": rate_table("universe"),
        "by_operator_count": rate_table("opbin"),
        "by_decay": rate_table("decay"),
        "by_field_family": rate_table("family"),
    }
    avoid = []
    for key in ("by_neutralization", "by_field_family", "by_universe"):
        for name, v in tables[key].items():
            if v["rate"] <= 0.02 and v["n"] >= 30:
                avoid.append(f"{key.replace('by_', '')}={name}({v['rate']:.0%}, n={v['n']})")
    return {
        "sample_size": len(records),
        "pass_rate": round(sum(1 for r in records if r["passed"]) / max(len(records), 1), 4),
        **tables,
        "avoid": avoid,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source": "tools/build_gate_prior_from_inventory.py",
    }


def write_priors(region: str, gate_priors: dict, db_path: Path):
    """把 gate_priors 并入 ledger region_kb（不覆盖其余键）。"""
    con = sqlite3.connect(str(db_path))
    try:
        row = con.execute(
            "SELECT value FROM ledger_kv WHERE region=? AND key='region_kb'", (region,)
        ).fetchone()
        kb = json.loads(row[0]) if row and row[0] else {}
        if not isinstance(kb, dict):
            kb = {}
        kb["gate_priors"] = gate_priors
        now = datetime.now().isoformat(timespec="seconds")
        con.execute(
            "INSERT INTO ledger_kv (region, key, value, created_at, updated_at) "
            "VALUES (?,?,?,?,?) "
            "ON CONFLICT(region, key) DO UPDATE SET value=excluded.value, updated_at=excluded.updated_at",
            (region, "region_kb", json.dumps(kb, ensure_ascii=False), now, now))
        con.commit()
    finally:
        con.close()


async def main_async(a):
    from brain_api import BrainApiClient
    regions = (DEFAULT_REGIONS if a.regions.strip().lower() == "all"
               else [x.strip().upper() for x in a.regions.split(",") if x.strip()])
    regions = [r for r in regions if r not in BANNED_REGIONS]
    if not regions:
        raise SystemExit("没有可扫描的区域（MEA 已被平台禁用，自动剔除）")

    brain = BrainApiClient()
    await brain.ensure_authenticated()

    all_candidates, per_region_summary = [], {}
    for reg in regions:
        raw = await fetch_region(brain, reg, a.per_region)
        records = []
        for al in raw:
            code = ((al.get("regular") or {}) or {}).get("code") or ""
            if al.get("type") != "REGULAR" or not code.strip():
                continue    # SuperAlpha / 无表达式，不算 RA
            nfail, fail_names, extra, pyr = screen_checks(al)
            st, isv = al.get("settings") or {}, al.get("is") or {}
            passed = nfail == 0
            records.append({
                "passed": passed,
                "neut": st.get("neutralization"),
                "universe": st.get("universe"),
                "decay": st.get("decay"),
                "opbin": op_bin(op_count(code)),
                "family": field_family(code),
            })
            if passed and al.get("status") == "UNSUBMITTED":
                all_candidates.append({
                    "id": al.get("id"), "region": st.get("region"),
                    "universe": st.get("universe"), "delay": st.get("delay"),
                    "neut": st.get("neutralization"), "decay": st.get("decay"),
                    "trunc": st.get("truncation"),
                    "sharpe": isv.get("sharpe"), "fitness": isv.get("fitness"),
                    "returns": isv.get("returns"), "turnover": isv.get("turnover"),
                    "longCount": isv.get("longCount"), "shortCount": isv.get("shortCount"),
                    "two_year_sharpe": extra.get("two_year_sharpe"),
                    "sub_universe_sharpe": extra.get("sub_universe_sharpe"),
                    "robust_universe_sharpe": extra.get("robust_universe_sharpe"),
                    "pyramids": pyr, "dateCreated": al.get("dateCreated"),
                    "code": code.strip(),
                })
        summ = summarize(records)
        per_region_summary[reg] = summ
        npass = sum(1 for r in records if r["passed"])
        print(f"[{reg}] REGULAR {len(records)} 条 -> 过闸 {npass} "
              f"({npass / max(len(records), 1):.1%})，候选(未提交) "
              f"{sum(1 for c in all_candidates if c['region'] == reg)}", flush=True)
        if a.write_priors:
            write_priors(reg, summ, Path(a.db_path) if a.db_path else DB)
            print(f"      -> 已写 ledger {reg}/region_kb.gate_priors", flush=True)

    if a.emit_candidates:
        Path(a.emit_candidates).write_text(
            json.dumps(all_candidates, ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"\n[候选池] {len(all_candidates)} 条 -> {a.emit_candidates}")
    if a.emit_summary:
        Path(a.emit_summary).write_text(
            json.dumps(per_region_summary, ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"[统计]   -> {a.emit_summary}")

    print("\n=== 各区过闸率 ===")
    for reg, s in sorted(per_region_summary.items(), key=lambda kv: -kv[1]["pass_rate"]):
        print(f"  {reg:4s} {s['pass_rate']:6.1%}  (n={s['sample_size']})")


def main():
    ap = argparse.ArgumentParser(description="用账户历史 alpha 库存反哺 GEM 先验 + 产出候选池")
    ap.add_argument("--regions", default="all", help="all 或逗号分隔（如 KOR,IND）；MEA 自动剔除")
    ap.add_argument("--per-region", type=int, default=OFFSET_CAP,
                    help=f"每区最多翻多少条（平台硬限 {OFFSET_CAP}）")
    ap.add_argument("--emit-candidates", default=None, help="候选池 JSON 输出路径")
    ap.add_argument("--emit-summary", default=None, help="过闸率统计 JSON 输出路径")
    ap.add_argument("--write-priors", action="store_true",
                    help="把过闸率写入 ledger region_kb.gate_priors（供 assemble-priors 消费）")
    ap.add_argument("--db-path", default=None, help="显式指定 wqb.db 路径")
    a = ap.parse_args()
    asyncio.run(main_async(a))


if __name__ == "__main__":
    main()
