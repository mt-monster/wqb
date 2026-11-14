# ★pv30 全字段是 GROUP 类型 = 现成的数据驱动聚类分组轴（2026-11-11 发现）

> 来自 pv30_fields.csv 全量解析（285 字段，**type 全部 = GROUP**）。

## 一、发现

- pv30 不是价格量数据集，而是**统计行业聚类标签集**：
  `factorN_group{L}_{universe}_513`（L ∈ 2/5/10/20/50，universe ∈ top300/400/600/800/1200/eas）+ `*_pca_component_*`；
- **cov=1.0 的可用轴**：`factor1_group2/5/10/20/50_top800_513`（factor1_group50 u45/a75 使用最广，factor1_group20 u19/a34）；
  `factor2_group*` 系列同样 cov=1.0（u0-5）；
- 这些是 **GROUP 类型 ⇒ 可直接作 group_rank/group_neutralize 的分组参数**（不像 pv29 的簇标签是 MATRIX，需 bucket 桥接——BE46 已实证）。

## 二、连带更正：BE56 积压批次 10/10 CANCELLED 的原因

- 旧积压表达式把 GROUP 字段当数值用：`days_from_last_change(sign(eighth_pca_component_top1200_group513))`、
  `divide(subtract(ts_delta(PC_i,5),...), add(abs(PC_i),abs(PC_j)))` —— GROUP 类型做算术 ⇒ 平台整批 CANCELLED；
- 且这些字段描述是 top1200 口径，DEU 只有 TOP500；
⇒ **pv30 积压表达式作废**；但 pv30 作为**分组轴**完全可用（cov=1.0）。

## 三、★重大反直觉发现：tail 不是万能后处理（BE51 实证）

| 场景 | tail 效果 | 证据 |
|---|---|---|
| 比值型信号（institutions1 信念比值） | **有效**（论坛 1.65-1.67 vs 无 tail 1.44） | 论坛 88 次回测 |
| **rank 型水平腿**（I7 = ts_rank(holdings,252)） | **有害**（S 1.46 → -0.43） | BE51 5 臂全负 |

机制解释：事件型字段的并列块在**比值信号**里是噪声（分子分母同时为 0），在**水平排序腿**里起分散化作用
（无申报股 ≈ 现金腿，剪掉反而让组合集中）。
⇒ 论坛作者「所有事件型数据集都该加 tail」的猜想**必须按信号形态分型**，不能一刀切。

## 四、★另一个关键坑：连续权重会重造并列块

- BE57（institutions1 冠军配方压缩版）全弱（0.37-0.49）：我原想把二值掩码换成
  `multiply(ratio_sum, ts_sum(vec_avg(inst1_tradesignificance),66))` 连续权重 ——
  **多数股票显著性累计=0 ⇒ 乘积=0 ⇒ 重新制造巨大并列块**，信号被毁；
- 正确做法：**用 `greater(...)` 直接当乘子**（天然 0/1），既省算子又保留掩码语义；
  `multiply(ratio_sum, greater(ts_sum(vec_avg(sig),66),2.0))` = 12 算子 ✓。

## 五、历史冠军 d5WwzRMY 的完整配方（本次挖出）

```
tail(
  winsorize(
    group_rank(
      multiply(
        ts_sum(divide(vec_sum(inst1_valueeur),add(vec_sum(inst1_holdings),0.0001)),66),
        if_else(and(greater(<ratio_sum>,0),greater(ts_sum(vec_avg(inst1_tradesignificance),66),2.0)),1,0)
      ),
      oth455_partner_n2v_p50_q200_w1_pca_fact1_cluster_5
    ),
    std=2
  ),
  lower=0.25, upper=0.75, newval=0.5
)
```

- S1.73 / F1.40 / 2Y2.64 / sub1.20 / TO12.85% / failed_ra=0（**9 项硬闸全 PASS**）；
- 塔：INSTITUTIONS + OTHER；
- **死因：self 0.9287 撞自家 2rmGAPqN（2026-10-09 ACTIVE，同族只差窗口 220↔66 与 cluster 参数）**；
- 原式 **20 算子**，超 ≤12 硬约束 ⇒ 必须压缩（BE58 压缩版用 greater() 代替 if_else 达 12 算子）。

## 六、★DEU 结构性事实（决定后续一切）

1. **DEU 的 prod 相关性 ≈ 一次 self 检查**：prod 直方图几乎全在 [-0.1,0.2]，唯一 [0.9,1] 那条就是自家 alpha；
   prod_wall_ratio 0.8197 的主因是**自锁**而非外部拥挤；
2. 新候选的 prod >0.9 时，**先跑 check_self_correlation 看 top 对端**，能直接点名是哪颗自家件；
3. LLZ87QY9 去掉自锁后外部相关仍 ~0.69，仍贴 0.7 墙 ⇒ institutions1 信念族**内外双堵**；
4. ⇒ **新候选第一道筛必须是「与自家 20 颗 OS 的族级正交性」**，先于 IS 波。