# CAMPAIGN REPORT — DEU regular_tower / INSIDERS 线（2026-11-16）— 修订 v2

> **修订说明（v2，同文件重写，不新开）**：本版按独立审读意见逐条修订。核心更正：
> ① **CW 被错误地计入了 w2 的近闸**（§0 说剔除、§2 又用 `gJaR5gov` 距 CW 0.069 计成近闸）——本版统一判据，**近闸只由 S/F/2Y 三闸决定**，w2/w4 的近闸数由 2/2 重算为 **1/1**，两波 PARTIAL 仍成立（已逐波验算）；
> ② **`+0.21/+0.18/+0.28/+0.12` 混了基线**——前三个是"掩码低带 − 同波高带"，第四个是"掩码 − 裸核"，不可并列；且 **w4 没有高带掩码臂**，所以"掩码四波一致"实际只有 **三波**；
> ③ **"w4 全项最高"与自己的表冲突**（best S 0.89 与 w2 并列、best 2Y w2 的 1.11 更高）——已改为逐项列明；
> ④ **`已点亮` 用词越界**：报告不得写"已点亮"，本版只照录 `lit` 布尔值；
> ⑤ **"合计需要 4 颗"与 16 条双塔件冲突**：双塔件是否同时计入两塔**未裁定**，本版不给"合计几颗"结论，只给分塔读数；
> ⑥ **"单集路线已封顶/边际产出趋零"是过度断言**：改为"本 run 最好 0.89，未触及外部上限 1.30"；
> ⑦ margin 的 `0.007` 量纲、`effective`/`atom`/`L2`/`vec_count` 全部补定义；
> ⑧ 6 条存量件的**取得方式与塔归属证据**补齐，并把"MODEL 是唯一保住 sub 的搭档"降级（6 条里 5 条 sub≥1.0，但只有 1 条核过塔归属）；
> ⑨ 补 §8「预答用户追问」12 条与 §9「修订对照」。
> 另：核到两处行号引用错误——DEU skill 的"禁止两腿相加"在 `insiders.md:55`（此前波档误写 `:44`），"门控只修 prod/robust 不造强度"在 `:63`。

- 范围：DEU / TOP500 / D1；**4 波 `rt-insiders-w1` … `rt-insiders-w4`，共 40 臂**；目标塔 **insiders + institutions**。
- 平台设置（4 波 10/10 臂 `get_alpha_details` 回显一致）：**decay=0、SUBINDUSTRY、truncation=0.08、nanHandling=ON**、maxTrade=OFF、maxPosition=OFF、pasteurization=ON、unitHandling=VERIFY、FASTEXPR；平台回显窗口 `startDate=2014-01-01`、`endDate=2023-12-31`。
  - ⚠ 与 `tracking/DEU/config/settings.json:5-16`（**decay=4、nanHandling=OFF**、2013-01-01 起）不同 ⇒ **40/40 臂全在探针档（decay0/nanON），区域生产档一次未跑**。本报告结论只在探针档内成立。
- 证据来源：
  1. ask 给定的塔位实读（`campaign_intel.py pyramid` / 平台 `get_pyramid_alphas` 当季实读）；
  2. **前序四波归因步骤已执行的平台只读 GET**：40 次 `batch_get_alpha_metrics`（40/40 success）+ 40 次 `get_alpha_details`（逐臂取 `settings`/`metrics`/`ra`/`checks`/`pyramids`/`code`）；另 1 次 `batch_get_alpha_metrics`（6 条存量件，6/6 success）；
  3. DB `wave_results`（DB id **2228 / 2230 / 2238 / 2239**，`status=closed`、`source_file=pipeline:auto`）与 `list_expressions(DEU, rt-insiders-w{1..4})`（4×10 条，与输入件逐条同序）；
  4. 4 份波次档案 `tracking/DEU/regular_tower/WAVE_rt-insiders-w{1..4}_20261116.md`；
  5. `tracking/DEU/config/thresholds.json`、`src/wqb/config.py:502`、`src/wqb/wave_results_contract.py:79-90`。
- **"零平台调用"的口径**：指**本报告（含本修订轮）的写作步骤**未发起任何平台请求、未提交、未消耗配额。上列第 2 项的 80+6 次只读 GET 是**前序波次归因步骤已经发生**的，不在本次重跑；本版**没有**再用 MCP 复核任何读数或塔位。
- **声明**：本报告不写"已点亮"。所有颗数/倍率均为**条件式计数**；`mult` 与 `lit` 的平台语义未在 ask 中定义，本报告只照录数值（§5.1-6）。

## §0 术语与口径（先读）

| 项 | 本报告口径 | 出处 |
|---|---|---|
| **margin 单位** | 平台 `margin` 是**小数**，1bp = 0.0001；闸 `margin_min = 0.0005` = **5bp**。本 run 40 臂实读区间 **[−0.001489, +0.006263]**（−14.89bp ~ +62.63bp），**全距 0.007752**。⇒ "距闸 0.4" 是该指标全距的 **51 倍**，阈值在 margin 上无分辨力 | `thresholds.json:7`；40 臂 `get_alpha_details.checks` |
| **effective** | 平台 `pyramids.effective` = 该 alpha **归属的塔数量**（1=单塔，2=双塔）。它是**属性计数**，不是权重、不是倍率；与本 run 的 `multiplier=1.6` **无算术关系**（1.6 是每座塔的独立字段，双塔件会有两个 1.6） | 40 臂 `get_alpha_details.pyramids` |
| **atom** | `expressions.atom_flag="atom"` 且 `atom_n_datasets=1` = 表达式只引用一个数据集。"单集表达式即 ATOM，免 IS_LADDER" | `FIELD_insiders1_20261116.md:209`；`list_expressions` 40 条 |
| **L1 / L2 / L3** | 沿用同目录 fundamental 报告 §3.2 的三层闸命名：**L1** = 平台 RA 18 项；**L2** = 提交前置（SELF/PROD/DATA_DIVERSITY 状态 + prod/self corr + 年度分年 + 项目五道闸）；**L3** = 用户确认 + `confirm_submit=True`。⚠ 这套 L1/L2/L3 **只在本报告内有效**，与 AGENTS.md 里 skill 的 `layer` 字段（`L-RA` / `L0`–`L7`）**不是同一套编号** | 同目录 `CAMPAIGN_REPORT_20261116.md` §3.2 |
| **近闸（本版统一判据）** | 只对 **量纲与 0.4 可比**的三闸计近闸：**S（1.58）、F（1.0）、2Y（1.58，含 `IS_LADDER` year=2）**——这三闸取值区间约 [−1, 3]，0.4 ≈ 满量程 10–15%，有分辨力。**CW（limit 0.10）、margin（limit 0.0005）、sub（平台 limit 逐臂 0.09–0.42）只登记、不计入**；**本地 review 线（sub 1.0 / CW 0.5）不参与近闸判定**。TO 本 run 10/10 全 pass、无缺口 | `thresholds.json:3,4,5`；各臂 `checks.fail.limit` |
| **`vec_count(F)`** | 平台向量算子，返回**当日该 VECTOR 字段的事件条数**。FIELD 档 §4.2 实测 5 个字段的 `vec_count` 逐位相同 | `FIELD_insiders1_20261116.md` §4.2 |
| **波级判定** | `verdict_from_counts`：**PASS** = ≥1 条过 RA 层全闸；**PARTIAL** = 0 达标但 ≥1 近闸；**FAIL** = 0 达标 0 近闸。本报告不自造枚举 | `src/wqb/wave_results_contract.py:79-90` |
| **RA 层全闸** | 平台 `ra.failed_ra_count = 0`；⚠ 只表示 RA 18 项全过，**不等于可提交** | `src/wqb/config.py:393-401,410-412` |
| 矛盾表述的处理 | 平台 `checks.fail=[]` 但 `ra.failed_ra_count>0` 的臂，一律以 `ra_failed_checks` 判 fail | `src/wqb/config.py:410-412`；AGENTS §8.7 |

## §1 塔位现状与优先级判断

⚠ **先读这条免责**：下表是 ask 给定的快照（`campaign_intel.py pyramid` / `get_pyramid_alphas` **当季**实读）。该工具对平台响应用 **1 小时 sqlite 缓存**（键 `pyramid_alphas:<hash>`，TTL 3600）；同目录 fundamental 报告 §11.3 有实证：**同一 turn 内该工具读 2、MCP 直读为 3**。**本报告未用 MCP 复核塔位**（指令要求只写档案、不做平台调用）⇒ **下文所有"差 N 颗"只以本快照为限**；若复核后某塔变为"差 1 颗"，§1 的优先级排序需**整体重排**。
 （唯一可做的交叉印证：本快照的 `fundamental=3` 与该报告 §11.3 的 MCP 直读 **一致**，说明该快照至少在这一项上不落后于平台；其余 15 条无交叉印证。）

塔位快照（**ask JSON 共 16 条记录，逐条照录；本报告无法判断平台是否还有图中未列出的塔**）：

| 塔 | alphas | need（差几颗） | mult | lit（**照录布尔值，不解释口径**） | 与目标塔的关系 |
|---|---:|---:|---:|:---:|---|
| insiders | 1 | 2 | 1.6 | false | **目标塔 A** |
| institutions | 1 | 2 | 1.6 | false | **目标塔 B** |
| sentiment | 1 | 2 | 1.8 | false | 非目标 |
| news | 0 | 3 | 1.8 | false | 非目标 |
| option | 0 | 3 | 1.7 | false | 非目标 |
| pv | 0 | 3 | 1.6 | false | 非目标 |
| earnings | 0 | 3 | 1.5 | false | 非目标 |
| macro | 0 | 3 | 1.5 | false | 非目标 |
| risk | 0 | 3 | 1.5 | false | 非目标 |
| socialmedia | 0 | 3 | 1.5 | false | 非目标 |
| imbalance | 0 | 3 | 1.2 | false | 非目标 |
| analyst | 6 | 0 | 1.8 | true | 非目标 |
| fundamental | 3 | 0 | 1.8 | true | 非目标 |
| model | 3 | 0 | 1.8 | true | 非目标 |
| other | 3 | 0 | 1.8 | true | 非目标 |
| shortinterest | 5 | 0 | 1.3 | true | 非目标 |

**读数（严格限定在快照内）**：
1. **按本快照，16 条记录里没有 `need=1` 的塔**：5 座 `need=0`（`lit=true`）、**3 座 `need=2`**（sentiment / insiders / institutions）、**8 座 `need=3`**（0/3）。
2. 两个目标塔各为 **1/3、各差 2 颗**（分塔口径）。
3. `mult` 读数：未点亮的 11 座里最高是 **news 1.8 与 sentiment 1.8**（并列），其次 option 1.7，再是 pv / insiders / institutions 1.6。
   ⚠ **`mult` 语义未定义**（乘在 alpha 还是整塔、何时生效、持续多久，ask 未给）⇒ 本报告**不把它当收益乘数、不据此算"投入产出比"**（v1 那句"投入产出比更高"已删除）。

**优先级判断（推荐，不代替用户决策）**：
- **P0 — insiders（1/3，差 2，1.6）**：目标塔；本 run 4 波 40 臂对它**增量 0**（§2/§3）。
- **P1 — institutions（1/3，差 2，1.6）**：目标塔；本 run 只以**第二腿**身份出现（16 条双塔件），**从未作为主核**——依据是四波 40 条表达式全文（`logs/_tmp_rt-insiders-w{1..4}_arms.json`）与 DB `list_expressions` 40 条，institutions6 的字段只出现在掩码 / bucket / 加权里。
- **P1.5 — sentiment（1/3，差 2，1.8）**：非目标。**若只看"差几颗"，它和两个目标塔成本相同（都差 2 颗）；差别只在 `mult` 读数（1.8 vs 1.6），而 `mult` 语义未定义** ⇒ 本报告**不**据此声称它更划算，只把"是否放宽目标塔范围"列为待裁定事项（§7）。
- **P3 — 8 座 0/3 塔**：需 3 颗（分塔口径），比两个目标塔各多 1 颗；其中 news（1.8）/ option（1.7）倍率读数较高。
- **不再投入 — 5 座 `need=0` 的塔**（analyst / fundamental / model / other / shortinterest）。

**一条不能当作"本 run 候选"的存量事实**：平台实读 DEU 有 **6 条 `failed_ra_count = 0` 的 IS 存量件**，全部 `status=UNSUBMITTED`（`batch_get_alpha_metrics` 6/6 success，w1 实读）：

| alpha | S | F | 2Y | sub | TO | DD | margin | 塔归属（平台实读？） |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| `Vk6eodeb` | 1.63 | 1.41 | 1.66 | 1.49 | 12.43% | 5.58% | 15.0bp | **已核**：`pyramids` = INSIDERS×1.6 + MODEL×1.8（eff 2） |
| `akLG3VgO` | 1.82 | 1.70 | 2.12 | 1.43 | 12.17% | 6.11% | 18.0bp | **未核**（只取指标） |
| `RRVPLpG0` | 1.88 | 1.66 | 1.78 | 1.00 | 12.96% | 5.83% | 15.7bp | **未核** |
| `le81ZVo5` | 1.91 | 1.69 | 1.85 | 0.96 | 11.22% | 5.78% | 17.5bp | **未核** |
| `O0rgvJgR` | 1.76 | 1.65 | 1.64 | 1.36 | 12.15% | 9.25% | 18.2bp | **未核** |
| `qMWVeeME` | 1.64 | 1.42 | 1.67 | 1.51 | 12.42% | 5.47% | 15.1bp | **未核** |

- **来源与取得方式**：指标列与 `status=UNSUBMITTED` 来自 `batch_get_alpha_metrics`（w1 实读 6/6）；**塔归属只有 `Vk6eodeb` 逐条核过**（`get_alpha_details.pyramids`）。其余 5 条**没有平台塔归属读数**，只能由 2026-09-13 的 DEU `wave_results` 记录（DB id **748** 焦点"R93 修正波"、**749** "R94"、**750** "R95"，`source_file=manual-direct-send (spawn-hang workaround) 2026-09-13`）的条目文字归到 insiders 族——**属"由记录条目推断"，不是平台实读**。
- ⚠ **它们不是 6 条独立候选**：同批记录（id 749）明写 `qMWVeeME` 与 `Vk6eodeb` **0.9974 同源**（"event-value 家族锁死"），id 748 另记 `Vk6eodeb` vs `Vk65zLzG` 相关 0.6262、`RRVPLpG0`/`le81ZVo5` vs `2rOe10qY` 0.956/0.9093 ⇒ **self-corr 会先筛掉大部分**。
- ⚠ **`Vk6eodeb` 的形态已不合现纪律**：平台实读 `code` 为**五腿 `add`**（`significant_value_1` + 四条 MODEL 预估字段），而 DEU skill 明令"禁止两条独立信号腿相加（含等权 `add`）；第二个数据集只以**条件 / 分组 / 残差**入场"（`Claude/skills/wq-brain-ra-deu/references/insiders.md:55`）。⇒ 它可作塔位备选，但**不是可复用配方**，也不能当本族单集/配对结论的反证。

**关于"几颗能点亮两塔"——本报告不下结论**：平台 `pyramids.list` 对 16/16 双塔件**同时列出两个塔名**（INSIDERS×1.6 + INSTITUTIONS×1.6），但"一条双塔 alpha 是否同时计入两塔的 `alphas` 计数"**未经验证**。若计入，2 条双塔件理论上可让两塔各 +2；若不计入，则需 4 颗。**两种口径都未被证实**，本报告只给"两塔各差 2 颗"的分塔读数。

## §2 本 run：4 波逐波读数

| 波 | 臂数 | 结构构成 | best S（alpha） | best 2Y（alpha） | 近闸（**本版重算**） | 波级判定（DB id） |
|---|---:|---|---|---|---:|---|
| `rt-insiders-w1` | 10 | 5 单集/单塔 + 5 双集/双塔（**5 条配对臂全带平台 UNITS 警告**） | **0.81**（`oma3GYeb` 臂7） | **1.17**（`vRAeGm0Q` 臂8） | 0 | **FAIL**（2228） |
| `rt-insiders-w2` | 10 | 5 单集/单塔 + 5 双集/双塔（单位已修，无 UNITS） | **0.89**（`d5aE63Ew` 臂3） | **1.11**（`QP02ANn5` 臂6） | **1** | **PARTIAL**（2230） |
| `rt-insiders-w3` | 10 | 6 单集/单塔 + 4 双集/双塔 | **0.78**（`RReNJvre` 臂3） | **0.93**（`RReNJvre` 臂3） | 0 | **FAIL**（2238） |
| `rt-insiders-w4` | 10 | 8 单集/单塔 + 2 双集/双塔 | **0.89**（`LLKnekRL` 臂1，**与 w2 并列**） | **1.05**（`Jj8nlbpW` 臂7） | **1** | **PARTIAL**（2239） |

### 2.1 近闸重算（回应审读意见 2/4/5/10）

**统一判据见 §0**：只计 S / F / 2Y 三闸，CW / margin / sub 只登记不计入，本地 review 线不参与。逐波结果：

| 波 | 旧口径（v1） | 本版 | 命中臂与方向 | verdict 是否变 |
|---|---|---|---|---:|
| w1 | 0 | **0** | 无（臂1/臂4 只"距 TO 上限 0.376"且 S −0.11/−0.07、DD 89–91% ⇒ 不计） | 否（FAIL） |
| w2 | 2 | **1** | `d5aE63Ew` F 0.63 vs 1.0 ⇒ **差 0.37 ≤ 0.4**。`gJaR5gov` 的命中是 **CW 0.168741 vs limit 0.10 ⇒ 已超限 0.0687（不是"还差"）**，按新判据只登记不计入 | **否**（仍 ≥1 近闸 → PARTIAL） |
| w3 | 0 | **0** | 无（臂3 最好，但 F 距 0.57 / S 距 0.80 / 2Y 距 0.65 全部 >0.4） | 否（FAIL） |
| w4 | 2 | **1** | `LLKnekRL` F 0.67 vs 1.0 ⇒ **差 0.33 ≤ 0.4**。`MP6bwkGM` 的命中是本地 sub 线 1.0 的差额 0.32，但平台 `LOW_SUB` 对它判 **PASS** ⇒ 按新判据只登记不计入 | **否**（仍 ≥1 近闸 → PARTIAL） |

⇒ **两波 PARTIAL 的构成从 2/2 改为 1/1，判定结论不变**（判定表只要求"≥1 近闸"）。

### 2.2 institutions 侧（第二腿）sub 实测（回应审读意见「0.21 无出处」）

16 条双塔件（institutions6 只作第二腿）逐波 sub：

| 波 | 双塔臂数 | sub 区间 | 该波最大值臂 |
|---|---:|---|---|
| w1 | 5 | [−0.06, +0.08] | 臂8 `vRAeGm0Q` 0.08 / 臂9 `N1PgzOk8` 0.08 |
| w2 | 5 | [+0.09, **+0.21**] | 臂9 `VkNXvRpb` **0.21（16 条里的最大值）** |
| w3 | 4 | [−0.12, +0.15] | 臂7 `qM7nKwAA` 0.15 |
| w4 | 2 | [−0.11, +0.10] | 臂3 `pwan087v` 0.10 |

⇒ 准确表述：**16 条 institutions6 第二腿件的 sub 全部落在 [−0.12, +0.21]**，最大值 0.21（w2 臂9）；**没有一条 ≥1.0**。w1 的 5 条另带 UNITS 警告，其读数不作结论。

### 2.3 极值与并列关系（回应审读意见「w4 全项最高」）

| 指标 | 四波最好值 | 归属 | 是否唯一 |
|---|---|---|---|
| S | **0.89** | w2 臂3 `d5aE63Ew` / w4 臂1 `LLKnekRL` | **并列** |
| F | **0.67** | w4 臂1 | 唯一（w2 最高 0.63） |
| 2Y | **1.17** | w1 臂8 `vRAeGm0Q` | 唯一（w4 最高 1.05，**低于 w1/w2**） |
| sub | **0.68** | w4 臂10 `MP6bwkGM` | 唯一（长侧仅 55 只，§5.3） |
| margin | **62.63bp** | w4 臂1 | 唯一 |
| TO 最低 | **1.94%** | w3 臂3 / w4 臂4 | 并列 |
| DD 最低 | **8.48%** | w4 臂9 `1YWovJdJ` | 唯一（**ask 括注称臂7 最低，实读臂7 为 10.37%、次低 ⇒ 本报告更正**） |

⇒ 准确表述：**w4 在 F / sub / margin / 最低 DD 四项为四波最好，且 best S 与 w2 并列；但 best 2Y 属于 w1（1.17）**。v1 的"w4 均四波最高"已作废。

## §3 候选与塔位增量预测（**未提交，点亮需用户确认**）

**结论：本 run 的塔位增量预测 = 0 颗（insiders 0 / institutions 0）。**

理由（三层都不成立）：
1. **L1（RA 层）**：40/40 臂 `failed_ra_count ≥ 3`，**没有一条过 RA 全闸** ⇒ 连"RA 层全过件"都没有。
2. **强度层**：三条近闸件距主闸仍远——
   | 臂（波） | S | S 距闸 | F | F 距闸 | 2Y | 2Y 距闸 | 命中项 |
   |---|---:|---:|---:|---:|---:|---:|---|
   | `d5aE63Ew`（w2 臂3） | 0.89 | 0.69 | 0.63 | **0.37** | 0.92 | 0.66 | F |
   | `LLKnekRL`（w4 臂1） | 0.89 | 0.69 | 0.67 | **0.33** | 0.86 | 0.72 | F |
   | `MP6bwkGM`（w4 臂10） | 0.82 | 0.76 | 0.53 | 0.47 | 0.81 | 0.77 | 本地 sub 线（平台 PASS，不计入） |
   ⇒ **近闸只是单项接近，三条没有一条 S 距闸 <0.69**。
3. **口径层**：40/40 臂都在 **decay0 / nanHandling=ON** 探针档；区域生产档（decay4 / nanOFF）一次未跑。按 DEU skill「设置是强度闸，跨档结果不可比」（`insiders.md:65`），本 run 读数**既不能外推为"生产档不可行"，也不能外推为"生产档可行"**。

**本 run 无正式待确认提交候选（rollup `[]`）。** 三条近闸件的最小前置（**本报告不执行**）：
- `LLKnekRL`：结构最简（`list_expressions` id 109942：`atom_flag=atom`、`atom_n_datasets=1`；`pyramids`=INSIDERS 单塔 eff 1；表达式为单层 `ts_ir`，无 `group_rank`）⇒ 先 prod/self，再年度分年，再五道闸。
- `d5aE63Ew`：与 `LLKnekRL` 同为 S 0.89，但结构是乘法复合（`multiply(rank(conc),rank(fresh))`），F 略低；同样先 prod/self。
- `MP6bwkGM`：**先拆解释**——补 `vec_count == 1` 分支 / 等样本数对照，分离"多笔日信息量更高"与"长侧仅 55 只"两种解释，再谈 prod；否则 sub 0.68 不可解释。

**塔位计数**：分塔各差 2 颗；"一条双塔件是否同时计入两塔"未裁定（§1 末），故**不给"合计需几颗"的结论**。本 run 不产生任何可能改变计数的件。

## §4 明确不做的

1. **不做提交 POST**：未调用 `workflow_submit_alpha(confirm_submit=True)`、`create_spc_submission`、`set_spc_submission_weight`、`/alphas/{id}/submit` 中的任何一个。
2. **不消耗配额**：本报告的**写作与修订步骤**零平台调用、零仿真、零提交；4 波 40 臂的仿真已在前序执行，本步骤不重复，也不为"探一探"再发任何臂。
3. **不做数据终态写动作**：无 `seal_dead_end`、无 dataset 状态改写；ask 的「无终态变更」照录。
4. **不取提交前置读数**：prod / self / DATA_DIVERSITY、年度分年、self-corr、互相关，本步骤一律未查；`alphas.prod_correlation/self_correlation` 40/40 为 **null**（未测，不是 0）。
5. **不做跨区外推**：所有对照都在 DEU 域内，且**只用了本 run 四波 + 2026-09-13 的 DEU 存量件记录**；**未使用** fundamental 线的波次读数做任何对照（v1 把它列为"对照"却未使用，本版删除该表述）。
6. **不改动既有报告**：未覆写 `CAMPAIGN_REPORT_20261116.md`（fundamental 线）。

## §5 未覆盖与盲区

### 5.1 证据通道盲区（先读；这几条会让"看起来有结论"变成假结论）

1. **塔位快照有 1h 缓存陷阱**（已上移到 §1 表头）：`tools/campaign_intel.py pyramid` TTL 3600，同日早前实测过"工具读 2、MCP 直读 3"。**本报告未复核**。
2. **"不在判死名单" ≠ "活着"**：`get_dead_datasets("DEU")` 只读 `*_dead` 台账键；`insiders1` 不在其中只说明**从未封过判死**。
3. **本地数据集画像表对 DEU 是空的**：`query_dataset_profile(DEU)` 返回 **count=0**（w1 实读）⇒ 本报告**不用**数据集画像做任何判据。
4. **DB 只覆盖"经 upsert 落库"的臂**：本 run 每波收割后都显式调用 `upsert_backtest_rows(region=DEU, wave=<波>, dataset=insiders1, rows=10)`（回执 n=10），该写入方同时写 `backtest_results` 与 `expressions`（AGENTS §8.8）⇒ **这就是 40 条能被 `list_expressions` 回读的原因**。盲区指的是**未走 upsert 的 MCP 直连仿真**（AGENTS §8.11 ⑦）：那类尝试对本档完全不可见，故本报告不宣称"平台侧无其他同族尝试"。
5. **`checks.fail` 与 `ra.failed_ra_count` 会不一致**：多波出现 `checks.fail=[]` 但 `ra.failed_ra_count>0`（LOW_SHARPE/LOW_FITNESS/LOW_2Y 落在 `checks.warning` 带 value/limit）⇒ 本报告一律以 `ra_failed_checks` 判 fail（`src/wqb/config.py:410-412`、AGENTS §8.7）。
6. **`mult` / `lit` 语义未定义**：倍率乘在什么对象、从何时生效、`lit` 计入 SUBMITTED 还是 ACTIVE，ask 均未给 ⇒ 只照录数值，**不解读为收益乘数，也不写"已点亮"**。

### 5.2 判死六维闸（D1–D6，四波累计）

| 维 | 现状与**证据指针** | 判定 |
|---|---|---|
| **D1 结构互异 ≥10** | **17 个**（逐条枚举，不收敛区间）：① holdings Δ66（含 z 化 / 比率两壳，w1）② holdings 事件新鲜度 `days_from_last_change(vec_avg)`（w2 臂1）③ valueeur 集中度 `max÷sum`（w1 臂7 / w2 / w4）④ valueeur 离散度 `stddev÷sum`（w2 臂2）⑤ 乘法 集中度×新鲜度（w2 臂3 / w3 臂5 / w4 臂5）⑥ 减法 集中度−`ts_ir`（w2 臂4）⑦ institutions 硬掩码（w1–w4）⑧ institutions bucket 分组（w2 臂9）⑨ institutions 互补加权 `g` / `1−g`（w3 臂6/7）⑩ institutions 有符号斜率 `reverse(group_zscore)`（w4 臂2）⑪ shares 集中度 + `ts_rank252`（w3 臂1 / w4 臂6）⑫ shares 集中度 `ts_ir`（w3 臂3 / w4 臂4/7）⑬ shares `trade_when` 事件门控（w3 臂4）⑭ shares 离散度（w3 臂10）⑮ `vec_count` 事件新鲜度（w3 臂2 / w4 臂9）⑯ 事件频率 `ts_sum(vec_count)`（w4 臂8）⑰ 事件条件 `ts_ir`（`vec_count>1`，w4 臂10） | **✓ 达**（17 ≥ 10） |
| **D2 字段族自测** | 分母 = `insd1_` 的 **6 个信号字段**：`holdings` / `valueeur` / `shares` / `tradesignificance` / `price` / `value`（另 2 个字段 `insd1_gvkey`、`transaction_currency_code` 是标识符/标签，非信号）。**已测 3**（holdings、valueeur、shares）；**未测 3**（`price` / `value` / `tradesignificance`） | **✗ 未达**（3/6） |
| D3 矩全家 | 水平：w1 臂7（`rank(ts_sum(max÷sum,66))`）、w4 臂1/4/7（`ts_ir` 的水平统计）；一阶差：w2 臂5（`ts_delta(ts_sum(conc,66),66)`，S 0.19）；二阶波动：w2 臂2 / w3 臂10（`vec_stddev÷vec_sum`）；比值：`max÷sum`、`stddev÷sum`；信噪比：`ts_ir`（w3 臂3、w4 臂1/4/7/10） | ✓ 达 |
| D4 分组轴 ≥2 | sector（w1/w2 多数臂）、subindustry（w3 臂3/6/7、w4 臂4/7/8/10）、bucket（w2 臂9） | ✓ 达 |
| D5 非线性 ≥1 | `multiply`（w2 臂3 等）、`if_else`（w1 臂3、w4 臂3/10）、`trade_when`（w3 臂4）、`bucket`（w2 臂9）、`ts_rank`、`ts_ir`、`reverse` / `group_zscore`（w4 臂2） | ✓ 达 |
| **D6 配置 ≥2** | 四波**同一套**探针档（decay0 / nanON / SUBINDUSTRY / trunc0.08）；**decay4 / nanOFF 一次未跑** | **✗ 未达** |

- D2 的"族级判死先验 S 1.13/1.14/1.21"出处：`Claude/skills/wq-basket-composition/references/deu-insiders-evidence.md:47-54` 的"完整判死清单"（`price` 1.13 / `value·valueeur` 1.14 / `tradesignificance` 1.21）。⚠ 该清单是 **insiders 族（姊妹集 + `vec_avg` 几何）** 的读数，**不是 `insd1_*` 原生几何**；按 AGENTS §7.6「禁止凭族先验封禁未测字段」，它们**不能替代本集实测**。
- ⇒ **缺 D2 / D6，`insiders1` 只能记 `provisional`**：不得判死、不得封集、不得作邻接集先验。但如实说：**判死资格"只剩两维"**，且 D2 未测的三个字段恰是族内最有"已判死先验"的三个。

### 5.3 其它盲区

- **符号指纹（翻符号对照）四波全未测**：40 条表达式**无一条整式取反**，ask 的严格判据（S(−expr)≈−S(expr) 且 TO/DD/longCount 逐位相同）无法执行。
- **"掩码单独对照"四波均缺**：从未跑 `if_else(cond, 1, 0.5)` 类纯掩码臂。四波只能**间接**证明该缺口有害（§6.3）。
- **窗口只有两个点（66 / 252）**：ask 的「22→66→132 单峰」衰减梯**未扫**，不能判"单峰"，只能判"252→66 上升"（w4 臂4 vs 臂7）。**另注**：40 臂里 24 条单集臂的窗口并非全为 66——w1 的 holdings-Δ 用的是 `ts_delta(·,66)` + `ts_std_dev(·,252)` 混用，故本报告**不再使用"单集 66 窗路线"这个说法**，改称"单集路线（窗口仅 66/252 两点）"。
- **年度分年未取**：40 臂均未取 `get_alpha_yearly_stats`。ask 提到 `XgaGb3J1` / `d5a2aO7v` 已核十年，但**二者不在本 run 40 臂内，本报告亦无其表达式/读数** ⇒ **不转录、不引用、不作为依据**。
- **单侧宽度不对称**：w4 臂10 长侧 **55** / 空侧 145，**两者之和 200 是该臂的持仓只数（55+145），不是宇宙容量**（TOP500 宇宙约 500 只，该臂只持有 200 只）。CW 平台判 PASS、无宽度塌缩，但 sub 0.68 建立在薄长侧上，可靠性受限。
- **6 条存量件只核了 1 条的塔归属**（§1），其余 5 条的平台 `pyramids`/`code` 未取。
- **w1 的 5 条配对臂带 UNITS 警告**（对 CSShare 字段加无量纲 1）⇒ w1 的配对读数不作结论；w2 起已修干净（10/10 无 UNITS）。
- **未做论坛取证 / 未判死**：本 run 无 `forum_recon`、无 `dead_end` 封存。

## §6 四波可复用结论（跨波，供下一棒直接取用）

### 6.1 单集路线的位置（改写过度的表述）

- **外部独立证据**：`BE176` 三波收敛 **`insiders1` 单集 S 上限 ≈1.30**（1.22 / 1.30 / 1.19，30 臂；`tracking/DEU/atom_orthogonal/BE176_INSIDERS1_CEILING_130_20261112.md:23,28-30`）。
- **本 run 观测**：四波最强 **0.81 / 0.89 / 0.78 / 0.89**。
- ⇒ 准确结论：**本 run 的最好值（0.89）离外部上限（1.30）还差 0.41，也没有任何一波接近该上限**。因此只能说"**本 run 未触及外部上限**"；**不能说"已封顶"、也不能说"边际产出为零"**（后者需要至少一条"同几何重复且读数不变"的证据，本 run 四波换的是字段/壳，不是同一几何的重复）。

### 6.2 三条正向杠杆（跨波复现，逐波给数）

| 杠杆 | 逐波对照（改造件 vs 裸件） | S / F / 2Y 的逐波差 |
|---|---|---|
| **集中度 × 事件新鲜度 乘法交互** | w2 臂3 `d5aE63Ew` 0.89/0.63/0.92 vs 左腿 w1 臂7 `oma3GYeb` 0.81/0.50/0.83（表达式逐字相同）<br>w3 臂5 `MP6bj2po` 0.55/0.26/0.58 vs 臂1 `2r5v12Kb` 0.17/0.04/−0.23（纯单变量）<br>w4 臂5 `QP0neEaX` 0.56/0.27/0.41 vs 臂6 `9ql9oJw9` 0.20/0.05/−0.47（纯单变量） | S **+0.08 / +0.38 / +0.36**<br>F **+0.13 / +0.22 / +0.22**<br>2Y **+0.09 / +0.81 / +0.88** |
| **离散度（`vec_stddev÷vec_sum`）> 集中度（`vec_max÷vec_sum`）** | w2 跨波：`mLarN0x1` sub 0.44 vs w1 臂7 sub 0.19（不同壳，弱对照）<br>w3 单 token 消融：臂10 `Jj8nV2OE` 0.44/0.18/0.56 vs 臂1 `2r5v12Kb` 0.17/0.04/−0.23（只差 `vec_max`→`vec_stddev`） | w3：S **+0.27** / F +0.14 / 2Y **+0.79** / sub **+0.47** |
| **事件时钟用金额 > 用交易条数** | w4 臂9 `1YWovJdJ` 0.43/0.17/0.32 vs w3 臂2 `O0Wn129p` 0.27/0.08/0.09（同壳、只换 `ts_backfill` 里的字段） | S **+0.16** / F +0.09 / 2Y **+0.23** / sub **+0.22** |

### 6.3 四条已证伪 / 不可用的轴（**正负号定义已写明**）

| 轴 | 定义 | 证据（同基线对照） | 结论 |
|---|---|---|---|
| `trade_when(…, −1)` 事件门控 | 门控失败即全额做空 | w3 臂4 vs 臂1（同核，仅加门控）：**Δ = 门控件 − 无门控件** = S **−0.40**、DD **+14.34pp**、sub −0.36 | 负杠杆，不用 |
| 减法复合 `subtract(rank(A), rank(B))` | 两腿秩相减 | w2 臂4 vs 被减腿（w1 臂7）：Δ = −0.97 S、DD +30.66pp、票池 129-140→31-30 | 破坏性（且缺 `ts_ir` 单腿对照，不可完全归因） |
| 有符号斜率 `reverse(group_zscore(inst))` | 机构持股 z 值取反后加权 | w4 臂2 vs 裸核 w4 臂6：Δ = **−0.64 S**、DD 32.32%（四波最高） | 把信号翻转，不用 |
| 硬 `if_else(…, 0.5)` 掩码的"低机构持股是强侧" | 掩码低带 vs 同波高带 | **只有三波有同基线对**：w1 臂8 − 臂9 = 0.74−0.53 = **+0.21**；w2 臂7 − 臂8 = 0.75−0.57 = **+0.18**；w3 臂8 − 臂9 = 0.27−(−0.01) = **+0.28**（正号 = 低带强）。**w4 没有高带掩码臂**，只能算"掩码 vs 裸核" = 臂3 − 臂6 = 0.32−0.20 = **+0.12**（**不同基线，不可与前三并列**） | 掩码三波同基线一致（低带强），但**所有显式加权形态反号**：w3 臂7 `x·g` 0.33 vs 臂6 `x·(1−g)` −0.22（Δ 高带−低带 = **+0.55**），且两臂逐元素相加 ≡ 裸腿 ⇒ **"低带强"是掩码形态的产物（自带 0.5 常数腿），不得作经济方向或外推** |

### 6.4 两条形态内部的取舍（不是优劣，是价格）

- **`ts_ir` 窗 66 vs 252**（w4 臂4 vs 臂7，纯单变量）：66 窗 S **+0.21** / F +0.18 / 2Y **+0.47** / sub **+0.40**，代价 TO **+3.50pp** / margin **−17.99bp**。
- **subindustry 分组 vs 无分组**（w4 臂1 vs 臂4，纯单变量）：分组 S **−0.22** / F **−0.33** / 2Y −0.28 / margin **−28.50bp**，换 sub +0.17 / DD −3.22pp / 宽度 +54 只。⚠ 这条**更正 w3 档"分组效应量 ≤0.1"的推断**——该推断只适用 sector 轴。

## §7 总结

- **塔位（限定在本快照）**：16 条记录里**没有 `need=1` 的塔**；两个目标塔 **insiders 1/3（差 2，`mult` 1.6）**、**institutions 1/3（差 2，`mult` 1.6）**；同样差 2 颗的 sentiment 的 `mult` 读数是 1.8，但 `mult` 语义未定义，不能据此算性价比。
- **本 run**：4 波 40 臂，**0 条过 RA 层全闸**；波级 0 PASS / 2 PARTIAL / 2 FAIL（PARTIAL 的近闸按统一判据各为 1 条）；**塔位增量预测 = 0 颗**。四波最好值：S 0.89（w2/w4 并列）、F 0.67（w4）、2Y 1.17（w1）、sub 0.68（w4，长侧仅 55 只）、margin 62.63bp（w4）。
- **数据集**：`insiders1` 四波维持 **provisional**（不判死、不 `data_excluded`、不封集）；本 run **无数据集终态变更**；六维只差 **D2（3/6 字段）/ D6（单配置）**。
- **可复用资产**：3 条跨波正向杠杆 + 4 条已证伪轴 + 2 条形态取舍。它们是**结构知识**，目前**没有一条能把候选推到闸口**。
- **待用户裁定的三件事**（本报告不代替决策，逐条给"本报告已知/未知"）：
  1. **是否继续 insiders 单集路线**：已知本 run 最好 0.89、外部上限 1.30、D2/D6 未达；未知"补齐 D2/D6 后能否突破 1.30"（无法从现有读数推断）。
  2. **是否把范围放宽到 sentiment（同差 2 颗、同一快照）**：已知其 `mult` 读数 1.8 > 1.6；未知 `mult` 语义与 sentiment 面的实际强度（本 run 未测）。
  3. **是否允许 MODEL 作第二腿**：已知平台实读的 6 条存量件里 5 条 sub≥1.0、其中唯一核过塔归属的 `Vk6eodeb` 是 INSIDERS+MODEL；未知其余 5 条是否也是 MODEL 搭档。⚠ **与"禁止两腿相加"不冲突**：`insiders.md:55` 禁的是 `add` 型并列，**明确允许**第二数据集以条件（`trade_when`/`if_else`）、分组（`group_rank`/`bucket`）或残差入场——所以"MODEL 作第二腿"若走条件/分组/残差形态是合规的；不合规的是 `Vk6eodeb` 那种五腿 `add`。

**待确认提交候选：无（`[]`）。**

## §8 预答用户追问（审读员列的 12 条，逐条给答案或"不知道"）

1. **"6 条存量件达标，为什么待确认候选是 []？"** — 因为"RA 层全过"只是 L1。它们的 L2 全部未做：`prod_correlation`/`self_correlation` 未测（`batch_get_alpha_metrics` 返回 null）、年度分年未取、五道闸未跑；且 id 749 记录明写其中两条（`qMWVeeME` / `Vk6eodeb`）**0.9974 同源**、id 748 记录另记 `RRVPLpG0`/`le81ZVo5` 与 `2rOe10qY` 0.956/0.9093 ⇒ self-corr 会先筛掉大部分。**它们该由谁在何时查**：属下一棒的"存量收割"步骤（prod/self → 分年 → 五道闸 → 用户确认）；本报告不做、不承诺时点。
2. **"能不能现在 MCP 直读复核塔位？"** — 本报告按指令"只写档案，不做平台调用"，**未复核**。复核入口是 `mcp__wq-brain-http__get_pyramid_alphas`（直读，绕开 1h 缓存）。**若某塔实为 `need=1`，§1 的 P0/P1/P1.5 排序需整体重排**——这是本报告最大的单点风险。
3. **"4 颗 vs 16 条双塔件，哪个对？一条双塔会不会同时记两塔？"** — **本报告不知道**。已知：平台 `pyramids.list` 对 16/16 双塔件同时列出两塔名；未知：平台的 `alphas` 计数是否按塔去重累加。**在验证前两种算法都只是假设**，故 §1/§3 只给分塔读数。
4. **"`mult` 未定义，sentiment 更划算还成立吗？"** — **不成立**（v1 该句已删）。本版只陈述"三座塔都差 2 颗，`mult` 读数 1.8 vs 1.6"，并明写 `mult` 语义未定义、不解读为收益乘数。
5. **"institutions 四波的 sub 到底多少？"** — 见 §2.2：16 条第二腿件 sub ∈ [−0.12, +0.21]，最大值 0.21（w2 臂9 `VkNXvRpb`）；w1 的 5 条另带 UNITS 警告。**没有一条 ≥1.0**。
6. **"MODEL 是唯一搭档只核 1/6，另外 5 条什么时候核？"** — 本报告未核、不排期。"唯一搭档"这个说法**已作废**（§1）：6 条里 5 条 sub≥1.0，但只有 `Vk6eodeb` 核过塔归属。若其余 5 条不是 MODEL，则"MODEL 作第二腿"这条建议**不成立**、应作废。
7. **"生产档没跑是排期还是有意？探针档结论能外推吗？"** — 本报告**无法判断**是排期还是设计（四波配置一致为 decay0/nanON，我只有读数，没有决策记录）。**不能外推**：DEU skill 明写"设置是强度闸，跨档结果不可比"（`insiders.md:65`），故探针档 0 增量**不能**推出生产档 0 增量，反之亦然。
8. **"下一棒先补 D2/D6 还是换 sentiment/news 面？各自配额与预期增量？"** — 本报告**不能给配额数字**（未核实各动作的配额消耗）。能给的只有事实：补 D2 至少需 3 条（一个字段族 1 条）；补 D6 至少需 1 波（同几何换 decay4/nanOFF）；换 sentiment 面需先做 S0/S1（新数据集）。**预期增量**：insiders 补 D2/D6 是在"已测上限 1.30 之下"补证据，**最可能的结果是把 `provisional` 变成 `capped` 或 `dead_proposed`，而不是变出候选**；sentiment 面未知（未测）。
9. **"w4 和 w2 都 0.89，先推哪条进 prod？"** — 按 **2Y** 应先推 w2 臂6 `QP02ANn5`（2Y **1.11**，四波第二）；按 **F / margin / 结构简单度** 应先推 w4 臂1 `LLKnekRL`（F 0.67、margin 62.63bp、单层 `ts_ir` 无分组）；按 **sub** 应先推 w4 臂10 `MP6bwkGM`（0.68，但需先拆长侧解释）。**三条 S 距闸都 ≥0.69**，所以"先推哪条"取决于你想补哪个闸，而**没有一个闸现在能补齐**。
10. **"CW 排除后 w2 的 PARTIAL 还成立吗？"** — **成立**。重算见 §2.1：w2 仍有 `d5aE63Ew` 的 F 距闸 0.37 ≤ 0.4 ⇒ ≥1 近闸 ⇒ PARTIAL。w4 同理（`LLKnekRL` F 0.33）。近闸判据已统一到平台 limit（§0）。
11. **"同目录的 fundamental 报告与本报告什么关系？`fundamental 已点亮` 是谁的结论？"** — 两条**独立战役线**：那份是 fundamental 线（5 波 50 臂，DB id 2206–2210），本报告是 insiders 线（4 波 40 臂，DB id 2228/2230/2238/2239）。本报告只从那份借用三样东西：术语（§0 的 L1/L2/L3）、命名法、以及 1h 缓存陷阱的实证。**塔位数字一律以本次 ask 快照为准**；本报告**不复制**它关于 fundamental 的结论，也不为它背书。
12. **"要不要先跑 prod/self 与十年分年，把那 6 条走完五道闸？需要新配额吗？"** — 本报告不执行、不排期。工具路径：prod/self 走 `check_self_correlation` / `check_correlation`；十年分年走 `get_alpha_yearly_stats`（只读）。**配额影响本报告未核实**（相关性检查是否占用仿真槽、是否命中 48h 缓存，需按 `docs/experience/01_platform_gates.md` 与 `wq-prod-corr-read` 的口径确认），故不做承诺。

## §9 修订对照（审读意见 → 本版处理）

| # | 审读意见 | 本版处理 |
|---:|---|---|
| 1 | margin `0.007` 量纲读不懂 | §0 给出单位（小数，5bp=0.0005）、40 臂实读区间 [−0.001489, +0.006263]、全距 0.007752，并说明"0.4 = 全距 51 倍"故该闸不判近闸 |
| 2 | §0 剔除 CW 但 §2 用 CW 计近闸，w2 近闸要不要重算 | §0 统一判据；§2.1 重算 0/1/0/1（w2 2→1、w4 2→1），并逐波验算 verdict 不变 |
| 3 | `effective=1/2` 未定义 | §0 定义：归属塔数量（属性计数），与 `multiplier` 无算术关系 |
| 4 | 近闸基准两套（平台 limit vs 本地 review 线）说不清 | §0 明确：近闸只用 S/F/2Y 三闸；CW/margin/sub 只登记；本地 review 线不参与 |
| 5 | "距 CW 0.069" 方向不明 | §2.1 写明：**已超限 0.0687**（value 0.168741 vs limit 0.10），不是"还差" |
| 6 | "L2 提交前置" 与 skill 的 L2 层冲突 | §0 定义 L1/L2/L3 为本报告三层闸命名，并声明与 skill `layer` 字段不是同一套 |
| 7 | `vec_count` 未定义 | §0 定义 + FIELD 档 §4.2 出处；§3 写明要补的是"`vec_count==1` 分支 / 等样本数"对照 |
| 8 | `+0.21/+0.18/+0.28/+0.12` 基线不明、正负号不明 | §6.3 改为"同基线三波（低带−高带）+ w4 单列（掩码−裸核）"，并标注 w4 无高带臂 ⇒ 删掉"四波一致" |
| 9 | D2 的 6 个字段族未列全 | §5.2 列出 6 个信号字段全名 + 2 个非信号字段 |
| 10 | 直连仿真不写 expressions 与 40 臂可回读矛盾 | §5.1-4 解释：每波显式 `upsert_backtest_rows`（回执 n=10）才写 `expressions`；盲区指未 upsert 的那类 |
| 11 | "零平台调用" 与 80 次 GET 并存 | 抬头声明口径：本报告写作/修订步骤零调用；80+6 次 GET 是前序步骤已发生的 |
| 12 | "总票池 200" 口径 | §5.3 改为"LC 55 + SC 145 = 200 是该臂持仓只数，不是宇宙容量（TOP500 约 500 只）" |
| 13 | `XgaGb3J1`/`d5a2aO7v` 说"仅转录"却无转录内容 | §5.3 改为"本报告无其表达式/读数 ⇒ 不转录、不引用、不作依据" |
| 14 | D1 给 17–20 区间而非计数 | §5.2 改为 **17 条逐条枚举** |
| 15 | "没有任何塔只差 1 颗" 建立在可能过期的缓存上 | §1 表头前置缓存免责；结论改为"按本快照"；并在 §8-2 说明复核入口与"若变 1 需重排" |
| 16 | "已点亮（本日早前 fundamental 线所点）" 无据、且与"不写已点亮"冲突 | 删除归因；全篇只照录 `lit` 布尔值，不写"已点亮" |
| 17 | "2026-09-13 产品" 无出处 | §1 补 DB `wave_results` id 748/749/750 与 `source_file` 日期 |
| 18 | 6 条存量件的族归属/UNSUBMITTED 怎么取得 | §1 加"来源与取得方式"：指标与 status 来自 `batch_get_alpha_metrics`；塔归属只 `Vk6eodeb` 核过，其余为记录推断 |
| 19 | "MODEL 是唯一保住 sub 的搭档" 与表里 5 条 sub≥1.0 冲突 | §1/§7 作废该说法：6 条里 5 条 sub≥1.0，但只有 1 条核过塔归属 |
| 20 | "institutions sub ≤0.21" 无出处 | §2.2 给逐波区间表与最大值臂 |
| 21 | "天花板 0.89 / 外部上限 1.30" 自相矛盾 | §6.1 改为"外部上限 1.30、本 run 最好 0.89、未触及" |
| 22 | "合计需 4 颗" 与 16 条双塔件冲突 | §1 末改为"未裁定，不给合计颗数" |
| 23 | "成本是 1.5 倍" 两个分母 | 删除该倍数，改为"各差 2 颗 / 0/3 塔差 3 颗"的分塔口径 |
| 24 | "单集已封顶 / 边际产出趋零" 过度断言 | §6.1 改写，并说明"边际产出为零"需要同几何重复证据、本 run 不具备 |
| 25 | 乘法杠杆的 F/2Y 区间无逐波证据 | §6.2 改为三行逐波给数（S/F/2Y） |
| 26 | D3/D4/D5 无证据指针 | §5.2 逐维补臂号与表达式 |
| 27 | "族级判死先验 1.13/1.14/1.21" 无出处 | §5.2 补 `deu-insiders-evidence.md:47-54`，并注明是姊妹集/`vec_avg` 几何、不能替代本集实测 |
| 28 | 用 `mult` 差 0.2 论证投入产出比 | §1 删除该论证；§7 只列读数并声明语义未定义 |
| 29 | "w4 全项最高" 与自己的表冲突 | §2.3 改为逐项列明（S 并列、2Y 属 w1） |
| 30 | "零平台调用" 与 80 次 GET | 同 #11 |
| 31 | "w1–w5 fundamental 线作为对照"却未使用 | §4-5 删除该表述，明写"未使用 fundamental 线读数做对照" |
| 32 | "MODEL 作配对腿" 与禁止两腿相加冲突 | §7-3 说明边界：`insiders.md:55` 禁 `add` 型并列，明确允许条件/分组/残差型第二腿 |
| 33 | 只评 w4 两条近闸、不评 w2 的 `d5aE63Ew` | §2.1/§3 把三条并列比较 |
| 34 | `LLKnekRL` 结构描述无出处、`atom` 未定义 | §0 定义 atom；§3 补 `list_expressions` id 109942 与 `pyramids` 读数 |
| 35 | "institutions 机制一套未测" 无据 | §1 补依据：40 条表达式全文 + DB `list_expressions` 40 条，institutions 字段只出现在第二腿 |
| 36 | "16 座塔" 口径/来源 | §1 写明"ask JSON 共 16 条、逐条照录、本报告无法判断是否还有未列出的塔" |

## §附表 · 对 §7「本 run 无 forum_recon」的更正（2026-11-16 审阅时追加）

§7 末尾那句「**本 run 无 `forum_recon`**」是**误记**（本报告作者未拿到证据阶段输出）。台账实查：

- `DEU/forum_recon_8d59ef391b`：`found=true`、`status=ok`、`n_useful=5`、`searched_at=2026-11-16T16:54:44`。
  **但 `queries_tried` 只有 1 条**（`"insiders1 alpha template"`）、`rounds=1` ⇒ **三维检索词矩阵只落了「数据集名」这一维，机制措辞维与算子×字段维未执行**。
  命中的 5 帖中仅 2 条是模板且均为价格族泛化模板（`小而稳 A×ts_std_dev(A,30)` 26 赞、`Delta 反转 −ts_delta(A,3)` 21 赞），其余 3 条为方法论帖（Gemini CLI 工作流 104 赞等），**无一条讲内部人机制**。
- `DEU/forum_paper_recon_829b5bb3ae`：**9 篇**，每篇带 `direction` + `scope`（明确标注美国/英国/新兴市场样本 ⇒ 不可外推 DEU），`queries_tried` 9 条覆盖三维。
  直接落模板的三条：Lakonishok-Lee 2001 → M2（变化 > 水平）、Cohen-Malloy-Pomorski 2012 → M6（routine/opportunistic）、Seyhun/Jeng-Metrick-Zeckhauser → M4（单笔规模）。
- 检索通道如实登记：WebSearch 三次 60s 超时、Semantic Scholar 429、本地 `docs/experience` 无内部人文献库 ⇒ 改用 Crossref REST + 论坛 MCP。

**未做**（本轮确属缺口，勿当作已完成）：① 论坛按「机制措辞 / 算子×字段」补检；② 作者线反查；③ 臂表未逐条标注证据来源（post_id / DOI），故「哪些臂由哪条证据驱动」不可追溯。
