# risk72 — KOR/D1 字段画像（2026-10-30 建）

> 数据来源：`get_datafields(dataset_id="risk72", region="KOR", universe="TOP600", delay=1, filter_sharpe=false)`
> ⇒ **平台仅 5 个字段，全部 MATRIX**，description **逐字相同**：「Daily reproducible specific returns in % units」。
> 塔位：**risk**（KOR/D1 未点亮，倍率 1.3）。

## 1. 字段全表（平台实测）

| # | field | 类型 | cov | aC | userCount | 宇宙口径（从字段名解出） |
|---|---|---|---|---|---|---|
| 1 | `rsk72_eqy_asi_supported_minvol1m_dsrt` | MATRIX | **0.7592** | 89 | 44 | ASI **min-vol 1m** 支持集（去极端高波股） |
| 2 | `rsk72_eqy_xjpci_supported_minvol1m_dsrt` | MATRIX | **0.7592** | 92 | 41 | xjpci（含日经成分域？vendor 内部口径）**min-vol 1m** |
| 3 | `rsk72_asi_top2000_eqy_dsrt` | MATRIX | 0.7085 | **131** | 87 | ASI TOP2000 |
| 4 | `rsk72_asi_top1500_eqy_dsrt` | MATRIX | 0.5426 | 82 | 35 | ASI TOP1500 |
| 5 | `rsk72_asi_top1000_eqy_dsrt` | MATRIX | 0.3534 | 89 | 33 | ASI TOP1000 |

**同名同义的 5 份拷贝**：分子公式、单位（%）、频率（日）全部一致，**唯一差别是计算时用的宇宙**。
⇒ 跨字段相关性预计 **>0.9**（同一残差在不同宇宙里重算）；**不能当 5 个独立信号用**（会自相撞 self-corr）。

## 2. 名 vs description 差异表（0.2 纪律）

| 差异 | 事实 | 下游后果 |
|---|---|---|
| **description 完全不区分宇宙** | 5 条 description 逐字相同，只写「Daily reproducible specific returns in % units」 | 按 description 分类会把 5 条看成**同一个字段的重复**（部分正确），而**丢失了「宇宙」这个唯一变量** ⇒ 必须按字段名解出宇宙档位 |
| **名字里的 `eqy` / `supported` / `minvol1m` 是无文档的 vendor 口径** | 平台未给宇宙定义的说明 | 不可据此推断「是否含 KOSPI 全成分」；只能**实测覆盖差**（.3534 → .7592 的梯度说明 minvol1m 口径覆盖最广） |
| `%` 单位 | `dsrt` 是百分数（不是小数） | 若与 decimal 字段（如 risk68 的 `residual_return`）直接相减必须**先统一单位**，否则量纲错 100 倍 |

## 3. 质量先验（0.1）

头部 = `rsk72_asi_top2000_eqy_dsrt`（aC 131 / userCount 87）。**但这不是新轴** —— 它是**最广覆盖档**，用户多只是因为它覆盖最高。
**本集没有独立经济轴**：5 个字段是**同一机制的 5 个宇宙快照**。

## 4. 五问（0.3）

| # | 问 | 答 |
|---|---|---|
| 1 时间维度 | 日频**流量**（每日残差收益），非存量 |
| 2 相对性 | 水平值（%），横截面可比 |
| 3 被定价的是谁 | 特质信息的**消化速度**（谁被过度反应、谁随后修正） |
| 4 有无博弈 | 有：残差反转是 KOR 已判死域，拥挤度中等（aC 82–131） |
| 5 事件性 | 非稀疏（每日都有值），但**信号本身是「昨日的残差」** ⇒ 天然短半衰期 |

## 5. 机制判定：**与已判死的 risk71 同族 ⇒ 0 槽**

| 判据 | 内容 |
|---|---|
| 同一量 | `dsrt` = **daily specific return**；risk71 的 `R`（MFM2 residual return）也是 daily specific return ⇒ **同一机制、同一被定价对象** |
| 已判死证据 | `KOR-RISK71-RESIDUAL-REVERSAL-2Y-DEAD`（wave 183/184）：`-ts_mean(R,5)` 逐年 S = 2016 **3.12** / 2018 **3.04** / 2020 **2.81** → 2022 **0.75** → 2023 **−1.21**；`-ts_zscore(R,22)` IS **2.20** 但 **2Y −0.92**；2Y 修法九种（inner industry neutralize / CROWDING / signed_power / REVERSION_AND_MOMENTUM / vol-gated / low-volume-gated / low-turnover-gated / turnover_sign_switch）**全部失效** |
| 死因性质 | **结构性符号翻转**（2022–2023：retail theme momentum + 2023-11 卖空禁令）⇒ 是**市场 regime 属性**，不是宇宙构造的产物 ⇒ **换宇宙档位不改变 regime** |
| 唯一「新」的东西 | 宇宙**差分**：`subtract(rank(top2000), rank(top1000))` = 同一股票在大小宇宙里残差排序的差 ⇒ 代理「该股在流动性/关注度分布中的位置」 |
| 为什么差分也不行 | 它本质是 **size / liquidity dispersion 暴露**，与 STATISTICAL 中性化正面对撞；且 risk 塔乘数仅 **1.3**，为一条 size 代理烧 2 槽不划算 |

## 6. 双通道取证

**通道 A（论坛）**：⚠ 待办。检索式 `"specific return"` / `"residual reversal"` / `"idiosyncratic"`。
**通道 B（论文）**：残差反转的经典依据（Lehmann 1990；Nagel 2012 的流动性机制）**已在 risk71 判死记录中用过**；
本区已用同一批机制做了 168+ 条实测并判死 ⇒ **不重复取证**（重复检索属于「已死轴」）。

**裁决**：B 有机制但**本区已证伪**；A 未取证**不改变结论**（证伪优先于「论坛有没有模板」）。

## 7. 十年覆盖验证

最短档 `top1000` cov 仅 **.3534** ⇒ 若真要开波，十年覆盖是硬风险（与本集「不投」的结论同向）。
`minvol1m` 两档 .7592 覆盖最好，但它们与 risk71 的宇宙口径几乎一致（minvol1m 也出现在 risk71 家族名里）。

## 8. 结论（写死，避免下一波重新论证）

⛔ **本集不投配额（0 槽）。** 三条理由按强度排序：
1. **机制已判死且死因与宇宙无关**（regime 级符号翻转）——投它就是违反铁律 F/G；
2. **5 个字段不是 5 个信号**，是同一量的 5 个宇宙拷贝 ⇒ 波次设计无从展开（「多腿」必撞 self-corr）；
3. 唯一残值（宇宙差分）是 size 代理，与 STATISTICAL 中性化对撞，乘数仅 1.3。

**若日后要翻案**，前提必须同时满足：① 提供 2024 年以后**新的 regime 证据**（卖空禁令解除 / 结构变化），
且 ② 用 `get_alpha_yearly_stats` 先证明 2023 之后符号已稳定 —— 否则不重开。

## 9. 禁区

- ⛔ 任何 `dsrt` 反转/动量形态（含 `ts_mean` / `ts_zscore` / 任何窗口）。
- ⛔ 5 个宇宙字段**两两组合当「多腿」**（同源拷贝，必撞 self-corr；且同源价差也仍是 size 代理）。
- ⛔ 与 risk68 的 `residual_return` 混用（单位 % vs decimal，且同机制）。

## 10. 实测记录

**无**（本集不投配额，故无回测记录）。本文件即「不投」的机器可核依据。
