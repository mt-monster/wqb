# -*- coding: utf-8 -*-
"""稳定论文通道 + EVID-PAPER 多样证硬闸守护（2026-11-19 用户明令）。

锁定三条契约：
  1) 论文检索唯一稳定实现 = tools/research/paper_search.py（Crossref→arXiv→本地库三层冗余），
     相关性校验防假阳性，弃用 WebSearch/WebFetch/Semantic Scholar。
  2) verify_diverse 多样证：≥5 篇不同论文 ∧ ≥3 不同第一作者（DOI/标题去重）。
  3) EVID-PAPER 闸（_gate_knowledge.py）：无 cite 留痕/孤证一律 fail-closed；
     活跃 saved workflow 的论文检索 ask 不得再出现 WebSearch。
"""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]


def _load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


ps = _load("wqb_paper_search", REPO_ROOT / "tools" / "research" / "paper_search.py")


def test_relevance_rejects_unrelated_papers():
    """Crossref 对任意查询都返回最接近结果——无关标题必须被 _relevance 拒绝。"""
    unrelated = [{"title": "ZZZ; Zzz", "authors": [], "doi": "10.fake/zzz", "year": "2020"}]
    assert ps._relevance("nonexistent xyz qqqwww", unrelated) == []


def test_relevance_accepts_mechanism_match():
    papers = [{"title": "Short Selling, Divergence of Opinion and Volatility",
               "authors": ["A Author"], "doi": "10.fake/1", "year": "2018"}]
    got = ps._relevance("divergence of opinion short selling", papers)
    assert len(got) == 1


def test_identity_dedup_by_doi():
    a = {"title": "Some Paper", "doi": "10.x/1"}
    b = {"title": "Some Paper (revised)", "doi": "10.x/1"}
    assert ps._identity(a) == ps._identity(b)


def test_first_author_extraction():
    assert ps._first_author({"authors": ["Miller, Edward"]}) == "miller"
    assert ps._first_author({"authors": ["Edward Miller"]}) == "miller"


def test_verify_diverse_uses_local_corpus_no_network(monkeypatch):
    """用 local 层验证多样证判定逻辑（不依赖网络）。"""
    fake = {
        "found": True, "papers": [
            {"title": "divergence of opinion A", "authors": ["Miller, E"], "doi": "1"},
            {"title": "divergence of opinion B", "authors": ["Fama, E"], "doi": "2"},
        ],
        "layers_tried": [], "errors": [],
    }
    monkeypatch.setattr(ps, "search_papers", lambda *a, **k: fake)
    r = ps.verify_diverse(["q1", "q2", "q3"], min_papers=2, min_authors=2, layers="local")
    assert r["diverse_ok"] is True
    assert r["n_papers"] == 2 and r["n_authors"] == 2


def test_verify_diverse_fails_single_author(monkeypatch):
    fake = {
        "found": True, "papers": [
            {"title": "divergence A", "authors": ["Miller, E"], "doi": "1"},
            {"title": "divergence B", "authors": ["Miller, E"], "doi": "2"},
        ],
        "layers_tried": [], "errors": [],
    }
    monkeypatch.setattr(ps, "search_papers", lambda *a, **k: fake)
    r = ps.verify_diverse(["q1"], min_papers=5, min_authors=3, layers="local")
    assert r["diverse_ok"] is False


def test_active_workflows_no_websearch_for_papers():
    """活跃 saved workflow 的论文检索不得再出现 WebSearch（稳定通道唯一）。"""
    wf_dir = REPO_ROOT / ".zcode" / "workflows"
    for wf in wf_dir.glob("*.dwf.ts"):
        text = wf.read_text(encoding="utf-8")
        if "paper_search.py" in text:
            assert "论文用 WebSearch" not in text, f"{wf.name} 仍用 WebSearch 查论文"
            assert "论文走 WebSearch" not in text, f"{wf.name} 仍用 WebSearch 查论文"


def test_no_active_code_uses_websearch_as_paper_channel():
    """活跃 skill/工具代码不得把 WebSearch 写成论文检索通道（边界声明除外）。"""
    for rel in ["Claude/skills/wq-brain-ra-kor/SKILL.md",
                "Claude/skills/wq-brain-ra-pipeline/references/_six-step-core.md"]:
        text = (REPO_ROOT / rel).read_text(encoding="utf-8")
        assert "paper_search.py" in text
        # 允许"已弃用"的说明句，但不允许工具表里仍列 WebSearch 为可用通道
        assert "| 补充单点事实 | `WebSearch" not in text
