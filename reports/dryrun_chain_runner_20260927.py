# -*- coding: utf-8 -*-
"""九步流水线 dry-run 演练（只读 / 零成本 / 不写库）。

对 wq-brain-ra-pipeline 九步中可映射到 workflow 节点的阶段逐节点干跑：
  步2 S0 -> campaign(stage=S0)
  步3 S1 -> feature_engineering
  步4 S2 -> gem / gem_wave / campaign(stage=S2, subcommand=assemble-priors)
  步5 门禁 -> wave_gate / unified_gate / hypothesis_round
  步6 S3 -> batch_track
  步7 S4 -> campaign(stage=S4) / auto_review / alpha_booster / modeb_improve
  步8 提交 -> judge（参考层；submit_alpha 需用户确认，不在演练内）
  步9 S6 -> campaign(stage=S6) / auto_pyramid / auto_harvest
步1 S-PRE 与库存盘点 -> inventory_scan
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "src"))

from wqb.workflow.executor import execute  # noqa: E402

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
    ("步8 判定(参考层)", "judge", {"alpha_id": "KPNvbQrp"}),
    ("步9 S6 复盘回写", "campaign",
     {"region": REGION, "stage": "S6", "dataset": DS, "wave": WAVE}),
    ("步9 点塔回写", "auto_pyramid", {"region": REGION, "wave": WAVE, "delay": DELAY}),
    ("步9 自动收批", "auto_harvest", {"region": REGION, "wave": WAVE}),
]


def brief(output, limit=900):
    s = json.dumps(output, ensure_ascii=False, default=str)
    return s if len(s) <= limit else s[:limit] + " …(截断)"


def main() -> int:
    rows = []
    for label, node, params in CASES:
        try:
            r = execute(node, params, dry_run=True)
            d = r.to_dict()
            row = {
                "label": label,
                "node": node,
                "params": params,
                "success": d["success"],
                "error": d["error"],
                "output_brief": brief(d["output"]),
            }
        except Exception as exc:  # noqa: BLE001
            row = {"label": label, "node": node, "params": params,
                   "success": False, "error": f"{type(exc).__name__}: {exc}",
                   "output_brief": ""}
        rows.append(row)
        flag = "OK  " if row["success"] else "FAIL"
        print(f"[{flag}] {label}  (node={node})")
        if not row["success"]:
            print(f"        error: {row['error']}")

    out = Path(__file__).resolve().parent / "dryrun_chain_result_20260927.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")
    ok = sum(1 for r in rows if r["success"])
    print(f"\n== {ok}/{len(rows)} 节点干跑通过 -> {out}")
    return 0 if ok == len(rows) else 1


if __name__ == "__main__":
    raise SystemExit(main())
