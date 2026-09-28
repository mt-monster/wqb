#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""_kor_s6_writeback.py — KOR 波次 S6 复盘回写（registry_empirical + ledger s6_verdict）。

wqb-db MCP 未连接时的降级路径，直接走 wqb.store 规范写库。
用法: python tools/_kor_s6_writeback.py
"""
from __future__ import annotations

import json
import sys
from datetime import datetime
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "src"))

from wqb.store import CampaignStore  # noqa: E402

REGION = "KOR"
WAVE = "s2_fundamental17_d1"
NOW = datetime.now().isoformat(timespec="seconds")

# ── registry_empirical：本波经验（dead_end + 保留线索）──
ENTRIES = [
    {
        "entry_id": "KOR-FND17-EV2EBITDA-DIVERGENCE-CEILING",
        "layer": "dead_end",
        "family": "fundamental17 EV/EBITDA 水平+趋势背离（group_rank/ts_zscore 族）",
        "payload": {
            "id": "KOR-FND17-EV2EBITDA-DIVERGENCE-CEILING",
            "dataset": "fundamental17",
            "wave": WAVE,
            "verdict": "SIGNAL_CEILING",
            "n": 168,
            "best_sharpe": 1.23,
            "best_alpha": "A1N8q1vR",
            "best_expr": "group_rank(reverse(divide(ts_delta(enterprise_value_to_ebitda_current, 66), add(abs(ts_mean(enterprise_value_to_ebitda_current, 252)), 0.05))), sector)",
            "best_two_year": 1.99,
            "reason": "fundamental17 原始会计字段族天花板 S=1.23/F=0.89（差 Mode B 资格线 S1.25/F0.8 仅 0.02），168 条全测 0 达标；|S|>=0.5 有 48 条但主墙恒为 SHARPE（IS 信号强度不足），非 prod/2Y 墙。",
            "rule": "fundamental17 EV/EBITDA 水平+趋势族不再投主攻槽位（S 天花板 1.23 < 1.58 提交线）；唯一残值 = A1N8q1vR（2Y=1.99 显著高于 IS 1.23）可作**慢腿**候选，配短周期低相关快腿走组合腿（KOR-COMBO-LEG-CONSTRAINT）。",
            "anti_patterns": [
                "ts_zscore(EV/EBITDA, N) 裸式：22/66/252 三个窗口全文 S=-1.12~-1.23（**方向为负且同幅**，即估值水平反转，非偏离度信号）",
                "用 raw 会计水平字段直接当信号（本波 176 条中 172 条曾被 GEM 用到货币代码/汇率换算 → 语义废产物，见闸 SEM）",
            ],
            "pyramid": "KOR/D1/FUNDAMENTAL（本波 168 条全部 MATCHES_PYRAMID pass，仍未点亮，差 2 颗）",
            "timestamp": NOW,
        },
    },
    {
        "entry_id": "KOR-FND17-RAW-ACCOUNTING-WEAK",
        "layer": "dead_end",
        "family": "signal_family: 原始会计比率字段族（margins/turnover/leverage/dividend 水平与差分）",
        "payload": {
            "id": "KOR-FND17-RAW-ACCOUNTING-WEAK",
            "dataset": "fundamental17",
            "wave": WAVE,
            "reason": "原始会计比率（gross/operating/net margin、asset/inventory/receivable turnover、debt-to-*、payout ratio）在 KOR/TOP600/D1/STATISTICAL 下单腿与差分结构均无稳定正信号；与 KOR 既有 fnd86/fnd89/fnd93/fnd94 全弱结论同向。",
            "rule": "KOR 原始会计字段族（fnd17/fnd86/fnd89/fnd93/fnd94）不再作为主信号来源；如需基本面暴露，走 analyst 预期修正（analyst10 pred_surps prod 0.60 干净）或组合腿辅助。",
            "evidence": "168 条回测（含 11 个经济大类、12 个骨架）best S=1.23，无一跨 1.58；类别分布 profitability/valuation/cash_quality/size_level 全覆盖仍不出货。",
            "timestamp": NOW,
        },
    },
]

# ── ledger：s6 verdict + 设置先验实证 ──
LEDGER = {
    f"s6_verdict_{WAVE}": {
        "region": REGION,
        "wave": WAVE,
        "dataset": "fundamental17",
        "verdict": "PARTIAL",
        "n_backtested": 168,
        "candidates": 0,
        "combo_candidates": 1,
        "near": 1,
        "best_sharpe": 1.23,
        "best_two_year": 1.99,
        "best_alpha": "A1N8q1vR",
        "main_wall": "SHARPE",
        "recorded_at": NOW,
        "note": "S4 自动写入 wave_results(PARTIAL/closed) + near_pool(+1) + salvage_pool(141)。本键为 SOP 步 9 要求的显式 s6 verdict 台账。",
    },
    f"s6_fnd17_settings_evidence": {
        "settings_used": {"universe": "TOP600", "delay": 1, "neutralization": "STATISTICAL",
                          "decay": 4, "truncation": 0.08},
        "settings_prior_auto_check": "pipeline 自动比对 KOR region_kb.gate_priors：decay=4 lift×1.0、STATISTICAL lift×1.0 均未达 min_lift=2.0 → 保持 settings.json 原值（=实测最优先验值，无冲突）",
        "neutralization_empirical": "989 条库存实测 STATISTICAL 14.63%(n=205) 最优 / SUBINDUSTRY 仅 1.64%(n=61) 全场最差。用户指令中的『KOR 实证 SUBINDUSTRY 最优』与实测相反，本波按 STATISTICAL 执行。",
        "recorded_at": NOW,
    },
}


def main():
    store = CampaignStore(str(REPO / "data" / "wqb.db"))
    try:
        cur = store.connection.cursor()
        ins = 0
        for e in ENTRIES:
            cur.execute(
                """INSERT INTO registry_empirical(region, layer, entry_id, family, payload, dead_at, created_at, updated_at)
                   SELECT ?,?,?,?,?,?,?,?
                   WHERE NOT EXISTS (SELECT 1 FROM registry_empirical WHERE region=? AND entry_id=?)""",
                (REGION, e["layer"], e["entry_id"], e.get("family"),
                 json.dumps(e["payload"], ensure_ascii=False), NOW, NOW, NOW, REGION, e["entry_id"]))
            ins += cur.rowcount
        store.connection.commit()
        print(f"[registry] 新增 {ins} 条 registry_empirical")
        for k, v in LEDGER.items():
            store.upsert_ledger(REGION, k, v)
            print(f"[ledger] {REGION}/{k}")
    finally:
        store.close()


if __name__ == "__main__":
    main()
