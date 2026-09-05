---
last_verified: 2026-08-22
name: wq-brain-ppa-mining
description: "WorldQuant Brain 平台未点亮金字塔数据集 PPA (Power Pool Alpha) 挖掘的完整工作流。以「平台实时体检硬门槛」(coverage≥0.85 / alphaCount≤50 / fieldCount≥10) 为开战役前置条件，整合 WebDataScope 数据集级/字段级 meta-analysis，把“凭经验猜参数”升级为“读数据定参数”，覆盖数据集选择、中性化选择、字段预处理、时间窗口选择、低竞争白空间发现与闸门检查。触发场景：用户提到 WQ Brain、WorldQuant、PPA、Power Pool Alpha、alpha 挖掘、未点亮数据集; 用户要求在 WQ Brain 平台上找可提交的 alpha; 用户问\"怎么选数据集/字段/中性化/时间窗口\"或\"哪些数据集竞争少\"; 用户要开新战役 / 换区域 / 问某数据集能不能打 → 必须先执行 §1.0 平台实时体检; 出现\"某数据集平台没数据/字段为 0/数据包过期\"的判断 → 先按 §1.3 排除跨区域误推荐"
layer: L0
allowed-tools:
  - Read
  - Bash
  - mcp__wq-brain-http__*
---







# WQ Brain PPA Alpha 挖掘方法论 (WebDataScope 增强版)

## 0. 总纲：数据驱动，而非经验驱动

WebDataScope 是 Chrome 扩展，对 WQ 平台数据做 **字段级 + 数据集级 meta-analysis**：
- 数据来源：IndexedDB 中的 `.bin` 文件（msgpack + pako 压缩），内容为平台 `activities/diversity` 与 dataset stats。
- 三个核心面板：
  - **dataAna.js**（字段级 hover 卡片，10 个指标）→ 决定单字段的预处理算子。
  - **dataFlag.js**（数据集列表徽章：OS/IS Sharpe、中性化、数据包可用性）→ 决定选哪个数据集、用哪种中性化、覆盖是否完整。
  - **distribution.js**（region × dataCategory 散点 + `non_data` 白空间表）→ 决定去哪个空白区挖低竞争 alpha。

**核心原则**：凡能由 WebDataScope 读出的参数（中性化方法、时间窗口、是否 winsorize/rank、覆盖完整性），一律**读取**，不要硬编码猜测。

## 衔接协议

- **上游**：S-PRE `wq-brain-campaign-matrix`（预解析配置包：region/universe/意图/delay/中性化）或用户直给区域参数。
- **本 skill 角色**：S0 健康检查方法论层——§1.0 平台实时体检硬门槛（cov≥0.85 / alphaCount≤50 / fields≥10）在 mode=ppa 下一票否决，general/REGULAR 战役降级为 tier 评分软罚；数据集/字段级参数决策（§1–§4）供 S1/S2 读取。
- **输出**：数据集白名单（仅 tier1）——编排器 `wq-brain-ra-pipeline` 步 2 执行健康检查后经 `mcp__wqb-db__upsert_ledger_key(region, "s0_whitelist", {...})` 回写 ledger_kv（结构化真相源）；字段级预处理建议由 S1 `brain-data-feature-engineering` 综合后经 `s1_<dataset>_d<delay>` 键入库。
- **下游**：S1 `brain-data-feature-engineering`（白名单内逐数据集，启动前读 `s0_whitelist` 校验）；数据集 dead 标记经 `wq-brain-campaign-toolkit` `score_datasets.py` 的 `make_ledger_store` 直写 `*_dead` 键，反哺本 skill 下一轮体检。

## 1. 数据集级决策（dataFlag.js → info_data.bin）

### 1.0 ★ 前置硬门槛：开战役前必须先做平台实时体检 ★

**这是 §1 其余所有步骤的前置条件。跳过此步 = 大概率浪费整轮回测配额。**

WebDataScope 读的是**离线数据包**，反映的是快照时刻的历史统计；而某数据集在**你的目标 region/universe/delay 下当前是否值得打**，必须以平台实时数据为准。二者不可互相替代。

运行体检工具（零第三方依赖，仅标准库，双通道）：

脚本随本 skill 分发于 `scripts/dataset_health_check.py`。
工作区自动探测：`WQB_WORKSPACE` 环境变量 > 向上查找含 `world-quant-brain-mcp/` 或 `tracking/` 的目录 > 脚本上级目录。

```bash
SK=~/.qoder-cn/skills/wq-brain-ppa-mining/scripts/dataset_health_check.py

# 数据集级体检（首选，秒级返回）
python "$SK" --region EUR --delay 1 --universe TOP1200

# 字段级下钻（确认某数据集的字段覆盖分布）
python "$SK" --region EUR --universe TOP1200 --dataset-fields ml_factor_proj

# MCP 服务未运行时走直连兜底（自带 429/5xx 指数退避）
python "$SK" --region KOR --universe TOP600 --mode direct

# 调整门槛
python "$SK" --region HKG --universe TOP800 --min-cov 0.9 --max-alphas 20 --top 30
```

**双通道**：默认 `--mode mcp`，复用常驻 world-quant-brain-mcp 服务（`127.0.0.1:8876`）已建立的稳定会话，规避沙箱到 `api.worldquantbrain.com` 的 TLS 抖动；`--mode direct` 用 `.env` 凭据自行 Basic Auth 直连兜底。
结果落盘 `tracking/mining/field_coverage_<REGION>_d<D>_<UNIVERSE>.json`，含 `stats` / `focus_check` / `opportunities` / `all_datasets`。

**三条硬门槛（全部满足才允许消耗回测配额）：**

| 指标 | 门槛 | 理由 |
|---|---|---|
| `coverage` | **≥ 0.85** | < 0.7 意味着三成以上标的无数据，turnover 虚高、CONCENTRATED_WEIGHT 几乎必然触发 |
| `alphaCount` | **≤ 50** | 拥挤数据集的 prod_corr 天然逼近 0.7 上限，sharpe 再高也过不了闸门 |
| `fieldCount` | **≥ 10** | 字段太少无法构建 spread / 组合信号 |

**一票否决**：`coverage < 0.7` 或 `alphaCount > 1000` 的数据集直接排除，不做任何回测。

排序优先级：`pyramidMultiplier` 降序 → `alphaCount` 升序 → `coverage` 降序。
`alphaCount == 0` 的数据集是零竞争白空间，优先级最高。

**血的教训（2026-08-05 EUR 战役）**：32 次回测全部消耗在 model30（cov 0.713 但 **alphaCount 4202**）、pv20（cov 0.69 / 倍率仅 1.1）、news21（**cov 0.53**）、insiders12（**cov 0.20**）四个数据集上，无一满足门槛，sharpe 天花板 0.72，零候选。而同期该区域有 **19 个** cov≥0.85 且 alphaCount≤50 的数据集从未被触碰，其中 7 个 alphaCount=0。**失败的是选择，不是区域。** 若此门槛前置执行，那 32 次回测可完全避免。

### 1.0.x 区域-类型亲和矩阵（白空间质量预判，2026-08-23 实证提炼）

**目的**：在平台体检通过后、投入回测配额前，根据台账中同区域同类数据集的死/活记录，对候选数据集给出信号概率预估。47 条死路中 22 条（47%）是白空间无信号——此规则旨在把这批数据集排到最低优先级，避免浪费首批配额。

**规则引擎**（从台账自动推导，无需硬编码）：查询 `mcp__wqb-db__get_dead_ends(region)` 和 `mcp__wqb-db__get_campaigns(region)`，按以下维度匹配：

| 匹配维度 | 红灯（大概率无信号） | 黄灯（需验证） | 绿灯（已验证有效） |
|---|---|---|---|
| 数据类型 | 同区域 3+ 同类判死 | 同区域 1-2 同类判死 | 同区域有 WIN 记录 |
| 数据密度 | 事件类/稀疏类（日频事件<50条/日） | 日频聚合类 | 连续截面类（基本面/价格衍生） |
| 区域特征 | KOR: 图表形态/新闻/AI/ML/信用风险 | KOR: 事件类需先验 CW | KOR: 分析师预期变化 |
| | MEA: 慢变基本面/value/quality | MEA: VECTOR 需先验 longCount | MEA: 分析师预期变化 |
| 跨区信号 | GLB emotion 判死 → 全区 emotion 红灯 | — | — |

**执行规则**：
1. 红灯数据集：排到最低优先级，仅在白名单中无其他候选时才考虑，且必须用 8 探针最小批快速验证（而非 10 表达式全批）。
2. 黄灯数据集：可入白名单，但标注风险项（如"需先验 CW"/"需先验 longCount"），在 S1 字段理解时优先处理这些风险项。
3. 绿灯数据集：优先排入白名单 tier1。

**当前已知的红灯规则（KOR 实证，2026-08-23）**：
- 图表形态族：chart_cnn_alpha / continuation_score / pattern_scores 三连判死，天花板 0.49
- 新闻/情绪族：news79 / equity_forum_data / news_sentiment_transfer 三连判死，天花板 0.76
- AI/ML 因子库：ai_factor_transfer / ai_equity_alpha / ml_factor_proj 三连判死，天花板 0.86
- 信用风险：quant_factor_lib / model313 双判死
- 行为金融/论坛：behavioral_signals / equity_forum_data 全灭
- 跨区：GLB emotion 42 候选全被 PROD 0.82-0.86 挡掉 → 任何区域 emotion 族红灯

### 1.1 OS/IS Sharpe 徽章（选数据集）
- 颜色规则：`sr < 0` 红、`sr > 均值` 绿、否则黄、缺失灰；显示 `sharpe(count)`。
- **决策**：优先选**绿色**（sharpe 显著高于同区域均值）的数据集；红色/灰色谨慎。
- 结合离线工具 `tools/webdata_quality.py --zip WebData_*.zip --region KOR --delay 1 --recommend` 可批量算出 sweet-spot 数据集（100 ≤ count ≤ 3000 且 sharpe ≥ 1.1×均值）。

### 1.2 中性化徽章（定中性化，**不要全局硬编码**）
- 显示该数据集的 **dominant neutralization method** `key(pct%)`，hover 表给出每种方法的 count / percentage / sharpe。
- **决策**：读该数据集自己的 dominant method 作为首选中性化；不要无脑 SUBINDUSTRY。
- 实证（2026-08-05）：**KOR → SECTOR 最佳（0.562）**；USA 多数场景 SUBINDUSTRY 仍优。SECTOR/MARKET 会大幅压低 IS_LADDER_SHARPE，仅在数据/区域需要时采用。

### 1.3 数据包可用性 ★★★ / ☆☆☆（⚠ 仅指离线包，**不等于**平台覆盖率）
- `★★★` = 精确匹配 `${dataset}_${region}_${universe}_Delay${delay}.bin`（本地离线包覆盖完整）。
- `☆☆☆` = 仅 partial universe 匹配（本地离线包可能不全）。
- **决策**：优先选与你的 (region, universe, delay) 配置完全匹配的 `★★★` 数据集。

**⚠ 严禁用离线包状态推断平台数据可用性。** 这两者是独立维度：
- 离线包缺 → 只是本地没快照，平台上该数据集可能好端端地存在且满覆盖。
- 离线包有 → 平台上该数据集也可能在当前 region 根本不提供。

**反例（2026-08-05 EUR）**：因离线包推荐榜里的 `fundamental86 / risk59 / model216 / fundamental94` 在平台查不到字段，误判为"数据包过期、平台 0 字段、等更新后重探"。实测真相是**这四个数据集 EUR 区域根本不提供**（不是 0 字段，是不存在），而它们在 **KOR 全部可用**（`fundamental94` 有 215 字段、cov 0.8558）。这是**跨区域误推荐**，与数据包新鲜度毫无关系，等待更新是纯粹的时间浪费。

**规则**：离线包推荐的数据集，必须先用 §1.0 体检确认它在目标区域**存在且达标**，再进入后续步骤。判定"某数据集不可用"之前，先换个区域查一遍，排除跨区误推荐。

### 1.4 OS 退化检测
- 若 `IS sharpe >> OS sharpe` → 该数据集过拟合/信号衰减，慎用或降权（参考 webdata_quality 的 `--cross-region` / OS 退化标记，如 KOR `model253` 被标退化）。

## 2. 字段级决策（dataAna.js → 10 指标 → 算子映射）

对每个候选字段，读其 hover 卡片的 10 个指标，按表定预处理：

| 指标 | 含义 | 决策（alpha 表达式如何写） |
|------|------|---------------------------|
| `frequency` | 更新频率 | **时间窗口选择**：季/年频（fundamental/earnings）→ 长 `ts_mean`(60/120) 且 `ts_backfill` > 更新间隔防断点；日频 → 短窗口(20-40) |
| `Coverage` / `CoverageRatio` | 非空比例 | 低 → `ts_backfill(66/120)` 填洞；极低(<30%) → 加 `is_placeholder` 或换字段 |
| `IndicativePositiveRatio` / `IndicativeNegativeRatio` | 指示值正负占比 | 强单边（如 >80% 同号）→ 符号含信息，用 `rank(signed value)` 或 `subtract` 两个同构字段取差 |
| `absValueBetween1and0ratio` | 取值落在 (0,1) 比例 | 高（>60%）→ 已压缩/有界，可跳过 `zscore` 直接用或 `rank`；低 → 需标准化 |
| `IntegerStatus` | 是否整数值 | 整数（计数类）→ 用 `rank`/`group_rank`/`bucket`，**勿用 `ts_mean` 平滑**（会抹掉离散信息）；连续 → `ts_mean` 平滑可用 |
| `skewness`（skew 偏度） | 分布偏斜 | 高偏 → `winsorize` 或 `signed_power(x, 0.5)` 或 `rank` 降偏 |
| `kurtosis`（峰度） | 尖峰厚尾 | 高 → `rank` / `winsorize`，抑制极端值 |
| `yearly_distribution` | 逐年直方图 | 形态分类：`point_mass`/`zero_inflated`/`ceiling`/`concentrated` → `rank(+winsorize)`；`spread`(近似正态) → `zscore`/`ts_zscore` 可用 |

**组合范式**（V9 突破版，保留并加字段预处理前置）：
```
scale(rank(ts_zscore(subtract(
    ts_mean(ts_backfill({field_B}, 66), 22),
    ts_mean(ts_backfill({field_A}, 66), 22),
    filter=true), 189)))
+ scale(-rank(ts_zscore(returns, 42))) * 0.35
```

## 3. 低竞争 / 白空间发现（distribution.js）

### 3.1 白空间表（`non_data`，Delay≠0 零提交对 = 真低竞争）
注意区分两类：
- **`non_data`（Delay 1+）零提交 = 真·低竞争机会**（重点）。
- **`non_data_delay0` 零提交 ≠ 机会**，多为该 region 在 Delay 0 无数据（仅 USA/AMR/EUR 有广泛 Delay0 覆盖），是数据不可用而非空白。

**可行动白空间（来自 `non_data`，按 region）：**
- **Broker**：几乎全 region 空白（GLB/USA/CHN/AMR/HKG/TWN/ASI/EUR/KOR）——但 Broker 数据本身在多数区域受限，先验证可用性。
- **KOR 空白**：Broker、Institutional Ownership、Macro、Option、Sentiment、Social media（Insiders/Fundamental/Analyst/News/Earnings/Short interest/PV/Model 有数据）。
- **Insiders 空白**：TWN、GLB、CHN。
- **Institutional Ownership 空白**：GLB、CHN、HKG、TWN、ASI、KOR。
- **Macro 空白**：CHN、HKG、TWN、ASI、KOR。
- **Option 空白**：CHN、HKG、TWN、ASI、KOR。
- **Sentiment 空白**：GLB、CHN、AMR、HKG、TWN、ASI、KOR（仅 USA/EUR/JPN 有）。
- **Social media 空白**：TWN、KOR。

### 3.2 平台多样性约束
- 平台 `dataDiversity.check` = PASS/FAIL 强制区域/类别多样性。
- 在 `non_data` 空白区提交，既能**低竞争**又能**满足多样性**——一石二鸟。

### 3.3 算子多样性（genius.js）
- `genius.js` 的 operator analysis 抓取你本季所有 alpha，统计各 operator 使用次数。
- **决策**：找你**极少使用**的 operator（如 `ts_regression`、`group_rank`、`winsorize`、`signed_power`），主动补进新 alpha，满足 Genius 六维（operatorCount / fieldCount 等）。
- operator 符号映射（解析 alpha code 用）：`+`→add, `-`→subtract, `*`→multiply, `/`→divide, `^`→power, `<=`→less_equal, `>=`→greater_equal, `<`→less, `>`→greater, `==`→equal, `!=`→not_equal, `?`→if_else, `&&`→and, `||`→or, `!`→not。

## 4. 模拟参数参考（simulate.js payload）

标准仿真请求体（所有可设字段）：
```json
{
  "type": "REGULAR",
  "settings": {
    "maxTrade": "ON", "nanHandling": "ON", "instrumentType": "EQUITY",
    "delay": 1, "universe": "TOP3000", "truncation": 0.08,
    "unitHandling": "VERIFY", "testPeriod": "P0D", "pasteurization": "ON",
    "region": "USA", "language": "FASTEXPR", "decay": 0,
    "neutralization": "SUBINDUSTRY", "visualization": false
  },
  "regular": "close"
}
```
- **限流**：响应头 `x-ratelimit-limit` / `x-ratelimit-remaining`；`429` = `SIMULATION_LIMIT_EXCEEDED`。并发上限 C=5（信号量包住整条 run_backtest）。
- **delay 选择**：Delay 0 仅 USA/AMR/EUR 数据广；其余区域用 Delay 1。

## 5. 信号构建范式（保留 V9 突破版）

### 最佳参数
- decay：4（returns 信号）、6（close 信号）
- neutralization：按数据集 dominant method（KOR→SECTOR，USA→SUBINDUSTRY）
- truncation：0.08；testPeriod：P6Y；instrumentType：EQUITY；delay：1

### 范式层级（从弱到强，USA 实测）
1. 纯基金信号：S=1.2-1.75，IS_LADDER ≤1.45
2. +ts_mean(22) 平滑：S=1.6-1.7，IS_LADDER=1.37
3. +close 反转组合：S=1.84，IS_LADDER=1.58（FAIL，阈值严格 >1.58）
4. **+returns 反转组合（突破）**：S=2.23，IS_LADDER=2.12 PASS

### 关键认知（修正版）
1. `returns` 反转 >> `close` 反转（近 2 年子区间尤其明显）。
2. 低 decay 配合 returns：decay=4/5 时 IS_LADDER 飙到 2.0+。
3. `IS_LADDER_SHARPE` 阈值 **严格 >1.58**（非 ≥1.58）。
4. 含价格信号触发 `IS_LADDER_SHARPE`；纯基金信号触发 `LOW_2Y_SHARPE`。
5. testPeriod P4Y/P3Y 不改变 IS_LADDER 计算；truncation 不影响 IS_LADDER。
6. SECTOR/MARKET 中性化大幅降低 IS_LADDER。
7. `hump` 对组合信号有破坏性（即使 0.001 也摧毁），勿用。
8. `subtract()` 支持 `filter=true`；`divide()` **不支持** filter=true。
9. `ts_regression(A,B,n).residual` 语法无效。

## 6. 闸门检查体系

### 廉价闸门（PC 等待前）
- Sharpe ≥ 1.58；Fitness ≥ 1.00；TVR ∈ [5%, 20%]；Margin > 5bp；Returns > 5%；平台检查无 FAIL。

### 硬闸门（PC 等待后）
- PROD_CORRELATION < 0.70（用户绝对红线）；SELF_CORRELATION < 0.50；复校廉价闸门。

## 7. 增强版挖掘流程（数据驱动）

0. **平台实时体检（不可跳过）**：`python scripts/dataset_health_check.py --region <R> --delay <D> --universe <U>`
   → 过 §1.0 三条硬门槛（cov≥0.85 / alphaCount≤50 / fields≥10），得到候选白名单。
   **后续所有步骤只在这份白名单内进行。** 白名单为空才考虑换区域/换 universe。
1. **数据集扫描**：在白名单内，WebDataScope 读 OS/IS Sharpe 徽章 → 选绿(>>均值)；读中性化徽章 → 定 neut；标 OS 退化。（★★★ 仅表示离线包完整，不参与可用性判断，见 §1.3）
2. **白空间扫描**：distribution.js `non_data` → 选 (region, category) 空白（低竞争 + 多样性）；与体检结果中 `alphaCount==0` 的数据集交叉验证。
3. **字段探测**：对每个候选字段读 dataAna 10 指标 → 定预处理（backfill / winsorize / rank / zscore / integer-bucket）。
4. **信号构建**：找有预测力的字段对 (A,B) 建 reversed spread，加 returns 反转组合提 IS_LADDER。
5. **参数扫描**：decay / 权重 / 窗口 / 中性化 / truncation 微调。
6. **算子多样性**：查 genius operator analysis，补 under-use 算子。
7. **闸门检查**：廉价闸门 → PC 等待 → 硬闸门。
8. **提交**：tags=["PowerPoolSelected"]，color=GREEN。

## 8. 区域实证结论（并入，待持续更新）

- **KOR**：SECTOR 最佳中性化(0.562)；sweet datasets：news59(0.597)、insiders5(0.564)、shortinterest3(0.524)、risk71(OS 1.306)、analyst39；model253 退化。
  平台实测(2026-08-05, TOP600/D1)：**192 个数据集**，cov 均值 0.7046，54 个 cov≥0.90。此前"KOR_TOP600 低覆盖(仅 1 数据集)"的说法来自离线包，与平台实况不符，已作废。
- **EUR**（结论已修订，原"死路"判断作废）：TOP1200/D1 实有 **178 数据集 / 38609 字段**，cov 均值 0.6616，35 个 cov≥0.90。
  原战役失败根因是**选集错误**而非区域无解（详见 §1.0 / §1.3 案例）。
  未开发首选：`ml_factor_proj`（**333 字段全部 cov=1.0**，MATRIX 类型，0 用户 0 alpha，valueScore 5.0，倍率 1.5，字段为标准因子变化率语义如 `change_1y_eps_growth`，可直接套模板）；
  次选 `news_sentiment_nlp`（valueScore **6.0** 全场最高，23 字段易穷举）、`global_seasonal_model`（449 字段 0 alpha）、`continuation_score` / `pattern_scores`（各 500+ 字段 cov 0.99 零 alpha）。
- **HKG**（TOP800/D1 实测）：**209 个数据集**（三区最多），cov 均值 0.6958，43 个 cov≥0.90。倍率档位三区最高（多个 1.8）。
  未开发首选：`news_sentiment_nlp`（**vs 9.0 / pm 1.8 / 0 alpha**）、`news_sentiment_dl`（vs 7.0 / pm 1.8 / 1 alpha）、`mmp_nlp_sentiment`（521 字段 cov 0.9476 / vs 7.0 / pm 1.8 / 2 alpha）。

- **★ 跨区域倍率差（决定区域优先级，选区前必查）**
  同一数据集在不同区域的 `pyramidMultiplier` / `valueScore` / 拥挤度差异巨大，**同样的信号在不同区域收益可差 20%+**：

  | 数据集 | EUR (TOP1200) | KOR (TOP600) | HKG (TOP800) |
  |---|---|---|---|
  | `news_sentiment_nlp` | pm1.5 / vs6.0 / **a0** | pm1.7 / **vs9.0** / **a0** | **pm1.8** / **vs9.0** / **a0** |
  | `ml_factor_proj` | pm1.5 / vs5.0 / **a0** | pm1.7 / vs6.0 / a10 | **pm1.8** / vs6.0 / a38 |
  | `ai_factor_transfer` | pm1.3 / vs4.0 / a0 | **pm1.7** / vs6.0 / a8 | pm1.7 / vs5.0 / a9 |
  | `analyst_earnings_ibes` | pm1.3 / vs5.0 / a1 | **pm1.7** / vs6.0 / a6 | pm1.7 / vs6.0 / a11 |
  | `price_signal_dl` | pm1.3 / vs5.0 / a2 | **pm1.7** / vs6.0 / a6 | pm1.7 / vs6.0 / **a1** |
  | `global_seasonal_model` | pm1.3 / vs5.0 / **a0** | pm1.7 / vs6.0 / a70 | pm1.7 / vs6.0 / a6 |

  **结论**：EUR 的倍率系统性低于 KOR/HKG（1.3–1.5 vs 1.7–1.8）。区域优先级 **HKG ≈ KOR > EUR**。
  **头号目标 `news_sentiment_nlp`**：三区**全部 alphaCount=0**（零竞争），KOR/HKG 的 valueScore 高达 **9.0**，字段仅 17–23 个可快速穷举。这是当前性价比最高的入口。
  **方法**：新战役开打前，对 2–3 个候选区域各跑一次 §1.0 体检，比完倍率再定区域，不要凭习惯选区。
- **ASI**：model110 经 mcp__wq-brain-http__get_datafields 取到 8 个 ASI 字段。
- **USA/D1/TOP3000**：institutions18 ✅ 3 个 PPA 提交(S=2.23)；institutions6/20 信号弱；imbalance5 仅 2 字段；fund_holdings_panel P6Y 不可用。
  b107–b128 战役：9+ 家族 15 批次，sharpe>1.5 者全部被 **prod_corr>0.7** 卡死（最佳 0.724，差 0.024），0 可提交 → 印证 §1.0 的 `alphaCount≤50` 门槛不是可选项。

## 9. WQ Brain API 要点

- 并发上限 C=5，信号量包住整条 run_backtest（POST+轮询）。
- 401 需自动重认证：捕获 401 后用凭据重新走 Basic Auth 建立会话再继续请求（自行实现 `_reauth()` 逻辑）。
- testPeriod 最大 P6Y0M0D。
- `hump(x, hump=0.01)` 必须命名参数。
- 429 限流：短退避重试（wait=min(20+attempt*8, 45)s，最多 ~40 次）。
- 孤儿模拟占槽：`TaskStop` 制造孤儿，只能等其自行释放。
- MCP（lavender1203 fork，Streamable HTTP，端口 8876）：66 工具（另有 wqb-db 台账服务器 32 工具），含 `mcp__wq-brain-http__get_datasets` / `mcp__wq-brain-http__get_datafields` / `mcp__wq-brain-http__create_multi_simulation` / `mcp__wq-brain-http__get_user_alphas`（count 上限 10000）/ `mcp__wq-brain-http__get_platform_setting_options` / `mcp__wq-brain-http__operator_audit` / `mcp__wq-brain-http__submit_verdict` / `mcp__wq-brain-http__workflow_*`（workflow 引擎：7 个节点快捷方式 + `workflow_list_nodes` / `workflow_execute` / `workflow_chain`）。连接需用户在连接器页 Trust。

### 9.1 data-sets / data-fields 实测约束（2026-08-05 验证，勿重复踩坑）

1. **数据集级体检走 `mcp__wq-brain-http__get_datasets`，不要逐字段聚合。** `/data-sets` 直接返回 `coverage / fieldCount / userCount / alphaCount / valueScore / pyramidMultiplier`，比拉 1 万个字段再 group-by 快约**两个数量级**。
2. **`GET /data-fields` 必须四参齐全**：`instrumentType + region + delay + universe`。只给 `dataset.id` 而不给 `universe` → **400 Invalid query**。（`dataset.id` 参数是存在的，服务端 `main.py:1241` 就在用；此前"该参数不存在"的判断是错的。）
3. **`universe` 传该区域非法档位 → HTTP 500**（不是 400），错误信息无提示，极易误判为服务故障或参数不支持。合法档位（`mcp__wq-brain-http__get_platform_setting_options` 实测）：
   - `USA`: TOP3000 / TOP2000 / TOP1000 / TOP500 / TOP200 / TOPSP500 / ILLIQUID_MINVOL1M
   - `EUR`: TOP2500 / TOP1200 / TOP800 / TOP400 / TOPCS1600 / ILLIQUID_MINVOL1M
   - `GLB`: TOP3000 / MINVOL1M / MINVOL10M / TOPDIV3000
   - `ASI`: TOP500 / MINVOL1M / MINVOL10M / ILLIQUID_MINVOL1M
   - `CHN`: TOP2000U / `KOR`: TOP600 / `HKG`: TOP500 / TOP800 / `IND`: TOP500 / `GBR`: TOP700 / `DEU`: TOP500 / `MEA`: TOP300 / TOP400
4. **响应格式差异**：直连 REST 返回的 `category` / `subcategory` 是 **dict**，MCP 已扁平化为 **str**，跨通道处理需归一化。
5. **沙箱链路抖动**：Bash 启动的 Python 直连 `api.worldquantbrain.com` 会间歇性 TLS 中断（表现为 `SSL: UNEXPECTED_EOF_WHILE_READING`，也可能被误报成 `ProxyError` / `RemoteDisconnected`，但 `HTTP(S)_PROXY` 实为 None）。**优先复用常驻 MCP 服务的稳定会话**；必须直连时对 429/5xx 与连接异常做指数退避（实测退避后可成功）。
6. 账号与常驻 MCP 服务共享配额，独立脚本高频拉取易触发 **429**，务必带退避。
