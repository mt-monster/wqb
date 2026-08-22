import asyncio, json, sys
sys.path.insert(0, 'world-quant-brain-mcp')
from brain_api import BrainApiClient

async def main():
    b = BrainApiClient()
    await b.ensure_authenticated()

    # 拉取最近提交的因子（不限日期，按 dateSubmitted 倒序），客户端筛选今天
    for stage in ("OS", "IS", "ALL"):
        try:
            data = await b.get_user_alphas(stage=stage, limit=60, order="-dateSubmitted")
        except Exception as e:
            print(f"stage={stage} ERROR:", repr(e))
            continue
        results = data.get("results", [])
        print(f"\n=== stage={stage} count(field)={data.get('count')} returned={len(results)} ===")
        today_hits = []
        for r in results:
            ds = r.get("dateSubmitted")
            # 今天命中
            if ds and ds.startswith("2026-08-22"):
                today_hits.append(r)
            # 仅打印前若干条用于观察格式
        print(f"今日(2026-08-22)命中数: {len(today_hits)}")
        for r in today_hits:
            print(json.dumps({
                "id": r.get("id"),
                "name": r.get("name"),
                "type": r.get("type"),
                "status": r.get("status"),
                "stage": r.get("stage"),
                "region": r.get("region"),
                "dateCreated": r.get("dateCreated"),
                "dateSubmitted": r.get("dateSubmitted"),
                "is_sharpe": (r.get("is") or {}).get("sharpe"),
                "is_fitness": (r.get("is") or {}).get("fitness"),
                "os_sharpe": (r.get("os") or {}).get("sharpe"),
            }, ensure_ascii=False))
        # 打印前 3 条的原始日期字段，确认格式
        if results:
            print("--- 样本日期格式 (前3) ---")
            for r in results[:3]:
                print(r.get("id"), "| dateCreated=", r.get("dateCreated"), "| dateSubmitted=", r.get("dateSubmitted"))

asyncio.run(main())
