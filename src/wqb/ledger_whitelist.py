# -*- coding: utf-8 -*-
"""s0_whitelist 的容错读取 —— 单一契约入口（2026-09-17 P0-4）。

## 问题（实测）
同一 ledger 键 `s0_whitelist` 在 13 个区域存在 **5 种互不兼容形态**：

| 形态 | 区域 | 数据集所在键 |
|---|---|---|
| `candidates[]` | CHN / DEU / EUR / KOR | `candidates[].dataset` |
| `whitelist[]` | HKG / JPN / MEA / USA | `whitelist[]`（字符串列表）|
| `datasets[]` | IND | `datasets[]` |
| `other` | ASI（counts/gate/delay…）/ GLB（analyst/earnings…）| 无显式列表 |
| **非 dict** | **GBR** | JSON 串内再包一层 JSON（双重序列化）|

对照：`s0_ranking` 在全部 10 个有记录的区域统一为 `ranking[]`，**零漂移** ——
说明漂移特异地集中在本键（写入方缺统一契约）。

## 后果：三个消费者三种假设，各自 fail-open
- `tools/campaign_intel.py` 只认 `candidates[].dataset` → 仅命中 4/13 区，
  其余 9 区白名单被当作空集（override-gap 审计静默降级为"无数据"）
- `score_datasets.py::_check_universe_consistency`（P3 守卫）只认
  `universe` 顶层或 `settings.universe` → DEU/JPN/MEA/USA/GLB 未记 universe
  → `if u and u != cur` 短路 → **守卫静默跳过**
- `workflow/nodes/campaign.py` 只认 `filter_criteria.{delay,universe}`
  → 全区域 `LIKE '%filter_criteria%'` 返回空 → **该读取路径是死代码**

## 本模块的立场
**宽容读取 + 显式失败**：接受全部已知形态并归一为统一结构；无法判定时返回
`ok=False + reason`，由调用方 WARN。绝不把"读不懂"伪装成"空集"。
"""
import json
import re
from typing import Any, Dict, List, Optional, Tuple

#: 已知的数据集列表键（按优先级）
_DATASET_KEYS = ("whitelist", "candidates", "datasets", "entries", "list")

#: 从未归一原值取值的候选键（含 settings / filter_criteria 下钻）
_SETTING_CONTAINERS = ("settings", "filter_criteria", "filters", "context")

# ---- 损坏记录兜底提取（GBR 实测：value 双重编码且内层 JSON 被截断）----
_DS_RE = re.compile(r'"dataset"\s*:\s*"([^"]+)"')
_UNIVERSE_RE = re.compile(r'"universe"\s*:\s*"([^"]+)"')
_DELAY_RE = re.compile(r'"delay"\s*:\s*(\d+)')
_WL_BLOCK_RE = re.compile(r'"whitelist"\s*:\s*\[(.*?)\]', re.S)
_QUOTED_TOKEN_RE = re.compile(r'"([A-Za-z][A-Za-z0-9_\-\.]{1,60})"')


def _recover_from_text(text: str) -> Dict[str, Any]:
    """从**损坏/截断**的 JSON 文本中按字段正则抢救可恢复内容。

    背景（2026-09-17 实测）：GBR `s0_whitelist` 的 value 是"JSON 串内再包一层
    JSON"，且内层在 5511 字符处**截断**（`... or STATISTICAL A/B twin"]}` 戛然而止），
    标准 `json.loads` 必然失败。但字段与数据集名仍可正则恢复 —— 直接判失败会让
    下游把该区白名单当空集（正是我们要消灭的 fail-open）。
    """
    ds = list(dict.fromkeys(_DS_RE.findall(text)))
    if not ds:
        m = _WL_BLOCK_RE.search(text)
        if m:
            ds = list(dict.fromkeys(_QUOTED_TOKEN_RE.findall(m.group(1))))
    uni = _UNIVERSE_RE.search(text)
    dly = _DELAY_RE.search(text)
    delay_val = int(dly.group(1)) if dly else None
    return {
        "ok": bool(ds),
        "reason": ("记录损坏（双重编码且内层截断），已按字段正则抢救"
                   if ds else "记录损坏且无法从文本抢救出数据集"),
        "schema": "recovered",
        "double_encoded": True,
        "universe": uni.group(1) if uni else None,
        "delay": delay_val,
        "datasets": ds,
        "entries": [],
        "extras": {"_recovered_from_truncated": True,
                   "_raw_len": len(text)},
    }


def _maybe_double_decoded(raw: Any) -> Tuple[Any, bool]:
    """解开可能的双重序列化（GBR 实测：value 是 JSON 串内再包一层 JSON）。"""
    if isinstance(raw, (bytes, bytearray)):
        raw = raw.decode("utf-8", "replace")
    if not isinstance(raw, str):
        return raw, False
    once = raw
    for _ in range(3):
        try:
            parsed = json.loads(once)
        except (ValueError, TypeError):
            return once, once is not raw
        if isinstance(parsed, str):
            once = parsed
            continue
        return parsed, once is not raw
    return once, True


def _pick_str(d: Dict[str, Any], *keys: str) -> Optional[str]:
    """按顺序取第一个非空字符串（顶层优先，再下钻 settings/filter_criteria）。"""
    for k in keys:
        v = d.get(k)
        if isinstance(v, str) and v.strip():
            return v.strip()
    for c in _SETTING_CONTAINERS:
        sub = d.get(c)
        if isinstance(sub, dict):
            for k in keys:
                v = sub.get(k)
                if isinstance(v, str) and v.strip():
                    return v.strip()
    return None


def _pick_number(d: Dict[str, Any], *keys: str) -> Optional[int]:
    """按顺序取第一个整数值（**兼容 JSON 数字与数字字符串**，如 `"delay": 1` 与 `"1"`）。

    2026-09-17：初版只走 `_pick_str`，导致 `{"delay": 1}`（JSON 数字）被漏掉，
    `delay` 恒为 None —— 由 `test_normalize_datasets_shape` 抓出。
    """
    for container in (d,) + tuple(
            v for v in (d.get(c) for c in _SETTING_CONTAINERS) if isinstance(v, dict)):
        for k in keys:
            v = container.get(k)
            if isinstance(v, bool):
                continue
            if isinstance(v, int):
                return v
            if isinstance(v, float) and v.is_integer():
                return int(v)
            if isinstance(v, str) and v.strip():
                try:
                    return int(v.strip())
                except ValueError:
                    continue
    return None


def _entries_to_datasets(entries: Any) -> List[str]:
    """从候选列表抽取数据集 id（兼容字符串列表与 dict 列表）。"""
    out: List[str] = []
    if not isinstance(entries, list):
        return out
    for item in entries:
        if isinstance(item, str) and item.strip():
            out.append(item.strip())
        elif isinstance(item, dict):
            for k in ("dataset", "id", "dataset_id", "name"):
                v = item.get(k)
                if isinstance(v, str) and v.strip():
                    out.append(v.strip())
                    break
    # 保序去重
    seen = set()
    uniq = []
    for d in out:
        if d not in seen:
            seen.add(d)
            uniq.append(d)
    return uniq


def normalize(raw: Any) -> Dict[str, Any]:
    """把任意已知形态的 `s0_whitelist` 归一为统一结构。

    返回：
      {
        "ok": bool,               # 能否识别出数据集合集
        "reason": str | None,     # ok=False 时说明原因（调用方据此 WARN）
        "schema": str,            # 命中的形态名（whitelist/candidates/datasets/
                                  #   inferred/non_dict/unparsable/empty）
        "double_encoded": bool,   # GBR 形态
        "universe": str | None,
        "delay": int | None,
        "datasets": [str],        # 归一后的数据集 id 列表
        "entries": [dict],        # 原始条目（保留 override 等审计字段）
        "extras": dict,           # 其余顶层键（供迁移时保留）
      }
    """
    out: Dict[str, Any] = {
        "ok": False, "reason": None, "schema": "unknown", "double_encoded": False,
        "universe": None, "delay": None, "datasets": [], "entries": [], "extras": {},
    }
    if raw is None:
        out["reason"] = "值为空（未写或已删除）"
        return out

    data, double = _maybe_double_decoded(raw)
    out["double_encoded"] = double

    if not isinstance(data, dict):
        # 损坏记录兜底（GBR 实测形态）：双重编码且内层截断 → 正则抢救
        if isinstance(data, str) and data.lstrip().startswith("{"):
            rec = _recover_from_text(data)
            if rec["ok"]:
                return rec
            out.update({"schema": rec["schema"], "reason": rec["reason"],
                        "datasets": rec["datasets"]})
            return out
        out["schema"] = "non_dict"
        out["reason"] = f"顶层不是对象而是 {type(data).__name__}（无法解析契约）"
        return out

    out["extras"] = {k: v for k, v in data.items() if k not in _DATASET_KEYS}
    out["universe"] = _pick_str(data, "universe")
    out["delay"] = _pick_number(data, "delay")

    # 1) 已知键直接命中
    for key in _DATASET_KEYS:
        if key in data:
            entries = data[key]
            ds = _entries_to_datasets(entries)
            out["schema"] = key
            out["entries"] = [e for e in entries if isinstance(e, dict)] \
                if isinstance(entries, list) else []
            out["datasets"] = ds
            if ds:
                out["ok"] = True
            else:
                out["reason"] = f"命中 `{key}` 但其中无有效数据集 id"
            return out

    # 2) 未命中已知键：尝试从任意列表值里推断（ASI/GLB 一类）
    inferred: List[str] = []
    for k, v in data.items():
        if isinstance(v, list):
            ds = _entries_to_datasets(v)
            if ds:
                inferred.extend(ds)
    if inferred:
        seen, uniq = set(), []
        for d in inferred:
            if d not in seen:
                seen.add(d)
                uniq.append(d)
        out["schema"] = "inferred"
        out["datasets"] = uniq
        out["ok"] = True
        out["reason"] = "无标准列表键，已从其它列表字段推断（契约漂移）"
        return out

    out["schema"] = "unparsable"
    out["reason"] = (f"未找到数据集列表键（已知键 {list(_DATASET_KEYS)} 均不命中，"
                     f"无其它可推断列表；顶层键={list(data.keys())[:8]}）")
    return out


def load_from_ledger(conn, region: str, key: str = "s0_whitelist") -> Dict[str, Any]:
    """便捷：从已连接的 sqlite 读某区 ledger 键并归一。"""
    row = conn.execute("SELECT value FROM ledger_kv WHERE region=? AND key=?",
                       (region, key)).fetchone()
    if row is None:
        out = normalize(None)
        out["reason"] = f"ledger 无 {region}/{key} 记录"
        return out
    return normalize(row[0])


def to_canonical(rec: Dict[str, Any], keep_legacy: Any = None) -> Dict[str, Any]:
    """产出统一契约形态（供迁移脚本使用）：顶层 universe/delay + datasets[]。

    迁移目标刻意对齐 `s0_ranking` 的稳定风格（顶层 universe），并保留
    `_legacy` 原值与 `_schema_from` 来源，确保可回溯、可回滚。
    """
    canonical: Dict[str, Any] = {
        "datasets": list(rec.get("datasets") or []),
        "generated_at": None,
    }
    if rec.get("universe"):
        canonical["universe"] = rec["universe"]
    if rec.get("delay") is not None:
        canonical["delay"] = rec["delay"]
    if rec.get("entries"):
        canonical["entries"] = rec["entries"]
    if keep_legacy is not None:
        canonical["_legacy"] = keep_legacy
    canonical["_schema_from"] = rec.get("schema")
    return canonical
