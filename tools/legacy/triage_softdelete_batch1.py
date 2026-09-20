# -*- coding: utf-8 -*-
"""死局软删除（第一批，确定集合）+ IND 2 颗 / EUR ladder 族 prod 补测。

软删除 = disposition='DEAD'（可恢复，备份 wqb.db.bak_triage_*）。
死局口径（本次会话已判定）：
  1. 硬闸过（sharpe/fitness）但实测 2Y<1.58 —— 平台 LOW_2Y 硬闸永不放行
  2. 2Y 缺但 ladder 实测 <1.58
  3. 绿池中 RA failed checks（CONCENTRATED_WEIGHT / IS_LADDER_SHARPE 等）
  4. prod_corr 实测 >0.85 的族（含 head-8 中 5 颗 DEU）——全部同 code 族成员
  5. 被替代/无杠杆：N1QMJ10q(被 883WZJ1W 替代)、V1-V4/V6、2rlVPwdw、qMja95Q2
排除：平台已点亮（ACTIVE/OS）一律不删。
"""
import asyncio
import json
import sqlite3
import sys
from datetime import datetime

sys.path.insert(0, r"D:\coding\traeCN_project\wqb\world-quant-brain-mcp")
DB = r"D:\coding\traeCN_project\wqb\data\wqb.db"
TRIAGE = r"D:\coding\traeCN_project\wqb\logs\_triage_prodcorr.json"

NOT_LIT = "(platform_status IS NULL OR (platform_status!='ACTIVE' AND stage!='OS'))"


def soft_delete(cur, where, reason):
    sql = f"""UPDATE alphas SET disposition='DEAD', dead_reason=?, dead_at=?
              WHERE {NOT_LIT} AND disposition IS NULL AND {where}"""
    cur.execute(sql, (reason, datetime.now().isoformat(timespec='seconds')))
    return cur.rowcount


def main_static(cur):
    n = {}
    n['2y_lt_158'] = soft_delete(cur, """sharpe>=1.58 AND fitness>=1.0
        AND two_year_sharpe IS NOT NULL AND two_year_sharpe < 1.58""", "2Y<1.58 硬闸死")
    n['ladder_lt_158'] = soft_delete(cur, """sharpe>=1.58 AND fitness>=1.0
        AND two_year_sharpe IS NULL AND is_ladder_sharpe IS NOT NULL AND is_ladder_sharpe < 1.58""",
        "ladder<1.58 死")
    n['ra_fail'] = soft_delete(cur, """sharpe>=1.58 AND fitness>=1.0
        AND EXISTS (SELECT 1 FROM backtest_results b WHERE b.alpha_id=alphas.alpha_id
                    AND b.ra_failed_checks IS NOT NULL AND b.ra_failed_checks NOT IN ('null','[]'))""",
        "RA failed checks 死")
    # prod>0.85 的族（按 code 分组，绿池成员）
    tri = json.load(open(TRIAGE, encoding="utf-8"))
    dead_reps = [(v['alpha_id'], v['prod']) for v in tri.values()
                 if 'error' not in v and (v.get('prod') or 0) > 0.85]
    # head-8 中 5 颗 DEU（0.87~0.996）+ 2rlVPwdw + qMja95Q2 由下方显式列表补
    total = 0
    for aid, prod in dead_reps:
        code_row = cur.execute("SELECT b.code FROM backtest_results b WHERE b.alpha_id=?", (aid,)).fetchone()
        if not code_row or not code_row[0]:
            continue
        c = soft_delete(cur, f"""sharpe>=1.58 AND fitness>=1.0 AND alpha_id!='{aid}'
            AND EXISTS (SELECT 1 FROM backtest_results b2 WHERE b2.alpha_id=alphas.alpha_id
                        AND b2.code={json.dumps(code_row[0])})""",
            f"族 prod={prod}>0.85 死（代表 {aid}）")
        c2 = soft_delete(cur, f"alpha_id='{aid}'", f"prod={prod}>0.85 死")
        total += c + c2
    n['fam_prod_gt_085'] = total
    # 显式名单
    explicit = {
        'N1QMJ10q': '被 883WZJ1W(TOP2000 变体) 替代',
        'P0ZLbM1x': 'V1 prod 0.8226', '1Yx3ROEQ': 'V2 prod 0.8021',
        'zqY7EGlE': 'V3 prod 0.7903', 'gJQN5dJQ': 'V4 prod 0.80',
        'Vk6QLx3Y': 'V6 prod 0.7225 被替代', '2rlVPwdw': 'prod/self 0.913 重度同源',
        'qMja95Q2': 'prod/self 0.735 且 IND 无 universe/中性化杠杆',
    }
    n['explicit'] = sum(soft_delete(cur, f"alpha_id='{a}'", r) for a, r in explicit.items())
    return n


TEST_INDIV = ["Jj7aRNKm", "3qlKQ1qX"]  # IND ladder 达标，族内 corr 未测


def eur_ladder_reps(cur):
    # EUR 2Y 缺、ladder>=1.58 的达标者，按 wave 去重取代表
    rows = cur.execute("""
        SELECT alpha_id, wave FROM (
            SELECT a.alpha_id, b.wave,
                   ROW_NUMBER() OVER (PARTITION BY b.wave ORDER BY a.fitness DESC) rn
            FROM alphas a JOIN backtest_results b ON b.alpha_id=a.alpha_id
            WHERE a.sharpe>=1.58 AND a.fitness>=1.0 AND a.two_year_sharpe IS NULL
              AND a.is_ladder_sharpe>=1.58 AND b.region='EUR'
        ) WHERE rn=1""").fetchall()
    return [r[0] for r in rows]


async def test_pc(aid):
    from brain_api import brain_client
    pc = await brain_client.check_correlation(aid, correlation_type="production", threshold=0.7)
    prod = (pc.get("checks") or {}).get("production") or {}
    return prod.get("max_correlation")


async def main():
    conn = sqlite3.connect(DB, timeout=30)
    cur = conn.cursor()
    n = main_static(cur)
    conn.commit()
    print("软删除（第一批）:", n)
    total_dead = cur.execute("SELECT COUNT(*) FROM alphas WHERE disposition='DEAD'").fetchone()[0]
    print(f"disposition='DEAD' 累计: {total_dead}")

    # 补测：IND 2 颗 + EUR ladder 族代表
    targets = list(TEST_INDIV) + eur_ladder_reps(cur)
    print(f"\n补测 prod: {targets}")
    from brain_api import brain_client
    await brain_client.ensure_authenticated()
    for aid in targets:
        try:
            pc = await test_pc(aid)
            conn.execute("UPDATE alphas SET prod_correlation=? WHERE alpha_id=?", (pc, aid))
            conn.commit()
            verdict = "PASS" if (pc or 1) <= 0.7 else ("NEAR" if (pc or 1) <= 0.85 else "DEAD")
            print(f"  {aid}: prod={pc} -> {verdict}")
            if verdict == 'DEAD':
                cur.execute("""UPDATE alphas SET disposition='DEAD', dead_reason=?, dead_at=?
                               WHERE alpha_id=? AND """ + NOT_LIT,
                            (f"prod={pc}>0.85", datetime.now().isoformat(timespec='seconds'), aid))
                conn.commit()
        except Exception as e:
            print(f"  {aid}: ERROR {str(e)[:100]}")
    conn.close()


asyncio.run(main())
