# -*- coding: utf-8 -*-
"""prod_first_screen.py — 区域"未提交存量"的 prod 首筛（prod-first 纪律的机械执行）。

背景（2026-09-22 盘点）：全库 370 颗 IS 合格但未提交的存量里，**只有 97 颗测过 prod，
其中仅 6 颗 <0.7** —— 瓶颈是 prod 不是 IS。而 **ASI 95 颗从未测过**（该区已测的 2 颗分别是
0.5093 / 0.5116，明显低于 0.7），是唯一未被开发的大池子。本工具把"先测 prod 再谈打磨"
变成一次性可跑的筛选。

行为：
  - 枚举区域内 IS 合格 & 未提交的 alpha（口径：sharpe≥1.58 & fitness≥1.0 & 2Y≥1.58 & margin 非空 & 未 ACTIVE）
  - 逐条测 **prod（原始 GET 轮询：空体=平台仍在算，非空取 `max`；见 2026-09-22 修正）** 与 **self（本地计算）**
  - **断点续跑**：state 文件记录已测 alpha；网络失败不入 state（下次重试）
  - 测得的值**回写 alphas.prod_correlation / self_correlation / corr_checked_at**（测量落库，幂等）
  - 输出 CSV + JSON；打印「<0.7 可提交清单」

用法（需 MCP venv 的 Python）：
  world-quant-brain-mcp/.venv/Scripts/python.exe tools/prod_first_screen.py --region ASI
  ... --region ASI --limit 20        # 小批试点
  ... --region ASI --dry-run         # 只列待测，不发起请求
"""
import argparse
import asyncio
import json
import os
import sqlite3
import sys
from datetime import datetime

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "world-quant-brain-mcp"))
sys.path.insert(0, os.path.join(REPO, "src"))
sys.path.insert(0, os.path.join(REPO, "src"))
from wqb.db_conn import connect as db_connect  # 规范工厂（裸 sqlite3.connect 被守卫禁止）
DB = os.path.join(REPO, "data", "wqb.db")

IS_QUALIFIED = (
    "a.alpha_id IS NOT NULL AND a.sharpe>=1.58 AND a.fitness>=1.0 AND a.two_year_sharpe>=1.58 "
    "AND a.margin IS NOT NULL AND (a.platform_status IS NULL OR a.platform_status='UNSUBMITTED')"
)


def targets(region, limit=0, skip_measured=True):
    conn = db_connect(DB)
    conn.row_factory = sqlite3.Row
    extra = "AND a.prod_correlation IS NULL" if skip_measured else ""
    sql = (f"SELECT a.alpha_id, a.sharpe, a.fitness, a.two_year_sharpe, r.name AS region "
           f"FROM alphas a JOIN regions r ON r.id=a.region_id "
           f"WHERE r.name=? AND {IS_QUALIFIED} {extra} "
           f"ORDER BY a.sharpe DESC")
    if limit:
        sql += f" LIMIT {int(limit)}"
    rows = [dict(r) for r in conn.execute(sql, (region.upper(),))]
    conn.close()
    return rows


async def main():
    ap = argparse.ArgumentParser(description="区域未提交存量的 prod 首筛（可续跑）")
    ap.add_argument("--region", default="ASI")
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--state", default=None)
    ap.add_argument("--out", default=None)
    ap.add_argument("--sleep", type=float, default=0.6)
    ap.add_argument("--retries", type=int, default=3)
    ap.add_argument("--window-s", type=int, default=300, help="每颗 prod 轮询窗口（秒）")
    ap.add_argument("--poll-gap", type=int, default=15, help="轮询间隔（秒）")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--all-measured", action="store_true",
                    help="连已测过 prod 的也重测（默认只测 prod 为 NULL 的）")
    a = ap.parse_args()

    state_path = a.state or os.path.join(REPO, "logs", f"_prod_screen_{a.region.upper()}_state.json")
    out_path = a.out or os.path.join(REPO, "logs", f"prod_screen_{a.region.upper()}.json")

    rows = targets(a.region, a.limit, skip_measured=not a.all_measured)
    state = {}
    if os.path.isfile(state_path):
        with open(state_path, encoding="utf-8") as f:
            state = json.load(f)
    todo = [r for r in rows if r["alpha_id"] not in state]
    print(f"{a.region}: 待测 {len(rows)}（其中未处理 {len(todo)}）｜state={state_path}")
    if a.dry_run:
        for r in todo[:20]:
            print(f"  {r['alpha_id']:<9} S={r['sharpe']:.2f} F={r['fitness']:.2f} 2Y={r['two_year_sharpe']:.2f}")
        print(f"  …共 {len(todo)} 条")
        return

    from brain_api import brain_client
    bc = brain_client
    await bc.ensure_authenticated()

    measured, failed = 0, 0
    for i, r in enumerate(todo, 1):
        aid = r["alpha_id"]
        # 2026-09-22 修正：改用**原始端点轮询**取 prod——
        # 客户端 check_correlation 是同一 GET 的阻塞式轮询，且结果缓存依赖 Redis（本环境不可用）
        # → 每次回源、易「等死」。原始 GET 始终秒回（空体=平台仍在算），自己控节奏更稳。
        # 非空返回体形如 {schema, records(直方图), max, min}，**max 即 0.7 判定值**。
        prod = self_v = None
        for _ in range(int(a.window_s / a.poll_gap) or 1):
            try:
                r = await asyncio.wait_for(
                    bc._request("GET", f"{bc.base_url}/alphas/{aid}/correlations/prod"),
                    timeout=25)
                txt = (r.text or "").strip()
                if txt:
                    j = json.loads(txt)
                    if j.get("max") is not None:
                        prod = j["max"]
                        break
            except Exception:
                pass
            await asyncio.sleep(a.poll_gap)
        for _ in range(2):
            try:
                sc = await bc.check_self_correlation(aid, threshold=0.7)
                self_v = (sc or {}).get("max_correlation")
                if self_v is not None:
                    break
            except Exception:
                pass
            await asyncio.sleep(0.8)

        if prod is None:                      # prod 取不到 → 不入 state，下次重试
            failed += 1
            print(f"  [{i}/{len(todo)}] {aid} prod=取不到（下次重试）")
        else:
            measured += 1
            state[aid] = {"prod": prod, "self": self_v,
                          "at": datetime.now().isoformat(timespec="seconds")}
            with open(state_path, "w", encoding="utf-8") as f:
                json.dump(state, f, ensure_ascii=False, indent=1)
            # 测量落库（幂等：覆盖为本次实测值 + 记录核查时间）
            conn = db_connect(DB)
            conn.execute("UPDATE alphas SET prod_correlation=?, self_correlation=COALESCE(?, self_correlation), "
                         "corr_checked_at=?, prod_corr_source='prod_first_screen' WHERE alpha_id=?",
                         (prod, self_v, state[aid]["at"], aid))
            conn.commit(); conn.close()
            flag = "✅" if prod < 0.7 else "  "
            print(f"  [{i}/{len(todo)}] {aid} prod={prod:.4f} self={self_v} {flag}")
        await asyncio.sleep(a.sleep)

    # 汇总
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump({"region": a.region.upper(), "measured": state,
                   "updated": datetime.now().isoformat(timespec="seconds")},
                  f, ensure_ascii=False, indent=1)
    passing = {k: v for k, v in state.items() if v["prod"] is not None and v["prod"] < 0.7}
    print(f"\n本次测得 {measured}｜prod 取不到 {failed}（未入 state，重跑即续）")
    print(f"累计已测 {len(state)}｜**prod<0.7 = {len(passing)}**")
    for k, v in sorted(passing.items(), key=lambda kv: kv[1]["prod"]):
        print(f"  ✅ {k}: prod={v['prod']:.4f} self={v['self']}")
    print(f"结果 → {out_path}")


asyncio.run(main())
