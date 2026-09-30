#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""shape_quota_check.py — 模板形状配额机检（ra-pipeline 步 4 §4.5.1，步 5 门禁前跑）。

准则：每波候选（ideas 渲染或 LLM 产出）须覆盖 ≥ 3 个形状族，且 `trade_when` 类条件式占比 ≤ 40%。
背景：wave84 / 85 实测——19 条选中仅约 9 个算子形状、`trade_when` 占比 62%（反模板同质化）。
分类规则、阈值与取值理由见 `src/wqb/shape_quota.py`（启发式：看表达式里出现了哪些定义架构的算子，每条只归一个主形状族）。

用法：
  python tools/shape_quota_check.py --region KOR --wave 97 [--dataset analyst4] [--verbose] [--json]

候选 = 库里该波 `expressions` 中 status 不是 superseded / dropped / deferred 的条目（与 `CampaignStore.list_expressions` 的缺省口径一致——
就是后面会进门禁 / 回测的那批）。**只读**：不写库、不建库。

退出码：0 = 达标，或候选不足 3 条（配额在构造上无法满足，探针批 / 单信号验证波，裁决记 n/a）；1 = 不达标（列出违反项）；
2 = 无法检查（库不存在 / 表缺失 / 本波在库里没有候选——步 4 没做完）。

不做的事：不判合规（比值 / 价差要不要满足步 7 §7.7.2、是否混信号，归闸 5 与人）；不入闸链（批级多样性的权威是闸 6，本检查是步 5 前的人可读体检）。
"""
from __future__ import annotations

import argparse
import json
import os
import sqlite3
import sys
from typing import Any, Dict, List, Optional

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_SRC = os.path.join(REPO_ROOT, "src")
if _SRC not in sys.path:
    sys.path.insert(0, _SRC)

from wqb import db_conn  # noqa: E402
from wqb import shape_quota as SQ  # noqa: E402

#: 与 `CampaignStore.list_expressions` 缺省过滤同口径的「不参与选波 / 回测」状态（tests/unit/test_shape_quota.py 守它们不漂移）
EXCLUDED_STATUS = ("superseded", "dropped", "deferred")


class CheckError(Exception):
    """无法检查（退出码 2）。"""


def _db_path(cli_db: Optional[str]) -> str:
    return db_conn.default_db_path() if not cli_db else cli_db


def load_candidates(db_path: str, region: str, wave: str, dataset: Optional[str] = None) -> List[Dict[str, Any]]:
    """本波候选（只读）。库不存在 / 表缺失 → `CheckError`。"""
    if not os.path.isfile(db_path):
        raise CheckError(f"库不存在：{db_path}（--db / WQB_DB_PATH）")
    try:
        conn = db_conn.connect(db_path, readonly=True, row_factory=sqlite3.Row)
    except sqlite3.Error as e:
        raise CheckError(f"打不开库：{e}")
    try:
        cols = {r[1] for r in conn.execute("PRAGMA table_info(expressions)")}
        if not {"expression", "status", "region", "wave"} <= cols:
            raise CheckError("expressions 表缺失或缺 region / wave 列（旧库未迁移？）")
        sql = "SELECT id, expression, status, " + ("dataset" if "dataset" in cols else "NULL AS dataset") + \
              " FROM expressions WHERE region = ? AND wave = ? AND status NOT IN (%s)" % ",".join("?" * len(EXCLUDED_STATUS))
        args: List[Any] = [region, str(wave), *EXCLUDED_STATUS]
        if dataset and "dataset" in cols:
            sql += " AND (dataset = ? OR dataset IS NULL)"
            args.append(dataset)
        return [dict(r) for r in conn.execute(sql + " ORDER BY id", args)]
    except sqlite3.Error as e:
        raise CheckError(f"读库失败：{e}")
    finally:
        conn.close()


def render(res: Dict[str, Any], region: str, wave: str, rows: List[Dict[str, Any]], verbose: bool) -> str:
    n = res["n"]
    out = [f"=== shape quota | {region} wave {wave} | 候选 {n} 条（status 不含 {'/'.join(EXCLUDED_STATUS)}）==="]
    if n:
        out.append("形状族分布（每条只归一个主形状族）：")
        for fam, cnt in res["families"].items():
            out.append(f"  {fam:<12} {cnt:>3}  {cnt / n:>4.0%}")
    th = res["thresholds"]
    out.append(f"形状族 {res['n_families']} 个（须 ≥ {th['min_families']}）；trade_when 占比 {res['trade_when_share']:.0%}"
               f"（须 ≤ {th['max_trade_when_share']:.0%}）")
    for note in res["notes"]:
        out.append(f"  · {note}")
    for issue in res["issues"]:
        out.append(f"  ✗ {issue}")
    if verbose:
        out.append("逐条：")
        for r in rows:
            tags = SQ.shape_tags(r["expression"])
            out.append(f"  [{tags[0]:<11}] {'+'.join(tags[1:]) or '-':<20} {str(r['expression'])[:110]}")
    out.append({SQ.VERDICT_PASS: "[PASS] 形状配额达标", SQ.VERDICT_NA: "[N/A] 候选不足，不判",
                SQ.VERDICT_FAIL: "[FAIL] 形状配额不达标——补形状（步 4 §4.5.1 第 2、3、5 条：事件条件化换形状、形状发现走非契约探索波、KB 模板），"
                                 "不要靠补参数变体凑数"}[res["verdict"]])
    return "\n".join(out)


def main(argv: Optional[List[str]] = None) -> int:
    ap = argparse.ArgumentParser(description="模板形状配额机检：每波 ≥3 个形状族、trade_when 占比 ≤40%（只读）")
    ap.add_argument("--region", required=True, help="区域（如 KOR）")
    ap.add_argument("--wave", required=True, help="波号（整数或字符串波号）")
    ap.add_argument("--dataset", default=None, help="只看某个数据集的候选（缺省全波）")
    ap.add_argument("--db", default=None, help="DB 路径（缺省 WQB_DB_PATH / <repo>/data/wqb.db）")
    ap.add_argument("--min-families", type=int, default=SQ.MIN_FAMILIES, help=f"最少形状族数（缺省 {SQ.MIN_FAMILIES}）")
    ap.add_argument("--max-trade-when", type=float, default=SQ.MAX_TRADE_WHEN_SHARE,
                    help=f"trade_when 占比上限（缺省 {SQ.MAX_TRADE_WHEN_SHARE}）")
    ap.add_argument("--verbose", action="store_true", help="逐条列出每条表达式的形状族")
    ap.add_argument("--json", action="store_true", help="输出 JSON（机器可读）")
    a = ap.parse_args(argv)
    try:
        rows = load_candidates(_db_path(a.db), a.region.strip(), str(a.wave).strip(), a.dataset)
        if not rows:
            raise CheckError(f"{a.region} wave {a.wave} 在库里没有候选（status 不含 {'/'.join(EXCLUDED_STATUS)}）——步 4 没做完，"
                             "或区域 / 波号写错（字符串波号如 s2_<ds>_d1 要原样传）")
    except CheckError as e:
        print(f"[shape_quota] 无法检查：{e}", file=sys.stderr)
        if a.json:
            print(json.dumps({"verdict": "error", "error": str(e)}, ensure_ascii=False))
        return 2
    res = SQ.check_quota([r["expression"] for r in rows], a.min_families, a.max_trade_when)
    res.update(region=a.region.strip(), wave=str(a.wave).strip(), dataset=a.dataset)
    if a.json:
        if a.verbose:
            res["items"] = [{"id": r["id"], "expression": r["expression"], "families": SQ.shape_tags(r["expression"])} for r in rows]
        print(json.dumps(res, ensure_ascii=False))
    else:
        print(render(res, a.region.strip(), str(a.wave).strip(), rows, a.verbose))
    return 1 if res["verdict"] == SQ.VERDICT_FAIL else 0


if __name__ == "__main__":
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import _pyenv  # noqa: E402  文档里写的是 `python tools/shape_quota_check.py`——保持与其它工具一致的解释器解析
    _pyenv.reexec_under_venv()
    sys.exit(main())
