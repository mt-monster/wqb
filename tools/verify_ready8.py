# -*- coding: utf-8 -*-
"""核实 8 颗 READY 候选：平台真实状态 + self_corr 复验（本地，不占 corr-lock 队列）。"""
import asyncio
import json
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from wqb.db_conn import connect as db_connect

import os as _os_repo
_REPO = _os_repo.path.dirname(_os_repo.path.dirname(_os_repo.path.abspath(__file__)))   # 仓库根（无盘符硬编码）
sys.path.insert(0, _os_repo.path.join(_REPO, 'world-quant-brain-mcp'))
DB = _os_repo.path.join(_REPO, 'data', 'wqb.db')
READY = ["Jj7ee6nO", "mLmxKN12", "omqEE1pn", "E5l6mmqJ",
         "gJboYLRl", "88jaV5lv", "6XjqLn3J", "LLNgdpw2"]


async def main():
    from brain_api import brain_client
    brain = brain_client
    await brain.ensure_authenticated()
    conn = db_connect(DB, timeout=20)
    now = datetime.now().isoformat(timespec="seconds")
    print("alpha_id | 平台状态 | 提交checks | self复验(pool) | 结论")
    for aid in READY:
        try:
            d = await brain.get_alpha_details(aid)
            st, stage = d.get("status"), d.get("stage")
            iss = d.get("is") or {}
            checks = {c.get("name"): c for c in (iss.get("checks") or [])}
            self_p = (checks.get("SELF_CORRELATION") or {}).get("result")
            self_v = (checks.get("SELF_CORRELATION") or {}).get("value")
            lit = (st == "ACTIVE" or stage == "OS")
            # 本地复验 self（看 pool 是否可信）
            sc = await brain.check_self_correlation(aid, threshold=0.7)
            local_self = sc.get("max_correlation")
            pool = (sc.get("correlation_data") or {}).get("pool_size", "n/a")
            verdict = "已点亮" if lit else ("提交就绪" if (local_self or 0) <= 0.7 else "self偏高")
            print(f"{aid} | {st}/{stage} | self_result={self_p} self_value={self_v} | "
                  f"local_self={local_self} pool={pool} | {verdict}")
            conn.execute("UPDATE alphas SET platform_status=?, stage=?, self_correlation=?, updated_at=? WHERE alpha_id=?",
                         (st, stage, local_self, now, aid))
        except Exception as e:
            print(f"{aid} | ERROR {str(e)[:100]}")
        conn.commit()
    conn.close()


asyncio.run(main())
