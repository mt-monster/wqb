# -*- coding: utf-8 -*-
"""提示词知识库（prompt_kb）——长期方案：提示词自动优化 + 版本管理 + A/B 测试。

设计目标：
1. **提示词版本管理**：每个提示词有版本号，支持回滚与 A/B 测试
2. **提示词自动优化**：基于历史回测结果自动优化提示词（如某个机制历史表现好，则加强）
3. **提示词知识库**：支持提示词的检索、复用、组合

数据模型：
- prompt_templates：提示词模板（category + version + content + metadata）
- prompt_performance：提示词性能（template_id + backtest_results + metrics）
- prompt_ab_tests：A/B 测试（test_id + template_a + template_b + winner）

集成方式：
- concept_first_rules(category, version=None) → 从知识库加载对应类别与版本的提示词
- 自动优化：定期分析 backtest_results，更新 prompt_performance，生成新版本提示词
"""
from __future__ import annotations

import json
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# 数据库路径（与 wqb.db 同库）
DB_PATH = Path(__file__).resolve().parent.parent.parent.parent.parent.parent / "data" / "wqb.db"


def _conn() -> sqlite3.Connection:
    """获取数据库连接（row_factory=Row，WAL 模式）。
    
    注意：本函数使用裸 sqlite3.connect 是因为 prompt_kb 是 GEM 引擎内部模块，
    需要独立于 wqb.db_conn 工厂（避免循环依赖）。已加入 DIRECT_CONNECT_WHITELIST
    白名单（src/wqb/db_conn.py），符合 test_db_write_guards 守护要求。
    """
    conn = sqlite3.connect(str(DB_PATH), timeout=30.0)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys=ON")
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA synchronous=NORMAL")
    conn.execute("PRAGMA busy_timeout=30000")  # 白名单要求：busy_timeout PRAGMA
    return conn


def _now() -> str:
    """获取当前时间戳。"""
    return datetime.now().isoformat(timespec="seconds")


# ---------------------------------------------------------------------------
# 表结构初始化
# ---------------------------------------------------------------------------

def init_prompt_kb_tables() -> None:
    """初始化提示词知识库表结构（幂等）。"""
    conn = _conn()
    c = conn.cursor()

    # 表 1：prompt_templates（提示词模板）
    c.execute("""
        CREATE TABLE IF NOT EXISTS prompt_templates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT NOT NULL,           -- 数据集类别（news/analyst/pv/fundamental/...）
            version INTEGER NOT NULL,          -- 版本号（从 1 开始递增）
            content TEXT NOT NULL,             -- 提示词内容（concept_first_rules 文本）
            metadata TEXT,                     -- 元数据（JSON：作者/创建时间/优化原因/父版本）
            is_active INTEGER DEFAULT 1,       -- 是否激活（0=停用，1=激活）
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            UNIQUE(category, version)
        )
    """)
    c.execute("""
        CREATE INDEX IF NOT EXISTS idx_prompt_templates_category_active
        ON prompt_templates(category, is_active)
    """)

    # 表 2：prompt_performance（提示词性能）
    c.execute("""
        CREATE TABLE IF NOT EXISTS prompt_performance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            template_id INTEGER NOT NULL,      -- 关联 prompt_templates.id
            region TEXT NOT NULL,              -- 区域
            dataset_id TEXT NOT NULL,          -- 数据集 ID
            wave TEXT NOT NULL,                -- 波次
            backtest_count INTEGER DEFAULT 0,  -- 回测数量
            pass_count INTEGER DEFAULT 0,      -- 过闸数量
            pass_rate REAL DEFAULT 0.0,        -- 过闸率
            avg_sharpe REAL DEFAULT 0.0,       -- 平均 sharpe
            best_sharpe REAL DEFAULT 0.0,      -- 最佳 sharpe
            metrics TEXT,                      -- 其他指标（JSON：fitness/turnover/coverage/...）
            created_at TEXT NOT NULL,
            FOREIGN KEY (template_id) REFERENCES prompt_templates(id) ON DELETE CASCADE
        )
    """)
    c.execute("""
        CREATE INDEX IF NOT EXISTS idx_prompt_performance_template
        ON prompt_performance(template_id, region, dataset_id)
    """)

    # 表 3：prompt_ab_tests（A/B 测试）
    c.execute("""
        CREATE TABLE IF NOT EXISTS prompt_ab_tests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            test_id TEXT NOT NULL UNIQUE,      -- 测试 ID（UUID）
            category TEXT NOT NULL,            -- 数据集类别
            template_a_id INTEGER NOT NULL,    -- 模板 A（关联 prompt_templates.id）
            template_b_id INTEGER NOT NULL,    -- 模板 B（关联 prompt_templates.id）
            region TEXT NOT NULL,              -- 区域
            dataset_id TEXT NOT NULL,          -- 数据集 ID
            status TEXT DEFAULT 'running',     -- 状态（running/completed/cancelled）
            winner_id INTEGER,                 -- 获胜模板 ID（NULL=未决）
            confidence REAL,                   -- 置信度（0-1）
            metrics TEXT,                      -- 测试指标（JSON：a_pass_rate/b_pass_rate/...）
            created_at TEXT NOT NULL,
            completed_at TEXT,
            FOREIGN KEY (template_a_id) REFERENCES prompt_templates(id) ON DELETE CASCADE,
            FOREIGN KEY (template_b_id) REFERENCES prompt_templates(id) ON DELETE CASCADE,
            FOREIGN KEY (winner_id) REFERENCES prompt_templates(id) ON DELETE SET NULL
        )
    """)
    c.execute("""
        CREATE INDEX IF NOT EXISTS idx_prompt_ab_tests_status
        ON prompt_ab_tests(status, category)
    """)

    conn.commit()
    conn.close()


# ---------------------------------------------------------------------------
# 提示词模板 CRUD
# ---------------------------------------------------------------------------

def create_prompt_template(
    category: str,
    content: str,
    metadata: Optional[Dict[str, Any]] = None,
    parent_version: Optional[int] = None,
) -> int:
    """创建提示词模板（返回模板 ID）。

    Args:
        category: 数据集类别
        content: 提示词内容
        metadata: 元数据（作者/创建时间/优化原因/父版本）
        parent_version: 父版本号（用于版本链追踪）

    Returns:
        模板 ID
    """
    conn = _conn()
    c = conn.cursor()

    # 获取下一个版本号
    c.execute(
        "SELECT MAX(version) FROM prompt_templates WHERE category=?",
        (category,),
    )
    max_version = c.fetchone()[0]
    next_version = (max_version or 0) + 1

    # 构建元数据
    meta = metadata or {}
    if parent_version is not None:
        meta["parent_version"] = parent_version
    meta["created_at"] = _now()

    # 插入新模板
    c.execute("""
        INSERT INTO prompt_templates (category, version, content, metadata, is_active, created_at, updated_at)
        VALUES (?, ?, ?, ?, 1, ?, ?)
    """, (category, next_version, content, json.dumps(meta, ensure_ascii=False), _now(), _now()))

    template_id = c.lastrowid
    conn.commit()
    conn.close()
    return template_id


def get_prompt_template(
    category: str,
    version: Optional[int] = None,
    active_only: bool = True,
) -> Optional[Dict[str, Any]]:
    """获取提示词模板（返回模板字典）。

    Args:
        category: 数据集类别
        version: 版本号（None=最新激活版本）
        active_only: 是否只返回激活版本

    Returns:
        模板字典（含 id/category/version/content/metadata/is_active/created_at/updated_at）
    """
    conn = _conn()
    c = conn.cursor()

    if version is not None:
        # 获取指定版本
        c.execute("""
            SELECT * FROM prompt_templates WHERE category=? AND version=?
        """, (category, version))
    else:
        # 获取最新激活版本
        sql = "SELECT * FROM prompt_templates WHERE category=?"
        params = [category]
        if active_only:
            sql += " AND is_active=1"
        sql += " ORDER BY version DESC LIMIT 1"
        c.execute(sql, params)

    row = c.fetchone()
    conn.close()

    if not row:
        return None

    result = dict(row)
    if result.get("metadata"):
        try:
            result["metadata"] = json.loads(result["metadata"])
        except (json.JSONDecodeError, TypeError):
            result["metadata"] = {}
    return result


def list_prompt_templates(
    category: Optional[str] = None,
    active_only: bool = True,
    limit: int = 50,
) -> List[Dict[str, Any]]:
    """列出提示词模板（返回模板列表）。

    Args:
        category: 数据集类别（None=全部类别）
        active_only: 是否只返回激活版本
        limit: 返回数量上限

    Returns:
        模板列表（按 category + version DESC 排序）
    """
    conn = _conn()
    c = conn.cursor()

    sql = "SELECT * FROM prompt_templates WHERE 1=1"
    params = []
    if category:
        sql += " AND category=?"
        params.append(category)
    if active_only:
        sql += " AND is_active=1"
    sql += " ORDER BY category, version DESC LIMIT ?"
    params.append(limit)

    c.execute(sql, params)
    rows = c.fetchall()
    conn.close()

    results = []
    for row in rows:
        result = dict(row)
        if result.get("metadata"):
            try:
                result["metadata"] = json.loads(result["metadata"])
            except (json.JSONDecodeError, TypeError):
                result["metadata"] = {}
        results.append(result)
    return results


def deactivate_prompt_template(template_id: int) -> bool:
    """停用提示词模板（返回是否成功）。"""
    conn = _conn()
    c = conn.cursor()
    c.execute("""
        UPDATE prompt_templates SET is_active=0, updated_at=? WHERE id=?
    """, (_now(), template_id))
    success = c.rowcount > 0
    conn.commit()
    conn.close()
    return success


# ---------------------------------------------------------------------------
# 提示词性能记录
# ---------------------------------------------------------------------------

def record_prompt_performance(
    template_id: int,
    region: str,
    dataset_id: str,
    wave: str,
    backtest_count: int,
    pass_count: int,
    avg_sharpe: float = 0.0,
    best_sharpe: float = 0.0,
    metrics: Optional[Dict[str, Any]] = None,
) -> int:
    """记录提示词性能（返回记录 ID）。

    Args:
        template_id: 模板 ID
        region: 区域
        dataset_id: 数据集 ID
        wave: 波次
        backtest_count: 回测数量
        pass_count: 过闸数量
        avg_sharpe: 平均 sharpe
        best_sharpe: 最佳 sharpe
        metrics: 其他指标（fitness/turnover/coverage/...）

    Returns:
        记录 ID
    """
    conn = _conn()
    c = conn.cursor()

    pass_rate = pass_count / backtest_count if backtest_count > 0 else 0.0

    c.execute("""
        INSERT INTO prompt_performance (
            template_id, region, dataset_id, wave,
            backtest_count, pass_count, pass_rate, avg_sharpe, best_sharpe,
            metrics, created_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        template_id, region, dataset_id, wave,
        backtest_count, pass_count, pass_rate, avg_sharpe, best_sharpe,
        json.dumps(metrics or {}, ensure_ascii=False), _now(),
    ))

    record_id = c.lastrowid
    conn.commit()
    conn.close()
    return record_id


def get_prompt_performance(
    template_id: int,
    region: Optional[str] = None,
    dataset_id: Optional[str] = None,
    limit: int = 50,
) -> List[Dict[str, Any]]:
    """获取提示词性能记录（返回记录列表）。"""
    conn = _conn()
    c = conn.cursor()

    sql = "SELECT * FROM prompt_performance WHERE template_id=?"
    params = [template_id]
    if region:
        sql += " AND region=?"
        params.append(region)
    if dataset_id:
        sql += " AND dataset_id=?"
        params.append(dataset_id)
    sql += " ORDER BY created_at DESC LIMIT ?"
    params.append(limit)

    c.execute(sql, params)
    rows = c.fetchall()
    conn.close()

    results = []
    for row in rows:
        result = dict(row)
        if result.get("metrics"):
            try:
                result["metrics"] = json.loads(result["metrics"])
            except (json.JSONDecodeError, TypeError):
                result["metrics"] = {}
        results.append(result)
    return results


# ---------------------------------------------------------------------------
# A/B 测试
# ---------------------------------------------------------------------------

def create_ab_test(
    test_id: str,
    category: str,
    template_a_id: int,
    template_b_id: int,
    region: str,
    dataset_id: str,
) -> int:
    """创建 A/B 测试（返回测试 ID）。"""
    conn = _conn()
    c = conn.cursor()

    c.execute("""
        INSERT INTO prompt_ab_tests (
            test_id, category, template_a_id, template_b_id,
            region, dataset_id, status, created_at
        ) VALUES (?, ?, ?, ?, ?, ?, 'running', ?)
    """, (test_id, category, template_a_id, template_b_id, region, dataset_id, _now()))

    test_db_id = c.lastrowid
    conn.commit()
    conn.close()
    return test_db_id


def complete_ab_test(
    test_id: str,
    winner_id: Optional[int],
    confidence: float,
    metrics: Optional[Dict[str, Any]] = None,
) -> bool:
    """完成 A/B 测试（返回是否成功）。"""
    conn = _conn()
    c = conn.cursor()

    c.execute("""
        UPDATE prompt_ab_tests
        SET status='completed', winner_id=?, confidence=?, metrics=?, completed_at=?
        WHERE test_id=?
    """, (winner_id, confidence, json.dumps(metrics or {}, ensure_ascii=False), _now(), test_id))

    success = c.rowcount > 0
    conn.commit()
    conn.close()
    return success


def get_ab_test(test_id: str) -> Optional[Dict[str, Any]]:
    """获取 A/B 测试（返回测试字典）。"""
    conn = _conn()
    c = conn.cursor()

    c.execute("SELECT * FROM prompt_ab_tests WHERE test_id=?", (test_id,))
    row = c.fetchone()
    conn.close()

    if not row:
        return None

    result = dict(row)
    if result.get("metrics"):
        try:
            result["metrics"] = json.loads(result["metrics"])
        except (json.JSONDecodeError, TypeError):
            result["metrics"] = {}
    return result


# ---------------------------------------------------------------------------
# 提示词自动优化
# ---------------------------------------------------------------------------

def analyze_prompt_performance(
    category: str,
    region: Optional[str] = None,
    dataset_id: Optional[str] = None,
    min_backtest_count: int = 10,
) -> Dict[str, Any]:
    """分析提示词性能（返回分析结果）。

    Args:
        category: 数据集类别
        region: 区域（None=全部区域）
        dataset_id: 数据集 ID（None=全部数据集）
        min_backtest_count: 最小回测数量（过滤样本不足的记录）

    Returns:
        分析结果（含 best_template_id / avg_pass_rate / avg_sharpe / recommendations）
    """
    conn = _conn()
    c = conn.cursor()

    # 获取该类别的所有模板
    c.execute("""
        SELECT id, version FROM prompt_templates WHERE category=? AND is_active=1
    """, (category,))
    templates = {row[0]: row[1] for row in c.fetchall()}

    if not templates:
        conn.close()
        return {"error": f"no active templates for category={category}"}

    # 获取性能记录
    sql = """
        SELECT template_id, AVG(pass_rate) as avg_pass_rate, AVG(avg_sharpe) as avg_sharpe,
               SUM(backtest_count) as total_backtests, SUM(pass_count) as total_passes
        FROM prompt_performance
        WHERE template_id IN ({})
    """.format(",".join("?" * len(templates)))
    params = list(templates.keys())

    if region:
        sql += " AND region=?"
        params.append(region)
    if dataset_id:
        sql += " AND dataset_id=?"
        params.append(dataset_id)
    sql += " GROUP BY template_id HAVING SUM(backtest_count) >= ?"
    params.append(min_backtest_count)

    c.execute(sql, params)
    rows = c.fetchall()
    conn.close()

    if not rows:
        return {"error": f"no performance records for category={category} (min_backtest_count={min_backtest_count})"}

    # 分析结果
    results = []
    for row in rows:
        template_id, avg_pass_rate, avg_sharpe, total_backtests, total_passes = row
        results.append({
            "template_id": template_id,
            "version": templates[template_id],
            "avg_pass_rate": avg_pass_rate,
            "avg_sharpe": avg_sharpe,
            "total_backtests": total_backtests,
            "total_passes": total_passes,
        })

    # 按 avg_pass_rate 排序
    results.sort(key=lambda x: x["avg_pass_rate"], reverse=True)

    # 生成推荐
    best = results[0] if results else None
    recommendations = []
    if best:
        recommendations.append(f"最佳模板：v{best['version']}（过闸率 {best['avg_pass_rate']:.1%}，平均 sharpe {best['avg_sharpe']:.2f}）")
        if len(results) > 1:
            worst = results[-1]
            if best["avg_pass_rate"] - worst["avg_pass_rate"] > 0.1:
                recommendations.append(f"性能差异显著（{best['avg_pass_rate']:.1%} vs {worst['avg_pass_rate']:.1%}），建议停用低性能模板")

    return {
        "category": category,
        "region": region,
        "dataset_id": dataset_id,
        "templates": results,
        "best_template_id": best["template_id"] if best else None,
        "avg_pass_rate": best["avg_pass_rate"] if best else 0.0,
        "avg_sharpe": best["avg_sharpe"] if best else 0.0,
        "recommendations": recommendations,
    }


def optimize_prompt_template(
    category: str,
    optimization_reason: str,
    performance_data: Optional[Dict[str, Any]] = None,
) -> Optional[int]:
    """基于性能数据自动优化提示词模板（返回新模板 ID）。

    Args:
        category: 数据集类别
        optimization_reason: 优化原因（如 "基于历史回测结果加强高过闸率机制"）
        performance_data: 性能数据（可选，用于指导优化方向）

    Returns:
        新模板 ID（失败返回 None）
    """
    # 获取当前激活模板
    current = get_prompt_template(category, active_only=True)
    if not current:
        return None

    # 分析性能数据，生成优化建议
    # TODO: 实现基于性能数据的自动优化逻辑（如加强高过闸率机制、削弱低过闸率机制）
    # 当前实现：简单复制当前模板内容，添加优化标记
    optimized_content = current["content"]
    if performance_data:
        # 示例：如果某个机制历史表现好，在提示词中加强
        # 实际实现需要更复杂的逻辑（如分析 backtest_results 中的 mechanism 分布）
        pass

    # 创建新模板
    metadata = {
        "optimization_reason": optimization_reason,
        "performance_data": performance_data or {},
        "auto_generated": True,
    }
    new_template_id = create_prompt_template(
        category=category,
        content=optimized_content,
        metadata=metadata,
        parent_version=current["version"],
    )

    return new_template_id


# ---------------------------------------------------------------------------
# 初始化（模块导入时自动创建表结构）
# ---------------------------------------------------------------------------

try:
    init_prompt_kb_tables()
except Exception:
    # 表结构创建失败不阻断模块导入（如数据库不存在）
    pass
