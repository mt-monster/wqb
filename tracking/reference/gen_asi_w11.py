"""ASI w11 —— 攻「处女地」开盘段（`*_post_open`）信号，换取真正的低相关。

## 为什么（关键发现）

ASI `intraday_pv_feats` 的 **`*_post_open` 族几乎完全无人使用**（0~1 users / 0~1 alphas）：

| 字段 | cov | users | alphas |
|---|---|---|---|
| `mean_ask_price_return_30m_post_open` | 0.987 | **0** | **0** |
| `mean_ask_price_return_60m_post_open` | 0.987 | 1 | 1 |
| `mean_bid_price_return_30m_post_open` | 0.987 | 1 | 1 |
| `mean_bid_price_return_60m_post_open` | 0.987 | **0** | **0** |
| `mean_high_price_return_30m_post_open` | 0.987 | **0** | **0** |
| `mean_high_price_return_60m_post_open` | 0.987 | **0** | **0** |

**经济含义**：`*_pre_close_*` 衡量**尾盘**价格变动（收盘竞价压力 → 隔日反转）；
`*_post_open` 衡量**开盘后 30/60 分钟**的价格变动（隔夜信息消化 → 开盘过度反应反转）。
**两者是不同 session segment → 不同信号概念 → 天然低相关。**

## 已确立的相关度约束（本轮实测，ASI/MINVOL1M）

| 变化 | 对 self-corr 的效果 |
|---|---|
| 换腿 last30→last60 | 0.81 → 0.57 ✓ 最强 |
| 换中性化 SECTOR→MARKET | 0.81 → 0.69 ✓ 中等 |
| 门控 and → news-only | → 0.65 ✓ 但 F/ladder/robust 4 项 FAIL |
| **门控 and → vol-only** | **0.8154 ✗ 反而恶化**（宽门控趋近基础信号） |
| 内层窗 d4→d11 | 反向恶化（0.69 → 0.77） |

→ 已提交 `1YZYj5QQ`(last60/d4/SECTOR) 与 `E5R56EbR`(last30/d4/MARKET)。
→ **第三颗必须换到不同 session segment**（尾盘族已被自身占满，self-corr 下限 ~0.65）。

## w11 设计（只换信号腿，其余沿用已验证配方）

- 信号腿：6 条 post_open 收益率（ask/bid/high × 30m/60m）+ 2 条带符号反转对照
- 门控 A（已证）：`and(vol_share>0.5, news>0.3)` → exit `or(vol_share<0.3, news<0.2)`
- 门控 B（替代）：`and(rel_daily_volume>0.5, news>0.3)` → 开盘段更自然的流动性门
- 几何：`signed_power(subtract(0.5, group_rank(ts_decay_linear(X, 4), country)), 0.5)`（沿用）
- settings：`MINVOL1M + SECTOR + decay12 + trunc0.08`（沿用）

合规：单信号腿 + 门控条件，无混信号。
"""
import json
import os

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                   "..", "ASI", "candidates", "exprs_asi_w11.json")

# ---- 门控 A（已证配方）----
VOL_SHARE = "rank(divide(mean_trade_volume_30m_pre_close_2, ts_mean(volume, 22)))"
NEWS = "rank(ts_mean(normalized_news_article_count, 22))"
GATE_A = f"and({VOL_SHARE} > 0.5, {NEWS} > 0.3)"
EXIT_A = f"or({VOL_SHARE} < 0.3, {NEWS} < 0.2)"

# ---- 门控 B（相对日成交量的流动性门）----
RELVOL = "rank(divide(volume, ts_mean(volume, 22)))"
GATE_B = f"and({RELVOL} > 0.5, {NEWS} > 0.3)"
EXIT_B = f"or({RELVOL} < 0.3, {NEWS} < 0.2)"

# ---- 处女地信号腿（post_open）----
LEGS = [
    ("ask30po", "mean_ask_price_return_30m_post_open"),
    ("ask60po", "mean_ask_price_return_60m_post_open"),
    ("bid30po", "mean_bid_price_return_30m_post_open"),
    ("bid60po", "mean_bid_price_return_60m_post_open"),
    ("high30po", "mean_high_price_return_30m_post_open"),
    ("high60po", "mean_high_price_return_60m_post_open"),
]

exprs = []
seen = set()


def add(lab, e):
    if e not in seen:
        seen.add(e)
        exprs.append([lab, e])


def core(x, dec=4, group="country"):
    return f"signed_power(subtract(0.5, group_rank(ts_decay_linear({x}, {dec}), {group})), 0.5)"


# 1-6：门控 A + 6 条 post_open 腿（反转方向，与尾盘族同号）
for tag, fld in LEGS:
    add(f"W11_A_{tag}", f"trade_when({GATE_A}, {core(fld)}, {EXIT_A})")

# 7-8：门控 B + 最强两条（换流动性门，进一步差异化）
for tag, fld in LEGS[:2]:
    add(f"W11_B_{tag}", f"trade_when({GATE_B}, {core(fld)}, {EXIT_B})")

# 9-10：正向（动量）对照 —— 开盘段可能是动量而非反转，用符号确认方向
for tag, fld in LEGS[:2]:
    add(f"W11_A_mom_{tag}",
        f"trade_when({GATE_A}, "
        f"signed_power(subtract(group_rank(ts_decay_linear({fld}, 4), country), 0.5), 0.5), {EXIT_A})")

os.makedirs(os.path.dirname(OUT), exist_ok=True)
with open(OUT, "w", encoding="utf-8") as f:
    json.dump(exprs, f, ensure_ascii=False, indent=1)

print(f"written {len(exprs)} exprs -> {os.path.abspath(OUT)}")
for lab, _ in exprs:
    print(" ", lab)
