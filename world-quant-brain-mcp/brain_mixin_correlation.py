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


class CorrelationMixin:
    def _pnl_response_to_series(self, aid: str, pnl_data: dict) -> Optional[pd.Series]:
        """Convert a raw PnL API response dict to a pandas Series indexed by date."""
        try:
            if not pnl_data:
                return None
            records = pnl_data.get('records', [])
            schema = pnl_data.get('schema', {}).get('properties', [])
            if not records or not schema:
                return None
            cols = [p['name'] for p in schema]
            df = pd.DataFrame(records, columns=cols)
            df['date'] = pd.to_datetime(df['date'])
            df.set_index('date', inplace=True)
            if 'pnl' not in df.columns:
                return None
            return df['pnl'].rename(aid)
        except Exception:
            return None

    def _os_pnl_pool_path(
        self,
        instrument_type: str,
        region: str,
        universe: str,
        delay: Union[int, str],
    ) -> Path:
        """Return the on-disk cache path for a configuration-specific OS PnL pool."""
        cache_dir = Path(__file__).parent / 'downloads'
        cache_dir.mkdir(parents=True, exist_ok=True)
        safe_parts = [
            str(instrument_type).strip().lower() or 'unknown',
            str(region).strip().lower() or 'unknown',
            str(universe).strip().lower() or 'unknown',
            f"delay{delay}",
        ]
        return cache_dir / f"os_pnl_pool_{'_'.join(safe_parts)}.pkl"

    def _os_ppac_ids_path(
        self,
        instrument_type: str,
        region: str,
        universe: str,
        delay: Union[int, str],
    ) -> Path:
        """Sidecar file holding the Power-Pool-Alpha id set for a configuration.

        BRAIN reports two distinct correlations that partition the same OS pool
        by each alpha's ``classifications``:
          * "Self Correlation"       -> pool EXCLUDING Power Pool Alphas
          * "Power Pool Correlation" -> pool of ONLY Power Pool Alphas
        We persist which OS ids are classified 'Power Pool Alpha' so the local
        self-correlation can exclude them (matching the platform).
        """
        return self._os_pnl_pool_path(
            instrument_type, region, universe, delay
        ).with_suffix('.ppac.json')

    def _load_ppac_ids(
        self,
        instrument_type: str,
        region: str,
        universe: str,
        delay: Union[int, str],
    ) -> set:
        """Load the cached Power-Pool-Alpha id set (empty set if unavailable)."""
        try:
            p = self._os_ppac_ids_path(instrument_type, region, universe, delay)
            if p.exists():
                return set(json.loads(p.read_text()))
        except Exception as e:
            self.log(f"[SC cache] Failed to load ppac ids sidecar: {e}", "WARNING")
        return set()

    async def _get_os_pnl_pool_lock(self, pool_path: Path) -> asyncio.Lock:
        """Return the in-process lock for one configuration-specific OS PnL cache."""
        pool_key = str(pool_path)
        async with self._os_pnl_pool_locks_guard:
            lock = self._os_pnl_pool_locks.get(pool_key)
            if lock is None:
                lock = asyncio.Lock()
                self._os_pnl_pool_locks[pool_key] = lock
            return lock

    def _exclude_os_pnl_target(self, pool: pd.DataFrame, exclude_id: Optional[str]) -> pd.DataFrame:
        if exclude_id and isinstance(pool, pd.DataFrame) and exclude_id in pool.columns:
            return pool.drop(columns=[exclude_id], errors='ignore')
        return pool

    async def _list_matching_os_alpha_ids(
        self,
        instrument_type: str,
        region: str,
        universe: str,
        delay: Union[int, str],
    ) -> List[str]:
        """Fetch OS alpha IDs that match the target alpha's market configuration.

        BRAIN self-correlation semantics compare against the user's self alpha
        pool for the same instrument/region/universe/delay, and can include
        both REGULAR and SUPER alphas. Filtering locally on the same
        configuration keeps the local calculation aligned with those semantics.
        """
        all_ids: List[str] = []
        ppac_ids: List[str] = []
        offset = 0
        page_size = 100
        while True:
            params = {
                'stage': 'OS',
                'limit': page_size,
                'offset': offset,
                'order': '-dateSubmitted',
            }
            try:
                data = await self._request_json_with_retries(
                    'GET',
                    f"{self.base_url}/users/self/alphas",
                    params=params,
                    op_name=f"list_matching_os_alphas(offset={offset})",
                )
            except Exception as e:
                self.log(f"Failed to page OS alpha list at offset={offset}: {e}", "WARNING")
                break
            results = data.get('results') or []
            if not results:
                break
            for alpha in results:
                if not alpha.get('id'):
                    continue
                settings = alpha.get('settings', {})
                if settings.get('instrumentType') != instrument_type:
                    continue
                if settings.get('region') != region:
                    continue
                if settings.get('universe') != universe:
                    continue
                if str(settings.get('delay')) != str(delay):
                    continue
                all_ids.append(alpha['id'])
                # A Power Pool Alpha is identified by its classifications, e.g.
                # {"id": "POWER_POOL_ALPHA", "name": "Power Pool Alpha"}. The
                # platform's "Self Correlation" EXCLUDES these; "Power Pool
                # Correlation" uses only these. Match on id OR name (as the atom
                # detector does) to be robust to the key the API returns.
                classifications = alpha.get('classifications') or []
                for c in classifications:
                    if not isinstance(c, dict):
                        continue
                    cid = c.get('id') or c.get('name') or ''
                    cname = c.get('name') or ''
                    if (isinstance(cid, str) and 'POWER_POOL' in cid.upper()) or \
                       (isinstance(cname, str) and cname.strip() == 'Power Pool Alpha'):
                        ppac_ids.append(alpha['id'])
                        break
            if len(results) < page_size:
                break
            offset += page_size

        # Persist the Power-Pool-Alpha id set so get_self_correlation can
        # exclude/select them without re-listing (survives the sync debounce
        # cache and process restarts).
        try:
            sidecar = self._os_ppac_ids_path(instrument_type, region, universe, delay)
            sidecar.write_text(json.dumps(sorted(set(ppac_ids))))
        except Exception as e:
            self.log(f"[SC cache] Failed to persist ppac ids sidecar: {e}", "WARNING")

        return all_ids

    async def sync_os_pnl_pool(
        self,
        instrument_type: str,
        region: str,
        universe: str,
        delay: Union[int, str],
        exclude_id: Optional[str] = None,
    ) -> pd.DataFrame:
        """Incrementally sync the matching OS alpha PnL pool cache on disk.

        Closed-loop logic (mirrors the reference implementation):
        - Fetch the current server-side list of matching OS alpha IDs.
        - Load the local pickle cache (if any) and drop any columns whose alpha
          is no longer present on the server (handles deletions).
        - Download PnL only for IDs that are on the server but missing locally
          (OS alpha PnL is effectively static, so old columns are reused).
        - Persist the merged pool back to disk and return it.
        """
        pool_path = self._os_pnl_pool_path(instrument_type, region, universe, delay)
        pool_lock = await self._get_os_pnl_pool_lock(pool_path)
        async with pool_lock:
            pool_key = str(pool_path)
            debounce = self._os_pnl_pool_sync_debounce_seconds
            cached_sync = self._os_pnl_pool_last_sync.get(pool_key)
            if cached_sync and debounce > 0:
                synced_at, synced_pool = cached_sync
                if time.time() - synced_at <= debounce:
                    return self._exclude_os_pnl_target(synced_pool, exclude_id)

            synced_pool = await self._sync_os_pnl_pool_unlocked(
                pool_path=pool_path,
                instrument_type=instrument_type,
                region=region,
                universe=universe,
                delay=delay,
            )
            self._os_pnl_pool_last_sync[pool_key] = (time.time(), synced_pool)
            return self._exclude_os_pnl_target(synced_pool, exclude_id)

    async def _sync_os_pnl_pool_unlocked(
        self,
        pool_path: Path,
        instrument_type: str,
        region: str,
        universe: str,
        delay: Union[int, str],
    ) -> pd.DataFrame:
        server_ids = await self._list_matching_os_alpha_ids(
            instrument_type, region, universe, delay
        )

        # Load existing cache and drop removed alphas (closed-loop cleanup)
        local_pool = pd.DataFrame()
        if pool_path.exists():
            try:
                local_pool = await asyncio.to_thread(pd.read_pickle, pool_path)
                if isinstance(local_pool, pd.DataFrame) and not local_pool.empty:
                    keep_cols = [c for c in local_pool.columns if c in set(server_ids)]
                    dropped = local_pool.shape[1] - len(keep_cols)
                    if dropped > 0:
                        self.log(f"[SC cache] Dropping {dropped} alpha(s) removed from OS list", "INFO")
                    local_pool = local_pool[keep_cols]
                else:
                    local_pool = pd.DataFrame()
            except Exception as e:
                self.log(f"[SC cache] Failed to read pool pickle, rebuilding: {e}", "WARNING")
                local_pool = pd.DataFrame()

        need_download = [aid for aid in server_ids if aid not in local_pool.columns]

        if not need_download:
            self.log(f"[SC cache] Pool up-to-date: {local_pool.shape[1]} OS alphas", "INFO")
            return local_pool

        self.log(f"[SC cache] Incremental download: {len(need_download)} new OS alpha(s)", "INFO")

        fetch_sem = asyncio.Semaphore(5)

        async def fetch_one(oid: str):
            async with fetch_sem:
                try:
                    data = await self.get_alpha_pnl(oid)
                    return self._pnl_response_to_series(oid, data)
                except Exception as e:
                    self.log(f"[SC cache] Skip {oid}: PnL fetch failed ({e})", "WARNING")
                    return None

        fetched = await asyncio.gather(*[fetch_one(oid) for oid in need_download])
        new_series = [s for s in fetched if s is not None]

        if new_series:
            new_df = pd.concat(new_series, axis=1)
            full_pool = new_df if local_pool.empty else pd.concat([local_pool, new_df], axis=1)
            full_pool = full_pool.sort_index()
            try:
                await asyncio.to_thread(full_pool.to_pickle, pool_path)
            except Exception as e:
                self.log(f"[SC cache] Failed to persist pool pickle: {e}", "WARNING")
            local_pool = full_pool
            self.log(f"[SC cache] Pool now has {local_pool.shape[1]} OS alphas", "INFO")
        else:
            self.log(f"[SC cache] No new PnL captured (all fetches failed?); keeping {local_pool.shape[1]} cached", "WARNING")

        return local_pool

    async def get_self_correlation(self, alpha_id: str, correlation_type: str = 'self') -> Dict[str, Any]:
        """Calculate self-correlation locally using an incrementally-cached OS PnL pool.

        - OS alpha PnL is considered static and cached on disk
          (``downloads/os_pnl_pool.pkl``); only newly-submitted OS alphas are
          downloaded on each call and stale entries are pruned.
        - The target alpha's PnL is always fetched fresh (it is typically still
          IS and may change between calls).
        - Correlation is computed on the last 4 years of daily returns, matching
          the reference ``calculate_sc_locally`` semantics.

        correlation_type partitions the OS pool the same way the BRAIN platform
        does, via each alpha's ``classifications``:
          * 'self'      -> "Self Correlation": pool EXCLUDING Power Pool Alphas.
          * 'powerpool' -> "Power Pool Correlation": ONLY Power Pool Alphas.
          * 'all'       -> legacy behaviour (whole OS pool, no partition).
        Default is 'self' so the number matches the platform's Self Correlation
        (previously the whole pool was used, which mixed in Power Pool Alphas and
        over-reported the max).
        """
        await self.ensure_authenticated()

        try:
            # Target alpha PnL is always fresh; details are needed only for the
            # market-configuration key. Fetch both independent endpoints at once.
            target_pnl_data, target_details = await asyncio.gather(
                self.get_alpha_pnl(alpha_id),
                self.get_alpha_details(alpha_id),
            )
            target_series = self._pnl_response_to_series(alpha_id, target_pnl_data)
            if target_series is None:
                self.log(f"Could not parse PnL for target alpha {alpha_id}", "WARNING")
                return {}

            target_settings = target_details.get('settings', {})
            instrument_type = target_settings.get('instrumentType')
            region = target_settings.get('region')
            universe = target_settings.get('universe')
            delay = target_settings.get('delay')
            if not all([instrument_type, region, universe]) or delay is None:
                self.log(
                    f"Missing target settings for self-correlation on {alpha_id}: {target_settings}",
                    "WARNING",
                )
                return {}

            # Sync only the OS pool matching the target alpha's market configuration.
            os_pool = await self.sync_os_pnl_pool(
                instrument_type=instrument_type,
                region=region,
                universe=universe,
                delay=delay,
                exclude_id=alpha_id,
            )

            if os_pool is None or os_pool.empty:
                self.log(f"No OS alphas available; self-correlation for {alpha_id} is 0", "INFO")
                return {'max': 0.0, 'records': [], 'local_calculation': True, 'pool_size': 0}

            # Combine target with pool, forward-fill gaps, diff -> daily returns.
            # Use a synthetic target column so any stale cached column with the
            # same alpha id cannot create duplicate labels.
            target_col = f"__target__{alpha_id}"
            combined = pd.concat([os_pool, target_series.rename(target_col).to_frame()], axis=1).ffill()
            rets = combined.diff()
            if rets.empty:
                return {'max': 0.0, 'records': [], 'local_calculation': True, 'pool_size': os_pool.shape[1]}

            last_date = rets.index.max()
            rets = rets[rets.index > last_date - pd.DateOffset(years=4)]

            if target_col not in rets.columns:
                return {'max': 0.0, 'records': [], 'local_calculation': True, 'pool_size': os_pool.shape[1]}

            target_rets = rets[target_col]
            pool_rets = rets.drop(columns=[target_col], errors='ignore')

            # Partition the OS pool by Power-Pool-Alpha classification to match
            # the platform's Self vs Power Pool correlation semantics. Excluding
            # Power Pool Alphas is what makes the local number line up with the
            # platform's "Self Correlation" (the previous code used the whole
            # pool and could over-report the max).
            ppac_ids = self._load_ppac_ids(instrument_type, region, universe, delay)
            ctype = (correlation_type or 'self').lower()
            full_pool_size = int(pool_rets.shape[1])
            if ctype in ('self', 'selfcorr'):
                drop_cols = [c for c in pool_rets.columns if c in ppac_ids]
                pool_rets = pool_rets.drop(columns=drop_cols, errors='ignore')
            elif ctype in ('powerpool', 'ppac', 'ppa'):
                keep_cols = [c for c in pool_rets.columns if c in ppac_ids]
                pool_rets = pool_rets[keep_cols]
            # ctype == 'all' -> legacy whole-pool behaviour (no partition)
            partitioned_pool_size = int(pool_rets.shape[1])

            if pool_rets.empty:
                return {
                    'max': 0.0,
                    'records': [],
                    'local_calculation': True,
                    'pool_size': partitioned_pool_size,
                    'correlation_type': ctype,
                    'full_os_pool_size': full_pool_size,
                    'ppac_ids_cached': len(ppac_ids),
                    'excluded_power_pool_count': full_pool_size - partitioned_pool_size if ctype in ('self', 'selfcorr') else None,
                }

            # Compute only target-vs-pool correlations instead of the full N x N
            # matrix; this is the hot path when the OS pool is large.
            sc_series = pool_rets.corrwith(target_rets).dropna()
            max_corr = float(sc_series.max()) if not sc_series.empty else 0.0

            records = [
                {'id': oid, 'correlation': float(val)}
                for oid, val in sc_series.nlargest(10).items()
            ]

            self.log(
                f"[SC本地] Alpha {alpha_id}: max_{ctype}_corr={max_corr:.4f} "
                f"(pool={partitioned_pool_size}/{full_pool_size} OS alphas after "
                f"'{ctype}' partition; {len(ppac_ids)} power-pool ids cached)",
                "INFO",
            )
            return {
                'max': max_corr,
                'records': records,
                'local_calculation': True,
                'pool_size': partitioned_pool_size,
                'correlation_type': ctype,
                'full_os_pool_size': full_pool_size,
                'ppac_ids_cached': len(ppac_ids),
                'excluded_power_pool_count': (full_pool_size - partitioned_pool_size) if ctype in ('self', 'selfcorr') else None,
            }

        except Exception as e:
            self.log(f"Failed to calculate self-correlation locally: {str(e)}", "ERROR")
            raise

    async def get_mutual_correlation(
        self,
        alpha_ids: List[str],
        threshold: float = 0.5,
        years: int = 4,
    ) -> Dict[str, Any]:
        """Pairwise ("mutual") correlation AMONG a caller-supplied set of alphas.

        Unlike check_self_correlation (target-vs-OS-pool) and check_correlation
        (target-vs-production), this computes the full NxN correlation matrix
        among the given alphas' own daily returns — the check needed when
        selecting a set of alphas that must be mutually decorrelated (e.g. a
        submission basket with a max-pairwise-correlation rule).

        Correlation convention matches the local self-correlation: daily returns
        = diff of cumulative PnL (ffill gaps), restricted to the last ``years``.

        Returns the matrix, the single most-correlated pair, every pair at/above
        ``threshold``, whether all pairs are below it, and a greedy maximal
        subset whose members are all mutually below ``threshold``.
        """
        await self.ensure_authenticated()

        # De-duplicate while preserving order.
        ids = list(dict.fromkeys([a for a in (alpha_ids or []) if a]))
        if len(ids) < 2:
            return {'error': 'Provide at least 2 distinct alpha ids.', 'alpha_ids': ids}

        fetch_sem = asyncio.Semaphore(5)

        async def fetch_one(oid: str):
            async with fetch_sem:
                try:
                    data = await self.get_alpha_pnl(oid)
                    return oid, self._pnl_response_to_series(oid, data)
                except Exception as e:
                    self.log(f"[mutual-corr] Skip {oid}: PnL fetch failed ({e})", "WARNING")
                    return oid, None

        fetched = await asyncio.gather(*[fetch_one(o) for o in ids])
        series = {oid: s for oid, s in fetched if s is not None}
        missing = [oid for oid, s in fetched if s is None]
        if len(series) < 2:
            return {
                'error': 'Fewer than 2 alphas had usable PnL.',
                'missing_pnl': missing,
                'alpha_ids': ids,
            }

        present = [oid for oid in ids if oid in series]
        combined = pd.concat([series[oid].rename(oid).to_frame() for oid in present], axis=1).ffill()
        rets = combined.diff()
        if not rets.empty:
            last_date = rets.index.max()
            rets = rets[rets.index > last_date - pd.DateOffset(years=years)]
        rets = rets.dropna(how='all')
        if rets.shape[0] < 2:
            return {'error': 'Insufficient overlapping PnL history.', 'missing_pnl': missing, 'alpha_ids': ids}

        corr = rets.corr()
        cols = [c for c in present if c in corr.columns]

        def cval(a: str, b: str) -> float:
            try:
                v = float(corr.loc[a, b])
                return v if v == v else 0.0  # NaN -> 0
            except Exception:
                return 0.0

        pairs = []
        for i in range(len(cols)):
            for j in range(i + 1, len(cols)):
                pairs.append((cols[i], cols[j], cval(cols[i], cols[j])))
        pairs.sort(key=lambda x: -abs(x[2]))

        over = [{'a': a, 'b': b, 'correlation': round(c, 4)} for a, b, c in pairs if abs(c) >= threshold]
        max_pair = (
            {'a': pairs[0][0], 'b': pairs[0][1], 'correlation': round(pairs[0][2], 4)}
            if pairs else None
        )

        # Greedy maximal mutually-below-threshold subset: consider nodes in
        # ascending order of average |correlation| (least entangled first), keep
        # a node only if it is < threshold vs every already-kept node. This is a
        # heuristic (max independent set is NP-hard) but gives a good basket.
        if len(cols) > 1:
            avg_abs = {
                o: sum(abs(cval(o, p)) for p in cols if p != o) / (len(cols) - 1)
                for o in cols
            }
        else:
            avg_abs = {cols[0]: 0.0} if cols else {}
        order = sorted(cols, key=lambda o: avg_abs.get(o, 0.0))
        kept: List[str] = []
        for oid in order:
            if all(abs(cval(oid, k)) < threshold for k in kept):
                kept.append(oid)

        matrix = {a: {b: round(cval(a, b), 4) for b in cols} for a in cols}

        self.log(
            f"[mutual-corr] {len(cols)} alphas: max pair "
            f"{max_pair['correlation'] if max_pair else 'n/a'}, "
            f"{len(over)} pair(s) >= {threshold}, max mutually-<{threshold} subset size {len(kept)}",
            "INFO",
        )

        return {
            'alpha_ids': cols,
            'threshold': threshold,
            'years': years,
            'num_points': int(rets.shape[0]),
            'matrix': matrix,
            'max_pair': max_pair,
            'pairs_over_threshold': over,
            'all_below_threshold': len(over) == 0,
            'max_mutually_below_subset': kept,
            'max_mutually_below_subset_size': len(kept),
            'missing_pnl': missing,
            'local_calculation': True,
        }

    async def check_self_correlation(
        self,
        alpha_id: str,
        threshold: float = 0.7,
        correlation_type: str = 'self',
    ) -> Dict[str, Any]:
        """Compute self-correlation locally using the cached OS PnL pool.

        Args:
            alpha_id: Target alpha ID.
            threshold: Max-correlation threshold used for the pass/fail check.
            correlation_type: 'self' (default; pool EXCLUDES Power Pool Alphas,
                matching the platform's "Self Correlation"), 'powerpool' (only
                Power Pool Alphas, matching "Power Pool Correlation"), or 'all'
                (legacy whole-pool behaviour).
        """
        await self.ensure_authenticated()

        correlation_data = await self.get_self_correlation(alpha_id, correlation_type=correlation_type)
        if not isinstance(correlation_data, dict) or not correlation_data:
            return {
                'alpha_id': alpha_id,
                'threshold': threshold,
                'correlation_type': correlation_type,
                'max_correlation': None,
                'passes_check': None,
                'status': 'data_unavailable',
                'message': 'Local self-correlation data is unavailable for this alpha.',
                'correlation_data': correlation_data,
            }

        try:
            max_correlation = float(correlation_data.get('max'))
        except (TypeError, ValueError):
            max_correlation = None

        passes_check = max_correlation < threshold if max_correlation is not None else None

        return {
            'alpha_id': alpha_id,
            'threshold': threshold,
            'correlation_type': correlation_type,
            'max_correlation': max_correlation,
            'passes_check': passes_check,
            'local_calculation': True,
            'correlation_data': correlation_data,
        }

    async def check_correlation(self, alpha_id: str, correlation_type: str = "production", threshold: float = 0.7) -> Dict[str, Any]:
        """ Only where all IS metrics PASS to Check alpha correlation, Check alpha correlation against production alphas, self alphas, or both.

        Concurrency: production correlation hits BRAIN's per-account
        single-concurrency endpoint. ``get_production_correlation`` uses a
        fail-fast lock, so concurrent production checks return busy instead of
        waiting. The ``self`` path is computed locally and is not gated here.
        """
        await self.ensure_authenticated()

        try:
            results = {
                'alpha_id': alpha_id,
                'threshold': threshold,
                'correlation_type': correlation_type,
                'checks': {}
            }
            
            # Determine which correlations to check
            check_types = []
            if correlation_type == "both":
                check_types = ["production", "self"]
            else:
                check_types = [correlation_type]
            
            all_passed = True
            
            for check_type in check_types:
                if check_type == "production":
                    correlation_data = await self.get_production_correlation(alpha_id)
                    
                    # Handle pending/data-not-yet-available case (super alphas, fresh simulations)
                    if correlation_data and correlation_data.get('status') == 'pending':
                        results['checks'][check_type] = {
                            'max_correlation': None,
                            'passes_check': None,
                            'status': 'pending',
                            'message': correlation_data.get('message', ''),
                            'correlation_data': correlation_data,
                        }
                        results['all_passed'] = None
                        results['status'] = 'pending'
                        results['message'] = correlation_data.get('message', '')
                        return results

                    if correlation_data and correlation_data.get('status') == 'correlation_busy':
                        results['checks'][check_type] = {
                            'max_correlation': None,
                            'passes_check': None,
                            'status': 'correlation_busy',
                            'message': correlation_data.get('message', ''),
                            'retry_after': correlation_data.get('retry_after'),
                            'correlation_data': correlation_data,
                        }
                        results['all_passed'] = None
                        results['status'] = 'correlation_busy'
                        results['message'] = correlation_data.get('message', '')
                        results['retry_after'] = correlation_data.get('retry_after')
                        return results

                    if (
                        correlation_data
                        and isinstance(correlation_data.get('records'), list)
                        and len(correlation_data['records']) > 0
                        and correlation_data.get('max') is not None
                    ):
                        max_correlation = correlation_data['max']
                        passes_check = max_correlation < threshold
                        results['checks'][check_type] = {
                            'max_correlation': max_correlation,
                            'passes_check': passes_check,
                            'correlation_data': correlation_data
                        }
                        if not passes_check:
                            all_passed = False
                            results["all_passed"] = all_passed
                            return results
                    else:
                        # Data returned but has no usable records/max (empty or malformed).
                        # Return None to signal "data unavailable" rather than faking max=0.
                        results['checks'][check_type] = {
                            'max_correlation': None,
                            'passes_check': None,
                            'status': 'data_unavailable',
                            'message': (
                                'Production correlation data is unavailable for this alpha. '
                                'This may be a newly-created super alpha where the platform '
                                'has not yet computed the correlation. Please retry in a few minutes.'
                            ),
                            'correlation_data': correlation_data,
                        }
                        results['all_passed'] = None
                        results['status'] = 'data_unavailable'
                        return results
                elif check_type == "self":
                    correlation_data = await self.get_self_correlation(alpha_id)
                else:
                    continue
                
                # Analyze correlation data (self-correlation path)
                if correlation_data and correlation_data.get('max') is not None:
                    max_correlation = correlation_data['max']
                    passes_check = max_correlation < threshold
                else:
                    max_correlation = None
                    passes_check = None
                
                results['checks'][check_type] = {
                    'max_correlation': max_correlation,
                    'passes_check': passes_check,
                    'correlation_data': correlation_data
                }
                
                if passes_check is not True:
                    all_passed = False
            
            results['all_passed'] = all_passed
            
            return results
            
        except Exception as e:
            self.log(f"Failed to check correlation: {str(e)}", "ERROR")
            raise

    async def get_submission_check(self, alpha_id: str) -> Dict[str, Any]:
        """Comprehensive pre-submission check."""
        await self.ensure_authenticated()
        
        try:
            # This endpoint might not exist, so we simulate it by calling other functions
            # In a real scenario, this would be a single API call
            
            pnl_data = await self.get_alpha_pnl(alpha_id)
            yearly_stats = await self.get_alpha_yearly_stats(alpha_id)
            correlation = await self.check_correlation(alpha_id)
            
            return {
                "pnl_summary": pnl_data.get("pnlSummary", {}),
                "yearly_stats": yearly_stats,
                "correlation": correlation
            }
        except Exception as e:
            self.log(f"Failed submission check: {str(e)}", "ERROR")
            raise

    async def set_alpha_properties(self, alpha_id: str, name: Optional[str] = None, 
                                   color: Optional[str] = None, tags: Optional[List[str]] = None,
                                   descriptions: str = "None",
                                   selection_description: Optional[str] = None,
                                   combo_description: Optional[str] = None
                                   ) -> Dict[str, Any]:
        """Update alpha properties (name, color, tags, descriptions)."""
        await self.ensure_authenticated()
        
        try:
            payload = {
                "color": color,
                "name": name,
                "tags": tags if tags is not None else [],
                "regular": {"description": descriptions}
            }
            if selection_description is not None:
                payload["selection"] = {"description": selection_description}
            if combo_description is not None:
                payload["combo"] = {"description": combo_description}
            
            response = await self._request('PATCH', f"{self.base_url}/alphas/{alpha_id}", json=payload)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            self.log(f"Failed to set alpha properties: {str(e)}", "ERROR")
            raise

    async def get_record_sets(self, alpha_id: str) -> Dict[str, Any]:
        """List available record sets for an alpha."""
        await self.ensure_authenticated()
        
        try:
            response = await self._request('GET', f"{self.base_url}/alphas/{alpha_id}/recordsets")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            self.log(f"Failed to get record sets: {str(e)}", "ERROR")
            raise

    async def get_record_set_data(self, alpha_id: str, record_set_name: str) -> Dict[str, Any]:
        """Get data from a specific record set."""
        await self.ensure_authenticated()
        
        try:
            response = await self._request('GET', f"{self.base_url}/alphas/{alpha_id}/recordsets/{record_set_name}")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            self.log(f"Failed to get record set data: {str(e)}", "ERROR")
            raise

    async def get_user_activities(self, user_id: str, grouping: Optional[str] = None) -> Dict[str, Any]:
        """Get user activity diversity data."""
        await self.ensure_authenticated()
        
        try:
            params = {}
            if grouping:
                params['grouping'] = grouping
            
            response = await self._request('GET', f"{self.base_url}/users/{user_id}/activities", params=params)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            self.log(f"Failed to get user activities: {str(e)}", "ERROR")
            raise

    async def get_pyramid_multipliers(self) -> Dict[str, Any]:
        """Get current pyramid multipliers showing BRAIN's encouragement levels."""
        await self.ensure_authenticated()
        
        try:
            response = await self._request('GET', f"{self.base_url}/users/self/activities/pyramid-multipliers")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            self.log(f"Failed to get pyramid multipliers: {str(e)}", "ERROR")
            raise

    async def get_pyramid_alphas(self, start_date: Optional[str] = None,
                               end_date: Optional[str] = None) -> Dict[str, Any]:
        """Get user's current alpha distribution across pyramid categories.
        Defaults to the current quarter if no dates are provided."""
        await self.ensure_authenticated()
        
        try:
            # Default to current quarter boundaries
            if not start_date or not end_date:
                now = datetime.utcnow()
                q_start_month = (now.month - 1) // 3 * 3 + 1
                quarter_start = datetime(now.year, q_start_month, 1)
                if q_start_month + 3 > 12:
                    quarter_end = datetime(now.year + 1, 1, 1)
                else:
                    quarter_end = datetime(now.year, q_start_month + 3, 1)
                if not start_date:
                    start_date = quarter_start.strftime("%Y-%m-%d")
                if not end_date:
                    end_date = quarter_end.strftime("%Y-%m-%d")

            params = {}
            if start_date:
                params["startDate"] = start_date
            if end_date:
                params["endDate"] = end_date

            cache_key = self._generate_cache_key('pyramid_alphas', params)
            cached_data = self._get_cached_data(cache_key)
            if cached_data:
                return {**cached_data, 'from_cache': True}

            try:
                timeout_seconds = max(
                    5,
                    int(os.environ.get("BRAIN_PYRAMID_ALPHAS_TIMEOUT_SECONDS", "15")),
                )
            except Exception:
                timeout_seconds = 15

            response = await self._request(
                'GET',
                f"{self.base_url}/users/self/activities/pyramid-alphas",
                params=params,
                timeout=timeout_seconds,
            )
            response.raise_for_status()
            data = response.json() if response.text else {}
            if isinstance(data, dict):
                data['from_cache'] = False
                self._set_cached_data(cache_key, data, ttl=3600)
            return data
        except Exception as e:
            self.log(f"Failed to get pyramid alphas: {str(e)}", "ERROR")
            raise

    async def get_user_competitions(self, user_id: Optional[str] = None) -> Dict[str, Any]:
        """Get list of competitions that the user is participating in."""
        await self.ensure_authenticated()
        
        try:
            if not user_id:
                # Get current user ID if not specified
                user_response = await self._request('GET', f"{self.base_url}/users/self")
                if user_response.status_code == 200:
                    user_data = user_response.json()
                    user_id = user_data.get('id')
                else:
                    user_id = 'self'
            
            response = await self._request('GET', f"{self.base_url}/users/{user_id}/competitions")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            self.log(f"Failed to get user competitions: {str(e)}", "ERROR")
            raise

    async def get_competition_details(self, competition_id: str) -> Dict[str, Any]:
        """Get detailed information about a specific competition."""
        await self.ensure_authenticated()
        
        try:
            response = await self._request('GET', f"{self.base_url}/competitions/{competition_id}")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            self.log(f"Failed to get competition details: {str(e)}", "ERROR")
            raise

    async def get_competition_agreement(self, competition_id: str) -> Dict[str, Any]:
        """Get the rules, terms, and agreement for a specific competition."""
        await self.ensure_authenticated()
        
        try:
            response = await self._request('GET', f"{self.base_url}/competitions/{competition_id}/agreement")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            self.log(f"Failed to get competition agreement: {str(e)}", "ERROR")
            raise

    async def get_platform_setting_options(self) -> Dict[str, Any]:
        """Get available instrument types, regions, delays, and universes with Redis caching (1 day TTL)."""
        await self.ensure_authenticated()
        
        try:
            # Generate cache key (no parameters needed as this endpoint returns fixed platform settings)
            cache_key = self._generate_cache_key('platform_settings', {})
            
            # Try to get from cache
            cached_data = self._get_cached_data(cache_key)
            if cached_data:
                return {**cached_data, 'from_cache': True}
            
            # Use OPTIONS method on simulations endpoint to get configuration options
            response = await self._request('OPTIONS', f"{self.base_url}/simulations")
            response.raise_for_status()
            
            # Parse the settings structure from the response
            settings_data = response.json()
            settings_options = settings_data['actions']['POST']['settings']['children']
            
            # Extract instrument configuration options
            instrument_type_data = {}
            region_data = {}
            universe_data = {}
            delay_data = {}
            neutralization_data = {}
            
            # Parse each setting type
            for key, setting in settings_options.items():
                if setting['type'] == 'choice':
                    if setting['label'] == 'Instrument type':
                        instrument_type_data = setting['choices']
                    elif setting['label'] == 'Region':
                        region_data = setting['choices']['instrumentType']
                    elif setting['label'] == 'Universe':
                        universe_data = setting['choices']['instrumentType']
                    elif setting['label'] == 'Delay':
                        delay_data = setting['choices']['instrumentType']
                    elif setting['label'] == 'Neutralization':
                        neutralization_data = setting['choices']['instrumentType']
            
            # Build comprehensive instrument options
            data_list = []
            
            for instrument_type in instrument_type_data:
                for region in region_data[instrument_type['value']]:
                    for delay in delay_data[instrument_type['value']]['region'][region['value']]:
                        row = {
                            'InstrumentType': instrument_type['value'],
                            'Region': region['value'],
                            'Delay': delay['value']
                        }
                        row['Universe'] = [
                            item['value'] for item in universe_data[instrument_type['value']]['region'][region['value']]
                        ]
                        row['Neutralization'] = [
                            item['value'] for item in neutralization_data[instrument_type['value']]['region'][region['value']]
                        ]
                        data_list.append(row)
            
            # Return structured data
            result = {
                'instrument_options': data_list,
                'total_combinations': len(data_list),
                'instrument_types': [item['value'] for item in instrument_type_data],
                'regions_by_type': {
                    item['value']: [r['value'] for r in region_data[item['value']]]
                    for item in instrument_type_data
                },
                'from_cache': False
            }
            
            # Cache the data (1 day TTL)
            self._set_cached_data(cache_key, result, ttl=604800)
            
            return result
            
        except Exception as e:
            self.log(f"Failed to get instrument options: {str(e)}", "ERROR")
            raise

    async def performance_comparison(self, alpha_id: str, competition: Optional[str] = None,
                                     team_id: Optional[str] = None) -> Dict[str, Any]:
        """Get before-and-after performance comparison data for an alpha.

        If a competition is provided, the competition-scoped endpoint is used;
        otherwise the user's own (self) alpha endpoint is used.
        """
        await self.ensure_authenticated()

        try:
            params = {"teamId": team_id}
            params = {k: v for k, v in params.items() if v is not None}

            if competition:
                url = f"{self.base_url}/competitions/{competition}/alphas/{alpha_id}/before-and-after-performance"
            else:
                url = f"{self.base_url}/users/self/alphas/{alpha_id}/before-and-after-performance"

            # The endpoint returns an empty body with a Retry-After header while
            # the comparison is being computed, then JSON once it is ready.
            return await self._request_json_with_retries(
                'GET', url, params=params, op_name="performance_comparison"
            )
        except Exception as e:
            self.log(f"Failed to get performance comparison: {str(e)}", "ERROR")
            raise

    async def expand_nested_data(self, data: List[Dict[str, Any]], preserve_original: bool = True) -> List[Dict[str, Any]]:
        """Flatten complex nested data structures into tabular format."""
        try:
            df = pd.json_normalize(data, sep='_')
            if preserve_original:
                original_df = pd.DataFrame(data)
                df = pd.concat([original_df, df], axis=1)
                df = df.loc[:,~df.columns.duplicated()]
            return df.to_dict(orient='records')
        except Exception as e:
            self.log(f"Failed to expand nested data: {str(e)}", "ERROR")
            raise

    async def get_documentation_page(self, page_id: str) -> Dict[str, Any]:
        """Retrieve detailed content of a specific documentation page/article."""
        await self.ensure_authenticated()
        
        try:
            response = await self._request('GET', f"{self.base_url}/tutorial-pages/{page_id}")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            self.log(f"Failed to get documentation page: {str(e)}", "ERROR")
            raise
