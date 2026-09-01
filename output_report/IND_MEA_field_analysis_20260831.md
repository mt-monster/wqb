# IND / MEA 字段分析（重点 IND）

> 数据源：`data/wqb.db`　分析日期：2026-08-31  
> 指标来源：`alphas` 表（唯一可靠指标源）

---

## 0. 一句话结论

**IND 是一个"小池塘但水质好"的区域：564 个字段只开发了 5.1%，却已产出多条 sharpe≥2 的 alpha（全库最高产区之一）。但你 IND 的高分 alpha 几乎全靠"外部字段"（mdl238/anl9/fnd86/analyst_revision\_*），IND 本地字段表里 535 个字段几乎没被系统开采——这是最大的增量空间。**

MEA 对比：字段元数据完整、已重度开采（analyst7 一个数据集就 8,958 个 alpha），主战场已红海化。

---

## 1. 两区字段基本面

| 维度              | IND                           | MEA                   |
| --------------- | ----------------------------- | --------------------- |
| 字段总数            | **564**                       | 2,115                 |
| MATRIX / VECTOR | 515 / 49                      | 589 / 1,497           |
| 数据集数            | 25（多数 field_count=0 空壳）       | 18                    |
| 已用字段            | **29（5.1%）**                  | 165（7.8%）             |
| 数据集元数据完整度       | ⚠️ 几乎全空（category/coverage 未灌） | ✅ 完整                  |
| alpha 数         | 少而精（多条 S≥2）                   | 多而卷（analyst7=8,958 条） |
| universe        | TOP500                        | TOP400/TOP300         |
| neutralization  | STATISTICAL                   | SECTOR                |



> ⚠️ **数据卫生问题**：IND 的 datasets 表里 category/coverage/alpha_count 几乎全 NULL（后灌的），25 个数据集里 12 个 field_count=0 是空壳。**真实有字段的只有 13 个数据集**。字段级 coverage 是有的（在 fields 表），可信。

---

## 2. IND 已验证的高 sharpe 信号线（3 条）

### 线 A：pv106 交易成本/滑点【S=1.85 F=1.51，本地字段，最强本地信号】

```
group_rank(ts_mean(ts_backfill(divide(transaction_cost_maximum, transaction_cost_median),66),42), industry)
```

- 命中字段：`transaction_cost_maximum/median`、`pv106_wli_spreadbp`（cov≈1.0，全 IND 最高）
- **结构**：交易成本离散度（max/median 比率）→ 时序平滑 → 行业分组排名
- **意义**：这是 IND 唯一一条"纯本地字段"跑出来的高分 alpha，证明 pv106 数据集有真信号。
- **空间**：pv106 还有 **20 个高覆盖未开发字段**（asia_trade_cost、slippage\_*、bid_ask\_*、group_buy/sell_slippage），全部 cov≈1.0，可直接套用同一"离散度+分组排名"模板。

### 线 B：ern3 财报事件【S=1.71 F=2.10，fitness 最高】

- 命中字段：`ern3_next_interval`（距下次财报间隔，cov=0.71）
- **注意**：这条线实际是 **MEA 区域**跑出来的（regs=['MEA']），ern3 是跨区共享数据集。IND 本地 earnings3 只有 8 个字段。
- **意义**：财报临近/间隔是稳定事件信号，可作条件掩码叠加到其他信号上。

### 线 C：model207 内部人交易【S=1.29–1.40，3 字段全用了】

```
-rank(vec_avg(security_transaction_unit_price_usd))
add(multiply(-rank(vec_avg(security_transaction_unit_price_usd)),0.5), multiply(-ts_rank(...)))
```

- 命中字段：`security_transaction_unit_price_usd` / `transactional_share_quantity_change` / `post_transaction_share_balance`（cov=0.67）
- **意义**：内部人交易价格/数量是有效信号，但 cov 偏低（0.67），天花板有限。

---

## 3. IND 的"假象"：高分 alpha 大多不靠本地字段

IND sharpe TOP 的 alpha（S=2.59–2.88）用的核心字段**都不在 IND 的 fields 表里**：

| 外部字段                                                   | 出现  | 实际来源                 |
| ------------------------------------------------------ | --- | -------------------- |
| `mdl238_global_rank`                                   | ×11 | **EUR/USA 字段**（跨区引用） |
| `analyst_revision_percentile_score_medium_4`           | ×3  | 平台字段，本地未灌            |
| `analyst_recommendation_downgrades_30d_medium_*`       | ×5  | 平台字段，本地未灌            |
| `anl9_daily_numup/numdn/numnochg`                      | ×2  | 平台字段，本地未灌            |
| `fnd86_earnings_score/risk_score/price_momentum_score` | ×1  | 平台字段，本地未灌            |

**两个直接推论**：

1. **token-name 隐患在 IND 同样存在**：这些字段在表达式里能跑，但你本地的 IND fields 表里没有——说明它们要么是跨区共享字段，要么本地 catalog 没灌全。**用 IND 字段前必须先确认它在 IND 上下文真的可用**（跑一个单字段 `rank(field)` 探针）。
2. **IND 真正的本地增量在没碰的 535 个字段里**，尤其是下面这些数据集。

---

## 4. IND 未开发高覆盖字段：按 ROI 排序的开采清单

| 优先级 | 数据集               | 高覆盖未用字段 | 字段本质                                                                                 | 建议结构                                                                                           |
| --- | ----------------- | ------- | ------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------- |
| ★★★ | **analyst4**      | **111** | 分析师估计（eps/ebit/ebitda/sales/netprofit 的 high/low/mean/median/number + est vs preest） | **估计修正**：`ts_delta(mean,22)` 或 `divide(est, preest)-1`；**估计离散度**：`divide(high-low, abs(mean))` |
| ★★★ | **model28**       | **109** | 信用违约风险（pd_pct、distance_to_default、leverage、各国/行业/地区/板块 default_risk_percentile）      | 违约概率反向：`-rank(default_probability_one_year_pct)`；杠杆：`-rank(leverage_ratio_to_assets)`          |
| ★★☆ | **model36**       | 37      | 信用评分（star_sr\_*、credit_risk\_*\_score、letter_rating）                                 | `-rank(star_sr_leverage)`、`rank(star_sr_profitability)`                                        |
| ★★☆ | **model32**       | 36      | 动量评分（star_pm\_*、short/mid/long_horizon_momentum）                                     | 动量反转/顺势：`rank(mid_horizon_momentum_score_float)`                                               |
| ★★☆ | **fundamental94** | 30      | 季度基本面 PIT（fnd94_q\_*：资产/负债/销售/现金流）                                                   | 当分母/锚：`rank(X / fnd94_q_q_qta)`（总资产）                                                           |
| ★★☆ | **pv106**         | 20      | 交易成本/滑点扩展                                                                            | 复制线 A 模板                                                                                       |
| ★☆☆ | **risk70**        | 35      | 板块暴露（sector_exposure\_*）+ 对冲基金持仓                                                     | ⚠️ 多为暴露因子/flag，适合做中性化变量，不适合单独做信号                                                               |

### 重点说 analyst4（最大增量，111 个字段）

analyst4 是 IND 最厚的数据集（247 字段），而且结构和你已验证的"最强信号族"（分析师修正）完全同源：

- **估计 vs 先前估计配对**（revision 信号）：`anl4_dez1*_est` 与 `anl4_dez1*_preest` 成对存在 → `rank(divide(est, preest) - 1)` 就是分析师上修/下修。
- **high/low/mean/median 四件套**：可做**估计分歧度** `divide(subtract(high,low), abs(mean))`——分歧大=不确定性高，通常在财报前有效。
- **eps/ebit/ebitda/sales/netprofit 五指标** × 多周期 → 每个都能独立成 atom alpha（符合纪律②）。

> ⚠️ 注意 analyst4 里 VECTOR 字段很多（est/preest/actual 类），**直接用 `rank()`/`ts_delta()` 喂它们，不要包 `vec_avg()`**（skill 明确：vec\_* 是横截面算子，不是单股信号想要的）。

---

## 5. IND 字段处理策略（4 条）

1. **先验证字段可用性**：IND 高分 alpha 大量引用外部/未灌字段，本地表不全。任何字段先跑 `rank(field)` 单字段探针确认 IND 上下文可用，再进组合。
2. **MATRIX 字段直接进时序/排名算子**；**VECTOR 字段直接用 `rank`/`ts_*`，禁止 `vec_avg` 包裹**。
3. **基本面（fnd94）当锚不当信号**：套 `rank(X / fnd94_q_q_qta)` 或 `/market_cap`。
4. **信用/违约类（model28/36）是 IND 最独特的本地资源**：USA/GLB 的 book 全是价值/盈利/情绪族，**违约概率、distance_to_default、信用评分与现有生产 alpha 相关性天然低**——这是绕开 PROD_CORRELATION 硬闸的潜在突破口（你全库 prod_corr 主战场正缺低相关新信号族）。

---

## 6. MEA 对比（简版）

- MEA 字段元数据完整，主力数据集 analyst7（715 字段）/pv96/model25 已被高强度开采（单数据集数千 alpha）。
- MEA 已验证有效模式与全库一致：**分析师计数差**（subtract(up,down)）、**基本面比率**（rank(net_income/market_cap)）、**时序变化+长期 zscore 反向**。
- **结论**：MEA 是红海，新增 alpha 的边际收益低、prod_corr 风险高；IND 才是当前的蓝海增量区。

---

## 7. 立即可执行的下一步

1. **analyst4 估计修正族**：把 `dez1*_est / dez1*_preest` 配对 + 五指标 high/low/mean/median 展开成 atom alpha 批（预计 30–50 个变体），STATISTICAL 中性化，delay 用 1。
2. **model28/36 信用风险族**：`-rank(default_probability)`、`-rank(leverage)`、`rank(distance_to_default)` 各配窗口 22/66/252 → 验证是否低 prod_corr。
3. **pv106 交易成本扩展**：复制线 A 模板到剩余 20 个滑点字段。
4. 每族先跑 ≤10 个变体探针（你的纪律：10 种结构无效果才转向），过闸门再扩。
