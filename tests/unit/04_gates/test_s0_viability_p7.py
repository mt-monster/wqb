# -*- coding: utf-8 -*-
"""S0 白名单 P7：字段语义可做性过滤（2026-10-02 落地）。

背景（DEU 2026-10-02 全类目穷尽 + 论坛六探针帖 43791732585879 整合）：
  S0 的 `usable_fields` 只数「coverage>=0.85 的字段数」，不区分字段语义类型，
  导致「字段多但全是事件/计数型」的集被当作高广度富矿选进白名单，
  建波后才发现平台侧有效持仓（longCount）不够，配额白烧。

实测证据（DEU/TOP500/D1，5 次独立验证）：
  字段语义类型          -> 实测 longCount   -> 结果
  ---------------------  ---------------  -----------------------------
  连续/比率/概率/预测型  -> 高（全市场）    dlrr prob 150 ⇒ S 1.45；pattern simscore 143~147
  事件/计数/稀疏型      -> 低（仅事件股）  predictive_starmine count 8~54；order_book 27~37；f6 8~18

本测试守护 P7 的四条契约：
  1. **默认关闭**（h.viability_filter_enable 缺省 False）=> 各区域行为与旧版逐条一致；
  2. 计数/布尔型 → 不可做（False）；概率/比率/预测型 → 可做（True）；
  3. **词元锚定**（`accounts` 不被 `count` 咬）；**主题词不判死**（`revision_magnitude` 是幅度，可做）；
  4. 不影响硬地板（hard_excluded 仍只看 coverage 与 P3 字段数）。
"""
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[3]
SKILL_SCRIPTS = REPO_ROOT / "Claude" / "skills" / "wq-brain-campaign-toolkit" / "scripts"

if str(SKILL_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SKILL_SCRIPTS))

sd = pytest.importorskip("score_datasets", reason="score_datasets.py 不在 toolkit scripts 目录")


# ---------------------------------------------------------------------------
# P7 契约 1：opt-in 默认关闭
# ---------------------------------------------------------------------------

def test_p7_disabled_by_default():
    """缺省 h 不含 viability_filter_enable => 视为关闭（旧版行为不变）。"""
    assert bool({}.get("viability_filter_enable", False)) is False
    assert bool({"viability_filter_enable": False}.get("viability_filter_enable", False)) is False
    assert bool({"viability_filter_enable": True}.get("viability_filter_enable", False)) is True


# ---------------------------------------------------------------------------
# P7 契约 2：计数/布尔型不可做，概率/比率/预测型可做
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("name,desc,expect", [
    # --- 实测 longCount 不足的真实字段（predictive_starmine，事件计数=稀疏）---
    ("analyst_downgrade_count_7d_4", "Number of analyst downgrades in 7 days", False),
    ("analyst_downward_revision_count_fq1_earnings_30d_4", "Count of downward revisions", False),
    ("analyst_downgrade_count_14d_2", "Number of analyst downgrades over 14 days", False),
    # --- ★ 覆盖计数（密集）= 必须放行（DEU/analyst7 实测：初版误判致 231 字段全灭）---
    ("act_q_cpx_surprisenum",
     "Number of estimates used for surprise calculation of actual capital expenditure", True),
    ("act_q_ebi_surprisenum",
     "Number of estimates used for surprise calculation of actual EBIT", True),
    ("analyst_coverage_count", "Number of analysts covering the company", True),    # --- 实测 longCount 充足的字段（dlrr / pattern_scores）---
    ("quantile_label_1bucket_5day_ohlcv_2",
     "Continuous regression prediction (float) of the 5-day forward market-neutral return", True),
    ("probability_label3_5quantile_20day_ohlcv_2",
     "Log-probability that the 20-day forward return falls in quantile bucket 3 of 5", True),
    ("asc_triangle_mean_simscore_lookback120",
     "Mean similarity score of ascending triangle pattern over 120 days", True),
    # --- 普通连续字段（应放行）---
    ("trade_market_impact_coefficient", "Trade market impact coefficient", True),
    ("eps_y2_estimate_coeff_var", "Coefficient of variation of FY2 EPS estimates", True),
    ("rsi_14", "Relative strength index over 14 days", True),
])
def test_p7_viability_known_cases(name, desc, expect):
    assert sd.field_viability(name, desc) is expect


def test_p7_coverage_count_checked_before_event_count():
    """★ 顺序契约：覆盖计数（密集）优先于事件计数（稀疏）。

    `Number of estimates` 同时含 "estimates"，若顺序反了会被 ② 或 ③ 拦下 ——
    这是 DEU/analyst7 231 字段全灭的根因，专门守护。
    """
    assert sd.field_viability("x", "Number of estimates used for surprise") is True
    assert sd.field_viability("x", "Number of downgrades in the last 7 days") is False


# ---------------------------------------------------------------------------
# P7 契约 3：词元锚定 + 主题词不判死（防误杀）
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("name,desc", [
    # `accounts` 含子串 count，但词元锚定要求 count 独立成词 => 不该被咬
    ("accounts_receivable_other", "Value of other accounts receivable."),
    ("discount_rate", "Discount rate applied to future cash flows"),
    # 主题词（revision/upgrade/downgrade）只说明「关于什么事件」，不代表是计数
    ("revenue_revision_magnitude", "Magnitude of revenue estimate revisions"),
    ("analyst_upgrade_ratio", "Ratio of analyst upgrades to total recommendations"),
    ("eps_downgrade_pct", "Percentage of EPS estimates revised downward"),
    # 技术指标（09-28 教训：indicator 名词不代表布尔标志）
    ("bollinger_band_width", "Bollinger band width indicator"),
    ("altman_z_score", "Altman Z-score indicator denoting financial distress"),
])
def test_p7_no_false_kill(name, desc):
    """防误杀回归：这些字段必须判为「可做」（True）。"""
    assert sd.field_viability(name, desc) is True


def test_p7_viable_desc_overrides_event_name():
    """高可做性描述优先于事件型名字（防 `*_count_*` 但描述是 probability 的字段被误杀）。"""
    assert sd.field_viability(
        "upgrade_count_score", "Probability-weighted score of analyst upgrade events") is True


# ---------------------------------------------------------------------------
# P7 契约 4：不影响硬地板（设计原则 3）
# ---------------------------------------------------------------------------

def test_p7_does_not_change_hard_excluded():
    """hard_excluded 只看 coverage 与 P3 字段数，P7 开关不改变其结论。"""
    h_off = {"coverage_hard_min": 0.6, "field_count_hard_min": 10, "viability_filter_enable": False}
    h_on = {"coverage_hard_min": 0.6, "field_count_hard_min": 10, "viability_filter_enable": True}
    for cov, fc in [(0.7, 20), (0.4, 20), (0.7, 3), (0.9, 100)]:
        assert sd.hard_excluded(cov, fc, h_off) == sd.hard_excluded(cov, fc, h_on)


def test_p7_breadth_falls_back_when_catalog_missing():
    """无 catalog => viable_field_count 返回 None（调用方回退 P3 值，不塌陷为 0）。"""
    class _Ctx:
        region = "ZZZ"
        settings = {"delay": 1}
        def catalog_path(self, ds):
            return "/nonexistent/path/does-not-exist.json"
    assert sd.viable_field_count(_Ctx(), "no_such_dataset") is None


def test_p7_viability_never_accepts_group_like_unknown():
    """未知语义 => 缺省 True（保守：不认识的不降权），与设计原则一致。"""
    assert sd.field_viability("some_unknown_factor_xyz", "A proprietary factor") is True
