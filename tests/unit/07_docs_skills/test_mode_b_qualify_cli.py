# -*- coding: utf-8 -*-
"""tools/mode_b_qualify.py：与 evaluate_mode_b 同一判定函数的只读 CLI（skills 审查 OP-18 / HP-15）。

用不存在的区域 ZZZ + 空的临时 DB，落到内置默认（主闸 1.25/0.8），不依赖仓库里 tracking/ 与 data/ 的现状。
"""
import io
import json
import sys
from contextlib import redirect_stdout
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "tools"))

import mode_b_qualify as Q  # noqa: E402


@pytest.fixture(autouse=True)
def _isolated_db(tmp_path, monkeypatch):
    monkeypatch.setenv("WQB_DB_PATH", str(tmp_path / "nope.db"))


def _run(*argv):
    buf = io.StringIO()
    with redirect_stdout(buf):
        rc = Q.main(list(argv))
    return rc, json.loads(buf.getvalue())


def _evaluate(**kw):
    argv = ["evaluate", "--region", "ZZZ"]
    for k, v in kw.items():
        flag = "--" + k.replace("_", "-")
        argv += [flag] if v is True else [flag, str(v)]
    return _run(*argv)


def test_main_gate():
    rc, out = _evaluate(sharpe=1.30, fitness=0.85)
    assert rc == 0 and out["result"]["verdict"] == "main_gate" and out["result"]["eligible"] is True
    assert out["main_gate"] == {"sharpe_min": 1.25, "fitness_min": 0.8}


def test_bypass_e_two_year_strong():
    _, out = _evaluate(sharpe=0.9, fitness=0.55, two_year_sharpe=1.35)
    assert out["result"]["verdict"] == "bypass" and out["result"]["bypass"] == "E_2y_strong"
    assert out["result"]["mode_b_action"]


def test_bypass_a_needs_robust_sharpe_which_the_judge_node_never_feeds():
    _, out = _evaluate(sharpe=0.9, fitness=0.55, robust_sharpe=1.1)
    assert out["result"]["bypass"] == "A_robust_strong"
    _, without = _evaluate(sharpe=0.9, fitness=0.55)
    assert without["result"]["verdict"] == "no_qualify"          # 缺该指标 = 旁路不命中，不是「通过」


def test_bypass_b_requires_other_dims_declared():
    _, unknown = _evaluate(sharpe=1.0, fitness=0.7, prod_corr=0.78)
    assert unknown["result"]["verdict"] == "no_qualify"
    _, ok = _evaluate(sharpe=1.0, fitness=0.7, prod_corr=0.78, other_dims_pass=True)
    assert ok["result"]["bypass"] == "B_prod_corr_only"


def test_bypass_c_margin_bp_alias():
    _, out = _evaluate(sharpe=1.05, fitness=0.7, margin_bp=6)
    assert out["result"]["bypass"] == "C_margin_strong"
    assert out["inputs"]["margin"] == pytest.approx(0.0006)


def test_bypass_d_uses_returns_median():
    _, out = _evaluate(sharpe=0.9, fitness=0.5, returns=0.08, returns_median=0.05, turnover=0.75)
    assert out["result"]["bypass"] == "D_turnover_fixable"


def test_hard_kill_needs_all_three_weak():
    _, dead = _evaluate(sharpe=0.9, fitness=0.55, two_year_sharpe=0.9)
    assert dead["result"]["verdict"] == "dead_end" and dead["result"]["eligible"] is False
    _, unknown_2y = _evaluate(sharpe=0.9, fitness=0.55)
    assert unknown_2y["result"]["verdict"] == "no_qualify"       # 2Y 未知不能判死
    _, s_ok = _evaluate(sharpe=1.3, fitness=0.55, two_year_sharpe=0.9)
    assert s_ok["result"]["verdict"] == "no_qualify"             # 单维度弱不判死


@pytest.mark.parametrize("bad", [["--margin", "5"], ["--turnover", "70"], ["--returns", "12"]])
def test_percent_or_bp_values_are_rejected(bad):
    with pytest.raises(SystemExit) as e:
        _run("evaluate", "--region", "ZZZ", "--sharpe", "1", "--fitness", "1", *bad)
    assert "小数" in str(e.value)


def test_show_prints_effective_config_and_source():
    rc, out = _run("show", "--region", "ZZZ")
    assert rc == 0
    cfg = out["config"]
    assert set(cfg["bypass_rules"]) == {"A_robust_strong", "B_prod_corr_only", "C_margin_strong",
                                        "D_turnover_fixable", "E_2y_strong"}
    assert cfg["hard_kill"]["two_year_sharpe_max"] == 1.2 and cfg["_source"] == "default"


def test_cli_is_read_only_and_never_creates_the_db(tmp_path):
    _evaluate(sharpe=1.3, fitness=0.9)
    assert not (tmp_path / "nope.db").exists()
