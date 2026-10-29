# 波 172 — RISK 塔 `mfm_model_output` 12 模板结构消融

**日期**：2026-10-30
**区域 / 设置**：USA / TOP3000 / D1 / INDUSTRY / decay 0 / truncation 0.05 / nanHandling ON / pasteurization ON / maxTrade OFF / 2014-01-01 ~ 2023-12-31
**数据集**：`mfm_model_output`（category=RISK，117 字段全 MATRIX，coverage 0.9963，alphaCount 仅 308，valueScore 3.0）
**塔位**：平台实测 `pyramid_short = "risk"`、`pyramids.list = [{name: "USA/D1/RISK", multiplier: 1.1}]`、`checks.pass` 含 `MATCHES_PYRAMID`
**批次**：multisim `3gbHfT2xf4ic98P4kNrWsRv`（T1–T6）+ multisim `3FAPPobnF4PzaM28XDVvotl`（T7–T12），12/12 COMPLETE，0 error
**结论**：**PARTIAL** — n_pass = 0，n_near = 3

---

## 1. 为什么选这个数据集

RISK category 7 个数据集的拥挤度对比（`get_datasets` + `query_dataset_profile`）：

| dataset | fields | coverage | alphaCount | valueScore | 已测 |
|---|---|---|---|---|---|
| `risk70` | 158 | 0.9971 | **82,093**（极度饱和） | 1.0 | 158 untested |
| `risk62` | 636 | 0.9988 | 23,601 | 1.0 | 636 untested |
| `risk72` | 3 | 0.6956 | 2,408 | 1.0 | 2 untested / 1 unusable |
| `risk60` | 5 | 1.0 | 1,984 | 1.0 | 22 回测 / 4 ra_pass |
| `risk65` | 6 | 0.9743 | 411 | **3.0** | 6 untested |
| **`mfm_model_output`** | **117** | **0.9963** | **308** | **3.0** | **0/117 已挖** |
| `risk59` | 16 | 0.9806 | 82 | 1.0 | 16 untested |

`mfm_model_output` 的 `alphaCount = 308` 在整个 RISK category 里是第二低（仅次于 `risk59` 的 82），却有 117 个字段与满分 valueScore 3.0，且**全库 0 次回测**。这是典型的「低拥挤 + 高供给」组合，是打未点亮 RISK 塔的首选。

字段画像详见 `docs/reference/USA/mfm_model_output_field_profile.md`（11,186 字节，7 章）。

---

## 2. 字段结构（117 → 4 个候选信号字段）

画像阶段把 117 字段切成 4 类，只有 2 个字段被判定携带信号：

| 类 | 数量 | 代表字段 | 判定 |
|---|---|---|---|
| 风格/维度因子 | 13 | `hedge_fund_ownership_factor0`(94/155 最拥挤)、`discount_store_retail_score`(26/43)、`short_interest_factor_score_2`(24/30) | 逐字段实测（本次重点） |
| 行业暴露 score | 61 | `industry_*_score` | **不可做信号**（数学上等价行业哑变量，`group_rank` 组内近常数，且已被 INDUSTRY 中性化吃掉；45 个字段 userCount=0） |
| 行业二元 flag | 43 | `industry_*_flag`（7 个 coverage 0.9377） | **不可做信号**（同上，且二值化后组内几乎全同） |
| 系统性风险 | 1 | `systemic_risk_measure_2`(3/4) | 实测 |

**两个致命命名陷阱（本轮最重要的字段理解）**：

- `discount_store_retail_score` — 名字像「折扣零售板块」，**实为 Daily specific (idiosyncratic) returns = 残差/特异日收益（%）**。
- `systemic_risk_factor_score` — 名字像「系统性风险」，**实为 Specific risk matrix per stock per day, annualized percent-squared = 特质方差 σ²_idio（%²）**，即 "systemic" 应为 "specific"。

真正的系统性风险贡献是 `systemic_risk_measure_2`。**若不看 description 只按字段名组 idea，会把这三个字段的机制全部搞反**——这正是「用字段名规律 + 字段描述找经济学关系」这条准则的反向应用：名字规律会骗人，description 才是权威。

---

## 3. 12 条模板与结果

`SR` = `systemic_risk_factor_score`（特质方差 σ²_idio）
`R` = `discount_store_retail_score`（残差日收益）
`bf(x,W)` = `ts_backfill(x, W)`

| # | 字段 | 模板结构 | alpha | S | F | TO | R | DD | 2Y | SUB | margin | invest_S | risk_neut_S | fRA |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| T1 | σ²_idio | `group_rank(reverse(bf(SR,22)), industry)` 水平反转 | `9qxowLw9` | 0.22 | 0.09 | 19.16% | 2.90% | — | 0.53 | 0.06 | 0.30bp | 0.22 | −0.66 | 4 |
| T2 | σ²_idio | `group_rank(ts_rank(bf(SR,22),252), sector)` 时序分位 | `j2YLZb05` | −0.16 | −0.02 | 42.70% | −0.80% | — | 0.02 | 0.04 | −0.04bp | −0.32 | 0.88 | 3 |
| **T3** | **R** | **`group_rank(reverse(ts_sum(bf(R,22),22)), industry)` 累加反转** | **`9qxowLr9`** | **1.05** | **0.55** | 27.71% | **7.50%** | — | 0.88 | **0.66** | 5.42bp | **0.97** | **2.16** | 3 |
| T4 | R | `rank(ts_delay(ts_sum(bf(R,22),252),22))` 长窗累加 + 延迟 | `YP1ZpG0J` | −0.09 | −0.02 | 8.02% | −0.84% | — | −0.34 | −0.11 | −2.09bp | −0.05 | −0.86 | 4 |
| T5 | σ²_idio | `group_rank(ts_std_dev(bf(SR,22),66), subindustry)` 二阶矩 | `2rAE7bN8` | −0.28 | −0.13 | 4.82% | −2.66% | — | −0.51 | −0.15 | −11.05bp | −0.25 | −0.17 | 4 |
| T6 | R | `group_rank(ts_ir(bf(R,22),252), industry)` 信息比标准化 | `O0AepExb` | −0.37 | −0.20 | 10.19% | −3.52% | — | −0.54 | −0.22 | −6.90bp | −0.28 | −1.71 | 4 |
| T7 | `short_interest_factor_score_2` | `group_rank(bf(·,22), sector)` 水平 | `kqNR3Qz6` | −0.92 | −0.69 | 8.08% | −6.98% | 72.71% | −1.58 | −0.49 | −17.28bp | −0.94 | 0.18 | 4 |
| **T8** | `hedge_fund_ownership_factor0` | `rank(ts_delta(bf(·,66),66))` 一阶差分 | **`omE2KY12`** | **1.10** | **0.47** | 5.18% | 2.25% | 2.79% | **1.12** | 0.33 | **8.67bp** | 0.85 | 1.20 | 4 |
| T9 | σ²_idio | `group_rank(reverse(ts_quantile(bf(SR,22),252,gaussian)), industry)` 分位变换 | `xArMxnKb` | 0.18 | 0.03 | **43.40%** | 0.90% | 20.80% | 0.04 | 0.03 | 0.42bp | 0.33 | −0.91 | 4 |
| **T10** | **R** | **`group_rank(reverse(ts_decay_linear(bf(R,22),22)), subindustry)` 线性衰减反转** | **`WjOkpgEZ`** | **1.28** | **0.61** | 33.53% | **7.74%** | 6.34% | 1.05 | **0.79** | 4.62bp | **1.15** | **3.19** | 3 |
| T11 | `systemic_risk_measure_2` | `group_rank(reverse(bf(·,22)), industry)` 水平反转 | `GrWVwor0` | 0.29 | 0.16 | 2.40% | 3.94% | **63.27%** | 0.65 | 0.16 | **32.83bp** | 0.27 | −0.13 | 3 |
| T12 | `relative_volatility_factor` | `group_rank(ts_rank(bf(·,22),504), sector)` 长窗时序分位 | `9qxowRqx` | 0.33 | 0.11 | 11.36% | 1.48% | 8.64% | 0.36 | 0.59 | 2.60bp | 0.32 | 1.03 | 3 |

持仓规模：全部 12 条 `longCount ≈ 1481–1578`、`shortCount ≈ 1481–1579`，约 3000–3150 只，十年覆盖完整（无空年）。

**模板多样性核对**：本波 + 波 173 共用模板库 ≥10 个结构互异模板——
水平反转 / 时序分位（252）/ 累加反转（ts_sum）/ 长窗累加 + 延迟（ts_delay）/ 二阶矩（ts_std_dev）/ 信息比标准化（ts_ir）/ 一阶差分（ts_delta）/ 分位变换（ts_quantile gaussian）/ 线性衰减反转（ts_decay_linear）/ 横截面秩 + 时序差分（波 173 R1）/ 分组 zscore（波 173 R2）/ 双窗相对强度（波 173 R4）/ 条件化 trade_when（波 173 R5）/ 算子顺序交换（波 173 R6）/ 秩的时序波动（波 173 R7）。差异落在骨架 / 算子几何 / 矩 / 分组轴 / 非线性变换五个维度上，非换窗口。

---

## 4. 核心发现一：`risk_neutralized_sharpe` 全面跑赢原始 Sharpe

| alpha | 原始 S | risk_neut_S | 倍数 |
|---|---|---|---|
| T10 `WjOkpgEZ` | 1.28 | **3.19** | **2.49×** |
| T3 `9qxowLr9` | 1.05 | **2.16** | **2.06×** |
| T8 `omE2KY12` | 1.10 | 1.20 | 1.09× |
| T12 `9qxowRqx` | 0.33 | 1.03 | 3.12× |
| T7 `kqNR3Qz6` | −0.92 | 0.18 | 符号翻转 |
| T2 `j2YLZb05` | −0.16 | 0.88 | 符号翻转 |
| T9 `xArMxnKb` | 0.18 | −0.91 | 反向恶化 |
| T6 `O0AepExb` | −0.37 | −1.71 | 反向恶化 |
| T11 `GrWVwor0` | 0.29 | −0.13 | 反向恶化 |

**含义**：本数据集的 alpha 收益被风险模型风格暴露**严重稀释**——不是「收益来自风格」，而是「风格暴露在拖累原始收益」。剥离风格后 T10 的 Sharpe 是 3.19，T3 是 2.16。

⇒ **这是把 S 1.28 推到 1.58 的最短路径，且零信号改动**（只换设置档，不动表达式），既不违反 ATOM（字段仍全来自单数据集），也不违反「禁 add(A,B) 混信号」纪律。

⚠ **反向警戒**：T6 / T9 / T11 的 risk_neut_S 比原始 S 更差，说明「中性化必然提分」是错的——只有信号本身与风格因子**负相关**时中性化才提分。T6（ts_ir）与 T11（systemic_risk_measure_2）本身就是风格类量，剥离后自然归零。

---

## 5. 核心发现二：只有 1 个字段有真信号

**唯一有效字段 = `discount_store_retail_score`（残差日收益反转）**，4 种加工全部有效且都过 SUB 闸：

- `ts_sum 22` + industry 轴 → S 1.05 / F 0.55 / SUB 0.66 / invest_S 0.97
- `ts_decay_linear 22` + subindustry 轴 → S 1.28 / F 0.61 / SUB 0.79 / invest_S 1.15
- 两者 2Y 分别 0.88 / 1.05

**其余字段全部判死**：

| 字段 | 最佳结构 | 最佳 S | 判死理由 |
|---|---|---|---|
| `systemic_risk_factor_score`（σ²_idio） | 水平反转 | 0.22 | **低特质波动异象在本数据集不成立**。三种矩全灭：水平 0.22 / 时序分位 −0.16 / 二阶矩 −0.28 / ts_quantile 0.18 |
| `hedge_fund_ownership_factor0` | ts_delta 66 | 1.10 | S 够但 **TO 5.18% 在 F 地板下**，`S²·R = 1.21×0.0225 = 0.0272` 距 F=1.0 所需 0.125 差 **4.6 倍** ⇒ F 结构性天花板 0.47 |
| `short_interest_factor_score_2` | 水平 + sector | −0.92 | 强负向。反号后 S 0.92 / margin +17.28bp / `S²·R = 0.846×0.0698 = 0.059` 距 0.125 差 **2.1 倍** ⇒ 反号也不足 |
| `relative_volatility_factor` | ts_rank 504 | 0.33 | 无增量 |
| `systemic_risk_measure_2` | 水平反转 | 0.29 | 见第 7 节「高 margin 陷阱」 |

---

## 6. 核心发现三：F 杠杆方向与波 171 完全相反

T10 的 `TO = 33.53% > 0.125` ⇒ **在地板之上**，`F = S·sqrt(R/TO)`：

```
F = 1.28 × sqrt(0.0774 / 0.3353) = 1.28 × 0.4805 = 0.615   ← 实测 0.61，逐位吻合
```

要 `F ≥ 1.0` 需 `R/TO ≥ 0.61`，现在 `R/TO = 0.2309`，差 **2.6 倍**。若把 TO 压到 12.5% 地板且 R 不衰减：

```
F = 1.28 × sqrt(0.0774 / 0.125) = 1.28 × 0.787 = 1.007   ← 刚好过闸
```

⇒ **降 TO（表达式内加长平滑窗 / 平台 decay）+ 换 neutralization 是两个正交杠杆，可以同时用**。

这与波 171（`insider_agg_matrix`，TO 2.9–18.8% 全在地板下，降 TO 对 F 零收益）**完全相反**。而 T8 的 TO 5.18% 又落回地板下、重演波 171 的 F 天花板。

**方法论沉淀**：拿到任何候选，第一步先判 TO 在 0.125 的哪一侧，再决定「降 TO」还是「提 R」——两个方向的默认动作相反，判错就整轮白跑。

---

## 7. 核心发现四：高 margin 陷阱（T11）

`GrWVwor0` = `group_rank(reverse(ts_backfill(systemic_risk_measure_2, 22)), industry)`：

| 指标 | 值 | 同波排名 |
|---|---|---|
| margin | **32.83 bp** | **全波第 1**（7.1× 于 T10） |
| Sharpe | 0.29 | 第 8 |
| R | 3.94% | 第 4 |
| **DD** | **63.27%** | **全波最差** |
| TO | 2.40% | 全波最低之一 |

高 margin + 极低换手 + 巨大回撤 = **单笔信息量大但方向一致性崩塌**。这类形态在 US 市场多半是「低频事件驱动 + 长期持有错方向」，Sharpe 才是唯一有效的可投性判据。

⇒ **再次确认：margin 与 Sharpe 不可互相替代。** 判「有没有信号」看 margin 绝对值；判「能不能投」看 Sharpe 的方向一致性。（此结论来自波 170 的 `LLMegrk2` S −1.00 / margin 67.6bp 与 `mLoOr0gW` S 0.18 / margin 0.46bp 的对照，本波 T11 是第三个独立验证。）

---

## 8. 判死与禁用清单

**算子级**：

- **`ts_quantile(..., driver="gaussian")` 在本数据集摧毁信号**：T9 与 T1 同为 σ²_idio 反向，仅把水平换成 ts_quantile ⇒ S 0.22→0.18、TO 19.16%→**43.40%**、margin 0.30bp→0.42bp、risk_neut_S −0.66→**−0.91**。机理：分位变换在快变日频序列上引入巨量翻转，换手翻倍把信息抹平。
- **`ts_ir`（= `divide(ts_mean, ts_std_dev)`）毁掉残差反转**：T6 同字段裸 `ts_sum` 是 S 1.05，加 ts_ir 后 S **−0.37**、risk_neut_S **−1.71**。这与波 171 的 `ts_zscore` 在离散指示器字段上产出全 NaN 同源——**任何除以滚动标准差的操作在本区是系统性风险动作**。禁用范围从「离散指示器」扩大到「有符号残差连续量」。

**字段级**：

- 行业 score（61 个）/ 行业 flag（43 个）永久封盘（组内近常数 + 被中性化吃掉 + 45 个 userCount=0）。
- σ²_idio（`systemic_risk_factor_score`）在本数据集封盘：低特质波动异象不成立，四模板全 ≤0.22。

---

## 9. 反证记录：第五个「骨架不可跨数据集迁移」

| 波次 | 数据集 | 该数据集最优骨架 |
|---|---|---|
| 167 | `shortinterest3` | **矩类**（协方差 / 方差）最强 |
| 168 | `earnings_sent_matrix` | **有符号差分 + 长窗 zscore** |
| 171 | `insider_agg_matrix` | **`ts_rank` 序位**（S 0.87 全场最高，形状族 margin 最高但 TO 地板下不可兼得） |
| **172** | **`mfm_model_output`** | **有符号残差量的水平 + 线性衰减平滑**（`ts_decay_linear` S 1.28） |
| 172 | 同集 σ² 字段 | 无骨架有效（四模板全灭） |

本波还额外暴露一个更细的反证：**同一个数据集内部，不同字段的最优骨架也不同**（R 字段要「衰减平滑」、σ² 字段全灭、hedge_fund 字段要「一阶差分」）。⇒ 连「数据集内跨字段继承骨架」都不成立，只能逐字段跑模板消融。

**S 排序（本数据集模板族）**：

```
ts_decay_linear(R) 1.28
  > hedge_fund ts_delta 1.10
  > ts_sum(R) 1.05
  > relative_volatility ts_rank 0.33
  > systemic_risk_measure_2 水平 0.29
  > σ² 水平 0.22
  > ts_quantile(σ²) 0.18
  > σ² 时序分位 −0.16
  > σ² 二阶矩 −0.28
  > ts_ir(R) −0.37
  > short_interest 水平 −0.92
```

粗排序规律：**有符号残差量（水平 + 平滑） >> 无符号方差量 >> 标准化比值**。这条只能作为「下一个数据集先试什么」的先验，不能当结论用。

---

## 10. 下一步（波 173）

两个正交杠杆，各发一批：

**波 173-A —— 中性化档位扫描**（已派发 7 条）
锚表达式 = T10（`WjOkpgEZ`），只换 `neutralization`：
`STATISTICAL` / `SLOW_AND_FAST` / `SLOW` / `FAST` / `REVERSION_AND_MOMENTUM` / `SUBINDUSTRY` / `CROWDING`（基线 `INDUSTRY` = S 1.28 已知）。
USA 区合法中性化共 11 档：`NONE / REVERSION_AND_MOMENTUM / STATISTICAL / CROWDING / FAST / SLOW / MARKET / SECTOR / INDUSTRY / SUBINDUSTRY / SLOW_AND_FAST`。
假设：`risk_neut_S 3.19` 对应的风险模型口径最可能是 `STATISTICAL` 或 `SLOW_AND_FAST`。若任一档能把 S 推过 1.58 且 F 过 1.0 ⇒ RISK 塔第一颗落地。

**波 173-B —— R 字段 7 个结构互异新模板**（已预检通过，等槽位）
R1 `group_rank(ts_delta(rank(bf(R,22)),66), industry)` 横截面秩的时序一阶差分
R2 `group_zscore(reverse(ts_decay_linear(bf(R,22),22)), industry)` rank→zscore 保幅度（记忆：zscore 比 rank 换手低 20-30%）
R3 `group_rank(reverse(ts_rank(bf(R,22),252)), industry)` 时序分位反转
R4 `group_rank(subtract(ts_sum(bf(R,22),22), ts_sum(bf(R,22),252)), industry)` 双窗相对强度
R5 `trade_when(rank(abs(bf(R,22))) > 0.7, group_rank(reverse(bf(R,22)), industry), 0)` 极端幅度条件化
R6 `ts_decay_linear(group_rank(reverse(bf(R,22)), industry), 66)` 算子顺序交换（先横截面后时序）
R7 `group_rank(reverse(ts_std_dev(rank(bf(R,22)),66)), industry)` 秩的时序波动（二阶矩 × 横截面秩）

**若 A 组出货**：直接进 S4 评审 + 相关性检查，RISK 塔点亮。
**若 A 组全灭且 B 组最高 S < 1.58**：本数据集 F/Sharpe 双天花板确立，落 dead_end 转向 `risk65`（6 字段、coverage 0.9743、valueScore 3.0、411 alphaCount、6 未测）。

---

## 附：本地落库回执

- `wave_results` USA/172：`inserted`，verdict `PARTIAL`，n_pass 0，n_near 3，status `closed`，8 条 key_findings。
- 画像文档：`docs/reference/USA/mfm_model_output_field_profile.md`（11,186 字节）。
