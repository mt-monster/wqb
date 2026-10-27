# pv20 字段画像（USA / TOP3000 / D1）

> as_of 2026-10-22。数据来源：`get_datafields(region=USA, delay=1, universe=TOP3000, dataset_id=pv20)`
> 全量 32 页（`complete=true`，1552 字段）。全字段清单见
> [`_usa-pv20-field-inventory-20261022.md`](_usa-pv20-field-inventory-20261022.md)。
> 选集理由与批次记录见交付日志附录 AG。

## 1. 结论速览

| 项 | 值 | 判读 |
|---|---|---|
| 平台 category | **pv** | 本季 USA/pv 提交 **0** ⇒ **未点亮**，可回测 |
| 字段数 | **1552** | 单一数据集里少见的「多源拼装集」 |
| 数据集 coverage | 0.779 | 过 S0 覆盖线 |
| alphaCount / userCount | 2117 / 768 | **≈1.4 α/字段 ⇒ 绝大多数字段 aC=0**，是全库少见的低拥挤区 |
| valueScore / pyramidMultiplier | 2 / 2 | 平台估值中档 |
| 结构 | 一致预期快照 + 厂商算法估计 + IBES 组预测信号 + 季度 as-reported + 风险模型特异收益 + 价量微结构 | 前四族是**基本面预期信号**，后两族是风险/价量 |

**一句话**：这是「披着 pv 外衣的 IBES 预期/预测集」——美国已证有效的修正式机制
（`e76xgXkM`，S 1.89 / prod 0.5532）可以在这里找到**同机制不同数据源**的字段，
而塔位在 pv（未点亮），不触碰「已点亮塔停测」的规则。

## 2. 家族画像（1552 字段全分类）

| 家族 | n | cov 中位 | cov 最低 | aC 中位 | aC 最高 | 类型 | 样例 |
|---|---:|---:|---:|---:|---:|---|---|
| 一致预期-快照/统计 (eps) | 123 | 0.924 | 0.454 | 0 | 50 | MATRIX:123 | `pv20_eps_indicator_0_feature0` |
| 一致预期-快照/统计 (ebt) | 123 | 0.789 | 0.344 | 1 | 36 | MATRIX:123 | `pv20_ebt_indicator_1_feature0` |
| 一致预期-快照/统计 (gps) | 118 | 0.899 | 0.358 | 0 | 11 | MATRIX:118 | `pv20_gps_indicator_1_feature0` |
| 一致预期-快照/统计 (sal) | 120 | 0.907 | 0.473 | 0 | 279 | MATRIX:120 | `pv20_sal_indicator_1_feature0` |
| 一致预期-快照/统计 (pre) | 117 | 0.892 | 0.370 | 0 | 26 | MATRIX:117 | `pv20_pre_indicator_1_feature0` |
| 一致预期-快照/统计 (net) | 116 | 0.912 | 0.428 | 0 | 11 | MATRIX:116 | `pv20_net_indicator_1_feature0` |
| 一致预期-快照/统计 (opr) | 109 | 0.562 | 0.301 | 0 | 11 | MATRIX:109 | `pv20_opr_indicator_1_feature0` |
| IBES 组预测信号 | 46 | 0.877 | 0.645 | 0 | 13 | MATRIX:46 | `ibes_ebt_group6_signal_12` |
| 厂商算法估计 (eps_forecast) | 34 | 0.895 | 0.541 | 0 | 12 | MATRIX:34 | `eps_forecast_0_12` |
| 厂商算法估计 (projection) | 16 | 0.914 | 0.645 | 0 | 2 | MATRIX:16 | `ebt_projection_9_5` |
| 厂商模型信号 (predictor) | 12 | 0.829 | 0.505 | 0 | 2 | MATRIX:12 | `ebt_predictor_p4` |
| 前瞻预测信号 (forward_estimate) | 15 | 0.830 | 0.443 | 0 | 2 | MATRIX:15 | `forward_estimate_signal_7_10` |
| 季度 as-reported (`pv20_q_*`) | 43 | 0.788 | 0.254 | 0 | 6 | MATRIX:43 | `pv20_q_1_announcement_dt` |
| as-reported 其他 (`pv20_a*`) | 67 | 0.833 | 0.267 | 2 | 14 | MATRIX:56 / VECTOR:11 | `pv20_a2_announcement_dt` |
| 事件前后共识（before/aftercons） | 8 | 1.000 | 1.000 | 0 | 3 | **VECTOR:8** | `pv20_beforecons_high_100` |
| Revere 行业分类 | 11 | 0.704 | 0.678 | 9 | 18 | **GROUP:11** | `pv20_revere_group_5_3_sector` |
| 特异收益 / 风险模型 | 15 | 0.755 | 0.069 | 1 | 45 | MATRIX:15 | `barra_ustm0_top1000_specific_return` |
| beta / 风险因子 | 36 | 1.000 | 0.500 | 1 | 5 | MATRIX:36 | `beta_ccmp_250d` |
| ETF 分组/聚类 | 3 | 0.110 | 0.110 | 0 | 0 | MATRIX:3 | `etf_top300_00_grouping` |
| 交易成本 / 滑点 / adv | 11 | 1.000 | 1.000 | 2 | 10 | MATRIX:11 | `adv20_usd_capped_100m` |
| 价量微结构 | 63 | 0.500 | 0.500 | 0 | 27 | MATRIX:63 | `close_to_open_return` |
| 其他（含 VECTOR 21 个） | 346 | 0.684 | 0.279 | 0 | 232 | GROUP:3 / MATRIX:322 / VECTOR:21 | `adv_alternative` |

**读法**

- **信号面在头部七族（826 字段）**：一致预期快照家族字段量最大、覆盖最好（中位 0.79–0.92）。
- `opr`（营业利润）覆盖只有 0.562，低于可安全裸用的经验线，用前必须 `ts_backfill` 或弃用。
- `price/volume` 那 63 个字段 coverage 一律 **0.500**——它们在 TOP3000 里只覆盖 TOP1500，**不是全宇宙字段**，
  本区若用它们要先确认样本域（本集不是拿来挖价量的，登记备查）。
- ETF 三字段 coverage 0.11 ⇒ 实质不可用。
- **风险模型特异收益族有 15 个，语义与 pv47 重叠**（见 §6 风险）。

## 3. 元数据质量警告（必须先读再用）

1. **描述大面积错贴**：`pv20_gps/sal/pre/net/opr_indicator_*` 的 description 大量写着
   "Pre-tax Profit"（ebt 的文案），与字段前缀不符。逐条比对 1552 条后确认：
   **只有 `eps` 与 `ebt` 两族的 feature 0/1/2 有可信的明确语义**，其余族的 feature 编号语义
   **无法从元数据判定**。⇒ 任何依赖「feature N 是某统计量」的设计，在 eps/ebt 以外的族上都是猜测。
2. **feature 编号语义（仅 eps / ebt 可用）**

   | feature | eps 语义 | ebt 语义 |
   |---|---|---|
   | 0 | `mean_flash`（均值·最新快报） | `mean_flash` |
   | 1 | **median 3 months ago**（3 个月前中位数） | 同 |
   | 2 | **median 4 weeks ago**（4 周前中位数） | 同 |
   | 3–12 | "Non-trivial feature"（不透明） | 不透明 |

   ⇒ feature1 → feature2 的差是**一条真实的两月修正**（有明确时间标注），是全库少见的
   「把修正幅度直接做进字段」的构造，也是批次 46A 的 R4/R5 臂。
3. **indicator 编号**：0–9 共 10 档，1/2/3/4 各 87–91 字段齐整（7 科目 × 13 feature），
   描述里 indicator_1 标 "[Fiscal Year 1]" ⇒ 编号大概率对应**财年/预测期**，但同样未逐档证实。
4. 没有任何 `frequency` 字段。更新频率只能**推断**（§5），不可当事实引用。

## 4. 可用性与预处理规则（本集）

- cov < 0.40 的字段（各家族最低值 0.25–0.47 那一批）**先 `ts_backfill(..., 66)`**，
  或直接弃用；裸用会得到集中持仓，即使 IS 好看也会挂 `CONCENTRATED_WEIGHT`。
- `opr` 族整族按 < 0.6 处理：主信号不用，最多作条件/分组。
- VECTOR 字段（`pv20_before/aftercons_*` 8 个 + 其他 21 个）**必须先 `vec_*` 聚合**再进标量算子；
  本集 40 个 VECTOR 里只有 8 个是「事件前/后共识」，语义清楚，可作事件条件腿。
- GROUP 字段（Revere 11 个）只能作分组轴，不能作信号。

## 5. 更新频率（推断，非平台元数据）

| 家族 | 推断频率 | 依据 |
|---|---|---|
| `*_indicator_*` feature0（mean_flash） | 日更 | IBES flash 随估计录入更新 |
| `*_indicator_*` feature1/2（3 个月 / 4 周前快照） | **4 周档位滚动** | 描述明示 lookback，取的是固定快照 |
| `ibes_*_group*_signal_*` / `forward_estimate_signal_*` | 日更 | 厂商「预测信号」产物 |
| `pv20_q_1_ard_*`（as-reported） | **季更** | 季度财报科目 |
| `specific_return_*` / `beta_*` | 日更 | 风险模型日频输出 |
| `adv*` / `slippage*` | 日更 | 价量衍生 |

⇒ 主信号族（预期）是**日更但有档位台阶**：`ts_delta(F, 63)` 捕捉的是两次档位跨越，
不是逐日漂移——这也是 R1–R3 选 63 日窗的原因（对齐「3 个月」的快照跳变）。

## 6. 分布特征：可得与不可得

**平台元数据里没有分布量**（min/max/分位/偏度一概没有），本仓也没有 pv20 的离线抽值缓存。
可作的是「结构性推断」，不可作的是「数值性断言」：

| 维度 | 现状 | 处理 |
|---|---|---|
| 单位/量纲 | 预期族是**每股金额**（EPS/EBT/Sales 每股），跨科目比值（EBT/营收）前需同度量 | 46A 的 M1/M2 用同科目比值，已按此构造 |
| 零值/缺失 | 覆盖 0.79–0.92 ⇒ 缺失 8–21%，未披露者无值 | 全部经 `ts_backfill(...,252)` 进壳 |
| 极端值 | 预期可能为负（亏损公司），比率腿可能爆量 | `winsorize(std=4)` 已在壳内 |
| 数值分布（偏度/分位） | **无直读通道**；要拿只能走 BRAIN Labs（`emit_labs_script` 出脚本 → 平台跑 → `ingest_labs_result` 回收） | 若后续需要剪裁阈值，先跑一次 Labs；当前不需要（壳对分布不敏感） |

**这一条要如实标注**：本画像的「分布特征」是结构性的，不是统计量。若后续要动
`winsorize` 阈值或做分位变换，必须以 Labs 抽值为前据。

## 7. 三条机制路线与首批

| 路线 | 经济机制 | 字段 | 为什么可能有效 | 风险 |
|---|---|---|---|---|
| **修正 R** | 分析师预期修正是美国最稳的基本面异象（post-revision drift） | eps/ebt/gps `feature0`、feature1→2 快照差 | 已证机制换数据源：`e76xgXkM`（Δ63 自归一）S1.89 / prod 0.55 | 与 `e76xgXkM` 同源 IBES ⇒ prod 可能被抬；aC=0 说明没人挖过，但源相同 |
| **利润率 M** | 营收与利润预期修正的**背离**＝隐含利润率变化（单一信号，不是两腿相加） | `EBT/营收`、`毛利/营收` 的 Δ63 | 利润率扩张是质量类异象，且与单纯修正正交 | 比值在分母近零时不稳定 |
| **模型-共识 S** | 厂商算法估计 vs 卖方共识的**分歧** → 私有信息或错误定价 | `eps_forecast_6_6/11` vs `eps_indicator_1_feature0` | 两套独立估计体系的差异是真正的「意外」 | 期次可能不一致（type 6 vs FY1），需首批标定 |
| 特异收益 P | 残差收益的短期反转 | `specific_return_gemtr_adv_allfactors_usd` 5 日 | 经典反转，aC 低 | **pv47 同族 prod 墙 0.9362**；只放 1 臂 |
| IBES 组信号 G | 厂商预算好的预测信号（语义不透明） | `ibes_ebt_group6_signal_12`（aC 13，族内最高） | 若有效则直接是成品信号 | 不透明；只放 1 臂标定 |

**批次 46A（10 臂）已收批**（multisim `1HQpXg8Vd5a5aBe2wtFGzy3`，10/10，入库 10 行）。
逐臂指标与归因见交付日志附录 AG §D，这里只留判决：

| 路线 | 最强臂 | S | F | 2Y | risk_neut_S | 判决 |
|---|---|---:|---:|---:|---:|---|
| **修正 R**（feature0 Δ63） | `VkdNoXNV` ebt | 1.03 | 0.50 | 1.93 | 0.73 | 信号在，强度不足 |
| **快照修正 R'**（F2−F1） | `rKd7mb01` ebt | **1.13** | **0.58** | 1.72 | **0.97** | **本集最强路线** |
| 利润率 M（同源比值） | `E5VQAqmL` gps/sal | 1.04 | 0.50 | 2.00 | 0.59 | 可用，DD 仅 4.95% 全批最优 |
| 模型-共识 S | `ZYmaLjgx` | 0.77 | 0.33 | 0.76 | 0.61 | 跨源口径差 ⇒ 弃 |
| **特异收益 P** | `leMaZ7EA` | **0.03** | 0.00 | 0.44 | 0.10 | **判死，封存** |
| IBES 组 G | `A1QxdnrR` | 0.86 | 0.39 | 0.60 | 0.35 | 不透明且四项失败 ⇒ 弃 |

三条结构性结论（46B/46C 实测后已更正第 2 条，见下）：

1. **快照差优于区间差分**：F2（4 周前）−F1（3 个月前）跨 8 周真实预期位移，`ts_delta(F0,63)`
   跨 63 个交易日净变化（含往返噪声）⇒ 后续修正路线一律优先用 `feature2 − feature1`。
2. **换手贴 1% 下限是本集的结构性特征**（全批 0.95%–1.03%，4 臂吃 `LOW_TURNOVER`），
   但**根因不是壳**：46B 单算子消融证明 **`quantile` 与换手无关**（拆掉后 0.89%，反而更低），
   `hump` 才是那个既压换手又压信噪比的算子（拆掉换手 6.00% 但 S 1.13→0.73、SUB 0.23 跌破线）。
   ⇒ **本集的换手无法在保信号的前提下修好**，要提换手只能引入更高频成分，不是继续拆壳。
3. **`specific_return_*` 分支与 pv47 的 prod 0.9362 同族，且这里 IS 就死** ⇒ 永久封存，
   不再为它花任何仿真（这条比 prod 读数更早给出否决）。

**46B / 46C 实测补充（2026-10-22，14 臂已入库）**

| 项 | 结果 | 含义 |
|---|---|---|
| 新最强臂 | **`JjP8llgW`（B8）S 1.31 / F 0.67 / 2Y 2.59 / DD 4.10% / risk_neut 0.96** | `ts_av_diff(EBT_F2/EBT_F1, 252)` 取代 `ts_zscore(ts_backfill)`；USA 慢变量上 `ts_av_diff` 更优（与 fnd21 一致） |
| 增长归一化（B1–B5、B10） | eps 0.79→0.92、ebt 1.03→0.98、gps 0.95→0.97 | **中性**，归因「高价股放大」不成立；252 日同比更差（DD 12–16%） |
| 拆 `hump`（B6）/ 拆 `quantile`（B7） | 6.00% TO / 0.73 S ↔ 0.89% TO / 1.15 S | 换手与信噪比在本集**绑定在同一个算子上** |
| 设置层 RAM + decay 20（46C） | TO 修到 4.75–5.33%，但 2Y 三臂崩到 0.92 / 1.00 / 1.03 | **cell 级设置不能跨数据集照搬**，`e76xgXkM` 的配置迁不过来 |

⇒ **本集预期快照（feature 0/1/2）分支到此为止**，不再加变体。

**46D / 46E 实测补充（2026-10-22，22 臂已入库：46D 12 + 46E 10）**

| 批 | 臂 | 最强 | S | F | 2Y | TO | SUB | risk_neut | 判决 |
|---|---|---|---:|---:|---:|---:|---:|---:|---|
| 46D 设置层 | 12（中性化 7 档 + decay / hump / avdiff 窗） | `KPmg1LZ8` INDUSTRY | **1.37** | 0.74 | 2.46 | 0.99% | 0.88 | **1.00** | 全批最强，仍差 S/F/TO 三闸 |
| 46E 事件共识 | 10（VECTOR `vec_avg/max/min` × 事件后/前共识） | `e761rYNM` disp-narrow max | 1.11 | **0.86** | 2.47 | 2.94% | — | — | 唯一 F≥0.8，但 DD 15.23% + 多空 1958/815 ⇒ 不可交 |

中性化排序（同核）：`INDUSTRY 1.37 > MARKET 1.30 > SECTOR 1.27 > SUBINDUSTRY 1.31 ≈ CROWDING 1.23 >
SLOW_AND_FAST 1.05 > STATISTICAL 0.93` ⇒ **中性化不是本集的钥匙**（跨度 0.44，且 INDUSTRY 也只有 1.37）。
同一族内 **聚合方式（`vec_avg/max/min`）比壳更决定结果**（E1/E2/E9 = 0.58/0.28/0.99）。

⇒ **路线裁决（D15 探针失败）**：pv20 共 **46 臂、0 进 S4、0 可提交**，最高 S 1.37 < 1.58。
**本数据集判死，不再加变体**。缺口转未点亮塔的新数据集：
`earnings` 类别（本季 1 次提交，未点亮）的 `earnings_chart_dl`
→ 画像 [`_usa-earnings-chart-dl-field-profile-20261022.md`](_usa-earnings-chart-dl-field-profile-20261022.md)。
`pv20_q_1_*` / `pv20_a*` 只有资产负债表科目、无利润表实际值 ⇒ **SUE/PEAD 在本集不可构造**，该分支作废。

## 8. 存档索引

- 本文件：`Claude/skills/wq-brain-ra-usa/references/_usa-pv20-field-profile-20261022.md`
- 全字段清单：`_usa-pv20-field-inventory-20261022.md`（1552 行）
- 交付日志：`_usa-atom-delivery-log-20261020.md` 附录 AG
- 机制母本：`_usa-analyst-consensus-fa-overlay-field-profile-20261021.md`（`e76xgXkM`）
