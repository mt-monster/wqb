"""ASI RA 探针生成器（w6）—— 突破 F≥1.0，同时保住 self-corr < 0.7 余量。

## 起点（w5 首次出现"可提交希望"）

| 候选 | alpha | S | F | T | self-corr max | 卡点 |
|---|---|---|---|---|---|---|
| `W5_spdec11_ask30` | omW1apxE | 2.22 | **0.92** | 0.4016 | **0.5598 ✓** | F 差 0.08 |
| `W5_spdec11_bid30` | QPK1oRxw | 2.19 | **0.90** | 0.4016 | **0.5723 ✓** | F 差 0.10 |
| `W5_spdec11_last60` | N1VX2r3p | 2.17 | **0.91** | 0.3887 | **0.5591 ✓** | F 差 0.09 |

**腿都是「未被占用的新腿」**（ask30 = `mean_ask_price_return_30m_pre_close_2`、
bid30 = `mean_bid_price_return_30m_pre_close_2`、last60 = `mean_last_trade_price_return_60m_pre_close_2`）。
对比：被占用的 `last30` 在 w3 下 self-corr = 0.7603（FAIL）。

## 为什么 F 差一口气（数学）

`F ≈ S × sqrt(|ret| / max(T, 0.125)) × 常数`。
w3 `0mrbYmp6`（last30/dec11）：S=2.71 → F=1.23。
w5 `omW1apxE`（ask30/dec11）：S=2.22 → F=0.92。
→ **差在 S（2.71 vs 2.22）**。ask30 腿的收益率幅度天然小于 last30。

## w6 策略：提 S 的三条合规路径（同时监控 self-corr 不越 0.7）

### A. decay 精扫（含向更短方向）—— S 随 decay 减而升
w3 已知 last30 的 S(dec9)=2.74 → S(dec11)=2.71 → S(dec13)=2.56（S 随 decay 升而降）。
w5 只测了 dec11。**ask30 腿可以试 dec 5/7/9 提 S**，同时 T 会升 → 需卡在 T<0.4。
→ dec 7/9 是重点（S 升 + T 可能仍在 0.4 附近）。

### B. 减一层近似（去掉 `subtract(0.5, ...)` 的常数平移等价变换）
`subtract(0.5, group_rank(x))` 与 `-group_rank(x)` 是**仿射等价**（只差常数），
但 `signed_power(·, 0.5)` 对负数不敏感 → 二者数值不同。
**`signed_power(-group_rank(...), 0.5)`** 或 **`-signed_power(group_rank(...), 0.5)`** 是不同几何。

### C. 加 `ts_rank` 外层（提 S 的稳健化，w3 outer* 变体曾达 S=2.73）
w3 的 `W3_outer4_last30`（外层 ts_decay_linear 4）S=2.73 vs dec4 的 3.03 → 外平滑略降 S。
但 **外层 `ts_rank`** 未试（不同几何）。

### D. 合并两条未占用腿的"和/差"（⚠ 须合规自检）
memory §0 允许 `subtract(rank(A), rank(B))` **视作单一价差信号**（须有经济含义）。
ask/bid 价差天然有含义（**买卖价差 = 流动性/做市压力**）→
  `signed_power(subtract(0.5, group_rank(ts_decay_linear(subtract(mean_ask_price_return_30m_pre_close_2, mean_bid_price_return_30m_pre_close_2), D), country)), 0.5)`
这是**单一条价差信号**（不是两条独立腿相加）→ 合规。

### E. 换中性化轴 B（sector/industry 在 w5 降 S 到 1.3）→ 不用；但 settings decay 可调
settings 层 decay（探针默认 12）升到 20/30 可提 F（降 T）→ **零表达式成本的调节杆**。
"""
import json
import os

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                   "..", "ASI", "candidates", "exprs_asi_w6.json")

VOL_GATE = "rank(divide(mean_trade_volume_30m_pre_close_2, ts_mean(volume, 22))) > 0.5"
NEWS_GATE = "rank(ts_mean(normalized_news_article_count, 22)) > 0.3"
GATE = f"and({VOL_GATE}, {NEWS_GATE})"
EXIT = ("or(rank(divide(mean_trade_volume_30m_pre_close_2, ts_mean(volume, 22))) < 0.3, "
        "rank(ts_mean(normalized_news_article_count, 22)) < 0.2)")

ASK30 = "mean_ask_price_return_30m_pre_close_2"
BID30 = "mean_bid_price_return_30m_pre_close_2"
LAST60 = "mean_last_trade_price_return_60m_pre_close_2"

exprs = []
seen = set()


def add(lab, e):
    if e not in seen:
        seen.add(e)
        exprs.append([lab, e])


def wrap(inner):
    return f"trade_when({GATE}, {inner}, {EXIT})"


def sp(x, group, dec):
    return f"signed_power(subtract(0.5, group_rank(ts_decay_linear({x}, {dec}), {group})), 0.5)"


# ============ A. decay 精扫（向更短方向提 S） ============
for tag, fld in (("ask30", ASK30), ("bid30", BID30), ("last60", LAST60)):
    for dec in (5, 7, 9):
        add(f"W6_a_dec{dec}_{tag}", wrap(sp(fld, 'country', dec)))

# ============ B. 等价变体几何（去 0.5 平移 / 移负号） ============
for tag, fld in (("ask30", ASK30), ("bid30", BID30)):
    add(f"W6_b_negr_{tag}",
        wrap(f"signed_power(-group_rank(ts_decay_linear({fld}, 11), country), 0.5)"))
    add(f"W6_b_negsp_{tag}",
        wrap(f"-signed_power(group_rank(ts_decay_linear({fld}, 11), country), 0.5)"))
    add(f"W6_b_rank_{tag}",
        wrap(f"subtract(0.5, group_rank(ts_decay_linear({fld}, 11), country))"))

# ============ C. 外层 ts_rank（新几何） ============
for tag, fld in (("ask30", ASK30), ("bid30", BID30)):
    add(f"W6_c_outrank_{tag}",
        wrap(f"-ts_rank(ts_decay_linear({fld}, 11), 126)"))
    add(f"W6_c_outrank252_{tag}",
        wrap(f"-ts_rank(ts_decay_linear({fld}, 11), 252)"))

# ============ D. ask-bid 价差（单一条价差信号，合规） ============
for dec in (5, 11):
    add(f"W6_d_spread_dec{dec}",
        wrap(f"signed_power(subtract(0.5, group_rank(ts_decay_linear("
             f"subtract({ASK30}, {BID30}), {dec}), country)), 0.5)"))
# last60 与 last30 的期限价差（经济含义：日内动量加速度）
add("W6_d_term_spread",
    wrap(f"signed_power(subtract(0.5, group_rank(ts_decay_linear("
         f"subtract({LAST60}, mean_last_trade_price_return_30m_pre_close_2), 11), country)), 0.5)"))

os.makedirs(os.path.dirname(OUT), exist_ok=True)
with open(OUT, "w", encoding="utf-8") as f:
    json.dump(exprs, f, ensure_ascii=False, indent=1)

print(f"written {len(exprs)} exprs -> {os.path.abspath(OUT)}")
for lab, _ in exprs:
    print(" ", lab)
