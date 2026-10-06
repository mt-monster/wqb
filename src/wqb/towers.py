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
（见 ``tools/verdict/submit_inventory.py::load_pyramid_multipliers``）。

注（2026-10-06）：本文件曾被外部 ``cline restore transaction`` 连同其他未跟踪
脚本一起清出工作区，且无任何 git 历史。此版本依据 ``__pycache__/towers.*.pyc``
中残留的字节码常量（正则、别名表、docstring、函数签名）重建，行为与原版一致。
"""

from __future__ import annotations

import re
from typing import Any, Dict, Optional, Tuple

_TOWER_RE = re.compile(r"^([A-Za-z]{2,5})/D([0-9]+)/([A-Za-z0-9_]+)$", re.IGNORECASE)

# 平台塔表的 category id 有多种写法（复数 / 连写），统一归一到塔表键的小写蛇形。
_CATEGORY_ALIASES = {
    "insiders": "insider",
    "institutions": "institution",
    "socialmedia": "social_media",
}


def format_tower(region: str, delay: int = 1, category: str = "") -> str:
    """规范塔名：``USA/D1/MODEL``（category 一律大写）。"""
    rg = str(region or "").strip().upper()
    try:
        dl = int(delay)
    except (TypeError, ValueError):
        dl = 1
    cat = str(category or "").strip().upper()
    return f"{rg}/D{dl}/{cat}"


def parse_tower(name: str) -> Optional[Tuple[str, int, str]]:
    """``"usa/d1/model"`` → ``("USA", 1, "MODEL")``；非塔名返回 ``None``。

    大小写不敏感（``/d`` 与 ``/D`` 均可，category 大小写均可），输出统一大写。
    """
    if not name:
        return None
    m = _TOWER_RE.match(str(name).strip())
    if not m:
        return None
    return (m.group(1).upper(), int(m.group(2)), m.group(3).upper())


def category_key(category: str) -> str:
    """category → 塔表键的小写蛇形（``"MODEL"`` → ``"model"``）。

    先去空白、转小写、空格/连字符转下划线，再过别名表。
    """
    s = str(category or "").strip().lower().replace(" ", "_").replace("-", "_")
    return _CATEGORY_ALIASES.get(s, s)


def lookup_multiplier(table: Dict[str, Any], region: str, delay: int,
                      category: str) -> Optional[float]:
    """在平台塔倍率表（键形如 ``"USA/D1/model"``）里查倍率；查不到返回 ``None``。"""
    if not table:
        return None
    rg = str(region or "").strip().upper()
    ck = category_key(str(category or ""))
    if not rg or not ck:
        return None
    try:
        dl = int(delay)
    except (TypeError, ValueError):
        return None
    key = f"{rg}/D{dl}/{ck}"
    if key in table:
        try:
            return float(table[key])
        except (TypeError, ValueError):
            return None
    # 兜底：忽略大小写再找一次（历史缓存可能存成大写）
    for k, v in table.items():
        if str(k).strip().lower() == key.lower():
            try:
                return float(v)
            except (TypeError, ValueError):
                return None
    return None


def _connect(db_path: Optional[str] = None):
    """取库连接：``wqb.store.connect``（若存在）→ ``wqb.store.submit_queue.connect``。"""
    try:
        from wqb.store import connect as _c  # type: ignore[attr-defined]
        return _c(db_path)
    except Exception:  # noqa: BLE001
        from wqb.store.submit_queue import connect as _c2
        return _c2(db_path)


def _region_id(region: str, con: Optional[Any] = None) -> Optional[int]:
    """区域名 → ``regions.id``。"""
    rg = str(region or "").strip().upper()
    if not rg:
        return None
    if con is None:
        con = _connect()
        close = True
    else:
        close = False
    try:
        row = con.execute("SELECT id FROM regions WHERE UPPER(name)=? LIMIT 1",
                          (rg,)).fetchone()
        return int(row[0]) if row else None
    except Exception:  # noqa: BLE001 - 表/列缺失时静默降级
        return None
    finally:
        if close:
            try:
                con.close()
            except Exception:  # noqa: BLE001
                pass


def field_index(region: str, db_path: Optional[str] = None,
                con: Optional[Any] = None) -> Dict[str, Dict[str, Any]]:
    """字段名 → ``{category, delay, dataset, pyramid_multiplier}``（按区域过滤）。"""
    if con is None:
        con = _connect(db_path)
        close = True
    else:
        close = False
    idx: Dict[str, Dict[str, Any]] = {}
    try:
        rid = _region_id(region, con)
        if rid is None:
            return {}
        rows = con.execute(
            "SELECT f.field_name, d.category, d.delay, d.name, d.pyramid_multiplier "
            "FROM fields f JOIN datasets d ON d.id = f.dataset_id "
            "WHERE d.region_id = ?", (rid,)).fetchall()
        for fname, cat, delay, dsname, mult in rows:
            if not fname:
                continue
            idx[str(fname)] = {
                "category": cat,
                "delay": delay,
                "dataset": dsname,
                "pyramid_multiplier": mult,
            }
    except Exception:  # noqa: BLE001 - 库不可用时返回空索引，由调用方降级
        return {}
    finally:
        if close:
            try:
                con.close()
            except Exception:  # noqa: BLE001
                pass
    return idx


def infer_tower(expr: str, region: str,
                field_idx: Optional[Dict[str, Dict[str, Any]]] = None,
                db_path: Optional[str] = None) -> Optional[Dict[str, Any]]:
    """从表达式反推塔位：取表达式命中的字段、按 category 投票取最多者。

    Returns: ``{"tower", "category", "delay", "dataset", "dataset_multiplier"}``；
    无法反推（无字段 / 库里查不到 / 无 category）返回 ``None``。
    """
    if not expr:
        return None
    if field_idx is None:
        field_idx = field_index(region, db_path=db_path)
    if not field_idx:
        return None
    try:
        from wqb.expression.atom import extract_fields
        names = extract_fields(expr) or []
    except Exception:  # noqa: BLE001 - 解析失败即无法反推
        return None
    votes: Dict[Tuple[str, Any, Optional[str]], int] = {}
    meta: Dict[Tuple[str, Any, Optional[str]], Dict[str, Any]] = {}
    for n in names:
        info = field_idx.get(str(n))
        if not info:
            continue
        cat = info.get("category")
        if not cat:
            continue
        delay = info.get("delay")
        try:
            delay = int(delay)
        except (TypeError, ValueError):
            delay = 1
        key = (str(cat).strip().upper(), delay, info.get("dataset"))
        votes[key] = votes.get(key, 0) + 1
        meta.setdefault(key, info)
    if not votes:
        return None
    key = max(votes.items(), key=lambda kv: (kv[1], kv[0][0]))[0]
    cat, delay, dsname = key
    info = meta.get(key) or {}
    mult = info.get("pyramid_multiplier")
    try:
        mult = float(mult) if mult is not None else None
    except (TypeError, ValueError):
        mult = None
    return {
        "tower": format_tower(region, delay, cat),
        "category": cat,
        "delay": delay,
        "dataset": dsname,
        "dataset_multiplier": mult,
        "votes": votes[key],
    }


def describe_tower(name: Optional[str] = None,
                   multiplier: Optional[float] = None,
                   source: str = "") -> str:
    """人类可读的一行塔位描述，用于报告打印。"""
    if not name:
        return "塔位未知"
    s = str(name)
    if multiplier is not None:
        try:
            s += f" ×{float(multiplier):g}"
        except (TypeError, ValueError):
            pass
    src = str(source or "").strip()
    if src:
        s += f"（{src}）"
    return s


__all__ = ["category_key", "describe_tower", "field_index", "format_tower",
           "infer_tower", "lookup_multiplier", "parse_tower"]
