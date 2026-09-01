#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Update hardcoded tracking paths inside .py scripts after reorg.
Reads tracking/_move_map.json (old_rel -> new_rel).
Run with `plan` arg for dry-run diff preview.
"""
import os, sys, json

BASE = r"D:\coding\traeCN_project\wqb\tracking"
WS = r"D:\coding\traeCN_project\wqb"


def main():
    with open(os.path.join(BASE, "_move_map.json"), encoding="utf-8") as f:
        move_map = json.load(f)  # old_rel -> new_rel

    # Build replacements: old_abs(bs/fs) -> new_abs(bs)
    reps = []
    for old_rel, new_rel in move_map.items():
        old_bs = (BASE + "\\" + old_rel.replace("/", "\\"))
        old_fs = (BASE + "/" + old_rel.replace("\\", "/"))
        new_bs = (BASE + "\\" + new_rel.replace("/", "\\"))
        reps.append((old_bs, new_bs))
        reps.append((old_fs, new_bs))

    # Find all .py under tracking
    py_files = []
    for root, _, files in os.walk(BASE):
        for fn in files:
            if fn.endswith(".py"):
                py_files.append(os.path.join(root, fn))

    changes = []  # (file, list of (old,new))
    for pf in py_files:
        with open(pf, encoding="utf-8", errors="ignore") as fh:
            content = fh.read()
        new_content = content
        file_changes = []
        for old, new in reps:
            if old in new_content:
                cnt = new_content.count(old)
                new_content = new_content.replace(old, new)
                file_changes.append((old, new, cnt))
        # special: kor_op_exploration_stats glob pattern
        if os.path.basename(pf) == "kor_op_exploration_stats.py":
            old_glob = r"tracking\KOR\kor_wave*.json"
            new_glob = r"tracking\KOR\candidates\kor_wave*.json"
            if old_glob in new_content:
                new_content = new_content.replace(old_glob, new_glob)
                file_changes.append((old_glob, new_glob, 1))
        # special: kor_preflight_check default whitelist
        if os.path.basename(pf) == "kor_preflight_check.py":
            old_wl = 'os.path.join(HERE, "kor_chart_cnn_alpha_field_whitelist.json")'
            new_wl = 'os.path.join(HERE, "..", "reference", "kor_chart_cnn_alpha_field_whitelist.json")'
            if old_wl in new_content:
                new_content = new_content.replace(old_wl, new_wl)
                file_changes.append((old_wl, new_wl, 1))
        if file_changes:
            changes.append((pf, file_changes, new_content))

    for pf, fc, _ in changes:
        print(f"\n### {os.path.relpath(pf, WS)}")
        for old, new, cnt in fc:
            print(f"    [x{cnt}] {old}")
            print(f"        -> {new}")

    if not changes:
        print("No script path references needed updating.")

    if "plan" in sys.argv:
        print(f"\n[PLAN MODE] {len(changes)} files would be updated. No writes.")
        return

    for pf, fc, new_content in changes:
        with open(pf, "w", encoding="utf-8") as fh:
            fh.write(new_content)
    print(f"\nUpdated {len(changes)} script files.")


if __name__ == "__main__":
    main()
