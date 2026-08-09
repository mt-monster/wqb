#!/usr/bin/env python3
"""Sync reference/ and .workbuddy/reference/ from 2_reference/ (authoritative source).

Keeps the skill-facing copies in lockstep with the single editable source,
resolving the duplicate-reference drift risk (project-structure issue C).

    python tools/sync_reference.py
"""
import os
import shutil

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "2_reference")
TARGETS = [
    os.path.join(ROOT, "reference"),
    os.path.join(ROOT, ".workbuddy", "reference"),
]


def sync(src, dst):
    if not os.path.isdir(src):
        print(f"SKIP (source missing): {src}")
        return
    os.makedirs(dst, exist_ok=True)
    # remove dst entries no longer present in src (prevents stale drift)
    for name in os.listdir(dst):
        s = os.path.join(src, name)
        d = os.path.join(dst, name)
        if not os.path.exists(s):
            if os.path.isdir(d) and not os.path.islink(d):
                shutil.rmtree(d)
            else:
                os.remove(d)
    # copy src -> dst
    for name in os.listdir(src):
        s = os.path.join(src, name)
        d = os.path.join(dst, name)
        if os.path.isdir(s):
            shutil.copytree(s, d, dirs_exist_ok=True)
        else:
            shutil.copy2(s, d)
    print(f"SYNCED {src} -> {dst}")


if __name__ == "__main__":
    for t in TARGETS:
        sync(SRC, t)
    print("DONE")
