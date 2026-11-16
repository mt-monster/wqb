# S0 塔位与数据集盘点 — DEU / TOP500 / D1（2026-11-15）

> 任务：DEU × TOP500 × D1 的塔位盘点（S0）——塔位实读、目标塔选定、数据集分母实取、逐集排除、配对塔评估、机制假设、判读基准、证据通道与盲区。
> 性质：**只读盘点**。本档零平台写、零仿真、零 DB 写；全部读数来自本会话 MCP 实读或本地档案逐行引用。
> 判据纪律：AGENTS.md §7.5（判死标记不得单独作依据 / 收割优先于重挖）+ §7.6（六维穷尽闸，缺维只能 PROVISIONAL）+ §8.11 ⑤（数据集级 coverage=0 不是数据存在性判据）+ §8.11 ⑦（「未测」清单必须标注证据通道与其盲区）。

## §0 证据通道总表（本档每条结论的来源）

| 通道 | 本会话具体调用 | 覆盖什么 | 对什么盲视 |
|---|---|---|---|
| 平台塔位 | `mcp__wq-brain-http__get_pyramid_alphas()`（无参=当季） | 当季 ACTIVE alpha 的 category×region×delay 计数 | 不含上一季；不区分 ATOM/REGULAR；不区分是哪个 alpha |
| 平台数据集表 | `mcp__wq-brain-http__get_datasets(category, region, delay, universe)` | **(region,universe,delay,category) 口径下平台登记的数据集全集 = 唯一合法分母** | 不给字段级可用性；`coverage` 与 `description` 均不可作判据（见 §8.3） |
| 平台 alpha 详情 | `get_alpha_details` / `get_alpha_yearly_stats` / `get_alpha_by_id` | 单条 alpha 的 checks / pyramids / 年度分年 / metrics | 只覆盖我点名的 6 条（mLaALJX2 / 1YWe0NPX / d5a2aO7v / RREALzx0 / E56AzejK / A1VqRZRd），不是全池扫描 |
| 本地台账 | `mcp__wqb-db__get_mining_yield(DEU, by_dataset, strict)` / `get_dead_datasets` / `get_dead_ends` / `get_field_catalog` / `search_alphas_by_sharpe`；只读 sqlite（`logs/_tmp_s0_deu_*.py`，`mode=ro`） | 历史臂数、判死档、字段目录、在册 alpha 池 | **不含 MCP 直连仿真**（AGENTS §8.11 ⑦ 实例二）；`alphas.dataset_id` 在 DEU 全为 1902（区域级占位）⇒ 不能用它做集归属 |
| 本地档案 | `tracking/DEU/atom_orthogonal/*` 与 `tracking/DEU/reference/*`（逐条 path:line 见正文） | 六维举证、逐集处置、波次归因 | 档案是他人槽位产物，可能滞后于平台（本档仅作线索，关键读数已用平台重核） |

---

## §1 塔位实读（平台，2026-11-15，当季 = 2026Q4）

调用：`mcp__wq-brain-http__get_pyramid_alphas()`（无参 → 平台按**当前自然季度**返回，每季首日清零）。

DEU 只有 **D1** 有计数（D0 全 0，与本战役 delay=1 无关）：

| category | alphas | need | mult | lit |
|---|---:|---:|---:|:--:|
| fundamental | **2** | **1** | 1.8 | ✗ |
| sentiment | 1 | 2 | 1.8 | ✗ |
| insiders | 1 | 2 | 1.6 | ✗ |
| institutions | 1 | 2 | 1.6 | ✗ |
| analyst | 6 | 0 | 1.8 | ✓ |
| model | 3 | 0 | 1.8 | ✓ |
| other | 3 | 0 | 1.8 | ✓ |
| shortinterest | 5 | 0 | 1.3 | ✓ |
| news / option / pv / earnings / macro / risk / socialmedia / imbalance | 0 | 3 | 1.5–1.8（imbalance 1.2） | ✗ |

- 读数与任务给定的表**逐项一致**（本会话独立重读，非转抄）；合计 D1 计数 22。
- 平台同一份读数还给出其它区域，本档不使用。

## §2 目标塔选定：**fundamental**（差 1 颗，×1.8）

排序依据 = need 升序 → 倍率 → 可挖面宽窄：

1. **fundamental（need 1, ×1.8）— 选中**。全 DEU 唯一「一次合规提交即点亮」的塔，且倍率并列最高。它是**唯一不必先补第二颗**的塔。
2. sentiment（need 2, ×1.8）— 倍率同高，但**数据跨度死**：`DEU-SENTIMENT-TOWER-DATASPAN-DEAD`（dead_at 2026-11-01）实测 sentiment7/27 首笔 2019-03、sentiment33 首笔 2018，2014–2018 五年零持仓 ⇒ 十年数据硬约束下不可用。本会话未复测（该档证据为年度分年实证），故只作**不选**依据，不作新判死。
3. insiders / institutions（need 2, ×1.6）— 差 2 颗，且两塔都以「族级封盘」为主（见 §6），单塔单独推进性价比低；它们的最佳角色是**配对腿**。
4. 其余 8 塔 need 3（×1.2–1.8）— 一轮只能推进 1/3 步，优先级最后。

**结论：targetTower = fundamental，targetNeed = 1。**

---

## §3 数据集分母（唯一合法口径 = 平台 `/data-sets` 按 region×universe×delay 实取）

实取命令（本会话执行，原样记录）：

```
mcp__wq-brain-http__get_datasets(category="fundamental", region="DEU", delay=1, universe="TOP500")
→ count = 12
```

| # | dataset id | fieldCount | 平台 coverage | alphaCount | userCount | 备注 |
|---|---|---:|---:|---:|---:|---|
| 1 | alpha_factor_lib | 65 | 0.0 | 4 | 4 | |
| 2 | digital_ad_spend | 9 | 0.0 | 5 | 5 | |
| 3 | fundamental1 | 123 | 0.0 | 88 | 61 | |
| 4 | fundamental17 | 135 | 0.0 | 1862 | 651 | 唯一带 `fundamental17_dead` 判死键 |
| 5 | fundamental22 | 1 | 0.69 | 46 | 10 | |
| 6 | fundamental45 | 12 | 0.269 | 92 | 67 | |
| 7 | fundamental6 | 196 | 0.4923 | 1114 | 470 | |
| 8 | **fundamental72** | **1031** | **0.0** | 306 | 159 | **本档主集** |
| 9 | fundamental86 | 7 | 0.0 | 188 | 98 | |
| 10 | fundamental89 | 407 | 0.0 | 450 | 209 | |
| 11 | fundamental90 | 66 | 0.0 | 176 | 115 | |
| 12 | fundamental93 | 46 | 0.0 | 44 | 26 | |

### §3.1 ⚠ 分母表本身就是本档最重要的一条读数

**12 集里 9 集平台 `coverage = 0.0`**（含主集 fundamental72）。若按「cov=0 ⇒ 剔除」执行，这一步会**在评估任何语义闸之前**把 fnd72 一起砍掉——而 fnd72 实测有 1031 个字段，且其近期最优件 `mLaALJX2` 平台实读 `longCount 209 / shortCount 173`（§4.3）。这正是 AGENTS §8.11 ⑤ 记的 GBR `techindi_model` 反例同型：**数据集级 coverage 是不可逆硬拦截，不是数据存在性判据**。可用性只认字段级实返回（`get_field_catalog` 1031 行）或一条探针/实回的 longCount/shortCount。

### §3.2 本地 `datasets` 表不能当分母（本会话实测补充）

`data/wqb.db` 的 `datasets` 表里 `fundamental*` 有 23+ 行（`fundamental2/3/4/7/13/14/21/23/25/28/31/35/44/65/67/69/91/94/110`…），远超平台 DEU/TOP500/D1 的 12 集，且**不分 universe/delay、含历史伪行**；同一 `name` 还有多 id 重复（如 `fundamental72` = id 32/181/373）。⇒ 分母只认 §3 的平台实取。

---

## §4 逐集排除面（12 集 = 10 排除 + 1 保留 + 1 主集）

> 纪律：每行给**依据**，判死标记只作参考；「已收敛」≠「信号死」，是「该集在当前几何下的边际产出已为 0」。

### §4.1 已收敛 / 数据层排除（10 集，不入选）

| 数据集 | 类型 | 排除依据（实读/档案原文） |
|---|---|---|
| fundamental1 | A 已收割 | 已提交 ACTIVE `pwaQ0bx3`（平台 ACTIVE，date_submitted 2026-11-14；DB：S 1.60/F 1.40/2Y 2.01/TO 2.58%/prod 0.6821）⇒ 该集已贡献塔位，网格收敛封顶（`CATEGORY_MATRIX_FUNDAMENTAL_20261115.md:27`、waveBE242:441-461）。台账 `get_mining_yield`：2 expr / 0 bt。 |
| fundamental6 | A 已收敛 | ATOM 天花板 1.15，单点 1.73 已被 `Wje5K71x` 占用（后者平台 ACTIVE，prod 0.4305）；台账 88 expr / 26 bt / **0 passed**。`CATEGORY_MATRIX_FUNDAMENTAL_20261115.md:28`。 |
| fundamental17 | A 已收敛（浅探） | 台账 10 bt / **0 passed** + 拥挤（平台 alphaCount 1862 / userCount 651，本会话实读）；`fundamental17_dead` 键存在但**不作单独依据**（§7.5），真正依据是 0 passed + 拥挤。`:29` |
| fundamental22 | C 单字段集（**修订，见 §11.8.2**） | 字段目录实读（`get_field_catalog(DEU, fundamental22)`）：**只有 1 个字段 `fnd22_value`**（描述=「ESG KPI 数值」，cov 0.69–0.76），**不是 RIC↔BBID 映射表**——原「伪集：映射表冒充」的表述是照抄错配的平台 description，本档撤回该理由。现行排除依据＝**单字段集结构性不可扩**（1 字段无法做跨字段构造/分母）+ 台账 12 expr / 11 bt / **prod_clean 0** + 本地 3 条 ra_clean 归属存疑；「信号死」未被本会话证据支持。`:30` |
| fundamental45 | A 已收敛 | QA（电话会 NLP）78 臂收敛 S≤1.04；基线 S 0.96 / 2Y 1.73 / sub 0.72 是**量级参照不是承诺**（waveBE242:6/:35；s2_nearmiss_rescue_20260904:4940）。`:31` |
| fundamental89 | A 终判死（六维） | 三波 24 臂 + 历史 20 臂，S 天花板 ~1.0 / 2Y ≤1.02；死档 `DEU-FND89-NONCURRENT-ACCRUAL-CEILING`（id 1576，四轴穷尽）；**不外推为 fnd72 先验**（waveBE242:251 明文）。台账 24 expr / 20 bt / 0 passed。`:34` |
| fundamental90 | A 已收敛 | 42 臂 S 平台 0.84–0.88，字段/合成/中性化/骨架四轴全实测；2Y 过闸塔位 ×4 已入册。台账 4 expr / 0 bt。`:35` |
| fundamental93 | A 已收敛 | 12 臂水平 ≤0.53 + 论坛 no_result；死档 `DEU-FND93-ACCRUAL-TAX-DEAD`。台账 8 bt / 0 passed。`:36` |
| alpha_factor_lib | C 数据层排除 | BE251 臂 DD 71%/199%/83%、margin −0.5~−5.7%（超窄账户签名）。`:37` |
| digital_ad_spend | C 数据层排除 | 探针 lc 25 / sc 25（约 50/500），CW 0.5 vs limit 0.1 挂；**数据层排除 ≠ 信号死**。`:38` |

### §4.2 保留（不入选、不排除）：fundamental86

`CATEGORY_MATRIX_FUNDAMENTAL_20261114.md:33`（本会话实读）把它记为 **active（本类别唯一活体）**：11-14 首波 10 臂 bestSharpe 0.91、near×2（`N1PkQxEw` S 0.91 CW 0.109；`1YW6xk3W` S 0.76 F 0.83）。台账 20 bt / 0 passed。
⇒ 它是**储备集**，不是主集：距 S 闸 0.67，且 fnd86 的 `fnd86_insider_trading_score` 已记字段级数据层排除。本档**不并槽**（他槽在途 + 距闸远）。

### §4.3 主集 fundamental72：选定理由 + 六维闸距离

**平台实读（本会话 `get_alpha_details("mLaALJX2")`，2026-11-15）**——这是全 fundamental 塔最接近点亮的一条：

| 项 | 读数 |
|---|---|
| type / stage / status | **REGULAR** / IS / UNSUBMITTED |
| settings | DEU / TOP500 / **D1** / decay 0 / **FAST** / trunc 0.08 / nan ON / 2014-01-01→2023-12-31 |
| S / F / 2Y / sub | **1.50** / **1.04** / **2.30** / **1.12** |
| TO / returns / DD / margin | 16.31% / 7.79% / 6.44% / **0.000955（= 9.55 bp）** |
| LC / SC | 209 / 173 |
| checks.fail | **仅 `LOW_SHARPE`：value 1.5 vs limit 1.58** |
| checks.pass | LOW_FITNESS / LOW_TURNOVER / HIGH_TURNOVER / **CONCENTRATED_WEIGHT** / **LOW_SUB_UNIVERSE_SHARPE** / CLUSTER_TEST / **LOW_2Y_SHARPE** / MATCHES_PYRAMID |
| checks.pending | SELF_CORRELATION / DATA_DIVERSITY / PROD_CORRELATION / REGULAR_SUBMISSION |
| pyramids | effective **1**：`DEU/D1/FUNDAMENTAL` ×1.8 |
| prod / self | 0.5444（check_correlation，2026-11-15）/ 未测 |

**同族备选（DB 实读，全部 UNSUBMITTED）**：`88NrmOVa` S 1.50 / F 1.04 / 2Y 2.04 / TO 15.90%（prod 未测）；`ZYaqO7dY` S 1.49 / 2Y 2.34；`vRA9K5Zw` S 1.44 / 2Y 2.83（2Y 最深备胎）。fnd72 族在册 **181 条**（163 UNSUBMITTED + 18 COMPLETE），`max S = 1.50`、`max 2Y = 2.83`，**无一条已提交** ⇒ 与 OS 池的同族 self-corr 风险为 0。

**年度分年（`get_alpha_yearly_stats("mLaALJX2")`，本会话实读）**：2014 **1.40** / 2015 2.03 / 2016 1.09 / 2017 1.58 / 2018 0.80 / 2019 0.80 / **2020 −0.35** / 2021 3.03 / 2022 2.60 / 2023 1.96；十年每年 LC 163–259 / **SC 139–220**（2015 为最低值 139，**修订**：初版误写 SC 141–220 / 「均 >140」），无零持仓年（十年数据面达标）；唯一的负年是 2020（pnl −200,587）。

**判死档距离（六维，AGENTS §7.6）**——结论：**PROVISIONAL，不得终判死**：

| 维 | 合格线 | fnd72 现状 | 判定 |
|---|---|---|---|
| D1 互异模板 | ≥10 | wave107 十模板（死档 id 1574）+ 11-15 近闸网格 51 臂（`NEARGATE_BREAK_GRID_FND72_20261115.md`） | ✓ |
| D2 字段族自测 | 每族 ≥1 | CF/BS 明细已实测（cov<2%）；**IS 季度标量族**已出货（q_ebit / q_is_oper_inc）；**IS 年度标量族 / CF q 族 / BS q_1·q_2 全族零本地实测** | ✗ |
| D3 矩全家 | 水平/一阶差/二阶/比值各≥1 | 一阶差 ✓（ts_delta 240/176）、比值 ✓（÷tot_asset）、水平 ✓（wave107）、二阶/分位 ✓（ts_rank / ts_corr） | ✓（11-15 网格补齐） |
| D4 分组轴 | ≥2 | sector / industry / subindustry 三轴已用 | ✓ |
| D5 非线性 | ≥1 | ts_rank ✓、tail ✓、hump ✓、bucket ✓（11-15 网格）；signed_power / trade_when 未测 | ✓ |
| D6 配置 | ≥2 | **FAST（S 1.50）vs SUBINDUSTRY（三波 25 臂 best 0.68）= 2 套中性化**；宇宙恒 TOP500、delay 恒 1、decay 0/2/4 已扫 | ✓ |

⇒ 六维中仅 **D2 未达**（字段族覆盖不全）⇒ 按 §7.6 只能 PROVISIONAL。**但 D2 的补法恰好与「赢得 0.08 S」的机制无关**：本档不靠「再扫字段」取胜，见 §5。

**结论：primaryDataset = fundamental72。**

---

## §5 机制假设（驱动臂表设计）

### §5.1 缺口定位（可量化，不是猜）

- 平台只拦一条闸：`LOW_SHARPE 1.50 < 1.58`，**差 0.08**。其余 7 条 RA 硬闸（F / 2Y / sub / TO / CW / CLUSTER / MATCHES_PYRAMID）**全 PASS**。
- 该族 **S 面的参数自由度已被 51 臂扫空**：decay（0/2/4 单调负）、分组轴（sector 峰）、winsorize std（3 峰）、tail 带宽（0.12–0.15 峰）、双窗位（240/176 峰）、三腿窗（1008 峰）、极值等价族（4 算子全弱）、zscore/SNR/5Y 锚（全灭）——**全部双向回落证峰**（`NEARGATE_BREAK_GRID_FND72_20261115.md:52`），说明剩余缺口不是「参数没调到」，而是**单族信息量天花板**。
- 同族 2Y 裸锚形态（a_ebit 1.51 / a_is_oper_inc 1.53，S 面 0.07–0.11 死）证明：**2Y 是 DEU 的免费轴，S 才是难轴**（同 ATOM 文档 `ATOM_OFFICIAL_DEFINITION_AND_GATE5_REVISION_20261112.md:29` 的机理结论）。
- 该族最弱年份 = **2018 (0.80) / 2019 (0.80) / 2020 (−0.35)**：缺口集中在「盈利改善动量在低增长/疫情冲击年份的系统性失效」，**不是全期均匀差 0.08**。

### §5.2 机制假设（一句话）

> **fnd72 的「季度营业利润/总资产 三窗 delta 秩乘」动量在单族内已到 S 1.50 天花板；把 insiders1 的「内部人持仓净变化」作为**信息确认腿**横向叠进主腿（小权重/正交/门控），用跨族条件化提高**个券层面**的信号精度——注意这是**横截面加权，不是按年份剔除**（初版把两者混写，已更正，见 §11.5）；时间维度另设一条独立的 regime 门控臂（D 形）。目标：在保留 2Y 2.30 与低换手的前提下把 S 推过 1.58，并让多数据集件的梯窗证据（§11.1）成立。**

### §5.3 结构骨架（不是权重网格，先验定方向）

按「不改主腿、只加一层可解释约束」的顺序派发，每条都在 SF 指纹上可判生死：

- **A 确认腿（软权重，首选）**：`multiply(主腿, add(0.5, rank(insd1 确认信号)))` —— 全截面保留（不动 LC/SC、不动 CW），只按确认强度倾斜权重。预期：S +0.05~0.15、TO 微升、sub 不降。
- **B 正交腿**：`vector_neut(主腿秩, insd1 确认信号)` —— 若两腿正相关（年度符号预警见 §6.4），去掉共同分量可能把「纯基本面残差」提纯；代价是可能丢失 2021–2023 的强段。
- **C 硬门控**：`trade_when(insd1 确认 > 0, 主腿, 0)` —— 精度最高但会砍宽度（LC/SC 209/173 起，砍到 <130 可能触 CW）；**只在 A/B 都不够时试，且必须先看 LC/SC**。
- **D 时间条件化（新增，回应「A/B/C 无时间维度」）**：`trade_when(<慢变 regime 变量> 处于有利态, 主腿, 0)` —— 唯一能直接作用在 2018–2020 段的形态。**约束**：门控形会带来 CW=0.5 的结构性指纹（`_effective-levers.md:102-121` 杠杆 G，跨波跨形 7/7），一旦 CW 挂即按 §11.1 的 0.1 线判死本臂；且必须先确认门控期 TO 不越 0.70。
- **反模式（禁）**：`add(主腿, insd1腿)` 的等权相加（混信号 + 权重自由度）；换回 SUBINDUSTRY（该族在这套配置下已三波证死 0.68）；重试 decay 4（族内单调负杠杆）。

### §5.4 验收与止损指纹

| 读数 | 判读 |
|---|---|
| S ≥ 1.58 且其余闸仍 PASS | 成立 → 进 S5 五道闸 |
| **梯窗（多数据集件必查）**：该颗 `checks` 里 `IS_LADDER_SHARPE` 报 pass，且 `two_year_sharpe` / `two_year_ladder_window` 与 `is_ladder_sharpe` 三处读数一致 | 缺此项即视为未验收（见 §11.1） |
| **时间集中度**：2018/2019/2020 三年逐年 Sharpe 若仍全 <1.0、而总 S 靠 2021–2023 撑起 | 记「时间集中度风险」，不得按可提交推进（即使总 S 过线） |
| S 落在 1.50–1.57 | 确认腿只贡献噪声 ⇒ 换腿型（A→B→C）或换伙伴集 |
| S 反而降 ≥0.10，或 sub 跌破 1.0（平台线 0.56，见 §6.5） | 确认腿**破坏**主腿 ⇒ 立即弃门控路线，回落纯 fnd72 + 换自由度（universe/delay，D6 处方） |
| CW 由 PASS 变 fail | **数据层指纹**（宽度塌缩），不是符号问题 ⇒ 不加门控宽度，改软权重 |
| 翻转后 \|S\| 同量级 | 衰减对称 = 机制在、符号错 ⇒ 翻符号保留（本族方向先验已定：盈利改善→做多） |

---

## §6 配对塔评估（主塔 + 另一座未点亮塔）

### §6.1 法规核对（任务给定第 7 条 + 平台点塔规则，逐条对本方案）

| 约束 | 本方案（FUNDAMENTAL + INSIDERS） | 结论 |
|---|---|---|
| ① trio 内部禁两两（PV/MODEL/OTHER，含同类两腿） | 两个类别都不在 trio | 不受限 |
| ② trio 某类 + 非 trio 类，本战役 ≤5 条 | 不涉及 | 不占额度 |
| ③ **≥3 塔同现一律记 0** | 必须严格 2 类：只用 fnd72 字段 + insd1 字段 + 标准分组（sector/industry/subindustry/market，ATOM 文档 :14 明示 group 字段豁免） | **硬约束，见 §6.3** |
| ④ 塔归属以平台 `pyramids[].name` 为准 | 已找到本区**实测先例**（§6.2） | 合规且可验证 |

### §6.2 双塔机制的**平台实测先例**（这条不是推断，是本会话读到的）

`get_alpha_details("d5a2aO7v")`（DEU，ACTIVE，2026-11-12 提交）：

```
code: subtract(group_rank(ts_rank(ts_backfill(vec_avg(insd1_holdings),110),252),sector),
               group_rank(ts_delta(vec_avg(shrt3_bar),220),sector))
pyramids.effective = 2
  DEU/D1/SHORTINTEREST ×1.3
  DEU/D1/INSIDERS     ×1.6
checks: fail = []  (LOW_SHARPE / LOW_FITNESS / LOW_SUB_UNIVERSE_SHARPE / IS_LADDER_SHARPE / CW 全 PASS)
self 0.5451 / prod 0.5451 / S 1.66 / F 1.36 / 2Y 2.58 / sub 0.92 / TO 9.47% / margin 0.001786
```

⇒ **两数据集合成 = 两塔计数**在 DEU 已被平台实证；同一条 alpha 还证明 `LOW_SUB_UNIVERSE_SHARPE` 的平台上限是 **0.56**（不是 1.0），`LOW_2Y_SHARPE` 是 1.58。这条先例同时说明：**配对路线在本区是走过、过过闸的**，不是纸面推演。

### §6.3 伙伴集选定：insiders1（insiders 塔，1/3 → 2/3）

平台实取：`get_datasets(category="insiders", DEU, delay=1, universe="TOP500")` → **2 集**：`insider_agg_matrix`（34 字段，cov 0.5617）、`insiders1`（8 字段，cov 0.5343）。

| 判据 | insiders1 的读数 | 出处 |
|---|---|---|
| 数据面（十年） | `get_alpha_yearly_stats("1YWe0NPX")`：**2014–2023 年年在册**（LC 35→180 / SC 74→219） | 本会话平台实读 |
| 塔归属（实测） | `get_alpha_details("1YWe0NPX")` → `pyramids = [DEU/D1/INSIDERS ×1.6]`（**单集 insiders 字段 = INSIDERS 塔**） | 本会话平台实读 |
| 单集上限 | S 1.19–1.30（BE172/174/176 三波 30 臂三条路径收敛，`BE176_INSIDERS1_CEILING_130_20261112.md:1,:32`；覆盖率 53.4% 见 :39） | 本地档案 |
| 伙伴角色可用性 | 它的任务**不是自己过 1.58**，是提供低相关确认信息；单集上限 1.30 不构成障碍 | 本档推理 |
| 换手/保证金 | TO **8.86%**、margin **0.002074（20.74 bp）** ⇒ 叠进主腿会**降 TO、抬 margin**（主腿 margin 9.55bp 本就达标） | 平台实读 |
| 拥挤度 | 字段目录 `get_field_catalog(DEU, insiders1)`：8 字段全 cov 0.5343，`insd1_holdings/tradesignificance/valueeur/shares/gvkey` 的 `userCount=1 / alphaCount=1` ⇒ **几乎无人用过** | 本会话 DB 实读 |
| 判死档 | `get_dead_datasets(DEU)` 19 集**不含 insiders1**；对 insiders1 的封禁只到「单集 ATOM 不可行」（`BE176:50`）。⚠ **但塔级有一条在册禁令**（初版漏引，见 §11.3）：`DEU-INSIDER-AGGMATRIX-DEAD`（id 1523，2026-10-30）rule 原文「**insiders 塔在 DEU D1 判定不可点亮。要做 insider 族改去 EUR/TOP2500**」——该塔级结论已被 2026-11-12 提交的 `d5a2aO7v`（平台 ACTIVE、pyramids=DEU/D1/INSIDERS×1.6）实证推翻 | 本会话 DB 实读 + 平台实读 |

**排除的替代伙伴（逐条给理由）**：

- **institutions1**（institutions 塔）——看似最强（`E56AzejK` S 1.71/F 1.36/2Y 2.79/sub 1.17），但三处硬伤：① `get_alpha_yearly_stats("E56AzejK")` 实测 **2014–2017 四年零持仓**（首笔 2018）⇒ 十年数据面不达标；② self-corr 0.9184 vs ACTIVE `2rmGAPqN`（死档 `DEU-INST1-OTH455-CLUSTER-DUP-DEAD`）；③ 该族两个封盘档（`DEU-INSTITUTIONS1-PROBE-DEAD-20260923`、上述 cluster-dup）。另 `institutions6` / `fund_holdings_panel` 各有死档（`DEU-INSTITUTIONS6-DEAD`、`DEU-INSTITUTIONS-fundholdings-SINGLEATOM-WEAK`）。
- **insider_agg_matrix**（同属 insiders 塔，34 字段、cov 0.5617）——**技术上是更好的分散腿**：`get_alpha_yearly_stats("A1VqRZRd")` 十年全在册，且与主腿年度符号**仅 5/10 同向**（2020 主腿 −0.35 vs 它 +0.93；2017 +1.58 vs −0.68），是理想的对冲型确认腿。**但** `DEU-INSIDER-AGGMATRIX-DEAD`（2026-10-30，22 模板 max S 0.92）明文「DEU 不再派发 insider_agg_matrix 任何模板」——本档**不擅越**。⇒ 列为 **fallback #1**，如要动用须由用户明确解禁该条 blanket ban（并说明仅作 ≤20% 权重的正交腿、不重跑那 22 个模板）。
- **news18**（news 塔 0/3，70 字段 cov 0.979，`DEATH_AUDIT_20261110.md:15` 记「从未探针、最大富矿」）—— 机制上「新闻情绪确认基本面」成立，但：news 塔差 3 颗（一轮只推进 1/3）、news18 十年跨度未测、`DEU-NEWS18-ALLDEAD` 档在册。⇒ 列为**下一轮候选**，不作本轮伙伴。
- **pv / model / other** —— trio 类别，与 fundamental 组合虽合规（②），但本区 PV 已多族终判死（pv106/intraday_pv_feats/pattern_scores/pv109），MODEL/OTHER 均已点亮（配对无塔位收益）。不选。

### §6.4 ⚠ 伙伴腿的风险登记（如实，不粉饰）

- **年度符号同向 9/10**：主腿 vs `1YWe0NPX` 的年度 Sharpe 符号只在 2017 相反 ⇒ **日频收益大概率正相关**，「分散化抬 S」的算术前提不成立。因此 §5.3 把**首选定为「确认/门控」而不是「等权相加」**：门控靠的是**个券层面的信息增量**，不靠收益流不相关。
- **配置轴不一致**：主腿必须 FAST（SUBINDUSTRY 已三波证死），而 `1YWe0NPX`/`d5a2aO7v` 都是 SUBINDUSTRY ⇒ insiders1 腿在 FAST 下**未测**，属本波新增自由度（D6 意义上合法）。
- **塔归属只由平台判定**：若 insiders1 的字段被用于 group 算子而非信号代数，是否仍计入 INSIDERS 塔**未知**（标准 group 如 sector 豁免，但数据集型 group 字段未见 DEU 实证）。⇒ 设计上**必须把 insd1 字段放进信号代数**（rank/multiply/vector_neut），不许只当分组轴；提交前仍以 `pyramids[].name` 逐条复核。

### §6.5 配对结论

**partnerTower = insiders，partnerDataset = insiders1。**
预期塔位增量：**fundamental 2/3 → 3/3（点亮，×1.8）；insiders 1/3 → 2/3（×1.6）**——一次合规提交同时推进两座未亮塔，且不触碰 trio 禁混与 ≥3 塔归零规则。

---

## §7 判读基准（读之前先把线写死）

**来源**：`tracking/DEU/config/thresholds.json:3-9,:20-21`（DEU 区域闸）+ 本会话平台 checks 实读（`LOW_SUB_UNIVERSE_SHARPE` limit 0.56、`LOW_2Y_SHARPE` limit 1.58 均由 `1YWe0NPX` / `mLaALJX2` 的 checks 直接读出）。

| 轴 | 线 | 本波参照（mLaALJX2 平台实读） |
|---|---|---|
| S（IS Sharpe） | **≥ 1.58**（平台 `LOW_SHARPE` limit 实测 1.58，不是 config 旧表里的 1.25） | 1.50（**差 0.08**） |
| F（Fitness） | ≥ 1.0 | 1.04 ✓ |
| 2Y Sharpe | **单集件**：LOW_2Y_SHARPE ≥1.58；**多数据集件**改走 **IS_LADDER_SHARPE**（闸种切换见 §11.1，保守预筛按「所有梯窗最差 ≥1.58」，以该颗 checks 实判为准） | 2.30 ✓（mLaALJX2 为单集件，走 LOW_2Y） |
| sub-universe | 本地 ≥1.0 / 平台 limit 0.56 | 1.12 ✓ |
| TO | 0.01 – 0.70 | 16.31% ✓ |
| margin | ≥ 5 bp（thresholds `margin_min = 0.0005`） | **0.000955 = 9.55 bp ✓**（⚠ 见 §9.1 更正） |
| CW（concentrated weight） | **平台 limit = 0.1**（实读 `zqdQqNG1`：value 0.5 / limit 0.1 / date 2014-03-06；`3q0gZE0N`：value 0.25 / limit 0.1）——`thresholds.json:20` 的 0.5 只是**本地 review 线**，按 0.5 验收会把 0.1–0.5 的宽度塌缩件放过去 | PASS ✓（mLaALJX2 平台 pass） |
| prod / self corr | 均 ≤ 0.70 | prod 0.5444 ✓ / self 未测 |
| 十年数据面 | 2014–2023 每年 LC>0 且 SC>0（AGENTS §7.5 第 3 条，人工核，无代码闸） | 每年 LC 163–259 / SC 141–220 ✓（2020 pnl 为负，登记为「唯一负年」，不作数据面失败） |

**符号指纹（本族专用，写死避免事后编故事）**

- **衰减对称**（翻转后 |S| 同量级）= 机制在、符号错 ⇒ 翻符号保留；**单向**（翻转即死）= 事件型信号。本族方向先验已定：**盈利改善 → 做多**（三 delta 同向乘积已证正向，RREALzx0/KPJmRpGN）。
- **CW 挂 = 数据层指纹**（宽度 ≤5 必挂，死档 id 1573），不是符号问题 ⇒ 不改符号重试，改宽度/几何。
- **decay 对本族是单调负杠杆**（0/2/4 → 1.40/1.28/1.33，`NEARGATE_BREAK_GRID_FND72_20261115.md:19`）⇒ 任何「加 decay 提 S」的臂直接不派。
- **门控推 2Y 的假设已族级证伪 5/5**（w2）；**gBF 修 CW 已证伪 2/2**（w3）⇒ 这两条老路不再派。
- 若加腿后 **S 不升反降 ≥0.10** 或 **sub <1.0**，记「确认腿破坏主腿」，不回炉调权重。

---

## §8 证据通道与盲区（「未测」清单必须带出处）

### §8.1 本档的「未测 / 没挖过」清单及其通道

| 结论 | 由哪条通道得出 | 该通道对什么盲视 |
|---|---|---|
| fnd72 的 IS 年度标量族 / CF q 族 / BS q_1·q_2 全族「零本地实测」 | `get_mining_yield(DEU, by_dataset=True, strict=True)`（backtest_results 台账）+ `get_field_catalog`（平台缓存） | **不含 MCP 直连仿真**：本会话跑的 `get_alpha_details` 是平台直读，不写 expressions/backtest_results；同理他人跑的直连仿真在这里完全隐形。⇒ 「台账里没有」≠「没人跑过」 |
| insiders1 在 FAST 配置下「未测」 | `get_alpha_details("1YWe0NPX")`（SUBINDUSTRY）与 DB 池（`insd1` 族 895 条，最高 S 2.63） | 该池里 887 条 UNSUBMITTED + 7 条 COMPLETE，**全部 `platform_status = UNSUBMITTED` 且 prod/self 多为 null**；我只能看到检索到的行 |
| news18「从未探针」 | `DEATH_AUDIT_20261110.md:15` 的自述 + news 塔当季 0 | 档案自指；本会话**未**对 news18 做任何平台读 |
| sentiment 十年跨度不足 | 死档 `DEU-SENTIMENT-TOWER-DATASPAN-DEAD` payload（引 yearly-stats 实证） | **本会话未复测**（未跑 sentiment 的 yearly stats）；只作「不选」依据，不作新判死 |

### §8.2 已知的工具/口径盲区

1. **DEU 的 `query_dataset_profile` / `query_field_profile` 全 0 行**（前档 `S0_DATASET_SCAN_FUNDAMENTAL_FND72_20261114.md:11` 实测；本会话未复跑）⇒ 逐集状态不走 profile 表。
2. **`alphas.dataset_id` 在 DEU 全为 `1902`**（本会话 `logs/_tmp_s0_deu_active.py` 实测：按 status/platform_status 过滤出的 **23 条** ACTIVE/SUBMITTED 行，`COUNT(DISTINCT dataset_id) = 1`，值恒 1902）⇒ 该列是区域级占位，**不能做集归属**；集归属只能靠表达式里的字段前缀 + 平台 pyramids。
3. **本地 `datasets` 表不能当分母**（§3.2）。
4. **平台 `description` 不可信**：本会话 `get_datasets` 实读发现 `fundamental22 / fundamental72 / fundamental86 / fundamental89 / fundamental90 / fundamental93` 六个集的 description 全部写着「RIC↔Bloomberg ID mapping」这类模板文案，而 fnd72 实际是 1031 个财务字段（`get_field_catalog` 实读）⇒ **描述既不能用来判伪集，也不能用来选集**。

### §8.3 本档未做的事（如实）

- 未跑任何**仿真/探针**（S0 只读）；fnd72 的 D2 字段族补齐、insiders1 在 FAST 下的表现，都留给 S1/S3。
- 未跑 `check_correlation` / `check_self_correlation`（prod 0.5444 是 DB 里 2026-11-15 的既有回执，不是本会话新测）。
- 未复测 sentiment / news18 的年度跨度（见 §8.1）。

---

## §9 对既有档案的两条更正（本档实读发现）

### §9.1 `NEARGATE_BREAK_GRID_FND72_20261115.md:46` 的 margin 单位误读

该档把 `mLaALJX2` 的 margin 记作「**0.96bp**」。平台原值 `margin = 0.000955`，而全仓单位换算是 `margin_bp = margin × 10000`（`Claude/skills/wq-brain-campaign-toolkit/scripts/metrics_cache.py:117`、`tools/verdict/candidate_health_card.py:141`）。同表 `RREALzx0` 的 `0.000898` 在该档被记作「8.98bp」——**同一档内两种换算法并用**。正确读数：**mLaALJX2 margin = 9.55 bp**，对 `margin_min = 0.0005`（5bp）是 **PASS 不是 fail**。
影响：该档「四道 RA 闸破三、唯一残余 LOW_SHARPE」的结论**不变**（margin 本就不是 RA check），但若按 0.96bp 读，会误判成「margin 也不达标」，从而多设计一条本不必要的提 margin 臂。

### §9.2 任务描述的「12 集里 11 集已排除」实为 **10 集**

`CATEGORY_MATRIX_FUNDAMENTAL_20261114.md:33` 与 `CATEGORY_MATRIX_FUNDAMENTAL_20261115.md:33`（本会话实读）都把 **fundamental86 记为 `active`（本类别唯一活体）**，不是 capped/dead/data_excluded。
⇒ 12 集 = **10 集排除**（§4.1）+ **1 集 active 储备**（fundamental86，§4.2）+ **1 集 provisional 主集**（fundamental72）。
这不改变主集选择（fnd86 bestSharpe 0.91，距闸 0.67，远于 fnd72 的 0.08），但改变「本类别已封盘」的表述强度——**fnd86 不是死集，是下一轮储备**。

---

## §10 交接（S1/S2 直接消费）

1. **主集** fundamental72；**入口资产** = `mLaALJX2`（S 1.50 / 唯一 fail = LOW_SHARPE 1.58）。
2. **唯一待补自由度** = 跨族确认腿；**伙伴集** insiders1（`insd1_holdings` / `insd1_tradesignificance` / `insd1_valueeur` / `insd1_shares`，cov 0.5343）。
3. **配置**：DEU / TOP500 / D1 / **FAST** / trunc 0.08 / nan ON / decay 0（decay>0 对本族是负杠杆）。
4. **禁派清单**（继承死档，臂表必须遵守）：CF 明细与 BS 明细字段（id 1573）；`ts_target_tvr_decay`（id 1575，慢变量+宽度<100）；bf 窗口 22（id 1577，基线 66/240/176/1008）；任何 ≥3 类别的混搭（社区融合类 at 0）；trio 内部两两（平台规则）。
5. **fallback #1**：`insider_agg_matrix`（对冲性更好，10 年全在册）——需用户解禁 `DEU-INSIDER-AGGMATRIX-DEAD` 的「不再派发任何模板」。
6. **不选但值得单开**：fundamental86（active 储备，S 0.91）；news18（news 塔 0/3，70 字段 cov 0.979，从未探针）；risk60（BA2 重开队列）。

---

## §11 复核修订（2026-11-15 第二版：独立复核 8 条 + 缺失证据 6 条的处置）

> 本节是**审计追溯**，不是新口径：§1–§10 的正文已就地改掉被复核判定为错的读数（逐处标「修订」），本节记录每条复核意见的采信 / 部分采信 / 不采信与对应证据。
> 本会话新增的平台实读：`get_pyramid_alphas` ×2（Q3 / Q4 显式区间）、`get_alpha_details` ×5（`zqdQqNG1` / `2r5MO67Z` / `XgaGb3J1` / `3q0gZE0N` / `pwaQ0bx3`）、`get_field_catalog(DEU, fundamental22)`；本地只读 sqlite 四支（`logs/_tmp_s0_rev1_prodclean.py` / `_rev2_pool.py` / `_rev3_fields.py` / `_rev4_fundpv.py`）。

### §11.0 处置总表

| # | 复核条目 | 处置 | 本档动作 |
|---|---|---|---|
| 1 | 双数据集件走 IS_LADDER_SHARPE，只写 2Y≥1.58 不够 | **采信**（「最差窗」措辞部分采信，见 §11.9） | §11.1 + §5.4 新增梯窗验收行 |
| 2 | CW 验收线 0.5 与平台不符（平台 0.1） | **全采信** | §11.1 + §7 表格改 0.1 |
| 3 | fnd72 在册 dead_end 未按 §7.6④ 撤判 | **全采信** | §11.2 同档追加降级记录 |
| 4 | insiders 塔级禁令被选择性引用 | **全采信** | §11.3 补全引 + 平台事实反驳 |
| 5 | 同字段 OS 件相关风险未量化 | **采信为前置闸**（候选不存在时无法跑相关） | §11.4 |
| 6 | 机制假设与臂形态不对齐（无时间维度） | **全采信** | §11.5 + §5.2 改写 + §5.3 新增 D 形 |
| 7 | 当季计数会过期，未登记时间炸弹 | **全采信** | §11.6 + `docs/time_bombs.json` TB-05 |
| 8 | 「无更省路径」未证明 | **全采信** | §11.7（实跑 57 行扫描，结论反而更强） |

### §11.1 闸种与验收线修订（复核 #1 / #2）

**(a) 单集 vs 多数据集是两套闸，互斥出现**

- 代码依据：`src/wqb/workflow/nodes/submit_alpha.py:952-966` 注释原文——`LOW_2Y_SHARPE ⇒ 单数据集（ATOM）：不走 IS Ladder，只查 Last-2Y`；`IS_LADDER_SHARPE ⇒ 多数据集：走 Ladder`，并注明「实测 DEU 侧 7Y 1.751 / FAIL 线 1.59，以该颗 IS_LADDER_SHARPE 的实判为准」。
- DB 列证据（本会话只读）：`is_ladder_sharpe` **仅多数据集件有值**——`d5a2aO7v`（insd1 × shrt3）**2.58**、`58gGQmlN`（inst1 × oth455）**2.58**；单数据集件全 null——`mLaALJX2` / `1YWe0NPX` / `3q0gZE0N`。
- 平台 checks 证据：`mLaALJX2` 的 `checks.pass` 含 **LOW_2Y_SHARPE**、不含 IS_LADDER_SHARPE；`d5a2aO7v` / `XgaGb3J1` / `2r5MO67Z` 的 `checks.pass` 含 **IS_LADDER_SHARPE**、不含 LOW_2Y_SHARPE ⇒ 闸种随「单 / 多数据集」切换，**本会话实测**。
- DEU 实判线：`tracking/DEU/s2_nearmiss_rescue_20261104.md:3448-3460` 实录 `{"name":"IS_LADDER_SHARPE","value":1.18,"limit":1.58,"year":2}`，并写明「任何 2Y < 1.58 的候选，即便总 S 过线也不可提交」。

**(b) 本档采用的线（保守）**：多数据集件的 2Y 项升级为

> **IS_LADDER_SHARPE：按「所有梯窗最差值 ≥1.58」保守预筛；派发前必须先跑 1 条代表臂，读回 `two_year_sharpe` + `two_year_ladder_window` + `checks`（含 IS_LADDER_SHARPE 的 value / limit / year），以该颗实判为准。**

⚠ 方向性歧义（不写成事实）：「最差窗」与 `submit_alpha.py:957-960` 注释的「2Y 不足可逐级退到 7Y 2.06 / 10Y 1.59」是**相反的宽松方向**。两者并存 ⇒ 本档只用它做**预筛**，不据此断定「4Y/6Y 必然 <1.58」。

**(c) CW 线 = 平台 0.1，两处实读**

- `zqdQqNG1`：`CONCENTRATED_WEIGHT value 0.5 / limit 0.1 / date 2014-03-06`
- `3q0gZE0N`：`CONCENTRATED_WEIGHT value 0.25 / limit 0.1`

`tracking/DEU/config/thresholds.json:20` 的 `concentrated_weight_max: 0.5` 是**本地 review 线**，不是平台线。⇒ 本波所有门控 / 宽度收缩形态一律按 **0.1** 预筛。另：门控形 CW 恒 0.5 是**结构指纹**（`Claude/skills/wq-brain-ra-deu/references/_effective-levers.md:102-121` 杠杆 G，跨波跨形 7/7）。

### §11.2 撤判 / 降级记录：`DEU-FND72-NARROW-BREADTH`（id 1574，按 AGENTS §7.6④ 在本档追加）

- **原规则（在册原文）**：「DEU 侧不再开 fundamental72 波次。同数据集在其他区域过 prod 不构成跨区可迁移先验——必须先核对三项：宇宙规模、字段级覆盖率、字段族完整性。零挖掘不等于机会。」
- **原前提（本次被证伪的那一条）**：payload.reason 末段——「另有 DEU 侧缺整个利润表（IS）字段族（fnd72_pit_or_is_a_* 全部 not found，**fnd72_s_ 标量路线也封闭**）」。
- **反证（平台实读，本会话）**：`get_alpha_details("mLaALJX2")` 的完整表达式使用 `fnd72_s_pit_or_is_q_is_oper_inc` 与 `fnd72_s_pit_or_bs_q_1_bs_tot_asset`，平台读数 S **1.50** / F **1.04** / 2Y **2.30** / LC 209 / SC 173 / `pyramids=[DEU/D1/FUNDAMENTAL]`；同族 `RREALzx0`（1.42）与 `KPJmRpGN`（1.38，2Y 1.58）使用 `fnd72_s_pit_or_is_q_ebit` / `fnd72_s_pit_or_is_q_is_oper_inc`。⇒ **「fnd72_s_ 标量路线封闭」为假**，该 dead_end 的前提不成立。
- **降级处置**：`DEU-FND72-NARROW-BREADTH` 由「终判死」降为 **PROVISIONAL**（六维 D2 未达，见 §4.3 表）。**其数据层子结论保留并继续生效**：`DEU-FND72-CF-DETAIL-SPARSE`（id 1573）——CF 明细 / BS 明细在 DEU/TOP500 覆盖 <2%、宽度 2–5 时 CW 必挂。
- **未做（如实）**：**没有写 waiver**（本档无用户授权原话；`tools/waiver.py` 要求 `approved_by` + `reason_code` + 有效期），因此这只是「PROVISIONAL 降级登记」，**规则层仍可能拦下**。若下一槽被在册规则拦住，处置路径两条：(i) 由用户出具 USER_INSTRUCTION 型 waiver；(ii) 在 registry 里把 id 1574 显式改档（本档不改他人档案正文）。

### §11.3 insiders 塔级禁令 vs 平台事实（复核 #4）

- **被漏引的原文**：`get_dead_ends(DEU)` → `DEU-INSIDER-AGGMATRIX-DEAD`（id 1523，dead_at **2026-10-30**）payload.rule 全文含：「DEU 不再派发 insider_agg_matrix 任何模板；**insiders 塔在 DEU D1 判定不可点亮。要做 insider 族改去 EUR/TOP2500**，且必须用 SLOW 中性化 + 分母窗 84 + 分子窗 1260。」
- **平台事实（本会话 `get_alpha_details("d5a2aO7v")`）**：`DEU_R_shrtinsd_02`，**2026-11-12 提交、status ACTIVE**，`ra.failed_ra_count = 0`，`self 0.5451 / prod 0.5451`，`pyramids.effective = 2` = `[DEU/D1/SHORTINTEREST ×1.3, DEU/D1/INSIDERS ×1.6]`。
- **判读**：id 1523 写于 10-30，而 11-12 仍有一颗粒子成功进入 INSIDERS 塔 ⇒ **「insiders 塔在 DEU D1 不可点亮」这条塔级结论已被平台事实推翻**；该档**数据集级**部分（insider_agg_matrix 22 模板 max S 0.92、跨区失效约 1.3 个 Sharpe）仍然有效，本档继续遵守它对 `insider_agg_matrix` 的封禁——这正是伙伴集选 `insiders1` 而不选 `insider_agg_matrix` 的原因。
- 台账口径：id 1523 的**塔级**断言降为 **PROVISIONAL-REFUTED**，**数据集级维持**。

### §11.4 与 ACTIVE 件 `d5a2aO7v` 的同源相关风险（复核 #5）

- 事实：`d5a2aO7v` 的主腿就是 `vec_avg(insd1_holdings)`（`group_rank(ts_rank(ts_backfill(vec_avg(insd1_holdings),110),252),sector)`），平台 `selfCorrelation = 0.5451`、`prodCorrelation = 0.5451`。计划中的确认腿同样用 `insd1_holdings` ⇒ **同字段同源**。
- **本会话无法量化**：`check_self_correlation` / `check_correlation` 均以 alpha id 为入参，候选尚不存在 ⇒ 只能登记为**派发前硬门**，不编数字。
- 派发前硬门（写进臂表前置）：

  1. 第 1 条臂出结果后立刻跑 `check_self_correlation`（对本区 OS 池）与 `check_correlation(production, refresh=True)`，**两者都必须 ≤0.70**；
  2. **成本预算**：做一次「去腿对照」——同一骨架去掉 insd1 腿后若 |ΔS| < 0.15，说明增益主要来自 insd1 而非基本面 ⇒ 即便过闸也大概率与 `d5a2aO7v` 高相关，**改腿**（`insd1_tradesignificance` / `insd1_valueeur` / `insd1_shares`）或退回单塔；
  3. 若 self > 0.70 且换腿无效 ⇒ **放弃配对**，退回纯 fnd72 单塔路线（此时只保留 LOW_2Y 闸，2Y 2.30 有余量）。

### §11.5 机制与臂形态对齐（复核 #6）

- **逐年对照（两条都是平台实读）**：
  - `mLaALJX2`（主腿）：2018 **0.80** / 2019 **0.80** / 2020 **−0.35**
  - `1YWe0NPX`（伙伴腿）：2018 2.76 / 2019 2.16 / 2020 **−0.19**

  ⇒ 伙伴腿在 2020 **也是负的**，单靠它救不了 2020；「剔掉 2018–2020」在横截面加权形态里**不可验证**。
- **更正**：§5.2 已改写为「横截面加权（个券降权），不是按年份剔除」；§5.3 新增 **D 形（时间条件化 regime 门控）** 作为唯一直接作用于时间段的形态，并标明门控形的 CW 结构性指纹。
- **验收（§5.4 新增两行）**：① 多数据集件必须带回 IS_LADDER_SHARPE 的三处一致读数；② 若 2018/2019/2020 三年仍全 <1.0 而总 S 靠 2021–2023 撑起，记「时间集中度风险」，**不得按可提交推进**。

### §11.6 Q4 时间炸弹（复核 #7，已实读并登记）

- **实读（本会话）**：
  - `get_pyramid_alphas(start_date=2026-07-01, end_date=2026-09-30)` → DEU D1 **fundamental = 0**
  - `get_pyramid_alphas(start_date=2026-10-01, end_date=2026-11-15)` → DEU D1 **fundamental = 2**

  ⇒ 计数按自然季清零**已被同区两季读数实测证实**。
- **炸弹**：**2026-12-31 之后**当季重置 → `targetNeed 1→3`，「一次提交即点亮」的前提消失，目标塔须重估（届时 sentiment / insiders / institutions 的 need 也同步重算）。
- **登记**：`docs/time_bombs.json` **TB-05**（date `2026-12-31`，manual，owner=user，status=pending；证据文件指向本档 §11.6）。
- **行动线**：要么 `2026-12-31` 前完成提交；要么到期后按 need=3 重估。

### §11.7 「无更省路径」穷尽扫描（复核 #8，本会话实跑）

**(a) fundamental 面**

- 口径：`region_id=10` 且 `prod_correlation < 0.70` 且 `platform_status ∉ {ACTIVE, SUBMITTED}` 且 `status ∈ {IS, UNSUBMITTED, COMPLETE}` → **57 行**（`logs/_tmp_s0_rev1_prodclean.py` / `_rev3_fields.py`）。
- 归属方法：用本地 `fields` 表（`field_name → dataset_id → datasets.name`）逐 token 反查表达式。⚠ **已知偏差**：`sector` 是 pv1 的 group 字段，会被误标成 PV 塔——已用平台 pyramids 校准（`mLaALJX2` 表达式含 `sector`，平台 pyramids 只有 FUNDAMENTAL ⇒ **group 字段不产生塔**）。
- 含 fundamental 字段的 17 行里，S≥1.3 的 4 条：

| alpha | 数据集 | S | F | 2Y | sub | TO | margin | prod | 平台判定 |
|---|---|---:|---:|---:|---:|---:|---:|---:|---|
| **3q0gZE0N** | fundamental1 | **1.56** | 1.46 | 2.01 | 1.28 | 2.92% | 74.97bp | 0.6276 | **2 条不达标**：LOW_SHARPE(warning 1.56/1.58) + **CONCENTRATED_WEIGHT 0.25/0.1** |
| mLaALJX2 | fundamental72 | 1.50 | 1.04 | 2.30 | 1.12 | 16.31% | 9.55bp | 0.5444 | 1 条不达标：LOW_SHARPE |
| gJa7A1k0 | fundamental1 | 1.46 | 1.10 | 1.72 | 1.27 | 2.86% | 50.07bp | 0.6560 | — |
| wpoXmKGv | fundamental1 | 1.35 | 0.97 | 1.61 | 1.27 | 2.74% | 46.87bp | 0.6805 | — |

- **关键反证（为什么 3q0gZE0N 不是更省路径）**：`get_alpha_details("pwaQ0bx3")` 的表达式是
  `tail(winsorize(group_zscore(group_backfill(ts_backfill(vec_avg(fnd1_board_characteristics_filtered_timerole),250),sector,250),sector),std=4),lower=-0.95,upper=0.95,newval=0)`
  —— 即 **3q0gZE0N 加一层 `group_backfill` + std 2→4 + 带宽 ±1→±0.95**；该件 **2026-11-14 已提交、status ACTIVE**，`failed_ra_count = 0`、S 1.60 / F 1.40 / 2Y 2.01 / sub 1.25 / CW PASS / LC 107 / SC 111 / self 0.1904 / **prod 0.6821**（距 0.70 只剩 0.018）。
  ⇒ fundamental1 的「更近件」实际是**已收割 ACTIVE 件的种子**：再挖＝复现 ACTIVE 件（self-corr 风险）+ prod 余量几乎用尽。
- 其余 fundamental 行：MP3ENd38 1.33 / e7QYZN9l 1.26 / 1YZ8AOXM 1.24（fnd6 同族）；gJaqYgQl 0.11 / LLKO3vZ9 0.07（fnd72 的 2Y 裸锚，S 面死）。
- **结论**：fundamental 面无「零仿真直达」路径；S ≥1.5 的 prod-clean 件只有 `mLaALJX2`（唯一单闸）与已被收割的 fnd1 族。**主集维持 fundamental72。**

**(b) insiders 侧：零仿真腿与「≥3 塔 = 0」的平台实证**

| alpha | 平台 pyramids（effective） | RA | S / F / 2Y / sub / TO / margin | 用途判读 |
|---|---|---|---|---|
| `XgaGb3J1` | **2**：[INSIDERS ×1.6, MODEL ×1.8] | fail=[]（含 IS_LADDER pass） | 2.36 / 2.02 / 2.71 / 1.51 / 17.38% / 14.66bp | **零仿真可把 insiders 1→2**（MODEL 已亮 ⇒ 无新塔收益）；prod / self 未测 |
| `2r5MO67Z` | **0**：[PV ×1.6, INSIDERS ×1.6, MODEL ×1.8] | fail=[]（含 IS_LADDER pass） | 2.63 / 2.13 / 2.94 / 1.63 / 19.70% / 13.15bp | **平台首次实证「≥3 塔 ⇒ 计数 0」**（此前只是规则条文）；S 再高也白搭 |
| `d5a2aO7v` | 2：[SHORTINTEREST, INSIDERS] | fail=[] | 1.66 / 1.36 / 2.58 / 0.92 / 9.47% / 17.86bp | 已 ACTIVE（insiders 现有的那 1 颗） |

- 该池 `insd1` 族共 **895 条**（887 UNSUBMITTED + 7 COMPLETE + 1 platform-ACTIVE），高位件多为 `significant_value_*`（属 **insider_agg_matrix**）+ `predicted_surprise_*`（属 **predictive_starmine**）+ `cap` / `market`（属 **pv1**）的三塔混搭 ⇒ 对点塔**零价值**。字段归属由本地 `fields` 表实查，与平台 pyramids 逐条吻合。
- **对选型的正面影响**：若先用 `XgaGb3J1`（零仿真、RA 全过）把 insiders 推到 2/3，再提交「fundamental + insiders」合成件，则**一次提交可同时点亮 fundamental 2→3 与 insiders 2→3 两座塔**。

### §11.8 读数更正（就地改 + 说明）

1. **mLaALJX2 2015 shortCount = 139**（不是 141）⇒ 全年区间 LC 163–259 / **SC 139–220**，初版「每年均 >140」撤回（§4.3 已改）。
2. **fundamental22 不是「RIC↔BBID 映射表」**：`get_field_catalog(DEU, fundamental22)` 实读只有 1 个字段 `fnd22_value`（描述「ESG KPI 数值」，cov 0.69–0.76）。⇒ 初版用错配的平台 description 当伪集理由，撤回；排除依据改为「单字段集不可扩 + prod_clean 0 + 归属存疑」（§4.1 已改）。
3. **NEARGATE:46 的 margin 0.96bp**：本档 §9.1 已更正为 9.55bp；**源头档同步追加更正段落**（`NEARGATE_BREAK_GRID_FND72_20261115.md` 末尾，不覆写他槽正文）。
4. **字段级 coverage 补充证据**：本地 `fields` 表里 fnd72 字段**非零**——`fnd72_s_pit_or_is_q_is_oper_inc` 多快照 cov 0.44–0.90、`fnd72_s_pit_or_is_a_ebit` 0.75–0.85、`fnd22_value` 0.31–0.76 ⇒ 进一步坐实「集级 cov=0 ≠ 无数据」。⚠ 该表**不带 universe / delay 列**，多快照来源不可区分，只能作存在性证据、不能作本配置的覆盖率。

### §11.9 未采信 / 部分采信（如实，不粉饰）

| 复核说法 | 处置与理由 |
|---|---|
| 「4Y/6Y/10Y 梯窗很可能 <1.58，S 破 1.58 也未必能提交」 | **部分采信**：闸种切换 + DEU 1.58 线已实证；但「所有回看窗取最差」与 `submit_alpha.py:957-960` 注释「2Y 不足可逐级退到 7Y 2.06 / 10Y 1.59」方向相反。本档按保守线预筛，**不把「必然 <1.58」写成结论** |
| 「CW 0.5 与平台不符」 | **全采信**，改 0.1（两处实读） |
| 「fnd72 dead_end 未撤判」 | **全采信**，§11.2 同档追加降级；**未写 waiver**（无用户授权原话），已注明规则层仍可能拦 |
| 「insiders 塔级禁令选择性引用」 | **全采信**，§11.3 补全引 + 平台事实反驳 |
| 「同字段 OS 件相关风险未量化」 | **采信为前置闸**：候选不存在 ⇒ 相关工具无可跑对象；给成本预算 + 硬门，不编数字 |
| 「机制与臂形态不对齐」 | **全采信**，改机制措辞 + 新增 D 形 + 两条验收 |
| 「Q4 时间炸弹」 | **全采信**，实测 Q3=0 / Q4=2 并登记 TB-05 |
| 「无更省路径未证明」 | **全采信**，跑 57 行扫描；翻出 3q0gZE0N 后经 `pwaQ0bx3` 比对确认其为 ACTIVE 件种子 ⇒ 结论更强 |
| 「缺 insd1 复合池成本对比」 | **全采信**，用平台 pyramids 逐条判定（XgaGb3J1 = 2 塔可收割 / 2r5MO67Z = 0 塔） |

### §11.10 修订后结论（**选型未变，理由加厚**）

| 项 | 值 | 依据 |
|---|---|---|
| targetTower / targetNeed | fundamental / **1**（**`2026-12-31` 前有效**） | §1 平台塔位 + §11.6 Q3/Q4 实读 |
| primaryDataset | **fundamental72** | §11.7(a)：fundamental 面 prod-clean 扫描无第二个 S≥1.5 的单闸件；fnd1 的更近件是 ACTIVE 件种子 |
| partnerTower / partnerDataset | **insiders / insiders1** | §11.3 塔级禁令已被平台推翻；§11.7(b) 证实高位 insd1 件多为 ≥3 塔混搭（计数 0） |
| towerGain | fundamental **2/3→3/3**；insiders **1/3→2/3**（合成件直接推进）或 **2/3→3/3**（先零仿真收割 XgaGb3J1 再合成 ⟹ 一次提交点亮两塔） | §11.7(b) |
| 判读基准 | 见 §7（已改：CW 0.1；多数据集件走 IS_LADDER 保守线） | §11.1 |
| 未解决的前置 | 对 `d5a2aO7v` 的 self / prod 相关闸（§11.4）；id 1574 / 1523 的规则层豁免（§11.2 / §11.3） | — |
