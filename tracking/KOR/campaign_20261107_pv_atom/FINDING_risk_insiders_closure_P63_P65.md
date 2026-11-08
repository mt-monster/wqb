# P63/P64/P65 收割：risk88 与 insiders5 的两处遗漏已补测完毕（2026-11-07）

## P63 — risk88（1V98du4Ll5fAbEmFF3UtTVd）10/10 完成，0 错

| alpha | 机制 | S | F | 2Y | raF |
|---|---|---:|---:|---:|---:|
| gJeLvKje | 特异收益 ÷ 特异风险（dsrt/srisk） | 0.96 | 0.42 | 0.34 | 5 |
| 9qxkoKpo | srisk 时序分位 252 | 0.80 | 0.50 | **1.89** | 2 |
| GrW9V6Gx | 价值载荷漂移 − 动量载荷漂移 | 0.74 | 0.44 | 0.77 | 3 |
| j2YOLXrO | srisk 水平（低特异风险溢价） | 0.69 | 0.54 | 1.38 | 3 |
| e75EAK3z | Δ srisk 66d（风险收缩） | 0.38 | 0.16 | 1.56 | 3 |
| xAr5MQjn | 非线性规模 − 规模 价差 | −0.14 | −0.04 | 0.30 | 5 |
| e75EAKzE | 特异收益-特异风险 ts_corr 66 | −0.21 | −0.05 | 0.41 | 4 |
| mLoQOA5E | 杠杆载荷漂移 66d | −0.32 | −0.11 | −0.06 | 4 |
| GrW9V6dP | 风格载荷集中度（价值/成长/动量 abs 均值） | −0.67 | −0.40 | −0.64 | 5 |
| 9qxkoKXo | 股息载荷漂移 66d | −0.84 | −0.55 | −0.61 | 5 |

**结论：risk88 全灭，最高 0.96。**
- srisk 水平 0.69，与 risk70 的 srisk（0.57）**同量级同方向** ⇒ 换风险模型不改变「特异风险只有水平信息且水平已定价」的结论。
- 风格载荷漂移（4 条）无一过 0.8 ⇒ Barra 风格载荷的变化率在 KOR 无可交易信息。

⇒ **RISK 7 集至此全部到底**（risk70/risk68 各容量 1 已满；risk59/60/71/72/88 判死）。**剩余信号 = 0。**

## P64 — insiders5 库存股族 + 重叠度族（4msrWE15Y5b59AlUbyjrWju）10/10，0 错

| alpha | 机制 | S | 2Y |
|---|---|---:|---:|
| YP1YZOVJ | 源口径未知重叠度 source_real_ratio/source_ratio（未做多空中性化） | −1.55 | −2.05 |
| npvr0lGE | 库存股 ÷ 集团持股 ratio | 0.49 | −0.38 |
| 9qxko359 | Δ 库存股比例 66d | 0.45 | −0.39 |
| QPv6eAxQ | 集团口径重叠度 real_ratio/ratio | −0.36 | −1.00 |
| Xg9Mqxd5 | 库存股关系方数 trsy_tnc | 0.00 | — |
| 其余 5 条 | 库存股水平/陈旧度/价差 · 重叠度时序分位 | \|S\|≤0.20 | — |

**结论：库存股族（trsy_*6 字段）全灭**（最高 0.49，trsy_tnc 恒定为 0 ⇒ 该字段无信号）。
唯一有量的是 **重叠度族**（source_real_ratio / source_ratio）⇒ 进 P65 精修。

## P65 — insiders5 重叠度精修（KHKGVfXP4nhaaxg3IT3aeg）10/10，0 错

| alpha | 几何 | S | F | TO | 2Y |
|---|---|---:|---:|---:|---:|
| 1YN060eK | rank（全市场）+ 负号 | **1.35** | 1.08 | 0.132 | 0.41 |
| akKGXG6v | group_rank(sector) + 负号 | 1.34 | 1.04 | 0.130 | 0.34 |
| WjOJKJqj | ts_mean22 + industry + 负号 | 1.27 | 0.93 | 0.054 | **1.45** |
| xAr5X5qn / KPJZxZ01 | industry / 反比几何 | 1.18 | 0.81 | 0.127 | 0.29 |
| qMLVeV1A | winsorize std=2 | 1.16 | 0.80 | 0.127 | 0.29 |
| vR1PaP8r | subindustry | 0.99 | 0.60 | 0.125 | 0.13 |
| 9qxkgkvd | Δ 66d | 0.63 | 0.21 | 0.213 | −1.32 |
| pwd3Q3Xo | ts_rank 252 | 0.34 | 0.10 | 0.144 | −0.04 |
| E56xox7R | subtract(source_ratio, source_real_ratio) | 0.00 | — | 0.000 | — |

**结论：重叠度族天花板 S 1.35（rank/group_rank 档），2Y 最高 1.45 但 S 只有 1.27。**
不存在 S≥1.58 ∧ 2Y≥1.58 的交集 ⇒ **insiders5 容量仍为 1**（RRE9NkVj）。

## ★ 方法学发现：group_rank 的「负号」不是镜像（本轮最重要的一条）

同一信号的两条读数：

```text
YP1YZOVJ  group_rank(OV, sector)                     S −1.55  TO 0.1296  2Y −2.05
akKGXG6v  multiply(group_rank(OV, sector), −1)        S +1.34  TO 0.1298  2Y +0.34
```

TO 几乎逐位相同（0.1296 vs 0.1298）⇒ 同一条信号、同样的换手，但**收益率曲线不互为相反数**（S 1.55 vs 1.34、2Y 2.05 vs 0.34）。

原因：**group_rank 输出区间是 [0,1]，不是零均值**。
- `group_rank(...)` = 全正的多头簿（含大额市场 beta）；
- `multiply(group_rank(...), −1)` = 全负的空头簿（含反向市场 beta）；
- 平台中性化不会把这个常数偏移完全抹掉，再叠加 truncation 0.08 的非对称截断，两者 PnL 就不对称。

**铁律**：
1. 要检验「反臂」，**必须写 `subtract(0.5, group_rank(...))`**（零均值、真正的多空价差），不要用 `multiply(...,−1)` / `reverse(...)`。
2. 看到「反臂 S 与正臂 S 不等」时，先怀疑这个坑，不要当成市场不对称性去解读。
3. 本轮 YP1YZOVJ 的 2Y −2.05 是**空头簿 beta 伪影**，我一度把它镜像读成「2Y 2.05 过线」，已被 P65 证伪 —— 这类误读会直接导致错判候选。

## 汇总：RISK / INSIDERS 覆盖终态

| 类别 | 集数 | 字段数 | 终态 |
|---|---:|---:|---|
| RISK | 7 | 184 | 全部到底：2 集容量满（risk70 / risk68），5 集判死 |
| INSIDERS | 2 | 62 | insiders1 判死（cov 0.3526）；insiders5 容量 1（已满） |
| **合计** | **9** | **246** | **剩余信号 = 0** |