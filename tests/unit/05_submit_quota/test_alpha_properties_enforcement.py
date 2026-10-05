# -*- coding: utf-8 -*-
"""守护提交属性的规范落地（2026-10-05 建立）。

背景：2026-10-05 盘点 alpha 提交属性（color/tags/name）时发现 4 类问题，
其中 3 类属「文档/注释写了但代码不执行」，改完若无守护必然漂回：

| 项 | 问题 | 本文件守护 |
|---|---|---|
| P0-1 | `build_name` 在 REGULAR 链路**零调用** → name 完全自由填写 | `_derive_name` 行为 |
| P0-2 | MCP `set_alpha_properties` docstring 教「tags 必须含 `PowerPoolSelected`」| docstring 不含该指令 |
| P1-3 | `check_tags` 除审计 CLI 外零调用 → 告警是死代码 | 节点确实调用它 |
| P2-4 | `CORR_*` 中间地带静默不打 tag | `CORR_MID` 存在且各档不重叠 |
| P2-5 | `PowerPoolSelected` 子串 vs 精确判定两套口径 | 精确判定 |

⚠ P0-2 / P1-3 守护的是**文本与接线**，看似脆弱—— 但它们本来就是
「注释/docstring 级约定」，没有代码约束就会退。P0-1/P2-4/P2-5 则是行为断言。
"""
import ast
import importlib
import inspect
import re
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[3]
SRC = REPO_ROOT / "src"
MCP_TOOLS = REPO_ROOT / "world-quant-brain-mcp" / "tools_alpha.py"
NODE = REPO_ROOT / "src" / "wqb" / "workflow" / "nodes" / "submit_alpha.py"
JUDGE = (REPO_ROOT / "Claude" / "skills" / "brain-alpha-judge" / "scripts" / "judge_alpha.py")


@pytest.fixture(scope="module")
def ap():
    if str(SRC) not in sys.path:
        sys.path.insert(0, str(SRC))
    return importlib.import_module("wqb.alpha_properties")


# ---------------------------------------------------------------- P0-1 name

@pytest.fixture(scope="module")
def derive_name():
    if str(SRC) not in sys.path:
        sys.path.insert(0, str(SRC))
    node = importlib.import_module("wqb.workflow.nodes.submit_alpha")
    return node._derive_name


_DETAILS_KOR = {"settings": {"region": "KOR"}}


def test_name_is_generated_when_not_given(derive_name):
    """name=None 时按 build_name 规范生成（这是 P0-1 的核心）。"""
    out = derive_name(None, _DETAILS_KOR, dataset="pv", wave="113",
                      expr_family="insgate", channel=None)
    assert out["derived"] is True
    assert re.fullmatch(r"KOR_R_insgate_\d{2}", out["name"]), out["name"]


def test_explicit_name_wins(derive_name):
    """显式传入的 name 优先，不被推导覆盖。"""
    out = derive_name("MY_NAME", _DETAILS_KOR, dataset="pv", wave="113",
                      expr_family="f", channel=None)
    assert out["name"] == "MY_NAME"
    assert out["derived"] is False


def test_name_not_guessed_when_region_unknown(derive_name):
    """**宁缺勿编**：region 取不到就不生成，不瞎编区域码。"""
    out = derive_name(None, {}, dataset="pv", wave="113", expr_family="f", channel=None)
    assert out["name"] is None
    assert out["derived"] is False
    assert "region" in out["note"]


def test_seq_always_two_digits_and_in_range(derive_name):
    """seq 必须 1..99（build_name 硬校验），且总是两位补零。"""
    for wave, lo, hi in [("113", 1, 99), ("5", 1, 99), ("9999", 1, 99), (None, 1, 1)]:
        out = derive_name(None, _DETAILS_KOR, dataset="ds", wave=wave,
                          expr_family="f", channel=None)
        seq = int(out["name"].rsplit("_", 1)[1])
        assert lo <= seq <= hi, (wave, seq)


def test_node_calls_build_name_somewhere(ap):
    """源码级：节点必须真的 import/调用 build_name（防注释冒充实现）。"""
    src = NODE.read_text(encoding="utf-8")
    body = "\n".join(l for l in src.splitlines() if not l.strip().startswith("#"))
    assert "build_name" in body
    assert re.search(r"_derive_name\(", body), "定义了却没被 run() 接线"


# ---------------------------------------------------------------- P0-2 docstring

def test_mcp_docstring_no_longer_teaches_ppatag():
    """MCP 工具说明不得再教「tags 至少包含 PowerPoolSelected」。

    该写法会给普通 REGULAR alpha 打上 PPA 通道标签 —— 历史已修过一次
    （submit_alpha 注释记载旧实现 color=GREEN + tags=[PowerPoolSelected]），
    但 docstring 一直没改，Agent 读工具说明就会复现。
    """
    tree = ast.parse(MCP_TOOLS.read_text(encoding="utf-8"))
    doc = "\n".join(
        ast.get_docstring(n) or "" for n in ast.walk(tree)
        if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))
    )
    bad = re.findall(r"tags[^\n]*至少包含[^`\n]*PowerPoolSelected", doc)
    assert not bad, f"MCP docstring 仍在教错误做法: {bad}"
    # 若提到该标签，必须同时给出「普通提交用别的通道」的警示
    if "PowerPoolSelected" in doc:
        assert re.search(r"CH_REG|不要打|专有", doc), (
            "提到 PowerPoolSelected 但未警示它是 PPA 专有、普通提交用 CH_REG")


# ---------------------------------------------------------------- P1-3 check_tags

def test_check_tags_is_called_by_node():
    """check_tags 必须被节点调用，否则规范告警等于死代码。"""
    src = NODE.read_text(encoding="utf-8")
    body = "\n".join(l for l in src.splitlines() if not l.strip().startswith("#"))
    assert "check_tags" in body, "submit_alpha 未调用 check_tags"
    assert "tag_warnings" in body, "告警结果未留痕到步骤输出"


# ---------------------------------------------------------------- P2-4 CORR_MID

def test_corr_bands_do_not_overlap_and_cover_middle(ap):
    """四档互斥且覆盖全区间：超红线无 tag（不可提交态）。"""
    got = {
        "low": ap._corr_tag(0.30, 0.40),
        "mid": ap._corr_tag(0.60, 0.62),
        "near": ap._corr_tag(0.66, 0.30),
        "redline": ap._corr_tag(0.75, 0.30),
    }
    assert got["low"] == ap.CORR_LOW
    assert got["mid"] == ap.CORR_MID, "中间地带又变回静默无 tag"
    assert got["near"] == ap.CORR_NEAR
    assert got["redline"] is None, "超红线不应出现在提交标签里"


def test_corr_none_when_never_measured(ap):
    """未测相关性 → 不打任何 CORR_（与「测了但中等」区分开）。"""
    assert ap._corr_tag(None, None) is None


# ---------------------------------------------------------------- P2-5 PPA 判定

def test_ppa_tag_is_exact_member_not_substring(ap):
    """精确成员判定：子串会让 `PowerPoolSelected_old` 之类误判为 PPA。"""
    assert ap.has_ppa_tag(["PowerPoolSelected"]) is True
    assert ap.has_ppa_tag(["PowerPoolSelected_old"]) is False
    assert ap.has_ppa_tag(["my_PowerPoolSelected"]) is False
    assert ap.has_ppa_tag(["CH_REG"]) is False
    assert ap.has_ppa_tag(None) is False


def test_judge_uses_exact_membership():
    """judge_alpha._is_ppa 必须用精确成员判定（与 check_tags 同口径）。"""
    src = JUDGE.read_text(encoding="utf-8")
    body = "\n".join(l for l in src.splitlines() if not l.strip().startswith("#"))
    assert re.search(r'"PowerPoolSelected"\s+in\s+tags', body), (
        "judge_alpha 仍用子串判定，与 alpha_properties.check_tags 口径不一致")