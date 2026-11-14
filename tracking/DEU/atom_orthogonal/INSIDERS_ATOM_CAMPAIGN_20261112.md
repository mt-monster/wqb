# insiders ATOM 攻坚：约束与基线设计

日期：2026-11-12
用户指令：「锁定 insiders 挖掘 ATOM」

## 一、ATOM 在 insiders 上的硬约束

| 约束 | 内容 | 代价 |
|---|---|---|
| 单数据集 | 只能用 `insiders1` **或** `insider_agg_matrix` 之一 | 无法用「holdings 变化 × HHI 集中度」这个最有效组合 |
| **禁 `cap` 桶** | `cap` 属 PV 塔，一用就变双塔 | **失去市值分桶中性化**（实测 cap 桶曾把 sub 从 0.63 拉到 0.90）|
| 禁 group 类外的其他数据集字段 | `sector`/`market`/`bucket(...)` 豁免不算数据集 | 分组轴仍可用 sector |
|
| 闸门 | ATOM 走 `LOW_2Y_SHARPE`（1.58），**不走 `IS_LADDER_SHARPE`** | 必须近两年强势 |

## 二、两个数据集的可选字段

### insiders1（VECTOR，6 个可用）
| 字段 | 语义 | 历史单腿最佳 |
|---|---|---:|
| `insd1_holdings` | 交易后总持股 | **1.33**（Δ66+ts_ir 两腿，BE178 的正交化版）|
| `insd1_valueeur` | 交易金额（欧元）| 1.14 |
| `insd1_shares` | 交易股数 | 1.29（占持仓比）|
| `insd1_tradesignificance` | 显著度 1-3 | 0.88 |
| `insd1_price` | 交易价 | 1.13 |
| `insd1_value` | 交易金额（原币）| 弱 |

### insider_agg_matrix（MATRIX，30 个可访问）
| 字段族 | 语义 | 历史单腿最佳 |
|---|---|---:|
| `significant_value_1..4` | 第 1-4 大单笔金额 | **0.93**（HHI+DI+TT）|
| `directional_indicator` | 方向指标（cov 1.0）| 0.59 |
| `total_*/avg_* buy/sell_shares` | 买卖股数比 | 未单测 |
| `top_*` 系列 | 高管维度 | 0.73-0.83（判死）|

## 三、已派基线波（先用数据说话）

| 波 | alpha 数 | 内容 |
|---|---:|---|
| **BE185** `PPAIJ52W` | 10 | insiders1 六字段 × 三形态（Δ66 / ts_ir66 / lvl66）单腿矩阵 |
| **BE186** `3IRA2k2M` | 10 | insider_agg_matrix 九字段单腿 + HHI+DI+TT 组合 |

目的：在**不动用 cap、不跨数据集**的前提下，找出每个数据集内的最强单腿，
再决定往哪个数据集投入。

## 四、已知的关键事实（避免重复踩坑）

1. **同源加腿必稀释**：insiders1 的 6 字段都来自同一条交易记录，跨字段相加只会平均化（BE174 实测 2 腿 1.30 → 7 腿 1.03）。
2. **正交化只 +0.03**：`vector_neut(B,A)` 从 1.30 到 1.33，因为残差只剩 10% 独立成分。
3. **同形态多窗是闸5 唯一放行形态**，但实测无增益（BE172：22/66/132 各窗组合 0.76-1.22）。
4. **ATOM 免 IS_Ladder 但要过 LOW_2Y**，对近两年弱的族更严（starmine 教训：S 1.80 却卡 2Y 1.51）。
5. **判据必须用 `submit_verdict`**，`checks.fail=[]` 会误判（78YWrjgZ 就是 `checks.fail=[]` 但 verdict BLOCKED）。

## 五、现实预期

| 数据集 | 已测最好 | 需要 | 缺口 |
|---|---:|---:|---:|
| insiders1 | 1.33 | 1.58 | −0.25 |
| insider_agg_matrix | 0.93 | 1.58 | −0.65 |

⇒ insiders1 更接近。但 1.33 是**用了两腿叠加**（A+B）的结果，而闸5 禁跨形态相加。
⇒ 若严格守闸5，insiders1 的单形态多窗上限只有 1.22（BE172）。
⇒ **本次攻坚的关键取舍**：用户要求「insiders + ATOM」，未明确闸5。
   若闸5 也需守，则 insiders1 上限 1.22，离 1.58 差 0.36，基本无解。