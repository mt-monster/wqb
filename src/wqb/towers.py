# -*- coding: utf-8 -*-
"""towers.py — 塔位（``region/D{delay}/{category}``）解析与从表达式反推。

背景（2026-10-05）
------------------
盘点报告需要标出每颗候选「点在哪个塔上」，但平台
``get_alpha_details()`` 对 **UNSUBMITTED** alpha 返回 ``pyramids=None``、
``category=None``、``themes=None``（实测 N1VnJjXg / O08EjLVp / LLZ6wZO2 三颗
READY 候选全部为 null）——塔位信息**只有提交后平台才会标注**。故塔位只能从
表达式用到的数据字段反推：

    表达式 → extract_fields() → fields.field_name → fields.dataset_id
           → datasets.category（平台口径，勿按语义猜）
           → "{region}/D{delay}/{category}"

数据集自身的 ``datasets.pyramid_multiplier`` 是 S0 catalog 抓下来的**数据集级**
倍率，与平台塔表（``get_pyramid_multipliers``）不完全一致（实测 EUR/D1/MODEL
dataset=1.6 vs 平台塔表=1.3）。真正结算以平台塔表为准，dataset 值仅作兜底。

本模块只读库、不调平台；塔倍率表的拉取与缓存由调用方负责
（见 ``tools/submit_inventory.py::load_pyramid_multipliers``）。
"""
from __future__ import annotations

import re
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple

# 2026-10-05 教训：字面量 `/D` 只认大写 D，导致 `parse_tower("usa/d1/model")` 返回 None
# （塔名是 case-insensitive 的语义：`format_tower` 只强制输出大写，`parse_tower` 也必须容受小写）。
_TOWER_RE = re.compile(r"^([A-Za-z]{2,5})/D([0-9]+)/([A-Za-z0-9_]+)$", re.IGNORECASE)

# 平台数据集 category 的规范小写键（与 config.PLATFORM_CATEGORIES 对齐）
_CATEGORY_ALIASES = {
    "insiders": "insider", "institutions": "institution", "socialmedia": "social_media",
}


def format_tower(region: str, delay: int, category: str) -> str:
    """规范塔名：``USA/D1/MODEL``（category 一律大写）。"""
    return f"{str(region).strip().upper()}/D{int(delay)}/{str(category).strip().upper()}"


def parse_tower(name: str) -> Optional[Tuple[str, int, str]]:
    """解析塔名 → ``(region, delay, category_upper)``；格式不符返回 None。

    容忍任意大小写与斜杠两侧的空白（``"  usa / d1 / model "``）。
    """
    if not name:
        return None
    s = " ".join(str(name).split()).replace(" ", "")  # 折叠并去掉所有空白
    m = _TOWER_RE.match(s)
    if not m:
        return None
    return m.group(1).upper(), int(m.group(2)), m.group(3).upper()


def category_key(category: str) -> str:
    """塔倍率表查键用的小写键（含别名归一）。"""
    c = str(category or "").strip().lower()
    return _CATEGORY_ALIASES.get(c, c)


def lookup_multiplier(table: Dict[str, Any], region: str, delay: int,
                      category: str) -> Optional[float]:
    """从平台塔倍率表查倍率。table 的键形态：
    * ``{"USA/D1/model": 1.3, ...}``（submit_inventory 缓存形态）
    * ``{("USA", 1, "model"): 1.3, ...}``（元组键）

    查不到返回 None（调用方自行决定兜底策略）。
    """
    if not table:
        return None
    rg, dk, ck = str(region).upper(), int(delay), category_key(category)
    for key in (f"{rg}/D{dk}/{ck}", (rg, dk, ck)):
        v = table.get(key)
        if isinstance(v, (int, float)):
            return float(v)
    return None


def _region_id(region: str, con) -> Optional[int]:
    r = con.execute("SELECT id FROM regions WHERE name=?", (str(region).upper(),)).fetchone()
    return r[0] if r else None


def field_index(region: str, db_path: Optional[str] = None,
                con: Optional[Any] = None) -> Dict[str, Dict[str, Any]]:
    """构建该区域的 ``field_name → {dataset, category, delay, multiplier}`` 索引。

    返回空 dict 表示区域无数据集目录（调用方应回退到台账/平台来源）。
    多数据集同名字段时保留 pyramid_multiplier 最大的一条（更可能是主力集）。
    """
    from wqb.store import submit_queue as _sq  # noqa: F401 - 复用连接工厂
    from wqb.db_conn import connect as db_connect

    own = con is None
    if own:
        con = db_connect(db_path)
    out: Dict[str, Dict[str, Any]] = {}
    try:
        rid = _region_id(region, con)
        if rid is None:
            return {}
        rows = con.execute(
            "SELECT f.field_name, d.name AS ds, d.category, d.delay, d.pyramid_multiplier "
            "FROM fields f JOIN datasets d ON d.id = f.dataset_id "
            "WHERE d.region_id = ? AND d.category IS NOT NULL AND d.category <> ''",
            (rid,)).fetchall()
        for r in rows:
            fn, ds, cat, delay, mult = r[0], r[1], r[2], r[3], r[4]
            if not fn:
                continue
            cur = out.get(fn)
            if cur is None or (mult or 0) > (cur.get("multiplier") or 0):
                out[fn] = {"dataset": ds, "category": cat, "delay": delay, "multiplier": mult}
        return out
    finally:
        if own:
            try:
                con.close()
            except Exception:  # noqa: BLE001
                pass


def infer_tower(expr: str, region: str,
                field_idx: Optional[Dict[str, Dict[str, Any]]] = None,
                db_path: Optional[str] = None) -> Optional[Dict[str, Any]]:
    """从表达式反推塔位。

    多字段跨多数据集时取**字段数最多**的数据集的 category（alpha 的主导信号族）；
    delay 取最大值（多数区域 D1）。

    Returns: ``{"tower","region","delay","category","dataset","fields","dataset_multiplier"}``
             表达式无数据字段 / 区域无目录时返回 None。
    """
    if not expr or "(" not in str(expr):
        return None
    try:
        from wqb.expression.atom import extract_fields, resolve_kind
    except Exception:  # noqa: BLE001
        return None
    if field_idx is None:
        field_idx = field_index(region, db_path)
    if not field_idx:
        return None
    ds_map = {k: v["dataset"] for k, v in field_idx.items()}
    hits: Dict[str, Dict[str, Any]] = {}
    used: List[str] = []
    for fld in extract_fields(expr):
        kind, _ds = resolve_kind(fld, ds_map)
        if kind != "dataset":
            continue
        info = field_idx.get(fld)
        if not info:
            continue
        used.append(fld)
        cat = str(info["category"]).upper()
        h = hits.setdefault(cat, {"count": 0, "delay": info["delay"],
                                  "dataset": info["dataset"], "multiplier": info["multiplier"]})
        h["count"] += 1
        if info["delay"] and (not h["delay"] or info["delay"] > h["delay"]):
            h["delay"] = info["delay"]
        if info["dataset"] and info["dataset"] != h["dataset"]:
            h["dataset"] = f'{h["dataset"]},{info["dataset"]}'
        if info["multiplier"] and (not h["multiplier"] or info["multiplier"] > h["multiplier"]):
            h["multiplier"] = info["multiplier"]
    if not hits:
        return None
    cat, h = max(hits.items(), key=lambda kv: (kv[1]["count"], str(kv[0])))
    return {
        "tower": format_tower(region, h["delay"] or 1, cat),
        "region": str(region).upper(),
        "delay": h["delay"] or 1,
        "category": cat,
        "dataset": h["dataset"],
        "fields": used,
        "dataset_multiplier": h["multiplier"],
    }


def describe_tower(name: Optional[str], multiplier: Optional[float],
                   source: str = "") -> str:
    """报告用的一行塔位描述。"""
    if not name:
        return "塔位未知（表达式无数据字段/区域无目录）"
    s = name
    if multiplier is not None:
        s += f" ×{multiplier:g}"
    if source:
        s += f"（{source}）"
    return s


__all__ = [
    "category_key", "describe_tower", "field_index", "format_tower",
    "infer_tower", "lookup_multiplier", "parse_tower",
]
