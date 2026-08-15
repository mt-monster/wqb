#!/usr/bin/env python3
"""Fast reference-trace: scan repo SOURCE files (<=1MB each) for curated
high-risk basenames we plan to move. Skips heavy dirs."""
import os, re

ROOT = r"D:\coding\traeCN_project\wqb"
EXCLUDE_DIRS = {".git", ".venv", "world-quant-brain-mcp", "node_modules", "__pycache__",
                ".cursor", ".reasonix", ".qoder", ".zcode", ".workbuddy", "extensions",
                "research-data"}
SRC_EXT = {".py", ".md", ".sh", ".json", ".toml", ".txt", ".yml", ".yaml"}

# curated high-risk basenames (things that might be imported/referenced)
RISK = ["all_fields.json", "mdl177_fields.json", "kor_seed_candidates.txt",
        "enum_mdl177", "gen_v5", "mine_corr", "harvest_fields", "harvest_usa",
        "investigate_", "verify_", "probe_region", "check_state",
        "mine_v", "sim_v", "sim_poll", "reference/", "mining_experience",
        "task_plan.md", "progress.md", "findings.md", "os_alpha_experience_summary.md",
        "src/", "automation/"]

scan = []
for dp, dn, fn in os.walk(ROOT):
    dn[:] = [d for d in dn if d not in EXCLUDE_DIRS]
    for f in fn:
        if os.path.splitext(f)[1].lower() in SRC_EXT:
            p = os.path.join(dp, f)
            try:
                if os.path.getsize(p) <= 1_000_000:
                    scan.append(p)
            except: pass

print(f"scanning {len(scan)} source files (<=1MB)\n")
hits = {}
for kw in RISK:
    pat = re.compile(re.escape(kw))
    found = []
    for sf in scan:
        if os.path.basename(sf) == kw:  # skip self
            continue
        try:
            with open(sf, "r", encoding="utf-8", errors="ignore") as fh:
                for i, line in enumerate(fh, 1):
                    if pat.search(line):
                        found.append((os.path.relpath(sf, ROOT), i, line.strip()[:110]))
                        break
        except: pass
    if found:
        hits[kw] = found

if not hits:
    print("CLEAN: no external references to any high-risk basename.")
for kw, found in hits.items():
    print(f"### {kw}  ({len(found)} refs)")
    for rel, i, ln in found:
        print(f"    {rel}:{i}  {ln}")
    print()
