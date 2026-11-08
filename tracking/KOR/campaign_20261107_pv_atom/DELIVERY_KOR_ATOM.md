# KOR × TOP600 × D1 · ATOM REGULAR 交付文档（滚动更新）

> 目标：10 颗通过验证的 ATOM（单数据集）REGULAR alpha。
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
| 已验收（含已上线） | **3** |
| 缺口 | **7** |
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











