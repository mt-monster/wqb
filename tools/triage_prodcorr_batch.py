# -*- coding: utf-8 -*-
"""全库分诊第三步：绿池未测族代表批量 prod_corr（串行，checkpoint 可续跑）。"""
import asyncio
import json
import sqlite3
import sys
from datetime import datetime

sys.path.insert(0, r"D:\coding\traeCN_project\wqb\world-quant-brain-mcp")
OUT = r"D:\coding\traeCN_project\wqb\logs\_triage_prodcorr.json"
DB = r"D:\coding\traeCN_project\wqb\data\wqb.db"


def build_targets():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    rows = conn.execute('''
        SELECT a.alpha_id, a.fitness, a.sharpe, a.two_year_sharpe, a.prod_correlation,
               b.code, b.region AS b_region
        FROM alphas a LEFT JOIN backtest_results b ON b.alpha_id = a.alpha_id
        WHERE a.sharpe>=1.58 AND a.fitness>=1.0 AND a.two_year_sharpe>=1.58
          AND a.margin IS NOT NULL
          AND (a.platform_status IS NULL OR (a.platform_status!='ACTIVE' AND a.stage!='OS'))
          AND a.alpha_id != '883WZJ1W'
          AND (b.ra_failed_checks IS NULL OR b.ra_failed_checks IN ('null','[]'))
    ''').fetchall()
    conn.close()
    fams = {}
    for r in rows:
        k = f"{r['b_region']}|{(r['code'] or r['alpha_id'])[:100]}"
        if k not in fams or (r['fitness'] or 0) > (fams[k]['fitness'] or 0):
            fams[k] = r
    return {k: v['alpha_id'] for k, v in fams.items()
            if v['prod_correlation'] is None and not k.startswith('USA|')}


def load_state():
    try:
        return json.load(open(OUT, encoding="utf-8"))
    except Exception:
        return {}


def save_state(st):
    json.dump(st, open(OUT, "w", encoding="utf-8"), indent=1, ensure_ascii=False)


def persist_prod_corr(alpha_id, prod):
    """边测边落库（2026-09-17 补）：只填 NULL，不覆盖既有/提交后同步值。

    此前结果只写 JSON checkpoint、从不回写 alphas 表 → SOP 的「prod-first 0.6
    预警线」始终无过程数据可触发（实测 alphas 覆盖率 6.5%）。
    """
    if not isinstance(prod, (int, float)):
        return
    try:
        conn = sqlite3.connect(DB)
        try:
            conn.execute("UPDATE alphas SET prod_correlation=? WHERE alpha_id=? "
                         "AND prod_correlation IS NULL", (float(prod), alpha_id))
            conn.commit()
        finally:
            conn.close()
    except Exception:
        pass  # 落库失败不影响抽测主流程（JSON checkpoint 仍是权威记录）


async def main():
    from brain_api import brain_client
    brain = brain_client
    await brain.ensure_authenticated()

    targets = build_targets()
    state = load_state()
    todo = {k: a for k, a in targets.items() if k not in state}
    print(f"未测族: {len(todo)}/{len(targets)}")

    for i, (k, aid) in enumerate(list(todo.items())):
        try:
            pc = await brain.check_correlation(aid, correlation_type="production", threshold=0.7)
            prod = (pc.get("checks") or {}).get("production") or {}
            state[k] = {"alpha_id": aid, "prod": prod.get("max_correlation"),
                        "pass": prod.get("passes_check")}
            persist_prod_corr(aid, prod.get("max_correlation"))  # 边测边落库
            print(f"[{i+1}/{len(todo)}] {aid} ({k[:45]}) prod={prod.get('max_correlation')}")
        except Exception as e:
            state[k] = {"alpha_id": aid, "error": str(e)[:150]}
            print(f"[{i+1}/{len(todo)}] {aid} ERROR {str(e)[:100]}")
        save_state(state)

    ok = {k: v for k, v in state.items() if 'error' not in (v or {})}
    n_pass = sum(1 for v in ok.values() if (v.get('prod') or 1) <= 0.7)
    near = [k for k, v in ok.items() if 0.7 < (v.get('prod') or 1) <= 0.85]
    print(f"\n完成: {len(ok)} 族 | prod<=0.7 过线 {n_pass} 族 | 0.70~0.85 可抢救 {len(near)} 族 | >0.85 {len(ok)-n_pass-len(near)} 族")


asyncio.run(main())
