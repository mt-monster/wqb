"""MCP 侧 alpha 落库 — 治本「平台有、本地无」（2026-10-28）。

## 为什么需要这个模块

``tools_sim.create_simulation`` 原先只把表达式提交到平台、把结果返回给调用方，
**对 ``backtest_results`` / ``CampaignStore`` 零引用**。于是通过 MCP 单条跑（或网页
手跑）的 alpha：**平台有、本地无** —— 面板（读本地库）看不到、挖掘产率被低估。
实测 2026-10-28：当日 ``alpha_corr_cache`` 新登记 41 颗，其中 18 颗在
``backtest_results`` 里没有任何记录，全部集中在 MCP 直跑的时段。

修法：**在拿到平台 alpha 响应的地方顺手写库**。写入口复用
``wqb.store.CampaignStore.upsert_backtest_rows``（全库唯一写入口，
``ON CONFLICT(alpha_id)`` 幂等 + COALESCE 保留旧指标），不写裸 SQL。

## 三条硬约束（改这个文件前先读）

1. **绝不覆盖已有行。** ``upsert_backtest_rows`` 的 ``region=excluded.region,
   wave=excluded.wave`` 是**直接覆盖**（不像其它列有 COALESCE）。若让 MCP 写一次，
   会把 campaign 落下的正确 ``wave``（如 ``150``）改写成 ``mcp-20261028``，产率
   统计跟着错。所以插入前先按 ``alpha_id`` 查存在性，命中直接返回 ``exists``。
2. **绝不抛异常。** 所有分支 try/except 兜住，失败只 log 并返回 ``ok=False``。
   落库是**旁路能力**：库被锁、磁盘满、schema 变了，都不能把仿真结果弄丢——
   调用方拿到的必须是平台原始返回值，一个字都不改。
3. **独立 wave ``mcp-YYYYMMDD``。** ``backtest_results.expression_id`` 是 NOT NULL，
   所以每行必须挂到一条 ``expressions`` 记录上（``upsert_backtest_rows`` 会自动
   建）。用独立 wave 让这批数据在按 wave 统计时自成一格，不混进 campaign 的波次。

## 与 ``ra_failed_checks`` 的关系

``upsert_backtest_rows`` 用 ``ra_failed_names(row)`` 推导该列。它会优先吃**完整
未分桶的 ``checks``**（每项都带 ``result``）—— 那是权威档（``wqb.config`` 的
RA 唯一定义）。所以本模块在拿到平台原始响应时**整段透传 ``is.checks``**；
只有拿到 slim 结果（分桶后的 checks）时，才退到用 ``ra.failed_ra_count``
预判「已知全过 → ``[]``」（``'[]'`` 与 ``NULL`` 的语义差异见 store/_backtest.py
的 ``ra_failed_names`` docstring，2026-10-23 P0-3）。
"""
from __future__ import annotations

import datetime as _dt
import os
from typing import Any, Dict, List, Optional, Tuple

from mcp_core import brain_client, logger

#: 落库总开关。``MCP_ALPHA_PERSIST=0`` 可一键关掉（回滚用，不必改代码）。
_ENV_SWITCH = "MCP_ALPHA_PERSIST"

#: wave 前缀。按日落一个 wave，便于把「MCP 直跑」与 campaign 波次区分开。
WAVE_PREFIX = "mcp"

#: slim.metrics 的键 → ``backtest_results`` 列名。未列出的键不进库
#: （``sharpe_se`` / ``sharpe_t_stat`` 等诊断量只留在 payload 里）。
_METRIC_MAP = {
    "sharpe": "sharpe",
    "fitness": "fitness",
    "turnover": "turnover",
    "margin": "margin",
    "returns": "returns",
    "drawdown": "drawdown",
    "two_year_sharpe": "two_year_sharpe",
    "sub_universe_sharpe": "sub_universe_sharpe",
    "robust_universe_sharpe": "robust_universe_sharpe",
    "risk_neutralized_sharpe": "risk_neutralized_sharpe",
    "longCount": "long_count",
    "shortCount": "short_count",
    "pnl": "pnl",
    "bookSize": "book_size",
}

_STORE = None
_STORE_ERR: Optional[str] = None
_STORE_TRIED = False


def _enabled() -> bool:
    return os.environ.get(_ENV_SWITCH, "1").strip().lower() not in ("0", "false", "no", "off")


def _today() -> str:
    return _dt.date.today().strftime("%Y%m%d")


def wave_name() -> str:
    """本次落库使用的 wave 名（``mcp-YYYYMMDD``，本地日期）。"""
    return "%s-%s" % (WAVE_PREFIX, _today())


def _get_store():
    """取 ``CampaignStore``。优先复用 brain_client 的缓存后端（同一实例、同一把锁）。

    不可用返回 ``None`` 并把原因记进 ``_STORE_ERR``——调用方据此返回 ``skipped``，
    绝不因为库不可用而影响仿真结果返回。
    """
    global _STORE, _STORE_ERR, _STORE_TRIED
    if _STORE_TRIED:
        return _STORE
    _STORE_TRIED = True
    # ① 复用 brain_client 已缓存的 store：MCP 里它本来就是跨线程共用 + RLock 串行化的，
    #    再开一条连接只会多一份 WAL 写者争用。
    try:
        be = getattr(brain_client, "_cache_backend", None)
        st = be() if callable(be) else None
        if st is not None:
            _STORE = st
            return _STORE
    except Exception as e:  # noqa: BLE001 — 空壳 client / 未初始化都按不可用处理
        _STORE_ERR = "cache_backend: %s: %s" % (type(e).__name__, e)
    # ② 兜底自建。
    try:
        from wqb.store import CampaignStore  # 延迟导入：MCP 包不强依赖 src

        _STORE = CampaignStore.from_workspace()
        _STORE_ERR = None
        return _STORE
    except Exception as e:  # noqa: BLE001
        _STORE_ERR = "CampaignStore: %s: %s" % (type(e).__name__, e)
        logger.warning("[alpha-persist] store 不可用，落库跳过：%s" % _STORE_ERR)
        return None


def _exists(store, alpha_id: str) -> bool:
    """该 alpha 是否已有回测行。命中即不写——避免覆盖 campaign 的 wave/region。"""
    lock = getattr(store, "_conn_lock", None)
    cur = None
    try:
        if lock is not None:
            with lock:
                cur = store.connection.cursor()
                cur.execute("SELECT 1 FROM backtest_results WHERE alpha_id=? LIMIT 1",
                            (alpha_id,))
                return cur.fetchone() is not None
        cur = store.connection.cursor()
        cur.execute("SELECT 1 FROM backtest_results WHERE alpha_id=? LIMIT 1", (alpha_id,))
        return cur.fetchone() is not None
    except Exception:  # noqa: BLE001 — 查不动就当不存在，让 upsert 的幂等兜住
        return False
    finally:
        if cur is not None:
            try:
                cur.close()
            except Exception:  # noqa: BLE001
                pass


def _as_slim(obj: Dict[str, Any]) -> Dict[str, Any]:
    """原始平台响应 → slim 形态；已经是 slim 形态就原样返回。

    判据：原始响应有 ``is`` / ``regular``，slim 形态有 ``metrics`` / ``ra``。
    """
    if not isinstance(obj, dict):
        return {}
    if isinstance(obj.get("is"), dict) or "regular" in obj:
        try:
            from mcp_core import _slim_alpha

            return _slim_alpha(obj)
        except Exception as e:  # noqa: BLE001
            logger.warning("[alpha-persist] slim 化失败：%s: %s" % (type(e).__name__, e))
            return {}
    return obj


def _as_text(v: Any) -> str:
    """从 str / dict 里取表达式或名称文本。

    平台的 ``combo`` / ``selection``（SUPER 类型）有时是 ``{"code": "..."}`` 而不是
    裸字符串——直接 ``.strip()`` 会炸 ``'dict' object has no attribute 'strip'``
    （2026-10-28 补录 22 颗时实测 6 颗 SUPER 全中此坑）。
    """
    if isinstance(v, str):
        return v.strip()
    if isinstance(v, dict):
        for k in ("code", "expression", "value", "text"):
            if isinstance(v.get(k), str):
                return v[k].strip()
    return ""


def _build_row(obj: Dict[str, Any]) -> Tuple[Optional[Dict[str, Any]], str, Optional[str],
                                             Optional[str], Dict[str, Any]]:
    """构造一行 ``backtest_results``。

    返回 ``(row, region, alpha_id, 跳过原因, slim)``。``slim`` 一并返回，
    让 exists 分支的状态同步不必重算一次。
    """
    if not isinstance(obj, dict):
        return None, "", None, "not a dict", {}
    alpha_id = obj.get("id") or obj.get("alpha_id")
    if not alpha_id:
        return None, "", None, "no alpha_id", {}

    slim = _as_slim(obj)
    if not slim:
        return None, "", alpha_id, "slim failed", {}

    settings = slim.get("settings") if isinstance(slim.get("settings"), dict) else {}
    region = _as_text(settings.get("region")).upper()
    if not region:
        return None, "", alpha_id, "no region in settings", slim

    code = _as_text(slim.get("code"))
    if not code:
        code = _as_text(obj.get("regular")) if not isinstance(obj.get("regular"), dict) \
            else _as_text(obj["regular"].get("code"))
    # SUPER 类型（combo / selection）没有 regular.code——用 combo/selection 兜，
    # 否则 upsert 会因为 code 为空静默丢弃整行（expr_id 取不到）。
    if not code:
        code = _as_text(obj.get("combo")) or _as_text(obj.get("selection"))
    if not code:
        return None, region, alpha_id, "no code (regular/combo/selection all empty)", slim

    row: Dict[str, Any] = {
        "id": alpha_id,
        "code": code,
        "status": slim.get("status"),
        # alphas 表的平台状态列（面板「已提交」列读它）；与 status 同源
        "platform_status": slim.get("status"),
        "stage": slim.get("stage"),
        "date_submitted": slim.get("dateSubmitted"),
        "universe": settings.get("universe"),
        "delay": settings.get("delay"),
        "neutralization": settings.get("neutralization"),
        "decay": settings.get("decay"),
        "truncation": settings.get("truncation"),
        "settings": settings,
    }
    metrics = slim.get("metrics") if isinstance(slim.get("metrics"), dict) else {}
    for src, dst in _METRIC_MAP.items():
        if metrics.get(src) is not None:
            row[dst] = metrics[src]
    if metrics.get("prodCorrelation") is not None:
        row["prod_corr"] = metrics["prodCorrelation"]
    if metrics.get("selfCorrelation") is not None:
        row["self_corr"] = metrics["selfCorrelation"]

    # RA 名单：完整 checks（每项带 result）优先交给 ra_failed_names 现算（权威档）；
    # 只有 slim（分桶）时才用 ra 预算值——且 failed_ra_count==0 必须写 []（已知全过），
    # 不能留空变成 NULL（= 未知）。
    checks = (obj.get("is") or {}).get("checks") if isinstance(obj.get("is"), dict) else None
    ladder = _ladder_sharpe(checks)
    if ladder is not None:
        # `upsert_backtest_rows` → `_write_alpha_row` 只从 row 里读这个键来镜像
        # `alphas.is_ladder_sharpe`；不放进 row 就永远写不进去（2026-10-28 补测发现）。
        row["is_ladder_sharpe"] = ladder
    if isinstance(checks, list) and checks and all(isinstance(c, dict) and "result" in c
                                                  for c in checks):
        row["checks"] = checks
    else:
        ra = slim.get("ra") if isinstance(slim.get("ra"), dict) else {}
        if ra.get("failed_ra_count") is not None:
            row["ra_failed_checks"] = (list(ra.get("ra_failed_checks") or [])
                                       if ra.get("failed_ra_count")
                                       else [])
    return row, region, alpha_id, None, slim


def _ladder_sharpe(checks: Any) -> Optional[float]:
    """从 ``is.checks`` 里取 ``IS_LADDER_SHARPE`` 的值（``alphas.is_ladder_sharpe`` 的来源）。"""
    for c in checks or []:
        if isinstance(c, dict) and c.get("name") == "IS_LADDER_SHARPE":
            v = c.get("value")
            return v if isinstance(v, (int, float)) else None
    return None


def _alpha_payload(slim: Dict[str, Any], region: str, code: str,
                   alpha_id: str, ladder: Optional[float] = None) -> Dict[str, Any]:
    """slim alpha → ``store.upsert_alpha_from_platform`` 的入参。

    只取该接口认识的键（多给的键会被忽略，但保持干净）。
    ``status`` 与 ``platform_status`` 同源：前者是本地工作流列、后者是平台回填列，
    这里都用平台值——`_merge_alpha_columns` 保证「生命周期不从已提交态回退」。
    """
    m = slim.get("metrics") if isinstance(slim.get("metrics"), dict) else {}
    s = slim.get("settings") if isinstance(slim.get("settings"), dict) else {}
    return {
        "alpha_id": alpha_id,
        "region": region,
        "expression": code,
        "universe": s.get("universe"),
        "delay": s.get("delay"),
        "neutralization": s.get("neutralization"),
        "sharpe": m.get("sharpe"),
        "fitness": m.get("fitness"),
        "turnover": m.get("turnover"),
        "two_year_sharpe": m.get("two_year_sharpe"),
        "is_ladder_sharpe": ladder,
        "status": slim.get("status"),
        "platform_status": slim.get("status"),
        "stage": slim.get("stage"),
        "date_submitted": slim.get("dateSubmitted"),
        "prod_correlation": m.get("prodCorrelation"),
        "self_correlation": m.get("selfCorrelation"),
    }


def _sync_alpha_row(store, slim: Dict[str, Any], region: str, code: str,
                    alpha_id: str, ladder: Optional[float] = None) -> bool:
    """把平台**状态/阶段/提交时间**同步进 ``alphas`` 表（不碰 ``backtest_results``）。

    ## 为什么 exists 分支还需要写

    ``backtest_results`` 的指标不该被 MCP 覆盖（campaign 的可能更全），但 alpha 的
    ``status`` 是**会变的**：``UNSUBMITTED → ACTIVE``（提交）、``ACTIVE →
    DECOMMISSIONED``（下架）。面板「已提交」列读的正是 ``alphas.platform_status``。
    整体跳过 ⇒ 状态永远停在落库那一刻的旧值。2026-10-28 实测：``e75pvoNz`` 在平台
    已 ACTIVE（dateSubmitted 13:28），本地 ``alphas`` 表却连行都没有，面板显示「未提交」。

    ## 只走 alphas 表

    ``upsert_alpha_from_platform`` 只写 ``alphas``（+ 必要的 region/dataset 字典表），
    不碰 ``backtest_results`` 的 wave/region，所以不存在「覆盖 campaign 波次」的风险
    （R28 那条只针对 ``upsert_backtest_rows``）。

    返回是否真的发生了写入（无差异时不产生 update，避免每次查看都写库）。
    """
    status = slim.get("status")
    stage = slim.get("stage")
    submitted = slim.get("dateSubmitted")
    lock = getattr(store, "_conn_lock", None)

    def _do() -> bool:
        cur = store.connection.cursor()
        try:
            cur.execute("SELECT platform_status, stage, date_submitted FROM alphas"
                        " WHERE alpha_id=?", (alpha_id,))
            row = cur.fetchone()
        finally:
            cur.close()
        if row is not None:
            same = ((row[0] or None) == (status or None)
                    and (row[1] or None) == (stage or None)
                    and (row[2] or None) == (submitted or None))
            if same:
                return False
        store.upsert_alpha_from_platform(
            _alpha_payload(slim, region, code, alpha_id, ladder))
        return True

    if lock is not None:
        with lock:
            return _do()
    return _do()


def persist_alpha(obj: Dict[str, Any], source: str = "mcp",
                 wave: Optional[str] = None) -> Dict[str, Any]:
    """把一份 alpha（平台原始响应或 slim 结果）落库。**永不抛异常**。

    ``wave`` 缺省用 ``mcp-YYYYMMDD``（本地日期）；补录历史数据时显式传，便于追溯。

    返回 ``{"ok", "action", "alpha_id", "reason", "wave", "status_synced"}``：
      - ``action="inserted"`` 新写入
      - ``action="exists"``   回测行已存在（指标不覆盖），但**状态已同步**到 ``alphas``；
        ``status_synced`` 说明这次有没有真的改（无差异时不写库）
      - ``action="skipped"``  信息不足（无 region / 无 code / store 不可用），重试也无用
      - ``action="error"``    落库时抛异常（脏数据 / 偶发库错）—— **可重试**，
        与 ``skipped`` 必须分开：补录脚本据此前者记账、后者重试
    """
    try:
        if not _enabled():
            return {"ok": False, "action": "skipped", "alpha_id": None,
                    "reason": "%s=0（落库已关闭）" % _ENV_SWITCH, "wave": None}
        row, region, alpha_id, why, slim = _build_row(obj)
        if row is None:
            return {"ok": False, "action": "skipped", "alpha_id": alpha_id,
                    "reason": why, "wave": None, "status_synced": False}
        store = _get_store()
        if store is None:
            return {"ok": False, "action": "skipped", "alpha_id": alpha_id,
                    "reason": _STORE_ERR or "store unavailable", "wave": None,
                    "status_synced": False}
        if _exists(store, alpha_id):
            # 指标不覆盖（campaign 的可能更全），但**状态必须同步**：alpha 的 status
            # 会变（UNSUBMITTED→ACTIVE→DECOMMISSIONED），而面板「已提交」列读的就是
            # alphas.platform_status。整体跳过会让状态永远停在落库那一刻
            # （2026-10-28 实测：e75pvoNz 平台已 ACTIVE，本地连 alphas 行都没有）。
            synced = False
            try:
                checks = (obj.get("is") or {}).get("checks") \
                    if isinstance(obj.get("is"), dict) else None
                synced = _sync_alpha_row(store, slim, region, row["code"],
                                         alpha_id, _ladder_sharpe(checks))
            except Exception as e:  # noqa: BLE001 — 同步失败不该改变 exists 语义
                logger.warning("[alpha-persist] %s 状态同步失败（已忽略）：%s: %s"
                               % (alpha_id, type(e).__name__, e))
            if synced:
                logger.info("[alpha-persist] %s 状态同步 → status=%s stage=%s"
                            % (alpha_id, slim.get("status"), slim.get("stage")))
            return {"ok": True, "action": "exists", "alpha_id": alpha_id,
                    "reason": None, "wave": None, "status_synced": synced}
        wave = wave or wave_name()
        lock = getattr(store, "_conn_lock", None)
        if lock is not None:
            with lock:
                n = store.upsert_backtest_rows(region, wave, [row])
        else:
            n = store.upsert_backtest_rows(region, wave, [row])
        if not n:
            # upsert 里被跳过（code 空 / expr 建不出来）——不静默，留一条日志
            logger.warning("[alpha-persist] %s 未落库（upsert 返回 0 行，source=%s）"
                           % (alpha_id, source))
            return {"ok": False, "action": "skipped", "alpha_id": alpha_id,
                    "reason": "upsert skipped (empty code / expr)", "wave": wave}
        logger.info("[alpha-persist] %s 落库 region=%s wave=%s source=%s"
                    % (alpha_id, region, wave, source))
        return {"ok": True, "action": "inserted", "alpha_id": alpha_id,
                "reason": None, "wave": wave}
    except Exception as e:  # noqa: BLE001 — 落库失败绝不能影响调用方
        aid = obj.get("id") if isinstance(obj, dict) else None
        logger.warning("[alpha-persist] %s 落库异常（已忽略，可重试）：%s: %s"
                       % (aid or "?", type(e).__name__, e))
        # action="error" 不是 "skipped"：异常是**可重试**的（脏数据形状 / 偶发库错），
        # 而 skipped 是"信息不足、重试也无用"。补录脚本据此决定记不记账。
        return {"ok": False, "action": "error", "alpha_id": aid,
                "reason": "%s: %s" % (type(e).__name__, e), "wave": None}


def persist_many(objs: List[Dict[str, Any]], source: str = "mcp") -> Dict[str, int]:
    """批量落库。返回 ``{"inserted", "exists", "skipped"}`` 计数（供日志/自检）。"""
    stat = {"inserted": 0, "exists": 0, "skipped": 0}
    for o in objs or []:
        r = persist_alpha(o, source=source)
        stat[r.get("action", "skipped")] = stat.get(r.get("action", "skipped"), 0) + 1
    if stat["inserted"]:
        logger.info("[alpha-persist] 批量落库 %d 颗（wave=%s, source=%s）"
                    % (stat["inserted"], wave_name(), source))
    return stat


__all__ = ["persist_alpha", "persist_many", "wave_name", "WAVE_PREFIX"]
