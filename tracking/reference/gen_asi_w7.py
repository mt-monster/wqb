"""ASI w7 —— settings 差异扫描（攻 self-corr 的关键杠杆）。

## 根因（2026-09-29 实测平台 settings）

| alpha | universe | neut | decay | trunc | S | F | 金字塔 |
|---|---|---|---|---|---|---|---|
| 88jaV5lv | MINVOL1M | **SECTOR** | 12 | 0.08 | 2.35 | 1.11 | PV+SENT |
| LLNgdpw2 | MINVOL1M | **SECTOR** | 12 | 0.08 | 1.98 | 1.02 | PV+SENT |
| P02wbJAM | MINVOL1M | **SECTOR** | 12 | 0.08 | 2.30 | 1.43 | PV+SENT+OTHER |
| rKjY5vGj | **MINVOL10M** | **INDUSTRY** | 6 | 0.05 | 2.01 | 1.36 | RISK+MODEL |
| qMNMbeGj | MINVOL1M | **MARKET** | 4 | 0.08 | 1.72 | 1.16 | OTHER |

**关键**：我的 w1/w3 探针用的是 `MINVOL1M + SECTOR + decay12 + trunc0.08`
= **与 88jaV5lv 完全相同的配置** → self-corr 0.76~0.81（必然高）。

**交叉相关实证（低相关配置的存在性）**：
- `O081GNWY`（last30/SECTOR）vs `rKjY5vGj`（MINVOL10M/INDUSTRY） = **0.1325**
- `O081GNWY` vs `qMNMbeGj`（MARKET） = **-0.0215**
→ **换 settings 能有效降相关**（换配置 ≈ 换持仓分布 ≈ 换 PnL）。

## w7 扫描矩阵（挑未占用配置 × 最强腿）

**腿**（w1/w5 实测强度）：
- `last30` = mean_last_trade_price_return_30m_pre_close_2（**最强 S=3.03 / F=1.29**）
- `ask30`（S=2.22，self-corr 0.56）
- `last60`（S=2.17，self-corr 0.56）

**配置（避开 SECTOR+decay12）**：
1. `MINVOL1M + MARKET + decay4 + trunc0.08`   ← qMNMbeGj 配置（corr -0.02）
2. `MINVOL1M + INDUSTRY + decay12 + trunc0.08`
3. `MINVOL1M + SUBINDUSTRY + decay12 + trunc0.08`
4. `MINVOL10M + INDUSTRY + decay6 + trunc0.05` ← rKjY5vGj 配置（F=1.36）
5. `MINVOL10M + SECTOR + decay12 + trunc0.08`
6. `MINVOL1M + STATISTICAL + decay12 + trunc0.08`

**输出**：`exprs_asi_w7.json`（腿 × 固定内层 dec4，配置由 CLI 切换）。
"""
import json
import os

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                   "..", "ASI", "candidates", "exprs_asi_w7.json")

VOL_GATE = "rank(divide(mean_trade_volume_30m_pre_close_2, ts_mean(volume, 22))) > 0.5"
NEWS_GATE = "rank(ts_mean(normalized_news_article_count, 22)) > 0.3"
GATE = f"and({VOL_GATE}, {NEWS_GATE})"
EXIT = ("or(rank(divide(mean_trade_volume_30m_pre_close_2, ts_mean(volume, 22))) < 0.3, "
        "rank(ts_mean(normalized_news_article_count, 22)) < 0.2)")

LEGS = [
    ("last30", "mean_last_trade_price_return_30m_pre_close_2"),   # 最强 S=3.03 F=1.29
    ("ask30", "mean_ask_price_return_30m_pre_close_2"),           # S=2.22 corr 0.56
    ("bid30", "mean_bid_price_return_30m_pre_close_2"),           # S=2.19 corr 0.57
    ("last60", "mean_last_trade_price_return_60m_pre_close_2"),   # S=2.17 corr 0.56
]

exprs = []
seen = set()

for tag, fld in LEGS:
    # 内层 dec 4（w1 最强：S 3.03；对应 88jaV5lv 的内层 dec4 但外层 settings 将差异化）
    e = (f"trade_when({GATE}, "
         f"signed_power(subtract(0.5, group_rank(ts_decay_linear({fld}, 4), country)), 0.5), "
         f"{EXIT})")
    if e not in seen:
        seen.add(e)
        exprs.append([f"W7_d4_{tag}", e])
    # 内层 dec 11（w3/w5 甜点：T 更安全）
    e2 = (f"trade_when({GATE}, "
          f"signed_power(subtract(0.5, group_rank(ts_decay_linear({fld}, 11), country)), 0.5), "
          f"{EXIT})")
    if e2 not in seen:
        seen.add(e2)
        exprs.append([f"W7_d11_{tag}", e2])

os.makedirs(os.path.dirname(OUT), exist_ok=True)
with open(OUT, "w", encoding="utf-8") as f:
    json.dump(exprs, f, ensure_ascii=False, indent=1)

print(f"written {len(exprs)} exprs -> {os.path.abspath(OUT)}")
for lab, _ in exprs:
    print(" ", lab)
