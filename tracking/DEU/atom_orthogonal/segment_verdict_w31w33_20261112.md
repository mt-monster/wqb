# DEU ATOM 战役 — Wave 31~33 段落判决书

日期：2026-11-12
region=DEU / universe=TOP500 / delay=1 / 仿真区间 2014-01-01 ~ 2023-12-31
硬闸：S≥1.58 / F≥1.0 / 2Y≥1.58 / 0.01≤TO≤0.7 / sub_u≥0.474×S / RA 失败=0 / self<0.7 / prod<0.7

---

## Wave 31 — `news18`（NEWS 塔）→ **判死**

批次 `31DSfIajL4jeaqJ17KukCxyd`，10/10 REJECT，全部 S < 0.45。

数据集画像：cov 0.8046 / 70 字段 / alphaCount 137，双覆盖层
（0.6925–0.6965 单实体层、**0.9788 多实体层**）。
机制设定 = 新闻情绪极性 × 新颖度 × 关注度变化（对齐论坛《新闻情绪因子》31 票帖的三条要点：
relevance 加权、`event_similarity_days` 新颖度过滤、关注变化而非水平）。

| # | 模板 | alpha | S | F | 2Y | TO | sub_u | drawdown | failed |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|
| T1 | relevance 加权情绪 W66 | Vkxepab8 | −0.04 | −0.01 | −0.46 | 0.0719 | −0.11 | 0.1662 | 4 |
| T2 | 新颖度过滤情绪 W66 | 0mY57X2r | 0.04 | 0.01 | −0.21 | 0.0728 | −0.00 | 0.1270 | 4 |
| T3 | 情绪动量 ts_delta 252 | YP1Ypbol | −0.10 | −0.02 | 0.01 | 0.0878 | −0.09 | 0.1637 | 4 |
| T4 | 新闻渠道分析师推荐变化 W66 | j2YOZAKk | −0.32 | −0.11 | −0.09 | 0.0658 | 0.04 | 0.2361 | 3 |
| T5 | 叙事冲击分 nip W66 | A1VEwNXW | −0.21 | −0.06 | −1.01 | 0.0645 | −0.37 | 0.1764 | 4 |
| **T6** | **新闻广度 event_count W66** | **xAr5x37w** | **0.44** | **0.21** | 0.96 | 0.0331 | −0.08 | 0.1326 | 4 |
| T7 | ts_covariance(情绪, 条数, 252) | omEZKLjn | −0.38 | −0.16 | −0.38 | 0.0409 | 0.36 | 0.3617 | 3 |
| T8 | 高置信情绪 qcm W252 | QPv6abRK | −0.43 | −0.17 | −0.87 | 0.0331 | −0.45 | 0.2370 | 4 |
| T9 | 无新闻即好消息 W252 | 88RXzjWV | −0.41 | −0.19 | −0.91 | 0.0194 | 0.05 | 0.3862 | 3 |
| T10 | 相关性 × 新颖度双条件 W66 | JjerpNaA | 0.04 | 0.01 | −0.46 | 0.0745 | −0.05 | 0.1657 | 4 |

**判死**：S 上限 **0.44**，10 条中 7 条为负；2Y 上限 0.96；回撤 0.127–0.386。
T6（纯新闻条数）是唯一正 S 项，且 sub_u −0.08 说明它只是一条「小盘噪声」。T9（无新闻即好消息）反向 −0.41
⇒ 新闻真空在德国不构成利好。

### 判据 H：DEU 新闻/文本族彻底封盘（第 5 次证伪，不再投任何 slot）

累计证据：

| 数据集 | cov | 最强 S | 结论 |
|---|---:|---:|---|
| news104 | 0.963 | 历史全灭 | 封盘 |
| news38 | 0.5992 | ≤0.40（历史） | 封盘 |
| news_sentiment_transfer | 0.9654 | 0.04（最强几何） | 封盘 |
| news50 | 0.65 | ≤0.40（历史） | 封盘 |
| **news18** | **0.8046** | **0.44（本波）** | **封盘** |

⇒ **覆盖率与新闻数据在 DEU 的预测力完全脱钩**。这条与既有记忆「cov 0.9654 却 S 0.04」同源，
现在有 5 个独立数据集、cov 0.60→0.97 全域覆盖的证据，判据升级为**机制级封盘**（不是数据集级）。
news17（cov 0.7906 / 48 字段）不再勘察。

---

## ★★★ 论坛命中：DEU 同区、同 universe、同 delay 的全闸骨架（可复用资产）

来源：`read_forum_post(article_id=43644505975959)`，作者 ZJ47333，2026-09-21。
标题《分析师预期修正的「水平 × 交叉指标动量」结构：一次打通 Sharpe 与 2Y 的实现记录》。
**关键：该帖的设置与本题完全一致 —— DEU / TOP500 / delay 1。**

### 一句话机制

分析师预期修正类信号里，**「预期水平」提供长期 Sharpe 但 2Y 墙**；引入**近 4 周修正动量**补 2Y；
且**水平与动量必须用不同指标**（跨指标交叉），否则两者同源、信息高度相关、2Y 提升有限。

### 作者实测的四版迭代（原文数值）

| 版 | 表达式 | S | F | 2Y | PC |
|---|---|---:|---:|---:|---:|
| V1 纯水平 | `group_rank(ts_zscore(est_12m_ebi_mean, 240), sector)` | 1.75 | 1.48 | **0.89** | — |
| V2 水平+同指标动量 | `group_rank(add(ts_zscore(est_12m_ebi_mean,240), ts_zscore(subtract(est_12m_ebi_mean, est_12m_ebi_mean_4wks_ago),66)), sector)` | 1.62 | — | 1.31 | — |
| V3 跨指标（动量换 ebt） | `... ts_zscore(subtract(est_12m_ebt_mean, est_12m_ebt_mean_4wks_ago),66) ...` | — | — | **1.70** | 0.725 ✗ |
| **V4 动量窗 44** | `group_rank(add(ts_zscore(est_12m_ebi_mean,240), ts_zscore(subtract(est_12m_ebt_mean, est_12m_ebt_mean_4wks_ago),44)), sector)` | **1.73** | **1.43** | **1.77** | **0.685** ✓ |

V4 附报 SC 0.387，作者称**全部检查通过**。动量窗 66→44 同时把 2Y 抬到 1.77、PC 压到 0.685（少见双赢点）。

### 作者的稳健性结论（逐条可执行）

1. **中性化 FAST 最优**；SECTOR / MARKET 略降；**SLOW_AND_FAST、SUBINDUSTRY 明显恶化**
2. **分组变量必须 `sector`**；industry / subindustry 都变差
3. **Decay = 0**，Truncation 0.08
4. **动量权重非线性**：加大到 ×1.5 / ×2.5 反而双降，等权附近最好
5. 动量窗口扫 22/44/66/126，**44 为甜点**
6. 补 S 可套 `signed_power(..., 1.5)`，略抬 S，对 2Y 几乎无影响
7. 降 PC 手段：`ts_rank → ts_zscore` 标准化器轮换、外层平滑、幂指数、**换 userCount 低的冷门字段**
8. 认知：**PC 与 Sharpe/Fitness 强负相关**，可提交窗口很窄，须逐点实测

### 与本战役已验结论的关系（重要：这是第 2 条独立的 2Y 杠杆）

| 杠杆 | 作用维度 | 出处 | 是否冲突 |
|---|---|---|---|
| `bucket` 中性化轴 | **截面**维（剥 regime 因子） | 本战役 Wave 27 `bl6AvMkN` 实测 2Y 2.15 | 不冲突 |
| **水平 × 跨指标快动量** | **时间尺度**维（慢分量撑 S、快分量撑 2Y） | 论坛 V4 实测 2Y 1.77 | 不冲突 |

⇒ **DEU 的 2Y 墙有两个正交解法**。既有的「平滑算子压死 2Y」结论不受影响——那是把快分量磨掉；
这里相反，是**故意加入一个更快的时间尺度**。

### 与本战役既有基线的冲突项（须实测裁定）

本战役自 Wave 1 起固定 `SUBINDUSTRY / decay 4`。论坛明确说 SUBINDUSTRY 对本骨架「明显恶化」、
FAST 最优。⇒ Wave 33 直接按论坛设置（**FAST / decay 0 / sector 分组**）派发，作为对照实验。

---

## `analyst7` 数据集字段画像（608 字段全 MATRIX，complete=true）

`get_datafields(region=DEU, universe=TOP500, delay=1, dataset_id=analyst7)` → count 608 / platform_count 608。

### 结构：16 个 12m 指标 × 27 变体 + 6 个季度指标 × ~25 变体 + 4 个推荐字段

**12m 指标族（各 27 个变体）**：`ebi`（EBIT）、`ebt`（税前利润）、`net`、`pre`、`gps`（GAAP EPS）、
`dps`（每股股息）、`cps`（每股现金流）、`roa`、`grm`（毛利率）、`nav`（净资产值）、
`ent`（企业价值）、`opr`（营业利润）、`tbv`（有形账面价值）、`csh`（现金）、`sal`（营收）、`eps`
**季度指标族**：`est_q_net`(26) / `est_q_ner`(25) / `est_q_ebt`(25) / `est_q_prr`(24) / `est_q_ndt`(23) / `est_q_dps`(22)

**27 个变体后缀（这是本数据集的核心价值）**

| 类别 | 后缀 | 机制含义 |
|---|---|---|
| 水平快照 | `_mean` `_median` `_high` `_low` `_std` `_num` | 一致预期水平 / 分歧度 / 覆盖家数 |
| **历史快照** | `_mean_28d` `_mean_4wks_ago` `_mean_3mth_ago` `_median_4wks_ago` `_std_4wks_ago` `_num_4wks_ago` | **可直接构造修正率**（现值 − 历史值） |
| **广度计数** | `_raised_1wk` `_raisednum_4wks` `_raisednum_1mth` `_lowered_1wk` `_lowerednum_4wks` `_lowerednum_1mth` | **上调/下调家数，cov 普遍 = 1.0** |

### 拥挤度（userCount / alphaCount）—— 选集依据

按论坛「优先挑 userCount 偏低的冷门字段」原则排序（`_mean` / `_mean_4wks_ago` 的 cov 与拥挤度）：

| 指标 | `_mean` cov | `_mean` uc/ac | `_4wks_ago` cov | `_4wks_ago` uc/ac |
|---|---:|---|---:|---|
| `tbv` | 0.5290 | **0 / 0** | 0.4938 | 0 / 0 |
| `ent` | 0.6860 | **1 / 1** | 0.6542 | 0 / 0 |
| `opr` | 0.6456 | 2 / 2 | 0.5144 | 0 / 0 |
| `csh` | 0.4827 | 2 / 2 | 0.4538 | 0 / 0 |
| `cps` | 0.7118 | 2 / 2 | 0.6808 | 2 / 2 |
| `grm` | 0.6245 | 2 / 2 | 0.5902 | 1 / 1 |
| `nav` | 0.6869 | 3 / 3 | 0.6755 | 0 / 0 |
| `dps` | 0.7351 | 9 / 9 | 0.7086 | 2 / 2 |
| `roa` | 0.6194 | 9 / 13 | 0.6092 | 4 / 4 |
| `pre` | 0.7321 | 16 / 22 | 0.7066 | 10 / 15 |
| `gps` | 0.7199 | 28 / 39 | 0.6845 | 15 / 19 |
| `ebt` | 0.7289 | 46 / 58 | 0.7003 | 21 / 30 |
| **`ebi`** | **0.7323** | **69 / 89** | 0.7055 | 28 / 35 |

### 广度计数族拥挤度（cov 全 = 1.0）

| 字段 | ac | 备注 |
|---|---:|---|
| `est_12m_ebi_raised_1wk` | **1446** | **全集最高**，周度上调家数 |
| `est_12m_ebi_raisednum_4wks` | **786** | 全集第二 |
| `rec_lowerednum_4wks` | 204 | 推荐下调家数 |
| `est_12m_ebi_num` | 154 | 覆盖家数 |
| `rec_raisednum_4wks` | 139 | 推荐上调家数 |
| `est_12m_ebi_lowerednum_4wks` | 120 | |
| `est_12m_gps_raisednum_4wks` | 103 | |
| `est_12m_sal_raisednum_4wks` | 57 | |
| `est_12m_net_raisednum_4wks` | 33 | |
| `rec_mean` (cov 0.7174) | 25 | 推荐评级均值 |
| `rec_num` (cov 1.0) | 26 | 推荐覆盖家数 |

### 4 个推荐字段（`rec_*`）

`rec_mean`（cov 0.7174，评级均值）/ `rec_num`（cov 1.0，评级家数）/
`rec_raisednum_4wks`（cov 1.0）/ `rec_lowerednum_4wks`（cov 1.0）

### 与已挖尽的 `analyst_factor_signals` 的区别（为何值得开波）

| 维度 | analyst_factor_signals | **analyst7** |
|---|---|---|
| 修正信号来源 | 厂商算好的 `estimate_change_3mo`（比率） | **原始水平 + 历史快照可自建修正率** |
| 广度信号 | 无 | **`_raisednum` / `_lowerednum` 全族，cov 1.0** |
| 推荐评级 | 无 | **`rec_mean` / `rec_raisednum` / `rec_lowerednum`** |
| 盈利惊喜 | 无 | **`act_q_*_surprisemean` / `surprisestd`（PEAD）** |
| 指标覆盖 | 6 个 12m 指标 | **16 个 12m 指标 × 27 变体** |
| 可构造「跨指标交叉」 | 极弱（只有 6 个） | **强（16 个，可做 A/B 交叉）** |

⇒ `analyst7` 提供 **4 类全新机制**：修正广度和方向、推荐评级变化、盈利惊喜（PEAD）、跨指标交叉。
这不是 analyst_factor_signals 的重复。ANALYST 塔在禁混集合之外，strict-ATOM 不占配额。

---

## Wave 32 — `analyst7` 广度/SUE/推荐族（SUBINDUSTRY / decay 4）

批次 `1drtcxgPa4Tla6E1fAueGYu1`，10 条 strict-ATOM，全部 ≤8 算子。

| # | 机制（文献） | 表达式骨架 | 算子数 |
|---|---|---|---:|
| W32-1 | 推荐净广度（Womack 1996） | `divide(subtract(rank(rec_raisednum_4wks), rank(rec_lowerednum_4wks)), add(0.001, rank(rec_num)))` | 7 |
| W32-2 | 三指标上调广度（Gleason-Lee 2003） | `add(add(rank(est_12m_ebi_raisednum_4wks), rank(est_12m_net_raisednum_4wks)), rank(est_12m_sal_raisednum_4wks))` | 6 |
| W32-3 | SUE 标准化盈利惊喜（Bernard-Thomas 1989 PEAD） | `divide(act_q_eps_surprisemean, add(0.001, act_q_eps_surprisestd))` | 3 |
| W32-4 | 推荐评级水平（Barber 2001） | `multiply(-1, ts_mean(rec_mean, 66))` | 3 |
| W32-5 | 4 周 rank 修正（ebi） | `subtract(rank(est_12m_ebi_mean), rank(est_12m_ebi_mean_4wks_ago))` | 4 |
| W32-6 | 分析师覆盖度变化（Gebhardt 2001） | `subtract(rank(est_12m_ebi_num), rank(est_12m_ebi_num_4wks_ago))` | 4 |
| W32-7 | 下调/上调不对称（Womack downgrade asymmetry） | `multiply(-1, divide(rank(est_12m_ebi_lowerednum_4wks), add(0.001, rank(est_12m_ebi_raisednum_4wks))))` | 6 |
| W32-8 | 修正/分歧信息比（Diether 2002 反向） | `divide(subtract(rank(est_12m_ebi_mean), rank(est_12m_ebi_mean_3mth_ago)), add(0.001, rank(est_12m_ebi_std)))` | 7 |
| W32-9 | 推荐 × 盈利广度双确认 | `multiply(rank(rec_raisednum_4wks), rank(est_12m_ebi_raisednum_4wks))` | 4 |
| W32-10 | 利润率修正背离（营收修正 − EBIT 修正） | `subtract(subtract(rank(est_12m_sal_mean), rank(est_12m_sal_mean_4wks_ago)), subtract(rank(est_12m_ebi_mean), rank(est_12m_ebi_mean_4wks_ago)))` | 8 |

外层：W32-1/3/5/7/8/10 用 `group_rank(..., industry)`；W32-2/4/6/9 用 `group_neutralize(..., subindustry)`。

### 结果：10/10 REJECT，但产出 2 个互补强腿

| # | 机制 | alpha | S | F | 2Y | TO | sub_u | drawdown | failed |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|
| W32-1 | 推荐净广度 | d5WvxJjx | 0.18 | 0.05 | −0.56 | 0.0800 | 0.05 | 0.2490 | 4 |
| **W32-2** | **三指标上调广度** | **VkxepQ7M** | 0.75 | 0.48 | **1.31** | 0.0998 | 0.78 | 0.1153 | 3 |
| W32-3 | SUE eps | 0mY57Zw2 | 0.09 | 0.02 | 0.58 | 0.0236 | −0.13 | 0.1994 | 4 |
| W32-4 | 推荐评级水平 | kqN93pVd | 0.09 | 0.02 | 0.00 | 0.0178 | 0.09 | 0.1641 | 3 |
| W32-5 | 4 周 rank 修正（ebi） | 2rAe7VOP | 0.43 | 0.18 | 0.20 | 0.1343 | 0.25 | 0.1054 | 3 |
| W32-6 | 覆盖度变化 | A1VEwX0g | 0.16 | 0.04 | 1.16 | 0.1407 | 0.20 | 0.2085 | 3 |
| **W32-7** | **下调/上调不对称（ebi）** | **O0Agpdr7** | **1.13** | **0.83** | 0.13 | 0.1189 | **0.93** | **0.1046** | 3 |
| W32-8 | 修正/分歧信息比 | gJeL1NQg | 0.63 | 0.35 | −0.35 | 0.0920 | 0.14 | 0.1058 | 4 |
| W32-9 | 推荐×盈利广度双确认 | YP1Yp35R | 0.58 | 0.32 | 0.56 | 0.1012 | 0.73 | 0.1178 | 3 |
| W32-10 | 利润率修正背离 | wpQWR7Zx | −0.11 | −0.02 | 0.01 | 0.1479 | 0.15 | 0.2167 | 3 |

**pre-screen 唯一 REVIEW = O0Agpdr7。**

### 判据 I：`analyst7` 里「广度方向」有料，「修正幅度」没料

拆解 W32 的 10 条，按机制族归纳：

| 机制族 | 代表 | S 区间 | 结论 |
|---|---|---:|---|
| **广度不对称/方向**（raised vs lowered 家数比） | W32-7 O0Agpdr7 | **1.13** | ★ **全波最强**，F 0.83 / sub_u 0.93 / dd 0.1046 三项都是高质地 |
| 广度水平（多指标 raised 家数叠加） | W32-2 VkxepQ7M | 0.75 | **2Y 1.31 全波最高**，但 S 不足 |
| 广度双确认（推荐 × 预期） | W32-9 YP1Yp35R | 0.58 | sub_u 0.73，可用作辅助腿 |
| **修正幅度**（rank 现值 − rank 历史） | W32-5 2rAe7VOP | 0.43 | **无料** — 与 `analyst_factor_signals` 的 `estimate_change_3mo` 不同，快照差分在 DEU 无效 |
| 修正/分歧比 | W32-8 gJeL1NQg | 0.63 | 2Y −0.35，方向不稳 |
| **水平类**（推荐评级均值、覆盖度） | W32-4 / W32-6 | 0.09 / 0.16 | **无料** — 水平量在 DEU 已第 N 次证伪 |
| 盈利惊喜 SUE | W32-3 0mY57Zw2 | 0.09 | **无料** — DEU 无 PEAD |
| 跨指标修正背离（营收−EBIT） | W32-10 wpQWR7Zx | −0.11 | **无料** — 利润率修正方向不成立 |

⇒ **本数据集唯一的信号通道是「分析师广度的方向与不对称」，不是「修正幅度」也不是「水平」。**
这与 `analyst_factor_signals`（唯一通道 = `estimate_change_3mo` 修正幅度）**在机制上完全正交**，
证实 `analyst7` 不是重复数据集。

### 判据 J：S 与 2Y 在 `analyst7` 内部由**不同字段族**分别供给（可配对）

| 角色 | 字段族 | 最佳件 | S | 2Y |
|---|---|---|---:|---:|
| **S 提供者** | 广度不对称 `_lowerednum / _raisednum` | O0Agpdr7 | **1.13** | 0.13 |
| **2Y 提供者** | 广度水平叠加 `Σ raisednum` | VkxepQ7M | 0.75 | **1.31** |

两者在 S 与 2Y 上**完全互补**（S 差 0.38、2Y 差 1.18）。
这正是论坛骨架「慢分量撑 S、快分量撑 2Y」所需要的一对腿 ⇒ 直接构成 Wave 34。

### 判据 K：`act_q_*_surprisemean`（SUE）在 DEU 无 PEAD

W32-3 用教科书式 SUE（`divide(surprisemean, add(0.001, surprisestd))`）得 S **0.09** / F 0.02 / sub_u −0.13。
`act_q_ebi_surprise*` 未测但同族。⇒ **德国 TOP500 的盈余公告后漂移已被套利干净**，SUE 族封盘，不再投 slot。

---

## Wave 33 — `analyst7` 论坛骨架跨指标 10 对（FAST / decay 0 / sector）

批次 `4cDq7GcIK5iLarVCmPi7lTX`。

统一骨架（5 算子）：
```
group_rank(add(ts_zscore(<慢指标>_mean, 240), ts_zscore(subtract(<快指标>_mean, <快指标>_mean_4wks_ago), 44)), sector)
```

| # | 慢指标（水平撑 S） | 快指标（动量撑 2Y） | 快腿 cov |
|---|---|---|---:|
| W33-1 | `ebi`（论坛 V4 原版，**校准用**） | `ebt` | 0.7003 |
| W33-2 | `pre` | `gps` | 0.6845 |
| W33-3 | `gps` | `pre` | 0.7066 |
| W33-4 | `dps` | `roa` | 0.6092 |
| W33-5 | `roa` | `grm` | 0.5902 |
| W33-6 | `nav` | `cps` | 0.6808 |
| W33-7 | `ent` | `dps` | 0.7086 |
| W33-8 | `ebi` | `nav` | 0.6755 |
| W33-9 | `ebt` | `ent` | 0.6542 |
| W33-10 | `pre` | `cps` | 0.6808 |

**W33-1 是校准探针**：原版表达式 + 原版设置。若复现 S≈1.73 / 2Y≈1.77 ⇒ 论坛骨架在本平台当前状态有效，
可按 W33-2~10 换冷门字段降 PC；若不复现 ⇒ 帖子已失效（作者原话承认「结论绑定本数据集+本区域+本时间」）。

### 结果：★★★ 骨架复现成功，且产出 RA 全闸通过件 `1YN0dw7R`

| # | 慢指标 | 快指标 | alpha | S | F | 2Y | TO | sub_u | drawdown | failed |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|
| **W33-1** | **ebi** | **ebt** | **1YN0dw7R** | **2.03** | **1.26** | **2.00** | 0.2512 | **1.15** | **0.0459** | **0** |
| W33-2 | pre | gps | e75E0z0J | 1.88 | 1.12 | 1.06 | 0.2467 | 1.05 | 0.0539 | 1 |
| W33-3 | gps | pre | zq3emkm8 | 1.74 | 0.99 | 0.95 | 0.2480 | 1.00 | 0.0863 | 2 |
| W33-8 | ebi | nav | P0oK37Gw | 1.28 | 0.62 | 0.81 | 0.2447 | 0.63 | 0.0588 | 3 |
| W33-10 | pre | cps | E56xElG9 | 1.22 | 0.58 | 1.08 | 0.2475 | 0.58 | 0.0692 | 3 |
| W33-9 | ebt | ent | pwd3ljNv | 1.12 | 0.49 | 0.72 | 0.2858 | 0.72 | 0.0692 | 3 |
| W33-5 | roa | grm | JjerO7vO | 1.03 | 0.46 | 0.43 | 0.2543 | 0.58 | 0.0676 | 3 |
| W33-4 | dps | roa | RREP871j | 1.03 | 0.44 | **−1.13** | 0.2552 | 0.55 | 0.1206 | 3 |
| W33-7 | ent | dps | QPv6V7GX | 0.56 | 0.18 | 0.55 | 0.2573 | 0.47 | 0.1120 | 3 |
| W33-6 | nav | cps | mLoQbjVW | 0.34 | 0.08 | 0.11 | 0.2481 | −0.01 | 0.1238 | 4 |

### ★★★ 判据 L：论坛骨架在 DEU 完全复现，且比原帖更好

| 指标 | 论坛 V4 原文 | 本战役实测 `1YN0dw7R` | 差异 |
|---|---:|---:|---|
| Sharpe | 1.73 | **2.03** | **+0.30** |
| Fitness | 1.43 | 1.26 | −0.17 |
| 2Y | 1.77 | **2.00** | **+0.23** |
| Turnover | 未报 | 0.2512 | — |
| PC | 0.685 | **0.704** | +0.019（卡墙） |
| SC | 0.387 | **0.2925** | **−0.095（更好）** |
| max drawdown | 未报 | **0.0459** | **全战役最低** |
| failed_ra | 通过 | **0** | 一致 |

⇒ 帖子虽写「结论绑定本数据集+本区域+本时间」，**两个月后在同区仍然成立**，是本战役唯一可复现的外部骨架。
**注意 S 与 2Y 双双高于原帖，但 PC 反而略升** —— 与帖子自述「PC 与 Sharpe/Fitness 强负相关」一致。

### ★★★ 判据 M：慢腿必须 `ebi`、快腿必须 `ebt`，这个配对是**唯一**同时过 S 与 2Y 的

拆 W33 的高 S 三条（S≥1.58）：

| 慢腿 | 快腿 | S | 2Y | 判定 |
|---|---|---:|---:|---|
| **ebi** | **ebt** | **2.03** | **2.00** | **✓ 双过** |
| pre | gps | 1.88 | 1.06 | ✗ 2Y 差 0.52 |
| gps | pre | 1.74 | 0.95 | ✗ 2Y 差 0.63 |

⇒ **S 高的配对不只一个，但 2Y 只有 ebi/ebt 这一对能过。**
两者不可互换（pre→gps 与 gps→pre 都高 S、都低 2Y，说明这不是「方向」问题而是**特定指标组合**问题）。
机理猜测：`ebi`（EBIT）与 `ebt`（税前利润）在德国会计口径下几乎同源但加工阶段不同
（EBIT 在税前利润之前、不含利息与少数股东项），恰好满足「共享经济源头 + 不同加工阶段」，
与本战役 Wave 27 推出的 bucket 轴三重条件同构。

### 判据 N：换手 0.25 是骨架固有属性（decay=0 的直接后果），但仍远在 0.7 上限内

10 条全部落在 **TO 0.2447–0.2858**（带宽仅 0.041），与慢/快腿选哪个指标几乎无关。
⇒ TO 由 `decay=0` 决定，不由字段决定。相对本战役既有件（TO 0.03–0.16）高 2–8 倍，但 0.25 << 0.7 上限，
且 `1YN0dw7R` 的 margin 0.000774 仍为正、drawdown 0.0459 极低 ⇒ 高换手在这里是**有效换手**。

### `1YN0dw7R` 全闸实测

```text
1YN0dw7R  group_rank(add(ts_zscore(est_12m_ebi_mean, 240),
                          ts_zscore(subtract(est_12m_ebt_mean, est_12m_ebt_mean_4wks_ago), 44)), sector)
设置：DEU / TOP500 / delay1 / **FAST** / **decay 0** / trunc 0.08 / SUBINDUSTRY 不适用
```

| 闸 | 值 | 阈值 | 判定 |
|---|---:|---|---|
| Sharpe | 2.03 | ≥1.58 | ✓ |
| Fitness | 1.26 | ≥1.0 | ✓ |
| 2Y Sharpe | **2.00** | ≥1.58 | ✓ |
| Turnover | 0.2512 | 0.01–0.7 | ✓ |
| sub_universe_sharpe | 1.15 | ≥0.474×2.03=0.962 | ✓ |
| margin | 0.000774 | >0 | ✓ |
| drawdown | 0.0459 | — | 全战役最低 |
| investability_sharpe | 1.73 | — | 高可投资性 |
| failed_ra | **0** | =0 | ✓ |
| **self correlation** | **0.2925** | <0.7 | **✓** |
| **prod correlation** | **0.7040** | <0.7 | **✗ 差 0.004** |

self 池 top：2rOe10qY 0.2925 / 58gkLAkk 0.2824 / 883Y3bAW 0.2794 / 2rjrMZ25 0.2694 / Vk65zLzG 0.2450；
pool_size 13 / full_os_pool_size 14。

prod 直方图（`[0.5,0.6)` 24 / `[0.6,0.7)` **1** / `[0.7,0.8)` **1**）⇒ **浅钉，单钉子 max 0.704**。

### 判据 O：prod 0.704 属「浅钉可救」而非「深钉判死」

按用户 2026-11-02 纠正的 prod triage 口径：`[0.7,0.8)` 桶 **n=1 且 max<0.75** ⇒ **不得判死**，
须先归因再定向破墙。本条 n=1、max=0.704，完全落在可救区间。
（`wq-window-valley-break-prod-wall` skill 的「n≥1 必死」判据是 KOR 16/16 实证，且 skill 自注「禁外推，换区必须重测」，
DEU 未验 ⇒ 不能直接套用判死。）

**归因**：钉子挂在「慢腿 ebi 水平」与「快腿 ebt 4 周修正」的组合持仓时间结构上，TO 0.2512。
**破墙路径（按「只动 prod 不动 2Y」优先序）**：
1. **窗口网格**（skill 指定唯一只动 prod 的旋钮）：慢 240→{220,252,264}、快 44→{36,40,48,52,60,66}
2. 标准化器替换 `ts_zscore → ts_rank`
3. 指标对轮换（但已知只有 ebi/ebt 能过 2Y，空间窄）

→ 已派 Wave 35 覆盖 1+2。

---

## 待收割

- Wave 32 指标表（本文件待补）
- Wave 33 指标表（本文件待补）
