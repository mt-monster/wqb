# DEU × other（组合分支）

> 回到 [DEU 区域流程](../SKILL.md) · [DEU profile（证据与历史）](../../wq-brain-ra-pipeline/references/regions/DEU.md) · 实时生效画像：`$WQ_PY -m wqb.profiles explain --region DEU --category other`

<!-- profiles:cell-panel:start -->
**状态**：active（跟区域入场 active）　**分组**：Other　**类别卡**：other

**涉及数据集**：dl_riskfree_returns、grtransform、insider_matrix、insider_trx_matrix、lean_le89、order_book_imbalance、other250、other455、other47、other47 (semrush)、other545、other699、tower_sprint_r103、tower_sprint_r104

### 回测设置（进仿真的值）

| 设置 | 值 | 来源 |
|---|---|---|
| instrumentType | EQUITY | 区域 settings.json |
| region | DEU | 区域 settings.json |
| universe | TOP500 | 区域 settings.json |
| delay | 1 | 区域 settings.json |
| neutralization | SUBINDUSTRY | 区域 settings.json |
| decay | 4 | 区域 settings.json |
| truncation | 0.08 | 区域 settings.json |
| pasteurization | ON | 区域 settings.json |
| unitHandling | VERIFY | 区域 settings.json |
| nanHandling | OFF | 区域 settings.json |
| maxTrade | OFF | 区域 settings.json |
| language | FASTEXPR | 区域 settings.json |
| visualization | false | 区域 settings.json |
| startDate | 2013-01-01 | 区域 settings.json |
| endDate | 2023-12-31 | 区域 settings.json |

### 阈值

- Mode B 主闸 sharpe / fitness：1.25 / 0.8（thresholds_override:DEU；下限锁生效，实时值看 explain）
- 其余阈值跟区域 thresholds.json（本组合无覆盖）

### 证据（2026-10-04 只读汇总）

| 回测 | RA 全过 | prod 已测 | 其中低于上限 | 判死 | 胜绩 |
|---|---|---|---|---|---|
| 401 | 47 | 50 | 6 | 8 | 1 |

主要数据集（回测数）：other455（227）、dl_riskfree_returns（68）、other699（31）、other545（22）、grtransform（10）、insider_trx_matrix（10）、lean_le89（8）、other250（8）

### S1 字段理解

- 数据集名会骗人：必读字段 description；稀疏高 valueScore 是陷阱
- 窗口（类别卡，均在白名单内）：daily 5/22；quarterly 66/252

### S2 生成

- **说明**：合规单信号形态的天花板约 0.69（other545，22 探针）；6 颗历史 ACTIVE 全靠 4~5 腿 add 相加——该形态被禁，没有可继承的配方（DEU profile 2026-10-02）
- **说明**：other455 纯复合 S 1.51 / prod 0.4531 干净，但撞 sub_universe 比值墙（n2v 只覆盖 97 股）：下一步把覆盖问题与形态合规分开解决
- **类别通用原语**（类别卡，跨区）：
  - name the priced risk first; the operator is secondary
  - 先按字段 description 判断经济含义，再套对应类别卡的思路（例：KOR other466 是财务比率 → fundamental；IND other532 是 Barra 特质收益 → 残差反转）
- **跨区结论**（KOR/EUR/DEU/GBR；negative）：other455 网络嵌入（n2v）族（证据：KOR RULES §G；EUR-W253-OTHER455-CUSTOMER-NETWORK-RETURNS；DEU-OTH455-PURECOMP-SUBUNIVERSE-WALL-20260923；GBR 红榜） <!-- lint:const-ok 证据原文 -->
- **禁止**（全局锁定）：禁止两条独立信号腿相加：加权（0.4×A + 0.6×B）、等权 add(rank(A), rank(B))、中缀 + 都算；第二个数据集只以条件（trade_when / if_else）、分组（group_rank / bucket）或残差（regression_neut / vector_neut）入场
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

- 资格判定：`$WQ_PY tools/mode_b_qualify.py evaluate --region DEU --sharpe <S> --fitness <F> --two-year-sharpe <2Y>`（喂全指标，旁路 A–E 才会生效）
- 提交链：`submit_verdict` 只否决；prod 与 self 双端点实测（`check_correlation(refresh=True)`）；用户明确确认后才 `workflow_submit_alpha(confirm_submit=True)`——见 `worldquant-submit-alpha`

### 判死记录（不要重试；「归属」= payload 绑定 / 由条目名推断 / 关键词推断）

| 条目 | 族 | 下次怎么办 / 说明 | 数据集 | 归属 |
|---|---|---|---|---|
| DEU-INSIDER-SELL-2Y-WALL | insider_matrix EUR 董事交易（value_2/3/4 卖出系） |  | insider_matrix | inferred | <!-- lint:const-ok 证据原文 -->
| DEU-INSIDER-TRX-MATRIX-CEILING-20260922 | insider_trx_matrix net insider conviction | DEU 不投 insider_trx_matrix；内部人净交易方向单腿天花板 ~0.33。 | insider_trx_matrix | payload | <!-- lint:const-ok 证据原文 -->
| DEU-OTH455-PURECOMP-SUBUNIVERSE-WALL-20260923 | other455 pure composite (non-spine) | other455 无脊柱纯复合路线关闭（不调参、不加腿——墙是覆盖性的）；若平台扩大 other455 DEU 覆盖或 sub_universe 口径变化可复活 O0NxWZMR | other455 | inferred | <!-- lint:const-ok 证据原文 -->
| DEU-OTH47-FAMILY-PROD-WALL-20260916 | web_traffic_visibility |  | other47 (semrush) | payload | <!-- lint:const-ok 证据原文 -->
| DEU-OTHER250-DEAD | other250 |  | other250 | inferred | <!-- lint:const-ok 证据原文 -->
| DEU-OTHER47-PROD-WALL | other47 web 流量 z-score（organic traffic 系） |  | other47 | inferred | <!-- lint:const-ok 证据原文 -->
| DEU-OTHER545-NETMOMO-CEILING-20260922 | other545 network momentum (NEMO 2.0) | DEU 不再投 other545（网络动量方向不成立）；零竞争≠有信号。OTHER 塔白空间已穷尽（other545/insider_trx_matrix 为本区最后两个未测 OTHER 集）。 | other545 | payload | <!-- lint:const-ok 证据原文 -->
| DEU-OTHER699-RETAIL-FLOW-DEAD-20260920 | other699 TipRanks retail-investor transaction events | DEU 不再投 other699（散户交易流方向不成立）；零竞争≠有信号——『无人用』本身是弱信号先验而非机会。 | other699 | payload | <!-- lint:const-ok 证据原文 -->

### 胜绩

| 条目 | 机制 | 设置与骨架 | 数据集 | 归属 |
|---|---|---|---|---|
| DEU-DLRISKFREE-WIN | dl_riskfree_returns |  | dl_riskfree_returns | inferred | <!-- lint:const-ok 证据原文 -->
<!-- profiles:cell-panel:end -->

## 补充说明（手写）

<!-- profiles:manual:start -->
<!-- profiles:manual:end -->
