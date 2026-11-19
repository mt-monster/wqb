# USA × analyst（组合分支）

> 回到 [USA 区域流程](../SKILL.md) · [USA profile（证据与历史）](../../wq-brain-ra-pipeline/references/regions/USA.md) · 实时生效画像：`$WQ_PY -m wqb.profiles explain --region USA --category analyst`

<!-- profiles:cell-panel:start -->
**状态**：active（跟区域入场 active）　**分组**：Analyst　**类别卡**：analyst

**涉及数据集**：analyst44、analyst7、analyst_consensus

### 回测设置（进仿真的值）

| 设置 | 值 | 来源 |
|---|---|---|
| instrumentType | EQUITY | 区域 settings.json |
| region | USA | 区域 settings.json |
| universe | TOP3000 | 区域 settings.json |
| delay | 1 | 区域 settings.json |
| truncation | 0.08 | 区域 settings.json |
| maxTrade | OFF | 区域 settings.json |
| pasteurization | ON | 区域 settings.json |
| unitHandling | VERIFY | 区域 settings.json |
| nanHandling | ON | 区域 settings.json |
| language | FASTEXPR | 区域 settings.json |
| visualization | false | 区域 settings.json |
| startDate | 2013-01-01 | 区域 settings.json |
| endDate | 2023-12-31 | 区域 settings.json |
| neutralization | REVERSION_AND_MOMENTUM | **本组合覆盖**（区域值 SUBINDUSTRY；证据：campaign_20261017/20261018 实测：SECTOR 族 prod 0.703-0.720 全撞墙，RAM 降到 0.648-0.698 且 SUB 升到 0.83-0.89；gJWoaJqv（RAM/market/504/d20）已 ACTIVE、S1.74/F1.27/2Y2.21/prod0.6978。仅 analyst44 实证；analyst7 全机制判死、analyst_consensus 已点亮） |
| decay | 20 | **本组合覆盖**（区域值 5；证据：同上：d10 档 S 最高（npAONOVa S1.81/F1.25/2Y1.82 但 prod 漂移 0.7088 撞线），d20 档唯一实证交付（gJWoaJqv ACTIVE）；d15/d20 修 SUB（0.67->0.74/0.82）） |

### 阈值

- Mode B 主闸 sharpe / fitness：1.25 / 0.8（default；下限锁生效，实时值看 explain）
- 其余阈值跟区域 thresholds.json（本组合无覆盖）

### 证据（2026-10-04 只读汇总）

| 回测 | RA 全过 | prod 已测 | 其中低于上限 | 判死 | 胜绩 |
|---|---|---|---|---|---|
| 19 | 0 | 1 | 0 | 2 | 0 |

主要数据集（回测数）：analyst44（8）、analyst7（8）、analyst_consensus（3）

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

- 资格判定：`$WQ_PY tools/mode_b_qualify.py evaluate --region USA --sharpe <S> --fitness <F> --two-year-sharpe <2Y>`（喂全指标，旁路 A–E 才会生效）
- 提交链：`submit_verdict` 只否决；prod 与 self 双端点实测（`check_correlation(refresh=True)`）；用户明确确认后才 `workflow_submit_alpha(confirm_submit=True)`——见 `worldquant-submit-alpha`

### 判死记录（不要重试；「归属」= payload 绑定 / 由条目名推断 / 关键词推断）

| 条目 | 族 | 下次怎么办 / 说明 | 数据集 | 归属 |
|---|---|---|---|---|
| USA-ANALYST-CONSENSUS-FXSPREAD-PROD-SAT | analyst_consensus_estimate |  | analyst_consensus | payload | <!-- lint:const-ok 证据原文 -->
| USA-ANALYST44-BREADTH-DEAD-EP-PRODWALL | analyst44 BEst revision breadth / dispersion / forward E-P z | USA analyst tower: neither revision breadth nor estimate-yield momentum is viable; only a mechanism orthogonal to value/ | analyst44 | payload | <!-- lint:const-ok 证据原文 -->
<!-- profiles:cell-panel:end -->

## 补充说明（手写）

<!-- profiles:manual:start -->
<!-- profiles:manual:end -->

---

## ★★★★★ 数据集清单更正（2026-10-18 实测，此前只列 3 个是错的）

USA/Analyst 类别实际有 **24 个 analyst* 数据集**（`field_profile_usa` 全量盘点）：

| 数据集 | 字段数 | 均覆盖 | 塔 | 高价值机制 |
|---|---:|---:|---|---|
| analyst_consensus | 3424 | 0.773 | ANALYST 1.2 | 4wk/3m 前值配对 → 修正率；actual vs 4wk 前值 → **惊喜**（S 1.79–1.86，但 prod 0.848） |
| analyst15 | 2567 | 0.994 | ANALYST 1.2 | **组级广播**（GICS 聚合），5 指标×3 分组×5 期限×3 窗 → 行业轮动（截面无效，S 0.33） |
| analyst10 | 2258 | 0.807 | — | `anl10_*ff_*` 财测 + `actual_update_flag_*`（未展开） |
| analyst4 | 1324 | 0.726 | — | 估值 + actuals（未展开） |
| analyst7 | 1317 | 0.500 | — | 判死（滞后窗口配对过平滑） |
| analyst_revision_horizons | 1095 | 0.941 | **MODEL 1.3** | 7d/30d/90d 修正 + SmartEstimate 预测惊喜（2Y 强、SUB 弱） |
| **analyst_factor_signals** | 922 | 0.660 | ANALYST 1.2 | **修正幅度/偏度/变异系数/趋势斜率/惊喜标准差等 10+ 机制**（S 最高 1.94，prod 0.807） |
| analyst14 | 868 | 0.500 | — | 未展开 |
| analyst69 | 646 | 0.934 | — | BEst 共识族 |
| analyst82 | 488 | 0.737 | — | `delta_*_predict/madp` 预测值网格（4 指标×4 季） |
| analyst11 | 445 | 0.530 | — | ESG/可持续性评分（S 0.62） |
| analyst_chart_cnn | 367 | 0.936 | MODEL | IBES 图表 CNN 特征（embedding，撞 LOW_TURNOVER） |
| analyst49 | 324 | 0.517 | — | 估值指标（股息率/PE） |
| analyst16 | 162 | 0.760 | — | StarMine 评级 1–5（S 0.82、TO 0.271） |
| analyst_earnings_ibes | 42 | 0.999 | MODEL | 事件窗收益（5 日 total return，S 0.70） |
| analyst57/35/48/94/8/base_ref/45 | 28–181 | 0.26–0.86 | — | 未展开 |

### ★★★ 本轮硬结论：Analyst 类别的 prod 地板 ≈0.80

- 12 批 / 43 条回测：**5 条 IS 八闸全过，0 条过 prod**（prod 0.8068–0.8673）。
- 换中性化（RAM↔CROWDING）、换窗（126/252/504）、换轴（industry/sector/subindustry/market）、
  换指标冷门度（EPS→NAV/利息费用/折旧摊销）——**prod 只在 0.807–0.867 内浮动**。
- **CROWDING 对 analyst_consensus 是 IS 增益器**（TO 0.053→0.012、margin 20→128bp、S 1.79→1.86、SUB 0.90→1.14），
  但 prod 不降 —— 与 analyst44 背离族（CROWDING 降 prod 到 0.669）方向相反。
- **SUB 是字段特异，不可按轴外推**：同 subindustry 轴下，`eps_revision_magnitude` SUB 1.09，
  而变异系数/幅度背离/NAV 只有 0.36–0.73。
- 结论：**新 ATOM 应转向未点亮塔或换区域**（IND analyst=2 / GBR analyst=3 / DEU analyst=1）。
