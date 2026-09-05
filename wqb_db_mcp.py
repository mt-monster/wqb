# -*- coding: utf-8 -*-
"""wqb-db-mcp — 本地 wqb.db 查询 MCP 服务（单轨 DB 模式）。

职责：查询本地 SQLite 数据库（wave_results / registry_empirical / ledger_kv / alphas 等），
     供 skills 在战役流程中快速获取历史结论/台账/候选信息。

与 wqb-mcp 的边界：
  - wqb-mcp：BRAIN 平台 API（回测/提交/论坛），需联网 + 凭据
  - wqb-db-mcp：本地数据库读写（wave_results / registry_empirical / ledger_kv upsert）

工具清单：
  wave_results 查询：get_wave_result / list_wave_results / get_latest_wave
  registry 查询：get_region_config / get_dead_ends / get_campaigns / get_cross_region_lessons
  ledger 查询：get_ledger_key / list_ledger_keys / get_submit_ready / get_dead_datasets
  alpha 查询：get_alpha_by_id / list_alphas_by_wave / search_alphas_by_sharpe
  综合查询：get_campaign_summary / get_region_overview
  写工具（upsert 幂等）：upsert_ledger_key / upsert_wave_result / upsert_registry_empirical
  战役产物：upsert_expressions / list_expressions / upsert_field_catalog / get_field_catalog
            / upsert_backtest_rows / upsert_gate_result / get_gate_result
  备选因子池：get_salvage_pool（Mode B 组合辅助腿消费接口）
"""
import json
import logging
import re
import sqlite3
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

from mcp.server.fastmcp import FastMCP

# 数据库路径（wqb_db_mcp.py 在 wqb 工作区根目录）
ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))
DB_PATH = ROOT / "data" / "wqb.db"

from wqb.store import CampaignStore  # noqa: E402


def _store() -> CampaignStore:
    return CampaignStore(str(DB_PATH))

mcp = FastMCP(
    "wqb-db-mcp",
    "Local wqb.db query service (single-track DB mode)",
)


def _conn():
    """获取数据库连接（row_factory=Row）。"""
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys=ON")
    return conn


def _rows_to_dicts(rows):
    """sqlite3.Row 列表转 dict 列表。"""
    return [dict(r) for r in rows]


def _parse_json_fields(row, fields):
    """解析 row 中的 JSON 字段。"""
    for f in fields:
        if row.get(f) and isinstance(row[f], str):
            try:
                row[f] = json.loads(row[f])
            except Exception:
                logging.getLogger(__name__).debug("swallowed exception", exc_info=True)
    return row


# ---------------- wave_results 查询 ----------------

@mcp.tool()
def get_wave_result(region: str, wave_number: int) -> Dict[str, Any]:
    """获取单个 wave 结果台账。

    Args:
        region: 区域（MEA/USA/KOR/ASI/EUR/GBR/HKG/IND/GLB/DEU）
        wave_number: 波次编号

    Returns:
        wave 结果 dict（含 key_findings/candidates/batches/verdict/full_payload）
    """
    conn = _conn()
    c = conn.cursor()
    c.execute(
        "SELECT * FROM wave_results WHERE region=? AND wave_number=?",
        (region, wave_number),
    )
    row = c.fetchone()
    conn.close()
    if not row:
        return {"error": f"wave not found: {region} wave{wave_number}"}
    result = dict(row)
    return _parse_json_fields(result, ["key_findings", "candidates", "batches", "full_payload"])


@mcp.tool()
def list_wave_results(
    region: Optional[str] = None,
    status: Optional[str] = None,
    archived: Optional[bool] = None,
    limit: int = 50,
) -> List[Dict[str, Any]]:
    """列出 wave 结果（可按 region/status/archived 过滤）。

    ⚠️ wave 编号仅区域内唯一（各区域独立递增）。省略 region 会返回跨区域
    混排列表，解读波号时须以 region 字段区分（如 KOR-w170 ≠ MEA-w170）。

    Args:
        region: 区域过滤（可选，跨区域查询强烈建议传）
        status: 状态过滤（open/closed，可选）
        archived: 是否归档（可选）
        limit: 返回数量上限

    Returns:
        wave 结果列表（按 region + 数值波号降序）
    """
    conn = _conn()
    c = conn.cursor()
    sql = "SELECT * FROM wave_results WHERE 1=1"
    params = []
    if region:
        sql += " AND region=?"
        params.append(region)
    if status:
        sql += " AND status=?"
        params.append(status)
    if archived is not None:
        sql += " AND archived=?"
        params.append(1 if archived else 0)
    sql += " ORDER BY region, CAST(wave_number AS INTEGER) DESC LIMIT ?"
    params.append(limit)
    c.execute(sql, params)
    rows = _rows_to_dicts(c.fetchall())
    conn.close()
    return [_parse_json_fields(r, ["key_findings", "candidates", "batches"]) for r in rows]


@mcp.tool()
def get_latest_wave(region: str, status: Optional[str] = None) -> Dict[str, Any]:
    """获取某区域最新 wave。

    Args:
        region: 区域
        status: 状态过滤（可选，如 "closed"）

    Returns:
        最新 wave 结果 dict
    """
    conn = _conn()
    c = conn.cursor()
    sql = "SELECT * FROM wave_results WHERE region=?"
    params = [region]
    if status:
        sql += " AND status=?"
        params.append(status)
    sql += " ORDER BY CAST(wave_number AS INTEGER) DESC LIMIT 1"
    c.execute(sql, params)
    row = c.fetchone()
    conn.close()
    if not row:
        return {"error": f"no wave found for region={region}"}
    result = dict(row)
    return _parse_json_fields(result, ["key_findings", "candidates", "batches", "full_payload"])


# ---------------- registry 查询 ----------------

@mcp.tool()
def get_region_config(region: str) -> Dict[str, Any]:
    """获取区域静态配置（universe 档位 / 默认 neutralization / EVENT 字段规则）。

    Args:
        region: 区域

    Returns:
        区域配置 dict
    """
    conn = _conn()
    c = conn.cursor()
    c.execute("SELECT * FROM regions WHERE name=?", (region,))
    row = c.fetchone()
    conn.close()
    if not row:
        return {"error": f"region not found: {region}"}
    result = dict(row)
    # P1 fix: parse the real JSON columns, not the non-existent "config" column.
    return _parse_json_fields(result, ["universe_legal", "delay_legal"])


@mcp.tool()
def get_dead_ends(region: Optional[str] = None) -> List[Dict[str, Any]]:
    """获取死路清单（registry_empirical 表的 dead_end 层）。

    Args:
        region: 区域过滤（可选，None=全部区域）

    Returns:
        死路列表（含 family/reason/rule/dead_at）
    """
    conn = _conn()
    c = conn.cursor()
    sql = "SELECT * FROM registry_empirical WHERE layer='dead_end'"
    params = []
    if region:
        sql += " AND region=?"
        params.append(region)
    sql += " ORDER BY region, dead_at DESC"
    c.execute(sql, params)
    rows = _rows_to_dicts(c.fetchall())
    conn.close()
    return [_parse_json_fields(r, ["payload"]) for r in rows]


@mcp.tool()
def get_campaigns(region: Optional[str] = None, status: Optional[str] = None) -> List[Dict[str, Any]]:
    """获取战役清单（registry_empirical 表的 campaign 层）。

    Args:
        region: 区域过滤（可选）
        status: 状态过滤（untried/in_progress/exhausted，可选）

    Returns:
        战役列表（含 dataset/status/note）
    """
    conn = _conn()
    c = conn.cursor()
    sql = "SELECT * FROM registry_empirical WHERE layer='campaign'"
    params = []
    if region:
        sql += " AND region=?"
        params.append(region)
    c.execute(sql, params)
    rows = _rows_to_dicts(c.fetchall())
    conn.close()
    results = [_parse_json_fields(r, ["payload"]) for r in rows]
    # status 过滤（在 payload 里）
    if status:
        results = [r for r in results if r.get("payload", {}).get("status") == status]
    return results


@mcp.tool()
def get_cross_region_lessons() -> List[Dict[str, Any]]:
    """获取跨区域铁律（GLB emotion 死路 / anl15 封禁 / 非法 universe 档）。

    数据来源：registry_empirical (layer='cross_region')。

    Returns:
        跨区教训列表
    """
    conn = _conn()
    c = conn.cursor()
    c.execute(
        "SELECT entry_id as lesson_id, family, payload FROM registry_empirical "
        "WHERE layer='cross_region' ORDER BY entry_id"
    )
    results = []
    for row in c.fetchall():
        d = _rows_to_dicts([row])[0]
        payload = d.get("payload")
        if isinstance(payload, str):
            import json as _json
            try:
                payload = _json.loads(payload)
            except Exception:
                payload = {}
        lesson = {
            "lesson_id": d.get("lesson_id"),
            "family": d.get("family"),
            "finding": payload.get("finding", "") if isinstance(payload, dict) else "",
            "rule": payload.get("rule", "") if isinstance(payload, dict) else "",
        }
        results.append(lesson)
    conn.close()
    return results


# ---------------- ledger 查询 ----------------

@mcp.tool()
def get_ledger_key(region: str, key: str) -> Any:
    """获取战役台账单个 key 的值。

    Args:
        region: 区域
        key: 台账 key（如 "submit_ready" / "pv1_dead" / "wave46_verdict"）

    Returns:
        key 对应的值（任意 JSON）
    """
    conn = _conn()
    c = conn.cursor()
    c.execute(
        "SELECT value FROM ledger_kv WHERE region=? AND key=?",
        (region, key),
    )
    row = c.fetchone()
    conn.close()
    if not row:
        return {"error": f"ledger key not found: {region}/{key}"}
    try:
        return json.loads(row[0])
    except Exception:
        return row[0]


@mcp.tool()
def list_ledger_keys(region: str) -> List[str]:
    """列出某区域台账全部 key。

    Args:
        region: 区域

    Returns:
        key 列表
    """
    conn = _conn()
    c = conn.cursor()
    c.execute("SELECT key FROM ledger_kv WHERE region=? ORDER BY key", (region,))
    keys = [r[0] for r in c.fetchall()]
    conn.close()
    return keys


@mcp.tool()
def get_submit_ready(region: str) -> List[Dict[str, Any]]:
    """获取某区域 submit_ready 候选列表（ledger_kv 的 submit_ready key）。

    Args:
        region: 区域

    Returns:
        submit_ready 候选列表
    """
    result = get_ledger_key(region, "submit_ready")
    if isinstance(result, dict) and "error" in result:
        return []
    return result if isinstance(result, list) else []


@mcp.tool()
def get_dead_datasets(region: str) -> List[str]:
    """获取某区域判死数据集列表（ledger_kv 的 *_dead keys）。

    Args:
        region: 区域

    Returns:
        判死数据集名列表
    """
    conn = _conn()
    c = conn.cursor()
    c.execute(
        "SELECT key FROM ledger_kv WHERE region=? AND key LIKE '%_dead'",
        (region,),
    )
    keys = [r[0].replace("_dead", "") for r in c.fetchall()]
    conn.close()
    return keys


# ---------------- alpha 查询 ----------------

@mcp.tool()
def get_alpha_by_id(alpha_id: str) -> Dict[str, Any]:
    """根据 alpha id 获取 alpha 详情。

    Args:
        alpha_id: BRAIN 平台 alpha id

    Returns:
        alpha 详情 dict
    """
    conn = _conn()
    c = conn.cursor()
    c.execute(
        "SELECT a.*, r.name AS region FROM alphas a "
        "JOIN regions r ON a.region_id = r.id "
        "WHERE a.alpha_id=?",
        (alpha_id,),
    )
    row = c.fetchone()
    conn.close()
    if not row:
        return {"error": f"alpha not found: {alpha_id}"}
    return dict(row)


@mcp.tool()
def list_alphas_by_wave(region: str, wave_number: int) -> List[Dict[str, Any]]:
    """列出某 wave 的全部 alpha。

    Args:
        region: 区域
        wave_number: 波次编号

    Returns:
        alpha 列表
    """
    conn = _conn()
    c = conn.cursor()
    # 先通过 regions 表查 region_id，再联合 waves 查数据
    c.execute(
        "SELECT a.*, r.name AS region, w.wave_number "
        "FROM alphas a "
        "JOIN regions r ON a.region_id = r.id "
        "JOIN waves w ON a.region_id = w.region_id AND a.dataset_id = w.dataset_id "
        "WHERE r.name=? AND w.wave_number=?",
        (region, str(wave_number)),
    )
    rows = _rows_to_dicts(c.fetchall())
    conn.close()
    return rows


@mcp.tool()
def search_alphas_by_sharpe(
    region: Optional[str] = None,
    min_sharpe: float = 1.0,
    limit: int = 20,
) -> List[Dict[str, Any]]:
    """按 sharpe 搜索 alpha（sharpe >= min_sharpe）。

    ⚠️ alpha 跨区域独立编号，省略 region 的结果为跨区域混排榜单，
    波号须配合返回的 region 字段解读。

    Args:
        region: 区域过滤（可选）
        min_sharpe: 最小 sharpe
        limit: 返回数量上限

    Returns:
        alpha 列表（按 sharpe 降序）
    """
    conn = _conn()
    c = conn.cursor()
    sql = (
        "SELECT a.*, r.name AS region FROM alphas a "
        "JOIN regions r ON a.region_id = r.id "
        "WHERE a.sharpe >= ?"
    )
    params = [min_sharpe]
    if region:
        sql += " AND r.name=?"
        params.append(region)
    sql += " ORDER BY a.sharpe DESC LIMIT ?"
    params.append(limit)
    c.execute(sql, params)
    rows = _rows_to_dicts(c.fetchall())
    conn.close()
    return rows


# ---------------- 综合查询 ----------------

@mcp.tool()
def get_campaign_summary(region: str) -> Dict[str, Any]:
    """获取某区域战役摘要（wave 数 / 候选数 / 死路数 / 最新 wave）。

    Args:
        region: 区域

    Returns:
        战役摘要 dict
    """
    conn = _conn()
    c = conn.cursor()
    # wave 统计
    c.execute(
        "SELECT COUNT(*) as total, SUM(CASE WHEN status='closed' THEN 1 ELSE 0 END) as closed FROM wave_results WHERE region=?",
        (region,),
    )
    wave_stats = dict(c.fetchone())
    # 最新 wave
    c.execute(
        "SELECT wave_number, focus, status FROM wave_results WHERE region=? "
        "ORDER BY CAST(wave_number AS INTEGER) DESC LIMIT 1",
        (region,),
    )
    latest_wave = c.fetchone()
    latest_wave = dict(latest_wave) if latest_wave else None
    # 死路数
    c.execute(
        "SELECT COUNT(*) FROM registry_empirical WHERE region=? AND layer='dead_end'",
        (region,),
    )
    dead_ends = c.fetchone()[0]
    # submit_ready 数
    c.execute(
        "SELECT value FROM ledger_kv WHERE region=? AND key='submit_ready'",
        (region,),
    )
    sr_row = c.fetchone()
    submit_ready_count = 0
    if sr_row:
        try:
            sr_list = json.loads(sr_row[0])
            submit_ready_count = len(sr_list) if isinstance(sr_list, list) else 0
        except Exception:
            logging.getLogger(__name__).debug("swallowed exception", exc_info=True)
    conn.close()
    return {
        "region": region,
        "waves": wave_stats,
        "latest_wave": latest_wave,
        "dead_ends": dead_ends,
        "submit_ready": submit_ready_count,
    }


@mcp.tool()
def get_region_overview() -> List[Dict[str, Any]]:
    """获取全部区域概览（wave 数 / 最新 wave / 死路数）。

    Returns:
        区域概览列表
    """
    conn = _conn()
    c = conn.cursor()
    c.execute("SELECT DISTINCT region FROM wave_results ORDER BY region")
    regions = [r[0] for r in c.fetchall()]
    conn.close()
    return [get_campaign_summary(r) for r in regions]


# ---------------- 写工具（upsert，幂等） ----------------

import datetime


def _now() -> str:
    return datetime.datetime.now().isoformat(timespec="seconds")


@mcp.tool()
def upsert_ledger_key(region: str, key: str, value: Any) -> Dict[str, Any]:
    """写台账单个 key（幂等 upsert）。

    用于 submit_ready / wave<N>_verdict / last_submission / *_dead 等台账键的写入。
    value 为任意 JSON 可序列化对象（list/dict/str/int）。

    Args:
        region: 区域
        key: 台账 key
        value: 任意 JSON 值

    Returns:
        {"action": "inserted"|"updated", "region": ..., "key": ...}
    """
    conn = _conn()
    c = conn.cursor()
    payload = json.dumps(value, ensure_ascii=False)
    c.execute("SELECT id FROM ledger_kv WHERE region=? AND key=?", (region, key))
    row = c.fetchone()
    if row:
        c.execute(
            "UPDATE ledger_kv SET value=?, updated_at=? WHERE region=? AND key=?",
            (payload, _now(), region, key),
        )
        action = "updated"
    else:
        c.execute(
            "INSERT INTO ledger_kv (region, key, value, created_at, updated_at) VALUES (?,?,?,?,?)",
            (region, key, payload, _now(), _now()),
        )
        action = "inserted"
    conn.commit()
    conn.close()
    return {"action": action, "region": region, "key": key}


@mcp.tool()
def upsert_wave_result(
    region: str,
    wave_number: int,
    focus: Optional[str] = None,
    context: Optional[str] = None,
    key_findings: Optional[Any] = None,
    candidates: Optional[Any] = None,
    batches: Optional[Any] = None,
    verdict: Optional[str] = None,
    status: str = "closed",
    source_file: Optional[str] = None,
    full_payload: Optional[Any] = None,
) -> Dict[str, Any]:
    """同步 wave 结果到 wave_results 表（幂等 upsert，按 region+wave_number）。

    key_findings/candidates/batches/full_payload 传 JSON 可序列化对象，自动序列化。

    Args:
        region: 区域
        wave_number: 波次编号
        focus: 本波焦点
        context: 背景上下文
        key_findings: 关键发现 list
        candidates: 候选 list
        batches: 批次 list
        verdict: 结论
        status: 状态（open/closed，默认 closed）
        source_file: 源文件路径
        full_payload: 完整 payload dict

    Returns:
        {"action": "inserted"|"updated", "region": ..., "wave_number": ...}
    """
    conn = _conn()
    c = conn.cursor()
    kf = json.dumps(key_findings, ensure_ascii=False) if key_findings is not None else None
    cand = json.dumps(candidates, ensure_ascii=False) if candidates is not None else None
    bat = json.dumps(batches, ensure_ascii=False) if batches is not None else None
    fp = json.dumps(full_payload, ensure_ascii=False) if full_payload is not None else None
    c.execute(
        "SELECT id FROM wave_results WHERE region=? AND wave_number=?",
        (region, wave_number),
    )
    row = c.fetchone()
    if row:
        c.execute(
            """UPDATE wave_results SET focus=?, context=?, key_findings=?, candidates=?,
               batches=?, verdict=?, status=?, source_file=?, full_payload=?, updated_at=?
               WHERE region=? AND wave_number=?""",
            (focus, context, kf, cand, bat, verdict, status, source_file, fp, _now(), region, wave_number),
        )
        action = "updated"
    else:
        c.execute(
            """INSERT INTO wave_results
               (region, wave_number, focus, context, key_findings, candidates, batches,
                verdict, status, source_file, archived, created_at, updated_at, full_payload)
               VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
            (region, wave_number, focus, context, kf, cand, bat, verdict, status,
             source_file, 0, _now(), _now(), fp),
        )
        action = "inserted"
    conn.commit()
    conn.close()
    return {"action": action, "region": region, "wave_number": wave_number}


@mcp.tool()
def upsert_registry_empirical(
    region: str,
    layer: str,
    entry_id: str,
    payload: Any,
    family: Optional[str] = None,
    dead_at: Optional[str] = None,
) -> Dict[str, Any]:
    """回写 registry 实证层（幂等 upsert，按 region+layer+entry_id）。

    layer ∈ {dead_end, campaign, win}。payload 为该条的完整 dict（自动序列化）。

    Args:
        region: 区域
        layer: 层（dead_end/campaign/win）
        entry_id: 条目 id（如 MEA-MDL31-CHG-WEAK）
        payload: 完整 payload dict
        family: 信号族名（可选）
        dead_at: 判死日期（可选，dead_end 层用）

    Returns:
        {"action": "inserted"|"updated", "region": ..., "layer": ..., "entry_id": ...}
    """
    conn = _conn()
    c = conn.cursor()
    pl = json.dumps(payload, ensure_ascii=False)
    c.execute(
        "SELECT id FROM registry_empirical WHERE region=? AND layer=? AND entry_id=?",
        (region, layer, entry_id),
    )
    row = c.fetchone()
    if row:
        c.execute(
            "UPDATE registry_empirical SET family=?, payload=?, dead_at=?, updated_at=? WHERE region=? AND layer=? AND entry_id=?",
            (family, pl, dead_at, _now(), region, layer, entry_id),
        )
        action = "updated"
    else:
        c.execute(
            "INSERT INTO registry_empirical (region, layer, entry_id, family, payload, dead_at, created_at, updated_at) VALUES (?,?,?,?,?,?,?,?)",
            (region, layer, entry_id, family, pl, dead_at, _now(), _now()),
        )
        action = "inserted"
    conn.commit()
    conn.close()
    return {"action": action, "region": region, "layer": layer, "entry_id": entry_id}


@mcp.tool()
def upsert_expressions(
    region: str,
    wave: str,
    expressions: Any,
    dataset: Optional[str] = None,
    status: str = "pending",
) -> Dict[str, Any]:
    """写入本波表达式（幂等，按 region+wave+expression）。

    expressions 为字符串列表或 {expression/expr/code, status, settings} 对象列表。
    """
    store = _store()
    try:
        return store.upsert_expressions(region, str(wave), expressions or [], dataset=dataset, status=status)
    finally:
        store.close()


@mcp.tool()
def list_expressions(
    region: str,
    wave: str,
    dataset: Optional[str] = None,
    status: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """列出某波表达式。"""
    store = _store()
    try:
        return store.list_expressions(region, str(wave), dataset=dataset, status=status)
    finally:
        store.close()


@mcp.tool()
def upsert_field_catalog(region: str, catalog: Any) -> Dict[str, Any]:
    """写入 typed catalog（scan_fields 产物）。catalog 须含 dataset 与 fields。"""
    store = _store()
    try:
        return store.upsert_field_catalog(region, catalog)
    finally:
        store.close()


@mcp.tool()
def get_field_catalog(region: str, dataset: str) -> Dict[str, Any]:
    """读取 typed catalog。"""
    store = _store()
    try:
        cat = store.get_field_catalog(region, dataset)
        return cat or {"error": f"catalog not found: {region}/{dataset}"}
    finally:
        store.close()


@mcp.tool()
def build_field_prefix_clusters(
    region: str,
    dataset: str,
    prefix_depth: int = 1,
    top_n: int = 10,
    samples_per_cluster: int = 5,
    coverage_high: float = 0.85,
) -> Dict[str, Any]:
    """基于 DB 中的字段目录构建 S1 字段前缀聚类摘要并写回 ledger_kv。"""
    store = _store()
    try:
        return store.build_field_prefix_clusters(
            region=region,
            dataset=dataset,
            prefix_depth=prefix_depth,
            top_n=top_n,
            samples_per_cluster=samples_per_cluster,
            coverage_high=coverage_high,
            persist=True,
        )
    finally:
        store.close()


@mcp.tool()
def get_field_prefix_clusters(region: str, dataset: str) -> Dict[str, Any]:
    """读取已持久化的 S1 字段前缀聚类摘要。"""
    store = _store()
    try:
        payload = store.get_field_prefix_clusters(region, dataset)
        return payload or {"error": f"prefix clusters not found: {region}/{dataset}"}
    finally:
        store.close()


@mcp.tool()
def upsert_backtest_rows(
    region: str,
    wave: str,
    rows: Any,
    dataset: Optional[str] = None,
) -> Dict[str, Any]:
    """写入回测行（pipeline/review 产物）。rows 为 metrics 行列表。"""
    store = _store()
    try:
        n = store.upsert_backtest_rows(region, str(wave), rows or [], dataset=dataset)
        return {"n": n, "region": region, "wave": str(wave)}
    finally:
        store.close()


@mcp.tool()
def upsert_gate_result(
    region: str,
    wave: str,
    dataset: str,
    report: Any,
) -> Dict[str, Any]:
    """写入门禁报告（wave_gate / gate.py）。"""
    store = _store()
    try:
        return store.upsert_gate_result(region, str(wave), dataset, report or {})
    finally:
        store.close()


@mcp.tool()
def get_gate_result(region: str, wave: str, dataset: str) -> Dict[str, Any]:
    """读取门禁报告。"""
    store = _store()
    try:
        got = store.get_gate_result(region, str(wave), dataset)
        return got or {"error": f"gate result not found: {region} wave{wave} {dataset}"}
    finally:
        store.close()


@mcp.tool()
def harvest_multisim_results(
    region: str,
    wave: str,
    alphas: Any,
    auto_link: bool = True,
    auto_upsert: bool = True,
) -> Dict[str, Any]:
    """收批 multisim 结果：关联 expressions 并写回 backtest_rows（幂等）。

    接收已从 BRAIN 平台拉取的 alpha 详情列表，负责：
      1. 按 alpha_id / expression 关联 expressions 表中的 expression_id
      2. 转换为 backtest_rows 格式
      3. 写回 backtest_results 表（幂等 upsert）

    网络拉取请使用 tools/harvest_multisim.py 或 wq-brain-http 的
    get_multisimulation_children + get_alpha_details。

    Args:
        region: 区域（如 GBR/USA/KOR）
        wave: 波次编号
        alphas: alpha 详情列表，每项含 alpha_id/sharpe/fitness/turnover 等
        auto_link: 是否自动关联 expressions 表（默认 True）
        auto_upsert: 是否自动写回 backtest_results（默认 True）

    Returns:
        {"linked": n, "upserted": n, "region": ..., "wave": ...}
    """
    store = _store()
    try:
        alpha_list = alphas if isinstance(alphas, list) else []
        linked = 0
        upserted = 0

        if auto_link and alpha_list:
            exprs = store.list_expressions(region, str(wave))
            expr_map = {e.get("alpha_id"): e.get("id") for e in exprs if e.get("alpha_id")}
            code_map = {e.get("expression"): e.get("id") for e in exprs if e.get("expression")}

            for a in alpha_list:
                alpha_id = a.get("alpha_id")
                code = a.get("expression") or a.get("code")
                if alpha_id and alpha_id in expr_map:
                    a["expression_id"] = expr_map[alpha_id]
                    linked += 1
                elif code and code in code_map:
                    a["expression_id"] = code_map[code]
                    linked += 1
                else:
                    a["expression_id"] = None

        if auto_upsert and alpha_list:
            rows = []
            for a in alpha_list:
                row = {
                    "alpha_id": a.get("alpha_id"),
                    "code": a.get("expression") or a.get("code"),
                    "status": "COMPLETE" if not a.get("error") else "ERROR",
                    "sharpe": a.get("sharpe"),
                    "fitness": a.get("fitness"),
                    "turnover": a.get("turnover"),
                    "margin": a.get("margin"),
                    "two_year_sharpe": a.get("two_year_sharpe"),
                    "sub_universe_sharpe": a.get("sub_universe_sharpe"),
                    "failed_checks": a.get("failed_checks"),
                    "universe": a.get("settings", {}).get("universe") if isinstance(a.get("settings"), dict) else None,
                    "delay": a.get("settings", {}).get("delay") if isinstance(a.get("settings"), dict) else None,
                    "neut": a.get("settings", {}).get("neutralization") if isinstance(a.get("settings"), dict) else None,
                }
                rows.append(row)
            upserted = store.upsert_backtest_rows(region, str(wave), rows)

        # --- P2: cascade auto-write wave_results (avoid end-of-campaign backfill) ---
        wave_result_action = None
        if auto_upsert and alpha_list:
            try:
                wave_result_action = _cascade_wave_result(region, str(wave), alpha_list)
            except Exception as e:
                wave_result_action = f"skipped: {e}"

        return {
            "linked": linked,
            "upserted": upserted,
            "region": region,
            "wave": str(wave),
            "wave_result": wave_result_action,
        }
    finally:
        store.close()


@mcp.tool()
def get_salvage_pool(
    region: str,
    boost_dim: Optional[str] = None,
    exclude_dataset: Optional[str] = None,
    min_sharpe: Optional[float] = None,
) -> Dict[str, Any]:
    """查询 salvage_pool 备选因子池（Mode B 组合辅助腿消费接口）。

    当某波出现强主信号但卡某个闸时，从池子找匹配辅助腿：
      - 卡 2Y 闸 → boost_dim="boost_2y"（找 2Y 高的辅助腿）
      - 卡 CW/子宇宙 → boost_dim="boost_cw"（找子宇宙稳健的骨架）
      - 卡 tvr 闸 → boost_dim="boost_tvr"（找低换手辅助腿）
      - 信号弱 → boost_dim="boost_sharpe"（找有信号强度的）

    Args:
        region: 区域（如 KOR）
        boost_dim: 补强维度过滤（boost_2y / boost_cw / boost_tvr / boost_sharpe）
        exclude_dataset: 排除与主信号同数据集的条目（跨数据集正交）
        min_sharpe: 最低 sharpe 过滤

    Returns:
        {"entries": [...], "total": n, "filters": {...}}
    """
    pool = _get_ledger_raw(region, "salvage_pool") or {"entries": []}
    entries = pool.get("entries", [])

    # 过滤
    if boost_dim:
        entries = [e for e in entries if boost_dim in e.get("boost_dims", [])]
    if exclude_dataset:
        entries = [e for e in entries if e.get("dataset") != exclude_dataset]
    if min_sharpe is not None:
        entries = [e for e in entries if isinstance(e.get("sharpe"), (int, float)) and e["sharpe"] >= min_sharpe]

    # 按 sharpe 降序
    entries.sort(key=lambda e: e.get("sharpe") or 0, reverse=True)

    return {
        "entries": entries,
        "total": len(entries),
        "filters": {
            "boost_dim": boost_dim,
            "exclude_dataset": exclude_dataset,
            "min_sharpe": min_sharpe,
        },
        "pool_updated_at": pool.get("updated_at"),
    }


def _cascade_wave_result(region: str, wave: str, alpha_list: list) -> str:
    """收批后自动汇总写 wave_results（幂等）。

    从 alpha 列表派生 candidates 与简要 verdict，只在能解析出 wave 数字时写入。
    不覆盖人工已写的 focus/context/key_findings——仅填 candidates/verdict。
    """
    m = re.search(r"(\d+)", str(wave))
    if not m:
        return "skipped: wave has no numeric part"
    wave_number = int(m.group(1))

    # 汇总候选指标
    cands = []
    passed = 0
    sharpes = []
    for a in alpha_list:
        aid = a.get("alpha_id")
        if not aid:
            continue
        sh = a.get("sharpe")
        fit = a.get("fitness")
        ty = a.get("two_year_sharpe")
        if isinstance(sh, (int, float)):
            sharpes.append(sh)
        ok = (
            isinstance(sh, (int, float)) and sh >= 1.58
            and isinstance(fit, (int, float)) and fit >= 1.0
            and (ty is None or (isinstance(ty, (int, float)) and ty >= 1.58))
        )
        if ok:
            passed += 1
        cands.append({
            "alpha_id": aid,
            "sharpe": sh,
            "fitness": fit,
            "two_year_sharpe": ty,
            "pass_hard_gate": ok,
        })

    total = len(cands)
    best = max(sharpes) if sharpes else None
    verdict = f"{passed}/{total} 过硬闸" + (f", 新高 {best:.2f}" if best else "")

    # 读取现有记录，保留人工写的 focus/context/key_findings
    conn = _conn()
    c = conn.cursor()
    c.execute("SELECT id FROM wave_results WHERE region=? AND wave_number=?", (region, wave_number))
    exists = c.fetchone() is not None
    conn.close()

    cand_json = json.dumps(cands, ensure_ascii=False)
    conn = _conn()
    c = conn.cursor()
    if exists:
        # 只更新 candidates/verdict/updated_at，不动人工字段
        c.execute(
            "UPDATE wave_results SET candidates=?, verdict=?, updated_at=? WHERE region=? AND wave_number=?",
            (cand_json, verdict, _now(), region, wave_number),
        )
        action = "updated"
    else:
        c.execute(
            """INSERT INTO wave_results
               (region, wave_number, focus, context, key_findings, candidates, batches,
                verdict, status, source_file, archived, created_at, updated_at, full_payload)
               VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
            (region, wave_number, None, None, None, cand_json, None, verdict,
             "closed", None, 0, _now(), _now(), None),
        )
        action = "inserted"
    conn.commit()
    conn.close()

    # --- salvage 分层：全 RED 时自动筛选可取因子入 salvage_pool ---
    if passed == 0 and total > 0:
        try:
            _salvage_to_pool(region, wave_number, alpha_list)
        except Exception:
            pass  # salvage 失败不阻塞主流程

    return action


def _salvage_to_pool(region: str, wave_number: int, alpha_list: list) -> None:
    """全 RED 波次自动分层：可取因子写入 salvage_pool ledger key（幂等）。

    入库条件（满足任一）：
      - sharpe >= 0.5（有信号强度）
      - two_year_sharpe >= 1.0（近期表现好）
      - sub_universe_sharpe >= 0.5（子宇宙稳健）
      - turnover <= 0.25（低换手，可作降 tvr 辅助腿）

    每条备选因子标注补强维度（boost_dims），供 Mode B 组合时匹配：
      - boost_2y: two_year_sharpe >= 1.0 → 补 2Y 闸
      - boost_cw: sub_universe_sharpe >= 0.5 → 补 CW/子宇宙闸
      - boost_tvr: turnover <= 0.25 → 降换手
      - boost_sharpe: sharpe >= 0.5 → 补信号强度
      - ortho_dataset: 与主信号不同数据集 → 跨数据集正交
    """
    pool_key = "salvage_pool"
    # 读现有池
    existing = _get_ledger_raw(region, pool_key) or {"entries": [], "updated_at": None}
    entries_map = {e["alpha_id"]: e for e in existing.get("entries", []) if e.get("alpha_id")}

    new_count = 0
    for a in alpha_list:
        aid = a.get("alpha_id")
        if not aid:
            continue
        sh = a.get("sharpe")
        ty = a.get("two_year_sharpe")
        sub = a.get("sub_universe_sharpe")
        tvr = a.get("turnover")
        expr = a.get("expression") or a.get("code", "")

        # 入库条件：sharpe > 0 且满足任一补强维度
        if not (isinstance(sh, (int, float)) and sh > 0):
            continue
        eligible = (
            sh >= 0.5
            or (isinstance(ty, (int, float)) and ty >= 1.0)
            or (isinstance(sub, (int, float)) and sub >= 0.5)
            or (isinstance(tvr, (int, float)) and tvr <= 0.25)
        )
        if not eligible:
            continue

        # 标注补强维度
        boost_dims = []
        if isinstance(ty, (int, float)) and ty >= 1.0:
            boost_dims.append("boost_2y")
        if isinstance(sub, (int, float)) and sub >= 0.5:
            boost_dims.append("boost_cw")
        if isinstance(tvr, (int, float)) and tvr <= 0.25:
            boost_dims.append("boost_tvr")
        if isinstance(sh, (int, float)) and sh >= 0.5:
            boost_dims.append("boost_sharpe")

        # 推断数据集（从表达式前缀）
        dataset = _infer_dataset_from_expr(expr)

        entries_map[aid] = {
            "alpha_id": aid,
            "expression": expr,
            "dataset": dataset,
            "wave": wave_number,
            "sharpe": sh,
            "fitness": a.get("fitness"),
            "two_year_sharpe": ty,
            "sub_universe_sharpe": sub,
            "turnover": tvr,
            "boost_dims": boost_dims,
            "salvaged_at": _now(),
        }
        new_count += 1

    if new_count > 0:
        pool = {
            "entries": list(entries_map.values()),
            "updated_at": _now(),
            "total": len(entries_map),
        }
        _upsert_ledger_raw(region, pool_key, pool)


def _infer_dataset_from_expr(expr: str) -> Optional[str]:
    """从表达式推断数据集前缀（如 anl10_*/fnd86_*/pv106_*）。"""
    if not expr:
        return None
    m = re.search(r"(anl\d+|fnd\d+|pv\d+|risk\d+|shortinterest\d+|intraday_\w+|mmp_\w+|news\d+|model\d+)", expr)
    return m.group(1) if m else None


def _get_ledger_raw(region: str, key: str) -> Optional[dict]:
    """直接读 ledger_kv（不经过 CampaignStore，避免循环依赖）。"""
    conn = _conn()
    c = conn.cursor()
    c.execute("SELECT value FROM ledger_kv WHERE region=? AND key=?", (region, key))
    row = c.fetchone()
    conn.close()
    if row and row[0]:
        try:
            return json.loads(row[0])
        except (json.JSONDecodeError, TypeError):
            return None
    return None


def _upsert_ledger_raw(region: str, key: str, value: dict) -> None:
    """直接写 ledger_kv（不经过 CampaignStore，避免循环依赖）。"""
    conn = _conn()
    c = conn.cursor()
    val_json = json.dumps(value, ensure_ascii=False)
    c.execute(
        "INSERT OR REPLACE INTO ledger_kv (region, key, value, updated_at) VALUES (?,?,?,?)",
        (region, key, val_json, _now()),
    )
    conn.commit()
    conn.close()


@mcp.tool()
def backfill_salvage_pool(
    region: str,
    wave_results_file: str,
    wave_number: Optional[int] = None,
) -> Dict[str, Any]:
    """从 wave_results JSON 文件补录 salvage_pool（通用修复工具）。

    用于修复历史波次未通过 harvest_multisim_alphas 自动触发 salvage 的问题。
    读取 JSON 文件，检查是否全 RED，满足条件则触发 _salvage_to_pool。

    Args:
        region: 区域（如 KOR）
        wave_results_file: wave_results JSON 文件路径（如 tracking/KOR/candidates/wave100_results.json）
        wave_number: 波次编号（可选，从文件内容推断）

    Returns:
        {"status": "success|skipped|error", "reason": ..., "salvaged_count": n}
    """
    import os

    # 读取 JSON 文件
    if not os.path.exists(wave_results_file):
        return {"status": "error", "reason": f"file not found: {wave_results_file}"}

    try:
        with open(wave_results_file, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        return {"status": "error", "reason": f"failed to read file: {e}"}

    # 推断 wave_number
    if wave_number is None:
        wave_str = data.get("wave", "")
        m = re.search(r"(\d+)", str(wave_str))
        if not m:
            return {"status": "error", "reason": f"cannot infer wave number from: {wave_str}"}
        wave_number = int(m.group(1))

    # 提取候选列表
    results = data.get("results", []) or data.get("verdicts", [])
    if not results:
        return {"status": "skipped", "reason": "no results/verdicts in file"}

    # 检查是否全 RED
    red_count = 0
    total_count = 0
    alpha_list = []

    for r in results:
        verdict = r.get("verdict", "").upper()
        # 跳过非 RED  verdict（GREEN/YELLOW/NEAR 等）
        if verdict and verdict != "RED" and not verdict.startswith("RED_"):
            continue

        total_count += 1
        if verdict == "RED" or verdict.startswith("RED_"):
            red_count += 1

        # 构建 alpha_list 格式
        alpha_list.append({
            "alpha_id": r.get("alpha_id") or r.get("alpha"),
            "expression": r.get("expression") or r.get("expr"),
            "sharpe": r.get("sharpe"),
            "fitness": r.get("fitness"),
            "two_year_sharpe": r.get("two_year_sharpe") or r.get("two_year"),
            "sub_universe_sharpe": r.get("sub_universe_sharpe") or r.get("sub"),
            "turnover": r.get("turnover") or r.get("tvr"),
        })

    # 判断是否全 RED
    if red_count == 0 or total_count == 0:
        return {"status": "skipped", "reason": f"not all RED (red={red_count}, total={total_count})"}

    if red_count < total_count:
        return {"status": "skipped", "reason": f"partial RED (red={red_count}, total={total_count}), not triggering salvage"}

    # 触发 salvage
    try:
        _salvage_to_pool(region, wave_number, alpha_list)
        # 读取更新后的 pool 统计
        pool = _get_ledger_raw(region, "salvage_pool") or {"entries": []}
        return {
            "status": "success",
            "reason": f"all RED (red={red_count}), salvaged to pool",
            "wave": wave_number,
            "total_entries_in_pool": len(pool.get("entries", [])),
        }
    except Exception as e:
        return {"status": "error", "reason": f"salvage failed: {e}"}


@mcp.tool()
def backfill_salvage_pool_batch(
    region: str,
    candidates_dir: str,
    wave_pattern: str = "wave*_results.json",
) -> Dict[str, Any]:
    """批量补录 salvage_pool（扫描目录下所有 wave_results 文件）。

    Args:
        region: 区域（如 KOR）
        candidates_dir: candidates 目录路径（如 tracking/KOR/candidates）
        wave_pattern: 文件匹配模式（默认 wave*_results.json）

    Returns:
        {"processed": n, "success": n, "skipped": n, "errors": n, "details": [...]}
    """
    import os
    import glob

    pattern = os.path.join(candidates_dir, wave_pattern)
    files = glob.glob(pattern)

    results = {
        "processed": 0,
        "success": 0,
        "skipped": 0,
        "errors": 0,
        "details": [],
    }

    for f in sorted(files):
        results["processed"] += 1
        r = backfill_salvage_pool(region, f)
        results["details"].append({
            "file": os.path.basename(f),
            "status": r.get("status"),
            "reason": r.get("reason"),
        })
        if r.get("status") == "success":
            results["success"] += 1
        elif r.get("status") == "skipped":
            results["skipped"] += 1
        else:
            results["errors"] += 1

    return results


if __name__ == "__main__":
    # stdio 模式启动（.mcp.json 注册）
    mcp.run()
