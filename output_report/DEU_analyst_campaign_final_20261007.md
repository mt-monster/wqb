# DEU / ANALYST 战役最终报告 · 2026-10-07

> 目标：锁定 ANALYST category，在 DEU 挖 10 颗可提交 REGULAR。
> 结论：**产出 0 颗可提交**；最优候选 `RR6mjbqn` **S 1.67 / 2Y 1.58（== limit）**，卡在分辨率墙。
> 本会话 DEU 全域累计 **≈205 次字段/机制测试 → 1 颗可提交（`58gkLAkk`，来自 MODEL）。全程零提交。**

---

## 1 战场选择（用平台数据定）

| 判据 | 实测 |
|---|---|
| 哪些塔已点亮 | `get_pyramid_alphas`：**DEU/D0 与 D1 全部 16 类计数 = 0** ⇒ 无"已点亮塔"约束 |
| ANALYST 高覆盖字段 | 642 个：`analyst7` 425、`analyst93` 100、`analyst_factor_signals` 49、`analyst44` 48 |
| 主战场 | **`analyst_factor_signals`**（cov 最高，单字段达 0.9234） |

## 2 有效信号面（关键结论）

`analyst_factor_signals` 49 个字段分 7 类，**只有 A 类「预期变化」携带有效信号**：

| 类 | 字段 | 数量 | 配的机制 | 结果 |
|---|---|---:|---|---|
| **A 变化** `*_estimate_change_3mo` | 7 | 水平+双窗 | ✅ **唯一有效** |
| B 幅度 `*_revision_magnitude` | 3 | 取变化 | ❌ |
| C 增长 `*_cagr_*yr` | 9 | 水平 | ❌ |
| D 分歧 `*_{skewness,asymmetry,coeff_var}` | 17 | 取变化（收敛） | ❌ 最大类全灭 |
| E 水平 `*_consensus_value` | 6 | 取偏离 | ❌ |
| F 趋势 `*_trend_slope` | 3 | 水平 | ❌ |

⇒ **方法论修正：机制匹配是必要条件而非充分条件**——**先判字段是否携带信号，再谈配机制**。
同一批字段换机制只有 ±0.1~0.3 的提升；A 类与非 A 类之间差 **0.6~1.5**。**字段的权重远大于机制。**

## 3 全方位算子优化（70 条，四个槽位）

| 槽位 | 结论 |
|---|---|
| 截面算子（rank/zscore/winsorize/normalize/scale/嵌套） | **全部单调无操作**（与对照逐位相同）；仅 `driver=uniform` 改结果 |
| 轴算子（3 层 × 4 种 + ~30 组合） | ★★ **图轴换 `group_scale`**：S **+0.08**、sub **+0.18** |
| 外层算子（signed_power/hump/tvr 族/quantile 参数） | 均无操作或更差 |
| 时序核（w1 1~8 × w2 180~252） | ★ **短腿 `w1` 缩到 1~3**：**同时**抬 S 与 2Y |

## 4 最终结果：优化到位，但卡在分辨率墙

| 指标 | 起点 `0mrM2bJr` | 终点 `RR6mjbqn` | Δ |
|---|---:|---:|---:|
| Sharpe | 1.54 | **1.67** | **+0.13** |
| Fitness | 1.35 | **1.46** | +0.11 |
| sub-universe | 0.81 | **1.02** | **+0.21** |
| **2Y（ladder）** | 1.57 | **1.58** | +0.01 |
| 失败闸 | 2 | **1** | — |

**权威判定**：`IS_LADDER_SHARPE value=1.58 limit=1.58 result=FAIL` ⇒ `verdict=BLOCKED`。
平台把 ladder 值**四舍五入到 2 位**再与 limit 做**严格比较**，**真值须 ≥ 1.585**。

**已 100% 穷尽的维度**：截面算子 8 种｜轴算子 3 层×4 种 + 组合｜外层算子 8 种｜时序核 w1{1,2,3,4,5,8}×w2{180~252}｜
桶粒度 0.03~0.08｜桶基准（自身 + 5 兄弟字段）｜`decay`{3,4,5,6,8,12}｜`truncation`{0.04,0.06,0.08,0.10,0.12}｜
`neutralization` 11 档｜`universe`（DEU 仅 TOP500）。

**为什么破不了**：基准字段靠"加第 4 层慢分量桶轴"（+0.49）破墙；本族桶轴**一开始就在用**，
再加第 4 层轴（图聚类 Z / market / exchange）实测**全部退化** ⇒ **没有可加的正交轴了**。

## 5 处置

- `RR6mjbqn` 已登记**台账 `DEU::submit_ready_blocked`**（状态 `BLOCKED_PENDING_REVIVAL`）。
- 翻案路径：① DEU 开放第二 universe 档 ② 平台改判 ladder 分辨率 ③ **把此配方迁移到别的区域**。
- `58gkLAkk`（MODEL，S1.75/F1.42/2Y2.07/prod0.5381/self0.5153/robustness PASS）仍在 `DEU::submit_ready` 累积，**待用户批准提交**。

## 6 本族最强配方（可复用）

```
DEU / TOP500 / D1 / decay=4 / SUBINDUSTRY / trunc=0.08 / nanHandling=OFF / maxTrade=OFF
group_neutralize(                                        # 桶轴（最外）
  group_neutralize(                                      # 行业轴
    group_scale(quantile(add(ts_mean(bf, 1), ts_mean(bf, 210))), <oth455 图聚类键>),  # ★ 图轴 group_scale
    subindustry),
  bucket(rank(ts_mean(bf, 252)), range="0,1,0.05"))      # ★ 短腿=1、桶粒度=0.05
bf = ts_backfill(eps_y1_estimate_change_3mo, 1008)
```
