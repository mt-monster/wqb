# Skills / 流程 Review（对照挖掘记忆经验）

> 2026-10-03。对照源 = `.workbuddy/memory/MEMORY.md` + `RULES.md §A–§H`。
> 方法：把记忆里的高价值法则当作**探针**，反查它们是否落到 ① 机器层 `methodology_rules.json` ② 文档层 `docs/experience/*.md` ③ skill 路由表 ④ 区域 profile。
> **核心结论：你最贵的两条学费（等价算子替换、换分母）在机器层和文档层都写进去了，但两条轨道都没接上消费点——武器成了孤儿。**

---

## P0 · 武器成孤儿（双轨同时断裂）

### 0.1 机器层：23 条规则里 19 条无任何代码分支消费

`Claude/skills/wq-brain-campaign-toolkit/config/methodology_rules.json` 共 23 条规则。
全仓消费点只有三个：`build_wave.py`（选波）、`review_wave.py:323 → recommend_next_wave`（步 7 诊断）、
`pipeline.py`（L1 采集 / L4 证伪）。

**真正能产生行为影响的只有 4 条**（在 `recommend_next_wave` 里生成 `recs`）：

| op | 规则 | 是否消费 |
|---|---|---|
| `gradient_dilute` | `prod_wall_dilution_v1` | ✅ |
| `warn_rnf_drop` | `rnf_dilution_tradeoff_v1` | ✅ |
| `classify_failure_nature` | `failure_nature_classifier_v1` | ✅ |
| `fail_fast_stop` | `no_effort_seven_signals_v1` | ✅ |

**其余 19 条分两类：**

| 类别 | 条数 | 说明 |
|---|---|---|
| **仅 print**（`build_wave.py:795`） | 12 | `apply_rules(ctx,"strategy")` 后只 `print(f"[rules][strategy:...]")`，注释明写「不拦截，仅提示」。且 12 条 strategy **无条件全打印**（condition 不参与匹配）。ⓘ 发生在**选波阶段**，此时还没有回测结果，`is_strong_but_blocked` 之类条件不可能成立 ⇒ 提示出现在最不该出现的时机 |
| **完全不可达** | 7 | 3 条 `gate_override` + 1 条 `field_whitelist` + 2 条 `diagnosis`（op 无分支）+ 1 条 `dead_end` 无 `block_pattern` |

最贵的两条落在「仅 print」类：

| rule_id | op | 消费分支 |
|---|---|---|
| `equivalent_operator_substitution_v1` | `scan_equivalent_operators` | ❌ 无 recs 分支（仅选波时 print） |
| `denominator_is_the_real_self_wall_variable_v1` | `swap_denominator` | ❌ 无 recs 分支（仅选波时 print） |

验证：`grep -rn "scan_equivalent_operators\|swap_denominator"` 排除规则定义文件后**返回空**。

**附带发现（死代码）**：`build_wave.py:781` 的判死拦截 `if pat:` 分支，
依赖 `action.block_pattern`——而**全部 23 条规则中带 `block_pattern` 的为 0 条**。
⇒ 判死规则（`zero_competition_no_signal_v1` / `no_effort_seven_signals_v1`）**永远拦不掉任何表达式**。

### 0.2 `trigger.condition` 是死字段

`RuleStore.query()`（`_lib/rules.py:216`）只匹配 `trigger.region / universe / dataset_type`，
**从不解析 `trigger.condition`**。而这两条规则的触发条件恰恰写在 condition 里：

- `"is_strong_but_blocked AND 几何已扫尽"`
- `"prod_corr > 0.7 AND 已提交通族兄弟"`

⇒ 条件是自然语言字符串，写得再精确也不参与匹配；实际匹配靠调用方硬编码的 `action.op`。
**既有噪声（无条件注入），也错失（条件满足时不会比别处更强）。**

### 0.3 文档层：步 7 的路由表没指向装武器的那一篇

- 等价算子替换 / 分母法则写在 **`docs/experience/02_signal_patterns.md` §12 / §13**（内容完整、含 KOR 实证表）。
- 但 `wq-brain-ra-pipeline/SKILL.md` 的经验库路由表把 `02_signal_patterns.md` 只映射给 **步 3–4（设计信号）**；
  **步 7（诊断改进）只指向 `05_antipatterns.md`**。
- 而 `05_antipatterns.md:34` 只引了 `02_signal_patterns.md §1`（组合形态），**没引 §12 / §13**。

### 0.4 后果（可归因）

IND 战役 20 批 / ~170 表达式 / 可提交 0 颗；KOR 首颗 ACTIVE 是**人工翻记忆**拿出 `quantile` 才产出的。
如果步 7 能自动注入这两条 rule，IND 那 8 颗 prod 撞墙候选至少会被建议"扫等价算子 / 换分母"各一次。

---

## P1 · skill 之间给出相反建议（硬性冲突）

| 来源 | 对 `signed_power` 的态度 |
|---|---|
| `wq-brain-ra-pipeline/references/step7-diagnose.md:98` | 「破比值闸的合规旋钮（实测有效）：… **`signed_power` 压尾** …」 |
| `brain-how-to-pass-alpha-test/SKILL.md:39` | 「**压尾前查持仓对称性**：`signed_power` 压尾会造成多空不对称而触发 `LOW_INVESTABILITY_CONSTRAINED_SHARPE`；实测 `quantile` 替 `signed_power` 后多空完全对称 ⇒ **优先换等价的非压尾包装算子**」 |

后者是对的（有 LC319/SC319 实证），前者是 `signed_power` 时代的遗留，
且正是 `02_signal_patterns.md §12` 明确"被推翻的结论"。
⇒ **建议**：step7-diagnose:98 加反向引用，把 `signed_power` 从"推荐旋钮"降级为"须先查持仓对称性"。

---

## P1 · 区域经验未回写 profile / 决策表

### 1.1 KOR profile 缺最根本的第 7 条约束

`references/regions/KOR.md` 只有判死清单（KOR-ANALYST16-EST-PCT-DEAD 等），
**完全没有「输入频率二选一」**——记忆里标为 KOR 7 条结构性约束中**最根本**的一条：

| 口径 | 频率 | S | 2Y |
|---|---|---|---|
| `accum_*` 累积 | 低频 | 0.80–0.98 | **1.72–1.93** |
| `stk_*` 当日 | 高频 | **2.00–2.01** | 1.12–1.20 |

低频出 2Y、高频出 IS，四闸要两者兼得 ⇒ **结构上不可同时满足，换塔换集都绕不开**。

### 1.2 选集排序准则缺「信息维度新颖度」

记忆铁律：**IS 强度与 prod 新颖度负相关**（拥挤族 S 2.2–4.5 / prod 0.78–0.99；未拥挤族 S 0.07–1.22）
⇒ 选集阶段就该按"信息维度是否已在 prod book"排序。

但 `step2-s0.md` / `decision-table.md` D4 仍按 **coverage / alphaCount / valueScore** 排序，
而记忆明确警告：**稀疏覆盖高 valueScore 是陷阱**（model77 valueScore 5.0 全场最高，字段 coverage 一律 0.4001）。
⇒ 排序准则与已付学费的教训相反。

---

## P2 · 工程坑未进 skill（只在记忆里）

| # | 教训 | 现状 |
|---|---|---|
| 1 | `tools/ind_sim_submit.py`（settings 全显式，2026-10-03 新写） | **未出现在任何 skill** |
| 2 | `submit_batch.py` 固定 nanHandling/maxTrade ⇒ 与 MCP 批**不可比** | 只在 `worldquant-submit-alpha` 提了"派发≠提交"，未提 settings 固定 |
| 3 | nanHandling=OFF / maxTrade=ON ⇒ IND 行为族 **S 2.19→0.46**（强度闸） | 只有 `inspect-raw-template` 提"各区不一致"，未提是强度闸 |
| 4 | 差集法端点 `/data-sets`（**不带 limit/offset 返回 0 条**、429 退避、`category` 是 dict） | 只有 `ace_lib.py` 代码，无文档 |
| 5 | `ts_backfill` **不支持 event inputs**（MATRIX 报出但实为 VECTOR/event ⇒ `vec_avg`） | skill 只写"VECTOR 先 vec_avg" |
| 6 | ledger 脏行 `Extra data`（`json.loads` 全表挂，连 `score_datasets.py` 一起瘫） | 未写 |
| 7 | multisim 卡死判据：progress 0.1 停滞 >10min 且 child_count=0 ⇒ 重发 | `step6-backtest.md` 故障表未见此判据 |
| 8 | **AGENTS.md 文档过时**：称 `RuleStore.query()` 在 `gate.py`/`build_wave.py`/`pipeline.py`/`review_wave.py` 四处强制注入 | 实际：`gate.py` 只用 **contract** 规则；`build_wave.py` 只 `apply_rules("dead_end")`；真正消费 strategy 的只有 `review_wave.py` 一处 |

---

## 已经做对的（不要动）

- 组合形态铁律（禁混信号）**双轨固化完整**：`platform_constraints.json` v1.5 + gate 闸 5 + `docs/experience/02 §1` + 记忆 §0。
- **SUB 是比值闸**（step7 §7.6.1）：明确写了"sharpe 越高越好在提交层是错的"，举例 sharpe 1.62 → SUB≥0.93（≈0.571 系数，建议把系数写死）。
- **步 5b prod-first 探针** + 决策表 D0-P：正是"挖到即测即交"的代码级固化。
- **步 8 同日提交**（pv103 案例：先做变体 1 小时被外部同款顶到 prod 1.0）：陈旧 prod 风险已覆盖。
- 已点亮塔不进白名单 ✓（缺一条："塔计数按自然季度清零，查上季须显式传 start/end"）。
- 五层漏斗 / L3.5 结构族 ✓。QUICK 产物不可提交 ✓。

---

## 建议修正（按性价比排序）

| 优先级 | 动作 | 成本 | 收益 |
|---|---|---|---|
| **A** | `_lib/rules.py::recommend_next_wave` 增两个 op 分支：`scan_equivalent_operators` / `swap_denominator`（照抄 `gradient_dilute` 分支改 op + priority + action_hint） | 极低 | 把最贵学费变成步 7 自动注入 |
| **B** | `ra-pipeline/SKILL.md` 经验库路由表：步 7 增引 `02_signal_patterns.md §12/§13` | 1 行 | 补上文档层断点 |
| **C** | 修 `step7-diagnose.md:98` 的 `signed_power` 建议（降级 + 交叉引用 `brain-how-to-pass-alpha-test` §墙表） | 1 处 | 消除 skill 间冲突 |
| **D** | `KOR.md` 补输入频率根因表；`step2-s0` / D4 增"信息维度新颖度"排序 + valueScore 陷阱提示 | 中 | 选集阶段就避开 prod 墙 |
| **E** | 上表 P2 的 8 条工程坑批量补进 `docs/experience/04_engineering.md`，并同步修正 AGENTS.md 的注入点描述 | 中 | 减少重复踩坑 |

**⚠ 改 skill / 节点的既有纪律**：改完跑 `tools/sync_skills.py`；改 workflow 节点须过
`tools/audit_node_registration.py`（五处同步）；双轨改动须保 `tests/unit/07_docs_skills/test_experience_kb_refs.py` 绿。
