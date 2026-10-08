# DEU × sentiment（组合分支）

> 回到 [DEU 区域流程](../SKILL.md) · [DEU profile（证据与历史）](../../wq-brain-ra-pipeline/references/regions/DEU.md) · 实时生效画像：`$WQ_PY -m wqb.profiles explain --region DEU --category sentiment`

<!-- profiles:cell-panel:start -->
**状态**：probe（跟区域入场 probe-only）　**分组**：News-Sentiment　**类别卡**：sentiment

**涉及数据集**：sentiment27、sentiment7

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
| 39 | 12 | 0 | 0 | 0 | 0 |

主要数据集（回测数）：sentiment27（24）、sentiment7（15）

### S1 字段理解

- 关注度冲击常是反向信号（IND news_sentiment_transfer 1.64 反号）
- 窗口（类别卡，均在白名单内）：event 1/5/22

### S2 生成

- **类别通用原语**（类别卡，跨区）：
  - disagreement and intensity, not the raw score
  - change in sentiment after backfill, not the snapshot
  - sentiment divergence: retail vs institutional sentiment gap
  - sentiment persistence: autocorrelation of sentiment changes
- **跨区结论**（USA/EUR/IND/KOR/AMR/GLB；negative）：新闻 / 情绪作主信号在多区同型全灭（robust 墙、CW 或换手墙）（证据：AMR profile 跨区负先验；KOR 新闻情绪四连死（news38/50/54/79）；IND sentiment21 robust 0.24；GLB-NEWS23-MNA-EVENT-DEAD、GLB news73 sentiment 判死） <!-- lint:const-ok 证据原文 -->
- **跨区结论**（GLB/KOR/HKG/AMR；negative）：emotion 系（含 sentiment / mood 命名的变体）跨区死路（证据：GLB 铁律（registry cross_region 层）；KOR / HKG / AMR profile 排除） <!-- lint:const-ok 证据原文 -->
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
<!-- profiles:cell-panel:end -->

## 补充说明（手写）

<!-- profiles:manual:start -->
### 字段画像结论（2026-10-08）

`UNUSABLE` 255｜`UNTESTED` 21（共 276）—— **未测**

可用面仅 `sentiment27` 的 18 个（`snl27_*`：`relpopularity` / `top50pctranking` / `avgranking`，**全 VECTOR** ⇒ 须 `vec_*`）。
机制 = **零售关注度 / 人气排名**（attention-driven buying）。**开批前先查同族换手**。
<!-- profiles:manual:end -->
