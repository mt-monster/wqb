# -*- coding: utf-8 -*-
"""persist_prod_corr.py — 把相关性抽样结果落库到 alphas（prod / self）。

背景（S123 报告建议②）：`tools/triage_prodcorr_batch.py`（分诊第三步）已实现
零成本抽测——按提交层预筛（sharpe≥1.58 & fitness≥1.0 & 2Y≥1.58 & margin 非空）、
族去重、checkpoint 续跑——但结果只写在 `logs/_triage_prodcorr.json`，
**从不回写 alphas 表** → SOP 的「prod-first 0.6 预警线」始终无过程数据可触发
（实测 alphas 4,038 行仅 270 有值，全来自提交后同步）。

本工具把 checkpoint 中的量测值回填进 alphas：
  - 只填 NULL（不覆盖既有值/提交后同步值），`--overwrite` 可强制覆盖；
  - 跳过 error 条目与非数值；
  - 幂等：重跑零变化；
  - 2026-09-18 扩展：支持 `self` 字段与 `source` 溯源标记
    （triage_local / platform_sync / manual），与 CampaignStore.persist_correlation
    同一契约（[0,1] 区间校验）。

用法（默认 dry-run）：
  python tools/persist_prod_corr.py                 # 预览将回填的行
  python tools/persist_prod_corr.py --apply         # 实际写库
  python tools/persist_prod_corr.py --state 其他.json
  python tools/persist_prod_corr.py --apply --source platform_sync --overwrite
"""
import argparse
import json
import os
import sqlite3
import sys
from datetime import datetime

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_STATE = os.path.join(REPO, "logs", "_triage_prodcorr.json")
DEFAULT_DB = os.path.join(REPO, "data", "wqb.db")

# checkpoint 中可能出现的键名（不同版本 triage 脚本写法不一）
_PROD_KEYS = ("prod", "prod_corr", "prod_correlation")
_SELF_KEYS = ("self", "self_corr", "self_correlation")


def _pick(d, keys):
    for k in keys:
        if d.get(k) is not None:
            return d.get(k)
    return None


def _valid(v):
    """[0,1] 区间校验；None / 非数值 / 越界 → None。"""
    if v is None:
        return None
    if isinstance(v, bool):
        return None
    try:
        f = float(v)
    except (TypeError, ValueError):
        return None
    if f < 0.0 or f > 1.0:
        return None
    return f


def _ensure_columns(conn):
    """防御性补列（正常由 CampaignStore.ensure_schema 建好）。"""
    cols = {r[1] for r in conn.execute("PRAGMA table_info(alphas)")}
    for col, ddl in (("prod_corr_source", "TEXT"), ("corr_checked_at", "TIMESTAMP")):
        if col not in cols:
            conn.execute(f"ALTER TABLE alphas ADD COLUMN {col} {ddl}")
    conn.commit()


def main():
    ap = argparse.ArgumentParser(description="prod/self 相关性抽样结果落库（默认 dry-run）")
    ap.add_argument("--state", default=DEFAULT_STATE)
    ap.add_argument("--db", default=DEFAULT_DB)
    ap.add_argument("--source", default="triage_local",
                    help="来源标记（triage_local/platform_sync/manual）")
    ap.add_argument("--overwrite", action="store_true",
                    help="覆盖已有值（默认只填 NULL，保留平台权威值）")
    ap.add_argument("--apply", action="store_true", help="实际写库（缺省只预览）")
    a = ap.parse_args()

    with open(a.state, encoding="utf-8") as f:
        state = json.load(f)
    if not isinstance(state, dict):
        print(f"[error] checkpoint 顶层应为 dict，实为 {type(state).__name__}")
        sys.exit(1)

    to_fill, skipped = [], []
    for key, v in state.items():
        if not isinstance(v, dict) or "error" in v:
            skipped.append((key, "error 条目"))
            continue
        aid = v.get("alpha_id") or key
        prod = _valid(_pick(v, _PROD_KEYS))
        self_ = _valid(_pick(v, _SELF_KEYS))
        if not aid:
            skipped.append((key, "缺 alpha_id"))
            continue
        if prod is None and self_ is None:
            skipped.append((key, "prod/self 均非有效数值"))
            continue
        to_fill.append((aid, prod, self_, key))

    conn = sqlite3.connect(a.db)
    conn.row_factory = sqlite3.Row
    _ensure_columns(conn)
    updated, already, missing = [], 0, []
    for aid, prod, self_, key in to_fill:
        row = conn.execute(
            "SELECT prod_correlation, self_correlation FROM alphas WHERE alpha_id=?",
            (aid,),
        ).fetchone()
        if row is None:
            missing.append((aid, key))
            continue
        cur_prod, cur_self = _valid(row["prod_correlation"]), _valid(row["self_correlation"])
        new_prod = prod if (prod is not None and (a.overwrite or cur_prod is None)) else None
        new_self = self_ if (self_ is not None and (a.overwrite or cur_self is None)) else None
        if new_prod is None and new_self is None:
            already += 1
        else:
            updated.append((aid, new_prod, new_self))

    print(f"checkpoint 条目 = {len(state)}：可回填 {len(updated)} | 已有值跳过 {already} | "
          f"alphas 无此 id {len(missing)} | 无效条目 {len(skipped)}")
    for aid, prod, self_ in updated[:8]:
        print(f"  将回填 {aid} → prod={prod} self={self_}")
    if missing:
        print(f"  无此 id 样例: {[m[0] for m in missing[:5]]}")

    if not a.apply:
        print(f"\n[dry-run] 未写库。确认后加 --apply --source {a.source}"
              + (" --overwrite" if a.overwrite else ""))
        return
    now = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    conn.execute("BEGIN")
    for aid, prod, self_ in updated:
        sets, vals = [], []
        if prod is not None:
            sets.append("prod_correlation=?")
            vals.append(prod)
        if self_ is not None:
            sets.append("self_correlation=?")
            vals.append(self_)
        sets += ["prod_corr_source=?", "corr_checked_at=?", "updated_at=?"]
        vals += [a.source, now, now, aid]
        conn.execute(f"UPDATE alphas SET {', '.join(sets)} WHERE alpha_id=?", vals)
    conn.commit()
    print(f"\n[apply] 已回填 {len(updated)} 行 → alphas（source={a.source}）")


if __name__ == "__main__":
    main()
