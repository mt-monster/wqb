# USA ShortInterest 数据集扫描 · 2026-10-19

> 命名规范：类别级扫描 `_usa-<category>-dataset-scan-<asOf>.md`；
> 若日后单集深挖，按字段前缀另建 `_usa-<字段前缀>-field-profile-<asOf>.md`（`shrt3_` / `shrt43_` / 无前缀）。

## 1. 六个数据集全景（USА / TOP3000 / D1）

| 数据集 | 名称 | 字段 | cov | aC | 机制 | 裁定 |
|---|---|---:|---:|---:|---|---|
| **short_interest_pred** | Short Interest Forecast | 10 | 0.9987 | 369 | 做空兴趣**预测 vs 实际（惊喜）** | **✗ 判死** |
| shortinterest24 | Short Sale Circuit Breaker | 1 | 0.2573 | 444 | Reg SHO 短路器名单 | 未测（单字段 + 覆盖 0.26） |
| shortinterest29 | Group Short Sale Data | 32 | 0.8838 | 223 | 集团级做空量/执行时间/规模 | 未测（待挖） |
| **shortinterest3** | Securities Lending | 31 | **1.0** | 4343 | 借券利用率 / 借券需求评分 | **✗ 方向对但强度不足** |
| shortinterest43 | Short Sell Dataset | 32 | 0.9994 | 1492 | 各交易所做空量/总量 | 未测（可造跨venue背离） |
| **us_short_sale** | US Equity Short Sale Volume | 4 | **1.0** | 224 | 日频做空占比 | **✗ 判死（纯噪声）** |

## 2. 字段八问（按族）

### 族 A：`short_interest_surprise_*`（short_interest_pred）

**① 是什么** 做空兴趣的「实际 − 预期」及其比率/幅度（模型预测次日 SI，再与实际比）。
**② 什么类型** MATRIX，10 字段（另有 `prior_*` 上期版本）。
**③ 覆盖** 0.9987（几乎全覆盖）。
**④ 更新** 日频（模型每日预测）。
**⑤ 分布** 比率型，无量纲；`surprise_value` 带 `Unit[TSShare]`（股数单位 ⇒ 与 hump 有 unit 警告）。
**⑥ 拥挤** uc 9–38 / aC 12–61（低拥挤）。
**⑦ 信号** 实测（配方 `winsorize4 + backfill756 + hump0.01`）：

| 字段 | S | F | 2Y | SUB |
|---|---:|---:|---:|---:|
| `short_interest_surprise_value` | **−0.22** | −0.04 | 1.32 | −0.10 |
| `short_interest_surprise_ratio` | **−0.03** | 0.00 | −0.27 | 0.22 |
| `short_interest_surprise_amount` | 0.16 | 0.02 | 1.24 | 0.26 |
| `short_interest_predicted_change` | 0.48 | 0.13 | −0.10 | 0.42 |

**⑧ 怎么用·判死** **判死**：全期 S≈0 且**符号随年份翻转**（surprise_value：全期 −0.22 但 2Y +1.32）
⇒ 结构性不稳定，非参数问题。**该集不可用于线性 ATOM 腿。**

### 族 B：日频做空占比（us_short_sale）

**① 是什么** `short_shares / total_shares`（executed 与 reported 两套配对）。
**② 类型** MATRIX × 4；**③ 覆盖** 1.0；**④ 更新** 日频。
**⑤ 分布** 0–1 比率，右偏；**⑥ 拥挤** aC 85–167。
**⑦ 信号** 实测（4 条）：S **0.05 / 0.04 / −0.65 / 0.05**，margin 仅 **0.06 bp** ⇒ 纯噪声。
**⑧ 判死** 日频做空占比在 TOP3000 上无截面预测力（与文献一致：该比率被做市商对冲噪声主导）。

### 族 C：借券利用率 / 借券需求（shortinterest3）

**① 是什么** `loan_utilization_ratio_d1`（借出/可借）、`borrow_activity_score`（1–10 需求评分）。
**② 类型** VECTOR（需 `vec_avg`）；**③ 覆盖** 1.0。
**④ 更新** 日频；**⑤ 分布** 利用率 0–1 强右偏、评分离散 1–10。
**⑥ 拥挤** **aC 81 / 72**（低拥挤）。
**⑦ 信号** 实测（7 条）：

| 结构 | S | F | 2Y | SUB |
|---|---:|---:|---:|---:|
| 利用率水平 | **−0.96** | −0.48 | −1.74 | −0.22 |
| 需求评分水平 | **−1.00** | −0.59 | −2.02 | −0.09 |
| 利用率 Δ63 | −0.04 | 0.00 | −0.91 | 0.03 |
| **反向利用率（subind）** | **+1.01** | 0.52 | **+1.72** ✓ | 0.24 ❌ |
| **反向需求评分（subind）** | **+1.07** | 0.65 | **+1.91** ✓ | 0.13 ❌ |
| 反向利用率（industry） | +1.04 | 0.61 | +1.58 | 0.24 ❌ |
| 反向 + 尾部门控（rank>0.9） | 0.65 / 0.98 | — | 1.35 / 2.02 | **−0.01 / −0.13 ❌** |

**⑧ 怎么用·判死** ★ **方向明确（反向）、2Y 极强（1.7–2.0），但 S 上限 1.07、SUB 0.13–0.24**：
- 距离 S 闸(1.58) 差 **0.5**、SUB 闸(0.44) 差 **0.3** ⇒ 双重结构性缺口；
- **尾部门控（文献的挤空假说）实测更差**（SUB 转负）⇒ 该信号在 TOP3000 不是"尾部事件"，而是**弱线性因子**；
- ⇒ 判死（换 universe 才可能有救，但纪律禁止）。

## 3. 结构性结论（ShortInterest 全类）

1. **日频做空量类一律噪声**（S≈0.05，margin 0.06bp）：`us_short_sale` 与 `shortinterest43` 的 venue 级 svol/tvol 同源，预期同结论。
2. **借券类方向确定但强度不足**：反向 S 1.0–1.07、2Y 1.7–2.0，卡在 S/SUB 双缺口 ⇒ **只差"再加一档强度"**，而唯一能加的杠杆（跨集/尾部门控）都已被证明失败或违规。
3. ⇒ **本类目在当前 universe 下无法产出 ATOM**；后续若要继续，唯一未测的是 `shortinterest29`（集团级做空量，aC 223）与 `shortinterest24`（短路器名单，单字段 cov 0.26）。

## 4. 对照：Fundamental 侧同日结论

| 数据集 | 测试条数 | 最高 S | 裁定 |
|---|---:|---:|---|
| fundamental67 | 8 | 0.64 | 判死 |
| fundamental93 | 12 | 0.99 | 判死 |
| fundamental21（ESG） | 12 | 1.43（prod 未知 / SUB 0.52；新配方后 TO 撞地板） | SUB 卡死 |
| fundamental17（DuPont） | 4 | 1.07 | 弱 |

⇒ **两个目标类别（Fundamental / ShortInterest）在 2026-10-19 的实测均未产出达标 ATOM**；
当日唯一 ATOM 来自 `analyst_factor_signals`（`omoK1A5m`，已 ACTIVE/OS）。

---

## 5. 追记（二轮）：`shortinterest29`（集团级做空）也判死

用 `sum_short_sale_volume / sum_squared_short_volume / short_volume_count / trade_price_count`
构造了四个**全新机制**（此前无人测）：

| 机制 | 表达式核心 | S | F | 2Y | SUB | 判定 |
|---|---|---:|---:|---:|---:|---|
| **平均单笔做空规模**（机构参与度代理） | `divide(sum_short_sale_volume, short_volume_count)` | −0.09 | −0.02 | 1.50 | −0.15 | ✗ |
| **平均单笔做空名义额** | `divide(sum_trade_price, trade_price_count)` | 0.30 | 0.11 | 1.74 | 0.23 | ✗ |
| 月度做空量变化 | `ts_av_diff(shrt29_monthly_data1, 63)` | −0.35 | −0.11 | 0.05 | −0.15 | ✗ |
| **做空笔数集中度（HHI 型）** | `divide(sum_squared_short_volume, multiply(sum, sum))` | −0.16 | −0.04 | 1.40 | −0.33 | ✗ |

⇒ 4/6 数据集（`short_interest_pred` / `us_short_sale` / `shortinterest3` / `shortinterest29`）、
**13 条结构**全部不达标。**ShortInterest 类目在 TOP3000 下判定为「结构性无 ATOM」**。

### 类目级结论（可写进选类别纪律）

| 子族 | 有方向？ | 强度上限 | 结论 |
|---|---|---|---|
| 日频做空量/占比 | 无 | S≈0.05 | **纯噪声**（做市商对冲主导） |
| 做空量水平/变化/规模/集中度 | 弱 | S≤0.30 | 无预测力 |
| 做空兴趣预测惊喜 | 不稳定 | 符号随年份翻转 | 不可用 |
| **借券利用率/需求评分** | **有（反向）** | **S 1.01–1.07、2Y 1.7–2.0** | **方向对但差 S 0.5 / SUB 0.3，且尾部门控更差** |

⇒ 若未来要碰 ShortInterest，**只剩 `shortinterest43`（venue 级背离）与 `shortinterest24`（短路器名单）未测**，
且按上表规律预期同样无法过 S 闸；**建议把该类别标记为低优先级**。
