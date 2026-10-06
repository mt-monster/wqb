# -*- coding: utf-8 -*-
"""ApiCacheMixin — 平台查询结果的通用 KV 缓存（2026-10-06 建，替代 Redis）。

背景（2026-10-06 prod 测量机制审计）：``brain_mixin_transport.py`` 的
``_get_cached_data`` / ``_set_cached_data`` **唯一后端是 Redis**，而本机 Redis 常未启动
（``redis_client=None`` → 读写静默 no-op）。后果不是"变慢"，是**缓存整条失效**：

- prod 相关性每次查询都重打平台**单账号单并发**队列（每颗 1-5 分钟）；
- 库里已有 737 条实测 prod，查询路径却一眼都不看；
- 多会话并存时互相排队，表现为"查 prod 一直等"。

更隐蔽的是第二个坑：Redis 那条路径的 TTL 是 **7 天**，而全库 prod 保鲜纪律是
**48h**（实证 EUR ``le8Y68K2`` 0.6929 → 0.9932）。也就是说**把 Redis 修好反而更危险**
——默认 ``refresh=False`` 会拿一周前的陈值去过 0.7 的闸。

故本模块把通用缓存落到 ``data/wqb.db::api_cache``：

- **SQLite 跨进程共享**：多个 MCP 进程（wq-brain-http / wqb-db）读同一份文件，
  这正是 Redis 当初被选中的唯一理由，SQLite 同样满足且不需要额外服务；
- **TTL 由调用方显式传**：不再有"默认 7 天"这种与业务纪律脱节的隐式值；
- **过期即未命中**：读侧按 ``expires_at`` 过滤，过期行视同不存在（回源平台）；
- **懒加载 + 失败降级**：MCP 侧导入失败只告警一次并置哨兵，**绝不阻断查询主流程**。

契约：

- ``get_api_cache(key)``：命中且未过期 → dict；否则 ``None``；
- ``set_api_cache(key, data, ttl)``：upsert，``ttl=None`` 表示不过期；
- ``prune_api_cache()``：清理过期行（运维用，不在热路径自动调用）。
"""
from __future__ import annotations

import json
import time
from typing import Any, Dict, Optional

from ._common import _now

_CACHE_COLUMNS = "cache_key, payload, expires_at, created_at, updated_at"


class ApiCacheMixin:
    """``api_cache`` 表的读写。平台查询结果的通用 KV 缓存后端。"""

    def get_api_cache(self, cache_key: str) -> Optional[Dict[str, Any]]:
        """读一条缓存；不存在或**已过期**返回 ``None``（过期行视同不存在）。"""
        if not cache_key:
            return None
        cur = self.connection.cursor()
        cur.execute(
            f"SELECT payload, expires_at FROM api_cache WHERE cache_key=?",
            (str(cache_key),),
        )
        row = cur.fetchone()
        if not row:
            return None
        exp = row[1]
        if exp is not None:
            try:
                if float(exp) <= time.time():
                    return None
            except (TypeError, ValueError):
                return None
        try:
            val = json.loads(row[0])
        except (TypeError, ValueError):
            return None
        return val if isinstance(val, dict) else None

    def set_api_cache(
        self,
        cache_key: str,
        data: Dict[str, Any],
        ttl: Optional[int] = None,
    ) -> Dict[str, Any]:
        """写一条缓存（upsert）。``ttl`` 为秒，``None`` / ``<=0`` 表示不过期。

        ``data`` 非 dict 时按 ``{"value": data}`` 包装，保证读侧类型稳定。
        """
        if not cache_key:
            return {"skipped": "no_cache_key"}
        payload = data if isinstance(data, dict) else {"value": data}
        try:
            body = json.dumps(payload, ensure_ascii=False)
        except (TypeError, ValueError) as e:
            return {"skipped": f"unserializable:{type(e).__name__}"}
        exp = None if (ttl is None or int(ttl) <= 0) else time.time() + int(ttl)
        now = _now()
        cur = self.connection.cursor()
        cur.execute(
            "INSERT INTO api_cache (cache_key, payload, expires_at, created_at, updated_at) "
            "VALUES (?,?,?,?,?) "
            "ON CONFLICT(cache_key) DO UPDATE SET "
            "  payload=excluded.payload,"
            "  expires_at=excluded.expires_at,"
            "  updated_at=excluded.updated_at",
            (str(cache_key), body, exp, now, now),
        )
        self.connection.commit()
        return {"action": "upserted", "cache_key": str(cache_key), "expires_at": exp}

    def prune_api_cache(self) -> Dict[str, Any]:
        """删除已过期行（运维用）。返回 ``{"deleted": n}``。"""
        cur = self.connection.cursor()
        cur.execute("DELETE FROM api_cache WHERE expires_at IS NOT NULL AND expires_at <= ?",
                    (time.time(),))
        n = cur.rowcount if cur.rowcount and cur.rowcount > 0 else 0
        self.connection.commit()
        return {"deleted": n}
