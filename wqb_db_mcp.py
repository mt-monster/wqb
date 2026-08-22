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
"""
import json
import sqlite3
from pathlib import Path
from typing import Any, Dict, List, Optional

from mcp.server.fastmcp import FastMCP

# 数据库路径（wqb_db_mcp.py 在 wqb 工作区根目录）
ROOT = Path(__file__).resolve().parent
DB_PATH = ROOT / "data" / "wqb.db"

mcp = FastMCP(
    "wqb-db-mcp",
    "Local wqb.db query service (single-track DB mode)",
)


def _conn():
    """获取数据库连接（row_factory=Row）。"""
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
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
                pass
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

    Args:
        region: 区域过滤（可选）
        status: 状态过滤（open/closed，可选）
        archived: 是否归档（可选）
        limit: 返回数量上限

    Returns:
        wave 结果列表（按 region, wave_number 排序）
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
    sql += " ORDER BY region, wave_number DESC LIMIT ?"
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
    sql += " ORDER BY wave_number DESC LIMIT 1"
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
    return _parse_json_fields(result, ["config"])


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

    Returns:
        跨区教训列表
    """
    conn = _conn()
    c = conn.cursor()
    c.execute("SELECT * FROM cross_region_lessons ORDER BY lesson_id")
    rows = _rows_to_dicts(c.fetchall())
    conn.close()
    return rows


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
    c.execute("SELECT * FROM alphas WHERE alpha_id=?", (alpha_id,))
    row = c.fetchone()
    conn.close()
    if not row:
        return {"error": f"alpha not found: {alpha_id}"}
    result = dict(row)
    return _parse_json_fields(result, ["metrics", "settings", "checks"])


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
    # waves 表找 wave_id
    c.execute(
        "SELECT id FROM waves WHERE region=? AND wave_number=?",
        (region, wave_number),
    )
    wave_row = c.fetchone()
    if not wave_row:
        conn.close()
        return []
    wave_id = wave_row[0]
    # alphas 表找该 wave 的 alpha
    c.execute("SELECT * FROM alphas WHERE wave_id=?", (wave_id,))
    rows = _rows_to_dicts(c.fetchall())
    conn.close()
    return [_parse_json_fields(r, ["metrics", "settings", "checks"]) for r in rows]


@mcp.tool()
def search_alphas_by_sharpe(
    region: Optional[str] = None,
    min_sharpe: float = 1.0,
    limit: int = 20,
) -> List[Dict[str, Any]]:
    """按 sharpe 搜索 alpha（metrics->>'$.sharpe' >= min_sharpe）。

    Args:
        region: 区域过滤（可选）
        min_sharpe: 最小 sharpe
        limit: 返回数量上限

    Returns:
        alpha 列表（按 sharpe 降序）
    """
    conn = _conn()
    c = conn.cursor()
    sql = """
        SELECT a.*, w.region, w.wave_number
        FROM alphas a
        JOIN waves w ON a.wave_id = w.id
        WHERE json_extract(a.metrics, '$.sharpe') >= ?
    """
    params = [min_sharpe]
    if region:
        sql += " AND w.region=?"
        params.append(region)
    sql += " ORDER BY json_extract(a.metrics, '$.sharpe') DESC LIMIT ?"
    params.append(limit)
    c.execute(sql, params)
    rows = _rows_to_dicts(c.fetchall())
    conn.close()
    return [_parse_json_fields(r, ["metrics", "settings", "checks"]) for r in rows]


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
        "SELECT wave_number, focus, status FROM wave_results WHERE region=? ORDER BY wave_number DESC LIMIT 1",
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
            pass
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


if __name__ == "__main__":
    # stdio 模式启动（.mcp.json 注册）
    mcp.run()
