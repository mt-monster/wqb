# institutions1 信念族关闭（最终判定，结构已完全查明）

> 2026-11-11 读 2rmGAPqN / LLZ87QY9 / d5WwzRMY 三件原始表达式后确认。

## 三件同源结构

```
tail(winsorize(group_rank(multiply(
  ts_sum(divide(vec_sum(inst1_valueeur),add(vec_sum(inst1_holdings),0.0001)), W),      # W = 220 | 66
  if_else(and(greater(ts_sum(<同上比值>,W),0),
              greater(ts_sum(vec_avg(inst1_tradesignificance),66),2.0)),1,0)          # 二值门
), CLUSTER), std=2), lower=0.25, upper=0.75, newval=0.5)
```

| alpha | 差异 | 状态 |
|---|---|---|
| 2rmGAPqN | W=220, cluster=oth455_..._fact2_cluster_20 | **ACTIVE（10-09）** |
| LLZ87QY9 | W=66, cluster=..._fact1_cluster_20 | self 0.9144 / prod 0.9144 |
| d5WwzRMY | W=66, cluster=..._fact1_cluster_5 | S1.73 全闸通过，self 0.9287 |

## 关闭理由（三重，任一独立成立）

1. **槽位自锁**：比值腿（inst1_valueeur ÷ inst1_holdings 的 ts_sum）主导全部收益流，
   任何 inst1 比值构造与 2rmGAPqN 的相关必然 ≥0.8 ⇒ 无法共存（self 闸 0.7）；
2. **簇轴是承重结构**：把 oth455 簇换成 industry / sector / pv30 簇后 S 从 1.73 塌到 0.43-0.70
   （BE58 六臂）⇒ 不能靠换轴脱身；
3. **算子预算**：原式 20 算子（比值写 3 遍），≤12 硬约束下任何压缩都改变信号结构
   （BE57 连续权重版 0.43-0.49 / BE58 greater() 版 0.43-0.70）；
4. 外部亦堵：LLZ87QY9 去掉自锁后外部相关仍 ~0.69（贴 0.7 墙）。

⇒ **institutions1 信念族关闭（不可破）**。BE49/BE57/BE58 三波共 22 臂为证。