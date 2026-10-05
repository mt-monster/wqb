# WQ BRAIN Alpha Optimization V1 — 示例与情景卡

> 主 SOP 见 [SKILL.md](SKILL.md)；Mode A 规则见 [reference.md](reference.md)；入场资格见 [`references/mode-b-qualification.md`](references/mode-b-qualification.md)。
> 命令里的 `$WQ_PY` 是 MCP venv 解释器（`python tools/_pyenv.py` 打印其路径）。

## 一、触发示例（用户怎么说 → 应该做什么）

### 示例 1：直接优化请求

用户：

```text
对 JPN alpha id 为 LLbaqEqa 的表达式做优化，region=JPN、delay=1。目标：所有检查 PASS（含 IS_LADDER_SHARPE），PROD 相关性读数可放行。
每轮回测完确认结果已入库，并把本轮 8 槽日志给我。
```

期望行为：

1. 读基线 alpha 并冻结核心字段；确认 JPN 合法设置；
2. **先做资格判定**（`mode_b_qualify.py evaluate`），按结论进 Mode B 或结束；
3. 按 Stage A / B 规划恰好 8 条；
4. 校验层三段（verifier → `ghost-audit` → `wave_gate --batch-type repair`）；
5. `create_multi_simulation` → `harvest_multisim_alphas` → `harvest_multisim_results`；
6. 只对零 FAIL 的候选做 `check_correlation`，读数按 D0-P 处置。

### 示例 2：Stage A 结构轮

用户：「继续优化这个 alpha，但目前 Sharpe 只有 1.1、Fitness 只有 0.7，不要做纯调参。」

期望：本轮定为 Stage A（未过微调闸）；禁止纯参数改动；用去噪 / 冻结 / 正交化 / 相关结构 / 换手控制等结构主题；批大小 8；每条先校验。

### 示例 3：强负信号翻转

用户：「上一轮里有两个表达式 Sharpe 很差但不像噪声，继续做下一轮。」

期望：在上一轮里找 `Sharpe ≤ -1.20` 且 `Fitness ≤ -0.50` 者，标 `CAND_NEG`；下一轮 8 条里至少 2 个翻转版；仍守算子 / 主题 / 校验闸。

### 示例 4：只要严格校验，先别回测

用户：「先不要急着回测，先把这 8 条表达式做严格校验。」

期望：跑校验层三段；只修精确的语法 / 签名 / 关键字 / 逗号 / 括号错误；**不为拿到绿灯而简化策略逻辑**。

### 示例 5：本轮日志块（写在回复里，不写文件）

```text
[2026-03-09 14:32:10] baseline=LLbaqEqa round=3 region=JPN delay=1 wave=<W>
slot=1 alpha_id=AAA Sharpe=1.62 Fitness=1.08 Turnover=0.18 FAIL=none PROD=0.64
slot=2 alpha_id=BBB Sharpe=1.31 Fitness=0.92 Turnover=0.11 FAIL=IS_LADDER_SHARPE
slot=3 alpha_id=CCC Sharpe=-1.28 Fitness=-0.58 Turnover=0.14 FAIL=none tag=CAND_NEG
slot=4 alpha_id=DDD Sharpe=0.97 Fitness=0.61 Turnover=0.43 FAIL=Turnover
next_actions=flip slot3, decorrelate slot6, compress operators for slot4
```

版式可以变，但要保留 8 槽历史。权威副本是 `backtest_results`（已由 harvest 入库）；这块日志只承载**角色与下一步**，S6 回写时并入 `wave_result.key_findings`。

## 二、情景卡

### 卡 OP-1　没过主闸：先判资格，再决定改不改

- **前置状态**：候选 Sharpe 0.90、Fitness 0.55、2Y 1.35，S4 判 FAIL。
- **步骤**
  1. `$WQ_PY tools/mode_b_qualify.py evaluate --region <REGION> --sharpe 0.90 --fitness 0.55 --two-year-sharpe 1.35`；
  2. 预期（内置默认主闸下）：`verdict: bypass`、`bypass: E_2y_strong`、`mode_b_action` = 补短期腿（跨周期正交）或换中性化域提 IS。
- **分支**：2Y 换成 0.90 → `dead_end`（候选级封存，先 `forum_recon` 再 `seal_dead_end`）；2Y 没读数 → `no_qualify`（**不判死**，也不进改进）。
- **产物与落点**：B3 的首选修法 = 上面的 `mode_b_action`；判定输出贴进本轮日志。
- **完成定义**：`result.verdict` 已明确，且下一步动作与它一致。
- **反例**：看到 Sharpe < 1.25 且 Fitness < 0.8 就判死——2Y ≥ 1.2 永不判死（旁路 E）。实际主闸值以 `mode_b_qualify.py show --region <REGION>` 为准，区域可能调过。

### 卡 OP-2　prod 踩线带（0.70–0.75）：只做 1 次结构性尝试

- **前置状态**：某族首探 `check_correlation` 读数 0.72；诊断显示自家 book 相关低（拥挤源在外部池）。
- **步骤**：从 D0-P 允许的两条里选 1 条：① 删腿 / 换广度轴；② `group_neutralize(同信号, sector)` 包裹。→ 校验层三段 → 仿真 → `check_correlation`（`refresh=True`）。
- **分支**：读数 < 0.70 → 按 D0-P 0.60–0.70 行（不扩变体、当天进步 8）；仍 ≥ 0.70 → 家族记 `dead_end`（先 `forum_recon`），换机制 / 换白名单不同数据集。
- **完成定义**：1 次尝试已做完并有读数；不存在第 2 次。
- **反例**：磨 decay / 中性化设置 / 窗口；用 bucket / 门控 / 平滑去压 prod（option8 IV 族在全参数空间实证无效）；镜像稀释；任何两条腿相加。

### 卡 OP-3　已 eligible 的候选卡 TVR 墙：组合腿救援

- **前置状态**：主腿 `eligible`（`main_gate`），turnover 0.82 出界，Mode B 常规改进 3 个周期无效。
- **步骤**
  1. `get_salvage_pool(region=<REGION>, boost_dim="boost_tvr")` → 取 ≤ 2 条辅助腿（必须来自返回条目）；
  2. 取形：卡点映射的第一优先 F6 `ts_target_tvr_hump(信号, target_tvr=0.15)`，备选 F6 `hump` / F3 `trade_when(…, -1)`（形态库 §「卡点 → 形态映射」）；
  3. 8 候选严格批 → 校验层三段 → 仿真 → 收割入库；每条溯源 `combo_rescue_from_<alpha_id>_with_<salvage_id>_<形态>`。
- **分支**：池空 / 全同数据集 / 1–2 轮仍 FAIL → 判死回写（先 `forum_recon`，再 `seal_dead_end`）。
- **完成定义**：候选 `Failed RA == 0`，走下游链；否则已判死回写。
- **反例**：`add(rank(主), rank(辅))` 或任何系数乘法 / 权重网格（闸 5 block）；凭空另造辅助腿。

### 卡 OP-4　prod ≥ 0.75 的「唯一例外」：跨数据集残差化

- **前置状态**：主腿已 `eligible`；prod 读数 0.78（D0-P：本应记 `dead_end`）；salvage 池里有跨数据集辅助腿。
- **步骤**：`get_salvage_pool(region=<REGION>, exclude_dataset=<主信号数据集>)` → F2 `vector_neut(rank(主), rank(辅))` → 校验层三段 → 仿真 → `check_correlation(refresh=True)`。
- **分支**：读数 < 0.70 → 下游链（selfcorr-quick → robustness → submit_verdict）；仍 ≥ 0.70 → 池内换另一条腿**至多 1 次**，再不行 → `dead_end`。
- **完成定义**：有 `refresh=True` 的终验读数。
- **反例**：把辅助腿当被加项；对没有 `eligible` 的候选走本例外（例外的前提就是已过资格判定）；辅助腿走 F1（跨数据集价差被闸 5 拦）。
