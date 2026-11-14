# 交付台账更新：11 → 14 颗（2026-11-12）

## 互相关裁决（threshold=0.7，用户 11-09 全局标准）

`compute_mutual_correlation(alpha_ids=[3 新候选 + 11 已交付], threshold=0.7)`

```
all_below_threshold = True
max_mutually_below_subset_size = 14
max_mutually_below_subset = [2r5MO67Z, d5apOzxj, npa9KaVd, bl6AvMkN, vR1oxZA3,
                             GrW9OxmG, zq3eb7No, rKRx2Alj, 78Yk8VR1, qM7KxkQV,
                             Jj8VQwoe, RREPm361, d5a2vxzY, 9qlz29Oe]
missing_pnl = []
```

**3 颗新候选与 11 颗已交付件的最大相关性：**

| 新候选 | 与已交付最大相关 | 撞谁 | 结论 |
|---|---:|---|---|
| 2r5MO67Z | **0.3376** | qM7KxkQV | 独立 |
| d5apOzxj | **0.2663** | qM7KxkQV | 独立 |
| npa9KaVd | **0.3544** | qM7KxkQV | 独立 |

⇒ **14 颗全对 < 0.7，全部可并入交付篮子。**

## 新的 14 颗清单

| # | alpha | 状态 | S | F | 2Y | sub | 塔 | 备注 |
|---|---|---|---:|---:|---:|---:|---|---|
| 1 | bl6AvMkN | ✅ACTIVE | 1.61 | 1.36 | 2.15 | — | MODEL+ANALYST | 存量 |
| 2 | vR1oxZA3 | ✅ACTIVE | 3.27 | 3.09 | 4.39 | — | （无标记）| 存量 |
| 3 | GrW9OxmG | ✅ACTIVE | 1.62 | 1.56 | 1.93 | — | ANALYST | 存量 |
| 4 | zq3eb7No | ✅ACTIVE | 2.01 | 1.28 | 1.64 | — | ANALYST | 存量 |
| 5 | rKRx2Alj | ✅ACTIVE | 1.95 | 1.80 | 2.23 | — | MODEL+ANALYST | 存量 |
| 6 | 78Yk8VR1 | ✅ACTIVE | 1.68 | 1.21 | 2.27 | — | SHORTINTEREST | 存量 |
| 7 | qM7KxkQV | 🟡待授权 | 1.72 | 1.34 | 2.43 | — | SHORT+INSIDERS | 存量 |
| 8 | Jj8VQwoe | 🟡待授权 | 1.65 | 1.24 | 2.42 | — | SHORT+OTHER | 存量 |
| 9 | RREPm361 | 🟡待授权 | 2.02 | 1.25 | 1.82 | — | ANALYST | 存量（prod 超时）|
| 10 | d5a2vxzY | 🟡待授权 | 1.60 | 1.08 | 2.05 | — | SHORTINTEREST | 存量 |
| 11 | 9qlz29Oe | 🟡待授权 | 1.86 | 1.34 | 2.02 | — | SHORT+NEWS | 存量 |
| **12** | **2r5MO67Z** | 🆕待授权 | **2.63** | **2.13** | **2.94** | **1.63** | PV+INS+MODEL（eff 0）| **NEW fail=[]** |
| **13** | **d5apOzxj** | 🆕待授权 | 1.59 | 1.14 | **2.65** | 0.98 | PV+INS+MODEL（eff 0）| **NEW fail=[]** |
| **14** | **npa9KaVd** | 🆕候选 | 1.58 | 1.33 | 1.24 | **0.99** | PV+INS（eff 2）| NEW 卡 ladder year3 |

**进度：14 / 20（70%）**

## 仍缺 6 颗

insiders 族的互相关结构已证明：**9 颗高 S 新件在 0.7 阈值下只能取 3 颗**（同源）。
要补 6 颗必须换**搭档族**，而不是继续在 S3/S7 × analyst 上变体。

### 下一批应换的搭档轴（尚未试过）

| 轴 | 说明 | 预期 |
|---|---|---|
| insiders × **news 情绪** | DEU/D1 news 塔 0 颗；news 与 analyst 信息源正交 | 新家族，低相关 |
| insiders × **risk** | DEU/D1 risk 塔 0 颗 | 新家族 |
| insiders × **earnings** | DEU/D1 earnings 塔 0 颗 | 新家族 |
| insiders × **shortinterest** | SHORT 塔已点亮，但作为搭档可用于低相关 | qM7KxkQV 已证 SHORT+INS 可行 |
| insiders × **institutions** | institutions 塔 1 颗 | 同为持仓面，可能高相关 |

**⚠ 三塔 effective=0 的教训**：若要保住塔倍率，必须控制**只占两塔**。
insiders + analyst 必然三塔（PV 来自 cap 桶）⇒ 要么**去掉 cap 桶**（但 T9 实测 S 掉 0.25、sub 掉 0.36），要么**接受 eff 0**。
若用 insiders × news（不含 analyst），则仍是 PV+INS+NEWS 三塔 ⇒ 同样 eff 0。
⇒ **只有「insiders 单类 + cap 桶」才是两塔（PV+INS, eff 2）**。
