# `3q0wVPgz` 算子压缩报告（DEU / TOP500 / D1）

日期：2026-11-17　｜　skill：`wq-alpha-gate-push-op-min`

## 一、原件

- settings：DEU / TOP500 / D1 / decay 0 / SUBINDUSTRY / trunc 0.08 / nan ON
- **operatorCount = 40**
- S 2.04 / F 1.81 / TO 12.53% / 2Y 2.49 / sub 1.33 / DD 5.61% / margin 0.001569
- `is.checks` 全 PASS，`failed_ra_count = 0`
- 塔：`DEU/D1/INSIDERS`(1.6×) + `DEU/D1/ANALYST`(1.8×)，effective 2，短板 1.6×
- 当季计数：insiders **1** / analyst **6** → 交后 2/7，**无新点亮，塔边际 0**

## 二、压缩路径 40 → 17（−57.5%）

### 1. 变量合并（零损失）
重复子式 4 处：

| 子式 | 原出现次数 |
|---|---|
| `vec_avg(insd1_holdings)` | 4 |
| `divide(sv1, add(sv1,sv2,sv3,sv4))` | 2 |
| `group_rank(ts_mean(p,66), sector)` | 2 |
| `group_rank(ts_ir(v,66), sector)` | 2 |

### 2. 多参摊平（零损失，只降调用数）
`add(add(a,b),add(c,d))` → `add(a,b,c,d)`（两处）；core 多层 `add` 摊平成单次 5 参 `add`。

### 3. 有损改写（实测后采纳）
| 改写 | 省 ops | 结果 |
|---|---|---|
| 删 `signed_power(·, 1.3)` | −1 | 指标略升（历史同结论：负成本） |
| `divide(1, add(dlc,1))` → `add(group_rank(dlc),-1)` 三参 multiply 写法 | −1 | 等价（rank 吸收单调递减） |
| 删 `leg1`（动量×份额交互腿） | −4 | S −0.02 |

## 三、平台侧异常（重要）

- 本轮 **含 `leg1` 的表达式全部 `status=ERROR`**，**包括原件 `3q0wVPgz` 本身**（用原始 code 重跑对照亦 ERROR）。
- 同期 `rank(close)` 探针在 DEU 与 USA 均成功，`signed_power(rank(close),1.3)` 成功、整数版 `1.3→2` 反而 ERROR ⇒ 判定为**平台运行期不稳定**，非表达式缺陷。
- 结论：`leg1` 当前不可复现，压缩只能沿「删 leg1」方向落地；原件历史读数（S 2.04）用于对比基线。

## 四、最终候选

### 首选 `VkNOJYnM`（17 ops，decay 0，grm 窗口 63）

```
v = vec_avg(insd1_holdings);
p = divide(significant_value_1, add(significant_value_1, significant_value_2, significant_value_3, significant_value_4));
grm = group_rank(ts_mean(p, 63), sector);
gri = group_rank(ts_ir(v, 66), sector);
leg2 = multiply(gri, add(group_rank(days_from_last_change(v), sector), -1), -1);
an = group_rank(divide(subtract(est_12m_ebi_raisednum_4wks, est_12m_ebi_lowerednum_4wks),
                       add(est_12m_ebi_raisednum_4wks, est_12m_ebi_lowerednum_4wks, 1)), sector);
group_zscore(add(leg2, grm, gri, an), sector)
```

| 指标 | 原件 40 ops | **`VkNOJYnM` 17 ops** | Δ |
|---|---|---|---|
| Sharpe | 2.04 | **2.03** | −0.01 |
| Fitness | 1.81 | **1.73** | −0.08 |
| Turnover | 12.53% | 12.26% | −0.27pp |
| 2Y / ladder | 2.49 | 2.25 | −0.24（线 2.02，余量 0.23） |
| sub | 1.33 | 1.34 | +0.01 |
| DD | 5.61% | **5.03%** | −0.58pp |
| margin | 0.001569 | 0.001479 | −5.7% |

- `failed_ra_count = 0`，`is.checks` 全 PASS
- **prod = 0.4489**（< 0.7）
- self：与已提交 `akaWd90w`/`88N6OOP7`/`j2a9moM5` 最高 **0.0865**
- 塔：`insiders/analyst` eff2 / 短板 1.6×，交后 2/7，**塔边际 0**
- 六维：distinct ops **10**、T1 Δ **+0.0143**、T2 Δ +0.0136（原 40 ops 未测六维，无法给 Δ；此为对账户基线的边际）

### 备选 `1YWJEzZX`（同结构 + decay 4）

S 1.96 / F 1.64 / TO **8.52%** / 2Y 2.16 / sub 1.29 / **margin 0.002043（+38%）** / DD 5.46%，全闸 PASS。
适用：更看重 margin 与换手（PPA/组合友好）而非 S 峰值。

### 精调扫描（窗口邻域，decay 0）

| 变体 | alpha | grm/gri 窗口 | S | F | 2Y | DD |
|---|---|---|---|---|---|---|
| **T1（采纳）** | `VkNOJYnM` | 63 / 66 | **2.03** | **1.73** | 2.25 | **5.03%** |
| 基准 V5 | `RRedWnob` | 66 / 66 | 2.02 | 1.72 | **2.30** | 5.22% |
| T2 | `YPaQqkEv` | 69 / 66 | 1.98 | 1.66 | 2.27 | 5.35% |
| T4 | `6XMzOROO` | 66 / 69 | 2.00 | 1.68 | 2.14 | 5.57% |
| T5 | `A1xkKgoQ` | 63 / 63 | 1.99 | 1.68 | 2.15 | 5.10% |

⇒ `ts_mean` 窗口 63 略优于 66；`ts_ir` 窗口 66 不可动（63/69 均降）。

## 五、未测 / 待补

1. `decay 3`（`T1_decay3` 仿真卡队列 0.15 未出）与 T3（gri 窗口 63）未取终态。
2. 六维原件基线未算（原件 40 ops 表达式当前不可复现，无法跑分）。
3. 稳健性审计（逐年 + PnL）未做；提交前需补 `robustness_<id>` 台账。

## 六、孪生关系

`VkNOJYnM` ↔ `RRedWnob` 互相关 **0.9955** ⇒ 同骨架只能保留 1 颗；`1YWJEzZX`（decay4）为同族第三颗。
其余中间件（`V1`–`V5`、T2/T4/T5）全部 `SUPERSEDED`。
