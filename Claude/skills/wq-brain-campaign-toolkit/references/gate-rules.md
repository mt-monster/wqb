# gate.py 闸门判定细则 · build_wave 选波规则 · review_wave 墙枚举

> **闸编号的唯一注册表 = `gate.py::GATE_REGISTRY`**（代码），INDEX 里的闸表由 `gate.py --print-gate-table` 生成、`tests/unit/test_gate_registry_docs.py` 比对；本文只写**细则**，不再自称编号基准。`tools/wave_gate.py` 层的闸（体检硬门 / 闸 SEM / 闸 PF / 闸 2b / 闸 2.6 / 区域闸）与逃生口总表在 INDEX「闸与逃生口总表」。
> 文档里「5 闸」= 闸 1–5，「8 闸」= 闸 1–8（+ 可选闸 0，子闸 1b / 2b / 2b-2，附加闸 9）；「体检硬门」是 `tools/field_inspect_gate.py`，与闸 7 / 8 不同源，勿混谈。
> 缓存：`cache/gate_cache.json`，key = sha1(dataset + `\n` + expr)，幂等命中跳过。退出码：0 = 全 PASS，1 = 存在 FAIL。

## 一、agent 需知（每个闸拦什么、怎么改）

### 闸 1 语法（含 1b 算子元数 / 命名参数）

`alpha-expression-verifier` 的 `ExpressionValidator` 直调（不是子进程）。查找顺序：`WQ_VALIDATOR_DIR` → 各宿主已安装副本（`~/.claude/skills` → `~/.codex/skills` → 历史位 → **仓库 `Claude/skills` 最后兜底**，与 `_lib/skill_roots.py` 一致）——**主目录里的旧副本会先于仓库版本被采用**，所以每个进程会在 stderr 打印一行 `[gate] 闸1 verifier = <路径>`；对不上就设 `WQ_VALIDATOR_DIR` 或重跑 `tools/sync_skills.py`。verifier 缺失时结果标 `SYNTAX_UNKNOWN`（元数缺 catalog 标 `ARITY_UNKNOWN`）显式报警，**绝不静默放过**。1b 抓的是 verifier 抓不到的「命名参数被当位置参数传」（`hump(x, 0.005)` 平台回 `Invalid number of inputs`，整批 CANCELLED）。

### 闸 2 字段白名单（含 2b / 2b-2 区域闸）

来源顺序：**DB typed catalog**（`scan_fields.py` 写进 `fields` 表，缺省来源）→ 文件 `reference/<region>_<ds>_fields.json` → legacy 白名单 `reference/<region>_<ds>_field_whitelist.json`，都没有则报错并引导先跑 `scan_fields`。表达式字段 = idents − 已知算子 − group 标识符 − 价量字段 − 驱动参数，必须 ∈ verified 集合。**闸 2b**：区域非法 group 字段（如 JPN 的 sector / industry / subindustry 是 `Invalid data field`，整批连坐）；**闸 2b-2**：区域不可用字段 + VECTOR 上套 `ts_*`（JPN 无 pv1）——来源 `platform_constraints.json` 的 `region_invalid_group_fields` / `region_invalid_fields` / `region_vector_ts_forbidden`。

### 闸 3 类型（数据驱动）

catalog 有字段级 `type` 时解析全部函数调用区间：`type==VECTOR` 的字段其**最内层包裹必须是 `vec_*`**，否则报 `[EVENT] 事件型字段必须经 vec_* 聚合`（**标签是历史遗留**：文案里的「事件型」指 VECTOR 字段，与闸 8 的 `type==EVENT` 无关）；MATRIX 数据集禁 `vec_*`（`[TYPE]`）。无字段级类型（legacy 白名单）时退 strip 启发式。

**`--fix`**：VECTOR 数据集下把裸用的 VECTOR 字段自动裹上 `vec_*`（字段名含 count / sum / num / vol / qty / amount / total → `vec_sum`，其余 `vec_avg`），幂等，报告含 `fixed_expr`。它会改写表达式，故**禁用缓存**；只裹聚合不改信号逻辑，重要候选人工复核 avg / sum 的选择。

### 闸 4 不可访问算子 + quantile 元数 + banned_patterns

`ts_min` / `ts_max`：语法合法但平台回测 ERROR 并级联整批 CANCELLED。`quantile` 仅 1 参。`banned_patterns` 来自 catalog / whitelist，支持 `scope: vector_dataset`（MATRIX 数据集跳过该条）。

### 闸 5 毒模式（平台级 8 条 + 区域级追加）

来源：`config/platform_constraints.json` 的 `poison_patterns`（v1.6）+ 战役 `reference/<region>_generation_constraints.json` 的 `poison_patterns`（**仅区域特有**，勿写进平台文件）。覆盖矩阵由 `tests/unit/test_gate5_coverage_matrix.py` 守。加权 / 等权 / 中缀「拼腿」是用户定案的全局禁令（CLAUDE.md：禁止混信号调参，警惕 add(A,B)；2026-09-09 / 09-13 / 09-28 三次重申，任何放宽须先经用户明确确认）。

| 名称 | 判定 | 拦什么 | 放行形态 |
|---|---|---|---|
| `nested_three_leg_add` | 正则 | `add(multiply(rank(x),a), add(multiply(rank(y),b), …))` 嵌套三腿 add（整批 CANCELLED，KOR 实证）。**不要再「改写成 `add(add(a,b),c)` 左结合」**——三腿混合本身已被下面的等权 / 加权判定禁止 | — |
| `weighted_signal_mix` | 正则 | ≥ 2 个 `系数*rank(…)` 中缀加权腿 | 单腿缩放 `0.5*rank(a)` |
| `weighted_signal_mix_structural` | **结构**（括号平衡扫描，正则占位永假） | 任一 `add(` 的顶层实参 ≥ 2 个以「系数*」开头（含嵌套与镜像腿 `subtract(0, rank(x))`；纯正则版会漏 81%） | 单腿缩放 |
| `weighted_leg_mix_func_prefix` / `weighted_leg_mix_func_suffix` | 正则 | `add(multiply(<权重>, <腿A>), multiply(<权重>, <腿B>))`，权重在前 / 在后 | — |
| `equal_weight_leg_add` | **结构** | `add` 顶层 ≥ 2 个**形态不同**的信号腿（含等权 0.5A+0.5B）；用户 2026-09-28 定案 | `add(abs(x), 0.01)`（1 腿 + 标量）；`add(ts_mean(x,22), ts_mean(x,66))`（同形态仅窗口差 = 单信号多窗平滑） |
| `infix_leg_sum` | **结构** | 中缀 `+` 相加 ≥ 2 条形态不同的信号腿（`A*0.6 + B*0.4`、`A + B + C`） | `abs(x)+0.01`；`ts_mean(x,22)+ts_mean(x,66)`；一正一负价差走 spread 规则 |
| `spread_cross_dataset` | **结构**（仅 `--datasets` 多集批有 field→dataset 映射时判） | `subtract(A,B)` / `A-B` 的两腿字段分属**不同数据集** | **同源价差**（同一组字段、可一句话说清衡量什么，见 `platform_constraints.json` 的 `spread_signal_ruling`）；带数值系数的价差腿只告警 `[SPREAD_WEIGHTED]` |

合规替代（三选一）：①单信号结构 `ts_scale` / 同源 `subtract(rank(A), rank(B))`；②换算子几何 `group_rank` / `group_zscore` / `ts_quantile`；③换字段组合或换信号概念（Mode B 想法层，见 `wq-brain-alpha-optimization-v1`）。**不得靠调混合权重或增删腿数修不达标的信号。**

### 闸 6 批级多样性（评估 → 执行强制，缺省开启）

只对**批级**（`--file` / 整波）生效；契约 = 台账 `diversity_audit_latest.next_round_injections`（`diversity_audit.py` 每次评估写入）：

- **注入算子**：每批至少 `per_batch_min_operators`（缺省 2）条使用 `required_operators` 之一，不达标报 `[DIVERSITY]` 拒绝；**骨架配额**：`skeleton_quota`（如 ratio ≥ 1 / event_gated ≥ 1）逐项检查。
- **豁免**：`--batch-type repair | probe`；或 `--skip-diversity-gate` 逃生（须在台账记录原因，键名见 INDEX「闸与逃生口总表」的 waiver 协议）。
- **效力**：`consumed_batches` 达 `expires_after_batches`（缺省 10）→ **FAIL-CLOSED**（阻断提交）并**自动续约**新契约，重跑闸门按新契约校验；**不是「过期就不再拦」**。批内容 sha1 已消费则重跑不重复计数；总闸全过才记账消费。
- **对账**：下次 `diversity_audit` 输出 `injection_landing`（上一契约逐项落地 / 未落地），未落地项要么继续强制要么移出清单。
- **构建端**：契约就在台账里（`campaign.py ledger get diversity_audit_latest`），批次构建照它写；旧的 `diversity_slots.py` 已归档。

**注入算子请融进有经济含义的结构，不要为过闸装饰**（KOR wave104 实证）。三种入场方式：①**事件门控**：`if_else(rank(A) > 0.5, rank(A), 0)` / `trade_when(…)`，同时命中 event_gated 骨架槽；②**分组**：`group_zscore(A, <group>)`，同时命中 group 骨架槽——**`<group>` 必须是该区合法的 group 字段**（JPN 的 `sector` 是非法字段，闸 2b 会拦；按区域 profile 选）；③**单信号几何**：`ts_corr` / `ts_decay_linear` 等作用在**同一信号**上。辅助信号如何入场（条件 / 分组 / 分桶）的完整形态表见 `wq-brain-alpha-optimization-v1/references/structural-interaction-forms.md`。`bucket(x, n)` 输出 `Unit[Group:1]`，`rank()` / `add()` 不接受（闸 1 报 `Incompatible unit`）——bucket 不能与 rank 骨架组合，改用 if_else / group 满足同槽。

skeleton 槽判定速查：含 `if_else(` / `trade_when(` → event_gated；含 `group_` → group；`divide(` → ratio；含 `add(` / `multiply(` → linear_mix；其余 single（优先级即此顺序）。

### 闸 7 / 闸 8 / 闸 9

闸 7（`--sanity-longcount`）：VECTOR 字段实际 `longCount < 80` → **WARN**（目前没有任何代码把它按 profile 升级为 FAIL）。闸 8（`--sanity-event-type`）：引用 `type==EVENT` 字段即 FAIL（平台无 `ts_event_*`，先单条探针）。闸 9：非标准时间窗口（白名单 1 / 5 / 22 / 66 / 252 / 504 / 1008 / 1260），缺省 warn，`window_whitelist_enforce=true` 升 block；非白名单窗口须给出解释或实测证据。`--sanity-all` = 闸 7 + 8，输出 JSON 多一个 `sanity_gates` 字段。

## 二、build_wave.py：选波规则（DB 口径）

`--from-db` 缺省：从 `expressions` 表按 region + wave 取 GEM 产物；**只做选波后处理，不生成表达式**。

1. **全历史去重**：对该区 DB 里的历史表达式（`history_expressions`，排除本波）建规范化（去空白）哈希集，重复候选直接丢（KOR 实测 92 / 854 重复 = 11% 配额浪费）；读库失败会打 `[dedup][WARN]`，此时去重被严重低估。
2. **near-miss 加权**：`wave_results` 的 near 池 + 台账 `near_pool` 里出现过的字段，含这些字段的候选排前。
3. **算子树分桶**：根调用 + 第一个函数参数作桶键（如 `rank>ts_av_diff`），轮转抽样，每桶 ≤ `--per-bucket`（缺省 8）。
4. **骨架配给**：skeleton 五分类（event_gated / group / ratio / linear_mix / single）按 `<region>_generation_constraints.json` 的 `skeleton_quota` 限量。**`linear_mix` 是「含 `add(` / `multiply(` 的表达式」的占比上限**（缺省 ≤ 50%，含 `multiply(rank(x), -1)` 这类单腿写法），**不是配给目标、也不代表允许加权 / 等权拼腿**——拼腿由闸 5 拦；强制事件门控 / group / ratio 骨架进候选是为了直击 CW 墙根因。
5. **波内字段去重**：同一字段单波出现 ≤ `--max-field-repeat`（缺省 3）。
6. **多样性增强缺省关闭**（`--enhance-diversity never`）：`auto` / `always` 会结构变异、替换算子、追加 novel / random，与 GEM 铁律（显式 idea 的表达式保持经济方向）冲突，只作显式 opt-in；`--selection-contract-key` 模式强制 `never`。算子全覆盖 `--auto-coverage` 缺省也是 `never`。

输出 `wave_meta`（去重数 / 桶规模 / 骨架分布 / `selection_audit`）。选波数量与身份契约见 [`selection-plan.md`](selection-plan.md)。

## 三、review_wave.py：walls 诊断

- **missing ≠ fail**：指标缺失（None）不算败，单独标 `*_UNKNOWN`（`FIT_UNKNOWN` / `2Y_UNKNOWN` / `MARGIN_UNKNOWN` / `TVR_UNKNOWN`；平台未返回 `LOW_2Y_SHARPE` 时不能算 2Y 败）；无 sharpe 标 `NO_DATA`。
- **墙枚举**（`walls()` 的输出词表）：`SHARPE` / `FITNESS` / `2Y` / `MARGIN` / `TVR` / `CW`（平台 `CONCENTRATED_WEIGHT` 映射）/ 平台其它失败检查名原样带出 / `RN_EXPOSURE`（风险中性化后 sharpe ≤ `review.rn_sharpe_min`，缺省 0，就是风险因子暴露本身）/ `RA_OTHER`；**近闸池的排除类**另有 `ROBUST_STRUCTURAL`（robust / limit 过低的结构性死信号）与 `RN_EXPOSURE`——这两类不进 near / salvage 池与组合候选。prod 类墙由 prod-first 与 RA 决策表 D0-P 处理，不在 `walls()` 里。
- candidates = 全门槛过；near = 未过但 `sharpe > near.sharpe_min`（附 walls 诊断）。
- `--write-ledger` 幂等回写 `review_<tag>` / `near_pool` / `salvage_pool`，另在 `submit_ready` ledger 键留一条**审计副本**（不是提交队列，见 SKILL §3）。

## 四、维护者需知（改闸 / 改 verifier 时看，agent 可略过）

- 闸 4 必须对表达式**全部 idents** 判定 `ts_min` / `ts_max`：它们不在 `KNOWN_OPS` 里，对 `ops_used` 判定是死代码（KOR 历史教训）。
- `quantile` 只在本层加严为 1 参；verifier 签名表允许 1–3 参是语法事实，**不要改 `validator.py`**。
- `--fix` 的修复器是工作区单一实现 `tools/lib/vector_wrap.py::wrap_naked_vectors()`，被本 gate、MCP `fix_vector_fields`、makeSomeGem 生成端三处复用。
- 结构判定的命中在 `check_one` 里统一追加（正则占位 `(?!)` 永假），新增毒模式先补覆盖矩阵测试。
