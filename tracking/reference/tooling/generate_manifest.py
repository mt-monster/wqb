#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate tracking/MANIFEST.json (full index + logical unified names),
zip large files into archive/large/ (cold backup), remove temp files."""
import os, json, re, zipfile

BASE = r"D:\coding\traeCN_project\wqb\tracking"

STAGE_MAP = {
    "candidates": "cand", "results": "result", "reviews": "review",
    "reports": "report", "scripts": "script", "reference": "ref",
    "ra": "ra", "ppa": "ppa", "deepexplore": "deep", "sims": "sim",
}
TYPE_KW = [
    ("review", "review"), ("eval", "eval"), ("verdict", "verdict"),
    ("report", "report"), ("summary", "summary"), ("recap", "recap"),
    ("candidate", "cand"), ("seed", "seed"), ("plan", "plan"),
    ("exprs", "exprs"), ("expression", "exprs"), ("matrix", "matrix"),
    ("fields", "fields"), ("field", "fields"), ("score", "score"),
    ("whitelist", "whitelist"), ("campaign", "campaign"),
    ("diversity", "diversity"), ("family", "family"), ("orthogonal", "ortho"),
    ("minusrank", "minusrank"), ("boost", "boost"), ("fix", "fix"),
    ("dilute", "dilute"), ("ai_model", "aimodel"), ("model", "model"),
    ("chart", "chart"), ("state", "state"), ("list", "list"),
    ("alpha", "alpha"), ("dataset", "dataset"), ("args", "args"),
    ("idea", "idea"), ("result", "result"), ("metric", "metric"),
    ("sim", "sim"), ("break", "break"), ("final", "final"),
    ("valid", "valid"), ("output", "output"), ("health", "health"),
    ("recommendation", "reco"), ("feature", "feature"),
    ("portability", "port"), ("academic", "academic"), ("method", "method"),
    ("search", "search"), ("supplement", "supplement"), ("condensed", "condensed"),
    ("dump", "dump"), ("poll", "poll"), ("submit", "submit"),
    ("enhance", "enhance"), ("progress", "progress"), ("loop", "loop"),
    ("quality", "quality"), ("pdf", "pdf"), ("multiplier", "mult"),
    ("forum", "forum"), ("new", "new"), ("cs1600", "cs1600"),
]

REGIONS = {"EUR", "KOR", "USA", "IND", "GLB", "DEU", "FORUM"}


def derive_type(name):
    low = name.lower()
    for kw, label in TYPE_KW:
        if kw in low:
            return label
    return os.path.splitext(name)[1].lstrip(".") or "data"


def unified_name(region, life, name):
    stage = STAGE_MAP.get(life, life)
    m = re.search(r'(wave|v|round|batch|d|step)(\d+)', name.lower())
    wave = m.group(2) if m else "x"
    type_ = derive_type(name)
    return f"{region}_{stage}_{wave}_{type_}"


def main():
    # load move map for original paths
    orig = {}
    mm = os.path.join(BASE, "_move_map.json")
    if os.path.exists(mm):
        with open(mm, encoding="utf-8") as f:
            mv = json.load(f)  # old_rel -> new_rel
        inv = {v: k for k, v in mv.items()}
    else:
        inv = {}

    records = []
    for root, dirs, files in os.walk(BASE):
        # skip archive, backup, temp, manifest itself
        rel_root = os.path.relpath(root, BASE)
        parts = rel_root.split(os.sep)
        top = parts[0] if rel_root != "." else "(root)"
        if top in ("archive",) or rel_root.startswith("archive"):
            continue
        if "tracking_backup" in root:
            continue
        for fn in files:
            if fn in ("MANIFEST.json", "_move_map.json", "_inventory_tmp.json"):
                continue
            full = os.path.join(root, fn)
            rel = os.path.relpath(full, BASE).replace(os.sep, "/")
            try:
                sz = os.path.getsize(full)
            except OSError:
                sz = -1
            # region + lifecycle
            region = top if top in REGIONS else (top if top in ("reference", "mining", "sessions", "runs") else "GLOBAL")
            life = parts[1] if len(parts) > 1 else "root"
            if region in ("reference", "mining", "sessions", "runs"):
                life = life if life != "root" else region
            ext = os.path.splitext(fn)[1].lstrip(".").lower()
            u = unified_name(region if region in REGIONS else top, life, fn)
            orig_path = inv.get(rel)
            records.append({
                "path": rel,
                "region": region if region in REGIONS else top,
                "lifecycle": life,
                "type": ext,
                "size_bytes": sz,
                "unified_name": u,
                "original_path": orig_path,
            })

    records.sort(key=lambda r: (r["region"], r["lifecycle"], r["path"]))
    manifest = {
        "generated": "2026-08-14",
        "base": "tracking/",
        "total_files": len(records),
        "regions": sorted(REGIONS),
        "lifecycle_dirs": ["candidates", "results", "reviews", "reports", "scripts", "reference"],
        "convention": "{REGION}/{lifecycle}/{REGION}_{stage}_{wave}_{type}.{ext}",
        "files": records,
    }
    with open(os.path.join(BASE, "MANIFEST.json"), "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)
    print(f"MANIFEST.json written: {len(records)} files indexed.")

    # ---- scheme ④: archive large files (compressed cold backup, originals kept) ----
    large = [r for r in records if r["size_bytes"] > 500_000]
    arch_dir = os.path.join(BASE, "archive", "large")
    os.makedirs(arch_dir, exist_ok=True)
    for r in large:
        src = os.path.join(BASE, r["path"])
        zname = os.path.basename(r["path"]).rsplit(".", 1)[0] + ".zip"
        zpath = os.path.join(arch_dir, zname)
        with zipfile.ZipFile(zpath, "w", zipfile.ZIP_DEFLATED) as z:
            z.write(src, os.path.basename(src))
        print(f"  archived -> archive/large/{zname} ({r['size_bytes']/1024:.0f}KB)")
    print(f"Archived {len(large)} large files (originals retained for compatibility).")

    # ---- scheme ⑥: remove temp inventory file ----
    tmp = os.path.join(BASE, "_inventory_tmp.json")
    if os.path.exists(tmp):
        os.remove(tmp)
        print("Removed temp _inventory_tmp.json")


if __name__ == "__main__":
    main()
