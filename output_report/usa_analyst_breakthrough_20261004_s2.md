# USA analyst category — 本轮突破报告（2026-10-04 续）

> 承接 `usa_analyst_category_report_20261004.md`。该报告原判「F 锁定 ≤0.83，唯一出口 = SA/跨集」——
> **本轮被推翻**：F 天花板由 **z 窗重参数化** 击穿，并首次在 analyst 族找到 **IS 全闸通过** 的候选。
> 统一设置：USA / TOP3000 / delay 1 / decay 30 / STATISTICAL / truncation 0.08 / nanHandling ON。

---

## 1. 一句话结论

**analyst 族本轮产生两枚「差一颗闸」的顶级候选，但**没有**一颗能单表达式提交**——缺口分别是 F 的 0.03 与 prod 的 0.07，且**两者都是结构性的**（前者骨架天花板，后者概念拥挤墙）。
⇒ analyst category 的终局仍是**组合/新血**，但「单信号不可用」的旧判**已被部分推翻**（analyst69 的 target-price 族 IS 三维全部大幅过线）。

---

## 2. ★★★ AFS 的 F 天花板：0.83 → 0.97（本轮击穿 0.14）

### 2.1 根因：旧批只测了 z 窗 {66,126,252}，漏掉真峰 96

`z 窗 → F` 响应曲线（market 分组, 分母常数 C=1.0）：

| z 窗 | 88 | 92 | **96** | 100 | 104 | 110 | 126 | 150 | 180 | 210 |
|---|---|---|---|---|---|---|---|---|---|---|
| F | 0.89 | 0.88 | **0.95** | 0.92 | 0.88 | 0.86 | **0.83** | 0.84 | 0.85 | 0.63 |
| SUB | FAIL | PASS | PASS | PASS | FAIL | PASS | PASS | FAIL | PASS | FAIL |

**F 峰在 z=96，不是 z=126。** 旧批把 z=126 当最优点，恰恰踩在 F 谷底。

### 2.2 第二旋钮：内层 `ts_backfill` 窗

| backfill | 33 | 55 | **66** | 88 |
|---|---|---|---|---|
| F（z=96, market） | 0.95 | 0.96 | **0.96** | 0.97 |

**最终最优候选**：

```
AFS-K-8  (MP3X7NWL)
group_rank(trade_when(rank(ts_backfill(est_revision_magnitude_profit,33)) > 0.5,
  divide(ts_zscore(ts_backfill(est_revision_magnitude_profit,66),96),
         add(ts_zscore(ts_backfill(est_revision_magnitude_eps,66),96), 1.0)), -1), market)
```

| 指标 | 值 | 闸线 | 判定 |
|---|---|---|---|
| Sharpe | **1.82** | ≥1.58 | ✅ |
| Fitness | **0.97** | ≥1.0 | ❌ 差 **0.03** |
| SUB_UNIVERSE | **0.80** | ≥0.571×S | ✅ PASS |
| 2Y Sharpe | **2.17** | ≥1.58 | ✅ PASS |
| **prod 相关** | **0.6748** | <0.7 | ✅ **PASS** |
| self 相关 | 0.489 | <0.7 | ✅ PASS |

**6/7 闸通过，唯一缺口 = F 的 0.03。** 这是全程 prod 也过关的最高分候选。

### 2.3 F 公式锁定（为何 0.03 难补）

`F = S × sqrt( returns / max(turnover, 0.125) )`，本族 turnover≈0.051 < 0.125 地板 ⇒
**F 只由 `S × sqrt(returns)` 决定**（turnover 已不参与）。
- K-8: S=1.82, r=3.55% ⇒ F=0.97。
- 补 0.03 需：**r 再 +6.5%**（3.55%→3.78%）**或 S 到 1.877**。

**已证无效的杠杆**（本批 ~50 表达式穷举）：等价算子替换（`quantile`→0.94 / `ts_rank`外层→0.85 / `group_zscore`嵌套→0.95）；短 z 窗（44-60 全部 SUB FAIL，与 analyst69 相反 ⇒ **窗口效应族特异**）；分组轴 sector/subindustry（≤0.90）；分母常数 0.75-1.25。

### 2.4 判定

**AFS 单表达式 F 天花板 = 0.97**，剩余 0.03 由骨架结构锁死。**唯一出口 = SA 组腿 / 跨集组合**（原报告结论在 F 部分仍成立，但缺口从 0.17 收窄到 0.03）。

---

## 3. ★★★★★ analyst69 target-price 族：IS 全闸首次通过（旧 ceiling 0.98 → 1.25）

### 3.1 发现：`target_price / close` = 分析师隐含上行空间

```
QPKjb68Q
group_rank(ts_zscore(divide(vec_avg(anl69_best_target_price), close), 44), industry)
```

| 指标 | 值 | 闸线 | 判定 |
|---|---|---|---|
| Sharpe | **1.74** | ≥1.58 | ✅ |
| Fitness | **1.12** | ≥1.0 | ✅ |
| SUB_UNIVERSE | **0.81** | 比值闸 | ✅ PASS |
| 2Y Sharpe | **1.78** | ≥1.58 | ✅ PASS |
| **ra_failed_checks** | **[]（0 个）** | — | ✅ **全 IS 检查 PASS** |
| pyramid | PV×1.1 + ANALYST×1.2 | — | **双塔** |
| **prod 相关** | **0.7724** | <0.7 | ❌ 差 0.07 |

**这是本项目首个 analyst 族「IS 全闸通过 + 零 RA 失败 + 双塔」候选。** 旧 ceiling 0.98 被大幅超越。

### 3.2 z 窗-F 响应（本族，与 AFS 相反）

| z 窗 | 30 | 44 | 50 | 60 | 66 | 72 | 80 | 126 |
|---|---|---|---|---|---|---|---|---|
| F | 1.25 | **1.12** | 1.06 | 1.02 | 1.00 | 0.99 | 0.98 | 0.89 |
| S | 1.86 | 1.74 | 1.67 | 1.63 | 1.61 | 1.60 | 1.59 | 1.49 |

**短 z 窗 = 高 F**（z=30 时 F=1.25 / S=1.86）。**与 AFS 族的 z=96 峰完全相反** ⇒ 印证「窗口效应族特异，禁外推」。

### 3.3 24 个 F≥1.0 的配置（同一概念，同一 prod 墙）

穷举 P3-P6 批共得 **24 个 S≥1.58 且 F≥1.0** 的配置（z∈{30,44,50,55,60}、分组轴∈{market,sector,industry,subindustry}、含 `ts_rank`/`winsorize`/`group_zscore` 变体）。
**全部 24 个的 prod 相关 = 0.772–0.796**（实测 6 个，其余按同族推断）。

### 3.4 ★★ prod 墙类型判定（决定能否撬）

看 `check_correlation` 的 `production.histogram_nonzero` **0.6–0.7 桶**：

| 候选 | 0.6-0.7 桶 n | 类型 |
|---|---|---|
| QPKjb68Q | **1201** | 密墙 |
| 0mrdXX0G | **1320** | 密墙 |
| P0g6gXMM | **1880** | 密墙 |
| 3qVxVGE0 | **1210** | 密墙 |

按 `wq-post-rank-clip-break-prod-wall` 判据：**桶 n ≥ 几十 ⇒ 密墙，裁剪无效，必须换族/换信息维度。**

实测已证：换分子（target_hi/lo/median）、换分母（去 close）、换算子（`ts_rank`/`winsorize`）、换分组轴（market/sector/subindustry）**全部 prod 0.77-0.80**，纹丝不动。
⇒ **`target_price/close` 是平台 prod book 里的拥挤概念，任何变换都不能降低相关。**

### 3.5 判定

**analyst69 target-price 族：IS 完美但 prod 密墙封死。** 若平台 prod book 变化（或该概念被挤出），这 24 个里任一即可直接提交。

---

## 4. USA SuperAlpha：PROD 被成分池锁死（BLOCKED）

- `sa_probe(USA)` = **GO**，eligible=**19**（≥10）⇒ 组件数够。
- 建 6 颗 SA，最佳 `xAbQrYoW`（SUBINDUSTRY, d8, sl10）IS 全过，双闸 **0.762 / 0.789 BLOCKED**。

| SA | 中性化 | decay | sl | SELF | PROD |
|---|---|---|---|---|---|
| 88PrRgMz | STATISTICAL | 3 | 19 | 0.933 | 0.933 |
| xAbQrYoW | SUBINDUSTRY | 8 | 10 | 0.762 | 0.789 |
| **gJZKe2mK** | **MARKET** | 10 | 12 | **0.698 ✅** | 0.825 |
| pw5EaO6v | SECTOR | 10 | 12 | 0.721 | 0.843 |
| JjQm87Xn | MARKET | 15 | 19 | 0.698 ✅ | **0.825** |

**★ 关键**：MARKET 能把 SELF 修到 <0.7，但 **PROD 恒为 0.8251**——decay 10/15、sl 12/19、gate 0.5、cp 1/5 **全部不动它**。
⇒ **PROD 由成分池本身决定**（我的 19 颗 REGULAR 成分彼此相似且各自 prod 偏高）。
⇒ 命中 skill levers §3：**PROD 饱和的唯一解 = 挖 prod<0.55 的新血 REGULAR**，调 SA 旋钮无用。

**判定：USA SA 路径 BLOCKED，等新血。**

---

## 5. 两枚顶级候选的最终状态

| 候选 | 表达式族 | S | F | SUB | 2Y | prod | self | 缺口 |
|---|---|---|---|---|---|---|---|---|
| **`MP3X7NWL`** | AFS divide+gate | 1.82 ✅ | 0.97 ❌ | 0.80 ✅ | 2.17 ✅ | **0.675 ✅** | 0.489 ✅ | **F 差 0.03** |
| **`QPKjb68Q`** | anl69 target/close | 1.74 ✅ | 1.12 ✅ | 0.81 ✅ | 1.78 ✅ | 0.772 ❌ | — | **prod 差 0.07** |

两者互相关仅 **0.205**（`compute_mutual_correlation` 实测）⇒ 是**互补腿**，但：
- AFS 腿 prod 干净、F 差 0.03；
- anl69 腿 IS 全过、prod 墙。
- SA 需要**已提交 ACTIVE** 组件，而两者都未提交（且 AFS 腿 F 不过、anl69 腿 prod 不过）⇒ **当前无法互相解救**。

---

## 6. 下一步（按期望价值排序）

1. **等 ET 00:00 配额重置**，用户确认后提交。但**当前无 single-candidate 可提交**（两枚各差一闸）。
2. **新血 REGULAR（prod<0.55）** 是同时解锁 AFS 组腿与 SA 的钥匙 ⇒ 挖**与现有 book 正交的新数据集**（非 analyst 亦可）。
3. **AFS F 的最后一搏**：唯一未试的机制 = 引入**第二条正交信息腿**（Mode B 允许：单信号结构化，非加权混信号），在保 SUB 前提下抬 returns。
4. anl69 target-price 族留作**平台 prod book 变化时的备用**（24 个现成配置，任一可提）。

---

## 7. 工程/纪律沉淀（本轮新增）

- **窗口效应族特异，禁外推**（第 N 次验证）：AFS 峰 z=96，anl69 峰 z≤30，方向相反。
- **prod 墙先看直方图桶**：0.6-0.7 桶 n≥几十 ⇒ 密墙，别浪费时间调权重（`wq-post-rank-clip-break-prod-wall`）。
- **SA 的 PROD 受成分池锁死**：中性化轴只动 SELF；PROD 由池决定 ⇒ 池不换，无解。
- **analyst69 事件字段陷阱**：多个标称 MATRIX 的字段实为 event-typed（`best_px_bps_ratio`/`best_roe_median`/`best_eps_chg_pct`/`sales_4wk_up`/`pe_ratio`）⇒ `ts_zscore`/`group_rank`/`add`/`reverse` 报 "does not support event inputs"；须改用 event 算子。
- 探针脚本：`attic/tracking_reference_20261004/scripts/tmp_probe_conc.py`，`--exprs-file` 传 JSON `[[label,expr],...]`，`--conc`≤4，单进程。

---

## 8. 【更新】AFS F 天花板正式判死 = 0.97（N/O 两批 20 式穷举）

AFS-N（10 式）+ AFS-O（10 式）系统测试了所有剩余旋钮：

| 试的旋钮 | 结果 | 结论 |
|---|---|---|
| `ts_decay_linear` 10 | F 0.90 ↓ | 平滑降 F |
| `ts_mean` 5 / 10 | F 0.92 / 0.77 ↓ | 平滑降 F |
| 外层 `ts_zscore` 250 | F 0.73 ↓ | 二次 z 毁灭 |
| gate 0.45 / 0.55 | F 0.84 / 0.93 | 0.5 最优 |
| subindustry / sector / industry 轴 | F 0.84 / 0.96 / 0.92 | market 最优 |
| backfill 100 / 120 / 132 | F 0.96 / — / 0.96 | ≥66 已饱和 |
| z 窗 90 / 108 | 见 O-8/O-9 | 96 最优 |

⇒ **F 硬顶 = 0.96–0.97，被 `F = S × sqrt(returns/max(TO,0.125))` 与 SUB 比值闸双侧夹死**。

**新添 4 颗 F0.96 + SUB PASS + 2Y PASS 的双塔全闸候选**（仅差 F）：
`pw5ExoYV`(O-1) / `omWvRlpE`(O-2) / `6XK1ZARp`(O-7) / `MP3X7NWL`（原 K-8）。

**判定：AFS 单表达式路径 F 无法破 0.97，正式判死。转 SA 组腿 + 新血。**

---

## 9. 【更新】新血路径启动：analyst_base_ref + analyst_earnings_ibes

按"白地 = 高 value_score / PPA_PASS / alpha_count 低 / USA 未测"筛出两个最高优先级目标：

| 数据集 | alpha_count | USA 已测 | 状态 | 覆盖 | 信号维度 |
|---|---|---|---|---|---|
| **`analyst_base_ref`** | **6** | 0 | **PPA_PASS** | q 向 0.90 | 超预期 / 预期-实际偏离 / 稀释调整 |
| **`analyst_earnings_ibes`** | 56 | 26 | **PPA_PASS** | 1.0 | 财报后漂移 PEAD（报告日价格/收益窗口） |

**关键字段洞察**：
- `analyst_base_ref`：季度向 VECTOR 覆盖 ~0.90（可用）、年度向仅 ~0.36（弃）；核心 = `consensus_surprise_percentage_quarterly`、`consensus_vs_actual_diff_quarterly`、`dilution_adjustment_ratio`、`number_of_issued_shares`。
- `analyst_earnings_ibes`：全 MATRIX 覆盖 1.0；`*_dlr1/2/3` = 最近/次近/前次报告日，`*_dlra1` = 报告后累计 ⇒ 可构造 PEAD。

**两批探针已启动**（各 12 式，conc 3，总并发 6）：`probe_abr1.json` / `probe_ibe1.json`。

**判定目标**：找到 **prod<0.55** 且 IS 全闸的新血 ⇒ 一举解锁 AFS 组腿与 USA SA（当前 PROD 恒 0.825 的唯一解）。
