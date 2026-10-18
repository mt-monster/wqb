# EUR Analyst 类别 · 数据集全面扫描与字段画像（2026-10-17）

> 本文档是 EUR region 下 Analyst 类别的**数据集普查 + 字段画像存档**（任务步骤 1–2 的交付物）。
> 数据来源：平台 `/data-sets` + `/data-fields` 实时接口（2026-10-17，EUR / D1 / TOPCS1600）。
> 塔态权威来源：`get_pyramid_alphas`（EUR/D1，2026-10-17 复核）。

## 一、塔态与选集约束

**EUR/D1 金字塔 alphaCount（权威，2026-10-17）**：

| 塔 | alphaCount | 说明 |
|---|---:|---|
| model | 1 | 已点亮 |
| fundamental | 1 | 已点亮 |
| **analyst** | **1** | `786pLKnb`（**PPA 通道**，按项目口径「RA 才是唯一可接受通道」⇒ 该塔实际**无 RA 产出**） |
| other | 1 | `LL5VwgO1`（CH_REG/RA） |
| risk | 1 | 已点亮 |
| 其余 9 类 | 0 | 未点亮 |

⇒ 用户明确指示「扫描全部 Analyst 数据集」⇒ 本轮以 Analyst 16 个数据集为扫描范围。
⇒ analyst 塔现有 1 颗系 PPA（不计入 RA 口径），故 Analyst 塔为**本轮主攻方向**。

## 二、Analyst 16 个数据集全量扫描（平台权威枚举）

| # | 数据集 | 字段数(平台) | αC | cov | 类型构成（实测） | 已测? | 历史最佳 S | 判定 |
|---|---|---:|---:|---:|---|---|---:|---|
| 1 | ★`analyst_factor_signals` | 108 | 58 | 0.55 | 108 MATRIX | ✅ | **1.71** | ★ 曾产 `786pLKnb`（PPA）；prod 池已被占 |
| 2 | ★`analyst10` | 961 | 1399 | 0.77 | 255 MATRIX + 39 VECTOR | ✅(浅) | ≤0.76 | **本轮主攻**（revise/smun/breadth 族富） |
| 3 | ★`analyst_consensus` | 1929 | **76** | 0.70 | 297 VECTOR + 3 MATRIX | ✅(浅) | ≤0.21 | breadth 无信号（旧结论），待换结构复测 |
| 4 | `analyst9` | 111 | 76 | 0.62 | 96 VECTOR + 5 MATRIX | ✅ | 1.01 | 共识水平 ≤0.76 |
| 5 | `analyst45` | 61 | 242 | 1.0 | 44 VECTOR | ✅ | 0.38 | ❌ |
| 6 | `analyst69` | 813 | 14111 | 0.65 | 247 VECTOR | ✅ | 1.48 | 结构性矛盾（TO 0.29） |
| 7 | `analyst4` | 776 | 3031 | 0.66 | 134 VECTOR | ✅ | 0.65 | TO 0.020 崩 |
| 8 | `analyst11` | 445 | 147 | 0.85 | — | ✅ | ≤0.21 | ❌ |
| 9 | `analyst14` | 121 | 267 | 0.50 | 113 MATRIX | ✅ | 0.48 | 2Y 负 |
| 10 | `analyst15` | 1744 | 898 | 0.51 | 297 MATRIX | ✅ | 0.17 | ❌ |
| 11 | `analyst39` | 24 | 541 | 0.88 | 24 MATRIX | ✅ | 0.19 | ❌ |
| 12 | `analyst40` | 22 | 12 | 0.30 | 董事变动 | ✅ | 0.20 | TO 爆炸 |
| 13 | `analyst7` | 1111 | 3081 | 0.50 | 299 MATRIX(actual) | ✅ | 0.10 | ❌ |
| 14 | `analyst_base_ref` | 17 | 6 | 0.55 | 股数/价格参考 | ✅ | 0.36 | 2Y −0.58 |
| 15 | `analyst81` | 5 | 5 | 0.24 | — | 跳过 | — | cov<0.35 |
| 16 | `model52` | 3 | 2 | 0.20 | 违约概率 PD | ✅ | −0.17 | cov 过低 |

**本轮筛选结论**：候选 = **`analyst10`**（主攻，修正/breadth 族富、cov 0.994 字段多）+ **`analyst_factor_signals`**（残差化等新结构复测）+ `analyst_consensus`（低拥挤备选）。

## 三、字段画像（存档）

### 3.1 `analyst_factor_signals`（108 MATRIX，全部 cov≥0.27；核心族 cov 0.85–0.94）

完整字段清单：`cache/_afs_fields.json`（本仓库缓存）+ 下表为分族画像。

| 字段族 | 代表字段 | cov | user | 更新频率 | 分布/含义 | 可用性 |
|---|---|---:|---:|---|---|---|
| **修正幅度** | `eps_revision_magnitude` | **0.931** | 0 | 日频（事件驱动） | Street revision 缩放幅度 | ★ 已验证原语（÷分歧度） |
| | `revenue_revision_magnitude` | 0.927 | 4 | 日频 | 收入修正幅度 | ✅ 待测（旧结构 S≤1.49） |
| | `netprofit_revision_magnitude` | 0.927 | 2 | 日频 | 净利修正幅度 | ✅ 待测 |
| **分歧度** | `eps_y1_estimate_coeff_var` | 0.870 | 3 | 月频 | CV=std/mean | ★ 已验证分母 |
| | `eps_y1_estimate_skewness` | 0.936 | 3 | 月频 | Pearson 偏度 | ✅ Estimate-Skew 配方 |
| | `eps_y1_estimate_asymmetry` | 0.870 | 0 | 月频 | 分布不对称 | ✅ |
| **共识水平** | `eps_y1_consensus_value` | 0.911 | 2 | 月频 | FY1 EPS 增速预期 | ⚠ 裸 rank 被禁；须 Δ/残差 |
| | `eps_y2_consensus_value` | 0.936 | 0 | 月频 | FY2 EPS 增速预期 | ✅ |
| **修正变化** | `eps_y1_estimate_change_3mo` | 0.931 | 6 | 月频 | 3 个月修正变化 | ✅ revision momentum |
| **季度估计** | `eps_q1_estimate_change_1mo` | 0.461 | 0 | 月频 | 快变量 | ✅ TO 合格 |
| **慢变量（TO 崩）** | `eps_estimate_volatility_adj_*` | 0.18–0.27 | 0–1 | 年频 | 波动调整 | ❌ TO 0.027 级 |
| **CAGR** | `eps_y1_cagr_*` | 0.66–0.85 | 0–1 | 年频 | 复合增速 | ❌ 旧判死（S≤0.51） |

**更新频率判据（类别卡实证）**：**快变量（change/revision/surprise）TO 合格；慢变量（level/volatility/CAGR）TO 崩** ⇒ 选集看更新频率而非仅看 type。

### 3.2 `analyst10`（294 实测：255 MATRIX + 39 VECTOR；225 个 cov≥0.5）

完整字段清单：`cache/_fields_analyst10.json`。分族画像：

| 字段族 | 代表字段 | cov | user | 含义 | 可用性 |
|---|---|---:|---:|---|---|
| ★**EBI 修正** | `anl10_ebirevise_value_fy1/fy2` | **0.994/0.993** | 5/0 | EBIT 前收益修正 delta consensus | ★★★ 最高覆盖 |
| | `anl10_ebirevise_ratio_to_consensus_fy1/fy2` | 0.994/0.993 | 0/1 | 修正÷共识（**预归一化**） | ★★★ |
| | `anl10_ebirevise_ratio_to_close_fy1` | 0.994 | 1 | 修正÷收盘价 | ★★ |
| **EBT 修正** | `anl10_ebtrevise_value_fy1/fy2` | 0.920 | 2/1 | 税前收益修正 | ★★ |
| **DPS 修正** | `anl10_dpsrevise_value_fy1/fy2` | 0.895/0.905 | 3/1 | 股息修正 | ★★ |
| **CapEx 修正** | `anl10_cpxrevise_value_fy1/fy2` | 0.844/0.836 | 1/1 | 资本开支修正 | ★★（Margin Scissor 原料） |
| **Cash 修正** | `anl10_cshrevise_value_fy1/fy2` | 0.588 | 1/1 | 现金修正 | ★ |
| ★**修正广度（breadth）** | `anl10_analyst_innovation_tbv_innovate_increase/decrease_fy1` | 0.502 | 1/3 | 创新性上调/下调**家数** | ★★★ 论坛配方直落 |
| | `anl10_analyst_innovation_tbv_normal_increase/decrease_fy1` | 0.502 | 1/1 | 普通上调/下调**家数** | ★★★ |
| | `anl10_analyst_innovation_tbv_innovation_score_fy1` | 0.502 | 1 | 创新评分 | ★ |
| **覆盖家数** | `anl10_*smun_*`（cpx/dps/ebi/ebt × 1qf/2qf/1yf/2yf） | 0.90–1.00 | 0–8 | 覆盖分析师数 | ★ 质量过滤/归一化分母 |
| **预测意外** | `anl10_*_pred_surps_v0/v1/v2` | ~1.00 | 1–3 | StarMine 式 smart surprise | ★★ |
| **共识值** | `anl10_cpxfy2_consensus` 等 | ~1.00 | 2 | 各指标 FY1/FY2 共识 | ★ |
| **细节 VECTOR** | `anl10_dpspast_det_analyst_287` 等 | 1.00 | 0 | 分析师 ID/时间/估计年龄 | ⚠ 需 vec_* 聚合 |

**合规性**（`gate.py` 实测）：同数据集内 `subtract`/`divide` **全部放行**（net breadth、revision÷smun、Margin Scissor 均 pass）；跨集才需声明。

### 3.3 `analyst_consensus`（300 实测：297 VECTOR + 3 MATRIX；236 cov≥0.5）

完整字段清单：`cache/_fields_analyst_consensus.json`。旧结论「breadth ≤0.21 无信号」；297 VECTOR 需 `vec_avg`/`vec_sum` 聚合。**备选**（若 analyst10 无果再上）。

### 3.4 `analyst9` / `analyst45`

- `analyst9`：101 字段（96 VECTOR），95 cov≥0.5，共识水平类（旧 S≤0.76）。
- `analyst45`：44 VECTOR 全 cov≥0.5（旧 S 0.38）。

## 四、本轮采用的结构清单（均为合规形态）

| 结构 | 表达式骨架 | 来源 | 合规 |
|---|---|---|---|
| **修正÷分歧度** | `signed_power(group_rank(divide(rev, ts_mean(cv,55)), industry), 3.0)` | EUR analyst 战役（2026-10-13） | ✅ 同集 |
| **双窗秩乘积** | `multiply(rank(ts_mean(F,2)), rank(ts_mean(F,252)))` | 破 prod 墙（2026-10-14） | ✅ 单字段 |
| **净广度** | `subtract(up_count, down_count)` | 论坛 breadth 帖（2026-09-04） | ✅ 同集 |
| **Margin Scissor** | `subtract(cpxrevise, ebirevise)` | 论坛 5 信号帖（2026-08-12） | ✅ 同集 |
| **修正动量** | `ts_delta(rev, 22)` | 论坛（revision momentum） | ✅ 单字段 |
| **残差化** | `rank(-ts_regression(ts_zscore(returns,252), ts_zscore(F,252), 252, rettype=0))` | IND（2026-10-16） | ✅ 残差三式之一 |

## 五、存档索引

| 文件 | 内容 |
|---|---|
| `cache/_afs_fields.json` | analyst_factor_signals 108 字段全量 |
| `cache/_fields_analyst10.json` | analyst10 294 字段全量 |
| `cache/_fields_analyst_consensus.json` | analyst_consensus 300 字段全量 |
| `cache/_fields_analyst9.json` / `cache/_fields_analyst45.json` | 其余两集 |
| 本文档 | 普查表 + 分族画像 + 结构清单 |

---

## 六、回测验证结果（2026-10-17，波 568–577，10 波 ≈100 条仿真）

> 全部：EUR / TOPCS1600（除标注）/ D1 / decay 1 / SUBINDUSTRY / trunc 0.08 / nanHandling ON / maxTrade OFF。
> 合规自检：所有表达式过 `gate.py`（同数据集内 subtract/divide 放行；无跨集；无加权腿）。

### 6.1 核心战绩：唯一有效原语的「窗口 × 指标 × prod」全谱

原语 = `ts_target_tvr_decay(signed_power(group_rank(divide(eps_revision_magnitude, ts_mean(eps_y1_estimate_coeff_var, W)), industry), 3.0), target_tvr=0.18)`

| 窗 W | alpha | S | F | TO | 2Y | sub | robust | **prod** | 互相关(786pLKnb) | 判定 |
|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 55 | `786pLKnb` | 1.71 | 1.09 | 0.1123 | 1.78 | ✅ | ✅ | 0.6170 | — | PPA 已提交 |
| **60** | **`0mj9nM36`** | **1.75** | **1.12** | 0.1121 | **1.74** | 1.20 | 1.01 | **0.9920** ❌ | **0.994** | IS 全过（failed_ra=0）但同腿 |
| 60（无 tvr） | `58j39lpM` | 1.75 | 1.12 | 0.1121 | 1.74 | 1.20 | 1.01 | 同上 | — | 同腿 |
| 66 | `wp9O6E66` | 1.66 | 1.04 | 0.112 | 1.50 | 1.16 | 1.01 | 0.9818 ❌ | 0.9866 | 2Y 差 0.08 + 同腿 |
| 77 | `XgRPX8r0` | 1.58 | 0.96 | 0.1117 | 1.48 | 1.07 | 0.96 | — | — | 双差 |
| 88 | `zqrQaRXO` | 1.52 | 0.90 | 0.1112 | 1.20 | 1.00 | 0.92 | — | — | 双差 |

⇒ **`revision_magnitude ÷ dispersion` 族（含全部窗变体）与 786pLKnb 互相关 ≥0.98 ⇒ 对 RA 通道封闭。**

### 6.2 各结构族验证结果

| 结构族 | 代表读数 | 结论 |
|---|---|---|
| **残差化**（`rank(-ts_regression(ts_zscore(returns,252), ts_zscore(F,252), 252, rettype=0))`，decay 126） | S 0.51–1.65，**2Y 0.37–1.08 全 DEAD** | ❌ EUR analyst 信号本就「残差状」，该结构不适用 |
| **双窗秩乘积** × 8 字段族 | winner 原语版 S 1.42/2Y 1.62；change_3mo 版 S 1.57/2Y 1.06 | ❌ 降 S（该结构的 prod 收益在该族不需要——本来就过不了 2Y） |
| **change_3mo 提 2Y**（tvr/ts_mean 22/66/5/换轴/换分母/ts_delta 加速度） | S 1.19–1.92，**2Y 0.28–0.93** | ❌ **2Y 硬顶 ~0.93**（快信号结构性缺 2Y） |
| **近miss push**（revenue/netprofit 跨指标版、y2 分歧度分母、y2_change） | S ≤1.56、2Y ≤1.17 | ❌ |
| **surprise(SUE) 族**（`eps_surprise_mean_diff` 及 Δ/÷stddev） | S ≤0.88 | ❌ |
| **trend_slope / zscore / trailing_4q** | S ≤0.88 / 0.06 / 0.40 | ❌ |
| **算子替换**（group_zscore / quantile / normalize / ts_scale / rank） | group_zscore 版 S **1.12**（vs signed_power 1.75） | ❌ 降 S；quantile/normalize/ts_scale 批遇平台瞬态未隔离 |
| **门控**（trade_when 高分歧度 / 正修正） | S 1.35 / 1.05（后者 2Y 1.89） | ❌ 降 S |
| **universe 变体**（change_3mo @ TOP2500） | S 1.82 但 sub 0.73 FAIL + 2Y 0.80 | ❌ |
| **`analyst10` 原始 revise/breadth/scissor/surps** | TO **1.40–1.75 爆炸**，S ≤0.74 | ❌ |
| **`analyst10` ts_mean(22) 平滑版** | TO 修复（0.01–0.17）但 S **0.03–0.70**、2Y 负 | ❌ **噪声型「平滑即杀」⇒ 数据集判死** |
| **`analyst_consensus`**（vec_avg 动量 / vec_stddev 分歧 / count 动量 / CV） | S ≤0.88（最佳 `eps_estimate_zscore` 0.88） | ❌ 该集只有 actual+count，无预测值 |

### 6.3 最终判定

**本轮（EUR Analyst 专项）未产出新的可提交 RA alpha。**

唯一 IS 全闸通过（`failed_ra_count = 0`）的候选 `0mj9nM36`（窗 60，S 1.75 / F 1.12 / 2Y 1.74 / sub 1.20 / robust 1.01）因 **prod 0.9920**（与 PPA 提交的 `786pLKnb` 互相关 0.994）被挡在 RA 闸外。

**根因**：EUR analyst 类别只有**一个**有效原语（修正幅度 ÷ 分歧度），其 prod 池已被 2026-10-12 的 PPA 提交占用；其余字段族全部卡 IS 闸（2Y 或 S 不足）。

### 6.4 可迁移结论（已同步至 skill）

1. **PPA 提交占 prod 池**：同原语的任何变体（窗 55–88、幂次、tvr、轴）互相关 ≥0.98 ⇒ **判某腿能否走 RA 必须实测 prod，不能只看 self**（self 仅 0.178 ✅ 会骗人）。
2. **快信号（change_3mo）2Y 硬顶**：S 1.90 也过不了 IS_LADDER 1.58；平滑/换轴/加速度/宇宙均无效 ⇒ **2Y 需要「慢变量结构化」（分母长窗平滑），快信号无解**。
3. **窗谱技术**：同一原语扫窗（55/60/66/77/88）可定位 IS 甜点；本例甜点在 55–60，且**甜点窗与 prod 占用窗重合** ⇒ 扫窗救不了被占的腿。
4. **`analyst10` = 噪声型数据集**（原始 TO 爆炸 + 平滑即杀双重签名）。
5. **`analyst_consensus` 无预测值**（只有 actual/count/flag）⇒ 别对「大字段数」抱期望，先核字段语义。
6. **工程**：multi-sim children 是子仿真 ID ⇒ 用 MCP `harvest_multisim_alphas`；派发前做字段存在性预检（`netprofit_y1_estimate_coeff_var` 不存在曾连坐整批）。

### 6.5 补充批（wave578）：修正幅度原语的「未试模板族」补全（2026-10-17）

> 回应用户追问「所有针对修正幅度的模板都试了吗」——本轮补试 7 类从未试过的模板族。

| 模板族 | 表达式骨架 | S | F | 2Y | 判定 |
|---|---|---:|---:|---:|---|
| ★**ts_zscore 外层**（窗 60） | `ts_zscore(divide(rev,cv,60),252)` | **0.51** | 0.16 | 0.19 | ❌ **灾难性**（与 techindi 上 S+0.3 完全相反 ⇒ `ts_zscore` 非普适，在该原语上是摧毁者） |
| **ts_zscore 外层**（窗 55） | 同上，窗 55 | 0.47 | 0.14 | 0.14 | ❌ |
| **修正加速度** | `ts_delta(eps_revision_magnitude, 22)` | −0.10 | −0.01 | −0.06 | ❌ 二阶导无信号 |
| **加速度÷分歧** | `divide(ts_delta(rev,22), ts_mean(cv,60))` | −0.10 | −0.01 | 0.93 | ❌ |
| **winner 边际** | `ts_delta(divide(rev,cv,60), 22)` | 0.09 | 0.01 | 1.00 | ❌ |
| **自标准化** | `divide(rev, ts_mean(rev,252))` | −0.21 | −0.04 | −0.50 | ❌ |
| **历史分位** | `ts_rank(rev, 252)` | 0.33 | 0.08 | −0.36 | ❌ |
| **修正×分歧时序相关** | `ts_corr(rev, cv, 252)` | 0.08 | 0.01 | −0.21 | ❌ |
| ⚠**双窗 add 分母** | `divide(rev, add(ts_mean(cv,22),ts_mean(cv,252)))` | **1.51** | 0.91 | **1.57** | ⚠ 三差极近（S−0.07/F−0.09/2Y−0.01）但均未过线；且同族 prod 必 ≥0.98 ⇒ 无意义 |
| **双窗乘积分母** | `divide(rev, multiply(ts_mean(cv,60),ts_mean(cv,252)))` | 1.11 | 0.57 | 0.09 | ❌ |

⇒ **修正幅度原语的模板穷尽结论**：分子侧（3 指标 × 水平/增量/自标准化）× 分母侧（12 种）× 外层（14 种包装/轴/幂次/tvr）× 残差化/门控/秩乘积 × 设置（decay/universe/maxTrade）**全部试尽**；IS 甜点唯一（窗 55–60 的 `rev ÷ ts_mean(cv,W)`），且**整个原语族与 PPA 提交的 786pLKnb 互相关 ≥0.98 ⇒ prod 池封闭，与模板选择无关**。

### 6.6 外部文献检索与「未试模板」补全（2026-10-17）

> 回应用户「查论坛或外部金融论文，看有无其它针对性模板和思路还没试」。
> 论坛 MCP 本轮持续故障（5 次 fetch failed）⇒ 以外部文献为主（4 篇直接相关论文），论坛待恢复后补检。

**文献清单与可落地的「未试方向」**：

| # | 论文 | 核心结论 | 落地为 BRAIN 模板 | 状态 |
|---|---|---|---|---|
| 1 | **Zhang (2006) / Diether-Malloy-Scherbina 扩展**（Analysts' Forecast Dispersion, Bias and Returns） | **分歧度可预测未来修正**（高分歧 ⇒ 未来负修正）；「预期修正」排序的月度收益差 **0.89%/月**，比单纯分歧度更强；剥离预期成分后的「条件分歧度」显著**正向**预测收益 | `rank(-ts_regression(rev, ts_mean(cv,W), 252, rettype=0))` = **修正意外**（实际修正 − 分歧度预期修正）；`reverse(ts_mean(cv,60))` = 预期修正代理（分歧度异象） | wave579 #1-3 |
| 2 | **Aiolfi, Rodriguez & Timmermann (2009)**（Understanding Analysts' Earnings Expectations） | 修正** asymmetric**：负修正频率更高、**幅度 2 倍、波动 3 倍**、**负修正后跟负修正**（持续性）；三状态模型（正/零/负） | `if_else` 拆分正/负修正单独建信号；`ts_mean(if_else(less(rev,0),1,0),66)` = **修正悲观率**（负修正时间占比） | wave579 #4-6 |
| 3 | **Scherbina (NBER 2004)**（Disagreement, Bias and Returns） | **分析师覆盖数下降**（3 个月）⇒ 年化收益低 **4.8%**；**右偏预期分布**负向预测收益；分析师「不愿下修」（underrevision） | `ts_delta(vec_avg(estimate_count), 66)` = **覆盖下降**信号；`reverse(skewness)` = 右偏异象 | wave579 #7-10 |
| 4 | **Driskill（分析师分歧衡量指标构建）** | 预测**时点**很重要（公告前 90–91 天的预测活动）；事前/事后窗口调整后分歧度与量、收益关系变强 | ⚠ EUR 无财报日历字段 ⇒ **无法落地**，记录备查 | — |
| 5 | **AAA（Analysts Say Anything Without Revising）** | 分析师通过**其它输出**（非 CQE 修正）表达分歧；「不修正」本身含信息 | ⚠ 需 SPT/FQE 文本字段 ⇒ EUR 无此字段，记录备查 | — |

### 6.7 文献模板实测结果（wave579，10 条全灭）

| # | 模板（文献来源） | 表达式骨架 | S | 2Y | 判定 |
|---:|---|---|---:|---:|---|
| 1 | **修正意外**（Zhang/DMS 扩展） | `rank(-ts_regression(rev, ts_mean(cv,60), 252, rettype=0))` | −0.20 | 1.10 | ❌ |
| 2 | 同上（窗 55） | 同 #1 | −0.24 | 1.10 | ❌ |
| 3 | **分歧度异象**（Diether et al. 2002） | `reverse(ts_mean(cv,60))` + tvr | **−1.21** | −1.20 | ❌ 但暴露**区域差异**：反向为 −1.21 ⇒ **EUR 高分歧 ⇒ 高收益（+1.21）**，与美国经典异象相反；S 仍不足 |
| 4 | **负修正单独信号**（Aiolfi asymmetry） | `if_else(less(rev,0), rev, 0)` | 1.05 | 0.02 | ❌ 拆分丢信息（合并版 1.75 ≫ 单侧 1.05） |
| 5 | 正修正反向 | `reverse(if_else(greater(rev,0), rev, 0))` | −1.34 | −0.35 | ❌ ⇒ **正修正才是有效侧**（与 #4 合并解读） |
| 6 | **修正悲观率**（Aiolfi persistence） | `ts_mean(if_else(less(rev,0),1,0), 66)` | −0.94 | 0.10 | ❌ |
| 7 | **右偏异象**（Scherbina/Zhang） | `reverse(skewness)` + tvr | −0.26 | 0.72 | ❌ EUR 无此效应 |
| 8 | 自相对 skew 反向 | `reverse(divide(skew, ts_mean(sk,252)))` | 0.13 | 0.20 | ❌ |
| 9 | **覆盖下降**（Scherbina，consensus count） | `ts_delta(vec_avg(estimate_count), 66)` | −0.15 | −0.56 | ❌ |
| 10 | **覆盖下降**（Scherbina，anl10 smun） | `ts_delta(anl10_ebtsmun_1yf, 66)` | −0.40 | −0.48 | ❌ |

**文献结论**：4 篇可落地论文的全部模板（修正意外/分歧度异象/修正不对称/悲观率/右偏/覆盖下降）在 EUR analyst 上**全部无效**；唯一有效仍是「修正幅度 ÷ 分歧度」本身（Zhang 2006 的原生日历异象在 EUR 也成立，但 prod 被占）。**EUR 与美国文献的系统性差异**：分歧度异象方向相反（#3）、修正不对称性不成立（#4/#5）、右偏无效应（#7）、覆盖下降无效应（#9/#10）。

**论坛状态**：MCP 论坛检索本轮 6 次全部 `fetch failed`（服务不稳定）；本会话此前已读 2 篇高相关帖（「5 个信号」42659792904343、「修正广度」43250301270295），其可落地模板（Margin Scissor/breadth/revision momentum）已在 wave569/575 实测失败；其余帖文方向（目标价区间位置）在 EUR 已判死的 analyst14 族数据集上，无落地字段。

### 6.8 「换腿降 prod」专项调查（wave580–582，回应用户追问）

**问题**：`0mj9nM36`（IS 全闸过）被 prod 0.9920 挡在 RA 闸外（与 PPA 提交的 786pLKnb 互相关 0.994）——能否通过换腿降 prod？

**换腿路径分级实测**：

| 级别 | 手段 | 互相关(786pLKnb) | prod | S | 判定 |
|---|---|---:|---:|---:|---|
| **参数级** | 幂次 6.0（持仓集中） | 0.9362 | 0.9310 | 1.61 | ❌ 降幅不足（需 <0.7） |
| | 幂次 8.0 | — | — | 1.50 | ❌ S 死 |
| | INDUSTRY 中性化档 | 0.9349 | 0.9231 | **1.78** | ❌ 降幅不足（但指标更优！见下） |
| | lambda_max=0.5（时序衰减受限） | 0.9855 | 0.9837 | 1.60 | ❌ 几乎无效 |
| | lambda_min=0.5 | — | — | 1.75 | ⚪ 逐位同基线（无效） |
| **输入级** | `change_3mo ÷ cv`（y1/y2/q1/revenue/netprofit 全试） | — | — | **0.74–1.13** | ❌ S 全塌 ⇒ 「修正÷分歧度」的强度是 **`eps_revision_magnitude` 字段特有**（Street revision 缩放构造），非结构通用 |
| **门控级** | trade_when 跨度量门控（change_3mo/q1/revenue/y2 方向 + 低分歧） | — | — | **0.49–1.50** | ❌ S 全塌 ⇒ 信号强度需全暴露 |
| **universe 级** | TOP1200 / TOP800 | — | — | **0.57–0.82** | ❌ S 死（analyst 覆盖集中于大市值，小宇宙丢覆盖） |
| **decay 级** | decay 4 | ~0.99（同序） | — | 1.58/1.59 但 **F 0.97** | ❌ 差 F 0.03；且同腿 |

**机理解释（核心结论）**：**prod 0.99 与 S 1.75 同源**——二者都是「`eps_revision_magnitude ÷ ts_mean(cv,W)` 在 TOPCS1600 上的排序」的结果。保序形变/参数微调 ⇒ 互相关地板 ~0.92（离 0.7 差 0.22，无接近者）；改变排序核心 ⇒ 丢强度。**「强度-占用」锁死**。

**★ 意外收获（INDUSTRY 中性化档）**：`LL56W0Q9` = winner 原语 @ **INDUSTRY** 中性化 ⇒ S **1.78** / F 1.17 / **2Y 1.89** / robust **1.23** / failed_ra=0，**全面优于** SUBINDUSTRY 版（1.75/1.12/1.74/1.01）。⇒ 区域 settings.json 声明的 SUBINDUSTRY 并非该原语最优档（历史从未扫过 neutralization 设置档，只扫过 group_rank 轴）。虽仍同腿（prod 0.9231），但**这是全场最优 IS 配置**，记录备查（若未来 prod 墙松解，优先提交此版）。

### 6.9 换腿调查最终结论（五级全试，全面封死）

| 换腿级别 | 最好 S | 最好 prod/互相关 | 封死原因 |
|---|---:|---:|---|
| 参数级（幂次/lambda/tvr/轴） | 1.78 | 0.9231 | 保序 ⇒ 相关性地板 0.92 |
| 输入级（换修正度量字段） | 1.13 | — | 「修正÷分歧度」强度 = `eps_revision_magnitude` 字段特有 |
| 门控级（跨度量 trade_when） | 1.50 | — | 信号强度需全暴露 |
| universe 级（TOP1200/800） | 0.82 | — | analyst 覆盖集中于大市值 |
| decay 级（decay 4） | 1.59 | ~0.99 | F 0.97 差 0.03 且同腿 |

**★ 根论：prod 0.99 与 S 1.75 同源**——二者同为「`eps_revision_magnitude ÷ ts_mean(cv,W)` 在 TOPCS1600 上的排序」之结果。**「强度-占用」锁死**：任何保持该排序的变换保强度但保高相关；任何改变排序的变换降相关但丢强度。⇒ **换腿不能降 prod；要出 RA 腿必须换原语/换数据集/换区域**。

**★ 附带最优发现（INDUSTRY 中性化档）**：`LL56W0Q9`（winner @ INDUSTRY neut）= S 1.78/F 1.17/2Y 1.89/robust 1.23/failed_ra=0，**全场最优 IS 配置**（SUBINDUSTRY 档并非该原语最优——历史从未扫过 neutralization 设置档）。prod 0.9231 仍同腿，但若 prod 墙松解，优先提交此版。
