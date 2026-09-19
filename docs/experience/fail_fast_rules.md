# Fail-Fast 判据：无效努力信号 与 可修复/结构性失败

> 来源：CSDN `2402_87488142`「WorldQuant BRAIN 实战笔记(1)：一个软工学生的一个月研究复盘」
> （3000+ 回测、36 次提交的实证复盘）+ 本仓 wave 复盘经验固化。
> 落地时间：2026-09-13 ｜ 机器实现：`wq-brain-campaign-toolkit/scripts/_lib/rules.py::classify_failure`
> 机器规则：`config/methodology_rules.json` 的 `failure_nature_classifier_v1`（diagnosis）+
> `no_effort_seven_signals_v1`（dead_end）；本文是**人看层**，两者同源。

**核心命题**（该复盘最重要的结论）：*决定研究效率的不是回测次数，是研究判断。*
同一家族里连续几条出现相似失败就该停——**确认一个方向不值得继续，本身就是有价值的研究成果**。

---

## 1. 无效努力七信号

| # | 信号 key | 现象 | 机器判据（`classify_failure`） |
|---|---|---|---|
| ① | `sharpe_plateau_0.7_0.9` | Sharpe 卡在 0.7–0.9，怎么也上不去 | 全波最高 sharpe ∈ [0.7, 0.9] |
| ② | `pnl_backhalf_decay` | PnL 曲线前半段好看、后半段明显衰减 | 存在 2Y 墙，或 `two_year_sharpe < 0.7 × sharpe` 的行占比 ≥ 50% |
| ③ | `window_invariant` | 换窗口/换变体后结果几乎无本质变化 | ≥3 行且 ≥80% 共享同一**硬墙**组合（SHARPE/FITNESS/SELF_CORRELATION/LOW_SUB_UNIVERSE_SHARPE） |
| ④ | `fitness_persistent_miss` | Fitness 始终不达标 | FITNESS 墙行占比 ≥ 50% |
| ⑤ | `subuniverse_repeat_fail` | Sub-universe 反复失败 | LOW_SUB_UNIVERSE_SHARPE 行占比 ≥ 34% |
| ⑥ | `weight_concentration_high` | Weight concentration 偏高 | CONCENTRATED_WEIGHT 行占比 ≥ 40% |
| ⑦ | `similarity_over` | 好不容易过线，Similarity 又爆表 | 存在 SELF_CORRELATION 墙，或 `prod_corr > 0.7` 的行 ≥ 1 |

> 此时若还抱着"再调一下也许就过了"的心态，**只是在消耗模拟次数**。

---

## 2. 可修复 vs 结构性失败（判定的关键分叉）

| 维度 | ✅ 可修复 | ❌ 结构性 |
|---|---|---|
| 指标 | Sharpe/Fitness **只差一点** | 换方向/换窗口结果都差不多 |
| PnL | 整体稳定、权重未失控 | 明显依赖某一段行情（前后段背离） |
| 换手 | Turnover 合理 | decay 一调反而更差 |
| 结构 | Sub-universe 非硬伤 | 加门控后指标继续恶化 |
| 相似度 | — | 过线后 Similarity 过高 |

**可用的修复杠杆**：改 decay ｜ 换 neutralization 档位 ｜ 加 gate ｜ 换历史位置表达。

**机器判定**（`classify_failure(...)["verdict"]`）：

| verdict | 触发 | 建议动作 |
|---|---|---|
| `STOP_STRUCTURAL` | 命中 ②/③/⑦ 任一，或 `max_sharpe < 1.0`（信号太弱），或命中 ≥ 2 项 | **停止该家族**，换字段/数据集方向；禁止继续参数微调 |
| `RETRY_FIXABLE` | 只卡参数层墙（2Y/MARGIN/TVR/CW/FITNESS）且命中 < 2 项 | 参数层轻量调整（decay / neutralization / gate / 历史位置） |
| `INCONCLUSIVE` | 未命中任何信号 | 正常流程 |

> ⚠️ `STRUCTURAL` 的三种来源里，**`max_sharpe < 1.0` 是"信号本身不足"**——与
> `recommend_next_wave` 既有的「结构层重构（字段太弱）」推荐同向，二者会被合并呈现。

---

## 3. 与推荐引擎的接线

`recommend_next_wave()` 在既有 walls 驱动逻辑**之前**先跑 `classify_failure()`：

| verdict | 落地方式 | priority |
|---|---|---|
| `RETRY_FIXABLE` | **新增**一条「可修复失败：参数层轻量调整」推荐，附带 `fail_fast_signals` | 65 |
| `STOP_STRUCTURAL` | **富化**既有「结构层重构」推荐的 `action_hint` + 附加 `fail_fast_signals`（不新增条目，两者结论同向） | 沿用 80 |
| 全局库有 `fail_fast_stop` 规则 | 推荐携带 `source_rule` = 规则 id | — |

---

## 4. 三个更早做会更好的工程实践

1. **尽早建立可用字段池** — 哪些字段可用 / 有 unit 问题 / 易致高 Similarity / 适合主信号或 gate，都应尽早记录，不要每次现搜现试。
2. **尽早建立 fail-fast 规则** — 同一家族连续几条卡在相似失败区间就先停下复盘，而不是机械增加模拟次数（本文即其机器化）。
3. **尽早区分「研究成功」与「提交成功」** — 提交成功重要，但确认一个方向不值得继续，同样是有价值的研究成果。

---

## 5. 反向纪律：AI/自动化只做研究效率，不碰提交

| ✅ 值得自动化 | ❌ 红线（不做） |
|---|---|
| 整理回测结果与 CSV | 自动生成并批量提交 Alpha |
| 统计 Sharpe/Fitness/Turnover/Margin | 自动刷平台规则 / 绕过检查 |
| 给 Alpha 打标签、按家族分类 | 直接公开可提交的核心表达式 |
| 记录失败原因、生成复盘报告 | |
| 沉淀 Prompt / Skill / Checklist | |

> AI 最有用的地方不是"凭空生成公式"，而是**复盘失败原因、把零散结果结构化、区分修复方向、把经验固化为规则**。
> 与本人既有纪律一致：`Maker ≠ Checker`（干活与把关分离）、不刷规则。

---

## 6. 可调阈值

见 `rules.py` 的 `FAIL_FAST_THRESHOLDS`，可按区域用 `thresh` 参数覆写：

```python
from _lib import rules as R
cf = R.classify_failure(rows, {"region": "IND"},
                        thresh={"plateau_low": 0.6, "min_signals_to_stop": 3})
```

| 键 | 默认 | 含义 |
|---|---|---|
| `plateau_low` / `plateau_high` | 0.7 / 0.9 | Sharpe 平台期区间 |
| `weak_sharpe` | 1.0 | 低于此判"信号太弱"（结构性） |
| `pnl_decay_ratio` | 0.7 | `two_year_sharpe < ratio × sharpe` 视为远期衰减 |
| `dominant_wall_share` | 0.8 | 变体不变性的共享墙占比阈值 |
| `wall_share` | 0.5 | 单信号行占比阈值 |
| `subuniverse_share` | 0.34 | Sub-universe 反复失败阈值 |
| `concentration_share` | 0.4 | 权重集中度阈值 |
| `min_signals_to_stop` | 2 | 命中此数量即判结构性 |

---

## 7. 落地验证（2026-09-13 实测）

`pytest tests/ -q` = **834 passed**；toolkit `test_rules.py` = **43 passed**（新增 10）；
`sync_skills.py` 4 个安装位已传播。

**真实数据 dry-run**（`logs/_tmp_failfast_dryrun.py`，只读 `data/wqb.db` 的 IND 回测）：

| 波次 | n | max_sharpe | 命中信号 | verdict |
|---|---|---|---|---|
| wave97 | 9 | 2.04 | weight_concentration_high | `RETRY_FIXABLE`（信号强，只需 group_neut / 降 truncation） |
| wave96 | 8 | 1.28 | subuniverse_repeat_fail + weight_concentration_high | `STOP_STRUCTURAL`（≥2 项） |
| wave95 | 8 | 1.05 | subuniverse_repeat_fail | `RETRY_FIXABLE`（单发参数层信号） |
| wave93 | 8 | 0.38 | subuniverse_repeat_fail + weight_concentration_high | `STOP_STRUCTURAL`（信号太弱 + ≥2 项） |

反例边界：虚构全达标波 → `INCONCLUSIVE`；虚构弱信号波（max_sharpe 0.3）→ `STOP_STRUCTURAL`。

> 解读：**同为"卡墙"，wave97 值得救而 wave93 应止损**——这正是本文要区分的判断力。

