# -*- coding: utf-8 -*-
"""A16N: 扫 neutralization 轴（USA）。每条轴单独一次 probe，tag=n_<axis>。
用法: python tools/tmp_a16n_neut.py
"""
import json, os, subprocess, sys

REPO = r"D:\coding\traeCN_project\wqb"
PY = r"C:\Users\MENGTAO\.workbuddy\binaries\python\versions\3.13.12\python.exe"
SCRIPT = os.path.join(REPO, "attic/tracking_reference_20261004/scripts/tmp_probe_conc.py")

# 核心 kernel（A16D-1，IS 全过，仅 prod 卡）
EXPR = ("group_rank(ts_zscore(subtract(vec_avg(anl16_clusterestsup),"
        "vec_avg(anl16_clusterestsdown)),125),industry)")

AXES = ["REVERSION_AND_MOMENTUM", "FAST", "SLOW", "SLOW_AND_FAST", "CROWDING",
        "MARKET", "SECTOR", "SUBINDUSTRY", "NONE"]

for ax in AXES:
    tag = "n_" + ax.lower().replace("_", "")
    f = os.path.join(REPO, "tracking/USA/candidates", f"exprs_usa_{tag}.json")
    json.dump([["A16N-" + ax, EXPR]], open(f, "w", encoding="utf-8"))
    cmd = [PY, SCRIPT, "--region", "USA", "--universe", "TOP3000", "--tag", tag,
           "--exprs-file", f, "--delay", "1", "--decay", "30",
           "--neutralization", ax, "--truncation", "0.08",
           "--nan-handling", "ON", "--conc", "1"]
    log = os.path.join(REPO, "logs", f"probe_{tag}.log")
    print("RUN", ax, "->", log, flush=True)
    with open(log, "w", encoding="utf-8") as lf:
        subprocess.run(cmd, stdout=lf, stderr=subprocess.STDOUT)
    print("DONE", ax, flush=True)
print("ALL DONE")
