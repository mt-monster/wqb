# -*- coding: utf-8 -*-
"""CorrCacheMixin — 平台相关性查询结果的**单一权威存储**（2026-10-04 建，2026-10-05 单源化）。

BRAIN 的相关性接口是**单账号单并发**，每颗 alpha 首次计算要 1-5 分钟，因此「查过就不再查」
是硬需求。MCP 侧的自相关（self）有文件缓存（``downloads/os_pnl_pool_*.pkl``），但 prod
结果此前唯一缓存后端是 Redis；本机 Redis 常未启动 → ``redis_client=None`` → 缓存整条失效
→ 多会话各自重复打平台单并发队列。

本模块把 prod/self 结果落到 ``data/wqb.db`` 的 ``alpha_corr_cache`` 表，并作为
**全库唯一的 prod 真值来源**（2026-10-05）：

- **与 ``alphas`` 表解耦**：仿真 alpha（UNSUBMITTED）不在 ``alphas`` 里
  （实测 ``E5RaV7Rr`` / ``O08kz5Mv`` 均 NOT IN alphas），用独立表才能缓存；
- **SQLite 天生跨进程共享**：多个 MCP 进程读同一份文件，无需 Redis；
- **让「查过就有」成立**：避免重复占用平台单并发队列。

单源化背景（三表并存的实际代价）：此前同一颗 alpha 的 prod 存在三处且**无同步契约**——
``alpha_corr_cache``（``check_correlation`` 内部写，196 行）、``alphas.prod_correlation``
（收批/首筛写，561 行）、``submit_ready.prod``（盘点写，队列内）。已发生实际事故：
6 颗 GBR 的实测值躺在 ``alphas`` 里而 ``alpha_corr_cache`` 缺条目 → 盘点判「无新鲜度依据」
→ 强制重打平台队列。**修复当时是手工 backfill，不是机制**。故本表升为权威，
``alphas`` 由 :meth:`CorrCacheMixin.set_corr_cache` **联动写入**（见 ``mirror_to_alphas``），
读写优先走 :meth:`get_corr_authoritative`。

.. note:: 2026-10-06 更正：原文档写「``alphas`` / ``submit_ready`` 均联动」，实际
   ``set_corr_cache`` **只联动 ``alphas``**；``submit_ready.prod`` 仍由盘点工具
   （``tools/submit_inventory.py``）自行写入。另：本 mixin 直至 2026-10-06 才真正
   挂上 ``CampaignStore``（此前定义了但没挂载，任何"写权威表"的调用都会
   AttributeError），见 ``docs/design/prod_corr_persistence_design_20260918.md`` §6.6。

契约（与 :meth:`BacktestMixin.persist_correlation` 同口径）：

- 相关性值须落在 ``[0, 1]``，否则按「没有」处理（防空值与异常值污染）；
- :meth:`set_corr_cache` 幂等：同值重复写不改变结果；
- **保鲜期 48h**（:data:`CORR_FRESH_HOURS`）：生产池会漂移（实证 EUR ``le8Y68K2``
  0.6929 → 0.9932；``E5pbM7Nm`` 0.6678 → 0.981），超过保鲜期的值只能用于排序参考，
  提交前必须 ``check_correlation(refresh=True)`` 当场终验。**过期不等于作废**，
  故本表不做物理清理，只在读取侧标 ``stale``。
"""
from __future__ import annotations

import json
from typing import Any, Dict, List, Optional

from ._common import _now
from ._backtest import _corr_value

_CACHE_COLUMNS = (
    "alpha_id, prod_correlation, self_correlation, prod_records, source, checked_at"
)

#: prod/self 的保鲜期小时数（单一事实源）。与 ``tools/submit_inventory.py --stale-hours``
#: 默认值、``wqb-db get_alpha_corr_metrics(stale_after_hours=48)`` 同口径，此前是三处
#: 各写各的默认值。现导出供 MCP 层与工具层统一引用，避免再漂。
CORR_FRESH_HOURS = 48.0

#: ``source`` / ``prod_corr_source`` 的**登记词表**（单一事实源）。
#:
#: 2026-10-05 审计：``alphas.prod_corr_source`` 实际有 6 个取值，其中 3 个
#: （``prod_first`` / ``p0_1_verify_20260923`` / ``raw_poll``）是**带日期或简写的自由文本**，
#: 未经登记，无法判断可信度。新写入一律经 :func:`normalize_corr_source` 收敛；
#: 自由文本映射到 ``LEGACY`` 并附原值到 ``detail``，不丢溯源信息。
#:
#: 语义分层（与 ``docs/design/prod_corr_persistence_design_20260918.md`` 一致）：
#:   PLATFORM   平台权威实测值
#:   BACKFILL   从其它本地存储（alphas / checkpoint）搬运，非本轮平台实测
#:   TOOL       本地工具实测（triage / 首筛 / 复核器）
#:   MANUAL     人工录入
#:   LEGACY     历史自由文本，无法归类（保留原值于 detail）
CORR_SOURCES = (
    "platform_sync",       # 平台权威（收批同步 / check_correlation 落库）
    "platform_cached",     # 命中缓存，未回源平台
    "check_correlation",   # MCP check_correlation 实测
    "prod_first_screen",   # tools/prod_first_screen.py
    "prod_recheck",        # PROD_BLOCKED 实时复核器
    "triage_local",        # 本地抽测（对近期孪生体失明，会低估）
    "alphas_backfill",     # 从 alphas 表搬运进本表
    "checkpoint_backfill",  # 从 checkpoint（logs/_submit_inventory.json）搬运
    "manual",              # 人工录入
    "legacy",              # 历史自由文本，原值见 detail
)

#: 历史自由文本 → 登记词表。键一律小写。
_LEGACY_SOURCE_ALIASES = {
    "prod_first": "prod_first_screen",
    "prod_firstscreen": "prod_first_screen",
    "raw_poll": "legacy",
    "api": "platform_sync",
    "verify": "platform_sync",
    "submit_verdict": "platform_sync",
    "alphas": "alphas_backfill",
    "alphas-backfill": "alphas_backfill",
    "platform": "platform_sync",
    "prod_blocked_recheck": "prod_recheck",
}


def normalize_corr_source(raw: Any) -> Dict[str, Any]:
    """把任意 ``source`` 输入收敛到 :data:`CORR_SOURCES` 词表。

    返回 ``{"source": <登记值>, "detail": <原值或 None>}``。
    ``detail`` 仅在原值不是合法登记值时非空——此时登记值为 ``legacy``，
    **原值不丢**（溯源信息保留在 detail 里）。
    """
    if raw is None or str(raw).strip() == "":
        return {"source": "manual", "detail": None}
    s = str(raw).strip()
    if s in CORR_SOURCES:
        return {"source": s, "detail": None}
    low = s.lower()
    if low in CORR_SOURCES:
        return {"source": low, "detail": None}
    alias = _LEGACY_SOURCE_ALIASES.get(low)
    if alias:
        return {"source": alias, "detail": s if alias != s else None}
    return {"source": "legacy", "detail": s}


def corr_age_hours(checked_at: Any, now: Optional[str] = None) -> Optional[float]:
    """``checked_at`` 距今小时数；无法解析返回 ``None``（**不是 0**，别把「未知」当「新鲜」）。"""
    if not checked_at:
        return None
    from datetime import datetime
    try:
        dt = datetime.fromisoformat(str(checked_at).replace("Z", "+00:00"))
    except (TypeError, ValueError):
        return None
    ref = None
    if now:
        try:
            ref = datetime.fromisoformat(str(now).replace("Z", "+00:00"))
        except (TypeError, ValueError):
            ref = None
    if ref is None:
        ref = datetime.now()
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=ref.tzinfo)
    if ref.tzinfo is not None and dt.tzinfo is None:
        dt = dt.replace(tzinfo=ref.tzinfo)
    try:
        return round((ref - dt).total_seconds() / 3600.0, 2)
    except TypeError:
        return None


class CorrCacheMixin:
    """``alpha_corr_cache`` 表的读写。**全库 prod 的单一权威**。

    与 ``alphas`` 表分开存：仿真阶段的 alpha 尚未进 ``alphas``，
    但仍需要缓存其相关性取值。
    """

    @staticmethod
    def _row_to_corr(row) -> Dict[str, Any]:
        prod = _corr_value(row[1])
        self_corr = _corr_value(row[2])
        records: Optional[List[Any]] = None
        if row[3]:
            try:
                records = json.loads(row[3])
            except (TypeError, ValueError):
                records = None
        age = corr_age_hours(row[5])
        return {
            "alpha_id": row[0],
            "max": prod,
            "prod_correlation": prod,
            "self_correlation": self_corr,
            "records": records,
            "source": row[4],
            "checked_at": row[5],
            # age_hours 缺时间戳时是 None（未知），**不是 0**——
            # 0 会被 stale 判成「刚测过」，把最危险的情形说成最安全的。
            "age_hours": age,
            "stale": (age is None) or (age > CORR_FRESH_HOURS),
            "fresh": (age is not None) and (age <= CORR_FRESH_HOURS),
            "fresh_hours": CORR_FRESH_HOURS,
        }

    def get_corr_cache(self, alpha_id: str) -> Optional[Dict[str, Any]]:
        """读一条缓存；不存在返回 ``None``。

        ``max`` 字段与 ``check_correlation`` 的返回口径对齐，便于直接回填。
        返回值带 ``age_hours`` / ``stale`` / ``fresh``（保鲜期 :data:`CORR_FRESH_HOURS`）。
        """
        if not alpha_id:
            return None
        cur = self.connection.cursor()
        cur.execute(
            f"SELECT {_CACHE_COLUMNS} FROM alpha_corr_cache WHERE alpha_id=?",
            (str(alpha_id),),
        )
        row = cur.fetchone()
        if not row:
            return None
        return self._row_to_corr(row)

    def get_corr_authoritative(self, alpha_id: str) -> Optional[Dict[str, Any]]:
        """**单源读**：先查权威表 ``alpha_corr_cache``，缺则回落到 ``alphas`` 表。

        回落是必要的——单源化前 ``alphas`` 有 561 行历史 prod 而权威表只有 196 行，
        两者无同步契约。回落时 ``from_alphas=True``，调用方可据此判断
        「这是搬运来的历史值，可能需要 refresh」。

        新写入一律走 :meth:`set_corr_cache`（它联动 ``alphas``），故本回落路径
        只会随存量消化而变薄。
        """
        row = self.get_corr_cache(alpha_id)
        if row and (row.get("prod_correlation") is not None
                    or row.get("self_correlation") is not None):
            return row
        try:
            cur = self.connection.cursor()
            cur.execute(
                "SELECT prod_correlation, self_correlation, corr_checked_at, "
                "prod_corr_source FROM alphas WHERE alpha_id=? LIMIT 1",
                (str(alpha_id),),
            )
            r = cur.fetchone()
        except Exception:  # noqa: BLE001 - alphas 表可能不存在（纯缓存库）
            return row
        if not r:
            return row
        prod = _corr_value(r[0])
        self_corr = _corr_value(r[1])
        if prod is None and self_corr is None:
            return row
        age = corr_age_hours(r[2])
        out = self._row_to_corr((str(alpha_id), prod, self_corr, None,
                                 normalize_corr_source(r[3])["source"], r[2]))
        out["from_alphas"] = True
        return out

    def set_corr_cache(
        self,
        alpha_id: str,
        prod: Optional[float] = None,
        self_: Optional[float] = None,
        records: Any = None,
        source: str = "platform_sync",
        mirror_to_alphas: bool = True,
        checked_at: Optional[str] = None,
    ) -> Dict[str, Any]:
        """写一条缓存（upsert，幂等）——**全库 prod 的唯一写入口**。

        任一列传入 ``None`` 时**保留旧值**（``COALESCE``），
        这样「只补 prod」不会把已存的 self 抹掉。

        ``source`` 经 :func:`normalize_corr_source` 收敛到登记词表（2026-10-05）。

        ``mirror_to_alphas=True``（默认）时联动写 ``alphas`` 的 prod/self/source/时间戳
        ——这一步正是 2026-10-05 单源化补的同步契约：三表并存且无同步时，
        ``check_correlation`` 写权威表而 ``alphas`` 缺条目，盘点会判「无新鲜度依据」
        强制重打平台单并发队列（实测 6 颗 GBR 因此被重复测量）。
        联动失败（alpha 不在 ``alphas`` / 无该表）**不影响本表写入**，结果记在 ``mirror``。
        """
        if not alpha_id:
            return {"skipped": "no_alpha_id"}

        p = _corr_value(prod)
        s = _corr_value(self_)
        recs_json: Optional[str] = None
        if records is not None:
            try:
                recs_json = json.dumps(records, ensure_ascii=False)
            except (TypeError, ValueError):
                recs_json = None

        if p is None and s is None and recs_json is None:
            return {"skipped": "no_valid_value", "alpha_id": str(alpha_id)}

        norm = normalize_corr_source(source)
        src = norm["source"]
        # ⚠ checked_at 必须可显式传入：回填历史值时若用 now()，647 条存量会被
        # 一律标成「刚测过」，保鲜期判据彻底失真（实测 fresh=848/stale=0）。
        # 搬运场景传原始测量时间戳；正常测量场景留 None 用当前时间。
        now = checked_at or _now()
        cur = self.connection.cursor()
        cur.execute(
            "INSERT INTO alpha_corr_cache "
            "(alpha_id, prod_correlation, self_correlation, prod_records, "
            " source, checked_at, created_at, updated_at) "
            "VALUES (?,?,?,?,?,?,?,?) "
            "ON CONFLICT(alpha_id) DO UPDATE SET "
            "  prod_correlation=COALESCE(excluded.prod_correlation, prod_correlation),"
            "  self_correlation=COALESCE(excluded.self_correlation, self_correlation),"
            "  prod_records=COALESCE(excluded.prod_records, prod_records),"
            "  source=excluded.source,"
            "  checked_at=excluded.checked_at,"
            "  updated_at=excluded.updated_at",
            (str(alpha_id), p, s, recs_json, src, now, now, now),
        )
        self.connection.commit()
        out = {
            "action": "upserted",
            "alpha_id": str(alpha_id),
            "prod_correlation": p,
            "self_correlation": s,
            "source": src,
            "checked_at": now,
        }
        if norm["detail"]:
            out["source_detail"] = norm["detail"]
        if mirror_to_alphas:
            # ⚠ overwrite=True 是 2026-10-06 修复：本方法语义就是「全库 prod 唯一写入口」，
            # 权威表已拿到新的平台实测值，镜像也必须一起覆盖，否则 alphas 里
            # 会留着旧值 —— 消费者走 alphas 表（select_ra_basket / prod_saturation_gate /
            # submit_queue / prod_first_screen）会读到过期数据、把新测过的 alpha 又当成
            # 「未测」重新排队（2026-10-06 实测 3 行 >0.01 冲突：E5pbM7Nm / VkaZYdbG /
            # wpZ3RP96）。persist_correlation 的 overwrite 默认值是 False（NULL-only），
            # 那是为本地 triage 单独写 alphas 时保留平台权威值设计的；此处不适用。
            try:
                out["mirror"] = self.persist_correlation(
                    str(alpha_id), prod=p, self_=s, source=src, overwrite=True)
            except Exception as e:  # noqa: BLE001 - 联动失败不阻断权威表写入
                out["mirror"] = {"error": f"{type(e).__name__}: {e}"}
        return out

    def normalize_legacy_sources(self) -> Dict[str, Any]:
        """把权威表里**存量**的未登记 ``source`` 收敛到词表（2026-10-05）。

        ``set_corr_cache`` 写新值时已经收敛，但本表建立之前写入的行
        （实测 ``platform`` 191 行 / ``alphas-backfill`` 6 行）未经此路径。
        这些值读出来会让消费方判不出可信度，故提供一次性治理。

        ⚠ ``manual`` 的成因与治理：不少历史行来源为空，回填时被归到 ``manual``
        ——但「来源不明」不等于「人工录入」，会误导消费方。这里按
        「来源 + 时间戳是否都缺」分派：都缺→ ``legacy``（确实无法归类），
        否则→ ``alphas_backfill``（值来自 alphas 的历史搬运）。

        幂等：已收敛的行不重复改写。返回 ``{"scanned", "changed", "map"}``。
        """
        cur = self.connection.cursor()
        rows = cur.execute(
            "SELECT c.alpha_id, c.source, c.checked_at, a.corr_checked_at "
            "FROM alpha_corr_cache c LEFT JOIN alphas a ON a.alpha_id = c.alpha_id"
        ).fetchall()
        changed, amap = 0, {}
        for r in rows:
            cur_src = r["source"]
            if cur_src == "manual":
                if not r["checked_at"]:
                    new_src = "legacy"              # 来源+时间都缺 → 无法归类
                else:
                    new_src = "alphas_backfill"      # 有测量时间但来源空 → 历史搬运
            else:
                new_src = normalize_corr_source(cur_src)["source"]
            if new_src == cur_src:
                continue
            cur.execute(
                "UPDATE alpha_corr_cache SET source=? WHERE alpha_id=?",
                (new_src, r["alpha_id"]))
            amap[f"{cur_src} -> {new_src}"] = amap.get(f"{cur_src} -> {new_src}", 0) + 1
            changed += 1
        self.connection.commit()
        return {"scanned": len(rows), "changed": changed, "map": amap}

    def backfill_from_alphas(self, limit: int = 0) -> Dict[str, Any]:
        """把 ``alphas`` 里「有 prod 但权威表缺条目」的历史值搬进权威表（幂等）。

        2026-10-05 单源化的一次性消化动作，可重复跑。**不覆盖**权威表已有条目
        （权威值优先）。返回 ``{scanned, migrated, skipped_invalid, rows}``。
        """
        cur = self.connection.cursor()
        sql = (
            "SELECT a.alpha_id, a.prod_correlation, a.self_correlation, "
            "       a.corr_checked_at, a.prod_corr_source "
            "FROM alphas a LEFT JOIN alpha_corr_cache c ON c.alpha_id = a.alpha_id "
            "WHERE c.alpha_id IS NULL "
            "  AND (a.prod_correlation IS NOT NULL OR a.self_correlation IS NOT NULL)"
        )
        if limit:
            sql += f" LIMIT {int(limit)}"
        rows = cur.execute(sql).fetchall()
        migrated, skipped = [], []
        for r in rows:
            # ★ 搬运行的 source 标 ``alphas_backfill``（**值来自 alphas**，不是人工录入）。
            # 原来源为空时不能落到 ``manual``——那会把「来源不明」说成「人工录入」，
            # 实测 457 条历史行正是这种情况。原来源有值时保留其归一化结果
            # （如 ``prod_first_screen``），它比"搬运"更能说明值是怎么来的。
            src = normalize_corr_source(r[4])["source"]
            if r[4] is None or str(r[4]).strip() == "":
                src = "alphas_backfill"
            elif src == "manual":
                src = "alphas_backfill"
            res = self.set_corr_cache(
                r[0], prod=_corr_value(r[1]), self_=_corr_value(r[2]),
                source=src,
                mirror_to_alphas=False,   # 值就是从 alphas 搬来的，无需回写
                # ★ 搬运**沿用原始测量时间戳**：用 now() 会把 647 条存量一律
                # 标成「刚测过」，保鲜期判据失真（prod 会随生产池漂移）。
                # 原时间为空时留空——get_corr_cache 会把「无时间戳」判为 stale，
                # 这正是「不知道新鲜度」应有的诚实结论。
                checked_at=r[3],
            )
            (skipped if res.get("skipped") else migrated).append(r[0])
        return {"scanned": len(rows), "migrated": len(migrated),
                "skipped_invalid": len(skipped), "rows": migrated[:50]}

    def list_corr_cache(self, alpha_ids: List[str]) -> Dict[str, Dict[str, Any]]:
        """批量读缓存，返回 ``{alpha_id: 记录}``（缺失的键不出现）。"""
        ids = [str(a) for a in (alpha_ids or []) if a]
        if not ids:
            return {}
        out: Dict[str, Dict[str, Any]] = {}
        cur = self.connection.cursor()
        # 分块避免 SQLite 变量上限（默认 999）
        for i in range(0, len(ids), 500):
            chunk = ids[i:i + 500]
            marks = ",".join("?" * len(chunk))
            cur.execute(
                f"SELECT {_CACHE_COLUMNS} FROM alpha_corr_cache WHERE alpha_id IN ({marks})",
                chunk,
            )
            for row in cur.fetchall():
                rec = self._row_to_corr(row)
                out[row[0]] = rec
        return out

    def get_corr_authoritative_batch(
        self, alpha_ids: List[str],
    ) -> Dict[str, Dict[str, Any]]:
        """批量单源读（2026-10-06 新增）：先查 ``alpha_corr_cache``，缺则回落到 ``alphas``。

        与 :meth:`get_corr_authoritative` 语义一致，但一次 SQL 拿全，适合消费者
        一次处理上百个候选的场景（``select_ra_basket.prod_freshness_index``、
        ``prod_saturation_gate`` 等）。**修复的是**：只查 alphas 表会让权威表里
        有、alphas 里无（或旧）的 191 行缓存不可见，被消费者判成「未测」
        重复排队（历史「6 颗 GBR 重复测量」就是这条链路的产物）。

        返回值：``{alpha_id: 记录}``；两条都查不到的 id 不出现在结果里。
        权威表已给的行标 ``from_alphas=False``；仅 alphas 有的行标 ``from_alphas=True``。
        分块 500，避免 SQLite 变量上限。
        """
        ids = [str(a) for a in (alpha_ids or []) if a]
        if not ids:
            return {}
        out: Dict[str, Dict[str, Any]] = {}
        cache_hits = self.list_corr_cache(ids)
        for aid, rec in cache_hits.items():
            if rec.get("prod_correlation") is not None or rec.get("self_correlation") is not None:
                rec.setdefault("from_alphas", False)
                out[aid] = rec
        missing = [a for a in ids if a not in out]
        if not missing:
            return out
        try:
            cur = self.connection.cursor()
            for i in range(0, len(missing), 500):
                chunk = missing[i:i + 500]
                marks = ",".join("?" * len(chunk))
                cur.execute(
                    f"SELECT alpha_id, prod_correlation, self_correlation, "
                    f"corr_checked_at, prod_corr_source FROM alphas "
                    f"WHERE alpha_id IN ({marks})",
                    chunk,
                )
                for r in cur.fetchall():
                    aid, prod, self_corr, checked_at, src = r
                    prod_v = _corr_value(prod)
                    self_v = _corr_value(self_corr)
                    if prod_v is None and self_v is None:
                        continue
                    rec = self._row_to_corr((str(aid), prod_v, self_v, None,
                                             normalize_corr_source(src)["source"], checked_at))
                    rec["from_alphas"] = True
                    out[aid] = rec
        except Exception:  # noqa: BLE001 - alphas 表可能不存在（纯缓存库）
            return out
        return out
