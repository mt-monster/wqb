
### 53. ★★★ F 的真实算法（大 TO 段）：F = S × √(ret / TO)，降 TO 同时抬 F（2026-11-13 精确验证）

**既有判据（第 17 条）只在小 TO 段成立**：`F = S×√(8·ret)` 是 `max(TO,0.125)=0.125` 的特例。

**本轮在 TO=68% 下精确验证**：
```
P05EONAK: S=1.76, ret=11.35%, TO=68.05%
实测 F = 0.72
公式 F = S×√(ret/TO) = 1.76×√(0.1135/0.6805) = 1.76×0.4084 = 0.719  ✅ 精确吻合
（若用 √(8·ret) 会得 1.68，完全错误）
```

**通用形式**：
```
F = S × √( ret / max(TO, 0.125) )
```
- TO < 12.5% 时退化为 `F = S×√(8·ret)`（既有判据）
- TO > 12.5% 时 F 与 √TO 成反比

**★★ 可复用的核心推论**：
> **降 TO 同时抬 F。** 在 S、ret 不变的前提下，TO 从 68% 降到 30%，F 从 0.72 升到 1.08（+50%）。

**应用**：
1. **F 不过闸时，第一优先是降 TO**，不是提 ret。降 TO 是唯一能同时保 S 又抬 F 的杠杆。
2. 反例警示：`ts_mean(22)` 把 TO 68%→13.2%，F 0.72→0.76（只 +0.04），因为 S 塌了 1.76→1.11。**暴力平滑虽降 TO 但杀 S，净效果几乎为零。**
3. **正确的降 TO 顺序**：decay 阶梯（0/2/4/8/12/16/24/32）→ 温和平滑（ts_mean 5/11）→ 换宇宙。decay 不改信号、只压换手，是首选。

### 54. ★★★ pv20 crowding 是 EUR 首个 S 破 1.58 且 TO 在限内的候选（2026-11-13）

```
P05EONAK
group_rank(ts_rank(subtract(0, specific_return_crowding_top2500), 630), industry)
region=EUR universe=TOP2500 delay=1 decay=8 neut=INDUSTRY trunc=0.08
```
**平台侧权威 checks**：
| 项 | 值 | 限 | 结果 |
|---|---:|---:|---|
| LOW_SHARPE | **1.76** | 1.58 | ✅ PASS |
| HIGH_TURNOVER | **68.05%** | 0.7 | ✅ PASS |
| LOW_SUB_UNIVERSE_SHARPE | **1.39** | 0.91 | ✅ PASS |
| LOW_FITNESS | 0.72 | 1.0 | ⚠️ |
| LOW_2Y_SHARPE | 0.92 | 1.58 | ⚠️ |
| CLUSTER_TEST | 1.18 | 1.58 | ⚠️ |

**机制**：`specific_return_crowding_top2500` = 按拥挤度分组构建的特异收益。**取反 = 做空近期涨得多的拥挤股**（短期反转 + 拥挤度惩罚）。
**关键设置**：**decay 8 + subtract(0,...) 同时解决两个问题**——S 从 −1.77 翻到 +1.76，TO 从 89.6% 压到 68.05%（刚好进限）。
**三条 crowding 字段同源**（top2500/top1200/notliquim 的 S 差 ≤0.03、TO 差 ≤0.1%）。
**边界**：`ts_mean` 平滑杀伤极大（22 日 → S 1.11 / TO 13.2%；66 日 → S 0.56）⇒ **该信号必须保持当期性**。

### 55. ★★ 目录里有字段 ≠ 平台可用：preflight 是选集前置闸（2026-11-13 两次整批归零实证）

**实证**：
| 字段 | 目录 JSON | 平台 preflight |
|---|---|---|
| `pv87_ann_matrix_return_on_equity_mean` | 有 | ❌ dataset-prefixed not found |
| `ann_matrix_return_on_equity_mean`（去前缀） | — | ❌ unknown_fields |
| `stddev_similarity_reversal_v_top` | 有 | ❌ unknown_fields |
| `stddev_similarity_reversal_v_top_120` | 有 | ❌ unknown_fields |

⇒ **pv87 全部 1649 字段在 EUR 未注册；V 反转族的 stddev 变体也未注册。**

**代价**：两次 `create_multi_simulation` 因单条字段不存在触发 **batch-kill**，5 臂 + 4 臂全部 CANCELLED，白烧 9 条配额。

**纪律（硬）**：`create_multi_simulation` 前**必须**跑 `preflight_expressions` 全量校验，过滤掉 unknown_fields 再派。**一条错 → 整批死。**
