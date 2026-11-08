# GBR 未点亮塔 campaign · W1 归因报告

日期：2026-11-04　区域：GBR / TOP700 / delay 1　标准档：SUBINDUSTRY、decay 4、truncation 0.08
目标：在 GBR 未点亮塔（pv / other / earnings / institutions / insiders / sentiment / risk / option / macro / shortinterest / imbalance / socialmedia）挖 20 个 regular alpha，优先 ATOM。

## 一、W1 派发明细

| 批次 | multisim | 条数 | 数据集 | 塔位 |
|---|---|---|---|---|
| W1-A | 2iHqqdafo55kcJxj4ZstwYa | 8 | pattern_scores | PV |
| W1-B（首次） | 267Qt953H4ASaX51f2Ggn38Y | 8 | institutions25 / insiders12 / other567 | INSTITUTIONS / INSIDERS / OTHER |
| W1-B（修正重派） | 2FuuDp9Ka5ho8Spm9dCv4IA | 8 | 同上，修正 vec_avg/winsorize 顺序 | 同上 |

## 二、W1-B 首次派发全灭的根因（★ 最重要的技术教训）

平台原始报错：`Operator winsorize does not support event inputs.`

- 错误写法：`winsorize(vec_avg(F), std=4)` 之外的 `vec_avg(winsorize(F, std=4))` —— `winsorize` 直接吃了 VECTOR(event) 输入。
- 正确写法：**先把 VECTOR 聚合为 MATRIX，再做标量算子** —— `winsorize(vec_avg(F), std=4)`。
- 连带效应：8 条子仿真中 **5 条 ERROR + 3 条 CANCELLED** —— 同批一条语法/类型错会连坐取消其余同批任务。

## 三、W1-A（pattern_scores，8 个结构互异模板）读数

| alpha | 模板 | S | F | TO | 2Y | sub |
|---|---|---|---|---|---|---|
| E56pZjrK | T2 asc_triangle delta+gated | 0.15 | 0.03 | 9.08% | 0.23 | 0.12 |
| 0mYXbVK2 | T4 v_reversal/continuation 比值 | −0.01 | −0.00 | 1.79% | −0.25 | 0.08 |
| zq38vxJK | T1 gap_up/gap_down 价差 | −0.30 | −0.08 | 1.56% | 0.37 | −0.04 |
| E56pZjgK | T6 gap_up q95 事件门控 | −0.14 | −0.02 | 1.60% | 0.94 | −0.14 |
| bl6bYmop | T5 falling/rising wedge 价差 | −0.42 | −0.15 | 7.09% | 0.33 | −0.18 |
| VkxavrYM | T3 对称三角离散度 | 0.04 | 0.00 | 2.00% | −0.37 | −0.29 |
| rKRO1qJd | T7 desc_triangle ts_quantile | −0.28 | −0.07 | 1.63% | −0.54 | −0.36 |
| 0mYXbVe2 | T8 gap_up max 长窗 | −0.01 | −0.00 | 1.61% | −0.88 | 0.07 |

- **8 条全部 `MATCHES_PYRAMID` PASS** ⇒ 塔位判断正确，问题不在塔位。
- **TO 集中在 1.56%–9.08%** ⇒ 病根在换手，不在方向。

## 四、W1-B2（探针，8 条）读数

| alpha | 数据集 | 模板 | S | F | TO | 2Y |
|---|---|---|---|---|---|---|
| WjObjmkQ | other567 | T3 利差动量 | **0.40** | 0.14 | 6.44% | 0.52 |
| A1VN1ddQ | other567 | T2 outlook−culture 利差 | 0.17 | 0.04 | 4.76% | 0.47 |
| Xg9bgE6m | institutions25 | T2 仓位变动 | 0.14 | 0.03 | 6.35% | **0.66** |
| 78LN8VVQ | other567 | T1 overall 门控 | 0.10 | 0.02 | 2.30% | −0.13 |
| 88Rj8q1V | insiders12 | T2 持股比例变动 | −0.13 | −0.03 | 3.48% | 0.23 |
| LLMNLxA1 | institutions25 | T1 做空情绪门控 | −0.18 | −0.04 | 3.30% | −0.70 |
| leAveZZe | insiders12 | T3 买入强度比值 | −0.24 | −0.08 | 1.98% | −0.62 |
| E56p5AJK | insiders12 | T1 净买入额 | −0.25 | −0.07 | 2.18% | −0.24 |

## 五、归因（★ 结构性结论，不是参数问题）

1. **瓶颈是换手，不是信号方向。** 16 条覆盖 4 个数据集、11 个结构互异模板，TO 一律落在 **1.6%–9.1%**。原因是骨架里叠了 `ts_mean(·,5)` / `ts_decay_linear(·,22)` / `hump(0.005)` **三层平滑**；被平滑的字段本身又是慢变量（形态相似度、员工评分、内部人季度持股）⇒ 换手被压到 2% 量级，收益被摊薄到撑不起 Sharpe。
2. **2Y 不是这里的约束，S 才是。** 多条 2Y（0.94 / 0.66 / 0.52）显著高于 S —— 与常见「S 高 2Y 崩」相反，说明信号在近年有效但幅度太小。
3. **pattern_scores 的 ATOM 路线基本走死。** 该数据集 504 字段全是形态相似度（无价格、无收益），要接价格类字段就构成 **PV+PV 组腿（明令禁止）**。相似度的「水平」对收益没有直接映射，而「变化率」也已试过（T2/T4 差分与比值）仍无信号。
4. **重平滑骨架在 GBR 应整体废弃。** 后续波次改用 `ts_target_tvr_decay(..., target_tvr=0.2–0.5)` 这类**显式换手目标算符**来控 TO，而不是靠叠平滑。

## 六、资产盘点（本轮新增的关键地图）

- **未点亮塔近闸库存 76 条**（S≥1.58、F≥1.0、TO 0.05–0.30、未提交）：earnings6 8 / order_book_imbalance 23 / pv1 4 / pv47 19 / shortinterest3 1 / techindi_model 21。
- **其中 prod 从未测过的有 69 条** —— prod 是唯一未探明的闸。
- **prod 命中缓存时仅需 5 秒**（`elapsed_ms 5236, computed true`）⇒ 可批量扫库存。
- **`techindi_model` 是 399 个 `tm_*` 字段的元数据集**：4 个模型版本（tm_1 / tm_8 / tm_15 / tm_16）× 3 个 horizon（r1 / r5 / r10）× 分位桶 q1–q5 与对数概率 `_p0.._p4`；191 个连续型 + 37 个离散桶标签；逐字段 aC 多为 0–15（真·处女子弹）。
- **全闸通过件 `XgJzLbl1`（techindi_model，塔位 other）实测 prod = 0.9955** —— self 仅 0.2995，但生产池里存在近乎克隆的对手 ⇒ **self 干净 ≠ prod 干净** 再次被证实。
- 获胜骨架（值得复用）：`group_rank(ts_target_tvr_decay(winsorize(rank(group_neutralize(add(ts_mean(ts_backfill(F,500),1), ts_mean(ts_backfill(F,500),60)), sector)), std=0.2), lambda_min=0, lambda_max=1, target_tvr=0.50), sector)`，neutralization=CROWDING，TO 21%、2Y 2.02、sub 1.93。

## 七、下一波设计原则

1. 一律用 `ts_target_tvr_decay` 显式控换手，目标 TO **15%–25%**；禁止 `hump` 与多层 `ts_decay_linear` 叠加。
2. 每个候选一个**互异核心字段**（不同 horizon / 不同分位桶 / 不同模型版本 / 概率 vs 回归强度），不做同核心换参数。
3. **避开已被占位的 `tm_16_r10_q2_p1`**。
4. 派发前先做 `compute_mutual_correlation` 去重（>0.70 只留最优一颗），再上 prod。
