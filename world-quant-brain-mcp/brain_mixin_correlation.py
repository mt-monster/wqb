from __future__ import annotations
import json
import time
import asyncio
import logging
from typing import Dict, List, Optional, Any, Union, Tuple
import re
from datetime import datetime
import os
from pathlib import Path

import pandas as pd
logger = logging.getLogger("brain_api")


def build_alpha_properties_payload(*, name: Optional[str] = None, color: Optional[str] = None,
                                   tags: Optional[List[str]] = None,
                                   descriptions: Optional[str] = None,
                                   selection_description: Optional[str] = None,
                                   combo_description: Optional[str] = None) -> Dict[str, Any]:
    """组 PATCH /alphas/{id} 的 body：**只含显式给出的字段**，None 一律不发。

    纯函数、无网络，供 set_alpha_properties 与单测共用。约定：
      - descriptions 为 None 或历史哨兵字符串 "None" → 不动 regular.description；
      - tags 为 None → 不动（平台侧保留已有标签）；传 [] 才是显式清空；
      - name/color 为 None → 不动。
    """
    payload: Dict[str, Any] = {}
    if name is not None:
        payload["name"] = name
    if color is not None:
        payload["color"] = color
    if tags is not None:
        payload["tags"] = list(tags)
    if descriptions is not None and descriptions != "None":
        payload["regular"] = {"description": descriptions}
    if selection_description is not None:
        payload["selection"] = {"description": selection_description}
    if combo_description is not None:
        payload["combo"] = {"description": combo_description}
    return payload


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
        """兼容包装：只返回 ID 列表（旧签名）。完整性判断见 :meth:`_list_matching_os_alpha_ids_ex`。

        ⚠ **不要在需要完整性结论的路径上用它**（例如 prune 池子 / 写 sidecar）：
        它丢掉了 ``complete=False`` 这个信息，空列表既可能是"确实没有 OS alpha"
        也可能是"列举中途失败"。
        """
        ids, _complete = await self._list_matching_os_alpha_ids_ex(
            instrument_type, region, universe, delay)
        return ids

    async def _list_matching_os_alpha_ids_ex(
        self,
        instrument_type: str,
        region: str,
        universe: str,
        delay: Union[int, str],
    ) -> Tuple[List[str], bool]:
        """Fetch OS alpha IDs that match the target alpha's market configuration.

        BRAIN self-correlation semantics compare against the user's self alpha
        pool for the same instrument/region/universe/delay, and can include
        both REGULAR and SUPER alphas. Filtering locally on the same
        configuration keeps the local calculation aligned with those semantics.

        2026-10-28：ID 列表加进程内 TTL 缓存（``BRAIN_SC_IDLIST_TTL_SECONDS``，
        缺省 900s，0=关闭）。OS 名单变化低频，而旧实现每次调用（超出 1s 防抖后）
        都全量分页列举（300+ 颗 ≈ 4 个 GET）并重写 ppac sidecar；PnL 本体的增量
        下载已由池 pickle 承担，这里省的是纯重复列举。新提交的 alpha 最迟在
        TTL 过期后的下一次 self 相关性计算进入池子。

        Returns:
            ``(ids, complete)``。``complete=False`` 表示分页中途失败（网络/HTTP），
            此时列表是**前缀**而不是全集。2026-10-28 新增完整性返回值的原因：
            旧版把半截列表当全集，下游会拿它**裁掉**池子里"服务端看似已删除"的列
            （实际只是没翻到），列一旦被裁就得重下；更糟的是列举**全失败**时
            列表为空 ⇒ 空池 ⇒ self 相关算出 ``max=0.0`` 并在页面上显示"通过"。
            因此：不完整时**不写 sidecar、不写 TTL 缓存、不裁池**。
        """
        cache = getattr(self, "_os_idlist_cache", None)
        if cache is None:
            cache = self._os_idlist_cache = {}
        ttl = float(getattr(self, "_os_idlist_ttl_seconds", 900.0) or 0.0)
        cache_key = f"{instrument_type}|{region}|{universe}|{delay}"
        cached = cache.get(cache_key)
        if cached and (time.time() - cached[0]) <= ttl:
            return cached[1], True

        all_ids: List[str] = []
        ppac_ids: List[str] = []
        complete = True
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
                complete = False
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

        if not complete:
            # 半截名单一不能缓存（会把"前缀"钉死 15 分钟）、二不能写 sidecar
            # （PPA 名单残缺 ⇒ self 相关性不排除 PPA ⇒ 数值不可比）。
            self.log(
                f"[SC cache] OS alpha 列表分页中断（已收集 {len(all_ids)} 个），"
                "本次不缓存、不写 ppac sidecar", "WARNING")
            return all_ids, False

        # Persist the Power-Pool-Alpha id set so get_self_correlation can
        # exclude/select them without re-listing (survives the sync debounce
        # cache and process restarts).
        try:
            sidecar = self._os_ppac_ids_path(instrument_type, region, universe, delay)
            sidecar.write_text(json.dumps(sorted(set(ppac_ids))))
        except Exception as e:
            self.log(f"[SC cache] Failed to persist ppac ids sidecar: {e}", "WARNING")

        cache[cache_key] = (time.time(), all_ids)
        return all_ids, True

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
        server_ids, complete = await self._list_matching_os_alpha_ids_ex(
            instrument_type, region, universe, delay
        )

        # Load existing cache and drop removed alphas (closed-loop cleanup)
        local_pool = pd.DataFrame()
        memo = getattr(self, "_os_pnl_pool_memo", None)
        if memo is None:
            memo = self._os_pnl_pool_memo = {}
        memo_key = str(pool_path)
        if pool_path.exists():
            try:
                # 2026-10-28：**按文件指纹复用已解析的 DataFrame**。
                # 旧实现每次调用都 ``pd.read_pickle`` 整个池（300+ 列 × 数千行，
                # 一次 self 相关性就要重读几十 MB）；而同一进程里池子只在
                # 增量下载后才变。指纹取 (st_mtime_ns, st_size)：写盘换了内容必变，
                # 同内容重写也不会把命中判错（最多多读一次）。
                st = pool_path.stat()
                stamp = (st.st_mtime_ns, st.st_size)
                hit = memo.get(memo_key)
                if hit is not None and hit[0] == stamp:
                    local_pool = hit[1]
                else:
                    local_pool = await asyncio.to_thread(pd.read_pickle, pool_path)
                if isinstance(local_pool, pd.DataFrame) and not local_pool.empty:
                    if complete:
                        keep_cols = [c for c in local_pool.columns if c in set(server_ids)]
                        dropped = local_pool.shape[1] - len(keep_cols)
                        if dropped > 0:
                            self.log(f"[SC cache] Dropping {dropped} alpha(s) removed from OS list", "INFO")
                        local_pool = local_pool[keep_cols]
                    else:
                        # 分页中断时名单只是前缀，按它裁列会把"没翻到"误判成"已删除"，
                        # 白扔已下载的 PnL 列。保留整池，等下一次完整列举再收口。
                        self.log(
                            "[SC cache] OS 名单不完整，本次跳过池子裁剪（保留 "
                            f"{local_pool.shape[1]} 列）", "WARNING")
                    if not local_pool.empty:
                        memo[memo_key] = (stamp, local_pool)
                else:
                    local_pool = pd.DataFrame()
            except Exception as e:
                self.log(f"[SC cache] Failed to read pool pickle, rebuilding: {e}", "WARNING")
                local_pool = pd.DataFrame()

        need_download = [aid for aid in server_ids if aid not in local_pool.columns]

        if not need_download:
            if not complete and local_pool.empty:
                # 2026-10-28：**fail-closed**。列举全失败（server_ids 为空）+ 本地无池
                # ⇒ 旧实现返回空池，get_self_correlation 据空池算出 ``max=0.0`` 并显示
                # "通过"——把"查不到"伪装成"最安全"。宁可报错让调用方重试。
                raise RuntimeError(
                    "OS alpha 列表获取失败且本地无 PnL 池缓存：无法计算 self 相关性。"
                    "请稍后重试（不要用 0.0 当结果——那是把未知当通过）。")
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
                # 落盘后同步指纹备忘：下一次调用可直接复用这份已解析的帧。
                try:
                    st = pool_path.stat()
                    memo[memo_key] = ((st.st_mtime_ns, st.st_size), full_pool)
                except Exception:  # noqa: BLE001 — 记账失败不影响结果
                    memo.pop(memo_key, None)
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
            combined = pd.concat([os_pool, target_series.rename(target_col).to_frame()], axis=1)
            # 2026-10-28：先裁剪到 4 年窗口（多留 1 行作窗口边界 diff 的前驱），
            # 再 ffill+diff——旧实现先对全历史 ffill+diff、随后把窗口外整段丢弃，
            # 池子大时是对会被扔掉的数据做纯浪费功。裁剪前 sort_index 保证
            # searchsorted/diff 的时序假设成立。
            # 语义注：若某列恰在裁剪点之前断更，旧实现会用更老的数据 ffill 过来，
            # 新实现留 NaN（corrwith 逐列跳过）——日频 PnL 稠密，实际等价。
            _window = pd.DateOffset(years=4)
            combined = combined.sort_index()
            _cutoff = combined.index.max() - _window
            _pos = int(combined.index.searchsorted(_cutoff))
            if _pos > 0:
                combined = combined.iloc[max(0, _pos - 1):]
            combined = combined.ffill()
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

    # ⚠ 2026-10-28 删除：曾有一组 ``_mutual_pair_*`` 缓存辅助（把 N×N 到的
    # 每一对写进 ``api_cache`` 的 ``mutual_corr_pairs:y{N}`` 大 JSON）。**只写不读**
    # ——``cval`` 从头到尾直接查 ``corr.loc[a,b]``，所谓"避免跨调用重算"从未发生，
    # 而每次调用都要把 N²/2 个键整表序列化写一遍（24 颗 = 276 对）。相关性矩阵本来
    # 就是一次 ``rets.corr()`` 的结果，查表比算它更贵，故整套删除。

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

        # Maximal mutually-below-threshold subset.
        # For small baskets (<=24 nodes) compute the EXACT maximum independent set
        # via branch-and-bound (the greedy heuristic under-counts, e.g. w103's
        # reported 8-alpha basket actually had 2 pairs over threshold). For larger
        # baskets fall back to the greedy heuristic and mark it approximate.
        def _greedy_subset() -> List[str]:
            if len(cols) > 1:
                avg_abs = {
                    o: sum(abs(cval(o, p)) for p in cols if p != o) / (len(cols) - 1)
                    for o in cols
                }
            else:
                avg_abs = {cols[0]: 0.0} if cols else {}
            order = sorted(cols, key=lambda o: avg_abs.get(o, 0.0))
            kept_g: List[str] = []
            for oid in order:
                if all(abs(cval(oid, k)) < threshold for k in kept_g):
                    kept_g.append(oid)
            return kept_g

        def _exact_max_independent() -> List[str]:
            # conflict graph: edge where |corr| >= threshold
            idx = {o: i for i, o in enumerate(cols)}
            adj = [0] * len(cols)  # bitmask adjacency
            for i in range(len(cols)):
                for j in range(i + 1, len(cols)):
                    if abs(cval(cols[i], cols[j])) >= threshold:
                        adj[i] |= (1 << j)
                        adj[j] |= (1 << i)
            best: List[int] = []

            def _popcount(x: int) -> int:
                return bin(x).count("1")

            def _bb(cand: int, chosen: List[int]):
                nonlocal best
                if len(chosen) + _popcount(cand) <= len(best):
                    return  # bound
                if cand == 0:
                    if len(chosen) > len(best):
                        best = chosen[:]
                    return
                # pick a vertex with max degree within cand
                max_deg = -1
                v = -1
                m = cand
                while m:
                    lsb = m & (-m)
                    i = lsb.bit_length() - 1
                    deg = _popcount(adj[i] & cand)
                    if deg > max_deg:
                        max_deg = deg
                        v = i
                    m -= lsb
                # branch: include v, then exclude v
                _bb(cand & ~(1 << v) & ~adj[v], chosen + [v])
                _bb(cand & ~(1 << v), chosen)

            full = (1 << len(cols)) - 1
            _bb(full, [])
            return [cols[i] for i in best]

        subset_exact = len(cols) <= 24
        if subset_exact:
            kept = _exact_max_independent()
        else:
            kept = _greedy_subset()

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
            'max_subset_exact': subset_exact,
            'max_subset_note': None if subset_exact else 'greedy approximation (>24 nodes), verify over-threshold pairs manually',
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

    # ⚠ 历史注记：本类曾有 ``_PROD_CORR_TTL_SECONDS = 48 * 3600``，**从未被任何代码读取**
    # （2026-10-06 审计发现、2026-10-28 删除）。prod 保鲜期只有一处生效事实源：
    # ``wqb.store._corr_cache.CORR_FRESH_HOURS``。别再在 MCP 侧重建同义常量——
    # 两份"48h"并存正是当初 Redis 7 天 TTL 漂移的成因。

    def _prod_corr_cached(self, alpha_id: str) -> Optional[Dict[str, Any]]:
        """读 prod 相关的**单源缓存**（权威表 → ``alphas`` 回落），**未过期**才返回。

        2026-10-28：改走 ``get_corr_authoritative``（旧版只查 ``alpha_corr_cache``）。
        单源化前 ``alphas`` 有 561 行历史 prod 而权威表只有 196 行、两者无同步契约，
        只查权威表会把「``alphas`` 里明明有新鲜值」判成未测 ⇒ 白占一次账号级单并发槽。
        回落命中带 ``from_alphas=True``，调用方据此知道这是搬运值而非本链路刚测。

        过期（>48h）或无时间戳一律按"没有"处理——把陈值当缓存命中，是拿漂移过的
        生产池数据去过 0.7 的闸，比不缓存更危险。
        """
        store = self._cache_backend()
        if store is None:
            return None
        try:
            authoritative = getattr(store, "get_corr_authoritative", None)
            if callable(authoritative):
                rec = authoritative(alpha_id)
            else:  # 极简后端（测试替身）只有单表读
                rec = store.get_corr_cache(alpha_id)
        except Exception as e:
            self.log(f"prod corr cache read failed for {alpha_id}: {e}", "WARNING")
            return None
        # 显式取值：`a or b` 会把**合法的 0.0 相关**当缺值（0.0 是最安全的取值，
        # 却最容易被"或链"吞成 None 而白排一轮平台队列）。
        _pv = rec.get("prod_correlation") if rec else None
        _mx = rec.get("max") if rec else None
        _val = _mx if _mx is not None else _pv
        if _val is None or rec.get("stale"):
            return None
        return {
            "max": _val,
            "records": rec.get("records") or [],
            "cached_at": rec.get("checked_at"),
            "source": rec.get("source") or "corr_cache",
            "from_alphas": bool(rec.get("from_alphas")),
        }

    def _prod_corr_last_known(self, alpha_id: str) -> Optional[Dict[str, Any]]:
        """取「最后一次已知 prod 值」，**不做保鲜判断**——只供 pending/busy 回传参考。

        与 :meth:`_prod_corr_cached` 的分工必须分清：
        缓存命中 = **可用来判闸**（48h 内）；本函数 = **只作参考**（可能早已漂移）。

        为什么需要它：平台单并发下最常见的结果是 ``correlation_busy`` / ``pending``，
        调用方拿不到任何数值只能盲等。把最近一次已知值连同 ``stale`` / ``age_hours``
        附在返回体里，人至少能判断「这颗上次是 0.72，本来就过不了」，不必再排一轮。
        **绝不可用它判闸**（判闸只认 ``_prod_corr_cached`` 与平台实测）。
        """
        store = self._cache_backend()
        if store is None:
            return None
        try:
            authoritative = getattr(store, "get_corr_authoritative", None)
            rec = authoritative(alpha_id) if callable(authoritative) else store.get_corr_cache(alpha_id)
        except Exception:  # noqa: BLE001 — 参考值取不到不影响主流程
            return None
        if not rec:
            return None
        _mx = rec.get("max")
        mx = _mx if _mx is not None else rec.get("prod_correlation")
        if mx is None:
            return None
        return {
            "max": mx,
            "checked_at": rec.get("checked_at"),
            "age_hours": rec.get("age_hours"),
            "stale": bool(rec.get("stale", True)),
            "source": rec.get("source") or "corr_cache",
            "from_alphas": bool(rec.get("from_alphas")),
            "note": "参考值，未做 48h 保鲜判断；判闸不得使用",
        }

    def _prod_corr_store(self, alpha_id: str, correlation_data: Dict[str, Any]) -> None:
        """把平台实测 prod 写进权威表（并联动 ``alphas`` 表——见 CorrCacheMixin）。

        失败只告警、绝不阻断查询主流程（与旧 Redis 写失败同哲学）。
        """
        store = self._cache_backend()
        if store is None:
            return
        try:
            store.set_corr_cache(
                alpha_id,
                prod=correlation_data.get("max"),
                records=correlation_data.get("records") or [],
                source="check_correlation",
            )
        except Exception as e:
            self.log(f"prod corr cache write failed for {alpha_id}: {e}", "WARNING")

    async def check_correlation(self, alpha_id: str, correlation_type: str = "production", threshold: float = 0.7, refresh: bool = False) -> Dict[str, Any]:
        """ Only where all IS metrics PASS to Check alpha correlation, Check alpha correlation against production alphas, self alphas, or both.

        Concurrency: production correlation hits BRAIN's per-account
        single-concurrency endpoint. ``get_production_correlation`` uses a
        fail-fast lock, so concurrent production checks return busy instead of
        waiting. The ``self`` path is computed locally and is not gated here.

        Caching (2026-10-06 改): 平台 prod 计算为异步排队（1-5 分钟，单并发），
        已决结果写入 ``data/wqb.db::alpha_corr_cache``（全库 prod 的单一权威，
        联动 ``alphas`` 表）。**保鲜期 48h**（生产池会漂移），过期即回源平台；
        ``pending``/``correlation_busy``/``data_unavailable`` 不缓存；
        ``refresh=True`` 强制重新走平台并覆盖缓存。

        预读命中（2026-10-28 修复）：平台已算好的值（alpha 详情 ``is.prodCorrelation``，
        ``source='alpha_detail_cached'``、无直方图）**直接采纳**——旧版成功判据要求
        records 非空，把该形态拒成 ``data_unavailable``，值被丢弃且不落缓存 ⇒ 重查永远
        卡死。预读结果**不写权威表**：``is.prodCorrelation`` 的测量时间不可知，写
        ``checked_at=now`` 会把 48h 保鲜判据污染成「刚测过」（与 ``set_corr_cache``
        处回填历史值同一教训）；预读本身无锁无队列，重复读取代价可忽略。

        ``refresh=True`` 现在同时跳过本地缓存**与预读**（``use_pre_read=False``），
        强制走平台重测——旧版预读短路使终验拿到的是平台旧存储值。

        并发与重试（2026-10-28 P0-2 / P1-1）：
          - 同 alpha 正在算（本机 inflight 标记）且非 refresh → **只预读等待**
            （``WQB_CORR_JOIN_WAIT_SEC``，缺省 25s），等不到就返回 ``correlation_busy``
            并带 ``inflight=True``；**不会二次触发计算**。
          - 锁被他进程占着但 holder 恰是同一 alpha → 同样等待窗口内的预读结果
            （``same_alpha_join``）；refresh 保持 fail-fast。
        """
        await self.ensure_authenticated()
        t0 = time.time()

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
                    # 结果缓存：单源读（权威表 alpha_corr_cache → alphas 回落），
                    # 48h 内直接命中，不占平台单并发队列；refresh=True / 缺失 / 已过期则回源。
                    cached = None if refresh else self._prod_corr_cached(alpha_id)
                    if cached and cached.get('max') is not None:
                        max_correlation = cached['max']
                        passes_check = max_correlation < threshold
                        self._corr_log_timing("cache_hit", alpha_id, t0,
                                              status="ok", max=max_correlation,
                                              source=cached.get('source'))
                        results['checks'][check_type] = {
                            'max_correlation': max_correlation,
                            'passes_check': passes_check,
                            'from_cache': True,
                            'cached_at': cached.get('cached_at'),
                            'source': cached.get('source'),
                            'from_alphas': bool(cached.get('from_alphas')),
                            'correlation_data': cached,
                        }
                        if not passes_check:
                            all_passed = False
                            results["all_passed"] = all_passed
                            return results
                        continue

                    correlation_data = await self.get_production_correlation(
                        alpha_id, use_pre_read=not refresh)
                    
                    # Handle pending/data-not-yet-available case (super alphas, fresh simulations)
                    if correlation_data and correlation_data.get('status') == 'pending':
                        # 2026-10-28：附「最近已知值」——pending 时调用方拿不到任何数只能盲等，
                        # 至少让它看到上次是多少（带 stale/age_hours，**不可用于判闸**）。
                        # 2026-10-28 P0-1：同时透传本次真正写入的冷却秒数（retry_after）与
                        # inflight 标记——调用方据此**隔到点后再来**，而不是立刻重触发。
                        _last_known = self._prod_corr_last_known(alpha_id)
                        results['checks'][check_type] = {
                            'max_correlation': None,
                            'passes_check': None,
                            'status': 'pending',
                            'message': correlation_data.get('message', ''),
                            'retry_after': correlation_data.get('retry_after'),
                            'inflight': bool(correlation_data.get('inflight')),
                            'attempts': correlation_data.get('attempts'),
                            'elapsed_ms': correlation_data.get('elapsed_ms'),
                            'last_known': _last_known,
                            'correlation_data': correlation_data,
                        }
                        results['all_passed'] = None
                        results['status'] = 'pending'
                        results['message'] = correlation_data.get('message', '')
                        results['retry_after'] = correlation_data.get('retry_after')
                        results['inflight'] = bool(correlation_data.get('inflight'))
                        results['last_known'] = _last_known
                        return results

                    if correlation_data and correlation_data.get('status') == 'correlation_busy':
                        _last_known = self._prod_corr_last_known(alpha_id)
                        results['checks'][check_type] = {
                            'max_correlation': None,
                            'passes_check': None,
                            'status': 'correlation_busy',
                            'message': correlation_data.get('message', ''),
                            'retry_after': correlation_data.get('retry_after'),
                            'inflight': bool(correlation_data.get('inflight')),
                            'holder': correlation_data.get('holder'),
                            'last_known': _last_known,
                            'correlation_data': correlation_data,
                        }
                        results['all_passed'] = None
                        results['status'] = 'correlation_busy'
                        results['message'] = correlation_data.get('message', '')
                        results['retry_after'] = correlation_data.get('retry_after')
                        results['inflight'] = bool(correlation_data.get('inflight'))
                        results['last_known'] = _last_known
                        return results

                    # ── 预读命中（2026-10-28 修复 P0）：平台已算值直接采纳 ──
                    # 该形态 records=[]（无直方图），不能进下面要求 records 非空的
                    # 平台实测分支；max 已在手，判闸与早退语义与实测分支完全一致。
                    # ``provisional=True``：这是**平台存储值、测量时间不可知**，
                    # 不等于刚才重测。终验（_prod_gate）看到它会补一次 refresh=True 重测，
                    # 避免「拿旧值过闸」。同 alpha 等待（joined）拿到的也是存储值，同理。
                    if (correlation_data
                            and correlation_data.get('source') == 'alpha_detail_cached'
                            and correlation_data.get('max') is not None):
                        max_correlation = correlation_data['max']
                        passes_check = max_correlation < threshold
                        results['checks'][check_type] = {
                            'max_correlation': max_correlation,
                            'passes_check': passes_check,
                            'source': 'alpha_detail_cached',
                            'provisional': bool(correlation_data.get('provisional', True)),
                            'joined': bool(correlation_data.get('joined')),
                            'correlation_data': correlation_data,
                        }
                        results['provisional'] = bool(correlation_data.get('provisional', True))
                        if not passes_check:
                            all_passed = False
                            results["all_passed"] = all_passed
                            return results
                        continue

                    # 2026-10-28：**判据只要求 max 非空**（旧版还要求 records 非空）。
                    # 平台契约里 ``max`` 是判闸唯一必需项，直方图 ``records`` 是附带信息；
                    # 要求 records 会把「平台给了 max 但没给直方图」的合法响应拒成
                    # data_unavailable，而该结果又因不满足成功判据而不落缓存 ⇒ 重查永远拿不到。
                    # 已知的值、未知的直方图，按已知处理（与预读分支同一口径）。
                    if correlation_data and correlation_data.get('max') is not None:
                        max_correlation = correlation_data['max']
                        passes_check = max_correlation < threshold
                        # 仅已决结果入缓存（pending/busy 分支已提前 return，不会走到这里）。
                        # 写权威表并联动 alphas——这是设计文档 §6.2 第 4 条自 2026-10-04
                        # 声称、却直到 2026-10-06 才真正实现的一步。
                        self._prod_corr_store(alpha_id, correlation_data)
                        results['checks'][check_type] = {
                            'max_correlation': max_correlation,
                            'passes_check': passes_check,
                            'attempts': correlation_data.get('attempts'),
                            'elapsed_ms': correlation_data.get('elapsed_ms'),
                            'computed': correlation_data.get('computed'),
                            'correlation_data': correlation_data
                        }
                        if not passes_check:
                            all_passed = False
                            results["all_passed"] = all_passed
                            return results
                    else:
                        # Data returned but has no usable max (empty or malformed).
                        # Return None to signal "data unavailable" rather than faking max=0.
                        _http_status = (correlation_data or {}).get('http_status')
                        _last_known = self._prod_corr_last_known(alpha_id)
                        results['checks'][check_type] = {
                            'max_correlation': None,
                            'passes_check': None,
                            'status': 'data_unavailable',
                            'http_status': _http_status,
                            'last_known': _last_known,
                            'message': (
                                (correlation_data or {}).get('message')
                                or 'Production correlation data is unavailable for this alpha. '
                                   'This may be a newly-created super alpha where the platform '
                                   'has not yet computed the correlation. Please retry in a few minutes.'
                            ),
                            'correlation_data': correlation_data,
                        }
                        results['all_passed'] = None
                        results['status'] = 'data_unavailable'
                        results['last_known'] = _last_known
                        if _http_status is not None:
                            results['http_status'] = _http_status
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
        """Comprehensive pre-submission check.

        2026-10-28：PnL 与年度统计**并行**取（两者互不依赖、各是一个 GET）；
        相关性放最后单独等——它可能占平台单并发槽到一轮轮询窗口（
        ``WAIT_THRESHOLDS["prod_corr_timeout_s"]``，2026-10-28 起 240s），与上面两个
        请求并行没有收益（账号级相关性子并发=1，且它自己会重试）。
        旧实现三连串行，最坏把「两个轻请求 + 一次相关性慢等」叠成同一段墙钟时间。
        """
        await self.ensure_authenticated()

        try:
            # This endpoint might not exist, so we simulate it by calling other functions
            # In a real scenario, this would be a single API call

            pnl_data, yearly_stats = await asyncio.gather(
                self.get_alpha_pnl(alpha_id),
                self.get_alpha_yearly_stats(alpha_id),
            )
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
        """Update alpha properties (name, color, tags, descriptions).

        PATCH 语义：只发送**显式给出**的字段（与官方 ace_lib.set_alpha_properties 一致）。
        2026-09-21 事故：此前无条件发送 name=None / regular.description=None / tags=[]，
        submit_alpha 节点在调用方不传 name/descriptions 时把 gJboYLRl 已设好的名称与
        描述 PATCH 成 null 后才提交。descriptions 的历史默认值 "None"（字符串）同样视为
        "未提供"。
        """
        await self.ensure_authenticated()

        try:
            payload = build_alpha_properties_payload(
                name=name, color=color, tags=tags, descriptions=descriptions,
                selection_description=selection_description,
                combo_description=combo_description,
            )
            if not payload:
                # 什么都没给：不发空 PATCH，直接回读当前属性（幂等、零副作用）
                response = await self._request('GET', f"{self.base_url}/alphas/{alpha_id}")
                response.raise_for_status()
                return response.json()

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
        """Get available instrument types, regions, delays, and universes (cached 1 day in SQLite)."""
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
            
            # Cache the data (1 day TTL)——2026-10-28：旧代码注释写 1 day、实际传 604800（7 天），
            # 二者不一致。平台设置项属于低频变化，但"注释说一天、代码存一周"会让排障时误判
            # 数据新鲜度，故按注释口径收成 86400。
            self._set_cached_data(cache_key, result, ttl=86400)
            
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
