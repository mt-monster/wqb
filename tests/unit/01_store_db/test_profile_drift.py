# -*- coding: utf-8 -*-
"""profile 漂移检测机制（2026-10-01，region-profile-contract.md §5）的回归护栏。

覆盖三层：
  * `wqb.region_profile` 解析器（新结构化形态 + 真实 14 个 profile 全量可解析）
  * `wqb.profile_drift.check_profile_drift`（集合判定：green_but_dead / red_but_won /
    unknown_dataset_ref / dead_not_listed / win_not_listed / stale / unbound）
  * `upsert_registry_empirical` 的回写钩子（win/dead_end 触发、fail-open、落 ledger）
"""
import importlib
import json
import sqlite3
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[3]
for _p in (REPO, REPO / "src", REPO / "tools"):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

from wqb import profile_drift as PD  # noqa: E402
from wqb import region_profile as RP  # noqa: E402
from wqb.store import CampaignStore  # noqa: E402


# ----------------------------------------------------------------------------- 解析器

PROFILE_TEXT = """---
region: TST
entry_verdict: active
one_liner: "测试 profile"
static:
  universe: [TOP600]
  universe_default: TOP600
datasets:
  red:
    - datasets: [model109, model170]
      reason: "已判死（实证）"
    - scope: family
      families: [chart_patterns, ai_ml]
      reason: "3 连死"
  green:
    - datasets: [other466]
      note: "win 实证绑定"
  yellow: [model264]
priors:
  signal_families_exclude: [chart_pattern]
gate_overrides:
  cw_gate: FAIL
loop_policy:
  max_probes_per_wave: 1
empirical_anchor:
  dead_ends_ref: "get_dead_ends(TST)"
  last_verified: 2026-09-01
---

# TST 正文
"""


def test_parser_reads_structured_datasets_block():
    fm = RP.parse_front_matter(PROFILE_TEXT)
    ds = fm["datasets"]
    assert ds["red"][0]["datasets"] == ["model109", "model170"]
    assert ds["red"][0]["reason"] == "已判死（实证）"
    assert ds["red"][1]["scope"] == "family" and ds["red"][1]["families"] == ["chart_patterns", "ai_ml"]
    assert ds["green"][0]["datasets"] == ["other466"] and ds["green"][0]["note"] == "win 实证绑定"
    assert ds["yellow"] == ["model264"]
    assert fm["empirical_anchor"]["last_verified"] == "2026-09-01"


def test_parser_handles_quoted_commas_and_inline_comments():
    text = ("---\nregion: TST\ndatasets:\n"
            "  green: []   # 动态：绿榜 = analyst 系（评级/预期）\n"
            "  red: [\"a, b 家族\", c]\n---\n")
    fm = RP.parse_front_matter(text)
    assert fm["datasets"]["green"] == []
    assert fm["datasets"]["red"] == ["a, b 家族", "c"]


def test_parser_tolerates_legacy_inline_form_as_family_entries(tmp_path):
    """旧文本形态（迁移漏网）不解析崩，按族级保留原文——精确性由迁移保证，不是靠猜。"""
    (tmp_path / "TST.md").write_text(
        "---\nregion: TST\nentry_verdict: active\ndatasets:\n"
        "  red: [chart_patterns, news_sentiment]\n"
        "  red_reason: \"3 连死\"\n"
        "  green: [analyst 系（评级/预期）, insiders, pv]\n"
        "empirical_anchor:\n  last_verified: 2026-08-25\n---\n",
        encoding="utf-8")
    prof = RP.load_profile("TST", tmp_path)
    assert prof is not None
    assert prof.dataset_refs() == {"green": [], "red": []}            # 旧形态没有精确层
    assert [f for e in prof.red for f in e.families] == ["chart_patterns", "news_sentiment"]
    assert all(e.scope == "family" for e in prof.green)


@pytest.mark.parametrize("path", sorted(RP.PROFILE_DIR.glob("*.md")), ids=lambda p: p.stem)
def test_all_real_profiles_parse(path):
    """全部真实 profile 必须可被唯一解析器读懂（9 键齐全、verdict 枚举——与契约测试同口径）。"""
    fm = RP.parse_front_matter(path.read_text(encoding="utf-8"))
    for k in ("region", "entry_verdict", "one_liner", "static", "datasets",
              "priors", "gate_overrides", "loop_policy", "empirical_anchor"):
        assert k in fm, f"{path.name} 缺键 {k}"
    assert fm["region"] == path.stem
    assert fm["entry_verdict"] in ("active", "probe-only", "frozen")
    prof = RP.load_profile(path.stem, path.parent)
    assert prof is not None and prof.last_verified


def test_split_dataset_refs_normalizes_composites():
    assert PD.split_dataset_refs("predictive_starmine × news73") == ["predictive_starmine", "news73"]
    assert PD.split_dataset_refs("a+b") == ["a", "b"]
    assert PD.split_dataset_refs("other47 (SEMrush)") == ["other47"]
    assert PD.split_dataset_refs(["model109_x", None, "OTHER466"]) == ["model109_x", "other466"]
    assert PD.split_dataset_refs({"not": "a str"}) == []


# ----------------------------------------------------------------------------- 漂移判定

@pytest.fixture
def conn(tmp_path):
    db = tmp_path / "wqb.db"
    CampaignStore(str(db)).close()
    c = sqlite3.connect(str(db))
    c.row_factory = sqlite3.Row
    yield c
    c.close()


@pytest.fixture
def profile_dir(tmp_path):
    d = tmp_path / "profiles"
    d.mkdir()
    (d / "TST.md").write_text(PROFILE_TEXT, encoding="utf-8")
    return d


def _insert_dataset(conn, region, name):
    rid = conn.execute("INSERT OR IGNORE INTO regions (name) VALUES (?) RETURNING id", (region,)).fetchone()
    if rid is None:
        rid = conn.execute("SELECT id FROM regions WHERE name=?", (region,)).fetchone()
    conn.execute("INSERT INTO datasets (name, region_id) VALUES (?,?)", (name, rid[0]))


def _upsert_reg(conn, region, layer, entry_id, dataset=None, updated_at="2026-09-30T00:00:00"):
    payload = {"id": entry_id}
    if dataset:
        payload["dataset"] = dataset
    conn.execute(
        "INSERT OR REPLACE INTO registry_empirical (region, layer, entry_id, payload, updated_at) "
        "VALUES (?,?,?,?,?)",
        (region, layer, entry_id, json.dumps(payload, ensure_ascii=False), updated_at))


def test_drift_detects_conflict_gap_opportunity_and_stale(conn, profile_dir):
    # profile 形态：red=[model109, model170]，green=[other466]
    for ds in ("model109", "model170", "other466", "analyst10"):
        _insert_dataset(conn, "TST", ds)
    # ledger 整集判死 other466，却在 green → green_but_dead（high）
    conn.execute("INSERT INTO ledger_kv (region, key, value, updated_at) VALUES ('TST','other466_dead','{}','2026-09-29')")
    # ledger 整集判死 model999，profile 未收录 → dead_not_listed（medium）
    conn.execute("INSERT INTO ledger_kv (region, key, value, updated_at) VALUES ('TST','model999_dead','{}','2026-09-28')")
    # registry 族级判死：model170 已被 red 收录（一致态）；analyst10 只进 family_dead 汇总计数
    _upsert_reg(conn, "TST", "dead_end", "TST-M170-FAM-DEAD", dataset="model170")
    _upsert_reg(conn, "TST", "dead_end", "TST-ANL10-FAM-DEAD", dataset="analyst10")
    # 一条 win 无 dataset 绑定 → unbound +1
    _upsert_reg(conn, "TST", "win", "TST-UNBOUND-WIN", dataset=None)
    conn.commit()

    rep = PD.check_profile_drift(conn, "TST", profile_dir)
    kinds = {(f["kind"], f["dataset"]) for f in rep["findings"]}
    assert ("green_but_dead", "other466") in kinds
    assert ("dead_not_listed", "model999") in kinds
    # 族级死不构成 per-dataset finding（model170 已被 red 收录；analyst10 只进汇总计数）
    assert not any(ds in ("model170", "analyst10") for _, ds in kinds)
    assert rep["summary"]["family_dead_datasets"] == ["analyst10", "model170"]
    assert rep["needs_refresh"] is True
    assert rep["summary"]["high"] == 1 and rep["summary"]["unbound_entries"] == 1
    # stale：last_verified 2026-09-01 < 最近回写 2026-09-30
    assert any(f["kind"] == "stale_last_verified" for f in rep["findings"])


def test_drift_flags_red_but_won_and_unknown_refs(conn, profile_dir):
    _insert_dataset(conn, "TST", "model109")
    _upsert_reg(conn, "TST", "win", "TST-M109-WIN", dataset="model109")      # red 收录却有胜绩
    rep = PD.check_profile_drift(conn, "TST", profile_dir)
    kinds = {(f["kind"], f["dataset"]) for f in rep["findings"]}
    assert ("red_but_won", "model109") in kinds
    assert ("unknown_dataset_ref", "other466") in kinds                       # green 引用了未同步的 id
    assert rep["needs_refresh"] is True


def test_drift_clean_when_consistent(conn, tmp_path):
    d = tmp_path / "profiles"
    d.mkdir()
    (d / "TST.md").write_text(PROFILE_TEXT.replace("[model109, model170]", "[model109]"),
                              encoding="utf-8")
    for ds in ("model109", "other466"):
        _insert_dataset(conn, "TST", ds)
    _upsert_reg(conn, "TST", "dead_end", "TST-M109-DEAD", dataset="model109")
    _upsert_reg(conn, "TST", "win", "TST-O466-WIN", dataset="other466", updated_at="2026-08-30T00:00:00")
    rep = PD.check_profile_drift(conn, "TST", d)
    highs = [f for f in rep["findings"] if f["severity"] == "high"]
    assert highs == [] and rep["needs_refresh"] is False


def test_drift_missing_profile_is_not_an_error(conn):
    rep = PD.check_profile_drift(conn, "ZZZ", Path("/nonexistent"))
    assert rep["profile"] == "missing" and rep["needs_refresh"] is False


# ----------------------------------------------------------------------------- 回写钩子

@pytest.fixture
def mcp(tmp_path, monkeypatch):
    db_path = tmp_path / "wqb.db"
    CampaignStore(str(db_path)).close()
    sys.modules.pop("wqb_db_mcp", None)
    mod = importlib.import_module("wqb_db_mcp")
    mod.set_db_path(db_path)        # 读写同源；隔离失效由 get_db_path() 的结果闸兜住
    return mod


def test_hook_fires_on_win_and_dead_end_but_not_campaign(mcp):
    out = mcp.upsert_registry_empirical(
        region="ZZZ", layer="win", entry_id="ZZZ-W1", payload={"id": "ZZZ-W1", "what": "w", "key": "k"})
    assert out["action"] == "inserted" and "profile_drift" in out
    assert out["profile_drift"]["needs_refresh"] is False                  # 无 profile → 无冲突
    assert "无 profile" in out["profile_drift"]["hint"]
    # 幂等落 ledger
    rep = mcp.get_ledger_key("ZZZ", "profile_drift")
    assert rep["trigger"] == {"layer": "win", "entry_id": "ZZZ-W1"} and rep["checked_at"]

    out2 = mcp.upsert_registry_empirical(
        region="ZZZ", layer="dead_end", entry_id="ZZZ-D1",
        payload={"id": "ZZZ-D1", "family": "f", "reason": "r", "rule": "u"})
    assert out2["profile_drift"]["needs_refresh"] is False

    out3 = mcp.upsert_registry_empirical(
        region="ZZZ", layer="campaign", entry_id="model219", payload={"status": "untried"})
    assert "profile_drift" not in out3                                    # 不影响 green/red 的层不触发


def test_hook_is_fail_open(mcp, monkeypatch):
    import wqb.profile_drift as pd_mod
    monkeypatch.setattr(pd_mod, "check_profile_drift",
                        lambda *a, **k: (_ for _ in ()).throw(RuntimeError("boom")))
    out = mcp.upsert_registry_empirical(
        region="ZZZ", layer="win", entry_id="ZZZ-W2", payload={"id": "ZZZ-W2", "what": "w", "key": "k"})
    assert out["action"] == "inserted"                                    # 回写本体成功
    assert "boom" in out["profile_drift"]["error"]                        # 漂移检查失败只降级为提示
