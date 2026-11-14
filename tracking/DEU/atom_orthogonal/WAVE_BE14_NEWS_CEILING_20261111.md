# BE14 结论：nws20/NEWS 腿 S 天花板 1.52（PROVISIONAL 弱）

## 一、十臂结果（sim 2RuXan7PW4i89uBsxlJBclu，complete=10 error=0）

骨架：`group_zscore(add(新腿, I7), market)`，I7 = `group_rank(ts_rank(ts_backfill(vec_avg(insd1_holdings),132),252),sector)`

| alpha | nws20 腿变体 | S | F | TO | R | sub | 2Y | fail |
|---|---|---:|---:|---:|---:|---:|---:|---|
| **QP010j5W** | Δ66 + 外层 **group_rank** | **1.52** | 0.83 | 0.2335 | 0.0699 | **0.70** | 1.46 | S/Sub/F/Ladder 4 项 |
| KPgKg68p | Δ66 + ts_mean **44** | 1.41 | **1.02** | **0.0812** | 0.0655 | **0.96** | 1.45 | S/Ladder 2 项 |
| kqaxaX1l | Δ66 + **hump 0.01** | 1.38 | **1.01** | **0.0577** | 0.0664 | 0.74 | **2.29** | 仅 S 1 项 |
| O0W1WkmJ | Δ66 + ts_mean 22 | 1.30 | 0.90 | 0.0970 | 0.0601 | 0.71 | 1.55 | S/F/Ladder |
| Grmqm630 | 水平 ts_zscore 66 | 1.33 | 0.68 | 0.2456 | 0.0636 | 0.54 | 1.17 | 4 项 |
| YPajamW6 | ts_rank 252 | 1.21 | 0.60 | 0.2405 | 0.0599 | 0.51 | 1.36 | 4 项 |
| A1xRxbOw | Δ132 | 1.10 | 0.53 | 0.2221 | 0.0525 | 0.55 | 1.47 | ⚠ 平台回 **fails:[]** 是数据缺失假象，ra=3 实为不达标 |
| 58JZJ9qX | Δ66 + I7 ts_mean22 版 | 1.16 | 0.59 | 0.2279 | 0.0592 | 0.59 | 0.81 | 同上假象，ra=3 |
| LLKPK6l9 | Δ264 | 1.09 | 0.54 | 0.2075 | 0.0510 | 0.44 | 1.35 | 4 项 |
| qM7K7dPP | Δ66 + insd1_tradesignificance | 0.58 | 0.27 | 0.0766 | 0.0272 | 0.64 | 1.49 | 3 项 |

## 二、F 公式实测校准（可复用）

`F = S × sqrt(|Returns| / max(Turnover, 0.125))`
- P05JM61x：算得 0.788 vs 平台 0.790 ✓
- rK71dLbE：算得 1.102 vs 平台 1.100 ✓

**推论（破 F 闸用）**：
1. TO > 0.125 时，降 TO **直接提 F**；TO 每降一半，F ×1.41。
2. **TO ≤ 0.125 后降 TO 不再提 F**（分母封顶），继续降只损失 S ⇒ **TO 目标值是 0.125，不是越低越好**。
3. 本波 KPgKg68p / kqaxaX1l 把 TO 压到 0.08/0.06，**越过了 0.125 甜点，白降且丢了 S**。

## 三、NEWS 塔判定：PROVISIONAL 弱（天花板 S=1.52）

**六维覆盖清单**：
- D1 模板互异 ≥10：✓（BE13b 5 臂 + BE14 10 臂，结构含水平/一阶差/平滑/rank/zscore/hump/双新族）
- D2 字段族自测：✓（nws20 情绪得分；nws20 其他字段在 nws 族历史波已测）
- D3 矩全家：✓（Δ66/Δ132/Δ264 一阶差、ts_zmean 水平、ts_rank 位置）
- D4 分组轴：✓（sector 内层 / market 外层 / industry 历史波）
- D5 非线性：✓（hump 门控、group_zscore vs group_rank、ts_mean 平滑）
- D6 配置：部分（仅 TOP500/D1/SUBINDUSTRY；DEU 实际仅 TOP500 可选，D0 已冻结）

**结论**：S 峰值 1.52（QP010j5W），距 1.58 差 0.06；且 S 与 TO 此消彼长，**无法同时满足 S≥1.58 且 F≥1.0**。
⇒ 记 **PROVISIONAL 弱**，不改判死、不再投波次；若未来引入更强第二腿可重估。

## 四、⚠ 平台陷阱（新增）

`harvest_multisim_alphas` 返回的 `checks.fail` **可能是空数组而实际有 fail**。
本波 A1xRxbOw / 58JZJ9qX 都是 `fail: []` 但 `ra.failed_ra_count = 3`。
**鉴别**：以 `ra.failed_ra_count` 与 `metrics` 为准；`checks.fail=[]` 必须用 `get_alpha_details` 复核后才可采信。
