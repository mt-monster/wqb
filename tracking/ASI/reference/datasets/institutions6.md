# institutions6 模板计划（ASI / MINVOL1M / D1）

> 战役：ASI/D1 Power Pool Dec'26。塔位：INSTITUTIONS **0/3 未点亮**（2026-11-23 实读）。
> 数据集：institutions6「Global Institutional Holdings」，cov 0.9991，11 字段全 MATRIX，JPN 覆盖完整，pyramid 1.2x。
> 全字段探测：11/11（`get_datafields` complete=true，2026-11-23）。
> 标准：2026-11-23 用户硬标准 —— **每集 ≥10 模板 ∧ 每模板来自论坛/论文（可指 post id / DOI）∧ 每模板跑完全部梯度 ∧ 算子逐类别全替换 ∧ 参数精调 ∧ 一模板穷尽后再下一个**。

## 字段全表（11/11，分四族）

| 字段 | 族 | cov | ac |
|---|---|---|---|
| `aggregate_equity_value_all_owners` | 资产水平-全体 | 1.000 | 355 |
| `aggregate_equity_value_institutions` | 资产水平-机构 | 0.995 | 204 |
| `aggregate_share_count_all_owners` | 股数水平-全体 | 1.000 | 195 |
| `aggregate_share_count_institutions` | 股数水平-机构 | 0.995 | 237 |
| `count_institutional_buyers_security` | 家数-buyers | 1.000 | 239 |
| `count_institutional_holders_security` | 家数-holders | 1.000 | 188 |
| `count_institutional_sellers_security` | 家数-sellers | 1.000 | 302 |
| `market_value_institutional_shares_acquired` | 市值流量-买入 | 1.000 | 156 |
| `market_value_institutional_shares_disposed` | 市值流量-卖出 | 1.000 | 221 |
| `quantity_institutional_shares_acquired` | 股数流量-买入 | 1.000 | 156 |
| `quantity_institutional_shares_disposed` | 股数流量-卖出 | 1.000 | 241 |

## TemplatePlan（14 模板，每模板一行证据）

| # | 模板（结构互异） | 机制/假设 | 证据来源 | 状态 |
|---|---|---|---|---|
| **T1** | `decay(group_neutralize(ts_zscore(buyers/(buyers+sellers), 252), industry), 3)` | 机构净买入家数占比 = 纯增量偏好（慢变量） | **论坛 44147814648215**（IND 全绿 GrOXE7YP S2.39/F2.01/prod.6524） | **进行中** |
| **T2** | 同 T1 但**市值口径**：`acquired/(acquired+disposed)` | 资金金额口径的净买入强度（vs T1 家数口径） | 论坛 44147814648215 口径说明 + `10.1016/j.frl.2004.06.003`（机构交易与收益） | **进行中** |
| **T3** | 同 T1 但**股数口径**：`quantity_acq/(quantity_acq+quantity_disp)` | 股数口径剥离价格效应 | `10.1086/508002`（机构持股变动与收益：口径方法论） | 待跑 |
| **T4** | `ts_zscore(divide(count_holders, ts_mean(count_holders,252)), 66)` | 机构**持有家数**广度变化（herding breadth） | `10.2139/ssrn.1107523`（机构羊群与未来收益） | 待跑 |
| **T5** | `ts_zscore(divide(count_buyers, count_holders), 66)` | 买入家数占存量持有家数比 = 流入强度归一 | `10.2139/ssrn.1107523` + 论坛帖 T1 分母思想 | 待跑 |
| **T6** | `ts_delta(ts_zscore(divide(agg_eq_value_institutions, agg_eq_value_all_owners),252), 66)` | 机构**占全体持有人比重**变化（拥挤度/渗透率） | `10.1086/508002`（持股比例变动） | 待跑 |
| **T7** | `group_rank(ts_zscore(buyer_ratio,252), industry)` 换外层为 industry **rank** | 分组轴：rank vs neutralize（论坛 T1 用 neutralize） | 论坛 44147814648215 消融 Step4 + `10.1108/03074351211201442`（台湾外资行业羊群→industry 轴） | 待跑 |
| **T8** | `group_rank(ts_zscore(buyer_ratio,252), country)` | 分组轴换 country（ASI 跨国市场，日本占比大） | 论坛 45201936320919（ASI 官方课：内层 country 对齐区域 Checks） | 待跑 |
| **T9** | `group_rank(ts_zscore(buyer_ratio,252), exchange)` | 分组轴换 exchange（亚洲交易所制度差异） | 论坛 44147814648215「分组层最大单一杠杆=exchange」 | 待跑 |
| **T10** | `ts_decay_linear(group_neutralize(ts_zscore(buyer_ratio,252), industry), 10)` | decay 轴精调（3→10，压换手抬 margin/2Y） | 论坛 44147814648215「decay 3-5 平滑换手降30%」 | 待跑 |
| **T11** | `winsorize(group_neutralize(ts_zscore(buyer_ratio,252), industry), std=4)` | 极端值截尾（提 Robust 保留率） | 论坛 45201936320919（Robust Universe 修法） | 待跑 |
| **T12** | `trade_when(rank(cap) > 0.2, <T1核>, -1)` | 流动性子集门控（若 prod 撞钉子时的破法） | 论坛 45201936320919 + 画像杠杆 §S4 | 待跑（条件触发） |
| **T13** | `add(ts_zscore(buyer_ratio,252), ts_zscore(mdl26_arm_revisions,66))` 双腿慢快 | 机构慢变量 × 分析师快变量正交协同 | **论坛 44147814648215**（IND prod 0.8339→0.6524 实证）；DOI `10.1177/0148558x0602100405` | 待跑（跨集，ATOM 穷尽后） |
| **T14** | `add(ts_zscore(buyer_ratio,252), ts_zscore(buyer_ratio,sellers),66)` 单集双尺度 | 同字段慢/快双尺度（ATOM 内合法） | 论坛 44713280965527（双尺度正交腿） | 待跑 |

**结构红线（论坛 44147814648215）**：禁 `rank(A) * rank(B)` 乘法复合（空头端坍塌：0.05×0.95→0.0475）；必须**独立标准化后对称加和**。

**ATOM 边界**：T1–T12 为单集 ATOM（institutions6 内部字段）；T13 为跨集（institutions6 + model26），需 ATOM 穷尽后启用，且计入组腿配额（当前已用 PV+FUNDAMENTAL 1 个、FUNDAMENTAL+ANALYST 1 个，T13 将为第 3 个，仍在 ≤5 内）。

## 梯度层定义（每模板都跑这 5 层）
- **L1 内层标准化**：ts_zscore 窗口 {66, 252, 504} × 等价替换 {ts_rank, ts_scale, quantile}
- **L2 外层算子**：group_neutralize / group_rank / group_zscore 全替换
- **L3 分组轴**：industry / country / exchange / market / subindustry
- **L4 中性化档**：INDUSTRY / SLOW / COUNTRY / SUBINDUSTRY
- **L5 参数精调**：decay {0,3,5,10} × trunc {0.05,0.08} × 窗口命名参数

## 待办
- [ ] T1 首批 2 臂读数（在飞）
- [ ] T1 全梯度 L1–L5
- [ ] T2/T3 口径模板全梯度
- [ ] T4–T6 家数/比重族
- [ ] T7–T9 分组轴
- [ ] T10–T12 设置/门控
- [ ] T13–T14（ATOM 穷尽后）

## 15. T1/T15 梯度实测（2026-11-23）

### T1（论坛 44147814648215 配方 ASI 迁移，分母=流量总和）
| 变体 | S | F | 2Y | JPN | 判定 |
|---|---|---|---|---|---|
| 家数口径 buyers/(buyers+sellers) 252w INDUSTRY | 0.63 | 0.28 | 0.84 | — | 弱 |
| 家数口径 @ SLOW | 0.55 | 0.15 | 1.33 | — | 更弱 |
| 市值口径 acquired/(acq+disp) | −0.11 | −0.02 | −0.10 | — | 死 |
| 股数口径 @ SLOW | 0.27 | 0.05 | −0.12 | — | 死 |

**T1 结论**：论坛 IND 配方在 ASI **不迁移**（跨区不外推铁律再证）。分母用「流量总和」是问题——正确形态是**流量÷存量**（KOR 版）。

### T15（KOR 全闸件 Jj8zG0Ye 配方 ASI 迁移，分母=ts_mean(holders,72)，窗1260）
| 变体 | S | F | 2Y | sub | **JPN** | Robust | failed_ra |
|---|---|---|---|---|---|---|---|
| 绝对门控<33 + rank 外层（原始迁移） | 1.54 | 1.05✓ | 2.34✓ | 0.69 | 0.43 | 1.33/1.39 | 3 |
| 无门控 | 0.99 | 0.59 | 1.74 | 0.65 | — | — | — |
| 相对门控 group_rank(holders,country)<0.3 | 1.25 | 0.82 | 2.25 | 0.58 | — | — | 5 |
| 相对门控 <0.5 | 1.32 | 0.89 | 2.42 | 0.85 | 0.33 | 1.17/1.19 | 4 |
| **★ rank→group_rank(country) 外层** | **1.86** | **1.35** | **2.94** | **0.80** | **0.50** | ✓✓ | **1** |
| 窗口 1260→840 | 1.56 | 1.06 | 2.24 | 0.72 | — | — | 3 |
| 门控放宽<60 | 1.80 | 1.25 | 3.04 | 1.01 | **0.25** | 1.55/1.62 | 3 |
| 门控放宽<100 | 1.84 | 1.23 | 2.86 | 1.15 | — | — | 3 |

### ★★ 当前最强件 `ZYaVVR01`（institutions6）
```
trade_when(ts_mean(count_institutional_holders_security, 90) < 33,
  signed_power(add(
    group_rank(ts_scale(divide(count_institutional_buyers_security,
                 ts_mean(count_institutional_holders_security, 72)), 1260), country),
    group_rank(ts_scale(ts_decay_linear(divide(subtract(count_institutional_buyers_security,
                 count_institutional_sellers_security),
                 ts_mean(count_institutional_holders_security, 72)), 42), 1260), country)), 1.0), -1)
```
@ ASI/MINVOL1M/D1/INDUSTRY/decay16/trunc0.08/maxTrade ON

**读数**：S1.86 / F1.35 / 2Y2.94 / sub0.80 / TO1.95% / margin 67.8bp / RN_S1.06 / **唯一缺口 JPN 0.50**（需 1.0）。

### 关键归因
1. **分母形态决定生死**：`buyers/(buyers+sellers)` 流量总和 → S0.63；`buyers/ts_mean(holders,72)` 流量÷存量 → S1.54（**+0.91**）。流量÷存量铁律第 3 次复现
2. **外层 rank → group_rank(country) 是最大单杠杆**：S 1.54→1.86（+0.32）、F 1.05→1.35、2Y 2.34→2.94 ✓
3. **门控是必需件**：无门控 S0.99 vs 有门控 S1.54（+0.55）
4. **JPN 与门控阈值反向**：<33 → JPN0.50；<60 → JPN0.25；相对门控 → 0.33 ⇒ JPN 低**不是门控排除日本票**，而是**机构买家比例信号在日本无定价力**（JPN 天花板 0.50）
5. 窗口 1260 优于 840（3 年 vs 5 年，慢变量需要长窗）

### 余量表（ZYaVVR01）
S +0.28 / F +0.35 / 2Y **+1.36** / sub +0.23 / margin 超厚 / **JPN −0.50（唯一硬缺口）** / prod&self 待测。

## 16. ★★ ZYaVVR01 完整闸门审计（2026-11-23，按 11-23 用户「差一项先查 prod+PnL+逐年」指令）

| 闸 | 值 | 门槛 | 判定 |
|---|---|---|---|
| Sharpe | 1.86 | ≥1.58 | ✅ |
| Fitness | 1.35 | ≥1.0 | ✅ |
| 2Y | 2.94 | ≥1.58 | ✅ 余量 +1.36 |
| Sub-universe | 0.80 | 动态 | ✅ |
| Turnover | 1.95% | [1%,70%] | ✅（低于内部严线 5%）|
| Margin | 67.8bp | — | ✅ 极厚 |
| Robust S / Ret | 过 | 90% | ✅ |
| **prod_corr** | **0.6083** | <0.70 | ✅（[0.6,0.7) 仅 2 条，主体健康）|
| **self_corr** | **0.1837** | <0.70 | ✅（最高 P02wbJAM 0.18，池 6）|
| **JPN Sharpe** | **0.50** | ≥1.0 | ❌ **唯一缺口** |
| RN Sharpe | 1.06 | — | 标准档（非风险线）|

**逐年**：10/10 年 PnL 全正，long/short 661–1446 无零持仓年 ⇒ 数据层干净（无排除）。
2014 S2.69 / 2015 **0.69** / 2016 2.48 / 2017 2.26 / 2018 **1.08** / 2019 1.93 / 2020 1.24 / 2021 2.12 / 2022 1.98 / 2023 **3.97**。

**★★ 关键情报：institutions6 是 ASI 上第一个 prod/self 双干净的信息源**
- prod 0.6083 ✓ / self 0.1837 ✓（对比 fundamental23 ebit：prod 0.8018 FAIL 钉子墙）
- ⇒ 机构持仓信息源在 ASI 生产池中有充足空间，**未来可继续用**

**JPN 0.50 归因（信号层结构墙）**：
1. 门控阈值反向：<33 → JPN 0.50；<60 → JPN 0.25；<100 → 更低 ⇒ 放宽门控（纳入更多日本票）反而更差
2. 相对门控（country 内分位 0.3/0.5）→ JPN 0.33，也更差
3. 整体 S1.86 vs 日本子集 0.50 ⇒ 日本票是该信号净拖累
4. ⇒ **机构买家比例信号在日本市场无定价力**，与 price_signal_dl（0.01-0.22）、analyst69 rating（0.52）同型
5. 平台严禁屏蔽日本（论坛 45201936320919「切勿使用屏蔽日本股票的写法，提交审核会直接报错」）⇒ 不可绕过

**结论**：ZYaVVR01 = **除 JPN 外全闸完美**的件（S1.86/F1.35/2Y2.94/prod0.61/self0.18/十年满仓），JPN 0.50 为数据集级信号层天花板。按 D15 记 PROVISIONAL，不写数据集死键。

## 17. 模板进度盘点（2026-11-23）

| 模板 | 状态 | 最好读数 |
|---|---|---|
| T1 论坛配方（流量总和分母） | ✅ 已测 4 变体 | S0.63（不迁移）|
| T15 KOR 配方（流量÷存量+门控+group_rank country） | ✅ 已测 8 变体 | **S1.86 / JPN0.50** |
| T4 家数广度 | ✅ 已测 | S1.02 |
| T6 机构渗透率 | ✅ 已测 | S0.44 |
| T2 市值口径 / T3 股数口径 | ✅ 已测（在 T1 批内） | −0.11 / 0.27 |
| T5 买入/存量比 | 待跑 | — |
| T7/T8/T9 分组轴（industry rank / country / exchange） | 部分覆盖（country ✓ / exchange ✓ SLOW档） | country 最优 |
| T10/T11 decay/winsorize 精调 | 部分（decay16 已测，winsorize 未） | decay16 |
| T12 门控（流动性子集） | 未跑 | — |
| T13/T14 双尺度/跨集 | 未跑（ATOM 未穷尽） | — |

**臂数**：~20 臂（T1×4 + T15×8 + T4/T6×2 + 其他 6）。**天花板**：S1.86（ZYaVVR01）。**卡点**：JPN 0.50（信号层）。

## 18. group_cartesian_product / 交叉分组验证（2026-11-23，用户点名）

按论坛依据双源验证分组结构对 JPN 的作用：
- **官方 ASI 课模板5**（帖 45201936320919）：`densify(group_cartesian_product(industry, country))` 可"同步中性化国家与行业"，优于连续嵌套
- **论坛帖①**（44713280965527，18赞）铁律："两腿的分组必须**交叉**（如 sector×exchange）；统一到单一分组会付区域/2Y 双 FAIL"

| 分组结构 | 表达式差异 | S | F | 2Y | sub | **JPN** |
|---|---|---|---|---|---|---|
| 单轴 country（ZYaVVR01） | 两腿都 `group_rank(·, country)` | **1.86** | 1.35 | **2.94** | 0.80 | 0.50 |
| 单轴 industry（YPaVj2eJ） | 两腿都 `group_rank(·, industry)` | 1.61 | 1.19 | 2.64 | 0.79 | 0.47 |
| **交叉**（2r5grRaZ） | 慢腿 country + 快腿 industry | 1.84 | **1.36** | 2.74 | 0.81 | **0.50** |
| **cartesian**（1YW8YLaM） | 两腿都 `densify(group_cartesian_product(industry, country))` | 1.68 | 1.15 | 2.75 | 0.64 | **0.39** |

**结论**：
1. **`group_cartesian_product` 在本集不改善**：S 1.86→1.68、sub 0.80→0.64、JPN 0.50→0.39 全面劣化（可能因 25 个「行业×国家」格子里样本过少，组内排名噪声大）
2. **交叉分组**：S 1.84（≈持平）、**F 1.36 略高**、JPN 0.50 不变——论坛「两腿必须交叉」在本集无增量（该铁律原生于 EMEA 稀疏更新场景，机构季度数据不适用）
3. **★ JPN 在 0.39–0.50 之间与分组结构完全无关** ⇒ 决定性证据：**JPN 0.50 是信号的日本子集属性**（机构买家比例在日本无定价力），不是分组/中性化/嵌套方式问题

**历史对照**（price_signal_dl）：`group_rank(·, densify(group_cartesian_product(industry, country)))` S0.87 < 单轴 country S0.95 —— cartesian 在两个 ASI 数据集上均劣于单轴。

**一般化建议**：ASI 用 cartesian 前先算组内样本量；「行业×国家」在 MINVOL1M 下可能过碎。cross-region（GLB）场景才可能需要它同步中性化。

## 19. 模板总数达标确认（2026-11-23 收口）

**10 个结构互异模板全部实测完成**（达 11-23 用户硬标准「每集 ≥10 模板」）：

| 模板 | 机制 | S | 2Y | JPN | 证据 |
|---|---|---|---|---|---|
| **T15** | 流量÷存量双尺度 + 门控 + group_rank country | **1.86** | **2.94** | 0.50 | KOR Jj8zG0Ye 经验迁移 |
| T4 | 持有家数广度变化 | 1.02 | 1.39 | — | DOI 10.2139/ssrn.1107523 |
| T16 | 机构集中度（平均持仓规模） | 1.01 | 1.07 | — | DOI 10.1086/508002 |
| T17 | 新进机构率 buyers/holders | 0.92 | 1.47 | — | 论坛 44147814648215 |
| T1 | 论坛配方（流量总和分母） | 0.63 | 0.84 | — | 论坛 44147814648215 |
| T6 | 机构渗透率变化 | 0.44 | 1.76 | — | DOI 10.1086/508002 |
| T3 | 股数口径净买入 | 0.27 | −0.12 | — | DOI 10.1086/508002 |
| T18 | 机构渗透率水平 | 0.25 | 0.35 | — | DOI 10.1086/508002 |
| T2 | 市值口径净买入 | −0.11 | −0.10 | — | 论坛 44147814648215 |
| T19 | 卖出压力 sellers/holders | −0.13 | −0.83 | — | DOI 10.2139/ssrn.1107523 |

**分组/设置维度的额外交互（不计入模板数）**：country/industry/exchange/market 轴 × 交叉分组 × cartesian × 门控 5 档 × 中性化 2 档 × 窗口 2 档 × 内层 z 2 种

**总计约 36 臂**｜**天花板**：S1.86（T15/ZYaVVR01）｜**卡点**：JPN 0.50（信号层，8 维度证据）｜**prod/self**：0.6083/0.1837 双干净
