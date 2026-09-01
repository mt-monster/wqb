# -*- coding: utf-8 -*-
"""提交 mLjGRm02（IND / TOP500 / d1 / STATISTICAL / decay6）。

选型依据：Xg73mNda(1.79/1.28) 已提交但指标弱；未提交的 mLjGRm02(3.70/3.19) 与
P07Ra2zJ(3.18/2.62) 的 CONCENTRATED_WEIGHT 均为 PASS，其中 mLjGRm02 指标最强，
LADDER 3.05(限2.02)、ROBUST 1.22(限1)、SELF 0.5965 / PROD 0.5963 双闸余量 >=0.10。

与同族被拦的 3qlKQ1qX 唯一差别：本颗 A 项为 rank(ts_mean(diff14, 10))（带平滑），
3qlKQ1qX 为 rank(diff14)（瞬时）-> 瞬时构造触发 CONCENTRATED_WEIGHT FAIL。
"""
import asyncio
import json
import sys
from pathlib import Path

WQ_ROOT = Path(r"D:\coding\traeCN_project\wqb")
sys.path.insert(0, str(WQ_ROOT / "world-quant-brain-mcp"))
sys.path.insert(0, str(WQ_ROOT / "src"))

AID = "mLjGRm02"
OUT = WQ_ROOT / "research-data" / "submit_mLjGRm02_result.json"

QUOTA_GATES = {"REGULAR_SUBMISSION", "SUPER_SUBMISSION"}

DESC = (
    "This India alpha pairs a short horizon analyst revision signal with a short term overreaction "
    "correction, and the way each leg is smoothed is a deliberate part of the construction rather "
    "than a cosmetic choice. The dominant leg carries sixty percent of the weight. It first takes the "
    "net analyst revision balance over the trailing fourteen days, measured as recommendation "
    "upgrades minus downgrades, then averages that balance over ten trading days, and finally ranks "
    "the smoothed value cross sectionally. A two week revision window is shorter than the one month "
    "windows usually used for revision signals, which keeps the measure closer to the marginal change "
    "in analyst opinion rather than a stale consensus level. The ten day averaging matters for two "
    "separate reasons. First, raw revision counts are sparse and lumpy in this market, so single day "
    "counts are noisy and averaging removes that noise while keeping the signal responsive. Second, "
    "averaging before ranking spreads the resulting scores more evenly across names instead of "
    "piling extreme scores onto the handful of stocks that happen to attract clustered revision "
    "activity, which in turn keeps the portfolio weights from concentrating in a few positions. The "
    "second leg contributes forty percent and takes the negative cross sectional rank of the ten day "
    "average residualized return, where the residual is what remains after removing the return "
    "explained by the broad universe factor structure. Fading that residual captures the tendency of "
    "idiosyncratic gains accumulated over roughly two weeks to partially retrace. Because the two "
    "legs draw on different information sets, the aggregate is neither a pure momentum nor a pure "
    "reversal bet: the revision leg supplies the directional view while the residual leg trims "
    "exposure to names whose price has already moved ahead of the revision news."
)


def isd_of(d):
    return d.get("is") or {}


def extract_ladder(isd):
    for c in (isd.get("checks") or []):
        if c.get("name") == "IS_LADDER_SHARPE":
            return c.get("value")
    return None


def platform_payload(d):
    isd = isd_of(d)
    st = d.get("settings") or {}
    raw = d.get("regular")
    expr = raw.get("code") if isinstance(raw, dict) else (raw or d.get("expression") or "")
    return {
        "alpha_id": d.get("id"),
        "region": isd.get("region") or st.get("region"),
        "expression": expr,
        "sharpe": isd.get("sharpe"), "fitness": isd.get("fitness"),
        "turnover": isd.get("turnover"), "returns": isd.get("returns"),
        "two_year_sharpe": None,
        "is_ladder_sharpe": extract_ladder(isd),
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

    result = {"alpha_id": AID}

    d0 = await brain.get_alpha_details(AID)
    if not d0:
        print("[ERROR] 详情为空")
        return
    print(f"[diag] status={d0.get('status')} stage={d0.get('stage')} type={d0.get('type')}")
    isd = isd_of(d0)
    print(f"[diag] sharpe={isd.get('sharpe')} fit={isd.get('fitness')} to={isd.get('turnover')}")

    # 写描述
    await brain.set_alpha_properties(AID, descriptions=DESC)
    d = await brain.get_alpha_details(AID)
    raw = d.get("regular")
    cur = raw.get("description") if isinstance(raw, dict) else None
    dl = len(cur or "")
    print(f"[desc] len={dl}")
    result["desc_len"] = dl
    if dl < 100:
        print("[ABORT] 描述 <100 字符")
        result["aborted"] = "desc_too_short"
        OUT.parent.mkdir(parents=True, exist_ok=True)
        OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
        return

    # submit#1
    v1 = await brain.submit_alpha(AID)
    print(f"\n[submit#1] success={v1.get('success')} code={v1.get('status_code')} "
          f"reason={v1.get('reason')}")
    for c in (v1.get("checks") or []):
        print(f"    {c.get('name')}={c.get('value')} (limit={c.get('limit')}) -> {c.get('result')}")
    result["submit1"] = {"success": v1.get("success"), "status_code": v1.get("status_code"),
                         "reason": v1.get("reason"), "checks": v1.get("checks")}

    checks1 = {c.get("name"): c for c in (v1.get("checks") or [])}
    quota_blocked = [n for n, c in checks1.items()
                     if n in QUOTA_GATES and c.get("result") == "FAIL"]
    if quota_blocked:
        print(f"[STOP] 配额闸门失败 {quota_blocked}")
        result["quota_blocked"] = quota_blocked
        OUT.parent.mkdir(parents=True, exist_ok=True)
        OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
        return

    hard_blocked = [n for n, c in checks1.items()
                    if c.get("result") == "FAIL" and n not in QUOTA_GATES]
    if hard_blocked:
        print(f"[HARD-GATE] 硬闸失败 {hard_blocked}（零成本）")
        result["hard_blocked"] = hard_blocked

    # submit#2 verdict
    await asyncio.sleep(20)
    v2 = await brain.submit_alpha(AID)
    print(f"\n[submit#2] success={v2.get('success')} code={v2.get('status_code')} "
          f"reason={v2.get('reason')}")
    for c in (v2.get("checks") or []):
        print(f"    {c.get('name')}={c.get('value')} (limit={c.get('limit')}) -> {c.get('result')}")
    result["submit2"] = {"success": v2.get("success"), "status_code": v2.get("status_code"),
                         "reason": v2.get("reason"), "checks": v2.get("checks")}

    # 轮询 OS
    flipped = False
    if v2.get("success"):
        for i in range(8):
            await asyncio.sleep(30)
            dd = await brain.get_alpha_details(AID)
            print(f"    [poll{i+1}] stage={dd.get('stage')} status={dd.get('status')}")
            if dd.get("stage") == "OS":
                flipped = True
                print(f"    >>> {AID} FLIPPED TO OS <<<")
                break
    result["flipped_os"] = flipped

    payload = await writeback(brain, AID)
    result["payload"] = payload

    if v2.get("success"):
        from wqb.store.campaign import CampaignStore
        store = CampaignStore(str(WQ_ROOT / "data" / "wqb.db"))
        try:
            store.record_submission(
                alpha_id=AID,
                region=(payload or {}).get("region"),
                submission_type="REGULAR",
                status="ACTIVE",
                verdict=result["submit2"],
                quota_used=1,
            )
            print(f"  [ledger] {AID} recorded")
            result["ledger"] = True
        except Exception as e:
            print(f"  [ledger] FAILED {e}")
            result["ledger"] = str(e)
        store.close()

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n[saved] {OUT}")
    print(f"\n[RESULT] submit1={result['submit1']['success']} "
          f"submit2={result['submit2']['success']} os={flipped} ledger={result.get('ledger')}")


if __name__ == "__main__":
    asyncio.run(main())
