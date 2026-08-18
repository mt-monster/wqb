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

# --- Main entry point ---
