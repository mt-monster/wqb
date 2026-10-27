# USA REGULAR Alpha 交付报告（2026-10-21）

> 目标：USA 区域内产出 10 个通过验证的 REGULAR alpha（优先 ATOM 类型）。
> 口径声明：**验证 = 平台 RA 全闸 PASS + `check_correlation(refresh=True)` 的 prod / self 均 < 0.7**
> （见 `Claude/skills/wq-brain-ra-usa/rules/gate-and-submit-discipline.md` 三·3：prod 只向上漂，存量读数作废）。
> 按这个严格口径，本次交付是 **5 / 10**；另 5 颗 IS 全闸但 prod 破 0.7 红线，**合规上不可提交**。
> 全程固定在 USA / TOP3000 / D1 / trunc 0.08，未换区域、未换 universe。
> **2026-10-23 更正（用户指出，撤回 10/10）**：`ai_equity_alpha` 属 **MODEL** 塔，而 USA/D1 的
> `model` 在本轮扩挖前已是 **4 颗 ACTIVE（已点亮）**。按用户既定规则「**已点亮塔的数据集不优选作为挖掘目标**
> （只作组腿辅助）」，§6.6 / §6.7 补入的 5 颗（`YPx89bQJ` / `58jr102k` / `zqrgna91` / `j2eoKKEj` / `N1eLE1de`）
> **不计入交付**，严格口径回退为 **5 / 10**。它们在 IS + 双相关性上仍全部过闸，保留作 **组腿辅助池**，
> 不作主数据集候选、不再申请提交。§1–§5 的 analyst 战役记录保留不改（开采时 analyst 仅 1 颗 ACTIVE、
> 未点亮；这 5 颗提交后才达 6 颗 → 已点亮）。
> **补充数据集路线**：改用 **未点亮塔**（优先 `fundamental`，次选 `other` / `institutions` / `pv` 等）
> 重新开采 5 颗，进度见 §8。

---

## 1. 交付清单（10 个 IS 全闸 ATOM/REGULAR 候选）

设置口径：全部 **USA / TOP3000 / D1 / truncation 0.08 / 回测区间 2014-01-01 → 2023-12-31**。
S = Sharpe，F = Fitness，2Y = 近两年 Sharpe，SUB = 子宇宙 Sharpe，TO = 换手率，prod / self = 平台相关性实测。

| # | alpha | 状态 | 数据集 | 核心字段 | 算子逻辑（一句话） | S | F | 2Y | SUB | TO | prod | self | 画像索引 |
|---:|---|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---|
| 1 | `omoK1A5m` | **ACTIVE** | analyst_factor_signals | `eps_q1_estimate_qoq_growth` | 季度 EPS 环比增速的 252 日均值变化，通用壳（backfill 756） | 2.05 | 1.24 | 1.79 | 0.93 | 3.65% | 0.6489 | 0.4864 | [§](../../Claude/skills/wq-brain-ra-usa/references/_usa-analyst-factor-signals-field-profile-20261019.md) |
| 2 | `akVnvzX5` | **ACTIVE** | analyst_factor_signals | `eps_y1_estimate_skewness` | 年度 EPS 预期偏度的 315 日时序 z 分，再按 industry 中性化 | 1.83 | 1.06 | 1.87 | 0.95 | 3.46% | 0.6594 | 0.5692 | [§](../../Claude/skills/wq-brain-ra-usa/references/_usa-analyst-factor-signals-field-profile-20261019.md) |
| 3 | `gJWoaJqv` | **ACTIVE**（`USA_R_ANALYST_03`） | analyst44 | `anl44_2_eps_value` / `_eps_prevalue` / `_sales_value` / `_sales_prevalue` | EPS 与营收背离度的 504 日均变化再取 252 日差分（背离加速度），market 分组 | 1.74 | 1.27 | 2.21 | 0.86 | 10.14% | 0.6978 | 0.5803 | [§](../../Claude/skills/wq-brain-ra-usa/references/_analyst-campaign-20261017.md) |
| 4 | `kqJLawqP` | **ACTIVE**（`USA_R_ANALYST_04`） | analyst44 | 同上 | 背离度先秩变换再取 756 日平均变化，market 分组，CROWDING 中性化 | 1.61 | 1.11 | 1.62 | 0.84 | 9.61% | 0.6757 | 0.6445 | [§](../../Claude/skills/wq-brain-ra-usa/references/_analyst-campaign-20261017.md) |
| 5 | `pw5RbrYX` | ❌ 拒提 | analyst_consensus | `mean/median_estimate_targetprice_annual12_tribes` + `stddev_estimate_fxadj_targetprice_annual12_tribes` | **分歧度 × 共识偏斜**：均值>中位数时做多分歧度、否则反向，20 日均值 | 2.07 | 1.21 | 1.67 | 0.90 | 3.75% | **0.9000** | 0.3495 | [§2.1](../../Claude/skills/wq-brain-ra-usa/references/_usa-analyst-consensus-field-profile-20261020.md) |
| 6 | `KPrGMEe1` | ❌ 拒提 | analyst_consensus | `mean_estimate_targetprice_annual12_tribes` | 目标价一致预期的 **175 日时序位置**（修正趋势，非绝对价位） | 1.94 | 1.24 | 1.71 | 1.04 | 5.94% | **0.9991** | 0.4277 | [§2.2](../../Claude/skills/wq-brain-ra-usa/references/_usa-analyst-consensus-field-profile-20261020.md) |
| 7 | `e76xgXkM` | **ACTIVE**（`USA_R_ANALYST_07`） | analyst_consensus | `mean_forecast_actual_combined_fxadj_eps_annual12` | 合并 EPS 的 **Δ63 按 252 日自身历史标准化**，RAM / industry 通用壳 | 1.89 | 1.12 | 1.76 | 1.05 | 3.29% | 0.5532 | 0.4553 | [§3.9](../../Claude/skills/wq-brain-ra-usa/references/_usa-analyst-consensus-field-profile-20261020.md) |
| 8 | `RR6bv6rz` | ❌ 拒提 | analyst_consensus | 同 #5 | #5 的分歧×偏斜结构，均值窗 **10 日**（#5 为 20 日） | 2.04 | 1.20 | 1.71 | 0.89 | 3.82% | **0.9054** | 0.3566 | [§2.1](../../Claude/skills/wq-brain-ra-usa/references/_usa-analyst-consensus-field-profile-20261020.md) |
| 9 | `leKKGb9l` | ❌ 拒提 | analyst_consensus | 同 #8 | 同 #5 结构，平滑算子换 **`ts_decay_linear 20`** | 2.04 | 1.19 | 1.66 | 0.92 | 3.78% | **0.9014** | 0.3547 | [§2.1](../../Claude/skills/wq-brain-ra-usa/references/_usa-analyst-consensus-field-profile-20261020.md) |
| 10 | `rKeOaLvo` | ❌ 拒提 | analyst_consensus | 同 #8 | #8 的同一表达式，**decay 512**（#8 为 500） | 2.04 | 1.20 | 1.71 | 0.89 | 3.83% | **0.9060** | 0.3567 | [§2.1](../../Claude/skills/wq-brain-ra-usa/references/_usa-analyst-consensus-field-profile-20261020.md) |

**设置明细**：#1/#2 = REVERSION_AND_MOMENTUM decay 1；#3 = RAM decay 20；#4 = CROWDING decay 10；
#5 = STATISTICAL decay 500；#6 = STATISTICAL decay 450；#7 = RAM decay 20（industry 分组）；
#8/#9 = STATISTICAL decay 500；#10 = STATISTICAL decay 512。

**ATOM 口径**：10 颗的全部非豁免字段均来自**单一数据集**（豁免仅限
country / exchange / market / sector / industry / subindustry 六个分组字段）。

---

## 2. 提交执行记录（2026-10-20，用户指令「按顺序提交至平台」）

| # | alpha | submit_verdict | prod（refresh=True） | 结果 |
|---:|---|---|---:|---|
| 1 | `omoK1A5m` | ALREADY_SUBMITTED | — | 早已 ACTIVE/OS |
| 2 | `akVnvzX5` | ALREADY_SUBMITTED | — | 早已 ACTIVE/OS |
| 3 | `gJWoaJqv` | ALREADY_SUBMITTED | — | 早已 ACTIVE/OS |
| 4 | `kqJLawqP` | ALREADY_SUBMITTED | — | 早已 ACTIVE/OS |
| 5 | `pw5RbrYX` | UNVERIFIABLE（无 FAIL，404 死端点） | **0.9000**（`[0.8,0.9)` n=1） | ❌ prod 红线，拒提 |
| 6 | `KPrGMEe1` | UNVERIFIABLE（无 FAIL） | **0.9991**（`[0.9,1]` n=1） | ❌ prod 红线，拒提 |
| 7 | `e76xgXkM` | UNVERIFIABLE（无 FAIL） | **0.5532** / self 0.4553 | ✅ 提交成功，ACTIVE/OS，`USA_R_ANALYST_07`，BLUE |
| 8 | `RR6bv6rz` | UNVERIFIABLE（无 FAIL） | **0.9054** | ❌ prod 红线，拒提 |
| 9 | `leKKGb9l` | UNVERIFIABLE（无 FAIL） | **0.9014** | ❌ prod 红线，拒提 |
| 10 | `rKeOaLvo` | UNVERIFIABLE（无 FAIL） | **0.9060** | ❌ prod 红线，拒提 |

- 逐颗的完整记录（含 `dateSubmitted`、金字塔归属、复核命令）见
  [`_usa-atom-delivery-log-20261020.md`](../../Claude/skills/wq-brain-ra-usa/references/_usa-atom-delivery-log-20261020.md) §1.1。
- #7 的客户端侧两次报 `MCP error -32603` 是等待超时（节点内 `_prod_gate(refresh=True)` + 提交后轮询），
  POST 已落地；以 `get_alpha_details` 复核为准，未重复补发。

---

## 3. 为什么是 5/10 而不是 10/10

**红线不可豁免**：`prod_correlation < 0.7` 是平台提交硬闸，`submit_verdict` 只能否决、不能放行；
#5/#6/#8/#9/#10 的 prod 实测落在 0.90–0.9991，任何一颗提交都会被平台拒，或即使提交也进不了 OS 的收益。

**同族不可再磨**：按决策表 D0-P，**prod ≥ 0.75 即判 `dead_end`**（红线，不因「只差一点」放宽）。
`alpha_corr_cache` 实测直方图（2026-10-21 只读复核）：

| 候选 | prod | `[0.7,0.8)` 桶 | `[0.8,0.9)` | `[0.9,1]` | 读法 |
|---|---:|---:|---:|---:|---|
| `pw5RbrYX` | 0.9000 | **0** | 1 | 0 | 单邻居重叠 |
| `RR6bv6rz` | 0.9054 | **0** | 0 | 1 | 单邻居重叠 |
| `leKKGb9l` | 0.9014 | **0** | 0 | 1 | 单邻居重叠 |
| `rKeOaLvo` | 0.9060 | **0** | 0 | 1 | 单邻居重叠 |
| `KPrGMEe1` | 0.9991 | **0** | 0 | 1 | 完全被定价（另有 3 颗在 0.6–0.7） |

⚠ **口径更正**：此前把 `[0.7,0.8)` 写成「n ≥ 1」是错的 —— 四条全是 **n = 0 + 单一邻居落在 ~0.90**，
形态属**单 alpha 重叠**，不是 `[0.9,1]` n ≥ 10 那种族级饱和。真正适用的是 D0-P 的
「prod ≥ 0.75 ⇒ `dead_end`」这一条，不是「族已饱和」这一条。
#5/#8/#9/#10 是**同一表达式结构的四种窗口/平滑变体**（prod 0.9000–0.9060，差 0.006），
#6 是另一个已被完全定价的信号（0.9991）——**降 prod 的唯一合法杠杆是换中性化，不是换窗口**；
而这四条全属 `analyst_consensus`，正落在**已点亮的 analyst 塔**（用户 2026-10-20 明令「已点亮塔先不回测」），
故该杠杆对它们**不可用**，只能换机制。

### 3.1 提交队列全量分诊（2026-10-21T18:38–18:47，`check_correlation(refresh=True)`）

`get_submit_ready(region="USA")` 的 10 条 READY 全部逐条实测，**无一条可提交**：

| alpha | 快照指标 | prod（本轮实测） | 近线桶形态 | 结论 |
|---|---|---:|---|---|
| `58gp1wdz` | S1.89 / F1.18 / 2Y1.72 / SUB0.94 | **0.9868**（17:49:50 重测） | `[0.7,0.8)` 0 / `[0.9,1]` 1 | 拒提（**同一颗 16:04 读数 0.6738，两小时内上漂 0.31**） |
| `A1QvkXol` | S1.94 / F1.38 / 2Y1.88 / SUB1.04 | **0.8731** | `[0.7,0.8)` 5163 / `[0.8,0.9)` 500 | 拒提（workforce 族饱和） |
| `akVxompO` | S1.89 / F1.31 / 2Y1.90 / SUB0.84 | **0.8586** | 5352 / 251 | 拒提（同上） |
| `GrgOk2qO` | S1.69 / F1.26 / 2Y1.89 / SUB0.96 | **0.9078** | 9580 / 884 | 拒提（同上） |
| `bl8OpAkr` | S2.09 / F1.96 / 2Y2.23 / SUB1.56 | **0.9745** | 1293 / 176 | 拒提（web_traffic 族饱和） |
| `RRA6XP3j` | S2.17 / F2.07 / 2Y2.21 / SUB1.69 | **0.9740** | 1317 / 180 | 拒提 |
| `omoW2ZO2` | S1.97 / F1.54 / 2Y2.07 / SUB1.26 | **0.9908** | 1948 / 234 | 拒提 |
| `58jgRYWX` | S1.74 / F1.48 / 2Y1.93 / SUB1.09 | **0.9781** | 2060 / 224 | 拒提 |
| `pw5RbrYX` / `leKKGb9l` | 见 §1 #5/#9 | 0.9000 / 0.9014 | 0 / 1 | 拒提 |

另外两颗同族强信号（不在 READY 队列，DB 内查出后一并实测）：
`N1QMJ10q`（S 2.42 / F 1.47 / **2Y 4.25**，塔位 **USA/D1/EARNINGS**）prod **0.8262**，
近线桶仅 `[0.7,0.8)` 4 / `[0.8,0.9)` 1 —— 形态是**5 条邻居**而非族级饱和，但 `prod ≥ 0.75` 按 D0-P 即判死；
且 earnings 塔本季已亮（用户 2026-10-20 明令「已点亮塔先不回测」）⇒ 该族不再扩批。

⚠ **本轮最重要的一条口径实证**：`58gp1wdz` 在**同一会话内的两小时**里从 0.6738 漂到 0.9868。
它不是缓存 bug（两条都是平台实测、都落了 `alpha_corr_cache`），而是生产池在动。
⇒ **「0.6738 / 余量 0.026」这类读数不能作为提交依据，必须在提交前当场重测**；
`get_submit_ready` 的 `corr_age_hours` 再小也一样（0.8 h 也不算新鲜）。

**缺口只能来自新机制**：本季 USA/D1 仅 `model=4 / analyst=1 / earnings=1` 亮着，
已亮塔不作主数据集；`value/quality/book` 种子全死（book/value 单族 145 颗同族 ACTIVE）。
本轮在 Fundamental 侧把**最后一个未开采数据集 `fundamental2` 也封存**（机制上限 +0.97，距 1.58 线 0.61，
见 [`_usa-fundamental2-field-profile-20261021.md`](../../Claude/skills/wq-brain-ra-usa/references/_usa-fundamental2-field-profile-20261021.md) §5），
并关闭 D0（delay 0）旁路 —— USA/D0 的 RA 门槛是 **S 2.69 / F 1.5 / 2Y 2.69**，
实测最强 2.13 / 0.98 全部不达标（见 `rules/gate-and-submit-discipline.md` §九）。
⇒ 截至本报告，**USA 侧「未判死 × 可开采」的 Fundamental 库存归零**，剩余 5 个缺口没有可用的既有机制。

---

## 4. 库存盘点（为什么不再扩批）

| 数据集 | 结论 | 依据 |
|---|---|---|
| `fundamental2` | **封存（2026-10-21）** | 八族同号负（−0.57…−1.00），镜面上限 +0.97；`quantile` 仅 +0.02 |
| `fundamental14`（208 董事字段） | 不投 | 与 `board_gov_stats` 同机制，后者 prod 0.8508 |
| `pv87`（2364 ESG 质量评级） | 不投 | 质量族在 USA 无全期 alpha，prod 先验已死 |
| `stock_search_trends` | **封存（2026-10-21，改判）** | 7/7 条实测 prod **0.8244–0.9382**（跨 3 种中性化 / 3 种窗口 / 反号与平滑全部 ≥ 0.75）⇒ `USA-STOCK-SEARCH-TRENDS-PROD-SAT`，是**机制级**饱和不是构造问题；`9qE7WOxr` 留作 SUPER 组合腿 |
| `web_traffic_engage` | **封存（2026-10-21）** | 水平族 prod 0.9740 / 0.9906；变化量腿（E8/E10）与份额腿实测 **0.9781 / 0.9782** ⇒ 五条互不相同机制全 ≥ 0.974 ⇒ `USA-WEB-TRAFFIC-PROD-SAT`（附录 AB） |
| `workforce_flow_skills` | **封存（2026-10-21）** | 10 条探针里 7 条 S ≥ 1.25、**4 条 RA 全闸**、rns 1.55–2.13、0 CW —— IS 侧是本轮最好的新数据集；但四条 prod **0.8586 / 0.8731 / 0.8829 / 0.9078** ⇒ 逐条 D0-P `dead_end` + `USA-WORKFORCE-PROD-SEAL`（附录 AE） |
| `other699`（散户逐笔成交） | **判死（2026-10-21，批 7 止损成立）** | 10/10 COMPLETE：最优 S 1.25 / F 0.51 / 2Y 1.93；bucket 族把 SUB 缺口解决（比值 0.576–0.812 全过）但 S 上限 1.25，幅度门控族（C/D）S 0.69–0.78 + SUB 0.10–0.16 + CW 失败 ⇒ 结构与「选名靠活动度」互斥，见 `_usa-other699-field-profile-20261021.md` §4.16 / §5 |
| `other545`（Linked Firms Momentum / NEMO 2.0） | **判死（2026-10-21）** | 3 批 25 条：事件向量**近似退化**（`vec_max ≡ vec_min ≡ vec_avg`，S/F 逐位相同、TO 差 <0.001）；最优壳 `quantile(group_rank(·, subindustry))` S 0.83 / F 0.48 / 2Y 0.72，距闸 1.9×，两个结构假设（分歧=置信、宽度=选名）全被证伪，见 `_usa-other545-field-profile-20261021.md` §5 |
| `institutions18`（机构持股占比） | **判死（2026-10-21 实测）** | 三条 RA 全闸：`88PmKRzv` S1.81/F1.44/2Y1.96/SUB0.99/TO1.93% **prod 0.9493**（平台直测 225s）；`JjQV5ep2` S1.73/F1.30/SUB0.84 **prod 0.9344**（407s 重测命中，直方图 `[0.7,0.8)` 987 条 / `[0.8,0.9)` 19 条）；`GrOq3WLP` S1.71/F1.33/SUB0.80 两轮轮询均被 `ConnectionResetError 10054` 打断、未取到读数。**已测两条全部过 D0-P 死线（≥0.75）**，机制（机构持仓水平→慢变量）与已死族正交但同样被定价 ⇒ 整族按 `USA-INSTITUTIONS18-PROD-SEAL` 封存；这也关闭了库存里最后一条未测的类别 |
| `other571`（Viewership Attention） | **双杀封存（2026-10-21）** | IS 天花板 **S 1.51**（`ZYmAVRo8`，差 1.58 线 0.07）+ prod **0.9087**（平台直测 405 s）⇒ `USA-OTH571-DOUBLE-KILL`。四波 30 条已把「归一 / 平滑 / 结构」三条轴走完：`decay` 10→15→22 只降 S（1.51/1.50/1.47）；`group_rank(subind)` 是负贡献；`ts_backfill` 把 S 从 1.51 砸到 0.69；`hump(0.01)` 把 S 打到 −0.27；换 MARKET 壳 S 0.96。见 `_usa-oth571-field-profile-20261021.md` §4 |
| `pv63`（逐笔订单流失衡） | **判弱结案（2026-10-21，3 批 30 条）** | 最优点 `QPYYZavW` = 吸收交互（计数失衡 × **−**5 日收益）**S 1.15 / F 0.48 / 2Y 1.06 / SUB 0.86 / DD 5.09% / TO 31.9%**；其镜像（× **+**5 日收益）只 0.29 / 0.30 ⇒ 方向性判决：信息是**吸收/反向**，不是动量确认。要 S1.58+F1.0 在该换手下需 12.8% 年化（实测 5.57%）⇒ 差 2.3 倍，**结构性不可达**。另三条负结果：事件门控（放量日）把 0.85 打到 0.15；`ts_zscore` 2Y 1.14 但 S 0.47 / SUB −0.38（水平 > 意外）；挂单占比 5.27% 换手却 24.7% 回撤。见 `_usa-pv63-field-profile-20261021.md` §5–§7 |
| `order_flow_imb`（期权参与人订单流，**option 塔 ×1.3**） | **D15 判死（2026-10-21，批 1）** | 120 MATRIX 字段 / cov 0.906 / ac 478 / valueScore 3；6 角色 × 5 形态 × 4 版本。10/10 COMPLETE，**最优 \|S\| = 0.35 且符号为负**（customer 镜面 +0.34，firm/pro_customer/proprietary 0.10–0.21，market_maker −0.21，firm−customer 价差 −0.35 只是分量的线性后果）；TO 29–43% 且**平滑让它更差**（与 pv63 相反 ⇒ 无慢成分）。D15：8 探针无 \|S\|≥0.5 ⇒ dead；上限外推 ≈0.76 < 1.58 的一半。见 `_usa-order-flow-imb-field-profile-20261021.md` §5 |
| **`analyst_consensus` · FA overlay 族** | **族内收尾（2026-10-21，7 批 67 条）；同数据集已转新机制** | `mean_forecast_actual_combined_*` = 「预测+实际」叠加单序列，**平台字段总数 3424 / 本族 147 行（92 个指标）**（旧 300 清单是 `max_fields` 截断）。七批读数：**全闸只有 2 条** —— `e76xgXkM`（eps 年线 1.89，已交付）与 `0mjj3deK`（fxadj reported 年线 **1.76/1.00/1.73/SUB 0.76 压线**；prod **0.7204** + self **0.7206** 双卡 ⇒ D0-P 唯一一次结构尝试换 SUBINDUSTRY ⇒ F 1.00→0.85、TO 3.36%→0.93% 破地板、SUB 反降到 0.60 ⇒ **dead_end**）。**终局判据**：S 与 SUB/S≥0.43 必须同时过线，21 个指标里只有这 2 条做到。批次 3 证伪 `ts_rank` 轴；批次 4 证明 `decay`/`hump` 是 2Y 杠杆且与 SUB 对抗、壳层对 S 零位移；批次 5 证明 `group_rank` 粒度是**第三条轴且字段特定**（assets S 1.47→**1.71**、SUB 比值 0.48→**0.591**；roe 反而 1.45→1.41）；批次 6 走 **level 轴**得 `P0MMd7G7` S1.74/F**1.09**/RET4.91%/SUB 0.83(0.75) **全平台绿、只缺 2Y 1.37**（prod 0.7435、[0.7,0.8) 直方图 n=25；0.21 的 2Y 缺口无杠杆 ⇒ dead_end）；批次 7 用 assets 的 0.27 SUB 余量买 2Y，9 臂全败（decay 30 反而同抬 2Y **与** SUB，代价是 S −0.08 ⇒ F 破；短窗把 2Y 打到 1.06/1.16）。见 `_usa-analyst-consensus-fa-overlay-field-profile-20261021.md` §5–§11 |
| `other685` / `option3` / `pv47` / `pv103` / `pv115` / `dl_volume_pred` / `insiders4` / `board_gov_stats` / `earnings_risk` / `news_sentiment_transfer` / `sentiment26` | 已判弱 / 已封存 | 逐条见交付日志 §2 |
| **`intraday_pv_feats`**（分钟线 PV 截面） | **封存（2026-10-22，4 批 25 条）** | corr-reversal 分支 prod **0.8693 / 0.8739** ⇒ D0-P 直接判死；尾盘 `high_price` 分支 prod **0.7429**，D0-P 允许的那**一次**结构尝试已由 CROWDING 臂消耗且实测为**负杠杆**（S 1.39→1.04，−0.35）⇒ `dead_end`。机制三条：① 收益全在尾部 —— 唯一能过 Fitness 的壳（fat-tail zscore）恰是 prod 最高的壳；② 任何降 prod/降 CW 的有界化把 RET 13.4%→4.3–6.5%，F 随即掉出 1.0；③ 降换手会把 TO 打进地板。**结构性互斥，不是参数问题**。见 `_usa-intraday-pv-feats-field-profile-20261022.md` §7 |
| **`news_transformer_scores`** | **low-yield 判死（2026-10-22，批 22 八臂）** | 8 条最高 \|S\| **0.50**（A4 负向）/ 正向最高 0.46，远低于预登记线（S≥1.00 且 F≥0.60）⇒ 首批无苗。唯一近「残余 alpha」的是 B3 镜像（做空高正面情绪 S≈+0.42、rns≈0.37），但该族本身是已证 **prod 0.72–0.83** 的人群面 ⇒ 轮换批不授权、不再投入仿真。方向性结论可复用：**「高正面情绪 → 未来跑输」（S −0.42 / 2Y −1.37）**，与情绪过度定价文献一致。见 `_usa-news-transformer-scores-field-profile-20261022.md` §4.2 |
| **`fundamental21`**（ESG Scores） | **判死（2026-10-22 封板）** | 覆盖率**结构性偏大盘**（与 universe 选择无关的判死理由）；最优 S 上限 1.52 / 1.23 均不过线。见 `_usa-fnd21-field-profile-20261021.md` 终判节 |
| **`fundamental1`**（17 张报表科目 / 全 VECTOR） | **`dead_end`（2026-10-22，数据集级，20 臂）** | 批 27 + 批 28 共 **20 臂 / 15 字段**，跨 **3 类变换**（`ts_av_diff` / `ts_zscore` / `ts_rank`）× **2 种形状**（`quantile(group_rank(...))` 与裸 `rank`），**两轮 max \|S\| 都是 0.94 且逐位相同** ⇒ 变换与形状两条轴均已穷尽。判死四条：① 强度上限 0.94 ≈ 0.6×闸线；② rank 在 3/3 组里优于 zscore ⇒ 尾部驱动而非中心趋势；③ size/network 族负向且 `risk_neu_S` 同负（L9 −0.91）⇒ 是真实但微弱的 **quality discount**，非风格伪装；④ TO 1.63–2.14% ⇒ 信息到达频率**结构性年频**，无法靠窗口提速。见 `_usa-fnd1-field-profile-20261022.md` §8 |

**可复用的跨数据集结论**（已写入交付日志与各画像）：
1. **`rns`（risk_neutralized_sharpe）是比 Sharpe 更低一级的判据** —— 接近 0 即纯风格暴露，
   不论 IS 多好看都别花仿真（`fundamental2` 正向 0.50–0.52 即典型）。
2. **同一族的镜面必然逐位对称**（±0.84 / ±0.95 / ±1.00）⇒ 符号翻转不产生新信息，
   「反向变体」只在原方向被定价时才值得单独跑。
3. **`quantile()` 在慢变量上几乎不加分**（+0.02，三次复证）；同簇换字段的增益更大（+0.12）。
4. **prod 直方图 `[0.9,1]` 桶 n ≥ 10 = 族级饱和**，不必再测同族（`pv47` 24 条 / `workforce` 全族）。
5. **delay 0 不是便宜门票**：塔位空不等于门槛低，平台对 delay-0 把 Sharpe / Fitness 线抬了约 70%。
6. **高 `rns` 不防 prod 饱和（2026-10-21 新增，workforce 实证）**：rns 1.84–2.00、0 CW、四条 RA 全闸，
   prod 仍 0.86–0.91。rns 只回答"信息是不是规模/行业伪装"，prod 才回答"平台里有没有人挖过"——
   **两个问题必须分开测**，缺后者 = IS 再漂亮也是白干。这是连续第三个「IS 完美 / prod 死」的数据集
   （web_traffic_engage 0.974–0.991、analyst 目标价族 0.90–0.999、workforce 0.86–0.91）。
7. **稀疏事件字段的壳陷阱（2026-10-21 新增，other699 实证）**：比率型信号（`x / 持仓`）在「新开仓 ⇒ 分母为 0」
   时会产生大量同值极值，`winsorize(std=4)` **压不住**（它不是分位裁剪），结果就是 `CONCENTRATED_WEIGHT`。
   修法是逐股时序分位 `ts_rank(<SIG>, 252)`：有界 + 自带规模中性化，代价是丢弃跨股绝对强度。
8. **`ts_backfill` 对"变化量 / 事件"字段是污染，不是补全（2026-10-21 新增，other571 实测）**：
   覆盖率缺口在这些数据集里是**结构性 NaN**（该股当期没人交易 / 没被持有），补全等于把陈旧值铺进
   "本应无信号"的区间，实测 S 1.51 → **0.69**（66d）/ 0.67（252d）。判据：先看 `count_*` 类字段
   是否 cov=1.0（返回 0 而非 NaN）——是则说明 NaN 语义是"没有"，禁用 backfill。
9. **`hump` 只适用于慢变量（2026-10-21 新增）**：同一个 fast 信号（`decay10`）上 `hump(0.01)` 把
   S 从 1.51 打到 **−0.27**、换手压到 2.4% —— 它不是"平滑"，是**用换手预算换持仓粘性**，
   对持仓期只有数日的信号等于换成另一个（无信息的）信号。快信号用 `decay`，慢信号才用 `hump`。
10. **`ts_rank` 是唯一抗 backfill 的归一（2026-10-21 新增）**：`ts_rank(backfill(F,66), 252)` 把
    被 backfill 砸到 0.69 的信号拉回 **1.28**（有界 + 逐股时序归一），但仍低于不 backfill 的 1.51
    ⇒ 能救噪但救不回信息。
11. **"流量 × 价格"的交互项必须**成对**跑（2026-10-21 新增，pv63 实证）**：同一基信号（计数失衡 mean5）
    `× (−5日收益)` = **S 1.15 / 2Y 1.06**，`× (+5日收益)` = **0.29 / 0.30**。四倍差距不是窗口噪声，
    而是**信息属性判决**：该流量是吸收/反向的，不是动量确认的。只跑一个符号 = 有一半概率把
    一个有信息的机制误判成噪声。**交互项成对，是"归因先于扩批"的最小成本实现。**
12. **流量型日频数据集的水平 > 意外（2026-10-21 新增，pv63 实证）**：`ts_zscore(·,22)` 把 2Y 抬到 1.14
    但 S 砸到 0.47、SUB −0.38 ⇒ Change 表示摧毁了截面水平信息。与 other566「持续状态的水平才是信号、
    修正是噪声」同向，但两条数据集一个是图像模型输出、一个是逐笔成交 —— **两类不同数据同一条规律**，
    可信度高于单集观察。
13. **事件门控在"天天有信号"的流量字段上是负贡献（2026-10-21 新增，pv63 实证）**：
    `trade_when(ts_rank(vtni,22) > 0.7, mean5(失衡), -1)` 把 0.85 打到 **0.15** ⇒ 信息是弥散的、
    放量日反而更噪。判据：先看信号在**低活动日**是否也成立（分组读数），再决定要不要加活动度门控；
    对逐笔/逐日流量，门控更可能是把有效样本砍掉而不是提纯。
14. **`LOW_SUB_UNIVERSE_SHARPE` 不是独立闸，是 S 的缩放线：闸值 = 0.43 × S，全程线性、无地板（2026-10-21 新增，
    21 条实测，批次 3 更正）**。逐点核对 S→SUB：1.89→0.81、1.82→0.79、1.76→0.76、1.57→0.68、1.47→0.63、
    0.99→0.43、**0.93→0.40**、0.66→0.29（比值恒 0.43±0.01）。⚠ 早前写的「S < 1.0 触 0.43 地板」**已证伪**
    （`O0JJPkb1` S0.93 的闸值是 0.40，0.99→0.43 只是 0.426 的进位）。**推论**：① 「把 S 拉过 1.58 就顺带修好 SUB」
    不成立——抬 S 会**同步抬闸值**，比值不变就永远差同样的相对量；② 唯一结构性修法是把 **SUB/S 比值**从 0.20–0.38
    抬到 ≥0.43，而比值是**信号在大票与小票上是否同样有效**的度量——只能换内容（字段/科目线）或换分组/中性化，
    不能靠平滑（§16 给出平滑为什么反而有害）；③ 全族 21 条里比值过线的只有 6 条，其中同时 S≥1.58 的仅
    `e76xgXkM`（0.56，已交付）与 `0mjj3deK`（0.432 压线，prod/self 0.72 双卡）。
15. **「预测→实际」叠加序列（`mean_forecast_actual_combined_*`）的机制是盈利兑现，不是"每股"、也不限于盈利
    （2026-10-21 新增，FA overlay 批次 1+2 共 20 条）**：① 每股口径被证伪 —— `bvps` 0.92 / `dividend` 0.34
    与 `eps` 1.89 不在同族；② 盈利族被扩展 —— `interest_expense_annual12` **1.53** 说明融资成本线是第二条通道；
    ③ **reported（GAAP）> adjusted（street）**：同一 horizon 同一壳，`eps_reported_quarterly16` **1.80** vs
    `eps_quarterly16` 0.95 ⇒ 主效应是报表口径，horizon 是二阶（年 1.89 vs 季 0.95 只在 adjusted 内成立）；
    ④ 顶线与慢存量（`revenue` 0.99 / `nav` 0.97 / `cfo` 0.90 / `pretax` 0.66 / `capex` 0.64）是死区 ——
    年度顶线预期已被 guidance 提前锁定，其变化率主要是年度滚动的机械项。**排序规则**：同科目先试 `reported`，
    再试 `annual`，两者叠加最强。
16. **`decay` / `hump` 是「2Y 杠杆」，且与 SUB 直接对抗（2026-10-21 新增，批次 4 九条对照）**：同一条线
    `fxadj_eps_reported_quarterly16` 四档给出整齐反向配对——decay 20→30：**Δ2Y +0.13 ↔ ΔSUB −0.10**；
    `winsorize std=2`：+0.07 ↔ −0.03；`hump 0.01→0.005`：+0.05 ↔ −0.05（`netprofit` 上 hump 同样 +0.13 ↔ −0.07）。
    机制：慢化 = 持仓更粘 = 近两年更稳，但同一时点覆盖的票更少。**判据**：当一条线**同时**缺 2Y 与 SUB 时，
    平滑类杠杆在原理上救不了它（每个杠杆都在修一个的同时弄坏另一个）——直接判死，别再换档。
    同批还复证：**壳层杠杆对 S 是零位移**（`netprofit` 四个壳 1.81–1.84、`eps_rep_q16` 四个壳 1.78–1.81，
    极差 ≤0.03），S 只由内容决定。
17. **prod 相关性是时间函数，入库读数不等于现值（2026-10-21 新增，同日两次打脸）**：`pw5RbrYX`/`leKKGb9l`
    在库里的 prod 是 0.5857/0.5896（10-17 写入），10-21 实测 **0.9000/0.9014**；`58gp1wdz` 三小时前 0.6738，
    本次 `refresh=True` 复测 **0.9868**。**纪律**：`get_submit_ready`/`alphas.prod_correlation` 只作线索，
    任何候选进交付表前必须 `check_correlation(refresh=True)` 复测；当天有新 alpha 落地就会把全池推高。
18. **Fitness 是 (S, RET) 的导出量，不是独立旋钮：`F = S · sqrt(|RET| / max(TO, 0.125))`（2026-10-21 新增，
    5 个独立臂逐位核验到小数点后两位）**。低换手族（TO < 12.5%，本项目几乎所有慢变量族都是 3–5%）
    于是 **F ≥ 1 ⇔ RET ≥ 0.125 / S²**：S 1.71 需 4.27%、S 1.74 需 4.13%、S 1.83 需 3.73%。
    核验：1.67·√(3.69/12.5)=0.907→平台 0.91；1.73·√(3.75/12.5)=0.948→0.95；1.59·√(3.51/12.5)=0.843→0.84；
    1.74·√(4.91/12.5)=1.091→**1.09**；1.92·√(5.34/12.5)=1.255→**1.25**。**用法**：选波阶段零仿真成本先算
    「这条信号形态的 RET 能撑到多高的 S」——change 轴 RET 3.6–3.8% ⇒ 需 S ≥ 1.82（该轴 21 条上限 1.71
    ⇒ F **结构上**过不去）；level 轴 RET 4.9–5.3% ⇒ S ≥ 1.55 即可（实测 1.74/1.92 全过）。
    **RET 由信号形态（level vs change、reported vs adjusted）决定，改壳改不出来** —— 这条把「F 不足就调参」
    从候选动作里删掉了。
19. **定律 16 的 `decay`↔SUB 对抗**不普适（2026-10-21 批次 7 九臂）：同一 `assets` 线 decay 20→30
    把 2Y 1.31→1.36 **同时** SUB 1.01→1.03（两个都涨），真实代价转移到 **S 1.71→1.63** ⇒ F 0.94→0.87。
    ⇒ decay 是「**S 换 2Y**」的兑换（汇率约 0.08 S : 0.05 2Y，明显不划算），不是免费杠杆；
    而**短窗**（`ts_zscore` 252→126、`ts_av_diff` 63→22）把 2Y 打到 1.06 / 1.16 ⇒ 本族是长窗支持 2Y。
    同时补一条轴结论：level 轴与 change 轴**各缺一条不同的腿**（level：SUB 富 / 2Y 穷；change：2Y 富 / SUB 穷），
    且不能相加（混信号），所以「同字段双轴」不构成解法。
20. **同数据集换机制比换数据集更值钱：四条新机制里有两条只差 SUB（2026-10-21 批次 8 十臂）**。
    冻结壳不变，把核心从「预期+实际叠加序列」换成**纯预期快照**后，RET 立刻变厚：
    **修正（`mean_estimate` / 3 月前快照）S1.71 / F1.15 / RET5.62% / 2Y1.66 / SUB0.67（限 0.74）**、
    **意外（`mean_surprise_value` / 实际值归一 + `ts_mean` 504 的 PEAD 慢变量）S1.62 / F1.21 / RET**6.93%** / 2Y1.96 / SUB0.52（限 0.70）**。
    两条都只缺 SUB（比值 0.392 / 0.321，线为 0.43）⇒ **上一族「F 结构性不可达」的死结被 RET 厚度打开**，
    定律 18 的 RET ≥ 0.125/S² 在新机制下有余量。三条结构事实：
    ① **覆盖（estimate_count）当主腿判死**（S 0.53 / 0.57）——只能当质量过滤器，与论坛结论一致；
    ② **分歧窗口越长越好**（4 周 2Y 0.75 → 3 月 1.51/1.70），与「公告后 1–2 个月收敛」的时标吻合；
    ③ **EPS 口径在修正与意外上全面强于营收**（1.71 vs 0.85、1.62 vs 1.15），与论坛「营收 surprise 更干净」
    相反，但本集营收 prior 快照后缀族不齐（`_tribes` vs 无 `_3`），属口径疑点不是否证。
    SUB 缺口集中在 EPS 意外的**组合广度**（同机制营收版 SUB 比值 0.478 过闸、EPS 版 0.321 不过）——
    这是持仓集中问题，故下一批只动广度杠杆（`group=subindustry`）与中性化域，不动信号。
    ⚠ **「持仓广度」这条猜测已被批次 9 十臂否证**（2026-10-21）：`group=subindustry` 是 **SUB 负杠杆**
    （修正线 0.392→0.321），且各臂多空持仓数同量级（1520–1605，含 SUB 过闸的 `e76xgXkM` 1554/1572）
    ⇒ SUB 是**内容问题**不是广度问题；唯一动过 SUB 的旋钮是 `neutralization=SUBINDUSTRY`
    （修正线 0.416 本族最好），代价是换手塌到 0.90% 踩地板。见画像 §13.1 / §14。
21. **`hump` 在「跳变信号」上是阶跃检测器，不是平滑器：拆掉它会换掉信号（2026-10-21 批次 10 五臂）**。
    EPS 修正线上把 `hump(0.01)` 拆掉，换手 0.93% → 3.4~4.1%（×3.5），但 **S 1.81 → 1.04、SUB 0.77 → 0.32**，
    d20 / d10 两档逐位同形 ⇒ 断崖不是噪声。机制：`ts_zscore(修正率,252)` 的日间变化绝大部分是
    **窗口滚动漂移**（无信息），信息只在**修正跳变日**，`hump` 死区把漂移挡在门外 —— 拆掉它等于
    把「慢漂移」当主信号。与定律 9（快信号上 `hump` 会毁信号）合起来才是完整图景：
    **hump 只在「信息是跳变、噪声是漂移」的序列上是增益项，其余场合是破坏项。**
    同时实测：**`decay` 不动换手**（0.93% vs 0.93~0.96%），只动 SUB（d20 0.77 vs d10 0.70）
    ⇒ 在阶跃类信号上「抬换手」只能动 hump 阈值或 z-score 窗；这也是本族最好臂 `kqJJkRNO`
    （S1.81 / F1.14 / 2Y2.42 / TO0.93% / SUB0.77@0.78）两条线都只差一线的根因。
22. **「SUB↑ 与 prod↑ 同源」：壳层旋钮买不到 SUB 而不付 prod（2026-10-21 批次 11 五臂）**。
    批次 11 用「hump 死区 + `neutralization=SUBINDUSTRY`」把 EPS 修正线的 SUB 比值从 0.392 抬到
    0.489–0.586，**四臂首次全过 IS 五线**（S 1.62–1.85 / F 1.10–1.20 / 2Y 1.93–2.49 / TO 1.00–1.84% / SUB 0.79–0.99）。
    但三条 `check_correlation(refresh=True)` 读数：`LL55qPoe` **0.8463**、`RRAAqJw0` **0.7868**、
    `e766glZ6` **0.8459**，且 `[0.7,0.8)` 桶 n = 4776 / 1004 / 4283 —— 按
    `wq-window-valley-break-prod-wall` 的族级判据（**n≥1 必死**）窗口微调不授权，D0-P 直接 dead_end。
    机制：低换手不是「更分散」，是**只在少数跳变日下注**，与平台现存修正类 alpha 的持仓重合
    ⇒ 抬 SUB 的那两个旋钮同时把组合推向人群。**对该信号族，改壳改不出可提交体，只能换核（新机制 = 新 prod 指纹）。**
    EPS 3 月修正记 `USA-ANLST-FA-REVISION-PROD-SEAL`，后续臂全部转同壳换核（GAAP NI / 税前 / EBIT 修正、净利润意外）。

---

## 5. 产物索引

| 内容 | 路径 |
|---|---|
| 交付日志（10 颗逐条 + 全库封存台账） | [`_usa-atom-delivery-log-20261020.md`](../../Claude/skills/wq-brain-ra-usa/references/_usa-atom-delivery-log-20261020.md) |
| analyst_factor_signals 字段画像 | [`_usa-analyst-factor-signals-field-profile-20261019.md`](../../Claude/skills/wq-brain-ra-usa/references/_usa-analyst-factor-signals-field-profile-20261019.md) |
| analyst44 战役档案 | [`_analyst-campaign-20261017.md`](../../Claude/skills/wq-brain-ra-usa/references/_analyst-campaign-20261017.md) |
| analyst_consensus 字段画像 | [`_usa-analyst-consensus-field-profile-20261020.md`](../../Claude/skills/wq-brain-ra-usa/references/_usa-analyst-consensus-field-profile-20261020.md) |
| fundamental2 字段画像（本轮新增） | [`_usa-fundamental2-field-profile-20261021.md`](../../Claude/skills/wq-brain-ra-usa/references/_usa-fundamental2-field-profile-20261021.md) |
| web_traffic_engage 字段画像（含批 1 十条实测，本轮新增） | [`_usa-web-traffic-engage-field-profile-20261021.md`](../../Claude/skills/wq-brain-ra-usa/references/_usa-web-traffic-engage-field-profile-20261021.md) |
| stock_search_trends 字段画像（含 7/7 prod 实测与改判） | [`_usa-stock-search-trends-field-profile-20261020.md`](../../Claude/skills/wq-brain-ra-usa/references/_usa-stock-search-trends-field-profile-20261020.md) |
| other566 字段画像（4 批 36 条 + 判死） | [`_usa-other566-field-profile-20261021.md`](../../Claude/skills/wq-brain-ra-usa/references/_usa-other566-field-profile-20261021.md) |
| pv63 字段画像（3 批 30 条 + 判弱结案，本轮新增） | [`_usa-pv63-field-profile-20261021.md`](../../Claude/skills/wq-brain-ra-usa/references/_usa-pv63-field-profile-20261021.md) |
| order_flow_imb 字段画像（120 字段解剖 + 批次 1 + D15，本轮新增） | [`_usa-order-flow-imb-field-profile-20261021.md`](../../Claude/skills/wq-brain-ra-usa/references/_usa-order-flow-imb-field-profile-20261021.md) |
| analyst_consensus · FA overlay 族画像（3424 字段口径更正 + 批次 1–5 设计与归因，本轮新增） | [`_usa-analyst-consensus-fa-overlay-field-profile-20261021.md`](../../Claude/skills/wq-brain-ra-usa/references/_usa-analyst-consensus-fa-overlay-field-profile-20261021.md) |
| analyst_consensus · FA overlay **全族字段画像清单**（147 字段 / 92 指标 / 21 条实测读数 / 未测候选按经济通道分组，本轮新增） | [`_usa-analyst-consensus-fa-overlay-field-inventory-20261021.md`](../../Claude/skills/wq-brain-ra-usa/references/_usa-analyst-consensus-fa-overlay-field-inventory-20261021.md) |
| Fundamental 数据集扫描 | [`_usa-fundamental-dataset-scan-20261019.md`](../../Claude/skills/wq-brain-ra-usa/references/_usa-fundamental-dataset-scan-20261019.md) |
| 字段族判死速查（rns 口径） | [`_usa-field-profile-playbook-20261018.md`](../../Claude/skills/wq-brain-ra-usa/references/_usa-field-profile-playbook-20261018.md) |
| 闸门与提交纪律（含 D0 门槛分档） | [`gate-and-submit-discipline.md`](../../Claude/skills/wq-brain-ra-usa/rules/gate-and-submit-discipline.md) |

---

## 6. 追补：MODEL 塔 `ai_equity_alpha`（2026-10-23）

### 6.1 为什么加这个数据集

原 5/10 的缺口全部来自 prod 破 0.7（analyst 族拥挤）。要补 5 颗，必须换**机制**而不是换窗口。
`ai_equity_alpha`（dataset id 294，category **MODEL**，pyramid `USA/D1/MODEL` **×1.3**，1108 字段，
dataset alpha_count 696 但 776/1108 字段 alphaCount=0）提供了一条此前完全没挖的机制：
**同一模型的多个版本/方法对同一目标的预测分歧**（不是「预测值水平」，而是「模型之间不一致」）。
字段画像：[`_usa-ai_equity-alpha-field-profile-20261023.md`](../../Claude/skills/wq-brain-ra-usa/references/_usa-ai_equity-alpha-field-profile-20261023.md)

### 6.2 第 6 颗（**已过 RA 全闸 + 相关性 + 稳健性 CONDITIONAL，待用户确认提交**）

| 项 | 值 |
|---|---|
| alpha | **`YPx89bQJ`** |
| 数据集 / 塔 | `ai_equity_alpha` / `USA/D1/MODEL`（×1.3） |
| 核心字段 | `predicted_earnings_surprise_2` − `predicted_earnings_surprise_3`（两代盈利意外预测分歧） |
| 算子逻辑 | `ts_decay_linear(group_rank(ts_zscore(ts_backfill(subtract(vec_avg(A), vec_avg(B)), 252), 252), subindustry), 5)` |
| 设置 | USA / TOP2000 / D1 / STATISTICAL / platform decay 0 / trunc 0.08 / VERIFY / nan ON / 2014-01-01→2023-12-31 |
| 指标 | S **2.19** / F **1.16** / 2Y **1.91** / SUB **1.24**（limit 1.19）/ TO 15.69% / RET 4.39% / DD 2.92% / margin 5.6 bp / long 1032 · short 1047 |
| RA 闸 | `failed_ra_count = 0`；warning 仅 CLUSTER_TEST 1.04（limit 1.58）、MATCHES_THEMES、OSMOSIS_ALLOCATION |
| 相关性 | prod **0.6803**（<0.7，余量 0.020）/ self **0.2812**（对 `O08EjLVp`） |
| 稳健性 | **CONDITIONAL**（recent-3yr S 1.79 ≥1.58；CV 0.48；衰减比 0.416；max/min 3.25）；无硬标记 |
| 稳健性报告 | [`reports/robustness_20261023.md`](../../reports/robustness_20261023.md)（`robustness_YPx89bQJ`） |
| 状态 | `submit_ready` READY；**未提交**，提交需用户明确确认（不可逆） |

风险三条，提交前一并交代：① prod 0.6803 距 0.70 仅 0.020，且 prod 只向上漂；② 2023 年 S 0.91、收益显著衰减；
③ margin 5.6 bp 偏薄。稳健性三态落 CONDITIONAL 而非 REJECT，故合规上可进队列。

### 6.3 同波被否的臂（避免重复劳动）

| 臂 | 表达式核 | 结果 | 裁决 |
|---|---|---|---|
| 99b 对照组 `O08EjLVp` | 同一壳（industry, decay 5） | S2.45/F1.55/2Y2.55/SUB1.47 | 已是 ACTIVE（同族代表） |
| 99c `group_zscore` | 外层换 `group_zscore` | S0.29 | 崩，不可用 |
| 99c `sector` / `market` 轴 | 换分组轴 | S1.99/1.99、SUB 破 | 不如 subindustry |
| 99c `ts_mean(22)` 替 `ts_zscore` | 换归一化 | S1.53/F0.87 | 崩 |
| 99b `information_opacity` / `credit_default_risk_assessment_3−4` / `pure_alpha_generation` / `cashflow_trend` | 其他族分歧腿 | S 0.27 / 0.54 / 0.72 / 1.02 | 族级不足，判死 |
| `O08GeKx1`（队列遗留 READY） | `group_rank(ts_zscore(mean_estimate_targetprice_annual12_tribes,175),subindustry)` decay 230 | S1.80 / 2023 S0.36 | **稳健性 REJECT**（衰减比 0.20、max/min 7.56）→ 已从队列 retire |

### 6.4 第 7 颗：波 100 分歧腿（`financing_structure_analysis_3 − _4`）

multisim `4abGpEr4iqb1ldIsZY3CD`，10 臂全部收批（`harvest_multisim_results` upserted 10，wave=`100`）。
同壳同设置，只换字段对；4 臂 RA 全过，其中 3 臂 prod 破 0.75（D0-P dead_end），1 臂双相关性过闸。

| 项 | 值 |
|---|---|
| alpha | **`58jr102k`** |
| 数据集 / 塔 | `ai_equity_alpha` / `USA/D1/MODEL`（×1.3） |
| 核心字段 | `financing_structure_analysis_3` − `financing_structure_analysis_4`（两代融资结构评估分歧） |
| 算子逻辑 | `ts_decay_linear(group_rank(ts_zscore(ts_backfill(subtract(vec_avg(A), vec_avg(B)), 252), 252), subindustry), 5)` |
| 设置 | USA / TOP2000 / D1 / STATISTICAL / platform decay 0 / trunc 0.08 / VERIFY / nan ON / 2014-01-01→2023-12-31 |
| 指标 | S **2.26** / F **1.33** / 2Y **2.06** / SUB **1.41**（limit 1.24）/ TO 12.57% / RET 4.38% / DD 1.80% / margin 6.96 bp / long 1028 · short 1052 |
| RA 闸 | `failed_ra_count = 0`；warning 仅 CLUSTER_TEST 1.13（limit 1.58）、UNITS（CSShare 单位提示，非闸）、MATCHES_THEMES、OSMOSIS_ALLOCATION |
| 相关性 | prod **0.6818**（<0.7）/ self **0.2329**（对 `O08EjLVp`） |
| 稳健性 | **PASS**（recent-3yr S 2.25；CV 0.264；衰减比 1.23；max/min 1.96；年度 PnL 10/10 为正；maxDD 4.1%） |
| 稳健性报告 | [`reports/robustness_20261023.md`](../../reports/robustness_20261023.md)（`robustness_58jr102k`） |
| 状态 | `submit_ready` READY；**未提交**，提交需用户明确确认（不可逆） |

同波其余臂：`npAmlRr8`（accounting_forensics − _6，S2.57/F1.46/2Y2.00/SUB1.75）prod **0.7946**、
`QPYOAk6w`（intrinsic_valuation − _91，S2.33/F1.09/2Y1.94）prod **0.7761**、
`N1eLGm2e`（balance_sheet_trend − _51，S2.30/F1.23/2Y2.14）prod **0.7663** —— 三臂 IS 全闸 + 稳健闸全过，
**卡在持仓与生产池重叠**，按 D0-P 记 dead_end。`j2eoJRMO`（buzz，S2.42/F1.26/2Y1.69）仅 SUB 1.13 差 0.15，未修。

**可复用结论（prod 双峰）**：同壳同设置下 prod 由**字段对持仓**决定、与 IS 强弱无关（S 最高的 2.57 撞得最狠）；
后续同壳新字段对必须先探 prod 再投稳健链。详见画像 §11。

### 6.5 第 8 颗：波 102 buzz 分歧腿（`zqrgna91`，market 轴 + `signed_power` 壳）

波 102 十臂中 9 臂有效（1 臂 `E5VNPlEP` 平台单位不兼容：`debt_to_market_cap_ratio_metric_11 − 21` 为
`Unit[CSPrice:1,CSShare:1]` vs 无量纲，`subtract` 直接拒），仅 1 臂 RA 全闸通过。

| 项 | 值 |
|---|---|
| alpha | **`zqrgna91`** |
| 数据集 / 塔 | `ai_equity_alpha` / `USA/D1/MODEL`（×1.3） |
| 核心字段 | `buzz_intensity_score_2` − `buzz_intensity_score_11`（两代市场关注度评分分歧） |
| 算子逻辑 | `signed_power(ts_decay_linear(group_rank(ts_zscore(ts_backfill(subtract(vec_avg(A), vec_avg(B)), 252), 252), market), 5), 0.8)` |
| 设置 | USA / TOP2000 / D1 / STATISTICAL / platform decay 0 / trunc 0.08 / VERIFY / **nanHandling ON** / 2014-01-01→2023-12-31 |
| 指标 | S **2.67** / F **1.66** / 2Y **1.68** / SUB **1.47** / TO 15.8% / MDD 2.19% / margin **7.74 bp**；`failed_ra_count = 0` |
| RA 闸 | 全过；warning 仅 CLUSTER_TEST 1.29（limit 1.58）、MATCHES_THEMES、OSMOSIS_ALLOCATION |
| 相关性 | prod **0.6877**（<0.7，余量 **0.0123**）/ self **0.2866** |
| 稳健性 | **PASS**（recent-3yr S 2.187；CV 0.300；衰减比 0.614；max/min 1.90；0 平年；年度 PnL 10/10 为正；maxDD 1.10%） |
| 稳健性报告 | [`reports/robustness_20261023.md`](../../reports/robustness_20261023.md)（`robustness_zqrgna91`） |
| 状态 | `submit_ready` **SUBMIT_LAYER_VERIFIED**；**未提交**，提交需用户明确确认（不可逆） |

软标记（已如实写入台账）：① 2021Q2 / 2020Q3 单季回撤为全期均值的 2.23×（各约 0.83% book，非结构性）；
② 2017 S1.68、2023 S1.64 贴线；③ 算子 7 个；④ prod 余量仅 0.0123 ⇒ **排在余量更大的候选之后提交**。

**机制说明**：分歧腿赚的是「模型版本间对同一目标看法不一致」的修正收益——当旧版评分仍高、新版已下修（或反之），
市场在注意力/情绪层面的定价滞后即产生可交易的均值回复。`market` 轴 + `signed_power(…,0.8)` 的作用是
把原始 z 分数按交易所切分后做截面排序并放大尾部，使 TOP1000 子宇宙内的持仓分布与全宇宙更一致（本臂 SUB
1.47 明显高于同族 subindustry 壳的 1.11–1.24）。

#### 6.5.1 波 102 的 SUB 近失臂（修复批已发）

| 臂 | 字段对 | 指标 | 缺口 | 处置 |
|---|---|---|---|---|
| `78o3Rj11` | `asset_liquidity_score − _2` | S2.03 / F1.05 / 2Y2.17 / SUB **0.86** | limit 1.08，差 0.22 | 修复批（multisim `4swHZ7yC4yO9Gk3hPe6813`，8 臂：market±signed_power / exchange / subindustry decay10） |
| `KPmvM7Ex` | `earnings_per_share_growth_metric_2 − _3` | S2.27 / F1.16 / 2Y2.02 / SUB **1.11** | limit 1.20，差 0.09 | 同上（同批 8 臂） |

注意 SUB 是**比值闸**（实测 ≈ 0.53 × alpha Sharpe），提 S 会同步抬高 SUB 绝对线 ⇒ 修复目标是抬高
`sub_sharpe / sharpe` 比值本身，而不是单纯堆 Sharpe。两臂原始宽度均为 `subindustry`，本批的核心变量就是换轴。

#### 6.5.2 跳过的近失臂：`j2eoJRMO`

`j2eoJRMO`（buzz 族，S2.42 / F1.26 / 2Y1.69 / SUB 1.13 差 0.15）**不再修**：它与已入册的
`zqrgna91` 同属 buzz 分歧机制，同族两颗先后提交会把 SELF 相关性推高（历史教训：同腿近亲提交后 self 0.99+），
收益不值得承担自锁风险。留档备查。

### 6.6 第 9 颗：波 102 修复批 EPS 增长分歧腿（`j2eoKKEj`）

波 102 SUB 修复批（multisim `4swHZ7yC4yO9Gk3hPe6813`，8 臂全终态、0 error）中，
EPS 增长腿在 `market + signed_power` 壳下由 SUB 1.11/limit 1.20（0.493 比值）提升到 **1.38/limit 1.36**（0.535 比值），
是全批唯一 RA 全闸通过臂。

| 项 | 值 |
|---|---|
| alpha | **`j2eoKKEj`** |
| 数据集 / 塔 | `ai_equity_alpha` / `USA/D1/MODEL`（×1.3） |
| 核心字段 | `earnings_per_share_growth_metric_2` − `earnings_per_share_growth_metric_3`（两代 EPS 增长模型分歧） |
| 算子逻辑 | `signed_power(ts_decay_linear(group_rank(ts_zscore(ts_backfill(subtract(vec_avg(A), vec_avg(B)), 252), 252), market), 5), 0.8)` |
| 设置 | USA / TOP2000 / D1 / STATISTICAL / platform decay 0 / trunc 0.08 / VERIFY / **nanHandling ON** / 2014-01-01→2023-12-31 |
| 指标 | S **2.58** / F **1.63** / 2Y **2.17** / SUB **1.38**（limit 1.36）/ TO 17.57% / RET 6.99% / DD 3.16% / margin **7.96 bp** / long 1113 · short 966 |
| RA 闸 | `failed_ra_count = 0`；warning 仅 CLUSTER_TEST 1.34（limit 1.58）、MATCHES_THEMES、OSMOSIS_ALLOCATION |
| 相关性 | prod **0.6434**（<0.7，余量 **0.0566** —— 全部候选中最大）/ self **0.2751**（对 `O08EjLVp`） |
| 稳健性 | **PASS**（recent-3yr S 2.093；CV 0.275；衰减比 0.570；max/min 1.95；0 平年；年度 PnL 10/10 为正；maxDD 1.58%） |
| 稳健性报告 | [`reports/robustness_20261023.md`](../../reports/robustness_20261023.md)（`robustness_j2eoKKEj`） |
| 状态 | `submit_ready` 已入队；**未提交**，提交需用户明确确认（不可逆） |

**SUB 修复的可复用结论（本批 8 臂对照）**：同一字段对，仅换分组轴——
`subindustry` 0.90 → `market` 1.27 → `exchange` 1.25（asset_liquidity，S 同步 2.03→2.45）；
`subindustry` 1.11 → `market` 1.38 → `exchange` 1.36（EPS 增长，S 2.53→2.58）。
**`market` 轴同时抬 S 与 SUB 比值**，是 SUB 墙的第一杠杆；`signed_power(…,0.8)` 相对平铺再抬一档
（EPS 腿 1.38 vs 1.31）。但注意 SUB 是**比值闸**（limit ≈ 0.527 × S），S 抬升会同步抬线，
所以 `exchange` 臂虽然绝对 SUB 1.36 仍差 0.01 落榜。

**同批其余臂（留档避免重复）**：
- `LL5EYYj2`（EPS，market 平铺）S2.40/F1.43/2Y2.03/SUB1.31 **RA 全过** —— 与 `j2eoKKEj` 同核近亲，只作备用，不双提（SELF 自锁）。
- `omoR005m`（EPS，exchange+signed_power）SUB 1.36 vs limit 1.37，**差 0.01 落榜**。
- `RRA9wwQn`（EPS，subindustry decay10）SUB 1.11 vs 1.34，subindustry 轴确认不适合本族。
- `78o3RRWL` / `1YjOAAeM` / `gJWXVVAO`（asset_liquidity 三壳）SUB 分别 1.27/1.17/1.25 vs limit 1.30/1.21/1.29，全部差 0.03–0.04；
  该字段对的 edge 更偏小盘，换轴后仍不够，暂不继续投入。
- `N1eLllwg`（asset_liquidity，subindustry decay10）SUB 0.90 vs 1.13，判死。

### 6.7 第 10 颗：波 103 信用风险分歧腿（`N1eLE1de`）

波 103（multisim `2deMBcfPr54hcnrb3pnevvc`，9 臂 / 6 COMPLETE / 3 单位错误）用同一 `subindustry` 壳扫 9 个未测 ai_equity 字段对，
其中 2 臂 RA 全闸、4 臂多闸失败、1 臂单位不兼容、1 臂平台未落 alpha。两臂全闸里 `3qj1mqK6`（fund_flow_prediction_metric 分歧）
prod **0.7168** 破 0.70 判不可提交；`N1eLE1de` 双相关性过闸，成为第 10 颗。

| 项 | 值 |
|---|---|
| alpha | **`N1eLE1de`** |
| 数据集 / 塔 | `ai_equity_alpha` / `USA/D1/MODEL`（×1.3） |
| 核心字段 | `credit_risk_model_score_5` − `credit_risk_model_score_7`（两代信用风险模型评分分歧 = 信用重估速率） |
| 算子逻辑 | `ts_decay_linear(group_rank(ts_zscore(ts_backfill(subtract(vec_avg(A), vec_avg(B)), 252), 252), subindustry), 5)` |
| 设置 | USA / TOP2000 / D1 / STATISTICAL / platform decay 0 / trunc 0.08 / VERIFY / **nanHandling ON** / 2014-01-01→2023-12-31 |
| 指标 | S **2.63** / F **1.54** / 2Y **2.07** / SUB **1.66**（limit 1.24）/ TO 14.09% / RET 4.86% / DD 2.41% / margin **6.89 bp** / long 1032 · short 1048 |
| RA 闸 | `failed_ra_count = 0`；warning 仅 CLUSTER_TEST 1.07（limit 1.58）、MATCHES_THEMES、OSMOSIS_ALLOCATION |
| 相关性 | prod **0.6916**（<0.7，余量 **0.0084** —— 全部候选最薄）/ self **0.2753**（对 `O08EjLVp`） |
| 稳健性 | **CONDITIONAL**（recent-3yr S 2.133；CV 0.358；**衰减比 0.407** 落 0.30–0.50 带；max/min 2.65；0 平年；年度 PnL 10/10 为正；maxDD 1.20%） |
| 稳健性报告 | [`reports/robustness_20261023.md`](../../reports/robustness_20261023.md)（`robustness_N1eLE1de`） |
| 状态 | `submit_ready` 已入队；**未提交**，提交需用户明确确认（不可逆） |

**2023 弱年是数据集级而非字段对级（可复用）**：本数据集已验的三条分歧腿 2023 年 S 全部显著低于前两年
——`YPx89bQJ` **0.91**、`j2eoKKEj` **1.47**、`N1eLE1de` **1.07**（各自 2021/2022 为 1.79/2.86、1.95/2.86、2.50/2.83）。
⇒ 判为 MODEL 数据集自身的**模型版本更新节奏放缓**导致分歧信号衰减，不是某个字段对失效；
后续同数据集候选在近窗稳健性上要**预期 2023 是低点**，不要把它当作字段对判死依据。

**同波其余臂（留档避免重复劳动）**：

| 臂 | 字段对 | S | F | 2Y | SUB | 裁决 |
|---|---|---:|---:|---:|---:|---|
| `3qj1mqK6` | fund_flow_prediction_metric − _81 | 2.36 | 1.42 | 1.92 | 1.46 | RA 全过，**prod 0.7168 → 不可提交**（0.70–0.75 段） |
| `bl8J0lmK` | creditworthiness_assessment_factor − _7 | 1.70 | 0.85 | 1.37 | 0.84 | 3 闸（F/SUB/2Y）→ 族无增量 |
| `A1QeX1AR` | forecast_value_accuracy_metric − _7 | 1.20 | 0.50 | 0.12 | 0.50 | 4 闸 → 族死 |
| `1Yj3YM6` | income_statement_trend_metric − _7 | — | — | — | — | 平台 404（仿真未落 alpha） |
| `0mjxZmJp` | credit_risk_model_score_7 − _5（反向） | 0.93 | 0.33 | 0.15 | −0.01 | 4 闸 → **正向确认正确** |
| `xA1V7ALg` / `58jrK8mk` / `88vVW8wa` | cashflow_trend − _121 / forecast_yield − _91 / 反向 | — | — | — | — | 单位不兼容（`subtract` index 1 期望 `Unit[]` 实得 `Unit[CSPrice:1]`），**该字段对双向都不可用** |

**方向对照再次成立**：`credit_risk_model_score` 正向 2.63 vs 反向 0.93，方向不可推断必须双向测（画像 §2.2）。
**prod 双峰再次成立**：同壳同设置下 `fund_flow` 对 0.7168 / `credit_risk` 对 0.6916，仍是字段对持仓决定 prod，与 IS 强弱无关
（S 2.63 的对反而 prod 更低）。

---

## 7. 严格口径清单（**5 / 10**，2026-10-23 更正）

口径：**平台 RA `failed_ra_count = 0` + `check_correlation(refresh=True)` 的 prod **与** self 均 < 0.7**；
**且主数据集所在的平台类别塔未点亮**（用户规则 2026-09-19：已点亮塔只作组腿辅助）。
前 5 颗已在 2026-10-20/21 提交并 ACTIVE/OS（开采时 analyst 未点亮）；#6–#10 因落在**已点亮 MODEL 塔**
作废，仅保留为组腿辅助池，**不计入**。

| # | alpha | 数据集 | 核心字段 | S | F | 2Y | SUB | prod | self | 稳健性 | 状态 |
|---:|---|---|---|---:|---:|---:|---:|---:|---:|---|---|
| 1 | `omoK1A5m` | analyst_factor_signals | eps_q1_estimate_qoq_growth | 2.05 | 1.24 | 1.79 | 0.93 | 0.6489 | 0.4864 | — | **ACTIVE** |
| 2 | `akVnvzX5` | analyst_factor_signals | eps_y1_estimate_skewness | 1.83 | 1.06 | 1.87 | 0.95 | 0.6594 | 0.5692 | — | **ACTIVE** |
| 3 | `gJWoaJqv` | analyst44 | eps/sales 背离加速度（4 字段） | 1.74 | 1.27 | 2.21 | 0.86 | 0.6978 | 0.5803 | — | **ACTIVE** |
| 4 | `kqJLawqP` | analyst44 | 同上（秩变换 + 756 日） | 1.61 | 1.11 | 1.62 | 0.84 | 0.6757 | 0.6445 | — | **ACTIVE** |
| 5 | `e76xgXkM` | analyst_consensus | mean_forecast_actual_combined_fxadj_eps_annual12 | 1.89 | 1.12 | 1.76 | 1.05 | 0.5532 | 0.4553 | — | **ACTIVE** |
| 6 | `YPx89bQJ` | ai_equity_alpha | predicted_earnings_surprise_2 − _3 | 2.19 | 1.16 | 1.91 | 1.24 | 0.6803 | 0.2812 | CONDITIONAL | **不计入（MODEL 已点亮）**
| 7 | `58jr102k` | ai_equity_alpha | financing_structure_analysis_3 − _4 | 2.26 | 1.33 | 2.06 | 1.41 | 0.6818 | 0.2329 | **PASS** | **不计入（MODEL 已点亮）**
| 8 | `zqrgna91` | ai_equity_alpha | buzz_intensity_score_2 − _11 | **2.67** | **1.66** | 1.68 | 1.47 | 0.6877 | 0.2866 | **PASS** | **不计入（MODEL 已点亮）**
| 9 | `j2eoKKEj` | ai_equity_alpha | earnings_per_share_growth_metric_2 − _3 | 2.58 | 1.63 | **2.17** | 1.38 | **0.6434** | 0.2751 | **PASS** | **不计入（MODEL 已点亮）**
| 10 | `N1eLE1de` | ai_equity_alpha | credit_risk_model_score_5 − _7 | 2.63 | 1.54 | 2.07 | **1.66** | 0.6916 | 0.2753 | CONDITIONAL | **不计入（MODEL 已点亮）**

**#6–#10 作废，不构成提交顺序**：原按 prod 余量的排序（`j2eoKKEj` 0.0566 → `YPx89bQJ` 0.0197 → `58jr102k` 0.0182 → `zqrgna91` 0.0123 → `N1eLE1de` 0.0084）仅留档，供未来作组腿时参考。
⚠ 后 5 颗同属 `ai_equity_alpha` 分歧机制，组内互相关 0.07–0.67（画像 §11）；
`zqrgna91` 与 `j2eoJRMO` 同属 buzz 机制，后者已退役不再提交（避免 SELF 自锁）。
**前 5 颗已由用户确认提交；后 5 颗按用户规则作废，agent 不会为其申请提交。**

**ATOM 口径**：计入的 5 颗非豁免字段均来自**单一数据集**（豁免仅限 country / exchange / market / sector /
industry / subindustry 六个分组字段）；#6–#10 同样落在 `ai_equity_alpha` 单数据集内，但因塔已点亮不计入。

**画像存档索引**（均在 `Claude/skills/wq-brain-ra-usa/references/`）：
- `_usa-analyst-factor-signals-field-profile-20261019.md`（#1 #2）
- `_usa-analyst-consensus-field-profile-20261020.md`（#5）
- `_analyst-campaign-20261017.md`（#3 #4，analyst44）
- `_usa-ai_equity-alpha-field-profile-20261023.md`（#6–#10；§2 字段画像总表、§10–§13 波次实测与可复用结论）
- 稳健性报告：`reports/robustness_20261023.md`（与台账 `robustness_<alpha_id>` 同源）

---

## 8. 2026-10-23 更正：已点亮塔不作为主数据集（用户规则）

### 8.1 平台事实（`get_pyramid_alphas` / `campaign_intel.py pyramid --region USA --delay 1`）

USA/D1 当季共 16 个平台类别，**2 个已点亮**：

| 类别 | 我方 ACTIVE | 塔位 | 乘数 |
|---|---:|---|---:|
| analyst | 6 | **LIT** | 1.2 |
| model | 4 | **LIT** | 1.3 |
| earnings | 1 | 未点亮（差 2） | 1.2 |
| fundamental | 0 | 未点亮（差 3） | 1.1 |
| other | 0 | 未点亮（差 3） | 1.4 |
| sentiment | 0 | 未点亮（差 3） | 1.4 |
| option | 0 | 未点亮（差 3） | 1.3 |
| news | 0 | 未点亮（差 3） | 1.2 |
| 其余 7 类 | 0 | 未点亮 | 1.0–1.1 |

规则源：`src/wqb/profiles/locked.py::lit_tower_platform_category`（用户 2026-09-19 定案，
「点塔 / 剔已亮塔一律按平台类别；已亮塔只作组腿辅助」）；工具侧 `campaign_intel.py s0-select`
默认剔除 `category_lit` 数据集（`--include-lit` 才保留）。

### 8.2 影响范围与归因

- 作废 5 颗：`YPx89bQJ` / `58jr102k` / `zqrgna91` / `j2eoKKEj` / `N1eLE1de`，全部来自
  `ai_equity_alpha`（`datasets.category = MODEL`），即**已点亮塔**。
- 前 5 颗 analyst 系列（`omoK1A5m` / `akVnvzX5` / `gJWoaJqv` / `kqJLawqP` / `e76xgXkM`）
  **保留计入**：开采与提交时 analyst 仅 1 颗 ACTIVE（未点亮），这 5 颗提交后才达 6 颗。
  `analyst` 现在已点亮，**后续不再从 analyst 主数据集开采**。
- 根因：扩挖 `ai_equity_alpha` 时按「字段数 1108 / 机制可组合性」直接选了数据集，
  **没有走 S0 的 `campaign_intel s0-select`（自带已亮塔剔除）**；已亮塔检查只在提交前想到，
  没有前移到选集。机制类别（divergence）与平台类别（model）不同不构成豁免——锁定表原文即此意。

### 8.3 处置与替换路线

1. 5 颗作废件保留在 `submit_ready` / 台账中作**组腿辅助池**，不申请提交。
2. 严格口径回退 **5 / 10**。补足路线固定 USA、不换区：
   - **首选 `fundamental` 塔**（未点亮、乘数 1.1，符合原始任务「全部 Fundamental 数据集逐一扫描」）；
   - 次选 `other`（1.4）/ `institutions`（1.0）/ `pv`（1.1）等未点亮塔；
   - **禁选**：`analyst`、`model` 两个已点亮塔。
3. 每波开波前必须记录 `campaign_intel.py pyramid --region USA --delay 1` 快照，
   确认目标数据集 `category` 不在 LIT 列表；此检查写进 S0 产物，不再只靠提交前人工回忆。

---

## 9. 补挖执行记录（2026-10-23，严格口径 5 → 目标 10）

### 9.1 已判死的替换路线（按时间顺序，全部 0 交付）

| # | 路线 | 塔 | 最好成绩 | 判死依据 | 存档 |
|---:|---|---|---|---|---|
| 1 | `fundamental` 全线（fnd1/21/22/25/35/69/72/91/93/110、other416/452 等 20+ 个） | fundamental 1.1 | 最高的 fnd1 S 1.17 | 逐数据集全灭：或字段退化（映射表 / 元数据表 / 覆盖 0.429）、或 S 上限 1.1–1.2 够不到 1.58、或已饱和停投 | `_usa-risk60-field-profile-20261023.md` §1 |
| 2 | `risk60`（借券费率 `lending_fee_bid_rate`/`rsk60_offer`） | risk 1.1 | **S 2.39 / F 5.24 / 2Y 3.88 / SUB 1.12 / RA 全过**（`A1Qr9Y8W`） | **prod 0.9917**，`[0.9,1]` 桶 n=116 ⇒ 结构性墙 | 同上 §7.2 |
| 3 | `pv106`（交易成本估计） | pv 1.1 | 十臂最好 S −0.30（全负） | 水平臂稳定为负（中位 −0.38）+ `transaction_cost_estimate` 是**空列**（5 臂零持仓） | `_usa-pv106-field-profile-20261023.md` |
| 4 | `other143` 冠军 `RRA97Wo0`（波 82 曾破 F 墙） | other 1.4 | F 墙已破 | **prod 0.8658** ⇒ 同机制判死 | risk60 画像 §7.2 |

**共同教训（写进选集纪律）**：数据集的 `alphaCount` / `userCount` 低，**不代表 prod 低**。
`lending_fee_bid_rate` 平台 aC 仅 168（同数据集另一字段 2395，差 14 倍）、此前零条 USA 表达式，
prod 仍是 0.9917。决定 prod 的是**机制在生产池里的拥挤度**；空头约束 / 借券费率 / 流动性溢价 /
交易成本这些**经典异象**已被挖尽，「冷门数据集 + 经典异象」不提供任何相关性优势。

### 9.2 `other635`（OTHER ×1.4，0 颗 ACTIVE）—— 已判死

选集四条判据同时成立：塔位 OTHER 未点亮、数据集 aC **18**（三个情绪字段 aC 分别 1 / 0 / 0）、
**9 字段 = 三套平行供应商管线 × 三指标**（可造跨供应商分歧）、覆盖 0.9929。
此前 12 条表达式全部 `dropped`、**无一条进过回测**。

波 1 十臂（`tracking/USA/runs/usa_oth635_w1.txt`，MARKET/TOP3000/decay 8/trunc 0.08/nanHandling ON/
2014-01-01..2023-12-31，multisim `28H7VC1qb4G49m3loRegYq`）覆盖三机制 + 一条控制臂：

| 机制 | 最好臂 | S | 判读 |
|---|---|---:|---|
| H-disp 跨供应商分歧 | A10 两词典间分歧 | **−0.86**（取反 +0.86） | 最强臂，但 RN −0.71 ⇒ **风格暴露**，距 1.58 差 1.8 倍 |
| H-sign 有符号分歧 | A4/A5 | ±0.10 | 差分的**符号无信息**，只有绝对值有信息 |
| H-level 情绪水平 | A7 | 0.24（TO 27%） | 66 日平滑把新闻情绪洗掉 |

**方向是统一反的**：5 个分歧臂全为负 ⇒ `+分歧` 全为正 ⇒ 美国新闻场景里「供应商分歧大」预示**更高**收益
（分歧 ≈ 事件强度/关注度，带动量性质），教科书的不确定性溢价先验不成立。

**本波最重要的跨数据集结论**：ai_equity 的分歧能到 S 2.19–2.67 / prod 0.64–0.69，因为两条腿都是
**对同一目标的高信息量预测**；把同一构造用在新闻情绪分类器上，差分提取的是**分词器/词典的标注差异**，
经济含义退化为新闻强度 ⇒ 方向反、RN 塌成风格、上限 0.86。
**可复用判据：分歧构造要求两条腿都是「对收益的预测」，不是「对文本的打分」。**

裁决：`other635` **停投**（情绪三字段三机制全测；长度四字段因 attention 代理最拥挤且同属文本差分而不投入）。
OTHER 塔仍 0 颗 ACTIVE，未被消耗。
画像：`_usa-other635-field-profile-20261023.md` §5.3–§5.4。

### 9.3 `chart_return_model`（PV ×1.1，0 颗 ACTIVE）—— 已判死

选集依据：248 字段、覆盖 1.0、**20 个 `predicted_*forward_return` 字段**——
① 期限族 6 个（1/3/5/10/20 日 + 基字段）；② 配置族 14 个（`_bidaskr10` 含成本 / `_g2`·`_g6r1` 分组 /
`_r10`·`_r20` 秩 / `_w2r1` 窗口 / `_t100` 宇宙）；绝大多数 `aC = 0`。
**这是 ai_equity 那套「平行模型对同一目标预测」结构的正版宿主**，且落在未点亮 PV 塔。

波 1 十臂（`tracking/USA/runs/usa_crm_w1.txt`，同设置，multisim `4alaRUbNk54auOyUZ12q7v`）：
4 条水平臂（基字段 / _t100 / 20 日 / 反向对照）+ 6 条分歧臂（gross−含成本 双向、g2−g6r1、r10−r20、
基−w2r1、5日−1日期限）。**预登记判据无一臂满足**：

| 臂 | S | F | TO | 2Y | SUB/S | 判读 |
|---|---:|---:|---:|---:|---:|---|
| `_t100`（`QPYNJJxW`，本波最高 S） | 1.22 | 0.37 | 57.1% | **−0.01** | 0.238 | 高换手 + 逐年崩塌；1-bar 预测在 D1 不可执行 |
| 20 日水平（`58jAbbmX`，本波最好 2Y/SUB） | 0.90 | 0.40 | 36.2% | 1.27 | **0.656** | 唯一方向与衰减都健康，但强度差 1.75 倍 |
| 5d−1d 期限分歧（`2rjX003Z`） | 0.71 | **0.52** | **9.8%** | 1.13 | 0.380 | 换手最低、F 最高，横截面区分度不足 |
| 配置分歧四组（双向） | \|0.20–0.49\| | — | — | — | — | 正负无序 ⇒ 无方向信息 |

**归因（主因 = 期限错配）**：14 个配置变体与基字段预测的是 **next interval（1-bar）**，D1 最早次日成交，
信号在可交易时点前已衰减 ⇒ 只剩高换手与近零 2Y。可执行的日尺度（5/10/20 日）只有 20 日臂接近可用形态，
但 S 0.90 远不够。

**第二条跨数据集结论**：`gross−bidask`、`g2−g6r1`、`r10−r20`、`base−w2r1` 四组配置分歧 |S| ≤ 0.49 且正负无序，
与 other635 同构 ⇒ **分歧腿必须来自「信息源不同」的模型**；同模型、同训练数据、只改正则/分组/窗口的
多配置差异主要是抽样噪声，差分会把公共信号减掉只剩噪声。**同模型多配置字段 aC 低 ≠ 未被挖掘，而是不含新信息。**

裁决：**停投**。PV 塔仍 0 颗 ACTIVE。画像：`_usa-chart-return-model-field-profile-20261023.md` §5–§6。

## 10. 补挖执行记录（2026-10-24）

### 10.1 当前口径：5 在册 + 4 臂 basket 待确认 = 潜在 9，第 10 颗必须来自新机制

| 块 | 数量 | 状态 |
|---|---:|---|
| 已提交 ACTIVE（analyst 三集） | **5** | 严格口径在册（prod 0.5532 / 0.6489 / 0.6594 / 0.6757 / 0.6978） |
| 全过未提交 basket（ds382×3 + ds381×1） | **4** | `O0Jgd7Y7` / `88vXxaqv` / `LL53QVvn` / `d5KzLo7v`，prod 0.5516–0.6964，**待用户确认提交** |
| 第 10 颗 | **0** | `compute_mutual_correlation` 在 0.7 阈值的最大互不相关子集 = **4 臂且 `max_subset_exact=true`** ⇒ 必须来自新机制 |

⇒ 补挖目标从"补 5 颗"改为**"补 1 颗新机制"**。前 4 颗已由 basket 承接（同族 DS 内多臂，彼此 self/prod 均已实测）。

### 10.2 2026-10-24 判死与结案（零新增交付）

| 对象 | 结论 | 依据 |
|---|---|---|
| `macro27`（MACRO 未点亮塔） | **结案，不开 w2** | 最强臂 `WjLxAWoN` prod **0.8771**；可提交方向 prod 0.7933；6 臂 max S 仅 1.39；共同失效年 2023 |
| `risk60` | **判死** | 四条 SUB 臂 prod **0.9631 / 0.9861 / 0.9917**（借券费率即卖方拥挤度的另一种写法） |
| `earnings4` | 不投 | 数据集级 aC **13771**，Tier B 饱和 |
| `imbalance5` | 不投 | 实为**油冲击韧性分** `imb5_score`（非订单不平衡），仅 2 字段、aC 4690 |
| `institutions18` | 判死 | `88PmKRzv` prod **0.9493** / `RR6JkEpd` 0.9377（2026-10-24 现测） |
| `fundamental110` | 不投 | 26 字段全是**长表 VECTOR 元数据**（metric/value/period/filing_type），不可直接做横截面信号 |
| `fundamental14` / `91` / `2` / `6` / `17` / `23` / `28` / `3` / `7` / `13` | 不投 | 元数据为主（248/407 字段绝大多数 VECTOR）或 aC 14188–860417 饱和 |

### 10.3 `fundamental93`（波 `fnd93_w1`）—— 六臂全灭，判弱结案

6 臂（应计水平 / 应计同比 / 应计 z 突刺 / 资产增长 / 税应计 / 递延税费用 z），统一壳
`-group_rank(ts_zscore(ts_backfill(<field>,252),504), subindustry)`，USA/TOP3000/D1/SUBINDUSTRY/decay 4/trunc 0.08。

| 指标 | 实测区间 | 判读 |
|---|---|---|
| Sharpe | **−0.54 … −0.78**（六臂全负） | 反号 |S| 上限 0.78 < 预注册判弱线 **0.9** ⇒ 概念不承载横截面信号 |
| Turnover | 1.50% – 2.68% | 低于平台 12.5% 换手地板 ⇒ F 按 `S·√(ret/0.125)` 计 |
| returns | −1.47% … −3.42% | F≥1.0 需 `S·√ret ≥ 0.354`；S 取 1.58 时需 ret ≥ **5.0%** ⇒ 调壳无解 |
| 2Y | −0.85 … **−1.70**（资产增长臂最差） | 应计 / 资产增长异象在 2022–2023 高利率周期被反向定价 |
| risk-neut S | 三臂转正（+0.17 / +0.41 / +0.28） | 负 alpha 中相当部分是行业/风险暴露，剥离后残差更弱 |

**结论**：按预注册判据**不开第二批**、不调壳。46 字段同属一个概念面（税务应计/应计/递延税费用/资产增长），
无第二机制可切 ⇒ 换数据集是执行预注册判据，不是"频繁切换"。
明细：`reports/usa_near_gate_candidates_20261024.md` §8.1（wave_results id 1388）。

### 10.4 第 10 颗的新方向：`order_flow_imb`（OPTION 未点亮塔，波 `ofi_w1`）

**选集依据（2026-10-24 live）**：120 个 MATRIX 字段、base 覆盖 **0.9058**（`_ise` 0.788 / `_noto` 0.773 / `_otm` 0.770）、
数据集 aC **478** / userCount 197（最挤字段 `customer_trade_imbalance` aC 108）、金字塔 USA/D1/OPTION **1.3×**、塔位未点亮。
机制面 = 6 类参与者（broker_dealer / customer / firm / market_maker / pro_customer / proprietary）×
bullish/bearish × contracts/trade_count/vol × imbalance × 4 变体，与已跑 11 族正交。

**模板来源（不是自创）**：论坛帖 42078917602455（93 票）冠军 `qM6ZNpaE` ——
S 1.17 / 2Y 1.76 / TO 26.18% / **7 算子 / 2 字段 / ATOM**，PPA self-corr 0.168。
经济机制 = 专业客户（知情）看涨成交量相对公司/做市商（流动性提供者）急剧上升 → 过度反应 → 反转，
用 `ts_ir` 衡量分歧持续性后取负号。算子数反推证实原帖形态为
`-ts_ir(ts_backfill(A,5) - ts_backfill(B,5), 22)`（2 字段 + 2 backfill + 减法 + ts_ir + 负号 = 7）。
学术旁证：Chordia-Roll-Subrahmanyam（订单不平衡预测收益）、知情交易者在做空成本高时转向期权。

**6 臂（两个 multisim，把中性化当设置层对照）**

| # | multisim | 中性化 | 表达式 | 机制 |
|---:|---|---|---|---|
| 1 | `1HsjND9fR50E9XmYI9KvOkC` | INDUSTRY | `-ts_ir(ts_backfill(pro_customer_bullish_vol,5) - ts_backfill(firm_bullish_vol,5), 22)` | 论坛主配方（公司作对手方） |
| 2 | 同上 | INDUSTRY | 同 #1 **去负号** | **符号对照**（动量假设） |
| 3 | `3YYYHFbGU4tP9F39fvV0010` | SUBINDUSTRY | `-ts_ir(ts_backfill(pro_customer_bullish_trade_count,5) - ts_backfill(market_maker_bullish_trade_count,5), 22)` | 换载体（笔数）+ 做市商对手方 |
| 4 | 同上 | SUBINDUSTRY | `-group_rank(ts_delta(ts_backfill(pro_customer_trade_imbalance,5) - ts_backfill(market_maker_trade_imbalance,5), 5), subindustry)` | 分歧加速度 |
| 5 | 同上 | SUBINDUSTRY | `-group_rank(ts_zscore(ts_backfill(pro_customer_vol_imbalance_otm,5), 66), subindustry)` | OTM 知情投机单类 |
| 6 | 同上 | SUBINDUSTRY | `-group_rank(ts_zscore(ts_backfill(customer_trade_imbalance,5), 66), subindustry)` | 散户逆向（dumb money 对手） |

- 设置：USA / TOP3000 / D1 / decay 4 / truncation 0.08 / nanHandling ON / unitHandling VERIFY /
  pasteurization ON / maxTrade OFF；全部字段单数据集（ATOM 口径）。
- **形状 3 族**（ts_ir ×3 / ts_delta ×1 / ts_zscore ×2）、`trade_when` 0%、载体 4 种 ⇒ 满足闸 6。
- **#1/#2 符号对照是对 fnd93 教训的直接修正**：六臂同号时无法区分"概念死"与"符号反"，
  本波用一对正负版本保证至少一臂落在正确方向。
- 预注册判据：max S < 0.9 ⇒ 不扩批；S ≥ 1.2 且 F ≥ 0.6 ⇒ 只动回填/窗口/中性化；S ≥ 1.58 / F ≥ 1.0 / 2Y ≥ 1.58 ⇒ 立刻 prod-first。

**收批结果（2026-10-24，`wave_results` `ofi_w1`）—— 判死，0 交付**

| # | alpha | S | F | TO | ret | 2Y | SUB |
|---:|---|---:|---:|---:|---:|---:|---:|
| 1 | `leMNKea8` | −0.33 | −0.09 | 13.45% | −1.09% | +0.07 | −0.08 |
| 2 | `78o268Y2` | +0.33 | +0.09 | 13.45% | +1.09% | −0.07 | +0.08 |
| 3 | `rKdnevdJ` | +0.02 | 0.00 | 14.49% | +0.11% | −0.25 | +0.01 |
| 4 | `npAXPMAl` | −0.53 | −0.10 | 44.37% | −1.61% | −0.28 | −0.37 |
| 5 | `O0J28EAq` | −0.32 | −0.09 | 15.98% | −1.22% | −0.63 | −0.40 |
| 6 | `j2eM8bYk` | **−1.11** | −0.31 | 42.37% | −3.28% | −0.75 | −1.08 |

- **论坛配方不可平移**：臂 1/2 符号对照**逐位镜像**（S ±0.33 / ret ±1.09%）⇒ 该分歧量在 TOP3000/D1/REGULAR 下不带方向信息；
  论坛的 S 1.17 属 TOP1000 + PPA 设置。臂 3 换载体（笔数 + market_maker 对手方）S 0.02，精确为零。
- **唯一活的方向**：臂 6 **反号** = 客户订单不平衡**动量**，逐年 8/10 年为正（2022 +0.29 / 2023 +1.31），
  稳健但 S 仅 1.11；**F 算术封死**（`F = 1.11·√(3.28%/42.37%) = 0.31`，F ≥ 1.0 需同时 S +42% 且 TO −70%）⇒ 不扩批。
- **战略发现**：平台对本波六臂的 `ppa_failed_checks` 只有 `LOW_SHARPE` / `LOW_SUB_UNIVERSE_SHARPE`，**PPA 轨无 fitness 闸**；
  且论坛冠军本身就是 PPA 投稿。两条独立证据同向 ⇒ **期权订单流是 PPA-profile 信号类**，其正确归宿是 PPA，
  臂 6 反号后 S +1.11 / SUB +1.08 即为现成首颗 PPA 候选。REGULAR 口径判死。
- 明细：`reports/usa_near_gate_candidates_20261024.md` §P3「收批结果」。

### 10.5 `fundamental` 全塔已穷尽 ⇒ 第 10 颗改由其它未点亮塔承接

原任务范围为 Fundamental 数据集；2026-10-24 复扫后 `fundamental` 塔已无可用集
（§10.2：14/91/2/6/17/23/28/3/7/13 元数据或饱和、110 长表 VECTOR、93 六臂全灭、69/91 已判死）。
`campaign_intel s0-select --region USA` 当前排序里 fundamental 只剩 `fundamental13`（aC 15361）/`fundamental17`
（aC 34886，跨区弱 GBR 0.80）两个高拥挤项 ⇒ 按「缺强度证据不开波」原则不再投 fundamental。
第 10 颗改由未点亮塔承接，优先**机制正交且低换手**（低换手是 F 闸的必要条件）的方向。

### 10.6 `earningscall_sentiment`（波 `ecs_w1`）—— 六臂全灭，判弱结案

财报电话会语调数据集（`earnings` 未点亮塔，波内口径计入 OTHER 1.4×；平台 `earnings` 塔当前 1 ACTIVE、差 2）。
字段为按 section × role 切分的 `mean_polarity_*` 语调标量，覆盖 0.843–0.858，值域 [0,1]。

6 臂统一壳（除 #6）：`±group_rank(ts_backfill(<tone diff>, 5), subindustry)`，USA/TOP3000/D1/SUBINDUSTRY/decay 4/trunc 0.08。

| # | alpha | 机制 | S | F | TO | ret | 2Y | SUB | CW |
|---:|---|---|---:|---:|---:|---:|---:|---:|---:|
| 1 | `VkdRxk5G` | −(盈利 − 现金流 回答语调) | −0.15 | −0.02 | 36.83% | −0.78% | −0.14 | −0.35 | 0.169738 |
| 2 | `78o2L8lb` | 同 #1 **去负号** | +0.15 | +0.02 | 36.83% | +0.78% | +0.14 | +0.35 | 0.169738 |
| 3 | `rKdnRK8o` | −(杠杆 陈述 − 回答 语调) | −0.33 | −0.07 | 36.82% | −1.69% | −0.64 | −0.35 | 0.169738 |
| 4 | `leMNAe1N` | 现金流 section 语调水平 | **+0.51** | 0.13 | 36.83% | 2.50% | 0.33 | 0.35 | 0.169738 |
| 5 | `omokEmk2` | 盈利 section 提问语调 | +0.33 | 0.07 | 36.77% | 1.62% | 0.56 | 0.23 | 0.169738 |
| 6 | `d5KPW5Pj` | 估值语调 `ts_delta 66` | +0.04 | 0.00 | 50.31% | 0.33% | 0.43 | 0.28 | 0.50（2017-01-09） |

- **符号对照给出零信息**：#1/#2 逐位镜像（S ±0.15 / ret ±0.78%）⇒ 「盈利 vs 现金流语调分歧」这一概念在
  TOP3000/D1 下**不带方向信息**，问题不在符号。
- **最佳臂不可用**：#4 逐年 2014 +1.39 / 2015 +2.24 / 2016 +2.54 / 2017 −1.62 / 2018 −0.41 / 2019 +0.12 /
  **2020 −3.64** / 2021 +2.07 / 2022 +0.54 / 2023 +0.01 ⇒ 顺周期语调动量，2020 单年吃掉全部累计收益。
- **一阶差分无效**：#6 `ts_delta 66` S 0.04 且换手翻倍（50.31%）⇒ 语调变化率不是可交易信号。
- **覆盖爬坡伪影**：6 臂 CW 全部落在**同一天 2014-01-02 的 0.169738**（#6 落在 2017-01-09 的 0.50）
  ⇒ 数据集早期只有个位数股票有覆盖；任何后续臂都必须加**宽度门**（如 `group_count` 过滤）才可能过 CW。
- **F 算术封死**：最佳臂 F 0.13，F ≥ 1.0 需 `S·√ret` 增长 **7.7×** ⇒ 调壳/换窗口在算术上不可能。
- **判定**：max |S| 0.51 < 预注册弱线 0.9 ⇒ 按预注册**不开第二批**、不调壳、不再投该数据集。
- **未测但已低先验判定**：5 个 `*_chunk_count` 字段（question aC 0 / presentation 6 / summary 1 / answer 13 /
  summary_fast_d1 0；覆盖 0.845–0.850）= 关注度/冗长度/回避度代理。记录为**条件腿 / PPA 素材**可回取，
  不作 REGULAR 独立信号继续投。
- 明细：`wave_results` USA/`ecs_w1`（verdict FAIL / status closed），`reports/usa_near_gate_candidates_20261024.md` §P3。

