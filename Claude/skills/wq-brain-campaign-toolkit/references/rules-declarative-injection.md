# 规则声明式注入契约（2026-10-03 建立）

> 解决「写了规则没人消费」：把规则消费从「调用方为每个 `action.op` 硬编码一个分支」
> 改为「规则自带声明式字段，通用执行器消费」。新增规则**不必再改代码**。
> 守护测试：`tests/unit/07_docs_skills/test_methodology_rules_connectivity.py`。

## 1. 背景：审计发现（2026-10-03）

`config/methodology_rules.json` 23 条 active 规则，实际消费情况：

| 类别 | 条数 | 说明 |
|---|---|---|
| 真正生效 | 4 | `recommend_next_wave` 里有 `action.op` 硬编码分支：`gradient_dilute` / `warn_rnf_drop` / `classify_failure_nature` / `fail_fast_stop` |
| 仅 print | 12 | `build_wave.py:795` 取 strategy 规则后只 `print`，注释写明「不拦截，仅提示」；且无条件全打印 |
| 完全不可达 | 7 | 3 `gate_override` + 1 `field_whitelist` + 2 `diagnosis`（op 无分支）+ 1 `dead_end` 无 `block_pattern` |

两个附加问题：

- **`trigger.condition` 是死字段**：`RuleStore.query()` 只匹配 `region / universe / dataset_type`，
  从不解析自然语言 `condition`。条件写得再精确也不参与匹配。
- **判死拦截是死代码**：`build_wave.py:781` 的 `if pat:` 依赖 `action.block_pattern`，
  而 23 条规则里带 `block_pattern` 的为 **0 条** ⇒ 判死规则一条都拦不掉。

## 2. Schema 扩展（两个可选字段，向后兼容）

存量规则**不加这两个字段也能立即生效**（降级为常驻提示），可逐条补 `when` 升级为精准触发。

### `when` — 结构化触发条件

```json
"when": {"all": [{"fact": "max_prod", "op": ">", "value": 0.7},
                 {"fact": "max_sharpe", "op": ">=", "value": 1.58}]}
```

- 支持 `all` / `any`，或单条子句（`{"fact":..,"op":..,"value":..}`）。
- 算子：`>` `>=` `<` `<=` `==` `!=` `in` `not_in`。
- **事实缺失 ⇒ 判假**（保守：宁可不提示，也不制造噪声）。
- 求值返回 `(matched, gated)`：`when` 缺失 ⇒ `(True, False)` = 命中但**未条件化**。

### `emit` — 覆盖产出文案与优先级

```json
"emit": {"direction": "扫等价算子替换（判定「天花板」前必扫）",
         "action_hint": "冻结骨架只换实现算子，如 signed_power(x,0.5)→quantile(x)",
         "priority": 92}
```

缺省派生规则：

| 字段 | 缺省值 |
|---|---|
| `direction` | `[{type}] {rule_id}` |
| `rationale` | `action.message` |
| `action_hint` | `action.hint` → `action.params` → `op={op}` |
| `priority` | **条件化命中**：`confidence × 100`；**未条件化**：`confidence × 40` |

⇒ 条件化命中（80–95）永远排在常驻提示（30–40）之前，精准建议不会被 24 条噪声淹没。

## 3. 阶段路由

`trigger.phase` 已有取值：`dataset_select` / `wave_design` / `simulate` / `wave_review` / `submit`。

`WIRED_PHASES = {"wave_review"}` 登记**已接入专属注入点的阶段**。
未接入阶段的规则由**步 7 兜底接收**（`fallback_unrouted=True`），保证无孤儿；
接入专属阶段后把该 phase 加进 `WIRED_PHASES` 即可停止兜底。

接入新阶段的方式（约 3 行）：

```python
from _lib import rules as rules_mod
for r in rules_mod.inject_rules(ctx, facts, phase="dataset_select",
                                context={"region": ctx.region}):
    print(f"[rules] {r['direction']} :: {r['action_hint']}")
```

## 4. 步 7 可用事实（facts）

`recommend_next_wave` 当前喂给 `inject_rules` 的事实：

| fact | 含义 |
|---|---|
| `max_sharpe` / `max_prod` | 本波最强 sharpe / 最高 prod_corr |
| `dom_wall` | 主导墙（`SHARPE` / `2Y` / `MARGIN` / `TVR` / `CW` / `PROD` / None） |
| `has_near` / `n_rows` | near 池是否非空 / 结果行数 |
| `verdict` | fail-fast 判定（`RETRY_FIXABLE` / `STOP_STRUCTURAL`） |
| `universe` / `region` | 当前 universe / region |

**尚未接入、需要时才补的 fact**（迁移表里会标注）：
`input_turnover` / `is_event_dataset` / `porting` / `reusing_legacy` / `has_candidates` /
`is_multi_dataset` / `two_year_missing`。

## 5. 迁移表（23 条 → 建议 when / priority）

✅ = 已迁移；ⓘ = 需先补 fact 才能条件化；— = 保持常驻提示（断言类/铁律类，常驻合理）

| # | rule_id | type | phase | 建议 when | prio | 备注 |
|---|---|---|---|---|---|---|
| — | `equivalent_operator_substitution_v1` | strategy | — | `max_sharpe>=1.0` ∧ `max_prod>0.6` | 92 | ✅ **已迁移** |
| — | `denominator_is_the_real_self_wall_variable_v1` | strategy | — | `max_prod>0.7` | 88 | ✅ **已迁移** |
| 1 | `prod_wall_dilution_v1` | strategy | wave_review | `max_sharpe>=1.0` ∧ `max_prod>0.7` | 90 | 已有专属分支，补 when 防重复注入时被降权 |
| 2 | `concentrated_weight_is_data_quality_not_params_v1` | strategy | wave_review | `dom_wall == "CW"` | 85 | |
| 3 | `rnf_dilution_tradeoff_v1` | diagnosis | wave_review | ⓘ 需 `dilution_applied` | 50 | 现有分支已嵌套在稀释建议内 |
| 4 | `metrics_cache_2y_fallback_bug` | gate_override | — | ⓘ 需 `two_year_missing` | 95 | 实为 bug 修复条目，建议改由 metrics 层消费 |
| 5 | `gate_cross_dataset_split_v1` | gate_override | — | ⓘ 需 `is_multi_dataset` | 75 | |
| 6 | `settings_wave_lock_v1` | gate_override | wave_design | ⓘ 需 `wave_launch` | 90 | message 称已落地 pipeline，建议核对后标 deprecated |
| 7 | `model_category_rich_v1` | field_whitelist | dataset_select | ⓘ 需 `category` | 85 | 接入选集阶段后移出兜底 |
| 8 | `zero_competition_no_signal_v1` | dead_end | dataset_select | ⓘ 需 `alpha_count` | 85 | **另需补 `block_pattern` 才能真拦截** |
| 9 | `pyramid_quota_v1` | strategy | dataset_select | ⓘ 需 `n_non_model` | 90 | |
| 10 | `win_replay_slow_fast_v1` | strategy | wave_design | ⓘ 需 `has_win` | 90 | |
| 11 | `prod_first_skeleton_v1` | strategy | simulate | ⓘ 需 `batch_index` | 85 | |
| 12 | `failure_nature_classifier_v1` | diagnosis | wave_review | — | 80 | 已由 `classify_failure` 消费，保持常驻 |
| 13 | `no_effort_seven_signals_v1` | dead_end | wave_review | — | 75 | 已由 fail-fast 消费；**另需 `block_pattern`** |
| 14 | `sub_universe_ratio_gate_v1` | diagnosis | wave_review | `dom_wall == "SUB"` | 90 | ★ 0.571 比值律 |
| 15 | `pyramid_lighting_platform_only_v1` | diagnosis | wave_review | — | 90 | 断言类（唯一权威=平台），常驻合理 |
| 16 | `same_family_consecutive_submit_v1` | strategy | submit | ⓘ 需 `has_candidates` | 85 | 接入步 8 后移出兜底 |
| 17 | `mixed_signal_leg_ban_v1` | strategy | wave_design | — | 95 | **铁律**，常驻最高优先级合理 |
| 18 | `region_stop_invest_v1` | diagnosis | dataset_select | ⓘ 需 `region_yield` | 85 | |
| 19 | `sparse_field_long_window_v1` | strategy | — | ⓘ 需 `input_turnover` / `is_event_dataset` | 85 | 判别标准是输入频率非 coverage |
| 20 | `cross_region_port_settings_alignment_v1` | strategy | wave_design | ⓘ 需 `porting` | 90 | |
| 21 | `multileg_strength_not_decomposable_v1` | strategy | dataset_select | ⓘ 需 `reusing_legacy` | 88 | |

**优先级排序建议**：铁律/安全类（95）> 破墙杠杆类（88–92）> 诊断类（75–90）> 常驻提示（30–40）。

## 6. 遗留项

1. **判死拦截仍不生效**：`zero_competition_no_signal_v1` / `no_effort_seven_signals_v1`
   需补 `action.block_pattern`（表达式级正则）或改为声明式 `block` 结构；
   否则 `build_wave.py:781` 的 `if pat:` 永远是死分支。**在补齐之前，不要以为判死已生效。**
2. **`trigger.condition` 与 `when` 并存**：`condition` 保留作人读文档，
   后续可加守护测试断言两者语义不冲突（暂未做）。
3. **步 7 兜底不是终态**：`dataset_select` / `wave_design` / `simulate` / `submit`
   四类规则目前都靠步 7 兜底露面，时机偏晚。应按 §3 接入各自阶段并登记 `WIRED_PHASES`。
