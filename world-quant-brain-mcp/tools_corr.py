"""相关性工具 (prod/self/mutual) — MCP 工具层 (2026-08-13 自 main.py 按域拆分)。"""
import os, re
from typing import Dict, List, Any

from mcp_core import mcp, brain_client, _slim_check_correlation

@mcp.tool()

async def check_correlation(alpha_id: str) -> Dict[str, Any]:
    """Check alpha correlation against production alphas, self alphas, or both."""
    correlation_type = "both"
    threshold = 0.7
    try:
        return _slim_check_correlation(await brain_client.check_correlation(alpha_id, correlation_type, threshold))
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
