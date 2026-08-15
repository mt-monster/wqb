#!/usr/bin/env python3
"""STAGE 2: fix path references + de-hardcode ace_lib import after the relocate.
Edits are assertion-guarded: if an expected old string is missing, it warns (no silent corruption)."""
import os, re, glob, json

ROOT = r"D:\coding\traeCN_project\wqb"
SKILL = r"C:/Users/MENGTAO/.workbuddy/skills/brain-simAlphasinBatch-and-track/scripts"
ENV_D = 'os.environ.get("WQ_ACE_LIB", r"%s")' % SKILL
ENV_S = "os.environ.get('WQ_ACE_LIB', r'%s')" % SKILL
ROOT_DEF = 'ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))'

def patch(path, repls):
    t = open(path, encoding="utf-8").read()
    orig = t
    for old, new in repls:
        if old not in t:
            print(f"  [WARN] expected substring NOT found in {os.path.relpath(path, ROOT)}:\n        {old!r}")
            continue
        t = t.replace(old, new, 1)
    if t != orig:
        open(path, "w", encoding="utf-8").write(t)
        print(f"  patched {os.path.relpath(path, ROOT)}")
    else:
        print(f"  (no change) {os.path.relpath(path, ROOT)}")

print("== harvest_fields_v2.py ==")
patch(os.path.join(ROOT, "mining", "scripts", "harvest_fields_v2.py"), [
    ('import sys, re, json, time\n',
     'import sys, re, json, time, os\n' + ROOT_DEF + '\n'),
    ('sys.path.insert(0, r"%s")' % SKILL,
     'sys.path.insert(0, %s)' % ENV_D),
    ('with open("all_fields.json","w") as f:',
     'with open(os.path.join(ROOT, "data_ref", "all_fields.json"), "w") as f:'),
])

print("== enum_mdl177.py ==")
patch(os.path.join(ROOT, "mining", "scripts", "enum_mdl177.py"), [
    ("sys.path.insert(0, r'%s')" % SKILL,
     'sys.path.insert(0, %s)' % ENV_S),
    ("cfg = json.load(open(r'%s/configs/config.json'))" % SKILL,
     "cfg = json.load(open(os.path.join(os.path.dirname(%s), 'configs', 'config.json')))" % ENV_S),
    ("json.dump(all_fields, open(r'D:/coding/traeCN_project/wqb/mdl177_fields.json', 'w'), indent=2)",
     "json.dump(all_fields, open(os.path.join(ROOT, 'data_ref', 'mdl177_fields.json'), 'w'), indent=2)"),
])
# add ROOT to enum_mdl177 (it imports os already)
p = os.path.join(ROOT, "mining", "scripts", "enum_mdl177.py")
t = open(p, encoding="utf-8").read()
if "ROOT =" not in t:
    t = t.replace("import json, sys, os, time\n",
                  "import json, sys, os, time\n" + ROOT_DEF + "\n", 1)
    open(p, "w", encoding="utf-8").write(t)
    print("  added ROOT to enum_mdl177.py")

print("== tools/sync_reference.py ==")
patch(os.path.join(ROOT, "tools", "sync_reference.py"), [
    ('os.path.join(ROOT, "reference")', 'os.path.join(ROOT, "docs", "reference")'),
])

print("== docs/experience/mining_experience/rules.json ==")
rp = os.path.join(ROOT, "docs", "experience", "mining_experience", "rules.json")
if os.path.exists(rp):
    t = open(rp, encoding="utf-8").read()
    if '"source": "os_alpha_experience_summary.md"' in t:
        t = t.replace('"source": "os_alpha_experience_summary.md"',
                      '"source": "../os_alpha_experience_summary.md"')
        open(rp, "w", encoding="utf-8").write(t)
        print("  patched rules.json source path")
    else:
        print("  (no change) rules.json")

print("== docs/experience/mining_experience/README.md ==")
rd = os.path.join(ROOT, "docs", "experience", "mining_experience", "README.md")
if os.path.exists(rd):
    patch(rd, [("os_alpha_experience_summary.md  (", "../os_alpha_experience_summary.md  (")])

print("== docs/experience/project_experience_master.md (reference/ -> docs/reference/) ==")
patch(os.path.join(ROOT, "docs", "experience", "project_experience_master.md"), [
    ("`reference/`", "`docs/reference/`"),
    ("`reference/usa_d0_mining_experience.md`", "`docs/reference/usa_d0_mining_experience.md`"),
])

print("== de-hardcode archived mine_v* (ace_lib import) ==")
for f in glob.glob(os.path.join(ROOT, "mining", "archive", "mine_v*.py")):
    t = open(f, encoding="utf-8").read()
    orig = t
    if ("SKILL_DIR = r" in t) or ('SKILL_DIR = r"' in t):
        t = re.sub(r'SKILL_DIR = r?["\'][^"\']*brain-simAlphasinBatch-and-track/scripts["\']',
                   'import os\nSKILL_DIR = ' + ENV_D, t, count=1)
    elif "sys.path.insert(0, r" in t or "sys.path.insert(0, r'" in t:
        t = re.sub(r'sys\.path\.insert\(0, r?["\'][^"\']*brain-simAlphasinBatch-and-track/scripts["\']\)',
                   'import os\nsys.path.insert(0, ' + ENV_D + ')', t, count=1)
    if t != orig:
        open(f, "w", encoding="utf-8").write(t)
print(f"  scanned {len(glob.glob(os.path.join(ROOT,'mining','archive','mine_v*.py')))} mine_v* scripts")

print("\nSTAGE 2 DONE")
