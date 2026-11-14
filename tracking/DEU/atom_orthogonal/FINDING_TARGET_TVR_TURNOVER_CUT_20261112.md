# 有价值发现：ts_target_tvr_hump / decay 保持 S 不变但换手降 58%

日期：2026-11-12
BE181 multisim 3rONwG9Hu4WLa91VkUGpdAP（2 臂，修正 target_tvr 命名参数后）

## 实测

| 臂 | 构造 | S | F | 2Y | sub | **TO** | fail |
|---|---|---:|---:|---:|---:|---:|---:|
| 基线（A+B 朴素）| `add(A,B)` | 1.30 | 1.20 | 1.08 | 0.56 | **22.7%** | 3 |
| **`ts_target_tvr_hump(A+B, target_tvr=0.10)`** | pwamppGx | **1.30** | 1.19 | 1.08 | 0.55 | **9.6%** | 3 |
| **`ts_target_tvr_decay(A+B, target_tvr=0.10)`** | O0WO22Vv | **1.30** | 1.19 | 1.08 | 0.56 | **9.6%** | 3 |

**S / F / 2Y / sub 全部持平，TO 从 22.7% 降到 9.6%（−58%）。**

## 为什么这有价值

1. **同 S 下换手减半 ⇒ F（fitness）**：本例 F 略降（1.20→1.19）因为 F 公式里 TO 有 sqrt 除数，
   但实际交易成本与滑点在实盘里大降。
2. **prod 相关性会更稳**：低换手的持仓轨迹变化慢，prod 计算窗口内的相关性漂移小。
   本项目记忆里有明确教训：「prod 漂移猛，48h 作废」。降换手是对冲手段之一。
3. **对 CONC（集中度）无副作用**：因为只是平滑，不改持仓排序。

## 正确用法（算子签名，已核实）

```
ts_target_tvr_hump(x, lambda_min=0, lambda_max=1, target_tvr=0.1)
ts_target_tvr_decay(x, lambda_min=0, lambda_max=1, target_tvr=0.1)
```

⚠ **三个参数都是命名参数**。只写 `lambda_min=0.10` 会报
`Required attribute "target_tvr" must have a value`——必须显式给 `target_tvr=`。

## 与 skill 里旧结论的关系

`wq-alpha-gate-push-op-min` 的杠杆阶梯 L3 写着：
> `ts_target_tvr_decay(x, target_tvr=t)` → S +0.03、TO↓、fit↑（**仅当 TO > t 时激活**）

本次实测：TO 22.7% > 10% ⇒ 激活，**TO 确实大降**，但 **S 没有 +0.03（持平）**、**F 无提升（略降）**。
⇒ 修正该条：**这个算子只降换手，不保证提 S/F**。价值在 prod 稳定性，不在指标。