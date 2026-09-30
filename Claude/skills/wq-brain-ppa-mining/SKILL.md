---
last_verified: 2026-09-29
name: wq-brain-ppa-mining
description: "开 PPA（Power Pool Alpha）战役、或要判断某个数据集在目标区域能不能打 PPA 时使用：S0 体检的 PPA 方法论（三条硬门槛与拥挤度口径）、数据集 / 字段体检指标 → 预处理的决策映射、白空间取数路径。RA 常规战役的白名单排序走 ra-pipeline 决策表 D4，不走本 skill；不编排、不提交。"
layer: L0
allowed-tools:
  - Read
  - Bash
  - mcp__wq-brain-http__*
---

# PPA 挖掘方法论（WebDataScope 增强版）

## 职责边界

- **本 skill 负责**：PPA 战役的 S0 体检方法论（三条硬门槛、拥挤度口径、区域-类型亲和判据）；数据集 / 字段体检指标 → 预处理算子的决策映射；白空间与算子多样性的**取数路径**。
- **本 skill 不做**：不编排（PPA 走 ra-pipeline 的 PPA 分支，见其 [`ppa-vs-ra.md`](../wq-brain-ra-pipeline/references/ppa-vs-ra.md)）；不出配置包；**不提交**——合法 PPA 只能由用户在平台 web UI 提交；**主题匹配核查也不在本 skill**（挖矿期 = ra-pipeline 步 1 §1.6 与 ppa-vs-ra §1，提交期 = `worldquant-submit-alpha` 的 PPA 通道）；不抄 registry 里的判死清单（registry 才是事实源，见 §4）。
- **上游 / 下游**：上游 = 平台 Power Pool 公告 + WebDataScope 离线包 + 本地 DB；下游 = S0 打分（`workflow_campaign(stage="S0")`，白名单落 ledger `s0_whitelist`）与 S1 字段语义。

## 1. 适用域：PPA 与 RA 的 S0 差异（先读这个）

本 skill 的**硬门槛与一票否决只适用于 PPA 模式**（`thresholds.json` 的 `dataset_health.mode = "ppa"`）。RA / general 战役的白名单排序以 ra-pipeline 决策表 **D4** 为准。

| 项 | PPA（`mode="ppa"`） | RA（`mode="general"`，现在所有区域的配置） |
|---|---|---|
| alphaCount | ≤ `alpha_count_max`（方法论建议 50）**硬闸**；tier1 中超标者降 tier2 | 只进 score 软罚 |
| coverage / fieldCount | tier1：`coverage_min`（建议 0.85）、`field_count_min`（建议 10）；硬地板 `coverage_hard_min` | 同一组键，区域各自配（例：KOR `coverage_min` 0.8、ASI / CHN / HKG 0.85） |
| 排序 | `pyramidMultiplier` 降序 → `alphaCount` 升序 → `coverage` 降序（求点塔倍率） | D4：**先按金字塔配给**（每波 ≥ 2 槽非 MODEL）再 score 降序；**禁止**按 `pyramidMultiplier` 降序（会把 PV 等整座金字塔挤出白名单） |
| 执行器（**唯一**） | `workflow_campaign(region, stage="S0")` + `python tools/campaign_intel.py s0-select …`（RA 步 2） | 同 |

- **PPA 阈值的真实位置** = 各区 `tracking/<R>/config/thresholds.json` 的 `dataset_health`；开 PPA 战役前把该区 `mode` 改 `"ppa"` 并核对上面三个键。代码缺省值（`score_datasets.py`）：`coverage_hard_min` 0.7、`field_count_hard_min` 5、`tier2_coverage_min` 0.85、`tier2_field_count_min` 5、`tier2_alpha_count_max` 200、`tier1_score_pct` 0.6、`tier2_score_pct` 0.3、PPA 分位路径的 `alpha_count_max` 50（`tests/unit/07_docs_skills/test_se_docs.py` 逐项对照源码）。
- 旧脚本 `scripts/dataset_health_check.py`（自读 `.env` 直连的第三个执行器）**已归档**到 `attic/ppa_mining_20260929/`：零调用方，且已被 `s0-select` + S0 打分取代。
- **「最优拥挤度」有三个不同口径，别混**：

| 口径 | 轴 | 区间 | 出处 |
|---|---|---|---|
| PPA 硬闸 | 平台实时 `alphaCount`（`get_datasets`） | ≤ 50 | `score_datasets.py`（`mode=ppa`） |
| 离线甜点区 | 数据包里社区提交量 `count`（2026-02 快照） | 100 ≤ count ≤ 3000 且 sharpe ≥ 1.1 × 区域均值 | `tools/webdata_quality.py --recommend` |
| 校准甜区（opt-in） | 平台 `alphaCount` | 50–1000（`crowd_sweet_spot_enable`） | toolkit `--calibrate`（EUR + GBR 实证） |

## 2. 体检怎么做（agent 取数路径）

| 要看什么 | 命令 / 工具 | 说明 |
|---|---|---|
| 数据集级体检（coverage / fieldCount / userCount / alphaCount / valueScore / pyramidMultiplier） | `mcp__wq-brain-http__get_datasets` | 一次返回，比拉字段再聚合快两个数量级 |
| 选集增强（真实点塔 × 历史产出率 × 判死） | `python tools/campaign_intel.py s0-select --region <R> --delay <D> --universe <U>` | 输出标记含义见 ra-pipeline `step2-s0.md` §2.2 |
| 字段级下钻 | `get_datafields(dataset_id=…, region, delay, universe)`；离线：`python tools/webdata_quality.py --zip research-data/WebData_20260219_V0.10.9 --region <R> --delay <D> --fields <ds>` | 见 §5 |
| 面板对应关系 | 扩展的「徽章」/「hover 卡片」/「白空间表」 | 这是 Chrome 扩展的 UI，agent 不能操作；等价的离线数据由上一行 `webdata_quality.py` 读取。UI 只作人工核对备注 |

## 3. 三条硬门槛（PPA）与「零竞争」

| 指标 | PPA 门槛 | 理由 |
|---|---|---|
| `coverage` | ≥ 0.85（一票否决线 < 0.7） | < 0.7 = 三成以上标的无数据，turnover 虚高、`CONCENTRATED_WEIGHT` 几乎必然触发 |
| `alphaCount` | ≤ 50（一票否决线 > 1000） | 拥挤数据集的 prod_corr 天然逼近 0.7 上限 |
| `fieldCount` | ≥ 10 | 字段太少无法构建 spread / 条件腿 |

- **`alphaCount == 0` 不是「优先级最高」**：toolkit `probe-scoring-v2` 已用 EUR + GBR 实测证伪「零竞争 = 高价值」（`ac < 50` 几乎全是伪白空间）。做法：满足三门槛的集里，ac = 0 者只做**探针（最小批）**，且要求 `coverage ≥ 0.9`、字段 ≥ 10、字段语义合规——不预设它高价值。
- **案例（2026-08-05 EUR）**：32 次回测全耗在 model30（cov 0.713 但 alphaCount 4202）、pv20（cov 0.69）、news21（cov 0.53）、insiders12（cov 0.20）上，零候选；而同期有 19 个 cov ≥ 0.85 且 alphaCount ≤ 50 的集从未被触碰。反事实「若前置体检可完全避免」**后来的验证结果是：ac = 0 的集多为伪白空间**，所以「前置体检」只避免了选错，不保证选对——体检是必要条件，不是充分条件。

## 4. 区域-类型亲和：红 / 黄 / 绿（判据 + 查询，不抄快照）

**事实源是 registry，不是本文**：`mcp__wqb-db__get_dead_ends(region)`、`mcp__wqb-db__get_campaigns(region)`、`get_cross_region_lessons()`。判据：

| 维度 | 红灯（大概率无信号） | 黄灯（需验证） | 绿灯 |
|---|---|---|---|
| 同区域同类判死 | ≥ 3 条 | 1–2 条 | 有 WIN 记录 |
| 数据密度 | 事件类 / 稀疏类（日频事件 < 50 条 / 日） | 日频聚合类 | 连续截面类（基本面 / 价格衍生） |

- 红灯集排到最低优先级，只在白名单无其它候选时才考虑，且只用 8 探针最小批验证；黄灯集入白名单但标风险项（如「需先验 CW」）；绿灯集优先排入 tier1。
- **跨区外推只按 ra-pipeline 的跨区先验规则**（≥ 2 区独立复现的死族才排除；「同集在别区 ≥ 16 条回测且 max\|S\| < 1.0」只降权）；**单区判死不外推到其它区**——旧文里「GLB emotion 判死 → 全区红灯」这类外推已删。

## 5. 数据集 / 字段级决策

### 5.1 数据集级

- **甜点与徽章**：`--recommend` 的甜点区见 §1 表；OS / IS 徽章颜色 = `sr < 0` 红、`sr` > 区域均值绿、其余黄、缺失灰。优先绿色。
- **OS 退化**：`IS sharpe − OS sharpe > 0.15` 判退化（与 `webdata_quality` 的 `degraded` 标记、field-quality 同阈值）→ 慎用 / 降权。
- **中性化**：读该数据集自己的 dominant method 作首选，**不要无脑 SUBINDUSTRY**；但 **SECTOR / MARKET 大幅压低 `IS_LADDER_SHARPE`**（决策表 D5 禁用）——只有 dominant method 实测更优**且** IS_LADDER 仍达标时才采用。KOR 的 SECTOR 最佳（0.562）是 2026-08 的离线实证，用前先复核。
- **离线包可用性 ★★★ / ☆☆☆ 只说明本地有没有快照，不等于平台可用**：★★★ = 精确匹配 `${dataset}_${region}_${universe}_Delay${delay}.bin`，只影响本地分析质量。**反例（2026-08-05 EUR）**：离线榜推荐的 `fundamental86 / risk59 / model216 / fundamental94` 在 EUR 平台查不到字段，被误判成「数据包过期」；实际是这四个集**EUR 根本不提供**（不是 0 字段），在 KOR 全部可用。规则：离线推荐的集必须先用 §2 的体检确认它在**目标区域存在且达标**；判「不可用」前先换区查一遍，排除跨区误推荐。

### 5.2 字段级：体检指标 → 预处理（阈值与体检硬门同源）

下表的数值就是 `tools/webdata_quality.py::check_expr_against_inspect`（`field_inspect_gate.py` 内置，RA 步 5 的 `wave_gate` 自动执行）的**硬性检查**，违反 → 波闸 FAIL：

| 体检指标 | 阈值 | 表达式必须 | 依据 |
|---|---|---|---|
| `CoverageRatio` | < 0.4 | 含 `ts_backfill` 或 `group_backfill`（缺 → 必然 `CONCENTRATED_WEIGHT`）；< 0.3 更宜换字段 | 硬检查 1 |
| `skewness` | \|skew\| > 2 | 含 `rank` / `winsorize` / `signed_power`（有界字段跳过 `winsorize`） | 硬检查 2 |
| `kurtosis` | > 8 | 含 `rank` 或 `winsorize` | 硬检查 3 |
| 指示值单边（恒正 / 恒负） | 单边占比高 | 含 `ts_delta` / `rank` / `bucket` 之一，不能直接用原始水平做多空 | 硬检查 4 |
| `yearly_distribution` 形态 | `zero_inflated` / `point_mass` | 用 `trade_when` 门控（稀疏事件）；`spread`（近似正态）才适合 `zscore` / `ts_zscore` | 硬检查 5 |
| `frequency` | daily / weekly / monthly / quarterly | 窗口算子窗口 ≥ 22 / 52 / 120 / 252（流量 / 事件类 daily 字段降到 5） | 硬检查 6 |
| `IntegerStatus` | 整数（计数类） | 用 `rank` / `group_rank` / `bucket`，**不用 `ts_mean` 平滑**（抹掉离散信息） | 决策表 D5 |
| `absValueBetween1and0ratio` | > 60% | 已压缩 / 有界，可直接用或 `rank`，跳过 `winsorize` | 决策表 D5 |

（旧文里的 `is_placeholder` **不是 BRAIN 算子**，会被幽灵算子闸拦下，已删；缺失字段一律「`ts_backfill` 或换字段」。）

## 6. 组合形态：返回反转不作加法项

旧文的「V9 突破版」是 `scale(rank(A)) + scale(-rank(ts_zscore(returns, 42))) * 0.35`——**带权重的两信号相加**，违反 ra-pipeline「路线 A」与 CLAUDE.md「禁止混信号调参」（同源价差 `subtract` 才是允许形态，见 ra-pipeline 步 7 §7.7）。**已删除作配方**；它在历史上的 S = 2.23 是加权混合的产物，不代表可复用。合规改写：把 returns 反转当**条件**或**分组**，而不是加法项：

```
trade_when(ts_zscore(returns, 22) < 0, rank(ts_zscore(subtract(ts_mean(ts_backfill(field_B, 66), 22), ts_mean(ts_backfill(field_A, 66), 22)), 252)), -1)
```

- `subtract(A, B)` 两腿须**同源**（同数据集、有单一经济含义）；`subtract(..., filter=true)` 可用，`divide` 没有 `filter`；`ts_regression(A, B, n).residual` 语法无效。
- 窗口用标准窗口（22 / 66 / 252……）；旧文的 189、42 没有依据，已换。
- `hump` **仍受支持但必须命名参数**：`hump(x, hump=k)`（决策表 D6；旧文「hump 破坏组合信号、勿用」已由实测取代——预闸会把位置参数形态自动改写）。

## 7. 参数与设置

- **并发不在这里定**：见 `wqb-concurrency`（`config.CONCURRENCY`）；旧文的「C = 5」已删（config 里 slots = 7）。
- delay：以 `config.REGIONS[<R>]["delays"]` 为准（D0 数据只有部分区域有，其余用 D1）；universe：`get_platform_setting_options` 与 `config.REGIONS[<R>]["universes"]`，**不凭记忆**——非法档位报 HTTP 500 而不是 400。
- decay / truncation：**缺省**才用 returns 信号 4、close 信号 6、truncation 0.08；有库存实测时以 settings prior 为准（决策表 D5）。**参数只在有依据的少数维度内扫**，并记录取值理由；**不扫权重**、不补参数变体凑数。
- testPeriod：「无测试期」写 `P0Y0M0D`（示例里的 `P0D` 是简写，平台接受的规范写法用前者）；`P6Y` 是真实的 6 年测试期，也是平台允许的最大值（`P6Y0M0D`）——是两回事。

## 8. 闸门线（口径 = `src/wqb/config.py`）

| 层 | 内容 | 来源 |
|---|---|---|
| 平台线 | Sharpe ≥ 1.58、Fitness ≥ 1.0、turnover ∈ [1%, 70%]、self_corr < 0.7、prod_corr < 0.7；另有 LOW_SHARPE（D1 1.25 / D0 2.0）等检查线 | `config.GATES_PLATFORM` / `PLATFORM_CHECK_LINES` |
| 内部严线（研究阶段省配额） | turnover ∈ [5%, 20%]、margin ≥ 10bp、returns ≥ 5%、self_corr < 0.5 | `config.GATES_INTERNAL` |
| PPA 附加 | Sharpe ≥ 1.0（低于 RA）、算子 ≤ 8、字段 ≤ 3、**PPAC**（Power Pool 相关性）< 0.5 | ppa-vs-ra.md（平台文档记载，**未向平台复核**） |

旧文把「Margin > 5bp、Returns > 5%」写成平台硬线——`GATES_PLATFORM` 没有这两项，5bp 既不是平台线也不是内部线，已删。本地快算 PPAC：`brain-calculate-alpha-selfcorr-quick`。

## 9. 流程（PPA 战役）

0. **S0 体检**：§2 的 `s0-select` + S0 打分 → 过 §3 三门槛 → 候选白名单。**之后的步骤只在这份白名单内做**；白名单为空才考虑换区 / 换 universe。
1. **数据集扫描**：§5.1（徽章 / 中性化 / OS 退化）。
2. **白空间**：`non_data` 表只作**候选池来源**，必须再过 §3 体检与 §4 跨区先验，不当结论（旧文把 KOR 的 Sentiment / Option / Macro 空白列为「重点机会」，同区又把新闻 / 情绪族列为三连判死——二者不矛盾的读法是：空白只说明没人试，不说明能出货）。`non_data_delay0` 零提交 ≠ 机会（多为该区 D0 无数据）。
3. **字段探测**：§5.2。
4. **信号构建**：单信号或同源价差；辅助腿入场三式（条件 / 分组 / 残差）见 ra-pipeline 步 7 §7.7；§6。
5. **调参**：§7，只在有依据的少数维度。
6. **算子多样性**：Genius 的 operatorCount 等维度是**指标补齐**，与「表达式质量」分开——为凑指标去用 `ts_regression` 之类罕见算子必须先过闸 5 与语法闸；不为凑数改写已过闸的表达式。
7. **闸门**：§8 廉价闸 → PC 等待 → 硬闸。
8. **交接**：PPA **由用户在 web UI 提交**，agent 只产出候选清单 + 主题匹配证据 + 交接单（`python tools/ppa_handoff.py sheet --alpha-id <ID> [--ppac <值>]`；用户提交后 `record --alpha-id <ID>` 落账）。`tags=["PowerPoolSelected"]` + `color` 的 MCP 提交在本环境**会被拦**（非 PPA 感知），不要教也不要试。

## 10. 选区与快照

- 选区前对 2–3 个候选区各跑一次 §2 的体检 + `get_mining_yield` + 跨区先验，再比 `pyramidMultiplier` / `valueScore`（同一集在不同区倍率可差 20%+）——**以实时数据为准，不凭习惯选区**。
- 2026-08 的区域快照（KOR / EUR / HKG 数据集数、倍率差表、「首选 news_sentiment_nlp」等）已移到 [references/region-snapshots-2026-08.md](references/region-snapshots-2026-08.md)，**带日期与失效条件，不是行动指令**——此后的证据是反向的（新闻 / 情绪在 USA / EUR / IND 同型全灭、KOR 新闻三连死、ac = 0 多为伪白空间）。

## 11. API 实测约束（症状 → 原因 → 处置）

| 症状 | 原因 | 处置 |
|---|---|---|
| 数据集级体检拉了一万个字段再聚合，很慢 | 该走 `get_datasets` | 直接用 `get_datasets`（返回 coverage / fieldCount / userCount / alphaCount / valueScore / pyramidMultiplier） |
| `GET /data-fields` → 400 Invalid query | 只给了 `dataset.id`，缺 `universe` | 四参齐全：`instrumentType + region + delay + universe`（`dataset.id` 参数是存在的） |
| `universe` 传该区非法档位 → **HTTP 500**（不是 400），无提示，像服务故障 | 档位非法 | 用 `get_platform_setting_options` 与 `config.REGIONS[<R>]["universes"]` 核对，不凭记忆（旧文里的档位表已过期，已删） |
| 直连 REST 的 `category` 是 dict，MCP 已扁平成 str | 通道差异 | 跨通道处理前归一化 |
| Python 直连 `api.worldquantbrain.com` 间歇 TLS 中断（`SSL: UNEXPECTED_EOF_WHILE_READING`，也可能被报成 `ProxyError` / `RemoteDisconnected`） | 沙箱链路抖动 | **优先复用常驻 MCP 服务的会话**；必须直连时按 wqb-concurrency 的退避规则处理；不自己手写 requests / `_reauth()`，用 `BrainApiClient` |
| 独立脚本高频拉取触发 429 | 与常驻 MCP 共享配额 | 带退避，批量取数 |

MCP 工具与 workflow 节点的**计数**一律见 [`INDEX.md`](../INDEX.md)「MCP 工具/节点计数基准段」，本文不裸写数字。
