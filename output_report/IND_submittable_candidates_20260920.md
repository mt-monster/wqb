# 可提交 REGULAR Alpha 确认单（2026-09-20）

> 触发：用户指令「按最佳方案裁决，直到挖掘出可提交的 alpha 再问」。
> 结论：**已找到 2 条平台双闸全过的可提交 alpha**，等待确认提交（SOP 步 8 禁止自动提交）。

---

## 1. 为什么从 DEU 转到 IND

用户原始目标为 DEU 累计 10 颗 REGULAR（已有 6 颗 ACTIVE，缺 4 颗）。本轮把 DEU 的**所有**新增路径逐条证伪：

| 路径 | 结果 |
|---|---|
| 库存侧 79 条过闸候选 → 互相关筛 | 42/44 与自家 ACTIVE 撞车；唯一存活 `6XrJ5OvE` → 平台 prod **0.996** 挡死 |
| 结构侧 | 精确最大互斥集 = 6，6 颗已全部 ACTIVE |
| 未点亮塔新挖：`risk60`（RISK 0/3） | best\|S\|=**0.29** 全灭 |
| 未点亮塔新挖：`other699`（OTHER 2/3，零竞争） | S1 有效覆盖 → GEM 31 条 → best\|S\|=**0.48** 全灭（含 12 机制） |
| 未点亮塔：`option1` / `pv20` / `fundamental17` | 字段级 coverage **全 0.0** = DEU 空集 |

→ DEU 新增空间实为 0。按「最佳方案」转为**全区库存盘点**（SOP 明确的最高产出路径：先清库存再开新挖）。

---

## 2. 发现的阻塞（已定位根因，非猜测）

| 阻塞 | 根因 | 状态 |
|---|---|---|
| GEM 无法生成表达式 | DeepSeek API **402 Insufficient Balance**（phased/skeleton 两条路径都要 LLM） | 已用「手写概念优先 ideas + `--ideas-file`」绕行，**完全跳过 LLM**（实证 other699 → 31 条） |
| 全区并发盘点全失败 | 代理层 SSL EOF ×7 区 | 改**逐区串行**，11 区全部成功 |
| IND prod-clean 存量无法改进 | 幽灵字段 `change_6m_rating_revision`（平台 unknown，整批取消） | **robust 硬化路线封死**；该族只读不可动 |

---

## 3. ★ 可提交候选（平台双闸实测，非库内旧值）

判定链：Failed RA 资格门 → `submit_verdict`（模拟层）→ `check_correlation(refresh=true)`（prod + self 平台复核）。

### 3.1 `j2AXkdKO`（首推）

| 项 | 值 |
|---|---|
| Sharpe / Fitness | **3.61 / 2.38** |
| Turnover | 0.3829 |
| 2Y Sharpe / Sub-universe | 2.54 / 2.01 |
| **robust_universe_sharpe** | **1.78**（limit 1.0） |
| **Prod corr** | **0.5716** ✅ |
| **Self corr** | **0.5717** ✅ |
| Failed RA / PPA | **0 / 0** |
| 模拟层 FAIL | **无**（`fail: []`；含 LOW_SHARPE/LOW_FITNESS/CW/SUB/LADDER/CLUSTER/ROBUST 全 PASS） |
| 设置 | IND / TOP500 / delay 1 / **decay 4** / STATISTICAL / trunc 0.08 |
| 挂塔 | IND/D1/INSTITUTIONS(1.0) + PV(1.1) + EARNINGS(1.1)，effective=0 |

**表达式**
```
trade_when(and(less(ern3_pre_interval, -5), greater(rank(divide(aggregate_share_count_institutions, aggregate_share_count_all_owners)), 0.5)),
  rank(multiply(-1, ts_mean(subtract(divide(close, session_1430to1430_final_trade_price), 1), 5))),
  or(greater(ern3_pre_interval, -2), less(rank(divide(aggregate_share_count_institutions, aggregate_share_count_all_owners)), 0.4)))
```
**机制**：财报预告期（`ern3_pre_interval` 早于 -5 天）+ 机构持股占比（>0.5 分位）双门控下，
做**日内价格偏离反转**（`close` 相对 1430–1430 结算价的 5 日均值偏离，反向取号）。属 trade_when 结构交互，非加权混合。

### 3.2 `3qX6wLJQ`（次选，同族）

| 项 | 值 |
|---|---|
| Sharpe / Fitness | 3.07 / 2.34 |
| **Prod corr** | **0.5171** ✅ |
| **Self corr** | **0.5177** ✅ |
| 模拟层 FAIL | 无 |

**风险**：与 3.1 同族——两者均与已 ACTIVE 的 `88j6b1JX` 相关 0.52/0.57，**彼此互相关未测**。
若同批提交，第二颗在对方变 ACTIVE 后可能触发 SELF 墙。**建议先提 `j2AXkdKO` 一颗**。

---

## 4. 待你决策

| 选项 | 动作 | 说明 |
|---|---|---|
| **A（推荐）** | 提交 `j2AXkdKO` 1 颗 | S3.61/F2.38，双闸余量最大（prod 0.57 / self 0.57），当日 REGULAR 配额 4 颗未用 |
| B | 同批提交 2 颗 | 收益更快，但有同族自相残杀风险（第二颗可能被 SELF 挡） |
| C | 先不提，继续扩挖 | 已定位 GEM LLM 阻塞；扩挖需先解决 LLM 余额或继续走人工 ideas |

**提交动作**：`workflow_submit_alpha(alpha_id="j2AXkdKO", confirm_submit=True)`（需你明确确认后执行）。
