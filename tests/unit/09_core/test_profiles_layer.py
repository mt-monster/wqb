# -*- coding: utf-8 -*-
"""wqb.profiles（2026-10-04 区域 × 类别拆分）：口径、锁定表、类别卡、组合文件、解析器、证据同步、渲染结构。

全部用临时目录 / 临时 sqlite，不读生产库；读仓库里真实的类别卡、cells.json 与区域 skill 只做契约校验。
"""
import importlib.util
import json
import sqlite3
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[3]

from wqb.profiles import cards as C  # noqa: E402
from wqb.profiles import cells as CE  # noqa: E402
from wqb.profiles import evidence as EV  # noqa: E402
from wqb.profiles import locked as L  # noqa: E402
from wqb.profiles import render as R  # noqa: E402
from wqb.profiles import resolver as RS  # noqa: E402
from wqb.profiles import taxonomy as T  # noqa: E402


# ---------------------------------------------------------------- 口径

def test_taxonomy_normalizes_and_maps_cards():
    assert T.normalize_category("MODEL") == "model"
    assert T.normalize_category(None) == "unknown"
    assert T.normalize_category({"id": "Pv"}) == "pv"
    assert T.card_of("imbalance") == "pv" and T.card_of("socialmedia") == "sentiment"
    assert T.card_of("broker") == "other" and T.card_of("nonexistent") == "other"
    assert T.group_of("sentiment") == "News-Sentiment"
    assert "pattern" in T.FAMILY_TAGS and "pattern" not in T.CARD_OF  # Pattern 是族标签，不是平台类别


def test_abbreviation_expansion_used_for_dead_end_binding():
    assert T.expand_abbrev("FND93") == "fundamental93"
    assert T.expand_abbrev("RSK70") == "risk70"
    assert T.expand_abbrev("SI5") == "shortinterest5"
    assert T.expand_abbrev("WAVE97") is None


# ---------------------------------------------------------------- 锁定表

@pytest.mark.parametrize("text,hit", [
    ("0.4*rank(A) + 0.6*rank(B)", True),
    ("add(multiply(0.4, rank(a)), multiply(0.6, rank(b)))", True),
    ("add(rank(x), rank(y))", True),
    ("add(multiply(rank(ts_delta(vec_avg(e),63)),0.6), multiply(rank(f),0.4))", True),   # 权重后置也算
    ("multiply(rank(ts_backfill(x, 66)), 0.4)", True),
    ("trade_when(rank(adv20) > 0.5, rank(x), -1)", False),
    ("group_rank(divide(subtract(P, ts_mean(P, 252)), add(abs(ts_mean(P, 252)), 1)), bucket(rank(cap)))", False),
])
def test_weighted_mix_detector(text, hit):
    assert L.recommends_weighted_mix(text) is hit


def test_nonstandard_windows_and_platform_bounds():
    assert L.nonstandard_windows("ts_corr(a, b, 42)") == [42]
    assert L.nonstandard_windows("ts_rank(group_rank(x, market), 504)") == []
    assert L.check_threshold_override("review.sharpe_min", 1.0)          # 比平台 LOW_SHARPE 线松
    assert L.check_threshold_override("review.turnover_max", 0.9)       # 超出平台换手上限
    assert L.check_threshold_override("review.sharpe_min", 1.7) is None
    assert L.check_threshold_override("d0p.prod_expand_max", 0.65)      # D0-P 不可改写


# ---------------------------------------------------------------- 类别卡

def test_real_category_cards_are_valid():
    assert C.validate_cards(C.load_cards()) == []


def _gem_dicts():
    p = ROOT / "Claude/skills/brain-make-some-gem/scripts/trailSomeAlphas/economic_priors.py"
    spec = importlib.util.spec_from_file_location("_gem_ep_for_cards", p)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    # CATEGORY_FORBIDDEN 是并行会话新加的字典，提交前的 GEM 没有它——缺了就只核对原语
    return m.CATEGORY_PRIMITIVES, getattr(m, "CATEGORY_FORBIDDEN", {})


def test_cards_preserve_every_gem_primitive_and_forbidden_item():
    """类别知识从 GEM 字典迁进卡片后不得丢条目（GEM 改读卡片之前，两份内容靠这条守住）。"""
    prims, forb = _gem_dicts()
    cards = C.load_cards()["cards"]
    glob = set(L.GLOBAL_FORBIDDEN)
    missing = []
    for cat, items in prims.items():
        have = set(cards[T.card_of(cat)].get("primitives") or [])
        missing += [f"{cat}.primitives: {x}" for x in items if x not in have]
    for cat, items in forb.items():
        have = set(cards[T.card_of(cat)].get("forbidden") or []) | glob
        missing += [f"{cat}.forbidden: {x}" for x in items if x not in have]
    assert not missing, "GEM 类别知识在卡片里丢了：\n" + "\n".join(missing)


def test_card_validator_rejects_single_region_claims_and_bad_windows():
    bad = {"cards": {"pv": {"title": "t", "group": "PV", "windows": {"d": [42]},
                            "cross_region": [{"id": "x", "what": "w", "regions": ["KOR"], "evidence": "e"}]}}}
    errs = C.validate_cards(bad)
    assert any("非白名单窗口" in e for e in errs)
    assert any("≥2 个区" in e for e in errs)


# ---------------------------------------------------------------- 组合文件

def _cells(region="KOR", **cell):
    return {"region": region, "cells": {"fundamental": dict({"status": "auto"}, **cell)}}


def test_cell_validator_requires_evidence_and_legal_settings():
    assert CE.validate_cells("KOR", _cells()) == []
    errs = CE.validate_cells("KOR", _cells(backtest={"overrides": {"decay": 6}}))
    assert any("_evidence" in e for e in errs)
    errs = CE.validate_cells("KOR", _cells(backtest={"overrides": {"universe": "TOP3000"},
                                                     "_evidence": {"universe": "x"}}))
    assert any("合法档" in e for e in errs)
    errs = CE.validate_cells("KOR", _cells(status="active"))
    assert any("status_note" in e for e in errs)
    errs = CE.validate_cells("KOR", _cells(generation={"skeletons": [
        {"text": "add(rank(a), rank(b))", "evidence": "w1"}]}))
    assert any("加权混合" in e for e in errs)
    errs = CE.validate_cells("KOR", _cells(thresholds={"overrides": {"review.sharpe_min": 1.0},
                                                       "_evidence": {"review.sharpe_min": "x"}}))
    assert any("平台线" in e for e in errs)


def test_real_cells_files_are_valid():
    bad = []
    for p in sorted((ROOT / "tracking").glob("*/config/cells.json")):
        region = p.parent.parent.name
        bad += [f"{region}: {e}" for e in CE.validate_cells(region, json.loads(p.read_text(encoding="utf-8")))]
    assert not bad, "\n".join(bad)


# ---------------------------------------------------------------- 解析器

@pytest.fixture
def campaign(tmp_path, monkeypatch):
    cfg = tmp_path / "KOR" / "config"
    cfg.mkdir(parents=True)
    (cfg / "settings.json").write_text(json.dumps(
        {"region": "KOR", "universe": "TOP600", "delay": 1, "neutralization": "STATISTICAL", "decay": 4}),
        encoding="utf-8")
    (cfg / "thresholds.json").write_text(json.dumps(
        {"review": {"sharpe_min": 1.58, "turnover_max": 0.7}, "mode_b_qualification": {"$ref": "GLOBAL/x"}}),
        encoding="utf-8")
    (cfg / "cells.json").write_text(json.dumps({"region": "KOR", "cells": {"fundamental": {
        "status": "auto",
        "backtest": {"overrides": {"decay": 6}, "_evidence": {"decay": "w1 实测"}},
        "thresholds": {"overrides": {"review.sharpe_min": 1.0, "review.turnover_max": 0.5,
                                     "mode_b.sharpe_min": 1.1, "mode_b.fitness_min": 0.9},
                       "_evidence": {"review.sharpe_min": "x", "review.turnover_max": "y",
                                     "mode_b.sharpe_min": "z", "mode_b.fitness_min": "z"}},
        "s4": {"levers": [{"id": "l1", "what": "换分母", "evidence": "e", "no_extrapolate": True}]},
    }}}), encoding="utf-8")
    from wqb.workflow import mode_b_config as M
    monkeypatch.setattr(M, "_thresholds_path", lambda region: str(cfg / "thresholds.json"))
    monkeypatch.setenv("WQB_DB_PATH", str(tmp_path / "absent.db"))
    return cfg


def test_resolver_layers_sources_and_locks(campaign):
    p = RS.resolve("KOR", category="fundamental", config_dir=campaign)
    assert p["backtest"]["decay"] == {"value": 6, "source": "cells.json:fundamental", "evidence": "w1 实测",
                                       "region_value": 4}
    assert p["backtest"]["universe"]["source"] == "settings.json"
    assert p["thresholds"]["review.turnover_max"]["value"] == 0.5             # 收紧：生效
    assert p["thresholds"]["review.sharpe_min"]["value"] == 1.58             # 比平台线松：不生效
    assert any("review.sharpe_min" in v for v in p["violations"])
    # Mode B：组合想把 sharpe 降到 1.1 → 被下限钳回；fitness 提到 0.9 → 生效
    assert p["mode_b"]["sharpe_min"] == 1.25 and p["mode_b"]["fitness_min"] == 0.9
    assert p["mode_b"]["clamped_from"] == {"sharpe_min": 1.1}
    assert p["s4"]["levers"][0]["scope"] == "组合"
    assert "mode_b_floor" in p["locks"] and "mixed_signal_ban" in p["locks"]
    assert "禁止两条独立信号腿相加" in p["generation"]["global_forbidden"][0]
    assert "== 生效画像" in RS.explain_text(p)


def test_backtest_pins_only_carry_cell_overrides(campaign, monkeypatch):
    assert RS.backtest_pins("KOR", category="fundamental", config_dir=campaign) == ["decay=6"]
    assert RS.backtest_pins("KOR", category="pv", config_dir=campaign) == []
    monkeypatch.setattr(T, "dataset_category", lambda region, ds, db=None: "fundamental")
    monkeypatch.setattr(RS, "dataset_category", lambda region, ds, db=None: "fundamental")
    assert RS.backtest_pins("KOR", dataset="other466", config_dir=campaign) == ["decay=6"]


def test_batch_track_pins_cell_overrides_with_set(campaign, monkeypatch):
    from wqb.workflow.nodes import batch_track as BT
    monkeypatch.setattr(RS, "dataset_category", lambda region, ds, db=None: "fundamental")
    pins, warn = BT._cell_backtest_pins("KOR", "other466", str(campaign.parent))
    assert pins == ["decay=6"] and warn is None
    src = (ROOT / "src/wqb/workflow/nodes/batch_track.py").read_text(encoding="utf-8")
    assert 'cmd += ["--set", kv]' in src


# ---------------------------------------------------------------- 证据同步（临时库）

def _mini_db(path: Path):
    con = sqlite3.connect(str(path))
    con.executescript("""
    CREATE TABLE regions(id INTEGER PRIMARY KEY, name TEXT);
    CREATE TABLE datasets(id INTEGER PRIMARY KEY, name TEXT, region_id INTEGER, category TEXT);
    CREATE TABLE backtest_results(id INTEGER PRIMARY KEY, region TEXT, dataset TEXT, sharpe REAL, fitness REAL,
                                  ra_failed_checks TEXT);
    CREATE TABLE alphas(id INTEGER PRIMARY KEY, region_id INTEGER, dataset_id INTEGER, prod_correlation REAL);
    CREATE TABLE registry_empirical(id INTEGER PRIMARY KEY, region TEXT, layer TEXT, entry_id TEXT, family TEXT,
                                    payload TEXT);
    CREATE TABLE ledger_kv(region TEXT, key TEXT, value TEXT);
    INSERT INTO regions VALUES (1, 'KOR'), (2, 'USA');
    INSERT INTO datasets VALUES (1, 'other466', 1, 'FUNDAMENTAL'), (2, 'pv106', 1, 'PV'),
                                (3, 'fundamental93', 1, NULL), (4, 'fundamental93', 2, 'FUNDAMENTAL');
    """)
    rows = [("KOR", "other466", 2.0, 1.2, "[]")] * 25 + [("KOR", "other466", 1.0, 0.5, "[]")] * 5 \
        + [("KOR", "pv106", 0.5, 0.3, '["LOW_SHARPE"]')] * 3 + [("KOR", None, 2.0, 2.0, "[]")] * 4
    con.executemany("INSERT INTO backtest_results(region, dataset, sharpe, fitness, ra_failed_checks) VALUES (?,?,?,?,?)", rows)
    con.executemany("INSERT INTO alphas(region_id, dataset_id, prod_correlation) VALUES (?,?,?)",
                    [(1, 1, 0.65), (1, 1, 0.82)])
    con.executemany("INSERT INTO registry_empirical(region, layer, entry_id, family, payload) VALUES (?,?,?,?,?)", [
        ("KOR", "dead_end", "KOR-FND93-ACCRUALS-DEAD", "fnd93", json.dumps({"rule": "别再挖应计"})),
        ("KOR", "dead_end", "KOR-PV106-LIQUIDITY-WEAK", "", json.dumps({"rule": "流动性天花板"})),
        ("KOR", "win", "KOR-OTHER466-WIN", "other466", json.dumps({"dataset": "other466", "key": "quantile"})),
        ("KOR", "dead_end", "KOR-NEWS-SENT-DEAD", "x", json.dumps({"rule": "r"})),
        ("KOR", "dead_end", "KOR-WAVE99-XXX-DEAD", "x", json.dumps({"rule": "r"})),
    ])
    con.commit()
    con.close()


def test_evidence_stats_binding_and_sync(tmp_path):
    db = tmp_path / "mini.db"
    _mini_db(db)
    st = EV.region_stats("KOR", db=str(db))
    assert st["fundamental"]["backtests"] == 30 and st["fundamental"]["ra_clean"] == 25
    assert st["fundamental"]["prod_measured"] == 2 and st["fundamental"]["prod_clean"] == 1
    assert st["unknown"]["backtests"] == 4                                   # 没写数据集的回测行不并进组合
    ents = {e["id"]: e for e in EV.registry_entries("KOR", db=str(db))}
    assert ents["KOR-OTHER466-WIN"]["bound"] == "payload" and ents["KOR-OTHER466-WIN"]["category"] == "fundamental"
    assert ents["KOR-FND93-ACCRUALS-DEAD"]["dataset"] == "fundamental93"     # 缩写推断 + 本区空类别借别区
    assert ents["KOR-FND93-ACCRUALS-DEAD"]["category"] == "fundamental"
    assert ents["KOR-PV106-LIQUIDITY-WEAK"]["bound"] == "inferred"
    assert ents["KOR-NEWS-SENT-DEAD"]["bound"] == "keyword" and ents["KOR-NEWS-SENT-DEAD"]["category"] == "news"
    assert ents["KOR-WAVE99-XXX-DEAD"]["bound"] == "unbound"

    cfg = tmp_path / "KOR" / "config"
    cfg.mkdir(parents=True)
    CE.save_cells("KOR", {"region": "KOR", "cells": {"fundamental": {
        "status": "auto", "s4": {"levers": [{"id": "x", "what": "人写的杠杆", "evidence": "e"}]}}}}, cfg)
    s = EV.sync_cells("KOR", db=str(db), config_dir=cfg, apply=True, min_backtests=20, today="2026-10-04")
    data = CE.load_cells("KOR", cfg)
    assert set(s["cells"]) == {"fundamental", "pv", "news"} and "unknown" not in data["cells"]
    assert data["cells"]["fundamental"]["s4"]["levers"][0]["what"] == "人写的杠杆"   # 人写字段不被覆盖
    assert data["cells"]["fundamental"]["evidence"]["wins"][0]["id"] == "KOR-OTHER466-WIN"
    assert data["unbound_registry_entries"] == 1 and data["unattributed_backtests"] == 4
    assert CE.validate_cells("KOR", data) == []


# ---------------------------------------------------------------- 区域 skill（结构）

def test_region_skills_exist_and_match_cells_and_settings():
    problems = R.check_structure()
    assert not problems, "区域 skill / 组合分支文件与控制文件不一致（跑 $WQ_PY -m wqb.profiles render --apply）：\n" \
        + "\n".join(problems)


def test_config_fallbacks_agree_with_existing_campaign_settings():
    """config.REGIONS 的 default_neutralization / default_universe 只给「新建战役目录」兜底；
    已有 settings.json 的区，兜底值与它不一致就会让新建 / 重建的目录静默换档（2026-10-04 收口两张字面量表时加）。"""
    import json
    from wqb.config import REGIONS
    root = Path(__file__).resolve().parents[3]
    bad = []
    for r, cfg in REGIONS.items():
        p = root / "tracking" / r / "config" / "settings.json"
        if not p.exists():
            continue
        s = json.loads(p.read_text(encoding="utf-8"))
        if "default_neutralization" in cfg and s.get("neutralization") != cfg["default_neutralization"]:
            bad.append(f"{r}.neutralization settings={s.get('neutralization')} config={cfg['default_neutralization']}")
        if s.get("universe") not in cfg["universes"]:
            bad.append(f"{r}.universe settings={s.get('universe')} 不在 config.REGIONS[{r}].universes")
    assert not bad, bad
