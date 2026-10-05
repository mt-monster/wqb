# -*- coding: utf-8 -*-
"""A16A: 扫 universe × decay（USA/STATISTICAL，base kernel）。
每个配置一次 probe（conc=1），最多 3 个 probe 并发。
用法: python tools/tmp_a16_axes.py
"""
import json, os, subprocess, sys, time

# 2026-10-05 修正：原先写死作者本机绝对路径（本仓库根 + 作者的 workbuddy解释器），
# 被 test_sd_portability::test_no_author_drive_paths_in_runtime_string_constants 判红。
# 换机器即失效，且解释器路径泄露本机用户名。改为仓库根上溯探测 + 当前解释器。
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PY = sys.executable  # 本脚本已在 venv 下运行，用当前解释器即可
SCRIPT = os.path.join(REPO, "attic/tracking_reference_20261004/scripts/tmp_probe_conc.py")

EXPR = ("group_rank(ts_zscore(subtract(vec_avg(anl16_clusterestsup),"
        "vec_avg(anl16_clusterestsdown)),125),industry)")

# (tag, universe, decay, neutralization)
CONFIGS = [
    ("u2000", "TOP2000", 30, "STATISTICAL"),
    ("u1000", "TOP1000", 30, "STATISTICAL"),
    ("u500",  "TOP500",  30, "STATISTICAL"),
    ("u200",  "TOP200",  30, "STATISTICAL"),
    ("d04",   "TOP3000",  4, "STATISTICAL"),
    ("d10",   "TOP3000", 10, "STATISTICAL"),
    ("d20",   "TOP3000", 20, "STATISTICAL"),
    ("d50",   "TOP3000", 50, "STATISTICAL"),
    ("d70",   "TOP3000", 70, "STATISTICAL"),
]

def build():
    procs = []
    MAXP = 3
    for tag, uni, dec, neu in CONFIGS:
        f = os.path.join(REPO, "tracking/USA/candidates", f"exprs_usa_{tag}.json")
        json.dump([["A16A-" + tag, EXPR]], open(f, "w", encoding="utf-8"))
        cmd = [PY, SCRIPT, "--region", "USA", "--universe", uni, "--tag", tag,
               "--exprs-file", f, "--delay", "1", "--decay", str(dec),
               "--neutralization", neu, "--truncation", "0.08",
               "--nan-handling", "ON", "--conc", "1"]
        log = open(os.path.join(REPO, "logs", f"probe_{tag}.log"), "w", encoding="utf-8")
        while len(procs) >= MAXP:
            procs = [p for p in procs if p.poll() is None]
            if len(procs) >= MAXP:
                time.sleep(3)
        print("RUN", tag, uni, "decay", dec, flush=True)
        procs.append(subprocess.Popen(cmd, stdout=log, stderr=subprocess.STDOUT))
    for p in procs:
        p.wait()
    print("ALL DONE", flush=True)

if __name__ == "__main__":
    build()
