# 四层结构性多样性保证 — Path1 修复 + 回归验证 + 批量扩展报告

**日期**：2026-08-25
**区域**：USA（event_return_model 回归；白名单 36 数据集横向）
**范围**：ra-pipeline S-PRE→S3（dryrun，零回测配额、零提交）

---

## 0. 背景与问题

美国线 S2→S3 发现：GEM 在无 LLM（--ideas-file 直实现）时只产 `ts_backfill / ts_delta / multiply / subtract` 等单调算子，**缺少 `group_*` / `ts_arg_*` 类算子**。这导致选波后的波次在闸6（批级多样性）被 `diversity_gate.pass=false` 拦截，S4 进不去。

Path1 修复思路：不让"AI 自觉传 ideas 文件"来保证多样性（不可靠），而是把多样性从**软约束**升级为**结构性保证**——从"GEM 自己记得用多样算子"改为"管道强制注入 + 闸门自愈"。

---

## 1. 四层结构性保证（改造内容）

| 层 | 机制 | 载体 | 状态 |
|---|---|---|---|
| ① | `factor_templates` 存**骨架**（模板+角色占位符 `{F1}`/`{F2}`），不存锚点字段具体表达式 | `operator_coverage.py` `plan_coverage_wave` 签发 | ✅ 已就绪（签发的契约 222810 全部 12 算子 `skeleton=true, template=true`） |
| ② | `build_wave` 消费活跃契约时，用**当前数据集 S1 catalog 角色池**实例化骨架，注入候选池头部（dead_end 排除/去重天然防护） | `build_wave.py` 契约注入段 | ✅ 本次补完 |
| ③ | GEM 生成层 `--require-operators` mandate + 补注（**best-effort 次保障**，非权威；权威保证在 ②） | `run_pipeline.py` + `headless_runner/run.py` 转发 | ✅ 已就绪 |
| ④ | `build_wave` 选波后若命中契约 `required_operators` 数 < `per_batch_min_operators`，**自愈补齐**（限一轮骨架实例化） | `build_wave.py` ④ 段 | ✅ 本次补完 |

> 说明：①③ 在会话早期已实现，本次仅补 ②④（契约注入实例化 + 选波自愈）；`run.py` 的 `--require-operators`/`--require-count` 转发此前已就位。

---

## 2. 回归验证（零手工 ideas）

**目标**：证明 GEM 自包含生成（不传任何 ideas 文件）也能结构性过多样性闸。

### 2.1 GEM 自包含生成的"裸"多样性（对照组）
GEM 以 `--require-operators "ts_arg_max,ts_arg_min,ts_av_diff" --require-count 2` 自含生成 **22 条**表达式落 `s2_event_return_model_d1`：

| 指标 | 结果 |
|---|---|
| 总表达式 | 22 |
| 命中 `ts_arg_max` | 4 |
| 命中 `ts_av_diff` | 2 |
| 命中任一 required 算子 | **仅 6/22（27%）** |

➡ 证明：GEM 自包含生成**本身不足**以保证多样性（73% 仍单调算子）。若无结构性保证，闸6 必 FAIL。

### 2.2 build-wave（契约注入 ②）
命令（**无 --file / 无 --ideas-file**，纯 DB 读取 22 条）：
```
campaign.py --campaign-dir tracking/USA build-wave --from-db \
  --dataset event_return_model --wave reg_event01
```
结果：
- 活跃契约 `explore_contract_USA_20260825_222810_719557`（required=12 算子，全部带 skeleton）
- **[coverage] 注入契约 12 个因子（骨架实例化 12，legacy 回退 0）** ← 层②生效
- `input=34`（22 GEM + 12 注入），`selected=15`
- 波内算子分布含 `group_backfill/cartesian_product/count/mean/neutralize/scale/std_dev/sum/zscore`（9 个 group 类）+ `ts_arg_max/ts_arg_min/ts_av_diff`（3 个 ts 类）+ `rank>multiply/subtract/ts_av_diff`
- 层④自愈**未触发**（层②注入已使命中数远超 `per_batch_min_operators=2`，属预期——层④是兜底网）

### 2.3 gate（闸6 批级多样性）
命令：
```
campaign.py --campaign-dir tracking/USA gate --from-db \
  --wave reg_event01 --dataset event_return_model
```
为排除 idempotent replay（digest 已消费导致 `applied=false`），已将测试契约 `consumed_batches` 清零后重跑，得到**干净结果**：

| 字段 | 值 |
|---|---|
| `all_pass` | **True** |
| `total` / `passed` | 15 / 15 |
| `diversity_gate.applied` | **True**（闸真实评估了契约） |
| `diversity_gate.pass` | **True** |
| `diversity_gate.consumed` | **True**（契约消费回写，幂等） |
| `diversity_gate.issues` | `[]` |

➡ **结论**：零手工 ideas 下，层②契约注入使最终波自动满足 `required_operators` 阈值，闸6 评估并 PASS。结构性保证成立。

> 备注：首次 reg_event01 闸门运行已 `applied=true` 并消费（consumed 6→7）；第二次 summary 抽取重跑因 digest 已消费显示 `applied=false`（幂等 replay，非失败）。清零后重跑即获上表干净结果。

---

## 3. 横向批量验证（Path1 扩展性）

对 S0 白名单 **36 个数据集**跑 S1(scan-fields)→S2(GEM v2 ideas 含 ts_arg 概念)→S3(build-wave+gate)，断点续跑 + 原子 checkpoint。

| 指标 | 结果 |
|---|---|
| 总数据集 | 36 |
| `status=done` | **35** |
| `gate_all_pass=True` | **35** |
| `diversity_pass=True` | **35** |
| 失败 | 1（`pattern_scores`：`gate_parse_fail`，闸门 JSON 解析异常 + 字段前缀问题，**非多样性失败**） |

排除的 4 个 dead_end 数据集（S-PRE 纪律）：`ai_news_scores / earningscall_embed / multifactor_return_pred / news_sentiment_dl`。

➡ Path1 修复在 USA 白名单具备横向扩展性：除 1 个闸门解析 bug（与多样性无关）外，35/36 全绿。

---

## 4. 结论

1. **GEM 自包含生成不足以保证多样性**（22 条仅 6 条命中 required 算子），旧的"传文件靠 AI 自觉"路径确实不可靠。
2. **四层结构性保证成立**：①骨架入库 + ②消费时按当前数据集实例化注入 + ③GEM 层 mandate + ④选波自愈，使"零手工 ideas"的波次也能自动过多样性闸（reg_event01：`all_pass=True, 15/15, diversity applied+pass+consumed`）。
3. **横向扩展可行**：36 数据集 35 绿，唯一失败为闸门 JSON 解析 bug（与多样性机制无关，可单列修复）。
4. 全部 dryrun **零回测配额、零提交**，仅做结构验证。

---

## 5. 待办 / 后续

- [ ] `pattern_scores` 闸门 JSON 解析异常独立排查（与本次多样性改造解耦）。
- [ ] 可选：层④自愈的端到端演示（构造 GEM+注入仍欠命中场景，验证自愈补齐触发并过闸）。
- [x] 测试契约 `consumed_batches` 复位（本轮重置为 0 并重跑 `reg_event02` 通过；**注：重置时发现其曾达 10/10 过期**，见 §6.3）。

---

## 6. 本轮优化落地（2026-08-25 续）

针对"多样性判定只认算子名"与"GEM ③ 命中率 27%"两项，已实施修复。

### 6.1 修复1：多样性判定 (算子,字段) 组合去重
**文件**：`wq-brain-campaign-toolkit/scripts/gate.py` `check_batch_diversity`
**原问题**：`op_hits` 只数"用了 required 算子的表达式条数"，两条 `group_neutralize(returns)` 被误判为 2 份多样性。
**新逻辑**：
- 对每个含 required 算子的表达式，用 `_op_call` 扁平检测算子 + `_leaf`（**词边界 `\b` + 负向先行 `(?!\s*\()`，杜绝把算子名截短当字段**）提取叶子字段；
- 按 `(算子, 字段)` 互异组合计数，`op_hits = len(combos)`；`need` 语义由"表达式条数"升级为"互异 (算子,字段) 组合数"。
- 附：可选**结构性冗余粗筛**（非阻断 WARN）——两条表达式的 (算子,字段) 组合集完全相同即打印 `[DIVERSITY-WARN]`，无需收益数据即可捕获近重复，避免浪费配额。

**验证**（隔离单测 + 真实波）：

| 场景 | 结果 |
|---|---|
| A 两条 `group_neutralize(returns)` 同字段 | `op_hits=1 < 2` → **正确 FAIL**（修复前误 PASS） |
| B 异字段 / C 嵌套+异字段 | PASS |
| D 两条完全同构表达式 | 打印 WARN 但 `FAIL_issues=0`（非阻断） |
| 真实波 `reg_event02`（重置契约消费后） | `all_pass=True, 8/8, diversity applied+pass+consumed=True, issues=[]` |

### 6.2 修复2：明确"② 为主、③ 为辅"的分工
**事实**：③ 实际含两部分——prompt mandate（软，仅 27% 命中）+ 行级补注 top-up（仅对 `_shapes` 已定义且绑定池非空的算子成立，且只补到 `require_count` 条）。真正的全量结构性保证在 **②（build_wave 契约注入：12 算子全池 + 全数据集角色池）**。原注释把 ③ 叫"硬保证"是误导。
**落点修改**：
- `run_pipeline.py` prompt mandate：由 "This is a hard requirement, not a suggestion." 改为明示 **best-effort**，并指出权威保证是 build_wave 契约注入（②）。
- `run_pipeline.py` `--require-operators` argparse help：去掉 "(operator diversity hard guarantee)" 误导。
- `run_pipeline.py` ③补注注释：明确"次保障，不可替代 ②"。
- `operator_coverage.py` ①骨架签发注释：标明"layer ② 是多样性闸的主结构性保证"。

### 6.3 旁证：契约过期 = 静默 fail-open（P0-2 实证）
重置 `reg_event02` 消费时发现 USA 契约 `consumed_batches` 已是 **10/10（过期）**。这正是上轮 P0-2 预警的真实风险：契约耗尽后 `check_batch_diversity` 直接 `return [], None`，多样性闸**静默 vacuous 通过、不再真正检查**。已复位至 0 并重跑通过。→ **P0-2（过期 fail-closed + 自动续约）应优先排期**。

---

## 7. P0-2 修复落地（2026-08-25 收尾）：契约过期 FAIL-CLOSED + 自动续约

### 7.1 根因
`get_active_contract`（`_lib/rules.py:499`）在 `len(consumed_batches) >= expires_after_batches` 时直接 `return None`。
gate `check_batch_diversity` 拿到 `None` 后走"无契约"分支 → `return [], None` → **多样性闸静默 vacuous 通过**，
四层保证在无人察觉下悄悄失效（§6.3 已实证：真实跑出 10/10 过期态）。

### 7.2 修复设计
1. **`_lib/rules.py` 新增 `get_contract_expiry_state(ctx, batch_type)`**：三态判定，返回
   `("none", None)` / `("expired", act)` / `("active", act)`，把"过期"与"缺失"区分开。
2. **`_lib/rules.py` 新增 `renew_contract(ctx, expired_act)`**：按过期契约的**同款参数**
   （required_operators / skeleton_quota / per_batch_min / exempt / factor_templates）调用既有
   `issue_contract` 签发新契约（consumed 清零），并自动 deprecate 旧契约（单活跃契约原则）。
3. **`gate.py` `check_batch_diversity` 改用三态判定**：
   - `expired` → **FAIL-CLOSED**：返回 `[DIVERSITY-EXPIRED] ... 保证已静默失效；已自动续约新契约 <rid>，请重跑闸门按新契约校验本批`，`consume_ref=None`（阻断提交）+ 调用 `renew_contract`。
   - `active` → 正常校验（含 digest 幂等 replay 保护）。
   - `none` → 维持现状（**P0-3 缺失契约亦应 fail-closed，待修**）。
   - 台账旧路径（`diversity_audit_latest.next_round_injections`）过期同样转 FAIL-CLOSED。
4. `gate.py` 模块文档"过期自动失效"改为"过期 FAIL-CLOSED 并自动续约"。

### 7.3 验证（隔离单测 + 真实波端到端）

| 场景 | 结果 |
|---|---|
| 单测 active（consumed=0） | 正常校验，`ref={'digest','rule_id'}`，**不触发续约** |
| 单测 expired（consumed=10/10） | `issues=[DIVERSITY-EXPIRED...]`、`ref=None`（阻断）、**续约被调用且沿用相同 required_ops** |
| 单测 none | 维持原行为 `[]` / `None`，**不续约** |
| 真实波 `reg_event02` 置过期后跑 gate | `all_pass=False`、多样性 `pass=False`、`issues=[DIVERSITY-EXPIRED...已自动续约 explore_contract_USA_20260825_231235_769479]` |
| 续约后重跑 gate | 新契约 `status=active, consumed=0/10, ft=Y`、旧 4 个 `deprecated`；`all_pass=True, 8/8, diversity.pass=True, consumed=True, issues=[]` |

**结论**：P0-2 已闭环——过期契约不再静默放过，而是阻断提交并自动续约；操作员只需重跑闸门即按新契约合法放行。全部 dryrun 零回测配额、零提交。

### 7.4 遗留
- **P0-3**（缺失契约 = 静默 fail-open）尚未修：`none` 态当前仍 `return [], None` 放行。建议补齐为"required 契约缺失 → 拒绝提交 + 显式告警"。
- 修复引入的副作用：gate 跑过期契约时会**写库签发新契约**（与既有的 `consume_contract` 写库一致，已 try/except 兜底）。
