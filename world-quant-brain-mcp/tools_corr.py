"""相关性工具 (prod/self/mutual) — MCP 工具层 (2026-08-13 自 main.py 按域拆分)。"""
import os, re
from typing import Dict, List, Any

from mcp_core import mcp, brain_client, _slim_check_correlation

@mcp.tool()
async def check_correlation(
    alpha_id: str,
    correlation_type: str = "both",
    refresh: bool = False,
) -> Dict[str, Any]:
    """Check alpha correlation against the production pool and/or self pool.

    correlation_type（2026-10-28 起可传，缺省 both 保持旧行为）：
      * 'production' —— 只查 prod。只需要 prod 判定时用这个，省去 self 侧的
        OS 池全量列举与 PnL 增量下载。
      * 'self'       —— 只查 self（本地 OS 池计算，不占平台相关性槽）。
      * 'both'       —— 先 prod 后 self；prod fail 时早退，不计算 self。
    threshold 固定 0.7（合规红线，严格不等式：max < 0.7 才 PASS）。

    缓存与回源：平台 prod 计算为异步排队（单并发，1-5 分钟）；同一 alpha 的已决
    prod 结果写入权威表 alpha_corr_cache，**保鲜 48h**（生产池会漂移），命中直接
    返回不占队列；缺失/过期自动回源。平台详情里已算好的值（is.prodCorrelation）
    经预读直接采纳——返回里 source=alpha_detail_cached、无直方图、不写缓存。
    correlation_busy（另一进程/调用正占平台单并发槽）与 pending 不缓存，按
    retry_after 稍后重查。

    并发语义（2026-10-28）：busy/pending 的返回体会带 ``retry_after``（秒）与
    ``inflight``（该 alpha 正在平台计算中）——按 retry_after 隔时重查即可，
    **inflight=true 时不要重新触发**（重复触发只会把自己顶成 busy）。
    同 alpha 的其它调用方会被 join 到这次计算上（``joined=true``），预热值
    带 ``provisional=true``（平台存储值、测量时间不可知，终验须 refresh=True）。

    refresh=True：跳过本地缓存**并跳过预读**，强制走平台重测——交付前终验用
    （prod 漂移猛，台账 5 天作废）。
    """
    if correlation_type not in ("production", "self", "both"):
        return {"error": f"correlation_type 必须是 production|self|both，收到 {correlation_type!r}"}
    threshold = 0.7
    try:
        return _slim_check_correlation(await brain_client.check_correlation(alpha_id, correlation_type, threshold, refresh=refresh))
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()

async def check_self_correlation(
    alpha_id: str,
    threshold: float = 0.7,
    correlation_type: str = 'self',
) -> Dict[str, Any]:
    """Validate self-correlation with the local incremental-cache calculation.

    This does not call the BRAIN /correlations/self endpoint, so it does not
    consume the platform correlation slot or use the correlation lock.

    The OS pool is partitioned by each alpha's ``classifications`` to match the
    platform exactly (the platform reports two numbers from the same pool):
      * correlation_type='self' (default) -> "Self Correlation": pool EXCLUDES
        Power Pool Alphas. Use this to mirror the submission "Self Correlation".
      * correlation_type='powerpool' -> "Power Pool Correlation": pool is ONLY
        Power Pool Alphas.
      * correlation_type='all' -> legacy whole-pool behaviour (mixes both;
        can over-report vs the platform's Self Correlation).

    Args:
        alpha_id: Target alpha ID.
        threshold: Pass/fail threshold applied to each max correlation
            (passes when max < threshold). Default 0.7.
        correlation_type: 'self' | 'powerpool' | 'all'. Default 'self'.

    Returns:
        Dict with the local max self-correlation, pass/fail result, top
        correlated OS alpha records, and pool-partition metadata
        (full_os_pool_size, excluded_power_pool_count, correlation_type).
    """
    try:
        return _slim_check_correlation(await brain_client.check_self_correlation(
            alpha_id,
            threshold=threshold,
            correlation_type=correlation_type,
        ))
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()

async def compute_mutual_correlation(
    alpha_ids: List[str],
    threshold: float = 0.5,
    years: int = 4,
) -> Dict[str, Any]:
    """Compute pairwise ("mutual") correlation AMONG a given set of your alphas.

    Use this to vet a submission basket that must be mutually decorrelated
    (e.g. a "no two alphas may correlate above 0.5" rule). It is fully local —
    it fetches each alpha's PnL and correlates their daily returns; it does NOT
    call the BRAIN correlation endpoint or consume the correlation slot.

    Distinct from the other two correlation tools:
      * check_correlation      -> target vs the PRODUCTION pool.
      * check_self_correlation -> target vs your submitted-OS pool
                                  (Self excl. Power Pool Alphas / Power Pool only).
      * compute_mutual_correlation (this) -> the full NxN matrix AMONG the
                                  supplied alphas themselves.

    Correlation is on the last ``years`` of daily returns (diff of cumulative
    PnL), matching the local self-correlation convention.

    Args:
        alpha_ids: 2+ alpha IDs to correlate against each other.
        threshold: Max acceptable pairwise correlation (default 0.5).
        years: Trailing window of daily returns to use (default 4).

    Returns:
        Dict with: matrix (NxN), max_pair (most-correlated pair),
        pairs_over_threshold, all_below_threshold (bool), and
        max_mutually_below_subset (a greedy maximal basket whose members are all
        mutually below threshold), plus missing_pnl for any unfetchable ids.
    """
    try:
        return await brain_client.get_mutual_correlation(alpha_ids, threshold=threshold, years=years)
    except Exception as e:
        return {"error": str(e)}
