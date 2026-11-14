# -*- coding: utf-8 -*-
"""守护 2026-11-14 用户明令：48h 内 prod 可信缓存直接提交，不默认 refresh=True。

防止文档/代码口径回退到「提交当刻必须回源」。逻辑实现在
``submit_alpha._prod_gate``（refresh=False + CORR_FRESH_HOURS=48 + provisional 补刷）。
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SKILL = ROOT / "Claude" / "skills" / "worldquant-submit-alpha"
CHAIN = SKILL / "references" / "submit-chain.md"
MAIN = SKILL / "SKILL.md"
GATES = ROOT / "docs" / "experience" / "01_platform_gates.md"
NODE = ROOT / "src" / "wqb" / "workflow" / "nodes" / "submit_alpha.py"


def test_all_authoritative_docs_state_48h_rule():
    for p in (CHAIN, MAIN, GATES, ROOT / "AGENTS.md"):
        assert "48h" in p.read_text(encoding="utf-8"), p
    chain = CHAIN.read_text(encoding="utf-8")
    assert "refresh=False" in chain
    assert "提交当刻必须 `refresh=True`" not in chain
    assert "2026-11-14 用户明令" in MAIN.read_text(encoding="utf-8")


def test_prod_gate_defaults_to_cache_first():
    src = NODE.read_text(encoding="utf-8")
    assert 'os.environ.get("WQB_PROD_GATE_REFRESH")' in src
    assert "refresh=False" in src
    assert "2026-11-14 用户明令" in src
    assert "CORR_FRESH_HOURS" in (ROOT / "src" / "wqb" / "store" / "_corr_cache.py").read_text(
        encoding="utf-8")
