# ★平台硬限：单表达式算子上限 = 64（不是 12）

日期：2026-11-12
来源：BE135 v2 整批 CANCELLED 的根因

## 现象

multisim 10 臂，其中 S6（`M0×2 + B`，即重复主腿两次）报：

```
Expression with 67 operators exceeds limit of 64.
```

**且该错误触发 batch-kill：整批 10 臂全部 CANCELLED，只有出错那条是 ERROR。**

## 算子预算实测

本族冠军 `mLapjPLX` 的算子构成（估算）：

| 组件 | 算子数 |
|---|---:|
| A = group_rank(ts_delta(ts_mean(vec_avg(H),66),66),sector) | 4 |
| B = group_rank(ts_ir(vec_avg(H),66),sector) | 3 |
| C = group_rank(ts_mean(divide(SV1, add(add(SV1,SV2),add(SV3,SV4))),66),sector) | 10 |
| FR = group_rank(divide(1,add(days_from_last_change(vec_avg(H)),1)),sector) | 5 |
| M0 = add(add(multiply(A,C),multiply(C,FR)),B) | 3+1(含内嵌) |
| 外层 signed_power(Z2(CAPB(·)),1.3) | 7 |

⇒ 冠军 ≈ **44 算子**（C 的算术展开占大头，且 M0 里 C 出现两次 ⇒ C 的成本翻倍）。

**剩余预算 ≈ 20 算子** = 最多再挂 2-3 条轻腿（group_rank 级别），
**不能重复整块主腿**（M0 一份 ≈ 37 算子，两份即爆 64）。

## 纪律

1. **算子预算按"展开后"计**，重复引用同一子式会按次数翻倍计费。
2. 加腿前先粗算：`预估 = 现有44 + 新腿算子数`，>60 就别派，免得连坐整批。
3. 想"重复相加调权"时，**只能重复轻腿**（group_rank 单腿 ~4 算子），不能重复重块。
4. 修正此前认知：**平台算子上限是 64**（`wq-brain-ra-deu` 里 "算子 ≤12" 的口径指**组合腿数量/操作符种类**约束，不是平台硬限）。
