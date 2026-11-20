# LLKRWzR2 双目标优化报告（2026-11-17 19:17 点名）

> 目标 A = 推到全闸；目标 B = 压算子。**判定：REJECT_SELF_WALL——self 墙结构性封死 + 指标天花板，12 条实测无解。零提交。**

## 一、原件画像

```
ts_target_tvr_decay(group_rank(subtract(0, ts_mean(board_departure_rate_3m_management, 66)), subindustry), target_tvr=0.1)
```
USA/TOP3000/d1/decay1/CROWDING。**4 ops，ATOM 纯血统**（单字段 `board_departure_rate_3m_management`，insiders 类）。

| 项 | 值 | 判定 |
|---|---:|---|
| S / F / 2Y / sub | 1.11 / 0.61 / 1.55 / 0.54 | **3 WARN**（S/F/2Y 全缺口） |
| **self（本地快筛）** | **0.7212 > 0.7** | **FAIL** |
| TO | 2.27% | 极低频 |
| 塔 | USA/D1/INSIDERS ×1.1，当季 **0**→1 | 不点亮（差 2 颗），边际 0 |

## 二、self 墙的性质（本轮核心发现）

top 相关 `ArN8Q8Y` = **2025-06 提交、现已 DECOMMISSIONED** 的 mdl177 fangma 件（S1.63/F1.41）——与本件**数据集、字段、机制完全不同**，是纯 PnL 层面的巧合重叠。

**12 条实测证明 self 对表达式旋钮完全钝感**：

| 变体 | self | 说明 |
|---|---:|---|
| 原件（66/subindustry） | 0.7212 | FAIL |
| **w=10 短窗** | 0.7237 | 反升 |
| **sector 轴+w10** | **0.7306** | **再反升** |

PnL 曲线的形状（低频缓变、负向截面）由字段本身决定——换窗/换轴只微调路径，不改变与 fangma 件的重叠本质。

⚠ 口径注记：`ArN8Q8Y` 已 DECOMMISSIONED。若平台 self 检查排除退场件，active-only 口径 top=`KmP73gj` 0.6747 可过——但本地工具设计为镜像平台口径且**无论如何 S/F 仍双 FAIL**，不必赌这个口径分歧。

## 三、指标救援实测（3 批 12 条）

| 通道 | 最优 | 结果 |
|---|---|---|
| **④d 窗口阶梯** | **w=21/10**（S 1.30→1.32，2Y 1.88→1.90，sub 0.75→0.77） | **2Y 闸已救活**（1.55→1.90）；短窗 10–22 全域平坦收敛 |
| **L1 sector 轴** | S **1.40** / F **0.94** / 2Y **1.93** / margin 50bp（`QP0Q9kAr`） | S +0.08 兑现但**缺 0.18**；F 缺 0.06 |
| zscore 替换 | S 0.95（`N1PORmGe`） | rank 类信号 zscore 灾难再证 |
| industry 轴 | S 1.36 | 介于两者 |
| tvr 0.14 | 与原件逐位同 | TO 2.3% < target，未激活（L3 对超低频件是 no-op） |
| w=126 | S 1.13 / sub 0.42 | 长窗更差 |

**天花板**：sector+w10 = S 1.40 / F 0.94——距闸 S 0.18 / F 0.06。剩余杠杆（L2 双窗需同字段双窗结构、L5 decay ±0.02）不足以补齐。

## 四、判定与建议

**REJECT_SELF_WALL，判死不提交**：
1. self 墙是字段级结构问题，表达式无解（0.72–0.73 全档稳定超线）；
2. 即使赌「平台排除退场件」的口径，S/F 仍双 FAIL；
3. 塔边际 0（差 2 颗点亮），不值得占配额。

**重启路径**：换字段族（`board_departure_rate_3m_*` 其它管理/董事子字段，或 if_else 掩码筛子集事件）才可能同时解 self 墙与指标；**同字段任何表达式级变体均已封死**（12 条留档）。

台账 `opmin_LLKRWzR2`（USA, REJECT_SELF_WALL）；全程 MCP 3 批 12 条，零临时脚本，零提交。

---

# 19:50 重启实测：换字段族 ⇒ self 墙升级定性，全字段族封死

## 实测 4 条（multisim，w10+sector 已证甜点结构）

| 变体 | S | F | 2Y | sub | self | 判定 |
|---|---:|---:|---:|---:|---:|---|
| **6m_management（WjlgAbvQ）** | **1.46** | **0.98** | 1.79 | 0.89 | **0.7645 更差** | 指标最优但 self 死；**active 口径 top KmP73gj 0.7278 也超线** ⇒ 连「平台排除退场件」的赌注都死了 |
| 1y_board（akaO1b51） | 1.33 | 0.91 | 1.88 | 0.56 | — | sub 崩 |
| board−management 差分（xAvnN3JW） | 0.33 | 0.09 | 0.15 | — | — | 两人群差分无信号 |
| 双人群联合（omaYNLxb） | 1.27 | 0.85 | 1.20 | 1.05 | — | 2Y 崩 |

## self 墙真维度（定性升级）

换**更低频**的 6m 字段（TO 2.27%→1.83%）后 self **0.7212→0.7645 反升** ⇒ 墙的维度不是字段/数据集，而是 **TO×方向**：

- 账号 OS 池存在「**超低频负截面**」族群：mdl177 fangma 族 10+ 颗（全部 DECOMMISSIONED，但 PnL 模板同源）、`KmP73gj`=`group_rank(fnd6_mrcta,subindustry)`（ACTIVE，TO 2.06%）、`dK5ExGg`/`lAXaGXx` 等慢频件——**直线型 PnL 互相关天然高**
- 本族信号（离职率负向）恰好落进该族群：频率越低 PnL 越直 ⇒ self 越高
- **反向操作（提 TO）数学上可行但经济上死**：returns 天花板 5.6%@TO1.8%，TO 提到 10%（self 可解）后 returns/TO=0.56 ⇒ F≈0.25，fitness 闸必死

## 最终判定

**REJECT_SELF_WALL（升级）**：`board_departure_rate_*` 全字段族 + 全表达式空间封死。重启唯一路径 = 换方向（正向）或换频率区间（TO 3%~8%），属**新信号设计**而非本字段优化。

台账已 merge 更新。全程 MCP 5 批 16 条，零提交。
