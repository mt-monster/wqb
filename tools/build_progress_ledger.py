#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""落地建议 1.2:
1) 刷新 KOR campaign_state, 对齐 wave 文件前沿(34), 并纳入平台核验结果。
2) 统一提交状态台账, 以平台 OS 真相为准, 算准总提交数。
"""
import json, os, glob, re
from collections import Counter
BASE = r"D:\coding\traeCN_project\wqb\tracking"

def load(p):
    try:
        return json.load(open(p, encoding="utf-8"))
    except (OSError, ValueError):
        return None

# ---- platform OS set (已全量拉取, 快照存于 _os_ids.json) ----
os_ids = {}
os_snap = os.path.join(BASE, "_os_ids.json")
if os.path.exists(os_snap):
    os_ids = json.load(open(os_snap, encoding="utf-8"))
else:
    for pf in ["_os_page0.json", "_os_page1.json"]:
        path = os.path.join(BASE, pf)
        if os.path.exists(path):
            for a in json.load(open(path, encoding="utf-8")):
                os_ids[a["id"]] = a.get("region")
    json.dump(os_ids, open(os_snap, "w"), ensure_ascii=False)
OS_TOTAL = len(os_ids)
OS_REGIONS = dict(Counter(os_ids.values()))

# ---- local alpha ids ----
local = {}
def add(aid, region, source, local_status, code=None):
    if aid: local[str(aid)] = dict(region=region, source=source,
                                   local_status=str(local_status).upper(), code=code)

# EUR/USA/IND results
def iter_items(obj):
    if isinstance(obj, dict):
        if obj and all(isinstance(v, dict) and ("alpha_id" in v or "S" in v or "F" in v) for v in obj.values()):
            for k, v in obj.items():
                if isinstance(v, dict): yield k, v
        else:
            for v in obj.values(): yield from iter_items(v)
    elif isinstance(obj, list):
        for it in obj:
            if isinstance(it, dict) and ("alpha_id" in it or "S" in it or "F" in it):
                yield it.get("id", it.get("alpha_id", "?")), it
            else:
                yield from iter_items(it)
for region, rd in [("EUR","EUR/results"),("USA","USA/results"),("IND","IND/results")]:
    d = os.path.join(BASE, rd)
    if os.path.isdir(d):
        for p in glob.glob(os.path.join(d, "*.json")):
            for k, e in iter_items(load(p)):
                add(e.get("alpha_id"), region, "results_json", "CREATED")

# KOR campaign_state multisims
cs = load(os.path.join(BASE, "KOR", "results", "kor_d1_campaign_state.json"))
kor_ids = {}
if isinstance(cs, dict):
    def walk(o):
        if isinstance(o, dict):
            if isinstance(o.get("id"), str) and ("exprs" in o or "status" in o or "setting" in o):
                kor_ids[o["id"]] = str(o.get("status","CREATED")).upper()
            for v in o.values(): walk(v)
        elif isinstance(o, list):
            for v in o: walk(v)
    walk(cs)
for k, v in kor_ids.items(): add(k, "KOR", "campaign_state", v)

# GLB batch
glb = load(os.path.join(BASE, "GLB", "glb_d1_batch01.json"))
glb_n = 0
if isinstance(glb, dict):
    for r in glb.get("results", []):
        if isinstance(r, dict):
            aid = r.get("alpha_id") or ""
            glb_n += 1
            add(aid if aid else "GLB_"+str(r.get("label","?")), "GLB", "glb_batch", r.get("status","?"))

# ---- status normalization against platform truth ----
ledger = []
by_region = {}
for aid, meta in local.items():
    region = meta["region"]
    if aid in os_ids:
        status = "SUBMITTED"
    elif region in ("EUR","USA","IND"):
        # 8-char valid ids, verified sample = IS/UNSUBMITTED; OS set complete -> not submitted
        status = "UNSUBMITTED" if len(aid) == 8 else "UNKNOWN_ID"
    elif region == "KOR":
        status = "INVALID_TRACKING_ID" if len(aid) != 8 else "UNSUBMITTED"
    else:  # GLB (no id)
        status = "SUBMITTED_UNVERIFIED" if meta["local_status"] == "SUBMITTED" else "UNKNOWN"
    rec = dict(alpha_id=aid, region=region, status=status,
               local_status=meta["local_status"], source=meta["source"])
    ledger.append(rec)
    by_region.setdefault(region, Counter())[status] += 1
ledger.sort(key=lambda r: (r["region"], r["status"], r["alpha_id"]))

verified_submitted = sum(1 for r in ledger if r["status"] == "SUBMITTED")

# ---- save ledger ----
out = dict(
    generated="2026-08-15",
    method="local_tracking_ids ∩ platform_get_user_alphas(stage=OS, fully fetched=146)",
    platform_os_total=OS_TOTAL,
    platform_os_regions=OS_REGIONS,
    platform_os_ids=sorted(os_ids.keys()),
    local_records=len(local),
    verified_submitted=verified_submitted,
    by_region={r: dict(c) for r, c in by_region.items()},
    note=("平台 OS 全量 146 已拉全, 与本地 257 个 id 交集为 0 -> 本地追踪 alpha 均处于 IS/未提交。"
          "KOR campaign_state 的 'id' 为 21-24 位(非标准 8 位 alpha id), GLB batch 的 alpha_id 为空,"
          "二者均无法在平台核验, 其 'submitted' 标记为本地臆测。真实提交活动在平台上(见 platform_os_regions),"
          "但未被 tracking/ 收录 -> 需将本地追踪与平台同步。"),
    ledger=ledger,
)
json.dump(out, open(os.path.join(BASE, "progress_ledger.json"), "w"), ensure_ascii=False, indent=2)

# ---- refresh KOR campaign_state ----
cs_path = os.path.join(BASE, "KOR", "results", "kor_d1_campaign_state.json")
if isinstance(cs, dict):
    bak = cs_path + ".bak"
    if not os.path.exists(bak):
        json.dump(cs, open(bak, "w"), ensure_ascii=False, indent=2)
    # wave inventory from wave files
    wave_files = sorted(glob.glob(os.path.join(BASE, "KOR", "kor_wave*_exprs.json"))) + \
                 sorted(glob.glob(os.path.join(BASE, "KOR", "candidates", "kor_wave*_exprs.json")))
    inv = {}
    for p in wave_files:
        o = load(p)
        if not isinstance(o, dict): continue
        m = re.search(r"wave(\d+)", os.path.basename(p))
        w = int(m.group(1)) if m else -1
        exprs = o.get("expressions", []) if isinstance(o.get("expressions"), list) else []
        inv.setdefault(w, dict(files=0, exprs=0, settings=set(), datasets=set()))
        inv[w]["files"] += 1
        inv[w]["exprs"] += len(exprs)
        st = o.get("setting")
        if st: inv[w]["settings"].add(json.dumps(st, ensure_ascii=False) if isinstance(st, (dict, list)) else str(st))
        dt = o.get("dataset")
        if dt: inv[w]["datasets"].add(str(dt))
    wave_inv = []
    for w in sorted(inv):
        d = inv[w]
        wave_inv.append(dict(wave=w, files=d["files"], exprs=d["exprs"],
                             settings=sorted(d["settings"]), datasets=sorted(d["datasets"])))
    frontier = max(inv.keys()) if inv else 0
    total_expr = sum(d["exprs"] for d in inv.values())
    # cache metrics summary
    metrics_files = glob.glob(os.path.join(BASE, "KOR", "cache", "metrics", "*.json"))
    m_pass = m_fail = 0
    for p in metrics_files:
        o = load(p)
        if isinstance(o, dict):
            if o.get("failed_checks"): m_fail += 1
            else: m_pass += 1
    cs["_refreshed_at"] = "2026-08-15"
    cs["frontier_wave"] = frontier
    cs["total_wave_files"] = len(wave_files)
    cs["total_candidate_exprs"] = total_expr
    cs["wave_inventory"] = wave_inv
    cs["cache_metrics"] = dict(files=len(metrics_files), passed=m_pass, failed=m_fail)
    cs["platform_reconciliation"] = dict(
        os_total=OS_TOTAL, os_regions=OS_REGIONS,
        kor_os_count=OS_REGIONS.get("KOR", 0),
        tracked_kor_ids_valid_alpha_ids=False,
        note=("campaign_state 内 multisim 'id' 为 21-24 位, 非标准 8 位 WQ alpha id, 无法在平台核验;"
              "平台 OS 中 KOR 仅 %d 个。本地 'submitted=39' 为本地标记, 不实。" % OS_REGIONS.get("KOR", 0)))
    cs["reconciliation_note"] = (
        "本文件原仅记录至 wave 16 且 'submitted' 标记与平台不符。已刷新前沿至 wave %d (%d 个 wave 文件, "
        "约 %d 条候选表达式), 并纳入 KOR/cache/metrics 回测结果(%d 个, 通过 %d/失败 %d)。"
        "提交状态请以平台 OS 为准: 平台 OS 全量 %d 个(地区分布见 platform_reconciliation), "
        "但均与本地追踪 id 无交集 -> tracking/ 与平台未同步。" % (
            frontier, len(wave_files), total_expr, len(metrics_files), m_pass, m_fail, OS_TOTAL))
    json.dump(cs, open(cs_path, "w"), ensure_ascii=False, indent=2)
    print("campaign_state refreshed ->", cs_path)

# ---- console summary ----
print("="*72)
print("落地结果 (2026-08-15)")
print("="*72)
print(f"平台 OS 全量: {OS_TOTAL}  (地区: {OS_REGIONS})")
print(f"本地追踪 alpha: {len(local)} 个")
print(f"经平台核验已提交(SUBMITTED): {verified_submitted} 个  <-- 关键结论")
print()
print(f"{'区域':<6}{'记录':>6}{'SUBMITTED':>11}{'UNSUBMITTED':>13}{'INVALID_ID':>12}{'UNVERIF':>9}")
for r in ["EUR","USA","IND","KOR","GLB"]:
    c = by_region.get(r, Counter())
    print(f"{r:<6}{sum(c.values()):>6}{c.get('SUBMITTED',0):>11}{c.get('UNSUBMITTED',0):>13}{c.get('INVALID_TRACKING_ID',0):>12}{c.get('SUBMITTED_UNVERIFIED',0):>9}")
print(f"\n台账已写 tracking/progress_ledger.json")
print(f"campaign_state 已刷新(前沿 wave={frontier}, wave文件={len(wave_files)}, 候选表达式≈{total_expr})")
