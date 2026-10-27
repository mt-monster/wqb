**Dataset**: intraday_pv_feats
**Region**: GLB
**Delay**: 1
**Universe**: MINVOL1M

# GLB wave78 · intraday_pv_feats 换经济量腿（定向挖掘 · PV 第三颗）

> **为什么换经济量而不是调参数**（2026-10-27 实测）：
> - last_trade 路径（`mean_last_trade_price_return_30m_pre_close_2`）在 10 条历史 alpha 上 prod 干净（0.45–0.65），
>   但**只差一闸 `LOW_GLB_EMEA_SHARPE`**，实测值 0.58–0.93（LLNlZKMa 0.62 / akbWK6V5 0.67 / 3qXn1rJN 0.89），
>   换窗（5↔10）、换轴（country/industry/sector）、换中性化（9 种）**均无法把它推过 1.0** ⇒ EMEA 墙对该路径是结构性的。
> - high-price 路径（`mean_high_price_return_30m_pre_close_2` + country + group_zscore）**prod 饱和**：该配方 12 条里 11 条撞 prod 墙
>   （唯一例外 mLmxKN12 已提交，prod 0.694 贴线）；换 group_rank / 换轴 / 换窗的腿另计（wave 77）。
> ⇒ 本波**换经济量**：在同一数据集内改用另外 3 条 30m 路径字段 + 1 条量能字段，
>   全部为 **prod 未撞墙的处女地字段**（平台 alphaCount 0–2），单数据集 + 豁免分组轴 ⇒ 仍是 ATOM。
> **已生效档位**：`cells.json:pv:intraday_pv_feats` 覆盖 = MINVOL1M / SUBINDUSTRY / decay 6 / trunc 0.02。

## 字段（Fields）

| Field ID | Type | 平台 alphaCount | 角色 | 说明 |
|---|---|---|---|---|
| `mean_low_price_return_30m_pre_close_2` | MATRIX | 2 | 主信号 | 尾盘**低价**成交路径收益；与 high-price 路径对称，但几乎无人用 |
| `mean_ask_price_return_30m_pre_close_2` | MATRIX | 6 | 主信号 | 尾盘**卖价**成交路径收益；卖方定价路径 |
| `mean_bid_price_return_30m_pre_close_2` | MATRIX | 22 | 主信号 | 尾盘**买价**成交路径收益；买方定价路径 |
| `mean_trade_volume_30m_pre_close_2` | MATRIX | 1 | 主信号 | 尾盘 30 分钟均量；类别卡「liquidity shock」原语的量能腿 |

## 特征（Features）

- 统一形态：`ts_decay_linear(x, 5)`（组合卡指定的记忆长度）+ `group_zscore(..., country)`（GLB 跨国宇宙，country 轴中性化有意义）。
- 不做：`ts_std_dev` / `ts_max_diff`（类别卡禁用于此类日内字段）、`ts_entropy` / `ts_skewness`（幽灵算子）、`ts_event_*`（平台没有）。
- 不引入第二个数据集的字段（`returns` / `cap` / `volume` 属 pv1 ⇒ 会破 ATOM）。

## 建议（Implementation Examples）

- ipv_low_path_country_d5: `-1.0*group_zscore(ts_decay_linear({mean_low_price_return_30m_pre_close_2}, 5), country)`
- ipv_ask_path_country_d5: `-1.0*group_zscore(ts_decay_linear({mean_ask_price_return_30m_pre_close_2}, 5), country)`
- ipv_bid_path_country_d5: `-1.0*group_zscore(ts_decay_linear({mean_bid_price_return_30m_pre_close_2}, 5), country)`
- ipv_volume_shock_country: `-1.0*group_zscore(ts_delta(ts_mean({mean_trade_volume_30m_pre_close_2}, 22), 5), country)`

## 字段白名单（Field Whitelist）

```
mean_low_price_return_30m_pre_close_2
mean_ask_price_return_30m_pre_close_2
mean_bid_price_return_30m_pre_close_2
mean_trade_volume_30m_pre_close_2
```

## Concepts

**Concept**: 尾盘 30m 低价路径反转 · country 轴

- **Mechanism**: 尾盘 30 分钟内以**最低价**成交路径衡量的收益。high-price 路径捕捉「尾盘买盘把价格推高」，其 prod 已饱和（12 条配方 11 条撞墙）；低价路径是同一时段的镜像读数——尾盘砸盘把价格打到新低。两者在几何上对称但**信息集不同**：低价路径的罕见被使用时，反映的是「尾盘卖压是否极端」，与「买盘是否极端」不是同一事件。该字段平台 alphaCount=2，prod 未撞墙。
- **Fields**: `mean_low_price_return_30m_pre_close_2`
- **Implementation Example**: `-1.0*group_zscore(ts_decay_linear({mean_low_price_return_30m_pre_close_2}, 5), country)`
- **Direction**: Low → long
- **Expected Exposure**: reversal
- **Expected Turnover Band**: high
- **Expected Coverage Band**: wide
- **Why not crowded**: 平台 alphaCount=2、userCount 极低；与已 prod 饱和的 high-price 配方不共享「字段+轴+归一化」指纹，prod-sat 闸不命中；同为 intraday_pv_feats 单数据集，ATOM 成立。

**Concept**: 尾盘 30m 卖价路径反转 · country 轴

- **Mechanism**: 用**卖方**成交路径的收益读尾盘压力。卖价路径反映的是「市场在尾盘愿意以什么价格出货」——卖价走强而均价不动，说明卖方在主动抬价出货（供给压力），属反转信号。这与 high/low 路径（成交极值）不同：它是**报价侧**而非成交侧的信息，alphaCount=6，prod 未撞墙。
- **Fields**: `mean_ask_price_return_30m_pre_close_2`
- **Implementation Example**: `-1.0*group_zscore(ts_decay_linear({mean_ask_price_return_30m_pre_close_2}, 5), country)`
- **Direction**: High → short
- **Expected Exposure**: reversal
- **Expected Turnover Band**: high
- **Expected Coverage Band**: wide
- **Why not crowded**: alphaCount=6、userCount 6，prod 未撞墙；与 high-price/last_trade 配方指纹不同（字段不同 ⇒ 饱和表不命中）。

**Concept**: 尾盘 30m 买价路径反转 · country 轴

- **Mechanism**: 与卖价路径对称，用**买方**成交路径读尾盘压力：买价走强说明买方在尾盘主动抬价扫货（需求压力），同样具短期反转含义。两条报价侧腿方向相反（卖价走强=出货、买价走强=扫货），可分别识别「供给冲击」与「需求冲击」两种尾盘形态——若两者一强一弱，则是纯粹的买卖价差扩大（流动性事件），与单侧走强含义不同。
- **Fields**: `mean_bid_price_return_30m_pre_close_2`
- **Implementation Example**: `-1.0*group_zscore(ts_decay_linear({mean_bid_price_return_30m_pre_close_2}, 5), country)`
- **Direction**: High → short
- **Expected Exposure**: reversal
- **Expected Turnover Band**: high
- **Expected Coverage Band**: wide
- **Why not crowded**: alphaCount=22、userCount 22，仍属低使用；prod 饱和表不含该字段。

**Concept**: 尾盘 30m 量能冲击（相对 22 日均量的变化）· country 轴

- **Mechanism**: 类别卡把「liquidity shock: volume spike vs historical average」列为 PV 独立原语：尾盘成交量相对近 22 日均量突然放大，说明尾盘出现了非日常的资金集中交易，次日更可能是流动性事件而非信息事件，故做反向。此腿测的是**量能**而非价格——与前三条价格路径腿的经济量完全不同，可用于分辨「EMEA 墙」是否来自价格路径的跨区不可比性（若是，量能腿的 EMEA 应明显更好）。
- **Fields**: `mean_trade_volume_30m_pre_close_2`
- **Implementation Example**: `-1.0*group_zscore(ts_delta(ts_mean({mean_trade_volume_30m_pre_close_2}, 22), 5), country)`
- **Direction**: High → short
- **Expected Exposure**: liquidity
- **Expected Turnover Band**: medium
- **Expected Coverage Band**: wide
- **Why not crowded**: 字段 alphaCount=1、userCount 1，处女地；用本集量能字段而非 pv1 的 `volume`，保住 ATOM。
