# insiders4（Edgar forms data）字段画像 · 模板 · 回测设计（USA / D1）

> 快照：2026-10-20，`get_datasets(category="insiders", USA, D1, TOP3000)` + `get_datafields(dataset_id="insiders4")`。
> 数据集：`insiders4`「Edgar forms data」，category = insiders（**未点亮**；本季 USA/D1 亮塔 = model 4 / analyst 5 / earnings 1）。
> 覆盖 0.6374，字段 16，userCount 409，alphaCount 1451，valueScore 2，pyramidMultiplier 1.1。
> ATOM 约束：本档案所有非豁免字段均来自 `insiders4`；`industry` / `subindustry` 分组属 6 个豁免分组字段。

## 1. 字段全景（16 字段）

| # | 字段 | 类型 | 覆盖 | userCount | aC | 语义 | 可用性 |
|---:|---|---|---:|---:|---:|---|---|
| 1 | `insd4_frequency_reportlen` | VECTOR | 0.8325 | 134 | 322 | 8-K 报告长度 | **主候选**：披露强度 / 事件密度 |
| 2 | `insd4_location_reportlen` | VECTOR | 0.8325 | 180 | 582 | 8-K 报告长度（第二解析变体） | **主候选**：与 #1 互为对照 / 组成比例 |
| 3 | `insd4_total` | VECTOR | 0.569 | 59 | 85 | 总薪酬 | 薪酬结构分母 / 水平 |
| 4 | `insd4_salary` | VECTOR | 0.569 | 55 | 86 | 基本工资 | 固定薪酬占比（守成） |
| 5 | `insd4_bonus` | VECTOR | 0.569 | 82 | 135 | 奖金 | 短期激励占比 |
| 6 | `insd4_stock_awards` | VECTOR | 0.569 | 30 | 44 | 股票奖励 | 权益薪酬占比（对齐） |
| 7 | `insd4_option_awards` | VECTOR | 0.569 | 43 | 52 | 期权奖励 | 权益薪酬占比（凸性） |
| 8 | `insd4_nonequity_plan` | VECTOR | 0.569 | 22 | 24 | 非权益激励计划 | 与 bonus 同族，优先级低 |
| 9 | `insd4_other` | VECTOR | 0.569 | 38 | 77 | 其他薪酬 | 结构残差，不作主信号 |
| 10 | `insd4_quarter_value` | VECTOR | 0.4355 | 75 | 152 | 季度数值信息 | **语义不明**（描述宽泛）⇒ 不作主信号 |
| 11 | `quarter_section_value` | VECTOR | 0.4395 | 1 | 1 | 季报章节数值 | 语义不明 + 近零使用 ⇒ 弃用 |
| 12 | `insd4_year` | VECTOR | 0.569 | 42 | 60 | 报告年份 | 元数据，不作信号 |
| 13 | `executive_position_label` | VECTOR | 0.6093 | 0 | 0 | 高管职位标签（字符串） | 非数值，FASTEXPR 不可直接用 ⇒ 弃用 |
| 14 | `executive_department_label` | VECTOR | 1.0 | 1 | 1 | 部门标签（字符串） | 同上 ⇒ 弃用 |
| 15 | `board_membership_indicator` | MATRIX | 1.0 | 2 | 2 | 是否董事会成员标志 | 近常数，aC=2 ⇒ **不作信号**（可作样本约束） |
| 16 | `insd4_*` 之外的 1 条经 sharpe 过滤被移除 | — | — | — | — | `sharpe_filter_removed=1` | 平台缺省过滤，不影响本设计 |

**字段家族（设计用）**：

| 家族 | 字段 | 覆盖档 | 更新形态 | 信号角色 |
|---|---|---|---|---|
| 披露强度 | `frequency_reportlen` / `location_reportlen` | 0.8325 | 事件驱动（8-K 提交时） | 主信号 |
| 权益对齐 | `stock_awards` / `option_awards` / `total` | 0.569 | 年度（薪酬表） | 主信号 |
| 固定薪酬 | `salary` / `nonequity_plan` | 0.569 | 年度 | 对照 |
| 短期激励 | `bonus` / `other` | 0.569 | 年度 | 对照 |
| 元数据 / 非数值 | `year` / `quarter_value` / 两个 label / `board_membership_indicator` / `quarter_section_value` | — | — | 不作信号 |

## 2. 数据结构与可用性判读

- **VECTOR 必须先聚合**：全部薪酬与报告长度字段都是 VECTOR（一家公司同日多条记录 / 多名高管）。
  标量算子只能接 `vec_*` 结果。本档案用 `vec_sum`（总量：薪酬总额、当日披露总长度）与
  `vec_avg`（典型值：单条记录长度）两种；`vec_stddev` 用于高管间薪酬离散度。**禁止把 VECTOR 直接塞进 `ts_rank`**。
- **覆盖两档**：报告长度 0.8325（可裸用 + `ts_backfill(252)`）；薪酬 0.569（**必须 backfill**，
  否则持仓只落在有薪酬披露的 57% 股票上，易触发 `CONCENTRATED_WEIGHT`）。
- **更新频率（推断，待 TO 实测检验）**：8-K 长度 = 事件驱动（可能日内多次）；薪酬 = 年度。
  ⇒ 报告长度用 Δ/秩变换捕捉"披露意外"；薪酬只在年度尺度有意义，窗口取 252/504。
- **语义坑**：两个 `reportlen` 的 description 完全相同，无法从元数据区分解析段；先按"同一机制的两个测量变体"
  处理，实测若相关性接近 1 则只保留 aC 更高的 `location_reportlen`。`quarter_value` 语义不明，
  不猜其经济含义（明确弃用，避免"先射箭再画靶"）。
- **零值含义**：无薪酬记录 → 向量为空 → `vec_sum` 缺省 0（nanHandling ON 下由平台处理），
  与"薪酬为零"不可区分 ⇒ 薪酬族的低覆盖本身是样本选择，解读时须与报告长度族互证。

## 3. 机制假设与文献

| # | 机制 | 字段 | 方向先验 | 经济逻辑 / 文献 |
|---:|---|---|---|---|
| H1 | 披露复杂度（长报告 = 信息难消化） | `reportlen` 水平秩 | 负 | 报告越长越难读，信息不对称与不确定性上升（Loughran & McDonald 2014；Li 2008 年报可读性与盈余持续性） |
| H2 | 披露脉冲（Δ 长度 = 事件密度突变） | `Δ reportlen` | 负 | 8-K 数量/长度骤增常对应治理事件（并购、离职、诉讼）；事件期风险溢价为负（论坛 2026-09-23 帖：解雇=风险） |
| H3 | 权益薪酬对齐 | `(stock+option)/total` | 正 | 权益薪酬提高 pay-for-performance 敏感度，降低代理成本（Jensen & Meckling 1976；Core & Guay 1999） |
| H4 | 固定薪酬守成 | `salary/total` | 负 | 固定薪酬占比高 = 激励不足 / 管理层权力（Murphy 1999；Bebchuk & Fried 2004） |
| H5 | 薪酬总量增长（租金提取） | `Δ total` | 负 | 薪酬增速超过自身历史 = 提取租金，后续回报偏弱（管理权力假说） |
| H6 | 高管薪酬离散度 | `std(total)/avg(total)` | 负 | 薪酬差距过大损害合作与生产率（pay dispersion 文献，结论混合，作对照） |
| H7 | 披露结构（两长度之比） | `location/frequency` | 待定 | 两个解析变体的相对占比 = 报告构成差异；无强先验，仅作 H1 的稳健性对照 |

**与 board_gov_stats 的正交性**：board_gov 测「人事结构/离任率」；本集测「披露强度 + 薪酬结构」，
即便同属 insiders 塔，信号源不同（8-K 文本长度 vs 董事会比率；薪酬 vs 离任）⇒ 不构成近重复。
仍须在过闸后实测 self-corr。

## 4. 适用模板与批量设计（D1–D8）

设置：EQUITY / USA / TOP3000 / D1 / SUBINDUSTRY / decay 5 / truncation 0.08 / maxTrade OFF /
pasteurization ON / unitHandling VERIFY / nanHandling ON / FASTEXPR；区间 2014-01-01 → 2023-12-31。
通用壳：`quantile(group_rank(hump(ts_backfill(winsorize(<SIG>, std=4), 252), hump=0.01), industry))`。

| # | 机制 | SIG（壳内核心） | 目的 |
|---:|---|---|---|
| D1 | H1 披露复杂度 | `-1 * ts_rank(vec_avg(insd4_frequency_reportlen), 504)` | 长报告负向，慢变量秩 |
| D2 | H2 披露脉冲 | `-1 * ts_av_diff(vec_avg(insd4_frequency_reportlen), 252)` | 长度突变负向 |
| D3 | H1 变体 | `-1 * ts_rank(vec_sum(insd4_location_reportlen), 504)` | 总量口径（aC 更高的变体） |
| D4 | H7 披露结构 | `ts_rank(vec_avg(insd4_location_reportlen) / (vec_avg(insd4_frequency_reportlen) + 1), 504)` | 两变体比例，方向待实测 |
| D5 | H3 权益对齐 | `ts_rank((vec_sum(insd4_stock_awards) + vec_sum(insd4_option_awards)) / (vec_sum(insd4_total) + 1), 504)` | 权益占比正向 | <!-- lint:counterexample: 权益授予占比分子（同族授予项相加） -->
| D6 | H4 固定薪酬 | `-1 * ts_rank(vec_sum(insd4_salary) / (vec_sum(insd4_total) + 1), 504)` | 工资占比负向 |
| D7 | H5 薪酬增长 | `-1 * ts_av_diff(vec_sum(insd4_total), 252)` | 总薪酬同比负向 |
| D8 | H6 薪酬离散 | `-1 * ts_rank(vec_stddev(insd4_total) / (vec_avg(insd4_total) + 1), 504)` | 高管间差距负向 |

**正交性**：D1/D3 同族不同解析变体（一 avg 一 sum）、D2 变化、D4 结构比、D5/D6 权益 vs 固定两端、
D7 总量变化、D8 离散度 —— 八个测量面互不重复；同族字段不并列相加（禁混信号）。

**预注册判据（写死）**：

- 任一 S≥1.58 / F≥1.0 / 2Y≥1.58 / SUB≥limit 且 fail=0 ⇒ 立即 `check_correlation(refresh=True)`（prod/self <0.7）。 <!-- from config.prod_corr_max -->
- **D1/D3 先看相关性**：若两条 S 都 <0.7 且彼此同号，说明报告长度族整体无信息 ⇒ 本集只剩薪酬族，
  后续只沿 D5/D6 扩批一次，不再磨长度窗。
- 若 8 条中薪酬族（D5–D8）全部 |S|<1.0 而长度族至少 1 条 ≥1.0 ⇒ 判「本集信息在披露侧」，
  只沿披露族补测量批（Δ/秩/比例），不换数据集。
- 任一 TO<1% ⇒ 先查是否整批低（薪酬年度变量 → 静态）；若是，对该条改 `ts_delta` / 事件门控，
  不跑全局去壳诊断。
- 全部 S<1.0 ⇒ 判本集弱并封存，第 10 颗改从剩余未点亮塔（sentiment22/23、other553）选，
  按 8 探针先验批处理，不直接扩批。

## 5. 回测结果及指标

### 5.1 批 1（已收 2026-10-20）

multisim `vWqIS4iA4veb4m1HSW66zg`，8/8 COMPLETE、0 error。设置：EQUITY / USA / TOP3000 / D1 /
SUBINDUSTRY（中性化）/ decay 5 / trunc 0.08 / nanHandling ON / VERIFY / pasteurization ON /
maxTrade OFF / FASTEXPR，区间 2014-01-01 → 2023-12-31。通用壳见 §4。

| # | 机制 | alpha | S | F | 2Y | SUB（limit） | TO | 收益 | risk-neut | 判读 |
|---:|---|---|---:|---:|---:|---|---:|---:|---:|---|
| D1 | 8-K 报告长度（频率侧，负向） | `58jkM9n6` | 0.45 | 0.16 | −0.12 | 0.27 (0.11) | 1.09% | 1.67% | 0.02 | 全期无 alpha |
| D2 | 报告长度 Δ252（负向） | `2rjNJR85` | 0.30 | 0.09 | −0.14 | −0.01 (0.13) | 1.11% | 1.12% | −0.21 | 变化方向无信息 |
| D3 | 8-K 报告长度（位置侧，负向） | `vROvd9wb` | 0.42 | 0.15 | 0.02 | 0.31 (0.10) | 1.09% | 1.53% | −0.21 | 与 D1 同弱 |
| D4 | 两长度比 | `QPY9EjMM` | 0.41 | 0.15 | 0.44 | 0.20 (0.13) | 1.08% | 1.61% | −0.59 | 结构比无信息 |
| D5 | 权益薪酬占比 | `A1Q7kbWW` | 0.57 | 0.21 | **1.00** | 0.10 (0.25) | **0.73% fail** | 1.73% | −0.39 | 2Y 为正但全期弱、TO 挂 |
| D6 | 工资占比（负向） | `1YjzJL9m` | 0.75 | 0.37 | **1.27** | **0.31 (0.32)** | **0.87% fail** | 3.05% | 0.03 | 本批最好之一，差 SUB 0.01 + TO |
| D7 | 薪酬总量 Δ252（负向） | `YPxgQmrl` | **0.80** | 0.39 | **1.45** | 0.23 (0.35) | **0.83% fail** | 2.98% | 0.18 | 本批最高 S，2Y 逼近 1.58，仍差 0.78 |
| D8 | 薪酬离散度（负向） | `zqrROj6K` | 0.58 | 0.22 | 1.15 | 0.18 (0.17) | **0.83% fail** | 1.85% | −0.26 | 离散度无信息 |

**归因（写死，本集在此封存）**：

1. **全批 S<1.0（max 0.80）⇒ 命中预注册止损**，判本集弱并封存；不再扩批、不再换测量面。
   发布时即为「第 9/10 颗主路径」，未产出可提交候选。
2. **披露侧（D1–D4）完全无信息**：S 0.30–0.45、risk-neut ≤0.02（D3/D4 为负），
   且 D1/D3 同族两解析变体同弱 ⇒ 8-K 报告长度在 USA/D1 已被定价或本字段解析不代表披露复杂度。
3. **薪酬侧（D5–D8）是「近年信号」而非全期 alpha**：D6/D7 的 2Y 1.27/1.45 明显高于全期 S 0.75/0.80，
   但 SUB 落后 0.01–0.12、TO<1%（0.73–0.87%）**结构性踩 LOW_TURNOVER**。
   ⇒ 年度薪酬变量在日频 D1 下天然静态；壳层（hump/quantile）已把换手压到地板，
   `ts_rank 504` 再压一档。即使把 TO 抬过 1%，S 仍差 0.78，**不是一闸之差**。
4. **risk-neut 不支撑「近年信号」**：D6 0.03、D7 0.18 ⇒ 2Y 的抬升不是干净 alpha，
   与 sentiment26 的「risk-neut 高恰好 2Y 负」相反形态、同样指向风格/短窗噪音。
5. **VECTOR 聚合无独立信息**：D1（vec_avg）与 D3（vec_sum）同弱；
   D6（工资占比）与 D7（总量 Δ）方向相反却同为 2Y 正、S<1.0 ⇒ 是「薪酬水平/增长」这一共同慢因子，
   不是两个独立机制。
6. **复用结论（入 playbook）**：年报级慢变量（薪酬/治理结构）在 USA/D1 想拿全期 S≥1.58，
   必须先解决 TO<1% 与 SUB 双墙；`ts_rank 504` 是已知最有效的 SUB 修复面，
   但它同时把 S 压低约 0.2–0.3 ⇒ 慢变量集应优先做**组合腿**而非单数据集 ATOM。

画像 → 本文件 §1–§5；交付日志 → [`_usa-atom-delivery-log-20261020.md`](_usa-atom-delivery-log-20261020.md)。

## 6. 风险与预判

- **覆盖率 0.569 的薪酬族是最大风险**：低覆盖 + 年度更新 ⇒ 可能同时低 TO 与低 SUB；
  若 D5–D8 出现成片 TO<1%，先判"低换手结构"再决定是否事件化，不提前判死。
- **报告长度可能已被挤占**：`location_reportlen` aC 582、`frequency_reportlen` 322，
  比薪酬族拥挤；若长度族信号弱于薪酬族，优先信薪酬族（拥挤度更低）。
- **VECTOR 空值污染**：`vec_sum` 对空向量返回 0，必须与报告长度族互证；薪酬为 0 的股票不应被当作"极低薪酬"做空。
- **风格 beta**：薪酬水平与规模高度相关；本批全部用"占自身总额的比例"或"自身时序秩"，
  不做裸薪酬水平截面；risk-neut <0.3 的构造成片出现即判本批为风格代理。
- **ATOM 合规**：全部字段来自 `insiders4`；`industry` 分组豁免。
