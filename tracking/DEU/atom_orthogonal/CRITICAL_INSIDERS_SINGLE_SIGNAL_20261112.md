# ★关键判断：insiders 族已收敛为「单一信号」，只能贡献 1 颗新件

日期：2026-11-12
方法：`compute_mutual_correlation(alpha_ids=[QP0M3Pjp, qM7KxkQV, qM78WMdv, mLapjPLX], threshold=0.5)`

## 一、互相关矩阵（近 4 年，1021 个点）

|  | S7 `QP0M3Pjp` (1.57) | S3 `qM78WMdv` (1.54) | `mLapjPLX` (1.50) | `qM7KxkQV`（已交付） |
|---|---:|---:|---:|---:|
| **S7 QP0M3Pjp** | 1.0 | **0.938** | **0.979** | 0.322 |
| **S3 qM78WMdv** | 0.938 | 1.0 | **0.933** | 0.395 |
| **mLapjPLX** | 0.979 | 0.933 | 1.0 | 0.324 |
| **qM7KxkQV** | 0.322 | 0.395 | 0.324 | 1.0 |

`max_pair = QP0M3Pjp ~ mLapjPLX = 0.9793`
`all_below_threshold(0.5) = False`
`max_mutually_below_subset = [QP0M3Pjp, qM7KxkQV]` ⇒ **最大独立集只有 2**

## 二、这意味着什么

1. **174+ 臂里所有「S 1.50-1.57」的形态（mLapjPLX / QP0M95Gg / rK7Y2vEJ / qM78WMdv / QP0M3Pjp）实质上是同一个信号**（互相关 0.93-0.98）。它们之间的差异只在**权重与外壳**（幂次、cap 桶、哪条腿乘 FR），不在信息源。
2. **即使把 S 推过 1.58，整个 insiders 攻坚只贡献 1 颗可交付新件**，不是 5 颗。
3. 与已交付的 `qM7KxkQV`（SHORT+INSIDERS，S 1.72）互相关仅 0.32-0.40 ⇒ **与存量件独立**，不撞 self。

## 三、对「20 颗目标」的直接影响

- 已交付 11 颗（6 ACTIVE + 5 待授授权）
- 缺口 **9 颗**
- insiders 攻坚的边际贡献 = **1 颗**（不论 S 是否能破闸）
- ⇒ **靠 insiders 单数据集无法补齐 9 颗**。这是结构性的，不是努力量问题。

## 四、要凑 9 颗的三条路（需用户裁决）

| 路 | 做法 | 代价 |
|---|---|---|
| A | **解锁其他未点亮塔**（news / risk / earnings / pv / institutions 等 DEU D1 均 0 颗） | 违反「已点亮塔不选」的反面——这些正是**未点亮**塔，本该是首选；但违反「锁 insiders」 |
| B | **跨 category 组腿做 regular**（insiders × analyst / news / risk），每颗换不同搭档 | 需 insiders 强腿（已有 S 1.57 可作腿），partner 变化带来低相关；消耗组腿配额 |
| C | 接受 insiders 只出 1 颗，把 20 颗目标下修或分摊到其他区 | 改目标数字 |

**建议 B**：`Vk65zLzG` 已证 insiders×model 可到 S 1.79 且全闸通过；M5 方法论「强腿换搭档仍强才算真强腿」正是为这条路设计的。这条路还能保住「insiders 为核心」的用户要求。
