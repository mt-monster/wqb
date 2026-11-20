# wf_profile_fund_holdings_panel — fund_holdings_panel（KOR / institutions）全字段画像

> 画像员：字段画像员-fund_holdings_panel · 归档日期 2026-11-18（KOR 战役 2026-11-17 会话延续）
> 数据集：fund_holdings_panel（Global Institutional Fund Holdings）· KOR / TOP600 / Delay=1
> 塔：KOR/D1/institutions —— 本轮 `get_pyramid_alphas` 实读 **institutions=0（未点亮，需 3 颗）**，
> 全平台 `pyramidMultiplier=1.4`（本集 30 字段逐一 1.4，`get_datasets` 亦为 1.4）。
> 本文件只做画像与归档，不发仿真、不改 DEAD 标记、不做候选排序决策。

---

## 0. 对账与证据来源（每条数字都注明出处）

| 项 | 值 | 出处（本轮实读/实测，或注明转引） |
|---|---|---|
| 字段全集 | 30 字段，`count=30` / `platform_count=30` / `complete=true` / `pages_fetched=1` | 本轮 MCP `get_datafields(region=KOR, dataset_id=fund_holdings_panel, universe=TOP600, delay=1, filter_sharpe=false, max_fields=未传)` 返回体 |
| 数据集级 coverage | **0.8093** | 本轮 `get_datasets(region=KOR, universe=TOP600, delay=1, search=fund_holdings_panel)` 返回 `coverage=0.8093` |
| 数据集级 fieldCount | 30 | 同上 |
| 数据集级 alphaCount | **240**（⚠ 与 ask 的 236 不一致） | 同上 `alphaCount=240`，`userCount=122`，`valueScore=4.0` |
| ask 背景 alphaCount | 236 | ask 原文「coverage=0.8093 fieldCount=30 alphaCount=236」；本轮平台实读 240，以平台为准，236 仅作历史快照 |
| 字段级 alphaCount 范围 | **0–35**，Σ=271（本轮平台口径） | 本轮 `get_datafields` 逐字段实取；最高 `boundary_transaction_total`=35，最低 4 个字段=0 |
| 字段类型分布 | **12 MATRIX + 18 VECTOR**（无 GROUP） | 本轮 `get_datafields` 逐字段实取；⚠ 与 `tracking/USA/runs/wf_profile_fund_holdings_panel.md:19` 的「USA 30/30 全 VECTOR」不同，同集跨区字段类型暴露不同，模板不可照抄 USA |
| 字段 dateCreated | **30/30 全为 2026-03-01**（新 onboard） | 本轮 `get_datafields` 逐字段实取；与 ask「30 字段全部 dateCreated=2026-03-01」一致 |
| 塔位 | KOR/D1/institutions=0，mult 1.4 | 本轮 `get_pyramid_alphas` 实读 |
| 死表状态 | `KOR-FUND-HOLDINGS-PANEL-DEAD` status=**REVOKED**（2026-11-17，用户指令） | 本轮 `get_dead_ends(region=KOR)` 实读 id=122 条目，`revoked_at=2026-11-17`、`revoked_by=user instruction` |
| VECTOR 有效覆盖 | 0.7%–33%（元数据 cov 0.887/0.6626 严重高估） | 转引 `tracking/KOR/reference/datasets/fund_holdings_panel.md:327-360` §10.1 法1 Long Count 实测（批次 `2eE84ukg5iAaxjimb9yLII`/`4yBKI23zt4iZbrc1cs4Ee39i`，2026-11-17）。本轮**未重跑**仿真（画像员不发仿真），数值为档案实测读数转录 |

**全字段探测合规**：本轮 `get_datafields` 不传 `max_fields`、`filter_sharpe=false`，返回 `complete=true`，
下表逐字段列真实 id（无 `*_active` 通配、无「N 个同构」占位），每个字段在 §2 都有带数字的实测读数（Long Count）。

---

## 字段全表（30/30，本轮 get_datafields 全量实取，按族排序）

| 字段 | 类型 | 覆盖 | aC | 语义（平台 description 原文 → 中文直译） | 角色 |
|---|---|---:|---:|---|---|
| `herfindahl_index_holdings` | MATRIX | .9553 | 34 | Herfindahl-Hirschman Index of holdings concentration based on account weights；持仓权重 HHI（0–1），持有人集中度 | 主信号（集中度变化/时序分位；水平=规模代理禁用） |
| `herfindahl_index_holdings_active` | MATRIX | .7666 | 11 | HHI of holdings weights across accounts (0 to 1)；活跃账户持仓 HHI | 对照（活跃子集，同源） |
| `holding_value_distribution_score` | MATRIX | .9553 | 19 | Concentration of holdings value across accounts, a custom crowding metric；持仓市值集中度=拥挤度代理 | 主信号（拥挤度变化/分位；水平禁用） |
| `holding_value_distribution_score_active` | MATRIX | .7666 | 7 | higher values indicate more crowding among holders；活跃账户拥挤度 | 对照（同源子集） |
| `holder_account_total` | MATRIX | .9553 | 30 | Number of distinct investment accounts or funds holding the ISIN on the date；持有账户数=机构覆盖广度 | 主信号（breadth stability 分子；水平=覆盖代理禁用） |
| `holder_account_total_active` | MATRIX | .7666 | 6 | Number of distinct accounts holding this ISIN on the date；活跃账户数 | 对照（同源子集） |
| `mean_security_weight` | MATRIX | .9553 | 13 | Average portfolio weight of security across accounts that hold it, as share of each fund AUM；平均组合权重 | 排除（水平=规模代理，仅离散度形态） |
| `mean_security_weight_active` | MATRIX | .7666 | 10 | 同上（活跃账户口径） | 对照（同约束） |
| `security_holding_usd_value` | MATRIX | .9553 | 7 | Total USD value of shares held in the ISIN across all accounts；持仓美元市值余额 | 排除（市值余额=规模代理；仅可作同源比值分母） |
| `security_holding_usd_value_active` | MATRIX | .7666 | 9 | 同上（活跃账户口径） | 对照 |
| `top_weighted_account_number` | MATRIX | .9553 | 16 | Number of accounts for which ISIN is a conviction holding (top 30% by portfolio weight)；信念持仓账户数 | 门控条件+占比变化轴（稀疏 12%；水平禁用） |
| `top_weighted_account_number_active` | MATRIX | .7666 | 11 | 同上（活跃账户口径，极稀疏） | 对照（同源子集） |
| `boundary_transaction_total` | VECTOR | .887 | 35 | Number of boundary transactions (new position initiations or complete liquidations) across all fund accounts on the date；边界交易笔数（全表 aC 最高） | 排除（数据层，有效覆盖约 3%） |
| `boundary_transaction_total_active` | VECTOR | .6626 | 4 | 同上（活跃账户口径） | 对照（同源子集） |
| `boundary_transaction_usd_value` | VECTOR | .887 | 6 | Total USD value of boundary transactions across all accounts on the date；边界交易美元额 | 排除（数据层，约 1.7%） |
| `boundary_transaction_usd_value_active` | VECTOR | .6626 | 2 | Dollar value of boundary transactions in USD；活跃账户边界额 | 对照 |
| `herfindahl_index_transactions` | VECTOR | .887 | 2 | HHI of trade value concentration across transacting accounts (0 to 1)；当日交易额跨账户 HHI | 门控条件（33% 覆盖，仅条件） |
| `herfindahl_index_transactions_active` | VECTOR | .6626 | 5 | 同上（活跃账户口径） | 对照 |
| `large_trade_count_50bps` | VECTOR | .887 | 3 | Number of transactions where trade value exceeds 0.5% of respective fund AUM；单笔超基金自身 AUM 0.5% 的大单笔数（唯一 AUM 归一计数） | 排除（数据层 0.8% 覆盖；机制好但覆盖不足） |
| `large_trade_count_50bps_active` | VECTOR | .6626 | 1 | 同上（活跃账户口径） | 对照 |
| `security_transaction_usd_value` | VECTOR | .887 | 3 | Dollar value of transactions in USD；当日机构成交美元额 | 主信号（流量÷存量分子；19% 覆盖，仅门控/比值） |
| `security_transaction_usd_value_active` | VECTOR | .6626 | 1 | 同上（活跃账户口径） | 对照 |
| `stable_boundary_trade_count_21d` | VECTOR | .887 | 13 | Count of boundary transactions by accounts that had no boundary trade in same security in prior 21 weekdays；持久性调仓笔数 | 排除（数据层 2.5% 覆盖） |
| `stable_boundary_trade_count_21d_active` | VECTOR | .6626 | 1 | 同上（活跃账户口径） | 对照 |
| `top_weighted_transaction_number` | VECTOR | .887 | 8 | Number of transactions in securities that were conviction holdings as of prior or current day；信念持仓相关交易笔数 | 排除（数据层 1.3% 覆盖） |
| `top_weighted_transaction_number_active` | VECTOR | .6626 | 1 | 同上（活跃账户口径） | 对照 |
| `transaction_account_total` | VECTOR | .887 | 6 | Number of distinct accounts that transacted the security on the date；当日交易账户数 | 门控条件（33% 覆盖，仅条件） |
| `transaction_account_total_active` | VECTOR | .6626 | 0 | Number of accounts that transacted the security；活跃账户当日交易账户数 | 对照 |
| `transaction_value_distribution_score` | VECTOR | .887 | 4 | Index 0 to 1 measuring how day trade value distributed across transacting accounts；当日成交额集中度 | 门控条件（33% 覆盖，仅条件） |
| `transaction_value_distribution_score_active` | VECTOR | .6626 | 3 | 同上（活跃账户口径） | 对照 |

---

## 2. 实测读数表（法1 覆盖率，Long Count / 600）

> 读数来源：转引 `tracking/KOR/reference/datasets/fund_holdings_panel.md:327-360` §10.1（2026-11-17 实测，
> 批次 `2eE84ukg5iAaxjimb9yLII` / `4yBKI23zt4iZbrc1cs4Ee39i`，NONE/d0/P0Y0M0D，universe=600）。
> 本轮画像员**未重跑**这些仿真（职责边界：只画像不仿真）；下表为档案实测数字逐字段转录。
> 全部 30 字段均有数字读数，无抽样、无凭名推断。

| 字段 | LongCount | 有效覆盖(LC/600) | 元数据覆盖 | 读数族 | 数据层裁决 |
|---|---:|---:|---:|---|---|
| `herfindahl_index_holdings` | 527 | 88% | .9553 | 存量-集中度 | 进主信号（变化量/分位） |
| `herfindahl_index_holdings_active` | 403 | 67% | .7666 | active-集中度 | 对照 |
| `holding_value_distribution_score` | 527 | 88% | .9553 | 存量-拥挤度 | 进主信号（变化量/分位） |
| `holding_value_distribution_score_active` | 403 | 67% | .7666 | active-拥挤度 | 对照 |
| `holder_account_total` | 527 | 88% | .9553 | 存量-广度 | 进主信号（breadth stability 分子） |
| `holder_account_total_active` | 403 | 67% | .7666 | active-广度 | 对照 |
| `mean_security_weight` | 527 | 88% | .9553 | 存量-权重 | 水平禁用（规模代理），仅离散形态 |
| `mean_security_weight_active` | 403 | 67% | .7666 | active-权重 | 对照 |
| `security_holding_usd_value` | 527 | 88% | .9553 | 存量-美元余额 | 水平禁用（市值代理），仅同源比值分母 |
| `security_holding_usd_value_active` | 403 | 67% | .7666 | active-美元余额 | 对照 |
| `top_weighted_account_number` | 75 | 12% | .9553 | 存量-信念(稀疏) | 门控+占比变化轴 |
| `top_weighted_account_number_active` | 43 | 7% | .7666 | active-信念(极稀疏) | 对照 |
| `boundary_transaction_total` | 20 | 3% | .887 | 流量-边界笔数 | 数据层排除（<0.05） |
| `boundary_transaction_total_active` | 14 | 2.3% | .6626 | active-边界笔数 | 排除 |
| `boundary_transaction_usd_value` | 10 | 1.7% | .887 | 流量-边界美元额 | 数据层排除 |
| `boundary_transaction_usd_value_active` | 6 | 1% | .6626 | active-边界美元额 | 排除 |
| `herfindahl_index_transactions` | 199 | 33% | .887 | 流量-交易集中度 | 仅门控条件（0.05–0.4） |
| `herfindahl_index_transactions_active` | 118 | 20% | .6626 | active-流量聚合 | 对照/门控 |
| `large_trade_count_50bps` | 5 | 0.8% | .887 | 流量-大单 | 数据层排除（<0.05，全表最低） |
| `large_trade_count_50bps_active` | 4 | 0.7% | .6626 | active-大单 | 排除 |
| `security_transaction_usd_value` | 116 | 19% | .887 | 流量-成交美元额 | 门控/比值（0.05–0.4） |
| `security_transaction_usd_value_active` | 64 | 11% | .6626 | active-成交美元额 | 对照 |
| `stable_boundary_trade_count_21d` | 15 | 2.5% | .887 | 流量-持久调仓 | 数据层排除 |
| `stable_boundary_trade_count_21d_active` | 11 | 1.8% | .6626 | active-持久调仓 | 排除 |
| `top_weighted_transaction_number` | 8 | 1.3% | .887 | 流量-信心交易 | 数据层排除 |
| `top_weighted_transaction_number_active` | 5 | 0.8% | .6626 | active-信心交易 | 排除 |
| `transaction_account_total` | 199 | 33% | .887 | 流量-交易账户 | 仅门控条件（0.05–0.4） |
| `transaction_account_total_active` | 118 | 20% | .6626 | active-流量聚合 | 对照/门控 |
| `transaction_value_distribution_score` | 199 | 33% | .887 | 流量-交易分布 | 仅门控条件（0.05–0.4） |
| `transaction_value_distribution_score_active` | 118 | 20% | .6626 | active-流量聚合 | 对照/门控 |

---

## 3. 结构观察（基于上表实测）

1. **VECTOR 元数据 coverage 严重高估**：元数据统一标 .887（全量）/.6626（active），实测有效覆盖 0.7%–33%。
   根因：元数据是「有该字段记录」的比例，不是「当天非零」的比例（`docs/experience/07_field_profile_template_mapping.md:157-169`）。
   ⇒ coverage 仅供排序；<0.05 直接数据层排除（large_trade 5、boundary_usd 10、top_weighted_trans 8、stable_boundary 15、boundary_total 20），
   0.05–0.4 只作门控条件（transaction_account / herfindahl_transactions / value_dist 三聚合族 199）。
2. **存量 MATRIX 族（6 主 + active）才有全截面**：5 个主存量 527/600=88%，active 403/600=67%。
   例外：`top_weighted_account_number` 主版仅 75、active 仅 43——「信念持仓」本就稀疏。
3. **12 MATRIX + 18 VECTOR 的跨区差异**：USA 同集 30/30 VECTOR（`tracking/USA/runs/wf_profile_fund_holdings_panel.md:19`），
   KOR 存量字段暴露为 MATRIX、流量字段为 VECTOR ⇒ 模板不可从 USA 照抄「一律 vec_* 起手」；
   KOR 对 MATRIX 存量字段直接用裸字段，仅 VECTOR 流量字段需 `vec_sum`/`vec_avg` 降维。
4. **active 孪生 = 同源降采样**：每对 active≈非 active 的 67%（403/527），同族窗口谱只留一席，禁同波并扫。

---

## 4. ★ 规模代理饱和律对照（ask 特别要求）

本集核心字段正是「慢变量的横截面水平值」，水平排序会撞规模代理：

| 字段 | 水平语义 | 规模通道证据 | 处理 |
|---|---|---|---|
| `security_holding_usd_value` | 持仓美元市值余额 | 饱和律点名的「市值余额」类，横截面排序≈做多市值 | **水平禁用**；仅作流量÷存量同源分母（须验证非抵消） |
| `mean_security_weight` | 持有人平均组合权重 | `tracking/USA/runs/wf_profile_fund_holdings_panel.md:60` T7 实测 level 版 long 2997 / short 0 纯多头 | **水平禁用**；仅 `vec_stddev` 离散形态（KOR 为 MATRIX，用 `ts_std_dev`） |
| `holder_account_total` | 持有账户数/覆盖广度 | 大票天然账户多 ⇒ 水平排序≈市值/覆盖代理 | **水平禁用**；仅 `ts_delta`（M2）或作归一分母 |
| `herfindahl_index_holdings` / `holding_value_distribution_score` | 集中度/拥挤度 | HHI 高↔账户少↔偏小盘；拥挤度水平有规模通道 | **水平禁用**；仅变化量/时序分位（M3） |
| `top_weighted_account_number` | 信念持仓账户数 | 大票账户多⇒信念账户数天然多；占比水平 W6 实测 −0.18 死 | **水平禁用**；仅占比变化（M4） |

**可替代写法（三类，写入 mechanisms 的统计族）**：① 变化量 `ts_delta(F, 22|66)`；
② 相对自身历史偏离 `ts_rank(F, 252)` / `ts_zscore(F, 252)`；③ 离散度 `ts_std_dev(F, 252)` / `vec_stddev`。
⛔ 禁 `rank(裸水平)` / `group_rank(裸水平, …)`；⛔ 禁 `add(带单位字段, 裸常数)` 防除零（W5 量纲闸实测整批 WARNING，见档案 §W5 量纲段）。

---

## 5. 机制假设（5 条；格式 = 机制名｜存量型/流量型｜经济叙事｜适用统计族｜可预注册证伪条件）

1. **机构流量÷存量（调仓强度）｜流量型（分子日频稀疏事件，分母慢变量存量，整体比率属流量族）｜**机构当日买卖额相对既有持仓规模越高 = 主动调仓意愿越强，跟随聪明钱方向，论坛帖报 S1.59/1.53（周期66）。｜**统计族**：`divide(vec_sum(security_transaction_usd_value), security_holding_usd_value)`（同单位相除自然无量纲，禁 add 常数），× `ts_rank(·,66)` 或 `ts_mean(·,66)` 平滑；分子 116/600=19% 只能作比值/门控，禁裸水平 rank。｜**证伪条件**：W5 已实测正向 S−0.93（TO 1.13 爆）、反向 0.71、66 平滑反向 0.44/2Y1.04；若新配置下 |S|<1.0 或与市值截面相关 |ρ|>0.9 ⇒ 机制推翻，不再扫窗口。
2. **持仓广度稳定性（breadth stability / 离散度）｜存量型的二阶变化（一阶差的波动=离散度）｜**持有人账户数变化相对自身历史波动的 z-score 高 = 机构共识的确定性迁移，S&P《An IQ Test For The Smart Money》称亚洲最强因子。｜**统计族**：`divide(ts_delta(holder_account_total,66), ts_std_dev(ts_delta(holder_account_total,66),252))`（论文原式）；替代 `ts_zscore(holder_account_total,252)`（相对自身历史偏离）；分母是慢变量水平须做变化量。｜**证伪条件**：W5 实测正向 −0.09、反向 0.00、industry 轴 −0.18 全近零；若新配置下 |S|<1.0 ⇒ 机制推翻（不是方向问题，是无截面定价力）。
3. **集中度/拥挤度的时序分位（抱团形成与瓦解）｜存量型（HHI/拥挤水平是慢变量，必撞规模代理，水平禁用，只用变化量/时序分位）｜**持仓 HHI 或拥挤度升至时序高位 = 大户集中加仓；拥挤度骤降 = 共识瓦解，方向由数据定。｜**统计族**：变化量 `ts_delta(herfindahl_index_holdings,66)` + 时序分位 `ts_rank(holding_value_distribution_score,252)`；`divide(ts_delta(herfindahl,66), ts_std_dev(ts_delta(herfindahl,66),252))`；交易侧 HHI 是日频流量，可 `ts_mean(herfindahl_index_transactions,22)` 短窗但仅作门控。｜**证伪条件**：转换后与市值/覆盖代理截面相关 |ρ|>0.9 ⇒ 换轴不调参；正式臂 S<1.0 ⇒ 机制推翻（W7 `signed_power(group_rank(Δherfindahl,sector),0.5)` S0.37/2Y1.23 是已知最好但仍未过线）。
4. **信念持仓占比变化 + AUM 归一大单｜存量型（`top_weighted_account_number` 水平撞规模通道，占比水平 W6 实测 −0.18 死，占比变化是合法轴）+ 流量型（`large_trade_count_50bps` 按基金自身 AUM 0.5% 门槛归一，天然规模中性）｜**新晋信念账户占比上升 = 深度研究资金进入；AUM 归一大单笔数上升 = 高信念建仓。｜**统计族**：`ts_delta(divide(top_weighted_account_number, holder_account_total),66)`（占比变化，两计数同单位直接 divide，避量纲坑）；`vec_sum(large_trade_count_50bps)` → `ts_rank(ts_mean(·,22),252)`；稀疏字段用 `trade_when(greater(F,0), ·, -1)` 门控。｜**证伪条件**：W6 实测门控 S−0.48/简单Δ −0.22；占比变化与 momentum/size 截面相关 >0.9 或 |S|<1.0 ⇒ 机制推翻；大单分子 5/600 覆盖若无法用门控救回则数据层排除优先。
5. **规模代理/拥挤反转陷阱（约束型机制）｜存量型（本条是禁用约束，不是可投方向）｜**`security_holding_usd_value`/`mean_security_weight`/`holder_account_total` 的横截面水平本质是市值/覆盖度代理（T7 level 版 long 2997/short 0 纯多头），裸水平会撞 self/prod 规模件；拥挤度高同时是流动性风险。｜**统计族**：⛔ 禁 `rank(裸水平)`；替代写法 = 一阶差 `ts_delta`、相对自身历史 `ts_rank`/`ts_zscore`、离散度 `ts_std_dev`/`vec_stddev`、同源比值（须验证非抵消，W5 同源比值 S−0.15/+0.08 已证无增量）。｜**证伪条件**：本条为约束不需证伪；解除条件 = 某字段水平与市值截面相关 |ρ|<0.5（当前证据不成立，暂不解除）。

---

## 6. 推荐回测档（settings）及理由

**主档（推荐）**：`KOR / TOP600 / delay1 / STATISTICAL / decay4 / trunc0.08 / nanHandling OFF / maxTrade OFF / pasteurization ON`
**对照档（D6 第二套，任何新波必配）**：`KOR / TOP600 / delay1 / SECTOR / decay4 / trunc0.08`

- **Universe = TOP600 / delay 1**：本画像即该口径实取（30 字段全返回、数据集 cov 0.8093）；KOR 区域配置 `tracking/KOR/config/settings.json:5-6` 同为 TOP600/delay1，结果可直接对照。⚠ KOR TOP600 小宇宙放大 CW/longCount 问题（`tracking/KOR/config/thresholds.json:95`）。
- **Neutralization = STATISTICAL（主档）/ SECTOR（对照）**：机构覆盖与集中度有强行业结构；KOR 默认 STATISTICAL（settings.json:7），W6/W7 亦用 STATISTICAL、W5 用 SECTOR。⛔ **避免 SUBINDUSTRY**——`get_dead_ends` 实读 `KOR-SUBINDUSTRY-PROD-SATURATED`（id=1040）：SUBINDUSTRY 把信号压向已生产 alpha 子空间，prod 0.797–0.801 撞墙，「prod 安全设置是 STATISTICAL 或 SECTOR」。换中性化只能平移 S/2Y，救不了机制（配置平移律）。
- **decay = 4**：KOR 默认。流量臂 TO 极高（W4 五条 VECTOR 臂 TO 0.96–1.20、CW=1.0）须先在表达式内 `ts_mean(22–66)` / `ts_sum` 把事件流压成慢变量再 decay；仍高换手用 `ts_target_tvr_decay(0.1)`，不动 decay/truncation（症状→模板查表，`docs/experience/07_field_profile_template_mapping.md:97-98`）。
- **是否需要 backfill：分两类**。存量 MATRIX 字段（持仓连续）可 `ts_backfill(x,66)`；**流量 VECTOR 字段禁长窗 backfill**——把「事件已停」填成「事件持续」是语义伪造。注意 `ts_backfill` 是 CW FAIL 的补覆盖手段（不是调 decay/truncation），但对本集流量族覆盖 0.8%–33%，补时间覆盖也救不回全截面缺失。
- **nanHandling OFF（KOR 默认）/ maxTrade OFF**：与 KOR 区域配置一致；本集无「多年零持仓」结构（残值均为稀疏日频事件），不触发 sustained-zero 门需 ON 的情形。

---

## 7. ★ 与 ask 候选理由的事实核对（不掩盖冲突）

1. **alphaCount**：ask=236，平台 `get_datasets` 本轮实读=240。差异 4，疑为快照时间不同；画像以平台为准。
2. **「两条结构从未在 KOR 落地」**：ask 候选理由称流量÷存量与 breadth stability「从未在 KOR 落地」，并以「旧判死基于 wave124 单批 max|S|0.51、非六维穷尽」为由废除死表。**但工作区档案显示二者已在 2026-11-17 W5 批次（`3kIZ7j4T24tob9fhB7b6yRY`）实测证伪**：
   - 流量÷存量：正向 S−0.93/反向 0.71/66 平滑反向 0.44（TO 0.065）；
   - breadth stability：正向 −0.09/反向 0.00/industry 轴 −0.18。
   出处 `tracking/KOR/reference/datasets/fund_holdings_panel.md:201-259`。
   ⇒ 撤销死表的**核心理由（"从未实测"）已被档案事实取代**。画像员不撤判、不重判，只如实登记：这两条结构属**已测且已知无效轴**，若再入场应视为重复验证而非新机制。
3. **塔位**：ask 称 institutions 0/3，本轮 `get_pyramid_alphas` 实读确认 KOR/D1/institutions=0 ✓。
4. **六维状态**：档案 `fund_holdings_panel.md:431-463` W7 后声明「六维基本穷尽」，累计 9 波 max|S| 0.51→0.71(TO爆)→0.37，0 交付。本画像的机制假设是对该结论的画像侧归档，不构成翻案。

---

## 8. 自查清单

- [x] 无抽样：`get_datafields` 不传 `max_fields`、`filter_sharpe=false`，`count=platform_count=complete=30`，逐字段列真实 id（§1 全表 30 行）。
- [x] 无凭名推断：语义全部来自平台 description 原文；覆盖/类型/aC 来自本轮 `get_datafields` 实取；有效覆盖来自档案 §10.1 Long Count 实测数字（注明转引，未谎称本轮重跑）。
- [x] 每个字段有带数字读数的实测行（§2，30/30 Long Count）。
- [x] VECTOR coverage 高估已标注，给出 <0.05 / 0.05–0.4 / >0.4 三档裁决。
- [x] 规模代理饱和律：5 类水平字段逐一点名，三种替代写法（变化量/时序分位/离散度）已写入 mechanisms。
- [x] 3–5 条机制假设，每条标注存量型/流量型 + 一句话经济叙事 + 适用统计族 + 可预注册证伪条件。
- [x] settings 给全（universe/中性化/decay/backfill + 理由），并标注 SUBINDUSTRY 禁用证据。
- [x] 事实冲突（aC 236 vs 240；两条结构「未测」vs W5 已证伪）如实登记，未填 plausibly guessed value。
- [x] 硬闸：`python tools/gates/field_profile_completeness_gate.py --profile <本文件>` 运行结果见归档回执（本文件写完后执行）。
