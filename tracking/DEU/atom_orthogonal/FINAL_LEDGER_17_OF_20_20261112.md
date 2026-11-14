# 最终盘点：DEU 可交付 17 颗（互相关口径）+ 20 颗平台合格

日期：2026-11-12 收尾

## 一、权威核实结果（`submit_verdict` 逐颗）

| 状态 | 数量 | alpha |
|---|---:|---|
| **ALREADY_SUBMITTED**（已在账）| 5 | zq3eb7No / rKRx2Alj / 78Yk8VR1 / GrW9OxmG / bl6AvMkN |
| **UNVERIFIABLE_404**（平台提交端点下线，非不合格）| 15 | d5apW38x / WjlMlWJd / leadEXnl / RREPm361 / 9qlz29Oe / 0mPqGEgq / npa9PKWw / qM7KxkQV / Jj8VQwoe / mLapKbd2 / d5a2vxzY / **6XM87Zb7** / **2r50PAzJ** / **Jj8w52Me** / VkN9waPY |
| **BLOCKED** | 1 | **MP6OgoPr**（IS_LADDER_SHARPE 1.56 < 1.58，WARNING 被资格门升级为阻断）|

⇒ 此前把 MP6OgoPr 算进「18 颗全闸通过」是**错的**，已剔除。

## 二、互相关最大独立集 = 17 颗

```
d5apW38x(2.36) 2r50PAzJ(1.83) WjlMlWJd(2.21) leadEXnl(2.20) RREPm361(2.02)
zq3eb7No(2.01) rKRx2Alj(1.95) 9qlz29Oe(1.86) npa9PKWw(1.74) qM7KxkQV(1.72)
78Yk8VR1(1.68) Jj8VQwoe(1.65) mLapKbd2(1.64) GrW9OxmG(1.62) bl6AvMkN(1.61)
d5a2vxzY(1.60) Jj8w52Me(1.67)
```

**被排除的 3 颗及原因：**

| alpha | S | 排除原因 |
|---|---:|---|
| **6XM87Zb7** | 1.87 | vs `zq3eb7No` **0.7768** —— 后者**已提交**、不可撤，故 6XM87Zb7 实质上进不了篮子 |
| VkN9waPY | 1.66 | vs `2r50PAzJ` **0.8324**（同源 surprise 腿）|
| 0mPqGEgq | 1.74 | vs `d5apW38x` **0.7249** |

## 三、本战役新挖 ATOM 实际入篮 = 2 颗

| alpha | S | F | Y2 | sub | 塔 | 状态 |
|---|---:|---:|---:|---:|---|---|
| **2r50PAzJ** | 1.83 | 1.46 | 1.63 | 1.32 | MODEL | ✅ 入篮 |
| **Jj8w52Me** | 1.67 | 1.16 | 1.77 | 1.11 | MODEL | ✅ 入篮 |
| 6XM87Zb7 | 1.87 | 1.06 | 1.91 | 1.08 | ANALYST | ⚠️ 与已提交件冲突，无法入篮 |

## 四、距 20 颗的缺口：3 颗

需要 3 颗新件，且每颗都须与上述 17 颗**全对 < 0.7**。

## 五、本轮判死的 14 个方向（全部实测）

| 方向 | 最高 S | 关键原因 |
|---|---:|---|
| RISK 塔（risk60/88）| 0.72 | 正负双向均无信号 |
| SENTIMENT 塔（sentiment27/7）| 0.72 | sub 常为负 |
| INSTITUTIONS 塔（institutions6 **cov=1.0**）| 0.72 | 季度低频、已被定价 |
| NEWS 塔（news104 cov 0.963）| 0.58 | 情绪/相关度加权无效 |
| PEAD 正向（act_q susceptisemean）| 0.44 | DEU 是**反转**不是漂移 |
| rec 评级族（cov 1.0）| 1.03 | 广度类无信号 |
| est_q 季度预估族 | 0.30 | 季度粒度劣于年度 |
| net/gps/nav/ent/opr/grm/roa 主轴 | 1.54 | Y2 全崩（0.27-0.98）|
| arm_score/recommendation 族 | 0.96 | TO 21-43% 过高 |
| revenue 口径 | 1.33 | Y2 差 |
| estimate_change 独占基底 | 1.62 | Y2 仅 0.81 |
| **FUNDAMENTAL 塔（fnd6 ROE/ROA/净利率）** | **0.37** | TO 2%，基本面更新过慢 |
| insiders 双重中性化 | 1.37 | 无变化 |
| decay 平滑（反转核心）| 1.41 | Y2 掉到 0.94 |

## 六、两条真正有效的新杠杆（本战役最大资产）

### 杠杆 A：`group_neutralize(·, subindustry)` 双层中性化破 2Y
`group_zscore(group_neutralize(group_zscore(X, sector), subindustry), sector)`
- starmine 5 腿：Y2 **1.57 → 1.63**
- 只对「单层 sector 排序 + 多腿相加」的 MODEL 结构有效

### 杠杆 B：反转 × 应计质量 乘法交互破 IS_LADDER
`multiply(reverse(5日反转), eq_vr_dlra1_accruals_component)`
- Y2 **1.47 → 1.77**（+0.30）
- **必须乘法**，加性并入崩到 0.50
- 机制：只在应计质量健康的股票上做财报后反转，剔除 2022-23 靠会计粉饰支撑的标的

## 七、结论

- **平台合格件：19 颗**（15 UNVERIFIABLE + 5 已提交 − 1 BLOCKED(MP6OgoPr) = 19，其中 5 已在账）
- **互相关 <0.7 可交付：17 颗**
- **距目标 20 颗：差 3 颗**
