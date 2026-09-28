# -*- coding: utf-8 -*-
"""九步流水线 dry-run 演练（独立复跑版，只读 / 零成本 / 不写库）。

与 reports/dryrun_chain_runner_20260927.py 的区别：
  - 独立输出文件名（_v2），不覆写并行会话产物；
  - 每条用例除节点干跑外，额外做**零副作用探针**（DB 行数摘要 + 目录树 mtime 摘要）；
  - 负例校验（故意错误参数必须带可诊断 error）。

覆盖：步1 库存盘点 / 步2 S0 / 步3 S1 / 步4 S2(priors+GEM+选波) / 步5 门禁(两道)
      / 步6 S3 / 步7 S4(诊断+自动评审) / 步8 判定(参考层) / 步9 S6(复盘+点塔+收批)
"""
from __future__ import annotations

import hashlib
import json
import sqlite3
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "src"))

import wqb.workflow.nodes  # noqa: F401,E402  （触发节点注册）
from wqb.workflow.executor import execute  # noqa: E402

DB = REPO / "data" / "wqb.db"
REGION = "GLB"
DS = "model264"
DELAY = 1
UNIVERSE = "TOP3000"
WAVE = "s2_mdl264_trendprob_d1"

CASES = [
    ("步1 S-PRE 库存盘点", "inventory_scan", {"region": REGION, "target": 10}),
    ("步2 S0 数据集体检+打分", "campaign", {"region": REGION, "stage": "S0"}),
    ("步3 S1 字段扫描/理解", "feature_engineering",
     {"region": REGION, "dataset_id": DS, "delay": DELAY, "universe": UNIVERSE}),
    ("步4 S2 priors 组装", "campaign",
     {"region": REGION, "stage": "S2", "subcommand": "assemble-priors"}),
    ("步4 S2 GEM 生成", "gem",
     {"region": REGION, "dataset_id": DS, "delay": DELAY, "universe": UNIVERSE}),
    ("步4 S2 选波(build_wave)", "campaign",
     {"region": REGION, "stage": "S2", "dataset": DS, "wave": WAVE}),
    ("步5 S2→S3 门禁", "wave_gate",
     {"region": REGION, "dataset": DS, "wave": WAVE, "from_db": True}),
    ("步5 合并门禁", "unified_gate",
     {"region": REGION, "dataset": DS, "wave": WAVE, "from_db": True}),
    ("步6 S3 七槽回测", "batch_track",
     {"region": REGION, "wave": WAVE, "dataset": DS}),
    ("步7 S4 诊断改进", "campaign",
     {"region": REGION, "stage": "S4", "dataset": DS, "wave": WAVE}),
    ("步7 S4 自动评审", "auto_review",
     {"region": REGION, "wave": WAVE, "dataset": DS}),
    ("步7 S4 结构变体", "structural_reconstruct",
     {"action": "report", "region": REGION, "wave": WAVE}),
    ("步8 判定(参考层)", "judge", {"alpha_id": "KPNvbQrp"}),
    ("步9 S6 复盘回写", "campaign",
     {"region": REGION, "stage": "S6", "dataset": DS, "wave": WAVE}),
    ("步9 点塔回写", "auto_pyramid", {"region": REGION, "wave": WAVE, "delay": DELAY}),
    ("步9 自动收批", "auto_harvest", {"region": REGION, "wave": WAVE}),
]

NEG_CASES = [
    ("S4 波号不存在", "campaign",
     {"region": REGION, "stage": "S4", "dataset": DS, "wave": "s2_nonexistent_d1"}),
    ("未注册区域 XYZ", "campaign", {"region": "XYZ", "stage": "S2", "subcommand": "assemble-priors"}),
    ("wave_gate 缺 dataset", "wave_gate", {"region": REGION, "wave": WAVE, "from_db": True}),
    ("gem 缺 universe", "gem", {"region": REGION, "dataset_id": DS, "delay": DELAY}),
    ("batch_track 缺 wave", "batch_track", {"region": REGION, "dataset": DS}),
]

TABLES = ["expressions", "backtest_results", "gate_results", "wave_results", "alphas", "ledger_kv"]


def db_digest() -> dict:
    """DB 六表行数 + 文件 sha1（零副作用探针）。"""
    out = {"mtime": DB.stat().st_mtime_ns if DB.exists() else None,
           "size": DB.stat().st_size if DB.exists() else None}
    try:
        c = sqlite3.connect(f"file:{DB.as_posix()}?mode=ro", uri=True)
        for t in TABLES:
            try:
                out[t] = c.execute(f"select count(*) from {t}").fetchone()[0]
            except Exception as e:  # noqa: BLE001
                out[t] = f"ERR:{e}"
        c.close()
    except Exception as e:  # noqa: BLE001
        out["db_open_error"] = str(e)
    return out


def tree_digest() -> dict:
    """仓库内可能被干跑污染的目录摘要（计数 + 最新 mtime）。"""
    watch = ["logs", "tracking", "data", "reports", "cache", "output_report"]
    out = {}
    for w in watch:
        p = REPO / w
        if not p.exists():
            out[w] = None
            continue
        files = [f for f in p.rglob("*") if f.is_file()]
        out[w] = {"n": len(files),
                  "max_mtime": max((f.stat().st_mtime_ns for f in files), default=0)}
    return out


def brief(output, limit=700):
    s = json.dumps(output, ensure_ascii=False, default=str)
    return s if len(s) <= limit else s[:limit] + " …(截断)"


def run_cases(cases, kind):
    rows = []
    for label, node, params in cases:
        try:
            r = execute(node, params, dry_run=True)
            d = r.to_dict()
            row = {"kind": kind, "label": label, "node": node, "params": params,
                   "success": d.get("success"), "error": d.get("error"),
                   "output_brief": brief(d.get("output"))}
        except Exception as exc:  # noqa: BLE001
            row = {"kind": kind, "label": label, "node": node, "params": params,
                   "success": False, "error": f"{type(exc).__name__}: {exc}",
                   "output_brief": ""}
        rows.append(row)
        flag = "OK  " if row["success"] else "FAIL"
        print(f"[{flag}] {label}  (node={node})")
        if not row["success"]:
            print(f"        error: {row['error']}")
    return rows


def main() -> int:
    print("=== 演练前快照 ===")
    before_db, before_tree = db_digest(), tree_digest()
    print(json.dumps(before_db, ensure_ascii=False))

    print("\n=== 正例：九步节点干跑 ===")
    rows = run_cases(CASES, "positive")

    print("\n=== 负例：故意错误参数必须被拦且带 error ===")
    negs = run_cases(NEG_CASES, "negative")

    print("\n=== 演练后快照 ===")
    after_db, after_tree = db_digest(), tree_digest()
    print(json.dumps(after_db, ensure_ascii=False))

    side = {"db_changed": before_db != after_db,
            "tree_changed": {k: (before_tree[k], after_tree[k])
                             for k in before_tree if before_tree[k] != after_tree[k]}}
    print("\n零副作用检查:", json.dumps(side, ensure_ascii=False))

    out = Path(__file__).resolve().parent / "dryrun_chain_result_v2_20260927.json"
    out.write_text(json.dumps(
        {"before": before_db, "after": after_db,
         "side_effects": side, "positive": rows, "negative": negs},
        ensure_ascii=False, indent=2), encoding="utf-8")

    ok = sum(1 for r in rows if r["success"])
    neg_ok = sum(1 for r in negs if (not r["success"]) and r["error"])
    print(f"\n== 正例 {ok}/{len(rows)} 通过；负例 {neg_ok}/{len(negs)} 被拦且带 error -> {out}")
    return 0 if (ok == len(rows) and neg_ok == len(negs)) else 1


if __name__ == "__main__":
    raise SystemExit(main())
