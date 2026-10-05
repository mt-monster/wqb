# -*- coding: utf-8 -*-
"""wqb.quota —— 提交配额的分型计数（2026-10-05 补测试）。

战例（2026-10-05 修正动因）：某日 4 颗提交里 1 颗是 SUPER，`_quota_gate` 与
`tools/quota_status.py` 都把「当日提交总数」当 REGULAR 用量，于是报 **4/4 满额**，
而真实 REGULAR 用量是 **3/4** —— 在仍有余额时误拦合法提交。平台对
REGULAR(4/ET 日) 与 SUPER(1/ET 日) 是**两条独立**配额线。

另一个方向也要守住：记录缺 `type` 时**判不了型**，按保守口径计入 REGULAR
（多算只是少提交一颗，漏算才会把配额判松、撞平台 403）。
"""
import datetime as dt
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "src"))

from wqb.quota import (  # noqa: E402
    REGULAR_DAILY_LIMIT,
    SUPER_DAILY_LIMIT,
    alpha_kind,
    probe_today,
)

UTC = dt.timezone.utc
# ET 2026-09-29 11:00（EDT=UTC-4）：同一 ET 日内的时刻
NOW = dt.datetime(2026, 9, 29, 15, 0, tzinfo=UTC)


def _row(ts, atype="REGULAR", region="USA"):
    return {"id": "A" + ts[-6:], "type": atype, "dateSubmitted": ts,
            "settings": {"region": region}}


def test_limits_are_pinned_to_the_platform_lines():
    assert (REGULAR_DAILY_LIMIT, SUPER_DAILY_LIMIT) == (4, 1)


def test_alpha_kind_reads_only_the_type_field():
    assert alpha_kind({"type": "REGULAR"}) == "REGULAR"
    assert alpha_kind({"type": " SUPER "}) == "SUPER"        # 大小写 / 空白容忍
    assert alpha_kind({"type": "WEIRD"}) is None             # 未知不猜
    assert alpha_kind({"name": "IND_S_10comp_x"}) is None    # ★ 不靠名字猜类型
    assert alpha_kind({}) is None
    assert alpha_kind(None) is None


def test_super_does_not_borrow_the_regular_line():
    """★ 4 颗（含 1 颗 SUPER）必须是 REGULAR 3/4 剩余 1，而不是 4/4。"""
    rows = [_row("2026-09-29T05:00:00-04:00") for _ in range(3)]
    rows.append(_row("2026-09-29T06:00:00-04:00", atype="SUPER"))
    q = probe_today(rows, NOW)
    assert q["total_today"] == 4
    assert (q["regular_explicit"], q["super_used"]) == (3, 1)
    assert (q["regular_used"], q["regular_remaining"]) == (3, 1)      # 不是 4/4
    assert (q["super_used"], q["super_remaining"]) == (1, 0)


def test_unclassified_counted_conservatively_into_regular():
    """老记录/上游瘦身丢掉 `type` 时宁可多算 REGULAR，绝不把配额判松。"""
    rows = [_row("2026-09-29T05:00:00-04:00"),
            {"id": "noType", "dateSubmitted": "2026-09-29T06:00:00-04:00"}]
    q = probe_today(rows, NOW)
    assert q["unclassified_used"] == 1
    assert q["regular_explicit"] == 1
    assert q["regular_used"] == 2                       # 未判型并入 REGULAR
    assert q["entries"][1]["kind"] == "UNCLASSIFIED"    # 打印宽度用，不能是 None


def test_only_the_current_et_day_counts_and_malformed_rows_are_skipped():
    rows = [_row("2026-09-29T05:00:00-04:00"),            # 今日（ET）
            _row("2026-09-29T13:00:00Z"),                 # 今日
            _row("2026-09-28T23:59:00-04:00"),            # 昨日 23:59 ET
            _row("2026-09-27T12:00:00Z"),
            {"dateSubmitted": "bad"},                     # 不可解析 → 跳过
            {"id": "no-ts"},                              # 缺字段 → 跳过
            "not-a-dict"]                                 # 脏行 → 跳过
    q = probe_today(rows, NOW)
    assert q["et_day"] == "2026-09-29"
    assert q["total_today"] == 2 and q["regular_used"] == 2


def test_day_boundary_is_dst_aware():
    """2026-11-02 04:30Z 在 EST 下仍是 11-01 23:30；写死 UTC-4 会误算成 11-02。"""
    rows = [_row("2026-11-01T22:00:00-05:00", atype="SUPER")]
    q1 = probe_today(rows, dt.datetime(2026, 11, 2, 4, 30, tzinfo=UTC))
    assert q1["et_day"] == "2026-11-01" and q1["super_used"] == 1
    q2 = probe_today(rows, dt.datetime(2026, 11, 2, 5, 0, tzinfo=UTC))   # 00:00 EST
    assert q2["et_day"] == "2026-11-02" and q2["super_used"] == 0


def test_consumers_take_numbers_from_wqb_quota_not_their_own():
    """两个消费点不得各自再算一套（历史上正是这样分叉出 4/4 误报的）。"""
    gate = (ROOT / "src" / "wqb" / "workflow" / "nodes" / "submit_alpha.py").read_text(encoding="utf-8")
    tool = (ROOT / "tools" / "quota_status.py").read_text(encoding="utf-8")
    assert "from ...quota import REGULAR_DAILY_LIMIT, probe_today" in gate
    assert "probe_today(results)" in gate
    assert "from wqb.quota import probe_today" in tool
    # 工具侧不得再自己拆时间戳（唯一实现 = probe_today）
    assert "fromisoformat" not in tool
    # 且不得回到「把当日总数当 REGULAR」的旧口径
    assert "used_r = len(" not in tool
