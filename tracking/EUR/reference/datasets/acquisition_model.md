# acquisition_model · EUR / TOPCS1600 / D1 字段画像（快判）

> 类型 VECTOR · 15 字段 · cov 0.748 · category = **other**（×1.5）· αC 27
> 采集：2026-11-07 · M&A 目标概率模型（NLP+基本面+信用+估值分位）

## 实测（已终态,multisim `Ot9JDgq64lJaS110sPM52fz`,FAST/decay15）

| 变体 | alpha id | S | F | 2Y |
|---|---|---|---|---|
| global 概率 | `qMLY3WqP` | **−0.91** | −0.45 | −0.85 |
| industry 概率 | `vR1p6kgv` | −1.03 | −0.53 | −0.73 |
| country 概率 | `O0AMVraJ` | −0.91 | −0.45 | −0.79 |
| sector 概率 | `omEJr6OJ` | −0.97 | −0.49 | −0.84 |
| global ts_rank 66/252 | `1YNlPxEM` | **−1.11** | −0.55 | −0.44 |

**归因**：五臂同向强负（−0.91~−1.11）——**并购目标概率高的股票跑输**（被收购预期 → 估值已透支/套利资金提前压制,或「易被收购」=经营差的代理）。反向 +0.91~+1.11 但 2Y 反向后仍弱（0.44-0.85）,且 CLUSTER_TEST 全负。**归档**:反向读数备用记录（OTHER 塔若重启,ts_rank 版 −1.11 是起点）,当前按用户指令锁定 insiders 不投入。
