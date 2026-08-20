from __future__ import annotations
import json
import time
import asyncio
import logging
from typing import Dict, List, Optional, Any, Union
import re
import base64
from bs4 import BeautifulSoup
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
import os
import sys
from pathlib import Path
from time import sleep
from urllib.parse import urljoin
import redis
import hashlib
import math
import uuid
import random

import requests
import pandas as pd
import zlib
import msgpack
from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field, EmailStr, model_validator
from brain_api_models import AuthCredentials, SimulationData, SimulationSettings
from brain_config import load_config, _resolve_config_path, _load_dotenv_into_environ
logger = logging.getLogger("brain_api")


class SimulationMixin:
    async def create_simulation(self, simulation_data: SimulationData) -> Dict[str, str]:
        """Create a new simulation on BRAIN platform."""
        await self._create_simulation_semaphore.acquire()
        try:
            await self.ensure_authenticated()
        
            self.log("🚀 Creating simulation...", "INFO")
            
            # Prepare settings based on simulation type
            settings_dict = simulation_data.settings.model_dump()
            
            # Remove fields based on simulation type
            if simulation_data.type == "REGULAR":
                # Remove SUPER-specific fields for REGULAR
                settings_dict.pop('selectionHandling', None)
                settings_dict.pop('selectionLimit', None)
                settings_dict.pop('componentActivation', None)
            
            # Filter out None values from settings
            settings_dict = {k: v for k, v in settings_dict.items() if v is not None}
            
            # Prepare simulation payload
            payload = {
                'type': simulation_data.type,
                'settings': settings_dict
            }
            
            # Add type-specific fields
            if simulation_data.type == "REGULAR":
                if simulation_data.regular:
                    payload['regular'] = simulation_data.regular
            elif simulation_data.type == "SUPER":
                if simulation_data.combo:
                    payload['combo'] = simulation_data.combo
                if simulation_data.selection:
                    payload['selection'] = simulation_data.selection
            
            # Filter out None values from entire payload
            payload = {k: v for k, v in payload.items() if v is not None}
            
            response = await self._request('POST', f"{self.base_url}/simulations", json=payload)
            if response.status_code >= 400:
                return {
                    "error": "Failed to create simulation",
                    "status_code": response.status_code,
                    "response": self._response_payload(response),
                    "request": {
                        "type": simulation_data.type,
                        "settings": settings_dict,
                        "has_regular": bool(simulation_data.regular),
                        "has_combo": bool(simulation_data.combo),
                        "has_selection": bool(simulation_data.selection),
                    },
                }
            
            location = response.headers.get('Location', '')
            location_url = self._to_absolute_url(location)
            simulation_id = location_url.split('/')[-1] if location_url else None
            
            self.log(f"Simulation created with ID: {simulation_id}", "SUCCESS")

            start_time = time.time()
            timeout_seconds = 1800  # 10 minutes
            max_poll_retries = 5  # Max retries for transient connection errors during polling
            poll_retry_delay = 3  # Initial delay between poll retries

            simulation_progress = None
            while True:
                # Check for timeout
                if time.time() - start_time > timeout_seconds:
                    raise TimeoutError(f"Simulation {simulation_id} timed out after {timeout_seconds} seconds")

                # Poll with retry logic for transient network errors
                poll_error = None
                for poll_attempt in range(max_poll_retries):
                    try:
                        simulation_progress = await self._request('GET', location_url)
                        poll_error = None
                        break  # Success, exit retry loop
                    except (ConnectionError, TimeoutError) as e:
                        poll_error = e
                        if poll_attempt < max_poll_retries - 1:
                            retry_wait = poll_retry_delay * (1.5 ** poll_attempt)
                            self.log(f"⚠️ Polling connection error for {simulation_id} (attempt {poll_attempt + 1}/{max_poll_retries}), retrying in {retry_wait:.1f}s: {str(e)}", "WARNING")
                            await asyncio.sleep(retry_wait)
                        else:
                            self.log(f"❌ Polling failed after {max_poll_retries} attempts for {simulation_id}: {str(e)}", "ERROR")
                
                if poll_error:
                    raise poll_error
                
                # Check if we need to wait
                retry_after = simulation_progress.headers.get("Retry-After")
                
                if not retry_after or float(retry_after) == 0:
                    break
                
                wait_time = float(retry_after)
                # Use asyncio.sleep instead of time.sleep to avoid blocking
                await asyncio.sleep(wait_time)

            self.log("Alpha done simulating, getting alpha details", "INFO")
            
            progress_data = simulation_progress.json()
            if not progress_data.get("alpha"):
                return {
                    "error": "Simulation failed or returned no alpha ID",
                    "message": self._simulation_error_message(progress_data),
                    "simulation_id": simulation_id,
                    "location": location,
                    "location_url": location_url,
                    "status": progress_data.get("status"),
                    "progress": progress_data,
                    "request": {
                        "type": simulation_data.type,
                        "settings": settings_dict,
                        "has_regular": bool(simulation_data.regular),
                        "has_combo": bool(simulation_data.combo),
                        "has_selection": bool(simulation_data.selection),
                    },
                }
                
            alpha_id = progress_data["alpha"]
            
            # Fetch alpha details with retry logic
            alpha_response = None
            for alpha_attempt in range(max_poll_retries):
                try:
                    alpha_response = await self._request('GET', f"https://api.worldquantbrain.com/alphas/{alpha_id}")
                    break
                except (ConnectionError, TimeoutError) as e:
                    if alpha_attempt < max_poll_retries - 1:
                        retry_wait = poll_retry_delay * (1.5 ** alpha_attempt)
                        self.log(f"⚠️ Failed to fetch alpha details (attempt {alpha_attempt + 1}/{max_poll_retries}), retrying in {retry_wait:.1f}s: {str(e)}", "WARNING")
                        await asyncio.sleep(retry_wait)
                    else:
                        self.log(f"❌ Failed to fetch alpha details after {max_poll_retries} attempts: {str(e)}", "ERROR")
                        raise
            
            return alpha_response.json()
            
        except Exception as e:
            self.log(f"❌ Failed to create simulation: {str(e)}", "ERROR")
            raise
        finally:
            self._create_simulation_semaphore.release()

    async def get_alpha_details(self, alpha_id: str) -> Dict[str, Any]:
        """Get detailed information about an alpha."""
        await self.ensure_authenticated()
        
        try:
            response = await self._request('GET', f"{self.base_url}/alphas/{alpha_id}")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            self.log(f"Failed to get alpha details: {str(e)}", "ERROR")
            raise

    async def get_datasets(self, category: Optional[str] = None, region: str = "USA",
                          delay: int = 1, universe: str = "TOP3000", theme: str = "false", search: Optional[str] = None) -> Dict[str, Any]:
        """Get available datasets with Redis caching (1 day TTL) and fetch all data at once."""
        await self.ensure_authenticated()
        
        try:
            # Generate cache key from parameters (excluding search for cache key)
            cache_params = {
                'category': category,
                'region': region,
                'delay': delay,
                'universe': universe,
                'theme': theme
            }
            cache_key = self._generate_cache_key('datasets', cache_params)
            
            # Try to get from cache
            cached_data = self._get_cached_data(cache_key)
            if cached_data:
                # Apply search filter if needed
                if search:
                    filtered_results = [
                        item for item in cached_data.get('results', [])
                        if search.lower() in json.dumps(item).lower()
                    ]
                    return {
                        **cached_data,
                        'results': filtered_results,
                        'count': len(filtered_results),
                        'from_cache': True
                    }
                return {**cached_data, 'from_cache': True}
            
            # Fetch all data from API (pagination loop)
            all_results = []
            offset = 0
            limit = 50
            total_count = None
            
            while True:
                params = {
                    'category': category,
                    'region': region,
                    'delay': delay,
                    'universe': universe,
                    'theme': theme,
                    'limit': limit,
                    'offset': offset
                }
                
                data = await self._request_json_with_retries(
                    'GET',
                    f"{self.base_url}/data-sets",
                    params=params,
                    op_name=f"get_datasets(offset={offset})",
                )
                
                results = data.get('results', [])
                all_results.extend(results)
                
                if total_count is None:
                    total_count = data.get('count', 0)
                
                # Break if we've fetched all data
                if len(results) < limit or len(all_results) >= total_count:
                    break
                
                offset += limit
            
            # Prepare complete response
            complete_data = {
                'results': all_results,
                'count': len(all_results),
                'extraNote': "if your returned result is 0, you may want to check your parameter by using get_platform_setting_options tool to got correct parameter",
                'from_cache': False
            }
            
            # Cache the complete data (1 week TTL)
            self._set_cached_data(cache_key, complete_data, ttl=604800)
            
            # Apply search filter if needed
            if search:
                filtered_results = [
                    item for item in all_results
                    if search.lower() in json.dumps(item).lower()
                ]
                complete_data['results'] = filtered_results
                complete_data['count'] = len(filtered_results)
            
            return complete_data
            
        except Exception as e:
            self.log(f"Failed to get datasets: {str(e)}", "ERROR")
            raise

    async def get_datafields(self, instrument_type: str = "EQUITY", region: str = "USA",
                            delay: int = 1, universe: str = "TOP3000", theme: str = "false",
                            dataset_id: Optional[str] = None, data_type: str = "",
                            search: Optional[str] = None,
                            filter_sharpe: bool = True) -> Dict[str, Any]:
        """Get available data fields with Redis caching (1 day TTL) and fetch all data at once.
        
        Search supports fuzzy matching across multiple fields:
        - Searches in: name, description, dataset.name, dataset.vendor, id
        - Multiple keywords (space-separated) use AND logic
        - Case-insensitive matching
        
        OS/IS Sharpe filtering (filter_sharpe=True by default):
        - Filters out datafields whose OS/IS Sharpe ratio < 0 to improve field quality
        - Uses pre-aggregated statistics from WebDataScope info_data.bin
        - Matching is done at datafield level first, then dataset level as fallback
        
        Examples:
        - search="price" -> matches any field containing "price"
        - search="stock volume" -> matches fields containing both "stock" AND "volume"
        """
        await self.ensure_authenticated()

        # Targeted search must hit the platform (dataset-specific ids are often
        # absent from an unscoped/paginated dump or its cache). Skip the
        # full-dump Redis lock and unscoped cache for these lookups.
        targeted_search = bool(search and str(search).strip())
        search_term = str(search).strip() if targeted_search else None
        
        # Redis-based distributed lock for concurrency control (limit to 1)
        lock_key = "lock:get_datafields"
        lock_acquired = False
        lock_timeout = 300  # Lock expires after 5 minutes to prevent deadlock
        max_wait_time = 600  # Maximum wait time for acquiring lock (10 minutes)
        wait_interval = 2  # Check every 2 seconds
        
        if self.redis_client and not targeted_search:
            start_wait = time.time()
            while time.time() - start_wait < max_wait_time:
                try:
                    # Try to acquire lock with NX (only set if not exists) and EX (expiration)
                    lock_acquired = self.redis_client.set(lock_key, "locked", ex=lock_timeout, nx=True)
                    if lock_acquired:
                        self.log(f"Acquired Redis lock for get_datafields", "INFO")
                        break
                    else:
                        # Lock is held by another process, wait and retry
                        ttl = self.redis_client.ttl(lock_key)
                        self.log(f"Waiting for get_datafields lock (TTL: {ttl}s)...", "INFO")
                        await asyncio.sleep(wait_interval)
                except Exception as e:
                    self.log(f"Redis lock acquisition failed: {str(e)}, proceeding without lock", "WARNING")
                    break
            
            if not lock_acquired and self.redis_client:
                self.log(f"Could not acquire get_datafields lock after {max_wait_time}s, proceeding anyway", "WARNING")
        
        try:
            def fuzzy_search_filter(item: Dict[str, Any], search_term: str) -> bool:
                """Enhanced fuzzy search across key fields with multi-keyword support."""
                if not search_term:
                    return True
                
                # Split search term into keywords (space-separated) for AND logic
                keywords = [kw.strip().lower() for kw in search_term.split() if kw.strip()]
                if not keywords:
                    return True
                
                # Extract searchable fields
                searchable_text_parts = []
                
                # Add field name
                if item.get('name'):
                    searchable_text_parts.append(str(item['name']))
                
                # Add field description
                if item.get('description'):
                    searchable_text_parts.append(str(item['description']))
                
                # Add field ID
                if item.get('id'):
                    searchable_text_parts.append(str(item['id']))
                
                # Add dataset information
                dataset = item.get('dataset', {})
                if isinstance(dataset, dict):
                    if dataset.get('name'):
                        searchable_text_parts.append(str(dataset['name']))
                    if dataset.get('vendor'):
                        searchable_text_parts.append(str(dataset['vendor']))
                    if dataset.get('id'):
                        searchable_text_parts.append(str(dataset['id']))
                
                # Combine all searchable text
                combined_text = ' '.join(searchable_text_parts).lower()
                
                # Check if ALL keywords match (AND logic)
                return all(keyword in combined_text for keyword in keywords)
            
            # Generate cache key from parameters (excluding search for cache key)
            cache_params = {
                'instrumentType': instrument_type,
                'region': region,
                'delay': delay,
                'universe': universe,
                'theme': theme,
                'dataset_id': dataset_id,
                'data_type': data_type
            }
            cache_key = self._generate_cache_key('datafields', cache_params)
            
            def sharpe_filter(items: list, rgn: str, dly: int) -> tuple:
                """Filter out datafields with OS/IS sharpe < 0. Returns (filtered_items, removed_count, applied)."""
                if not self._isos_data:
                    return items, 0, False
                region_key = f"{rgn}_{dly}"
                isos_info = self._isos_data.get(region_key, {})
                isos_section = isos_info.get('isos', {})
                datafield_sharpe = isos_section.get('datafield', {})
                dataset_sharpe_map = isos_section.get('dataset', {})
                if not datafield_sharpe and not dataset_sharpe_map:
                    return items, 0, False
                filtered = []
                for item in items:
                    field_name = item.get('id', '') or item.get('name', '')
                    dataset_info = item.get('dataset', {})
                    ds_id = dataset_info.get('id', '') if isinstance(dataset_info, dict) else ''
                    df_stats = datafield_sharpe.get(field_name)
                    if df_stats is not None:
                        sr = df_stats.get('sharpe_ratio')
                        if sr is not None and sr < 0:
                            continue
                    if df_stats is None and ds_id:
                        ds_stats = dataset_sharpe_map.get(ds_id)
                        if ds_stats is not None:
                            sr = ds_stats.get('sharpe_ratio')
                            if sr is not None and sr < 0:
                                continue
                    filtered.append(item)
                return filtered, len(items) - len(filtered), True

            # Try to get from cache (never for targeted search — dump may be truncated)
            cached_data = None if targeted_search else self._get_cached_data(cache_key)
            if cached_data:
                result = {**cached_data, 'from_cache': True}
                results = result.get('results', [])
                # Apply OS/IS Sharpe filtering
                if filter_sharpe:
                    results, removed, applied = sharpe_filter(results, region, delay)
                    result['sharpe_filter_applied'] = applied
                    result['sharpe_filter_removed'] = removed
                result['results'] = results
                result['count'] = len(results)
                return result
            
            # Fetch all data from API (pagination loop)
            all_results = []
            offset = 0
            # The platform's /data-fields endpoint caps page size at limit=50
            # for ALL queries (verified 2026-08-17: limit=100 returns HTTP 400
            # "Invalid query: pagination limit too high", regardless of offset
            # or search). A larger page size is NOT permitted, so use limit=50
            # uniformly and stop gracefully on client errors, returning
            # whatever pages were already fetched instead of failing the
            # whole call.
            limit = 50
            # Cap unscoped dumps: a full listing (1500+ fields) is useless as
            # a catalog to the model and blows up the MCP response size/time.
            # Stop early and tell the caller to narrow with search /
            # dataset_id / data_type instead.
            max_fields = 300
            total_count = None
            truncated = False
            capped = False
            
            while True:
                params = {
                    'instrumentType': instrument_type,
                    'region': region,
                    'delay': delay,
                    'universe': universe,
                    'limit': limit,
                    'offset': offset
                }
                
                if data_type != 'ALL' and data_type:
                    params['type'] = data_type
                
                if dataset_id:
                    params['dataset.id'] = dataset_id

                if targeted_search:
                    params['search'] = search_term
                
                try:
                    data = await self._request_json_with_retries(
                        'GET',
                        f"{self.base_url}/data-fields",
                        params=params,
                        op_name=f"get_datafields(offset={offset})",
                    )
                except requests.HTTPError as e:
                    status = getattr(getattr(e, 'response', None), 'status_code', None)
                    if status is not None and 400 <= status < 500 and all_results:
                        # Server rejected a deeper page (e.g. search + deep offset).
                        # Keep the pages already fetched instead of failing the whole call.
                        self.log(
                            f"get_datafields: pagination stopped at offset={offset} "
                            f"(HTTP {status}), returning {len(all_results)} partial results",
                            "WARNING",
                        )
                        truncated = True
                        break
                    raise
                
                results = data.get('results', [])
                all_results.extend(results)
                
                if total_count is None:
                    total_count = data.get('count', 0)
                
                # Stop early once the unscoped size cap is reached
                if not targeted_search and len(all_results) >= max_fields:
                    capped = True
                    break
                
                # Break if we've fetched all data
                if len(results) < limit or len(all_results) >= total_count:
                    break
                
                offset += limit
                # Brief pause between pages; rate-limit backoff is already
                # handled by _request_json_with_retries (429/5xx retries).
                await asyncio.sleep(0.5)
            
            # Prepare complete response
            complete_data = {
                'results': all_results,
                'count': len(all_results),
                'extraNote': "if your returned result is 0, you may want to check your parameter by using get_platform_setting_options tool to got correct parameter. Search supports fuzzy matching with multiple keywords (space-separated, AND logic).",
                'from_cache': False
            }
            if truncated or capped:
                complete_data['pagination_truncated'] = True
                if capped:
                    complete_data['extraNote'] += (f" NOTE: unscoped listing capped at {max_fields} fields; "
                                                   "use search / dataset_id / data_type to narrow.")
                else:
                    complete_data['extraNote'] += (" NOTE: server rejected a deeper page (HTTP 4xx), "
                                                   "results may be partial; narrow the search term or "
                                                   "dataset filter to see more.")
            
            # Cache the complete unscoped dump only (never poison it with search pages)
            if not targeted_search:
                self._set_cached_data(cache_key, complete_data, ttl=604800)
            
            # Extra client-side narrowing for targeted search (id/name/description)
            if targeted_search:
                filtered_results = [
                    item for item in all_results
                    if fuzzy_search_filter(item, search_term)
                ]
                complete_data['results'] = filtered_results
                complete_data['count'] = len(filtered_results)
            
            # Apply OS/IS Sharpe ratio filtering
            if filter_sharpe:
                results, removed, applied = sharpe_filter(complete_data['results'], region, delay)
                complete_data['results'] = results
                complete_data['count'] = len(results)
                complete_data['sharpe_filter_applied'] = applied
                complete_data['sharpe_filter_removed'] = removed
                if applied:
                    self.log(f"Sharpe filter ({region}_{delay}): removed {removed}/{removed + len(results)} fields with OS/IS sharpe < 0", "INFO")
            
            return complete_data
            
        except Exception as e:
            self.log(f"Failed to get datafields: {str(e)}", "ERROR")
            raise
        finally:
            # Release Redis lock if acquired
            if lock_acquired and self.redis_client:
                try:
                    self.redis_client.delete(lock_key)
                    self.log(f"Released Redis lock for get_datafields", "INFO")
                except Exception as e:
                    self.log(f"Failed to release Redis lock: {str(e)}", "WARNING")

    async def get_alpha_pnl(self, alpha_id: str) -> Dict[str, Any]:
        """Get PnL data for an alpha with retry logic."""
        await self.ensure_authenticated()
        
        max_retries = 5
        retry_delay = 2  # seconds
        
        for attempt in range(max_retries):
            try:
                self.log(f"Attempting to get PnL for alpha {alpha_id} (attempt {attempt + 1}/{max_retries})", "INFO")
                
                response = await self._request('GET', f"{self.base_url}/alphas/{alpha_id}/recordsets/pnl")
                response.raise_for_status()
                
                text = (response.text or "").strip()
                if not text:
                    if attempt < max_retries - 1:
                        self.log(f"Empty PnL response for {alpha_id}, retrying in {retry_delay} seconds...", "WARNING")
                        await asyncio.sleep(retry_delay)
                        retry_delay *= 1.5
                        continue
                    else:
                        self.log(f"Empty PnL response after {max_retries} attempts for {alpha_id}", "WARNING")
                        return {}
                
                try:
                    pnl_data = response.json()
                    if pnl_data:
                        self.log(f"Successfully retrieved PnL data for alpha {alpha_id}", "SUCCESS")
                        return pnl_data
                    else:
                        if attempt < max_retries - 1:
                            self.log(f"Empty PnL JSON for {alpha_id}, retrying in {retry_delay} seconds...", "WARNING")
                            await asyncio.sleep(retry_delay)
                            retry_delay *= 1.5
                            continue
                        else:
                            self.log(f"Empty PnL JSON after {max_retries} attempts for {alpha_id}", "WARNING")
                            return {}
                            
                except json.JSONDecodeError as parse_err:
                    if attempt < max_retries - 1:
                        self.log(f"PnL JSON parse failed for {alpha_id} (attempt {attempt + 1}), retrying in {retry_delay} seconds...", "WARNING")
                        await asyncio.sleep(retry_delay)
                        retry_delay *= 1.5
                        continue
                    else:
                        self.log(f"PnL JSON parse failed for {alpha_id} after {max_retries} attempts: {parse_err}", "WARNING")
                        return {}
                        
            except requests.RequestException as e:
                if attempt < max_retries - 1:
                    self.log(f"Failed to get alpha PnL for {alpha_id} (attempt {attempt + 1}), retrying in {retry_delay} seconds: {str(e)}", "WARNING")
                    await asyncio.sleep(retry_delay)
                    retry_delay *= 1.5
                    continue
                else:
                    self.log(f"Failed to get alpha PnL for {alpha_id} after {max_retries} attempts: {str(e)}", "ERROR")
                    raise
        
        return {}

    def _match_alpha_filters(self, alpha: Dict[str, Any], region: Optional[str],
                             status: Optional[str], alpha_type: Optional[str],
                             is_super: Optional[bool]) -> bool:
        """Check if an alpha matches the client-side filters."""
        if region and alpha.get('settings', {}).get('region', '').upper() != region.upper():
            return False
        if status and alpha.get('status', '').upper() != status.upper():
            return False
        if alpha_type and alpha.get('type', '').upper() != alpha_type.upper():
            return False
        if is_super is not None:
            actual_is_super = alpha.get('type', '').upper() == 'SUPER'
            if actual_is_super != is_super:
                return False
        return True

    async def get_user_alphas(
        self,
        stage: str = "OS",
        limit: int = 30,
        offset: int = 0,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        submission_start_date: Optional[str] = None,
        submission_end_date: Optional[str] = None,
        order: Optional[str] = None,
        hidden: Optional[bool] = None,
        region: Optional[str] = None,
        status: Optional[str] = None,
        alpha_type: Optional[str] = None,
        is_super: Optional[bool] = None,
    ) -> Dict[str, Any]:
        """Get user's alphas with advanced filtering and Redis caching (1 day TTL).
        
        Note: The BRAIN API does not support region/status/type/is_super as query
        parameters. These are applied as client-side filters after fetching.
        """
        await self.ensure_authenticated()
        
        need_client_filter = any([region, status, is_super is not None])
        
        try:
            # Build API params (only params the API actually supports)
            api_params = {
                "stage": stage,
            }
            if start_date:
                api_params["dateCreated>"] = start_date
            if end_date:
                api_params["dateCreated<"] = end_date
            if submission_start_date:
                api_params["dateSubmitted>"] = submission_start_date
            if submission_end_date:
                api_params["dateSubmitted<"] = submission_end_date
            if order:
                api_params["order"] = order
            if hidden is not None:
                api_params["hidden"] = str(hidden).lower()
            # 'type' is supported server-side (REGULAR, SUPER, etc.)
            if alpha_type:
                api_params["type"] = alpha_type
            
            # Build full cache key including client-side filter params
            cache_params = {**api_params, "limit": limit, "offset": offset}
            if region:
                cache_params["_region"] = region
            if status:
                cache_params["_status"] = status
            if alpha_type:
                cache_params["_type"] = alpha_type
            if is_super is not None:
                cache_params["_is_super"] = str(is_super).lower()
            
            cache_key = self._generate_cache_key('user_alphas', cache_params)
            
            # Try to get from cache
            cached_data = self._get_cached_data(cache_key)
            if cached_data:
                return {**cached_data, 'from_cache': True}
            
            if not need_client_filter:
                # No client-side filtering needed — use simple server-side pagination
                api_params["limit"] = limit
                api_params["offset"] = offset
                data = await self._request_json_with_retries(
                    'GET',
                    f"{self.base_url}/users/self/alphas",
                    params=api_params,
                    op_name=f"get_user_alphas(stage={stage}, offset={offset})",
                )
            else:
                # Client-side filtering: fetch only enough server pages to
                # satisfy the requested page. Scanning the whole alpha history
                # can take minutes for accounts with thousands of IS alphas.
                # Note: The API caps results at 100 per request regardless of limit param.
                BATCH_SIZE = 100
                try:
                    max_scan = max(
                        BATCH_SIZE,
                        int(os.environ.get("BRAIN_USER_ALPHAS_CLIENT_FILTER_MAX_SCAN", "1000")),
                    )
                except Exception:
                    max_scan = 1000
                target_matches = max(offset, 0) + max(limit, 0)
                filtered_results = []
                api_offset = 0
                total_server_count = None
                exhausted = False
                hit_scan_limit = False
                
                while True:
                    if api_offset >= max_scan:
                        hit_scan_limit = True
                        break

                    batch_limit = min(BATCH_SIZE, max_scan - api_offset)
                    api_params_batch = {**api_params, "limit": batch_limit, "offset": api_offset}
                    batch_data = await self._request_json_with_retries(
                        'GET',
                        f"{self.base_url}/users/self/alphas",
                        params=api_params_batch,
                        op_name=f"get_user_alphas(stage={stage}, offset={api_offset})",
                    )
                    
                    if total_server_count is None:
                        total_server_count = batch_data.get('count', 0)
                    
                    batch_results = batch_data.get('results', [])
                    if not batch_results:
                        exhausted = True
                        break
                    
                    for alpha in batch_results:
                        if self._match_alpha_filters(alpha, region, status, alpha_type, is_super):
                            filtered_results.append(alpha)
                    
                    api_offset += len(batch_results)
                    if target_matches and len(filtered_results) >= target_matches:
                        break
                    # Stop if we've exhausted all server-side results
                    if api_offset >= total_server_count:
                        exhausted = True
                        break
                
                # Apply user's offset/limit to the filtered results
                total_filtered = len(filtered_results)
                page_results = filtered_results[offset:offset + limit]
                
                next_offset = offset + limit
                has_more = (
                    total_filtered > next_offset
                    or (
                        len(page_results) == limit
                        and not exhausted
                        and not hit_scan_limit
                        and total_server_count is not None
                        and api_offset < total_server_count
                    )
                )
                partial_count = not exhausted
                data = {
                    'count': total_filtered if not partial_count else max(total_filtered, next_offset if has_more else total_filtered),
                    'next': f"offset={next_offset}&limit={limit}" if has_more else None,
                    'previous': f"offset={max(0, offset - limit)}&limit={limit}" if offset > 0 else None,
                    'results': page_results,
                    'partial_count': partial_count,
                    'server_scanned': api_offset,
                    'server_count': total_server_count,
                    'max_scan': max_scan,
                }
            
            # Add metadata
            data['from_cache'] = False
            
            # Cache complete pages longer. Partial client-filtered pages are
            # fast-path snapshots, so keep their TTL short.
            cache_ttl = 300 if data.get('partial_count') else 604800
            self._set_cached_data(cache_key, data, ttl=cache_ttl)
            
            return data
            
        except Exception as e:
            self.log(f"Failed to get user alphas: {str(e)}", "ERROR")
            raise

    def pre_submit_check(self, alpha_details: Dict[str, Any]) -> Dict[str, Any]:
        """Check IS metrics against submission thresholds before submitting.

        Criteria:
        - Sharpe > 1.3 and Fitness > 0.75 (relaxed thresholds for pre-submission check)
        - Margin > 0.05% for USA, otherwise > 0.15% (hard floor 0.08%)
        - Turnover between 4% and 40%
        - Returns > 4%
        - All other IS checks must PASS (no FAIL)
        """
        is_data = alpha_details.get('is')
        if not is_data:
            return {'passed': False, 'reason': 'No IS data available for this alpha. Simulation may not be complete.', 'details': []}

        failures = []
        warnings = []

        sharpe = is_data.get('sharpe', 0)
        fitness = is_data.get('fitness', 0)
        margin = is_data.get('margin', 0)
        turnover = is_data.get('turnover', 0)
        returns = is_data.get('returns', 0)
        drawdown = is_data.get('drawdown', 0)
        settings = alpha_details.get('settings') or {}
        region = (settings.get('region') or alpha_details.get('region') or '').upper()

        # Sharpe > 1.3
        if sharpe <= 1.3:
            failures.append(f'Sharpe {sharpe} <= 1.3 (required > 1.3)')

        # Fitness > 0.75
        if fitness <= 0.75:
            failures.append(f'Fitness {fitness} <= 0.75 (required > 0.75)')

        # USA margin rule is relaxed to >5bp. Other regions keep the >15bp target with a 8bp hard floor.
        # 2026-08-13 fix: margin is a LOCAL heuristic, NOT a platform check.
        # EUR qMNEG2Z2 (6.12bp) was blocked here but the platform's real verdict
        # was PROD_CORRELATION 0.839 FAIL — margin never appears in platform checks.
        # Downgrade to WARNING so the platform decides.
        if region == 'USA':
            if margin <= 0.0005:
                warnings.append(f'Margin {margin*100:.4f}% <= 5bp (recommended > 5bp for USA; platform does not check margin)')
        else:
            if margin <= 0.0008:
                warnings.append(f'Margin {margin*100:.4f}% <= 8bp (recommended > 15bp; platform does not check margin — real verdict is PROD_CORRELATION etc.)')
            elif margin <= 0.0015:
                warnings.append(f'Margin {margin*100:.4f}% <= 15bp (recommended > 15bp)')

        # Turnover between 4% and 40%
        if turnover < 0.04:
            failures.append(f'Turnover {turnover*100:.2f}% < 4% (required 4%-40%)')
        elif turnover > 0.40:
            failures.append(f'Turnover {turnover*100:.2f}% > 40% (required 4%-40%)')

        # Returns > 4%
        if returns <= 0.04:
            failures.append(f'Returns {returns*100:.2f}% <= 4% (required > 4%)')

        # # Returns > drawdown
        # if returns <= drawdown:
        #     failures.append(f'Returns {returns*100:.2f}% <= Drawdown {drawdown*100:.2f}% (required Returns > Drawdown)')

        # All other IS checks must not be FAIL
        checks = is_data.get('checks', [])
        for chk in checks:
            result = chk.get('result', '')
            name = chk.get('name', 'UNKNOWN')
            if result == 'FAIL':
                value = chk.get('value', 'N/A')
                limit = chk.get('limit', 'N/A')
                failures.append(f'IS check {name} FAILED (value={value}, limit={limit})')

        passed = len(failures) == 0
        return {
            'passed': passed,
            'failures': failures,
            'warnings': warnings,
            'metrics': {
                'region': region or None,
                'sharpe': sharpe,
                'fitness': fitness,
                'margin': margin,
                'margin_bp': round(margin * 10000, 2),
                'turnover': turnover,
                'returns': returns,
                'drawdown': drawdown,
            },
            'is_checks_summary': [
                {'name': c.get('name'), 'result': c.get('result'), 'value': c.get('value'), 'limit': c.get('limit')}
                for c in checks
            ],
        }

    async def submit_alpha(self, alpha_id: str) -> Dict[str, Any]:
        """Submit an alpha for production and return a detailed verdict dict.

        Handles the tri-state async submit flow correctly:
          - POST /alphas/{id}/submit -> 201/202 : accepted asynchronously; brief GET
            poll, then return accepted (IS checks resolve via get_alpha_details).
          - POST /alphas/{id}/submit -> 200 : IS checks already computed in body.
          - POST /alphas/{id}/submit -> 403 : forbidden.
          - Retry-After header on any response : rate-limited; GET-poll until clear.

        Returns: {"success": bool, "reason": str, "status_code": int,
                  "checks": [{"name","result","value","limit"}, ...]}
        """
        await self.ensure_authenticated()
        
        submit_url = f"{self.base_url}/alphas/{alpha_id}/submit"
        attempt = 0

        while True:
            attempt += 1
            self.log(f"Submit attempt {attempt} for alpha {alpha_id}", "INFO")

            try:
                response = await self._request('POST', submit_url)
            except Exception as e:
                self.log(f"Submit POST failed for {alpha_id}: {e}", "ERROR")
                raise

            self.log(f"Alpha submit, alpha_id={alpha_id}, status_code={response.status_code}", "INFO")

            # 201/202 = accepted asynchronously -> brief poll, then return accepted.
            if response.status_code in (201, 202):
                self.log(f"Submission accepted async (HTTP {response.status_code}); brief poll", "INFO")
                final = await self._poll_submit_until_resolved(submit_url)
                if final is not None and final.status_code == 200:
                    return self._interpret_submit_response(final, alpha_id)
                return {"success": True,
                        "reason": "Accepted (async); IS checks still computing - poll get_alpha_details",
                        "status_code": response.status_code, "checks": []}

            # Handle Retry-After header: switch to GET polling
            while 'retry-after' in {k.lower() for k in response.headers}:
                retry_after_raw = response.headers.get('Retry-After') or response.headers.get('retry-after', '5')
                try:
                    wait_time = float(retry_after_raw)
                except ValueError:
                    wait_time = 5.0
                # Match reference: 5x multiplier for short waits
                actual_wait = 5 * wait_time if wait_time < 60 else wait_time
                self.log(f"Rate limited (Retry-After={retry_after_raw}s), waiting {actual_wait:.0f}s then GET polling...", "INFO")
                await asyncio.sleep(actual_wait)
                try:
                    response = await self._request('GET', submit_url)
                    self.log(f"GET poll response, alpha_id={alpha_id}, status_code={response.status_code}", "INFO")
                except Exception as e:
                    self.log(f"Submit GET poll failed for {alpha_id}: {e}", "ERROR")
                    raise

            if response.status_code == 200:
                # Parse response JSON to validate IS checks
                try:
                    res_json = response.json()
                except (json.JSONDecodeError, ValueError):
                    self.log(f"Submit response for {alpha_id} is not valid JSON: {(response.text or '')[:200]}", "ERROR")
                    return False

                if not res_json:
                    return False

                if 'detail' in res_json and res_json['detail'] == 'Not found.':
                    self.log(f"Submit failed: alpha {alpha_id} not found", "ERROR")
                    return False

                # Check IS checks in response
                if 'is' in res_json and 'checks' in res_json['is']:
                    for item in res_json['is']['checks']:
                        if item.get('name') == 'ALREADY_SUBMITTED':
                            self.log(f"Alpha {alpha_id} already submitted", "WARNING")
                            return False
                        if item.get('result') == 'FAIL':
                            self.log(f"Alpha {alpha_id} IS check failed: {item.get('name')} limit={item.get('limit')} value={item.get('value')}", "ERROR")
                            return False

                self.log(f"Alpha {alpha_id} submission successful!", "INFO")
                return self._interpret_submit_response(response, alpha_id)

            elif response.status_code == 403:
                self.log(f"Submit forbidden (403) for alpha {alpha_id}", "ERROR")
                detail = {}
                try:
                    detail = response.json()
                except Exception:
                    pass
                failing = []
                checks = []
                if 'is' in detail and 'checks' in detail['is']:
                    for item in detail['is']['checks']:
                        checks.append({"name": item.get('name'), "result": item.get('result'), "value": item.get('value'), "limit": item.get('limit')})
                        if item.get('result') == 'FAIL':
                            failing.append(f"{item.get('name')}(value={item.get('value')}, limit={item.get('limit')})")
                if failing:
                    reason = "HTTP 403 - failing IS checks: " + ", ".join(failing)
                else:
                    reason = "HTTP 403 Forbidden (no failing IS check shown - likely account/quota block)"
                return {"success": False, "reason": reason, "status_code": 403, "checks": checks, "raw": (response.text or '')[:800]}

            else:
                self.log(f"Submit failed status={response.status_code} for {alpha_id}, waiting 2 minutes before retry...", "WARNING")
                await asyncio.sleep(120)

    async def _poll_submit_until_resolved(self, submit_url: str, max_polls: int = 6, sleep_s: int = 10) -> Any:
        """Briefly GET-poll the submit endpoint; returns the latest response or None."""
        last = None
        for _ in range(max_polls):
            await asyncio.sleep(sleep_s)
            try:
                resp = await self._request('GET', submit_url)
            except Exception as e:
                self.log(f"Submit poll GET failed: {e}", "ERROR")
                return last
            last = resp
            if 'retry-after' in {k.lower() for k in resp.headers}:
                continue
            if resp.status_code == 200:
                return resp
        self.log("Submit poll reached max_polls; returning last response", "WARNING")
        return last

    def _interpret_submit_response(self, response, alpha_id: str) -> Dict[str, Any]:
        """Parse a submit GET/POST response into a verdict dict."""
        try:
            res_json = response.json()
        except (json.JSONDecodeError, ValueError):
            self.log(f"Submit response for {alpha_id} is not valid JSON: {(response.text or '')[:300]}", "ERROR")
            return {"success": False, "reason": "Non-JSON submit response", "status_code": response.status_code, "checks": [], "raw": (response.text or '')[:500]}
        if not res_json:
            return {"success": False, "reason": "Empty submit response", "status_code": response.status_code, "checks": []}
        if 'detail' in res_json and res_json['detail'] == 'Not found.':
            self.log(f"Submit failed: alpha {alpha_id} not found", "ERROR")
            return {"success": False, "reason": "Alpha not found", "status_code": response.status_code, "checks": []}

        checks = []
        if 'is' in res_json and 'checks' in res_json['is']:
            for item in res_json['is']['checks']:
                checks.append({
                    "name": item.get('name'),
                    "result": item.get('result'),
                    "value": item.get('value'),
                    "limit": item.get('limit'),
                })
            for item in res_json['is']['checks']:
                if item.get('name') == 'ALREADY_SUBMITTED':
                    self.log(f"Alpha {alpha_id} already submitted (idempotent success)", "WARNING")
                    return {"success": True, "reason": "ALREADY_SUBMITTED (idempotent success)", "status_code": response.status_code, "checks": checks}
                if item.get('result') == 'FAIL':
                    self.log(f"Alpha {alpha_id} IS check FAILED: {item.get('name')} limit={item.get('limit')} value={item.get('value')}", "ERROR")
                    return {"success": False, "reason": f"IS check FAIL: {item.get('name')}", "status_code": response.status_code, "checks": checks}

        self.log(f"Alpha {alpha_id} submission successful!", "INFO")
        return {"success": True, "reason": "IS checks passed", "status_code": response.status_code, "checks": checks}

    async def get_submission_quota(self, window_hours: int = 48, limit: int = 4) -> Dict[str, Any]:
        """Estimate REGULAR_SUBMISSION quota usage (rolling 48h, limit 4).

        Read-only: counts OS alphas whose dateSubmitted falls inside the
        trailing window (conservative estimate; platform uses rolling release).
        Platform-verified 2026-08-13: REGULAR_SUBMISSION check limit=4
        (qMNEG2Z2 verdict showed value=3 after IND x2 + 1 other).
        """
        import datetime as _dt
        try:
            payload = await self.get_user_alphas(stage="OS", limit=100, order="-dateSubmitted")
        except Exception as exc:
            return {"error": str(exc)}

        now = _dt.datetime.now(_dt.timezone.utc)

        def _parse(ts: str):
            if not ts:
                return None
            try:
                parsed = _dt.datetime.fromisoformat(ts)
                if parsed.tzinfo is None:
                    parsed = parsed.replace(tzinfo=_dt.timezone.utc)
                return parsed
            except ValueError:
                return None

        submissions = []
        for alpha in payload.get("results", []):
            parsed = _parse(alpha.get("dateSubmitted"))
            if parsed:
                submissions.append((alpha.get("id"), parsed))
        used = [aid for aid, ts in submissions if (now - ts).total_seconds() <= window_hours * 3600]
        remaining = max(0, limit - len(used))
        latest = max((ts for _, ts in submissions), default=None)
        release = (latest + _dt.timedelta(hours=window_hours)).isoformat() if latest else None
        hours_left = (
            max(0.0, (latest + _dt.timedelta(hours=window_hours) - now).total_seconds() / 3600)
            if latest else None
        )
        return {
            "limit": limit,
            "window_hours": window_hours,
            "used": len(used),
            "used_ids": used,
            "remaining": remaining,
            "earliest_release_utc": release,
            "hours_until_release": hours_left,
            "note": "Conservative trailing-window estimate; platform uses rolling release per submission.",
        }

    async def get_events(self) -> Dict[str, Any]:
        """Get available events and competitions."""
        await self.ensure_authenticated()
        
        try:
            response = await self._request('GET', f"{self.base_url}/events")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            self.log(f"Failed to get events: {str(e)}", "ERROR")
            raise

    async def get_leaderboard(self, user_id: Optional[str] = None) -> Dict[str, Any]:
        """Get leaderboard data."""
        await self.ensure_authenticated()
        
        try:
            params = {}
            
            if user_id:
                params['user'] = user_id
            else:
                # Get current user ID if not specified
                user_response = await self._request('GET', f"{self.base_url}/users/self")
                if user_response.status_code == 200:
                    user_data = user_response.json()
                    params['user'] = user_data.get('id')
            
            response = await self._request('GET', f"{self.base_url}/consultant/boards/leader", params=params)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            self.log(f"Failed to get leaderboard: {str(e)}", "ERROR")
            raise
