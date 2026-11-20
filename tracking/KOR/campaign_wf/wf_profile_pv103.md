# wf_profile_pv103 — pv103（KOR / pv）全字段画像

> 画像员：字段画像员-pv103 · 归档日期 2026-11-19
> 数据集：pv103 = "Interval and MOO&MOC statistics" · category pv · KOR / TOP600 / Delay=1
> 塔：KOR/D1/pv —— 本轮 `get_pyramid_alphas` 实读 **pv = 2**（与 ask「近闸 2/3」一致）。
> 本文件只做画像与归档，不发仿真、不撤判死标记、不做候选排序决策。

---

## 0. 对账与证据来源（每条数字注明出处）

| 项 | 值 | 出处（本轮实读，或注明转引） |
|---|---|---|
| 字段全集 | 7 字段，`count=7` / `platform_count=7` / `complete=true` / `pages_fetched=1` / `returned=7` | 本轮 MCP `get_datafields(region=KOR, dataset_id=pv103, universe=TOP600, delay=1, filter_sharpe=false, max_fields=未传)` 返回体（`ordering_scope=KOR/TOP600/D1`） |
| 数据集级 coverage | **1.0** | 本轮 `get_datasets(region=KOR, universe=TOP600, delay=1, search=pv103)` 返回 `coverage=1.0` |
| 数据集级 fieldCount | 7 | 同上 |
| 数据集级 alphaCount | **200**（与 ask 一致 ✓） | 同上 `alphaCount=200`；`userCount=109`、`valueScore=3.0`、`pyramidMultiplier=1.4` |
| 字段类型分布 | **7/7 全 MATRIX**，无 VECTOR / 无 GROUP | 本轮 `get_datafields` 逐字段实取 |
| 字段级 alphaCount 范围 | **21–56**（Σ=247） | 本轮 `get_datafields` 逐字段实取；最低 `max_trade_price`=21，最高 `final_trade_price`=56 |
| 字段级 userCount 范围 | **17–39** | 同上 |
| 字段 dateCreated | **7/7 全为 2025-10-01**（新 onboard，与 ask 一致 ✓） | 同上 |
| 字段 pyramidMultiplier | **7/7 = 1.4** | 同上（与 `get_datasets` 的 1.4 一致） |
| 塔位 | KOR/D1/pv = **2**（全平台 pv 计数：KOR 2、EUR 2、GLB 2、GBR 4、IND 12、HKG 1） | 本轮 `get_pyramid_alphas` 实读 |
| 本地字段画像库 | 7 字段 `verdict=UNTESTED`、`n_tests=0`、`updated_at=2026-10-25` | 本轮 `mcp__wqb-db__query_field_profile(region=KOR, dataset=pv103)` 实读（**快照早于 P103 实测，属陈旧数据**） |
| 历史实测（关键） | pv103 已于 2026-11-07 派 10 臂实测，天花板 **S1.04**，判死 | 转引 `tracking/KOR/reference/datasets/pv103.md:12-22` 与 `tracking/KOR/campaign_20261107_pv_atom/DELIVERY_KOR_ATOM.md:744-751`；派发凭据 `tracking/KOR/campaign_20261107_pv_atom/_p103_dispatch.json`（multisim `30wKDr4fo5aP9khqabGLnRq`，10 条表达式） |

**全字段探测合规**：本轮 `get_datafields` 不传 `max_fields`、`filter_sharpe=false`，返回 `complete=true`，
下表逐字段列真实 id（无 `*_active` 通配、无「同构孪生」占位），每个字段在 §2 都有带数字的读数行。

---

## 字段全表（7/7，本轮 get_datafields 全量实取）

| 字段 | 类型 | 覆盖 | aC | uC | dateCreated | 语义（平台 description 原文 → 中文直译） | 角色 |
|---|---|---:|---:|---:|---|---|---|
| `session_1430to1430_final_trade_price` | MATRIX | 1.0 | 56 | 39 | 2025-10-01 | Last trade price recorded at the end of the 14:30 to 14:30 session；14:30→次日14:30 时段的最后成交价 | 主信号（收尾价：比率分子/时序分位；**裸水平禁用**，价格水平=价格/股本结构代理） |
| `session_1430to1430_initial_trade_price` | MATRIX | 1.0 | 41 | 22 | 2025-10-01 | First trade price recorded at the start of the 14:30 to 14:30 session；时段首个成交价 | 主信号（时段开价：比率分母/时序分位；裸水平禁用同前） |
| `session_1430to1430_market_value` | MATRIX | 1.0 | 26 | 20 | 2025-10-01 | Aggregate market value of all trades during the 14:30 to 14:30 session；时段全部成交的美元金额合计 | **排除主信号**（成交额水平=规模/流动性代理；仅变化量/相对自身历史写法） |
| `session_1430to1430_max_trade_price` | MATRIX | 1.0 | 21 | 17 | 2025-10-01 | Highest trade price recorded during the 14:30 to 14:30 session；时段最高成交价 | 主信号（区间上沿：收盘位置/振幅分子；裸水平禁用） |
| `session_1430to1430_min_trade_price` | MATRIX | 1.0 | 52 | 28 | 2025-10-01 | Lowest trade price recorded during the 14:30 to 14:30 session；时段最低成交价 | 主信号（区间下沿：收盘位置/振幅分母；裸水平禁用） |
| `session_1430to1430_total_traded_volume` | MATRIX | 1.0 | 44 | 33 | 2025-10-01 | Total number of shares or contracts traded during the 14:30 to 14:30 session；时段成交股数/合约数 | 分组轴/规模-流动性轴（**裸水平禁用**；仅变化量/时序分位/相对自身历史） |
| `session_1430to1430_volume_weighted_avg_price` | MATRIX | 1.0 | 47 | 34 | 2025-10-01 | Volume-weighted average price for trades during the 14:30 to 14:30 session；时段成交量加权均价（VWAP） | 主信号（机构执行基准：比率分母/时序分位；裸水平禁用） |

---

## 2. 实测读数表

> 读数分三列来源，**不混称**：① 本轮 `get_datafields` 平台元数据（覆盖/aC/uC/dateCreated）；
> ② 本轮 `mcp__wqb-db__query_field_profile` 本地画像库读数；③ 本集档案实测读数（P103 批次，
> 转引 `tracking/KOR/reference/datasets/pv103.md:14-19`，仅 4 臂有归档数字）。
> 画像员本轮**未重跑仿真**（职责边界：只画像不仿真），P103 数值为档案实测数字逐字段转录。

| 字段 | 元数据覆盖 | aC | uC | DB 画像判定 | 本集档案实测（P103 臂，含该字段的表达式） | 数据层裁决 |
|---|---:|---:|---:|---|---|---|
| `session_1430to1430_final_trade_price` | 1.0 | 56 | 39 | UNTESTED（陈旧快照） | `zq37WKEX` VWAP 偏离 ts_mean22 **S1.04**/F0.72/2Y1.77/TO0.192/raF2；`qML2X9V2` 反向裸 S0.70/TO0.958 | 进主信号（比率分子） |
| `session_1430to1430_initial_trade_price` | 1.0 | 41 | 22 | UNTESTED（陈旧快照） | `VkxQ81R0` 时段收益反转裸 S0.50/F0.17/2Y1.29/TO0.467 | 进主信号（比率分母） |
| `session_1430to1430_market_value` | 1.0 | 26 | 20 | UNTESTED（陈旧快照） | 末臂 `group_rank(ts_backfill(session_1430to1430_market_value,5), sector)`：**档案未留读数**（`_p103_dispatch.json` 第 10 条表达式，无对应结果行） | 排除主信号（规模/流动性代理） |
| `session_1430to1430_max_trade_price` | 1.0 | 21 | 17 | UNTESTED（陈旧快照） | `e75MrkWE` 收盘位极（`divide(subtract(final,min), subtract(max,min))`）**S−0.37**/F−0.06/2Y0.99/TO0.835 | 进主信号（区间上沿；裸水平禁用） |
| `session_1430to1430_min_trade_price` | 1.0 | 52 | 28 | UNTESTED（陈旧快照） | 同上 `e75MrkWE`（区间下沿，同臂） | 进主信号（区间下沿；裸水平禁用） |
| `session_1430to1430_total_traded_volume` | 1.0 | 44 | 33 | UNTESTED（陈旧快照） | 「量」臂（`reverse(group_rank(ts_backfill(total_traded_volume,5), sector))`）：**档案未留读数** | 分组轴（裸水平禁用） |
| `session_1430to1430_volume_weighted_avg_price` | 1.0 | 47 | 34 | UNTESTED（陈旧快照） | `zq37WKEX`（分母）/ `qML2X9V2`（分母）同臂读数 | 进主信号（执行基准/时序分位） |

**档案留数缺口（如实登记，不填猜测值）**：P103 十臂只归档了 4 臂读数（`tracking/KOR/reference/datasets/pv103.md:14-19`），
其余 6 臂（量臂、市值臂、ts_zscore 臂、ts_mean22 变体臂、ts_rank 臂、两组 VWAP 偏离变体）在档案中**没有数字读数**，
`get_alpha_details` 等本轮未回读平台历史结果，故本表对应行记为「档案未留读数」，不补估算。

---

## 3. 结构观察（基于上表实测）

1. **全 MATRIX、无 VECTOR ⇒ 本集不适用「VECTOR 元数据覆盖高估」坑**（该坑见 `docs/experience/07_field_profile_template_mapping.md:157-167`，
   实测高估发生在 VECTOR 流量族）。但 **MATRIX 的 coverage=1.0 也不能当「当天非零」的保证**：
   元数据 coverage 是「有该字段记录」的比例；14:30 时段聚合字段在停牌/当日无成交票上仍可能为空值，
   须靠 `ts_backfill` 短窗补覆盖并观察 CW。
2. **价格水平字段是慢变量的横截面水平值**：final/initial/max/min/vwap 五个字段的横截面排序 ≈ 价格水平/股本结构代理，
   裸水平 `rank` 会撞规模/价格代理（详见 §4）。合法用法只有：比率（同字段族相除，自然无量纲）与相对自身历史（时序分位/zscore/一阶差）。
3. **`market_value`（成交额美元）与 `total_traded_volume`（成交股数）是规模/流动性代理**，是本集最需要防撞的字段（§4 逐一点名）。
4. **7 字段全部是信号字段**，无元数据/参考型字段（不像 pv20 的公司名/SEDOL 参考集），无需先做字段可用性排查。
5. **P103 只测过 1 套配置**（REV&MOM、d4、trunc0.08，10 条表达式全部 `group_rank(..., sector)` 组轴 + `ts_backfill(·,5)`）
   ⇒ 按判死六维口径，本集只满足 D3（水平/比率/zscore/ts_rank）与 D5（ts_rank）部分，**D4 分组轴仅 1 个（sector）、D6 配置仅 1 套**。
   档案「判死」属**单配置单轴的信号层判死**，不是六维穷尽判死；本画像员不撤判、不重判，仅如实登记该口径。

---

## 4. ★ 规模代理饱和律对照（ask 特别要求）

本集核心字段确含「慢变量的横截面水平值」——价格水平与成交额/股数水平，横截面排序会撞规模代理：

| 字段 | 水平语义 | 规模通道证据 | 处理（可替代写法） |
|---|---|---|---|
| `session_1430to1430_market_value` | 时段成交美元额 | 大票成交额天然大、流动性高 ⇒ 横截面排序≈做多大盘/高流动票，是**规模&流动性暴露**而非微结构信号 | **水平禁用**；替代：`divide(market_value, ts_mean(market_value,66))`（相对自身历史）、`ts_rank(market_value,252)`、`ts_delta(market_value,22)`；仅作比率分母须验证非抵消 |
| `session_1430to1430_total_traded_volume` | 时段成交股数 | 股数与市值/换手强相关 ⇒ 水平≈规模/流动性代理 | **水平禁用**；替代：`ts_rank(total_traded_volume,252)`、`ts_delta`、`divide(total_traded_volume, ts_mean(total_traded_volume,66))`；或作分组轴 |
| `session_1430to1430_final_trade_price` 等 5 个价格字段 | 价格水平 | 价格水平横截面排序≈价格/股本结构代理，且高价≠高收益 | **水平禁用**；替代：**比率**（`divide(final, vwap)`、`divide(final, initial)`、`divide(subtract(final,min), subtract(max,min))`，同字段族相除无量纲）或**相对自身历史**（`ts_rank(vwap,252)`/`ts_zscore(vwap,252)`/`ts_delta(vwap,22)`） |

**三类合法写法（写入 §5 统计族）**：① 变化量 `ts_delta(F, 22|66)`；② 相对自身历史偏离 `ts_rank(F,252)` / `ts_zscore(F,252)`；
③ 离散度/分歧——本集字段为日频时段聚合，无多日横截面离散度可用，改用**同字段比率价差**实现「分歧」（如 final/vwap 与 initial/vwap 的差）。
⛔ 禁 `rank(裸水平)` / `group_rank(裸水平, …)`；⛔ 禁 `add(带单位字段, 裸常数)` 防除零（量纲坑，`docs/experience/07_field_profile_template_mapping.md` 量纲段）。

---

## 5. 机制假设（5 条；格式 = 机制名｜存量型/流量型｜一句话经济叙事｜适用统计族｜可预注册证伪条件）

1. **收尾相对 VWAP 偏离（收盘买卖压力 / 执行质量）｜流量型（14:30 时段统计量，每交易日刷新，可用短窗平滑）｜** 机构以 VWAP 为执行基准下单，收盘成交价相对全时段均价的偏离 = 收尾阶段净买卖压力，压力在后续交易中被修正。｜**统计族**：`divide(session_1430to1430_final_trade_price, session_1430to1430_volume_weighted_avg_price)` → `ts_mean(·,22)` 平滑降换手 → `group_rank(·, sector)` 或 `ts_rank(·,66)`；方向取 P103 实测为正向。｜**证伪条件**：P103 正向 `zq37WKEX` S1.04、反向 `qML2X9V2` S0.70（TO0.958 爆）已确证方向；若新配置（STATISTICAL/SECTOR 双档）下 |S|<1.0 或与市值/换手截面相关 |ρ|>0.9 ⇒ 机制在 KOR 无截面定价力，封盘不再扫窗口/平滑谱。
2. **时段内收益与反转（intraday return & reversal）｜流量型（日内时段收益是日频刷新量）｜** 时段首末成交价之比刻画当日动量痕迹，次日存在回吐 ⇒ 负向外推可得超额。｜**统计族**：`divide(final, initial)` → `ts_zscore(·,66)` / `ts_mean(·,22)`；裸比率臂 TO 0.467 偏高，须先平滑或 `ts_target_tvr_decay(0.1)`（不动 decay/truncation）。｜**证伪条件**：P103 裸臂 `VkxQ81R0` S0.50/2Y1.29 已弱；若新档 |S|<1.0 且 2Y<1.0 ⇒ 机制死（P103 已近此形态，不再扫窗）。
3. **收盘位置与振幅（close location / intraday range）｜流量型｜** 收盘落在 [min,max] 的位置（Williams %R 型）反映尾盘推升或压落；区间幅度相对 VWAP 是当日实现波动，具低波异象。｜**统计族**：位置 `divide(subtract(final,min), subtract(max,min))`（同族相减相除、无量纲）；波动侧 `divide(subtract(max,min), vwap)`，配 `ts_mean(·,22)` 降换手。｜**证伪条件**：P103 `e75MrkWE` 收盘位极 S−0.37/2Y0.99；若 |S|<1.0 或与波动率代理截面相关 >0.9 ⇒ 死（禁止裸 zscore 防右偏厚尾，用 rank/比率）。
4. **成交均价的自身历史分位（时序位置，避规模代理）｜存量型（VWAP 是价格水平，慢变量；横截面水平禁用，仅时序分位合法）｜** VWAP 相对自身一年历史处于高/低分位 = 成交重心漂移，去价格水平截面后仍保留时段定价信息。｜**统计族**：`ts_rank(session_1430to1430_volume_weighted_avg_price,252)` / `ts_zscore(·,252)` / `ts_delta(·,22)`；如需截面化再 `group_rank(·, sector)`。｜**证伪条件**：与 12-1 动量或市值代理截面相关 |ρ|>0.85 ⇒ 退化为动量/规模代理，机制推翻；或正式臂 |S|<1.0 ⇒ 死。
5. **规模代理陷阱与合法替代（约束型机制，非可投方向）｜存量型（market_value / total_traded_volume 的水平是规模与流动性代理，变化量与相对自身历史才是合法用法）｜** 成交额与成交股数的横截面水平排序本质是做多大盘/高流动票的暴露，不是微结构信号；只有相对自身历史或变化量才能剥离规模通道。｜**统计族**：⛔ 禁 `rank(market_value)` / `rank(total_traded_volume)` / `group_rank(裸水平)`；合法替代 = `divide(market_value, ts_mean(market_value,66))`、`ts_rank(total_traded_volume,252)`、`ts_delta(·,22)`；Amihud 类 `divide(abs(return), market_value)` 需跨集收益字段，本集 ATOM 前提下不作主信号。｜**证伪条件**：本条为约束不需证伪；解除条件 = 某写法与市值/成交额水平截面相关 |ρ|<0.5（当前无此证据，不解除）。

---

## 6. 推荐回测档（settings）及理由

**主档（推荐）**：`KOR / TOP600 / delay1 / STATISTICAL / decay4 / trunc0.08 / nanHandling OFF / maxTrade OFF / pasteurization ON`
**对照档（第二套，任何新波必配）**：`KOR / TOP600 / delay1 / SECTOR / decay4 / trunc0.08`
**基线档（沿用 P103 唯一实测档，用于配置平移对照）**：`KOR / TOP600 / delay1 / REVERSION_AND_MOMENTUM / decay4 / trunc0.08`

- **Universe = TOP600 / delay 1**：本画像即该口径实取（7 字段全返回、数据集 cov 1.0）；KOR 区域配置
  `tracking/KOR/config/settings.json:3-13` 同为 TOP600/delay1，结果可直接对照。⚠ KOR TOP600 小宇宙放大 CW/longCount 问题
  （`tracking/KOR/config/thresholds.json:95` 附近口径）。
- **Neutralization = STATISTICAL（主）/ SECTOR（对照）/ REVERSION_AND_MOMENTUM（基线）**：KOR 默认 STATISTICAL（`settings.json:7`）；
  P103 唯一实测档为 REVERSION_AND_MOMENTUM（档案记作 "RAM"，派发文件 `_p103_dispatch.json` 与 `DELIVERY_KOR_ATOM.md:637` 记为 "RAM/d4/trunc0.08"）。
  ⚠ **"RAM" 不是平台中性化枚举值**：本轮 `get_platform_setting_options` 实读 KOR/D1 合法中性化 11 档为
  NONE / REVERSION_AND_MOMENTUM / STATISTICAL / CROWDING / FAST / SLOW / MARKET / SECTOR / INDUSTRY / SUBINDUSTRY / SLOW_AND_FAST
  （`src/wqb/config.py:32-45` 同），其中**无 "RAM"**。本画像按「campaign 短写 + 与 CROWDING/SECTOR/INDUSTRY/NONE 同列比较」的证据，
  将 RAM 判为 **REVERSION_AND_MOMENTUM 的缩写**——此为**推断**，不是平台字段直证；若要复现 P103 基线，建议用 REVERSION_AND_MOMENTUM 并先跑一条对照臂确认数值对齐。
  **避免 SUBINDUSTRY**：KOR 已有 `KOR-SUBINDUSTRY-PROD-SATURATED` 判死记录（转引 `tracking/KOR/reference/datasets/fund_holdings_panel.md:159` 的 `get_dead_ends` 实读，本轮未重读该键），
  换中性化档只能平移 S/2Y，救不了机制（配置平移律，见 ask 附的 2026-11-17 实测律）。
- **decay = 4**：KOR 默认。裸时段比率臂 TO 0.467–0.958（P103 实测）⇒ 表达式内先 `ts_mean(·,22)` / `ts_rank(·,66)` 压换手；
  仍高换手用 `ts_target_tvr_decay(0.1)`，**不动 decay/truncation**（症状→模板查表，`docs/experience/07_field_profile_template_mapping.md:97-98`）。
- **是否需要 backfill：需要，且只许短窗**。7 字段均为时段聚合，停牌/当日无成交票会出现空值，P103 十臂全部带
  `ts_backfill(·,5)`（`_p103_dispatch.json`）——沿用 **`ts_backfill(x,5)`**。**禁长窗 backfill**：把「当天无成交」填成「成交延续」是语义伪造，
  且会把稀疏零值票填成持续信号、放大 CW 与集中度。`ts_backfill` 是 CW FAIL 的补覆盖手段（不是调 decay/truncation）。
- **nanHandling OFF / maxTrade OFF**：与 KOR 区域配置一致；本集无「多年零持仓」结构，不触发 sustained-zero 门需 ON 的情形。

---

## 7. ★ 与 ask 候选理由的事实核对（不掩盖冲突）

1. **「未挖」不成立**：ask 候选理由称本集「未挖」，但工作区档案显示 **pv103 已于 2026-11-07 实测并判死**
   （10 臂 multisim `30wKDr4fo5aP9khqabGLnRq`，天花板 S1.04 `zq37WKEX`，缺口 0.54；出处
   `tracking/KOR/reference/datasets/pv103.md:12-22`、`tracking/KOR/campaign_20261107_pv_atom/DELIVERY_KOR_ATOM.md:744-751`）。
   「字段前缀零命中 ⇒ 真未挖」是 **2026-11-07 派发时刻**的核查结论（`DELIVERY_KOR_ATOM.md:736`），现已被同战役的实测收口取代。
2. **aC「21–56 处甜点」属实但含义需修正**：本轮 `get_datafields` 实读 aC 21–56、uC 17–39，字段确属甜点区；
   但 aC 高≠未挖，本集 200 个平台 alpha 中已有 10 臂实测落空，aC 只说明拥挤度低、不说明机制可交付。
3. **「PV 塔近闸（2/3）」与本轮实读一致**：`get_pyramid_alphas` 实读 KOR/D1/pv=2。
   ⚠ 按 2026-11-17 战役口径，pv=2 被列入「已亮塔」名单（insiders 3/3、analyst 4、fundamental 3、model 3、risk 3、shortinterest 4、**pv 2**、other 2）
   ⇒ 本集**不属未亮塔可攻面**；画像照做，候选资格由选集方裁定，本画像员不做选择。
4. **「字段仅 7 个（roadmap 记样本太小）」风险确认**：全集仅 7 字段且均为时段聚合，机制族覆盖面窄
   （VWAP 偏离、时段收益、区间位置/振幅、时序分位、规模替代），无独立异质腿可组合。
5. **「拍卖统计与 pv1 日内量场相关性未验」**：本集字段语义为 14:30 时段 OHLCV+VWAP，**不含 MOO/MOC 拍卖统计字段**
   （数据集目录描述提到 auction data，但 KOR 该 7 字段无一为拍卖字段，`get_datasets` 描述为平台级原文，字段层语义以 `get_datafields` description 为准）。
   与 pv1 日内量场的相关性本轮**未验**（画像员不发仿真、不做相关性计算），登记为未验证项。
6. **跨区不照抄**：EUR 同集 pv103 为 9 字段（`docs/reference/EUR/datasets/pv103.md:76-88`：16:00 时段 7 字段 + `pv103_ivam_sum` / `pv103_ntrd_sum`，
   覆盖 0.924，mult 1.1）——**同集号不同区字段集与倍率均不同**，EUR 画像结论不可平移到 KOR。

---

## 8. 自查清单

- [x] 无抽样：`get_datafields` 不传 `max_fields`、`filter_sharpe=false`，`count=platform_count=complete=7`，§1 逐字段列真实 id（7 行，无通配）。
- [x] 无凭名推断：语义全部来自平台 description 原文；覆盖/类型/aC/uC/dateCreated 来自本轮 `get_datafields` 实取；
  DB 判定来自本轮 `mcp__wqb-db__query_field_profile` 实读；P103 数值为档案转录并注明「本轮未重跑」。
- [x] 每个字段有带数字读数的实测行（§2，7/7 行；档案未留读数的行如实标注，未补估算）。
- [x] 规模代理：价格水平 5 字段 + 成交额/股数 2 字段逐一点名，三类替代写法（变化量/时序分位/比率价差）写入 §5 统计族。
- [x] 机制假设 5 条，每条标注存量型/流量型 + 一句话经济叙事 + 适用统计族 + 可预注册证伪条件。
- [x] settings 给全（universe/中性化/decay/backfill + 理由），并登记「RAM 非平台枚举值、按缩写推断为 REVERSION_AND_MOMENTUM」的不确定性。
- [x] 事实冲突（「未挖」vs 2026-11-07 已判死；DB 画像 UNTESTED vs 档案已测）如实登记，未填 plausibly guessed value。
- [x] 硬闸：`python tools/gates/field_profile_completeness_gate.py --profile tracking/KOR/campaign_wf/wf_profile_pv103.md` 运行结果见 §9。

## 9. 硬闸回执

> 本文件写完后执行：`python tools/gates/field_profile_completeness_gate.py --profile tracking/KOR/campaign_wf/wf_profile_pv103.md`
> **结果（2026-11-19 实跑，exit 0 = 通过）**：
> `字段全表 id 数: 7` · `带实测读数的字段: 7` · `✅ PASS：全字段均有实测读数，且分母无通配占位`
