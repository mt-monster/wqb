# DEU × Analyst 战役报告：未点亮塔的合规前沿与 2Y 墙

**日期**：2026-10-13　**区域**：DEU / TOP500 / delay=1　**类别**：ANALYST（未点亮塔）　**数据集**：`analyst_factor_signals`
**结论摘要**：**产出 1 颗全闸通过的 ANALYST alpha = `9qWX78vV`**（S1.65 / F1.47 / 2Y1.69 / self 0.3014 ✅ / prod 0.6197 ✅ / `failed_ra_count=0`）。
**★ 关键转折**：自造 40 条结构全部卡 2Y（≤1.17）；改用 **2026-10-07 战役已验证的 DEU A 级框架**后，2Y 直接到 **1.69** ⇒ **墙是「结构」不是「字段」**。

---

## ★ 重大更新（本报告最重要的部分）

我最初用 `group_rank(F, sector)` 一类的自定义结构测了 40 条，2Y 全部 ≤1.17，误判「2Y 不可破」。
随后在仓库历史产物 `output_report/DEU_gem_templates_after_skeleton_audit.md` 找到 **2026-10-07 已过闸的 A 级框架**：

```
group_neutralize(rank(add(ts_mean(bf(F), 1), ts_mean(bf(F), 210))),
                 bucket(rank(ts_mean(bf(F), 252)), range="0,1,0.05"))      bf(F)=ts_backfill(F, 1008)
```

**同一字段、同一设置，只换结构**：

| 结构 | S | F | 2Y | sub | 判定 |
|---|---|---|---|---|---|
| `group_rank(eps_y1_estimate_change_3mo, sector)` | 1.81 | 1.61 | 1.12 | — | 卡 2Y |
| `ts_mean(...,22)` / `tvr_decay` 等 40 条自定义 | ≤1.81 | ≤1.61 | **≤1.17** | — | 卡 2Y |
| **A 级框架（双窗 1/210 + 单桶轴）** | **1.65** | **1.47** | **1.69** | 0.78 | ✅ **全过** |

**⇒ 结论改写：`analyst_factor_signals` 的 2Y 完全可达（1.69），此前 40 条的失败是「结构选择错误」而非结构墙。**
**A 级框架的三要素**（缺一不可）：① `bf=ts_backfill(F,1008)`；② 双窗 `add(ts_mean(bf,1), ts_mean(bf,210))`（**短腿必须=1**）；③ `bucket(rank(ts_mean(bf,252)), range="0,1,0.05")` 作分组轴。

---

## 0. 前置纠错（本轮最重要的工程教训）

**事故**：我据 `alphas` 台账 `dataset_id` 把 `zqbVMkv1` 判为 **shortinterest3** 的胜绩，并据此向用户推荐 ShortInterest 方向。
**实测推翻**（`get_alpha_details`）：

```
zqbVMkv1 = winsorize(group_rank(ts_target_tvr_decay(multiply(
             rank(ts_delta(divide(fnd6_newq_oiadpq,fnd6_newq_seqq),240)),
             rank(ts_delta(divide(fnd6_newq_oiadpq,fnd6_newq_seqq),176))),
             target_tvr=0.05),sector),std=4)
```
⇒ 字段是 `fnd6_newq_oiadpq` / `fnd6_newq_seqq` ⇒ **fundamental6**，与 shortinterest3 无关。
且 `shortinterest3` 在 `alphas`（dataset_id=1137）下 **0 条**。

**铁律强化（第三次同类事故）**：`alphas.dataset_id` 归因**不可信**（同「台账 code 可能是配方标签」）⇒ **任何 alpha 的归属/机制结论，引用前必须 `get_alpha_details` 核 `regular.code`。**

---

## 1. DEU 全量普查：合规前沿的真实形状

**普查口径**：DEU 台账 1968 条 alpha（1 ACTIVE / 649 COMPLETE / 1318 UNSUBMITTED）。

| 事实 | 证据 |
|---|---|
| S≥1.58 共 **389 条**，高分候选**绝大多数是多腿 `add(rank(A),rank(B),…)` 混信号** | `grtransform` R83、`lean_le89` R89、`sentiment27` R87/R90、`sentiment7` R100~R102 |
| 这些混信号 **RA 层能过**（平台不校验「禁混信号」）但 **prod 全撞 0.72–0.79** | `1Yx0k6XX` prod .7496；`6XrNXg67` .7542；`wpYWGW76` .7252 |
| 唯一 ACTIVE = `blRnKEk6`，仍是 **4 腿 add + `CH_PPA`/`PowerPoolSelected`** | S2.02/F1.70/2Y2.74/prod .5766 —— **PPA 产物，非 RA 合规路径** |
| **唯一合规全闸过的 REGULAR** = `Wje5K71x`（fundamental6） | S1.73/F1.37/2Y1.87/TO.1269/self.1879/**prod 0.4305** |

**⇒ 未点亮塔（analyst/news/insiders/pv/earnings/sentiment/risk/option/macro/socialmedia/shortinterest/imbalance）逐一核查**：

| 未点亮类别 | 单信号实证 | 裁决 |
|---|---|---|
| `sentiment`（sentiment27/7） | 单信号探针 S 仅 **0.45–0.63**（高分全来自违规 4~5 腿组合） | **排除** |
| `shortinterest`（shortinterest3） | 合规单信号 **S≈0.73 或为负**（`min_loan_rate_main` −0.74；费率/拥挤度族已族级否证） | **排除** |
| `insiders`（insider_agg_matrix） | 单信号 0 条；1.86 全来自多腿 | **排除** |
| `risk`（risk60） | 费率/crowding 族已 DEFINITIVE 判死 | **排除** |
| `pv`（pattern_scores） | DEU maxS 0.42 | **排除** |
| `news` | 换手墙（全 DEU 换手爆表率最高 1.1%） | **排除** |
| **`analyst`（analyst_factor_signals）** | 已有**合规单信号 S1.90 / F1.70** 实证（`d51Yw0Yv`） | **✅ 唯一入选** |

---

## 2. 目标数据集：`analyst_factor_signals`（ANALYST，未点亮）

- **字段面**（108 个 MATRIX，实测覆盖率**远高于**注册表记的 0.60）：主字段 cov **0.89–0.93**
  `{eps|netprofit|revenue}_y1_estimate_change_3mo`(0.923)｜`*_y1_estimate_skewness`(0.927)｜`*_revision_magnitude`(0.922)｜`*_y1_estimate_coeff_var`(0.892)｜`*_y1_cagr_2yr`(0.79–0.80)｜`*_y1_consensus_value`(0.89)｜`*_y1_estimate_asymmetry`(0.886)
  ⇒ **~20 个字段 cov≥0.88**，为 DEU 未点亮塔中最好的字段面。
- **历史锚**：`d51Yw0Yv` = `tail(winsorize(group_rank(eps_y1_estimate_change_3mo,sector),std=2),lower=0.25,upper=0.75,newval=0)` → S1.90/F1.70，**卡 sub 0.86（限0.90）+ 2Y 0.94（限1.58）**。
- **与 `analyst93` 的本质区别**：an93 是**分析师技能元数据**（准确率/一致性，换手 0.019–0.029 ⇒ `DEAD_STATIC`）；本集是**预期修订量**（前瞻）⇒ **an93 的「判死」不适用**。

**回测设置**：DEU / TOP500 / D1 / SUBINDUSTRY / decay 4 / trunc 0.08 / **nanHandling ON**（对齐 `d51Yw0Yv`、`zqbVMkv1` 先例）。
**合规性**：全部为**单信号**表达式（无 `add` 多腿），符合「禁混信号」。

---

## 3. 实测：4 批 × 10 条 = 40 条合规单信号

### 批 W-ANL1（字段面 / 基础结构，`1P4WalgDz4AX8Mo2FVtlgey`）

| 表达式 | S | F | TO | 2Y |
|---|---|---|---|---|
| **`group_rank(eps_y1_estimate_change_3mo, sector)`** | **1.81** | **1.61** | .0751 | 1.12 |
| `group_rank(eps_y1_estimate_change_3mo, industry)` | 1.69 | 1.40 | .0794 | 0.92 |
| `group_rank(ts_mean(eps_y1_estimate_change_3mo,22), sector)` | 1.69 | 1.46 | .0453 | **1.17** |
| `group_rank(netprofit_y1_estimate_change_3mo, sector)` | 1.57 | 1.29 | .0768 | 0.76 |
| `group_rank(eps_revision_magnitude, sector)` | 0.97 | 0.61 | .0796 | 0.58 |
| 双窗级联 `multiply(rank(ts_delta(f,240)),rank(ts_delta(f,176)))` | **0.91** | 0.57 | .0749 | 0.68 |
| 同上（netprofit） | 0.83 | 0.49 | .0760 | 0.54 |
| `group_rank(eps_y1_estimate_coeff_var, sector)` | 0.56 | 0.30 | .0468 | 0.27 |
| `group_rank(eps_y1_estimate_skewness, sector)` | 0.40 | 0.15 | .1008 | −0.86 |
| `group_rank(revenue_y1_estimate_skewness, sector)` | −0.08 | −0.01 | .0953 | −1.29 |

### 批 W-ANL2（拉长 horizon / 长窗平滑，`K401K1Nz4Aa9dKunLW6VFN`）

| 表达式 | S | F | TO | 2Y |
|---|---|---|---|---|
| `group_rank(ts_mean(eps_y1_estimate_change_3mo,22), subindustry)` | 1.61 | 1.25 | .0405 | 1.16 |
| `group_rank(ts_mean(eps_y1_estimate_change_3mo,66), sector)` | 1.61 | 1.37 | .0354 | 1.01 |
| `group_rank(netprofit_y2_estimate_change_3mo, sector)` | 1.41 | 1.15 | .0783 | 1.04 |
| `group_rank(eps_y2_estimate_change_3mo, sector)` | 1.35 | 1.09 | .0773 | 0.96 |
| `group_rank(multiply(rank(change),rank(consensus_value)), sector)` | 1.30 | 1.00 | .0600 | 0.79 |
| `group_rank(ts_mean(...,252), sector)` | 0.90 | 0.57 | .0249 | 0.54 |
| `group_rank(revenue_y2_estimate_change_3mo, sector)` | 0.80 | 0.50 | .0812 | 0.58 |
| `group_rank(eps_y1_cagr_2yr, sector)` | 0.31 | 0.11 | .0258 | 0.43 |
| `group_rank(revenue_y1_cagr_2yr, sector)` | −0.03 | NA | .0258 | −0.62 |
| `subtract(rank(y2_change),rank(y1_change))` horizon gap | −0.02 | NA | .1112 | 0.03 |

### 批 W-ANL3（2Y 专攻：归一化 / 轴 / 平滑算子，`1AXqj09pT4yOcgdkgYRgrpd`）

| 表达式 | S | F | TO | 2Y |
|---|---|---|---|---|
| `winsorize(group_rank(eps_y1_estimate_change_3mo,sector),std=4)` | **1.81** | **1.61** | .0751 | 1.12 |
| `group_rank(eps_y1_estimate_change_3mo, market)` | 1.77 | 1.58 | .0684 | 1.12 |
| `group_rank(ts_mean(...,22), industry)` | 1.64 | 1.34 | .0471 | 1.05 |
| `group_rank(ts_mean(netprofit_...,22), sector)` | 1.62 | 1.35 | .0459 | 1.01 |
| `group_rank(ts_decay_linear(...,66), sector)` | 1.61 | 1.37 | .0375 | 1.07 |
| `group_rank(ts_target_tvr_decay(...,target_tvr=0.05), sector)` | 1.55 | 1.27 | .0492 | **1.17** |
| `group_zscore(..., sector)` | 1.17 | 1.09 | .0901 | 0.70 |
| `group_rank(ts_rank(...,252), sector)` | 1.04 | 0.66 | .1026 | 0.52 |
| `group_rank(ts_zscore(...,252), sector)` | 0.96 | 0.58 | .0857 | 0.49 |
| `subtract(rank(y1_change),rank(y2_change))` | 0.53 | 0.24 | .1116 | 0.12 |

### 批 W-ANL4（累积 / 双窗差分，五层配方迁移）

| 表达式 | S | F | TO | 2Y |
|---|---|---|---|---|
| `group_rank(ts_sum(eps_y1_estimate_change_3mo,126), sector)` | **1.29** | 1.00 | .0282 | 0.62 |
| `group_rank(multiply(rank(ts_sum(f,240)),rank(ts_sum(f,176))), sector)` | 0.86 | 0.54 | .0249 | 0.40 |
| `group_rank(ts_sum(netprofit_y1_estimate_change_3mo,252), sector)` | 0.76 | 0.44 | .0233 | 0.63 |
| `group_rank(ts_sum(eps_y1_estimate_change_3mo,252), sector)` | 0.64 | 0.34 | .0229 | 0.38 |
| `group_rank(ts_delta(ts_sum(f,252),252), sector)` | 0.58 | 0.29 | .0268 | **1.13** |
| `group_rank(ts_mean(ts_sum(f,252),66), sector)` | 0.34 | 0.13 | .0214 | 0.04 |
| `group_rank(ts_sum(eps_revision_magnitude,252), sector)` | 0.30 | 0.11 | .0239 | −0.12 |
| `group_rank(subtract(ts_sum(f,252),ts_sum(f,66)), sector)` 双窗差分 | 0.24 | 0.08 | .0252 | −0.18 |
| `group_rank(ts_sum(f,504), sector)` | 0.15 | 0.04 | .0199 | −0.23 |
| `group_rank(ts_sum(revenue_y1_estimate_change_3mo,252), sector)` | 0.08 | 0.02 | .0235 | −0.14 |

**批 W-ANL4 结论**：**`ts_sum` 累积迁移同样失败**（max S 1.29）——累积把信号抹平成低 TO 低 S 的慢变量。
`ts_delta(ts_sum(...,252),252)` 是本批唯一 2Y 上 1.1 的（1.13）但 S 只剩 0.58。
⇒ **five-layer 配方（累积→双窗差分）在本族 100% 不可移植。**

**★ 全局最优（40 条中的 2Y 极值）**：`max 2Y = 1.17`（`P0MJZMdp` / `mLYPm6KW`），**距门槛 1.58 差 0.41**。

---

## 4. 核心结论

### ★★ 结论 1：`analyst_factor_signals` 的 S/F 轻松过线，**2Y 是唯一硬墙**
- 最佳形态只用 **1 个算子 + 1 个字段**：`group_rank(eps_y1_estimate_change_3mo, sector)` → **S 1.81 / F 1.61 / TO 0.0751**。
- **30 条结构全部 2Y ≤ 1.17**（需 1.58）。
- `winsorize(std=4)` 与基座**逐位相同**（1.81/1.61）⇒ 再次实证「**保序变换不改排序、不改门槛指标**」。

### ★★ 结论 2：`ts_delta` 双窗级联在本族**第三次崩塌**（0.91 / 0.83）
- `*_estimate_change_3mo` 是**变化率**（已是差分），再差分 = 二阶噪声。
- ⇒ **铁律再确认**：**双窗级联只对「水平量」有效；对「率/变化类」字段崩**。fundamental6 的看家配方**不可移植**到 analyst 修订族。
- 反向验证：`ts_sum`（累积，把变化率还原成准水平量）是唯一理论可行的迁移方向 → 见批 W-ANL4。

### ★ 结论 3：`group_rank` 是本族的 S/2Y 承重项
- 换 `group_zscore`：S 1.81 → 1.17、2Y 1.12 → 0.70。（与 USD analyst16 实证同向：丢 group_rank ⇒ S 虚高或 2Y 崩。）
- 轴序：`sector` ≈ `market`（1.81/1.77）> `industry`（1.69）> `subindustry`（1.61）。
- `ts_rank(252)` / `ts_zscore(252)` 长窗自标准化 **大幅削 S**（1.04 / 0.96）⇒ 不适用。

### ★ 结论 4：horizon 拉长（FY2 / CAGR）**反而变差**
`eps_y2_change` 1.35 < `eps_y1_change` 1.81；`cagr_2yr` 0.31 / −0.03。⇒ 本族信息集中在 **FY1 的 3 个月修订**。

---

## 5. A 级框架 × 字段 全扫（批 W-ANL5/6）

### 批 W-ANL5（`1kJiUl7Lj4A4awb8nurItc3`）— 框架 × 10 字段

| 字段 | S | F | 2Y | 判定 |
|---|---|---|---|---|
| **`eps_y1_estimate_change_3mo`** | **1.65** | **1.47** | **1.69** | ✅ **全闸（`9qWX78vV`）** |
| `netprofit_y1_estimate_change_3mo` | 1.33 | 1.05 | 1.39 | ❌ S |
| `eps_y2_estimate_change_3mo` | 1.24 | 0.98 | 1.35 | ❌ S |
| `netprofit_y2_estimate_change_3mo` | 1.17 | 0.89 | 1.12 | ❌ S |
| `revenue_y1_estimate_change_3mo` | 1.02 | 0.71 | 0.84 | ❌ |
| `revenue_y2_estimate_change_3mo` | 0.75 | 0.46 | 0.64 | ❌ |
| `netprofit_q1_estimate_change_1mo` | 0.60 | 0.26 | 0.43 | ❌ |
| `eps_revision_magnitude` | 0.50 | 0.24 | 0.26 | ❌ |
| `revenue_q1_estimate_change_1mo` | 0.35 | 0.11 | −0.19 | ❌ |
| `eps_q1_estimate_change_1mo` | 0.23 | 0.06 | −0.70 | ❌ |

**⇒ 框架可迁移（2Y 全部 ≥0.26、多条 ≥1.35），但只有 `eps_y1_estimate_change_3mo` 同时满足 S≥1.58。**

### 批 W-ANL6（混合结构：框架 2Y 机制 + `group_rank` 载重）

对 runner-up（netprofit_y1 1.33 / eps_y2 1.24）试：`group_neutralize(group_rank(add(ts_mean(bf,1),ts_mean(bf,210)),sector), bucket(...))`
＋纯框架的窗/桶粒度微调（w1=3、w2=240、gran=0.1）。

| 结构 | 字段 | S | F | 2Y |
|---|---|---|---|---|
| **HYBRID** | `eps_y1_estimate_change_3mo` | **1.77** | **1.61** | **1.83** |
| HYBRID | `netprofit_y1_estimate_change_3mo` | 1.36 | 1.07 | 1.34 |
| framework | `netprofit_y1_estimate_change_3mo` (w2=240) | 1.30 | 1.01 | 1.35 |
| HYBRID | `eps_y2_estimate_change_3mo` | 1.30 | 1.03 | 1.38 |
| framework | `netprofit_y1_estimate_change_3mo` (gran 0.1) | 1.29 | 1.00 | 1.37 |
| framework | `eps_y2_estimate_change_3mo` (w2=240) | 1.26 | 1.00 | 1.40 |
| framework | `netprofit_y1_estimate_change_3mo` (w1=3) | 1.23 | 0.93 | 1.47 |
| framework | `eps_y2_estimate_change_3mo` (w1=3) | 1.17 | 0.89 | 1.46 |
| HYBRID | `netprofit_y2_estimate_change_3mo` | 1.08 | 0.78 | 1.30 |
| HYBRID | `revenue_y1_estimate_change_3mo` | 1.01 | 0.69 | 0.77 |

**★★ 突破**：**HYBRID 结构**（`group_rank` 载重 + `bucket` 轴）在 `eps_y1_estimate_change_3mo` 上拿到
**S 1.77 / F 1.61 / 2Y 1.83** —— 同时**优于**纯框架（1.65/1.47/1.69）与纯 `group_rank`（1.81/1.61/1.12 但 2Y 挂）。
```
group_neutralize(group_rank(add(ts_mean(bf, 1), ts_mean(bf, 210)), sector),
                 bucket(rank(ts_mean(bf, 252)), range="0,1,0.05"))      bf=ts_backfill(F,1008)
```
`failed_ra_count=0`、全闸 PASS；**prod 0.651 ✅ / self 0.3437 ✅** ⇒ `WjLEOqLP`。

**但 runner-up 全部止步 S 1.36**（框架/混合/窗调 gran 调均无法把 netprofit_y1 / eps_y2 推过 1.58）。

---

## 5b. 跨类别验证：把 A 级框架/HYBRID 搬到其它类别的 19 个字段

批 W-ANL7（`1THbBy3eh4xnb2rNlgZGXsw`）— HYBRID × 10 个跨类别字段：

| 字段（数据集／类别） | S | F | 2Y | 判定 |
|---|---|---|---|---|
| `snl27_relpopularity1`（sentiment27／sentiment） | 0.64 | 0.33 | 0.96 | ❌ |
| `snl27_totaldomains`（sentiment27） | 0.46 | 0.19 | 0.77 | ❌ |
| `stable_boundary_trade_count_21d_active`（fund_holdings_panel／institutions） | 0.44 | 0.09 | 0.75 | ❌ |
| `event_sentiment_score`（news18／news） | 0.23 | 0.05 | 0.34 | ❌ |
| `count_institutional_buyers_security`（institutions6／institutions） | 0.02 | NA | 0.45 | ❌ |
| `loaned_share_count_main`（shortinterest3） | **−0.18** | −0.05 | −1.22 | ❌ 反向 |
| `loaned_market_value_usd_main`（shortinterest3） | −0.34 | −0.12 | −0.28 | ❌ |
| `transaction_count_main`（shortinterest3） | −0.35 | −0.12 | −0.37 | ❌ |
| `loan_rate_volatility_main`（shortinterest3） | −0.44 | −0.14 | −0.38 | ❌ |
| `lending_fee_bid_rate`（risk60／risk） | **−0.52** | −0.22 | −0.24 | ❌ 反向 |

**⇒ 全部 |S| ≤0.64 ⇒ 框架/ HYBRID 无法救活这些类别。**
**⇒ 再次实证**：① 借券费率/活动族在 DEU **无信号或反向**（−0.18~−0.52）；② 零售关注度（sentiment27）0.64 为跨类别最优但仍远不及格；③ 「零竞争」不等于有信号。

批 W-ANL8（`cache/wDEU_crosscat_g8.txt`）— 剩余未测概念（institutions6 卖出家数 / 增持市值、fhp Herfindahl、model28 违约距离、model53 PD 短端、model36 杠杆分、other47 自然流量、sentiment27 top50 排名、risk60 crowding）：
| 字段（数据集／类别） | S | F | 2Y |
|---|---|---|---|
| `credit_risk_leverage_score_d1`（model36／model） | 0.53 | 0.28 | 0.59 |
| `mdl28_sm_structural_credit_structural_distance_to_default`（model28） | 0.29 | 0.13 | 0.51 |
| `market_value_institutional_shares_acquired`（institutions6） | 0.24 | 0.07 | 0.62 |
| `snl27_top50pctranking`（sentiment27） | 0.08 | 0.01 | 0.79 |
| `rsk60_crowding`（risk60／risk） | −0.05 | NA | 0.59 |
| `oth47_organic_traffic`（other47／other） | −0.12 | −0.03 | 0.52 |
| `annualized_pd_1_month_jc7`（model53） | −0.16 | −0.05 | −0.65 |
| `herfindahl_index_transactions`（fund_holdings_panel） | −0.17 | −0.02 | −0.30 |
| `count_institutional_sellers_security`（institutions6） | −0.50 | −0.22 | 0.03 |

**⇒ 全部 |S| ≤0.53 ⇒ 跨类别 19 个字段（19 概念模板库的未测部分）无一可用。**

### 全轮汇总（8 波 79 条合规表达式）

| 波 | 内容 | max S | max 2Y | 出闸 |
|---|---|---|---|---|
| WANL1 | 自造结构 × 字段 | 1.81 | 1.17 | 0（2Y） |
| WANL2 | 长 horizon / 平滑 | 1.61 | 1.16 | 0（2Y） |
| WANL3 | 2Y 专攻（归一化/轴/算子） | 1.81 | 1.17 | 0（2Y） |
| WANL4 | 累积 / 双窗差分 | 1.29 | 1.13 | 0 |
| **WANL5** | **A 级框架 × 10 字段** | 1.65 | **1.69** | **1（`9qWX78vV`）** |
| **WANL6** | **HYBRID × 变体** | **1.77** | **1.83** | **1（`WjLEOqLP`）** |
| WANL7 | HYBRID × 10 跨类别字段 | 0.64 | 0.96 | 0 |
| WANL8 | HYBRID × 9 剩余概念 | 0.53 | 0.79 | 0 |

**⇒ DEU 全域的可提交产出，本轮只来自 `analyst_factor_signals` 的单一字段 `eps_y1_estimate_change_3mo`。**

### 批 W-ANL12（`2PQtapayi555b1v97jVP3f2`）— 最后一片未测面：`pattern_scores` 504 个零竞争字段

**为什么值得测**：`pattern_scores`（PV，未点亮塔）有 **504 个 MATRIX 字段、覆盖率 1.0、alphaCount = 0**（全平台零竞争），
且历史只用**自造结构**测过 15 条（max S 0.42）——**从未用过 A 级框架**。另加 `insider_agg_matrix.directional_indicator`（cov 1.0）与 `risk88.alternative_market_cap_usd`（cov 1.0）。

| 字段（类别） | S | 2Y |
|---|---|---|
| `mean_similarity_rising_wedge` | 0.09 | −0.57 |
| `median_similarity_reversal_v_bottom` | 0.08 | 0.40 |
| `alternative_market_cap_usd`（risk88） | −0.03 | 0.37 |
| `max_similarity_sym_triangle_downward` | −0.08 | −0.17 |
| `directional_indicator`（insider） | −0.10 | 0.17 |
| `max_similarity_common_gap_downward` | −0.17 | 0.35 |
| `dynamic_similarity_falling_wedge` | −0.18 | 0.34 |
| `max_similarity_falling_wedge`（HYBRID） | −0.27 | 0.26 |
| `v_shape_reversal_top_std_similarity_40d` | −0.30 | 0.07 |
| `max_similarity_falling_wedge`（纯框架） | −0.31 | 0.19 |

**⇒ 全部 |S| ≤ 0.09。**
**⇒ 连同换手异常（TO 0.21–0.36，图表形态相似度天然高频变动），`pattern_scores` 在 DEU 判死**（零竞争 ≠ 有信号，第二次实证）。
**⇒ `insider_agg_matrix` / `risk88` 的 cov=1.0 字段同样无信号。**

**★ 本轮总计：DEU 103 条合规表达式、12 个批次，max S = 1.81；可提交产出 = 1 颗。**

---

## 5c. 合规性质疑与「无 add」消融实验（2026-10-13 用户质疑后补充）

**质疑**：`WjLEOqLP` 里有 `add(ts_mean(bf,1), ts_mean(bf,210))`，是否属于被禁的 `add(A,B)` 混信号？

**判定：不违规。** 规则原文是「禁止**两条独立信号腿**相加：加权(0.4A+0.6B)、等权 `add(rank(A),rank(B))`、中缀 `+`；
第二个数据集只以条件/分组/残差入场」。本式的两个腿是**同一个字段** `eps_y1_estimate_change_3mo` 的 **1 日窗 + 210 日窗**，
没有任何第二个字段/数据集/机制 ⇒ 属「**单信号结构化**」（多窗口平滑），不是混信号。
对照真违规的 `blRnKEk6`：add 了 **4 个字段、3 个数据集**（`mean_loan_rate_main`+`predicted_surprise_*`+`mean_estimate_change_pct_*`）。

**消融实验（批 W-ANL9，把 `add` 全部去掉，只留单窗口）**：

| 核心（不含 add） | S | F | 2Y |
|---|---|---|---|
| **含 add：`add(ts_mean(bf,1), ts_mean(bf,210))`** | **1.77** | **1.61** | **1.83** |
| `bf` / `ts_mean(bf,1)`（短腿单窗） | 1.56 | 1.29 | 1.18 |
| `ts_decay_linear(bf,210)` | 1.40 | 1.13 | 1.20 |
| `ts_mean(bf,66)` | 1.37 | 1.07 | 1.22 |
| `ts_mean(bf,105)` | 1.26 | 0.95 | 0.78 |
| `ts_mean(bf,210)`（长腿单窗） | 0.97 | 0.65 | 0.29 |

**⇒ 去掉 `add` 后最好只有 S1.56 / 2Y1.22，全部不过闸。**
**⇒ 210 日长腿单独用是 0.97（几乎无效），1 日短腿单独用是 1.56；两者相加得 1.77 / 2Y 1.83 ⇒ 是真正的多窗口互补增益，不是两个独立信号叠加。**
**⇒ 结论：A 级框架的双窗 `add` 是同一字段的多窗口结构化，合规且是承重结构，不可删。**

---

## 6. 状态与最终判定



### ★ 全闸通过候选（2 颗，但**互斥 ⇒ 实际可提交 1 颗**）

| Alpha | 结构 | S | F | TO | 2Y | sub | self | prod |
|---|---|---|---|---|---|---|---|---|
| **`WjLEOqLP`** | HYBRID | **1.77** | **1.61** | .1199 | **1.83** | 0.88 | **0.3437** ✅ | **0.6510** ✅ |
| `9qWX78vV` | 纯框架 | 1.65 | 1.47 | .1182 | 1.69 | 0.78 | **0.3014** ✅ | **0.6197** ✅ |

**★★ 两者同腿（均为 `eps_y1_estimate_change_3mo`）⇒ 互相关系数 0.9372（>0.7）⇒ 只能提交其一。**
（平台 self 只对已提交 OS 池计算，故先提一颗后另一颗的 self 会跳到 ~0.94 而被拒。）

**建议提交 `WjLEOqLP`**（指标全面更强），**但需注意 prod 余量仅 0.049**（0.651 vs 0.7），
而 prod 会逐日漂移（既有实证：`zqbVMkv1` 一夜 0.4116→0.8527）⇒ **提交当日必须 `check_correlation(refresh=True)` 复核**。
若当日 WjLEOqLP 的 prod 漂过 0.7，则退回 `9qWX78vV`（prod 余量 0.080，更稳）。

### Analyst 类别的量产边界（本轮 + 2026-10-07 战役共同结论）

| 数据集 | 结论 |
|---|---|
| `analyst_factor_signals` | **只有 `eps_y1_estimate_change_3mo` 过线**（同族 9 个 change 字段最好 S1.36）；`revision_magnitude`/`coeff_var`/`skewness`/`cagr`/`consensus_value` 全弱 |
| `analyst7`（608 字段） | 画像最优 `est_12m_net_raisednum_1mth` S1.18/2Y0.28；高 2Y 全是计数类（S≈0）⇒ 无门槛候选 |
| `analyst93` | S 天花板 1.31（4 结构 × 5 轴已穷尽） |
| `analyst44`/`analyst9`/`analyst48`/`analyst47` | 元数据 / 计数 / 时间戳族，DEAD |

**⇒ Analyst 在 DEU 的可提交上限 = 1 颗**（与 2026-10-07 战役「≈205 次测试 → 0 颗可提交」相比，本轮靠 **A 级框架**首次过闸）。
**⇒ 跨类别已实测（批 W-ANL7/8，19 字段 19 概念）：全部 |S| ≤0.64 ⇒ 换类别在本轮同样出不了货。**
**⇒ DEU 当前唯一现实产出 = ANALYST 1 颗（`WjLEOqLP`）；要凑 10 颗必须引入新数据源或新区域。**

### 提交预检结果（`submit_verdict`）
| Alpha | verdict | failed_ra | failed_ppa | sim_fails | prod | self |
|---|---|---|---|---|---|---|
| `WjLEOqLP` | **UNVERIFIABLE**（非 BLOCKED，404 死端点） | **0** | **0** | **[]** | **0.651** ✅ | **0.344** ✅ |

⇒ **模拟层零 FAIL、双端点全过 ⇒ 满足放行条件（prod<0.7 + 用户确认）**。
**⚠ 唯一未做项**：`robustness_<alpha_id>` 台账未落（`submit_verdict` 提示「未跑 brain-alpha-robustness 则先跑」，不拦截）；
`tools/direct_submit.py` 是 fail-closed，无该台账会拒提交 ⇒ **真提交前需先跑稳健性审计**。

### 本轮方法论沉淀（最重要）
1. **墙常在「结构」不在「字段」**：自造 40 条结构全灭（2Y≤1.17）；换用已验证框架后同字段 2Y=1.83。**开新战场前必须先检索仓库内历史战役产物**（`output_report/DEU_*`、skill 的 win_recipes）。
2. **A 级框架三要素缺一不可**：`bf=ts_backfill(F,1008)` → 双窗 `add(ts_mean(bf,1),ts_mean(bf,210))`（**短腿=1**）→ `bucket(rank(ts_mean(bf,252)), range="0,1,0.05")` 作分组轴。
3. **HYBRID 变体**（把框架的 `rank` 换成 `group_rank(..., sector)`）= 当前最强形态，同时拿到 S 与 2Y。
4. `ts_delta` 双窗级联**只对水平量有效**，对变化率字段连续三次崩塌（本轮 0.91/0.83）；`ts_sum` 累积迁移同样失败。

---

## 6. 产物

| 类型 | 路径 |
|---|---|
| 表达式（批 1–4） | `cache/wDEU_anlfs_g1..g4.txt` |
| 台账 | `backtest_results` wave = `WANL1`~`WANL4`（region=DEU） |
| skill 沉淀 | `wq-brain-ra-deu/references/analyst.md`、`shortinterest.md` |
| 记忆 | `.workbuddy/memory/2026-10-13.md` |
