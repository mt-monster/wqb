# DEU ATOM 挖掘 · Wave 26–27 分段判决 + 2Y 突破

**日期**：2026-11-12
**区域**：DEU / TOP500 / D1 / SUBINDUSTRY / decay 4 / trunc 0.08
**区间**：2014-01-01 ~ 2023-12-31
**核心结论**：★★★ **2Y 墙被攻破**。`bl6AvMkN` 达成 `failed_ra = 0`、2Y 2.15、prod 0.647 —— Wave 14 以来第一颗全闸通过件。

---

## 一、Wave 26：`fundamental6`（FUNDAMENTAL 塔首开）→ **判弱**

- 批次：`3GH368axV5fn9ilrTOrCipm`
- 画像：cov **0.4923** / 196 字段全 MATRIX / alphaCount **1028**
- 内容：经典 Compustat 会计明细（季频资产负债表 + 年度流量表混排）
- 模板策略：**一次上 10 个结构互异的学术文献标准异象**（每个模板本身就是独立假设，有文献先验，不属于「盲目扫参」）

| # | 模板（文献来源） | alpha | S | F | **2Y** | TO | sub_u | margin |
|---|---|---|---:|---:|---:|---:|---:|---:|
| T1 | Gross Profitability（Novy-Marx 2013） | Xg9M1Gn8 | 0.51 | 0.27 | 0.55 | 0.0156 | 0.45 | 0.00434 |
| T2 | ROA（Ball-Gerakos 等） | qMLVg8lO | 0.49 | 0.24 | 0.01 | 0.0170 | 0.33 | 0.00364 |
| **T3** | **★ Sloan 应计异象（Sloan 1996，反向）** | **LLM3kW1v** | **1.09** | **0.85** | 0.36 | 0.0179 | **0.87** | **0.00847** |
| T4 | 资产增长（Cooper-Gulen-Schill 2008，反向） | E56xk1eJ | 0.09 | 0.02 | **1.11** | 0.0341 | 0.04 | 0.00038 |
| T5 | 杠杆（Bhandari 1988，反向） | rKR8AYPJ | −0.04 | −0.01 | −0.87 | 0.0147 | 0.06 | −0.0003 |
| T6 | Capex 强度（Titman-Wei-Xie 2004，反向） | Jjerbqve | −0.35 | −0.15 | 0.32 | 0.0155 | −0.11 | −0.0031 |
| T7 | R&D 强度（Chan-Lakonishok-Sougiannis 2001） | 78LlJWz8 | 0.02 | 0.00 | 0.73 | 0.0129 | 0.35 | 0.0003 |
| T8 | 毛利率扩张 ts_delta 252 | xAr5RqNw | 0.60 | 0.36 | −0.66 | 0.0368 | 0.29 | 0.00239 |
| T9 | 营运资本强度（反向） | VkxeOVG8 | −0.15 | −0.05 | −0.51 | 0.0176 | −0.21 | −0.0013 |
| T10 | 三口径盈利质量广度 | e75ELm36 | 0.45 | 0.23 | 0.04 | 0.0179 | 0.33 | 0.00368 |

**判决：判弱（不判死）**
- S 上限 **1.09** / F 上限 0.85 / 2Y 上限 1.11
- 唯一有料维度 = **Sloan 应计**：sub_u **0.87**（闸线 0.517）远超、margin **0.00847** 全波最高、换手 0.0179 极低 ⇒ 这是个**高质量但强度不足**的信号
- 全部 10 条 TO 落在 0.0129–0.0368（年度财报节奏），TO 不是问题
- **判据**：经典会计异象在 DEU TOP500 已被套利到 S≈1.0 级别；会计明细数据在 DEU 不能作为主信号塔，只能作辅助腿（与 `_class` 族同命运）

---

## 二、Wave 27：ANALYST × MODEL 合法两集混合 → **★★★ 攻破 2Y 墙**

- 批次：`17OgUNbV04L3bAva1HW5p59`（10/10 COMPLETE，无单位错）
- 混合合法性：`{PV, MODEL, OTHER, FUNDAMENTAL}` 集合内 × 集合外 ⇒ **ANALYST × MODEL 合法**，占「集合内×集合外」≤5 配额中的 1 个类型
- 设计思路：`d5WvnvGg` 双窗骨架（S 1.63 / 2Y 1.04）＋ `predictive_starmine` 的 f12m 三腿（已交付件 2Y 2.0–2.2 的驱动腿）

| # | 结构 | alpha | S | F | **2Y** | TO | sub_u | failed |
|---|---|---|---:|---:|---:|---:|---:|---:|
| T1 | 三腿 66/5 + f12m_ebitda W5 | vR1Pd9wz | **1.73** | 1.47 | 1.39 | 0.0854 | 1.01 | 1 |
| T2 | 三腿 66/5 + f12m_earnings W66 | omEZVv86 | 1.61 | 1.35 | 1.10 | 0.0568 | 0.76 | 1 |
| T3 | 四腿全加 | 1YN0JLkK | **1.77** | **1.54** | 1.31 | 0.0791 | 0.97 | 1 |
| T4 | 两腿简化 66 + f12m W5 | WjOJ9dMj | 1.57 | 1.23 | 1.39 | 0.0918 | 0.90 | 2 |
| T5 | f12m 权重 ×2 | kqN9QXdk | 1.49 | 1.09 | 1.32 | 0.1026 | 0.84 | 2 |
| T6 | group_neutralize **subindustry** | A1VEkb9l | 1.68 | 1.46 | **1.51** | 0.0853 | **1.05** | 1 |
| T7 | multiply 双确认 | xAr5RQql | 1.61 | 1.29 | 1.23 | 0.0639 | **1.06** | 1 |
| T8 | 252/11 长窗 | VkxeOEVb | 1.02 | 0.64 | 1.06 | 0.0734 | 0.69 | 3 |
| T9 | trade_when(f12m>0, …) 门控 | MPYVkXWo | 0.90 | 0.62 | **0.08** | 0.0335 | 0.39 | 4 |
| **T10** | **★★★ bucket(f12m W66) + group_neutralize** | **bl6AvMkN** | **1.61** | **1.36** | **2.15** | 0.1097 | **0.94** | **0** |

### ★★★ T10 `bl6AvMkN` 全闸通过（Wave 14 以来第一颗）

```text
group_neutralize(add(rank(ts_mean(eps_y1_estimate_change_3mo, 66)),
                     rank(ts_mean(predicted_surprise_f12m_ebitda_4, 5))),
                 bucket(rank(ts_mean(predicted_surprise_f12m_ebitda_4, 66)), range="0,1,0.1"))
```

- 算子数 **9**（≤12 ✓）：group_neutralize / add / rank×2 / ts_mean×3 / bucket
- 数据集：`analyst_factor_signals` ⊕ `predictive_starmine`（ANALYST × MODEL）
- 塔：`DEU/D1/MODEL ×1.8` + `DEU/D1/ANALYST ×1.8` ⇒ **effective = 2 塔**（一颗点亮两塔）

| 指标 | 值 | 闸 | 判定 |
|---|---:|---|---|
| Sharpe | **1.61** | ≥1.58 | ✓ |
| Fitness | **1.36** | ≥1.0 | ✓ |
| **2Y Sharpe** | **2.15** | ≥1.58 | ✓ |
| Turnover | 0.1097 | 0.01–0.7 | ✓ |
| sub_universe_sharpe | **0.94** | ≥0.474×1.61 = 0.763 | ✓ |
| margin | 0.001617 | >0 | ✓ |
| drawdown | 0.0701 | — | ✓ |
| **failed_ra** | **0** | =0 | ✓ |
| **prod correlation** | **0.647** | <0.7 | ✓ |
| 互相关（vs 6 交付件） | 最高 **0.658**（E56pROb9） | <0.7 | ✓ |
| checks.fail | **[]** | 空 | ✓ |
| checks.warning | MATCHES_COMPETITION / MATCHES_THEMES | 非 fail | ✓ |

- RA 全过 9 项：`LOW_SHARPE` / `LOW_FITNESS` / `LOW_TURNOVER` / `HIGH_TURNOVER` / `CONCENTRATED_WEIGHT` / `LOW_SUB_UNIVERSE_SHARPE` / `IS_LADDER_SHARPE` / `CLUSTER_TEST` / `MATCHES_PYRAMID`
- pending：`SELF_CORRELATION` / `DATA_DIVERSITY` / `PROD_CORRELATION` / `REGULAR_SUBMISSION`（PROD 已实测 0.647 ✓）
- `investability_sharpe` 1.23 / `risk_neutralized_sharpe` 0.58

### ★★★ 核心判据：**bucket 轴是 2Y 的唯一有效杠杆，且必须建在「异族字段」上**

同核心信号（`eps_y1_estimate_change_3mo` 66 + `predicted_surprise_f12m_ebitda_4` 5），只换中性化轴：

| 中性化轴 | alpha | S | **2Y** | 2Y 变化 |
|---|---|---:|---:|---:|
| `subindustry` | A1VEkb9l | 1.68 | **1.51** | 基线 |
| **`bucket(rank(f12m W66), 0-1-0.1)`** | **bl6AvMkN** | 1.61 | **2.15** | **+0.64** |
| `industry` + 单字段双窗（对照） | d5WvnvGg | 1.63 | 1.04 | −0.47 |

**逐年归因对比（这是全部机理所在）**：

| 年 | d5WvnvGg（industry 轴） | **bl6AvMkN（bucket 轴）** | Δ |
|---|---:|---:|---:|
| 2014 | 2.68 | 2.22 | −0.46 |
| 2015 | 3.15 | 2.86 | −0.29 |
| 2016 | 1.78 | 0.85 | −0.93 |
| 2017 | 1.35 | 1.03 | −0.32 |
| 2018 | 1.96 | 0.87 | −1.09 |
| 2019 | 1.21 | 1.61 | +0.40 |
| 2020 | 0.07 | 0.36 | +0.29 |
| 2021 | 3.38 | 2.70 | −0.68 |
| **2022** | **1.24** | **2.03** | **+0.79** |
| **2023** | **0.83** | **1.78** | **+0.95** |
| 全窗 | 1.63 | 1.61 | −0.02 |

**机理判读**：bucket 轴（由 `predicted_surprise_f12m_ebitda_4` 的 10 桶构成）**不是平滑算子**，它做的是「在相近预测惊喜水平的股票之间比较分析师修正强度」，从而把「预测惊喜本身已被市场定价的那部分」从信号中剥掉。这个 regime 因子在 2022–2023 高通胀/加息期间定价剧烈，剥掉它就把近两年 Sharpe 从 1.24/0.83 拉到 2.03/1.78 —— 而全窗 Sharpe 几乎不变（1.63→1.61）。

⇒ **与旧判据「平滑算子压死 2Y」并不矛盾**：`ts_mean` / `ts_target_tvr_decay` 是**时间维平滑**（抹掉时序信息 ⇒ 2Y 塌）；`bucket` 中性化是**截面维条件化**（剥掉一个 regime 因子 ⇒ 2Y 升）。**两者作用维度正交。**

**bucket 轴为什么必须建在异族字段上**（Wave 25 T10 vs Wave 27 T10 对照）：
- Wave 25 T10 `kqN9nYxl`：`bucket(rank(ts_mean(F, 252)))` 用**同一字段**，粒度 0.05 ⇒ S 1.52 / **2Y 0.95**（失败）
- Wave 27 T10 `bl6AvMkN`：`bucket(rank(ts_mean(M, 66)))` 用**另一数据集的另一语义族**，粒度 0.1 ⇒ S 1.61 / **2Y 2.15**（成功）
- ⇒ 轴字段与信号字段**必须承载不同的经济信息**，否则 bucket 只是把信号自己切碎，2Y 无改善。

### 其余 6 条 REVIEW 件的价值

| alpha | 2Y 缺口 | 备注 |
|---|---:|---|
| A1VEkb9l | 1.51 vs 1.58（差 0.07） | sub_u 1.05 / S 1.68 / F 1.46 最强；只差 2Y 一步 |
| vR1Pd9wz | 1.39 vs 1.58 | S 1.73 / F 1.47 / sub_u 1.01 |
| 1YN0JLkK | 1.31 vs 1.58 | S 1.77 / F 1.54 —— **全波 S/F 最高** |
| xAr5RQql | 1.23 vs 1.58 | sub_u 1.06 / investability_ratio 0.9876 最高 |
| omEZVv86 | 1.10 | — |
| VkxeOEVb | 1.06 | 长窗 252 失效（S 1.02）⇒ 再次印证长窗不是 2Y 杠杆 |
| MPYVkXWo | 0.08 | ★ `trade_when(f12m>0, …)` 门控把 2Y 打到 0.08、drawdown 0.1532 ⇒ **trade_when 门控在本族是毒药** |

**★ 新判据（第 7 次印证）**：`trade_when` 作门控在本区 = 灾难。此前 KOR 冠军骨架 `trade_when(ts_arg_max(...))` 在 DEU institutions6 上也只有 S 0.20。**DEU 不用 trade_when。**

**★ 新判据**：长窗 252 不是 2Y 杠杆（VkxeOEVb 2Y 1.06 < 短窗 A1VEkb9l 1.51）。窗口长度与 2Y 无单调关系。

---

## 三、Wave 28：strict-ATOM 复制 bucket 轴（在飞）

- 批次：`3csx9q8C04IbaHlaAIZLpjW`
- 目的：把 `bl6AvMkN` 的成功结构**压成严格单数据集 ATOM**（全部字段来自 `analyst_factor_signals`），因为 ANALYST×MODEL 两塔组合候选已超 ≤3 配额，且交付目标是 ATOM
- 10 个结构（全部 9 算子、全部 strict ATOM）：

| # | 轴字段（异族） | 粒度/窗口 | 设计意图 |
|---|---|---|---|
| W28-1 | `eps_revision_magnitude` | 0.1 / 66 | 直译 bl6AvMkN（revision 族 vs change 族 = 不同经济信息） |
| W28-2 | `revenue_revision_magnitude` | 0.1 / 66 | 换轴族：营收修正口径 |
| W28-3 | `eps_y2_estimate_change_3mo` | 0.1 / 66 | 换期限：2 年期 |
| W28-4 | `netprofit_y1_estimate_change_3mo` | 0.1 / 66 | 换指标：净利润口径 |
| W28-5 | `eps_revision_magnitude` | **0.05** / 66 | 粒度加密（20 桶） |
| W28-6 | `eps_revision_magnitude` | **0.2** / 66 | 粒度放粗（5 桶） |
| W28-7 | `eps_revision_magnitude` | 0.1 / **252** | 轴窗口加长（年度基线桶） |
| W28-8 | `eps_revision_magnitude` | 0.1 / 66 | 换信号：净利润双窗 |
| W28-9 | `eps_y1_estimate_change_3mo` **同族** | 0.1 / 66 | **对照实验**：故意用同族轴，预期 2Y 塌（复现 Wave 25 T10 结论） |
| W28-10 | `eps_q1_estimate_change_1mo` | 0.1 / 66 | 换期限：1 月期（更短的反应窗） |

**W28-9 是对照组**：若它也给出 2Y>1.58，则「bucket 轴必须异族」判据被推翻；若 2Y 落在 0.9–1.1，则判据成立。

---

## 四、数据集判决累计

本段新增：`fundamental6` **判弱**（累计判死/判弱 **47 个**有数据的数据集 + 44 个 cov=0 ⇒ 91 个）。

## 五、交付件状态（截至 Wave 27）

**全闸通过 7 颗**（全部 UNSUBMITTED）：

| # | alpha | 数据集 | 塔 | S | F | 2Y | TO | prod | 严格 ATOM |
|---|---|---|---|---:|---:|---:|---:|---:|---|
| 1 | mLox6Mg2 | sentiment7 + sentiment27 | SENTIMENT | 2.05 | 1.71 | 2.53 | 0.147 | 0.6935 | ✗ 双集 |
| 2 | E56pROb9 | model216 + predictive_starmine | MODEL | 1.79 | 1.70 | 2.03 | 0.067 | 0.6859 | ✗ **违禁 MODEL+MODEL** |
| 3 | QPvzNNGG | predictive_starmine | MODEL | 1.70 | 1.30 | 2.18 | 0.155 | 0.6777 | ✓ |
| 4 | LLMzYrZe | predictive_starmine | MODEL | 1.61 | 1.16 | 1.69 | 0.153 | 0.6697 | ✓ |
| 5 | MPY9VNY9 | shortinterest3 | SHORTINTEREST | 1.59 | 1.26 | 2.36 | 0.036 | 0.5986 | ✓ |
| 6 | QPv6jLvX | analyst93 | ANALYST | 1.59 | 1.52 | 2.01 | 0.0411 | 0.6615 | ✓ |
| **7** | **bl6AvMkN** | **analyst_factor_signals + predictive_starmine** | **MODEL+ANALYST（双塔）** | **1.61** | **1.36** | **2.15** | 0.1097 | **0.647** | ✗ 双集（合法） |

- 严格单数据集 ATOM = **4 颗**（QPvzNNGG / LLMzYrZe / MPY9VNY9 / QPv6jLvX）
- 合法两集（不违禁混）= mLox6Mg2（SENTIMENT×SENTIMENT 同塔不同集）+ bl6AvMkN（ANALYST×MODEL）= **2 颗**
- 违禁 1 颗：E56pROb9（MODEL+MODEL）
- 剔除违禁后 **合格件 = 6 颗**，全部可提交
- 互相关池：6 交付件全 <0.7；`bl6AvMkN` 与 6 交付件最高 0.658 ✓；`bl6AvMkN` 与 `d5WvnvGg` 0.715（但 d5WvnvGg 不可提交，不冲突）
