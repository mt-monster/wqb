# -*- coding: utf-8 -*-
"""回归：set_alpha_properties 只 PATCH 显式给出的字段（2026-09-21）。

事故：GLB gJboYLRl 提交前已用 set_alpha_properties 设好 name/description；
workflow_submit_alpha(confirm_submit=True) 未传 name/descriptions，节点把 None 原样
交给客户端，客户端无条件发 {"name": null, "regular": {"description": null}, "tags": []}
→ 平台把名称/描述清空后才 POST submit。官方 ace_lib.set_alpha_properties 的语义是
"None 不发"，这里对齐并加单测钉死。
"""
from __future__ import annotations

import os
import sys

import pytest

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, os.path.join(REPO, "src"))
sys.path.insert(0, os.path.join(REPO, "world-quant-brain-mcp"))

from brain_mixin_correlation import build_alpha_properties_payload  # noqa: E402
from wqb.workflow.nodes.submit_alpha import _preserved_properties  # noqa: E402


def test_none_fields_are_omitted_not_nulled():
    payload = build_alpha_properties_payload(color="GREEN", tags=["A", "B"])
    assert payload == {"color": "GREEN", "tags": ["A", "B"]}
    assert "name" not in payload
    assert "regular" not in payload


def test_descriptions_sentinel_string_none_is_not_sent():
    # 历史默认值是字符串 "None"（MCP 工具签名遗留），同样不能把描述清空
    payload = build_alpha_properties_payload(name="x", descriptions="None")
    assert payload == {"name": "x"}


def test_explicit_values_are_sent_including_empty_tags():
    payload = build_alpha_properties_payload(
        name="GLB_x_p0665", color="BLUE", tags=[],
        descriptions="Idea: a\n\nRationale for data used: b\n\nRationale for operators used: c",
        selection_description="sel", combo_description="cmb",
    )
    assert payload["name"] == "GLB_x_p0665"
    assert payload["tags"] == []          # 显式空列表 = 显式清空，允许
    assert payload["regular"] == {"description": payload["regular"]["description"]}
    assert payload["regular"]["description"].startswith("Idea:")
    assert payload["selection"] == {"description": "sel"}
    assert payload["combo"] == {"description": "cmb"}


def test_all_none_gives_empty_payload():
    assert build_alpha_properties_payload() == {}


def test_submit_node_reports_preserved_name_and_description():
    details = {"name": "GLB_pvcorr_p0665", "regular": {"description": "Idea: keep me"}}
    kept = _preserved_properties(details, name=None, descriptions=None)
    assert kept == {"name": "GLB_pvcorr_p0665", "description": "Idea: keep me"}
    # 调用方显式给了 name → 不属于"保留"，只报 description
    kept2 = _preserved_properties(details, name="new", descriptions=None)
    assert kept2 == {"description": "Idea: keep me"}
    # 非 dict 输入容错
    assert _preserved_properties(None, name=None, descriptions=None) == {}
