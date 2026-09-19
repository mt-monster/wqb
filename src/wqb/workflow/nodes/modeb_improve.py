# -*- coding: utf-8 -*-
"""Mode B 想法层改进节点（S4 增强）.

实现 4 阶段 Mode B 改进策略：
- Phase 0: Conditional signals (regime-dependent)
- Phase 1: Residual structures (industry-neutralized)
- Phase 2: Interaction terms (cross-concept)
- Phase 3: Temporal innovations (momentum/acceleration/inflection)
"""

import sqlite3
import hashlib
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

DB = r'D:\coding\traeCN_project\wqb\data\wqb.db'


def run(
    region: str,
    dataset: str,
    base_field: str,
    phase: Optional[int] = None,
    wave: Optional[str] = None,
    start_wave: int = 160,
    _context: Optional[Dict[str, Any]] = None,
    dry_run: bool = False,
) -> Dict[str, Any]:
    """Mode B 想法层改进节点.
    
    Args:
        region: 区域代码
        dataset: 数据集 ID
        base_field: 基础字段名
        phase: 运行特定阶段 (0-3)，None 表示全部
        wave: 指定 wave 号，None 自动分配
        start_wave: 起始 wave 号（默认 160）
        dry_run: 干跑模式（不实际插入）
    
    Returns:
        执行结果
    """
    if dry_run:
        return {
            "success": True,
            "dry_run": True,
            "region": region,
            "dataset": dataset,
            "base_field": base_field,
            "phase": phase,
            "message": "Dry run: would generate Mode B improvement expressions",
        }
    
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    
    try:
        results = {}
        
        if phase is not None:
            # Run specific phase
            exprs = _generate_phase(region, dataset, base_field, phase)
            wave = wave or str(start_wave + phase)
            count = _insert_wave(conn, region, dataset, exprs, wave)
            results[phase] = count
        else:
            # Run all phases
            for p in range(4):
                exprs = _generate_phase(region, dataset, base_field, p)
                wave = str(start_wave + p)
                count = _insert_wave(conn, region, dataset, exprs, wave)
                results[p] = count
        
        return {
            "success": True,
            "region": region,
            "dataset": dataset,
            "base_field": base_field,
            "results": results,
            "total_expressions": sum(results.values()),
        }
    
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "region": region,
            "dataset": dataset,
            "base_field": base_field,
        }
    
    finally:
        conn.close()


def _generate_phase(region: str, dataset: str, base_field: str, phase: int) -> List[Dict[str, str]]:
    """Generate expressions for a specific phase."""
    f = base_field
    
    if phase == 0:
        # Conditional signals
        return [
            {"expr": f"trade_when(ts_zscore(ts_std_dev(returns, 21), 63) > 1, rank(ts_backfill({f}, 66)), nan)",
             "tag": "cond_highvol", "concept": "regime"},
            {"expr": f"trade_when(ts_zscore(ts_std_dev(returns, 21), 63) > 1, rank({f}), rank(-{f}))",
             "tag": "cond_switch", "concept": "regime"},
            {"expr": f"trade_when(ts_zscore(ts_delta(ts_mean(volume, 21), 5), 63) < -1, rank(ts_backfill({f}, 66)), nan)",
             "tag": "cond_volcontract", "concept": "regime"},
            {"expr": f"trade_when(ts_std_dev(returns, 21) > ts_mean(ts_std_dev(returns, 21), 63), rank(ts_backfill({f}, 66)), nan)",
             "tag": "cond_volmean", "concept": "regime"},
        ]
    
    elif phase == 1:
        # Residual structures
        return [
            {"expr": f"subtract(rank(ts_backfill({f}, 66)), group_neutralize(rank(ts_backfill({f}, 66)), industry))",
             "tag": "resid_industry", "concept": "residual"},
            {"expr": f"subtract(rank({f}), group_neutralize(rank({f}), subindustry))",
             "tag": "resid_subind", "concept": "residual"},
            {"expr": f"ts_zscore(subtract(rank({f}), group_neutralize(rank({f}), industry)), 63)",
             "tag": "resid_zscore", "concept": "residual"},
        ]
    
    elif phase == 2:
        # Interaction terms
        return [
            {"expr": f"multiply(rank({f}), rank(ts_delta(ts_mean(volume, 21), 5)))",
             "tag": "def_x_liquidity", "concept": "interaction"},
            {"expr": f"multiply(rank(ts_backfill({f}, 66)), rank(ts_zscore(volume, 63)))",
             "tag": "def_x_volzscore", "concept": "interaction"},
            {"expr": f"multiply(rank({f}), rank(-ts_std_dev(returns, 21)))",
             "tag": "def_x_lowvol", "concept": "interaction"},
            {"expr": f"multiply(rank({f}), rank(ts_arg_max(volume, 21)))",
             "tag": "def_x_volpeak", "concept": "interaction"},
        ]
    
    elif phase == 3:
        # Temporal innovations
        return [
            {"expr": f"rank(ts_delta({f}, 21))",
             "tag": "temp_momentum", "concept": "temporal"},
            {"expr": f"rank(ts_delta(ts_delta({f}, 5), 5))",
             "tag": "temp_accel", "concept": "temporal"},
            {"expr": f"rank(ts_arg_max({f}, 63))",
             "tag": "temp_inflection", "concept": "temporal"},
            {"expr": f"rank(ts_zscore({f}, 252))",
             "tag": "temp_longz", "concept": "temporal"},
        ]
    
    else:
        return []


def _insert_wave(conn: sqlite3.Connection, region: str, dataset: str, 
                 exprs: List[Dict[str, str]], wave: str) -> int:
    """Insert expressions into a wave."""
    max_wid = conn.execute("SELECT COALESCE(MAX(wave_id), 0) FROM expressions").fetchone()[0]
    new_wave_id = max_wid + 1
    max_id = conn.execute("SELECT MAX(id) FROM expressions").fetchone()[0]
    now = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S')
    
    for i, e in enumerate(exprs):
        new_id = max_id + 1 + i
        fp = hashlib.sha1(e["expr"].encode()).hexdigest()[:16]
        conn.execute("""
        INSERT INTO expressions (id, wave_id, expression, fingerprint, status, region, wave, dataset, created_at, updated_at)
        VALUES (?, ?, ?, ?, 'selected', ?, ?, ?, ?, ?)
        """, (new_id, new_wave_id, e["expr"], fp, region, wave, dataset, now, now))
    
    conn.commit()
    return len(exprs)
