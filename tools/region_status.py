# -*- coding: utf-8 -*-
"""区域状态记分板（P1-6：区域状态单一事实源）。

收敛三个原型的同一需求：
  - brain-next-move-analysis §5.5 区域饱和度检测（日报消费）
  - wq-brain-campaign-matrix 配置包 prod_saturation / prod_risk 标注（S-PRE 消费）
  - 数据集记分板（防止重复挖已饱和 dataset）

数据源（全部本地 DB / 文件，零平台请求、零配额）：
  - backtest_results ：每区回测量与 S>=1.58 达标数（研究仿真口径）
  - alphas           ：platform_status=ACTIVE 存量（本地口径，注意与平台全量有偏差）
  - registry_empirical（layer=campaign）：untried / in_progress / exhausted 分布
  - waves            ：波次投入
  - region profile   ：Claude/skills/wq-brain-ra-pipeline/references/regions/<R>.md 的
                       entry_verdict（active/probe-only/frozen）

退出码：0=成功。默认只读；--rotate --write-ledger 会写 region_rotation 台账（幂等 upsert）。

轮转模式（--rotate）：当前区证实结构性饱和 → 按证据（产出率/可行库存/prod 墙/战役穷尽/
  profile entry_verdict）排序推荐下一区并承接过闸目标。判定与打分逻辑的**单一事实源**在
  ``src/wqb/region_rotation.py``，本工具只做 DB 采集 + 展示 + 可选台账写入；同一逻辑亦经
  ``mcp__wqb-db__region_rotation`` 暴露给 Agent/skill。
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sqlite3
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB = os.path.join(REPO, "data", "wqb.db")
PROFILE_DIR = os.path.join(REPO, "Claude", "skills", "wq-brain-ra-pipeline",
                           "references", "regions")


def _entry_verdict(region: str) -> str:
    path = os.path.join(PROFILE_DIR, f"{region}.md")
    if not os.path.exists(path):
        return "(no-profile)"
    m = re.search(r"^entry_verdict:\s*(\S+)",
                  open(path, encoding="utf-8", errors="replace").read(), re.M)
    return m.group(1) if m else "(unset)"


def region_status(conn: sqlite3.Connection, region: str) -> dict:
    bt_total, bt_pass = conn.execute(
        "SELECT COUNT(*), COALESCE(SUM(CASE WHEN sharpe>=1.58 THEN 1 ELSE 0 END),0) "
        "FROM backtest_results WHERE region=?", (region,)).fetchone()
    active = conn.execute(
        "SELECT COUNT(*) FROM alphas a JOIN regions r ON r.id=a.region_id "
        "WHERE r.name=? AND UPPER(COALESCE(a.platform_status,''))='ACTIVE'",
        (region,)).fetchone()[0]
    waves = conn.execute(
        "SELECT COUNT(*) FROM waves w JOIN regions r ON r.id=w.region_id WHERE r.name=?",
        (region,)).fetchone()[0]
    camp = {"untried": 0, "in_progress": 0, "exhausted": 0}
    try:
        for (payload,) in conn.execute(
                "SELECT payload FROM registry_empirical WHERE region=? AND layer='campaign'",
                (region,)):
            try:
                st = (json.loads(payload) or {}).get("status")
            except Exception:
                continue
            if st in camp:
                camp[st] += 1
    except sqlite3.OperationalError:
        pass
    total_camp = sum(camp.values())
    exhausted_pct = round(100 * camp["exhausted"] / total_camp, 1) if total_camp else 0.0
    hit_rate = round(100 * bt_pass / bt_total, 1) if bt_total else 0.0
    # 动作建议（与 next-move §5.5 / campaign-matrix 口径一致）
    if bt_pass >= 10:
        action = "继续（注意 PROD 同质风险→正交方向）"
    elif exhausted_pct >= 80 and total_camp >= 5:
        action = "冻结/转区（exhausted 占比过高）"
    elif camp["untried"] > 0 and bt_total < 20:
        action = "开战役候选（untried 充足、投入不足）"
    else:
        action = "继续观察"
    return {
        "region": region,
        "entry_verdict": _entry_verdict(region),
        "backtested": bt_total,
        "pass_ge_158": bt_pass,
        "pass_rate_pct": hit_rate,
        "active_local": active,
        "waves": waves,
        "campaigns": camp,
        "exhausted_pct": exhausted_pct,
        "suggested_action": action,
    }


def _upsert_ledger(conn, region, key, value):
    """幂等写 ledger_kv(region,key,value)。"""
    import json as _json
    from datetime import datetime, timezone
    now = datetime.now(timezone.utc).isoformat()
    conn.execute(
        "INSERT INTO ledger_kv(region,key,value,created_at,updated_at) VALUES(?,?,?,?,?) "
        "ON CONFLICT(region,key) DO UPDATE SET value=excluded.value, updated_at=excluded.updated_at",
        (region, key, _json.dumps(value, ensure_ascii=False), now, now))
    conn.commit()


def _rotate(conn, a) -> int:
    """区域轮转决策：当前区饱和 → 推荐下一区（逻辑源自 wqb.region_rotation）。"""
    src = os.path.join(REPO, "src")
    if src not in sys.path:
        sys.path.insert(0, src)
    from wqb.region_rotation import (gather_all_regions, gather_region_metrics,
                                     recommend_rotation)
    current = (a.current or (a.regions.split(",")[0] if a.regions else None) or "EUR").strip().upper()
    names = [r[0] for r in conn.execute("SELECT name FROM regions")]
    verdicts = {r: _entry_verdict(r) for r in names}
    allm = gather_all_regions(conn, verdicts=verdicts)
    if current not in allm:  # 当前区可能无活动痕迹，仍补采以给出饱和判定
        allm[current] = gather_region_metrics(conn, current,
                                              entry_verdict=verdicts.get(current))
    rec = recommend_rotation(current, allm, target=a.target)
    cs = rec.get("current_saturation") or {}

    print(f"=== 区域轮转决策 current={current} target={rec.get('carry_target')} ===")
    print(f"当前区判定: {cs.get('verdict')}  strong={cs.get('strong')}  medium={cs.get('medium')}")
    for r in (cs.get("reasons") or []):
        print(f"  - {r}")
    if cs.get("data_caveat"):
        print(f"  [caveat] {cs['data_caveat']}")
    print(f"\nshould_rotate = {rec['should_rotate']}   all_saturated = {rec.get('all_saturated')}")
    print(f"推荐转入区: {rec.get('to_region')}")
    print(f"理由: {rec.get('reason')}")
    print(f"下一步: {rec.get('next_action')}")

    if rec.get("ranked"):
        print(f"\n{'rank':>4} {'region':7s} {'score':>7s} {'verdict':10s} {'yield':>6s} "
              f"{'feasUnsub':>9s} {'exh%':>5s} {'prodWall%':>9s} {'prof':11s}")
        for i, r in enumerate(rec["ranked"], 1):
            yr = f"{r['yield_rate']:.3f}" if r['yield_rate'] is not None else "  -  "
            pwr = f"{r['prod_wall_ratio']:.2f}" if r['prod_wall_ratio'] is not None else "  -  "
            print(f"{i:>4} {r['region']:7s} {r['score']:>7.4f} {r['verdict']:10s} {yr:>6s} "
                  f"{r['feasible_unsubmitted']:>9} {r['exhausted_pct']*100:4.0f}% {pwr:>9s} "
                  f"{str(r['entry_verdict']):11s}")

    payload = {
        "from_region": rec.get("from_region"), "to_region": rec.get("to_region"),
        "should_rotate": rec.get("should_rotate"), "all_saturated": rec.get("all_saturated"),
        "carry_target": rec.get("carry_target"), "reason": rec.get("reason"),
        "next_action": rec.get("next_action"), "current_verdict": cs.get("verdict"),
        "current_reasons": cs.get("reasons"), "data_caveat": cs.get("data_caveat"),
        "ranked": [{"region": r["region"], "score": r["score"], "verdict": r["verdict"],
                    "yield_rate": r["yield_rate"],
                    "feasible_unsubmitted": r["feasible_unsubmitted"]}
                   for r in (rec.get("ranked") or [])[:8]],
    }
    if a.json:
        print("\n" + json.dumps(payload, ensure_ascii=False, indent=1))
    if a.write_ledger:
        if not rec.get("should_rotate"):
            print(f"\n[ledger] 未轮转（{current} 未饱和），不写台账。")
        else:
            _upsert_ledger(conn, current, "region_rotation", payload)
            print(f"\n[ledger] 已写 region_rotation 台账（region={current}）：承接目标 "
                  f"{rec.get('carry_target')} → {rec.get('to_region')}。")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="区域状态记分板（本地 DB 驱动，零平台请求）")
    ap.add_argument("--regions", default=None,
                    help="逗号分隔；默认取 DB 内有 backtest/波次记录的全部区域")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--rotate", action="store_true",
                    help="区域轮转决策：当前区饱和→推荐下一区（逻辑源 wqb.region_rotation）")
    ap.add_argument("--current", default=None,
                    help="--rotate 的当前区（默认取 --regions 首个，再默认 EUR）")
    ap.add_argument("--target", type=int, default=None,
                    help="--rotate 承接的过闸目标数（写入 carry_target，如 20）")
    ap.add_argument("--write-ledger", action="store_true",
                    help="--rotate 时把决策幂等写入 ledger_kv(region=<current>, key=region_rotation)")
    a = ap.parse_args()
    if not os.path.exists(DB):
        print(f"[region_status] DB 不存在：{DB}", file=sys.stderr)
        return 1
    conn = sqlite3.connect(DB)
    if a.rotate:
        try:
            return _rotate(conn, a)
        finally:
            conn.close()
    try:
        if a.regions:
            regions = [r.strip().upper() for r in a.regions.split(",") if r.strip()]
        else:
            regions = [r[0] for r in conn.execute(
                "SELECT DISTINCT region FROM backtest_results WHERE region IS NOT NULL "
                "ORDER BY region")]
        rows = [region_status(conn, r) for r in regions]
    finally:
        conn.close()

    if a.json:
        print(json.dumps({"regions": rows,
                          "note": "backtest/active 为本地口径，平台全量以 sync_platform_alphas 为准"},
                         ensure_ascii=False, indent=1))
        return 0
    hdr = (f'{"region":7s} {"verdict":11s} {"回测":>5s} {"达标":>4s} {"命中率":>6s} '
           f'{"ACTIVE":>6s} {"waves":>5s} {"exhaust%":>8s} 建议')
    print(hdr)
    print("-" * 88)
    for r in rows:
        print(f'{r["region"]:7s} {r["entry_verdict"]:11s} {r["backtested"]:5d} '
              f'{r["pass_ge_158"]:4d} {r["pass_rate_pct"]:5.1f}% {r["active_local"]:6d} '
              f'{r["waves"]:5d} {r["exhausted_pct"]:7.1f}% {r["suggested_action"]}')
    print("-" * 88)
    print("消费方：next-move §5.5 日报 / campaign-matrix 配置包标注 / 波次规划。"
          "本地口径偏差提醒见输出 JSON note。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
