# -*- coding: utf-8 -*-
"""2026-10-24 P1-6 / P0-4 守卫：区域层选集规则文件（判死清单 + 机制标注）。

背景：
  - P1-6 把「USA 已判死数据集」落成区域文件，由 `campaign_intel s0-select` 自动剔除。
    不走 ledger `*_dead` 键，是因为那条写入路径受 `seal_dead_end` 论坛取证闸管辖
    （AGENTS.md §8.11，工具故障/无证据不得判死）。
  - P0-4 把「机制是否经典异象」并入排序键第三层。
  - 用户 2026-10-23 纪律：过期证据不能作证 ⇒ 条目 `as_of` 超过 `review_after_days`
    自动降为 advisory（判死清单）/ 未标注（机制图），且必须显式告警、不许静默生效。

本测试锁死：
  1. 解析 fenced ```json 块 + live/stale 分流 + as_of 缺失按过期处理
  2. 文件缺失静默、解析失败告警（fail-soft 但不静默）
  3. 机制标注的 tier 映射（true=0 / 缺失=1 / false=2）
  4. 真实 USA 两个文件可解析且字段完整（防手改坏 JSON）
"""
import importlib.util
import os
import sys

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))


def _load():
    spec = importlib.util.spec_from_file_location(
        "campaign_intel_region_rules", os.path.join(REPO, "tools", "campaign_intel.py"))
    m = importlib.util.module_from_spec(spec)
    sys.modules["campaign_intel_region_rules"] = m
    spec.loader.exec_module(m)
    return m


def _write_rule(tmp_path, filename, json_text):
    d = tmp_path / "tracking" / "TESTREG" / "reference"
    d.mkdir(parents=True, exist_ok=True)
    p = d / filename
    p.write_text("# test\n\n```json\n" + json_text + "\n```\n", encoding="utf-8")
    return p


def test_dead_list_splits_live_and_stale(tmp_path):
    ci = _load()
    _write_rule(tmp_path, "testreg_dead_datasets.md", """
{
  "region": "TESTREG", "as_of": "2026-10-01", "review_after_days": 30,
  "datasets": [
    {"dataset": "fresh_ds", "verdict": "prod_sealed", "reason": "prod 0.99", "as_of": "2026-10-20"},
    {"dataset": "old_ds", "verdict": "signal_short", "reason": "S 0.3", "as_of": "2026-01-01"}
  ]
}""")
    res = ci._load_region_dead_list("TESTREG", root=str(tmp_path))
    assert set(res["live"]) == {"fresh_ds"}
    assert set(res["stale"]) == {"old_ds"}
    assert res["review_after_days"] == 30
    assert res["warning"] is None


def test_missing_as_of_counts_as_stale(tmp_path):
    """无日期无法证明新鲜 ⇒ 过期（用户 2026-10-23 纪律），不得生效。"""
    ci = _load()
    _write_rule(tmp_path, "testreg_dead_datasets.md", """
{"datasets": [{"dataset": "no_date", "reason": "x"}]}""")
    res = ci._load_region_dead_list("TESTREG", root=str(tmp_path))
    assert res["live"] == {}
    assert set(res["stale"]) == {"no_date"}


def test_missing_file_is_silent(tmp_path):
    ci = _load()
    res = ci._load_region_dead_list("TESTREG", root=str(tmp_path))
    assert res["entries"] == {} and res["warning"] is None


def test_broken_json_warns_not_silent(tmp_path):
    """解析失败必须带 warning（fail-soft 但不静默吞掉）。"""
    ci = _load()
    d = tmp_path / "tracking" / "TESTREG" / "reference"
    d.mkdir(parents=True, exist_ok=True)
    (d / "testreg_dead_datasets.md").write_text(
        "# broken\n\n```json\n{not json}\n```\n", encoding="utf-8")
    res = ci._load_region_dead_list("TESTREG", root=str(tmp_path))
    assert res["entries"] == {}
    assert res["warning"] and "无法解析" in res["warning"]


def test_mechanism_tier_mapping():
    ci = _load()
    assert ci._mechanism_tier({"classic_anomaly": True}) == 0
    assert ci._mechanism_tier({}) == 1
    assert ci._mechanism_tier(None) == 1
    assert ci._mechanism_tier({"classic_anomaly": False}) == 2
    # 字符串 "false" 不得被当成 True 以外的东西：只认真正的布尔
    assert ci._mechanism_tier({"classic_anomaly": "false"}) == 1


def test_mechanism_map_stale_entries_not_live(tmp_path):
    ci = _load()
    _write_rule(tmp_path, "testreg_dataset_mechanisms.md", """
{
  "as_of": "2026-01-01", "review_after_days": 30,
  "datasets": [
    {"dataset": "classic_ds", "mechanism": "PEAD", "classic_anomaly": true, "as_of": "2026-10-20"},
    {"dataset": "old_mech", "mechanism": "x", "classic_anomaly": true, "as_of": "2026-01-01"}
  ]
}""")
    res = ci._load_region_mechanisms("TESTREG", root=str(tmp_path))
    assert set(res["live"]) == {"classic_ds"}
    assert set(res["stale"]) == {"old_mech"}
    assert ci._mechanism_tier(res["live"]["classic_ds"]) == 0


def test_usa_real_files_are_complete():
    """真实 USA 文件守卫：条目数、必填字段、无重复 id。

    条数变化时改这里前先确认是「新判死」而不是误删（清单是硬剔除面）。
    """
    ci = _load()
    dead = ci._load_region_dead_list("USA")
    assert dead["warning"] is None
    assert len(dead["entries"]) >= 40
    assert not dead["stale"], f"USA 判死清单有 {len(dead['stale'])} 条过期，需复核"
    for ds, e in dead["entries"].items():
        assert e.get("verdict"), ds
        assert e.get("reason"), ds
        assert e.get("evidence"), ds
        assert e.get("as_of"), ds

    mech = ci._load_region_mechanisms("USA")
    assert mech["warning"] is None
    assert {"insider_agg_matrix", "insider_matrix", "earnings_sent_matrix"} <= set(mech["live"])
    for ds, e in mech["entries"].items():
        assert e.get("mechanism"), ds
        assert isinstance(e.get("classic_anomaly"), bool), ds
        assert e.get("evidence"), ds
        assert e.get("as_of"), ds
