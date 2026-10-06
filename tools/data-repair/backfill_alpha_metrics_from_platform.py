# -*- coding: utf-8 -*-
"""backfill_alpha_metrics_from_platform.py — 从平台补 `alphas` / `submit_ready` 缺失的 IS 指标。

★ 为什么需要它（2026-10-06 定案）
  平台**有** two_year_sharpe / sub_universe_sharpe（在 `get_alpha_details` 的
  `is.checks` 各 check 的 `value`，或 `metrics.*`），但部分本地入库路径没抽：
    - `tools/sync_platform_alphas.py` 曾**显式传 two_year_sharpe=None**（已修）；
    - 非 harvest 路径（无 `backtest_results` 行，如 `P0gv3AO7`）从不抽 2Y/sub。
  全库实测 **1798/11002 行 2Y 为 NULL**。本工具按需从平台回填，**不改 ingest 逻辑、不改回测**。

★ 覆盖两张表（2026-10-06 04:00 扩展；04:28 再扩 margin/约束变体）
  - `--table alphas`（默认）：补 `two_year_sharpe` / `sub_universe_sharpe` / `is_ladder_sharpe`。
  - `--table submit_ready`：补「体检卡三层」所需的一组 IS 指标（**直连路线候选**——只在
    submit_ready 登记、不在 `alphas`，原工具够不到；如 `N1VnJjXg`）：
      two_year / sub_universe / margin / returns / drawdown / long_count / short_count
      / investability_constrained_sharpe / risk_neutralized_sharpe。
    该表**无 updated_at 列**，只写指标。
  - `--table both`：两表各跑一遍。checkpoint 键对 submit_ready 加 `sr:` 前缀，避免与 alphas 撞键。

★ 口径
  - 目标 = 目标表中**任一映射列为空**的行（可筛区/状态/IDs/仅闸内）。
  - 只**补空**：已有值的列不覆盖（`--overwrite` 才覆盖）。
  - **每颗落盘可断点续跑**（checkpoint `results/backfill_alpha_metrics_checkpoint.json`）；
    checkpoint 记录「本行覆盖过的列集」，新增映射列时旧的 `sr:` 条目**不会**把新列误跳过。
  - 默认 **dry-run**；`--apply` 才写库。纯 GET 只读平台，不占相关性队列。
用法:
  python tools/data-repair/backfill_alpha_metrics_from_platform.py                                 # dry-run（默认 alphas 全库 NULL 行）
  python tools/data-repair/backfill_alpha_metrics_from_platform.py --only-gate                     # 只看「过 IS 闸」的 NULL 行
  python tools/data-repair/backfill_alpha_metrics_from_platform.py --region GBR                    # 限区
  python tools/data-repair/backfill_alpha_metrics_from_platform.py --ids P0gv3AO7 xAb1             # 指定颗（alphas）
  python tools/data-repair/backfill_alpha_metrics_from_platform.py --table submit_ready --status READY   # 补 READY 行（直连候选）
  python tools/data-repair/backfill_alpha_metrics_from_platform.py --table both --status READY --apply
退出码: 0=正常  3=DB/平台失败
"""
from __future__ import annotations

import argparse
import asyncio
import json
import os
import sqlite3
import sys
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple

_sys_pe = sys
_os_pe = os
_sys_pe.path.insert(0, _os_pe.path.dirname(_os_pe.path.dirname(_os_pe.path.abspath(__file__))))


REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
MCP_DIR = os.path.join(REPO_ROOT, "world-quant-brain-mcp")
DB = os.path.join(REPO_ROOT, "data", "wqb.db")
CKPT = os.path.join(REPO_ROOT, "results", "backfill_alpha_metrics_checkpoint.json")

# 每张表的「本地列 → 平台指标键」映射 + 是否有 updated_at 列。
TABLE_SPEC: Dict[str, Dict[str, Any]] = {
    "alphas": {
        "cols": [("two_year_sharpe", "two_year_sharpe"),
                 ("sub_universe_sharpe", "sub_universe_sharpe"),
                 ("is_ladder_sharpe", "is_ladder_sharpe")],
        "updated_at": "updated_at",
        # alphas 的目标集**保持不变**（只认 2Y/sub 为空），避免把 margin 等
        # 早已由 ingest 填好的列也拖进目标集、把目标数从 1798 炸到全库。
        "predicate": "(a.two_year_sharpe IS NULL OR a.sub_universe_sharpe IS NULL)",
    },
    "submit_ready": {
        "cols": [("two_year", "two_year_sharpe"),
                 ("sub_universe", "sub_universe_sharpe"),
                 # 2026-10-06 04:28：体检卡三层的台账落点（与 submit_ready 新增 7 列同批）
                 ("margin", "margin"),
                 ("returns", "returns"),
                 ("drawdown", "drawdown"),
                 ("long_count", "long_count"),
                 ("short_count", "short_count"),
                 ("investability_constrained_sharpe", "investability_constrained_sharpe"),
                 ("risk_neutralized_sharpe", "risk_neutralized_sharpe")],
        "updated_at": None,
        # 目标 = 任一映射列为空的 READY 候选（新列刚加时全员为空 → 一次补齐）。
        "predicate": None,   # None = 由 _null_predicate 动态生成
    },
}


def _want_cols(table: str) -> List[str]:
    return [c for c, _ in TABLE_SPEC[table]["cols"]]


def _null_predicate(table: str) -> str:
    """目标谓词：任一映射列为空。alphas 用固定 predicate（见 TABLE_SPEC 注释），
    submit_ready 动态生成。"""
    spec = TABLE_SPEC[table]
    if spec.get("predicate"):
        return str(spec["predicate"])
    return "(" + " OR ".join(f"{c} IS NULL" for c in _want_cols(table)) + ")"


def _first_not_none(*vals: Any) -> Optional[float]:
    for v in vals:
        if v is not None:
            return v
    return None


def extract_is_metrics(d: Dict[str, Any]) -> Tuple[Optional[float], Optional[float], Optional[float]]:
    """从 `get_alpha_details` 的对象里抽 (two_year, sub_universe, is_ladder)。

    兼容平台多种形态：`is.checks[].value`（LOW_2Y_SHARPE / LOW_SUB_UNIVERSE_SHARPE /
    IS_LADDER_SHARPE）、`is.*` 扁平、`metrics.*`。
    """
    isd = d.get("is") or {}
    met = d.get("metrics") or {}
    ty = sub = ladder = None
    for c in (isd.get("checks") or []):
        if not isinstance(c, dict):
            continue
        n, v = c.get("name"), c.get("value")
        if v is None:
            continue
        if n == "LOW_2Y_SHARPE":
            ty = v
        elif n == "LOW_SUB_UNIVERSE_SHARPE":
            sub = v
        elif n == "IS_LADDER_SHARPE":
            ladder = v
    ty = _first_not_none(ty, isd.get("two_year_sharpe"), met.get("two_year_sharpe"),
                         (d.get("two_year_sharpe")))
    sub = _first_not_none(sub, isd.get("sub_universe_sharpe"), met.get("sub_universe_sharpe"),
                          (d.get("sub_universe_sharpe")))
    ladder = _first_not_none(ladder, isd.get("is_ladder_sharpe"), met.get("is_ladder_sharpe"))
    return ty, sub, ladder


def load_ckpt() -> Dict[str, Any]:
    if os.path.exists(CKPT):
        try:
            return json.load(open(CKPT, encoding="utf-8"))
        except Exception:
            pass
    return {"done": {}}


def save_ckpt(ck: Dict[str, Any]) -> None:
    os.makedirs(os.path.dirname(CKPT), exist_ok=True)
    tmp = CKPT + ".tmp"
    json.dump(ck, open(tmp, "w", encoding="utf-8"), ensure_ascii=False)
    os.replace(tmp, CKPT)


def ckpt_key(table: str, alpha_id: str) -> str:
    """checkpoint 键：alphas 保持裸 alpha_id（向后兼容）；submit_ready 加 sr: 前缀防撞键。"""
    return alpha_id if table == "alphas" else f"sr:{alpha_id}"


def _covered(entry: Any, want: List[str]) -> bool:
    """该 checkpoint 条目是否已覆盖当前要补的**全部**列。

    旧格式条目（只有 two_year_sharpe/… 无 `cols`）视为**未覆盖** → 新增映射列时会被
    重新处理（这正是我们要的：加了 margin 等新列后，旧 `sr:` 条目不能把它们跳过）。
    """
    if not isinstance(entry, dict):
        return False
    cols = entry.get("cols")
    if not isinstance(cols, dict):
        return False
    return all(c in cols for c in want)


def pick_targets(con: sqlite3.Connection, table: str, region: Optional[str],
                 only_gate: bool, ids: Optional[List[str]], limit: Optional[int],
                 status: Optional[str]) -> List[Tuple[str, Optional[str]]]:
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    if table == "alphas":
        if ids:
            q = ("SELECT a.alpha_id, r.name region FROM alphas a LEFT JOIN regions r ON a.region_id=r.id "
                 "WHERE a.alpha_id IN (" + ",".join("?" * len(ids)) + ")")
            return [(r["alpha_id"], r["region"]) for r in cur.execute(q, ids).fetchall()]
        q = ("SELECT a.alpha_id, r.name region FROM alphas a LEFT JOIN regions r ON a.region_id=r.id "
             "WHERE (a.two_year_sharpe IS NULL OR a.sub_universe_sharpe IS NULL)")
        ps: List[Any] = []
        if region:
            q += " AND r.name = ?"
            ps.append(region)
        if only_gate:
            q += (" AND COALESCE(a.status,'') IN ('UNSUBMITTED','COMPLETE') "
                  "AND COALESCE(a.soft_deleted,0)=0 AND COALESCE(a.disposition,'')<>'DEAD' "
                  "AND COALESCE(a.platform_status,'') NOT IN ('ACTIVE','DECOMMISSIONED') "
                  "AND a.date_submitted IS NULL "
                  "AND a.sharpe>=1.58 AND a.fitness>=1.0 "
                  "AND (a.prod_correlation IS NULL OR a.prod_correlation<0.7)")
        q += " ORDER BY a.sharpe DESC"
        if limit:
            q += f" LIMIT {int(limit)}"
        return [(r["alpha_id"], r["region"]) for r in cur.execute(q, ps).fetchall()]

    # submit_ready（直连候选，region 是独立文本列）
    if ids:
        q = ("SELECT alpha_id, region FROM submit_ready WHERE alpha_id IN ("
             + ",".join("?" * len(ids)) + ")")
        return [(r["alpha_id"], r["region"]) for r in cur.execute(q, ids).fetchall()]
    q = f"SELECT alpha_id, region FROM submit_ready WHERE {_null_predicate('submit_ready')}"
    ps = []
    if region:
        q += " AND region = ?"
        ps.append(region)
    if status:
        q += " AND status = ?"
        ps.append(status)
    if only_gate:  # submit_ready 语境下「过闸」= READY
        q += " AND status = 'READY'"
    q += " ORDER BY sharpe DESC"
    if limit:
        q += f" LIMIT {int(limit)}"
    return [(r["alpha_id"], r["region"]) for r in cur.execute(q, ps).fetchall()]


async def fetch_metrics(alpha_id: str) -> Dict[str, Any]:
    """一次 GET，返回**所有映射平台键**的取值（供 alphas / submit_ready 共用）。

    兼容平台多种形态：`is.checks[].value`、`is.*` 扁平、`metrics.*`，以及约束变体
    `is.investabilityConstrained.sharpe` / `is.riskNeutralized.sharpe`。
    """
    from brain_api import brain_client
    d = await brain_client.get_alpha_details(alpha_id)
    if isinstance(d, dict) and isinstance(d.get("result"), dict):
        d = d["result"]
    d = d or {}
    isd = d.get("is") or {}
    ty, sub, ladder = extract_is_metrics(d)

    def _cons(name: str, key: str = "sharpe") -> Optional[float]:
        blk = isd.get(name)
        return blk.get(key) if isinstance(blk, dict) else None

    return {
        # alphas 侧（3）
        "two_year_sharpe": ty,
        "sub_universe_sharpe": sub,
        "is_ladder_sharpe": ladder,
        # submit_ready 侧（7）
        "margin": isd.get("margin"),
        "returns": isd.get("returns"),
        "drawdown": isd.get("drawdown"),
        "long_count": isd.get("longCount"),
        "short_count": isd.get("shortCount"),
        "investability_constrained_sharpe": _cons("investabilityConstrained"),
        "risk_neutralized_sharpe": _cons("riskNeutralized"),
    }


def run_table(con: sqlite3.Connection, table: str, a: argparse.Namespace,
              done: Dict[str, Any]) -> Tuple[int, int, int]:
    """处理单张表；返回 (补到, 无值, 失败)。就地更新 done（由调用方负责落盘）。"""
    spec = TABLE_SPEC[table]
    cur = con.cursor()
    try:
        targets = pick_targets(con, table, a.region, a.only_gate, a.ids, a.limit, a.status)
    except Exception as e:  # noqa: BLE001
        print(f"[ERROR] {table} 查询失败: {e}", file=sys.stderr)
        raise
    todo = [t for t in targets if not _covered(done.get(ckpt_key(table, t[0])), _want_cols(table))]
    print(f"[{table}] 目标 {len(targets)} 颗（已跳过已完成 {len(targets)-len(todo)}）; 待处理 {len(todo)}"
          f"; 映射列 {[c for c, _ in spec['cols']]}")
    if not a.apply:
        for aid, reg in todo[:20]:
            print(f"  {aid} [{reg}]")
        if len(todo) > 20:
            print(f"  … 其余 {len(todo)-20} 条")
        return 0, 0, 0

    ts = datetime.now().isoformat(timespec="seconds")
    got = miss = err = 0
    for i, (aid, reg) in enumerate(todo):
        try:
            m = asyncio.run(fetch_metrics(aid))
        except Exception as e:  # noqa: BLE001
            err += 1
            done[ckpt_key(table, aid)] = {"error": str(e)[:120]}
            save_ckpt({"done": done})
            print(f"  [err] {aid}: {str(e)[:100]}")
            continue
        sets, vals = [], []
        for col, key in spec["cols"]:
            v = m.get(key)
            if v is None:
                continue
            if a.overwrite:
                sets.append(f"{col}=?")
                vals.append(v)
            else:
                sets.append(f"{col}=COALESCE({col}, ?)")
                vals.append(v)
        record = {col: m.get(key) for col, key in spec["cols"]}
        if sets:
            if spec["updated_at"]:
                sets.append(f"{spec['updated_at']}=?")
                vals.append(ts)
            cur.execute(f"UPDATE {table} SET {', '.join(sets)} WHERE alpha_id=?", vals + [aid])
            con.commit()
            got += 1
            done[ckpt_key(table, aid)] = {"cols": record}
        else:
            miss += 1
            done[ckpt_key(table, aid)] = {"cols": record, "no_metrics": True}
        save_ckpt({"done": done})
        if (i + 1) % 25 == 0:
            print(f"  进度 {i+1}/{len(todo)} 补到={got} 无值={miss} 失败={err}")
    print(f"[{table}] 完成：补到 {got} / 无值 {miss} / 失败 {err}")
    return got, miss, err


def main() -> int:
    ap = argparse.ArgumentParser(description="从平台补 alphas/submit_ready 缺失的 2Y/sub（只补空）")
    ap.add_argument("--table", choices=["alphas", "submit_ready", "both"], default="alphas",
                    help="目标表（默认 alphas；submit_ready=直连候选；both=两表）")
    ap.add_argument("--region", default=None, help="限区（如 GBR）")
    ap.add_argument("--status", default=None, help="仅 submit_ready：限状态（如 READY）")
    ap.add_argument("--only-gate", action="store_true", help="只处理过 IS 闸的 NULL 行（submit_ready 语境=READY）")
    ap.add_argument("--ids", nargs="*", default=None, help="指定 alpha_id 列表")
    ap.add_argument("--limit", type=int, default=None, help="最多处理条数（按 sharpe 降序）")
    ap.add_argument("--apply", action="store_true", help="写库（默认 dry-run）")
    ap.add_argument("--overwrite", action="store_true", help="已有值的列也覆盖")
    a = ap.parse_args()

    tables = ["alphas", "submit_ready"] if a.table == "both" else [a.table]

    try:
        con = sqlite3.connect(DB, timeout=15)
    except Exception as e:  # noqa: BLE001
        print(f"[ERROR] DB 打开失败: {e}", file=sys.stderr)
        return 3
    con.row_factory = sqlite3.Row

    ck = load_ckpt()
    done = ck.get("done", {})

    totals = [0, 0, 0]
    try:
        for table in tables:
            g, m, e_ = run_table(con, table, a, done)
            totals[0] += g
            totals[1] += m
            totals[2] += e_
    except Exception as e:  # noqa: BLE001
        print(f"[ERROR] {e}", file=sys.stderr)
        con.close()
        return 3

    if not a.apply:
        print("[dry-run] 未写库；加 --apply 生效。")
    else:
        print(f"\n[apply] 合计：补到 {totals[0]} / 无值 {totals[1]} / 失败 {totals[2]}（checkpoint={CKPT}）")
        for table in tables:
            spec = TABLE_SPEC[table]
            if not spec["cols"]:
                continue
            c0 = spec["cols"][0][0]
            r = con.execute(f"SELECT COUNT(*), SUM(CASE WHEN {c0} IS NOT NULL THEN 1 ELSE 0 END) "
                            f"FROM {table}").fetchone()
            print(f"{table} 现状: 总量={r[0]} {c0}有值={r[1]}")
    con.close()
    return 0


if __name__ == "__main__":
    sys.path.insert(0, MCP_DIR)
    try:
        import _pyenv  # type: ignore  # noqa: E402
        _pyenv.reexec_under_venv()
    except Exception:
        pass
    sys.exit(main())
