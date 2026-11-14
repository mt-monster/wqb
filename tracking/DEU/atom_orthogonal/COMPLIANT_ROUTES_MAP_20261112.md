# 合规探索地图（DEU D1，2026-11-12）

## 规则本质（从 Goal 约束第 7 条提炼）

> 「禁止PV,MODEL,OTHER下数据字段两两组腿，不能PV.MODEL,OTHER之间两两组腿……但是可以它们同其它category组腿」

**⇒ 一个表达式里最多只能出现一个 trio 成员（PV / MODEL / OTHER）。**
trio 成员可以与任意多个非 trio 类别（INSIDERS / NEWS / FUNDAMENTAL / SENTIMENT / SHORTINTEREST / EARNINGS …）组腿，总量 ≤5。

## 已知实测结果

| 路线 | 构造 | 塔构成 | 合规 | 实测最好 |
|---|---|---|---|---|
| **PV + INS** | insiders + `bucket(rank(cap))` | PV+INS | ✅ | S **1.58** / sub 0.99（`npa9KaVd`），`effective=2` |
| **MODEL + INS** | insiders + analyst 无 cap | MODEL+INS | ✅ | BE140 在验（BE138 有 cap 版曾达 S 2.63，但违规）|
| **OTHER + INS** | insiders + other455 无 cap | OTHER+INS | ✅ | BE141 在验 |
| **PV + INS + NEWS** | insiders + cap + news104 | PV+INS+NEWS | ✅ | BE139 在验（PV+NEWS 是 goal 举例允许）|
| ❌ PV+INS+MODEL | insiders + cap + analyst | 三分类 | **违规** | S 2.63（作废，仅作机制参考）|

## 塔倍率与点塔

| 形态 | effective | 说明 |
|---|---:|---|
| insiders + cap 桶 | **2** | PV×1.6 + INSIDERS×1.6 —— **唯一实测 effective=2 的合规形态** |
| insiders + cap + analyst | **0** | 三塔被判 0 |

⇒ **要点亮 INSIDERS 塔（需 3 颗），必须走「insiders + cap 桶」两塔形态**，不能用 analyst 加成。

## 缺口与配比策略

目标 20，已合规 11，缺 **9**。

| 来源 | 可出颗数 | 依据 |
|---|---:|---|
| insiders + cap（PV+INS）| 3-4 | 当前只有 1 颗合规过闸（S 1.58 卡 ladder）；需在 S 与 ladder 同时达标上继续攻 |
| insiders + analyst 无 cap（MODEL+INS）| 3-4 | BE140 在验；BE138 证明 analyst 腿能 +0.5~+1.1 S |
| insiders + news（PV+INS+NEWS）| 2-3 | BE139 在验 |
| insiders + other455（OTHER+INS）| 2-3 | BE141 在验 |

**关键洞察**：三条合规路线的「搭档族」不同 ⇒ 产出的件天然低相关（信息源不同），这正是补足 9 颗所需的多样性。
