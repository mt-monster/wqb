# GBR × insiders（组合分支）

> 回到 [GBR 区域流程](../SKILL.md) · [GBR profile（证据与历史）](../../wq-brain-ra-pipeline/references/regions/GBR.md) · 实时生效画像：`$WQ_PY -m wqb.profiles explain --region GBR --category insiders`

<!-- profiles:cell-panel:start -->
**状态**：active（跟区域入场 active）　**分组**：Insider　**类别卡**：insiders

**涉及数据集**：insider_agg_matrix

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
| 18 | 0 | 0 | 0 | 1 | 0 |

主要数据集（回测数）：insider_agg_matrix（18）

### S1 字段理解

- 稀疏事件矩阵作主信号常撞 CW / 稀疏墙
- 窗口（类别卡，均在白名单内）：event 5/22；monthly 66

### S2 生成

- **类别通用原语**（类别卡，跨区）：
  - 交易方向与规模：净买入 / 净卖出，取负放在 rank 之后并保持零均值（决策表 D6）
  - 持续性：内部人连续同向交易的次数，而不是单次交易
  - 相对：按行业 / 市值分组比较，避免把行业交易季节性当信号
- **跨区结论**（KOR/DEU/USA/EUR；negative）：insiders 数据集作主信号天花板低（证据：KOR insiders5 1.05、insider_feats prod 0.7185；DEU insider_trx_matrix 0.33；USA-INSIDER-MATRIX-SPARSE-EVENT-WALL；EUR-INSIDER-AGG-MATRIX-COLD-ZERO-YIELD） <!-- lint:const-ok 证据原文 -->
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
| GBR-INSIDER-AGG-CEILING | insider_agg_matrix | IS 天花板 0.51 + CW 闸结构性超闸 + 2Y 全弱，10 条结构无路径可过全闸 | insider_agg_matrix | payload | <!-- lint:const-ok 证据原文 -->
<!-- profiles:cell-panel:end -->

## 补充说明（手写）

<!-- profiles:manual:start -->
### 2026-11-09 ★★ insider_agg_matrix 只有 3 个字段可用，其余会连坐整批

字段实读（GBR TOP700 / D1）：`total_buy_shares` / `total_sell_shares` / `directional_indicator` 可用
（`88RxLYXl`、`xArpnW5m` 已证明）。**以下字段虽然 `get_datafields` 返回 MATRIX 且 `validate_expressions` 通过，
但仿真阶段会让整批 6 条全部失败**（harvest 返回 `error_count=6`、`"No alpha_id in sim response"`）：

- `directional_significant_value_1..4` / `significant_value_1..4` / `top_directional_significant_value_1..4`
- `directional_indicator_2`（描述 enhanced insider，cov 1）
- `avg_top_buy_shares` / `avg_top_sell_shares`

**两条硬规则**：

1. **加 `ts_backfill(字段,120)` 会额外触发失败**——已成功的 `88RxLYXl`/`xArpnW5m` 都是**直接取字段**，
   insider 事件字段不能 backfill。报错是整批泛化失败（`error_count=6`），不是单条。
2. **`validate_expressions` 只查字段存在性，不查类型/事件性** ⇒ 派发前必须用「已成功表达式 + 1 个新字段」
   的小批（2–3 条）隔离验证，否则一条坏字段烧掉整个 6 条批次。

### `insd1_tradesignificance`（交易显著性 1–3 分）——2026-11-09 实测 · **判死**

`insiders1` 上 1–3 分的离散显著性打分，曾被当作「比原始金额更干净的事件强度」。实测：

| 字段 | 骨架 | S | 2Y |
|---|---|---:|---:|
| `insd1_tradesignificance` | `group_rank(ts_zscore(vec_avg(...), 252), sector)` | **0.06** | −0.32 |
| `insd1_value` | `group_rank(ts_zscore(vec_sum(...), 126), sector)` | −0.21 | −0.53 |

⇒ **显著性打分与原始金额都是零信号**。加上此前已测的 insider 方向/净买「只在挂借券短腿时才有 S」，
`insiders` 族的真实结论是：**它自己不能当主腿**，任何纯 insider ATOM 都不成立。
（可用字段仍仅限已知那 3 个；`*_significant_value_*` / `directional_indicator_2` / `avg_top_*_shares` 不可用，会整批拒收。）

<!-- profiles:manual:end -->
