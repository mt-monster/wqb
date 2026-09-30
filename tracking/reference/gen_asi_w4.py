"""ASI RA 探针生成器（w4）—— Mode B 换信号概念，目标【低自相关】。

## 为什么需要 w4（w3 的瓶颈）

w3 找到换手/适应度甜点（decay 10~13），但 4 颗全过候选**彼此仅 decay 差 1~2**
→ 互相关系数必然 >0.99。

实测：`1YZqNxM6`（dec13）**提交层 403，原因是 `SELF_CORRELATION` value=0.7603 > limit=0.7**。
（同批 `0mrbYmp6`/`wpb89PO2`/`1YZqNE2K` 另有 `LOW_ROBUST_UNIVERSE_RETURNS` 模拟层 FAIL，
value 与 limit 仅差 0.0001~0.0006 → 也是卡点。）

→ **结论：同骨架调参路线已到顶**。要再拿多颗，必须走 **Mode B：换信号概念**
（memory §0 铁律：唯一合规方向 = 换字段组合/换信号概念/换算子几何/换分组轴）。

## w4 设计：换到未触碰的 `corr_*` 家族（价量协同性，与收益率家族语义正交）

w1/w3 用的全是 `mean_*_price_return_*`（**收益率**）。
`intraday_pv_feats` 另有一大家 `corr_*`（**日内区间相关性**，共 ~150 个字段）完全未用：
  - `corr_last_trade_price_with_volume`  ← asi_priors 已实证可用（"dw 20d robust 0.82"）
  - `corr_vwap_with_volume` / `corr_bid_price_with_volume` / `corr_ask_price_with_volume`
  - `corr_high_price_with_volume` / `corr_low_price_with_volume`
  - `corr_last_vwap_with_volume`
  - 深度/滑点类：`corr_ask_price_with_bid_size` / `corr_bid_price_with_ask_size`
    / `corr_ask_price_with_slippage` / `corr_bid_price_with_slippage`
    / `corr_last_trade_price_with_slippage` / `corr_high_price_with_bid_size`

**经济含义**（与收益率反转不同）：日内「价量协同性」衡量**上涨是否放量**。
正相关 = 放量推价（趋势/知情交易）；负相关 = 缩量涨（流动性驱动、易反转）。
→ 这是**独立的第二信号家族**，不是同骨架变体。

## 分组轴也换（memory 明列的合规方向）

w1/w3 全用 `country`。w4 混入 `sector` / `industry` / `subindustry` / `market`
→ 同样的字段在不同分组下 = 不同的横截面暴露 → 天然降相关。

## 算子几何也换

w1/w3 全是 `signed_power(subtract(0.5, group_rank(...)), 0.5)`。
w4 混入：
  - `group_zscore` + 负号（asi_priors wins[1] 的原式）
  - `ts_rank`（长窗平滑，换手更友好）
  - `ts_zscore`

合规自检：单信号腿（一个 corr_* 字段）+ 新闻量仅作门控 → 非混信号。
"""
import json
import os

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                   "..", "ASI", "candidates", "exprs_asi_w4.json")

VOL_GATE = "rank(divide(mean_trade_volume_30m_pre_close_2, ts_mean(volume, 22))) > 0.5"
NEWS_GATE = "rank(ts_mean(normalized_news_article_count, 22)) > 0.3"
GATE = f"and({VOL_GATE}, {NEWS_GATE})"
EXIT = ("or(rank(divide(mean_trade_volume_30m_pre_close_2, ts_mean(volume, 22))) < 0.3, "
        "rank(ts_mean(normalized_news_article_count, 22)) < 0.2)")

# corr_* 家族（价量协同性 / 深度 / 滑点）—— 全部与收益率家族正交
CORR_LEGS = [
    ("clpvw", "corr_last_trade_price_with_volume"),   # asi_priors 实证腿
    ("vwapvw", "corr_vwap_with_volume"),
    ("bidvw", "corr_bid_price_with_volume"),
    ("askvw", "corr_ask_price_with_volume"),
    ("highvw", "corr_high_price_with_volume"),
    ("lowvw", "corr_low_price_with_volume"),
    ("lvwapvw", "corr_last_vwap_with_volume"),
    ("askbidsz", "corr_ask_price_with_bid_size"),     # 深度类
    ("bidasksz", "corr_bid_price_with_ask_size"),
    ("askslip", "corr_ask_price_with_slippage"),      # 滑点类
    ("bidslip", "corr_bid_price_with_slippage"),
    ("clpslip", "corr_last_trade_price_with_slippage"),
    ("highbidsz", "corr_high_price_with_bid_size"),
    ("vwapbidsz", "corr_vwap_with_bid_size"),
]

exprs = []
seen = set()


def add(lab, e):
    if e not in seen:
        seen.add(e)
        exprs.append([lab, e])


def wrap(inner):
    return f"trade_when({GATE}, {inner}, {EXIT})"


# --- 几何 A：group_zscore 取负（asi_priors wins[1] 原式）+ decay 10 甜点 ---
for tag, fld in CORR_LEGS:
    add(f"W4_gz10_{tag}",
        wrap(f"-group_zscore(ts_decay_linear({fld}, 10), country)"))

# --- 几何 B：signed_power(subtract(0.5, group_rank)) — w3 骨架但换字段 ---
for tag, fld in CORR_LEGS[:7]:
    add(f"W4_sp10_{tag}",
        wrap(f"signed_power(subtract(0.5, group_rank(ts_decay_linear({fld}, 10), country)), 0.5)"))

# --- 几何 C：换分组轴（sector/industry/market）—— 天然降相关 ---
AXES = ("sector", "industry", "market")
for i, (tag, fld) in enumerate(CORR_LEGS[:6]):
    ax = AXES[i % 3]
    add(f"W4_gz10{ax[:3]}_{tag}",
        wrap(f"-group_zscore(ts_decay_linear({fld}, 10), {ax})"))

# --- 几何 D：ts_rank 长窗平滑（换手友好 + 与 zscore/rank 不同几何）---
for tag, fld in CORR_LEGS[:6]:
    add(f"W4_tsr252_{tag}",
        wrap(f"-ts_rank(ts_decay_linear({fld}, 10), 252)"))

# --- 几何 E：ts_zscore（时序标准化，第三种几何）---
for tag, fld in CORR_LEGS[:6]:
    add(f"W4_tsz252_{tag}",
        wrap(f"-ts_zscore(ts_decay_linear({fld}, 10), 252)"))

os.makedirs(os.path.dirname(OUT), exist_ok=True)
with open(OUT, "w", encoding="utf-8") as f:
    json.dump(exprs, f, ensure_ascii=False, indent=1)

print(f"written {len(exprs)} exprs -> {os.path.abspath(OUT)}")
for lab, _ in exprs:
    print(" ", lab)
