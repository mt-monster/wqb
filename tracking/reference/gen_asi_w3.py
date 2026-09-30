"""ASI RA 探针生成器（w3）——目标：换手 <0.4 且 fitness ≥1.0 同时成立。

## 为什么需要 w3（w1/w2 实测）

w1（SECTOR/decay12，20 条）：
  - 11/15 条 S≥1.58，最强 `W1_last30_gcoun`(O081GNWY) S=3.03 / **F=1.29** / SUB=2.13
  - 但 T≈0.43~0.51 → 全部撞 `HIGH_TURNOVER` 硬闸（limit 0.4）
  - 唯一四硬闸全过的是 O081GNWY（模拟层 19 checks：0 FAIL）

w2（降换手变体，16 条，补取指标后）：
  - 加长 ts_decay_linear 窗（4→13/22）+ 外层平滑 → T 成功压到 0.33~0.38 ✓
  - **但 F 全线掉到 0.61~0.96** ✗（闸 1.0）
  - 最好 `88Pm3RYv`(外层 dec8) S=2.20 / F=0.96 / T=0.3686 → 仍差 0.04

## 核心矛盾（本轮要解的）

S 与 F 同源（F ≈ S × sqrt(|ret|/max(to, 0.125)) × 常数），降窗/降 T 必然同降 S 与 F。
把 T 从 0.49 压到 0.37 时 F 掉 0.33 → **要保住 F≥1.0，T 只能压到 ~0.43**（不能到 0.37）。
→ 必须找"**压 T 但不压 F**"的手段，即**不改变信号强度、只消除微小权重的无效抖动**。

## w3 三路（均为合规"单信号结构化"，不改信号概念）

1. **round T 边界**：decay 13→9/10/11、外层 dec 8→4/5/6 → 在 T≈0.40~0.44 区间精确定位。
2. **hump 限幅**（改对语法！w2 的 `hump(x, 0.01)` 位置传参报错）：
   平台签名 `hump(x, hump = 0.01)` 是 keyword 命名参 → 必须写 `hump(x)` 或 `hump(x, hump=0.01)`。
   hump 只把 |Δw| 限幅到阈值，**不改信号排序** → 是"压 T 保 F"的最优候选。
3. **ts_target_tvr_hump**（定向压 T）：`ts_target_tvr_hump(x, lambda_min, lambda_max, target_tvr)`，
   扫 target_tvr = 0.35/0.40/0.45，让平台自己去逼近目标换手。

合规自检：全部仍是「尾盘价量反转单腿 + 新闻量门控」，无第二条信号腿相加 → 非混信号。
"""
import json
import os

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                   "..", "ASI", "candidates", "probe_asi_w3.json")

VOL_GATE = "rank(divide(mean_trade_volume_30m_pre_close_2, ts_mean(volume, 22))) > 0.5"
NEWS_GATE = "rank(ts_mean(normalized_news_article_count, 22)) > 0.3"
GATE = f"and({VOL_GATE}, {NEWS_GATE})"
EXIT = ("or(rank(divide(mean_trade_volume_30m_pre_close_2, ts_mean(volume, 22))) < 0.3, "
        "rank(ts_mean(normalized_news_article_count, 22)) < 0.2)")

# w1 唯一四闸全过 + w2 最好两条
LAST30 = "mean_last_trade_price_return_30m_pre_close_2"   # w1 O081GNWY S=3.03 F=1.29
BID30 = "mean_bid_price_return_30m_pre_close_2"           # w1 npP1NgPq S=2.46
ASK30 = "mean_ask_price_return_30m_pre_close_2"           # w2 ZYAR0Rj3 S=2.02(F=0.82)


def core(x, group, dec):
    return f"signed_power(subtract(0.5, group_rank(ts_decay_linear({x}, {dec}), {group})), 0.5)"


def wrap(inner):
    return f"trade_when({GATE}, {inner}, {EXIT})"


exprs = []
seen = set()


def add(lab, e):
    if e not in seen:
        seen.add(e)
        exprs.append([lab, e])


# --- 路线 2：hump 限幅（正确语法；压 T 保 F 的最优候选）---
# hump 只对 |Δw| 限幅、不动排序 → 期望 T 显著降而 F 基本保持
for tag, fld in (("last30", LAST30), ("bid30", BID30), ("ask30", ASK30)):
    add(f"W3_hump_default_{tag}", wrap(f"hump({core(fld, 'country', 4)})"))
    add(f"W3_hump003_{tag}", wrap(f"hump({core(fld, 'country', 4)}, hump=0.03)"))
    add(f"W3_hump_dec9_{tag}", wrap(f"hump({core(fld, 'country', 9)})"))

# --- 路线 1：T 边界精扫（decay 9/10/11/13 + 外层 4/5/6）---
for tag, fld in (("last30", LAST30), ("ask30", ASK30)):
    for dec in (9, 10, 11, 13):
        add(f"W3_dec{dec}_{tag}", wrap(core(fld, 'country', dec)))
    for od in (4, 5, 6):
        add(f"W3_outer{od}_{tag}", wrap(f"ts_decay_linear({core(fld, 'country', 4)}, {od})"))

# --- 路线 3：ts_target_tvr_hump 定向压 T ---
for tag, fld in (("last30", LAST30), ("ask30", ASK30)):
    for tvr in (0.35, 0.40, 0.45):
        add(f"W3_ttth{tvr}_{tag}",
            wrap(f"ts_target_tvr_hump({core(fld, 'country', 4)}, 0, 1, {tvr})"))

os.makedirs(os.path.dirname(OUT), exist_ok=True)
with open(OUT, "w", encoding="utf-8") as f:
    json.dump(exprs, f, ensure_ascii=False, indent=1)

print(f"written {len(exprs)} exprs -> {os.path.abspath(OUT)}")
for lab, _ in exprs:
    print(" ", lab)
