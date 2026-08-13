"""thresholds 单一事实源单元测试 (shared_libs/thresholds.py).

覆盖: 区域×delay Sharpe/Fitness 门槛、PPA 资格边界、Turnover 三层口径、
配额常量、平台体检门槛、异步检查名集合。
"""
import sys
from pathlib import Path

import pytest

SKILLS_LIBS = Path.home() / ".zcode" / "skills" / "shared_libs"
if str(SKILLS_LIBS) not in sys.path:
    sys.path.insert(0, str(SKILLS_LIBS))

pytestmark = pytest.mark.skipif(
    not (SKILLS_LIBS / "thresholds.py").exists(),
    reason="shared_libs/thresholds.py 不存在 (skills 未注册)",
)

import thresholds as t  # noqa: E402


# ---------------------------------------------------------------------------
# 区域 × delay 门槛
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("region,expected", [
    ("EUR", 1.58), ("KOR", 1.58), ("GBR", 1.58), ("DEU", 1.58),
    ("IND", 1.58), ("MEA", 1.58), ("ASI", 1.58), ("GLB", 1.58), ("USA", 1.58),
    ("CHN", 2.07), ("HKG", 1.58), ("JPN", 1.58),
])
def test_sharpe_min_d1(region, expected):
    assert t.sharpe_min(region, 1) == expected


def test_sharpe_min_gbr_d0_override():
    assert t.sharpe_min("GBR", 0) == 2.69


def test_sharpe_min_d0_official_default():
    assert t.sharpe_min("USA", 0) == 2.0  # D0 官方门槛 2.0


def test_fitness_min_defaults():
    assert t.fitness_min("EUR", 1) == 1.0
    assert t.fitness_min("USA", 0) == 1.3   # D0 官方 1.3
    assert t.fitness_min("GBR", 0) == 1.5   # GBR D0 override


# ---------------------------------------------------------------------------
# 通用硬门槛
# ---------------------------------------------------------------------------

def test_2y_sharpe_strict():
    assert t.SHARPE_2Y_MIN == 1.58  # 严格大于, 1.58 恰好 FAIL (GBR 战役实测)


def test_turnover_three_tiers():
    assert t.TURNOVER_PLATFORM_MIN == 0.01 and t.TURNOVER_PLATFORM_MAX == 0.70
    assert t.TURNOVER_LOCAL_MIN == 0.04 and t.TURNOVER_LOCAL_MAX == 0.40
    assert t.TURNOVER_CHEAP_GATE == (0.05, 0.20)
    # 口径分层: 平台窗口 ⊃ 本地预检 ⊃ 战役闸
    assert t.TURNOVER_PLATFORM_MIN < t.TURNOVER_LOCAL_MIN < t.TURNOVER_CHEAP_GATE[0]
    assert t.TURNOVER_CHEAP_GATE[1] < t.TURNOVER_LOCAL_MAX < t.TURNOVER_PLATFORM_MAX


def test_corr_limits():
    assert t.SELF_CORR_MAX == 0.70
    assert t.PROD_CORR_MAX == 0.70
    assert t.PPA_SELF_CORR_MAX == 0.50  # PPA 官方更严


def test_margin_is_local_heuristic():
    assert t.MARGIN_FLOOR_BP == 8.0
    assert t.MARGIN_RECOMMEND_USA_BP == 5.0
    assert t.MARGIN_RECOMMEND_BP == 15.0


# ---------------------------------------------------------------------------
# PPA 资格
# ---------------------------------------------------------------------------

def test_ppa_eligible_boundary():
    ok, msg = t.is_ppa_eligible(8, 3)
    assert ok
    assert "OK" in msg


def test_ppa_ineligible_ops():
    ok, msg = t.is_ppa_eligible(9, 3)
    assert not ok
    assert "9 > 8" in msg


def test_ppa_ineligible_fields():
    ok, _ = t.is_ppa_eligible(8, 4)
    assert not ok


# ---------------------------------------------------------------------------
# 配额 / 体检门槛 / 异步检查
# ---------------------------------------------------------------------------

def test_quota_constants():
    q = t.QUOTA["regular_submission"]
    assert q["limit"] == 4
    assert q["window_hours"] == 48
    assert q["shared"] is True  # RA 与 PPA 共享池


def test_dataset_gate():
    g = t.DATASET_GATE
    assert g["coverage_min"] == 0.85
    assert g["alpha_count_max"] == 50
    assert g["field_count_min"] == 10


def test_async_check_names():
    assert {"SELF_CORRELATION", "PROD_CORRELATION", "REGULAR_SUBMISSION",
            "D0_SUBMISSION"} <= t.ASYNC_CHECK_NAMES


def test_submit_semantics_reliable_signal():
    assert "ACTIVE" in t.SUBMIT_SEMANTICS["reliable_signal"]


def test_region_gate_table_smoke():
    table = t.region_gate_table()
    assert "EUR" in table and "CHN" in table and "GBR" in table
