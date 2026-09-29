# -*- coding: utf-8 -*-
"""planning-with-files 的文档 / 钩子一致性（skills 审查 PW-01…PW-10，2026-09-29）。

  · 钩子永不阻断（Stop 钩子 exit 0，没有 exit 1/2），PreToolUse 不再挂在 Bash 上；
  · 正文逐个钩子写明做什么与成本；
  · 触发口径一个、不再有「没有商量余地」与「永不重复失败」的绝对化说法（暂时性失败按各 skill 协议重试）；
  · 规划文件在仓库根、已被 .gitignore 忽略；WQ 战役示例的 Phase / Status 行与 check-complete 的计数口径一致。
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SK = ROOT / "Claude" / "skills" / "planning-with-files"
SKILL = (SK / "SKILL.md").read_text(encoding="utf-8")


def _frontmatter() -> str:
    return re.match(r"^---\n(.*?)\n---\n", SKILL, re.S).group(1)


def _hook_commands():
    fm = "\n".join(ln for ln in _frontmatter().splitlines() if not ln.lstrip().startswith("#"))
    return re.findall(r'(?m)^\s*command:\s*"((?:[^"\\]|\\.)*)"\s*$', fm)


def test_hooks_never_block_and_pretooluse_skips_bash():
    cmds = _hook_commands()
    assert len(cmds) == 4
    for c in cmds:
        assert not re.search(r"\bexit\s+[12]\b", c), f"钩子不得阻断：{c[:80]}"
        assert "<SKILL_ROOT>" not in c
    stop = [c for c in cmds if "Phase" in c][0]
    assert "exit 0" in stop
    pre = re.search(r"PreToolUse:\s*\n\s*- matcher:\s*\"([^\"]+)\"", _frontmatter()).group(1)
    assert "Bash" not in pre and set(pre.split("|")) == {"Write", "Edit"}


def test_body_documents_every_hook_event_and_its_cost():
    section = SKILL.split("## 钩子（frontmatter `hooks:`）到底做什么", 1)[1].split("\n## ", 1)[0]
    for event in ("SessionStart", "PreToolUse", "PostToolUse", "Stop"):
        assert event in section, f"正文没有说明 {event} 钩子"
    assert "exit 0" in section and "不阻断" in section and "成本" in section


def test_single_trigger_criterion_and_priority_rules():
    head = _frontmatter()
    assert "5 次工具调用" not in head and "Auto-activates" not in head
    assert "用户当次指令 > 领域协议" in SKILL
    assert "没有商量余地" not in SKILL and "绝不开始复杂任务" not in SKILL
    assert "共用运行环境约定" not in SKILL                        # 旧边界声称共用 $WQ_PY，全文并无使用
    for needle in ("确定性失败", "暂时性失败", "429", "PENDING", "失败」的粒度"):
        assert needle in SKILL


def test_planning_files_live_in_repo_root_and_are_gitignored():
    ignore = (ROOT / ".gitignore").read_text(encoding="utf-8").splitlines()
    for f in ("/task_plan.md", "/findings.md", "/progress.md"):
        assert f in ignore, f"{f} 未被 .gitignore 忽略"
    assert "仓库根" in SKILL and "结果的真相源" in SKILL or "真相源是 DB 台账" in SKILL
    assert "不是战役产物" in SKILL


def test_wq_example_matches_the_check_complete_counting_convention():
    text = (SK / "references" / "wq-examples.md").read_text(encoding="utf-8")
    plan = text.split("```markdown", 1)[1].split("```", 1)[0]
    phases = re.findall(r"(?m)^### Phase", plan)
    statuses = re.findall(r"(?m)^- \*\*Status:\*\* (complete|in_progress|pending)$", plan)
    assert len(phases) == 9 == len(statuses)                       # 九步 ↔ 九个阶段，每阶段恰有一行 Status
    assert plan.count("**Status:** complete") == 2 and "未经用户确认不提交" in plan


def test_check_complete_script_is_documented_as_manual_only():
    sh = (SK / "scripts" / "check-complete.sh").read_text(encoding="utf-8")
    assert "Used by Stop hook" not in sh and "Manual check only" in sh
    assert "手动" in SKILL and "不接钩子" in SKILL


def test_version_and_hooks_semantics_are_defined_in_index():
    idx = (ROOT / "Claude" / "skills" / "INDEX.md").read_text(encoding="utf-8")
    assert "上游版本号" in idx and "白名单内的 skill 可声明" in idx
