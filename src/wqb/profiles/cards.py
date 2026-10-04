# -*- coding: utf-8 -*-
"""类别卡（跨区的类别级知识）：`category_cards.json` 的加载与校验（2026-10-04）。

类别卡只收两类内容：
- 与区域无关的类别常识：概念原语（迁自 GEM `economic_priors.CATEGORY_PRIMITIVES`）、类别特有禁止项
  （迁自 `CATEGORY_FORBIDDEN`）、字段性质提示（更新频率 / 类型 → 窗口）；
- **至少两个区同向复现**的结论（`cross_region`，每条写明区域与证据）。只有一个区的证据写进该区的
  组合（`tracking/<R>/config/cells.json`），不写进卡——「证据作用域 = 规则作用域」。
跨区结论相反的（如「换分母」KOR 有效、EUR 是毒药）以 `type: conflict` 登记，提醒按组合取用。
"""
from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path
from typing import Any, Dict, List

from .locked import nonstandard_windows, recommends_weighted_mix
from .taxonomy import CARD_OF

CARDS_PATH = Path(__file__).resolve().parent / "category_cards.json"

#: 卡片字段（未列出的键视为笔误，校验报错）
CARD_KEYS = {"title", "group", "aliases", "families", "field_profile", "windows", "s1_hints",
             "primitives", "forbidden", "cross_region", "s4_levers", "mechanisms_ref"}
ENTRY_KEYS = {"id", "what", "regions", "evidence", "type", "note", "precondition"}


@lru_cache(maxsize=1)
def _load_cached(path: str, mtime: float) -> Dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def load_cards(path: Path = CARDS_PATH) -> Dict[str, Any]:
    p = Path(path)
    return _load_cached(str(p), p.stat().st_mtime)


def card(card_id: str, path: Path = CARDS_PATH) -> Dict[str, Any]:
    return (load_cards(path).get("cards") or {}).get(card_id) or {}


def global_section(path: Path = CARDS_PATH) -> Dict[str, Any]:
    return load_cards(path).get("global") or {}


def _entries(card_body: Dict[str, Any]) -> List[Dict[str, Any]]:
    return list(card_body.get("cross_region") or []) + list(card_body.get("s4_levers") or [])


def validate_cards(data: Dict[str, Any]) -> List[str]:
    """返回错误列表（空 = 合法）。"""
    from wqb.config import STANDARD_WINDOWS
    errs: List[str] = []
    cards = data.get("cards")
    if not isinstance(cards, dict) or not cards:
        return ["category_cards.json 缺 cards"]
    valid_ids = set(CARD_OF.values())
    for cid, body in cards.items():
        if cid not in valid_ids:
            errs.append(f"{cid}: 不是 taxonomy.CARD_OF 里的卡 id")
            continue
        extra = set(body) - CARD_KEYS
        if extra:
            errs.append(f"{cid}: 未知键 {sorted(extra)}")
        for k, ws in (body.get("windows") or {}).items():
            bad = [w for w in ws if w not in STANDARD_WINDOWS]
            if bad:
                errs.append(f"{cid}.windows.{k}: 非白名单窗口 {bad}")
        for text in body.get("primitives") or []:
            if recommends_weighted_mix(text):
                errs.append(f"{cid}.primitives 推荐了加权混合: {text[:60]}")
        for e in _entries(body):
            extra = set(e) - ENTRY_KEYS
            if extra:
                errs.append(f"{cid}.{e.get('id')}: 未知键 {sorted(extra)}")
            if not e.get("id") or not e.get("what"):
                errs.append(f"{cid}: 条目缺 id / what")
            regions = e.get("regions") or []
            if len(set(regions)) < 2:
                errs.append(f"{cid}.{e.get('id')}: 类别卡只收 ≥2 个区复现的结论（单区证据写进组合 cells.json）")
            if not e.get("evidence"):
                errs.append(f"{cid}.{e.get('id')}: 缺 evidence")
            if e.get("type") not in (None, "negative", "positive", "conflict", "lever"):
                errs.append(f"{cid}.{e.get('id')}: type 只能是 negative / positive / conflict / lever")
            if e.get("type") != "negative" and recommends_weighted_mix(str(e.get("what"))):
                errs.append(f"{cid}.{e.get('id')}: 推荐了加权混合")
            bad = nonstandard_windows(str(e.get("what")))
            if bad and "窗口" not in str(e.get("note") or ""):
                errs.append(f"{cid}.{e.get('id')}: 非白名单窗口 {bad} 未在 note 里写解释与证据")
    for e in (data.get("global") or {}).get("s4_levers") or []:
        if len(set(e.get("regions") or [])) < 2 or not e.get("evidence"):
            errs.append(f"global.s4_levers.{e.get('id')}: 需 ≥2 区证据")
    return errs
