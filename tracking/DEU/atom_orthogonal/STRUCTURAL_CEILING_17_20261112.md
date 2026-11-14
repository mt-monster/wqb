# DEU 20 颗的结构性天花板：17 个方向判死后的收敛结论

日期：2026-11-12 终章

## 一、核心结论：DEU 只对「分析师预估数值的水平与变化」定价

累计 **17 个方向**判死，全部落在 0.21-1.62 区间：

| # | 方向 | 数据集 | 最高 S |
|---:|---|---|---:|
| 1 | RISK 塔 | risk60/risk88 | 0.72 |
| 2 | SENTIMENT 塔 | sentiment27/sentiment7 | 0.72 |
| 3 | INSTITUTIONS 塔 | institutions6（**cov 1.0**）/fund_holdings_panel | 0.72 |
| 4 | NEWS 塔 | news104（**cov 0.963**）/news17/news18 | 0.58 |
| 5 | PEAD 正向 | act_q_*_surprisemean | 0.44 |
| 6 | PEAD 反向 | analyst_earnings_ibes 反转 | 1.30 |
| 7 | rec 评级族 | analyst7 rec_*（cov 1.0）| 1.03 |
| 8 | est_q 季度族 | analyst7 est_q_* | 0.30 |
| 9 | net/gps/nav/ent/opr/grm/roa 主轴 | analyst7 | 1.54（Y2 崩）|
| 10 | arm_score/recommendation | predictive_starmine | 0.96 |
| 11 | revenue 口径 | predictive_starmine | 1.33 |
| 12 | estimate_change 独占基底 | predictive_starmine | 1.62（Y2 0.81）|
| 13 | FUNDAMENTAL 塔 | fundamental6 ROE/ROA/净利率 | **0.37**（TO 2%）|
| 14 | insiders 双重中性化 | insiders1+insider_agg | 1.37 |
| 15 | insiders × 应计质量 | insiders + eq_vr | 1.37 |
| 16 | 分析师分歧形态 | analyst_factor_signals skewness/coeff_var/asymmetry | 0.56 |
| 17 | model264 分档字段 | model264（380 字段 cov 1.0）| 0.64 |

## 二、唯一的两个有效机制

| 机制 | 数据集 | 塔 | 强度 | 变体空间 |
|---|---|---|---:|---|
| **预测意外 + 预估修正幅度** | predictive_starmine | MODEL | S 1.66-1.86 | 已挖尽（腿数/窗口/中性化/幂次全部试过）|
| **est_12m 水平 + 4周修正** | analyst7 | ANALYST | S 1.87-2.02 | 已挖尽（32 个指标族的有效子集只有 ebi/ebt/pre）|

**互相关结构（这是 20 颗无法达成的根本原因）：**
- analyst7 内部任意两件：0.87-0.98（同源）
- starmine 内部任意两件：0.65-0.83（共享 surprise 腿）
- analyst7 × starmine：0.13-0.26（真正的正交，但只有这两簇）

## 三、为什么 20 颗做不到

要达到 20 颗全对 <0.7，需要 **≥4 个互不相关的机制簇**（每簇 2-3 颗）。DEU 实测只有 **2 个**：

```
簇 A（analyst7 est_12m）:  RREPm361, zq3eb7No, 6XM87Zb7, d5aXXzaw, 3q0bbP0z, e7appGa6 ...
                            ↑ 内部 0.87-0.98，只能取 1 席
簇 B（starmine）:            qM78pjkV, RRe3L5kg, 2r50PAzJ, VkN9waPY, Jj8w52Me, omapv6W5 ...
                            ↑ 内部 0.65-0.83，只能取 2-3 席
```

加上 17 颗存量（多数是 insiders/analyst/starmine 的混合）——这 17 颗之间已经用掉 0.7 阈值的余量。

## 四、实际战果

| 项 | 值 |
|---|---|
| 平台合格件总数 | **20**（15 UNVERIFIABLE_404 + 5 ALREADY_SUBMITTED）|
| 互相关 <0.7 可交付篮子 | **17** |
| 本战役新挖且入篮的 ATOM | **2**（2r50PAzJ 1.83 / Jj8w52Me 1.67）|
| 本战役新挖但被互相关排除 | 2（6XM87Zb7 1.87 冲突 zq3eb7No 0.78；VkN9waPY 1.66 冲突 2r50PAzJ 0.83）|
| 本战役新挖的合格件（含变体）| ≥10 颗（analyst 4 + starmine 6）|

## 五、两条新增可复用杠杆（跨区资产）

### A. 双层中性化破 2Y
`group_zscore(group_neutralize(group_zscore(X, sector), subindustry), sector)`
→ starmine Y2 1.57 → 1.63。仅对「单层 sector + 多腿相加」MODEL 结构有效。

### B. 反转 × 应计质量 破 IS_LADDER
`multiply(reverse(反转腿), eq_vr_dlra1_accruals_component)`
→ Y2 1.47 → 1.77。**必须乘法**；加性并入崩到 0.50。

## 六、若要继续逼近 20 颗，唯一可行路径

**换 region**（用户明令不得换，故不列）。

**在 DEU 内的残余可能**（成功率低，已标注依据）：
1. 接受 `6XM87Zb7` 与 `zq3eb7No` 的 0.78 相关（牺牲一次越线换 1 颗）→ 18 颗
2. 同时接受 `VkN9waPY` 与 `2r50PAzJ` 的 0.83 → 19 颗
3. 再接受 `0mPqGEgq` 与 `d5apW38x` 的 0.72 → 20 颗

⇒ **20 颗只能通过放宽互相关阈值达成，不存在第 4 个独立机制簇。**
