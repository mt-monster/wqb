# 已提交 Alpha 的算子使用讲解（按 dataset category 分组）

> 生成时间：2026-11-14 12:58 GMT+8｜数据来自平台实时接口｜**本报告只做只读分析，未提交、未修改任何 alpha**

## 0 口径与数据来源

| 项 | 口径 |
|---|---|
| 已提交 alpha 列表 | `GET /users/self/alphas?stage=OS&type=REGULAR` 分页拉全：**373 条**；其中 `status=ACTIVE` 且有 `regular.code` 的 **260 条**为分析总体，113 条 `DECOMMISSIONED` 已排除。SUPER alpha 不在本轮范围（其 combo/selection 表达式属 COMBO 作用域）。 |
| 权限内算子 | `GET /operators` 返回的**该账号授权清单 = 103 个**（9 个 operator category：Arithmetic 16 / Time Series 30 / Reduce 14 / Logical 11 / Group 11 / Cross Sectional 7 / Vector 7 / Transformational 4 / Special 3）。本轮 13 条代表 alpha 中共出现 **38 个唯一算子，100% 在该清单内**，无未识别函数调用、`unknown called ops = 0`。 |
| 定义 / 允许用法 / 场景 / 限制 | `GET /operators` 的 `definition`、`description`、`scope`、`level`，加 `GET /operators/{name}` 详细文档页（103 个中 57 个有文档页）。 |
| category 口径 | **平台 dataset 的 `category` 字段**（`GET /datasets` 返回 16 类），不是 operator category。每个 category 下列出 1 个代表 dataset + 1 条已提交 alpha；每条算子另标注它所属的 operator category。 |
| 字段 → dataset → category | 本地平台 catalog 缓存 `data/wqb.db` 的 `fields`(315,394 条) / `datasets`(2,083 条)；14 个候选 dataset 逐个用 `get_datafields` 在对应 region/universe/delay 下复验，**13 个通过**（FUNDAMENTAL 见该节说明）。 |
| 选样规则 | ① alpha 必须 OS/ACTIVE 且表达式**实际引用**该 dataset 字段；② 优先信号字段纯度高、算子覆盖类别多、平台附设计说明者；③ 每个 category 只输出 1 个代表 dataset；④ 表达式若含其他 dataset 字段，逐项列明来源，**不跨 category 借用样本**；⑤ 该 category 无可信主体样本 → 标注「无可用样本」并跳过。 |
| 中缀语法糖 | `+ - * / > <` 与一元负号按平台 `definition` 分别计入 `add/subtract/multiply/divide/greater/less/reverse`，**仅在该表达式实际出现时才计入**。变量赋值 `a = ...` 与命名参数（`std=`、`driver=`）不是算子。 |

## 1 总览：category → dataset → alpha

| category | 代表 dataset | 已提交 alpha | 平台指标 S / F / TO | 实际出现的算子数 | 算子类别覆盖 |
|---|---|---|---|---|---|
| **ANALYST** / 分析师预期 | `analyst44` | `KP78pLWk` | 1.63 / 1.04 / 0.2284 | 4 | 4 |
| **EARNINGS** / 财报/业绩 | `earnings_sent_matrix` | `XgaG2Vom` | 1.75 / 1.05 / 0.0872 | 7 | 3 |
| **FUNDAMENTAL** / 基本面 | `fundamental6` | `qMjLYVVP` | 1.74 / 1.72 / 0.0287 | 5 | 4 |
| **IMBALANCE** / 订单失衡 | `imbalance5` | `levk1d98` | 2.81 / 1.7 / 0.3262 | 6 | 5 |
| **INSIDERS** / 内部人交易 | `insiders5` | `RRE9NkVj` | 1.76 / 1.63 / 0.0968 | 4 | 4 |
| **INSTITUTIONS** / 机构持仓/申报 | `institutions1` | `2rmGAPqN` | 1.81 / 1.48 / 0.1296 | 12 | 7 |
| **MACRO** / 宏观/指数 | — | **无可用样本** | — | — | — |
| **MODEL** / 量化模型 | `predictive_starmine` | `GrlqxwKx` | 1.8 / 1.28 / 0.1298 | 5 | 3 |
| **NEWS** / 新闻 | `news17` | `58E7jkaN` | 1.85 / 1.14 / 0.0802 | 10 | 5 |
| **OPTION** / 期权 | — | **无可用样本** | — | — | — |
| **OTHER** / 其他替代数据 | `insider_feats` | `pwjpKGJ3` | 1.65 / 1.38 / 0.1046 | 6 | 3 |
| **PV** / 价量 | `intraday_pv_feats` | `gJZ6pONl` | 2.87 / 1.37 / 0.6894 | 10 | 6 |
| **RISK** / 风险因子 | `risk70` | `6Xdo27P5` | 1.68 / 1.3 / 0.1201 | 5 | 3 |
| **SENTIMENT** / 情绪/关注度 | `sentiment7` | `bl6OWZ2M` | 2.03 / 1.61 / 0.161 | 8 | 4 |
| **SHORTINTEREST** / 卖空/融券 | `shortinterest38` | `O08kz5Mv` | 2.16 / 1.65 / 0.1831 | 8 | 5 |
| **SOCIALMEDIA** / 社交媒体 | — | **无可用样本** | — | — | — |

> 说明：MACRO 类虽有 2 条 alpha 引用了 `macro63` 字段，但平台描述明确该字段是零常数、仅为挂塔而声明 → 按「不跨 category 借用」判为无可用样本，详见 §3。

---

## 2 分组讲解（13 个有样本 category）

### 2.1 ANALYST / 分析师预期

**→ 代表 dataset：`analyst44`**

- 选择依据：ANALYST 类共 61 条已提交 alpha 用到该类 dataset；`analyst44` 在 KOR/TOP600 有 520 个字段（平台复验），且该样本是纯单 dataset、同时覆盖 Vector→Time Series→Cross Sectional→Arithmetic 四层处理，最能演示分析师数据的完整加工链。
- 平台复验：`get_datafields(region=KOR, universe=TOP600, delay=1, dataset_id=analyst44)` 返回 **520** 个字段；本 alpha 实际用到并命中：`anl44_second_en_eps_value`, `eps_estimate_4wk_change`。

**→ 已提交 alpha：`KP78pLWk`**

- 设置：`KOR/TOP600` · delay 1 · decay 12 · neutralization `INDUSTRY`；提交日 `2026-09-25T02:36:22-04:00`；状态 OS/ACTIVE。
- 平台 IS 指标：Sharpe **1.63** / Fitness **1.04** / Turnover **0.2284**。
- 原始表达式：

```text
add(ts_rank(vec_avg(anl44_second_en_eps_value), 50), rank(vec_avg(eps_estimate_4wk_change)))
```

**表达式整体含义 / 想捕捉的信号**：平台未附描述，以下为基于字段与算子的解读：两条分析师预期信号相加。① `anl44_second_en_eps_value`（二次英文 EPS 预测）先按向量取均值，再取 50 日时序分位，衡量「当前预测值相对自身近 50 日水位的高低」；② `eps_estimate_4wk_change`（4 周 EPS 预期变化）取全市场截面分位，衡量「相对同业的预期修正强度」。两路都是 0~1 有界量，相加后「预期水位偏高且正在上修」的股票得分最高——捕捉分析师预期的时间维度惯性与横截面修正动量。

**辅助字段与归属**：无跨 dataset 字段；表达式两个字段均属 `analyst44`。

**实际出现且在权限范围内的算子（4 个）**

| 算子（operator category） | 平台定义 · 允许用法(scope) · 适用场景与限制 | 对该 alpha 的数据做了什么处理 | 在最终信号中的具体作用与影响 | 为何适合该 dataset / category 场景 |
|---|---|---|---|---|
| **`add`**<br>(Arithmetic) | `add(x, y, filter=false), x + y`<br>scope **COMBO/REGULAR/SELECTION**<br>场景：逐元素相加，可多参数；把多路有界信号等权或加权合成<br>限制：filter=false 时 NaN 传播；filter=true 把 NaN 当 0，可提高覆盖 | 把两路 0~1 分位逐元素相加，无拟合系数。 | 形成最终打分；两路有界，任一路都不会支配另一路，天然限制单因子暴露。 | 分析师数据常需把「水平」与「变化」两种正交信息合成，相加是最简且不引入过拟合的组合。 |
| **`rank`**<br>(Cross Sectional) | `rank(x, rate=2)`<br>scope **COMBO/REGULAR**<br>场景：每日横截面分位（0~1）；消除量纲与极端值<br>限制：rate 控制排序精度，默认 2，设 0 为精确排序；仅 REGULAR/COMBO，不用于 SELECTION | 把 4 周 EPS 预期变化映射到当日全市场分位（0~1）。 | 贡献第二路得分，并与第一路同尺度相加；决定「修正强度」在最终信号中的权重（等权 1:1）。 | 预期修正值跨公司不可直接比较，截面排序是 ANALYST 类的标准归一方式。 |
| **`ts_rank`**<br>(Time Series) | `ts_rank(x, d, constant=0)`<br>scope **COMBO/REGULAR**<br>场景：当前值在过去 d 日自身序列中的分位，突出时序相对高低<br>限制：仅 REGULAR/COMBO；constant 可平移输出 | 把汇总后的 EPS 预测值映射到其自身过去 50 日的分位（0~1），把绝对 EPS 数字转成时序位置。 | 贡献第一路得分；消除公司间 EPS 绝对量纲差异，使高价股与低价股可比。 | 分析师预期是慢变量且分布厚尾，时序分位比 ts_zscore 更不容易被单次大幅调整扭曲。 |
| **`vec_avg`**<br>(Vector) | `vec_avg(x)`<br>scope **COMBO/REGULAR**<br>场景：把 VECTOR 字段逐元素取算术平均，转成每股票每日一个标量<br>限制：x 必须是 VECTOR 字段；仅 REGULAR/COMBO | 把 `anl44_second_en_eps_value` 与 `eps_estimate_4wk_change` 两个 VECTOR 字段各压成一个每日标量，消除「同一天多位分析师/多条预测记录」的维度。 | 决定后续 ts_rank、rank 的输入尺度；若改用 vec_sum，结果会随分析师覆盖人数变化而被大市值公司主导。 | analyst44 是典型逐记录存储的分析师预测向量，类别场景要求「跨来源汇总成一致预期」而非挑单条记录。 |

---

### 2.2 EARNINGS / 财报/业绩

**→ 代表 dataset：`earnings_sent_matrix`**

- 选择依据：EARNINGS 类 10 条已提交样本中，`earnings_sent_matrix` 提供同源于财报电话会议文本的情绪字段；平台复验 EUR/TOP2500 下 7 个字段，样本 `XgaG2Vom` 用到 7 个算子、覆盖 Time Series/Arithmetic/Group 三类，且平台附有完整设计说明。
- 平台复验：`get_datafields(region=EUR, universe=TOP2500, delay=1, dataset_id=earnings_sent_matrix)` 返回 **7** 个字段；本 alpha 实际用到并命中：`likelihood_of_neutral_tone`, `overall_sentiment_score`。

**→ 已提交 alpha：`XgaG2Vom`（平台名 `EUR_R_sentcert_01`）**

- 设置：`EUR/TOP2500` · delay 1 · decay 1 · neutralization `MARKET`；提交日 `2026-11-11T08:27:00-05:00`；状态 OS/ACTIVE。
- 平台 IS 指标：Sharpe **1.75** / Fitness **1.05** / Turnover **0.0872**。
- 原始表达式：

```text
a = ts_mean(overall_sentiment_score, 66); m = ts_mean(likelihood_of_neutral_tone, 66); k = ts_corr(a, m, 252); group_neutralize(ts_zscore(multiply(a, subtract(add(k, 2.1), m)), 420), industry)
```

**表达式整体含义 / 想捕捉的信号**：平台描述：净语调 = 情绪分 − 中性语调强度；两序列的 252 日相关性充当「确信度门控」，因为强语调若由中性套话承载多为噪声。66 日均值平滑文本噪声，`k + 2.1` 保证调制项恒正，420 日 ts_zscore 归一化情绪 regime，最后用 industry 中性化剔除行业措辞偏差。捕捉的是「方向性语调确凿且非套话」的财报文本 alpha。

**辅助字段与归属**：`industry` 来自 pv1（PV 类）的通用 GROUP 字段，仅作分组容器，不构成信号来源。

**实际出现且在权限范围内的算子（7 个）**

| 算子（operator category） | 平台定义 · 允许用法(scope) · 适用场景与限制 | 对该 alpha 的数据做了什么处理 | 在最终信号中的具体作用与影响 | 为何适合该 dataset / category 场景 |
|---|---|---|---|---|
| **`add`**<br>(Arithmetic) | `add(x, y, filter=false), x + y`<br>scope **COMBO/REGULAR/SELECTION**<br>场景：逐元素相加，可多参数；把多路有界信号等权或加权合成<br>限制：filter=false 时 NaN 传播；filter=true 把 NaN 当 0，可提高覆盖 | `add(k, 2.1)` 把相关系数整体平移到正值区间。 | 保证后续乘法不会翻转信号符号；常数 2.1 是人为选择的保底偏移。 | 相关系数可取负值，财报情绪类信号需要单向调制而非方向反转。 |
| **`group_neutralize`**<br>(Group) | `group_neutralize(x, group)`<br>scope **COMBO/REGULAR**<br>场景：组内减均值，剔除组共同暴露<br>限制：group 须为 GROUP 字段；仅 REGULAR/COMBO | 按 industry 减去组内均值。 | 最终头寸只保留行业内相对语调差，剔除行业共同措辞、监管话术带来的假信号。 | 不同行业电话会议的语气规范差异极大，组内中性化是必需而非可选。 |
| **`multiply`**<br>(Arithmetic) | `multiply(x, y, ..., filter=false), x * y`<br>scope **COMBO/REGULAR/SELECTION**<br>场景：逐元素相乘，可多参数；加权、掩码、条件合成<br>限制：filter=false 时任一 NaN 使结果为 NaN | 把平滑情绪 a 与上述调制因子相乘。 | 生成最终原始信号；确信度高时放大情绪，确信度低时压缩到近零。 | 该 dataset 的两个字段是「水平 × 置信度」关系，乘法比相加更贴合语义。 |
| **`subtract`**<br>(Arithmetic) | `subtract(x, y, filter=false), x - y`<br>scope **COMBO/REGULAR/SELECTION**<br>场景：逐元素左到右相减；构造差值、中心化、价差<br>限制：NaN 传播；多参数按 ((a-b)-c) 计算 | `subtract(add(k,2.1), m)` 得到「确信度 − 中性语调强度」的调制因子。 | 与 a 相乘前先扣除套话成分，中性措辞越重、调制越弱。 | EARNINGS 文本里「中性语气概率」是需被剔除的混杂变量，差分是最直接的解耦。 |
| **`ts_corr`**<br>(Time Series) | `ts_corr(x, y, d)`<br>scope **COMBO/REGULAR**<br>场景：两序列过去 d 日 Pearson 相关，取值 -1~1<br>限制：平台注明在近似正态、线性关系下最有效；仅 REGULAR/COMBO | 计算 a 与 m 在 252 日窗口的 Pearson 相关 k（-1~1）。 | 输出确信度调制项的核心：k+2.1 后再减 m，相关性越高/越低直接改变最终语调的放大倍数。 | 同一文本模型的两个输出天然共动，用长期相关度量「这次语调是否由模板语言驱动」是该 dataset 特有的清洗方式。 |
| **`ts_mean`**<br>(Time Series) | `ts_mean(x, d)`<br>scope **COMBO/REGULAR**<br>场景：过去 d 日均值，平滑噪声、提取慢变量<br>限制：仅 REGULAR/COMBO；d 为交易日数 | 对 `overall_sentiment_score` 与 `likelihood_of_neutral_tone` 各做 66 日均值，得到慢变量 a、m。 | 把逐日文本打分转为季度级语调水平，是最终信号的基线幅度；窗口决定信号记忆长度。 | 财报电话会议情绪按日更新、单日噪声大，EARNINGS 场景必须先平滑再比较。 |
| **`ts_zscore`**<br>(Time Series) | `ts_zscore(x, d)`<br>scope **COMBO/REGULAR**<br>场景：当前值相对过去 d 日均值差多少个标准差，跨期/跨股可比<br>限制：仅 REGULAR/COMBO；短窗口内标准差不稳定 | 对乘积做 420 日滚动标准化。 | 把不同情绪 regime（牛熊、披露季）拉回同一尺度，避免某一年整体情绪偏高长期满仓。 | 财报情绪存在明显年度/周期偏移，长窗标准化是 EARNINGS 类稳健性的关键。 |

---

### 2.3 FUNDAMENTAL / 基本面

**→ 代表 dataset：`fundamental6`**

- 选择依据：FUNDAMENTAL 类 51 条样本，`fundamental6` 是其中被引用最多的单 dataset；`qMjLYVVP` 是纯单 dataset 且 5 个算子覆盖 Vector/Arithmetic/Time Series/Cross Sectional 四类，平台附设计说明。
- 平台复验：`get_datafields(region=MEA, universe=TOP400, delay=1, dataset_id=fundamental6)` 返回 **0** 个字段；本 alpha 实际用到并命中：（见该节说明）。

**→ 已提交 alpha：`qMjLYVVP`（平台名 `MEA_R_fundamental6_jLYVVP`）**

- 设置：`MEA/TOP400` · delay 1 · decay 8 · neutralization `COUNTRY`；提交日 `2026-09-01T00:24:25-04:00`；状态 OS/ACTIVE。
- 平台 IS 指标：Sharpe **1.74** / Fitness **1.72** / Turnover **0.0287**。
- 原始表达式：

```text
multiply(rank(divide(vec_avg(fundamental_retained_earnings),vec_avg(fundamental_common_equity_total))),rank(multiply(ts_zscore(vec_avg(debt_current_liabilities_total),252),-1)))
```

**表达式整体含义 / 想捕捉的信号**：平台描述：质量叠加去杠杆双重条件——偏好留存收益/普通股权益高、且正在压降流动负债的 MEA 股票。两路各自截面分位后相乘，只有「质量高」且「偿债改善」同时成立才得高分，是逻辑与而非加权和。

**辅助字段与归属**：表达式三个字段全属 `fundamental6`。注：平台 `get_datafields(MEA, TOP400, fundamental6)` 当前返回 0 个字段（dataset 可能已调整区域可用范围），字段归属依据本地平台 catalog 缓存与 alpha 的 `SRC_fundamental6` 标签；该 alpha 状态为 OS/ACTIVE，已提交事实不受影响。

**实际出现且在权限范围内的算子（5 个）**

| 算子（operator category） | 平台定义 · 允许用法(scope) · 适用场景与限制 | 对该 alpha 的数据做了什么处理 | 在最终信号中的具体作用与影响 | 为何适合该 dataset / category 场景 |
|---|---|---|---|---|
| **`divide`**<br>(Arithmetic) | `divide(x, y), x / y`<br>scope **COMBO/REGULAR/SELECTION**<br>场景：逐元素相除；构造比率、归一到相对量<br>限制：分母为 0 会报错；平台建议 divide(x, add(y, 0.0001)) 加 epsilon | 留存收益 ÷ 普通股权益，构造「累计盈利 / 资本」质量比率。 | 第一路得分的主体；把规模效应除掉，使大公司与小公司可比。 | FUNDAMENTAL 场景的通用做法是用比率消除市值/规模量纲；此处未加 epsilon，分母为 0 时依赖平台 NaN 处理。 |
| **`multiply`**<br>(Arithmetic) | `multiply(x, y, ..., filter=false), x * y`<br>scope **COMBO/REGULAR/SELECTION**<br>场景：逐元素相乘，可多参数；加权、掩码、条件合成<br>限制：filter=false 时任一 NaN 使结果为 NaN | 内层 `multiply(..., -1)` 把去杠杆方向翻正；外层把两路分位相乘。 | 内层决定「负债下降得正分」；外层实现逻辑与，任一路接近 0 都会把总分压到 0。 | 质量要求与改善要求不可互相替代，乘积比相加更能表达「双条件同时满足」。 |
| **`rank`**<br>(Cross Sectional) | `rank(x, rate=2)`<br>scope **COMBO/REGULAR**<br>场景：每日横截面分位（0~1）；消除量纲与极端值<br>限制：rate 控制排序精度，默认 2，设 0 为精确排序；仅 REGULAR/COMBO，不用于 SELECTION | 对质量比率与去杠杆 z-score 各取截面分位（0~1）。 | 统一两路尺度并抑制财务比率极端值；使最终乘积落在 0~1。 | 财报比率常含极端异常值，截面排序是 FUNDAMENTAL 类的稳健化标准动作。 |
| **`ts_zscore`**<br>(Time Series) | `ts_zscore(x, d)`<br>scope **COMBO/REGULAR**<br>场景：当前值相对过去 d 日均值差多少个标准差，跨期/跨股可比<br>限制：仅 REGULAR/COMBO；短窗口内标准差不稳定 | 对流动负债做 252 日（约一年）滚动标准化。 | 把「负债变化」转成相对自身历史的偏离度，是第二路得分的时序基准。 | 负债水平有强季节性，用年度标准化才能识别真实的去杠杆趋势。 |
| **`vec_avg`**<br>(Vector) | `vec_avg(x)`<br>scope **COMBO/REGULAR**<br>场景：把 VECTOR 字段逐元素取算术平均，转成每股票每日一个标量<br>限制：x 必须是 VECTOR 字段；仅 REGULAR/COMBO | 把 `fundamental_retained_earnings`、`fundamental_common_equity_total`、`debt_current_liabilities_total` 三个 VECTOR 财务项各压成单值。 | 为比率与 z-score 提供逐日标量输入；聚合方式决定财务口径（均值而非求和）。 | fundamental6 的财报项目按报告期/口径存成向量，需先跨版本汇总才能做比率。 |

---

### 2.4 IMBALANCE / 订单失衡

**→ 代表 dataset：`imbalance5`**

- 选择依据：IMBALANCE 类仅 4 条已提交样本，全部引用 `imbalance5`（IND/TOP500 下平台复验 2 个字段）；选 `levk1d98` 因其 6 个算子覆盖 Logical/Transformational/Time Series/Cross Sectional 四类，且平台描述把失衡度门控的作用写得很清楚。
- 平台复验：`get_datafields(region=IND, universe=TOP500, delay=1, dataset_id=imbalance5)` 返回 **2** 个字段；本 alpha 实际用到并命中：`imb5_mktcap`。

**→ 已提交 alpha：`levk1d98`（平台名 `IND_R_imbalance5_vk1d98`）**

- 设置：`IND/TOP500` · delay 1 · decay 4 · neutralization `STATISTICAL`；提交日 `2026-09-20T00:10:22-04:00`；状态 OS/ACTIVE。
- 平台 IS 指标：Sharpe **2.81** / Fitness **1.7** / Turnover **0.3262**。
- 原始表达式：

```text
trade_when(greater(rank(imb5_mktcap), 0.5), rank(multiply(-1, ts_mean(corr_last_trade_price_with_volume, 5))), less(rank(imb5_mktcap), 0.4))
```

**表达式整体含义 / 想捕捉的信号**：平台描述：以市值缩放的失衡度截面排名 >0.5 时开仓，<0.4 时平仓；持仓是「5 日均价量相关性的负值」的截面分位。经济逻辑是单边订单流把价量关系推离常态、这种压力通常短暂，故在高失衡状态下做价量一致性的反转。

**辅助字段与归属**：**混合样本**：`imb5_mktcap`（imbalance5，本 category）承担开/平仓门控；`corr_last_trade_price_with_volume` 来自 `intraday_pv_feats`（PV 类）构成反转主体。平台 pyramid 也同时登记 IMBALANCE 与 PV 两类。此处如实标注，未把 PV 数据冒充 IMBALANCE 数据。

**实际出现且在权限范围内的算子（6 个）**

| 算子（operator category） | 平台定义 · 允许用法(scope) · 适用场景与限制 | 对该 alpha 的数据做了什么处理 | 在最终信号中的具体作用与影响 | 为何适合该 dataset / category 场景 |
|---|---|---|---|---|
| **`greater`**<br>(Logical) | `input1 > input2`<br>scope **COMBO/REGULAR/SELECTION**<br>场景：大于返回 1；把连续量转成触发布尔<br>限制：比较结果为 0/1，常与 trade_when / if_else 联用 | `greater(rank(imb5_mktcap), 0.5)` 生成开仓触发布尔。 | 决定 trade_when 何时把新信号写入；不触发时维持前一日持仓。 | 订单流失衡是状态量而非连续信号，IMBALANCE 场景适合离散触发。 |
| **`less`**<br>(Logical) | `input1 < input2`<br>scope **COMBO/REGULAR/SELECTION**<br>场景：小于返回 1；构造退出条件<br>限制：比较结果为 0/1 | `less(rank(imb5_mktcap), 0.4)` 生成退出布尔。 | z 条件优先：为真则把持仓置 NaN 平仓；与 0.5 开仓阈值形成 0.1 的滞回带，避免反复开平。 | 失衡状态消退后应离场，滞回区间能抑制阈值附近的抖动换手。 |
| **`multiply`**<br>(Arithmetic) | `multiply(x, y, ..., filter=false), x * y`<br>scope **COMBO/REGULAR/SELECTION**<br>场景：逐元素相乘，可多参数；加权、掩码、条件合成<br>限制：filter=false 时任一 NaN 使结果为 NaN | `multiply(-1, ...)` 对平滑后的相关取负。 | 把「价量同向」翻成反转头寸方向，决定最终多空符号。 | 该 dataset 描述的是偏离常态的单边压力，方向应做 fade 而非跟随。 |
| **`rank`**<br>(Cross Sectional) | `rank(x, rate=2)`<br>scope **COMBO/REGULAR**<br>场景：每日横截面分位（0~1）；消除量纲与极端值<br>限制：rate 控制排序精度，默认 2，设 0 为精确排序；仅 REGULAR/COMBO，不用于 SELECTION | 分别把 `imb5_mktcap` 与 5 日价量相关映射成 0~1 截面分位。 | 让 0.5 / 0.4 阈值跨日、跨股票可比；同时把持仓强度限制在有界区间。 | 失衡度是量纲不定的缩放值，只有排名才能作为稳定的状态阈值。 |
| **`trade_when`**<br>(Transformational) | `trade_when(x, y, z)`<br>scope **COMBO/REGULAR**<br>场景：x 为真才更新为 y，z 为真平仓为 NaN，其余保持前值；事件驱动 + 降换手<br>限制：z 优先于 x；z 为真输出 NaN（无持仓）；仅 REGULAR/COMBO | 三参数分别为开仓触发、目标持仓、退出条件。 | 只在失衡高位持有反转、其余日保持前值；这是整条 alpha 的结构骨架，直接决定换手与持仓持续性。 | 订单失衡是事件/状态型数据，条件持有比连续打分更贴合 IMBALANCE 场景。 |
| **`ts_mean`**<br>(Time Series) | `ts_mean(x, d)`<br>scope **COMBO/REGULAR**<br>场景：过去 d 日均值，平滑噪声、提取慢变量<br>限制：仅 REGULAR/COMBO；d 为交易日数 | 对 `corr_last_trade_price_with_volume` 做 5 日均值。 | 把日内价量相关平滑成可交易的短期状态，降低单日噪声。 | 价量一致性是高频量，IMBALANCE 门控下的反转需要短窗平滑而非长窗趋势。 |

---

### 2.5 INSIDERS / 内部人交易

**→ 代表 dataset：`insiders5`**

- 选择依据：INSIDERS 类 6 条样本，`insiders5` 在 KOR/TOP600 平台复验 53 个字段；`RRE9NkVj` 是纯信号样本且用到 vec_stddev 这个少见的 Vector 离散度算子，能演示内部人数据的「分歧度」用法。
- 平台复验：`get_datafields(region=KOR, universe=TOP600, delay=1, dataset_id=insiders5)` 返回 **53** 个字段；本 alpha 实际用到并命中：`insd5_vol_chg`。

**→ 已提交 alpha：`RRE9NkVj`（平台名 `KOR_R_insd5vol55_01`）**

- 设置：`KOR/TOP600` · delay 1 · decay 4 · neutralization `REVERSION_AND_MOMENTUM`；提交日 `2026-11-06T08:45:33-05:00`；状态 OS/ACTIVE。
- 平台 IS 指标：Sharpe **1.76** / Fitness **1.63** / Turnover **0.0968**。
- 原始表达式：

```text
subtract(0.5, group_rank(ts_mean(vec_stddev(insd5_vol_chg), 55), sector))
```

**表达式整体含义 / 想捕捉的信号**：平台描述：把内部人成交量变化的离散度当作行业相对的反向信号。内部人真实申报的分散程度反映知情分歧；离散度越高，方向越不明确，故取负。

**辅助字段与归属**：`sector` 来自 pv1（PV 类）通用 GROUP 字段，仅作分组容器。

**实际出现且在权限范围内的算子（4 个）**

| 算子（operator category） | 平台定义 · 允许用法(scope) · 适用场景与限制 | 对该 alpha 的数据做了什么处理 | 在最终信号中的具体作用与影响 | 为何适合该 dataset / category 场景 |
|---|---|---|---|---|
| **`group_rank`**<br>(Group) | `group_rank(x, group)`<br>scope **COMBO/REGULAR**<br>场景：组内分位（0~1）；只比较同行业/同板块/同聚类内的相对位置<br>限制：group 须为 GROUP 字段；仅 REGULAR/COMBO | 在 sector 内取离散度的分位（0~1）。 | 把绝对分歧度转成行业内相对位置，剔除行业间申报活跃度差异。 | 不同行业内部人交易频率差别大，组内比较才有经济含义。 |
| **`subtract`**<br>(Arithmetic) | `subtract(x, y, filter=false), x - y`<br>scope **COMBO/REGULAR/SELECTION**<br>场景：逐元素左到右相减；构造差值、中心化、价差<br>限制：NaN 传播；多参数按 ((a-b)-c) 计算 | `subtract(0.5, group_rank(...))` 中心化并翻转。 | 离散度最低的股票得最高正分、最高者得负分，形成反向头寸，输出落在 -0.5~+0.5。 | 平台描述明确该信号为 contrarian，0.5 中心化同时保证多空对称。 |
| **`ts_mean`**<br>(Time Series) | `ts_mean(x, d)`<br>scope **COMBO/REGULAR**<br>场景：过去 d 日均值，平滑噪声、提取慢变量<br>限制：仅 REGULAR/COMBO；d 为交易日数 | 对离散度做 55 日均值平滑。 | 把偶发的单日申报噪声抹平，形成中期分歧水平；窗口决定反应速度。 | 内部人申报稀疏且不规则，必须时间平滑才有稳定横截面。 |
| **`vec_stddev`**<br>(Vector) | `vec_stddev(x)`<br>scope **COMBO/REGULAR**<br>场景：返回 VECTOR 字段内元素的标准差，衡量日内/跨来源离散度<br>限制：level 未标注、无详细文档页；仅 REGULAR/COMBO | 对 `insd5_vol_chg` 这个 VECTOR 字段取元素标准差，得到当日内部人交易量变化的离散度。 | 把「多笔申报的差异」压成一个可比较的分歧度数值，是整条信号的唯一信息源。 | insiders5 按申报记录存向量，类别场景关心的是申报之间是否一致，而非总量。 |

---

### 2.6 INSTITUTIONS / 机构持仓/申报

**→ 代表 dataset：`institutions1`**

- 选择依据：INSTITUTIONS 类 8 条样本，`institutions1` 在 DEU/TOP500 平台复验 7 个字段；`2rmGAPqN` 用到 12 个函数算子、覆盖 7 个算子类别，是全轮算子密度最高的代表，且平台附有 1500+ 字设计说明。
- 平台复验：`get_datafields(region=DEU, universe=TOP500, delay=1, dataset_id=institutions1)` 返回 **7** 个字段；本 alpha 实际用到并命中：`inst1_holdings`, `inst1_tradesignificance`, `inst1_valueeur`。

**→ 已提交 alpha：`2rmGAPqN`（平台名 `DEU_R_insconviction_01`）**

- 设置：`DEU/TOP500` · delay 1 · decay 4 · neutralization `FAST`；提交日 `2026-10-09T06:51:28-04:00`；状态 OS/ACTIVE。
- 平台 IS 指标：Sharpe **1.81** / Fitness **1.48** / Turnover **0.1296**。
- 原始表达式：

```text
tail(winsorize(group_rank(multiply(ts_sum(divide(vec_sum(inst1_valueeur),add(vec_sum(inst1_holdings),0.0001)),220),if_else(and(greater(ts_sum(divide(vec_sum(inst1_valueeur),add(vec_sum(inst1_holdings),0.0001)),220),0),greater(ts_sum(vec_avg(inst1_tradesignificance),66),2.0)),1,0)),oth455_partner_n2v_p50_q200_w1_pca_fact2_cluster_20),std=2),lower=0.25,upper=0.75,newval=0.5)
```

**表达式整体含义 / 想捕捉的信号**：平台描述：内部人/机构申报的信息量来自「交易金额相对自身持仓的规模」，而非绝对欧元金额。构造 `valueeur / holdings` 的无量纲信念度，要求买入侧且披露显著性达标，再在供应链伙伴聚类内排序；中间区间用 tail 压平以剔除未申报名称形成的无信息密度。

**辅助字段与归属**：分组依据 `oth455_partner_n2v_..._cluster_20` 来自 `other455`（OTHER 类），仅作为 group 参数；平台 pyramid 同时登记 INSTITUTIONS 与 OTHER。三个 `inst1_*` 信号字段全部来自 `institutions1`。

**实际出现且在权限范围内的算子（12 个）**

| 算子（operator category） | 平台定义 · 允许用法(scope) · 适用场景与限制 | 对该 alpha 的数据做了什么处理 | 在最终信号中的具体作用与影响 | 为何适合该 dataset / category 场景 |
|---|---|---|---|---|
| **`add`**<br>(Arithmetic) | `add(x, y, filter=false), x + y`<br>scope **COMBO/REGULAR/SELECTION**<br>场景：逐元素相加，可多参数；把多路有界信号等权或加权合成<br>限制：filter=false 时 NaN 传播；filter=true 把 NaN 当 0，可提高覆盖 | `add(vec_sum(inst1_holdings), 0.0001)` 给分母加 epsilon。 | 防止全额处置（持仓为 0）时除法报错，是这条 alpha 能稳定运行的前提。 | 平台 divide 文档明确建议该写法；申报类数据分母为 0 并非罕见。 |
| **`and`**<br>(Logical) | `and(input1, input2)`<br>scope **COMBO/REGULAR/SELECTION**<br>场景：双条件同时为真返回 1；逻辑门控<br>限制：输入应为 0/1 布尔 | 合并两个布尔条件。 | 只有「买入 + 高显著性」同时成立才输出 1，收紧候选集。 | 单条件会引入大量例行小额申报噪声。 |
| **`divide`**<br>(Arithmetic) | `divide(x, y), x / y`<br>scope **COMBO/REGULAR/SELECTION**<br>场景：逐元素相除；构造比率、归一到相对量<br>限制：分母为 0 会报错；平台建议 divide(x, add(y, 0.0001)) 加 epsilon | `valueeur / (holdings + 0.0001)` 构造无量纲信念度。 | 把大额交易的规模效应归一化，是整条信号的主干；决定后续累计与排序的数值。 | INSTITUTIONS 场景比较的是「相对自身仓位下了多大注」，比率比绝对额更可比。 |
| **`greater`**<br>(Logical) | `input1 > input2`<br>scope **COMBO/REGULAR/SELECTION**<br>场景：大于返回 1；把连续量转成触发布尔<br>限制：比较结果为 0/1，常与 trade_when / if_else 联用 | 两处：信念度累计 >0（买入侧）、显著性累计 >2.0（非常规申报）。 | 把连续量转成两个筛选布尔；直接决定哪些名称进入后续打分。 | 申报方向与大额/机会主义交易的区分是 INSTITUTIONS 类最核心的先验。 |
| **`group_rank`**<br>(Group) | `group_rank(x, group)`<br>scope **COMBO/REGULAR**<br>场景：组内分位（0~1）；只比较同行业/同板块/同聚类内的相对位置<br>限制：group 须为 GROUP 字段；仅 REGULAR/COMBO | 在供应链伙伴聚类（`other455` 的 cluster 字段）内取信念度分位。 | 把比较对象从行业同业换成经济关联公司，决定最终相对强弱。 | 平台说明：供应链路上的信息扩散比行业分类更贴近机构申报的传导路径。 |
| **`if_else`**<br>(Logical) | `if_else(cond, x, y)`<br>scope **COMBO/REGULAR/SELECTION**<br>场景：条件选择两路表达式之一；事件驱动分支<br>限制：条件为真取第 2 参数、为假取第 3 参数 | 条件成立取 1、否则取 0，生成 0/1 掩码。 | 把布尔条件变成可与信念度相乘的数值。 | 稀疏披露下大量股票当日无有效申报，需要显式掩码而不是 NaN 传播。 |
| **`multiply`**<br>(Arithmetic) | `multiply(x, y, ..., filter=false), x * y`<br>scope **COMBO/REGULAR/SELECTION**<br>场景：逐元素相乘，可多参数；加权、掩码、条件合成<br>限制：filter=false 时任一 NaN 使结果为 NaN | 信念度累计 × 0/1 掩码。 | 不满足条件的名称直接归零，不参与聚类内排序。 | 把「有无有效信息」与「信息强度」解耦，避免无申报名称占据中间排名。 |
| **`tail`**<br>(Transformational) | `tail(x, lower=0, upper=0, newval=0)`<br>scope **COMBO/REGULAR**<br>场景：把落在 (lower, upper) 区间的值替换成 newval，剥离无信息区间<br>限制：lower/upper/newval 必须是常数；level 未标注 | `lower=0.25, upper=0.75, newval=0.5` 把中间区间统一压成 0.5。 | 剥离「未申报/无信息」名称堆积出的中间密度，只保留两端的有效分位。 | 平台说明该 dataset 覆盖率仅约 0.23，NaN 转 0 会造出大量伪中性值，tail 是针对性清洗。 |
| **`ts_sum`**<br>(Time Series) | `ts_sum(x, d)`<br>scope **COMBO/REGULAR**<br>场景：过去 d 日求和，累计事件并保留发生频次<br>限制：仅 REGULAR/COMBO；与 ts_mean 不同，不会被天数除掉 | 对信念度做 220 日累计（另对显著性做 66 日累计）。 | 把稀疏申报累积成年度信号水平，并保留申报频次信息——平台说明特意指出不能用 ts_mean，否则会把「申报次数」除掉。 | 机构/内部人披露是低频事件，累计窗口是把事件流变成连续信号的必要手段。 |
| **`vec_avg`**<br>(Vector) | `vec_avg(x)`<br>scope **COMBO/REGULAR**<br>场景：把 VECTOR 字段逐元素取算术平均，转成每股票每日一个标量<br>限制：x 必须是 VECTOR 字段；仅 REGULAR/COMBO | 对 `inst1_tradesignificance` 向量取均值。 | 给出当日申报的平均显著性，作为过滤 routine filing 的依据。 | 同一日多笔披露重要性不同，均值比最大值更稳健。 |
| **`vec_sum`**<br>(Vector) | `vec_sum(x)`<br>scope **COMBO/REGULAR**<br>场景：把 VECTOR 字段所有元素求和，得到当日总量<br>限制：x 必须是 VECTOR 字段；仅 REGULAR/COMBO | 把 `inst1_valueeur`、`inst1_holdings` 两个 VECTOR 字段按日求和，得到当日申报总金额与总持仓。 | 为信念度比率提供分子与分母；用求和保留「当日多笔申报」的总规模。 | institutions1 是按申报逐条存向量的披露数据，类别场景需要日内总量。 |
| **`winsorize`**<br>(Cross Sectional) | `winsorize(x, std=4)`<br>scope **COMBO/REGULAR**<br>场景：把超出 ±std 个标准差的值截到边界，抑制极端值<br>限制：平台建议 std 取 2~5（分别剔除约 4.5%/0.27%/0.01%/0.0001% 极端值）；过小阈值会大幅改写分布 | `std=2` 把剩余极端值截到 ±2 个标准差。 | 限制少数巨额申报支配组合；平台建议 std 2~5，此处取最激进档。 | 披露金额分布极厚尾，INSTITUTIONS 类必须做截尾。 |

---

### 2.7 MODEL / 量化模型

**→ 代表 dataset：`predictive_starmine`**

- 选择依据：MODEL 类 63 条已提交样本中 `predictive_starmine` 被引用最多（20 条），GBR/TOP700 平台复验 631 个字段；`GrlqxwKx` 是纯单 dataset 样本，用 4 路估值/预期分位合成，能演示「多因子等权 + 中缀语法糖」的典型 MODEL 用法。
- 平台复验：`get_datafields(region=GBR, universe=TOP700, delay=1, dataset_id=predictive_starmine)` 返回 **631** 个字段；本 alpha 实际用到并命中：`ep_yield_pct_smest_fy1_3`, `ep_yield_pct_smest_fy2_3`, `forward_pe_smest_fy1_3`。

**→ 已提交 alpha：`GrlqxwKx`（平台名 `GBR_R_predictive_starmin_lqxwKx`）**

- 设置：`GBR/TOP700` · delay 1 · decay 4 · neutralization `SUBINDUSTRY`；提交日 `2026-08-17T14:28:38-04:00`；状态 OS/ACTIVE。
- 平台 IS 指标：Sharpe **1.8** / Fitness **1.28** / Turnover **0.1298**。
- 原始表达式：

```text
add(0.3 * rank(ts_av_diff(ep_yield_pct_smest_fy2_3, 20)), 0.233 * multiply(rank(forward_pe_smest_fy1_3), -1), 0.233 * rank(ep_yield_pct_smest_fy1_3), 0.233 * rank(ts_delta(ep_yield_pct_smest_fy1_3, 66)))
```

**表达式整体含义 / 想捕捉的信号**：平台未附有效描述，以下为基于字段与算子的解读：四个分位项加权合成——① FY2 盈利收益率相对 20 日均值的偏离（权重 0.3）；② FY1 远期 PE 分位取负（0.233）；③ FY1 盈利收益率水平分位（0.233）；④ FY1 盈利收益率 66 日变化分位（0.233）。同时奖励「便宜」（高盈利收益率、低 PE）与「预期上修」（收益率近期抬升/偏离均值为正）。

**辅助字段与归属**：三个字段全属 `predictive_starmine`；无跨 dataset 字段。表达式中的 `0.3 *`、`0.233 *` 是 multiply 的中缀语法糖。

**实际出现且在权限范围内的算子（5 个）**

| 算子（operator category） | 平台定义 · 允许用法(scope) · 适用场景与限制 | 对该 alpha 的数据做了什么处理 | 在最终信号中的具体作用与影响 | 为何适合该 dataset / category 场景 |
|---|---|---|---|---|
| **`add`**<br>(Arithmetic) | `add(x, y, filter=false), x + y`<br>scope **COMBO/REGULAR/SELECTION**<br>场景：逐元素相加，可多参数；把多路有界信号等权或加权合成<br>限制：filter=false 时 NaN 传播；filter=true 把 NaN 当 0，可提高覆盖 | 把四个加权项相加（add 的多参数形式）。 | 生成最终打分；四路共线但不完全重合，相加起到温和分散作用。 | MODEL 场景就是把同一模型族的不同视角合成为单一选股分数。 |
| **`multiply`**<br>(Arithmetic) | `multiply(x, y, ..., filter=false), x * y`<br>scope **COMBO/REGULAR/SELECTION**<br>场景：逐元素相乘，可多参数；加权、掩码、条件合成<br>限制：filter=false 时任一 NaN 使结果为 NaN | `multiply(rank(forward_pe...), -1)` 反转 PE 方向；`0.3 *` / `0.233 *` 施加权重。 | 决定每路得分的符号与贡献比例；PE 越低得分越高。 | 估值因子需要方向对齐（便宜=高分），加权则是多因子模型的基本表达。 |
| **`rank`**<br>(Cross Sectional) | `rank(x, rate=2)`<br>scope **COMBO/REGULAR**<br>场景：每日横截面分位（0~1）；消除量纲与极端值<br>限制：rate 控制排序精度，默认 2，设 0 为精确排序；仅 REGULAR/COMBO，不用于 SELECTION | 对三路原始量（偏离、远期 PE、盈利收益率、66 日变化）分别取截面分位。 | 把量纲不同的四个模型输出压到 0~1 同一尺度，使 0.3/0.233/0.233/0.233 的权重真正可比。 | MODEL 数据集常混合比率、百分比、评分字段，截面排序是唯一无歧义的归一方式。 |
| **`ts_av_diff`**<br>(Time Series) | `ts_av_diff(x, d) = x - ts_mean(x, d)`<br>scope **COMBO/REGULAR**<br>场景：当前值相对 d 日均值的偏离，忽略均值计算中的 NaN<br>限制：仅 REGULAR/COMBO | `ts_av_diff(ep_yield_pct_smest_fy2_3, 20)` 计算 FY2 盈利收益率相对其 20 日均值的偏离（忽略 NaN）。 | 第一路得分：捕捉估值相对近期中枢的抬升，权重最高（0.3）。 | MODEL 类输出多为已加工的模型分数，用「偏离自身中枢」比绝对值更能识别重定价。 |
| **`ts_delta`**<br>(Time Series) | `ts_delta(x, d)`<br>scope **COMBO/REGULAR**<br>场景：当前值减 d 日前值，测变化/动量<br>限制：仅 REGULAR/COMBO | `ts_delta(ep_yield_pct_smest_fy1_3, 66)` 取 FY1 盈利收益率的 66 日变化。 | 第四路得分：把预期/估值的中期动量纳入，防止只买静态便宜但持续恶化的名称。 | 分析师模型分数更新有惯性，季度级 delta 是该 dataset 的自然观察尺度。 |

> 中缀/一元语法糖实际出现：`multiply`，已按平台 definition 计入上表。

---

### 2.8 NEWS / 新闻

**→ 代表 dataset：`news17`**

- 选择依据：NEWS 类 13 条样本，`news17` 在 GBR/TOP700 平台复验 48 个字段；`58E7jkaN` 用到 10 个算子、覆盖 Vector/Cross Sectional/Time Series/Group/Arithmetic/Transformational 六类，是全轮覆盖面最广的样本之一，且平台附完整说明。
- 平台复验：`get_datafields(region=GBR, universe=TOP700, delay=1, dataset_id=news17)` 返回 **48** 个字段；本 alpha 实际用到并命中：`nws17_multiple_comp_event_similarity_days`, `nws17_multiple_comp_ssc`。

**→ 已提交 alpha：`58E7jkaN`（平台名 `GBR_R_news_ssc_sim_01`）**

- 设置：`GBR/TOP700` · delay 1 · decay 15 · neutralization `FAST`；提交日 `2026-10-30T03:36:53-04:00`；状态 OS/ACTIVE。
- 平台 IS 指标：Sharpe **1.85** / Fitness **1.14** / Turnover **0.0802**。
- 原始表达式：

```text
ts_target_tvr_decay(group_neutralize(-ts_rank(ts_mean(multiply(vec_count(nws17_multiple_comp_ssc), rank(vec_avg(nws17_multiple_comp_event_similarity_days))), 60), 252), densify(market)), target_tvr=0.05, lambda_max=5, lambda_min=0)
```

**表达式整体含义 / 想捕捉的信号**：平台描述：GBR 新闻关注度 × 事件相似度构成复合注意力，取 252 日时序分位后反向，再做市场中性化，捕捉新闻驱动的注意力均值回归。

**辅助字段与归属**：`market` 来自 pv1（PV 类）通用 GROUP 字段，经 densify 压缩后仅作中性化分组容器。两个 `nws17_*` 信号字段全属 `news17`。

**实际出现且在权限范围内的算子（10 个）**

| 算子（operator category） | 平台定义 · 允许用法(scope) · 适用场景与限制 | 对该 alpha 的数据做了什么处理 | 在最终信号中的具体作用与影响 | 为何适合该 dataset / category 场景 |
|---|---|---|---|---|
| **`densify`**<br>(Arithmetic) | `densify(x)`<br>scope **COMBO/REGULAR**<br>场景：把稀疏分组字段压成实际存在的桶，降低分组计算开销<br>限制：仅 REGULAR/COMBO；只用于分组字段 | 把 `market` 分组字段压缩为实际存在的桶。 | 不改变经济含义，只让 group_neutralize 在稀疏分组上高效计算。 | GBR/TOP700 的 market 桶数少但编号稀疏，NEWS 类高换手数据对计算效率敏感。 |
| **`group_neutralize`**<br>(Group) | `group_neutralize(x, group)`<br>scope **COMBO/REGULAR**<br>场景：组内减均值，剔除组共同暴露<br>限制：group 须为 GROUP 字段；仅 REGULAR/COMBO | 按 market 减去组内均值。 | 剔除全市场共同的新闻浪潮，只保留个股相对注意力差异。 | 宏观新闻会同时抬高所有股票的覆盖率，不做市场中性化会得到伪 beta。 |
| **`multiply`**<br>(Arithmetic) | `multiply(x, y, ..., filter=false), x * y`<br>scope **COMBO/REGULAR/SELECTION**<br>场景：逐元素相乘，可多参数；加权、掩码、条件合成<br>限制：filter=false 时任一 NaN 使结果为 NaN | 事件条数 × 相似度分位，形成复合注意力强度。 | 决定后续时序比较的对象；只有「多且相似」的新闻簇才推高注意力。 | NEWS 场景要区分真实新闻冲击与重复转载，乘积同时编码强度与集中度。 |
| **`rank`**<br>(Cross Sectional) | `rank(x, rate=2)`<br>scope **COMBO/REGULAR**<br>场景：每日横截面分位（0~1）；消除量纲与极端值<br>限制：rate 控制排序精度，默认 2，设 0 为精确排序；仅 REGULAR/COMBO，不用于 SELECTION | 把相似度天数字段映射到截面分位。 | 让「相似度」与「事件条数」在可相乘的尺度上组合，抑制极端相似度值。 | 不同公司新闻覆盖量差异极大，截面排序可避免大公司天然占优。 |
| **`reverse`**<br>(Arithmetic) | `reverse(x), -x`<br>scope **COMBO/REGULAR/SELECTION**<br>场景：取相反数；翻转信号方向<br>限制：无参数限制，但对 NaN 仍返回 NaN | 一元负号把时序分位取反。 | 把「注意力高位」映射为负向头寸，实现 fade。 | 平台描述明确该信号为注意力均值回归，方向必须翻转。 |
| **`ts_mean`**<br>(Time Series) | `ts_mean(x, d)`<br>scope **COMBO/REGULAR**<br>场景：过去 d 日均值，平滑噪声、提取慢变量<br>限制：仅 REGULAR/COMBO；d 为交易日数 | 对复合注意力做 60 日平滑。 | 把日度新闻尖峰抹成季度级注意力水平；窗口决定均值回归的观察期。 | 新闻到达是点过程，平滑后才能定义「相对过去一年的高位」。 |
| **`ts_rank`**<br>(Time Series) | `ts_rank(x, d, constant=0)`<br>scope **COMBO/REGULAR**<br>场景：当前值在过去 d 日自身序列中的分位，突出时序相对高低<br>限制：仅 REGULAR/COMBO；constant 可平移输出 | 取 252 日窗口内当前平滑值的时序分位。 | 把注意力转成「过去一年中处于多高位置」，是反向信号的直接输入。 | 均值回归需要相对自身历史的极值判定，而不是跨公司横向比较。 |
| **`ts_target_tvr_decay`**<br>(Time Series) | `ts_target_tvr_decay(x, lambda_min=0, lambda_max=1, target_tvr=0.1)`<br>scope **COMBO/REGULAR**<br>场景：在 lambda 区间内自动调 decay，使换手命中目标值<br>限制：level 未标注、无详细文档页；仅 REGULAR/COMBO | 在 lambda 0~5 范围内自动调 decay，使换手命中 `target_tvr=0.05`。 | 作为最外层，直接把最终信号平滑到目标换手，是该 alpha 低换手（TO 0.0802）的主要来源。 | 新闻注意力信号换手偏高而提交要求换手受限，NEWS 类常用目标换手型平滑。 |
| **`vec_avg`**<br>(Vector) | `vec_avg(x)`<br>scope **COMBO/REGULAR**<br>场景：把 VECTOR 字段逐元素取算术平均，转成每股票每日一个标量<br>限制：x 必须是 VECTOR 字段；仅 REGULAR/COMBO | 对 `nws17_multiple_comp_event_similarity_days` 向量取均值，得到平均事件相似度天数。 | 提供「新闻是否重复/聚类」的标量，参与注意力的加权。 | 新闻类数据的语义在「事件簇」而非单条，跨记录平均是合理汇总。 |
| **`vec_count`**<br>(Vector) | `vec_count(x)`<br>scope **COMBO/REGULAR**<br>场景：返回 VECTOR 字段的元素个数，衡量事件条数/覆盖广度<br>限制：level 未标注；仅 REGULAR/COMBO | 数出 `nws17_multiple_comp_ssc` 向量中的元素个数，得到当日多公司 SSC 事件条数。 | 作为「关注度」的分子/主体，决定复合注意力的量级。 | news17 把同一天多条新闻事件存成向量，事件条数本身就是覆盖广度的度量。 |

---

### 2.9 OTHER / 其他替代数据

**→ 代表 dataset：`insider_feats`**

- 选择依据：OTHER 类 45 条样本，`insider_feats` 在 KOR/TOP600 平台复验 31 个字段；`pwjpKGJ3` 是纯单 dataset 样本，6 个算子覆盖 Time Series/Cross Sectional/Arithmetic 三类，且含 scale 这类少见的仓位归一算子。
- 平台复验：`get_datafields(region=KOR, universe=TOP600, delay=1, dataset_id=insider_feats)` 返回 **31** 个字段；本 alpha 实际用到并命中：`buy_sell_ratio_top20_250d_filled`, `buy_sell_tx_count_ratio_all_60d_filled`。

**→ 已提交 alpha：`pwjpKGJ3`（平台名 `0.5763`）**

- 设置：`KOR/TOP600` · delay 1 · decay 10 · neutralization `STATISTICAL`；提交日 `2026-09-02T00:05:36-04:00`；状态 OS/ACTIVE。
- 平台 IS 指标：Sharpe **1.65** / Fitness **1.38** / Turnover **0.1046**。
- 原始表达式：

```text
scale(add(multiply(0.3, rank(ts_backfill(buy_sell_tx_count_ratio_all_60d_filled, 60))), multiply(0.7, ts_delta(rank(ts_backfill(buy_sell_ratio_top20_250d_filled, 60)), 20))))
```

**表达式整体含义 / 想捕捉的信号**：平台描述：用散户/机构订单流失衡预测韩股收益，近期大单变化的权重（0.7）高于广谱参与失衡（0.3）。两路各自截面标准化后加权合成，最后归一到单位敞口。

**辅助字段与归属**：两个字段全属 `insider_feats`；标签含 `CH_PPA` / `PowerPoolSelected`，但平台状态为 OS/ACTIVE REGULAR，属于已提交 alpha。

**实际出现且在权限范围内的算子（6 个）**

| 算子（operator category） | 平台定义 · 允许用法(scope) · 适用场景与限制 | 对该 alpha 的数据做了什么处理 | 在最终信号中的具体作用与影响 | 为何适合该 dataset / category 场景 |
|---|---|---|---|---|
| **`add`**<br>(Arithmetic) | `add(x, y, filter=false), x + y`<br>scope **COMBO/REGULAR/SELECTION**<br>场景：逐元素相加，可多参数；把多路有界信号等权或加权合成<br>限制：filter=false 时 NaN 传播；filter=true 把 NaN 当 0，可提高覆盖 | 把两路加权项相加。 | 形成最终混合信号，兼顾水平与变化两个时间尺度。 | 订单流的「参与广度」与「大单动量」互补，相加即可合成。 |
| **`multiply`**<br>(Arithmetic) | `multiply(x, y, ..., filter=false), x * y`<br>scope **COMBO/REGULAR/SELECTION**<br>场景：逐元素相乘，可多参数；加权、掩码、条件合成<br>限制：filter=false 时任一 NaN 使结果为 NaN | 分别施加 0.3 与 0.7 权重。 | 决定两路合成比例；突出近期知情大单、弱化广谱噪声。 | OTHER 类混合特征质量参差，显式加权比等权更能表达先验。 |
| **`rank`**<br>(Cross Sectional) | `rank(x, rate=2)`<br>scope **COMBO/REGULAR**<br>场景：每日横截面分位（0~1）；消除量纲与极端值<br>限制：rate 控制排序精度，默认 2，设 0 为精确排序；仅 REGULAR/COMBO，不用于 SELECTION | 把广谱参与失衡与大单比率各自映射到截面分位。 | 把不同口径的比率统一到 0~1，使 0.3/0.7 权重有意义。 | 订单流比率分布偏斜且含极端值，截面排序是标准稳健化。 |
| **`scale`**<br>(Cross Sectional) | `scale(x, scale=1, longscale=1, shortscale=1)`<br>scope **COMBO/REGULAR**<br>场景：把权重绝对值之和缩放到目标 book size，可分别缩放多空<br>限制：仅 REGULAR/COMBO | 把合成信号缩放到绝对权重之和为 1（默认 scale=1）。 | 作为最外层控制组合总敞口与多空规模；不这一步，信号幅度会随市场覆盖率漂移。 | KOR/TOP600 覆盖变化较大，OTHER 类混合信号需要显式归一到固定 book size。 |
| **`ts_backfill`**<br>(Time Series) | `ts_backfill(x, lookback=d, k=1)`<br>scope **COMBO/REGULAR**<br>场景：用回看窗口内最近有效值填补 NaN，提高覆盖率、降低回撤风险<br>限制：只在 lookback 窗口内有效；k 可取第 k 个最近有效值；稀疏数据窗口外的 NaN 不会被填 | 对两个 `_filled` 订单流比率各做 60 日窗口回填。 | 补齐稀疏交易日的 NaN，保证 rank / ts_delta 有连续输入；窗口外的缺口仍为空。 | 订单流衍生比率覆盖不全，OTHER 类混合特征尤其依赖回填后才能做时序差分。 |
| **`ts_delta`**<br>(Time Series) | `ts_delta(x, d)`<br>scope **COMBO/REGULAR**<br>场景：当前值减 d 日前值，测变化/动量<br>限制：仅 REGULAR/COMBO | 对大单比率的排名取 20 日变化。 | 把「大单失衡水平」变成「大单失衡动量」，是权重最高（0.7）的得分来源。 | 平台说明大单变化比水平更能代表知情交易的方向演进。 |

---

### 2.10 PV / 价量

**→ 代表 dataset：`intraday_pv_feats`**

- 选择依据：PV 类样本最多（193 条），`intraday_pv_feats` 在 HKG/TOP800 平台复验 579 个字段；`gJZ6pONl` 用到 10 个算子、5 个算子类别，且含中缀比较语法糖与 trade_when 条件持仓，最能演示盘中价量数据的完整加工链。
- 平台复验：`get_datafields(region=HKG, universe=TOP800, delay=1, dataset_id=intraday_pv_feats)` 返回 **579** 个字段；本 alpha 实际用到并命中：`mean_last_trade_price_return_30m_pre_close_2`, `mean_trade_volume_30m_pre_close_2`。

**→ 已提交 alpha：`gJZ6pONl`（平台名 `HKG_R_preclose30mrev_01`）**

- 设置：`HKG/TOP800` · delay 1 · decay 12 · neutralization `INDUSTRY`；提交日 `2026-09-30T09:00:31-04:00`；状态 OS/ACTIVE。
- 平台 IS 指标：Sharpe **2.87** / Fitness **1.37** / Turnover **0.6894**。
- 原始表达式：

```text
trade_when(rank(divide(mean_trade_volume_30m_pre_close_2, ts_mean(volume, 22))) > 0.5, signed_power(subtract(0.5, group_rank(ts_decay_linear(mean_last_trade_price_return_30m_pre_close_2, 4), industry)), 0.5), rank(divide(mean_trade_volume_30m_pre_close_2, ts_mean(volume, 22))) < 0.3)
```

**表达式整体含义 / 想捕捉的信号**：平台描述：港股尾盘 30 分钟价格异动在下一交易日倾向部分回撤，但只在收盘成交量占比偏高时交易——放量代表真实订单流失衡，缩量时的异动多为稀薄成交造成的伪信号。

**辅助字段与归属**：`volume`、`industry` 来自 pv1（PV 类），同 category；前者作 22 日基线、后者作分组容器。两个 `mean_*_30m_pre_close_2` 字段来自 `intraday_pv_feats`。

**实际出现且在权限范围内的算子（10 个）**

| 算子（operator category） | 平台定义 · 允许用法(scope) · 适用场景与限制 | 对该 alpha 的数据做了什么处理 | 在最终信号中的具体作用与影响 | 为何适合该 dataset / category 场景 |
|---|---|---|---|---|
| **`divide`**<br>(Arithmetic) | `divide(x, y), x / y`<br>scope **COMBO/REGULAR/SELECTION**<br>场景：逐元素相除；构造比率、归一到相对量<br>限制：分母为 0 会报错；平台建议 divide(x, add(y, 0.0001)) 加 epsilon | 尾盘 30 分钟成交量 ÷ 22 日基线，得到收盘放量倍数。 | 构造开/平仓状态量；比值越大说明当日尾盘越受关注。 | 价量类信号应归一到相对量，才能跨市值、跨流动性比较。 |
| **`greater`**<br>(Logical) | `input1 > input2`<br>scope **COMBO/REGULAR/SELECTION**<br>场景：大于返回 1；把连续量转成触发布尔<br>限制：比较结果为 0/1，常与 trade_when / if_else 联用 | 中缀 `> 0.5` 生成开仓触发（等价 greater 定义 `input1 > input2`）。 | 放量排名进入上半区才允许建仓。 | PV 事件型条件天然是布尔逻辑，中缀写法即平台允许的 greater 语法糖。 |
| **`group_rank`**<br>(Group) | `group_rank(x, group)`<br>scope **COMBO/REGULAR**<br>场景：组内分位（0~1）；只比较同行业/同板块/同聚类内的相对位置<br>限制：group 须为 GROUP 字段；仅 REGULAR/COMBO | 在 industry 内取平滑收益的分位。 | 去掉行业共同方向，只保留行业内相对强弱。 | 港股行业轮动强烈，组内比较才能隔离尾盘个股异动。 |
| **`less`**<br>(Logical) | `input1 < input2`<br>scope **COMBO/REGULAR/SELECTION**<br>场景：小于返回 1；构造退出条件<br>限制：比较结果为 0/1 | 中缀 `< 0.3` 生成退出条件。 | 放量退潮即平仓（z 优先）；与 0.5 形成滞回带，抑制反复开平。 | 尾盘关注度衰减后反转逻辑失效，需要明确离场。 |
| **`rank`**<br>(Cross Sectional) | `rank(x, rate=2)`<br>scope **COMBO/REGULAR**<br>场景：每日横截面分位（0~1）；消除量纲与极端值<br>限制：rate 控制排序精度，默认 2，设 0 为精确排序；仅 REGULAR/COMBO，不用于 SELECTION | 把放量倍数映成 0~1 截面分位。 | 使 0.5 / 0.3 阈值跨日稳定可比。 | 成交量倍数右偏严重，分位比原始比值更适合做状态阈值。 |
| **`signed_power`**<br>(Arithmetic) | `signed_power(x, y) = sign(x)*abs(x)^y`<br>scope **COMBO/REGULAR/SELECTION**<br>场景：保号幂变换；y<1 压缩极端、y>1 放大强信号<br>限制：与 power 不同：负输入不会丢符号；y 非整数时 power 会丢符号 | `signed_power(..., 0.5)` 做保号开方。 | 压缩极端排名的影响，使组合不被少数几只暴涨暴跌股主导；保号保证多空方向不变。 | 港股尾盘收益厚尾，需非线性压缩但绝不能丢符号——这正是 signed_power 相对 power 的价值。 |
| **`subtract`**<br>(Arithmetic) | `subtract(x, y, filter=false), x - y`<br>scope **COMBO/REGULAR/SELECTION**<br>场景：逐元素左到右相减；构造差值、中心化、价差<br>限制：NaN 传播；多参数按 ((a-b)-c) 计算 | `subtract(0.5, group_rank(...))` 中心化并反向。 | 尾盘涨幅最大的得负分（预期回撤），输出落在 -0.5~+0.5，实现反转方向。 | 平台描述明确为 late-session reversal，0.5 中心化同时保证多空对称。 |
| **`trade_when`**<br>(Transformational) | `trade_when(x, y, z)`<br>scope **COMBO/REGULAR**<br>场景：x 为真才更新为 y，z 为真平仓为 NaN，其余保持前值；事件驱动 + 降换手<br>限制：z 优先于 x；z 为真输出 NaN（无持仓）；仅 REGULAR/COMBO | 触发为真时写入反转头寸、退出为真时置 NaN、其余日保持前值。 | 整条 alpha 的结构骨架；决定持仓持续性，也是 TO 0.6894 的主要约束点。 | 收盘竞价是离散事件，条件持有比连续打分更贴合 HKG 微观结构。 |
| **`ts_decay_linear`**<br>(Time Series) | `ts_decay_linear(x, d, dense=false)`<br>scope **COMBO/REGULAR**<br>场景：近端权重高的线性加权平滑，降换手、抑制跳跃<br>限制：默认稀疏模式把 NaN 当 0；dense=true 不替换 NaN；仅 REGULAR/COMBO | 对尾盘 30 分钟收益率做 4 日线性衰减平滑。 | 把隔夜跳动的收益序列变成可交易慢变量，减少单日噪声与换手。 | 盘中收益在日频重采样时噪声大，PV 类常用短窗线性衰减。 |
| **`ts_mean`**<br>(Time Series) | `ts_mean(x, d)`<br>scope **COMBO/REGULAR**<br>场景：过去 d 日均值，平滑噪声、提取慢变量<br>限制：仅 REGULAR/COMBO；d 为交易日数 | 对 `volume` 做 22 日均值，得到正常成交量基线。 | 为放量倍数提供分母；窗口 ~1 个月，决定「异常放量」的判定基准。 | 港股收盘竞价成交量有稳定日间节律，PV 场景必须用自身历史基线而非全市场均值。 |

> 中缀/一元语法糖实际出现：`greater, less`，已按平台 definition 计入上表。

---

### 2.11 RISK / 风险因子

**→ 代表 dataset：`risk70`**

- 选择依据：RISK 类 20 条样本，`risk70` 在 KOR/TOP600 平台复验 96 个字段；`6Xdo27P5` 是纯信号样本且用到 vector_neut 正交化 + winsorize + signed_power 三层风险处理，最能体现风险因子 dataset 的用法。
- 平台复验：`get_datafields(region=KOR, universe=TOP600, delay=1, dataset_id=risk70)` 返回 **96** 个字段；本 alpha 实际用到并命中：`rsk70_mfm2_asetrd_anlystsn`, `rsk70_mfm2_asetrd_momentum`。

**→ 已提交 alpha：`6Xdo27P5`（平台名 `KOR_R_rsk70anmom_01`）**

- 设置：`KOR/TOP600` · delay 1 · decay 1 · neutralization `REVERSION_AND_MOMENTUM`；提交日 `2026-11-06T13:59:38-05:00`；状态 OS/ACTIVE。
- 平台 IS 指标：Sharpe **1.68** / Fitness **1.3** / Turnover **0.1201**。
- 原始表达式：

```text
signed_power(group_rank(winsorize(vector_neut(rank(rsk70_mfm2_asetrd_anlystsn), rank(rsk70_mfm2_asetrd_momentum)), std=0.38), exchange), 4)
```

**表达式整体含义 / 想捕捉的信号**：平台描述：把分析师情绪修正对动量做正交化，残差即「市场尚未定价的预期漂移」；随后截尾、交易所内排序、并用 4 次保号幂把权重集中到最强残差。

**辅助字段与归属**：`exchange` 来自 pv1（PV 类）通用 GROUP 字段，仅作分组容器；两个 `rsk70_*` 信号字段全属 `risk70`。

**实际出现且在权限范围内的算子（5 个）**

| 算子（operator category） | 平台定义 · 允许用法(scope) · 适用场景与限制 | 对该 alpha 的数据做了什么处理 | 在最终信号中的具体作用与影响 | 为何适合该 dataset / category 场景 |
|---|---|---|---|---|
| **`group_rank`**<br>(Group) | `group_rank(x, group)`<br>scope **COMBO/REGULAR**<br>场景：组内分位（0~1）；只比较同行业/同板块/同聚类内的相对位置<br>限制：group 须为 GROUP 字段；仅 REGULAR/COMBO | 在 exchange 内取残差分位（0~1）。 | 把限幅后的残差重新拉开为相对排名，决定最终多头/空头顺序。 | KOR 市场不同板块/交易所流动性与披露节奏不同，组内排序更稳健。 |
| **`rank`**<br>(Cross Sectional) | `rank(x, rate=2)`<br>scope **COMBO/REGULAR**<br>场景：每日横截面分位（0~1）；消除量纲与极端值<br>限制：rate 控制排序精度，默认 2，设 0 为精确排序；仅 REGULAR/COMBO，不用于 SELECTION | 把 `rsk70_mfm2_asetrd_anlystsn` 与 `rsk70_mfm2_asetrd_momentum` 各自取截面分位。 | 在正交化前把两个不同量纲的风险描述符放到同一尺度，避免投影被数值尺度主导。 | risk70 输出的是多源风险暴露分数，量纲不一致，截面排序是正交化前的必要预处理。 |
| **`signed_power`**<br>(Arithmetic) | `signed_power(x, y) = sign(x)*abs(x)^y`<br>scope **COMBO/REGULAR/SELECTION**<br>场景：保号幂变换；y<1 压缩极端、y>1 放大强信号<br>限制：与 power 不同：负输入不会丢符号；y 非整数时 power 会丢符号 | `signed_power(..., 4)` 对中心化前的分位做 4 次保号幂。 | 把权重高度集中到分位两端的强残差，中间名次近乎归零；保号确保多空不混淆。 | 风险残差信号通常只有极端分位有效，幂变换能表达「只交易最显著偏离」。 |
| **`vector_neut`**<br>(Cross Sectional) | `vector_neut(x, y)`<br>scope **COMBO/REGULAR**<br>场景：把 x 对 y 做正交投影剔除，输出与 y 正交的残差<br>限制：level 未标注；仅 REGULAR/COMBO；要求 x、y 同维度 | 把分析师分位向量对动量分位向量做投影并剔除，输出与动量正交的残差。 | 整条 alpha 的经济核心：去掉已被动量解释的部分，只留下独立的预期修正信息。 | RISK 类 dataset 的用途正是构造/剥离风险暴露，正交化比简单相减更严格。 |
| **`winsorize`**<br>(Cross Sectional) | `winsorize(x, std=4)`<br>scope **COMBO/REGULAR**<br>场景：把超出 ±std 个标准差的值截到边界，抑制极端值<br>限制：平台建议 std 取 2~5（分别剔除约 4.5%/0.27%/0.01%/0.0001% 极端值）；过小阈值会大幅改写分布 | `std=0.38` 把残差截到 ±0.38 个标准差内。 | 大幅压平残差分布，为后续 4 次幂放大做准备；注意平台建议 std 2~5，此处远低于建议区间，属于激进改写分布。 | 正交残差在覆盖边缘会产生尖峰，需先限幅再放大强信号；但阈值过小会损失大量横截面信息。 |

---

### 2.12 SENTIMENT / 情绪/关注度

**→ 代表 dataset：`sentiment7`**

- 选择依据：SENTIMENT 类 10 条样本，`sentiment7` 在 DEU/TOP500 平台复验 3 个字段；`bl6OWZ2M` 用到 8 个算子且覆盖 Vector/Time Series/Arithmetic/Cross Sectional 四类，是全轮唯一演示「多语言浏览量 → 时序分位正态化 → 跨来源正交化」完整链条的样本。
- 平台复验：`get_datafields(region=DEU, universe=TOP500, delay=1, dataset_id=sentiment7)` 返回 **3** 个字段；本 alpha 实际用到并命中：`snt7_all_languages_views`。

**→ 已提交 alpha：`bl6OWZ2M`（平台名 `DEU_R_alpha_01`）**

- 设置：`DEU/TOP500` · delay 1 · decay 2 · neutralization `SUBINDUSTRY`；提交日 `2026-11-04T10:02:17-05:00`；状态 OS/ACTIVE。
- 平台 IS 指标：Sharpe **2.03** / Fitness **1.61** / Turnover **0.161**。
- 原始表达式：

```text
a = ts_backfill(vec_avg(snt7_all_languages_views), 22);
vector_neut(ts_quantile(ts_ir(ts_mean(max(a, ts_delay(a, 5)), 5), 22), 252, driver="gaussian"), ts_backfill(vec_avg(snl27_relpopularity08), 22))
```

**表达式整体含义 / 想捕捉的信号**：平台未附描述，以下为基于字段与算子的解读：把多语言维基浏览量向量取均值、22 日回填后，与 5 日前值取 max（只保留关注度抬升、忽略回落），再做 5 日均值和 22 日信息比，经 252 日高斯分位变换正态化，最后对 `sentiment27` 的网站流行度做正交化——得到「剥离互联网整体热度后的公司特定关注度」。

**辅助字段与归属**：主信号 `snt7_all_languages_views` 属 `sentiment7`；正交基准 `snl27_relpopularity08` 属 `sentiment27`，两者同属 SENTIMENT 类，未跨 category。变量 `a =` 是表达式内的中间赋值，不是算子。

**实际出现且在权限范围内的算子（8 个）**

| 算子（operator category） | 平台定义 · 允许用法(scope) · 适用场景与限制 | 对该 alpha 的数据做了什么处理 | 在最终信号中的具体作用与影响 | 为何适合该 dataset / category 场景 |
|---|---|---|---|---|
| **`max`**<br>(Arithmetic) | `max(x, y, ..)`<br>scope **COMBO/REGULAR/SELECTION**<br>场景：取多个输入的最大值；构造下界/只保留上行变化<br>限制：至少 2 个输入 | `max(a, ts_delay(a,5))` 取当前与 5 日前较大者。 | 构造单边 Attention：关注度回落时不下调，只保留抬升；这决定信号是「累积关注」而非「净变化」。 | SENTIMENT 场景常认为注意力冲击有黏性，max 编码了这种不对称。 |
| **`ts_backfill`**<br>(Time Series) | `ts_backfill(x, lookback=d, k=1)`<br>scope **COMBO/REGULAR**<br>场景：用回看窗口内最近有效值填补 NaN，提高覆盖率、降低回撤风险<br>限制：只在 lookback 窗口内有效；k 可取第 k 个最近有效值；稀疏数据窗口外的 NaN 不会被填 | 22 日窗口回填浏览量 NaN。 | 保证 max / ts_mean / ts_ir 有连续序列；窗口外长期缺失仍为空。 | 网页浏览量数据稀疏且上报延迟，SENTIMENT 类几乎必须回填。 |
| **`ts_delay`**<br>(Time Series) | `ts_delay(x, d)`<br>scope **COMBO/REGULAR**<br>场景：取 d 日前的值，构造滞后基准<br>限制：仅 REGULAR/COMBO | 取 5 日前的回填值。 | 为 max 提供比较基准，定义「关注度是否较 5 日前抬升」。 | 关注度是短周期流量，周级滞后比日级更能过滤上报噪声。 |
| **`ts_ir`**<br>(Time Series) | `ts_ir(x, d) = ts_mean(x,d)/ts_std_dev(x,d)`<br>scope **COMBO/REGULAR**<br>场景：滚动信息比，衡量单位波动带来的平均水平<br>限制：level 未标注；分母接近 0 时数值不稳定 | `ts_ir(..., 22)` = 22 日均值 / 22 日标准差，即滚动信息比。 | 把「关注度高」升级为「关注度稳定地高」，决定后续分位变换的输入。 | 舆论热度需要区分持续关注与一次性爆点，信息比是 SENTIMENT 类常用稳健度度量。 |
| **`ts_mean`**<br>(Time Series) | `ts_mean(x, d)`<br>scope **COMBO/REGULAR**<br>场景：过去 d 日均值，平滑噪声、提取慢变量<br>限制：仅 REGULAR/COMBO；d 为交易日数 | 对 max 结果做 5 日均值。 | 平滑单边序列，为信息比提供均值项。 | 短窗平滑适配浏览量的日频抖动。 |
| **`ts_quantile`**<br>(Time Series) | `ts_quantile(x, d, driver="gaussian")`<br>scope **COMBO/REGULAR**<br>场景：先做 d 日时序分位，再经分布逆 CDF 变换，把序列正态化<br>限制：driver 支持 gaussian/uniform/cauchy；仅 REGULAR/COMBO | `ts_quantile(..., 252, driver="gaussian")` 先做一年时序分位，再经高斯逆 CDF 映射。 | 把有偏的信息比分布正态化，尾部被重新拉开；直接影响正交化后的权重分布。 | 浏览量分布极端右偏，高斯化能让跨股票、跨时期的关注度可比。 |
| **`vec_avg`**<br>(Vector) | `vec_avg(x)`<br>scope **COMBO/REGULAR**<br>场景：把 VECTOR 字段逐元素取算术平均，转成每股票每日一个标量<br>限制：x 必须是 VECTOR 字段；仅 REGULAR/COMBO | 把 `snt7_all_languages_views` 多语言浏览量向量取均值，得到每股票每日单一浏览量。 | 为整条链提供输入；均值而非求和可避免语言数量随时间变化造成假趋势。 | sentiment7 按语言/来源分向量存储，类别场景需要跨来源汇总而非单一语言。 |
| **`vector_neut`**<br>(Cross Sectional) | `vector_neut(x, y)`<br>scope **COMBO/REGULAR**<br>场景：把 x 对 y 做正交投影剔除，输出与 y 正交的残差<br>限制：level 未标注；仅 REGULAR/COMBO；要求 x、y 同维度 | 把上述信号对 `snl27_relpopularity08`（网站流行度，同样 22 日回填 + 向量均值）做正交化。 | 剥离「公司官网整体流量」这一共同成分，只留下与泛热度无关的增量关注；是最终输出的最后一步。 | SENTIMENT 类最大的混杂是全网/全站流量趋势，跨数据集正交化正是该类别的标准净化手段。 |

---

### 2.13 SHORTINTEREST / 卖空/融券

**→ 代表 dataset：`shortinterest38`**

- 选择依据：SHORTINTEREST 类 22 条样本，`shortinterest38` 在 KOR/TOP600 平台复验 80 个字段；`O08kz5Mv` 是纯信号样本、8 个算子覆盖 Vector/Arithmetic/Time Series/Group/Cross Sectional 五类，含少见的 quantile 分布变换。
- 平台复验：`get_datafields(region=KOR, universe=TOP600, delay=1, dataset_id=shortinterest38)` 返回 **80** 个字段；本 alpha 实际用到并命中：`shrt38_accum_buy_amt`, `shrt38_accum_net_buy_amt`, `shrt38_accum_sell_amt`。

**→ 已提交 alpha：`O08kz5Mv`**

- 设置：`KOR/TOP600` · delay 1 · decay 4 · neutralization `STATISTICAL`；提交日 `2026-10-04T00:57:34-04:00`；状态 OS/ACTIVE。
- 平台 IS 指标：Sharpe **2.16** / Fitness **1.65** / Turnover **0.1831**。
- 原始表达式：

```text
multiply(-1, quantile(group_rank(ts_backfill(ts_rank(divide(vec_sum(shrt38_accum_net_buy_amt), add(vec_sum(shrt38_accum_buy_amt), vec_sum(shrt38_accum_sell_amt))), 462), 66), sector)))
```

**表达式整体含义 / 想捕捉的信号**：平台未附描述，以下为基于字段与算子的解读：用累计净买入额 ÷（累计买入额 + 累计卖出额）构造「净买压比率」，取 462 日（约两年）时序分位并回填，再在行业内取分位、经高斯分位变换，最后取负。捕捉买压长期处于历史高位后的拥挤反转。

**辅助字段与归属**：`sector` 来自 pv1（PV 类）通用 GROUP 字段，仅作分组容器；三个 `shrt38_*` 金额字段全属 `shortinterest38`。

**实际出现且在权限范围内的算子（8 个）**

| 算子（operator category） | 平台定义 · 允许用法(scope) · 适用场景与限制 | 对该 alpha 的数据做了什么处理 | 在最终信号中的具体作用与影响 | 为何适合该 dataset / category 场景 |
|---|---|---|---|---|
| **`add`**<br>(Arithmetic) | `add(x, y, filter=false), x + y`<br>scope **COMBO/REGULAR/SELECTION**<br>场景：逐元素相加，可多参数；把多路有界信号等权或加权合成<br>限制：filter=false 时 NaN 传播；filter=true 把 NaN 当 0，可提高覆盖 | 买入额 + 卖出额构造分母（总交易额）。 | 把净买压归一到 [-1, 1] 区间，消除规模效应。 | 做空/买卖金额随市值差异巨大，比率化是 SHORTINTEREST 类的必要步骤。 |
| **`divide`**<br>(Arithmetic) | `divide(x, y), x / y`<br>scope **COMBO/REGULAR/SELECTION**<br>场景：逐元素相除；构造比率、归一到相对量<br>限制：分母为 0 会报错；平台建议 divide(x, add(y, 0.0001)) 加 epsilon | 净买入额 ÷ 总交易额，得到净买压比率。 | 整条信号的主干；决定后续时序分位衡量的「拥挤程度」。 | 平台 divide 明确警告分母为 0 会报错、建议加 epsilon；本式未加，零成交日依赖平台 NaN 处理，是已知限制。 |
| **`group_rank`**<br>(Group) | `group_rank(x, group)`<br>scope **COMBO/REGULAR**<br>场景：组内分位（0~1）；只比较同行业/同板块/同聚类内的相对位置<br>限制：group 须为 GROUP 字段；仅 REGULAR/COMBO | 在 sector 内取分位。 | 把时序拥挤度转成行业内相对排名，剔除行业整体做空偏好差异。 | 不同行业卖空活跃度结构性不同，组内比较才公平。 |
| **`multiply`**<br>(Arithmetic) | `multiply(x, y, ..., filter=false), x * y`<br>scope **COMBO/REGULAR/SELECTION**<br>场景：逐元素相乘，可多参数；加权、掩码、条件合成<br>限制：filter=false 时任一 NaN 使结果为 NaN | `multiply(-1, ...)` 对整条信号取负。 | 把「买压高位」翻成负向头寸，实现拥挤反转；决定最终多空符号。 | 平台常见做法：卖空/买压极度拥挤后预期反转，方向需翻转。 |
| **`quantile`**<br>(Cross Sectional) | `quantile(x, driver=gaussian, sigma=1.0)`<br>scope **COMBO/REGULAR**<br>场景：截面排序后按分布逆 CDF 重映射，压尾部<br>限制：driver 可选 gaussian/cauchy/uniform；仅 REGULAR/COMBO | 把组内分位经高斯逆 CDF 重映射。 | 重新拉开两端、压缩中部，使最终头寸更集中在极端拥挤/极端冷清的名称。 | 买压分位在中部堆积，SHORTINTEREST 信号主要来自尾部，分布变换强化有效区间。 |
| **`ts_backfill`**<br>(Time Series) | `ts_backfill(x, lookback=d, k=1)`<br>scope **COMBO/REGULAR**<br>场景：用回看窗口内最近有效值填补 NaN，提高覆盖率、降低回撤风险<br>限制：只在 lookback 窗口内有效；k 可取第 k 个最近有效值；稀疏数据窗口外的 NaN 不会被填 | 对时序分位做 66 日回填。 | 填补申报/停牌造成的缺口，让 group_rank 有连续截面。 | shortinterest 类数据披露低频不规则，回填是必需工序。 |
| **`ts_rank`**<br>(Time Series) | `ts_rank(x, d, constant=0)`<br>scope **COMBO/REGULAR**<br>场景：当前值在过去 d 日自身序列中的分位，突出时序相对高低<br>限制：仅 REGULAR/COMBO；constant 可平移输出 | 对比率取 462 日时序分位。 | 把当日买压转成「相对近两年自身历史的位置」，是拥挤度判定的核心。 | 卖空/买压水平有强个股固定效应，时序比较比横截面比较更有意义。 |
| **`vec_sum`**<br>(Vector) | `vec_sum(x)`<br>scope **COMBO/REGULAR**<br>场景：把 VECTOR 字段所有元素求和，得到当日总量<br>限制：x 必须是 VECTOR 字段；仅 REGULAR/COMBO | 把 `shrt38_accum_net_buy_amt`、`..._buy_amt`、`..._sell_amt` 三个 VECTOR 金额字段各按日求和。 | 把逐笔/逐账户的做空相关金额汇总成可比的日度总量，是比率三项的来源。 | shortinterest38 按交易记录或账户存向量，类别场景需要日内总买压。 |

---

## 3 无可用样本（明确标注并跳过）

| category | 判定 | 证据 |
|---|---|---|
| **MACRO** / 宏观·指数 | **无可用样本** | 260 条 ACTIVE REGULAR 中仅 2 条引用 `macro63`（`0mr6mLAq`、`9qWmZM8d`），字段都是 `mcr63_membership`。平台 `regular.description` 原文写明：「*mcr63_membership (Macro category, index reconstitution membership) is declared so the alpha is attributed to the Macro pyramid; it is identically zero across the IND panel and therefore contributes no signal*」。两条的时序信号主体全部来自 `other532`（OTHER 类）。把零常数挂塔当作 MACRO 样本属于跨 category 借用 → 跳过。 |
| **OPTION** / 期权 | **无可用样本** | 373 条 OS REGULAR 的表达式字段映射中，无任何 `option*` 类 dataset 字段命中；无已提交样本可选。 |
| **SOCIALMEDIA** / 社交媒体 | **无可用样本** | 同上，无任何 `socialmedia*` 类 dataset 字段命中。 |

> 这三类不借用其他 category 的 alpha 充数，也不列举未提交候选。

## 4 权限边界与限制（仅针对本轮样本实际涉及的口径）

1. **权限集 = 平台 `GET /operators` 返回的 103 个算子**。本轮 13 条代表中出现的 38 个唯一算子全部命中；表达式解析未发现清单外的函数调用（SUPER 的 combo/selection 表达式不在本轮范围）。
2. **scope 决定「允许用法」**：本轮算子全部是 `REGULAR` 可用的（`COMBO+REGULAR` 或 `COMBO+REGULAR+SELECTION`）。授权清单中 `Reduce`(14 个) 与 `Special`(3 个) 整族只标 `COMBO` 或 `SELECTION`，`generate_stats` 只标 `COMBO`——它们虽然在权限内，但按 scope **不允许**出现在 REGULAR alpha 的表达式里，因此本轮样本中不会出现。这是「有权限」与「该处可用」的区别。
3. **`level` 不是权限开关**：部分算子 `level=null`（如 `tail`、`ts_ir`、`ts_target_tvr_decay`、`vec_count`、`vec_stddev`、`vector_neut`），平台未给等级但仍在授权清单与 `REGULAR` scope 内；本报告按平台实际返回标注，不臆造等级。
4. **数值安全**：`divide` / `inverse` 遇分母为 0 会报错，平台建议 `add(y, 0.0001)` 加 epsilon——INSTITUTIONS 样本照做，FUNDAMENTAL 与 SHORTINTEREST 样本未加，属已知限制；`add/subtract/multiply` 的 `filter` 默认为 false，NaN 会传播，需 `filter=true` 才把 NaN 当 0/1。
5. **稀疏数据**：`ts_backfill` 只在 `lookback` 窗口内有效，窗口外长期缺口不会被填；`vec_*` 只接受 VECTOR 字段；`group_*` 的 `group` 必须是 GROUP 字段，`densify` 用于压缩稀疏桶。
6. **分布与换手约束**：`winsorize` 平台建议 `std=2~5`，RISK 样本用了 `std=0.38`（激进改写分布，已在表中标注）；`rank` 的 `rate` 控制排序精度；`trade_when` 的退出条件 `z` 优先于触发条件 `x`，`z` 为真直接置 NaN；`ts_target_tvr_decay` 用目标换手反解 decay，是 NEWS 样本低换手的主要来源。

## 5 产物与可复核数据

| 文件 | 内容 |
|---|---|
| `results/os_alphas_all.json` | 平台 OS REGULAR 全量 373 条原始返回 |
| `results/os_alphas_mapped.json` | 260 条 ACTIVE 的表达式、算子、字段→dataset→category 映射 |
| `results/operators_permitted.json` | 103 个授权算子的 definition / description / scope / level |
| `results/operator_docs.json` | 57 个算子的平台详细文档页 |
| `results/dataset_verify.json` | 14 个候选 dataset（含最终判无样本的 `macro63`）的 `get_datafields` 复验结果 |
| `results/final_pick.json` | 本轮最终选样与逐算子事实 |
