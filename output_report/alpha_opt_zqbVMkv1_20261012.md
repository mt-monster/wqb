# `zqbVMkv1` 指标优化 + 算子压缩报告
**执行**：`wq-alpha-gate-push-op-min` skill　**日期**：2026-10-12　**区域**：DEU / TOP500 / D1

---

## 一、结果（两条都全闸通过，按目标二选一）

| 项 | **原 `zqbVMkv1`** | **`j287l66O`（算子最少）** | **`Wje5K71x`（指标最高）** |
|---|---|---|---|
| **operatorCount** | 10 | **6（−40%）** | **7（−30%）** |
| `LOW_SHARPE` | 1.59（余量 +0.01） | **1.61** | **1.73（+0.14）** |
| `LOW_FITNESS` | 1.20 | **1.21** | **1.37（+0.17）** |
| `LOW_2Y_SHARPE` | 1.94 | **1.99** | 1.87 |
| `LOW_SUB_UNIVERSE_SHARPE` | 1.25 | 1.14 | ✅ |
| `SELF_CORRELATION` | 0.1380 | 0.1892 | 0.1879 |
| `PROD_CORRELATION` | 0.4116 | 0.4361 | 0.4305 |
| `CONCENTRATED_WEIGHT` / TO | ✅ / 0.1309 | ✅ / 0.1306 | ✅ / 0.1269 |

### 最终表达式

**① 算子最少（6 算子）—— `j287l66O`**
```python
group_rank(multiply(rank(ts_delta(fnd6_newq_oiadpq, 240)),
                    rank(ts_delta(fnd6_newq_oiadpq, 180))), sector)
```

**② 指标最高（7 算子）—— `Wje5K71x`**
```python
group_rank(ts_target_tvr_decay(
    multiply(rank(ts_delta(fnd6_newq_oiadpq, 240)),
             rank(ts_delta(fnd6_newq_oiadpq, 176))),
    target_tvr=0.03), sector)
```

settings 均为 `DEU / TOP500 / D1 / decay4 / FAST / truncation 0.08 / nanHandling ON`。

---

## 二、优化路径（skill 的六步流程）

### ① 采集 —— 发现两个隐患
- IS 全 PASS，但 **`LOW_SHARPE` 余量只有 +0.01**（1.59 vs 1.58）⇒ 任何压缩都会掉闸 ⇒ **必须先推余量**
- **`operatorCount = 10`**，正好卡在复杂度闸线（调用点 ≥10）
- fitness 公式验证通过：`1.59 × √(0.0744/0.1309) = 1.199 ≈ 1.20` ✓

### ② 算子审计（`op_count.py`）
`逐算子计数：rank×2, ts_delta×2, divide×2, winsorize×1, group_rank×1, ts_target_tvr_decay×1, multiply×1` → 共 10

### ③ 推指标（Phase A）
| 动作 | S |
|---|---|
| 起点 `target_tvr=0.05` | 1.59 |
| `target_tvr=0.04` | **1.61** |
| `target_tvr=0.035` | 1.70 |
| `target_tvr=0.03` | **1.73**（最高） |
| `target_tvr=0.02` | 回落 |

⇒ **限速器 `target_tvr` 越低 S 越高**（新规则 C14），于是 S 余量从 +0.01 扩到 +0.15。

### ④ 压缩算子（Phase B）—— 三条实测结论
| 轮次 | 动作 | 算子 | S | fit | 2Y | 判定 |
|---|---|---|---|---|---|---|
| — | 起点 | 10 | 1.59 | 1.20 | 1.94 | — |
| **C11** | **去掉两个 `divide`（比率归一化）** | **8** | **1.65** | **1.27** | **1.98** | ✅ **双赢** |
| **C5** | **删外层 `winsorize`** | **7** | **1.65** | 1.27 | 1.98 | ✅ **逐位无损** |
| C14 | 再加 `target_tvr=0.03` | 7 | **1.73** | **1.37** | 1.87 | ✅ 指标最高 |
| — | 短窗 176→180（无 tvr） | **6** | **1.61** | 1.21 | **1.99** | ✅ 算子最少 |

**★ 最大收益 = C11**：`ts_delta(divide(A,B),W)` → `ts_delta(A,W)`
⇒ **省 2 个算子，且 S 反而 +0.04** —— 因为**比率归一化稀释了水平变化信号**。

**反例（证明哪些算子必须保留）**：
| 试验 | 算子 | S | 结论 |
|---|---|---|---|
| 删两个 `rank` | 4 | **0.61** | ✗ 崩 |
| 删一个 `rank` | 5 | 1.34 | ✗ 不够 |
| `subtract(rank,rank)` 替换 `multiply` | 6 | **0.73** | ✗ 崩且不省算子 |

### ⑤ 设置收敛
`decay` 3/4/5/6/8 为平台期（取 4）；`truncation` 零杠杆；`neutralization` 保持 FAST（换档全降 S）。

### ⑥ 判定（全闸复核）
两条候选 **10/10 全 PASS**（含 self < 0.7 与 prod < 0.7 两把相关性闸）。
⚠ **提交仍需用户授权**（`ALLOW_ALPHA_SUBMIT=False` 全局闸锁）。

---

## 三、回写到 skill 的新规则

已写入 `references/op-compression.md`：
- **C11**（新，双赢）：去掉比率归一化 —— 省 2 算子且提 S
- **C14**（新）：限速器 `target_tvr` 越低 S 越高（0.05→0.03 = S 1.61→1.73）
- **C5**（已验证）：`winsorize` 在「限速器外层」结构里可无损删除
- **C12/C13**（反例）：`multiply` 内 `rank` 必需；`subtract(rank,rank)` 形态崩
- 附第六节「端到端案例」，含本轮完整对照表

**另验证**：平台 `operatorCount` 与本 skill `op_count.py` 的正则计数**逐位一致**（同一表达式两处都报 7 / 6）。
