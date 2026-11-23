# GBR / imbalance5（Oil Price Resilience Scores，SHIELD-OIL 韧性评分，MATRIX）

> 塔：**imbalance**（GBR/D1 乘数 **1.0**，当前 0/3 未点亮）
> ⛔ **2026-11-21 用户禁令：GBR 不再用 PV 与其它数据集组腿** ⇒ 本页所有含 `ts_rank(volume, M)` 门控的模板与候选（`1YWlbQb6` / `1YWOGvmQ` / `Xgaab3nz` / `N1PLLxjw` / `0mPxKx1K`）**全部退出交付清单**（`get_alpha_details` 实读 `pyramids.effective=2`，IMBALANCE+PV）。本页读数保留作 imb5 机制参考；**PV-free 同形态（去 volume 因子）重测中**（批 `1GzMjodrG4NY8QmRUO9VhfY`）。
> 画像日期 2026-11-21 · 数据源 `mcp__wq-brain-http__get_datafields`（GBR/TOP700/D1，`filter_sharpe=false`，不传 `max_fields`）
> 本轮实拉：`count=2` / `platform_count=2` / `returned=2` / `complete=true` ⇒ 单页全量。
> ⚠ 两字段 `coverage=0.0` 是 **GBR 元数据盲区**；历史回测 `long_count` 400–520 / `short_count` 400–520 证明有数据。
> ⚠ 全 MATRIX ⇒ 探针/信号**不得套 `vec_avg`**（VECTOR 专用，类型不匹配必 FAIL）。

---

## ★ PV-free 纯单集重建（2026-11-21，PV 禁令后）

> 形态：`group_backfill(group_scale(ts_scale(imb5_score, N), industry), sector, 252)`（无 PV 门控，`pyramids.effective=1`）

| N（内核窗） | α | S | F | 2Y | TO | RA | self（对 ACTIVE 0mPPVEoK） |
|---|---|---:|---:|---:|---:|---:|---:|
| 126（基线） | `2r5XRnn8` | 2.23 | 1.48 | 1.98 | 17.5% | 0 | **0.7106 FAIL** |
| **504** | **`58JA6ewo`** | **2.06** | **1.43** | **2.00** | **15.0%** | **0** | **0.5729 PASS** |
| 250 | `LLKmXrRm` | 2.11 | 1.44 | 1.91 | 15.9% | 0 | 0.6254 PASS |
| 252 | `wpo2zPR5` | 2.12 | 1.45 | 1.91 | 15.9% | 0 | 0.6265 PASS |
| 66 | `blarPn9q` | 2.26 | 1.39 | 2.14 | 20.1% | 0 | 0.7273 FAIL |

**结论**：① PV 门控去掉后仍全闸通过（S 2.06–2.26 / 2Y 1.91–2.14 / TO 15–20%）⇒ **PV 腿不是过闸的必要条件**，此前「必须靠 volume 分散器过 prod」的判断在**平台闸层面**被推翻（相关性层面另论）；② **窗口是破 self 锁的杠杆**：N≥250 把对 `0mPPVEoK` 的相关性从 0.71 压到 0.57–0.63（N=66 反而 0.73）——长窗把 PnL 时间结构改得足够远；③ 内核层（同 N=126）全替无解（0.76–0.82），**窗口 > 内核** 对去相关。
> ⚠ 内核对 S 的影响在 PV-free 基线上仍成立：ts_scale 2.23 > ts_rank 2.01 ≈ ts_quantile 2.00 > ts_av_diff 1.81 > ts_zscore 1.85（2Y 1.29 FAIL）。
> prod 相关性待平台实测（首测遇单并发槽占用，101s 后重试）。

### 外层包装全替换（PV-free 基线 × 窗 504，2026-11-21，批 `18jQi5f4R4Awbf2FfJ1c3ag`）

| 外层 Group | α | S | F | 2Y | TO | RA | self（对 0mPPVEoK） |
|---|---|---:|---:|---:|---:|---:|---:|
| `group_scale`（基线） | `58JA6ewo` | 2.06 | 1.43 | **2.00** | 15.0% | 0 | 0.5729 PASS |
| **`group_zscore`** | **`j2aPdggW`** | **2.04** | **1.45** | 1.72 | 14.9% | 0 | **0.5562 PASS** |
| `group_neutralize` | `xAv2mnnb` | 2.07 | 1.49 | 1.53 | 14.9% | 1（2Y 差 0.05） | 未测（2Y 已挂） |
| `group_rank` | `gJago3x0` | 0.27 | 0.10 | 0.14 | 9.4% | 4 | — |
| `group_std_dev`（聚合型） | `gJago330` | 0.26 | 0.05 | 0.60 | **109.6%** | 5 | — |
| `group_sum`（聚合型） | `kqaWLK3l` | −0.55 | −0.17 | 0.03 | **107.4%** | 5 | — |

**外层结论**：`group_scale` ≡ `group_zscore`（S2.04–2.06 / 2Y 1.72–2.00），两者都过闸且 self 0.56–0.57；`group_neutralize` 2Y 1.53 差 0.05；`group_rank` 崩（0.27）——**与门控基线上 group_rank 崩的结论一致**；聚合型 TO 爆 107–110%。⇒ **PV-free 可行外层 = group_scale / group_zscore**。

### prod 实测（2026-11-21，单并发槽逐颗）

| α | 形态 | self | **prod** | 判定 |
|---|---|---:|---:|---|
| `2r5XRnn8` | group_scale × N=126 × SUBIND | 0.7106 | 0.7234 | self/prod 双 FAIL（毫厘） |
| `58JA6ewo` | group_scale × N=504 × SUBIND | 0.5729 | **0.7878** | self PASS / **prod FAIL** |
| `2r5XKm65` | group_scale × N=504 × **INDUSTRY** | 0.4427 | **0.8266** | self PASS / **prod FAIL**（[0.7,0.8) 11 对 / [0.8,0.9) 1 对） |

**★ prod 墙结构性定案（三点实测，2026-11-21 终验）**：N=126×SUBIND **0.7234** → N=504×SUBIND **0.7878** → N=504×INDUSTRY **0.8266** —— **prod 随「窗口变长」与「INDUSTRY 残差」单调上升，而这两个恰是破 self 的钥匙** ⇒ **PV-free imb5 无法同时过三闸**（self 与 prod 是同一把锁的两端，去相关杠杆全部用上只会把 prod 推得更远）。公开池 imb5 变体密度（[0.7,0.8) 11 对）就是墙本身；**唯一能过 prod 的 imb5 形态是 PV 门控版（`0mPPVEoK` 0.6865），已被用户禁令封死**。
⇒ **PV 禁令下 imb5 塔无第二席可交付**（ACTIVE `0mPPVEoK` 占 1 席）；按用户「混塔一 Shot + 不再持续投入」规则，本塔停止加注。

**prod 墙的成因（推断+实证支持）**：`imb5_score` 平台 αC **1962** / uC **770**，prod 池里有大量公开 imb5 变体 ⇒ 裸 score 的任何几何都要撞它们；**PV volume 门控之所以能把 prod 从 0.72–0.79 压到 0.6865（0mPPVEoK 实测）**，靠的是跨集分散器而非信号本身。PV 禁用后，**替代分散器只能从同一数据集里找** ⇒ 在测批 `8hiR26w14LY9qq9xPkUeX0`（4 臂）：`imb5_mktcap` 规模门控（ts_rank 22/66/126 + ts_scale），仍满足 ATOM（单数据集、`effective=1`）——**结果：4/4 全崩（S0.57–0.69）⇒ 同集无可用分散器**。

### 中性化档（2026-11-21，逐档 2 臂：N=126 / N=504）

| 档 | α（N=126 / N=504） | S | F | 2Y | TO | RA | self（N=504） |
|---|---|---|---:|---:|---:|---:|---:|---:|
| SUBINDUSTRY（基线） | 2r5XRnn8 / 58JA6ewo | 2.23 / 2.06 | 1.48 / 1.43 | 1.98 / **2.00** | 17.5/15.0% | 0 | 0.5729 |
| **INDUSTRY** | `YPaEAMzA` / **`2r5XKm65`** | 2.16 / **2.04** | 1.48 / **1.51** | **1.64** / **1.74** | 17.4/14.9% | 0 | **0.4427 PASS** |
| FAST | `blar9k7M` / `rK7NW3Q9` | 1.90 / 1.83 | 1.06 / 1.08 | **1.32 / 1.42** | 20.3/17.9% | 1 | —（2Y 挂） |
| SECTOR | 在测（`99gii5Br4QR8ULQMJ2y7C4`） | | | | | | |

**★ INDUSTRY 中性化是第二把去 self 的钥匙**：SUBINDUSTRY→INDUSTRY 后 self 从 0.57 压到 **0.4427**（N=504），同时平台闸全过（S2.04/2Y1.74/TO14.9%/RA0）。机理：`0mPPVEoK` 是 SUBINDUSTRY 行业残差口径，换 INDUSTRY 残差后 PnL 正交化程度更高。**FAST 档不可用**（风险模型中性化把 2Y 吃掉 0.5+）。

---

## 字段全表（平台实拉 2/2）

| 字段 | 类型 | cov | αC | uC | 经济含义（平台 description） |
|---|---|---:|---:|---:|---|
| `imb5_score` | MATRIX | 0.0 | **1962** | **770** | SHIELD-OIL 综合评分（0–1）：在油价冲击 regime 下的韧性/优势 |
| `imb5_mktcap` | MATRIX | 0.0 | 350 | 188 | 证券市值（本币） |

> αC/uC：1962/770（score，全集最活跃、全塔最活跃字段之一）、350/188（mktcap）。
> 数据集级：`id=imbalance5` / `name=Oil Price Resilience Scores` / `category=imbalance` / `fieldCount=2` / `coverage=0.0` / `userCount=792` / `alphaCount=2152` / `valueScore=1.0` / `pyramidMultiplier=1.0`。

---

## 4. 字段族拆解

| 族 | 字段 | 机制 |
|---|---|---|
| **A 韧性评分族**（唯一信号） | `imb5_score` | 0–1 有界评分，SHIELD-OIL 对油价冲击的行业/个股韧性；有界 ⇒ 截面分布均匀、天然可 rank |
| **B 规模族**（分母/门控） | `imb5_mktcap` | 市值（本币），量纲 10⁶–10⁹ 右偏，宜作门控/加权/分母，不作独立信号 |

**族间关系**：A 是唯一信号面（有界评分）；B 是规模刻度。本集只有 2 字段 ⇒ 信号面窄，`imb5_score` 的历史 alphaCount 1962 说明它是被广泛使用的成熟字段。

---

## 5. 可用性三分

| 分类 | 字段 | 依据 |
|---|---|---|
| **① 可直接做信号** | `imb5_score` | 0–1 有界评分、截面分布均匀，可 `ts_zscore`（有界值 ts_zscore 稳定）/`rank`/`group_*` |
| **② 可做门控/加权** | `imb5_mktcap` | 市值右偏长尾，作门控 `ts_rank` 或加权 |
| **③ 元数据盲区** | 两字段 `cov=0.0` | GBR 已知盲区，非数据缺失（历史回测双边长计数） |

---

## 6. 六法/实测

| 法 | 读数 / 结论 |
|---|---|
| **① 覆盖率** | 平台 cov=0（盲区）；实读 `longCount` 416–459 / `shortCount` 409–450（批 A 各臂）⇒ 覆盖约 60–65%，`density=dense` |
| **② 非零率** | 评分型字段，零值不是问题（评分 0 是有效值）⇒ 不判门控必要性 |
| **③ 更新频率** | 日频评分（按 regime 逐日变化）；`ts_zscore(126)` 有效、`ts_zscore(66)` 崩（见 §8）⇒ 中长窗更稳 |
| **④ 量纲** | score 0–1 有界；mktcap 10⁶–10⁹ 右偏 ⇒ mktcap 必须 `ts_rank` 去量纲 |
| **⑤ 中心** | score 有界非单边；ts_zscore 后近零均值 |
| **⑥ 分布** | score 有界均匀（0–1）；mktcap 右偏长尾 |

**模板白名单（实测得出）**：
- `multiply(group_backfill(group_zscore(ts_zscore(imb5_score, N), industry|sector), G, 252), ts_rank(volume, M))`
  - N（内核窗）∈ {126, 252}（**66 崩**：S1.89/2Y1.10）
  - G（外层分组）∈ {sector 优于 subindustry}（**sector 2.35 > subindustry 2.26**）
  - M（门控窗）∈ {22, 66, 252 差异 <0.1}；门控字段 `volume` 最佳（去门控 S 2.35→1.96 = −0.39）
- 排除：`ts_rank(imb5_mktcap,66)` 门控（S1.58/F0.92/RA3 FAIL）；内核 66；内层 sector（S 2.09，低于 industry 的 2.26）

---

## 7. 判据核验

- cov 全 0 不判 excluded：批 A 十臂 lc/sc 双边长计数 400+ 即铁证。
- 历史：GBR `backtest_results` `code LIKE '%imb5_%'` 最高 S 2.32（`d5amYQZJ`，SLOW 档），**标准档无全闸件** ⇒ 本轮批 A 是标准档首次全闸。

---

## 8. 批 A · 梯度 Δ 表（2026-11-21，标准档 SUBINDUSTRY/decay4/trunc0.08/nanON）

`multisimulation_id=3iVhNc6ty4s29JG18ttORRu9`（10 臂，单维变化，Δ 可归因）

| 臂 | 变体（相对基线单维改动） | S | F | 2Y | TO | sub | RA | inv_ratio |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| xAvVmVLJ | 基线 gate66 / subindustry / ts_zscore126 | 2.26 | 1.19 | 1.56 | 29.8% | 1.87 | 1 | 0.67 |
| P05xXxVq | 门控窗 66→22 | 2.21 | 1.12 | 1.49 | 31.6% | 1.76 | 1 | 0.68 |
| leaEREml | 门控窗 66→252 | 2.16 | 1.15 | 1.56 | 28.4% | 1.76 | 1 | 0.72 |
| akaeWepR | 门控换 5 日成交额 | 2.10 | 1.16 | 1.50 | 26.1% | 1.79 | 1 | 0.68 |
| xAvVmVZJ | 内层轴 industry→sector | 2.09 | 1.06 | 1.41 | 29.8% | 1.68 | 1 | 0.68 |
| **0mPxKx1K** | **外层轴 subindustry→sector** | **2.35** | **1.29** | **2.18** | 28.9% | 1.86 | **0** | 0.68 |
| npamOmLd | 内核窗 126→66 | 1.89 | 0.89 | 1.10 | 31.5% | 1.61 | 2 | 0.64 |
| **A1xeOeoE** | **内核窗 126→252** | **2.34** | **1.27** | **2.12** | 29.2% | 1.88 | **0** | 0.70 |
| A1xeOrRW | 去 volume 门控 | 1.96 | 1.21 | 1.54 | 18.8% | 1.58 | 1 | 0.79 |
| 58JrqAZz | 门控换 mktcap | 1.58 | 0.92 | 1.55 | 22.0% | 1.41 | 3 | 0.82 |

**Δ 归因（本轮新增）**：
1. **外层分组轴是最大杠杆**：subindustry→sector 同时抬 S(+0.09)/F(+0.10)/2Y(+0.62)/RA1→0。与 GBR 既有「轴越细 S 越高」相反——本族**反向**（有界评分在粗轴上更稳，细轴被同业噪声稀释）。
2. **内核窗 252 ≈ 外层 sector**（S2.34/2Y2.12 两条独立路径都过 2Y）：评分型信号需要长窗才稳定；**66 是崩点**（S1.89/2Y1.10）。
3. **volume 门控是门控字段最优**（+0.39 S vs 无门控）；mktcap 门控反向（−0.68 S、RA3）。
4. **SLOW 档 vs SUBINDUSTRY 档同水平**（旧 d5amYQZJ S2.32@SLOW vs 新基线 S2.26@SUBINDUSTRY）⇒ 内核跨档稳定，标准档可交付。

---

## 9. 全闸候选记录（2026-11-21）

### ★ `0mPxKx1K`（第 1 颗全闸）
- 表达式：`multiply(group_backfill(group_zscore(ts_zscore(imb5_score, 126), industry), sector, 252), ts_rank(volume, 66))`
- 设置：GBR/TOP700/D1 / SUBINDUSTRY / decay4 / trunc0.08 / nanON / maxTrade OFF
- 指标：**S 2.35 / F 1.29 / 2Y 2.18 / TO 28.9% / sub 1.86 / DD 3.9% / margin 5.99bps / RN 2.07 / invest_S 1.60 / invest_ratio 0.68**
- 闸门：`checks.fail=[]` 全 PASS（LOW_SHARPE/LOW_FITNESS/LOW_TURNOVER/HIGH_TURNOVER/CONCENTRATED_WEIGHT/LOW_SUB_UNIVERSE_SHARPE/IS_LADDER_SHARPE/CLUSTER_TEST/MATCHES_PYRAMID）｜RA failed=0
- 逐年：10/10 年正（2017 S2.63 最低正年 2023 S1.29；无空年，lc 378–483 / sc 361–469）
- self-corr：**0.1496**（本地 OS 池 33 颗）｜prod：**0.6963 PASS**（直方图 max 0.6–0.7 段 16 颗）
- 塔位：`GBR/D1/IMBALANCE`（1.0）+ `GBR/D1/PV`（1.4），effective=2 ⇒ **imbalance 塔 0/3→1/3**
- 状态：**待用户确认提交**（只挖不提交红线）

### ★★★ `1YWlbQb6`（**当前最强全闸**；2026-11-21 换层重扫产出，已替代 1YWOGvmQ）
- 表达式：`multiply(group_backfill(group_scale(ts_scale(imb5_score, 126), industry), sector, 252), ts_rank(volume, 66))`
- 指标：**S 3.16 / F 1.52 / 2Y 2.68 / TO 45.6% / sub 1.93 / DD 3.4% / margin 4.65bps / invest_S 2.47 / RA0**
- 逐年：**10/10 年正**（2019 S0.95 最低正年；lc 353–452 / sc 386–501）
- self **0.4661** PASS｜**prod 0.5732 PASS（余量 0.127）**
- 与 `Xgaab3nz` 互相关 **0.4561（<0.5）** ⇒ `max_mutually_below_subset = [1YWlbQb6, Xgaab3nz]`
- 与 `1YWOGvmQ` 互相关 0.9224（同族替代：1YWlbQb6 更强，取它）；与 N1PLLxjw 0.728
- 塔位 IMBALANCE+PV effective2
- 来源：L3 换 group_scale 后按「换层下游重扫」重测内核 → `ts_scale` 反超 `ts_zscore`（旧基线上它是劣解）

### ★★ `1YWOGvmQ`（第 2 颗全闸，被 1YWlbQb6 替代；2026-11-21 L3 梯度产出）
- 表达式：`multiply(group_backfill(group_scale(ts_zscore(imb5_score, 126), industry), sector, 252), ts_rank(volume, 66))`
- 指标：**S 3.03 / F 1.41 / 2Y 2.76 / TO 47.3% / sub 1.80 / DD 4.1% / margin 4.3bps / RN 2.69 / invest_S 2.31 / invest_ratio 0.7624**
- 闸门：`checks.fail=[]` 全 PASS（HIGH_TURNOVER 上限 0.70 ⇒ 47.3% 过）｜RA failed=0
- 逐年：**10/10 年正**（2019 S0.92 最低正年，2023 S2.08；lc 353–501 / sc 386–501）
- self-corr **0.4869** PASS｜prod **0.5523 PASS**（余量 0.148）
- 与 `Xgaab3nz` 互相关 **0.4786**（<0.5）⇒ `max_mutually_below_subset = [1YWOGvmQ, Xgaab3nz]`，**imbalance 塔可同篮两颗**（两塔组合配额内）
- 塔位：IMBALANCE（1.0）+ PV（1.4），effective=2
- 代价：TO 47.3% 超 review 偏好带（5–30%），但平台闸内且 F 1.41；如需压 TO 走 ts_decay_linear/decay 档（Layer 4/设置层）

### 备选 `A1xeOeoE`（同内核，prod 差 0.008）
- 表达式：`multiply(group_backfill(group_zscore(ts_zscore(imb5_score, 252), industry), subindustry, 252), ts_rank(volume, 66))`
- S 2.34 / F 1.27 / 2Y 2.12 / TO 29.2% / RA0 / self 0.1294 / **prod 0.7079 FAIL**（1 颗钉子 0.7–0.8）
- 与 `0mPxKx1K` 同内核（互相关待测，预计 >0.7 同席）⇒ 仅作备选，不再单独破墙。

---

## 10. 小结

- imbalance5 = 2 字段窄集，唯一信号 `imb5_score`（aC1962 成熟字段）；标准档首次跑出全闸件。
- **全闸候选 `0mPxKx1K`**：外层 sector + 内核 126 + volume 门控；prod 0.6963 贴线（0.70 下限余量 0.0037，属「单颗钉子型」近墙，后续若需更稳可再扫门控字段）。
- 塔位 imbalance 0/3 → 提交后 1/3。
- **★ 梯度完成（2026-11-21，4 层 44 臂；档案 `tracking/GBR/waves/wave20261121_gradient_imbalance5.md`）**：
  - **Layer 1（内核算子，Time Series 10/21 全替）→ 收敛于 `ts_zscore`**：唯一 ΔS 为正的 `ts_scale`（+0.08）以 **2Y −0.74** 换得（非帕累托）；水平型 `ts_mean` −1.72、波动/时效型（`ts_std_dev`/`ts_ir`/`ts_arg_max`）−1.9~−3.3 全崩。
  - **Layer 2（窗口，8 臂）→ 收敛于 {126, 252} 平台**（S 2.35 一致、2Y 2.18/2.17、RA 均 0）；短窗 22/66 是崩点（2Y 0.42/1.24），504 稍劣（2Y1.55），双窗 66+504 仅 +0.01S 不构成改进。
  - **Layer 3（外层 Group 8/9）→ 换基线到 `group_scale`**：**ΔS +0.68 / Δ2Y +0.58 / ΔF +0.12**（`group_rank` 0.55 / `group_sum` 0.29 崩塌；`group_neutralize` 丢标准化收益）⇒ **产出全闸件 `1YWOGvmQ`（S3.03/2Y2.76/prod 0.5523）**。
  - **Layer 4（门控，8 臂）→ 收敛于 `ts_rank(volume,66)`**（全 ΔS≤0）；`ts_mean(volume,5)` 是低 TO 替代（TO 47.3%→30.1%、2Y 仅 −0.03）⇒ 产出 `N1PLLxjw`。
  - `tools/gates/gradient_gate.py` 判定 **GRADIENT_DONE（arc_layers=5）**；**PROVISIONAL（梯度未完成）已解除**。
- **本集 2 颗全闸 + 1 颗低 TO 备选**：`1YWOGvmQ`（S3.03/prod 0.5523/self 0.4869，与 Xgaab3nz 互相关 0.4786 可同篮）｜`0mPxKx1K`（S2.35/prod 0.6963 余量薄）｜`N1PLLxjw`（TO30.1% 低换手替代，self/prod 待测）。
- 仍**不判死**（2 字段窄集，D1/D6 面天然窄，但已达全闸 + 四层梯度收敛）。
### 互相关矩阵（本地计算，4 年日收益，2026-11-21）

| pair | corr |
|---|---:|
| `2r5XKm65` ↔ `YPaEAMzA` | **0.9123**（同腿：只能提交一颗） |
| `2r5XKm65` ↔ `58JA6ewo` | 0.8834 |
| `YPaEAMzA` ↔ `58JA6ewo` | 0.8141 |
| **`2r5XKm65` ↔ `0mPPVEoK`（ACTIVE）** | **0.4427**（<0.5，可同篮） |
| `YPaEAMzA` ↔ `0mPPVEoK` | 0.5780 |
| `58JA6ewo` ↔ `0mPPVEoK` | 0.5729 |

⇒ `max_mutually_below_subset = [2r5XKm65, 0mPPVEoK]` ⇒ **imb5 塔可再加一席（PV-free INDUSTRY × N=504）**，与已有 ACTIVE 不撞。
