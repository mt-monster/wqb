# risk60 字段画像（DEU / TOP500 / D1）

> 建档 2026-11-23。数据源 `mcp__wq-brain-http__get_datafields(region=DEU, universe=TOP500, delay=1, dataset_id="risk60", filter_sharpe=false)`。

## 字段全表（5 字段，**全 VECTOR**）

| 字段 id | 类型 | coverage | alphaCount | userCount | description |
|---|---|---:|---:|---:|---|
| `rsk60_offer` | **VECTOR** | 0.835 | 214 | 135 | Composite borrow fee (annualized) paid by the short seller |
| `lending_fee_bid_rate` | **VECTOR** | 0.835 | 167 | 114 | Composite lending fee (annualized) at which long inventory is lent |
| `rsk60_last` | **VECTOR** | 0.835 | 141 | 94 | Most recent borrow/lend rate observed at the snapshot time |
| `rsk60_crowding` | **VECTOR** | 0.835 | 61 | 40 | Signed daily indicator of shorting activity（正 = 空头增加/拥挤） |
| `rsk60_datatime` | **VECTOR** | 0.835 | 15 | 10 | Vendor timestamp in HHMMSS（**元数据，不可作信号**） |

**★★ 与 risk68 的字段类型相反**：risk68 五字段全 **MATRIX**（包 `vec_avg` 会整批失败）；risk60 五字段全 **VECTOR**（**必须** `vec_avg` 降维，裸用会失败或语义错误）。

> 纪律：**字段类型逐集确认，只信 `get_datafields`**。同一类目（RISK）内不同数据集的类型可以完全相反。

## 机制聚类（1 条机制）

5 个字段中 4 个是**借券/出借费率**的不同快照（`offer` 空头借券费率 / `lending_fee_bid_rate` 多头出借费率 / `rsk60_last` 最近观测费率 / `rsk60_crowding` 空头拥挤度），
`rsk60_datatime` 是**时间戳元数据**（不可作信号）。
⇒ **risk60 = 1 条机制「证券借贷费率」**（与 GBR risk60「借券费率（水平型）」一致）。

**结构可用模板族（费率类信号 → 水平型）**
- H 水平：`ts_zscore(vec_avg(f),252)` —— 费率水平
- E 比值：`divide(vec_avg(offer), vec_avg(bid))` —— 借券-出借价差（**本集独有，经济含义最强**）
- D 差分：`ts_delta(vec_avg(f),66)` —— 费率变动
- N 信噪比：`ts_ir(vec_avg(f),66)`
- P 分位：`ts_quantile(vec_avg(f),252)`
- B 波动：`ts_std_dev(vec_avg(f),66)`
- G 门控：`trade_when(费率高位, 主信号, -1)`

## 实测

### ⚠ 首批（裸字段）整批失败 —— 实证 VECTOR 必须降维

2026-11-23 首批 8 臂用**裸字段**（未包 `vec_avg`）派出（`1jTilY31o4rv9EN4cCPK3d9`），
结果 `all_terminal=True / child_count=8 / errors=8`，每个子任务报同一错误：

```
Operator ts_zscore does not support event inputs.
```

⇒ **VECTOR 字段必须先 `vec_avg()`（或其它 `vec_*`）降维，才能进 `ts_*` 等标量算子。**

> ⚠ 这次失败有个前因：我在建档时**已经写下「全 VECTOR ⇒ 必须 vec_avg」**，但派批时仍用了裸字段。
> 说明「字段类型纪律」必须落实成**派批前的机械检查**（`preflight_expressions` 的 `auto_fix_vector=True`
> 或 `fix_vector_fields`），不能靠人记住。
> 对照 risk68：五字段全 **MATRIX**，包 `vec_avg` 反而整批静默失败（返回 None，无报错）。
> **同一 RISK 类目内，两个数据集的字段类型可以完全相反。**

### 修正批（vec_avg，8 臂，5 个结构互异族）

`4kBh5S1VG50pbnEVUwcZI7b`：H 水平 ×4 字段 + D 差分 + E 价差比 + E 价差差 + N 信噪比。**8/8 全部有效读数**：

| 族 | 结构 | alpha | S | F | 2Y | TO | sub | sub/S | RA |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|
| **H** | `ts_zscore(vec_avg(rsk60_offer),252)` | `RRewGXv1` | **−0.79** | −0.48 | −0.99 | 10.3% | −0.38 | ✗ | 5 |
| H | `ts_zscore(vec_avg(lending_fee_bid_rate),252)` | `P05mkeAK` | −0.72 | −0.42 | −0.99 | 10.8% | −0.34 | ✗ | 4 |
| H | `ts_zscore(vec_avg(rsk60_last),252)` | `YPaoRZ9R` | −0.71 | −0.34 | −0.92 | 16.0% | −0.30 | ✗ | 4 |
| H | `ts_zscore(vec_avg(rsk60_crowding),252)` | `npa5L0lM` | +0.09 | 0.01 | −0.24 | 22.3% | 0.15 | ✗ | 4 |
| **D** | `ts_delta(vec_avg(rsk60_offer),66)` | `A1x8o65g` | −0.33 | −0.11 | **0.85** | 14.6% | −0.29 | ✗ | 5 |
| **E** | `ts_zscore(divide(offer,bid),252)` | `O0WXlej7` | **+0.31** | 0.11 | 0.08 | 14.5% | **0.38** | **1.23 ✓** | 4 |
| E | `ts_zscore(subtract(offer,bid),252)` | `rK7MZkwd` | −0.61 | −0.33 | −0.84 | 12.1% | −0.65 | ✗ | 5 |
| **N** | `ts_ir(vec_avg(rsk60_offer),66)` | `88NxMAZV` | −0.18 | −0.05 | −0.55 | 5.5% | 0.28 | ✗ | 3 |

**五条首批结论**

1. **T1 方向被论文预测命中**：费率水平原向 **S −0.79**（高费率 → 跑输），即 D'Avolio 2002 / Loan Fees 2022 的「高借券费率 = 空头约束紧 = 高估」在 DEU 成立；
   **取反后 S≈+0.79**，是 risk60 当前最强方向。两个费率腿（offer −0.79 / bid −0.72）与 last 费率（−0.71）高度一致。
2. **T3 价差比是唯一「S 正 + sub 合规」的结构**：`divide(offer,bid)` → S +0.31 / sub·S⁻¹ **1.23 ✓**。
   而价差**差**（offer−bid）是 −0.61 —— **比值与差值的符号相反**（比值压缩信息、差值含量纲噪声）。
3. **T6 费率变动给 2Y 0.85**（本集最高 2Y），但 S −0.33。
4. `rsk60_crowding` 单用几乎无信号（S +0.09）—— 拥挤度**不是独立信号**，只可作门控/对手腿（对应论坛帖「成本曲线 × 空头结构对齐」的用法）。
5. 全部 8 臂 **|S| ≤ 0.79**，说明**单腿费率信号本身偏弱**，必须靠结构（价差比 / 成本曲线 / 残差化 / 门控）提取。

### T1 五层梯度（进行中，2026-11-23）

L1 = 15 个同类别算子全替 + 基线，核取**反转方向** `subtract(0,vec_avg(rsk60_offer))`，窗口 252。
批 `4cFbSefAt4ulcreGgCIgv3C`（10 臂）+ `44F0VG4ED4KAcDaGngqwzNG`（6 臂）在飞。

## 待补

- 5 字段 × 7 族的完整模板库与逐族梯度
- 逐字段实测读数回填

---

## 模板进度（2026-11-23，模板层级账本见 `../risk60_TemplatePlan.md`）

| 模板 | 机制 | 五层 | 臂数 | 天花板 | 状态 |
|---|---|---|---:|---|---|
| **T1 费率水平（反转）** | 借券费率水平 | 全 | ~62 | S 1.29 / F 1.43 / 2Y 1.96 / sub 0.83 | **关闭**：prod **0.844 FAIL** + RN S 仅 0.81（六成是因子 beta） |
| **T2 成本曲线（费率高于 252 日低点）** | 券源紧张的边际 | 全 | ~68 | S **1.07**（STAT exp3）/ 2Y **1.62**（SECTOR exp2）/ F **1.19**（SUBIND exp3） | **穷尽 PROVISIONAL**：真信号（RN 0.81≥raw）+ **prod 0.6178 ✓ 不拥挤**，但 S 与 2Y 不可兼得 + CW 无解 |
| **T3 借券-出借价差比** | 供需失衡 | L1 进行 | 10 | 首探 S +0.31 / sub·S⁻¹ **1.23** | 在跑 |

**已实证的三条硬事实（对本集后续模板通用）**

1. **字段全 VECTOR**：裸用报 `Operator ts_zscore does not support event inputs`；必须先 `vec_avg`。
2. **表达式层 group 轴是 no-op**：sector/industry/market/subindustry 四轴在 T2 上读数逐位相同
   ⇒ 轴只调**平台中性化设置**，不要在表达式里换 group 名。
3. **长窗把「低点」拉远**：T2 的 `vec_min(...,252)` 在 504/1008 上单调衰减（T1 水平型反而 504 最优）
   ⇒ **相对量信号与水平量信号的最优窗口方向相反**。

**判读纪律（本集踩过）**

- `rsk60_crowding` 不是独立信号（单用 S +0.09），只可作门控/残差对手腿。
- 价差**比**（+0.31，sub 1.23）与价差**差**（−0.61）符号相反 ⇒ 比值压缩信息、差值含量纲噪声。
- `crowding` / `statistical` 是**中性化档名，不是 group 变量**；写进 `group_neutralize(...,crowding)` 会报
  `unknown variable`，且**一条 ERROR 会让整批 8 臂 CANCELLED**。

## ★★★ 数据集级终判（2026-11-23，约 240 臂）

**DEU 塔位实读（`get_pyramid_alphas`）：RISK 0/3 —— 未点亮，本集产出计入交付。**

### 天花板

| alpha | 结构 | 配置 | S | F | 2Y | sub·S⁻¹ | TO | RA | prod |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|
| **`MP6vb5ar`** | 双残差 add + `ts_mean(·,66)` | INDUSTRY d16 | **1.24** | **1.08 ✓** | **1.94 ✓** | 0.63 ✓ | 2.6% | **1** | **0.6677 ✓** |
| `RRexNKp1` | 同上 | SECTOR d16 | 1.23 | **1.10 ✓** | **2.28 ✓** | 0.59 ✓ | 2.4% | **1** | 待测 |
| `YPa3NJ0R` | 分母 `vec_max(bid)` | INDUSTRY d16 | **1.25** | **1.10 ✓** | 1.80 ✓ | 0.64 ✓ | 2.6% | **1** | 待测 |

**RA 1 = 平台 18 项检查里只有 `LOW_SHARPE`（S 1.25 vs 1.58）一项不过；F/2Y/sub/TO/CW/prod 全部通过。**

**⇒ 结论：S 天花板 1.25，距闸 0.33–0.35，不可交付。**

### 为什么 S 上不去（不是没调好，是信息量不够）

- **5 个字段是 1 条机制**（借券费率的不同快照）：offer / bid / last / crowding + 一个时间戳。
  `rsk60_crowding` 单用 S 0.09，不是独立信息源。
- **约 40 个不同结构/配置的 S 全落在 1.20–1.29**，无一越过 1.30：
  内层 16 算子 × 3 核、group 全替 × 3、外层结构 8 种、轴 7 档、decay 6 档、trunc 4 档、
  窗口 5 档、指数 4 档、残差对象 11 种、腿数与权重 8 种、平滑 6 档 —— 全试过，S 变化区间 ±0.06。
- **逐年**：2014 2.46 / 2018 2.20 / 2022 2.66 撑起，2017 −0.82 是唯一亏损年，2015/2016/2021 仅 0.43–0.56。

### 三条可外推的先验（给其它 risk 类集）

1. **「水平/比值」形状的费率信号在 DEU 已拥挤**（prod 0.816–0.844）；
   **残差化 + `ts_mean` 平滑后能降到 0.59–0.69** —— 这条路径对 risk68/71/72/88 通用。
2. **修 S 与降 prod 在轴维度严格对立**：粗中性化给 S/2Y 但继承拥挤，细中性化（SUBINDUSTRY）剥掉组级暴露
   ⇒ 想两者兼得只能换 PnL 形状（残差对象/腿组合），不能调轴。
3. **`ts_mean` 是 CW 的真正解药**（TO 低时 decay 完全无效、trunc 反向加 RA）。

### 保留资产

`MP6vb5ar` / `RRexNKp1` / `YPa3NJ0R` 三颗 RA-1 件留作**换宇宙 / 换 delay / 未来组合腿**的种子；
不进本轮交付清单。
