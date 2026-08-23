# -*- coding: utf-8 -*-
"""sa_probe.py - SuperAlpha 组件池探针（替代 probe_kor_sa.py / tracking/_scratch/probe_sa2_*.py）。

拉取指定区域全部 REGULAR alpha（IS/OS 双阶段翻页），统计 ACTIVE 组件数，
输出 GO/BLOCKED verdict——SUPER alpha 硬前置是 ≥10 颗同区域 ACTIVE REGULAR。

用法:
  python tools/sa_probe.py --region KOR
  python tools/sa_probe.py --region MEA --min 10 --json research-data/mea_sa_pool.json
  python tools/sa_probe.py --region USA --detail

退出码: 0=GO（eligible >= min）, 1=BLOCKED
运行环境: 使用 MCP venv（`$WQ_PY` 或 world-quant-brain-mcp/.venv），依赖 brain_api。
"""
import argparse
import asyncio
import json
import os
import sys


def _mcp_venv_python():
    env = os.environ.get("WQ_PY")
    cands = [env, r"d:\coding\traeCN_project\wqb\world-quant-brain-mcp\.venv\Scripts\python.exe"]
    for c in cands:
        if c and os.path.isfile(c):
            return c
    return sys.executable


def _bootstrap():
    py = _mcp_venv_python()
    if py and os.path.abspath(py) != os.path.abspath(sys.executable):
        os.execv(py, [py] + sys.argv)
    mcp = os.environ.get("WQ_MCP_DIR", r"d:\coding\traeCN_project\wqb\world-quant-brain-mcp")
    sys.path.insert(0, mcp)


async def fetch_pool(brain, region, limit_hint):
    """按 IS/OS 分阶段翻页拉取 REGULAR 池（平台 offset 窗口上限 ~1000）。"""
    pool = []
    for stage in ("OS", "IS"):
        off = 0
        while off < limit_hint:
            d = await brain.get_user_alphas(stage=stage, limit=50, alpha_type="REGULAR",
                                            order="-dateSubmitted", offset=off)
            res = d.get("results") or []
            if not res:
                break
            for r in res:
                s = r.get("settings") or {}
                if (s.get("region") or r.get("region")) != region:
                    continue
                pool.append({
                    "id": r["id"], "stage": stage, "name": r.get("name"),
                    "status": r.get("status"), "type": r.get("type"),
                    "sharpe": (r.get("is") or {}).get("sharpe"),
                    "fitness": (r.get("is") or {}).get("fitness"),
                    "dateSubmitted": r.get("dateSubmitted"),
                })
            if len(res) < 50:
                break
            off += 50
    # 去重（同一 alpha 不会同时出现在 IS/OS，防御性处理）
    seen, dedup = set(), []
    for a in pool:
        if a["id"] not in seen:
            seen.add(a["id"])
            dedup.append(a)
    return dedup


async def main():
    ap = argparse.ArgumentParser(description="SuperAlpha 组件池探针（≥10 ACTIVE REGULAR 硬前置）")
    ap.add_argument("--region", required=True, help="区域代码，如 KOR/USA/MEA")
    ap.add_argument("--min", type=int, default=10, help="GO 阈值（默认 10）")
    ap.add_argument("--json", dest="json_out", help="池清单落盘路径（如 research-data/<region>_sa_pool.json）")
    ap.add_argument("--limit-hint", type=int, default=950, help="单阶段最大翻页量（平台上限约 1000）")
    ap.add_argument("--detail", action="store_true", help="逐条打印全部候选")
    a = ap.parse_args()

    _bootstrap()
    from brain_api import BrainApiClient  # noqa: F402
    brain = BrainApiClient()
    await brain.ensure_authenticated()

    pool = await fetch_pool(brain, a.region, a.limit_hint)
    by_stage = {}
    for p in pool:
        by_stage.setdefault(p["stage"], []).append(p)

    # eligible：status ACTIVE 或处于 IS/OS 阶段（平台对已提交且在跑的 alpha 均计 ACTIVE）
    eligible = [p for p in pool if p["status"] == "ACTIVE" or p["stage"] in ("IS", "OS")]
    verdict = "GO" if len(eligible) >= a.min else "BLOCKED"

    print(f"=== {a.region} REGULAR pool: {len(pool)} "
          f"(OS {len(by_stage.get('OS', []))} / IS {len(by_stage.get('IS', []))}) ===")
    if a.detail:
        for st in ("OS", "IS"):
            print(f"\n--- stage={st} ---")
            for p in by_stage.get(st, []):
                print(f"  {p['id']}  status={p['status']}  sharpe={p.get('sharpe')} "
                      f"fitness={p.get('fitness')}  sub={p.get('dateSubmitted')}")
    print(f"\n=== eligible (ACTIVE/IS/OS) count: {len(eligible)} (need >= {a.min}) ===")
    print(f"VERDICT: {verdict}"
          + ("" if verdict == "GO" else f" (还差 {a.min - len(eligible)} 颗)"))

    if a.json_out:
        os.makedirs(os.path.dirname(a.json_out) or ".", exist_ok=True)
        json.dump({"region": a.region, "total": len(pool), "eligible": len(eligible),
                   "need": max(0, a.min - len(eligible)), "verdict": verdict,
                   "pool": pool}, open(a.json_out, "w", encoding="utf-8"),
                  ensure_ascii=False, indent=2)
        print(f"\n[out] {a.json_out}")
    sys.exit(0 if verdict == "GO" else 1)


if __name__ == "__main__":
    asyncio.run(main())