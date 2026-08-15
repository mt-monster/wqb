#!/usr/bin/env python3
"""STAGE 1: backup + relocate root-level loose files into a clean layout.
Run with `plan` arg to preview; otherwise executes.
Layout targets:
  mining/scripts/        active mining+harvest scripts
  mining/scripts/diagnostics/   one-off investigate/verify/probe/check scripts
  mining/archive/         mine_v6..v27 triad (py+log+results)
  polling/archive/        legacy sim_*_poll.sh
  logs/                   scattered *.log (except mine_v*.log -> archive)
  data_ref/               field catalogs + candidate/seed lists
  docs/plans/             planning md
  docs/experience/        os_alpha_experience_summary.md
  docs/reference/         merge root reference/  (exists)
  docs/experience/mining_experience/  whole pkg move
  tracking/GLB/           misplaced glb_d1_batch01.json
  tracking/reference/tooling/  cleanup helper scripts
Deletions: WebData zip (dup), tracking_backup (zip->archive/large), empty src/ automation/ wqb-share-03/
"""
import os, sys, shutil, glob, re

ROOT = r"D:\coding\traeCN_project\wqb"
BACKUP = os.path.join(ROOT, "root_backup_20260814b")

def ensure(p): os.makedirs(p, exist_ok=True)

def move_item(src, dst):
    if os.path.isfile(src):
        d = dst
        if os.path.isdir(dst):
            d = os.path.join(dst, os.path.basename(src))
        ensure(os.path.dirname(d))
        shutil.move(src, d)
    else:
        if not os.path.exists(dst):
            ensure(os.path.dirname(dst))
            shutil.move(src, dst)
        else:
            for c in os.listdir(src):
                move_item(os.path.join(src, c), os.path.join(dst, c))
            try: os.rmdir(src)
            except OSError: pass

def build_plan():
    plan = []  # (src, dst)
    # mine_v* triad -> mining/archive/
    for f in glob.glob(os.path.join(ROOT, "mine_v*.py")):
        plan.append((f, os.path.join(ROOT, "mining", "archive", os.path.basename(f))))
    for f in glob.glob(os.path.join(ROOT, "mine_v*_results.json")):
        plan.append((f, os.path.join(ROOT, "mining", "archive", os.path.basename(f))))
    for f in glob.glob(os.path.join(ROOT, "mine_v*.log")):
        if f.endswith("_run.log"):
            continue  # run logs -> logs/, not the archive triad
        plan.append((f, os.path.join(ROOT, "mining", "archive", os.path.basename(f))))
    # active mining/harvest scripts
    for n in ["harvest_fields.py", "harvest_fields_v2.py", "harvest_usa.py",
              "enum_mdl177.py", "gen_v5.py", "mine_corr.py"]:
        plan.append((os.path.join(ROOT, n), os.path.join(ROOT, "mining", "scripts", n)))
    # diagnostics
    for n in ["investigate_account.py", "investigate_os.py", "investigate_os2.py",
              "investigate_selfcorr.py", "verify_3set.py", "verify_submit_fC.py",
              "probe_region.py", "check_state.py"]:
        plan.append((os.path.join(ROOT, n), os.path.join(ROOT, "mining", "scripts", "diagnostics", n)))
    # logs (non mine_v) -> logs/
    for f in glob.glob(os.path.join(ROOT, "*.log")):
        if re.match(r"mine_v\d+\.log$", os.path.basename(f)):
            continue
        plan.append((f, os.path.join(ROOT, "logs", os.path.basename(f))))
    # data_ref: field catalogs + seed lists
    for n in ["all_fields.json", "mdl177_fields.json", "kor_seed_candidates.txt",
              "risk60_f.txt", "risk62_f.txt", "risk64_f.txt", "risk88_f.txt",
              "fundamental14_f.txt", "fundamental17_f.txt"]:
        if os.path.exists(os.path.join(ROOT, n)):
            plan.append((os.path.join(ROOT, n), os.path.join(ROOT, "data_ref", n)))
    # planning md -> docs/plans
    for n in ["task_plan.md", "progress.md", "findings.md"]:
        plan.append((os.path.join(ROOT, n), os.path.join(ROOT, "docs", "plans", n)))
    # os_alpha_experience_summary -> docs/experience
    plan.append((os.path.join(ROOT, "os_alpha_experience_summary.md"),
                 os.path.join(ROOT, "docs", "experience", "os_alpha_experience_summary.md")))
    # reference/ -> docs/reference/ (merge)
    plan.append((os.path.join(ROOT, "reference"), os.path.join(ROOT, "docs", "reference")))
    # mining_experience/ -> docs/experience/mining_experience/
    plan.append((os.path.join(ROOT, "mining_experience"),
                 os.path.join(ROOT, "docs", "experience", "mining_experience")))
    # misplaced glb json -> tracking/GLB
    plan.append((os.path.join(ROOT, "wqb-share-03", "tracking", "glb_d1_batch01.json"),
                 os.path.join(ROOT, "tracking", "GLB", "glb_d1_batch01.json")))
    # legacy pollers -> polling/archive
    for f in glob.glob(os.path.join(ROOT, "sim_*poll*.sh")):
        plan.append((f, os.path.join(ROOT, "polling", "archive", os.path.basename(f))))
    # cleanup helpers -> tracking/reference/tooling
    for n in ["inventory_root.py", "refcheck_root.py"]:
        if os.path.exists(os.path.join(ROOT, n)):
            plan.append((os.path.join(ROOT, n),
                         os.path.join(ROOT, "tracking", "reference", "tooling", n)))
    return plan

def main():
    plan = build_plan()
    if len(sys.argv) > 1 and sys.argv[1] == "plan":
        print(f"PLAN: {len(plan)} moves\n")
        for s, d in plan:
            print(f"  {os.path.relpath(s, ROOT)}  ->  {os.path.relpath(d, ROOT)}")
        # deletions preview
        print("\nDELETIONS (after move):")
        print("  WebData_20260219_V0.10.9.zip  (dup of research-data/WebData_20260219_V0.10.9)")
        print("  tracking_backup_20260814/  -> zip to tracking/archive/large/")
        print("  src/  (empty)")
        print("  automation/  (empty)")
        print("  wqb-share-03/  (emptied after file move)")
        print("  root_backup_20260814b/  (self backup, removed at end)")
        return
    # 1. backup
    print("Backing up to", os.path.relpath(BACKUP, ROOT))
    for s, d in plan:
        rel = os.path.relpath(s, ROOT)
        bp = os.path.join(BACKUP, rel)
        if os.path.isfile(s):
            ensure(os.path.dirname(bp)); shutil.copy2(s, bp)
        elif os.path.isdir(s):
            if os.path.exists(bp): shutil.rmtree(bp)
            shutil.copytree(s, bp)
    # 2. execute moves
    for s, d in plan:
        if os.path.exists(s):
            move_item(s, d)
            print("moved", os.path.relpath(s, ROOT), "->", os.path.relpath(d, ROOT))
    # 3. deletions
    z = os.path.join(ROOT, "WebData_20260219_V0.10.9.zip")
    if os.path.exists(z):
        os.remove(z); print("deleted", os.path.basename(z))
    tb = os.path.join(ROOT, "tracking_backup_20260814")
    if os.path.isdir(tb):
        arch = os.path.join(ROOT, "tracking", "archive", "large")
        ensure(arch)
        shutil.make_archive(os.path.join(arch, "tracking_backup_20260814"), "zip", tb)
        shutil.rmtree(tb); print("zipped tracking_backup_20260814 -> tracking/archive/large/")
    for d in ["src", "automation", "wqb-share-03"]:
        p = os.path.join(ROOT, d)
        if os.path.isdir(p) and not os.listdir(p):
            os.rmdir(p); print("removed empty", d)
    # 4. gitignore
    gi = os.path.join(ROOT, ".gitignore")
    txt = open(gi, encoding="utf-8").read()
    add = []
    if ".qoder/" not in txt: add.append(".qoder/")
    if ".vscode/" not in txt: add.append(".vscode/")
    if add:
        with open(gi, "a", encoding="utf-8") as f:
            f.write("\n# agent/IDE state\n" + "\n".join(add) + "\n")
        print("updated .gitignore:", add)
    # 5. remove self backup
    if os.path.isdir(BACKUP):
        shutil.rmtree(BACKUP)
    print("\nSTAGE 1 DONE")

if __name__ == "__main__":
    main()
