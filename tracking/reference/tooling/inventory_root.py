#!/usr/bin/env python3
"""Inventory the workspace ROOT (excluding the already-organized tracking/)."""
import os, json, re
from collections import Counter, defaultdict

ROOT = r"D:\coding\traeCN_project\wqb"
EXCLUDE_DIRS = {"tracking", ".git", ".venv", "node_modules", "__pycache__",
                ".workbuddy", "world-quant-brain-mcp"}  # heavy/binary deps

# We still want to know their existence + size, just not recurse
SPECIAL_REPORT = ["tracking", ".git", ".venv", "world-quant-brain-mcp",
                  "extensions", "node_modules"]

def human(n):
    for u in ["B", "KB", "MB", "GB", "TB"]:
        if n < 1024: return f"{n:.0f}{u}"
        n /= 1024
    return f"{n:.1f}PB"

def dir_size(path):
    tot = 0
    try:
        for dp, dn, fn in os.walk(path):
            # skip nested heavy dirs
            for f in fn:
                try: tot += os.path.getsize(os.path.join(dp, f))
                except: pass
    except: pass
    return tot

rows = []
for name in sorted(os.listdir(ROOT)):
    p = os.path.join(ROOT, name)
    is_dir = os.path.isdir(p)
    if is_dir:
        # don't recurse heavy dirs, just measure
        if name in EXCLUDE_DIRS:
            sz = dir_size(p)
            rows.append((name, "DIR(excluded)", 0, sz, ""))
        else:
            cnt = 0
            sz = 0
            for dp, dn, fn in os.walk(p):
                if any(x in dn for x in (".git", "__pycache__", ".venv")):
                    dn[:] = [x for x in dn if x not in (".git", "__pycache__", ".venv")]
                for f in fn:
                    cnt += 1
                    try: sz += os.path.getsize(os.path.join(dp, f))
                    except: pass
            rows.append((name, f"DIR({cnt} files)", cnt, sz, ""))
    else:
        ext = os.path.splitext(name)[1].lower()
        try: sz = os.path.getsize(p)
        except: sz = 0
        rows.append((name, f"FILE({ext})", 1, sz, ""))

print("="*100)
print(f"ROOT: {ROOT}")
print(f"{'name':36s} {'type':18s} {'count':>7s} {'size':>10s}")
print("-"*100)
for name, typ, cnt, sz, _ in sorted(rows, key=lambda r: (-r[3], r[0])):
    print(f"{name:36s} {typ:18s} {cnt:>7d} {human(sz):>10s}")

# Totals
tot = sum(r[3] for r in rows)
print("-"*100)
print(f"{'TOTAL (incl. excluded dirs shown)':36s} {'':18s} {sum(r[2] for r in rows):>7d} {human(tot):>10s}")

# Now: categorize ROOT-LEVEL loose files
print("\n" + "="*100)
print("ROOT-LEVEL LOOSE FILES BY EXTENSION")
print("="*100)
ext_c = Counter()
ext_sz = defaultdict(int)
for name in os.listdir(ROOT):
    p = os.path.join(ROOT, name)
    if os.path.isdir(p): continue
    ext = os.path.splitext(name)[1].lower() or "(noext)"
    try: sz = os.path.getsize(p)
    except: sz = 0
    ext_c[ext] += 1
    ext_sz[ext] += sz
for ext, c in sorted(ext_c.items(), key=lambda x: -ext_sz[x[0]]):
    print(f"  {ext:12s} count={c:4d}  size={human(ext_sz[ext])}")

# Group loose files by naming pattern
print("\n" + "="*100)
print("ROOT-LEVEL FILE GROUPS BY PREFIX PATTERN")
print("="*100)
pat = defaultdict(list)
for name in os.listdir(ROOT):
    p = os.path.join(ROOT, name)
    if os.path.isdir(p): continue
    base = name
    m = re.match(r"^([a-zA-Z_]+?)(\d+|_[a-z]+)?[_\- ]?", base)
    key = re.split(r"[\d_]", base)[0].rstrip("_").lower()[:12]
    pat[key].append(name)
for k in sorted(pat, key=lambda x: -len(pat[x])):
    if len(pat[k]) >= 2:
        print(f"  {k:14s} {len(pat[k]):3d}  e.g. {pat[k][0]}  ...  {pat[k][-1]}")
