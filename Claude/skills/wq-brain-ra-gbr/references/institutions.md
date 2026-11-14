# GBR × institutions（组合分支）

> 回到 [GBR 区域流程](../SKILL.md) · [GBR profile（证据与历史）](../../wq-brain-ra-pipeline/references/regions/GBR.md) · 实时生效画像：`$WQ_PY -m wqb.profiles explain --region GBR --category institutions`

<!-- profiles:cell-panel:start -->
**状态**：active（跟区域入场 active）　**分组**：Institutions　**类别卡**：institutions

**涉及数据集**：fund_holdings_panel、institutions6

### 回测设置（进仿真的值）

| 设置 | 值 | 来源 |
|---|---|---|
| instrumentType | EQUITY | 区域 settings.json |
| region | GBR | 区域 settings.json |
| universe | TOP700 | 区域 settings.json |
| delay | 1 | 区域 settings.json |
| neutralization | SUBINDUSTRY | 区域 settings.json |
| decay | 4 | 区域 settings.json |
| truncation | 0.08 | 区域 settings.json |
| maxTrade | OFF | 区域 settings.json |
| pasteurization | ON | 区域 settings.json |
| unitHandling | VERIFY | 区域 settings.json |
| nanHandling | ON | 区域 settings.json |
| language | FASTEXPR | 区域 settings.json |
| visualization | false | 区域 settings.json |
| startDate | 2014-01-01 | 区域 settings.json |
| endDate | 2023-12-31 | 区域 settings.json |

### 阈值

- Mode B 主闸 sharpe / fitness：1.25 / 0.8（default；下限锁生效，实时值看 explain）
- 其余阈值跟区域 thresholds.json（本组合无覆盖）

### 证据（2026-10-04 只读汇总）

| 回测 | RA 全过 | prod 已测 | 其中低于上限 | 判死 | 胜绩 |
|---|---|---|---|---|---|
| 88 | 0 | 0 | 0 | 2 | 0 |

主要数据集（回测数）：institutions6（88）

### S1 字段理解

- 季频慢变量：适合当 trade_when 慢开关（进 >0.5 出 <0.4 的滞回带），不适合当快信号
- 窗口（类别卡，均在白名单内）：quarterly 66/252

### S2 生成

- **类别通用原语**（类别卡，跨区）：
  - owner change vs owner level: flow, not the stale holding
  - concentration vs breadth of holders
  - country/industry relative ownership, not a screening flag
  - institutional momentum: new positions vs closed positions
  - ownership stability: long-term holders vs short-term traders
- **跨区结论**（IND/ASI/KOR/EUR；negative）：institutions6 作主信号判死；作慢门控腿可用（IND levk5JYN：机构持股比例 rank>0.5，prod 0.55）（证据：IND institutions6 best 0.32；ASI 死名单；KOR 红榜；EUR-INSTITUTIONS6-COLD-ZERO-YIELD） <!-- lint:const-ok 证据原文 -->
- **禁止**（全局锁定）：禁止两条独立信号腿相加：加权（0.4×A + 0.6×B）、等权 add(rank(A), rank(B))、中缀 + 都算；第二个数据集只以条件（trade_when / if_else）、分组（group_rank / bucket）或残差（ts_regression / group_neutralize / vector_neut）入场（★ 2026-10-20 更正：'vector_neut' **平台可用**——本地算子清单缺它是假阳性，EUR 平台已用它交付 JjQmx9nm；'regression_neut' 仍非平台算子名）
- **禁止**（全局锁定）：禁止 ts_event_* 系列（平台没有）与幽灵算子；字段名逐一经 get_datafields 验证

### S4 改进（按顺序试：组合 → 类别卡 → 全局）

1. [全局] 判「无解 / 天花板」前先扫等价算子替换：signed_power → quantile、ts_scale → quantile / normalize。数值路径不同，一次动多个闸（含 prod，要读全部闸）（KOR/GLB 复现：KOR other466 signed_power→quantile：2Y 1.51→1.56、prod 0.6544→0.6397；GLB quantile 替 ts_scale：S +0.20、F +0.06、prod 0.475→0.565（DEC-72）） <!-- lint:const-ok 证据原文 -->
   - 注意：效应量逐区实测，禁外推；quantile 只收 1 个参数
2. [全局] 强但撞 prod 墙的快信号：用一个经济子集门控（trade_when 进 >0.5 出 <0.4 的慢变量，或 rank(cap)>0.2 ∩ 子集）只在子集里持仓（GLB/ASI/IND 复现：GLB-DL20D-SUBSET-GATE-FAMILY-20260921（prod 0.82→0.60–0.67）；ASI LLNgdpw2 / 88jaV5lv；IND ZYbqREW1 / levk5JYN（prod 0.54–0.55）） <!-- lint:const-ok 证据原文 -->
   - 前提：未门控的基础信号 IS sharpe 不低于 2.5、fitness 不低于 1.5（GLB 2026-09-27 铁律：门控只修 prod / robust，不造强度）；慢信号门控后换手会升，只用于快信号
- 提醒：prod 与 self 两个端点都取 max、都过线才可提；不改持仓的降 prod 杠杆（hump、加大 decay）会把 self 推爆（EUR wave274） <!-- lint:const-ok 证据原文 -->
- 提醒：设置是强度闸：nanHandling / maxTrade / decay / 中性化换档等于换信号，跨档结果不可比（IND 行为族 S 2.19→0.46） <!-- lint:const-ok 证据原文 -->
- 提醒：decay 匹配信号速度：快信号上 decay 越大越差；decay 0 与 1 逐位相同，只留一个 <!-- lint:const-ok 证据原文 -->
- 提醒：prod 墙先看直方图分单颗钉子 / 密墙 / 可破三型，再决定换分母、换设置档或分组轴（决策表 D0-P 诊断前置） <!-- lint:const-ok 证据原文 -->

### S5 提交前

- 资格判定：`$WQ_PY tools/mode_b_qualify.py evaluate --region GBR --sharpe <S> --fitness <F> --two-year-sharpe <2Y>`（喂全指标，旁路 A–E 才会生效）
- 提交链：`submit_verdict` 只否决；prod 走 `check_correlation(refresh=False)`（48h 缓存优先，不默认回源）+ self 实测；用户明确确认后才 `workflow_submit_alpha(confirm_submit=True)`——见 `worldquant-submit-alpha`

### 判死记录（不要重试；「归属」= payload 绑定 / 由条目名推断 / 关键词推断）

| 条目 | 族 | 下次怎么办 / 说明 | 数据集 | 归属 |
|---|---|---|---|---|
| GBR-FUNDHOLDINGS-DEAD | fund_holdings_panel | 不生成 fund_holdings_panel 表达式 | fund_holdings_panel | inferred | <!-- lint:const-ok 证据原文 -->
| GBR-INST6-HOLDINGS-CEILING-20260929 | institutions6_institutional_holdings_flow | institutions6机构持仓/流量族不再生成新变体（含几何/分组轴/窗口）；GBR institutions塔判死 | institutions6 | payload | <!-- lint:const-ok 证据原文 -->
<!-- profiles:cell-panel:end -->

## 补充说明（手写）

<!-- profiles:manual:start -->
### 2026-10-31 · institutions1 判死 ⇒ INSTITUTIONS 塔在 GBR 结构性不可达（5 个数据集全排除）

论坛帖 `43212475386007`（DEU `institutions1`「流量/存量比 + `ts_sum(·,66)` + `group_rank`」报 **S 1.53–1.59**）在 GBR 从未被实测过 —— 此前被「cov 0.3118 必崩」的先验跳过，而那其实是 `insiders1`（另一数据集）的失败结论。本轮用 4 条**单自由度探针**（弱几何 vs 强几何）复测：

| 探针 | 表达式核心 | S | 2Y | 备注 |
|---|---|---:|---:|---|
| P1 | `group_rank(ts_sum(divide(vec_sum(inst1_shares), vec_sum(inst1_holdings)), 66), industry)` | **−0.27** | −1.14 | 帖原版裸骨架 |
| P2 | 同 SIG + 强几何基底 | 0.28 | **2.22** | 强几何**救不回不存在的信号** |
| P3 | `group_rank(vec_count(inst1_valueeur), industry)` | −0.14 | −0.23 | **TO 27.07%**（稀疏事件裸计数爆换手） |
| P4 | 同 P3 强几何 | 0.32 | 0.69 | |

⇒ **4/4 全灭 ⇒ `institutions1` 判死**。注意 `inst1_shares` / `inst1_valueeur` 是**股数 / 欧元金额**，
与存量 `inst1_holdings`（股数）同单位相除才过 `unit_handling=VERIFY`；帖里的 `valueeur/holdings`（EUR/股）**量纲不一致**，未采用。

★ **归因修正**：此前记「`institutions1` 是机构持股、`insiders1` 是内部人交易 ⇒ 主体性质不同」—— **错**。
`inst1_holdings` 的平台描述明写 *"held by the **insider** after the reported transaction"* ⇒ **两者都是内部人申报交易**，
真正的差异是 GBR 的披露制度 ≠ DEU。

⇒ **GBR `institutions` 类目 5 个数据集全排除**：`fund_holdings_panel`（cov 0.9099，24 探针，真 F 墙）·
`institutions6`（cov 1.0，天花板 |S| 0.56）· `institutions4`（cov 0.39，平台描述是 FSYM_ID/CUSID/ISIN **标识符映射 ⇒ 非信号数据**）·
`institutions25`（cov 0）· `institutions1`（本轮判死）。
**⇒ 跨区补量请走 IND 的 `institutions6` 卖压回归族（`E5VNe67L` S 3.20 / F 2.52 / 2Y 3.00，INSTITUTIONS+PV 双塔），不要在本区继续派发。**
（提交前五道闸见 [`../rules/gate-and-submit-discipline.md`](../rules/gate-and-submit-discipline.md)；字段通道地图见 `docs/reference/GBR/field_mechanism_map_20261031.md`。）

### 2026-11-09 修正：institutions25 = 做空经理数据；institutions4 不是标识符映射

**★ `institutions25` 此前被记成「cov 0 ⇒ 无数据」，实读 20 字段全是做空机构行为面**（不是 13F 多头持股）：
`inst25_crowding`（拥挤度 0–100）· `inst25_concentration`（前三大空头占比）· `inst25_position` / `inst25_position_change` ·
`inst25_security_cover_count`（平空笔数）· `inst25_security_short_count`（开空笔数）· `inst25_security_trade_count_1wk/1mo/3mo/1yr` ·
`inst25_activity` · `inst25_manager_count` · `inst25_age`。
⇒ **它与 `shortinterest3`（借贷费/券源）是两个不同信息通道，且都在禁混集合外 ⇒ 组腿不限量**，是 GBR 少见的合规扩席口子。

实测（GBR / TOP700 / D1，主腿对比）：

| 主腿机制 | 短腿 | S | 2Y | 结论 |
|---|---|---:|---:|---|
| `reverse(group_rank(ts_zscore(ts_backfill(vec_avg(inst25_crowding),66),126),sector))` | `transaction_count_main` | 1.19 | 1.39 | 短腿太弱，不代表主腿 |
| `divide(vec_sum(inst25_security_cover_count), add(vec_sum(inst25_security_short_count),1))` 开平比 | `transaction_count_main` | 0.28 | 2.26 | 比值 2Y 高但 S 崩 |
| `reverse(group_rank(ts_zscore(ts_backfill(vec_sum(inst25_position_change),66),126),sector))` | `transaction_count_main` | 1.15 | 1.54 | 同族 |

★ **纠错：`institutions4` 不是「FSYM_ID/CUSID/ISIN 标识符映射」**。实读 6 字段为
`institutional_holding_current_market_value` / `current_shares` / `percent_of_portfolio` / `percent_of_shares_outstanding` /
`previous_market_value` / `previous_shares` ⇒ **可用于「机构净增持率」的真信号**。
但纯 ATOM 形态实测 **S −0.37**（wave-M），单独不做信号，只可作组合腿候选。

## ★★★ ANALYST × INSTITUTIONS 组合跨区移植证伪（2026-11-09 实测 · 重要）

**为什么这条值得单独记**：`ANALYST` 与 `INSTITUTIONS` 两腿**都在 `{PV,MODEL,OTHER}` 之外**，
按 GBR 规则**不占组腿配额**，且该配方在 EUR 已跑通（EUR 冠军 `N1NGbddg`：S1.69 / F1.05 / 2Y2.17）。
理论上它是扩席的完美路径 —— 实测**全灭**。

GBR 可用字段（6 个全部存在）：
- 主腿 `divide(subtract(est_12m_ebi_raisednum_4wks, est_12m_ebi_lowerednum_4wks), est_12m_ebi_num_4wks_ago)`（EBI 修正广度比率）
- 小腿 `divide(subtract(count_institutional_buyers_security, count_institutional_sellers_security), count_institutional_holders_security)`

| 变体（结构差异） | S | 2Y |
|---|---:|---:|
| **V1 = EUR 冠军原样**（signed_power 2.1 + `-0.5` 小腿 + market 外中性化，12 算子） | **0.88** | **0.60** |
| V2 主腿朴素 `group_rank` + 小腿 `group_zscore`（9 算子） | 0.51 | −0.30 |
| V3 主腿 `ts_rank(66)` 平滑等权 | 0.34 | 1.09 |
| V4 小腿换买盘单腿比率（`buyers/holders`） | **0.98** | 0.89 |
| V5 = V1 但外中性化 market→subindustry | 0.73 | 0.48 |
| V6 主腿改 `ts_delta(21)` 广度动量 | 0.35 | 0.60 |

⇒ **EUR 冠军原样搬到 GBR 只有 S0.88 / 2Y0.60**（EUR 1.69 / 2.17），6 个结构变体最高 0.98。
**组合层的 alpha 同样不可跨区搬运**，与「GOLD2 主腿离开借券短腿就崩」是同一枚硬币的两面：
GBR 的强度绑定在 `loaned_share_count_main` 这条借券腿的**区内**信息上。

**规则化**：跨区移植只有两种情况才值得花一票——① 该机制在**本区单腿探针**已显示 S≥1.0；
② 移植的是**几何结构**（如 `-0.5` 居中、`ts_zscore` 后 `rank`），不是**腿的语义**。
腿的语义（谁是主腿、谁是短腿）必须在本区重测。

**附：`institutions` 侧的可用读数**（除已知 `institutional_*` 六字段外）
`count_institutional_buyers_security` / `count_institutional_sellers_security` / `count_institutional_holders_security`
是**广度计数**三件套（不是市值），可作组合腿的分母/分子；单独做 ATOM 实测同族全弱。

<!-- profiles:manual:end -->
