# -*- coding: utf-8 -*-
"""生效画像解析器：区域 × 类别组合在每一步实际用到的设置 / 阈值 / 生成与改进要点（2026-10-04）。

合成顺序（后者覆盖前者，锁定表最后兜底）：
  全局缺省（config / 类别卡 global）→ 类别卡 → 区域（settings.json / thresholds.json / profile）
  → 组合（cells.json）→ 锁定表（`locked.py`；Mode B 下限由 mode_b_config 执行）
每个值都带 `source`（来自哪一层、哪个文件 / 键），`$WQ_PY -m wqb.profiles explain` 把它打印出来。

本模块只读：不写库、不改文件、不发请求。
"""
from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any, Dict, List, Optional

from . import cards as _cards
from .cells import cell_for, config_dir_of, validate_cells, load_cells
from .locked import GLOBAL_FORBIDDEN, LOCKED, check_threshold_override
from .taxonomy import card_of, dataset_category, group_of, normalize_category

#: explain 里展示的区域阈值节（S4 / S5 判定用；S0 的 dataset_health 不随组合变化）
THRESHOLD_SECTIONS = ("review", "near", "gates", "diversity")


class _ReadonlyLedger:
    """只读台账（Mode B 下限 / 区域自适应值）；库不存在或读失败一律返回 None。"""

    def __init__(self, db: Optional[str] = None):
        from wqb.db_conn import default_db_path
        self.db = db or default_db_path()

    def get_ledger(self, region: str, key: str):
        if not os.path.isfile(self.db):
            return None
        try:
            from wqb.db_conn import connect
            conn = connect(self.db, readonly=True, timeout=5.0)
            try:
                row = conn.execute("SELECT value FROM ledger_kv WHERE region=? AND key=?", (region, key)).fetchone()
            finally:
                conn.close()
            return json.loads(row[0]) if row else None
        except Exception:  # noqa: BLE001
            return None


def _read_json(p: Path) -> Dict[str, Any]:
    try:
        return json.loads(p.read_text(encoding="utf-8-sig"))
    except FileNotFoundError:
        return {}


def _flatten(d: Dict[str, Any], prefix: str = "") -> Dict[str, Any]:
    out: Dict[str, Any] = {}
    for k, v in d.items():
        if str(k).startswith("_"):
            continue
        key = f"{prefix}.{k}" if prefix else str(k)
        if isinstance(v, dict):
            out.update(_flatten(v, key))
        else:
            out[key] = v
    return out


def _entry_verdict(region: str, profile_dir: Optional[Path]) -> str:
    try:
        from wqb.region_profile import load_profile
        prof = load_profile(region, profile_dir) if profile_dir else load_profile(region)
        return (prof.entry_verdict if prof else "") or "unknown"
    except Exception:  # noqa: BLE001
        return "unknown"


def _cell_status(cell: Dict[str, Any], entry_verdict: str) -> str:
    st = cell.get("status") or "auto"
    if st != "auto":
        return st
    return {"active": "active", "probe-only": "probe", "frozen": "archived"}.get(entry_verdict, "probe")


def resolve(region: str, category: Optional[str] = None, dataset: Optional[str] = None, *,
            store=None, config_dir: Optional[Path] = None, profile_dir: Optional[Path] = None,
            db: Optional[str] = None) -> Dict[str, Any]:
    """合成本区域（可选：某类别 / 某数据集）的生效画像。"""
    region = region.upper()
    cat_source = "参数"
    if dataset and not category:
        category = dataset_category(region, dataset, db=db)
        cat_source = "datasets 表（缺记录时前缀推断）"
    cat = normalize_category(category) if category else None
    cdir = Path(config_dir) if config_dir else config_dir_of(region)
    settings = _read_json(cdir / "settings.json")
    thresholds = _read_json(cdir / "thresholds.json")
    cell = cell_for(region, cat, cdir) if cat else {}
    verdict = _entry_verdict(region, profile_dir)
    violations: List[str] = []

    # ---- 回测设置：settings.json → 组合覆盖 ----
    backtest: Dict[str, Dict[str, Any]] = {}
    for k, v in settings.items():
        if not str(k).startswith("_"):
            backtest[k] = {"value": v, "source": "settings.json"}
    bt = cell.get("backtest") or {}
    for k, v in (bt.get("overrides") or {}).items():
        backtest[k] = {"value": v, "source": f"cells.json:{cat}",
                       "evidence": (bt.get("_evidence") or {}).get(k, ""),
                       "region_value": settings.get(k)}

    # ---- 阈值：thresholds.json 的 S4/S5 节 → 组合覆盖（受锁定表约束）----
    th: Dict[str, Dict[str, Any]] = {}
    for sec in THRESHOLD_SECTIONS:
        if isinstance(thresholds.get(sec), dict):
            for k, v in _flatten(thresholds[sec], sec).items():
                th[k] = {"value": v, "source": "thresholds.json"}
    tov = cell.get("thresholds") or {}
    for k, v in (tov.get("overrides") or {}).items():
        if k.startswith("mode_b."):
            continue  # 交给 mode_b_config（含下限钳制）
        why = check_threshold_override(k, v)
        if why:
            violations.append(f"组合阈值覆盖未生效：{why}")
            continue
        th[k] = {"value": v, "source": f"cells.json:{cat}",
                 "evidence": (tov.get("_evidence") or {}).get(k, ""),
                 "region_value": (th.get(k) or {}).get("value")}

    # ---- Mode B 主闸（含组合覆盖与下限钳制）----
    from wqb.workflow.mode_b_config import load_mode_b_config
    mb_cfg = load_mode_b_config(store if store is not None else _ReadonlyLedger(db), region=region, category=cat)
    mg = mb_cfg.get("main_gate") or {}
    mode_b = {"sharpe_min": mg.get("sharpe_min"), "fitness_min": mg.get("fitness_min"),
              "source": mb_cfg.get("_source"), "floor": mb_cfg.get("_floor"),
              "clamped_from": mb_cfg.get("_clamped_from")}

    # ---- 生成（S2）与改进（S4）要点：全局 → 类别卡 → 组合 ----
    cid = card_of(cat) if cat else None
    card = _cards.card(cid) if cid else {}
    glob = _cards.global_section()
    gen_cell = cell.get("generation") or {}
    generation = {
        "global_forbidden": list(GLOBAL_FORBIDDEN),
        "card_forbidden": list(card.get("forbidden") or []),
        "primitives": list(card.get("primitives") or []),
        "card_cross_region": list(card.get("cross_region") or []),
        "windows": dict(card.get("windows") or {}),
        "s1_hints": list(card.get("s1_hints") or []),
        "use": list(gen_cell.get("use") or []),
        "avoid": list(gen_cell.get("avoid") or []),
        "skeletons": list(gen_cell.get("skeletons") or []),
        "notes": list(gen_cell.get("notes") or []),
    }
    s4_cell = cell.get("s4") or {}
    levers = [dict(lv, scope="组合") for lv in (s4_cell.get("levers") or [])]
    levers += [dict(lv, scope="类别卡") for lv in (card.get("s4_levers") or [])]
    levers += [dict(lv, scope="全局（跨区复现）") for lv in (glob.get("s4_levers") or [])]
    s4 = {"levers": levers, "avoid": list(s4_cell.get("avoid") or []), "notes": list(glob.get("notes") or [])}

    return {
        "region": region, "dataset": dataset, "category": cat, "category_source": cat_source if cat else None,
        "card": cid, "group": group_of(cat) if cat else None,
        "entry_verdict": verdict, "cell_exists": bool(cell), "cell_status": _cell_status(cell, verdict) if cat else None,
        "cell_note": cell.get("note") or cell.get("status_note") or "",
        "backtest": backtest, "thresholds": th, "mode_b": mode_b,
        "generation": generation, "s4": s4, "evidence": dict(cell.get("evidence") or {}),
        "locks": [str(lk["id"]) for lk in LOCKED], "violations": violations,
    }


def backtest_pins(region: str, dataset: Optional[str] = None, category: Optional[str] = None,
                  config_dir: Optional[Path] = None, db: Optional[str] = None) -> List[str]:
    """组合的回测设置覆盖，按 pipeline.py 的 `--set KEY=VALUE` 形态返回（无覆盖返回空列表）。"""
    if dataset and not category:
        category = dataset_category(region, dataset, db=db)
    if not category:
        return []
    cdir = Path(config_dir) if config_dir else config_dir_of(region)
    ov = ((cell_for(region, category, cdir).get("backtest") or {}).get("overrides")) or {}
    return [f"{k}={v}" for k, v in ov.items()]


def check_region(region: str, config_dir: Optional[Path] = None) -> List[str]:
    """校验本区组合文件（schema + 锁定表 + 证据）；返回错误列表。"""
    return validate_cells(region, load_cells(region, config_dir))


# ---------------------------------------------------------------- 文本输出

def _fmt_val(v: Any) -> str:
    return json.dumps(v, ensure_ascii=False) if not isinstance(v, str) else v


def explain_text(p: Dict[str, Any]) -> str:
    """把 resolve() 的结果排成给人看的文本。"""
    L: List[str] = []
    head = f"{p['region']}"
    if p.get("category"):
        head += f" × {p['category']}（类别卡 {p['card']}，分组 {p['group']}；类别来源：{p['category_source']}）"
    if p.get("dataset"):
        head += f"  数据集 {p['dataset']}"
    L.append(f"== 生效画像：{head}")
    L.append(f"区域入场：{p['entry_verdict']}" + (f"；组合状态：{p['cell_status']}"
                                                 f"{'' if p['cell_exists'] else '（本组合无专属文件，全部跟区域）'}"
                                                 if p.get("category") else ""))
    if p.get("cell_note"):
        L.append(f"组合备注：{p['cell_note']}")
    L.append("")
    L.append("-- 回测设置（进仿真的值；来源：settings.json = 区域，cells.json = 本组合覆盖）")
    for k, v in p["backtest"].items():
        extra = f"  ← 区域值 {_fmt_val(v.get('region_value'))}；证据：{v.get('evidence')}" if "region_value" in v else ""
        L.append(f"  {k:<16} {_fmt_val(v['value']):<14} [{v['source']}]{extra}")
    L.append("")
    mb = p["mode_b"]
    L.append(f"-- Mode B 主闸：sharpe {mb['sharpe_min']} / fitness {mb['fitness_min']}  [{mb['source']}]"
             f"；下限 {mb.get('floor')}" + (f"；被钳掉的原值 {mb['clamped_from']}" if mb.get("clamped_from") else ""))
    L.append("-- 阈值（S4 评审 / S5 前置；thresholds.json 的 review / near / gates / diversity 节 + 组合覆盖）")
    for k, v in p["thresholds"].items():
        extra = f"  ← 区域值 {_fmt_val(v.get('region_value'))}；证据：{v.get('evidence')}" if "region_value" in v else ""
        L.append(f"  {k:<40} {_fmt_val(v['value']):<10} [{v['source']}]{extra}")
    g = p["generation"]
    if p.get("category"):
        L.append("")
        L.append("-- S1 字段提示（类别卡）")
        L += [f"  · {x}" for x in g["s1_hints"]] or ["  （无）"]
        L.append(f"  窗口（类别卡，均在白名单内）：{g['windows'] or '（未写）'}")
        L.append("-- S2 生成")
        L += [f"  用（组合）：{x}" for x in g["use"]]
        L += [f"  避（组合）：{x}" for x in g["avoid"]]
        L += [f"  骨架（组合，{s.get('evidence')}）：{s.get('text')}" for s in g["skeletons"]]
        L += [f"  说明（组合）：{x}" for x in g["notes"]]
        L += [f"  原语（类别卡）：{x}" for x in g["primitives"]]
        L += [f"  跨区结论（类别卡，{'/'.join(e.get('regions', []))}）：{e.get('what')}" for e in g["card_cross_region"]]
        L += [f"  禁止（类别卡）：{x}" for x in g["card_forbidden"]]
    L += [f"  禁止（全局）：{x}" for x in g["global_forbidden"]]
    L.append("-- S4 改进杠杆（按顺序试；组合 → 类别卡 → 全局）")
    for i, lv in enumerate(p["s4"]["levers"], 1):
        tag = "；禁外推" if lv.get("no_extrapolate") else ""
        L.append(f"  {i}. [{lv['scope']}] {lv.get('what')}（证据：{lv.get('evidence')}{tag}）")
        if lv.get("precondition"):
            L.append(f"     前提：{lv['precondition']}")
    L += [f"  不要用（组合）：{a.get('what')}（{a.get('evidence')}）" for a in p["s4"]["avoid"]]
    L += [f"  提醒：{x}" for x in p["s4"]["notes"]]
    ev = p.get("evidence") or {}
    if ev:
        L.append("")
        L.append(f"-- 证据（sync-cells 于 {ev.get('synced_at')} 只读汇总）：回测 {ev.get('backtests')}、RA 全过 "
                 f"{ev.get('ra_clean')}、prod 已测 {ev.get('prod_measured')}（<上限 {ev.get('prod_clean')}）、"
                 f"判死 {len(ev.get('dead_ends') or [])}、胜绩 {len(ev.get('wins') or [])}")
    L.append("")
    L.append("-- 锁定（任何层都不能放宽）：" + "、".join(p["locks"]))
    if p["violations"]:
        L.append("!! 未生效的覆盖：")
        L += [f"   {v}" for v in p["violations"]]
    return "\n".join(L)
