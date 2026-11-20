"""datafields 本地排序/过滤（2026-11-17 新增）单测。

背景：外部经验里最有用的一条选字段法是「按 dateCreated 降序 + alphaCount 升序」——
老数据集里 alphaCount==0 的字段多半是被全平台犁过仍无信号的死字段，白空间在近期 onboard 字段。
原始平台 payload 本就带 dateCreated / pyramidMultiplier，是 `_slim_datafields` 曾把它们裁掉，
导致该方法在 MCP 面上不可执行。本文件锁住：
  1) _slim_datafields 必须透传 dateCreated / pyramidMultiplier；
  2) _order_fields 的排序方向、缺失值置尾、覆盖率过滤、非法参数报错、元数据回显。
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mcp_core import _slim_datafields                      # noqa: E402
from tools_data import _order_fields                       # noqa: E402


def _payload():
    return {
        "results": [
            {"id": "old_hot", "coverage": 0.9, "alphaCount": 300, "dateCreated": "2023-01-01"},
            {"id": "new_cold", "coverage": 0.85, "alphaCount": 0, "dateCreated": "2026-10-01"},
            {"id": "mid", "coverage": 0.6, "alphaCount": 5, "dateCreated": "2025-05-05"},
            {"id": "no_date", "coverage": 0.7, "alphaCount": 1},
        ],
        "count": 4,
        "complete": True,
    }


def test_slim_passes_through_date_created_and_multiplier():
    raw = {"results": [{
        "id": "f1", "type": "MATRIX", "coverage": 0.8, "userCount": 2, "alphaCount": 3,
        "dateCreated": "2026-09-30", "pyramidMultiplier": 1.7,
        "description": "x" * 999,
    }], "count": 1}
    out = _slim_datafields(raw)["results"][0]
    assert out["dateCreated"] == "2026-09-30"
    assert out["pyramidMultiplier"] == 1.7
    assert len(out["description"]) <= 161


def test_sort_date_created_desc_puts_newest_first_and_missing_last():
    out = _order_fields(_payload(), "dateCreated", "", None)
    assert [f["id"] for f in out["results"]] == ["new_cold", "mid", "old_hot", "no_date"]
    assert out["sorted_by"] == "dateCreated"
    assert out["sort_order"] == "desc"


def test_sort_alpha_count_defaults_to_ascending():
    out = _order_fields(_payload(), "alphaCount", "", None)
    assert [f["id"] for f in out["results"]][0] == "new_cold"
    assert out["sort_order"] == "asc"


def test_explicit_order_overrides_default_and_missing_still_last():
    out = _order_fields(_payload(), "dateCreated", "asc", None)
    ids = [f["id"] for f in out["results"]]
    assert ids[0] == "old_hot" and ids[-1] == "no_date"
    assert out["sort_order"] == "asc"


def test_min_coverage_filters_and_reports_returned():
    out = _order_fields(_payload(), "", "", 0.8)
    assert {f["id"] for f in out["results"]} == {"old_hot", "new_cold"}
    assert out["returned"] == 2
    assert out["count"] == 4          # 平台总数语义不变
    assert out["min_coverage"] == 0.8


def test_invalid_sort_by_errors_instead_of_silently_ignoring():
    out = _order_fields(_payload(), "notAField", "", None)
    assert "error" in out and "sort_by" in out["error"]


def test_invalid_sort_order_errors():
    out = _order_fields(_payload(), "dateCreated", "upward", None)
    assert "error" in out and "sort_order" in out["error"]


def test_no_sort_by_keeps_platform_order():
    out = _order_fields(_payload(), "", "", None)
    assert [f["id"] for f in out["results"]] == ["old_hot", "new_cold", "mid", "no_date"]
    assert out["sorted_by"] is None


# ---- 2026-11-17 补：max_fields 与排序/过滤的组合语义 ----
# 原缺陷：max_fields 被下传给平台当 limit ⇒ 先截断再排序，「按 dateCreated 找最新字段 + 只看前 N」
# 直接失效（dataset-scoped 实测 returned=0：平台默认序的前 N 条被 min_coverage 全过滤掉）。

import asyncio                                                # noqa: E402

import tools_data as td                                       # noqa: E402


class _FakeClient:
    def __init__(self, payload):
        self.payload = payload
        self.calls = []

    async def get_datafields(self, *args, **kwargs):
        self.calls.append(args)
        return self.payload


def _payload_with_type():
    p = _payload()
    for f in p["results"]:
        f.setdefault("type", "MATRIX")
        f.setdefault("description", "d")
    return p


def test_dataset_scoped_max_fields_is_applied_after_ordering(monkeypatch):
    fake = _FakeClient(_payload_with_type())
    monkeypatch.setattr(td.brain_client, "get_datafields", fake.get_datafields)
    out = asyncio.run(td.get_datafields(
        region="USA", dataset_id="ds1", universe="TOP3000",
        sort_by="dateCreated", max_fields=2))
    # 平台侧不得被 max_fields 截断（第 10 个位置参数就是 max_fields）
    assert fake.calls[0][9] is None
    assert [f["id"] for f in out["results"]] == ["new_cold", "mid"]
    assert out["returned"] == 2
    assert out["cap_applied_after_ordering"] is True


def test_dataset_scoped_max_fields_without_ordering_still_caps_at_api(monkeypatch):
    fake = _FakeClient(_payload_with_type())
    monkeypatch.setattr(td.brain_client, "get_datafields", fake.get_datafields)
    out = asyncio.run(td.get_datafields(
        region="USA", dataset_id="ds1", universe="TOP3000", max_fields=3))
    assert fake.calls[0][9] == 3            # 无排序/过滤时保持平台侧截断
    assert out["returned"] == 4             # 假数据原样返回（不本地截断）


def test_min_coverage_also_disables_api_cap(monkeypatch):
    fake = _FakeClient(_payload_with_type())
    monkeypatch.setattr(td.brain_client, "get_datafields", fake.get_datafields)
    out = asyncio.run(td.get_datafields(
        region="USA", dataset_id="ds1", universe="TOP3000",
        min_coverage=0.8, max_fields=1))
    assert fake.calls[0][9] is None
    assert out["returned"] == 1
    assert out["results"][0]["id"] in ("old_hot", "new_cold")


def test_unscoped_ordering_warns_about_truncation(monkeypatch):
    fake = _FakeClient(_payload_with_type())
    monkeypatch.setattr(td.brain_client, "get_datafields", fake.get_datafields)
    out = asyncio.run(td.get_datafields(
        region="USA", dataset_id=None, universe="TOP3000",
        sort_by="dateCreated", max_fields=2))
    assert fake.calls[0][9] == 2            # unscoped 仍平台侧截断
    assert "ordering_warning" in out
