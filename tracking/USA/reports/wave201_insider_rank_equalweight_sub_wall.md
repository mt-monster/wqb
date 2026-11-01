# 波 201：`insider_trx_matrix` × `group_rank` 等权化强度扫描 —— SUB/S 比值是唯一真墙

- **日期**：2026-10-29
- **multisim**：`3hRdZy8BH58H8CcJwPIAGYv`（10/10 COMPLETE）
- **数据集**：`insider_trx_matrix`（USA / OTHER 塔 / 平台 alphaCount = 1）
- **设置**：`USA / TOP3000 / D1 / decay=5 / SLOW_AND_FAST / trunc=0.08 / nanHandling=ON / pasteurization=ON / maxTrade=OFF / unitHandling=VERIFY`
- **设置选择理由**：与 B 档冠军 `0mjaa2Ev` 完全一致，确保本波与「已过闸的 OTHER 候选」之间是**单变量对照**（只换外层几何）。

## 科学问题

波 199 得到两条互相拉扯的发现：

- **发现 A**：`ts_sum` 累积是换手控制器 —— 日频原始水平 S 9.19 / TO 141%，加 `ts_sum(...,63)` 后 S 3.73 / TO 16.27%。
- **发现 B**：`group_rank` 是 `invest_ratio` 的 7.7× 杠杆 —— 0.0831 → 0.6385，同时 TO 16.27% → 6.56%，代价 S 3.73 → 1.30。

本波问的是：**等权化强度能否找到 S 与 invest_ratio 的双解点？** 统一基础信号 `mean_secondary_buy_transaction_count`，外层全部用 `group_rank`，只在时间变换 / 非线性 / 分组轴上做结构性区分。

## 结果总表

| # | 模板（差异维度） | alpha | S | F | TO | 2Y | SUB | SUB limit | **SUB/S** | invest_S | fRA |
|---|---|---|---|---|---|---|---|---|---|---|---|
| T1 | 无时间变换（纯横截面） | `omEQ8QLn` | 3.34 | 1.37 | 47.45% | 3.66 | 0.58 | 1.45 | 0.174 | −0.26 | 1 |
| T2 | 时间 rank × 横截面 rank | `WjOK1Kbx` | 2.69 | 1.00 | 47.29% | 3.05 | 0.24 | 1.16 | **0.089** | −0.32 | 1 |
| **T3** | **时间 zscore × 横截面 rank** | **`pwdQYQ5X`** | **5.37** | **3.31** | **47.97%** | **5.30** | **1.56** | **2.33** | **0.291** | **0.34** | **1** |
| T4 | winsorize(std=4) 去极值 | `vR1awa2d` | 5.37 | 3.31 | 47.97% | 5.30 | 1.56 | 2.33 | 0.291 | 0.34 | 1 |
| T5 | ts_decay_linear 信号值平滑 | `P0ojQjgK` | 5.29 | 3.26 | 47.84% | 5.20 | 1.49 | 2.29 | 0.282 | 0.29 | 1 |
| T6 | hump(1e-4) 阈值换手抑制 | `j2YNzNeQ` | 5.37 | 3.31 | 47.98% | 5.29 | 1.56 | 2.33 | 0.291 | 0.34 | 1 |
| T7 | 分组轴 = 市值桶 | `1YN6k6jX` | 5.06 | 3.07 | 48.36% | 4.90 | 1.51 | 2.19 | 0.298 | 0.16 | 1 |
| T8 | 位移算子 ts_av_diff | `58ENnNEo` | 3.29 | 1.53 | 49.14% | 3.50 | 0.99 | 1.42 | **0.301** | 0.01 | 1 |
| T9 | 二阶矩 ts_std_dev | `mLoeweo6` | 0.48 | 0.14 | 13.45% | 0.24 | 0.05 | 0.21 | 0.104 | 0.11 | **4** |
| T10 | 分组轴 = subindustry | `88Rg5gNm` | 4.17 | 2.21 | 48.09% | 4.53 | 1.15 | 1.81 | 0.276 | −0.01 | 1 |

**对照组（已过闸，来自波 196–198）**：`0mjaa2Ev` `group_neutralize(ts_zscore(ts_sum(total_top_secondary_buy_transaction_count,126),252), sector)` → S 3.24 / F 2.60 / TO 16.22% / 2Y 4.30 / **SUB 1.40 / S 3.24 = 0.432 ✅ 过闸** / prod 0.6460。

## 三条核心结论

### 1. ★★★★★ SUB limit 精确等于 `0.434 × S` —— 要优化的是比值不是绝对值

10 条实测 `limit / S` 全部落在 **0.431–0.438**：

```
1.45/3.34 = 0.434    1.16/2.69 = 0.431    2.33/5.37 = 0.434
2.29/5.29 = 0.433    2.19/5.06 = 0.433    1.42/3.29 = 0.432
0.21/0.48 = 0.438    1.81/4.17 = 0.434
```

⇒ **提高 S 会同比抬高 SUB 门槛**。`pwdQYQ5X` 的 S 5.37 是全 USA 区历史最高一档，但它的 SUB 门槛也随之抬到 2.33。**「把 S 堆高」在 SUB 闸面前是零和**。真正要追的是 `SUB/S ≥ 0.434` 这个比值。

这与波 199 的 `wpQX8vj2`（S 3.73 → limit 1.62 = 0.434）完全一致，**该系数跨波次、跨骨架稳定**。

### 2. ★★★★★ SUB/S 三层规律：横截面操作越**多**，SUB/S 越**差**

> ⚠ **本节曾于 2026-10-29 23:05 纠正**。初版把功劳归给 `group_neutralize`，随后核对 B 档 6 颗已过闸候选的真实表达式才发现：它们**根本没有 group 外层**。真正的自变量是「有没有横截面操作」以及「横截面操作有多强」。

| 外层几何（由弱到强） | 代表 alpha | S | SUB/S | 过闸？ |
|---|---|---|---|---|
| **无外层**：裸 `ts_zscore(ts_sum(F,W),252)` | `vROPEJ8w` | 2.08 | **0.630** | ✅ |
| 无外层（同上，另一字段/窗口） | `1Yj08nb6` | 1.58 | 0.595 | ✅ |
| 无外层 | `XgRM3Yra` | 1.66 | 0.584 | ✅ |
| 无外层 | `O0Jgd7Y7` | 2.27 | 0.537 | ✅ |
| 无外层 | `88vXxaqv` | 1.99 | 0.447 | ✅ |
| `group_rank` + `winsorize(std=2)` + `tail(0.2,0.8,0.5)` | `d5KzLo7v` | 2.93 | 0.440 | ✅（靠截尾救回） |
| `group_neutralize(..., sector)` | `0mjaa2Ev` | 3.24 | 0.432 | ✅ 卡线 |
| `group_rank(ts_zscore(F,252), sector)` | `pwdQYQ5X` | 5.37 | 0.291 | ❌ |
| `group_rank(..., subindustry)` | `88Rg5gNm` | 4.17 | 0.276 | ❌ |
| `group_rank(F, sector)` | `omEQ8QLn` | 3.34 | 0.174 | ❌ |
| `group_rank(ts_rank(F,252), sector)` | `WjOK1Kbx` | 2.69 | 0.089 | ❌ |

**机理**：`ts_zscore` 的幅度加权让权重集中在极端 z 值上，这些极端值天然偏向事件驱动的小票。任何横截面归一都在**抹平幅度加权**：

- `group_neutralize`（行业内去均值）只抹掉水平项，保留幅度 ⇒ SUB/S 从 0.44–0.63 掉到 0.432，**只掉一点点**；
- `group_rank`（行业内等权重排）抹掉整个幅度分布 ⇒ SUB/S 塌到 0.09–0.30，**掉一半以上**。

S 之所以在 `group_rank` 下反而涨（2.08 → 5.37），是因为等权化让收益分散到全宇宙、波动更低，但**收益来源从「大票事件」变成了「全宇宙事件」，SUB 侧被稀释**。

**⇒ 破 SUB 墙的正确方向是【减】横截面操作，不是【加】。** 波 201 的设计前提（以为等权化能救 invest_ratio 而不伤 SUB）从根上就错了 —— `invest_ratio` 与 `SUB` 对大票暴露的要求本来就是相反的（见 §3）。

### 3. ★★★ invest_ratio 与 SUB 对大票暴露的要求相反 —— 不存在双解

| alpha | invest_S | SUB | 谁赢 |
|---|---|---|---|
| `pwdQYQ5X` | **0.34**（好） | 1.56 / 2.33（差） | invest_ratio |
| `88Rg5gNm` | **−0.01**（差） | 1.15 / 1.81（差） | 双输 |
| `0mjaa2Ev`（对照） | 0.0895（差） | 1.40 / 1.45（过） | SUB |

`group_rank` 提 `invest_ratio`（发现 B 成立）但降 `SUB/S`（本波成立）。而 `invest_ratio` 是**自设闸**（平台 `checks.fail` 不含该项，USA 未下发 `LOW_INVESTABILITY_CONSTRAINED_SHARPE`），`SUB` 是**平台硬闸**。⇒ 若要二选一，**必须保 SUB**。

## 四条副产物结论

### 4. `group_rank` 是全族最好的换手杠杆（141% → 48%，3×）

- `QPvm1o3r`（`group_neutralize(ts_zscore(F,252), sector)`）→ S 9.19 / **TO 141.22%**
- `pwdQYQ5X`（`group_rank(ts_zscore(F,252), sector)`）→ S 5.37 / **TO 47.97%**

代价 S 打 42%，换来 F 3.31 / 2Y 5.30 —— 是波 199 以来最强的一组硬指标。**`group_rank` 的正确用途是压 TO 与提 invest_ratio，不是过 SUB。**

### 5. 等权化之后 `winsorize` 与 `hump` 完全失效（结构不变性验证）

`pwdQYQ5X`（纯 ts_zscore）/ `vR1awa2d`（winsorize std=4）/ `j2YNzNeQ`（hump 1e-4）三条**产出逐位近乎相同的指标**：

```
S    5.37 / 5.37 / 5.37
TO   47.97% / 47.97% / 47.98%
SUB  1.56 / 1.56 / 1.56
```

⇒ 等权化已经把分布压平，没有极端值可截、没有微小变动可 hyster 掉。**在 `group_rank` 内层做非线性处理是空操作**，应在 `group_rank` **外层或之前**做。

### 6. `bucket(rank(cap))` 分组会引入 PV 塔 —— 合规不可用

`1YN6k6jX` 的 `pyramid_short = "pv/other"`，2 塔。按「PV / MODEL / OTHER 三塔之间禁止两两混合」硬约束，**即便 SUB/S 0.298 也不可用**。⇒ 该数据集任何用 `cap` 做分组的模板一律排除。

### 7. 二阶矩再次确认无信号（第三次）

`mLoeweo6`（`ts_std_dev(F,22)`）S 0.48 / F 0.14 / SUB 0.05 / **fRA = 4**。与波 200 N5（`finnews_nlp_scores` 离散度二阶矩，S −0.01）方向一致 ⇒ **该数据集的信号全在一阶矩**。

### 8. 分组轴 sector → subindustry 是负增量

`88Rg5gNm`（subindustry）S 4.17 / SUB/S 0.276，全面劣于 `pwdQYQ5X`（sector）S 5.37 / 0.291。与波 199 结论一致。

## 判死与后续

- **判死条目已落库**：`USA-INSIDER-RANK-EQUALWEIGHT-SUB-DEAD`（`registry_empirical` / `layer=dead_end`）。
- **判死范围**：仅 `group_rank` 等权化路线。`group_neutralize` 路线（B 档 6 颗）**不受影响，仍可提交**。
- **未测 / 在测的破墙路径**（按理论依据强弱排序）：
  1. **✅ 已经验证过的正解：干脆不加横截面外层**。B 档 6 颗裸 `ts_zscore(ts_sum(F,W),252)` 的 SUB/S = 0.447–0.630，全部过闸。这条不是假设，是已提交资产。
  2. **🔄 在测：`group_rank` 下扫平台 decay**（同一表达式 × decay ∈ {8,10,12,15}，已派发）。逻辑：TO 从 47.97% 降下来时 S 会降、SUB limit 同比降，若 SUB 降得比 S 慢则比值上升。**这是唯一还能救 `group_rank` 路线的实验**。
  3. **✅ 已验证的补丁：`group_rank` 后接截尾中位化**。`d5KzLo7v` 用 `tail(winsorize(group_rank(...), std=2), lower=0.2, upper=0.8, newval=0.5)` 把 SUB/S 从 0.29 量级救到 **0.440**，代价是 S 被压到 2.93 但 TO 只剩 48.55%→ 实际该条 TO 偏高需另治。⇒ **如果非要 group_rank，必须配套截尾。**
  4. 若 (2) 也失败 ⇒ `group_rank` 路线在该数据集判定为**结构性不可过 SUB**，全族停止；但**裸 zscore 路线不受影响，已产出 6 颗可提交候选**。

## 与 B 档提交资产的关系

本波**不改变** B 档 6 颗的提交资格 —— 它们是 `group_neutralize` 路线、`failed_ra_count = 0`、prod 全部 < 0.70。本波只是把「`group_rank` 路线」这条支路封掉，避免后续继续在上面浪费仿真槽。
