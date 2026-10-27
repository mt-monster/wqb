**Dataset**: intraday_pv_feats
**Region**: GLB
**Delay**: 1
**Universe**: TOPDIV3000

# GLB wave72 · intraday_pv_feats 定向概念（手写 ideas · source=manual）

> 依据 `Claude/skills/wq-brain-ra-glb/references/pv.md` 组合卡：
> ① **用**——尾盘 30 分钟反转，只用 `ts_decay_linear(x, 5)`，high-price 路径能过 EMEA 子宇宙；
> ② **避**——`mean_last_trade_price_return_30m_pre_close_2`（last_trade 快骨架 EMEA 墙）、
> `corr_*_with_slippage` 族（换手墙）、60m 路径（2Y 墙）、post_open/first_half/skew 族（第三机制已穷尽）；
> ③ 本波**禁两两混腿**（用户 2026-10-27 定案）⇒ 每个概念单字段、单信号腿；
> ④ **ATOM 优先** ⇒ 只用本集字段 + 6 个豁免分组键（country/exchange/market/sector/industry/subindustry），
> 不用任何非豁免分组键（pv30 的 `pca_industry_grouping_method*` 等一律不进本波）；
> ⑤ 时间窗口只用白名单标准窗 5 / 22 / 66。
>
> 拥挤度依据（平台 userCount / alphaCount 实测）：
> `mean_high_price_return_30m_pre_close_2` ac=95（最挤，prod 墙风险）·
> `mean_low_price_return_30m_pre_close_2` ac=2 ·
> `mean_ask_vwap_ratio_30m_pre_close_2` ac=1 ·
> `mean_bid_ask_size_ratio_30m_pre_close_2` ac=低 ·
> `mean_trade_volume_30m_pre_close_2` ac=1（field_type=scale）。

## 字段（Fields）

| Field ID | Type | Coverage | Role |
|---|---|---|---|
| `mean_high_price_return_30m_pre_close_2` | MATRIX | 0.9982 | 主信号 |
| `mean_low_price_return_30m_pre_close_2` | MATRIX | 0.9982 | 主信号 |
| `mean_ask_vwap_ratio_30m_pre_close_2` | MATRIX | 0.9976 | 主信号 |
| `mean_bid_ask_size_ratio_30m_pre_close_2` | MATRIX | 0.99 | 主信号 |
| `mean_trade_volume_30m_pre_close_2` | MATRIX | 0.9989 | 主信号 |

## 特征（Features）

- 预处理：`group_zscore(..., country)` 做截面国家内中性化（豁免分组轴，保 ATOM）；`ts_decay_linear(x, 5)` 记忆尾盘冲击；`ts_mean(x, 22)` 做月度尺度平滑。
- 不做：`ts_std_dev` / `ts_max_diff`（类别卡禁用于此类日内字段）、`ts_entropy` / `ts_skewness`（幽灵算子）。
- 不用任何加权和 / `add(rank(A), rank(B))` 式两腿混合。

## 建议（Implementation Examples）

- ipv_high_preclose_country_reversal: `group_zscore(ts_decay_linear({mean_high_price_return_30m_pre_close_2}, 5), country)`
- ipv_low_preclose_country_reversal: `group_zscore(ts_decay_linear({mean_low_price_return_30m_pre_close_2}, 5), country)`
- ipv_ask_vwap_spread_efficiency: `group_zscore(ts_mean({mean_ask_vwap_ratio_30m_pre_close_2}, 22), country)`
- ipv_bid_ask_size_imbalance: `group_zscore(ts_mean({mean_bid_ask_size_ratio_30m_pre_close_2}, 22), country)`
- ipv_preclose_volume_shock: `group_zscore(ts_delta(ts_mean({mean_trade_volume_30m_pre_close_2}, 22), 5), country)`

## 字段白名单（Field Whitelist）

```
mean_high_price_return_30m_pre_close_2
mean_low_price_return_30m_pre_close_2
mean_ask_vwap_ratio_30m_pre_close_2
mean_bid_ask_size_ratio_30m_pre_close_2
mean_trade_volume_30m_pre_close_2
```

## Concepts

**Concept**: 尾盘 30 分钟最高价路径反转（country 轴，快骨架）

- **Mechanism**: 收盘前 30 分钟内以最高价成交路径衡量的收益，捕捉尾盘买盘冲击；该冲击在多国市场多为短期流动性事件而非信息事件，country 轴中性化后应反向持有。GLB 本地胜绩 GLB-IPV-PRECLOSE-HIGH-FAST-COUNTRY-WIN 即此形态（能过 EMEA 子宇宙）。
- **Fields**: `mean_high_price_return_30m_pre_close_2`
- **Implementation Example**: `group_zscore(ts_decay_linear({mean_high_price_return_30m_pre_close_2}, 5), country)`
- **Direction**: High → short
- **Expected Exposure**: reversal
- **Expected Turnover Band**: medium
- **Expected Coverage Band**: wide
- **Why not crowded**: 该字段平台 alphaCount=95 是本集最挤的一条，裸用有 prod 墙风险；本概念靠 country 轴 + 5 日衰减把信号变成「国家内的尾盘买盘相对强弱」，与同族 last_trade 路径（已判死 EMEA 墙）在字段与骨架上均不同。

**Concept**: 尾盘 30 分钟最低价路径反转（country 轴，同机制镜像腿）

- **Mechanism**: 以最低价成交路径衡量的尾盘收益，捕捉尾盘卖压冲击；卖压极端同样多为短期流动性事件，应反向持有。与 high-price 概念互为镜像，但使用完全不同的字段，避开最拥挤的那条。
- **Fields**: `mean_low_price_return_30m_pre_close_2`
- **Implementation Example**: `group_zscore(ts_decay_linear({mean_low_price_return_30m_pre_close_2}, 5), country)`
- **Direction**: Low → long
- **Expected Exposure**: reversal
- **Expected Turnover Band**: medium
- **Expected Coverage Band**: wide
- **Why not crowded**: 该字段平台 alphaCount=2、userCount=1，接近处女地；同族只有 high-price 一条被大量使用（ac=95），本腿无拥挤风险。GLB × pv 组合卡的判死清单未覆盖 low-price 路径。

**Concept**: 尾盘 30 分钟卖价相对 VWAP 的价差（价格效率 / 流动性）

- **Mechanism**: 卖价与 VWAP 的比值衡量尾盘卖方定价相对当日均价的位置；持续高于 VWAP 说明尾盘买盘薄、价差宽，通常对应承压的微观结构状态，做空该状态。
- **Fields**: `mean_ask_vwap_ratio_30m_pre_close_2`
- **Implementation Example**: `group_zscore(ts_mean({mean_ask_vwap_ratio_30m_pre_close_2}, 22), country)`
- **Direction**: High → short
- **Expected Exposure**: liquidity
- **Expected Turnover Band**: low
- **Expected Coverage Band**: wide
- **Why not crowded**: 该字段平台 userCount=1、alphaCount=1，且与已判死的 `corr_*_with_slippage` 换手墙族不是同一字段；比率型字段在 PV 类别卡里属「price efficiency」原语，本区尚无实证。

**Concept**: 尾盘 30 分钟买卖盘量不对称（订单簿失衡）

- **Mechanism**: 买卖报价量的比例刻画尾盘订单簿的失衡方向；卖盘占优时短期承压，买盘占优时短期修复，故以卖压端为做空方向。与价差概念是不同经济量（量 vs 价），不是同一信号的两个写法。
- **Fields**: `mean_bid_ask_size_ratio_30m_pre_close_2`
- **Implementation Example**: `group_zscore(ts_mean({mean_bid_ask_size_ratio_30m_pre_close_2}, 22), country)`
- **Direction**: Low → short
- **Expected Exposure**: liquidity
- **Expected Turnover Band**: low
- **Expected Coverage Band**: wide
- **Why not crowded**: 本集 30m pre_close 族里几乎无人使用该字段（平台使用数个位数），且它是「订单簿量」而非「价格」信息，与已判死的收盘区间微观结构族（last/vwap close-location）不是同一形态。

**Concept**: 尾盘 30 分钟成交量冲击（量能相对历史均值的变化）

- **Mechanism**: 尾盘 30 分钟均量相对过去 22 日均量的变化，度量资金在收盘前的异常涌入或撤离；PV 类别卡把「liquidity shock: volume spike vs historical average」列为独立原语，异常放量往往是次日流动性事件的先行指标。
- **Fields**: `mean_trade_volume_30m_pre_close_2`
- **Implementation Example**: `group_zscore(ts_delta(ts_mean({mean_trade_volume_30m_pre_close_2}, 22), 5), country)`
- **Direction**: High → long
- **Expected Exposure**: liquidity
- **Expected Turnover Band**: medium
- **Expected Coverage Band**: wide
- **Why not crowded**: 该字段平台 alphaCount=4、userCount=1，且是 scale 型字段（推荐算子 rank/ts_mean/group_scale），本概念只用本集字段，不引入 pv1 的 `volume`（那会变双数据集、破坏 ATOM）。
