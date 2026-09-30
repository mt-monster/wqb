"""ASI w10 —— 用「换门控条件」制造与 1YZYj5QQ 低相关的第二颗（last60 系）。

## 为什么走这条（实测规律）

| 变化维度 | 对 self-corr 的效果 | 证据 |
|---|---|---|
| 换腿 last30 → **last60** | **最强**（0.81 → 0.57） | 1YZYj5QQ self 0.5732 vs O081GNWY 0.8127 |
| 换中性化 SECTOR → MARKET | 中等（0.81 → 0.69） | E5R56EbR self 0.6918（余量仅 0.008，太薄） |
| 换内层窗 d4 → d11 | 反向恶化 | XgJgaXeX(d11) 0.7690 > E5R56EbR(d4) 0.6918 |

→ 已提交 `1YZYj5QQ` = last60/**d4**/country/**SECTOR**，self 0.5732（含 vs 88jaV5lv）。
→ 第二颗必须与 `1YZYj5QQ` 也拉开，否则会撞自己。

## 杠杆：换「门控条件」（合规 —— 门控是条件不是信号腿）

`1YZYj5QQ` 的门控 = `and(vol>0.5, news>0.3)`，退出 `or(vol<0.3, news<0.2)`。
**门控决定「持哪些股」** → 换门控 = 换持仓集合 = 换 PnL → 直接降相关，且不动信号本体。

参照现有 alpha 的门控形态：
- `88jaV5lv` / `P02wbJAM`：`and(vol>0.5, news>0.3)`（本颗同）
- `LLNgdpw2`：**news-only** `news>0.5`，退出 `news<0.4`

## w10 变体（全部 last60 系，保持 MINVOL1M+SECTOR+decay12+trunc0.08 已证配置）

门控变体 × 内层窗：
1. `news_only_d4`    —— 纯新闻门控（LLNgdpw2 形态）：gate `news>0.5` / exit `news<0.4`
2. `vol_only_d4`     —— 纯量门控：gate `vol>0.5` / exit `vol<0.3`
3. `news07_d4`       —— `and(vol>0.5, news>0.7)`
4. `both07_d4`       —— `and(vol>0.7, news>0.5)`
5. `newsw5_d4`       —— 新闻窗 22 → 5
6. `newsw63_d4`      —— 新闻窗 22 → 63
7. `news_only_d3`    —— 纯新闻门控 + 更短内层窗
8. `news_only_d5`    —— 纯新闻门控 + 稍长内层窗
9. `news_only_d6`
10. `news_only_d11`  —— 与 LLNgdpw2 同内层窗(4?)对照

合规自检：门控是 `trade_when` 的条件项，信号本体始终是**单一 last60 腿** → 非混信号。
"""
import json
import os

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                   "..", "ASI", "candidates", "exprs_asi_w10.json")

LAST60 = "mean_last_trade_price_return_60m_pre_close_2"

VOL = "rank(divide(mean_trade_volume_30m_pre_close_2, ts_mean(volume, 22)))"
NEWS22 = "rank(ts_mean(normalized_news_article_count, 22))"
NEWS5 = "rank(ts_mean(normalized_news_article_count, 5))"
NEWS63 = "rank(ts_mean(normalized_news_article_count, 63))"

exprs = []
seen = set()


def add(lab, e):
    if e not in seen:
        seen.add(e)
        exprs.append([lab, e])


def core(dec):
    return (f"signed_power(subtract(0.5, group_rank(ts_decay_linear({LAST60}, {dec}), country)), 0.5)")


GATES = {
    # name:        (entry_condition,                              exit_condition)
    "news_only":   (f"{NEWS22} > 0.5",                            f"{NEWS22} < 0.4"),
    "vol_only":    (f"{VOL} > 0.5",                               f"{VOL} < 0.3"),
    "news07":      (f"and({VOL} > 0.5, {NEWS22} > 0.7)",          f"or({VOL} < 0.3, {NEWS22} < 0.5)"),
    "both07":      (f"and({VOL} > 0.7, {NEWS22} > 0.5)",          f"or({VOL} < 0.5, {NEWS22} < 0.3)"),
    "newsw5":      (f"and({VOL} > 0.5, {NEWS5} > 0.3)",           f"or({VOL} < 0.3, {NEWS5} < 0.2)"),
    "newsw63":     (f"and({VOL} > 0.5, {NEWS63} > 0.3)",          f"or({VOL} < 0.3, {NEWS63} < 0.2)"),
}

# 1-6：各门控 × 内层 d4
for gname, (g, x) in GATES.items():
    add(f"W10_{gname}_d4", f"trade_when({g}, {core(4)}, {x})")

# 7-10：纯新闻门控 × 内层窗 d3/d5/d6/d11
for dec in (3, 5, 6, 11):
    g, x = GATES["news_only"]
    add(f"W10_news_only_d{dec}", f"trade_when({g}, {core(dec)}, {x})")

os.makedirs(os.path.dirname(OUT), exist_ok=True)
with open(OUT, "w", encoding="utf-8") as f:
    json.dump(exprs, f, ensure_ascii=False, indent=1)

print(f"written {len(exprs)} exprs -> {os.path.abspath(OUT)}")
for lab, _ in exprs:
    print(" ", lab)
