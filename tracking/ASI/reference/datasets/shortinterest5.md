# shortinterest5 探针结论（ASI / MINVOL1M / D1）

> 战役：ASI/D1 Power Pool Dec'26。塔位 SHORTINTEREST **0/3 未点亮**（2026-11-23 实读）。
> 数据集：shortinterest5「Daily Price Limit Data」，cov 0.9624，3 字段，pyramid 1.3x。
> 实际内容：**涨跌停板制度数据**（沪深港，CSI 300 成分）—— 名字叫 shortinterest 但机制是 price limit（数据集名≠内容，第 2 例）。

## 字段全表（3/3）

| 字段 | 类型 | cov | ac | 语义 |
|---|---|---|---|---|
| `max_price_decrease_ratio` | MATRIX | 0.9624 | 125 | 每日跌停幅度比例（按交易所规则） |
| `max_price_increase_ratio` | MATRIX | 0.9624 | 119 | 每日涨停幅度比例 |
| `price_limit_condition` | MATRIX | 0.9624 | 82 | 当前可交易状态编码（正常/涨停/跌停/停牌），需 codebook |

## 探针实测（4 臂，全部零持仓）

| # | 表达式 | S | TO | longCount | shortCount |
|---|---|---|---|---|---|
| 1 | `group_rank(max_price_decrease_ratio, market)` | 0.0 | 0.0 | **0** | **0** |
| 2 | `group_rank(subtract(max_price_increase_ratio, max_price_decrease_ratio), market)` | 0.0 | 0.0 | **0** | **0** |
| 3 | `group_rank(price_limit_condition, country)` | 0.0 | 0.0 | **0** | **0** |
| 4 | `group_rank(ts_delta(price_limit_condition, 5), country)` | 0.0 | 0.0 | **0** | **0** |

## 判定：**数据层排除**（非信号层死）

**根因分析**：
1. **幅度类字段是制度常数**：`max_price_decrease_ratio` 按交易所/板块统一定义（沪深主板 10%、创业板/科创板 20%、ST 5% 等），**同一市场内所有股票同值** ⇒ 组内 rank 恒 0.5 ⇒ 建不出多空。用户的推理被 4 臂实测证实：0/0 持仓。
2. **状态字段也零持仓**：`price_limit_condition` 在有意义的日频截面上同样产出 0 仓 ⇒ 该字段在 ASI/MINVOL1M 实际无可区分取值（可能全为「正常」默认值，或 data 本身未落地）。
3. cov 0.9624 是**名义覆盖率**（平台 coverage 口径已知偏差），不代表有效数值。

⇒ 按用户红线：**记为数据层排除（PROVISIONAL）**，不写数据集死键。理由写明「制度参数+状态字段在 ASI 无截面可区分取值」。

## 证据（论坛 + 论文，5 篇 diverse）
- `Investor attention, aggregate limit-hits, and stock returns` (2022, DOI 10.1016/j.irfa.2022.102265)
- `The intraday stock return characteristics surrounding price limit hits` (2004, DOI 10.1016/j.mulfin.2004.02.004)
- **`Empirical Analysis of Price Limit Hits of Tokyo Stock Exchange`** (2009, DOI 10.2139/ssrn.1471222) — 证明日本有涨跌停制度（但本数据集未落 JPN 数值）
- `Trading aggression when price limit hits are imminent: magnet effect` (2018, DOI 10.1016/j.jbef.2018.01.007)
- `Forecasting Volatility with Price Limit Hits` (2018, DOI 10.1080/1540496x.2018.1532888)

论坛：`45145781788311`（HKG Tips，12 赞）明确指出 **"HKG does not need a limit-status setup"** —— 与本观测一致：涨跌停状态在港股/亚洲不构成可交易信号。

## 可复用教训

**制度参数（regulatory constants）不可作截面信号**：
- 判定方法：先跑 1 臂 `group_rank(field, market)` 看 longCount/shortCount。若为 0 ⇒ 全市场常数。
- 这类字段只可能有两种用法：① 当**分组/门控变量**（把不同制度股票分开）；② 与价格信号交互（如 `trade_when(limit_up, ..., -1)`）——但前提是该状态字段有真实日频取值（本例实测为 0 仓，不成立）。

## 塔位影响
SHORTINTEREST 塔（1.3x）在 ASI **仅此 1 个数据集**且数据层排除 ⇒ **该塔在 ASI 结构性不可点亮**（无其它数据集可选）。这与「已点亮塔不投」无关，是「唯一数据集无有效数据」。
