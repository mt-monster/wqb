#!/usr/bin/env python
"""验证平台 PATCH `osmosisPoints: null` 是否能把点数真正清零（而非回退到 1）。

背景（2026-10-21）：本仓库 `osmosis_allocate.py::zero_others` 发 `{"osmosisPoints": 0}`
被平台 400 拒（"greater than or equal to 1"），只能回退到最小值 1 ⇒ 每个 scope 的
实际点数和 = 100,000 + 计划外颗数（实测 IND/KOR 各 +12、GBR +3、GLB +2、DEU +1）。

论坛帖 DL61056《Osmosis 分数自动分配脚本》评论区 CM59456（2026-09-21）实证：
    "我这边 PATCH {"osmosisPoints":0} 会返回 400，改写 null 才是 200。"
若成立，则可用 null 彻底清零残留，无需 balance_osmosis.py 事后扣回。

本脚本只挑 **当前点数恰好为 1** 的 alpha（= 上一轮回退产生的计划外残留）做实验，
失败自动回写 1，正常情况下无副作用。

用法：
  python tools/data-repair/verify_zero_null.py            # 只列出候选，不动平台
  python tools/data-repair/verify_zero_null.py --apply    # 实测一颗
"""
from __future__ import annotations

import argparse
import asyncio
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "world-quant-brain-mcp"))


def purge() -> int:
    from wqb.db_conn import connect
    con = connect(readonly=False)
    n = con.execute("DELETE FROM api_cache WHERE cache_key LIKE 'user_alphas%'").rowcount
    con.commit()
    con.close()
    return n


async def fetch() -> list:
    from brain_api import brain_client
    rows: list = []
    off = 0
    for _ in range(200):
        r = await brain_client.get_user_alphas(stage="OS", limit=100, offset=off)
        pl = r["result"] if isinstance(r, dict) and isinstance(r.get("result"), dict) else r
        res = pl.get("results", []) or []
        if not res:
            break
        rows.extend(res)
        if not pl.get("next"):
            break
        off += 100
    return rows


def pts_of(rec: dict):
    v = rec.get("osmosisPoints")
    return v


async def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true", help="真正 PATCH 一颗做实验")
    ap.add_argument("--id", default=None, help="指定要实验的 alpha id（默认取第一个候选）")
    args = ap.parse_args()

    # 清缓存，确保拿到最新的 osmosisPoints
    n = purge()
    print(f"[cache] 已清 user_alphas 缓存 {n} 条", file=sys.stderr)

    rows = await fetch()
    print(f"[fetch] 平台 OS 池共 {len(rows)} 颗", file=sys.stderr)

    ones = []
    for r in rows:
        if pts_of(r) == 1:
            st = (r.get("settings") or {})
            ones.append({
                "id": r.get("id"),
                "type": r.get("type"),
                "status": r.get("status"),
                "region": st.get("region"),
                "delay": st.get("delay"),
            })

    print(f"\n[候选] osmosisPoints == 1 的 alpha 共 {len(ones)} 颗：")
    for o in ones[:40]:
        print(f"  {o['id']:<12} {str(o['type']):<8} {str(o['status']):<10} "
              f"{o['region']}/D{o['delay']}")
    if len(ones) > 40:
        print(f"  ... 其余 {len(ones) - 40} 颗略")

    if not ones:
        print("\n没有 points==1 的候选，无法做无损实验。", file=sys.stderr)
        return 1

    if not args.apply:
        print("\n[preview] 未写入平台。加 --apply 实测第一颗。")
        return 0

    target = None
    if args.id:
        target = next((o for o in ones if o["id"] == args.id), None)
        if target is None:
            print(f"\n[error] {args.id} 不在 points==1 候选里（它不是残留，拒绝实验）。",
                  file=sys.stderr)
            return 1
    else:
        target = ones[0]
    aid = target["id"]
    from brain_api import brain_client
    await brain_client.ensure_authenticated()
    base = brain_client.base_url

    print(f"\n[test] 对 {aid} 依次尝试 null / 0 ……")

    for payload in ({"osmosisPoints": None}, {"osmosisPoints": 0}):
        label = "null" if payload["osmosisPoints"] is None else "0"
        try:
            resp = await brain_client._request("PATCH", f"{base}/alphas/{aid}",
                                               json=payload)
            code = resp.status_code
            text = (getattr(resp, "text", "") or "")[:240]
            echo = None
            try:
                echo = resp.json().get("osmosisPoints", "<absent>")
            except Exception:
                pass
            print(f"  PATCH {label:<4} -> HTTP {code} | echo osmosisPoints={echo} | {text}")
            if code < 400:
                # 回读确认
                await asyncio.sleep(2)
                r2 = await brain_client._request("GET", f"{base}/alphas/{aid}")
                try:
                    now = r2.json().get("osmosisPoints", "<absent>")
                except Exception:
                    now = "<parse-fail>"
                print(f"  GET  回读 osmosisPoints={now}")
                if now in (None, 0):
                    print(f"\n[结论] PATCH {label} 可以把点数清零（回读 = {now}）。"
                          f"\n       ⇒ zero_others 应改为发 {label}，可消除每 scope 的 +N 残留。")
                    return 0
                else:
                    print(f"\n[结论] PATCH {label} 返回成功但回读仍为 {now}，未真正清零。")
                    return 2
        except Exception as ex:  # noqa: BLE001
            print(f"  PATCH {label} -> EXC {ex}")

    # 全部失败：恢复为 1
    print("\n[restore] 两种写法均失败，回写 1 ……")
    resp = await brain_client._request("PATCH", f"{base}/alphas/{aid}",
                                       json={"osmosisPoints": 1})
    print(f"  restore HTTP {resp.status_code}")
    return 3


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main()))
