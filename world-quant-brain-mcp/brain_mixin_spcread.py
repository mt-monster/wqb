from __future__ import annotations
import json
import time
import asyncio
import logging
from typing import Dict, List, Optional, Any
import re
import base64
from bs4 import BeautifulSoup
from datetime import datetime
import os
import math
import random

import requests
import pandas as pd
from forum_functions import forum_client
logger = logging.getLogger("brain_api")

#: prod 相关性**单次阻塞轮询窗口**（秒）。唯一来源 = ``wqb.config.WAIT_THRESHOLDS``
#: 的 ``prod_corr_timeout_s``；MCP 包在这里留字面量是为了在 ``wqb`` 不可导入的宿主下
#: 仍能工作，两处一致性由 ``tests/unit/07_docs_skills/test_wait_thresholds.py`` 守护。
#:
#: 2026-10-28：120 → 240。一次**正常**的平台计算 180–200 s，120s 窗口会让每条真实
#: 查询都收在 ``pending``（锁白占满窗口、再叠 195s 冷却，端到端 ~300s 且多绕一轮）。
#: 240 = 200 上限 + 一个 30s 慢轮询台阶 + 抖动余量。
#: ⚠ 这个值只有一个定义：两处使用点都引用本常量（旧版另有独立的 ``120.0``，改窗口会漏改）。
_PROD_CORR_WAIT_S = 240


class SpcDataMixin:
    def _spc_isin_checksum_valid(self, isin: str) -> bool:
        expanded = ""
        for char in isin:
            if char.isdigit():
                expanded += char
            elif "A" <= char <= "Z":
                expanded += str(ord(char) - ord("A") + 10)
            else:
                return False
        total = 0
        double = False
        for digit_char in reversed(expanded):
            digit = int(digit_char)
            if double:
                digit *= 2
            total += digit // 10 + digit % 10
            double = not double
        return total % 10 == 0

    def _validate_spc_sample_output(self, sample_output: str) -> List[str]:
        """Validate an SPC sample output string against the competition contract.

        Checks: parseable JSON object, ISIN|MIC key format, ISIN checksum,
        numeric confidence scores within [-1, 1]. Returns a list of error strings.
        """
        errors: List[str] = []
        stripped = (sample_output or "").strip()
        if not stripped:
            return ["sample_output is empty"]
        if stripped.startswith("```") or stripped.endswith("```"):
            errors.append("sample_output contains markdown code fences; must be pure JSON")
        try:
            data = json.loads(stripped)
        except json.JSONDecodeError as exc:
            errors.append(f"sample_output is not valid JSON: {exc.msg} at line {exc.lineno}, column {exc.colno}")
            return errors
        if not isinstance(data, dict):
            errors.append("sample_output top-level value must be a JSON object")
            return errors
        if not data:
            errors.append("sample_output object must not be empty")
        for key, value in data.items():
            if not self._SPC_ISIN_MIC_RE.match(str(key)):
                errors.append(f"invalid key format, expected ISIN|MIC: {key!r}")
                continue
            isin = str(key).split("|", 1)[0]
            if not self._spc_isin_checksum_valid(isin):
                errors.append(f"invalid ISIN checksum: {isin}")
            if isinstance(value, bool) or not isinstance(value, (int, float)):
                errors.append(f"confidence score must be numeric for {key!r}")
            elif not math.isfinite(value):
                errors.append(f"confidence score must be finite for {key!r}")
            elif value < -1.0 or value > 1.0:
                errors.append(f"confidence score out of [-1, 1] for {key!r}: {value}")
        return errors

    def _validate_spc_fields(
        self,
        name: Optional[str] = None,
        prompt: Optional[str] = None,
        model: Optional[str] = None,
        weight: Optional[float] = None,
        update_frequency: Optional[str] = None,
    ) -> List[str]:
        """Validate SPC submission metadata fields. Only non-None fields are checked."""
        errors: List[str] = []
        if name is not None and len(name) > 200:
            errors.append(f"name exceeds 200 characters ({len(name)})")
        if prompt is not None:
            if not prompt.strip():
                errors.append("prompt is empty")
            if len(prompt) > 10000:
                errors.append(f"prompt exceeds 10000 characters ({len(prompt)})")
        if model is not None and model not in self.SPC_MODELS:
            errors.append(f"model must be one of {list(self.SPC_MODELS)}, got {model!r}")
        if update_frequency is not None and update_frequency not in self.SPC_FREQUENCIES:
            errors.append(f"update_frequency must be one of {list(self.SPC_FREQUENCIES)}, got {update_frequency!r}")
        if weight is not None and not (0.0 <= float(weight) <= 1.0):
            errors.append(f"weight must be between 0 and 1, got {weight}")
        return errors

    async def get_spc_submissions(self, limit: int = 50, offset: int = 0) -> Dict[str, Any]:
        """List the current user's SPC prompt submissions."""
        await self.ensure_authenticated()
        try:
            response = await self._request(
                'GET',
                f"{self.base_url}/competitions/spc/submissions",
                params={"limit": limit, "offset": offset},
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            self.log(f"Failed to get SPC submissions: {str(e)}", "ERROR")
            raise

    async def create_spc_submission(
        self,
        name: str,
        prompt: str,
        sample_output: str,
        model: str,
        model_version: str,
        weight: float,
        update_frequency: str,
        skip_validation: bool = False,
    ) -> Dict[str, Any]:
        """Create a new SPC prompt submission."""
        await self.ensure_authenticated()
        if not skip_validation:
            errors = self._validate_spc_fields(name, prompt, model, weight, update_frequency)
            errors += self._validate_spc_sample_output(sample_output)
            if errors:
                return {
                    "error": "Local validation failed; nothing was submitted",
                    "validation_errors": errors,
                    "hint": "Fix the errors or pass skip_validation=true to submit anyway",
                }
        payload = {
            "name": name,
            "prompt": prompt,
            "sampleOutput": sample_output,
            "model": model,
            "modelVersion": model_version,
            "weight": round(float(weight), 2),
            "updateFrequency": update_frequency,
        }
        try:
            response = await self._request(
                'POST', f"{self.base_url}/competitions/spc/submissions", json=payload
            )
            if response.status_code == 400:
                return {"error": "Server rejected the submission", "details": self._response_payload(response)}
            response.raise_for_status()
            return response.json()
        except Exception as e:
            self.log(f"Failed to create SPC submission: {str(e)}", "ERROR")
            raise

    async def set_spc_submission_weight(self, submission_id: str, weight: float) -> Dict[str, Any]:
        """Set the weight of an existing SPC submission. weight=0 withdraws the prompt.

        The API only allows changing weight after creation; all other fields are
        immutable. To change a prompt's content, create a new submission and set
        the old one's weight to 0.
        """
        await self.ensure_authenticated()
        errors = self._validate_spc_fields(weight=weight)
        if errors:
            return {"error": "Local validation failed; nothing was updated", "validation_errors": errors}
        try:
            response = await self._request(
                'PATCH',
                f"{self.base_url}/competitions/spc/submissions/{submission_id}",
                json={"weight": round(float(weight), 2)},
            )
            if response.status_code == 400:
                return {"error": "Server rejected the update", "details": self._response_payload(response)}
            response.raise_for_status()
            return response.json()
        except Exception as e:
            self.log(f"Failed to update SPC submission {submission_id}: {str(e)}", "ERROR")
            raise

    async def get_spc_leaderboard(
        self,
        board: Optional[str] = None,
        limit: int = 30,
        offset: int = 0,
        aggregate: str = "user",
    ) -> Dict[str, Any]:
        """Get the SPC leaderboard. board is a month key like '202607' (defaults to current month server-side)."""
        await self.ensure_authenticated()
        params: Dict[str, Any] = {"limit": limit, "offset": offset, "aggregate": aggregate}
        if board:
            params["board"] = board
        try:
            response = await self._request(
                'GET', f"{self.base_url}/consultant/boards/spc", params=params
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            self.log(f"Failed to get SPC leaderboard: {str(e)}", "ERROR")
            raise

    def _is_atom(self, detail: Optional[Dict[str, Any]]) -> bool:
        """Match atom detection used in extract_regular_alphas.py:
        - Primary signal: 'classifications' entries containing 'SINGLE_DATA_SET'
        - Fallbacks: tags list contains 'atom' or classification id/name contains 'ATOM'
        """
        if not detail or not isinstance(detail, dict):
            return False

        classifications = detail.get('classifications') or []
        for c in classifications:
            cid = (c.get('id') or c.get('name') or '')
            if isinstance(cid, str) and 'SINGLE_DATA_SET' in cid:
                return True

        # Fallbacks
        tags = detail.get('tags') or []
        if isinstance(tags, list):
            for t in tags:
                if isinstance(t, str) and t.strip().lower() == 'atom':
                    return True

        for c in classifications:
            cid = (c.get('id') or c.get('name') or '')
            if isinstance(cid, str) and 'ATOM' in cid.upper():
                return True

        return False

    async def value_factor_trendScore(self, start_date: str, end_date: str) -> Dict[str, Any]:
        """Compute diversity score for regular alphas in a date range.

        Description:
        This function calculate the diversity of the users' submission, by checking the diversity, we can have a good understanding on the valuefactor's trend.
        value factor of a user is defiend by This diversity score, which measures three key aspects of work output: the proportion of works
        with the "Atom" tag (S_A), atom proportion, the breadth of pyramids covered (S_P), and how evenly works
        are distributed across those pyramids (S_H). Calculated as their product, it rewards
        strong performance across all three dimensions—encouraging more Atom-tagged works,
        wider pyramid coverage, and balanced distribution—with weaknesses in any area lowering
        the total score significantly.

        Inputs (hints for AI callers):
        - start_date (str): ISO UTC start datetime, e.g. '2025-08-14T00:00:00Z'
        - end_date (str): ISO UTC end datetime, e.g. '2025-08-18T23:59:59Z'
        - Note: this tool always uses 'OS' (submission dates) to define the window; callers do not need to supply a stage.
                - Note: P_max (total number of possible pyramids) is derived from the platform
                    pyramid-multipliers endpoint and not supplied by callers.

        Returns (compact JSON): {
            'diversity_score': float,
            'N': int,  # total regular alphas in window
            'A': int,  # number of Atom-tagged works (is_single_data_set)
            'P': int,  # pyramid coverage count in the sample
            'P_max': int, # used max for normalization
            'S_A': float, 'S_P': float, 'S_H': float,
            'per_pyramid_counts': {pyramid_name: count}
        }
        """
        # Fetch user alphas (always use OS / submission dates per product policy)
        await self.ensure_authenticated()
        alphas_resp = await self.get_user_alphas(stage='OS', limit=500, submission_start_date=start_date, submission_end_date=end_date)

        if not isinstance(alphas_resp, dict) or 'results' not in alphas_resp:
            return {'error': 'Unexpected response from get_user_alphas', 'raw': alphas_resp}

        alphas = alphas_resp['results']
        regular = [a for a in alphas if a.get('type') == 'REGULAR']

        # Fetch details for each regular alpha
        pyramid_list = []
        atom_count = 0
        per_pyramid = {}
        for a in regular:
            try:
                detail = await self.get_alpha_details(a.get('id'))
            except Exception:
                continue

            is_atom = self._is_atom(detail)
            if is_atom:
                atom_count += 1

            # Extract pyramids
            ps = []
            if isinstance(detail.get('pyramids'), list):
                ps = [p.get('name') for p in detail.get('pyramids') if p.get('name')]
            else:
                pt = detail.get('pyramidThemes') or {}
                pss = pt.get('pyramids') if isinstance(pt, dict) else None
                if pss and isinstance(pss, list):
                    ps = [p.get('name') for p in pss if p.get('name')]

            for p in ps:
                pyramid_list.append(p)
                per_pyramid[p] = per_pyramid.get(p, 0) + 1

        N = len(regular)
        A = atom_count
        P = len(per_pyramid)

        # Determine P_max similarly to the script: use pyramid multipliers if available
        P_max = None
        try:
            pm = await self.get_pyramid_multipliers()
            if isinstance(pm, dict) and 'pyramids' in pm:
                pyramids_list = pm.get('pyramids') or []
                P_max = len(pyramids_list)
        except Exception:
            P_max = None

        if not P_max or P_max <= 0:
            P_max = max(P, 1)

        # Component scores
        S_A = (A / N) if N > 0 else 0.0
        S_P = (P / P_max) if P_max > 0 else 0.0

        # Entropy
        S_H = 0.0
        if P <= 1 or not per_pyramid:
            S_H = 0.0
        else:
            total_occ = sum(per_pyramid.values())
            H = 0.0
            for cnt in per_pyramid.values():
                q = cnt / total_occ if total_occ > 0 else 0
                if q > 0:
                    H -= q * math.log2(q)
            max_H = math.log2(P) if P > 0 else 1
            S_H = (H / max_H) if max_H > 0 else 0.0

        diversity_score = S_A * S_P * S_H

        return {
            'diversity_score': diversity_score,
            'N': N,
            'A': A,
            'P': P,
            'P_max': P_max,
            'S_A': S_A,
            'S_P': S_P,
            'S_H': S_H,
            'per_pyramid_counts': per_pyramid
        }

    async def get_operators(self) -> Dict[str, Any]:
        """Get available operators for alpha creation."""
        await self.ensure_authenticated()
        
        try:
            response = await self._request('GET', f"{self.base_url}/operators")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            self.log(f"Failed to get operators: {str(e)}", "ERROR")
            raise

    async def recommend_datasets(self, region: str = "USA", delay: int = 1,
                                  universe: str = "TOP3000", top_n: int = 20) -> Dict[str, Any]:
        """Recommend datasets with unlit pyramid priority and in-pyramid quality ranking.

        The ranking favors datasets from unlit pyramids first. Within those
        pyramids it prefers high OS/IS Sharpe, high dataset userCount, and high
        dataset alphaCount, with a small random component to avoid returning the
        exact same list on every call.
        """
        await self.ensure_authenticated()

        def _category_id(value: Any) -> str:
            if isinstance(value, dict):
                return str(value.get('id') or '')
            return str(value or '')

        def _category_name(value: Any) -> str:
            if isinstance(value, dict):
                return str(value.get('name') or value.get('id') or '')
            return str(value or '')

        def _as_float(value: Any, default: float = 0.0) -> float:
            try:
                if value is None:
                    return default
                return float(value)
            except (TypeError, ValueError):
                return default

        def _as_int(value: Any, default: int = 0) -> int:
            try:
                if value is None:
                    return default
                return int(float(value))
            except (TypeError, ValueError):
                return default

        def _rank_score(value: Optional[float], values: List[float], points: float) -> float:
            """Return 0..points based on value's rank in the supplied sample."""
            if value is None or not values:
                return 0.0
            sorted_values = sorted(values)
            if len(sorted_values) == 1:
                return points
            below_or_equal = sum(1 for item in sorted_values if item <= value)
            percentile = (below_or_equal - 1) / (len(sorted_values) - 1)
            return points * max(0.0, min(1.0, percentile))

        def _log_score(value: int, values: List[int], points: float) -> float:
            if not values:
                return 0.0
            log_values = [math.log1p(max(0, item)) for item in values]
            return _rank_score(math.log1p(max(0, value)), log_values, points)

        def _region_delay_match(item: Dict[str, Any]) -> bool:
            return item.get('region') == region and _as_int(item.get('delay'), -1) == delay

        def _platform_row_match(item: Dict[str, Any], require_universe: bool = True) -> bool:
            if item.get('InstrumentType') != 'EQUITY':
                return False
            if item.get('Region') != region:
                return False
            if _as_int(item.get('Delay'), -1) != delay:
                return False
            if not require_universe:
                return True
            return universe in (item.get('Universe') or [])

        # ---- 1. Fetch pyramid status from the platform's pyramid endpoints ----
        pyramid_alphas: Dict[str, Any] = {}
        pyramid_multipliers: Dict[str, Any] = {}
        try:
            pyramid_alphas, pyramid_multipliers = await asyncio.gather(
                self.get_pyramid_alphas(),
                self.get_pyramid_multipliers(),
            )
        except Exception as e:
            self.log(f"Failed to fetch pyramid status: {e}", "WARNING")

        pyramid_summary: Dict[str, Dict[str, Any]] = {}
        for item in pyramid_multipliers.get('pyramids', []):
            if not isinstance(item, dict) or not _region_delay_match(item):
                continue
            cat_obj = item.get('category', {})
            cat_id = _category_id(cat_obj)
            if not cat_id:
                continue
            pyramid_summary[cat_id] = {
                'category_id': cat_id,
                'category_name': _category_name(cat_obj),
                'alpha_count': 0,
                'need_to_light': 3,
                'lit': False,
                'multiplier': _as_float(item.get('multiplier'), 1.0),
            }

        for item in pyramid_alphas.get('pyramids', []):
            if not isinstance(item, dict) or not _region_delay_match(item):
                continue
            cat_obj = item.get('category', {})
            cat_id = _category_id(cat_obj)
            if not cat_id:
                continue
            alpha_count = _as_int(item.get('alphaCount'), 0)
            pyramid_summary.setdefault(cat_id, {
                'category_id': cat_id,
                'category_name': _category_name(cat_obj),
                'multiplier': 1.0,
            })
            pyramid_summary[cat_id].update({
                'category_name': pyramid_summary[cat_id].get('category_name') or _category_name(cat_obj),
                'alpha_count': alpha_count,
                'need_to_light': max(0, 3 - alpha_count),
                'lit': alpha_count >= 3,
            })

        # ---- 2. Fetch available datasets for this region/delay ----
        datasets_resp = await self.get_datasets(region=region, delay=delay, universe=universe)
        all_datasets = datasets_resp.get('results', [])
        if not all_datasets:
            return {'error': 'No datasets available for the given region/delay/universe'}

        # ---- 2.1. Fetch neutralization options for the same simulation settings ----
        neutralization_options: List[str] = []
        neutralization_info: Dict[str, Any] = {
            'instrument_type': 'EQUITY',
            'region': region,
            'delay': delay,
            'universe': universe,
            'options': neutralization_options,
            'available': False,
            'source': 'platform_setting_options',
        }
        try:
            platform_options = await self.get_platform_setting_options()
            setting_rows = platform_options.get('instrument_options', [])
            matching_rows = [
                item for item in setting_rows
                if isinstance(item, dict) and _platform_row_match(item)
            ]
            universe_matched = True
            if not matching_rows:
                matching_rows = [
                    item for item in setting_rows
                    if isinstance(item, dict) and _platform_row_match(item, require_universe=False)
                ]
                universe_matched = False

            neutralization_options = sorted({
                str(option)
                for row in matching_rows
                for option in (row.get('Neutralization') or [])
                if option
            })
            available_universes = sorted({
                str(option)
                for row in matching_rows
                for option in (row.get('Universe') or [])
                if option
            })
            neutralization_info.update({
                'options': neutralization_options,
                'available': bool(neutralization_options),
                'universe_matched': universe_matched,
                'available_universes': available_universes,
            })
        except Exception as e:
            self.log(f"Failed to fetch neutralization options for dataset recommendations: {e}", "WARNING")
            neutralization_info.update({
                'error': str(e),
                'available': False,
            })

        for ds in all_datasets:
            cat_obj = ds.get('category', {})
            cat_id = _category_id(cat_obj)
            if not cat_id:
                continue
            pyramid_summary.setdefault(cat_id, {
                'category_id': cat_id,
                'category_name': _category_name(cat_obj),
                'alpha_count': 0,
                'need_to_light': 3,
                'lit': False,
                'multiplier': _as_float(ds.get('pyramidMultiplier'), 1.0),
            })

        # ---- 3. Load dataset quality from OS/IS Sharpe (info_data.bin) ----
        region_key = f"{region}_{delay}"
        isos_info = self._isos_data.get(region_key, {}).get('isos', {}) if self._isos_data else {}
        dataset_sharpe_map = isos_info.get('dataset', {})

        datasets_by_category: Dict[str, List[Dict[str, Any]]] = {}
        for ds in all_datasets:
            cat_id = _category_id(ds.get('category', {}))
            datasets_by_category.setdefault(cat_id, []).append(ds)

        sharpe_values_by_category: Dict[str, List[float]] = {}
        user_counts_by_category: Dict[str, List[int]] = {}
        alpha_counts_by_category: Dict[str, List[int]] = {}
        for cat_id, datasets in datasets_by_category.items():
            for ds in datasets:
                ds_id = ds.get('id', '')
                ds_sharpe_info = dataset_sharpe_map.get(ds_id, {})
                ds_sharpe = ds_sharpe_info.get('sharpe_ratio') if isinstance(ds_sharpe_info, dict) else None
                if ds_sharpe is not None:
                    sharpe_values_by_category.setdefault(cat_id, []).append(_as_float(ds_sharpe))
                user_counts_by_category.setdefault(cat_id, []).append(_as_int(ds.get('userCount'), 0))
                alpha_counts_by_category.setdefault(cat_id, []).append(_as_int(ds.get('alphaCount'), 0))

        unlit_categories = {cat_id for cat_id, item in pyramid_summary.items() if not item.get('lit')}
        restrict_to_unlit = any(
            _category_id(ds.get('category', {})) in unlit_categories
            for ds in all_datasets
        )
        candidate_datasets = [
            ds for ds in all_datasets
            if not restrict_to_unlit or _category_id(ds.get('category', {})) in unlit_categories
        ]

        # ---- 4. Score each dataset ----
        scored_datasets = []
        max_multiplier = max(
            [_as_float(item.get('multiplier'), 1.0) for item in pyramid_summary.values()] or [1.0]
        )
        for ds in candidate_datasets:
            ds_id = ds.get('id', '')
            ds_name = ds.get('name', ds_id)
            cat_obj = ds.get('category', {})
            ds_category = _category_id(cat_obj)
            ds_category_name = _category_name(cat_obj)
            sub_obj = ds.get('subcategory', {})
            ds_subcategory = _category_id(sub_obj)
            pyramid = pyramid_summary.get(ds_category, {})

            # --- Pyramid lighting score (0~40 points) ---
            cat_lit = bool(pyramid.get('lit', False))
            cat_count = _as_int(pyramid.get('alpha_count'), 0)
            need = _as_int(pyramid.get('need_to_light'), max(0, 3 - cat_count))
            multiplier = _as_float(pyramid.get('multiplier'), _as_float(ds.get('pyramidMultiplier'), 1.0))
            if not cat_lit:
                need_score = 24.0 * (need / 3.0)
                multiplier_score = 16.0 * (multiplier / max(max_multiplier, 1.0))
                pyramid_score = min(40.0, need_score + multiplier_score)
            else:
                pyramid_score = 5.0 * (multiplier / max(max_multiplier, 1.0))

            # --- Quality score from OS/IS Sharpe (0~30 points) ---
            ds_sharpe_info = dataset_sharpe_map.get(ds_id, {})
            ds_sharpe = ds_sharpe_info.get('sharpe_ratio') if isinstance(ds_sharpe_info, dict) else None
            ds_sharpe_float = _as_float(ds_sharpe) if ds_sharpe is not None else None
            ds_os_count = _as_int(ds_sharpe_info.get('count'), 0) if isinstance(ds_sharpe_info, dict) else 0
            quality_score = _rank_score(
                ds_sharpe_float,
                sharpe_values_by_category.get(ds_category, []),
                30.0,
            )

            # --- Dataset popularity: prefer more users and more submitted alphas (0~20 points) ---
            ds_user_count = _as_int(ds.get('userCount'), 0)
            ds_alpha_count = _as_int(ds.get('alphaCount'), 0)
            usage_score = _log_score(
                ds_user_count,
                user_counts_by_category.get(ds_category, []),
                10.0,
            )
            submission_score = _log_score(
                ds_alpha_count,
                alpha_counts_by_category.get(ds_category, []),
                10.0,
            )

            # --- Controlled randomness (0~5 points) ---
            random_score = random.uniform(0.0, 5.0)
            total_score = pyramid_score + quality_score + usage_score + submission_score + random_score

            scored_datasets.append({
                'dataset_id': ds_id,
                'dataset_name': ds_name,
                'category': ds_category,
                'category_name': ds_category_name,
                'subcategory': ds_subcategory,
                'total_score': round(total_score, 2),
                'pyramid_score': round(pyramid_score, 2),
                'quality_score': round(quality_score, 2),
                'usage_score': round(usage_score, 2),
                'submission_score': round(submission_score, 2),
                'random_score': round(random_score, 2),
                'distribution_score': round(usage_score + submission_score, 2),
                'category_lit': cat_lit,
                'category_alpha_count': cat_count,
                'category_need_to_light': need,
                'pyramid_multiplier': multiplier,
                'dataset_user_count': ds_user_count,
                'dataset_alpha_count': ds_alpha_count,
                'dataset_submissions_this_quarter': None,
                'os_is_sharpe': round(ds_sharpe_float, 4) if ds_sharpe_float is not None else None,
                'os_is_count': ds_os_count,
                'neutralization_options': neutralization_options,
                'neutralization_info': neutralization_info,
            })

        # Sort by total_score descending
        scored_datasets.sort(key=lambda x: x['total_score'], reverse=True)

        lit_count = sum(1 for item in pyramid_summary.values() if item.get('lit'))
        unlit_count = sum(1 for item in pyramid_summary.values() if not item.get('lit'))
        unlit_category_ids = sorted([cat_id for cat_id, item in pyramid_summary.items() if not item.get('lit')])

        return {
            'region': region,
            'delay': delay,
            'universe': universe,
            'neutralization_options': neutralization_options,
            'neutralization_info': neutralization_info,
            'recommendations': scored_datasets[:top_n],
            'total_datasets_scored': len(scored_datasets),
            'total_available_datasets': len(all_datasets),
            'total_candidate_datasets': len(candidate_datasets),
            'restricted_to_unlit_categories': restrict_to_unlit,
            'category_summary': pyramid_summary,
            'pyramid_summary': pyramid_summary,
            'pyramid_status': {
                'lit_categories': lit_count,
                'unlit_categories': unlit_count,
                'total_categories': lit_count + unlit_count,
                'unlit_category_ids': unlit_category_ids,
            },
            'scoring_weights': {
                'pyramid_lighting': '0~40 pts (unlit pyramids get priority; higher multiplier helps)',
                'dataset_quality': '0~30 pts (higher OS/IS Sharpe rank within the same pyramid)',
                'dataset_usage': '0~10 pts (higher dataset userCount rank within the same pyramid)',
                'dataset_submissions': '0~10 pts (higher dataset alphaCount rank within the same pyramid)',
                'randomness': '0~5 pts (small random jitter for exploration)',
            }
        }

    async def run_selection(
        self,
        selection: str,
        instrument_type: str = "EQUITY",
        region: str = "USA",
        delay: int = 1,
        selection_limit: int = 1000,
        selection_handling: str = "POSITIVE"
    ) -> Dict[str, Any]:
        """Run a selection query to filter instruments."""
        await self.ensure_authenticated()
        
        try:
            selection_data = {
                "selection": selection,
                "instrumentType": instrument_type,
                "region": region,
                "delay": delay,
                "selectionLimit": selection_limit,
                "selectionHandling": selection_handling
            }
            
            response = await self._request('GET', f"{self.base_url}/simulations/super-selection", params=selection_data)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            self.log(f"Failed to run selection: {str(e)}", "ERROR")
            raise

    async def get_user_profile(self, user_id: str = "self") -> Dict[str, Any]:
        """Get user profile information."""
        await self.ensure_authenticated()
        
        try:
            response = await self._request('GET', f"{self.base_url}/users/{user_id}")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            self.log(f"Failed to get user profile: {str(e)}", "ERROR")
            raise

    async def get_documentations(self) -> Dict[str, Any]:
        """Get available documentations and learning materials."""
        await self.ensure_authenticated()
        
        try:
            response = await self._request('GET', f"{self.base_url}/tutorials")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            self.log(f"Failed to get documentations: {str(e)}", "ERROR")
            raise

    async def get_messages(self, limit: Optional[int] = None, offset: int = 0) -> Dict[str, Any]:
        """Get messages for the current user with optional pagination.
        
        This function retrieves messages, processes their descriptions to extract
        and format embedded JSON, and handles file attachments by saving them locally.
        """
        from typing import Tuple
        
        def process_description(desc: str, message_id: str) -> Tuple[str, List[str]]:
            """
            Processes message description to handle HTML, embedded images, and JSON.
            """
            attachments = []
            
            # Handle embedded images
            soup = BeautifulSoup(desc, 'html.parser')
            for idx, img_tag in enumerate(soup.find_all('img')):
                src = img_tag.get('src', '')
                if src.startswith('data:image'):
                    try:
                        # Extract image data
                        header, encoded = src.split(',', 1)
                        ext = header.split(';')[0].split('/')[1]
                        safe_ext = re.sub(r'[^a-zA-Z0-9]', '', ext)
                        
                        # Decode and save image
                        content = base64.b64decode(encoded)
                        file_name = f"{message_id}_img_{idx}.{safe_ext}"
                        with open(file_name, "wb") as f:
                            f.write(content)
                        
                        # Update HTML and add attachment info
                        img_tag['src'] = file_name
                        attachments.append(f"Saved embedded image to ./{file_name}")
                        
                    except Exception as e:
                        attachments.append(f"Could not process embedded image: {e}")
            
            desc = str(soup)

            # Handle JSON content
            try:
                json_part_match = re.search(r'```json\n({.*?})\n```', desc, re.DOTALL)
                if json_part_match:
                    json_str = json_part_match.group(1)
                    desc = desc.replace(json_part_match.group(0), "").strip()
                    
                    try:
                        data = json.loads(json_str)
                        formatted_json = json.dumps(data, indent=2)
                        desc += f"\n\n---\n**Details**\n```json\n{formatted_json}\n```"
                    except json.JSONDecodeError:
                        desc += f"\n\n---\n**Details (raw)**\n{json_str}"
            except Exception:
                logging.getLogger(__name__).debug("swallowed exception", exc_info=True)
                
            return desc, attachments

        await self.ensure_authenticated()
        
        try:
            params = {"limit": limit, "offset": offset}
            params = {k: v for k, v in params.items() if v is not None}
            
            response = await self._request('GET', f"{self.base_url}/users/self/messages", params=params)
            response.raise_for_status()
            messages_data = response.json()
            
            # Process descriptions and attachments
            for msg in messages_data.get("results", []):
                try:
                    msg_id = msg.get("id", "unknown_id")
                    new_desc, attachments = process_description(msg.get("description", ""), msg_id)
                    msg["description"] = new_desc
                    if attachments:
                        msg["attachments_info"] = attachments
                except Exception as e:
                    self.log(f"Error processing message {msg.get('id')}: {e}", "ERROR")

            return messages_data
            
        except Exception as e:
            self.log(f"Failed to get messages: {str(e)}", "ERROR")
            raise

    async def get_glossary_terms(self, email: str, password: str) -> List[Dict[str, str]]:
        """Get glossary terms from forum."""
        try:
            return await forum_client.get_glossary_terms(email, password)
        except Exception as e:
            self.log(f"Failed to get glossary terms: {str(e)}", "ERROR")
            raise

    async def search_forum_posts(self, email: str, password: str, search_query: str, 
                                 max_results: int = 50) -> Dict[str, Any]:
        """Search forum posts."""
        try:
            rate_limited = await self._rate_limit_forum_op("search_forum_posts")
            if rate_limited:
                return {
                    **rate_limited,
                    'operation': 'search_forum_posts',
                    'search_query': search_query,
                    'max_results': max_results,
                }
            return await forum_client.search_forum_posts(email, password, search_query, max_results)
        except Exception as e:
            self.log(f"Failed to search forum posts: {str(e)}", "ERROR")
            raise

    async def read_forum_post(self, email: str, password: str, article_id: str, 
                              include_comments: bool = True) -> Dict[str, Any]:
        """Get forum post."""
        try:
            rate_limited = await self._rate_limit_forum_op("read_forum_post")
            if rate_limited:
                return {
                    **rate_limited,
                    'operation': 'read_forum_post',
                    'article_id': article_id,
                    'include_comments': include_comments,
                }
            return await forum_client.read_full_forum_post(email, password, article_id, include_comments)
        except Exception as e:
            self.log(f"Failed to read forum post: {str(e)}", "ERROR")
            raise

    async def get_alpha_yearly_stats(self, alpha_id: str) -> Dict[str, Any]:
        """Get yearly statistics for an alpha."""
        await self.ensure_authenticated()
        
        max_retries = 5
        retry_delay = 2
        
        for attempt in range(max_retries):
            try:
                self.log(f"Attempting to get yearly stats for alpha {alpha_id} (attempt {attempt + 1}/{max_retries})", "INFO")
                
                response = await self._request('GET', f"{self.base_url}/alphas/{alpha_id}/recordsets/yearly-stats")
                response.raise_for_status()
                
                text = (response.text or "").strip()
                if not text:
                    if attempt < max_retries - 1:
                        self.log(f"Empty yearly stats response for {alpha_id}, retrying...", "WARNING")
                        await asyncio.sleep(retry_delay)
                        retry_delay *= 1.5
                        continue
                    else:
                        return {}
                
                try:
                    stats_data = response.json()
                    if stats_data:
                        return stats_data
                    else:
                        if attempt < max_retries - 1:
                            self.log(f"Empty yearly stats JSON for {alpha_id}, retrying...", "WARNING")
                            await asyncio.sleep(retry_delay)
                            retry_delay *= 1.5
                            continue
                        else:
                            return {}
                            
                except json.JSONDecodeError as parse_err:
                    if attempt < max_retries - 1:
                        self.log(f"Yearly stats JSON parse failed for {alpha_id}, retrying...", "WARNING")
                        await asyncio.sleep(retry_delay)
                        retry_delay *= 1.5
                        continue
                    else:
                        raise
                        
            except requests.RequestException as e:
                if attempt < max_retries - 1:
                    self.log(f"Failed to get yearly stats for {alpha_id}, retrying: {e}", "WARNING")
                    await asyncio.sleep(retry_delay)
                    retry_delay *= 1.5
                    continue
                else:
                    raise
        
        return {}

    async def _read_existing_prod_correlation(self, alpha_id: str,
                                              quiet: bool = False) -> Optional[Dict[str, Any]]:
        """**只读**：从 alpha 详情取平台已算好的 prod 相关（不占锁、不触发计算）。

        2026-10-26 新增。动机：平台的账号级 correlation 单槽经常被"对早已算完的 alpha
        反复触发计算"占满。先读 ``is.prodCorrelation`` 能直接拿到已算结果，
        完全绕开锁与平台队列。

        返回 ``None`` 表示平台尚未算出（调用方应回退到"触发计算"路径）。

        2026-10-28：改走 ``_request``（to_thread + 信号量 + asyncio 超时包装）。
        旧实现直接 ``self.session.get`` 是全包唯一在事件循环上阻塞的 HTTP 调用
        （最长 15s），HTTP 常驻服务下会卡住所有并发工具调用。
        ``quiet=True``：等待/轮询路径反复预读时不刷日志（P1-1 / P0-2）。
        """
        try:
            r = await self._request(
                'GET', f"{self.base_url}/alphas/{alpha_id}", timeout=15
            )
        except Exception:  # noqa: BLE001 — 预读是 best-effort，任何失败都回退主路径
            return None
        if getattr(r, "status_code", 0) != 200:
            return None
        try:
            j = r.json()
        except Exception:
            return None
        if not isinstance(j, dict):
            return None
        is_ = j.get("is")
        if not isinstance(is_, dict):
            return None
        mx = is_.get("prodCorrelation")
        if mx is None:
            return None
        try:
            mx = float(mx)
        except (TypeError, ValueError):
            return None
        if not quiet:
            self.log(f"[prod-corr] {alpha_id} 命中平台已算值 prod={mx}（未占锁、未触发计算）", "INFO")
        return {
            "status": "ok",
            "alpha_id": alpha_id,
            "max": mx,
            "records": [],
            "source": "alpha_detail_cached",
            "message": "从 alpha 详情读取平台已算好的 prod 相关（未触发新计算）",
        }

    # ── prod 相关性计时 / 同 alpha 等待（2026-10-28 P0-1 / P0-2 / P1-1 / P2-8）──

    def _corr_log_timing(self, event: str, alpha_id: str, t0: float, **fields) -> None:
        """结构化打点：``[corr-t] {"event":..., ...}``。

        只放可聚合的标量，供 ``tools/probe/corr_timing_report.py`` 从 MCP 日志
        统计「查一次 prod 到底花了多少时间、花在哪」。解析侧在
        ``wqb.corr_timing``，两边字段名必须一致（守护测试比对）。
        """
        payload = {"event": event, "alpha": str(alpha_id), "pid": os.getpid(),
                   "ts": time.strftime("%Y-%m-%dT%H:%M:%S")}
        try:
            payload["elapsed_ms"] = int(max(0.0, time.time() - t0) * 1000)
        except Exception:
            pass
        for k, v in fields.items():
            if v is None or isinstance(v, (int, float, str, bool)):
                payload[k] = v
        try:
            self.log(f"[corr-t] {json.dumps(payload, ensure_ascii=False, sort_keys=True)}", "INFO")
        except Exception:
            pass

    def _corr_join_wait_seconds(self) -> float:
        """同 alpha 等待上限（秒）。缺省 25s ≈ 平台典型耗时的一个快轮询周期。

        设 0 关闭等待（回到 2026-10-28 之前的「立即 busy」语义）。
        """
        try:
            return max(0.0, float(os.environ.get("WQB_CORR_JOIN_WAIT_SEC", "25")))
        except (TypeError, ValueError):
            return 25.0

    @staticmethod
    def _corr_holder_is_alpha(holder, op_name: str) -> bool:
        """``holder`` 是 lock token 的 tag（``corr:<op_name>``），精确比对。"""
        return bool(holder) and str(holder) == f"corr:{op_name}"

    async def _await_same_alpha_value(self, alpha_id: str, wait_s: float) -> Optional[Dict[str, Any]]:
        """等同一 alpha 正在算的结果：**只预读，不再触发**（P0-2 / P1-1）。

        每 5s 读一次 ``is.prodCorrelation``（不占锁、零平台计算成本），拿到即返回。
        返回 ``None`` 表示等待窗口内没等到——调用方应回 busy/pending，而不是重触发。
        """
        if wait_s <= 0:
            return None
        deadline = time.time() + wait_s
        interval = 5.0
        while True:
            r = await self._read_existing_prod_correlation(alpha_id, quiet=True)
            if r is not None:
                r["joined"] = True
                return r
            remain = deadline - time.time()
            if remain <= 0:
                return None
            await asyncio.sleep(min(interval, remain))

    def _corr_release_plan(self, result: Optional[Dict[str, Any]]):
        """P0-1：按本次结果决定释放槽时**是否写冷却 / 写多久**。返回 ``(cooldown, seconds)``。

        | 结果 | 平台状态 | 冷却 |
        |---|---|---|
        | success（拿到值） | 槽已可用 | 仅 ``COOLDOWN_SETTLE_SEC``（5s）收尾 |
        | pending（轮询超时） | 大概率仍在算 | 平台 Retry-After 或 195s |
        | data_unavailable（4xx 终态） | 没有占槽理由 | 不写 |
        | 异常 / 未知 | 说不清 | 不写（inflight 标记兜重复触发） |

        旧实现无条件写 195s：一次「一个 GET 就拿到既有值」也被罚 3 分钟，
        吞吐被压到 ~4 alpha/小时（`reports/prod_corr_timing_20261028.md`）。
        """
        try:
            from wqb.correlation_slot import COOLDOWN_SEC_DEFAULT, settle_seconds
            _settle = settle_seconds()
        except Exception:  # pragma: no cover
            COOLDOWN_SEC_DEFAULT, _settle = 195.0, 5.0
        if not isinstance(result, dict):
            return False, None
        status = result.get("status")
        if status == "pending":
            try:
                ra = float(result.get("platform_retry_after") or 0.0)
            except (TypeError, ValueError):
                ra = 0.0
            return True, (ra if 0 < ra <= COOLDOWN_SEC_DEFAULT else None)
        if status == "ok":
            return True, _settle
        return False, None

    @staticmethod
    def _corr_retry_after_seconds(response) -> float:
        """读平台 ``Retry-After``（秒）。缺失/解析失败 → 0。"""
        try:
            raw = (getattr(response, "headers", None) or {}).get("Retry-After")
        except Exception:
            return 0.0
        if not raw:
            return 0.0
        try:
            return max(0.0, float(str(raw).strip()))
        except (TypeError, ValueError):
            return 0.0

    async def get_production_correlation(self, alpha_id: str,
                                         max_wait_seconds: float = None,
                                         use_pre_read: bool = True) -> Dict[str, Any]:
        """Get production correlation data for an alpha.

        Polls every 30 seconds for up to 1 hour by default to handle platform rate-limiting.
        For super alphas, the platform may return an empty body (HTTP 200) for a few
        minutes after simulation completes while it computes the correlation data.
        The polling loop handles this by retrying until data is available.
        Returns {'status': 'pending', ...} after max_wait_seconds if data never arrives.

        BRAIN allows only one in-flight correlation computation per account. If
        another request is already polling, this returns ``correlation_busy``
        immediately instead of queueing behind it.

        Args:
            use_pre_read: 先读 alpha 详情里平台已算好的 ``is.prodCorrelation``
                （不占锁、不触发计算）。**``refresh=True`` 的强制重测语义必须传
                ``use_pre_read=False``**——否则终验拿到的是平台旧存储值，从未真正重测
                （2026-10-28 修复）。直连调用方（如 perf_max 探针）缺省 True 不变。

        ⚠ **账号级单并发 + 跨进程互斥**（2026-10-22 修 bug）：平台相关性计算是
        **每账号仅 1 个在飞**；本仓的相关性查询散落在多个进程（MCP 服务 + 各 CLI 工具
        + 一次性脚本），进程内 asyncio 锁互不相识 ⇒ 多进程同时轮询同一单槽，
        平台对后来者只返空体（= 仍在算），于是每个进程都空转到轮询上限
        ⇒ **一个卡住的 alpha 能把整账号的相关性查询堵死一小时**。
        故槽位由**跨进程文件锁**（``logs/_dblock/correlation.lock.json``）守护，
        拿不到就**立即返回 busy**（fail-fast），不排队、不降级放行。

        2026-10-28 追加三层（P0-1 / P0-2 / P1-1）：
          1. **冷却按结果分流**——只有「真触发计算」才写 195s 冷却；拿到既有值、
             4xx 终态、异常都不写（旧版无条件写，吞吐被压到 ~4 alpha/小时）。
          2. **inflight 侧车**——开始轮询先标记该 alpha 在飞；同 alpha 在 TTL 内的
             新调用（非 refresh）**只预读等待、不再二次触发**。
          3. **同 alpha 等待**——锁被他进程占着但 holder 恰是同一 alpha 时，等待
             ``WQB_CORR_JOIN_WAIT_SEC``（缺省 25s）里的预读结果，而不是立即 busy。
             refresh 路径保持 fail-fast（终验要的是新算的值，等别人的旧结果没有意义）。
        """
        await self.ensure_authenticated()
        t0 = time.time()

        # ── 2026-10-26 新增：「先读后算」────────────────────────────────────
        # 平台把算好的 prod 相关存进 alpha 详情的 ``is.prodCorrelation``。
        # 先读一次（**不占锁、不触发计算**）：已有值就直接返回。
        # 这是消除"重复触发把账号单槽反复占满"的最高性价比手段——
        # 实测大量调用是在对**平台早已算完**的 alpha 反复触发。
        # 2026-10-28：use_pre_read=False 时跳过（refresh=True 的强制重测语义）。
        if use_pre_read:
            try:
                _pre = await self._read_existing_prod_correlation(alpha_id)
                if _pre is not None:
                    self._corr_log_timing("pre_read_hit", alpha_id, t0,
                                          status="ok", max=_pre.get("max"),
                                          source="alpha_detail_cached")
                    return _pre
            except Exception as _e:  # 预读失败不影响主流程（可能是 alpha 尚在仿真）
                self.log(f"[prod-corr] 预读 is.prodCorrelation 失败({type(_e).__name__})，"
                         "回退到触发计算", "INFO")

        refresh = not use_pre_read
        op_name = f"get_production_correlation({alpha_id})"
        wait_s = (float(max_wait_seconds) if max_wait_seconds is not None
                  else float(_PROD_CORR_WAIT_S))

        # ── P0-2：同 alpha 正在算（inflight）且非 refresh → 只等不触发 ──────
        _inflight = {}
        if not refresh:
            try:
                from wqb.correlation_slot import inflight_get as _inflight_get
                _inflight = _inflight_get(alpha_id) or {}
            except Exception:
                _inflight = {}
            if _inflight:
                joined = await self._await_same_alpha_value(
                    alpha_id, self._corr_join_wait_seconds())
                if joined is not None:
                    self._corr_log_timing("inflight_join", alpha_id, t0,
                                          status="ok", max=joined.get("max"),
                                          source="alpha_detail_cached")
                    return joined
                self._corr_log_timing("inflight_busy", alpha_id, t0,
                                      status="correlation_busy",
                                      inflight_n=_inflight.get("n"))
                return {
                    'status': 'correlation_busy',
                    'message': (
                        f"Alpha {alpha_id} 的生产相关性正在计算中（本机 inflight 标记，"
                        "第 %s 次触发），等待窗口内预读未拿到值。"
                        "请稍后重查，**不要重新触发计算**。"
                        % (_inflight.get("n") or 1)
                    ),
                    'retry_after': min(60, int(self._corr_join_wait_seconds()) or 30),
                    'inflight': True,
                    'max': None,
                    'records': [],
                }

        lock_info = await self._try_acquire_brain_correlation_lock(op_name)
        if not lock_info.get('acquired'):
            # ── P1-1：占着槽的正是同一 alpha → 等它的结果，而不是立即放弃 ──
            if not refresh and self._corr_holder_is_alpha(lock_info.get('holder'), op_name):
                joined = await self._await_same_alpha_value(
                    alpha_id, self._corr_join_wait_seconds())
                if joined is not None:
                    self._corr_log_timing("same_alpha_join", alpha_id, t0,
                                          status="ok", max=joined.get("max"),
                                          source="alpha_detail_cached",
                                          holder=str(lock_info.get('holder')))
                    return joined
                self._corr_log_timing("same_alpha_wait_timeout", alpha_id, t0,
                                      status="correlation_busy")
            # 2026-10-28：**透传真实剩余时间**。旧版写死 busy_retry_after（180s），
            # 把 correlation_slot 冷却档本来能给出的精确剩余秒数丢掉了：
            # 上一轮刚算完、冷却只剩 10s 时，调用方仍被要求盲等 180s。
            # 冷却档（cooldown）给 retry_after；锁被占档没有剩余时间估计，
            # 退回 busy 缺省值。
            retry_after = (
                lock_info.get('retry_after')
                or self._brain_correlation_busy_retry_after_seconds
            )
            self._corr_log_timing("busy", alpha_id, t0,
                                  status="correlation_busy",
                                  retry_after=retry_after,
                                  cooldown=bool(lock_info.get('cooldown')))
            return {
                'status': 'correlation_busy',
                'message': (
                    'Another production correlation check is already running for this account. '
                    'The BRAIN platform supports only one in-flight correlation computation. '
                    f'Please retry in {retry_after} seconds.'
                ),
                'retry_after': retry_after,
                'lock_retry_after': lock_info.get('retry_after'),
                'cooldown': bool(lock_info.get('cooldown')),
                'holder': lock_info.get('holder'),
                'max': None,
                'records': [],
            }

        # ── P0-2：开轮询即标记 inflight（成功/终态清，超时保留）────────────
        inflight_clear = None
        try:
            from wqb.correlation_slot import inflight_clear as _inflight_clear
            from wqb.correlation_slot import inflight_mark as _inflight_mark
            try:
                _inflight_mark(alpha_id, ttl_sec=max(300.0, wait_s + 60.0))
            except Exception:
                pass
            inflight_clear = _inflight_clear
        except Exception:  # pragma: no cover - 侧车不可用不影响主流程
            inflight_clear = None

        result = None
        try:
            result = await self._poll_production_correlation(alpha_id, max_wait_seconds)
            return result
        finally:
            # P0-1：释放槽时按结果分流冷却
            cd, sec = self._corr_release_plan(result)
            if isinstance(result, dict) and result.get('status') == 'pending':
                # 把本次**真正写入**的冷却秒数告诉调用方（它要隔到这个点再来）。
                try:
                    from wqb.correlation_slot import COOLDOWN_SEC_DEFAULT as _CDD
                except Exception:  # pragma: no cover
                    _CDD = 195.0
                result['retry_after'] = sec if sec else _CDD
                result['inflight'] = True
            if inflight_clear is not None and isinstance(result, dict) \
                    and result.get("status") != "pending":
                try:
                    inflight_clear(alpha_id)
                except Exception:
                    pass
            await self._release_brain_correlation_lock(lock_info, op_name,
                                                       cooldown=cd, seconds=sec)

    async def _poll_production_correlation(self, alpha_id: str,
                                           max_wait_seconds: float = None) -> Dict[str, Any]:
        # 2026-10-22：**3600 → 900**（账号级单并发下，卡住的 alpha 若占槽 60 分钟会把
        # 整账号的相关性查询堵死一小时；超时按 ``pending`` 返回，不缓存、不判死）。
        # 2026-10-26：900 → 120。**锁覆盖整个轮询窗口**，窗口长度 = 单次持锁时长。
        # ⚠ 2026-10-28 修正取值 120 → 240：一次**正常**的平台计算 180–200 s（用户口径），
        # 120s 窗口短于它 ⇒ 每条真实计算都必然 pending，再叠 195s 冷却才算拿到值。
        # 定 120 时引用的「实测 94s/条」是 2026-10-06 在 900s 窗口下的旧观测；后来那次
        # 14h 取证的「成功耗时最大 117s」是被 120s 窗口**截断**的样本（超窗即 pending，
        # 不会进入成功统计），不能用来反证窗口够用。窗口值与
        # ``wqb.config.WAIT_THRESHOLDS["prod_corr_timeout_s"]`` 同源（常量 + 守护测试比对）。
        if max_wait_seconds is None:
            max_wait_seconds = _PROD_CORR_WAIT_S
        max_wait_seconds = float(max_wait_seconds)
        # 2026-10-06 实测调优：原 30s 固定间隔让结果落在两个查询点之间时白等。
        # 改成 10s 起、前 12 次 10s、之后 30s 的阶梯：短任务更快收敛，
        # 长尾任务仍不会被请求数放大。与 240s 窗口的配合：10s×12 覆盖前 120s，
        # 之后 30s 一档 ⇒ 查询点约在 0/10/…/120/150/180/210s，200s 内的正常计算
        # 最迟在 210s 那一次拿到（抖动后仍落在窗口内）。
        poll_interval = 30       # 长尾阶段的稳态间隔
        poll_fast = 10           # 前 12 次的快轮询间隔
        start_time = time.time()
        attempt = 0
        consecutive_empty = 0    # track consecutive empty-body responses
        consecutive_network_failures = 0
        saw_empty = False        # 本次是否真见过「仍在算」的空体（= 我们确实触发了一次计算）
        platform_retry_after = None  # 平台 Retry-After（秒），用于 P0-1 的冷却与 P2-9 的间隔

        def _meta(**extra) -> Dict[str, Any]:
            """P2-8：给返回体带上可统计的耗时/次数元数据。"""
            out = {
                'attempts': attempt,
                'elapsed_ms': int(max(0.0, time.time() - start_time) * 1000),
                'computed': bool(saw_empty) or attempt > 1
                            or (time.time() - start_time) >= 2.0,
            }
            if platform_retry_after is not None:
                out['platform_retry_after'] = platform_retry_after
            out.update(extra)
            return out

        def _sleep_s(seconds: float) -> float:
            """P2-7：加 ±15% 抖动，避免多进程在同一秒集体醒来（thundering herd）。"""
            return max(0.0, float(seconds) * random.uniform(0.85, 1.15))

        while True:
            elapsed = time.time() - start_time
            if elapsed >= max_wait_seconds:
                self.log(f"Production correlation timeout after {int(elapsed)}s for {alpha_id}", "WARNING")
                self._corr_log_timing("pending", alpha_id, start_time,
                                      status="pending", attempts=attempt,
                                      computed=_meta()['computed'],
                                      platform_retry_after=platform_retry_after)
                return {
                    'status': 'pending',
                    'message': (
                        f"Production correlation data for alpha {alpha_id} was not available "
                        f"after {int(elapsed)}s of polling. The platform may still be computing "
                        "it. Please retry check_correlation in a few minutes."
                    ),
                    'max': None,
                    'records': [],
                    **_meta(),
                }

            attempt += 1
            try:
                if attempt % 5 == 1:
                    self.log(f"[PC等待] 正在等待 Alpha {alpha_id} 的 PC 数据 (第 {attempt} 次查询, 已等待 {int(elapsed)}s)", "INFO")

                response = await self._request('GET', f"{self.base_url}/alphas/{alpha_id}/correlations/prod")
                # P2-9：平台偶尔给 Retry-After（429 / 空体可能带）。只在**合理范围**内
                # 当轮询间隔用：>30s 的值会把快轮询拖成长等待，不如按自己的阶梯走。
                _ra = self._corr_retry_after_seconds(response)
                if 0 < _ra <= 30:
                    platform_retry_after = _ra
                if response.status_code == 401:
                    # 2026-10-28：会话过期不该烧掉整个轮询窗口（旧版 401 落进
                    # raise_for_status → HTTPError → 按"网络失败"重试到 pending）。
                    # 与 _request_json_with_retries 同策略：清鉴权缓存、刷新后继续。
                    self._auth_validated_until = 0.0
                    try:
                        await self.ensure_authenticated()
                    except Exception as auth_err:  # noqa: BLE001 — 刷新失败按退避重试
                        self.log(f"[PC等待] {alpha_id} 鉴权刷新失败: {auth_err}", "WARNING")
                    consecutive_network_failures += 1
                    await asyncio.sleep(_sleep_s(min(5 * consecutive_network_failures, poll_interval)))
                    continue
                if response.status_code == 429 and _ra > 0:
                    # 429 带 Retry-After：按它退避（同样不超过稳态间隔）
                    await asyncio.sleep(_sleep_s(min(_ra, poll_interval)))
                    continue
                response.raise_for_status()
                
                text = (response.text or "").strip()
                if not text:
                    consecutive_empty += 1
                    saw_empty = True
                    if consecutive_empty == 3:
                        # Platform is still computing — log once so users understand the wait
                        self.log(
                            f"[PC计算中] Alpha {alpha_id} 的生产相关性数据尚未就绪 "
                            f"(已收到 {consecutive_empty} 次空响应). "
                            "平台正在计算中，通常需要 1-5 分钟，请耐心等待...",
                            "INFO"
                        )
                    _wait = poll_fast if attempt <= 12 else poll_interval
                    if platform_retry_after:
                        _wait = min(_wait, platform_retry_after)
                    await asyncio.sleep(_sleep_s(_wait))
                    continue
                
                # Got a non-empty response — reset empty counter
                consecutive_empty = 0
                try:
                    corr_data = response.json()
                    if isinstance(corr_data, list):
                        # 平台偶尔返回数组形态（samples 数组 / 空数组）。
                        # 空数组 = 仍在算（未就绪）；非空则取首个 dict 元素。
                        corr_data = corr_data[0] if (corr_data and isinstance(corr_data[0], dict)) else None
                    if isinstance(corr_data, dict) and corr_data.get('max') is not None:
                        self.log(f"[PC成功] Alpha {alpha_id} PC={corr_data['max']} (第 {attempt} 次查询, 耗时 {int(elapsed)}s)", "INFO")
                        out = dict(corr_data)
                        out['status'] = 'ok'
                        out.setdefault('alpha_id', alpha_id)
                        out.update(_meta(source='platform_poll'))
                        self._corr_log_timing("success", alpha_id, start_time,
                                              status="ok", max=out.get('max'),
                                              source="platform_poll",
                                              computed=out.get('computed'))
                        return out
                except (json.JSONDecodeError, ValueError):
                    logging.getLogger(__name__).debug("swallowed exception", exc_info=True)
                except AttributeError as e:
                    # 防御：任何非预期的响应形态都不应让整条 prod 查询崩掉
                    self.log(f"[PC异常] Alpha {alpha_id} 响应解析失败: {type(e).__name__}: {e}", "WARNING")
                    
            except (requests.RequestException, ConnectionError, TimeoutError) as e:
                # 2026-10-28：**4xx 是终态，不是可重试的网络抖动**。
                # 旧版把 403（无权限 / alpha 无生产相关）/ 404（alpha 不存在）也当网络失败，
                # 在持锁状态下重试满整个轮询窗口，再返回 ``pending`` 诱导调用方排下一轮
                # ⇒ 账号级单槽被一个永不会成功的请求反复占用。HTTPError 是
                # ``requests.RequestException`` 的子类，会落进本分支，故在此按状态码分流。
                http_status = getattr(getattr(e, 'response', None), 'status_code', None)
                _retryable_4xx = (408, 409, 425, 429)  # 请求超时 / 冲突 / 尚早 / 限流
                if (http_status is not None and 400 <= http_status < 500
                        and http_status not in _retryable_4xx):
                    self.log(
                        f"[PC终态] Alpha {alpha_id} prod 相关返回 HTTP {http_status}"
                        "（不可重试），立即返回 data_unavailable", "WARNING")
                    self._corr_log_timing("terminal", alpha_id, start_time,
                                          status="data_unavailable",
                                          http_status=http_status)
                    return {
                        'status': 'data_unavailable',
                        'http_status': http_status,
                        'message': (
                            f"Platform returned HTTP {http_status} for "
                            f"/alphas/{alpha_id}/correlations/prod. This is a terminal "
                            "response (insufficient permission, alpha not found, or no "
                            "production correlation available); retrying will not help."
                        ),
                        'max': None,
                        'records': [],
                        **_meta(),
                    }
                consecutive_network_failures += 1
                retry_delay = min(5 * consecutive_network_failures, poll_interval)
                self.log(
                    f"Failed to get production correlation for {alpha_id} "
                    f"(network failure {consecutive_network_failures}): {e}. "
                    f"Retrying in {retry_delay}s",
                    "WARNING"
                )
                await asyncio.sleep(_sleep_s(retry_delay))
                continue

            consecutive_network_failures = 0

            _wait = poll_fast if attempt <= 12 else poll_interval
            if platform_retry_after:
                _wait = min(_wait, platform_retry_after)
            await asyncio.sleep(_sleep_s(_wait))

