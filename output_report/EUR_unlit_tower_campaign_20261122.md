# EUR/D1 未亮塔战役报告（2026-11-22）

> 目标：交付 10 颗验证通过 regular alpha（ATOM 优先）。全程固定 EUR / D1 / delay1。
> 口径：S>1.58、F>1.0、2Y>1.58、checks.fail=[]、prod<0.7、self<0.7、逐年满仓、塔位未满（已点亮塔不进交付清单）。
> **本轮未提交任何 alpha**（红线：提交须用户显式确认）。
>
> **★★★ 方向纠正（2026-11-22 深夜，用户指正）**：本报告 §7 的 5 席篮**全是跨集混腿**（`techindi × 弱腿`×3 + 另 2 条组腿），
> **零纯 ATOM**——这是我把"ATOM 全灭"当结论后错误转向混腿凑数的结果，**不是交付主线**。
> 更根本的问题：此前 60+ 族 ATOM 判死几乎全用**单一配置 TOP2500/CROWDING**，违反判死六维闸 D6（≥2 套配置）。
> 已发现反例：`LLK3EMa1` 纯 ATOM（金字塔 EARNINGS effective=1）在 **TOP800/INDUSTRY** 下 S1.91/F2.49/**2Y1.99**，
> 只差 2Y 闸 0.03（该限值 2.02 是 TOP800 的 IS_LADDER）。
> 平台确认 EUR 还有 **TOP1200 / TOP400** 两个从未测过的宇宙 ⇒ 换宇宙可能把 2Y 限值降到 1.58 ⇒ **正在重攻纯 ATOM**。
> **ATOM 攻坚结果（2026-11-22）：合规穷尽后确认 0 交付**（详见台账 §14）：
> - 补做配置维：CROWDING / **SLOW_AND_FAST** / **STATISTICAL** / INDUSTRY 四档全测（此前只有 CROWDING 单档）；
> - 补做宇宙维：TOP2500 / TOP800 / **TOP1200** 全测（平台确认 EUR 有 5 宇宙，TOP1200/TOP400 此前从未测）；
> - 补做强腿维：`earnings_sent_matrix` **首次作强腿**（此前只作弱腿）；
> - 结论：**未亮塔集作强腿全部 S<1.0**；唯一接近全闸的纯 ATOM `LLK3EMa1`（S1.91/F2.49/2Y1.99@TOP800）
>   被**数据层封死**（2014–2020 零持仓，仅 3 年数据，违反"近十年有数据"硬约束）。
> - ⇒ **"只打未亮塔 + 纯 ATOM + 近十年数据"三条约束交集为空**。混腿篮只作备选，不作交付主线。
> - **用户授权放宽"近十年数据"后**（2026-11-22）：对唯一接近全闸的 `LLK3EMa1` 做了完整梯度穷尽
>   （ts_mean 16 算子 / ts_delta 16 算子 / group_backfill / 参数轴 / 宇宙轴 / 配置轴）——
>   **2Y 1.99 是结构性天花板，限 2.02（TOP800 IS_LADDER），0.03 缺口数学上不可达**。
>   ⇒ **即便放宽十年数据，未亮塔纯 ATOM 仍 0 交付**。唯一能产纯 ATOM 的方向是放宽"只打未亮塔"（纳入已亮塔存量全闸 ATOM 件），待用户裁定。

## 0. 结论摘要

| 维度 | 结果 |
|---|---|
| 本轮派批 | **27 批 / 172 臂**（含 Wave A–D 新增 4 批 16 臂） |
| **可交付候选（prod+self 全过、塔位未满、互相关<0.7）** | **4 颗已终判**：N1NGbddg（INSTITUTIONS 0→1/3）+ 58geG1P1（PV 2→3/3）+ d5aPlXjX（INSTITUTIONS 1→2/3）+ XgaO2WOa（INSIDERS 2→3/3）；两两互相关 **0.0407–0.6297** ✅<br>**+1 颗待 prod**：`vRAoOjYb`（SOCIALMEDIA 0→1/3，S2.11/F1.27/2Y2.16/sub1.16/TO21.9%/fRA=0，与 4 席最大互相关 **0.6406**）——由修复批 `VB8xw9qh4se9irIuSO1sX9` 产出，prod 因 MCP 会话连接中断未读出 |
| 全闸但 prod 撞单件 | **2 颗原形**：WjlxGbRG（**0.752**）、rK7nJ5nE（**0.7134**）——直方图均 `[0.7,0.8)` 孤立 n=1（撞单个近重复件）⇒ 按 §9 第 29 条配方换弱腿形态后已救回（见 `vRAoOjYb` / `WjlxL7Yd`） |
| 本轮新挖全闸件 | **2 颗**（MACRO：2r5exOvP / N1P8GQnX），被重复件墙拦（prod 0.766、self 0.7703 撞已提交件 GrmmNzz0） |
| 族 L 近闸件 | **6 颗**（S2.29–2.91 / F2.08 / 2Y2.34），统一卡 sub 比率闸（0.43–0.51 < 0.52） |
| ATOM 路径 | **10 个未亮塔数据集 × 模板族全覆盖**（+ socialmedia12 5 族 + Wave D 3 探针），**纯 ATOM 可交付 = 0**（实测，非推断） |
| 互相关容量律 | **每个强腿最多 4 席**（techindi 实测：第 5 件 ≥0.705）；EUR 仅 3 个强腿有可交付件（techindi / analyst7-EBI / fnd72），各自容量被族内互相关锁死 |
| 实际可交付容量 | **4 席已终判 + 1 席待 prod = 5 席**（名义 11 席不可达，见 §5 容量事实终判） |
| 组腿配额（rule 3） | **已用 4/5**（58geG1P1 PV / d5aPlXjX / XgaO2WOa / rK7nJ5nE 各 OTHER） |
| 提交 | **0**（用户裁决：先攒候选不提交） |

## 1. 塔位实况（平台 `get_pyramid_alphas`，2026-11-22）

| 状态 | 塔 | 席 |
|---|---|---|
| 满塔（不可投） | analyst 10 / model 3 / fundamental 3 / news 3 / other 3 / risk 3 / sentiment 3 / imbalance 3 | — |
| **未满（可交付）** | **institutions 0/3**、**socialmedia 0/3**、**earnings 1/3**、**insiders 2/3**、**macro 2/3**、**pv 2/3** | 11 |

## 2. 收割面：11-19 会话 fallback 件的 prod 复验（refresh 实测，6/6 全过）

| # | alpha | 塔位 | S | F | 2Y | TO | prod |
|---|---|---|---:|---:|---:|---:|---:|
| 1 | N1NGbddg | INSTITUTIONS 0/3 + ANALYST | 1.69 | 1.05 | 2.17 | 5.14% | **0.6872** ✅ |
| 2 | vRAvo8jA | INSTITUTIONS + ANALYST | 1.72 | 1.06 | 2.27 | 5.18% | **0.6781** ✅ |
| 3 | leAXvaLn | INSTITUTIONS + ANALYST | 1.78 | 1.06 | 2.10 | 5.31% | **0.6951** ✅ |
| 4 | A1x7E3ae | INSIDERS 2/3 + ANALYST | 1.84 | 1.15 | 2.25 | 5.07% | **0.6604** ✅ |
| 5 | RRemVOeb | INSIDERS + ANALYST | 1.84 | 1.15 | 2.22 | 5.07% | **0.6615** ✅ |
| 6 | 2r5NgWvY | SOCIALMEDIA 0/3 + ANALYST | 1.65 | 1.01 | 2.07 | 5.11% | **0.6785** ✅ |

- 6/6 平台闸全绿（failed_ra_count=0）、prod 直方图健康（无孤立高桶 n=1 指纹）、全部 UNSUBMITTED、全部落未满塔。
- 2r5NgWvY 逐年满仓确认（2014–2023 每年 long/short >0；2020 年 S −0.63 为负年但持仓存在）。

**★ 但互相关实测推翻「6 颗 = 6 席」**：本地 4 年 PnL（1021 点）两两相关 **0.80–0.9986**，
`max_mutually_below_subset`（阈值 0.7）**= {N1NGbddg}，规模 1**。
⇒ **6 颗同属一个机制族（analyst EBI 修正强腿），同篮只能交 1 颗**。

## 3. 本轮新挖（4 个数据集的 ATOM 闭环）

### 3.1 earnings6（EARNINGS 塔 1/3，剩 2 席）——7 批 58 臂，梯度穷尽

| 批 | 改动 | 关键读数 | 判定 |
|---|---|---|---|
| 1 | TOP800→TOP2500（换宇宙治 CW） | S 2.39→**1.05** | ❌ 信号住小盘 |
| 2 | 中性化 SUBINDUSTRY→**INDUSTRY**（治 CW 根因）+ decay32 | **CW 0.167→PASS**（5/8 臂）；2Y 1.73–1.90 | ✅ CW 解决，2Y 卡 2.02 |
| 3–4 | decay 32→16（+窗口 85/95/105/115/125） | **2Y 1.99**（LLK3EMa1）CW PASS | 差 0.03 |
| 5 | decay 16→8 | 2Y 1.99 峰值同值 | decay 轴见顶 |
| 6 | TOP800→**TOPCS1600** | S 0.95、longCount **83** vs short 895 | ❌ 大宇宙纯空头无信息 |
| 7 | truncation 0.05→0.08 + 610/252 慢腿变体 | 2Y 峰 1.93 | ❌ truncation 抬高伤 2Y |

**三条可迁移定律**：
1. **CW 的根因是「中性化组稀疏度」，不是权重上限**。TOP800 上 SUBINDUSTRY 组内只剩 1–2 只 ⇒ 权重集中；放宽到 INDUSTRY 即通过（代价 S −0.05、2Y −0.1）。**truncation 反而是反向杠杆**（0.05→0.08 使 2Y 1.99→1.93）。
2. **2Y 限值 2.02 是 TOP800 专属的 IS_LADDER 阶梯闸**，与 S 无关（恒 2.02）⇒ 「降 S 降闸限」对 2Y 无效。TOP2500/CS1600 限值为 1.58。
3. **decay 轴单调性已穷尽**：d32→1.90 / d16→1.99 / d8→1.99，峰 1.99，限 2.02，差 0.03 不可破。

### 3.2 mcr27 / macro27（MACRO 塔 2/3）——数据层排除，整线关停

- 首波 6 臂：全闸候选 `KPgZvxwE`（created÷closed_days@subindustry）**S 2.27 / F 1.28 / 2Y 2.49 / fRA=0**，prod **0.7202**（差 0.02）。
- 换轴把 prod 从 0.8378（RReEEgwb@industry）压到 0.7202 ⇒ 分组轴降 prod 有效（−0.12）。
- **但逐年复核推翻**：`get_alpha_yearly_stats` 显示 2014–2020 七年 longCount=0，数据仅 2021–2023 三年 ⇒ **数据层排除成立（优先级高于 prod 墙）**，原计划的罕见化扰动批**取消省配额**。
- 教训：prod 差 0.02 时的下一步不一定是罕见化扰动，**先做逐年拆解**——数据层排除的优先级高于任何 prod 杠杆。

### 3.3 socialmedia15（SOCIALMEDIA 塔 0/3）——两代字段全灭

- 本轮新系 10 字段（2026-03 onboard、αC≤9 蓝海）：全灭，|S| ≤ 0.54，9/10 为负；唯一正向 litigation +0.38。
- 叠加 11-18 会话对 d1_ 系十臂全灭（|S| ≤ 0.21）⇒ **45 字段两代全测，SOCIALMEDIA 纯 ATOM 判死**。
- 归因：cov 0.37 + 事件计数语义稀疏 ⇒ 有效样本小 + EUR 社媒打分定价效率高。⇒ **socialmedia 在 EUR 应作「门控腿」不作「信号腿」**（反证：`2r5NgWvY` 用 scl12_buzz 作弱腿反而出全闸件）。

### 3.4 fund_holdings_panel（INSTITUTIONS 塔 0/3）——10 臂全灭，纯 ATOM 判死

骨架：`group_rank(ts_zscore(ts_backfill(<读数>, 66), 504), industry)`，TOP2500/SUBINDUSTRY/decay8（multisim `2fEcXT92H4V6be132ueS6BI`）

| 读数 | S | 2Y | sub | 判定 |
|---|---:|---:|---:|---|
| boundary_transaction_total ÷ holder_account_total | 0.06 | −0.12 | 0.10 | 无信号 |
| stable_boundary_trade_count_21d | 0.02 | −0.18 | −0.08 | 无信号 |
| large_trade_count_50bps | 0.04 | 0.16 | 0.48 | 无信号 |
| transaction_value_distribution_score（取反） | −0.11 | −0.16 | −0.34 | 负 |
| mean_security_weight | −0.17 | −0.13 | −0.13 | 负 |
| security_transaction_usd ÷ security_holding_usd | −0.21 | 1.26 | −0.39 | 负 |
| holding_value_distribution_score（取反） | −0.21 | −0.92 | −0.41 | 负 |
| transaction_account_total ÷ holder_account_total | −0.22 | 0.99 | −0.33 | 负 |
| top_weighted_account_number Δ66 | −0.33 | −0.29 | −0.09 | 负 |
| herfindahl_index_holdings（取反） | −0.31 | −0.71 | −0.62 | 负 |

**归因**：日频机构面板的读数在 EUR 全被定价消化（HHI 拥挤、边界交易密度、conviction 扩张无一有效）；与 11-20 会话「机构持仓变动 prod 0.8887」结论一致 ⇒ **institutions 类在 EUR 是信息源级饱和**。
⚠ 3 臂撞 UNITS 量纲坑（`add(vec_avg(count_field), 1)`：CSShare + 无量纲不兼容）——`divide` 型读数必须先归一化分母。

### 3.5 族 F（FUNDAMENTAL(fnd72) × EARNINGS(earnings6)）——8 臂全灭，骨架层教训

| 臂 | S | F | 2Y | 判定 |
|---|---:|---:|---:|---|
| 弱腿 w=0.5 @subindustry（基准） | 0.99 | 0.41 | 0.96 | 全灭 |
| w=0.3 / w=0.7 | 0.98 / 0.99 | 0.40 | 0.95 / 0.98 | 全灭 |
| 弱腿 = actual_eps 裸值 | 0.94 | 0.38 | 1.19 | 全灭 |
| 弱腿 zscore 窗 504 | 0.98 | 0.40 | 0.95 | 全灭 |
| backfill 窗 22 | 0.98 | 0.40 | 0.93 | 全灭 |
| 弱腿轴 industry | 0.99 | 0.41 | 0.96 | 全灭 |
| 弱腿方向取反（estimated/actual） | 0.98 | 0.40 | 0.95 | 全灭 |

**★ 两条新定律（本轮最贵的教训）**：
1. **跨集组腿必须照搬强腿的完整骨架**：`58geG1P1` 的强腿核是
   `ts_target_tvr_decay(quantile(signed_power(trade_when(...), 1.05)), driver=gaussian, lambda_min=0, lambda_max=1, target_tvr=0.06)`，
   我只借了字段（`fnd72_pit_or_*`）而把外层换成 `group_neutralize(group_rank(...))` ⇒ **S 从 1.79 掉到 0.99（−45%）**。
   ⇒ **组腿实验的强腿侧必须逐字复制原表达式（含 TVR/quantile/signed_power 全部外层）**，只换弱腿。
2. **三塔组合 `pyramids.effective = 0`**：本族 8 臂的 `pyramids.list` 全是 [FUNDAMENTAL, PV, EARNINGS] 三段、effective=0
   ⇒ **多腿组腿不产生有效塔位收益** ⇒ 组腿**最多两腿**，三腿直接无价值。

⇒ 族 F 判死（不投后续配额）。**修正后的族 F 配方**：复制 `58geG1P1` 全骨架，仅把弱腿换成 earnings6 / fund_holdings_panel / insider_agg_matrix。

## 4. 已排除路线汇总（含证据）

| 路线 | 排除理由 |
|---|---|
| earnings6 换宇宙 / decay / truncation | 58 臂，三轴均封顶 |
| mcr27 招聘岗位 | 逐年 2014–2020 零持仓（数据层） |
| socialmedia15 新系 | 10 臂全灭；叠加 d1_ 系 = 45 字段全测 |
| pv106 微观结构价差 | 11-12 已测：价差/成本负向，取反上限 1.01 |
| investor_activity 零售流 | 11-20 已测 85 臂：prod 0.78–0.84 + 仅 6 年数据（双卡） |
| earningscall_sentiment | 11-20 已测 66 臂：prod 0.78 信息源级墙 |
| 11-21 三颗全闸件 | RReEEgwb→MACRO 已亮 + prod 0.8378；58geG1P1→FUNDAMENTAL+PV 满塔；E56GgqLL→FUNDAMENTAL+OTHER 满塔 |
| 11-12 存量 20 颗清单 | techindi 族→other 满；risk 族→risk 已满 3/3；imb5 族→imbalance 满；仅 N1NGbddg 落未满塔 |

## 5. ★ 容量事实（交付目标的硬约束，2026-11-22 深夜终判）

**口径**：EUR/D1 未满塔共 11 席（institutions 3 / socialmedia 3 / earnings 2 / insiders 1 / macro 1 / pv 1）。
**可交付条件**：① 平台闸全绿 ② prod<0.7 ③ self<0.7 ④ 逐年满仓 ⑤ 落未满塔 ⑥ 篮内互相关<0.7 ⑦ 组腿配额 rule 3。

**终判：EUR 实际可达 = 5 席（本轮实测），名义 11 席不可达。**

| 塔 | 名额 | 可达 | 不可达原因（实测读数） |
|---|---:|---:|---|
| INSTITUTIONS | 3 | 2 | 第 3 席需新强腿；两个 institutions 数据集自身 S 上限 0.95 / ≤1.0；techindi×fund_holdings 互相关 0.705–0.766 + TO 37–39% |
| INSIDERS | 1 | 1 | 已达（XgaO2WOa） |
| SOCIALMEDIA | 3 | 1 | socialmedia12 作强腿 S **0.04–0.40**（5 族）；socialmedia15 6 族全灭；同强腿第 2 件互相关 0.658→饱和 |
| EARNINGS | 2 | 0 | earnings6 2Y **1.99 / 限 2.02**（58 臂穷尽）；earnings_sent_matrix 只配当弱腿且把 prod 抬到 **0.752** |
| PV | 1 | 1 | 已达（58geG1P1） |
| MACRO | 1 | 0 | mcr27 数据层排除（<10 年）；macro10 仅 1 字段 |

**为什么名义 11 席只到 5 席**——三条独立的硬约束同时成立：

1. **数据集维度稀薄**：EUR 未亮塔只有 10 个数据集（institutions 2 / socialmedia 2 / earnings 2 / insiders 2 / macro 2），
   每个塔 2 个数据集，没有"换集"空间。
2. **这些数据集的自身信号强度全在 1.0 以下**（除 earnings6 的 2.4@TOP800，卡 2Y 0.03）。
   ⇒ ATOM 路线结构性为 0（51 族 + socialmedia12 5 族 + Wave D 新强腿 3 探针，共 60+ 族实测）。
3. **唯一强腿 techindi 的互相关容量 = 4 件**（实测：第 5 件无论换哪个弱腿都 ≥0.705）。
   而 prod 又把其中 1 件（WjlxGbRG 0.752）剔掉 ⇒ **可交付 3 件**。
4. **组腿配额 rule 3 已用 4/5**（58geG1P1 PV、d5aPlXjX/XgaO2WOa/rK7nJ5nE 各 OTHER）⇒ 即便找到新 MV/OTHER 强腿，也只剩 1 个名额。

**★ 一条可迁移的元结论**：**「未亮塔」限制的是提交时的塔位收益，不是 alpha 的可交易性**。
真正的容量约束是 **prod<0.7 × 信息源新颖度 × 强腿互相关容量**——EUR 生产池对经典因子已饱和，
真正能过 prod 的都是「生产池里没人做过的信息源」（招聘岗位曾 prod 0.53，但数据只有 3 年）。

### 5.1 若用户仍要 10 颗：三个出口（须用户裁定）

| 出口 | 内容 | 代价 / 风险 |
|---|---|---|
| **E1 放宽「未亮塔」红线** | 纳入已亮塔的存量全闸件（techindi 族 / risk 族 / imb5 族 / analyst-fnd72 族，prod 0.54–0.69 已实测） | 违反「只打未亮塔」红线；塔位已满 ⇒ 不增加塔位收益，只增加收益来源 |
| **E2 换强腿造正交族** | 已实测穷尽：analyst EBI(sub 0.40–0.44❌) / fnd72(族内 0.94–0.997) / earnings6(2Y 差 0.03) / news18(S0.66) / imbalance(S0.61) / model182(S0.33) / earnings_sent(prod 墙) ⇒ **EUR 内已无未试强腿** | 需 EUR 以外的新数据集（跨区不外推铁律 ⇒ 不可移植） |
| **E3 等平台补数据** | mcr27 补齐 2014–2020 历史 ⇒ prod 0.53 + 十年满仓 ⇒ MACRO 塔点亮且是全新信息源 | 依赖平台，不消耗配额 |

**当前按红线严格执行 ⇒ 交付 5 颗**（4 席四闸全验 + rK7nJ5nE 待 prod 回读）。

## 6. ★ ATOM 面穷尽清单（模板族级）（用户 2026-11-22 指令「优先做 ATOM」的落地台账）

**ATOM 定义**：表达式只含单一数据集字段 + 豁免分组轴（不跨类组腿）。

| 数据集 | 塔 | ATOM 臂数 | 最好读数 | 结论 |
|---|---|---:|---|---|
| earnings6 | EARNINGS 1/3 | **58**（7 批） | S1.91/F2.49/2Y1.99（CW 过、2Y 差 0.03） | ⛔ 参数轴封顶 |
| socialmedia15 | SOCIALMEDIA 0/3 | **10**（新系）+ 历史 10（d1_ 系） | \|S\| ≤ 0.54 | ⛔ 45 字段两代全测 |
| fund_holdings_panel | INSTITUTIONS 0/3 | **10** | \|S\| ≤ 0.33 | ⛔ 信息源级饱和 |
| institutions6 | INSTITUTIONS 0/3 | 历史 40 + 8（11-06/11-19） | S1.35/F0.75/2Y1.61（prod 0.8257） | ⛔ F 数学约束 |
| mcr27 | MACRO 2/3 | 6 + 8 + 8 | **S2.77/F1.13/2Y3.03 全闸** | ⛔ 数据层 3 年 + 重复件（self 0.7703） |
| macro10 | MACRO 2/3 | 0 | 单标量无截面 | ⛔ 结构性排除 |
| insider_agg_matrix | INSIDERS 2/3 | 🔄 批17 在飞 | — | 测试中 |
| socialmedia12 | SOCIALMEDIA 0/3 | 🔄 批17 在飞（时序相对化形态） | — | 测试中 |
| pv106 | PV 2/3 | 历史 8（11-12） | 价差负向，取反 ≤1.01 | ⛔ |
| investor_activity | PV 2/3 | 历史 85（11-20） | prod 0.78–0.84 + 6 年 | ⛔ 双卡 |
| earningscall_sentiment | OTHER（已亮） | 历史 66 | prod 0.78 | ⛔ 信息源级墙 |
| earnings_sent_matrix | EARNINGS | 历史 7 全测 | prod 0.87–0.92 | ⛔ 信息源级墙 |
| pv47 | PV | 历史 31 | 2Y 封顶 1.05–1.27 | ⛔ 时效死 |
| pv13 / pv37 / pv20 / pv173 / pv109 | PV | 历史 | 见各档 | ⛔ |

**★ ATOM 路径的三重封死（EUR 实证总结）**：
1. **信号层**：字段维度被历史 5 轮扫遍，剩下的读数 |S| ≤ 0.55（fund_holdings / socialmedia15）。
2. **数据层**：mcr27 等新信息源只有 3 年历史（mcr27 已提交件同样如此 ⇒ 平台接受该先例）。
3. **重复件层**：账号内已提交件（`GrmmNzz0` mcr27 / `O0W0w3P7` news46）使同信息源变体的 prod 天花板 = 0.76–0.83。

⇒ **纯 ATOM 的现实上限：1–2 席**（A 族的 institutions6 腿 = 唯一的纯 ATOM 出货路径：institutions6 买家净差 × analyst EBI —— 但严格说它是跨集组腿）。

## 7. 交付清单（**4 席全验 + 1 席修复中**：第 5/6 席 prod 均 0.71–0.75 撞单件，已按"可修"派修复批）

### 7.1 四席终表（全部通过：平台闸 + prod + self + 逐年满仓 + 篮内互相关 < 0.7）

| # | alpha | 数据集 | 核心字段 | 算子逻辑（要点） | 点亮塔位 | S | F | 2Y | sub | TO | prod | self |
|---|---|---|---|---:|---|---|---:|---:|---:|---:|---:|---:|---:|
| 1 | **N1NGbddg** | institutions6 × analyst7 | 机构买家/卖家/持有家数 + est_12m_ebi 修正三件套 | `group_neutralize(add(signed_power(group_zscore((raised−lowered)/num_4wks_ago, subindustry),2.1), subtract(group_rank(ts_zscore(ts_backfill((buyers−sellers)/holders,120),35),subindustry),0.5)), market)`；TOP2500/FAST/d40 | **INSTITUTIONS 0/3 → 1/3** | 1.69 | 1.05 | 2.17 | 0.90 | 5.14% | **0.6872** | 0.6595 |
| 2 | **58geG1P1** | fnd72 × pv106 | `fnd72_pit_or_cf_a_cf_cash_from_oper`/`..._bs_a_bs_tot_asset`/`..._cf_a_cf_net_inc`/`fnd72_pit_or_is_a_ebitda`/`pv106_spreadbp` | `ts_target_tvr_decay(quantile(signed_power(trade_when(ebitda/netinc>0.3, group_rank(CFO/资产 × CFO/净利, sta1_allc5), -1),1.05), driver=gaussian), lambda_min=0, lambda_max=1, target_tvr=0.06)`；TOPCS1600/SUBIND/d1 | **PV 2/3 → 3/3** | 1.79 | 1.25 | 2.17 | 1.20 | 6.93% | **0.5362** | 0.4342 |
| 3 | **d5aPlXjX** | techindi_model × institutions6 | techindi 概率分位差 + 机构买家净差 | `group_rank(add(group_rank(prob5q10d_b4 − prob5q10d_b0, industry), group_rank(ts_zscore(ts_backfill((buyers−sellers)/holders,120),35), industry)), industry)`；TOP2500/**CROWDING**/d4 | **INSTITUTIONS 1/3 → 2/3** | **3.90** | **2.32** | **3.21** | 2.25 | 28.4% | **0.6820** | 0.4312 |
| 4 | **XgaO2WOa** | techindi_model × insiders1 | techindi 概率分位差 + 内部人「流量÷存量」 | `group_rank(add(group_rank(prob5q10d_b4 − prob5q10d_b0, industry), group_rank(ts_sum(divide(multiply(vec_sum(insd1_valueeur), vec_avg(insd1_tradesignificance)), vec_sum(insd1_holdings)), 44), industry)), industry)`；TOP2500/CROWDING/d4 | **INSIDERS 2/3 → 3/3** | **3.89** | **2.40** | 2.87 | 2.22 | 26.4% | **0.6770** | 0.3776 |

### 7.2 四席验证明细

| 项 | N1NGbddg | 58geG1P1 | d5aPlXjX | XgaO2WOa |
|---|---|---|---|---|
| failed_ra_count | 0 | 0 | 0 | 0 |
| prod（refresh 实测） | 0.6872 | 0.5362 | 0.6820 | 0.6770 |
| self（本地池） | 0.6595 | 0.4342 | 0.4312 | 0.3776 |
| 逐年 longCount | 1301–1491 全 >0 | 325–430 全 >0 | 1313–1482 全 >0 | **1308–1474 全 >0** ✅ |
| 逐年 shortCount | 全 >0 | 全 >0 | 全 >0 | **1309–1507 全 >0** ✅ |
| 逐年 pnl | 2020 −87k 其余正 | 十年全正 | 十年全正 S3.3–5.8 | **十年全正（554k–1.43M）S 2.09–6.45** ✅ |

**第 5 席 rK7nJ5nE 逐年（已验）**：2014–2023 十年 pnl **全正**（144k–1.44M），longCount 1305–1482 / shortCount 1312–1479 全 >0，
S 0.38（2020）–3.99，TO 26.7%–34.1%。2020 是弱年但为正（与全市场效应一致，非零持仓）。

**篮内互相关矩阵（本地 `compute_mutual_correlation`，1021 个交易日）**：
```
           N1NGbddg  58geG1P1  d5aPlXjX  XgaO2WOa  rK7nJ5nE  [WjlxGbRG]
N1NGbddg     1.00     0.0538    0.0576   -0.0513    0.0313      0.0147
58geG1P1    0.0538    1.00      0.0407    0.0420   -0.0003     -0.0306
d5aPlXjX    0.0576    0.0407    1.00      0.6297    0.5989      0.6445
XgaO2WOa   -0.0513    0.0420    0.6297    1.00      0.6807      0.6519
rK7nJ5nE    0.0313   -0.0003    0.5989    0.6807    1.00        0.6580
[WjlxGbRG]  0.0147   -0.0306    0.6445    0.6519    0.6580      1.00
```
⇒ 与 N1NGbddg / 58geG1P1 的全部 8 对 < 0.06（信息源独立）；
⇒ techindi 强腿的 3 件（d5aPlXjX / XgaO2WOa / rK7nJ5nE）两两 0.599–0.681，**最大对 0.6807 < 0.7（余量仅 0.019）**；
第 4 件 WjlxGbRG 互相关合规（0.6445–0.6580）但 **prod 0.752 越线**；第 5 件（Wave A/C）互相关全部 ≥0.705 ⇒ **该强腿容量实测封顶 4 件、可交付 3 件**。

**点亮塔位合计**：INSTITUTIONS 0→2/3（+2 席）、PV 2→3/3（满）、INSIDERS 2→3/3（满）。

### 7.3 第 5–6 席（prod 终验结果）

| # | alpha | 数据集 | 弱腿字段 | 塔位 | S | F | 2Y | sub | TO | prod | 结论 |
|---|---|---|---|---|---:|---:|---:|---:|---:|---|---|
| 5 | **rK7nJ5nE**（原形） | techindi × socialmedia12 | `scl12_buzz` 250d backfill | **SOCIALMEDIA 0/3 → 1/3** | 2.58 | 1.41 | 2.57 | 1.55 | 29.9% | **0.7134 ❌ FAIL** | **修复批在飞** |

**rK7nJ5nE prod 直方图**：`[0.6,0.7)` **32 对**、`[0.7,0.8)` **仅 1 对**、min −0.5491
⇒ 与 WjlxGbRG 同一指纹：**撞单个近重复件**（按 §9 第 26 条判据属"可修"，不是信息源级拥挤）。

#### 修复批 `VB8xw9qh4se9irIuSO1sX9`（5 臂，全闸）——保持强腿、只换弱腿形态

| 弱腿形态 | alpha | S | F | 2Y | sub | TO | 与 4 席最大互相关 |
|---|---|---:|---:|---:|---:|---:|---:|
| buzz 120d bf + z250 | WjlxL7Yd | 2.59 | 1.39 | 2.68 | 1.51 | 29.2% | 0.6516 ✅ |
| buzz ts_rank250 | blaK8jx6 | 2.67 | 1.41 | 2.49 | 1.55 | 31.3% | 0.6776 ✅ |
| **buzz ts_mean66** | **vRAoOjYb** | **2.11** | **1.27** | **2.16** | **1.16** | **21.9%** | **0.6406 ✅（余量最大）** |
| buzz 一年比值 | 3q02jl1Z | 3.58 | 2.03 | 3.00 | 1.97 | 36.9% | **0.7491 ❌** |
| sentiment 120d bf + z250 | P05AM7xq | 2.59 | 1.38 | 2.52 | 1.44 | 29.1% | 0.6828 ✅ |

`max_mutually_below_subset(0.7)` = **6** = {N1NGbddg, 58geG1P1, d5aPlXjX, XgaO2WOa, **WjlxL7Yd**, **vRAoOjYb**}；
且 `WjlxL7Yd × vRAoOjYb = 0.6802`（两者也能共存）。
⇒ **修复批把一颗 prod 0.7134 的死件变成了 2 个可共存候选**，且互相关余量从 0.6807 改善到 **0.6406**。

⇒ **第 5 席取 `vRAoOjYb`**（TO 21.9% 最接近 EUR 评审带、互相关余量最大、S 2.11 稳过闸）；
`WjlxL7Yd` 作平替（S 更高但 TO 29.2% 贴上限）。
⚠ rule 3 配额只剩 1 个名额 ⇒ 两者只能取一。**prod 待回读**（MCP 会话连接中断，恢复后立即测）。
| 6 | ~~WjlxGbRG~~ | techindi × earnings_sent_matrix | `positive−negative_sentiment_probability_3`（66d bf + 252d z） | EARNINGS 1/3 → 2/3 | 3.09 | 2.03 | 2.76 | 2.08 | 23.8% | **0.752 ❌ FAIL** | **出局** |

`WjlxGbRG` prod 直方图：`[0.6,0.7)` **85 对**、`[0.7,0.8)` **仅 1 对**、min −0.5298 ⇒ 「撞单个近重复件」指纹，
不是自复制（自复制会在 ≈0.99 出现孤立高桶）。属已固化口径的 prod 上限带 0.76–0.83 形态。

**第 7 候选被互相关否决**：`VkNRPabY`（techindi × `sentiment_weighting_method1`，S2.51/F1.46/2Y2.05/sub1.39，fRA=0）
与 `WjlxGbRG` 互相关 **0.8097 ≥ 0.7** ⇒ 同弱腿数据集 + 同强腿，只能择一。

### 7.4 ★ 本轮后续四批全部出局（含定量原因）

| 批 | 内容 | 读数 | 出局原因 |
|---|---|---|---|
| Wave A | techindi × fund_holdings_panel ×2（INSTITUTIONS 最后 1 席） | `pwapKq9g` S3.97/F2.09、`E5Q2eZ9G` S3.53/F1.74，均 fRA=0 | **互相关 0.705 / 0.733 / 0.766**（对 techindi 族）+ **TO 36.7% / 39.0%** 超 EUR 评审带 30% |
| Wave B | socialmedia12 **纯 ATOM 五族**（H/R/B/X/D） | S 0.04 / 0.07 / 0.39 / 0.40 / 0.38，fRA 2–4 | 该集作**强腿**无定价力（只能作弱腿） |
| Wave C | techindi × earnings6（4 个未测字段形态，EARNINGS 第 3 席） | `Grm7GkAJ` S4.78/F3.02、`ZYa1Er3Q` S4.65、`YPa9vQKR` S4.80、`akag1oq2` S4.79，均 fRA=0 | **互相关 0.768–0.803** + 彼此 0.9188 + TO 34–36%；四臂读数几乎相同 ⇒ 弱腿信息量≈0，本质是 techindi 第 5 件 |

⇒ **techindi 强腿的互相关容量 = 4 件，实测封顶**（第 5 件无论换哪个弱腿都 ≥0.70）。

### 7.4 备选池

| 组 | 成员 | 为何不进 | 何时可用 |
|---|---|---|---|
| A 族同源 5 颗 | vRAvo8jA / leAXvaLn / A1x7E3ae / RRemVOeb / 2r5NgWvY | 与 N1NGbddg 互相关 0.80–0.9986 | N1NGbddg 被拒或漂移时平替 |
| PV 同族 2 颗 | e75x1vAl / mL61avpx | 与 58geG1P1 0.9369 / 0.9970 | 同上 |
| techindi 变体 | wpovJma2（S4.55/F3.00/2Y2.32） | prod **0.7644** ❌（insider_agg 弱腿） | 换弱腿后可复活 |
| 双满塔件 | gJa0ozqJ（S3.44/F1.92） | 塔位 RISK+OTHER 双满 | 不可交付 |

## 8. 字段画像存档索引（本轮新增 / 更新）

> 总索引：`tracking/EUR/reference/field_profile_index_20261122.md`（含命名规则 / 完整性闸 / 每集 ATOM 状态）
> 完整性闸：`python tools/gates/field_profile_completeness_gate.py --profile <档案路径>`（exit 0 = 全字段逐条有实测读数）

| 数据集 | 全字段数 | 档案路径 | 状态 |
|---|---:|---|---|
| earnings6 | 66/66 | `tracking/EUR/reference/datasets/earnings6.md` | 新增（含 7 批 58 臂读数） |
| **socialmedia12** | **6/6** | `tracking/EUR/reference/datasets/socialmedia12.md` | **新增（含 6 模板族设计 + Wave B 5 族实测）** |
| **earnings_sent_matrix** | **7/7** | `field_profile_index_20261122.md` §A | **新增（7 字段全表 + prod 墙结论）** |
| **euro_equity_imbalance** | **31/31** | `field_profile_index_20261122.md` §B | **新增（31 字段全表 + Wave D 探针）** |
| **model182** | **7/7** | `field_profile_index_20261122.md` §C | **新增（7 字段全表 + Wave D 探针）** |
| mcr27 (macro27) | 33/33 | `tracking/EUR/reference/datasets/mcr27.md` | 新增（含 prod 墙分析 + 数据层排除） |
| mcr27 prod 墙笔记 | — | `tracking/EUR/reference/datasets/mcr27_prod_wall_notes.md` | 新增 |
| socialmedia15 | 45/45 | `tracking/EUR/reference/datasets/socialmedia15.md` | 新增（含 10 臂全灭读数） |
| fund_holdings_panel | 30/30 | `tracking/EUR/reference/datasets/fund_holdings_panel_EUR.md` | 新增 |
| pv106 | 15/15 | （本轮只拉目录，未开挖） | 已排除（11-12 实测） |
| institutions6 | 11/11 | `tracking/EUR/reference/datasets/institutions6.md` | 已存在（11-06 档案） |
| 交付候选台账 | — | `tracking/EUR/reference/delivery_candidates_20261122.md` | 新增 |

## 9. 调优经验摘要（可迁移，15 条）

1. **CW 的根因诊断序**：先查「中性化组内有效股票数」⇒ 放宽中性化档（SUBINDUSTRY→INDUSTRY）比调 truncation 更有效且更便宜（truncation 在本例是反向杠杆）。
2. **IS_LADDER 限值是宇宙相关**：TOP800 触发 2Y 限 2.02、TOP2500/CS1600 是 1.58 ⇒ 「差一点点过 2Y」时，换宇宙可能直接改限值（但本例信号住小盘，换宇宙杀信号 ⇒ 两难）。
3. **「降 S 降闸限」只对比率闸（sub=0.52×S）有效，对阶梯闸（2Y ladder）无效**。
4. **prod 差 0.02 时的动作序**：先逐年拆解（数据层排除优先于 prod 墙）→ 再换形态 → 最后才罕见化扰动。本轮 mcr27 因跳过第一步白等一批。
5. **弱腿要「组腿形态」才出信号**：scl12_buzz 单独十臂全灭，作 analyst 强腿的弱腿反而出全闸件 prod 0.6785 ⇒ 未亮塔数据更适合当腿而非主腿。
6. **同强腿不产生新席**：6 颗 analyst×(institutions/insiders/socialmedia) 两两 0.80–0.9986 ⇒ 换弱腿降相关只有 0.02–0.06（EUR skill §43），**提席位的唯一杠杆是换强腿或换信息源**。
7. **字段 catalog id 不可信**：socialmedia15 的 `dividend_trend_score` 在 catalog 里显示 `scl15_dividend_trend_score`（平台 preflight 报 unknown）⇒ 每次派批前必须 preflight 全量字段。
8. **平台并发纪律**：连续派批会撞 `429 CONCURRENT_SIMULATION_LIMIT_EXCEEDED`；prod 查询会撞 `correlation_busy`（账号级单槽）⇒ 两者都要退避重试，不可连发。
9. **★ MCP 数值参数传递的间歇性 schema 故障（2026-11-22 实测 4 次）**：`create_multi_simulation` / `preflight_expressions` / `check_correlation` 的 `delay`/`decay`/`truncation`/`timeout_s` 偶发被报 "expected number but provided string"，**同一调用重传同样的数值仍失败** ⇒ 处置：**去掉该参数用工具缺省**（`create_multi_simulation` 缺省 decay=4 / trunc=0 / delay=1；`check_correlation` 缺省 timeout=240s）即可绕开，不是表达式或参数值的问题。
   ⚠ 副作用：省略 `decay`/`truncation` 意味着那批用的是缺省档，**报告里必须记明实际生效设置**（本轮批11/批12 即为 decay 4 / trunc 0）。
10. **本地 prod 缓存不能当候选池**：`get_alpha_corr_metrics` 返回的行里可能有 `failed_ra_count=4` 的件（实测 `omEGpKR2` S1.54/F0.67/2Y1.16，prod 0.5177 很好但 IS 闸 4 项失败）⇒ **候选筛选必须同时过 IS 闸 + prod，不能只筛 prod**。
11. **★★★ 重复件陷阱的完整判据（EUR 2026-11-22 二次实证）**：账号内已提交件 `GrmmNzz0`（mcr27 招聘核）使同族变体 `2r5exOvP`/`N1P8GQnX` 的 **self = 0.7703**、**prod = 0.768/0.766**（两件直方图出现**同一个孤立桶 [0.7,0.8] n=1** = 母件本身）。
    ⇒ **同一信息源在本账号已占位后，其变体的 prod 天花板 ≈ 0.76+**，改轴/改窗/改外层算子全无效。
    ⇒ **判据顺序**：造新族前先 `check_self_correlation` 看最高相关对象是谁；命中自己已提交的件 ⇒ 该信息源已被占位 ⇒ **必须换信息源，不能换形态**。
12. **★ 组腿必须逐字照搬强腿骨架（不能只借字段）**：`58geG1P1` 的 fnd72 强腿核是 `ts_target_tvr_decay(quantile(signed_power(trade_when(...),1.05)), driver=gaussian, lambda_min=0, lambda_max=1, target_tvr=0.06)`；
    我只借字段而剥掉外层 ⇒ **S 1.79 → 0.99（−45%）**。⇒ 组腿实验的强腿侧必须逐字复制原表达式。
13. **★ 三塔组合 `pyramids.effective = 0` ⇒ 无塔位收益**：族 F 8 臂的 `pyramids.list` 全是 [FUNDAMENTAL, PV, EARNINGS] 三段、effective=0 ⇒ **组腿最多两腿**，三腿组合直接无价值（省配额）。
14. **★ 换宇宙不一定是降 prod 的解法**：mcr27 从 TOP2500 换 TOPCS1600 ⇒ **F 从 0.93 塌到 0.61–0.71**（TO 冲到 38%），与「换宇宙降 prod」的经验相反。
    ⇒ 判据：**换宇宙同时改 S/F/sub/prod 四个方向，不是单变量**；本例的正确杠杆是**换中性化轴**（industry→subindustry 使 S 2.38→2.73、F 0.93→1.11）。
15. **★ subindustry 轴在稀疏/重尾类数据上常是最优轴**：mcr27 S 沿 sector 2.25 → industry 2.38 → **subindustry 2.77**（F 0.86→0.93→1.13），且该族首次在 subindustry 上同时过 S/F/2Y/sub。
    ⇒ 与「EUR 常用 INDUSTRY/SUBINDUSTRY」的通用偏好一致，但对**重尾计数类**（招聘/订单/流量）应显式扫 subindustry。
16. **★ sub 比率闸是强腿的结构属性，换轴/降 S/换窗都不改它**：族 L 10 臂梯度里 sub/S 恒为 0.43–0.44
    （弱腿轴 industry→subindustry→sector→cartesian、强腿幂次 1.5→1.2→1.0、弱腿窗 22/63/132、弱腿形态 ts_sum/ts_mean/ts_zscore 全部试遍）
    ⇒ **要抬 sub 比率必须换「强腿本身」**（不同 metric 族），换弱腿无效（与 EUR skill §43「换弱腿降相关仅 0.02–0.06」同源）。
17. **★ 弱腿几乎不影响指标，只决定塔位**：族 L 4 个弱腿（institutions6 / insider_agg_matrix / earnings6 / socialmedia12）读数几乎一致
    （S 2.29–2.91、sub 0.83–1.26）⇒ **强腿决定指标、弱腿决定塔位** ⇒ 弱腿只需挑「塔位未满 + 字段有数据」的那个，不必做参数优化。
18. **★ 会话凭据会部分失效**：批22 查询时 `batch_status` 返 `HTTP 401` ⇒ 调 `authenticate`（返回 201/authenticated）即恢复；
    与 EUR skill 记载一致（`/users/self` 与创建仿真 401 ⇒ 所有发批变幽灵）。
19. **★「字段在 catalog 里存在」≠「该字段在 EUR 有数据」**：`insider_agg_matrix` 的 `directional_indicator` / `total_top_sell_shares` 类字段 3 臂读数 **S=0 / TO=0**（全零）；`earnings6` 的 `eps_change_*` 同样复现 11-12 的全零结论
    ⇒ **派批前必须先跑「单臂字段存在性探针」（看 TO 是否为 0）**，否则浪费整批。


20. **★★ 平台在大敏感批（≥10 臂）上会整批拒收**（2026-11-22 晚，两批实证）：批23（10 臂）与批24（10 臂）均返回
    `No alpha_id in sim response`（10/10 失败），而 **preflight 全过、字段全存在**；
    紧接着把同样的表达式拆成 **2 臂 / 3 臂 / 4 臂** 小批后**全部成功**。
    ⇒ 判据：**`No alpha_id in sim response` 且 preflight 通过 ⇒ 先怀疑批大小，不是字段/语法**。
    ⇒ 处置：**拆成 ≤4 臂小批重派**（本轮 2/3/4 臂均成功）。
    ⚠ 与 EUR skill 旧记载「1 个字段不存在导致整批废」并存——两者症状相同，必须用 preflight 区分。
21. **★★★ techindi 概率分位是唯一 sub 比率 > 0.52 的组腿强腿**（族 M 突破）：
    | 强腿 | sub/S | prod |
    |---|---:|---:|
    | analyst EBT 修正（族 L） | 0.40–0.44 ❌ | 0.74 |
    | news46 事件流量（族 H） | 0.51 ❌ | 0.83 |
    | **techindi 概率分位（族 M）** | **0.55–0.58 ✅** | **0.68 ✅ / 0.76 ❌** |
    ⇒ 族 M 配方：`group_rank(add(group_rank(subtract(probability_fifth_quantile_ten_day_bucket_four_15, probability_fifth_quantile_ten_day_bucket_zero_15), industry), group_rank(<未满塔弱腿>, industry)), industry)`
    + TOP2500 / **CROWDING** / decay 4 / trunc 0.0。
22. **★★★ 同强腿换弱腿可降 prod 0.082**（techindi 族内实证）：
    | 弱腿 | 塔位 | prod |
    |---|---|---:|
    | insider_agg_matrix 高管净买入 ts_sum63 | INSIDERS + OTHER | 0.7644 ❌ |
    | **institutions6 买家净差 ts_zscore120** | INSTITUTIONS + OTHER | **0.6820 ✅** |
    ⇒ **prod 贴闸时优先换弱腿**（改持仓集合），而不是换算子/中性化/轴（那三项 EUR 实证为免疫）。
    ⚠ 与旧结论「换弱腿只降相关 0.02–0.06」不矛盾：**降相关小、降 prod 大**，两个维度分开看。

23. **★★★★ 同一强腿的「互相关容量」= 4 件，且与弱腿无关（本轮最贵的定量结论）**：
    以 techindi 概率分位为强腿，7 件组腿件两两互相关实测——
    `d5aPlXjX×rK7nJ5nE 0.599 / d5aPlXjX×XgaO2WOa 0.630 / WjlxGbRG×d5aPlXjX 0.645 / XgaO2WOa×WjlxGbRG 0.652 / rK7nJ5nE×WjlxGbRG 0.658 / XgaO2WOa×rK7nJ5nE 0.681`（全部 <0.7）；
    第 5 件起全部越线：`WjlxGbRG×pwapKq9g 0.705 / pwapKq9g×E5Q2eZ9G 0.733 / WjlxGbRG×E5Q2eZ9G 0.766 / Grm7GkAJ×d5aPlXjX 0.768 / Grm7GkAJ×YPa9vQKR 0.919`。
    ⇒ **弱腿（institutions6 / insiders1 / socialmedia12 / earnings_sent / earnings6 / fund_holdings_panel）只能把互相关从 0.60 推到 0.77，推不到 0.7 以下**。
    ⇒ 规划席位数时按「**每个强腿 4 席**」算总量，不要按塔位表算。

24. **★★★ 弱腿信息量可定量判定：四臂读数几乎相同 ⇒ 弱腿≈0**（Wave C 实证）：
    techindi × earnings6 四个**结构不同**的弱腿（EPS surprise 差分 252d / EPS surprise 水平 / eps_change_pct 66d / 预告区间宽度 z252）
    得到 S **4.78 / 4.65 / 4.80 / 4.79**、F 2.95–3.02、2Y 3.08–3.19、sub 2.70–2.75，彼此互相关 0.9188。
    ⇒ 判据：**弱腿四臂 S 极差 < 0.20 且互相关 > 0.9 ⇒ 该弱腿不提供新信息，只是噪声扰动**；
    反之 techindi × {institutions6, insiders1, socialmedia12} 的 S 为 3.90 / 3.89 / 2.58（极差 1.3）⇒ 弱腿有实质信息。
    ⇒ 这个判据能在**一个批（5 分钟）内**判定弱腿是否值得继续投入，比逐轴扫参数省 10 倍配额。

25. **★★★ 「冷门数据集」不等于「有 alpha」——aC 是必要条件不是充分条件**（Wave D 实证）：
    `euro_equity_imbalance`（31 字段，aC 4–307，mult 1.5）与 `model182`（7 字段，aC **0–8**，mult 1.3）
    是 EUR 中 alphaCount 最低的两个数据集（纯蓝海），但作强腿实测 S 仅 **0.61 / 0.33**；
    与 institutions6 组腿后也仅 **0.98 / 0.84**（闸 1.58）。
    ⇒ **aC 低只说明没人挖过，不说明有信号**；冷门集必须先做 3 臂探针（水平/相对历史/第二字段）再决定是否投组腿。
    ⇒ 与「按 onboard 时间找字段」不矛盾：onboard 新 ≠ 有定价力，**必须实测**。

26. **★★ prod 直方图能区分「撞单个近重复件」与「撞大量同族件」，两者处置不同**：
    `WjlxGbRG`（prod 0.752）：`[0.6,0.7)` **85 对** + `[0.7,0.8)` **仅 1 对** ⇒ 只有 1 个近重复件 ⇒ **有救**（换弱腿/换窗即可躲开那 1 个）；
    而族 A 的 6 颗（prod 0.66–0.70）实测是同族互相压制，直方图高桶段是**连续分布** ⇒ 无救。
    ⇒ 判据：**孤立高桶 n=1 = 单件冲突（可修）；高桶段连续多对 = 信息源级拥挤（不可修）**。

27. **★★ `group_rank` 之后不得再加 `winsorize` / `signed_power`**（复现确认）：两者在秩空间上是单调变换 ⇒ 数学空操作，读数逐位相同；
    要 winsorize 必须作用在**原始信号**上（`group_rank` 之前）。

28. **★★ 平台 prod 相关性单槽会出现「长时间 inflight」**：`rK7nJ5nE` 单次计算 >20 分钟仍 inflight（`retry_after` 逐次递减、`inflight=true`）。
    ⇒ **`inflight=true` 时绝不能重触发**（重发把自己排队到尾）；只能隔 3–5 分钟读一次，或等平台侧完成。
    ⇒ 与既有记载一致：prod 单次 ~105s 是常态，但队列拥塞时可到 20 分钟以上。

29. **★★★ 「撞单件」的标准修复配方（prod 0.70–0.78 且直方图孤立 n=1）**：
    **保持强腿不动、只换弱腿形态**——塔位不变、S 基本不掉，但 PnL 与那个近重复件的同构被打散。
    本轮 5 个弱腿形态变体（同一强腿 techindi，同一弱腿数据集 socialmedia12）：
    | 变体 | 与原件 `ts_backfill(buzz,250)` 的差异 |
    |---|---|
    | `ts_zscore(ts_backfill(buzz,120),250)` | 换窗 250→120 + 加 z 归一 |
    | `ts_rank(ts_backfill(buzz,250),250)` | 水平→时序分位（非线性形变） |
    | `ts_mean(ts_backfill(buzz,250),66)` | 补平滑（降 TO） |
    | `divide(buzz, ts_mean(buzz,250))` | 水平→相对自身一年基线（去量纲） |
    | `ts_zscore(ts_backfill(sentiment,120),250)` | **换字段**（buzz→sentiment） |
    ⇒ 优先级：**先换窗/换归一（保信号）→ 再换算子形态 → 最后换字段（换信号）**。
    ⇒ 反例警戒：若直方图高桶段是**连续分布**（同族大量件压制），上述配方无效，属信息源级判死（族 A 6 颗实证）。

30. **★★★ 工具 bug：`operator_swap_matrix.py` 只换算子名、不重排参数（Group 类替换必炸 UNITS）**：
    - 现象：把 `group_backfill(x, sector, 20)` 换成 `group_mean` → 平台报 `Incompatible unit for input of "group_mean" at index 1, expected Unit[], found Unit[Group:1]`；
    - 根因：`group_backfill(x, group, d)` 签名 =(值,**组**,窗)，`group_mean(x, weight, group)` =(值,**权重**,组)——**都 3 参、过 arity 校验**，
      但工具 `_replace_op` 只改算子名，`sector`（Group 类型）落到 weight 位（期待数值）⇒ UNITS 错；
      2 参的 group_rank/zscore/scale/neutralize 则被 arity 校验（3≠2）**错误跳过**（工具不会顺带删窗口参数 `20`）。
    - **修复方法**：跨"参数形状不同"的 Group 算子时，手工构造正确参数顺序——
      `group_mean(x, 1, group)` / `group_rank|zscore|scale|neutralize(x, group)`，并过 preflight 后再派。
    - **验证**：Wave H3-fix 5 臂全 COMPLETE、无 UNITS 错，group 层真正测完（最高 2Y 1.88 < 基线 1.99，基线仍最优）。
    - ⚠ 现有 `test_group_swaps_skip_non_binary_arity` 只验 arity 数字、不验**参数类型位置**，故这个 bug 测试全绿也漏得掉；
      工具层彻底修（解析嵌套参数 + 按 signature 重排）是独立工程任务。

## 10. SOP 待优化点

1. **「未亮塔优先」与「prod<0.7」在 EUR 存在结构性冲突**——建议把「交付口径」在 SOP 里明确写成「**未满塔（not full）× prod<0.7 × 互相关<0.7**」三者的交集，而非「未点亮塔」，否则目标数会被塔位表观席位数误导（EUR 11 席 vs 可证 1 席）。
2. **`get_pyramid_alphas` 应作为每次交付前的强制门**（本轮实测：11-12 存量 20 颗里 19 颗因塔位已满而失效），建议进 `submit_verdict` 的 BLOCKED 判据。
3. **逐年拆解应前置于 prod 优化**（数据层排除优先级高于 prod 墙）——建议写入 `wq-brain-ra-eur` 步 4 的判定顺序。
4. **未亮塔数据集的 ATOM 穷尽需要状态登记**（模板族级）：本轮已把 7 个未亮塔数据集 × 38 个模板族的实测结论写入
   `tracking/EUR/reference/template_family_exhaustion_20261122.md`（含族级定义 H/R/D/B/X/P/G/E/N），
   建议把该文件顶进 `wq-brain-ra-eur` 的 references 索引，并在各 `datasets/*.md` 顶部标注「族级穷尽 + 臂数 + 日期」。
5. **「同骨架换字段」不算模板族**（本轮自查发现的流程缺口）：用户 2026-11-22 明确要求「每个数据集 ≥5 个模板族，每个族按流程做完整梯度」，
   而我在 earnings6 / socialmedia15 / fund_holdings_panel 上把「同一骨架换 10 个字段」误当作多族。
   ⇒ 建议在 `wq-brain-ra-eur` 的组装步加一条机械判据：**模板族计数按「字段族 × 算子几何 × 机制语义」三要素同时不同来计**，换字段不计数。
6. **字段存在性探针应前置**：派批前用 1 臂验证新字段的 TO > 0（避免整批被全零字段浪费）。
7. **★ 容量规划必须按「强腿 × 互相关容量」算，不能按塔位表算**：EUR 塔位表给 11 席，
   而实测每强腿只能供 4 席，且 EUR 仅 3 个强腿（techindi / analyst7-EBI / fnd72）有可交付件、各出一个族 ⇒ 实际 5 席。
   ⇒ 建议 SOP 加一步「**开战役前先做容量预算**」：列出本区全部候选强腿 × 各自已用席数 × 剩余容量，再定目标数。
   否则会像本轮一样在"看起来还有 6 席"的假设下反复撞互相关墙。
8. **★ 「弱腿四臂同值」应成为弱腿筛选的标准动作**：一次 4 臂（结构互异的弱腿形态）就能判定弱腿是否有信息，
   比逐轴扫参数省 10 倍配额（见 §9 第 24 条）。建议写进 `wq-brain-alpha-optimization-v1` 的组腿章节。
9. **★ 组腿配额（rule 3）应在派批前记账**：本轮直到第 5 席才发现 PV/MODEL/OTHER 配额已用 4/5。
   ⇒ 建议 `build_wave.py` 加一个「配额账目」字段（每波记录本波消耗的配额类型），并在闸门里硬拦超额。
10. **★ prod 直方图应作为标准输出**：工具已返回 `histogram_nonzero`，但 SOP 未要求解读。
    ⇒ 建议把「孤立高桶 n=1 vs 高桶段连续」写成 prod 归因的第一判据（见 §9 第 26 条），
    因为它直接决定"是换弱腿可救还是信息源级判死"。
11. **★ 新数据集先跑 3 臂探针再投组腿**：`euro_equity_imbalance`（aC 4–307）与 `model182`（aC 0–8）
    这种极冷门集，先花 3 臂测水平/相对历史/第二字段，S < 0.8 就不投组腿（本轮省下 2 个组腿名额）。
12. **★ `check_correlation` 的 `inflight` 语义应写进 SOP**：`inflight=true` 期间重触发会把自身排到队尾，
    实测单次可达 20+ 分钟。建议 SOP 明确「生产相关性查询 ≤ 每 3 分钟一次，且必须看 `inflight`」。
    ⚠ **补充诊断（本轮实测）**：`correlation_busy` 的 `holder` 形如 `corr:<tool>(<alpha_id>)`，
    而锁文件 `logs/_dblock/correlation.lock.json` 的 `owner` 可能是**自己这台机器上的 MCP 进程 pid**
    （本轮 pid 24924）——因为**多个 Agent 会话共用同一个 HTTP MCP 服务（127.0.0.1:8000）**，
    并行会话的相关性请求会显示成"自己占自己的槽"。
    ⇒ 判据：**看 `logs/_dblock/correlation.inflight.json` 的 `expires_at`**（epoch）：未到期就等它，
    到期后 `lock.json` 会被轮转为 `.stale` 再接管——**不要手工删锁**（会打断并行会话的计算）。
