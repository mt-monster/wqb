#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""配额重置后自动提交队列（2026-09-01 12:00 GMT+8 开闸）。

队列（6 颗，成功 4 颗即停 = 当日 REGULAR 配额用满）：
  1. RR7OWQKd  IND 情绪+残差反转   (3.32/2.81, P 0.6884/S 0.5518)
  2. P07Ra2zJ  IND 观点偏移+残差   (3.18/2.62, P 0.5831/S 0.5831)
  3. 58lEQMo1  MEA 分析师上调广度   (1.87/1.89, P 0.6925/S 0.6128)
  4. qMjLYVVP  MEA 质量×去杠杆     (1.74/1.72, P 0.5791/S 0.4508)
  5. 1YzOz8ZM  GLB 微观反转        (2.17/1.61, P 0.628/S≈0)
  6. 0mwVnbkG  IND 残差+成长情绪   (2.45/1.87, P 0.5895/S 0.5895)

纪律（沿用已验证流程）：
  - 每颗提交前重测**新鲜平台 PROD 闸**（refresh=True；PROD 是 SELF 的超集上界，
    自家新 OS 也进 production pool，故 PROD<0.7 ⇒ SELF<0.7）
  - 描述 PATCH ≥100 字并回读校验（<100 字会被静默丢弃）
  - 硬闸 FAIL 零成本 → 记录后继续下一颗；配额 FAIL → 等待重试（重置传播延迟）
  - 断点续跑：结果增量落盘，重启跳过已决候选
  - 成功后平台详情回写 alphas + submission_ledger

用法：
    python _submit_queue_20260901.py                # 等到 RESET_AT 后执行
    QUEUE_NOW=1 python ...                          # 跳过等待立即执行
    QUEUE_RESET_AT="2026-09-01T04:00:20+00:00" ...  # 自定义开闸时间
"""
import asyncio
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

WQ_ROOT = Path(r"D:\coding\traeCN_project\wqb")
sys.path.insert(0, str(WQ_ROOT / "world-quant-brain-mcp"))
sys.path.insert(0, str(WQ_ROOT / "src"))

OUT = WQ_ROOT / "research-data" / "submit_queue_20260901.json"

RESET_AT = os.environ.get(
    "QUEUE_RESET_AT", "2026-09-01T04:00:20+00:00")  # 12:00:20 GMT+8
QUEUE_NOW = os.environ.get("QUEUE_NOW") == "1"
MAX_SUCCESS = 4

QUOTA_GATES = {"REGULAR_SUBMISSION", "SUPER_SUBMISSION"}

DESCS = {
    "RR7OWQKd": (
        "Idea: Blend short-horizon news sentiment with reversal of stock-specific "
        "residual returns in the India TOP500 universe.\n\n"
        "Rationale for data used: anl46_sentiment captures aggregate sentiment that "
        "tends to lead subsequent drift, while residualized_return_india_top500_equity "
        "strips market and sector moves so the reversal reflects stock-specific "
        "overreaction rather than beta.\n\n"
        "Rationale for operators used: ts_mean(...,10) smooths both legs to stabilize "
        "weights and avoid concentration; rank makes the legs comparable before the "
        "0.4/0.6 blend, and the residual-return leg enters negatively as a reversal."
    ),
    "P07Ra2zJ": (
        "Idea: Fade recent negative analyst opinion shifts combined with reversal of "
        "residual returns in India TOP500.\n\n"
        "Rationale for data used: analyst_opinion_avg_shift_30d_short measures "
        "short-term changes in average analyst opinion, a slow-moving anchor; "
        "residualized_return_india_top500_equity isolates stock-specific overreaction.\n\n"
        "Rationale for operators used: ts_mean(...,10) on both legs prevents "
        "concentrated weights; both legs enter negatively (downgrades short, "
        "overreaction short) and are ranked then blended 0.6/0.4."
    ),
    "58lEQMo1": (
        "Idea: Rank MEA TOP400 stocks by the breadth of analyst upgrades across price "
        "targets, earnings estimates, dividends, plus operating cash-flow quality.\n\n"
        "Rationale for data used: four-week price-target raises minus lowers, one-week "
        "net-income upward revisions minus downward revisions, one-month dividend "
        "raises minus lowers capture breadth of improving expectations; operating cash "
        "flow over total assets adds an accrual-quality anchor.\n\n"
        "Rationale for operators used: vec_avg aggregates vector fields across "
        "analysts, subtract forms net breadth, ts_backfill fills sparse reports, rank "
        "equalizes the four legs blended at 0.35/0.35/0.15/0.15."
    ),
    "qMjLYVVP": (
        "Idea: Quality reinforced by deleveraging: favor MEA stocks with high retained "
        "earnings relative to common equity that are simultaneously reducing current "
        "liabilities.\n\n"
        "Rationale for data used: retained earnings to common equity proxies "
        "accumulated profitability and balance-sheet quality; the one-year standardized "
        "change in current liabilities captures improving short-term solvency.\n\n"
        "Rationale for operators used: vec_avg aggregates the vector fundamentals, "
        "ts_zscore(...,252) standardizes the liability trend over a full year, the "
        "negative sign rewards deleveraging, and the product requires both quality and "
        "improvement to score high."
    ),
    "1YzOz8ZM": (
        "Idea: Industry-relative reversal of end-of-day order-flow pressure in the GLB "
        "minimum-volatility universe.\n\n"
        "Rationale for data used: mean_last_trade_price_return_30m_pre_close_2 measures "
        "the average last-30-minute pre-close price return, a micro-structure signal "
        "reflecting late-day buying or selling pressure that tends to mean-revert.\n\n"
        "Rationale for operators used: ts_backfill(...,66) fills sparse trading gaps, "
        "ts_decay_linear(...,34) smooths the signal to control turnover, the negative "
        "sign implements reversal, and group_zscore by industry strips industry-wide "
        "flows."
    ),
    "0mwVnbkG": (
        "Idea: Combine reversal of stock-specific residual returns with "
        "growth-weighted news sentiment in India TOP500.\n\n"
        "Rationale for data used: residualized_return_india_top500_equity isolates "
        "stock-specific overreaction; oth696_growthweighted_sentiment_score weights "
        "news sentiment by growth relevance, capturing attention-driven drift.\n\n"
        "Rationale for operators used: ts_mean(...,10) smooths the reversal leg and "
        "ts_backfill(...,66) fills sentiment gaps; both legs are ranked before the "
        "0.6/0.4 blend with the residual leg entering negatively."
    ),
}

QUEUE = ["RR7OWQKd", "P07Ra2zJ", "58lEQMo1", "qMjLYVVP", "1YzOz8ZM", "0mwVnbkG"]


def load_ckpt():
    if OUT.exists():
        return json.load(open(OUT, encoding="utf-8"))
    return {"results": {}, "successes": 0, "started_at": datetime.now(timezone.utc).isoformat()}


def save_ckpt(ck):
    tmp = str(OUT) + ".tmp"
    json.dump(ck, open(tmp, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    os.replace(tmp, OUT)


def checks_dict(v):
    return {c.get("name"): c for c in (v.get("checks") or [])}


def extract_ladder(isd):
    for c in (isd.get("checks") or []):
        if c.get("name") == "IS_LADDER_SHARPE":
            return c.get("value"), c.get("limit")
    return None, None


def platform_payload(d):
    isd = d.get("is") or {}
    st = d.get("settings") or {}
    ladder_val, ladder_limit = extract_ladder(isd)
    raw = d.get("regular")
    return {
        "alpha_id": d.get("id"),
        "region": isd.get("region") or st.get("region"),
        "expression": (raw.get("code") if isinstance(raw, dict) else raw) or "",
        "sharpe": isd.get("sharpe"), "fitness": isd.get("fitness"),
        "turnover": isd.get("turnover"), "two_year_sharpe": None,
        "is_ladder_sharpe": ladder_val,
        "prod_correlation": isd.get("prodCorrelation") or d.get("prod_correlation"),
        "self_correlation": isd.get("selfCorrelation") or d.get("self_correlation"),
        "platform_status": d.get("status"), "stage": d.get("stage"),
        "alpha_type": d.get("type"), "date_submitted": d.get("dateSubmitted"),
        "universe": st.get("universe"), "delay": st.get("delay"),
        "neutralization": st.get("neutralization"), "_ladder_limit": ladder_limit,
    }


async def writeback(brain, aid, row):
    from wqb.store.campaign import CampaignStore
    d = await brain.get_alpha_details(aid)
    if not d:
        print(f"  [writeback] {aid}: 详情为空，跳过", flush=True)
        return None
    payload = platform_payload(d)
    store = CampaignStore(str(WQ_ROOT / "data" / "wqb.db"))
    try:
        store.upsert_alpha_from_platform(payload)
        print(f"  [writeback] {aid}: alphas OK status={payload['platform_status']}", flush=True)
    except Exception as e:
        print(f"  [writeback] {aid}: alphas FAILED {e}", flush=True)
    if row.get("submitted_ok"):
        try:
            store.record_submission(
                alpha_id=aid, region=payload.get("region"),
                submission_type="REGULAR", status="ACTIVE",
                verdict=row.get("submit2") or row.get("submit1"), quota_used=1)
            row["ledger"] = True
            print(f"  [ledger] {aid} recorded", flush=True)
        except Exception as e:
            row["ledger"] = str(e)
            print(f"  [ledger] FAILED {e}", flush=True)
    store.close()
    return payload


async def precheck_prod(brain, aid):
    """新鲜平台 PROD 闸（refresh=True，含自家新 OS 的超集上界）。"""
    p = await brain.check_correlation(aid, correlation_type="production",
                                      threshold=0.7, refresh=True)
    pc = (p.get("checks") or {}).get("production") or {}
    return pc.get("max_correlation"), pc.get("passes_check")


async def ensure_description(brain, aid):
    d = await brain.get_alpha_details(aid)
    raw = (d or {}).get("regular") or {}
    cur = raw.get("description") if isinstance(raw, dict) else None
    if isinstance(cur, str) and len(cur.strip()) >= 100:
        return True, len(cur)
    desc = DESCS.get(aid)
    if not desc:
        return False, 0
    await brain.set_alpha_properties(aid, descriptions=desc)
    d2 = await brain.get_alpha_details(aid)
    raw2 = (d2 or {}).get("regular") or {}
    cur2 = raw2.get("description") if isinstance(raw2, dict) else None
    ok = isinstance(cur2, str) and len(cur2.strip()) >= 100
    return ok, (len(cur2) if isinstance(cur2, str) else 0)


async def process(brain, aid, row):
    # 0) 状态
    d0 = await brain.get_alpha_details(aid)
    if not d0 or d0.get("status") != "UNSUBMITTED":
        row["verdict"] = f"skip_status={d0.get('status') if d0 else 'NOT_FOUND'}"
        print(f"  [skip] {aid} status={row['verdict']}", flush=True)
        return
    # 1) 新鲜 PROD 闸
    try:
        pc, ok = await precheck_prod(brain, aid)
    except Exception as e:
        row["verdict"] = f"precheck_error={type(e).__name__}"
        print(f"  [precheck-ERR] {aid}: {e}", flush=True)
        return
    row["precheck_prod"] = pc
    row["precheck_pass"] = ok
    print(f"  [precheck] {aid} PROD={pc} pass={ok}", flush=True)
    if ok is not True:
        row["verdict"] = f"prod_gate_fail={pc}"
        return
    # 2) 描述
    desc_ok, desc_len = await ensure_description(brain, aid)
    row["desc_len"] = desc_len
    if not desc_ok:
        row["verdict"] = "description_patch_failed"
        print(f"  [desc] {aid} PATCH/校验失败，跳过提交", flush=True)
        return
    print(f"  [desc] {aid} len={desc_len} OK", flush=True)
    # 3) submit（含配额重试）
    accepted_async = False
    for att in range(6):
        v1 = await brain.submit_alpha(aid)
        c1 = checks_dict(v1)
        row["submit1"] = {"success": v1.get("success"),
                          "status_code": v1.get("status_code"),
                          "reason": v1.get("reason"), "checks": v1.get("checks")}
        print(f"  [submit#1] {aid} code={v1.get('status_code')} reason={v1.get('reason')}", flush=True)
        for c in (v1.get("checks") or []):
            print(f"      {c.get('name')}={c.get('value')} (limit={c.get('limit')}) -> {c.get('result')}", flush=True)
        quota_blocked = [n for n, c in c1.items()
                         if n in QUOTA_GATES and c.get("result") == "FAIL"]
        if quota_blocked:
            wait_s = 300
            print(f"  [quota] {quota_blocked} 未放行，{wait_s}s 后重试（{att+1}/6）", flush=True)
            await asyncio.sleep(wait_s)
            continue
        hard_blocked = [n for n, c in c1.items()
                        if c.get("result") == "FAIL" and n not in QUOTA_GATES]
        if hard_blocked:
            row["verdict"] = f"hard_gate_fail={hard_blocked}"
            print(f"  [hard-gate] {aid} {hard_blocked}（零成本）", flush=True)
            return
        if v1.get("status_code") == 201:
            accepted_async = True
        break
    else:
        row["verdict"] = "quota_never_released"
        return
    # 4) 201 异步受理 → 直接轮询 OS（RR7OWQKd 实证：40s 内翻 OS，submit#2 会 403 已提交）
    if accepted_async:
        for i in range(8):
            await asyncio.sleep(20)
            dd = await brain.get_alpha_details(aid)
            print(f"      [async-poll{i+1}] stage={dd.get('stage')} status={dd.get('status')}", flush=True)
            if dd.get("stage") == "OS":
                row["flipped_os"] = True
                row["submitted_ok"] = True
                print(f"  >>> {aid} FLIPPED TO OS <<<", flush=True)
                payload = await writeback(brain, aid, row)
                row["payload"] = payload
                row["verdict"] = "submitted"
                return
        print(f"  [async] {aid} 轮询未翻 OS，尝试 submit#2 verdict", flush=True)
    # 5) submit#2 verdict
    await asyncio.sleep(10)
    v2 = await brain.submit_alpha(aid)
    row["submit2"] = {"success": v2.get("success"),
                      "status_code": v2.get("status_code"),
                      "reason": v2.get("reason"), "checks": v2.get("checks")}
    print(f"  [submit#2] {aid} success={v2.get('success')} code={v2.get('status_code')}", flush=True)
    row["submitted_ok"] = bool(v2.get("success"))
    if (not row["submitted_ok"]) and v2.get("status_code") == 403:
        # 可能是"已提交"拒绝（异步受理迟到）→ 以平台状态为准
        dd = await brain.get_alpha_details(aid)
        if dd.get("status") == "ACTIVE" and dd.get("stage") == "OS":
            row["submitted_ok"] = True
            row["flipped_os"] = True
            print(f"  [403-已提交] {aid} 平台已 ACTIVE/OS，按成功处理", flush=True)
    # 6) 轮询 OS
    if row["submitted_ok"] and not row.get("flipped_os"):
        for i in range(6):
            await asyncio.sleep(30)
            dd = await brain.get_alpha_details(aid)
            print(f"      [poll{i+1}] stage={dd.get('stage')} status={dd.get('status')}", flush=True)
            if dd.get("stage") == "OS":
                row["flipped_os"] = True
                print(f"  >>> {aid} FLIPPED TO OS <<<", flush=True)
                break
    # 7) 回写
    payload = await writeback(brain, aid, row)
    row["payload"] = payload
    row["verdict"] = "submitted" if row["submitted_ok"] else "submit2_unconfirmed"


async def main():
    from brain_api import BrainApiClient

    ck = load_ckpt()
    done_ids = {k for k, v in ck["results"].items()
                if v.get("verdict") in ("submitted",)}
    queue = [a for a in QUEUE if a not in ck["results"] or not ck["results"][a].get("verdict")]
    print(f"[INFO] 队列 {QUEUE}", flush=True)
    print(f"[INFO] 已决 {sorted(ck['results'])}，本轮 {queue}，已有成功 {ck['successes']}", flush=True)

    reset = datetime.fromisoformat(RESET_AT)
    now = datetime.now(timezone.utc)
    if not QUEUE_NOW and now < reset:
        wait = (reset - now).total_seconds()
        print(f"[INFO] 等待配额重置：{(reset - now).total_seconds()/60:.1f} 分钟"
              f"（{RESET_AT} = 12:00 GMT+8）", flush=True)
        await asyncio.sleep(wait)
    print(f"[INFO] 开闸，开始执行队列 {datetime.now(timezone.utc).isoformat()}", flush=True)

    brain = BrainApiClient()
    await brain.ensure_authenticated()

    for aid in queue:
        if ck["successes"] >= MAX_SUCCESS:
            print(f"[INFO] 已成功 {ck['successes']} 颗 = 当日配额，停止", flush=True)
            break
        print(f"\n{'='*60}\n=== {aid} ===\n{'='*60}", flush=True)
        row = ck["results"].setdefault(aid, {})
        try:
            await process(brain, aid, row)
        except Exception as e:
            row["verdict"] = f"error={type(e).__name__}"
            row["error"] = str(e)[:300]
            print(f"  [ERR] {aid}: {e}", flush=True)
        if row.get("submitted_ok"):
            ck["successes"] += 1
        save_ckpt(ck)

    save_ckpt(ck)
    print(f"\n[done] 成功 {ck['successes']}/{MAX_SUCCESS}", flush=True)
    for aid, r in ck["results"].items():
        print(f"  {aid}: {r.get('verdict')} prod={r.get('precheck_prod')} "
              f"os={r.get('flipped_os')} ledger={r.get('ledger')}", flush=True)


if __name__ == "__main__":
    asyncio.run(main())
