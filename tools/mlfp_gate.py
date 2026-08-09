#!/usr/bin/env python3
"""ml_factor_proj 挖掘结果汇总 + 闸门检查 + 提交。

用法:
  python tools/mlfp_gate.py summary                 # 汇总全部批次
  python tools/mlfp_gate.py gate <alpha_id> [...]   # 对候选跑 prod/self corr
  python tools/mlfp_gate.py mutual <id1> <id2> ...  # 互相关
"""
import importlib.machinery
import importlib.util
import json
import sys
import time
from pathlib import Path

_p = Path(__file__).resolve().parent / "mcp_py"
_s = importlib.util.spec_from_loader("mcp_py", importlib.machinery.SourceFileLoader("mcp_py", str(_p)))
_m = importlib.util.module_from_spec(_s)
_s.loader.exec_module(_m)
call_tool = _m.call_tool

WORKSPACE = Path(__file__).resolve().parent.parent
OUT = WORKSPACE / "tracking" / "mining"

# 廉价闸门
GATE_SHARPE = 1.58
GATE_FITNESS = 1.0
GATE_TVR_LO, GATE_TVR_HI = 0.05, 0.70


def _retry(tool, args, n=4, wait=8, timeout=900):
    last = None
    for _ in range(n):
        r = call_tool(tool, args, timeout=timeout)
        if not (isinstance(r, dict) and r.get("error")):
            return r
        last = r
        time.sleep(wait)
    return last


def summary():
    allrows = []
    for f in sorted(OUT.glob("rows_mlfp_*.json")):
        tag = f.stem.replace("rows_mlfp_", "")
        for r in json.loads(f.read_text(encoding="utf-8")):
            r["batch"] = tag
            allrows.append(r)
    allrows.sort(key=lambda x: -(x.get("sharpe") if x.get("sharpe") is not None else -9))
    hdr = f"{'batch':5} {'label':22} {'alpha':10} {'sharpe':>7} {'fit':>6} {'tvr':>6} {'ret':>8} {'dd':>6}"
    print(hdr)
    print("-" * len(hdr))
    passed = []
    for r in allrows:
        sh = r.get("sharpe")
        fi = r.get("fitness")
        tv = r.get("turnover")
        nn = lambda v: v if v is not None else float("nan")
        print(f"{r['batch']:5} {r['label'][:22]:22} {str(r.get('alpha'))[:10]:10} "
              f"{nn(sh):7.2f} {nn(fi):6.2f} {nn(tv):6.3f} "
              f"{nn(r.get('returns')):8.4f} {nn(r.get('drawdown')):6.3f}")
        if sh is not None and abs(sh) >= GATE_SHARPE and fi is not None and abs(fi) >= GATE_FITNESS \
                and tv is not None and GATE_TVR_LO <= tv <= GATE_TVR_HI:
            passed.append(r)
    print(f"\nTOTAL={len(allrows)}  PASS_CHEAP_GATE={len(passed)}")
    for r in passed:
        print("  PASS:", r["batch"], r["label"], r["alpha"], r["sharpe"], r["fitness"])
    (OUT / "summary_mlfp.json").write_text(
        json.dumps({"rows": allrows, "passed": passed}, ensure_ascii=False, indent=1),
        encoding="utf-8")
    return allrows, passed


def gate(ids):
    res = {}
    for aid in ids:
        pc = _retry("check_correlation", {"alpha_id": aid}, n=3)
        sc = _retry("check_self_correlation", {"alpha_id": aid}, n=3)
        res[aid] = {"prod": pc, "self": sc}
        print(f"== {aid} ==")
        print(" prod:", json.dumps(pc, ensure_ascii=False, default=str)[:400])
        print(" self:", json.dumps(sc, ensure_ascii=False, default=str)[:400])
    (OUT / "gate_mlfp.json").write_text(
        json.dumps(res, ensure_ascii=False, indent=1, default=str), encoding="utf-8")


def mutual(ids):
    r = _retry("compute_mutual_correlation", {"alpha_ids": ids})
    print(json.dumps(r, ensure_ascii=False, indent=1, default=str)[:2000])
    (OUT / "mutual_mlfp.json").write_text(
        json.dumps(r, ensure_ascii=False, indent=1, default=str), encoding="utf-8")


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "summary":
        summary()
    elif cmd == "gate":
        gate(sys.argv[2:])
    elif cmd == "mutual":
        mutual(sys.argv[2:])
