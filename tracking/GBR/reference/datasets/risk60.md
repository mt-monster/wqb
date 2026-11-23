# GBR / risk60（Lending Fees，借券费率，VECTOR×5）

> 塔：**risk**（GBR/D1 乘数 **1.3**，当前 0/3 未点亮）
> 画像日期 2026-11-22 · 数据源 `mcp__wq-brain-http__get_datafields`（GBR/TOP700/D1，`filter_sharpe=false`，`dataset_id=risk60`）
> 本轮实拉：`count=5` / `platform_count=5` / `returned=5` / `complete=true` ⇒ 单页全量。
> 数据集级：`pyramidMultiplier=1.3`、全部字段 `dateCreated=2026-07-01`（同批 onboard）。
> ⚠ 全部 VECTOR ⇒ 探针/信号必须 `vec_avg`/`vec_sum` 折叠。
> ⚠ 2026-11-22 用户标准升级：**每数据集 ≥10 个互异模板 × 各自完整 5 层梯度**。本档案为本轮 12 模板梯度服务的画像。机制聚类先于模板构造（risk 类别「字段多≠机制多」教训）。

---

## 字段全表（平台实拉 5/5）

| 字段 | 类型 | cov | αC | uC | 经济含义（平台 description） |
|---|---|---:|---:|---:|---|
| `rsk60_crowding` | VECTOR | 0.6694 | 98 | 67 | 做空活动日度符号指标（正=做空/拥挤增加，负=平仓/去拥挤） |
| `rsk60_offer` | VECTOR | 0.6694 | 53 | 40 | 卖空方支付的综合借入费率（年化） |
| `lending_fee_bid_rate` | VECTOR | 0.6694 | 42 | 39 | 长期库存出借方的综合出借费率（年化） |
| `rsk60_last` | VECTOR | 0.6694 | 33 | 31 | 快照时刻最新观察到的借入/出借费率 |
| `rsk60_datatime` | VECTOR | 0.6694 | 13 | 10 | 快照的供应商时间戳（HHMMSS，盘中打印排序用） |

> cov 0.6694（非 GBR 盲区，真实覆盖 67% —— TOP700 里约 470 只可借券标的）。

---

## 4. 字段族拆解（机制聚类先行）

| 族 | 字段 | 机制 |
|---|---|---|
| **A 费率水平族（3 字段）** | `lending_fee_bid_rate`（出借）/ `rsk60_offer`（借入）/ `rsk60_last`（最新） | 借券成本水平。年化费率（%），右偏长尾（难借标的天价费率）⇒ 水平型信号，宜 `ts_backfill + vec_avg` 折叠 + 去量纲 |
| **B 流量族（1 字段）** | `rsk60_crowding` | ±符号日度指标：正=做空/拥挤增加、负=平仓/去拥挤 ⇒ 累计型（`vec_sum`）+ 差分型两种取法 |
| **C 元数据族（1 字段）** | `rsk60_datatime` | 时间戳 HHMMSS，仅排序用，**不作信号**（数据层排除） |

**族间关系（模板设计依据）**：
- A 内部：offer（借入）≥ bid_rate（出借）通常恒成立，**价差 = 经纪商利润/融资紧张度**（`subtract` / `divide` 两个互异模板）；`last` 是最新混合读数。
- A×B：费率高企 + crowding 符号 → **拥挤度与费率的残差**（`vector_neut(bid_rate, crowding)`）与**门控**（crowding 门控 offer）两个互异组合模板。
- 同一字段族内不同字段 = 独立模板（同 inst25 H/I 先例），但读数逐位重合时要合并族级天花板。

---

## 5. 完整梯度 12 模板清单（2026-11-22，用户「每数据集 ≥10 模板」）

| # | 模板（信号构造） | 机制 | L1 探针内核 |
|---|---|---|---|
| T1 | `vec_avg(lending_fee_bid_rate)` 出借费率水平 | A 水平 | ts_zscore |
| T2 | `vec_avg(rsk60_offer)` 借入费率水平 | A 水平 | ts_zscore |
| T3 | `vec_avg(rsk60_last)` 最新费率水平 | A 水平 | ts_zscore |
| T4 | `vec_avg(lending_fee_bid_rate)` 差分 | A 变化 | ts_av_diff |
| T5 | `vec_avg(rsk60_offer)` 差分 | A 变化 | ts_av_diff |
| T6 | `vec_sum(rsk60_crowding)` 累计拥挤 | B 累计 | ts_sum |
| T7 | `vec_sum(rsk60_crowding)` 差分（去拥挤速度） | B 变化 | ts_av_diff |
| T8 | `subtract(offer, bid_rate)` 价差 | A×A | ts_zscore |
| T9 | `divide(offer, bid_rate)` 比值 | A×A | ts_zscore |
| T10 | `vector_neut(bid_rate, crowding)` 费率⊖拥挤残差 | A×B | ts_zscore |
| T11 | `multiply(offer, ts_rank(crowding,66))` 拥挤门控费率 | A×B | ts_zscore |
| T12 | `vec_avg(lending_fee_bid_rate)` 波动 | A 二阶 | ts_std_dev |

> 每个模板各自跑完整 5 层（L2 内核 15 臂 → L2b 窗 4 → L3 轴 6 → L4 外包 8 → L5 设置 4 档 × 2 轴 + L5-R 重扫）。基线结构统一：`reverse(group_rank(<K>(ts_backfill(<FOLD>,250),N), industry))`，设置 SUBINDUSTRY/decay4/trunc0.08/nanON。
> 探针批：`2m3gol1a054Wcy4NweoLVxi`（T1–T8）+ `3OgMGx4g44LucmC1ayIhHZkG`（T9–T12）。

---

## 6. 六法/实测（12 模板 L1 探针，2026-11-22）

### L1 探针全表（12 臂，`2m3gol1a054Wcy4NweoLVxi`（T1–T8）+ `3OgMGx4g44LucmC1ayIhHZkG`（T9–T12））

基线：`reverse(group_rank(<K>(ts_backfill(<FOLD>,250),126), industry))` / SUBINDUSTRY / decay4 / trunc0.08

| 模板 | 构造 | 探针内核 | α | S | F | 2Y | TO |
|---|---|---|---|---:|---:|---:|---:|
| **T7** | `vec_sum(rsk60_crowding)` 去拥挤速度 | ts_av_diff | `leaNRYpA` | **0.46** | 0.19 | **+0.92** | 15.2% |
| **T11** | `multiply(offer, ts_rank(crowding,66))` 拥挤门控费率 | ts_zscore | `1YW2n0qm` | **0.43** | 0.14 | −0.03 | 21.8% |
| **T4** | `vec_avg(lending_fee_bid_rate)` 费率差分 | ts_av_diff | `e7aWqP7z` | **0.31** | 0.11 | +0.33 | 10.0% |
| T5 | `vec_avg(rsk60_offer)` 费差分 | ts_av_diff | `qM7wmpM2` | 0.23 | 0.07 | +0.18 | 9.3% |
| T3 | `vec_avg(rsk60_last)` 最新费率水平 | ts_zscore | `1YW2nRY6` | 0.15 | 0.03 | −0.45 | 16.3% |
| T10 | `vector_neut(bid_rate, crowding)` 残差 | ts_zscore | `akagWw55` | 0.14 | 0.03 | −0.20 | 13.7% |
| T6 | `vec_sum(rsk60_crowding)` 累计拥挤 | ts_sum | `QP0o5AZr` | 0.09 | 0.02 | −1.03 | 5.7% |
| T12 | `vec_avg(bid_rate)` 费率波动 | ts_std_dev | `1YW2n0qX` | 0.04 | 0.00 | −0.29 | 3.0% |
| T9 | `divide(offer, bid_rate)` 比值 | ts_zscore | `e7aWqvX6` | 0.03 | 0.00 | −0.56 | 12.4% |
| T1 | `vec_avg(bid_rate)` 出借费率水平 | ts_zscore | `pwap1kq6` | 0.00 | 0.00 | −0.63 | 10.6% |
| T8 | `subtract(offer, bid_rate)` 价差 | ts_zscore | `vRAoJb8w` | 0.00 | 0.00 | −1.18 | 11.6% |
| T2 | `vec_avg(rsk60_offer)` 借入费率水平 | ts_zscore | `xAvEmoKp` | −0.01 | −0.00 | −1.01 | 9.9% |

**L1 结论**：
1. **费率水平族（T1/T2/T3/T8/T9/T12）全部 ≤0.15、2Y 多为负** ⇒ **借券费率「水平」在 GBR 无横截面定价力**（与 2026-11-21 上会话的层1读数一致但更彻底）。
2. **活面全在「变化/流量」**：T7（crowding 差分，去拥挤速度）S0.46/**2Y0.92** 最佳；T11（拥挤门控费率）S0.43/subU **1.07**；T4（费率差分）0.31/2Y0.33。
3. **与 risk 类别「字段多≠机制多」一致**：5 字段 = 2 条机制（费率水平 + 做空流量），水平型三字段（bid/offer/last）与两组合（价差/比值）**全部同向死亡**，说明是同一信息源。

| 法 | 读数 / 结论 |
|---|---|
| ① 覆盖率 | cov 0.6694 ⇒ 探针 lc/sc 待补（TO 1.5–28%） |
| ② 非零率 | 费率可为 0（无借贷摩擦标的）⇒ T9 比值有 0 除风险（读数 S0.03 未崩，说明分母基本非零） |
| ③ 更新频率 | 日频快照 ✅ |
| ④ 量纲 | 费率年化 %（右偏）；crowding ±符号 ⇒ **crowding 直接 ts_sum 无需去量纲** |
| ⑤ 中心 | 费率右偏；crowding 近零双边 ✅ |
| ⑥ 分布 | 费率长尾（T12 波动型 S0.04 说明噪声主导）；crowding 差分有效说明是均值回复型 |

---

## 7. 模板梯度档案

`tracking/GBR/waves/wave20261122_gradient_risk60.md`（12 模板 × 完整 5 层 + L5-R；进行中）

- 上个会话（2026-11-21）risk60 层 1 梯度曾产出 S0.52/2Y0.84（费率水平族），批已 404 失效；本轮从零重来并扩到 12 模板，**L1 证明费率水平族无信号（≤0.15）**，上会话 0.52 应来自未记录的配置组合，本轮以 12 模板重测为准。
- `tools/ledger/dead_sets.py --region GBR` 中 risk60 无数据集级判死记录。

---

## 8. 2026-11-23 补测结论（全目录口径，非模板级候选集）

### 8.1 ★ VECTOR 折叠函数是一个独立的「类别轴」（此前从未扫过）

本数据集 5 字段**全部 VECTOR** ⇒ 「用哪个 `vec_*` 折叠」是 8 算子的一整个类别，且折叠函数改变信号的**经济含义**：

| 折叠 | 机制含义 |
|---|---|
| `vec_avg` | 经纪商间**平均**费率（水平） |
| `vec_max` | **最高**费率 = 尾部摩擦（最难借的那家） |
| `vec_min` | 最低费率 = 乐观口径 |
| `vec_sum` | 合计（与经纪商家数混杂 ⇒ 信息量杂） |
| **`vec_stddev`** | 经纪商间费率**离散度** = 费率**不确定性**（≠ 水平，结构互异的新机制） |
| `vec_range` | max−min = 离散度的无中心版本 |
| `vec_count` | 报价经纪商数 = 覆盖度代理（非费率） |

⇒ 风险提示：`vec_avg` 之所以在 12 构造里通吃，**可能只是因为没人试过别的折叠**；`vec_stddev`（费率离散度）与 `vec_max`（尾部摩擦）在经济上是「借券市场摩擦」的标准度量，值得独立开构造。

### 8.2 平台算子表实拉（2026-11-23，`get_operators`）

- 平台实时算子 = **103 个**，与 `docs/reference/operators_catalog.json` **逐项一致** ⇒ 本地 catalog 可作离线判据，无需逐次实拉。
- ⚠ **平台无 `ts_median`** ⇒ 论坛帖 `44941181410455` 给出的官方模板 `ts_median(ts_backfill(FIELD,60),20)` **在当前平台不可照搬**；须用 `ts_mean` 等价改写，或实测该算子是否存在（幽灵算子风险）。
- 单位族硬约束（实测）：`bucket` / `tail` / `generate_stats` / `combo_a` / `group_cartesian_product` 输出带 **Group 单位** ⇒ 与 `reverse` / `group_rank` 链路不兼容（静态闸直接拒）。

### 8.3 C8 路线（`divide(offer,bid)`）的当前最优与缺口

- **当前最优 = FAST × `ts_covariance`750 × subindustry × `group_rank` = S0.66 / F0.26 / 2Y1.50 / TO8.3%**（α `aka9pPv1`，RA 失败项 = LOW_SHARPE + LOW_FITNESS + LOW_2Y_SHARPE）。
- **`ts_covariance` 是模板级候选集漏掉的更强内核**（0.49 vs `ts_ir` 0.38，同层位）⇒ **候选集穷尽 ≠ 类别穷尽**。
- 窗口层实测峰值在 **750**（窄峰，两侧都掉：1000→0.43、132→0.59；短窗 44–110 全塌且 2Y 转负）。
- 缺口：**S 差 0.92 / F 差 0.74 / 2Y 差 0.08** ⇒ 2Y 已接近闸口，S 是主要瓶颈。

### 8.4 命名参数精调清单（平台实拉 103 算子中带命名参数的）

| 算子 | 可调命名参数 | 档位建议 |
|---|---|---|
| `ts_target_tvr_decay` / `ts_target_tvr_hump` | `lambda_min` `lambda_max` `target_tvr` | target_tvr ∈ {0.05, 0.1, 0.2, 0.3} |
| `hump` | `hump` | {0.005, 0.01, 0.02} |
| `kth_element` | `k` `ignore` | k ∈ {1, 2, 3} |
| `ts_regression` | `lag` `rettype` | rettype ∈ {0, 1, 2} |
| `ts_quantile` | `driver` | {gaussian, cauchy, uniform} |
| `ts_scale` / `ts_rank` | `constant` | {0, 1, 0.5} |
| `ts_returns` | `mode` | {1, 2} |
| `ts_decay_linear` | `dense` | {false, true} |
| `winsorize` | `std` | {1, 2, 4, 8} |
| `rank` | `rate` | {1, 2, 3} |
| `quantile` | `driver` `sigma` | sigma ∈ {0.5, 1, 2} |
| `normalize` | `useStd` `limit` | {false, true} |
| `scale` | `scale` `longscale` `shortscale` | {1} |
| `group_backfill` | `d` `std` | std ∈ {1, 2, 4, 8} |

⇒ 「窗口档」只是参数精调的一半；**命名参数档**必须单独扫（用户标准 #5）。

### 8.5 新增构造 C13（论坛派生，构造数 12 → 13）

论坛 `44941181410455`（BRAIN Tips 001）官方模板：`group_neutralize(vector_neut(ts_median(ts_backfill(FIELD,60),20), ts_median(ts_backfill(FIELD,60),250)), country)`
⇒ 经济直觉「最近相对它自己的常态，发生了什么变化」= **常态迁移速度**，与 C11 的「溢价水平」机制互异。
⇒ 来源：论坛 `44941181410455` + 论文 `10.2139/ssrn.6652118`（An Anatomy of the Stock Borrow Fee Anomaly）。
⇒ ⚠ 平台**无 `ts_median`**（`get_operators` 实拉 103 个算子清单里没有）⇒ 该帖模板需用 `ts_mean` 等价改写。

### 8.6 ★★ 新增构造 C14（尾部摩擦折叠，构造数 13 → **14**）—— **risk60 目前最强读数**

```
C14 = reverse(group_rank(
        ts_covariance(
          divide(ts_backfill(vec_max(rsk60_offer),250),
                 ts_backfill(vec_max(lending_fee_bid_rate),250)),
          ts_backfill(vec_sum(rsk60_crowding),250),
          750),
        subindustry))
```

| 读数 | 值 | 闸线 | 判定 |
|---|---:|---:|---|
| Sharpe | **0.73** | 1.58 | ✗ 差 0.85 |
| Fitness | **0.30** | 1.0 | ✗ 差 0.70 |
| 2Y IS Sharpe | **1.70** | 1.58 | **✓ 过闸**（risk60 全部读数中的 2Y 高点） |
| Turnover | 8.29% | — | ✓ |
| Sub-universe Sharpe | 0.66 | 0.4 | ✓ |
| CONCENTRATED_WEIGHT | pass | 0.10 | ✓ |
| failed_RA | **2** | — | 只剩 `LOW_SHARPE` + `LOW_FITNESS`（`LOW_2Y_SHARPE` 已进 pass 列） |
| pyramids.effective | 1 | — | GBR/D1/RISK ×1.2（risk 塔 0/3，未点亮） |

- **机制 = 尾部借券摩擦（TBR / hard-to-borrow）**：`vec_max` = 经纪商报出的**最高**费率 = 最难借的那家 ⇒ 与 C8 的「平均费率水平」**不是同一信息**。
- **折叠序实测**：max(0.73) > avg(0.66) > min(0.51) ⇒ **均值被摊薄，尾部才带稀缺性信息**；`vec_sum` ≡ `vec_avg`（同比例缩放被 `group_rank` 吸收，no-op）；`vec_stddev` / `vec_range`（离散度）双双转负 ⇒ **「费率不确定性」这条机制在本数据集不存在**。
- **两侧必须同时取 max**：max÷max 0.73/1.70 > max÷avg 0.67/1.39 ≫ avg÷max 0.28/2Y−0.15 ⇒ **尾部信息只在分子（借入费率 `rsk60_offer`）侧**。
- **轴层**：subindustry 独占最优（0.73 vs sector 0.55 / industry 0.54 / market≡exchange≡country 0.46）。
- **来源**：论文 `10.2139/ssrn.2655527`（TBR=最难借标的费率，直接对应 `vec_max` 语义）+ `10.2139/ssrn.2256795` + `10.2139/ssrn.1357069` + `10.2139/ssrn.7437258`；论坛 `44687266076823`（借券费进入成本，空头腿须单独审计）。

### 8.7 ★ 平台结构事实：GBR 单国市场 ⇒ `market` ≡ `exchange` ≡ `country`

三轴读数**逐位相同**（0.46/0.16/1.21/TO8.28%/subU0.75）⇒ 在 GBR 这三个分组字段是**同一个组**（单一交易所/单一国家）。
⇒ 扫分组轴时**任选其一即可，不必各占一个臂**（可省 2 臂位）；⚠ **此为 GBR 结构事实，不外推到多国区**。

