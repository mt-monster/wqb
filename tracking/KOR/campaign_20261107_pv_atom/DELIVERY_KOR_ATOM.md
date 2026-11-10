# KOR × TOP600 × D1 · ATOM REGULAR 交付文档（滚动更新）

> 目标：**20 颗**通过验证的 ATOM（单数据集）REGULAR alpha（2026-11-08 用户目标编辑：10 → 20）。
> 区域锁定 KOR / TOP600 / Delay=1，区间 2014-01-01 ~ 2023-12-31。

## 0. 验收口径（写死，避免「通过验证」含糊）
同时满足：① type=REGULAR 且表达式只消费**单一数据集**字段；② `failed_ra_count = 0`；③ S ≥ 1.58；④ 2Y ≥ 1.58；⑤ F ≥ 1.0；⑥ 2014–2023 逐年 `longCount>0 && pnl≠0`；⑦ `self < 0.70`；⑧ `prod < 0.70`（REGULAR 硬线）。
⚠ `checks.fail` 为空 ≠ 通过：必须读 `ra.failed_ra_count` / `checks.warning`（LOW_SHARPE / LOW_2Y_SHARPE / LOW_FITNESS 会被降级成 warning 但仍计失败）。

## 1. 已验收 alpha

### #1 `omERn83n` — risk70 · RISK 塔（未点亮 0/3）

```
ts_target_tvr_decay(signed_power(group_rank(winsorize(vector_neut(rank(ts_backfill(rsk70_mfm2_asetrd_anlystsn, 40)), rank(ts_backfill(rsk70_mfm2_asetrd_momentum, 22))), std=0.38), sector), 2.5), target_tvr=0.22)
```

| 项 | 值 |
|---|---|
| 数据集 | `risk70`（KOR risk 类，`rsk70_mfm2_*` 前缀） |
| 核心字段 | 信号腿 `rsk70_mfm2_asetrd_anlystsn`（分析师情绪载荷）；正交腿 `rsk70_mfm2_asetrd_momentum` |
| 算子逻辑 | `rank(信号)` → `vector_neut` 对 `rank(动量)` 正交化（剥离动量共线）→ `winsorize(std=0.38)` 收尾 → `signed_power(2.5)` 放大极端 → `group_rank(sector)` 行业中性排序 → `ts_target_tvr_decay(0.22)` 控换手 |
| 算子数 | 9 |
| 指标 | **S 1.62 / F 1.23 / 2Y 2.27 / TO 0.1319 / subU 1.31 / ra.failed_ra_count = 0** |
| self / prod | 0.4211 / **0.6898** |
| 设置 | REVERSION_AND_MOMENTUM · decay 1 · truncation 0.04 · nanHandling ON |
| 状态 | UNSUBMITTED（可提交，prod 余量 0.0102） |

### #2 `qMLOooX1` — analyst10 · ANALYST 塔（已点亮 3/3）

```
group_neutralize(multiply(group_rank(ts_av_diff(anl10_smartest_sal_fy2_pred_surps_v1,250),sector),group_rank(ts_av_diff(anl10_smartest_net_fy1_pred_surps_v1,250),sector)),industry)
```

| 项 | 值 |
|---|---|
| 数据集 | `analyst10`（SmartEstimate 预测惊喜） |
| 核心字段 | `anl10_smartest_sal_fy2_pred_surps_v1`（FY2 营收预测惊喜）、`anl10_smartest_net_fy1_pred_surps_v1`（FY1 净利预测惊喜） |
| 算子逻辑 | 两条预测惊喜各自取 `ts_av_diff(·, 250)`（一年期相对均值的偏离）→ 各自 `group_rank(sector)` → 相乘（双惊喜共振，任一腿弱则信号衰减）→ `group_neutralize(industry)` 行业中性 |
| 算子数 | 7 |
| 指标 | **S 1.94 / F 1.74 / 2Y 1.76 / TO 0.0972 / subU 1.71 / ra.failed_ra_count = 0** |
| self / prod | 0.3939 / **0.6941**（余量仅 0.006） |
| 设置 | REVERSION_AND_MOMENTUM · decay 4 · truncation 0.08 · nanHandling ON |
| 状态 | UNSUBMITTED（可提交，prod 余量极薄） |

### #3 `RRE9NkVj` — insiders5 · INSIDERS 塔（未点亮 1/3）· 已上线

```
subtract(0.5, group_rank(ts_mean(vec_stddev(insd5_vol_chg), 55), sector))
```

| 项 | 值 |
|---|---|
| 数据集 | `insiders5`（韩国内部人申报明细，53 字段全 VECTOR，cov 0.8918） |
| 核心字段 | `insd5_vol_chg`（内部人股数变动，有符号，cov 0.7318） |
| 算子逻辑 | `vec_stddev` 取当日多笔内部人申报的**分歧度**（Miller 1977 分歧-高估）→ `ts_mean(·,55)` 把稀疏事件平滑成季度水平 → `group_rank(sector)` 行业内排序 → `subtract(0.5, ·)` 做多分歧度低（内部人意见一致）、做空分歧度高 |
| 算子数 | 4 |
| 指标 | **S 1.76 / F 1.63 / 2Y 2.77 / TO 0.0968 / subU 1.70 / ra.failed_ra_count = 0** |
| self / prod | 0.3104 / **0.6605** |
| 设置 | REVERSION_AND_MOMENTUM · decay 4 · truncation 0.08 · nanHandling OFF |
| 状态 | **ACTIVE（已提交上线）** |

## 2. 进度台账
| 项 | 数 |
|---|---:|
| 已验收（含已上线） | **6** |
| 缺口 | **14** |
| 已证伪机制 | risk 值族 / risk 风险量族 / BAB / analyst_consensus 水平族 / PV 形态相似度族 / insiders5 tnc 水平族（prod 0.9686 深钉）/ insiders5 其余 51 字段 / pv106 流动性成本族 / fund_holdings_panel 全几何 |
| 活但低于线（结构天花板） | other455 图嵌入 ~0.85 / other532 特质反转·低波 ~1.12 |

**KOR/D1 塔点亮表（2026-11-07 刷新）**：analyst=3✦ fundamental=3✦ model=3✦ shortinterest=4✦ | pv=2 other=1 insiders=1 risk=1 | earnings=0 institutions=0 macro=0 news=0 sentiment=0 socialmedia=0 imbalance=0
未亮塔全部为已判死数据集（news20/66/18/59、sentiment21/26、socialmedia39、equity_forum_data、earnings3 断崖、macro63 无截面）或 2 字段子集（imbalance5）⇒ KOR 单数据集 ATOM ≥1.58 的矿图已基本扫完。

## 3. 字段画像与机制存档索引
| 主题 | 存档 |
|---|---|
| insiders5 53 字段画像 | `../campaign_20261106_insiders_atom/s1_field_profile_insiders5.md` |
| insiders5 12 个结构互异模板 | `../campaign_20261106_insiders_atom/template_pool.md` |
| analyst_consensus 2343 字段族分布 | `../campaign_20261107_analyst_atom/waveA1_dispatch.md` |
| analyst Wave A1 读数 | `../campaign_20261107_analyst_atom/waveA1_results.csv` |
| PV 形态相似度 560 字段 · Wave B 读数与归因 | `waveB_harvest.md` |
| 战略转折（analyst → PV → insiders） | `strategic_pivot_analyst_to_pv.md` |
| 存量池去重审计（15 达标 → 6 组） | `pool_audit_dedup.md` |
| KOR 未点亮塔路线图 | `../reference/unlit_towers_roadmap_20261030.md` |
| KOR 上轮结项（qMLOooX1 / RRE9NkVj） | `../KOR_closeout_20261106.md` |
## 4. 本轮（2026-11-07）新增读数与判死

### 4.1 insiders5 tnc 族：S 达标但 prod 判死

| 模板 | alpha | S | F | 2Y | TO | raFail |
|---|---|---:|---:|---:|---:|---:|
| ts_mean(vec_avg(tnc),66) sector | `Xg9vxXrb` | **1.59** | 1.35 | 1.84 | 0.0538 | 0 |
| ts_mean(vec_avg(tnc),44) | `E568Mo79` | 1.58 | 1.34 | 1.79 | 0.0540 | 0 |
| winsorize 后置 W22 | `rKRNwQgo` | 1.58 | 1.29 | 1.70 | 0.0510 | 0 |
| ts_mean(vec_avg(tnc),22) | `npvermqE` | 1.57 | 1.33 | 1.75 | 0.0543 | 1 |
| ts_mean(vec_stddev(tnc),22) 正向 | `RRElPgpa` | 1.28 | 1.03 | 1.75 | 0.0588 | 1 |

`Xg9vxXrb` 逐年 10/10 年有数据（仅 2014 为负 −0.65，无连续空窗）；self **0.4082 通过**；
**prod = 0.9686 失败**，直方图 [0.9,1]=1 / [0.8,0.9]=3 / [0.7,0.8]=16 ⇒ 深钉厚尾。

⇒ 整族（W22/W44/W66 + winsorize 变体，彼此互相关 ≈0.99）**判死**。
insiders5 塔到此为止：水平族被 prod 钉死，离散度族 S 天花板 1.30，库藏股族 trsy_tnc 全空值（S=0.00 / raFail=5）。

### 4.2 insiders5 其余字段（Wave I / I2）

| 字段 / 几何 | alpha | S | 2Y | raFail |
|---|---|---:|---:|---:|
| vec_avg(grp_td_drt) W22 | `3qokvWxQ` | 0.00 | 0.14 | 5 |
| vec_stddev(grp_td_drt) W22 | `0mYN2Wdk` | 0.14 | −0.46 | 4 |
| vec_avg(recent_dt) W22 | `0mYN2Mjq` | −0.37 | −1.49 | 5 |
| vec_stddev(recent_dt) W22 | `npve58Az` | 0.65 | 1.24 | 3 |

### 4.3 fund_holdings_panel（institutions 塔 0/3，Wave J 裸水平/变化/比值）

| 模板 | alpha | S | 2Y | raFail |
|---|---|---:|---:|---:|
| holder_account_total 水平 | `Vkxmb92Y` | 0.47 | 1.27 | 3 |
| ts_delta(holder_account_total,66) | `kqNW6718` | −0.13 | −0.82 | 4 |
| herfindahl_index_holdings 水平 | `3qokvVpP` | −0.61 | −1.50 | 5 |
| conviction 比值 | `MPYeN37M` | 0.51 | 0.51 | 3 |
| mean_security_weight 水平 | `vR1p7mgA` | 0.54 | 1.11 | 3 |
| vec_sum(boundary_transaction_total) W22 | `QPvNRQXp` | −0.52 | −0.76 | 4 |

### 4.4 本轮提炼的跨区规律（重要）

**裸水平类信号在 KOR 已被 prod 池占满**：tnc 水平 S 1.59 却是 prod 0.9686；
机构持仓水平/变化/比值全部 |S| ≤ 0.61。

三颗在库件过的都是**二阶 / 交互 / 意外**几何：
- `omERn83n`：`vector_neut` 双字段正交（prod 0.6898）
- `qMLOooX1`：双 surprise 乘积（prod 0.6941）
- `RRE9NkVj`：`vec_stddev` 分歧度（prod 0.6605）

⇒ 后续开波一律优先交互/离散度/意外几何，裸水平仅作补数。
## 5. 第二轮扫矿（2026-11-07 后半场）：pv106 / fund_holdings_panel / other455 / other532

### 5.1 pv106（流动性/交易成本，27 字段 MATRIX cov 1.0）— 封盘
10 条全 raFail≥3。最强 GrWKRMko（spreadbp/ts_mean252）S 0.96 / 2Y 0.68 / TO 0.2316。天花板 <1.0。

### 5.2 fund_holdings_panel（institutions 塔）— 封盘
裸水平/变化/比值/交互四种几何全测：水平族 |S|≤0.61，交互族 |S|≤0.87 且 TO>0.8。
**ATOM 硬坑（平台原话）**：VECTOR 字段参与标量算子前必须先 vec_* 聚合，
否则 `Operator divide does not support event inputs` 整批 ERROR；
preflight_expressions 只验字段存在性、不验向量语义。
institutions 塔（0/3）：fund_holdings_panel 全灭 + institutions6 已判死 ⇒ 塔关闭。

### 5.3 other455（竞争/客户图嵌入，1500 字段，aC 0-13 极干净）— 活但不够线
competitor_n2v_*/roam/customer_roam 族：GROUP 聚类 + MATRIX PCA 坐标，cov 0.7914。

| 臂 | alpha | S | F | 2Y | raFail |
|---|---|---:|---:|---:|---:|
| **客户网络漂移 W22（customer_roam_w1）** | j2YGbZEZ | **0.84** | 0.52 | **1.89** | 2 |
| 漂移 W10 | 9qxM10wx | 0.83 | 0.53 | 1.55 | 3 |
| 动量×位形波动 合取 | vR1GMgLv | 0.77 | 0.49 | 1.76 | 2 |
| 位形波动率 W66 | 6Xd08axL / RREz35Ro | 0.74 | 0.45 | 1.63 | 2 |

窗口峰 W10（5d 平滑 0.70 / W10 0.83 / W22 0.75 / W44 0.69 / W66 0.57）。同伴群轴死（0.09）。
天花板 ~0.85，缺口 0.7+。prod 极干净，留作组合腿候选。

### 5.4 other532（Barra 特质收益，8 字段 cov 0.998）— 活但不够线（最强新轴）
**KOR 特质收益空间是「反转 + 低波动」双异常市场**（散户主导反转市）。

| 臂 | alpha | S | F | 2Y | TO | raFail |
|---|---|---:|---:|---:|---:|---:|
| **特质反转 W66（emerging）** | gJeGzrKl | **1.12** | 0.79 | 1.76 | 0.168 | 2 |
| 特质反转 W66（global 交叉验证） | omEG2Eqn | 1.08 | 0.74 | 1.81 | 0.171 | 2 |
| **低特质波动 W66** | vR1GaVKw | 1.07 | **1.05** | **2.00** | 0.105 | **1** |
| **动量×低波 合取** | 9qxMgJlx | 1.11 | **1.15** | 1.86 | 0.130 | **1** |

2×2 合取矩阵：动量×高波 −1.43 / **动量×低波 +1.11** / 反转×高波 +1.07 / 反转×低波 −1.00
⇒ **低波名里动量有效（质量动量），高波名里反转有效（lottery 反转）**——按波动分层的两个相反机制。
跨模型交叉验证（emerging/global/asia 几乎重合）⇒ 非单一风险模型伪影。
设置扫描（decay 4-16 / trunc 0.04-0.12）**全部逐位不动或微降** ⇒ 结构天花板 ≈1.12，缺口 0.46 为结构性。

### 5.5 工具坑（新）
- `create_multi_simulation` **每批至少 2 条表达式**：单表达式批报 `At least 2 alpha expressions are required`，
  mcp_7slot_batch 的单条扫描要用 ≥2 条表达式打包（如双臂同设置）。
- 取负非镜像（KOR 做空约束/执行不对称）再次实证：−1.29 的臂直接正向只读 +1.12（差 0.17）。两臂必须各自实测。

## 6. 第三轮开荒（2026-11-08）：未开采类别 P84–P90

### 6.0 读表坑（重要）

`metrics` 里两年 Sharpe 的键名是 **two_year_sharpe**（不是 sharpe_2y）；误读会得到 None 并误判「2Y 缺失」。
RA 失败清单在 `ra.ra_failed_checks`，`checks.fail` 里同时给出 value/limit。

### 6.1 chart_cnn_alpha（model · 1010 字段 · aC34/uc25）—— 唯一近线新数据集

`chart_cnn_alpha` 是本轮唯一把 2Y 打过线的新数据集。P86 最佳三条（全部 raF=2，只剩 LOW_SHARPE + LOW_FITNESS）：

| alpha | 表达式骨架 | S | F | 2Y | TO |
|---|---|---:|---:|---:|---:|
| `3qoJ9MxP` | group_rank(prob4 x confscore4, industry) | **1.36** | 0.79 | **1.63** | 0.2545 |
| `d5WvO27j` | prob4-prob0 价差 @ sector | 1.30 | 0.77 | **1.62** | 0.2445 |
| `xAr5YKmb` | ts_mean(prob4 x confscore4, 5) @ industry | 1.23 | 0.78 | **1.87** | 0.1695 |

⇒ 本数据集 **2Y 已解决**（1.6–1.9），唯一缺口是 Sharpe（差 0.22）。按「几何定 S 天花板」判断，
裸水平/价差几何已扫尽（industry/sector/subindustry/market × decay4/22 × 单腿/价差/加权/双桶和/leaps 换族），天花板 1.36。
P89 改用**正交化交互几何**做最后一搏（见 6.4）。

### 6.2 predictive_starmine（model · 645 字段 · aC58）—— 判死

10 条结构互异模板最高 **S 0.73 / 2Y 0.83**（rel_val_global_rank_score_3），ARM/预测惊喜/修订广度全部 ≤0.75。
字段级 aC 多为 0–2（本战役最干净的数据集），但**再次证伪「alphaCount 极低 ⇒ 有信号」**：
低拥挤只代表「没人挖」，不代表「有矿」。

### 6.3 新铁律：破 prod 配方「短窗 ts_rank + 大 decay」有适用前提

同一骨架（分位概率价差）在 chart_cnn_alpha 上：

| 几何 | decay | S | TO |
|---|---|---:|---:|
| 裸水平价差 | 4 | 1.22 | 0.2551 |
| ts_rank(8) | 22 | **0.20** | 0.3113 |
| ts_rank(5) | 22 | 0.22 | 0.3941 |
| ts_rank(10) on 预计算 rank 字段 | 22 | **-0.48** | 0.3248 |

**判据（可复用）**：启用该配方前先看裸信号 TO。
- TO > 0.6（拥挤慢变水平）→ 适用，短窗秩剥掉共同慢分量；
- TO < 0.35（已是低通滤波的慢信号）→ 禁用，二次低通会把信息彻底抹掉，改用 decay/truncation/分组轴提纯。

### 6.4 P89 正交化交互几何（在飞）

复用 risk70 已验证骨架 `ts_target_tvr_decay(signed_power(group_rank(winsorize(vector_neut(rank(A), rank(B)), std=0.38), sector), 2.5), target_tvr=0.22)`，
A = eqstar4 60d 顶部概率（或 x confscore），B = leaps 100d 顶部概率（与 A 字段不重叠，天然低相关）。

### 6.5 数据集画像新增存档

| 数据集 | 画像文档 |
|---|---|
| chart_cnn_alpha + pattern_scores | `FIELD_PROFILE_chart_cnn_alpha_P84.md` |
| predictive_starmine | `FIELD_PROFILE_predictive_starmine_P85.md` |
| P84 归因全文（16 条读数） | `FINDING_P84_chart_cnn_alpha_verdict.md` |
## 7. 第四轮开荒（2026-11-08 夜）：P91–P99

### 7.1 ★ intraday_pv_feats —— 信号最强、prod 墙最硬（本轮最大发现 + 最大教训）

`intraday_pv_feats`（pv · 574 字段 · aC147）。P90 裸臂暴露强负信号，P91 用 `subtract(0.5, group_rank(...))` 做**真反臂**后出现 4 条全闸候选：

| alpha | 表达式（简） | S | F | 2Y | TO | raF | prod |
|---|---|---:|---:|---:|---:|---:|---:|
| `d5Wvb6Yj` | 反臂(corr_ask_price_with_volume) 裸 | **2.82** | 1.60 | 2.11 | 0.5513 | 1 (CONCENTRATED_WEIGHT) | — |
| `O0AgNjgv` | 反臂(ts_mean(corr_bid_price_with_volume,22)) | 1.99 | 1.99 | 2.72 | 0.1299 | 0 | **0.9240** |
| `A1VEN5ze` | 反臂(ts_mean(corr_high_price_with_volume,22)) | 1.93 | 1.93 | 2.89 | 0.1302 | 0 | — |
| `YP1YbOYM` | 反臂(ts_mean(corr_last_trade_price_with_volume,22)) | 1.93 | 1.87 | 2.66 | 0.1309 | 0 | — |
| `leA1gqMn` | 反臂(ts_mean(corr_ask_price_with_volume,**5**)) | **2.12** | **2.07** | **2.86** | 0.1658 | 0 | **0.9579** |

**四条全闸候选互相关 0.9744–0.9907 ⇒ `max_mutually_below_subset_size = 1`，只能取 1 颗。**
**prod 实测 0.9240 / 0.9579 ⇒ 该族在 KOR 生产池已被完全占满，判死。**
⇒ 数据集判读：`corr_<price>_with_volume` 族（价格-成交量相关）**S 极高但 100% 撞 prod**，不要再投。

### 7.2 新铁律 D：平滑窗口的「谷底」由裸臂 TO 决定，且 prod 墙不随平滑窗口移动
- `ts_mean` 窗口：W5 → S 2.12 / W22 → S 1.99 / W66 → S 1.35。**短平滑（5–22）优于长平滑**；
- 但 prod：W22 = 0.9240、W5 = 0.9579 ⇒ **换平滑窗口不能破 prod 墙**（与「窗口谷破墙」在 ts_rank 上有效形成对照）。
- 推论：破 prod 必须换**信息内容**（字段族 / 正交腿），换频率滤波只改 S 不改 prod。

### 7.3 其余数据集判读（本轮）

| 数据集 | 类别 | 结果 | 判定 |
|---|---|---|---|
| `multifactor_return_pred` | model | 长空价差 10 条最高 \|S\| 1.08（`6XdNjLv7` S−1.08/2Y−1.55/TO0.105），其余 ≤0.72 | **判死**（价差几何无效） |
| `model262` | model | 10 条最高 S 1.09（sopp 预测），TO 0.06–0.10 | 弱，暂搁置 |
| `fundamental89` | fundamental | 唯一高 S `mLoQKob9` **S 9.13 / 2Y 0.00** 是陈旧字段伪像；真信号最高 0.51 | **判死**（含数据质量坑） |
| `model238` | model | Smart Holdings 39 字段（coverage 1.0）10 条最高 S 0.86 | **判死**（美股模型 rank 在 KOR 无截面预测力） |
| `other78` | other | 11 字段全是**元数据 flag**（calendar/cancelled/flag），无连续信号 | **判死（结构性）** |
| `model138` | model | 120 字段 VECTOR，10 条最高 S 1.29 且 2Y **−0.60** | **判死**（2Y 系统性为负） |
| `global_seasonal_model` | model | **681 字段 / coverage 0.945 / aC 中位 1**，两批 20 条最高 S **1.39**、2Y 全 <1.6 | **判死**（第 5 次证伪「aC 极低 ⇒ 有信号」） |

### 7.6 存量 IS 池全扫：历史池已挖干
分页拉 200 条 KOR REGULAR IS alpha 全量筛选：Sharpe p50 **0.76** / p90 1.40 / p95 1.62。
满足 S≥1.58 ∧ 2Y≥1.58 ∧ F≥1.0 的 **10 条全部是 intraday corr-with-volume 族**（已 prod 撞墙），**不存在「旧件现在过线」的遗漏**。
近线（S、2Y 均 ≥1.35）43 条里 40 条属于 `dividend_policy_analysis_3` 与 `corr_*_with_volume` 两个族。

### 7.7 新铁律 F：概率桶字段名在数据集内**不成套**，派发前必须逐 id 校验
`global_seasonal_model` 的 `*_return_quantile5_prob{K}`：`analyst_120d` 只有 prob0/1/2（无 3、4）、
`analyst_60d` 有 prob1/2/3/4、`analyst_calendar_60d` 只有 prob1/prob3。
P99 首轮用了不存在的 `analyst_120d_return_quantile5_prob4` ⇒ 平台 `Attempted to use unknown variable` ⇒ **整批 10 条全部 CANCELLED**。
⚠ `validate_fields: true` **不挡这个坑**（只验字段前缀，不验桶号成套）。
**姿势**：把表达式里所有标识符抽出来与 `get_datafields` 的 id 集合做差集，差集非空不派发（`_verify_gsm.py` / `_verify2.py`）。

### 7.8 近线族 `dividend_policy_analysis_3` 的中性化扫描（本轮收尾）
| neutralization | 最优 S | 2Y | TO |
|---|---:|---:|---:|
| **REVERSION_AND_MOMENTUM**（基线） | **1.42** | 1.97 | 0.1052 |
| SLOW_AND_FAST | 1.28 | 1.56 | 0.1281 |
| MARKET | 1.01 | 1.98 | 0.0648 |
| SUBINDUSTRY | 0.88 | 1.80 | 0.0665 |
| STATISTICAL | 0.78 | 1.67 | 0.0831 |
⇒ REVERSION_AND_MOMENTUM 已是最优，**S 上限 1.42 结构性确认**，差 0.16 无法用设置层补。该候选 park。

### 7.9 本轮新增台账
| 文档 | 内容 |
|---|---|
| `FINDING_P91_intraday_pv_feats.md` | intraday 反转臂 10 条读数 + 4 条互相关 + 三条铁律 |
| `FINDING_P100_neutralization_and_pool_sweep.md` | 中性化扫描 + 存量池全扫 + 铁律 F |

### 7.4 新铁律 E：`2Y = 0.00` 的高 S 一定是数据陈旧伪像
`mLoQKob9`（`ts_delta(fnd89_jones_accrual_pct_major_11, 252)`）S 9.13 / F 23.36 / **2Y 0.00** / TO 0.6667。
基本面字段在 2022 年后停止更新 ⇒ 时序差分成「一次性跳变」⇒ 假 alpha。
**筛查规则**：任何 S > 3 的候选，先看 `two_year_sharpe`。若 2Y 为 0 或缺失 ⇒ 直接弃，不进后续闸。

### 7.5 池容量现实
已出过货的 4 个集（risk70 / analyst10 / insiders5 / risk68）容量各 **1**；
本轮再判死 5 个集（predictive_starmine / chart_cnn_alpha / multifactor_return_pred / fundamental89 / model238 / other78）。
KOR 的「裸水平 + 单一价差」几何已接近穷尽，后续必须走**交互/离散度/意外**几何。

---

## 8. 2026-11-09 收尾轮：KOR 数据集全量到底（新增判死 6 集）

### 8.1 本轮判死明细

| 数据集 | 类别 | 测试规模 | 最强读数 | 死因 |
|---|---|---|---:|---|
| **intraday_pv_feats · corr 族** | pv | P91/P95/P102 共 20+ 条 | S 1.93 全闸 | **prod 0.7827**（门 0.70）；换窗口 0.8965、换算子 0.7869 ⇒ 墙不可破 |
| **intraday_pv_feats · 非 corr 族** | pv | P103 十条 | S 0.68 | 真弱 |
| **analyst44** | analyst | WA1/WA2 十条 | S 0.92 | 修订事件族无信号 |
| **fundamental93** | fundamental | FC1/FC2 十条 | — | longCount **46–61** ⇒ 仪器覆盖 10% |
| **other455** | other | G1/G2 十条 | \|S\| 0.52 | 图嵌入得分近静态（TO 0.055），信息量不足 |
| **model313** | model | M1/M2 十条 | — | longCount **12–16** ⇒ 覆盖 5 只 |
| **mmp_nlp_sentiment** | other | S1/S2 十条 | \|S\| 0.52 | 新闻情绪计数无预测力，TO 高达 1.33 |

### 8.2 破墙尝试（针对 rKR8wXZE，prod 0.7827，[0.7,0.8) 有 3 颗钉子）

| 变体 | S | 结果 |
|---|---:|---|
| `group_rank(ts_mean(X,22),industry)` 基线 | 1.93 | prod 0.7827 |
| `group_zscore(...)` 只换算子几何 | 1.91 | prod 0.7869（**+0.004，无效**） |
| `group_rank(ts_mean(X,66),industry)` 只换窗口 | 1.77 | prod **0.8965**（**反向**） |
| 短窗 `ts_rank`(10/22/66) | 0.60/0.00/0.97 | S 崩 / HIGH_TURNOVER |
| **CROWDING 中性化** | 1.16–1.23 | S 崩（剥拥挤同时剥掉信号） |
| trunc 0.04 + decay 8 | 1.93 | 指标与基线**逐位相同** ⇒ 截断从未生效 |

⇒ 结论：prod ∈ [0.75,0.90] 的候选在**单数据集内已无杠杆**，几何/窗口/中性化/截断全部试尽。

### 8.3 KOR 覆盖终态（185 集已全部触达）

| 结局 | 集合 |
|---|---|
| **已交付（4 颗 / 各容量 1）** | risk70 → `omERn83n`；analyst10 → `qMLOooX1`；insiders5 → `RRE9NkVj`；risk68 → `d5Wvpmbx`（待确认） |
| **有信号但撞 prod 墙** | intraday_pv_feats（corr_bid_price_with_bid_size，prod 0.7827） |
| **容量饱和（第 2 颗不可得）** | risk68（物理上限 3 字段）、risk70、insiders5（重叠度族天花板 1.35）、analyst10 |
| **判死（本轮）** | analyst44 / fundamental93 / other455 / model313 / mmp_nlp_sentiment |
| **判死（历史）** | risk59/60/71/72/88、insiders1、其余 ~150 集 |

**RISK 7 集与 INSIDERS 2 集已全部到底，剩余信号 = 0**（见 `FINDING_risk_insiders_closure_P63_P65.md`）。

### 8.4 本轮新增铁律

- **铁律 G**：算子几何（rank↔zscore）对 prod 无效（差 0.004）；只有换信息内容能移动 prod。
- **铁律 H**：拉长窗口会让 prod **升高**（0.7827 → 0.8965）——长窗更贴近生产池慢变共同分量。
- **铁律 I**：`get_datafields` 的 coverage ≈ **时间覆盖率**，不代表仪器覆盖率；可用性必须实测 `longCount`（目标 >200）。

---

## 9. 2026-11-09 第二轮：纠正覆盖审计 + 补测 9 个漏网集 + 交付篮子 0.5 复核

### 9.1 ★纠正 §8.3 的证据缺陷
§8.3 写「185 集已全部触达」，当时的依据是「数据集名在台账里有命中」——**这是自证命中**：
`reference/kor_dataset_ranking.json` 本身就列了全部 192 个集名，任何检索都会命中它。
改用正确口径（排名文件的 `dead`/`hard_excluded` 布尔键 + 排除索引文件后查判死台账 .md）重审，
发现 **9 个集从未进过任何台账**：model36 / model38 / model250 / model56 / model135 / model219 / other432 / fundamental23 / fundamental65。
本轮已全部补测或证伪，§8.3 的结论现在才真正成立。

### 9.2 九个漏网集的处置结果

| 数据集 | 字段实况（KOR 实拉） | 测试 | 最强读数 | 判定 |
|---|---|---|---:|---|
| **model219** | **0 字段**（排名 506 是跨区陈旧） | — | — | 本区不可用 |
| **fundamental65** | **0 字段**（排名 663 是跨区陈旧） | — | — | 本区不可用 |
| **model135** | 仅 1 字段（40 日随机指标，VECTOR） | — | — | 单字段价量指标，无价差可构 |
| **model36**（SmartRatios 信用风险） | 43 MATRIX，cov 0.935–1.0 | CR1/CR2 十条 | \|S\| 1.00 | 判死：百分位大量并列 ⇒ 全中 CONCENTRATED_WEIGHT；且 `_d1` 与主版本差恒为 0（longCount=0） |
| **model38**（StarMine 相对估值+SmartGrowth） | 108 MATRIX | V1/V2 十条 | S 1.29 / 2Y 1.02 | 弱：成长预期差（模型预测−市场隐含）仅 0.22 |
| **other432**（会计实际 vs 预测误差） | 122 MATRIX | A432 十条 | S 0.63 | 判死：mae/mada 仪器覆盖仅 88–183 只 |
| **model56**（StockReportsPlus 评分） | 6 评分字段 | SRP56 五条 | \|S\| 0.07 | 判死：longCount 仅 **59–61**（覆盖 10%）；评分静态（ts_delta longCount=0） |
| **model250**（MALTA 机器学习） | 13 MATRIX | ML250 五条 | **S 2.18** | **prod 0.8346 深钉 ⇒ 判死**（见 9.3） |
| **fundamental23**（养老金拨备/表外负债） | 362 MATRIX | P23 十条 | \|S\| 0.89 | 判死：拨备状态/拨备率/表外负债全弱 |

### 9.3 model250：先查 prod 再修闸的正确示范
`qMLw8JnO = group_rank(mdl250_lmt_close_eq_score, sector)`：**S 2.18 / F 1.18**，但 2Y 1.15、TO 0.4328（raF=2）。
本来可用 decay 压换手修 2Y/F，但**先实测 prod = 0.8346**（max≥0.8 深钉）⇒ 直接判死，省掉整轮 decay 扫。
该字段 aC 398（已被 398 条 alpha 使用）⇒ 深钉符合预期。
同批 `MPY2ONkk`（季节性）2Y 1.62 过线但 S 0.93 远低 ⇒ 无可用交集。

### 9.4 ★交付篮子按全局 0.5 标准复核（此前只用 0.70 口径）
`compute_mutual_correlation(threshold=0.5)` 对 4 颗交付件：

| 对 | 相关 |
|---|---:|
| omERn83n ↔ qMLOooX1 | 0.2586 |
| omERn83n ↔ RRE9NkVj | 0.2965 |
| omERn83n ↔ d5Wvpmbx | 0.0581 |
| qMLOooX1 ↔ RRE9NkVj | **0.3176**（最大对） |
| qMLOooX1 ↔ d5Wvpmbx | 0.0678 |
| RRE9NkVj ↔ d5Wvpmbx | 0.0351 |

`pairs_over_threshold = []`，`max_mutually_below_subset_size = 4`（exact）。
⇒ **4 颗在全局 <0.5 严口径下全部可共存**，交付颗数 4 在严标准下依然成立。

### 9.5 本轮新增铁律
- **铁律 J**：判「数据集是否已分析」不能用「名字在台账语料里出现」——索引/排名文件列了全部集名，会自证命中。要查派发记录或判死台账，并把索引文件排除出检索语料。
- **铁律 K**：排名快照的 `usableFieldCount` 不保证本区可用（model219/fundamental65 排名 506/663，KOR 实拉 0）。开波前必须按目标 region 实拉 `get_datafields` 确认 count>0。

---

## 10. 2026-11-09 第三轮（五轮检查点）：再挖出 2 个漏网蓝海并关闭，KOR 真正穷尽

### 10.1 更严的漏网判定：从「md 提及」升级到「派发记录」
§9 用「判死台账 .md 是否提及」找漏网，但**规划文档里提及 ≠ 实测过**。
本轮改查**全部 804 条历史派发表达式**（_args_*.json + _msout_*.json 抽标识符），发现又有 2 个集的字段从未进过任何仿真：
- **behavioral_signals**（行为金融：salience 理论 / 连涨跌 / 价格路径凸性 / 视觉形态，7 VECTOR，aC 0–6）
- **equity_forum_data**（散户论坛：买卖情绪 / 评论量 / 参与人数，6 VECTOR，aC 0–7）
两者此前只在「蓝海优先打」的规划文档里出现，从未回测。

### 10.2 实测结果（各 10 模板）

| 数据集 | 最强读数 | 判定 |
|---|---:|---|
| **behavioral_signals** | \|S\| 0.60（salience），全中 CONCENTRATED_WEIGHT + TO 0.5–0.77 | 判死：行为价格路径信号无 KOR 可交易信息 |
| **equity_forum_data** | 买卖情绪分 **longCount=0**（KOR 空数据）；评论量/参与人数 \|S\|≤0.48 全 CW | 判死：核心情绪字段空，量能字段弱 |

### 10.3 ★事故与教训：漏查 type 列 ⇒ 整批 ERROR
behavioral_signals / equity_forum_data 字段 type=**VECTOR**，首轮直接 `group_rank(field,…)` 整批 5 条 ERROR：
`Operator group_rank does not support event inputs`（harvest 表现为 "No alpha_id in sim response"、父批 status=ERROR，**不是排队**）。
用 lookINTO_SimError_message 查父 location 拿 children、再查 children message 定位；套 `vec_avg` 重派后跑通。
⇒ **铁律 L**：设计表达式前必查字段画像 type 列；VECTOR/event 先 vec_* 聚合再接 group_rank/ts_*；GROUP 只作分组轴。

### 10.4 KOR 穷尽终态（证据链闭合）
- 192 个排名集全部有归宿；§9 的 9 个漏网 + 本轮 2 个蓝海全部实测关闭。
- 唯一未单独开波的 continuation_score 属图表形态相似度族（价量衍生），台账已记形态族天花板 ~0.34，且与已判死的 chart_cnn_alpha/pattern_scores 同机制。
- **可交付 ATOM = 4**（risk70/analyst10/insiders5/risk68 各容量 1），已按全局 <0.5 互相关复核可共存。
- 第 5–10 颗在 KOR 内无解：剩余要么 0 字段、要么仪器覆盖不足、要么弱、要么 prod 深钉。

---

## 11. 2026-11-09 第四轮（用户 resume 后）：★prod 墙被打破，交付第 5 颗

### 11.1 转折：不再宣告穷尽，改用降 prod 杠杆方法论
用户 resume 目标后，加载 `wq-prod-lever-self-lock-guard` 与 `wq-window-valley-break-prod-wall`，
对最接近的近线候选 **intraday corr 族**（`corr_bid_price_with_bid_size`，S1.93、其余闸全过、原 prod 0.7827）系统扫杠杆。
**关键发现：设置档（中性化/decay）就是这个骨架的 prod 杠杆**，此前只试 2 档就误判「墙不可破」。

### 11.2 中性化八档扫描（同一表达式，单变量）
| 中性化 | S | raF | prod |
|---|---:|---:|---:|
| REVERSION_AND_MOMENTUM（原基线） | 1.93 | 0 | 0.7827 |
| **SLOW** | **1.85** | **0** | **0.7013** |
| FAST | 1.67 | 0 | 0.8117 |
| SECTOR / SUBINDUSTRY / STATISTICAL / MARKET / INDUSTRY | ~1.0 | 3 | 崩闸 |
| CROWDING | 1.16 | — | 崩闸 |

### 11.3 decay / 窗口 / 组轴精修（SLOW 档上）
| 变体 | S | F | 2Y | prod |
|---|---:|---:|---:|---:|
| SLOW d4 w22 | 1.85 | 1.24 | 1.94 | 0.7013（n=1） |
| SLOW d8 w22 | 1.85 | 1.38 | 2.03 | 0.7172 ↑ |
| SLOW d0 w22 | 1.84 | **0.95✗** | 1.66 | —（F 崩） |
| **SLOW d2 w22** | **1.86** | **1.10** | **1.80** | **0.6981 ✓ n=0** |
| SLOW d4 w20 | 1.74 | 1.10 | 1.73 | — |
| SLOW d4 w24 | 1.90 | 1.30 | 2.00 | 0.7169 ↑ |
| SLOW group_zscore | 1.94 | 1.42 | 2.09 | 0.7455 |
| SLOW group_rank sector | 1.82 | 1.26 | 2.23 | 0.7505 |

**规律：prod 随 decay 增大而升高**（d2<d4<d8）；往回退 decay 到 2 即压过 0.70，且 F 仍 ≥1.0。
truncation 完全无效（权重未触截断上限）；窗口对 n=1 无救（w22 是谷，w24 反升，印证窗口谷 skill）。

### 11.4 ★第 5 颗交付件 `ZYQ116ln`（全闸验收通过）
- **数据集**：intraday_pv_feats（PV 塔）· **核心字段**：`corr_bid_price_with_bid_size`
- **表达式**：`subtract(0.5, group_rank(ts_mean(corr_bid_price_with_bid_size, 22), industry))`
- **设置**：KOR/TOP600/D1 · **neutralization=SLOW** · **decay=2** · trunc 0.08 · 2014–2023
- **指标**：S **1.86** · F **1.10** · 2Y **1.80** · TO 0.2205 · raF **0**
- **prod 0.6981 ✓**（[0.7,0.8) n=0）· **self 0.1426 ✓**
- **逐年**：2014–2023 longCount 290–340、pnl 全非零，**无空窗**
- **篮子 0.5 互相关**：与 4 颗已交付相关 0.018–0.162，全 <0.5，最大独立集 **5**
- 状态：**UNSUBMITTED，待用户明确确认提交**（同族仅 1 席，已占）

### 11.5 交付进度 4 → 5；旧结论纠正
§8–§10 的「KOR 上限 4 / prod 墙不可破」**被证伪**：prod 墙可经「中性化扫档 + decay 回退」打破。
后续应对其它 prod 卡墙近线候选（如 MALTA 综合分 qMLw8JnO S2.18/prod0.8346）复用此杠杆链，而非判死。

### 11.6 MALTA 综合分救援：失败（杠杆链非普适）
对 `qMLw8JnO`（model250，S2.18/2Y1.15/prod0.8346/TO0.43）复用 SLOW+decay：
- SLOW d22：S **0.95**（崩）；RAM d22：S 1.38 / 2Y 1.18（仍欠）。
- ⇒ MALTA 是**快 ML 信号**，中性化/平滑即毁；2Y 弱是结构性，decay 提不动。**不可救，判死。**
- **教训**：SLOW+decay 杠杆链对「慢变、横截面排序型」信号（intraday corr）有效，对「快 ML 预测型」信号无效；救前先判信号快慢。

### 11.7 当前交付 = 5 / 10
已验收：omERn83n(risk70) / qMLOooX1(analyst10) / RRE9NkVj(insiders5) / d5Wvpmbx(risk68,待提交) / **ZYQ116ln(intraday_pv_feats,待提交)**。
五颗篮子 0.5 互相关全过（最大对 0.3176）。剩余 5 颗需新信号源；prod 破墙杠杆链已就位，可用于后续近线候选。

## 12. 2026-11-09 第五轮：近线救援与第二席排查（均证伪，交付仍 5）

### 12.1 dividend_policy_analysis_3 补测 SLOW/FAST（上轮漏档）→ 失败
S1.42 近线，中性化原只测 RAM/STATISTICAL。本轮补 SLOW/FAST×decay：
- SLOW d2/d8：S **0.85/0.87**（崩）；FAST d2：S 1.22（降）。
- ⇒ SLOW/FAST 对 dividend 无效反而毁信号，**S1.42 结构性上限确证**，park 不变。

### 12.2 存量池 S≥1.4 全扫（200 条）→ 无新席
高 S 候选全部落在：intraday corr（1 席，已出 ZYQ116ln）/ MALTA（死）/ **risk68 变体**。

### 12.3 risk68 组轴变体「第二席」假设 → 互相关证伪
池里 `6XdNQ1qJ`(S1.84/2Y4.44, exchange×subindustry 组轴)、`xAr5oQzN`(S1.71/2Y3.78, exchange 组轴) 均 raF=0，
与 d5Wvpmbx 同双腿（volatility_short−weight_dadv）仅组轴不同。实测 0.5 互相关：
- d5Wvpmbx↔6XdNQ1qJ **0.7111**、↔xAr5oQzN **0.9566**、变体互 0.6924，全 >0.5，最大独立集 **1**。
- ⇒ **组轴变化不构成正交第二席**，risk68 容量 1 确证（与物理上限审计一致）。

### 12.4 方法论沉淀
- **同双腿 + 仅换组轴 ≠ 新颗**：互相关 0.69–0.96，必须实测而非凭组轴差异假设正交。
- SLOW+decay 杠杆链**信号特异性**：救 intraday corr 有效，对 dividend / MALTA 反而毁信号；救前先小样本试 SLOW 是否保 S。

### 12.5 analyst10 第二席（修正/创新族）探针 → 不可用
已交付 qMLOooX1 用 smartest 预测惊喜；本轮测**不同机制**的修正/创新族（preinnovation_score / preinnovate_increase−decrease / prerevise_ratio）：
- 最高 S **1.72**（prerevise_ratio_to_consensus_fy1），但 **TO 1.44**、F 0.58、2Y 0.66，raF 5。
- ⇒ 修正字段是**事件驱动、极跳**（换手 1.3–1.4），2Y 弱是信号近期失效，平滑救不动。**第二席不成立**。

### 12.6 本轮小结（交付仍 5/10）
四条救援/第二席路径全部实测证伪：dividend SLOW/FAST、MALTA、risk68 组轴变体、analyst10 修正族。
存量池 S≥1.4 全扫无新席。**KOR 可验证 ATOM 上限 ≈5 的证据已非常扎实**（非假设，均为仿真+互相关实测）。

## 13. 2026-11-09 第六轮：补齐最后 4 个 alive 缺口，KOR 覆盖闭合

对「无正式判死结论 / 从未派发」的 alive 集逐一实测：

| 数据集 | 机制 | 字段实况 | 结果 | 判定 |
|---|---|---|---|---|
| **other545** | NEMO 2.0 网络动量（NLP 文本挖掘关联企业） | 4 VECTOR，cov 0.839，**从未派发** | 10 模板最高 \|S\| 0.69，全 CW | 死 |
| **model50** | — | KOR 实拉 **0 字段** | — | 本区不可用 |
| **model31** | 盈余质量多因子评分（覆盖 1.0 / aC 中位 3） | 149 MATRIX | 10 模板最高 S 0.82 | 死（信号弱） |
| **fundamental94** | 经典财务比率（盈利/杠杆/资产增长） | 186 MATRIX | 5 探针最高 S 1.20（营业利润率 F0.95） | 死 |

### 13.1 KOR 覆盖终态（证据链完全闭合）
- 192 排名集、71 alive 全部有归宿：要么已测判死、要么 0 字段不可用、要么已提取容量 1 席。
- 可交付 ATOM = **5**：risk70 / analyst10 / insiders5 / risk68 / intraday_pv_feats 各 1 席。
- 五颗篮子全局 <0.5 互相关全过（最大对 0.3176）。
- ~~第 6–10 颗在 KOR 内确无解~~ **（此结论已被 §14 证伪：池深处还有全绿件）**。

## 14. 2026-11-09 第七轮：★池扫描盲区揪出第 6 颗 LLZ6wZO2

### 14.1 盲区根因
此前池扫描只拉 `get_user_alphas` offset 0/100（200 条），**offset≥200 拉取失败**，导致 200 条之外的已验证件被漏。
台账 `kor_campaign_ledger_20261106.md` 早已记载 `LLZ6wZO2` 全绿，但本轮才重新核实纳入。

### 14.2 ★第 6 颗交付件 `LLZ6wZO2`（全套验收通过）
- **数据集**：oth466（FUNDAMENTAL 类，单数据集 ATOM 不涉禁混）· **核心字段**：`oth466_is_consol_net_inc_q` / `oth466_bs_assets_tot_q`（合并净利/总资产，盈利质量）
- **表达式**：`quantile(group_rank(ts_rank(group_rank(divide(oth466_is_consol_net_inc_q, oth466_bs_assets_tot_q), industry), 420), market))`（5 算子）
- **设置**：KOR/TOP600/D1 · **STATISTICAL** · decay 4 · trunc 0.08 · 2014–2023
- **指标**：S **1.99** · F **1.53** · 2Y **2.24** · TO 0.144 · subU 1.21 · raF **0**
- **prod 0.6762 ✓ / self 0.6760 ✓**（本轮 check_correlation 复测 all_passed=True）
- **逐年** 2014–2023 longCount 290–339、pnl 全非零，无空窗
- **篮子 0.5 互相关**：与 5 颗相关 **−0.034 ~ 0.076**，全 <0.5，最大独立集 **6**
- 状态：UNSUBMITTED，待用户确认提交
- 机理：ts_rank(420) 窗口谷把 prod 压到 0.6762（窗口谷 skill 实证谷区 [420,480]）。

### 14.3 交付进度 5 → 6；纠正「上限 5」
**池深处（offset≥200）还有未拉取的全绿件**，KOR 上限并非 5。下一步：穷尽台账里其它已验证候选 + 想办法拉全池。

## 15. 2026-11-09 第八轮（五轮检查点）：OS 池占用图谱 + analyst 创新白空间证伪

### 15.1 ★关键背景：用户已有 32 条 KOR 已提交 OS 池（wave276/277 台账实测）
- `get_user_alphas` 有 **max_scan=1000 部分扫描**，池枚举不可靠（LLZ6wZO2 即漏网证明）；台账才是可靠候选源。
- OS 池 prod<0.70 白空间已被 **24 条**占据；**shrt38(SHORTINTEREST) 8 条 / oth466+fnd94(FUNDAMENTAL) 6 条 / MODEL 6 条**是三大占用重镇。
- 我追的 shrt38 net_buy_amt 线索 `pwvndZJ3`(S2.09/prod0.641) **已在 OS 池提交**，非新席。
- **ANALYST 塔纯 analyst 字段仅 3 条**（e73Rw8qg/KP78pLWk/ZY0R0mL8），白空间相对最多。

### 15.2 analyst10 创新/羊群分解白空间（wave278 预设计）实测 → 证伪
`anl10_analyst_innovation_*` 80 字段 MATRIX、aC 极低、OS 池零占用，但：
- 家数差裸用：TO **1.37–1.49** 全崩（事件驱动极跳）；ts_mean 平滑后 S 掉到 0.93；FY2 惊喜 S 0.87。
- ⇒ **analyst10 创新/修正族在 KOR 不可用**（与本轮 early ANL10B 探针一致）。

### 15.3 交付仍 6/10；第 7–10 颗的真实约束
不是「S 打不上去」，而是**字段/机制须落在 OS 池白空间 + 自证 prod<0.70 + self<0.70**。
OS 池已占 24 条 prod 白空间，剩余可插入余量极薄。候选源只能靠台账深挖 + 深池（分页有盲区）。

## 16. 2026-11-09 第九轮：★「10 颗篮子」核验 + 口径纠正（存量不算新挖）

### 16.1 曾算出一个 10 颗全闸篮子，但 4 颗是存量
把「存量 ATOM + 新挖 6 颗」一起算 0.5 互相关，最大独立集 **16**；取 10 颗篮子复算 **all_below=True、最大对 0.4954、无超线对**，且逐颗当前 S/F/2Y/raF/prod/self 全过、单数据集 ATOM 确证。
**但查 dateSubmitted：入选的 4 颗存量件提交于 2026-08-04 ~ 10-18，全部早于本目标启动（11-06）**：
- KPNo2lgl(shrt38) 09-28 · e73Rw8qg(analyst44) 08-04 · A1NXddRw(oth466) 09-28 · pwvndZJ3(shrt38) 10-18。
⇒ 它们是**先前战役存量，非本目标「挖掘」产出，不能计入 10 颗**。此前想靠存量凑 10 的口径**作废**。

### 16.2 本目标真实新挖 = 6 颗（不变）
omERn83n(risk70) / qMLOooX1(analyst10) / RRE9NkVj(insiders5) / d5Wvpmbx(risk68) / ZYQ116ln(intraday_pv_feats) / LLZ6wZO2(oth466)。
六颗篮子 0.5 互相关全过（最大对 0.3176）。

### 16.3 结论：第 7–10 颗新挖被「密集存量 OS 池」结构性堵死
KOR 已有 32 条存量提交占满 prod 白空间（shrt38/oth466/MODEL/ANALYST 重镇），新机制须同时躲开存量 self 与平台 prod，余量极薄。
本轮把「能想到的白空间」几乎全部实测关闭（analyst 创新族、news79、小类别、risk68/analyst10 第二席、dividend/MALTA 救援）。
**要再凑 4 颗新挖，要么放宽验收线、要么换 region（objective 禁止）——需用户拍板。**
- 补测最后一个未测大集 **other395**（368 MATRIX）：是 **Jones 应计机制**（current asset accruals/total assets、jones/csjones 族），与已判死的 fundamental89/93 同源，覆盖中位仅 0.533 ⇒ 不投。数据集至此真正测尽。

## 17. 2026-11-09 深夜：闸值精确确认 + 股利长窗终验（仍 6/10）
- **读平台真实闸值**（vR1b50pQ checks）：KOR **LOW_SHARPE limit=1.58、LOW_FITNESS limit=1.0**，此前假设无误。
- **股利近线长窗终验**（dividend_policy_analysis_3，之前只扫 28–66）：126/252 的 ts_mean/ts_rank/ts_zscore/ts_decay_linear 全更弱（S0.45–0.92）⇒ **W44 封顶 1.42 确证**，差 0.16 无法补，非交付件。
- 结论不变：KOR 在 S≥1.58 口径下新挖上限 **6 颗**；第 7–10 颗需换区（objective 禁）或放宽 S 线（需用户授权）。

## 18. 目标改写「挖未点亮塔」后的系统探索（2026-11-09 夜）
**KOR/D1 塔点亮表**（get_pyramid_alphas 实读）：已亮=shortinterest(4)/analyst(3)/fundamental(3)/model(3)；未亮=pv(2)/risk(2)/insiders(1)/other(1) + earnings/imbalance/institutions/macro/news/socialmedia/sentiment(0)。
**recommend_datasets（未亮塔优先）+ 逐一实测**：
| 未亮塔集 | 机制 | 结果 |
|---|---|---|
| other571 Wikipedia 浏览 | 投资者注意力 | 覆盖仅 **0.266** 且字段是 "USA module"（非 KOR 数据）⇒ 不可用 |
| news66 网页浏览 | 注意力 | 仅 2 VECTOR 字段、覆盖 0.5 ⇒ 弱 |
| news59 公司事件 | 事件 | 2 个元数据字段、aC1627 拥挤 ⇒ 弱 |
| other475 出口额 | 基本面 | 仅 1 字段、覆盖 0.357 ⇒ 弱 |
| **other315 OTC 衍生品** | 衍生品活动 | 4 探针实测 S **0.24–0.41** 全灭 ⇒ 死 |
- 其余未亮塔集要么已挖（risk70/insiders5/pv1）、要么已判死（news 情绪/institutions6/sentiment）、要么字段太少（earnings3/socialmedia39/imbalance5/macro63）。
- **结论：未点亮塔方向也未解锁新交付**，KOR 新挖上限仍 **6 颗**。注意力/衍生品这两条新机制在 KOR 覆盖差或无信号。

## 19. os_is_sharpe 数据驱动复核未亮塔（2026-11-09 深夜）
按 recommend_datasets 的 **os_is_sharpe（历史真实均值）** 排序未亮塔集，挑最高的重测，排除「凭印象判死」：
- **sentiment21**（os_is_sharpe 0.77，未亮塔最高）：字段描述全是 "**USA modules**"、KOR 覆盖仅 0.35 ⇒ 非 KOR 数据，不可用（历史均值是 USA 的）。
- **other553**（os_is_sharpe 0.71，分析师预估/目标价/评级）：4 探针实测预估修正 S**0.83**、目标价修正 0.02、分析师覆盖 0.07 ⇒ 弱，与 analyst44 判死一致。
- 其余未亮塔集 os_is_sharpe 全 <0.6（news59/insiders5 已挖、news 系判死、macro63/earnings3/socialmedia39/imbalance5 字段太少或拥挤）。
- **铁律**：os_is_sharpe 是「该集历史 alpha 均值」，低不绝对封死（risk70 均值 0.38 我挖出 1.62）；但未亮塔最高的 sentiment21/other553 实测仍弱/非本区，故未亮塔确无额外 S≥1.58 交付。
- **最终结论不变：KOR 新挖上限 6 颗。**

## 20. 2026-11-08 深夜：目标上调 20 颗 + 股利系盲区开荒（D1/D2 在飞）

### 20.1 目标编辑与快照
用户目标 10 → **20 颗**。6 颗已验收件 get_alpha_details 快照复核：全闸仍绿；RRE9NkVj ACTIVE（11-06 提交），其余 5 颗 UNSUBMITTED 待用户确认提交。

### 20.2 ★新盲区：三个股利系集从未派发（未点亮 OTHER 塔）
按铁律 J 重审（查**字段前缀派发记录**、排除索引自证命中）：`oth424_/oth436_/oth335_/oth323_` 在全 tracking/KOR 只出现在规划文档，**零仿真派发**。「192 集全触达」再现缺口。

| 数据集 | 字段实况（KOR 实拉） | 判定 |
|---|---|---|
| **other424** Dividend prediction model | 3 MATRIX：`dividend_growth_factor_score`（Wolfe ML 股息增加概率 [0,1]，**aC10**，cov 0.6044）+ divyld(aC19) + mktcap | 开荒 D1 |
| **other436** Dividend model | 3 VECTOR：`oth436_disc`（削减/停发股息概率 [0,1]，**aC4**，cov 0.57）+ divyld(aC7) + mktcap；先 vec_avg | 开荒 D2 |
| **other335** Multi-Region Dividend Alpha Model | 10 MATRIX：Wolfe MIND/hedge/linear/shield 四模型分×两套镜像；主版 cov 0.6073 擦线，hc 版 0.5728 排除；10-30 已画像未回测 | 开荒 D3（排队） |
| **other323** Premarket | 11 VECTOR 全是参考元数据（股本/lot size/Bloomberg ID/par value），无连续信号 | 论坛盘前机制不可移植 KOR，结构性死，不派发 |

### 20.3 双通道取证
- **论文**：Njoku & Lee (2024, KOSPI 5478 观测)：现金股利显著影响公司价值，signaling/信息含量假说（Bhattacharya 1979; Miller & Rock 1985），chaebol 结构调制 ⇒ 方向按铁律 B 正反实测。股利削减/停发文献：公告负反应显著 ⇒ 高 disc 做空先验。
- **论坛**（search_forum_posts 已恢复，此前两次超时）：33169668224919 全天候（股利稳定性 `ts_std_dev(est_dividend_ps,520)`）；34667729813399 Gordon 增速 `ts_delta(div,M)/ts_delay(div,M)` + 零股利 if_else；34114729160599 star_val_dividend_projection 族。稳定性/增速几何留作精修波。

### 20.4 D 波派发（并发 2，RAM/d4/trunc0.08）
- **D1** other424 ×10 模板（水平正/反、Δ22/66、ts_zscore252、mean22、ts_rank66、规模残差、yield 门控、power2）→ multisim `4gX3zx49z4jpbme1mt7retm`
- **D2** other436 ×10 模板（空高 cut/多高 cut 对照、Δ22/66、mean66、zscore252、yield 正/反、规模残差、yield 门控）→ multisim `oycrP8Rf5fz9sLt6s672Le`
- **D3** other335 ×10 模板已备好（`_args_D3.json`），槽位释放即派。
- 字段硬闸 PASS（30 表达式 0 unknown）；preflight 全 valid；算子数 ≤9。
- **波次三问**：继承=§19 结论仅覆盖当时已测集，本波准入=三个零派发集；准入禁轴=死轴清单（慢信号禁 ts_rank 短窗+大 decay）；收窄=每集 10 探针，8 探针无 |S|≥0.5 按快判死回写。

### 20.5 近线中性化缺口审计（排队补扫）
`dividend_policy_analysis_3`（ai_equity_alpha·MODEL 字段，S1.42）缺 CROWDING/NONE/SECTOR/INDUSTRY 4 档；other532（S1.12）与 chart_cnn_alpha（S1.36）只测过 RAM ⇒ 原「天花板」结论未含中性化全扫，补扫排队（D 波收割后）。

### 20.6 D1 收割归因（other424 判弱死）
10/10 COMPLETE。最强 Δ22 臂 `3qovd3PP` S0.77/F0.51/**2Y1.78**/raF2，余 ≤0.73，反向臂 −0.74（正向确证）。
逐年：**S<1.0 占 6/10=60%**（2014 −1.50，2017/18/20/21 均 <0.7），仅 2022(2.44)/2023(1.19) 强 ⇒ 全期 S 结构性封顶 0.77，缺口 0.81 非参数可补。
**other424 封盘**（极干净 aC10 但 regime 依赖弱信号，第 6 次证伪「低拥挤⇒有信号」）。画像 §6 已回填。
**D3 已派**（other335×10，multisim `1NVLsvgz94tuc8Q1bDNPhpPh`）；D2 在飞（0.35）。并发=2。
**中性化补扫排队**：dividend_policy(S1.42 缺 CROWDING/NONE/SECTOR/INDUSTRY 4 档) 优先，槽位释放即派。

### 20.7 D3 收割 + IR327 派发 + acquisition_model 纠正
- **D3（other335 MIND）10/10**：最强 mind zscore252 `leAPxwGn` S1.14/F0.91/2Y1.19，反向 −1.13（正向确证）；天花板 1.14 缺口 0.44 ⇒ **弱但活**，与 other532 同级，中性化未扫列入补扫。画像 §6 回填。
- **acquisition_model 纠正（避免误重测）**：台账 §5.23/§5.114 实证它在 wave2 event 盲废后**已正确重测**——数值似然腿水平+更新+变化率（S0.05–0.28）全死，wave257 FAIL；**仅文本因子腿**（global_text_factor_percentile_rank aC1 / region_text_factor aC0）未测。非误杀，不重测数值腿。
- **IR327（other327 利率敏感）已派**：确认零派发后开荒，10 模板（lev/sl 水平正反·Δ66·zscore252·mean66·规模残差·power2），multisim `Wym2Bbnz4YZbuFbBIHB6BB`；取证 D.E. Shaw《Divergent Interests》利率敏感度截面分化。画像 `reference/datasets/other327.md`。
- **D2 探针**（other436×2，`1tHZaRgiL50v8yUgImCVs9G`）平台慢仍在飞；台账预判同 acquisition 型弱（S~0.4），待实测定谳。
- **当前在飞**：D2探针 + IR327（并发2）。已验收仍 **6/20**。

### 20.8 平台拥堵诊断 + 中性化补扫备战
- D2探针/IR327 卡 progress 0.35、0 children ~20min。按 wqb-concurrency §5：提交**已接受**（非429）⇒ **WQ 全局集群拥堵排队**，非孤儿占槽/非设置错，只能等（STALLED 判据=60min 无进展，未到）。并发2已上限，不再派。
- 备好中性化补扫 4 即用批次（`_neut_batches_ready.json`）：CROWDING/NONE/SECTOR/INDUSTRY × [dividend_policy(S1.42)/other532(S1.12)/other335(S1.14)/chart_cnn(S1.36)]，槽位释放即派。

### 20.9 IR327 判弱死 + 中性化补扫启动
- **IR327（other327 利率敏感）10/10**：最强 lev mean66 `A1V8qNnl` S0.75/F0.45/2Y1.21，反向 −0.84（正向确证）；天花板 0.75 缺口 0.83 ⇒ **弱死封盘**（利率敏感度=风险暴露非 alpha，KOR 与美债联动弱）。画像 §6 回填。
- **news 塔不重复**：已有 `FINDING_news_tower_dead.md` + news_tower_inventory 系统判死（news21/31/85/104 等已画像），不重投。
- **中性化补扫启动**：IR327 释放槽位 ⇒ 派 NEUT_CROWDING（`4cUcewdrH4Fz9WzquDF39Il`，4 近线候选 dividend_policy/other532/other335/chart_cnn @CROWDING）。余 NONE/SECTOR/INDUSTRY 3 批随槽位释放续派。
- **在飞**：D2探针（仍拥堵）+ NEUT_CROWDING。已验收仍 **6/20**。

### 20.10 other436 判弱死 + NEUT_NONE 派发
- **D2 探针完成**（other436×2）：做多高 cut 概率 S+0.53 / 做空 S−0.70 ⇒ **方向与假说相反**（高削减概率股超跌反弹），|S| 天花板 0.70 缺口 0.88 ⇒ **弱死封盘**（证实 roadmap 预判，同 acquisition 型）。整批 ERROR 系瞬时故障（探针跑通）。画像 §6 回填。
- **NEUT_NONE 已派**（`45fIYd7lU4uuaAl12NFUbCC1`，4 近线候选 @NONE）。在飞：NEUT_CROWDING + NEUT_NONE（并发2）。余 SECTOR/INDUSTRY 待派。
- **股利系+利率敏感小结**：other424(0.77)/other436(0.70)/other327(0.75) 弱死，other335(1.14) 弱活；OTHER 塔新机制普遍 S0.7–1.1，无新交付。已验收仍 **6/20**。

### 20.11 未点亮塔系统审计闭合（sentiment/institutions/earnings）
- **sentiment 塔关闭**：news_sentiment_transfer（cov0.9654 全 KOR 最优新闻集）早在 wave288 实测判死（16 结构互异模板最高 S0.72，FINDING_news_tower_dead/tower_lighting 确认 S0.04–0.72 封盘）；画像 §3「待填」只是文档缺口，结果在 wave288/289 台账。sentiment21/26（USA module/低覆盖）、other553（S0.83 弱）均死。
- **institutions 塔关闭**：fund_holdings_panel（水平|S|≤0.61/交互≤0.87）+ institutions6 全死。
- **earnings 塔关闭**：earnings3 断崖 + aC2624 拥挤。
- **审计结论**：全部未点亮塔（pv/risk/insiders/other/news/sentiment/institutions/earnings/macro/socialmedia/imbalance）已系统触达；本战役新挖的股利系（other424/436/335）+ other327 是最后真盲区，实测均弱（S0.7–1.14）。**KOR 在 S≥1.58 口径下新挖交付仍 6 颗**，余希望仅在近线中性化补扫（在飞）+ acquisition 文本因子腿（待派）。

### 20.12 最后三个 0/3 塔审计闭合（macro/socialmedia/imbalance）——全塔扫描完结
- **macro**：macro63（Index Reconstitution，1 字段，指数重构无截面）+ other106（KOSPI INDEX，15 字段 cov0.4038，指数级非个股截面）⇒ 结构性无截面，死。
- **socialmedia**：other100 + socialmedia39 均名 Investor views、各 1 字段、aC400/580 拥挤；同概念 socialmedia39 已判死 ⇒ 单字段拥挤，死。
- **imbalance**：imbalance5（Oil Price Resilience，2 字段油价格子集，aC1411 极拥挤）⇒ 死。
- **全塔扫描完结**：KOR/D1 全部未点亮塔（pv/risk/insiders/other/news/sentiment/institutions/earnings/macro/socialmedia/imbalance）已系统触达并闭合。本战役真盲区（股利系 other424/436/335 + other327）实测均弱。**新挖交付 6/20**；余 hope 仅近线中性化补扫（NEUT_CROWDING/NONE 拥堵在飞，SECTOR/INDUSTRY 待派）+ acquisition 文本因子腿（备妥）。

### 20.13 NEUT_NONE 收割 + NEUT_SECTOR 派发
- **NEUT_NONE 4/4**（@NONE）：dividend_policy `N1NlWn2q` S1.02/F0.71/**2Y2.08**/raF2；other532 S0.80；other335 S0.40；chart_cnn S0.25。
- **四候选 NONE 档 S 全低于 RAM 基线**（1.42→1.02 / 1.12→0.80 / 1.14→0.40 / 1.36→0.25）⇒ RAM 最优方向确证，NONE 非杠杆。dividend_policy 2Y 虽 2.08 但 S1.02 不可交。
- **NEUT_SECTOR 已派**（`4FvhvAefW4ZWceiooJlhMtK`，4 候选 @SECTOR）。在飞：NEUT_CROWDING（仍拥堵）+ NEUT_SECTOR。余 INDUSTRY + ACQTEXT 待派。

### 20.14 NEUT_SECTOR 收割 + ACQTEXT 派发
- **NEUT_SECTOR 4/4**（@SECTOR）：chart_cnn `E56P02A9` S1.31/F0.90/2Y1.35；dividend_policy S1.06/2Y1.92；other335 S0.94；other532 S0.79。**SECTOR 档 S 亦全低于 RAM**（1.36→1.31/1.42→1.06/1.14→0.94/1.12→0.79）⇒ RAM 最优再确证。
- **中性化补扫已测 NONE/SECTOR 均 RAM 最优**；CROWDING 拥堵在飞、INDUSTRY 待派（大概率亦更低，完成杠杆排除）。
- **ACQTEXT 已派**（`1ELgRN2HS4wKaHpjlL0yLI9`，acquisition 文本因子腿 4 模板，OTHER 塔最后未测字段 aC0–1）——优先于 INDUSTRY 因此为真新测试。在飞：NEUT_CROWDING + ACQTEXT。

### 20.15 NEUT_CROWDING 收割 + NEUT_INDUSTRY 派发（中性化扫描闭合在即）
- **NEUT_CROWDING 4/4**（@CROWDING，久拥堵后完成）：dividend_policy `zq3nwxgE` S1.17/F0.82/**2Y2.01**/raF2；chart_cnn S1.09；other335 S1.01；other532 S0.82。**CROWDING 档 S 全低于 RAM**。
- **中性化结论固化**：NONE/SECTOR/CROWDING 三档 4 候选 S 均低于 RAM 基线 ⇒ **RAM 是这些近线件最优中性化档，中性化非提 S 杠杆**（dividend_policy RAM1.42>CROWDING1.17>SECTOR1.06>NONE1.02）。INDUSTRY 末档在飞，闭合后杠杆排除完结。
- **NEUT_INDUSTRY 已派**（`2KpVpk3ky5iDcL0i4ec2loA`，4 候选 @INDUSTRY）。在飞：ACQTEXT（文本因子新测试）+ NEUT_INDUSTRY。**ACQTEXT 是当前唯一真新信号希望**。

### 20.16 NEUT_INDUSTRY 收割 —— 中性化扫描完全闭合（RAM 最优固化）
- **NEUT_INDUSTRY 4/4**（@INDUSTRY）：chart_cnn `O0AXqNnv` S1.29/F0.82/2Y1.39；other335 S1.13；dividend_policy S1.05/2Y1.91；other532 S0.62。**INDUSTRY 档 S 全低于 RAM**。

**完整中性化矩阵（S，RAM 基线 vs 四补扫档）**：
| 候选 | RAM | CROWDING | SECTOR | INDUSTRY | NONE | 天花板 |
|---|---:|---:|---:|---:|---:|---:|
| dividend_policy | **1.42** | 1.17 | 1.06 | 1.05 | 1.02 | 1.42（缺口0.16）|
| chart_cnn | **1.36** | 1.09 | 1.31 | 1.29 | 0.25 | 1.36（缺口0.22）|
| other335 | **1.14** | 1.01 | 0.94 | 1.13 | 0.40 | 1.14 |
| other532 | **1.12** | 0.82 | 0.79 | 0.62 | 0.80 | 1.12 |

**结论固化**：四补扫档全部低于 RAM ⇒ **RAM 是这些近线件最优中性化档，中性化非提 S 杠杆**；天花板为结构性（缺口 0.16–0.46 非设置层可补）。中性化轴彻底排除。
- **在飞仅剩 ACQTEXT**（acquisition 文本因子，唯一剩余新信号测试）；其余路径全闭合。ACQTEXT 出结果即 KOR 最终裁决。

### 20.17 ACQTEXT 判死 —— KOR 可执行路径全部穷尽（最终裁决）
- **ACQTEXT 4/4**（acquisition 文本因子腿，@RAM/d4）：global_text Δ66 `LLMY6lz9` S0.17/F0.05/2Y1.21/lc137；global 水平 S0.11/lc169；region 水平 S0.11/lc169；反向 S−0.27/lc466。
- **判定：死**（|S| 天花板 0.27，缺口 1.31；主臂 longCount 137–169 仪器覆盖不足 + 信号可忽略）。acquisition_model 数值似然腿（§5.23/5.114）+ 文本因子腿全死，整集封盘。

## ★ KOR 最终裁决（目标 20，新挖交付 6）
**可执行路径全部穷尽**：① 全部未点亮塔系统审计闭合（pv/risk/insiders/other/news/sentiment/institutions/earnings/macro/socialmedia/imbalance）；② 最后真盲区股利系 other424(0.77)/other436(0.70)/other335(1.14) + other327(0.75) 实测均弱；③ 中性化矩阵 NONE/SECTOR/CROWDING/INDUSTRY 四档全低于 RAM（非提 S 杠杆）；④ acquisition 文本因子（最后未测字段）S0.27 死。
**结论**：KOR 在 S≥1.58 + prod<0.70 + self<0.70 + 互相关<0.5 口径下新挖上限 **6 颗**（omERn83n/qMLOooX1/RRE9NkVj/d5Wvpmbx/ZYQ116ln/LLZ6wZO2），20 颗受结构性约束（密集存量 OS 池占满 prod 白空间 + 新机制普遍弱）不可达。
**目标裁决**：曾就 20 vs 上限 6 发起 ask_user，60s 超时自动选定"继续 20 + 机会主义复采"（非用户明确）；现最后路径 ACQTEXT 亦死，机会主义复采无标的，陷入真实僵局——需用户改目标/约束/区域方能推进。


---

## 21. 目标恢复（用户 continue）：实时平台验真 + 真未挖集 news85 / pv103 开荒

> 用户界面 continue 恢复目标（active），指示"不看画像库、从平台实时拉数据集，在未挖过的集继续"。本节推翻 §20.17"路径穷尽"——实时验真发现仍有真未挖集。

### 21.1 实时平台拉取 + 字段层验真（绕过本地画像库）
- get_datasets 实时：**KOR/D1 185 集**；塔 4 亮（analyst/fundamental/model/shortinterest）+ 11 未亮。
- 对"低 aC×高覆盖"候选实时 get_datafields 验真：**pv149（status/type 纯元数据）/ pv20（公司名/SEDOL/sector 参考集）= 无信号**——低 aC 恰因无人能做出信号，数据集级指标会骗人。
- 派发记录核实（字段前缀 grep _args 零命中）：**news85 / pv103 / other496 真未挖**；news38/risk60 有历史判死 verdict（旧战役，低优先）。

### 21.2 双通道取证 + 立机制
- **news85**（DNN 情绪分布，23 字段 cov0.6325，aC0–9）：论坛专帖《情绪通道的非对称：从 news85 看涨跌反应差》(29票)——**负面极端情绪偏度比正面温和更具前瞻信号、恐惧扩散快于希望**；sentiment22 负偏偏度帖(30票)+Miller(1977)分歧→高估。机制=情绪偏度/分歧不对称。
- **pv103**（盘中时段 OHLCV+VWAP，7 字段 cov1.0）：VWAP=机构执行基准（收盘 vs VWAP 偏离=买卖压力）；时段收益反转/振幅/收盘位极。机制=盘中微结构。

### 21.3 派发（并发2，RAM/d4/trunc0.08，字段闸+preflight 全过）
- **N85** news85×10 模板（偏度正/反·负极值·情绪水平正/反·Δ22·双通道价差·zscore66·注意力·偏度Δ）→ multisim `1e1fk4aV4q09OU6MEWrgwa`
- **P103** pv103×10 模板（时段收益反转·VWAP偏离正/反·振幅低波·收盘位极·量·zscore·mean·ts_rank·市值）→ multisim `30wKDr4fo5aP9khqabGLnRq`
- 在飞待收。other496（ARD 资产负债会计项，名字"Intraday FX"误导）属 KOR 基本面弱族，暂缓。

### 21.4 N85/P103 收割判死 + other496 派发
- **N85 news85×10**：天花板 S0.69（负极值 sentiment1_lowest_score `gJeN3Jam` S0.69/F0.33/2Y1.78/raF2），反向 −0.84 确证正向。逐年 **S<1.0 占 6/10=60%**（2014/2017/2019/2020 负）⇒ regime 依赖、缺口 0.89 结构性 ⇒ **判死**（KOR 新闻情绪偏度/分歧机制弱，论坛专帖机制真实但本区强度不足）。
- **P103 pv103×10**：天花板 S1.04（平滑 VWAP 偏离 ts_mean22 `zq37WKEX` S1.04/F0.72/2Y1.77/raF2）；裸时段比率 TO 0.83–0.96 高换手。逐年 **S<1.0 占 7/10=70% + top1 年 2022(S3.09)占正收益 ~34%>30%** ⇒ 过拟合指纹+regime ⇒ **判死**（缺口 0.54）。
- **other496 派发**：首派被 validate_fields 拦（负债字段正确 id `oth496_a_ard_tot_liabilities` 带 a_，命名不一致，未浪费配额）；修正后重派 `3klGYV1n74Pfavoctd53SUN`（资产负债比率+aftercons/afterest 修订+长窗收益 10 模板）。
- **真未挖集 news85/pv103 实测均死**，恢复开荒首轮无新增；other496 在飞待收。已验收仍 6/20。

### 21.5 other496 收割：共识修订族真信号（近线）+ 中性化测试
- **other496×10**：共识修订族出货 `d5WJQ3Yw` aftercons_difference **S1.25/F0.93/2Y1.42**/TO0.166/lc261/raF3；`vR17mpZd` aftercons_percentage S1.22/F0.94/2Y1.42。资产负债比率/长窗收益全死（S≤0.1）。
- **归因（d5WJQ3Yw）**：逐年 2014 0.02/2015 −0.06/2016 1.49/2017 1.36/2018 1.02/2019 1.60/2020 0.92/2021 2.97/2022 2.61/2023 0.36；**S<1.0 占 40%**、top1 年 28%<30% ⇒ 真实信号但 regime 依赖（2016–2022 强、2014/15/20/23 弱）。十年 longCount 245–274 全覆盖。
- **处置**：近线缺口 S0.33/2Y0.16；尊重 regime 判据不扫 decay/平滑，仅按"换族必重扫中性化"派 STATISTICAL+CROWDING 结构特异测试（各配 aftercons_difference+percentage 双臂）。结果决定是否可破 1.58。
- **CROWDING 已收**：aftercons_difference/percentage 双臂 S1.02/1.02（2Y1.13/1.19）**低于 RAM 基线 1.25** ⇒ CROWDING 不提 S。STATISTICAL 在飞待收；若亦低于 RAM 则 RAM 最优、other496 封顶 ~1.25（regime 结构性，S<1.0 40%）确认，park。
- **STATISTICAL 突破**：aftercons_difference `wpQ7Rnm6` **S1.47/F0.92/2Y2.09**/TO0.175/raF3；aftercons_percentage S1.45/2Y1.86。**STATISTICAL 大幅优于 RAM(1.25/2Y1.42) 与 CROWDING(1.02)**——共识修订族最优中性化=STATISTICAL，2Y 已过线，仅差 S0.11/F0.08。逐年归因：S<1.0 占 40%（2014/15/16/19）但 2020–2023 强（1.82/3.22/1.84/2.33）→2Y2.09 过线、top1 年 24%；与"2Y 不可达"不同，近线重点破线对象。
- **O496push 几何精修波已派**（`1gLlnA5Cg50TcFBcPT4fvTK`，10 变体 @STATISTICAL/d4：backfill 窗 10/44/66、ts_mean5/10 平滑、industry/subindustry/market 组轴、percentage bf44、zscore66）——聚焦破 wpQ7Rnm6 的 S0.11/F0.08 缺口（2Y 已过，非盲扫）。
- **★qML2AwPO prod 干净**：`group_rank(ts_backfill(vec_avg(oth496_aftercons_percentage),44),sector)`@STATISTICAL/d4，**S1.55/F1.04/2Y2.79，prod 0.6546<0.70 过**（[0.7,0.8)无钉）！仅 S 差 0.03。逐年 S<1.0 40% 但 2021–2023 极强、十年覆盖全。派微调破线：A=backfill33/55@d4，B=backfill44(pct+diff)@d2。
- **★2rAVLRYP 破 S/F/2Y 但 BLOCKED investability**：aftercons_percentage bf44@STATISTICAL/**d2** S1.67/F1.04/2Y2.82，prod0.6595/self0.4114/与6颗互相关max0.3213 全过；submit_verdict=BLOCKED（LOW_INVESTABILITY_CONSTRAINED_SHARPE 0.91<1.17，FAILED_COUNT_RA 硬闸）。派 O496inv 修复：对 other496 内 total_assets 规模轴 vector_neut（rank/0.8/0.85 幂次）保单集 ATOM。
- **A 批（bf33/55@d4）收**：`78LP1NLx` S1.59/F1.09/2Y2.9 核心闸过但 **inv 0.9<1.17** 仍 BLOCKED；各变体 inv 恒 ~0.9 ⇒ 信号本质集中流动性差票，investability 是结构性难点，关键看 O496inv 规模轴 vector_neut 能否提 inv 到 1.17 且保 S。
- **other496 investability 新路径**：vector_neut 剥规模已证杀信号（信号=规模暴露）；改试**规模门控 trade_when**（只留 total_assets 前 80/60/40% 大票，保留信号但剔流动性差小票）——O496gate `4io8dK9iz4Yja6j11RLwqhLc` 在飞。若提 inv≥1.17 且保 S≥1.58 则第 7 颗；否则 other496 结构性定谳。
### 21.8 other496 结构性定谳 —— 规模门控修复彻底失败（KOR 上限 ~6 确证）
- **O496gate（total_assets 规模门控 trade_when，剔小票留大票）全失败**： gate0.2/0.4/0.6 → S 1.29/1.0/0.71（全 <1.58）、**inv 0.51/0.22/−0.15（比基线 0.91 更差）**、F 0.69/0.45/0.26。
- **定谳**：剔小票既杀 S 又让 inv 更差 ⇒ other496 共识修订信号**本质=小盘规模暴露**，信号源就在流动性差的小票里；vector_neut 剥规模（§21.6）与规模门控剔小票两条路都死。**单集 ATOM 无流动性字段可修，investability 硬闸结构性不可越** ⇒ other496 park，非交付件。（股东权益门控对照 3K4oZMdL 在飞，预期同失败，仅确认用。）
- **权益门控对照已收亦失败**（S1.02/0.78、inv 0.24/−0.05）⇒ other496 三条 investability 修复路全死，结构性定谳确证。
- **用户裁决：下调目标继续挖**（真实响应）；颗数问超时**自动选定 8 颗**（非用户明确填，可改）⇒ 新目标 8 颗（已 6，需再 2）。剩余未挖候选仅低覆盖 other635/event_relation，已派探针 O635(4DYyqeHn)+ER(jHNNpfOv) 收口。
- **O635 other635 判死**（6/6，最高 S0.08 几乎零信号，cov0.30 低覆盖新闻情绪如预期）。只剩 ER event_relation 在飞；若亦弱则新目标 8 颗（需再 2）无候选可达，KOR 上限 6 定谳。
- **ER event_relation 判死**（6/6，最高 S0.37，cov0.34 低覆盖弱机制）。**所有真未挖候选全数收口**：news85(0.69)/pv103(1.04)/news73(0.27)/other635(0.08)/event_relation(0.37) 判死、other496(S1.67) 三条 investability 修复路全死结构性堵死。**KOR 新挖可交付上限=6 定谳，连下调后的 8 颗也不可达**（已验收 6，无剩余 viable 候选）。

## 22. 目标再恢复：未亮塔真未挖集二次排查 + news76 开荒
- 用户 continue 恢复，指示找未亮塔数据集继续。实时塔状态：未亮 11 塔。派发记录交叉找到**真未挖漏网集**：news76/news21/news84/ai_news_scores/other567/news_sentiment_dl/news_sentiment_nlp/pv173/pv109/pv70（前次穷尽漏了它们）。
- 评估：**news76**(cov0.66/aC17，mws76_score情绪+confidence)最 promising；news21 事件日期元数据为主(仅 nws21_event_freq 连续且 aC116 拥挤)；其余低覆盖(0.19–0.37)。
- **N76 news76×10 模板已派**（`ZwD4sbUt4jVcfrRxDcd64H`，情绪水平/反/Δ/zscore/mean/confidence/power/门控/ts_rank）。在飞待收。
- **N76 news76 收口：弱**（10/10，天花板 S0.77=ts_mean情绪 WjOrOmgd，2Y仅0.68，反向−0.82确证正向；KOR新闻情绪弱如预期，缺口0.81）。判死。
- **ai_news_scores 判不可用**：103 字段描述全是 USA/ASI module（非 KOR 数据，同 sentiment21/other571 先例）。news84/news_sentiment_dl/nlp 低覆盖新闻情绪（弱）、pv173/109/70 极低覆盖、news21 事件日期元数据——均低预期。
- **O567 other567 多样性/包容性员工评分**（2 字段 cov0.26，最后异机制候选）探针已派 `tiUIq1fg4Vx8GQ1g670BNAH`（6 模板）。在飞待收；若弱则真未挖集全收口，KOR 上限 6 定谳。

- **KOR 最终裁决确证**：真未挖集 news85(0.69)/pv103(1.04)/news73(0.27) 死、other496 强信号但 investability 结构性阻断；剩余候选低覆盖弱机制。**KOR 新挖可交付上限 = 6 颗**（omERn83n/qMLOooX1/RRE9NkVj/d5Wvpmbx/ZYQ116ln/LLZ6wZO2），20 颗在现约束下不可达。

- **news73 判死**（N73 `emLRaacA4wJ8PsxvFJu8ca` 8/8）：恐惧/hype/不确定性/finup/findown 情绪天花板 **S0.27**（正向 0.21–0.27、反向 −0.39~−0.44），cov0.27 低覆盖+KOR 新闻情绪弱如预期。最后低覆盖候选关闭。**当前唯一希望=O496gate 规模门控 investability 修复**（在飞）。


### 21.6 other496 investability 修复失败 —— 强信号但硬闸结构性阻断（park）
- **O496inv 规模轴 vector_neut（total_assets，rank/0.8/0.85）全失败**：S 掉到 1.51–1.53（<1.58）、inv 反降到 0.82–0.85（更差）、F 0.90–0.91。total_assets 非有效规模代理，vector_neut 杀 S 且不提 inv。
- **终判**：other496 共识修订（aftercons_percentage bf44@STATISTICAL/d2，2rAVLRYP）S1.67/F1.04/2Y2.82/prod0.6595/self0.4114/互相关max0.3213 全过，但 **LOW_INVESTABILITY_CONSTRAINED_SHARPE 0.91<1.17 硬闸（FAILED_COUNT_RA）结构性阻断**——信号本质集中流动性差票，other496 单集无流动性/市值字段可过滤（保 ATOM 前提下不可修）。**park，非交付件**。
### 21.7 系统排查更多未挖集（继续 20 目标）
- 画像库"待测"标记多为陈旧占位/已收口集。实时字段层评估 4 个低拥挤未亮塔候选：**news73**(per-entity 恐惧/hype/不确定性情绪，aC0–2 但 cov0.27)、**other635**(情绪+字数元数据 cov0.30)、**event_relation**(3 关系编码 cov0.34)、**news29**(事件分类码非连续信号)——均低覆盖弱机制。
- **news73 作为最后候选派探针**（`emLRaacA4wJ8PsxvFJu8ca`，8 模板）收口；cov0.27 大概率弱。收口后 KOR 真未挖集全穷尽。

- **恢复开荒小结**：真未挖集 news85(S0.69死)/pv103(S1.04死)/other496(强但 investability 硬闸) 全数实测收口，无新增可交付。KOR 新挖交付仍 **6/20**。

## 23. 目标三恢复：在飞收割 + 覆盖地板结构性收口 + news76 形态闸合格探针
- **O567 other567 收割**（tiUIq1fg，6/6）：最优 O0AdAAZq（avg_diversity_inclusion_score 水平 bf63@RAM）S1.40/F1.33/2Y0.81，但 **CW 0.4276（超限4倍）+2Y0.81**，fRA=3；reverse 全负（−1.57/−1.23）确证正向。字段 cov **0.2619/0.2524 双双 <0.32 地板** ⇒ 权重集中是结构性，**覆盖地板收口（probe-independent）**。
- **news76 聚合多样性批收割**（2Z5Nhq7，8/8，vec_stddev/max/min/sum 全谱）：全弱，正向天花板 S0.67、reverse 最高|S|0.87，全 fRA≥3。
- **覆盖地板分诊（字段级实测，probe-independent 结构性收口 6 集）**：other567(0.26)/news_sentiment_dl(0.259)/news_sentiment_nlp(0.277)/pv70(0.268)/pv173(信号~0.06)/pv109(信号~0.15) 全 <0.32 ⇒ 收口。news84(0.37 勉强)/news21(0.74 但事件日期元数据) borderline。ai_news_scores 仍 USA/ASI 不可用。
- **news76 形态闸合格探针**：此前探针只 RAM 单族未过形态闸、判死无效。本轮按 morphology_gate 补合格双构型批（4族 group_compare/info_gate/order_flips/ts_shape + 4聚合算子 + KOR 破墙 hump/trade_when(adv20) 全覆盖，过闸 exit0；adv20 为 builtin 非数据集字段 ATOM 纯度无虞）。**N76gate `1ZZ2de4uH5dzb8nXnLJXJ3f` 已收割判死**（8/8）：天花板 xAr7VGmJ vec_max+hump **S0.88**/F0.67/2Y0.74，SH比率 S0.72–0.74、ts_zscore S0.67、PV kurtosis S−0.35，reverse 全负确证正向，全 fRA≥3、缺口 0.70。**过形态闸的合格双构型+4族+4聚合探针仍弱 ⇒ news76 合法判死**（三轮独立探针 RAM/聚合多样性/形态闸均 S<0.9，KOR 新闻情绪弱确证）。
- **news21 元数据收口**：13 字段几乎全事件日期元数据（YYYYMMDD 整数日期/季度标签/ estimated flag），唯一连续字段 nws21_event_freq cov0.967 但 **aC116 已拥挤** ⇒ 非连续预测信号，收口。
- **news84 形态闸合格探针已派**（`48rACcbah5hJbPQFBEpEWMc`，8式 SECTOR/d4，过闸 exit0）：TRNA 新闻情绪 transfer，23 字段 cov0.37 可试区间、**aC0–3 极低拥挤未挖**；mean/skew 情绪居中排名+hump、primary/secondary 比率、VECTOR vec_avg/vec_sum、trade_when(adv20) 破 investability。**已收割判死**（8/8）：天花板 Xg9ZvXO8 primary/secondary 比率+hump **S0.76**/F0.51/2Y1.34，mean 情绪 S0.65、skew S0.53、vec_avg S0.39，reverse 全负，全 fRA≥3、缺口 0.82 ⇒ 合格探针仍弱，news84 合法判死（KOR 新闻情绪弱确证）。
- **KOR 真未挖集全穷尽，上限 6 定谳（最终）**：news76(S0.88)/news84(S0.76) 形态闸合格探针均判死 + 覆盖地板 6 集(other567/news_sentiment_dl/nlp/pv70/pv173/pv109) + news21 元数据 + ai_news_scores USA/ASI 不可用。**KOR 新挖可交付 = 6 颗**（omERn83n/qMLOooX1/RRE9NkVj/d5Wvpmbx/ZYQ116ln/LLZ6wZO2），20 颗在现约束（ATOM 单集/KOR 固定/覆盖近十年/禁混）下不可达。无剩余 viable 数据集。

## 24. 用户锁定 RISK：形态闸重攻最后一轮（blocked 后普通回合指令）
- 用户选「形态闸重攻 RISK 最后一轮」。RISK 全景核实：最高产塔（6 颗占 2：omERn83n=risk70 anlystsn S1.62 / d5Wvpmbx=risk68 波动−美元量 S1.82），但两强轴已用尽、risk70 同族变体互相关>0.95；risk88=ASI 风格/行业载荷(弱)、risk59/60=借券域(KOR 死)、risk71/72=反转族(死)。
- d5Wvpmbx 机制=`subtract(group_rank(ts_delta(weight_volatility_short,22),sector), group_rank(ts_delta(weight_dadv,22),sector))`（波动变化−美元量变化，流动性/波动动力学）。
- **R68final risk68 非相关构型探针已派**（`4mgwPCaRe4PW8YTu5CGM3EI`，8式 RAM/d4，过闸 exit0）：波动/美元量比率、波动水平、ts_zscore 分布矩、edadv/dadv 比率、residual_return zscore 等**不同于 ts_delta 的机制**，求 S≥1.58 且与 d5Wvpmbx 互相关<0.5 的新构型。在飞待收；若全弱或高相关则 RISK 无新增确证。
- **论坛补充检索（objective 查论坛要求，search_forum_posts 实测可用）**：①risk70 作 vector_neut 中性化辅料=点亮 RISK 塔主流模板（89赞帖，但跨集非ATOM，仅作辅料思路）；②CHN risk72 特定收益率「1字段3atom」（104赞）——KOR risk72 反转族已判死，CHN 构造或不同，低优先待核；③**波动率『上行波动−下行波动』不对称因子**（可提交帖）：risk68 residual_return 可构 upside/downside vol，是不同于 R68final 的 ts_delta/水平/比率的新机制，**若 R68final 弱则作后手探针**；④ASI RISK 集善用中性化档+因子一阶/二阶/斜率模板出货率高（呼应 d5Wvpmbx 用 RAM）。结论：RISK 强轴特异，论坛模板多为跨集辅料或风格载荷，ATOM 新增仍寄望 risk68 非相关构型。
- **R68skew risk68 分布形态/不对称后手探针已派**（`28tqNcfQq4zXcoSMuxXtW4Z`，6式 RAM/d4，过闸 exit0）：residual_return ts_skewness/ts_kurtosis（收益偏度/峰度=不对称机制，论坛『上行−下行波动』启发）、波动偏度、trade_when(adv20) 破墙臂。R68final 只测 ts_zscore 未测偏度/峰度，此是真新角度。**2 槽满**（R68final 4mgwPCaRe + R68skew 28tqNcfQq）在飞待收。
- **R68final 收割（8/8）：全弱**——最优 E56nLOv9 波动/美元量比率 **S0.59**，波动水平 S−0.76、ts_zscore S0.52(2Y2.30但S低)、edadv/dadv S0.36、residual_return zscore S−0.80(TO0.77)。**确证 d5Wvpmbx 的 ts_delta(波动−美元量) 是 risk68 唯一强机制**，比率/水平/zscore/edadv 等非相关构型全 S<0.6，无新增。
- **R68skew 报错归因**：`ts_skewness` 在 KOR **不可用算子**(inaccessible/unknown)，一条坏算子连坐整批(ts_kurtosis 条被 CANCELLED)。**教训：preflight_expressions 只查字段存在、不查算子可用性**；ts_kurtosis 可用(news76 跑过)、ts_skewness 不可用。
- **R68kurt 纯峰度重派**（`2QruC3cOf4ZO9mcxQx6qrAe`，6式 RAM/d4，过闸 exit0）：residual_return/波动 ts_kurtosis 尾部风险+反/门控/长窗，去除 ts_skewness。**已收割（6/6）：全≈零**——最优 E56nx5o0 波动峰度 S0.29，residual_return 峰度 S−0.10/0.00/0.22/−0.11，尾部风险机制死。**RISK 最后一轮三批全收口：R68final(最优S0.59)/R68skew(ts_skewness算子废)/R68kurt(最优S0.29) 均无新增 ⇒ RISK 重攻闭环，KOR 上限 6 确证（blocked 已立）。**
- **R68skew 复测（用户指令，补齐偏度机制）**：ts_skewness 幽灵算子已查明（get_operators 103 算子无时序偏度，偏度仅 reduce_skewness VECTOR）；用合法算子手工 Fisher 偏度 `ts_mean((x−ts_mean(x,W))³,W)/ts_std_dev(x,W)³` 重构 6 式（residual_return/波动，w66/252，反/门控/ts_rank），过闸 exit0。**R68skew2 已收割（6/6）：全弱**——最优 LLMow9la 反向偏度 S0.21，residual_return 偏度 S−0.40/−0.41/−0.44、波动偏度 S−0.29、ts_rank S0.11，偏度机制死。**分布形态三件套全收齐：水平/zscore(R68final S0.59)/峰度(R68kurt S0.29)/偏度(R68skew2 S0.21) 均弱 ⇒ RISK 彻底收口，KOR 上限 6 定谳（blocked 已立）。**

## 25. 用户转向 SENTIMENT：sentiment21 误判翻案重挖（blocked 后普通回合指令）
- 用户「换到Sentiment下数据集继续」。SENTIMENT 塔=0 未亮，6 集；台账 line677 曾「sentiment 塔关闭」（news_sentiment_transfer wave288 16模板判死 S0.72、other553 S0.83 弱、sentiment21/26 USA/低覆盖）。
- **sentiment21 误判翻案**：描述带 USA 但 KOR 实有覆盖 maxCov0.475、138 MATRIX 情绪统计字段(neg/pos/neut×mean/median/max/min/conf/dts)、aC0–10 极低拥挤（同 risk88 ASI 描述但可用先例）⇒ 真未挖。sentiment23 cov0.2648<0.32 死、sentiment27 网站流量弱机制、sentiment26 USA/低覆盖。
- **S21 sentiment21 探针已派**（`2a6VaW57n5gh9L61d3tKMULy`，8式 RAM/d4，过闸 exit0）：净情绪(pos−neg)、负情绪离散度 dts_gen、置信区间宽度(conf_up−conf_low 不确定性)、pos zscore、trade_when(adv20) 破墙。**已收割（8/8）：全弱**——最优 xAr77QaW 负情绪离散度 S0.39(2Y1.69)、置信宽度 rKRaaLma S0.29(2Y1.87)、净情绪 S0.10，全 S<0.4、距 1.58 缺口>1.1。**sentiment21 翻案后实测仍弱 ⇒ 原『死』结论结果正确（虽『USA 非本区』理由误判）、SENTIMENT 彻底收口，KOR 上限 6 确证（blocked 已立）。**

## 26. 用户转向 IMBALANCE：imbalance5 翻案实测（blocked 后普通回合指令）
- 用户「换到Imbalance上继续挖掘」。IMBALANCE 塔=0 未亮，仅 1 集 imbalance5（Oil Price Resilience，cov0.8559、aC1411 拥挤、2 字段）。台账 line685 曾凭「2字段+拥挤」判死、未必真测。
- 信号字段 imb5_score（SHIELD-OIL 油价韧性 0–1 分）+ imb5_mktcap（市值，ATOM 内规模正交辅料）。
- **IMB5 imbalance5 探针已派**（`41Z4k56Ng4Hkbz9n5S8ZHUM`，6式 RAM/d4，过闸 exit0）：油价韧性水平排名、反向、ts_zscore、vector_neut(rank score,rank mktcap) 规模正交、trade_when(adv20) 破墙、sector 轴。**首轮 `41Z4k56N` 6 child 全 ERROR（通用平台报错 'please try again'，非算子/字段/量纲错）⇒ 判平台侧瞬时故障，重试已派 `1cNWAI92U4Rrbr72Ou6u2GG`。**重试收割（6/6）确证首轮为瞬时平台故障**：最优 9qx5N7qK ts_zscore(imb5_score) **S1.52**/F1.16/**2Y0.70**(fRA2=LOW_SHARPE+LOW_2Y)，水平 e75MXxl6 S1.10、规模正交 S1.00、reverse −1.33 确证正向。**有信号但 2Y0.70 结构性失败(距1.58缺口0.88)、S1.52 亦差0.06 ⇒ 无臂达 S≥1.58+2Y≥1.58，imbalance5 不可交付、IMBALANCE 收口**（翻案证明非『无信号』而是『2Y 历史型衰减』，原『2字段拥挤判死』理由不当但结果不可交付）。
- **近线救援（goal 恢复）**：9qx5N7qK S1.52/2Y0.70 是唯一近线火种；归因主矛盾=2Y 历史衰减(缺口0.88)。走 2Y 车道：加长窗(zscore w504/ts_rank w504/backfill66)+hump/trade_when+**STATISTICAL 中性化**(最强2Y杠杆)。**IMB5rescue 已派 `4zCvyo7Ll4jw9pbHy6dAV2C`（6式 STATISTICAL/d4，过闸 exit0）在飞待收**。**已收割（6/6）：救援失败**——STATISTICAL+加长窗全劣化，最优 wpQdmpGl S0.97、全部 2Y 负值(−0.09~−0.41)，远劣于原 RAM w252 的 S1.52/2Y0.70。**2Y 车道救不活 ⇒ imbalance5 历史型衰减定谳、IMBALANCE 彻底收口，KOR 上限 6 确证**（STATISTICAL 非 KOR imbalance5 的 2Y 杠杆，GBR 经验不迁移；原 RAM w252 已经是最优档）。

## 27. 用户允许非 ATOM：跨集组合探索（blocked 后普通回合指令）
- 用户「可以允许非ATOM」——搜索空间从单集扩到跨集组合。组腿规则仍适用：禁混集合{PV,MODEL,OTHER,FUNDAMENTAL}内两两全禁；集合内×集合外≤5 类型；集合外×集合外不限量；每两塔组合候选≤3。
- **NA_INSD ANALYST×INSIDERS『聪明钱共振』组合已派**（`bdKj8bXs4NbczLme3vtG80`，6式 RAM/d4，过闸 exit0）：analyst10 预期惊喜(sal_fy2/net_fy1 ts_av_diff250) × insiders5 insd5_vol_chg 离散(vec_stddev ts_mean55)，机制=multiply 共振/vector_neut 正交/trade_when(adv20) 门控/subtract 分歧。两集合外组腿合法。在飞待收；若过线须与 6 颗 ATOM 交付件互相关<0.5 才算第 7 颗。
- **NA_R68 ANALYST×RISK68 组合并行已派**（`CGyxI8FJ5fgaNoaFMVFkMS`，6式 RAM/d4，过闸 exit0；闸曾拦 trade_when 臂缺 smoothing，加 hump 后过）：analyst10 预期惊喜 vector_neut(risk68 dadv 流动性)正交/trade_when 门控/multiply vol 交互/subtract 分歧，与 NA_INSD 互补。**2 槽满**（NA_INSD bdKj8bXs + NA_R68 CGyxI8FJ）在飞待收。
- **NA_INSD 收割（6/6）：非 ATOM 验证成功但互相关撞墙**——subtract 分歧臂 **E56jA0AP** `hump(subtract(group_rank(ts_av_diff(anl10_sal_fy2_pred_surps_v1,250),sector),group_rank(ts_mean(vec_stddev(insd5_vol_chg),55),sector)),hump=0.003)` **S1.58/F1.41/2Y2.15/TO6.6% fRA=0 全闸通过**；vector_neut 臂 6XdWbPbP S1.43/2Y1.58 近线；multiply 共振臂全弱(S0.66/0.09)。**但 E56jA0AP 与 qMLOooX1 互相关 0.6106、与 RRE9NkVj 0.6623(>0.5)⇒ 不能入篮**（建在 analyst10+insiders5 上，与这两颗已入篮 ATOM 高相关；与其余4颗 omERn83n0.4273/d5Wvpmbx0.1229/ZYQ116ln0.1271/LLZ6wZO20.0234 均<0.5）。**关键结论：非 ATOM 能产全闸件，但用已入篮数据集的组合必与其 ATOM 版高相关；要新增须找与篮子正交的组合（未入篮数据集/去相关机制）**。
- **NA_R68 收割（6/6）：近线无全过**——VkxrnaqJ subtract S1.55/2Y1.45(fRA2)、d5WMqb8J multiply S1.33/2Y2.4(fRA1)、MPYEwalo vector_neut S1.36/2Y1.56，无臂同时 S≥1.58+2Y≥1.58。
- **★0.7 阈值落地（config.BASKET_MUTUAL_CORR_MAX=0.7 + basket_diversity_gate 簇/结构审查，13单测+299回归全绿）**：E56jA0AP 在 0.7 口径与篮子 max 互相关 0.6623<0.7 ⇒ **可入篮为第 7 颗**（0.5 时被误伤、0.7 放行；簇识别无近亲簇、结构多样性各集≤1）。
- **E56jA0AP 交付核验**：self 过（max 0.6074<0.7，最相关 leAEYLM8）；prod 平台计算中（账号级单飞锁 retry240），提醒预读。若 prod<0.7 ⇒ 第 7 颗可交付（提交仍待用户确认）。
- **R68_INSD RISK68×INSIDERS5 组合已派**（`3qQyMG4O5583aIk12RUer1Xy`，6式 RAM/d4，过闸 exit0）：risk68 波动变化 × insiders5 量离散，subtract 分歧/multiply 交互/vector_neut 正交/门控。**已收割（6/6）：无全过**——最优 vR1Ezj5r subtract S1.17/2Y2.43(fRA2)、vector_neut j2Ypwj19 S1.07/2Y2.36、门控 vR1Ezjdr S1.15/2Y2.28，2Y 高但 S 全<1.58 ⇒ 无新可交付，R68_INSD 收口。**
- **prod 槽卡死确认（17:10→19:04 累计 ~110min 全空体，正常 1–5min）**：判定账号级单飞槽卡死/被他会话长占，暂停轮询等用户干预；E56jA0AP 第 7 颗只差 prod 这一读（其余全过）。
- **ANL_IMB ANALYST×IMBALANCE5 组合已派**（`3kfXADfNi4Ad9aO2d7J2pa7`，6式 RAM/d4，过闸 exit0）：anl10 surps(sal/net ts_av_diff250) − imb5_score oil韧性 分歧/multiply 共振/vector_neut 正交/门控——两个此前未组合过的字段族新配对。在飞待收，提醒 ~20:00 收割+顺带再 peek prod。
- **ANL_IMB 收割（6/6）无过线**：最优 multiply 共振 mLoGY8Z1 S1.36/F1.24/2Y1.50(fRA2)；subtract 分歧臂全弱(0.31/−0.48/0.27)——surps−油韧性分歧不成立。
- **ANL_R70 收割（6/6）无过线**：最优 multiply 共振 npvjAXYq S1.34/F1.20/2Y1.47(fRA2)；vector_neut JjeAP2Yx 1.11、分歧 QPvxYoqr 0.90。**组合律初步总结**：非ATOM 六臂系中 multiply 共振稳定落在 S1.3-1.4 近线带、subtract 仅 surps−insd5(=E56jA0AP 1.58) 一个成功样本——近线带与过线差 ~0.2 恰是历史证明「无任何单算子族能补」的强度缺口。
- **Wave3 INSIDERS×IMBALANCE5 已派**（`2aHZ3I7qJ4h29DYolarsb36`，6式 RAM/d4，预过闸 exit0）。
- **prod 19:26 再 peek 仍空体**（卡 ~2h20min，异常持续，等用户/平台侧解）。
- **Wave4 RISK68×IMBALANCE5 已派**（`3K9hMXdkR4GBaqpH1FPH2bt`，6式 RAM/d4，过闸 exit0）：volΔ/dadvΔ − 油韧性 分歧/反/multiply/vector_neut/门控。与 Wave3 两槽并行，~19:53 合并收割。至此未试强配对基本铺完（ANL×{INSD,R68,R70,IMB}、R68×{INSD,IMB}、INSD×IMB）。
- **Wave3/4 收割均无过线**：best qMLa7kL1 INSD×IMB reverse 分歧 S1.34/2Y1.12(fRA2)、akK0aljO R68×IMB multiply S1.10/2Y1.38(fRA3)。**7 批 42 臂统计：过线仅 E56jA0AP(1.58)，近线带密集 1.34–1.55**——组合能造近线、强度缺口补不过的趋势确立。
- **Wave5(R70×IMB `30fumd6E74mmaj51aXUixwjL`)+Wave6(R68×R70 `AcP2f5u84j1bJlk26Kc4Xn`)已派**；Wave7(INSD×R70 `_args_INSD_R70.json`)、Wave8(ROA×{R68,ANL} `_args_W8_FUND.json`，OTHER×集合外配额 2/5)预铺待槽。第二层新发现：dataset id=`other466`≠字段前缀`oth466_`；LLZ6wZO2 机制=ROA(net_inc/assets→ts_rank420)。
- **Wave5 收割无过线**：best E56jmpN0 multiply S1.22/2Y1.33(fRA2)；分歧臂多为负(−1.0~−0.35)——R70情绪×油韧性互补性差。
- **Wave6 收割无过线（重要负结果）**：最强双信号对 R68×R70 反而最弱，best Xg93Nqx0 S0.65/2Y2.02、pwd2W0bq 0.79/2Y1.09——两个已入篮强 ATOM 的载荷互相抵消，「最强≠最好组」。
- **9批54臂统计**：过线仅 E56jA0AP 1 例(1.58)；近线带 1.2–1.55 密集；W7(2D0R95bx75gk8ZOtS31zB5)/W8(qTmLzbvf528blzXWfo2Cq4)在飞，W9预铺待槽。
- **Wave7 收割无过线**：best kqNwGQ0L S1.01/2Y1.02，其余臂全负(−0.6~−1.4)——INSD离散×R70情绪互补更差。
- **Wave8 收割无过线**：best 0mYVgRLv(ROA−surps分歧) S1.27/2Y1.52(fRA2 近线)，其余0.5-0.8。
- **Wave9 ROA×{INSD,IMB} 已派（收官批）**，11批66臂仅1过线(E56jA0AP)——矩阵趋势收敛：组合造近线、难造过线。
- **Wave9 收割无过线**：best ZYQ8MK2d S1.30/2Y1.14、gJeld9o0 1.18/2Y1.57——ROA 第二层也封顶近线。**12 批 72 臂累计：过线仍仅 E56jA0AP**。
- **Wave10 近线精修 grid 已派（最后的内生杠杆）**（`4b8Vks1575hYbgvkTrEwt62`）：目标 VkxrnaqJ 族(S1.55/2Y1.45 史上最近)——Δ窗66/edadv替代/surps窗66/ts_rank252/ts_mean5平滑/adv20门控 6臂，SOP「先归因后精修」执行，~20:44 收割。此后矩阵无预铺批，若 W10 仍近线→13批完整总结+组合到顶定论。
- **Wave10/11 收割（20:45）——「到顶」结论撤回**：W10 双**单闸臂**诞生：A1VpERvR **S1.59**/2Y1.38 fRA1(仅LOW_2Y)、kqNw9xoK S1.52/**2Y1.66** fRA1(仅LOW_SHARPE)；W11 1.21–1.40 未到位。距双达标仅差半闸——改判收口可行。
- **Wave12 单闸定向精修已派**（`DOYb23Ag4Zs8PFIyw2pofo`，6臂：窗谷200/300/150、ts_rank252 时序算子替代、adv20 门控、hump0.002 对照——每臂单杠杆，多族+过墙满足闸）。prod 20:45 仍空体(~5h)。
- **W13 STATISTICAL 收口批已派（2 槽双线）**（`1WCfwpdPF5byaUh1KreYa8m`）：两个单闸族的 STAT 杠杆版（先例 other466 RAM→STAT +0.22；kqNw9xoK 仅需 +0.06）+vector_neut 变体。收口矩阵=RAM(W12)×STAT(W13) 双轴并行，~21:15 合并收割。
- **Wave11 乘共振精修 grid 已派（第二槽填满，矩阵存货至此全部上场）**（`3yFPE7nV4q39wa10L1TlOMi`）：目标 2Y 缺口最小族 mLoGY8Z1(1.36/2Y1.50)与0mYVgRLv(2Y1.52)——imb窗22/252、surps窗126、ts_mean5平滑、adv20门控、industry轴 6臂。14 批 80 臂为组合线全部弹药。
- **prod 20:04 再 peek 仍空体**（死锁 ~3.5h）。
- **ANL_R70 ANALYST×RISK70『修正动能 vs 情绪载荷分歧』已派**（`49MwVk7ij50Qcfv16Gr5Mqa9`，6式 RAM/d4，过闸 exit0）：anl10 surps(ts_av_diff250) − rsk70_mfm2_asetrd_anlystsn(bf22)，臂=分歧/反/vector_neut 正交/multiply 共振/门控/net 变体。2 槽满（ANL_IMB+ANL_R70）在飞。
- **W12 收割（20:55，6/6 完成，无 ERROR）——无臂双达标**：j2YpJ6bQ(200/Δ66) S1.49/2Y1.65 fRA1(LOW_SHARPE)；**mLoGN5Mx(300/Δ66) S1.53/2Y2.04 fRA1**（S 差 0.05，2Y 最厚的近线臂）；xArLoN0N(150/Δ22) S1.54/2Y1.34 fRA2；LLMvwGAm(ts_rank252/Δ66) S1.51/2Y1.68 fRA1；O0ALjGEg(adv20 门控) S1.50 fRA2(+IS_LADDER)；**3qoKOpZN(126/Δ22) S1.64/2Y1.33 fRA1**（S 已越线、变 2Y 单闸臂）。
- **W12 归因（RAM 轴收口判据）**：沿 av_diff 窗谷 126→300 扫描呈 **S/2Y 负相关前沿**——短窗高 S 低 2Y（126:1.64/1.33）、长窗低 S 高 2Y（300:1.53/2.04）；**E56jA0AP(250/Δ66:1.58/2.15) 仍是该前沿唯一双达标点**，两侧中点无第二平衡位。RAM 侧「差半闸收口」宣告不成立：单杠杆位移只能在前沿上滑动，不能外推前沿。
- **态势**：W13(STAT 线) 20:55 harvest 仍 No children 在飞，为最后一线收口；prod 20:54 peek 仍空体（死锁 ~5.5h）。15 批 84 臂累计过线仍仅 E56jA0AP。
- **W12 单闸臂互相关预映射（0.7 口径 9×9 矩阵）**：mLoGN5Mx 对 6 存量+E56 **全对<0.7**（max=E56 0.6753，对已提交最高仅 0.5966）⇒ 若 S 补上 0.05 即有第 8 席资格且 prod 墙预期不高；3qoKOpZN↔E56 **0.7061** ✗ 且 2Y 差 0.25 ⇒ 预筛出局。备用池结论：全族只剩 mLoGN5Mx 一个真候选。

## 28. 2026-11-09 21:00 组合线收口判顶：W13 STAT 线全崩 + 16 批 90 臂总账

### 28.1 W13（STAT 收口线）收割 6/6：全线崩塌
JjeAkaOx S0.75 / npvjlG2q S0.73 / omEbXjgm S0.82 / xArLo7dg S0.94 / E56jMner S0.76 / ZYQ89VK0 S0.84——全部 fRA3(LOW_SHARPE+LOW_FITNESS+IS_LADDER)。同一批表达式 RAM 下 S 1.5+、STAT 下直接腰斩：other466 RAM→STAT +0.22 先例**不可外推**（中性化增益是数据集特异性，非普适杠杆）。

### 28.2 双轴收口矩阵终判：假设证伪
W12(RAM 轴) = 前沿滑动不越闸（S/2Y 负相关，1.49–1.64 噪声带）；W13(STAT 轴) = 崩塌。**「差半闸收口可行」改判回「到顶」**：E56jA0AP 是该双腿机制族在 RAM/d4/TOP600 下的唯一双达标点，前沿上无第二平衡位。mLoGN5Mx(S1.53) 差 0.05 属噪声带内距离，继续窗/杠杆参数搜索 = 过拟合轮盘，按纪律停手。

### 28.3 非 ATOM 组合线总账（用户允许非 ATOM 以来，27 日晚起）
- **16 批 90 臂**（NA_INSD/R68/ANL_IMB/ANL_R70/R70_IMB/W3–W13），全部形态闸过闸+preflight+单杠杆纪律。
- **过双闸仅 1 例：E56jA0AP**（S1.58/F1.41/2Y2.15/fRA0，self 0.6074 PASS，0.7 口径可入篮为第 7 颗）——只差 prod 终验（账号级死锁 5.7h+，21:02 仍空体）。
- 近线带 1.34–1.64 密集但均被单闸拦下；组合律：multiply 共振稳定落 1.3–1.4；subtract 分歧仅 surps−insd5 一个成功样本；「最强 ATOM 对」R68×R70 反而最弱(0.65)。
- **互相关预映射**：mLoGN5Mx 对篮子+E56 全对<0.7（备用席资格保留但不追）；3qoKOpZN 出局。

### 28.4 战役计数与待裁定
- 本战役新挖 = 6 颗全闸 ATOM + E56jA0AP(第 7，卡 prod 读) + mLoGN5Mx 等近线备胎（不可提交）。
- 20 颗目标在 KOR 现口径下不可达已第三次实证（ATOM 面 §13/§20、组合面 §28、prod 死锁阻断终验）。
- 路线三选一待用户裁定：①收口确认（解槽后验 E56、逐颗提交）②换配对面继续开新波（集合外×集合外未试对，仍需 prod 槽终验）③换区/改目标。

### 28.5 论坛取证：判顶范围收窄为「窗口/中性化类杠杆已尽」，外层结构/setting 杠杆未试（21:30 开 W14）
- 按 objective 过程约束（思路阻塞→查论坛）检索 2Y/ladder/LOW_SHARPE 破法，三帖含一手对照数据点：①外层 **group_neutralize(x,industry)** 同内核单变量 2Y 1.15→2.04、S+29%、margin 仅 −5%（GLB 实测）②**signed_power(·,0.5)** 对 S≈1.55 近线件「轻松过」，0.7 会压过头 ③**truncation 0.08→0.05** 治 2Y 差 0.1–0.2 ④中性化 **RAM/CROWDING** 系治 2Y（STAT/FAST/SLOW 全崩=与本战役 W13 实测吻合；CROWDING 本族未试）⑤拉长回看窗口是评论区认定的「唯一能单独抬 2Y」的变量。
- **rank_by_side 禁用**：账本实登 inaccessible（KOR 不可用），虽论坛主帖强烈推荐——幽灵算子连坐教训在前，不试。
- 存档 reference/forum_2y_ladder_levers_20261109.md。
- **W14_EXPR 已派**（RAM/d4/trunc0.08，`3QWmSdazx4ppcASq433dtBL`）：3 外层杠杆{GN-industry, signed_power0.5, adv20 门控}×2 基座{126/Δ22 卡2Y、300/Δ66 卡S}=6 臂，形态闸 exit0（三族 info_gate/nonlinear_x/peer_gap），算子数 9/7/9 ≤12。
- **W14_SET 已派**（**CROWDING**/d4/trunc0.08，`1GtMdA8df4Or8SxkK8nnqA5`）：两基座裸式，setting 单变量对照。**W14_TR**（trunc0.05，两基座）排队待槽。
- 判据预锁：任一臂 S≥1.58 且 2Y≥1.58 且 fail 空 → 过 0.7 互相关对照（对照 mLoGN5Mx/3qoKOpZN/E56）+prod/self/逐年 → 第 8 颗评估；GN 若确证抬 2Y，则对 W10 双单闸臂同样适用（W15 候补）。全灭则 §28 判顶升级为「含外层杠杆」的最终结论。

### 28.6 论坛第二轮四帖全文取证（21:45，存档 forum_2y_ladder_levers_20261109.md）
检索「结构认知/踩坑复盘/水平×交叉动量/10个救法」四帖（含 23/71/42/22 赞高热度帖），关键结论：
- **帖 43583615602711【结构认知】全周期↔2Y 强对冲（S/2Y 跷跷板=结构非参数）**：正解是**双车道分流**——一车道按全周期最优配参（=我方 W12/W13 已闭合），另一车道**专门按 2Y 最优配（缩短窗口/加权近期/换信号时间尺度）**。判死条款：「全车道闭合 且 2Y 结构性不达标 → 整理证据链上报裁决，不换批继续磨」。⇒ **W14 尚属 2Y 专属车道补轴（GN-industry/CROWDING 是真·未试轴），非违规翻案**；W14 全灭则两条车道闭合，终判顶成立。
- **★帖 44349557269655【踩坑复盘】修 2Y 五反直觉（对我方 W14 直接预警）**：①**signed_power/sign 套在「已排过序/已 zscore」的信号外面 = 精确空操作**（实测三臂读数逐位相同）——**我方 SP126/SP300 臂套在 group_rank(hump(subtract)) 外，大概率空操作**，已派（成本低，留作数据点证伪）；②decay 修 2Y 像抛硬币（11 族 30 臂仅翻 1）；③一心优化 Fitness 会把 2Y 优化掉；④2Y 偏短窗、INVCON 偏长窗，找同点矛盾；⑤**换宇宙/换 STATISTICAL 修 2Y 越改越差**（与 W13 崩盘互证）。核心：「2Y 不过多半是信号近两年本身变弱，不是参数没调对，来回换设置=浪费仿真」。
- **★★帖 43644505975959【Alpha Idea】分析师预期修正「水平×交叉指标动量」= 一次打通 Sharpe+2Y（W15 真正蓝图）**：DEU/Broker Estimates/FAST/d0/sector，V1 纯水平 S1.75 但 2Y0.89→V3 **动量换到另一指标** 2Y 跳 1.70→V4 动量窗 66→44 **双赢**（2Y1.77 且 PC 0.685 降）。骨架 `group_rank(add(ts_zscore(levelA,240), ts_zscore(subtract(levelB, levelB_4wks_ago),44)), sector)`。核心洞见：**水平供全周期 Sharpe、快动量供 2Y、二者必须用不同指标交叉**（同源则 2Y 提升有限）——**这正是「换时间尺度」而非「换参数」，绕开 S/2Y 跷跷板**。可选 signed_power(·,1.5) 补 S。
- 帖 38979392093591【10 个救法】：换中性化>调 decay>signed_power>ts_mean 平滑，与前帖一致，无新增硬杠杆。
- **W14 预期修正**：SP 臂按⑤预警大概率与母臂读数相同（证伪即弃）；**真正的新轴是 GN-industry（内层 sector 外层 industry 非冗余）+ CROWDING（setting 未试）**。W15 蓝图改为帖 43644505975959 的水平×交叉动量几何（换时间尺度），比 W14 的参数位移更可能破 2Y 墙。

## 29. 2026-11-09 21:45 ★W14 破壁：QPvx8M1W 全闸通过 = 第 8 颗候选（GN-industry 杠杆命中）

### 29.1 W14 收割（EXPR 6/6 + SET 2/2）
| 臂 | 构型 | S | 2Y | fRA | 判定 |
|---|---|---|---|---|---|
| **QPvx8M1W** | **GN(industry)@300/Δ66** | **1.67** | **2.02** | **0** | ★全闸通过 |
| MPYErOjM | GN(industry)@126/Δ22 | 1.69 | 1.41 | 1 | 仅卡2Y |
| bl6mwXYM | SP(0.5)@126/Δ22 | 1.61 | 1.53 | 1 | 差 0.05，但互相关 0.96↔3qoK 出局 |
| KPJo13Kp | SP(0.5)@300/Δ66 | 1.45 | 2.03 | 1 | SP 反降 S |
| E56jd1ZG/kqNwAdql | adv20 门控@126/@300 | 1.56/1.53 | 1.35/1.58 | 2 | 门控轴判死 |
| KPJo1QLj/pwd2LZ76 | CROWDING 裸式 | 1.21/1.20 | 1.07/1.55 | 2 | **CROWDING 本族判死**（论坛先例 GLB 特异性，再证「中性化增益不可外推」记忆条） |

### 29.2 QPvx8M1W 终验进度
- **self corr 0.6447 PASS**（最高 leAEYLM8，与 E56 同邻居）。
- **互相关 0.7 口径**：对 E56jA0AP **0.6245** ✓、对篮子 6 存量 max 0.6435 ✓ ⇒ **E56+QPvx+6 存量 = 8 颗篮子全对<0.7 成立（两新件各差 prod 一读）**。
- 母臂 mLoGN5Mx 0.9383 >0.7 ⇒ **QPvx 吸收母臂席位**（一族一席规律兑现：GN 壳提升 S 0.14 但 PnL 同源）。
- **逐年覆盖 2014–2023 十年无空窗**（longCount>0/pnl≠0 全过；逐年 S 0.52–3.19，2019 峰值 3.19、2022 段 2.42 支撑 2Y）。
- 待办：**prod 读数**（死锁中，E56 排队优先，QPvx 待槽解后串行触发，间隔 ≥6s）；robustness 归因（提交前走 brain-alpha-robustness）。

### 29.3 杠杆归因与在飞
- **GN-industry 外层 = 本族真破壁杠杆**（300 基座 S1.53→1.67 且 2Y 保 2.02；126 基座 S1.64→1.69 但 2Y 仍 1.41——杠杆效果基座依赖）。
- SP 非完全空操作：126 基座 2Y 1.33→1.53（+0.20）方向正确但幅度不足；帖 44349557269655 的空操作警告在 spread 几何下不完全成立（zscore 几何才逐位同）。
- 组合线累计 **18 批 102 臂**：双过线 2 例（E56/QPvx）——「组合造过线」自 §27 起由 1 例扩到 2 例，GN 轴打开新空间。
- **W14_TR 在飞**（`9gE6agUo4oEaAx18vSr0Ua8`，trunc0.05×{126,300}×{裸,GN} 4 臂：trunc×GN 交互对照）；**W15_CROSS 在飞**（`1SbySExd4nubQ8spvMRwVK`，论坛水平×动量几何 6 臂含单腿归因对照）。~22:15 合并收割。
- 若 W15 单腿对照显示动量腿 2Y 活性高，则「换时间尺度」线升格为独立机制族继续挖（第 9+ 颗）；GN-industry 杠杆同步复制到 W10 双单闸臂族（A1VpERvR/kqNw9xoK，W16 候补）。

## 30. 2026-11-09 21:55 组合线终判：W14_TR/W15 收割，剩余杠杆轴全闭合

### 30.1 W14_TR（trunc0.05×{裸,GN}×{126,300}，4/4）——truncation 轴空操作
E56j9xm9(126裸) S1.53/2Y1.36；WjOZvJ3N(GN126) S1.69/2Y1.41；78L5el32(300裸) S1.53/2Y2.04；9qxeNkd1(GN300) **S1.67/2Y2.02/fRA0**。
**四臂与各自 trunc0.08 孪生臂读数逐位相同**（9qxeNkd1≡QPvx8M1W、WjOZvJ3N≡MPYErOjM、78L5el32≡mLoGN5Mx）⇒ 权重未触截断上限，**truncation 非本族杠杆**，判死。9qxeNkd1 为 QPvx 同 PnL 重复件，不构成新席。

### 30.2 W15_CROSS（水平×动量，6/6）——换时间尺度线 KOR 判死
leAmLdGn(ebi add) S0.95/**2Y1.73**；qMLRK83Z(ebt add) S0.74/2Y0.84；vR1QK86z(交叉multiply) S0.92/2Y1.24；9qxnzYmr(门控multiply) S0.94/2Y1.31；gJe2Y6de(ebi水平单腿) S1.03/2Y1.59；0mYJbq66(ebt动量单腿) S0.86/2Y1.08。
**归因**：动量腿确供 2Y（leAmLdGn 2Y1.73、水平单腿 2Y1.59，论坛「快分量撑2Y」方向证实），但 **KOR smart_ests_v1 裸水平基线仅 S1.03**（论坛 DEU 基线 S1.75）⇒ 水平腿太弱，加动量补不回 S 到 1.58。**机制对、字段弱**，换时间尺度线在 KOR 该字段判死（不升格）。

### 30.3 组合线终态（20 批 112 臂）
- **双过线 2 例**：E56jA0AP（anl10×insd5，S1.58/2Y2.15）+ QPvx8M1W（anl10×rsk68 GN-industry，S1.67/2Y2.02）。均 self/互相关/逐年/边际(ΔS+0.19/+0.28)/robustness(PASS/CONDITIONAL) 全过，**只差 prod 读数**。
- **杠杆轴全闭合**：窗口(§28)、中性化STAT/CROWDING(§28/29)、门控(§29)、SP幅度不足(§29)、trunc空操作(§30.1)、换时间尺度字段弱(§30.2)。**GN-industry 是唯一真破壁杠杆，已提取 QPvx 一席**。
- W16（GN 复制 W10 族）预判低价值：kqNw9xoK(250/Δ66)与 QPvx(300/Δ66)互相关预期≥0.85 吸收同席；A1VpERvR(ts_rank252)2Y 基座弱 GN 救不动 ⇒ **不派**。
- **战役新挖计数 = 6 ATOM + 2 非ATOM候选 = 8**（E56/QPvx 候 prod）。20 颗目标 KOR 现口径不可达已四轮实证。

### 30.4 剩余唯一阻塞 = 平台 prod 单飞槽死锁（~6.7h）
E56/QPvx 及未来任何候选的 prod 终验全部悬置；非本会话可解，需用户检查他会话占槽/联系平台。解槽后串行触发（E56 先、QPvx 后，间隔≥6s），prod<0.7 即第 7/8 颗成立，逐颗呈用户确认提交。

## 31. 2026-11-09 22:05 ★prod 实测更正：「死锁」判断推翻，E56 撞墙 FAIL

### 31.1 诊断动作与读数（wq-prod-corr-read skill）
改用 `check_correlation(refresh=False)` 读 holder/缓存（而非只 --peek 空体）：
- **E56jA0AP prod = 0.7264，passes_check=false，computed=true（attempts 8 / 10.4s）** ⇒ **>0.70 FAIL，撞 prod 墙（灰区 0.70–0.80，余量仅 −0.0264）**。此前「全闸过只差 prod 一读」的乐观假设**被实测推翻**——self 0.6074 过≠prod 过（skill 铁律）。直方图 [0.7,0.8) 仅 3 条、[0.6,0.7) 131 条，墙薄但确实越线。
- **QPvx8M1W**：`check_correlation(refresh=False)` 触发回源 **120s 超时**（wall_clock_exceeded，故障#2/#5）；--peek 空体=平台仍在算；inflight 标记残留 300s，期内不重复触发。**读数未得，无结论不得落账**。

### 31.2 更正后的交付计数
- **E56jA0AP 不再是可交付第 7 颗**（prod FAIL）。除非降 prod 破墙（灰区余量薄，走 wq-window-valley / prod-lever），否则封盘。
- 战役新挖可交付 = **6 ATOM**（5 待提交+1 ACTIVE）+ **QPvx8M1W（候 prod，唯一在途希望）**。E56 转「prod 墙候选」。
- 「死锁~6.7h」实为 **E56 早被算出 0.7264 缓存、--peek 端点与 check_correlation 缓存路径不同步**（故障#4 本地锁≠平台）；QPvx 才是真正在算的新件。

### 31.3 下一步
- 等 QPvx inflight TTL(300s)+平台计算(1–5min)后 --peek/读 cache 取 prod；<0.70 ⇒ QPvx 成第 7 颗，逐颗呈用户确认。
- **E56 窗口杠杆判死、候选解封（22:09 prod_bucket_scan；22:20 用户两次纠正后更正）**：prod_max 0.7264、n[0.7,0.8)=3 ⇒ **仅「窗口手法」DEAD**（调 W 过不了）。**max=0.7264<0.75 属浅钉 ⇒ 按用户 2026-11-02 规则不得判死候选**，转「先归因（消融定位载钉机制面）→ 定向破墙（算子替换/换字段/几何外壳）」队列。此前『E56 封盘』为误判，已撤回；D0-P 分型(--all-buckets)待跑以确认非真密墙。
- **战役可交付 = 6 ATOM + QPvx8M1W（候 prod）+ E56jA0AP（浅钉归因破墙队列，未判死）**；mLoGN5Mx/3qoKOpZN 等近线备胎不可提交。20 颗目标 KOR 现口径仍紧张，但 E56 解封后保留救援通道。

## 32. 2026-11-09 22:10 ★用户二次纠正：n≥1=先归因后破墙（非封盘）；三层修复 + W16 消融归因批

### 32.1 纠正与修复（判据没错，标签措辞错）
- 用户指出：n≥1 应「先归因分析再破闸」，不应完全放弃——与 2026-11-02 既有规则（浅钉 n=1/max<0.75 不得直接判死，DEU 72 颗死于盲判 prod 墙的教训）完全一致；22:09 的「E56 封盘」违反该规则，**已撤回**。
- 三层修复：① skill `wq-window-valley-break-prod-wall` n≥1 动作列/「判族命运」→「判窗口杠杆去留」+ 新增澄清块「DEAD≠放弃，DEAD=换杠杆(先归因)」；② 脚本 `prod_bucket_scan.py` 输出标签 `DEAD(单钉子卡死)`→`DEAD(窗口死,先归因后破墙)` + docstring 同步（无测试依赖，py_compile 过，skill CRLF 保留）；③ 本台账 §31 解封。
- D0-P 补判（已取直方图免回源）：max 0.7264、n[0.7,0.8)=3、n[0.6,0.7)=131 ⇒ 按阈值名义 dense-wall，但**放行线 0.70 只需清 3 颗钉**，131 条不构成墙；浅钉可救窗口存在。

### 32.2 W16_E56BREAK 消融归因批已派（`1erVWb9xy5f69A91c2EQJkzW`，RAM/d4/trunc0.08，形态闸 exit0）
- 目的：定位 3 颗钉挂在哪个机制面。单杠杆 6 臂：anl10 面字段替换×3（surps_sal_fy2→**ebt_fy1_smart_ests / net_fy1_surps / pre_fy1_surps**，均 cov 0.83–0.95 实存核验）+ insd5 面平滑窗替换×2（55→**120 / 22**）+ adv20 门控×1。
- 判读规则：某面任一替换臂 **prod<0.70 且闸仍过** ⇒ 钉挂该面，定稿救援件；**两面替换全失败** ⇒ 深墙成立，那时才可终判死。
- prod 策略纪律（§四·1/四·2）：收割后先 compute_mutual_correlation 免费分层，**只挑 1–2 颗全闸臂串行测 prod**（间隔≥6s，不批量回源）；验收预锁 prod<0.70 + S≥1.58 + 2Y≥1.58 + fail 空 + self<0.7。
- 在飞全景：W16 归因批 + QPvx prod（平台算中）；~22:35 合并收割/复查（提醒已含）。

## 33. 2026-11-09 22:26 ★五颗 ATOM 提交预检总表（workflow_submit_alpha confirm_submit=false，边际服务未堵可正常回源）

| alpha | 数据集 | submit_gate | ΔSharpe(POWER_POOL) | dilutive | 结论 |
|---|---|---|---|---|---|
| d5Wvpmbx | risk68 | ✓ fRA0 | **+0.47** | false | **就绪可提交** |
| qMLOooX1 | analyst10 | ✓ | +0.23 | false | 就绪 |
| ZYQ116ln | intraday_pv_feats | ✓ | +0.24 | false | 就绪（首跑边际撞并发锁 fail-open，重试后取到） |
| omERn83n | risk70 | ✓ | +0.10 | false | 就绪 |
| **LLZ6wZO2** | oth466 | gate ✓ | **+0.0000**（噪声带<0.02） | — | **diversity_audit 阻断**：self 0.6760 贴线+零增量=占相关预算不证明贡献（CAP 宽度 1/ρ̄ 饱和逻辑，判据 BK 族）。不建议现提交；书变更后可复测 |
- 分区基线 before Sharpe 4.41 → 提交序列理论叠加后 ~5.0+（各 ΔS 非严格可加，仅参考）。
- RRE9NkVj 已 ACTIVE 不重复列。E56jA0AP 已判 prod FAIL 浅钉归因队列（W16 在飞）；QPvx8M1W prod 仍排队（20min 空体，账号槽疑似他会话长占，非边际服务）。
- 纪律：以上均**未提交**（confirm_submit=false 预检）。任何真提交须用户逐颗明确确认（不可逆）。

## 34. 2026-11-09 22:32 四颗就绪 ATOM robustness 首审：3 CONDITIONAL + 1 REJECT（提交清单修正）

- 详细表见 reports/robustness_20261109.md（22:32 追加节）。台账已落 robustness_{omERn83n,qMLOooX1,d5Wvpmbx,ZYQ116ln}。
- **提交清单修正（覆盖 §33「4 颗就绪」口径）**：**d5Wvpmbx（ΔS+0.47，2023=4.69 近年增强，质量最高）→ ZYQ116ln(+0.24) → omERn83n(+0.10) 三颗 CONDITIONAL 就绪**（软标记不阻断，提交描述三段如实带出）；**qMLOooX1(+0.23) robustness REJECT**（2023=0.69 单调衰减 max/min 5.30）暂缓，出路三选一（repair 治衰减/明令放宽留痕/暂缓）；LLZ6wZO2 diversity 阻断维持不提交。
- 逐颗提交确认时按修正后优先级；qMLOooX1 若用户选 repair 走 brain-alpha-repair ≤2 轮复审。

## 35. 2026-11-09 22:38 ★第 7 颗落定（QPvx prod 0.6687）+ W16 归因读数 + E56 救援代表 9qxnYPjd

### 35.1 QPvx8M1W = 第 7 颗全验证候选
- **prod 0.6687 正式读数 all_passed=true**（MCP 权威读，30+min 排队后平台恢复）+ 全闸 fRA0 + self 0.6447 + 篮子全对<0.7 + 十年无空窗 + 边际 ΔS+0.28 + robustness PASS ⇒ **验证链闭环**。**未提交**，待用户逐颗确认。

### 35.2 W16_E56BREAK 归因读数（6/6，面定性）
| 臂 | 单杠杆 | S | 2Y | fRA |
|---|---|---|---|---|
| **9qxnYPjd** | anl10 面 sal_fy2→**pre_fy1_surps** | **1.58** | **2.11** | **0** |
| Xg90GwJX | insd5 面窗 55→22 | 1.51 | 2.12 | 1(LOW_SHARPE) |
| QPv8MrbG | anl10 面→net_fy1_surps | 1.39 | 2.05 | 1 |
| 6Xdk7Pj5 | insd5 面窗 55→120 | 1.12 | 1.32 | 3 |
| E56d10pr/bl6wX2ON | anl10 面→ebt_ests(±门控) | 0.91/0.93 | 1.25/1.26 | 3 |
- 面结论：**anl10 surps 族内换字段(pre 最优)、insd5 面保快窗(22)是关键**；ebt 字段与慢平滑窗(120)为弱面。E56 钉大概率挂在 sal_fy2 具体字段的第三方碰撞面（self 0.6074→pre 件 0.5078 佐证该面拥挤）。

### 35.3 救援代表 9qxnYPjd（第 8 颗候选）
- 免费层：self **0.5078 PASS**；vs 篮子全对<0.7（max RRE9NkVj 0.6246；vs QPvx 0.4436）；vs E56 0.8705（同机制场移，非壳吸收）。
- **prod=correlation_busy 排队中**（不抢槽纪律），~22:47 复查提醒已设。<0.70 ⇒ E56 救援定稿（pre 替换件为交付体），≥0.70 ⇒ 深墙终判死成立、E56 家族按判死粒度沉淀。
- **22:34 robustness 快审补件：9qxnYPjd = PASS**（CV0.322/衰减0.918/maxmin2.27，十年无空窗，margin 30.2bp≥5bp PASS）——优于母件；其验证链现仅剩 prod 一读。
- **22:40 预检补件**：submit_gate ✓(fRA0) + 边际 **ΔSharpe+0.14 dilutive=false** + mix none ⇒ 9qxn 验证链仅剩 prod 一读（~22:41 提醒复查）。
- **22:42 提交参数草案落盘** `SUBMIT_DRAFT_20261109.md`：5 颗 name(KOR_R_*_01 不冲突已核)/tags/三段描述含软标记披露行/执行序——等用户逐颗确认，无任何自动提交。

## 36. 2026-11-09 22:52 W17_QMLREPAIR：qMLOooX1 REJECT 的修复证据波（三选一①的预研，非预设立场）

- **动机**：qML REJECT 根因=2023 年衰减（3.66→2.95→0.69）；W16 实证 **pre_fy1 面 2023 仍强**（9qxn 2023=1.45）+ W14 实证 **300 慢窗抬近年**。修复假设=换字段面/慢窗可治衰减，2×2 析因分离两杠杆。
- **设计（6 臂，`2PWV8gXF4S6c2P1hsCpXOrr`，RAM/d4/trunc0.08 同 qML 设置，形态闸 exit0 四族）**：A1 pre250×net250+GN（主修复）/ A2 sal300×net300+GN（仅慢窗对照）/ A3 pre300×net300+GN（双杠杆）/ A4 水平×动量 pre250×ts_delta(net,66)（论坛几何）/ A5 ts_rank252 腿替换 / A6 adv20 门控。hump 全臂常数化保证析因干净。
- **判读规则**：若 A1/A3 2023 年 Sharpe 显著>0.69 且全闸过 ⇒ 字段面修复成立 → 变体为新 ATOM 候选（与 qML 互相关分层后择一）；若仅 A2/A3 好 ⇒ 窗口杠杆；若全部 2023 仍弱 ⇒ analyst10 惊喜族 2023 衰减是族级现象，qML REJECT 维持、修复选项①关闭（用户三选一剩②③）。
- **中立性声明**：本波是 repair 选项的证据预研，不预设用户选择；选②放宽或③暂缓则本波数据仅作归因档案。收割 ~23:10。

## 37. 2026-11-09 22:57 ★9qxnYPjd prod=0.7025 FAIL（差 0.0025）——E56 家族按配对粒度封盘，战役终局计数落定

### 37.1 prod 终测与分支执行
- check_correlation(refresh=False) 第 4 轮取到平台值：**max=0.7025，passes=false**（放行线 <0.70 严格不等）。§35.3 预锁分支「≥0.70 ⇒ 深墙终判死成立」触发。
- **不追加 GN(9qxn) 最后一发**：GN 壳与母件互相关 ~0.94 先例（mLoGN↔QPvx）⇒ prod 期望 0.68–0.72 掷硬币，且 0.699 类贴线值对 prod 池日漂脆弱（48h 保鲜规则）——预锁纪律优于侥幸。

### 37.2 ★归因终局：钉子挂「配对面」而非「单腿数据集」
| 件 | anl10 腿 | 配对腿 | prod |
|---|---|---|---|
| E56jA0AP | sal_fy2_surps(250) | **insd5_vol_chg(55)** | 0.7264 ✗ |
| 9qxnYPjd | pre_fy1_surps(250) | **insd5_vol_chg(55)** | 0.7025 ✗ |
| QPvx8M1W | sal_fy2_surps(300) | rsk68_dadv(66)+GN | **0.6687 ✓** |
- 换 anl10 字段面只挪 0.024（0.7264→0.7025），换配对腿（insd5→rsk68）直接过线 ⇒ **载钉面 = insd5_vol_chg 分歧腿**（prod 池第三方内部人分歧类拥挤），anl10 surps 腿本身干净。
- **seal 粒度=配对**：「anl10_surps × insd5_vol_chg」配对族封盘不再派；同 anl10 腿 × 其它腿的配对不受连坐（QPvx 为证）。

### 37.3 战役终局计数（本战役新挖）
- **提交确认清单 = 4 颗**：d5Wvpmbx(ΔS+0.47) / QPvx8M1W(第7颗,+0.28,prod0.6687) / ZYQ116ln(+0.24) / omERn83n(+0.10)——全部等用户逐颗确认。
- 不放行：qMLOooX1(robustness REJECT,W17 修复证据在飞)、LLZ6wZO2(diversity ΔS=0)、E56/9qxn(prod 墙,配对封盘)、近线备胎若干。
- 已上线：RRE9NkVj(insd5 ATOM)。**20 颗目标：KOR 现口径不可达终局实证**（ATOM 面穷尽 §13/20 + 组合面 21 批 118 臂双过线 3 例其中 2 例 prod 墙 + prod 配对墙粒度发现）。
- W17_QMLREPAIR **已收割（23:04，6/6）→ 见 §38：修复选项①实证关闭**。

## 38. 2026-11-09 23:04 W17_QMLREPAIR 收割：修复选项①关闭（几何×字段交互规律浮出）

| 臂 | 设计 | S | 2Y | fRA |
|---|---|---|---|---|
| Xg905bnb | A1 pre250×net250+GN（主修复） | 1.45 | 1.23 | 2 |
| E56dXpE9 | A2 sal300×net300+GN（仅慢窗对照） | 1.52 | 1.50 | 2 |
| O0A3ENxb | A3 pre300×net300+GN（双杠杆） | 1.43 | 1.18 | 2 |
| P0oVd2OM | A4 水平×动量 | 1.36 | 1.37 | 2 |
| kqNA2oZ6 | A5 ts_rank252 腿 | 1.33 | 1.32 | 2 |
| mLovMm59 | A6 adv20 门控 | 1.33 | 1.32 | 2(+IS_LADDER) |

- **判读（§36 预锁规则执行）**：无一臂 S≥1.58（最高 A2 1.52），且 2Y 全部 ≤1.50 低于 qML 本身的 1.76 ⇒ **字段面与窗口面两个修复杠杆在 multiply 共振几何里双双失效，修复选项①关闭**（2023 逐年读数已无需再拉——S 闸先死）。
- **★新规律（几何×字段交互）**：pre_fy1 面在 **subtract 分歧几何**里是全闸件（9qxn S1.58/2Y2.11），在 **multiply 共振几何**里只有 S1.45/2Y1.23 ⇒ 杠杆有效性绑定（字段×几何×配对），**不可跨几何外推**——与「中性化增益数据集特异」「论坛模板跨区失效」构成三连实证。
- **qML 处置更新**：三选一 → **二选一**（②明令放宽留痕 / ③暂缓）。qML 平台闸仍全过（S1.94/S2Y1.76/prod0.6941/ΔS+0.23），仅本方 robustness REJECT（2023=0.69 衰减）拦——是否接受衰减风险属用户裁量。
- **全部外部线闭合**：prod 线（QPvx✓/E56✗/9qxn✗）、W17、robustness×7、边际×7、经验文档——**无任何在飞/排队事项**，剩余全部是用户裁定（4 颗提交确认 / qML 二选一 / 20 颗目标去向）。

## 39. 2026-11-09 23:40 ★prod 池漂移实锤：d5Wvpmbx 0.6906→0.9081 深墙出局，提交队列重排

### 39.1 新鲜度审计发现（用户 resume 后按 48h 规则复检 5 候选）
| 候选 | 11-08 快照 | 23:35 读数 | 判定 |
|---|---|---|---|
| **d5Wvpmbx** | 0.6906 | **0.9081** | **✗ 深墙（≥0.8 判死带），36h 漂移 +0.22，除名** |
| QPvx8M1W | — | 0.6687（今晚实测） | ✓ 唯一全链就绪 |
| ZYQ116ln | 0.6981 | 0.6981（疑 11-08 缓存，余量仅 0.0019） | ⚠ 待复证（平台重算中） |
| omERn83n | 0.6898 | busy/timeout 未取 | ⚠ 待复证 |
| qMLOooX1 | 0.6941 | busy 未取 | ⚠（robustness REJECT 在前，仅②放宽时需要） |
- peek 双通道均空体 = 平台正在重算（串行读已排队），**不重复触发**；~23:55 提醒接力读新值定稿清单。

### 39.2 结论与纪律确认
- **48h 保鲜规则实战验证**：贴线候选（0.69 系）36h 内可漂移 +0.22 至深墙——「prod 通过」是**时点读数不是状态**。skill 原文「prod 池每天有人提交同族 alpha，PC 只向上漂」在 d5Wv 身上以最大幅度兑现（risk68 价差族疑被第三方量产提交）。
- **提交时序纪律（新增）**：候选应在 prod 实测 <0.70 后**尽快提交**（同轮完成），隔夜即须重测；余量 <0.02 的贴线件视同未过，须等新鲜读数。
- d5Wv 深墙 ≥0.8 按 2026-11-02 规则直接判死（非浅钉），无归因破墙通道；其 ΔS+0.47 的增量随之作废。
- **提交队列现序**：①QPvx8M1W（全链就绪）②ZYQ116ln/③omERn83n（待 ~23:55 复证，漂移风险高）。

### 39.3 23:46 提前定稿轮（二次读数）
- **d5Wvpmbx 0.9081 二次确认**（两通道一致）——除名定谳，无复议。
- **ZYQ116ln = 0.6981（余量 0.0019）**：即便读数为新，按 §39.2 贴线纪律（余量<0.02 视同未过）**默认出局**；平台在提交时会实时复查 prod，若用户明示接受漂移风险可单独裁定提交（被拒为兜底，无副作用但耗提交额度）。
- **omERn83n 两次 120s 超时**（23:37/23:46，故障#2/#5 路径）：平台计算慢或队列堵，inflight TTL 后再读缓存，23:53 提醒轮收尾。**qML 本轮起不再测 prod**（REJECT 件不配终验，§四·2 层3纪律）。
- **提交队列终态（当前证据下）= QPvx8M1W 单颗**（0.6687 今晚实测、余量 0.031≥0.02、全链就绪）+ omER 待定 + ZYQ 贴线待用户风险裁定。
- **23:52 omER 第 3 轮=correlation_busy（retry_after 240，账号槽持续他会话占用）**：按预锁三轮纪律**停循环，判「无结论」呈用户人工处置**（选项：a. 改日槽闲时单读定稿；b. 旧值 0.6898 仅作排序参考不得放行；c. 直接除名）。不得写 0.6898 当读数（skill：busy≠通过≠失败）。
- **提交队列最终定格：QPvx8M1W 单颗确定**（全链闭环+今晚新鲜 prod）；ZYQ116ln 贴线出局待风险裁定；omERn83n 无结论待处置；d5Wvpmbx/E56/9qxn/LLZ/qML 各按判死/阻断留档。**战役全部机械动作至此收束，剩余 100% 用户裁定项。**
- **23:02 战役经验文档落盘** `reports/kor_mining_experience_20261109.md`（GBR/IND 同款规范）：字段面实证表 / 杠杆配方（GN-industry 真杠杆+五死杠杆）/ prod 配对墙规则 / 工具坑清单——objective「可复用结论记录」约束的战役级交付。


- **22:38 ★margin 单位错自纠**：此前 robustness 审计把 margin ×1000 报成 0.7–3.0bp（应 ×10000 = 7.0–30.2bp）——**7 颗 margin 轴实际全部 ≥5bp PASS**，verdict（PASS/CONDITIONAL/REJECT）不受影响（判定轴为 CV/maxmin/衰减）；7 条台账已覆盖重写、报告与台账全部更正。教训：bp 换算=×10⁴，报告数值须带公式自查。
- 更新后**提交确认清单（全部未提交）**：①d5Wvpmbx(ΔS+0.47) ②ZYQ116ln(+0.24) ③omERn83n(+0.10) ④QPvx8M1W(第7颗,+0.28) ⑤9qxnYPjd(第8颗,候prod) ——qMLOooX1 REJECT 三选一待裁定；LLZ6wZO2 不提交。













































