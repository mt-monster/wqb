# -*- coding: utf-8 -*-
"""Profile 漂移检测：profile 的 datasets.green/red（精确层）↔ DB 实证（win/dead_end/ledger *_dead）。

机制定位（2026-10-01，region-profile-contract.md §5）：把 profile 从静态文档接回流水线——
每次 win / dead_end 回写（`upsert_registry_empirical`）后自动核对一次，结果幂等落
ledger `profile_drift`；`tools/profile_drift_check.py` 提供全区体检入口。

判定全部是**集合运算**（精确化的意义所在）：

| kind | 判据 | 严重度 | 含义 |
|---|---|---|---|
| green_but_dead | 数据集在 profile green，且 ledger `*_dead` 已整集判死 | high | profile 在指路去死路 |
| red_but_won | 数据集在 profile red，但 win 层已有胜绩 | high | profile 在封杀活路 |
| green_but_family_dead | 数据集在 profile green，registry dead_end 层有**族级**判死记录 | medium | 未必整集死，人工核实 |
| unknown_dataset_ref | profile 引用的数据集 id 不在 `datasets` 表（本区） | medium | 写错 id 或数据集同步缺口 |
| dead_not_listed | ledger `*_dead` 整集判死但 profile red 未收录 | medium | 死路未沉淀进 profile，S0 可能再选 |
| win_not_listed | 有胜绩数据集不在 profile green | medium | 活路未认领 |
| stale_last_verified | `last_verified` 早于最近一次实证回写 | low | 内容层未复核（只提示，不构成 needs_refresh） |

**两档死亡证据严格分开**：ledger `*_dead` = 整集判死（步 3 铁律① 的显式写入，唯一无歧义）；
registry `dead_end` 的 `payload.dataset` = 该数据集语境下**某族**死了（如
`GBR-INST6-HOLDINGS-CEILING` 是 holdings 族死，不是 institutions6 整集死）。族级死只进
`green_but_family_dead`（medium）与汇总计数，**不**驱动 dead_not_listed（族死不妨碍
S0 选该集的其它族）。

族级条目（scope=family）不参与集合运算——它们本来就不绑定单个数据集（如 GLB emotion
信号族），强绑才是错误。registry 条目没有 `dataset` 绑定的记 `unbound_entries` 计数并提示
补绑（不补绑的条目永远只能停留在 advisory 层——这是逼着补齐的杠杆）。

needs_refresh = 存在任一 high 级发现。本模块只读 + 产出报告，不改 profile（那是人工复核的事）。
"""
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from wqb.region_profile import RegionProfile, load_profile

#: 复合 dataset 写法拆分（历史数据里有 'predictive_starmine × news73' / 'a+b' / 'a,b' / 'a（注）'）
_SPLIT = re.compile(r"\s*(?:×|\+|＋|,|，|\bx\b|\bX\b)\s*")
_PAREN = re.compile(r"[（(][^)）]*[)）]")


def split_dataset_refs(raw: Any) -> List[str]:
    """把 registry payload 里的 dataset / datasets 归一成干净的数据集 id 列表。

    - str / list[str] 均可；dict 等异形态丢弃
    - 拆分复合写法（× / + / ,），剥掉括号注释，lowercase
    """
    items: List[str] = []
    if isinstance(raw, str):
        items = [raw]
    elif isinstance(raw, list):
        items = [x for x in raw if isinstance(x, str)]
    out: List[str] = []
    for it in items:
        for part in _SPLIT.split(_PAREN.sub("", it)):
            part = part.strip().lower()
            if part:
                out.append(part)
    return out


def _registry_facts(conn, region: str) -> Tuple[Dict[str, str], Dict[str, str], int, str]:
    """本区 registry win/dead_end 层的实证。返回 (win_datasets, dead_datasets, unbound_n, latest_write)。"""
    wins: Dict[str, str] = {}
    deads: Dict[str, str] = {}
    unbound = 0
    latest = ""
    cur = conn.execute(
        "SELECT layer, entry_id, payload, updated_at FROM registry_empirical "
        "WHERE region=? AND layer IN ('win','dead_end')",
        (region,),
    )
    for layer, entry_id, payload, updated_at in cur.fetchall():
        if updated_at and str(updated_at) > latest:
            latest = str(updated_at)
        try:
            p = json.loads(payload) if isinstance(payload, str) else (payload or {})
        except (ValueError, TypeError):
            p = {}
        if not isinstance(p, dict):
            p = {}
        ds = split_dataset_refs(p.get("dataset")) + split_dataset_refs(p.get("datasets"))
        if not ds:
            unbound += 1
        target = wins if layer == "win" else deads
        for d in ds:
            target.setdefault(d, entry_id)
    return wins, deads, unbound, latest


def _ledger_dead_facts(conn, region: str) -> Tuple[Dict[str, str], str]:
    """ledger_kv 的 `*_dead` 键（数据集级判死，键名即数据集）。返回 (dead_datasets, latest_write)。"""
    out: Dict[str, str] = {}
    latest = ""
    cur = conn.execute(
        "SELECT key, updated_at FROM ledger_kv WHERE region=? AND key LIKE '%_dead'",
        (region,),
    )
    for key, updated_at in cur.fetchall():
        name = str(key)[: -len("_dead")].strip().lower()
        if name:
            out[name] = f"ledger:{key}"
        if updated_at and str(updated_at) > latest:
            latest = str(updated_at)
    return out, latest


def _valid_datasets(conn, region: str) -> Optional[set]:
    """本区 datasets.name 集合；表缺/区缺返回 None（此时跳过 unknown_dataset_ref 判定，不误报）。"""
    try:
        cur = conn.execute(
            "SELECT d.name FROM datasets d JOIN regions r ON d.region_id=r.id WHERE r.name=?",
            (region,),
        )
    except Exception:
        return None
    names = {str(r[0]).strip().lower() for r in cur.fetchall() if r[0]}
    return names or None


def dead_dataset_index(conn, region: str) -> Dict[str, set]:
    """本区「别再碰」数据集索引（公共件；消费方如 `tools/select_ra_basket.py` 的剔死过滤）。

    返回三档（语义层级见模块 docstring）：
      - ``dataset_dead``：ledger `*_dead` 整集判死
      - ``family_dead``：registry dead_end 的 payload.dataset 族级绑定
      - ``saturated``：  ledger `saturated_datasets` 的 datasets 键（prod 饱和，P2 触发键）
    全部 lowercase。读失败 → 对应档为空集（fail-open，宁可漏剔不可误杀）。
    """
    _wins, deads_reg, _u, _l1 = _registry_facts(conn, region)
    deads_ledger, _l2 = _ledger_dead_facts(conn, region)
    saturated: set = set()
    try:
        row = conn.execute(
            "SELECT value FROM ledger_kv WHERE region=? AND key='saturated_datasets'", (region,),
        ).fetchone()
        if row and row[0]:
            v = json.loads(row[0])
            if isinstance(v, dict):
                ds = v.get("datasets")
                if isinstance(ds, dict):
                    saturated = {str(k).strip().lower() for k in ds}
                elif isinstance(ds, list):
                    saturated = {str(x).strip().lower() for x in ds if isinstance(x, str)}
    except Exception:
        pass
    return {
        "dataset_dead": set(deads_ledger),
        "family_dead": set(deads_reg),
        "saturated": saturated,
    }


def whitelist_dead_intersection(conn, region: str, datasets) -> Dict[str, Any]:
    """白名单写入守卫：`s0_whitelist` 的 datasets 与判死证据求交（**非阻断告警**）。

    挂载点 = `upsert_ledger_key` 对该键的归一化拦截链（每次写入必经，2026-10-01 落地）。
    动机（KOR risk70 事故）：白名单写入方只查本区台账（「KOR dead_end 台账零命中」），
    跨三区死族得以进名单；做过跨区检查的修正又被写进零读取方的孤儿键。

    分级（与步 1 §1.4 跨区规则同口径）：
      - high   = 本区整集死（ledger `*_dead`）/ 本区饱和 / **跨区 ≥2 区判死**（§1.4 排除线）
      - medium = 跨区恰 1 区判死（降权参考，不排除）
      - low    = 本区族级死（dead_end 绑定，未必整集死，人工核实）
    fail-open：任何读取异常只降级为部分结果，绝不阻断写入本体。
    """
    region = str(region).upper()
    ds_list = sorted({str(d).strip().lower() for d in (datasets or []) if d})
    if not ds_list:
        return {"hits": [], "n_high": 0, "clean": True, "hint": "白名单为空"}
    local = dead_dataset_index(conn, region)

    xreg: Dict[str, set] = {}
    try:
        for rname, entry_id, payload in conn.execute(
                "SELECT region, entry_id, payload FROM registry_empirical "
                "WHERE layer='dead_end' AND region<>?", (region,)):
            # 证据二路：① payload.dataset 干净绑定（首选）② entry_id 词元精确匹配
            # （如 IND-RISK70-NO-SIGNAL 按 '-' 切词含 risk70——补「只写 family 文本没绑 dataset」
            # 的召回缺口；词元精确匹配不是子串，pv1 不会误中 pv106）
            tokens = set(str(entry_id or "").lower().split("-"))
            try:
                p = json.loads(payload) if isinstance(payload, str) else (payload or {})
            except (ValueError, TypeError):
                p = {}
            if not isinstance(p, dict):
                p = {}
            bound = split_dataset_refs(p.get("dataset")) + split_dataset_refs(p.get("datasets"))
            for d in ds_list:
                if d in bound or d in tokens:
                    xreg.setdefault(d, set()).add(rname)
        for rname, key in conn.execute(
                "SELECT region, key FROM ledger_kv WHERE key LIKE '%_dead' AND region<>?", (region,)):
            d = str(key)[: -len("_dead")].strip().lower()
            if d in ds_list:
                xreg.setdefault(d, set()).add(rname)
    except Exception:
        pass

    hits: List[Dict[str, Any]] = []
    for d in ds_list:
        if d in local["dataset_dead"]:
            hits.append({"dataset": d, "severity": "high", "kind": "local_dead",
                         "detail": "本区已整集判死（ledger *_dead）——不应进白名单"})
        elif d in local["saturated"]:
            hits.append({"dataset": d, "severity": "high", "kind": "local_saturated",
                         "detail": "本区已 prod 饱和（saturated_datasets）——不应进白名单"})
        xr = sorted(xreg.get(d, set()))
        if len(xr) >= 2:
            hits.append({"dataset": d, "severity": "high", "kind": "xregion_dead",
                         "detail": f"跨区死族（{len(xr)} 区判死：{'/'.join(xr)}）——步 1 §1.4 应排除"})
        elif len(xr) == 1:
            hits.append({"dataset": d, "severity": "medium", "kind": "xregion_weak",
                         "detail": f"其它区 {xr[0]} 有判死记录——降权参考（1 区不排除）"})
        if d in local["family_dead"]:
            hits.append({"dataset": d, "severity": "low", "kind": "local_family_dead",
                         "detail": "本区有族级判死（未必整集死）——人工核实"})
    n_high = sum(1 for h in hits if h["severity"] == "high")
    hint = (f"白名单含 {n_high} 个强告警数据集：逐条核实后再决定保留（报告不阻断写入）"
            if n_high else ("有提示项，见 hits" if hits else "白名单与判死证据无交集"))
    return {"hits": hits, "n_high": n_high, "clean": not hits, "hint": hint}


def check_profile_drift(conn, region: str, profile_dir: Optional[Path] = None) -> Dict[str, Any]:
    """对某区跑一次 profile 漂移检查。返回结构化报告（机读 + 人读 hint）。

    Args:
        conn: 已打开的 wqb.db 连接（调用方管理生命周期）
        region: 区域（如 KOR）
        profile_dir: profile 目录覆盖（测试用）；缺省 = 仓库权威目录
    """
    region = str(region).upper()
    prof: Optional[RegionProfile] = load_profile(region, profile_dir)
    if prof is None:
        return {
            "region": region, "needs_refresh": False, "profile": "missing",
            "summary": {}, "findings": [],
            "hint": f"{region} 无 profile 文件——开新区前先补 references/regions/{region}.md",
        }

    refs = prof.dataset_refs()
    green_ds, red_ds = set(refs["green"]), set(refs["red"])
    wins, deads_reg, unbound, latest_reg = _registry_facts(conn, region)
    deads_ledger, latest_lg = _ledger_dead_facts(conn, region)
    deads_family = {k: v for k, v in deads_reg.items() if k not in deads_ledger}  # 仅族级死
    valid = _valid_datasets(conn, region)

    findings: List[Dict[str, Any]] = []

    def add(kind: str, severity: str, dataset: Optional[str], detail: str):
        findings.append({"kind": kind, "severity": severity, "dataset": dataset, "detail": detail})

    for ds in sorted(green_ds & set(deads_ledger)):
        add("green_but_dead", "high", ds,
            f"profile green 收录，但已整集判死（{deads_ledger[ds]}）——从 green 移除或改 red")
    for ds in sorted(green_ds & set(deads_family)):
        add("green_but_family_dead", "medium", ds,
            f"profile green 收录，但 dead_end 层有族级判死（{deads_family[ds]}）——核实是否整集死")
    for ds in sorted(red_ds & set(wins)):
        add("red_but_won", "high", ds,
            f"profile red 收录，但 win 层有胜绩（{wins[ds]}）——从 red 移除或改 green")
    if valid is not None:
        for ds in sorted((green_ds | red_ds) - valid):
            add("unknown_dataset_ref", "medium", ds,
                "不在本区 datasets 表——id 写错，或该区数据集未同步")
    for ds in sorted(set(deads_ledger) - red_ds - green_ds):
        add("dead_not_listed", "medium", ds,
            f"已整集判死（{deads_ledger[ds]}）但 profile red 未收录——死路没沉淀，S0 可能再选")
    for ds in sorted(set(wins) - green_ds - red_ds):
        add("win_not_listed", "medium", ds,
            f"win 层有胜绩（{wins[ds]}）但 profile green 未收录——活路未认领")

    latest_write = max(latest_reg, latest_lg) if (latest_reg or latest_lg) else ""
    lv = (prof.last_verified or "").strip()
    if lv and latest_write and lv < latest_write[:10]:
        findings.append({
            "kind": "stale_last_verified", "severity": "low", "dataset": None,
            "detail": f"last_verified={lv} 早于最近一次实证回写 {latest_write[:10]}——"
                      "复核正文与 front-matter 一致性后人工 bump（禁止批量机械刷新）",
        })

    n_high = sum(1 for f in findings if f["severity"] == "high")
    summary = {
        "high": n_high,
        "medium": sum(1 for f in findings if f["severity"] == "medium"),
        "low": sum(1 for f in findings if f["severity"] == "low"),
        "green_datasets": sorted(green_ds),
        "red_datasets": sorted(red_ds),
        "win_datasets": sorted(wins),
        "dead_datasets": sorted(deads_ledger),
        "family_dead_datasets": sorted(deads_family),
        "unbound_entries": unbound,
    }
    needs_refresh = n_high > 0
    if needs_refresh:
        hint = (f"{region} profile 与 DB 实证冲突 {n_high} 处："
                "按 findings 逐条修 datasets.green/red 后人工复核 bump last_verified")
    elif findings:
        hint = f"{region} profile 无硬冲突，有 {len(findings)} 条提示（见 findings）"
    else:
        hint = f"{region} profile 与 DB 实证一致"
    if unbound:
        hint += f"；另有 {unbound} 条 win/dead_end 条目缺 payload.dataset 绑定，无法进精确层——补齐后本检查覆盖更全"
    return {
        "region": region,
        "needs_refresh": needs_refresh,
        "profile": str(prof.path) if prof.path else None,
        "last_verified": lv or None,
        "latest_writeback": latest_write or None,
        "summary": summary,
        "findings": findings,
        "hint": hint,
    }
