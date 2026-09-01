# -*- coding: utf-8 -*-
"""综合再评估（只读）：gJjN80rm 落地后，各区域还能提交什么 / 还能不能再组 SA。

1) 全区域 ACTIVE 池盘点（REGULAR / SUPER 按 settings.region 分组）
2) 每个 SUPER 的 selection / combo 详情（IND 2 颗 + MEA 2 颗）
3) MEA 7 颗低 PROD 候选的平台当前状态
4) 配额（/users/self/activities/submissions）
5) IND super-selection 预览：第 3 颗 SA 的组件空间
6) USA 侧 UNSUBMITTED 高 fitness 候选抽查（D1 第 4 个 alpha 路径）
"""
import asyncio
import json
import sys
from pathlib import Path

WQ_ROOT = Path(r"D:\coding\traeCN_project\wqb")
sys.path.insert(0, str(WQ_ROOT / "world-quant-brain-mcp"))

OUT = WQ_ROOT / "research-data" / "reassess_all_20260831.json"

MEA_CANDS = ["qMjLYVVP", "Jj7ee6nO", "omqEE1pn", "E5l6mmqJ",
             "Xg79vj7a", "58lEQMo1", "ak7KQoXv"]


async def _fetch_all_active(brain):
    rows = []
    offset = 0
    while True:
        r = await brain._request(
            "GET", f"{brain.base_url}/users/self/alphas",
            params={"limit": 100, "offset": offset, "status": "ACTIVE",
                    "order": "-dateSubmitted"},
        )
        if r.status_code != 200:
            print(f"[ERR] {r.status_code} {r.text[:200]}")
            break
        j = r.json()
        batch = j.get("results") or []
        rows.extend(batch)
        if j.get("next") is None or not batch:
            break
        offset += len(batch)
        if offset >= 1000:
            print("[warn] offset 达 1000 上限")
            break
    return rows


def _row_meta(a):
    isd = a.get("is") or {}
    st = a.get("settings") or {}
    return {
        "alpha_id": a.get("id"),
        "type": a.get("type"),
        "sharpe": isd.get("sharpe"), "fitness": isd.get("fitness"),
        "turnover": isd.get("turnover"), "returns": isd.get("returns"),
        "dateSubmitted": a.get("dateSubmitted"),
        "universe": st.get("universe"),
        "neutralization": st.get("neutralization"),
        "delay": st.get("delay"),
        "region": st.get("region"),
    }


async def main():
    brain = None
    from brain_api import BrainApiClient
    brain = BrainApiClient()
    await brain.ensure_authenticated()

    report = {}

    # ---------- 1) 全区域池盘点 ----------
    print("=== 1) 全区域 ACTIVE 池盘点 ===")
    rows = await _fetch_all_active(brain)
    by_region = {}
    for a in rows:
        reg = (a.get("settings") or {}).get("region") or "?"
        by_region.setdefault(reg, []).append(a)
    print(f"平台 ACTIVE 总数: {len(rows)}")
    print(f"{'region':<8}{'REGULAR':>9}{'SUPER':>7}{'合计':>7}")
    counts = {}
    for reg in sorted(by_region, key=lambda k: -len(by_region[k])):
        lst = by_region[reg]
        nr = sum(1 for x in lst if x.get("type") != "SUPER")
        ns = sum(1 for x in lst if x.get("type") == "SUPER")
        counts[reg] = {"regular": nr, "super": ns, "total": len(lst)}
        print(f"{reg:<8}{nr:>9}{ns:>7}{len(lst):>7}")
    report["active_counts"] = counts

    # ---------- 2) SUPER 详情（IND/MEA） ----------
    print("\n=== 2) 已有 SUPER 的 selection/combo ===")
    supers_all = [a for a in rows if a.get("type") == "SUPER"]
    sup_detail = {}
    for a in supers_all:
        aid = a.get("id")
        d = await brain.get_alpha_details(aid)
        if not d:
            continue
        sel = d.get("selection") or {}
        cmb = d.get("combo") or {}
        st = d.get("settings") or {}
        sup_detail[aid] = {
            "region": st.get("region"),
            "selection_expr": sel.get("expression") or sel.get("code"),
            "combo_expr": cmb.get("expression") or cmb.get("code"),
            "selectionLimit": st.get("selectionLimit"),
            "universe": st.get("universe"),
            "neutralization": st.get("neutralization"),
            "decay": st.get("decay"),
            "delay": st.get("delay"),
            "sharpe": (d.get("is") or {}).get("sharpe"),
            "fitness": (d.get("is") or {}).get("fitness"),
        }
        print(f"  {aid} [{st.get('region')}] selLimit={sup_detail[aid]['selectionLimit']} "
              f"neut={st.get('neutralization')} decay={st.get('decay')}")
        print(f"    sel: {sup_detail[aid]['selection_expr'][:110]}")
        print(f"    cmb: {sup_detail[aid]['combo_expr'][:110]}")
    report["super_detail"] = sup_detail

    # ---------- 3) MEA 候选状态 ----------
    print("\n=== 3) MEA 7 颗低 PROD 候选现状 ===")
    mea_cand = {}
    for aid in MEA_CANDS:
        try:
            d = await brain.get_alpha_details(aid)
        except Exception as e:
            mea_cand[aid] = {"error": str(e)}
            print(f"  {aid}: ERROR {e}")
            continue
        if not d:
            mea_cand[aid] = {"status": "NOT_FOUND"}
            print(f"  {aid}: NOT_FOUND")
            continue
        st = d.get("settings") or {}
        isd = d.get("is") or {}
        mea_cand[aid] = {
            "status": d.get("status"), "stage": d.get("stage"),
            "region": st.get("region"), "universe": st.get("universe"),
            "neutralization": st.get("neutralization"), "delay": st.get("delay"),
            "sharpe": isd.get("sharpe"), "fitness": isd.get("fitness"),
            "turnover": isd.get("turnover"), "returns": isd.get("returns"),
        }
        print(f"  {aid}: status={d.get('status')} stage={d.get('stage')} "
              f"sharpe={isd.get('sharpe')} fit={isd.get('fitness')} "
              f"to={isd.get('turnover')} univ={st.get('universe')} neut={st.get('neutralization')}")
    report["mea_candidates"] = mea_cand

    # ---------- 4) 配额 ----------
    print("\n=== 4) 配额 / 提交活动 ===")
    try:
        r = await brain._request(
            "GET", f"{brain.base_url}/users/self/activities/submissions",
            params={"grouping": "SUBMISSION"},
        )
        report["quota_raw"] = r.text[:2000]
        print(f"  status={r.status_code} body={r.text[:800]}")
    except Exception as e:
        print(f"  {e}")
        report["quota_error"] = str(e)

    # ---------- 5) IND super-selection 预览 ----------
    print("\n=== 5) IND super-selection 预览（第 3 颗 SA 空间） ===")
    try:
        r = await brain._request(
            "GET", f"{brain.base_url}/simulations/super-selection",
            params={"selectionLimit": 300, "region": "IND"},
        )
        print(f"  status={r.status_code}")
        if r.status_code == 200:
            j = r.json()
            recs = j.get("records") or j.get("results") or []
            # 预览接口忽略 region 参数 → 本地按 settings.region 过滤
            ind_recs = [x for x in recs if ((x.get("settings") or {}).get("region") or x.get("region")) == "IND"]
            print(f"  返回 {len(recs)} 条（接口忽略 region），本地过滤出 IND {len(ind_recs)} 条")
            report["ind_super_selection_count"] = {"raw": len(recs), "ind_filtered": len(ind_recs)}
            for x in ind_recs[:20]:
                st = x.get("settings") or {}
                print(f"    {x.get('id')}  {x.get('dateSubmitted','')[:10]}  "
                      f"prod={x.get('prodCorr') or x.get('prod_correlation')}  "
                      f"self={x.get('selfCorr') or x.get('self_correlation')}")
    except Exception as e:
        print(f"  {e}")
        report["super_selection_error"] = str(e)

    # ---------- 6) USA UNSUBMITTED 高 fitness 抽查 ----------
    print("\n=== 6) USA UNSUBMITTED 候选抽查 ===")
    try:
        r = await brain._request(
            "GET", f"{brain.base_url}/users/self/alphas",
            params={"limit": 100, "offset": 0, "status": "UNSUBMITTED",
                    "order": "-is.fitness"},
        )
        if r.status_code == 200:
            j = r.json()
            usa_u = []
            for a in (j.get("results") or []):
                st = a.get("settings") or {}
                if st.get("region") == "USA":
                    isd = a.get("is") or {}
                    usa_u.append({
                        "alpha_id": a.get("id"),
                        "sharpe": isd.get("sharpe"),
                        "fitness": isd.get("fitness"),
                        "turnover": isd.get("turnover"),
                        "dateSubmitted": a.get("dateSubmitted"),
                        "universe": st.get("universe"),
                        "neutralization": st.get("neutralization"),
                        "delay": st.get("delay"),
                    })
            print(f"  USA UNSUBMITTED: {len(usa_u)} 颗")
            for x in usa_u[:15]:
                print(f"    {x['alpha_id']}  sharpe={x['sharpe']} fit={x['fitness']} "
                      f"to={x['turnover']} {x['universe']}/{x['neutralization']}/d{x['delay']}")
            report["usa_unsubmitted_top"] = usa_u[:15]
        else:
            print(f"  [ERR] {r.status_code} {r.text[:200]}")
    except Exception as e:
        print(f"  {e}")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n[saved] {OUT}")


if __name__ == "__main__":
    asyncio.run(main())
