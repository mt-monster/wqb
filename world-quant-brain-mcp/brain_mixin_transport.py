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
        # ---- 连接池修复 (2026-10-26) ----
        # 背景：MCP server 长时间运行后堆积 CloseWait 连接（本地 FIN 已发但 socket 未回收）。
        # 原因：默认 HTTPAdapter 的 pool_connections=10/pool_maxsize=10 与 _request_semaphore(8)
        # + _create_simulation_semaphore(6) 的 14 并发上限不匹配，且 asyncio.wait_for 超时后
        # asyncio.to_thread 里的 requests 线程不被强制中断，socket 持续占用连接池槽位。
        # 修复：显式挂载更大 pool 的 adapter；启动 daemon sweeper 定期清空 idle socket；
        # 进程退出时 close session。
        try:
            _pool_size = int(os.environ.get("BRAIN_POOL_MAXSIZE", "24"))
        except Exception:
            _pool_size = 24
        try:
            _idle_sweep_sec = max(30, int(os.environ.get("BRAIN_POOL_IDLE_SWEEP_SEC", "90")))
        except Exception:
            _idle_sweep_sec = 90
        try:
            _adapter = requests.adapters.HTTPAdapter(
                pool_connections=_pool_size,
                pool_maxsize=_pool_size,
                max_retries=0,  # retry 由 _request_json_with_retries 手动实现，避免双重
                pool_block=False,
            )
            self.session.mount("https://", _adapter)
            self.session.mount("http://", _adapter)
        except Exception as _e:
            logging.getLogger(__name__).warning("HTTPAdapter mount failed, using default: %s", _e)
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
        # pickle 指纹备忘：{(mtime_ns, size) → DataFrame}，避免每次 self 相关性
        # 都重新 read_pickle 整个 OS 池（2026-10-28）。
        self._os_pnl_pool_memo: Dict[str, Any] = {}
        try:
            self._os_pnl_pool_sync_debounce_seconds = max(
                0.0,
                float(os.environ.get("BRAIN_SC_POOL_SYNC_DEBOUNCE_SECONDS", "1")),
            )
        except Exception:
            self._os_pnl_pool_sync_debounce_seconds = 1.0
        # OS ID 列表的进程内 TTL（秒）。OS 名单低频变化，TTL 内复用列举结果，
        # 省掉每次 self 相关性计算的 3-4 个分页 GET（2026-10-28）。0=关闭缓存。
        try:
            self._os_idlist_ttl_seconds = max(
                0.0,
                float(os.environ.get("BRAIN_SC_IDLIST_TTL_SECONDS", "900")),
            )
        except Exception:
            self._os_idlist_ttl_seconds = 900.0
        # 槽被**另一进程持着且没有冷却信息**时给调用方的重试提示。
        # 2026-10-28：180 → 240。持锁时长就是一轮轮询窗口（现 240s + 收尾），
        # 提示 180s 会让调用方早 60s 回来再撞一次 busy（每次 busy 只是本地文件锁检查，
        # 但仍是一次空转）；240 = "按一轮完整查询的时长后再来"。
        try:
            self._brain_correlation_busy_retry_after_seconds = max(
                1,
                int(os.environ.get("BRAIN_CORRELATION_BUSY_RETRY_AFTER_SECONDS", "240")),
            )
        except Exception:
            self._brain_correlation_busy_retry_after_seconds = 240
        # 跨进程相关性槽（logs/_dblock/correlation.lock.json）的 TTL。
        # 2026-10-22 起该锁是**账号级真互斥**（平台相关性接口单并发），
        # TTL 必须 ≥ 单次轮询窗口，否则长轮询期间 token 被 TTL 自愈回收 ⇒
        # 第二个进程以为拿到槽、实际并发打平台（正是本次要修的 bug 的反面）。
        #
        # 2026-10-26：3700 → 600。旧值 3700 让崩溃残留锁占用 62 分钟。
        # 2026-10-28：窗口 120 → 240，600 仍是（窗口 + 30s 台阶 + 抖动）的 2.2 倍，
        # 覆盖一次完整长轮询绰绰有余；**不要**按「5× 窗口」抬到 1200（崩溃残留翻倍）。
        try:
            self._brain_correlation_lock_ttl_seconds = max(
                60,
                int(os.environ.get("BRAIN_CORRELATION_LOCK_TTL_SECONDS", "600")),
            )
        except Exception:
            self._brain_correlation_lock_ttl_seconds = 600
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
        # 注意：requests.Session 没有 .timeout 属性，旧代码 self.session.timeout=... 是死代码。
        # 真正的 timeout 靠每次 self.session.request(..., timeout=timeout) 显式传（见 _request）。
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })

        # ---- Idle socket sweeper + atexit close (2026-10-26) ----
        # 见文件顶部 Fix 1 注释。此处启动 daemon 线程，每 _idle_sweep_sec 秒清一次
        # urllib3 PoolManager 的空闲 socket，避免 asyncio.wait_for 超时后遗留的僵尸 socket
        # 一直挂在池里（这是 CloseWait 堆积的直接机制）。
        import threading
        import atexit
        def _pool_idle_sweeper():
            while True:
                try:
                    time.sleep(_idle_sweep_sec)
                except Exception:
                    return
                try:
                    for _k in ("https://", "http://"):
                        _ad = self.session.get_adapter(_k)
                        if getattr(_ad, "poolmanager", None) is not None:
                            try:
                                _ad.poolmanager.clear()
                            except Exception:
                                pass
                except Exception:
                    logging.getLogger(__name__).debug("pool sweeper tick failed", exc_info=True)
        _sweeper = threading.Thread(target=_pool_idle_sweeper, daemon=True, name="brain-pool-sweeper")
        _sweeper.start()
        atexit.register(self.session.close)
        
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

        ⚠ 默认 TTL 保留 604800（1 周）只为兼容既有调用点（datafields / mutual / 平台设置等）。
        **prod 相关性不走 ``api_cache``**：它是异步算出来的、昂贵的权威值，落
        ``alpha_corr_cache``（``wqb.store._corr_cache``），保鲜 48h 由
        ``CORR_FRESH_HOURS`` 一处判。生产池会漂移，7 天陈值用于提交判定会出事。
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

        **两级，顺序不可换**（2026-10-22 修 bug：60 分钟轮询把平台单并发槽占死）：

          1) **进程内 asyncio.Lock**——同进程内的并发（MCP 服务同时来两个请求）。
             必须**先**拿：``wqb.db_write_lock`` 把「同 pid 再 acquire」当**重入续约**，
             若文件锁先拿，同进程的两个协程会**同时**自认持有（都续约同一 token）⇒ 互斥失效。
          2) **跨进程文件锁**（``logs/_dblock/correlation.lock.json``）——真正的账号级互斥。
             平台 ``GET /alphas/{id}/correlations/prod`` 是**账号级单并发**接口：同一账号
             任何时刻只允许一个相关性计算在飞。而本仓的相关性查询散落在**多个进程**
             （MCP 常驻服务 + ``tools/campaign_intel.py prod-first`` + ``tools/probe/prod_bucket_scan.py``
             + 各类一次性脚本），它们**各自**新建 ``BrainApiClient`` ⇒ 只剩进程内锁时
             进程间互不相识 ⇒ 多进程同时轮询同一账号级单槽。
             平台侧表现为：后到者拿到**空体**（= 仍在算），于是它一直轮询到
             ``max_wait_seconds`` 才放弃 ⇒ **一个卡住的 alpha 能把整账号的
             相关性查询堵死一小时**（2026-10-22 实测：另一个会话的 prod 队列脚本卡在
             第 4 个目标上，本会话的查询空转 800s+ 拿不到数；杀掉它之后本会话
             同一 alpha 1499s 才出数）。

        第 2 级用 ``wqb.db_write_lock``（O_CREAT|O_EXCL + TTL 自愈 + 死持有者按 pid 回收），
        token 文件名与写库锁不同 ⇒ 两个锁互不干扰（且 ``_prune_expired`` 按名精确定位，
        不会用短 TTL 回收对方仍持有的 token）。**fail_fast=True**：槽被占就立即返回 busy，
        **不排队、不降级放行**——放行等于让第二个进程也去打这个单并发接口。

        2026-10-06 注（Redis 移除后）：曾一度只剩进程内锁，注释写「本机 MCP 服务是单进程，
        无影响」。**该假设已被实测证伪**：相关性查询不止 MCP 服务一个进程在跑。
        """
        lock_key = self._brain_correlation_lock_key()

        # 1) 进程内互斥（先拿：同 pid 的文件锁是「重入续约」，不能承担进程内互斥）
        if self._brain_correlation_local_lock.locked():
            self._log_corr_busy(f"[corr-lock] Busy local correlation lock for {op_name}")
            return {
                'acquired': False,
                'backend': 'local',
                'lock_key': lock_key,
                'retry_after': None,
                # P1-1：同进程并发时也能判断「占着的是不是同一个 alpha」
                'holder': f"corr:{getattr(self, '_corr_local_holder_op', '') or ''}",
            }
        await self._brain_correlation_local_lock.acquire()
        self._corr_local_holder_op = op_name

        # 2) 跨进程文件锁（账号级真互斥）；拿不到 → 释放进程内锁并立即报忙
        file_lock = self._try_acquire_cross_process_corr_lock(op_name)
        if file_lock is None:
            # 本模块不可用 / degraded → 只剩进程内互斥（跨进程无保证，但可用）
            self.log(f"[corr-lock] Acquired local correlation lock for {op_name} "
                     "(跨进程锁不可用，仅进程内互斥)", "WARNING")
            return {
                'acquired': True,
                'backend': 'local',
                'lock_key': lock_key,
                'lock_token': None,
            }
        if not file_lock.get('acquired'):
            # 槽被别的进程占着 → 释放进程内锁，立即报忙（不排队、不降级放行）
            if self._brain_correlation_local_lock.locked():
                self._brain_correlation_local_lock.release()
                self._corr_local_holder_op = None
            return file_lock

        # 两级都拿到 → 释放时两级都要还
        file_lock['local_lock_held'] = True
        return file_lock

    def _try_acquire_cross_process_corr_lock(self, op_name: str) -> Optional[Dict[str, Any]]:
        """第 2 级：跨进程文件锁。返 ``None`` 表示本模块不可用 → 只剩进程内互斥。

        复用 ``wqb.correlation_slot``（``wqb.db_write_lock`` 的通用单文件锁：
        O_CREAT|O_EXCL + TTL 自愈 + 死持有者按 pid 回收 + ``.stale`` 退役），
        ``fail_fast=True`` 保持「立即返回忙、不排队」的语义。
        """
        try:
            from wqb.correlation_slot import acquire as _slot_acquire
            from wqb.correlation_slot import release as _slot_release
        except Exception as e:  # pragma: no cover - 依赖缺失时才走到
            self.log(
                f"[corr-lock] 跨进程文件锁不可用（{type(e).__name__}），"
                "降级为进程内锁——多进程并存时可能并发打平台相关性接口",
                "WARNING",
            )
            return None

        try:
            info = _slot_acquire(op_name, ttl_sec=float(self._brain_correlation_lock_ttl_seconds))
        except Exception as e:  # pragma: no cover - 锁实现异常时降级
            self.log(f"[corr-lock] 跨进程文件锁异常（{type(e).__name__}: {e}），降级为进程内锁",
                     "WARNING")
            return None

        if info.get("busy"):
            self._log_corr_busy(
                f"[corr-lock] Busy cross-process file lock for {op_name} "
                "(另一进程正在查平台相关性——账号级单并发，不能并发打)"
            )
            # 2026-10-28：**透传 correlation_slot 给出的剩余冷却时间**。
            # 旧版一律用 busy 缺省值（180s），而冷却档（上一轮刚算完、COOLDOWN_SEC=195s）
            # 实际有精确的 ``retry_after``；吞掉它会让调用方在冷却快结束时仍盲等三分钟。
            # 锁被真占（另一进程在轮询）时没有剩余时间估计，退回缺省值。
            #
            # 2026-10-28 P1-1：附带 ``holder``（当前 token 的 tag）。调用侧据此
            # 判断「占着槽的是不是同一个 alpha」——同 alpha 可以等待而不是立即放弃。
            try:
                from wqb.correlation_slot import holder_tag as _holder_tag
                holder = _holder_tag()
            except Exception:
                holder = None
            return {
                'acquired': False,
                'backend': 'file',
                'lock_key': "correlation.lock.json",
                'retry_after': info.get("retry_after")
                               or self._brain_correlation_busy_retry_after_seconds,
                'cooldown': bool(info.get("cooldown")),
                'holder': holder,
            }
        if not info.get("token"):
            # 写锁目录不可写 → degraded，无法承担跨进程互斥 → 退回进程内锁
            self.log(
                f"[corr-lock] 跨进程文件锁 degraded（{op_name}），降级为进程内锁",
                "WARNING",
            )
            return None

        self.log(
            f"[corr-lock] Acquired cross-process file lock for {op_name} "
            f"(ttl={self._brain_correlation_lock_ttl_seconds}s)",
            "INFO",
        )
        return {
            'acquired': True,
            'backend': 'file',
            'lock_key': info["token"],
            'lock_token': info["token"],
            '_flock_release': _slot_release,
        }

    async def _release_brain_correlation_lock(self, lock_info: Dict[str, Any], op_name: str,
                                              *, cooldown: bool = True, seconds=None):
        """释放两级锁。**冷却按结果分流（2026-10-28 P0-1）**：

        - ``cooldown=False``：本次没有触发计算（立即拿到既有值 / 4xx 终态 / 异常）
          ⇒ 不写冷却，下一个调用可直接拿槽；
        - ``seconds=x``：真触发了一次计算 ⇒ 写平台 ``Retry-After`` 或 195s；
        - ``cooldown=True, seconds=None``：旧语义（195s），保留给未分类路径。

        注意：冷却只在 **file backend** 释放时写（本地 backend 没有跨进程互斥，
        写冷却会让本进程自己也白等；且它本来就只是降级形态）。
        """
        if not lock_info or not lock_info.get('acquired'):
            return
        backend = lock_info.get('backend')

        if backend == 'file':
            try:
                release_fn = lock_info.get('_flock_release')
                if release_fn is None:  # 兜底：重新导入（走 correlation_slot 才有冷却语义）
                    from wqb.correlation_slot import release as release_fn  # noqa: WPS440
                release_fn(lock_info['lock_key'], cooldown=cooldown, seconds=seconds)
                self.log(
                    f"[corr-lock] Released cross-process file lock for {op_name} "
                    f"(cooldown={'%.0fs' % seconds if (cooldown and seconds) else ('on' if cooldown else 'off')})",
                    "INFO",
                )
            except Exception as e:  # noqa: BLE001
                self.log(f"[corr-lock] File lock release failed for {op_name}: {e}", "WARNING")
            # 两级都拿到时，进程内锁也要还（否则本进程后续查询永远 busy）
            if lock_info.get('local_lock_held') and self._brain_correlation_local_lock.locked():
                self._brain_correlation_local_lock.release()
                self._corr_local_holder_op = None
                self.log(f"[corr-lock] Released local correlation lock for {op_name}", "INFO")
            return

        if backend == 'local' and self._brain_correlation_local_lock.locked():
            self._brain_correlation_local_lock.release()
            self._corr_local_holder_op = None
            self.log(f"[corr-lock] Released local correlation lock for {op_name}", "INFO")

    def _log_corr_busy(self, message: str, every_seconds: float = 60.0) -> None:
        """打「相关性槽被占」日志，但**按时间节流**（2026-10-28 P2-7）。

        实测 14h 日志里有 1,020 条 busy 行——调用方（Agent 循环）每几秒重试一次，
        每次打一行 INFO，日志被刷穿、真正的取数结论被埋掉。节流后每
        ``every_seconds`` 才打一行，并在行尾带上期间被吞掉的条数。
        """
        now = time.time()
        last = float(getattr(self, '_corr_busy_log_at', 0.0) or 0.0)
        suppressed = int(getattr(self, '_corr_busy_log_suppressed', 0) or 0)
        if now - last < every_seconds:
            self._corr_busy_log_suppressed = suppressed + 1
            return
        self._corr_busy_log_at = now
        self._corr_busy_log_suppressed = 0
        if suppressed:
            message = f"{message}（期间另有 {suppressed} 次 busy 未打日志）"
        self.log(message, "INFO")


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
