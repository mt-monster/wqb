# -*- coding: utf-8 -*-
"""PyramidsMixin: 塔位指纹的落库与查询（`alpha_pyramids` 表）。

背景（2026-10-30）
------------------
`alphas` 表**没有** pyramid 列、没有 `decay` / `truncation` 列，`region_id` 又会混区
（EUR 与 GBR 共用同一 id）。后果：要判「这颗候选会不会点亮某座塔 / 当时用的什么设置档」，
每轮都被迫逐条回平台 `get_alpha_details`，而一次回测审计动辄几十条候选。

★★★ 塔位到底在哪：`is.checks[]` 里的 `MATCHES_PYRAMID` 项
-----------------------------------------------------------
这一点极易踩错，两天内错了两次。**原始 REST `GET /alphas/{id}` 的形态是**：

    j["pyramids"]        -> None        # 恒为 null，REST 从不填
    j["ra"]              -> KeyError    # 这个键根本不存在
    j["category"]        -> None
    j["is"]["checks"]    -> [ {...17 项...} ]   # ★ 塔位在这里

其中名为 `MATCHES_PYRAMID` 的那一项才是权威：

    {"result": "PASS", "name": "MATCHES_PYRAMID", "effective": 2, "multiplier": 1.4,
     "pyramids": [{"name": "GBR/D1/PV",          "multiplier": 1.4},
                  {"name": "GBR/D1/FUNDAMENTAL", "multiplier": 1.6}]}

而 MCP 工具 `get_alpha_details` 返回的 `ra` / `pyramids` / `checks.fail|pass|warning|pending`
**全部是 MCP 侧从 `is.checks` 归一化出来的**（`world-quant-brain-mcp/mcp_core.py:187-223`：
`MATCHES_PYRAMID` → `pyramids`，`pyramid_short` = 各塔 `name` 末段小写以 `/` 连接）。
⇒ 本模块以 `is.checks` 为**主路径**，MCP 归一化形态只作兼容降级。

★ `failed_ra_count` 同理：原始 REST 没有 `ra.failed_ra_count`，必须自己数
`is.checks[]` 里 `result == "FAIL"` 的条数（`checks_fail` = 这些项的 `name`）。
`WARNING` / `PENDING` 不计入 —— `rKRkL9QE` 有 2 个 warning、6 个 pending，但
`failed_ra_count = 0`，与平台一致。

★ 为什么不再用 `wqb/towers.py::infer_tower()`
---------------------------------------------
1. 它按字段 category **投票取最多者**，只返回一条腿；而**一条 alpha 可同时点亮多座塔**
   （`divide(fnd6_<科目>, cap)` 天生 PV+FUNDAMENTAL，`effective=2`，倍率 1.4+1.6）。
   用它做点塔进度会系统性低估塔数与倍率。
2. 塔位**不可**从 `dataset_id` 推断：`dataset_id=291` 一个槽位同时装
   `rKRkL9QE`（PV+FUNDAMENTAL）与 `9qxQamje`（OTHER）两种塔位。

写入方：`tools/backfill_alpha_pyramids.py`（批量回填）与 harvest 链路。
本模块只做「平台 payload → 库」的纯解析与 upsert，不发任何网络请求。
"""
from __future__ import annotations

from typing import Any, Dict, Iterable, List, Optional, Tuple

from ._common import _dumps, _loads, _now


def _as_dict(detail: Any) -> Dict[str, Any]:
    """兼容 `{"result": {...}}` 外壳（MCP 结构化回包会套一层）。"""
    if not isinstance(detail, dict):
        return {}
    for wrap in ("result", "data", "alpha"):
        inner = detail.get(wrap)
        if isinstance(inner, dict) and ("id" in inner or "is" in inner or "pyramids" in inner):
            return inner
    return detail


def _check_items(detail: Dict[str, Any]) -> List[Dict[str, Any]]:
    """取出检查项列表 —— 平台唯一权威形态是 `is.checks`（list）。

    兼容三种入口形态，优先级由高到低：
    1. `detail["is"]["checks"]` 是 list（原始 REST，主路径）
    2. `detail["checks"]` 是 list（调用方已把 `is` 段拍平）
    3. 都没有 ⇒ 返回 `[]`，上层退回 MCP 归一化字段
    """
    isd = detail.get("is")
    if isinstance(isd, dict):
        raw = isd.get("checks")
        if isinstance(raw, list):
            return [c for c in raw if isinstance(c, dict)]
    raw = detail.get("checks")
    if isinstance(raw, list):
        return [c for c in raw if isinstance(c, dict)]
    return []


def _matches_pyramid(detail: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """定位 `MATCHES_PYRAMID` 检查项；没有则 `None`。"""
    for c in _check_items(detail):
        if str(c.get("name") or "").strip().upper() == "MATCHES_PYRAMID":
            return c
    return None


def _towers(detail: Dict[str, Any]) -> List[Dict[str, Any]]:
    """取出塔位列表 `[{"name","multiplier"}]`。

    主路径：`is.checks[MATCHES_PYRAMID].pyramids`
    降级：MCP 归一化 `pyramids.list`
    """
    raw: Any = None
    mp = _matches_pyramid(detail)
    if isinstance(mp, dict):
        raw = mp.get("pyramids")
    if not isinstance(raw, list):
        pyr = detail.get("pyramids")
        if isinstance(pyr, dict):
            raw = pyr.get("list")
    if not isinstance(raw, list):
        return []

    out: List[Dict[str, Any]] = []
    for item in raw:
        if not isinstance(item, dict):
            continue
        name = item.get("name")
        if not name:
            continue
        mult = item.get("multiplier")
        try:
            mult_f = float(mult) if mult is not None else None
        except (TypeError, ValueError):
            mult_f = None
        out.append({"name": str(name), "multiplier": mult_f})
    return out


def _effective(detail: Dict[str, Any], towers: List[Dict[str, Any]]) -> Optional[int]:
    """`effective` = 该 alpha 计入几座塔（≠ `len(towers)`，但通常相等）。"""
    mp = _matches_pyramid(detail)
    if isinstance(mp, dict) and isinstance(mp.get("effective"), int):
        return mp["effective"]
    pyr = detail.get("pyramids")
    if isinstance(pyr, dict) and isinstance(pyr.get("effective"), int):
        return pyr["effective"]
    return len(towers) or None


def _pyramid_short(detail: Dict[str, Any], towers: List[Dict[str, Any]]) -> Optional[str]:
    """`pv/fundamental` 形态的短标签 —— 与平台 `ra.pyramid_short` 同构。"""
    ra = detail.get("ra")
    if isinstance(ra, dict) and ra.get("pyramid_short"):
        return str(ra["pyramid_short"])
    names = [str(t["name"]).split("/")[-1].lower() for t in towers if t.get("name")]
    return "/".join(n for n in names if n) or None


def _checks_summary(detail: Dict[str, Any]) -> Tuple[Optional[int], Optional[List[str]]]:
    """数 `is.checks[]` 里 `result == "FAIL"` 的条数，并收集其 `name`。

    只数 FAIL：`WARNING` / `PENDING` 不是闸，计入会把「平台全闸通过」误判成不通过。
    无 `is.checks` 时降级读 MCP 归一化的 `ra.failed_ra_count` / `checks.fail`。
    """
    items = _check_items(detail)
    if items:
        fails = [str(c.get("name")) for c in items
                 if str(c.get("result") or "").strip().upper() == "FAIL" and c.get("name")]
        return len(fails), fails
    ra = detail.get("ra")
    if isinstance(ra, dict) and isinstance(ra.get("failed_ra_count"), int):
        checks = detail.get("checks")
        raw = checks.get("fail") if isinstance(checks, dict) else None
        fails = [str(x) for x in raw] if isinstance(raw, list) else None
        return ra["failed_ra_count"], fails
    return None, None


def _num(v: Any, cast=float):
    if v is None:
        return None
    try:
        return cast(v)
    except (TypeError, ValueError):
        return None


class PyramidsMixin:
    """塔位指纹读写（`alpha_pyramids`）。"""

    # ------------------------------------------------------------------ 写

    def upsert_alpha_pyramids(self, detail: Any) -> Dict[str, Any]:
        """把一份 `get_alpha_details` 回包落到 `alpha_pyramids`（幂等 upsert）。

        `detail` 可以是单个回包，也可以是回包列表。返回
        ``{"action", "upserted", "skipped"}``，`skipped` 记录缺 alpha id 的条目。
        """
        items: Iterable[Any]
        if isinstance(detail, (list, tuple)):
            items = detail
        else:
            items = [detail]
        upserted = 0
        skipped: List[str] = []
        cur = self.connection.cursor()
        now = _now()
        for raw in items:
            d = _as_dict(raw)
            aid = d.get("id") or d.get("alpha_id")
            if not aid:
                skipped.append("missing_alpha_id")
                continue
            settings = d.get("settings") or {}
            if not isinstance(settings, dict):
                settings = {}
            towers = _towers(d)
            mult_sum = None
            if towers:
                vals = [t["multiplier"] for t in towers if t["multiplier"] is not None]
                mult_sum = round(sum(vals), 6) if vals else None
            failed_n, fails = _checks_summary(d)

            row = (
                str(aid),
                settings.get("region"),
                _num(settings.get("delay"), int),
                settings.get("universe"),
                _pyramid_short(d, towers),
                _dumps(towers) if towers else None,
                _effective(d, towers),
                mult_sum,
                failed_n,
                _dumps(fails) if fails is not None else None,
                settings.get("neutralization"),
                _num(settings.get("decay"), int),
                _num(settings.get("truncation"), float),
                settings.get("maxTrade"),
                settings.get("nanHandling"),
                d.get("status"),
                now,
                now,
            )
            cur.execute(
                """INSERT INTO alpha_pyramids
                   (alpha_id, region, delay, universe, pyramid_short, towers, n_towers,
                    multiplier_sum, failed_ra_count, checks_fail, neutralization, decay,
                    truncation, max_trade, nan_handling, alpha_status, fetched_at, updated_at)
                   VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
                   ON CONFLICT(alpha_id) DO UPDATE SET
                     region=excluded.region,
                     delay=excluded.delay,
                     universe=excluded.universe,
                     pyramid_short=excluded.pyramid_short,
                     towers=COALESCE(excluded.towers, alpha_pyramids.towers),
                     n_towers=COALESCE(excluded.n_towers, alpha_pyramids.n_towers),
                     multiplier_sum=COALESCE(excluded.multiplier_sum, alpha_pyramids.multiplier_sum),
                     failed_ra_count=excluded.failed_ra_count,
                     checks_fail=excluded.checks_fail,
                     neutralization=excluded.neutralization,
                     decay=excluded.decay,
                     truncation=excluded.truncation,
                     max_trade=excluded.max_trade,
                     nan_handling=excluded.nan_handling,
                     alpha_status=excluded.alpha_status,
                     fetched_at=excluded.fetched_at,
                     updated_at=excluded.updated_at""",
                row,
            )
            upserted += 1
        self.connection.commit()
        return {"action": "upserted", "upserted": upserted, "skipped": skipped}

    # ------------------------------------------------------------------ 读

    def get_alpha_pyramids(self, alpha_id: str) -> Optional[Dict[str, Any]]:
        """按 alpha id 读一行；无记录返回 ``None``。"""
        cur = self.connection.cursor()
        cur.execute("SELECT * FROM alpha_pyramids WHERE alpha_id=?", (str(alpha_id),))
        row = cur.fetchone()
        if not row:
            return None
        cols = [d[0] for d in cur.description]
        out = dict(zip(cols, row))
        out["towers"] = _loads(out.get("towers")) or []
        out["checks_fail"] = _loads(out.get("checks_fail")) or []
        return out

    def list_alpha_pyramids(self, region: Optional[str] = None, delay: Optional[int] = None,
                            only_clean: bool = False, limit: int = 500) -> List[Dict[str, Any]]:
        """按区域 / delay 列出塔位指纹。

        `only_clean=True` 只返回 `failed_ra_count == 0`（平台全闸通过）的行 ——
        这才是「如果提交会真的点亮塔」的那批。
        """
        sql = "SELECT * FROM alpha_pyramids WHERE 1=1"
        args: List[Any] = []
        if region:
            sql += " AND UPPER(region)=?"
            args.append(str(region).strip().upper())
        if delay is not None:
            sql += " AND delay=?"
            args.append(int(delay))
        if only_clean:
            sql += " AND failed_ra_count=0"
        sql += " ORDER BY multiplier_sum DESC NULLS LAST, alpha_id LIMIT ?"
        args.append(int(limit))
        cur = self.connection.cursor()
        cur.execute(sql, args)
        cols = [d[0] for d in cur.description]
        out: List[Dict[str, Any]] = []
        for row in cur.fetchall():
            rec = dict(zip(cols, row))
            rec["towers"] = _loads(rec.get("towers")) or []
            rec["checks_fail"] = _loads(rec.get("checks_fail")) or []
            out.append(rec)
        return out

    def pyramid_tally(self, region: str, delay: Optional[int] = None,
                      only_clean: bool = True) -> Dict[str, Any]:
        """统计「若全部提交会点亮哪些塔、各几颗」——直接回答点塔进度问题。

        Returns::

            {"region": "GBR", "delay": 1,
             "towers": {"GBR/D1/PV": {"n": 9, "multiplier": 1.4}, ...},
             "alphas": {"rKRkL9QE": ["GBR/D1/PV", "GBR/D1/FUNDAMENTAL"], ...},
             "n_alphas": 10, "n_multi_tower": 10}
        """
        rows = self.list_alpha_pyramids(region=region, delay=delay,
                                        only_clean=only_clean, limit=10000)
        towers: Dict[str, Dict[str, Any]] = {}
        alphas: Dict[str, List[str]] = {}
        for rec in rows:
            names: List[str] = []
            for t in rec.get("towers") or []:
                name = t.get("name")
                if not name:
                    continue
                names.append(name)
                slot = towers.setdefault(name, {"n": 0, "multiplier": t.get("multiplier")})
                slot["n"] += 1
            if names:
                alphas[rec["alpha_id"]] = names
        return {
            "region": str(region or "").upper(),
            "delay": delay,
            "towers": towers,
            "alphas": alphas,
            "n_alphas": len(rows),
            "n_multi_tower": sum(1 for v in alphas.values() if len(v) > 1),
            "only_clean": only_clean,
        }


__all__ = ["PyramidsMixin"]
