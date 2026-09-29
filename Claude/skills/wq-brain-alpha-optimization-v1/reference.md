# WQ BRAIN Alpha Optimization V1 — Mode A 参考

本页是 **Mode A（参数层）** 的操作规则：在不浪费模拟配额的前提下，对现有 alpha 做 8 候选严格批优化。Mode B（想法层）与入场判定见 [SKILL.md](SKILL.md) 与 [`references/mode-b-qualification.md`](references/mode-b-qualification.md)；arXiv 工具见 [arXiv_API_Tool_Manual.md](arXiv_API_Tool_Manual.md)。

## 1. 目标

按固定 8 表达式一批：生成 → 校验 → 回测 → 诊断 → 迭代，直到出现达标候选，或触发 SKILL「止损阶梯」。

## 2. 完成定义（Definition of Done）

候选「达标」需同时满足：

- 平台全部检查 PASS，`Failed RA == 0`（口径与 PENDING / WARNING 语义见 RA [`webdatascope-failed-gates.md`](../wq-brain-ra-pipeline/references/webdatascope-failed-gates.md)），其中含 `IS_LADDER_SHARPE`、Sub-universe、`CONCENTRATED_WEIGHT`；
- 内部闸线：`wqb.config.GATES_INTERNAL`（Sharpe / Fitness / Turnover / margin 等**数值以 config 为准，本页不复写**；平台线更宽，别互相顶替）；
- PROD 相关性读数（`check_correlation`，只读）按 RA 决策表 [D0-P](../wq-brain-ra-pipeline/references/decision-table.md) 可放行。**PROD ≥ 0.7 时候选不算 done**，即便其余全过。

## 3. 输入

必需：`baseline_alpha_id`；平台设置 `region` / `universe` / `delay` / `neutralization` / `language`；算子清单（`platform_constraints.json` 的 `known_ops`，或平台 `get_operators` 实测）。

可选：阶段提示（`Stage A` / `Stage B`）；已知失败史（`weight` / `sub-universe` / `correlation` / `unit` / `warning`）；本轮日志要写给谁（缺省 = 本轮回复 + S6 `key_findings`）。

## 4. 每轮的标准产物

出现在回复或笔记里的逻辑产物：

- `batch_plan`：8 条表达式、角色、主题对、粗略算子数
- `preflight_report`：算子存在性与签名核对
- `local_validation_report`：校验层三段的结果与精确修复记录
- `backtest_summary`：alpha id、关键指标、FAIL 项（**权威副本 = `backtest_results` 表**，见 §10 Step 7）
- `next_batch_actions`：下一轮要翻转 / 压缩 / 去噪 / 去相关什么

## 5. 工具

平台侧（MCP）：

- `mcp__wq-brain-http__get_platform_setting_options`
- `mcp__wq-brain-http__get_alpha_details`（含 `is.checks`）
- `mcp__wq-brain-http__create_multi_simulation`
- `mcp__wq-brain-http__harvest_multisim_alphas` → `mcp__wqb-db__harvest_multisim_results`（收割入库）
- `mcp__wq-brain-http__get_user_alphas`
- `mcp__wq-brain-http__lookINTO_SimError_message`（仿真报错 / 状态；参数 `locations` = multi 返回的 location 列表）

**本地校验入口**（回测前的硬闸，三段顺序执行；命令见 SKILL「Mode A 校验层」）：

1. 语法 / 算子元数：[expression verifier skill](../alpha-expression-verifier/SKILL.md)（`wave_gate.py` 内含，与闸 1 同源）；
2. 幽灵算子：`tools/campaign_intel.py ghost-audit`。`validate_expressions` / `preflight_expressions` **不查幽灵算子**（会对 `ts_median` 返回 valid=true）；
3. 闸 1–9 + SEM：`tools/wave_gate.py --batch-type repair`（修复批不做质量预估标注、默认豁免批级多样性；闸的处置见 RA [step5-gates.md](../wq-brain-ra-pipeline/references/step5-gates.md)）。

## 6. 全局约束

### 6.1 核心字段冻结

先读基线表达式并冻结其核心字段 / 数据集族。后续候选可以变换、去噪、中性化、组合、翻转这些字段，但不得把核心来源换成无关字段。

### 6.2 算子数与复杂度

- **PPA**：表达式算子数 ≤ 8（平台 Power Pool 规则；文档记载、本环境未向平台复核）。
- **REGULAR**：平台无算子数上限；复杂度纪律见 `brain-make-some-gem`「复杂度预算」（默认 2–5 个算子）与 `brain-alpha-robustness`（> 5 为软标记）。
- 本地估算只是回测前的粗闸：每种函数名计一次；直接写的 `+ - * /` 各计一次；字段、常量、括号不计；用了 `add` / `subtract` 函数式就别再重复计符号式。**平台返回的 `operatorCount` 是最终裁判。**

### 6.3 每轮 8 条

每轮恰好 8 个候选。若有候选因语法 / 签名 / 门禁被拦，必须在发批前改写，使整批仍是 8 条有效表达式。

### 6.4 命名参数强制

不要凭记忆写算子用法，先查算子清单。位置必需参数必须给；可选参数必须写成 `name=value`；裸的可选字面量无效。示例（均取自 `known_ops` 内的算子）：

- `winsorize(x, std=4)`
- `ts_returns(x, d, mode=1)`
- `hump(x, hump=0.01)`（`hump` 仍受支持，但必须命名参数；RA 决策表 D6）
- `bucket(rank(x), range="0,1,0.1")`

### 6.5 微调闸（Fine-Tune Gate）与 Stage A / B

纯参数微调只在当前最优候选**同时**满足下面两条时允许：

- Sharpe > 1.40
- Fitness > 0.90

不满足 → 本轮是 **Stage A**，8 条里 0 条可以是纯微调；满足 → **Stage B**（见 §7）。「Stage A / B」在本 skill 内只指这两个进入状态，与 toolkit 探针里的 Stage A / B 探针不是一回事。

### 6.6 强负信号保留

若候选 Sharpe ≤ -1.20、Fitness ≤ -0.50，且没有权重爆炸 / 单位失效等硬性淘汰失败，标 `CAND_NEG`。下一轮至少做 2 个翻转变体 `CAND_SHORTFLIP`，例如 `multiply(-1, expr)`。不要因为信号是负的就丢掉强负信号。

## 7. 阶段逻辑

### Stage A（微调闸未过）

允许的候选类型：

1. 基于字段行为的结构升级：去噪、冻结、正交化、换手控制、相关性重构；
2. 同数据集字段组合：最多 2 个紧密相关字段，且有清楚的互补理由；
3. 核心字段 + 价量语义，只要核心数据集仍冻结。

建议配额：结构升级 ≥ 3、同数据集组合 ≥ 3、价量语义组合 ≥ 2。**Stage A 禁止纯参数改动。**

### Stage B（微调闸已过）

- `#1` 至 `#5`：exploit 或受控微调；
- `#6` 至 `#8`：强制 explore。explore 槽各自至少含 2 个来自 §8 主题集的算子，且 3 条 explore 的主题对不得重复。

## 8. 主题配额

每轮 8 条必须覆盖 A–F 中**至少 4 个不同主题**。下表按平台 `get_operators` 实测清单（`platform_constraints.json` 的 `known_ops`）分栏：

- **已核验**：在 `known_ops` 内，可直接用；
- **未列入清单**：本页历史上把它们当主题算子，但当前**不在 `known_ops`**——用前必须先 `get_operators` 复核；未复核就用会在闸 1 被当作未知标识符处理（或回测 ERROR 并连坐整批）。

配额统计只按「已核验」栏计（6 个主题都有足够的已核验算子可选）。

| 主题 | 含义 | 已核验 | 未列入清单（用前 `get_operators` 复核） |
|---|---|---|---|
| A | 条件交易 / 冻结 | `trade_when`, `if_else` | `keep`, `nan_mask` |
| B | 去噪 / 跳变处理 / 回填 | `days_from_last_change`, `group_backfill`, `hump`, `kth_element`, `last_diff_value`, `ts_backfill` | `filter`, `hump_decay`, `jump_decay` |
| C | 尾部处理 / 稳健截断 | `pasteurize`, `tail`, `winsorize` | `clamp`, `left_tail`, `nan_out`, `purify`, `replace`, `right_tail`, `truncate` |
| D | 正交化 / 投影 | `ts_regression`, `vector_neut` | `group_multi_regression`, `group_vector_neut`, `group_vector_proj`, `multi_regression`, `regression_neut`, `regression_proj`, `ts_poly_regression`, `ts_theilsen`, `ts_vector_neut`, `ts_vector_proj`, `vector_proj` |
| E | 相关结构 | `ts_corr`, `ts_covariance` | `ts_co_kurtosis`, `ts_co_skewness`, `ts_partial_corr`, `ts_triple_corr` |
| F | 换手 / 尺度 / 单边 / 约束 | `scale`, `ts_target_tvr_decay`, `ts_target_tvr_hump` | `inst_pnl`, `inst_tvr`, `one_side`, `rank_by_side`, `scale_down`, `ts_delta_limit`, `ts_target_tvr_delta_limit` |

「已核验」栏与 `known_ops` 的一致性由 `tests/unit/test_optimization_v1_docs.py` 守：平台清单变了，这张表必须跟着改。

## 9. 常用算子限额

下列高频算子不得主导一轮：`ts_sum`、`ts_mean`、`rank`、`zscore`、`winsorize`、`ts_std_dev`、`scale`、`trade_when`（`round` 不在 `known_ops`，同上先复核）。

- 每个算子在 8 条表达式里**最多出现 2 次**；
- 补偿规则：一条表达式用了 ≥ 2 个高频算子，就至少再加 1 个 A–F 主题算子。

## 10. 必需执行流

### Step 0：确认设置

1. 需要时先认证；
2. `get_platform_setting_options` 确认 `region` / `delay` / `universe` / `neutralization` / `language` 的合法组合。

### Step 1：读基线并冻结核心字段

1. `get_alpha_details(baseline_alpha_id)`；
2. 提取并冻结：核心字段 / 数据集族；当前弱点（噪声、换手、相关性、拥挤、不稳定）。

### Step 2：先规划 8 个候选再写

每个槽位先定：角色（exploit / explore）、主题覆盖、类型（结构 / 同数据集组合 / 价量语义）、粗略算子数、高频算子预算。发批前确认：恰好 8 条；覆盖 ≥ 4 个主题；高频算子不超限。

### Step 3：算子预检

对每个候选：列出全部算子与显式算术符号；逐个查算子清单（存在性、必需参数、可选参数、关键字拼写）；拒绝裸的可选值与缺失的参数名。有缺失或畸形就先改写再校验。

### Step 4：本地校验（校验层三段）

按 §5 三段顺序执行，全过才继续。规则：失败就只修报错点、重跑到通过；不得删核心算子或替换成平凡形式来让校验器闭嘴。

### Step 5：多仿真

把 8 条已校验表达式交给 `create_multi_simulation`。响应被截断时：收集所有可见 alpha id → 用 `get_alpha_details` 补取缺失指标 / 表达式 → 以逐 alpha 的完成结果作为唯一可靠的本轮汇总。

### Step 6：回测后必做

对每个候选依次：

1. 检查强负信号并标 `CAND_NEG`；
2. 判断下一轮仍是 Stage A 还是可进 Stage B；
3. 平台返回 `operatorCount` 超限的（PPA）作废；
4. 全部检查 PASS 且 0 FAIL → 立即 `check_correlation`（只读的 PROD 相关性闸）；
5. PROD ≥ 0.7 → 按 D0-P 处置（不是无脑再来一批去相关）。

### Step 7：结果入库（不写自建文本文件）

批回测一结束就收割入库：`harvest_multisim_alphas` → `harvest_multisim_results`（`region` / `wave` / `alphas`），入库后 `backtest_results` 是本轮结果的**唯一权威副本**。迭代日志（8 槽角色、alpha id、Sharpe / Fitness / Turnover / 关键 FAIL、是否触发相关性检查、PROD 读数、next_actions）写在本轮回复里；S6 回写时进 `wave_result.key_findings`。**不要另写 `*_optimization_results.txt` 之类的追加文本**——那会形成第二份真相，也无人读取。

### Step 8：选全局最优并迭代

在当前全部候选（含基线本身，如果它仍占优）里选最优，作为下一轮参照。

## 11. 错误处理

### 11.1 仿真报错

先用 `lookINTO_SimError_message` 看详细报错，再分类：语法 / 畸形表达式；参数 / 签名不匹配；单位或警告；NaN 或数据问题。

### 11.2 429 或重复失败

遇到任何 429、警告或意外失败：

1. 逐个复查候选里用到的算子（对算子清单）；
2. 核对参数个数、关键字名、允许的用法形态；
3. 算子审计干净后才重试。

禁止：为过请求而丢核心算子；换一个更弱的无关算子走捷径；Stage 闸仍是 Stage A 时转入微调。

## 12. 提示模式示例（LLbaqEqa 类请求）

用户请求形如：「优化 JPN alpha `LLbaqEqa`，`region=JPN`、`delay=1`，目标全部 PASS、PROD 相关性可放行、`IS_LADDER_SHARPE` 必须过」。skill 应严格按本页执行：

1. 用 MCP 工具读基线 alpha 与设置选项；
2. 每轮恰好 8 个候选；
3. 仿真前走校验层三段；
4. 仿真该批，收割入库；
5. 回复里给出本轮 8 槽日志块与 next_actions；
6. 持续到出现达标候选，或平台证明当前分支无效，或触发 SKILL 的止损阶梯。
