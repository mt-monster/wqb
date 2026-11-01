# -*- coding: utf-8 -*-
"""多 alpha prod **无锁批量**探测：抓端点/账号级单并发槽恢复的窗口期。

为什么需要它
------------
`prod_wait.py` 一次只测一颗，而 prod 端点是**账号级单并发**：
- 兄弟会话（如并行的 GBR 战役）长期占槽时，本机有锁路径会一直 correlation_busy；
- 端点自身故障时，`/alphas/{id}/correlations/prod` 返回 **200 + 空体**。

两种情况下都不能判断「这颗 alpha 不行」，只能等窗口。串行排 5 颗 × 单颗 90-240s
远超单次会话耐心；本工具用**无锁只读 peek**（不申请 correlation_slot、不写
inflight、不触发平台重算），每个周期对每颗各打一次，谁先到就先落盘。

与 prod_wait.py 的关系
----------------------
复用其 `parse()` 与输出格式（results/prod_peek_<alpha>.json），区别是：
1. 接收多个 alpha，循环轮询而非死等一颗；
2. 已取到的自动跳过，未取到的继续；
3. 结束时打印「已取到 / 仍缺」清单，供上层直接判断。

用法
----
    python tools/prod_peek_batch.py --alphas MPYoQ1E6,88vJ1YKa,e75eewKO \
        --minutes 45 --interval 45

退出码：0 = 全部取到；2 = 仍有缺失（不是错误，是端点/槽未恢复）。
"""
import argparse
import asyncio
import json
import os
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))
sys.path.insert(0, os.path.join(ROOT, "world-quant-brain-mcp"))

from prod_wait import parse  # noqa: E402
from brain_api import BrainApiClient  # noqa: E402


async def _one(client, alpha_id):
    """单次无锁探测。返回 (value, note)。

    value is None 表示本次没拿到；note 说明原因，便于日志分辨
    「空体（平台仍在算）/ 端点坏」与「有体但解析不出 max」。
    """
    try:
        r = await client._request("GET", f"/alphas/{alpha_id}/correlations/prod")
    except Exception as e:                                    # noqa: BLE001
        return None, f"EXC {type(e).__name__}: {str(e)[:100]}"
    code = getattr(r, "status_code", None)
    txt = (getattr(r, "text", "") or "").strip()
    if code != 200:
        return None, f"HTTP {code} {txt[:100]}"
    if not txt:
        return None, "空体"
    try:
        j = json.loads(txt)
    except Exception:                                         # noqa: BLE001
        return None, f"非JSON {txt[:100]}"
    v = parse(j)
    if v is None:
        return None, f"有体无max {txt[:100]}"
    return v, "ok"


async def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--alphas", required=True,
                    help="逗号分隔的 alpha id 列表")
    ap.add_argument("--minutes", type=float, default=45,
                    help="总时长上限（默认 45 分钟，须小于后台任务 60 分钟上限）")
    ap.add_argument("--interval", type=float, default=45,
                    help="每轮之间间隔秒（默认 45；生产池是异步队列，太快无收益）")
    args = ap.parse_args()

    ids = [x.strip() for x in args.alphas.split(",") if x.strip()]
    if not ids:
        print("没有 alpha id", flush=True)
        return 2

    outdir = os.path.join(ROOT, "results")
    os.makedirs(outdir, exist_ok=True)

    client = BrainApiClient()
    await client.ensure_authenticated()

    done = {}
    deadline = time.time() + args.minutes * 60
    cycle = 0
    while time.time() < deadline and len(done) < len(ids):
        cycle += 1
        left = int(deadline - time.time())
        pending = [a for a in ids if a not in done]
        print(f"\n=== 第 {cycle} 轮 | 待取 {len(pending)} 颗 | 剩余 {left}s ===", flush=True)
        for alpha_id in pending:
            v, note = await _one(client, alpha_id)
            if v is None:
                print(f"  {alpha_id}: {note}", flush=True)
                continue
            done[alpha_id] = v
            path = os.path.join(outdir, f"prod_peek_{alpha_id}.json")
            with open(path, "w", encoding="utf-8") as fh:
                json.dump({"alpha_id": alpha_id, "prod": v,
                           "at": time.strftime("%F %T"), "source": "no-lock peek batch"},
                          fh, ensure_ascii=False, indent=1)
            print(f"  {alpha_id}: ★ prod = {v}  -> {os.path.basename(path)}", flush=True)
        if len(done) >= len(ids):
            break
        await asyncio.sleep(max(10.0, args.interval))

    print("\n" + "=" * 60, flush=True)
    print(f"已取到 {len(done)}/{len(ids)}：", flush=True)
    for a in ids:
        print(f"  {a}: {done.get(a, '缺')}", flush=True)
    if len(done) < len(ids):
        print("\n仍缺的说明 prod 端点/账号槽未恢复（不是这些 alpha 的问题）。", flush=True)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
