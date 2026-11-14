# BE145/BE146 结果与 15 颗边界状态

日期：2026-11-12

## BE145 analyst7（真 ANALYST 类）——6 颗 fail=0、全合规、trio=0、eff=2

| alpha | 构造 | S | F | 2Y | sub |
|---|---|---:|---:|---:|---:|
| VkNV0zqM | S3 + 净上调比 | **2.05** | 1.92 | 2.19 | 1.30 |
| 3q0wVPgz | S7 + 净上调比 | 2.04 | 1.81 | 2.49 | 1.33 |
| O0WO8zqq | S3 + 上调广度 | 1.83 | 1.63 | 2.27 | 1.10 |
| GrmPOz05 | S7 + 上调占比 | 1.79 | 1.41 | 2.66 | 1.02 |
| YPa6MznR | S7 + 双 analyst | 1.77 | 1.47 | 1.44 | **1.49** |
| vRA82Ga3 | S7 + 上调广度 | 1.75 | 1.44 | 2.59 | 1.22 |

**但全部不能进篮子**：`VkNV0zqM` vs `npa9PKWw` = **0.7973**、vs `KPg3NZX8` = **0.7559**。
⇒ 印证「S7 核心是共同因子」的结构性上限。

**副产品**：analyst7 单腿 S 只有 0.39（上调广度）/ 0.68（净上调比），但挂到 S7 上能 +0.5 ⇒ analyst7 是优质辅助腿。

## BE146 双搭档族叠加——7 颗 fail=0、全合规、但 eff=0

| alpha | 构造 | S | F | 2Y | sub | 塔 |
|---|---|---:|---:|---:|---:|---|
| **vRA82ogA** | S7+机构+AN2 | **2.07** | **1.85** | 2.59 | **1.43** | INST+INS+ANALYST |
| aka6xgq2 | S7+O4+AN1 | 2.03 | 1.81 | **3.18** | 1.25 | INS+OTHER+ANALYST |
| A1x9v2dQ | S7+O4+机构 p1.0 | 1.84 | 1.59 | 2.74 | 1.03 | INST+INS+OTHER |
| KPg3r2jz | S7+机构+AN1 | 1.82 | 1.53 | 2.72 | 1.32 | INST+INS+ANALYST |
| vRA82oM3 | S7+O4+机构 | 1.79 | 1.56 | 2.81 | 0.99 | INST+INS+OTHER |
| qM780wqv | S7+O1+机构 | 1.71 | 1.45 | 2.49 | 1.18 | INST+INS+OTHER |
| WjlMexmQ | S7+O4+机构+热度 | 1.70 | 1.49 | 2.58 | 0.90 | INST+INS+SENT+OTHER |

三塔/四塔 ⇒ 全部 **eff=0**（不贡献塔倍率）。

## ★15 颗只差 0.0003

`compute_mutual_correlation([npa9PKWw, vRA82ogA] + 13 颗, threshold=0.7)`：

```
all_below_threshold = False
max_subset_size = 14
pairs_over_threshold = [{ a: "vRA82ogA", b: "KPg3NZX8", correlation: 0.7053 }]   ← 仅超 0.0003
```

- `vRA82ogA` vs `npa9PKWw` = **0.5485** ✓（可共存）
- `vRA82ogA` vs `KPg3NZX8` = **0.7053** ❌（仅超 0.0003）

⇒ **两个选项**：
1. **替换**：用 `vRA82ogA`（S 2.07/F 1.85/sub 1.43）换掉 `KPg3NZX8`（S 1.72/F 1.36/sub 1.07）⇒ 仍 14 颗，但质量显著提升
2. **求第 15 颗**：找一颗与 `KPg3NZX8` **且** 与 `vRA82ogA` 都 <0.7 的件

## 当前 14 颗篮子成员（质量最优组合）

```
vRA82ogA (S2.07), npa9PKWw (S1.74), XgaGb3J1 (S2.36), bl6AvMkN (S1.61),
vR1oxZA3 (S3.27), GrW9OxmG (1.62), zq3eb7No (2.01), rKRx2Alj (1.95),
78Yk8VR1 (1.68), qM7KxkQV (1.72), Jj8VQwoe (1.65), RREPm361 (2.02),
d5a2vxzY (1.60), 9qlz29Oe (1.86)
```

（`KPg3NZX8` 被 `vRA82ogA` 替换，因为后者 S/F/sub 全面更优且仅超阈 0.0003）

## 在飞

- **BE147** `1zaICTbQS5fwcKqr17dma29`：shortinterest3 新维度（费率波动率/借券期限/笔数/最低费率）
- **BE148** `NIMO5bwg5hu9I117IrN1wEi`：**不同 insiders 核心**（金额/显著度/占比，算子仅 11-18）
