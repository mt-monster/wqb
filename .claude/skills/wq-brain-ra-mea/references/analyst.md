# MEA × analyst（组合分支）

> 回到 [MEA 区域流程](../SKILL.md) · [MEA profile（证据与历史）](../../wq-brain-ra-pipeline/references/regions/MEA.md) · 实时生效画像：`$WQ_PY -m wqb.profiles explain --region MEA --category analyst`

<!-- profiles:cell-panel:start -->
**状态**：archived（跟区域入场 frozen）　**分组**：Analyst　**类别卡**：analyst

**涉及数据集**：analyst、analyst7、fundamental72+analyst7

### 回测设置（进仿真的值）

| 设置 | 值 | 来源 |
|---|---|---|
| instrumentType | EQUITY | 区域 settings.json |
| region | MEA | 区域 settings.json |
| universe | TOP400 | 区域 settings.json |
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
| 76 | 13 | 49 | 16 | 1 | 5 |

主要数据集（回测数）：analyst7（68）、fundamental72+analyst7（8）

### S1 字段理解

- 分清 actual_*（已实现、事后）与 mean_estimate_* / flash（预测、前瞻）：IND analyst_consensus 前 16 条全灭的真因是用了 actual（DEC-77）
- VECTOR 先 vec_avg / vec_count 聚合；JPN 下 vec_* 外再套 ts_* 会报错
- 窗口（类别卡，均在白名单内）：monthly 22/66；quarterly 66/252

### S2 生成

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

- 资格判定：`$WQ_PY tools/mode_b_qualify.py evaluate --region MEA --sharpe <S> --fitness <F> --two-year-sharpe <2Y>`（喂全指标，旁路 A–E 才会生效）
- 提交链：`submit_verdict` 只否决；prod 与 self 双端点实测（`check_correlation(refresh=True)`）；用户明确确认后才 `workflow_submit_alpha(confirm_submit=True)`——见 `worldquant-submit-alpha`

### 判死记录（不要重试；「归属」= payload 绑定 / 由条目名推断 / 关键词推断）

| 条目 | 族 | 下次怎么办 / 说明 | 数据集 | 归属 |
|---|---|---|---|---|
| MEA-ANALYST-FND-FLAT-COMBO-DEAD | analyst7×fundamental72 平铺 .5/.5 两腿组合（修订广度/股息广度/EBI广度/eps_mea | 不再做 analyst×fnd 简单两腿平铺；动量×动量组合禁入（CW 结构性触发）；下一步必须引入事件时序代理腿（announcement_dt 新鲜度）或权重再平衡/平滑增强 | analyst | inferred | <!-- lint:const-ok 证据原文 -->

### 胜绩

| 条目 | 机制 | 设置与骨架 | 数据集 | 归属 |
|---|---|---|---|---|
| MEA-ANALYST-3BREADTH-FUSION-WIN | analyst breadth fusion | 三广度腿融合: rank(subtract(vec_avg(eps_up_4w),vec_avg(eps_down_4w)))*0.3 + rank(subtract(vec_avg(ni_raised_1w),vec_avg(ni_dow | analyst | inferred | <!-- lint:const-ok 证据原文 -->
| MEA-ANALYST-PT4W-LEG-WIN | analyst breadth fusion | pt4w腿=rank(subtract(analyst_price_target_raised_count_four_weeks,analyst_price_target_lowered_count_4_weeks))(MATRIX无需ve | analyst | inferred | <!-- lint:const-ok 证据原文 -->
| MEA-ANL7-PT-NET-BREADTH-DECORR | analyst7 PT raised-breadth + Net est breadth 双轴（零 revision 腿 | analyst_price_target_raised_count_four_weeks/analyst_price_target_count (MATRIX 裸用) + vec_avg(est_q_net_raisednum_4wks)/ | analyst7 | inferred | <!-- lint:const-ok 证据原文 -->
| MEA-ESTQ-MOMENTUM-OTHERLIAB-LEG | analyst7 est_q_*动量×fundamental6 other_liab去杠杆 | ⚠ 加权拼腿已被闸 5 禁止，只作历史证据：骨架: add(multiply(rank(ts_delta(vec_avg(est_q_<X>_mean),W)),0.6), multiply(rank(multiply(ts_zscore(vec_avg(fundamental_ot | analyst7 | inferred | <!-- lint:const-ok 证据原文 --> <!-- lint:counterexample -->
| MEA-ESTQ-SAL-MOMENTUM-DCL | analyst7 est_q_sal动量×fundamental6 dcl去杠杆 | ⚠ 加权拼腿已被闸 5 禁止，只作历史证据：add(multiply(rank(ts_delta(vec_avg(est_q_sal_mean),63)),0.6), multiply(rank(multiply(ts_zscore(vec_avg(debt_current_liab | analyst7 | inferred | <!-- lint:const-ok 证据原文 --> <!-- lint:counterexample -->
<!-- profiles:cell-panel:end -->

## 补充说明（手写）

<!-- profiles:manual:start -->
<!-- profiles:manual:end -->
