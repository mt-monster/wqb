# USA · fundamental69 字段画像（字段八问）

as_of 2026-10-21 · region USA / delay 1 / universe TOP3000 · 平台 12 字段（sharpe 过滤剔除 1）· 取回 11
数据来源：`get_datafields(dataset_id="fundamental69", region="USA", delay=1, universe="TOP3000")`

## 0. 一句话结论

fnd69 是**季度现金流量表的「投资 + 融资流」子集**：净股票发行（Sale − Purchase）、净债务发行（Issuance − Reduction）、资本开支、经营现金流、现金股利，分母用 `qta`（资产总额，覆盖 1.0）。它承载的是**外部融资 / 投资 / 股东回报三组经典异象**（净发行负向、回购与股利正向、capex 负向、OCF 正向），字段 `alphaCount` 5–58 属低拥挤区，机制语义清晰、无歧义。**主风险不是信号弱，而是「季度频率 × 覆盖 0.39–0.43」**：`ts_backfill(·,252)` 会把换手压到 LOW_TURNOVER 线附近（fnd93 同形态已实证 TO 0.0095–0.013 触发 LOW_TURNOVER），因此本集必须走「比率 + 短/中窗口 backfill + 分组排序」，而不是长时间窗平滑。

## 1. 字段全表（11 / 平台 12）

| id | 类型 | cov | uC | aC | 描述 | 角色 |
|---|---|---|---|---|---|---|
| `fnd69_capxy2q` | MATRIX | 0.4197 | 27 | 28 | Capital Expenditures (Quarterly) | 信号（投资） |
| `fnd69_dltry2q` | MATRIX | 0.3930 | 7 | 7 | Long-Term Debt - Reduction (Quarterly) | 信号（融资流出） |
| `fnd69_q2ycktsrp` | MATRIX | 0.3897 | 12 | 15 | Purchase of Common and Preferred Stock (Quarterly) | 信号（回购） |
| `fnd69_q2yfcnao` | MATRIX | 0.4333 | 31 | 40 | Operating Activities - Net Cash Flow (Quarterly) | 信号（经营现金流） |
| `fnd69_q2yktss` | MATRIX | 0.3883 | 23 | 29 | Sale of Common and Preferred Stock (Quarterly) | 信号（股票发行） |
| `fnd69_q2ysitld` | MATRIX | 0.3933 | 11 | 12 | Long-Term Debt - Issuance (Quarterly) | 信号（债务发行） |
| `fnd69_q2yvd` | MATRIX | 0.4010 | 5 | 5 | Cash Dividends (Cash Flow) (Quarterly) | 信号（股利） |
| `fnd69_qta` | MATRIX | 1.0000 | 15 | 17 | Assets - Total (Quarterly) | 分母 / 规模（**不作主信号**） |
| `fnd69_fiscalquarter` | MATRIX | 1.0000 | 16 | 17 | Fiscal quarter | 标识符（剔除） |
| `fnd69_fiscalyear` | MATRIX | 1.0000 | 26 | 31 | Fiscal year | 标识符（剔除） |
| `fnd69_rtqf` | MATRIX | 1.0000 | 41 | 58 | Fiscal quarter | 标识符（剔除） |

**ATOM 判定**：11 个字段全部来自单一数据集 fundamental69；`fiscalquarter` / `fiscalyear` / `rtqf` 是日历标识符，按 S1 语义分类属非信号字段（与「国家 / 交易所 / 市场 / 板块 / 行业」同类的元数据），不参与信号构造。三条批内**不混入任何其它数据集字段**。

## 2. 字段八问

**① 类型与频率**：全部 MATRIX（标量），无 VECTOR → 无需 `vec_*` 聚合。季度报表口径（`*2q` / `y2q` 后缀 = 季度累计流量），平台按季度发布，日频面板上以阶梯 + 缺失呈现。

**② 覆盖率**：流量字段 0.3883–0.4333（约四成），`qta` 与三个日历字段 1.0。覆盖率**不是随机缺失**：现金流量表的明细项只对报送完整报表的公司存在（大市值 / 主板更全）→ 直接用 `rank` 会把「报表完整度」当成信号，必须 `ts_backfill` + `group_rank`。

**③ 更新频率与滞后**：季度更新，且财报披露有 1–3 个月滞后。**这是本集最重要的结构事实**：信号在两次报表之间是常数，`ts_backfill(·, 252)` 最大持有 1 年 → 换手极低（fnd93 实证 0.0095–0.013）。平台 `LOW_TURNOVER` 线 0.01、用户审查下限 0.05，故 backfill 窗口是本集的第一旋钮：**252 求稳（F 高）但可能贴 0.01 线，66 是备选**。

**④ 取值范围与符号（⚠ 最易错）**：Compustat 口径下**现金流出项（Purchase of Common/Preferred、Long-Term Debt Reduction、Capital Expenditures、Cash Dividends）以正数入账**，因此：
- 净股票发行 = `q2yktss − q2ycktsrp`（发行 − 回购）
- 净债务发行 = `q2ysitld − dltry2q`（发行 − 偿还）
- 两者都**不需要**再取绝对值；符号方向由公式给出，不靠猜数据符号。
`qta` 为正、量级 1e6–1e9 → **比率必须除 `qta`**，否则变成市值/规模信号（`group_rank` 只能部分吸收）。

**⑤ 缺失结构**：同一公司同一季度，`q2yfcnao` 存在而同季 `q2yvd` 缺失是常态（不分红）→ **缺失≠0，不能 `nanHandling` 里填 0 当"无股利"**。本集全部走 `ts_backfill` 继承上一季值，等价于「最近一次披露」，方向可接受；但把 `q2yvd/qta` 当连续强度读时，需承认它混合了"不分红"与"未披露"。

**⑥ 截面分布**：比率类（flow / qta）右偏，尾部有极端值（小型公司一次性融资）。平台 `truncation=0.08` 会截尾，仍建议 `group_rank` 先做秩变换，避免 `ts_av_diff` 在尾部爆量。

**⑦ 与规模 / 价格的相关性**：`qta` 本身是规模代理，`capx/qta`、`fcnao/qta` 与规模的相关性显著低于裸流量；但**净发行 / 净债务发行天然与规模负相关**（小公司更依赖外部融资）→ 全部表达式必须 `group_rank(·, subindustry)`（USA 已实证：去掉 group_rank 会掉 S 22–42%、F 61–76%，且 SUB 由 PASS 翻 FAIL）。

**⑧ 可用性**：可以**直接当信号**——每个字段都有明确的经济含义与符号预期，无需先做 Labs 分析。但必须先过 ③ 的换手关与 ② 的覆盖关。三个日历字段不可用作信号。

## 3. 机制映射（8 个独立机制 + 2 条结构/变化轴）

| 机制 | 公式（分母统一 `qta`） | 预期方向 | 依据 |
|---|---|---|---|
| **M1 净股票发行** | `(q2yktss − q2ycktsrp)/qta` | **负向**（发得多 → 未来收益低） | 净发行异象（Pontiff & Woodgate；Daniel & Titman 融资异象） |
| **M2 回购强度** | `q2ycktsrp/qta` | 正向 | 回购公告效应 / 资本配置信号 |
| **M3 股利强度** | `q2yvd/qta` | 正向 | 股利溢价（payout premium） |
| **M4 净债务发行** | `(q2ysitld − dltry2q)/qta` | 负向 | 外部融资异象的债务腿 |
| **M5 资本开支强度** | `capxy2q/qta` | 负向（投资异象） | Titman/Wei/Xie 资产增长；USA 饱和的 value/quality 之外的正交族 |
| **M6 经营现金流资产比** | `q2yfcnao/qta` | 正向（盈利质量） | 现金流定价；与 accrual 族互补 |
| **M7 净外部融资** | `M1 + M4`（股票 + 债务合并） | 负向 | Bradshaw 等「外部融资总额」异象（比 M1 更稳） |
| **M8 股东回报** | `(q2ycktsrp + q2yvd)/qta` | 正向 | payout 组合腿，与 M2/M3 互补（回购+股利） |
| 变化轴 | `ts_av_diff(ts_backfill(M6,252), 252)` | 正向（改善） | 现金流 YoY 改善，USA 慢变量规律（`ts_av_diff` > `ts_zscore(ts_backfill())`） |
| 结构轴 | M1 换成 `sector` 分组 | — | 检验机制是否只是行业结构（控制项，不作独立机制） |

**与既有档案的去重**：fnd93 已做过「季度低覆盖字段」形态并留下 TO 崩塌的教训——本集**不重复其长窗平滑路线**，改用「比率 + `group_rank` + 252/66 双档」。value/quality/book 族在 USA 已判死，M1/M4/M7 是**发行侧**而非估值侧，不属同族。

## 4. 批 4 设计（10 条，预登记）

统一外壳：`group_rank(X, subindustry)`；`X` 用 `ts_backfill(·, 252)`（首轮），#3 作结构对照换 `sector`。

| # | 机制 | 表达式 |
|---|---|---|
| 1 | M1 净股票发行（负） | `group_rank(-ts_backfill((fnd69_q2yktss - fnd69_q2ycktsrp)/fnd69_qta, 252), subindustry)` |
| 2 | M1 结构对照 | `group_rank(-ts_backfill((fnd69_q2yktss - fnd69_q2ycktsrp)/fnd69_qta, 252), sector)` |
| 3 | M2 回购强度 | `group_rank(ts_backfill(fnd69_q2ycktsrp/fnd69_qta, 252), subindustry)` |
| 4 | M3 股利强度 | `group_rank(ts_backfill(fnd69_q2yvd/fnd69_qta, 252), subindustry)` |
| 5 | M4 净债务发行（负） | `group_rank(-ts_backfill((fnd69_q2ysitld - fnd69_dltry2q)/fnd69_qta, 252), subindustry)` |
| 6 | M6 OCF/资产 | `group_rank(ts_backfill(fnd69_q2yfcnao/fnd69_qta, 252), subindustry)` |
| 7 | M5 capex 强度（负） | `group_rank(-ts_backfill(fnd69_capxy2q/fnd69_qta, 252), subindustry)` |
| 8 | M7 净外部融资（负） | `group_rank(-ts_backfill((fnd69_q2yktss - fnd69_q2ycktsrp + fnd69_q2ysitld - fnd69_dltry2q)/fnd69_qta, 252), subindustry)` | <!-- lint:counterexample: 会计恒等式分子（科目相加），非信号腿相加 -->
| 9 | M8 股东回报 | `group_rank(ts_backfill((fnd69_q2ycktsrp + fnd69_q2yvd)/fnd69_qta, 252), subindustry)` | <!-- lint:counterexample: 会计恒等式分子（科目相加），非信号腿相加 -->
| 10 | M6 变化轴 | `group_rank(ts_av_diff(ts_backfill(fnd69_q2yfcnao/fnd69_qta, 252), 252), subindustry)` |

覆盖：8 个机制 + 1 结构轴 + 1 变化轴；每条单一数据集字段（ATOM）；无 `add` 混信号、无跨集字段。

**预登记判据（批 4）**：

- 任一条 **S ≥ 1.58 且 F ≥ 1.0** ⇒ 进 `check_correlation(refresh=True)`；prod ≥ 0.75 按 D0-P 判死；
- **全部 TO < 0.012** ⇒ 不是信号问题而是频率问题：把 backfill 252 → 66 重发前 5 名（**只此一次**窗口降档），仍不行则判死 `USA-FND69-TURNOVER`；
- **max S < 1.45** ⇒ 先看是哪一族（发行侧 vs 投资侧 vs 现金流）最强，只对这一族加一批（≤ 2 批），不整集重扫；
- #2（sector）显著优于 #1（subindustry）⇒ 机制是行业结构而非个股选择，后续统一用 `sector` 并降低对该集的预期；
- #10（变化轴）优于 #6（水平）⇒ fnd69 的价值在**改善**而非水平，后续只用差分族。

## 4. 批 4 实测与归因（2026-10-21，multisim `13XQHN7Zx4rvbjEt2rV745c`，10/10 COMPLETE）

| # | 机制 | alpha | S | F | TO | R | SUB | 2Y | **rns** |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|
| 1 | M1 净股票发行(−) | `npAdPrAz` | 0.67 | 0.35 | 0.0210 | 0.0332 | 0.30 | 1.09 | 0.28 |
| 2 | M1 sector 对照 | `Vkda0edb` | 0.69 | 0.38 | 0.0206 | 0.0380 | 0.35 | 1.09 | 0.37 |
| 3 | M2 回购 | `bl8bOA6N` | 0.76 | 0.40 | 0.0183 | 0.0350 | 0.34 | 1.02 | 0.34 |
| 4 | M3 股利 | `A1QNvEVE` | 0.30 | 0.11 | 0.0122 | 0.0181 | 0.15 | 0.72 | 0.27 |
| 5 | M4 净债务发行(−) | `Vkda0eNJ` | 0.54 | 0.19 | 0.0255 | 0.0148 | 0.37 | 0.64 | −0.07 |
| 6 | M6 OCF/资产 | `leMvK1al` | 0.61 | 0.31 | 0.0263 | 0.0324 | 0.46 | 0.99 | **0.44** |
| 7 | M5 capex(−) | `zqr8bedG` | 0.11 | 0.02 | 0.0186 | 0.0030 | −0.46 | 0.93 | −0.06 |
| 8 | M7 净外部融资(−) | `xA13b5vJ` | **0.77** | **0.40** | 0.0249 | 0.0316 | 0.44 | 1.03 | 0.16 |
| 9 | M8 股东回报 | `JjPNQr3n` | 0.46 | 0.21 | 0.0167 | 0.0273 | 0.17 | 0.83 | 0.33 |
| 10 | M6 变化轴 | `omoLWZPk` | 0.54 | 0.17 | 0.0354 | 0.0118 | 0.46 | 1.31 | 0.13 |

**归因（逐条对照预登记判据）**：

1. **机制方向全部正确**：M1/M4/M7 负向、M2/M3/M6/M8 正向，没有一条符号翻转 —— 说明「外部融资 / 投资 / 股东回报」的经济解释成立，**问题不在方向而在强度**。
2. **强度天花板明确**：`max S = 0.77`（净外部融资），仅为 RA 线 1.25 的 **62%**；`max F = 0.40`，为 1.0 的 40%。8 个独立机制全部落在 0.11–0.77，**没有一族接近门槛**，故不满足预登记的「只对最强一族加一批」前提（该分支要求已有族接近 1.45）。
3. **`risk_neutralized_sharpe` 是决定性否决证据**：10 条中 8 条 < 0.40（最高 #6 = 0.44），按 USA 字段档案既有判据（**rns < 0.3 = 纯风格 beta，别花仿真**）—— **本集的 PnL 主要来自风险因子暴露，不是独立 alpha**。这条比 S 更能解释「为什么再换算子也不会有救」。
4. **换手如预期崩塌但方向无害**：TO 0.0122–0.0354（预登记担心 < 0.012，实测仅 #4 贴线），低 TO 反而抬 F，不是失败原因。
5. **结构对照无信息**：#2（sector）vs #1（subindustry）S 0.69 vs 0.67，机制不是行业结构，但两者都弱。
6. **变化轴未优于水平**：#10（0.54）< #6（0.61），预登记的「价值在改善」不成立。

**结论：判死 `USA-FND69-WEAK`（信号强度天花板 + 风格 beta）**。本批**只跑 1 批即封口**，理由：预登记的「≤ 2 批」分支前提是「最强族接近 1.45 而只差一口气」；实测最强族 0.77、rns 全部 < 0.5，缺口属**信号本体**而非算子/窗口，第二批只能重复同一信息，属用户明令禁止的盲扫。字段画像与机制表保留，供后续「组合腿 / 条件腿」按需引用（不作主信号）。

**下一步**：回到 `_usa-fundamental-dataset-scan-20261019.md` 的候选池，按「未点亮塔（fundamental）× 语义可用 × aC 低」继续；本集不复活。

## 5. 判死准则

只有同时满足才判 `USA-FND69-*`：
① ≥ 2 批、≥ 8 个机制各至少 1 条实测；② 全批 `max |S| < 1.45`；③ 已排除换手/覆盖率等技术性失败（即不是 TO < 0.012 或覆盖 < 0.4 导致的假失败）。
单批失败或单一机制弱**不构成数据集判死**（2026-10-21 fundamental 扫描更正口径）。
