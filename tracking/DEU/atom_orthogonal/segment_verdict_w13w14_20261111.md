# DEU ATOM 正交战役 — Wave 13（model264 纯单数据集）判决 + Wave 14（starmine 修正广度）设计（2026-11-11）

> region 固定 DEU / TOP500 / D1 / SUBINDUSTRY / decay 4 / trunc 0.08 / nanHandling OFF / pasteurization ON / unitHandling VERIFY / maxTrade OFF；仿真区间 2014-01-01 ~ 2023-12-31。
> 硬闸：S >= 1.58、F >= 1.0、2Y >= 1.58、0.01 <= TO <= 0.7、sub_universe >= 0.474*S、RA fail = 0、self < 0.7、prod < 0.7。**2Y 是阻断线不是警告**。

---

## 一、Wave 13：`model264` 纯单数据集第一波 → **判弱（不可作主信号）**

批次 `gxYw6cqA4XKakqgNReNKy3`，10 条全部 COMPLETE / REJECT。

| # | 字段 | alpha | S | F | 2Y | TO | sub_u | failed |
|---|---|---|---:|---:|---:|---:|---:|---:|
| 1 | `mdl264_div_payout_class` | JjerXlEA | 0.48 | 0.24 | 0.45 | 0.0807 | 0.10 | 4 |
| 2 | `mdl264_amihud_class` | 2rAeZEbP | **0.69** | 0.24 | 0.81 | 0.3821 | 0.17 | 4 |
| 3 | `mdl264_bookp_class` | vR1Pz03d | 0.19 | 0.04 | 0.85 | 0.3350 | -0.12 | 4 |
| 4 | `mdl264_es_eps_fy1_r1m_class` | omEZz2ME | -0.30 | -0.09 | -0.43 | 0.1834 | -0.28 | 4 |
| 5 | `mdl264_eps_sur_decay_class` | 1YN0mvQR | 0.31 | 0.12 | 0.05 | 0.0705 | -0.57 | 4 |
| 6 | `-mdl264_eps_disp_class` | WjOJXk8Q | -0.22 | -0.05 | 0.31 | 0.2756 | 0.17 | 3 |
| 7 | `mdl264_gr_5y_eps_class` | wpQWz6g5 | 0.64 | 0.27 | **0.97** | 0.2324 | 0.36 | 3 |
| 8 | `mdl264_hr_epsyld_class` | omEZz2OE | 0.16 | 0.04 | 0.10 | 0.2114 | -0.23 | 4 |
| 9 | `add(div_payout, amihud)` | 88RX6Aqm | 0.63 | 0.27 | 0.64 | 0.2225 | 0.04 | 4 |
| 10 | `mdl264_news_sentvol_1d_class` | wpQWz6V5 | 0.14 | 0.02 | -0.14 | 0.3433 | -0.18 | 4 |

### 归因（★ 四条可复用结论）

1. ★★★ **`_class` 归一化分档字段作主信号全线 0-0.69**。同一批字段在组合件里却能到 1.68-1.75：
   - `mdl264_amihud_class` 单独 S **0.69**，与 starmine 两腿组合后 S **1.75**（Vkx3MjW8）
   - `mdl264_div_payout_class` 单独 S **0.48**，与 starmine 两腿组合后 S **1.68**（wpQYNvZp）
   ⇒ **model264 的 `_class` 族是「增量腿」不是「主信号」**：它只贡献相对排序的边际信息，单独不足以支撑截面 alpha。
   ⇒ 推论：任何「在组合件里表现好」的字段，必须先单独体检过 S>=1.0 才能当主腿，否则只能作辅助腿。

2. ★★ **MODEL 塔内两数据集组腿属禁止范围**。`wpQYNvZp` / `Vkx3MjW8` / `E56pROb9` 全是 `MODEL + MODEL`（model264 或 model216 x predictive_starmine），
   违反「PV/MODEL/OTHER/FUNDAMENTAL 集合内两两全禁」。**这三颗不能计入交付**，需重新审计存量 6 颗的合规性。

3. ★★ **修正族 `es_*_r1m_class` 方向为负**：`mdl264_es_eps_fy1_r1m_class` S **-0.30**。
   与 analyst93 / starmine 上「修正为正」相反 ⇒ **`_class` 分档把修正的方向信息压掉了**（分档只保留相对位置，丢失符号与幅度）。
   ⇒ 修正类机制不要用 `_class` 分档版，要用原始值版（本集只有 `_l1/_l2/_l3` 滞后原始值，无当期原始值）。

4. ★ **纯技术 / 纯质量族全灭**：`news_sentvol_1d` 0.14、`hr_epsyld` 0.16、`bookp` 0.19、`eps_sur_decay` 0.31。
   与 DEU 全区的结构性事实一致：**DEU 只对「前瞻预期修正」和「拥挤度」定价**。

---

## 二、Wave 14：`predictive_starmine` 修正广度族（批次 `1BnlEiAp4wLbV0OfYCeLUi`）

### 2.1 为什么选这一族

`predictive_starmine` 631 字段里存在一个**与已交付 6 颗完全不相交**的族：

| 族 | 字段数 | 说明 |
|---|---:|---|
| `analyst_upward_revision_count_*` | 60 | 上调分析师家数 |
| `analyst_downward_revision_count_*` | 44 | 下调分析师家数 |
| `analyst_upgrade_count_*` / `analyst_downgrade_count_*` | 10 + 10 | 评级上调/下调家数 |
| `recommendation_mean_change_*` | 10 | 推荐均值变化 |
| `surprise_pct_*` | 12 | 已实现惊喜百分比 |

维度：`{fq1,fq2,fy1,fy2} x {earnings,ebitda,revenue} x {7d,14d,30d}`。

**机制**：Chan-Jegadeesh-Lakonishok (1996) 修正广度（revision breadth）——
净上调比例 = U/(U+D) 是分析师群体行为的**方向一致性**度量，与「修正幅度」（已用 `mean_estimate_change_pct_*`）在信息上互补而非重复。

**为什么严格 ATOM 合规**：全部腿落在**同一个数据集** `predictive_starmine` 内，不构成任何两数据集组腿。

**为什么与存量 6 颗低相关**：存量用到的字段只有 3 个 ——
`mean_estimate_change_pct_f12m_earnings_14d_4` / `predicted_surprise_f12m_ebitda_4` / `mean_estimate_change_pct_f12m_ebitda_90d_3`，
与本波 16 个字段**零交集**。按既有判据「腿不相交才算新颗」，本波有资格扩充互相关池。

### 2.2 模板库（10 个结构互异模板）

设 `U` = upward 计数、`D` = downward 计数、`B = U/(U+D)` = 净上调比例。
全部外层加 `group_rank(..., industry)`（DEU 已验证最优轴），算子数 2-9，全部 <= 12。

| # | 模板 | 信息加工方式 | 算子数 | 来源 |
|---|---|---|---:|---|
| 1 | `group_rank(ts_mean(B, 22), industry)` | 水平（方向一致性） | 4 | 自建 / CJL1996 |
| 2 | `group_rank(multiply(ts_mean(B,22), rank(ts_mean(U+D,252))), industry)` | 水平 x 关注度（覆盖家数） | 8 | 自建（广度加权） |
| 3 | `group_rank(ts_av_diff(B, 66), industry)` | 一阶偏离自身历史 | 4 | 台账 DRF 归因（2Y 最优几何） |
| 4 | `group_rank(subtract(ts_mean(B_14d,22), ts_mean(B_30d,22)), industry)` | 期限结构（短窗 vs 长窗） | 8 | 自建（news-window term structure） |
| 5 | `group_rank(add(rank(ts_mean(B,132)), rank(ts_rank(U7-D7,11))), industry)` | 两腿异窗 add（倍率 12x） | 9 | QPv6jLvX 冠军骨架 |
| 6 | `group_rank(subtract(ts_mean(rank(UG),22), ts_mean(rank(DG),22)), industry)` | 评级动作净广度 | 6 | 自建 |
| 7 | `group_rank(ts_mean(recommendation_mean_change_30d_5, 22), industry)` | 推荐均值变化（水平） | 2 | 自建 |
| 8 | `group_rank(subtract(ts_mean(B_fy1,22), ts_mean(B_fq1,22)), industry)` | 目标层扩散（年度 vs 季度） | 8 | 自建（horizon spread） |
| 9 | `-group_rank(ts_std_dev(B, 66), industry)` | 二阶矩（分歧度反向） | 4 | 自建（低分歧溢价） |
| 10 | `group_rank(multiply(rank(ts_mean(B,66)), rank(surprise_pct_last_quarter_revenue)), industry)` | 跨族交互（广度 x 已实现惊喜） | 7 | 自建（两个独立信息源） |

### 2.3 preflight 结果

`valid=true`、`unknown_fields=[]`、`vector_fields=[]`、`platform_field_count=16`。16 个字段全部存在，无一需 `vec_*` 包装。

### 2.4 姊妹对命名陷阱（★ 下次直接用）

`analyst_upward_*` 与 `analyst_downward_*` 的**尾号（_2.._7）不是配对的**，同一 (horizon, metric, window) 下两侧尾号常常不同。
**已验证同尾号配对**（可直接用）：

| horizon_metric_window | 尾号 |
|---|---|
| fy1_earnings_14d | _4 |
| fy1_earnings_7d | _7 |
| fy1_revenue_14d | _4 / _7 |
| fy1_revenue_30d | _4 |
| fq1_ebitda_14d | _4 |
| fq1_earnings_30d | _7 |
| fq2_earnings_30d | _5 |
| fq2_revenue_30d | _3 / _6 |

**不可配对**：全部 `fy2_*`（downward 侧完全没有 fy2 字段）、`fq2_ebitda_30d`、`fy1_ebitda_14d`、`fy1_revenue_7d`。

---

## 三、Wave 13 / 14 设计期结论汇总

| 项 | 结果 |
|---|---|
| Wave 13 `model264` 单数据集 | **判弱**（S <= 0.69），只能作辅助腿 |
| 新增判死数据集 | `model264`（纯单数据集路线） |
| 存量合规性风险 | `E56pROb9`（model216+predictive_starmine）疑违 MODEL+MODEL 禁混 |
| 交付进度 | 合格件 6 颗（其中严格单数据集 ATOM 4 颗）；若剔除非合规 `E56pROb9` 则 5 颗 |


---

## 四、Wave 14 收批：`predictive_starmine` 修正广度族 → **判死**

批次 `1BnlEiAp4wLbV0OfYCeLUi`，10 条全部 COMPLETE / REJECT。

| # | 模板 | alpha | S | F | **2Y** | TO | sub_u | failed |
|---|---|---|---:|---:|---:|---:|---:|---:|
| 1 | 净广度比率 水平(22) | rKR8z8gE | **0.72** | **0.43** | **-0.14** | 0.1330 | 0.34 | 3 |
| 5 | 两腿异窗 add 132/11 | d5Wv7vAX | 0.71 | 0.26 | 0.23 | 0.3233 | 0.17 | 5 |
| 8 | 年度vs季度 horizon spread | j2YOwObO | 0.56 | 0.33 | 0.28 | 0.2089 | **0.74** | 4 |
| 6 | upgrade-downgrade 净动作 | QPv6l6Lr | 0.54 | 0.25 | 0.01 | 0.0915 | 0.39 | 3 |
| 2 | 广度 x 覆盖家数 | MPYV8VRa | 0.29 | 0.11 | -0.36 | 0.1289 | 0.13 | 4 |
| 3 | 一阶偏离 ts_av_diff 66 | bl6APAZK | 0.20 | 0.04 | **1.16** | 0.4119 | 0.10 | 4 |
| 10 | 广度 x 已实现惊喜 | xAr5z5gn | 0.02 | 0.00 | 0.29 | 0.0843 | -0.02 | 5 |
| 7 | 推荐均值变化 | 0mY5Q50p | -0.02 | 0.00 | 0.50 | 0.0923 | 0.14 | 3 |
| 4 | 14d vs 30d 期限结构 | zq3eoe6V | -0.31 | -0.10 | -0.16 | 0.1797 | -0.18 | 4 |
| 9 | 分歧度反向 | RREPaPWn | -0.36 | -0.15 | **-1.77** | 0.0582 | -0.21 | 4 |

### ★★★ 核心归因：**修正「幅度」有效，修正「广度」无效**

本波 10 条的 **2Y 几乎全为负或近零**：

```
-1.77 / -0.36 / -0.16 / 0.01 / 0.23 / 0.28 / 0.29 / 0.50   (8 条)
2Y 唯一 >1.0 的是 bl6APAZK = 1.16，但它的 S 只有 0.20
```

对比同一数据集 `predictive_starmine` 的**幅度族**（已在库）：

| 族 | 代表字段 | 已交付件 | S | 2Y |
|---|---|---|---:|---:|
| 修正**幅度** | `mean_estimate_change_pct_*` + `predicted_surprise_*` | QPvzNNGG | 1.70 | **2.18** |
| 修正**幅度** | 同上 | LLMzYrZe | 1.61 | 1.69 |
| 修正**广度** | `analyst_upward/downward_revision_count_*` | 本波 10 条 | <=0.72 | <=1.16 |

⇒ **同样是「分析师修正」，幅度是 DEU 的有效信号，广度不是。**
⇒ 机理假说：DEU 的定价只对**修正的强度/方向**（一阶矩）敏感，对**参与人数占比**（比例型广度）不敏感——
   广度是「有多少人改」，幅度是「改了多少」；前者在 TOP500 这种小宇宙里噪声占比过高（多数股票只有 1-3 个分析师，U/(U+D) 只有 0/0.5/1 三档，近似离散）。
⇒ **可移植判据：TOP500 级小宇宙里，凡是「分析师家数占比」型广度信号，先看分母（覆盖家数）分布，分母中位数 <4 就不要派发。**

### 其他归因

1. **`ts_av_diff` 仍然是 2Y 的最优几何**（bl6APAZK 2Y 1.16 为全波最高），与 DRF 台账「提 2Y 用 ts_av_diff」第四次一致；但它同时把 S 压到 0.20 => 该几何在弱信号上只能救 2Y 不能救 S。
2. **`upgrade-downgrade` 净动作（QPv6l6Lr）S 0.54 / 2Y 0.01** —— 评级动作族比修正计数族更弱，与 DRF 台账 `recommendation_mean_change` 0.02 一致。
3. **分歧度反向（-ts_std_dev）2Y -1.77 是全段最差** —— 第二次证伪「低分歧溢价」（首次是 news104 情绪一致性 -0.23）。**不要再用离散度类几何**。
4. **j2YOwObO 的 sub_u = 0.74 是唯一亮点**（年度与季度广度差），但 S 0.56 补不回来。

**判决**：`predictive_starmine` 的 `analyst_upward/downward_revision_count_*` / `analyst_upgrade/downgrade_count_*` /
`recommendation_mean_change_*` / `surprise_pct_*` 四族**全部判死**，不再投入。
该数据集仍只靠 `mean_estimate_change_pct_*` + `predicted_surprise_*` 两族贡献（已在库 2 颗）。

---

## 五、★ 新增工具坑：`preflight_expressions` 默认按 USA/TOP3000 校验

**现象**：对 DEU 特有数据集（如 `model216`）的 8 个字段跑 preflight，返回
`valid=false`、`unknown_fields=[全部 8 个]`、`platform_field_count=0`，
但 `get_datafields({region:"DEU", delay:1, universe:"TOP500", dataset_id:"model216"})` 明确列出这些字段存在且 `complete=true`。

**根因**：不显式传 `region` / `universe` / `delay` 时，preflight 内部按 **USA / TOP3000 / delay 1** 校验字段池，
返回体里 `region: "USA"`, `universe: "TOP3000"` 就是证据。区域特有数据集在这个池里查不到 => 整批误报 unknown。

**修法**：每次 preflight 必须显式带上

```json
{ "alpha_expressions": [...], "region": "DEU", "universe": "TOP500", "delay": 1 }
```

传了之后同一批 10 条立刻 `valid=true`、`unknown_fields=[]`。

**归类**：这是既知三类 preflight 缺陷（不校验算子-类型兼容 / 不校验字段名存在性 / 把 driver 值当字段）之外的**第四类**：
**默认区域错配导致的假阴性**。判读口诀：「红了先看返回体的 region/universe 是不是你要的区」。

---

## 六、Wave 15 / Wave 16 设计（在飞）

| 波次 | 批次 id | 数据集 | 塔 | 机制 | 模板数 |
|---|---|---|---|---|---:|
| Wave 15 | `12XoP3g4w5dH8Mkd6bhq01O` | `model216` | MODEL | 纯 ARM 修正模型（preferred/secondary/revenue x fq1/fy1/fy2 + 推荐修正），全 VECTOR 走 vec_avg | 10 |
| Wave 16 | `YVzh54q54QS94n1hf8kM0w8` | `shortinterest3` | SHORTINTEREST | 借券市场第二字段群（费率/费率波动/借出规模/借券期限/交易笔数），与 MPY9VNY9 的 `shrt3_bar` 腿不相交 | 10 |

### Wave 16 十模板（借券市场机制，Drechsler 2016 shorting premium / Muravyev 2021）

| # | 模板 | 机制 | 算子数 |
|---|---|---|---:|
| 1 | `-group_rank(ts_mean(vec_avg(mean_loan_rate_p5_d1), 22), industry)` | 借券费率水平（做空成本） | 3 |
| 2 | `-group_rank(ts_delta(ts_mean(vec_avg(mean_loan_rate_p5_d1), 22), 66), industry)` | 费率上升（压力累积） | 4 |
| 3 | `-(max - min)/mean` 费率分散度 | 借券市场摩擦/异质信念 | 7 |
| 4 | `-group_rank(借出股数 22d/252d, industry)` | 借出规模相对自身历史（short interest ratio） | 6 |
| 5 | `-group_rank(ts_av_diff(ts_mean(vec_avg(loaned_market_value_usd_p5_d1), 22), 132), industry)` | 借出美元规模偏离 | 5 |
| 6 | `-group_rank(ts_mean(vec_avg(average_loan_duration_days_p5_d1), 22), industry)` | 借券期限（做空者持有意图） | 3 |
| 7 | 费率波动 x 费率水平 | 双条件（紧张 + 不稳定） | 7 |
| 8 | `group_rank(transaction_count 22d/252d, industry)` | 借券活动升温 | 6 |
| 9 | 费率 132/11 两腿异窗 add | QPv6jLvX 冠军骨架（倍率 12x） | 6 |
| 10 | 费率 rank − 规模 rank 背离 | 供给端紧张 vs 供给充足 | 11 |

preflight：`valid=true`、9 个字段全部存在、`unknown_fields=[]`（已带 region=DEU/universe=TOP500）。
