# S1 · risk70 全字段画像（96/96，KOR / TOP600 / Delay=1）

> 采集：MCP `get_datafields(dataset_id="risk70", region="KOR", universe="TOP600", delay=1, **filter_sharpe=false**)`
> → `count=96 / platform_count=96 / complete=true`（**96/96 全见，无隐藏字段**）
> 数据集元数据：coverage **0.967** · userCount 1230 · alphaCount **8018** · valueScore 1.0 · 塔乘数 **1.3**（risk 塔 KOR 0/3 未点亮）
> 来源模型：**Axioma MFM2 / ASETRD**（地区风险模型，逐日重估）

---

## 0. 名 vs description 差异表（0.2 纪律：只按 description 分类，逐条记录差异）

| 族 | 名形态 | description 实义 | 若按名字分类会犯的错 |
|---|---|---|---|
| 风格载荷 27 支 | `rsk70_mfm2_asetrd_<style>` | 「… Style Factor Loading」= 个股对风格因子的**回归载荷**（无量纲，可正可负） | 会与 PV/fundamental 同名指标（momentum/value/size）混为「重复字段」；实际是**正交的载荷口径**，不是指标本身 |
| 行业载荷 20 支 | `rsk70_mfm2_asetrd_<industry>` | 「… Industry Factor Loading」= 行业哑变量型载荷 | 会被当信号误用；**只能作分组轴** |
| 三支同描述 `srtindcnt` / `indadj` / `primaryindustry` | 名完全不同 | **description 逐字相同**「Industry factor loading」 | 按 description 会把三者当同一字段；**αC 差 11 倍（1431 / 307 / 126）** ⇒ 它们语义不同但描述未区分（**唯一一处 description 无法辨义的缺口**） |
| `srisk` / `srisku` / `resvol` | 名不含 risk 的 `resvol` 也是风险量 | 三支都是年化特异风险 `%²`，但口径不同（最终 / 未调整初始 / 风格载荷口径） | 会当成三条独立腿；实测 `srisk` 与 `srisku` **S/TO 到小数点后两位相同**（§6.1）⇒ 同一量 |
| `dsrt` | 名不含 risk | 「Specific returns」= 特异收益 | 极易被当独立 alpha；**实为 risk71/risk72 已判死同一量** |
| 非前缀辅件 21 支 | `sector_exposure_*` / `us_equity_*_flag` / `hedge_fund_*` / `*market_cap_usd` / `sector_relative_momentum` / `short_term_industry_country_factor` / `*_adjustment_factor_*` | 混合了**分组轴、规模轴、国家哑变量、以及 3 个真正的经济字段** | 按统一前缀分类会**整块丢弃**，从而漏掉 `hedge_fund_*` / `sector_relative_momentum` / `short_term_industry_country_factor` 这 3 个唯一未被测过的经济轴 |

⚠ `sector_exposure_*` 与 `rsk70_mfm2_asetrd_<industry>` 是**同一件事的两种写法**（行业暴露），
但 αC 差 2 个数量级（0–12 vs 45–425）⇒ 平台用户只认 `rsk70_*` 前缀；本战役统一只用 `rsk70_*` 作分组素材。

---

## 1. 全字段表（96/96）

**列义**：`cov`=横截面覆盖率；`aC`=alphaCount（拥挤度）；`U`=userCount；
`频率`=更新频率（风险模型逐日重估；标「慢」者为本战役按经济含义推断的低频量）；
`形态`=分布形态（载荷≈零中心近正态；风险量=单边恒正右偏；哑变量=0/1）；
`可用性`=本战役裁定（✅可作信号 / ⛔禁区 / ▦仅分组轴 / 🅢仅规模壳）。

### 1.1 风格载荷（27）—— ✅ 主战场

| # | field | type | cov | aC | U | 频率 | 形态 | 可用性 |
|---|---|---|---:|---:|---:|---|---|---|
| 1 | `rsk70_mfm2_asetrd_anlystsn` | MATRIX | .967 | **2922** | **622** | 日 | 零中心近正态 | ✅ **头部轴（首攻）** |
| 2 | `rsk70_mfm2_asetrd_earnyild` | MATRIX | .967 | **1795** | **582** | 日 | 零中心近正态 | ✅ **第二轴** |
| 3 | `rsk70_mfm2_asetrd_btop` | MATRIX | .967 | 794 | 248 | 日 | 零中心近正态 | ✅ 价值轴（与 earnyild 构成 value-quality 差分） |
| 4 | `rsk70_mfm2_asetrd_growth` | MATRIX | .967 | 551 | 157 | 日 | 零中心近正态 | ✅ 备选 |
| 5 | `rsk70_mfm2_asetrd_invsqlty` | MATRIX | .967 | 530 | 123 | 日 | 零中心近正态 | ✅ 备选 |
| 6 | `rsk70_mfm2_asetrd_size` | MATRIX | .967 | 508 | 132 | 日 | 零中心近正态 | 🅢 规模壳 / 备选 |
| 7 | `rsk70_mfm2_asetrd_beta` | MATRIX | .967 | 499 | 150 | 日 | 零中心近正态 | ⛔ 风险68 已实测 beta 漂移 0.09 |
| 8 | `rsk70_mfm2_asetrd_profit` | MATRIX | .967 | 467 | 107 | 日 | 零中心近正态 | ✅ 备选 |
| 9 | `rsk70_mfm2_asetrd_momentum` | MATRIX | .967 | 460 | 123 | 日 | 零中心近正态 | ✅ 备选（载荷变化 = 动量暴露漂移） |
| 10 | `rsk70_mfm2_asetrd_ltrevrsl` | MATRIX | .967 | 434 | 127 | 日 | 零中心近正态 | ✅ 备选 |
| 11 | `rsk70_mfm2_asetrd_indmom` | MATRIX | .967 | 427 | 102 | 日 | 零中心近正态 | ✅ 备选 |
| 12 | `rsk70_mfm2_asetrd_leverage` | MATRIX | .967 | 416 | 120 | 日 | 零中心近正态 | ✅ 备选 |
| 13 | `rsk70_mfm2_asetrd_midcap` | MATRIX | .967 | 414 | 94 | 日 | 零中心近正态 | ✅ 备选 |
| 14 | `rsk70_mfm2_asetrd_divyild` | MATRIX | .967 | 274 | 108 | 日 | 零中心近正态 | ✅ 备选 |
| 15 | `rsk70_mfm2_asetrd_earnqlty` | MATRIX | .967 | 255 | 86 | 日 | 零中心近正态 | ✅ 备选 |
| 16 | `rsk70_mfm2_asetrd_shortint` | MATRIX | .967 | 248 | 91 | 日 | 零中心近正态 | ✅ 备选（空头兴趣载荷） |
| 17 | `rsk70_mfm2_asetrd_strevrsl` | MATRIX | .967 | 199 | 77 | 日 | 零中心近正态 | ✅ 备选 |
| 18 | `rsk70_mfm2_asetrd_earnvar` | MATRIX | .967 | 607 | 121 | 日 | 零中心近正态 | ✅ 备选（盈利波动载荷，非特异风险） |
| 19 | `rsk70_mfm2_asetrd_season` | MATRIX | .967 | 703 | 107 | 日 | 零中心近正态 | ✅ 备选（季节性因子载荷，KOR 未测） |
| 20 | `rsk70_mfm2_asetrd_cnt_kor` | MATRIX | .967 | 428 | 117 | 日 | 零中心近正态 | ⛔ 单国家宇宙 ⇒ 全市场共线，**与 country 中性化等价** |
| 21 | `rsk70_mfm2_asetrd_cntadj` | MATRIX | .943 | 249 | 93 | 日 | 零中心近正态 | ⛔ 同上（国家调整） |
| 22 | `rsk70_mfm2_asetrd_indadj` | MATRIX | .943 | 307 | 101 | 日 | 零中心近正态 | ▦ 行业调整轴 |
| 23 | `rsk70_mfm2_asetrd_srtindcnt` | MATRIX | .967 | **1431** | 225 | 日 | 待实测 | ✅ **第三轴（描述含糊，需实测辨义）** |
| 24 | `rsk70_mfm2_asetrd_primaryindustry` | MATRIX | .962 | 126 | 56 | 日 | 哑变量型 | ▦ 行业主轴 |
| 25 | `rsk70_mfm2_asetrd_market` | MATRIX | .967 | 58 | 35 | 日 | 常数≈1 | ⛔ 市场因子载荷（KOR 全市场≈1） |
| 26 | `rsk70_mfm2_asetrd_newssent` | MATRIX | .967 | 93 | 40 | 日 | 零中心近正态 | ✅ 备选（新闻情绪载荷，与 news 塔不同源 ⇒ 不与已死 news 族撞车） |
| 27 | `rsk70_mfm2_asetrd_resvol` | MATRIX | .967 | 1006 | 231 | 日 | 单边恒正右偏 | ⛔ 特异波动载荷，与 `srisk` 同族（wave214 判死） |

### 1.2 行业载荷（20）—— ▦ 仅分组轴

`airlines`(85) · `autocomp`(90) · `banks`(71) · `capgoods`(72) · `commsvcs`(47) · `consdur`(80) · `constr`(68) ·
`consvcs`(58) · `divfinan`(78) · `foodprd`(55) · `foodretl`(57) · `hardware`(74) · `health`(74) · `hshldprd`(61) ·
`insuran`(52) · `machin`(91) · `metals`(130) · `oilgas`(70) · `othermat`(425) · `pharmac`(79) · `realest`(45) ·
`retail`(63) · `semicond`(106) · `software`(94) · `telecom`(87) · `transprt`(66) · `utility`(56)
（全部 MATRIX / cov .967 / 日频 / 0-1 型哑变量 ⇒ **不作信号**）

### 1.3 特异风险 / 收益（4）—— ⛔ 全部禁入

| # | field | cov | aC | U | 形态 | 裁定 |
|---|---|---|---:|---:|---|---|
| 1 | `rsk70_mfm2_asetrd_srisk` | .967 | 473 | 150 | 单边恒正 `%²` | ⛔ wave214 实测 0.57 / 反向 0.73，**S<1.0 年 5/10 + 单年占 31.5%** |
| 2 | `rsk70_mfm2_asetrd_srisku` | .967 | 588 | 189 | 单边恒正 `%²` | ⛔ 与 `srisk` 逐位相同（同一量） |
| 3 | `rsk70_mfm2_asetrd_resvol` | .967 | 1006 | 231 | 单边恒正 | ⛔ 同上族 |
| 4 | `rsk70_mfm2_asetrd_dsrt` | .967 | 1063 | 252 | 日频流量 | ⛔ `KOR-RISK71-RESIDUAL-REVERSAL-2Y-DEAD`（同一量） |

### 1.4 ★ 非载荷经济字段（8）—— ✅ 本轮新增攻击面（历史上从未测过）

| # | field | type | cov | aC | U | 频率 | 形态 | 机制定位 |
|---|---|---|---:|---:|---:|---|---|---|
| 1 | `hedge_fund_ownership_percentage` | MATRIX | **1.0** | 22 | 15 | 季（13F/申报口径） | 0–1 比例、右偏 | **对冲基金持股占比** = smart money 存量 |
| 2 | `hedge_fund_number_owners` | MATRIX | **1.0** | 20 | 18 | 季 | 计数、右偏 | **持有对冲基金家数** = smart money 广度 |
| 3 | `sector_relative_momentum` | MATRIX | **1.0** | 22 | 13 | 日 | 零中心 | **行业内相对动量**（风控模型内建） |
| 4 | `short_term_industry_country_factor` | MATRIX | **1.0** | 44 | 26 | 日 | 零中心 | **短周期行业×国家合成因子暴露** |
| 5 | `broad_market_exposure_factor` | MATRIX | 1.0 | 10 | 6 | 日 | ≈1 | 市场总暴露（≈beta）⇒ ⛔ 同 beta |
| 6 | `country_adjustment_factor_2` | MATRIX | 1.0 | 12 | 10 | 日 | 常数 | 国家调整乘数 ⇒ ⛔ 单国家无信息 |
| 7 | `industry_adjustment_factor_3` | MATRIX | .9923 | 13 | 12 | 日 | 常数 | 行业调整乘数 ⇒ ⛔ 低优先 |
| 8 | `us_equity_short_interest_ratio` | MATRIX | 1.0 | 10 | 10 | 日 | 0–1 | **美股**空头比例 ⇒ KOR TOP600 内大概率全 0（待实测；若全 0 则零方差） |

### 1.5 分组 / 规模辅件（21）—— ▦/🅢

`sector_exposure_*` 21 支（cov 全 1.0，aC 0–12，行业哑变量）·
`apacm6_total_market_cap_usd`(aC81) / `current_market_cap_usd`(aC90) / `alternative_market_cap_usd`(risk88) ⇒ 🅢 规模壳（**属本数据集 ⇒ `vector_neut` 不破坏 ATOM**）·
`us_equity_consumer_durables_flag` / `us_equity_insurance_sector_flag` / `us_equity_korea_country_flag` / `us_equity_retail_sector_flag` ⇒ ▦ 哑变量

---

## 2. 字段画像五问（0.3，A-1）

| # | 问 | 答 | 决策 |
|---|---|---|---|
| 1 | **时间维度** | 载荷/风险 = **存量水平**（每交易日一个横截面快照）；`dsrt` = 日频流量 | 存量 ⇒ 铁律 A 只对单边恒正量（`srisk/resvol`）生效；**载荷可正可负 ⇒ 不适用铁律 A，禁裸水平做多空须先秩化** |
| 2 | **相对性** | **排序差异**为主：载荷绝对值无经济含义，只有横截面相对位置有意义 | `group_rank` / `zscore`；禁裸水平 |
| 3 | **被定价的是谁** | **强度**（对因子的敏感度），不是广度 | 按敏感度排序；**变化率另立机制**（style drift），不与水平混用 |
| 4 | **有无博弈** | **有且极强**：`anlystsn` 622 users / 2922 alphas；`earnyild` 582 / 1795 ⇒ 头部两轴已被大量占用 | 任何头部轴候选**首颗就查 prod**（`prod_first_skeleton_v1`），不摊完再查 |
| 5 | **事件性** | **否**：cov .967 连续、逐日重估 | 禁 `trade_when` 门控（会把连续信号切碎） |

## 3. 预处理决策（体征 → 骨架）

| 体征 | 决策 |
|---|---|
| cov .967（3.3% NaN） | `ts_backfill(F, 5/22/40)` 前置（回填覆盖本身是信号强度来源；`days_from_last_change` 门控实测毁 S） |
| 载荷零中心、量级无意义 | 必须 `rank` / `group_rank`；**粗轴优先**（risk59 实证 sector > industry > subindustry 单调更差） |
| `srisk/resvol` 单边恒正 | 铁律 A：`ts_delta` 变化率；但**已实测 ΔIVOL 归零**（S −0.04）⇒ IVOL 只有水平信息，且水平已判死 |
| 头部两轴 αC >1700 | 拥挤；任何候选**先查 prod 再谈 S** |
| 风格载荷 27 支 | **一条腿只出 1 颗**；同族多支（value: earnyild/btop；reversal: strevrsl/ltrevrsl；vol: resvol/earnvar）**不可当独立腿** |
| `hedge_fund_*` 季频 | 窗口 ≥66（取 66/126/252）；短窗会被 NaN 污染 |
| 行业载荷 20 支 + `sector_exposure_*` | 只作分组轴 |
| `dsrt` | 排除（继承 risk71/72 判死） |

---

## 4. 机制（A-2 收益来源声明）—— 三条独立机制

### M1 · 分析师情绪载荷（`anlystsn`，αC 2922）

| 声明项 | 内容 |
|---|---|
| **谁在被定价** | 卖方分析师情绪驱动的**趋势跟随资金**（KOR 散户 + 主题基金） |
| **为什么会被错** | 个股对「分析师情绪因子」的载荷高 ⇒ 其收益被分析师预期修正主导；KOR 修正周期存在**延迟反应（post-revision drift）**与**过度外推**两段，方向由哪一段主导须实测 |
| **错了多久修复** | 1–3 个月（22–66d） |
| **预期方向** | 双向（铁律 B 各测一条）：正 = 修正漂移延续；反 = 外推过度回吐 |
| **失效条件** | 分析师覆盖稀疏股（载荷估计噪声大）；风险模型版本切换 |

### M2 · 风格漂移（style drift = 载荷变化率）

| 声明项 | 内容 |
|---|---|
| **谁在被定价** | 风格轮动的**滞后追随者**（按风格标签配置的资金） |
| **为什么会被错** | 载荷上升 = 个股特征向该风格靠拢；资金按标签调仓有滞后 ⇒ 载荷变化领先于资金流 |
| **错了多久修复** | 1–2 季（66–126d） |
| **预期方向** | 载荷向「当期占优风格」漂移 ⇒ 后续跑赢；方向随风格而定 ⇒ 逐轴正反各测 |

### M3 · 对冲基金持股（`hedge_fund_ownership_percentage` / `hedge_fund_number_owners`）

| 声明项 | 内容 |
|---|---|
| **谁在被定价** | 对冲基金（informed traders）vs 后知后觉的散户 |
| **为什么会被错** | 申报口径有滞后（季频），且 KOR 以散户为主、机构持仓信息被系统性低估 ⇒ **smart money 累积未被定价** |
| **错了多久修复** | 1–2 季（66–126d） |
| **预期方向** | 持股占比 / 家数**上升** ⇒ 后续跑赢（正）；下降 ⇒ 跑输 |
| **失效条件** | ⚠ `institutions6`（全机构持仓）已判死（S ≤0.8）⇒ 对冲基金是**子集**，若同死于本区，说明申报口径持仓在 KOR 无信息 |

### M4 · 行业内相对动量（`sector_relative_momentum`）

| 声明项 | 内容 |
|---|---|
| **谁在被定价** | 行业内轮动资金 |
| **为什么会被错** | 行业内相对赢家被继续追捧（行业内动量）或过度反应后回吐（行业内反转） |
| **错了多久修复** | 1–3 月 |
| **预期方向** | 双向各测（KOR 短周期以反转为主，长周期动量弱） |

---

## 5. 双通道取证（②.d）

### 通道 A｜平台论坛
| 检索式 | 状态 |
|---|---|
| `risk model factor loading alpha` | 本轮待查 |
| `analyst sentiment factor loading` | 本轮待查 |
| `hedge fund ownership` | 本轮待查 |
| `industry relative momentum` | 本轮待查 |

（`risk70.md` 已记录：wave 214 的 IVOL 双通道已完成 —— 论坛帖 `43607291078935`「特质波动率之谜」+ KOSPI/KOSDAQ 1997–2016 IVOL 文献；
本轮**不复用**该机制，改打载荷轴与持股轴。）

### 通道 B｜外部文献
| 机制 | 文献 | 可证伪结论 | 本区可迁移性 |
|---|---|---|---|
| M1 分析师修正漂移 | Stickel (1991, JF)；Gleason & Lee (2003, TAR) | 上调 ⇒ 后续 3–12 月正异常；延迟反应是**修正数量**的函数 | ⭐ KOR 已实测 analyst 数据集修正族 S 1.40–1.66 ⇒ **机制在 KOR 成立**；本集载荷是其**平滑暴露**，可迁移但须实测 |
| M2 风格漂移 / 特征动量 | Ehsani & Linnainmaa (2022, JF)「Factor Momentum」；Arnott et al. (2019) | 因子动量来自**个股特征变化的时序自相关**，非因子收益自相关 | ⚠ 美股样本；KOR 小宇宙需实测 |
| M3 对冲基金持股 | Griffin & Xu (2009, JF)；Aragon & Martin (2012) | 对冲基金持仓变化对后续收益有正预测力，且强于共同基金 | ⚠ 美股 13F 样本；KOR 由 vendor 映射，口径未知 ⇒ 先当假说 |
| M4 行业内动量 | Moskowitz & Grinblatt (1999, JF) | 行业内动量解释大部分个股动量 | ⚠ USA；KOR 动量弱、反转强 ⇒ 方向可反 |

⚠ **文献偏误**：以上全部为美股样本。KOR 散户占比高、卖空受限、涨跌停制度 ⇒ **先当假说，本区实测定生死**。

---

## 6. 实测记录

### 6.1 wave 214（历史，2026-10-30，STATISTICAL / decay4 / trunc .08）

| # | alpha | 表达式 | S | F | TO | 2Y |
|---|---|---|---|---|---|---|
| 1 | `9qxP55Vq` | `reverse(group_rank(ts_backfill(rsk70_mfm2_asetrd_srisk,5),sector))` | 0.57 | 0.32 | .0907 | 1.64 |
| 2 | `P0orLLZq` | 同式去 reverse | −0.73 | −0.46 | .0904 | −1.88 |
| 3 | `leA6ww8l` | `reverse(group_rank(ts_delta(...,22),sector))` | −0.04 | 0 | .1738 | 0.08 |
| 4 | `omEwjj6k` | `reverse(group_rank(ts_backfill(srisku,5),sector))` | 0.57 | 0.32 | .0906 | 1.62 |

归因：S<1.0 年份 **5/10**、2022 占正收益 **31.5%** ⇒ IVOL 轴判死（换机制族，不扫参数）。

### 6.2 本轮 wave R1（2026-11-06，P-ATOM-1 / INDUSTRY / decay1 / trunc .04 / nan ON）

见 [`waves.md`](waves.md)。
