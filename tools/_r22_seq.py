# r22 串行：等 r22a 终态 → 派 r22b → 等 → 派 r22c → 等 → 汇总。全程并发 ≤2。
import json, os, re, subprocess, sys, time
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # tools/*.py -> 仓库根，勿写死盘符
PY = os.path.join(ROOT, "world-quant-brain-mcp", ".venv", "Scripts", "python.exe")
SB = os.path.join(ROOT, "tools", "submit_batch.py")
sys.path.insert(0, os.path.join(ROOT, "world-quant-brain-mcp"))
from brain_api import brain_client

TERM = ("COMPLETE", "ERROR", "FAIL", "CANCELLED")
def log(m):
    print(m, flush=True)

def kids_of(sid):
    r = brain_client.session.get(f"{brain_client.base_url}/simulations/{sid}").json()
    if not isinstance(r, dict):
        return None
    return r.get("children") or []

def wait(sid, tag, rounds=80):
    for _ in range(rounds):
        k = kids_of(sid)
        if k:
            sts = []
            for x in k:
                j = brain_client.session.get(f"{brain_client.base_url}/simulations/{x}").json()
                sts.append(j.get("status") if isinstance(j, dict) else "?")
            if all(s in TERM for s in sts):
                log(f"[{tag}] 终态 {sts}")
                out = []
                for x in k:
                    j = brain_client.session.get(f"{brain_client.base_url}/simulations/{x}").json()
                    if not isinstance(j, dict):
                        continue
                    if j.get("status") == "COMPLETE" and j.get("alpha"):
                        out.append(j["alpha"])
                        log(f"    OK {j['alpha']}")
                    else:
                        log(f"    {j.get('status')} err={str(j.get('error'))[:80]}")
                return out
        time.sleep(15)
    log(f"[{tag}] TIMEOUT（sim={sid}）")
    return []

def submit(stem):
    p = os.path.join(ROOT, "tracking", "EUR", "runs", stem + ".txt")
    cmd = [PY, SB, "--path", p, "--region", "EUR", "--universe", "TOPCS1600",
           "--delay", "1", "--decay", "4", "--neutralization", "FAST",
           "--truncation", "0.08", "--max-trade", "ON", "--nan-handling", "ON",
           "--simulation-mode", "FULL"]
    o = subprocess.run(cmd, capture_output=True, text=True)
    m = re.findall(r"/simulations/([A-Za-z0-9]+)", o.stdout)
    sid = m[-1] if m else None
    log(f"### {stem} -> sim={sid}")
    if not sid:
        log("    submit 失败: " + (o.stdout or o.stderr)[-400:])
    return sid

def main():
    # 父进程必须先认证，否则 session.get 拿到 401 JSON（无 children）⇒ wait() 空转到超时
    import asyncio
    asyncio.run(brain_client.ensure_authenticated())
    ids = []
    first = "1Pl7VofdA4om9b7InekcTfF"
    log("== r22a 已在跑，等待")
    ids += wait(first, "r22a")
    for stem in ("r22b_f23_lemn", "r22c_f23_xa1"):
        sid = submit(stem)
        if sid:
            ids += wait(sid, stem)
        time.sleep(5)
    log("ALPHAS=" + json.dumps(ids))
    json.dump(ids, open(os.path.join(ROOT, "logs", "r22_alphas.json"), "w"))

main()
