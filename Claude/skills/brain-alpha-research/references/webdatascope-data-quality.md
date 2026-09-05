# WebDataScope 数据包驱动的数据集/字段质量预筛与中性化选择

来源：WebDataScope-1.3.1 插件（幻华，2026-08-02 发布；2026-08-05 更新，zip 在 `wqb-share-03/WebDataScope-1.3.1.zip`，解压目录 `wqb-share-03/WebDataScope-1.3.1/`）+ 离线数据包 `WebData_20260219_V0.10.9.zip`（数据包与插件版本解耦，格式不变）。
数据包为 zlib + msgpack 编码，导入后存入插件 IndexedDB（`WQP_Extension_Data_Files`）。以下规则在挖矿 research 阶段作为**零成本预筛**使用（不消耗模拟额度）。注：本档规则转写自 1.0.6，2026-08-05 已核对 1.3.1 源码（`src/background/background.js:270` 的 `getAlphaCheckStates` failed-count 门禁逻辑保留，规则一致；插件 1.3.1 新增 alpha 描述助手/社区帖标记/prod memo/会话保活等扩展功能，不影响离线预筛规则）。

## 数据包结构（实测）

- `data/oth/osis_data.bin`（39KB）— **OS-only 快照**。每 `<REGION>_<DELAY>`：`{mean, sub_beg_time, sub_end_time, total_count, dataset, category}`。USA_1 窗口 2022-02-05 → 2025-10-18，510,573 alpha，338 dataset / 12 category。每条目 `{count, sharpe_ratio, fitness_ratio}`。**无 datafield、无 neutralization**。OS = 提交后已积累足够样本外的 alpha 子集，是更"真实"的样本外质量度量。
- `data/oth/info_data.bin`（14.8MB）— **IS+OS 完整快照**（插件实际消费的主文件，`dataStore.js` 的 `REQUIRED_FILES`）。每 `<REGION>_<DELAY>`：`{sub_beg_time, sub_end_time, isos, neutralization}`。USA_1 窗口 2022-02-05 → 2026-02-17，901,969 alpha。
  - `isos`: `{mean, total_count, dataset, datafield, category}`，每条目 `{count, sharpe_ratio, fitness_ratio}`。dataset 350 / datafield 39,910 / category 16。
  - `neutralization`: `{mean, dataset, datafield, category}`。`mean[<NEUT_KEY>]` 与每条目均为 `{count, sharpe_ratio, osis_count, fitness_ratio}`（**`osis_count` = 该格的 OS 子集样本量**，是中性化推荐可信度的关键阈值字段）。
- `data/<dataset>_<REGION>_<UNIVERSE>_Delay<N>.bin` — 该数据集**每字段 10 年（2012–2021）原始数据体检**。每字段含：`year` / `LongCount` / `ShortCount` / `Coverage` / `CoverageRatio` / `PositiveValues` / `NegativeValues` / `IndicativePositiveRatio` / `IndicativeNegativeRatio` / `IndicativePositiveNegativeRatio` / `IntegerStatus` / `absValueBetween1and0ratio` / `skenewss` / `kurtosis`（**均为 10 元素年度列表，取均值用于整体判定**）/ `frequency`（daily/weekly/monthly/quarterly）/ `yearly_distribution`（10 年分位直方图字符串）。
- `data/dataSetList.json` — 160 个 `<dataset>_<region>_<universe>_Delay<N>` 条目，标记哪些组合有逐字段体检数据。覆盖：USA_TOP3000×112、EUR_TOP1200×19、CHN_TOP3000×12、ASI_MINVOL1M×6、GLB_TOP3000×5、JPN_TOP1600×2、KOR_TOP600×1 等。

## 规则 1 — 数据集质量先验（"极少有人提交 = 低质量"的量化版）

按目标 region_delay 取 `isos.dataset` 排名：

| 提交量 count | 判定 | 动作 |
|---|---|---|
| < 50 | 社区未验证，质量风险高 | 默认跳过；仅作刻意去相关的探索性尝试 |
| 100 – 3000 且 sharpe ≥ 1.1×区域均值 | **甜点区**：已验证可提交、未饱和 | 优先入围（ProdCorr 死区风险低） |
| > 30000 | 饱和（模板空间被社区挖穿） | 需高度非对称结构才能过 ProdCorr<0.7，冷启动避开 |
| 任意 count 但 sharpe 明显低于区域均值 | 社区大量尝试仍拿不到好结果 | 跳过（如 USA_1 的 fundamental2: 29784 次 / sharpe -0.003 / fitness -0.026） |

USA_1 参考值：`isos.mean` sharpe 0.358 / fitness 0.353；甜点区示例（2026-02 数据）：`macro38(0.539)`、`other566(0.799)`、`other696(0.664)`、`risk65(0.645)`、`sentiment21(0.568)`、`institutions10(0.559)`、`news54(0.550)`、`risk88(0.540)`、`earnings1(0.535)`、`sentiment22(0.532)`、`model38(0.481)`、`model135(0.437, REVERSION_AND_MOMENTUM 下 0.876)`。USA_1 共 46 个数据集 count<50（如 fundamental92/pv68/earnings11/other507）。

## 规则 2 — 类别级先验（数据集样本不足时的上一级回退）

`isos.category` 与 `osis_data.bin.category` 给出 16 个 dataCategory（analyst/fundamental/news/sentiment/...）的聚合 count/sharpe/fitness。用途：(a) 冷启动选方向时按类别 sharpe 排序挑高潜力类别；(b) 当某数据集 `count<50` 无法直接判定时，回退到其类别均值作弱先验；(c) `neutralization.category[<cat>][<NEUT>]` 给出该类别在各中性化下的表现，样本量远大于单数据集，可作中性化选择的稳健回退（见规则 3 第 5 条）。

## 规则 3 — 中性化选择（数据驱动，替代盲扫）

1. **全局排序**用 `neutralization.mean[<NEUT>]`（USA_1 实测）：`STATISTICAL(0.461) > SUBINDUSTRY(0.424) > INDUSTRY(0.358) > FAST(0.350) > SLOW(0.347) > CROWDING(0.333) > NONE(0.280) > MARKET(0.235) > SECTOR(0.232) > REVERSION_AND_MOMENTUM(0.229) > SLOW_AND_FAST(0.222)`。
2. **但每个数据集的最优中性化差异巨大**——先查 `neutralization.dataset[<ds>]`，把 sharpe 最高的 2-3 个中性化排进模拟计划前列。**可信度阈值：`count ≥ 20` 且 `osis_count ≥ 20`**（OS 子集样本量，比纯 IS count 更可靠）。示例：`other696→SECTOR`、`insiders3→SLOW(0.755)`、`model38/model135→REVERSION_AND_MOMENTUM`、`pv87→SECTOR/INDUSTRY`、`macro38→STATISTICAL(0.68)`。
3. **字段级细化**：`neutralization.datafield[<field>]`（`count ≥ 5`）进一步收窄；当数据集级样本不足但字段级充足时以字段级为准。
4. **类别级回退**：数据集级与字段级样本都不足时，用 `neutralization.category[<cat>][<NEUT>]`（样本量通常上万）。
5. **risk-neut 遍历规则**（源自 `background.js:327` 注释）：用传统中性化回测时，结果页会有一条 risk-neutralized 曲线；若该曲线的 sharpe 和 fitness 都明显更高，说明信号的超额来自风险因子剥离，应把 risk-based 中性化（SLOW/FAST/CROWDING/STATISTICAL/REVERSION_AND_MOMENTUM 等）纳入遍历。

## 规则 4 — 字段级预筛（原始数据体检 → 预处理决策）

来自 `<dataset>_<REGION>_<UNIVERSE>_Delay<N>.bin` 的逐字段档案（10 年列表取均值）：

| 观测 | 含义 | 动作 |
|---|---|---|
| `CoverageRatio` 均值 < 0.4 | 覆盖不足 → 集中持仓风险（CONCENTRATED_WEIGHT） | 必须 `ts_backfill`/`group_backfill`，否则弃用 |
| `CoverageRatio` 早年低、近年高（厂字形覆盖） | 数据供应商中途扩容 | 回测解读时注意早年年份失真，稳健性判定用近 3 年 |
| `IndicativePositiveRatio` ≈ 1（单边字段） | 原始值恒正（如估值、量） | 不要直接用原始水平做多空信号；先做变化率/横截面排名/与基准差 |
| `IndicativeNegativeRatio` ≈ 1 | 原始值恒负（如负债、亏损） | 同上，先做变化率/排名 |
| `IndicativePositiveNegativeRatio` 极端（×10000 缩放） | 正负值严重不对称 | 对称化处理（减均值/双序 rank）后再入组合 |
| `LongCount`/`ShortCount` 严重失衡 | 多空样本不对称 | 检查是否需要 `signed_power`/双 rank 平衡 |
| `IntegerStatus` = 1（离散值） | 评分/等级/计数类字段 | 慎用平滑类算子；优先 `rank`/`bucket`/`group_rank`；`ts_delta` 会产生稀疏跳变 |
| `yearly_distribution` 高度集中于单一分位段 | 分布极偏或截尾 | 先 `winsorize`/`rank`/`zscore` 再进入组合结构 |
| `frequency` = monthly/quarterly | 更新频率低 | 时序窗口 ≥ 更新周期（月度 ≥21d，季度 ≥63d），短窗只采样噪声；换手天然低，适合低换手轨道 |
| `skenewss`/`kurtosis` 年度均值高 | 厚尾 | 外层包 `rank`/`signed_power(x, <1)` 抑制极值 |
| `absValueBetween1and0ratio` ≈ 1 | 值域集中在 [-1,1] | 已是比率/标准化字段，避免再除以波动类归一化 |

## 规则 5 — 字段使用先验（与 get_datafields 的 alphaCount 互补）

`isos.datafield[<field>]` 给出每字段的社区提交 count/sharpe/fitness。与平台 `get_datafields` 的 `alphaCount` 口径互补（数据包是离线快照+含 sharpe/fitness 质量维度）。用法：**从高 count 高 sharpe 字段起步**；count 高但 sharpe 低的字段（如 `sharesout` 40243 次 / 0.219）说明社区大量踩坑，避免作主信号。

## 规则 6 — OS 质量交叉验证（防 IS 过拟合）

`osis_data.bin` 给出 OS-only 的 dataset/category 级 sharpe/fitness（窗口较短，仅含已积累样本外的 alpha）。对规则 1 的甜点区候选，**交叉对比 `osis_data.bin[<key>].dataset[<ds>].sharpe` 与 `info_data.bin[<key>].isos.dataset[<ds>].sharpe`**：若 OS sharpe 明显低于 IS+OS sharpe（如差距 >0.15），说明该数据集的 alpha 在样本外退化，IS 表现含过拟合，降低优先级或要求更强鲁棒性证据。`neutralization.*.*.osis_count` 同理——`osis_count` 远小于 `count` 的中性化格意味着大部分提交尚无 OS 数据，推荐可信度打折。

## 规则 7 — 快照新鲜度与覆盖矩阵

- 每条 region_delay 记录都有 `sub_beg_time`/`sub_end_time`：引用任何数值时附带窗口（如 "USA_1 2022-02-05→2026-02-17, 901,969 α"），让下游判断先验是否过时。网盘发布新版数据包后重跑 `tools/webdata_quality.py` 刷新。
- 用 `dataSetList.json` 在挖矿前确认目标 `<dataset>_<region>_<universe>_Delay<N>` 是否有逐字段体检数据（共 160 个组合，USA_TOP3000 覆盖 112 个）。**缺失时**：插件 `dataFlag.js` 会按 `<ds>_<region>_*_Delay<N>` 前缀回退到同 region 其他 universe 的体检数据（UI 标 ☆☆☆）。挖矿中可作粗略代理，但 universe 特定覆盖差异需在实际 `get_datafields` 的 `coverage` 上复核。

## 规则 8 — OS 选择性偏差与退化识别（OS-only 快照的正确解读, 2026-08-01 新增）

`osis_data.bin` 只含**已提交且积累了样本外数据的 alpha**。因此 OS sharpe 普遍**高于** IS+OS sharpe（提交本身是选择——只有通过了筛选的 alpha 才进 OS），这是正常现象，不是"OS 更好"。**两种真正的信号**：

| 模式 | 含义 | 动作 |
|---|---|---|
| IS+OS sharpe 高但 OS sharpe 明显低（差 >0.15） | 数据集在样本外退化 | 降低优先级；要求更强鲁棒性证据（yearly/子宇宙归因） |
| OS 差异极大（如 model230 IS+OS 0.045 → OS 0.811） | OS 子集被少数高表现 alpha 主导，社区多数尝试失败 | 关注高规模式：小样本 caution、需要非对称结构 |
| 类别级 OS >> IS+OS（如 sentiment OS 0.654 vs IS+OS 0.224） | 该类别的 IS 表现不代表提交后表现 | 该类别用 OS 数据作为更真实的先验 |

实测（USA_1 2026-02 数据包）：
- 退化数据集：`model252/analyst55/shortinterest34/model22/option7`（样本<130，OS 显著低于 IS+OS）
- `sentiment` 类别 IS+OS 0.224 → OS 0.654（提交后反而更好）；`shortinterest` IS+OS 0.454 → OS 1.028
- `pv87` IS+OS 0.357 → OS 0.755（均值被大量未成熟提交拉低，少量高质量 alpha 驱动）

## 规则 9 — 字段分布形状解析（yearly_distribution 深度用法, 2026-08-01 新增）

`yearly_distribution` 字符串含 10 年的 `(分位段, 频率)` 直方图（格式 `[{(0, 0.05): 92.377, ...}, ...]`）。除规则 4 的整体偏度/峰度外，**逐字段分布形状**直接决定预处理算子（`tools/webdata_quality.py --fields <ds>` 自动解析为 5 种形状）：

| 分布形状 | 判定条件 | 预处理建议 |
|---|---|---|
| `point_mass` | 单档占比 >90% | 近似常量/哑变量 → rank/变化率无效，检查是否事件指示器 |
| `zero_inflated` | [0,0.1) 占比 >50% | 事件/稀疏字段 → 配合 `ts_backfill` 或用事件门控（trade_when） |
| `ceiling` | [0.9,1] 占比 >50% | 值截尾 → `winsorize`/`rank`/`densify` 抑制 |
| `concentrated` | 前 3 档占比 >70% | 有效信息少 → 慎作主信号，作辅助/门控 |
| `spread` | 其他 | 直接使用或轻度预处理 |

这比只看 `skenewss`/`kurtosis` 更有指导性——例如 `zero_inflated` 字段即使偏度不高，直接 `ts_mean` 也会产生大量 0 值的主信号（有效信息被稀释）。实测 `fundamental6` 中 `revenue/liabilities/inventory_turnover` 均为 `zero_inflated`，`sales_growth` 为 `ceiling`，`operating_income/pretax_income` 为 `spread`。

## 规则 10 — 中性化可信度三级门槛（osis_count 的深度用法）

`neutralization.*.*` 每条目含 `{count, sharpe_ratio, osis_count, fitness_ratio}`。**osis_count 是 OS 子集样本量**，比纯 IS count 更有说服力（IS count 含大量未过筛的提交）。三级可信度：

| 门槛 | 判定 | 用法 |
|---|---|---|
| `count ≥ 20` 且 `osis_count ≥ 20` | 高可信 | 直接作为该数据集/字段的推荐中性化 |
| `count ≥ 5`（osis 未验证） | 中可信 | 字段级中性化推荐（`--fields` 输出），用 sharpe 排序但标注 osis 覆盖 |
| `osis_count` 远小于 `count` | 低可信 | 该格大部分提交尚无 OS 数据，推荐打折；优先参考 category 级 |

示例：`neutralization.dataset[analyst10]` 中 `NONE(2次)` sharpe 1.069 但 osis_count=1 → 不可信；`INDUSTRY(322次, osis 307)` 才是可靠推荐。

## 规则 11 — Pyramid 匹配（WQPPYS 与 MATCHES_PYRAMID, 2026-08-01 新增）

`getAlphaCheckStates`（插件 `background.js` 注入到 fetch 拦截器）会解析 `MATCHES_PYRAMID` 检查项，提取命中的 pyramid 名写入 `is.WQPPYS` 字段（如 `momentum/value`）。**Pyramid 是数据集的"高表现池"**——不同 pyramid 定义不同的字段组合/风格。用途：

1. **提交前**：`get_submission_check` 的 `MATCHES_PYRAMID` 是否命中直接决定能否提交（不匹配就是死路）；用金字塔名搜索该数据集的高质量字段组合习惯。
2. **数据包交叉**：`dataSetList.json` 只列出 160 个组合的逐字段体检；若目标 `<ds>_<region>_<universe>_Delay<N>` 缺失，用插件同款前缀回退（`dataFlag.js`: `<ds>_<region>_*_Delay<N>` 找同 region 其他 universe），但 universe 特定覆盖差异需在实际 `coverage` 上复核。

## 规则 12 — 时间窗口与回测区间选择（sub_beg_time/sub_end_time 深度用法, 2026-08-02 新增）

每条 region_delay 记录含 `sub_beg_time`/`sub_end_time`，**字段体检 .bin 也含 10 年（2012-2021）CoverageRatio 时序**。除规则 7 的新鲜度标注外：

| 信号 | 来源 | 动作 |
|---|---|---|
| IS+OS 窗口 vs OS-only 窗口长度差大 | `info_data` vs `osis_data` 的 `sub_beg_time`/`sub_end_time` | OS 窗口短 = 大量提交尚未积累样本外 → 退化判断保守 |
| 字段 CoverageRatio 早年低近年高（厂字形） | `<ds>_*.bin` 的 `CoverageRatio` 10 元素列表 | 数据商中途扩容 → 早年回测失真，稳健性判定用近 3 年（与 brain-alpha-robustness 近 3 年准则一致） |
| 字段 CoverageRatio 早年高近年低 | 同上 | 数据商弃用/缩容 → 近年信号衰减，慎用 |
| 区域 alpha 总量近 4 年 vs 早期 | `isos.total_count` 与窗口长度比 | 总量骤增 = 社区挖掘热度上升 → ProdCorr 竞争加剧 |

实测：`fundamental6` 的 `fnd6_eventv110_*` 系列字段早年 CoverageRatio=0、近年 0.02-0.43（典型厂字形）→ 2012-2015 不可用，回测从 2018 起算。

## 规则 13 — 换手率与 decay 预测（frequency + LongCount/ShortCount, 2026-08-02 新增）

字段体检的 `frequency` 与 `LongCount`/`ShortCount` 直接预测换手带与最优 decay：

| frequency | 预测换手带 | decay 建议 | 时序窗口下限 |
|---|---|---|---|
| daily | 中-高 | 0-10（短信号）或 10-60（平滑） | ≥5d |
| weekly | 中 | 0-10 | ≥5d |
| monthly | 低 | 0 即可 | ≥21d |
| quarterly | 极低 | 0 即可 | ≥63d |

`LongCount`/`ShortCount` 失衡（如 Long2873/Short2）→ 必须对称化（`signed_power`/双 rank/减均值），否则单边持仓触发 CONCENTRATED_WEIGHT 或换手异常。`IntegerStatus=1`（离散）字段用 `ts_delta` 会产生稀疏跳变 → 换手飙高，优先 `rank`/`bucket`/`group_rank`。

## 规则 14 — 截尾/Power 参数提示（skew/kurt 驱动, 2026-08-02 新增）

字段体检的 `skenewss`/`kurtosis` 直接指导 `truncation` 与 `Power` 参数：

| 观测 | 含义 | 参数建议 |
|---|---|---|
| `skenewss` 均值 | >2 | `truncation=0.04`（更紧）+ 外层 `winsorize`/`signed_power(x, <1)` |
| `skenewss` 均值 | 0.5-2 | `truncation=0.08`（默认） |
| `kurtosis` 均值 | >8（厚尾） | 外层 `rank`/`signed_power(x, 0.5)`；避免 `ts_mean` 直接平滑 |
| `kurtosis` 均值 | <3 | 正态附近，可直接用 |
| `absValueBetween1and0ratio` ≈ 1 | 已是比率/标准化 | 避免再除以波动类归一化；`truncation=0.08` 即可 |

与项目记忆中的最优参数（Power 15 + decay 60）互补：体检提供字段级先验，Power/decay 在模拟阶段二阶调优。

## 规则 15 — 自相关预测（count + sharpe 组合, 2026-08-02 新增）

`isos.dataset[<ds>]` 的 count + sharpe 组合预测 SelfCorr 与 ProdCorr 风险：

| count | sharpe | 含义 | SelfCorr/ProdCorr 风险 |
|---|---|---|---|
| >30K | 低（<均值） | 社区大量踩坑（如 USA_1 fundamental2: 29784 次 / -0.003） | ProdCorr 高（结构被挖穿），SelfCorr 高（大量相似 alpha） |
| >30K | 高（>1.5×均值） | 饱和高表现（如 pv1） | ProdCorr 高，需高度非对称结构 |
| 100-3000 | 高 | 甜点区（已验证未饱和） | ProdCorr 低（死区风险小），SelfCorr 中 |
| <50 | 任意 | 未验证 | SelfCorr 低（少有人做），但质量风险高 |

字段级同理：`isos.datafield[<field>]` count 高但 sharpe 低（如 `sharesout` 40243 次 / 0.219）→ 社区大量踩坑字段，作主信号 ProdCorr 高。优先 count 中等（100-3000）且 sharpe 高的字段。

## 规则 16 — 跨区域数据集对比（region-specific alpha 识别, 2026-08-02 新增）

同数据集在多 region 的 sharpe 差异揭示 region-specific 机会。用 `tools/webdata_quality.py --cross-region` 输出：

| 模式 | 含义 | 动作 |
|---|---|---|
| 同 ds 在 A region 高 sharpe、B region 低/负 | 该 ds 的 alpha 在 A region 有效，B region 无效 | 优先在 A region 挖；B region 避开 |
| 同 ds 在两 region 都高 | 通用信号 | ProdCorr 竞争可能跨 region，需检查 SelfCorr |
| 同 ds 在低覆盖 region（KOR/JPN/CHN）高 | 未饱和的高潜力 | 优先挖（ProdCorr 竞争小） |

实测（ASI_1 vs 其他 region, 2026-02 数据包）：
- `news29` ASI 0.597 vs EUR -0.715 → ASI 专属机会
- `model144` ASI 0.614 vs USA -0.469 → ASI 专属机会
- `pv106` ASI 0.64 vs CHN 1.462 → CHN 更优，考虑切 region

## 规则 17 — Universe 选择（dataSetList.json 覆盖矩阵, 2026-08-02 新增）

`dataSetList.json` 的 160 个组合分布极不均（`tools/webdata_quality.py` 自动输出覆盖表）：

| region_universe | 体检数据集数 | 竞争度 | 建议 |
|---|---|---|---|
| USA_TOP3000 | 112 | 最激烈 | 主战场，但 ProdCorr<0.7 难度高 |
| EUR_TOP1200 | 19 | 中 | 中等机会 |
| CHN_TOP3000 | 13 | 较低 | 未饱和，ProdCorr 友好 |
| ASI_MINVOL1M | 6 | 较低 | 同上 |
| GLB_TOP3000 | 5 | 低 | 跨区域分散 |
| JPN_TOP1600 | 2 | 极低 | 数据少但竞争小 |
| KOR_TOP600 | 1 | 极低 | 同上 |

低覆盖 universe（KOR/JPN/CHN/GLB）竞争小 → ProdCorr 风险低，但字段体检数据也少 → 需在实际 `get_datafields` coverage 上复核。

## 规则 18 — 字段组合潜力（分布形状配对, 2026-08-02 新增）

`tools/webdata_quality.py --fields <ds>` 现自动输出基于分布形状互补的 2-field 组合建议：

| 配对 | 逻辑 | 表达式骨架 |
|---|---|---|
| `point_mass`/`zero_inflated` + `spread` | 稀疏事件门控 + 连续主信号 | `trade_when(<gating>_cond, <signal>_expr, -1)` |
| `ceiling` + `zero_inflated` | 截尾 + 稀疏，分布形状互补降低结构相关 | `rank(<ceiling>_field) - rank(<zero_inflated>_field)` |
| `spread` + `spread` | 两个连续字段双 rank 去相关 | `rank(<spread_a>) - rank(<spread_b>)` |
| 多个 `concentrated` | 有效信息少 | 慎作主信号，优先作辅助/门控 |

实测（`fundamental6` USA）：`fnd6_idesindq_curcd`（稀疏）+ `cashflow`（连续）→ 事件门控候选；`fnd6_eventv110_gdwlid12`（截尾）+ `assets`（稀疏）→ 互补组合；`rank(cashflow) - rank(cashflow_fin)` → 双信号去相关。

## 规则 19 — 区域级中性化排名（neutralization.mean 逐区域差异极大, 2026-08-03 新增）

`neutralization.mean[<NEUT>]` 的**全局排序每个 region 都不同，切勿照搬 USA 顺序**。实测（2026-02 数据包）：

| region_delay | 最优中性化排名（前 5） |
|---|---|
| USA_1 | STATISTICAL(0.461) > SUBINDUSTRY(0.424) > INDUSTRY(0.358) > FAST(0.350) > SLOW(0.347) |
| KOR_1 | **SECTOR(0.562) > MARKET(0.473) > SUBINDUSTRY(0.308) > INDUSTRY(0.257) > NONE(0.192)** |

`tools/webdata_quality.py` 启动即输出目标 region 的区域级排名（含 osis_count 可信度标注）。规划模拟批次时：
- 先扫目标 region 的区域排名，把前 2-3 个中性化设为默认候选；
- 再按规则 3 细化到数据集级/字段级；
- 每格用 `count` 与 `osis_count` 双阈值判可信度（规则 10）。KOR 的 CROWDING/SLOW 为负值——risk-based 中性化在 KOR 社区整体踩坑，非首选。

## 规则 20 — 挖掘推荐综合评分（--recommend, 2026-08-03 新增）

`tools/webdata_quality.py --recommend` 输出按综合 score 排序的挖掘推荐表，直接决定"下一个挖哪个数据集"：

```
score = sharpe × sweet_bonus × os_penalty × neut_reliability
- sweet_bonus: 甜点区(100≤count≤3000 且 sharpe≥1.1×均值)=1.3; count>30000=0.5; 其他=1.0
- os_penalty: (IS+OS sharpe − OS sharpe) > 0.15 视为样本外退化 → 0.5
- neut_reliability: 该数据集最优中性化的 count≥20 且 osis_count≥20 → 1.1
```

KOR_1 实测推荐序：`news59(0.854) > insiders5(0.806) > pv106(0.805) > shortinterest3(0.750) > fundamental44(0.735)`。所有 score 都已叠加"社区验证"（甜点区）、"OS 质量"（退化惩罚）、"中性化可靠度"三重先验——规划批次时从表头往下消费，避免凭直觉挑数据集。

## 规则 21 — 字段级 Top 榜与字段级中性化（--field-top N, 2026-08-03 新增）

`isos.datafield[<field>]` 给出每字段的社区 alphaCount/sharpe/fitness，`neutralization.datafield[<field>]` 给出**字段级**最优中性化（比数据集级更细，样本 `count≥5` 即可）。`--field-top N` 输出两者合并的字段榜：

KOR_1 实测 Top15 头部：`close(21744) / returns(17091) / volume(14150) / cap(13374) / adv20(11986) / open / low / high / vwap / sharesout / split / dividend / mws59_event_fiscal_year / rsk70_mfm2_asetrd_anlystsn / mws59_event_time_value`。注意：
- 前 12 个全是 pv 类基础字段（KOR 社区 78% 提交集中在 pv 类）→ 想点亮非 pv 金字塔必须用高 sharpe 的非 pv 字段（如 `mws59_*`、`rsk70_*`）；
- 字段级中性化先例：`low/high/vwap/sharesout/split/dividend` 最优是 **MARKET**，其余多为 SECTOR——与区域级排名交叉验证中性化选择；
- 高 alphaCount 字段 = 社区反复验证可提交（规则 5），但也是拥挤度信号（规则 24 反查确认）。

## 规则 22 — region×category 数据可用矩阵（插件硬编码表, 2026-08-03 新增）

`distribution.js` 硬编码了两张"该 region 无该 category 数据"的表（`non_data` 与 `non_data_delay0`），是 WQ 平台数据可用性的权威矩阵（图表 NAN 灰点）：

- **KOR delay1 无数据类别**：Broker / Institutional Ownership / Macro / Option / Sentiment / Social media / Insiders
- **KOR delay0 额外无数据**：Fundamental / Analyst / News / PV / Earnings / Short interest / Other / Risk / Model（即 KOR delay0 几乎无数据）
- JPN 大多类别无数据（fundamental/analyst/news/sentiment/pv/option/earnings/insiders/institutions/shortinterest/macro/other/risk/model 在 delay0 全缺）

规划用途：目标 region×category 若在表中 → **直接跳过**，不必上平台试（数据包 category 统计里那些小样本如 KOR sentiment=666 是历史提交，数据可能已下线）。挖矿前先对照此矩阵定"该 region 能挖哪些 category"，再从中选未点亮金字塔。

## 规则 23 — 用户多样性/金字塔点亮 API（diversity 端点, 2026-08-03 新增）

插件 distribution 图调用的 `GET /users/self/activities/diversity?grouping=region,delay,dataCategory` 返回用户在每个 region×delay×category 格的 `alphaCount` 与 `dataDiversity.check`（PASS/FAIL）。用途：
- **点塔规划**：check 非 PASS 的格子 = 该金字塔未点亮 → 与 `get_pyramid_alphas` 交叉确认后作为优先挖掘目标（KOR 全 15 类未点亮，全点灯空间大）；
- **配额对比**：每格 `alphaCount / 该 region 最大格 count` 给出相对密度，辅助判断拥挤度。

## 规则 24 — 字段反查已提交 alpha（拥挤度/ProdCorr 预判, 2026-08-03 新增）

插件 `alphaDetailsPopup.js` 双击任意字段名 → 列出**本季度所有使用该字段的已提交 alpha**（含设置/代码），并调 `/data-fields/<id>` 反查字段所属 dataset/category。挖矿用途：
- **拥挤度预判**：某字段被大量已提交 alpha 使用 → 新 alpha 用它 ProdCorr/SelfCorr 风险高，需非对称结构或换字段；
- **风格模仿**：查看他人已提交代码学习该字段的合理用法（结合论坛模板）；
- 对应平台 REST 同款能力：`/users/self/alphas?limit=..&offset=..&status!=UNSUBMITTED%1FIS-FAIL&dateSubmitted>..&dateSubmitted<..` + 代码子串过滤。

## 规则 25 — 批量回测基础设施（配额/保活/重试, 2026-08-03 新增）

插件三件基础设施直接映射 MCP 批量挖矿运维：
- **配额监控**（`simulate.js`）：`/simulations` 响应头 `x-ratelimit-limit/remaining` 实时显示剩余配额，429 = SIMULATION_LIMIT_EXCEEDED。批量轮询 `lookINTO_SimError_message` 时若遇 429/503 应退避重试（插件用线性退避 retryCount×500ms，最多 10 次）；
- **会话保活**（`sessionKeeperService.js`）：每 5 分钟 ping `https://api.worldquantbrain.com/authentication` 防止 token 过期；MCP 长时挖矿会话若中途 401，先重新 `authenticate` 再继续批次；
- **GET 重试**（`noMoreDifficulties.js`）：对 `api.worldquantbrain.com` 的 GET 自动重试 429/500/502/503/504 与网络错误（幂等安全）；POST 不重试（防副作用）——MCP 轮询/取详情等同理。

## 规则 26 — 体检→表达式硬门校验（2026-08-05 新增）

规则 4/9/13/14/18 的体检建议原本只是人类可读文本（`field_inspect` 的 `print()` 输出），执行 skill 的 AI 可以"参考"但跳过不会报错。规则 26 把这些约束变成**代码可执行的硬门**。

### 结构化导出

`tools/webdata_quality.py` 新增 `--export-expr` 参数和两个函数：

| 函数 | 输入 | 输出 | 用途 |
|---|---|---|---|
| `field_inspect_to_expr(field, fdata, neut)` | 单字段体检数据 | `{field, advices, expressions[], metadata{}}` | 生成候选表达式 + 结构化元数据 |
| `check_expr_against_inspect(expr, result)` | 表达式字符串 + 体检结果 | `{ok: bool, violations: []}` | 校验表达式是否满足体检硬性要求 |

导出命令：

```bash
python tools/webdata_quality.py --zip WebData_*.zip --region USA --delay 1 \
    --fields fundamental6,insiders3 \
    --export-expr tracking/field_inspect_usa.json \
    --neut subindustry
```

生成的 JSON 每字段含：
- `advices`: 人类可读建议列表（原 `field_inspect` 输出）
- `expressions`: 按 priority 排序的候选 FASTEXPR（1=最高优先，覆盖最严重体检信号）
- `metadata`: 覆盖率/偏度/峰度/频率/分布形状/最小窗口/推荐decay/推荐truncation

### 5 条硬门校验规则

`check_expr_against_inspect` 对每条表达式检查：

| # | 体检信号 | 硬门要求 | 不满足的后果 |
|---|---|---|---|
| 1 | CoverageRatio < 0.4 | 表达式必须含 `ts_backfill` 或 `group_backfill` | CONCENTRATED_WEIGHT |
| 2 | \|skewness\| > 2 | 表达式必须含 `rank`/`winsorize`/`signed_power` | 极值未抑制 |
| 3 | kurtosis > 8 | 表达式必须含 `rank` 或 `winsorize` | 厚尾未处理 |
| 4 | 单边恒正/负 | 不能直接用原始水平（须含 `ts_delta`/`rank`/`bucket`） | 信号不对称 |
| 5 | 分布形状 = zero_inflated/point_mass | 必须含 `trade_when` 门控 | 有效信息被稀释 |

### 在 skill 中的消费位置

| Skill | 步骤 | 动作 |
|---|---|---|
| `brain-alpha-research` | 第 16 步 | 研究阶段跑 `--export-expr` 生成 JSON |
| `wq-brain-ra-pipeline` | 步 5 | `check_batch` 后、`create_multi_simulation` 前调用 `check_expr_against_inspect` |
| `brain-alpha-repair` | 第 2c 步 | 修复后复验，`ok=False` 继续修复 |
| `brain-alpha-repair/references/repair-order.md` | 第 6 步 | 修复流程末尾的体检硬门复验 |
| `brain-alpha-robustness` | Phase B.0a | 候选到达 robustness 审计时的体检硬门前置确认 |
| `alpha-template-labs-data-analysis` | Hard Rules | Labs 分析衍生的表达式提交前须通过体检硬门 |

执行流程：`check_batch（多样性）→ check_expr_against_inspect（合理性）→ create_multi_simulation`

## 重新生成排名数据

解包与排名脚本见 [`../../../../tools/webdata_quality.py`](../../../../tools/webdata_quality.py)（依赖 `msgpack`）：

```bash
# 数据集排名 + 甜点区 + OS 退化 + 类别统计 + Universe 覆盖
python tools/webdata_quality.py --zip WebData_20260219_V0.10.9.zip --region USA --delay 1

# 跨区域数据集对比（识别 region-specific 机会）
python tools/webdata_quality.py --zip WebData_20260219_V0.10.9.zip --region ASI --delay 1 --cross-region

# 字段级体检（分布形状解析 + 预处理算子建议 + 字段组合建议）
python tools/webdata_quality.py --zip WebData_20260219_V0.10.9.zip --region USA --delay 1 --fields fundamental6,insiders3

# 导出完整 JSON（含字段 Top 榜 + 每字段最优中性化）
python tools/webdata_quality.py --zip WebData_20260219_V0.10.9.zip --region USA --delay 1 --json-out tracking/quality_usa1.json

# 挖掘推荐表（规则 20 综合评分, 决定挖掘顺序）+ 字段 Top 榜（规则 21）
python tools/webdata_quality.py --zip WebData_20260219_V0.10.9.zip --region KOR --delay 1 --recommend --field-top 15
```

输出：**区域级中性化排名表**（规则 19）、**Universe 覆盖表**、（可选）跨区域对比表、数据集排名（count/sharpe/fitness/OS sharpe/最优中性化，含 `osis_count` 阈值）、甜点区清单（区域均值×1.1 阈值）、**OS 退化检测表**、类别级统计、**字段级体检报告**（含分布形状与组合建议）、**挖掘推荐表**（规则 20）、**字段 Top 榜**（规则 21，含字段级最优中性化）。数据包更新后重跑即可刷新先验。
