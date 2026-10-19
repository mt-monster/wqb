"""提交 alpha 并复核真实 status（避免「报错≠未发生」）。
用法: python tools/data-repair/submit_and_verify.py <ALPHA_ID> [--wait N]
- POST /alphas/{id}/submit（submit_alpha）
- 不信任返回体，按 flip 窗口轮询 GET /alphas/{id} 的 status，直到离开 UNSUBMITTED 或超时
- 超时也打印最后已知 status，绝不据报错补发
"""
import os
import sys
import asyncio
import json
import time

HERE = os.path.dirname(os.path.abspath(__file__))
WQB = os.path.dirname(os.path.dirname(HERE))
MCP = os.path.join(WQB, "world-quant-brain-mcp")
for p in (HERE, MCP):
    if p not in sys.path:
        sys.path.insert(0, p)

from brain_api import brain_client


async def get_status(aid):
    a = await brain_client.get_alpha_details(aid)
    reg = a.get("regular") or {}
    return {
        "status": a.get("status"),
        "code": reg.get("code"),
        "dateSubmitted": a.get("dateSubmitted"),
    }


async def main(aid, wait):
    await brain_client.ensure_authenticated()
    print(f"[pre] status before submit: {await get_status(aid)}")

    # 1) 发起提交（不信任返回体）
    try:
        r = await brain_client.submit_alpha(aid)
        print(f"[post] submit_alpha returned: {json.dumps(r, ensure_ascii=False)[:400]}")
    except Exception as e:
        print(f"[post] submit_alpha raised: {repr(e)[:300]}")
        print("[post] 按铁律：报错≠未发生，进入复核，不补发")

    # 2) 轮询复核真实 status（flip 窗口）
    deadline = time.time() + wait
    last = None
    while time.time() < deadline:
        await asyncio.sleep(20)
        try:
            last = await get_status(aid)
        except Exception as e:
            print(f"[poll] get_alpha_details err: {repr(e)[:200]}")
            continue
        print(f"[poll {int(wait-(deadline-time.time())):>3d}s left] status={last}")
        if last.get("status") and last["status"] != "UNSUBMITTED":
            print(f"[done] status 已离开 UNSUBMITTED -> {last}")
            return last
    print(f"[timeout] 窗口 {wait}s 内 status 仍为 {last}（可能仍在异步处理）")
    print("[note] 不据超时补发；稍后可用本脚本或 get_alpha_details 复核")
    return last


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage: submit_and_verify.py <ALPHA_ID> [--wait N]")
        sys.exit(2)
    aid = sys.argv[1]
    wait = 300
    if "--wait" in sys.argv:
        wait = int(sys.argv[sys.argv.index("--wait") + 1])
    asyncio.run(main(aid, wait))
