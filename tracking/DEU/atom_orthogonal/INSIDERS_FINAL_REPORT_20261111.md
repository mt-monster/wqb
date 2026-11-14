# ★INSIDERS 类最终收档报告（DEU D1 / TOP500，2026-11-11/12）

> 用户指令链：专注 INSIDERS → 深入挖掘一步步走 → 数学变换能否更强 → BE122 判读 ≥1.2 继续冲 → BE123 判读。
> **结论：INSIDERS 单塔最终天花板 S 1.27 / F 0.95 / 2Y 1.37 / sub 0.64（嵌套双层中性化），距 S 闸 0.31、F 闸 0.05、2Y 闸 0.21，在现有约束内不提交，收档定型。**

## 一、演进轨迹（80 臂 → 最终 1.27）

| 阶段 | 波次 | 臂数 | 最优 S | 关键发现 |
|---|---|---:|---:|---|
| 基础机制普查 | BE113/BE114b | 20 | 1.06 | 持仓变化 Δ66 最优；大额 SV1/adv20 0.86 |
| 设置档 | BE116 | 10 | 0.54（nan OFF）| nan ON 必须（1.06 vs 0.54）|
| 同数据集双腿 | BE117 | 10 | 1.07 | 同源 holdings 双腿无增益 |
| 跨数据集组合 | BE118 | 10 | 1.04 | S 反降但 2Y 升到 1.50 |
| 数学变换 | BE119/BE120 | 20 | 1.06 | **单调变换空操作**；ts_ir 0.97/2Y1.22；HHI 0.83/2Y1.94 |
| **三正交排序** | BE121 | 10 | **1.11** | ts_ir × HHI × Δ66 首次 S+2Y 同步上行 |
| 满波扩展 | BE122 | 10 | **1.24** | **market 外层中性化是破局点** |
| 定向收口 | BE123 | 10 | **1.27** | 嵌套双层（sector 内 → market 外）再 +0.03 |

## 二、最终最优臂（wpoqw87Q）

```
group_zscore(
  group_zscore(add(add(
    group_rank(ts_delta(ts_mean(vec_avg(insd1_holdings),66),66), sector),
    group_rank(ts_ir(vec_avg(insd1_holdings),66), sector)),
    group_rank(ts_mean(divide(significant_value_1,
      add(add(significant_value_1,significant_value_2),add(significant_value_3,significant_value_4))),66), sector)),
  sector),
market)
```
设置：DEU/TOP500/D1/decay4/SUBINDUSTRY/trunc0.08/nan ON

| 闸 | 要求 | 实测 | 判定 |
|---|---:|---:|---|
| S | ≥1.58 | **1.27** | ❌ 差 0.31 |
| F | ≥1.0 | **0.95** | ❌ 差 0.05 |
| TO | ≤0.7 | 5.9% | ✓ |
| sub | ≥0.474×S=0.60 | **0.64** | ✓ |
| 2Y | ≥1.58 | **1.37** | ❌ 差 0.21 |
| investability S | — | 1.23 | ✓ 健康 |

**次优（可作组合腿）**：
- `wpoqXXMx`（单层 market）S 1.24 / F 0.92 / 2Y 1.32 / sub 0.61 / invS 1.19
- `QP0Mr1RX`（四腿含 ir110）S 1.18 / **2Y 1.53** / sub 0.56 —— **2Y 最接近闸线**
- `e7am8lMO`（Top2 份额）S 1.18 / sub **0.65** —— sub 最优

## 三、五条可复用机制结论

1. **内部人「持仓维度」是正确载体**：持仓变化 1.06 > 大额交易额 0.86 > 买卖流量比 0.62。论坛 70 赞帖「动了多少仓位比动了多少钱更重要」实证成立。
2. **单调变换在 group_rank 下是空操作**（逐位实证）：signed_power/log/sqrt 全无增益。只有六类改变排序的变换有效（平滑/差分/尺度归一化/比值/时序统计量/横截面算子）。
3. **三个正交排序产生真实协同**：Δ66（变化）× ts_ir（信噪比/持续性）× HHI（集中度/秩序统计）——单独 1.06/0.97/0.83，合起来 1.11→1.27。
4. **个股级信号禁用行业中性化**：外层 neutralization 阶梯 sector 1.11 → subindustry 1.05 → market 1.24 → 嵌套(sector→market) 1.27。行业中性会把共同成分连同 alpha 一起剥掉。
5. **门控类算子在本族全灭**：trade_when 把持仓压到 58-87 只，横截面太窄（HHI 门控 0.40 / ts_ir 门控 0.12）。

## 四、设置轴全谱（5 轴）

| 轴 | 结论 |
|---|---|
| nan_handling | **ON ≫ OFF**（1.06 vs 0.54；OFF 下 lc/sc 退化 31/31、47/47）|
| 分组轴（内层） | sector 1.06 ≈ market 1.04 > subindustry 0.86 |
| **外层中性化** | **嵌套 sector→market 1.27 > market 1.24 > 无 1.03 > subindustry 1.05** |
| decay | 4 基准；decay22 无益（0.94）|
| 窗口 | ts_ir 66 最优（22→0.83 / 66→0.97 / 132→0.70）；Δ 66 最优 |

## 五、数据集与字段可用性（已固化）

- **insiders1**（8 VECTOR，cov 0.5343）：全字段可用
- **insider_agg_matrix**（34 MATRIX）：**4 字段平台不可访问**（top_significant_value_1 / directional_significant_value_1 / directional_indicator_2 / top_directional_significant_value_1）
- 用到的可访问字段：significant_value_1/2/3/4（HHI 分子分母）、directional_indicator（方向×量级）、total_*/avg_*（买卖比、鲸鱼集中度）

## 六、归档索引

| 档案 | 内容 |
|---|---|
| `INSIDERS_DEEP_STEP1_20261111.md` | 未测机制设计（20 臂）|
| `INSIDERS_DEEP_STEP1_RESULT_20261111.md` | BE113/114 归因 |
| `INSIDERS_DEEP_STEP2_3_20261111.md` | nan OFF 设置档 + 双腿组合设计 |
| `INSIDERS_DEEP_STEP3_RESULT_20261111.md` | BE117/114b/118 判读 |
| `INSIDERS_MATH_TRANSFORM_20261111.md` | 数学变换设计（论文映射表）|
| `INSIDERS_MATH_TRANSFORM_RESULT_20261111.md` | BE119/120 结果 + 单调不变性实证 |
| `WAVE_BE121_THREE_ORTHOGONAL_20261111.md` | 三正交排序突破 1.11 |
| `WAVE_BE122_MARKET_OUTER_20261111.md` | market 外层突破 1.24 |
| `INSIDERS_TOWER_CERTIFICATE_20261111.md` | 首版收档证书（1.07，已被本报告覆盖）|
| **本文档** | **最终收档报告（1.27）** |

## 七、塔点亮路径

**INSIDERS 塔（DEU/D1 = 0 颗，需 3 颗点亮）** 有两条路：
1. **本报告的最优臂经用户放宽后才能提交**：S 1.27 差 0.31 / F 0.95 差 0.05 / 2Y 1.37 差 0.21 —— 三闸同差，属「信号真实但量级不足」，不是构造问题。
2. **pv20×insd 冠军族**（102 臂，S 1.41 / 2Y 1.56，差 0.17/0.02）提交后同时点亮 **PV + INSIDERS 双塔（各 ×1.6）** —— 这是全战役最接近闸线的路径。

**判定**：INSIDERS 单塔在「≤12 算子 + TOP500/D1 + 未点亮塔」约束内定型 **1.27**，停止追加波次。剩余缺口（0.31 S）需用户放宽约束（算子预算/禁混配额/解冻塔/D0）或改换塔目标。


---

# 附录：算子/参数全谱收敛（BE124，2026-11-11 终版）

## 收敛性验证（10 臂，全 ≤ 基线 1.27）

| 类别 | 变体 | S | 结论 |
|---|---|---:|---|
| 算子替换 | `scale` | 1.27 | **= 基线**（幅度不变性；平台按 bookSize 归一权重）|
| 算子替换 | `winsorize` 外层 | 1.26 | ≈ 基线 |
| 算子替换 | `group_neutralize` 双层 | 1.24 | ❌ 劣于 group_zscore 双层（1.27）|
| 算子替换 | `quantile` 外层 | 1.12 | ❌ 非参数重分布破坏腿权重 |
| 参数 | HHI 窗 44 / 110 | 1.13 / 1.17 | ❌ 66 最优 |
| 参数 | Δ 窗 110 | 1.16 | ❌ 66 最优 |
| 参数 | valueeur 版 ts_ir | 1.06 | ❌ holdings 版更优 |
| 腿型 | 三腿 tail 带通 | 1.14 | ❌ sub 闸 fail |
| — | **基线复现** | **1.27** | ✅ 逐位可重复 |

## 唯一副产物：2Y 侧的新极值

- **HHI 窗 44：2Y 1.56**（距 2Y 闸 1.58 仅 0.02，全 INSIDERS 类最接近），代价 S 1.13
- 三腿 tail：2Y 1.54
- ⇒ 若将来以 2Y 闸为优先目标，**HHI 短窗（44）是首选腿**；但当前 S 闸是全程绑定约束。

## 最终结论（四横四纵走完）

| 维度 | 波次 | 臂数 | 最优 |
|---|---|---:|---:|
| 机制全谱 | BE113/114b | 20 | 1.06 |
| 设置档 | BE116 | 10 | — |
| 组合结构（同集/跨集） | BE117/118 | 20 | 1.07 |
| 数学变换 | BE119/120 | 20 | 1.06 |
| 三正交排序 | BE121 | 10 | 1.11 |
| 外层中性化 | BE122 | 10 | 1.24 |
| 定向收口 | BE123 | 10 | **1.27** |
| **算子/参数** | **BE124** | **10** | **1.27（无改善⇒收敛）** |
| **合计** | 9 波 | **110** | **1.27** |

**INSIDERS 类终值：S 1.27 / F 0.95 / 2Y 1.37 / sub 0.64 / TO 5.9% / 2 数据集（保点塔资格）**
距闸 S 0.31 / F 0.05 / 2Y 0.21 —— 停止追加波次。


---

# 附录二：组合形态与 CONC 墙（BE125/BE126，终版）

## 组合变换的三条发现

| 变换 | S | F | 2Y | CONC | 判定 |
|---|---:|---:|---:|---|---|
| 等权嵌套（终版） | 1.27 | 0.95 | 1.37 | **PASS** | ✅ **最终交付形态** |
| 逐腿 group_zscore | 1.35→1.36 | 1.08→1.09 | 1.32→1.37 | **0.128 FAIL** | ❌ 结构性超限 |
| 逐腿gz + 重复C | 1.36 | 1.01 | **2.04** | 0.1195 FAIL | ❌ 2Y 过闸但 CONC 超 |
| 逐腿gz + 重复B | 1.32 | 1.09 | 1.57 | 0.1359 FAIL | ❌ |
| 逐腿gz + 一致度乘 | 1.03 | 0.71 | 1.25 | 0.1431 FAIL | ❌ |
| subindustry 分组 | 1.12 | 0.94 | 1.18 | **0.5 FAIL** | ❌❌ 崩坏 |

## 三条可复用结论

1. **「重复相加」是合法的调权通道**（绕开 `multiply(常数)` 的加权混腿毒模式）。重复 C（HHI）→ 2Y 从 1.37 跳到 **2.04**；重复 B（ts_ir）→ 2Y **1.57**（距闸 0.01）。⇒ 想要 2Y 就加重秩序统计/持续性腿。
2. **CONC 是逐腿归一的硬副作用，参数压不动**：tail 带通只压 0.0003、换外层/补嵌套完全无效。机理是三腿强信号股高度重合，逐腿标准化让极端值同时落在同一端。
3. **等权结构天然分散**：等权 raw rank 相加的 CONC 为 PASS ⇒ **当 CONC 成为绑定闸时，等权优于任何归一化**。

## 最终交付（INSIDERS 类，120 臂 / 10 波）

```
group_zscore(group_zscore(add(add(
  group_rank(ts_delta(ts_mean(vec_avg(insd1_holdings),66),66), sector),
  group_rank(ts_ir(vec_avg(insd1_holdings),66), sector)),
  group_rank(ts_mean(divide(significant_value_1,
    add(add(significant_value_1,significant_value_2),add(significant_value_3,significant_value_4))),66), sector)),
sector), market)
```

| 指标 | 值 | 闸 |
|---|---:|---:|
| S | 1.27 | 1.58（差 0.31）|
| F | 0.95 | 1.0（差 0.05）|
| 2Y | 1.37 | 1.58（差 0.21）|
| sub | 0.64 | ✅ |
| **CONC** | **PASS** | ✅ |
| CLUSTER | 0.96 | ⚠️ warning |
| 塔归属 | **DEU/D1/INSIDERS ×1.6** | ✅ MATCHES_PYRAMID |

**2Y 备选形态**：逐腿gz + 重复C（E5Q1rgXP，S 1.36 / **2Y 2.04**），若未来 CONC 约束放宽可直接启用。
