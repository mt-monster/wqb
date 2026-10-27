# XgRVngzz 归因分析与定向破闸 — 2026-10-25

> 目标结构：`group_rank(-ts_regression(ts_zscore(returns,252), ts_zscore(vec_range(opt1_p_deltasurface_d1_vi),252),252,rettype=0), sector)`
> 设置：IND / TOP500 / D1 / decay 126 / trunc 0.08 / STATISTICAL / nanHandling OFF / maxTrade OFF

---

## 一、逐闸归因（`get_alpha_details` + `submit_verdict`）

| 闸 | 值 | 线 | 缺口 | 判定 |
|---|---:|---:|---:|---|
| **LOW_SHARPE** | **1.32** | 1.58 | **−0.26（−16.5%）** | FAIL |
| **LOW_FITNESS** | **0.94** | 1.00 | **−0.06（−6%）** | FAIL |
| **IS_LADDER_SHARPE（year 2）** | **1.13** | 1.58 | **−0.45（−28.5%）** | **FAIL（最严重）** |
| LOW_TURNOVER / HIGH_TURNOVER | 0.128 | 0.01–0.40 | — | PASS |
| LOW_SUB_UNIVERSE_SHARPE | 1.45 | ≈0.29×S | — | PASS |
| LOW_ROBUST_UNIVERSE_SHARPE | 1.31 | 1.0 | — | PASS |
| CONCENTRATED_WEIGHT | — | — | — | PASS |
| CLUSTER_TEST | — | — | — | PASS |
| **prod 相关性** | **0.3895** | 0.70 | **+0.310 余量** | **PASS** |
| **self 相关性** | **0.1894** | 0.70 | **+0.511 余量** | **PASS** |
| investability_sharpe | 1.17（保留率 88.6%） | 0.70×S | — | PASS |

**`failed_ra_count = 3`**：LOW_SHARPE / LOW_FITNESS / IS_LADDER_SHARPE。
**`checks.fail` 为空**（这三项落在 warning 组，但计入 `failed_ra_checks`——再次印证「读 `ra.failed_ra_checks`，不读 `checks.fail`」）。

### ★ 归因的最重要一条
**prod 只有 0.3895，余量 0.31。** 意味着可以做「提 S 但抬 prod」的激进交换——绝大多数候选死在 prod，这颗反而是反向富余。
**代价约束**：prod 若从 0.39 涨到 0.70，仍可接受（+0.31 空间）。

---

## 二、逐年归因（定位伤口）

| 年 | 2014 | 2015 | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Sharpe | 1.07 | 2.65 | 1.05 | **−0.69** | 1.92 | 1.91 | 2.06 | 0.88 | **0.25** | 2.09 |
| TO | 0.127 | 0.099 | 0.097 | 0.105 | 0.116 | 0.135 | 0.129 | 0.162 | **0.167** | 0.146 |
| margin(bp) | 8.6 | 24.9 | 9.6 | **−5.1** | 13.9 | 13.4 | 20.9 | 7.2 | **1.2** | 11.5 |

### 两条伤口，一条重叠
| 伤口 | 数值 | 影响哪道闸 |
|---|---|---|
| **2017 = −0.69** | margin −5.1bp，唯一负年 | 只拖全期 S |
| **2022 = 0.25** | margin 仅 **1.2bp**，TO 0.167（全期最高） | **同时拖全期 S 与 IS_LADDER** |

**IS_LADDER_SHARPE(year 2) = 1.13 正是 2022–2023 窗口**（2022 0.25 + 2023 2.09）。
⇒ **修 2022 一举解决两道闸**（S 与 ladder），是最高优先级的靶点。

### 2022 的形态特征（决定用哪个杠杆）
- **margin 崩到 1.2bp**（其余年份 7–25bp）→ 不是没信号，是**信号方向在高波动年份失真**。
- TO 0.167 为全期最高 → 高波动下信号频繁翻转。
- 2017 同样 margin 为负 → 两个伤口同属「趋势性强 / 波动剧烈年份 skew 反转失灵」，与论坛 77 赞帖自陈的规律一致（"skew 反转在低波动、趋势性强的年份会失灵，在高波动年份爆发"——但这里 2022 是例外，说明 IND 的高波动传导路径不同）。

---

## 三、定向破闸设计（单变量对照，同一批内跑）

| # | 杠杆 | 表达式变体 | 目标伤口 | 机理 |
|---|---|---|---|---|
| 1 | **对照** | 原式 | — | 基线 |
| 2 | `ts_scale(·,252)` | 外层加尺度归一 | **2022** | 把信号换算成「相对自身历史」，压掉高波动年份的幅度放大 |
| 3 | `ts_scale(·,504)` | 更长归一窗 | 2022 | 同上，更慢的基准 |
| 4 | `group_neutralize(·,subindustry)` | 内层细分组中性化 | 2022 | 2022 的失真可能来自行业级共振，内层剥掉 |
| 5 | `group_neutralize(·,industry)` | 内层行业中性化 | 2022 | 同上，粗一档 |
| 6 | `group_neutralize(·,market)` | 内层市场中性化 | 2017/2022 | 剥掉市场 beta |
| 7 | `group_neutralize(ts_scale(·,252), subindustry)` | **杠杆 2+4 组合** | 2022 | 若两者各自有效则叠加 |
| 8 | `trade_when(IV_z<1.5, 原式, -1)` | 高 IV 区间空仓门控 | **2022** | 2022 属高 IV 年，直接不在该状态持仓 |
| 9 | `winsorize(·,std=4)` | 尾部截断 | 2017/2022 | 两伤口都由极端值主导 |
| 10 | `tail(·,lower=-3,upper=3,newval=0)` | 中间段清零 | 2017/2022 | 只保留强信号，去掉噪声段 |

**控制变量**：10 条全部在同一 multisim、同一设置（decay 126 / trunc 0.08 / STATISTICAL / nanHandling OFF / maxTrade OFF）下跑，唯一差异是表达式里的杠杆，可直接横向比较。

**判读规则（预设，避免事后解释）**
- 杠杆有效 ⟺ `S ≥ 1.32` **且** 2022 年 Sharpe 上升；
- 若 S 上升但 2022 变差 ⇒ 判定为「非靶点增益」，不算解决归因问题；
- 若 prod 从 0.39 涨破 0.70 ⇒ 该杠杆作废（余量用完）。

---

## 四、实测结果

### 批 1：归因对照批（decay 126 / trunc 0.08，`jfe1d9094ZWbNw1a5hTxWTR`）

| # | 杠杆 | S | F | TO | sub | rob | 判定 |
|---|---|---:|---:|---:|---:|---:|---|
| 1 | **对照（原式）** | **1.32** | **0.94** | 0.128 | 1.45 | 1.31 | 基线（复现一致） |
| 2 | `ts_scale(·,252)` | 1.32 | 0.94 | 0.128 | 1.44 | 1.30 | **逐位相同——完全无效** |
| 3 | `ts_scale(·,504)` | 1.32 | 0.94 | 0.128 | 1.44 | 1.30 | **逐位相同——完全无效** |
| 4 | `group_neutralize(·,subindustry)` | 1.11 | 0.70 | 0.132 | 1.17 | 1.15 | 伤 −0.21 |
| 5 | `group_neutralize(·,industry)` | 0.99 | 0.62 | 0.128 | 1.24 | 1.04 | 伤 −0.33 |
| 6 | `group_neutralize(·,market)` | 0.53 | 0.26 | 0.102 | 0.89 | 0.77 | 重伤 |
| 7 | `group_neutralize(ts_scale(·,252), subindustry)` | 0.45 | 0.18 | 0.066 | 0.59 | 0.40 | 重伤 |
| 8 | `trade_when(IV_z<1.5, ·, -1)` | 0.27 | 0.09 | 0.066 | 0.27 | 0.30 | 重伤 |
| 9 | `winsorize(·, std=4)` | 0.08 | 0.01 | 0.062 | 0.25 | 0.09 | 毁 |
| 10 | `tail(·, ±3, newval=0)` | 0.01 | 0.00 | 0.105 | 0.10 | 0.19 | 毁 |

### 批 2：decay 66（唯一未测的 decay 轴，`ADPsSgBp4rA99Thjy0NF2C`）

| 变体 | S | F | TO | sub | rob |
|---|---:|---:|---:|---:|---:|
| 原式 @ decay 66 | **1.34** | 0.85 | 0.169 | 1.44 | 1.35 |
| `group_rank(·,industry)` @ 66 | 1.20 | 0.71 | 0.167 | 1.27 | 1.25 |
| `vec_range(option_implied_volatility_value)` @ 66 | 1.12 | 0.65 | 0.173 | 1.53 | 1.28 |

**decay 66：S +0.02、rob +0.04，但 F −0.09** —— TO 从 0.128 升到 0.169，被 `F = S×√(returns/TO)` 的换手项吃掉。**净效果更差，decay 126 仍是最优。**

---

## 五、结论：S 1.32 是信息上限，不是参数问题

**13 条杠杆全部测试完毕，无一胜过对照：**

| 类别 | 已试 | 结果 |
|---|---|---|
| 尺度归一 | `ts_scale` 126/252/504 | **逐位不变**（group_rank 已做横截面归一，再套时序归一无新增信息） |
| 内层中性化 | subindustry / industry / market / 组合 | 全部伤，粒度越细伤越重 |
| 尾部处理 | `winsorize(std=4)` / `tail(±3)` | 毁信号（残差已无肥尾可截） |
| 状态门控 | `trade_when` 高 IV 空仓 | 重伤（门控同时砍掉了有效区间） |
| 速度 | decay 8 / 66 / 126 / 252 | **126 最优**；66 提 S 但伤 F |
| 分组轴 | plain rank / sector / industry / subindustry | **sector 最优** |
| 外层算子 | rank / group_rank / quantile | group_rank(sector) 最优 |
| 结构 | 纯 skew 反转 vs 残差化 | 残差化必需（纯反转 S 0.57） |

### 为什么 2022 修不动
2022 年 margin 只有 **1.2bp**（其余年份 7–25bp），说明**信号在高波动年份的方向准确性本身下降**，而不是权重集中或极端值问题：
- 若是极端值 → `winsorize`/`tail` 应有效 ⇒ 实测毁信号，否证；
- 若是行业共振 → 内层 `group_neutralize` 应有效 ⇒ 实测减分，否证；
- 若是高 IV 状态污染 → `trade_when` 应有效 ⇒ 实测减分，否证。

⇒ 剩下的解释只有：**IND 的 skew 反转在 2022 这类年份信息本身消失**（与论坛 77 赞帖自陈的「低波动趋势年失灵」同源，只是 IND 的失灵年份不同）。这是信息层面的事实，FASTEXPR 内无解。

### 最终判定
- **prod 0.3895 / self 0.1894 全过，且余量巨大（0.31 / 0.51）——这颗不是死在任何一堵墙，是死在 S 的绝对高度上。**
- S 1.32 / F 0.94 / IS_LADDER 1.13，三闸同时差一点，且已验证无杠杆可推。
- **`XgRVngzz` 定性为 YELLOW 近闸天花板样本**，作为 IND × option 类别的能力边界证据保留。

---

## 六、2Y / IS-Ladder 专项攻关（论坛 + 官方文档）

### 6.1 官方机制（`get_documentation_page("consultant-submission-tests")`）

**阶梯逻辑**
1. 全历史 S < **FAIL_THRESHOLD（D1 = 1.59）⇒ 直接判失败**
2. 否则从 N=2 起：`S[N] < FAIL` ⇒ FAIL；`S[N] > PASS[N]` ⇒ PASS；介于两者 ⇒ N+1 继续

**D1 阈值表**：2/3/4/5 年 = **2.38**｜6 年 2.22｜7 年 2.06｜8 年 1.90｜9 年 1.74｜10 年 1.59
**★ 换手 < 30% 时 PASS 阈值 ×0.85**（FAIL 阈值不打折）⇒ 本颗 TO 0.128，2 年 PASS 实为 2.02。

> **关键推论：IS-Ladder 不是独立闸。它第一级就要求 2Y ≥ 1.59（FAIL 地板）。**
> **2Y 不够时，任何全期 S 的提升都救不了 ladder。**

### 6.2 跷跷板定量证据（三个配置）

| 配置 | S | F | TO | **2Y** |
|---|---:|---:|---:|---:|
| **decay 0** | **1.91**（LOW_SHARPE 直接 PASS） | 0.49 | **1.309** | **0.94** |
| decay 126（原式） | 1.32 | 0.94 | 0.128 | **1.13** |
| decay 126 + `quantile(ts_rank(·,120))` | 1.37 | **0.97** | 0.128 | 1.12 |

**2Y 在所有配置中从未超过 1.13。** 唯一让 S 过 1.58 的配置（decay 0）把 2Y 压到 0.94、TO 打到 1.31（HIGH_TURNOVER + F 0.49）。
⇒ 与论坛 23 赞帖「全周期 sharpe 与 2y 强对冲」完全一致，本轮给出了**定量坐标**。

### 6.3 论坛三条线索的实际效果

| 线索来源 | 做法 | 实测 |
|---|---|---|
| 2Y 排查帖（16 赞）+ IS-ladder 实践帖（14 赞） | `quantile(ts_rank(F,120))` 替换 `ts_zscore(F,252)` | ✅ **S 1.32→1.37、F 0.94→0.97、rob 1.31→1.37**；❌ 2Y 1.13→1.12 未动 |
| 同上 | `ts_rank` 窗 252 / 66 | S 1.26 / 1.23（120 最优） |
| KOR 1.33→1.61 帖（27 赞） | **decay = 0**（"信号够稳时 decay 反而削弱"） | ⚠ S 冲到 1.91，但 TO 1.309 爆表、F 0.49、2Y 掉到 0.94 |
| 同上 | **引入第二数据源**（其突破靠双数据集相加） | 我们用**合法形态**替代：`bucket(rank(ts_std_dev(returns,20)))` 波动分桶 / `bucket(rank(cap))` 规模分桶 / `trade_when` 高波动门控 ⇒ **全部更差**（S 1.13–1.23 vs 对照 1.37） |

### 6.4 2Y 为什么修不动（三重否证 + 官方机制）

| 假设 | 杠杆 | 实测 | 结论 |
|---|---|---|---|
| 极端值主导 | `winsorize` / `tail` | 毁信号 | 否证 |
| 行业共振 | 内层 `group_neutralize` | 减分 | 否证 |
| 高 IV 状态污染 | `trade_when` 门控 | 减分 | 否证 |
| 波动/规模分层差异 | `bucket(rank(vol))` / `bucket(rank(cap))` | 减分 | 否证 |
| 更新节奏断粮 | `quantile(ts_rank(·,120))` | 提全期 S，**2Y 不涨** | 否证（对 2Y 无效） |
| 速度不够 | decay 0 | 2Y 反降 | 否证 |

**唯一剩下的解释**：2022 年（S 0.25、margin 1.2bp）该信号的信息本身不存在。2Y 窗口（2022–2023）里有一半是空的，任何参数/结构都无法无中生有。

### 6.5 结论

> **2Y 无解，因此这颗 alpha 无法提交——不是因为 S 不够（decay 0 已证 S 可达 1.91），而是因为 IS-Ladder 的 2Y 地板是硬的，而这个信号在 2022 年没有信息。**

**当前最优版本更新为 `d5K6GQWJ`**：
```
group_rank(-ts_regression(ts_zscore(returns,252),
                          quantile(ts_rank(vec_range(opt1_p_deltasurface_d1_vi),120)),
                          252, rettype=0), sector)
decay 126 | trunc 0.08 | STATISTICAL
```
S **1.37** / F **0.97** / TO 0.128 / sub 1.37 / rob **1.37** / 2Y 1.12 / prod 0.39（余量充足）
—— **F 只差 0.03，是历史最好的版本；但仍卡在 2Y。**

---

## 七、双腿同族字段替换矩阵（「换字段」轴）

> 换字段是分区纪律里唯一能同时保住多道闸的杠杆，此前只零散试过几个，本轮做成完整矩阵。

**基准**：`group_rank(-ts_regression(<A>, quantile(ts_rank(<B>,120)), 252, rettype=0), sector)` @ decay 126 / trunc 0.08

| A 腿（PV） | B 腿（option1） | S | F | rob |
|---|---|---:|---:|---:|
| **returns** | **`vec_range(opt1_p_deltasurface_d1_vi)`** | **1.37** | **0.97** | **1.37** |
| returns | `vec_stddev(opt1_p_deltasurface_d1_vi)` | 1.29 | 0.89 | 1.28 |
| returns | `vec_range(opt1_p_raw_deltasurface_d1_vi)` | 1.22 | 0.84 | 1.26 |
| returns | `vec_range(option_implied_volatility_value)` | 1.20 | 0.80 | 1.22 |
| returns | `vec_range(opt1_p_deltasurface_d1_delta)` | 1.02 | 0.63 | 0.88 |
| returns | `vec_avg(opt1_p_deltasurface_d1_delta)` | 0.96 | 0.59 | 0.82 |
| **volume** | `vec_range(delta_vi)` | **−0.23** | −0.07 | −0.09 |
| **adv20** | `vec_range(delta_vi)` | −0.17 | −0.04 | 0.05 |
| **close** | `vec_range(delta_vi)` | −0.08 | −0.01 | −0.08 |
| **ts_std_dev(returns,20)** | `vec_range(delta_vi)` | 0.12 | 0.02 | 0.26 |

### 两条结论

**1. A 腿 `returns` 是刚性的，不可替换。** 换成 volume / adv20 / close / 实际波动率，S 全部崩到 −0.23 ~ +0.12。
机理：残差化剥掉的是「收益中被 IV 曲面解释的那部分」，A 腿一换就丢掉了「收益 vs 期权定价」这个经济含义，残差退化成两个无关量之差。

**2. B 腿 `vec_range(opt1_p_deltasurface_d1_vi)` 确认最优。** 次优 `vec_stddev(同字段)` 1.29（仅差 0.08）⇒ **「IV 沿 delta 轴的离散度/极差」这一族是最强信息源**；而 **delta 轴自身字段（`delta_delta`）明显更弱**（1.02 / 0.96）⇒ **有效信息在 IV 轴，不在 delta 轴。**

⇒ **「换字段」这条轴正式关闭：当前字段组合已是该族最优。**



