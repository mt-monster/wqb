# hiring_trends「Job Postings / 招聘需求」字段画像与战役档案（2026-10-21）

> 区域口径：USA / TOP3000 / Delay 1 / ATOM（3 个字段全部来自 `hiring_trends`；分组字段 subindustry 属豁免）。
> 判死口径沿用 USA 纪律：S≥1.58 / F≥1.0 / 2Y≥1.58 / SUB/|S|≥0.43 / TO∈[1%,70%]；先读 `rns`（<0.3 = 风格 beta）。
> 提交前必须 `check_correlation(refresh=True)` 实测 prod/self 均 <0.7，且用户明确确认。 <!-- from config.prod_corr_max -->

## 0. 选集理由（2026-10-21，接 other359 判弱之后）

**上一集结案**：`other359`（Web Comments & Reaction Data）单批 10/10 后按预注册规则 3 判弱封存
（`USA-OTHER359-WEAK`，详见 [`_usa-other359-field-profile-20261021.md`](_usa-other359-field-profile-20261021.md) §5）。
换集原因逐条可核：

| 判据 | other359 | hiring_trends |
|---|---|---|
| 库内历史回测行 | 10（本批） | **0**（`backtest_results WHERE dataset='hiring_trends'` 实测 0 行） |
| 是否在 dead_end 名单 | 本批新增 | **不在**（`registry_empirical` USA 42 条 dead_end 实测无此集） |
| 塔状态 | other / 未点亮 / ×1.4 | other / 未点亮 / **×1.7**（全 USA 未点亮塔里最高倍率之一） |
| 机制可陈述性 | 社媒情绪（已六次判死） | **劳动力需求 → 未来增长**（Belo-Lin-Bazdresch 2014），与价量/分析师/基本面零同源 |
| 字段数 | 10 全 VECTOR | 3 全 VECTOR（ATOM 自动满足，算子空间小 ⇒ 可真正穷尽） |
| 覆盖 | 0.6882–0.80 | **0.4966–0.4998**（>0.4 阈值，仍需 backfill 处理缺口） |
| 拥挤度 | aC 2–17 | 字段 aC 79–340（**`aggregate_open_positions_count` aC 340 = 全集中最挤**）|

**为什么不选 `fund_holdings_panel`**（原本的第一候选）：实测 `backtest_results WHERE dataset='fund_holdings_panel'` = **148 行**
（最近 2026-10-12），且交付日志已记 `mean_security_weight` Δ63 S1.34/DD 2.45%、DL 图表预测 2Y 2.21 但全期 S 0.54
⇒ **已挖过、非新面**，不是"无计可施才换集"该挑的对象。`hiring_trends` 才是零历史回测的那一格。

**已知风险**：① 覆盖率 ≈0.5，若 backfill 策略错会把「没抓到招聘」当成「招聘归零」；② 字段级 aC 340 ⇒
招聘类信号在 USA 被大量使用，prod 先验不低；③ 只有 3 字段 ⇒ **无第二个信号轴可救**，一条不成就得整集判死。

## 1. 字段全表（3 / 平台 3，全 VECTOR）

`get_datafields(region=USA, universe=TOP3000, delay=1, dataset_id="hiring_trends")` 实测（`platform_count: 3, complete: true`）：

| # | 字段 | 语义（平台原文） | cov | uC | aC |
|---:|---|---|---:|---:|---:|
| 1 | `aggregate_open_positions_count` | Total job openings on the website as of 'snapshot_date' —— **存量**（当日挂着的岗位总数） | 0.4998 | 130 | **340** |
| 2 | `fresh_open_positions_count` | New job openings found for this company as of 'snapshot_date' —— **流量**（当日新挂） | 0.4998 | 50 | 79 |
| 3 | `rolling_84d_new_positions_sum` | Count of job openings newly posted over the trailing 84 days up to the snapshot date —— **已平滑的 84 日流量** | 0.4966 | 77 | 173 |

**结构观察**

1. **存量 / 流量 / 平滑流量三件套**：`aggregate` = 岗位存量（≈ 用工规模 + 招聘强度），`fresh` = 当日新增（噪音大、时效强），
   `rolling_84d` = 84 日累计新增（供应商已做平滑，等于**厂商版的中期招聘趋势**）。三者不是同一量的三种精度：
   存量对**规模**敏感（大公司永远大），流量对**变化**敏感。
2. **全 VECTOR**：每行是一组岗位记录 ⇒ 必须 `vec_*` 聚合。按论坛 43031425132823 纪律：
   计数类 `vec_sum`；每记录强度/比率 `vec_avg`；记录条数 `vec_count`；记录间离散 `vec_stddev`。
   **`ts_backfill` 一律放在 vec 聚合之后**。
3. **覆盖率 0.4966–0.4998**：>0.4 阈值故不强制 `group_backfill`，但**明令禁止 group_backfill**（见 §2.4 第 8 条）——
   把行业均值注入个股会把「这家公司没被爬到」变成「这家公司招聘=行业中位」，直接制造伪信号。
4. **`rolling_84d` 的 84 天窗口与 `ts_delta(…,63)` 的组合要小心**：84 日已平滑量再做 22 日差分 ≈ 两次重叠平滑，
   信号会滞后 ~3 个月；本批只用它做「相对自身历史分位」与「事件门控的内层量」，不做短窗差分（唯一例外 N8 明示）。
5. **aC 340** ⇒ `aggregate` 是全数据集最拥挤字段。**低 aC ≠ 低 prod，高 aC 一定不低 prod**（交付日志 §4 第 13 条）：
   本集一旦有全闸候选，prod 必须实测，且预期会撞墙。

## 2. 机制、壳与批 1 设计

### 2.1 机制（可陈述的收益来源）

| # | 机制 | 构造直觉 | 文献/逻辑 | 方向先验 |
|---|---|---|---|---|
| M1 | 招聘扩张 = 增长期权 | 岗位存量与时序增长 | Belo-Lin-Bazdresch (2014, JFE)：**hiring rate 高 → 未来收益高**（劳动力调整成本 → 扩张是需求信号，不是过度投资） | **正** |
| M2 | 资产增长 / 过度扩张 | M1 的同构造反号 | Cooper-Gulen-Schill (2008) 资产增长异象：扩张 = 过度投资 → 低收益 | **负**（与 M1 对撞，必须成对发） |
| M3 | 招聘广度 | 岗位记录条数 `vec_count` 的变化 | 广度=多岗位/多地点同时开；广度变化比总量更少受单一大岗位影响 | **正** |
| M4 | 岗位周转率（churn） | `fresh / aggregate` | 高周转 = 高离职 + 高替换成本（labor turnover → 低收益）；也可读作"扩张更激进" | **负** |
| M5 | 招聘结构离散度 | 岗位规模 `vec_stddev/vec_avg` | 少数大岗位主导 ⇒ 单点扩产（易受一次性订单影响）；离散度高 = 招聘计划不均衡 | **负** |
| M6 | 招聘加速 | `rolling_84d` 的短期增量 | 加速比水平更接近"预期差" | **正** |
| M7 | 事件条件：招聘激增日 | 只在关注度/招聘量异常日交易 | 与新闻 skill 的 event-conditioned 思路一致；把弱信号门控到信息日 | **正** |
| M8 | 时序分位（多年度高位） | `ts_rank(level,252)` | 招聘位于自身一年高位 = 趋势持续（比 z 分更稳健，慢变量） | **正** |
| M9 | 招聘存量 z 分（对照 M8） | `ts_zscore(level,66)` | 短窗相对自身基线 | 正 |

### 2.2 通用壳与聚合纪律

```
quantile(group_rank(winsorize(ts_backfill(<SIG>, 22), std=4), subindustry))
```

- `<SIG>` 内部先 `vec_*` 聚合，**再** `ts_backfill`（论坛 43031425132823 的顺序纪律）。
- `ts_backfill(...,22)` = 一个月：招聘数据按周/月更新，22 日是「补一个更新周期」，不是平滑。
- `winsorize(..., std=4)` 必须具名（preflight 会对 `std` 报 `unknown_fields` 假阳性，属已知误报；发批带 `validate_fields=false`）。
- `quantile(...)` 只接 1 个参数（平台硬约束）。
- 分组用豁免字段 `subindustry`；中性化用 cell 缺省 `SUBINDUSTRY`。

### 2.3 批 1（10 条，预登记，发批前写死）

| # | 桶 | 机制 | 构造（SIG 部分，外层走 §2.2 壳） | 方向 |
|---:|---|---|---|---|
| N1 | Level | M1 | `vec_sum(aggregate_open_positions_count)` | 正 |
| N2 | Level | M2 | `multiply(-1, vec_sum(aggregate_open_positions_count))` | 负 |
| N3 | Change | M1 | `divide(vec_sum(aggregate), add(ts_delay(vec_sum(aggregate),63),1))` | 正 |
| N4 | Change | M1 | `ts_zscore(ts_delta(vec_sum(aggregate),63),252)` | 正 |
| N5 | Change | M3 | `ts_zscore(ts_delta(vec_count(aggregate),63),252)` | 正 |
| N6 | Level(ratio) | M4 | `multiply(-1, divide(vec_sum(fresh), add(vec_sum(aggregate),1)))` | 负 |
| N7 | Dispersion | M5 | `multiply(-1, divide(vec_stddev(aggregate), add(vec_avg(aggregate),1)))` | 负 |
| N8 | Change | M6 | `ts_zscore(ts_delta(vec_sum(rolling_84d_new_positions_sum),22),252)` | 正 |
| N9 | Event-cond. | M7 | `trade_when(greater(ts_zscore(vec_sum(fresh),66),1), ts_zscore(vec_sum(rolling_84d_new_positions_sum),66), -1)` | 正 |
| N10 | Level | M8 | `ts_rank(vec_sum(aggregate),252)` | 正 |

算子覆盖：`vec_sum` / `vec_avg` / `vec_count` / `vec_stddev` 四种聚合（≥2 满足）；`ts_delay` / `ts_delta` / `ts_zscore` /
`ts_rank` / `trade_when` / `greater` / `multiply` / `subtract`（无）/ `divide` / `winsorize` / `ts_backfill` / `group_rank` / `quantile`。
形状：level ×3 / change ×4 / ratio ×1 / dispersion ×1 / event-cond. ×1；M9 未占槽（与 N1/N4 高度同族，留批 2）。

### 2.4 预注册止损规则（**先写后测，收批后不得改**）

1. **数据集级**：10 条 `max |S| < 1.0` ⇒ 构造层失败，判弱 `USA-HIRING-TRENDS-WEAK`，**不发批 2**。
2. **机制级**：同一机制 ≥2 条且 `max |S| < 1.0` ⇒ 该机制封存（N1/N2 属同一构造的 M1/M2 对撞，按一对合并判）。
3. **核心轴优先**：若 M1（招聘水平/增长）在**全部方向**上 `< 1.0`，**不再为 M3–M8 补批**——3 字段数据集没有第二个信号轴，
   换聚合器只是盲扫。
4. **过闸即测 prod**：任一条 `S≥1.58 ∧ F≥1.0 ∧ 2Y≥1.58 ∧ SUB/|S|≥0.43 ∧ TO∈[1%,70%]` ⇒ 立即
   `check_correlation(refresh=True)`；prod ≥0.7 按 D0-P 看直方图，`[0.7,0.8)` 桶 n≥1 ⇒ **族级封存，不磨参数**。
5. **风格 beta 早停**：`risk_neutralized_sharpe < 0.3` ⇒ 判风格 beta，不再修 SUB/2Y。
6. **频率问题单次降档**：全部 TO >70% 或 <1% ⇒ 只允许**一次**窗口降/升档重发前 5 名，仍不行则封存。
7. **批次上限**：最多 2 批（10 + ≤8）；批 2 **只许一个自由度**，且只能是下列之一：
   ① 中性化换档 SUBINDUSTRY → INDUSTRY（论坛 43322749748503 的「industry 分组」提示）；
   ② 窗口换档（22 ↔ 66 ↔ 252）。**不得同时改**（3 字段数据集同时改两个自由度 = 重置穷举）。
8. **覆盖率的唯一处理**：只允许 `ts_backfill(SIG,22)` 在 vec 聚合之后；**禁止 `group_backfill`**——
   会把行业均值注入缺失个股，制造伪信号。若某条因覆盖不足而持仓数过少（`long_count+short_count` 明显偏低），
   记录读数但不为此加 group_backfill，直接换形状。

### 2.5 论坛与文献取证

| 来源 | 可复用结论 | 对本批的作用 |
|---|---|---|
| 论坛 43322749748503《招聘变化与业务扩张：hiring_trends 在 USA 的因子化尝试》（92 票） | USA 的「**活动量相对变化 + industry 分组 + SLOW 中性化**」模板有效（帖内另一数据集 S3.00/F1.88）；**招聘类信号要做相对化，不要用绝对水平** | N3/N4/N5/N8 全部用相对化/时序归一；批 2 单自由度备选中性化换 INDUSTRY；N1/N2 的绝对水平是**反例对照**（验证"绝对水平不行"这条） |
| 论坛 43031425132823《vec 操作符解析》 | 计数类 `vec_sum`；每记录强度 `vec_avg`；条数 `vec_count`；**回填必须在 vec 聚合之后**；存量 vs 流量是两个 alpha | §2.2 顺序；N6 用 fresh/aggregate 区分存量流量；N5 用 `vec_count` |
| Belo, Lin & Bazdresch (2014, *JFE*) "Labor hiring, investment, and stock return predictability" | 招聘率高的公司未来收益高（劳动力调整成本 → 扩张含需求信息） | M1 方向先验（正）与 N1/N3/N4 的构造依据 |
| Cooper, Gulen & Schill (2008) 资产增长异象 | 总资产高增长 → 未来低收益（过度投资） | M2 的对撞先验 ⇒ N1/N2 必须成对发，符号由 S 判定 |
| 交付日志 §4 第 10 条 | 慢变量的真解是 `ts_zscore(Δ63, 252)`，不是对水平值做 z 分 | N4/N5/N8 的构造；N10 用 `ts_rank` 作对照 |
| `equity_forum_data` / `sentiment26` 判弱 | 纯关注度类在 USA 已被开采；时序归一会抹掉慢存量信号 | N1（绝对水平）预期最弱，若 N1 反而最强说明存量信号未被定价 |

### 2.6 批 2 预登记（收批 1 后、发批 2 前写死，2026-10-21）

**规则对账（逐条，不得事后改）**

| 规则 | 是否触发 | 依据 |
|---|---|---|
| 1 数据集级 max\|S\|<1.0 | **不触发** | N10 `qMExOLLZ` S=1.04 |
| 2 机制级（≥2 条且 max\|S\|<1.0） | **触发（仅 N1/N2 这一对）** | `vec_sum(aggregate)` 原始水平与其反号：0.80 / 0.09 ⇒ **该构造封存**，不再以绝对水平扩展 |
| 3 核心轴全方向 <1.0 | **不触发** | M1 的 N4 `ts_zscore(Δ63,252)` = 1.02（仅高出 2%，borderline） |
| 4 过闸即测 prod | **不触发** | 无一条 S≥1.58 ⇒ **prod 配额 0 消耗** |
| 5 风格 beta 早停 | **触发 5 条** | rns：N1 0.11 / N2 −0.50 / N5 −0.10 / N6 −0.66 / N9 0.28 ⇒ 判风格 beta，不为其修 SUB/2Y |
| 6 频率问题 | **不触发** | TO 1.86%–15.40%，全在 [1%,70%] |
| 7 批次上限 | 批 2 获准 | 见下 |
| 8 覆盖处理 | 遵守 | 仅 `ts_backfill(SIG,22)` 在 vec 之后；零 `group_backfill` |

**批 2 的单一自由度 = 中性化 SUBINDUSTRY → INDUSTRY**（规则 7 的第 ① 项）。
理由：招聘是强行业周期变量，SUBINDUSTRY 中性化把行业共同的招聘扩张成分一并剥掉；论坛 43322749748503 的
「活动量相对变化 + industry 分组」提示指向同一方向。**窗口 / decay / truncation / 宇宙 / 表达式一律逐字不动**
（选窗口换档会与中性化换档叠成两个自由度，违反规则 7）。

**候选 = 批 1 里 rns ≥ 0.40 的全部 5 条**（唯一"真信号"簇）：N3 `npAdmvdq`(0.65)、N4 `omoLREWm`(0.72)、
N7 `omoLREom`(0.40)、N8 `QPYbOvYG`(0.69)、N10 `qMExOLLZ`(0.71)。不含 N1/N2/N5/N6/N9（规则 5）。

**批 2 终判（写死）**：批 2 收批后若仍无 `S≥1.58 ∧ F≥1.0 ∧ 2Y≥1.58 ∧ SUB/|S|≥0.43` 候选 ⇒
该集**中性化轴已穷尽、3 字段无第二信号轴**，判弱 `USA-HIRING-TRENDS-WEAK` 并转下一集；
若出现全闸候选 ⇒ 立即 `check_correlation(refresh=True)`，prod ≥0.7 按 D0-P 直方图处置（`[0.7,0.8)` n≥1 ⇒ 族级封存）。

## 3. 回测结果

批 1 回测：`multisimulation_location=/simulations/iAPtz10A4q4akGEvzYTNzt`，收批 **10/10 COMPLETE，error 0**。
公开面设置：USA / TOP3000 / D1 / SUBINDUSTRY / decay 5 / truncation 0.08 / VERIFY / NaN ON / pasteurization ON / maxTrade OFF；
外层壳 `quantile(group_rank(winsorize(ts_backfill(<SIG>,22), std=4), subindustry))`。
金字塔：每条均为 `USA/D1/OTHER` 且 `MATCHES_PYRAMID: pass`（倍率栏 1.4，`get_datasets` 报 1.7 —— 平台两处口径不同，以回测行为准）。

| # | alpha | S | F | TO | ret | DD | 2Y | SUB | SUB/\|S\| | rns | 失败 RA |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| N1 | `9qEj8xjo` | 0.80 | 0.48 | 1.86% | 4.53% | 9.69% | 0.94 | 0.79 | 0.99 | **0.11** | S/F/2Y |
| N2 | `JjPNoeNx` | 0.09 | 0.02 | 1.90% | 0.35% | 6.09% | −0.25 | −0.09 | — | **−0.50** | S/F/SUB/2Y |
| N3 | `npAdmvdq` | 0.97 | 0.58 | 4.42% | 4.49% | 6.53% | 0.86 | 0.89 | 0.92 | 0.65 | S/F/2Y（UNITS warn） |
| N4 | `omoLREWm` | 1.02 | 0.61 | 8.16% | 4.44% | 6.51% | 0.86 | 0.82 | 0.80 | **0.72** | S/F/2Y |
| N5 | `88vjVRPa` | 0.75 | 0.40 | 7.15% | 3.51% | 9.24% | 0.57 | 0.57 | 0.76 | **−0.10** | S/F/2Y |
| N6 | `leMvEAKA` | 0.24 | 0.06 | 15.40% | 0.98% | 6.28% | −0.29 | 0.39 | — | **−0.66** | S/F/2Y（UNITS warn） |
| N7 | `omoLREom` | 0.96 | 0.55 | 11.57% | 4.06% | 6.71% | 0.95 | 0.94 | 0.98 | 0.40 | S/F/2Y（UNITS warn） |
| N8 | `QPYbOvYG` | 0.98 | 0.58 | 11.28% | 4.40% | 6.67% | 0.75 | 0.93 | 0.95 | 0.69 | S/F/2Y |
| N9 | `MP0adY0n` | 0.92 | 0.52 | 7.26% | 4.06% | 8.64% | 0.79 | 0.80 | 0.87 | **0.28** | S/F/**CW 0.496@2018-12-27**/2Y |
| N10 | `qMExOLLZ` | **1.04** | **0.64** | 6.86% | 4.67% | **4.66%** | **1.05** | **0.99** | 0.95 | **0.71** | S/F/2Y |

- 全员通过 `LOW_TURNOVER` / `HIGH_TURNOVER` / `LOW_SUB_UNIVERSE_SHARPE` / `MATCHES_PYRAMID`；N9 另挂 `CONCENTRATED_WEIGHT`
  （`0.496 @2018-12-27`，与 other359 的 `+1` 分母在稀薄日制造集中同一指纹 —— `trade_when` 的 else 腿把样本压到少数股票）。
- **无一过 S 线**（最高 1.04 vs 1.58），故规则 4 未触发，prod 配额未动。

**批 2（单一自由度：中性化 SUBINDUSTRY → INDUSTRY）**，`multisimulation_location=/simulations/3RRm6g5pn53F8E6CaERKHCd`，
`5/5 COMPLETE，error 0`，表达式逐字复用批 1：

| # | 批1 alpha | 批1 S | 批2 alpha | 批2 S | ΔS | 批1 F | 批2 F | 批1 TO | 批2 TO | 批1 ret | 批2 ret | 批1 DD | 批2 DD | 批1 2Y | 批2 2Y | 批1 SUB | 批2 SUB | 批1 rns | 批2 rns |
|---|---|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| N3 | `npAdmvdq` | 0.97 | `JjPNWglj` | 1.02 | +0.05 | 0.58 | 0.66 | 4.42% | 4.07% | 4.49% | 5.19% | 6.53% | 7.88% | 0.86 | **0.75** | 0.89 | 0.97 | 0.65 | 0.76 |
| N4 | `omoLREWm` | 1.02 | `zqr82PaO` | **1.06** | +0.04 | 0.61 | 0.68 | 8.16% | 7.45% | 4.44% | 5.16% | 6.51% | 7.93% | 0.86 | **0.72** | 0.82 | 0.90 | 0.72 | 0.83 |
| N7 | `omoLREom` | 0.96 | `QPYbN2ew` | 0.98 | +0.02 | 0.55 | 0.60 | 11.57% | 10.60% | 4.06% | 4.69% | 6.71% | 7.54% | 0.95 | **0.76** | 0.94 | 0.96 | 0.40 | 0.51 |
| N8 | `QPYbOvYG` | 0.98 | `j2eAP9Nj` | 0.98 | 0.00 | 0.58 | 0.61 | 11.28% | 10.25% | 4.40% | 4.90% | 6.67% | 8.02% | 0.75 | **0.63** | 0.93 | 0.95 | 0.69 | 0.75 |
| N10 | `qMExOLLZ` | 1.04 | `Vkdam2wV` | 1.03 | −0.01 | 0.64 | 0.66 | 6.86% | 6.28% | 4.67% | 5.14% | 4.66% | 5.84% | **1.05** | **0.87** | 0.99 | 0.99 | 0.71 | 0.78 |

批 2 五条全部通过 `LOW_TURNOVER` / `HIGH_TURNOVER` / `CONCENTRATED_WEIGHT` / `LOW_SUB_UNIVERSE_SHARPE` / `MATCHES_PYRAMID`；
仍全部挂在 `LOW_SHARPE` / `LOW_FITNESS` / `LOW_2Y_SHARPE`。**最高 S 1.06、最高 2Y 0.87、最高 F 0.68**。

## 4. 归因

**先读 rns 再看 SUB/2Y**（交付日志 §4 第 14 条），把 10 条切成两簇：

| 簇 | 成员 | rns | 读数 |
|---|---|---|---|
| **真信号** | N3 0.65 / N4 **0.72** / N7 0.40 / N8 0.69 / N10 **0.71** | ≥0.40 | 风险中性化后仍有独立信息；SUB/|S| 全部 0.80–0.98，2Y 0.75–1.05；DD 6.5–6.7%（N10 仅 4.66%） ⇒ 信号是真的，**只是强度差一档** |
| **风格 beta** | N1 0.11 / N2 −0.50 / N5 −0.10 / N6 −0.66 / N9 0.28 | <0.30 | SUB 数字好看（N1 0.99、N9 0.87）但 rns 塌掉 ⇒ 收益来自行业/市值/波动风格暴露，不是招聘信息。**按规则 5 不修 SUB/2Y** |

逐机制：

- **M1 招聘扩张（核心轴）：成立但弱。** 四种构造（原始水平 N1 0.80、相对 63 日前 N3 0.97、Δ63 的 z 分 N4 1.02、
  一年时序分位 N10 1.04）**单调收敛到 ~1.0**，且 rns 随构造"相对化程度"上升（0.11 → 0.65 → 0.72 → 0.71）。
  这直接印证论坛结论「招聘类要做相对化、不要用绝对水平」，也印证交付日志第 10 条（慢变量要 z 分 Δ 而不是 z 分水平）。
  **绝对水平构造（N1/N2）按规则 2 永久封存**：N2 反号后 S 0.09，说明不是方向错，是信息被规模效应淹没。
- **M2 过度扩张（反号）：证伪。** S 0.09 / rns −0.50。招聘扩张在 USA 不呈现资产增长异象，方向先验属 Belo-Lin-Bazdresch
  而非 Cooper-Gulen-Schill —— 两个文献在"招聘"这一量上对撞，**实证站在前者**（与 N1 正号一致）。
- **M3 招聘广度：证伪。** N5 S 0.75 / rns −0.10。`vec_count` 的变化在 rns 后消失 ⇒ 岗位条数更多反映发布渠道/格式，不是用工需求。
- **M4 周转率 `fresh/aggregate`：证伪。** N6 S 0.24 / rns −0.66 / TO 15.40%。日频流量噪声主导，方向也不稳。
- **M5 结构离散度：成立但弱。** N7 S 0.96 / rns 0.40（五条里最弱）。`vec_stddev/vec_avg` 相对化后仍有信息，但边际低于 M1。
- **M6 招聘加速：成立。** N8 S 0.98 / rns 0.69，`rolling_84d` 的 22 日增量（厂商已平滑的流量再做短期差分）效果与 M1 同档。
- **M7 事件门控：不成立。** N9 S 0.92 但 rns 0.28 + CW 0.496。`trade_when` 在稀疏数据上把持仓压进少数股票（与 other359 同指纹），
  **稀疏 VECTOR 数据集慎用 trade_when**，这条进可复用法则。
- **M8 时序分位：本批最强。** N10 S1.04 / F0.64 / DD 4.66% / 2Y 1.05，`ts_rank(level,252)` 优于 z 分（N4 1.02 但 DD 6.51%）
  ⇒ **慢变量的时序分位比 Δ 的 z 分更稳**（DD 降 29%），修正交付日志第 10 条：**Δ 的 z 分用于修 SUB，时序分位用于拿 DD**。

**F 的结构性约束（关键，决定批 2 的预期）**：本批全部 TO < 12.5% ⇒ `F = S × sqrt(returns / 0.125)`。
N10 实测 1.04×sqrt(0.0467/0.125)=0.64 ✓。因此 decay / winsor / 平滑**都不动 F**；要 F≥1.0，必须
`S=1.58 时 returns≥5.0%` 或 `S=1.3 时 returns≥7.4%`。批 1 的 returns 天花板 4.67% ⇒ **即使 S 修到 1.58，
F 仍会差 0.03–0.05**。这是本集的硬约束，批 2 必须同时把 S 与 returns 抬起来，单抬 S 不够（中性化换档理论上两者同抬：
保留行业共同成分 ⇒ 暴露更连续 ⇒ 收益与稳定性同升）。

**UNITS 警告（N3/N6/N7）**：`divide(vec_sum(fresh), add(vec_sum(aggregate),1))` 一类带 `+1` 的比值在 VERIFY 模式下报
无量纲常数加有单位字段（交付记忆 `brain-verify-units`）。属警告不属闸，但批 2 不再使用 `+1` 分母（CW 与 UNITS 同源）。

**批 2（INDUSTRY）的归因 —— 中性化不是 S 的杠杆，是"全期 ↔ 近期"的交换**

五条同向、幅度极一致，可当成一次受控实验读：

| 指标 | 5 条 Δ | 读数 |
|---|---|---|
| S | +0.05 / +0.04 / +0.02 / 0.00 / −0.01（均值 **+0.02**） | **几乎不动** ⇒ 中性化换档无法把 1.0 推到 1.58 |
| returns | +0.70 / +0.72 / +0.63 / +0.50 / +0.47 pp（均值 **+0.60pp**） | 全升 |
| rns | +0.11 / +0.11 / +0.11 / +0.06 / +0.07（均值 **+0.09**） | 全升 ⇒ 粗档中性化让信号更"纯" |
| F | +0.08 / +0.07 / +0.05 / +0.03 / +0.02（均值 +0.05） | 由 returns 带动，仍远低于 1.0 |
| **2Y** | −0.11 / −0.14 / −0.19 / −0.12 / −0.18（均值 **−0.15**） | **全降** |
| DD | +1.35 / +1.42 / +0.83 / +1.35 / +1.18 pp | 全升 |

**解释**：INDUSTRY 少剥一层行业共同成分 ⇒ 保留的是"行业招聘周期"这类缓慢轮动暴露，全期好看（returns↑、rns↑），
但 2022–2024 这段轮动方向反转 ⇒ 2Y 与 DD 同时恶化。SUBINDUSTRY 留下的是公司特异招聘变化，全期稍弱但近两年更稳。
**可复用法则（新）**：**当 2Y 是短板时，中性化往粗档调会「抬 S / 抬 returns / 抬 rns / 压 2Y / 加 DD」——
它是用近期换全期，不是修 2Y 的杠杆**。本集 2Y 是第二短板（最高 1.05 vs 线 1.58），故粗档方向从一开始就不对；
但批 2 是预注册的唯一单自由度，只能实测确认，不能纸上跳过。

**为什么整集封存（而不是继续修）**：三字段数据集已把可陈述的机制轴全部走完 —— 水平（N1/N2，规则 2 封）、
相对变化（N3/N4）、广度（N5）、周转（N6）、离散（N7）、加速（N8）、事件门控（N9，CW）、时序分位（N10）。
批 2 证明设置轴也到顶（中性化两档差异 ≤0.05 S）。**剩余可调项只有窗口（84d/63d/22d 已各用过）与 decay，属磨参数**，
按 USA 纪律（禁止同族磨参数）不再消耗仿真。

## 5. 决策

**判弱 `USA-HIRING-TRENDS-WEAK`（批 2 终判，按 §2.6 预注册执行）**。

**规则对账（终局）**

| 规则 | 终局判定 |
|---|---|
| 1 数据集级 max\|S\|<1.0 | 不触发（批 1 1.04 / 批 2 **1.06**），但**未达 1.58 过闸线** |
| 2 机制级 | 触发于 N1/N2 原始水平对（0.80/0.09）⇒ 该构造永久封存 |
| 3 核心轴 | 不触发（N4 批 1 1.02、批 2 1.06）⇒ M1 是**真信号但封顶 ~1.06** |
| 4 过闸即测 prod | 全程未触发 ⇒ **prod 配额 0 消耗**，本集未占用任何相关性槽 |
| 5 风格 beta | 批 1 封 5 条（N1/N2/N5/N6/N9）；批 2 后 rns 全部 ≥0.51 ⇒ 优选簇确为真信号 |
| 6 频率 | 不触发（TO 4.07%–10.60%） |
| 7 批次上限 | **已达上限（10 + 5）**，2 个自由度（中性化两档）均已测 |
| 8 覆盖 | 遵守：仅 `ts_backfill(...,22)`，零 `group_backfill` |

**证据链**：`hiring_trends` 的招聘信息在 USA **真实存在且非风格 beta**（rns 0.51–0.83、SUB/|S| 0.90–0.99、
DD 5.8–8.0%、TO 4–11%、`MATCHES_PYRAMID pass`），但**幅度天花板 ~1.06 S / ~0.68 F / ~1.05 2Y**，
三项都约为过闸线的 2/3。这不是构造错误（8 个机制方向已穷尽、两档中性化同向），是**该数据源的截面信息强度不足**。
F 侧另有结构性约束：TO<12.5% 时 `F=S·√(returns/0.125)`，returns 天花板 5.19% ⇒ S 要 1.55 才够 F=1.0。

**处置**：不写 DB `dead_end`（`seal_dead_end` 的论坛取证闸 fail-closed，本会话论坛检索虽已跑通，
但该集未做 `forum_recon` 记录；不绕过闸、不 `force_seal`）。仅在档案与交付日志登记 `USA-HIRING-TRENDS-WEAK`，
供 `campaign_intel`/排期按「已判弱」处理。

**可复用法则（3 条，已回写交付日志）**
1. **中性化粗档 = 近期换全期**（见 §4 表）：2Y 短板时不要往 INDUSTRY 调。
2. **招聘类必须相对化**：绝对水平 N1 S0.80/rns0.11 vs 相对变化 N4 S1.02/rns0.72 —— 论坛结论在 USA 复现。
3. **稀疏 VECTOR 上 `trade_when` + `+1` 分母 = 双料 CW 制造机**（N9 0.496；other359 同指纹）。

**下一集**：`other384`（财报电话会披露结构轴，66 字段、cov 0.82、结构类 aC 0–2），
预注册见 [`_usa-other384-field-profile-20261021.md`](_usa-other384-field-profile-20261021.md) §2。
