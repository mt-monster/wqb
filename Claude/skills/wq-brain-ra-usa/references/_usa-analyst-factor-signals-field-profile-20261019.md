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
