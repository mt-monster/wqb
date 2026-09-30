# -*- coding: utf-8 -*-
"""RA 核心 SKILL.md 的「每步固定模板」机检（skills 审查 RA-10 / D.3.1）。

旧版声称「每步含 目的 / MCP 调用 / 产物 / 失败分支」，实际步 7 无「目的 / 产物」、失败分支夹在段中、完成定义散落各处。
现在每一步（步 1–9）必须逐项具备：目的 / 前置 / 调用 / 产物 / 完成定义 / 失败分支 / 不做 / 细则；
步 5b 是「定义只在一处」的小节（目的 / 调用 / 产物 / 处置 / 不做）。步内引用的 references 文件必须真实存在。
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
RA = ROOT / "Claude" / "skills" / "wq-brain-ra-pipeline"
SKILL = RA / "SKILL.md"

FULL = ("目的", "前置", "调用", "产物", "完成定义", "失败分支", "不做", "细则")
STEP_5B = ("目的", "调用", "产物", "处置", "不做")


def _sections():
    text = SKILL.read_text(encoding="utf-8")
    parts = re.split(r"(?m)^### (步 [0-9]+b?[^\n]*)\n", text)
    # parts = [preamble, title1, body1, title2, body2, ...]
    return {parts[i].split("（")[0].split("：")[0].strip(): parts[i + 1] for i in range(1, len(parts) - 1, 2)}


def test_all_nine_steps_and_5b_exist_in_order():
    text = SKILL.read_text(encoding="utf-8")
    heads = re.findall(r"(?m)^### (步 [0-9]+b?)", text)
    assert heads == ["步 1", "步 2", "步 3", "步 4", "步 5", "步 5b", "步 6", "步 7", "步 8", "步 9"], heads


def test_every_step_follows_the_fixed_template():
    secs = _sections()
    missing = []
    for name, body in secs.items():
        need = STEP_5B if name == "步 5b" else FULL
        for label in need:
            if not re.search(rf"(?m)^- \*\*{label}\*\*", body):
                missing.append(f"{name} 缺「{label}」")
    assert not missing, "核心 SKILL.md 有步骤不符合固定模板：\n  " + "\n  ".join(missing)


def test_step_local_links_resolve():
    text = SKILL.read_text(encoding="utf-8")
    bad = []
    for m in re.finditer(r"\]\((references/[^)#\s]+|\.\./[^)#\s]+)\)", text):
        tgt = m.group(1)
        if not (SKILL.parent / tgt).resolve().exists():
            bad.append(tgt)
    assert not bad, f"核心 SKILL.md 里失效的相对链接：{sorted(set(bad))}"


def test_core_skill_stays_a_core_file():
    """核心文件只留规则与骨架；细则下沉 references/（旧版 950 行、最长表格单元 ≈2000 字）。"""
    lines = SKILL.read_text(encoding="utf-8").splitlines()
    assert len(lines) <= 300, f"核心 SKILL.md 已 {len(lines)} 行——把细则下沉到 references/"
    longest = max(len(ln) for ln in lines)
    assert longest <= 900, f"核心 SKILL.md 出现 {longest} 字符的超长行——拆成小节或下沉 references/"
