import os, re, json

BASE = r"D:\coding\traeCN_project\wqb\world-quant-brain-mcp\.venv\Lib\site-packages\cnhkmcp\untracked\skills"

def parse_frontmatter(text):
    m = re.match(r'^---\s*\n(.*?)\n---\s*\n', text, re.S)
    if not m:
        return None
    fm = {}
    for line in m.group(1).splitlines():
        if ':' in line:
            k, v = line.split(':', 1)
            fm[k.strip()] = v.strip()
    return fm

report = {}
for skill in sorted(os.listdir(BASE)):
    sp = os.path.join(BASE, skill)
    if not os.path.isdir(sp):
        continue
    skill_md = os.path.join(sp, "SKILL.md")
    if not os.path.isfile(skill_md):
        report[skill] = {"name": None, "broken": ["NO_SKILL.md"]}
        continue
    text = open(skill_md, encoding="utf-8").read()
    fm = parse_frontmatter(text)
    name = fm.get("name") if fm else None
    # extract md/json relative links
    links = re.findall(r'\[[^\]]*\]\(([^)]+)\)', text)
    broken = []
    for l in links:
        if l.startswith(("http://", "https://", "mcp_")):
            continue
        if not re.search(r'\.(md|json|sh|py|html)$', l):
            continue
        clean = re.sub(r'#.*$', '', l)
        target = os.path.normpath(os.path.join(sp, clean))
        if not os.path.exists(target):
            broken.append(clean)
    report[skill] = {"name": name, "name_matches_dir": (name == skill), "broken": broken}

# print
print(f"{'SKILL':<40} {'name==dir?':<12} BROKEN_LINKS")
for skill, r in report.items():
    nm = "OK" if r["name_matches_dir"] else f"NO('{r['name']}')"
    br = ", ".join(r["broken"]) if r["broken"] else "-"
    print(f"{skill:<40} {nm:<12} {br}")
