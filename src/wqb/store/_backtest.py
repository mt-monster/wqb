# -*- coding: utf-8 -*-
"""BacktestMixin: backtest rows and submission recording for CampaignStore."""
from __future__ import annotations

from typing import Any, Dict, List, Optional, Sequence

from ._common import _dumps, _loads, _now


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
            failed = r.get("failed_checks") or r.get("ra_failed_checks") or []
            payload = _dumps(r)
            cur.execute(
                """INSERT INTO backtest_results
                   (expression_id, alpha_id, status, sharpe, fitness, turnover,
                    margin, returns, drawdown, two_year_sharpe, sub_universe_sharpe,
                    long_count, short_count, pnl, book_size, ra_failed_checks,
                    region, wave, dataset, code, payload_json, created_at)
                   VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
                   ON CONFLICT(alpha_id) DO UPDATE SET
                    expression_id=excluded.expression_id, status=excluded.status,
                    sharpe=excluded.sharpe, fitness=excluded.fitness,
                    turnover=excluded.turnover, margin=excluded.margin,
                    returns=excluded.returns, drawdown=excluded.drawdown,
                    two_year_sharpe=excluded.two_year_sharpe,
                    sub_universe_sharpe=excluded.sub_universe_sharpe,
                    long_count=excluded.long_count, short_count=excluded.short_count,
                    pnl=excluded.pnl, book_size=excluded.book_size,
                    ra_failed_checks=excluded.ra_failed_checks,
                    region=excluded.region, wave=excluded.wave, dataset=excluded.dataset,
                    code=excluded.code, payload_json=excluded.payload_json,
                    created_at=excluded.created_at""",
                (
                    expr_id, alpha_id, r.get("status") or "COMPLETE",
                    r.get("sharpe"), r.get("fitness"), turnover, margin,
                    r.get("returns"), r.get("drawdown"),
                    r.get("two_year_sharpe"), r.get("sub_universe_sharpe"),
                    r.get("long_count"), r.get("short_count"),
                    r.get("pnl"), r.get("book_size"),
                    _dumps(failed) if failed else None,
                    region, str(wave), dataset, code, payload, now,
                ),
            )
            if alpha_id:
                cur.execute("SELECT id FROM alphas WHERE alpha_id=?", (alpha_id,))
                arow = cur.fetchone()
                aval = (
                    code or "",
                    rid, ds_id,
                    r.get("universe"), r.get("delay"),
                    r.get("neut") or r.get("neutralization"),
                    r.get("sharpe"), r.get("fitness"), margin, turnover,
                    r.get("two_year_sharpe"),
                    r.get("status") or "UNSUBMITTED",
                    r.get("prod_corr") or r.get("prod_correlation"),
                    r.get("self_corr") or r.get("self_correlation"),
                    r.get("is_ladder_sharpe"),   # 2026-08-29 新增：提交硬闸之一
                    # 平台侧状态（审计 P0-2 新增列）：alphas.status 保留本地语义，
                    # platform_status 存平台 status，二者同名不同义，勿混用。
                    r.get("platform_status"),
                    r.get("stage"),              # IS | OS
                    r.get("alpha_type"),         # REGULAR | SUPER
                    r.get("date_submitted"),
                    now,
                )
                if arow:
                    cur.execute(
                        """UPDATE alphas SET expression=?, region_id=?, dataset_id=?,
                           universe=?, delay=?, neutralization=?, sharpe=?, fitness=?,
                           margin=?, turnover=?, two_year_sharpe=?, status=?,
                           prod_correlation=?, self_correlation=?, is_ladder_sharpe=?,
                           platform_status=?, stage=?, alpha_type=?, date_submitted=?,
                           updated_at=?
                           WHERE id=?""",
                        aval + (int(arow[0]),),
                    )
                else:
                    cur.execute(
                        """INSERT INTO alphas
                           (alpha_id, expression, region_id, dataset_id, universe,
                            delay, neutralization, sharpe, fitness, margin, turnover,
                            two_year_sharpe, status, prod_correlation, self_correlation,
                            is_ladder_sharpe, platform_status, stage, alpha_type,
                            date_submitted, created_at, updated_at)
                           VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                        (alpha_id,) + aval + (now,),
                    )
            # 回填 expressions 表的指标列（修复三表不一致根因）
            if alpha_id and r.get("sharpe") is not None:
                cur.execute(
                    """UPDATE expressions SET sharpe=?, fitness=?, margin=?, turnover=?,
                       updated_at=? WHERE alpha_id=?""",
                    (r.get("sharpe"), r.get("fitness"), margin, turnover, now, alpha_id),
                )
            n += 1
        self.connection.commit()
        return n

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
        if ds_id is None:
            ds_id = self._ensure_dataset(region, "_unknown")

        cur.execute("SELECT id FROM alphas WHERE alpha_id=?", (aid,))
        row = cur.fetchone()
        now = _now()
        cols = {
            "alpha_id": aid,
            "expression": expr,
            "region_id": rid,
            "dataset_id": ds_id,
            "universe": d.get("universe"),
            "delay": d.get("delay"),
            "neutralization": d.get("neutralization"),
            "sharpe": d.get("sharpe"),
            "fitness": d.get("fitness"),
            "turnover": d.get("turnover"),
            "two_year_sharpe": d.get("two_year_sharpe"),
            "status": d.get("status") or "UNSUBMITTED",
            "prod_correlation": d.get("prod_correlation") or d.get("prod_corr"),
            "self_correlation": d.get("self_correlation") or d.get("self_corr"),
            "is_ladder_sharpe": d.get("is_ladder_sharpe"),
            "platform_status": d.get("platform_status"),
            "stage": d.get("stage"),
            "alpha_type": d.get("alpha_type"),
            "date_submitted": d.get("date_submitted"),
        }
        if row:
            sets = ", ".join(f"{k}=?" for k in cols)
            cur.execute(f"UPDATE alphas SET {sets}, updated_at=? WHERE id=?",
                        list(cols.values()) + [now, int(row[0])])
        else:
            klist = ", ".join(cols.keys())
            ph = ", ".join("?" * len(cols))
            cur.execute(
                f"INSERT INTO alphas ({klist}, created_at, updated_at) VALUES ({ph}, ?, ?)",
                list(cols.values()) + [now, now],
            )
        self.connection.commit()
        return aid

    save_backtest_results = upsert_backtest_rows

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
