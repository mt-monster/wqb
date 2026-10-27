**Dataset**: intraday_pv_feats
**Region**: GLB
**Delay**: 1
**Universe**: MINVOL1M

# GLB wave77 · intraday_pv_feats 尾盘 30m 高价路径反转（定向）

> 依据 `Claude/skills/wq-brain-ra-glb/references/pv.md`：
> ① **用**——尾盘 30 分钟反转，只用 `ts_decay_linear(x, 5)`，**high-price 路径能过 EMEA 子宇宙**；
> ② **避**——last_trade 快骨架（9 种中性化下 EMEA 全败，0.58–0.93）、60m 路径（2Y 墙）、
>    corr_*_with_slippage 族（换手墙）、post_open/first_half/skew 族（第三机制已穷尽）。
> ③ 已提交 ACTIVE 实证 **mLmxKN12**：`-1.0*group_zscore(ts_decay_linear(mean_high_price_return_30m_pre_close_2, 5), country)`
>    档位 MINVOL1M/decay6/SUBINDUSTRY/trunc0.02，failed_ra_count=0、prod 0.694、self 0.2823、2Y 2.92、sub 1.94。
>    ⇒ 本波基线即此形态，其后各条**只改一个旋钮**（换轴 / 换窗 / 换几何 / 换价差分母），
>    走「机制换腿」而非参数扫描，不克隆基线。
> ④ **ATOM 约束**：只用本集字段 + 6 个豁免分组键（country/exchange/market/sector/industry/subindustry），
>    不引入第二个数据集的字段。
> ⑤ 已生效档位：`cells.json:pv:intraday_pv_feats` 覆盖（MINVOL1M / SUBINDUSTRY / decay 6 / trunc 0.02）。

## 字段（Fields）

| Field ID | Type | Coverage | Role |
|---|---|---|---|
| `mean_high_price_return_30m_pre_close_2` | MATRIX | 0.9982 | 主信号 |
| `mean_ask_price_return_30m_pre_close_2` | MATRIX | 0.9972 | 主信号（价差分子） |
| `mean_bid_price_return_30m_pre_close_2` | MATRIX | 0.9972 | 主信号（价差分子） |
| `mean_vwap_return_30m_pre_close_2` | MATRIX | 0.9982 | 主信号（价差分母） |

## 特征（Features）

- 预处理：`ts_decay_linear(x, 5)`（组合卡指定记忆长度）；`group_zscore / group_rank` 做截面中性化；`ts_mean(x, 22)` 作变体的时间聚合。
- 不做：`ts_std_dev` / `ts_max_diff`（类别卡禁用于此类日内字段）、`ts_entropy` / `ts_skewness`（幽灵算子）、`ts_event_*`（平台没有）。

## 建议（Implementation Examples）

- ipv_high_country_d5: `-1.0*group_zscore(ts_decay_linear({mean_high_price_return_30m_pre_close_2}, 5), country)`
- ipv_high_industry_d5: `-1.0*group_zscore(ts_decay_linear({mean_high_price_return_30m_pre_close_2}, 5), industry)`
- ipv_high_country_d10: `-1.0*group_zscore(ts_decay_linear({mean_high_price_return_30m_pre_close_2}, 10), country)`
- ipv_high_country_grouprank: `-1.0*group_rank(ts_decay_linear({mean_high_price_return_30m_pre_close_2}, 5), country)`
- ipv_high_ask_vwap_spread: `-1.0*group_zscore(ts_decay_linear(subtract({mean_ask_price_return_30m_pre_close_2}, {mean_vwap_return_30m_pre_close_2}), 5), country)`
- ipv_high_bid_vwap_spread: `-1.0*group_zscore(ts_decay_linear(subtract({mean_bid_price_return_30m_pre_close_2}, {mean_vwap_return_30m_pre_close_2}), 5), country)`

## 字段白名单（Field Whitelist）

```
mean_high_price_return_30m_pre_close_2
mean_ask_price_return_30m_pre_close_2
mean_bid_price_return_30m_pre_close_2
mean_vwap_return_30m_pre_close_2
```

## Concepts

**Concept**: 尾盘 30m 高价路径反转 · country 轴 · 5 日衰减（基线复现已提交机制）

- **Mechanism**: 收盘前 30 分钟以最高价成交路径衡量的收益，捕捉尾盘买盘冲击；该冲击多为短期流动性事件而非信息事件，country 轴中性化后反向持有。GLB 已提交 ACTIVE alpha mLmxKN12 即此形态（failed_ra_count=0，prod 0.694，self 0.2823）。
- **Fields**: `mean_high_price_return_30m_pre_close_2`
- **Implementation Example**: `-1.0*group_zscore(ts_decay_linear({mean_high_price_return_30m_pre_close_2}, 5), country)`
- **Direction**: High → short
- **Expected Exposure**: reversal
- **Expected Turnover Band**: high
- **Expected Coverage Band**: wide
- **Why not crowded**: 字段 alphaCount=95 属热门，但 country 轴 + 5 日衰减这一具体形态的 prod 只有 0.694，余量极薄 —— 本波基线取它是为了复现已验证形态并以「换轴/换窗/换几何」三条邻域腿扩产，不是同骨架参数扫描。

**Concept**: 尾盘 30m 高价路径反转 · industry 轴 · 5 日衰减（换分组轴）

- **Mechanism**: 把同一尾盘买盘冲击信号放到行业轴中性化：若冲击来自公司特有事件，行业内相对强者更可能是事件驱动、均值回归空间更大；若冲击来自行业级资金流，行业轴会把共同成分中性化掉、只留个股残差。两种分母对应两种经济解释，prod 撞墙时「换分母」是 GLB 已验证的破 SELF/prod 墙手段。
- **Fields**: `mean_high_price_return_30m_pre_close_2`
- **Implementation Example**: `-1.0*group_zscore(ts_decay_linear({mean_high_price_return_30m_pre_close_2}, 5), industry)`
- **Direction**: High → short
- **Expected Exposure**: reversal
- **Expected Turnover Band**: high
- **Expected Coverage Band**: wide
- **Why not crowded**: 与基线同字段但分母不同（行业 vs 国家），是分母维度的结构性差异而非参数变体；GLB×pv 卡记载该族在 9 种中性化下均产出过 prod 干净 alpha。

**Concept**: 尾盘 30m 高价路径反转 · country 轴 · 10 日衰减（换记忆长度）

- **Mechanism**: 组合卡指定 ts_decay_linear(x, 5)，其含义是「只记近 5 日的尾盘冲击记忆」。把衰减拉到 10 日，等于把信号定义为「近两周持续的尾盘买盘倾向」而非「单日冲击」——若原始效应是持续性的（资金持续进场），更长记忆会放大强度；若是一次性冲击，更长记忆会稀释它。这是同一经济量的时间尺度检验。
- **Fields**: `mean_high_price_return_30m_pre_close_2`
- **Implementation Example**: `-1.0*group_zscore(ts_decay_linear({mean_high_price_return_30m_pre_close_2}, 10), country)`
- **Direction**: High → short
- **Expected Exposure**: reversal
- **Expected Turnover Band**: medium
- **Expected Coverage Band**: wide
- **Why not crowded**: 换时间尺度不改变分母与字段，prod 画像与基线同族（基线 prod 0.694 已贴线），故预期 prod 同源、需要靠 2Y/子宇宙表现区分。

**Concept**: 尾盘 30m 高价路径反转 · country 轴 · group_rank 几何（换归一化算子）

- **Mechanism**: group_zscore 对尾部极值敏感（单个极端尾盘冲击会主导 zscore），group_rank 只看截面序、不受极值幅度影响。若尾盘买盘冲击的强度信息本身携带信号（强冲击更可能反转），zscore 优于 rank；若强度只是噪声而序有用，rank 优于 zscore。两者经济含义不同，不是数值微调。
- **Fields**: `mean_high_price_return_30m_pre_close_2`
- **Implementation Example**: `-1.0*group_rank(ts_decay_linear({mean_high_price_return_30m_pre_close_2}, 5), country)`
- **Direction**: High → short
- **Expected Exposure**: reversal
- **Expected Turnover Band**: high
- **Expected Coverage Band**: wide
- **Why not crowded**: 换的是归一化几何（分布稳健性），属「等价算子替换」允许方向；且不引入第二数据集，仍是 ATOM。

**Concept**: 尾盘 30m 卖价路径 − VWAP 路径价差 · country 轴（换价差分母）

- **Mechanism**: 高价路径的收益里混着「整段尾盘的上行幅度」与「卖方定价相对当日均价的抬升」两种成分。用卖价路径收益减去 VWAP 路径收益，把「尾盘整体上涨」扣掉，只留「卖方定价相对均价走强」——后者是资金愿意在尾盘抬价接货的证据，属更纯粹的订单流含义。
- **Fields**: `mean_ask_price_return_30m_pre_close_2`, `mean_vwap_return_30m_pre_close_2`
- **Implementation Example**: `-1.0*group_zscore(ts_decay_linear(subtract({mean_ask_price_return_30m_pre_close_2}, {mean_vwap_return_30m_pre_close_2}), 5), country)`
- **Direction**: High → short
- **Expected Exposure**: reversal
- **Expected Turnover Band**: high
- **Expected Coverage Band**: wide
- **Why not crowded**: 价差为同一数据集内两字段相减（成本价差，非两腿加权混合），不破 ATOM；与基线相比换的是分母口径（VWAP 而非高价），属 GLB 规则允许的「换分母」破墙方向。

**Concept**: 尾盘 30m 买价路径 − VWAP 路径价差 · country 轴（买侧价差）

- **Mechanism**: 与上一条对称，用买价路径而非卖价路径与 VWAP 相减：买价相对均价走强说明买方在尾盘主动抬价，含义与卖价相对均价走强相反，两者不是同一信号的换算。分开测可判断订单流方向信号到底由哪一侧驱动。
- **Fields**: `mean_bid_price_return_30m_pre_close_2`, `mean_vwap_return_30m_pre_close_2`
- **Implementation Example**: `-1.0*group_zscore(ts_decay_linear(subtract({mean_bid_price_return_30m_pre_close_2}, {mean_vwap_return_30m_pre_close_2}), 5), country)`
- **Direction**: High → short
- **Expected Exposure**: reversal
- **Expected Turnover Band**: high
- **Expected Coverage Band**: wide
- **Why not crowded**: 与基线同族但换成买侧价差分子，同数据集内相减，仍是 ATOM；预期与卖侧价差腿 prod 接近但相关性更低（同族一次只提 1 颗的纪律适用）。
