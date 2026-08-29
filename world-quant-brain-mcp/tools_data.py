"""数据集/字段/算子/文档/表达式校验工具 — MCP 工具层 (2026-08-13 自 main.py 按域拆分)。"""
import os, re, sys, asyncio, time, logging
import logging
from typing import Dict, List, Optional, Any, Sequence, Tuple
from datetime import datetime
from pathlib import Path

from mcp_core import mcp, brain_client, logger, _slim_datafields, _slim_datasets, _slim_text_lookup

@mcp.tool()

async def get_datasets(
    category: Optional[str] = None,
    region: str = "USA",
    delay: int = 1,
    universe: str = "TOP3000",
    theme: str = "false",
    search: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Get available datasets for research.
    
    Use this to discover what data is available for your alpha research.
    
    Args:
        category: Type of datesets (e.g., "news","sentiment","option")
        region: Market region (e.g., "USA")
        delay: Data delay (0 or 1)
        universe: Universe of stocks (e.g., "TOP3000")
        theme: Theme filter
    
    Returns:
        Available datasets
    """
    try:
        return _slim_datasets(await brain_client.get_datasets(category, region, delay, universe, theme, search))
    except Exception as e:
        return {"error": f"An unexpected error occurred: {str(e)}"}

@mcp.tool()

async def get_datafields(
    region: str,
    dataset_id: Optional[str],
    universe: str,
    delay: int = 1,
    data_type: str = "",
    search: Optional[str] = None,
    filter_sharpe: bool = True,
) -> Dict[str, Any]:
    """
    Get available data fields for alpha construction.
    
    Use this to find specific data fields you can use in your alpha formulas.
    By default, fields with OS/IS Sharpe ratio < 0 are filtered out to improve quality.
    
    Args:
        region: Market region (e.g., "USA"、"GLB"、"IND"、"ASI"、"CHN")
        delay: Data delay (0 or 1)
        universe: Universe of stocks (e.g., USA和GLB默认"TOP3000"、IND默认"TOP500"、ASI默认"MINVOL1M"、CHN默认"TOP2000U")
        dataset_id: Specific dataset ID to filter by
        data_type: Type of data (e.g., "MATRIX",'VECTOR','GROUP')
        search: Search term to filter fields
        filter_sharpe: Filter out fields with OS/IS Sharpe < 0 (default: True)
    
    Returns:
        Available data fields
    """
    instrument_type = "EQUITY"
    theme = "false"
    try:
        return _slim_datafields(await brain_client.get_datafields(instrument_type, region, delay, universe, theme, dataset_id, data_type, search, filter_sharpe))
    except Exception as e:
        return {"error": f"An unexpected error occurred: {str(e)}"}

@mcp.tool()

async def value_factor_trendScore(start_date: str, end_date: str) -> Dict[str, Any]:
    """Compute and return the diversity score for REGULAR alphas in a submission-date window.
    This function calculate the diversity of the users' submission, by checking the diversity, we can have a good understanding on the valuefactor's trend.
    This MCP tool wraps BrainApiClient.value_factor_trendScore and always uses submission dates (OS).

    Inputs:
        - start_date: ISO UTC start datetime (e.g. '2025-08-14T00:00:00Z')
        - end_date: ISO UTC end datetime (e.g. '2025-08-18T23:59:59Z')
        - p_max: optional integer total number of pyramid categories for normalization

    Returns: compact JSON with diversity_score, N, A, P, P_max, S_A, S_P, S_H, per_pyramid_counts
    """
    try:
        return await brain_client.value_factor_trendScore(start_date=start_date, end_date=end_date)
    except Exception as e:
        return {"error": str(e)}

# --- Community and Events Tools ---

@mcp.tool()

async def get_operators() -> Dict[str, Any]:
    """
    Get available operators for alpha creation.
    
    Returns:
        Dictionary containing operators list and count
    """
    try:
        operators = await brain_client.get_operators()
        if isinstance(operators, list):
            return _slim_text_lookup({"results": operators, "count": len(operators)}, n=160)
        return _slim_text_lookup(operators, n=160)
    except Exception as e:
        return {"error": f"An unexpected error occurred: {str(e)}"}

@mcp.tool()

async def run_selection(
    selection: str,
    instrument_type: str = "EQUITY",
    region: str = "USA",
    delay: int = 1,
    selection_limit: int = 1000,
    selection_handling: str = "POSITIVE",
) -> Dict[str, Any]:
    """
    Run a selection query to filter instruments.
    
    Args:
        selection: Selection criteria
        instrument_type: Type of instruments
        region: Geographic region
        delay: Delay setting
        selection_limit: Maximum number of results
        selection_handling: How to handle selection results
    
    Returns:
        Selection results
    """
    try:
        return await brain_client.run_selection(
            selection, instrument_type, region, delay, selection_limit, selection_handling
        )
    except Exception as e:
        return {"error": f"An unexpected error occurred: {str(e)}"}

@mcp.tool()

async def get_documentations() -> Dict[str, Any]:
    """
    Get available documentations and learning materials.
    
    Returns:
        List of documentations
    """
    try:
        return await brain_client.get_documentations()
    except Exception as e:
        return {"error": f"An unexpected error occurred: {str(e)}"}

# --- Message and Forum Tools ---

@mcp.tool()

async def recommend_datasets(
    region: str = "USA",
    delay: int = 1,
    universe: str = "TOP3000",
    top_n: int = 20,
) -> Dict[str, Any]:
    """
    Recommend datasets for alpha construction with unlit pyramid priority:
    
    1. **Pyramid lighting (点塔)**: Uses the pyramid-alphas and pyramid-multipliers
       endpoints. Unlit pyramids (fewer than 3 alphas) are recommended first.
    2. **Dataset quality**: Ranks datasets by OS/IS Sharpe within the same pyramid.
    3. **Dataset popularity**: Favors datasets with more platform users and more
       submitted alphas (dataset userCount and alphaCount).
    4. **Randomness**: Adds a small random score so recommendations keep some variety.
    
    Each dataset gets a score (0~95):
    - Pyramid lighting: 0~40 pts
    - Dataset quality: 0~30 pts
    - Dataset users: 0~10 pts
    - Dataset submissions: 0~10 pts
    - Randomness: 0~5 pts
    
    Args:
        region: Market region (e.g., "USA", "CHN", "EUR", "ASI", "GLB")
        delay: Data delay (0 or 1)
        universe: Stock universe (e.g., "TOP3000")
        top_n: Number of top recommendations to return (default 20)
    
    Returns:
        Ranked dataset recommendations with scores, pyramid status summary,
        and neutralization options for the selected region/delay/universe.
    """
    try:
        return await brain_client.recommend_datasets(region, delay, universe, top_n)
    except Exception as e:
        return {"error": f"An unexpected error occurred: {str(e)}"}

@mcp.tool()

async def expand_nested_data(data: List[Dict[str, Any]], preserve_original: bool = True) -> List[Dict[str, Any]]:
    """Flatten complex nested data structures into tabular format."""
    try:
        return await brain_client.expand_nested_data(data, preserve_original)
    except Exception as e:
        return [{"error": f"An unexpected error occurred: {str(e)}"}]
        
# --- Documentation Tool ---

@mcp.tool()

async def get_documentation_page(page_id: str) -> Dict[str, Any]:
    """Retrieve detailed content of a specific documentation page/article."""
    try:
        return await brain_client.get_documentation_page(page_id)
    except Exception as e:
        return {"error": f"An unexpected error occurred: {str(e)}"}

# --- Advanced Simulation Tools ---

_FIELD_RE = re.compile(r"[a-zA-Z_][a-zA-Z0-9_]*")


def _catalog_operator_names() -> set:
    """从 shared_libs/operators_catalog.py (8-11 平台 102 算子) 派生算子名 — 单一事实源。

    2026-08-13 修复: 原手写清单缺 ts_returns/ts_ir 等 catalog 算子, 导致
    validate_expressions 把它们误报为 unknown_fields (校验误杀)。catalog 不可用时
    回退空集 (校验降级为纯手工别名层, 不崩溃)。
    """
    try:
        skills_libs = Path.home() / ".zcode" / "skills" / "shared_libs"
        if str(skills_libs) not in sys.path:
            sys.path.insert(0, str(skills_libs))
        from operators_catalog import BY_NAME
        return set(BY_NAME.keys())
    except Exception as exc:  # skills 未注册/目录缺失 — 降级
        logger.warning(f"operators_catalog 不可用 ({exc}) — 字段预检算子过滤降级")
        return set()


# FASTEXPR 算子/语言关键字 (不视为字段) = catalog 102 (运行时派生)
# + 手工别名层 (catalog 拉取遗漏的 FASTEXPR 别名 + 语言关键字 + GROUP 维度;
#   sector/industry/... 是合法维度名, 排除后不会误伤字段名)。

_OPERATOR_KEYWORDS = _catalog_operator_names() | {
    # arithmetic / logical
    "add", "subtract", "multiply", "divide", "power", "abs", "log", "sign", "exp",
    "sqrt", "min", "max", "signed_power", "inverse", "purify", "round", "mod",
    "and", "or", "not", "if_else", "is_nan", "true", "false", "null", "nan",
    # cross-sectional
    "rank", "scale", "zscore", "winsorize", "pasteurize", "hump", "reverse",
    "bucket", "quantile", "fill", "trade_when",
    # time series
    "ts_rank", "ts_zscore", "ts_mean", "ts_std_dev", "ts_delta", "ts_decay_linear",
    "ts_backfill", "ts_regression", "ts_corr", "ts_covariance", "ts_sum",
    "ts_product", "ts_delay", "ts_argmax", "ts_argmin", "ts_scale", "ts_min",
    "ts_max", "ts_count", "ts_target_tvr_decay", "ts_trend", "ts_stdev",
    "ts_average", "ts_median", "ts_momentum", "ts_skewness", "ts_kurtosis",
    "ts_entropy", "ts_kurtosis1", "ts_av_diff",
    # group
    "group_rank", "group_zscore", "group_neutralize", "group_mean", "group_scale",
    "group_count", "group_std_dev", "group_sum", "group_backfill",
    "group_cartesian_product", "group_percentage", "group_max", "group_min",
    # vector
    "vec_avg", "vec_sum", "vec_count", "vec_max", "vec_min", "vec_stddev",
    "vec_zscore", "vec_dot", "vec_choose",
    # GROUP dimensions (always available)
    "sector", "industry", "subindustry", "country", "market", "exchange",
    "currency", "ticker", "cusip", "sedol", "isin",
}

def _extract_field_candidates(alpha_expressions) -> List[str]:
    candidates: set = set()
    for expr in alpha_expressions:
        candidates.update(_FIELD_RE.findall(expr or ""))
    return sorted(candidates - _OPERATOR_KEYWORDS)


def _ids_from_datafields_payload(payload) -> set:
    if not isinstance(payload, dict):
        return set()
    return {f.get("id") for f in (payload.get("results") or []) if isinstance(f, dict) and f.get("id")}


async def _verify_fields_exist(
    candidates: Sequence[str],
    *,
    instrument_type: str = "EQUITY",
    region: str = "USA",
    universe: str = "TOP3000",
    delay: int = 1,
    client=None,
    max_concurrency: int = 6,
    total_timeout: float = 120.0,
    cache_ttl: int = 86400,
) -> Dict[str, Any]:
    """Confirm candidate field ids via targeted platform search.

    Never treats "missing from an unscoped/paginated dump" as unknown.
    A field is unknown only when a targeted lookup succeeds and the exact
    id is absent. Lookup errors / incomplete payloads fail open (skip).

    2026-08-16 修复: 并发执行字段验证 + 总超时控制，避免串行调用导致
    validate_expressions 超时（每个 API 调用默认 30s，字段多时累计超时）。
    2026-08-16 优化: Redis 缓存字段验证结果（TTL 24h），避免重复查询
    同一字段（region/universe/delay 组合下字段存在性基本不变）。
    """
    client = client or brain_client
    ordered = list(dict.fromkeys(candidates))
    known: List[str] = []
    unknown: List[str] = []
    lookup_errors: List[str] = []

    if not ordered:
        return {
            "known": known,
            "unknown": unknown,
            "skipped": False,
            "warning": None,
            "lookup_errors": lookup_errors,
        }

    # --- Redis cache: check which fields are already verified ---
    cache_prefix = f"field_exists:{instrument_type}:{region}:{universe}:{delay}"
    uncached: List[str] = []
    redis_cli = getattr(client, 'redis_client', None)
    if redis_cli:
        for fid in ordered:
            try:
                cached_val = redis_cli.get(f"{cache_prefix}:{fid}")
                if cached_val is not None:
                    val = cached_val.decode() if isinstance(cached_val, bytes) else str(cached_val)
                    if val == "1":
                        known.append(fid)
                    elif val == "0":
                        unknown.append(fid)
                    else:
                        uncached.append(fid)
                else:
                    uncached.append(fid)
            except Exception:
                uncached.append(fid)
    else:
        uncached = list(ordered)

    if not uncached:
        return {
            "known": known,
            "unknown": unknown,
            "skipped": False,
            "warning": None,
            "lookup_errors": lookup_errors,
            "cache_hits": len(ordered) - len(uncached),
        }

    semaphore = asyncio.Semaphore(max_concurrency)
    start_time = time.time()

    async def _check_one(field_id: str) -> Tuple[str, Optional[str], Optional[str]]:
        """返回 (field_id, status, error_msg)。status: 'known'/'unknown'/'error'"""
        async with semaphore:
            # 检查总超时
            if time.time() - start_time > total_timeout:
                return (field_id, "error", f"total timeout {total_timeout}s exceeded")
            try:
                payload = await client.get_datafields(
                    instrument_type=instrument_type, region=region, delay=delay,
                    universe=universe, filter_sharpe=False, data_type="",
                    search=field_id,
                )
                if not isinstance(payload, dict) or "error" in payload or "results" not in payload:
                    return (field_id, "error", "incomplete lookup payload")
                if field_id in _ids_from_datafields_payload(payload):
                    # Cache the positive result
                    if redis_cli:
                        try:
                            redis_cli.setex(f"{cache_prefix}:{field_id}", cache_ttl, "1")
                        except Exception:
                            logging.getLogger(__name__).debug("swallowed exception", exc_info=True)
                    return (field_id, "known", None)
                else:
                    # Cache the negative result
                    if redis_cli:
                        try:
                            redis_cli.setex(f"{cache_prefix}:{field_id}", cache_ttl, "0")
                        except Exception:
                            logging.getLogger(__name__).debug("swallowed exception", exc_info=True)
                    return (field_id, "unknown", None)
            except Exception as exc:
                return (field_id, "error", str(exc))

    # 并发执行所有未缓存字段验证
    tasks = [_check_one(fid) for fid in uncached]
    results = await asyncio.gather(*tasks, return_exceptions=True)

    for result in results:
        if isinstance(result, Exception):
            lookup_errors.append(f"gather error: {result}")
            continue
        field_id, status, error_msg = result
        if status == "known":
            known.append(field_id)
        elif status == "unknown":
            unknown.append(field_id)
        else:
            lookup_errors.append(f"{field_id}: {error_msg}")

    skipped = bool(lookup_errors) and not unknown
    warning = None
    if lookup_errors:
        warning = "Field pre-check skipped or incomplete: " + "; ".join(lookup_errors)
        logger.warning(warning)
    return {
        "known": known,
        "unknown": unknown,
        "skipped": skipped,
        "warning": warning,
        "lookup_errors": lookup_errors,
        "cache_hits": len(ordered) - len(uncached),
    }

@mcp.tool()

async def validate_expressions(
    alpha_expressions: Sequence[str],
    region: str = "USA",
    universe: str = "TOP3000",
    delay: int = 1,
) -> Dict[str, Any]:
    """
    Validate field identifiers in alpha expressions before batch submission.

    Extracts field names from each expression, filters out operator keywords,
    and confirms each candidate via targeted datafield search (not an unscoped
    first-page dump). Catches the classic "unknown variable destroys the
    whole multisim batch" failure BEFORE submission (e.g. adv10/adv40 don't
    exist; ep_yield_pct_smest_fy1_3 is D1-only and not available at D0).

    Args:
        alpha_expressions: List of alpha expression strings
        region: Market region (default "USA")
        universe: Stock universe (default "TOP3000")
        delay: Data delay (default 1)
    Returns:
        valid / unknown_fields / fields_checked / platform_field_count
    """
    try:
        candidates = _extract_field_candidates(alpha_expressions)
        if not candidates:
            return {
                "valid": True,
                "expressions": len(alpha_expressions),
                "fields_checked": [],
                "unknown_fields": [],
                "note": "No field identifiers found (pure operator expressions).",
            }
        verified = await _verify_fields_exist(
            candidates, region=region, universe=universe, delay=delay)
        unknown = verified["unknown"]
        out = {
            "valid": not unknown,
            "region": region,
            "delay": delay,
            "universe": universe,
            "expressions": len(alpha_expressions),
            "fields_checked": candidates,
            "unknown_fields": unknown,
            "platform_field_count": len(verified["known"]),
        }
        if verified.get("warning"):
            out["warning"] = verified["warning"]
            if verified.get("skipped"):
                out["valid"] = True
                out["note"] = "Field lookup incomplete; not treating candidates as unknown."
        return out
    except Exception as e:
        return {"error": f"An unexpected error occurred: {str(e)}"}
