# op-min：`leadbAKA` 双目标优化报告（2026-11-11 19:4x–20:0x）

> **只挖不提交**，本轮零提交。提交权归用户点名。

## 0 结论

| 目标 | 结果 |
|---|---|
| **A 推指标到全闸通过** | ✅ **达成**：`LOW_FITNESS` 0.96 FAIL → **1.03 PASS**；`submit_gate passed=true` / `failed_any=0` / `hard_gate_warns=[]` |
| **B 算子压到最少** | ✅ **13 → 9 ops**（−3 零损失变量合并 + −1 删冗余平滑）；9 是最小可行集 |
| **可提交？** | ✅ **硬闸全绿**：prod **0.6740** < 0.7、self **0.2393** < 0.7、ΔS **+0.05** ≥ 0。前置：补三问、refresh prod、稳健软标记复核 |

**交付件 `88NbAJnl`**
```
a = ts_mean(overall_sentiment_score, 66); b = subtract(1, likelihood_of_neutral_tone);
c = ts_mean(b, 66);
group_neutralize(ts_zscore(multiply(a, add(c, subtract(1, ts_corr(a, c, 252)))), 378), industry)
```

> 与上一轮 `1YWkN1Q6` 的对照很关键：那颗 3 ops 全闸 PASS 却 **prod 0.7998 判死**；本颗 9 ops 却 **prod 0.674 活**。
> ⇒ **算子数不是唯一目标，prod 才是硬闸**；`ts_corr` 背离腿是把 prod 从基线 0.8078 拉下来的关键，不能为省算子而删。

---

## 1 起始状态

| 项 | 值 |
|---|---|
| id / 状态 | `leadbAKA` / UNSUBMITTED REGULAR |
| settings | EUR / TOP2500 / D1 / decay 1 / MARKET / truncation 0.05 / nanHandling ON |
| 原式 | `ts_decay_linear(group_neutralize(ts_zscore(multiply(ts_mean(overall_sentiment_score,66),add(ts_mean(subtract(1,likelihood_of_neutral_tone),66),subtract(1,ts_corr(...)))),252), industry), 11)` |
| operatorCount | **13**（ts_mean×4、subtract×3、ts_decay_linear / group_neutralize / ts_zscore / multiply / add / ts_corr 各 1） |
| 指标 | S 1.67 PASS｜**F 0.96 FAIL**｜2Y 1.66 PASS｜sub 1.32/0.87 PASS｜CLUSTER 1.24/1.58 WARNING｜TO 0.0683 |
| **prod** | **0.6713 PASS**（`results/prod_wait_leadbAKA.json` @19:38 + 平台复检 `passes_check=true`） |
| 字段 | 两个字段同属 `earnings_sent_matrix`（Global Earnings Call Sentiment Matrix），coverage 0.5062 |
| 塔 | `EUR/D1/EARNINGS` ×1.2 |
| 背景 | `results/notes_cu_cx.md`：本轮「情感 ×（确定性 + 背离）」组合里结构最健康的一颗；基线 `A1xjLLbX` 5 ops / S 1.74 / F 1.07 但 **prod 0.8078 卡墙** |

**缺口**：F +0.04（唯一 FAIL）｜CLUSTER +0.34（WARNING，非 FAIL）｜算子 13 ≥ 复杂度闸 10 ⇒ 按 skill 例外条款 **先压缩再推指标**。

---

## 2 实验（2 批 / 12 条 FULL 仿真）

| 批 | sim id | 内容 | 产出 |
|---|---|---|---|
| A0 | `4eBtpMbkX4mJ91LnQK4LuTd` | 2 条：变量合并（零损失）、变量合并 + 删 `ts_decay_linear` | 13→10→9 ops，F 过闸 |
| B | `aNbclgKi4Li8VzcJBDJ4Du` | 10 条：`ts_zscore` 窗口 378/504/576/630/672/756 + 3 处消融 + `ts_corr` 窗口 504 | 9 ops 最小可行集；prod 择优 |

本地零成本：`op_count.py`、`plan.py`、`scan.py --json` 三通道、`operator_coverage_audit.py --checklist` 逐类过审 84 个 REGULAR 算子；2 条签核写入 `results/op_coverage_signoff.jsonl`。

---

## 3 五条实证

### ① 重复子式变量合并：13 → 10 ops，指标逐位不变

原式里 `ts_mean(overall_sentiment_score,66)` ×2、`ts_mean(subtract(1,likelihood_of_neutral_tone),66)` ×2、内层 `subtract(1,likelihood_of_neutral_tone)` ×2。
用 FASTEXPR 单行变量赋值 `a / b / c` 合并后 → `O0WOvdld`：**10 ops**，S 1.67 / F 0.96 / TO 0.0683 / 2Y 1.66 / sub 1.32 / CL 1.24 **全部逐位相同**。
⇒ 验证了 skill ④ 第 0 步：**赋值本身不计数，重复调用才计数**；单行分号写法平台 201 接受（`--path` 按行读，多行会破坏解析，必须用单行）。

### ② 删 `ts_decay_linear`：10 → 9 ops，顺带修好 F

| 版本 | ops | S | F | 2Y | sub | CL | prod |
|---|---:|---:|---:|---:|---:|---:|---:|
| 原式 | 13 | 1.67 | 0.96 FAIL | 1.66 | 1.32 | 1.24 | 0.6713 |
| `O0WOvdld` 变量合并 | 10 | 1.67 | 0.96 FAIL | 1.66 | 1.32 | 1.24 | — |
| `N1P0odXg` 合并+删平滑 | **9** | **1.74** | **1.01 PASS** | **1.88** | 1.33 | 1.16 | 0.6964 |

再次印证上一轮同数据集实证与 skill 禁用表：**`ts_decay_linear` 在累积型信号上零和**（降 TO 同时削 alpha）。注意 prod 从 0.6713 升到 **0.6964（余量仅 0.0036）** ⇒ 删平滑改善指标却吃掉 prod 安全边际，必须复检。

### ③ `ts_zscore` 窗口：提 2Y/sub，但**对 CLUSTER 无效**（与上一轮相反）

| W | id | S | F | 2Y | sub | CLUSTER | prod |
|---:|---|---:|---:|---:|---:|---:|---:|
| 252 | `N1P0odXg` | 1.74 | 1.01 | 1.88 | 1.33 | 1.16 | 0.6964 |
| **378** | **`88NbAJnl`** | **1.74** | **1.03** | **1.91** | **1.48** | **1.26** | **0.6740** |
| 504 | `j2avLGg5` | 1.70 | 1.00 | 1.95 | 1.40 | 1.21 | — |
| 576 | `vRA80Gma` | 1.68 | 0.99 | 1.99 | 1.39 | 1.19 | — |
| 630 | `vRA80Gmv` | 1.68 | 0.99 | 2.02 | 1.38 | 1.14 | — |
| 672 | `rK7YkGW9` | 1.69 | 1.00 | 2.04 | 1.39 | 1.16 | — |
| 756 | `P05Nez1L` | 1.72 | 1.03 | **2.05** | 1.42 | 1.21 | 0.6942 |

上一轮 3-ops 版 CLUSTER 随窗口单调升到 1.65；本颗混信号版 CLUSTER 始终 **1.14–1.26**，无提升趋势 ⇒ 结构性，不再投仿真。
但 W378 同时给出**最低 prod 0.6740**（余量 0.026，是 W252 的 7 倍）与最高 sub/CLUSTER ⇒ 按 skill ④b「prod 贴线时低 prod 优先」选 W378。

### ④ 9 ops 是最小可行集

| 消融 | ops | S | F | 2Y | 判定 |
|---|---:|---:|---:|---:|---|
| `MP6OwzpM` 删 corr 背离腿 | 6 | 1.51 | 0.85 | 1.51 FAIL | 回滚（且会丢低 prod） |
| `npa90qgw` 删 `ts_zscore` | 8 | 1.00 | 0.52 | 1.11 | 回滚 |
| `78YWOmwx` 删 `group_neutralize` | 8 | 1.46 | 0.84 | 1.15 | 回滚 |
| `RReMXzpb` `ts_corr` 窗口 504 | 9 | 1.66 | 0.96 | 1.82 | 不如原式 |

⇒ 变量合并后的 9 个算子全部承重。

### ⑤ prod 随结构变化，必须逐颗复检

`leadbAKA` 0.6713 → `N1P0odXg` 0.6964 → `88NbAJnl` **0.6740** → `P05Nez1L` 0.6942。全部 `passes_check=true`，但幅度差 0.025 ⇒ 对余量 <0.05 的候选，**结构微调就能决定生死**。

---

## 4 交付件 `88NbAJnl` 完整判据

| 项 | 值 | 门槛 | 判定 |
|---|---|---|:---:|
| 表达式 | 变量合并 a/b/c + `ts_zscore` 窗口 378、无平滑 | — | **9 ops** |
| Sharpe | **1.74** | 1.58 | ✅ |
| Fitness | **1.03** | 1.0 | ✅ |
| 2Y（ATOM:LAST_2Y） | **1.91** | 1.58 | ✅ |
| Sub-universe | **1.48** | 0.90 | ✅ |
| CLUSTER | 1.26 | 1.58 | ⚠ **WARNING**（非 FAIL，`submit_gate` 不拦） |
| Turnover | 0.0881 | 0.01–0.7 | ✅ |
| `submit_gate` | passed / failed_any=0 / hard_gate_warns=[] | — | ✅ |
| mix | `two_leg` legs=2 coef_legs=0，**未硬拦但需三问** | — | ⚠ 待补 |
| 数据使用 | `SINGLE_DATA_SET` → **ATOM 免 Ladder** | — | ✅ |
| ΔS | **+0.05**（`EQUITY:EUR:1` 常规，5.91→5.96） | ≥0 | ✅ |
| self | **0.2393** | <0.7 | ✅ |
| **prod** | **0.6740**（余量 0.026） | <0.7 | ✅ |
| 逐年 | 十年零负年，min **0.19(2019)**、末年 0.98、CV10 **0.592**、CV3 0.536 | CV ≤0.60 | ⚠ CONDITIONAL（2019 近乎零收益年） |

**相对原式的改善**：F 0.96→1.03（FAIL→PASS）、S +0.07、2Y +0.25、sub +0.16、CL +0.02、算子 **13→9**；prod 基本持平（0.6713→0.6740）。

### 提交前置（用户点名后需完成）

1. **补三问**（`two_leg`）：holders / polarity / prior 各 ≥8 字符。建议方向：holders = 财报电话会情绪标签 × 情绪确定性及其与情感的时序背离；polarity = 两腿同向（背离项用 `1−corr` 保持同号）；prior = 情绪强度 × 确定性加权、背离作折扣，回测前由逻辑钉死。
2. **prod `refresh=True` 终验**：现值 0.674 余量 0.026，48h 作废且漂移猛。
3. **稳健软标记复核**：2019=0.19、末年 0.98、CV10 0.592 贴 0.60 线。
4. 三段式属性（name / tags ≤5 / description ≥100 词）。

### 备选 `N1P0odXg`（9 ops, W252）

逐年更稳（min 0.61、末年 1.10、CV10 0.578）、self 0.1987 更分散、ΔS +0.06；但 **prod 0.6964 余量仅 0.0036**、F 1.01 贴线、sub 1.33 / CL 1.16 更低 ⇒ 仅当 `88NbAJnl` refresh 后 prod 翻脸时递补。

---

## 5 与上一轮 `1YWkN1Q6` 的权衡结论

| | `6XMmNmjP`（上轮） | `88NbAJnl`（本轮） |
|---|---|---|
| ops | **3** | 9 |
| S / F / 2Y | 1.79 / 1.14 / 1.91 | 1.74 / 1.03 / 1.91 |
| CLUSTER | **1.65 PASS** | 1.26 WARNING |
| prod | **0.7998 死** | **0.6740 活** |
| 结构 | 单字段 ATOM | 同数据集双字段 + `ts_corr` 背离腿 |

⇒ 同一 `earnings_sent_matrix` 信息源在 EUR 的高 prod 墙，**只能靠改变持仓结构（背离腿）绕开，不能靠拉窗口或压算子**。代价是 +6 个算子与 CLUSTER WARNING。按「prod 是硬闸、算子数是软指标」的优先级，本轮交付件胜出。

---

## 6 产物与数据来源

- 报告：`output_report/opmin_leadbAKA_20261111.md`
- 批次：`results/wp_leadbAKA_{A0,B}_20261111.txt`、`results/wp_leadbAKA_batchB_20261111.json`
- 签核：`results/op_coverage_signoff.jsonl`（2 条）
- 台账：`ledger_kv[EUR].robustness_88NbAJnl`
- 平台：`/alphas/{id}`、`/simulations/{id}`（2 批）、`workflow_submit_alpha(confirm_submit=false)`、`check_correlation(production)` ×4、`check_self_correlation`、`get_alpha_yearly_stats` ×2、`wqb.store.submit_queue.mix_review`、`operator_coverage_audit.py --checklist`

**本轮零提交、零平台写操作**（仅本地台账 1 条）。所有仿真均为派发回测。
