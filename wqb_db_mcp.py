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
  战役产物：upsert_expressions / list_expressions / set_expression_status（批量改状态，
            只传 id/状态过滤，不回传表达式正文）/ upsert_field_catalog / get_field_catalog
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
    """获取数据库连接（row_factory=Row，WAL 模式，批量优化）。"""
    conn = sqlite3.connect(str(DB_PATH), timeout=30.0)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys=ON")
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA synchronous=NORMAL")
    conn.execute("PRAGMA cache_size=-64000")  # 64MB page cache
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


@mcp.tool()
def get_mining_yield(
    region: Optional[str] = None,
    by_dataset: bool = False,
    sharpe_min: float = 1.58,
    fitness_min: float = 1.0,
    strict: bool = True,
) -> Dict[str, Any]:
    """实测挖掘产出率：生成→回测转化率 + 回测→达标率（2026-09-06 新增）。

    为什么需要它（2026-09-06 审计结论）：区域间达标率相差 25 倍
    （IND 35.7% vs USA 1.4%），而槽位分配完全没吃这个反馈 —— USA 的生成量
    是 IND 的 3 倍。选区靠 S0 评分与人工判断，"这个区历史上到底出不出货"
    这个最硬的先验此前在库里躺着没人查。

    口径：
      - expressions：该 region（可选 dataset）下的表达式总数
      - backtested：backtest_results 行数
      - conversion：backtested / expressions —— 低说明 S2→S3 断链（生成远超回测吞吐）
      - passed：|sharpe| >= sharpe_min 且 fitness >= fitness_min
      - yield_rate：passed / backtested —— 低说明这个区/集本身不出货

    两个比率含义不同，不要混：conversion 是**流水线**问题，yield_rate 是
    **标的**问题。conversion 低 → 修管道；yield_rate 低 → 换区/换集。

    2026-09-19 严格口径（strict，默认开）：旧 passed 只看 sharpe/fitness，IND 显示 34%
    "产出率"而实际可提交为 0（robust/2Y/CW 全在 ra_failed_checks 里，prod 墙在 alphas 表），
    选区先验被系统性高估。strict 下：
      - ra_clean：sharpe/fitness 达标 **且** ra_failed_checks 为空（平台 RA 硬闸全过）
      - prod_clean：ra_clean 且 alphas.prod_correlation 已测且 < prod_max（0.7）
      - prod_blocked：ra_clean 且 prod_correlation 已测且 >= prod_max
      - yield_rate = ra_clean / backtested（选区/选集用这个）；yield_rate_loose 保留旧口径对照
      - prod_wall_ratio = prod_blocked / (prod_clean + prod_blocked)，已测 prod 的撞墙占比
      - 注意：ra_failed_checks 为 NULL 的旧行按"无失败"计（2026-09 前入库的行无该字段）
    strict=False 回到旧口径（yield_rate = passed / backtested）。

    Args:
        region: 限定区域；省略则返回全部区域
        by_dataset: True 时按 region×dataset 拆分（用于选集）
        sharpe_min / fitness_min: 达标口径，默认平台 RA 硬阈值
        strict: 见上

    Returns:
        {"rows": [...], "totals": {...}, "criteria": {...}}
        rows 按 yield_rate 降序，无回测记录的排在最后。
    """
    conn = _conn()
    c = conn.cursor()

    group_cols = "region, dataset" if by_dataset else "region"
    params: List[Any] = []
    where = "region IS NOT NULL"
    if region:
        where += " AND region=?"
        params.append(region)

    c.execute(
        f"SELECT {group_cols}, COUNT(*) n FROM expressions "
        f"WHERE {where} GROUP BY {group_cols}",
        params,
    )
    expr_counts = {tuple(r)[:-1]: r[-1] for r in c.fetchall()}

    prod_max = 0.7
    # ra_failed_checks 为空 = NULL / '' / '[]'；prod 取 alphas 表最新一行（LEFT JOIN，可能未测）
    ra_clean_sql = ("(ABS(COALESCE(b.sharpe,0))>=? AND COALESCE(b.fitness,0)>=? "
                    "AND COALESCE(TRIM(b.ra_failed_checks),'') IN ('', '[]'))")
    c.execute(
        f"SELECT {', '.join('b.' + g for g in group_cols.split(', '))}, COUNT(*) n, "
        f"SUM(CASE WHEN ABS(COALESCE(b.sharpe,0))>=? AND COALESCE(b.fitness,0)>=? "
        f"THEN 1 ELSE 0 END) passed, "
        f"SUM(CASE WHEN {ra_clean_sql} THEN 1 ELSE 0 END) ra_clean, "
        f"SUM(CASE WHEN {ra_clean_sql} AND a.prod_correlation IS NOT NULL "
        f"AND a.prod_correlation < ? THEN 1 ELSE 0 END) prod_clean, "
        f"SUM(CASE WHEN {ra_clean_sql} AND a.prod_correlation IS NOT NULL "
        f"AND a.prod_correlation >= ? THEN 1 ELSE 0 END) prod_blocked "
        f"FROM backtest_results b LEFT JOIN alphas a ON a.alpha_id=b.alpha_id "
        f"WHERE {where.replace('region', 'b.region')} "
        f"GROUP BY {', '.join('b.' + g for g in group_cols.split(', '))}",
        [sharpe_min, fitness_min,
         sharpe_min, fitness_min,
         sharpe_min, fitness_min, prod_max,
         sharpe_min, fitness_min, prod_max] + params,
    )
    bt_counts = {tuple(r)[:-5]: (r[-5], r[-4] or 0, r[-3] or 0, r[-2] or 0, r[-1] or 0)
                 for r in c.fetchall()}
    conn.close()

    rows = []
    # 2026-09-09 修复：by_dataset=True 时 key 可能含 dataset=None（expressions 表
    # 有 dataset 为 NULL 的历史行），sorted() 对 (region, None) 与 (region, 'xxx')
    # 混合排序报 TypeError: '<' not supported between NoneType 和 str。
    # 排序键统一转 str（None→''），仅影响遍历顺序，不影响分组正确性。
    def _sort_key(k):
        return tuple("" if part is None else str(part) for part in k)
    for key in sorted(set(expr_counts) | set(bt_counts), key=_sort_key):
        n_expr = expr_counts.get(key, 0)
        n_bt, n_pass, n_ra, n_pc, n_pb = bt_counts.get(key, (0, 0, 0, 0, 0))
        row: Dict[str, Any] = {"region": key[0]}
        if by_dataset:
            row["dataset"] = key[1] if len(key) > 1 else None
        n_yield = n_ra if strict else n_pass
        row.update({
            "expressions": n_expr,
            "backtested": n_bt,
            "conversion": round(n_bt / n_expr, 4) if n_expr else None,
            "passed": n_pass,
            "ra_clean": n_ra,
            "prod_clean": n_pc,
            "prod_blocked": n_pb,
            "yield_rate": round(n_yield / n_bt, 4) if n_bt else None,
            "yield_rate_loose": round(n_pass / n_bt, 4) if n_bt else None,
            # 已测 prod 的 ra_clean 里撞墙占比（None=没有一条测过 prod）
            "prod_wall_ratio": (round(n_pb / (n_pc + n_pb), 4) if (n_pc + n_pb) else None),
        })
        rows.append(row)

    rows.sort(key=lambda r: (r["yield_rate"] is None, -(r["yield_rate"] or 0)))

    tot_expr = sum(r["expressions"] for r in rows)
    tot_bt = sum(r["backtested"] for r in rows)
    tot_pass = sum(r["passed"] for r in rows)
    tot_ra = sum(r["ra_clean"] for r in rows)
    tot_pc = sum(r["prod_clean"] for r in rows)
    tot_pb = sum(r["prod_blocked"] for r in rows)
    tot_yield = tot_ra if strict else tot_pass
    return {
        "rows": rows,
        "totals": {
            "expressions": tot_expr,
            "backtested": tot_bt,
            "conversion": round(tot_bt / tot_expr, 4) if tot_expr else None,
            "passed": tot_pass,
            "ra_clean": tot_ra,
            "prod_clean": tot_pc,
            "prod_blocked": tot_pb,
            "yield_rate": round(tot_yield / tot_bt, 4) if tot_bt else None,
            "yield_rate_loose": round(tot_pass / tot_bt, 4) if tot_bt else None,
        },
        "criteria": {"sharpe_min": sharpe_min, "fitness_min": fitness_min,
                     "strict": strict, "prod_max": prod_max,
                     "yield_rate_def": ("ra_clean/backtested（sharpe/fitness 达标且 ra_failed_checks 为空）"
                                        if strict else "passed/backtested（仅 sharpe/fitness）")},
    }


# ---------------- 区域轮转（饱和检测 + 跨区决策） ----------------

_REGION_PROFILE_DIR = ROOT / "Claude" / "skills" / "wq-brain-ra-pipeline" / "references" / "regions"


def _read_entry_verdict(region: str) -> Optional[str]:
    """读区域 profile 的 entry_verdict（active/probe-only/frozen）；缺失返回 None。"""
    path = _REGION_PROFILE_DIR / f"{region}.md"
    if not path.exists():
        return None
    try:
        mm = re.search(r"^entry_verdict:\s*(\S+)",
                       path.read_text(encoding="utf-8", errors="replace"), re.M)
        return mm.group(1) if mm else None
    except Exception:
        return None


@mcp.tool()
def region_rotation(current_region: str, target: Optional[int] = None,
                    write_ledger: bool = False) -> Dict[str, Any]:
    """区域结构性饱和检测 + 跨区轮转决策（单区证实饱和→推荐下一区并承接目标）。

    把挖掘 SOP 的止损规则（"白名单被 dead_end 全覆盖→停止" / "连续 3 波全 FAIL→转区"）
    自动化为确定性、DB 驱动的轮转决策。判定/打分逻辑的**单一事实源**在
    ``src/wqb/region_rotation.py``，与 ``tools/region_status.py --rotate`` 同源。
    零平台请求、零配额。

    饱和判据（不依赖 prod 测量量；NULL prod ≠ 可行）：战役穷尽 / 深挖波次 /
    判死厚度 / prod 墙占比（仅 measured 充足时）/ 产出率崩塌；仍有未提交可行存量则豁免降级为 WATCH。

    Args:
        current_region: 当前挖掘区（如 EUR）。
        target: 待承接的过闸目标数（如 20），写入 carry_target。
        write_ledger: True 时把决策幂等写入 ledger_kv(region=current, key=region_rotation)。

    Returns:
        {"should_rotate", "from_region", "to_region", "all_saturated", "carry_target",
         "current_saturation", "reason", "next_action", "ranked": [...]}
    """
    from wqb.region_rotation import (gather_all_regions, gather_region_metrics,
                                     recommend_rotation)
    conn = _conn()
    try:
        names = [r[0] for r in conn.execute("SELECT name FROM regions")]
        verdicts = {r: _read_entry_verdict(r) for r in names}
        allm = gather_all_regions(conn, verdicts=verdicts)
        cur = str(current_region).upper()
        if cur not in allm:  # 当前区可能无活动痕迹，仍补采以给出饱和判定
            allm[cur] = gather_region_metrics(conn, cur, entry_verdict=verdicts.get(cur))
        rec = recommend_rotation(cur, allm, target=target)
        if write_ledger and rec.get("should_rotate"):
            payload = {k: rec.get(k) for k in
                       ("from_region", "to_region", "should_rotate", "all_saturated",
                        "carry_target", "reason", "next_action")}
            payload["current_verdict"] = (rec.get("current_saturation") or {}).get("verdict")
            payload["ranked"] = [{"region": r["region"], "score": r["score"],
                                  "verdict": r["verdict"]}
                                 for r in (rec.get("ranked") or [])[:8]]
            upsert_ledger_key(cur, "region_rotation", payload)
            rec["ledger_written"] = True
        return rec
    finally:
        conn.close()


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


_WAVE_VERDICT_OK = ("PASS", "FAIL", "PARTIAL")


def _normalize_wave_verdict(verdict):
    """自由文本 verdict → 枚举（与 tools/migrate_wave_verdict_enum.classify 同规则）。返回 (枚举|None, 规则)。"""
    v = str(verdict or "").strip()
    if not v:
        return None, "空"
    up = v.upper()
    if up in _WAVE_VERDICT_OK:
        return up, "枚举"
    if up.startswith("GREEN") or up.startswith("PASS"):
        return "PASS", "前缀"
    if up.startswith(("YELLOW", "PARTIAL", "CLOSED_ACCEPTED")):
        return "PARTIAL", "前缀"
    if up.startswith(("RED", "FAIL", "CLOSED_DEAD_END", "GATE_BLOCKED", "PROBE_WEAK")):
        return "FAIL", "前缀"
    m = re.search(r"(\d+)\s*/\s*(\d+)\s*过硬闸", v)
    if m:
        return ("PASS" if int(m.group(1)) > 0 else "FAIL"), "过硬闸计数"
    if "全灭" in v or "GATE_FAIL" in up:
        return "FAIL", "关键词"
    return None, "无匹配"


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
    # 2026-09-15 ⑦：verdict 强制三态枚举。此前本入口不校验，Agent 写入了 ~40 行
    # "PASS_READY_x2：…" / "CLOSED_DEAD_END_DATASET：…" 式自由文本，`WHERE verdict='FAIL'`
    # 类机械判定（连续 FAIL 停止规则等）对它们全部失明。前缀可辨的归一到枚举、原文
    # 搬进 key_findings 首条；无法辨认的直接拒绝（与 _lib/wave_results.upsert 同契约）。
    if verdict is not None:
        norm, note = _normalize_wave_verdict(verdict)
        if norm is None:
            return {"error": f"verdict 必须是 PASS/FAIL/PARTIAL（或带该前缀），收到 {verdict!r}；"
                             f"描述性结论请放 key_findings", "region": region, "wave_number": wave_number}
        if norm != str(verdict).strip():
            kf_list = list(key_findings) if isinstance(key_findings, list) else (
                [key_findings] if key_findings else [])
            kf_list.insert(0, f"原 verdict（写入时归一）: {str(verdict).strip()}")
            key_findings = kf_list
        verdict = norm
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
    source: Optional[str] = None,
) -> Dict[str, Any]:
    """写入本波表达式（幂等，按 region+wave+expression）。

    expressions 为字符串列表或 {expression/expr/code, status, settings, source} 对象列表。

    source（2026-09-17 新增）：候选来源标签，与 status（流水线状态）正交。
    实际生成链路 = GEM runner → 本工具落库，此前**本工具没有 source 形参**，
    导致全库 source 几乎全 NULL（GEM 产出不可辨识、无法做模式 A/B）。
    建议取值：`gem_phased` / `gem_skeleton` / `gem_single`（对应 --pipeline-mode）、
    `manual` / `probe` / `diversity`。条目级 `source` 优先于本参数。
    """
    store = _store()
    try:
        return store.upsert_expressions(region, str(wave), expressions or [],
                                        dataset=dataset, status=status,
                                        source=source)
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
def set_expression_status(
    region: str,
    wave: str,
    to_status: str,
    ids: Optional[List[int]] = None,
    from_status: Optional[str] = None,
    reason: Optional[str] = None,
) -> Dict[str, Any]:
    """批量改本波表达式状态（单条 UPDATE；只传 id/状态过滤，不回传表达式正文）。

    2026-09-12 GBR wave57 实测：用 upsert_expressions 改 43 条状态要原样回传全部表达式，
    服务端 3 ms、MCP 侧却吐 3-4k token——成本在载荷不在库。改状态一律用本工具。

    Args:
        region: 区域
        wave: 波次（与 expressions.wave 同口径，字符串）
        to_status: 目标状态（pending/gem/enhanced/selected/gated/superseded/dropped …）
        ids: 表达式 id 列表（list_expressions 返回的 id）；与 from_status 至少给一个，同给取交集
        from_status: 只改当前处于该状态的行
        reason: 变更原因，连同 from/to/at 合并进 settings_json.status_change（不清空其他设置键）

    规则：已回测行（alpha_id 非空）只有 to_status ∈ {superseded, dropped} 才会被改，
    否则自动跳过并以 n_protected 回报；无过滤（ids/from_status 都缺）直接拒绝。

    Returns:
        {"n_updated", "n_protected", "n_requested", "region", "wave", "from_status", "to_status"}
        或 {"error": ...}
    """
    store = _store()
    try:
        return store.set_expression_status(
            region, str(wave), to_status, ids=ids, from_status=from_status, reason=reason,
        )
    except ValueError as e:
        return {"error": str(e)}
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
def persist_correlation(
    alpha_id: str,
    prod: Optional[float] = None,
    self_: Optional[float] = None,
    source: str = "triage_local",
    overwrite: bool = False,
) -> Dict[str, Any]:
    """把相关性检查结果落库到 alphas 表（2026-09-18，设计文档 §2.4）。

    动机：check_correlation 的返回值此前只进内存 / triage checkpoint，
    复盘时必须重打平台 API（占单并发队列）。本工具提供「检查即落库」。

    Args:
        alpha_id: 目标 alpha（必须已在 alphas 表，否则返回 skipped=not_found）
        prod: 生产池相关性（[0,1]，越界或 None 忽略）
        self_: 自相关（[0,1]，越界或 None 忽略）
        source: 来源标记 platform_sync（平台权威）| manual | triage_local（本地抽测）
        overwrite: False（默认）只填 NULL 列保留平台权威值；True 覆盖

    Returns:
        成功 {"alpha_id", "prod_correlation", "self_correlation", "source", "checked_at"}
        跳过 {"skipped": "not_found"|"already_set"|"no_valid_value"|"no_alpha_id"}
    """
    store = _store()
    try:
        return store.persist_correlation(
            alpha_id=alpha_id,
            prod=prod,
            self_=self_,
            source=source,
            overwrite=overwrite,
        )
    finally:
        store.close()


@mcp.tool()
def get_alpha_corr_metrics(
    region: Optional[str] = None,
    max_prod: Optional[float] = None,
    max_self: Optional[float] = None,
    source: Optional[str] = None,
    limit: int = 50,
) -> List[Dict[str, Any]]:
    """本地查询相关性指标（免打平台）。用于提交前候选筛选。

    Args:
        region: 区域过滤（可选）
        max_prod: prod_correlation 上界（如 0.7）
        max_self: self_correlation 上界（如 0.7）
        source: prod_corr_source 过滤（platform_sync / manual / triage_local）
        limit: 返回条数上限（默认 50）

    Returns:
        按 prod_correlation 升序的 alpha 指标列表（本地库直接读，零配额）
    """
    conn = _conn()
    try:
        sql = (
            "SELECT a.alpha_id, r.name AS region, a.sharpe, a.fitness, a.turnover, "
            "a.prod_correlation, a.self_correlation, a.prod_corr_source, "
            "a.corr_checked_at, a.status, a.date_submitted "
            "FROM alphas a LEFT JOIN regions r ON a.region_id = r.id WHERE 1=1"
        )
        params: List[Any] = []
        if region:
            sql += " AND r.name = ?"
            params.append(region)
        if max_prod is not None:
            sql += " AND a.prod_correlation IS NOT NULL AND a.prod_correlation <= ?"
            params.append(float(max_prod))
        if max_self is not None:
            sql += " AND a.self_correlation IS NOT NULL AND a.self_correlation <= ?"
            params.append(float(max_self))
        if source:
            sql += " AND a.prod_corr_source = ?"
            params.append(source)
        sql += " ORDER BY (a.prod_correlation IS NULL), a.prod_correlation ASC LIMIT ?"
        params.append(int(limit))
        cur = conn.execute(sql, params)
        cols = [d[0] for d in cur.description]
        return [dict(zip(cols, row)) for row in cur.fetchall()]
    finally:
        conn.close()


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
def _flatten_platform_alpha(a: Dict[str, Any]) -> Dict[str, Any]:
    """把平台 harvest_multisim_alphas / get_alpha_details 的嵌套 alpha 拍平成扁平 dict（幂等：已扁平的原样返回）。"""
    out = dict(a)
    out.setdefault("alpha_id", a.get("alpha_id") or a.get("id"))
    out.setdefault("expression", a.get("expression") or a.get("code"))
    m = a.get("metrics") if isinstance(a.get("metrics"), dict) else {}
    # 平台原始 alpha（GET /alphas/{id}）把指标放在 "is" 块（sharpe/fitness/turnover/checks…）；
    # 2Y/sub/robust 等在 is.checks 里按 name 给 value —— 统一并进 m
    isb = a.get("is") if isinstance(a.get("is"), dict) else {}
    if isb and not m:
        m = {k: isb.get(k) for k in ("sharpe", "fitness", "turnover", "margin", "returns", "drawdown",
                                     "longCount", "shortCount", "pnl", "bookSize") if isb.get(k) is not None}
        _name_map = {"LOW_2Y_SHARPE": "two_year_sharpe", "LOW_SUB_UNIVERSE_SHARPE": "sub_universe_sharpe",
                     "LOW_ROBUST_UNIVERSE_SHARPE": "robust_universe_sharpe",
                     "LOW_INVESTABILITY_CONSTRAINED_SHARPE": "investability_sharpe",
                     "IS_LADDER_SHARPE": "is_ladder_sharpe", "PROD_CORRELATION": "prod_correlation",
                     "SELF_CORRELATION": "self_correlation"}
        fails = []
        for c in isb.get("checks") or []:
            if not isinstance(c, dict):
                continue
            nm, val, res = c.get("name"), c.get("value"), c.get("result")
            if nm in _name_map and val is not None and m.get(_name_map[nm]) is None:
                m[_name_map[nm]] = val
            if res == "FAIL":
                fails.append(nm)
        if a.get("checks") is None:
            out["checks"] = [c for c in (isb.get("checks") or []) if isinstance(c, dict)]
        if out.get("ra_failed_checks") is None:
            out["ra_failed_checks"] = fails
        if isb.get("prodCorrelation") is not None:
            out.setdefault("prod_correlation", isb.get("prodCorrelation"))
        if isb.get("selfCorrelation") is not None:
            out.setdefault("self_correlation", isb.get("selfCorrelation"))
    if out.get("expression") is None and isinstance(a.get("regular"), dict):
        out["expression"] = a["regular"].get("code")
    stg = a.get("settings") if isinstance(a.get("settings"), dict) else {}
    if stg:
        out.setdefault("neut", stg.get("neutralization")); out.setdefault("decay", stg.get("decay"))
        out.setdefault("universe", stg.get("universe")); out.setdefault("delay", stg.get("delay"))
    for k in ("sharpe", "fitness", "turnover", "margin", "returns", "drawdown", "two_year_sharpe",
              "sub_universe_sharpe", "robust_universe_sharpe", "investability_sharpe",
              "risk_neutralized_sharpe", "long_count", "short_count", "pnl", "book_size"):
        if out.get(k) is None and m.get(k) is not None:
            out[k] = m.get(k)
    for src, dst in (("longCount", "long_count"), ("shortCount", "short_count"),
                     ("prodCorrelation", "prod_correlation"), ("selfCorrelation", "self_correlation")):
        if out.get(dst) is None and m.get(src) is not None:
            out[dst] = m.get(src)
    ra = a.get("ra") if isinstance(a.get("ra"), dict) else {}
    if out.get("ra_failed_checks") is None and ra.get("ra_failed_checks") is not None:
        out["ra_failed_checks"] = ra.get("ra_failed_checks")
    if isinstance(out.get("ra_failed_checks"), str) and out["ra_failed_checks"].startswith("["):
        try:
            out["ra_failed_checks"] = json.loads(out["ra_failed_checks"])
        except Exception:
            pass
    checks = a.get("checks")
    if isinstance(checks, dict):  # {"fail":[{name,value,limit}], "pass":[...], ...} → 扁平列表
        flat = []
        for k in ("fail", "warning", "pass", "pending"):
            for c in checks.get(k) or []:
                if isinstance(c, dict):
                    flat.append({**c, "result": k.upper()})
                elif isinstance(c, str):
                    flat.append({"name": c, "result": k.upper()})
        out["checks"] = flat
    if out.get("failed_checks") is None and isinstance(out.get("checks"), list):
        out["failed_checks"] = [c.get("name") for c in out["checks"] if c.get("result") == "FAIL"]
    return out


def harvest_multisim_results(
    region: str,
    wave: str,
    alphas: Any,
    auto_link: bool = True,
    auto_upsert: bool = True,
    dataset: Optional[str] = None,
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
        # 2026-09-19：接受 wq-brain-http harvest_multisim_alphas 的原样输出（嵌套 metrics/ra/settings/checks），
        # 拍平为本函数期望的扁平键；此前嵌套结构进来 ra_failed_checks/dataset/2Y/robust 全部静默丢失。
        alpha_list = [_flatten_platform_alpha(a) for a in alpha_list if isinstance(a, dict)]
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
                settings = a.get("settings") if isinstance(a.get("settings"), dict) else {}
                # 2026-09-18 修复（设计文档 §2.2 改动#3 / 断链 B）：
                # 原 row 构造无 prod/self 相关性、is_ladder、risk_neut、cluster_test，
                # 走 MCP 收批时这些指标静默丢失（与 tools/harvest_multisim.py 的
                # _to_backtest_rows 口径不一致）。现对齐两处。
                checks = a.get("checks") or []
                check_map = {}
                if isinstance(checks, list):
                    for c in checks:
                        if isinstance(c, dict) and c.get("name"):
                            check_map[c["name"]] = c.get("value")

                def _pick(*keys, default=None):
                    for k in keys:
                        if a.get(k) is not None:
                            return a.get(k)
                    return default

                prod_corr = _pick("prod_correlation", "prod_corr")
                if prod_corr is None:
                    prod_corr = check_map.get("PROD_CORRELATION")
                self_corr = _pick("self_correlation", "self_corr")
                if self_corr is None:
                    self_corr = check_map.get("SELF_CORRELATION")

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
                    "risk_neutralized_sharpe": a.get("risk_neutralized_sharpe"),
                    "returns": a.get("returns"),
                    "drawdown": a.get("drawdown"),
                    "long_count": a.get("long_count"),
                    "short_count": a.get("short_count"),
                    "concentrated_weight": _pick("concentrated_weight")
                        or check_map.get("CONCENTRATED_WEIGHT"),
                    "cluster_test": check_map.get("CLUSTER_TEST"),
                    "prod_correlation": prod_corr,
                    "self_correlation": self_corr,
                    "is_ladder_sharpe": _pick("is_ladder_sharpe")
                        or check_map.get("IS_LADDER_SHARPE"),
                    "failed_checks": a.get("failed_checks"),
                    "ra_failed_checks": a.get("ra_failed_checks"),
                    "robust_sharpe": a.get("robust_universe_sharpe"),
                    "investability_sharpe": a.get("investability_sharpe"),
                    "universe": settings.get("universe"),
                    "delay": settings.get("delay"),
                    "neut": settings.get("neutralization"),
                }
                rows.append(row)
            ds = dataset
            if not ds:  # 缺省取该波表达式的 dataset（2026-09-19：此前恒 NULL）
                try:
                    _ds = {e.get("dataset") for e in store.list_expressions(region, str(wave)) if e.get("dataset")}
                    ds = next(iter(_ds)) if len(_ds) == 1 else None
                except Exception:
                    ds = None
            upserted = store.upsert_backtest_rows(region, str(wave), rows, dataset=ds)

            # 相关性来源标记：harvest 链路拿到的是平台返回值，标 platform_sync
            for row in rows:
                if row.get("alpha_id") and (
                    row.get("prod_correlation") is not None
                    or row.get("self_correlation") is not None
                ):
                    try:
                        store.persist_correlation(
                            alpha_id=row["alpha_id"],
                            prod=row.get("prod_correlation"),
                            self_=row.get("self_correlation"),
                            source="platform_sync",
                        )
                    except Exception:
                        pass  # 相关性落库失败不阻断主写入

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

    # --- salvage 分层：每波收取 FAIL 达辅料线者入 salvage_pool ---
    # 2026-09-13 放宽：原实现仅“全 RED 波”（passed==0）触发，而“>10 种结构判死”
    # 场景横跨多波，部分过闸波里的失败候选会散落未收。现每波均收取（幂等 by
    # alpha_id、零配额成本）。辅料线独立于 mode_b_qualification（收集宽、动用严）。
    if total > 0:
        try:
            _salvage_to_pool(region, wave_number, alpha_list)
        except Exception:
            pass  # salvage 失败不阻塞主流程

    return action


def _salvage_to_pool(region: str, wave_number: int, alpha_list: list) -> None:
    """波次收敛自动分层：FAIL 候选达【辅料线】者写入 salvage_pool ledger key（幂等）。

    收集宽 / 动用严（2026-09-13 定案）：
      - 辅料线（本函数判据）= 收集线，独立于各区 mode_b_qualification
        （1.2~1.5/0.8 那套只管“动用救援”的入口资格，不管“入池留档”）；
      - 入池零配额成本（不新跑回测，仅 ledger 留档），达线即收；
      - 消费与动用纪律见 wq-brain-alpha-optimization-v1「组合腿救援」
        （路线 A：禁加权混合，仅结构交互 / SuperAlpha combo）。

    入库条件（辅料线 v1，满足任一）：
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


@mcp.tool()
def seal_dead_end(
    region: str,
    entry_id: str,
    family: Optional[str] = None,
    reason: Optional[str] = None,
    wave_numbers: Optional[List[int]] = None,
    dead_at: Optional[str] = None,
) -> Dict[str, Any]:
    """判死封存：先沉降残值、再封存 dead_end（2026-09-13 新增，S6 判死标准动作）。

    收集宽、动用严：把该 idea 涉及波次的失败候选达【辅料线】者沉降入
    salvage_pool（复用 _salvage_to_pool，幂等、零配额成本），并把残值
    alpha_id 列表回填 dead_end 条目 payload["salvage"]（schema 预留字段，
    此前恒 null）。救援动用入口仍以各区 mode_b_qualification 资格线为准——
    本工具只做收集，不改动用侧。

    Args:
        region: 区域
        entry_id: dead_end 条目 id（registry_empirical，如 KOR-WAVE99-XXX-DEAD）
        family: 信号族名（可选，payload 无则补）
        reason: 判死原因（可选，并入 payload）
        wave_numbers: 该 idea 涉及的波次号列表（沉降扫描范围）；缺省则不扫描，
            仅以空 salvage 封存
        dead_at: 判死日期（缺省今天）

    Returns:
        {"entry_id", "status", "action", "waves_scanned", "candidates_scanned",
         "salvaged_count", "salvage_ids", "total_in_pool"}
    """
    waves_scanned: List[int] = []
    candidates_scanned = 0
    collected_ids: set = set()

    for w in wave_numbers or []:
        try:
            wave_number = int(w)
        except (TypeError, ValueError):
            continue
        conn = _conn()
        c = conn.cursor()
        c.execute(
            "SELECT candidates FROM wave_results WHERE region=? AND wave_number=?",
            (region, wave_number),
        )
        row = c.fetchone()
        conn.close()
        if not (row and row[0]):
            continue
        try:
            cands = [d for d in json.loads(row[0]) if isinstance(d, dict) and d.get("alpha_id")]
        except (json.JSONDecodeError, TypeError):
            continue
        if not cands:
            continue
        # 沉降（辅料线判据单点定义在 _salvage_to_pool，幂等 by alpha_id）
        _salvage_to_pool(region, wave_number, cands)
        waves_scanned.append(wave_number)
        candidates_scanned += len(cands)
        collected_ids.update(d["alpha_id"] for d in cands if d.get("alpha_id"))

    # 读回池：只回填真正入池的残值 alpha_id（达辅料线者）
    pool = _get_ledger_raw(region, "salvage_pool") or {"entries": []}
    pool_ids = {e.get("alpha_id") for e in pool.get("entries", []) if e.get("alpha_id")}
    salvage_ids = sorted(collected_ids & pool_ids)

    # 读现有 dead_end payload 并回填 salvage
    payload: Dict[str, Any] = {}
    conn = _conn()
    c = conn.cursor()
    c.execute(
        "SELECT payload, family FROM registry_empirical WHERE region=? AND layer=? AND entry_id=?",
        (region, "dead_end", entry_id),
    )
    row = c.fetchone()
    conn.close()
    if row and row[0]:
        try:
            parsed = json.loads(row[0])
            if isinstance(parsed, dict):
                payload = parsed
        except (json.JSONDecodeError, TypeError):
            pass
    if family:
        payload.setdefault("family", family)
    if reason:
        payload["reason"] = reason
    payload.setdefault("source", "registry_dead_end")
    payload["salvage"] = {
        "alpha_ids": salvage_ids,
        "count": len(salvage_ids),
        "source_waves": waves_scanned,
        "sealed_at": _now(),
        "note": ("seal_dead_end 沉降：供 Mode B 组合腿救援消费（get_salvage_pool）；"
                 "动用仍守 mode_b_qualification 资格线"),
    }

    res = upsert_registry_empirical(
        region=region,
        layer="dead_end",
        entry_id=entry_id,
        payload=payload,
        family=(family or payload.get("family")),
        dead_at=(dead_at or _now()),
    )
    return {
        "entry_id": entry_id,
        "status": "success",
        "action": res.get("action"),
        "waves_scanned": waves_scanned,
        "candidates_scanned": candidates_scanned,
        "salvaged_count": len(salvage_ids),
        "salvage_ids": salvage_ids,
        "total_in_pool": len(pool.get("entries", [])),
    }


# ---------------- 质量效能增益评估：已于 2026-09-17 整体下线 ----------------
# 移除 6 个工具：record_step_metrics / get_step_metrics / compute_wave_summary /
# compute_campaign_summary / get_step_gain_report / workflow_step_metrics。
# 原因：唯一自动采集入口 collect_from_checkpoint() 是 TODO 空壳（无数据源）；
# 质量指标可从既有表推导（写新表=双真相源）；增益指标是反事实估算无客观来源；
# 五张表恒 0 行。替代方案 = `tools/step_funnel.py`（只读步级漏斗）。
# 归档与复活步骤见 `attic/step_metrics_20260917/README.md`。

@mcp.tool()
def workflow_inventory_scan(
    region: str,
    target: int = 20,
    regions: Optional[List[str]] = None,
) -> Dict[str, Any]:
    """自动化库存盘点 workflow 节点（inventory_scan 节点快捷方式）.

    Args:
        region: 区域代码
        target: 目标候选数（默认 20）
        regions: 要盘点的区域列表（默认 all）

    Returns:
        执行结果字典
    """
    from wqb.workflow import execute
    
    result = execute("inventory_scan", {
        "region": region,
        "target": target,
        "regions": regions,
    })
    return result.to_dict()


@mcp.tool()
def workflow_field_understanding(
    region: str,
    dataset: str,
    delay: int = 1,
    auto_classify: bool = True,
    identify_high_value: bool = True,
) -> Dict[str, Any]:
    """自动化字段理解 workflow 节点（field_understanding 节点快捷方式）.

    Args:
        region: 区域代码
        dataset: 数据集 ID
        delay: 延迟（默认 1）
        auto_classify: 是否自动分类字段（默认 True）
        identify_high_value: 是否识别高价值字段（默认 True）

    Returns:
        执行结果字典
    """
    from wqb.workflow import execute
    
    result = execute("field_understanding", {
        "region": region,
        "dataset": dataset,
        "delay": delay,
        "auto_classify": auto_classify,
        "identify_high_value": identify_high_value,
    })
    return result.to_dict()


@mcp.tool()
def workflow_gem_wave(
    region: str,
    dataset_id: str,
    delay: int,
    universe: str,
    data_type: Optional[str] = None,
    wave: Optional[str] = None,
    auto_dedup: bool = True,
    auto_bucket: bool = True,
    auto_skeleton: bool = True,
    auto_select: bool = True,
) -> Dict[str, Any]:
    """合并选波到 GEM 生成 workflow 节点（gem_wave 节点快捷方式）.

    Args:
        region: 区域代码
        dataset_id: 数据集 ID
        delay: 延迟
        universe: Universe
        data_type: 数据类型（可选）
        wave: 波次号（可选）
        auto_dedup: 是否自动去重（默认 True）
        auto_bucket: 是否自动分桶（默认 True）
        auto_skeleton: 是否自动骨架配给（默认 True）
        auto_select: 是否自动选波（默认 True）

    Returns:
        执行结果字典
    """
    from wqb.workflow import execute
    
    result = execute("gem_wave", {
        "region": region,
        "dataset_id": dataset_id,
        "delay": delay,
        "universe": universe,
        "data_type": data_type,
        "wave": wave,
        "auto_dedup": auto_dedup,
        "auto_bucket": auto_bucket,
        "auto_skeleton": auto_skeleton,
        "auto_select": auto_select,
    })
    return result.to_dict()


@mcp.tool()
def workflow_unified_gate(
    region: str,
    dataset: str,
    wave: str,
    exprs_file: Optional[str] = None,
    from_db: bool = True,
    skip_diversity_gate: bool = False,
) -> Dict[str, Any]:
    """合并重复门禁检查 workflow 节点（unified_gate 节点快捷方式）.

    Args:
        region: 区域代码
        dataset: 数据集 ID
        wave: 波次号
        exprs_file: 表达式文件路径（可选）
        from_db: 是否从 DB 读取表达式（默认 True）
        skip_diversity_gate: 是否跳过多样性闸（默认 False）

    Returns:
        执行结果字典
    """
    from wqb.workflow import execute
    
    result = execute("unified_gate", {
        "region": region,
        "dataset": dataset,
        "wave": wave,
        "exprs_file": exprs_file,
        "from_db": from_db,
        "skip_diversity_gate": skip_diversity_gate,
    })
    return result.to_dict()


@mcp.tool()
def workflow_auto_harvest(
    region: str,
    wave: str,
    multisim_id: Optional[str] = None,
    auto_link: bool = True,
    auto_upsert: bool = True,
    auto_report: bool = True,
) -> Dict[str, Any]:
    """自动化收批 workflow 节点（auto_harvest 节点快捷方式）.

    Args:
        region: 区域代码
        wave: 波次号
        multisim_id: multisim ID（可选）
        auto_link: 是否自动关联 expressions（默认 True）
        auto_upsert: 是否自动写回 backtest_results（默认 True）
        auto_report: 是否自动生成收批报告（默认 True）

    Returns:
        执行结果字典
    """
    from wqb.workflow import execute
    
    result = execute("auto_harvest", {
        "region": region,
        "wave": wave,
        "multisim_id": multisim_id,
        "auto_link": auto_link,
        "auto_upsert": auto_upsert,
        "auto_report": auto_report,
    })
    return result.to_dict()


@mcp.tool()
def workflow_auto_review(
    region: str,
    wave: str,
    dataset: Optional[str] = None,
    auto_prescreen: bool = True,
    auto_walls: bool = True,
    auto_salvage: bool = True,
    auto_report: bool = True,
) -> Dict[str, Any]:
    """自动化评审 workflow 节点（auto_review 节点快捷方式）.

    Args:
        region: 区域代码
        wave: 波次号
        dataset: 数据集 ID（可选）
        auto_prescreen: 是否自动 S4 预筛（默认 True）
        auto_walls: 是否自动 walls 诊断（默认 True）
        auto_salvage: 是否自动卡闸辅助腿检索（默认 True）
        auto_report: 是否自动生成评审报告（默认 True）

    Returns:
        执行结果字典
    """
    from wqb.workflow import execute
    
    result = execute("auto_review", {
        "region": region,
        "wave": wave,
        "dataset": dataset,
        "auto_prescreen": auto_prescreen,
        "auto_walls": auto_walls,
        "auto_salvage": auto_salvage,
        "auto_report": auto_report,
    })
    return result.to_dict()


@mcp.tool()
def workflow_auto_pyramid(
    region: str,
    wave: str,
    delay: int = 1,
    auto_embed: bool = True,
    auto_report: bool = True,
) -> Dict[str, Any]:
    """自动化点塔进度回写 workflow 节点（auto_pyramid 节点快捷方式）.

    Args:
        region: 区域代码
        wave: 波次号
        delay: 延迟（默认 1）
        auto_embed: 是否自动嵌入 wave_result.key_findings（默认 True）
        auto_report: 是否自动生成点塔报告（默认 True）

    Returns:
        执行结果字典
    """
    from wqb.workflow import execute
    
    result = execute("auto_pyramid", {
        "region": region,
        "wave": wave,
        "delay": delay,
        "auto_embed": auto_embed,
        "auto_report": auto_report,
    })
    return result.to_dict()


if __name__ == "__main__":
    import os as _os_sc; _os_sc.environ.setdefault("WQB_STARTUP_CHECKS", "once")  # 启动校验每进程只打一次（2026-09-19）
    # stdio 模式启动（.mcp.json 注册）
    mcp.run()
