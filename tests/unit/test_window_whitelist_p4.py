# -*- coding: utf-8 -*-
"""回归测试：窗口白名单机械化（2026-09-17 #4）。

## 背景（实测）
SOP 两处（`wq-brain-ra-pipeline` 步 4 / `brain-make-some-gem`）都要求
**"只用标准窗口 1/5/22/66/252/504/1008/1260；其他窗口须给出解释或实测证据"**，
但此前**只写在散文里、零机械守护**。

实测全库 22,024 条表达式里 **23%（4,491 条）**用了非白名单窗口，
Top 恰为 **20(1,402) / 10(1,389) / 120(478) / 60(413)** —— 与
`_lib/operator_coverage.py::_DEFAULT_WINDOWS` 的旧默认值 `[20,60,120,5,10,252]`
**完全吻合**，即**工具默认值就是污染源**。

本文件锁定三件事：
1. 白名单只此一份、两处同源（src/wqb/config.py 与 toolkit config）必须一致；
2. 污染源 `_DEFAULT_WINDOWS` 已对齐白名单；
3. gate 的窗口检查是 **warning 不阻断**（SOP 允许"给出解释后用"）。
"""

import json
import os
import sys

import pytest

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(REPO, "src"))
sys.path.insert(0, os.path.join(REPO, "Claude", "skills",
                                "wq-brain-campaign-toolkit", "scripts"))

TK_CONFIG = os.path.join(REPO, "Claude", "skills", "wq-brain-campaign-toolkit",
                         "config", "platform_constraints.json")
WHITELIST = [1, 5, 22, 66, 252, 504, 1008, 1260]


def _pc():
    return json.load(open(TK_CONFIG, encoding="utf-8"))


# ---- 单一事实源 ------------------------------------------------------------

def test_platform_config_has_whitelist():
    assert _pc().get("window_whitelist") == WHITELIST


def test_config_py_standard_windows_agrees():
    """`src/wqb/config.py::STANDARD_WINDOWS` 必须与 toolkit config 同源一致。"""
    from wqb import config
    assert list(config.STANDARD_WINDOWS) == WHITELIST


def test_pollution_source_is_aligned():
    """`_DEFAULT_WINDOWS` 的每个值都必须在白名单内（它曾是污染源）。"""
    from _lib.operator_coverage import _DEFAULT_WINDOWS  # noqa: E402
    bad = [w for w in _DEFAULT_WINDOWS if w not in WHITELIST]
    assert not bad, f"仍有白名单外的默认窗口 {bad}"


# ---- 提取器 ---------------------------------------------------------------

def test_extracts_trailing_int_args_as_windows():
    sys.path.insert(0, os.path.join(REPO, "Claude", "skills",
                                    "wq-brain-campaign-toolkit", "scripts"))
    import gate
    assert gate.expression_windows("ts_decay_linear(ts_backfill(f, 66), 22)") == [66, 22]
    assert gate.expression_windows("ts_corr(a, b, 20)") == [20]
    assert gate.expression_windows("ts_backfill(f, 120)") == [120]


def test_excludes_named_params_decimals_and_strings():
    sys.path.insert(0, os.path.join(REPO, "Claude", "skills",
                                    "wq-brain-campaign-toolkit", "scripts"))
    import gate
    # `std=4` 是命名参数，不是窗口
    assert gate.expression_windows("winsorize(x, std=4)") == []
    # bucket 的 range 串里没有窗口
    assert gate.expression_windows('bucket(rank(x), range="0,1,0.1")') == []
    # 0.5 是小数不是窗口
    assert gate.expression_windows("quantile(x, 0.5)") == []
    # 平滑系数 0.7 不是窗口
    assert gate.expression_windows("multiply(0.7, rank(x))") == []


def test_range_bounds_exclude_scalars():
    """范围边界：越界数（>2000）不判为窗口。

    ⚠ 已知启发式边界：`add(x, 3)` 的 `3` 在 [2,2000] 内会被判为窗口候选。
    真实语料里裸小整数加法极罕见，且白名单里本就有 1/5，所以这是可接受代价；
    这里锁定的是**实际口径**（含此边界），不是理想口径。
    """
    sys.path.insert(0, os.path.join(REPO, "Claude", "skills",
                                    "wq-brain-campaign-toolkit", "scripts"))
    import gate
    assert gate.expression_windows("add(x, 3)") == [3]      # 锁定实际口径（含边界）
    assert gate.expression_windows("ts_mean(f, 99999)") == []  # 越界 → 不判
    assert 252 in gate.expression_windows("ts_mean(f, 252)")


# ---- gate 集成：warning 不阻断 --------------------------------------------

@pytest.fixture()
def gate_mod():
    import gate
    return gate


def test_warning_emitted_for_off_whitelist_window(gate_mod):
    pc = _pc()
    poison = [p for p in pc.get("poison_patterns", [])
              if p.get("severity", "block") == "block"]
    out = gate_mod.check_one(
        "rank(ts_mean(f, 10))",            # 10 不在白名单
        ({"f", "ts_mean", "rank"}, "MATRIX", {}, []),
        None, poison, pc,
    )
    win = [w for w in out["warnings"] if "WINDOW" in w]
    assert win, "非白名单窗口必须产生告警"
    assert "10" in win[0]


def test_warning_not_emitted_for_standard_window(gate_mod):
    pc = _pc()
    poison = [p for p in pc.get("poison_patterns", [])
              if p.get("severity", "block") == "block"]
    out = gate_mod.check_one(
        "rank(ts_mean(f, 66))",            # 66 在白名单
        ({"f", "ts_mean", "rank"}, "MATRIX", {}, []),
        None, poison, pc,
    )
    assert not [w for w in out["warnings"] if "WINDOW" in w]


def test_warning_does_not_affect_pass(gate_mod):
    """SOP 允许"给解释后用"→ 告警不得把 `pass` 打成 False。"""
    pc = _pc()
    poison = [p for p in pc.get("poison_patterns", [])
              if p.get("severity", "block") == "block"]
    out = gate_mod.check_one(
        "rank(ts_mean(f, 10))",
        ({"f", "ts_mean", "rank"}, "MATRIX", {}, []),
        None, poison, pc,
    )
    assert out["pass"] is True
    assert out["issues"] == []
    assert out["warnings"]              # 但告警必须在


def test_no_whitelist_config_means_no_check(gate_mod):
    """配置缺 `window_whitelist` 时必须整体跳过（向后兼容，不因缺配置误报）。"""
    pc = _pc()
    poison = []
    pc2 = dict(pc)
    pc2["window_whitelist"] = []
    out = gate_mod.check_one(
        "rank(ts_mean(f, 10))",
        ({"f", "ts_mean", "rank"}, "MATRIX", {}, []),
        None, poison, pc2,
    )
    assert not [w for w in out["warnings"] if "WINDOW" in w]
    assert out["pass"] is True


def test_enforce_mode_blocks_non_whitelist_window(gate_mod):
    """`window_whitelist_enforce=true` 时闸9 升为 block（2026-09-17 新增）。

    默认仍是 warning（SOP 允许"给出解释后用"）；enforce 是给操作者的可选硬门
    ——当日实测新语料违规率 26.5%，散文约束无效。
    """
    pc = _pc()
    pc2 = dict(pc)
    pc2["window_whitelist_enforce"] = True
    out = gate_mod.check_one(
        "rank(ts_mean(f, 10))",
        ({"f", "ts_mean", "rank"}, "MATRIX", {}, []),
        None, [], pc2,
    )
    hits = [i for i in out["issues"] if "WINDOW" in i]
    assert hits, "enforce 模式下非白名单窗口必须进 issues"
    assert "enforce" in hits[0]
    assert out["pass"] is False


def test_enforce_mode_allows_whitelisted_window(gate_mod):
    """enforce 模式下白名单窗口不受影响（不误伤）。"""
    pc = _pc()
    pc2 = dict(pc)
    pc2["window_whitelist_enforce"] = True
    out = gate_mod.check_one(
        "rank(ts_mean(f, 22))",
        ({"f", "ts_mean", "rank"}, "MATRIX", {}, []),
        None, [], pc2,
    )
    assert not [i for i in out["issues"] if "WINDOW" in i]
    assert out["pass"] is True
