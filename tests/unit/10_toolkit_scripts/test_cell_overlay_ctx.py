# -*- coding: utf-8 -*-
"""2026-10-04 区域 × 类别组合：toolkit CampaignContext.bind_cell 与设置先验的钉住语义。"""
import importlib
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
TOOLKIT_SCRIPTS = REPO_ROOT / "Claude" / "skills" / "wq-brain-campaign-toolkit" / "scripts"


def _lib(name):
    if str(TOOLKIT_SCRIPTS) not in sys.path:
        sys.path.insert(0, str(TOOLKIT_SCRIPTS))
    return importlib.import_module(f"_lib.{name}")


def _campaign(tmp_path, cells):
    d = tmp_path / "KOR"
    (d / "config").mkdir(parents=True)
    (d / "config" / "settings.json").write_text(json.dumps(
        {"region": "KOR", "universe": "TOP600", "neutralization": "STATISTICAL", "decay": 4}), encoding="utf-8")
    (d / "config" / "thresholds.json").write_text(json.dumps({"review": {"turnover_max": 0.7}}), encoding="utf-8")
    (d / "config" / "cells.json").write_text(json.dumps({"region": "KOR", "cells": cells}), encoding="utf-8")
    return d


def _cell():
    return {"fundamental": {
        "status": "auto",
        "backtest": {"overrides": {"decay": 6, "neutralization": "MARKET"},
                     "_evidence": {"decay": "w1", "neutralization": "w2"}},
        "thresholds": {"overrides": {"review.turnover_max": 0.5, "review.sharpe_min": 1.0, "mode_b.sharpe_min": 1.4},
                       "_evidence": {"review.turnover_max": "x", "review.sharpe_min": "y", "mode_b.sharpe_min": "z"}},
    }}


def test_bind_cell_applies_overrides_respects_cli_pins_and_locks(tmp_path, monkeypatch):
    common = _lib("common")
    import wqb.profiles.taxonomy as T
    monkeypatch.setattr(T, "dataset_category", lambda region, ds, db=None: "fundamental")
    ctx = common.CampaignContext(str(_campaign(tmp_path, _cell())))
    logs = []
    applied = ctx.bind_cell("other466", pinned={"neutralization"}, log=logs.append)
    assert applied == {"decay": 6}
    assert ctx.settings["decay"] == 6 and ctx.settings["neutralization"] == "STATISTICAL"   # CLI 钉住的不动
    assert ctx.cell_pinned == {"decay"}
    assert ctx.thresholds["review"]["turnover_max"] == 0.5                                  # 收紧生效
    assert "sharpe_min" not in ctx.thresholds["review"]                                    # 比平台线松：不并
    assert "mode_b" not in ctx.thresholds                                                   # mode_b.* 交给 mode_b_config
    assert any("未生效" in s for s in logs)


def test_bind_cell_is_a_noop_without_cell_or_dataset(tmp_path, monkeypatch):
    common = _lib("common")
    import wqb.profiles.taxonomy as T
    monkeypatch.setattr(T, "dataset_category", lambda region, ds, db=None: "pv")
    ctx = common.CampaignContext(str(_campaign(tmp_path, _cell())))
    before = dict(ctx.settings)
    assert ctx.bind_cell("pv106", log=lambda *_: None) == {} and ctx.settings == before
    assert ctx.bind_cell(None, log=lambda *_: None) == {}


def test_settings_prior_does_not_override_cell_pinned_dims(tmp_path, monkeypatch):
    common = _lib("common")
    region_kb = _lib("region_kb")
    ctx = common.CampaignContext(str(_campaign(tmp_path, {})))
    ctx.cell_pinned = {"decay"}
    monkeypatch.setattr(region_kb, "settings_prior_recommendations", lambda c, cfg=None: [
        {"dim": "decay", "current": 4, "current_rate": 0.01, "current_n": 50, "recommended": 14,
         "rate": 0.3, "n": 60, "lift": 30.0, "source": "gate_priors", "apply": True}])
    applied = region_kb.apply_settings_prior(ctx, pinned=(), cfg={"enabled": True}, log=lambda *_: None)
    assert applied == [] and ctx.settings["decay"] == 4
    ctx.cell_pinned = set()
    applied = region_kb.apply_settings_prior(ctx, pinned=(), cfg={"enabled": True}, log=lambda *_: None)
    assert ctx.settings["decay"] == 14 and len(applied) == 1                                # 反向前提：不钉住时确实会改


def _pipeline_args(**kw):
    import argparse
    base = dict(cmd="run", wave="01A", fresh=True, checkpoint_dir=None, dataset="other466", neutralization=None,
                set=[], no_settings_prior=True, force=False)
    base.update(kw)
    return argparse.Namespace(**base)


def _drive_pipeline_settings(tmp_path, monkeypatch, cells, **kw):
    """跑 pipeline._cmd_main 到 universe 规则闸（让它判死返回 2），看此时 ctx.settings——不发任何仿真。"""
    _lib("common")
    import pipeline
    import wqb.profiles.taxonomy as T
    monkeypatch.setattr(T, "dataset_category", lambda region, ds, db=None: "fundamental")
    monkeypatch.setattr(pipeline, "_neut_query_top", None)
    monkeypatch.setattr(pipeline.rules_mod, "check_universe_lever", lambda ctx, uni: (False, []))
    ctx = pipeline.CampaignContext(str(_campaign(tmp_path, cells)))
    rc = pipeline._cmd_main(_pipeline_args(checkpoint_dir=str(tmp_path / "ck"), **kw), ctx)
    return rc, ctx


def test_pipeline_cli_applies_cell_overrides_but_cli_set_wins(tmp_path, monkeypatch):
    rc, ctx = _drive_pipeline_settings(tmp_path, monkeypatch, _cell(), set=["decay=8"])
    assert rc == 2
    assert ctx.settings["decay"] == 8                       # --set 钉住：组合的 decay 6 不生效
    assert ctx.settings["neutralization"] == "MARKET"       # 组合覆盖生效
    assert ctx.cell_pinned == {"neutralization"}
    assert ctx.thresholds["review"]["turnover_max"] == 0.5


def test_pipeline_cli_without_cell_keeps_region_settings(tmp_path, monkeypatch):
    rc, ctx = _drive_pipeline_settings(tmp_path, monkeypatch, {})
    assert rc == 2
    assert ctx.settings["decay"] == 4 and ctx.settings["neutralization"] == "STATISTICAL"   # 反向前提：无组合即区域值
