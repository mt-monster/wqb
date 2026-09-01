# -*- coding: utf-8 -*-
"""提交 IND 第 3 颗 SA：wpjrMnz5（STATISTICAL / decay 30 / limit 10）。

本地预检：SELF 0.6390 / PROD 0.6394（限 0.7）；sharpe 3.73 / fit 4.00 / ladder 4.01。
SUPER 写描述必须裸 PATCH；SUPER_SUBMISSION 配额 limit=1。
"""
import asyncio
import json
import sys
from pathlib import Path

WQ_ROOT = Path(r"D:\coding\traeCN_project\wqb")
sys.path.insert(0, str(WQ_ROOT / "world-quant-brain-mcp"))
sys.path.insert(0, str(WQ_ROOT / "src"))

AID = "wpjrMnz5"

SELECTION_DESC = (
    "This selection expression scores every active India regular alpha by how much novelty it "
    "contributes relative to the production pool, using the distance between its production "
    "correlation and the submission threshold of zero point seven as the score. Alphas whose "
    "production correlation is far below the threshold receive a much larger weight, so the "
    "combination is led by signals that are genuinely distinct from what the platform already "
    "holds rather than by signals that merely squeak past the limit. A non-gating multiplicative "
    "term of one plus zero times a boolean is present so the expression evaluates to a numeric "
    "weight instead of a bare predicate, which is required for the score to be interpreted "
    "correctly. A hard self-correlation gate below zero point six five removes components that are "
    "too close to alphas already in the account book, and a turnover band between one and fifty "
    "percent keeps the selected set tradable while excluding both near-static and excessively "
    "churning signals. Because the score decreases monotonically with production correlation, the "
    "platform ranks the most novel alphas first and retains the top ten, which yields a component "
    "set that overlaps only partially with the components held by the two India super alphas "
    "already in production."
)

COMBO_DESC = (
    "The combination expression weights each selected component by the fifth power of one minus "
    "the maximum pairwise self correlation observed for that component over a five hundred day "
    "return window. Raising the weight to the fifth power rather than using it linearly sharply "
    "amplifies the dispersion among the components: an alpha whose return stream is largely "
    "idiosyncratic with respect to the rest of the set keeps a weight close to one, while an alpha "
    "that moves together with any other member is compressed strongly toward zero. This "
    "concentrates the aggregate portfolio on the most independent contributors instead of letting "
    "redundant signals dilute the combination. Identical return series are mapped to missing values "
    "before the maximum is taken, so degenerate duplicate components cannot silently dominate the "
    "weighting. A decay of thirty days is applied so positions adjust at a moderate pace: long "
    "enough to damp daily noise, short enough that the in-sample Sharpe, fitness and ladder Sharpe "
    "all stay far above their submission limits. The overall intent is a third India super alpha "
    "whose self correlation and production correlation both remain comfortably below the "
    "submission threshold while retaining the return contribution of the strongest novel "
    "components in the India book."
)


async def main():
    from brain_api import BrainApiClient
    brain = BrainApiClient()
    await brain.ensure_authenticated()

    d0 = await brain.get_alpha_details(AID)
    isd0 = d0.get("is") or {}
    st0 = d0.get("settings") or {}
    print(f"[diag] type={d0.get('type')} status={d0.get('status')} stage={d0.get('stage')}")
    print(f"[diag] sharpe={isd0.get('sharpe')} fit={isd0.get('fitness')} to={isd0.get('turnover')}")
    print(f"[diag] {st0.get('universe')}/{st0.get('neutralization')}/d{st0.get('delay')} "
          f"decay={st0.get('decay')} trunc={st0.get('truncation')}")

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
        print("[ABORT] 描述过短")
        return

    result = {"alpha_id": AID, "sel_desc_len": sl, "combo_desc_len": cl}

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
        Path(WQ_ROOT / "research-data" / "ind_sa2_submit_result.json").write_text(
            json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
        return

    await asyncio.sleep(20)
    v2 = await brain.submit_alpha(AID)
    print(f"\n[submit#2] success={v2.get('success')} code={v2.get('status_code')} "
          f"reason={v2.get('reason')}")
    for c in (v2.get("checks") or []):
        print(f"    {c.get('name')}={c.get('value')} (limit={c.get('limit')}) -> {c.get('result')}")
    result["submit2"] = {"success": v2.get("success"), "checks": v2.get("checks")}

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
        result["db_written"] = True
        print(f"[db] alphas OK status={dd.get('status')} stage={dd.get('stage')}")
        cur = store.connection.cursor()
        cur.execute("UPDATE alphas SET status='COMPLETE' WHERE alpha_id=? AND status<>'COMPLETE'",
                    (AID,))
        store.connection.commit()
        print(f"[db] status -> COMPLETE ({cur.rowcount})")
    except Exception as e:
        result["db_written"] = str(e)
        print(f"[db] alphas FAILED {e}")

    if v2.get("success"):
        try:
            store.record_submission(
                alpha_id=AID, region="IND", submission_type="SUPER",
                status="ACTIVE", verdict=result["submit2"], quota_used=1,
            )
            result["ledger"] = True
            print("[db] submission_ledger OK")
        except Exception as e:
            result["ledger"] = str(e)
            print(f"[db] ledger FAILED {e}")
    store.close()

    Path(WQ_ROOT / "research-data" / "ind_sa2_submit_result.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print("\n[saved] research-data/ind_sa2_submit_result.json")


if __name__ == "__main__":
    asyncio.run(main())
