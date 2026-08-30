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
                    margin, two_year_sharpe, sub_universe_sharpe, ra_failed_checks,
                    region, wave, dataset, code, payload_json, created_at)
                   VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                (
                    expr_id, alpha_id, r.get("status") or "COMPLETE",
                    r.get("sharpe"), r.get("fitness"), turnover, margin,
                    r.get("two_year_sharpe"), r.get("sub_universe_sharpe"),
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

        历史问题：该表长期只有 DRYRUN 测试数据，真实提交（MEA/IND/SA）从未入账。
        提交脚本（含 SUPER alpha）在拿到 verdict 后应调用本方法落账。
        """
        cur = self.connection.cursor()
        cur.execute("SELECT id FROM submission_ledger WHERE alpha_id=?", (alpha_id,))
        row = cur.fetchone()
        v = _dumps(verdict) if isinstance(verdict, (dict, list)) else verdict
        now = _now()
        if row:
            cur.execute(
                """UPDATE submission_ledger SET region=?, submission_type=?, status=?,
                   quota_used=?, quota_remaining=?, verdict=?, submitted_at=?,
                   verified_at=?, updated_at=? WHERE id=?""",
                (region, submission_type, status, quota_used, quota_remaining, v,
                 now, now, now, int(row[0])),
            )
        else:
            cur.execute(
                """INSERT INTO submission_ledger
                   (alpha_id, region, submission_type, status, quota_used,
                    quota_remaining, verdict, submitted_at, verified_at,
                    created_at, updated_at)
                   VALUES (?,?,?,?,?,?,?,?,?,?,?)""",
                (alpha_id, region, submission_type, status, quota_used,
                 quota_remaining, v, now, now, now, now),
            )
        self.connection.commit()
        return {"alpha_id": alpha_id, "status": status, "region": region}

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
            "status": d.get("status") or "COMPLETE",
            "prod_correlation": d.get("prod_correlation"),
            "self_correlation": d.get("self_correlation"),
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
