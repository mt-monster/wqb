# -*- coding: utf-8 -*-
"""brain-how-to-pass-alpha-test 文档守护（skills 审查 HP-02 / HP-03 / HP-04 / HP-05 / HP-09 / HP-11 / HP-18 / HP-19）。

  · SKILL §0 的检查名表必须覆盖 `wqb.config.RA_CHECK_NAMES` 全部 18 项（加一项检查而文档没跟上就红）；
  · 表里写的 config 键必须真实存在（数字只在 config，正文不手抄）；
  · 数值例与公式对得上；
  · 不再有「靠 POST submit 读配额」「Redis 不可用所以等死」「15s 轮询」「幽灵算子 / 中缀加权示例」。
"""
import math
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SK = ROOT / "Claude" / "skills" / "brain-how-to-pass-alpha-test"
sys.path.insert(0, str(ROOT / "src"))

from wqb import config  # noqa: E402


def _t(p: Path) -> str:
    return p.read_text(encoding="utf-8")


def test_check_table_covers_every_ra_check_name():
    skill = _t(SK / "SKILL.md")
    section = skill.split("## 0. 检查名 → 线 → 读哪节", 1)[1].split("## 失败点 → 修法族", 1)[0]
    missing = [n for n in sorted(config.RA_CHECK_NAMES) if f"`{n}`" not in section]
    assert not missing, f"§0 检查名表漏了 RA_CHECK_NAMES：{missing}"
    for corr in ("SELF_CORRELATION", "PROD_CORRELATION"):
        assert corr in section


def test_config_keys_named_in_the_table_exist():
    skill = _t(SK / "SKILL.md")
    for obj_name, key in re.findall(r"`(PLATFORM_CHECK_LINES|GATES_INTERNAL|GATES_PLATFORM)\['([a-z0-9_]+)'\]`", skill):
        assert key in getattr(config, obj_name), f"{obj_name}['{key}'] 在 wqb.config 里不存在"


def _fitness(sharpe, returns, turnover):
    return sharpe * math.sqrt(abs(returns) / max(turnover, 0.125))


def test_numeric_examples_match_the_formula():
    skill = _t(SK / "SKILL.md")
    assert round(_fitness(1.6, 0.06, 0.08), 2) == round(_fitness(1.6, 0.06, 0.125), 2) == 1.11
    assert round(_fitness(1.6, 0.06, 0.40), 2) == 0.62 and round(_fitness(1.6, 0.06, 0.25), 2) == 0.78
    for shown in ("≈ **1.11**", "≈ **0.62**", "≈ **0.78**"):
        assert shown in skill
    assert round(1.6 * 0.75 * math.sqrt(1000 / 3000), 2) == 0.69 and "≥ **0.69**" in skill
    assert 1.9 / 1.6 >= 1.10 > 1.7 / 1.6                       # §6a 的两个 Sharpe 高 10% 例
    scen = _t(SK / "references" / "scenarios.md")
    assert "≈ 0.62" in scen and "≈ 0.78" in scen and "≈ 1.11" in scen


def test_boundary_says_read_only_and_does_not_execute_dead_end_writeback():
    skill = _t(SK / "SKILL.md")
    boundary = skill.split("## 职责边界", 1)[1].split("\n## ", 1)[0]
    assert "只读" in boundary and "不执行" in boundary and "seal_dead_end" in boundary
    assert "mode-b-qualification.md" in skill and "mode_b_qualify.py" in skill
    assert "未达标 → 判死" not in skill


def test_no_quota_via_submit_and_no_stale_environment_claims():
    blob = _t(SK / "SKILL.md") + _t(SK / "reference.md")
    assert "get_submission_quota" not in blob
    assert "从 submit 响应" not in blob
    for stale in ("依赖 Redis（本环境不可用）", "15s 间隔", "易「等死」"):
        assert stale not in blob, f"how-to-pass 里还有过期的 check_correlation 环境说法：{stale}"
    assert "prod-corr-avoidance.md" in _t(SK / "SKILL.md")                 # 环境事实只写那一处
    ra = _t(ROOT / "Claude" / "skills" / "wq-brain-ra-pipeline" / "references" / "prod-corr-avoidance.md")
    for fact in ("仅在有 Redis 时", "retry_after", "至多 1 次", "5 分钟"):
        assert fact in ra


def test_reference_no_longer_carries_idea_layer_or_unsafe_examples():
    ref = _t(SK / "reference.md")
    for stale in ("scale_down", "ts_median(", "oth455", "Multi-Smoothing Ranking Signal", "102 operators",
                  "low turnover < 250%", "TOP3000 (USA, D1)"):
        assert stale not in ref, f"reference.md 里还留着：{stale}"
    assert "confirm_submit=False" in ref and "irreversible" in ref
    # 权重相加示例只允许作为「被 gate 5 拦下的反例」出现
    assert "ts_decay_linear(signal,5)*rank(volume*close)" not in ref


def test_concentrated_weight_evidence_page_flags_scope_and_forbidden_forms():
    page = _t(SK / "references" / "concentrated-weight-evidence.md")
    assert "n = 4" in page and "IND / TOP500" in page and "不在标准窗口白名单" in page
    assert page.count("已被闸 5 禁止") >= 3 and "可复制的合规式样" in page
    skill = _t(SK / "SKILL.md")
    assert "add(0.6*rank" not in skill                                    # 正文不再带可复制的加权混合表达式


def test_playbook_scope_is_region_family_and_window_notes_present():
    pb = _t(SK / "references" / "two-year-sharpe-playbook.md")
    assert "(region, family)" in pb and "seal_dead_end" in pb and "forum_recon" in pb
    assert "〔白名单取" in pb and "known_ops" in pb
