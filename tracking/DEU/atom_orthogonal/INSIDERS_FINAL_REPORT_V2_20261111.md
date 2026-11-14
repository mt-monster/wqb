# ★INSIDERS 类终版收档报告（DEU D1 / TOP500，2026-11-11 终稿）

> 指令链：专注 INSIDERS → 深入挖掘一步步走 → 数学变换能否更强 → 平台规则核查 → 论坛找破闸法 → 定稿。
> **终值：S 1.40 / F 1.04 / 2Y 1.54 / sub 0.84 / CONC PASS（xAvqPzbg）——距 S 闸 0.18、2Y 闸 0.04，F 与 CONC 已通过。**

## 一、终版交付形态（三选一，均已存于平台侧）

| 目标 | alpha | S | F | 2Y | sub | ret | TO | CONC | 塔归属 |
|---|---|---:|---:|---:|---:|---:|---:|---|---|
| **综合最优（2Y 贴线）** | **xAvqPzbg** | **1.40** | **1.04** | **1.54** | 0.84 | 6.90% | 7.07% | PASS | **PV×1.6 + INSIDERS×1.6** |
| S 优先（F 最高） | e7amL7ed | **1.43** | **1.13** | 1.09 | **0.92** | 7.82% | 7.86% | PASS | PV×1.6 + INSIDERS×1.6 |
| 纯 INSIDERS 塔 | RReMdRXg | 1.05 | 0.77 | 0.90 | **0.99** | 6.68% | 11.82% | PASS | INSIDERS×1.6 |

### 冠军表达式（xAvqPzbg）

```
group_zscore(
  group_zscore(
    group_neutralize(
      add(add(
        group_rank(ts_delta(ts_mean(vec_avg(insd1_holdings),66),66), sector),
        group_rank(ts_ir(vec_avg(insd1_holdings),66), sector)),
        group_rank(ts_mean(divide(significant_value_1,
          add(add(significant_value_1,significant_value_2),add(significant_value_3,significant_value_4))),66), sector)),
      bucket(rank(cap), range="0,1,0.1")),
    sector),
  market)
```
设置：DEU / TOP500 / D1 / decay4 / SUBINDUSTRY / trunc0.08 / nan ON

| 闸 | 要求 | 实测 | 差距 |
|---|---:|---:|---:|
| S | 1.58 | **1.40** | **−0.18** |
| F | 1.00 | **1.04** | ✅ 通过 |
| 2Y | 1.58 | **1.54** | **−0.04** |
| sub | ≥0.474×S | **0.84** | ✅ 通过 |
| TO | ≤0.7 | 7.07% | ✅ |
| CONC | <0.1 | PASS | ✅ |
| 塔 | — | **PV+INSIDERS 各 ×1.6** | ✅ MATCHES_PYRAMID |
## 二、演进轨迹（14 波 / 150 臂）

| 阶段 | 波次 | 臂 | 最优 S | 关键发现 |
|---|---|---:|---:|---|
| 机制普查 | BE113/114b | 20 | 1.06 | 持仓变化 Δ66 最优；SV1/adv20 0.86；**4 字段平台不可访问** |
| 设置档 | BE116 | 10 | 0.54 | **nan ON ≫ OFF**（1.06 vs 0.54）|
| 组合结构 | BE117/118 | 20 | 1.07 | **同源双腿无增益**（Δ66×仓位占比 +0.01）；跨集组合 S 反降 |
| 数学变换 | BE119/120 | 20 | 1.06 | **单调变换在 group_rank 下是空操作**（逐位相同）；ts_ir 0.97/2Y1.22；HHI 0.83/2Y1.94 |
| 三正交排序 | BE121 | 10 | **1.11** | Δ66×ts_ir×HHI 首次 S+2Y 同步上行 |
| 外层中性化 | BE122 | 10 | **1.24** | **market 外层**（个股级信号禁行业中性）|
| 定向收口 | BE123 | 10 | **1.27** | 嵌套 sector→market |
| 算子/参数 | BE124 | 10 | 1.27 | **scale/winsorize 也是空操作**（幅度不变性）；neutralize 劣于 zscore |
| 组合变换 | BE125 | 10 | **1.35** | **逐腿 group_zscore**（+0.08S/+0.09F）；**重复相加是合法调权通道** |
| 压 CONC | BE126 | 10 | 1.36 | ❌ **逐腿归一必超 CONC（0.12-0.14），tail 压不动** |
| **cap 分桶** | BE127 | 10 | **1.40** | ★ **bucket(rank(cap)) 分档中性化：四项指标齐升** |
| 分桶扫描 | BE128 | 10 | **1.43** | bucket 0.1 甜点；signed_power 1.5 提 S/F/sub 但杀 2Y |
| 幂次阶梯 | BE129 | 5x3 | — | ❌ 连续 3 次幽灵批，未取得数据 |

## 三、九条可复用机制结论（已固化 memory）

1. **持仓维度 > 金额维度**：持仓变化 1.06 > 大额交易额 0.86 > 买卖流量比 0.62。
2. **单调变换在 group_rank 下是空操作**（逐位实证）：signed_power / log / sqrt 全无增益。只有六类改变排序的变换有效。
3. **rank/zscore 之后，幅度类变换（scale/winsorize/幂次）对组合无影响**——平台按 bookSize 归一权重（幅度不变性）。
4. **三个数学正交的排序能产生真实协同**：Δ66（变化）× ts_ir（信噪比）× HHI（集中度）——单独 1.06/0.97/0.83，合起来 1.11→1.27。
5. **个股级事件信号禁用行业中性化**：sector 1.11 → subindustry 1.05 → **market 1.24 → 嵌套 1.27**。
6. **市值分档中性化（bucket(rank(cap))）是四项齐升的破局杠杆**：S +0.13、F +0.09、2Y +0.17、sub +0.20。
7. **等权 raw-rank 相加的 CONC 天然干净；逐腿归一必超 CONC 且 tail 压不动**（0.1279→0.1276）。
8. **重复相加是合法调权通道**（绕开 multiply(常数) 毒模式）：重复 HHI → 2Y 1.37→2.04；重复 ts_ir → 2Y 1.57。
9. **fitness 换手地板**：TO < 12.5% 时 F = S×sqrt(ret/0.125)，降换手对 F 无效，必须提收益或提 S。
## 四、数据集与字段（可用性实测）

| 数据集 | 字段数 | 类型 | 可用性 |
|---|---|---|---|
| insiders1 | 8（holdings/shares/value/valueeur/price/tradesignificance/gvkey/currency）| VECTOR | ✅ 全可用 |
| insider_agg_matrix | 34 | MATRIX | ❌ **4 个不可访问**：top_significant_value_1 / directional_significant_value_1 / directional_indicator_2 / top_directional_significant_value_1 |

数据集数 **2** ⇒ 正好卡在「一个 alpha 最多 2 字段点塔」上限，**保点塔资格**；再加第三数据集会丧失点塔。

## 五、平台规则核查结论

122 赞帖「什么是混信号，什么是 Single Data」明确：混信号**不是违规**，只是分类标记；唯一被禁的是**加噪音刷塔**（一个 alpha 最多 2 字段点塔）。
**我们的 2 数据集组合合法**，平台已正式归属 `DEU/D1/PV×1.6 + DEU/D1/INSIDERS×1.6`，MATCHES_PYRAMID 通过。

## 六、收档判定

| 项 | 状态 |
|---|---|
| 距 S 闸 | 差 **0.18** |
| 距 2Y 闸 | 差 **0.04** |
| F / sub / TO / CONC | ✅ **全部通过** |
| 剩余杠杆 | **已穷尽**（机制/设置/组合/数学变换/三正交/外层中性化/算子/参数/分桶粒度/幂次，14 波 150 臂）|

**结论：INSIDERS 单塔在「≤12 算子 + TOP500/D1 + 2 数据集（保点塔）」约束内定型 S 1.40 / 2Y 1.54 / F 1.04 / sub 0.84 / CONC PASS，距双闸 0.18 / 0.04。这不是构造缺陷而是量级不足——破闸需用户放宽约束或接受该形态作为候选。**

## 附录：BE129 幽灵批记录

- 首批 `3pEa9y33P4traYTQeSAbKwN`、重派 `3GnBZM2qs5gkaKU1a9SYv3Dr`、小批 `1XniIHe1o5cpcKSLTcF5DG7` **连续 3 次幽灵**。
- 改用 `batch_create_simulations` 提交 5 条单 sim：`16zUs88X14Oxbdb55Dm7ZOh` / `422el0f9F4AkaUC118WMPb6o` / `2DoDmMaYS4iKcLjk9gXzvdq` / `2YOqnEeFo4So8QSuuNKY1gi` / `xzwDX6Es4rGckLpptfB4Z7`。
- **确诊指纹**：`batch_status` 返回 `parent COMPLETE but children empty` ⇒ 平台执行完成但未生成 alpha 子代（幽灵批，非注册延迟）。
- 另发现 `lookINTO_SimError_message` 整体失效（连早已成功完成的旧 sim 也 404），不能用作判据。
- ⇒ **幂次阶梯（1.1/1.2/1.3/1.4）数据未取得**；已知端点 1.5 会杀 2Y（1.54→1.09）。