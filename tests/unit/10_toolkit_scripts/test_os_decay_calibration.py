# -*- coding: utf-8 -*-
"""2026-09-20：OS 衰减基线接进步 7 IS 阈值校准。

背景：`os_decay_baseline()` 落库后只被同步脚本打印，无代码消费。
本测试守护接线：review_wave 评审给每行追加 `os_calibration`（预期 OS 水位
+ 存活率），并写进 payload；基线缺失时 fail-open（不阻断评审）。

关键实证（决定了折算语义）：IS sharpe 与 OS sharpe 的 Spearman 秩相关仅 +0.086，
IS 各桶 OS>0 存活率平坦 70-80% —— 故本校准**不抬高 IS 阈值**，只给期望水位。
"""
import importlib
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
SRC = REPO_ROOT / "src"
TOOLKIT_SCRIPTS = REPO_ROOT / "Claude" / "skills" / "wq-brain-campaign-toolkit" / "scripts"

BASELINE = {
    "n": 124, "is_sharpe_mean": 1.5307, "os_sharpe_mean": 0.548,
    "os_is_sharpe_ratio_mean": 0.3578, "above_gate_1_58": 14,
    "above_one": 38, "non_positive": 27, "non_positive_pct": 21.77,
}


def _os_decay():
    if str(SRC) not in sys.path:
        sys.path.insert(0, str(SRC))
    sys.modules.pop("wqb.research.os_decay", None)
    return importlib.import_module("wqb.research.os_decay")


def _review_wave():
    if str(TOOLKIT_SCRIPTS) not in sys.path:
        sys.path.insert(0, str(TOOLKIT_SCRIPTS))
    sys.modules.pop("review_wave", None)
    return importlib.import_module("review_wave")


# ---------------------------------------------------------------------------
# 折算语义
# ---------------------------------------------------------------------------

def test_calibrate_review_multiplies_by_decay_ratio():
    od = _os_decay()
    info = od.calibrate_review({"sharpe": 1.76, "fitness": 1.12}, BASELINE, "USA")
    assert info["decay_ratio"] == 0.3578
    assert info["expected_os_sharpe"] == round(1.76 * 0.3578, 4)
    assert info["expected_os_fitness"] == round(1.12 * 0.3578, 4)
    # 存活率 = 1 - OS<=0 占比
    assert info["survival_rate"] == 0.7823
    assert "0.358" in info["note"] and "USA n=124" in info["basis"]


def test_calibrate_review_carries_rank_correlation_caveat():
    """必须带 caveat：IS/OS 秩相关仅 +0.086，折算值不是排序依据。"""
    od = _os_decay()
    info = od.calibrate_review({"sharpe": 2.0}, BASELINE, "USA")
    assert "0.086" in info["caveat"]
    assert "提高 IS 阈值" in info["caveat"]


def test_calibrate_review_fail_open_without_sample():
    """基线样本不足 → 全部 None + no_sample，不抛异常（评审不被阻断）。"""
    od = _os_decay()
    for bad in (None, {}, {"n": 0}, {"n": 3}):
        info = od.calibrate_review({"sharpe": 1.8}, bad)
        assert info["expected_os_sharpe"] is None
        assert info["basis"] == "no_sample"
        assert "样本不足" in info["note"] or "同步" in info["note"]


def test_calibrate_review_handles_missing_is_metrics():
    """行缺 sharpe/fitness（如 NO_DATA）→ 对应字段 None，不崩。"""
    od = _os_decay()
    info = od.calibrate_review({"sharpe": None, "fitness": None}, BASELINE, "USA")
    assert info["expected_os_sharpe"] is None and info["expected_os_fitness"] is None
    assert info["decay_ratio"] == 0.3578          # 基线信息仍在
    assert info["survival_rate"] == 0.7823


def test_load_baseline_tolerates_store_error():
    """store 抛错 → 返回 n=0 带 error，不向上抛（fail-open）。"""
    od = _os_decay()

    class _Bad:
        def os_decay_baseline(self, region=None):
            raise RuntimeError("db locked")

    b = od.load_baseline(_Bad())
    assert b["n"] == 0 and "db locked" in b["error"]


def test_annotate_rows_in_place():
    od = _os_decay()
    rows = [{"sharpe": 1.6, "fitness": 1.0}, {"sharpe": 2.4, "fitness": 1.8}, {"sharpe": None}]
    out = od.annotate_rows(rows, BASELINE, "USA")
    assert out["annotated"] == 2
    assert rows[0]["os_calibration"]["expected_os_sharpe"] == round(1.6 * 0.3578, 4)
    assert rows[2]["os_calibration"]["expected_os_sharpe"] is None


def test_annotate_rows_single_row_failure_isolated():
    """单行异常不拖垮整批（写入 error 标记后继续）。"""
    od = _os_decay()
    rows = [{"sharpe": 1.6}]
    orig = od.calibrate_review
    calls = {"n": 0}

    def boom(row, base, region=None):
        calls["n"] += 1
        if calls["n"] == 1:
            raise ValueError("x")
        return orig(row, base, region)

    od.calibrate_review = boom
    try:
        od.annotate_rows(rows, BASELINE, "USA")
    finally:
        od.calibrate_review = orig
    assert rows[0]["os_calibration"]["basis"] == "error"


# ---------------------------------------------------------------------------
# review_wave 接线
# ---------------------------------------------------------------------------

def test_review_wave_has_os_baseline_hook():
    rw = _review_wave()
    assert callable(rw._os_baseline)
    assert callable(rw.annotate_os_calibration)


def test_review_wave_annotate_returns_none_on_empty_baseline():
    rw = _review_wave()
    assert rw.annotate_os_calibration([{"sharpe": 1.5}], None, "USA") is None
    assert rw.annotate_os_calibration([{"sharpe": 1.5}], {"n": 0}, "USA") is None


def test_review_wave_annotate_uses_os_decay_module():
    rw = _review_wave()
    rows = [{"sharpe": 1.8, "fitness": 1.2}]
    out = rw.annotate_os_calibration(rows, BASELINE, "USA")
    assert out["annotated"] == 1
    assert rows[0]["os_calibration"]["expected_os_sharpe"] == round(1.8 * 0.3578, 4)
