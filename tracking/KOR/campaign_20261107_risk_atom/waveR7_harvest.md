# Wave R7 收割 + 归因（COMPLETE 8/8 · **四条负面结论，锁定锚点上限**）

- multisim: 3Ymarsc054gBcyD18KAsVEYc · 设置同 R4（KOR/TOP600/D1 · STATISTICAL · decay4 · trunc0.08）

## 读数
| id | S | F | TO | 2Y | raFail | 骨架 |
|---|---:|---:|---:|---:|---:|---|
| **58EAzO5N** | **1.24** | **0.93** | 0.0879 | **1.41** | 3 | w66 + winsorize(rank 后) |
| QPvNbVzw | 1.02 | 0.40 | **0.4044** | −0.60 | 4 | rsk68 风险调整反转 |
| QPvNbVNw | 0.97 | 0.57 | 0.086 | 0.89 | 3 | w66 subindustry 轴 |
| P0oY23YE | 0.95 | 0.62 | 0.0817 | 0.92 | 4 | w126 |
| bl6rbqrR | 0.90 | 0.56 | 0.0787 | 1.12 | 3 | w252 |
| mLo0mb7K | 0.27 | 0.10 | 0.082 | 0.46 | 3 | M5xM4 合取 |
| omEJLlJJ | −0.34 | −0.13 | 0.0973 | 0.73 | 5 | 66x252 多窗乘积 |
| leA5vlG7 | **−0.39** | −0.15 | 0.0833 | **−0.86** | 5 | M5 低 beta |

## 结论 1（推翻我自己上一轮的假设）：**w66 是窗口极大值，不是单调延长**
| 窗口 | 22 | **66** | 126 | 252 |
|---|---:|---:|---:|---:|
| S | 1.02 | **1.24** | 0.95 | 0.90 |
| 2Y | 1.08 | **1.41** | 0.92 | 1.12 |

⇒ 22→66 上升、66 之后**单调下降**。**66 是峰，别再往长扫**。
（上一轮我从「22→66 改善」误推「越长越好」，本条为更正。）

## 结论 2：**开 truncation 时，winsorize 放在 group_rank 之后同样是幂等的**
58EAzO5N（winsorize(subtract(0.5, group_rank(...)), std=2)）与 leA58QNO（裸式）读数**逐位相同**：
S 1.24 / F 0.93 / TO 0.0879 / 2Y 1.41。
- 机理：平台 **truncation 0.08 已在组合层截尾**，signal 层再 winsorize 改变不了最终权重。
- 修正记忆里「winsorize 放 rank 之后是真杠杆（risk70 先例 1.49→1.63）」：**那个先例应无 truncation 或 truncation 更松**；
  在 trunc 0.08 下 winsorize 前后都是死杠杆。

## 结论 3：**M5 低 beta（BAB）在 KOR/TOP600/D1 判死**
- 低 beta 多头 / 高 beta 空头：S **−0.39** / 2Y **−0.86**（方向反了也不是 +0.39，见铁律 B 不精确翻转）。
- beta ∧ 低波动 合取：S 0.27 / 2Y 0.46，微弱。
- ⇒ **BAB 在 KOR 不成立**，与美股长样本相反。关闭 M5 整条机制，不再投入。

## 结论 4：轴与几何的边界
- subindustry 轴 0.97/0.89 < **sector 轴 1.24/1.41** ⇒ 本族固定 sector（industry 上一轮已证更差 0.90/0.75）。
- 多窗乘积（66x252）S −0.34 ⇒ **同信号跨窗相乘是非单调变换，会毁信号**，禁止再用。
- rsk68 风险调整反转 S 1.02 但 TO **0.4044**（其余约 0.08）+ 2Y −0.60 ⇒ 换手爆表且近年失效，不可用。

## 锚点现状（本族上限）
**leA58QNO / 58EAzO5N：S 1.24 · F 0.93 · 2Y 1.41 · TO 0.0879 · raFail 3（LOW_SHARPE/LOW_FITNESS/LOW_2Y_SHARPE）**

已穷尽（勿重复）：窗口 22/66/126/252 · 轴 sector/industry/subindustry · winsorize · 多窗乘积 · ts_delta · ts_zscore252 · M5 beta。
**仅剩未测杠杆：平台 neutralization（7+ 档，只试过 STATISTICAL）、decay、truncation。**
