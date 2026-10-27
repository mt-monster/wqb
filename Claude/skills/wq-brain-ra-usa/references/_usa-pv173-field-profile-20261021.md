# pv173「Corporate Bond Pricing Data」字段画像与回测档案（USA / D1 / TOP3000）

> as_of 2026-10-21。来源：`get_datafields(region="USA", delay=1, universe="TOP3000", dataset_id="pv173")`
> （平台报 `platform_count=51`，工具按字段 sharpe 过滤后返回 43；`preflight_expressions` 的 VECTOR 清单补齐全部 51 个 id）。
> 塔位：**pv / 未点亮**（USA/D1 仅 analyst、model 点亮）。数据集级 aC **88**、cov 0.3916、valueScore 3、multiplier 1.1。
> 结构：§1 字段画像 · §2 适用模板与机制 · §3 回测结果 · §4 归因 · §5 决策。

## §1 字段画像

### 1.1 数据集元数据

| 项 | 值 |
|---|---|
| id / 名称 | `pv173` / **Corporate Bond Pricing Data** |
| 类别 / 塔 | `pv` / **未点亮** |
| coverage / fieldCount | 0.3916 / **51** |
| userCount / alphaCount | 58 / **88**（本池中拥挤度最低的一档） |
| valueScore / pyramidMultiplier | 3 / **1.1** |
| 官方描述 | 由公司债定价数据派生的股票信号：z-spread 曲线、期限利差，以及 PCA 因子（shift / twist / curvature） |

### 1.2 ★ 字段集是一个 3 × 8 × 2 的网格，不是 51 个独立字段

平台把 **8 个底层信号** 用 **3 种视图** × **2 个覆盖档** 展开成 48 个字段 + 3 个 `atlas_unit_name`（字符串元数据，**非信号**）。
这一条决定了本集的正确挖法：**先选 8 个信号，再选视图/覆盖档，绝不能把 48 个别名当 48 个方向去扫**。

| 前缀族 | 视图含义 | 用途判读 |
|---|---|---|
| `rawratios*` | 原始值（raw ratio） | **首选**：交给我们自己的 `winsorize/group_rank` 归一，损失最小 |
| `ranks*` | 平台已做**全 Markit BLE 横截面排序** | 已被截面秩压缩，再做 `group_rank` 是二次秩；只在与 raw 对照时用 |
| `zscores*` | 平台已做**横截面 z 分** | 同上，标准化的另一种口径 |

**覆盖两档**（同一信号的两个物理列，底层窗口/清洗不同）：

| 档 | 命名 | 覆盖 |
|---|---|---|
| 宽带 | `rawratios<name>` / `ranks<name>_2xx` / `zscores<name>` | **0.366–0.407** |
| 窄带 | `rawratios_<name>` / `ranks_<name>` / `zscores_<name>` | 0.3199–0.3389 |

> 本批**一律用宽带 rawratios**（覆盖高 3–7pp，且 raw 不需要反解平台的秩变换）。
> ⚠ 平台的字段 sharpe 过滤移除了 8 个字段，其中包含 `ranksmt5yzspreadindrelsbst_209` / `ranksmt5yzspreadsbst_216`
> 两个宽带 rank 变体 —— 说明这两条在平台侧的字段级 sharpe 不达标，**不要为了"覆盖更高"去捡它们**。

### 1.3 八个底层信号（字段八问逐条）

| # | 信号（宽带 raw 字段） | 类型 | cov | uc/ac | 语义 | 更新 | 形态判读 |
|---|---|---|---:|---|---|---|---|
| S1 | `pv173_rawratiosbondreturn20deqwt` | VECTOR | 0.3389 | 1/1 | 发行人债券组合（3–7y 到期）**20 日等权收益** | 日频价格 | **原始收益率**，量纲明确、可直接时序差分 |
| S2 | `pv173_rawratioseqbddivrgbdrtn120d` | VECTOR | 0.395 | 0/0 | **股债背离（收益口径）**：市场股票收益 − 由 120 日「股票~债券组合收益」回归估出的应有股票收益 | 日频 | **已回归残差化**，是"股票未被债券解释的那部分" |
| S3 | `pv173_rawratioseqbddivrgsprd5y120dsbst` | VECTOR | 0.3216 | 0/0 | 同上，但回归自变量换成 **5y 中段 z-spread 变化** | 日频 | 同一构念的信用口径版本 |
| S4 | `pv173_rawratiosmt5yzspreadchg60dsbst` | VECTOR | 0.366 | 4/7 | 5y 中段 z-spread 的 **60 日变化** | 日频 | **已差分**，慢变量；不要再叠一次长窗差分 |
| S5 | `pv173_rawratiosmt5yzspreadchgstd20dsbst` | VECTOR | 0.3753 | 1/1 | z-spread 变化的 **20 日标准差**（信用波动率） | 日频 | 已是二阶矩，**只做水平用**，勿再 `ts_std_dev` |
| S6 | `pv173_rawratiosmt5yzspreadindrelsbst` | VECTOR | 0.3767 | 0/0 | **行业相对** 5y z-spread（发行人 − 行业） | 日频 | 已剔行业信用因子 ⇒ 与 `group_rank(...,industry)` 语义重复，**外层别再按 industry 分组** |
| S7 | `pv173_rawratiosmt5yzspreadsbst` | VECTOR | 0.3767 | 0/0 | 5y 中段 z-spread **水平**（曲线节点缺失时用债券级聚合替代） | 日频 | 已替代/填补，**原始信用风险溢价** |
| S8 | `pv173_rawratios_mt5yzspreadzscore60dsbst` | VECTOR | 0.3242 | 0/0 | 5y z-spread 的 **60 日时序 z 分** | 日频 | 已是自身历史偏离；**勿再套 `ts_zscore`**（同 `ts_av_diff` 抹平 embedding 的教训） |

**共性画像**

- **全部 VECTOR** ⇒ 必须先 `vec_avg` 标量化（本批 S9 另测 `vec_max` 作为"发行人最差债券"的尾部口径）。
- **覆盖率是本集第一约束**：0.32–0.41 ⇒ TOP3000 中有效标的约 **960–1220 只**。`group_rank(...,subindustry)` 的小组可能只剩个位数成员 ⇒ **CW 风险高于 analyst 族**，且 SUB 指标天然偏低。
- **数据是"加工品"不是"原料"**：S2–S8 全部经过回归/替代/标准化。按 fundamental 扫描的 §7 教训（已加工量只做轻加工），**骨架必须是轻壳**（`hump` + `group_rank` + 至多一层 `ts_backfill`），不得堆 `ts_zscore`/长窗差分。
- 更新频率：日频（Markit BLE 日定价），但**发行人级曲线在节点缺失时有替代填充** ⇒ 同一发行人可能出现"曲线节点值"与"债券级聚合值"混合，隐含噪声。

## §2 适用模板与机制

### 2.1 经济机制（8 条，含文献锚）

| # | 机制 | 经济陈述 | 构造（信号） | 预期符号 |
|---|---|---|---|---|
| M1 | **跨资产动量溢出** | 债券投资者是机构、信息反应更慢；发行人债券 20 日收益正向预示股票收益（Hong–Torous–Valkanov 2007；Cohen–Frazzini 2008） | `S1` 水平 | 正 |
| M2 | **股债背离反转（收益口径）** | 股票跑赢"债券隐含的应有收益"= 股票端过度反应 ⇒ 后续回吐 | `S2` 水平 | 负 |
| M3 | **股债背离反转（信用口径）** | 股票相对 z-spread 隐含收益跑赢 ⇒ 信用未确认的股价上涨 | `S3` 水平 | 负 |
| M4 | **信用恶化 → 股票跑输** | z-spread 走阔 = 违约风险上升，股票承担同等破产风险但反应滞后（Campbell–Hilscher–Szilagyi 2008） | `S4` 水平 | 负 |
| M5 | **行业相对信用风险溢价** | 剔除行业共同信用因子后，个体信用溢价被定价 | `S6` 水平 | 正或负（待测） |
| M6 | **自身历史信用位置** | z-spread 处于自身 60 日高位 = 信用被抛售，反转 | `S8` 水平 | 负（或反转） |
| M7 | **信用波动率溢价** | 信用利差波动 = 不确定性，不确定性被折价 | `S5` 水平 | 正 |
| M8 | **信用水平 = 违约风险** | 高位 z-spread 的"垃圾级"效应：distress anomaly（股票反而跑输） | `S7` 水平 | 负 |
| M9 | **尾部债券风险** | 发行人最差那只债的 z-spread 比均值更能表达尾部违约风险 | `vec_max(S7)` | 负 |

> 用户纪律：**机制模板不限于 8 个**。本批 9 条机制含"PC 曲线"外的全部可得构念；
> PCA shift/twist/curvature 在字段层面**未暴露为独立字段**（描述提到但 51 个字段里没有 `pca_*`）
> ⇒ 本集**不设计**曲线形态机制，改为用 `S6`（行业相对水平）与 `S3`（spread 口径背离）近似表达曲线信息。

### 2.2 通用壳与假设

**主壳**：`quantile(group_rank(winsorize(ts_backfill(vec_avg(<SIG>), 252), std=4), subindustry))`
- `ts_backfill(252)`：发行人债券覆盖本身有缺口，回填只补时序空洞、不改截面分布（analyst 族两次验证的顺序：先 `winsorize` 再 `backfill`）。
- `quantile` 单参数（历史杠杆：对慢变量抬 SUB/2Y，字段特异）。
- 外层 `subindustry` 是 USA 默认。⚠ `S6`（行业相对 z-spread）本身已剔过一次行业，再按 subindustry 分组有双重剔除嫌疑；
  本批仍用 subindustry 作为**统一口径**（保证 10 条可比），若 S6 出现"方向对但弱"再单独换 `market` 归因。
- **次壳**（覆盖率兜底）：`group_rank(..., market)` —— 覆盖 0.4 时 subindustry 组内样本可能过少，market 组是本批的重型兜底，
  本批用最强信号 `S2` 跑一条 market 版做对照。

### 2.2.1 批 1 表达式清单（10 条 = 8 信号 + 2 口径对照）

| # | 机制 | 信号 | 聚合/分组 | 说明 |
|---|---|---|---|---|
| 1 | M1 跨资产动量 | S1 债券 20 日收益 | `vec_avg` / subindustry | 主证 |
| 2 | M2 背离反转（收益口径） | S2 | `vec_avg` / subindustry | 主证 |
| 3 | M3 背离反转（信用口径） | S3 | `vec_avg` / subindustry | 主证 |
| 4 | M4 信用恶化 | S4 z-spread 60d 变化 | `vec_avg` / subindustry | 主证 |
| 5 | M5 行业相对信用溢价 | S6 | `vec_avg` / subindustry | 主证 |
| 6 | M6 自身历史信用位置 | S8 z-spread 60d z 分 | `vec_avg` / subindustry | 主证（勿再套 ts_zscore） |
| 7 | M7 信用波动率 | S5 | `vec_avg` / subindustry | 主证 |
| 8 | M8 信用水平 | S7 | `vec_avg` / subindustry | 主证 |
| 9 | M9 尾部债券风险 | S7 | **`vec_max`** / subindustry | 聚合面：最差那只债 |
| 10 | M2 覆盖率兜底对照 | S2 | `vec_avg` / **market** | 分组面：覆盖 0.4 时 subindustry 组可能过小 |

### 2.3 预注册止损（先写死，回测后不得改判据）

1. **8 条信号全部 `|S| < 1.0`** ⇒ 判弱封存 `USA-PV173-WEAK`，不补批（8 个底层信号 = 字段全集，剩余自由度只有视图/覆盖档，属同族磨参）。
2. **全部 `risk_neutralized_sharpe < 0.3`** ⇒ 纯信用/利率风格 beta，直接封存不再花仿真。
3. 任一 `|S| ∈ [1.25, 1.58)` 且 rns ≥ 0.5 ⇒ Mode A，**先测 prod**（D0-P）。
4. 任一 RA 全闸 ⇒ 立刻 `check_correlation(refresh=True)`，prod ≥ 0.7 则按 D0-P 留池/封存，< 0.7 才报为可交付候选（提交仍需用户确认）。 <!-- from config.prod_corr_max -->
5. 出现 `CONCENTRATED_WEIGHT` ⇒ 先归因（覆盖 < 0.4 导致组内少数标的），**不得盲改 decay/窗口**；只允许"换分组粒度"与"`group_backfill`"两类修法各测一次。
6. `2Y < 1.6` 但 `S/F` 过 ⇒ 参照 analyst 族先验：2Y 短窗杠杆（`ts_av_diff` 窗缩半）**只测一轮**；信用数据是慢变量，若缩窗不灵即判该机制不耐久。

### 2.4 数据集切换理由（对应"不得频繁切换数据集，仅在确实无计可施时才更换"）

1. **Fundamental 类别已被穷尽**：23 个数据集全扫，5 个直接实测（fnd67 / fnd93 / fnd21 / fnd17 / fnd91）+ fnd69 当日判弱
   ⇒ 类别级结论"S 天花板 1.43 / SUB 天花板 0.52 ⇒ USA/TOP3000 结构性无法产出 ATOM"（见 `_usa-fundamental-dataset-scan-20261019.md` §6）。
2. **other 塔低拥挤集已全探**：2026-10-20 一天内 other545 / other546 / other567 / other571 / other580 / cre_exposure /
   earnings_risk / equity_forum_data / equity_kpi_forecast / sustainable_profit / event_relation / acquisition_model /
   macro63 / news_sentiment_nlp 全部出结论（全弱或 prod 墙），0 可交付。
3. **analyst 塔**：analyst44 已出 2 颗 ACTIVE；analyst_factor_signals 修正/偏度复族因 prod 直方图 `[0.7,0.8)` n≥1 判族级死；
   analyst_consensus 目标价族 prod 漂到 0.90+。
4. **`s0-select` 存活池全部 aC > 1000**（sentiment21 1482 / institutions6 3641 / macro38 16219 / other566 1992 / pv1 2.19M …）
   ⇒ 继续在拥挤族里磨 = 直接触 prod 墙。
5. **pv173 是唯一同时满足**「未点亮塔 + aC < 100 + 字段数 ≥ 20 + 机制与已交付 7 方向正交 + 从无画像」的剩余集。
   ⇒ 切换成立，且**本集只此一批探针**，未出信号即按预注册封存。

---

## 3. 回测结果（批 1 探针 · multisim `2Nq9ps7ah4Rybyv17mclmLUY`）

设置：USA / TOP3000 / EQUITY / D1 / SUBINDUSTRY / decay 5 / trunc 0.08 / VERIFY / nan ON / pasteurize ON / maxTrade OFF。
区间 2014-01-01 → 2023-12-31（IS）。10/10 COMPLETE，0 ERROR。平台闸线 S ≥ 1.25 / F ≥ 1.0 / 2Y ≥ 1.6（显示 1.58 为派生条）。

| # | 机制 | 底层信号 | alpha id | S | F | TO | R | DD | 2Y | SUB | **rns** | 失败闸 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | M1 跨资产动量 | S1 `bondreturn20deqwt` | `A1QNVMxW` | 0.71 | 0.36 | 0.0690 | 3.19% | 7.85% | 1.21 | 0.46 | **0.53** | SHARPE / FITNESS / 2Y |
| 2 | M2 背离反转（收益） | S2 `eqbddivrgbdrtn120d` | `VkdaxgN8` | 0.26 | 0.08 | 0.1456 | 1.26% | 16.05% | 0.96 | −0.06 | **−0.50** | +SUB |
| 3 | M3 背离反转（信用） | S3 `eqbddivrgsprd5y120dsbst` | `pwvRdAa3` | 0.23 | 0.07 | 0.1512 | 1.40% | 22.61% | 0.91 | −0.03 | **−0.58** | +SUB |
| 4 | M4 信用恶化 | S4 `mt5yzspreadchg60dsbst` | `vROr13Y3` | 0.43 | 0.19 | 0.0469 | 2.34% | 13.24% | 1.14 | 0.25 | **−0.37** | SHARPE / FITNESS / 2Y |
| 5 | M5 行业相对信用 | S6 `mt5yzspreadindrelsbst` | `gJWbeErM` | 0.70 | 0.36 | 0.0170 | 3.31% | 8.53% | 1.29 | 0.54 | −0.07 | SHARPE / FITNESS / 2Y |
| 6 | M6 自身历史位置 | S8 `mt5yzspreadzscore60dsbst` | `XgRb95Nz` | 0.45 | 0.20 | 0.0688 | 2.39% | 11.09% | 0.97 | 0.25 | **−0.38** | SHARPE / FITNESS / 2Y |
| 7 | M7 信用波动率 | S5 `mt5yzspreadchgstd20dsbst` | `zqr831gK` | 0.58 | 0.27 | 0.0337 | 2.67% | 8.60% | **1.39** | 0.33 | −0.10 | SHARPE / FITNESS / 2Y |
| 8 | M8 信用水平 | S7 `mt5yzspreadsbst` | `omoLEMRn` | **0.72** | **0.37** | 0.0171 | 3.37% | 8.99% | 1.32 | **0.55** | −0.02 | SHARPE / FITNESS / 2Y |
| 9 | M9 尾部债券 | S7 `vec_max` | `3qjXoZ10` | 0.72 | 0.37 | 0.0171 | 3.37% | 8.98% | 1.31 | 0.55 | −0.02 | 同 #8（逐位相同） |
| 10 | M2 / market 兜底 | S2 / `market` | `MP0aYodr` | 0.44 | 0.18 | 0.1079 | 2.09% | 11.43% | 1.20 | 0.06 | −0.14 | +SUB |

持仓规模：多 872–1070 / 空 1876–2079（合计 ≈ 2900/3000），**无一条 `CONCENTRATED_WEIGHT`**。

## 4. 归因

### 4.1 预注册规则 #1 触发（结论先行）

8 个底层信号的 `|S|` 全部落在 **0.23–0.72**，最大值 **0.72 < 1.0** ⇒ 按 §2.3 第 1 条**判弱封存 `USA-PV173-WEAK`，不补批**。
8 个底层信号就是字段全集，剩余自由度只有"视图"（`rawratios` / `ranks` / `zscores`）与"覆盖档"（宽 / 窄）——两者都是同族别名维度，
再开批等于磨参。

### 4.2 三条失败曲线，不是一个

把 10 条按 rns 分成三族，失败机理完全不同：

| 族 | 信号 | S 区间 | SUB | rns | 判读 |
|---|---|---|---|---|---|
| **A 债券动量** | S1 | 0.71 | 0.46 | **+0.53** | **唯一风险中性后仍为正的信号**——机制真实（跨资产动量外溢），但强度只有 0.71，F 0.36 |
| **B 价差水平** | S5 / S6 / S7（+vec_max） | 0.58–0.72 | 0.33–0.55 | **−0.10 ~ −0.02** | 原始指标最漂亮的一族（SUB 0.55 / 2Y 1.39），但**中性化后符号翻转 ⇒ 纯信用/利率风格 beta**，不是横截面信息 |
| **C 背离/变化** | S2 / S3 / S4 / S8z | 0.23–0.45 | −0.06 ~ 0.25 | **−0.37 ~ −0.58** | 强负 rns：字段是提供方已做过回归/标准化的"加工品"，共同因子被他们先扣掉了，剩下的是噪声 + 归一化伪影 |

**B 族是最值得记住的反面样本**：`SUB 0.55 / 2Y 1.32 / DD 8.99%` 三个指标都在"看起来能救"的区间，但 rns ≈ −0.02 说明
收益全部来自信用风险敞口（价差水平 ↔ 低波 / 质量 / 久期），alpha 一旦被风险模型扣掉就归零。**只看 SUB 会误判这一族可救。**

### 4.3 F 墙是信息量问题，不是杠杆问题

最优组合（S 0.72 / TO 0.0171 / R 3.37%）落在 F = S·√(R/0.125) 的低换手区间：`0.72 × √(0.0337/0.125) = 0.374`，与平台 0.37 逐位吻合。
要在 S = 0.72 下把 F 做到 1.0，需要 **R = 24.2%**（年化），而该信号的信息量只给 3.4% —— **差 7 倍**。
即使把 S 提到 1.58，也仍需 R ≈ 10%。⇒ 任何 `winsorize` / `hump` / `decay` / 窗口微调都动不了这一层。

### 4.4 `vec_max` 维度在本集无效（修正 §2.2.1 的假设）

#9 与 #8 的 longCount（872 / 2046）、S（0.72）、F（0.37）、2Y（1.31 vs 1.32）、SUB（0.55）**逐位相同**，
唯一差异在小数点后四位（DD 8.98% vs 8.99%）。⇒ 该字段每只股票实际只有一个有效债项元素，**"最差那只债"的尾部机制在本集不可测**。
记录为结构性事实：pv173 的 VECTOR 维度不携带尾部信息，后续同类"债券组合聚合"不要再假设 `vec_max ≠ vec_avg`。

### 4.5 覆盖率假设被证伪（修正 §2.3 第 5 条的前置）

§1 把"覆盖 0.32–0.41"列为最紧约束、§2.3 第 5 条据此预置了 CW 的两条修法。实测 **0 条 CW**，多空合计 ≈ 2900/3000 只。
原因：`vec_avg` + `ts_backfill(252)` 的并集把有效覆盖推到了交易面几乎全覆盖。⇒ **本集的约束不是覆盖，是信息量**；
不过 `market` 兜底对照（#10，S 0.26 → 0.44、SUB −0.06 → 0.06）仍然证实了"低覆盖集用粗分组能抬 SUB"这条通用经验，
只是抬完依旧远低于 1.0，救不了弱信号。

### 4.6 论坛取证（负结果，可复用）

两轮检索（corporate bond / z-spread / credit spread → equity cross-section）**均无专题帖**，与平台 `alphaCount = 88` 的低拥挤度一致。
记录为：**"论坛没有 pv173 / 公司债 z-spread 的现成经验"**——低 aC 往往意味着"没人挖"，也意味着"没人验过这条路能不能走通"；
本次实测给出的答案是：**在 USA/TOP3000/D1 走不通，因为它是风格 beta 通道而非 alpha 通道。**

## 5. 决策

1. **封存 `USA-PV173-WEAK`**，依据 §2.3 第 1 条（8 信号全 `|S| < 1.0`）。不开第二批，不换视图/覆盖档重试。
2. **不提交、不入池**：无一条达到 RA 闸线（最好成绩 S 0.72 / F 0.37 / 2Y 1.39，距 S 1.25 差 0.53）。
3. **可复用结论（三条，进 playbook）**：
   - **信用类字段先看 rns 再看 SUB**：价差水平族可以同时做到 SUB 0.55 + 2Y 1.3 + DD 9%，而 rns ≈ 0 —— 这是风格 beta 的典型指纹，
     SUB 在这里不具判别力（它是在同一套风格倾斜的宇宙里算的）。
   - **`vec_max` vs `vec_avg` 要先验"向量是否真的多元"**：逐位相同即说明该字段每股单元素，尾部机制不可测，别为它单独开一批。
   - **覆盖 0.4 + `ts_backfill` 的并集足以覆盖交易面**（多空 ≈ 2900/3000），"低覆盖 ⇒ CW"不是必然；CW 的真因是组内样本少，不是字段覆盖低。
4. **对目标的影响**：USA 交付仍为 **5 / 10**（`omoK1A5m` / `akVnvzX5` / `gJWoaJqv` / `kqJLawqP` / `e76xgXkM`）。
   下一集选择须同时满足「未点亮塔 + 机制在 prod 池未被挖过」，且**探针批必须带 rns 判死口径**（本集已经证明 rns 比 S/F 更早给出死刑判决）。
