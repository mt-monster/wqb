---
name: brain-alpha-research-hypothesis-first
layer: L1
description: "饱和数据集（平台 alphaCount ≥ 1 万，或该集连续 2 波模板全灭）改走假设驱动：起草可证伪假设目录，用 hypothesis_round 节点构建主假设 / 去门控消融 / 对照 / 变体四条一组的实验，回测后交 judge() 判定。条件激活：目录缺失时先起草。触发词：饱和数据集 / 假设优先 / hypothesis-first / 模板挖尽。"
last_verified: 2026-09-29
allowed-tools:
  - Read
  - Bash
  - mcp__wq-brain-http__*
---

# BRAIN Alpha 研究 — 假设优先（Hypothesis-First）

## 职责边界

- **本 skill 负责**：**饱和数据集**的假设驱动路径——起草可证伪假设目录 → 构建「主假设 / 去门控消融 / 对照 / 变体」四条一组的实验 → 回测读数交 `judge()` 判定 → 记账。
- **本 skill 不做**：不饱和数据集不走此路（走概念优先生成，步 4）；**不豁免任何闸**——门禁、回测、提交判定（步 5–8）照走；**不写 `dead_end`**（判死只由 RA 步 9 `seal_dead_end`）；不提交。
- **上游 / 下游**：上游 = RA 步 2 约束 6 的路由（本 skill 只在它命中时接管）+ 步 3 的字段语义 `s1_semantic_<ds>`；下游 = 步 5 门禁 → 步 6 回测 → 本 skill 的 judge → 步 9 写回。假设**目录由 agent 按 §3 起草**（字段扫描不产假设）。

## 状态：条件激活（dormant）——先读这一节

| 项 | 现状（2026-09-29 核验） |
|---|---|
| 代码 | `src/wqb/research/hypothesis_miner.py` 与节点 `hypothesis_round` 存在、有单测；节点**纯本地**：不触平台、不写 `expressions` 表 |
| 假设目录 | 仓库不带目录（`data/` 整体 gitignore）；本机没有 `data/hypothesis_catalog/<ds>_hypotheses.json` 就是**尚未起草**，不是「缺前置」 |
| 使用记录 | 没有战役实跑过；`judge()` 除单测外**没有调用方**（§5 的 ⑥ 是手工一步） |
| 结论 | RA 步 2 约束 6 命中即**激活**——目录缺失时由 agent 起草（§1 的分支表），**不存在「等假设生成器」的前置**（旧文「目录为空时不强行路由」与 RA「强制切换」会死锁，已取消） |

## 1. 何时切换、目录缺失怎么办

**两条可测信号（与 RA 步 2 约束 6 同一口径，满足任一即切）**：① 目标数据集平台 `alphaCount ≥ 1 万`（`get_datasets` / `recommend_datasets` 里读；拥挤线是经验值，出自 2026-09-12 的实测样本）；② 该集**连续 2 波**模板全灭（`gate_results.all_pass` 全 0）。

背景，**不作触发**：news12（约 12 万 α / 2.1 万用户）Fitness ≈ 0.42 的天花板（2026-04-23，一次 90 条会话的实测个例）；论坛高赞自动化模板流程（帖 HZ32281，80 赞）——一个是个例数字，一个无法度量。

| 情况 | 动作 |
|---|---|
| 目录存在且 ≥ 20 条 | 直接 §4 |
| 目录缺失 / 不足 20 条 | §3 起草，先干跑校验；**没有额外的人工批准点**——校验器、幽灵算子闸、步 5 闸就是批准人，用户可随时否决 |
| 起草不出 ≥ 20 条可证伪假设（字段太少 / 讲不出机制叙事） | 不硬凑：停止模板遍历，回 RA 步 2 换集 / 换区；同集仍要挖 → 按 RA 步 3 §3.3 冷门字段优先 + 步 5b prod-first |

「≥ 20 条」是起草量的**经验起点**（`load_catalog` 不强制条数）；每轮只跑 `max_hypotheses` 个假设，多起草是为后几轮不必重来。

## 2. 字段语义：用 `s1_semantic_<ds>`，不另建 YAML

旧版要求建 `data/field_semantics/<region>_<dataset>.yaml`（`anchor_only` 等）——**没有任何代码读它、也没有闸执行它**，且与步 3 的 `s1_semantic_<ds>`（signal / blocked，闸 SEM 读）是两套互不引用的字段语义，**已取消**。

- 字段语义 = `s1_semantic_<ds>`（`python tools/field_semantic_classify.py --region <R> --dataset <ds> --write-ledger`）；`blocked` 字段不得作主信号（闸 SEM 拦）。
- **anchor-only**（价格锚，如 `news_spy_close`、`news_eod_close`）是**纪律**不是台账字段：只作条件 / 分母 / group，**不作主信号**（CLAUDE.md「区分主信号与辅助信号」）；假设用到锚字段时写进 `description`。
- **字段选择与 FQ 反向**：饱和数据集里高使用量字段最易撞 prod 墙（RA 步 3 §3.3、[`brain-alpha-research-field-quality`](../brain-alpha-research-field-quality/SKILL.md) §1）——**信号字段优先取 users 0–9 的冷门字段**（冷门字段占批次预算 ≥ 50%，经验阈值，出自 GLB 2026-08 实验），热门字段只作门控 / 锚；`alphaCount` / `userCount` **不再作种子排序依据**。

## 3. 起草假设目录（JSON）

- 路径 `data/hypothesis_catalog/<dataset>_hypotheses.json`（节点缺省；也可传 `catalog_path`）。**只支持 JSON**（`load_catalog`）——旧文的 YAML 示例是错的。目录是**输入计划**，不是战役事实源（事实源是回测与 `wave_results`）；丢了可重建，也不入库。
- 每条 8 个必填字段，**`hypothesis_miner._REQUIRED_FIELDS` 是唯一字段清单**；`hypothesis_class` 必须在 `HYPOTHESIS_CLASSES`（下面 12 类）里，**不在则 `load_catalog` 抛错**。
- 四条表达式的分工：`minimal_expression` = 假设的最小落地（信号 + 门控 / 结构）；`ablation_no_gate` = 去掉门控只留信号（门控有没有贡献）；`control_constant` = **对照臂**：保持**同一结构**，把信号项换成与假设无关的项（收益若不变 → 不是该字段在起作用，即伪信号）；`variant` = 同一假设的另一种落地（换算子，或换到另一个标准窗口）。`control_constant` 沿用代码字段名，**不是数值常数**——常数表达式经中性化后没有截面信息，不能当对照。
- **对照的替换字段取同一数据集内、机制无关的字段**——白名单外的字段（如非 pv 数据集里的 `volume`）会被闸 2 拦掉整波。`expected_direction` 只是记录，`judge` 不读它：`minimal_expression` 必须**已按预期方向写好符号**（Sharpe 为负 → `needs_refinement`，先试翻符号）。
- 窗口只用标准窗口 1 / 5 / 22 / 66 / 252 / 504 / 1008 / 1260（RA 预闸会把 20 别名成 22）；表达式须先过校验器与幽灵算子闸。

```json
{"hypotheses": [{
  "hypothesis_id": "H_overreact_attention",
  "hypothesis_class": "over_reaction",
  "description": "高关注度日的短期价格反应过度，5 日内回归；价格只作信号腿，不作主信号（示意字段，换成本数据集的真实字段）",
  "minimal_expression": "trade_when(rank(<关注度字段>) > 0.8, -rank(ts_zscore(<反应字段>, 5)), -1)",
  "ablation_no_gate": "-rank(ts_zscore(<反应字段>, 5))",
  "control_constant": "trade_when(rank(<关注度字段>) > 0.8, -rank(ts_zscore(<同集无关字段>, 5)), -1)",
  "variant": "trade_when(rank(<关注度字段>) > 0.8, -rank(ts_zscore(<反应字段>, 22)), -1)",
  "expected_direction": "positive"
}]}
```

假设类别（12 类；与 dfe 8 问 / GEM 概念位的对应见 [`wq-brain-ra-pipeline/references/concept-taxonomy-map.md`](../wq-brain-ra-pipeline/references/concept-taxonomy-map.md)，词表单一来源 = `hypothesis_miner.HYPOTHESIS_CLASSES`，测试守三处一致）：`over_reaction / under_reaction / dispersion / event_conditional / propagation / information_asymmetry / cross_dataset / horizon_spread / regime / residual / slow_diffusion / urgency`。

## 4. 构建一轮实验（本地、零成本）

```
mcp__wq-brain-http__workflow_execute  node="hypothesis_round"  dry_run=true \
  params={"dataset_id": "<ds>", "region": "<R>", "delay": 1, "max_hypotheses": 2}
```

先干跑：校验目录存在 / 可解析 / 类别合法，返回计划（`total_expressions = 4 × 选中假设数`）。通过后 `dry_run=false` 实跑，得 `experiments[<hypothesis_id>].expressions`（按上面顺序的 4 条）。`max_hypotheses=2` 正好 8 条 = 本仓库的标准批（`create_multi_simulation` 单次 2–10 条）；一条坏式会取消整批兄弟，所以先过 §5 的闸。可选 `save_ledger=true`（§6）。目录缺失 / 字段缺 / 类别不在词表 → `success=false`，报错里有路径与原因。

## 5. 完整回路：计划 → 入库 → 闸 → 回测 → 判定

| # | 动作 | 工具 | 产物 / 完成定义 |
|---|---|---|---|
| ① | 干跑校验 | §4 的干跑 | 计划通过 |
| ② | 实跑构建 | §4 的实跑 | 每个假设 4 条表达式 |
| ③ | 入库 | `mcp__wqb-db__upsert_expressions(region, wave, expressions=[…], dataset=<ds>, source="hypothesis")`（RA S2 的「直写」入口） | `list_expressions(region, wave)` 查到 4×N 条——**未验证入库不得说成功** |
| ④ | 步 5 门禁 | `python tools/campaign_intel.py ghost-audit …` → `python tools/wave_gate.py --campaign-dir tracking/<R> --dataset <ds> --wave <W> --from-db`（[`step5-gates.md`](../wq-brain-ra-pipeline/references/step5-gates.md)，一字不省） | `get_gate_result` 的 `all_pass=1` |
| ⑤ | 步 6 回测 | `mcp__wq-brain-http__workflow_batch_track`（[`step6-backtest.md`](../wq-brain-ra-pipeline/references/step6-backtest.md)） | 4×N 条 `backtest_results` |
| ⑥ | 判定 | 从 `mcp__wqb-db__list_alphas_by_wave(region, wave)` 按表达式取 `sharpe` / `fitness`，调 `judge()`（下） | 每个假设一个 verdict |
| ⑦ | 写回 | RA 步 9 的 `upsert_wave_result`，`key_findings` 带 `hypothesis_id` / `hypothesis_class` / verdict / `sharpe_delta` | 事实源 |

```powershell
& $WQ_PY -c "import sys; sys.path.insert(0,'src'); from wqb.research.hypothesis_miner import ExperimentResult, judge, save_to_ledger; v=judge(ExperimentResult('<hid>', primary_sharpe=<主>, ablation_sharpe=<消融>, control_sharpe=<对照>, variant_sharpe=<变体>, primary_fitness=<主 fitness>)); print(v['status'].value, v['reason'], v['diagnostics'])"
```

### verdict：假设级结论，词汇与全库的关系

| `judge` 状态 | 判据（代码常量，**经验值、没有校准记录**） | 下一步 |
|---|---|---|
| `rejected` | \|主 − 对照\| ≤ 0.1（`_PSEUDO_SIGNAL_TOLERANCE`，**伪信号**）；或对照比主假设好 > 0.1（门控在拖累） | 该假设结案，不追变体——伪信号在**第一批**就判死，省下 ~40 条变体追踪的仿真 |
| `needs_refinement` | 主 Sharpe < 0.3（`_MIN_PRIMARY_SHARPE`） | 按诊断改表达式（负值先试翻符号）后再走 ③–⑥ |
| `partially_supported` | 有增量但 Δ ≤ 0.5 或 fitness ≤ 0.8 | 看 `diagnostics` 的 `ablation_delta` / `variant_delta`，细化一个参数 |
| `supported` | Δ > 0.5（`_SUPPORTED_SHARPE_DELTA`）且主 fitness > 0.8（`_SUPPORTED_FITNESS`） | 主假设表达式进步 7 / 步 8，**与其它候选走同一条路**——`supported` 不等于可提交，评审闸与 `tools/submit_verdict.py` 照走 |

这四态是**假设级**的，与波级 verdict（`PASS` / `PARTIAL` / `FAIL`）、数据集 / 区域级的 `dead_end` 是不同层：`rejected` **不写** registry；`needs_refinement` / `partially_supported` 的每一轮都计入 RA 步 7 的「同一想法 > 10 种结构仍不过 → 步 9 记 `dead_end`」；判死只走步 9 ⑤（未选、未回测不得写）。

## 6. 台账

- **事实源**：RA 步 9 的 `wave_results.key_findings`（§5 ⑦）。
- **辅助日志**：`tracking/hypotheses/ledger.jsonl`（`save_to_ledger` / 节点 `save_ledger=true`）——运行时缓存，gitignore，**不作事实源**、可丢弃；节点里它锚在仓库根，手工调 `save_to_ledger` 缺省是相对当前目录（在仓库根运行）。记录只有 `session_id` / `status` / `reason` / `diagnostics` / `timestamp`，**没有 hypothesis_id / class 字段**，按类聚合做不了；要按假设复盘就把 id 拼进 session（约定 `<dataset>_<REGION>_d<delay>_<hypothesis_id>`）。
- 旧文的 `data/hypothesis_ledger/<session>.jsonl` 从未存在；「对假设类别的元学习取代逐臂 bandit 后验」没有实现，已删。

## 验证清单（每项写产物）

1. **路由条件已核**：回报里有 `alphaCount ≥ 1 万` 的读数，或连续 2 波 `all_pass = 0` 的两波编号。
2. **目录已校验**：`hypothesis_round` 干跑 `success=true`，计划的 `total_expressions` = 4 × 选中假设数；类别都在 `HYPOTHESIS_CLASSES`。
3. **已入库且过闸**：`list_expressions` 有 4×N 条（`source="hypothesis"`），`get_gate_result` 的 `all_pass=1`。
4. **每个假设已判定**：`judge` 输出（状态 + `diagnostics`）写进本波 `key_findings`，含 `hypothesis_id` / `hypothesis_class`；伪信号第一批即 `rejected`，没有为它追变体。
