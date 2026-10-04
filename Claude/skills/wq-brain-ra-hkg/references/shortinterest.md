# HKG × shortinterest（组合分支）

> 回到 [HKG 区域流程](../SKILL.md) · [HKG profile（证据与历史）](../../wq-brain-ra-pipeline/references/regions/HKG.md) · 实时生效画像：`$WQ_PY -m wqb.profiles explain --region HKG --category shortinterest`

<!-- profiles:cell-panel:start -->
**状态**：probe（跟区域入场 probe-only）　**分组**：ShortInterest　**类别卡**：shortinterest

**涉及数据集**：shortinterest55

### 回测设置（进仿真的值）

| 设置 | 值 | 来源 |
|---|---|---|
| instrumentType | EQUITY | 区域 settings.json |
| region | HKG | 区域 settings.json |
| universe | TOP800 | 区域 settings.json |
| delay | 1 | 区域 settings.json |
| neutralization | SECTOR | 区域 settings.json |
| decay | 4 | 区域 settings.json |
| truncation | 0.08 | 区域 settings.json |
| maxTrade | ON | 区域 settings.json |
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
| 8 | 0 | 1 | 0 | 0 | 17 |

主要数据集（回测数）：shortinterest55（8）

### S1 字段理解

- YYYYMMDD 交易日字段（如 KOR shrt38_stk_invacttd_drt）不是信号
- 累积口径偏 2Y、当日口径偏 IS（KOR shortinterest38 实证，作选区先验，不作类别结论）
- 窗口（类别卡，均在白名单内）：daily 5/22；long 252/504

### S2 生成

- **类别通用原语**（类别卡，跨区）：
  - short interest change: delta of short interest vs float
  - short squeeze potential: high short interest + positive catalyst
  - short covering: rapid decline in short interest
  - days to cover: short interest vs average daily volume
  - short interest momentum: acceleration of short interest changes
- **跨区结论**（IND/ASI；negative）：shortinterest5 价带宽度在 TOP500 级宇宙没有横截面离散度（证据：IND-SHORTINTEREST5-PRICEBAND-DEAD；ASI-SI5-MCR63-RSK70-CORRGATE-WEAK-20260921） <!-- lint:const-ok 证据原文 -->
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

- 资格判定：`$WQ_PY tools/mode_b_qualify.py evaluate --region HKG --sharpe <S> --fitness <F> --two-year-sharpe <2Y>`（喂全指标，旁路 A–E 才会生效）
- 提交链：`submit_verdict` 只否决；prod 与 self 双端点实测（`check_correlation(refresh=True)`）；用户明确确认后才 `workflow_submit_alpha(confirm_submit=True)`——见 `worldquant-submit-alpha`

### 胜绩

| 条目 | 机制 | 设置与骨架 | 数据集 | 归属 |
|---|---|---|---|---|
| HKG-DUALGATE-EXP-20260909 | shortinterest55 · 双门实验 |  | shortinterest55 | inferred | <!-- lint:const-ok 证据原文 -->
| HKG-G7-REGIME-GATED-PREMIUM | shortinterest55 · 最佳结构 |  | shortinterest55 | inferred | <!-- lint:const-ok 证据原文 -->
| HKG-QMWLONOE-BEST-OVERALL | shortinterest55 · 全天最佳 |  | shortinterest55 | inferred | <!-- lint:const-ok 证据原文 -->
| HKG-QMWLONOE-MODEB-CEILING-20260909 | shortinterest55 · Mode B 参数化到顶 |  | shortinterest55 | inferred | <!-- lint:const-ok 证据原文 -->
| HKG-QMWLONOE-MODEC-ROUND1-20260909 | shortinterest55 · 结构级变体 |  | shortinterest55 | inferred | <!-- lint:const-ok 证据原文 -->
| HKG-QMWLONOE-MODEC2-ZFIX-20260909 | shortinterest55 · zfix 方向修正 |  | shortinterest55 | inferred | <!-- lint:const-ok 证据原文 -->
| HKG-QMWLONOE-STATISTICAL-MODEA-20260909 | shortinterest55 · Mode A 突破 |  | shortinterest55 | inferred | <!-- lint:const-ok 证据原文 -->
| HKG-QMWLONOE-TRADEWHEN-BREAKTHROUGH-20260909 | shortinterest55 · trade_when 突破 |  | shortinterest55 | inferred | <!-- lint:const-ok 证据原文 -->
| HKG-QMWLONOE-TRUNC-EXHAUSTED-20260909 | shortinterest55 · Mode A 到顶 |  | shortinterest55 | inferred | <!-- lint:const-ok 证据原文 -->
| HKG-QP3VJJO5-BEST-RA-CANDIDATE | shortinterest55 · 最佳 RA 候选 |  | shortinterest55 | inferred | <!-- lint:const-ok 证据原文 -->
| HKG-REGIME-SWITCH-IS-THE-ALPHA | shortinterest55 空头执行价溢价 · 归因修正 |  | shortinterest55 | inferred | <!-- lint:const-ok 证据原文 -->
| HKG-REGIME-SWITCH-SURVIVES-PPA-BUDGET | shortinterest55 · 制度切换 |  | shortinterest55 | inferred | <!-- lint:const-ok 证据原文 -->
| HKG-SHORT-EXECUTION-PRICE-PREMIUM | short-selling execution price premium (shortinterest55) |  | shortinterest55 | inferred | <!-- lint:const-ok 证据原文 -->
| HKG-SHORTINT-LIT-20260910 | shortinterest55 · 点塔达成 |  | shortinterest55 | inferred | <!-- lint:const-ok 证据原文 -->
| HKG-SHORTINTEREST55-PROD-CLEAN-VIA-COLD-FIELDS | shortinterest55 · prod 规避 |  | shortinterest55 | inferred | <!-- lint:const-ok 证据原文 -->
| HKG-SHORTPREM-LIQUIDITY-BAND | shortinterest55 · 流动性band |  | shortinterest55 | inferred | <!-- lint:const-ok 证据原文 -->
| HKG-W15-TOP500-RESULTS | shortinterest55 · w15 |  | shortinterest55 | inferred | <!-- lint:const-ok 证据原文 -->
<!-- profiles:cell-panel:end -->

## 补充说明（手写）

<!-- profiles:manual:start -->
<!-- profiles:manual:end -->
