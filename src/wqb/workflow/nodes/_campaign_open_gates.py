# -*- coding: utf-8 -*-
"""开波闸簇：从 campaign.py 抽出的三道开波闸及其辅助（内部模块，勿直接改签名）。

内容与职责与抽离前完全一致；`campaign.py` 顶部 `from ._campaign_open_gates import ...`
re-export 保持对外接口不变（run_open_wave_gates / _normalize_verdict 等仍可从
`wqb.workflow.nodes.campaign` 导入）。

成员：
  - 常量：STOP_RULES_DEFAULTS / BACKLOG_GATE_DEFAULTS
  - 三道开波闸：_run_backlog_gate / _run_stop_rules_gate / _run_signal_floor_gate
  - 聚合入口：run_open_wave_gates（batch_track 也复用）
  - 停止规则求值：_evaluate_stop_rules_axis 及其辅助
    （_recent_closed_waves / _axis_wave_metadata / _dead_end_productive / _wall_routing_hint /
     _stop_rules_schema_supports_axis / _parse_dt_loose / _waiver_from_result / _normalize_verdict）
"""
import json
import os
import re
import sqlite3
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Tuple

from ...wave_results_contract import normalize_verdict as _contract_normalize_verdict
from ... import waiver as _waiver
from .._common import (
    connect_db_readonly,
    local_ts,
    resolve_db_path,
)



#: 停止规则默认参数（区域 thresholds.json `diversity.stop_rules` 可覆盖；enabled=false 关闭）
STOP_RULES_DEFAULTS = {
    "enabled": True,
    "yield_min_backtests": 100,     # 区级：回测 ≥N 且达标 0 → 停区
    "consecutive_fail_waves": 3,    # 规则 B1：同轴最近 K 个 closed 波连续可计数 FAIL → 熔断该轴（旧口径=全区最近 K 波全 FAIL）
    "sharpe_min": 1.58,
    "fitness_min": 1.0,
    # ---- 2026-09-17 加固（P0-3 停止闸输入完整性）----
    # verdict 已归一化（见 _normalize_verdict，与写入契约同一张表）：自由文本 `0/8 过硬闸` 算 FAIL，
    # 空值算 UNKNOWN。以下两项控制更严/更保守的可选口径，默认不改变既有拦截面。
    "strict_no_pass": False,        # True → 最近 K 个 closed 波"无任何 PASS"即停区（严于全 FAIL；两条路径均生效）
    "unknown_warn": True,           # verdict 空/不可识别 → 输出 WARN，但不当作"通过"也不据此拦截
    # ---- 2026-09-23 按轴计数（axis_scope=True 且 schema 齐备时生效，否则回落旧口径）----
    "axis_scope": True,             # 规则 B 按轴(region×dataset)计数；False=旧全区口径
    "axis_window": 8,               # B2 聚合窗口：最近 M 个 closed 波（B1 同窗口内取该轴序列）
    "distinct_fail_axes": 4,        # B2：窗口内 ≥D 个不同轴全 FAIL 且无 PASS → 停区
    "exempt_dead_end_waves": True,  # 产出新 dead_end 的 FAIL 波不计数
    "exempt_zero_cost_waves": True, # 零配额 FAIL（有 gate_results 无 backtest）不计数
}


#: 积压闸默认参数（区域 thresholds.json `diversity.backlog_gate` 可覆盖；enabled=false 关闭）
BACKLOG_GATE_DEFAULTS = {
    "enabled": True,
    "conversion_min": 0.10,       # 区级 conversion（已回测/已生成）低于此值 → 拦截
    "pending_gated_ratio_max": 0.30,  # pending+gated 占比超此值 → 拦截
    "min_expressions": 200,       # 表达式总量低于此值的新区不判（样本不足）
    # ---- 2026-09-17 P0-2：补齐"未消费"口径 ----
    # 旧口径只算 pending+gated，**漏掉 gem/selected**（数量最大的两类积压）。
    # 实测：DEU pending+gated 仅 6.6% 过闸，但其 gem 存量占全区表达式 72% → 假通过；
    # JPN 首日 gem=1640/pending+gated=0，若非 conversion=0 恰好命中，积压完全不可见。
    "unconsumed_ratio_max": 0.30,     # (gem+selected+pending+gated) 占比上限
    "unconsumed_enforce": False,      # 灰度：默认只报不拦；经确认清单后再置 True
}


def _run_backlog_gate(
    region: str,
    dataset: Optional[str],
    campaign_dir: str,
) -> Dict[str, Any]:
    """区级积压闸（2026-09-15 审计行动 3；S2/S3 前置，零配额）。

    ra-pipeline 步 6「积压清理」与步 1 产出率读法（conversion <10% 的区先清积压
    再开新波）此前只是 prose，DB 实证 7 区违反仍在开新波（GLB 0%、EUR 1%、
    GBR/ASI 3%、CHN/KOR 7%、USA 9%）。本闸把它变成 S2/S3 开波前置硬判定：

      - conversion（status 含 backtested/submitted/completed ÷ 总数）< conversion_min
        且总量 ≥ min_expressions → 拦截（提示先消化近闸积压）
      - pending+gated 占比 > pending_gated_ratio_max 且总量 ≥ min_expressions
        → 拦截（S2→S3 断链，堆库不消化）

    只看库、零平台调用。命中时与 stop_rules 同样支持 ledger `backlog_gate_override`
    {"reason","until"} 显式放行留痕。
    """
    result: Dict[str, Any] = {"step": "backlog_gate", "success": True}
    # 测试/沙箱隔离口：WQB_DISABLE_BACKLOG_GATE=1 时跳过（与 signal_floor 的
    # thresholds 关闭口并行；单测不封库时用，生产路径不受影响）
    if os.environ.get("WQB_DISABLE_BACKLOG_GATE") == "1":
        result["skipped"] = "WQB_DISABLE_BACKLOG_GATE=1"
        return result
    cfg = dict(BACKLOG_GATE_DEFAULTS)
    thresholds_path = os.path.join(campaign_dir, "config", "thresholds.json")
    try:
        with open(thresholds_path, "r", encoding="utf-8") as f:
            thresholds = json.load(f)
        cfg.update((thresholds.get("diversity") or {}).get("backlog_gate") or {})
    except (OSError, json.JSONDecodeError):
        pass
    if cfg.get("enabled") is False:
        result["skipped"] = "backlog_gate disabled in thresholds.json"
        return result

    db_path = resolve_db_path()
    try:
        conn = connect_db_readonly(db_path)
        try:
            # 放行读取单源 = wqb.waiver（waiver_backlog_<region>_all → 旧键 backlog_gate_override）
            result.update(_waiver.gate_report_fields(_waiver.load(conn, "backlog", region)))

            total, bt, pending_gated, gem_n, selected_n = conn.execute(
                "SELECT COUNT(*), "
                "SUM(CASE WHEN status IN ('backtested','submitted','completed') THEN 1 ELSE 0 END), "
                "SUM(CASE WHEN status IN ('pending','gated') THEN 1 ELSE 0 END), "
                "SUM(CASE WHEN status='gem' THEN 1 ELSE 0 END), "
                "SUM(CASE WHEN status='selected' THEN 1 ELSE 0 END) "
                "FROM expressions WHERE region=?",
                (region,),
            ).fetchone()
        finally:
            conn.close()
    except Exception as e:
        result["warning"] = f"backlog gate could not read DB: {e}"
        return result

    total = int(total or 0)
    bt = int(bt or 0)
    pending_gated = int(pending_gated or 0)
    gem_n = int(gem_n or 0)
    selected_n = int(selected_n or 0)
    conversion = bt / total if total else 1.0
    pg_ratio = pending_gated / total if total else 0.0
    # 2026-09-17 P0-2：未消费 = gem + selected + pending + gated（回测之后才叫"已消费"）
    unconsumed = gem_n + selected_n + pending_gated
    uc_ratio = unconsumed / total if total else 0.0
    result["evidence"] = {
        "total": total, "backtested": bt, "pending_gated": pending_gated,
        "gem": gem_n, "selected": selected_n, "unconsumed": unconsumed,
        "conversion": round(conversion, 4), "pending_gated_ratio": round(pg_ratio, 4),
        "unconsumed_ratio": round(uc_ratio, 4),
        "unconsumed_enforced": bool(cfg.get("unconsumed_enforce")),
    }

    # 样本不足的新区不判
    if total < int(cfg["min_expressions"]):
        result["skipped"] = f"expression sample {total} < min {cfg['min_expressions']}"
        return result

    hits = []
    if conversion < float(cfg["conversion_min"]):
        hits.append(
            f"conversion={conversion:.1%}（{bt}/{total}）< {float(cfg['conversion_min']):.0%}："
            f"生成远超回测吞吐（S2→S3 断链），先消化近闸积压再开新波"
        )
    if pg_ratio > float(cfg["pending_gated_ratio_max"]):
        hits.append(
            f"pending+gated={pending_gated}/{total}（{pg_ratio:.0%}）> "
            f"{float(cfg['pending_gated_ratio_max']):.0%}：积压超限，本波应优先 "
            f"build_wave --from-db 重取近闸积压，而非新建表达式堆库"
        )
    uc_hit = uc_ratio > float(cfg["unconsumed_ratio_max"])
    if uc_hit:
        _msg = (
            f"未消费积压={unconsumed}/{total}（{uc_ratio:.0%}，其中 gem={gem_n} selected={selected_n} "
            f"pending+gated={pending_gated}）> {float(cfg['unconsumed_ratio_max']):.0%}："
            f"连最早期积压（gem/selected）也未被回测消化"
        )
        if cfg.get("unconsumed_enforce"):
            hits.append(_msg)
        else:
            # 灰度阶段：只记录不拦截（可经 thresholds 置 unconsumed_enforce=true 转为硬闸）
            result.setdefault("warnings", []).append(f"[灰度·未拦截] {_msg}")
    if not hits:
        return result
    result["hits"] = hits
    if result.get("override"):
        result["note"] = (f"积压闸命中但已被 ledger {result['waiver']['source_key']} 放行："
                          f"{result['override']['reason']}")
        return result
    result["success"] = False
    result["error"] = (
        f"积压闸拦截（{region}）：{'；'.join(hits)}。消化积压后再开新波；"
        f"确需继续（用户显式指令）请写 {_waiver.write_hint('backlog', region)}，或在 "
        f"{thresholds_path} 的 diversity.backlog_gate 调阈值。"
        f"{_waiver.rejected_note(_waiver_from_result(result))}"
    )
    return result


def _waiver_from_result(result: Dict[str, Any]) -> Optional["_waiver.Waiver"]:
    """闸结果里的 waiver 字典 → Waiver（只为 rejected_note 复用同一份措辞）。"""
    d = result.get("waiver")
    return _waiver.Waiver(**d) if isinstance(d, dict) else None


def _normalize_verdict(raw: Any) -> str:
    """把 `wave_results.verdict` 归一到 PASS|FAIL|PARTIAL|UNKNOWN（2026-09-17 P0-3）.

    背景（实测 2026-09-17）：verdict 列**不是干净枚举**。除 FAIL/PARTIAL/PASS 外还存有
    `0/6 过硬闸, 新高 0.31` / `0/8 过硬闸, 新高 0.43` 这类自由文本，以及 None / ''。
    旧规则 B 用 `all(v == "FAIL")` 判定，上述形态一律静默"不算 FAIL" → **停止闸失效**；
    JPN wave1 的 `verdict=None` 同理（`str(None or "")=""`）。

    2026-09-27 N30：归一规则只有一份——`wqb.wave_results_contract.normalize_verdict`（写入时用的
    同一张表）。此前这里另有一套：`3/8 过硬闸` 判 PARTIAL，写入契约判 PASS，同一文本两种枚举；
    也认不出 `GREEN:` / `RED:` / `全灭` 等写入契约早已归一的历史写法（只能给 UNKNOWN）。
    契约认不出的仍给 UNKNOWN：规则 B 只告警、不据此拦截。只做字符串语义归一，不 join 回测结果
    反推达标数（`backtest_results.wave` 在 DEU 写的是数据集名，join 不可靠）。
    """
    norm, _rule = _contract_normalize_verdict(raw)
    return norm or "UNKNOWN"


def _recent_closed_waves(conn: sqlite3.Connection, region: str, k: int) -> List[Tuple[str, Any]]:
    """停止规则 B 的窗口：按**波的开始时刻**取最近 k 个 closed 波，返回 [(wave_number, verdict)]（新→旧）。

    开始时刻 = 该波首次入库表达式的时间（`waves.created_at`，一波一行、此后不再改写）；
    没有表达式的波（探针 / 纯结论行）退到 `wave_results.created_at`。

    2026-09-27 R22（审计 N22）：此前按 `COALESCE(updated_at, created_at)` 排序——给任何旧波补记
    结论、补写 findings 都会把它顶进"最近 k 个"。KOR 真实复现：按 R20 的建议给旧波 91c 补记 PASS
    （91c 早于 92–97），窗口变成 [91c PASS, 97, …]，区域停波被解除、下一波放行。
    `wave_results.created_at` 只作兜底：旧版 toolkit `WaveResultsStore.upsert` 是 INSERT OR REPLACE，
    每写一次就重置它（N30 起改走写入契约的合并写入、保留 created_at，但库里已被重置过的旧行还在）；
    波号也曾按首个数字入库、与 waves 对不上（N30 起按原字符串）。两种时钟（本地 `T` / UTC 空格）先经 `local_ts` 统一；同一秒内按波号数字部分
    再按原串倒序。库里没有 waves / regions 表（最小库）时只按 `wave_results.created_at`。
    """
    tables = {name for (name,) in conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name IN ('waves', 'regions')")}
    if tables == {"waves", "regions"}:
        sql = ("SELECT wr.wave_number, wr.verdict, wr.created_at, "
               "(SELECT MIN(w.created_at) FROM waves w JOIN regions r ON r.id = w.region_id "
               " WHERE r.name = wr.region AND w.wave_number = wr.wave_number) "
               "FROM wave_results wr WHERE wr.region=? AND wr.status='closed'")
    else:
        sql = ("SELECT wave_number, verdict, created_at, NULL "
               "FROM wave_results WHERE region=? AND status='closed'")
    rows = conn.execute(sql, (region,)).fetchall()

    def started(row):
        wave, _verdict, wr_created, wave_created = row
        m = re.search(r"\d+", str(wave))
        return (local_ts(wave_created) or local_ts(wr_created),
                int(m.group()) if m else -1, str(wave))

    rows.sort(key=started, reverse=True)
    return [(str(r[0]), r[1]) for r in rows[:k]]


def _parse_dt_loose(value: Any) -> Optional[datetime]:
    """容错解析台账时间戳（'YYYY-MM-DD[ HH:MM:SS[.fff]]' / ISO T 分隔），失败返回 None。"""
    if not value:
        return None
    s = str(value).strip().replace("T", " ").rstrip("Z")
    for fmt in ("%Y-%m-%d %H:%M:%S.%f", "%Y-%m-%d %H:%M:%S", "%Y-%m-%d"):
        try:
            return datetime.strptime(s, fmt)
        except ValueError:
            continue
    return None


def _stop_rules_schema_supports_axis(conn) -> bool:
    """探测库 schema 是否支持规则 B 按轴计数（2026-09-23）。

    需要：wave_results 带 wave_number/verdict/status/created_at/updated_at；
    backtest_results 带 wave/dataset/sharpe；expressions（wave/dataset）、
    gate_results（wave）、registry_empirical（layer/payload/created_at）表齐备。
    缺任一项 → False，调用方回落旧口径（保守原则：零配额/dead_end 豁免需正面
    证据，拿不到证据保持旧行为——旧测试夹具即依赖此回落）。
    """
    def _cols(table: str) -> set:
        try:
            return {row[1] for row in conn.execute(f"PRAGMA table_info({table})")}
        except Exception:
            return set()

    def _has(table: str) -> bool:
        return conn.execute(
            "SELECT 1 FROM sqlite_master WHERE type='table' AND name=?", (table,)
        ).fetchone() is not None

    if not {"region", "wave_number", "verdict", "status",
            "created_at", "updated_at"} <= _cols("wave_results"):
        return False
    if not {"region", "wave", "dataset", "sharpe"} <= _cols("backtest_results"):
        return False
    if not _has("expressions") or not {"region", "wave", "dataset"} <= _cols("expressions"):
        return False
    if not _has("gate_results") or not {"region", "wave"} <= _cols("gate_results"):
        return False
    if not _has("registry_empirical") or not {
            "region", "layer", "payload", "created_at"} <= _cols("registry_empirical"):
        return False
    return True


def _axis_wave_metadata(conn, region: str, wave_number: Any) -> Dict[str, Any]:
    """单波按轴元数据：axis(dataset) / n_backtests / max_abs_sharpe / zero_cost。

    axis 取值序：backtest_results(wave=波号) → expressions(wave=波号) → None。
    zero_cost = 该波无任何回测且 gate_results 有该波记录（过了 gate 但从未回测）。
    波号对齐：wave_results.wave_number 与 backtest_results.wave / expressions.wave /
    gate_results.wave 都是 TEXT，比较一律走 str()。
    """
    wave = str(wave_number)
    n_bt, max_abs = conn.execute(
        "SELECT COUNT(*), MAX(ABS(sharpe)) FROM backtest_results WHERE region=? AND wave=?",
        (region, wave),
    ).fetchone()
    axis = None
    for table in ("backtest_results", "expressions"):
        row = conn.execute(
            f"SELECT dataset FROM {table} WHERE region=? AND wave=? "
            f"AND dataset IS NOT NULL AND dataset != '' LIMIT 1",
            (region, wave),
        ).fetchone()
        if row:
            axis = row[0]
            break
    zero_cost = False
    if int(n_bt or 0) == 0:
        zero_cost = conn.execute(
            "SELECT 1 FROM gate_results WHERE region=? AND wave=? LIMIT 1", (region, wave)
        ).fetchone() is not None
    return {
        "axis": axis,
        "n_backtests": int(n_bt or 0),
        "max_abs_sharpe": float(max_abs) if max_abs is not None else None,
        "zero_cost": zero_cost,
    }


def _dead_end_productive(
    wave_number: Any,
    wave_created: Any,
    wave_updated: Any,
    dead_rows: List[Any],
) -> bool:
    """该波是否产出新 dead_end（2026-09-23 豁免口径）。

    registry_empirical(layer='dead_end') 中 payload 提及该波号（如 `"wave": 216`），
    或 created_at 落在 [波 created_at, 波 updated_at + 2 天] 窗口内。
    """
    wn = str(wave_number)
    created = _parse_dt_loose(wave_created)
    updated = _parse_dt_loose(wave_updated) or created
    deadline = (updated + timedelta(days=2)) if updated else None
    for _id, payload, de_created in dead_rows:
        if wn and payload and wn in str(payload):
            return True
        de_dt = _parse_dt_loose(de_created)
        if de_dt and created and deadline and created <= de_dt <= deadline:
            return True
    return False


def _wall_routing_hint(waves: List[Dict[str, Any]], floor: float) -> Optional[str]:
    """撞墙型 FAIL（max|sharpe| ≥ floor）的路由提示：信号存在但结构性不可提交。"""
    wall = [w for w in waves
            if w.get("max_abs_sharpe") is not None and w["max_abs_sharpe"] >= floor]
    if not wall:
        return None
    detail = "/".join(f"{w['wave']}({w['max_abs_sharpe']:.2f})" for w in wall[:5])
    return (f"撞墙型 FAIL：波 {detail} max|sharpe| ≥ floor {floor}——"
            f"信号存在但结构性不可提交：优先 prod-first 探针/换 universe/换池，而非停区")


def _evaluate_stop_rules_axis(
    conn,
    region: str,
    dataset: Optional[str],
    cfg: Dict[str, Any],
    floor: float,
):
    """按轴口径（axis_scope=True）的规则 B：B1 同轴熔断 + B2 区级多轴停（2026-09-23）。

    取最近 axis_window 个 closed 波（verdict 已归一），逐波补元数据并分类：
      可计数 FAIL = verdict==FAIL 且非 zero_cost（开关）且非 dead_end_productive（开关）；
      豁免 FAIL 不计数也不打断连续性；非 FAIL（PASS/PARTIAL/UNKNOWN）打断连续失败。
      signal_class（wall / signal_absent / unknown）仅作 evidence 标注——信号缺席
      （max|sharpe| < floor）的拦截归 signal_floor 闸，与本闸正交分工。

    返回 (hits, waves)：hits 为拦截文案（含撞墙路由提示）；waves 为每波证据（最近在前）。
    """
    window = max(1, int(cfg.get("axis_window") or 8))
    k = int(cfg["consecutive_fail_waves"])
    d_axes = max(1, int(cfg.get("distinct_fail_axes") or 4))
    # 窗口排序与 `_recent_closed_waves` 同源（R22：按**波的开始时刻**，补记旧波不进窗口）。
    # 此前按 COALESCE(updated_at, created_at) 取窗——给旧波补记结论就把它顶进最近窗口，
    # 与 R22 语义相反（N30/p1_batch2 守护用例：补记 91c / s2_old_d1 后窗口仍应是 97/96/95）。
    _tables = {name for (name,) in conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name IN ('waves', 'regions')")}
    if _tables == {"waves", "regions"}:
        rows = conn.execute(
            "SELECT wr.wave_number, wr.verdict, wr.created_at, wr.updated_at, "
            "(SELECT MIN(w.created_at) FROM waves w JOIN regions r ON r.id = w.region_id "
            " WHERE r.name = wr.region AND w.wave_number = wr.wave_number) "
            "FROM wave_results wr WHERE wr.region=? AND wr.status='closed'",
            (region,)).fetchall()
    else:
        rows = conn.execute(
            "SELECT wave_number, verdict, created_at, updated_at, NULL "
            "FROM wave_results WHERE region=? AND status='closed'",
            (region,)).fetchall()

    def _started(row):
        wave, _v, wr_created, _u, wave_created = row
        m = re.search(r"\d+", str(wave))
        return (local_ts(wave_created) or local_ts(wr_created),
                int(m.group()) if m else -1, str(wave))

    rows = sorted(rows, key=_started, reverse=True)[:window]
    dead_rows = conn.execute(
        "SELECT id, payload, created_at FROM registry_empirical "
        "WHERE region=? AND layer='dead_end'",
        (region,),
    ).fetchall()
    waves: List[Dict[str, Any]] = []
    for wave_number, raw_verdict, created_at, updated_at, _wave_created in rows:
        meta = _axis_wave_metadata(conn, region, wave_number)
        verdict = _normalize_verdict(raw_verdict)
        zero_cost = bool(meta["zero_cost"]) and bool(cfg.get("exempt_zero_cost_waves", True))
        productive = False
        if cfg.get("exempt_dead_end_waves", True):
            productive = _dead_end_productive(wave_number, created_at, updated_at, dead_rows)
        countable = verdict == "FAIL" and not zero_cost and not productive
        # 信号分类（evidence 标注用，与 signal_floor 闸正交）：FAIL 波一律标注——
        # wall（信号存在但结构性不可提交）/ signal_absent（信号缺席，拦截归 signal_floor
        # 闸）/ unknown（无回测 sharpe 证据）；非 FAIL 波不标注。
        if verdict == "FAIL" and meta["max_abs_sharpe"] is not None:
            signal_class = "wall" if meta["max_abs_sharpe"] >= floor else "signal_absent"
        elif verdict == "FAIL":
            signal_class = "unknown"
        else:
            signal_class = None
        waves.append({
            "wave": str(wave_number),
            "verdict": verdict,
            "verdict_raw": None if raw_verdict is None else str(raw_verdict),
            "axis": meta["axis"],
            "n_backtests": meta["n_backtests"],
            "max_abs_sharpe": meta["max_abs_sharpe"],
            "zero_cost": zero_cost,
            "dead_end_productive": productive,
            "countable_fail": countable,
            "signal_class": signal_class,
        })

    hits: List[str] = []
    # B1 同轴熔断：仅当开波带 dataset（开波未定轴不判——不能因上一波的轴死了就拦新轴）
    if dataset:
        streak = 0
        involved: List[Dict[str, Any]] = []
        for w in waves:
            if w["axis"] != dataset:
                continue
            if w["countable_fail"]:
                streak += 1
                involved.append(w)
            elif w["verdict"] == "FAIL":
                continue  # 豁免 FAIL（零配额/dead_end）：不计数也不打断连续性
            else:
                break  # 非 FAIL（PASS/PARTIAL/UNKNOWN）打断连续失败
        if streak >= k:
            seq = "/".join(w["wave"] for w in involved[:k])
            hits.append(f"B: 轴 {dataset} 连续 {k} 波 FAIL（换数据集/换轴）——{seq}")
            hint = _wall_routing_hint(involved, floor)
            if hint:
                hits.append(hint)
    # B2 区级多轴停：窗口内无任何 PASS 且 ≥D 个不同轴全部 FAIL（多轴探索已证伪）
    if not any(w["verdict"] == "PASS" for w in waves):
        groups: Dict[Any, List[Dict[str, Any]]] = {}
        for w in waves:
            groups.setdefault(w["axis"], []).append(w)
        qualifying = []
        for axis, members in groups.items():
            if (all(m["verdict"] == "FAIL" for m in members)
                    and any(m["countable_fail"] for m in members)):
                qualifying.append((axis, [m for m in members if m["countable_fail"]]))
        if len(qualifying) >= d_axes:
            names = ", ".join(str(a) for a, _ in qualifying)
            hits.append(f"B: 窗口内 {len(qualifying)} 个不同轴全部 FAIL（{names}），"
                        f"多轴探索已证伪")
            hint = _wall_routing_hint([m for _, ms in qualifying for m in ms], floor)
            if hint:
                hits.append(hint)
    # B0 未定轴兜底（2026-09-27 合并对齐）：axis=None 的波既不进 B1（开波未定轴不判）
    # 也不满 B2（无轴组），于是「连续零回测 FAIL 波」（seed/台账只有 wave_results、
    # 无 backtest/expressions 关联）会让停止规则 B 被彻底架空——远端 P0 回归
    # test_stop_rule_b_survives_findings_only_update 的场景。窗口内无任何 PASS 且
    # axis=None 的可计数 FAIL 连续 ≥k → 区级兜底熔断（旧全区口径精神，保守止损）。
    # 豁免规则与 B1 相同：零配额/产 dead_end 的 FAIL 不计数也不打断连续性。
    if not any(w["verdict"] == "PASS" for w in waves):
        streak0 = 0
        seq0: List[Dict[str, Any]] = []
        for w in waves:
            if w["axis"] is None and w["countable_fail"]:
                streak0 += 1
                seq0.append(w)
            elif w["verdict"] == "FAIL":
                continue  # 豁免 FAIL / 有轴 FAIL：不计数也不打断未定轴连续段
            else:
                break  # 非 FAIL（PASS/PARTIAL/UNKNOWN）打断连续失败
        if streak0 >= k:
            seq = "/".join(w["wave"] for w in seq0[-k:])
            hits.append(f"B: 连续 {streak0} 波未定轴（零回测关联）FAIL"
                        f"（区级兜底熔断，换区/换主题）——{seq}")
    return hits, waves


def _run_stop_rules_gate(
    region: str,
    dataset: Optional[str],
    campaign_dir: str,
) -> Dict[str, Any]:
    """区域停止规则（2026-09-15 ⑦ SQL 化；2026-09-23 按轴改版；S2/S3 前置，零配额）。

    ra-pipeline「循环与停止」表里两条规则此前只是 prose，从未被任何代码判定：
      A. yield=0 且样本 ≥100 的区不要再投槽位（GBR 0/327 本应触发）
      B. 连续失败停区（旧口径：最近 K 个 closed 波 verdict 全 FAIL）
    现按库判定。用户显式覆盖：ledger `stop_rules_override`
    {"reason": "...", "until": "YYYY-MM-DD"(可选)} —— 命中即放行并记录覆盖原因
    （SOP：用户指令优先，但要在台账留痕）。

    2026-09-17 加固（P0-3）：规则 B 的输入先经 `_normalize_verdict` 归一 ——
    自由文本 `0/N 过硬闸` 归 FAIL，空值归 UNKNOWN。UNKNOWN 既不当作"通过"
    （会 WARN 提示补写），也不据此拦截（避免因台账缺写误停区域）。
    可选更严口径 `strict_no_pass=True`：最近 K 波"无任何 PASS"即停（两条路径均生效）。
    2026-09-27 R22：规则 B 的"最近 K 波"按波的开始时刻取，补记旧波不再改变窗口
    （见 `_recent_closed_waves`）；证据里的 `recent_closed_waves` 列出窗口内的波号。

    2026-09-23 按轴改版（axis_scope=True 且 schema 齐备时；否则完全回落旧口径）：
    轴 = region×dataset。连续失败计数器按轴作用域，换数据集/换轴即清零：
      B1 同轴熔断——开波带 dataset 时，该轴最近 closed 波序列中连续可计数 FAIL
        ≥ consecutive_fail_waves(K) → 拦截（换数据集/换轴）；
      B2 区级多轴停——最近 axis_window 个 closed 波窗口内无任何 PASS，且全部成员
        为 FAIL 的不同轴数 ≥ distinct_fail_axes(D) → 停区（多轴探索已证伪）。
    可计数 FAIL = verdict==FAIL 且非 UNKNOWN 且非零配额 FAIL（gate_results 有记录
    但 backtest_results 无记录，开关 exempt_zero_cost_waves）且非有信息产出的 FAIL
    （registry_empirical 新增 dead_end 提及该波，开关 exempt_dead_end_waves）。
    撞墙型 FAIL（波内 max|sharpe| ≥ floor）计数但附路由提示（优先 prod-first
    探针/换 universe/换池，而非停区）；信号缺席的拦截归 signal_floor 闸，与本闸
    正交（本闸只在 evidence 标注 signal_absent/wall）。
    """
    result: Dict[str, Any] = {"step": "stop_rules_gate", "success": True}
    # 测试/沙箱隔离口：WQB_DISABLE_STOP_RULES_GATE=1 时跳过（与 backlog 闸的
    # WQB_DISABLE_BACKLOG_GATE 并行）。本闸读真库 wave_results/backtest_results，
    # 命令拼装类单测不封库时会被 USA 等区的真实数据拦截（与被测行为无关的污染）。
    if os.environ.get("WQB_DISABLE_STOP_RULES_GATE") == "1":
        result["skipped"] = "WQB_DISABLE_STOP_RULES_GATE=1"
        return result
    cfg = dict(STOP_RULES_DEFAULTS)
    thresholds_path = os.path.join(campaign_dir, "config", "thresholds.json")
    thresholds: Dict[str, Any] = {}
    try:
        with open(thresholds_path, "r", encoding="utf-8") as f:
            thresholds = json.load(f)
        cfg.update((thresholds.get("diversity") or {}).get("stop_rules") or {})
    except (OSError, json.JSONDecodeError):
        pass
    if cfg.get("enabled") is False:
        result["skipped"] = "stop_rules disabled in thresholds.json"
        return result
    # 撞墙提示用的 sharpe floor：与 signal_floor 闸同源（diversity.signal_floor.
    # max_sharpe_floor，缺省 0.5）。信号缺席的拦截归 signal_floor 闸，本闸只标注。
    floor = float(((thresholds.get("diversity") or {}).get("signal_floor") or {}).get(
        "max_sharpe_floor", 0.5))

    db_path = resolve_db_path()
    axis_ready = False       # schema 齐备且 axis_scope=True → 按轴口径；否则旧口径
    axis_hits: List[str] = []
    waves: List[Dict[str, Any]] = []
    try:
        conn = connect_db_readonly(db_path)
        try:
            # 覆盖键
            # 放行读取单源 = wqb.waiver（waiver_stop_rules_<region>_all → 旧键 stop_rules_override）
            result.update(_waiver.gate_report_fields(_waiver.load(conn, "stop_rules", region)))
            # A. 区级产出率
            bt, passed = conn.execute(
                "SELECT COUNT(*), SUM(CASE WHEN sharpe > ? AND fitness > ? THEN 1 ELSE 0 END) "
                "FROM backtest_results WHERE region=? AND sharpe IS NOT NULL",
                (float(cfg["sharpe_min"]), float(cfg["fitness_min"]), region),
            ).fetchone()
            passed = int(passed or 0)
            k = int(cfg["consecutive_fail_waves"])
            # B. 最近 closed 波 verdict（原样取出，归一化统一在下方做）——
            #    按轴口径（schema 齐备且 axis_scope=True）取 axis_window 窗口并逐波
            #    补元数据；否则回落旧口径只取最近 K 个（R22：按波的开始时刻取窗口，
            #    补记旧波不再改变窗口，见 _recent_closed_waves）。
            axis_ready = bool(cfg.get("axis_scope", True)) and _stop_rules_schema_supports_axis(conn)
            if axis_ready:
                axis_hits, waves = _evaluate_stop_rules_axis(conn, region, dataset, cfg, floor)
                raw_verdicts = [w["verdict_raw"] for w in waves[:k]]
                window = [(w["wave"], w["verdict_raw"]) for w in waves[:k]]
            else:
                window = _recent_closed_waves(conn, region, k)
                raw_verdicts = [v for _w, v in window]
        finally:
            conn.close()
    except Exception as e:
        result["warning"] = f"stop_rules gate could not read DB: {e}"
        return result

    # 2026-09-17 加固：先归一化 verdict 再判定（自由文本/空值不再静默漏判）
    if axis_ready:
        verdicts = [w["verdict"] for w in waves[:k]]
    else:
        verdicts = [_normalize_verdict(v) for v in raw_verdicts]
    result["evidence"] = {
        "backtested": int(bt or 0),
        "passed": passed,
        "recent_closed_waves": [w for w, _v in window],
        "recent_closed_verdicts": verdicts,
        "recent_closed_verdicts_raw": [None if v is None else str(v) for v in raw_verdicts],
    }
    if axis_ready:
        result["evidence"]["axis_scope"] = True
        result["evidence"]["wave_details"] = waves
    hits = []
    if int(bt or 0) >= int(cfg["yield_min_backtests"]) and passed == 0:
        hits.append(f"A: {region} 已回测 {bt} 条、达标 0（≥{cfg['yield_min_backtests']} 样本零产出）")
    hits.extend(axis_hits)
    # B：归一化后判定。
    #   按轴口径：B1 同轴熔断 / B2 区级多轴停（见 _evaluate_stop_rules_axis）。
    #   旧口径 = 全 FAIL（与原语义一致，只是现在能识别 `0/N 过硬闸` 等自由文本形态）。
    #   UNKNOWN（空/不可识别）出现时**不**据此拦截，只 WARN —— 既不把"没写"当"通过"，
    #   也不因台账缺写误停区域。
    unknowns = [v for v in verdicts if v == "UNKNOWN"]
    # 轴信息退化（窗口内所有波都推不出 dataset 轴：无回测/表达式行的结论波）→ 按轴判不
    # 出 B1/B2，回落旧口径的"全 FAIL"判定（R22 用例夹具即此形态；不回落则闸对它们失明）。
    axis_degenerate = axis_ready and bool(verdicts) and all(
        w.get("axis") is None for w in waves[:k])
    if len(verdicts) >= k and not unknowns:
        if cfg.get("strict_no_pass"):
            if not any(v == "PASS" for v in verdicts):
                hits.append(f"B: 最近 {k} 个 closed 波无任何 PASS（{'/'.join(verdicts)}）")
        elif (not axis_ready or axis_degenerate) and all(v == "FAIL" for v in verdicts):
            hits.append(f"B: 最近 {k} 个 closed 波 verdict 全 FAIL")
    if unknowns and cfg.get("unknown_warn", True):
        result["warning"] = (
            f"{len(unknowns)}/{len(verdicts)} 个最近 closed 波 verdict 为空或不可识别"
            f"（{len(unknowns)} 个）——规则 B 本次不据此拦截；"
            f"请回写 verdict（探针/全灭波也应写 FAIL，勿留空壳 closed 记录）。"
        )
    if not hits:
        return result
    result["hits"] = hits
    if result.get("override"):
        result["note"] = (f"停止规则命中但已被 ledger {result['waiver']['source_key']} 放行："
                          f"{result['override']['reason']}")
        return result
    result["success"] = False
    result["error"] = (
        f"停止规则拦截（{region}）：{'；'.join(hits)}。继续开波只会重复烧槽位——"
        f"换区域/换 universe/换数据集；确需继续（用户显式指令）请写 {_waiver.write_hint('stop_rules', region)}，或在 "
        f"{thresholds_path} 的 diversity.stop_rules 调阈值。"
        f"{_waiver.rejected_note(_waiver_from_result(result))}"
    )
    return result


#: 信号天花板闸默认参数（区域 thresholds.json `diversity.signal_floor` 可覆盖）
#: 2026-09-17 #8：整节缺失时**不再静默放行**，改为回落本默认值继续判定（fail-closed）。
SIGNAL_FLOOR_DEFAULTS = {
    "enabled": True,
    "max_sharpe_floor": 0.5,
    "min_batches": 2,
}


def _run_signal_floor_gate(
    region: str,
    dataset: Optional[str],
    campaign_dir: str,
) -> Dict[str, Any]:
    """区域信号天花板闸（S2/S3 前置，2026-09-06 接线）.

    背景：`tracking/<REGION>/config/thresholds.json` 的 `diversity.signal_floor`
    早就写好了参数与语义——"连续 min_batches 批 max|sharpe| < floor 即判信号
    天花板，停止生成/增强并转区域决策"——实现也在
    `wqb.expression._enhancer.signal_evidence_gate()`，但**没有任何调用方**：
    不在 toolkit 脚本里、不在节点里、也没有 skill 引用，配置项从头到尾没人读。

    代价是实测出来的：GBR 按自己的配置该在第 2 批停，实际跑了 180 条回测、
    max|sharpe|=1.04、avg=0.41、达标 0 条。本函数把这道闸接进真正的执行路径。

    判定只用已落库的回测结果（零平台调用、零配额）。

    2026-09-17 #8 加固（fail-open → fail-closed）：旧行为是"缺 `signal_floor` 整节
    即静默放行"，与停止闸使命矛盾（GBR 曾因此跑满 180 条回测、max|sharpe|=1.04、
    达标 0 条）。现改为：读不到 thresholds.json 或整节缺失时，**回落
    `SIGNAL_FLOOR_DEFAULTS` 继续判定**并输出 `warning` 提示补配置；
    只有显式 `enabled: false` 才放行。
    """
    result: Dict[str, Any] = {"step": "signal_floor_gate", "success": True}
    # 测试/沙箱隔离口：WQB_DISABLE_SIGNAL_FLOOR_GATE=1 时跳过（与 backlog/stop_rules
    # 闸的 WQB_DISABLE_* 并行）。本闸读真库最近批次的回测 sharpe——USA 真实数据
    # 近 2 批 max=0.88 会触发天花板判定，让命令拼装类单测因环境而非行为失败。
    # （旧注释自述"只能靠'无回测证据即跳过'侥幸不爆"，此开关补齐三闸隔离的最后一环。）
    if os.environ.get("WQB_DISABLE_SIGNAL_FLOOR_GATE") == "1":
        result["skipped"] = "WQB_DISABLE_SIGNAL_FLOOR_GATE=1"
        return result

    thresholds_path = os.path.join(campaign_dir, "config", "thresholds.json")
    thresholds: Dict[str, Any] = {}
    try:
        with open(thresholds_path, "r", encoding="utf-8") as f:
            thresholds = json.load(f)
    except (OSError, json.JSONDecodeError) as e:
        result["warning"] = (
            f"thresholds.json 不可读（{type(e).__name__}）——已回落默认 signal_floor "
            f"{SIGNAL_FLOOR_DEFAULTS}（fail-closed），请补 {thresholds_path}"
        )

    cfg = dict(SIGNAL_FLOOR_DEFAULTS)
    configured = (thresholds.get("diversity") or {}).get("signal_floor")
    if isinstance(configured, dict):
        cfg.update(configured)
    elif configured is None:
        result["warning"] = (
            (result.get("warning") + "；" if result.get("warning") else "")
            + f"thresholds.json 缺 diversity.signal_floor 整节——已按默认 "
              f"floor={SIGNAL_FLOOR_DEFAULTS['max_sharpe_floor']} / "
              f"min_batches={SIGNAL_FLOOR_DEFAULTS['min_batches']} 判定（fail-closed）；"
              f"如需关闭请显式设 enabled:false"
        )
    if cfg.get("enabled") is False:
        result["skipped"] = "signal_floor disabled in thresholds.json"
        return result

    floor = float(cfg.get("max_sharpe_floor", 0.5))
    min_batches = int(cfg.get("min_batches", 2))

    # 取该 region（有 dataset 则再限定 dataset）最近若干波的回测结果。
    # 每个 wave 记为一"批"，与 signal_evidence_gate 的 batch_idx 语义对齐。
    # 口径：thresholds.json 说的是"**连续** min_batches 批"，不是全历史。
    # 取全历史会让闸永不触发 —— GBR 跑了 20 批、全局 max|sharpe|=1.04 > floor 0.5，
    # 哪怕最近 10 批全是 0.3 也照样判 ok。所以只看最近 min_batches 个波次。
    # 2026-09-17 一致性修复：改用 resolve_db_path()，与另两道闸及 WQB_DB_PATH 契约对齐。
    # 此前硬编码 REPO_ROOT/data/wqb.db，导致设了 WQB_DB_PATH 的单测/沙箱仍读真库
    #（本闸因此在 tests 里无法隔离，只能靠"无回测证据即跳过"侥幸不爆）。
    db_path = resolve_db_path()
    rows: List[Dict[str, Any]] = []
    recent_waves: List[str] = []
    try:
        conn = connect_db_readonly(db_path)
        try:
            where = "region=? AND sharpe IS NOT NULL"
            params: List[Any] = [region]
            if dataset:
                where += " AND dataset=?"
                params.append(dataset)

            # 最近 min_batches 个波次（按该波最后一条回测的时间排序）
            recent_waves = [
                str(w) for (w,) in conn.execute(
                    f"SELECT wave FROM backtest_results WHERE {where} AND wave IS NOT NULL "
                    f"GROUP BY wave ORDER BY MAX(id) DESC LIMIT ?",
                    params + [min_batches],
                )
            ]
            if recent_waves:
                placeholders = ",".join("?" * len(recent_waves))
                query_params = params + recent_waves
                for sharpe, wave_id in conn.execute(
                    f"SELECT sharpe, wave FROM backtest_results "
                    f"WHERE {where} AND wave IN ({placeholders})",
                    query_params,
                ):
                    rows.append({"sharpe": sharpe, "batch_idx": wave_id})
        finally:
            conn.close()
    except Exception as e:  # DB 不可读不阻断，只记录
        result["warning"] = f"signal_floor gate could not read DB: {e}"
        return result

    if not rows:
        result["skipped"] = "no backtest evidence yet"
        return result

    result["window"] = {"recent_waves": recent_waves, "results": len(rows)}

    # 证据不足以构成"连续 N 批"时不判死（新区域/新数据集应当有试探空间）
    if len(recent_waves) < min_batches:
        result["skipped"] = (
            f"evidence only spans {len(recent_waves)} batch(es), "
            f"need {min_batches} to judge a ceiling"
        )
        return result

    try:
        # 走 diversity_enhancer 门面而非 _enhancer 私有模块：后者被 _metrics
        # 在模块底部反向 import，直接进 _enhancer 会撞循环导入。
        from wqb.expression.diversity_enhancer import signal_evidence_gate
    except ImportError as e:
        result["warning"] = f"signal_evidence_gate unavailable: {e}"
        return result

    verdict = signal_evidence_gate(rows, max_sharpe_floor=floor, min_batches=min_batches)
    result["verdict"] = verdict
    result["scope"] = f"{region}/{dataset}" if dataset else region
    if not verdict.get("passed", True):
        result["success"] = False
        result["error"] = (
            f"信号天花板闸拦截（{result['scope']}）：{verdict.get('message')}。"
            f"继续生成/回测只会重复烧槽位——请换 universe / 换数据集 / 换区域，"
            f"或在 {thresholds_path} 里把 diversity.signal_floor.enabled 设为 false "
            f"并在台账记录理由。"
        )
    return result


def run_open_wave_gates(
    region: str,
    dataset: Optional[str],
    campaign_dir: str,
) -> Tuple[List[Dict[str, Any]], Optional[str]]:
    """三道开波闸：信号天花板 → 停止规则 → 积压，任一拦截即停。返回 (各闸结果, 拦截原因 | None)。

    全部是只读 DB 判定、零配额，干跑也走——干跑就该回答"这个区还值不值得开波 / 发批"。
    campaign 节点的 S2 / S3 与 batch_track 节点（2026-09-27 R5）共用本函数；toolkit 的
    `_lib/region_gates` 逐个调用同样三个闸函数。
    """
    steps: List[Dict[str, Any]] = []
    for gate in (_run_signal_floor_gate, _run_stop_rules_gate, _run_backlog_gate):
        res = gate(region, dataset, campaign_dir)
        steps.append(res)
        if not res.get("success", True):
            return steps, res.get("error") or f"{res.get('step', gate.__name__)} 拦截"
    return steps, None
