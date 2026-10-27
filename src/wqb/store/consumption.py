# -*- coding: utf-8 -*-
"""「表达式被回测消费」的唯一口径（single source of truth，2026-10-20 P1-3 固化）。

背景（审计实测，EUR 2026-10-20）：同一件事三处各算一遍、结论差一倍 ——

  * backlog 闸（`wqb.workflow.nodes.campaign._run_backlog_gate`）只看
    `expressions.status`：EUR 458/13086 = **3.5%**。漏掉 status='dropped'
    但 id 已被 `backtest_results.expression_id` 指向的 311 行（回测过、状态被覆盖）；
  * mining_yield（`wqb_db_mcp.get_mining_yield`）只数 `backtest_results` 行：
    EUR 934 行 = 7.1%（回测行会因重复回测重复计数，且看不到 status 已回填、行已清理的行）；
  * 实测真值（EUR）：consumed = **866** = 状态口径 ∪ expr_id 口径 ∪ alpha_id 口径（6.6%）。

口径（两把规范键 + 状态并集，取并集不取交集）：

    consumed(e) := e.status ∈ CONSUMED_STATUSES
                 ∪ e.id ∈ backtest_results.expression_id
                 ∪ e.alpha_id ∈ backtest_results.alpha_id

为什么**不做**文本 join（`backtest_results.code = expressions.expression`）：
EUR 上文本 join 会多出 259 条，逐条核查 254/254 是**跨波重复副本**（同文本存在 ≥2 行，
bt 行的 expression_id 指向同文本的**另一行**；0 条 unique，5 条 bt 行在其它区域）——
把它们算进 consumed 等于把 dedup 掉的副本当作已消费，高估。故不认文本键。

消费方：
  * `wqb.workflow.nodes.campaign._run_backlog_gate`（conversion 分子）
  * `wqb_db_mcp.get_mining_yield`（conversion 分子；backtested=行数另列保留为吞吐）
新增消费方一律经本模块，禁止各自手写 SQL 谓词。
"""
import sqlite3

#: 视为「已消费」的 expressions.status 集合（被回测改写过的三类终态）
CONSUMED_STATUSES = ("backtested", "submitted", "completed")

_STATUS_IN = ", ".join(f"'{s}'" for s in CONSUMED_STATUSES)


def has_backtest_link(conn: sqlite3.Connection) -> bool:
    """backtest_results 表存在且带 expression_id / alpha_id 两把键。

    旧库 / 测试夹具可能根本没有这张表（或列不全）——`PRAGMA table_info` 对不存在的表
    返回空集而非报错，故这里显式判列。False 时走纯状态口径（退化但不崩）。
    """
    try:
        cols = {r[1] for r in conn.execute("PRAGMA table_info(backtest_results)")}
    except sqlite3.Error:
        return False
    return "expression_id" in cols and "alpha_id" in cols


def consumed_sql(alias: str = "e", with_backtest: bool = True) -> str:
    """consumed 谓词（SQL 布尔式），作用于别名 `alias` 的 expressions 行。

    with_backtest=False 退化为纯状态口径（配合 `has_backtest_link` 的判定使用）。
    子查询用 `IN (SELECT …)` 而非相关 EXISTS：实测（EUR，0.05s）前者把两张表各物化一次，
    后者在两万行级会上到分钟级。
    """
    pred = f"{alias}.status IN ({_STATUS_IN})"
    if with_backtest:
        pred += (
            f" OR {alias}.id IN "
            f"(SELECT expression_id FROM backtest_results WHERE expression_id IS NOT NULL)"
            f" OR ({alias}.alpha_id IS NOT NULL AND {alias}.alpha_id IN "
            f"(SELECT alpha_id FROM backtest_results WHERE alpha_id IS NOT NULL))"
        )
    return f"({pred})"