#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Import skill folders (ZIP URL / Git repo / local dir) into a **quarantine staging directory**,
with a security audit. It never installs into a live skill root by default.

Usage:
  python pull_skills.py <zip_url | git_url | local_dir> [--dest <dir>] [--branch <b>]
                        [--overwrite] [--allow-live-dest] [--accept-risk]

Why (skills review PB-01/02/03, 2026-09-29): an imported skill is **instructions + executable material
injected into the agent runtime** (frontmatter `hooks:` run arbitrary commands, `scripts/` are run by
the agent). The old importer copied straight into a live root, `--overwrite` did `shutil.rmtree` with no
backup, and the documented default destination differed from the code.

Behavior:
- Default destination is a staging dir: `<repo>/attic/import_staging` (repo = nearest parent that holds
  `Claude/skills`; `attic/` is git-ignored) or `<cwd>/import_staging`. **Nothing is installed.** After a
  human reviews the audit, move the folder into `Claude/skills/` and run `python tools/sync_skills.py`.
- Every candidate gets an audit: frontmatter `hooks:` / `allowed-tools:`, `scripts/` inventory, symlinks,
  and risky-pattern hits (credential/.env/ssh reads, network egress, deletion, dynamic execution),
  plus a name-collision check against live roots. Risk is `low` / `review` / `high`.
- `--overwrite` never deletes: the existing folder is moved to `<dest>/.backup/<name>_<timestamp>`.
- A live skill root as destination (Claude/skills, ~/.claude/skills, ~/.codex/skills, ~/.cursor/skills,
  ~/.workbuddy/skills, <cwd>/.qoder/skills) needs `--allow-live-dest`; even then, folders whose risk is
  not `low` are skipped unless `--accept-risk` is given.
- Nothing from the imported folders is ever executed by this tool.

Notes:
- Requires Git in PATH only for git URLs. Only checks that SKILL.md/skill.md exists (case-insensitive);
  it does not validate YAML semantics. Copies top-level folders only.
"""

import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
import zipfile
from typing import Dict, List, Optional, Tuple

LIVE_ROOT_HINTS = (
    os.path.join("~", ".claude", "skills"),
    os.path.join("~", ".codex", "skills"),
    os.path.join("~", ".cursor", "skills"),
    os.path.join("~", ".workbuddy", "skills"),
    os.path.join("~", ".qoder-cn", "skills"),
)

#: (pattern, label) — applied to every text file inside the candidate folder
RISK_PATTERNS: List[Tuple[str, str]] = [
    (r"(?i)\.env\b|credentials|\.ssh\b|id_rsa|api[_-]?key|passw(or)?d\s*[:=]", "credential/secret access"),
    (r"(?i)\b(curl|wget|Invoke-WebRequest|iwr)\b|requests\.(post|put)|urllib\.request|httpx\.(post|put)|socket\.", "network egress"),
    (r"(?i)\brm\s+-rf\b|shutil\.rmtree|Remove-Item\s+.*-Recurse|os\.remove|unlink\(", "deletion"),
    (r"\beval\s*\(|\bexec\s*\(|os\.system|subprocess\.|Invoke-Expression|powershell\s+-enc|base64\s+-d", "dynamic/shell execution"),
]
TEXT_SUFFIXES = {".md", ".py", ".sh", ".ps1", ".bat", ".cmd", ".js", ".ts", ".json", ".yaml", ".yml", ".toml", ".txt", ""}
MAX_SCAN_BYTES = 512 * 1024


def run(cmd: List[str], cwd: Optional[str] = None) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)


def ensure_dir(path: str) -> None:
    os.makedirs(path, exist_ok=True)


# ---------------------------------------------------------------- roots / destination
def find_repo_root(start: Optional[str] = None) -> Optional[str]:
    here = os.path.abspath(start or os.getcwd())
    for _ in range(8):
        if os.path.isdir(os.path.join(here, "Claude", "skills")):
            return here
        parent = os.path.dirname(here)
        if parent == here:
            break
        here = parent
    return None


def default_staging_dir(cwd: Optional[str] = None) -> str:
    root = find_repo_root(cwd)
    if root:
        return os.path.join(root, "attic", "import_staging")
    return os.path.join(os.path.abspath(cwd or os.getcwd()), "import_staging")


def live_roots(cwd: Optional[str] = None) -> List[str]:
    roots = [os.path.realpath(os.path.expanduser(h)) for h in LIVE_ROOT_HINTS]
    roots.append(os.path.realpath(os.path.join(os.path.abspath(cwd or os.getcwd()), ".qoder", "skills")))
    repo = find_repo_root(cwd)
    if repo:
        roots.append(os.path.realpath(os.path.join(repo, "Claude", "skills")))
    return roots


def is_live_dest(dest: str, cwd: Optional[str] = None) -> bool:
    d = os.path.realpath(dest)
    return any(d == r or d.startswith(r + os.sep) for r in live_roots(cwd))


# ---------------------------------------------------------------- audit
def _frontmatter(text: str) -> str:
    m = re.match(r"^---\s*\n(.*?)\n---\s*(\n|$)", text, re.S)
    return m.group(1) if m else ""


def audit_skill_folder(folder: str) -> Dict[str, object]:
    """Static audit of one candidate folder. Never executes anything from it."""
    findings: List[str] = []
    scripts: List[str] = []
    symlinks: List[str] = []
    fm = ""
    for root, dirs, files in os.walk(folder):
        for name in list(dirs) + list(files):
            p = os.path.join(root, name)
            rel = os.path.relpath(p, folder).replace(os.sep, "/")
            if os.path.islink(p):
                symlinks.append(rel)
        for name in files:
            p = os.path.join(root, name)
            rel = os.path.relpath(p, folder).replace(os.sep, "/")
            if os.path.islink(p):
                continue
            if rel.startswith("scripts/") or name.lower().endswith((".sh", ".ps1", ".bat", ".cmd", ".py", ".js")):
                scripts.append(rel)
            if os.path.splitext(name)[1].lower() not in TEXT_SUFFIXES:
                continue
            try:
                if os.path.getsize(p) > MAX_SCAN_BYTES:
                    findings.append(f"{rel}: file too large to scan (> {MAX_SCAN_BYTES // 1024} KB)")
                    continue
                with open(p, "r", encoding="utf-8", errors="replace") as f:
                    text = f.read()
            except OSError:
                continue
            if name.lower() == "skill.md" and root == folder:
                fm = _frontmatter(text)
            for pat, label in RISK_PATTERNS:
                hits = re.findall(pat, text)
                if hits:
                    findings.append(f"{rel}: {label} ×{len(hits)}")
    has_hooks = bool(re.search(r"(?m)^hooks\s*:", fm))
    allowed_tools = re.search(r"(?m)^allowed-tools\s*:\s*(.*)$", fm)
    if has_hooks:
        findings.insert(0, "frontmatter `hooks:` — runs commands at agent lifecycle events (must be reviewed line by line)")
    if allowed_tools:
        findings.insert(0, f"frontmatter `allowed-tools:` {allowed_tools.group(1).strip()[:80]}")
    if symlinks:
        findings.insert(0, f"symlinks: {', '.join(symlinks[:5])}")
    if has_hooks or symlinks or (allowed_tools and "bash" in allowed_tools.group(1).lower()):
        risk = "high"
    elif findings or scripts:
        risk = "review"
    else:
        risk = "low"
    return {"risk": risk, "hooks": has_hooks, "allowed_tools": allowed_tools.group(1).strip() if allowed_tools else None,
            "scripts": scripts[:30], "symlinks": symlinks, "findings": findings[:40]}


# ---------------------------------------------------------------- copy
def copy_skill_folder(src_folder: str, dest_root: str, overwrite: bool, *, backup: bool = True) -> Dict[str, str]:
    name = os.path.basename(src_folder.rstrip("/\\"))
    dest_folder = os.path.join(dest_root, name)

    # Check for SKILL.md existence (case-insensitive: SKILL.md / skill.md both accepted)
    if not any(f.lower() == "skill.md" for f in os.listdir(src_folder)):
        return {"status": "skipped", "folder": name, "reason": "no SKILL.md/skill.md found (case-insensitive)"}

    backed_up = None
    if os.path.exists(dest_folder):
        if not overwrite:
            return {"status": "skipped", "folder": name, "reason": "exists (use --overwrite to replace; a backup is kept)"}
        # Never delete: move the existing folder aside (recoverable).
        backup_dir = os.path.join(dest_root, ".backup")
        ensure_dir(backup_dir)
        backed_up = os.path.join(backup_dir, f"{name}_{time.strftime('%Y%m%d_%H%M%S')}")
        shutil.move(dest_folder, backed_up)

    shutil.copytree(src_folder, dest_folder, symlinks=True)   # symlinks copied as links, never followed
    out = {"status": "copied", "folder": name, "dest": dest_folder}
    if backed_up:
        out["backup"] = backed_up
    return out


def _safe_extract(zf: zipfile.ZipFile, target: str) -> None:
    """Zip-slip guard: every member must resolve inside `target`."""
    base = os.path.realpath(target)
    for member in zf.namelist():
        resolved = os.path.realpath(os.path.join(base, member))
        if resolved != base and not resolved.startswith(base + os.sep):
            raise ValueError(f"unsafe zip member path: {member}")
    zf.extractall(target)


# ---------------------------------------------------------------- main
def parse_args(argv: List[str]) -> Dict[str, object]:
    opts: Dict[str, object] = {"src": argv[0], "dest": None, "branch": None, "overwrite": False,
                               "allow_live": False, "accept_risk": False}
    i = 1
    while i < len(argv):
        a = argv[i]
        if a == "--dest" and i + 1 < len(argv):
            opts["dest"] = argv[i + 1]
            i += 2
        elif a == "--branch" and i + 1 < len(argv):
            opts["branch"] = argv[i + 1]
            i += 2
        elif a == "--overwrite":
            opts["overwrite"] = True
            i += 1
        elif a == "--allow-live-dest":
            opts["allow_live"] = True
            i += 1
        elif a == "--accept-risk":
            opts["accept_risk"] = True
            i += 1
        else:
            i += 1
    return opts


def main() -> None:
    if len(sys.argv) < 2:
        print(json.dumps({
            "ok": False,
            "error": "Missing source (zip url / git url / local dir)",
            "usage": "python pull_skills.py <zip_url|git_url|local_dir> [--dest <dir>] [--branch <b>] "
                     "[--overwrite] [--allow-live-dest] [--accept-risk]",
        }, ensure_ascii=False))
        sys.exit(1)

    o = parse_args(sys.argv[1:])
    repo_url = str(o["src"])
    dest = str(o["dest"] or default_staging_dir())
    live = is_live_dest(dest)
    if live and not o["allow_live"]:
        print(json.dumps({
            "ok": False, "stage": "dest_check", "dest": dest,
            "error": "destination is a LIVE skill root; imported skills carry instructions/hooks/scripts. "
                     "Stage first (omit --dest), review the audit, move reviewed folders into Claude/skills/, "
                     "then run tools/sync_skills.py. To really write here pass --allow-live-dest.",
        }, ensure_ascii=False))
        sys.exit(3)
    ensure_dir(dest)

    tempdir = tempfile.mkdtemp(prefix="pull_skills_")
    repo_dir = os.path.join(tempdir, "repo")
    try:
        if os.path.isdir(repo_url):                                   # Case 1: local directory
            try:
                shutil.copytree(repo_url, repo_dir, symlinks=True, dirs_exist_ok=True)
            except Exception as e:
                print(json.dumps({"ok": False, "stage": "copy_local", "error": str(e)}, ensure_ascii=False))
                sys.exit(2)
        elif repo_url.lower().endswith(".zip"):                        # Case 2: ZIP URL
            import urllib.request
            try:
                zip_path = os.path.join(tempdir, "repo.zip")
                urllib.request.urlretrieve(repo_url, zip_path)
                extract_dir = os.path.join(tempdir, "extracted")
                with zipfile.ZipFile(zip_path, "r") as zf:
                    _safe_extract(zf, extract_dir)
                contents = os.listdir(extract_dir)
                if len(contents) == 1 and os.path.isdir(os.path.join(extract_dir, contents[0])):
                    shutil.move(os.path.join(extract_dir, contents[0]), repo_dir)     # GitHub zip: <repo-branch>/
                else:
                    shutil.move(extract_dir, repo_dir)
            except Exception as e:
                print(json.dumps({"ok": False, "stage": "download_zip", "error": str(e), "url": repo_url},
                                 ensure_ascii=False))
                sys.exit(2)
        else:                                                         # Case 3: Git clone
            clone_cmd = ["git", "clone", "--depth", "1"]
            if o["branch"]:
                clone_cmd += ["--branch", str(o["branch"])]
            clone_cmd += [repo_url, repo_dir]
            cp = run(clone_cmd)
            if cp.returncode != 0:
                print(json.dumps({"ok": False, "stage": "clone", "cmd": " ".join(clone_cmd),
                                  "stderr": cp.stderr.strip(), "stdout": cp.stdout.strip()}, ensure_ascii=False))
                sys.exit(2)

        existing_live = set()
        for r in live_roots():
            if os.path.isdir(r):
                existing_live.update(os.listdir(r))

        copied: List[Dict[str, object]] = []
        skipped: List[Dict[str, object]] = []
        for entry in sorted(os.listdir(repo_dir)):
            sub = os.path.join(repo_dir, entry)
            if not os.path.isdir(sub) or os.path.islink(sub) or entry == ".git":
                continue
            if not any(f.lower() == "skill.md" for f in os.listdir(sub)):
                skipped.append({"status": "skipped", "folder": entry, "reason": "no SKILL.md/skill.md found (case-insensitive)"})
                continue
            audit = audit_skill_folder(sub)
            audit["name_collision_with_live"] = entry in existing_live
            if live and audit["risk"] != "low" and not o["accept_risk"]:
                skipped.append({"status": "skipped", "folder": entry, "reason": f"risk={audit['risk']} — review, then re-run with --accept-risk",
                                "audit": audit})
                continue
            res: Dict[str, object] = dict(copy_skill_folder(sub, dest, bool(o["overwrite"])))
            res["audit"] = audit
            (copied if res["status"] == "copied" else skipped).append(res)

        print(json.dumps({
            "ok": True, "repo": repo_url, "dest": dest, "dest_is_live_root": live,
            "staged_only": not live,
            "next_step": ("REVIEW each audit (hooks / allowed-tools / scripts / findings). Then move reviewed folders into "
                          "Claude/skills/ and run `python tools/sync_skills.py` (+ `--check`)." if not live else
                          "Written to a live root: restart the agent host and re-run the skill integrity tests."),
            "copied": copied, "skipped": skipped,
        }, indent=2, ensure_ascii=False))
    finally:
        shutil.rmtree(tempdir, ignore_errors=True)   # our own temp clone only — never a user/skill folder


if __name__ == "__main__":
    main()
