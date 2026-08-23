"""仿真工具 (单发/批量/子查询/错误诊断) — MCP 工具层 (2026-08-13 自 main.py 按域拆分)。"""
import json, os, re, sys, asyncio, time, logging
from typing import Dict, List, Optional, Any, Union, Sequence, Tuple
from datetime import datetime, timedelta
from time import sleep
from pathlib import Path

from mcp_core import (mcp, brain_client, logger, save_config, _slim_checks, _slim_alpha,
    _slim_alpha_response, _slim_alpha_list, _slim_multisim, _slim_datafields, _slim_datasets,
    _records_to_dicts, _slim_yearly, _slim_pnl, _slim_correlation_block, _slim_check_correlation,
    _slim_pyramids, _slim_text_lookup,     _ra_bad, _truncate, _unwrap_result, _rewrap, _is_error)

from brain_api import SimulationSettings, SimulationData

# 复用工作区 tools/lib 下的 vector_wrap（单一权威源，避免副本 drift）
_REPO_TOOLS_LIB = Path(__file__).resolve().parents[1] / "tools" / "lib"
if _REPO_TOOLS_LIB.is_dir() and str(_REPO_TOOLS_LIB) not in sys.path:
    sys.path.insert(0, str(_REPO_TOOLS_LIB))
try:
    from vector_wrap import wrap_naked_vectors
except Exception:  # pragma: no cover - 工作区布局异常时降级
    wrap_naked_vectors = None

@mcp.tool()

async def create_simulation(
    type: str = "REGULAR",
    region: str = "USA",
    universe: str = "TOP3000",
    delay: int = 1,
    decay: int = 4,
    neutralization: str = "SUBINDUSTRY",
    truncation: float = 0.08,
    test_period: str = "P0Y0M",
    language: str = "FASTEXPR",
    unit_handling: str = "VERIFY",
    nan_handling: str = "ON",
    lookback: Optional[int] = None,
    alpha_expression: Optional[str] = None,
    combo: Optional[str] = None,
    selection: Optional[str] = None,
    pasteurization: str = "ON",
    max_trade: str = "OFF",
    selection_handling: str = "POSITIVE",
    selection_limit: int = 1000,
    component_activation: str = "IS",
) -> Dict[str, Any]:
    """
    Create a new simulation on BRAIN platform.
    
    This tool creates and starts a simulation with your alpha code. Use this after you have your alpha formula ready.
    if field type=VECTOR should deal with vec_ suffer vec_*(FIELD)
    Args:
        type: Simulation type ("REGULAR" or "SUPER")
        region: Market region (e.g., "USA")
        universe: Universe of stocks (e.g., "TOP3000")
        delay: Data delay (0 or 1)
        decay: Decay value for the simulation
        neutralization: Neutralization method
        truncation: Truncation value
        test_period: Test period (e.g., "P0Y0M" for 1 year 6 months)
        language: Expression language ("FASTEXPR" or "PYTHON")
        unit_handling: Unit handling method. Used for FASTEXPR simulations.
        nan_handling: NaN handling method
        lookback: Historical lookback window. Only used for PYTHON simulations; defaults to 256 for PYTHON.
        alpha_expression: Alpha expression code (for REGULAR type)
        combo: Combo code (for SUPER type)
        selection: Selection code (for SUPER type). For USA SUPER simulations,
            this must include (prod_correlation > 0)
    
    Returns:
        Simulation creation result with ID and location
    """
    instrument_type = "EQUITY"
    visualization = False
    try:
        # 参数确认日志：防止 MCP 默认值覆盖调用方传入的 region/universe
        logger.info(f"[create_simulation] region={region}, universe={universe}, delay={delay}, "
                    f"neutralization={neutralization}, decay={decay}, truncation={truncation}")
        if region == "USA" and universe == "TOP3000":
            logger.warning("[create_simulation] 使用默认 USA/TOP3000！"
                           "如果期望其他区域，请检查 MCP 调用参数是否正确传递。")

        normalized_language = language.upper()
        settings_kwargs = {
            "instrumentType": instrument_type,
            "region": region,
            "universe": universe,
            "delay": delay,
            "decay": decay,
            "neutralization": neutralization,
            "truncation": truncation,
            "testPeriod": test_period,
            "language": normalized_language,
            "visualization": visualization,
            "pasteurization": pasteurization,
            "maxTrade": max_trade,
            "selectionHandling": selection_handling,
            "selectionLimit": selection_limit,
            "componentActivation": component_activation,
        }

        if normalized_language == "PYTHON":
            settings_kwargs["lookback"] = 256 if lookback is None else lookback
            settings_kwargs["unitHandling"] = None
            settings_kwargs["nanHandling"] = None
        else:
            settings_kwargs["unitHandling"] = unit_handling
            settings_kwargs["nanHandling"] = nan_handling

        settings = SimulationSettings(
            **settings_kwargs
        )
        
        sim_data = SimulationData(
            type=type,
            settings=settings,
            regular=alpha_expression,
            combo=combo,
            selection=selection
        )
        
        return _slim_alpha_response(await brain_client.create_simulation(sim_data))
    except Exception as e:
        extra_info = ""
        error_msg = str(e)
        if error_msg and "does not support event inputs" in error_msg:
            extra_info = "If fields is vector type  should use vec_* operator with event input"
            return {"error": f"An unexpected error occurred: {str(e)}. {extra_info}"}
        return {"error": f"An unexpected error occurred: {str(e)}"}

# --- Alpha and Data Retrieval Tools ---

@mcp.tool()

async def create_multi_simulation(
    alpha_expressions: List[str],
    instrument_type: str = "EQUITY",
    region: str = "USA",
    universe: str = "TOP3000",
    delay: int = 1,
    decay: int = 4,
    neutralization: str = "INDUSTRY",
    truncation: float = 0.0,
    test_period: str = "P0Y0M",
    unit_handling: str = "VERIFY",
    nan_handling: str = "OFF",
    language: str = "FASTEXPR",
    lookback: Optional[int] = None,
    visualization: bool = False,
    pasteurization: str = "ON",
    max_trade: str = "OFF",
    wait_for_completion: bool = False,
    validate_fields: bool = False
) -> Dict[str, Any]:
    """
    🚀 Create multiple regular alpha simulations on BRAIN platform in a single request.
    
    This tool creates a multisimulation with multiple regular alpha expressions.
    By default (wait_for_completion=False) it submits and immediately returns the
    simulation locations so the caller can poll with lookINTO_SimError_message.
    If wait_for_completion=True it blocks until all simulations complete (can take 8+ minutes,
    which may exceed the MCP client request timeout — prefer the default async mode).
    
    Call get_platform_setting_options to get the valid options for the simulation.
    Args:
        alpha_expressions: List of alpha expressions/code strings (2-10 expressions required)
        instrument_type: Type of instruments (default: "EQUITY")
        region: Market region (default: "USA")
        universe: Universe of stocks (default: "TOP3000")
        delay: Data delay (default: 1)
        decay: Decay value (default: 4)
        neutralization: Neutralization method (default: "NONE")
        truncation: Truncation value (default: 0.0)
        test_period: Test period (default: "P0Y0M")
        unit_handling: Unit handling method. Used for FASTEXPR simulations.
        nan_handling: NaN handling method. Used for FASTEXPR simulations.
        language: Expression language ("FASTEXPR" or "PYTHON")
        lookback: Historical lookback window. Only used for PYTHON simulations; defaults to 256 for PYTHON.
        visualization: Enable visualization (default: False)
        pasteurization: Pasteurization setting (default: "ON")
        max_trade: Max trade setting (default: "OFF")
        wait_for_completion: If False (default), submit and immediately return simulation
            locations for polling. If True, block until all simulations finish (may timeout
            at the MCP client level for 8+ minute simulations).
        validate_fields: If True, confirm extracted field ids via targeted
            datafield search before submit. Default False — local lint (validator.check_batch)
            already covers structural checks; field existence is verified on-demand
            via the standalone validate_expressions tool.
    
    Returns:
        Dictionary containing multisimulation location and (if wait_for_completion)
        detailed results for each alpha.
    """
    try:
        # 参数确认日志：防止 MCP 默认值覆盖调用方传入的 region/universe
        logger.info(f"[create_multi_simulation] region={region}, universe={universe}, delay={delay}, "
                    f"neutralization={neutralization}, decay={decay}, truncation={truncation}, "
                    f"expressions={len(alpha_expressions)}")
        if region == "USA" and universe == "TOP3000":
            logger.warning("[create_multi_simulation] 使用默认 USA/TOP3000！"
                           "如果期望其他区域，请检查 MCP 调用参数是否正确传递。")

        # Validate input
        if len(alpha_expressions) < 2:
            return {"error": "At least 2 alpha expressions are required"}
        if len(alpha_expressions) > 10:
            return {"error": "Maximum 10 alpha expressions allowed per request"}

        await brain_client.ensure_authenticated()

        # Field whitelist pre-check (2026-08-13): one unknown variable cancels
        # the ENTIRE multisim batch. Confirm each candidate via targeted
        # datafield search (not an unscoped/paginated dump). Lookup errors
        # warn and continue rather than blocking submission.
        if validate_fields and language.upper() != "PYTHON":
            from tools_data import _extract_field_candidates, _verify_fields_exist
            candidates = _extract_field_candidates(alpha_expressions)
            if candidates:
                try:
                    verified = await _verify_fields_exist(
                        candidates,
                        instrument_type=instrument_type,
                        region=region,
                        universe=universe,
                        delay=delay,
                        client=brain_client,
                    )
                    if verified.get("warning"):
                        logger.warning(verified["warning"])
                    if verified.get("unknown") and not verified.get("skipped"):
                        return {
                            "error": "Field validation failed — unknown variable(s) detected. "
                                     "One unknown field cancels the whole multisim batch.",
                            "unknown_fields": verified["unknown"],
                            "fields_checked": candidates,
                            "hint": "Re-check field ids via get_datafields, or re-run with validate_fields=False.",
                        }
                except Exception as exc:
                    logger.warning(f"Field pre-check skipped: {exc}")

        normalized_language = language.upper()
        
        # Create multisimulation data
        multisimulation_data = []
        for alpha_expr in alpha_expressions:
            settings = {
                'instrumentType': instrument_type,
                'region': region,
                'universe': universe,
                'delay': delay,
                'decay': decay,
                'neutralization': neutralization,
                'truncation': truncation,
                'pasteurization': pasteurization,
                'language': normalized_language,
                'visualization': visualization,
                'testPeriod': test_period,
                'maxTrade': max_trade
            }

            if normalized_language == "PYTHON":
                settings['lookback'] = 256 if lookback is None else lookback
            else:
                settings['unitHandling'] = unit_handling
                settings['nanHandling'] = nan_handling

            simulation_item = {
                'type': 'REGULAR',
                'settings': settings,
                'regular': alpha_expr
            }
            multisimulation_data.append(simulation_item)
        
        # Send multisimulation request
        response = await brain_client._request('POST', f"{brain_client.base_url}/simulations", json=multisimulation_data)
        
        if response.status_code != 201:
            return {
                "error": f"Failed to create multisimulation. Status: {response.status_code}",
                "details": response.text,
            }
        
        # Get multisimulation location
        location = response.headers.get('Location', '')
        if not location:
            return {"error": "No location header in multisimulation response"}
        
        # Async mode (default): submit and immediately return locations for polling.
        if not wait_for_completion:
            print(f"Multisimulation submitted (async mode): {location}", file=sys.stderr)
            return {
                'success': True,
                'message': f'Multisimulation submitted successfully with {len(alpha_expressions)} alpha expressions',
                'async': True,
                'multisimulation_id': location.split('/')[-1],
                'multisimulation_location': location,
                'multisimulation_url': brain_client._to_absolute_url(location),
                'submitted_expressions': alpha_expressions,
                'polling_tool': 'lookINTO_SimError_message',
                'note': 'Simulations are processing. Poll the multisimulation children (GET /simulations/{id}) or use lookINTO_SimError_message once children are available.'
            }
        
        # Wait for children to appear and get results
        return _slim_multisim(await _wait_for_multisimulation_completion(location, len(alpha_expressions)))
        
    except Exception as e:
        return {"error": f"Error creating multisimulation: {str(e)}"}

@mcp.tool()

async def batch_create_simulations(
    items: List[Dict[str, Any]],
    base_region: Optional[str] = None,
    base_universe: Optional[str] = None,
    base_delay: int = 1,
    base_decay: int = 4,
    base_neutralization: str = "STATISTICAL",
    base_truncation: float = 0.08,
    language: str = "FASTEXPR",
    unit_handling: str = "VERIFY",
    nan_handling: str = "OFF",
    pasteurization: str = "ON",
    max_trade: str = "OFF",
) -> Dict[str, Any]:
    """🎯 一次调用提交 N 个“各自独立设置”的仿真（异步，立即返回全部 location）。

    填补 create_multi_simulation 的盲区：multisim 整批共享同一套设置，做不了
    “同一表达式×N 套设置”的参数矩阵（Mode A）或 per-item settings 批。
    本工具服务端内逐条顺序提交（带 429 退避与限流缓冲），不阻塞等待仿真完成，
    避免并行 MCP 单仿真调用挤爆 stdio 通道（2026-08-23 八连超时实证）。
    提交后用 lookINTO_SimError_message 轮询返回的 locations。

    Args:
        items: 1-20 条，每条 {"expression": "...", "settings": {...}?, "tag": "..."?}；
            settings 缺省键用 base_* 填充；支持的键：region / universe / delay /
            decay / neutralization / truncation（平台 camelCase 键亦接受）
        base_region: 默认区域（item 未给 region 时用）
        base_universe: 默认 universe
        base_delay / base_decay / base_neutralization / base_truncation: 默认设置
        language / unit_handling / nan_handling / pasteurization / max_trade: 固定设置段
    Returns:
        {submitted, total, results: [{index, tag, ok, simulation_id, location} | 错误], note}
    """
    try:
        if not isinstance(items, list) or not (1 <= len(items) <= 20):
            return {"error": "items 需为 1-20 条的列表"}
        if not base_region:
            return {"error": "base_region 必填（防 MCP 默认值误用：不设 USA/TOP3000 默认）"}

        base = {
            'instrumentType': 'EQUITY',
            'region': base_region,
            'universe': base_universe,
            'delay': base_delay,
            'decay': base_decay,
            'neutralization': base_neutralization,
            'truncation': base_truncation,
            'pasteurization': pasteurization,
            'language': language.upper(),
            'visualization': False,
            'testPeriod': 'P0Y0M',
            'maxTrade': max_trade,
        }
        if language.upper() != "PYTHON":
            base['unitHandling'] = unit_handling
            base['nanHandling'] = nan_handling

        payloads = []
        tags = []
        for it in items:
            expr = it.get('expression') or it.get('expr') or it.get('regular')
            if not expr:
                return {"error": f"items[{len(payloads)}] 缺 expression 字段"}
            settings = dict(base)
            for k, v in (it.get('settings') or {}).items():
                settings[k] = v
            payloads.append({'type': 'REGULAR', 'settings': settings, 'regular': expr})
            tags.append(it.get('tag'))

        logger.info(f"[batch_create_simulations] n={len(payloads)} base_region={base_region} "
                    f"base_universe={base_universe}")
        res = await brain_client.batch_create_simulations(payloads)
        for r, tag in zip(res.get("results", []), tags):
            if tag:
                r["tag"] = tag
        res['async'] = True
        res['polling_tool'] = 'lookINTO_SimError_message'
        return res
    except Exception as e:
        return {"error": f"Error in batch_create_simulations: {str(e)}"}

@mcp.tool()

async def get_multisimulation_children(multisimulation_location: str) -> Dict[str, Any]:
    """Get the child simulation locations/status of a submitted multisimulation.

    Use this after create_multi_simulation (async mode) to discover the individual
    simulation URLs, then poll each child with lookINTO_SimError_message until done.

    Args:
        multisimulation_location: The multisimulation location returned by
            create_multi_simulation (e.g. "/simulations/{id}" or full URL).
    Returns:
        Dict with children list, count, and per-child status/alpha when available.
    """
    try:
        await brain_client.ensure_authenticated()
        resp = await brain_client._request('GET', multisimulation_location)
        if resp.status_code != 200:
            return {"error": f"HTTP {resp.status_code}", "raw": brain_client._response_payload(resp)}
        data = resp.json() if resp.text else {}
        children = data.get('children', [])
        out_children = []
        for c in children:
            child_url = c if c.startswith('http') else f"{brain_client.base_url}/simulations/{c}"
            out_children.append({"location": c, "location_url": child_url})
        return {
            "success": True,
            "multisimulation_id": multisimulation_location.split('/')[-1],
            "child_count": len(out_children),
            "children": out_children,
            "note": "Poll each child location with lookINTO_SimError_message until status shows the alpha id."
        }
    except Exception as e:
        return {"error": f"Error getting multisimulation children: {str(e)}"}

async def _poll_single_child(child_url: str, child_index: int) -> Dict[str, Any]:
    """Poll a single child simulation until completion, then fetch alpha details.

    Uses Retry-After header for intelligent backoff. Returns a result dict.
    """
    max_alpha_attempts = 100
    alpha_attempt = 0
    alpha_data = None

    while alpha_attempt < max_alpha_attempts:
        alpha_attempt += 1
        try:
            alpha_progress = await brain_client._request('GET', child_url)
            if alpha_progress.status_code == 200:
                alpha_data = alpha_progress.json()
                retry_after = alpha_progress.headers.get("Retry-After")
                if retry_after is not None:
                    retry_after_val = float(retry_after)
                else:
                    retry_after_val = 0.0

                if retry_after_val <= 0:
                    # Simulation complete
                    break
                else:
                    await asyncio.sleep(retry_after_val)
            else:
                await asyncio.sleep(5)
        except Exception as e:
            await asyncio.sleep(5)

    if alpha_data is None:
        return {
            'location': child_url,
            'error': f'Alpha simulation did not complete within {max_alpha_attempts} attempts'
        }

    # Get alpha details from the completed simulation
    alpha_id = alpha_data.get("alpha")
    if not alpha_id:
        return {
            'location': child_url,
            'error': 'No alpha ID found in completed simulation'
        }

    try:
        alpha_details = await brain_client._request(
            'GET', f"{brain_client.base_url}/alphas/{alpha_id}"
        )
        if alpha_details.status_code == 200:
            return {
                'alpha_id': alpha_id,
                'location': child_url,
                'details': alpha_details.json()
            }
        else:
            return {
                'alpha_id': alpha_id,
                'location': child_url,
                'error': f'Failed to get alpha details: {alpha_details.status_code}'
            }
    except Exception as e:
        return {
            'alpha_id': alpha_id,
            'location': child_url,
            'error': f'Error fetching alpha details: {str(e)}'
        }


async def _wait_for_multisimulation_completion(location: str, expected_children: int) -> Dict[str, Any]:
    try:
        print(f"Waiting for multisimulation to complete... (this may take several minutes)", file=sys.stderr)
        print(f"Expected {expected_children} alpha simulations", file=sys.stderr)
        print("", file=sys.stderr)

        # Phase 1: Wait for children to appear
        children = []
        max_wait_attempts = 200
        wait_attempt = 0

        while wait_attempt < max_wait_attempts and len(children) == 0:
            wait_attempt += 1
            try:
                multisim_response = await brain_client._request('GET', location)
                if multisim_response.status_code == 200:
                    multisim_data = multisim_response.json()
                    children = multisim_data.get('children', [])
                    if children:
                        break
                    else:
                        retry_after = multisim_response.headers.get("Retry-After")
                        wait_time = float(retry_after) if retry_after else 5.0
                        await asyncio.sleep(wait_time)
            except Exception as e:
                await asyncio.sleep(5)

        if not children:
            return {"error": f"Children did not appear within {max_wait_attempts} attempts (multisimulation may still be processing)"}

        # Phase 2: Poll ALL children in parallel using asyncio.gather
        print(f"Children appeared ({len(children)}), polling all in parallel...", file=sys.stderr)

        child_urls = []
        for c in children:
            url = c if c.startswith('http') else f"{brain_client.base_url}/simulations/{c}"
            child_urls.append(url)

        # Launch all child polls concurrently
        tasks = [
            _poll_single_child(url, i)
            for i, url in enumerate(child_urls)
        ]
        alpha_results = await asyncio.gather(*tasks, return_exceptions=True)

        # Normalize results: convert exceptions to error dicts
        normalized_results = []
        for i, result in enumerate(alpha_results):
            if isinstance(result, Exception):
                normalized_results.append({
                    'location': child_urls[i] if i < len(child_urls) else f"child_{i+1}",
                    'error': str(result)
                })
            else:
                normalized_results.append(result)

        print(f"Multisimulation completed! Retrieved {len(normalized_results)} alpha results", file=sys.stderr)
        return {
            'success': True,
            'message': f'Successfully created {expected_children} regular alpha simulations',
            'total_requested': expected_children,
            'total_created': len(normalized_results),
            'multisimulation_id': location.split('/')[-1],
            'multisimulation_location': location,
            'alpha_results': normalized_results
        }

    except Exception as e:
        return {"error": f"Error waiting for multisimulation completion: {str(e)}"}

# --- Payment and Financial Tools ---

from typing import Sequence

@mcp.tool()

async def lookINTO_SimError_message(locations: Sequence[str]) -> dict:
    """
    Fetch and parse error/status from multiple simulation locations (URLs).
    Args:
        locations: List of simulation result URLs (e.g., /simulations/{id})
    Returns:
        List of dicts with location, error message, and raw response
    """
    results = []
    for loc in locations:
        try:
            resp = await brain_client._request('GET', loc)
            if resp.status_code != 200:
                results.append({
                    "location": loc,
                    "location_url": brain_client._to_absolute_url(loc),
                    "error": f"HTTP {resp.status_code}",
                    "status_code": resp.status_code,
                    "raw": brain_client._response_payload(resp)
                })
                continue
            data = resp.json() if resp.text else {}
            error_msg = brain_client._simulation_error_message(data)
            # If alpha ID is missing, include that info
            if not data.get("alpha") and error_msg == "Unknown error":
                error_msg = "Simulation did not get through; inspect raw/status for the platform response."
            extra_info = ""
            if error_msg and "does not support event inputs" in error_msg:
                extra_info = "Operator xxx does not support event inputs : If fields is vector type  should use vec_* operator with event input"
            results.append({
                "location": loc,
                "location_url": brain_client._to_absolute_url(loc),
                "error": error_msg,
                "status": data.get("status"),
                "alpha": data.get("alpha"),
                "raw": data,
                "extra_info": extra_info
            })
        except Exception as e:
            results.append({
                "location": loc,
                "error": str(e),
                "raw": None
            })
    return _slim_text_lookup({"results": results}, n=2000)


@mcp.tool()
async def fix_vector_fields(
    alpha_expressions: List[str],
    region: str,
    dataset_id: str,
    universe: str,
    delay: int = 1,
    agg: Optional[str] = None,
) -> Dict[str, Any]:
    """本地预检并自动修复：把表达式中裸用的 VECTOR(event) 字段裹上 vec_* 聚合。

    平台规则：VECTOR 类型字段必须先经 vec_* 聚合成标量(MATRIX)，才能被
    ts_*/divide/subtract/add/rank 等常规算子使用，否则提交后平台报
    "does not support event inputs"（HTTP 400），浪费一次回测。

    本工具在 create_simulation / create_multi_simulation 之前调用：
    按 dataset_id 拉取字段类型，找出 type==VECTOR 的字段，把表达式中
    未被 vec_* 包裹的出现位置自动裹上聚合算子（幂等，已裹的不动）。

    Args:
        alpha_expressions: 待检测/修复的表达式列表
        region: 市场区域（如 "USA"、"EUR"、"ASI"）
        dataset_id: 数据集 ID（用于拉取字段类型）
        universe: 股票池（与回测一致）
        delay: 数据延迟（0 或 1）
        agg: 强制指定聚合算子（如 "vec_sum"）；None 则按字段语义自动选
             （count/sum/num/vol 等 -> vec_sum，其余 -> vec_avg）

    Returns:
        {"results": [{"original", "fixed", "wrapped_fields", "changed"}],
         "vector_fields": [...], "any_changed": bool}
        调用方应用 fixed 替换原表达式后再提交回测。
    """
    if wrap_naked_vectors is None:
        return {"error": "vector_wrap 模块不可用（tools/lib 未找到），无法本地修复"}
    try:
        await brain_client.ensure_authenticated()
        resp = await brain_client.get_datafields(
            "EQUITY", region, delay, universe, "false", dataset_id, "VECTOR", None, False)
        fields = resp.get("results") if isinstance(resp, dict) else resp
        if not isinstance(fields, list):
            fields = (resp or {}).get("fields", []) if isinstance(resp, dict) else []
        vector_fields = [f.get("id") for f in fields
                         if isinstance(f, dict) and str(f.get("type", "")).upper() == "VECTOR" and f.get("id")]
        if not vector_fields:
            return {"results": [{"original": e, "fixed": e, "wrapped_fields": [], "changed": False}
                                for e in alpha_expressions],
                    "vector_fields": [], "any_changed": False,
                    "note": "数据集无 VECTOR 字段或拉取为空，未做改动"}
        results, any_changed = [], False
        for e in alpha_expressions:
            fixed, wrapped = wrap_naked_vectors(e, vector_fields, agg=agg)
            changed = bool(wrapped)
            any_changed = any_changed or changed
            results.append({"original": e, "fixed": fixed,
                            "wrapped_fields": wrapped, "changed": changed})
        return {"results": results, "vector_fields": sorted(vector_fields),
                "any_changed": any_changed}
    except Exception as e:
        return {"error": f"fix_vector_fields 失败: {str(e)}"}


# --- Main entry point ---
