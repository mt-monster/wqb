"""批量测 prod 相关性（平台单并发端点，序列化 + 退避）。
用法: python tracking/IND/scripts/_prod_batch.py <aid> [<aid> ...]
     加 --raw 打印单条完整返回（调试用）。
"""
import asyncio, sys, json
sys.path.insert(0, "world-quant-brain-mcp")
from brain_api import brain_client as brain


def extract(res):
    if not isinstance(res, dict):
        return None
    ch = (res.get("checks") or {}).get("production") or {}
    for k in ("max_correlation", "max"):
        if ch.get(k) is not None:
            return ch[k]
    return res.get("max")


async def one(aid):
    for i in range(5):
        try:
            res = await brain.check_correlation(aid, correlation_type="production", threshold=0.7)
            return res
        except Exception as e:
            msg = f"{type(e).__name__}:{str(e)[:70]}"
            await asyncio.sleep(min(20 * (i + 1), 120))
    return {"error": msg}


async def main(argv):
    raw = "--raw" in argv
    ids = [a for a in argv if not a.startswith("--")]
    await brain.ensure_authenticated()
    out = []
    for aid in ids:
        res = await one(aid)
        if raw:
            print(json.dumps(res, ensure_ascii=False)[:900])
            continue
        mx = extract(res)
        flag = "OK" if (isinstance(mx, (int, float)) and mx < 0.7) else ("PEND" if mx is None else "FAIL")
        note = ""
        if mx is None and isinstance(res, dict):
            ch = (res.get("checks") or {}).get("production") or {}
            note = str(ch.get("status") or ch.get("reason") or res.get("error") or "")[:50]
        print(f"{aid:12s} prod={mx!s:>7s}  {flag}  {note}")
        out.append({"aid": aid, "prod": mx, "flag": flag, "note": note})
        await asyncio.sleep(5)
    json.dump(out, open("logs/_prod_latest.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("saved -> logs/_prod_latest.json")


asyncio.run(main(sys.argv[1:]))
