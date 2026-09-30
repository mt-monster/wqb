"""ASI w15 —— 尾盘段「全腿矩阵」扫荡（每条新腿 ≈ 一颗低自相关新 alpha）。

## 核心洞察（本轮实证）

**相关性由「腿」主导，不由中性化/门控主导**：
- 同腿同窗换中性化：self-corr **0.95~0.98**（npPprGgq 0.9535 / akxkglX1 0.9813）
- **换腿**：self-corr **0.57~0.66**（bid30 0.6624 / ask30 0.6630 / bid30_d11 0.5723）

→ **腿 = 正交性来源**。`intraday_pv_feats` 尾盘段共 12 条收益率腿，已用 2 条（last30/last60）。
→ 剩余 10 条腿每一条都可能产出一颗低自相关 alpha。

## 待测腿（全部 pre-close_2 段，coverage 0.9926）

| 腿 | 字段 | users | 说明 |
|---|---|---|---|
| ask60 | `mean_ask_price_return_60m_pre_close_2` | 4 | 卖价收益 |
| bid60 | `mean_bid_price_return_60m_pre_close_2` | 1 | 买价收益 |
| high30 | `mean_high_price_return_30m_pre_close_2` | 4 | 最高价收益 |
| high60 | `mean_high_price_return_60m_pre_close` | 2 | 最高价收益（注意无 `_2` 后缀） |
| **vwap30** | `mean_vwap_return_30m_pre_close_2` | 9 | **VWAP 收益** |
| **vwap60** | `mean_vwap_return_60m_pre_close_2` | 4 | **VWAP 收益** |
| **low30** | `mean_low_price_return_30m_pre_close_2` | 1 | **最低价收益** |
| **low60** | `mean_low_price_return_60m_pre_close_2` | **0** | **最低价收益（处女）** |

## 门控：双档并跑（w14 将给出 vol-only vs and 的优劣，此处两档都备）

- `vol`：`vol_share > 0.5` / exit `< 0.3`（w10/w14 实证提 S 幅度最大）
- `and`：`and(vol_share>0.5, news>0.3)` / exit `or(<0.3, <0.2)`（原配方）

内层窗 d5（bid30 的 F 峰值：d4 0.86 / **d5 0.98** / d6 0.98）。

合规：单信号腿 + 门控条件，非混信号。
"""
import json
import os

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                   "..", "ASI", "candidates", "exprs_asi_w15.json")

VOL = "rank(divide(mean_trade_volume_30m_pre_close_2, ts_mean(volume, 22)))"
NEWS = "rank(ts_mean(normalized_news_article_count, 22))"
GATE_VOL = f"{VOL} > 0.5"
EXIT_VOL = f"{VOL} < 0.3"
GATE_AND = f"and({VOL} > 0.5, {NEWS} > 0.3)"
EXIT_AND = f"or({VOL} < 0.3, {NEWS} < 0.2)"

LEGS = [
    ("ask60", "mean_ask_price_return_60m_pre_close_2"),
    ("bid60", "mean_bid_price_return_60m_pre_close_2"),
    ("high30", "mean_high_price_return_30m_pre_close_2"),
    ("high60", "mean_high_price_return_60m_pre_close"),
    ("vwap30", "mean_vwap_return_30m_pre_close_2"),
    ("vwap60", "mean_vwap_return_60m_pre_close_2"),
    ("low30", "mean_low_price_return_30m_pre_close_2"),
    ("low60", "mean_low_price_return_60m_pre_close_2"),
]

exprs = []
seen = set()


def add(lab, e):
    if e not in seen:
        seen.add(e)
        exprs.append([lab, e])


def core(x, dec=5, group="country"):
    return f"signed_power(subtract(0.5, group_rank(ts_decay_linear({x}, {dec}), {group})), 0.5)"


for tag, fld in LEGS:
    c = core(fld, 5)
    add(f"W15_vol_{tag}_d5", f"trade_when({GATE_VOL}, {c}, {EXIT_VOL})")
    add(f"W15_and_{tag}_d5", f"trade_when({GATE_AND}, {c}, {EXIT_AND})")

os.makedirs(os.path.dirname(OUT), exist_ok=True)
with open(OUT, "w", encoding="utf-8") as f:
    json.dump(exprs, f, ensure_ascii=False, indent=1)

print(f"written {len(exprs)} exprs -> {os.path.abspath(OUT)}")
for lab, _ in exprs:
    print(" ", lab)
