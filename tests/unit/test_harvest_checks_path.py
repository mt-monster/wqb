# -*- coding: utf-8 -*-
"""checks 取值路径守卫（2026-09-19 修复）。

**根因**：`tools/harvest_multisim.py::_pick_checks` 此前依次找
`data.checks` → `data.raw.checks` → `data.raw.is.checks`，**全部落空**；
真实位置是**顶层 `data.is.checks`**（alpha 详情顶层键含 `is`，checks 在其内）。
后果（实测）：该函数恒返回 `[]` → 所有 checks 派生列采集不到 ——
`alphas.cluster_test` **0/4,926**、`concentrated_weight` **0/4,926**，
而直接读 `is.*` 的列正常（`two_year_sharpe` 86.1%）。

证据链：`is.checks` 含
`{name: CLUSTER_TEST, result: PASS, limit: 1, value: 2.59}`（IND/QPGbAOn5）。
修复后回填实测：`cluster_test` 0 → 73 条，其中 **60 条真正达标**
（IND 22/22、KOR 14/16、USA 7/11、DEU 6/6、HKG 4/4）。

夹具 `tests/fixtures/alpha_detail_cluster_sample.json` 为真实载荷裁剪件（无凭证）。
"""
import json
import os
import sys

import pytest

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(REPO, "tools"))
FIXTURE = os.path.join(REPO, "tests", "fixtures", "alpha_detail_cluster_sample.json")


@pytest.fixture(scope="module")
def H():
    import harvest_multisim as _H  # noqa: PLC0415
    return _H


@pytest.fixture(scope="module")
def payload():
    with open(FIXTURE, encoding="utf-8") as f:
        return json.load(f)


# --------------------------------------------------------------------------- 1
def test_pick_checks_reads_top_level_is_checks(H, payload):
    """核心回归：必须能从顶层 `is.checks` 取到 checks（修复前为 0 项）。"""
    checks = H._pick_checks(payload)
    assert len(checks) == 13, f"应取到 13 项检查，实得 {len(checks)}"
    names = {c["name"] for c in checks}
    assert "CLUSTER_TEST" in names
    assert {"LOW_SHARPE", "LOW_FITNESS", "CONCENTRATED_WEIGHT",
            "LOW_SUB_UNIVERSE_SHARPE"} <= names


def test_extract_cluster_test_value(H, payload):
    """CLUSTER_TEST 的数值必须可提取（写入 alphas.cluster_test）。"""
    checks = H._pick_checks(payload)
    assert H._extract_check_value(checks, "CLUSTER_TEST") == pytest.approx(2.59)
    assert H._extract_check_value(checks, "LOW_SHARPE") == pytest.approx(3.67)
    # 缺失项返回 None（不得抛异常 / 不得瞎猜）
    assert H._extract_check_value(checks, "NOT_A_CHECK") is None


def test_cluster_check_carries_region_limit(H, payload):
    """CLUSTER_TEST 自带区域门槛（文章：默认 1.58；KOR/JPS/TWN/HKG/IND/GBR/DEU 为 1.0）。

    夹具为 IND → limit 应为 1（低门槛区），这是"是否达标"的权威判据，
    比按区域名硬编码更可靠。
    """
    checks = H._pick_checks(payload)
    entry = next(c for c in checks if c["name"] == "CLUSTER_TEST")
    assert float(entry["limit"]) == pytest.approx(1.0)
    assert entry["result"] == "PASS"


# --------------------------------------------------------------------------- 2
def test_badge_lives_in_classifications_value_lives_in_checks(payload):
    """两个位置的分工必须被文档化锁定：

    - **徽章**（`CLUSTER:CLUSTER`）在 `classifications`；
    - **数值/门槛**（CLUSTER_TEST）在 `is.checks`。
    只读其一会拿不到完整事实（前者是定性结论，后者是定量与门槛）。
    """
    ids = [c.get("id") for c in (payload.get("classifications") or [])]
    assert "CLUSTER:CLUSTER" in ids
    names = {c["name"] for c in (payload["is"]["checks"])}
    assert "CLUSTER_TEST" in names


# --------------------------------------------------------------------------- 3
@pytest.mark.parametrize("shape", ["flat", "raw", "raw_is"])
def test_legacy_shapes_still_supported(H, shape):
    """兼容层回归：历史端点形态不得被本次修复破坏。"""
    payload = {
        "flat": {"checks": [{"name": "LOW_SHARPE", "value": 1.0}]},
        "raw": {"raw": {"checks": [{"name": "LOW_SHARPE", "value": 1.0}]}},
        "raw_is": {"raw": {"is": {"checks": [{"name": "LOW_SHARPE", "value": 1.0}]}}},
    }[shape]
    assert H._pick_checks(payload) == [{"name": "LOW_SHARPE", "value": 1.0}]


def test_pick_checks_returns_empty_when_absent(H):
    """无 checks（如未完成回测）→ 空列表，绝不抛异常。"""
    assert H._pick_checks({}) == []
    assert H._pick_checks({"is": {}}) == []
    assert H._pick_checks({"is": {"checks": []}}) == []


def test_is_checks_takes_priority_over_legacy(H):
    """顶层 `is.checks` 与 legacy 同时存在时，以真实位置为准。"""
    payload = {
        "is": {"checks": [{"name": "REAL", "value": 1.0}]},
        "checks": [{"name": "STALE", "value": 9.9}],
    }
    assert H._pick_checks(payload) == [{"name": "REAL", "value": 1.0}]
