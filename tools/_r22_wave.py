# 定向波 r22 串行派发器：每批 2 条，批间等待，严格并发 2
import json, os, re, subprocess, sys, time
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # tools/*.py -> 仓库根，勿写死盘符
PY = os.path.join(ROOT, "world-quant-brain-mcp", ".venv", "Scripts", "python.exe")
SB = os.path.join(ROOT, "tools", "submit_batch.py")
sys.path.insert(0, os.path.join(ROOT, "world-quant-brain-mcp"))
from brain_api import brain_client

FILES = ["r22a_f23_vkd", "r22b_f23_lemn", "r22c_f23_xa1"]

def submit(stem):
    p = os.path.join(ROOT, "tracking", "EUR", "runs", stem + ".txt")
    cmd = [PY, SB, "--path", p, "--region", "EUR", "--universe", "TOPCS1600",
           "--delay", "1", "--decay", "4", "--neutralization", "FAST",
           "--truncation", "0.08", "--max-trade", "ON", "--nan-handling", "ON",
           "--simulation-mode", "FULL"]
    out = subprocess.run(cmd, capture_output=True, text=True).stdout
    m = re.findall(r"/simulations/([A-Za-z0-9]+)", out)
    return (m[-1] if m else None), out.strip().splitlines()[-1:]

def wait(sid, tag):
    for _ in range(60):
        r = brain_client.session.get(f"{brain_client.base_url}/simulations/{sid}").json()
        kids = r.get("children") or []
        st = [brain_client.session.get(f"{brain_client.base_url}/simulations/{k}").json().get("status") for k in kids] if kids else []
        if kids and all(s in ("COMPLETE", "ERROR", "FAIL", "CANCELLED") for s in st):
            print(f"[{tag}] children={len(kids)} 终态={st}")
            for k in kids:
                j = brain_client.session.get(f"{brain_client.base_url}/simulations/{k}").json()
                print(f"    {j.get('status')} {j.get('alpha')} {str(j.get('error',''))[:60]}")
            return True
        time.sleep(15)
    print(f"[{tag}] TIMEOUT 仍在跑（sim={sid}）")
    return False

for stem in FILES:
    sid, tail = submit(stem)
    print(f"### {stem}: sim={sid}  {tail}")
    if sid:
        wait(sid, stem)
    time.sleep(5)
print("ALL DISPATCHED")
