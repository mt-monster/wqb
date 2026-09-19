# -*- coding: utf-8 -*-
"""可抢救带（prod 0.70~0.85）全族换 universe 抢救：DEU TOP500 -> TOP300。

流程：按 triage checkpoint 取 near 带 26 族代表 -> 批量提交 TOP300 变体仿真
-> 轮询终态 -> 硬闸检查 -> 过闸者重测 prod_corr（串行）。
checkpoint: logs/_triage_salvage.json 可续跑。
"""
import asyncio
import json
import sqlite3
import sys
from datetime import datetime

sys.path.insert(0, r"D:\coding\traeCN_project\wqb\world-quant-brain-mcp")
TRIAGE = r"D:\coding\traeCN_project\wqb\logs\_triage_prodcorr.json"
OUT = r"D:\coding\traeCN_project\wqb\logs\_triage_salvage.json"
DB = r"D:\coding\traeCN_project\wqb\data\wqb.db"


def build_variants():
    st = json.load(open(TRIAGE, encoding="utf-8"))
    near = {k: v for k, v in st.items() if 'error' not in v
            and 0.70 < (v.get('prod') or 0) <= 0.85}
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    variants = []
    for k, v in sorted(near.items(), key=lambda x: x[1]['prod']):
        rep = v['alpha_id']
        d = conn.execute('''SELECT a.alpha_id, b.code, b.wave FROM alphas a
                            LEFT JOIN backtest_results b ON b.alpha_id=a.alpha_id
                            WHERE a.alpha_id=?''', (rep,)).fetchone()
        variants.append({"family": k[:60], "rep": rep, "code": d['code']})
    conn.close()
    return variants


def load_state():
    try:
        return json.load(open(OUT, encoding="utf-8"))
    except Exception:
        return {"variants": {}}


def save_state(st):
    json.dump(st, open(OUT, "w", encoding="utf-8"), indent=1, ensure_ascii=False)


async def poll_terminal(brain, sim_id, max_wait=1800):
    waited = 0
    while waited < max_wait:
        r = await brain._request('GET', f"{brain.base_url}/simulations/{sim_id}")
        d = brain._response_payload(r)
        status = (d or {}).get("status")
        if status in ("COMPLETE", "ERROR", "FAIL"):
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
    print(f"可抢救族: {len(variants)}")

    # 原版设置从 rep 的 payload 恢复（DEU TOP500 D1 SUBINDUSTRY trunc 0.08 为默认，逐个拉 details 更稳）
    for v in variants:
        if v['family'] in state['variants']:
            continue
        rep_d = await brain.get_alpha_details(v['rep'])
        settings = rep_d.get('settings') or {}
        settings['universe'] = 'TOP300'
        settings['visualization'] = False
        payload = {"type": "REGULAR", "settings": settings,
                   "regular": {"code": v['code']}}
        rec = {"rep": v['rep'], "family": v['family'], "rep_prod": None, "sim_status": None}
        resp = None
        for attempt in range(3):
            resp = await brain._request('POST', f"{brain.base_url}/simulations", json=payload)
            if resp.status_code != 429:
                break
            await asyncio.sleep(3 * (attempt + 1))
        if resp.status_code < 400:
            loc = resp.headers.get('Location', '')
            rec['sim_id'] = loc.rstrip('/').split('/')[-1] if loc else None
        else:
            rec['error'] = f"HTTP {resp.status_code}: {str(brain._response_payload(resp))[:150]}"
        state['variants'][v['family']] = rec
        save_state(state)
        await asyncio.sleep(1.0)

    # 轮询终态
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

    # 指标 + prod 重测
    for fam, rec in state['variants'].items():
        aid = rec.get('alpha_id')
        if not aid or rec.get('prod_corr') or rec.get('gate') is False:
            if rec.get('gate') is False:
                continue
            if not aid:
                continue
        d = await brain.get_alpha_details(aid)
        iss = d.get("is") or {}
        checks = {c.get("name"): c for c in (iss.get("checks") or [])}
        y2 = (checks.get("LOW_2Y_SHARPE") or {}).get("value")
        rec['metrics'] = {"sharpe": iss.get("sharpe"), "fitness": iss.get("fitness"),
                          "turnover": iss.get("turnover"), "margin": iss.get("margin"),
                          "two_year_sharpe": y2}
        gates = ((iss.get("sharpe") or 0) >= 1.58 and (iss.get("fitness") or 0) >= 1.0
                 and (y2 or 0) >= 1.58 and (iss.get("margin") or 0) > 0)
        rec['gate'] = gates
        save_state(state)
        print(f"[gate] {aid} {rec['metrics']} gate={gates}")
        if not gates:
            continue
        pc = await brain.check_correlation(aid, correlation_type="production", threshold=0.7)
        prod = (pc.get("checks") or {}).get("production") or {}
        rec['prod_corr'] = {"max": prod.get("max_correlation"), "pass": prod.get("passes_check")}
        save_state(state)
        print(f"  prod={prod.get('max_correlation')} pass={prod.get('passes_check')}")

    saved = [(rec.get('alpha_id'), rec.get('prod_corr', {}).get('max'))
             for rec in state['variants'].values() if rec.get('prod_corr')]
    print(f"\n抢救完成：重测 {len(saved)} 个，过线 {sum(1 for _, p in saved if (p or 1) <= 0.7)} 个")


asyncio.run(main())
