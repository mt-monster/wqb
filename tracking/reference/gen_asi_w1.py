"""ASI RA 探针生成器（w1）——复用已实证的 ASI 结构模板。

来源（全部来自本项目实证，非直觉）：
  asi_priors.wins[2] / ASI 三颗 ACTIVE (P02wbJAM / 88jaV5lv / LLNgdpw2, 2026-09-21~23)：
    结构 = trade_when(<关注度门控>, signed_power(subtract(0.5, group_rank(ts_decay_linear(X,4), country)), 0.5), <退出>)
    其中：
      - 门控腿 A：rank(divide(mean_trade_volume_30m_pre_close_2, ts_mean(volume,22))) > 0.5   （尾盘量占比）
      - 门控腿 B：rank(ts_mean(normalized_news_article_count,22)) > 0.3                        （新闻关注度，来自 news_sentiment_transfer，仅作门控）
      - 信号腿 X：尾盘 30m 价格收益率（单字段、单腿 → 合规，非混信号）
      - 分组轴：country（ASI 特有，region_kb 实证）
  asi_priors.key_notes："news_sentiment_transfer 的 normalized_news_article_count 仅作关注度门控腿（已实证有效）"
  asi_priors.wins[1]：intraday_pv_feats 收盘前 30 分钟反转 / 价量相关反转

合规性（对应用户铁律）：
  - 不 add / 不 multiply 两条独立信号腿 → 信号本体只有一条腿 X（尾盘价量特征），门控只是触发条件
  - 用 trade_when 事件门控（memory §0 明确列入合规方向）+ group_rank + signed_power（结构化）
  - 反向统一写 subtract(0.5, ...) 使零均值（反转三铁律之二）

探针设计（Mode B = 换字段，不换概念）：
  维度1  信号腿 X：ask/bid/high/low/成交量 的 30m/60m 尾盘收益与量特征（同族不同字段 → 低相关新 alpha）
  维度2  分组轴：country / subindustry / sector
  维度3  窗口：30m / 60m
"""
import json
import os

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                   "..", "ASI", "candidates", "probe_asi_w1.json")

# ---- 门控（固定，来自已实证成功结构）----
VOL_GATE = "rank(divide(mean_trade_volume_30m_pre_close_2, ts_mean(volume, 22))) > 0.5"
NEWS_GATE = "rank(ts_mean(normalized_news_article_count, 22)) > 0.3"
GATE = f"and({VOL_GATE}, {NEWS_GATE})"
EXIT = "or(rank(divide(mean_trade_volume_30m_pre_close_2, ts_mean(volume, 22))) < 0.3, rank(ts_mean(normalized_news_article_count, 22)) < 0.2)"


def wrap(x, group="country", dec=4):
    """单信号腿结构化包装（已实证骨架）。"""
    return (f"trade_when({GATE}, "
            f"signed_power(subtract(0.5, group_rank(ts_decay_linear({x}, {dec}), {group})), 0.5), "
            f"{EXIT})")


# ---- 信号腿候选（同族未用字段；已成功用的是 mean_last_trade_price_return_30m_pre_close_2）----
SIGNAL_FIELDS = [
    # A. 尾盘 30m 价格收益率（ask/bid/high —— 已成功只用过 last_trade_price）
    ("ask30", "mean_ask_price_return_30m_pre_close_2"),
    ("bid30", "mean_bid_price_return_30m_pre_close_2"),
    ("high30", "mean_high_price_return_30m_pre_close_2"),
    ("last30", "mean_last_trade_price_return_30m_pre_close_2"),
    # B. 尾盘 60m 价格收益率（60m 窗口 = 更长信息累积，与 30m 低相关）
    ("ask60", "mean_ask_price_return_60m_pre_close_2"),
    ("bid60", "mean_bid_price_return_60m_pre_close_2"),
    # C. 尾盘量/流动性特征
    ("vol30", "mean_trade_volume_30m_pre_close_2"),
    ("slippage", "max_slippage_30m_pre_close_2"),
    ("vwapratio30", "mean_ask_vwap_ratio_30m_pre_close_2"),
    ("bidask30", "mean_bid_ask_size_ratio_30m_pre_close_2"),
]

GROUPS = ["country", "subindustry"]

exprs = []
seen = set()
for tag, fld in SIGNAL_FIELDS:
    for g in GROUPS:
        e = wrap(fld, group=g)
        if e in seen:
            continue
        seen.add(e)
        exprs.append([f"W1_{tag}_g{g[:4]}", e])

os.makedirs(os.path.dirname(OUT), exist_ok=True)
with open(OUT, "w", encoding="utf-8") as f:
    json.dump(exprs, f, ensure_ascii=False, indent=1)

print(f"written {len(exprs)} exprs -> {os.path.abspath(OUT)}")
for lab, e in exprs[:3]:
    print(lab, "::", e[:180])
