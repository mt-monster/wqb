# 挖掘流程复盘与优化方案

**日期**：2026-09-08　**范围**：`wq-brain-ra-pipeline` 九步 SOP + `brain-makeSomeGem` GEM 引擎 + `wq-brain-campaign-toolkit` 门禁链路
**证据基础**：本会话约 170 次新回测（USA/IND/KOR/HKG）+ 7608 条历史 IS alpha 的过闸对照样本

---

## 一、挖掘过程复盘

### 1.1 前半段：新挖，产出 0

| 区域 | 波次 | 机制 | 结果 |
|---|---|---|---|
| USA | w34–37 | multifactor_return_pred 多因子分位数混合 | IS 强（fitness 1.11），prod 锁死 0.77–0.80，三种结构变体均失败 |
| IND | w136–138 | pv103 + pv47 交易成本/流动性 | 三度证伪，稳健死墙 |
| KOR | w173–181 | eps 修正 × 价差；pv106 成本离散 | `E5vql38G` 九闸全过但 prod 0.7231；pv106 覆盖仅 129/600 |
| HKG | w1–4 | fund_holdings_panel；shortinterest2/3 | w3 得 `O0roWEM7` sharpe 1.17 / risk_neutralized 0.96；w4 借贷利率族 7/7 全灭 |

**约 170 次回测，可提交 RA = 0。**

其中 HKG w3→w4 是一次干净的受控实验：同数据集族、同分组轴（`hk_equity_pca_method4_group20`）、同设置，唯一变量是字段拥挤度。低拥挤字段（uc 0–12）的 `risk_neutralized_sharpe` 分布为 0.79 / 0.11 / −0.33 / −0.41 / −0.50 / −0.57 —— **六个负值说明其方向性全部来自风险因子暴露，不是 alpha**。"冷门 = 未被挖"与"冷门 = 无效"，在该族里是后者。

### 1.2 后半段：转向库存筛选，产出 20

| 步骤 | 手段 | 结果 |
|---|---|---|
| 枚举 | 按 `settings.region` 分区，每区 `order=-is.fitness` 翻前 1000 条 | 扫 7608 条 REGULAR/IS |
| 资格门 | 本地复算 `failed_ra_count == 0`（规则对齐 `mcp_core.py::_slim_checks`） | 859 条（11.3%） |
| 去参数网格 | 按 (region, delay, 字段集合) 归并 | **859 → 277 条独立信号** |
| 自相关预筛 | 与 21 条 OS alpha 本地互相关，>0.7 剔除 | 110 中剔除 45 |
| 篮内正交 | 贪心选两两 <0.7，优先未点亮金字塔 | 20 条，篮内最大 0.6547 |
| 平台复核 | 逐条 `GET /alphas/{id}` 查 `is.checks` 无 `result==FAIL` | 拦下 3 条，补齐至 20 |

**产出**：20 条合格 RA，覆盖 20 个互不相同的金字塔、7 个区域，中位数 sharpe 2.42 / fitness 1.70 / 2Y 2.29。

### 1.3 各区过闸率（fitness 前 1000 条中 `failed_ra_count==0` 的比例）

| region | 过闸率 | region | 过闸率 |
|---|---|---|---|
| GLB | 23.5% | KOR | 9.9% |
| IND | 19.4% | GBR | 5.3% |
| EUR | 13.4% | CHN | 2.8% |
| USA | 11.6% | ASI | 1.8% |
| | | HKG | 0.3% |

去重压缩比：GLB 9.0× / CHN 9.0× / GBR 4.4× / EUR 3.2× / IND 2.6× / KOR 2.2× / ASI 2.0× / USA 1.8×。
**名义库存被参数网格严重虚高**——GBR 53 条候选去重后只剩 12 条独立想法。

---

## 二、现行链路的实际结构

```
步4 (S2)  workflow_gem
            └─ resolve_skill_dir("brain-makeSomeGem") → ~/.claude/skills/brain-makeSomeGem
                 └─ scripts/headless_runner/run.py         ← 从 DB 读 priors_snapshot_<region>
                      └─ scripts/trailSomeAlphas/run_pipeline.py  (2617 行)
                           ├─ economic_priors.py::concept_first_rules()   ← 概念优先规则
                           ├─ economic_priors.py::compact_priors_text()   ← wins/dead_ends/矩阵
                           └─ build_prompt()  → Moonshot → ideas.md → implement_idea.py
                                                              → final_expressions.json → DB

步5 (S2→S3) check_batch (src/wqb/expression/validator.py)
            check_expr_against_inspect  (体检硬门)
            wave_gate  (tools/wave_gate.py，含闸6 算子类别覆盖)
```

**注**：`world-quant-brain-mcp/.venv/.../cnhkmcp/untracked/skills/brain-makeSomeGem/` 下有一份 **1443 行的陈旧拷贝**，无 `economic_priors.py`、`run_pipeline.py` 不接受 `--priors-file`。它不在 `_skill_roots()` 的解析路径上（实测解析到 `~/.claude/skills`），但存在即是隐患——若 `WQ_SKILLS_DIR` 被误设或 `.claude/skills` 缺失，管道会静默退化成无 priors 运行。

### GEM prompt 的实际内容（`economic_priors.py`）

**做得好的部分**：

- `CATEGORY_PRIMITIVES` 按数据集类别给出真正的经济学原语，而非算子套壳：
  - analyst：修正惊喜（变化非水平）、分歧度（离散非均值）、广度 vs 幅度、FY2−FY1 期限缺口
  - fundamental：应计/现金缺口（盈余质量非盈余水平）、杠杆变化、效率而非资产存量
  - news：一手 vs 二手分歧、强度加权语调、语调修正、偏度/极化
  - institutions：持有人变化 vs 存量、集中度 vs 广度
- `concept_first_rules` 要求每个概念按序回答：机制 → 为何能预测下期收益 → 具体字段 id → 方向 → 失效模式 → Expected Exposure → 换手带 → 覆盖带
- 明令禁止 `rank({field})` 单独成概念、禁止"每字段套算子"、禁止发明字段 id
- 注入 wins（照抄机制换腿）/ dead_ends（禁止族）/ skeleton×字段族有效性矩阵与正交提示

**这套设计是对的。问题不在概念优先本身，在它被三条硬性配额推离了高过闸率区。**

---

## 三、诊断

### D1 ★★★ 算子类别硬闸与过闸率负相关

**位置**：`Claude/skills/wq-brain-campaign-toolkit/scripts/_lib/operator_coverage.py:54`

```python
_CATEGORY_GATE_REQUIRED = {"Logical", "Group", "Vector"}
```

**执行点**：`tools/wave_gate.py:574` —— 缺任一类别即整波 FAIL（MATRIX 数据集在 `:544` 豁免 Vector，**不豁免 Logical**）。
**GEM 侧对应**：`concept_first_rules` 的 "At least 1 concept using Logical operators: if_else / trade_when"。

**证据（859 条过闸样本的算子出现率）**：

| 算子 | 出现率 | 类别 |
|---|---|---|
| `rank` | 67.5% | Cross Sectional |
| `ts_backfill` | 45.4% | Time Series |
| `ts_mean` | 40.4% | Time Series |
| `group_rank` | 32.0% | **Group ✅** |
| `vec_avg` | 12.6% | **Vector ✅** |
| `if_else` | **5.1%** | **Logical ⚠** |
| `trade_when` / `bucket` / `ts_corr` / `ts_kurtosis` | 未进前 22 | — |

`Group` 与 `Vector` 的强制是**无害的**（group_rank 32%、vec_avg 12.6% 本就常见）。
**只有 `Logical` 是有害强制项**：它在过闸者中出现率 5.1%，却是每波必过的硬闸。

本会话的直接后果：KOR w173 / IND w136 报 `[opcat] 缺 Logical 类别` FAIL → 被迫加 `trade_when` / `if_else` regime 门 → 加完 sharpe 塌陷。HKG w4 的 `QP3EWd6p`（`if_else` 切换）sharpe 0.00、`om6VPeZE`（`bucket` 分组）sharpe 0.05，且 `bucket` 还把 `pyramids.effective` 从 2 降到 1。

### D2 ★★★ GEM prompt 没有复杂度预算

**位置**：`economic_priors.py::concept_first_rules`

现行要求：≥8 个概念、其中 ≥3 个多字段、≥3 个不同 Expected Exposure、≥3 个算子类别、≥1 Logical、≥1 Group、≥1 高级 TS、单一外层包裹占比 ≤30%。

**证据**：过闸者算子数分位 **p10=2 / p25=3 / 中位数 5 / p75=8 / p90=12**，**46.4% 只有 ≤4 个算子**。
极端例证：CHN `1Ypvp1O6` = `ts_rank(mdl39_price_mo_short_term_component, 1000)` —— 一字段两算子，sharpe 2.14 / fitness 1.42 / 2Y 2.75 全闸过。

本会话提交的表达式基本落在 p90（12 算子）以上尾部，无一过闸。**结构复杂度不是通往过闸的路。** 每加一腿都在稀释主信号方向性，同时压低 `sub_universe_sharpe` 与 `2Y sharpe`——恰是本会话卡得最多的两个闸。

### D3 ★★ Expected Exposure 只问不验

GEM 要求每个概念声明 `Expected Exposure`（value/momentum/quality/…），但**全链路无任何回环验证**声明是否兑现。

`risk_neutralized_sharpe` 正是这个验证器：**若它 ≈ 0 或为负，说明这条 alpha 就是那个 exposure 本身，而不是 exposure 之上的超额。**

本会话证据：HKG w4 六条为负；w3 的 `O0roWEM7` risk_neutralized 0.96 ≈ raw sharpe 1.17，是约 150 次回测中唯一"真信号"特征。该指标从未进入任何闸或回写。

### D4 ★★ priors 的监督样本比可用样本小两个数量级

`wins` / `dead_ends` / `skeleton_field_matrix` 来自 campaign registry（`registry_empirical` 740 行、`wave_results` 427 行）。
而账户有 **≥3 万条已回测 alpha**（USA/EUR 各 ≥10000、GLB 5251、IND 5163、KOR 4205、ASI 2613、GBR 2489、CHN 318、HKG 290），其中已验证 7608 条里 859 条过闸——**一份现成的、大两个数量级的监督样本，从未被 GEM 消费。**

### D5 ★★ 本地资格门与平台判定不一致

- `mcp_core.py::_RA_CHECK_NAMES` **缺 `LOW_ROBUST_UNIVERSE_SHARPE.WITH_RATIO`**（该名只出现在 `_PPA_CHECK_NAMES`），但平台以 FAIL 拦 REGULAR 提交。实测 23 条候选里误判 3 条（ASI `YPvLNjnW` 2.43 vs 限 2.44，差 0.01）。
- `submit_verdict` 在 `submit_status:404` + `prepost_unverifiable:true` 时报**假 SUBMITTABLE**（本会话第二、三次复现：IND `qMja95Q2`、MEA `Jj7ee6nO`/`omqEE1pn`）。
- list 端点的 `is.checks` ≠ detail 端点的 `is.checks`——筛选必须以 detail 为准。

### D6 ★ 缺库存枚举能力

`/users/self/alphas` 两个硬限制此前无人记录：

- **`offset > 1000` 返回 HTTP 400 + list 体**（不是 dict）`["Cannot display more than the first 1,000 alphas…"]`，直接 `j.get()` 抛 `AttributeError`
- **`count` 封顶 10000**，USA/EUR 都显示 10000 并非真实总数

真正的服务端过滤只有 `settings.region` / `dateCreated>` / `dateCreated<` / `order` / `stage` / `hidden` / `type`。MCP 包装层里 `region` 与 `status` 是**客户端过滤**（`brain_mixin_simulation.py` 的 `api_params` 构造），写进 params 会被平台忽略。

`tools/sync_platform_alphas.py` 只存轻量字段（无 `checks` / `two_year_sharpe` / `neutralization`），不足以做资格门筛选。

### D7 ★ 陈旧引擎拷贝

venv 内 `cnhkmcp/untracked/skills/brain-makeSomeGem/` 是 1443 行的旧版，无 `economic_priors.py`、`run_pipeline.py` 不接受 `--priors-file`（strict `parse_args()`）。当前未被解析命中，但构成静默降级风险。

---

## 四、优化方案

### P0-1　把 Logical 从每波硬闸改为条件触发

**改 `_lib/operator_coverage.py:54`**：

```python
# Group / Vector 保留强制（过闸样本中 group_rank 32.0% / vec_avg 12.6%，本就常见）
_CATEGORY_GATE_REQUIRED = {"Group", "Vector"}
# Logical 改为条件要求：仅当数据集含事件型字段（有明确事件时间戳/计数字段）时要求
_CATEGORY_GATE_CONDITIONAL = {"Logical"}
```

**改 `tools/wave_gate.py` 闸6**：Logical 缺失时降为 WARNING，只在 `s1_<ds>` ledger 标记该数据集为事件型时才升为 FAIL。

**理由**：`if_else` 在过闸者中占 5.1%，`trade_when`/`bucket` 不入前 22。强制它等于强制每波至少一槽落在低过闸率结构区。事件型数据集（财报日、公告、内部人交易）用 `trade_when` 是对的；连续型面板（借贷利率、估值、模型分）用它只是噪声门。

### P0-2　GEM prompt 加入复杂度预算

**改 `economic_priors.py::concept_first_rules`**，在 `FORBIDDEN` 后新增：

```
COMPLEXITY BUDGET (empirical, from 859 gate-passing alphas):
- Operator-count distribution of alphas that PASS the IS hard gates:
  p10=2, p25=3, median=5, p75=8, p90=12. 46% of passers use <= 4 operators.
- DEFAULT to 2-5 operators. A single-field atom with one time-series
  transform and one cross-sectional wrapper is a first-class concept,
  not a placeholder.
- Every ADDITIONAL leg beyond the second must be justified by naming the
  SPECIFIC gate it fixes (sub_universe_sharpe / 2Y_sharpe / concentrated_weight).
  "More signal" is not a justification.
- Of the 8 concepts, at least 3 MUST be <= 4 operators.
- Adding legs dilutes directionality and depresses sub_universe_sharpe and
  2Y sharpe - the two gates that block most candidates.
```

同时把「≥3 个多字段」下调为「≥2 个多字段」，为原子概念让出配额。

### P0-3　多样性口径改按语义维度，不按算子类别

**改 `concept_first_rules` 的 OPERATOR CATEGORY COVERAGE 段**，替换为：

```
DIVERSITY (enforced on semantics, not on operator names):
- >= 3 distinct Expected Exposure values across the 8 concepts
- >= 3 distinct field families (different dataset prefixes or different
  economic quantities within one dataset)
- >= 2 distinct grouping axes when group_* is used (industry / subindustry /
  a pca_* cluster field / a bucket of a continuous auxiliary field)
- >= 2 distinct time-window scales (fast <= 22 vs slow >= 252)
Operator variety is a CONSEQUENCE of these, not a target in itself.
```

**理由**：算子多样性与信号多样性不是一回事。本会话 USA w35 触发 `GROUP-DOMINANCE 9/12 共享 字段族=alt2`——那是真的同质化，按字段族判定抓得准；而 `[opcat] 缺 Logical` 抓的是假问题。

### P1-1　用库存反哺 priors

新增 `tools/build_gate_prior_from_inventory.py`：

1. 按 `settings.region` 分区枚举（每区 `order=-is.fitness` 前 1000，需要全枚举时用 `dateCreated` 窗口递归二分至每窗 ≤1000）
2. 本地复算 `failed_ra_count`（含 `.WITH_RATIO`）
3. 按 (region × universe × neutralization × 骨架签名 × 字段族) 统计**条件过闸率**
4. 写入 `region_kb.gate_priors`，由 `assemble-priors` 并入 priors
5. `compact_priors_text` 新增一段：

```
Empirical gate-pass rates in this region (from N historical backtests):
- neutralization=STATISTICAL: X% pass | SUBINDUSTRY: Y% | SECTOR: Z%
- operator-count <=4: X% pass | 5-8: Y% | >8: Z%
- field family <foo>: X% pass (n=..)
Prefer the high-rate cells. These are measured, not guessed.
```

**理由**：把 740 行 registry 的先验换成 3 万条回测的先验，样本量提升两个数量级，且是同一账户、同一设置习惯下的分布，外推风险低。

### P1-2　把 `risk_neutralized_sharpe` 提为一等公民

1. **S3 收割时记录**：`backtest_results` 增列 `risk_neutralized_sharpe`
2. **S4 诊断硬规则**：`risk_neutralized_sharpe <= 0` 且 `sharpe >= 1.58` → 判定为"因子暴露伪装成 alpha"，标 `dead_end`，禁止继续调参
3. **S6 回写**：比对 GEM 声明的 `Expected Exposure` 与实测 `risk_neutralized_sharpe`，兑现的写 `template_kb.validated`，未兑现的写 `failed`，形成闭环
4. **GEM prompt 补一句**：

```
Your Expected Exposure claim WILL be verified post-backtest against
risk_neutralized_sharpe. If risk_neutralized_sharpe collapses to ~0 while
raw sharpe is high, the concept WAS the exposure, not alpha on top of it.
Design so that the signal survives removal of its own stated exposure.
```

### P1-3　修资格门与提交判定

1. `mcp_core.py::_RA_CHECK_NAMES` 补 `"LOW_ROBUST_UNIVERSE_SHARPE.WITH_RATIO"`
2. 篮子敲定前必须逐条 `GET /alphas/{id}`，以 detail 端点 `is.checks` 无 `result == FAIL` 为准
3. `submit_verdict` 在 `submit_status == 404 and prepost_unverifiable` 时，`verdict` 应返回 `UNVERIFIABLE` 而非 `SUBMITTABLE`

### P2-1　流程顺序：库存优先于新挖

在 `wq-brain-ra-pipeline` **步 1（S-PRE）** 增加一条开工前置：

```
库存盘点（每次新目标必做）：
  tools/build_gate_prior_from_inventory.py --regions all --emit-candidates
  → 得到 failed_ra_count==0 的候选池
  → compute_mutual_correlation 免费去同族冗余 + 剔除与 OS 池撞车者
  → 逐条 detail 复核
  只有当候选池不足以覆盖目标金字塔时，才进入步 2 开新挖。
```

**理由**：本会话前半段 170 次新回测产出 0，后半段一次库存扫描产出 20。**先清库存，再开新挖**是数量级差异的顺序问题。

### P2-2　清理陈旧拷贝

删除或重命名 `world-quant-brain-mcp/.venv/.../cnhkmcp/untracked/skills/brain-makeSomeGem/`，并在 `resolve_skill_dir` 命中非 `~/.claude/skills` 时打印显式 WARNING（现有 `_warn_if_legacy` 已有类似机制，需覆盖该路径）。

### P2-3　补 `tools/` 常驻库存扫描器

把本会话的一次性脚本固化：`screen_is_alphas.py`（分区枚举 + 资格门复算）、`select_basket.py`（OS 撞车预筛 + 互不相关子集 + 金字塔轮转）。二者已验证可用，产物为 20 条合格篮子。

---

## 五、经验配方（可直接用于下一波 GEM）

基于 859 条过闸样本：

| 维度 | 取值 |
|---|---|
| 算子数 | **2–5**（默认 3），超过 8 需明确说明修哪个闸 |
| 核心算子 | `rank`(67.5%) / `ts_backfill`(45.4%) / `ts_mean`(40.4%) / `group_rank`(32.0%) |
| 中性化 | **STATISTICAL**(25.3%) 或 SUBINDUSTRY(21.8%)；COUNTRY 适用于 GLB 类多国宇宙 |
| decay | **4**（35%），次选 6 / 5 |
| truncation | **0.08**（65%） |
| 换手目标带 | **0.10–0.12**（中位 0.1166），不要刻意压到 0.03–0.05 |
| 字段类型 | 优先 `mdl*` / `smest*` 等 MODEL 类单字段；MODEL 塔在过闸者中占比最高 |
| 区域优先级 | GLB(23.5%) > IND(19.4%) > EUR(13.4%) > USA(11.6%) > KOR(9.9%) ≫ GBR/CHN/ASI/HKG |
| 时间窗口 | 严守 1/5/22/66/252/504/1008/1260；1000≈1008 属可接受近似 |

**反例清单**（本会话实证无效）：三腿以上等权混合、`bucket` 自定义分组（还会丢金字塔归属）、`if_else` regime 切换、刻意低换手、低拥挤字段堆砌。
