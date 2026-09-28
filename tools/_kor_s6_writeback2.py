#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""_kor_s6_writeback2.py — A/B 双线四波 S6 回写（2026-09-28 下午）。

覆盖 wave: kor_w185_modeb / kor_w186_slowfast / kor_w187_spread / s2_risk70_d1
用法: python tools/_kor_s6_writeback2.py
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
NOW = datetime.now().isoformat(timespec="seconds")

ENTRIES = [
    {
        "entry_id": "KOR-FND17-SLOWFAST-SPREAD-CEILING",
        "layer": "dead_end",
        "family": "fundamental17 慢(毛利率水平)×快(EV/EBITDA 趋势)价差结构",
        "payload": {
            "id": "KOR-FND17-SLOWFAST-SPREAD-CEILING",
            "dataset": "fundamental17",
            "waves": ["kor_w185_modeb", "kor_w186_slowfast", "kor_w187_spread"],
            "verdict": "SIGNAL_CEILING_CONFIRMED",
            "n": 25,
            "progression": {
                "base_A1N8q1vR": "S=1.23 / F=0.89 / 2Y=1.33",
                "slowfast_价差_XgbAk910": "S=1.30 / F=0.94 / 2Y=1.87（核心突破：结构交互同时抬三项）",
                "refine_QPbpQLqg": "S=1.30 / F=0.93 / 2Y=1.79（换 subindustry 轴无增益）",
            },
            "reason": "慢×快价差结构（subtract(group_rank(慢腿), group_rank(快腿))）在 KOR/TOP600/D1/STATISTICAL 下稳定把 S 1.23→1.30、F 0.89→0.94、2Y 1.33→1.87，但 **S 天花板锁在 ~1.30**，跨不过 Mode B 资格线 1.25→提交线 1.58。二轮精调 8 条（窗口 22/66/252、轴 industry/subindustry、ts_decay 平滑、去掉离散度分母）全部落在 S=1.11–1.30，无一突破。",
            "rule": "KOR fundamental17 原始会计字段族**判死**（含结构交互路线）：不再投任何主攻槽位。累计已测 176(概念优先) + 10(Mode B) + 8(慢×快) + 8(价差精调) = **202 条 / >10 种结构**，符合『同一想法 >10 种结构仍不过则记 dead_end』。",
            "salvage_lead": {
                "慢腿": "group_rank(ts_mean(gross_margin_trailing_twelve_months, 66), industry) → S=0.75 / 2Y=1.99 / turn=0.062（同族 22/66/252 四窗口 2Y 全 ≥1.58）",
                "用途": "作跨数据集组合的慢腿（boost_2y + boost_tvr 双维度），配短周期低相关快腿",
                "可复用性": "毛利率水平族是全波唯一 2Y 稳定 ≥1.58 的结构，与 EV/EBITDA 趋势族（S 高 2Y 低）天然互补——本波价差组合已验证互补性成立",
            },
            "anti_patterns": [
                "ts_zscore(EV/EBITDA, N) 裸式 22/66/252：S=-1.12~-1.23 同幅反向（估值水平反转，非偏离度信号）",
                "trend ÷ level-dispersion（ts_zscore 做分母）作快腿：S=-1.44，符号完全反了",
                "ts_rank(L1, 252) 时序分位替换水平：S=-0.87，破坏信号",
            ],
            "timestamp": NOW,
        },
    },
    {
        "entry_id": "KOR-RISK70-FACTOR-LOADING-NO-ALPHA",
        "layer": "dead_end",
        "family": "risk70 MFM2 风格因子载荷（momentum/ltrevrsl/btop/resvol/profit/growth/leverage/earnvar/season/beta/invsqlty/anlystsn/shortint/dsrt/srisk/market）",
        "payload": {
            "id": "KOR-RISK70-FACTOR-LOADING-NO-ALPHA",
            "dataset": "risk70",
            "wave": "s2_risk70_d1",
            "verdict": "NO_SIGNAL",
            "n": 114,
            "best_sharpe": 0.87,
            "best_fitness": 0.67,
            "candidates": 0,
            "near": 0,
            "reason": "risk70 是风险模型**因子载荷**数据集：载荷本身就是模型要中性化掉的暴露，不是超额收益来源。114 条（闸 SEM 从 207 剔到 118、实回测 114）best S=0.87，0 达标 0 near。",
            "rule": "KOR risk70 判死，不再投槽位。**推广规律（durable）**：任何『风险模型因子载荷』类数据集（字段描述含 Factor Loading / Exposure）在 KOR 小宇宙内不宜作主信号；若要用，只能作条件/分组/中性化辅助腿。",
            "note": "与既有 KOR-RISK71-RESIDUAL-REVERSAL-2Y-DEAD（risk71 MFM2 residual reversal 2Y 死）同源同向：MFM2 系（risk70/risk71）作信号在 KOR 均不出货。",
            "report_note": "本次同时验证：闸 SEM + 语义干净字段池把 GEM 池内命中率从 3.2%→87.4%、行业哑变量泄漏从 49.4%→4.8%、骨架数从 12→91——**池约束是 GEM 产物质量第一杠杆**（与结果无关，属方法学收益）。",
            "timestamp": NOW,
        },
    },
]

LEDGER = {
    "s6_verdict_kor_w185_modeb": {"region": REGION, "wave": "kor_w185_modeb", "dataset": "fundamental17",
                                  "verdict": "PARTIAL", "n_backtested": 9, "candidates": 0, "near": 2,
                                  "best_sharpe": 1.23, "best_two_year": 1.52, "main_wall": "SHARPE",
                                  "note": "Mode B 结构交互 10 变体；最好 mLmWxvLp S=1.22/2Y=1.52。天花板未破。", "recorded_at": NOW},
    "s6_verdict_kor_w186_slowfast": {"region": REGION, "wave": "kor_w186_slowfast", "dataset": "fundamental17",
                                     "verdict": "PARTIAL", "n_backtested": 8, "candidates": 0, "near": 2,
                                     "best_sharpe": 1.3, "best_fitness": 0.94, "best_two_year": 1.87,
                                     "best_alpha": "XgbAk910", "main_wall": "SHARPE",
                                     "note": "**关键突破**：慢(毛利率水平)×快(EV/EBITDA 趋势) 价差结构 → S 1.23→1.30 / F 0.89→0.94 / 2Y 1.33→1.87。结构交互同时抬三项，验证 SLOW×FAST 配方在 fundamental17 内成立；但 S 仍 <1.58。",
                                     "recorded_at": NOW},
    "s6_verdict_kor_w187_spread": {"region": REGION, "wave": "kor_w187_spread", "dataset": "fundamental17",
                                   "verdict": "PARTIAL", "n_backtested": 8, "candidates": 0, "near": 6,
                                   "best_sharpe": 1.3, "best_two_year": 1.88, "main_wall": "SHARPE",
                                   "note": "价差结构精调 8 条：near 率 6/8，全部聚在 S=1.11–1.30 / 2Y=1.56–1.88。**天花板锁定 ~1.30**，判死 fundamental17。",
                                   "recorded_at": NOW},
    "s6_verdict_s2_risk70_d1": {"region": REGION, "wave": "s2_risk70_d1", "dataset": "risk70",
                                "verdict": "FAIL", "n_backtested": 114, "candidates": 0, "near": 0,
                                "best_sharpe": 0.87, "best_fitness": 0.67, "main_wall": "SHARPE",
                                "note": "risk70（风险模型因子载荷）全灭。池约束方法学收益记录见 registry KOR-RISK70-FACTOR-LOADING-NO-ALPHA。",
                                "recorded_at": NOW},
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
