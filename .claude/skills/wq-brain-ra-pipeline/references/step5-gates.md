# 步 5（S2→S3）细则：门禁——顺序、失败分支、豁免

> 主 SOP 见 [`../SKILL.md`](../SKILL.md) 步 5。**闸清单的唯一来源是 [INDEX](../../INDEX.md) 的两张生成表**（gate.py 闸表由 `GATE_REGISTRY` 生成；「闸与逃生口总表」由 `waiver.GATE_POLICIES` 生成）——本文不再复述闸的编号与开关，只写**怎么跑、失败后做什么**。
> 禁止新建 `_gate_waveNN.py`、禁止写 `cache/gate_wave*.json`：用 `tools/wave_gate.py`，结果落 `gate_results`。理由：旁路文件不是 `gate_results`，`get_gate_result` 读不到，本步「完成定义」永远是红的，S4 / S6 也会把这一波当成「没过门禁」；旁路脚本还会漏掉后加的闸（SEM / PF / 体检）。

## 5.1 怎么跑（一条路径）

```
# ① 幽灵算子硬闸（纯本地、零配额，先拦——含幽灵算子会整批 CANCELLED 连坐）
python tools/campaign_intel.py ghost-audit --region $REGION --exprs-file <候选表达式.txt>
# ①b 形状配额体检（只读、不入闸链；步 4 §4.5.1）：≥3 个形状族、trade_when ≤40%。退出码 1 = 不达标 → 回步 4 补形状，不要带着同质批进门禁
python tools/shape_quota_check.py --region $REGION --wave $W
# ② 每波门禁：语法 + gate.py 各闸 + 体检硬门 + 闸 SEM + 闸 PF + 批级多样性，一键落盘 gate_results
python tools/wave_gate.py --campaign-dir tracking/$REGION --dataset $DS --wave $W --from-db
#    候选不在库时： --exprs-file <候选表达式.txt> ；单条自查： --expr <表达式>
```

- 节点等价：`mcp__wq-brain-http__workflow_execute(node="wave_gate", params={region, dataset, wave, …})`（遵守 dry-run 契约 + argv 契约校验）；与 CLI **同一实现**，节点只是把它包成可入链的一步。无 MCP 时用 CLI。
- ⚠ `workflow_campaign(stage="S2")` 只路由到 `build_wave.py` = **选波**（步 4 已调），**不要拿它代替本步门禁**；仅需要重建波次时才回选波。
- 脚本归属：`wave_gate.py` / `preflight_wave.py` / `field_inspect_gate.py` 在仓库根 `tools/`；`gate.py` / `pipeline.py` / `build_wave.py` / `score_datasets.py` / `assemble_priors.py` 在 toolkit `Claude/skills/wq-brain-campaign-toolkit/scripts/`。`--wave` 全链路为**字符串**（`97` 与 `s2_xxx_d1` 都可）。
- VECTOR 字段用 `mcp__wq-brain-http__preflight_expressions(auto_fix_vector=true)`；repair / probe 批的多样性豁免见 5.4。
- **完成定义**：`mcp__wqb-db__get_gate_result(region, wave, dataset)` 有本波记录且 `all_pass=1`（`all_pass` 只有 true / false 两种终态；门禁脚本崩溃 = ERROR 终态、退出码 2，不是 FAIL）。

## 5.2 失败分支：闸 → 现象 → 动作 → 回哪步 → 能否豁免

| 闸 / 检查 | 现象 / 退出码 | 动作 | 回 | 豁免（waiver 的 gate） |
|---|---|---|---|---|
| 语法（闸 1）/ 算子元数（闸 1b） | wave_gate 语法 FAIL | 修表达式（PLY verifier + `op_arity`） | 步 4 | 否 |
| **幽灵算子** `ghost-audit` | 退出码 1 | 见 5.3 决策表；违规式隔离到独立小批 | 步 4 | 否 |
| 字段白名单（闸 2）/ 区域非法 group（2b）/ 区域不可用字段（2b-2） | gate FAIL | 换字段 / 去掉非法 group 字段 | 步 4 | 否 |
| 类型（闸 3） | VECTOR 未被 `vec_*` 包裹 / MATRIX 上误用 `vec_*` | `preflight_expressions(auto_fix_vector=true)` | 步 4 | 否 |
| 毒模式（闸 5） | FAIL（含加权 / 等权腿相加 / 中缀 `+` / 跨数据集价差） | 改写为合规结构，见步 7 细则「允许的组合形态」 | 步 4 | 否 |
| **批级多样性（闸 6）** | FAIL | 回步 4 补骨架（查 `KB/community_tpl_kb` 按 category 检索候选骨架，先过 `ghost_operator_advisory`）；**软触发（准则，无代码闸）**：批内结构熵 < 1.5（原文口径）或 diversity 配额超限即查 KB 补骨架，不等硬 FAIL——代码里 `diversity_enhancer` 自己用的是算子熵 < 2.0；**KB 无货 → `forum_recon` 补库后回补骨架**（显式 `--queries` 关键词包可避免机械派生的穷举）；若「2 跨集」FAIL 则拆回单集组合，不停挖 | 步 4 | `diversity`（repair / probe 批默认豁免，仍需显式 `--skip-diversity-gate` 时才要 waiver） |
| longCount（闸 7）/ EVENT 类型（闸 8）/ 非标窗口（闸 9） | 7、9 = WARN；8 = FAIL（引用 `type==EVENT` 字段） | 8：移除 EVENT 字段或先单条探针；7：低 longCount 字段降级为条件腿 | 步 4 | 否 |
| **闸 SEM** | **exit 2**：缺 `s1_semantic_<ds>`；命中黑名单字段的表达式被剔出 | 跑 `field_semantic_classify.py --write-ledger` | **步 3** | `semantic` |
| **体检硬门** | 违规计入 FAIL；缺体检包按 `--inspect-mode`（warn 放行 / enforce 整波拦） | 补预处理（低覆盖 → `ts_backfill`；高偏度 / 厚尾 → `rank` / `winsorize`；稀疏事件 → `trade_when`）或补体检包 | 步 4 / 步 2 | `inspect` |
| **闸 PF** | 命中**已死路骨架**（本区 `prod_family_<region>_<骨架指纹>` / alphas 表里同骨架前 2 个算子 ≥ 3 条实测且 prod ≥ 0.7）→ **enforced 拦整波**；**新骨架**（本区无 prod 记录）、**小样本**（n < 3）、**混合骨架**（既有 ≥ 0.7 又有干净记录，先加深到前 3 个算子再判）→ 只 WARN（与闸 2.6 `prod_saturation_gate`〔字段热度 / 数据集占比〕互补） | 换骨架 / 机制；新骨架先 prod-first 探针（步 5b） | 步 4 / 步 5b | `prod_family`（CLI 开关 `--no-prod-family-gate`） |
| 开波区域闸 | **exit 2**（enforce）：signal_floor / stop_rules / backlog / catalog 命中 | 按闸提示消化积压 / 补 catalog / 换区；用户显式要求继续 → waiver | 步 2 / 步 1 | `stop_rules` / `backlog` / `region_gates` |

> 「拦整波」（闸 PF、开波区域闸）与「只剔出命中表达式」（闸 SEM）粒度不同：前者是骨架 / 区域级证据，后者是逐条字段问题。

## 5.3 幽灵算子命中后的三种处置（决策）

| 情形 | 处置 |
|---|---|
| `ghost_operator_advisory` 里有已验证的等价算子 | **等价替换**（映射表在键内与 `docs/reference/community_tpl_library_sequel.md` §十八） |
| 无等价映射但想保留想法 | `mcp__wq-brain-http__preflight_expressions` **单条实测**；平台确实不认 → 丢弃 |
| 已知幽灵（`config.GHOST_OPERATORS`，如 `ts_median`）且无替代 | **丢弃**，用已验证算子重写想法 |

区分：`operator_audit`（MCP）审计**平台算子表**；`campaign_intel.py ghost-audit` 是**表达式级**检查。`validate_expressions` / `preflight_expressions` **不查幽灵算子**（会对 `ts_median` 返回 valid=true），所以 dispatch 之前必须显式跑 ghost-audit。

## 5.4 批级多样性守卫（闸 6）与 repair / probe 批

- **判据的唯一执行口径 = toolkit `gate.py:check_batch_diversity`**，由 `wave_gate.py` 在提交前自动调用。三源：① **自学习契约** `explore_contract`（`rules.get_active_contract`）；② **收益来源多样性**（读 DB idea ledger 的 `expected_exposure`：同批 > 60% 表达式共享同一 exposure 且字段族相同 → FAIL；无 exposure 元信息 → WARN 不阻断）；③ **家族天花板预检**（主导腿信号族占比 ≥ 2/3 → WARN 不阻断；wave94 / 95 / 98 / 104 实证 SELF ≥ 0.9 必死）。60% 与 2/3 是这些实证波的经验值。
- **契约过期的处理顺序**：过期 → **自动续约** → 用新契约**重判**（重判结果仍可 FAIL）。
- **形状配额（步 4 §4.5.1）与闸 6 的分工**：闸 6 是这里的硬闸（契约 / 收益来源 / 家族天花板）；`tools/shape_quota_check.py` 是门禁前的**人可读体检**（≥ 3 个形状族、`trade_when` ≤ 40%，启发式分类），不入闸链、不产生 gate_results。两者判据不同，通过一个不代表通过另一个。
- `wqb.expression.validator.check_batch` **只作方法论参考**（形状维度自检），全仓零调用方，不构成门禁；不要以为调了它就过了闸。
- `--batch-type {explore,repair,probe}`：repair / probe 批默认豁免多样性契约；需要显式跳过闸 6 时才加 `--skip-diversity-gate`，且须先写 `diversity` waiver。

## 5.5 生成侧预闸与本步的关系

预闸（GEM 产出侧自动修：hump 命名参数、bucket 补 range、非法 group 字段丢弃、窗口别名…，见步 4 细则 4.4）与闸 2b / 语法闸是同一批规则的两种处置：**预闸 = 产出侧自动修；闸 2b / 语法闸 = 非 GEM 来源表达式的兜底**。

## 5.6 体检硬门的五条判据与体检包

`tools/wave_gate.py` 内置调用 `tools/field_inspect_gate.py`，逐条比对字段体检结果，违规计入 FAIL：

| 体检结果 | 表达式必须含 |
|---|---|
| 低覆盖（cr < 0.4） | `ts_backfill` |
| 高偏度（\|skew\| > 2） | `rank` / `winsorize` / `signed_power` |
| 厚尾（kurt > 8） | `rank` / `winsorize` |
| 单边恒正 / 恒负 | 不能直接用原始水平值 |
| 稀疏事件（zero_inflated / point_mass） | `trade_when` |

- 体检包路径 `tracking/mining/field_inspect_<region 小写>_<dataset>.json`，**生成器 = `tools/gen_field_inspect_packs.py`**（细则见步 2 细则 §2.5）。**不要直接用 `webdata_quality.py --export-expr`**：它一次把整个 region × delay 的全部数据集导成**一个**约 29 MB 的文件（闸每次只查一个数据集），且 2026-09-07 修复 `rsplit` 越界之前恒产出 0 字段；生成器 = 在它之上做瘦身与按数据集拆分。
- 缺包时本闸**不生效**，`wave_gate` 会打印 `[inspect] 体检硬门未生效` 并给生成命令——看到这行就说明这一波的预处理约束没人把关。
- 单独自查：`python tools/field_inspect_gate.py --region USA --dataset model267 --exprs-file <txt>`。

## 5.7 为什么这一步不能省

门禁的存在理由：整批 CANCELLED 连坐（批内一条坏式 ERROR 取消全部兄弟任务）与整批同质化都发生过。两个「假绿」要警惕：**干跑绿不证明 LLM 可达**（步 4）、**体检包缺失时体检门不生效**（上面）。
