"""ASI w14 —— 攻 `ask30`/`bid30` 腿的 F≥1.0（该族 self-corr 仅 0.57~0.66 ✓）。

## 现状（本轮实测，2026-09-30 ET）

`ask30`/`bid30`（ask/bid 报价收益率）是**未被占用的腿**，且自相关极低：

| 候选 | 腿/窗 | S | F | **self max** | 主要相关对象 |
|---|---|---|---|---|---|
| `zqbq8rR8` | bid30/d5 | 2.44 | **0.98** | **0.6624 ✓** | E5R56EbR |
| `GrOrOl3Z` | ask30/d5 | 2.40 | 0.95 | **0.6630 ✓** | E5R56EbR |
| `omW1apxE` | ask30/d11 | 2.22 | 0.92 | **0.5758 ✓** | E5R56EbR |
| `QPK1oRxw` | bid30/d11 | 2.19 | 0.90 | **0.5723 ✓** | 88jaV5lv |
| `leKeaJP5` | bid30/d4(MARKET) | 2.35 | 0.86 | 0.7453 ✗ | E5R56EbR |

→ **只差 F**：`zqbq8rR8` 差 **0.02**；其余差 0.05~0.10。

## 提 F 的手段（F ≈ S × sqrt(|ret| / max(T,0.125)) × k）

1. ★ **换 vol-only 门控**（已证提 S 幅度极大）：同一 last60 腿，`and(vol,news)` → `vol-only`
   使 **S 由 2.61 → 3.10（+0.49）**，F 由 1.10 → 1.30。**去除 news 过滤扩大股票池 → 捕获更多原始反转。**
2. **去门控**（纯反转）：S 更高，但可能撞他人 alpha（corr 上升）。
3. **内层窗 d4/d5/d6**：d 越短 S 越高（但 T 也升）。
4. **settings decay 加大**：降 T 提 F（需单独 run）。

## w14 设计（单次 run，SECTOR/decay12/trunc0.08）

门控三档 × 腿 × 窗：
- 门控 `and(vol>0.5, news>0.3)`（原配方，基线）
- 门控 `vol>0.5`（**vol-only，主攻**）
- 无门控（纯反转，极限 S 对照）

跑完取 S/F/T，并逐个测 self-corr（阈值 <0.7，目标 <0.66 保持余量）。

合规：门控是条件项；无门控版 = 纯单腿信号。信号本体始终单一 `ask/bid` 收益率腿 → 非混信号。
"""
import json
import os

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                   "..", "ASI", "candidates", "exprs_asi_w14.json")

VOL = "rank(divide(mean_trade_volume_30m_pre_close_2, ts_mean(volume, 22)))"
NEWS = "rank(ts_mean(normalized_news_article_count, 22))"

GATES = {
    "and":   (f"and({VOL} > 0.5, {NEWS} > 0.3)", f"or({VOL} < 0.3, {NEWS} < 0.2)"),
    "vol":   (f"{VOL} > 0.5",                     f"{VOL} < 0.3"),
    "none":  (None,                               None),
}

LEGS = [
    ("ask30", "mean_ask_price_return_30m_pre_close_2"),
    ("bid30", "mean_bid_price_return_30m_pre_close_2"),
]

exprs = []
seen = set()


def add(lab, e):
    if e not in seen:
        seen.add(e)
        exprs.append([lab, e])


def core(x, dec=5, group="country"):
    return f"signed_power(subtract(0.5, group_rank(ts_decay_linear({x}, {dec}), {group})), 0.5)"


# 门控 vol-only（主攻）× 双腿 × 窗 d4/d5/d6
for gname in ("vol", "and", "none"):
    g, x = GATES[gname]
    for tag, fld in LEGS:
        for dec in (4, 5, 6):
            c = core(fld, dec)
            lab = f"W14_{gname}_{tag}_d{dec}"
            if g is None:
                add(lab, c)
            else:
                add(lab, f"trade_when({g}, {c}, {x})")

os.makedirs(os.path.dirname(OUT), exist_ok=True)
with open(OUT, "w", encoding="utf-8") as f:
    json.dump(exprs, f, ensure_ascii=False, indent=1)

print(f"written {len(exprs)} exprs -> {os.path.abspath(OUT)}")
for lab, _ in exprs:
    print(" ", lab)
