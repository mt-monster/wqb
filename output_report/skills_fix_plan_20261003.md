# Skills / 流程完整修正方案（待决策）

> 2026-10-03。诊断依据见 [`skills_review_20261003.md`](skills_review_20261003.md)。
> **本文只出方案，未再动代码。** 每项标注：改动面 / 风险 / 验收 / 建议。
> 你逐条拍板后我再动手。

---

## 〇、当前状态：已动过的地方（可回退）

在你喊停之前，我已经做了以下改动。**全部可回退**，回退命令见文末。

| # | 文件 | 改动 | 状态 |
|---|---|---|---|
| 1 | `Claude/skills/wq-brain-campaign-toolkit/scripts/_lib/rules.py` | 新增声明式通用注入：`evaluate_when()` / `inject_rules()` / `WIRED_PHASES`；`recommend_next_wave` 末尾接入兜底注入 | 纯新增，不改既有分支行为 |
| 2 | `.../config/methodology_rules.json` | 给 2 条星标规则加 `when` + `emit` | 加字段，不改原值 |
| 3 | `tests/unit/07_docs_skills/test_methodology_rules_connectivity.py` | 新建守护测试（10 例，含反向负例） | 全绿 |
| 4 | `.../references/rules-declarative-injection.md` | 新建契约文档（schema + 迁移表） | — |
| 5 | `output_report/skills_review_20261003.md` | Review 报告 | — |
| 6 | `.workbuddy/memory/MEMORY.md` | 超限精简（9.4k → 3.2k 字符） | 系统强制动作 |

**验证结果**：24/24 active 规则露面、孤儿 0；两条星标规则以 GATED 优先级 92/88 排最前。

| 测试范围 | 结果 |
|---|---|
| `tests/unit/07_docs_skills`（新增 10 + 既有 10） | ✅ 20 passed |
| `tests/unit/06_wave_pipeline` | ✅ 全绿 |
| `02_workflow` 中引用 `_lib.rules` 的两个文件 | ✅ 3 passed |

⚠ **待确认**：`06+07+02` 合并跑时见 3 个 `F`，但三个范围分开跑均全绿，
且 `02_workflow` 单次跑 10 分钟被 timeout 截断（只到 ~50%）。
这 3 个 `F` 落在未跑完的 `02_workflow` 后段，**尚未定位**。
已知混淆因素：safe-delete 钩子会造成环境性假红（记忆 §4）。
⇒ 定位这 3 个失败列为**待办**，建议在你拍板后与第 1 批改动一并处理。

---

## 一、问题全景（一张图）

```
写规则 ──> 机器层 rules.json ──> ??? ──> 消费点
                                  ↑
                          断在这里：
                          ① op 无硬编码分支（19/23）
                          ② trigger.condition 从不解析（死字段）
                          ③ phase 未接入专属阶段（4 类靠步7兜底）
                          ④ block_pattern 全为 0（判死永不拦截）
```

**根因不是"规则写得少"，是"消费模型错了"**：按 `action.op` 硬编码分支 ⇒ 每条新规则都要改代码 ⇒ 漏改就成孤儿。

---

## 二、方案主体：四层，从"读得到"到"有价值"

### L1 · 读得到 —— 声明式通用注入 ✅ 已实现

| 项 | 内容 |
|---|---|
| 改动面 | `_lib/rules.py` 新增 ~110 行；`recommend_next_wave` 末尾 ~15 行 |
| 风险 | 低。纯新增；既有 4 个 op 分支行为不变（靠 `source_rule` 去重） |
| 验收 | 24/24 露面、孤儿 0（守护测试已断言） |
| 建议 | **保留** |

关键设计：规则自带 `when`（结构化条件）+ `emit`（文案/优先级），通用执行器消费 ⇒ **新增规则不必再改代码**。

### L2 · 有价值 —— 21 条规则补 `when` / `emit`（未做）

现状：只有 2 条条件化（92/88 GATED），其余 22 条是常驻提示（优先级 30–40）。
**排序已保证精准建议不被淹没，但条件化比例太低。**

| 批次 | 条数 | 内容 | 前置 | 建议 |
|---|---|---|---|---|
| L2-a | 6 | 可直接用现有 facts 条件化：`prod_wall_dilution`(dom_wall/max_prod)、`concentrated_weight`(dom_wall=="CW")、`sub_universe_ratio_gate`(dom_wall=="SUB")、`same_family_consecutive_submit`、`failure_nature_classifier`、`pyramid_lighting` | 无 | **做**（半天） |
| L2-b | 8 | 需先补 facts 才能条件化：`input_turnover`、`is_event_dataset`、`porting`、`reusing_legacy`、`has_candidates`、`is_multi_dataset`、`two_year_missing`、`alpha_count` | 需在 `recommend_next_wave` 里 plumb 新事实 | **做**（1–2 天） |
| L2-c | 8 | 断言类/铁律类，保持常驻合理：`mixed_signal_leg_ban`(95)、`pyramid_quota`、`win_replay`、`prod_first_skeleton`、`zero_competition`、`region_stop_invest`、`model_category_rich`、`no_effort_seven_signals` | — | **只调优先级，不条件化** |

> 迁移表（逐条建议 when / priority）见
> [`rules-declarative-injection.md`](../Claude/skills/wq-brain-campaign-toolkit/references/rules-declarative-injection.md) §5。

### L3 · 分阶段路由（未做）

现状：`dataset_select` / `wave_design` / `simulate` / `submit` 四类规则**全靠步 7 兜底露面**，时机偏晚。

| 阶段 | 接入点 | 改法 | 建议 |
|---|---|---|---|
| `dataset_select` | `score_datasets.py` / `build_wave` 选波前 | 3 行 `inject_rules(phase="dataset_select")` + 登记 `WIRED_PHASES` | **做** |
| `wave_design` | `build_wave` | 同上 | **做** |
| `simulate` | `pipeline.py` 发批前 | 同上 | **做** |
| `submit` | `submit_verdict.py` / 步 8 | 同上 | **做**（价值最高：同族连提那条） |

每个阶段约 3 行 + 1 个 `WIRED_PHASES` 登记。

### L4 · 不退化（部分已做）

| 项 | 状态 | 建议 |
|---|---|---|
| 连通性守护（孤儿=0） | ✅ 已做 | 保留 |
| 反向负例（条件不成立不得多出规则） | ✅ 已做 | 保留 |
| `when` / `trigger.condition` 语义一致性守护 | ❌ 未做 | **可选**：断言两者不冲突 |
| `block_pattern` 缺失告警 | ❌ 未做 | **做**（见 P1-1） |

---

## 三、Review 发现的其他修正项（未动）

### P1 · 必须修（有实际危害）

| # | 项 | 改动面 | 风险 | 建议 |
|---|---|---|---|---|
| 1 | **判死拦截是死代码**：`build_wave.py:781` 的 `if pat:` 依赖 `action.block_pattern`，而 23 条规则里 **0 条**有该字段 ⇒ 判死规则一条都拦不掉 | 给 `zero_competition_no_signal_v1` / `no_effort_seven_signals_v1` 补 `block_pattern`（正则），或改成声明式 `block` 结构；否则删掉死分支 | 中（正则可能误伤） | **做**。⚠ 在此之前不要以为判死已生效 |
| 2 | **`step7-diagnose.md:98` 与 `brain-how-to-pass-alpha-test:39` 冲突**：前者推荐 `signed_power` 压尾破比值闸，后者说它正是 `LOW_INVESTABILITY_CONSTRAINED_SHARPE` 成因、应换 `quantile` | 1 处：给前者加反向引用 + 降级措辞 | 低 | **做** |
| 3 | **KOR profile 缺最根本约束**：「输入频率二选一」（低频 `accum_*` 出 2Y / 高频 `stk_*` 出 IS） | `references/regions/KOR.md` 加一张表 | 低 | **做** |
| 4 | **选集排序准则与教训相反**：D4/step2-s0 按 coverage/alphaCount/valueScore 排，但记忆说「稀疏覆盖高 valueScore 是陷阱」；缺「信息维度是否已在 prod book」排序 | `step2-s0.md` + `decision-table.md` D4 | 中（影响选集） | **做，但单独讨论** |
| 5 | **文档层断点**：步 7 路由表只指 `05_antipatterns.md`，而等价算子替换在 `02_signal_patterns.md §12/§13` | `ra-pipeline/SKILL.md` 经验库表加 1 行 | 低 | **做** |

### P2 · 工程坑补文档（未动）

| # | 内容 | 建议 |
|---|---|---|
| 1 | `tools/ind_sim_submit.py` 未进任何 skill | 补 |
| 2 | `submit_batch.py` 固定 nanHandling/maxTrade ⇒ 批次与 MCP 批不可比 | 补 |
| 3 | nanHandling/maxTrade 是强度闸（IND 行为族 S 2.19→0.46） | 补 |
| 4 | 差集法 `/data-sets`（不带 limit/offset 返回 0 条、429 退避、category 是 dict） | 补 |
| 5 | `ts_backfill` 不支持 event inputs（MATRIX 实为 VECTOR/event ⇒ `vec_avg`） | 补 |
| 6 | ledger 脏行 `Extra data`（`json.loads` 全表挂） | 补 |
| 7 | multisim 卡死判据（progress 0.1 停滞 >10min 且 child=0 ⇒ 重发） | 补 |
| 8 | **AGENTS.md 过时**：称 `RuleStore.query()` 在 gate/build_wave/pipeline/review_wave 四处强制注入，实际 gate 只用 contract、build_wave 只 apply dead_end | 补 |

落点：`docs/experience/04_engineering.md`（**双轨纪律：同步 `methodology_rules.json` 一侧**）。

---

## 四、建议执行顺序

```
第 1 批（低风险、高价值，半天）
  P1-2 step7 signed_power 冲突   ·  P1-5 步7 路由表补 §12/§13
  P1-3 KOR profile 补输入频率    ·  L2-a 6 条规则条件化

第 2 批（需要设计决策，1–2 天）
  P1-1 block_pattern / 判死拦截  ·  L3 四个阶段接入
  L2-b 补 facts + 8 条条件化

第 3 批（影响面大，需单独讨论）
  P1-4 选集排序准则              ·  P2 工程坑批量补文档

持续
  L4 守护测试随每批扩充
```

---

## 五、回退方式

若决定不采纳第 1–4 项（L1 引擎部分），回退：

```bash
# 1) rules.py 回退到改动前
git diff -- Claude/skills/wq-brain-campaign-toolkit/scripts/_lib/rules.py   # 先看清差异
# 2) methodology_rules.json 去掉新增的 when / emit 两个字段块
# 3) 删除新增文件
#    Claude/skills/wq-brain-campaign-toolkit/references/rules-declarative-injection.md
#    tests/unit/07_docs_skills/test_methodology_rules_connectivity.py
#    logs/_tmp_verify_rules_inject.py
```

⚠ 注意：本仓库当前有 **364 个未提交改动**（非本次产生），`git checkout` 类操作务必限定单文件，
不要用 `git reset --hard` 或批量回退。

---

## 六、改 skill / 节点的既有纪律（动手前必读）

- 改完 skill 跑 `tools/sync_skills.py`。
- 改 workflow 节点须过 `tools/audit_node_registration.py`（五处同步）。
- 双轨改动保 `tests/unit/07_docs_skills/test_experience_kb_refs.py` 绿。
- 全量 pytest 红灯**先排除 safe-delete 钩子**（环境问题，非代码）。
