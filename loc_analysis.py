import os
ROOT = "."
EXCLUDE = {".venv","__pycache__","node_modules","tracking",".git",".workbuddy"}
counts = {}
total = 0
files = []
for dirpath, dirnames, filenames in os.walk(ROOT):
    parts = dirpath.replace("\\","/").split("/")
    if any(p in EXCLUDE for p in parts):
        continue
    for fn in filenames:
        if fn.endswith(".py"):
            p = os.path.join(dirpath, fn).replace("\\","/")
            try:
                with open(p, encoding="utf-8", errors="ignore") as f:
                    n = sum(1 for _ in f)
            except:
                n = 0
            files.append((p, n))
            total += n
            top = p.split("/")[0] if "/" in p else "."
            counts[top] = counts.get(top, 0) + n
print("=== TOTAL PY FILES:", len(files), " TOTAL LOC:", total)
print("\n=== LOC by top-level dir ===")
for k in sorted(counts, key=lambda x:-counts[x]):
    print(f"  {k:30s} {counts[k]}")
print("\n=== TOP 30 LARGEST FILES ===")
for p,n in sorted(files, key=lambda x:-x[1])[:30]:
    print(f"  {n:6d}  {p}")
