# DEU 战役最终状态（2026-11-10 收官）

## 一、交付件（本战役新挖）

| # | alpha_id | 数据集 | 塔 | 状态 | S | F | 2Y | TO | self | prod | ΔS |
|---|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|
| 1 | zq3eb7No | analyst7 | ANALYST | ✅ ACTIVE | 2.01 | 1.28 | 1.64 | 0.2262 | 0.3641 | 0.6171 | — |
| 2 | bl6AvMkN | analyst_factor_signals + predictive_starmine | MODEL+ANALYST | ✅ ACTIVE | 1.61 | 1.36 | 2.15 | 0.1097 | 0.5137 | 0.6470 | — |
| 3 | 1YNMAA8M | analyst7 + analyst15 | MODEL+ANALYST | 🟡 四闸全过，待授权 | 1.58 | 1.36 | 2.13 | 0.1337 | 0.6946 | 0.6951 | +0.43 |
| 4 | E569ZE7L | shortinterest3 | SHORTINTEREST | 🟡 四闸全过，CV 超线 | 1.68 | 1.21 | 2.27 | 0.1128 | 0.5444 | 0.5444 | +0.06 |

**已撤回**：mLovbnm2 —— 与 OS 池 rKRx2Alj（2026-11-09 ACTIVE）互相关 0.9966，self 撞死。
暂存文件已标 WITHDRAWN_DO_NOT_SUBMIT，不得提交。

### 交付篮子正交性
compute_mutual_correlation(threshold=0.7, years=4)，19 颗全算 → all_below_threshold = true，
max_mutually_below_subset_size = 19（19/19 完整独立集）

| 配对 | 互相关 |
|---|---:|
| 1YNMAA8M ~ E569ZE7L | 0.1227 |
| 1YNMAA8M ~ rKRx2Alj | 0.6946（最高） |
| E569ZE7L ~ xArzm3Mn | 0.5444（最高） |
| 1YNMAA8M ~ bl6AvMkN | 0.5128 |
| 1YNMAA8M ~ zq3eb7No | 0.2471 |
| E569ZE7L ~ Wje5K71x / 2rmGAPqN / bl6OWZ2M | 0.0411 / 0.0436 / 0.0485 |

---

## 二、本轮（2026-11-10 上午起）新增工作

**回测量**：Wave A~W 共 23 波 / 约 210 条（此前 125 波 / 455 条 ⇒ 累计 148 波 / 约 665 条）

### 2.1 关键纠正（改变了交付结论）

1. **mLovbnm2 撤回提交授权** —— OS 池新增 rKRx2Alj（2026-11-09）与之互相关 0.9966。
   此前台账的 self 0.5620 是 rKRx2Alj 提交前的旧值，已失效。
2. **分析师修正三腿族结构性封盘** —— IS 池 24 颗硬闸候选 self 全量重算（本地工具，零平台槽）：
   仅 1YNMAA8M PASS（0.6946），其余 23 颗全部超线（0.7008~0.9966）。
   族内改窗口/改轴/改第三腿字段/改第三腿数据集全部无效。

### 2.2 第三席寻觅（14 波 / 135 条，五条路径全试）

| 路径 | 波次 | 结论 |
|---|---|---|
| A. fundamental6 季度财报（goal 第1条指定） | A/B/C/E/G | ❌ 封盘：信号集中 fnd6_newq_oiadpq；换 8 字段全灭（S≤1.23）；该字段组合已被生产池占据（prod 0.9389/0.9728） |
| B. shortinterest3 借券 | D/F/H/I/J/K/L | ✅ 机制成立：8+ 颗四闸全过，S1.53~1.76，prod 0.51~0.58，10y 满覆盖，无负年；唯一问题：族内互相关 0.758~0.901 ⇒ 只能出 1 席；最优件 E569ZE7L 的 3y CV = 0.626 |
| C. sentiment / attention | M/O/P/Q/R/S/T | ❌ 强度与覆盖不可兼得：snt7 强（S1.78）但 2019 才起数据；snl27 覆盖满但弱（S≤0.67） |
| D. news / risk | N/U/V | ❌ RavenPack 事件情绪三数据集交叉验证全灭（覆盖好、符号混乱 ⇒ 信号本身无效） |
| E. 内置价格字段 | W | ❌ 纯价格机制 S ≤ 0.94，符号混乱 |

### 2.3 借券族（路径 B）的关键发现

**机制**：借券需求（borrow demand）抬升 = 做空/对冲需求拥挤 ⇒ 后续反转 ⇒ 做空借券需求抬升股。
学术支撑：Lou & Polk 2018 comomentum；short-interest skew 作为拥挤早期预警。

**可交付骨架（跨族通用）**：

    -group_rank(
      ts_target_tvr_decay(
        multiply(
          rank(ts_delta(ts_backfill(vec_avg(shrt3_bar), 132), 264)),
          rank(ts_delta(ts_backfill(vec_avg(shrt3_bar), 132), 132))
        ),
        target_tvr=0.03
      ),
      subindustry
    )

设置：DEU/TOP500/delay1/decay4/FAST/trunc0.08/nanON/maxTradeOFF，10 算子

**族内 8+ 颗四闸全过候选排序**：

| 候选 | 窗口/轴 | S | 2Y | 10y CV | 3y CV | 负年 | prod | self |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| **E569ZE7L** | 264/132 sub | 1.68 | 2.27 | **0.507** | **0.626** | **0** | 0.5444 | 0.5444 |
| GrWZqQaJ | 264/154 sub | 1.76 | 2.77 | 0.538 | 0.640 | 0 | — | — |
| 9qxnNkeq | 264/88 sub | 1.66 | 2.69 | 0.618 | 0.665 | 0 | 0.5327 | 0.5327 |
| 1YNrqG9X | 264/132 tvr.04 | 1.72 | 2.28 | 0.530 | 0.680 | 0 | — | — |
| wpQ08Nqx | 264/132 sector | 1.74 | 2.63 | 0.587 | 0.791 | 0 | — | — |
| pwd9qYlq | 132/88 sector | 1.59 | 2.90 | 0.704 | 0.869 | 0 | — | 0.5239 |
| j2Y7qlA5 | 132/88 sub | 1.65 | 2.72 | 0.663 | 1.035 | 1 | 0.5788 | 0.5788 |
| E56d9xnP | 66/44 market | 1.56 | 3.10 | 0.737 | 1.112 | 1 | — | 0.4228 |
| qMLQK9lZ | 66/44 sub | 1.63 | 3.03 | 0.689 | 1.107 | 1 | — | 0.5620 |

---

## 2.4 口径修正（2026-11-10 09:45，本轮最重要产出）

稳健性判定以 Claude/skills/brain-alpha-robustness/SKILL.md Phase C 判定表为唯一权威。此前我凭印象用「CV>=0.60 即 REJECT」判死，犯三重口径错误：

| 项 | 此前错误用法 | 权威口径 | 影响 |
|---|---|---|---|
| CV 的 sd | 样本 sd (n-1) | **总体 sd (n)**，样本 sd 仅参考带 | E569ZE7L: 0.626 -> **0.511** |
| 0.60 语义 | 当生死线 | **0.60 是 REJECT 上界，0.40-0.60 是 CONDITIONAL 带** | E569ZE7L: REJECT -> **CONDITIONAL** |
| CV 能否单独 REJECT | 认为可以 | **永不单独 REJECT** | 判定从生死变带 soft_flag |
| 族代表排序 | 按样本 sd CV | 按完整判定表（含 max/min） | 选错 -> **E569ZE7L** (max/min 4.80) 而非 9qxnNkeq (6.00 REJECT) |

台账已落库并经 submit_verdict 实测验证消费：E569ZE7L=CONDITIONAL(不拦截) / 1YNMAA8M=PASS / 9qxnNkeq=REJECT(BLOCKED) / 波X 5 件 REJECT。

**E569ZE7L repair 第 1 轮（Wave X，10 个变体）已跑完且无改善**：换轴 market/country、换 backfill 窗口 264/504/66、换第二窗口 66/88、换 target_tvr 0.02/0.04 —— 全部 REJECT，2021 年 Sharpe 更差(0.18~0.46 vs 基线 0.55)，max/min 恶化到 7.65~15.22。=> 2021 是借券数据本身信息量不足，结构修复无空间；基线 264/132 + subindustry 是族内唯一 max/min<5 的结构。

### 2.5 机制族覆盖已完整（2026-11-10 10:2x）

波 Y（insider 族，insiders 塔未点亮，cov 1.0）与波 Z（dl_riskfree_returns，厂商 ML 前瞻收益预测，cov 1.0）均全灭（符号混乱，S ≤0.58）。

DEU 15 塔现已全部实测或因无供数排除：

| 塔 | 状态 | 结论 |
|---|---|---|
| ANALYST | 6 颗 | 三腿族被 rKRx2Alj 整体锁死 |
| MODEL / OTHER / FUNDAMENTAL | 3/2/1 | 禁混集合内 或 fundamental6 封盘 |
| SHORTINTEREST | 2 颗 | 本轮唯一新机制成立（族容量 1 席） |
| SENTIMENT | 1 颗 | attention 族强度-覆盖不可兼得 |
| INSIDERS | 0 颗 | 波 Y 全灭（内部人事件极稀疏） |
| INSTITUTIONS | 1 颗 | 早前判死 S≤0.35 |
| NEWS | 0 颗 | 三数据集交叉验证全灭 |
| RISK | 0 颗 | 与 shortinterest3 同机制且更弱 |
| EARNINGS/MACRO/OPTION/SOCIALMEDIA/IMBALANCE | 0 颗 | cov=0 或过稀疏，无供数 |
| 内置价格 / 厂商 ML 输出 | — | 波 W / 波 Z 全灭 |

⇒ **DEU 域内可交付上限 = 4 颗**（2 颗已 ACTIVE + 1YNMAA8M + E569ZE7L）。要往第 5 颗走，**必须放开「不得换 region」过程约束**（goal 明文，需用户修改）。

### 2.6 未点亮塔逐一实测完毕（2026-11-10 10:2x）

波 AA/AB（other532 Barra 特质收益）、波 AD（pattern_scores 形态相似度）、波 AE（order_book_imbalance 订单簿失衡）均判死。

**关键平台事实（判据 MU）**：AA/AB 两波 preflight 全绿（valid/unknown_fields/unknown_soft 全空）但整批 CANCELLED；
改用 create_simulation **单条提交同一条表达式 → 成功**（Xg9dQYJm S-0.41 / lc 204）
⇒ 整批 CANCELLED 有两种根因，必须分叉排查：① 表达式错（preflight 会报）② **平台批次限制（preflight 全绿，单条可过）**。

**逐族归因**：

| 族 | 结果 | 归因 |
|---|---|---|
| other532 (Barra 残差) | S-0.41 单腿 / -0.09 加速度 | 残差=已剔除系统暴露的收益，非新信息；DEU 小市值不成立 |
| pattern_scores (K线形态) | S -0.31~+0.52 | 形态=价格的确定性变换 ⇒ 与波 W 纯价格同源，一致判死 |
| order_book_imbalance | S -0.48~+0.50 | 微观结构失衡在 DEU 截面无定价力；正反 lc 160 vs 290 = 样本集分裂（判据 MQ）非方向问题 |

⇒ **DEU 15 塔 + 内置价格 + 厂商 ML + 形态 + 微观结构全部覆盖完毕，域内可交付上限 = 4 颗**。

**1YNMAA8M prod refresh 终验（提交前强制项）= 0.6951 PASS**，与上轮一致，池未漂移。

### 2.7 旧判死族的新骨架重测（2026-11-10 10:3x，判据 MX）

**关键新假设（已证）**：族级判死只在**当时用的骨架**下成立。shortinterest3 早前判死（S≤0.90），
换「双窗口加速度 × target_tvr_decay × 反向持有」骨架后出货 8+ 颗四闸全过。

⇒ 派波 AF（借券塔第二席：10 个**不同语义字段** —— 借券费率/费率波动率/出借股数/贷款久期/交易笔数）+ 
波 AG（institutions6 机构持仓买卖流，早前 12 条旧骨架 S≤0.35）+ 
波 AE（order_book_imbalance 微观结构）—— 三个方向在飞。

**族内扩容思路（判据 MY）**：族内第二席的第一顺位是**换字段**不是换参数 —— shrt3_bar（需求评级）与 mean_loan_rate（费率）是不同信息面，互相关可能 < 0.7。

**OS 池复核**：DEU OS 池 19 件全部 ACTIVE，无新增/变动 ⇒ 1YNMAA8M 的 self 0.6946 与 E569ZE7L 的 self 0.5444 结论仍有效。

**1YNMAA8M prod refresh 终验（第二次）= 0.6951 PASS**，与首次一致（池未漂移），暂存文件已刷新。

### 2.8 借券塔第二席突破（2026-11-10 10:1x）

**族容量从 1 席修正为 2 席**（判据 MY 证实）：

| 候选 | 字段 | 信息面 | 与 E569ZE7L 互相关 |
|---|---|---|---:|
| E569ZE7L | shrt3_bar | 借券**需求评级** | — |
| **1YNrQMr6** | max_loan_rate_p5_d1 | 借券**费率** | **0.6025 ✅** |
| E569Xd91 | max_loan_rate_main | 借券费率（同源） | 0.7095 ✗ |

⇒ 最大独立集 = 20（E569ZE7L + 1YNrQMr6 + 1YNMAA8M + 17 件 OS）。

**但 1YNrQMr6 及后续 3 个费率变体（波 AH: bl6eELlZ S1.85 / ZYQOGpR0 S1.67 / Jje6Kd9x S1.64）稳健性全 REJECT**，
根因经逐字段逐年对比定位：**费率信号在 2023 整体失效（0.19~0.53），需求评级没有（1.88）**。
换轴/换窗/换 backfill/换 tvr 共 10 个变体全部撞同一 2023 崩塌 ⇒ 参数层面无解（判据 MN）。

⇒ 修复方向：**需求评级 × 费率双字段混合**（健康腿承载主信号 + 弱腿补强度，两者互补覆盖失效年）—— 波 AI 已派出 10 条。

**DEU 域内可交付上限 = 5 颗**（分析师 1 席 + 借券 2 席 + 2 颗已 ACTIVE）。

### 2.9 借券塔第二席修复阶梯推进到第 4 档（2026-11-10 10:5x）

| 档 | 动作 | 结果 |
|---|---|---|
| 1 | 换字段（找健康信息面） | 1YNrQMr6 四闸全过，稳健性 REJECT（2023 塌） |
| 2 | 换组合算子（乘积→差值→加法） | 乘积修2023坏2021；**差值修掉2021负年**（-0.09→+0.18）且强度更足；加法与乘积同号无增量 |
| 3 | 换轴/窗口/tvr | 10 变体全撞同一崩塌，无解 |
| 4 | **专项扫该弱年（2021）的短窗口对** | **波 AN 在飞（132/66、66/44、88/44、132/88、66/22…）** |
| 5 | 放宽 CV 闸 | 需用户明确指令 |

**根因总结**：借券族**没有单一字段三年全健康**（需求评级 2021 弱/费率 2023 失效/main 2021 负）；
且 **2021 是全族共同弱年**（0.18~0.85），2022 永远最强 ⇒ 任何组合都救不了全部年份，
max/min 被单年拉爆（7.8~14.3）。

**已验证的三条方法论**：判据 MQ（差值不传染失效）、MO（年度健康度矩阵）、MX（判死族要用新骨架重测）。

## 三、待用户裁定（三项，提交需文字授权）

### 1. 提交授权（不可逆；问卷自动选中不算授权）

| 件 | 状态 | 风险 |
|---|---|---|
| **1YNMAA8M** | 四闸全过；prod refresh 0.6951 PASS；self 0.6946；18/18 独立集；ΔS+0.43；submit_gate passed；稳健性 PASS | 双闸余量各仅 0.005，与 rKRx2Alj 互相关 0.6946 贴线 ⇒ 提交前必须再 refresh 终验 |
| **E569ZE7L** | 四闸全过；prod/self 0.5444；10y 满覆盖；无负年；ΔS+0.06；ATOM 单数据集（点 SHORTINTEREST 塔） | 近三年 CV 0.626 ≥ 0.60 ⇒ 按字面 REJECT，需你明确放宽 |

**建议**：先提交 1YNMAA8M（无争议项），E569ZE7L 待 CV 闸裁定。
不建议同时提交两件（1YNMAA8M 的 self 余量会被推高）。

### 2. 稳健性 CV 闸口径
维持 0.60 ⇒ 借券族不出货；放宽至 0.65 ⇒ E569ZE7L 可提交（族内最优 + 唯一无负年 + 10y CV 最低）。

### 3. 目标数字口径
goal 标题「20 个」vs 正文第 4 条「10 个」并存。
当前本战役新挖 3 颗（2 ACTIVE + 1 待授权），含 E569ZE7L 为 4 颗。

**DEU 域内的现实约束**：分析师修正族封盘、fundamental6 封盘、attention 族强度-覆盖不可兼得、
news 族机制性无效、纯价格无效 ⇒ **DEU 域内可交付上限约 4~5 颗**。
要往 10 颗走，**必须放开「不得换 region」过程约束**（goal 明文，需你修改）。

---

## 四、本轮沉淀的判据（Agent Memory，16 条）

| 编号 | 判据 | 要点 |
|---|---|---|
| DB | OS 池漂移使旧 self 结论失效 | 发现 OS 新增件须立即重扫待提交清单 |
| DC | 自相关筛查走本地工具全扫 | check_self_correlation 零平台槽 |
| DD | 族被自己人锁死时穷举参数无效功 | 族内变体 self 全 ≥0.7 ⇒ 结构性封盘 |
| DE | 「族内只投 X」准则要用 OS 池实证推翻 | 不得凭本轮临时结论固化规则 |
| DF | preflight 的 soft 警告当硬警告 | 否则整批 CANCELLED |
| DG | 子 alpha id 在完成前是 simulation id | lookINTO_SimError_message 参数名 locations（复数） |
| MG | 族级判死看符号一致性 | 全正=强度不足 / 全负=方向反（翻转重测）/ 混合=真噪声 |
| MH | 同机制已有出货源时新源直接判死 | risk60 vs shortinterest3 |
| MI | 事件型数据须先 backfill 转面板 | cov 高 ≠ 可用（news104 cov 0.963 全灭） |
| MJ | 覆盖空窗根因 = 数据源起始年 | ts_backfill 造不出历史；多腿一腿晚则整件空窗 |
| MK | 复刻已出货骨架不要拆腿单测 | 腿间正交化贡献大部分信号（S 0.77→1.22） |
| ML | attention 类数据强度与覆盖不可兼得 | snt7 强但 2019 起；snl27 弱但满覆盖 |
| MM | 族内候选排序完整判据链 | 覆盖 → 硬闸 → self → 族内互相关 → prod |
| MN | RavenPack 事件情绪在 DEU 无横截面定价力 | 三数据集交叉验证，排除方向/覆盖/几何三因素 |
| MO | 覆盖好但信号弱 ≠ 判死理由 | 机制性判死 vs 数据性判死要分开写 |
| MP | 族容量按信息面算 | 跨件占用 vs 族内互相关，两种约束分开查 |

---

## 五、相关文件

- CRITICAL_CORRECTION_20261110.md —— mLovbnm2 撤回 + 24 颗 self 全量重算
- SEAT3_9qxnNkeq_profile.md / SEAT3_j2Y7qlA5_profile.md —— 第三席候选档案
- WAVE_MNO_VERDICT_20261110.md / WAVE_PQRS_VERDICT_20261110.md / WAVE_STU_VERDICT_20261110.md / WAVE_VU_VERDICT_20261110.md —— 波次归因台账
- THIRD_SEAT_SEARCH_LOG_20261110.md —— 第三席寻觅全日志（5 条路径）
- DELIVERY_UPDATE_20261110.md —— 交付更新
- submit_staging_1YNMAA8M.json / submit_staging_E569ZE7L.json —— 提交参数（待授权）
- submit_staging_mLovbnm2.json —— 已标记 WITHDRAWN_DO_NOT_SUBMIT