# analyst45 Feature Engineering Analysis Report

**Dataset**: analyst45
**Region**: EUR
**Delay**: 1

- **Dataset**: `analyst45`
- **Category**: `analyst`
- **Region**: `EUR`
- **Delay**: `1`
- **Universe**: `TOP2500`
- **Fields Analyzed**: 61

---

## 数据集画像（2026-09-11）

分析师想法/投资组合表现数据集，61 个 VECTOR 字段，coverage 1.0。
信号核心：分析师想法的超额收益表现（Jensen's alpha / 相对指数超额 / 日均相对收益）。
注意 anl45_net_market_exposure(users58)/current_inv(users28) 已超 prod_corr 分级线，
只做方向验证；优先 users 0-9 冷门字段（jensensalpha/rel_index_ret_per/ad_rel_ret_per）。
全部 VECTOR 字段必须先 vec_* 聚合。

## GEM 兼容模板（Concept Blocks）

> 分析师想法表现信号：机制 → 具体字段 → 一个实现。占位符用字段族后缀。

**Concept**: Jensen's alpha 超额（风险调整表现）
- **Mechanism**: 分析师想法的风险调整超额收益，高 alpha=分析师真有能力→long
- **Fields Used**: `anl45_jensensalpha`
- **Implementation Example**: `rank(ts_mean(vec_avg({anl45_jensensalpha}), 66))`
- **Direction**: High → long

**Concept**: 相对指数超额（跑赢基准）
- **Mechanism**: 想法相对基准指数的超额收益，持续跑赢=信号→long
- **Fields Used**: `anl45_rel_index_ret_per`
- **Implementation Example**: `rank(ts_mean(vec_avg({anl45_rel_index_ret_per}), 66))`
- **Direction**: High → long

**Concept**: 日均相对收益动量（idea 表现动量）
- **Mechanism**: 想法日均相对收益的时间序列动量，表现改善→long
- **Fields Used**: `anl45_ad_rel_ret_per`
- **Implementation Example**: `rank(ts_delta(vec_avg({anl45_ad_rel_ret_per}), 22))`
- **Direction**: High → long

**Concept**: Jensen's alpha 行业内相对（group_rank）
- **Mechanism**: alpha 在行业内相对定位，剥离行业分析师覆盖差异
- **Fields Used**: `anl45_jensensalpha`
- **Implementation Example**: `group_rank(ts_mean(vec_avg({anl45_jensensalpha}), 66), subindustry)`
- **Direction**: High → long

**Concept**: 超额收益 zscore 离群（截面异常）
- **Mechanism**: 相对指数超额截面 zscore，识别异常强的分析师想法
- **Fields Used**: `anl45_rel_index_ret_per`
- **Implementation Example**: `rank(zscore(vec_avg({anl45_rel_index_ret_per})))`
- **Direction**: High → long

**Concept**: 想法年龄调整超额（days_since 加权）
- **Mechanism**: 年轻想法的超额更有信息量（未被市场消化），年龄衰减加权
- **Fields Used**: `anl45_rel_index_ret_per`, `anl45_days_since_inception`
- **Implementation Example**: `rank(vec_avg({anl45_rel_index_ret_per}) - vec_avg({anl45_days_since_inception}))`
- **Direction**: High → long

## 字段白名单（Field Whitelist）

```
anl45_jensensalpha
anl45_rel_index_ret_per
anl45_ad_rel_ret_per
anl45_rel_ret_per_today
anl45_tot_ret_per
anl45_days_since_inception
anl45_avg_dur
```
