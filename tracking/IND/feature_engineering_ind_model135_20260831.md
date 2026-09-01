# IND delay1 model135（Alternative Technical Factor Models）特征工程文档

- **数据集**: model135（技术指标库：动量/量能/波动/趋势/周期 5 轴 × 1-40 日多时间尺度，137 字段全 VECTOR，cov 0.7855）
- **区域/延迟/域**: IND / delay1 / TOP500；类目 Model（黄灯：alphaCount=5308 超阈，降为首探快判）
- **生成方式**: brain-data-feature-engineering skill（standalone）
- **日期**: 2026-08-31

---

## 1. 数据集理解（字段）

### 1.1 字段分类（字段画像）

| 轴 | 代表字段 | 含义 |
|---|---|---|
| 动量震荡 | mdl135_d{1..40}_isrs/isr（RSI/StochRSI）, willimsr_*, macd_*, triple_ema_rate_change_*（TRIX）, d*_oa（Awesome）, d*_os（Stoch）, d*_ou（Ultimate）, d*_ist（TSI） | 超买超卖/动量强度 |
| 量能资金流 | d*_fmc（Chaikin MF）, d*_ifm（MFI）, d*_lda（A/D Line）, d*_vbo（OBV）, d*_tpv（VPT）, d*_if（Force Index）, d*_ivn（NVI）, d*_vme（EOM）, d*_ovp（PVO） | 量价确认/资金进出 |
| 波动 | d*_bb（Bollinger）, d*_rta（ATR）, d*_im（Mass Index） | 波动区间/扩张 |
| 趋势强度 | d*_xda（ADX）, d*_iv（Vortex）, d*_icc（CCI） | 趋势存在性 |
| 周期 | d*_opd（DPO 去趋势）, mdl135_vlc（CLV 收盘位置） | 周期偏离 |
| 其他 | mdl135_mktcap（市值）, d*oc（复合一致指标）, d*ntr（区间回报）, gsubind（行业码-慎用） | 上下文 |

### 1.2 数据结构要点

- 全 VECTOR 类型但为**日频截面更新**（非事件稀疏）→ vec_avg 直聚 + ts_backfill(66) 标准流程。
- IND 量价/技术族已有三杀判死（ai_factor_transfer/intraday_pv_feats/behavioral_signals）→ 本集按**最小探针批快判**纪律执行：批 1 ≤8 条含反向对照，全 |S|<0.7 且无梯度即判死，不恋战。
- 指标已归一化（zscore）→ 直接 rank/quantile，不必再 winsorize。

## 2. 特征工程建议（探针优先）

**Concept**: Short Momentum Reversal（短动量反转，IND 反转风格）
- **Fields**: `mdl135_d3_isr`
- **Implementation Example**: `-rank(ts_backfill(vec_avg({mdl135_d3_isr}), 66))`
- **Direction**: Short overbought (long low RSI)

**Concept**: Money Flow Divergence（5日资金流方向）
- **Fields**: `mdl135_d5_fmc`
- **Implementation Example**: `quantile(ts_mean(ts_backfill(vec_avg({mdl135_d5_fmc}), 66), 21))`
- **Direction**: Long accumulation

**Concept**: Force Index Smoothed（量价合力）
- **Fields**: `mdl135_d5_if`
- **Implementation Example**: `group_rank(ts_mean(ts_backfill(vec_avg({mdl135_d5_if}), 66), 42), industry)`
- **Direction**: Long strong force

**Concept**: Volume Confirmation of Price（量能确认）
- **Fields**: `mdl135_d5_lda`
- **Implementation Example**: `quantile(ts_delta(ts_mean(ts_backfill(vec_avg({mdl135_d5_lda}), 66), 21), 21))`
- **Direction**: Long rising A/D

**Concept**: Volatility Compression（Bollinger 收窄后突破）
- **Fields**: `mdl135_d5_bb`
- **Implementation Example**: `-rank(ts_mean(ts_backfill(vec_avg({mdl135_d5_bb}), 66), 63))`
- **Direction**: Long compressed bands

**Concept**: Trend Strength Filtered Momentum（ADX 门控动量）
- **Fields**: `mdl135_d5_xda`, `mdl135_d5_iv`
- **Implementation Example**: `quantile(trade_when(ts_mean(ts_backfill(vec_avg({mdl135_d5_iv}), 66), 21), less(20, ts_backfill(vec_avg({mdl135_d5_xda}), 66)), nan))`
- **Direction**: Long uptrend strength when trend strong

**Concept**: Mid-term Momentum Persistence（20日动量持续）
- **Fields**: `mdl135_d02_isrs`
- **Implementation Example**: `group_rank(ts_mean(ts_backfill(vec_avg({mdl135_d02_isrs}), 66), 63), subindustry)`
- **Direction**: Long momentum

**Concept**: Cycle Detrend Reversion（去趋势周期回归）
- **Fields**: `mdl135_d62_opd`
- **Implementation Example**: `-rank(ts_backfill(vec_avg({mdl135_d62_opd}), 66))`
- **Direction**: Long below-trend (reversion)

## 3. 实现约束

1. 每条表达式只用 1-2 个字段；VECTOR 必包；正反向对照入批（判死纪律）。
2. 中性化：首轨 STATISTICAL（量价类无 analyst 族 SUBINDUSTRY 实证），分组骨架 industry 备轨。
3. 判死止损线：批 1 全 |S|<0.7 且窗口无梯度 → 判死入库。

## 4. 风险与局限

- IND 量价技术族三杀前科：本集先验概率偏低，探针批定生死。
- alphaCount=5308 拥挤：即使有信号，prod_corr 撞墙概率高。
