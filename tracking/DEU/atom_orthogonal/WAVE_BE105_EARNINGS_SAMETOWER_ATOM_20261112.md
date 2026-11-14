# BE105 — EARNINGS 塔 ATOM：earnings6 × earnings_sent_matrix 同塔跨数据集（2026-11-12）

> 用户指令：「先集中在 EARNINGS 塔下数据集分析，挖掘 ATOM」。

## 一、字段层结论：EARNINGS 塔已无新字段可用

| 数据集 | 字段数 | 已测（严格口径） | 未测 | 未测字段性质 |
|---|---:|---:|---:|---|
| earnings_sent_matrix | 7 | **7/7** | 0 | — |
| earnings6 | 18 | 11/18（宽松 13） | 5 | `ern6_3q` / `ern6_actual_fiscal_year` / `ern6_estimated_fiscal_year` / `ern6_next_ed_fiscal_year` / `ern6_x_dividend_oc` —— **全是财年/季度标签与股息币种变体，非信号** |

⇒ 已测覆盖 20/25 字段，剩余 5 个无信号价值。**塔内不存在「未试字段」这条出路。**

## 二、结构层结论：唯一未碰过的是「同塔跨数据集」

DEU 全档案 **9,743 条去重表达式**中的分布：

| 类别 | 条数 |
|---|---:|
| 只含 earnings6 | 23 |
| 只含 esm | 35 |
| **同时含两者** | **0** |

⇒ earnings6（SUE/指引/股息/日历）× esm（电话会语调）**从未组合过一次**。

**为什么这仍是 ATOM**：金字塔归属按数据集判定，两集同属 `DEU/D1/EARNINGS` ⇒ 组合后 towers=1 ⇒ ATOM 资格不变
（本战役已在 ANALYST 4 集、SENTIMENT 3 集上复验 eff=1）。

## 三、闸5 合规性：全部用乘法门控，不用加性合并

闸5 禁止两条独立信号腿加权相加。本波 10 臂**全部避免 add 合并两腿**：
`add` 仅出现在 TONE 的分母位（P+N 归一化）⇒ 放行；双信号组合一律走 `multiply`（与 `Jj8w52Me` 同法）。

## 四、十臂设计（协议 v2 · L1 正交网格：2 字段 × 2 矩 × 2 骨架 + 2 文献臂）

记号：`SUE = vec_avg(ern6_actual_eps) − vec_avg(ern6_estimated_eps)`（同量纲 EPS 净额）、
`TONE = P/(P+N)`（esm 的条件正概率，本塔最强构造）。

| # | 构造 | 回答的问题 |
|---|---|---|
| A1 | `group_rank(ts_zscore(SUE,252), subindustry)` | earnings6 侧基线（当前口径下 SUE 有无信号） |
| A2 | `group_rank(ts_zscore(ts_delta(SUE,66),504), subindustry)` | SUE 的**变化矩**（预期修正方向，非水平） |
| A3 | `group_rank(ts_zscore(TONE,504), subindustry)` | esm 侧基线（已知 0.71，作对照锚点） |
| A4 | `group_rank(ts_zscore(ts_delta(TONE,66),252), subindustry)` | TONE 的**变化矩**（语调转向） |
| **A5** | `group_rank(multiply(ts_zscore(SUE,252), ts_zscore(TONE,504)), subindustry)` | **PEAD × 看涨语调共振**（文献核心假设） |
| **A6** | `group_rank(multiply(ΔSUE_z, ΔTONE_z), subindustry)` | 预期修正与语调修正**同向**时更强 |
| A7 | `group_rank(multiply(SUE_z, ΔTONE_z), subindustry)` | 水平 × 变化（信息新鲜度交叉） |
| A8 | `group_rank(multiply(ΔSUE_z, TONE_z), subindustry)` | 变化 × 水平（同上反向配对） |
| A9 | `group_rank(multiply(SUE_z, 公告活跃度_z), subindustry)` | **事件密度门控**：有实际公告的 SUE 更可信（覆盖噪声过滤） |
| A10 | `group_rank(multiply(Δ股息_z, TONE_z), subindustry)` | 管理层信心（股息变化）× 语调 |

设置：DEU / TOP500 / D1｜**decay 0**（esm 实证主杠杆）｜SUBINDUSTRY｜trunc 0.08｜**nan ON**（esm 实测 ON 优于 OFF：0.87 vs 0.70）｜pasteurization ON

## 五、判读线（派发前预设）

| 结果 | 处置 |
|---|---|
| 任一臂 S ≥ 1.2 且 lc/sc 健康 | 按 L2 补 10 臂（窗阶 252/504/1008 × 另两矩） |
| max S ∈ [0.9, 1.2) | 说明「同塔组合」确有协同（对照单腿 A3=0.71/单腿 A1），补 8 臂 |
| max S < 0.9 且 ≤ 单腿最好值 | **同塔组合无协同** ⇒ EARNINGS 塔第 6 面封闭，本塔字段+结构双穷尽，终局 |
| 任一臂 |S| ≥1.2 但 lc/sc = 0 或严重失衡 | 空心件，作废，不得据此升级（BE99 教训） |

**先验（诚实披露）**：两腿单独天花板分别 0.80 / 0.87，乘法门控通常进一步压低绝对值（本战役 4 次实证「加腿/组合不增 S」）。
本波的赌点不是「平均变强」，而是「**共振子样本的 IC 显著高于全体**」——若成立，rank 后的极端分位会给出更高 Sharpe。


---

## 六、实测结果（10/10 COMPLETE，0 ERROR）

| 排名 | alpha | 臂 | S | F | TO | Y2 | sub | fRA |
|---:|---|---|---:|---:|---:|---:|---:|---:|
| 1 | `vRAqo2mr` | **A3（esm 单腿对照，与 BE102 同一表达式）** | **0.71** | 0.35 | 4.6% | 2.13 | 0.50 | 2 |
| 2 | `d5aX6Eov` | A1/A2（earnings6 侧） | 0.53 | 0.23 | 6.5% | 0.65 | −0.07 | 4 |
| 3 | `Jj8wkg2m` | 其余组合臂 | 0.39 | 0.16 | 8.3% | −0.02 | −0.28 | 5 |
| 4 | `3q0bOa2Q` | 组合臂 | 0.06 | 0.01 | **67.0%** | 0.17 | −0.54 | 5 |
| 5-10 | 余 | 组合臂 | 0.05 ~ −0.17 | ≤0.01 | **50-72%** | ≤0.11 | ≤−0.59 | 5-6 |

### ★判决：本波不成立，但**结论只能限定为「本设置下无协同」，不能推出「同塔组合无信号」**

**致命观察**：所有含 earnings6 的臂 TO 全部飙到 **50-72%**（对比 esm 单腿 4.6%）。
季频事件数据不可能有 70% 的年换手 —— 这说明 `vec_avg(ern6_*)` 在 DEU/TOP500 上**大面积无效值**，
nan ON 把无效值填 0 后，`ts_delta/ts_zscore` 处理的是「0 → 偶尔一个跳点」的序列 ⇒ 产出的不是信号，是跳点噪声。

**推论**：本波的 9 个组合臂**从未真正测到「两条腿的组合」**——因为其中一条腿（earnings6）在该设置下是死的。
「组合无协同」这个结论因此**不成立**，只能说「在 earnings6 退化的前提下，组合无协同」。

**这暴露了 L1 正交网格的设计缺陷**（用户当场指出）：
网格把「腿的质量」「组合结构」「回测设置」三件事压在同一个 10 臂里，任一维度失效都会污染全部结论。
