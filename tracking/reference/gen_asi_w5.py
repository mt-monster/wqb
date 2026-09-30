"""ASI RA 探针生成器（w5）—— 双目标：① 提升 w4 corr 家族强度；② 找未被使用的收益率腿。

## 已确证的诊断（w3 × w4）

| 家族 | S | F | T | self-corr |
|---|---|---|---|---|
| w3 `mean_last_trade_price_return_30m_pre_close_2` | 2.71 | **1.23** | 0.387 | **0.760 ✗** |
| w4 `corr_last_trade_price_with_volume` | 1.59 | 0.61 | 0.400 | **0.237 ✓** |
| w4 `corr_high_price_with_volume` | 1.58 | 0.61 | 0.402 | **0.209 ✓** |
| w4 `corr_vwap_with_volume` | 1.34 | 0.48 | 0.400 | — |

→ **强度与相关性成反比**：`corr_*` 家族正交（self 0.21~0.24，余量巨大）但 F 仅 0.5~0.6（闸 1.0）。
→ 已占用（不可用）：`mean_last_trade_price_return_30m_pre_close_2` + country + decay12
   （被 `88jaV5lv` 0.7603 / `LLNgdpw2` 0.6115 占据）。

## w5 五条路线

### 路线 1：corr 家族换"点位/窗口"版本（w4 只用了 "daily 全区间"聚合）
`intraday_pv_feats` 里 corr 家族还有 **last_half / first_half / last_quarter 时段切片版**，
w4 全部没试。不同时段的价量协同性 = 不同信号 → 可能更强且仍正交。
  - `corr_volume_with_bid_price_first_half` / `..._last_half`
  - `corr_bid_with_ask_price_first_half` / `..._last_half`
  - `corr_volume_with_last_price_last_half`（新字段，用户 2）
  - `corr_interval_vwap_with_interval_high`（用户 4）

### 路线 2：corr 家族做时序化（ts_delta / ts_mean 差分 = 变化率，非水平值）
水平值（level）弱，但**变化**（delta）常强。w4 全是 level。
  - `ts_delta(corr_*, 22)` / `ts_zscore(corr_*, 252)`

### 路线 3：未占用的收益率腿（同为 intraday_pv_feats，但字段不同）
  - `mean_last_trade_price_return_60m_pre_close_2`（w1 未测 60m 的 last）
  - `mean_high_price_return_30m_pre_close_2` / `..._60m_pre_close`
  - `last_trade_price_last_interval`（**点位**而非收益率）

### 路线 4：TS 时序反转几何（换算子几何，天然低相关于横截面 rank）
  - `-ts_rank(mean_*_return_30m_pre_close_2, 252)`：**时序**反转而非横截面
  - `-ts_zscore(mean_*_return_30m_pre_close_2, 252)`

### 路线 5：换中性化轴（sector / industry / subindustry / market）到收益率腿
  已实证（[W1] country 最强），但换轴可降相关 —— 且 w3 从未试过 last30 的非 country 轴。
  - `signed_power(subtract(0.5, group_rank(..., sector|industry|subindustry|market)), 0.5)`

合规：全部单信号腿 + 新闻量门控，无 add 混腿。
"""
import json
import os

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                   "..", "ASI", "candidates", "exprs_asi_w5.json")

VOL_GATE = "rank(divide(mean_trade_volume_30m_pre_close_2, ts_mean(volume, 22))) > 0.5"
NEWS_GATE = "rank(ts_mean(normalized_news_article_count, 22)) > 0.3"
GATE = f"and({VOL_GATE}, {NEWS_GATE})"
EXIT = ("or(rank(divide(mean_trade_volume_30m_pre_close_2, ts_mean(volume, 22))) < 0.3, "
        "rank(ts_mean(normalized_news_article_count, 22)) < 0.2)")

LAST30 = "mean_last_trade_price_return_30m_pre_close_2"
LAST60 = "mean_last_trade_price_return_60m_pre_close_2"
HIGH30R = "mean_high_price_return_30m_pre_close_2"
ASK30R = "mean_ask_price_return_30m_pre_close_2"
BID30R = "mean_bid_price_return_30m_pre_close_2"

exprs = []
seen = set()


def add(lab, e):
    if e not in seen:
        seen.add(e)
        exprs.append([lab, e])


def wrap(inner):
    return f"trade_when({GATE}, {inner}, {EXIT})"


def sp(x, group, dec=10):
    return f"signed_power(subtract(0.5, group_rank(ts_decay_linear({x}, {dec}), {group})), 0.5)"


# ============ 路线 1：corr 家族时段切片版（w4 未试） ============
C_SLICE = [
    ("cvbp_fh", "corr_volume_with_bid_price_first_half"),
    ("cvbp_lh", "corr_volume_with_bid_price_last_half"),
    ("ba_fh", "corr_bid_with_ask_price_first_half"),
    ("ba_lh", "corr_bid_with_ask_price_last_half"),
    ("cvlp_lh", "corr_volume_with_last_price_last_half"),
    ("vw_high", "corr_interval_vwap_with_interval_high"),
    ("vw_low", "corr_interval_vwap_with_interval_low_2"),
    ("lvh_ih", "corr_last_high_with_interval_vwap"),
]
for tag, fld in C_SLICE:
    add(f"W5_corrs{tag}", wrap(sp(fld, 'country', 10)))

# ============ 路线 2：corr 家族时序化（delta / zscore） ============
C_CORE = [
    ("clpvw", "corr_last_trade_price_with_volume"),
    ("highvw", "corr_high_price_with_volume"),
    ("vwapvw", "corr_vwap_with_volume"),
]
for tag, fld in C_CORE:
    add(f"W5_corrd22_{tag}", wrap(sp(f"ts_delta({fld}, 22)", 'country', 10)))
    add(f"W5_corrdz_{tag}", wrap(sp(f"ts_zscore({fld}, 252)", 'country', 10)))

# ============ 路线 3：未占用收益率腿 ============
R_LEGS = [
    ("last60", LAST60),
    ("high30", HIGH30R),
    ("ask30", ASK30R),
    ("bid30", BID30R),
]
for tag, fld in R_LEGS:
    add(f"W5_spdec11_{tag}", wrap(sp(fld, 'country', 11)))   # decay11 = w3 甜点

# ============ 路线 4：TS 时序反转几何（换几何，天然低相关） ============
for tag, fld in [("last30", LAST30), ("last60", LAST60), ("high30", HIGH30R)]:
    add(f"W5_tsr_{tag}", wrap(f"-ts_rank(ts_decay_linear({fld}, 10), 252)"))
    add(f"W5_tsz_{tag}", wrap(f"-ts_zscore(ts_decay_linear({fld}, 10), 252)"))

# ============ 路线 5：换中性化轴（last30 的非 country 轴） ============
for ax in ("sector", "industry", "subindustry", "market"):
    add(f"W5_ax{ax[:4]}_last30", wrap(sp(LAST30, ax, 11)))

os.makedirs(os.path.dirname(OUT), exist_ok=True)
with open(OUT, "w", encoding="utf-8") as f:
    json.dump(exprs, f, ensure_ascii=False, indent=1)

print(f"written {len(exprs)} exprs -> {os.path.abspath(OUT)}")
for lab, _ in exprs:
    print(" ", lab)
