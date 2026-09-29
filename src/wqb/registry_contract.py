# -*- coding: utf-8 -*-
"""registry_empirical 写入契约（单一实现）。

toolkit `campaign.py registry`（`_lib/registry.py`）与 wqb-db MCP 的 `upsert_registry_empirical` /
`seal_dead_end` 写的是同一张表，此前各守各的规则：CLI 校验必填字段并补 `dead_at` / `date`，
MCP 照单全收——同一张表里于是有两种形状的 dead_end（缺 `id` / `rule`），而 `rule`（「下次怎么办」）
恰是配置包与人读的唯一可执行部分。skills 审查 CM-03 / CM-05（2026-09-29，DEC-34）：
校验只在这里实现一份，两个入口都调它；本模块不碰数据库。

layer 约定：
  dead_end   判死的信号族      必填 id / family / reason / rule（可选 salvage / dead_at / 任意扩展）
  win        可复用配方        必填 id / what / key（可选 date / evidence）
  campaign   数据集进度        必填 dataset / status ∈ untried|in_progress|exhausted（可选 note）
  orphan     403 后的孤儿      必填 id
  cross_region  跨区铁律（自旧表 cross_region_lessons 迁入；只读层，不校验）
"""
from __future__ import annotations

import datetime
from typing import Any, Dict, Optional

REQUIRED: Dict[str, list] = {
    "dead_end": ["id", "family", "reason", "rule"],
    "win": ["id", "what", "key"],
    "campaign": ["dataset", "status"],
    "orphan": ["id"],
}
STATUS_OK = ("untried", "in_progress", "exhausted")
#: 有读取方、没有写入规范的层：MCP 写入时不校验必填（保持迁入数据可原样回写）
FREEFORM_LAYERS = ("cross_region",)


class RegistryContractError(ValueError):
    """payload 不满足所在 layer 的写入契约。"""


def _today() -> str:
    return datetime.date.today().isoformat()


def validate(layer: str, payload: Dict[str, Any], today: Optional[str] = None) -> Dict[str, Any]:
    """按 layer 校验必填字段；缺省自动补 `dead_at`（dead_end）/ `date`（win）。返回规范化后的新 dict。"""
    if layer not in REQUIRED:
        raise RegistryContractError(f"非法 layer: {layer}（可选: {sorted(REQUIRED)}）")
    if not isinstance(payload, dict):
        raise RegistryContractError(f"{layer} payload 必须是对象（dict），得到 {type(payload).__name__}")
    missing = [k for k in REQUIRED[layer] if not payload.get(k)]
    if missing:
        raise RegistryContractError(f"{layer} payload 缺必填字段: {missing}")
    if layer == "campaign" and payload["status"] not in STATUS_OK:
        raise RegistryContractError(f"campaign.status 非法: {payload['status']}（可选: {STATUS_OK}）")
    p = dict(payload)
    if layer == "dead_end" and not p.get("dead_at"):
        p["dead_at"] = today or _today()
    if layer == "win" and not p.get("date"):
        p["date"] = today or _today()
    return p


def entry_id_of(layer: str, payload: Dict[str, Any]) -> str:
    """`registry_empirical.entry_id`：campaign 层用数据集名，其余层用 payload.id。"""
    return payload["dataset"] if layer == "campaign" else payload["id"]


def family_of(layer: str, payload: Dict[str, Any]) -> Optional[str]:
    """`registry_empirical.family` 列：dead_end 取 family，win 取 what，campaign 取 dataset。"""
    if layer == "dead_end":
        return payload.get("family")
    if layer == "win":
        return payload.get("what")
    if layer == "campaign":
        return payload.get("dataset")
    return None


def dead_at_of(payload: Dict[str, Any]) -> Optional[str]:
    """`registry_empirical.dead_at` 列（win 层存的是 date）。"""
    return payload.get("dead_at") or payload.get("date")
