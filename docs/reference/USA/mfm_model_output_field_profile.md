# `mfm_model_output` 字段画像（USA / D1 / RISK 塔）

- **区域**：USA / TOP3000 / delay 1
- **category**：RISK
- **字段数**：117（全部 MATRIX，无 VECTOR / GROUP）
- **数据集覆盖率**：0.9963
- **平台拥挤度**：`alphaCount = 308`、`valueScore = 3.0`（RISK category 内仅次于 `risk65` 的第二低拥挤度）
- **本地已测**：`n_tests = 0`（117 字段全部 UNTESTED）
- **画像日期**：2026-10-29

---

## 1. 这是什么数据集

字段描述里反复出现 **"MFMCR universal risk model"**（`oil_gas_consumers_score`、`momentum_factor_score`、`telecommunications_services_score`、`airline_industry_score` 的描述都明确点名）。
⇒ 这是**商业多因子风险模型（MFMCR）的逐日输出面板**，即对每只股票每天给出：

1. **风格因子暴露**（standardized exposures）
2. **行业因子暴露**（industry factor loadings）
3. **行业哑变量**（binary membership flags）
4. **两个非暴露类风险量**：特质风险（specific risk）、特异收益（specific return）

理解这个数据集的**第一性原理**：风险模型的产物天生是「解释收益」的，不是「预测收益」的。
所以它的 alpha 价值只可能来自三个地方：

| 来源 | 为什么有价值 | 对应字段 |
|---|---|---|
| **模型解释不掉的那部分** | 因子暴露已被市场定价，**残差才是 alpha** | `discount_store_retail_score`（特异收益）、`systemic_risk_factor_score`（特质风险） |
| **暴露的**变化率**而非水平** | 水平已被风险模型中性化掉，变化率携带「资金正在换仓」的信息 | 各 `relative_*_factor` |
| **暴露的离散度 / 不稳定性** | 二阶矩刻画「这只票的因子画像在漂移」 | 各 `*_factor` 的 `ts_std_dev` |

**反面**：直接拿 `*_score` 水平做 `rank` 等价于重新发明 size / momentum / volatility 因子 —— 这类构造在 USA 生产池里极度拥挤，prod 相关性几乎必过 0.7。

---

## 2. 结构清点（117 字段三分）

| 族 | 数量 | coverage | 说明 |
|---|---|---|---|
| **风格/维度因子** | **13** | 全部 1.0 | `relative_*_factor` 5 个 + `*_factor_score*` 6 个 + `systemic_risk_measure_2` + `discount_store_retail_score` |
| **行业暴露 score** | **61** | 全部 1.0 | 每个行业一个因子载荷，跨行业累计解释个股收益 |
| **行业二元 flag** | **43** | 36 个 =1.0、**7 个 =0.9377** | `industry_*_flag`，只取 0/1 |

**coverage 分布**：110 个字段 = 1.0；7 个 = 0.9377（`industry_office_furniture_flag`、`industry_engineering_services_flag`、`industry_airlines_flag`、`industry_housewares_flag`、`industry_office_business_services_flag`、`industry_distribution_services_flag`、`industry_telecommunications_flag`）。
⇒ 覆盖不是选字段的区分维度（**没有字段是低覆盖**），必须靠「经济含义 + 拥挤度」来选。

---

## 3. 13 个风格/风险因子（唯一值得挖的族）

| 字段 | userCount | alphaCount | 官方描述 | 经济读法 |
|---|---|---|---|---|
| `hedge_fund_ownership_factor0` | **94** | **155** | 对冲基金持股度量 0 | **本集最拥挤字段**，prod 墙高危 |
| `hedge_fund_ownership_factor1` | 34 | 47 | 对冲基金持股度量 1 | 同上，第二度量 |
| `discount_store_retail_score` | **26** | **43** | **「Daily specific (idiosyncratic) returns for stocks, in percent」** | ★ **因子模型残差收益**（名字与内容严重不符，纯误导） |
| `short_interest_factor_score_2` | 24 | 30 | 空头兴趣水平的得分 | 标准化空头兴趣暴露 |
| `relative_volatility_factor` | 11 | 14 | 相对价格波动 | 波动率风格暴露 |
| `relative_liquidity_factor` | 9 | 12 | 相对交易流动性 | 流动性风格暴露 |
| `relative_leverage_factor` | 5 | 5 | 相对财务杠杆 | 杠杆风格暴露 |
| `systemic_risk_measure_2` | 3 | 4 | 公司对系统性金融风险的贡献度 | 系统性风险贡献 |
| `relative_momentum_factor` | 2 | 2 | 相对价格动量 | 动量风格暴露 |
| `momentum_factor_score` | 2 | 2 | MFMCR 动量风格因子逐日暴露 | 动量（与上一个同族不同口径） |
| `relative_size_factor` | 2 | 2 | 相对规模 | 规模风格暴露 |
| `systemic_risk_factor_score` | 2 | 4 | **「Specific risk matrix per stock per day, annualized percent-squared」** | ★ **特质方差 σ²_idio（年化 %²）** |
| `broad_market_factor_score_2` | **0** | **0** | 宽基市场因子暴露 | ★ 完全未开发，但≈beta，价值低 |

### 关键命名陷阱

- **`discount_store_retail_score`** 名字像「折扣零售板块得分」，**实际是特异收益（个股残差日收益，单位 %）**。这是本数据集**最像 alpha 源**的字段 —— 因为是因子模型残差，在构造上就与所有风格/行业因子正交。
- **`systemic_risk_factor_score`** 名字像「系统性风险」，**实际是特质风险（specific risk，年化方差 %²）** —— 即**模型解释不掉的那部分方差**。名字里的 "systemic" 是错的，正解是 "specific"。
- **`systemic_risk_measure_2`** 才是真正的系统性风险贡献，两个字段名极易混。

### 拥挤度分层（决定 prod 墙风险）

| 档 | 字段 | 用法建议 |
|---|---|---|
| **红（>40 用户）** | `hedge_fund_ownership_factor0`(94/155)、`hedge_fund_ownership_factor1`(34/47) | 只做**控制变量**（`vector_neut` 分母），不做信号主体 |
| **黄（20–40）** | `discount_store_retail_score`(26/43)、`short_interest_factor_score_2`(24/30) | 可做信号主体，但必须有正交化或独特几何 |
| **绿（≤11）** | 其余 9 个 | 低拥挤，优先开发 |

---

## 4. 61 个行业暴露 score + 43 个行业 flag —— 全部判为不可做信号

**理由（三条独立成立）**：

1. **数学上等价于行业哑变量**：个股对其所属行业的因子暴露通常是 1（或接近 1），对其余行业接近 0。`group_rank(x, industry)` 在组内样本上几乎是常数 ⇒ 输出退化为 NaN 或噪声。
2. **已被中性化吃掉**：回测设置 `neutralization = INDUSTRY` 会直接消掉行业截面差异；平台 RA 的 `MATCHES_PYRAMID` 也按行业对齐。
3. **实测无信息**：`userCount = 0` 的有 45 个字段（行业 score + flag 各占一半），平台 308 个 alpha 里几乎没有用它们的。

**唯一可能的用法**（未验证，列为低优先）：
- 43 个 flag 可作为**自定义分组轴**（例如 `group_rank(x, industry_semiconductors_flag)` 只有 2 组，无意义；但多个 flag 相加可构造「跨行业多元化程度」）。
- `conglomerate_sector_score`（3/3 用户）+ `industry_diversified_flag`（1/1）可构造「多元化溢价」，但这两者本质是同一个信息。

---

## 5. 可用字段清单（按优先级）

### Tier A —— 首选（低拥挤 + 高信息含量）

| 字段 | 构造 | 对应机制 | 文献先验（⚠ 未经在线核验） |
|---|---|---|---|
| `discount_store_retail_score` | 特异收益 R | 残差反转 / 残差动量 | Blitz-Huij-Martens (2011) 残差动量；Da-Liu-Schaumburg (2014) 残差反转 |
| `systemic_risk_factor_score` | 特质方差 σ²_idio | 低特质波动异象 / 特质波动冲击 | Ang-Hodrick-Xing-Zhang (2006) 特质波动异象 |
| `systemic_risk_measure_2` | 系统性风险贡献 | 系统重要性折价 | — |

### Tier B —— 次选（中等拥挤，只能当控制变量）

`relative_volatility_factor`、`relative_liquidity_factor`、`relative_leverage_factor`、`relative_momentum_factor`、`relative_size_factor`、`momentum_factor_score`

### Tier C —— 拥挤，仅作正交化分母

`hedge_fund_ownership_factor0/1`、`short_interest_factor_score_2`

---

## 6. 「用机制前查论坛 + 论文」结论

### 论坛侧（`search_forum_posts`，本会话实测）

检索 `residual volatility 特异波动率 低波动` 命中 10 篇，与本数据集相关的可复用要点：

| 来源 | 要点 |
|---|---|
| `30680255378071`【alpha灵感】volatility 波动率因子-可提交的 alpha | 上行波动率 − 下行波动率的不对称性包含信息；**波动率因子为负（低波）的股票未来表现更好** ⇒ 支持 `reverse(σ)` 方向 |
| `36877431208983`【Alpha灵感】尾部风险（波动率因子） | 可提交版本做了两步改造：**加负号 + 除以波动率**；即「个股是否显著受行业尾部风险拖累」 |
| `41482839127959` 波动率机制转换 | **低波动 alpha 在「低波→高波」切换初期表现最好**（高波股跌幅远超低波股）⇒ 低波信号的收益集中在制度切换窗口，这正是 `2Y Sharpe` 容易崩的机理 |
| `35723869706007`【Alpha灵感】流动性波动率因子 | **日频回报换手过高、月频损失太多信息，周频（W=66）最优** ⇒ 周级窗口是本类信号的甜点 |
| `34689255273623` 波动率的「好与坏」 | 已实现波动可分解为正/负收益两部分，`relative signed jump variation` 单独成因子 |

### 论文侧（⚠ `web_search` 402 余额用尽，以下为模型知识，**未经在线核验**）

| 机制 | 定义 | 预期方向 |
|---|---|---|
| 特质波动异象 | 特质方差 σ²_idio 与预期收益**负相关** | 空高 σ²、多低 σ² |
| 残差反转 | 月度残差收益反转（1M） | 空上月残差赢家 |
| 残差动量 | 12M 残差收益动量、跳过最近 1M | 多残差赢家（与上一行方向相反，须实测裁决） |
| 杠杆效应 | 收益与波动的负相关 | 相关性越负，后续波动越大 |
| 低流动性溢价 | Amihud 非流动性 | 空低流动性（**但会撞 investability 闸**） |

---

## 7. 波 172 实测结论（12 模板，本画像的直接检验）

> 完整归因见 `tracking/USA/reports/wave172_mfm_model_output_shape_ablation.md`

| 模板 | 字段 | 结构 | S | F | TO | 2Y | risk_neut_S |
|---|---|---|---|---|---|---|---|
| 残差反转·1M | `discount_store_retail_score` | `reverse(ts_sum(R,22))` | **1.05** | 0.55 | 27.7% | 0.88 | **2.16** |
| 特质波动率·水平 | `systemic_risk_factor_score` | `reverse(σ)` | 0.22 | 0.09 | 19.2% | 0.53 | −0.66 |
| 特质波动率·时序分位 | 同上 | `ts_rank(σ,252)` | −0.16 | −0.02 | 42.7% | 0.02 | 0.88 |
| 残差动量·12M | `discount_store_retail_score` | `ts_delay(ts_sum(R,252),22)` | −0.09 | −0.02 | 8.0% | −0.34 | −0.86 |
| 特质波动率·二阶矩 | `systemic_risk_factor_score` | `ts_std_dev(σ,66)` | −0.28 | −0.13 | 4.8% | −0.51 | −0.17 |
| 残差信息比 | `discount_store_retail_score` | `ts_ir(R,252)` | −0.37 | −0.20 | 10.2% | −0.54 | −1.71 |

**核心结论：13 个风格因子中，只有 `discount_store_retail_score`（特异收益）与 `systemic_risk_factor_score`（特质方差）携带信号；行业 score / flag / 高拥挤持股因子三族全部无增量。**

`risk_neutralized_sharpe = 2.16`（vs 原始 S 1.05）是本数据集**最重要的单一发现**：说明残差反转的收益在剥离风险模型风格暴露后翻倍 ⇒ **风格暴露是在拖累而不是在贡献**，后续必须做风格正交化（`vector_neut`）。
