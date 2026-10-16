# USA 未点亮塔战役 · 最终战报（campaign_20261014）

> 日期：2026-10-14　区域：USA（严格锁定，未切换）
> 规模：**44 波 / 168 条回测 / 9 个数据集 / 103 个算子全量核验**
> 纪律：**全程零自动提交**；所有结论以平台回测读数为准。

---

## 一、目标达成情况（诚实账）

| 任务 | 状态 |
|---|---|
| 1. 数据集全面扫描（排除已点亮塔） | ✅ 286 个数据集全扫，93 个 alive；确认本季仅 model=4/analyst=1/earnings=1 点亮 |
| 2. 字段画像（4 个入选集 93 字段） | ✅ 数据类型/覆盖率/更新频率/拥挤度/机制逐字段画像 |
| 3. 构建并提交 10 个 regular alpha | ❌ **0 个提交**。最好候选距全闸仅差 1 个指标 |

**未达成原因**：USA 是全球最饱和市场，且本季已点亮 3 塔（model/analyst/earnings），
剩余未点亮塔中同时满足「月频流量 + 非存量 + 低拥挤 + 未点亮」四条件的数据集已全部穷尽。

---

## 二、★ 本战役最大突破：破 `LOW_2Y_SHARPE` 闸

此前 `2Y` 卡在 1.48（需 1.58）长达 20+ 变体，一度误判为「数据期不可救」。
最终通过论坛查证 + 算子穷尽找到解法：

### `winsorize(x, std=N)` 是 USA 低换手族的 2Y 杠杆

| 表达式（净招聘波动率） | S | F | 2Y | SUB | TO | margin |
|---|---:|---:|---:|---:|---:|---:|
| 无外层 `d5KXbPov` | 1.62 | 1.21 | 1.48 | 0.95 | 0.013 | 109bp |
| **`winsorize(·,std=3)` `rKdgpaPd`** | **1.85** | 1.06 | **1.63 ✓** | 0.70 | 0.045 | 18bp |
| `normalize(·)` `zqrMV2oV` | 1.82 | 1.04 | **1.65 ✓** | 0.68 | 0.043 | 19bp |
| **`tail`+`winsorize` `qMEr926K`** | **2.17** | **1.28** | 1.11 | **0.98 ✓** | 0.049 | 18bp |

**机制**：`winsorize` 压极端值 ⇒ 抑制「少数极端公司主导近期收益」（本族 = 2022-23 科技业裁员潮）
⇒ **2Y 1.48 → 1.63/1.65**。这是论坛 70 票帖 `rank_by_side` 的等效实现
（**`rank_by_side` 本账号无权限**，已在 103 算子清单中核实不存在）。

### `winsorize` vs `tail` 分工（本族实证）

| 算子 | 作用 | 方向 |
|---|---|---|
| `winsorize(std=N)` | **2Y ↑**（1.48→1.63），SUB ↓ | 保留全分布 |
| `tail(lower,upper,newval)` | **S/SUB ↑↑**（1.85→2.17 / 0.70→0.98），2Y ↓ | 只信极值 |

⇒ 两者**反向**，构成 USA workforce 族的机制性权衡墙。

---

## 三、最优候选池（均 `failed_ra_count=1`，仅差一个指标）

### 候选 A：`rKdgpaPd`（差 SUB 0.10）
```text
quantile(group_rank(winsorize(ts_std_dev(divide(subtract(vec_sum(employee_inflow_count),
    vec_sum(employee_outflow_count)), add(vec_sum(employee_inflow_count),
    vec_sum(employee_outflow_count))), 126), std=3), sector))
USA / TOP3000 / D1 / STATISTICAL / decay 10 / trunc 0.08
```
**S 1.85 ✓ / F 1.06 ✓ / 2Y 1.63 ✓ / SUB 0.70（需 0.80）/ TO 0.045 / margin 18bp / inv_S 1.88**

### 候选 B：`qMEr926K`（差 2Y 0.47）
```text
quantile(group_rank(tail(winsorize(ts_std_dev(...same..., 126), std=3),
    lower=0.2, upper=0.8, newval=0), sector))
```
**S 2.17 ✓ / F 1.28 ✓ / SUB 0.98 ✓ / 2Y 1.11（需 1.58）/ TO 0.049 / margin 18bp**

### 候选 C：`1Yj9r3pz`（差 SUB 0.10，2Y 略低）
S 1.84 / F 1.05 / 2Y 1.64 ✓ / SUB 0.70 —— 与 A 同族，轴 sector。

---

## 四、已判死清单（9 个数据集，勿重试）

| 腿 | 数据集 | 塔/mult | 最优 | 死因 |
|---|---|---|---|---|
| 1 | `short_interest_pred` | shortinterest/1.1 | S2.13/F0.54 | 日更字段 ⇒ TO 0.66，fitness 结构性不可达 |
| 2 | `twitter_sentiment_l2` | socialmedia/1.0 | S0.79/TO0.48–1.06 | 高频事件型，HIGH_TURNOVER |
| 3a | **`workforce_flow_skills`** | **other/1.4** | **S2.17/F1.28/SUB0.98** 或 **S1.85/2Y1.63** | ★ 机制成立，**2Y↔S/SUB 权衡墙** |
| 3b | `hiring_trends` | other/1.4 | S1.27/F0.85 | 3 闸；信号集中在单字段 |
| 4 | `institutions18` | institutions/1.0 | S0.92/F0.62 | 强度不足 |
| 5 | `macro27` | macro/1.1 | S0.92/F0.52 | 同机制、周频 ⇒ 信号更钝 |
| — | `macro63` | macro/1.1 | — | 3 个二元 flag，只能当分组轴 |
| — | `other551` | macro/1.1 | — | 33 字段全**日频** beta/R²/resret |
| — | `mfm_model_output` | risk/1.1 | — | 117 字段全**日频**行业暴露 |

---

## 五、本战役沉淀的 16 条方法论（已全部写入 skill）

| # | 结论 |
|---|---|
| 1 | **fitness = S × √(returns / max(TO, 0.125))** —— 39 颗 ACTIVE 验证，误差 0.2%；与论坛 `F = S×√(505×margin)` 互证 |
| 2 | **选集硬筛**：月频流量 + 比率形态 + 未点亮塔；**日更字段直接跳过**；**cov<0.65 反是优势** |
| 3 | **`SECTOR` = fitness/margin 杠杆**（F 1.28→1.41、margin 109→794bp）；`STATISTICAL` = prod 杠杆 |
| 4 | **`ts_std_dev`（波动率）> 水平值** = 「换算子 = 换机制」 |
| 5 | **对称化比率 `(a−b)/(a+b)` 优于 `a/(b+1)`**（SUB 1.38 vs 1.21） |
| 6 | ★ **`winsorize(std=N)` = 2Y 杠杆**；`tail` = S/SUB 杠杆（两者反向） |
| 7 | **`rank_by_side` 本账号无权限**（103 算子清单核实不存在）⇒ `winsorize`/`normalize` 等效替代 |
| 8 | **`winsorize` 必须写 `std=` 具名参数**；preflight 会误报 `unknown_fields:["std"]` ⇒ **preflight 误报 ≠ 不可用** |
| 9 | **`normalize` 无 `limit` 参数**（gate 明确报错） |
| 10 | **算子穷尽后 2Y 不动 = 数据期问题** —— 但**必须先试极值压缩类算子**再下此结论 |
| 11 | **「全期 Sharpe 正常、只挂 2Y」⇒ 高换手线换 RAM/CROWDING；低换手线（TO<0.05）换 neut 无效** |
| 12 | **`delay=0` 不可用 ⇒ 慢数据集无法靠鲜数据提 2Y** |
| 13 | **`ts_corr` 与净招聘比正交（0.84<0.7）⇒ 合法的同数据集双腿**（量 vs 节奏） |
| 14 | **两集同机制但更新频率不同 ⇒ 优先更新频率更高的**（workforce 日更 > macro27 周更） |
| 15 | **`ts_regression` 在本集是全零持仓毒算子** |
| 16 | **槽位饥饿表现为 progress 停在 0.1/0.15** ⇒ 改一个设置维度另起一批，勿原样重发（自相关互冲） |

---

## 六、下一步建议

候选 A/B 各差一个指标，**均未提交**。若要继续破闸，最可行的两条路：

1. **Mode B 组合腿**：`ts_corr` 腿（SUB 1.24，本族另一条正交腿）与波动率腿组合
   —— 合规（非 add），且两条腿互补（量 vs 节奏），有机会同时补 2Y 与 SUB。
2. **等平台数据期更新**：候选 A 的 S/2Y 都达标，只差 SUB 0.10；
   数据更新到 2024+ 年后 2Y 余量会增加，届时可换 SECTOR 中性化拿 SUB。

**提交权归用户** —— 所有候选均为 `UNSUBMITTED` 状态，未做任何提交动作。