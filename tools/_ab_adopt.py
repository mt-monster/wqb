# -*- coding: utf-8 -*-
"""把「手动补派」的 A/B 批次收割进断点，避免重复派发。

用法：python tools/_ab_adopt.py <batch_key> <sim_id>
例：  python tools/_ab_adopt.py b01 2H1IoJ1JI4U1cugAYyfshhG
"""
import json
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PY = os.path.join(ROOT, "world-quant-brain-mcp", ".venv", "Scripts", "python.exe")
HARVEST = os.path.join(ROOT, "cache", "_harvest_safe.py")
CK = os.path.join(ROOT, "results", "_ab_template_ck.json")
LEDGER = os.path.join(ROOT, "results", "_ab_template_ledger.json")
BATCH = 10

os.environ.setdefault("WQB_REPO_ROOT", ROOT)
sys.path.insert(0, os.path.join(os.path.expanduser("~"), ".workbuddy", "skills", "wq-brain-ra-eur", "scripts"))
sys.path.insert(0, os.path.join(ROOT, "world-quant-brain-mcp"))


def build_plan():
    import sqlite3
    from wqb_campaign.fields import select_fields
    from wqb_campaign.generate import build_one_family, DS_FREQ
    DATASETS = ["other571", "insider_matrix"]
    OLD = ["lvl_zs", "lvl_qt", "lvl_sc", "ir_pl", "dsp_rk"]
    NEW = ["pp"]
    CTRL = ["lvl_rk"]
    con = sqlite3.connect(os.path.join(ROOT, "data", "wqb.db")); con.execute("PRAGMA busy_timeout=30000")
    con.row_factory = sqlite3.Row
    plan = []
    for ds in DATASETS:
        _all = select_fields(con, ds, field_min_cov=0.6)
        _full = [r for r in _all if r.get("tier") == "full"]
        _probe = [r for r in _all if r.get("tier") != "full"]
        sel = (_full + _probe)[:8]
        freq = DS_FREQ.get(ds, "daily")
        for arm in OLD + NEW + CTRL:
            for r in sel:
                if arm == "dsp_rk" and r.get("field_type") != "VECTOR":
                    continue
                e = build_one_family(arm, r, freq)
                if not e:
                    continue
                plan.append(dict(ds=ds, arm=arm, field=r["field_name"], expr=e))
    con.close()
    return plan


def main():
    key, sid = sys.argv[1], sys.argv[2]
    idx = int(key[1:])
    plan = build_plan()
    chunk = plan[idx * BATCH:(idx + 1) * BATCH]
    out = subprocess.run([PY, HARVEST, sid, chunk[0]["ds"], "camp"],
                         capture_output=True, text=True, timeout=600, cwd=ROOT).stdout
    rows = []
    for ln in out.splitlines():
        m = re.match(r"\s*\+\s+(\w+)\s+S=([-\d.]+)\s+F=([-\d.]+).*?2Y=([-\d.]+)\s+sub=([-\d.]+)", ln)
        if m:
            rows.append(dict(alpha=m.group(1), S=float(m.group(2)), F=float(m.group(3)),
                             Y2=float(m.group(4)), sub=float(m.group(5))))
    print("收割 %d/%d" % (len(rows), len(chunk)))
    ck = json.load(open(CK, encoding="utf-8")) if os.path.isfile(CK) else {"done": [], "results": []}
    have = {(r.get("alpha"), r.get("arm")) for r in ck["results"]}
    added = 0
    for i, r in enumerate(rows):
        if i < len(chunk):
            r.update(ds=chunk[i]["ds"], arm=chunk[i]["arm"], field=chunk[i]["field"])
        if (r["alpha"], r.get("arm")) in have:
            continue
        ck["results"].append(r)
        added += 1
    if key not in ck["done"]:
        ck["done"].append(key)
    for p, obj in ((CK, ck), (LEDGER, ck["results"])):
        tmp = p + ".tmp"
        json.dump(obj, open(tmp, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        os.replace(tmp, p)
    print("adopt %s: +%d 条｜done=%s" % (key, added, sorted(ck["done"])))


if __name__ == "__main__":
    main()
