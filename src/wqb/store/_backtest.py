# -*- coding: utf-8 -*-
"""BacktestMixin: backtest rows and submission recording for CampaignStore."""
from __future__ import annotations

from typing import Any, Dict, List, Optional, Sequence

from ..config import RA_CHECK_NAMES, compute_webdata_failed_counts
from ._common import _dumps, _loads, _now


def _check_names(v: Any) -> Optional[List[str]]:
    """项名列表（元素是名字或 {name, …}；也收 JSON 字符串——旧路径有双重编码——与逗号分隔的名字串，
    同 submit_queue.ra_fail_of）；认不出的形状返回 None。"""
    for _ in range(2):
        if isinstance(v, (str, bytes, bytearray)):
            v = _loads(v)
    if isinstance(v, str):
        v = [x.strip().strip('"') for x in v.strip().strip("[]").split(",")]
    if not isinstance(v, (list, tuple)):
        return None
    names = [x.get("name") if isinstance(x, dict) else x for x in v]
    return [n for n in names if isinstance(n, str) and n]


def ra_failed_names(r: Dict[str, Any]) -> Optional[List[str]]:
    """一行回测的 RA 资格门失败项名——`backtest_results.ra_failed_checks` 列的唯一写法（2026-09-28）。

    口径是 wqb.config 的 RA 唯一定义（R3）：18 项 RA check 里 result 既不是 PASS 也不是 PENDING 的。
    按行里现有的信息取，优先级：
      1. ra_failed_checks（拍平层 / 平台精简结构按同一定义算好的；空列表 = RA 全过），只留 RA 项名；
      2. 完整 checks（[{name, result, …}]）→ compute_webdata_failed_counts 现算；
      3. 只有 failed_checks（全部 FAIL 项名：旧指标缓存行、旧调用方）→ 只留 RA 项名。这一档看不到
         RA 项的 WARNING / ERROR（真实数据里 RA 项只出现 PASS / FAIL）。
    三者都没有 → None（入库为 NULL，读取方按"无失败"计，与此前一致）。

    此前这一列存 `failed_checks or ra_failed_checks`，实际是所有 check 里 FAIL 的名字：相关性等
    非 RA 项 FAIL 时被记成"RA 不干净"，RA 项 WARNING / ERROR 时又被记成干净。
    failed_checks（全部 FAIL）原样留在 payload_json 里。
    """
    given = _check_names(r.get("ra_failed_checks"))
    if given is not None:
        return list(dict.fromkeys(n for n in given if n in RA_CHECK_NAMES))
    checks = r.get("checks")
    if isinstance(checks, list) and any(isinstance(c, dict) and "result" in c for c in checks):
        return compute_webdata_failed_counts(checks)["ra_failed_names"]
    failed = _check_names(r.get("failed_checks"))
    if failed is not None:
        return list(dict.fromkeys(n for n in failed if n in RA_CHECK_NAMES))
    return None


def _corr_value(v: Any) -> Optional[float]:
    """相关性取值：[0,1] 内的数才算数；None / 非数 / 越界按"没有"处理（防空值与异常值污染）。"""
    if v is None:
        return None
    try:
        fv = float(v)
    except (TypeError, ValueError):
        return None
    return fv if 0.0 <= fv <= 1.0 else None


def _first_present(d: Dict[str, Any], *keys: str) -> Any:
    """按顺序取第一个不是 None 的键值（此前用 `or` 串联，0 / 0.0 会被当成没有）。"""
    for k in keys:
        if d.get(k) is not None:
            return d.get(k)
    return None


#: 生命周期列的"已提交"态：一旦到了这里，不再被未提交类的值（UNSUBMITTED / COMPLETE / IS …）改回去
_SUBMITTED_STATES = {
    "status": frozenset({"ACTIVE", "SUBMITTED", "DECOMMISSIONED"}),
    "platform_status": frozenset({"ACTIVE", "SUBMITTED", "DECOMMISSIONED"}),
    "stage": frozenset({"OS"}),
}


def _merge_alpha_columns(existing: Dict[str, Any], incoming: Dict[str, Any]) -> Dict[str, Any]:
    """已有 alphas 行的合并式更新：返回真正要写的列（2026-09-28 N35）。

    - 值为 None / 空串的列不写：这一行"没带"不等于"清空"；
    - status / platform_status / stage 已处在已提交态时，不被未提交类的值改回去（已提交态之间可以变，
      如 ACTIVE → DECOMMISSIONED）。
    """
    out: Dict[str, Any] = {}
    for col, val in incoming.items():
        if val is None or val == "":
            continue
        submitted = _SUBMITTED_STATES.get(col)
        if (submitted and str(existing.get(col) or "").upper() in submitted
                and str(val).upper() not in submitted):
            continue
        out[col] = val
    return out


class BacktestMixin:
    """Backtest results and submission recording methods."""

    def upsert_backtest_rows(
        self, region: str, wave: str, rows: Sequence[Dict[str, Any]],
        dataset: Optional[str] = None,
    ) -> int:
        wave_id = self._ensure_wave(region, str(wave), dataset)
        n = 0
        cur = self.connection.cursor()
        now = _now()
        rid = self._ensure_region(region)
        ds_id = self._ensure_dataset(region, dataset or "_unknown")
        # 批量事务：BEGIN ... COMMIT 包裹全部写入，减少 fsync
        cur.execute("BEGIN")
        try:
            for r in rows:
                code = r.get("code") or r.get("expression") or r.get("expr") or ""
                alpha_id = r.get("id") or r.get("alpha_id")
                expr_id = None
                if code:
                    cur.execute(
                        "SELECT id FROM expressions WHERE wave_id=? AND expression=?",
                        (wave_id, code),
                    )
                    erow = cur.fetchone()
                    if erow:
                        expr_id = int(erow[0])
                    else:
                        self.upsert_expressions(
                            region, str(wave),
                            [{"expression": code, "alpha_id": alpha_id, "status": "backtested"}],
                            dataset=dataset,
                        )
                        cur.execute(
                            "SELECT id FROM expressions WHERE wave_id=? AND expression=?",
                            (wave_id, code),
                        )
                        erow = cur.fetchone()
                        expr_id = int(erow[0]) if erow else None
                if expr_id is None:
                    continue
                margin = r.get("margin")
                if margin is None and r.get("margin_bp") is not None:
                    margin = r["margin_bp"] / 10000.0
                turnover = r.get("turnover")
                if turnover is None and r.get("turnover_pct") is not None:
                    turnover = r["turnover_pct"] / 100.0
                failed = ra_failed_names(r)
                payload = _dumps(r)
                # 同一 alpha 再次入库（重评审、重收批、事后补收）时按合并写（2026-09-28 N35）：
                # 行里没带的指标与数据集保留原值——toolkit 评审行本来就不带 returns / drawdown / 多空数等，
                # 此前会把收批写进来的值清成 NULL。ra_failed_checks 只在这一行说得清时才改
                # （空 = RA 全过也要写进去，覆盖旧名单）。payload_json 仍是最近一次入库的原始行。
                cur.execute(
                    """INSERT INTO backtest_results
                       (expression_id, alpha_id, status, sharpe, fitness, turnover,
                        margin, returns, drawdown, two_year_sharpe, sub_universe_sharpe,
                        risk_neutralized_sharpe,
                        long_count, short_count, pnl, book_size, ra_failed_checks,
                        region, wave, dataset, code, payload_json, created_at)
                       VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
                       ON CONFLICT(alpha_id) DO UPDATE SET
                        expression_id=excluded.expression_id, status=excluded.status,
                        sharpe=COALESCE(excluded.sharpe, sharpe),
                        fitness=COALESCE(excluded.fitness, fitness),
                        turnover=COALESCE(excluded.turnover, turnover),
                        margin=COALESCE(excluded.margin, margin),
                        returns=COALESCE(excluded.returns, returns),
                        drawdown=COALESCE(excluded.drawdown, drawdown),
                        two_year_sharpe=COALESCE(excluded.two_year_sharpe, two_year_sharpe),
                        sub_universe_sharpe=COALESCE(excluded.sub_universe_sharpe, sub_universe_sharpe),
                        risk_neutralized_sharpe=COALESCE(excluded.risk_neutralized_sharpe,
                                                         risk_neutralized_sharpe),
                        long_count=COALESCE(excluded.long_count, long_count),
                        short_count=COALESCE(excluded.short_count, short_count),
                        pnl=COALESCE(excluded.pnl, pnl),
                        book_size=COALESCE(excluded.book_size, book_size),
                        ra_failed_checks=CASE WHEN ? THEN excluded.ra_failed_checks
                                              ELSE ra_failed_checks END,
                        region=excluded.region, wave=excluded.wave,
                        dataset=COALESCE(excluded.dataset, dataset),
                        code=excluded.code, payload_json=excluded.payload_json,
                        created_at=excluded.created_at""",
                    (
                        expr_id, alpha_id, r.get("status") or "COMPLETE",
                        r.get("sharpe"), r.get("fitness"), turnover, margin,
                        r.get("returns"), r.get("drawdown"),
                        r.get("two_year_sharpe"), r.get("sub_universe_sharpe"),
                        r.get("risk_neutralized_sharpe"),
                        r.get("long_count"), r.get("short_count"),
                        r.get("pnl"), r.get("book_size"),
                        _dumps(failed) if failed else None,
                        region, str(wave), dataset, code, payload, now,
                        failed is not None,
                    ),
                )
                if alpha_id:
                    self._write_alpha_row(
                        cur, alpha_id,
                        {
                            "expression": code,
                            "universe": r.get("universe"),
                            "delay": r.get("delay"),
                            "neutralization": _first_present(r, "neut", "neutralization"),
                            "sharpe": r.get("sharpe"),
                            "fitness": r.get("fitness"),
                            "margin": margin,
                            "turnover": turnover,
                            "two_year_sharpe": r.get("two_year_sharpe"),
                            "status": r.get("status"),
                            "prod_correlation": _corr_value(_first_present(r, "prod_corr", "prod_correlation")),
                            "self_correlation": _corr_value(_first_present(r, "self_corr", "self_correlation")),
                            "is_ladder_sharpe": r.get("is_ladder_sharpe"),
                            "platform_status": r.get("platform_status"),
                            "stage": r.get("stage"),
                            "alpha_type": r.get("alpha_type"),
                            "date_submitted": r.get("date_submitted"),
                            # ---- 2026-09-18：回测指标全量落库（设计文档 §2.2）----
                            "sub_universe_sharpe": r.get("sub_universe_sharpe"),
                            "returns": r.get("returns"),
                            "drawdown": r.get("drawdown"),
                            "long_count": r.get("long_count"),
                            "short_count": r.get("short_count"),
                            "concentrated_weight": r.get("concentrated_weight"),
                            "cluster_test": r.get("cluster_test"),
                        },
                        region_id=rid,
                        # 调用方点名了数据集才改归属；没点名（缺省 _unknown）不动已有归属
                        dataset_id=ds_id if dataset and dataset != "_unknown" else None,
                        dataset_authoritative=True,
                        default_dataset_id=ds_id,
                        # 回测行里的相关性来自平台返回的 alpha（两条收批路径都是），可在行里用 prod_corr_source 另注
                        corr_source=r.get("prod_corr_source") or "platform_sync",
                        now=now,
                    )
                if alpha_id and r.get("sharpe") is not None:
                    cur.execute(
                        """UPDATE expressions SET sharpe=?, fitness=COALESCE(?, fitness),
                           margin=COALESCE(?, margin), turnover=COALESCE(?, turnover),
                           updated_at=? WHERE alpha_id=?""",
                        (r.get("sharpe"), r.get("fitness"), margin, turnover, now, alpha_id),
                    )
                n += 1
            self.connection.commit()
        except Exception:
            self.connection.rollback()
            raise
        return n

    def _write_alpha_row(
        self, cur: Any, alpha_id: str, incoming: Dict[str, Any], *,
        region_id: int, dataset_id: Optional[int], dataset_authoritative: bool,
        default_dataset_id: int, corr_source: str, now: str,
    ) -> str:
        """alphas 行的唯一写法：upsert_backtest_rows 与 upsert_alpha_from_platform 共用（2026-09-28 N35）。

        - 新行：照写；status 缺省 UNSUBMITTED，没有数据集归属时用 default_dataset_id（_unknown）。
        - 已有行：按 `_merge_alpha_columns` 合并——行里没带的列不动，生命周期不从已提交态回退。
          此前两个写入方都是整行覆盖：一次 toolkit 重评审就把已提交 alpha 改回 UNSUBMITTED、清空
          platform_status / date_submitted / 相关性，提交队列随后又把它放回 READY。
        - dataset_id：dataset_authoritative（调用方点名了数据集）时覆盖；否则（字段投票等推断）只在
          原来没有归属（_unknown）时补上。
        - 写了相关性就同时记来源与时间（prod_corr_source / corr_checked_at），与 persist_correlation 一致。

        不提交事务，由调用方提交。返回 "inserted" / "updated"。
        """
        cur.execute(
            "SELECT a.id, a.status, a.platform_status, a.stage, d.name FROM alphas a "
            "LEFT JOIN datasets d ON d.id = a.dataset_id WHERE a.alpha_id=?",
            (alpha_id,),
        )
        row = cur.fetchone()
        corr_cols = {c for c in ("prod_correlation", "self_correlation") if incoming.get(c) is not None}
        if row is None:
            cols = dict(incoming)
            cols["expression"] = cols.get("expression") or ""
            cols["status"] = cols.get("status") or "UNSUBMITTED"
            cols.update(alpha_id=alpha_id, region_id=region_id,
                        dataset_id=dataset_id if dataset_id is not None else default_dataset_id)
            if corr_cols:
                cols.update(prod_corr_source=corr_source, corr_checked_at=now)
            cols.update(created_at=now, updated_at=now)
            cur.execute(
                f"INSERT INTO alphas ({', '.join(cols)}) VALUES ({', '.join('?' * len(cols))})",
                list(cols.values()),
            )
            return "inserted"
        sets = _merge_alpha_columns(
            {"status": row[1], "platform_status": row[2], "stage": row[3]}, incoming)
        sets["region_id"] = region_id
        if dataset_id is not None and (dataset_authoritative or row[4] in (None, "_unknown")):
            sets["dataset_id"] = dataset_id
        if corr_cols & set(sets):
            sets.update(prod_corr_source=corr_source, corr_checked_at=now)
        sets["updated_at"] = now
        cur.execute(
            f"UPDATE alphas SET {', '.join(f'{k}=?' for k in sets)} WHERE id=?",
            list(sets.values()) + [int(row[0])],
        )
        return "updated"

    def record_submission(
        self,
        alpha_id: str,
        region: Optional[str] = None,
        submission_type: str = "REGULAR",
        status: str = "ACTIVE",
        verdict: Optional[Any] = None,
        quota_used: int = 1,
        quota_remaining: Optional[int] = None,
    ) -> Dict[str, Any]:
        """记录一次真实提交到 submission_ledger（审计 P0-3）。

        已统一委托给 upsert_submission，消除双写路径冲突。
        """
        return self.upsert_submission(
            alpha_id=alpha_id,
            region=region,
            submission_type=submission_type,
            status=status,
            quota_used=quota_used,
            verdict=verdict if isinstance(verdict, dict) else None,
        )

    def upsert_alpha_from_platform(self, d: Dict[str, Any]) -> Optional[str]:
        """提交成功后把平台详情回写 alphas 表（2026-08-30 新增）。

        背景：平台侧新建/提交的 alpha（LL7mzYQv 等）未走 harvest 入库，
        alphas 表无法反映全部已提交 alpha（仅 submission_ledger 有记录）。
        提交脚本在 ACTIVE 后调用本方法，用 get_alpha_details 的数据落库。

        期望 d 键：alpha_id, region, expression, sharpe, fitness, turnover,
        two_year_sharpe, is_ladder_sharpe, prod_correlation, self_correlation,
        platform_status, stage, alpha_type, date_submitted, universe, delay, neutralization

        已有行按合并写（2026-09-28 N35，见 `_write_alpha_row`）：d 里没有或为 None 的键不动——
        tools/sync_platform_alphas 传 two_year_sharpe=None（平台 is 段没有这一项），此前会把本地回测
        写进来的 2Y 清掉；字段投票推断的数据集只补 _unknown，不改掉已有归属。相关性记来源 platform_sync。
        """
        import re
        from collections import Counter

        aid = d.get("alpha_id")
        region = d.get("region")
        if not aid or not region:
            return None
        rid = self._ensure_region(region)
        cur = self.connection.cursor()

        # dataset 解析：字段反查（仅唯一归属字段投票，跨集共享字段不投票），失败归 _unknown
        _ops = {
            "rank", "ts_delta", "ts_mean", "ts_zscore", "ts_backfill", "vec_avg",
            "vec_sum", "divide", "subtract", "add", "multiply", "ts_decay_linear",
            "group_neutralize", "ts_std_dev", "abs", "sign", "log", "max", "min",
            "if_else", "ts_rank", "scale", "group_rank", "ts_sum", "ts_av_diff",
            "ts_delay", "ts_corr", "ts_covariance", "group_zscore", "ts_regression",
            "last_diff_value", "kth_element", "ts_arg_max", "ts_arg_min", "ts_max",
            "ts_min", "ts_product", "inverse", "signed_power", "tail", "trade_when",
            "is_nan", "nan_out", "purify", "densify", "winsorize", "zscore",
            "ts_count_nans", "ts_median", "ts_percentile", "ts_step", "ts_scale",
        }
        expr = d.get("expression") or ""
        fields = set()
        for m in re.finditer(r"vec_(?:avg|sum)\(([a-zA-Z_][\w]*)\)", expr):
            fields.add(m.group(1))
        for tok in re.findall(r"\b[a-zA-Z_][a-zA-Z0-9_]{3,}\b", expr):
            if tok.lower() not in _ops and not tok.isdigit():
                fields.add(tok)
        ds_id = None
        votes = Counter()
        for f in fields:
            cur.execute("SELECT DISTINCT dataset_id FROM fields WHERE field_name=?", (f,))
            ds = [r[0] for r in cur.fetchall()]
            if len(ds) == 1:
                votes[ds[0]] += 1
        if votes:
            top = votes.most_common(2)
            if len(top) == 1 or top[0][1] > top[1][1]:
                ds_id = int(top[0][0])

        self._write_alpha_row(
            cur, aid,
            {
                "expression": expr,
                "universe": d.get("universe"),
                "delay": d.get("delay"),
                "neutralization": d.get("neutralization"),
                "sharpe": d.get("sharpe"),
                "fitness": d.get("fitness"),
                "turnover": d.get("turnover"),
                "two_year_sharpe": d.get("two_year_sharpe"),
                "status": d.get("status"),
                "prod_correlation": _corr_value(_first_present(d, "prod_correlation", "prod_corr")),
                "self_correlation": _corr_value(_first_present(d, "self_correlation", "self_corr")),
                "is_ladder_sharpe": d.get("is_ladder_sharpe"),
                "platform_status": d.get("platform_status"),
                "stage": d.get("stage"),
                "alpha_type": d.get("alpha_type"),
                "date_submitted": d.get("date_submitted"),
            },
            region_id=rid,
            dataset_id=ds_id,                      # 字段投票的推断，只补 _unknown
            dataset_authoritative=False,
            default_dataset_id=self._ensure_dataset(region, "_unknown"),
            corr_source="platform_sync",
            now=_now(),
        )
        self.connection.commit()
        return aid

    save_backtest_results = upsert_backtest_rows

    def persist_correlation(
        self,
        alpha_id: str,
        prod: Optional[float] = None,
        self_: Optional[float] = None,
        source: str = "triage_local",
        overwrite: bool = False,
    ) -> Dict[str, Any]:
        """把相关性检查结果落库到 alphas 表（2026-09-18，设计文档 §2.4）。

        动机：`check_correlation` 的返回值此前只进内存 / triage checkpoint，
        复盘/查询时必须重打平台 API（占单并发队列）。本方法提供「检查即落库」。

        契约：
          - alpha 不存在 → {"skipped": "not_found"}
          - overwrite=False（默认）→ 只填 NULL 列，已有值不动（保留平台权威值）
          - overwrite=True → 覆盖（用于平台权威值修正本地估算值）
          - 值非 [0,1] 区间 → 该值被忽略（防空值/异常污染），全部无有效值则 skipped
          - 写入时同步更新 prod_corr_source / corr_checked_at
        幂等：同值重复调用零变化。

        source 取值：platform_sync（平台权威）> manual > triage_local（本地抽测）。
        注意 triage_local **高可信、低不可信**：对近期提交的孪生体失明会低估。
        """
        if not alpha_id:
            return {"skipped": "no_alpha_id"}

        p = _corr_value(prod)
        s = _corr_value(self_)
        if p is None and s is None:
            return {"skipped": "no_valid_value", "alpha_id": alpha_id}

        cur = self.connection.cursor()
        cur.execute(
            "SELECT id, prod_correlation, self_correlation FROM alphas WHERE alpha_id=?",
            (alpha_id,),
        )
        row = cur.fetchone()
        if not row:
            return {"skipped": "not_found", "alpha_id": alpha_id}

        cur_prod = _corr_value(row[1])
        cur_self = _corr_value(row[2])
        new_prod = p if (p is not None and (overwrite or cur_prod is None)) else None
        new_self = s if (s is not None and (overwrite or cur_self is None)) else None
        if new_prod is None and new_self is None:
            return {"skipped": "already_set", "alpha_id": alpha_id}

        now = _now()
        sets, vals = [], []
        if new_prod is not None:
            sets.append("prod_correlation=?")
            vals.append(new_prod)
        if new_self is not None:
            sets.append("self_correlation=?")
            vals.append(new_self)
        sets.append("prod_corr_source=?")
        vals.append(source)
        sets.append("corr_checked_at=?")
        vals.append(now)
        sets.append("updated_at=?")
        vals.append(now)
        vals.append(int(row[0]))
        cur.execute(f"UPDATE alphas SET {', '.join(sets)} WHERE id=?", vals)
        self.connection.commit()
        return {
            "alpha_id": alpha_id,
            "prod_correlation": new_prod,
            "self_correlation": new_self,
            "source": source,
            "checked_at": now,
        }

    def list_backtest_rows(self, region: str, wave: str) -> List[Dict[str, Any]]:
        cur = self.connection.cursor()
        cur.execute(
            "SELECT * FROM backtest_results WHERE region=? AND wave=? ORDER BY id",
            (region, str(wave)),
        )
        out = []
        for row in cur.fetchall():
            d = dict(row)
            if d.get("payload_json"):
                d["payload"] = _loads(d["payload_json"])
            out.append(d)
        return out
