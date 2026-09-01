# -*- coding: utf-8 -*-
"""提交 d5jJebLv / Jj7aRNKm / 2rlVPwdw（IND 同族 mdl135_icc 变体）。

6 步闭环：
  1) 诊断（非 UNSUBMITTED 则跳过提交，仅回写）
  2) submit#1
  3) 若配额类 FAIL 立即停（避免浪费）；硬闸 FAIL 零成本，继续记录
  4) sleep 20s -> submit#2 (verdict)
  5) 轮询 OS 翻转
  6) 平台详情回写 alphas + submission_ledger

硬闸（PROD/SELF/IS_LADDER_SHARPE）失败返回 403 且不消耗 REGULAR_SUBMISSION 配额。
"""
import asyncio
import json
import sys
from pathlib import Path

WQ_ROOT = Path(r"D:\coding\traeCN_project\wqb")
sys.path.insert(0, str(WQ_ROOT / "world-quant-brain-mcp"))
sys.path.insert(0, str(WQ_ROOT / "src"))

TARGETS = ["d5jJebLv", "Jj7aRNKm", "2rlVPwdw"]
OUT = WQ_ROOT / "research-data" / "submit3_result.json"

# 会消耗配额的闸门（命中即停）
QUOTA_GATES = {"REGULAR_SUBMISSION", "SUPER_SUBMISSION"}


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


async def writeback(brain, aid, results):
    """把平台详情 + 预检双闸写入 DB。"""
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
        print(f"  [writeback] {aid}: alphas FAILED {e}")
        rid = None
    store.close()
    return payload


async def main():
    from brain_api import BrainApiClient
    brain = BrainApiClient()
    await brain.ensure_authenticated()

    results = {}
    for aid in TARGETS:
        print(f"\n{'='*60}\n=== {aid} ===\n{'='*60}")
        d0 = await brain.get_alpha_details(aid)
        if not d0:
            print(f"  [ERROR] 详情为空")
            results[aid] = {"error": "empty details"}
            continue

        pstatus = d0.get("status")
        pstage = d0.get("stage")
        print(f"  [diag] platform_status={pstatus} stage={pstage} "
              f"type={d0.get('type')} region={isd_of(d0).get('region')}")

        row = {"initial_status": pstatus, "initial_stage": pstage}

        # 1) 非 UNSUBMITTED -> 跳过提交，仅回写
        if pstatus != "UNSUBMITTED":
            print(f"  [skip] 已提交过（{pstatus}/{pstage}），仅回写平台详情")
            row["skipped"] = True
            payload = await writeback(brain, aid, results)
            row["payload"] = payload
            results[aid] = row
            continue

        # 2) submit#1
        v1 = await brain.submit_alpha(aid)
        ok1 = v1.get("success")
        print(f"  [submit#1] success={ok1} code={v1.get('status_code')} reason={v1.get('reason')}")
        checks1 = {c.get("name"): c for c in (v1.get("checks") or [])}
        for c in (v1.get("checks") or []):
            print(f"      {c.get('name')}={c.get('value')} (limit={c.get('limit')}) -> {c.get('result')}")
        row["submit1"] = {
            "success": ok1, "status_code": v1.get("status_code"),
            "reason": v1.get("reason"), "checks": v1.get("checks"),
        }

        # 3) 配额类闸门 FAIL -> 停
        quota_blocked = [
            n for n, c in checks1.items()
            if n in QUOTA_GATES and c.get("result") == "FAIL"
        ]
        if quota_blocked:
            print(f"  [STOP] 配额闸门失败 {quota_blocked}，停止后续提交")
            row["quota_blocked"] = quota_blocked
            results[aid] = row
            break

        hard_blocked = [
            n for n, c in checks1.items()
            if c.get("result") == "FAIL" and n not in QUOTA_GATES
        ]
        if hard_blocked:
            print(f"  [HARD-GATE] 硬闸失败 {hard_blocked}（零成本，不消耗配额）")
            row["hard_blocked"] = hard_blocked

        # 4) submit#2 verdict
        await asyncio.sleep(20)
        v2 = await brain.submit_alpha(aid)
        ok2 = v2.get("success")
        print(f"  [submit#2] success={ok2} code={v2.get('status_code')} reason={v2.get('reason')}")
        for c in (v2.get("checks") or []):
            print(f"      {c.get('name')}={c.get('value')} (limit={c.get('limit')}) -> {c.get('result')}")
        row["submit2"] = {
            "success": ok2, "status_code": v2.get("status_code"),
            "reason": v2.get("reason"), "checks": v2.get("checks"),
        }

        # 5) 轮询 OS
        flipped = False
        if ok2:
            for i in range(6):
                await asyncio.sleep(30)
                dd = await brain.get_alpha_details(aid)
                print(f"      [poll{i+1}] stage={dd.get('stage')} status={dd.get('status')}")
                if dd.get("stage") == "OS":
                    flipped = True
                    print(f"      >>> {aid} FLIPPED TO OS <<<")
                    break
        row["flipped_os"] = flipped

        # 6) 回写 + 落账
        payload = await writeback(brain, aid, results)
        row["payload"] = payload

        if ok2:
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

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n[saved] {OUT}")

    print("\n" + "=" * 60)
    print("汇总")
    print("=" * 60)
    for aid, r in results.items():
        print(f"{aid}: skipped={r.get('skipped')} submit1={r.get('submit1', {}).get('success')} "
              f"submit2={r.get('submit2', {}).get('success')} os={r.get('flipped_os')} "
              f"ledger={r.get('ledger')}")
        if r.get("hard_blocked"):
            print(f"    硬闸失败: {r['hard_blocked']}")


if __name__ == "__main__":
    asyncio.run(main())
