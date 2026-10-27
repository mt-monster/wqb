"""r22 串行执行器：兼容 multi-sim（有 children）与单 sim（只有 status/progress）两种形状。"""
import asyncio, json, os, re, subprocess, sys, time
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # tools/*.py -> 仓库根，勿写死盘符
PY = os.path.join(ROOT, "world-quant-brain-mcp", ".venv", "Scripts", "python.exe")
SB = os.path.join(ROOT, "tools", "submit_batch.py")
sys.path.insert(0, os.path.join(ROOT, "world-quant-brain-mcp"))
from brain_api import brain_client

TERM = ("COMPLETE", "ERROR", "FAIL", "CANCELLED")
def log(m): print(m, flush=True)

def submit_all(stem):
    p = os.path.join(ROOT, "tracking", "EUR", "runs", stem + ".txt")
    code = [ln.strip() for ln in open(p, encoding="utf-8") if ln.strip() and not ln.startswith("#")]
    cmd = [PY, SB, "--path", p, "--region", "EUR", "--universe", "TOPCS1600", "--delay", "1",
           "--decay", "4", "--neutralization", "FAST", "--truncation", "0.08",
           "--max-trade", "ON", "--nan-handling", "ON", "--simulation-mode", "FULL"]
    o = subprocess.run(cmd, capture_output=True, text=True)
    sids = re.findall(r"/simulations/([A-Za-z0-9]+)", o.stdout)
    log(f"### {stem}: n={len(code)} submitted, sims={sids}")
    if not sids:
        log("    FAIL " + (o.stdout or o.stderr)[-300:])
    return sids

def poll(sids, tag):
    """返回该批所有 COMPLETE alpha id。兼容 children 形状与单 sim 形状。"""
    alphas = set()
    for _ in range(100):
        done_all = True
        for sid in sids:
            j = brain_client.session.get(f"{brain_client.base_url}/simulations/{sid}").json()
            if not isinstance(j, dict):
                done_all = False; continue
            kids = j.get("children")
            if kids:
                sts = []
                for k in kids:
                    kk = brain_client.session.get(f"{brain_client.base_url}/simulations/{k}").json()
                    sts.append(kk if isinstance(kk, dict) else {})
                if not all(x.get("status") in TERM for x in sts):
                    done_all = False
                for x in sts:
                    if x.get("status") == "COMPLETE" and x.get("alpha"):
                        alphas.add(x["alpha"])
                    elif x.get("status") in ("ERROR", "FAIL", "CANCELLED"):
                        log(f"    {sid} child FAIL {str(x.get('error'))[:70]}")
            else:
                st = j.get("status")
                if st in TERM:
                    if st == "COMPLETE" and j.get("alpha"):
                        alphas.add(j["alpha"])
                    else:
                        log(f"    {sid} {st} {str(j.get('error'))[:70]}")
                else:
                    done_all = False
        if done_all:
            log(f"[{tag}] 完成，alpha={sorted(alphas)}")
            return sorted(alphas)
        time.sleep(15)
    log(f"[{tag}] TIMEOUT")
    return sorted(alphas)

def main():
    asyncio.run(brain_client.ensure_authenticated())
    all_ids = []
    # r22a 已提交（可能有多条 sim，逐个补收）
    all_ids += poll(["1Pl7VofdA4om9b7InekcTfF"], "r22a")
    for stem in ("r22b_f23_lemn", "r22c_f23_xa1"):
        sids = submit_all(stem)
        if sids:
            all_ids += poll(sids, stem)
        time.sleep(3)
    log("ALPHAS=" + json.dumps(all_ids))
    json.dump(all_ids, open(os.path.join(ROOT, "logs", "r22_alphas.json"), "w"))

main()
