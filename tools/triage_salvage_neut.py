# -*- coding: utf-8 -*-
"""可抢救带（prod 0.70~0.85）中性化变体抢救 v2：SUBINDUSTRY -> STATISTICAL。

依据：USA 案例中 STATISTICAL 的 prod 比 SUBINDUSTRY 低约 0.10（镜像杠杆）。
DEU 无 TOP300 universe（平台 400 已证实），换 universe 不可行。
若平台拒绝 STATISTICAL 则回退 MARKET。checkpoint: logs/_triage_salvage2.json。
"""
import asyncio
import json
import sqlite3
import sys
from datetime import datetime

sys.path.insert(0, r"D:\coding\traeCN_project\wqb\world-quant-brain-mcp")
TRIAGE = r"D:\coding\traeCN_project\wqb\logs\_triage_prodcorr.json"
OUT = r"D:\coding\traeCN_project\wqb\logs\_triage_salvage2.json"
DB = r"D:\coding\traeCN_project\wqb\data\wqb.db"


def build_variants():
    st = json.load(open(TRIAGE, encoding="utf-8"))
    near = {k: v for k, v in st.items() if 'error' not in v
            and 0.70 < (v.get('prod') or 0) <= 0.85}
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    out = []
    for k, v in sorted(near.items(), key=lambda x: x[1]['prod']):
        rep = v['alpha_id']
        d = conn.execute('''SELECT b.code FROM alphas a
                            LEFT JOIN backtest_results b ON b.alpha_id=a.alpha_id
                            WHERE a.alpha_id=?''', (rep,)).fetchone()
        out.append({"family": k[:60], "rep": rep, "rep_prod": v['prod'], "code": d['code']})
    conn.close()
    return out


def load_state():
    try:
        return json.load(open(OUT, encoding="utf-8"))
    except Exception:
        return {"variants": {}}


def save_state(st):
    json.dump(st, open(OUT, "w", encoding="utf-8"), indent=1, ensure_ascii=False)


async def submit_variant(brain, v, alt_neut=None):
    rep_d = await brain.get_alpha_details(v['rep'])
    settings = rep_d.get('settings') or {}
    real_code = (rep_d.get('regular') or {}).get('code')
    if not real_code:
        return {"error": "rep 平台详情无 regular.code"}
    settings['neutralization'] = alt_neut or 'STATISTICAL'
    settings['visualization'] = False
    payload = {"type": "REGULAR", "settings": settings, "regular": real_code}
    for attempt in range(3):
        resp = await brain._request('POST', f"{brain.base_url}/simulations", json=payload)
        if resp.status_code == 429:
            await asyncio.sleep(3 * (attempt + 1))
            continue
        break
    if resp.status_code < 400:
        loc = resp.headers.get('Location', '')
        return {"sim_id": loc.rstrip('/').split('/')[-1] if loc else None}
    body = str(brain._response_payload(resp))[:150]
    if alt_neut is None and 'not available' in body:
        fb = await submit_variant(brain, v, alt_neut='MARKET')
        fb.setdefault('fallback', 'MARKET')
        return fb
    return {"error": f"HTTP {resp.status_code}: {body}"}


async def poll_terminal(brain, sim_id, max_wait=2400):
    waited = 0
    while waited < max_wait:
        r = await brain._request('GET', f"{brain.base_url}/simulations/{sim_id}")
        d = brain._response_payload(r)
        status = (d or {}).get("status")
        if status in ("ERROR", "FAIL"):
            return d
        if status == "COMPLETE" and d.get("alpha"):
            return d
        await asyncio.sleep(25)
        waited += 25
    return {"status": "TIMEOUT"}


async def main():
    from brain_api import brain_client
    brain = brain_client
    await brain.ensure_authenticated()

    variants = build_variants()
    state = load_state()
    print(f"可抢救族（中性化变体）: {len(variants)}")

    for v in variants:
        fam = v['family']
        if fam in state['variants'] and (state['variants'][fam].get('sim_id') or state['variants'][fam].get('error')):
            continue
        rec = {"rep": v['rep'], "rep_prod": v['rep_prod']}
        try:
            rec.update(await submit_variant(brain, v))
        except Exception as e:
            rec['error'] = str(e)[:150]
        state['variants'][fam] = rec
        save_state(state)
        await asyncio.sleep(1.0)
    print(f"[submit] 完成: {sum(1 for r in state['variants'].values() if r.get('sim_id'))} 成功提交,"
          f" {sum(1 for r in state['variants'].values() if r.get('error'))} 失败")

    for fam, rec in state['variants'].items():
        if rec.get('alpha_id') or rec.get('error') or not rec.get('sim_id'):
            continue
        d = await poll_terminal(brain, rec['sim_id'])
        rec['sim_status'] = d.get('status')
        rec['alpha_id'] = d.get('alpha')
        if d.get('message'):
            rec['sim_message'] = str(d.get('message'))[:150]
        save_state(state)
        print(f"[sim] {rec['rep']} -> {d.get('status')} {d.get('alpha')}")

    for fam, rec in state['variants'].items():
        aid = rec.get('alpha_id')
        if not aid or rec.get('prod_corr') or rec.get('gate') is False:
            continue
        d = await brain.get_alpha_details(aid)
        iss = d.get("is") or {}
        checks = {c.get("name"): c for c in (iss.get("checks") or [])}
        y2 = (checks.get("LOW_2Y_SHARPE") or {}).get("value")
        ladder = (checks.get("IS_LADDER_SHARPE") or {}).get("value")
        rec['metrics'] = {"sharpe": iss.get("sharpe"), "fitness": iss.get("fitness"),
                          "turnover": iss.get("turnover"), "margin": iss.get("margin"),
                          "two_year_sharpe": y2, "ladder": ladder}
        gates = ((iss.get("sharpe") or 0) >= 1.58 and (iss.get("fitness") or 0) >= 1.0
                 and ((y2 or 0) >= 1.58 or (ladder or 0) >= 1.58)
                 and (iss.get("margin") or 0) > 0)
        rec['gate'] = gates
        save_state(state)
        print(f"[gate] {aid} sh={iss.get('sharpe')} fit={iss.get('fitness')} 2Y={y2} lad={ladder} gate={gates}")
        if not gates:
            continue
        pc = await brain.check_correlation(aid, correlation_type="production", threshold=0.7)
        prod = (pc.get("checks") or {}).get("production") or {}
        rec['prod_corr'] = {"max": prod.get("max_correlation"), "pass": prod.get("passes_check")}
        sc = await brain.check_self_correlation(aid, threshold=0.7)
        rec['self_corr'] = {"max": sc.get("max_correlation"), "pass": sc.get("passes_check"),
                            "status": sc.get("status")}
        save_state(state)
        print(f"  prod={prod.get('max_correlation')} self={rec['self_corr']['max']}")

    saved = [(r.get('alpha_id'), (r.get('prod_corr') or {}).get('max'))
             for r in state['variants'].values() if r.get('prod_corr')]
    n_pass = sum(1 for _, p in saved if (p or 1) <= 0.7)
    print(f"\n抢救 v2 完成：重测 {len(saved)} 个，prod 过线 {n_pass} 个")


asyncio.run(main())
