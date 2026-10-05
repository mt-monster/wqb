# -*- coding: utf-8 -*-
"""auto_review 节点：收批后评审报告（S4 增强，只读）.

只读读库里本波的回测行，产出一份评审报告，不写任何库：
1. auto_prescreen：本地 S4 分层（READY/REVIEW/REJECT）。复刻 tools/campaign_intel.py
   s4-prescreen 的硬闸口径（sharpe≥1.58 / fitness≥1.0 / 2Y≥1.58、turnover∈[0.04,0.40]），
   但只用 backtest_results 已落库的指标，不打平台 API（prod/self 相关性不在本表，不参与分层）。
2. auto_walls：walls 诊断（structural / robust / sub_universe / turnover / rn_exposure），
   只读真实列、指标 NULL 视为"缺失"（不触发该墙）。
3. auto_salvage：从 ledger_kv 的 salvage_pool 按卡闸维度检索辅助腿（只读）。
4. auto_report：汇总评审报告。

2026-09-28 N32：此前三处缺陷令本节点从未在真实表结构上跑通（单测只覆盖 dry-run）——
  ① turnover / sharpe 等指标为 NULL 时 `bt.get(k, 0) > x` 直接 `TypeError`（`.get` 的缺省值只在
     键不存在时生效，库里读出的是 None）；
  ② auto_report 往并不存在的 `review_results` 表 `INSERT OR REPLACE`（schema 无此表、全库无消费方）；
  ③ auto_prescreen 走 subprocess 调 campaign_intel.py s4-prescreen，而该子命令要鉴权打平台
     `get_alpha_details`，既非"只读战役库"、也无法在真实表结构上单测；步骤还按下标 `steps[0..3]` 取，
     关掉某个 auto_* 开关即 IndexError。
现全部改为只读、在真实表结构上跑通、指标 NULL 按缺失处理、步骤按名取、不写任何库。
SOP 的 S4 完整评审仍走 toolkit review_wave.py，本节点是只读的二级入口。
"""

import json
import logging
import os
import sqlite3
from datetime import datetime
from typing import Any, Dict, List, Optional

from .._common import connect_db_readonly, resolve_toolkit_file

logger = logging.getLogger(__name__)

#: 硬闸口径（与 tools/campaign_intel.py s4-prescreen / judge 节点一致；prod/self 不在本表故不参与）
_SHARPE_MIN, _FITNESS_MIN, _TWO_Y_MIN = 1.58, 1.0, 1.58
_TVR_LO, _TVR_HI = 0.04, 0.40
#: 2Y 稳健墙用平台 2Y 硬闸阈；子宇宙墙沿用本文件既有的 0.5 口径
_ROBUST_MIN, _SUB_UNIVERSE_MIN = 1.58, 0.5


def run(
    region: str,
    wave: str,
    dataset: Optional[str] = None,
    auto_prescreen: bool = True,
    auto_walls: bool = True,
    auto_salvage: bool = True,
    auto_report: bool = True,
    _context: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """收批后评审报告（只读）.

    Args:
        region: 区域代码
        wave: 波次号（原字符串）
        dataset: 数据集 ID（可选，仅进入返回体，不参与查询）
        auto_prescreen: 是否本地 S4 分层（默认 True）
        auto_walls: 是否 walls 诊断（默认 True）
        auto_salvage: 是否检索卡闸辅助腿（默认 True）
        auto_report: 是否生成评审报告（默认 True）
        _context: 执行上下文

    Returns:
        执行结果字典
    """
    ctx = _context or {}
    result: Dict[str, Any] = {
        "region": region,
        "wave": wave,
        "dataset": dataset,
        "success": False,
        "steps": [],
    }
    if auto_prescreen:
        result["steps"].append({"step": "auto_prescreen", "success": True,
                                "description": "本地 S4 分层（只读，不打平台 API）"})
    if auto_walls:
        result["steps"].append({"step": "auto_walls", "success": True, "description": "walls 诊断"})
    if auto_salvage:
        result["steps"].append({"step": "auto_salvage", "success": True,
                                "description": "从 salvage_pool 按卡闸维度检索辅助腿"})
    if auto_report:
        result["steps"].append({"step": "auto_report", "success": True, "description": "生成评审报告"})

    # 如果是 dry-run，到此为止（不读库、不 subprocess、零副作用）
    if ctx.get("dry_run"):
        result["success"] = True
        result["dry_run"] = True
        result["note"] = "dry-run：评审流程已构建，未读库"
        return result

    try:
        conn = connect_db_readonly()
    except sqlite3.Error as e:
        result["error"] = f"打不开战役库（只读）：{e}"
        return result
    try:
        conn.row_factory = sqlite3.Row
        rows = [dict(r) for r in conn.execute(
            "SELECT * FROM backtest_results WHERE region=? AND wave=?", (region, str(wave)))]
        if not rows:
            result["error"] = f"库里没有 {region}/{wave} 的回测行"
            return result

        tiers = _prescreen(rows) if auto_prescreen else None
        walls = _diagnose_walls(rows) if auto_walls else None
        salvage_legs = _retrieve_salvage_legs(conn, region, rows) if auto_salvage else []
    except sqlite3.Error as e:
        logger.exception("Auto review failed")
        result["error"] = f"读回测行失败：{e}"
        return result
    finally:
        conn.close()

    if auto_prescreen:
        _step(result, "auto_prescreen").update(
            tiers={k: len(v) for k, v in tiers.items()},
            ready=tiers["READY"], review=tiers["REVIEW"], reject=tiers["REJECT"])
    if auto_walls:
        _step(result, "auto_walls")["walls"] = walls
    if auto_salvage:
        _step(result, "auto_salvage").update(salvage_legs=salvage_legs, salvage_count=len(salvage_legs))
    if auto_report:
        _step(result, "auto_report")["report"] = _generate_review_report(rows, tiers, walls, salvage_legs)

    result["success"] = True
    result["backtest_count"] = len(rows)
    result["message"] = f"评审完成：{len(rows)} 条回测行"
    return result


def _step(result: Dict[str, Any], name: str) -> Dict[str, Any]:
    return next(s for s in result["steps"] if s.get("step") == name)


def _prescreen(rows: List[Dict[str, Any]]) -> Dict[str, List[Optional[str]]]:
    """本地 S4 分层：READY / REVIEW / REJECT（2026-10-02 P1：口径收敛到 _lib/prescreen）。

    此前本函数自带一套硬闸常量（_SHARPE_MIN 等），与 `tools/campaign_intel.py s4-prescreen`
    及 `review_wave.walls()` **三处口径互不一致**（实测 GBR s2_institutions6_d1 77 条在本口径
    下全判 REJECT、在 review_wave 口径下会产候选）。现统一调 `_lib/prescreen.prescreen_row`：
      - NULL 指标走 `*_UNKNOWN`（**不判败**），修掉旧 `bt.get(x) or 0` 把缺失当 0 的静默判死；
      - prod/self 在本表无列 → 传 None，不参与判定（不再因"离线没这两列"而口径分裂）；
      - 阈值缺省 = 平台线 1.58/1.0/1.58（本函数无 region 上下文，用 DEFAULT）。
    """
    try:
        import sys as _sys
        # 仓库副本优先（安装位 ~/.claude/skills 可能滞后于本仓：本次实测它没有
        # prescreen.py，导致新口径被静默 fallback 回旧常量，正是要消除的口径分裂）。
        _ps_file = resolve_toolkit_file("_lib/prescreen.py")
        if not _ps_file:
            raise ImportError("未找到含 _lib/prescreen.py 的 toolkit 副本")
        _scripts_dir = os.path.dirname(os.path.dirname(_ps_file))  # .../scripts
        if _scripts_dir not in _sys.path:
            _sys.path.insert(0, _scripts_dir)
        from _lib.prescreen import prescreen as _ps  # type: ignore
    except Exception:  # noqa: BLE001 — 包不可达则退回旧常量口径（fail-open，不阻断评审）
        return _prescreen_legacy(rows)
    out: Dict[str, List[Optional[str]]] = {"READY": [], "REVIEW": [], "REJECT": []}
    res = _ps(rows)
    for tier in ("READY", "REVIEW", "REJECT"):
        out[tier] = list(res.get(tier) or [])
    return out


def _prescreen_legacy(rows: List[Dict[str, Any]]) -> Dict[str, List[Optional[str]]]:
    """旧口径（保留作 fail-open 兜底）：`_lib/prescreen` 不可导入时使用。"""
    tiers: Dict[str, List[Optional[str]]] = {"READY": [], "REVIEW": [], "REJECT": []}
    for bt in rows:
        aid = bt.get("alpha_id")
        if bt.get("status") == "ERROR":
            tiers["REJECT"].append(aid)
            continue
        sharpe = bt.get("sharpe") or 0
        fitness = bt.get("fitness") or 0
        two_year = bt.get("two_year_sharpe") or 0
        tvr = bt.get("turnover") or 0
        hard_pass = sharpe >= _SHARPE_MIN and fitness >= _FITNESS_MIN and two_year >= _TWO_Y_MIN
        tvr_ok = _TVR_LO <= tvr <= _TVR_HI
        any_signal = sharpe >= 1.0 or fitness >= 0.5
        if hard_pass and tvr_ok:
            tiers["READY"].append(aid)
        elif any_signal:
            tiers["REVIEW"].append(aid)
        else:
            tiers["REJECT"].append(aid)
    return tiers


def _diagnose_walls(rows: List[Dict[str, Any]]) -> Dict[str, bool]:
    """walls 诊断（只读真实列，指标 NULL 视为缺失、不触发该墙）."""
    walls = {
        "structural": False,   # sharpe < 1.0
        "robust": False,       # two_year_sharpe < 1.58（平台 2Y 硬闸）
        "sub_universe": False,  # sub_universe_sharpe < 0.5
        "turnover": False,     # turnover > 0.7
        "rn_exposure": False,  # 风险中性化后 sharpe<=0 而 raw sharpe 达标 → 因子暴露本身
    }
    for bt in rows:
        sharpe = bt.get("sharpe")
        two_year = bt.get("two_year_sharpe")
        sub_u = bt.get("sub_universe_sharpe")
        tvr = bt.get("turnover")
        rn = bt.get("risk_neutralized_sharpe")
        if sharpe is not None and sharpe < 1.0:
            walls["structural"] = True
        if two_year is not None and two_year < _ROBUST_MIN:
            walls["robust"] = True
        if sub_u is not None and sub_u < _SUB_UNIVERSE_MIN:
            walls["sub_universe"] = True
        if tvr is not None and tvr > 0.7:
            walls["turnover"] = True
        if rn is not None and rn <= 0 and (sharpe or 0) >= _SHARPE_MIN:
            walls["rn_exposure"] = True
    return walls


def _retrieve_salvage_legs(
    conn: sqlite3.Connection, region: str, rows: List[Dict[str, Any]]
) -> List[Dict[str, Any]]:
    """按卡闸维度从 salvage_pool 检索辅助腿（只读，指标 NULL 按 0 计）."""
    row = conn.execute(
        "SELECT value FROM ledger_kv WHERE region=? AND key='salvage_pool'", (region,)
    ).fetchone()
    if not row or not row[0]:
        return []
    try:
        pool = json.loads(row[0])
    except (ValueError, TypeError):
        return []
    entries = pool.get("entries", []) if isinstance(pool, dict) else []

    salvage_legs: List[Dict[str, Any]] = []
    for bt in rows:
        if (bt.get("sharpe") or 0) >= _SHARPE_MIN:
            continue  # 已过闸，不需要辅助腿
        # 卡 2Y 闸
        if (bt.get("two_year_sharpe") or 0) < _TWO_Y_MIN:
            salvage_legs.extend(e for e in entries if "boost_2y" in (e.get("boost_dims") or []))
        # 卡 CW/子宇宙闸
        if (bt.get("sub_universe_sharpe") or 0) < _SUB_UNIVERSE_MIN:
            salvage_legs.extend(e for e in entries if "boost_cw" in (e.get("boost_dims") or []))
        # 卡 tvr 闸
        if (bt.get("turnover") or 0) > 0.25:
            salvage_legs.extend(e for e in entries if "boost_tvr" in (e.get("boost_dims") or []))

    seen: set = set()
    unique_legs: List[Dict[str, Any]] = []
    for leg in salvage_legs:
        leg_id = leg.get("alpha_id")
        if leg_id not in seen:
            seen.add(leg_id)
            unique_legs.append(leg)
    return unique_legs


def _generate_review_report(
    rows: List[Dict[str, Any]],
    tiers: Optional[Dict[str, List[Optional[str]]]],
    walls: Optional[Dict[str, bool]],
    salvage_legs: List[Dict[str, Any]],
) -> Dict[str, Any]:
    """汇总评审报告（指标缺失按 0 计：ERROR 行没有指标）."""
    total = len(rows)
    passed = len([bt for bt in rows
                  if (bt.get("sharpe") or 0) >= _SHARPE_MIN and (bt.get("fitness") or 0) >= _FITNESS_MIN])
    error = len([bt for bt in rows if bt.get("status") == "ERROR"])
    pass_rate = round(passed / total, 4) if total else 0
    return {
        "total": total,
        "passed": passed,
        "error": error,
        "pass_rate": pass_rate,
        "prescreen": {k: len(v) for k, v in tiers.items()} if tiers else {},
        "walls": walls or {},
        "salvage_legs_count": len(salvage_legs),
        "generated_at": datetime.now().isoformat(timespec="seconds"),
    }
