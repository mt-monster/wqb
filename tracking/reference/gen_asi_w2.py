"""ASI RA 探针生成器（w2）——在 w1 成功配方上做"降换手"变体。

背景（w1 实测）：
  - w1（SECTOR/decay12）11/15 条 S≥1.58，最强 W1_last30_gcoun S=3.03/F=1.29
  - 但全部 T≈0.43~0.51，撞 HIGH_TURNOVER 硬闸（limit=0.4）→ 全部不可提交
  - 已成功三颗 ACTIVE（同骨架）T=0.21~0.30 → 说明骨架本身可达标，需降换手

降换手手段（合规，均为 memory 推荐的"单信号结构化"）：
  1. hump(x, 0.01)            专治换手（限幅，抑制微小权重抖动）
  2. ts_decay_linear 加长窗    (4 → 8/13/22) 平滑信号
  3. 外层再加 ts_decay_linear 对最终权重平滑
  4. 加大 settings decay       (12 → 22/30)

合规：不改信号概念（仍是尾盘价量反转单腿），只做时序平滑/限幅 → 属结构化，非混信号。
"""
import json, os

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                   "..", "ASI", "candidates", "probe_asi_w2.json")

VOL_GATE = "rank(divide(mean_trade_volume_30m_pre_close_2, ts_mean(volume, 22))) > 0.5"
NEWS_GATE = "rank(ts_mean(normalized_news_article_count, 22)) > 0.3"
GATE = f"and({VOL_GATE}, {NEWS_GATE})"
EXIT = "or(rank(divide(mean_trade_volume_30m_pre_close_2, ts_mean(volume, 22))) < 0.3, rank(ts_mean(normalized_news_article_count, 22)) < 0.2)"


def core(x, group, dec):
    return f"signed_power(subtract(0.5, group_rank(ts_decay_linear({x}, {dec}), {group})), 0.5)"


def wrap(inner):
    return f"trade_when({GATE}, {inner}, {EXIT})"


# 信号腿：w1 里最强的三个（避免与 w1 之外的无关字段）
LEGS = [
    ("last30", "mean_last_trade_price_return_30m_pre_close_2"),  # w1 最强 S=3.03
    ("bid30", "mean_bid_price_return_30m_pre_close_2"),          # w1 S=2.46
    ("ask30", "mean_ask_price_return_30m_pre_close_2"),          # w1 S=2.41
]

exprs = []
seen = set()


def add(lab, e):
    if e not in seen:
        seen.add(e)
        exprs.append([lab, e])


# --- H 组：hump 限幅（最直接） ---
for tag, fld in LEGS:
    add(f"W2_hump_{tag}",
        wrap(f"hump({core(fld, 'country', 4)}, 0.01)"))

# --- D 组：加长 ts_decay_linear 窗（4→13/22） ---
for tag, fld in LEGS:
    for dec in (13, 22):
        add(f"W2_dec{dec}_{tag}",
            wrap(core(fld, 'country', dec)))

# --- HH 组：hump + 长窗（组合） ---
for tag, fld in LEGS:
    add(f"W2_hump_dec13_{tag}",
        wrap(f"hump({core(fld, 'country', 13)}, 0.01)"))

# --- 外层平滑：对最终权重再 ts_decay_linear ---
for tag, fld in LEGS:
    add(f"W2_outerdec8_{tag}",
        wrap(f"ts_decay_linear({core(fld, 'country', 4)}, 8)"))

# --- 更大 hump 阈值对比 ---
add("W2_hump003_last30", wrap(f"hump({core('mean_last_trade_price_return_30m_pre_close_2', 'country', 4)}, 0.03)"))

os.makedirs(os.path.dirname(OUT), exist_ok=True)
with open(OUT, "w", encoding="utf-8") as f:
    json.dump(exprs, f, ensure_ascii=False, indent=1)

print(f"written {len(exprs)} exprs -> {os.path.abspath(OUT)}")
for lab, e in exprs:
    print(lab)
