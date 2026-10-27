# USA acquisition_model 字段画像（M&A Target Model 百分位族）

> **as_of** 2026-10-20 ｜ **region/delay/universe** USA / 1 / TOP3000 ｜ **塔** USA/D1/OTHER（×1.4，未点亮）
> **状态**：**判死（沿用既有 `USA-ACQUISITION-MODEL-DEAD`）**。本轮 8 条为**复核批**——
> 该集在既有 dead 名单上（旧证据：4 候选 3 负 1 个 0.95），本轮排期时未先核 `get_dead_ends` 即发出，
> 属流程偏离（见 §5.3）；结果与旧判死一致，不新增判死键。

## 0. 坐标与一句话结论

`acquisition_model` 是某第三方 M&A 目标概率模型的**百分位输出集**：15 个字段**全部为 VECTOR**、
**覆盖率统一 0.9063**、取值 1–100。它把「公司成为并购目标的概率」拆成 5 条 likelihood 轴
（country / global / industry / region / sector）与 5×2 个组件轴（size / credit / fundamental / text / valuation
× global / region）。

**一句话结论**：**静态目标概率在 USA 没有截面 alpha**（水平 H S 0.11、INDUSTRY 百分位 S 0.10，2Y 均为负）；
唯一有读数的是**一阶变化 `ts_av_diff(…,22)`（S 0.72 / SUB 0.41 PASS / TO 15%）**，但 2Y −0.68 ⇒
方向在近端翻转，作为全期单腿不可交付。本集封存。

## 1. 字段画像

### 1.1 总览

| 维度 | 读数 |
|---|---|
| 字段数 | 15（全部 VECTOR） |
| 覆盖率 | **全部 0.9063**（同一行级覆盖，字段间无差异） |
| 取值 | 百分位 1–100（不是原始财务量） |
| 更新频率 | 模型分，低频（水平轴换手 1.8–3.7%，见 §5） |
| aC 区间 | 1–54；**最高 `global_valuation_percentile_rank` = 54**（组件轴最拥挤） |
| 拥挤度最低 | 多条 likelihood 轴 aC 1–4（`region_` 2、`sector_` 3、`global_` 4） |

### 1.2 五条 likelihood 轴（目标概率本体）

| 字段 | aC | 经济含义 |
|---|---:|---|
| `global_percentile_acquisition_likelihood` | 4 | 全市场百分位 |
| `country_percentile_acquisition_likelihood` | 10 | 本国同行内百分位 |
| `industry_percentile_acquisition_likelihood` | 8 | Region+Industry 同行内 |
| `sector_percentile_acquisition_likelihood` | 3 | Region+Sector 同行内 |
| `region_percentile_acquisition_likelihood` | 2 | M&A region 集合内 |

**判读**：五轴是**同一个目标的相对化口径**，不是五个机制。`group_rank(x, industry)` 已经把截面中性化到 industry，
再叠加 `industry_percentile_*` 会造成**二次相对化**（把「同行内排名」再在同行内排名），
因此 A3 的读数（S 0.10）与 A1（0.11）几乎相同，属预期而非巧合。

### 1.3 十条组件轴（global × region）

| 组件 | global aC | region aC | 说明 |
|---|---:|---:|---|
| valuation | **54** | 31 | 估值分位，最拥挤——市场已充分使用 |
| fundamental_factor | 12 | 27 | 基本面 |
| credit_quality | 14 | 25 | 信用质量 |
| company_size | 12 | 1 | 规模 |
| text_factor | **3** | 3 | 文本/新闻因子，几乎无人用但 A4/A5 实测无效 |

**判读**：aC 的分布说明「估值 + 基本面 + 信用」三轴被用尽（合计 156 条 α），
而 `text_factor` 只有 6 条 α——**低拥挤 ≠ 有信号**，本批 A4/A5 的 |S| ≤0.14 是这条判据的反例。

## 2. 适用模板（按机制，不按字段数）

| 编号 | 机制 | 表达式骨架 | 依据 |
|---|---|---|---|
| M01 | 静态目标概率（水平） | `quantile(group_rank(winsorize(vec_avg(<likelihood>), std=4), industry))` | 标准 value-like 壳；本集实测无效 |
| M02 | 镜像方向 | `-` M01 | 必发，检验对称性 |
| M03 | **目标概率的边际变化** | `quantile(group_rank(winsorize(ts_av_diff(vec_avg(<likelihood>), 22), std=4), industry))` | 唯一有读数的轴（A6 0.72） |
| M04 | 历史分位 | `ts_rank(vec_avg(<likelihood>), 252)` | 慢变量的时间标准化 |
| M05 | 平滑水平 | `ts_mean(vec_avg(<likelihood>), 22)` | 检验是否只是噪声 |
| M06 | 组件分解 | 对 5 条组件轴逐一 M01 | 归因用途，不是新机制 |
| M07 | 跨口径价差 | `vec_avg(global_…) − vec_avg(industry_…)` | 「相对同行更可能被收购」，本批未发（见 §5 偏离说明） |
| M08 | 事件条件 | `trade_when(Δlikelihood > 阈值, 水平, -1)` | 需先证明 Δ 在近端不翻向；本集已判死，未投入 |

**壳层纪律**：`quantile` 只接 1 参数；`winsorize` 必须具名 `std=`；VECTOR 必须先 `vec_avg`/`vec_sum` 再进标量算子。
本集全部字段已是百分位，**不需要再 `rank`**（再 rank 只是重复），这是与原始财务字段的重要差别。

## 3. 批 1 预注册与执行（multisim `2ikiU4aes4R0b6RCyFz57oD`，8 条）

| # | alpha | 轴 | 模板 |
|---|---|---|---|
| A1 | `mLYVbNm6` | global likelihood | M01 |
| A2 | `gJW9M5ZJ` | global likelihood | M02 |
| A3 | `N1eRrGVq` | industry likelihood | M01 |
| A4 | `78on1r6Z` | global text factor | M01 |
| A5 | `9qE7r3W2` | global text factor | M02 |
| A6 | `1YjzdRjQ` | global likelihood | M03（Δ22） |
| A7 | `6XAe9QAY` | global likelihood | M04（ts_rank252） |
| A8 | `N1eRrGe7` | global likelihood | M05（ts_mean22） |

**预注册判据**：任一 `S≥1.58 / F≥1.0 / 2Y≥1.58 / SUB PASS / TO 1–70%` 且 fail=0 ⇒ 立即 `check_correlation(refresh=True)`；
若水平轴与 Δ 轴**同向且量级差 ≥3 倍** ⇒ 归因为「只有创新有信息」，再决定是否发 M07；
若全部 |S| < 0.8 ⇒ 判弱。

## 4. 外部证据

- **M&A 目标预测的经典特征族**：Palepu (1986, *Journal of Accounting and Economics*)「Predicting takeover targets:
  A methodological and empirical analysis」给出的目标预测变量族就是 **size / valuation / liquidity / leverage(credit) / 盈利质量**，
  与本集 5 条组件轴一一对应 ⇒ 组件设计不是黑盒，**建模的是经典的 target-score**。
- **为什么静态概率可能没有 α**：目标概率是**慢状态变量**且被卖方研究广泛覆盖；可交易的信息在**概率的更新**（并购传闻、
  13D 申报、行业整合浪潮），而不在水平。本批 A6（Δ22）显著高于 A1（水平）正是这条的实证。
- **方向不确定**：高目标概率既可能因「被收购溢价」上涨，也可能因「折价成交 / 交易失败」下跌；
  文献对 target 组合的超额方向结论不一致，因此 **A2 镜像必发**（本批读数与 A1 严格对称，说明方向确由单一成分决定）。

## 5. 回测结果与归因

### 5.1 批 1 结果（8/8 COMPLETE，0 error）

| # | alpha | 轴/模板 | S | F | 2Y | SUB | TO | rns | fail |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|
| A1 | `mLYVbNm6` | global 水平 | 0.11 | 0.03 | −0.65 | 0.03 FAIL | **2.5%** | 0.10 | 4 |
| A2 | `gJW9M5ZJ` | global 水平（镜像） | −0.11 | −0.03 | 0.65 | −0.03 | 2.5% | −0.10 | 3 |
| A3 | `N1eRrGVq` | industry 水平 | 0.10 | 0.02 | −0.77 | 0.02 FAIL | 2.7% | −0.14 | 4 |
| A4 | `78on1r6Z` | text 水平 | −0.14 | −0.04 | −0.91 | 0.15 | 3.7% | −0.13 | 3 |
| A5 | `9qE7r3W2` | text 水平（镜像） | 0.14 | 0.04 | 0.91 | −0.15 FAIL | 3.7% | 0.13 | 4 |
| A6 | `1YjzdRjQ` | **Δ22** | **0.72** | **0.32** | −0.68 | **0.41 PASS** | **15.1%** | 0.37 | 3 |
| A7 | `6XAe9QAY` | ts_rank252 | 0.04 | 0.01 | −0.58 | 0.15 | 7.7% | −0.12 | 3 |
| A8 | `N1eRrGe7` | ts_mean22 | 0.07 | 0.02 | −0.66 | −0.01 FAIL | 1.8% | 0.03 | 4 |

### 5.2 归因（8 条）

1. **水平轴无信息**：A1/A3/A8 的 S 0.07–0.11，TO 仅 1.8–2.7% ⇒ 这是一个**几乎不动的静态分**。
   合理解释：目标概率被卖方与套利资金持续定价，水平本身不含可交易预期收益。
2. **两对镜像严格对称**（A1/A2 差 0、A4/A5 差 0）⇒ 方向由**单一成分**决定，不存在「正负方向各自有效」的非对称。
3. **Δ 是唯一有效变换**：A6 的 S 0.72 是水平（0.11）的 **6.5 倍**，TO 也从 2.5% 升到 15.1%
   ⇒ 信息在**概率的更新**里，不在概率的绝对水平。这与 §4 的慢变量解释一致，是本集唯一可复用的机制结论。
4. **Δ 的 2Y 为 −0.68**：全期正、近两年负 ⇒ 近端发生 regime 翻转（并购潮 2020–2021 之后失效）。
   与 other699 的 B1/B2（全期弱、2Y 强）**方向相反**，但同属「全期与近端符号冲突」的不可交付形态。
5. **text factor 无效**：A4/A5 的 |S| 0.14，2Y 分别为 −0.91 / 0.91，等于把噪声反了个号。
   ⇒ aC 3 的「低拥挤」不代表有 alpha，这条对后续「按 aC 从低到高挑字段」的做法是反例。
6. **B 型（组件轴）未逐一发**：valuation 的 aC 54 已被用尽、其余组件（size/credit/fundamental）与 likelihood 高度共线；
   在水平轴已证明无信息、Δ 轴 2Y 翻转的前提下，再发 5 条组件水平只是重复测量，**不构成新机制** ⇒ 主动不发（偏离留痕）。

### 5.3 决策：判死（沿用 `USA-ACQUISITION-MODEL-DEAD`）

- 预注册「全部 |S| < 0.8 ⇒ 判弱」成立（max 0.72 且来自 2Y 翻转的 Δ 轴）。
- **⚠ 流程偏离登记**：该集在本轮之前已在 `get_dead_ends(region="USA")` 名单上
  （`USA-ACQUISITION-MODEL-DEAD`，旧证据 4 候选 3 负 1 个 0.95）。本轮排期时**未先复核 dead 名单**即发出 8 条，
  属「禁止因 aC 低而复活」的反向违规（这里是因字段干净 + aC 低而复活）。
  结果**与旧判死一致**（无一条过闸），故不推翻结论，8 条读数只作该键的补充证据。
- **不新增判死键**：避免同一数据集出现两个 entry_id；旧键继续有效。
- **salvage**：A6 `1YjzdRjQ`（Δ22 likelihood，S 0.72 / F 0.32 / SUB 0.41 PASS / rns 0.37）
  作为「并购概率创新」的**弱方向笔记**登记；若将来做 regime-aware 组合（只在并购活跃期开启）可回捞，
  全期 REGULAR 单腿不可交付。
- **不做第三个变量批**：水平无信息 + Δ 近端翻向 + text 无效，三条已覆盖本集的全部机制面
  （五条 likelihood 轴只是相对化口径，不是新机制）。再发 = 盲扫。
- **可复用纪律**：**排期前必须 `get_dead_ends(region)` 复核**（台账 §2 末尾已有这条，本轮自己踩了）。
  「字段干净 + aC 低 + 复合模型」是最容易诱发复活冲动的组合。

## 6. 风险与预判

1. **百分位字段不要再 rank**：全部字段已是 1–100 百分位，`group_rank` 已做截面中性化；再 `rank`/`zscore` 是重复变换，
   只会改变分布形状不会增加信息。本批全部模板已规避。
2. **`vec_avg` 的语义未验证**：VECTOR 的维度含义（多模型快照 / 多子模型）未在字段描述中给出；
   本批用 `vec_avg` 取均值是保守选择。若将来要用，先做 `vec_count` / `vec_stddev` 画像确认向量长度稳定。
3. **2Y 翻向是结构性的**：A6 的 2Y −0.68 与全期 0.72 冲突，说明该信号只在特定并购周期有效；
   任何基于本集的候选都必须先过逐年诊断（`brain-alpha-robustness`）。
4. **ATOM 合规**：本批所有字段来自 acquisition_model 单数据集；`industry` 为分组豁免字段。
5. **覆盖率 0.9063 是行级**：与 other699 的「行级覆盖 ≠ 每日每票有值」同一口径风险；
   本批 CW 全部 PASS（无 0.5 塌缩），说明百分位字段的稀疏性远低于事件级 VECTOR。

## 7. 索引

- 本篇：`references/_usa-acquisition-model-field-profile-20261020.md`
- 交付台账：`references/_usa-atom-delivery-log-20261020.md`
- 同型教训（低 aC ≠ 有信号 / 水平 vs 变化）：`references/_usa-other580-etf-holdings-field-profile-20261020.md`
- 未点亮塔战役总表：`references/_unlit-tower-campaign-20261014.md`
