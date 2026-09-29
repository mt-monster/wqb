# -*- coding: utf-8 -*-
"""skill frontmatter 的 `hooks:` / `allowed-tools:` 守护（skills 审查 PW-01 / IX-18 / X-9 / X-17 #14，2026-09-29）。

skill 是运行时输入：`hooks:` 等价于「在 agent 生命周期事件上执行任意命令」，`allowed-tools:` 决定 skill 能调哪些工具。
此前全库没有任何审查规则——INDEX 只有「边界」的形式检查。规则：
  1. 只有白名单里的 skill 可以声明 hooks（现在只有 planning-with-files），新增须先审查再入白名单；
  2. 钩子命令不得含未解析的占位符（如 `<SKILL_ROOT>`：sync_skills 不替换，命令必然执行失败），
     不得含外发 / 动态执行 / 删除 / 凭据读取；
  3. allowed-tools 棘轮：任何 skill 不得比基线多出工具（要加，先改 tests/fixtures/skill_capabilities_baseline.json
     并写明理由，由人审查）。
"""
import json
import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
SKILLS = ROOT / "Claude" / "skills"
BASELINE = json.loads((ROOT / "tests" / "fixtures" / "skill_capabilities_baseline.json").read_text(encoding="utf-8"))

ALLOWED_HOOK_SKILLS = {"planning-with-files"}
DANGEROUS = [
    (r"\b(curl|wget)\b|Invoke-WebRequest|\biwr\b|\bnc\s|requests\.", "network egress"),
    (r"\beval\b|Invoke-Expression|base64\s+-d|powershell\s+-enc|\bsh\s+-c\s+\"?\$\(", "dynamic execution"),
    (r"\brm\s+-rf\b|Remove-Item|shutil\.rmtree|\bmkfs\b|\bdd\s+if=", "deletion"),
    (r"\.env\b|credentials|\.ssh\b|api[_-]?key|passw(or)?d", "credential access"),
]


def _frontmatter_text(path: Path) -> str:
    m = re.match(r"^---\n(.*?)\n---\n", path.read_text(encoding="utf-8"), re.S)
    assert m, f"{path}: 缺 frontmatter"
    # 去掉整行注释（钩子旁的说明），避免被当成命令解析
    return "\n".join(ln for ln in m.group(1).splitlines() if not ln.lstrip().startswith("#"))


def _frontmatter(path: Path):
    """只解析本测试需要的几个键（不引入 PyYAML：MCP venv 没装）。"""
    fm = _frontmatter_text(path)
    tools = []
    m = re.search(r"(?m)^allowed-tools:\s*\n((?:[ \t]+-[^\n]*\n?)+)", fm + "\n")
    if m:
        tools = [ln.strip()[1:].strip() for ln in m.group(1).splitlines() if ln.strip().startswith("-")]
    hooks_text = ""
    hm = re.search(r"(?m)^hooks:\s*\n((?:[ \t]+[^\n]*\n?)+)", fm + "\n")
    if hm:
        hooks_text = hm.group(1)
    cmds = []
    for cm in re.finditer(r'(?m)^[ \t-]*command:\s*("(?:[^"\\]|\\.)*"|\'[^\']*\')\s*$', hooks_text):
        raw = cm.group(1)
        cmds.append(json.loads(raw) if raw.startswith('"') else raw[1:-1])
    stop = []
    sm = re.search(r"(?m)^[ \t]+Stop:\s*\n((?:[ \t]{4,}[^\n]*\n?)+)", hooks_text)
    if sm:
        for cm in re.finditer(r'command:\s*("(?:[^"\\]|\\.)*")', sm.group(1)):
            stop.append(json.loads(cm.group(1)))
    return {"allowed-tools": tools, "hooks": {"_commands": cmds, "Stop": stop} if hooks_text else None}


def _all():
    return {p.parent.name: _frontmatter(p) for p in sorted(SKILLS.glob("*/SKILL.md"))}


def _hook_commands(hooks):
    if not hooks:
        return []
    return list(hooks.get("_commands", []))


def test_only_reviewed_skills_declare_hooks():
    declaring = {name for name, fm in _all().items() if fm.get("hooks")}
    assert declaring <= ALLOWED_HOOK_SKILLS, (
        f"新增了带 hooks 的 skill: {sorted(declaring - ALLOWED_HOOK_SKILLS)}。hooks = 在生命周期事件上执行任意命令，"
        "须先人工审查命令，再把它加入 ALLOWED_HOOK_SKILLS（并写明理由）。")


@pytest.mark.parametrize("name", sorted(ALLOWED_HOOK_SKILLS))
def test_hook_commands_are_resolvable_and_harmless(name):
    fm = _all()[name]
    cmds = _hook_commands(fm.get("hooks"))
    assert cmds, f"{name} 声明了 hooks 却没有命令？"
    for c in cmds:
        assert not re.search(r"<[A-Za-z_]{3,}>", c), f"{name}: 钩子命令含未解析占位符（sync_skills 不替换）: {c}"
        for pat, label in DANGEROUS:
            assert not re.search(pat, c), f"{name}: 钩子命令含 {label}: {c}"


def test_planning_with_files_stop_hook_is_inline_and_never_blocks(tmp_path):
    """Stop 钩子：无 task_plan.md 静默；有未完成阶段只提醒（stderr），任何情形 exit 0。"""
    import subprocess
    cmd = [c for c in _all()["planning-with-files"]["hooks"]["Stop"] if "task_plan" in c][0]
    assert "check-complete.sh" not in cmd
    r = subprocess.run(cmd, shell=True, cwd=tmp_path, capture_output=True, text=True)
    assert (r.returncode, r.stdout, r.stderr) == (0, "", "")
    (tmp_path / "task_plan.md").write_text("### Phase 1\n**Status:** complete\n### Phase 2\n**Status:** pending\n")
    r = subprocess.run(cmd, shell=True, cwd=tmp_path, capture_output=True, text=True)
    assert r.returncode == 0 and "1/2 phases complete" in r.stderr
    (tmp_path / "task_plan.md").write_text("### Phase 1\n**Status:** complete\n")
    r = subprocess.run(cmd, shell=True, cwd=tmp_path, capture_output=True, text=True)
    assert (r.returncode, r.stderr) == (0, "")


def test_allowed_tools_never_exceed_the_reviewed_baseline():
    base = BASELINE["allowed_tools"]
    now = {name: sorted(fm.get("allowed-tools") or []) for name, fm in _all().items()}
    new_skills = sorted(set(now) - set(base))
    assert not new_skills, f"新 skill 未登记能力基线: {new_skills}（在 tests/fixtures/skill_capabilities_baseline.json 登记并审查）"
    grew = {n: sorted(set(now[n]) - set(base[n])) for n in now if set(now[n]) - set(base.get(n, []))}
    assert not grew, (f"这些 skill 的 allowed-tools 比审查基线多出工具: {grew}。"
                      "先改基线文件并写明理由（人审），再改 skill。")
