# -*- coding: utf-8 -*-
"""判死集合的**单一事实源**（2026-11-19 新增）。

为什么需要它
------------
本仓的判死记录有**两套存储 + 四种键形态**，而硬闸只认其中一种（`key LIKE '%_dead'`）：

| 存储 | 粒度 | 消费方 | 规模（实测） |
|---|---|---|---|
| `ledger_kv` 的 `<ds>_dead` | **数据集级** | `pipeline.py::dead_dataset_guard`（硬闸）、`get_dead_datasets` | DEU 19 / GBR 22 / KOR 16 / EUR 4 / USA 0 |
| `registry_empirical` 的 `dead_end` 层 | 族 / 结构级 | `get_dead_ends` | EUR 163 / GLB 96 / GBR 82 / DEU 70 …（主力） |
| `ledger_kv` 的 `dead_datasets` 聚合键 | 数据集级（列表 / 映射） | **无人读** | EUR / GBR 各 1 |
| `ledger_kv` 的 `dead_end_*` / `*_dead_end` / `*_dead_<date>` | 多为**族级**镜像 | **无人读** | 24 条 |

2026-11-19 审计实测该后缀匹配造成的三类事故：

1. **漏拦**：聚合键 `dead_datasets`（GBR 另有 model264 / news104 / pattern_scores / pv29 / pv30
   只记在这里）读不到；`*_dead_end` / `*_dead_<date>` 形态全部读不到。
2. **误拦**：DEU `DEATH_AUDIT_20261110.md` 已撤判重开 `risk60` / `risk88` / `news50` / `other545`，
   ledger 里的死键未回写 ⇒ 硬闸照拦。
3. **粒度混淆**：族级记录（EUR `dead_end_eur_analyst_consensus_actual` 判的是 `analyst_consensus`
   的 `actual_*` **字段族**，不是整集）若按数据集名进黑名单，会误伤同集的其他字段族。

本模块按**载荷语义**把记录分级，三档：

- ``dataset``     —— 数据集级：硬闸拦（沿用历史口径）
- ``conditional`` —— 条件死（如「不再作为单塔主信号，仅可作辅助腿」）：**告警不拦**
- ``family``      —— 族 / 路线级：只进台账，不进数据集黑名单

**设计取舍**：误拦的代价（停掉合法的波）远高于漏拦（死集多投一次配额），所以
凡是判不准的记录一律降级到 ``family``，不做猜测。
"""
from __future__ import annotations

import json
import re
from typing import Any, Iterable

#: 规范数据集级键：`<dataset>_dead`（数据集名形如 `analyst44` / `other545` / `fund_holdings_panel`）
CANONICAL_DEAD_KEY = re.compile(r"^(?P<ds>[a-z][a-z0-9_]*)_dead$")

#: 聚合键：值是 list[{dataset: ...}] 或 dict{<dataset>: {...}}
AGGREGATE_KEY = "dead_datasets"

#: 族 / 路线级键前缀（`dead_end_*`）与后缀（`*_dead_end` / `*_dead_<日期>`）
FAMILY_KEY_PREFIX = "dead_end_"
FAMILY_KEY_SUFFIX = re.compile(r"_dead_end$|_dead_\d{6,8}$")

#: 「已重新开放」标记（撤判回写用）——出现即**不再**参与硬闸
_REOPEN_MARKERS = {"reopened", "reopen", "revived", "active", "alive"}


def _loads(value: Any) -> Any:
    if isinstance(value, (dict, list)):
        return value
    if isinstance(value, str):
        try:
            return json.loads(value)
        except (json.JSONDecodeError, ValueError):
            return None
    return None


def _is_reopened(payload: Any) -> bool:
    if not isinstance(payload, dict):
        return False
    for k in ("status", "verdict", "state", "disposition"):
        v = payload.get(k)
        if isinstance(v, str) and v.strip().lower() in _REOPEN_MARKERS:
            return True
    for k in ("reopened", "reopen", "revived"):
        if payload.get(k) is True:
            return True
    return False


def _is_conditional(payload: Any) -> bool:
    """条件死：只禁「主信号用法」，不禁「辅助腿」用法。

    判据**以 `rule`（执行指令）为准**，`reason`/`conclusion` 只作兜底——
    否则会出现「rule 写『不再生成』但 reason 引了别的铁律里的『只可作辅助腿』」而被误判成
    条件死（2026-11-19 实测：GBR `risk88_dead` 的 rule 是「risk88 不再生成；GBR risk 域关闭」，
    reason 里却引了 02 铁律的「只可作辅助腿」⇒ 若按 reason 判会漏拦一个明令关闭的数据集）。
    """
    if not isinstance(payload, dict):
        return False
    lvl = payload.get("death_level")
    if isinstance(lvl, str) and "CONDITIONAL" in lvl.upper():
        return True
    rule = str(payload.get("rule") or "")
    if any(w in rule for w in ("仅可作", "只可作", "辅助腿")):
        return True
    if any(w in rule for w in ("不再生成", "不再作为", "不再投", "关闭", "不得再")):
        return False                       # 明令关闭 ⇒ 仍是数据集级
    blob = " ".join(str(payload.get(k, "")) for k in ("reason", "conclusion", "scope"))
    return any(w in blob for w in ("仅可作", "只可作", "辅助腿", "不再作为单塔主信号"))


def _family_of(payload: Any) -> str | None:
    if isinstance(payload, dict):
        fam = payload.get("family")
        if isinstance(fam, str) and fam.strip():
            return fam.strip()
    return None


def _dataset_of(payload: Any) -> str | None:
    if isinstance(payload, dict):
        ds = payload.get("dataset")
        if isinstance(ds, str) and ds.strip():
            return ds.strip()
    return None


def classify_entry(key: str, value: Any) -> list[dict[str, Any]]:
    """把一条 ledger 判死记录解析成若干条目。

    返回每条：``{dataset, level, key, reason, dead_at, reopened, detail}``。
    ``dataset`` 为 None 表示「不是数据集级」（族 / 路线级记录）。
    """
    payload = _loads(value)
    out: list[dict[str, Any]] = []

    def _mk(dataset: str | None, level: str, reason: str = "", dead_at: str = "") -> None:
        out.append({
            "dataset": dataset,
            "level": level,
            "key": key,
            "reason": reason,
            "dead_at": dead_at,
            "reopened": _is_reopened(payload),
            "detail": payload if isinstance(payload, dict) else None,
        })

    def _one(ds: str | None, payload_obj: Any) -> None:
        """按载荷语义给单条数据集判死定级。"""
        if not ds:
            _mk(None, "family")
            return
        fam = _family_of(payload_obj)
        if fam and fam != ds:
            # 族 / 机制级：判的不是整集 ⇒ 不进数据集黑名单
            _mk(ds, "family")
            return
        if _is_reopened(payload_obj):
            _mk(ds, "conditional", reason="已撤判重开", dead_at="")
            out[-1]["reopened"] = True
            return
        if _is_conditional(payload_obj):
            _mk(ds, "conditional")
            return
        reason, dead_at = "", ""
        if isinstance(payload_obj, dict):
            reason = str(payload_obj.get("reason") or payload_obj.get("conclusion") or "")[:400]
            dead_at = str(payload_obj.get("dead_at") or payload_obj.get("date") or "")[:40]
        _mk(ds, "dataset", reason, dead_at)

    # ---- 形态 1：聚合键 `dead_datasets` ----
    if key == AGGREGATE_KEY:
        if isinstance(payload, list):
            for item in payload:
                if isinstance(item, dict):
                    _one(_dataset_of(item), item)
                elif isinstance(item, str):
                    _one(item, None)
        elif isinstance(payload, dict):
            # dict{<dataset>: {...}}（GBR 形态）或 dict{...}（内层再包一层 datasets）
            inner = payload.get("datasets")
            if isinstance(inner, dict):
                for ds, sub in inner.items():
                    _one(ds, sub if isinstance(sub, dict) else None)
            elif isinstance(inner, list):
                for item in inner:
                    _one(item if isinstance(item, str) else _dataset_of(item), None)
            else:
                for ds, sub in payload.items():
                    if isinstance(sub, dict):
                        _one(ds, sub)
                    elif isinstance(sub, str):
                        _one(ds, None)
        return out

    # ---- 形态 2：规范 `<ds>_dead` ----
    m = CANONICAL_DEAD_KEY.match(key)
    if m:
        ds = _dataset_of(payload) or m.group("ds")
        _one(ds, payload)
        return out

    # ---- 形态 3：族 / 路线级镜像键 ----
    if key.startswith(FAMILY_KEY_PREFIX) or FAMILY_KEY_SUFFIX.search(key):
        _one(_dataset_of(payload), payload)
        return out

    return out


def parse_dead_entries(rows: Iterable[tuple[str, Any]]) -> dict[str, dict[str, Any]]:
    """把若干 ledger 行解析成 ``{dataset: 条目}``（同名合并，dataset 级优先）。

    ``rows`` 形如 ``[(key, value_json_str), ...]``。
    """
    merged: dict[str, dict[str, Any]] = {}
    unclassified: list[str] = []
    for key, value in rows:
        entries = classify_entry(key, value)
        if not entries:
            unclassified.append(key)
            continue
        for e in entries:
            ds = e["dataset"]
            if not ds:
                continue
            prev = merged.get(ds)
            if prev is None or (e["level"] == "dataset" and prev["level"] != "dataset"):
                merged[ds] = e
    if unclassified:
        merged.setdefault("__unclassified__", {
            "dataset": None, "level": "family", "key": ",".join(sorted(unclassified)),
            "reason": "键形态未归类（不参与硬闸）", "dead_at": "", "reopened": False, "detail": None,
        })
    return merged


def dead_levels(rows: Iterable[tuple[str, Any]]) -> dict[str, list[str]]:
    """返回 ``{"dataset": [...], "conditional": [...], "family": [...]}`` 三档数据集名。

    ``dataset`` 档 = 可硬拦；``conditional`` 档 = 只告警；``family`` 档 = 只登记。
    """
    parsed = parse_dead_entries(rows)
    out: dict[str, list[str]] = {"dataset": [], "conditional": [], "family": []}
    for ds, e in parsed.items():
        if ds == "__unclassified__" or not ds:
            continue
        if e.get("reopened"):
            continue                      # 已撤判重开 ⇒ 不出现在任何档
        out[e["level"]].append(ds)
    for k in out:
        out[k] = sorted(set(out[k]))
    return out


def blocking_datasets(rows: Iterable[tuple[str, Any]]) -> set[str]:
    """硬闸数据集集合（只含 ``dataset`` 档）。"""
    return set(dead_levels(rows)["dataset"])
