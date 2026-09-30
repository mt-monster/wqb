"""ASI w8 —— 攻 `LOW_ROBUST_UNIVERSE_RETURNS` 最后一根头发（blOlOp3K 差 0.0001）。

## 现状（2026-09-29 实测）

`blOlOp3K` = last60/dec5，MINVOL1M+SECTOR+settings_decay12+trunc0.08：
18/19 checks PASS（含 SELF_CORRELATION 0.5839 ✓ / PROD 0.5839 ✓），
**唯一 FAIL = `LOW_ROBUST_UNIVERSE_RETURNS` value=0.0749 / limit=0.075（ratio=0.9）**。

## 已发现的单调律（关键线索）

| 候选 | 内层 dec | S | F | robust value | limit | ratio |
|---|---|---|---|---|---|---|
| blOlOp3K (last60) | **5** | 2.61 | 1.10 | 0.0749 | 0.0750 | **0.9987** |
| akxkbQNO (last60) | **7** | 2.42 | 1.03 | 0.0688 | 0.0698 | 0.9857 |
| omW1apxE (ask30) | **11** | 2.22 | 0.92 | 0.0645 | 0.0615 | **1.0488 ✓** |
| O081GNWY (last30) | 4 | 3.03 | 1.29 | 0.0809 | 0.0808 | 1.0012 ✓ |

→ ★ **内层窗越短，robust 比值越高**（last60: dec7 0.9857 → dec5 0.9987）。
→ 外推：**dec 2/3/4** 应能把比值推过 1.0，同时 S 还会升（S 随窗短而升）→ F 也升。

## w8 设计（同一 config 单次探针即可）

config 固定 = `MINVOL1M + SECTOR + settings_decay 12 + trunc 0.08`（blOlOp3K 同配置）
→ 保证 self-corr 仍在 ~0.58 安全区。

腿 × 内层窗：
- `last60` × dec 2, 3, 4（主攻：0.9987 → 需 +0.13%）
- `last60` × dec 6（补验证单调性）
- `ask30`  × dec 3, 5（ask30 的 robust 比值本就 1.0488，短窗后 S/F 若上来即双赢）
- `bid30`  × dec 5
- `last30` × dec 5（对照：S 最高但 self-corr 0.81 必 FAIL，仅作 robustness 参照）

合规：全部单信号腿 + 门控，无混信号。
"""
import json
import os

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                   "..", "ASI", "candidates", "exprs_asi_w8.json")

VOL_GATE = "rank(divide(mean_trade_volume_30m_pre_close_2, ts_mean(volume, 22))) > 0.5"
NEWS_GATE = "rank(ts_mean(normalized_news_article_count, 22)) > 0.3"
GATE = f"and({VOL_GATE}, {NEWS_GATE})"
EXIT = ("or(rank(divide(mean_trade_volume_30m_pre_close_2, ts_mean(volume, 22))) < 0.3, "
        "rank(ts_mean(normalized_news_article_count, 22)) < 0.2)")

LAST60 = "mean_last_trade_price_return_60m_pre_close_2"
ASK30 = "mean_ask_price_return_30m_pre_close_2"
BID30 = "mean_bid_price_return_30m_pre_close_2"
LAST30 = "mean_last_trade_price_return_30m_pre_close_2"

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


# 主攻：last60 短窗（robust 比值随窗短升）
for dec in (2, 3, 4, 6):
    add(f"W8_last60_d{dec}", wrap(sp(LAST60, 'country', dec)))

# ask30 短窗（robust 本就 1.0488，短窗提 S/F 双赢）
for dec in (3, 5):
    add(f"W8_ask30_d{dec}", wrap(sp(ASK30, 'country', dec)))

# bid30
add("W8_bid30_d5", wrap(sp(BID30, 'country', 5)))

# 对照
add("W8_last30_d5", wrap(sp(LAST30, 'country', 5)))

os.makedirs(os.path.dirname(OUT), exist_ok=True)
with open(OUT, "w", encoding="utf-8") as f:
    json.dump(exprs, f, ensure_ascii=False, indent=1)

print(f"written {len(exprs)} exprs -> {os.path.abspath(OUT)}")
for lab, _ in exprs:
    print(" ", lab)
