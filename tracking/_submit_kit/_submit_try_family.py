# -*- coding: utf-8 -*-
"""按优先级依次试提交：3qlKQ1qX（指标最优） -> Xg73mNda（CONC_WEIGHT=PASS 保底）。

背景：qMja95Q2（同族指标最强 sharpe4.26/fit3.97）提交被 CONCENTRATED_WEIGHT 硬闸拦
（IS 阶段 WARNING -> 提交后 FAIL）。3qlKQ1qX 同为 WARNING，Xg73mNda 为 PASS。
硬闸 FAIL 零成本（不消耗 REGULAR_SUBMISSION 配额），故可安全地逐个试探。

规则：第一个 submit#2 成功的即停（同族只留 1 颗，避免自相残杀 + 省配额）。
"""
import asyncio
import json
import sys
from pathlib import Path

WQ_ROOT = Path(r"D:\coding\traeCN_project\wqb")
sys.path.insert(0, str(WQ_ROOT / "world-quant-brain-mcp"))
sys.path.insert(0, str(WQ_ROOT / "src"))

OUT = WQ_ROOT / "research-data" / "submit_try2_20260901.json"
QUOTA_GATES = {"REGULAR_SUBMISSION", "SUPER_SUBMISSION"}

# 顺序：指标最优优先；成功即停
ORDER = ["3qlKQ1qX", "Xg73mNda"]

DESC = {
    "3qlKQ1qX": (
        "This India alpha blends a short horizon analyst revision signal with a short term "
        "overreaction correction. The dominant leg, weighted at sixty percent, ranks names cross "
        "sectionally on the net analyst revision balance over the trailing fourteen days, measured "
        "as recommendation upgrades minus downgrades. A two week window is deliberately shorter than "
        "the one month windows typically used for revision signals, because in this universe the "
        "revision information is incorporated quickly and a fresher window keeps the signal closer to "
        "the marginal change in analyst opinion rather than a stale consensus level. The second leg "
        "contributes forty percent and takes the negative rank of the ten day average residualized "
        "return, where the residual is computed after removing the return explained by the broad "
        "universe factor structure. Fading that residual captures the tendency of idiosyncratic gains "
        "accumulated over roughly two weeks to partially retrace. Because the two legs operate on "
        "different information sets and different horizons, the combination is not simply a momentum "
        "or a reversal bet: the revision leg supplies the directional view while the residual leg "
        "trims exposure to names whose move has already run ahead of the revision news."
    ),
    "Xg73mNda": (
        "This India alpha is a single, deliberately simple signal built on the net analyst revision "
        "balance. For each stock it takes the difference between the number of recommendation "
        "upgrades and the number of recommendation downgrades over the trailing thirty days, averages "
        "that difference over ten trading days, and then ranks the result cross sectionally. Averaging "
        "before ranking matters: raw revision counts are sparse and lumpy in this market, so smoothing "
        "over ten days removes single day noise while still keeping the signal responsive. The "
        "economic mechanism is post revision price drift. Analyst coverage in this universe is thinner "
        "than in developed markets, so each revision carries relatively more information, and prices "
        "adjust to revisions gradually rather than instantaneously. A net positive upgrade balance "
        "therefore identifies names where the earnings expectation consensus is being revised upward "
        "and where the subsequent drift has not yet fully played out. The cross sectional rank keeps "
        "the signal scale free and prevents a handful of heavily covered names from dominating the "
        "portfolio, which also keeps the resulting position weights well distributed across the "
        "universe."
    ),
}


def isd_of(d):
    return d.get("is") or {}


def extract_ladder(isd):
    for c in (isd.get("checks") or []):
        if c.get("name") == "IS_LADDER_SHARPE":
            return c.get("value"), c.get("limit")
    return None, None


def platform_payload(d):
    isd = isd_of(d)
    st = d.get("settings") or {}
    ladder_val, _ = extract_ladder(isd)
    raw = d.get("regular")
    expr = raw.get("code") if isinstance(raw, dict) else (raw or d.get("expression") or "")
    return {
        "alpha_id": d.get("id"),
        "region": isd.get("region") or st.get("region"),
        "expression": expr,
        "sharpe": isd.get("sharpe"), "fitness": isd.get("fitness"),
        "turnover": isd.get("turnover"), "two_year_sharpe": None,
        "is_ladder_sharpe": ladder_val,
        "prod_correlation": isd.get("prodCorrelation") or d.get("prod_correlation"),
        "self_correlation": isd.get("selfCorrelation") or d.get("self_correlation"),
        "platform_status": d.get("status"), "stage": d.get("stage"),
        "alpha_type": d.get("type"), "date_submitted": d.get("dateSubmitted"),
        "universe": st.get("universe"), "delay": st.get("delay"),
        "neutralization": st.get("neutralization"),
    }


async def writeback(brain, aid):
    from wqb.store.campaign import CampaignStore
    d = await brain.get_alpha_details(aid)
    if not d:
        print(f"  [writeback] {aid}: 详情为空")
        return None
    payload = platform_payload(d)
    store = CampaignStore(str(WQ_ROOT / "data" / "wqb.db"))
    try:
        rid = store.upsert_alpha_from_platform(payload)
        print(f"  [writeback] {aid}: alphas OK (id={rid}) "
              f"status={payload['platform_status']} stage={payload['stage']}")
    except Exception as e:
        print(f"  [writeback] {aid}: FAILED {e}")
    store.close()
    return payload


async def main():
    from brain_api import BrainApiClient
    brain = BrainApiClient()
    await brain.ensure_authenticated()

    results = {}
    submitted_ok = None

    for aid in ORDER:
        print(f"\n{'='*64}\n=== 试提交 {aid} ===\n{'='*64}")
        d0 = await brain.get_alpha_details(aid)
        if not d0:
            print("  [ERROR] 详情为空")
            results[aid] = {"error": "empty details"}
            continue
        isd = isd_of(d0)
        st = d0.get("settings") or {}
        print(f"  [diag] status={d0.get('status')} stage={d0.get('stage')} "
              f"sharpe={isd.get('sharpe')} fit={isd.get('fitness')} to={isd.get('turnover')}")
        print(f"  [diag] {st.get('region')}/{st.get('universe')}/"
              f"{st.get('neutralization')}/d{st.get('delay')}")

        row = {"initial_status": d0.get("status"), "initial_stage": d0.get("stage")}

        if d0.get("status") != "UNSUBMITTED":
            print(f"  [skip] 非 UNSUBMITTED（{d0.get('status')}）")
            row["skipped"] = True
            row["payload"] = await writeback(brain, aid)
            results[aid] = row
            continue

        # 写描述
        await brain.set_alpha_properties(aid, descriptions=DESC[aid])
        d = await brain.get_alpha_details(aid)
        raw = d.get("regular")
        cur = raw.get("description") if isinstance(raw, dict) else None
        dl = len(cur or "")
        print(f"  [desc] len={dl}")
        row["desc_len"] = dl
        if dl < 100:
            print("  [ABORT] 描述 <100 字符")
            row["aborted"] = "desc_too_short"
            results[aid] = row
            continue

        # submit#1
        v1 = await brain.submit_alpha(aid)
        print(f"  [submit#1] success={v1.get('success')} code={v1.get('status_code')} "
              f"reason={v1.get('reason')}")
        for c in (v1.get("checks") or []):
            print(f"      {c.get('name')}={c.get('value')} "
                  f"(limit={c.get('limit')}) -> {c.get('result')}")
        row["submit1"] = {"success": v1.get("success"), "status_code": v1.get("status_code"),
                          "reason": v1.get("reason"), "checks": v1.get("checks")}

        checks1 = {c.get("name"): c for c in (v1.get("checks") or [])}
        quota_blocked = [n for n, c in checks1.items()
                         if n in QUOTA_GATES and c.get("result") == "FAIL"]
        if quota_blocked:
            print(f"  [STOP] 配额闸门失败 {quota_blocked}")
            row["quota_blocked"] = quota_blocked
            results[aid] = row
            break

        hard_blocked = [n for n, c in checks1.items()
                        if c.get("result") == "FAIL" and n not in QUOTA_GATES]
        if hard_blocked:
            print(f"  [HARD-GATE] 硬闸失败 {hard_blocked}（零成本，不消耗配额）")
            row["hard_blocked"] = hard_blocked

        # submit#2 verdict
        await asyncio.sleep(20)
        v2 = await brain.submit_alpha(aid)
        print(f"  [submit#2] success={v2.get('success')} code={v2.get('status_code')} "
              f"reason={v2.get('reason')}")
        for c in (v2.get("checks") or []):
            print(f"      {c.get('name')}={c.get('value')} "
                  f"(limit={c.get('limit')}) -> {c.get('result')}")
        row["submit2"] = {"success": v2.get("success"), "status_code": v2.get("status_code"),
                          "reason": v2.get("reason"), "checks": v2.get("checks")}

        if not v2.get("success"):
            print(f"  [next] {aid} 未通过，尝试下一个候选")
            row["payload"] = await writeback(brain, aid)
            results[aid] = row
            continue

        # 成功 -> 轮询 OS
        flipped = False
        for i in range(8):
            await asyncio.sleep(30)
            dd = await brain.get_alpha_details(aid)
            print(f"      [poll{i+1}] stage={dd.get('stage')} status={dd.get('status')}")
            if dd.get("stage") == "OS":
                flipped = True
                print(f"      >>> {aid} FLIPPED TO OS <<<")
                break
        row["flipped_os"] = flipped

        payload = await writeback(brain, aid)
        row["payload"] = payload

        from wqb.store.campaign import CampaignStore
        store = CampaignStore(str(WQ_ROOT / "data" / "wqb.db"))
        try:
            store.record_submission(
                alpha_id=aid,
                region=(payload or {}).get("region"),
                submission_type="REGULAR",
                status="ACTIVE",
                verdict=row["submit2"],
                quota_used=1,
            )
            print(f"  [ledger] {aid} recorded")
            row["ledger"] = True
        except Exception as e:
            print(f"  [ledger] FAILED {e}")
            row["ledger"] = str(e)
        store.close()

        results[aid] = row
        submitted_ok = aid
        print(f"\n  >>> 已成功提交 {aid}，按同族纪律停止后续候选 <<<")
        break

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps({"order": ORDER, "submitted": submitted_ok,
                               "results": results},
                              ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n[saved] {OUT}")
    print(f"\n[RESULT] submitted={submitted_ok}")
    for aid, r in results.items():
        s2 = r.get("submit2") or {}
        print(f"  {aid}: s1={r.get('submit1', {}).get('success')} s2={s2.get('success')} "
              f"os={r.get('flipped_os')} hard={r.get('hard_blocked')} "
              f"ledger={r.get('ledger')}")


if __name__ == "__main__":
    asyncio.run(main())
