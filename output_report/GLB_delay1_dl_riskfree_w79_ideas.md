**Dataset**: dl_riskfree_returns
**Region**: GLB
**Delay**: 1
**Universe**: MINVOL1M

# GLB wave79 · dl_riskfree 20 日 CNN × 经济子集门控（胜绩换腿）

> **依据** `Claude/skills/wq-brain-ra-glb/references/other.md` 与已提交 **ACTIVE** alpha **VkaXbmbG**
> （`GLB_dl20d_shortpressure_gate_d10`，2026-09-22 提交，failed_ra_count=0、prod 0.6675、self 0.4649、
> S3.52 / F3.25 / TO0.1171 / 2Y4.52 / sub 2.23，**同时点亮 GLB/D1/PV + RISK + OTHER 三座塔**）。
> **已生效档位**：`cells.json:other:dl_riskfree_returns` = MINVOL1M / SUBINDUSTRY / **decay 10** / trunc 0.08 / 2014-01-01→2023-12-31。
> **纪律**：按 `win_replay_slow_fast_v1`「有 win 则至少 2 槽按机制换腿、禁止克隆 win 表达式」——
> 本波每条**只换一个经济旋钮**（门控读数 / 门控阈值 / 子集阈值 / 信号分母轴），
> 不是参数扫描，也不复制 win 原式。
> **形态边界**：本族形态 = 1 条信号腿（dl_riskfree 20 日 CNN）+ 1 条条件腿（借券压力门控）+ 1 个子集条件（cap 分位）。
> 条件/分组入场是 GLB 允许的组合形态，**不属「两条独立信号腿加权相加」**（那才是被禁的混腿）；
> 信号腿仍只有 1 条。

## 字段（Fields）

| Field ID | Type | 角色 | 说明 |
|---|---|---|---|
| `single_bucket_20day_return_estimate_ohlcv_img_2` | MATRIX | 主信号 | 20 日 CNN 市场中性收益预测分位（胜绩模板的信号腿） |
| `rsk60_offer` | VECTOR | 条件腿 | 借券费率报价（借券紧张度读数） |
| `rsk60_crowding` | VECTOR | 条件腿 | 借券拥挤度（同经济量的另一读数） |
| `cap` | MATRIX | 子集条件 | 市值分位（子集门控） |

## 特征（Features）

- 信号腿：`group_rank(<CNN 分位>, country)` 后减 0.5 → `signed_power(..., 0.5)`（区间归一到 [-0.5, 0.5]）。
- 条件腿：`rank(ts_mean(vec_avg(<借券读数>), 5))`（VECTOR 必须先 vec_avg 聚合）。
- 子集：`rank(cap) > 0.2`（只在大市值子集持仓，避免集中权重）。

## 建议（Implementation Examples）

- dlr20d_gate_crowding: `trade_when(and(rank(ts_mean(vec_avg(rsk60_crowding), 5)) > 0.7, rank(cap) > 0.2), signed_power(subtract(group_rank(single_bucket_20day_return_estimate_ohlcv_img_2, country), 0.5), 0.5), or(rank(ts_mean(vec_avg(rsk60_crowding), 5)) < 0.6, rank(cap) < 0.1))`
- dlr20d_gate_offer_tight: `trade_when(and(rank(ts_mean(vec_avg(rsk60_offer), 5)) > 0.8, rank(cap) > 0.2), signed_power(subtract(group_rank(single_bucket_20day_return_estimate_ohlcv_img_2, country), 0.5), 0.5), or(rank(ts_mean(vec_avg(rsk60_offer), 5)) < 0.7, rank(cap) < 0.1))`
- dlr20d_gate_offer_cap3: `trade_when(and(rank(ts_mean(vec_avg(rsk60_offer), 5)) > 0.7, rank(cap) > 0.3), signed_power(subtract(group_rank(single_bucket_20day_return_estimate_ohlcv_img_2, country), 0.5), 0.5), or(rank(ts_mean(vec_avg(rsk60_offer), 5)) < 0.6, rank(cap) < 0.05))`
- dlr20d_gate_offer_industry: `trade_when(and(rank(ts_mean(vec_avg(rsk60_offer), 5)) > 0.7, rank(cap) > 0.2), signed_power(subtract(group_rank(single_bucket_20day_return_estimate_ohlcv_img_2, industry), 0.5), 0.5), or(rank(ts_mean(vec_avg(rsk60_offer), 5)) < 0.6, rank(cap) < 0.1))`

## 字段白名单（Field Whitelist）

```
single_bucket_20day_return_estimate_ohlcv_img_2
rsk60_offer
rsk60_crowding
cap
```

## Concepts

**Concept**: 20 日 CNN × 借券**拥挤度**门控（换条件腿读数）

- **Mechanism**: 胜绩 VkaXbmbG 用借券**费率**（rsk60_offer）当门控：费率被推到高位 = 空头借券成本高 = 卖压拥挤，此时只在大市值子集持有 20 日 CNN 反转信号。换成**拥挤度**（rsk60_crowding）读的是同一经济量（借券需求是否紧张）的另一侧面——费率可能因整体利率环境抬升而高，拥挤度则只看借券需求本身。两者分母不同、含义不同，故是换腿而非参数变体。
- **Fields**: `single_bucket_20day_return_estimate_ohlcv_img_2`, `rsk60_crowding`, `cap`
- **Implementation Example**: `trade_when(and(rank(ts_mean(vec_avg(rsk60_crowding), 5)) > 0.7, rank(cap) > 0.2), signed_power(subtract(group_rank(single_bucket_20day_return_estimate_ohlcv_img_2, country), 0.5), 0.5), or(rank(ts_mean(vec_avg(rsk60_crowding), 5)) < 0.6, rank(cap) < 0.1))`
- **Direction**: 低分位 → long
- **Expected Exposure**: value
- **Expected Turnover Band**: low
- **Expected Coverage Band**: medium
- **Why not crowded**: 门控读数换字段（费率→拥挤度），信号腿与子集条件不变；避开与 win 的 prod/self 指纹重叠，预期 prod 与 win 有差异但同族。

**Concept**: 20 日 CNN × 更严的借券压力门控（0.7→0.8 阈值 + 对称出场 0.6→0.7）

- **Mechanism**: 胜绩的门控阈值是「费率分位 > 0.7 才进场」——即最差三成时间不持仓。收紧到 0.8 把门控变成「只在最差两成时间持仓」：若效应来自「借券压力极端时的强迫平仓」，极端子集会更纯；若效应来自「借券压力温和抬升时的渐进挤空」，收紧会削掉信号。这是门控**强度**的经济检验，不是数值微调（两侧阈值同时收紧保持对称性，避免引入新的不对称暴露）。
- **Fields**: `single_bucket_20day_return_estimate_ohlcv_img_2`, `rsk60_offer`, `cap`
- **Implementation Example**: `trade_when(and(rank(ts_mean(vec_avg(rsk60_offer), 5)) > 0.8, rank(cap) > 0.2), signed_power(subtract(group_rank(single_bucket_20day_return_estimate_ohlcv_img_2, country), 0.5), 0.5), or(rank(ts_mean(vec_avg(rsk60_offer), 5)) < 0.7, rank(cap) < 0.1))`
- **Direction**: 低分位 → long
- **Expected Exposure**: value
- **Expected Turnover Band**: low
- **Expected Coverage Band**: narrow
- **Why not crowded**: 门控子集收紧（持仓时间占比下降），分母不变；预期 prod 与 win 同源但自相关更低（持仓时段不同）。

**Concept**: 20 日 CNN × 借券压力门控 × 更大市值子集（cap 0.2→0.3，出场 0.1→0.05）

- **Mechanism**: 胜绩的子集条件是「只在大市值子集持仓」（rank(cap)>0.2），用来压集中权重。放宽到 0.3 会进一步抬高市值门槛、把持仓集中在流动性最好的头部，把 alpha 变成「大市值内的相对反转」；出场侧同步收紧到 0.05 保持进出对称。这条腿检验的是：效应是否只在**大盘股**上成立（若成立，说明它跟资金体量/机构持仓相关，而非零售驱动）。
- **Fields**: `single_bucket_20day_return_estimate_ohlcv_img_2`, `rsk60_offer`, `cap`
- **Implementation Example**: `trade_when(and(rank(ts_mean(vec_avg(rsk60_offer), 5)) > 0.7, rank(cap) > 0.3), signed_power(subtract(group_rank(single_bucket_20day_return_estimate_ohlcv_img_2, country), 0.5), 0.5), or(rank(ts_mean(vec_avg(rsk60_offer), 5)) < 0.6, rank(cap) < 0.05))`
- **Direction**: 低分位 → long
- **Expected Exposure**: value
- **Expected Turnover Band**: low
- **Expected Coverage Band**: narrow
- **Why not crowded**: 换的是持仓宇宙（分位门槛）而非信号；预期 prod 同源、自相关下降。

**Concept**: 20 日 CNN × 借券压力门控 · 信号改用 industry 分母（换信号分母轴）

- **Mechanism**: 胜绩的信号腿用 country 轴分位（每个国家内部比较 20 日 CNN 预测分位）。换成 industry 轴：此时比较的是「同一行业内不同公司的预测分位高低」，把国家级共同成分（国家资金流/宏观）从分母里去掉。GLB 规则「同族 prod 撞墙时先查是不是同分母；换分母破 SELF 墙，换分子没用」——这条腿就是换分母。
- **Fields**: `single_bucket_20day_return_estimate_ohlcv_img_2`, `rsk60_offer`, `cap`
- **Implementation Example**: `trade_when(and(rank(ts_mean(vec_avg(rsk60_offer), 5)) > 0.7, rank(cap) > 0.2), signed_power(subtract(group_rank(single_bucket_20day_return_estimate_ohlcv_img_2, industry), 0.5), 0.5), or(rank(ts_mean(vec_avg(rsk60_offer), 5)) < 0.6, rank(cap) < 0.1))`
- **Direction**: 低分位 → long
- **Expected Exposure**: value
- **Expected Turnover Band**: low
- **Expected Coverage Band**: medium
- **Why not crowded**: 分母从 country 换 industry，属 GLB 破墙规则允许的「换分母」；同族自相关应明显下降，prod 与 win 指纹不同。
