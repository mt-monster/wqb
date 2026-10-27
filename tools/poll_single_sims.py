"""轮询 batch_create_simulations 的单条仿真直到终态，打印指标表。

用法: python tools/poll_single_sims.py <tag>=<sim_id> [<tag>=<sim_id> ...] [--json out.json]
"""
import asyncio
import json
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _pyenv  # noqa: E402

_pyenv.bootstrap_paths()
from brain_api import brain_client  # noqa: E402

TERM = {"COMPLETE", "DONE", "WARNING", "ERROR", "CANCELLED", "FAILED", "FAIL"}


async def one(sid):
    await brain_client.ensure_authenticated()
    r = await brain_client._request("GET", f"{brain_client.base_url}/simulations/{sid}")
    if r.status_code != 200:
        return {"status": f"HTTP{r.status_code}"}
    j = r.json()
    st = str(j.get("status") or "").upper()
    is_ = j.get("is") or {}
    m = is_.get("metrics") or {}
    aid = j.get("alpha")
    # 单条仿真 GET 不带 is/metrics —— 必须再 GET /alphas/{id}
    if st in TERM and aid and not m:
        try:
            ra = await brain_client._request("GET", f"{brain_client.base_url}/alphas/{aid}")
            if ra.status_code == 200:
                m = (ra.json().get("is") or {})
        except Exception:
            pass
    cks = {c.get("name"): c for c in (m.get("checks") or []) if isinstance(c, dict)}
    ladder = (cks.get("IS_LADDER_SHARPE") or {}).get("value")
    if ladder is None:
        ladder = m.get("twoYearSharpe")
    return {
        "status": st,
        "alpha": aid,
        "sharpe": m.get("sharpe") or is_.get("sharpe"),
        "fitness": m.get("fitness") or is_.get("fitness"),
        "turnover": m.get("turnover") or is_.get("turnover"),
        "returns": m.get("returns"),
        "sub": m.get("subUniverseSharpe"),
        "robust": m.get("robustUniverseSharpe"),
        "ladder": ladder,
        "checks_fail": [c.get("name") for c in (m.get("checks") or []) if c.get("result") == "FAIL"],
    }


async def main(pairs, out):
    todo = dict(pairs)
    done = {}
    t0 = time.time()
    while todo and time.time() - t0 < 3600:
        for tag, sid in list(todo.items()):
            try:
                r = await one(sid)
            except Exception as e:
                continue
            if r.get("status") in TERM:
                done[tag] = r
                todo.pop(tag)
                print(f"[{time.strftime('%H:%M:%S')}] {tag} {r['status']} "
                      f"S={r.get('sharpe')} F={r.get('fitness')} TO={r.get('turnover')} "
                      f"2Y={r.get('ladder')} sub={r.get('sub')} rob={r.get('robust')}", flush=True)
        if todo:
            print(f"[{time.strftime('%H:%M:%S')}] 等待 {sorted(todo)} …", flush=True)
            await asyncio.sleep(60)
    if out:
        with open(out, "w", encoding="utf-8") as f:
            json.dump(done, f, ensure_ascii=False, indent=1)
    print("=== 汇总 ===", flush=True)
    for tag, r in sorted(done.items(), key=lambda kv: -(kv[1].get("sharpe") or 0)):
        print(f"{tag:8s} S={r.get('sharpe')} F={r.get('fitness')} 2Y={r.get('ladder')} "
              f"sub={r.get('sub')} rob={r.get('robust')} TO={r.get('turnover')} a={r.get('alpha')}",
              flush=True)


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    out = None
    if "--json" in sys.argv:
        out = sys.argv[sys.argv.index("--json") + 1]
        args = [a for a in args if a != out]
    pairs = [tuple(a.split("=", 1)) for a in args]
    asyncio.run(main(pairs, out))
