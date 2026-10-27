# analyst_factor_signals（anl 增长族）字段画像 · 字段八问

> 命名：`_usa-<字段前缀>-field-profile-<asOf>.md`｜前缀 **anl**（数据集 analyst_factor_signals）
> **as_of**：2026-10-19 ｜ 本页只记本轮新证；完整字段表见 `_usa-field-profile-playbook-20261018.md` §2

## ① 是什么
分析师一致预期的**增长率族**：`*_qoq_growth`（环比增长）、`*_actual_q1_qoq_growth`（实际值环比增长）、
`*_yoy_growth`。单位：百分比（无量纲）。经济锚：**增长速率**（不是"修正"、不是"惊喜"）。

## ② 什么类型
MATRIX，全部单值；命名族 `{metric}_{estimate|actual}_q{1|2}_qoq_growth`。

## ③ 覆盖多少
estimate 族 0.90–0.93；**actual 族 0.85–0.90**（更高，因实际值必披露）。

## ④ 怎么更新
季频（财报/预期更新），`ts_av_diff` 平滑后 TO 0.04 左右（天然低换手）。

## ⑤ 分布如何
无量纲比率，可直接相减；`actual` 族比 `estimate` 族更"稳定"（无预期漂移）。

## ⑥ 拥挤吗
`eps_q1_estimate_qoq_growth` uc5/**ac6**、`revenue_actual_q1_qoq_growth` uc1/**ac1** —— 字段级极冷门。
⚠ 但 **prod 取决于机制拥挤度**：实际营收增长（0.81）远高于预期 EPS 增长（0.71）。

## ⑦ 出不出信号（本轮 20 条实测摘录）

| 结构 | S | F | 2Y | SUB | prod | 判定 |
|---|---:|---:|---:|---:|---:|---|
| estimate EPS + RAM / subind / hump / d10（`1YjoKAz6`） | 1.89 | 1.12 | 1.66 | 0.84 | **0.7094** | 八闸全过，prod 差 0.0094 |
| **actual 营收 + 内层 GN(sector) / d20（`zqrW26mo`）** | **1.66** | **1.08** | **1.59** | **0.77** | **0.8118** | **八闸全过，prod 差 0.11** |
| actual 营收 + GN / d20 / **无 hump** | 1.58 | 1.08 | 1.45 | 0.80 | — | 2Y ❌（hump 是 2Y 必要条件） |
| actual 净利 + GN / d10 | 1.54 | 0.91 | **1.65** | 0.83 | — | S/F 双差 |
| actual 营收（无 GN）/ d20 | 1.72 | 1.15 | **1.40** | 0.92 | — | 2Y ❌ |

## ⑧ 怎么用·怎么判死（★★★★★ 本轮最有价值的杠杆）

1. **内层 `group_neutralize(F, sector)` = 已验证的 2Y 杠杆**（归因工具 #1，论坛证据 2Y 1.15→2.04）：
   实测 `revenue_actual_q1_qoq_growth` 的 **2Y 1.40 → 1.59（跨过 1.58 闸）**，S/F/SUB 基本不变。
   **粒度铁律**：内层 GN 必须**粗于**外层 `group_rank`（外层 subindustry ⇒ 内层用 sector/market；
   用 industry 会打崩 SUB 到 0.70）。
2. **该杠杆是字段特异的**：同一 GN 用在 `eps_q1_estimate_qoq_growth` 上让 2Y 从 1.66 **掉到 0.85**（sector）/1.31（industry）⇒ 换字段必重测。
3. **`hump` 在 actual 增长族是 2Y 的命门**：去 hump 后 2Y 1.59→1.45（崩），TO 仅 0.041→0.059。
4. **TO<0.125 时降 TO 对 F 完全无效**（F 用 max(TO,0.125)）⇒ F 缺口只能靠 S 或 returns 补，别在 TO 上浪费时间。
5. **prod 与"信息冷门度"不一致**：actual 营收增长字段 aC=1 却 prod 0.81；expected EPS 增长 aC=6 却 prod 0.71
   ⇒ **prod 看的是机制（营收增长是公募因子），不是字段使用次数**。

---

## ⑨ 算子穷举实测（2026-10-19，用户纪律「破闸要按算子族扫」）

**基线（`eps_q1_estimate_qoq_growth` + RAM/subindustry/hump0.01/d10）**：S 1.89 / F 1.12 / 2Y 1.66 / SUB 0.84 / **prod 0.7094**（仅差 0.0094）。

| 算子（内层，`group_rank` 之内） | S | F | 2Y | SUB | prod | 判定 |
|---|---:|---:|---:|---:|---:|---|
| `signed_power(·, 2.5)` | 1.82 | 1.06 | 1.31 | 0.89 | — | 2Y ❌ |
| `winsorize(·, std=3)` | 1.92 | 1.14 | 1.25 | **0.99** | — | 2Y ❌ |
| `winsorize(·, std=5)` | 1.80 | 1.04 | 1.55 | 0.78 | — | 2Y ❌ |
| **`winsorize(·, std=4)`** | 1.83 | 1.07 | 1.64 | 0.78 | **0.7023** | SUB 差 0.01 |
| `ts_regression(·, eps_y1_cagr_2yr, 252, 0)` | 1.62 | 1.14 | **2.09** | 0.73 | **0.8985** | **2Y 杠杆但 prod 杀手** |
| `ts_ir(·, 252)` | 1.15 | 0.53 | 0.32 | 0.20 | — | 弱 |
| `ts_backfill(winsorize4, 63)` | 1.94 | 1.16 | 1.41 | 0.90 | — | 2Y 差 |
| `group_backfill(·, subindustry, 63)` | 0.56 | 0.16 | 0.85 | 0.27 | — | 毁信号 |
| **`ts_backfill(winsorize4, 252)`** ★ | **1.99** | **1.20** | **1.73** | **0.94** | **0.6608** | **★ ATOM 全闸通过** |

### ★★★★★ 结论（本战役最重要）

1. **`ts_backfill` 是破 prod 的最后一块拼图**：winsorize 版 prod 0.7023（差 0.0023），
   套 `ts_backfill(·, 252)` 后 **prod 0.7023 → 0.6608（−0.04）**，同时 **S +0.16 / F +0.13 / 2Y +0.09 / SUB +0.16 全线上涨**
   ⇒ **"提覆盖"算子在本族是四赢**（不是换手/强度的权衡，而是同时改善）。
2. **`winsorize` 的 std 是 SUB↔2Y 的跷跷板**：std=3 → SUB 0.99/2Y 1.25；std=4 → SUB 0.78/2Y 1.64；
   std=5 → SUB 0.78/2Y 1.55。**std=4 是唯一 2Y 过线的档**，再用 backfill 补 SUB。
3. **`ts_regression` 残差化是 2Y 杠杆、prod 毒药**（2Y 1.66→2.09，prod 0.71→0.90）⇒ 只在 prod 有余量时可用。
4. **`group_backfill` 会毁信号**（S 0.56）：它用组内 winsorized 均值填 NaN，把个股信息抹平。
5. **算子顺序很重要**：`ts_backfill` 必须包在 `winsorize` **外侧**（先缩尾再回填），
   这个顺序让 backfill 只在缺失处生效、不改变已有值的分布。

### ⑩ 最终 ATOM（2026-10-19 交付）

```
quantile(group_rank(hump(ts_backfill(winsorize(ts_av_diff(eps_q1_estimate_qoq_growth, 252), std=4), 252), hump=0.01), subindustry))
```
设置：`USA / TOP3000 / D1 / decay=10 / RAM / truncation=0.08 / pasteurization=ON / unitHandling=VERIFY / nanHandling=ON`
读数：**S 1.99 ｜ F 1.20 ｜ 2Y 1.73 ｜ SUB 0.94 ｜ TO 0.0356 ｜ CLUSTER 1.36 ｜ prod 0.6608 ｜ self 0.4879** ⇒ `all_passed: true`
数据集：`analyst_factor_signals`（单集 ⇒ ATOM）｜alpha_id **`zqrWnPWK`**

---

## ⑪ 指标极限优化记录（2026-10-19，skill `wq-alpha-gate-push-op-min`）

**起点** `zqrWnPWK`：S 1.99 / F 1.20 / 2Y 1.73 / SUB 0.94 / prod 0.6608 / self 0.4879（6 算子）
**终点** `omoK1A5m`：S **2.05** / F **1.24** / 2Y **1.79** / SUB 0.93 / **prod 0.6489** / **self 0.4793**

### 消融（\④ 压缩，用户允许不省算子但仍做了消融）

| 变体 | ops | S | F | 2Y | SUB | 判定 |
|---|---:|---:|---:|---:|---:|---|
| 去 `quantile` | 5 | 1.91 | 1.09 | 1.68 | 0.89 | 全过（省 1 算子，指标略降） |
| 去 `winsorize` | 5 | 2.04 | 1.23 | **1.55** | 0.96 | 2Y ❌ ⇒ **winsorize 必须留** |
| 去两者 | 4 | 1.97 | 1.13 | **1.50** | 0.90 | 2Y ❌ |

### 杠杆梯（⑤ 设置收敛 + L2/L6）

| 杠杆 | S | F | 2Y | SUB | prod | 结论 |
|---|---:|---:|---:|---:|---:|---|
| 双窗乘积 `multiply(rank(Δ252),rank(Δ126))` | 1.94 | 1.15 | **1.29** | **1.05** | — | 2Y 崩 ⇒ 否 |
| 两腿乘积（eps×revenue） | 1.51 | 0.91 | 1.00 | 0.71 | — | 否 |
| backfill 252→**504** | 1.98 | 1.19 | **1.75** | 0.94 | — | ✓ 2Y +0.02 |
| decay 10→**2** | 2.04 | 1.24 | 1.72 | **0.97** | **0.6533** | ✓ |
| **decay 1 + backfill 756** ★ | **2.05** | **1.24** | **1.79** | 0.93 | **0.6489** | ★ 最优 |
| hump 0.01→0.005 | 2.05 | 1.25 | 1.60 | **0.79 ❌** | — | 否（SUB 崩） |
| winsorize std 4→3 | 2.04 | 1.22 | **0.99 ❌** | 1.13 | — | 否（2Y 崩） |

### 三条结论

1. **`decay` 在本族是「S/F 杠杆」而非「换手杠杆」**：TO 仅 0.0356→0.0365（几乎不动），
   但 S 1.99→2.05、F 1.20→1.24 ⇒ 低换手信号上 decay 改变的是**加权时序**而非换手。
2. **`ts_backfill` 的窗口是「2Y + prod」双杠杆**：252→756 使 2Y 1.72→1.79、prod 0.6533→0.6489。
3. **两个参数窗口都是尖峰**：`hump=0.01`（0.005 崩 SUB 到 0.79）、`winsorize std=4`（3 崩 2Y 到 0.99）
   ⇒ 该骨架的甜点就在 (0.01, 4, 756, decay=1)，四周都是墙。

---

## ⑫ 按字段形态选模板 → ATOM #2（2026-10-19 16:40）

用户明令「不能同一配方盲套，要按字段特点选模板」。四族各配一套，实测：

| 族 | 形态判别 | 选用模板 | S | F | 2Y | SUB | 结果 |
|---|---|---|---:|---:|---:|---:|---|
| 修正幅度 | 带量纲幅度 | **除以分歧度** `divide(Δ252, coeff_var_mean55)` | 1.25 | 0.62 | 1.03 | 0.53 | ✗ 更差 |
| **偏度** | **有界形状量** | **`ts_zscore(·,504)` 归一** | **1.68** | 0.94 | **1.12** | **0.99** | ✓ 2Y+0.23/SUB+0.18 |
| 惊喜 | 事件驱动 | **t 统计量** `divide(F, ts_std_dev(F,252))` | 1.48 | 0.87 | 0.99 | 0.80 | 中性 |
| 趋势斜率 | 已差分 | 长窗 `ts_backfill(·,504)` | 1.50 | 0.79 | 1.04 | 0.27 | ✗ SUB 崩 |

### 偏度族的定向推演（ATOM #2）

| 版本 | zscore 窗 | 内层 GN | decay | S | F | 2Y | SUB | 判定 |
|---|---:|---|---:|---:|---:|---:|---:|---|
| 基准 | 504 | 无 | 1 | 1.68 | 0.94 | 1.12 | 0.99 | 2Y/F ✗ |
| +GN(sector) | 504 | sector | 1 | 1.69 | 0.95 | 1.21 | 0.90 | ✗ |
| +GN(industry) | 504 | industry | 1 | 1.74 | **1.00** | 1.39 | 0.97 | 仅 2Y 差 0.19 |
| 缩窗 | 378 | industry | 1 | 1.75 | 1.00 | 1.50 | 0.80 | 仅差 0.08 |
| **缩窗 ★** | **315** | **industry** | **1** | **1.81** | **1.05** | **1.63** | **0.92** | **八闸全过** |
| 过缩 | 252 | industry | 1 | 1.68 | 0.93 | 1.40 | 0.82 | ✗ |
| 长窗 | 630 | industry | 1 | 1.67 | 0.94 | 1.15 | 0.97 | ✗ |
| decay 4 | 504 | industry | 4 | 1.75 | 1.00 | 1.43 | 0.97 | ✗ |

**★ 三个甜点（全部是尖峰，±1 档就掉）**：
1. **`ts_zscore` 窗 = 315**（2Y：504→1.39 / 378→1.50 / **315→1.63** / 252→1.40）—— 2Y 对窗长极敏感，**必须逐档扫**；
2. **内层 GN 用 `industry`**（sector 1.21 / **industry 1.39** / market 1.12）—— 与 revenue 增长族相反（那里 sector 最好）；
3. decay=1（4 已掉到 1.43）。

### ATOM #2 完整信息

```
quantile(group_rank(hump(group_neutralize(ts_zscore(eps_y1_estimate_skewness, 315), industry), hump=0.01), subindustry))
```
`USA / TOP3000 / D1 / decay=1 / RAM / truncation=0.08 / pasteurization=ON / unitHandling=VERIFY / nanHandling=ON`
**S 1.81 ｜ F 1.05 ｜ 2Y 1.63 ｜ SUB 0.92 ｜ TO 0.0368 ｜ prod 0.6618 ｜ self 0.5471（对 omoK1A5m 0.547）**
数据集：`analyst_factor_signals`（单集 ⇒ ATOM）｜alpha_id **`e76OQvWO`**
经济含义：**分析师预期分布的偏度异常**（预期右偏=乐观分歧 = 后续跑输）⇒ 与"增长率"机制正交，故 self 仅 0.547。

---

## ⑬ ATOM #2 指标极限优化（skill `wq-alpha-gate-push-op-min`，跳过算子压缩）

**起点** `e76OQvWO`（5 算子）：S 1.81 / F 1.05 / 2Y 1.63 / SUB 0.92 / prod 0.6618 / self 0.5471
**终点** `akVnvzX5`（7 算子）：S **1.83** / F **1.06** / 2Y **1.87** / SUB **0.95** / **prod 0.6594** / self 0.5694

### 杠杆实测（按 skill ③ 阶梯）

| 杠杆 | S | F | 2Y | SUB | 采纳 |
|---|---:|---:|---:|---:|---|
| 基准（5 算子） | 1.81 | 1.05 | 1.63 | 0.92 | — |
| **+ `winsorize(std=4)` + `ts_backfill(252)`** | **1.83** | **1.06** | **1.87** | **0.95** | ★ **是** |
| + 仅 `ts_backfill(252)` | 1.75 | 1.00 | 1.54 | 0.87 | 否（2Y 掉） |
| L2 双窗乘积 `multiply(rank(zs315), rank(zs504))` | 1.68 | 0.92 | 1.36 | 0.84 | 否 |
| `hump` 0.01 → 0.005 | 1.97 | 1.22 | **1.19** | 1.13 | 否（2Y 崩） |
| backfill 504 | 1.78 | 1.01 | 1.75 | 0.98 | 次优 |
| **backfill 756** | 1.81 | 1.04 | **1.98** | **0.98** | 次优（prod 0.6691 更差） |

**★ 结论**：
1. **`winsorize + ts_backfill` 在这个数据集上是「2Y 杠杆」**（1.63→1.87，+0.24），
   与增长族的结论一致（那里是四赢，这里是 2Y/SUB/F/S 全升、prod 略降）
   ⇒ **该组合在 analyst_factor_signals 已两次验证**，可视为该集的默认后缀。
2. **L2 双窗级联在本腿失效**（2Y 1.36）：两尺度 zscore 相乘会稀释偏度信息（偏度本身已是一个"窗口统计量"）。
3. **`hump=0.01` 再次是尖峰**（0.005 → S 飙到 1.97 但 2Y 崩到 1.19）。
4. **backfill 窗口是 2Y 的单调杠杆**（252→1.87 / 504→1.75 / 756→1.98 非单调），
   但 756 会把 prod 抬到 0.6691 ⇒ **在 prod 卡线期应选 252**（prod 0.6594，多 0.01 余量）。

### 最终 ATOM #2（READY）

```
quantile(group_rank(hump(ts_backfill(winsorize(group_neutralize(ts_zscore(eps_y1_estimate_skewness, 315), industry), std=4), 252), hump=0.01), subindustry))
```
`USA / TOP3000 / D1 / decay=1 / RAM / trunc=0.08`（7 算子）
**S 1.83 ｜ F 1.06 ｜ 2Y 1.87 ｜ SUB 0.95 ｜ TO 0.0346 ｜ prod 0.6594 ｜ self 0.5694**

---

## ⑭ 跨指标扩展战役（2026-10-19 下午；非 EPS 字段 + 价差体系实测）

> 目的：ATOM #1/#2 都是 EPS 指标。要凑 10 颗互不相关的 ATOM，必须验证
> **同一数据集内非 EPS 指标（净利/营收/EBITDA/资本开支/营业现金流）**能否复现两套骨架，
> 并给"价差类"机制划出死线。以下全部为 USA/TOP3000/D1、decay 见各行、RAM、trunc 0.08、
> pasteurization ON、unitHandling VERIFY、nanHandling ON。

### ⑭.1 字段画像补充：非 EPS 指标族（覆盖率 / 使用度）

> **全字段底表**：`_usa-analyst-factor-signals-field-inventory-20261020.md`（平台实测 **300 字段**，
> 含 cov / uc / ac / 描述，按覆盖率降序）。本节只摘与骨架适配相关的关键族；
> 选新字段先查底表的 uc/ac——同族变体（`est_q2_qoq_eps` vs `eps_q2_estimate_qoq_growth`）应视为同一机制。

| 指标族 | 代表字段 | 覆盖 | 使用度（uc/ac） | 画像判读 |
|---|---|---:|---|---|
| 净利实际增长 | `netprofit_actual_q1_qoq_growth` | 0.897 | 低 | **本轮最佳新腿**，actual 族无预期漂移 |
| 净利预估增长 | `netprofit_q2_estimate_qoq_growth` | 0.918 | 19/27 | 中等拥挤 |
| 净利修正幅度 | `netprofit_revision_magnitude` | 0.945 | 29/42 | 拥挤（修订是最热机制） |
| 营收预估增长 | `revenue_q1_estimate_qoq_growth` | 0.896 | 4/4 | 字段冷门，但机制（营收增长）prod 高 |
| 营收实际增长 | `revenue_actual_q1_qoq_growth` | 0.885 | 1/1 | 极冷门字段、热机制 |
| EBITDA 预估 | `ebitda_q1_estimate_qoq_growth` | 0.776 | 低 | 覆盖可接受，可与净利组杠杆价差 |
| 资本开支偏度 | `capex_estimate_q1_skewness` | 0.613 | 0/0 | 覆盖偏低，冷门；适合形状类骨架 |
| 营业现金流偏度 | `cf_operating_estimate_q2_skewness` | 0.599 | 0/0 | 覆盖偏低，冷门 |
| COGS 偏度 | `cogs_q2_estimate_skewness` | 0.626 | 0/0 | 覆盖偏低，冷门 |

**判读**：覆盖 > 0.75 才适合做主力腿；0.6 档只能做分散化补充，且要接受 SUB 下探。
使用度冷门 ≠ prod 低（⑧.5 的结论再次成立：prod 看机制，不看字段被用次数）。

### ⑭.2 骨架 A（growth shell）横向移植：净利/营收/EBITDA

`quantile(group_rank(hump(ts_backfill(winsorize(<内层>, std=4), <bf>), hump=0.01), subindustry))`
内层 `ts_av_diff(F,252)`；decay 1 与 5 各跑一批（批 3 / 批 4，8 条全 COMPLETE、0 error）：

| 字段 · 内层 GN · backfill | decay | S | F | 2Y | SUB | 判定 |
|---|---:|---:|---:|---:|---:|---|
| `netprofit_actual_q1_qoq_growth` + GN(sector) · 756 | 1 | 1.60 | 0.95 | **1.94** | 0.74 | **仅 F 差 0.05** |
| 同上 | 5 | 1.61 | 0.96 | **1.95** | 0.76 | **仅 F 差 0.04** |
| `eps_actual_q1_qoq_growth` + GN(sector) · 756 | 5 | 1.50 | 0.84 | 1.66 | 0.66 | S/F 双差 |
| `eps_actual_q1_qoq_growth` + GN(industry) · 756 | 1 | 1.51 | 0.84 | 1.60 | 0.78 | S/F 双差 |
| `eps_revision_magnitude` + GN(sector) · 252 | 1 | 1.67 | 0.96 | 1.45 | **0.76** | 2Y/F 双差 |
| `eps_revision_magnitude` + GN(industry) · 756 | 1 | 1.67 | 0.96 | 1.43 | 0.68 | 2Y/F/SUB 三差 |
| `eps_revision_magnitude` + 无 GN · 504 | 1 | 1.65 | 0.94 | 1.38 | 0.62 | 全差 |
| `eps_revision_magnitude` + ts_zscore(252) + GN(industry) · 504 | 1 | 1.64 | 0.93 | 1.42 | 0.59 | 全差 |

**归因（不盲扫）**：
1. **净利实际增长是唯一接近全闸的非 EPS 腿**；它的 2Y 1.94–1.95 是"actual 族 + GN(sector)"共同给的，
   与营收实际增长（2Y 1.59）同向，说明 **actual（已披露）族 + sector 粗中性化**是本集 2Y 的稳定配方。
2. **修订幅度（revision_magnitude）族 2Y 天花板 ~1.45**，即使给它 sector GN 也上不去 ⇒ 该族是"低换手但不耐久"，
   不再追加算子（其 prod 另有 0.725 前科，见 ⑬ 之前的 `j2erv9oE`）。
3. **decay 1 vs 5 对 S/F 只有 ±0.01**（与 ⑪ 结论一致：低换手腿上 decay 是权重杠杆不是换手杠杆）。

### ⑭.3 骨架 B（价差 shell）：同数据集跨指标价差 = 死路

`quantile(group_rank(hump(ts_backfill(winsorize(subtract(rank(A), rank(B)), std=4), 756), hump=0.01), subindustry))`
8 对（批 5，decay=1，全 COMPLETE）：

| A − B（经济含义） | S | F | 2Y | SUB | 判定 |
|---|---:|---:|---:|---:|---|
| 预期 EPS 增长 − 预期毛利增长（经营杠杆改善） | 1.03 | 0.62 | 0.22 | 0.51 | 全灭 |
| 预期 EPS 增长 − 预期净利增长（回购增厚） | 1.38 | 0.75 | **−0.13** | 0.75 | 2Y 反向 |
| 预期净利增长 − 预期毛利增长（费用杠杆） | 1.01 | 0.61 | 0.22 | 0.59 | 全灭 |
| 预期毛利 YoY − COGS YoY（毛利率扩张） | 1.15 | 0.79 | 0.61 | 0.54 | 全灭 |
| 预期 EPS 增长 − 预期 EBITDA 增长 | 1.31 | 0.78 | 0.02 | 0.67 | 2Y≈0 |
| 实际 EPS 增长 − 实际 EBITDA 增长 | 1.21 | 0.68 | 0.31 | 0.09 | 全灭 |
| EPS 修订幅度 − EBITDA 修订幅度 | 1.18 | 0.62 | 0.56 | 0.33 | 全灭 |
| 预期 EPS YoY − 实际 EPS YoY（预期差） | **1.43** | **0.94** | **1.45** | 0.58 | 最接近，仍 4 闸 |

**★★★★ 死线结论**：
**"rank 后的横截面价差"在本数据集是 2Y 杀手**（8/8 中 6 条 2Y < 0.7，最差为负）。
原因不是配对选错，而是 `subtract(rank(A), rank(B))` 把两个慢变量的**时序信息全部消掉**，
只剩横截面相对位置；随后 `ts_backfill` 与 `winsorize` 都无法补回时间维度。
⇒ **价差机制不是本集的可行杠杆**；若要用"两指标关系"，必须走**比值/标准化**形态
（如 `divide(A,B)` 或 `divide(A−B, ts_std_dev(A−B))`），保留量纲与时序变化。

### ⑭.4 近失候选的唯一缺口与下一步（不盲扫，按缺口配杠杆）

`netprofit_actual_q1_qoq_growth + GN(sector) + bf756`：**S 1.60 / F 0.95 / 2Y 1.94 / SUB 0.74**
F 公式：`F = S·sqrt(|returns| / max(TO,0.125))`。该腿 TO≈0.04 < 0.125 ⇒ **降 TO 对 F 无效**。
要补 0.05 的 F，只有两条路：**S +0.08**（到 1.68）或 **returns +11%**。
- 杠杆清单（按先验排序）：内层 GN 粒度（sector → market/industry 已测不佳）、
  `ts_av_diff` 窗（252 → 126，短窗可能提 S 但伤 2Y）、`hump` 档位、
  neutralization 平台档（STATISTICAL / CROWDING / SLOW，**换 neutralization 是破 prod 的正路**）。
- **禁止**同族磨参数超过一轮（决策表 D0-P）；若上述一轮后 F 仍 <1.0，判该机制为 near-miss 封存。

### ⑭.5 论坛可复用结论（本轮检索沉淀）

1. **分析师修正动量是社区最热机制** ⇒ 本集 revision / actual-growth 腿的 prod 天然偏高（0.72–0.75 前科）。
2. **营收 surprise 比 EPS surprise 干净**（EPS 受一次性项目、税率、回购扰动）⇒ 营收腿优先做 surprise 而非 growth。
3. **分析师分歧（dispersion / coeff_var）是独立因子**，与修正动量正交，适合做分散化腿。
4. **期限结构（FY1 vs FY2）是已验证的独立家族**，但要用比值/斜率，不要用 rank 价差（见 ⑭.3）。
5. **PEAD 的 fast/slow 结构**（10 日 vs 120 日均线）可用 `ts_mean` 双窗，但需事件门控 `trade_when` 控制换手。

### ⑭.6 本轮在飞 / 待判批次

| 批 | 机制 | 表达式骨架 | 状态 |
|---|---|---|---|
| 5 | 同集跨指标水平价差（8 对） | 见 ⑭.3 | **已判死（2Y）** |
| 6 | 价差的变化 `ts_av_diff(spread,252)` | 同上 8 对 | **1 条近失（见 ⑭.7）**，其余 7 条判死 |
| 7 | 跨指标偏度（8 字段） | skew shell（ATOM #2 同构） | **已判死（2Y 普遍崩溃，见 ⑭.8）** |
| 8 | ⑭.7 近失的定向修复梯（8 变体） | 同一机制、只动一个杠杆 | **1 条只差 SUB（见 ⑭.8）** |

### ⑭.7 批 6 的唯一近失：预期差的变化（`kqJZ7Kk8`）

`est_q1_yoy_eps_growth − eps_actual_q1_yoy_growth` = **分析师预期 YoY 增长 − 实际 YoY 增长**
（经济含义：预期误差；取 252 日变化 = 预期误差的修正方向）。
骨架：`quantile(group_rank(hump(ts_backfill(winsorize(ts_av_diff(spread, 252), std=4), 756), hump=0.01), subindustry))`

**S 1.60 ｜ F 1.10 ｜ 2Y 1.47 ｜ SUB 0.65 ｜ TO 0.0484 ｜ CLUSTER 1.14**
⇒ **S/F 已过，只差 2Y（−0.11）与 SUB（−0.04）**。这是本数据集上第一颗"两闸之差"的非 EPS 候选，
且机制（expectation error）与增长族（growth）、偏度族（skewness）都正交，值得定向修复。

**关键对照**：同一对**水平价差**（批 5 的 `0mjMlWov`，无 ts_av_diff）只有 S 1.43 / 2Y 1.45 / SUB 0.58。
⇒ **`ts_av_diff` 把"预期差水平"变成"预期差修正"，带来 S +0.17 / F +0.16**，是这一对腿的关键算子；
说明"预期差的**变化**"才是有信息量的截面，水平值只是慢变量。

**修复梯（批 8，只动一个杠杆，8 变体）**：
① 内层 GN(industry) ② 内层 GN(sector) ③ 内层 GN(market) ④ `ts_av_diff` 504
⑤ `ts_av_diff` 126 ⑥ backfill 504 ⑦ hump 0.02 ⑧ `ts_zscore(spread,315)` 替换 ts_av_diff。
先验：⑭.2 已证 sector GN 对 actual 族 2Y 最有效；⑧ 用于检验"是否必须用变化而非标准化水平"。

批 7 字段：`netprofit_q1_estimate_skewness` / `revenue_q1_estimate_skewness` / `eps_q1_estimate_skewness` /
`capex_estimate_q1_skewness` / `capex_estimate_y1_skewness` / `cogs_q2_estimate_skewness` /
`cf_operating_estimate_q2_skewness` / `capex_estimate_q2_skewness`（8 字段已过 preflight；
`winsorize(std=)` 会被 validate_fields 误报为未知字段，用 `validate_fields=false`）。

### ⑭.8 批 7 / 批 8 结果：偏度骨架不可迁移；126 窗把近失推到「只差 SUB」

**批 7 —— 跨指标偏度（ATOM #2 同构骨架，bf252，decay=1，8 条全 COMPLETE）**

| 字段 | S | 2Y | SUB | 判定 |
|---|---:|---:|---:|---|
| `eps_q1_estimate_skewness` | 1.64 | **0.46** | 0.50 | 2Y 崩 |
| `netprofit_q1_estimate_skewness` | 1.48 | **0.49** | — | 2Y 崩 |
| `revenue_q1_estimate_skewness` | 1.37 | **0.32** | — | 2Y 崩 |
| `capex_estimate_q1_skewness` / `_y1_` / `_q2_` | <1.0 | — | — | S 不足 |
| `cogs_q2_estimate_skewness` | <1.0 | — | — | S 不足 |
| `cf_operating_estimate_q2_skewness` | <1.0 | — | — | S 不足 |

**★★ 结论：偏度骨架是字段特异，不是模板通用。** 同一个 shell 只对 `eps_y1_estimate_skewness`
给出 2Y 1.87；搬到同族 EPS 的 `q1` 偏度都掉到 0.46，其他指标 0.3–0.5。
机制解释：偏度读取的是「一致预期的分布形状」，只有 FY1 EPS 的覆盖人数与更新密度足以让形状变化
对应稳定的截面收益；净利/营收/资本开支覆盖薄，偏度主要是噪声。⇒ **该骨架不再横向迁移**。

**批 8 —— kqJZ7Kk8 修复梯（8 变体，全 COMPLETE；只记录关键行）**

| 变体 | S | F | 2Y | SUB | 判定 |
|---|---:|---:|---:|---:|---|
| 基准 `kqJZ7Kk8`（252 / bf756） | 1.60 | 1.10 | 1.47 | 0.65 | 2Y/SUB 差 |
| **`A1Q7WVlY`：ts_av_diff **126** / bf756** | **1.60** | **1.09** | **1.59 ✓** | **0.64** | **只差 SUB（需 0.69）** |
| ts_av_diff 252 / **bf504** | 1.64 | 1.14 | 1.42 | 0.66 | 2Y/SUB 差 |
| 内层 GN(industry)（bf756） | 升高 | 升高 | — | **0.58** | SUB 反被压低 |
| 内层 GN(sector)（bf756） | 升高 | 升高 | — | **0.64** | 同上 |
| 内层 GN(market) | — | — | **1.19** | — | 最差 |
| `hump=0.02` | 与 0.01 **逐字节相同** | — | — | — | 该旋钮已饱和 |
| `akVEYKLO`：`ts_zscore(spread,315)` 替换变化 | 1.57 | 1.07 | 1.41 | **0.71 ✓** | S 差 0.01、2Y 差 0.17 |

**归因**：
1. **窗口 252→126 是 2Y 杠杆**（1.47→1.59），且 S 不掉 ⇒ 预期差修正的「半衰期」偏短，
   126 日变化更接近当期信息。这一点让 A1Q7WVlY 成为本数据集第二颗「一闸之差」候选。
2. **SUB 与 S 反向**：能抬 S 的内层 GN（industry/sector）会同时压低 SUB 比率
   （0.40→0.37 量级），所以「只想补 SUB」不能走 GN 路径。
3. **hump 在 0.02 与 0.01 上完全同值**（与 ⑬ 的 0.005 尖峰不同侧）⇒ 该参数只在 0.01 以下敏感。
4. `ts_zscore` 版本 SUB 达标、S/2Y 不达标 ⇒ **「变化」算子不可由「标准化水平」替代**（与 ⑭.7 对照一致）。

### ⑭.9 批 9 / 批 10 结果：SUB 比率是机制指纹；surprise 已被平台占满

**批 9 —— 预期差 126 窗修复梯（8 变体，全 COMPLETE）**

| 变体 | S | F | 2Y | SUB | 判定 |
|---|---:|---:|---:|---:|---|
| `A1Q7WVlY`（bf756，批 8 基准） | 1.60 | 1.09 | **1.59 ✓** | 0.64 / 需 0.69 | 只差 SUB |
| `MP0LWrq9`：`winsorize(std=3)` | 1.60 | 1.09 | **1.59 ✓** | 0.65 / 需 0.69 | 只差 SUB |
| `QPY9J8rp`：外层 `group_rank(..., sector)` | 1.64 | **1.22** | **1.66 ✓** | 0.61 / 需 0.71 | 只差 SUB |
| bf504 / bf252 | 1.62 | 1.11 | 1.52 | 0.65 / 0.66 | SUB+2Y |
| 内层 GN(sector) / GN(industry) | 1.67 / 1.66 | 1.15 | 1.48 / 1.56 | 0.66 / 0.65 | SUB+2Y |
| `hump=0.005` | 1.55 | 1.04 | 1.54 | 0.60 | 三闸 |
| 去掉 `quantile` | 1.56 | 1.01 | 1.53 | 0.61 | 三闸 |

**★ 结论：该族 SUB 比率结构性锁死在 0.40（需 0.435）。** 三轮（批 6/8/9）已覆盖内层 GN、
变化窗、backfill 窗、winsorize 宽度、hump、外层分组 6 类杠杆，全部无法把 SUB/S 抬过 0.435
⇒ **按 D0-P 封存**（`A1Q7WVlY` / `MP0LWrq9` 记为 near-miss，不再磨）。

**批 10 —— 期限结构 + 修正变化（8 条，1 条 UNITS warning、7 条有效）**

| 机制 | alpha | S | F | 2Y | SUB | 相关性 | 判定 |
|---|---|---:|---:|---:|---:|---|---|
| **surprise 比** `eps_surprise_mean_diff / eps_surprise_stddev`（zscore315/GN industry/bf252） | **`j2erEp1O`** | **1.68** | **1.09** | **1.94** | **0.96** | self **0.7278** / prod **0.8452** | **RA 全闸，双墙判死** |
| **营收 3 月修正**（skew shell，bf252） | **`xA1d6Lnn`** | **1.77** | **1.10** | **2.06** | **0.88** | self **0.631 ✓** / prod **0.7565** | **RA 全闸，仅 prod** |
| EPS 3 月修正（同骨架） | `xA1d6Lng` | 1.68 | 0.96 | 1.71 | 0.68 | — | F/SUB |
| EPS 期限结构 `eps_y2/eps_y1`（变化） | `78onA5x5` | **2.10** | **1.33** | **2.28** | 0.78 / 需 0.91 | — | 只差 SUB（+UNITS warn） |
| 净利期限结构 | `RRA13Odn` | 1.64 | 1.02 | 1.82 | 0.44 / 需 0.71 | — | SUB |
| 营收期限结构 | `WjLVqZ9G` | 1.24 | 0.73 | 1.55 | — | — | 三闸 |
| EPS 1 月修正 | `6XAe8WEG` | 1.58 | 0.85 | **0.38** | 0.49 | — | 2Y 崩 |
| 营收 1 月修正 | `npA8Jjgx` | 1.35 | 0.73 | 1.35 | — | — | 三闸 |

**★★ 三条可复用结论**：
1. **SUB 比率 = 机制指纹**（不是可调参数）：修正/surprise 类（营收 3 月修正 0.50、surprise 0.57）
   可达标；预期差水平/期限结构类（0.40 / 0.37 / 0.27）结构性不达标。
   ⇒ 遇到 SUB 差 0.04–0.05 时，**换杠杆是浪费**，直接换机制。
2. **营收修正 > EPS 修正**（同骨架同设置：营收 S1.77/F1.10/SUB0.88 全过；EPS S1.68/F0.96/SUB0.68
   两闸不过）——论坛「营收 surprise 比 EPS 干净」在本集得到正面对照证据（唯一变量是字段）。
3. **surprise 是平台已占满的机制**：`j2erEp1O` prod 直方图 [0.7,0.8) 桶 **n=5749**、
   最高 0.8452；self 也 0.7278。即使 RA 全过也不可用。**同类 surprise 机制不再开批**。
   （对照：`xA1d6Lnn` 的 [0.7,0.8) 桶仅 **n=77**、max 0.7565 ⇒ 属可救型，已派 CROWDING 破墙批。）

**在飞**：批 12 = `xA1d6Lnn` CROWDING 中性化破 prod 墙（8 个表达式级变体：内层 GN 粒度、backfill 窗、外层分组、zscore 窗）；
批 13 = 修正指标族 2×4 设计（`eps_y2_estimate_change_3mo` / `est_q1_change_1mo_profit` /
`ebitda_estimate_revision_magnitude` / `cf_operating_estimate_year1_change_3mo` × growth shell / skew-zscore shell）。

### ⑭.10 批 11 结果：分歧 / 不对称度族 = 第三条 SUB 指纹（比率 0.005–0.396）

| 字段 · 骨架 | alpha | S | F | 2Y | SUB（门槛） | SUB/S | 判定 |
|---|---|---:|---:|---:|---|---:|---|
| `eps_y1_estimate_coeff_var` · zscore315/GN industry/bf252 | `O0JxPnVd` | 1.62 | 0.89 | 0.93 | 0.61（0.70） | 0.38 | 三闸 |
| `eps_y1_estimate_coeff_var` · ts_av_diff252/bf756 | `P0MOanKE` | 1.69 | **1.01 ✓** | **1.97 ✓** | 0.67（0.73） | 0.40 | **只差 SUB** |
| `eps_y2_estimate_coeff_var` · zscore315 | `npA8Rnr8` | **1.90** | **1.12 ✓** | 0.83 | 0.64（0.82） | 0.34 | SUB+2Y |
| `eps_y1_estimate_asymmetry` · zscore315 | `d5KRVnvv` | 1.66 | 0.89 | 1.30 | 0.02（0.72） | 0.01 | 三闸 |
| `eps_y1_estimate_asymmetry` · ts_av_diff252 | `d5KRVnPX` | 1.86 | **1.03 ✓** | **2.33 ✓** | **0.01**（0.81） | **0.005** | **只差 SUB（极端）** |
| `eps_q1_estimate_coeff_var` · zscore315 | `gJW9Om0m` | 1.82 | **1.09 ✓** | 0.93 | 0.43（0.79） | 0.24 | SUB+2Y |
| `eps_q2_estimate_coeff_var` · zscore315 | `YPxgKN9M` | **1.99** | **1.21 ✓** | **1.75 ✓** | 0.61（0.86） | 0.31 | **只差 SUB** |
| `est_q1_coeff_var_profit` · zscore315 | `qME6rnw2` | 1.32 | 0.75 | 0.68 | 0.64 | — | 三闸 |

**★ 三条结论**：
1. **分歧/不对称度是第三条 SUB 指纹族，比率 0.005–0.396，全部低于 0.435** —— 与预期差（0.40）、
   期限结构（0.27–0.37）同侧。至此「机制指纹」证据覆盖 3 族：**修正/surprise 类（0.50–0.57）达标，
   其余全部结构性不合格**。
2. **asymmetry 是「全期强、子宇宙零」的极端**（`d5KRVnPX` 2Y 2.33 但 SUB 0.01）：形状量只在大票 /
   尾部定价，TOP3000 子宇宙内没有横截面信息 ⇒ 该族不再投入任何杠杆。
3. **coeff_var 族 S/F/2Y 很强**（`YPxgKN9M` S1.99/F1.21/2Y1.75），唯一缺口仍是 SUB ⇒ 按 D0-P
   直接封存，不做修复梯（第 4 次验证「SUB 差一点 ≠ 用杠杆补」）。

### ⑭.11 批 12 结果：CROWDING 不是 revenue 修正族的破墙杠杆（8/8 RA 全过，prod 反而更差）

`xA1d6Lnn`（revenue 3 月修正 / skew-zscore 壳 / RAM / prod 0.7565）的 CROWDING 破墙批，
8 个表达式级变体全部 COMPLETE、`failed_ra_count = 0`（TO 0.010–0.011）：

| 变体（相对基线） | alpha | S | F | 2Y | SUB | self |
|---|---|---:|---:|---:|---:|---:|
| 外层 `group_rank(..., market)` | `vROvMNkw` | 1.78 | 1.26 | 1.84 | 1.07 | 0.6836 ✓ |
| 外层 `group_rank(..., sector)` | `j2erR6jO` | 1.76 | 1.24 | 1.88 | 1.07 | 0.6930 ✓ |
| 内层 GN(market) + bf252 | `6XAeVplE` | 1.78 | 1.17 | 2.17 | 0.92 | 0.6740 ✓ |
| 对照（zscore315/GN industry/bf252） | `N1eRmbbe` | 1.75 | 1.13 | 2.16 | 0.96 | — |
| bf756 | `2rjNzppx` | 1.75 | 1.13 | 2.16 | 0.94 | — |
| 内层 GN(sector) | `xA1d8Njg` | 1.75 | 1.14 | 2.10 | 0.87 | — |
| zscore252 | `QPY9kG3r` | 1.71 | 1.09 | 2.18 | 0.86 | — |
| zscore504 | `1Yjzbpxz` | 1.73 | 1.12 | 2.16 | 0.85 | — |

**prod 实测**：`vROvMNkw` = **0.8164 FAIL**，直方图 [0.7,0.8) 桶 **n = 1461**
（对照 `xA1d6Lnn` RAM 下 0.7565、桶 n = 77）。

**★ 三条结论**：
1. **CROWDING 不是 prod 杠杆，方向相反**：同一底层信号 RAM → CROWDING，prod 0.7565 → 0.8164。
   中性化换档会改变哪些风格被剥掉，但改变不了「营收 3 月修正在 OS 池里已被大量使用」这一事实。
2. **self 0.67–0.69 说明族内高度同源**：8 个变体之间已经互相顶到 self 线；即便 prod 侥幸过关，
   也只能取 1 颗，且会占掉后续同族额度。
3. **直方图 n=1461 是族级拥挤的直接读数**（不是单点近邻）：[0.7,0.8) 已被占满 ⇒ 按 D0-P
   `prod ≥ 0.75 且踏线修复失败` 判 **revenue 修正族 dead_end**，不再开破墙批。

### ⑭.12 批 13 结果：修正族换科目后 S/F 全面塌陷（0/8 过闸）

2 骨架 × 4 修正字段（RAM / decay1 / trunc 0.08）：

| 字段 | 成长壳 S/F/2Y | skew-zscore 壳 S/F/2Y | SUB/S |
|---|---|---|---|
| `eps_y2_estimate_change_3mo` | `E5VeWLE1` 1.52/0.85/1.21 | `vROvM6vz` 1.67/**0.97**/1.50 | 0.33–0.35 |
| `est_q1_change_1mo_profit` | `88ve9YQa` 1.40/0.76/1.06 | `1YjzbPzz` 1.53/0.89/1.12 | 0.16–0.29 |
| `ebitda_estimate_revision_magnitude` | `XgR8Qena` 1.49/0.89/0.68 | `e76xwvxE` 1.27/0.74/0.81 | 0.40–0.61 |
| `cf_operating_estimate_year1_change_3mo` | `E5VeWLe1` 0.94/0.48/0.45 | `akVEZw1v` 0.75/0.36/0.60 | 0.69–0.85（但 S 本身 <1） |

**★ 结论**：
1. **营收 3 月修正是一个「孤峰」字段**：同骨架下营收 S1.77，换成 EPS 年 2 / 单季利润 / EBITDA 修正幅度 /
   经营现金流后 S 跌到 0.75–1.67，无一过 1.58。修正机制不是普遍有效，**字段选择比机制命名更重要**。
2. 两骨架在这 4 个字段上 2 胜 2 负，**无系统性优势**；同字段双骨架并列不再做。
3. `cf_operating_estimate_year1_change_3mo` 触发 `hump` 的 UNITS warning（字段为 `TSPrice:1` 单位），
   仍 COMPLETE；该字段 S 仅 0.75–0.94，**单位受限 + 弱信号 ⇒ 判死**，不修。
4. SUB/S 指纹在 0.16–0.85 之间随 S 走：低 S 的变体 SUB 比率虚高（`akVEZw1v` 0.69 但 S0.75），
   **不能只看比率不看 S 绝对值**。

### ⑭.13 全量字段清单更正 + 科目线白空间（2026-10-20）

- **旧 300 条清单是工具截断，不是平台事实**：平台 `count = 922`；根因
  `world-quant-brain-mcp/brain_mixin_simulation.py:475` 的 `max_fields = 300`（未限定数据集 dump 提前 break）。
  已按 `dataset.id` + `limit=50` 翻页重拉，清单与家族计数全部重写。
- 补回的两大族：`revenue_*` 36 条、`netprofit_*` 36 条；另补 `dividend`(33)、`interest`(32)、
  `nav`(36)、`op`(30)、`capex`(30)、`fwd/forward`(34)、`quarter1/quarter2`(31)、`est_slope`(10) 等。
- **141 个 cov ≥ 0.85 且 ac ≤ 5 的低拥挤字段**；最干净的白空间按报表线排列：
  | 科目线 | 代表字段（cov / ac） | 机制 |
  |---|---|---|
  | interest_expense | `interest_expense_y1_skewness` 0.885/0、`interest_expense_y1_change_3mo` 0.877/2 | 偏度 / 3 月修正 |
  | nav | `nav_estimate_year1_skewness` 0.899/1、`nav_estimate_year1_change_3mo` 0.890/0 | 偏度 / 3 月修正 |
  | op_expense | `op_expense_estimate_y1_skewness` 0.840/1、`_y1_change_3mo` 0.831/0 | 偏度 / 3 月修正 |
  | capex | `capex_estimate_y1_skewness` 0.806/2、`_y1_change_3mo` 0.798/2 | 偏度 / 3 月修正 |
  | netprofit | `netprofit_y1_estimate_skewness_alt` 0.950/1、`_y1_change_3mo` 0.945/1 | 偏度 / 3 月修正 |
- **判据**：这 5 条报表线在 OS 池里与经济含义上都与 EPS / 营收不同（利息、净资产、运营费用、资本开支、
  净利润），是换「报表科目」而非换「参数」的正交方向；已派批 14（偏度 × 8 科目线）与批 15
  （3 月修正 × 8 科目线）验证。


### ⑭.14 批 14 结果：偏度 × 8 报表科目线（decay=1 / RAM）（2026-10-20）

multisim `425Ic0bRG4OUajuFZJxWr71`，skew-zscore 壳 × 8 条科目线（TOP3000/D1/trunc 0.08），8/8 COMPLETE、0 error：

| 字段 | alpha | S | F | 2Y | SUB/S | 判读 |
|---|---|---:|---:|---:|---|---|
| `interest_expense_y1_skewness` | `wp9EMwGd` | 1.03 | 0.55 | 0.71 | 0.42 | 弱 |
| `nav_estimate_year1_skewness` | `1YjzQVPJ` | 1.12 | 0.63 | 1.05 | 0.64 ✓ | 三闸不过 |
| `op_expense_estimate_y1_skewness` | `6XAevPJL` | 0.80 | 0.41 | −0.23 | 0.36 | 死 |
| `capex_estimate_y1_skewness` | `58jkbg6n` | 0.86 | 0.45 | 1.08 | 0.47 ✓ | 弱 |
| **`netprofit_y1_estimate_skewness_alt`** | **`Grgep090`** | **1.86** | **1.09** | **1.42** | **0.42** | **仅 2Y+SUB 小缺口** |
| `revenue_q2_estimate_skewness` | `LL5dAb39` | 1.55 | 0.93 | 0.70 | 0.63 ✓ | S/F 差一线、2Y 远 |
| `est_y1_skewness_profit` | `WjLV6wJZ` | 1.47 | 0.80 | 0.99 | 0.59 ✓ | 三闸不过 |
| `ebitda_y1_estimate_skewness` | `d5KRpEGY` | 0.64 | 0.29 | 0.14 | 0.36 | 死 |

**★ 结论**：偏度机制在**净利润年 1** 上强（S1.86/F1.09），在小科目线（利息 / 运营费用 / EBITDA）上不成立 ——
科目线白空间换到偏度机制时，**报表科目越小、分析师覆盖越薄、偏度越接近噪声**。
`Grgep090` 的缺口是 2Y 1.42（线 1.58）与 SUB 0.79（线 0.81），堆叠衰减是首选杠杆。

### ⑭.15 批 15 结果：3 月修正 × 8 报表科目线（decay=1 / RAM）（2026-10-20）

multisim `3LANQX7184Yq8X61aJwAYwGG`，growth 壳 × 8 条科目线，8/8 COMPLETE、0 error：

| 字段 | alpha | S | F | 2Y | SUB/S | 判读 |
|---|---|---:|---:|---:|---|---|
| `interest_expense_y1_change_3mo` | `RRA1nYQd` | 1.41 | 0.80 | 0.91 | 0.32 | 四闸不过 |
| `nav_estimate_year1_change_3mo` | `58jko905` | 1.08 | 0.53 | 0.75 | 0.33 | 弱 |
| `op_expense_estimate_y1_change_3mo` | `npA8MoMx` | 1.42 | 0.76 | 0.74 | 0.33 | 四闸不过 |
| `capex_estimate_y1_change_3mo` | `omogMvMv` | 0.95 | 0.51 | 0.71 | 0.47 ✓ | 弱 |
| **`netprofit_y1_estimate_change_3mo`** | **`QPY9LjLG`** | **1.49** | **0.81** | **1.68 ✓** | **0.68 ✓** | **仅 S+F 差一线** |
| `netprofit_q1_estimate_change_1mo` | `RRA1nYne` | 1.52 | 0.82 | 1.58 ✓ | 0.17 | SUB 崩 |
| **`revenue_y2_estimate_change_3mo`** | **`gJW9EKEl`** | **1.71** | **1.03** | **2.01** | **0.35 ✗** | **仅 SUB 差（0.60/0.74）** |
| `estimate_y1_change_3mo_ebit` | `YPxgGmqq` | 1.41 | 0.75 | 1.25 | 0.47 ✓ | 三闸不过 |

**★ 新发现：SUB/S 比率依赖预测期**。同为 3 月修正、同骨架：营收 **y1** 修正 SUB/S ≈ 0.50（`gJWoaJqv` 已交付），
营收 **y2** 修正 SUB/S ≈ 0.35（`gJW9EKEl` 1.71/0.60）——远期预测的修正对子宇宙更不稳健，
**y2 线不是 y1 的免检复制品**。同理净利润 y1（`QPY9LjLG` 0.68）过了 SUB，而净利润 q1/1mo（`RRA1nYne` 0.17）崩掉。

**三个近失候选**：`Grgep090`（2Y+SUB）、`QPY9LjLG`（S+F）、`gJW9EKEl`（SUB）。均已派修（批 16 = decay 20 扫、
批 17 = 增长加速机制族）。

### ⑭.16 批 16 结果：decay=20 复测近失 + 偏度/修正壳对比（2026-10-20）

multisim `3HDc7t6nP4pNb7s3975Ek6`（decay=20，其余同）：8/8 COMPLETE。

| 字段 × 壳 | alpha | S | F | 2Y | SUB/线 | 判读 |
|---|---|---:|---:|---:|---|---|
| netprofit_y1_skewness_alt × skew | `0mjM06Wk` | 1.78 | 1.02 | 1.53 | 0.76/0.77 | **两闸各差一线** |
| netprofit_y1_skewness_alt × growth | `78onEMVL` | 1.26 | 0.56 | 0.93 | 0.34/0.55 | 壳不适配 |
| **netprofit_y1_3mo × skew** | **`vROv360w`** | **1.54** | **0.86** | **1.67 ✓** | **0.93 ✓** | **仅 S/F，F 缺口大** |
| netprofit_y1_3mo × growth | `WjLV60kG` | 1.42 | 0.79 | 1.58 | 0.93 ✓ | 三闸 |
| **revenue_y2_3mo × skew** | **`2rjNbWEx`** | **1.78** | **1.11** | **2.01 ✓** | **0.75/0.77** | **仅 SUB 差 0.02** |
| revenue_q2_skewness × skew | `9qE7Lmgo` | 1.49 | 0.88 | 0.75 | 0.72 ✓ | 2Y 塌 |
| est_y1_skewness_profit × skew | `0mjM06np` | 1.49 | 0.82 | 1.11 | 0.88 ✓ | 2Y 塌 |
| netprofit_q2_skewness × skew | `mLYVM1eE` | 1.69 | 1.07 | 1.24 | 0.56/0.73 | 2Y+SUB |

**★ 结论**：
1. **skew 壳 + decay20 把 SUB 比率抬到 0.42–0.49**（revenue y2 由 growth 壳的 0.35 → skew 壳 0.42），
   **但 growth 壳的 SUB 比率只有 0.27–0.33**。同字段选壳对 SUB 的影响大于 decay。
2. decay20 换来 2Y 提升、S 略降：netprofit y1 3mo S 1.49→1.54、2Y 1.68→1.67；
   偏度 alt 2Y 1.42→1.53 但 SUB 0.79→0.76。**decay 不是免费杠杆，SUB 与 2Y 反向**。
3. 三个候选卡在两闸各差 0.01–0.05：`0mjM06Wk`（2Y −0.05 / SUB −0.01）、
   `2rjNbWEx`（SUB −0.02）、`vROv360w`（S −0.04 / F −0.14）。

### ⑭.17 批 17 结果：增长加速族（qoq/yoy/trailing）（2026-10-20）

multisim `3y8A6j5rb5iW9jX13n2sldu2`（decay=1 / RAM / growth 壳）：8/8 出结果，其中 5 条
`hump` 触发 UNITS（字段为 `TSShare`/`TSPrice` 计价格单位，仍 COMPLETE、指标有效）。

| 字段 | alpha | S | F | 2Y | SUB/线 | 判读 |
|---|---|---:|---:|---:|---|---|
| `eps_trailing_4q_estimate` | `2rjNblnZ` | **1.99** | **1.20** | 1.72 ✓ | 0.53/0.86 | SUB 比率 0.27，结构性死 |
| `est_q1_yoy_profit_growth` | `88vedl6X` | 1.67 | 1.13 | 1.58 | 0.66/0.72 | 2Y 边界 + SUB −0.06 |
| `est_q1_yoy_eps_growth` | `xA1d0jzb` | 1.78 | 1.21 | 1.27 | 0.66/0.77 | 2Y + SUB |
| `netprofit_q2_qoq_growth` | `88vedlrX` | 1.58 | 0.86 | 1.79 ✓ | 0.77 ✓ | 仅 F，但 prod 0.7044 已死 |
| `revenue_trailing_4q_estimate` | `N1eRv75w` | 1.45 | 0.81 | 0.65 | 0.26/0.63 | 死 |
| `revenue_q1_qoq_growth` | `omogMqvl` | 1.19 | 0.64 | 0.90 | 0.37/0.52 | 弱 |
| `ebitda_q1_qoq_growth` | `leM3bjzO` | 1.06 | 0.56 | 0.03 | 0.35/0.46 | 死 |
| `op_expense_q2_qoq_growth` | `qME6ojzP` | 0.93 | 0.42 | 0.23 | 0.41 ✓ | 死 |

**★ 结论**：增长加速族能出高 S 高 F（`2rjNblnZ` S1.99、`xA1d0jzb` S1.78），但 **SUB 比率只有 0.27–0.40**，
是「大盘股驱动」的典型形态；`2rjNblnZ` 甚至 2Y 1.72 也过，只败在 SUB。**水平类/增速类字段不破 SUB 墙**，
与「修正/惊喜类 SUB 比率 0.5+」形成清晰分界。

### ⑭.18 prod 实测：三个近失的相关性裁决（2026-10-20）

| alpha | 字段 | prod max | [0.7,0.8) n | 结论 |
|---|---|---:|---:|---|
| `QPY9LjLG` | netprofit_y1_3mo (growth) | 0.7332 | 14 | **判死**（族内已有 prod 重叠，且 >0.70） |
| `88vedlrX` | netprofit_q2_qoq (growth) | 0.7044 | 1 | **判死**（只差 0.0044 但族桶已非 0） |
| **`Grgep090`** | netprofit_y1_skewness_alt (skew) | **0.6937** | 11 | **prod 过关**（self 0.6937，与 `akVnvzX5` 同源风险） |

⇒ 只剩偏度 alt 这一条在 prod 上可用，但它的 self 0.6937 已贴线，**任何增强都可能同时踩 self 与 prod**。

### ⑭.19 批 18 结果：惊喜 z-score / 修正幅度族（decay=1）（2026-10-20）

multisim `5NOUbghA4nYaqEkvtCpxtm`（8/8 COMPLETE）：

| 字段 × 壳 | alpha | S | F | 2Y | SUB/线 | 判读 |
|---|---|---:|---:|---:|---|---|
| `estimate_surprise_difference_nprofit` × growth | `E5VeJWmK` | **1.79** | **1.16** | 1.60 ✓ | 0.98 ✓ | **RA 全过（prod 0.7842 死）** |
| `interest_expense_revision_magnitude` × skew | `KPmEadvl` | 1.67 | 1.01 | 1.01 | 0.57/0.72 | 2Y+SUB |
| `eps_estimate_zscore` × skew | `d5KRLVWx` | 1.57 | 0.92 | 1.42 | **−0.04**/0.68 | SUB 为负，z-score 型不适合 |
| `revenue_estimate_zscore` × skew | `GrgeJAmJ` | 1.52 | 0.98 | 1.12 | 0.53/0.66 | 4 闸 |
| `netprofit_estimate_zscore` × skew | `A1Q7KZxg` | 1.48 | 0.90 | 0.92 | 0.56/0.64 | 4 闸 |
| `eps_estimate_zscore` × growth | `6XAeOVMJ` | 1.24 | 0.62 | 1.21 | 0.17/0.54 | 死 |
| `netprofit_estimate_zscore` × growth | `pwvKOrWX` | 1.46 | 0.82 | 1.38 | 0.68 ✓ | S/F/2Y |
| `nav_estimate_revision_magnitude` × skew | `E5VeJWmm` | 1.30 | 0.70 | 1.48 | 0.51/0.56 | 死 |

**★ 结论**：**惊喜差值（actual − consensus）是本数据集唯一能自然过 SUB 的新机制**
（`E5VeJWmK` SUB/S = 0.55），但它正是平台最拥挤的一族（prod 直方图 [0.7,0.8) n=880）。
z-score 化后的 surprise（`*_estimate_zscore`）SUB 反而塌到 0 附近 —— **季度事件的 z-score 在子宇宙不稳定**。

### ⑭.20 批 19 结果：decay=30 对 SUB 的翻转型影响（2026-10-20）

multisim `VACpogeR4HLa5X126vdRLWO`（skew 壳，decay=30，8/8 COMPLETE）：

| 字段 | alpha | S | F | 2Y | SUB/线 | 判读 |
|---|---|---:|---:|---:|---|---|
| **`eps_trailing_4q_estimate`** | **`3qjeLYWO`** | **2.10** | **1.36** | **2.19 ✓** | **1.12 ✓** | **RA 全过（prod 0.7174 死）** |
| **`revenue_y2_estimate_change_3mo`** | **`e76xR8oE`** | **1.79** | **1.12** | **1.87 ✓** | **0.84 ✓** | **RA 全过（prod 0.7789 死）** |
| `eps_y1_estimate_change_3mo` | `1YjzEVEz` | 1.77 | 1.06 | 1.50 | 0.82 ✓ | 仅 2Y −0.08 |
| `est_revision_magnitude_profit` | `leM3X6xx` | 1.73 | 1.03 | 1.91 ✓ | 0.66/0.75 | 仅 SUB −0.09 |
| `netprofit_y1_estimate_skewness_alt` | `E5VeJ0Xr` | 1.75 | 1.00 | 1.73 ✓ | 0.68/0.76 | 仅 SUB −0.08 |
| `netprofit_y1_estimate_change_3mo` | `qME6qkqZ` | 1.58 | 0.89 | 1.56 | 0.94 ✓ | 仅 F/2Y 一线 |
| `est_q1_yoy_profit_growth` | `kqJZlklz` | 1.57 | 1.05 | 1.11 | 0.57/0.68 | S/SUB/2Y |
| `est_q1_yoy_eps_growth` | `9qE70PQr` | 1.56 | 1.05 | 1.33 | 0.69 ✓ | S/2Y |

**★★ 关键机制发现（可复用）：decay 不是单调杠杆，对 SUB 是「翻转型」的**。
同一表达式 `eps_trailing_4q_estimate`：growth 壳 decay1 SUB 0.53（死）→ skew 壳 decay30 SUB **1.12**（过）。
同字段 `revenue_y2_3mo`：growth decay1 SUB/S 0.35 → skew decay20 0.42 → skew decay30 **0.47**。
**衰减拉长把这个「水平/增速」类信号从「大盘驱动」变成「子宇宙稳健」——因为 decay 抑制了高换手的大票进出。**
反例：`netprofit_y1_skewness_alt` 的 SUB 随 decay 单调下降（0.79→0.76→0.68）——偏度类字段不喜欢长衰减。
**判据：增速/水平类 → decay 30；偏度/修正类 → decay 1–20。**

### ⑭.21 prod 终裁：三条 RA 全过全部撞墙（2026-10-20）

| alpha | 字段 | prod max | [0.7,0.8) n | 结论 |
|---|---|---:|---:|---|
| `E5VeJWmK` | estimate_surprise_difference_nprofit | 0.7842 | 880 | 死（惊喜族最拥挤） |
| `e76xR8oE` | revenue_y2_3mo (skew/decay30) | 0.7789 | 223 | 死（营收修正族已被我方 2 颗 + 平台覆盖） |
| `3qjeLYWO` | eps_trailing_4q (skew/decay30) | 0.7174 | 24 | **唯一可尝试破线**（0.70–0.75 区间） |

⇒ **本数据集当前瓶颈已从「指标闸」转为「prod 相关性墙」**。已交付 4 颗 prod 分布 0.649–0.6978，
留给后续候选的余量极薄；下一步必须换**持仓结构**（final group / 壳形态），而不是磨算子或参数。

### ⑭.22 批 20：final group 是收益杠杆，不是 prod 杠杆（2026-10-20）

multisim `JbTyb8844lvc9oQlfeUC2g`（skew 壳，decay=30，8/8 COMPLETE）。同一表达式只把最后一层
`group_rank(..., subindustry)` 换成 `market` / `industry`：

| 字段 | alpha | final group | S | F | 2Y | SUB | TO | ret | prod（[0.7,0.8) n） |
|---|---|---|---|---:|---:|---:|---:|---:|---|
| `eps_trailing_4q_estimate` | `leM3Xa98` | market | 2.11 | 1.49 | 1.98 ✓ | 1.14 ✓ | 4.19% | 6.20% | **0.7168 ✗（7）** |
| `eps_trailing_4q_estimate` | `RRA1Weva` | industry | 2.03 | 1.36 | 2.10 ✓ | 1.02 ✓ | 4.06% | 5.58% | **0.7418 ✗（23）** |
| `revenue_y2_estimate_change_3mo` | `A1Q7KxmX` | market | 2.04 | 1.48 | 1.97 ✓ | 1.11 ✓ | 3.95% | 6.55% | **0.783 ✗（440）** |
| `revenue_y2_estimate_change_3mo` | `gJW9pa0Q` | industry | 1.97 | 1.38 | 1.84 ✓ | 1.02 ✓ | 3.81% | 6.10% | **0.7859 ✗（492）** |
| `eps_y1_estimate_change_3mo` | `E5VeJQx0` | market | 1.90 | 1.25 | 1.49 | — | — | — | 仅 2Y −0.09 |
| `est_revision_magnitude_profit` | `ZYmKGaNn` | market | 1.91 | 1.28 | 2.16 ✓ | 0.71/0.83 | — | — | 仅 SUB −0.12 |
| `interest_expense_revision_magnitude` | `bl8dEaKl` | market | 1.66 | 1.09 | 1.11 | 0.53 | — | — | 四闸不过 |
| `netprofit_y1_estimate_skewness_alt` | `e76xRaEN` | market | 1.55 | 0.89 | 1.52 | 0.60 | — | — | 四闸不过 |

**★★ 关键结论 1：final group 是「收益/F」杠杆，不是「prod」杠杆。**
同一字段换 `subindustry → market/industry`：returns 从 ~4.9% 抬到 5.6–6.6%，S 从 1.79–2.10 抬到 1.97–2.11，
F 从 1.12–1.36 抬到 1.36–1.49，SUB 保持 ≥1.02。**原因：排序分母从子行业换成全市场，头部组合集中到
「全市场最极端」的修正，单票信息更强、覆盖更宽，故 returns 与 sharpe 同步抬升。**
但它**不动 prod**：eps_trailing_4q 仍是 0.717/0.742，revenue_y2_3mo 仍是 0.783/0.786。
⇒ **prod 相关性由「信号内容」决定，与持仓分组无关；想破 prod 只能换字段/机制，不能靠分组或壳微调。**

**★★ 关键结论 2：本数据集 revision/skew 复合体已判死（族级）。**
三条主族 prod 直方图 [0.7,0.8) 全部 n≥1：eps_trailing_4q（n=7~24）、revenue_y2_3mo（n=223~492）、
surprise（n=880）。平台侧同族覆盖已密。**在 analyst_factor_signals 上继续磨修正/偏度族不会有新的可提交产出。**

**交付现状**：本数据集已交付 **2 颗**（`omoK1A5m` / `akVnvzX5`，prod 0.649 / 0.659）。
另 2 颗 `gJWoaJqv` / `kqJLawqP` 使用 `anl44_2_*` 字段（数据集 **analyst44**，tag `SRC_ANALYST44`），不属本数据集——2026-10-20 更正此前「本数据集已交付 4 颗」的误记。
**换数据集判据已触发**（用户约束：仅在确实无计可施时更换，并说明原因）：
指标侧本数据集仍有大量可过闸字段，但**可提交性被 prod 族级墙锁死**——瓶颈不在模板/算子/参数，继续留在此集会重复撞同一堵墙。

---

## ⑮ 2026-10-22 换集回打：不确定性族 × 趋势斜率族（批 29 / 批 30）

### ⑮.1 为什么回到本集

`fundamental1` 已判数据集级 `dead_end`（20 臂最强 |S| 0.94，见
[`_usa-fnd1-field-profile-20261022.md`](_usa-fnd1-field-profile-20261022.md) §8）。换集依据两条：
① USA Fundamental 类别级扫描（[`_usa-fundamental-dataset-scan-20261019.md`](_usa-fundamental-dataset-scan-20261019.md) §6）
实证该类别在 USA/TOP3000 **无法产出 ATOM**（32 条最高 S 1.43 且 SUB 挂）；② 已交付 5 颗全部来自 analyst 族。
新波次只打**未交付过的机制族**，不与已交付的增长率（`omoK1A5m`）/偏度（`akVnvzX5`）/背离（`gJWoaJqv`、`kqJLawqP`）/动量（`e76xgXkM`）重叠。

### ⑮.2 论坛取证（2026-10-22，检索「分析师 修正 离散度 不确定性 预测分歧」，50 条命中）

| 帖 | 日期 / 票评 | 可复用结论 |
|---|---|---|
| 【Alpha灵感】分析师预测分歧度——从一致预期的收敛中寻找 Alpha | 2025-10-15 / 14 票 6 评 | ★ **关键不是分歧水平，是分歧的变化方向**：下降 = 预期收敛 = 风险消化 / 信息落地；上升 = 市场意见分化 |
| 分析师数据的正确打开方式: 预期差与修正 | 2026-08-19 / **30 票** 2 评 | ★ **分歧越大 → 不确定性越高 → 未来回报越差；低分歧（强共识）有正溢价**；并提醒「数据更新频率低（季度为主）」；另指出收入比 EPS 更干净（不易被一次性项目/税率/回购操纵） |
| 【Alpha Idea】分析师修正当成节奏，而不是评分 | 2026-09-30 | 用 `ts_product(window)` 判「最近几天是不是一直在往同一个方向改」= 修正**连击/节奏**，与幅度（magnitude）是不同机制 |
| 【Alpha Idea】从"分析师上调"到"组内归一"（DEU 记录） | 2026-09-07 / 1 票 | 同行归一优于全市场排序 —— 本集现有壳 `group_rank(..., subindustry)` 已内含 |
| 我以为 analyst15 只是普通预期数据 | 2026-05-14 / 27 票 4 评 | 上修需被**其他维度确认**；「预测分歧度是否在放大」是独立观察轴 |

⇒ 拆成三条可执行机制：① 不确定性**水平**做空（批 29 R5–R8）；② 不确定性**变化方向**做空上升（批 31，预登记见 ⑮.5）；③ 修正**连击**（`ts_product`）而非幅度（后续波次）。

### ⑮.3 批次 29：不确定性 / 修正强度 / 实现值（multisim `2HsrKY4v04Tu9gMxqHfMuvK`）

壳沿用已交付冠军 `omoK1A5m` 的完整配方（`quantile(group_rank(hump(ts_backfill(winsorize(T, std=4), 756), hump=0.01), subindustry))`，
RAM decay 1）；`T` ∈ {`ts_av_diff(F,252)`, `ts_zscore(F,504)`}。

| 臂 | 机制 | 字段 | cov | aC | 方向 |
|---|---|---|---:|---:|---|
| R1/R2 | 修正强度（EPS） | `est_revision_magnitude_eps` | 0.9378 | 6 | − |
| R3/R4 | 修正强度（净利） | `netprofit_revision_magnitude` | 0.9452 | 9 | − |
| R5/R6 | 意外波动率 | `eps_surprise_stddev` | 0.9098 | 1 | − |
| R7/R8 | 估计变异系数 | `netprofit_y1_estimate_volatility_adj_1yr` | 0.8954 | **0** | − |
| R9/R10 | 实现值增速（对照） | `eps_actual_q1_qoq_growth` | 0.9131 | **0** | + |

**预登记判据**：任一臂 IS 全闸（S≥1.58 / F≥1.0 / 2Y≥1.58 / SUB 按 0.43×S / TO 0.01–0.70）→ 立即 `submit_verdict` + `check_correlation(refresh=True)`；
若 10 臂全无 S ≥ 1.20 ⇒ 不确定性族判不可达。

### ⑮.4 批次 30：预期趋势斜率（multisim `3LvQeC3xF4m2b1FboBTykdO`）

机制：**一致预期时间序列的拟合斜率**（趋势持续性），与已交付的「单期环比增速」不同 —— 后者问"这一期比上期快多少"，
前者问"过去一年/两年的趋势线是否在抬升"。同壳同设置，方向 +。

| 臂 | 字段 | cov | aC |
|---|---|---:|---:|
| S1/S2 | `eps_estimate_trend_slope_1yr` | 0.9302 | 0 |
| S3/S4 | `revenue_estimate_trend_slope_1yr` | 0.9090 | 3 |
| S5/S6 | `netprofit_estimate_trend_slope_1yr` | 0.9178 | 0 |
| S7/S8 | `eps_estimate_trend_slope_2yr` | 0.8780 | 0 |
| S9/S10 | `estimate_trend_slope_1yr_pprofit` | 0.8875 | 0 |

**已知风险（预登记）**：本族与已交付 #1（`eps_q1_estimate_qoq_growth`）同属"预期向好"方向，
prod 相关可能 ≥0.70。**处置按 D0-P**：prod 0.60–0.70 不再出变体；0.70–0.75 只做一次结构性尝试；≥0.75 判 `dead_end`。
若 IS 未过闸则不进 prod 测量（省配额）。

**收批（8 有效 + 2 UNITS ERROR）**：`ZYmQNv0j` / `akVKG9L5` 触发
`Incompatible unit for input of "hump"`（`ts_av_diff` 保留字段单位 `TSShare`/`TSPrice`，`hump` 要求无量纲）——
与本集批 17 同形态，**结论不变：单位带量字段只能用 `ts_zscore` / `ts_rank`，不能用 `ts_av_diff` 进 `hump`**。

| 臂 | 字段 / 变换 | alpha | S | F | 2Y | SUB / 线 | TO |
|---|---|---|---:|---:|---:|---|---:|
| S1 | eps_1yr / av_diff | `GrgW95l5` | 1.55 | 0.79 | 0.42 | 0.55/0.67 | 3.91% |
| S2 | eps_1yr / z504 | `RRAEPwV0` | 1.75 | 0.97 | **1.97 ✓** | 0.23/0.76 | 3.68% |
| S3 | revenue_1yr / z504 | `N1eN8lQL` | 1.35 | 0.70 | 1.37 | 0.57/0.58 | 4.03% |
| S4 | netprofit_1yr / z504 | `QPYv6pb5` | **1.84** | **1.07** | 1.30 | 0.36/0.80 | 3.94% |
| S5 | eps_2yr / av_diff | `rKdR8MOd` | 1.76 | **1.21** | 1.21 | 0.66/0.76 | 4.49% |
| S6 | eps_2yr / z504 | `leMA1PKe` | 1.51 | 0.96 | 1.16 | 0.51/0.65 | 4.52% |
| S7 | pprofit_1yr / av_diff | `78oLlR6Q` | 1.78 | **1.02** | 1.08 | 0.41/0.77 | 4.36% |
| S8 | pprofit_1yr / z504 | `6XAdNLKJ` | **1.83** | **1.10** | 1.10 | **0.78/0.79** | 4.29% |

**★ 归因（不是盲扫，先归因再推进）**：
1. **SUB 是 trend_slope 族的唯一共性墙**：8/8 全挂 SUB，`SUB/S` 比率 0.14–0.43，
   而闸线恰为 0.43×S ⇒ **收益系统性来自 non-sub-universe 的小盘段**（大盘段几乎不赚钱）。
2. S/F 双过而只挂 SUB/2Y 的有 3 条（S4 / S5 / S8），其中 `6XAdNLKJ` **SUB 只差 0.01**。
3. **2Y 与 SUB 反向**：2Y 最高的是 `RRAEPwV0`（1.97）但 SUB 只有 0.23；S8 的 SUB 最高（0.78）但 2Y 只有 1.10。
   ⇒ 同一族内「近两年强」与「子宇宙稳健」互斥，磨窗口不会同时解决，**必须换壳**。
4. 与批 29 的「不确定性族 → 正收益」并列：本族方向（趋势斜率向上）**不需要反号**，S 全正。

### ⑮.5 批次 31 的设计变更（原预登记顺延为批 32）

**变更原因（两处，都是本集既有实证，不是新猜测）**：

① **我用了错误的 decay 档**。批 29/30 全部按 `omoK1A5m` 的 decay=1 发，但
`$WQ_PY -m wqb.profiles explain --region USA --dataset analyst_factor_signals` 显示本组合登记的覆盖值是
**`decay=20`，证据写明「d15/d20 修 SUB（0.67→0.74/0.82）」**。SUB 墙的根因之一是设置档偏离登记值。
② **本集唯一 RA 全过的壳不是批 29/30 用的那条**。`leM3Xa98` / `3qjeLYWO`（`eps_trailing_4q_estimate`，
decay=30）实测 **S 2.11/F 1.49/2Y 1.98/SUB 1.14** 与 **S 2.10/F 1.36/2Y 2.19/SUB 1.12**，RA **全过**，
其壳为 `quantile(group_rank(hump(ts_backfill(winsorize(group_neutralize(ts_zscore(F, 315), industry), std=4), 252), hump=0.01), market|subindustry))`
——比批 29/30 的壳多一层 `group_neutralize(..., industry)`、窗口 315/252（非 504/756）、final group 可换 market。
批 20 已证 `final group` 是**收益/F/SUB 杠杆**（换 market 后 SUB 保持 ≥1.02），不是 prod 杠杆。

⇒ 批 31 拆两批并行，各自只答一个问题：

| 批 | multisim | 设置 | 壳 | 答什么问题 |
|---|---|---|---|---|
| **31a** | `424alLb4p5adallIdkJ7PNX` | decay **20**（登记值）/ RAM / trunc 0.08 | 批 29 壳（504/756，无 group_neutralize） | 登记 decay 能否把批 29 的 SUB 0.60–0.71 抬过线；同时给 4 条正向臂拿到**可提交的 alpha id** |
| **31b** | `1yMqnYbRh5jGbXC1fW3dc0PT` | decay **30** / RAM / trunc 0.08 | **RA 全过壳**（315 + group_neutralize(industry) + 252 + final market/subindustry） | RA 全过壳能否移植到 trend_slope（全 aC=0）上，并顺带解决 2Y/SUB 反向 |

**31a 十臂**：4 条已知强正向臂 × {subindustry, industry} final group + 2 条新字段
（`est_revision_magnitude_profit`、`nav_estimate_revision_magnitude`）——批 20 已证 industry 组抬 SUB。
**31b 十臂**：5 条 trend_slope × {market, subindustry}。

**预登记判据（两批共用）**：任一臂 RA 全闸 → 立即 `submit_verdict` + `check_correlation(refresh=True)`；
prod 按 D0-P 处置。**31b 的新字段全是 aC=0**，若能过闸则 prod 大概率干净——这是当前最可能出交付的一批。

#### ⑮.5.1 批 31a 收批（decay 20，10/10 COMPLETE）

壳同批 29（504/756，无 `group_neutralize`），只动 decay 与 final group。

| 字段 × 变换 | final group | alpha | S | F | 2Y | SUB/线 | TO | 判读 |
|---|---|---|---:|---:|---:|---|---:|---|
| `eps_surprise_stddev` z504 | subindustry | `78oL2qzQ` | 1.82 | **1.23** | 1.53 | 0.73/0.79 | 4.47% | SUB −0.06、2Y −0.05 |
| `eps_surprise_stddev` z504 | **industry** | **`kqJNYkjd`** | 1.75 | **1.22** | **1.82 ✓** | **0.79 ✓** | 4.47% | **RA 全过** |
| `netprofit_y1_est_volatility_adj_1yr` z504 | subindustry | `LL5M2bG1` | 1.79 | 1.06 | **1.81 ✓** | 0.60/0.78 | 3.86% | **仅 SUB**（−0.18） |
| `netprofit_y1_est_volatility_adj_1yr` z504 | industry | `akVKg272` | 1.81 | 1.14 | 1.52 | 0.59/0.78 | 3.86% | SUB + 2Y |
| `eps_actual_q1_qoq_growth` av_diff | subindustry | `QPYvorGK` | 1.60 | 0.92 | 1.58 | **0.78 ✓** | 4.09% | F −0.08、2Y 贴线 |
| `eps_actual_q1_qoq_growth` av_diff | **industry** | **`E5V620lK`** | **1.80** | **1.15** | **1.77 ✓** | **0.86 ✓** | 4.09% | **RA 全过** |
| `netprofit_revision_magnitude` z504 | subindustry | `0mjYakM2` | 1.65 | 0.95 | **1.63 ✓** | 0.66/0.71 | — | F + SUB |
| `netprofit_revision_magnitude` z504 | industry | `gJWe0q8g` | 1.58 | 0.94 | **1.67 ✓** | **0.54**/0.68 | — | SUB 反降 0.12 |
| `est_revision_magnitude_profit` z504 | subindustry | `1YjN2VwX` | 1.77 | 1.07 | **2.09 ✓** | 0.41/0.77 | 3.56% | 仅 SUB（−0.36） |
| `nav_estimate_revision_magnitude` z504 | subindustry | `vRO1onjA` | 1.50 | 0.89 | 1.78 | 0.51/0.65 | 3.58% | 三闸 |

**★ 归因**：

1. **decay 20 确能抬 SUB**（登记值是对的）：`eps_actual_q1_qoq_growth` av_diff 的 SUB
   由批 29（decay 1）的 0.60–0.71 区间抬到 **0.78 并过线**；`eps_surprise_stddev` 也到 0.73/0.79。
   同一字段同壳，只换 decay，SUB 抬 0.1 量级 ⇒ **对「水平/增速类」字段，decay 20 是登记值不是保守档**。
2. **final group 的增益方向是字段族特定的，不是单向杠杆**（修正批 20 的一般化）：
   - **意外/实现类 → industry 全面更好**：`eps_surprise_stddev` SUB 0.73→0.79（过线）、2Y 1.53→1.82（过线）；
     `eps_actual_q1_qoq_growth` S 1.60→1.80、F 0.92→1.15、2Y 1.58→1.77、SUB 0.78→0.86 **四项同升**。
   - **修正幅度类 → industry 是负贡献**：`netprofit_revision_magnitude` SUB 0.66→**0.54**、S 1.65→1.58。
   - **估计波动率类 → 持平但伤 2Y**：SUB 0.60→0.59、F 1.06→1.14、2Y **1.81→1.52**。
   ⇒ 机制解释：**修正幅度必须与同子行业可比**（子行业内的修正才有信息量，换宽基准把噪声引进来）；
   而**意外/实现值的水平**在子行业样本里中位数不稳（每子行业股票少），换行业基准才抬得起统计功效。
   判据：**先看字段是「相对同侪的偏离」还是「自身水平的波动」** —— 前者用 subindustry，后者用 industry。
3. **两条 RA 全过臂都不是修正幅度族**，而是批 29 已验证的「不确定性水平 + 实现值增速」——与批 29 强项同源。
4. `est_revision_magnitude_profit` 2Y 2.09 很漂亮但 SUB 0.41（差 0.36）⇒ **修正幅度族在 USA 的 SUB 墙
   是结构性的（连续 3 批 5 条全灭）**，与批 20「修正/偏度族 prod 已死」叠加，本族双杀结案。

**prod 裁决（2026-10-22，MCP `check_correlation` 超时 → 改 `brain_client` 带外跑）**：

| alpha | 核心字段 | prod | 裁决 |
|---|---|---:|---|
| `kqJNYkjd` | `eps_surprise_stddev` z504 | **0.8591** | **D0-P dead_end**（≥0.75，零变体） |
| `E5V620lK` | `eps_actual_q1_qoq_growth` av_diff | 见 §⑮.7 | — |

⚠ **`eps_surprise_stddev` 是本集里被用得最多的字段之一**（批 29 六条臂都在它上面），
prod 0.86 说明「惊喜离散度的水平量」已被生产池充分覆盖 —— 与批 20「修正幅度族 prod 已死」同型。
**本集低 prod 的白空间只剩 aC=0 的冷字段**（forward 估计 / qoq 实现值等多半 aC=0），
这是后面所有选字段的第一判据。

#### ⑮.5.2 批 31b 收批（RA 全过壳 × trend_slope，10/10 COMPLETE）

壳 = `quantile(group_rank(hump(ts_backfill(winsorize(group_neutralize(ts_zscore(F,315), industry), std=4), 252), hump=0.01), G))`，
decay 30。`G ∈ {market, subindustry}`。

| 字段 | G | alpha | S | F | 2Y | SUB/线 | 判读 |
|---|---|---|---:|---:|---:|---|---|
| `eps_estimate_trend_slope_1yr` | market | `1YjN2LJJ` | 1.56 | 0.91 | 1.46 | **0.22** | 四闸 |
| `revenue_estimate_trend_slope_1yr` | market | `RRAEvYdb` | 1.31 | 0.74 | 1.30 | 0.73 ✓ | S/F/2Y |
| `netprofit_estimate_trend_slope_1yr` | market | `1YjN2LJW` | 1.68 | 1.03 | 1.09 | 0.53 | SUB+2Y |
| `eps_estimate_trend_slope_2yr` | market | `88vR2rnX` | 1.62 | 1.16 | 1.43 | 0.50 | SUB+2Y |
| `estimate_trend_slope_1yr_pprofit` | market | `WjLOxd9Z` | 1.78 | 1.16 | 1.30 | **0.83 ✓** | **仅 2Y**（−0.28） |
| `eps_estimate_trend_slope_1yr` | subind | `JjPe2mdj` | 1.78 | 1.01 | **1.90 ✓** | 0.41 | **仅 SUB**（−0.36） |
| `revenue_estimate_trend_slope_1yr` | subind | `N1eN26Ow` | 1.32 | 0.69 | 1.32 | 0.64 ✓ | S/F/2Y |
| `netprofit_estimate_trend_slope_1yr` | subind | `pwvdpE7g` | 1.79 | 1.03 | 1.02 | 0.52 | SUB+2Y |
| `eps_estimate_trend_slope_2yr` | subind | `bl86KM9M` | 1.52 | 0.99 | 1.36 | 0.62 | 四闸 |
| `estimate_trend_slope_1yr_pprofit` | subind | `A1QV2b3w` | 1.80 | 1.09 | 1.03 | **0.85 ✓** | **仅 2Y**（−0.55） |

**★ 归因**：

1. **RA 全过壳移植失败**：同样 5 个字段，批 30 用批 29 壳最好 SUB 0.36 / 2Y 1.97；本批换 RA 全过壳后
   最好 SUB 0.85 / 2Y 1.03。**2Y 与 SUB 仍严格反向**（同一字段两个 G：pprofit market 2Y1.30/SUB0.83 vs
   subind 2Y1.03/SUB0.85；eps 1yr market 2Y1.46/SUB0.22 vs subind 2Y1.90/SUB0.41）。
2. `market` 组把 SUB 压到 0.22–0.83、`subindustry` 组把 2Y 压到 1.02–1.90 ⇒ **两种分组各守一门、互为代价**，
   与批 20「market 靠大盘段抬收益」一致，但这次在大盘段付出的正是 SUB。
3. **trend_slope 族判弱结案**（不判死）：3 批 20 条，S 稳定 1.3–1.8、F 到 1.21，但**没有一条同时过 2Y 与 SUB**。
   机制上「预期趋势斜率」是慢变量，收益集中在子宇宙外 —— 与 `fundamental2`/`workforce` 同型，不再投入。

### ⑮.6 批次 32（原 ⑮.5 预登记，顺延）

**机制**：不确定性**变化方向** —— 论坛 14 票帖与 30 票帖共同指向的核心。
`A = ts_delta(<dispersion>, 63)`：做空不确定性上升（`-quantile(group_rank(A))`），做多收敛。
字段候选：`eps_surprise_stddev` / `netprofit_surprise_stddev`、`estimate_surprise_stddev_ebit`。
**先验预期**：与批 29 的水平量臂部分相关（同一字段的差分量），但与已交付 5 颗正交。
⚠ **注意批 29 的水平量方向是正的**（6/6 反号），论坛 30 票帖的「分歧大→回报差」在本区不成立；
故本批差分方向须按批 29 实测取**正向**（不确定性上升 → 回报上升），不再是「做空上升」。

### ⑮.7 批次 33 收批：预测视界差（horizon gap）× 4 字段式（8/8 COMPLETE）

multisim `2Za1MD5N34EK9wFCZSIHhRw`，USA/TOP3000/D1/decay 20/RAM/trunc 0.08，批 29 壳。

**★ 先做字段盘点，本集 forward 估计只有 5 个字段**（catalog 实测）：
`forward_year1_estimate_gpm`（cov 0.696）、`forward_year1_estimate_nprofit`（0.9129）、
`forward_year1_estimate_pprofit`（0.9177）、`forward_year2_estimate_nprofit`（0.9369）、
`forward_year2_estimate_pprofit`（0.9431）。**没有 eps / revenue 的 forward 对**，
gpm 只有 year1 ⇒ 视界差只能做 nprofit / pprofit 两科，8 臂即为全集。

| 变换 | 字段 | G | alpha | S | F | 2Y | SUB/线 | 判读 |
|---|---|---|---|---:|---:|---:|---|---|
| `(FY2−FY1)/abs(FY1)` | nprofit | **industry** | **`GrgWNrw3`** | **1.81** | **1.33** | **2.34 ✓** | **0.70/0.78** | **仅 SUB（−0.08）** |
| 同上 | nprofit | subind | `E5V6M5wR` | 1.78 | 1.21 | **2.45 ✓** | 0.65/0.77 | 仅 SUB（−0.12） |
| 同上 | pprofit | industry | `9qEx3qwd` | 1.64 | 1.17 | **1.98 ✓** | 0.51/0.71 | 仅 SUB（−0.20） |
| 同上 | pprofit | subind | `88vRZ8zW` | 1.56 | 1.02 | **1.82 ✓** | 0.48 | **S+SUB**（S −0.02） |
| `ts_av_diff(FY2,252)/ts_mean(abs(FY2),252)` | nprofit | industry | `e765P70p` | 1.57 | 0.87 | 1.53 | **0.10** | 四闸 |
| 同上 | nprofit | subind | `leMAYelx` | 1.55 | 0.80 | 1.30 | **0.07** | 四闸 |
| 同上 | pprofit | industry | `2rjAxrLJ` | 1.60 | 0.87 | 1.04 | **0.75 ✓** | F+2Y |
| 同上 | pprofit | subind | `78oLr811` | 1.48 | 0.73 | 1.16 | 0.64 ✓ | S+F+2Y |

\* `88vRZ8zW` 平台 checks 为 F 1.02 过闸（metrics 读数 1.02，上表按失败项判定）。

**★ 归因（三条，全部指向下一步）**：

1. **「视界差」是水平比值，不是时间差分**：`(FY2−FY1)/abs(FY1)` 形态 S 1.64–1.81 / F 1.17–1.33 /
   2Y 1.98–2.45，是本战役 **F 最高的一族**；换 `ts_av_diff(FY2,252)` 后 S 掉到 1.48–1.60、SUB 塌到 0.07–0.10。
   机制：视界差的信息在**两个预测水平之比**里，做时间差分反而把「FY1 锚」丢掉、只剩 FY2 自身的漂移。
2. **final group 方向与批 31a 一致（industry 更好）**：两科四臂里 industry 在 S/F/2Y/SUB 上全面不差于
   subindustry（nprofit 1.81/1.33/2.34/0.70 vs 1.78/1.21/2.45/0.65）。与 §⑮.5.1 的判据吻合 ——
   视界差是**自身水平的比值**（不是相对同侪的偏离），走 industry。
3. **唯一墙是 SUB（−0.08），且不是字段问题而是结构问题**：S 1.81 / F 1.33 / 2Y 2.34 三条余量都很大，
   只 SUB 差 0.08。而同一壳在批 31a 用 industry 拿到过 SUB 0.79 / 0.86 ⇒ **壳有能力过 SUB，
   本族的小盘段偏弱**，可用 S4 Mode A 的壳层杠杆单独修（见 §⑮.8）。

⚠ **`batch_get_alpha_metrics` 对本批 8 条全返 null（status UNSUBMITTED / failed_ra_count 0）**，
而 `get_alpha_details` 逐条都有完整 metrics ⇒ **收批一律用 `get_alpha_details`**，
`batch_get_alpha_metrics` 在「仿真刚完成、alpha 尚未被平台索引」的窗口内不可信（2026-10-22 实测）。

### ⑮.8 批次 34：`GrgWNrw3` 的 SUB 修复（S4 Mode A，已收批 8/8，命中 1）

**归因先行**：`GrgWNrw3` 三条闸余量 S +0.23 / F +0.33 / 2Y +0.76，**只 SUB 差 0.08**。
所以本批**冻结核心想法**（`(FY2n−FY1n)/abs(FY1n)` + 批 29 壳 + industry），只动壳层/设置，
每臂对准一个**具名 SUB 机制假设**，不做参数笛卡尔积。

| 批 | multisim | 设置 | 臂 | 假设 |
|---|---|---|---|---|
| **34a** | `1LgL9FfIU4xRagYQczAqacF` | decay 20 / RAM / trunc 0.08 | backfill **252** / **504** | 小盘股的陈旧估计被 756 天的回填锚死 → 缩短回填让小盘用上新鲜值 |
| 同上 | 同上 | 同上 | winsorize **std=3** / **std=6** | SUB 由少数小盘极值仓拖累 → 收/放尾部截断 |
| 同上 | 同上 | 同上 | hump **0.005** / **0.02** | 平滑度过高会抹掉小盘信号 → 调 hump 甜区 |
| **34b** | `1BoKPAcF54WuaVpKSpkBc6t` | **decay 30** / RAM / trunc 0.08 | industry / subindustry | 登记证据 `d15/d20 修 SUB`，skew 壳用 d30 拿到过 SUB 1.14 ⇒ 测 d30 是否再抬一档 |

**预登记判据**：任一臂 SUB 过线且 S/F/2Y 仍全过 → 立即 `submit_verdict` + prod 实测（带外脚本，见 §⑮.7 注）
→ D0-P 裁决。**字段是 aC=0 的 forward 估计 ⇒ prod 先验干净，这是当前最可能出交付的一批。**
若 8 臂全部仍卡 SUB ⇒ 判「本族 SUB 是结构性墙」，按 D0-P 记 dead_end，不再扩变体。

#### 收批结果（baseline = `GrgWNrw3`：decay 20 / bf 756 / std=4 / hump 0.01 / industry，S 1.81 F 1.33 2Y 2.34 SUB 0.70/0.78）

| alpha | 单一改动 | S | F | 2Y | SUB/线 | 判读 |
|---|---|---:|---:|---:|---|---|
| `3qjoOE1P` | backfill **252** | 1.81 | 1.32 | 2.33 | 0.71/0.78 | 差 0.07 |
| `MP0YnbeM` | backfill **504** | 1.80 | 1.31 | 2.32 | 0.69/0.78 | 差 0.09 |
| `akVK8NQW` | winsorize **std=3** | 1.80 | 1.32 | 2.34 | 0.68/0.78 | 差 0.10 |
| `O0JAjnMJ` | winsorize **std=6** | 1.83 | 1.34 | 2.36 | 0.71/0.79 | 差 0.08 |
| `omoEXnJJ` | hump **0.005** | 1.81 | 1.34 | 2.35 | 0.68/0.78 | 差 0.10 |
| **`QPYvAnNw`** | **hump 0.02** | **1.83** | **1.31** | **2.12** | **0.80/0.78 ✓** | **RA 全过**（checks.fail=[]） |
| `1YjNRJ5Q` | decay **30** / industry | 1.85 | 1.37 | 2.36 | 0.74/0.80 | 差 0.06 |
| `6XAdQzbY` | decay **30** / subind | 1.83 | 1.27 | 2.49 | 0.72/0.79 | 差 0.07 |

**★ 归因（三条，第一条是本战役最有价值的算子级发现）**：

1. **`hump` 档位是「抬 SUB 而不抬 S」的唯一杠杆**：hump 0.01→0.02 让 SUB 0.70→**0.80**（+0.10）
   而 S 只 1.81→1.83（SUB 线 0.78 未动）、DD 10.85%→**8.26%**、TO 4.57%→4.37%。
   对照 `decay 30`：S 1.81→1.85 ⇒ SUB 线 0.78→0.80，SUB 虽 0.70→0.74 却仍差 0.06
   —— **decay 抬 S 的同时把 SUB 线一起抬走**（见 §⑮.5 的 0.43×S 机制），是**假杠杆**。
   机制：hump 是**对输入小变化/小值的过滤**（❗不是分位数离散化 —— 该说法 2026-10-22 批 36 已证伪，
   见 §⑮.10.1：在 `interest_expense_revision_magnitude` 上 hump 0.02 与 0.03 的 8 项指标逐位相同），
   在当前信号上它抑制了小盘噪声仓 ⇒ DD 与 TO 同降、子宇宙持仓更有效；它不改信号强度（S 稳）只改持仓分布。
   **判据：SUB 差 ≤ 0.10 时先扫 hump 档（0.005/0.01/0.02），再谈 decay** ——
   但该杠杆**不是通用的**，作用域 = 信号非零量级的分布落在 hump 阈值**之下**才有咬合（§⑮.10.1 两次证伪）。
2. **回填窗口 / winsorize 尾部与 SUB 无关**（四臂 0.68–0.71，全在 baseline ±0.03）：
   SUB 不是「陈旧估计」或「极值仓」造成的，而是**分组基准内小盘样本的结构性分布**——这两类杠杆在本族无效，不再扫。
3. **代价是 2Y −0.22（2.34→2.12），但余量仍 +0.54**：hump 0.02 牺牲的是近两年表现（平滑后错过快速切换），
   对本族是**可付的代价**。若后续需要更宽 SUB 余量，可试 hump 0.03（预判 2Y 继续降，需 ≥1.58）。

**下一步（已执行）**：`QPYvAnNw` → `submit_verdict` = 无仿真层失败（failed_ra 0）→ prod/self 带外实测（见 §⑮.11）。

### ⑮.9 aC=0 白空间地图（2026-10-22，922 字段全量聚合）

**判据来源**：`eps_surprise_stddev` prod 0.8591（§⑮.5.1）⇒ **被生产池覆盖过的是「水平量/修正量」，
本集低 prod 的白空间只剩平台零使用（alphaCount=0）的冷字段**。把 `get_field_catalog` 的 922 字段
按前缀聚合（脚本 `logs/_tmp_ac0_map.py`，只读 catalog，零平台请求），**按 aC=0 数量排序**：

| 族 | aC=0 / 总数 | 均 cov | 代表字段（cov） | 战役状态 |
|---|---:|---:|---|---|
| `estimate_*` | **302/322** | 0.611 | `estimate_q1_change_1mo_ebit`（0.893） | 巨族，未系统挖 |
| `est_y*` | 32/38 | 0.737 | `est_y1_asymmetry_eps`（0.868） | 不对称度族（批 11 已判 SUB 指纹） |
| **`interest_expense_*`** | **32/32** | **0.731** | `interest_expense_y1_skewness`（0.885）、`y1_change_3mo`（0.877） | **零使用，本批 35 首挖** |
| `dividend_estimate_*` | 31/31 | **0.398** | — | 覆盖 < 0.4，弃 |
| `nav_estimate_*` | 30/34 | 0.645 | `nav_estimate_cagr2y_year1`（0.797） | 修正幅度臂已死（§⑮.5.1） |
| `est_q*` | 28/36 | 0.694 | `est_q1_change_1mo_profit`（0.862） | 季度版，未挖 |
| `netprofit_*` / `eps_*` / `revenue_*` | 27 / 25 / 24（各 36） | 0.87–0.89 | trend_slope / qoq_growth | 已多轮覆盖 |
| `op_expense_*` | 23/30 | 0.660 | `op_expense_estimate_y1_change_3mo`（0.831） | **零使用，未挖（是利润腿的镜像，prod 先验较差）** |
| `fwd_year1_estimate_cagr*` | 13 条 cagr | 0.54–0.86 | `fwd_year1_estimate_cagr_2yr`（0.853） | 是「FY1 自身的历史 CAGR」= 趋势族，趋势族已判弱 |
| `ebitda_*` / `cogs_*` / `capex_*` / `cf_operating_*` | 12 / 9 / 15 / 17 | 0.53–0.76 | — | 未挖，覆盖偏低 |

**三条可复用判据**：

1. **选字段第一判据是 aC=0**，不是覆盖或描述漂亮。aC>0 的字段在本集已有 5 次 prod 0.85+ 的前科。
2. **`forward_year*_estimate_*` 只有 5 个字段**（nprofit/pprofit × y1/y2 + gpm 仅 y1）——
   「视界差」在本集已挖尽（§⑮.7 的 8 臂即全集）。
3. `dividend_estimate_*` 全族 cov ≤ 0.495，**低于 0.4 的字段不进入候选**（coverage 硬闸），不再评估。

### ⑮.10 批次 35：利息费用族（成本墙 / 资本结构）预登记

multisim `4i29lZ7CL59C9buRNwjZEBx`，USA/TOP3000/D1/decay 20/RAM/trunc 0.08，批 29 壳，**8 臂**。

**机制（成本上升 = 信用恶化）**：分析师上调**利息费用**预期 ⇒ 再融资成本上升 / 加杠杆 ⇒ 股权未来跑输；
下调 ⇒ 去杠杆 / 低成本再融资 ⇒ 跑赢。所以方向取 **负**（做空利息负担上升）。
这是本集里唯一一条**与盈利腿经济上分离**的族（利息费用不直接进 EPS 分子，但进信用与风险溢价），
且 32 个字段**平台零使用** ⇒ prod 先验最干净。

| # | 变换 | 语义 | 方向 |
|---|---|---|---|
| E1 | `ts_zscore(interest_expense_y1_change_3mo, 504)` | FY1 利息预期近 3 月变动的自身历史标准化 | − |
| E2 | `ts_zscore(interest_expense_y2_change_3mo, 504)` | FY2 版本（更长期） | − |
| E3 | `ts_zscore(interest_expense_q1_change_1mo, 504)` | 当季 1 月变动（最快） | − |
| E4 | `interest_expense_2yr_cagr_estimate`（本就是比率） | 过去 2 年利息费用 CAGR 水平 | − |
| E5 | `ts_zscore(interest_expense_trend_slope_1yr, 504)` | 1 年趋势斜率（单位经 z-score 归一） | − |
| E6 | `ts_zscore(interest_expense_y1_skewness, 504)` | 分析师分歧偏斜（离散度机制） | + |
| E7 | `ts_zscore(interest_expense_y1_coeff_variation, 504)` | 分歧变异系数（离散度机制） | + |
| E8 | `ts_zscore(interest_expense_revision_magnitude, 504)` | 修正幅度（无向，当坏消息代理） | − |

**预登记判据**：先看 E1–E5（方向机制）与 E6–E8（离散度/幅度机制）两组各自的过闸数——
**同族内两组若方向相反且都能过闸，直接判「方向不可识别」并弃族**（这是本集非对称度族的既有教训）；
任一臂 RA 全过 → `submit_verdict` + prod 带外实测 → D0-P。

#### 收批结果（8/8 COMPLETE，2026-10-22）

| # | alpha | 变换 | S | F | 2Y | SUB/线 | 判读 |
|---|---|---|---:|---:|---:|---|---|
| E1 | `N1eNGKoX` | y1_change_3mo − | **1.71** | **1.11** | **2.02** | 0.44/0.74 | 仅 SUB（−0.30） |
| E2 | `vRO1bYVd` | y2_change_3mo − | 1.52 | 0.93 | 1.20 | 0.68/0.66 ✓ | S/F/2Y（SUB 反过） |
| E3 | `1YjNRG5X` | q1_change_1mo − | 1.57 | 0.99 | 1.28 | 0.39/0.68 | 四闸 |
| E4 | `1YjNRG5R` | 2yr_cagr 水平 − | 1.21 | 0.81 | 1.91 | 0.28/0.52 | 四闸 + **CW 0.2277** |
| E5 | `58jE1GRo` | trend_slope_1yr − | 1.50 | 0.90 | 0.90 | 0.35/0.65 | 四闸 |
| E6 | `akVK8RJ1` | y1_skewness + | 1.14 | 0.67 | 0.93 | 0.44/0.49 | 四闸 |
| E7 | `RRAEo5Xz` | y1_coeff_variation + | 1.24 | 0.74 | 1.17 | 0.71 ✓ | S/F/2Y |
| **E8** | **`gJWe5r7J`** | **revision_magnitude −** | **1.60** | **1.01** | **1.87** | **0.68/0.69** | **仅 SUB（−0.01）** |

**★ 归因（四条）**：

1. **E8 只差 0.01，且与批 34 的 hump 杠杆同型**（幅度信号 + 同一壳）⇒ 已直接发批 36（hump 0.02/0.03，
   E8 与 E1 各两档，multisim `4kgXdT8nq5ecabN3WjtHSOO`）。**SUB 差 ≤ 0.05 时先加 hump 档，不换概念。**
2. **E1 是 S/F/2Y 最强臂（1.71/1.11/2.02）但 SUB 0.44（−0.30）**：`y1_change_3mo` 是**变化量**机制，
   在子宇宙系统性弱 —— 与本集「水平/增速 vs 变化量」的既有分化一致（§⑮.5.1）。SUB 缺口太大，
   不投入修壳；若批 36 的 E1+hump 0.02/0.03 仍不进 0.30 缺口，判「变化量腿本族结构性 SUB 墙」。
3. **离散度族（E6/E7）S 只要 1.14/1.24** ⇒ 利息费用上的「分析师分歧」无横截面预测力，
   与盈利腿的分歧族（批 29 的 surprise_stddev 能到 1.8）**不同族**，判弱结案（不判死：E7 的 SUB 与 2Y 都过，
   只缺 S/F，属可被壳层抬 S 的形态，但优先级低于 E8）。
4. **E4 水平量触发 CONCENTRATED_WEIGHT 0.2277（限 0.1）**：无债务公司利息费用=0，横截面在 0 处堆积
   ⇒ **利息费用的「水平」不可用，只能用变化/修正/分歧**（与 §⑮.9 的字段族判断互补）。

**方向可识别性**：负向组（E1/E3/E5/E8）与正向组（E6/E7）没有同时过闸，**不触发弃族判据**；
E8（负向、修正幅度）与 E1（负向、变化）一致，方向机制成立。

#### ⑮.10.1 批次 36：hump 阶梯在利息费用族上的**证伪**（multisim `4kgXdT8nq5ecabN3WjtHSOO`，4/4 COMPLETE）

设计：把批 34 的 hump 杠杆搬到批 35 的两个近失臂上（E8 `revision_magnitude`、E1 `y1_change_3mo`），各取 hump 0.02 / 0.03。

| # | 臂 | hump | S | F | 2Y | SUB / 线 | 判读 |
|---|---|---:|---:|---:|---:|---|---|
| **E8-a** | `E5V6P0r1` revision_magnitude | 0.02 | 1.59 | 1.00 | 1.86 | 0.67 / 0.69 | 仅 SUB（−0.02） |
| **E8-b** | `1YjNAVn6` revision_magnitude | 0.03 | 1.59 | 1.00 | 1.86 | 0.67 / 0.69 | **与 0.02 逐位相同** |
| **E1-a** | `P0MomrXp` y1_change_3mo | 0.02 | 1.70 | 1.10 | 2.02 | 0.44 / 0.74 | 四闸外的 SUB −0.30 |
| **E1-b** | `XgR9AwYa` y1_change_3mo | 0.03 | 1.70 | 1.10 | 2.02 | 0.44 / 0.74 | **与 0.02 逐位相同** |

**★ 归因（两条，第一条推翻了 §⑮.8 的机制解释）**：

1. **hump 0.02 与 0.03 的 8 项指标（S/F/TO/RET/DD/margin/long/short/2Y/SUB）逐位相同** ⇒
   `hump` **不是分位数离散化**，而是「对输入小变化/小值的过滤」。它只在**信号非零量级的质量落在阈值之下**时咬合；
   本族两个信号的量级质量整块位于 0.03 以上 ⇒ 阈值 0.02 与 0.03 完全等价，等于**空转**。
   对照批 34 的 `(FY2−FY1)/|FY1|`：该比值的小数部分恰好落在 0.01–0.02 区间，所以 0.01→0.02 才咬到 +0.10 SUB。
   ⇒ **修正后的判据**：SUB 差 ≤ 0.10 时仍可先扫 hump，但**必须先看信号量级分布**；若量级显著大于拟扫档位，
   这是**零成本的死杠杆**，不要再花仿真。
2. **E8 的 0.01 缺口没被修掉，反而从 0.68 退到 0.67**（S 1.60→1.59、2Y 1.87→1.86）⇒
   hump 在本族是**负向微扰**。E8 的 SUB 缺口既不是「极值仓」（批 34 winsorize 无效）、也不是「回填陈旧」（bf 无效）、
   也不是「平滑不足」（hump 无效）⇒ **判 `interest_expense_revision_magnitude` 的 SUB 为结构性缺口，
   预登记判据「8 臂全卡 SUB ⇒ 本族 SUB 是结构性墙」在 4 臂上提前成立**（E1 缺口 −0.30 更是量级问题）。
   **利息费用族结案**：E8 归档为「RA 近失（SUB −0.01→−0.02）」，不再扩变体；
   E1/E3/E5（变化量/斜率）判「变化量腿系统性弱于子宇宙」；E6/E7（分歧）判 S 不足。

### ⑮.11 批次 37：高阶动态族（aC=0 白空间的下一层机制）预登记

**选型依据 = §⑮.9 的 aC=0 白空间（135 个 cov≥0.6 的 `estimate_*` 字段）+ 三条本集既有教训的交集**：

| 教训 | 出处 | 对选型的约束 |
|---|---|---|
| 「水平量 / 修正量」是被生产池覆盖过的构念 | §⑮.9 判据 1 | 不再拿 `*_value_*`（EBIT/FCF 绝对水平）当主信号；只能作对照 |
| value / quality **水平**在 USA 结构性死亡（book/value 单族 145 颗 ACTIVE） | 区域 profile | 账面价值**水平**、毛利率**水平**弃；只留它们的**变化/趋势** |
| 对预测水平做**时间差分**会把信息打散（丢掉 FY1 锚） | §⑮.7 归因 1 | 不做 `ts_av_diff(forecast_level)`；跨视界差（FY2−FY1）或厂商直接构造的斜率才是对的几何 |
| 稀疏非负项的水平量会在 0 处堆积 → `CONCENTRATED_WEIGHT` | §⑮.10 归因 4（E4 CW 0.2277） | 避开利息费用这类零堆积水平；EBIT/FCF 可正可负，不触发该形态 |

⇒ **本批攻击的是「预测路径的高阶动态」，不是「预测水平」**：加速度（二阶斜率）、边际扩张（毛利率斜率）、
跨视界现金增速、资本密度、隐含 CAGR、账面价值修正。这一层与已交付的 7 个方向（目标价水平 / 视界差 /
修正强度 / 偏度 / 跳空等）机制上零重叠。

multisim `49Ghj09AE5gdaStR8v3YTFb`，**8 臂**，USA / TOP3000 / D1 / decay 20 / RAM / trunc 0.08 /
VERIFY / nan ON / pasteurization ON / maxTrade OFF。**壳固定为批 29 冠军壳 + industry 分组 + hump 0.01**
（唯一变量 = 核），保证归因只指向信号本身：

`quantile(group_rank(hump(ts_backfill(winsorize(<CORE>, std=4), 756), hump=0.01), industry))`

| # | 核心 | 方向 | 机制假设 | cov |
|---|---|---|---|---:|
| A1 | `ts_zscore(estimate_trend_slope2_ebit, 504)` | + | EBIT 预期**加速度**（二阶斜率）：改善在被证实前不被定价 | 0.828 |
| A2 | `ts_zscore(estimate_trend_slope2_eps_reported, 504)` | + | 同机制换 EPS reported 腿 → 检验加速度是**机制**还是**腿特定噪声** | 0.845 |
| A3 | `ts_zscore(estimate_trend_slope_primary_gross_margin, 504)` | + | 毛利率预期**趋势**（边际定价权扩张）；刻意不是水平量 | 0.629 |
| A4 | `ts_zscore(estimate_year2_free_cash_flow − estimate_year1_free_cash_flow, 504)` | + | FCF **跨视界增速**（FY2−FY1 的预期差）；用 z-score 归一而非分母比值 ⇒ 避开 FY1≈0 的爆炸 | 0.790/0.756 |
| A5 | `ts_zscore(estimate_year2_free_cash_flow, 504)` | + | FCF 预期水平相对自身历史（现金创造能力）；A4 的对照组 | 0.790 |
| A6 | `ts_zscore(estimate_y1_depr_amort, 504)` | − | D&A 预期抬升 = **资本密度**上升 ⇒ FCF 转化率下降 | 0.847 |
| A7 | `ts_zscore(estimate_y1_cagr2_ebit, 504)` | + | 分析师隐含 **2 年 EBIT CAGR**（增长率水平，不是修正量） | 0.856 |
| A8 | `ts_zscore(estimate_y2_change_3mo_book_value_ps, 504)` | + | 账面价值预期 **3 月上修**（真实权益增长，比 EPS 修正更难操纵）；变化量而非水平，避开 value 死区 | 0.802 |

**预注册判据（六条，按序执行）**：

1. **任一臂 RA 全过** → 立即 `submit_verdict` + 带外 `check_correlation(refresh=True)` → D0-P 裁决。
2. **只差 SUB 且缺口 ≤ 0.10** → 先加 hump 档（0.02 / 0.03），不换概念（§⑮.8 杠杆一）。
3. **同机制双胞胎**（A1/A2 加速度；A4/A5 FCF 水平 vs 增速）：若都过闸，只留 IS 更强的一条送 prod，
   另一条直接归档（同族 self-corr 风险，不拿两条换一颗）。
4. **方向可识别性**：同一构念的 +/− 若都能过闸 ⇒ 判「方向不可识别」并弃该构念（沿用 §⑮.10 判据）。
5. **衰退判据**：若 8 臂全部 `S < 1.25`，判「预测路径高阶动态在本集无横截面预测力」，封存
   `USA-ANLFS-HIGHER-ORDER-WEAK`，本集只保留「视界差 + 修正」两条已证实线。
6. **A6 的符号若反了**（D&A 上升反而跑赢），说明本集把 D&A 当 capex 扩张（成长）而非成本 —— 记结论不修壳。


### ⑮.12 批次 37 结果：8 臂 0 全过，但 **A6 符号反转**产出全 session 最近的 RA 近失（multisim `49Ghj09AE5gdaStR8v3YTFb`，8/8 COMPLETE）

同上批设置（decay 20 / RAM / industry / hump 0.01 / backfill 756）。指标全部经 `get_alpha_details` 取。

| # | id | 核心 | S | F | 2Y | SUB（限 0.43·S） | 判定 |
|---|---|---|---:|---:|---:|---|---|
| A1 | `leMAPEX8` | `ts_zscore(estimate_trend_slope2_ebit,504)` **+** | 1.60 | 1.11 | **1.25 ✗** | 0.63（0.69） | 2Y 挂 0.33 |
| A2 | `RRAEw9Lj` | `ts_zscore(estimate_trend_slope2_eps_reported,504)` **+** | 1.56 | 1.09 | **1.31 ✗** | 0.54（0.67） | S/2Y/SUB 三挂 |
| A3 | `O0JAXRvb` | `ts_zscore(estimate_trend_slope_primary_gross_margin,504)` **+** | 0.82 | 0.44 | **0.04** | — | 判死（2Y≈0） |
| A4 | `JjPeJoLW` | `ts_zscore(estimate_year2_free_cash_flow − estimate_year1_free_cash_flow,504)` **+** | 1.16 | 0.72 | 1.27 | 0.72 | 太弱，弃 |
| A5 | `qMELJOb1` | `ts_zscore(estimate_year2_free_cash_flow,504)` **+** | 0.89 | 0.47 | 0.75 | — | 判死（水平量） |
| A6 | `9qExO8o9` | `ts_zscore(estimate_y1_depr_amort,504)` **−** | **−1.56** | −1.03 | −1.82 | −1.03 | **符号反了 → 镜像即候选** |
| A7 | `58jEdrRJ` | `ts_zscore(estimate_y1_cagr2_ebit,504)` **+** | 1.66 | 1.23 | **2.23** | **0.40**（0.72） | 只挂 SUB，缺口 0.31 |
| A8 | `78oLR3gb` | `ts_zscore(estimate_y2_change_3mo_book_value_ps,504)` **+** | 1.48 | 1.00 | 1.50 | 0.53（0.64） | S/2Y/SUB 挂，缺口 0.11 |

**归因（逐条具名，不盲扫）**：

1. **A6 的符号反转命中预注册第 6 条**：本集把 D&A 预期抬升读成 **capex 扩张 / 成长周期**，不是成本负担。
   ⇒ 镜像表达式 `quantile(group_rank(hump(ts_backfill(winsorize(ts_zscore(estimate_y1_depr_amort, 504), std=4), 756), hump=0.01), industry))`
   实测 **S 1.56 / F 1.03 / 2Y 1.82 / SUB 1.03（限 0.67）/ TO 4.57%**，**唯一缺口 = LOW_SHARPE 1.56 vs 1.58（−0.02）**。
   这是本 session 离 RA 全闸最近的一条（比 A8/A7 都近）。
   ⚠ **方向可识别性检验**：反号只有 −1.56 一侧成立、正号侧 −1.56 ⇒ 该构念方向**可识别且强**，不是双向噪声
   （§⑮.10 判据 4 的反面）。**教训：负号臂也是信息——它定义了构念的符号，别把负 S 当废结果丢掉。**
2. **A1/A2 加速度双胞胎：机制真实但不持久**。两腿 S 都到 1.56–1.60（S/F 双过），2Y 却只有 1.25/1.31。
   S > 2Y 的含义是**近期半衰**：加速度的超额集中在前半段（2014–2018 预期修正制度更慢），近年被定价。
   ⇒ 加速度构念**可作对照腿，不可作主腿**（USA 2Y 闸 1.58 结构性拦它）。本集这一层封存。
3. **A3 毛利率趋势 2Y = 0.04 ⇒ 判死**。2Y 接近 0 且 S 0.82 说明 `trend_slope_primary_gross_margin`
   是**噪声级**字段（cov 0.629 也偏低），与「毛利率水平在 USA 必死」是两条独立的死因，合起来这条线全封。
4. **A4/A5 FCF 双输 ⇒ FCF 线关闭**：跨视界增速 1.16、水平 0.89。水平量输印证 §⑮.9 判据 1
   （水平构念被生产池覆盖 / value 死区）；增速输说明 FCF 预期路径在本集**没有横截面区分度**
   （FCF 是残差项，一致预期对它的一致性最低）。
5. **A7 是「强信号 + 子宇宙断层」的教科书样本**：S 1.66 / F 1.23 / **2Y 2.23** 全过，SUB 0.40 vs 限 0.72。
   2Y 2.23 是本集历史最高，说明机制（隐含 2 年 EBIT CAGR）**真实且持久**；
   缺口 0.31 指向**小盘集中**（隐含 CAGR 高的多是覆盖稀疏的小票）。这不是算子能修的形态
   —— 本族已证 winsorize/backfill/hump/decay 对 SUB 全为 no-op（§⑮.8 / §⑮.10.1）。
   **待验杠杆 = 中性化档（RAM→SUBINDUSTRY/MARKET）与分组轴**，属设置层诊断，须单独成批并写明诊断问题。
6. **A8 缺口 0.11，界于可修与不可修之间**：S 1.48 还要再涨 0.10 才够闸，而 SUB 也差 0.11
   ⇒ 双重缺口，非单一杠杆可解；且账面价值修正与已交付的 EPS 修正族同源（self-corr 风险）。
   **归档不追**。

**本批对白空间账本的更新**：`estimate_*` aC=0 白空间里，**D&A 族（y1/y2/q2_qoq 三个字段，cov 0.85/0.87/0.77）
是当前唯一「S 贴闸 + SUB 大幅富余」的构念** ⇒ 下一批（批 38）把全部仿真预算压在它的 S 修复上（+0.02），
不再分散到其它构念。

### ⑮.13 批次 38/39：D&A 预期水平的 S×2Y 联合修复 —— **3 条 RA 全过候选**（本集首个三连过闸）

批 38（S 修复，decay 20/30 分开发）+ 批 39（S×2Y 联合修复）共 19 臂，全部经 `get_alpha_details` 取。
核心构念全程冻结为 `ts_zscore(estimate_y1_depr_amort, W)` 水平（= 批 37 A6 的符号反转），
只动 W / 分组轴 / hump 档 / decay —— 属 S4 Mode A（参数层），未换概念、未改中性化（RAM 固定）。

**批 38（multisim `2cmQzE4HS4xYbIo17gXponCx` 8 臂 + `fkuuL4uL4VT8GdbagWqzDF` 3 臂）**

| 臂 | id | W / 分组 / hump / decay | S | F | 2Y | SUB（限） | 缺口 |
|---|---|---|---:|---:|---:|---|---|
| B1 对照 | `RRAExkQd` | 504 / industry / .01 / 20 | 1.56 | 1.03 | 1.82 | 1.03（0.67） | S −0.02 |
| B2 | `58jEKq05` | 756 / industry / .01 / 20 | 1.54 | 1.01 | **1.91** | 1.00 | S −0.04 |
| B3 | `bl860W5Z` | 252 / industry / .01 / 20 | 1.56 | 1.02 | 1.82 | 0.96 | S −0.02 |
| B4 | `LL5MolAn` | 504 / industry / **.005** / 20 | 1.46 | 0.93 | 1.56 | 0.93 | S/F/2Y 三挂 |
| B5 | `QPYvR5Lg` | 504 / **subind** / .01 / 20 | **1.61** | 1.03 | 1.58 | 0.97 | **2Y −0.005** |
| B6 | `omoEj9O6` | **y2 字段** / industry / .01 / 20 | 1.61 | 0.95 | 1.55 | **0.29** | F/SUB/2Y |
| B7 | `QPYvR5Xg` | **q2_qoq 字段** / industry / .01 / 20 | 1.20 | 0.70 | 1.21 | **0.21** | 四挂 |
| B8 | `0mjYZKWq` | **y2−y1 增速** / industry / .01 / 20 | 1.55 | 1.01 | 1.32 | **0.41** | S/SUB/2Y |
| C1 | `omoEjvm5` | 504 / industry / .01 / **30** | 1.55 | 1.02 | 1.81 | 1.03 | S −0.03 |
| C2 | `vRO179Rd` | 756 / industry / .01 / **30** | 1.53 | 1.00 | 1.89 | 1.01 | S −0.05 |
| C3 | `P0MoL60K` | 504 / **subind** / .01 / **30** | 1.61 | 1.03 | 1.56 | 0.98 | 2Y −0.02 |

**批 39（multisim `ueqMsf6v4xB8QqA92VjeVc` 8 臂，全 decay 20 / RAM）**

| 臂 | id | W / 分组 / hump | S | F | 2Y | SUB（限） | 判定 |
|---|---|---|---:|---:|---:|---|---|
| T1 对照 | `QPYvR5Lg` | 504 / subind / .01 | 1.61 | 1.03 | 1.58 | 0.97（0.69） | 2Y −0.005 |
| T2 主假说 | `A1QVXE8g` | 756 / subind / .01 | 1.55 | 0.97 | 1.77 | 0.86 | S/F 挂 |
| T3 | `9qEx5kOV` | 1008 / subind / .01 | 1.55 | 0.97 | 1.79 | 0.84 | S/F 挂 |
| T4 | `e765MEZM` | **252** / subind / .01 | 1.59 | 1.00 | 1.70 | 0.87（0.68） | ✅ **RA 全过** |
| T5 | `GrgWj9jJ` | 504 / **sector** / .01 | **1.61** | **1.08** | 1.78 | 0.94（0.69） | ✅ **RA 全过（最强）** |
| T6 | `ZYmQVNVQ` | 756 / **sector** / .01 | 1.58 | 1.05 | **1.83** | 0.90（0.68） | ✅ **RA 全过** |
| T7 | `0mjYZ5Z2` | 504 / subind / **.02** | 1.59 | 1.01 | 1.56 | 0.92 | 2Y −0.02 |
| T8 | `kqJNp9wd` | 756 / subind / **.005** | 1.43 | 0.85 | 1.45 | 0.83 | 三挂 |

**归因（每条都是可复用杠杆，不是本批局部结论）**：

1. **分组轴是 S / 2Y 的权衡轴，不是免费杠杆**：industry → 2Y 富余（1.82）/ S 缺（1.56）；
   subindustry → S +0.05（1.61）/ 2Y −0.24（1.58）；**sector → 两者兼得（1.61 / 1.78）**。
   机制：分组越细同侪基准越紧，S 上升来自更干净的相对定价；但 2Y 恶化说明 2022–2023 段
   **细分行业内的 D&A 资本密度差被抹平**，而 sector（11 桶）保留了行业间的资本密度差。
   ⇒ 以后遇到「S 够 2Y 不够 / 2Y 够 S 不够」的双闸互斥，**先扫分组轴（3 档）再谈任何参数**。
2. **单变量外推在两项交互时会失效**：z756 在 industry 上抬 2Y +0.09 只花 0.02 S，
   但 subindustry 上 T2 是 **1.55**（若可加应为 1.59）⇒ z756 × 分组存在交互。
   T6（z756 × sector）再验：S 代价 0.03、2Y 收益 +0.05，也不是常数。
   **铁律：加了第二维就重测该维的每个档，不要用单维斜率外推。**
3. **hump 甜区在本族 = 0.01**（.005 一律更差：B4 1.46 / T8 1.43；.02 掉 2Y：T7 1.56）。
   这是 §⑮.10.1 证伪「hump 是分位数离散化」后的第二个正面证据：hump 对小值/小变化过滤，
   **咬合阈值由信号量级分布决定**，本族量级正落在 0.005–0.02 带。
4. **decay 30 在本族是负杠杆**（C1 1.55 < B1 1.56；C3 2Y 1.56 < B5 1.58），
   推翻「本集 decay 20→30 = +0.04 S」的旧结论 —— 那条来自**另一个核心**（§⑮ 批 34），不可跨核迁移。
   decay 对本族唯一作用是压低换手（4.57%→4.57%，实际无变化）⇒ **确认为假杠杆**（§⑮.8 的同源结论第二次复现）。
5. **字段口径：y1 是唯一「全赛道」口径**。y2 掉 SUB 到 0.29、q2_qoq 掉到 0.21、y2−y1 增速掉到 0.41。
   ⇒ 本族正确几何是**水平量本身**（FY1 一致预期 D&A 占收入/资产的强度），
   一旦换成远期口径（y2）或变化量（y2−y1、qoq）就**只剩小盘 alpha**（SUB 崩塌）。
   这与 §⑮.7 归因 1（对预测水平做时间差分丢锚）同源：**跨视界差把 FY1 锚丢了**。
6. **同机制孪生纪律生效**：T4/T5/T6 是同构念的三个参数变体，全部 RA 过闸。
   按 §⑮.11 预注册判据 3，**只送最强的一条（T5 `GrgWj9jJ`）去 prod**，
   另两条归档（`e765MEZM` 低 DD 5.99% 留作 T5 prod 不合格时的替补，`ZYmQVNVQ` 2Y 1.83 最高但 S 贴线）。

**T5 全闸读数**（`GrgWj9jJ`，提交候选 #6）：S 1.61 / F 1.08 / 2Y 1.78 / **SUB 0.94（限 0.69）** /
TO 4.67% / DD 6.92% / 多空 1506·1619 / margin 2.4‱；RA 8 项全 PASS，`ra_failed=false`；
warnings 只有 `CLUSTER_TEST 0.97`（允许项）+ `MATCHES_THEMES` + `OSMOSIS_ALLOCATION`。
金字塔挂 `USA/D1/ANALYST`（×1.2）。

### ⑮.14 批次 40：A7 隐含 CAGR 的 SUB 断层诊断 —— 分组轴救不回来，判 small-cap-only

**诊断问题（单一）**：A7 `58jEdrRJ`（S 1.66 / F 1.23 / **2Y 2.23**）唯一缺口是
SUB 0.40 vs 限 0.72。断层源于「分组桶过窄只剩小盘」还是「构念本身只在小盘有效」？

8 臂同壳（`quantile(group_rank(hump(ts_backfill(winsorize(ts_zscore(<core>, W), std=4), 756), hump=0.01), <group>))`），
core 默认 `estimate_y1_cagr2_ebit`：

| # | 臂 | core / W | group | S | F | 2Y | SUB（限） | SUB/限 | DD |
|---|---|---|---|---|---|---|---|---|---|
| V1 | 对照 industry | cagr2 / 504 | industry | 1.66 | 1.23 | 2.23 | 0.40（0.72） | 0.556 | 10.78% |
| **V2** | **sector** | cagr2 / 504 | **sector** | **1.81** | **1.41** | 2.20 | 0.46（0.78） | **0.590** | **8.63%** |
| V3 | subindustry | cagr2 / 504 | subindustry | 1.48 | 0.99 | 2.17 | 0.36（0.64） | 0.563 | 11.08% |
| V4 | market | cagr2 / 504 | market | 1.76 | 1.36 | 2.04 | 0.47（0.76） | **0.618** | 9.68% |
| V5 | z756 | cagr2 / 756 | industry | 1.65 | 1.22 | 2.24 | 0.33（0.71） | 0.465 | 10.31% |
| V6 | 3y 视界 | **cagr3** / 504 | industry | 1.43 | 1.07 | 2.16 | 0.60（0.62） | **0.968** | 16.79% |
| V7 | 5y 视界 | **cagr5** / 504 | industry | 1.11 | 0.79 | 1.84 | 0.58（**PASS**） | >1 | 22.45% |
| V8 | sector+3y | cagr3 / 504 | sector | 1.46 | 1.12 | 2.14 | 0.62（0.63） | **0.984** | 18.12% |

ALPHA ID：V1 `58jEdrRJ` / V2 `JjPeAaRW` / V3 `E5V6jn00` / V4 `RRAEOxZb` /
V5 `JjPeAaYj` / V6 `2rjAgVQZ` / V7 `ZYmQ8Vqd` / V8 `leMAnw2O`。

**归因 1（决定性）：SUB 不是分组产物。**

分组轴从最细 `subindustry` → `industry` → `sector`（11 桶）→ `market`（单桶），
SUB/限 比值只从 0.563 抬到 0.618（+0.055）。**桶宽几乎不改变断层的相对深度**，
两条极端（最细 vs 不分组）落在同一带内 ⇒ 「桶窄=只剩小盘」的假设**证伪**。
若真是桶宽问题，market（全市场一个桶）应该接近 1.0，实测 0.618。

**归因 2（决定性）：SUB 沿「视界轴」单调修复，但 S 同向崩塌 —— 这是同一条轴上的零和。**

| core | S | 2Y | SUB/限 |
|---|---|---|---|
| cagr2（2 年） | 1.66 | 2.23 | 0.556 |
| cagr3（3 年） | 1.43 | 2.16 | 0.968 |
| cagr5（5 年） | 1.11 | 1.84 | **PASS** |

**远期 CAGR 预期是纯小盘信息**：2 年预期增速在**大盘内部几乎无截面差异**（都收敛到长期名义增速），
所以大盘子宇宙的排序接近随机 ⇒ SUB 恒低；把视界拉长到大盘也有分化的 5 年，
SUB 才恢复，但那时 alpha 本身也弱了（S 1.11 / F 0.79 / DD 22.45%）。
**不存在既保住 S≥1.58 又让 SUB 达标的视界档** ⇒ 该构念在本区域不可提交，
与参数、分组、窗口无关。

**归因 3（副产品，本族最强 IS 读数）：V2 sector 是整场 session 最高的 IS 组合。**

S **1.81** / F **1.41** / 2Y 2.20 / DD **8.63%** / TO 5.03% / margin 3.0‱ / 多空 1525·1601。
比 V1 同时抬 S +0.15、F +0.18、降 DD 2.15pt —— **sector 分组在「2 年 CAGR 水平」构念上是全局最优分组**
（与批 39 T5 在 D&A 上选 sector 的结论一致，跨核心第二次复现）。
但它 SUB 0.46 硬挂 ⇒ **留档为「SUB 墙参照点」，不提交**。

**归因 4（同族教训）：market 分组是「SUB 上界」的测量器。**
V4 的 SUB/限 0.618 是本批最高 ⇒ 说明该核心的**大盘信息含量上限就是 0.62 倍限值**，
任何分组/窗口都只是在这个上限下抖动。**以后遇到 SUB 挂且 S 够高的候选，先做一个 market 分组臂量上界**：
若 market 也 < 0.8 倍限值 ⇒ 直接判 small-cap-only，不必再扫分组轴（省 3–4 臂）。

**处置**：A7 族（隐含 2 年 CAGR 水平的任意变体）判 **small-cap-only ⇒ dead_end**（按批 40 预注册判据）。
唯一未测的同字段异机制是**修正/revision 构念**（预期变化量而非水平），
它属新机制、不是本条的参数救援，留待 aC=0 白空间批另行设计。

### ⑮.15 批次 41：资本资产结构（capex / D&A / EBIT 比率）预登记

**为什么换腿**：已交付 5 颗（#1 EPS 环比增速、#2 EPS 偏度、#3/#4 EPS×营收背离、#7 合并 EPS 修正幅度）
＋排队 3 颗（T5 D&A 预期水平、`QPYvAnNw` 视界差、`E5V620lK` 实际 EPS 环比）
**全部落在 EPS / 修正 / 分歧三条腿上**。本批换到**资产基础的新旧结构**，与三种既有几何（水平 / 修正 / 分歧）都正交。

**几何**：两个预期量相除（同单位 ⇒ 无量纲，避开 VERIFY 的 UNITS 警告），
再用本集唯一 SUB 安全的壳：`quantile(group_rank(hump(ts_backfill(winsorize(ts_zscore(<ratio>, 504), std=4), 756), hump=0.01), sector))`。

**四个字段全部 aC=0**（§⑮.9 判据 1）：`next_fiscal_year_capex_consensus`(0.7779) /
`estimate_y1_depr_amort`(0.8465) / `estimate_y1_value_ebit`(0.9163) / `estimate_trailing_12mo_ebit`(0.8877)。

| # | 构念 | 比率 | 方向 | 机制 |
|---|---|---|---|---|
| K1 | 资产更新率 | capex / D&A | + | >1 = 资产基础净扩张；与批 37 归因 6（D&A 上升读作 capex 扩张）同向 |
| K2 | 同上 | 同上 | − | 反向：高 capex/D&A = 过度投资（经典 investment 因子） |
| K3 | 资本密度 | D&A / FY1 EBIT | − | 单位盈利需要更多资产 ⇒ 周转低 |
| K4 | 同上 | 同上 | + | 反向：重资产 = 进入壁垒 |
| K5 | 资产负担 | D&A / trailing EBIT | − | 追赶型折旧拖累当期盈利 |
| K6 | 同上 | 同上 | + | 反向 |
| K7 | 再投资率 | capex / FY1 EBIT | + | 投入 = 未来增长 |
| K8 | 同上 | 同上 | − | 反向：低自由现金流 |

**预登记判据**：每构念成对发双向（批 37 教训：负号臂定义构念符号）。
两向都 RA 过 ⇒ 符号不可识别，取 S 强者；任一条 RA 全过 ⇒ `submit_verdict` + prod 带外 → D0-P。
**统一预判风险**：`next_fiscal_year_capex_consensus` 覆盖 0.7779 是本批最低，交集覆盖需 ≥0.4（硬闸）。
若 8 臂全灭且病灶集中在 SUB ⇒ 复用 §⑮.14 归因 4 的 market 分组量上界，不再盲扫分组轴。

multisim `1FSvAY2PH4AA8FWGj2RJQHD`，USA/TOP3000/D1/decay 20/RAM/trunc 0.08，8 臂。

### ⑮.16 批次 41 结果：资本资产结构族 —— 比率腿在 S/F/SUB 全过，唯独丢 2Y

multisim `1FSvAY2PH4AA8FWGj2RJQHD`（8/8 COMPLETE）。壳与设置同预登记。

| # | 构念 | 字段比率 | 方向 | alpha | S | F | 2Y | SUB/限 | DD | 病灶 |
|---|---|---|---|---|---|---|---|---|---|---|
| K1 | 资产更新率 | capex / D&A | + | `3qjo8nOe` | 1.16 | 0.74 | 1.05 | 0.68 / 0.50 pass | 6.7% | S/F/2Y 三挂 |
| K2 | 同上 | 同上 | − | `wp9Q0JAd` | −1.16 | −0.74 | −1.05 | pass | — | 精确镜像 |
| K3 | 资本密度 | D&A / FY1 EBIT | − | `O0JAl5Xb` | −1.65 | −1.11 | −1.38 | pass | — | 2Y 挂 |
| **K4** | 同上 | 同上 | **+** | **`58jEPqdX`** | **1.65** | **1.11** | **1.38** | **0.83 / 0.71 pass** | **5.74%** | **仅 2Y（差 0.20）** |
| K5 | 资产负担 | D&A / trailing EBIT | − | `mLYoExnX` | −1.60 | −1.07 | −1.50 | pass | — | 2Y 挂 |
| **K6** | 同上 | 同上 | **+** | **`3qjo8nmP`** | **1.60** | **1.07** | **1.50** | **0.91 / 0.69 pass** | **6.59%** | **仅 2Y（差 0.08）** |
| K7 | 再投资率 | capex / FY1 EBIT | + | `bl86eWmM` | 0.98 | 0.57 | 0.69 | 0.34 fail | — | SUB 先挂 |
| K8 | 同上 | 同上 | − | `omoEx9bJ` | −0.98 | −0.57 | −0.69 | fail | — | 精确镜像 |

**归因 1（符号识别完成）**：K3/K4、K5/K6 是精确镜像（±S/F/2Y），K1/K2、K7/K8 亦同。
⇒ 该构念的**符号是可识别且已识别**：D&A/EBIT **正向**（重资产 = 进入壁垒/折旧口径健康）成立，
负向（追赶型折旧拖累盈利）不成立。批 37 的「负号臂定义构念符号」纪律第二次生效。

**归因 2（核心病灶 = 比率腿丢 2Y，不是 SUB）**：K4/K6 的 SUB 都健康（0.83/0.91，限 0.71/0.69，余量 0.12/0.22），
DD 也低（5.7% / 6.6%）。与 T5 `GrgWj9jJ`（D&A **水平**腿，S1.61/F1.08/**2Y1.78**/SUB0.94）对照：
**同一个 D&A 周期的信息，做成比率后 S/F 不掉（甚至 K4 S1.65 略高），2Y 却从 1.78 掉到 1.38/1.50。**
⇒ 除法引入了跨股票分母噪声（EBIT 低的股票比率极端化），牺牲了两年期的稳定性。
这不是「换个 ratio」能修的——K4/K6 已经是分母最干净的两个版本（FY1 与 trailing EBIT）。
**比率族的 2Y 上限就在 1.5 附近**；2Y 差 0.08 的 K6 或许能被 z756 杠杆补上，但补上后仍是 T5 的同族孪生。

**归因 3（处置：K4/K6 = T5 的替补，不自成一线）**：K6 `3qjo8nmP` 与 T5 `GrgWj9jJ` 同属
「D&A 预期相对盈利」这一机制的 level/ratio 两面，self 相关必然高。
**T5 prod 若通过 → K4/K6 不单独提交**（同族自锁，且 2Y 未过）；
**T5 prod 若 0.70+ → K6 作为唯一备胎做 z756 补 2Y**（差 0.08 在已实测杠杆区间 0.05–0.09 内）。
故本批**不新增排队项**，K4/K6 并入 T5 的备用梯队（T6 / T4 之后）。

**归因 4（族级）：capex 腿在本集是弱腿**。K1/K2（capex/D&A）S 只有 1.16，K7/K8（capex/EBIT）更差（0.98）。
`next_fiscal_year_capex_consensus` 覆盖 0.7779 是本批最低，且 ac=1–2（非 aC=0）——与 §⑮.9 判据 1 一致：
**aC>0 的 capex 族在本集的历史命中率低**，后续批不再从 capex 出发。
D&A（`estimate_y1_depr_amort`）+ EBIT 预期族仍是本集最强的正交腿之一。

**下一步（本批结论驱动）**：转向 `nav_estimate_*` / `*_mktblsec`（全 aC=0、cov 0.80–0.90）的
**水平 / 修正**构念——它们在机制上与已交付的 EPS / D&A / 分歧三条腿都不同，
且 `estimate_y1_change_3mo_mktblsec`（0.856）带「3 个月修正」信息，可复用已验证的修正幅度壳。

### ⑮.17 批次 42：未见度量族 × T5 全过壳（预登记）

multisim `4FW1ul56X4JJbhgKMin1nn3`，8 臂，USA/TOP3000/D1/decay 20/RAM/trunc 0.08/VERIFY/nan ON/past ON/maxTrade OFF。

**为什么是「度量族」而不是「机制」**：已交付 5 颗 + 排队 3 颗，机制只有四条腿
（EPS 增速 / EPS 偏度 / EPS×营收背离 / 修正幅度）。继续在同四条腿上换壳、换窗口，只会抬高 self-corr。
本批**冻结壳与机制，改换度量对象**：EBITDA / 净利（年度+季度）/ 净资产 NAV / 有价证券 / 税前利润。
这五个度量在本集**平台零使用或近零使用**（aC=0 占 7/8），且与四条已交付腿的收益来源不同
（现金盈利 vs 每股盈利；账面价值 vs 盈利；税前 vs 税后）。

壳 = T5 `GrgWj9jJ` 原样（本集唯一 8 项 RA 全 PASS 的壳）：
`quantile(group_rank(hump(ts_backfill(winsorize(ts_zscore(<FIELD>, 504), std=4), 756), hump=0.01), sector))`

| # | 字段 | 机制 | 方向 | cov / aC |
|---|---|---|---|---:|
| N1 | `ebitda_y1_estimate_skewness` | EBITDA FY1 预期偏度 = 现金盈利上行分歧 | + | 0.8633 / 0 |
| N2 | `ebitda_estimate_surprise_stdev` | EBITDA 意外波动 = 可预测性（低波动⇒溢价） | − | 0.7455 / 0 |
| N3 | `fwd_year1_estimate_change_3mo_nprofit` | FY1 净利预期 3 月修正（非 EPS） | + | 0.9311 / 0 |
| N4 | `quarter1_estimate_qoq_change_nprofit` | 下一季净利预期环比增速（季度视界） | + | 0.8859 / 0 |
| N5 | `nav_estimate_year2_change_3mo` | FY2 净资产预期 3 月修正（账面价值） | + | 0.8901 / 0 |
| N6 | `estimate_y1_skewness_mktblsec` | 有价证券 FY1 预期偏度（财务弹性分歧） | + | 0.8629 / 0 |
| N7 | `ebitda_estimate_year2` | FY2 EBITDA 预期水平（现金盈利能力） | + | 0.8633 / 1 |
| N8 | `fwd_year1_estimate_cagr_2yr_pprofit` | 前瞻 FY1 税前利润 2 年 CAGR | + | 0.8581 / 0 |

**预登记判据（按序）**：

1. **任一臂 RA 全过** → `submit_verdict` + 带外 prod → D0-P。**若同批出现 ≥2 条全过**，
   按 self-corr 先行自检（不同度量族之间未必低相关），只送最正交的一条。
2. **同族近失（只差一闸 ≤ 0.10）** → 按 §⑮.9/§⑮.16 的杠杆阶梯修（2Y 差 ⇒ 扫 W 252/756；
   SUB 差 ⇒ 先量 market 分组上界再决定，§⑮.14 归因 4），不换概念。
3. **N2 的符号是唯一存疑项**（「意外波动低 ⇒ 溢价」是文献方向，但本集可能把高波动读成成长）。
   若 N2 只差一闸且为负 S ⇒ 发镜像，不入下一批主预算。
4. **衰退判据**：若 8 臂全部 `S < 1.25`，判「未见度量族在本集无横截面预测力」，
   封存 `USA-ANLFS-METRIC-FAMILY-WEAK`，本集只保留 D&A / EPS 两条已证实线，转向别集。
5. **N3/N5 与已交付 #7 / 排队的 QPYvAnNw 同属修正机制** ⇒ 若三条都 RA 过，
   只按「修正对象不同」保留，且必须在提交前实测 mutual/self-correlation，不默认正交。

### ⑮.18 批次 42 结果：未见度量族 —— **1 条 RA 全过 + 1 条双微差**，离散度与水平量全灭

multisim `4FW1ul56X4JJbhgKMin1nn3`（8/8 COMPLETE）。壳 = T5 原样（sector / W504 / bf756 / hump .01）。

| # | 度量 | alpha | S | F | 2Y | SUB / 限 | DD | 判读 |
|---|---|---|---:|---:|---:|---|---:|---|
| N1 | EBITDA 偏度 | `RRAeJ9mz` | 0.63 | 0.30 | 0.40 | −0.01 / 0.27 | 8.9% | **判死**（分歧只在 EPS 上有信息） |
| N2 | EBITDA 意外波动 − | `6XAMnZl7` | −1.27 | −0.82 | −0.46 | pass | 63.4% | **判死**（符号也不救：\|S\|1.27） |
| N3 | FY1 净利 3 月修正 | `XgRajV7l` | **1.57** | **0.96** | 1.94 | **0.75 / 0.68 ✓** | 12.2% | **双微差**（S −0.01 / F −0.04） |
| N4 | 下季净利环比 | `vROAKZjA` | 1.58 | 1.00 | 1.43 | 0.30 / 0.68 | 9.8% | SUB+2Y 双挂（小盘集中） |
| N5 | NAV FY2 3 月修正 | `VkdNvZ7A` | 1.35 | 0.80 | 1.66 | 0.42 / 0.58 | 10.1% | 三挂 |
| N6 | 有价证券偏度 | `leMaLE82` | 0.86 | 0.48 | 1.09 | 0.46 | 9.1% | **CW 0.4754 硬挂** |
| N7 | FY2 EBITDA 水平 | `LL5KPE9m` | 1.03 | 0.53 | **0.26** | 0.46 | 6.9% | **判死**（利润水平 = value 死区） |
| **N8** | **前瞻 FY1 税前利润 2 年 CAGR** | **`LL5KPENL`** | **1.72** | **1.32** | **2.23** | **0.78 / 0.74 ✓** | 10.1% | **✅ RA 全过** |

**N8 全闸读数**：TO 5.03% / margin 2.90‱ / 多空 1523·1603；`ra_failed=false`、`checks.fail=[]`；
warnings 仅 `CLUSTER_TEST 1.14`（允许）+ `MATCHES_THEMES` + `OSMOSIS_ALLOCATION`。金字塔 `USA/D1/ANALYST`（×1.2）。

**归因（五条）**：

1. **★ 离散度是 EPS 专属的，不是机制。** N1（EBITDA 偏度）S 只有 0.63，而 #2 的 EPS 偏度 S 1.83。
   同一壳、同一机制、只换度量 ⇒ **「分析师分歧」只有在覆盖最密的度量（EPS）上才有横截面信息**；
   EBITDA / 有价证券的分歧是噪声（N6  además CW 0.4754，说明估计稀疏到个别股票独占权重）。
   **今后不在低频度量上做 skewness/coeff_var**。
2. **★ 利润「水平」是 value 死区，成本「水平」不是。** N7（FY2 EBITDA 水平）2Y 只有 0.26，
   而 T5（D&A 水平）2Y 1.78。二者都是 z 后 group_rank、同一壳 —— 差别在**度量是利润还是成本**：
   利润水平≈价值因子（USA 结构性死亡），成本/资本密度水平≈资产结构因子（未拥挤）。
   这条与 §⑮.9 判据 1（水平量被生产池覆盖）互补：**该判据只对利润类水平成立，不对成本类成立**。
3. **「隐含 2 年 CAGR」是本集第二条高效线，且税前口径 > EBIT 口径。**
   批 37 A7（`estimate_y1_cagr2_ebit`, industry 组）S1.66/F1.23/2Y2.23 但 SUB 0.40 挂；
   本批 N8（`fwd_year1_estimate_cagr_2yr_pprofit`, sector 组）S1.72/F1.32/**2Y2.23**/SUB 0.78 **过**。
   **2Y 完全相同（2.23）说明机制同源（利润增长路径），差异全在 SUB** —— sector 分组把 SUB 从 0.40 抬到 0.78
   （与 §⑮.14 归因 4 的「分组轴 = SUB 上界」一致），税前口径还额外避开税项噪声。
   ⚠ **A7 与 N8 是同一机制的两个度量**：若 N8 提交，A7 不再单独送 prod（同族自锁）。
4. **N3 的双微差（S −0.01 / F −0.04）是 W 杠杆的标准形态**：2Y 1.94 与 SUB 0.75 都有大余量，
   缺口只在水平值。按 §⑮.13 的 z 窗口阶梯（252/756 在本族实测 ±0.05–0.09）⇒ 发批 43 修。
5. **N2 的负号臂给出方向信息**：EBITDA 意外波动**正向**时 S 1.27，说明「高意外波动 = 高成长」在本集成立
   但强度不够 1.58；不是「低波动溢价」。归档不追。

**批次 42 对白空间账本的更新**：`estimate_*` aC=0 白空间里能过闸的只剩**两条线**
（D&A 成本水平 = T5 族；利润隐含 CAGR = N8 族）。偏离这两条的度量（离散度 / 利润水平 / 意外）一律弱。

### ⑮.19 批次 43 结果：6 臂 0 全过，但**两个单闸近失**（R3 2Y 差 0.02、R4 S/F 极强 2Y 差 0.09）

multisim `1oqC8a42j4MqchQLXHyrVnP`（8/8 → 6 臂全 COMPLETE），指标经 `harvest_multisim_alphas` 取。
同一 T5 壳（sector 组 / hump 0.01 / backfill 756 / winsorize std=4 / decay 20 / RAM）。

| # | id | 核心 | S | F | 2Y | SUB（限） | TO | 判定 |
|---|---|---|---:|---:|---:|---|---:|---|
| R1 | `3qj0qANP` | `ts_zscore(fwd_year1_estimate_change_3mo_nprofit, 252)` | 1.56 | 0.95 | **1.99** | 0.73 ✓ | 3.95% | S/F 双挂 0.02/0.05 |
| R2 | `A1Qx13ow` | 同上 W756 | **1.61** | 0.98 | 1.92 | **0.67 ✗**(0.69) | 3.97% | F/SUB 双挂 |
| **R3** | **`9qElqRNe`** | `ts_zscore(divide(estimate_y1_depr_amort, estimate_trailing_12mo_ebit), 756)` | **1.61** | **1.08** | **1.56** | **0.92 ✓** | 5.05% | **只挂 2Y −0.02** |
| **R4** | **`GrgmrwqG`** | `ts_zscore(estimate_surprise_diff_ebit, 504)` | **1.88** | **1.33** | **1.49** | **1.02 ✓** | 4.75% | **只挂 2Y −0.09** |
| R5 | `O0JW0p1d` | `-ts_zscore(estimate_surprise_diff_depr_amort, 504)` | −1.18 | −0.83 | −0.74 | −0.57 | 6.28% | **判死：CW 0.4227**（2014-01-06） |
| R6 | `j2ea2Z2j` | `ts_zscore(nav_estimate_cagr2y_year1, 504)` | 1.34 | 0.94 | 1.66 | **0.36 ✗**(0.58) | 4.94% | 判死（NAV 增速 = book 死区） |

**归因（五条）**：

1. **z 窗口不是 N3 族的解**：R1（W252）把 2Y 从 1.94 抬到 1.99，代价是 S 1.57→1.56、F 0.96→0.95；
   R2（W756）把 S 抬到 1.61，代价是 SUB 0.75→0.67 破闸。三个闸在这族上**互相拉扯**（S↔SUB 反向、2Y↔S 反向），
   W 只是在闸间搬分数、不做净增益 ⇒ **N3（`fwd_year1_estimate_change_3mo_nprofit`）封存**，不再单独修。
   教训：近失 0.01–0.02 出现在**两个及以上闸**时，先看它们是否反向耦合；反向耦合的族没有单一杠杆可解。
2. **W756 是 D&A/EBIT 比率族的确定 2Y 杠杆**：R3 对 K6（W504）2Y 1.50→**1.56**（+0.06）、S +0.01、SUB +0.01。
   机制解释：分母 `estimate_trailing_12mo_ebit` 是滚动量，长窗 z 把近期分母剧变压得更平 ——
   **比率构念的 2Y 病灶在分母噪声，不在分子信号**。⇒ 批 44 用 W1008 再推一格（W 是唯一还有白空间的旋钮）。
3. **★ R4 是全 session S/F 最强的新构念**：`actual − consensus` 的 EBIT 意外，S 1.88 / F 1.33 / SUB 1.02（限 0.81）。
   **S 1.88 ≫ 2Y 1.49 = 典型近期半衰**（PEAD 型漂移在 2022–2023 被抢跑）。
   ⇒ 不是算子形态问题，是构念时效问题；但 0.09 缺口 + S/F/SUB 全部大余量 ⇒ 值得用 W 与度量变换再试一格。
   ⚠ 该字段 **aC=1**（已被用过一次），不属 aC=0 白空间 ⇒ 投入前先看 prod（批 44 出结果后优先测）。
4. **★ R5 判死的理由是 CW 不是方向**：`estimate_surprise_diff_depr_amort` 在 2014-01-06 单票权重 **42.27%**
   —— 该字段早年覆盖极稀。CW 与符号无关（镜像同权重）⇒ 正号侧同样死。
   **新判据：surprise 族先看早年 CW 再看指标**；2014 年覆盖不足的事件字段直接弃，别浪费镜像臂。
5. **R6 判死复证 book 死区**：NAV 2 年 CAGR 的 SUB 0.36（限 0.58）说明它是大盘集中构念，
   与 §⑮.18 判据 2（利润水平 = value 死区）同源。**NAV 族封存**（唯一例外是已判死的 A8 账面价值 3 月修正）。

**白空间账本更新**：`surprise` 族（actual − consensus）是本集**唯一还有 S/F/SUB 大幅余量**的新构念。
aC=0 的兄弟字段全部未试：`estimate_surprise_difference_pprofit`（cov 0.8265）、
`ebitda_estimate_surprise_diff`（0.7286）、`interest_expense_surprise_difference`（0.7331）、
`op_expense_surprise_difference`（0.7051）。⇒ 批 44 主线 = surprise 族四兄弟 + 两个 2Y 修复臂（R3/R4 的 W 梯）。

### ⑮.20 批次 44 结果：**S4 税前利润意外 RA 全过**（surprise 族首个），并测出「聚合层级 → 2Y」单调律

multisim `1jFAtJeWb4RF9j3n3Yo0G1d`（8/8 COMPLETE），指标经 `harvest_multisim_alphas` 取。

| # | id | 核心 | S | F | 2Y | SUB（限） | TO | 判定 |
|---|---|---|---:|---:|---:|---|---:|---|
| S1 | `WjLl1w2o` | EBIT 意外 W252 | 1.90 | 1.35 | **1.50** | 0.97（0.82） | 4.75% | 只挂 2Y −0.08 |
| S2 | `O0JWQwdp` | EBIT 意外 W756 | 1.87 | 1.32 | **1.50** | 1.00（0.80） | 4.77% | 只挂 2Y −0.08 |
| S3 | `kqJaEkpz` | EBIT 意外 `ts_av_diff 504` | 1.83 | 1.22 | **1.79** | **0.59 ✗**（0.79） | 4.43% | 只挂 SUB；⚠ UNITS 警告 |
| **S4** | **`QPY0ZrxG`** | **税前利润意外 W504** | **1.83** | **1.33** | **2.06** | **0.91 ✓**（0.79） | 4.88% | **✅ RA 全过（failed_ra=0）** |
| S5 | `0mjPOkJq` | EBITDA 意外 W504 | 1.27 | 0.84 | **0.80** | 0.74 ✓ | 5.15% | 判死（3 闸） |
| S6 | `RRAejZge` | −利息费用意外 | −1.21 | −0.77 | −1.47 | −0.43 | 5.50% | 判死（3 闸） |
| S7 | `leMap6ox` | −经营费用意外 | −1.31 | −0.79 | −0.70 | −0.29 | 5.06% | 判死（3 闸） |
| S8 | `O0JWQwlR` | D&A/EBIT 比率 W1008 | 1.61 | 1.09 | **1.55** | 0.93 ✓ | 5.03% | 只挂 2Y −0.03（**W 梯见顶**） |

**归因（五条，第一条是本批最重要的机制发现）**：

1. **★「聚合层级 → 2Y 持久性」单调律**：同一壳、同一 `actual − consensus` 机制、只换度量对象——
   **EBITDA 意外 2Y 0.80 ＜ EBIT 意外 2Y 1.49 ＜ 税前利润意外 2Y 2.06**（S 分别 1.27 / 1.88 / 1.83）。
   机制：越靠近利润表底线的聚合项，意外越接近「真实盈利惊喜」；EBIT 及以上的层级会被
   成本重分类 / 费用计提口径差异污染，漂移不持久。**⇒ 意外族今后一律先做税前/净利口径，不做 EBIT 以下层级。**
   ⚠ 这条同时**改写了 ⑮.18 判据 5 的「意外一律弱」**：弱的是 EBIT/EBITDA 口径，不是意外机制本身。
2. **W 对 EBIT 意外的 2Y 是 no-op**：S1（W252）/ S2（W756）2Y 都是 1.50，对 W504 的 1.49 只 +0.01。
   ⇒ 2Y 墙是**构念口径**造成的，不是窗口造成的；与归因 1 互证（换口径 → +0.57，换窗口 → +0.01）。
3. **`ts_av_diff` 用 SUB 换 2Y，净不过**：S3 把 2Y 从 1.49 抬到 **1.79**（+0.30），SUB 从 1.02 掉到 **0.59**（−0.43）。
   ⇒ 度量变换买到的是「近两年更强、子宇宙更偏」；净结果仍差一闸，**不作候选**。
   ⚠ 同臂触发 `UNITS` 警告（`hump` 期待 `Unit[]`，实收 `Unit[TSPrice:1]`）——`ts_av_diff` 输出保留价格量纲，
   与 `hump` 的语义不匹配。**今后 `ts_av_diff` 后不直接接 `hump`**（改接 zscore 或去掉 hump 档）。
4. **费用项不是独立信号源**：S6 利息费用 / S7 经营费用的负号臂 |S| 1.21 / 1.31，且 2Y 更差（−1.47 / −0.70）。
   即便正号侧也只有 1.2–1.3 的强度 ⇒ 它们是「利润意外的噪声分量」，不是另一个 alpha 源。**费用意外族封存。**
5. **D&A/EBIT 比率族的 W 梯已到顶**：W504 2Y 1.50 → W756 **1.56** → W1008 **1.55**（非单调，见顶）。
   ⇒ 该族 2Y 天花板 1.56，缺 0.02 无杠杆可补。**比率腿封存**（T5 水平腿仍是本族主力，见 prod 队列）；
   预注册判据 2 的「2Y 差 ⇒ 扫 W 252/756」在此族已穷尽。

**预注册判据执行情况**：判据 1 命中（S4 全过 → `submit_verdict` + prod 排队）；判据 2 命中三次（S1/S2/S8 单闸近失，
杠杆阶梯已走完）；判据 3（同族 ≥2 条 |S|≥1.5 ⇒ 测同源相关）**待执行**：S4 与已排队的 N8 / QPYvAnNw / E5V620lK
同属「利润增长/意外」大类，提交前必须 pair 测 `compute_mutual_correlation`；判据 4 未触发。

**白空间账本更新**：`surprise` 族的可用口径锁定为**税前利润**（`estimate_surprise_difference_pprofit`，aC=0、cov 0.8265）。
同口径的近邻字段（`est_surprise_diff_profit` cov 0.8224 aC=1、`estimate_surprise_difference_nprofit` cov 0.8596 aC=3）
是同机制的更拥挤版本，**只在 S4 的 prod 失败时作替补**，不并行投入。
