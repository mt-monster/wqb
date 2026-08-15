#!/usr/bin/env python3
"""Universal de-hardcode: replace raw ace_lib skill path with env-aware form
across ALL .py under mining/ (scripts, diagnostics, archive)."""
import os, re, glob

ROOT = r"D:\coding\traeCN_project\wqb"
SKILL = r"C:/Users/MENGTAO/.workbuddy/skills/brain-simAlphasinBatch-and-track/scripts"
RAW_D = 'r"%s"' % SKILL
RAW_S = "r'%s'" % SKILL
ENV_D = 'os.environ.get("WQ_ACE_LIB", r"%s")' % SKILL

count = 0
for f in glob.glob(os.path.join(ROOT, "mining", "**", "*.py"), recursive=True):
    t = open(f, encoding="utf-8").read()
    if SKILL not in t:
        continue
    if "WQ_ACE_LIB" in t:
        continue  # already env-wrapped
    new = t.replace(RAW_D, ENV_D).replace(RAW_S, ENV_D)
    if "import os" not in new:
        new = "import os\n" + new
    open(f, "w", encoding="utf-8").write(new)
    count += 1
    print("  de-hardcoded", os.path.relpath(f, ROOT))
print(f"\nDe-hardcoded {count} files under mining/")
