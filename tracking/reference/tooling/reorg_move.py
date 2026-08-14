#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Reorganize tracking/ into region/lifecycle structure.
Run with `plan` arg for dry-run (no filesystem changes).
"""
import os, sys, json, shutil

BASE = r"D:\coding\traeCN_project\wqb\tracking"
REGIONS = ["EUR", "KOR", "USA", "IND", "GLB"]
THEMATIC = {
    "deepexplore_deu": ("DEU", "deepexplore"),
    "eur_ra_20260812": ("EUR", "ra"),
    "ppa_mining": ("EUR", "ppa"),
}
KEEP_FLAT = ["FORUM", "reference", "sessions"]  # mining handled separately (untouched)

REGION_PREFIX = {"EUR": "eur_", "KOR": "kor_", "USA": "usa_", "IND": "ind_", "GLB": "glb_"}

CAND_KW = ("candidate", "seed", "plan", "exprs", "matrix", "fields", "score",
           "campaign", "diversity", "family", "orthogonal", "minusrank", "boost",
           "fix", "dilute", "ai_model", "cs1600", "chart", "model", "state",
           "list", "alpha", "dataset", "args", "idea")
RESULT_KW = ("result", "metric", "sim", "backtest", "break", "summary", "final", "valid", "output")
REPORT_KW = ("report", "recap", "stat", "health", "recommendation", "feature",
             "portability", "academic", "method", "search", "supplement", "condensed", "dump")
REVIE_KW = ("review", "eval", "verdict", "judge")


def classify(region, name, ext):
    low = name.lower()
    if ext == ".py":
        return "scripts"
    if any(k in low for k in REVIE_KW):
        return "reviews"
    if any(k in low for k in REPORT_KW) or ext in (".md", ".txt", ".log"):
        return "reports"
    if any(k in low for k in CAND_KW):
        return "candidates"
    if any(k in low for k in RESULT_KW):
        return "results"
    return "results"


def norm_region(name, region):
    lp = REGION_PREFIX[region]
    if name.lower().startswith(lp):
        return region + "_" + name[len(lp):]
    if name.startswith(region + "_"):
        return name
    return region + "_" + name


def plan_kor(name, ext):
    """Return (lifecycle, keep_basename)."""
    low = name.lower()
    if ext == ".py":
        return "scripts", True
    if "review" in low or "diversity" in low:
        return "reviews", True
    if "whitelist" in low:
        return "reference", True
    if "campaign_state" in low:
        return "results", True
    return "candidates", True


def build_plan():
    moves = []  # list of (old_rel, new_rel, rename_flag)
    for top in sorted(os.listdir(BASE)):
        old_top = os.path.join(BASE, top)
        if not os.path.isdir(old_top):
            continue
        if top == "mining":
            continue  # external tool writes here; keep untouched
        if top in ("_inventory_tmp.json",) or top.startswith("_backup") or top.startswith("archive"):
            continue

        if top in REGIONS:
            for fn in sorted(os.listdir(old_top)):
                fp = os.path.join(old_top, fn)
                if os.path.isdir(fp):
                    # nested subdir inside a region (shouldn't normally happen)
                    for root2, _, files2 in os.walk(fp):
                        for f2 in files2:
                            rel2 = os.path.relpath(os.path.join(root2, f2), BASE)
                            life = classify(top, f2, os.path.splitext(f2)[1])
                            if top == "KOR":
                                newname = f2
                            else:
                                newname = norm_region(f2, top)
                            moves.append((rel2, f"{top}/{life}/{newname}", top != "KOR"))
                    continue
                ext = os.path.splitext(fn)[1]
                if top == "KOR":
                    life, _ = plan_kor(fn, ext)
                    moves.append((os.path.relpath(fp, BASE), f"{top}/{life}/{fn}", False))
                else:
                    life = classify(top, fn, ext)
                    moves.append((os.path.relpath(fp, BASE), f"{top}/{life}/{norm_region(fn, top)}", True))

        elif top in THEMATIC:
            region, sub = THEMATIC[top]
            if top == "deepexplore_deu":
                for root2, dirs2, files2 in os.walk(old_top):
                    for f2 in files2:
                        full = os.path.join(root2, f2)
                        rel2 = os.path.relpath(full, BASE)
                        inner = os.path.relpath(full, old_top)  # e.g. enhance_input/x.json
                        if inner.startswith("templates"):
                            continue  # drop empty templates
                        moves.append((rel2, f"{region}/{sub}/{inner}", False))
            elif top == "eur_ra_20260812":
                for fn in sorted(os.listdir(old_top)):
                    fp = os.path.join(old_top, fn)
                    if os.path.isdir(fp):
                        continue
                    ext = os.path.splitext(fn)[1]
                    if ext == ".py":
                        life = "scripts"
                    elif ext in (".md", ".txt"):
                        life = "reports"
                    else:
                        life = "results"
                    moves.append((os.path.relpath(fp, BASE), f"{region}/{sub}/{life}/{fn}", False))
            elif top == "ppa_mining":
                for root2, dirs2, files2 in os.walk(old_top):
                    for f2 in files2:
                        full = os.path.join(root2, f2)
                        rel2 = os.path.relpath(full, BASE)
                        inner = os.path.relpath(full, old_top)
                        if inner.startswith("sims"):
                            moves.append((rel2, f"{region}/{sub}/{inner}", False))
                        else:
                            moves.append((rel2, f"{region}/{sub}/candidates/{f2}", False))

        elif top in KEEP_FLAT:
            # FORUM / reference / sessions -> keep flat (sessions preserves dated subdir)
            for root2, dirs2, files2 in os.walk(old_top):
                for f2 in files2:
                    full = os.path.join(root2, f2)
                    rel2 = os.path.relpath(full, BASE)
                    inner = os.path.relpath(full, old_top)
                    if top == "FORUM":
                        # normalize prefix to FORUM_ for consistency
                        newname = f2 if f2.lower().startswith("forum_") else "forum_" + f2
                        moves.append((rel2, f"FORUM/{newname}", False))
                    else:
                        moves.append((rel2, f"{top}/{inner}", False))
    return moves


def main():
    plan = build_plan()
    # dedupe / collision handling in exec
    print(f"Total move operations planned: {len(plan)}")
    # summary by new top dir / lifecycle
    from collections import Counter
    buckets = Counter()
    for old, new, rn in plan:
        parts = new.split("/")
        key = parts[0] + "/" + (parts[1] if len(parts) > 1 else "")
        buckets[key] += 1
    print("\n--- New location buckets ---")
    for k, v in sorted(buckets.items()):
        print(f"  {k:24s} {v}")
    print("\n--- Sample moves (first 25) ---")
    for old, new, rn in plan[:25]:
        print(f"  {old}  ->  {new}  [rename={rn}]")
    if len(plan) > 25:
        print(f"  ... and {len(plan)-25} more")

    if "plan" in sys.argv:
        print("\n[PLAN MODE] No filesystem changes made.")
        return

    # EXEC
    backup = BASE + "_backup_20260814"
    if not os.path.exists(backup):
        print(f"\nBacking up tracking -> {backup} ...")
        shutil.copytree(BASE, backup)
    else:
        print(f"\nBackup already exists: {backup}")

    # resolve collisions
    used = set()
    final_moves = []
    for old, new, rn in plan:
        target = new
        base, ext = os.path.splitext(new)
        i = 2
        while target in used:
            target = f"{base}_{i}{ext}"
            i += 1
        used.add(target)
        final_moves.append((old, target, rn))

    for old, new, rn in final_moves:
        src = os.path.join(BASE, old)
        dst = os.path.join(BASE, new)
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        if os.path.abspath(src) != os.path.abspath(dst):
            shutil.move(src, dst)

    # remove now-empty original region/thematic/sessions dirs
    for d in list(REGIONS) + list(THEMATIC.keys()) + KEEP_FLAT:
        p = os.path.join(BASE, d)
        if os.path.isdir(p) and not os.listdir(p):
            os.rmdir(p)
        elif os.path.isdir(p):
            # remove leftover empty subdirs
            for root2, dirs2, _ in os.walk(p, topdown=False):
                for dd in dirs2:
                    dp = os.path.join(root2, dd)
                    if not os.listdir(dp):
                        try:
                            os.rmdir(dp)
                        except OSError:
                            pass

    # write move map
    move_map = {old: new for old, new, _ in final_moves}
    with open(os.path.join(BASE, "_move_map.json"), "w", encoding="utf-8") as f:
        json.dump(move_map, f, ensure_ascii=False, indent=2)
    print(f"\nExecuted {len(final_moves)} moves. Move map -> tracking/_move_map.json")

    # create runs/ dir for labs tool
    os.makedirs(os.path.join(BASE, "runs"), exist_ok=True)
    print("Ensured tracking/runs/ exists.")


if __name__ == "__main__":
    main()
