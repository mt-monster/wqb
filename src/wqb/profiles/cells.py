# -*- coding: utf-8 -*-
"""区域 × 类别组合（cell）的控制文件：`tracking/<R>/config/cells.json`（2026-10-04）。

一个组合 = 区域 × 平台类别（与「塔」一一对应）。文件只写**覆盖值与本组合的知识**，不复制区域缺省：
没写的项由解析器从 settings.json / thresholds.json / 类别卡 / 全局缺省合成（`$WQ_PY -m wqb.profiles explain`
会逐项写明来源）。

每个组合的键：
  status         "auto"（跟区域 entry_verdict）| active | probe | archived；非 auto 必须写 status_note
  backtest       {"overrides": {设置名: 值}, "_evidence": {设置名: 证据}} —— 进回测的设置覆盖
                 （workflow_batch_track 以 --set 钉住；toolkit CampaignContext.bind_cell 同样生效）
  thresholds     {"overrides": {"review.sharpe_min": 值, "mode_b.sharpe_min": 值, ...}, "_evidence": {...}}
  generation     {"use": [...], "avoid": [...], "skeletons": [{"text","evidence","window_note"}], "notes": [...]}
  s4             {"levers": [{"id","what","evidence","no_extrapolate"}], "avoid": [{"what","evidence"}]}
  evidence       由 `sync-cells` 从数据库只读汇总后写入（回测数、RA 全过、prod、判死 / 胜绩条目），勿手改
每个覆盖值都必须在 `_evidence` 里写证据（波号 / alpha id / 日期）——没有证据的覆盖校验不通过。
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional

from .locked import check_threshold_override, nonstandard_windows, recommends_weighted_mix
from .taxonomy import CARD_OF, normalize_category

CELLS_FILE = "cells.json"
SCHEMA_VERSION = 1

#: 组合可覆盖的仿真设置（与平台 simulation settings 字段同名）
BACKTEST_KEYS = ("universe", "delay", "neutralization", "decay", "truncation",
                 "nanHandling", "maxTrade", "pasteurization", "unitHandling")
#: 组合可覆盖的阈值键前缀（点分：<thresholds.json 节>.<键>，mode_b.* 交给 mode_b_config）
THRESHOLD_PREFIXES = ("review.", "near.", "mode_b.", "gates.", "diversity.")
#: flow = 本组合与主流程的**控制流**差异（新步骤 / 新工具 / 新停止规则），只有它非空才可能被判「够格拆 skill」
CELL_KEYS = {"status", "status_note", "datasets", "backtest", "thresholds", "generation", "s4", "evidence",
             "note", "flow"}
STATUS_VALUES = ("auto", "active", "probe", "archived")


def config_dir_of(region: str, root: Optional[Path] = None) -> Path:
    if root is None:
        from wqb.config import REPO_ROOT
        root = REPO_ROOT
    return Path(root) / "tracking" / region.upper() / "config"


def cells_path(region: str, config_dir: Optional[Path] = None) -> Path:
    return Path(config_dir or config_dir_of(region)) / CELLS_FILE


def load_cells(region: str, config_dir: Optional[Path] = None) -> Dict[str, Any]:
    """读组合文件；不存在返回空骨架（不报错——没有组合 = 全部跟区域）。"""
    p = cells_path(region, config_dir)
    if not p.exists():
        return {"schema_version": SCHEMA_VERSION, "region": region.upper(), "cells": {}}
    return json.loads(p.read_text(encoding="utf-8-sig"))


def save_cells(region: str, data: Dict[str, Any], config_dir: Optional[Path] = None) -> Path:
    p = cells_path(region, config_dir)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(data, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    return p


def cell_for(region: str, category: Optional[object], config_dir: Optional[Path] = None) -> Dict[str, Any]:
    if not category:
        return {}
    return (load_cells(region, config_dir).get("cells") or {}).get(normalize_category(category)) or {}


def cell_backtest_overrides(region: str, category: Optional[object],
                            config_dir: Optional[Path] = None) -> Dict[str, Any]:
    c = cell_for(region, category, config_dir)
    return dict(((c.get("backtest") or {}).get("overrides")) or {})


def cell_threshold_overrides(region: str, category: Optional[object],
                             config_dir: Optional[Path] = None) -> Dict[str, Any]:
    c = cell_for(region, category, config_dir)
    return dict(((c.get("thresholds") or {}).get("overrides")) or {})


def _legal_settings(region: str) -> Dict[str, List[Any]]:
    from wqb.config import REGIONS
    r = REGIONS.get(region.upper()) or {}
    return {"universe": list(r.get("universes") or []), "delay": list(r.get("delays") or []),
            "neutralization": list(r.get("neutralizations") or [])}


def validate_cells(region: str, data: Dict[str, Any]) -> List[str]:
    """返回错误列表（空 = 合法）。"""
    errs: List[str] = []
    reg = region.upper()
    if str(data.get("region") or "").upper() != reg:
        errs.append(f"region 字段 {data.get('region')!r} ≠ {reg}")
    legal = _legal_settings(reg)
    for cat, body in (data.get("cells") or {}).items():
        where = f"{reg}/{cat}"
        if cat != normalize_category(cat) or cat not in CARD_OF:
            errs.append(f"{where}: 类别键必须是小写平台类别（taxonomy.CARD_OF 里的键）")
        extra = set(body) - CELL_KEYS
        if extra:
            errs.append(f"{where}: 未知键 {sorted(extra)}")
        status = body.get("status", "auto")
        if status not in STATUS_VALUES:
            errs.append(f"{where}: status 只能是 {STATUS_VALUES}")
        elif status != "auto" and not body.get("status_note"):
            errs.append(f"{where}: status={status} 必须写 status_note（为什么不跟区域）")
        bt = body.get("backtest") or {}
        bt_ov, bt_ev = bt.get("overrides") or {}, bt.get("_evidence") or {}
        for k, v in bt_ov.items():
            if k not in BACKTEST_KEYS:
                errs.append(f"{where}.backtest: 不可覆盖的设置 {k}（可覆盖：{BACKTEST_KEYS}）")
                continue
            if not str(bt_ev.get(k) or "").strip():
                errs.append(f"{where}.backtest.{k}: 覆盖没有 _evidence")
            if k in legal and legal[k] and v not in legal[k]:
                errs.append(f"{where}.backtest.{k}={v!r} 不在本区合法档 {legal[k]}（config.REGIONS）")
        th = body.get("thresholds") or {}
        th_ov, th_ev = th.get("overrides") or {}, th.get("_evidence") or {}
        for k, v in th_ov.items():
            if not k.startswith(THRESHOLD_PREFIXES):
                errs.append(f"{where}.thresholds: 键 {k} 不在可覆盖前缀 {THRESHOLD_PREFIXES}")
            if not str(th_ev.get(k) or "").strip():
                errs.append(f"{where}.thresholds.{k}: 覆盖没有 _evidence")
            why = check_threshold_override(k, v)
            if why:
                errs.append(f"{where}.thresholds: {why}")
        gen = body.get("generation") or {}
        for text in list(gen.get("use") or []) + [s.get("text", "") for s in gen.get("skeletons") or []]:
            if recommends_weighted_mix(str(text)):
                errs.append(f"{where}.generation 推荐了加权混合: {str(text)[:60]}")
        for s in gen.get("skeletons") or []:
            if not s.get("evidence"):
                errs.append(f"{where}.generation.skeletons: 骨架缺 evidence: {str(s.get('text'))[:50]}")
            bad = nonstandard_windows(str(s.get("text")))
            if bad and not s.get("window_note"):
                errs.append(f"{where}.generation.skeletons: 非白名单窗口 {bad} 需 window_note（解释 + 实测证据）")
        for lv in (body.get("s4") or {}).get("levers") or []:
            if not lv.get("what") or not lv.get("evidence"):
                errs.append(f"{where}.s4.levers: 杠杆缺 what / evidence")
            if recommends_weighted_mix(str(lv.get("what"))):
                errs.append(f"{where}.s4.levers 推荐了加权混合: {str(lv.get('what'))[:60]}")
    return errs
