# -*- coding: utf-8 -*-
"""KOR SI 串行提交 v4（严格 1 颗一循环：提交 → 轮询 → 重测同族兄弟 → 下一颗）。

纪律：
  - 单账号单并发：本脚本绝不被其他平台请求任务并发调用。
  - 同族一次只提 1 颗；每提完 1 颗，重测该族剩余候选 prod（兄弟可能被抬）。
  - prod>=0.7 一律 fail-closed 跳过（MAX 铁律）。
  - 每颗提交前直轮询确认 prod<0.7；403 配额成本为零。

用法:
  python tmp_submit_serial.py --order=QPbxpJ8K,JjNAkqbn,vRrQ5Npr   # 指定序
  python tmp_submit_serial.py --dry
台账: tracking/KOR/candidates/submit_serial_log.jsonl
"""
import asyncio, json, sys, os, time
REPO = r"D:\coding\traeCN_project\wqb"
sys.path.insert(0, os.path.join(REPO, "world-quant-brain-mcp"))
LOG = os.path.join(REPO, "tracking/KOR/candidates/submit_serial_log.jsonl")

# 提交候选序（跳过 sector 轴族A；跨族 B/F/C/G）
DEFAULT_ORDER = [
    ("vRrQ5Npr", "F", "净额差/subindustry", 1.76, 1.18),
    ("JjNAkqbn", "B", "vec_sum比值/industry dl500", 2.31, 1.75),
    ("QPbxpJ8K", "C", "vec_sum比值/subindustry dl500", 1.73, 1.15),
    ("e7bjnPk6", "G", "vec_avg比值/subindustry dl500", 1.80, 1.22),
]


async def get_prod(bc, aid, window_s=300, gap=15):
    t0 = time.time()
    while time.time() - t0 < window_s:
        try:
            r = await bc._request("GET", f"https://api.worldquantbrain.com/alphas/{aid}/correlations/prod")
        except Exception:
            await asyncio.sleep(gap); continue
        if r.status_code == 200 and r.text.strip():
            try:
                d = r.json()
            except Exception:
                await asyncio.sleep(gap); continue
            mx = d.get("max")
            recs = d.get("records") or []
            if mx is None and recs:
                mx = max((x[2] for x in recs if len(x) > 2 and x[2] is not None), default=None)
            return mx
        await asyncio.sleep(gap)
    return None


async def main():
    dry = "--dry" in sys.argv
    order = DEFAULT_ORDER
    for a in sys.argv[1:]:
        if a.startswith("--order="):
            ids = a.split("=", 1)[1].split(",")
            m = {x[0]: x for x in DEFAULT_ORDER}
            order = [m[i] for i in ids if i in m]
    if dry:
        for o in order:
            print(o)
        return
    from brain_api import brain_client
    await brain_client.ensure_authenticated()
    done = []
    for aid, fam, desc, s, f in order:
        # 前置：实测 prod
        pr = await get_prod(brain_client, aid)
        print(f"\n[{fam}] {aid} pre-prod={pr} (S={s} F={f}) {desc}", flush=True)
        if pr is None:
            print("  skip: prod 未取到（超时）"); continue
        if pr >= 0.7:
            print("  skip: prod>=0.7 (MAX 铁律)"); continue
        # 提交
        r = await brain_client._request("POST", f"https://api.worldquantbrain.com/alphas/{aid}/submit")
        body = r.text.strip()
        print(f"  POST {r.status_code} len={len(body)}", flush=True)
        if body:
            try:
                j = r.json()
                fails = [c for c in (j.get("is") or {}).get("checks", []) if c.get("result") != "PASS"]
                for c in fails[:8]:
                    print("   ", json.dumps(c, ensure_ascii=False))
            except Exception:
                print("   ", body[:300])
            if r.status_code == 403:
                continue
        # 轮询
        status = None
        for i in range(40):
            await asyncio.sleep(20)
            rr = await brain_client._request("GET", f"https://api.worldquantbrain.com/alphas/{aid}")
            status = rr.json().get("status")
            print(f"   [{i*20}s] {status}", flush=True)
            if status in ("ACTIVE", "FAIL"):
                break
        rec = {"id": aid, "family": fam, "pre_prod": pr, "status": status, "ts": time.strftime("%Y-%m-%d %H:%M:%S")}
        with open(LOG, "a", encoding="utf-8") as fp:
            fp.write(json.dumps(rec, ensure_ascii=False) + "\n")
        done.append(rec)
    print("\n=== SUMMARY ===")
    print(json.dumps(done, ensure_ascii=False, indent=1))


asyncio.run(main())
