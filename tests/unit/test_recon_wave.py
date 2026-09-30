# -*- coding: utf-8 -*-
"""波级默认取证的决策问题派生（`src/wqb/recon_wave.py`）守护。

派生必须是机械、确定、可解释的：同一波同一批结果 → 同一问题；不是「墙」的（个案 / 全弱 / 无指标）不问论坛（token 黑洞）。
"""
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "src"))

from wqb import recon_evidence as RE  # noqa: E402
from wqb import recon_wave as RW  # noqa: E402
from wqb.config import PRODCORR_CEILING, RA_CHECK_NAMES  # noqa: E402


def _row(alpha="a", ds="analyst4", sharpe=1.7, failed=(), prod=None):
    return {"alpha_id": alpha, "dataset": ds, "sharpe": sharpe,
            "ra_failed_checks": list(failed) if failed is not None else None, "prod_correlation": prod}


# ----------------------------------------------------------------------------- 词表与 config 的单一事实源
def test_every_ra_check_has_a_wall_and_nothing_else_does():
    """config 新增一项 RA 闸而这里没给它墙 → 该闸挡住的行会被静默算成「pass」；反之墙表里有 config 里没有的闸名 → 拼写漂移。"""
    assert set(RW.WALL_BY_CHECK) == set(RA_CHECK_NAMES)


def test_walls_are_a_closed_vocabulary_with_titles_and_priorities():
    walls = set(RW.WALL_BY_CHECK.values())
    assert walls == {RW.STRENGTH_WALL} | set(RW.WALL_TITLE) - {"prod"}      # prod 来自相关性列，不来自 RA 闸名
    assert set(RW.WALL_PRIORITY) == set(RW.WALL_TITLE)                      # 每堵可选的墙都有说法、都有并列顺序
    assert RW.STRENGTH_WALL not in RW.WALL_TITLE                            # 强度不是「墙」：缺的是想法，不是破墙配方


# ----------------------------------------------------------------------------- failed_names
@pytest.mark.parametrize("value,expected", [
    (["LOW_2Y_SHARPE"], ["LOW_2Y_SHARPE"]),
    ('["LOW_2Y_SHARPE", "CONCENTRATED_WEIGHT"]', ["LOW_2Y_SHARPE", "CONCENTRATED_WEIGHT"]),
    ([{"name": "HIGH_TURNOVER", "result": "FAIL"}], ["HIGH_TURNOVER"]),
    ([], []), ("[]", []),                                     # 空列表 = RA 全过（不是「不知道」）
    (None, None), ("", None), ("not json", None), ({"a": 1}, None), (5, None),
])
def test_failed_names(value, expected):
    assert RW.failed_names(value) == expected


# ----------------------------------------------------------------------------- classify_row
def test_classify_row_categories():
    assert RW.classify_row({"sharpe": None, "ra_failed_checks": ["LOW_SHARPE"]})["category"] == "none"     # 无指标：不参与
    assert RW.classify_row({"sharpe": "", "ra_failed_checks": []})["category"] == "none"
    assert RW.classify_row(_row(failed=[]))["category"] == "pass"
    assert RW.classify_row(_row(failed=None))["category"] == "pass"                                        # NULL 与 [] 同义：store 把「RA 全过」也存成 NULL
    c = RW.classify_row(_row(failed=["LOW_2Y_SHARPE", "IS_LADDER_SHARPE", "CONCENTRATED_WEIGHT"]))
    assert c["category"] == "blocked" and c["walls"] == ["2Y", "CW"]                                       # 同一堵墙的两个闸名只算一次
    assert RW.classify_row(_row(failed=["LOW_SHARPE", "LOW_2Y_SHARPE"]))["category"] == "weak"             # 强度没过 → 缺想法，不是缺配方


def test_strength_falls_back_to_the_numbers_when_the_ra_list_is_null():
    """NULL 名单既可能是「RA 全过」也可能是「没带名单的旧行」——强度线按数值兜底，弱行不会被误记成 pass。"""
    assert RW.classify_row(_row(sharpe=0.5, failed=None))["category"] == "weak"
    assert RW.classify_row({"sharpe": 1.9, "fitness": 0.6, "ra_failed_checks": None})["category"] == "weak"
    assert RW.classify_row({"sharpe": 1.9, "fitness": None, "ra_failed_checks": None})["category"] == "pass"   # 没有 fitness：不以缺失判弱
    assert RW.classify_row({"sharpe": RW.SHARPE_MIN, "fitness": RW.FITNESS_MIN, "ra_failed_checks": None})["category"] == "pass"   # 严格不等式：等于线不算弱
    assert RW.classify_row(_row(sharpe=0.5, failed=["LOW_SHARPE"]))["walls"] == ["sharpe"]                  # 名单已有强度项：不重复


def test_prod_correlation_is_a_wall_at_the_shared_ceiling_and_strength_still_wins():
    assert RW.classify_row(_row(prod=PRODCORR_CEILING))["walls"] == ["prod"]                               # 与 is_pass 同口径：>= 就算
    assert RW.classify_row(_row(prod=PRODCORR_CEILING - 0.01))["category"] == "pass"
    assert RW.classify_row(_row(prod=0.95, failed=["LOW_FITNESS"]))["category"] == "weak"
    assert RW.classify_row(_row(prod=0.9, failed=None))["walls"] == ["prod"]                               # NULL 名单 = 无 RA 失败，prod 照样是墙
    assert RW.classify_row(_row(prod="bad"))["category"] == "pass"                                         # 非数按「没有」处理


# ----------------------------------------------------------------------------- derive_decision：墙问题
def test_a_shared_wall_becomes_the_wall_question():
    rows = [_row(f"a{i}", failed=["LOW_2Y_SHARPE"]) for i in range(3)] + [_row("p", failed=[])]
    d = RW.derive_decision("KOR", 97, rows)
    assert d["kind"] == RW.KIND_WALL and d["wall"] == "2Y" and d["dataset"] == "analyst4"
    assert d["question"] == "KOR analyst4 2Y 稳健性墙 破墙配方"
    assert d["context"] == {"region": "KOR", "dataset": "analyst4", "wall": "2Y"}
    assert d["question_key"] == RE.question_key(d["question"])
    assert d["basis"]["n_blocked"] == 3 and d["basis"]["n_pass"] == 1 and d["basis"]["wall_counts"] == {"2Y": 3}
    assert d["reason"] is None


def test_one_row_is_an_anecdote_not_a_wall():
    d = RW.derive_decision("KOR", 1, [_row("a", failed=["LOW_2Y_SHARPE"]), _row("b", failed=[])])
    assert d["kind"] is None and d["reason"] == RW.SKIP_NOTHING
    d = RW.derive_decision("KOR", 1, [_row("a", failed=["LOW_2Y_SHARPE"])])
    assert d["kind"] is None and d["reason"] == RW.SKIP_TOO_FEW


def test_most_rows_wins_and_priority_only_breaks_ties():
    rows = [_row(f"t{i}", failed=["HIGH_TURNOVER"]) for i in range(3)] + [_row(f"p{i}", prod=0.9) for i in range(2)]
    assert RW.derive_decision("KOR", 1, rows)["wall"] == "tvr"                         # 票数多者胜
    rows = [_row(f"c{i}", failed=["CONCENTRATED_WEIGHT"]) for i in range(2)] + [_row(f"y{i}", failed=["LOW_2Y_SHARPE"]) for i in range(2)]
    assert RW.derive_decision("KOR", 1, rows)["wall"] == "2Y"                          # 并列：2Y 先于 CW
    assert RW.derive_decision("KOR", 1, list(reversed(rows)))["question"] == RW.derive_decision("KOR", 1, rows)["question"]   # 与行序无关


def test_prod_wall_question():
    rows = [_row(f"a{i}", prod=0.81) for i in range(2)]
    d = RW.derive_decision("HKG", "s2_ds_d1", rows)
    assert d["wall"] == "prod" and d["question"] == "HKG analyst4 prod 相关性墙 破墙配方" and d["wave"] == "s2_ds_d1"


def test_weak_rows_are_not_counted_toward_walls():
    """强度都没过的行，2Y 也没过是必然的——那不是「2Y 墙」，是信号弱。"""
    rows = [_row(f"w{i}", sharpe=0.5, failed=["LOW_SHARPE", "LOW_2Y_SHARPE"]) for i in range(4)]
    d = RW.derive_decision("KOR", 1, rows)
    assert d["kind"] == RW.KIND_DEAD_END and d["basis"]["wall_counts"] == {}


# ----------------------------------------------------------------------------- derive_decision：判死取证问题
def test_an_all_weak_wave_asks_the_dead_end_question():
    rows = [_row(f"w{i}", sharpe=0.4, failed=["LOW_SHARPE", "LOW_FITNESS"]) for i in range(3)]
    d = RW.derive_decision("KOR", 5, rows)
    assert d["kind"] == RW.KIND_DEAD_END and d["wall"] is None
    assert d["question"] == "KOR analyst4 有无解法" and d["context"] == {"region": "KOR", "dataset": "analyst4"}
    assert d["question_key"] == RE.question_key("KOR analyst4 有无解法")


def test_dead_end_question_needs_no_pass_no_blocked_and_enough_weak_rows():
    weak = [_row(f"w{i}", failed=["LOW_SHARPE"]) for i in range(3)]
    assert RW.derive_decision("KOR", 1, weak + [_row("p", failed=[])])["reason"] == RW.SKIP_NOTHING      # 有产出：不判死
    assert RW.derive_decision("KOR", 1, weak + [_row("b", failed=["LOW_2Y_SHARPE"])])["reason"] == RW.SKIP_NOTHING   # 单条卡墙：还不是共同瓶颈，也不是全灭
    assert RW.derive_decision("KOR", 1, weak[:1])["reason"] == RW.SKIP_TOO_FEW                            # 一条弱不足以说「全灭」


# ----------------------------------------------------------------------------- derive_decision：不参与 / 不问
def test_rows_without_metrics_are_not_evidence():
    rows = [{"alpha_id": "e1", "dataset": "d", "sharpe": None, "ra_failed_checks": None},
            {"alpha_id": "e2", "dataset": "d", "sharpe": None, "ra_failed_checks": ["LOW_SHARPE"]}]
    d = RW.derive_decision("KOR", 1, rows)
    assert d["kind"] is None and d["reason"] == RW.SKIP_NO_ROWS and d["basis"]["n_rows"] == 2 and d["basis"]["n_evaluated"] == 0
    assert RW.derive_decision("KOR", 1, [])["reason"] == RW.SKIP_NO_ROWS
    mixed = rows + [_row("a", failed=["LOW_2Y_SHARPE"])]                              # ERROR 行不凑数：只剩 1 条有指标的
    assert RW.derive_decision("KOR", 1, mixed)["reason"] == RW.SKIP_TOO_FEW


def test_dataset_is_taken_from_the_argument_else_the_majority_and_is_required():
    rows = [_row("a", ds="d1", failed=["LOW_2Y_SHARPE"]), _row("b", ds="d2", failed=["LOW_2Y_SHARPE"]),
            _row("c", ds="d2", failed=["LOW_2Y_SHARPE"])]
    assert RW.derive_decision("KOR", 1, rows)["dataset"] == "d2"
    assert RW.derive_decision("KOR", 1, rows, dataset="d1")["question"].startswith("KOR d1 ")
    no_ds = [_row(f"n{i}", ds="", failed=["LOW_2Y_SHARPE"]) for i in range(3)]
    d = RW.derive_decision("KOR", 1, no_ds)
    assert d["kind"] is None and d["reason"] == RW.SKIP_NO_DATASET              # 没有数据集就没有具体问题：泛问题只会烧 token


def test_the_question_does_not_depend_on_the_wave_so_the_seven_day_cache_is_shared_across_waves():
    rows = [_row(f"a{i}", failed=["LOW_2Y_SHARPE"]) for i in range(2)]
    assert RW.derive_decision("KOR", 1, rows)["question_key"] == RW.derive_decision("KOR", 2, rows)["question_key"]
    assert RW.derive_decision("HKG", 1, rows)["question_key"] != RW.derive_decision("KOR", 1, rows)["question_key"]   # region 分键：ledger 记录按 region 作用域


# ----------------------------------------------------------------------------- 波标记
def test_marker_status_and_who_consumes_the_wave_quota():
    assert RW.marker_status({"status": "ok"}) == "ok" and RW.marker_status({"status": "no_result"}) == "no_result"
    assert RW.marker_status({"status": "error"}) == "error"
    assert RW.marker_status({"status": "whatever"}) is None and RW.marker_status(None) is None and RW.marker_status("x") is None
    assert RW.marker_blocks_rerun({"status": "ok"}) and RW.marker_blocks_rerun({"status": "no_result"})
    assert not RW.marker_blocks_rerun({"status": "error"})                       # 故障不占额度：故障 ≠ 取证
    assert not RW.marker_blocks_rerun({}) and not RW.marker_blocks_rerun(None) and not RW.marker_blocks_rerun({"status": "x"})


def test_build_marker_derives_status_from_found_and_keeps_the_trace():
    d = RW.derive_decision("KOR", 97, [_row(f"a{i}", failed=["LOW_2Y_SHARPE"]) for i in range(2)])
    m = RW.build_marker("KOR", 97, d, {"found": False, "sink": "KOR/forum_recon_negative_x"}, "2026-09-30T00:00:00")
    assert (m["status"], m["found"], m["wave"], m["kind"], m["wall"]) == ("no_result", False, "97", "wall", "2Y")
    assert m["question_key"] == d["question_key"] and m["sink"] == "KOR/forum_recon_negative_x" and m["forced"] is False
    err = RW.build_marker("KOR", 97, d, {"found": None, "error": "auth"}, "t", forced=True)
    assert err["status"] == "error" and err["error"] == "auth" and err["forced"] is True
    assert RW.build_marker("KOR", 97, d, {"found": True}, "t")["status"] == "ok"
