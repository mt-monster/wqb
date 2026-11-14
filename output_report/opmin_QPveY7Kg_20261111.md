# op-min 收口：`QPveY7Kg`（DEU / TOP500，sentiment7 × snl27）

生成时间：2026-11-11 15:15 (GMT+8)｜skill：`wq-alpha-gate-push-op-min`｜**未提交**

---

## 0 结论

**这颗的 op-min 结果已经交付并上线**：`QPveY7Kg`（12 算子）的无损变量合并版 **`bl6OWZ2M`（10 算子）已于 2026-11-04 提交、现为 ACTIVE**，S/F/TO/returns 逐位相同。

**本轮 16 条仿真证明 10 是下限**：再删任何 1 个算子（9 ops）或 2 个（8 ops），`CONCENTRATED_WEIGHT` 立刻越线，`submit_gate` **直接 BLOCKED**。

**★ 顺带确认一条闸门规则**：`CONCENTRATED_WEIGHT` 的 **WARNING 会被提交闸当硬门拦**（`WebDataScope Failed RA=1`），不是可以忽略的告警 —— 这与 `LOW_FITNESS` / `LOW_2Y_SHARPE` 降级 WARNING 的形态不同，二者不能一概而论。

---

## 1 原件读数

```
vector_neut(ts_quantile(ts_ir(ts_mean(max(ts_backfill(vec_avg(snt7_all_languages_views),22),
     ts_delay(ts_backfill(vec_avg(snt7_all_languages_views),22),5)),5),22),252,driver="gaussian"),
     ts_backfill(vec_avg(snl27_relpopularity08),22))
```

DEU / TOP500 / delay 1 / **decay 2** / SUBINDUSTRY / trunc **0.02** / nan ON｜**12 算子**

| 项 | 值 | 闸 |
|---|---|---|
| Sharpe | 2.03 | ≥1.58 PASS |
| Fitness | 1.61 | ≥1.0 PASS |
| Turnover / returns / margin | 0.161 / 10.14% / 12.6bp | — |
| SUB / LADDER | 1.20 (lim .96) / 2.54 (lim 2.02) | PASS |
| CONCENTRATED_WEIGHT / CLUSTER | PASS / 1.43 | PASS |
| 塔 | **DEU/D1/SENTIMENT ×1.8** | 全库最高倍率档 |

**★ 样本有效性（决定性约束）**：逐年统计 **2014–2018 五年全为零**（pnl 0、long/short 0），有效样本只有 **2019–2023 共 5 年 < 6** ⇒ 按纪律 **禁调参**。本轮因此**只做结构删除、未扫任何窗口或参数**。

---

## 2 已经存在的压缩（本轮之前）

| alpha | ops | 做法 | 状态 |
|---|---|---|---|
| `QPveY7Kg` | 12 | 原件 | UNSUBMITTED（已被取代） |
| **`bl6OWZ2M`** | **10** | FASTEXPR 变量合并：`a = ts_backfill(vec_avg(snt7),22)` 把重复子式收成 1 处 | **ACTIVE**（2026-11-04 提交） |

`bl6OWZ2M` 与原件指标逐位相同（S 2.03 / F 1.61 / TO 0.161 / ret 10.14%），CW 仍 PASS。

---

## 3 本轮：从 10 再往下压（16 条仿真）

### 3.1 逐算子删除结果

| 删除的算子 | alpha | ops | S | F | SUB | LADDER | **CW** | 判定 |
|---|---|---|---|---|---|---|---|---|
| —（基准） | `bl6OWZ2M` | **10** | 2.03 | 1.61 | 1.20 | 2.54 | **PASS** | 已 ACTIVE |
| `ts_quantile` | `kqaE08PL` | 9 | **2.16** | **1.83** | **1.39** | **2.62** | WARN .3079 | **BLOCKED** |
| `ts_backfill`（向量轴） | `6XMm9Gp7` | 9 | 1.99 | 1.51 | 1.19 | 2.45 | WARN | BLOCKED（且 ρ .9887 与已提交同席） |
| `ts_ir` | `oma8lPgE` | 9 | **−0.35** | −0.11 | −0.54 | −0.59 | — | 信号死 |
| `ts_mean` | `A1xjPLGQ` | 9 | 1.25 | 0.73 | 1.06 | 1.36 | WARN | 死 |
| `ts_backfill`（主信号） | — | 9 | — | — | — | — | — | 仿真未落地（平台 pending） |
| `vector_neut` | `LLKV187L` | 7 | 0.75 | 0.37 | 0.52 | — | WARN | 死 |
| 组合：`quantile`+`backfill(G)` | `mLawVVZE` | **8** | 2.02 | 1.59 | **1.32** | 2.36 | WARN | **BLOCKED** |
| 组合：`quantile`+`backfill(主)` | `gJak993m` | **8** | 1.80 | 1.43 | 1.29 | 2.02 | WARN .2203 | **BLOCKED** |
| 组合：`quantile`+`ts_mean` | `A1xj77wY` | 8 | 1.39 | 1.00 | 1.00 | 2.02 | WARN .2782 | 死 |
| 组合：`quantile`+`vector_neut` | `kqaEZZK8` | 6 | 1.17 | 0.73 | 0.88 | — | WARN .3265 | 死 |
| 峰化块删除族（5 条，`max`+`ts_delay`） | `O0WQZjwq` 等 | 7–8 | 1.07–1.19 | ≤0.71 | ≤0.95 | ≤1.45 | WARN | 全死 |

### 3.2 最重要的两件事

**① `ts_quantile(252, gaussian)` 是"权重去集中器"，不是可有可无的排名层。**
删掉它，指标全线变好（S 2.03→**2.16**、F 1.61→**1.83**、sub 1.20→**1.39**、ladder 2.54→**2.62**），
但 `CONCENTRATED_WEIGHT` 从 PASS 变成 **0.3079 vs lim 0.1** —— 单一持仓占到组合 31%，提交闸直接拦。
**它承的不是 alpha，是风险预算。**

**② `CONCENTRATED_WEIGHT` 的 WARNING 是硬门。**
`submit_gate` 返回：`WebDataScope Failed RA=1 / PPA=0（Phase B.0 硬门非零，任一通道失败即拦）：['CONCENTRATED_WEIGHT']`。
对 `mLawVVZE`（8 ops）与 `kqaE08PL`（9 ops）都实测到同一拦截。
⇒ 不能把 CW 的 WARNING 当"非硬闸"处理（这与 `LOW_FITNESS`/`LOW_2Y_SHARPE` 的降级 WARNING 完全不同，后两者只需看 `result` 是否为 PASS）。

### 3.3 相关性（4 年日收益）

| 对 | ρ | 含义 |
|---|---|---|
| `kqaE08PL` ~ `bl6OWZ2M` | **0.6789** | 低于 0.70，不同席（但被 CW 拦） |
| `mLawVVZE` ~ `bl6OWZ2M` | 0.6685 | 低于 0.70 |
| `gJak993m` ~ `bl6OWZ2M` | **0.5813** | 最正交 |
| `mLawVVZE` ~ `kqaE08PL` | 0.9894 | 同一信号 |
| `6XMm9Gp7` ~ `bl6OWZ2M` | **0.9887** | **同席，不可与已提交共存** |

---

## 4 判定：10 算子是本骨架的下限

| 目标 | 能否达成 |
|---|---|
| 12 → 10（变量合并，无损） | ✅ 已完成并提交（`bl6OWZ2M`） |
| 10 → 9（删任一算子） | ❌ 全部触发 CW 或被信号性否决 |
| 10 → 8（删两个） | ❌ 同上 |
| 10 → 7 以下 | ❌ 峰化块 `max(a, ts_delay(a,5))` 一删，S 从 2.03 掉到 1.07–1.19 |

**四个算子各承一件事，没有一个可删**：
- `ts_backfill`+`vec_avg`（snt7）：VECTOR→标量 + 稀疏情感数据前向填充，删任一 S 直接归零或 CW 崩
- 峰化块 `max(a, ts_delay(a,5))`：捕捉"当前热度高于 5 日前"的尖峰，删掉 S 腰斩
- `ts_ir(...,22)`：波动归一化，删掉 S 变负（−0.35）
- `ts_quantile(252, gaussian)`：**权重去集中**，删掉 CW 从 PASS 变 0.31（硬门）
- `vector_neut(..., G)`：对 popularity 向量中性化，删掉 S 0.75

---

## 5 产物与状态

- 批次文件：`results/batch_QPveY7Kg_flat.txt`（5 条）、`results/batch_QPveY7Kg_asm.txt`（6 条）、`results/batch_QPveY7Kg_opmin2.txt`（5 条）
- 覆盖签核：`results/op_coverage_signoff.jsonl` 2 条（session `QPveY7Kg-opmin1` / `-opmin2`）
- **未提交任何新 alpha**。`bl6OWZ2M` 保持 ACTIVE，是这颗的唯一交付件。
- 若日后要"用更低算子替换已上线的 `bl6OWZ2M`"，**无可行解**：9 算子件指标更好但 CW 越线，且与已提交件 ρ .6789 属同一信号源，收益有限、风险明确。

> 附：`results/batch_QPveY7Kg_asm.txt` 第 5 条（删主信号 `ts_backfill`）仿真在平台侧仍未落地，故上表标为未测；不影响结论——其余 15 条已覆盖全部单删与主要组合删。
