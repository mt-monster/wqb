# -*- coding: utf-8 -*-
"""查看 selection 预览接口返回的原始字段，重点确认 os_start_date 的取值与类型。"""
import asyncio
import json
import sys
from pathlib import Path

WQ_ROOT = Path(r"D:\coding\traeCN_project\wqb")
sys.path.insert(0, str(WQ_ROOT / "world-quant-brain-mcp"))


async def main():
    from brain_api import BrainApiClient
    brain = BrainApiClient()
    await brain.ensure_authenticated()

    params = {
        "selection": "1",
        "instrumentType": "EQUITY",
        "region": "IND",
        "delay": 1,
        "selectionLimit": 300,
        "selectionHandling": "POSITIVE",
        "limit": 100,
        "offset": 0,
    }
    # 预览接口按 dateSubmitted 升序返回全区域 alpha，必须翻页拉全量
    rows, count = [], None
    while True:
        r = await brain._request(
            "GET", f"{brain.base_url}/simulations/super-selection", params=params)
        data = r.json()
        if count is None:
            count = data.get("count")
        batch = data.get("results") or []
        rows.extend(batch)
        if not data.get("next") or len(rows) >= (count or 0):
            break
        params["offset"] += 100
    print(f"count={count} fetched={len(rows)}")

    ind = [x for x in rows if ((x.get("settings") or {}).get("region") == "IND")]
    print(f"IND rows: {len(ind)}\n")

    if ind:
        print("--- 单条记录的顶层键 ---")
        print(sorted(ind[0].keys()))
        print()
        print("--- 单条完整样例（截断）---")
        print(json.dumps(ind[0], ensure_ascii=False)[:1200])
        print()

    print("--- 各 alpha 的关键字段 ---")
    for x in sorted(ind, key=lambda a: str(a.get("dateSubmitted") or "")):
        st = x.get("settings") or {}
        os_ = x.get("os") or {}
        print(f"{x.get('id'):<10} os_start_date={x.get('os_start_date')!r:<14} "
              f"dateSub={str(x.get('dateSubmitted'))[:10]}  "
              f"pCorr={(x.get('is') or {}).get('prodCorrelation')} "
              f"sCorr={(x.get('is') or {}).get('selfCorrelation')} "
              f"to={(x.get('is') or {}).get('turnover')} "
              f"neut={st.get('neutralization')}")


if __name__ == "__main__":
    asyncio.run(main())
