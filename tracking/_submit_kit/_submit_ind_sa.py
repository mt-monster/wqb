# -*- coding: utf-8 -*-
"""提交 IND SUPER alpha gJjN80rm（decay=90，SELF 0.6545 / PROD 0.6722 双闸 PASS）。

关键：SUPER alpha 必须用裸 PATCH 写描述（set_alpha_properties 带 regular 字段必 400）。
硬闸失败不消耗配额；SUPER_SUBMISSION 配额 limit=1（48h 滚动）。
"""
import asyncio
import json
import sys
from pathlib import Path

WQ_ROOT = Path(r"D:\coding\traeCN_project\wqb")
sys.path.insert(0, str(WQ_ROOT / "world-quant-brain-mcp"))
sys.path.insert(0, str(WQ_ROOT / "src"))

AID = "gJjN80rm"

SELECTION_DESC = (
    "This super alpha selects India regular component alphas using two independent correlation "
    "screens applied together. The first screen keeps only components whose production correlation "
    "stays below 0.7, which removes signals that are already well represented in the broader "
    "platform production pool and therefore add little incremental information. The second and "
    "stricter screen keeps only components whose self correlation against the account's existing "
    "active book stays below 0.45, which is tighter than the submission threshold because the "
    "account's dominant historical failure mode has been submitting near duplicate signals that "
    "correlate strongly with alphas already in production. Combining both screens yields a ten "
    "component set that spans the STATISTICAL, SECTOR, SUBINDUSTRY and INDUSTRY neutralization "
    "families present in the India book, so the aggregate signal is not dominated by any single "
    "neutralization style. A no-op multiplicative term of one plus zero times a boolean is included "
    "so that the expression is evaluated as a numeric weight rather than a bare predicate, which is "
    "required for the selection weight to be interpreted correctly by the platform."
)

COMBO_DESC = (
    "The combination expression assigns each selected component a weight equal to the fifth power "
    "of one minus the maximum pairwise self correlation observed for that component over a five "
    "hundred day return window. Taking the fifth power rather than the first power deliberately "
    "amplifies the dispersion of the weights: components whose return stream is largely idiosyncratic "
    "with respect to the rest of the selected set receive a weight close to one, while components that "
    "move together with any other member of the set are compressed strongly toward zero. This "
    "concentrates the aggregate portfolio on the most independent contributors and reduces the "
    "resulting self correlation and production correlation well below what an equal weighted average "
    "or a linearly decaying weight would achieve. Identical return series are mapped to missing values "
    "before the maximum is taken so that degenerate duplicate components cannot silently dominate the "
    "weighting. A decay of ninety days is applied so that the aggregate position adjusts gradually, "
    "which further reduces the day to day co-movement with the existing India super alpha while "
    "keeping the in-sample Sharpe, fitness and ladder Sharpe comfortably above their submission limits."
)


async def main():
    from brain_api import BrainApiClient
    brain = BrainApiClient()
    await brain.ensure_authenticated()

    # 0) 前置诊断
    d0 = await brain.get_alpha_details(AID)
    print(f"[diag] type={d0.get('type')} status={d0.get('status')} stage={d0.get('stage')}")
    isd = d0.get("is") or {}
    print(f"[diag] sharpe={isd.get('sharpe')} fit={isd.get('fitness')} to={isd.get('turnover')}")

    # 1) 裸 PATCH 写描述（SUPER 必须）
    payload = {
        "selection": {"description": SELECTION_DESC},
        "combo": {"description": COMBO_DESC},
    }
    r = await brain._request("PATCH", f"{brain.base_url}/alphas/{AID}", json=payload)
    print(f"[PATCH] status={r.status_code}")
    if r.status_code not in (200, 201):
        print(f"[PATCH] body={r.text[:600]}")
        return
    d = await brain.get_alpha_details(AID)
    sl = len((d.get("selection") or {}).get("description") or "")
    cl = len((d.get("combo") or {}).get("description") or "")
    print(f"[verify] sel_desc_len={sl} combo_desc_len={cl}")
    if sl < 100 or cl < 100:
        print("[ABORT] 描述过短，平台会静默丢弃提交")
        return

    result = {"alpha_id": AID, "sel_desc_len": sl, "combo_desc_len": cl}

    # 2) submit#1
    v1 = await brain.submit_alpha(AID)
    print(f"\n[submit#1] success={v1.get('success')} code={v1.get('status_code')} "
          f"reason={v1.get('reason')}")
    for c in (v1.get("checks") or []):
        print(f"    {c.get('name')}={c.get('value')} (limit={c.get('limit')}) -> {c.get('result')}")
    result["submit1"] = {"success": v1.get("success"), "checks": v1.get("checks")}

    quota_fail = [
        c.get("name") for c in (v1.get("checks") or [])
        if c.get("name") in ("SUPER_SUBMISSION", "REGULAR_SUBMISSION")
        and c.get("result") == "FAIL"
    ]
    if quota_fail:
        print(f"[STOP] 配额闸门失败: {quota_fail}")
        result["quota_fail"] = quota_fail
        Path(WQ_ROOT / "research-data" / "ind_sa_submit_result.json").write_text(
            json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
        return

    # 3) submit#2 verdict
    await asyncio.sleep(20)
    v2 = await brain.submit_alpha(AID)
    print(f"\n[submit#2] success={v2.get('success')} code={v2.get('status_code')} "
          f"reason={v2.get('reason')}")
    for c in (v2.get("checks") or []):
        print(f"    {c.get('name')}={c.get('value')} (limit={c.get('limit')}) -> {c.get('result')}")
    result["submit2"] = {"success": v2.get("success"), "checks": v2.get("checks")}

    # 4) 轮询 OS
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

    # 5) 落账
    dd = await brain.get_alpha_details(AID)
    st = dd.get("settings") or {}
    isd2 = dd.get("is") or {}
    ladder = None
    for c in (isd2.get("checks") or []):
        if c.get("name") == "IS_LADDER_SHARPE":
            ladder = c.get("value")
    from wqb.store.campaign import CampaignStore
    store = CampaignStore(str(WQ_ROOT / "data" / "wqb.db"))
    try:
        store.upsert_alpha_from_platform({
            "alpha_id": AID, "region": "IND",
            "expression": "(SUPER) " + str((dd.get("selection") or {}).get("expression") or ""),
            "sharpe": isd2.get("sharpe"), "fitness": isd2.get("fitness"),
            "turnover": isd2.get("turnover"), "two_year_sharpe": None,
            "is_ladder_sharpe": ladder,
            "prod_correlation": isd2.get("prodCorrelation"),
            "self_correlation": isd2.get("selfCorrelation"),
            "platform_status": dd.get("status"), "stage": dd.get("stage"),
            "alpha_type": dd.get("type"), "date_submitted": dd.get("dateSubmitted"),
            "universe": st.get("universe"), "delay": st.get("delay"),
            "neutralization": st.get("neutralization"),
        })
        print(f"[db] alphas 回写 OK status={dd.get('status')} stage={dd.get('stage')}")
        result["db_written"] = True
    except Exception as e:
        print(f"[db] alphas FAILED {e}")
        result["db_written"] = str(e)

    if v2.get("success"):
        try:
            store.record_submission(
                alpha_id=AID, region="IND", submission_type="SUPER",
                status="ACTIVE", verdict=result["submit2"], quota_used=1,
            )
            print("[db] submission_ledger OK")
            result["ledger"] = True
        except Exception as e:
            print(f"[db] ledger FAILED {e}")
            result["ledger"] = str(e)
    store.close()

    Path(WQ_ROOT / "research-data" / "ind_sa_submit_result.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print("\n[saved] research-data/ind_sa_submit_result.json")


if __name__ == "__main__":
    asyncio.run(main())
