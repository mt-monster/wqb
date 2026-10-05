# -*- coding: utf-8 -*-
"""GLB 串行提交器（放在 tracking/ 下避免被外部清理进程删除；logs/ 会被清）。

用法: python tracking/GLB/scripts/_serial_runner.py <spec.json> <tag_prefix>
spec.json 形如 [{"path":"...b1.txt","decay":10,...}, ...]（submit_batch.py --spec 格式）。
checkpoint: tracking/GLB/scripts/_serial_<tag_prefix>_ckpt.json（断点续跑）。
"""
import subprocess, time, sys, re, asyncio, json, os

ROOT = r"D:/coding/traeCN_project/wqb"
sys.path.insert(0, os.path.join(ROOT, "world-quant-brain-mcp"))
sys.path.insert(0, ROOT)
from brain_api import BrainApiClient

TOOL = os.path.join(ROOT, "tools", "submit_batch.py")


def main():
    spec_path = sys.argv[1]
    prefix = sys.argv[2]
    specs = json.load(open(spec_path, encoding="utf-8"))
    ckpt_path = os.path.join(ROOT, "tracking", "GLB", "scripts", f"_serial_{prefix}_ckpt.json")
    logp = os.path.join(ROOT, "tracking", "GLB", "scripts", f"_serial_{prefix}.log")

    def log(m):
        line = f"[{time.strftime('%H:%M:%S')}] {m}"
        with open(logp, "a", encoding="utf-8") as f:
            f.write(line + "\n")
        print(line, flush=True)

    def load_ckpt():
        if os.path.exists(ckpt_path):
            try:
                return json.load(open(ckpt_path, encoding="utf-8"))
            except Exception:
                return {}
        return {}

    def save_ckpt(d):
        tmp = ckpt_path + ".tmp"
        json.dump(d, open(tmp, "w", encoding="utf-8"))
        os.replace(tmp, ckpt_path)

    async def wait_batch(sid, timeout=3600):
        c = BrainApiClient()
        await c.ensure_authenticated()
        t0 = time.time()
        last = None
        while time.time() - t0 < timeout:
            try:
                r = await c._request("GET", f"/simulations/{sid}")
                if r.status_code == 200:
                    d = r.json()
                    st = d.get("status"); pr = d.get("progress"); ch = d.get("children") or []
                    if ch and isinstance(ch[0], dict):
                        done = sum(1 for x in ch if x.get("status") in ("COMPLETE", "ERROR", "FAIL", "WARNING"))
                    else:
                        done = len(ch)
                    cur = (st, len(ch), done)
                    if cur != last:
                        log(f"  {sid}: status={st} nchild={len(ch)} done={done} prog={pr}")
                        last = cur
                    if ch and done >= len(ch):
                        log(f"  {sid} ALL CHILDREN DONE"); return "DONE"
                    if st in ("COMPLETE", "ERROR", "FAIL", "CANCELLED") and not ch and pr is None:
                        log(f"  {sid} terminal {st}"); return st
                elif r.status_code == 404:
                    log(f"  {sid} 404"); return "404"
            except Exception as e:
                log(f"  poll ERR {type(e).__name__}")
            await asyncio.sleep(40)
        return "TIMEOUT"

    ckpt = load_ckpt()
    done_tags = {t for t, v in ckpt.items() if v.get("sid")}
    if done_tags:
        log(f"resume: skip {sorted(done_tags)}")

    for i, spec in enumerate(specs):
        tag = f"{prefix}_b{i+1}"
        if tag in done_tags:
            log(f"=== {tag} SKIP (done {ckpt[tag]['sid']}) ===")
            continue
        log(f"=== {tag} START ===")
        sid = None
        p = spec["path"]
        args = [sys.executable, TOOL, "--path", p, "--sleep", "4",
                "--region", spec.get("region", "GLB"),
                "--delay", str(spec.get("delay", 1)),
                "--universe", spec.get("universe", "MINVOL1M"),
                "--neutralization", spec.get("neutralization", "SUBINDUSTRY"),
                "--decay", str(spec.get("decay", 10)),
                "--truncation", str(spec.get("truncation", 0.02)),
                "--nan-handling", spec.get("nanHandling", "OFF"),
                "--max-trade", spec.get("maxTrade", "OFF")]
        for it in range(60):
            r = subprocess.run(args, capture_output=True, text=True, cwd=ROOT)
            out = (r.stdout or "") + (r.stderr or "")
            m = re.search(r"simulations/([A-Za-z0-9]+)", out)
            if "status=201" in out and m:
                sid = m.group(1); log(f"  {tag} submitted {sid}")
                ckpt[tag] = {"sid": sid}; save_ckpt(ckpt)
                break
            if "429" in out or "CONCURRENT" in out:
                if it % 3 == 0:
                    log(f"  {tag} iter={it} 429")
                time.sleep(55)
            elif "Authentication failed" in out:
                log(f"  {tag} iter={it} AUTH-400"); time.sleep(30)
            else:
                log(f"  {tag} iter={it} other: {out[-200:]}"); time.sleep(30)
        if not sid:
            log(f"  {tag} FAILED"); continue
        st = asyncio.run(wait_batch(sid))
        log(f"=== {tag} DONE {st} ===")
    log("ALL DONE")


if __name__ == "__main__":
    main()
