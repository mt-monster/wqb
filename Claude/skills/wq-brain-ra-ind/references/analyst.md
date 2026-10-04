# IND × analyst（组合分支）

> 回到 [IND 区域流程](../SKILL.md) · [IND profile（证据与历史）](../../wq-brain-ra-pipeline/references/regions/IND.md) · 实时生效画像：`$WQ_PY -m wqb.profiles explain --region IND --category analyst`

<!-- profiles:cell-panel:start -->
**状态**：probe（跟区域入场 probe-only）　**分组**：Analyst　**类别卡**：analyst

**涉及数据集**：analyst、analyst39、analyst45、analyst_consensus

### 回测设置（进仿真的值）

| 设置 | 值 | 来源 |
|---|---|---|
| instrumentType | EQUITY | 区域 settings.json |
| region | IND | 区域 settings.json |
| universe | TOP500 | 区域 settings.json |
| delay | 1 | 区域 settings.json |
| neutralization | STATISTICAL | 区域 settings.json |
| decay | 4 | 区域 settings.json |
| truncation | 0.08 | 区域 settings.json |
| pasteurization | ON | 区域 settings.json |
| testPeriod | P0Y0M0D | 区域 settings.json |
| unitHandling | VERIFY | 区域 settings.json |
| nanHandling | OFF | 区域 settings.json |
| maxTrade | OFF | 区域 settings.json |
| language | FASTEXPR | 区域 settings.json |
| visualization | false | 区域 settings.json |

### 阈值

- Mode B 主闸 sharpe / fitness：1.5 / 1.0（thresholds_override:IND；下限锁生效，实时值看 explain）
- 其余阈值跟区域 thresholds.json（本组合无覆盖）

### 证据（2026-10-04 只读汇总）

| 回测 | RA 全过 | prod 已测 | 其中低于上限 | 判死 | 胜绩 |
|---|---|---|---|---|---|
| 114 | 7 | 18 | 10 | 5 | 3 |

主要数据集（回测数）：analyst_consensus（92）、analyst45（22）

### S1 字段理解

- 分清 actual_*（已实现、事后）与 mean_estimate_* / flash（预测、前瞻）：IND analyst_consensus 前 16 条全灭的真因是用了 actual（DEC-77）
- VECTOR 先 vec_avg / vec_count 聚合；JPN 下 vec_* 外再套 ts_* 会报错
- 窗口（类别卡，均在白名单内）：monthly 22/66；quarterly 66/252

### S2 生成

- **用**：robust 墙（平台对 IND 额外要求 robust universe Sharpe 不低于 1.0）的破法：用 pretax（税前利润一致预期）代替 EPS；水平偏离形；按市值十分位 group_rank；decay 7–10
- **避**：anl39 / qfl / anl9 族（判死或拥挤）
- **避**：actual_*（已实现）字段当预测用：analyst_consensus 前 16 条全灭的真因（DEC-77）
- **说明**：只有这个「偏离 1 年均值 / abs(均值)」函数形态 prod 低于上限；z-score / ts_rank 形态恒 0.73–0.75（撞 2 颗外部 prod alpha）
- **说明**：SECTOR 中性化提 S 但降 robust，robust 卡线时别用；该族在别的区都无效（／S／ ≤1.07）
- **已验证骨架**（证据见每行注释；照抄前先按本组合当前 prod 复核）：

  ```text
  group_rank(divide(subtract(P, ts_mean(P, 252)), add(abs(ts_mean(P, 252)), 1)), bucket(rank(cap), range="0,1,0.1"))
  ```

  - group_rank(divide(subtract(P, ts_mean(P, 252)), add(abs(ts_m… ← P = ts_backfill(vec_avg(mean_flash_estimate_pretax_annual12), 22)；zq8wZgQO / pwRJmvP3：S 1.60–1.67、robust 1.06–1.11、prod 0.65（IND profile / Claude 记忆 ra10）
- **类别通用原语**（类别卡，跨区）：
  - revision surprise: change in FY1/FY2 vs the stale level
  - dispersion: disagreement across estimates, not the consensus mean
  - breadth vs magnitude: how many estimates moved, not how far the mean moved
  - horizon gap: FY2 minus FY1 as a growth-expectation residual
  - rating momentum: upgrade/downgrade frequency vs historical baseline
  - target price gap: current price vs consensus target (upside/downside)
  - estimate acceleration: second derivative of estimate revisions
- **跨区结论**（USA/GLB/HKG/KOR/EUR/DEU/GBR；negative）：flash / pretax 一致预期动量族只在 IND 有效，别的区 ／S／ 都在 1.07 以下（证据：waves probe_flash_eps_20260919 / probe_pretax_20260919：USA ≤0.09、GLB ≤0.08、HKG 0.64、KOR ≤1.07、EUR ≤0.96、DEU ≤0.72、GBR ≤0.54） <!-- lint:const-ok 证据原文 -->
- **跨区结论**（KOR/USA/DEU；negative）：分析师主信号族普遍撞 prod 墙（证据：KOR analyst10/16/44/consensus（RULES §G）；USA-ANALYST44-BREADTH-DEAD-EP-PRODWALL（E/P z prod 0.93）；DEU analyst93 prod 饱和） <!-- lint:const-ok 证据原文 -->
- **禁止**（类别卡）：禁止使用裸 rank(estimate)（必须 ts_delta 或 group_zscore）
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

- 资格判定：`$WQ_PY tools/mode_b_qualify.py evaluate --region IND --sharpe <S> --fitness <F> --two-year-sharpe <2Y>`（喂全指标，旁路 A–E 才会生效）
- 提交链：`submit_verdict` 只否决；prod 与 self 双端点实测（`check_correlation(refresh=True)`）；用户明确确认后才 `workflow_submit_alpha(confirm_submit=True)`——见 `worldquant-submit-alpha`

### 判死记录（不要重试；「归属」= payload 绑定 / 由条目名推断 / 关键词推断）

| 条目 | 族 | 下次怎么办 / 说明 | 数据集 | 归属 |
|---|---|---|---|---|
| IND-ANALYST45-ROBUST-WALL | analyst45 net_market_exposure | IND analyst45 想法台账类单信号族 REGULAR 提交判死：robust 墙0.36-0.60为结构性，同族参数/包裹/分组/混合优化不再投入；analyst 族新集首探必须批1即含 robust 快判 | analyst45 | inferred | <!-- lint:const-ok 证据原文 -->
| IND-ANALYSTBASE-SUE-DEAD | analyst consensus surprise/stddev/coverage | skip analyst_base_ref consensus family; low-competition tier1 exhausted -> switch to STATISTICAL track or Mode B dilutio | analyst_consensus | inferred | <!-- lint:const-ok 证据原文 -->
| IND-ANL39-EPSCOL-DEAD | anl39 除非常项/单季 EPS 字段(xlcxspemtp/roxlcxspeq/roxlcxspea/ptmeps | IND anl39 该批字段不再投入回测配额 | analyst39 | inferred | <!-- lint:const-ok 证据原文 -->
| IND-ANL39-TTMQ-EPS-CORE-DEAD | anl39 TTM-Q EPS 差分核心(ttmepsincx/qepsinclxo)变体族 | IND anl39 表达式禁止再以 ttmepsincx-qepsinclxo 差分为核心; 若要 anl39 必须完全换核心字段或彻底重构结构 | analyst39 | inferred | <!-- lint:const-ok 证据原文 -->
| IND-REVMAG-ANALYST-SATURATED | eps_revision_magnitude analyst | 信号族饱和时组合无法绕开 prod 墙（分量同族暴露本质相同），换族比稀释更高效；同族不再展开 | analyst | inferred | <!-- lint:const-ok 证据原文 -->

### 胜绩

| 条目 | 机制 | 设置与骨架 | 数据集 | 归属 |
|---|---|---|---|---|
| IND-ANALYST-FUNDAMENTAL-MIX | 分析师修正+基本面混合信号（58l2or1N） | 0.6 分析师修正 + 0.4 基本面 earnings score，通过引入基本面信号降低 prod_corr（0.8094 → 0.6617），S=2.17, F=1.78, 2Y=2.53 | analyst | inferred | <!-- lint:const-ok 证据原文 -->
| IND-ANALYST-FUNDAMENTAL-WIN | Analyst revision + fundamental combination alpha in IND regi | analyst_revision_percentile_score_long_4 (60%) + fnd86_earnings_score (40%) with INDUSTRY neutralization, decay=4 | analyst | inferred | <!-- lint:const-ok 证据原文 -->
| IND-ANL39-ROBUST-BREAK-WIN | anl39 族破解 LOW_ROBUST_UNIVERSE_SHARPE 隐形墙 | scale(-rank(x)) 通过 robust 1.01; scale(reverse(rank(x))) 不过(0.90-0.94). IND 提交带 -rank 语法 | analyst39 | inferred | <!-- lint:const-ok 证据原文 -->
<!-- profiles:cell-panel:end -->

## 补充说明（手写）

<!-- profiles:manual:start -->
<!-- profiles:manual:end -->
