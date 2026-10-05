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
import redis
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

        # Initialize Redis connection
        # 2026-10-03 启动性能修复：Redis 是可选缓存（无它功能不受影响，只是无缓存）。
        # 原 socket_connect_timeout=5 在本机无 Redis 时会白等满 5 秒（TCP 探测超时），
        # 使 MCP stdio 启动耗时 ~5.8s，客户端连接超时后直接放弃挂载 → 整server 工具
        # 不可用。改为 0.3s：仍然能连上本地/容器里正常响应的 Redis，但不可达时几乎
        # 无感失败。经实测 import 耗时 5.75s → 1.47s。
        # 仅影响"连不上时要等多久"，不影响连得上时的行为。
        try:
            redis_host = os.environ.get('REDIS_HOST', 'localhost')
            try:
                redis_port = int(os.environ.get('REDIS_PORT', str(6379)))
            except Exception:
                redis_port = 6379

            self.redis_client = redis.Redis(
                host=redis_host,
                port=redis_port,
                db=0,
                decode_responses=True,
                socket_connect_timeout=float(os.environ.get('REDIS_CONNECT_TIMEOUT', '0.3'))
            )
            # Test connection
            self.redis_client.ping()
            self.log("Redis connection established", "INFO")
        except Exception as e:
            # 2026-09-01 降噪：Redis 是可选缓存（无 Redis 功能不受影响，只是无缓存），
            # 连接失败降为一次性 INFO 提示，不再刷 WARNING（CLI 工具如 submit_verdict
            # 每次调用都会初始化客户端，WARNING 噪音掩盖真实告警）。
            self.log(f"Redis not available ({type(e).__name__}), caching disabled (optional)", "INFO")
            self.redis_client = None

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

    def _get_cached_data(self, cache_key: str) -> Optional[Dict[str, Any]]:
        """Get data from Redis cache."""
        if not self.redis_client:
            return None
        try:
            cached = self.redis_client.get(cache_key)
            if cached:
                self.log(f"Cache hit for key: {cache_key}", "INFO")
                return json.loads(cached)
        except Exception as e:
            self.log(f"Cache read error: {str(e)}", "WARNING")
        return None

    def _set_cached_data(self, cache_key: str, data: Dict[str, Any], ttl: int = 604800):
        """Set data in Redis cache with TTL (default 1 week = 604800 seconds)."""
        if not self.redis_client:
            return
        try:
            self.redis_client.setex(cache_key, ttl, json.dumps(data))
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

        三级降级（2026-10-02 补第三级）：
          1) Redis          —— 真跨进程（多 MCP 进程并存时唯一有效的一级）
          2) 跨进程文件锁    —— Redis 不可达时的跨进程兜底（复用 wqb.db_write_lock 的
                               O_CREAT|O_EXCL + TTL 自愈 + 死持有者回收）
          3) 进程内 asyncio  —— 最后兜底，仅本进程内互斥

        背景：平台相关性接口**单账号单并发**。2026-10-02 实测本机 Redis 未启动
        （localhost:6379 超时 → redis_client=None），而同时有 8 个 MCP 进程在跑，
        旧实现直接落到第 3 级 asyncio.Lock ⇒ **跨进程零互斥** ⇒ 并发打平台单并发
        接口 ⇒ 429/空体/查不到结果。补第 2 级后，无 Redis 也能跨进程互斥。
        """
        lock_key = self._brain_correlation_lock_key()
        try:
            lock_ttl = int(os.environ.get("BRAIN_CORRELATION_LOCK_TTL_SECONDS", "3700"))
        except Exception:
            lock_ttl = 3700
        lock_token = uuid.uuid4().hex

        if self.redis_client:
            try:
                if self.redis_client.set(lock_key, lock_token, ex=lock_ttl, nx=True):
                    self.log(
                        f"[corr-lock] Acquired {lock_key} for {op_name} (ttl={lock_ttl}s)",
                        "INFO",
                    )
                    return {
                        'acquired': True,
                        'backend': 'redis',
                        'lock_key': lock_key,
                        'lock_token': lock_token,
                    }
                ttl = self.redis_client.ttl(lock_key)
                self.log(
                    f"[corr-lock] Busy {lock_key} for {op_name} (holder_ttl={ttl}s)",
                    "INFO",
                )
                return {
                    'acquired': False,
                    'backend': 'redis',
                    'lock_key': lock_key,
                    'retry_after': ttl if ttl and ttl > 0 else None,
                }
            except Exception as e:
                self.log(
                    f"[corr-lock] Redis error acquiring lock for {op_name}: {e}. "
                    "Falling back to cross-process file lock.",
                    "WARNING",
                )

        # 2) 跨进程文件锁兜底（无 Redis 时恢复真正的全局互斥）
        file_lock = self._try_acquire_cross_process_corr_lock(op_name, lock_ttl)
        if file_lock is not None:
            return file_lock

        # 3) 最后兜底：进程内 asyncio.Lock（仅本进程互斥，跨进程无保证）
        if self._brain_correlation_local_lock.locked():
            self.log(f"[corr-lock] Busy local correlation lock for {op_name}", "INFO")
            return {
                'acquired': False,
                'backend': 'local',
                'lock_key': lock_key,
                'retry_after': None,
            }

        await self._brain_correlation_local_lock.acquire()
        self.log(
            f"[corr-lock] Acquired local correlation lock for {op_name} "
            "(仅进程内互斥，跨进程无保证)",
            "WARNING",
        )
        return {
            'acquired': True,
            'backend': 'local',
            'lock_key': lock_key,
            'lock_token': lock_token,
        }

    def _try_acquire_cross_process_corr_lock(self, op_name: str,
                                             lock_ttl: int) -> Optional[Dict[str, Any]]:
        """第 2 级：跨进程文件锁。返回 None 表示本模块不可用 → 交给第 3 级。

        复用 ``wqb.db_write_lock``（O_CREAT|O_EXCL 单文件锁 + TTL 自愈 +
        死持有者按 pid 回收 + ``os.replace(.stale)`` 退役，避开沙箱 safe-delete 守卫），
        以 ``fail_fast=True`` 保持"立即返回忙、不排队"的原语义。
        """
        try:
            from wqb.db_write_lock import acquire as _flock_acquire
            from wqb.db_write_lock import release as _flock_release
        except Exception as e:  # pragma: no cover - 依赖缺失时才走
            self.log(
                f"[corr-lock] 跨进程文件锁不可用（{type(e).__name__}），"
                "降级为进程内锁——多进程并存时可能并发打平台相关性接口。",
                "WARNING",
            )
            return None

        info = _flock_acquire(
            tag=f"corr:{op_name}",
            ttl_sec=float(lock_ttl),
            wait_timeout=0.0,
            name="correlation.lock.json",
            fail_fast=True,
        )
        if info.get("busy"):
            self.log(
                f"[corr-lock] Busy cross-process file lock for {op_name} "
                "(另一进程正在查平台相关性)",
                "INFO",
            )
            return {
                'acquired': False,
                'backend': 'file',
                'lock_key': info.get("token") or "correlation.lock.json",
                'retry_after': None,
            }
        if not info.get("token"):
            # 写锁目录不可建/写入失败 → degraded，无法承担跨进程互斥，交给第 3 级
            self.log(
                f"[corr-lock] 跨进程文件锁 degraded（{op_name}），降级为进程内锁",
                "WARNING",
            )
            return None

        self.log(
            f"[corr-lock] Acquired cross-process file lock for {op_name} "
            f"(ttl={lock_ttl}s)",
            "INFO",
        )
        return {
            'acquired': True,
            'backend': 'file',
            'lock_key': info["token"],
            'lock_token': info["token"],
            '_flock_release': _flock_release,
        }

    async def _release_brain_correlation_lock(self, lock_info: Dict[str, Any], op_name: str):
        if not lock_info or not lock_info.get('acquired'):
            return
        backend = lock_info.get('backend')
        if backend == 'redis' and self.redis_client:
            try:
                self.redis_client.eval(
                    "if redis.call('get', KEYS[1]) == ARGV[1] then "
                    "return redis.call('del', KEYS[1]) else return 0 end",
                    1,
                    lock_info['lock_key'],
                    lock_info['lock_token'],
                )
                self.log(f"[corr-lock] Released {lock_info['lock_key']} for {op_name}", "INFO")
            except Exception as e:
                self.log(f"[corr-lock] Lock release failed for {op_name}: {e}", "WARNING")
            return

        if backend == 'file':
            try:
                release_fn = lock_info.get('_flock_release')
                if release_fn is None:  # 兜底：重新导入
                    from wqb.db_write_lock import release as release_fn  # noqa: WPS440
                release_fn(lock_info['lock_key'])
                self.log(
                    f"[corr-lock] Released cross-process file lock for {op_name}", "INFO"
                )
            except Exception as e:
                self.log(
                    f"[corr-lock] File lock release failed for {op_name}: {e}", "WARNING"
                )
            return

        if backend == 'local' and self._brain_correlation_local_lock.locked():
            self._brain_correlation_local_lock.release()
            self.log(f"[corr-lock] Released local correlation lock for {op_name}", "INFO")

    async def _rate_limit_forum_op(self, op_name: str) -> Optional[Dict[str, Any]]:
        if self._forum_rate_limit_seconds <= 0:
            return None

        if self.redis_client:
            try:
                lock_key = "rate_limit:forum_ops"
                if not self.redis_client.set(lock_key, "locked", ex=self._forum_rate_limit_seconds, nx=True):
                    ttl = self.redis_client.ttl(lock_key)
                    if not isinstance(ttl, int) or ttl < 0:
                        ttl = self._forum_rate_limit_seconds
                    return {
                        'status': 'rate_limited',
                        'message': f"Rate limit exceeded. Please wait {ttl} seconds before trying again.",
                        'retry_after': ttl,
                    }
            except Exception as e:
                self.log(f"Rate limiting for {op_name} failed, falling back to local limiter: {str(e)}", "WARNING")

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
