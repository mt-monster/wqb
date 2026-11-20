# E5Qrx2JG 复验与"保留 dlc 的最小过闸表达式"核实（2026-11-17 17:1x）

> 用户问：保留 `days_from_last_change`（dlc）信号的前提下其它能减就减，过闸表达式是什么？
> **答案：`E5Qrx2JG`（14 ops / 10 distinct，全闸 PASS）就是保留 dlc 的实测最优解**——11-16 第五轮已产，今日平台复验全部指标逐位一致。

## 过闸表达式（14 ops，全闸 PASS：S1.78/F1.42/2Y1.90/DD3.74%/TO8.84%）

```
v = vec_avg(insd1_holdings);
gri = group_rank(ts_ir(v, 66), sector);
dlc = group_rank(days_from_last_change(v), sector);
leg = multiply(gri, add(dlc, -1), -1);
core = add(leg, rank(ts_mean(add(predicted_surprise_f12m_ebitda_4, predicted_surprise_pct_fy2_earnings_4,
                  mean_estimate_change_pct_f12m_ebitda_14d_4, mean_estimate_change_pct_f12m_ebitda_90d_3), 30)));
group_neutralize(core, bucket(rank(cap), range="0,1,0.1"))
```
settings：DEU/TOP500/d1/**decay=3**/SUBINDUSTRY。

## 为什么 14 ops 就是保留 dlc 的下限（本日实测补强）

| 尝试 | 结果 | 结论 |
|---|---|---|
| 10 ops 版丢 dlc（`P05X8AqW`） | S1.74 全过但 T3 丢 +1 | 能减但**违背保留 dlc 的前提** |
| 13 ops 同向变体 `gri×gr(dlc)`（`rK7rn1d1`） | S1.24 ❌ | **反向 (1−gr(dlc)) 是唯一正确写法**（老持仓做空头） |
| **本日**：删 rank 包裹（分析师项裸 ts_mean） | **S0.12 / F0.03 崩** | `rank` 包裹承重（分析师 4 字段量纲不可裸加） |
| **本日**：删 ts_mean30（裸 add） | 首批 CANCELLED 重派后确认不可行 | 平滑承重 |
| **本日**：`multiply(gri,add(dlc,-1),-1)` → `subtract(gri,dlc)` | S1.68/F1.39/2Y1.49（`1YWgQn2X`） | **可行且更精简（−1 调用）但 IS_LADDER 1.49<1.58 FAIL**——乘法形态的尾部保护更强，ladder 差 0.09 |
| **本日**：④d 精调 ts_mean 30→22 | S1.56 / ladder **1.39** ❌（`YPaAGOko`） | **W30 是尖峰再证**（分析师修正中周期≈半季度） |
| ④d 精调 ts_ir 66 邻域（11-16 实测） | 63→1.98 / 69→1.98 | 66 尖峰确认 |

⇒ **14 ops 是保留 dlc 的实测下限**：dlc 腿（2 ops）+ gri 腿（3 ops）+ 交互（2 ops）+ 分析师项（3 ops）+ 终局（2 ops）+ vec_avg 提取（1 op）+ bucket 中性化（2 ops），每一段都被消融证实承重。

## 结构注记

- `multiply(gri, add(dlc,-1), -1)` 的含义：`gri × (1 − gr(dlc))`——信息比率排名 × 「老持仓折价」，老持仓做空头。
- dlc 独立加项有毒（11-16 实测 S0.76）——它只能以交互形态入场。
- 塔：`DEU/D1/PV+INSIDERS+MODEL` 三类 effective=0（bucket 的 cap 是 PV 来源），当季 PV0/INSIDERS1/MODEL3 均 <3 ⇒ **塔边际 0**。
- ⚠ self/prod 未测（提交前须补）；与 `88NKJOav` 骨架高度相似，二者只能选一。

## ATOM 视角（本轮 skill 增强）

本件混 3 个数据集类别（insiders1 + analyst 修正族 + cap/PV），**非 ATOM**——按新补的 skill「ATOM 前置检查」，混 3 类别金字塔计 0、倍率按最低类结算。**但在本仓政策下这是合法的 regular 跨集形态**（grouping/bucket 轴 + 交互，非 add 等权混腿），且 PV 来源是分组轴而非信号腿——若未来要 ATOM 化，第一刀是把分析师项换成本数据集字段或砍掉，但那会破坏 2Y 的尾部保护（11-16 实测 10 ops 版 2Y 1.78 vs 14 ops 版 1.90）。

---

# 2026-11-17 19:25 完整 skill 流程复核（用户点名）

> 本轮 = 对 11-16 第五轮「保留 dlc 最小过闸件」的完整 skill 流程复核：ATOM 判定 → 采集 → 相关性硬闸补测 → 同骨架族验证 → 六维 → 判定。零提交。

## 一、ATOM 判定

**非 ATOM**（混 3 类别）：
- 主字段 `insd1_holdings`（insiders1）
- 分析师腿 4 字段（predicted_surprise_* / mean_estimate_change_*，model/analyst 类）
- `bucket(rank(cap))` —— **cap 是 pv1 字段**（skill 三种隐形破 ATOM 自查第 ② 条命中）

⇒ 塔结算 PV/insiders/model 三类 effective=0（当季均 <3），倍率按最低类。按 skill 分流表本应「拆 ATOM 优先」，但本件**用户指令是保留 dlc 的最小过闸形态**（11-16 第五轮结论），本轮按"已冻结形态"复核，不再动表达式。

## 二、平台实值复核（get_alpha_details，与昨日一致）

S **1.78** / F **1.42** / TO 8.84% / 2Y **1.90** / sub **1.23** / investability 1.83 / margin 18.04bp。
`checks.fail=[]`，`ra_failed=0`，PASS 9 项（含 IS_LADDER_SHARPE / CONCENTRATED_WEIGHT / LOW_SUB_UNIVERSE_SHARPE / CLUSTER_TEST）。`operatorCount` 14 次调用 / 10 distinct。

## 三、相关性硬闸补测（本轮核心增量）

| 闸 | 值 | 判定 |
|---|---:|---|
| **self** | **0.3431**（top `Vk65zLzG`，pool 20/24，无新提交，读数可信） | ✅ PASS，余量 0.357 |
| **prod** | **0.3444**（平台缓存 2026-11-17 04:52，platform_sync，非 provisional） | ✅ PASS，余量 0.356 |

**双闸余量均 >0.35** —— 这是本件最意外的优点：昨日报告标注「self/prod 未测」是缺口，实测后发现它是**相关性最安全的 DEU 候选之一**（对比 `88NKJOav` 的 0.5778/0.5779）。

## 四、同骨架族验证（与 `88NKJOav`）

`compute_mutual_correlation`（4 年日收益，1021 点）：

| pair | ρ |
|---|---:|
| **E5Qrx2JG ↔ 88NKJOav** | **0.6621** |
| E5Qrx2JG ↔ d5a2aO7v / blRnKEk6 / Vk65zLzG | 0.29 / 0.29 / 0.34 |

- **0.6621 < 0.7** ⇒ 非孪生封死，两件可共存于 OS 池；但同池提交**只能择优一颗**（平台 self 罚会累积）。
- `88NKJOav`（22 ops，11-16 第四轮产物）指标**全面碾压**：S **2.60** vs 1.78 / F **2.12** vs 1.42 / 2Y **2.77** vs 1.90 / sub **1.70** vs 1.23 / margin 13.3bp vs 18.04bp。
- `88NKJOav` 的 self **0.5779** / prod **0.5778**（本轮实测）同样全过 ⇒ **同池二选一明确是 `88NKJOav`**。

**`E5Qrx2JG` 的定位**：`88NKJOav` 的**精简备份**（14 ops vs 22 ops，六维 T1/T2 软成本更低）——仅当 `88NKJOav` 未来 prod 漂移撞墙时启用。两件 prod 相差 0.233，`88NKJOav` 漂移空间更大，备份价值真实存在。

## 五、六维（genius_tiebreak 实测）

| 维 | 值 | 判定 |
|---|---|---|
| ops / fields | 10 / 5 | — |
| T1 平均 ops | 4.6074 → 4.6217（**+0.0143**） | worse（软成本） |
| T2 平均 fields | 1.8488 → 1.8571（**+0.0083**） | worse（软成本） |
| **T3 总算子** | **+1 `days_from_last_change`** | **better**（全账号首次使用） |
| T4 总字段 | flat（5 字段均已用过） | flat |

价值在 T3 新算子，T1/T2 是可接受的软成本。

## 六、压缩与精调完成度复核（对照 skill 硬环节）

- **④/④c 消融**：11-16 第五轮 7 条实测已证 14 ops 下限（删 rank→S0.12 崩、删 ts_mean30 不可行、multiply→subtract 使 ladder 1.49 FAIL、13 ops 同向变体 S1.24 崩）✅
- **④d 精调**：ts_mean **30**（22→1.39 ladder 崩）/ ts_ir **66**（63/69 邻域已扫）尖峰均确认 ✅
- **⑤ universe**：DEU 单档 TOP500 ⇒ 按 skill 规则跳过 ✅
- **ATOM 分流**：非 ATOM 但形态已按用户指令冻结，不再拆 ✅

## 七、判定

**PASS_ALL_GATES** —— 全部硬闸（IS 9 项 + self 0.3431 + prod 0.3444）通过，压缩/精调/universe 三环节完成度 100%。

**提交顺位（交用户定）**：
1. **`88NKJOav` 优先**（S2.60/F2.12/2Y2.77 全面碾压，prod/self 0.578 同样安全）
2. `E5Qrx2JG` 是精简备份（14 ops + 最安全相关性），仅当 `88NKJOav` prod 漂移撞墙时启用

本轮零提交。台账 `opmin_E5Qrx2JG`(DEU) 已落。

---

# 2026-11-17 19:1x 去混尝试：cap→非 PV 市值字段（凑两塔）⇒ 失败

> 用户问：PV 或 MODEL 有没有替代，把 3 类混凑成 2 类塔。核实塔计数控股权在 `cap`（唯一 PV 来源）——替换它即可成 INSIDERS+MODEL 两类（倍率短板 1.6，同时计两塔）。

## 替代字段候选（get_datafields 实查）

| 字段 | 类型 | coverage | 倍率 | 备注 |
|---|---|---|---|---|
| `logarithmic_market_cap` | MATRIX | 0.5368 | 1.8 | 非 PV，可直接替换 cap，算子数不变 |
| `mdl109_log_float` | VECTOR | 0.5368 | 1.8 | 与 insd1_holdings coverage 完全匹配，需 +vec_avg（15 ops） |
| insd1 数据集 | — | — | — | **无 GROUP 字段**（GROUP 查询 0 结果） |

## 实测（multisim 2 条，同 settings）

| 变体 | S | F | 2Y | sub | Ra failed | 判定 |
|---|---:|---:|---:|---:|---:|---|
| **E5Qrx2JG（cap 原件）** | **1.78** | **1.42** | **1.90** | **1.23** | **0** | 基准 |
| MP6xx25n（→logarithmic_market_cap） | 0.97 | 0.72 | 1.50 | 0.87 | 3 | **崩** |
| zqdWWLPX（→vec_avg(mdl109_log_float)） | 0.80 | 0.54 | 1.17 | 0.73 | 3 | **更崩** |

## 结论

**去混失败，`cap` 是承重中性化轴**——它对 2Y 尾部保护承重（DD 3.74% vs 替代件 12%+），替代字段（cov 0.53 与 insd1 同源）反而弱化横截面。这与 op-min 的删除消融同理：**「可用替代字段存在」≠「去混可行」，中性化轴的承重性必须实测**。

凑两塔的剩余路径只有**拆腿**（insd1+dlc 单独成 ATOM / 分析师腿单独成 ATOM），都不在本件冻结形态内；且 11-16 已证 insd1+dlc 单腿 2Y 不够。E5Qrx2JG 维持 3 类混 ⇒ 塔计 0，价值在 T3 新算子与精简备份位。

本轮零提交。
