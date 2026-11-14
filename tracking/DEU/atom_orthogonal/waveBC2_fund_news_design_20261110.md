# Wave BC2 设计 — FUNDAMENTAL x NEWS 组合（候选，待 BC1 腾槽）

> BC1（OTHER x NEWS）在飞；本文件预置第二条组合路线，组合类型限额内（总量 ≤5，每类 ≤3）。

## 为什么选 FUNDAMENTAL x NEWS

- **fundamental6 T1 现金利润率（gJeLvb8O）是全 DEU 最强弱腿**：S **1.15** / F 0.98 / **margin 0.006856（全 DEU 最高档）** / TO 0.0265 / sub 0.79；短板是 2Y 0.43。
- **news18 N4（qM7KrW6A）**：S 0.57 / **2Y 1.44** / lc **170** / TO 0.024。
- **两腿短板互补**：T1 弱在 2Y（近期弱）、N4 强在 2Y（近期强，2022 年 1.96）⇒ 组合有望把 2Y 拉过 1.58。
- 塔合规：FUNDAMENTAL 属禁混集合，NEWS 属集合外 ⇒ **集合内 x 集合外，允许**（此类组合总量 ≤5）。

## ⚠ 唯一阻断项

fundamental6 T1 的字段组合**已被生产池占据**（prod 0.9389 / 0.9728，FINAL_STATUS 路径 A 记录）。
⇒ 若以 T1 原式为腿，组合后 prod 大概率仍 >0.7 ⇒ 逐闸第一步就会死。

**缓解方案**：换 fundamental6 的**近邻字段**（同族但不同科目，避开被占据的 fnd6_newq_oiadpq）——需先做字段自测。
候选：`fnd6_oancfy / fnd6_revty`（T1 本身用此二字段）、`fnd6_gpy`（毛利）、`fnd6_newq_seqq`（股东权益）。

## 待办（在 BC1 收割后）

1. 先查 T1（gJeLvb8O）的 prod 现状 refresh —— 若已 <0.7，直接用它做腿。
2. 若仍 >0.9：跑 2-3 条 fundamental6 近邻字段的水平臂（探针），找未被占据的现金利润率变体。
3. 组合臂（3 条）：
   - D1: `group_rank(add(rank(T1等效腿), N4), subindustry)`
   - D2: `vector_neut(N4, T1腿)`（纯新闻残差）
   - D3: `rank(T1腿) x rank(N4)` 乘积确认

## 其他备选组合类型（若 BC2 也失败）

| 类型 | 两腿 | 备注 |
|---|---|---|
| INSTITUTIONS x NEWS | fund_holdings F2(0.65) x news18 N4(0.57) | F2 TO0.467 会推高组合换手，风险中等 |
| INSTITUTIONS x SENTIMENT | F2 x event_sent A1(0.70/2Y1.97) | A1 的 2Y 强、TO0.034 |
| OTHER x SENTIMENT | other47 W1(0.80) x event_sent A1(0.70) | 两腿都低换手 |