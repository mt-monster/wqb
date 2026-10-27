# USA REGULAR Alpha 挖掘 · 详细情况汇报（2026-10-25）

> 快照日：2026-10-25。数据来源：平台 live（`get_alpha_details` / `get_pyramid_multipliers` / `batch_status`）、
> DB 台账（`get_submit_ready` / `get_wave_result` / `get_dead_ends`）、`tools/campaign_intel.py s0-select --region USA`。
> 本报告只陈述现状与证据，不构成提交授权。

---

## 0. 一句话结论

**严格口径在册 5 / 10。** 原先的「5 在册 + 4 臂 basket = 潜在 9」已作废：
2026-10-24 容量侧复核（`reports/robustness_20261024.md`）实测 insider 全族 `invest_S` 极低，
**4 臂 basket 全部撤回**，交付缺口回到 **5 颗**，且必须来自新的未点亮塔机制。

当前唯一「活口」是 `techindi_model` 的 `kqJM08g8`（S 1.63 / F 0.95 / 2Y 2.57 / invest_S 1.29），
只差 `LOW_FITNESS` 0.05；按 `usa_tm_w6r_notes.md` §4 预注册，已触发**设置调参线**（允许再开一波、只动设置）。

---

## 1. 交付口径与计数

口径（用户 2026-09-19 定案 + 2026-10-23 更正）：平台 RA `failed_ra_count = 0`
+ `check_correlation(refresh=True)` 的 **prod 与 self 均 < 0.7**
+ **主数据集所在平台类别塔未点亮** + **容量（invest_S）不塌陷**。

| 块 | 数量 | 状态 |
|---|---:|---|
| 已提交 ACTIVE（analyst 三集） | **5** | ✅ 严格口径在册（开采/提交时 analyst 未点亮） |
| 全过未提交 basket（insider 族 4 臂） | 0（原 4） | ❌ **已按容量复核撤回**，见 §3 |
| ai_equity 分歧族 5 颗 | 0（原 5） | ❌ MODEL 塔已点亮，仅作组腿辅助池 |
| `submit_ready` 里其余已验证件 | 0 | ❌ 全部撞已亮塔或容量坍缩，见 §7 |
| **当前交付缺口** | **5** | 必须来自新机制（fundamental 塔已穷尽，见 §8） |

> 计数变化链：`5/10`（10-23 剔除 MODEL 塔 5 颗）→ `潜在 9`（10-24 basket 入册）→ **`5/10`**（10-24 容量复核撤回 basket）。

---

## 2. 已提交 ACTIVE（5 颗，均在册）

| # | alpha | 数据集 | 核心字段 | S | F | 2Y | SUB | prod | self |
|---:|---|---|---|---:|---:|---:|---:|---:|---:|
| 1 | `omoK1A5m` | analyst_factor_signals | `eps_q1_estimate_qoq_growth` | 2.05 | 1.24 | 1.79 | 0.93 | 0.6489 | 0.4864 |
| 2 | `akVnvzX5` | analyst_factor_signals | `eps_y1_estimate_skewness` | 1.83 | 1.06 | 1.87 | 0.95 | 0.6594 | 0.5692 |
| 3 | `gJWoaJqv` | analyst44 | EPS/sales 背离加速度（4 字段） | 1.74 | 1.27 | 2.21 | 0.86 | 0.6978 | 0.5803 |
| 4 | `kqJLawqP` | analyst44 | 同上（秩变换 + 756 日） | 1.61 | 1.11 | 1.62 | 0.84 | 0.6757 | 0.6445 |
| 5 | `e76xgXkM` | analyst_consensus | `mean_forecast_actual_combined_fxadj_eps_annual12` | 1.89 | 1.12 | 1.76 | 1.05 | 0.5532 | 0.4553 |

`analyst` 塔现已点亮（6 颗 ACTIVE），**后续不再从 analyst 主数据集开采**。

---

## 3. 已撤回：insider 族 4 臂 basket（容量复核）

**原 basket（`compute_mutual_correlation` 阈值 0.7 下最大互不相关子集，`max_subset_exact=true`）**

| alpha | 表达式核心 | S | F | 2Y | SUB | invest_S | ratio |
|---|---|---:|---:|---:|---:|---:|---:|
| `O0Jgd7Y7` | `ts_zscore(ts_sum(total_buy_transaction_count,42),252)` TOP2000 | 2.27 | 2.03 | 3.09 | 1.22 | **−0.06** | −0.026 |
| `88vXxaqv` | `ts_zscore(ts_sum(total_buy_transaction_count,63),504)` TOP3000 | 1.99 | 1.66 | 2.04 | 0.89 | **−0.29** | −0.146 |
| `LL53QVvn` | `ts_zscore(ts_sum(mean_top_buy_transaction_count,63),252)` TOP2000 | 1.61 | 1.39 | 2.75 | 1.00 | 0.22 | 0.137 |
| `d5KzLo7v` | insider_matrix `eur_aggregated_value_1` tail 壳 TOP3000 | 2.93 | 1.41 | 2.53 | 1.29 | 0.29 | 0.099 |

**撤回依据（`reports/robustness_20261024.md`「容量侧复核」）**

- 同族 6 颗实测 `invest_S` 落在 **−0.29 … +0.29**，ratio **−0.146 … +0.137**；
  对照 USA 17 颗 ACTIVE 的基准 ratio **0.83–1.05** ⇒ 差一个数量级以上。
- 两个容量杠杆都试过并失败：`d5KzLo7v@TOP1000` S 2.93→1.19（强度崩塌）；
  `d5KzLo7v@TOP2000 + maxTrade=ON` S 2.93→0.32（三项 RA FAIL）。
- 机制归因：内部人**笔数/金额聚合**的 z 分数极值集中在**不可投资小盘**，按 ADV 约束后剩余名字没有 alpha
  ⇒ 是信号本体问题，不是设置问题。
- 结论：**本族六颗全部不提交**（含后来更强的 `0mjaa2Ev` S 3.24 / prod 0.6460）。

**同族后来新验证的 3 颗（不增加计数）**

| alpha | 表达式 | S | F | 2Y | SUB | prod | self | invest_S | 说明 |
|---|---|---:|---:|---:|---:|---:|---:|---:|---|
| `88v2XRm7` | `total_top_secondary_buy_transaction_count` × ts_sum126 → ts_zscore252，subindustry/RAM | 2.73 | 2.60 | 3.55 | 1.27 | **0.6993** | 0.0859 | 0.34 | 与 basket 相关 >0.7，prod 贴线 |
| `d5KPPrxx` | 同上，industry/SLOW_AND_FAST | 3.13 | 2.46 | 4.10 | 1.36 | 0.6737 | 0.1092 | 0.25 | 与赢家相关 **0.9837**，指标落后 ⇒ 弃 |
| `vROPEJ8w` | `ts_zscore(ts_sum(mean_buy_transaction_count,63),252)` TOP2000 | 2.08 | 1.74 | 3.49 | 1.31 | 0.5517 | 0 | 0.17 | 同族备胎 |

三者 `invest_S` 0.17–0.34（ratio 0.08–0.12），与 basket 同结论；且篮子最大独立子集 = 4 已穷尽
⇒ **它们是替代品而非增量**。队列里仍显示 `READY / SUBMIT_LAYER_VERIFIED`，**待标记 withdrawn**。

---

## 4. 已收批：波 `tm_w6r`（techindi_model 信号效率定向调参）

**设计**：`kqJM08g8` 的核心是论坛「换参照系」几何
`group_neutralize(group_zscore(x, <group>), group_cartesian_product(bucket(rank(ts_std_dev(x,22)),"0,1,0.2"), bucket(rank(ts_mean(x,252)),"0,1,0.2")))`。
w6r 把 decay 从 22 提到 44，并测分组/宇宙/平滑三轴。

**收批现状（2026-10-25）**

| 臂 | alpha | S | F | TO | ret | 2Y | SUB | invest_S | RA |
|---|---|---:|---:|---:|---:|---:|---:|---:|---|
| subindustry × decay44（TOP3000） | `kqJM08g8` | **1.63** | **0.95** | 12.82% | 4.38% | **2.57** | 0.71 | **1.29** | 仅 `LOW_FITNESS`（0.95 < 1.0） |
| hump 单桶 | `zqrEmAbV` | 0.64 | 0.24 | 6.03% | 1.73% | 1.08 | 0.27 | 0.49 | 4 项 FAIL ⇒ 平滑方向为负 |
| baseline sector × decay44（TOP3000） | — | — | — | — | — | — | — | — | **HTTP 404（未回测）** |
| baseline × TOP2000（M2 整批） | — | — | — | — | — | — | — | — | **HTTP 404（整批）** |

- M1 `2no3eO7Iv4OK8Kw6eT7Akda`：child_count 3，2 COMPLETE、1 个 child 持续 404
  （location `440pPI9T654O9FwLVbaYgqu`）；M2 `kBAWV90K4UGbbw1eVXMTbIc` 连续两轮整批 404。
- 404 不影响裁决：`kqJM08g8` 已越过判死线并触发调参线。

**对照预注册判据（`tracking/USA/runs/usa_tm_w6r_notes.md` §4）**

| 判据 | 阈值 | 实测 | 结论 |
|---|---|---|---|
| 判死线 | max S < 1.38 | 1.63 | 未触发 |
| 推进线 | S ≥ 1.58 且 F ≥ 1.00 且 2Y ≥ 1.58 | F 0.95 | 未触发（差 0.05） |
| **调参线** | S ≥ 1.50 且 F ≥ 0.85 | 1.63 / 0.95 | **触发 ⇒ 允许再开一波，只动设置** |
| 封存触发 | RA 全过而 prod ≥ 0.70 | RA 未全过 | 不适用 |

**F 算术（决定下一波杠杆方向）**

`F = S·√(ret / max(TO, 0.125))`；当前 TO 12.82% 已贴平台地板 12.5%，**继续压换手几乎不再放大 F**
（即使 TO 压到 12.5%，F 也仅 0.965）。要到 1.00 必须**抬 S 或抬收益**：

- 保持 ret 4.38% ⇒ 需 **S ≥ 1.69**；
- 保持 S 1.63 ⇒ 需 **ret ≥ 4.70%**（+7.3%）。

⇒ 下一波的设置轴必须优先选「能抬 Sharpe/收益」的项（decay 上调、truncation 放宽、中性化档），
而不是只做平滑。

---

## 5. 本轮收口波次与裁决（2026-10-24 → 10-25）

| 波 | 数据集 / 塔 | 最好臂 | 关键证据 | 裁决 |
|---|---|---|---|---|
| `tm_w5` | techindi_model / OTHER 1.4× | `_5` S 1.38 / F 0.69 / 2Y 2.14；`_13` S 0.40 | prod **0.7109**，`[0.7,0.8)` 桶 **n=1** ⇒ 几何改写未破墙 | `_13` 死；`_5` 留作 tm_w6 种子 |
| `insd_agg_w2` | insider_agg_matrix / INSIDERS 1.1× | `A2` S 0.96 / F 0.43 / 2Y 0.95；镜像 `A5` −0.96 | 符号对照逐位镜像 ⇒ 无方向歧义；F 反解需 ret 2× | 灰区结案，**弱不判死**（0.6 判死线未触发），不开 w3 |
| `fnd93_w1` | fundamental93 | 六臂全负，max \|S\| 0.78 | 应计/资产增长在高利率周期被反向定价 | 判弱结案 |
| `ofi_w1` | order_flow_imb / OPTION 1.3× | max \|S\| 0.33 | 论坛配方 7 算子复刻无信号；反号臂 +1.11 / SUB +1.08 | REGULAR 判死；**转 PPA 素材** |
| `ecs_w1` | earningscall_sentiment | max \|S\| 0.51 | #1/#2 镜像 ⇒ 概念无方向；CW 全落 2014 爬坡日 | 判弱结案 |
| `orev_w1` | other567 员工评价 / OTHER 1.4× | `9qE2G3L2` S 1.74 / F 1.23 / 2Y 1.50 | 3 条实测 prod **0.8503–0.8983**；`[0.7,0.8)` 桶 n=1871–9521 | 按 D0-P 结构性判死 |
| `oth566_w1` | other566 | `9qE2nllq` S 1.35 / F 0.46；invest_S 1.56 | 标签族 prod 0.866，prod 干净族 S 天花板 1.35 / F 0.46 | 数据集级封存 |
| `fnd91_w1` | fundamental91（8-K NLP） | `xA1oAgGJ` S 1.45 / F 0.77 | prod 0.7846（[0.7,0.8) n=2）；另一臂 0.9269 | 判死 |
| `oth580_w1` | other580（ETF 流向） | max \|S\| 0.66 | 反转先验被否（raw 正号）；广度臂 ±0.66 精确镜像 | 判弱结案 |
| `macro27_w1` | macro27 | max S 1.39 | prod 0.8771；可提交方向 0.7933 | 结案 |
| `risk60` | risk 1.1× | `A1Qr9Y8W` S 2.39 / F 5.24 | prod **0.9917**（[0.9,1] 桶 n=116） | 结构性判死 |
| `institutions18` | institutions 1.0× | `88PmKRzv` / `RR6JkEpd` | prod **0.9493 / 0.9377** | 判死 |
| `tm_w6r` | techindi_model / OTHER 1.4× | `kqJM08g8` S 1.63 / F 0.95 / 2Y 2.57 | 仅 LOW_FITNESS；invest_S 1.29；调参线触发 | **PARTIAL**（已入库，允许设置调参波） |

**台账总量**（`get_region_overview`，`tm_w6r` 入库后）：USA 共 **138 波 / 已结案 119 波 / 判死记录 37 条**。

---

## 6. 已判死 / 停投清单（数据集级，累计）

| 塔 | 已判死 / 停投 |
|---|---|
| fundamental 1.1× | **全塔穷尽**：14/91/2/6/17/23/28/3/7/13 元数据或饱和、110 长表 VECTOR、93 六臂全灭、1/21/22/25/35/69/72 低 S；唯一剩下的 13（aC 15361）/17（aC 34886）为高拥挤项 |
| other 1.4× | 566（标签族 prod 0.866）、567（prod 0.85–0.90）、580（max\|S\| 0.66）、635（跨供应商分歧）、143（prod 0.8658）、571（S 1.51 + prod 0.9087） |
| pv 1.1× | pv20（46 行 max\|S\| 1.44）、pv106（全负 + 空列）、pv149、chart_model_alpha、chart_return_model（同模型多配置无新信息） |
| risk 1.1× | risk60（prod 0.9631–0.9917） |
| option 1.3× | option9（PCR）、option40（IV surface ~1.1）、option_chart_model（prod 0.78–0.84）、option_horizon_decomp（IV skew ~1.45/F 0.84）、order_flow_imb（转 PPA） |
| news / sentiment / socialmedia | ai_news_scores、news81、news_sentiment_dl、event_sentiment_signals、earningscall_embed、earningscall_sentiment |
| macro / institutions | macro27、institutions18 |
| insiders 1.1× | insider_matrix（稀疏事件双墙）、insider_feats（\|S\|<0.5）、insider 计数族（容量墙，§3） |
| shortinterest | shortinterest3 / 7 / 29 |
| 其他 | acquisition_model、pattern_scores、pv_tech_indicators、ml_factor_proj（prod 0.92–0.93）、multifactor_return_pred 部分机制 |

---

## 7. `submit_ready` 队列现状（READY 14 条，**当前无可提交件**）

按 live 全量拉取（`status=ALL`，180 行）复核：`READY 14` / `DEAD 140` / `SUBMITTED 13` / `SUPERSEDED 13`。
READY 的 14 条 = **6 条 SUBMIT_LAYER_VERIFIED + 8 条 IS_ONLY**。

**6 条已验证（prod/self 都测过）—— 逐条不可提原因**

| alpha | 数据集 | S | F | 2Y | prod | self | 为什么不能提 |
|---|---|---:|---:|---:|---:|---:|---|
| `88v2XRm7` | insider_trx_matrix | 2.73 | 2.60 | 3.55 | 0.6993 | 0.0859 | 容量撤回（invest_S 0.34 / ratio 0.12） |
| `d5KPPrxx` | insider_trx_matrix | 3.13 | 2.46 | 4.10 | 0.6737 | 0.1092 | 容量撤回（invest_S 0.25）+ 与族内赢家相关 **0.9837** |
| `vROPEJ8w` | insider_trx_matrix | 2.08 | 1.74 | 3.49 | 0.5517 | 0 | 容量撤回（invest_S 0.17 / ratio 0.08） |
| `zqrgna91` | ai_equity_alpha | 2.67 | 1.66 | 1.68 | 0.6877 | 0.2866 | MODEL 塔已亮（降级为组腿池）；corr 59.2h |
| `N1eLE1de` | ai_equity_alpha | 2.63 | 1.54 | 2.07 | 0.6916 | 0.2753 | MODEL 塔已亮；prod 余量仅 0.0084；corr 59.0h |
| `1YZpv1bK` | analyst_consensus | 1.79 | 1.06 | 1.66 | 0.6934 | 0.4122 | analyst 塔已亮；corr **435.6h（18 天，已过期）** |

**8 条 IS_ONLY**（prod 未测，不构成候选）：`WjLoMW0x`(1.69/2.94)、`xA1GAZwN`(2.62/1.60)、
`ZYmzYJq8`(2.59/1.58)、`88vJ1YKa`(2.94/1.42)、`ZYmzGMr0`(2.92/1.41)、`wpbagVMY`(2.03/1.36)、
`1Yj08nb6`(1.58/1.20, prod 0.5796)、`XgRM3Yra`(1.66/1.19, prod 0.5803)
—— 全部来自 `insd_agg_w2`（insider 族），即使补测 prod 也逃不出 §3 的容量结论。

> 队列另有 **13 条 SUBMITTED**（2026-09-20 前后 PPA 时代遗留，corr age 847h）与 **13 条 SUPERSEDED**，
> 不在 §1 严格口径内；`SUBMITTED` 中带塔位标注的为 OTHER×1.4 ×3 / MODEL×1.3 ×4 / EARNINGS×1.2 ×2 /
> INSTITUTIONS×1.0 ×1 / FUNDAMENTAL×1.1 ×1 —— 这些塔今天仍未点亮，但它们属旧口径，不计入本轮交付。

**待处置**：把 insider 族 READY 行标 `DEAD`（撤回），避免队列继续误导。
⚠ `tools/submit_queue.py retire` 的**单颗路径不传 `--note`**（`cmd_retire` 调 `sq.retire()` 时只给 status/region），
撤回原因会丢；要么先补这个参数，要么把原因集中记在本报告与 `reports/robustness_20261024.md`。

---

## 8. 下一步（按优先级）

### 8.1 `tm_w7`：唯一活口的设置调参波（立刻可开）

- 对象：`kqJM08g8` 冻结表达式（subindustry 4 维几何），**只动设置**。
- 轴：decay `44 → 60 / 66 / 88`；truncation `0.08 → 0.10 / 0.12`；
  neutralization `FAST → STATISTICAL / SLOW / CROWDING`；universe `TOP3000 → TOP2000 / TOP1000`。
- 预注册：`F ≥ 1.00 且 S ≥ 1.58 且 2Y ≥ 1.58` ⇒ 立刻 prod-first；
  同时要求 `prod < 0.70`、`[0.7,0.8)` 桶 n=0、`invest_S ratio ≥ 0.5`；
  一波不达标 ⇒ tm 结案（不再加波）。
- 一并补发 w6r 的两个 404 臂（baseline sector × TOP3000 / TOP2000），只作对照，不影响主判。

### 8.2 补 5 颗：范围必须扩到其它未点亮塔

`fundamental` 塔已穷尽（§6）。`campaign_intel s0-select --region USA --delay 1`（2026-10-25 live）：
平台推荐 45 → 剔除已亮塔 0 → 剔除判死 14 → **存活 31**；点塔 **2/16**（analyst、model 已亮）。

可开但**尚无强度证据**的候选（按分数序）：`other696`（Hybrid NLP，294 字段，aC 1324）、
`other335`（Multi-Region Dividend Alpha Model，10 字段）、`pv141`（VWAP Tick，6 字段）、
`institutions6`（Stake Ownership，11 字段）、`option8`（Volatility）、`macro38`（Technical Ratings，aC 16240）。

按 P5 纪律「缺强度证据不开波」：**先跑 `prod-probe`（0 回测槽）封族，再决定开哪 1–2 个**，
不做十臂盲扫。原任务限定 Fundamental，范围外扩需要用户确认（§9）。

### 8.3 收尾与运维

- 队列清理：insider 族 READY 11 条 + 同波入队的 `1YZpv1bK` 标 `DEAD`（原因见 §7 与
  `reports/robustness_20261024.md`，**不要依赖 `--note`**，单颗 retire 会丢原因）；
  `1YZpv1bK` 的 corr 若再用需 `refresh=True`（且 analyst 已亮，不建议）。
- **waiver 到期 2026-10-31**：`waiver_stop_rules_USA_all`、`waiver_stop_rules_USA_insd_trx_w7`、
  `waiver_inspect_USA_oth566_w1`、`waiver_inspect_USA_fnd91_w1`、`waiver_inspect_USA_fnd67_w1`
  —— 需续期（用户指令）或到期自动失效。
- `tm_w6`（首次被 `[OPS] 10 ≥ 10` 与字段族重复拦下的那一版）留在 `gate_results` 作为失败留痕，勿复用该波号。

---

## 9. 待用户决策

1. **insider 族 4 臂 basket**：已按容量复核撤回（invest_S ratio −0.146…+0.137 vs ACTIVE 基准 0.83–1.05）。
   是否认可该结论？若否决并要求提交，需明确指令（提交不可逆）。
2. **补挖范围**：fundamental 已穷尽，是否同意把剩余 5 颗的范围扩到 `other` / `pv` / `institutions` / `option` 等未点亮塔？
3. **tm_w7**：是否按上述设置轴开波（预计 8 臂、并发 2 槽、约 1 个批次窗口）。
