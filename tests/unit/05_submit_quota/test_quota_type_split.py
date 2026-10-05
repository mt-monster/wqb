# -*- coding: utf-8 -*-
"""配额类型化口径：REGULAR / SUPER 分流计数（`wqb.quota`）。

回归（2026-10-05 事故）：
  `tools/quota_status.py` 与 `submit_alpha._quota_gate` 都把 OS 池里**当日提交总数**
  当作 REGULAR 用量。而平台对 REGULAR(4/ET 日) 与 SUPER(1/ET 日) 是**两条独立**配额线
  ⇒ 混入 SUPER 会**高估** REGULAR 用量、在仍有余额时误报满额并拦下合法提交。

  实测当日 4 颗提交中 1 颗为 SUPER（`d51nKZJE` / `IND_S_10comp_1nKZJE`）：
  工具报 REGULAR `4/4`，**实际 `3/4`**。
"""
import datetime as dt
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[3]
UTC = dt.timezone.utc


def _u(*a):
    return dt.datetime(*a, tzinfo=UTC)


@pytest.fixture(scope="module")
def q():
    if str(ROOT / "src") not in sys.path:
        sys.path.insert(0, str(ROOT / "src"))
    import wqb.quota as mod
    return mod


def _rec(aid, ts, *, type_=None, name=None, settings=None, region="IND"):
    r = {"id": aid, "dateSubmitted": ts, "settings": {"region": region, **(settings or {})}}
    if type_ is not None:
        r["type"] = type_
    if name is not None:
        r["name"] = name
    return r


# ---------------------------------------------------------------- alpha_kind

def test_kind_prefers_explicit_type_field(q):
    assert q.alpha_kind(_rec("A", None, type_="REGULAR")) == "REGULAR"
    assert q.alpha_kind(_rec("B", None, type_="SUPER")) == "SUPER"
    assert q.alpha_kind(_rec("C", None, type_="regular")) == "REGULAR"   # 大小写不敏感


def test_kind_falls_back_to_selection_settings(q):
    """无 type 时，SUPER 专有 settings 键可判型。"""
    assert q.alpha_kind(_rec("A", None, settings={"selectionHandling": "POSITIVE"})) == "SUPER"
    assert q.alpha_kind(_rec("B", None, settings={"selectionLimit": 10})) == "SUPER"
    assert q.alpha_kind(_rec("C", None, settings={"componentActivation": "IS"})) == "SUPER"
    # 普通 REGULAR settings 不误判
    assert q.alpha_kind(_rec("D", None, settings={"decay": 5, "neutralization": "SECTOR"})) == "UNKNOWN"


def test_kind_falls_back_to_name_convention(q):
    assert q.alpha_kind(_rec("A", None, name="IND_S_10comp_1nKZJE")) == "SUPER"
    assert q.alpha_kind(_rec("B", None, name="ASI_R_qbucket_01")) == "REGULAR"


def test_kind_unknown_on_malformed_record(q):
    assert q.alpha_kind(None) == "UNKNOWN"
    assert q.alpha_kind({}) == "UNKNOWN"
    assert q.alpha_kind({"settings": None}) == "UNKNOWN"


# ---------------------------------------------------------------- probe_today

def test_probe_splits_regular_and_super(q):
    """2026-10-05 真实构成：3 REGULAR + 1 SUPER ⇒ REGULAR 用量必须报 3（不是 4）。"""
    now = _u(2026, 10, 5, 19, 10)                       # ET 2026-10-05 15:10
    rows = [
        _rec("d51nKZJE", "2026-10-05T02:00:11-04:00", type_="SUPER", name="IND_S_10comp_1nKZJE"),
        _rec("LLZg3XWa", "2026-10-05T01:40:18-04:00", type_="REGULAR", name="IND_R_anlcountgate_01"),
        _rec("0mre68gv", "2026-10-05T01:35:28-04:00", type_="REGULAR", region="KOR"),
        _rec("3qVa2Lze", "2026-10-05T01:14:46-04:00", type_="REGULAR", region="GBR",
             name="GBR_R_pd2y_rank_bf500"),
    ]
    p = q.probe_today(rows, now)
    assert p["et_day"] == "2026-10-05"
    assert p["regular_used"] == 3 and p["regular_remaining"] == 1
    assert p["regular_explicit"] == 3 and p["unclassified_used"] == 0
    assert p["super_used"] == 1 and p["super_remaining"] == 0
    assert len(p["entries"]) == 4


def test_probe_excludes_previous_et_day(q):
    now = _u(2026, 10, 5, 19, 10)
    rows = [_rec("A", "2026-10-05T01:00:00-04:00", type_="REGULAR"),
            _rec("B", "2026-10-04T23:59:00-04:00", type_="REGULAR"),   # 昨日 ET
            _rec("C", "2026-10-03T12:00:00Z", type_="REGULAR")]
    p = q.probe_today(rows, now)
    assert p["regular_used"] == 1


def test_probe_tolerates_malformed_rows(q):
    now = _u(2026, 10, 5, 19, 10)
    rows = [{"id": "x"}, {"dateSubmitted": "bad"}, None,
            _rec("ok", "2026-10-05T01:00:00-04:00", type_="REGULAR")]
    p = q.probe_today(rows, now)
    assert p["regular_used"] == 1 and len(p["entries"]) == 1
    assert q.probe_today(None, now)["regular_used"] == 0


def test_untyped_rows_are_charged_to_regular_conservatively(q):
    """判不出类型的条目**仍计入 REGULAR 预算**（保守记账），同时单列 unclassified 供复核。

    理由：反向（未知不计入）会让闸放行——虽有平台 403 兜底（零成本），但会白跑一次 POST；
    而今天出事的正是"多算/误拦"方向，故此处取「保守记账 + 可复核」而非「乐观释放」。
    """
    now = _u(2026, 10, 5, 19, 10)
    p = q.probe_today([_rec("mystery", "2026-10-05T01:00:00-04:00")], now)
    assert p["regular_used"] == 1        # 保守：占 REGULAR 预算
    assert p["regular_explicit"] == 0    # 但显式 REGULAR 数为 0
    assert p["unclassified_used"] == 1   # 单列，供上游字段缺失时告警
    assert p["super_used"] == 0


def test_regular_and_super_limits_are_independent(q):
    now = _u(2026, 10, 5, 19, 10)
    rows = [_rec(f"R{i}", f"2026-10-05T0{i}:00:00-04:00", type_="REGULAR") for i in range(1, 5)]
    rows.append(_rec("S1", "2026-10-05T05:00:00-04:00", type_="SUPER"))
    p = q.probe_today(rows, now)
    assert p["regular_remaining"] == 0 and p["super_remaining"] == 0   # 各自独立满额
