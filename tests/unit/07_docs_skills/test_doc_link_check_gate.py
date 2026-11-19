# -*- coding: utf-8 -*-
"""活文档 markdown 链接死链闸 `tools/code-audit/doc_link_check.py` 的守护用例。

为什么要有这道闸（`doc_path_refs.py` 的真空地带）：
`doc_path_refs.collect()` 里 `if not t or "/" not in t: continue` ⇒ 它只校验**反引号路径**
与**带 `/` 且首段是仓库顶层目录**的写法；**markdown 链接**（`](docs/experience/…md)`）
与**裸文件名**永远不在它的视野里。2026-11-19 审计实测：1794 条 markdown 链接里 3 条两种
口径都解析不到（`AGENTS.md` / `docs/README.md` / `docs/design/…`），此前无人发现。

守四件事：
1. **棘轮有效**：相对基线无新增死链（存量记 `tests/fixtures/doc_link_check_baseline.json`）。
2. **工具已登记**：`tools/README.md` + `tools/THEMES.json` 都有它（§6 / G9 硬闸）。
3. **已接进 pre-commit**：不接线的闸等于没有闸。
4. **工具故障不得伪装成「无违规」**：自身异常 ⇒ 退出码 2（不是 0）。
"""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[3]
TOOL = REPO / "tools" / "code-audit" / "doc_link_check.py"
BASELINE = REPO / "tests" / "fixtures" / "doc_link_check_baseline.json"


def _load():
    spec = importlib.util.spec_from_file_location("doc_link_check_for_test", TOOL)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_tool_exists_and_loads():
    assert TOOL.is_file(), f"闸工具不存在：{TOOL}"
    mod = _load()
    assert callable(mod.scan) and callable(mod.main)


def test_no_new_broken_links_against_baseline():
    """棘轮：相对基线不得有新增死链。"""
    mod = _load()
    broken, n_docs, n_links = mod.scan()
    baseline = set(json.loads(BASELINE.read_text(encoding="utf-8")).get("violations", []))
    new_broken = sorted(set(broken) - baseline)
    assert not new_broken, (
        f"新增 markdown 死链 {len(new_broken)} 条：{new_broken}\n"
        "修法：改成真实路径（相对所在目录，或仓库根相对——skill 里直写 docs/... 亦可）"
        "／恢复丢失文件／归档并写明「已归档」")
    assert n_links > 1000, f"扫描到的链接数异常偏少（{n_links}）——扫描面可能失效"


def test_both_resolution_semantics_are_covered():
    """闸必须同时认两种口径：文件相对（渲染器）与仓库根相对（agent）。

    只认一种 ⇒ 要么把合规的仓库根相对链接全判成死链（误伤），
    要么把真正断链放过（漏拦）。本用例各造一个真实样本验证两种口径都被接受。
    """
    mod = _load()

    # (a) 文件相对：skill 内同树链接（相对链接所在目录可解析）
    a_fp = REPO / "Claude" / "skills" / "wq-brain-ra-pipeline" / "SKILL.md"
    a_tgt = "../worldquant-submit-alpha/references/submit-chain.md"
    assert (a_fp.parent / a_tgt).exists(), "样本前提失效：(a) 文件相对样本不再存在"
    assert mod.resolves(a_fp, a_tgt), "闸未接受文件相对口径"

    # (b) 仓库根相对：skill 里直写 docs/...（相对文件目录不可解析，但相对仓库根可解析）
    b_fp = REPO / "Claude" / "skills" / "brain-alpha-judge" / "SKILL.md"
    b_tgt = "AGENTS.md"
    assert not (b_fp.parent / b_tgt).exists(), "样本前提失效：(b) 该路径不该能按文件目录解析"
    assert (REPO / b_tgt).exists(), "样本前提失效：(b) 仓库根目标不存在"
    assert mod.resolves(b_fp, b_tgt), "闸未接受仓库根相对口径"

    # 反向：两者都不存在 ⇒ 必须判死
    assert not mod.resolves(a_fp, "docs/experience/__不存在的文件__.md"), "闸把死链当活链"


def test_tool_is_registered():
    readme = (REPO / "tools" / "README.md").read_text(encoding="utf-8")
    assert "code-audit/doc_link_check.py" in readme, "tools/README.md 未登记该闸（§6 / G9 硬闸）"
    themes = json.loads((REPO / "tools" / "THEMES.json").read_text(encoding="utf-8"))
    files = themes["themes"]["code-audit"]["files"]
    assert "doc_link_check.py" in files, "tools/THEMES.json 的 code-audit 主题未登记该文件"


def test_pre_commit_wires_the_gate():
    hook = (REPO / "tools" / "git-hooks" / "pre-commit").read_text(encoding="utf-8")
    assert "doc_link_check.py" in hook, "该闸未接进 pre-commit —— 不接线的闸等于没有闸"


def test_tool_fault_is_not_reported_as_clean(monkeypatch, capsys):
    """工具自身异常 ⇒ 退出码 2，绝不能是 0（否则崩溃会被读成「无死链」）。"""
    mod = _load()

    def _boom():
        raise RuntimeError("模拟扫描故障")

    monkeypatch.setattr(mod, "scan", _boom)
    rc = mod.main([])
    assert rc == 2, f"工具故障时退出码应为 2（无法判定），实际 {rc}"


def test_baseline_file_shape():
    data = json.loads(BASELINE.read_text(encoding="utf-8"))
    assert "violations" in data and isinstance(data["violations"], list)
    assert "_doc" in data, "基线须写明棘轮语义与收紧方式"
