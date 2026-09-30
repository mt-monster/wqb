# -*- coding: utf-8 -*-
"""跨 skill 的「全库扫描」守护（skills 审查 T0-10 / T0-12 / T0-20 / X-3 / X-16 / P0-1 / P0-2）。

这些问题此前是「逐个 skill 修一遍、下次又长回来」：幽灵算子、平台没有的 `ts_event_*`、加权拼腿配方仍出现在 SOP / 参考文档里。
这里把「只许以警告 / 反例 / 历史的口吻出现」写成机检：命中词旁边必须有否定 / 警示标记，否则视为在**教**它。
"""
import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
SKILLS = ROOT / "Claude" / "skills"

#: 命中词所在行（或紧邻的前 3 行）里，出现任一即视为「以警示口吻提到」
WARN = re.compile(
    r"幽灵|不存在|没有|无\s*`|平台无|不在|不要|勿|禁|拦|反例|不得|不可|已被|历史|旧文|旧配方|旧口径|更正|已删|已废|废止|替代|替换|不是 BRAIN|"
    r"FAIL|ERROR|CANCEL|counterexample|lint:counterexample|deprecated|❌|⚠|\bghost\b|GHOST|known_ops|复核|先.*探针|未核验|未列入|不再有效|路线 A",
    re.I)


def _md_files():
    files = [p for p in SKILLS.rglob("*.md") if "brain-alpha-judge/data/forum_corpus" not in p.as_posix()
             and "trailSomeAlphas/skills/" not in p.as_posix() and p.name != "CHANGELOG.md"]
    files += [p for p in (ROOT / "docs" / "reference").glob("*.md")]
    files += [ROOT / "AGENTS.md", ROOT / "README.md"]
    return files


def _context(lines, i):
    """命中行的语境：紧邻前 3 行；若在表格里，再加上表头（表格前一行 + 表头两行）——表头常写「不可用 / 幽灵 / 替换」。"""
    ctx = lines[max(0, i - 3):i + 1]
    if lines[i].lstrip().startswith("|"):
        j = i
        while j > 0 and lines[j - 1].lstrip().startswith("|"):
            j -= 1
        ctx = lines[max(0, j - 2):j + 2] + ctx
    return " ".join(ctx)


def _hits(pattern: "re.Pattern[str]"):
    for f in _md_files():
        lines = f.read_text(encoding="utf-8").splitlines()
        for i, line in enumerate(lines):
            if pattern.search(line):
                yield f, i, _context(lines, i)


def test_no_doc_recommends_ts_event_operators():
    """平台没有 `ts_event_*` 系列（KOR wave16 实测 8/8 ERROR；闸 8 引用 EVENT 字段即 FAIL）。"""
    bad = [f"{f.relative_to(ROOT)}:{i + 1}" for f, i, ctx in _hits(re.compile(r"ts_event_")) if not WARN.search(ctx)]
    assert not bad, f"这些行在推荐 ts_event_*（平台没有）：{bad}"


@pytest.mark.parametrize("op", ["ts_median", "scale_down", "vec_mean", "is_placeholder"])
def test_ghost_and_unknown_operators_only_appear_as_warnings(op):
    bad = [f"{f.relative_to(ROOT)}:{i + 1}" for f, i, ctx in _hits(re.compile(rf"\b{op}\b")) if not WARN.search(ctx)]
    assert not bad, f"{op} 不在平台算子目录 / 是幽灵算子，只许以警示口吻出现；这些行在当正常算子用：{bad}"


#: 加权 / 等权拼腿的表面写法（与 gate.py 闸 5 的 regex 同源思路）
WEIGHTED = re.compile(
    r"add\(\s*multiply\(|multiply\(\s*(?:rank|ts_|zscore|group_)[^,()]*(?:\([^()]*\))?[^,()]*,\s*0?\.\d+\s*\)|"
    r"\b0?\.\d+\s*\*\s*(?:rank|ts_|zscore|group_|scale)\w*\(|"
    r"(?:rank|ts_[a-z_]+|zscore|group_[a-z_]+)\([^()]*(?:\([^()]*\))?[^()]*\)\s*\*\s*0?\.\d+")
BANNER = "现行政策提示（2026-09-29）"


def test_weighted_leg_mixes_only_appear_as_counterexamples_or_under_the_policy_banner():
    bad = []
    for f in _md_files():
        text = f.read_text(encoding="utf-8")
        under_banner = BANNER in text
        lines = text.splitlines()
        for i, line in enumerate(lines):
            if WEIGHTED.search(line) and not under_banner:
                if not WARN.search(_context(lines, i)):
                    bad.append(f"{f.relative_to(ROOT)}:{i + 1}")
    assert not bad, (
        "这些行在教加权 / 等权拼腿（政策：自 2026-09-13 起被路线 A 与闸 5 禁止）。改写成条件 / 分组 / 残差三式，"
        f"或标 <!-- lint:counterexample -->；纯历史资料文件在文件头加「{BANNER}」横幅：{bad}")


def test_the_historical_reference_docs_that_contain_weighted_mixes_carry_the_policy_banner():
    for name in ("combination_optimization_strategy", "economic_alpha_template_library", "multidim_ab_test_report_template",
                 "101_formulaic_alphas_kb"):
        text = (ROOT / "docs" / "reference" / f"{name}.md").read_text(encoding="utf-8")
        head = "\n".join(text.splitlines()[:6])
        assert BANNER in head and "structural-interaction-forms.md" in head, name


def test_the_gbr_profile_no_longer_recommends_the_weighted_slow_fast_recipe_as_a_win():
    t = (SKILLS / "wq-brain-ra-pipeline" / "references" / "regions" / "GBR.md").read_text(encoding="utf-8")
    assert "禁**加权 / 等权相加" in t or "禁加权" in t or "禁**加权" in t
    win = [ln for ln in t.splitlines() if "T-KB-01" in ln]
    assert win and all(("禁" in ln or "已被闸 5 禁止" in ln or "不加权" in ln) for ln in win), win
    cfg = (ROOT / "src" / "wqb" / "config.py").read_text(encoding="utf-8")
    assert '"_slow_fast_mix_status": "deprecated_20260913_route_a"' in cfg


IRREVERSIBLE_OK = re.compile(r"用户|确认|仅|不可逆|不入链|拒绝|禁止|不要|默认|词表|放行|不是|irreversible|explicit|Never|False", re.I)


def test_confirm_submit_true_is_only_ever_written_next_to_the_user_confirmation_gate():
    """T0-3 / X-9：提交示例默认必须是预检形态；`confirm_submit=True` 只许和「用户确认 / 不可逆 / 禁止」同行出现。"""
    bad = []
    for f in _md_files():
        for i, line in enumerate(f.read_text(encoding="utf-8").splitlines()):
            if re.search(r"confirm_submit\s*=\s*True", line) and not IRREVERSIBLE_OK.search(line):
                bad.append(f"{f.relative_to(ROOT)}:{i + 1}")
    assert not bad, f"这些行写了 confirm_submit=True 却没有提到用户确认 / 不可逆：{bad}"


PROBE = re.compile(r"POST[^\n]{0,30}submit[^\n]{0,60}(零成本|探针|探测|预检|试探|probe)|(零成本|探针|探测|预检|试探)[^\n]{0,40}POST[^\n]{0,30}submit", re.I)
PROBE_OK = re.compile(r"禁止|禁用|不要|勿|反例|不得|没有零成本|无零成本|通过即|真提交|不可逆|不能|不靠|不是|用户确认|确认后")


def test_post_submit_is_never_taught_as_a_zero_cost_probe():
    """T0-2：平台把 POST /submit 同时当「提交」和「提交前检查」，全过就是一次真提交——它不是探针。"""
    bad = []
    for f in _md_files():
        lines = f.read_text(encoding="utf-8").splitlines()
        for i, line in enumerate(lines):
            if PROBE.search(line) and not PROBE_OK.search(" ".join(lines[max(0, i - 1):i + 1])):
                bad.append(f"{f.relative_to(ROOT)}:{i + 1}")
    assert not bad, f"这些行把 POST /submit 当成探针在教：{bad}"


def test_no_skill_document_mixes_powershell_and_bash_fenced_blocks():
    """X-14：同一份文档里 PowerShell 与 bash 混用（SB-24 / TK-16 / JD-13 / BM-14）——读者在哪种 shell 里都会有一半命令跑不通。
    全库整体统一 shell 被否决（DEC-63：31 个 PowerShell 块 / 32 个 bash 块 是各 skill 的既有取向，且命令都经 `$WQ_PY`），
    但**一个文件内只用一种方言**必须成立。"""
    fence = re.compile(r"^```(\w+)", re.M)
    bad = []
    for f in _md_files():
        if SKILLS not in f.parents:
            continue
        langs = {m.group(1).lower() for m in fence.finditer(f.read_text(encoding="utf-8", errors="ignore"))}
        if langs & {"powershell", "pwsh", "ps1"} and langs & {"bash", "sh", "shell"}:
            bad.append(str(f.relative_to(ROOT)))
    assert not bad, f"这些文档同时含 PowerShell 与 bash 命令块，改成同一种方言：{bad}"
