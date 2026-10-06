from __future__ import annotations
import json
import time
import asyncio
import logging
from typing import Dict, Optional, Any
import re
import os
import sys
from pathlib import Path
from urllib.parse import urljoin
import hashlib
import uuid
import random

import requests
import zlib
import msgpack
logger = logging.getLogger("brain_api")


class TransportMixin:
    def __init__(self):
        # Best-effort: load .env early so env overrides are available here
        try:
            from dotenv import load_dotenv, find_dotenv
            env_path = find_dotenv(usecwd=True)
            if env_path:
                load_dotenv(env_path, override=False)
            else:
                candidate = Path(__file__).parent / ".env"
                if candidate.exists():
                    load_dotenv(candidate, override=False)
        except Exception:
            # Fallback: simple parser
            try:
                candidate = Path(__file__).parent / ".env"
                if candidate.exists():
                    for line in candidate.read_text().splitlines():
                        line = line.strip()
                        if not line or line.startswith('#') or '=' not in line:
                            continue
                        k, v = line.split('=', 1)
                        k = k.strip()
                        v = v.strip().strip('"').strip("'")
                        os.environ.setdefault(k, v)
            except Exception:
                logging.getLogger(__name__).debug("swallowed exception", exc_info=True)

        self.base_url = "https://api.worldquantbrain.com"
        self.session = requests.Session()
        self.auth_credentials = None
        self.is_authenticating = False
        self._request_semaphore = asyncio.Semaphore(int(os.environ.get("BRAIN_MAX_CONCURRENCY", "8")))
        # _session_lock removed: requests.Session is thread-safe (urllib3 connection pool + cookiejar),
        # and the lock was serializing ALL requests through asyncio.to_thread, defeating parallelism.
        # Auth mutations (cookies.clear, auth=None) are protected by _auth_lock instead.
        self._auth_lock = asyncio.Lock()
        self._auth_validated_until = 0.0
        try:
            self._auth_check_ttl_seconds = max(0.0, float(os.environ.get("BRAIN_AUTH_CHECK_TTL_SECONDS", "300")))
        except Exception:
            self._auth_check_ttl_seconds = 300.0
        self._brain_correlation_local_lock = asyncio.Lock()
        # get_datafields 全量 dump 的并发闸（原 Redis 分布式锁，2026-10-06 改本地）
        self._datafields_local_lock = asyncio.Lock()
        self._os_pnl_pool_locks: Dict[str, asyncio.Lock] = {}
        self._os_pnl_pool_locks_guard = asyncio.Lock()
        self._os_pnl_pool_last_sync: Dict[str, Any] = {}
        try:
            self._os_pnl_pool_sync_debounce_seconds = max(
                0.0,
                float(os.environ.get("BRAIN_SC_POOL_SYNC_DEBOUNCE_SECONDS", "1")),
            )
        except Exception:
            self._os_pnl_pool_sync_debounce_seconds = 1.0
        try:
            self._brain_correlation_busy_retry_after_seconds = max(
                1,
                int(os.environ.get("BRAIN_CORRELATION_BUSY_RETRY_AFTER_SECONDS", "180")),
            )
        except Exception:
            self._brain_correlation_busy_retry_after_seconds = 180
        # Allow timeout override via env (e.g., API_SETTINGS_TIMEOUT)
        try:
            self._default_timeout_seconds = int(os.environ.get("API_SETTINGS_TIMEOUT", "30"))
        except Exception:
            self._default_timeout_seconds = 30
        self._create_simulation_semaphore = asyncio.Semaphore(int(os.environ.get("BRAIN_CREATE_SIMULATION_MAX_CONCURRENCY", "6")))
        try:
            self._forum_rate_limit_seconds = max(0, int(os.environ.get("FORUM_RATE_LIMIT_SECONDS", "0")))
        except Exception:
            self._forum_rate_limit_seconds = 0
        self._forum_rate_limit_lock = asyncio.Lock()
        self._forum_rate_limit_until = 0.0
        
        # Configure session
        self.session.timeout = self._default_timeout_seconds
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        
        # Load OS/IS Sharpe ratio data for datafield quality filtering
        self._isos_data = {}
        try:
            info_data_path = Path(__file__).parent / 'config' / 'info_data.bin'
            if info_data_path.exists():
                with open(info_data_path, 'rb') as f:
                    self._isos_data = msgpack.unpackb(zlib.decompress(f.read()), raw=False)
                self.log(f"Loaded OS/IS Sharpe data: {len(self._isos_data)} region_delay entries", "INFO")
            else:
                self.log(f"OS/IS Sharpe data file not found at {info_data_path}, sharpe filtering disabled", "WARNING")
        except Exception as e:
            self.log(f"Failed to load OS/IS Sharpe data: {str(e)}, sharpe filtering disabled", "WARNING")

        # ---- 缓存后端（2026-10-06：Redis 移除，改用 SQLite）----
        # 原实现连 Redis，失败即 ``redis_client=None``，于是 ``_get_cached_data`` /
        # ``_set_cached_data`` 读写**静默 no-op**——缓存整条失效，prod 相关性每次都重打
        # 平台单并发队列。且 Redis 那版默认 TTL 7 天，与 prod 48h 保鲜纪律冲突。
        # 现统一走 ``data/wqb.db::api_cache``（跨进程共享，不依赖额外服务）。
        # ``_cache_store`` 懒加载：首次用到时才 import wqb.store，导入失败置哨兵并
        # 只告警一次，**绝不阻断查询主流程**（与旧 Redis 失败降级同哲学）。
        self._cache_store = None
        self._cache_store_loaded = False

    def log(self, message: str, level: str = "INFO"):
        """Log messages to stderr to avoid MCP protocol interference."""
        print(f"[{level}] {message}", file=sys.stderr)

    def _to_absolute_url(self, url: str) -> str:
        if not url:
            return url
        if url.startswith("http://") or url.startswith("https://"):
            return url
        return urljoin(self.base_url, url)

    def _response_payload(self, response: requests.Response) -> Any:
        """Return JSON when possible, otherwise response text for diagnostics."""
        try:
            return response.json()
        except ValueError:
            return response.text

    def _simulation_error_message(self, data: Any) -> str:
        """Extract the most useful error text from a simulation progress payload."""
        if not isinstance(data, dict):
            return str(data) if data is not None else "Unknown error"

        for key in ("error", "message", "detail", "details", "statusMessage", "status"):
            value = data.get(key)
            if value:
                if isinstance(value, (dict, list)):
                    return json.dumps(value, ensure_ascii=False)
                return str(value)

        collected: list[str] = []

        def visit(node: Any) -> None:
            if len(collected) >= 8:
                return
            if isinstance(node, dict):
                for key, value in node.items():
                    lower = str(key).lower()
                    if any(token in lower for token in ("error", "message", "exception", "traceback")) and value:
                        if isinstance(value, (dict, list)):
                            collected.append(json.dumps(value, ensure_ascii=False))
                        else:
                            collected.append(str(value))
                    visit(value)
            elif isinstance(node, list):
                for item in node:
                    visit(item)

        visit(data)
        return " | ".join(collected) if collected else "Unknown error"

    def _generate_cache_key(self, prefix: str, params: dict) -> str:
        """Generate a cache key from prefix and parameters."""
        # Sort params to ensure consistent key generation
        sorted_params = sorted(params.items())
        param_str = json.dumps(sorted_params, sort_keys=True)
        hash_str = hashlib.md5(param_str.encode()).hexdigest()
        return f"{prefix}:{hash_str}"

    def _cache_backend(self):
        """返回 SQLite 缓存 store；不可用返回 ``None``（懒加载 + 一次性告警）。

        2026-10-06：原先返回 Redis 客户端，Redis 未启动时整条缓存链路静默失效。
        现改为 ``wqb.store.CampaignStore``（``data/wqb.db::api_cache``），
        它天然跨进程共享——这正是当初选 Redis 的唯一理由。
        """
        # getattr 惰性取值：``BrainApiClient.__new__`` 造的空壳实例（单测常用）不会
        # 走 __init__，直接取属性会 AttributeError。这里按"未初始化"处理。
        if getattr(self, "_cache_store_loaded", False):
            return getattr(self, "_cache_store", None)
        self._cache_store_loaded = True
        try:
            from wqb.store import CampaignStore  # 延迟导入：MCP 包不强依赖 src
            self._cache_store = CampaignStore.from_workspace()
            self.log("Cache backend: sqlite (data/wqb.db::api_cache)", "INFO")
        except Exception as e:
            # 只告警一次：CLI 工具每次调用都初始化客户端，重复告警会掩盖真实问题。
            self.log(f"Cache backend unavailable ({type(e).__name__}: {e}), caching disabled", "INFO")
            self._cache_store = None
        return self._cache_store

    def _get_cached_data(self, cache_key: str) -> Optional[Dict[str, Any]]:
        """读缓存（SQLite ``api_cache`` 表）。未命中 / 已过期 / 后端不可用 → ``None``。"""
        store = self._cache_backend()
        if store is None:
            return None
        try:
            hit = store.get_api_cache(cache_key)
        except Exception as e:
            self.log(f"Cache read error: {str(e)}", "WARNING")
            return None
        if hit:
            self.log(f"Cache hit for key: {cache_key}", "INFO")
        return hit

    def _set_cached_data(self, cache_key: str, data: Dict[str, Any], ttl: int = 604800):
        """写缓存（SQLite ``api_cache`` 表），TTL 单位为秒。

        ⚠ 默认 TTL 保留 604800（1 周）只为兼容既有调用点（datafields / mutual 等），
        但 **prod 相关性不走这个默认值**——它在 ``check_correlation`` 里按 48h 保鲜
        期显式传 TTL（见 ``brain_mixin_correlation._PROD_CORR_TTL_SECONDS``）。
        生产池会漂移，7 天陈值用于提交判定会出事。
        """
        store = self._cache_backend()
        if store is None:
            return
        try:
            store.set_api_cache(cache_key, data, ttl=ttl)
            self.log(f"Cached data with key: {cache_key}, TTL: {ttl}s", "INFO")
        except Exception as e:
            self.log(f"Cache write error: {str(e)}", "WARNING")

    def _brain_correlation_lock_key(self) -> str:
        """Per-account lock key. BRAIN's correlation concurrency limit is per
        account, so multi-account deployments sharing one Redis must not block
        each other."""
        email = (self.auth_credentials or {}).get('email') if self.auth_credentials else None
        if email:
            digest = hashlib.md5(email.encode()).hexdigest()[:12]
            return f"lock:brain_correlation:{digest}"
        return "lock:brain_correlation"

    async def _try_acquire_brain_correlation_lock(self, op_name: str) -> Dict[str, Any]:
        """Try once to acquire the per-account platform correlation slot.

        2026-10-06：原实现优先用 Redis 分布式锁、失败才回退本地 asyncio 锁。Redis 移除后
        只保留本地锁——语义不变（都是 fail-fast：拿不到就回 busy 而不是排队），
        代价只是**跨进程**不再互斥（本机 MCP 服务是单进程，无影响）。
        """
        lock_key = self._brain_correlation_lock_key()
        lock_token = uuid.uuid4().hex

        if self._brain_correlation_local_lock.locked():
            self.log(f"[corr-lock] Busy local correlation lock for {op_name}", "INFO")
            return {
                'acquired': False,
                'backend': 'local',
                'lock_key': lock_key,
                'retry_after': None,
            }

        await self._brain_correlation_local_lock.acquire()
        self.log(f"[corr-lock] Acquired local correlation lock for {op_name}", "INFO")
        return {
            'acquired': True,
            'backend': 'local',
            'lock_key': lock_key,
            'lock_token': lock_token,
        }

    async def _release_brain_correlation_lock(self, lock_info: Dict[str, Any], op_name: str):
        if not lock_info or not lock_info.get('acquired'):
            return
        backend = lock_info.get('backend')
        if backend == 'local' and self._brain_correlation_local_lock.locked():
            self._brain_correlation_local_lock.release()
            self.log(f"[corr-lock] Released local correlation lock for {op_name}", "INFO")

    async def _rate_limit_forum_op(self, op_name: str) -> Optional[Dict[str, Any]]:
        if self._forum_rate_limit_seconds <= 0:
            return None

        async with self._forum_rate_limit_lock:
            now = time.time()
            until = float(self._forum_rate_limit_until)
            if now < until:
                ttl = int(until - now)
                if ttl < 0:
                    ttl = 0
                return {
                    'status': 'rate_limited',
                    'message': f"Rate limit exceeded. Please wait {ttl} seconds before trying again.",
                    'retry_after': ttl,
                }
            self._forum_rate_limit_until = now + self._forum_rate_limit_seconds
            return None

    async def _request(self, method: str, url: str, **kwargs) -> requests.Response:
        """Run blocking requests I/O in a worker thread to avoid blocking the asyncio event loop."""
        absolute_url = self._to_absolute_url(url)
        timeout = kwargs.pop("timeout", self._default_timeout_seconds)
        # Add extra buffer for asyncio timeout to catch stuck threads
        asyncio_timeout = timeout + 10
        
        async with self._request_semaphore:
            try:
                # Wrap asyncio.to_thread with wait_for to prevent infinite hangs
                return await asyncio.wait_for(
                    asyncio.to_thread(
                        self.session.request,
                        method,
                        absolute_url,
                        timeout=timeout,
                        **kwargs,
                    ),
                    timeout=asyncio_timeout
                )
            except asyncio.TimeoutError:
                self.log(f"Request asyncio timeout for {method} {absolute_url} after {asyncio_timeout}s", "ERROR")
                raise TimeoutError(f"Request timed out after {asyncio_timeout}s")
            except asyncio.CancelledError:
                self.log(f"Request cancelled for {method} {absolute_url}", "WARNING")
                raise
            except requests.Timeout as e:
                self.log(f"Request timeout for {method} {absolute_url}: {str(e)}", "ERROR")
                raise TimeoutError(f"Request timed out after {timeout}s") from e
            except requests.ConnectionError as e:
                self.log(f"Connection error for {method} {absolute_url}: {str(e)}", "ERROR")
                raise ConnectionError(f"Failed to connect to {absolute_url}") from e
            except requests.HTTPError as e:
                self.log(f"HTTP error for {method} {absolute_url}: {str(e)}", "ERROR")
                raise
            except Exception as e:
                # Catch other unexpected errors (e.g., RemoteDisconnected wrapped in other exceptions)
                error_str = str(e)
                if "RemoteDisconnected" in error_str or "Connection aborted" in error_str:
                    self.log(f"Remote disconnected for {method} {absolute_url}: {error_str}", "ERROR")
                    raise ConnectionError(f"Remote server disconnected: {absolute_url}") from e
                raise

    def _retry_wait_seconds(self, response: Optional[requests.Response], attempt: int, base_delay: float = 2.0, max_delay: float = 60.0) -> float:
        if response is not None:
            retry_after = response.headers.get("Retry-After")
            if retry_after:
                try:
                    return min(max(float(retry_after), 0.0), max_delay)
                except (TypeError, ValueError):
                    logging.getLogger(__name__).debug("swallowed exception", exc_info=True)
        backoff = min(base_delay * (1.6 ** attempt), max_delay)
        return backoff + random.uniform(0, min(1.0, backoff * 0.1))

    async def _request_json_with_retries(
        self,
        method: str,
        url: str,
        *,
        op_name: str,
        max_retries: int = 6,
        retry_statuses: Optional[set] = None,
        allow_empty: bool = False,
        **kwargs,
    ) -> Dict[str, Any]:
        """Request JSON with bounded retries for bulk/paginated endpoints."""
        retry_statuses = retry_statuses or {429, 500, 502, 503, 504}
        last_error: Optional[Exception] = None

        for attempt in range(max_retries):
            response: Optional[requests.Response] = None
            try:
                response = await self._request(method, url, **kwargs)
                if response.status_code == 401:
                    self._auth_validated_until = 0.0
                    if attempt < max_retries - 1:
                        self.log(
                            f"{op_name}: HTTP 401, refreshing authentication "
                            f"(attempt {attempt + 1}/{max_retries})",
                            "WARNING",
                        )
                        await self.ensure_authenticated()
                        continue
                    response.raise_for_status()
                if response.status_code in retry_statuses:
                    wait = self._retry_wait_seconds(response, attempt)
                    self.log(
                        f"{op_name}: HTTP {response.status_code}, retrying in {wait:.1f}s "
                        f"(attempt {attempt + 1}/{max_retries})",
                        "WARNING",
                    )
                    await asyncio.sleep(wait)
                    continue

                response.raise_for_status()
                text = (response.text or "").strip()
                if not text:
                    if allow_empty:
                        return {}
                    wait = self._retry_wait_seconds(response, attempt)
                    self.log(
                        f"{op_name}: empty response, retrying in {wait:.1f}s "
                        f"(attempt {attempt + 1}/{max_retries})",
                        "WARNING",
                    )
                    await asyncio.sleep(wait)
                    continue
                try:
                    return response.json() or {}
                except json.JSONDecodeError as e:
                    last_error = e
                    wait = self._retry_wait_seconds(response, attempt)
                    self.log(
                        f"{op_name}: JSON parse failed, retrying in {wait:.1f}s "
                        f"(attempt {attempt + 1}/{max_retries})",
                        "WARNING",
                    )
                    await asyncio.sleep(wait)
                    continue
            except requests.HTTPError:
                raise
            except (ConnectionError, TimeoutError, requests.RequestException) as e:
                last_error = e
                wait = self._retry_wait_seconds(response, attempt)
                self.log(
                    f"{op_name}: transient request failure ({e}), retrying in {wait:.1f}s "
                    f"(attempt {attempt + 1}/{max_retries})",
                    "WARNING",
                )
                await asyncio.sleep(wait)

        if last_error:
            raise last_error
        raise RuntimeError(f"{op_name}: failed after {max_retries} attempts")
