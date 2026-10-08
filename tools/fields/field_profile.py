#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""字段画像构建器（多区域通用版）—— 用回测副产品建画像，降筛字段成本。

背景：部分区域（如 DEU）不在 WebDataScope 数据包覆盖内（无预筛、无 field_profile），
     只能靠回测试错。但实测本身会留下**别区没有的原料**：
     每个测过的字段的 换手 / 最好 S / 最好 2Y / 最好 sub / 失败项计数。

本工具把这些副产品 + fields 表元数据（coverage/type）+ 命名族解析，
合成**多区域隔离**的画像存储，使「筛字段」从"每字段一条回测"变成"一条 SQL"。

★ 多区域隔离设计（2026-10-08 重构，解决"串号"问题）：
  主表 = `field_profile_perf`（**复合主键 (region, dataset, field)**，一份 schema 管所有区）
  每区一个只读视图 = `field_profile_<region小写>`（如 field_profile_eur）
      ⇒ 查询体验等同"每区一张独立表"，但 schema 只需维护一处；
      ⇒ build 只 `DELETE WHERE region=?`，**不再 DROP 整表**（旧版会清掉其它区域数据）。
  兼容：`field_profile_deu` 保留为视图（指向 perf 表 WHERE region='DEU'），旧查询/文档不破。

画像列：
  region / dataset / category / field / ftype / coverage
  family          —— 命名族（去掉数字与期限后缀后的骨架）
  n_tests         —— 已测次数
  to_med          —— 换手中位数（None = 未测）
  to_min / to_max
  best_s / best_2y / best_sub / best_f
  best_2y_when_s_hi —— S 最高那条的 2Y（诊断「2Y有S无」形态）
  verdict         —— 判定：ALIVE / WEAK / DEAD_STATIC / DEAD_TURNOVER / DEAD_COUNT / DEAD / UNTESTED
  n_sg            —— 单信号（合规形态）样本数

判定规则（全部来自实测，见 docs/reference/field_characteristic_to_mechanism.md）：
  DEAD_STATIC     to_med < 0.03          —— 静态属性，任何骨架都无用
  DEAD_TURNOVER   to_med > 0.70          —— 被 HIGH_TURNOVER 闸直接拒
  DEAD_COUNT      名字含 num/count/surprisenum/raisednum 且 best_2y ≥ 1.3 且 best_s ≤ 0.7
                                          —— 「2Y有S无」判死形态
  ALIVE           best_s_sg ≥ 1.58       —— 达到闸线
  WEAK            best_s_sg ≥ 1.10       —— 有信号但不够强
  DEAD            已测但 best_s_sg < 1.10
  UNTESTED        n_tests == 0（且 coverage ≥ 0.6、非 GROUP）

用法:
    # 建某区画像（只影响该区，不影响其它区）
    python tools/field_profile.py --build --region DEU
    python tools/field_profile.py --build --region EUR --category analyst

    # 一次建全部有实测数据的区域
    python tools/field_profile.py --build --all-regions

    # 查询（默认查主表并按 region 过滤；也可直接查每区视图）
    python tools/field_profile.py --query --region DEU --verdict WEAK
    python tools/field_profile.py --query --region EUR --category analyst --min-s 1.1

    # 盘点：列出所有已建画像的区域
    python tools/field_profile.py --list

    # 一次性迁移：把旧版 field_profile_deu **表** 的存量搬进 perf 表并改为视图
    python tools/field_profile.py --migrate-legacy            # 默认 dry-run
    python tools/field_profile.py --migrate-legacy --apply    # 落盘
"""
from __future__ import annotations

import argparse
import os
import re as _re
import sqlite3
import statistics
import sys
from typing import Any, Dict, List, Optional

from pathlib import Path as _Path

_REPO = str(next(_p for _p in _Path(__file__).resolve().parents if (_p / "pyproject.toml").exists() and (_p / "src" / "wqb").is_dir()))
sys.path.insert(0, os.path.join(_REPO, "src"))
from wqb.db_conn import connect as _db_connect  # noqa: E402
DB = os.path.join(_REPO, "data", "wqb.db")

# ── 多区域隔离的核心常量 ──────────────────────────────────────────────
PERF_TABLE = "field_profile_perf"          # 统一主表（region 为复合主键一部分）
LEGACY_NAME = "field_profile_deu"          # 旧版名（迁移后改为视图，保持兼容）


def view_name(region: str) -> str:
    """每区视图名：field_profile_<region小写>（查询体验 = 每区一张独立表）。"""
    return f"field_profile_{region.lower()}"


SKIP_TOKENS = {
    "ts_backfill", "ts_mean", "group_neutralize", "bucket", "quantile", "oth455", "subindustry",
    "ts_delta", "ts_av_diff", "signed_power", "ts_decay_linear", "ts_rank", "ts_zscore",
    "ts_regression", "trade_when", "group_scale", "group_rank", "group_zscore", "group_mean",
    "group_std_dev", "group_count", "group_sum", "vec_avg", "vec_max", "vec_min", "vec_sum",
    "vec_stddev", "vec_range", "vec_count", "ts_corr", "ts_delay", "ts_arg_max", "ts_arg_min",
    "log", "abs", "sign", "add", "subtract", "multiply", "divide", "if_else", "greater", "less",
    # ★ 分组轴名（不是信号字段，必须排除，否则含轴的单信号会被误判为多腿）
    "subindustry", "industry", "sector", "market", "country", "exchange", "currency",
    "continent", "region", "cluster", "universe", "densify", "pasteurize", "winsorize",
    "normalize", "zscore", "scale", "nanHandling", "trade_when", "ts_target_tvr_decay",
    "ts_target_tvr_hump", "self_corr", "ts_sum", "ts_std_dev", "ts_min", "ts_max",
    "ts_median", "kth_element", "ts_quantile", "ts_scale", "ts_corr", "ts_delay",
    "ts_arg_max", "ts_arg_min", "vec_avg", "vec_max", "vec_min", "vec_sum", "vec_stddev",
    "vec_range", "vec_count", "densify", "group_backfill", "group_cartesian_product",
}
# ★ 2026-10-08 修正（用户指正「判断字段要读 description，不能光看字段名」）。
#   两条纪律由此固化：
#   ① 名字匹配必须**子串**（`count`/`_num` 后面常跟 `_` 或字母：`count_50bps`、`_numup`、`_numanalysts`，
#      用 `\b` 会误放走合法 case —— 实测 `\bcount\b` 会把 DEAD_COUNT 从 4 打到 0）。
#   ② 匹配到名字后**必须用 description 二次确认语义**，因为名字会骗人：
#      · 名字无 count 但描述是计数：`oth47_organic_keywords` = "Count of unique keywords … unit: count"
#      · 名字有 count 但描述是比值/百分位：`country_percentile_*`(Percentile)/`accounts_receivable_turnover_ratio`(ratio)
#      · 名字有 num 但语义是「参与家数/覆盖度」而非「方向性修正家数」：`*_surprisenum` = "Number of
#        estimates used for surprise calculation"
#      · 名字有 count 但已是均值：`mean_buy_transaction_count` = "Average per event of insider buy activity"
COUNT_PAT = _re.compile(r"(raisednum|lowerednum|surprisenum|_num|count)", _re.I)
#: description 侧「确属计数/参与量」的证据
COUNT_DESC_PAT = _re.compile(
    r"(number of|count of|\bcounts?\b|how many|breadth|number of estimates|number of accounts|"
    r"number of transactions|number of analysts|number of investors|number of shares)", _re.I)
#: description 侧「并非原始计数」的反证（比例/百分位/均值/排名 ⇒ 不属于 DEAD_COUNT 形态）
COUNT_DESC_NEG = _re.compile(
    r"(ratio|percentage|percentile|per\s?cent|fraction|average|per event|normaliz|scaled|"
    r"\brank\b|code representing|type of index|weighted)", _re.I)
MULTILEG_PAT = _re.compile(r"add\(")


def _add_arg_count(code: str) -> int:
    """数 `add(` 的**参数树**里有几个"信号子表达式"（而非字段 token 数）。"""
    best = 0
    for m in MULTILEG_PAT.finditer(code or ""):
        i = m.end()
        depth, legs, start = 1, 0, i
        while i < len(code):
            ch = code[i]
            if ch == "(":
                depth += 1
            elif ch == ")":
                depth -= 1
                if depth == 0:
                    if code[start:i].strip():
                        legs += 1
                    break
            elif ch == "," and depth == 1:
                if code[start:i].strip():
                    legs += 1
                start = i + 1
            i += 1
        best = max(best, legs)
    return best


def is_multileg(code: str) -> bool:
    """多腿组合判据（v4）：`add(` 存在 **且** 表达式里出现 >=2 个**不同信号字段**。

    区分要点：
      违禁 = add(<信号A>, <信号B>)             —— 不同信号字段（混信号）
      合规 = add(ts_mean(F,w1), ts_mean(F,w2)) —— 同字段不同窗（时序混合，即双窗骨架）
    """
    c = code or ""
    if not MULTILEG_PAT.search(c):
        return False
    toks = {
        t
        for t in _re.findall(r"\b([a-z][a-z0-9_]{9,})\b", c)
        if t not in SKIP_TOKENS and not t.startswith(("ts_", "vec_", "group_", "oth455_"))
    }
    return len(toks) >= 2


def field_of(code: str) -> Optional[str]:
    """从表达式提取主字段（第一个非算子长 token）。"""
    toks = _re.findall(r"\b([a-z][a-z0-9_]{9,})\b", code or "")
    for t in toks:
        if t in SKIP_TOKENS:
            continue
        if t.startswith(("ts_", "vec_", "group_", "oth455_")):
            continue
        return t
    return None


def family_of(field: str) -> str:
    """命名族：去掉数字与期限后缀，保留机制骨架。"""
    f = _re.sub(r"\d+", "#", field)
    f = _re.sub(r"_(3mth|4wks|28d|1wk|1mth|2yr|3yr|4yr|60d|90d|120d|250d)_ago$", "_ago", f)
    return f


def norm_cov(c) -> Optional[float]:
    if c is None:
        return None
    return round(float(c) / 100.0, 4) if float(c) > 1.0 else round(float(c), 4)


# ── 表 / 视图管理 ─────────────────────────────────────────────────────

def ensure_perf_table(con: sqlite3.Connection) -> None:
    """建主表（IF NOT EXISTS —— **绝不 DROP**，这是多区不串号的关键）。"""
    con.execute(
        """CREATE TABLE IF NOT EXISTS field_profile_perf (
            region TEXT, dataset TEXT, category TEXT, field TEXT, ftype TEXT,
            coverage REAL, family TEXT, n_tests INTEGER,
            to_med REAL, to_min REAL, to_max REAL,
            best_s REAL, best_2y REAL, best_sub REAL, best_f REAL,
            best_2y_when_s_hi REAL, verdict TEXT,
            best_s_sg REAL, best_2y_sg REAL, best_sub_sg REAL, n_sg INTEGER,
            PRIMARY KEY (region, dataset, field))"""
    )
    con.execute(
        f"CREATE INDEX IF NOT EXISTS idx_{PERF_TABLE}_region_verdict "
        f"ON {PERF_TABLE}(region, verdict)"
    )


def refresh_views(con: sqlite3.Connection, region: str) -> None:
    """为该区重建只读视图（同名视图先 DROP，只影响本区视图定义）。

    ★ 无区域特判：视图名统一为 `field_profile_<region小写>`。
      DEU 的视图名恰为 `field_profile_deu`，**天然兼容旧表名与旧文档引用**，
      无需任何 `if region == ...` 分支（符合"区域差异不进代码分支"的仓库规约）。
    """
    v = view_name(region)
    con.execute(f"DROP VIEW IF EXISTS {v}")
    con.execute(
        f"CREATE VIEW {v} AS SELECT * FROM {PERF_TABLE} WHERE region='{region}'"
    )


def table_exists_as(con: sqlite3.Connection, name: str, kind: str) -> bool:
    r = con.execute(
        "SELECT type FROM sqlite_master WHERE name=?", (name,)
    ).fetchone()
    return bool(r) and r[0] == kind


# ── 构建 ──────────────────────────────────────────────────────────────

def build(con: sqlite3.Connection, region: str, category: Optional[str]) -> int:
    cur = con.cursor()
    rid = cur.execute("SELECT id FROM regions WHERE name=?", (region,)).fetchone()
    if not rid:
        print(f"[error] 区域 {region} 不存在")
        return 2
    rid = rid[0]

    cat_clause = "AND lower(d.category)=lower(?)" if category else ""
    params: List[Any] = [rid] + ([category] if category else [])
    fields = cur.execute(
        f"""SELECT d.name, d.category, f.field_name, f.field_type, MAX(f.coverage), MAX(f.description)
            FROM fields f JOIN datasets d ON f.dataset_id=d.id
            WHERE d.region_id=? {cat_clause}
            GROUP BY d.name, d.category, f.field_name, f.field_type""",
        params,
    ).fetchall()

    # 实测副产品：从 backtest_results 取（**只取该区**）
    agg: Dict[str, Dict[str, List]] = {}
    for code, _ds, s, t2, sub, f_, to in cur.execute(
        """SELECT code, dataset, sharpe, two_year_sharpe, sub_universe_sharpe,
                  fitness, turnover
           FROM backtest_results WHERE region=? AND sharpe IS NOT NULL""",
        (region,),
    ):
        fld = field_of(code)
        if not fld:
            continue
        a = agg.setdefault(fld, {"to": [], "s": [], "t2": [], "sub": [], "f": [], "pair": [], "sg_s": [], "sg_t2": [], "sg_sub": []})
        a["s"].append(s)
        if t2 is not None:
            a["t2"].append(t2)
        if sub is not None:
            a["sub"].append(sub)
        if f_ is not None:
            a["f"].append(f_)
        if to is not None:
            a["to"].append(to)
        if t2 is not None:
            a["pair"].append((s, t2))
        if not is_multileg(code):
            a["sg_s"].append(s)
            if t2 is not None:
                a["sg_t2"].append(t2)
            if sub is not None:
                a["sg_sub"].append(sub)

    rows = []
    for ds, cat, fld, ftype, cov, desc in fields:
        a = agg.get(fld)
        n = len(a["s"]) if a else 0
        if a and a["to"]:
            to_med = statistics.median(a["to"])
            to_min, to_max = min(a["to"]), max(a["to"])
        else:
            to_med = to_min = to_max = None
        best_s = max(a["s"]) if (a and a["s"]) else None
        sg = a["sg_s"] if a else []
        best_s_sg = max(sg) if sg else None
        best_2y_sg = max(a["sg_t2"]) if (a and a["sg_t2"]) else None
        best_sub_sg = max(a["sg_sub"]) if (a and a["sg_sub"]) else None
        best_2y = max(a["t2"]) if (a and a["t2"]) else None
        best_sub = max(a["sub"]) if (a and a["sub"]) else None
        best_f = max(a["f"]) if (a and a["f"]) else None
        b2w = None
        if a and a["pair"]:
            b2w = max(a["pair"], key=lambda x: x[0])[1]

        if n == 0:
            if cov is None or norm_cov(cov) is None or norm_cov(cov) < 0.6:
                verdict = "UNUSABLE"
            elif (ftype or "").upper() == "GROUP":
                verdict = "AXIS_ONLY"
            else:
                verdict = "UNTESTED"
        elif to_med is not None and to_med < 0.03:
            verdict = "DEAD_STATIC"
        elif to_med is not None and to_med > 0.70:
            verdict = "DEAD_TURNOVER"
        elif (
            # ★ 2026-10-08：类型判定**以 description 为准**，名字只作辅助（用户指正「读 description 而不是看名字」）。
            #   纯描述驱动比「名字+描述」多捕获 1 例（`oth47_organic_keywords` 名字无 count 但描述
            #   写明 "Count of unique keywords … unit: count"），且不引入 `country`/`accounts` 类假阳性。
            COUNT_DESC_PAT.search(desc or "")
            and not COUNT_DESC_NEG.search(desc or "")
            and best_2y is not None
            and best_2y >= 1.30
            and best_s_sg is not None
            and best_s_sg <= 0.70
        ):
            verdict = "DEAD_COUNT"
        elif best_s_sg is not None and best_s_sg >= 1.58:
            verdict = "ALIVE"
        elif best_s_sg is not None and best_s_sg >= 1.10:
            verdict = "WEAK"
        else:
            verdict = "DEAD"

        rows.append(
            (
                region, ds, cat, fld, ftype, norm_cov(cov), family_of(fld), n,
                round(to_med, 4) if to_med is not None else None,
                round(to_min, 4) if to_min is not None else None,
                round(to_max, 4) if to_max is not None else None,
                best_s, best_2y, best_sub, best_f, b2w, verdict,
                best_s_sg, best_2y_sg, best_sub_sg, len(sg),
            )
        )

    # ★ 多区域隔离：建表用 IF NOT EXISTS（绝不 DROP），清数据只清本区
    ensure_perf_table(con)
    seg = f"DELETE FROM {PERF_TABLE} WHERE region=?" + (" AND category=?" if category else "")
    cur.execute(seg, params)
    if rows:
        cur.executemany(
            f"INSERT OR REPLACE INTO {PERF_TABLE} VALUES (" + ",".join(["?"] * len(rows[0])) + ")",
            rows,
        )
    refresh_views(con, region)
    con.commit()
    print(f"[build] {region}" + (f" / {category}" if category else "") + f" → {len(rows)} 行"
          f"  （视图 {view_name(region)}）")
    dist: Dict[str, int] = {}
    for r in rows:
        dist[r[16]] = dist.get(r[16], 0) + 1
    for k, v in sorted(dist.items(), key=lambda x: -x[1]):
        print(f"   {k:<16}{v:>5}")
    return 0


def build_all_regions(con: sqlite3.Connection) -> int:
    """建所有「有实测数据」的区域画像（互不影响）。"""
    regs = [r[0] for r in con.execute(
        "SELECT DISTINCT region FROM backtest_results WHERE sharpe IS NOT NULL ORDER BY region"
    )]
    if not regs:
        print("[warn] backtest_results 无任何区域的实测数据")
        return 1
    print(f"[all] 将建 {len(regs)} 个区域：{', '.join(regs)}")
    rc = 0
    for r in regs:
        rc |= build(con, r, None)
        print()
    return rc


# ── 查询与盘点 ────────────────────────────────────────────────────────

def query(con, region, category, verdict, min_s, limit):
    cur = con.cursor()
    w, p = ["region=?"], [region]
    if category:
        w.append("lower(category)=lower(?)"); p.append(category)
    if verdict:
        w.append("verdict=?"); p.append(verdict)
    if min_s is not None:
        w.append("COALESCE(best_s_sg,best_s)>=?"); p.append(min_s)
    p.append(limit)
    sql = f"""SELECT dataset, field, ftype, coverage, family, n_tests, to_med,
                     best_s_sg, best_2y_sg, best_sub_sg, verdict, best_s
              FROM {PERF_TABLE} WHERE {' AND '.join(w)}
              ORDER BY COALESCE(best_s_sg,-9) DESC, COALESCE(coverage,0) DESC LIMIT ?"""
    rows = cur.execute(sql, p).fetchall()
    print(f"{'dataset':<18}{'field':<44}{'type':<7}{'cov':>6}{'n':>4}{'to_med':>7}{'S_sg':>6}{'2Y_sg':>7}{'sub':>6}{'S_all':>7}  verdict")
    for ds, fld, ft, cov, fam, n, to, s, t2, sub, v, s_all in rows:
        print(f"{ds[:17]:<18}{fld[:43]:<44}{ft or '':<8}"
              f"{(f'{cov:.2f}' if cov is not None else '-'):>6}{n:>4}"
              f"{(f'{to:.3f}' if to is not None else '-'):>8}"
              f"{(f'{s:.2f}' if s is not None else '-'):>6}"
              f"{(f'{t2:.2f}' if t2 is not None else '-'):>6}"
              f"{(f'{sub:.2f}' if sub is not None else '-'):>6}"
              f"{(f'{s_all:.2f}' if s_all is not None else '-'):>7}  {v}")
    print(f"[query] {region} / {len(rows)} 行")


def list_regions(con) -> int:
    """盘点：列出所有已建画像的区域（行数 + 关键 verdict 计数）。"""
    ensure_perf_table(con)
    rows = con.execute(
        f"""SELECT region, COUNT(*) n,
                   SUM(CASE WHEN verdict NOT IN ('UNTESTED','UNUSABLE','AXIS_ONLY') THEN 1 ELSE 0 END) tested,
                   SUM(CASE WHEN verdict='UNTESTED' THEN 1 ELSE 0 END) untested,
                   SUM(CASE WHEN verdict IN ('ALIVE','WEAK') THEN 1 ELSE 0 END) alive_weak,
                   SUM(CASE WHEN verdict LIKE 'DEAD%' THEN 1 ELSE 0 END) dead
            FROM {PERF_TABLE} GROUP BY region ORDER BY n DESC"""
    ).fetchall()
    if not rows:
        print("[list] 画像为空（先跑 --build --region <R>）")
        return 0
    print(f"{'region':<10}{'总字段':>8}{'已测':>7}{'未测':>7}{'活/弱':>7}{'判死':>7}  视图")
    for r, n, te, un, aw, dd in rows:
        print(f"{r:<10}{n:>8}{te:>7}{un:>7}{aw:>7}{dd:>7}  {view_name(r)}")
    print(f"[list] {len(rows)} 个区域")
    return 0


# ── 一次性迁移（旧表 → 新表 + 视图）──────────────────────────────────

def migrate_legacy(con: sqlite3.Connection, apply: bool) -> int:
    """把旧版 `field_profile_deu` **表** 的存量搬进 `field_profile_perf`，再把旧名改为视图。

    默认 dry-run（只报告），`--apply` 才落盘。已迁移过（旧名已是视图）则直接跳过。
    """
    kind = con.execute("SELECT type FROM sqlite_master WHERE name=?", (LEGACY_NAME,)).fetchone()
    if not kind:
        print(f"[migrate] {LEGACY_NAME} 不存在 → 无需迁移")
        return 0
    if kind[0] == "view":
        print(f"[migrate] {LEGACY_NAME} 已是视图 → 已迁移过，跳过")
        return 0

    n_old = con.execute(f"SELECT COUNT(*) FROM {LEGACY_NAME}").fetchone()[0]
    regions_old = [r[0] for r in con.execute(f"SELECT DISTINCT region FROM {LEGACY_NAME}")]
    print(f"[migrate] 发现旧**表** {LEGACY_NAME}：{n_old} 行，区域={regions_old}")
    print(f"[migrate] 计划：① 建 {PERF_TABLE}（IF NOT EXISTS）"
          f" ② 搬迁这 {n_old} 行 ③ DROP 旧表 ④ 建视图 {LEGACY_NAME}")
    if not apply:
        print("[migrate] dry-run —— 未落盘。加 --apply 执行。")
        return 0

    con.execute("BEGIN")
    try:
        ensure_perf_table(con)
        # 按现表列序搬迁（旧表列序与新表一致，均为 21 列）
        cols = [r[1] for r in con.execute(f"PRAGMA table_info({PERF_TABLE})")]
        col_list = ",".join(cols)
        con.execute(
            f"INSERT OR REPLACE INTO {PERF_TABLE} ({col_list}) SELECT {col_list} FROM {LEGACY_NAME}"
        )
        con.execute(f"DROP TABLE {LEGACY_NAME}")
        con.commit()
    except Exception as e:
        con.rollback()
        print(f"[migrate] 失败并已回滚：{type(e).__name__}: {e}")
        return 1

    for r in regions_old:
        refresh_views(con, r)
    con.commit()
    n_new = con.execute(f"SELECT COUNT(*) FROM {PERF_TABLE}").fetchone()[0]
    print(f"[migrate] ✅ 完成：{PERF_TABLE} 共 {n_new} 行；"
          f"视图 {', '.join(view_name(r) for r in regions_old)}；{LEGACY_NAME} 已改为视图")
    return 0


# ── CLI ───────────────────────────────────────────────────────────────

def main():
    ap = argparse.ArgumentParser(description="多区域字段画像构建器")
    ap.add_argument("--build", action="store_true", help="建某区画像")
    ap.add_argument("--all-regions", action="store_true", help="建全部有实测数据的区（互不影响）")
    ap.add_argument("--query", action="store_true")
    ap.add_argument("--list", action="store_true", help="盘点所有已建画像的区域")
    ap.add_argument("--migrate-legacy", action="store_true", help="一次性迁移旧表（默认 dry-run）")
    ap.add_argument("--apply", action="store_true", help="--migrate-legacy 落盘")
    ap.add_argument("--region", default="DEU")
    ap.add_argument("--category")
    ap.add_argument("--verdict")
    ap.add_argument("--min-s", type=float)
    ap.add_argument("--limit", type=int, default=30)
    a = ap.parse_args()
    if not os.path.exists(DB):
        print(f"[error] 找不到 {DB}")
        return 2
    con = _db_connect(DB)
    try:
        if a.migrate_legacy:
            return migrate_legacy(con, a.apply)
        if a.build:
            return build(con, a.region, a.category)
        if a.all_regions:
            return build_all_regions(con)
        if a.query:
            query(con, a.region, a.category, a.verdict, a.min_s, a.limit)
            return 0
        if a.list:
            return list_regions(con)
        ap.print_help()
        return 2
    finally:
        con.close()


if __name__ == "__main__":
    sys.exit(main())
