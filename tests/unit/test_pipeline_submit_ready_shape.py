# -*- coding: utf-8 -*-
"""submit_ready 台账 list/dict 两种形态都能追加候选（2026-09-19 IND w182 实证崩溃）。"""
import os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(ROOT, "Claude", "skills", "wq-brain-campaign-toolkit", "scripts"))
import pipeline  # noqa: E402


def test_list_shape_passthrough():
    d = {"submit_ready": [{"id": "a"}]}
    sr = pipeline._submit_ready_list(d)
    sr.append({"id": "b"})
    assert [x["id"] for x in d["submit_ready"]] == ["a", "b"]


def test_dict_shape_appends_into_valid():
    d = {"submit_ready": {"valid": [{"id": "x", "status": "ACTIVE"}], "blocked": [], "updated": "2026-09-01"}}
    sr = pipeline._submit_ready_list(d)
    sr.append({"id": "y"})
    assert [x["id"] for x in d["submit_ready"]["valid"]] == ["x", "y"]
    assert d["submit_ready"]["blocked"] == []


def test_dict_without_valid_and_missing_key():
    d = {"submit_ready": {"blocked": []}}
    pipeline._submit_ready_list(d).append({"id": "z"})
    assert d["submit_ready"]["valid"] == [{"id": "z"}]
    e = {}
    pipeline._submit_ready_list(e).append({"id": "w"})
    assert e["submit_ready"] == [{"id": "w"}]
