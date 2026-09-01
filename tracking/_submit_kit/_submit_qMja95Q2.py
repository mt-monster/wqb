# -*- coding: utf-8 -*-
"""提交 qMja95Q2（IND / TOP500 / STATISTICAL / d1，analyst 修正 + 短周期残差反转）。

三选一依据（同族 3 颗里最优）：
  qMja95Q2 sharpe 4.26 / fit 3.97 / IS_LADDER 2.97(限2.02) / ROBUST 1.79(限1) / CLUSTER 3.12
  3qlKQ1qX sharpe 3.61 / fit 2.90 / ROBUST 1.04（限1，余 0.04，OS 易挂）
  Xg73mNda sharpe 1.79 / fit 1.28（贴线，且无 ladder）
双闸预检：qMja95Q2 SELF 0.5483 / PROD 0.6317 全 PASS。

闭环：写描述 -> submit#1 -> (配额闸命中即停) -> sleep20 -> submit#2 -> 轮询 OS -> DB 回写+落账
"""
import asyncio
import json
import sys
from pathlib import Path

WQ_ROOT = Path(r"D:\coding\traeCN_project\wqb")
sys.path.insert(0, str(WQ_ROOT / "world-quant-brain-mcp"))
sys.path.insert(0, str(WQ_ROOT / "src"))

AID = "qMja95Q2"
OUT = WQ_ROOT / "research-data" / "submit_qMja95Q2_result.json"

QUOTA_GATES = {"REGULAR_SUBMISSION", "SUPER_SUBMISSION"}

DESC = (
    "This India alpha combines two signals that capture different parts of the return generation "
    "process and are largely orthogonal to each other. The first component, carrying sixty percent "
    "of the weight, ranks stocks cross sectionally by the net analyst revision balance, computed as "
    "the number of recommendation upgrades over the trailing thirty days minus the number of "
    "downgrades over the same window. In the Indian equity market analyst coverage is comparatively "
    "sparse relative to developed markets, so each individual revision carries proportionally more "
    "information, and revisions tend to be followed by a gradual price adjustment rather than an "
    "instantaneous repricing. A positive net upgrade balance therefore identifies names where the "
    "earnings expectation consensus is being revised upward. The second component contributes the "
    "remaining forty percent and takes the negative of the cross sectional rank of the ten day mean "
    "residualized return. Residualized return strips out the exposures that the broad universe factor "
    "structure already explains, so what remains is the idiosyncratic move. Short horizon idiosyncratic "
    "gains in this universe tend to partially retrace, so fading them removes the part of the analyst "
    "signal that has already been reflected in the price. Combining the medium term consensus revision "
    "direction with a short term overreaction correction raises the signal to noise ratio relative to "
    "either leg on its own, and the negative loading on the residual leg means the aggregate position "
    "is not simply a momentum bet on recent winners."
)


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
    ladder_val, ladder_limit = extract_ladder(isd)
    return {
        "alpha_id": d.get("id"),
        "region": isd.get("region") or st.get("region"),
        "expression": (d.get("regular") or {}).get("code")
        if isinstance(d.get("regular"), dict)
        else (d.get("regular") or d.get("expression") or ""),
        "sharpe": isd.get("sharpe"),
        "fitness": isd.get("fitness"),
        "turnover": isd.get("turnover"),
        "two_year_sharpe": None,
        "is_ladder_sharpe": ladder_val,
        "prod_correlation": isd.get("prodCorrelation") or d.get("prod_correlation"),
        "self_correlation": isd.get("selfCorrelation") or d.get("self_correlation"),
        "platform_status": d.get("status"),
        "stage": d.get("stage"),
        "alpha_type": d.get("type"),
        "date_submitted": d.get("dateSubmitted"),
        "universe": st.get("universe"),
        "delay": st.get("delay"),
        "neutralization": st.get("neutralization"),
        "_ladder_limit": ladder_limit,
    }


async def writeback(brain, aid):
    from wqb.store.campaign import CampaignStore
    d = await brain.get_alpha_details(aid)
    if not d:
        print(f"  [writeback] {aid}: 详情为空，跳过")
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

    # 1) 诊断
    d0 = await brain.get_alpha_details(AID)
    if not d0:
        print("[ERROR] 详情为空")
        return
    print(f"[diag] status={d0.get('status')} stage={d0.get('stage')} type={d0.get('type')}")
    isd = isd_of(d0)
    print(f"[diag] sharpe={isd.get('sharpe')} fit={isd.get('fitness')} to={isd.get('turnover')}")

    # 2) 写描述（REGULAR 用 set_alpha_properties 即可，SUPER 才需裸 PATCH）
    await brain.set_alpha_properties(AID, descriptions=DESC)
    d = await brain.get_alpha_details(AID)
    raw = d.get("regular")
    cur = raw.get("description") if isinstance(raw, dict) else None
    dl = len(cur or "")
    print(f"[desc] len={dl}")
    result["desc_len"] = dl
    if dl < 100:
        print("[ABORT] 描述 <100 字符，平台会静默丢弃提交")
        result["aborted"] = "desc_too_short"
        OUT.parent.mkdir(parents=True, exist_ok=True)
        OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
        return

    # 3) submit#1
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
        print(f"[STOP] 配额闸门失败 {quota_blocked}（不提交后续）")
        result["quota_blocked"] = quota_blocked
        OUT.parent.mkdir(parents=True, exist_ok=True)
        OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
        return

    hard_blocked = [n for n, c in checks1.items()
                    if c.get("result") == "FAIL" and n not in QUOTA_GATES]
    if hard_blocked:
        print(f"[HARD-GATE] 硬闸失败 {hard_blocked}（零成本，不消耗配额）")
        result["hard_blocked"] = hard_blocked

    # 4) submit#2 verdict
    await asyncio.sleep(20)
    v2 = await brain.submit_alpha(AID)
    print(f"\n[submit#2] success={v2.get('success')} code={v2.get('status_code')} "
          f"reason={v2.get('reason')}")
    for c in (v2.get("checks") or []):
        print(f"    {c.get('name')}={c.get('value')} (limit={c.get('limit')}) -> {c.get('result')}")
    result["submit2"] = {"success": v2.get("success"), "status_code": v2.get("status_code"),
                         "reason": v2.get("reason"), "checks": v2.get("checks")}

    # 5) 轮询 OS
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

    # 6) DB 回写 + 落账
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
