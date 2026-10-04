# -*- coding: utf-8 -*-
"""_kor_d33_writeback.py — KOR s2_oth466_d33 复盘入库（一次性）。

结论（2026-10-04）：
  d33 用「已验证骨架 + 已验证资产侧分母 oth466_bs_assets_tot_q」，扫 8 个未试分子。
  结果：4 条过 S/F 闸（vR29LgEz/ZYAxpG80/xAbQxgLn/P0g6p9Rx），3 条过 2Y 闸；
  vR29LgEz 全闸通过（S1.94/F1.53/2Y2.51/SUB1.17）——**但 prod=0.7671 撞墙**。

根因：分子 oth466_is_consol_net_inc_q 与已 ACTIVE 的 0mrnWojG
      分子 oth466_is_net_inc_basic_q 经济含义同义（归属普通股股东净利）。
      ⇒ 换分母不能破墙，因为撞墙变量是【分子经济概念】而非分母。
"""
from __future__ import annotations

import json
import os
import sqlite3
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src"))

from wqb.db_conn import connect as _db_connect  # noqa: E402

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB = os.path.join(REPO, "data", "wqb.db")

WAVE = "s2_oth466_d33"
REGION = "KOR"
DATASET = "other466"

# alpha_id -> (分子, S, F, 2Y, SUB, 判定)
ROWS = {
    "vR29LgEz": ("oth466_is_consol_net_inc_q", 1.94, 1.53, 2.51, 1.17,
                 "全闸通过但 prod=0.7671 撞墙（分子与 0mrnWojG 同义）"),
    "ZYAxpG80": ("oth466_is_net_inc_basic_beft_xord_q", 1.86, 1.48, 1.95, 1.06,
                 "SUB 0.99 差 0.01（同族分子，注定撞 prod）"),
    "xAbQxgLn": ("oth466_is_net_inc_dil_q", 1.75, 1.33, 1.88, 0.99,
                 "SUB 0.99（同族分子）"),
    "P0g6p9Rx": ("oth466_is_oper_inc_q", 1.68, 1.27, 1.24, 1.37,
                 "2Y 1.24 不过闸；但分子概念【新】（营业利润）"),
    "omWvKObm": ("oth466_is_sales_q", 1.48, 1.04, 0.15, 0.97,
                 "2Y 0.15 崩（收入族与资产分母不匹配）"),
    "xAbQxgLg": ("oth466_is_gross_inc_q", 1.22, 0.73, 1.22, 0.88, "S/F 双不过"),
    "N1V6p9Ee": ("oth466_is_net_profit_12m_q", 0.65, 0.30, 1.07, 0.25, "死"),
    "qM0dAq22": ("oth466_is_revenue_q", 0.31, 0.09, -0.07, 0.13, "死"),
}


def main() -> int:
    conn = _db_connect(DB, timeout=30.0, row_factory=sqlite3.Row)
    cur = conn.cursor()

    # 1) registry_empirical：封 d33 结论为 campaign 层
    entry = {
        "wave": WAVE,
        "dataset": DATASET,
        "date": "2026-10-04",
        "verdict": "MIXED_NO_SUBMIT",
        "key_finding": (
            "换分母（bs_eq_tot_q → bs_assets_tot_q）不能破 prod 墙："
            "vR29LgEz 分子 consol_net_inc_q 与已 ACTIVE 0mrnWojG 的 net_inc_basic_q 同义，"
            "prod 0.7671 > 0.7。撞墙变量是【分子经济概念】，不是分母。"
        ),
        "evidence": {
            "vR29LgEz": "S1.94/F1.53/2Y2.51/SUB1.17 全闸过；prod=0.7671 BLOCKED",
            "bench_gJZ7AvZO": "同骨架同族已 ACTIVE，prod=0.6413",
            "bench_0mrnWojG": "分子近义，prod=0.6843",
        },
        "next_direction": (
            "同骨架其它分子已穷尽；下一步须换【经济概念】（非净利/收入类），"
            "或换分组轴/算子等价替换；或转向 other466 非 quantile 骨架。"
        ),
    }
    cur.execute(
        "INSERT INTO registry_empirical (region, layer, entry_id, family, payload, created_at, updated_at) "
        "VALUES (?,?,?,?,?,datetime('now'),datetime('now'))",
        (REGION, "campaign", f"KOR-OTH466-D33-{WAVE}",
         "other466 资产侧分母 × 净利族分子 quantile 包装——全闸可过但 prod 撞墙，换分母不破墙",
         json.dumps(entry, ensure_ascii=False)),
    )

    # 2) dead_end：给「净利族分子 + 同骨架」判死，防止重复挖
    dead = {
        "wave": WAVE,
        "dataset": DATASET,
        "dead_family": "other466 quantile(group_rank(ts_rank(group_rank(divide(F,F),F),N),F)) × 净利族分子",
        "reason": "同骨架已有 2 颗 ACTIVE（0mrnWojG/gJZ7AvZO）；净利族分子（consol_net_inc/net_inc_basic_beft_xord/net_inc_dil/net_inc_basic）互相同义 ⇒ prod 必撞 >0.7",
        "probed_molecules": list({v[0] for v in ROWS.values()}),
        "date": "2026-10-04",
    }
    cur.execute(
        "INSERT INTO registry_empirical (region, layer, entry_id, family, payload, dead_at, created_at, updated_at) "
        "VALUES (?,?,?,?,?,datetime('now'),datetime('now'),datetime('now'))",
        (REGION, "dead_end", f"KOR-OTH466-QUANTILE-NETINC-FAMILY-DEAD-20261004",
         "other466 quantile 骨架 × 净利族分子（prod 墙）",
         json.dumps(dead, ensure_ascii=False)),
    )

    # 3) wave_results：本波复盘
    findings = {
        "probed": len(ROWS),
        "above_is_gate": 4,
        "above_2y_gate": 3,
        "all_gate_pass": 1,
        "prod_tested": 1,
        "prod_blocked": 1,
        "conclusion": "换分母不破 prod 墙；同骨架净利族已尽",
    }
    cands = [
        {"alpha_id": a, "molecule": v[0], "sharpe": v[1], "fitness": v[2],
         "two_year": v[3], "sub_universe": v[4], "verdict": v[5]}
        for a, v in ROWS.items()
    ]
    cur.execute(
        "INSERT INTO wave_results (region, wave_number, focus, context, key_findings, candidates, batches, verdict, status, created_at, updated_at) "
        "VALUES (?,?,?,?,?,?,?,?,?,datetime('now'),datetime('now'))",
        (REGION, WAVE, f"{DATASET} 资产侧分母 × 净利族分子扫（probe 批）",
         "已验证骨架 quantile(group_rank(ts_rank(group_rank(divide(NUM,DEN),industry),1008),market))，固定 DEN=oth466_bs_assets_tot_q",
         json.dumps(findings, ensure_ascii=False),
         json.dumps(cands, ensure_ascii=False),
         json.dumps({"multisim": "3bFsMocQn4CT9p8M0PapTB1", "n": 8, "batch_type": "probe"}, ensure_ascii=False),
         "MIXED_NO_SUBMIT", "completed"),
    )

    conn.commit()
    print("[ok] registry_empirical +2（campaign/dead_end）")
    print("[ok] wave_results +1")
    for r in cur.execute("SELECT id, layer, entry_id FROM registry_empirical WHERE region='KOR' ORDER BY id DESC LIMIT 3"):
        print("   ", dict(r))
    conn.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
