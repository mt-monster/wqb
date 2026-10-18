"""只读采集单个 alpha 的现状：表达式、设置、is.checks 与关键指标、self/prod 相关性。
用法: python tools/data-repair/collect_alpha.py <ALPHA_ID>
"""
import os
import sys
import json
import asyncio

HERE = os.path.dirname(os.path.abspath(__file__))
WQB = os.path.dirname(os.path.dirname(HERE))
MCP = os.path.join(WQB, "world-quant-brain-mcp")
for p in (HERE, MCP):
    if p not in sys.path:
        sys.path.insert(0, p)

from brain_api import brain_client


async def main(aid):
    await brain_client.ensure_authenticated()
    a = await brain_client.get_alpha_details(aid)

    print("=== 顶层 ===")
    print("id:", a.get("id"))
    print("status:", a.get("status"), "| type:", a.get("type"), "| stage:", a.get("stage"))
    print("code:", ((a.get("regular") or {}).get("code") or a.get("code") or ""))
    print("settings:", json.dumps(a.get("settings") or {}, ensure_ascii=False))

    isd = a.get("is") or {}
    print("\n=== is 关键指标 ===")
    for k in ("sharpe", "fitness", "twoYearSharpe", "turnover", "margin",
              "prodCorrelation", "selfCorrelation", "investabilityConstrained"):
        if k == "investabilityConstrained":
            v = (isd.get(k) or {}).get("sharpe")
            print(f"  {k}.sharpe: {v}")
        else:
            print(f"  {k}: {isd.get(k)}")
    print("  operatorCount:", a.get("operatorCount") or isd.get("operatorCount"))

    print("\n=== is.checks ===")
    for x in (isd.get("checks") or []):
        print("  %-30s %-8s val=%-10s lim=%s" % (
            x.get("name"), x.get("result"), x.get("value"), x.get("limit")))

    # OS 段
    osd = a.get("os") or {}
    if osd:
        print("\n=== os ===")
        print("  sharpe:", osd.get("sharpe"), "| fitness:", osd.get("fitness"),
              "| turnover:", osd.get("turnover"))

    # 落盘原始以备用
    out = os.path.join(WQB, "results", f"alpha_{aid}_raw.json")
    json.dump(a, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=2, default=str)
    print(f"\n[raw] -> {out}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage: collect_alpha.py <ALPHA_ID>")
        sys.exit(2)
    asyncio.run(main(sys.argv[1]))
