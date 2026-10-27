# 稳健性审计报告 · 2026-10-20

> 技能：`brain-alpha-robustness`（Phase B 归因 → Phase C 反过拟合闸 → Phase D 回写）。
> 阈值来源：`references/techniques.md`（2026-04-22 论坛共识台账），**不因当日论坛内容改变**。
> 本日候选 1 颗：EUR `YPxg1LzM`（EUR ATOM analyst 战役的唯一存活候选）。

---

## EUR · `YPxg1LzM` — CONDITIONAL（无硬 REJECT 触发；3 项 CONDITIONAL + 5 项软标记）

### B.1 规范信息与顶层指标（`get_alpha_details`）

```
group_neutralize(signed_power(group_zscore(netprofit_y2_estimate_change_3mo, industry), 1.8), market)
```

| 项 | 值 | 项 | 值 |
|---|---|---|---|
| status / stage | `UNSUBMITTED` / `IS` | universe / delay | **TOP2500** / 1 |
| neutralization / decay | **FAST** / 20 | truncation | 0.08 |
| 窗口 / 模式 | 2014-01-01→2023-12-31 / **FULL** | language | FASTEXPR |
| Sharpe / Fitness | **1.73** / **1.54** | turnover | 0.0687 |
| returns / drawdown | 0.0995 / 0.064 | margin | 0.002898（**28.98 bp**） |
| long / short | 1469 / 1350（**多头倾斜 1.088**） | pnl | 10 269 828 |
| `sub_universe_sharpe` | **0.90**（限 0.8989） | `two_year_sharpe` | **2.09** |
| `ra.failed_ra_count` | **0** | `ra.failed_ppa_count` | **0** |
| `pyramid_short` | `analyst` | pyramids | effective **1**，`EUR/D1/ANALYST` ×1.3 |

`checks.pass`（8）：`LOW_SHARPE` `LOW_FITNESS` `LOW_TURNOVER` `HIGH_TURNOVER` `CONCENTRATED_WEIGHT` `LOW_SUB_UNIVERSE_SHARPE` `LOW_2Y_SHARPE` `MATCHES_PYRAMID`
`checks.warning`（3）：`CLUSTER_TEST` 1.32/1.58（分类性，非阻断）、`MATCHES_THEMES`、`OSMOSIS_ALLOCATION`
`checks.pending`（6）：`SELF_CORRELATION` `DATA_DIVERSITY` `PROD_CORRELATION` `REGULAR_SUBMISSION` `POWER_POOL_CORRELATION` `MATCHES_THEMES`

⚠ **`IS_LADDER_SHARPE` 不出现在任何一列** ⇒ 活体确认 ATOM 替代机制：平台文档 `single-dataset-alphas` 载明
单数据集 alpha「**instead of** the IS Ladder Sharpe Pass/Fail criteria」只跑 2 年平均 IS Sharpe 线（D1 = 2.38，TO<30% 时 ×0.85 = **2.023**）。
V5 的 2Y = **2.09 ≥ 2.023**，余量 **+0.067**。

### B.2 逐年归因（`get_alpha_yearly_stats`，10 个 IS 年全量）

| 年 | pnl | Sharpe | Fitness | returns | DD | margin | TO | long/short | L/S 比 |
|---|---:|---:|---:|---:|---:|---:|---:|---|---:|
| 2014 | 1 596 960 | **3.40** | 3.77 | .1536 | .0273 | .003931 | .0781 | 1342/1277 | 1.051 |
| 2015 | 1 107 076 | 1.90 | 1.75 | .1064 | .0385 | .003190 | .0667 | 1403/1324 | 1.060 |
| 2016 | **4 538** | **0.01** | 0.00 | .0004 | .0613 | .000013 | .0667 | 1523/1201 | 1.268 |
| 2017 | 805 816 | 1.47 | 1.16 | .0775 | .0249 | .002327 | .0666 | 1477/1477 | 1.000 |
| 2018 | 1 257 111 | 2.40 | 2.36 | .1209 | .0317 | .003700 | .0653 | 1525/1406 | 1.085 |
| 2019 | 701 159 | 1.33 | 0.98 | .0674 | .0311 | .002035 | .0663 | 1691/1142 | **1.481** |
| 2020 | **−205 381** | **−0.30** | −0.12 | −.0215 | .0631 | −.000624 | .0688 | 1398/1368 | 1.022 |
| 2021 | **2 203 844** | **3.65** | **4.75** | .2119 | .0239 | .006341 | .0668 | 1380/**1587** | **0.870** |
| 2022 | 2 040 486 | **2.88** | 3.61 | .1962 | .0640 | .005347 | .0734 | 1510/1398 | 1.080 |
| 2023 | 758 090 | **1.22** | 0.93 | .0729 | .0419 | .002143 | .0680 | 1435/1325 | 1.083 |

逐年 pnl 合计 **10 269 699**，与顶层 10 269 828 差 129（0.001%，日频聚合舍入）⇒ 数据自洽。

**分布读数**：均值 1.796｜中位数 1.685｜样本 std 1.3249（CV **0.738**）｜总体 std 1.2570（CV **0.6998**）
高于 1.58 提交线的年份 = **5/10**（2014/2015/2018/2021/2022）｜低于 1.0 的年份 = **2/10**（2016、2020）

**★ 三项结构性发现（本报告的实质贡献，Phase C 表内没有对应格）**

1. **PnL 高度集中**：top-1 年（2021）= **21.5%**｜top-2 年（2021+2022）= **41.3%**｜top-3 年（+2014）= **56.9%**。
   即 **30% 的年份贡献了 57% 的 PnL**。
2. **★ ATOM 2Y 通过是*单年依赖*，且盈亏平衡余量只有 +0.054**：平台 2Y ≈ 两年 Sharpe 均值（实测 (2.88+1.22)/2 = 2.05 vs 平台 2.09）。
   解 `(x + 1.22)/2 = 2.023` ⇒ **x = 2.826**。2022 的实际读数是 **2.88** ⇒
   **只要 2022 低 0.054 个 Sharpe，ATOM 2Y 闸就翻红**。若 2022 落在样本中位数 1.685，2Y ≈ **1.45**，
   同时击穿 ATOM 线（−0.57）与 `LOW_2Y_SHARPE`（−0.13）。
3. **★ 2021 是 10 年里*唯一*的空头倾斜年（L/S 0.870），同时也是最好的一年（S 3.65 / F 4.75）**；
   其余 9 年全部多头倾斜（1.000–1.481）。⇒ **最佳年的收益来自与其余样本相反的账面取向**，
   这是**取向层面的结构性不稳定**，不只是水平漂移。

**换手稳定性（正面证据）**：TO 逐年 .0653–.0781，全距仅 0.0128 ⇒ **无换手制度变化**，
不是「某几年靠暴增换手做出来的 Sharpe」。回撤方面最大年 DD 0.0640 = 全期 DD，
`2× 全期均值` 阈值 = 0.128，**无任何年份触发**。

### B.3 回撤日历 / 换手×margin / 集中度（`get_alpha_pnl` 的替代口径）

- **换手 × margin（论坛 LJ46725 噪声拟合线：TO>60% 且 margin<3bp）**：TO **6.87%**、margin **28.98 bp** ⇒ **不触发**，且两项都远离阈值。
- **Top-5 个股集中度**：**不可测** —— `get_alpha_pnl` 返回日频聚合，平台尚未提供逐股分解（技能 Phase B.3 已注明「逐股 PnL 可得时」）。
  以平台 `CONCENTRATED_WEIGHT` = **PASS**（单票权重 < 0.1）为准，本项不单独判定。
- **回撤日历**：以年粒度替代季粒度，见 B.2 末段 ⇒ **PASS**。

### B.4 相关性（`check_correlation`，本战役内 `refresh=True` 实测）

| 项 | 值 | 线 | 判定 |
|---|---:|---:|---|
| **prod** | **0.7398** | < 0.70 | **✗ 超 0.0398** |
| prod 直方图 `[0.7,0.8)` 桶 | **n = 3**（V3 / V5 / V7） | `wq-window-valley-break-prod-wall`：n ≥ 1 必死 | **族级判死** |
| self | 未测（同族互相关见下） | < 0.70 | — |

同族/同字段互相关（`compute_mutual_correlation`，本地零槽位、1021 点、4 年、`missing_pnl []`）：
V5 × W3（同字段 `netprofit_y2`，不同 p）= **0.9938**｜V5 × V3 = **0.9986**｜V5 × X3(np_y1) = 0.4720｜V5 × X5(eps_y1) = 0.3874｜V5 × Z6(`analyst10` sales) = **0.0458**。

⇒ **prod 是本候选唯一的硬阻断项，且已代数证明不可修**（`netprofit_y2` 族的四闸交集为空：
S≥1.58⇒p≤2.111｜2Y≥2.023⇒p≤1.991｜比率≥0.51961⇒p≥1.962｜prod<0.7⇒p≥2.146，**prod 要求的区间与前三闸不相交**）。
唯一残余路径是平台「Sharpe 比在位相关 alpha 高 ≥10%」豁免条款（V5 的 1.73 对任何 S ≤ 1.573 的在位者成立），
而**该条款只能用一次不可逆提交验证**（在位者身份与 Sharpe 在 API 上不可读：`get_record_sets` 无相关性记录集、`PROD_CORRELATION` 恒 `pending`）。

### B.5 相对池贡献（`performance_comparison`，分区 `EQUITY:EUR:1:POWER_POOL`）

| 指标 | before（池） | after（+V5） | Δ | 判读 |
|---|---:|---:|---:|---|
| **Sharpe** | **3.17** | **3.13** | **−0.04（−1.3%）** | **边际为负 ⇒ 软标记** |
| **Fitness** | 2.01 | **2.17** | **+0.16（+8.0%）** | 正贡献 |
| returns | .0502 | .0601 | +.0099 | 正 |
| drawdown | .0200 | **.0184** | −.0016 | 正（回撤变浅） |
| turnover | .1123 | .1036 | −.0087 | 正（换手变低） |
| pnl | 5 178 385 | 6 196 648 | +1 018 263 | 正 |
| long / short | 685 / 782 | 842 / 895 | +157 / +113 | 持仓数扩张 |

⇒ **6 项里 5 项为正、唯 Sharpe 边际为负（−0.04）**。这是「加进去让池更分散、更稳、但单单位风险的收益略降」的典型形态，
按 Phase C「边际贡献为负是软标记，写进报告交用户终审」处置 ⇒ **软标记，不 REJECT**。

### Phase C — 反过拟合闸逐项判定

| 检查项 | V5 读数 | 判定 |
|---|---|---|
| WebDataScope failed count | `failed_ra` **0**、`failed_ppa` **0**、`checks.fail` **[]**、无名单内 `PENDING` | **PASS** |
| **Recent-3yr Sharpe（主判定）** | 2021/2022/2023 = 3.65 / 2.88 / 1.22；3 年均值 **2.583 ≥ 1.58**；三年每年 > 0.3 | **PASS** |
| Recent-3yr CV_Sharpe | 样本 std/mean = 1.2419/2.5833 = **0.481**（总体口径 **0.393**） | **CONDITIONAL**（0.40–0.60 带；跨在 0.40 边界，取保守口径） |
| 衰减比 | 1.22 / 1.73 = **0.705** | **PASS**（≥ 0.50） |
| 平年（仅最近 3 年） | **0** | **PASS** |
| Recent-3yr max/min | 3.65 / 1.22 = **2.99** | **PASS**（≤ 3，**贴线**） |
| 全历史早年疲软（CV / 字形 / max-min） | 全史 CV **0.70**；2016 S **0.01**、2020 S **−0.30**；max/min 3.65/−0.30；**双峰字形**（峰在 2014 与 2021，非厂字形） | **软标记**（表内明示**绝不 REJECT**） |
| Sub-universe | 平台 `LOW_SUB_UNIVERSE_SHARPE` = **PASS**，但 0.90 vs 限 **0.8989** = 余量 **+0.0011** | **CONDITIONAL**（贴线） |
| 算子数 | **3**（`group_zscore` / `signed_power` / `group_neutralize`） | **PASS**（软标记线 > 5） |
| Margin @ turnover | **28.98 bp** @ TO **6.87%** | **PASS**（≥ 5 bp；且远离「>60% 且 <3bp」噪声线） |
| Top-5 个股集中度 | 逐股 PnL 不可得；平台 `CONCENTRATED_WEIGHT` = PASS | **不可测**，以平台闸为准 |
| 经济可解释性 | 一句话可写：「分析师对未来 2 年净利润共识预期的 3 个月渐进上修，市场对其反应不足」 | **PASS** |

**硬 REJECT 触发数 = 0** ⇒ 不 REJECT。**CONDITIONAL 项 = 3**（CV_Sharpe、sub 贴线、Recent-3yr max/min 贴线）。

### ⚠ 判定的重要限定：近窗制度在本候选上**恰好把两个制度年都包进了窗口**

Phase C 的主判定用「最近 3 个 IS 年」（用户指令 2026-06-20，理由：要求 10 年全强过严会杀死活信号）。
本候选的最近 3 年是 **2021 / 2022 / 2023**，其中 **2021（3.65）与 2022（2.88）正是全样本的两个峰**。
⇒ **「Recent-3yr PASS」是窗口选择的产物，不构成稳健性证据。** 三条独立证据说明这一点：

1. **10 年里只有 5 年高于 1.58 提交线**，2 年基本为零或为负（2016 S 0.01、2020 S −0.30）。
2. **57% 的 PnL 来自 3 个年份**（B.2 发现 1）。
3. **ATOM 2Y 闸的通过依赖 2022 单年，盈亏平衡余量 +0.054**（B.2 发现 2）。

**⇒ OS（2024+）的理性中心估计 = 1.2–1.5**，取自三个互相独立的口径：
最近一个非峰年 2023 = **1.22**｜剔除 2021+2022 两个峰年后其余 8 年均值 = **1.429**｜全样本中位数 = **1.685**。
**三者中两者低于 1.58 提交线。** 这与本战役档案 §38.4 的一阶过拟合警报一致，
但**现在有了 V5 自身的逐年证据**（此前只有同族兄弟腿 `1YjzoEGm` / `Grge67NZ` 的旁证，其 2022/2023 = 2.88/1.22 与 2.75/1.23）。

**这条限定不改变 Phase C 的三态判定**（表内明示全历史疲软绝不 REJECT），但**必须在用户确认提交前如实呈现**，
因为它意味着「过了闸 ⇒ 可提交」在 OS 期望上高估约 **0.5–0.9 个 Sharpe**。

### 最终判定

**CONDITIONAL** — 无硬 REJECT；`failed_checks = []`；8 项软标记（见台账 `soft_flags`）。

**下游含义**：
- 按技能契约，`submit_verdict` 读到 `CONDITIONAL` **不改判**，只在 `next_step` 提示「先 repair 并重审（≤2 轮）再请用户确认」。
- **但本候选的实际阻断项不是稳健性，是 prod 0.7398**（B.4），且已代数证明族内不可修。
- **`brain-alpha-repair` 轮换在本例无意义**：3 项 CONDITIONAL 全是「贴线」形态（0.481 / +0.0011 / 2.99），
  而任何抬高 sub 余量的杠杆（ finer 分组、更高 p）都已实测同时压低 S 与 2Y（战役档案 §39.1 粒度定律、§39.2 四闸交集为空）。
  ⇒ **修复通道在本候选上是封闭的，不是「还没试」。**
- **不建议提交**：唯一路径是 prod 豁免条款的不可逆验证，而 OS 中心估计 1.2–1.5 低于提交线 ⇒
  **即使豁免通过、提交成功，OS 大概率不达标并被 DECOMMISSION**。这是本报告的终审意见，交用户裁决。

### 数据取自（可复现）

```
mcp__wq-brain-http__get_alpha_details(alpha_id="YPxg1LzM")
mcp__wq-brain-http__get_alpha_yearly_stats(alpha_id="YPxg1LzM")
mcp__wq-brain-http__performance_comparison(alpha_id="YPxg1LzM")   # 分区 EQUITY:EUR:1:POWER_POOL
mcp__wq-brain-http__check_correlation(alpha_id="YPxg1LzM", refresh=True)   # 本战役内实测 prod 0.7398
mcp__wq-brain-http__compute_mutual_correlation([...6 腿...])      # 本地零槽位，1021 点 / 4 年
```

`performance_comparison` 完整输出（220 279 字符，超 25 000 token 上限被自动持久化）：
`…\4e5d9d69-0b67-44d3-8578-a581857e0132\tool-results\wq_brain_http_performance_comparison_1a208d1698d2.txt`
战役完整证据链（§38.4 制度年警报、§39.2 四闸代数、§40.7 去相关矩阵、§40.13 算术终局）：
`docs/reference/EUR/eur_analyst_field_profile_20261018.md`

---

# 候选二：AD1 `LL5dmv9a`（EUR / analyst7 / `dps` 四周修正 ÷ 分歧度）

**判定：PASS（带软标记）** — 本战役首个 `failed_ra_count = 0` 的全闸通过 ATOM 候选。
与本文件候选一（V5）的根本差别：V5 是 **prod-bound**（prod 0.7398 ✗，其余全过）；
AD1 是 **S/F-bound**（prod 余量 0.203，S 余量仅 0.13）。⇒ 约束几何反转，
后续优化只许推 S 与 returns，**禁止再动任何 prod 杠杆**（抬 decay / hump / tail / 更细笛卡尔分组）。

## B.0　WebDataScope failed-count 门

| 项 | 读数 | 判定 |
|---|---|---|
| Failed RA | **0** | PASS |
| Failed PPA | **0** | PASS |
| `checks.fail` | `[]` | — |
| `checks.warning` | `CLUSTER_TEST 1.28/1.58`（分类型、非阻断）、`MATCHES_THEMES`、`OSMOSIS_ALLOCATION` | 非 RA 项 |
| `checks.pending` | SELF / DATA_DIVERSITY / PROD / REGULAR_SUBMISSION / POWER_POOL / MATCHES_THEMES | 均为相关性 / 提交类，B.4 直接实测 |

## B.0a　体检硬门 — ⚠ **未生效（协议缺口，fail-open，如实登记）**

```
$ tools/field_inspect_gate.py --region EUR --dataset analyst7 --exprs-file logs/_tmp_ad1_expr.txt
[inspect] 体检硬门未生效（EUR/analyst7）
          体检包缺失或为空：tracking\mining\field_inspect_eur_analyst7.json
EXIT=0
```

现存 EUR 体检包含 `analyst9 / analyst11 / analyst14 / analyst16 / analyst_factor_signals`，**不含 `analyst7`**。
**根因**：本战役全部批次经 `batch_create_simulations` 直发，从未走 `tools/wave_gate.py` / RA 步 5，
⇒ B.0a 对**任何一腿**都未执行过。闸退出码 0（fail-open）故不阻断，
但「低覆盖 / 厚尾 / 稀疏事件」的预处理约束**无人把关**。
补建需要 WebDataScope 数据包：`python tools/webdata_quality.py --zip <包> --export-expr tracking/mining/field_inspect_eur_analyst7.json`。
**不得据此声称本闸通过。**

## B.1　规范信息（`get_alpha_details` / `get_user_alphas`）

- 表达式：`group_neutralize(signed_power(group_zscore(divide(subtract(est_12m_dps_mean, est_12m_dps_mean_4wks_ago), est_12m_dps_std), subindustry), 1.4), market)`
- 数据集：`analyst7`（Broker Estimates，1111 MATRIX 字段，αC 3101，coverage 0.50）；字段 3 个，**同数据集 ⇒ ATOM 合规**
- 设置：EUR / TOP2500 / D1 / FAST / **decay 40** / trunc 0.08 / maxTrade ON / nanHandling ON / pasteurization ON / unitHandling VERIFY / 2014-01-01→2023-12-31 / FULL
- 指标：S **1.71**（线 1.58，余量 +8.2%，**绑定闸**）｜F **1.02**（线 1.0，+5.0%，**次绑定**）｜2Y **2.41**｜sub_universe_sharpe **0.95**（ratio 0.556，线 0.5196，+7.0%）｜returns .0449｜TO .0522｜DD **.0450**（全战役最低）｜margin **17.21 bp**｜pnl 4 634 507｜L/S 1388/1431
- `checks.pass` = LOW_SHARPE, LOW_FITNESS, LOW_TURNOVER, HIGH_TURNOVER, CONCENTRATED_WEIGHT, LOW_SUB_UNIVERSE_SHARPE, **LOW_2Y_SHARPE**, MATCHES_PYRAMID；`fail` = `[]`
- ⚠ `IS_LADDER_SHARPE` **不在任何一张名单** ⇒ ATOM 的「2Y cutoff 替代 IS Ladder」条款在平台侧确实生效
- ⚠ `LOW_ROBUST_UNIVERSE_SHARPE` **不在 pass / warning / fail 任何一张名单** ⇒ **平台未发出该检查项，无法核实**（登记为软标记，不推断其结果）
- 金字塔：`{effective 1, [EUR/D1/ANALYST, multiplier 1.3]}`，`MATCHES_PYRAMID ∈ pass`

## B.2　逐年归因（近窗制度：最近 3 个 IS 年 = 2021 / 2022 / 2023）

| 年 | pnl | Sharpe | returns | DD | margin | TO | L/S | Fitness |
|---|---:|---:|---:|---:|---:|---:|---|---:|
| 2014 | 767 301 | **3.38** | .0738 | .0141 | .002373 | .0622 | 1225/1394 | 2.60 |
| 2015 | 470 004 | 1.59 | .0452 | .0210 | .001765 | .0512 | 1362/1364 | 0.96 |
| 2016 | 120 928 | **0.44** | .0116 | .0215 | .000459 | .0507 | 1361/1363 | 0.13 |
| 2017 | 499 599 | 2.45 | .0480 | .0070 | .001889 | .0509 | 1408/1546 | 1.52 |
| 2018 | 161 901 | **0.65** | .0156 | .0162 | .000609 | .0512 | 1500/1431 | 0.23 |
| 2019 | 450 630 | 1.71 | .0433 | .0194 | .001711 | .0506 | 1500/1333 | 1.01 |
| 2020 | **−143 650** | **−0.48** | −.0150 | .0439 | −.00055 | .0547 | 1477/1289 | −0.17 |
| 2021 | **902 862** | **3.18** | .0868 | .0132 | .003452 | .0503 | 1373/1593 | 2.65 |
| 2022 | 795 497 | 2.41 | .0765 | .0144 | .00298 | .0513 | 1368/1540 | 1.89 |
| 2023 | 609 711 | 2.45 | .0586 | .0119 | .002386 | .0491 | 1313/1448 | 1.68 |

**主判定（Recent-3yr）**

| 检查 | 读数 | 线 | 判定 |
|---|---:|---:|---|
| Recent-3yr Sharpe | 3.18 / 2.41 / 2.45，均值 **2.68** | ≥ 1.58 且每年 > 0.3 | **PASS（余量极大）** |
| Recent-3yr CV_Sharpe | **0.162**（样本）/ **0.132**（总体） | < 0.40 | **PASS**（V5 为 0.481 / 0.393 ⇒ AD1 稳定约 3 倍） |
| 衰减比 = 末年 / 全期 | 2.45 / 1.71 = **1.433** | ≥ 0.50 | **PASS**（V5 为 0.705）；> 1 ⇒ **完全无衰减**，近年强于全期 |
| 平年（\|S\| < 0.3） | **0** | 0 | **PASS** |
| Recent-3yr max/min | 3.18 / 2.41 = **1.32** | ≤ 3 | **PASS**（V5 为 2.99） |

**全历史（仅软标记，绝不据此 REJECT）**：均值 1.778｜中位数 2.06｜CV **0.702**（样本）/ **0.666**（总体）｜
**9/10 年为正**（仅 2020 负），无平年。软标记来源 = 早年疲软（2016 S 0.44、2018 S 0.65、2020 S −0.48）。

**§42.4 / §42.10 提案格的实测结果（仍属技能层提案，需人审）**

- **PnL 年度集中度**：top-1 **19.5%**｜top-2 **36.6%**｜top-3 **53.2%**（V5：21.5 / 41.3 / **56.9**）
  ⇒ 三项均优于 V5；集中度因子 **1.77×**（V5 1.90×）。⚠ top-3 仍过半，
  但 AD1 的 top-3 含 **2021 与 2022**（前向加权），不是靠早年遗产撑起来的。
- **最优年的 book 朝向**（§42.10 第二提案格）：2021 L/S = 1373/1593 = **0.862**；
  其余九年 L/S = 0.879（2014）/ 0.999 / 0.999 / 0.911 / 1.048 / 1.125 / 1.146 / 0.888 / 0.907，
  区间 **[0.879, 1.146]** ⇒ **0.862 落在区间外（低于下界 0.017）⇒ 该格 FIRES**。
  ⚠ **更正**：本报告初稿口算曾判为「落在区间内、该格不触发」，逐值复算后**证伪**。
  合并候选三（AE2，2021 L/S 0.833 vs 其余区间 [0.9125, 1.1066]）后，
  **V5 / AD1 / AE2 三例全部触发**，且三例的最优年都是 **2021**
  ⇒ **该格检出的是 EUR 2021 的制度性空头倾斜（book 普遍偏空），不是某个 alpha 的过拟合签名**
  ⇒ **§42.10 该提案格在本数据集上无判别力，不予采纳**（这是对该提案的实证否证）。

## B.3　PnL / 回撤 / 换手归因

- **回撤日历**：全期 DD **.0450** ⇒ 2× 阈值 **.0900**；逐年最大 DD = **.0439**（2020，即唯一负年）< .0900
  ⇒ **无任一季触发**。（V5 全期 DD .0640 ⇒ 阈值 .128；AD1 低 30%。）
- **换手 × margin**：TO **5.22%** ≪ 60% ⇒ 论坛 LJ46725 的「TO > 60% 且 margin < 3 bp = 噪声拟合」规则**未触发**；
  margin **17.21 bp** 同时越过 3 bp 论坛线与 10 bp 内部严线（`GATES_INTERNAL.margin_bp_min`）。
- **Top-5 个股集中度：不可测**。`get_alpha_pnl` 返回 `properties: ["date","pnl"]`（2579 条、`downsampled: true`），
  **无逐股分解** ⇒ 以平台 `CONCENTRATED_WEIGHT ∈ pass`（limit 0.1）替代，与候选一同一处置；
  符合技能「逐股 PnL 可得时」的可选条款。**不推断个股集中度数值。**
- **PnL 曲线形态**（降采样序列）：近单调上行 0 → 4 634 783；可见回撤段
  2015-01→2015-04（791 468→715 792）、2016-02→2016-03（1 271 508→1 151 931），
  最大一段 **2020-02-27 2 730 003 → 2020-12-23 2 341 778（−388 k）**；此后 2021→2023 无中断上行。

## B.4　相关性（`check_correlation(refresh=True)`，非缓存实测）

| 项 | 读数 | 线 | 判定 |
|---|---:|---:|---|
| **prod** | **max_correlation 0.497**，`passes_check true` | 0.7 | **PASS，余量 0.203（全战役最宽）** |
| prod 直方图 | 最高非零桶 `[0.3,0.4] n=16991`、`[0.4,0.5] n=75`；**`[0.7,0.8)` 桶不存在 ⇒ n = 0** | n ≥ 1 即族死 | **族级可救**（按 `wq-window-valley-break-prod-wall` 判据） |
| prod min | −0.4716 | — | — |
| **self** | **max 0.17063**，`passes_check true` | 0.7 | **PASS，余量 0.529** |
| self top | `gJj1nxLM` 0.1706｜`78jdv6b1` 0.1223｜`Wj71Q12o` −0.1217｜`Wj7g2gAx` −0.1733 | — | — |
| 池 | `pool_size 4`｜`full_os_pool_size 6`｜`excluded_power_pool_count 2`｜`ppac_ids_cached 2` | — | — |
| 汇总 | **`all_passed: true`** | — | — |

**族内旁证**：AC7 `zqrR22VE` prod **0.4203**、AC3 `9qE7dM1e` prod **0.4232** ⇒
三腿（三分组轴 / 两 decay / 两 p）全落 0.42–0.50 ⇒ **低 prod 是 `analyst7` 的数据集级属性，不是 AD1 的偶发**。

## B.5　相对池贡献 — **未执行（如实登记）**

`performance_comparison` 单次输出约 73 k token（超 25 000 上限会被自动持久化），
且其结论在本技能里**只产生软标记、不改判定**（候选一已实测过，形态为 Sharpe −1.3% 软标记）。
本轮为控制预算**未对 AD1 / AE2 执行**；若用户要在提交前补齐，命令为
`mcp__wq-brain-http__performance_comparison(alpha_id="LL5dmv9a")`（分区 `EQUITY:EUR:1:POWER_POOL`）。

## Phase C　反过拟合闸

| 检查项 | 读数 | 判定 |
|---|---|---|
| WebDataScope failed count | Failed RA 0 / PPA 0，RA 名单内无 PENDING | **PASS** |
| **Recent-3yr Sharpe（主判定）** | 均值 2.68 ≥ 1.58，三年全正 | **PASS** |
| Recent-3yr CV_Sharpe | 0.162 < 0.40 | **PASS** |
| 衰减比 | 1.433 ≥ 0.50 | **PASS** |
| 平年（近 3 年） | 0 | **PASS** |
| Recent-3yr max/min | 1.32 ≤ 3 | **PASS** |
| 全历史早年疲软 | CV 0.702、2016/2018/2020 疲软 | **软标记（绝不 REJECT）** |
| Sub-universe | 平台 `LOW_SUB_UNIVERSE_SHARPE ∈ pass`（0.95 / ratio 0.556 vs 线 0.5196） | **PASS** |
| 算子数 | **5**（`group_neutralize` `signed_power` `group_zscore` `divide` `subtract`）—— 在边界上、**不 > 5** | 无软标记；PPA 上限 8 亦满足 |
| Margin @ turnover | 17.21 bp @ TO 5.22% | **PASS** |
| Top-5 个股集中度 | 不可测；以 `CONCENTRATED_WEIGHT ∈ pass` 替代 | **PASS（替代口径）** |
| 经济可解释性 | 一句话可写（见下） | **PASS** |

**经济解释（一句话）**：分析师对 12 个月前瞻每股派息（DPS）一致预期的四周修正，
按横截面分歧度（分析师预测标准差）归一化——市场对「分歧收窄后的上调」反应不足，
因此在子行业内部比较时能捕捉到未被定价的修正动量。

**硬标记 0 项 / 软标记 1 项（闸内）⇒ 判定 PASS。**

## 最终判定

**PASS（带软标记）** — `failed_checks = []`，无硬 REJECT 触发项。

**软标记清单（须带进提交前的三段式 description，供一年后 OS 复盘）**

1. 全历史早年疲软：2016 S 0.44、2018 S 0.65、2020 S −0.48；全历史 CV 0.702（样本）/ 0.666（总体）。
2. **B.0a 体检硬门未生效** —— `tracking/mining/field_inspect_eur_analyst7.json` 缺失；本战役全部批次直发，未经 `wave_gate`。
3. **Top-5 个股集中度不可测** —— `get_alpha_pnl` 无逐股分解；以平台 `CONCENTRATED_WEIGHT` 替代。
4. **`LOW_ROBUST_UNIVERSE_SHARPE` 无法核实** —— 平台未在三张名单中发出该检查项。
5. **B.5 `performance_comparison` 未执行**（软标记项，不改判定）。
6. **returns .0449 < 0.05** —— 低于 EUR profile「升 active」的 returns 触发线；
   ⚠ 该区域级条件由**同族其它腿**满足（AB1 .0549 / AC1 .0546 / AC2 .0531 / AC6 .0612 / AC7 .0528），
   **AD1 自身不满足**。如实分开记，不挪用。
7. **最优年（2021）book 朝向 0.862 落在其余九年区间 [0.879, 1.146] 之外** —— 与 V5 / AE2 同形态，
   属 EUR 2021 制度性空头倾斜，非本 alpha 特有。

**下游含义**

- 按技能契约，`submit_verdict` 读到 `PASS` **不改判、不加提示**（对比候选一的 `CONDITIONAL` 会提示先 repair）。
- ⚠ **`submit_verdict` 在本环境永远不会返回 PASS**：`GET /alphas/{id}/submit` 是死端点（实测返回
  `UNVERIFIABLE` / `reason_code UNVERIFIABLE_404` / `submit_layer_view "dead_endpoint_404"`）。
  **不要把 `UNVERIFIABLE` 读成「差一点」**；放行权威恒为「prod 实测 < 0.7 + 用户明确确认 + `confirm_submit=True`」。
- ⚠ **`checks.warning` 里的 `MATCHES_THEMES` 命中的是 GLB 主题**（实测 `54blOMB`「GLB/D1 TOPDIV3000 Theme」打在 EUR alpha 上）
  ⇒ 该警告**不区分区域**，**不得**当作 Phase E 的 PPA 主题证据。
- ⛔ **本报告不构成提交授权**。提交是不可逆动作，须用户明确确认。

## 数据取自（可复现）

```
mcp__wq-brain-http__get_alpha_details(alpha_id="LL5dmv9a")
mcp__wq-brain-http__get_alpha_yearly_stats(alpha_id="LL5dmv9a")
mcp__wq-brain-http__get_alpha_pnl(alpha_id="LL5dmv9a")            # 2579 条，properties 仅 ["date","pnl"]
mcp__wq-brain-http__check_correlation(alpha_id="LL5dmv9a", refresh=True)   # prod 0.497 / self 0.17063 / all_passed true
mcp__wq-brain-http__compute_mutual_correlation([...5 腿...])       # 本地零槽位，1021 点 / 4 年
tools/field_inspect_gate.py --region EUR --dataset analyst7 --exprs-file logs/_tmp_ad1_expr.txt   # EXIT=0，体检包缺失
```

---

# 候选三：AE2 `e76xGOQO`（EUR / analyst7 / `ebt` = **EBITDA** 四周修正 ÷ 分歧度）

> ⚠ **口径更正（2026-10-20，字段名机器核验）**：`est_12m_ebt_*` 的 catalog 描述是
> **"Mean analyst estimate of EBITDA regarding the next 4 quarters"** ⇒ `ebt` = **EBITDA（息税折旧摊销前利润）**，
> 不是「税前利润」。同族易混字段的正确映射：`ebi` = EBIT · **`ebt` = EBITDA** · `pre` = pre-tax profit ·
> `prr` = pretax profit as reported · `ner` = net profit as reported · `net` = net income ·
> `gps` = GAAP EPS · `csh` = cash EPS · `ent` = enterprise value · `nav` = net asset value。
> 本节初稿按「税前利润」写就，经济解释已于下方同步更正；台账 `robustness_e76xGOQO.economic_rationale` 已重写。

**判定：PASS（带软标记）** — Batch AE 七指标扫描的唯一全闸通过腿，**IS 强度全面超越 AD1**，
但 **2Y 落在文档推导的 ATOM cutoff 之下**（平台自报线通过），这是本候选唯一的实质性未决风险。

## 与 AD1 的逐项对照（同配方，只换指标）

| 轴 | AD1 `dps` | **AE2 `ebt`** | 差 |
|---|---:|---:|---|
| Sharpe | 1.71 | **2.15** | **+0.44** |
| Fitness | 1.02 | **1.59** | **+0.57** |
| returns | .0449 | **.0685** | **+53%**（⇒ 单独越过 EUR profile 的 0.05 升-active 触发线） |
| margin | 17.21 bp | **25.37 bp** | **+47%** |
| pnl | 4 634 507 | **7 064 269** | **+52%** |
| drawdown | .0450 | **.0359** | **−20%（更低）** |
| sub_universe_sharpe | 0.95（ratio 0.556） | **1.12** | 更强 |
| **2Y Sharpe** | **2.41** | 1.93 | **−0.48（AE2 唯一劣势轴）** |
| **prod** | **0.497** | 0.6236 | AD1 余量更宽（.203 vs .0764） |
| self | 0.1706 | 0.3209 | 均 PASS |
| `failed_ra_count` | **0** | **0** | 平 |
| 正年数 | 9/10 | **10/10** | AE2 更稳 |
| 全历史 CV（样本） | 0.702 | **0.359** | **AE2 低一半** |
| PnL top-3 集中度 | 53.2% | **37.8%** | **AE2 显著更分散** |

## B.0 / B.0a

Failed RA **0** / Failed PPA **0**；`checks.fail = []`；
`warning` 仅 `MATCHES_THEMES`、`OSMOSIS_ALLOCATION`（**无 `CLUSTER_TEST` ⇒ 该检查 ∈ pass**）。
**B.0a 体检硬门同 AD1：未生效，`analyst7` 体检包缺失**（同一协议缺口，不重复举证）。

## B.1　规范信息

- 表达式：`group_neutralize(signed_power(group_zscore(divide(subtract(est_12m_ebt_mean, est_12m_ebt_mean_4wks_ago), est_12m_ebt_std), subindustry), 1.4), market)`
- 设置：与 AD1 **逐字相同**（EUR / TOP2500 / D1 / FAST / decay 40 / trunc 0.08 / …/ 2014→2023 / FULL）⇒ **唯一变量 = 指标 `dps` → `ebt`**
- 字段 3 个，同数据集 `analyst7` ⇒ **ATOM 合规**；分组字段仅 `subindustry` 与 `market`（均在平台许可的 6 个内）
- `checks.pass` = LOW_SHARPE, LOW_FITNESS, LOW_TURNOVER, HIGH_TURNOVER, CONCENTRATED_WEIGHT, LOW_SUB_UNIVERSE_SHARPE, **CLUSTER_TEST**, **LOW_2Y_SHARPE**, MATCHES_PYRAMID
- `IS_LADDER_SHARPE` 同样**不在任何名单** ⇒ ATOM 替代条款生效
- `LOW_ROBUST_UNIVERSE_SHARPE` 同样**缺席 ⇒ 无法核实**

## ★ 2Y 线的实测裁定（推翻文档推导）

`single-dataset-alphas` 文档载 D1 的 2Y cutoff = **2.38**，且「TO < 30% 时 IS Sharpe Ladder 的 PASS_THRESHOLDS × 0.85」
⇒ 推导出的操作线为 **2.38 × 0.85 = 2.023**。**Batch AE 的四条腿直接证伪了这个推导在本环境下的可操作性**：

| 腿 | 2Y | 平台 `LOW_2Y_SHARPE` 处置 | 平台自报 limit |
|---|---:|---|---:|
| AE4 `sal` | 1.26 | **warning + 计入 `ra_failed_checks`** | **1.58** |
| AE3 `eps` | 1.33 | **warning + 计入** | **1.58** |
| AE7 `cps` | 1.34 | **warning + 计入** | **1.58** |
| AE1 `ebi` | 1.38 | **warning + 计入** | **1.58** |
| **AE2 `ebt`** | **1.93** | **pass，未计入** | **1.58** |
| AD1 `dps` | 2.41 | pass | — |

⇒ **平台在 IS 阶段实际执行的是 1.58，不是 2.023**（若为 2.023，AE2 的 1.93 必被计入）。
**但 `REGULAR_SUBMISSION` 仍是 pending，而提交端点是死 404 ⇒ 提交阶段会不会换成 2.023 / 2.38，无法核实。**
诚实结论：**AD1（2.41）越过该线的每一种读法（1.58 / 2.023 / 2.38 全部满足）；
AE2（1.93）只越过平台自报的那一种（1.58），越过 2.023 与 2.38 均不成立。**
⇒ **就提交安全性而言 AD1 严格优于 AE2；就 IS 强度而言 AE2 严格优于 AD1。** 二者不是替代关系，是**互补的两颗**。

## B.2　逐年归因

| 年 | pnl | Sharpe | returns | DD | margin | TO | L/S | Fitness |
|---|---:|---:|---:|---:|---:|---:|---|---:|
| 2014 | 912 769 | **3.36** | .0878 | .0123 | .002735 | .0642 | 1318/1301 | 2.82 |
| 2015 | 841 702 | 2.68 | .0809 | .0194 | .003192 | .0507 | 1381/1345 | 2.16 |
| 2016 | 498 868 | **1.53** | .0480 | .0258 | .001797 | .0534 | 1354/1370 | 0.95 |
| 2017 | 838 840 | **3.27** | .0807 | .0197 | .003032 | .0532 | 1505/1448 | 2.63 |
| 2018 | 534 565 | **1.58** | .0514 | .0271 | .001933 | .0532 | 1519/1412 | 1.01 |
| 2019 | 794 007 | 2.79 | .0763 | .0111 | .002861 | .0534 | 1409/1424 | 2.18 |
| 2020 | 404 513 | **0.96** | .0423 | .0359 | .001444 | .0586 | 1453/1313 | 0.56 |
| 2021 | **915 776** | 2.61 | .0881 | .0210 | .003365 | .0523 | 1348/1618 | 2.19 |
| 2022 | 589 709 | **1.55** | .0567 | .0309 | .002162 | .0525 | 1387/1520 | 1.04 |
| 2023 | 733 387 | 2.46 | .0705 | .0199 | .002896 | .0487 | 1378/1383 | 1.85 |

**主判定（Recent-3yr = 2021 / 2022 / 2023）**

| 检查 | 读数 | 线 | 判定 |
|---|---:|---:|---|
| Recent-3yr Sharpe | 2.61 / 1.55 / 2.46，均值 **2.207** | ≥ 1.58 且每年 > 0.3 | **PASS** |
| Recent-3yr CV_Sharpe | **0.260**（样本）/ **0.212**（总体） | < 0.40 | **PASS** |
| 衰减比 | 2.46 / 2.15 = **1.144** | ≥ 0.50 | **PASS**（> 1 ⇒ 无衰减） |
| 平年 | **0** | 0 | **PASS** |
| Recent-3yr max/min | 2.61 / 1.55 = **1.684** | ≤ 3 | **PASS** |

**全历史（软标记区）**：均值 **2.279**｜中位数 **2.535**｜CV **0.359**（样本）/ **0.341**（总体）
⇒ **CV 连 0.40 的 CONDITIONAL 带都没进**，是本战役测过的最平稳逐年分布；
**10/10 年全部为正**（AD1 9/10，V5 8/10 且有 2016 = 0.01 的平年）；全历史 max/min = 3.36/0.96 = **3.50**（落 3–5 带 ⇒ 信息性软标记）。

**§42.4 提案格（PnL 集中度）**：top-1 **12.96%**｜top-2 **25.89%**｜top-3 **37.80%**
⇒ 三项**全面优于** AD1（19.5 / 36.6 / 53.2）与 V5（21.5 / 41.3 / 56.9）；
集中度因子 **1.26×**（AD1 1.77×，V5 1.90×）⇒ **接近逐年均匀贡献，是本战役最健康的 PnL 分布。**

**§42.10 提案格（最优年 book 朝向）**：2021 L/S = 1348/1618 = **0.833**；
其余九年区间 **[0.9125, 1.1066]** ⇒ **落在区间外 ⇒ 该格 FIRES**（与 V5、AD1 同形态，见 AD1 节的否证结论）。

## B.3　PnL / 回撤 / 换手归因

- **回撤日历**：全期 DD **.0359** ⇒ 2× 阈值 **.0718**；逐年最大 DD = **.0359**（2020）< .0718 ⇒ **无触发**。
- **换手 × margin**：TO **5.40%** ≪ 60% ⇒ 噪声拟合规则未触发；margin **25.37 bp** 越过 3 bp 与 10 bp 两条线，**全战役最高**。
- **Top-5 个股集中度：不可测**（同 AD1，`get_alpha_pnl` 无逐股分解）⇒ 以 `CONCENTRATED_WEIGHT ∈ pass` 替代。
- **B.5 `performance_comparison`：未执行**（同 AD1，理由与命令同前，`alpha_id="e76xGOQO"`）。

## B.4　相关性（`check_correlation(refresh=True)`）

| 项 | 读数 | 判定 |
|---|---:|---|
| **prod** | **max_correlation 0.6236**，`passes_check true` | **PASS，余量 .0764** |
| prod 直方图 | `[0.6,0.7] n=3`、`[0.5,0.6] n=362`、`[0.4,0.5] n=18765`；**`[0.7,0.8)` 桶不存在 ⇒ n = 0** | **族级可救** |
| prod min | −0.5341 | — |
| **self** | **max 0.32090**，`passes_check true` | **PASS，余量 .379** |
| self top | `78jdv6b1` 0.3209｜`gJj1nxLM` 0.1842｜`Wj7g2gAx` −0.0694｜`Wj71Q12o` −0.1651 | — |
| 池 | `pool_size 4`｜`full_os_pool_size 6`｜`excluded_power_pool_count 2`｜`ppac_ids_cached 2` | — |
| 汇总 | **`all_passed: true`** | — |

⚠ **prod 余量比 AD1 窄（.0764 vs .203）**，且 `[0.6,0.7]` 桶已有 n=3（AD1 的最高桶是 `[0.4,0.5]`）
⇒ `ebt` 比 `dps` 更靠近 prod 墙。按 §32.1 的 decay→prod 斜率（+0.00113/unit），
decay 上抬空间约 68 个单位，**充裕**；但**不得**为了别的目的再抬 decay（AD1 节已证 d40 在 subindustry+p1.4 基座上全面优于 d20，
而 prod 在这里不是绑定闸）。

## Phase C　反过拟合闸

| 检查项 | 读数 | 判定 |
|---|---|---|
| WebDataScope failed count | Failed RA 0 / PPA 0 | **PASS** |
| **Recent-3yr Sharpe（主判定）** | 均值 2.207 ≥ 1.58，三年全正 | **PASS** |
| Recent-3yr CV_Sharpe | 0.260 < 0.40 | **PASS** |
| 衰减比 | 1.144 ≥ 0.50 | **PASS** |
| 平年（近 3 年） | 0 | **PASS** |
| Recent-3yr max/min | 1.684 ≤ 3 | **PASS** |
| 全历史早年疲软 | CV 0.359 **未进 0.40 带**；10/10 正年；max/min 3.50（3–5 带） | **软标记（仅 max/min，信息性）** |
| Sub-universe | `LOW_SUB_UNIVERSE_SHARPE ∈ pass`（1.12） | **PASS** |
| 算子数 | **5**（同 AD1 配方） | 无软标记；PPA 上限 8 满足 |
| Margin @ turnover | 25.37 bp @ TO 5.40% | **PASS** |
| Top-5 个股集中度 | 不可测；`CONCENTRATED_WEIGHT ∈ pass` 替代 | **PASS（替代口径）** |
| 经济可解释性 | 一句话可写（见下） | **PASS** |

**经济解释（一句话）**：分析师对 12 个月前瞻 **EBITDA** 一致预期的四周修正，按横截面分歧度归一化——
EBITDA 剔除了折旧政策、资本结构与税率的差异，是最接近经营现金流的度量，市场对「分歧收窄后的上调」反应不足，
故在子行业内部比较时能捕捉未被定价的修正动量。

**硬标记 0 项 ⇒ 判定 PASS。**

## 最终判定

**PASS（带软标记）** — `failed_checks = []`。

**软标记清单**

1. **2Y 1.93 < 文档推导的 ATOM cutoff 2.023（亦 < 2.38）**：平台 IS 阶段自报线为 **1.58** 且已判 pass、`failed_ra_count = 0`；
   **提交阶段是否改判无法核实**（`REGULAR_SUBMISSION` pending + 提交端点死 404）。**这是本候选唯一的实质性未决风险。**
2. **prod 余量 .0764**（AD1 为 .203），`[0.6,0.7]` 桶已有 n=3。
3. **B.0a 体检硬门未生效**（`analyst7` 体检包缺失，同 AD1）。
4. **Top-5 个股集中度不可测**（同 AD1）。
5. **`LOW_ROBUST_UNIVERSE_SHARPE` 无法核实**（同 AD1）。
6. **B.5 `performance_comparison` 未执行**。
7. 全历史 max/min 3.50（3–5 带，信息性）。
8. 最优年（2021）book 朝向 0.833 落在其余九年区间之外（EUR 2021 制度性现象，三例共有）。

**下游含义**：`submit_verdict` 读到 `PASS` 不改判。⛔ **不构成提交授权**；提交须用户明确确认。
⚠ **塔位冲突须先交用户裁决**：`get_pyramid_alphas()` 实测 EUR/D1/ANALYST 现持 **1** 颗，
按用户裁定口径「点亮 = 已提交 ≥ 3」⇒ **再提交 2 颗即点亮该塔**，随后触发锁定项「已点亮塔不作主数据集」，
与「10 颗全部来自 analyst 塔」的目标直接冲突。

## 数据取自（可复现）

```
mcp__wq-brain-http__get_user_alphas(region="EUR", limit=10, order="-dateCreated")   # count 66，AE 七腿全收
mcp__wq-brain-http__get_alpha_yearly_stats(alpha_id="e76xGOQO")
mcp__wq-brain-http__check_correlation(alpha_id="e76xGOQO", refresh=True)   # prod 0.6236 / self 0.32090 / all_passed true
```

---

# 第二轮（2026-10-20 09:45）：5 颗 prod 可提交候选的稳健性审计

> 触发：`check_correlation(refresh=True)` 实测 10 颗，**7 颗 prod < 0.7**；其中 5 颗位于本地 4 年 PnL 互相关 ≤ 0.7 的**最大同时提交团（精确解）**。
> 本轮补审 `6XAe27eL` / `3qjeJGle` / `qME6VWbj`；`e76xGOQO` / `LL5dmv9a` 已在前两节审计。
> 方法同前：Recent-3yr（2021–2023）为主判定；逐年 DD 对 **2× 全期 DD**；Top-5 个股集中度不可测 ⇒ 以平台 `CONCENTRATED_WEIGHT ∈ pass` 替代；B.5 只作软标记。

| alpha | 形式 | Recent-3yr 均值 | CV 样本/总体 | 衰减比 | max/min | prod | self | 判定 |
|---|---|---:|---:|---:|---:|---:|---:|---|
| `6XAe27eL` | pre 幅度 + ts_zscore 门控 | 1.907 | .385/.314 | 1.333 | 2.208 | **0.4857** | 0.1797 | **PASS** |
| `3qjeJGle` | gps（GAAP EPS）幅度 | 2.390 | **.436**/.356 | 1.343 | 2.496 | **0.5710** | 0.2484 | **CONDITIONAL** |
| `qME6VWbj` | ebi（EBIT）幅度 | 2.017 | .382/.312 | 1.324 | 2.263 | **0.6609** | 0.2674 | **PASS** |

---

## `6XAe27eL` — pre 修订幅度 + `|ts_zscore|>1.0` 门控（Batch AL4）

```
trade_when(abs(ts_zscore(divide(subtract(est_12m_pre_mean, est_12m_pre_mean_4wks_ago), est_12m_pre_std), 66)) > 1.0,
           group_neutralize(signed_power(group_zscore(divide(subtract(est_12m_pre_mean, est_12m_pre_mean_4wks_ago), est_12m_pre_std), subindustry), 1.4),
           market),
           0)
```

| 项 | 值 | 项 | 值 |
|---|---|---|---|
| status / stage | `UNSUBMITTED` / `IS` | universe / delay | **TOP2500** / 1 |
| neutralization / decay | **FAST** / **80** | Sharpe / Fitness | **1.74** / **1.10** |
| returns / drawdown | .0499 / .0507 | margin / turnover | **23.94 bp** / 4.17% |
| sub / 比率 | .96 / **.552** | 2Y | **1.62** |
| 算子数 | **8** | failed RA / PPA | 0 / 0 |

| 年 | pnl | Sharpe | returns | DD | margin | TO | L/S | Fitness |
|---|---:|---:|---:|---:|---:|---:|---|---:|
| 2014 | 512 808 | 1.90 | .0493 | .0121 | 18.98 bp | .0520 | 1316/1303 | 1.19 |
| 2015 | 819 102 | **2.73** | .0788 | .0246 | 38.33 bp | .0411 | 1411/1316 | 2.17 |
| 2016 | 105 929 | **0.38** | .0102 | .0261 | 5.06 bp | .0403 | 1369/1355 | 0.11 |
| 2017 | 604 075 | 2.57 | .0581 | .0183 | 28.47 bp | .0408 | 1540/1413 | 1.75 |
| 2018 | 607 103 | 2.19 | .0584 | .0167 | 29.99 bp | .0389 | 1544/1387 | 1.50 |
| 2019 | 682 064 | 2.66 | .0656 | .0146 | 32.72 bp | .0401 | 1521/1313 | 1.93 |
| 2020 | 16 221 | **0.05** | .0017 | .0364 | 0.78 bp | .0435 | 1511/1255 | 0.01 |
| 2021 | 703 367 | 2.34 | .0676 | .0136 | 34.18 bp | .0396 | 1337/1629 | 1.72 |
| 2022 | 388 480 | **1.06** | .0374 | **.0472** | 18.33 bp | .0408 | 1395/1513 | 0.58 |
| 2023 | 708 201 | 2.32 | .0681 | .0218 | 34.09 bp | .0400 | 1363/1397 | 1.71 |

**主判定（Recent-3yr = 2021 / 2022 / 2023）**

| 检查 | 读数 | 线 | 判定 |
|---|---:|---:|---|
| Recent-3yr Sharpe | 2.34 / 1.06 / 2.32，均值 **1.907** | ≥ 1.58 且每年 > 0.3 | **PASS** |
| Recent-3yr CV_Sharpe | **.385**（样本）/ **.314**（总体） | < 0.40 | **PASS（贴线）** |
| 衰减比 | 2.32 / 1.74 = **1.333** | ≥ 0.50 | **PASS** |
| 平年 | **0** | 0 | **PASS** |
| Recent-3yr max/min | 2.34 / 1.06 = **2.208** | ≤ 3 | **PASS** |

**全历史（软标记区）**：均值 **1.820**｜中位数 **2.255**｜CV **.535**（样本）/ **.508**（总体）｜10/10 年为正｜max/min = 2.73/0.05 = **54.6**（2020 近零）⇒ 早年疲软只作信息性软标记，**不据此 REJECT**。

**PnL 集中度**：top-1 **15.91%**｜top-2 **29.67%**｜top-3 **43.34%** ⇒ 集中度因子 **1.445×**（e76x 1.26× / LL5 1.78× 之间）。

**B.3　PnL / 回撤 / 换手归因**

- **回撤日历**：全期 DD **.0507** ⇒ 2× 阈值 **.1014**；逐年最大 DD = **.0472**（2022）< .1014 ⇒ **无触发**。
- **换手 × margin**：TO **4.17%** ≪ 60% ⇒ 噪声拟合规则未触发；margin **23.94 bp** 远越过 3 bp / 10 bp 两条线。
- **Top-5 个股集中度：不可测**（`get_alpha_pnl` 只有 `date,pnl`）⇒ 以平台 `CONCENTRATED_WEIGHT ∈ pass` 替代。
- **B.5 `performance_comparison`：未执行**（只产生软标记、不改判定）。

**B.4　相关性**

| 项 | 读数 | 判定 |
|---|---:|---|
| **prod** | **0.4857**，`passes_check true` | **PASS，余量 .2143** |
| **self** | **0.1797**，`passes_check true` | **PASS，余量 .520** |
| 本地互相关 | 与 `qME6VWbj` **0.5078**（§55.6 实测最高） | 团内独立席位 |

**Phase C　反过拟合闸**

| 检查项 | 读数 | 判定 |
|---|---|---|
| WebDataScope failed count | Failed RA 0 / PPA 0 | **PASS** |
| **Recent-3yr Sharpe（主判定）** | 均值 1.907 ≥ 1.58，三年全正 | **PASS** |
| Recent-3yr CV_Sharpe | .385 < .40 | **PASS（贴线）** |
| 衰减比 | 1.333 ≥ .50 | **PASS** |
| 平年（近 3 年） | 0 | **PASS** |
| Recent-3yr max/min | 2.208 ≤ 3 | **PASS** |
| 全历史早年疲软 | CV .535；max/min 54.6（2020 .05） | **软标记（仅信息性）** |
| Sub-universe | .96 / 比率 **.552** ≥ .53 | **PASS（贴线）** |
| 算子数 | **8**（> 5 软标记；PPA 上限 8 满足） | **软标记** |
| Margin @ turnover | 23.94 bp @ 4.17% | **PASS** |
| Top-5 个股集中度 | 不可测；`CONCENTRATED_WEIGHT ∈ pass` 替代 | **PASS（替代口径）** |
| 经济可解释性 | 一句话可写 | **PASS** |

**经济解释（一句话）**：分析师对未来 12 个月**税前利润**一致预期的四周修正，按横截面分歧度归一化，并只在对自身近 66 日异常大（`|ts_zscore| > 1.0`）时持仓——税前利润修正混杂税项与一次性项目，门控滤掉噪声型小修正；子行业内部比较剥离行业级预期潮，再做市场中性。

**最终判定：PASS（带软标记）** — `failed_checks = []`。

**软标记清单**

1. **2Y 1.62 仅比平台线 1.58 高 .04**，是 5 席中最贴线的一颗（另 < 文档推导的 ATOM cutoff 2.023）。
2. **sub 比率 .552 仅比 .53 线高 .022**，同为 5 席最紧。
3. 算子数 **8** > 5（软标记；PPA 上限 8 恰好满足）。
4. B.0a 体检硬门未生效（`tracking/mining/field_inspect_eur_analyst7.json` 缺失）。
5. Top-5 个股集中度不可测；`LOW_ROBUST_UNIVERSE_SHARPE` 无法核实；B.5 未执行。
6. 全历史 CV .535 / max-min 54.6（2020 Sharpe .05）—— 仅信息性；`MATCHES_THEMES` / `CLUSTER_TEST 1.42` / `OSMOSIS_ALLOCATION` 告警。

**下游含义**：`submit_verdict` 读到 `PASS` 不改判。⛔ **不构成提交授权**；提交须用户明确确认。2Y 贴线使其成为 5 席中**最先需要复测**的一颗。

---

## `3qjeJGle` — gps（GAAP EPS）修订幅度 p1.4 / d80（Batch AN2）

```
group_neutralize(signed_power(group_zscore(divide(subtract(est_12m_gps_mean, est_12m_gps_mean_4wks_ago), est_12m_gps_std), subindustry), 1.4), market)
```

| 项 | 值 | 项 | 值 |
|---|---|---|---|
| status / stage | `UNSUBMITTED` / `IS` | universe / delay | **TOP2500** / 1 |
| neutralization / decay | **FAST** / **80** | Sharpe / Fitness | **1.72** / **1.08** |
| returns / drawdown | .0497 / .0334 | margin / turnover | **21.32 bp** / 4.66% |
| sub / 比率 | .95 / **.552** | 2Y | **1.80** |
| 算子数 | **5** | failed RA / PPA | 0 / 0 |

| 年 | pnl | Sharpe | returns | DD | margin | TO | L/S | Fitness |
|---|---:|---:|---:|---:|---:|---:|---|---:|
| 2014 | 755 517 | **3.22** | .0726 | .0117 | 25.59 bp | .0568 | 1265/1354 | 2.45 |
| 2015 | 160 712 | **0.52** | .0155 | .0291 | 6.91 bp | .0447 | 1354/1373 | 0.18 |
| 2016 | 278 931 | 0.95 | .0268 | .0132 | 11.74 bp | .0457 | 1352/1372 | 0.44 |
| 2017 | 565 780 | 2.34 | .0544 | .0222 | 24.30 bp | .0448 | 1431/1523 | 1.54 |
| 2018 | 364 147 | 1.23 | .0350 | .0313 | 15.44 bp | .0453 | 1493/1438 | 0.65 |
| 2019 | 657 837 | 2.43 | .0633 | .0122 | 28.19 bp | .0449 | 1471/1362 | 1.73 |
| 2020 | 229 013 | **0.61** | .0240 | **.0334** | 9.47 bp | .0506 | 1529/1237 | 0.27 |
| 2021 | 929 845 | **3.47** | .0894 | .0095 | 40.98 bp | .0436 | 1327/1640 | 2.93 |
| 2022 | 483 380 | **1.39** | .0465 | .0260 | 20.03 bp | .0464 | 1376/1532 | 0.85 |
| 2023 | 699 916 | 2.31 | .0673 | .0163 | 30.90 bp | .0436 | 1408/1353 | 1.69 |

**主判定（Recent-3yr = 2021 / 2022 / 2023）**

| 检查 | 读数 | 线 | 判定 |
|---|---:|---:|---|
| Recent-3yr Sharpe | 3.47 / 1.39 / 2.31，均值 **2.390** | ≥ 1.58 且每年 > 0.3 | **PASS** |
| Recent-3yr CV_Sharpe | **.436**（样本）/ **.356**（总体） | < 0.40 | **CONDITIONAL（0.40–0.60 带，取保守样本口径）** |
| 衰减比 | 2.31 / 1.72 = **1.343** | ≥ 0.50 | **PASS** |
| 平年 | **0** | 0 | **PASS** |
| Recent-3yr max/min | 3.47 / 1.39 = **2.496** | ≤ 3 | **PASS** |

**全历史（软标记区）**：均值 **1.847**｜中位数 **1.85**｜CV **.571**（样本）/ **.542**（总体）｜10/10 年为正｜max/min = 3.47/0.52 = **6.67**（2015 弱年）⇒ 早年疲软只作信息性软标记，**不据此 REJECT**。

**PnL 集中度**：top-1 **18.14%**｜top-2 **32.89%**｜top-3 **46.54%** ⇒ 集中度因子 **1.551×**。

**B.3　PnL / 回撤 / 换手归因**

- **回撤日历**：全期 DD **.0334** ⇒ 2× 阈值 **.0668**；逐年最大 DD = **.0334**（2020）< .0668 ⇒ **无触发**。
- **换手 × margin**：TO **4.66%** ≪ 60%；margin **21.32 bp** 远越过 3 bp / 10 bp 两条线。
- **Top-5 个股集中度：不可测** ⇒ 以 `CONCENTRATED_WEIGHT ∈ pass` 替代；**B.5 未执行**。

**B.4　相关性**

| 项 | 读数 | 判定 |
|---|---:|---|
| **prod** | **0.5710**，`passes_check true` | **PASS，余量 .129** |
| **self** | **0.2484**，`passes_check true` | **PASS，余量 .452** |
| 本地互相关 | `qME6VWbj` **.6267**｜`e76xGOQO` .5284｜`P0MOK7wx` .4984｜`LL5dmv9a` .3735 | 团内独立席位（略紧） |

**Phase C　反过拟合闸**

| 检查项 | 读数 | 判定 |
|---|---|---|
| WebDataScope failed count | Failed RA 0 / PPA 0 | **PASS** |
| **Recent-3yr Sharpe（主判定）** | 均值 2.390 ≥ 1.58，三年全正 | **PASS** |
| **Recent-3yr CV_Sharpe** | **.436**（样本）/ .356（总体） | **CONDITIONAL** |
| 衰减比 | 1.343 ≥ .50 | **PASS** |
| 平年（近 3 年） | 0 | **PASS** |
| Recent-3yr max/min | 2.496 ≤ 3 | **PASS** |
| 全历史早年疲软 | CV .571；max/min 6.67（2015 .52） | **软标记（仅信息性）** |
| Sub-universe | .95 / 比率 **.552** ≥ .53 | **PASS（贴线）** |
| 算子数 | **5** | 无软标记 |
| Margin @ turnover | 21.32 bp @ 4.66% | **PASS** |
| Top-5 个股集中度 | 不可测；`CONCENTRATED_WEIGHT ∈ pass` 替代 | **PASS（替代口径）** |
| 经济可解释性 | 一句话可写 | **PASS** |

**经济解释（一句话）**：分析师对未来 12 个月 **GAAP EPS** 一致预期的四周修正，按横截面分歧度归一化——GAAP EPS 是最常被用作业绩基准的口径，修正信息沿分析师网络缓慢扩散，市场对「分歧收窄后的上调」反应不足；子行业内部比较剥离行业级预期潮，decay 80 平滑短窗噪声。

**最终判定：CONDITIONAL** — `failed_checks = ["recent3yr_cv_sharpe"]`，硬 REJECT 触发 0。

**软标记清单**

1. **CONDITIONAL 的唯一来源**：Recent-3yr CV 样本 **.436** 落 0.40–0.60 带（总体 .356 未进带）；驱动 = 2022 Sharpe **1.39** 对 2021 3.47 / 2023 2.31。按 skill，CONDITIONAL **不阻断** `submit_verdict`，但建议先 repair/轮换并复审（≤ 2 轮）再请用户确认。
2. 2Y 1.80 < 文档推导的 ATOM cutoff 2.023（平台线 1.58 通过）。
3. sub 比率 .552 仅比 .53 线高 .022。
4. B.0a 体检硬门未生效；Top-5 集中度不可测；`LOW_ROBUST_UNIVERSE_SHARPE` 无法核实；B.5 未执行。
5. 全历史 CV .571 / max-min 6.67（2015 .52）—— 仅信息性。
6. 最优年 2021 的 book 朝向 L/S **.809** 落在其余九年区间 **[.898, 1.236]** 之外 ⇒ 与 V5 / AD1 / e76x 同形的 EUR 2021 制度性现象。
7. `MATCHES_THEMES`（GLB/D1 TOPDIV3000 ×2.5）/ `OSMOSIS_ALLOCATION` 告警。

**下游含义**：`submit_verdict` 读到 CONDITIONAL 不改判，只加「先 repair 并重审再请用户确认」提示；**它仍是 5 席团成员**（与团内最大相关 .6267）。若按 skill 建议先修复，5 席临时降为 4 席。

---

## `qME6VWbj` — ebi（EBIT）修订幅度 p1.0 / d40（Batch AK4）

```
group_neutralize(signed_power(group_zscore(divide(subtract(est_12m_ebi_mean, est_12m_ebi_mean_4wks_ago), est_12m_ebi_std), subindustry), 1.0), market)
```

| 项 | 值 | 项 | 值 |
|---|---|---|---|
| status / stage | `UNSUBMITTED` / `IS` | universe / delay | **TOP2500** / 1 |
| neutralization / decay | **FAST** / **40** | Sharpe / Fitness | **1.76** / **1.07** |
| returns / drawdown | .0464 / .0292 | margin / turnover | **18.46 bp** / 5.03% |
| sub / 比率 | **1.01** / .574 | 2Y | **1.65** |
| 算子数 | **5** | failed RA / PPA | 0 / 0 |

| 年 | pnl | Sharpe | returns | DD | margin | TO | L/S | Fitness |
|---|---:|---:|---:|---:|---:|---:|---|---:|
| 2014 | 808 603 | **3.61** | .0778 | .0096 | 25.48 bp | .0610 | 1364/1255 | 2.85 |
| 2015 | 527 234 | 1.82 | .0507 | .0237 | 20.58 bp | .0493 | 1376/1351 | 1.16 |
| 2016 | 184 123 | **0.69** | .0177 | .0175 | 7.25 bp | .0488 | 1341/1383 | 0.26 |
| 2017 | 658 444 | 2.49 | .0633 | .0169 | 25.63 bp | .0494 | 1488/1466 | 1.77 |
| 2018 | 405 517 | 1.55 | .0390 | .0243 | 15.58 bp | .0501 | 1519/1412 | 0.87 |
| 2019 | 471 135 | 1.84 | .0453 | .0142 | 18.80 bp | .0482 | 1435/1398 | 1.11 |
| 2020 | 151 615 | **0.45** | .0159 | **.0292** | 5.94 bp | .0534 | 1496/1270 | 0.16 |
| 2021 | 656 547 | 2.58 | .0631 | .0153 | 25.94 bp | .0487 | 1376/1591 | 1.83 |
| 2022 | 346 315 | **1.14** | .0333 | .0274 | 13.82 bp | .0482 | 1414/1494 | 0.59 |
| 2023 | 580 572 | 2.33 | .0558 | .0141 | 24.15 bp | .0462 | 1363/1398 | 1.56 |

**主判定（Recent-3yr = 2021 / 2022 / 2023）**

| 检查 | 读数 | 线 | 判定 |
|---|---:|---:|---|
| Recent-3yr Sharpe | 2.58 / 1.14 / 2.33，均值 **2.017** | ≥ 1.58 且每年 > 0.3 | **PASS** |
| Recent-3yr CV_Sharpe | **.382**（样本）/ **.312**（总体） | < 0.40 | **PASS（贴线）** |
| 衰减比 | 2.33 / 1.76 = **1.324** | ≥ 0.50 | **PASS** |
| 平年 | **0** | 0 | **PASS** |
| Recent-3yr max/min | 2.58 / 1.14 = **2.263** | ≤ 3 | **PASS** |

**全历史（软标记区）**：均值 **1.850**｜中位数 **1.83**｜CV **.515**（样本）/ **.489**（总体）｜10/10 年为正｜max/min = 3.61/0.45 = **8.02**（2020 弱年）⇒ 早年疲软只作信息性软标记，**不据此 REJECT**。

**PnL 集中度**：top-1 **16.88%**｜top-2 **30.59%**｜top-3 **44.33%** ⇒ 集中度因子 **1.478×**。

**B.3　PnL / 回撤 / 换手归因**

- **回撤日历**：全期 DD **.0292** ⇒ 2× 阈值 **.0584**；逐年最大 DD = **.0292**（2020）< .0584 ⇒ **无触发**。
- **换手 × margin**：TO **5.03%** ≪ 60%；margin **18.46 bp** 远越过 3 bp / 10 bp 两条线。
- **Top-5 个股集中度：不可测** ⇒ 以 `CONCENTRATED_WEIGHT ∈ pass` 替代；**B.5 未执行**。

**B.4　相关性**

| 项 | 读数 | 判定 |
|---|---:|---|
| **prod** | **0.6609**，`passes_check true` | **PASS，余量仅 .0391（5 席最窄）** |
| **self** | **0.2674**，`passes_check true` | **PASS，余量 .433** |
| 本地互相关 | `e76xGOQO` **.6957**（5 席团内最大对）｜`3qjeJGle` .6267｜`P0MOK7wx` .6186 | 团内边缘席位 |

**Phase C　反过拟合闸**

| 检查项 | 读数 | 判定 |
|---|---|---|
| WebDataScope failed count | Failed RA 0 / PPA 0 | **PASS** |
| **Recent-3yr Sharpe（主判定）** | 均值 2.017 ≥ 1.58，三年全正 | **PASS** |
| Recent-3yr CV_Sharpe | .382 < .40 | **PASS（贴线）** |
| 衰减比 | 1.324 ≥ .50 | **PASS** |
| 平年（近 3 年） | 0 | **PASS** |
| Recent-3yr max/min | 2.263 ≤ 3 | **PASS** |
| 全历史早年疲软 | CV .515；max/min 8.02（2020 .45） | **软标记（仅信息性）** |
| Sub-universe | **1.01** / 比率 .574 ≥ .53 | **PASS** |
| 算子数 | **5** | 无软标记 |
| Margin @ turnover | 18.46 bp @ 5.03% | **PASS** |
| Top-5 个股集中度 | 不可测；`CONCENTRATED_WEIGHT ∈ pass` 替代 | **PASS（替代口径）** |
| 经济可解释性 | 一句话可写 | **PASS** |

**经济解释（一句话）**：分析师对未来 12 个月 **EBIT** 一致预期的四周修正，按横截面分歧度归一化——EBIT 剥离利息与税率差异，是最干净的经营盈利能力度量；市场对「分歧收窄后的上调」反应不足，故在子行业内部比较时能捕捉未被定价的修正动量。

**最终判定：PASS（带软标记）** — `failed_checks = []`。

**软标记清单**

1. **prod .6609 余量仅 .0391**（5 席最窄）；与 `e76xGOQO` 的本地互相关 **.6957** 是 5 席团内最大对 ⇒ 提交必须**逐颗** `check_self_correlation`。
2. 2Y 1.65 仅比平台线 1.58 高 .07（另 < 文档推导 cutoff 2.023）。
3. Recent-3yr CV 样本 .382 仅低于 .40 线 .018（贴线 PASS）。
4. B.0a 体检硬门未生效；Top-5 集中度不可测；`LOW_ROBUST_UNIVERSE_SHARPE` 无法核实；B.5 未执行。
5. 全历史 CV .515 / max-min 8.02（2020 .45）—— 仅信息性。
6. `MATCHES_THEMES` / `CLUSTER_TEST 1.45` / `OSMOSIS_ALLOCATION` 告警。

**下游含义**：`submit_verdict` 读到 `PASS` 不改判。⛔ **不构成提交授权**；提交须用户明确确认。它是 5 席中的**边缘席位**：若第 5 颗提交时 self 超线，首先被牺牲的是它（或 `e76xGOQO` 二选一）。

---

## 本轮小结

| 判定 | alpha | 台账键 |
|---|---|---|
| **PASS** | `6XAe27eL` / `qME6VWbj` / `e76xGOQO` / `LL5dmv9a` | `robustness_<id>` 已落 |
| **CONDITIONAL** | `3qjeJGle`（Recent-3yr CV 样本 .436；2022 弱年驱动） | `robustness_3qjeJGle` 已落 |
| **PASS（修复继任者）** | `Grge2lN3`（= `3qjeJGle` + regime 门控；CV 样本 **.366**） | `robustness_Grge2lN3` 已落；见文末「修复轮」 |

- **4 PASS + 1 CONDITIONAL**（母体 5 颗）；硬 REJECT 触发 **0**，5 颗全部 `failed_ra_count = 0` / `failed_ppa_count = 0`。同日修复轮把 CONDITIONAL 的 `3qjeJGle` 修成 **`Grge2lN3`（PASS）** ⇒ 换座后 5 席稳健性全 PASS（见文末「修复轮」）。
- `submit_verdict` 对 5 颗均为 `UNVERIFIABLE_404`（提交端点死链）、`sim_fails = 0`：**它不会拦任何一颗**；CONDITIONAL 只加 repair 提示。
- ⛔ **本报告不构成提交授权**。5 席最大同时提交团（精确解）仍为
  `{6XAe27eL, e76xGOQO, LL5dmv9a, qME6VWbj, 3qjeJGle}`，团内最大对 `e76xGOQO`–`qME6VWbj` **.6957**（贴线，余量 .0043）；须逐颗提交并复测 self。
- 本轮新增台账：`EUR/robustness_6XAe27eL`（PASS）、`EUR/robustness_3qjeJGle`（CONDITIONAL）、`EUR/robustness_qME6VWbj`（PASS）。

## 数据取自（第二轮，可复现）

```
mcp__wqb-db__get_alpha_by_id(alpha_id="6XAe27eL" / "3qjeJGle" / "qME6VWbj")
mcp__wq-brain-http__get_alpha_yearly_stats(alpha_id="6XAe27eL" / "3qjeJGle" / "qME6VWbj")
mcp__wqb-db__get_ledger_key(region="EUR", key="robustness_e76xGOQO")   # 台账 schema 模板
mcp__wqb-db__upsert_ledger_key(region="EUR", key="robustness_6XAe27eL" / "robustness_3qjeJGle" / "robustness_qME6VWbj")
```

---

## 修复轮（同日追加）· `3qjeJGle` → `Grge2lN3`：CONDITIONAL → **PASS**

> 触发：`3qjeJGle` 唯一的 CONDITIONAL 项是 Recent-3yr CV 样本 **.436**（> .40），驱动 = 2022 Sharpe 1.39 vs 2021 3.47 / 2023 2.31（弱年波动，未转亏）。
> 第 1 轮（skill 允许 ≤2 轮）repair：**核心信号全部冻结**（analyst7 / `gps` 四周修正 / SUBINDUSTRY 分组 / p1.4 / decay 80 / TOP2500 / D1 / FAST / truncation .08 / nanHandling·maxTrade ON），只改外层结构。
> 批次 `rep_3qje_20261020`（REP-A decay 80 六腿 multisim `1X65kecOe57I8T6Sl8EwRPU` + REP-B decay 120 两腿 multisim `P8X1MgdE4DsbUr10lAabYV2`），8/8 已收割入库，**6 腿过硬闸、2 腿掉 S/F/2Y**。

### 修复实验（8 腿）

| # | alpha | 杠杆（其余冻结） | S | F | 2Y | sub | 2021 / 2022 / 2023 | CV(样本) | 判定 |
|---|---|---|---:|---:|---:|---:|---|---:|---|
| — | `3qjeJGle` | 母体（p1.4 d80） | 1.72 | 1.08 | 1.80 | .95 | 3.47 / **1.39** / 2.31 | **.436** | CONDITIONAL |
| 1 | `gJW9lj0l` | p1.2 d80 | 1.73 | 1.06 | 1.69 | .94 | 3.57 / 1.34 / 2.15 | .480 | ✗ CV 更差 |
| 2 | `MP0LE7no` | `ts_mean(ratio,5)` p1.4 | 1.42 | 0.81 | 1.50 | — | — | — | ✗ 掉 S/F/2Y |
| 3 | `kqJZwjMk` | `ts_mean(ratio,5)` p1.2 | 1.43 | 0.80 | 1.40 | — | — | — | ✗ 掉 S/F/2Y |
| 4 | **`Grge2lN3`** | **`trade_when(abs(ts_zscore(est_12m_gps_mean,66))>1.0, 母体, 0)` + p1.4 d80** | **1.79** | **1.15** | **2.02** | .94 | **3.68 / 2.09 / 1.99** | **.366** | **✓ PASS** |
| 5 | `qME6ajpA` | 同门控 + p1.2 d80 | 1.81 | 1.14 | 1.91 | .95 | 3.81 / 2.05 / 1.82 | .425 | ✗ CV 仍过线 |
| 6 | `A1Q7pl5l` | `winsorize(std=2.5)` p1.4 d80 | 1.74 | 1.07 | 1.64 | .90 | 3.74 / 1.32 / 2.08 | .520 | ✗ CV 更差 |
| 7 | `E5Vejl2r` | p1.4 d120 | 1.85 | 1.22 | 1.95 | .97 | 3.96 / 1.66 / 2.35 | .444 | ✗ CV 仍过线 |
| 8 | `xA1dLjEn` | p1.2 d120 | 1.85 | 1.19 | 1.84 | .97 | 4.03 / 1.58 / 2.20 | .489 | ✗ CV 更差 |

**三条归因**

1. **decay 120 只抬水平、不治离散**：S 1.72→1.85，但 2021 同时由 3.47 抬到 3.96，CV 反升到 .444 ⇒ 单调时序平滑不是 CV 的解。
2. **对修正比率做 `ts_mean` 是毒药**：S 掉到 1.42–1.43、F 掉到 .80–.81 ⇒ 修正信号的时效性本身就是 alpha，平滑即在删信号。
3. **regime 门控是唯一同时改善弱年与强年的结构**：2022 1.39→2.09（+50%），2021 3.47→3.68（+6%），2023 2.31→1.99（−14%）；换手反而由 4.66% 降到 4.42%。门控用单字段 `ts_zscore(est_12m_gps_mean, 66)`（**不是**把修正比率算两遍——那会让算子调用点数达到 10、被闸 1b-2 拦下）。

### 获胜者 `Grge2lN3` 重审（Phase B → C → D）

```
trade_when(abs(ts_zscore(est_12m_gps_mean, 66)) > 1.0,
           group_neutralize(signed_power(group_zscore(divide(subtract(est_12m_gps_mean, est_12m_gps_mean_4wks_ago), est_12m_gps_std), subindustry), 1.4), market),
           0)
```

| 项 | 值 | 项 | 值 |
|---|---|---|---|
| status / stage | `UNSUBMITTED` / `IS` | region / universe / delay | **EUR** / **TOP2500** / 1 |
| neutralization / decay | **FAST** / **80** | truncation | 0.08 |
| Sharpe / Fitness | **1.79** / **1.15** | turnover | **0.0442** |
| returns / drawdown | 0.0517 / 0.0439 | margin | 0.002342（**23.42 bp**） |
| pnl | 5 336 113 | long / short | 1391 / 1428 |
| `sub_universe_sharpe` | **0.94**（比率 .525） | `two_year_sharpe` | **2.02** |
| `ra.failed_ra_count` | **0** | `ra.failed_ppa_count` | **0** |
| op_count | **8** | pyramid | `EUR/D1/ANALYST` ×1.3 |

逐年 Sharpe（10 年全正）：2014 **2.78**｜2015 1.18｜2016 0.21｜2017 2.75｜2018 0.43｜2019 3.03｜2020 0.67｜2021 **3.68**｜2022 **2.09**｜2023 **1.99**。

`checks.pass`（9）：`LOW_SHARPE` `LOW_FITNESS` `LOW_TURNOVER` `HIGH_TURNOVER` `CONCENTRATED_WEIGHT` `LOW_SUB_UNIVERSE_SHARPE` `CLUSTER_TEST` `LOW_2Y_SHARPE` `MATCHES_PYRAMID`
`checks.warning`（2）：`MATCHES_THEMES`、`OSMOSIS_ALLOCATION`
`checks.pending`（4）：`SELF_CORRELATION` `DATA_DIVERSITY` `PROD_CORRELATION` `REGULAR_SUBMISSION`（提交时平台才算；prod / self 已用只读端点实测，见下）

| Phase C 检查项 | 读数 | 判定 |
|---|---|---|
| WebDataScope failed count | Failed RA **0** / PPA **0**，无 PENDING 在计分名单内 | **PASS** |
| **Recent-3yr Sharpe（主判定）** | 2Y **2.02** ≥ 1.58；三年 3.68 / 2.09 / 1.99 全 > 0.3 | **PASS** |
| **Recent-3yr CV_Sharpe** | **.3666**（< .40；总体口径 .2994） | **PASS**（母体 .436 → 修复 .366） |
| 衰减比 | 1.99 / 1.79 = **1.112** ≥ .50 | **PASS** |
| 平年（近 3 年） | **0** | **PASS** |
| Recent-3yr max/min | 3.68 / 1.99 = **1.849** ≤ 3 | **PASS** |
| 全历史早年疲软 | 2016 0.21 / 2018 0.43；全史 CV .640、max-min 17.5 | 软标记（**绝不** REJECT） |
| Sub-universe | 平台 `LOW_SUB_UNIVERSE_SHARPE` PASS（0.94，比率 .525） | **PASS** |
| 算子数 | 8（≤8 PPA 文档上限；>5 记过拟合风险） | 软标记 |
| Margin @ turnover | 23.42 bp @ 4.42% TVR | **PASS** |
| Top-5 个股集中度 | 不可测；`CONCENTRATED_WEIGHT ∈ pass` 替代 | **PASS（替代口径）** |
| 经济可解释性 | 一句话可写 | **PASS** |

**CV 计算（可复算）**：三年 Sharpe `[3.68, 2.09, 1.99]`，均值 **2.5867**，样本 std **0.9482** ⇒ CV = 0.9482 / 2.5867 = **0.3666**。

**相关性（只读实测）**

| 对象 | 方法与读数 | 判定 |
|---|---|---|
| PROD（`check_correlation(refresh=True)`） | **max 0.5893**（min −0.4979；直方图 [0.5,0.6) n=318） | **PASS**（余量 .1107） |
| SELF（本地 OS 池，排除 Power Pool） | **max 0.2628**（`78jdv6b1`；池 4 + 2 PPAC） | **PASS**（余量 .4372） |
| ↔ 母体 `3qjeJGle` | 本地 4 年互相关 **0.9092** | 同族继任 ⇒ **只能提交一颗** |
| ↔ 其余 6 颗 | `.6026` qME6VWbj / `.5392` e76xGOQO / `.5168` P0MOK7wx / `.4518` wp9EvMmv / `.4478` 6XAe27eL / `.3732` LL5dmv9a | 全部 < .7 |

**最终判定：PASS** — `failed_checks = []`。软标记：2Y 2.02 距文档推导 ATOM cutoff 2.023 仅 −0.003（平台线 1.58 通过）；sub 比率 .525 贴 .53 经验线；prod 余量 .1107；op_count 8；B.0a 体检包缺失；Top-5 不可测；`LOW_ROBUST_UNIVERSE_SHARPE` 未发；B.5 未执行；全史 CV .640 仅信息性。

**处置建议（⛔ 不构成提交授权）**

- **5 席团换座**：`3qjeJGle`（CONDITIONAL）→ `Grge2lN3`（PASS）。换座后 `{6XAe27eL, e76xGOQO, LL5dmv9a, qME6VWbj, Grge2lN3}` 五席**稳健性全 PASS**。
- 换座后团内最大对仍是 `e76xGOQO`–`qME6VWbj` **.6957**（本地 4 年）；提交时须逐颗 `check_self_correlation` 复测。
- 提交前仍须：用户明确确认 + 平台 prod 实测 < .7 + `confirm_submit=True`（不可逆）。`submit_verdict` 只有否决权。

**台账**：`EUR/robustness_Grge2lN3`（verdict **PASS**，`failed_checks = []`，`repaired_from = 3qjeJGle`）。母体 `EUR/robustness_3qjeJGle` 保持 CONDITIONAL（其表达式未变；继任关系不是对它的解封）。

## 数据取自（修复轮，可复现）

```
mcp__wq-brain-http__get_alpha_details(alpha_id="Grge2lN3")
mcp__wq-brain-http__get_alpha_yearly_stats(alpha_id="Grge2lN3")
mcp__wq-brain-http__get_alpha_pnl(alpha_id="Grge2lN3")
mcp__wq-brain-http__check_self_correlation(alpha_id="Grge2lN3")
mcp__wq-brain-http__check_correlation(alpha_id="Grge2lN3", refresh=True)
mcp__wq-brain-http__compute_mutual_correlation(alpha_id_list=["Grge2lN3","3qjeJGle","6XAe27eL","e76xGOQO","P0MOK7wx","LL5dmv9a","qME6VWbj","wp9EvMmv"], threshold=0.5, years=4)
mcp__wqb-db__upsert_ledger_key(region="EUR", key="robustness_Grge2lN3")
```
