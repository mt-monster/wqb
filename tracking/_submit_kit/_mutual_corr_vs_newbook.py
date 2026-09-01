# -*- coding: utf-8 -*-
"""决定性证据：剩余候选 vs 今日新入池 4 颗（及彼此）的本地 PnL 互相关。

背景：平台 prod/self 计算用生产池快照，对 1h 前刚提交的 alpha 可能滞后
（0mwVnbkG 与 RR7OWQKd 同腿孪生但实测仍 0.5895，与理论矛盾）。
本地直接拉每日 PnL 序列做 Pearson 相关，不受快照滞后影响。

输出：research-data/mutual_corr_vs_newbook_20260901.json
"""
import asyncio
import json
import sys
from pathlib import Path

WQ_ROOT = Path(r"D:\coding\traeCN_project\wqb")
sys.path.insert(0, str(WQ_ROOT / "world-quant-brain-mcp"))

RD = WQ_ROOT / "research-data"
OUT = RD / "mutual_corr_vs_newbook_20260901.json"

NEW_OS = ["RR7OWQKd", "P07Ra2zJ", "58lEQMo1", "qMjLYVVP"]
CANDS = ["0mwVnbkG", "1YzOz8ZM", "58kALa11", "pwjpKGJ3", "Jj7ee6nO", "omqEE1pn"]


def pnl_series(rec):
    """recordsets/pnl -> {date: pnl} 累计值。"""
    series = {}
    try:
        records = rec.get("records") or []
        schema = rec.get("schema") or {}
        props = schema.get("properties") or []
        names = [p.get("name") for p in props]
        if not records or "date" not in names:
            return series
        di = names.index("date")
        pi = names.index("pnl") if "pnl" in names else 1
        for r in records:
            series[r[di]] = r[pi]
    except Exception:
        pass
    return series


async def fetch_pnl(brain, aid):
    try:
        rec = await brain.get_alpha_pnl(aid)
        return pnl_series(rec if isinstance(rec, dict) else {})
    except Exception as e:
        print(f"  [pnl-ERR] {aid}: {type(e).__name__} {str(e)[:80]}")
        return {}


def corr(a, b):
    ks = sorted(set(a) & set(b))
    if len(ks) < 60:
        return None
    da = [a[k] for k in ks]
    db = [b[k] for k in ks]
    # 日增量（累计 PnL -> daily pnl）
    da = [da[i] - (da[i - 1] if i else 0) for i in range(len(da))]
    db = [db[i] - (db[i - 1] if i else 0) for i in range(len(db))]
    n = len(da)
    ma, mb = sum(da) / n, sum(db) / n
    cov = sum((x - ma) * (y - mb) for x, y in zip(da, db))
    va = sum((x - ma) ** 2 for x in da) ** 0.5
    vb = sum((y - mb) ** 2 for y in db) ** 0.5
    if va == 0 or vb == 0:
        return None
    return cov / (va * vb)


async def main():
    from brain_api import BrainApiClient
    brain = BrainApiClient()
    await brain.ensure_authenticated()

    pnls = {}
    print("=== 拉取 PnL ===")
    for aid in NEW_OS + CANDS:
        pnls[aid] = await fetch_pnl(brain, aid)
        print(f"  {aid}: {len(pnls[aid])} 天")

    print("\n=== 互相关矩阵（行=候选，列=新 OS + 候选彼此）===")
    res = {}
    for c in CANDS:
        row = {}
        for other in NEW_OS + [x for x in CANDS if x != c]:
            if not pnls.get(c) or not pnls.get(other):
                continue
            r = corr(pnls[c], pnls[other])
            if r is not None:
                row[other] = round(r, 4)
        res[c] = row
        vs_os = {k: v for k, v in row.items() if k in NEW_OS}
        mx_os = max(vs_os.values()) if vs_os else None
        mx_all = max(row.values()) if row else None
        print(f"  {c:<10} vs新OS max={mx_os}  全表 max={mx_all}")
        for k, v in sorted(row.items(), key=lambda x: -abs(x[1]))[:4]:
            print(f"      {k:<10} {v}")

    OUT.write_text(json.dumps(res, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n[saved] {OUT}")


if __name__ == "__main__":
    asyncio.run(main())
