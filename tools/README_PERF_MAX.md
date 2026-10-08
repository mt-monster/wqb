# perf_max — 全闸通过 alpha 的业绩极致优化（零提交）

> **边界声明**：`alpha_booster`（S4）管「卡闸 → 修到通过」；`perf_max` 管「通过 → 闸门保持绿的前提下业绩推到极致」。
> 两者首尾相接、互不重叠。perf_max **只接受 `failed_ra_count == 0` 的 baseline**，卡闸候选请走 alpha_booster / Mode B。

## 三段式用法

```bash
# 1. plan：拉 baseline（或离线 JSON）→ 生成变体梯 + 派发材料
python tools/perf_max.py plan --alpha-id RR6bv6rz --objective fitness
# 离线冒烟：
python tools/perf_max.py plan --baseline-json tracking/USA/candidates/rr6bv6rz_baseline.json

# 2. 派发（复用仓库唯一 REST 客户端，不新增第三套）
python tools/submit_batch.py --spec tracking/USA/perfmax/<stamp>/dispatch_spec.json
python tools/harvest_multisim.py <multisim_id> --json-out harvest.json

# 3. harvest：回填实测指标 + 闸保持判定
python tools/perf_max.py harvest --plan-dir tracking/USA/perfmax/<stamp> --from-harvest harvest.json
# 或逐条：--alpha-ids EQ_SP05=XXXX WIN_HALF_5=YYYY

# 4. report：排名表 + 推荐（写台账默认 dry-run）
python tools/perf_max.py report --plan-dir tracking/USA/perfmax/<stamp> --write-ledger          # dry-run
python tools/perf_max.py report --plan-dir tracking/USA/perfmax/<stamp> --write-ledger --apply  # 真写
```

## 变体梯（按序，每轮 ≤8 条 = multi-sim 硬上限 10 内）

1. **EQ** 等价算子替换（优先原则）：`quantile` ↔ `signed_power(0.5)` ↔ `winsorize` ↔ `normalize(useStd)`
2. **POW** 幂次微调：0.5 / 0.7 / 1.5 / 2.0（>1 凹性提 S/2Y，<1 凸性压中间）
3. **WIN** 窗口微扫（只动**最外层**时序窗口的半/双，TS_OP_WINDOWS 白名单）——`wq-window-valley-break-prod-wall` 同族手法
4. **DECAY** 半/双（cap 512；0/1 留一纪律）
5. **CTRL** `nanHandling=OFF` 对照（隔离强度闸归因）

**禁扫 truncation**（D5 零杠杆实证）。

## 闸保持判定口径（`gate_status`）

- `checks.fail` 空 + `ra_failed_checks` 空
- `turnover ∈ PLATFORM_CHECK_LINES["turnover_range"]`
- 阈值一律引用 `src/wqb/config.py`（GATES_INTERNAL / PLATFORM_CHECK_LINES），本工具与本文档禁复写数字。

## 续跑 / 断点

- `plan.json` 原子写（tmp + `os.replace`）；`harvest --skip-done`（默认）跳过已有 `result` 的变体。
- 表达式级去重（同一 expr 不重复派发）；`op_arity.check_expressions` 自检不过的变体静默剔除并在 `skipped` 记原因。

## 硬规则（继承项目铁律）

- **零提交**：本工具只到「推荐」为止；提交 = `submit_verdict` 预检 → prod/self 终验（`check_correlation refresh=True`，>48h 规则）→ **用户逐次授权**。
- 派发客户端唯一性：只复用 `tools/submit_batch.py`（REST）与 MCP，**勿新增第三套**。
- 429 `CONCURRENT_SIMULATION_LIMIT_EXCEEDED` 退避 ≥90s；发批前三闸（op_arity + 平台算子交叉 + 字段存在性）。
- 挖掘产出即时落 `tools/ledger/mining_ledger.py`（report --write-ledger 是便捷入口，默认 dry-run）。

## 可交付必入 submit_ready（2026-10-08 阶段五）

用户后续从 `submit_ready` 取当日候选比较提交 ⇒ **可交付 alpha 一律入队**。三层保障：

1. **自动入队**：`perf_max.py report` 默认把闸保持变体入队（`--no-queue` 关闭）；`perf_max.py enqueue --plan-dir <dir>` 独立重放入队（补 prod/self 相关性后入）。
2. **漏盘兜底**：`tools/enqueue_sweep.py [--region R] [--dry-run]` 扫本地 alphas/backtest_results，把「is_pass 命中且不在 submit_ready」的补入。最终 gate 以入队判定为准（兄弟 prod 连坐 → DEAD，prod/self 未测 → IS_ONLY）。
3. **平台补录**：平台有、本地无的走 `tools/submit_queue.py add --alpha-id <ID>`（入队后同样打列填充审计）。

**入队铁律**：所有可得字段当场落库（prod/self/towers/themes/2Y/sub/cluster/margin/returns/drawdown/long/short/investability/ra_failed/family/settings/expr），入队后立即跑 `column_fill_audit` 逐列查空——`risk_neutralized_sharpe`/`towers` 是平台真不可得列（raw `pyramids` 对 UNSUBMITTED 恒 None），允许空但必须被看见。`_upsert` ON CONFLICT 对 `family/cluster_test/sub_universe/expr` 用 COALESCE 更新（防首入 None 后旧值锁死）。

## 测试

`tests/unit/10_toolkit_scripts/test_perf_max.py` —— baseline 解析 / 闸保持判定 / 变体梯纪律（禁 truncation、DECAY 封顶、EQ 优先、去重、算子预算）/ 外层剥取三形态 / 窗口微扫括号平衡 / 打分 None 语义 / 原子写续跑 / harvest 映射 / dispatch 分组 / 入队（build_enqueue_record 全字段、只入闸保持、dry-run 回滚）。
`tests/unit/10_toolkit_scripts/test_enqueue_sweep.py` —— 挑可交付、跳已入队、commit/dry-run（fixture SQLite）。
