# `us_short_sale` 字段画像 · USA / TOP3000 / D1（全量 4/4 字段）

> **as_of**：2026-11-16（采集时点）｜**文件名日期**：20261115（按任务指定）｜**区**：USA 固定
> **口径**：region=USA / universe=TOP3000 / delay=1 / instrumentType=EQUITY（`get_datasets` + `-m wqb.profiles explain`）
> **数据源**：平台 `get_datafields`（`filter_sharpe=false`、`max_fields` 未设、`count=4 == platform_count=4`、`complete=true`、`pages_fetched=1` ⇒ **无截断、无抽样**）
> **本文件回答**：这个数据集长什么样、每个字段能干什么、哪些机制已经被实测过、哪些还没测、现在能不能判死。
> **不回答**：能不能提交（提交权归用户；`WQB_ALLOW_ALPHA_SUBMIT=False`，本次零提交、零仿真派发）。

---

## §0 归档路径与命名规则（必读）

### 0.1 本次落盘的两个位置

| 角色 | 路径 |
|---|---|
| **主档（归档母本）** | `tracking/USA/reference/_usa-us_short_sale-field-profile-20261115.md` |
| **skills 镜像（Agent 读取位）** | `Claude/skills/wq-brain-ra-usa/references/_usa-us_short_sale-field-profile-20261115.md` |

两份**逐字相同**；改一处必须同时改另一处（`tracking/` 侧是归档母本，`Claude/skills/` 侧是区域分支 skill 的实证目录）。

### 0.2 命名规则

```
_usa-<dataset_id>-field-profile-<YYYYMMDD>.md
```

- **`_` 前缀** = 区域专题（手写实证），**不是** `wqb.profiles render` 的生成物 ⇒ 不会被 `render --apply` 覆盖；
  与生成块文件（`references/<category>.md` 的 `profiles:cell-panel` 块）分工不同。
- **`<dataset_id>` 保留原样（含下划线）**：本仓既有的 field-profile 多用 kebab（`_usa-fund-holdings-panel-field-profile-20261023.md`、
  `_usa-board-gov-stats-field-profile-20261020.md`），但那些数据集 id 本身就带下划线（`fund_holdings_panel`、`board_gov_stats`）。
  本文件按任务给定的 `_usa-<ds>-field-profile-<date>.md` 模板**保留 `us_short_sale` 原样**：
  ① 与平台的 dataset_id 逐字一致，grep `us_short_sale` 不会漏；② 避免 `us-short-sale` 与 `us_short_sale` 两个写法并存产生分叉。
  若要统一成 kebab，**改名一次做全**（母本 + 镜像 + 所有引用方），不要留别名副本。
- **`<YYYYMMDD>` = 画像文件名日期**。本文件取任务指定的 `20261115`；实际采集时点是 **2026-11-16**，
  两者不同就已在本行显式登记，**不要**把文件名日期当成数据时点引用。
- 类别级扫描的命名另有一套（`_usa-<category>-dataset-scan-<asOf>.md`），见 `_usa-shortinterest-dataset-scan-20261019.md:3-5`。

### 0.3 生效流程（镜像写完必做）

仓库 `Claude/skills/` 是编辑权威，安装位是派生物：

```bash
$WQ_PY tools/sync_skills.py            # 从仓库同步到 5 个受维护安装位
$WQ_PY tools/sync_skills.py --check    # 期望「全部受维护安装位与仓库一致」
```

本文件归档的实际执行记录（2026-11-16，本会话真跑）：

| 步 | 命令 | 输出 |
|---|---|---|
| ① 落盘前基线 | `… tools/sync_skills.py --check` | 5/5 安装位一致（绿） |
| ② 母本 → 镜像 | `cp tracking/…  Claude/skills/…` | 两侧 `md5sum` **相同**（逐字一致；哈希随每次编辑变化，只作同版本比对，不作跨版本比对） |
| ③ 同步 | `… tools/sync_skills.py` | **已同步 5 个文件（5 个安装位）** = 本文件 1 个 × 5 个安装位 |
| ④ 复验 | `… tools/sync_skills.py --check` | **全部受维护安装位与仓库一致** |

⇒ 任何后续修改本文件，都要重跑 ③④；只改 `tracking/` 侧或只改 `Claude/skills/` 侧都会造成母本与镜像分叉。

---

## §1 数据集级元数据（平台实拉，2026-11-16）

| 项 | 值 | 来源 |
|---|---|---|
| dataset_id | `us_short_sale` | `get_datafields` / `get_datasets` |
| name | **US Equity Short Sale Volume** | `get_datasets(category=shortinterest)` |
| category | `shortinterest` | 同上 |
| coverage（数据集级） | **1.0** | 同上 |
| **fieldCount（平台声明）** | **4** | 同上 —— 本次**全量取回 4/4**，无遗漏 |
| userCount | 189 | 同上 |
| alphaCount（数据集级） | **356** | 同上 |
| valueScore | 3.0 | 同上 |
| **pyramidMultiplier** | **1.1**（短利塔 ×1.1） | 同上 |
| 分组 | ShortInterest | `-m wqb.profiles explain --region USA --dataset us_short_sale` |
| 字段类型分布 | **4/4 MATRIX，0 个 VECTOR** | `get_datafields` |

**描述（平台原文，唯一语义来源）**：
> "This dataset provides comprehensive daily and monthly records of short sale activity across major US equity markets, including aggregate short sale volumes and total trading volumes for all exchange-l…"

**同类别 6 个集（`get_datasets` 全量，count=6）**：

| dataset | name | fieldCount | aC | cov | valueScore |
|---|---|---:|---:|---:|---:|
| `short_interest_pred` | Short Interest Forecast Signals | 10 | 518 | 0.9987 | 3.0 |
| `shortinterest24` | Short Sale Circuit Breaker Data | 1 | 449 | 0.2573 | 3.0 |
| `shortinterest29` | Group Short Sale Data | 32 | 276 | 0.8838 | 4.0 |
| `shortinterest3` | Securities Lending Files Data | 31 | 4856 | 1.0 | 2.0 |
| `shortinterest43` | Short Sell Dataset | 32 | 1571 | 0.9994 | 3.0 |
| **`us_short_sale`** | **US Equity Short Sale Volume** | **4** | **356** | **1.0** | **3.0** |

### 1.1 回测设置（本数据集的生效画像，逐项带来源）

`world-quant-brain-mcp/.venv/Scripts/python.exe -m wqb.profiles explain --region USA --dataset us_short_sale` 实跑输出：

| 设置 | 值 | 来源标记 |
|---|---|---|
| universe / delay | TOP3000 / 1 | settings.json |
| neutralization | **SUBINDUSTRY** | settings.json |
| decay | **5** | settings.json（本组合 cells 无覆盖） |
| truncation | 0.08 | settings.json |
| maxTrade / nanHandling / pasteurization / unitHandling | OFF / ON / ON / VERIFY | settings.json |
| startDate / endDate | 2013-01-01 / 2023-12-31 | settings.json |
| Mode B 主闸 | sharpe **1.25** / fitness **0.8** | GLOBAL_ledger（下限锁） |
| review 阈值 | S≥1.25、F≥1.0、2Y≥1.6、margin≥0.0005、**TO∈[0.05, 0.30]**、`ra_failed_count_max=0` | thresholds.json |
| 可投资性闸 | **invest_S / S ≥ 0.70** | `Claude/skills/wq-brain-ra-usa/SKILL.md:98-103` |
| prod 红线 | **max < 0.70 才 PASS，无豁免** | `src/wqb/config.py:502`（`PRODCORR_CEILING = 0.70`）+ 任务硬约束 |
| 窗口白名单 | 1 / 5 / 22 / 66 / 252 / 504 / 1008 / 1260 | `src/wqb/config.py:656` |

> ⚠ **decay=5 是区域缺省，不是本集实证最优**。已实测 4 臂（§6）用的是 MCP 直连、设置未逐项记录 ⇒
> 与区域缺省**不可假定量纲一致**（`Claude/skills/wq-brain-ra-usa/references/shortinterest.md` 的「设置是强度闸」提醒）。

---

## §2 预注册判据（开波前必填，禁止事后挑选口径）

依据 `Claude/skills/wq-brain-ra-usa/references/_usa-field-profile-playbook-20261018.md:24-31`（P1-1 裸强度探针 + P0-1 prod 探针）。

| 项 | 本集预注册内容 | 判据 |
|---|---|---|
| **裸强度探针** | `group_rank(ts_mean(divide(executed_short_trade_share_count, aggregate_executed_trade_share_count), 22), subindustry)` | **\|S\| < 0.5 ⇒ kill 该字段对**；实测 **0.84**（`RReYlOVz`）⇒ **不 kill，但也没过 1.0 的「需继续」线** |
| **prod 探针** | `campaign_intel.py prod-probe --region USA --dataset us_short_sale`（每族 1 条，不占回测槽） | `prod ≥ 0.75` 封族；**[0.70,0.75) 按 D0-P 处置**。**本集 prod 从未测过**（§9 缺口 G1） |
| **机制归属** | F1/F2 = 日频做空成交压力（FINRA Reg SHO 日报口径）；**不是**做空余额/挤空类经典异象 | 登记位 `tracking/USA/reference/usa_dataset_mechanisms.md` —— **当前无 `us_short_sale` 条目**（缺口 G3） |
| **证伪条件** | 见 §4 每族「可证伪假设」的证伪行 | 回测后按此写归因，不得事后改口径 |

**共同前提（本节所有读数）**：USA / TOP3000 / D1 / SUBINDUSTRY / truncation 0.08 / nanHandling ON / maxTrade OFF；
`failed_ra_count`、`investability_ratio` 取 `batch_get_alpha_metrics`；逐年取 `get_alpha_yearly_stats`。

---

## §3 逐字段画像（4/4 全量，无抽样）

### 3.0 总表

| # | field id | type | coverage | userCount | **alphaCount（平台实数）** | 经济量 | 更新频率 | 分布形态 | 族（§4） |
|---|---|---|---:|---:|---:|---|---|---|---|
| 1 | `aggregate_executed_trade_share_count` | MATRIX | 1.0 | 129 | **223** | 常规交易时段**总成交股数** | 日频 | 非负股数、厚尾右偏、量级≈规模×换手 | F3（分母/流动性） |
| 2 | `executed_short_trade_share_count` | MATRIX | 1.0 | 124 | **218** | 常规交易时段**做空成交股数** | 日频 | 非负股数、厚尾右偏，且 ⊆ 字段 1 | F1（分子） |
| 3 | `reported_short_sale_share_quantity` | MATRIX | 1.0 | 74 | **126** | **全市场汇总**的做空成交股数 | 日频 | 非负股数、厚尾右偏，且 ⊆ 字段 4 | F2（分子） |
| 4 | `reported_total_trade_share_quantity` | MATRIX | 1.0 | 76 | **131** | **全市场汇总**的总成交股数 | 日频 | 非负股数、厚尾右偏、量级≈规模×换手 | F3（分母） |

> **alphaCount 必须读平台实数**：本地 `get_field_catalog` 给的是 36 / 37 / 30 / 32（约实况的 16–17%），
> 是**陈旧快照**，见 §5.2 对账。

### 3.1 `aggregate_executed_trade_share_count`

- **id / type / coverage**：`aggregate_executed_trade_share_count` / **MATRIX** / **1.0**
- **alphaCount / userCount**：**223** / 129（平台实数；本地 catalog 记 36 / 25）
- **语义（description 原文，唯一语义来源）**：*"Total number of shares traded during regular trading hours."*
  —— **常规交易时段**（不含盘前盘后）的**总成交股数**，多头+空头都算；是**流量**（volume），不是余额。
- **更新频率**：**日频**。依据三条：① description 的 "during regular trading hours" 是逐日口径；
  ② 数据集级 description 明写 "daily and monthly records"；③ 实测臂（§6）在 22 日 `ts_mean` + decay 5–8 下换手 0.023–0.065，
  与日频更新一致（若是月频，22 日均值会退化成阶梯、换手应显著更低）。
  ⚠ 平台 `/data-fields` 返回体**没有 frequency 字段**（本次返回的键只有 `id / type / coverage / userCount / alphaCount / description`），
  所以频率**只能**由 description + 实证反推，**不是平台元数据直读**。
- **分布形态**：非负**股数**（计数型），横截面厚尾右偏；量级由「流通盘 × 当日换手」决定。
  **可判定的是形态（非负 + 难有上界 + 量级跨几个数量级）；本会话未测数值矩**（median / 偏度 / 峰度 / 零值率）——
  `/data-fields` 不提供分布统计，`get_record_set_data` 需要 alpha_id，本次没有为此开仿真。
  ⇒ 直接当信号 = 拿「规模 × 换手」当 alpha，属**风格 beta**（`_usa-field-profile-playbook-20261018.md:17`：risk-neut <0.3 一律弃）。
- **可用性与 alpha 适用性**：**可用（cov 1.0）**，但**只建议当分母 / 流动性条件**，不建议独腿。
  角色依据：`docs/experience/02_signal_patterns.md:449-486`（分母决定横截面比较基准，换分母才是破 self/prod 墙的真变量）。
  alphaCount 223 已略高于「<200 = 低拥挤」线（同一文档 `:15`），拥挤度中等。

### 3.2 `executed_short_trade_share_count`

- **id / type / coverage**：`executed_short_trade_share_count` / **MATRIX** / **1.0**
- **alphaCount / userCount**：**218** / 124（本地 catalog 记 37 / 26）
- **语义（description 原文）**：*"Total number of shares sold short during regular trading hours."*
  —— 常规交易时段**被卖空的股数**（申卖标记为 short 的成交），**流量**。
  ⚠ 注意它**不含**"exempt / non-exempt" 拆分：institutions20 有 `exempt_short_trade_share_total` 与
  `short_exempt_transaction_share_count`（§5.3），本集没有 ⇒ **无法把做市商豁免性做空从方向性做空里剥出来**，
  这是本集比 institutions20 更粗、也更噪的结构性原因。
- **更新频率**：**日频**（同 3.1 三条依据，"regular trading hours" 逐日口径）。
- **分布形态**：非负股数、厚尾右偏；与 3.1 同一口径（同为 executed/regular-hours 口径），
  经济上应满足 `executed_short ≤ aggregate_executed` ⇒ 二者之比落在 [0,1]。
  **本会话未验证该不等式在数据上是否恒成立**（负值/越界会在比率里表现为 >1 或 <0，属于必须先测的数据质量项）。
- **可用性与 alpha 适用性**：**可用（cov 1.0，aC 218 中等拥挤）**。**首选角色 = 比率的分子**（F1），
  且历史实测方向一致为**反向**（做空占比高 → 未来收益差）：2026-11-15 的四臂里 `reverse` 版 S **+0.84**、
  非 reverse 版 S **−0.83**（§6.1），符号严格对称 ⇒ 方向可信、强度不足。
- **不要单独当腿**：水平值 = 规模/流动性代理，方向随规模漂移。

### 3.3 `reported_short_sale_share_quantity`

- **id / type / coverage**：`reported_short_sale_share_quantity` / **MATRIX** / **1.0**
- **alphaCount / userCount**：**126** / 74 ——**本集最不拥挤的字段**（<200，符合「低拥挤」线；也是 4 个字段里 userCount 最低的）
- **语义（description 原文）**：*"Aggregate quantity of shares sold short across all included markets."*
  —— **跨全部纳入市场汇总**的做空股数（对比 3.2 的 "regular trading hours"：**差异在市场覆盖口径，不是时段**）。
- **更新频率**：**日频**（数据集级 "daily and monthly records"；本字段描述用 "aggregate … across all included markets"，
  未写 monthly，且字段目录里**没有**对应的 monthly 字段 —— 4 个字段全是日频流量）。
- **分布形态**：非负股数、厚尾右偏；与 3.4 同口径，故 `reported_short ≤ reported_total` 应有 [0,1] 比率。
  **未测数值矩**（同上）。
- **可用性与 alpha 适用性**：**本集最优选腿**（拥挤度最低 + 口径最完整）。角色 = F2 的分子。
  历史主用骨架是 `divide(reported_short, reported_total)`（`tracking/USA/candidates/exprs_usa_prod19_shortint.json:14-29`、
  `exprs_usa_prod19b_shortint_tvr.json:16-28`），属已多次测过的机制 ⇒ 开新波要**换结构**（§8 D1）。
  ⚠ 本地自动分类器把它分到 `semantic_family = 其他`，另三个字段分到 `价量与波动` —— 同一经济量的分类不一致，见 §5.3(b)。

### 3.4 `reported_total_trade_share_quantity`

- **id / type / coverage**：`reported_total_trade_share_quantity` / **MATRIX** / **1.0**
- **alphaCount / userCount**：**131** / 76（本地 catalog 记 32 / 22）
- **语义（description 原文）**：*"Aggregate quantity of shares traded across all included markets."*
  —— 跨全部纳入市场汇总的**总成交股数**（含多空），**流量**。
- **更新频率**：**日频**（同 3.3）。
- **分布形态**：非负股数、厚尾右偏、量级≈规模×换手；与 3.1 的差别只在市场覆盖口径。
- **可用性与 alpha 适用性**：**可用**，角色 = F2 的分母 / 规模归一化基。
  **额外用途（未测）**：`reported_total ÷ aggregate_executed` = **口径覆盖比**（全市场汇总 ÷ 常规时段单一口径），
  是市场结构（成交去哪了）的代理，**更适合作分组轴**而不是信号腿（§4.4 附）。

---

## §4 字段族归并（按经济机制）与可证伪假设

四字段按「分子 / 分母 × 覆盖口径」自然成两对，外加一对**派生**。每族一条可证伪假设，证伪条件写在族内。

```
F1  executed 口径做空占比   = executed_short_trade_share_count / aggregate_executed_trade_share_count
F2  reported 口径做空占比   = reported_short_sale_share_quantity / reported_total_trade_share_quantity
F3  成交总量（规模/流动性）  = aggregate_executed_trade_share_count, reported_total_trade_share_quantity  （单腿）
F4  双口径背离（派生）       = F1 − F2      （另附：口径覆盖比 reported_total / aggregate_executed）
```

### F1 · executed 口径做空成交压力

- **字段**：`executed_short_trade_share_count`（分子）+ `aggregate_executed_trade_share_count`（分母）
- **机制叙述**：单日"卖空成交 / 全部成交"= 当日做空压力（FINRA Reg SHO 日报口径）。做空压力高 → 短期卖压 →
  未来收益差；反向持有低做空压力股，博卖压释放后的修复。
- **可证伪假设 H1**：*日频做空成交占比在 TOP3000 上不存在**稳定的**横截面方向；现有 0.84 的读数是个股噪声上限，
  换窗口/平滑/分组都不能把它推过 1.58。*
  - **支持证据**：22d 反向 = 0.84（`RReYlOVz`）、66d+tail = 0.48（`wpo1GoRv`）、126d = 0.54（`qM7dG7lK`）
    —— 三个窗口**全部低于 1.0**，且 2019 年 pnl 为负（§7）。
  - **证伪条件**：任一**结构互异**模板（不是换窗/换 decay）在同一设置下 S ≥ **1.58** 且 `failed_ra=0`
    ⇒ H1 被推翻，进 S4 网格。
- **状态**：**已测 3 臂（2026-11-15）+ 早期 4 臂（2026-10-19，字段未记录）**，方向可信、强度不足。

### F2 · reported 口径做空成交压力

- **字段**：`reported_short_sale_share_quantity`（分子）+ `reported_total_trade_share_quantity`（分母）
- **机制叙述**：与 F1 同机制，但覆盖**全部纳入市场**，理论上少了单一口径的 venue 噪声。
- **可证伪假设 H2**：*reported 口径比 executed 口径更干净 —— 同窗口、同设置下，reported 比率的 |S| 应比 executed 比率高 ≥0.2。*
  - 若成立 ⇒ 后续只用 F2（本集最不拥挤的两字段正好都在 F2，aC 126/131）。
  - **证伪条件**：两者差 <0.2，或 reported 更低 ⇒ 「口径完整性」不是噪声来源，F1/F2 应合并成同一族。
  - **现状**：**未做这个对照实验**。2026-11-15 的四臂全部用 executed 口径；历史上常用骨架用 reported 口径
    （`exprs_usa_prod19_shortint.json:14-29`），但两者的**设置与窗口不同**，不可直接比。⇒ H2 待测（缺口 G4）。
- **状态**：已多次测过同一骨架（reported 比率 + zscore/rank + 多 decay），**0 条过闸**（本节无及格读数入库）。

### F3 · 成交总量（规模 / 流动性）

- **字段**：`aggregate_executed_trade_share_count`、`reported_total_trade_share_quantity`
- **机制叙述**：这两个是"总成交股数"，本质是**规模 × 换手**的复合量，不是做空信号。
- **可证伪假设 H3**：*这两个字段单独作信号 = 规模/流动性 beta，risk_neutralized_sharpe < 0.3，做不出 alpha。*
  - **证伪条件**：risk-neut Sharpe ≥ 0.3，且做因子正交化后保留 ≥50% 强度
    （判定口径见 `_usa-field-profile-playbook-20261018.md:17,146,192`；正交化掉幅 >50% 判 KILL 的用法见同册 §8.5）。
  - **现状**：**从未单独测过**（历史表达式一律把它们当分母）⇒ H3 未验证，但先验很强
    （与 `risk70` 的 `market_capitalization_factor` / `trading_liquidity_factor` 同方向，`docs/experience/03_region_dataset.md:347`）。
  - **纪律**：即便 H3 被证伪，也不建议把它们当信号腿——它们会把 alpha 变成规模/流动性暴露，撞 LOW_SUB_UNIVERSE 与 invest 闸。
- **状态**：**仅作分母测过**；单腿 = 未测（缺口 G5）。

### F4 · 双口径背离（派生，本集唯一未被任何人测过的机制）

- **构造**：`divide(executed_short, aggregate_executed) − divide(reported_short, reported_total)`
- **机制叙述**：两套同源但**覆盖不同**的做空占比之差，度量"做空行为在常规时段单一口径 vs 全市场汇总口径之间的错配"。
  若做空集中在特定申报口径（例如做市商在某设施上的对冲），背离会先于总量变化。
- **可证伪假设 H4**：*背离携带单口径比率**之外**的信息 —— 反向背离应与单口径比率**低互相关（<0.5）**，且 |S| 不低于单口径。*
  - **证伪条件**：`compute_mutual_correlation(背离, 单口径比率)` ≥ 0.9 ⇒ 两者几乎是同一变量，背离无独立信息，判死该机制。
  - **现状（可核实的新颖性证据）**：全仓检索 `tracking/USA/candidates/*.json` 中**同时**引用两套字段名的表达式 = **0 条**
    （`grep "reported_short_sale" … | grep -c "executed_short_trade_share_count"` ⇒ `0`）。
    历史只出现过"单口径比率"一种形态 ⇒ **F4 完全未测**。
- **状态**：**未测（唯一的新机制入口）**。这是本集在「D1 结构互异模板」上最省力的补位方向。

### 4.4 附：口径覆盖比（市场结构轴，未测）

`reported_total_trade_share_quantity ÷ aggregate_executed_trade_share_count` = 全市场汇总成交量 ÷ 常规时段单一口径成交量。
经济含义是"成交在申报口径间的分布"，**近静态**（截面差异大、时序慢）⇒ 按 `_usa-field-profile-playbook-20261018.md` 的
「110+ 行业/板块暴露 score 只能当分组原料」同理（`docs/experience/03_region_dataset.md:390`），**建议只做 `bucket()` 分组轴**，
不做信号腿。同样**未测**。

### 4.5 本集**做不到**的机制（语义层结论，重要）

类别卡（`-m wqb.profiles explain --region USA --dataset us_short_sale` 的 S2 原语）列了 5 个 shortinterest 原语：
`short interest change` / `short squeeze potential` / `short covering` / `days to cover` / `short interest momentum`。
**这 5 个全部需要"做空余额（short interest level, 未平仓）"**，而本集 4 个字段**全是成交流量**（description 全部写 shares traded / sold short）。
⇒ **本集与类别卡 5 个原语 0 个直接匹配**，只能做"做空流量/压力"这一类。
这与「数据集的 category 是 shortinterest」不矛盾——category 是塔位归属（×1.1），不是机制清单。
**不要**因为塔是 shortinterest 就套用 squeeze / days-to-cover 骨架：那需要 `shortinterest3`（借券）或 `shortinterest29`（做空量+规模）的字段，
在本集里写出来会因字段不存在被 `preflight_expressions` 拦下。

---

## §5 三方对账：类型 / 覆盖 / 语义

### 5.1 类型对账 —— **一致，且本集无 VECTOR**

| 来源 | 结果 |
|---|---|
| 平台 `get_datafields` | 4/4 **MATRIX**（无 VECTOR / GROUP） |
| 本地 `get_field_catalog(USA, us_short_sale)` | `data_type: MATRIX`，4/4 MATRIX |
| 本地 `query_field_profile` | `field_type = MATRIX` × 4 |

**结论：无矛盾。** 由此得两条操作性结论：
① 本集**不存在 VECTOR 字段** ⇒ 不需要 `vec_avg` / `vec_sum` 之类的降维包裹，AGENTS 里"VECTOR 必须 vec_* 归约"的规则在本集**不适用**；
② 四个字段都是 MATRIX ⇒ 直接进表达式，**不要**加 `vec_*` 包裹（加了会因入参类型不符被 preflight 拦）。

### 5.2 覆盖 / 拥挤度对账 —— **覆盖率一致，拥挤度三方不一致（本地严重陈旧）**

| 指标 | 平台 `get_datafields` | 本地 `get_field_catalog` | 数据集级 `get_datasets` | 判定 |
|---|---:|---:|---:|---|
| `aggregate_executed_trade_share_count`.cov | 1.0 | 1.0 | 1.0（集级） | ✅ 一致 |
| `executed_short_trade_share_count`.cov | 1.0 | 1.0 | — | ✅ |
| `reported_short_sale_share_quantity`.cov | 1.0 | 1.0 | — | ✅ |
| `reported_total_trade_share_quantity`.cov | 1.0 | 1.0 | — | ✅ |
| **alphaCount** | **223 / 218 / 126 / 131** | **36 / 37 / 30 / 32** | **356** | ⚠ **三方不同，见下** |
| userCount | 129 / 124 / 74 / 76 | 25 / 26 / 20 / 22 | 189 | ⚠ 本地陈旧 |

**alphaCount 三个数字为什么不同（不是错误，是口径）**：
- **字段级之和 ≠ 数据集级**：223+218+126+131 = **698** > 集级 **356**。比值 698/356 = **1.96**
  ⇒ 平均每个 alpha 用了约 **1.96** 个字段，与本集"分子+分母成对出现"的结构完全吻合。
  **引用拥挤度时必须说明用哪个口径**：判"字段被多少人用过"用字段级，判"这个集被多少 alpha 碰过"用集级。
- **本地 catalog 陈旧**：36/37/30/32 是旧快照（约实况 16–17%）。同一次快照里 `updated_at = 2026-10-25 23:30:45`（`query_field_profile`）。
  ⇒ **禁止用本地 catalog 的 alphaCount 判拥挤度**；本文件一律用平台实数。
  （历史文档也印证增长：`_usa-shortinterest-dataset-scan-20261019.md:15` 记本集 aC=224，today 356。）

### 5.3 语义对账 —— **字段级语义无冲突；3 处派生冲突已定位**

字段级（description 是唯一语义来源）：4 条描述两两成对、互相自洽：
- `executed_short` ⊆ `aggregate_executed`（同为 "regular trading hours" 口径）
- `reported_short` ⊆ `reported_total`（同为 "across all included markets" 口径）
- 两对之间的差别是**市场覆盖口径**，**不是时段**（两者都写 regular hours 或未写时段）⇒ 这条区分在字段名里看不出来，
  只能从 description 读出。**任何"executed 是盘前、reported 是盘中"之类的解读都是错的。**

派生冲突（都不影响字段语义，但会误导下游）：

**(a) 历史文档把本集字段"代称"成了别的名字。**
`_usa-shortinterest-dataset-scan-20261019.md:39-45`（族 B）把本集说成 "`short_shares / total_shares`（executed 与 reported 两套配对）"，
并给出 aC 范围 "85–167"。**平台实际字段名与 aC 都与之不同**（实为 4 个长名 + aC 126–223）。
⇒ 引用该扫描的"结论"可以，**引用它的字段名/aC 不行**。

**(b) 本地自动语义分类自相矛盾。**
`query_field_profile` 里 `reported_short_sale_share_quantity` 的 `semantic_family = 其他`，
另三个是 `价量与波动`，而 `sem_type` **全为 NULL**（AGENTS 记录：`load_field_profiles_to_db.py` 建库时 sem_type 全 NULL）。
同一经济量的 4 个字段被分进 2 个族 ⇒ 该分类**不能作为族归并依据**；本文件的 §4 是按"分子/分母 × 口径"手工归并的。

**(c) 本地 `freq_hint` 是无信息占位符。**
4 个字段的 `freq_hint` 全是 **"快照（按库表更新，需实测）"**，与平台 description 的日频口径不一致。
⇒ **不能引用 `freq_hint` 当频率**；本文件 §3 的频率是 description + 实证反推，并已标注"平台元数据无 frequency 字段"。

**(d) ⚠ 幽灵字段风险（必须记一笔）：`short_sale_executed_share_quantity` 不是本集字段。**
该名出现在历史 candidates 与 `expressions` 表（wave 341 / mcp-20261108 共 9 条），**但它是 `institutions20` 的字段**：
`get_datafields(institutions20)` 的 17 字段里含 `short_sale_executed_share_quantity`、
`overall_executed_trade_share_amount`、`exempt_short_trade_share_total`、`short_exempt_transaction_share_count`、
`aggregate_trade_share_count_regular_hours`、`executed_short_position_share_sum`、`inst20_{sq,yx,ra}_{sv,tv,sev,market}`。
**它是同一套 FINRA 做空成交数据、但按申报设施拆分的版本**（`inst20_sq_*` = FINRA/Nasdaq TRF Carteret，
`inst20_yx_*` = FINRA/NYSE TRF）。
⇒ 拿"历史 ds=us_short_sale 的记录"推断"executed 口径已在本集测过"会错；本集与 institutions20 是**同源不同粒度**的两个集（§9 G6）。

### 5.4 对账结论一句话

**类型一致（4/4 MATRIX、无 VECTOR）、覆盖一致（4/4 = 1.0）、字段级语义自洽**；
不一致全部落在**下游派生层**：本地 alphaCount/userCount 陈旧（禁用）、本地 semantic_family 自相矛盾（禁用）、
本地 freq_hint 占位（禁用）、历史文档字段名与 aC 过时（结论可用、名称不可用）、
以及 `short_sale_executed_share_quantity` 属 institutions20 而非本集（幽灵字段风险）。

---

## §6 已实测证据（全部为本会话从本地库 / 平台直读，不是转述）

### 6.1 本集 4 臂（2026-11-15，`expressions.wave = mcp-20261115`，`dataset` 列为 NULL）

来源：`data/wqb.db::expressions` id 108928–108931 + `alphas`（只读 SELECT，脚本 `logs/_tmp_uss_alpha_evidence.py`），
指标经 `batch_get_alpha_metrics` 复核（4/4 success，`prescreen = REJECT`）。

| alpha | 表达式（节选） | S | F | 2Y | SUB | TO | **invest 比** | failed_RA |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| `xAvQ2LYN` | `group_rank(ts_mean(divide(executed_short, aggregate_executed), 22), subindustry)` | **−0.83** | −0.39 | −1.02 | −0.47 | 0.0648 | 0.8675 | 4 |
| **`RReYlOVz`** ★ | **`reverse`** 同式 22d | **0.84** | 0.39 | **1.02** | 0.48 | **0.0648** | **0.8571** ✓ | 3 |
| `wpo1GoRv` | reverse 66d + `tail(0.15/0.85)` | 0.48 | 0.17 | 0.84 | 0.34 | **0.0368** ⚠ | **0.4792** ✗ | 3 |
| `qM7dG7lK` | reverse 126d | 0.54 | 0.20 | 0.99 | 0.49 | **0.0231** ⚠ | 0.8519 ✓ | 3 |

判读（三条都可复核）：
1. **方向可信**：`−0.83` / `+0.84` 严格对称（同一表达式加不加 `reverse`）⇒ 符号是信号本体，不是噪声。
2. **强度不足**：最好 0.84，距 Mode B 的 1.25 差 0.41、距提交线 1.58 差 0.74；三个窗口全低于 1.0。
3. **两个新坑（本集特有）**：
   - **`tail` 版本把 invest 比打到 0.4792**（0.8571 → 0.4792）⇒ 在本集，`tail` 不是"白送 2Y"的杠杆，它会顺手废掉可投资性
     （对比 earnings 语气族 `tail` 把 2Y 从 1.03 抬到 1.95–2.39，见 `tracking/USA/runs/usa_campaign_ledger_20261114.md:3-20`）。
   - **慢窗把 TO 压到区域评审地板以下**：`qM7dG7lK` TO 0.0231、`wpo1GoRv` 0.0368，而本区 `review.turnover_min = 0.05`
     ⇒ 即便 S 提上来，这两条也过不了区域评审口径（平台 `LOW_TURNOVER` limit 0.01 是另一回事）。

### 6.2 更早的两次记录（口径不同，不可与本表直接混比）

| 时间 | 记录 | 读数 | 口径差异 |
|---|---|---|---|
| 2026-10-19 | `_usa-shortinterest-dataset-scan-20261019.md:39-45` 族 B「实测 4 条」 | S **0.05 / 0.04 / −0.65 / 0.05**，margin 仅 **0.06 bp** ⇒ 判"纯噪声" | 4 条的具体表达式/字段未落盘，无法复现 |
| 2026-08 | `alpha-inspiration-usa-d1-shortinterest-insiders.md:19,33` executed 比率 | S **1.25 / 1.28**（`quantile(ts_backfill(ratio,60))` + 外层 `quantile`/`group_rank`；decay 8、trunc 0.04） | 该文件自述「2026-08 历史提炼，**未按现行流程复核**」（`:5`） |

**⚠ 这两条与 §6.1 构成未解冲突**：同一个 executed 做空占比机制，2026-08 记 1.28、2026-11-15 实测 0.84（差 0.44）。
已知差异：外层用 `quantile` vs `group_rank(ts_mean(·,22))`、`ts_backfill` vs 无、decay 8 vs 未记录、trunc 0.04 vs 0.08。
**在统一设置下复跑一次之前，不得引用 1.28 作为该机制的天花板**（缺口 G4）。这也是本文件**不写"天花板 = 0.84"** 而写
"已测最好 = 0.84" 的原因——`usa_campaign_ledger_20261114.md:558` 里的 "0.84 即天花板" 是**同口径内**的结论，
跨口径不成立。

### 6.3 跨集旁证：institutions20 同源族（wave 341 / mcp-20261108，共 5+4 条重复登记）

`expressions` 表 id 99610–99614 / 99601–99606，字段是 **institutions20** 的 `short_sale_executed_share_quantity` 等：
读数 **S = 0.03 / 0.28 / −0.08 / −0.02 / −0.04**（`alphas` 表，2026-11-08）。
⇒ **同源数据的另一个切法（按设施拆分）同样读不出强度**，与 §6.1 的 0.84 方向一致：**做空成交流量这个信息面本身弱**，
不是本集独有的问题。这条旁证把"数据集不行"与"信息面不行"区分开了（归因需要）。

---

## §7 「近十年」闸实测（`get_alpha_yearly_stats`，本会话真跑）

对象：`RReYlOVz`（§6.1 的 0.84 臂），IS 窗口 2013-01-01 → 2023-12-31。

| 年 | longCount | shortCount | pnl | S | TO |
|---|---:|---:|---:|---:|---:|
| 2014 | 1513 | 1519 | +361,275 | 1.29 | 0.0704 |
| 2015 | 1535 | 1536 | +339,018 | 1.30 | 0.0639 |
| 2016 | 1531 | 1532 | +425,624 | 1.28 | 0.0621 |
| 2017 | 1514 | 1518 | +96,553 | 0.46 | 0.0606 |
| 2018 | 1521 | 1527 | +84,027 | 0.33 | 0.0603 |
| **2019** | 1514 | 1523 | **−204,696** | **−0.61** | 0.0667 |
| 2020 | 1514 | 1520 | +302,147 | 0.85 | 0.0726 |
| 2021 | 1544 | 1545 | +526,765 | 1.35 | 0.0684 |
| 2022 | 1544 | 1545 | +688,803 | 1.65 | 0.0629 |
| 2023 | 1548 | 1556 | +102,038 | 0.26 | 0.0608 |

**判定（按 `output_report/USA_regular_alpha_delivery_20261114.md:204-226` 的逐年判据 `longCount>0 && shortCount>0 && pnl>0`）**：

- **覆盖 10/10 年**（2014–2023），每年 longCount 与 shortCount 都在 **1513–1556** 的窄带里（≈全宇宙一半多头一半空头）
  ⇒ **数据在本集上是连续有持仓的，不存在 earnings 族那种"前 4 年完全空仓"的形态**。这是本集的强项。
- **pnl>0 只有 9/10 年**：**2019 年 −204,696（S −0.61）** ⇒ 按该闸的严格口径，**本臂不满足「逐年 pnl>0」**。
- **2013 年无任何年度记录**（IS 起点是 2013-01-01）⇒ 有效年份按 2014 起算共 10 年，"近十年"= 2014–2023。
  **不要**把它写成"2013 起 11 年"。

⇒ 一句话：**「有数据」这条 10/10 过；「逐年都赚」这条 9/10 不过（2019 年）。**
后续任何候选都必须在自己身上重跑这条闸（不同骨架的 2019 表现会不同，本表只证"数据覆盖十年"，不证"信号十年都赚"）。

---

## §8 判死六维穷尽闸现状（AGENTS §7.6）

**结论先行：D1 / D2 / D3 三维不满足 ⇒ 本集只能记 `PROVISIONAL`（探针级判弱），不得终判死、
不得作为邻接 shortinterest 集（`shortinterest29` / `shortinterest43`）的先验依据。**

| 维 | 要求 | 本集现状 | 判定 |
|---|---|---|---|
| **D1 结构互异模板** | ≥10 个（不同经济机制/算子几何） | 已测/已落盘：①22d `ts_mean` 反向比率 ②66d+`tail` 反向 ③126d 反向 ④reported 比率的 zscore+多 decay 网格（`prod19`/`prod19b`，实为同骨架换窗/换 decay）⑤`ts_rank` 变体 ⑥`ts_delta` 动量变体 ⑦归一化比率倒数。**粗算 ≤7，且多数未在现行设置下复跑** | ❌ 未达 10 |
| **D2 字段族自测** | 每族 ≥1 条实测 | F1 ✅（3 臂）、F2 ✅（历史骨架，无及格读数）、**F3 ❌（单腿从未测）**、**F4 ❌（0 条）** | ❌ |
| **D3 矩全家** | 水平 / 一阶差 / 二阶波动 / 比值或信噪比 各 ≥1 | 水平 ✅（比率/秩）、一阶差 ✅（`ts_delta` 模板）、比值 ✅（比率本身 + `ts_mean(5)/ts_mean(66)` 在 institutions20 测过，本集未测）、**二阶波动 ❌（无任何记录）** | ❌ |
| **D4 分组轴** | ≥2（subindustry / industry / sector / market / bucket） | subindustry ✅（2026-11-15 四臂）、industry ✅（`prod19` `a19_ss_ratio_ind`）、market ✅（`a19_ss_ratio_mkt`）、sector 部分（inspiration 模板 2 变体）、bucket ❌ | ✅ |
| **D5 非线性** | ≥1（signed_power / ts_rank / ts_quantile / trade_when / bucket） | `signed_power(...,0.8)` ✅（`prod19` `a19_ss_ratio_sp08`）、`tail` ✅（2026-11-15）、`ts_rank` ✅ | ✅ |
| **D6 配置** | ≥2（宇宙×中性化×decay 至少变一维） | decay 5/22/66/126/252 ✅、中性化 SUBINDUSTRY vs INDUSTRY ✅、trunc 0.08 vs 0.04 ✅（宇宙恒 TOP3000，纪律要求） | ✅ |

**与台账的一致性**：`tracking/USA/runs/usa_campaign_ledger_20261114.md:566` 已写「探针级判弱（**非终判死，D1–D6 未穷尽**）」，
本表把这句话落到维度上：**缺的是 D1（结构数）、D2（F3/F4 未测）、D3（二阶波动）**，不是"信号已被证伪"。

---

## §9 开放缺口（按"开下一波前必须先清"排序）

| # | 缺口 | 现状 / 为什么是缺口 | 关闭动作 |
|---|---|---|---|
| **G1** | **prod 从未测** | 4 臂的 `prod_correlation` 全 null（`batch_get_alpha_metrics`）；`-m wqb.profiles explain` 的类别证据也记 `prod 已测 0`。**prod ≥0.7 是不可豁免红线**，prod 未知 ⇒ 连"能不能提交"都无从谈起 | `check_correlation(alpha_id, refresh=False)` 只走 MCP（禁脚本直连）；先对 `RReYlOVz` 取一次（48h 缓存优先，`docs/experience/01_platform_gates.md:120-126`）。⚠ prod 端点单账号单并发，取数前确认没有别的会话占槽 |
| **G2** | self-corr 从未测 | 4 臂 `self_correlation` 全 null | `check_self_correlation`（MCP），并核 `full_os_pool_size` |
| **G3** | 机制未登记 | `tracking/USA/reference/usa_dataset_mechanisms.md` 里**没有 `us_short_sale` 条目**；P0-4 要求机制归属登记（含 `classic_anomaly`），否则 S0 选集排序缺一层 | 追加一条：`mechanism = "日频做空成交占比（FINRA Reg SHO 日报流量，非余额）"`，`classic_anomaly` 需给出可引用文献后才能填 `true`；**现在没有可引用文献 ⇒ 如实填 `false` 并写明理由** |
| **G4** | 口径冲突未解（1.28 vs 0.84） | §6.2：2026-08 记 1.28，2026-11-15 实测 0.84，设置不同 | 统一到 `explain` 的生效设置（SUBINDUSTRY/decay 5/trunc 0.08），**同批 2 条**发 `quantile+backfill60` 版与 `group_rank+ts_mean22` 版（`create_multi_simulation` 每批恰好 2 条） |
| **G5** | F3 单腿未测（H3） | 见 §4 F3 | 1 条裸探针（字段 → 单一 `rank`），同时取 `risk_neutralized_sharpe` |
| **G6** | 与 institutions20 的同源关系未量化 | 两集是同一 FINRA 做空成交数据的不同粒度（§5.3(d)）；已各自有臂，但**互相关从未算过** | 若两集都继续挖，先 `compute_mutual_correlation`（同机制跨集自相关是 self 墙的高发区） |
| **G7** | 字段级数值分布未测 | 本会话只有形态学判定，没有 median/偏度/零值率/越界率（`executed_short ≤ aggregate_executed` 是否恒成立**未验证**） | 走 `alpha-template-labs-data-analysis`（BRAIN Labs 原始数据分析）；或在 1 条探针后读 `get_record_set_data` |
| **G8** | 幽灵字段 | `short_sale_executed_share_quantity` 属 institutions20，不属本集（§5.3(d)） | 下发前必跑 `preflight_expressions`（字段存在性），本文件不替代该检查 |

---

## §10 一句话总账

`us_short_sale` = **4 个 MATRIX 字段、覆盖率 1.0、全量取回无截断、无 VECTOR** 的 FINRA 日频**做空成交流量**集（做空塔 ×1.1、aC 356）。
它**没有**做空余额，所以 shortinterest 类别卡的 5 个原语一个都用不上；能做的是"做空成交占比"这一个机制的两个口径（F1 executed / F2 reported）
加一个**从未被任何人测过**的双口径背离（F4）。
已测最好读数 **0.84**（22d 反向，2Y 1.02、invest 比 0.857 ✓、TO 0.0648 合规、failed_RA 3），
覆盖 10/10 年但 2019 年 pnl 为负；prod 与 self **都未测**。
按判死六维，**D1/D2/D3 未达 ⇒ PROVISIONAL 判弱，不得终判死、不得外推到同类别其它集**。

---

## §11 引用源（本文件每条外部结论的出处）

| 用途 | 位置 |
|---|---|
| 类别卡 / 生效设置 / 阈值 / 可投资性闸 | `Claude/skills/wq-brain-ra-usa/references/shortinterest.md`（cell-panel 块）、`Claude/skills/wq-brain-ra-usa/SKILL.md:98-103` |
| 预注册判据（裸探针 / prod 探针 / risk-neut 口径 / aC<200 低拥挤） | `Claude/skills/wq-brain-ra-usa/references/_usa-field-profile-playbook-20261018.md:15,17,24-31,146,192` |
| 开波前探针与判死分级（D15 fast_kill 只到字段级） | `Claude/skills/wq-brain-ra-usa/SKILL.md:90,142,145` |
| 本集历史判死叙事（族 B，字段名为代称、aC 已过时） | `Claude/skills/wq-brain-ra-usa/references/_usa-shortinterest-dataset-scan-20261019.md:3-5,15,39-45,72` |
| 2026-11-15 四臂读数与"D1–D6 未穷尽" | `tracking/USA/runs/usa_campaign_ledger_20261114.md:550,558,566` |
| 2026-08 executed 比率 1.28（未按现行流程复核） | `Claude/skills/brain-alpha-research/references/alpha-inspiration-usa-d1-shortinterest-insiders.md:5,16-19,33` |
| 分母决定横截面基准（F3 只当分母的依据） | `docs/experience/02_signal_patterns.md:449-486` |
| 判据 B（max S < 1.58 出局）/ 裸探针 |S|<0.5 kill | `docs/experience/03_region_dataset.md:294-296` |
| 近十年闸的逐年判据与空仓年前置 | `output_report/USA_regular_alpha_delivery_20261114.md:204-226` |
| prod 端点机制 / 48h 缓存 / 单并发 | `docs/experience/01_platform_gates.md:114-141` |
| prod 红线常量 / 窗口白名单 | `src/wqb/config.py:502`、`src/wqb/config.py:656` |
| 本集是否在判死清单（**不在**；`shortinterest29` 在） | `tracking/USA/reference/usa_dead_datasets.md:67`（`shortinterest29` 条），本集无条目 |
| S0 扫描把 short sale 日频量排到 P5（institutions20） | `tracking/USA/reference/usa_s0_dataset_scan_20261114.md` §2 候选表 P5 行 |
| 本集的覆盖度审计结论（TESTED / 证据命中 2 字段） | `data/dataset_assets/USA_shortinterest_coverage_audit_d1.json`、`reports/dataset_experience/usa_shortinterest_coverage_audit_20261115.md` |

## §12 本会话实际执行过的检查（可复核清单）

| 检查 | 命令 / 调用 | 结果 |
|---|---|---|
| 全量字段（无抽样） | `get_datafields(USA, TOP3000, delay=1, dataset_id=us_short_sale, filter_sharpe=false)`（未设 `max_fields`） | `count=4 == platform_count=4`，`complete=true`，`pages_fetched=1` |
| 数据集元数据与同类别分母 | `get_datasets(USA, TOP3000, delay=1, category=shortinterest)` | 6 集；本集 fieldCount 4 / aC 356 / cov 1.0 / ×1.1 |
| 本地 typed catalog | `get_field_catalog(USA, us_short_sale)` | 4 字段 MATRIX，aC 36/37/30/32（陈旧） |
| 本地字段画像 | `query_field_profile(region=USA, dataset=us_short_sale)` | 4 行全 `UNTESTED`、`n_tests=0`（**与 §6 的 4 臂冲突，因 MCP 直连仿真不写该表**） |
| 生效设置 | `world-quant-brain-mcp/.venv/Scripts/python.exe -m wqb.profiles explain --region USA --dataset us_short_sale` | SUBINDUSTRY / decay 5 / trunc 0.08；review TO∈[0.05,0.30]；invest 闸在锁定项 |
| 4 臂读数 + invest 比 | `batch_get_alpha_metrics(["RReYlOVz","xAvQ2LYN","wpo1GoRv","qM7dG7lK"])` | 4/4 success，`prescreen=REJECT`，invest 比 0.8571 / 0.8675 / 0.4792 / 0.8519 |
| 近十年 | `get_alpha_yearly_stats("RReYlOVz")` | 2014–2023 共 10 年，lc/sc 1513–1556 全 >0，2019 pnl<0 |
| 同源旁证集 | `get_datafields(USA, TOP3000, delay=1, dataset_id=institutions20, filter_sharpe=false)` | 17 字段含 `short_sale_executed_share_quantity` 等（即 §5.3(d) 的幽灵字段来源） |
| 历史臂与幽灵字段 | `python -I logs/_tmp_uss_alpha_evidence.py`（只读 SELECT：`alphas` / `expressions`） | 9 条 alpha、14 条 expression；确认 4 臂 wave=`mcp-20261115` 且 `dataset` 为 NULL |
| 覆盖度审计（并行会话产物，本会话只读其结论） | `data/dataset_assets/USA_shortinterest_coverage_audit_d1.json` | `status=TESTED`、`evidence_hit_n=2`、`in_db_evidence=false`、`probe_status=null` |
| skill 镜像漂移基线 | `world-quant-brain-mcp/.venv/Scripts/python.exe tools/sync_skills.py --check` | 5/5 安装位一致（**本文件落盘前**的基线） |

| 母本↔镜像一致性 | `md5sum` 两侧 | 同版本两侧相同（逐字一致） |
| skill 镜像同步 + 复验 | `… tools/sync_skills.py` → `… tools/sync_skills.py --check` | 已同步 5 个文件 / 5 个安装位；复验 5/5 一致 |

**未执行（如实登记）**：本次**未派发任何仿真**（0 仿真配额消耗）、**未查 prod / self 相关性**（G1/G2）、
**未测字段数值分布**（G7）、**未跑 `preflight_expressions`**（本文件不派发表达式）。
