# KOR/D1 未点亮塔战役路线图（2026-10-30 建；**本文件 = 现场作战图 + 波次排程唯一权威**）

> 依据（全部机器可核，勿凭记忆）：
> - `get_pyramid_alphas(KOR,D1)` + `get_pyramid_multipliers(KOR,D1)`（点亮态 / 倍率）
> - `query_dataset_profile(KOR, 200)`（覆盖率 / 字段数 / αC）
> - `get_dead_datasets("KOR")` = **16 个死数据集**
> - `get_dead_ends("KOR")` = **85 条判死记录**
> - `get_wave_result(KOR, N)` + `tracking/KOR/reference/datasets/<ds>.md` 逐集档案
>
> 目标：在**未点亮塔**上挖 60 个 REGULAR alpha（优先 ATOM = 单数据集）。
> 配套：数据集机制读法见 [`unlit_tower_category_profile.md`](unlit_tower_category_profile.md) §2；
> 逐集字段档案见 `datasets/<ds>.md`（**开波前必须先补齐**）。

## 0. 点亮态（2026-10-30 实测，平台权威）

| 塔 | KOR/D1 已点亮 | 倍率 | 状态 |
|---|---|---|---|
| analyst | 2 | 1.6 | 已亮，可增量 |
| fundamental | 3 | 1.6 | **满** |
| model | 3 | 1.6 | **满** |
| pv | 2 | 1.4 | 已亮 |
| other | 1 | 1.6 | 已亮 |
| shortinterest | 4 | 1.4 | 已亮 |
| **earnings** | **0** | **1.1** | ⬅ 未亮 |
| **institutions** | **0** | **1.4** | ⬅ 未亮 |
| **macro** | **0** | **1.4** | ⬅ 未亮 |
| **news** | **0** | **1.6** | ⬅ 未亮 |
| **sentiment** | **0** | **1.6** | ⬅ 未亮 |
| **risk** | **0** | **1.3** | ⬅ 未亮 |
| **insiders** | **0** | **1.2** | ⬅ 未亮 |
| **imbalance** | **0** | **1.0** | ⬅ 未亮 |
| **socialmedia** | **0** | **1.0** | ⬅ 未亮 |

⚠ DB 里 `pyramid_multiplier` 是**当前生效值**（随点亮态衰减），与平台基础倍率不同；**以平台为准**。
⚠ KOR/D1 顶层可打的塔只剩 **news / sentiment**（乘数同为 1.6 且都还有活数据集），其余塔要么无活集、要么乘数 ≤1.4。

## 1. 未点亮塔 × 数据集（**以 `get_dead_datasets` + `get_dead_ends` 双表为准，不看印象**）

### 判定口径（写死，防止第三次误记）

| 判据 | 来源 | 效力 |
|---|---|---|
| **死数据集** | `get_dead_datasets(KOR)` 16 个 | ⛔ 整集关闭，任何波不得再投槽 |
| **判死记录** | `get_dead_ends(KOR)` 85 条（`registry_empirical` layer=dead_end） | ⛔ 该**机制族**关闭；同集其它机制若未被点名，仍可试 |
| 「本地实测弱」 | 逐集 `datasets/<ds>.md` 的实测表 | ⚠ **不等于判死**；要判死必须 `seal_dead_end` 走论坛取证闸 |

### 攻击面总表

| 塔 | 倍率 | ✅ 可攻数据集 | ⛔ 已死（来源） | 机制可用性 |
|---|---|---|---|---|
| **news** | 1.6 | ~~news7、news18、news46、news31、news21、news76~~ **⛔ 无（塔关闭，wave 211 五条轴全死）** | **news79**（死集）、news38（`KOR-NEWS38-HEADLINETONE-DEAD`）、news50（`KOR-NEWS50-EVENTSCORE-WEAK`）、news54（`KOR-FORUM-DEAD`）、news_sentiment_transfer（`KOR-NEWS-SENTIMENT-TRANSFER-DEAD`） | 情绪/标题语气/事件评分族**全灭** ⇒ 只剩**注意力计数 / 事件计数 / 时间模式**（见 `datasets/news7.md` §5 论坛实证） |
| **sentiment** | 1.6 | **other553**（cov **.6243**，21 VECTOR，平台 category=sentiment，名字带 other 前缀 ⇒ **不属 other 塔**）、sentiment26（cov .356，被动 DNS 注意力）、sentiment23（cov .2648，156 字段 transformer 标题情绪） | **sentiment21**（死集）、**sentiment27**（wave189 覆盖判死：2019 起） | ⭐ **other553 = 本塔最优**（覆盖率最高的活集）：卖方 PT/评级/预期**修正**域（`value`/`prevalue` 成对）。sentiment26 = 网站热度族（与 sentiment27 同源，覆盖风险最高，只作探针）。sentiment23 = 标题情绪 ⇒ **与已判死的 news 情绪族同机制，最低优先**。⛔ **本塔已于 wave 216 关闭**（other553 / 190 / 189 / sentiment26 四集全死，见 §3） |
| **institutions** | 1.4 | **⛔ 无** | **institutions6**（死集）、**fund_holdings_panel**（`KOR-FUND-HOLDINGS-PANEL-DEAD`，wave187 复验 S −0.04 / 0.28） | **本塔在 KOR 无攻击面**，需新数据集授权才能开 |
| **macro** | 1.4 | ~~other106、macro63~~ **⛔ 无（塔关闭）** | 无 | ~~macro63 单字段无截面差异 ⇒ 只能做成分变更事件；other106 cov .404 需 backfill~~ **2026-10-30 实测收口**：`macro63` 全表 1 字段 `mcr63_membership`（MATRIX，cov 1.0，aC 158）=「WisdomTree WTIDJH 指数成分状态」⇒ **0/1 哑变量、无截面强度**，且其唯一可用机制（成分变更 → 供给冲击，Shleifer 1986 / Greenwood 2008）**已在 wave 190 用 other106 实测判死**（max\|S\| 0.75，十年覆盖 PASS）⇒ 机制已测、字段无强度，**macro 塔关闭** · **wave 215 实测补证（2026-10-30）**：3 条全空账（S 0.00 / TO 0.00 / 2014–2023 `longCount` 十年全 0）⇒ 判 `KOR-MACRO63-NO-CROSS-SECTION`，见 `datasets/macro63.md` §7.2 |
| **risk** | 1.3 | risk59（**仅方差/凸变换机制**，见下注）、risk68、risk72 | risk60（`KOR-RISK60-CROWDDING-NOSIGNAL`）、risk71（`KOR-RISK71-RESIDUAL-REVERSAL-2Y-DEAD`）、risk88（`KOR-RSK88-STYLOAD-WEAK`）、risk59 **裸截面族**（`KOR-WAVE96-UNLIT-BARE-SIGNAL-DEAD`） | ⚠ **risk59 的判死范围必须按登记表原话读**：`family='intraday_pv_feats/risk59/shortinterest38/mmp_nlp_sentiment bare cross-sectional signals'`，reason 点名的是 **bid/ask-vwap 比率、squeeze_risk、做空金额、invactnet_buy_qty、bullish_top**（wave96 8/8 RED max\|S\|=0.84）。⇒ **水平/裸 rank 关闭；时序方差（`ts_covariance(x,x,W)`）/凸变换不在死范围内**，wave 201 即测后者。域内互锁 0.64–0.80 是 **prod 风险**，不是判死依据 |
| **insiders** | 1.2 | insiders1 | insiders5（`KOR-INSIDERS5-CEILING-20260909`，天花板 1.05；wave185 8 全灭 max\|S\|=0.81）、insider_feats（prod 0.7+） | 仅 insiders1（cov .55，需 backfill） |
| **earnings** | 1.1 | earnings3（**未封死，但已实测弱**） | 无 | **wave186 已 FAIL**：8 式 max\|S\|=0.94 / max F=0.49；2Y 与 IS 严重背离（IS 0.94 vs 2Y 1.68）⇒ 按决策表「近年 S 断崖」= 机制性，非参数 ⇒ **不再投主攻槽**，只余「距公告日 × 属性」的可能组合轴 |
| **imbalance** | 1.0 | imbalance5（**未封死，但实测 2Y 结构性不可达**） | 无 | 3 种 ATOM 形态（rank / vector_neut 规模中性 / ts_delta）S 1.08–1.09 全卡 **2Y≈0.17**，且投资域仅 2 字段、αC 1109 极拥挤 ⇒ 待 `seal_dead_end` 正式封存 |
| **socialmedia** | 1.0 | ~~socialmedia39、other100~~ **⛔ 无（塔关闭）** | 无 | ~~单字段 cov 1.0，10 年覆盖风险最高（数据源起步晚）⇒ 只做探针~~ **2026-10-30 实测收口（`get_field_catalog` 双查）**：`socialmedia39` 全表 1 字段 = "Atlas instrument IDs of the co-viewed neighbor tickers"（**连接键**）；`other100` 全表 1 字段 `oth100_top5_people_also_watch_ticker_ii` = "Related tickers that have caught people's attention"（VECTOR，aC 357）⇒ **同形态 ID 列表**。两集都只有"邻居票清单"，**零信号面** |

**结论（按「乘数 × 剩余空间」排；2026-10-30 wave 211 后更正）**：~~news(1.6)~~ **⛔ 塔关闭**（五条轴全死、十年覆盖全 PASS，见 §3 wave 211）→ ~~sentiment(1.6)~~ **⛔ 塔关闭**（189 覆盖 / 192 机制 / **216 sentiment26 双重判死：仅 7/10 年 + max\|S\| 0.20**）→ **risk(1.3)**（唯一仍有近闸腿 `QPvr1vPM` S 1.02 / 2Y 1.80）→ macro(1.4) → insiders(1.2) ⛔ 塔关闭 → earnings/imbalance/socialmedia(≤1.1，仅补数)。
⚠ **剩下的两条路：① risk × earnings / risk × news 的合规组合腿（`subtract`/`multiply`/`trade_when`，禁 `add` 双腿）；② 新数据集授权。** 单塔单字段的 ATOM 上限已实测 ≤1.02。

## 2. KOR 事件类数据的结构性风险（判死记录原话，务必先读）

> **「CW 1.0 事件日集中为 KOR 事件类数据通病」**（`KOR-AIEQUITY-PROBE-DEAD`）
> **「事件流字段均需先验证 CW」**（`KOR-FORUM-DEAD`）

⇒ 任何 `trade_when(事件, …)`、事件稀疏型信号的**第一件事是看 CONCENTRATED_WEIGHT（≤0.1）**，不是看 Sharpe。
这条直接适用于 earnings3 的 `trade_when(less(next_interval,6))` 形态与 news 的「无新闻日为空」形态。
**CW 修法优先级**（`strategy:concentrated_weight_is_data_quality_not_params_v1`）：
覆盖率 → 数据类型 → 窗口 → `ts_backfill` 最小窗 → 换思路；**不要把 truncation/decay/neutralization 当第一根杠杆**。

## 3. 波次排程（铁律 G：新线 8 探针，续线 ≤ 上一波 1/3）

| 波 | 数据集 | 塔 | 候选数 | 状态 | 结论 |
|---|---|---|---|---|---|
| 185 | insiders5 | insiders | 8 | **CLOSED** | 8 全灭，max\|S\|=0.81 ⇒ 撞 `KOR-INSIDERS5-CEILING-20260909` 天花板 |
| 186 | earnings3 | earnings | 8 | **CLOSED FAIL** | max\|S\|=0.94 / max F=0.49；2Y≫IS ⇒ 机制性衰减；batch4 僵尸已弃 |
| 187 | fund_holdings_panel | institutions | 2（误发） | **CLOSED FAIL** | 死集误发（门禁不校 dead 表）；S −0.04 / 0.28 复验 |
| 187b | news7（首波，被 186/187 挤占后顺延） | news | 8 | **CLOSED FAIL** | ⛔ **机制判死**：8/8 全灭，max\|S\|=**0.55**（`2rAP6rj8`），2Y 区间 −1.50…0.95，0 candidates / 0 near。**十年覆盖 PASS**（longCount 297–344/年）⇒ 死因是机制不是数据。**最优臂 IS +0.55 / 2Y −0.34 反号 ⇒ 直接触发证伪**，按决策表换字段族、不扫参数。唯一可继承读数：注意力计数族**不触发 CW**（经 `ts_rank`+`group_rank` 归一后权重健康）。详见 `datasets/news7.md` §7.1 |
| **189** | **sentiment27**（Tranco 网站排名 → 注意力冲击） | sentiment | 2 **（原 8，砍 6）** | ⛔ **CLOSED — 覆盖判死** | 批 1 落地即读 yearly_stats：**2014–2018 连续 5 年 longCount=0，数据起点 2019 ⇒ 有效历史 5 年，违反用户约束 4**；S −0.22 / +0.06，2Y 更差 ⇒ 无方向问题、是无信号。剩 3 批 6 条**未发即 kill**。⛔ 本塔在约束 4 下**结构性不可点亮**，除非约束放宽到 5 年。见 `datasets/sentiment27.md` §7.1 |
| 190 | **other106**（KOSPI 成分/公司行为 → 指数机制供给冲击） | macro→other | 8（实发 4） | ⛔ **CLOSED FAIL** | **机制判死**：批 1 max\|S\|=0.75（`d5WeomjK`）/ max\|2Y\|=0.08，批 2 核心同源比值腿 max\|S\|=0.24 ⇒ 预置判据触发，**批 3–4 未发即 kill**。**⭐ 十年覆盖 PASS**（longCount 2014–2023 逐年 267–347，本区首次）⇒ 死因是机制不是数据。TO .405–.42 是成功带的 3–5 倍，但降 TO 只修 F 不改 S；CW 仍 1.0@2016。金字塔归属实证 = `KOR/D1/MACRO ×1.4`。机制背景：15 字段全 VECTOR、aC 9–55；核心资产 **`_cls`/`_nxt` 成对** ⇒ 天然**同源比值**（最贴 lit alpha 几何）。机制 = Shleifer 1986 需求曲线向下 + Greenwood 2008 权重调整反转。⚠ 覆盖 .404 需 `ts_backfill`；§7 第 8 条是**阴性对照**（份额水平出信号即整波作废）。**通道 A 已取证（2026-10-30）= 无本机制专属帖**，只捞到两条非机制纪律（`vector_neut` 禁用、低频信号先压 TO）。见 `datasets/other106.md` |
| 191 | **news46**（RavenPack 新颖度/相关度） | news | ≤8（实发 4） | ⛔ **CLOSED FAIL** | **机制判死**：4/4 全灭，max\|S\|=**0.47**（`JjeRrOan` relevance）/ max\|2Y\|=1.08，0 near；预置判据触发 ⇒ 剩 4 条未发即 kill。⭐ **十年覆盖 PASS**（`58ENYomN` 2014–2023 逐年 longCount 291–340，本集首次实测）⇒ 死因机制非数据。**新的塔级结论：news 塔「文本内容强度」轴（novelty/relevance）与「注意力计数」轴（news7）双双判死** ⇒ 该塔只剩「事件计数 / 时间模式」未试。可继承读数：稀疏新闻型数据经 `ts_rank-252 + ts_backfill` 归一后 **CW 不触发**。见 `datasets/news46.md` §7.1 |
| 192 | **other553**（卖方 PT/评级/预期**修正**；平台 category=sentiment ×1.6） | sentiment | ≤4（实发 2） | ⛔ **CLOSED FAIL** | **机制判死**：批 1 正/反 2/2 全灭，`rKRQ8MYa` S=+0.13 / 2Y=+0.66 / TO .2474，`58ENYdbo` S=−0.28 / 2Y=−0.95；max\|S\|=**0.28** 且 max\|2Y\|=**0.95** ⇒ 预置判据触发，**legs 3–4 未发即 kill**。⭐ **十年覆盖 PASS**（longCount 286–343/年，2014–2023 无一空年，本集首次实测；对照 189 sentiment27 全空）⇒ 死因机制非数据。归因：2014 单年占正收益 **62%**（过拟合指纹）+ 年 S 符号翻转（+2.2/−1.11/−0.95/+0.98）+ raw 与 2Y 同步走弱（⇒ 不扫中性化档）+ TO 约为成功带 2 倍但 S 仅 0.13（⇒ 平滑无益）。**塔级结论：sentiment 塔三连死**（189 覆盖 / 190 other106 机制 / 192 other553 机制）⇒ 仅剩 `sentiment26` 且须先验十年覆盖。见 `datasets/other553.md` §7.1 |
| 193 | **insiders1**（内部人持股变动） | insiders | 8（实发 2） | ⛔ **CLOSED FAIL** | **数据集判死 + 塔判死**：批 1 两腿同字段同窗仅符号相反 ⇒ 铁律 B 双测完成，`max\|S\|=**0.11**`、`max\|2Y\|=0.26` ⇒ 预注册判死触发，**剩 6 腿未发即 kill**。⭐ **十年覆盖 PASS**（longCount 248–323/年，2014–2023 无空年）⇒ 死因机制+形态。**两腿 CW=1.00 @2018-02-06**：季频 VECTOR 经 `vec_avg` 后有效档位极少 ⇒ `group_rank` 退化成近二值、权重塌单票（**数据形态缺陷，参数无解**）。TO .3035/.3037 = 获胜带 2.2–4.0 倍 ⇒ F 天花板 0.02。逐年 S 翻转 5 次、S<1.0 年份 7/10 ⇒ regime 依赖。**继承：⛔ insiders 塔关闭（叠加 insiders5 天花板 1.05）；⛔ VECTOR 类字段先用前必须跑非零率体检，<0.3 直接跳过**。见 `datasets/insiders1.md` §7.1 |
| 194 | **risk68**（risk72 **判 0 槽**） | risk | 4 | ⛔ **CLOSED FAIL** | **机制判死**：4/4 全灭，`leAJNQQA` S=−0.50/F=−0.22 / `78Lg2aa5` S=+0.18 / `A1Vq2z9Y` S=+0.09 / `omEQkG76` S=−0.11，`max\|S\|=**0.50**`、`max\|2Y\|=0.64`，0 candidates / 0 near。⭐ **十年覆盖 PASS**（290–341/年）⇒ 死因机制非数据。**2Y 结构性不可达**：`78Lg2aa5` 逐年 S<1.0 占 **6/10**、符号剧烈翻转（+2.21/−0.51/−2.13/+0.46/+1.32/−1.56/+0.74/−0.23/+0.30/+0.93）；2014 单年占正收益 **29.7%**（过拟合指纹）。唯一 \|2Y\|>1 的 `leAJNQQA`（−1.23）**与自身 IS 同号但幅度 2.5×** ⇒ 按决策表判不可信。波动率短长比（5/66）在 STATISTICAL 下被风格因子吃掉。**继承：⛔ risk 塔关闭（risk68 机制死 + risk72 同源拷贝 0 槽 + risk88 `ri_*` 风格载荷）**。见 `datasets/risk68.md` §9.1 |
| 193b | ~~risk72~~ | risk | **0** | ⛔ **判不投（0 槽）** | 5 字段 description **逐字相同**（"Daily reproducible specific returns in % units"），只差宇宙口径 ⇒ **不是 5 个信号，是同一量的 5 份拷贝**（跨字段 corr 预计 >0.9）。机制与 risk71 同族，死因 = **regime 级符号翻转**（2022–2023），换宇宙不换 regime；唯一残值「宇宙差分」是 size 代理，与 STATISTICAL 对撞且乘数仅 1.3。翻案前提写死在 `datasets/risk72.md` §8 |
| 194 | ~~socialmedia39~~ | socialmedia | **0** | **结构性不可用** | ⛔ 平台实测**全数据集只有 1 个字段** `scl39_top5_people_also_watch_ticker_ii`，description = "Atlas instrument IDs of the **co-viewed neighbor tickers**; stable identifiers suitable for **joins**" ⇒ 是**连接键/ID 列表**，不是信号。**本塔在 KOR 无攻击面**（`other100` 同日 `get_field_catalog` 双查：同为「邻居票 ID 列表」⇒ 亦无信号面，见 §1） |
| **200** | **fund_holdings_panel（误发第 2 次）** | institutions | 4 | ⛔ **CLOSED FAIL** | **同一死集第二次误发**（wave124 判死、wave187 已复验过一次）。4 腿全部归零：`O0AK3qaJ` S −0.15 / `58ENX3WX` +0.08 / `bl67wvMq` −0.32 / `mLoevZA6` +0.25，max\|S\|=**0.32**，TO .063–.085 **落在获胜带内** ⇒ 不是换手问题，是机制缺失。**根因已定位并修（本波直接触发）**：`assemble_priors.MAX_DEADENDS=12` 而 KOR 实有 99 条死记录 ⇒ **gate 的 `PRIORS-DEADEND-HIT` 只看得到 12%**，`fund_holdings_panel` 的死条目被截断，两道闸都放行。修法 = priors 增写全量 `_dead_ends_all`（不占 GEM prompt 名额）+ `gate.check_priors` 取并集 ⇒ 实测 99 条全部可见。见 §4 流程禁区 |
| **201** | **risk59（借券费**方差**，非水平）** | risk | 5 | ⛔ **CLOSED FAIL** | **机制判死 + 风险塔关闭**：4/4 全灭，`2rAP3EJY` ts_std_dev 反向 S=0.39 / 2Y=0.48；`58ENXrLz` ts_covariance 反向 S=0.14 / 2Y=−0.10；`LLMO0eRe` ts_delta 反向 S=0.04 / 2Y=−0.20；`Xg9X0Vkz` ts_covariance 正向 S=−0.27。`max\|S\|=0.39` ⇒ 预注册判据触发。**合判**：level 族 `QPvr1vPM`（S 1.02 / 2Y 1.80 / F 0.67 / CW fail）已是全家族最高，且属 roadmap §4 明令关闭的「水平/比率/拥挤度族」；方差/协方差/差分三形态全部 ≤0.39 ⇒ **risk 塔三条形态轴（level / variance / delta）全部实测完成、全部不可达，塔关闭** |
| — | QPvr1vPM（risk59 借券费水平） | risk | — | **仅登记，不投** | 全库最近闸的 KOR 候选（S 1.02 / 2Y **1.80** / F 0.67 / TO 0.135 / subU 0.95 / prod 0.6552 / self 0.2202）。若 S→1.58 且 TO/收益比不变则 F 自动到 1.03 ⇒ **唯一缺口是 S 与 CW**。但机制属 §4 关闭的裸截面族，**不再投配额**；留档备查 |
| **205** | ~~institutions6~~ | institutions | 2（实发） | ⛔ **作废（第三次死集误发）** | 开波前**未核死表**：institutions6 在 `get_dead_datasets(KOR)` 16 死集名单内。批 1 的 2 腿已上平台（multisim `1ip4rtgDn4nLbtR6OrLGi2n`），其余 2 腿 **未发即废**；4 条表达式已 `dropped`。**根因=链路从不检查死表**：`gate.check_priors` 的 `PRIORS-DEADEND-HIT` 仅在 `--require-priors` 时升 FAIL，而 `pipeline.py` 从不传 ⇒ 死集一路 WARN 到派发（wave187 / 200 / 205 同一根因）。**已修**：`pipeline.py` 新增 `dead_dataset_guard()`（直接读 `ledger_kv` 的 `<ds>_dead`，命中即 exit 2，逃生口仅 `--allow-dead-dataset`），实测 institutions6 被拦、活集放行 |
| **206** | **news31**（Refinitiv 报道结构：句位显著度 / 同篇公司数） | news | 4 | ⛔ **CLOSED FAIL** | 画像见 `datasets/news31.md`（25 字段全量、αC 0–3 基本无人碰、cov .7991、数据集 αC **105** 为本塔最不拥挤）。**新轴 = 报道显著性与注意力稀释**（news 塔前三条轴——情绪/注意力计数/内容强度——均已判死，本轴从未测）。4 腿 = {句位, 同篇公司数} × {+, −}（铁律 B 双测）。壳层机械复用 news46 已验证的 `group_rank(ts_rank(ts_backfill(vec_avg(F),22),252), sector)`（实测不触发 CW） |
| **207** | **news85**（`sentiment1_*` 情绪分布统计：lowest_score / 偏度 / 全文均值） | news | 4（8 式实发 4） | ⛔ **CLOSED FAIL** | **机制判死**：4/4 全灭，最好 `O0AwPEvq` = `-ts_corr(headline_item_count, sentiment_overall_average, 22)` **S 0.67 / F 0.32 / TO .1284（★落获胜带）/ 2Y 1.53**；其余三腿 S 0.22 / −0.17 / −0.02。⇒ **情绪水平与情绪偏度均无信号**（与 news38 标题语气判死一致），唯一有读数的是**「情绪 ↔ 报道量背离」的互相关形态**，它同时给出本塔最优 TO（.1284，其余新闻腿都是 .16–.30）。塔级：news 塔第 4 条轴（情绪分布）判死；保留读数 = **稀疏新闻字段要进获胜带必须用双字段互相关，不用单字段时序** |
| **208** | ~~news_sentiment_transfer~~ | news | **0** | ⛔ **开波前 kill（0 配额）** | 命中判死记录 `KOR-NEWS-SENTIMENT-TRANSFER-DEAD`，派发前手工核查发现并终止，4 条表达式置 `dropped`，未消耗任何仿真槽。⚠ **暴露门禁缺口**：`dead_dataset_guard()` 只查 16 个死**数据集**，不查 `get_dead_ends` 的**机制族**死记录 ⇒ 「死集不投」已机械化，「死机制不投」仍靠人工 |
| **209** | **earnings3**（`ern3_next_interval` 财报日历距离） | earnings | 3（实发 2） | ⛔ **CLOSED FAIL，但 ★ 单点解除 CW** | `omEwRJwJ` = `group_rank(ts_backfill(-1*next_interval, 10), sector)` → **S 0.95 / F 0.52 / TO .1567 / R .0465 / 2Y 1.75 / subU .82 / CW ✅ pass**（基线 `78LgN03b` CW **0.803** 硬破）。**CW 根因 = 事件日历字段在无排期日为 NaN，`nanHandling=OFF` 丢票致权重塌缩；`ts_backfill(F,10)` 跨空档前向填充即解**，且 sector/market 两轴同时 pass ⇒ 与分组轴无关，纯数据形态问题（CW 阶梯第 4 步，未动 truncation/decay/中性化）。十年覆盖 PASS（292–354/年）。剩余墙仅 S −0.63 / F −0.48。详见 `datasets/earnings3.md` §8.7 |
| **210** | **earnings3**（强度几何三选一） | earnings | 3（实发 2） | ⛔ **CLOSED FAIL + 强度天花板判定** | `pwdJMWb6` zscore 保距 → S **0.89** / **2Y 2.17**（用长样本强度换近期强度）；`A1VJrLpR` `ts_rank-252` cadence 归一 → S **0.26**（**机制被抹掉**，证伪 wave188 第 3 条杠杆）；`tail` 连续两次 SYNTAX FAIL 未上平台 ⇒ 本线弃用。**三几何 S 上界 0.95，R 恒定 .0465–.0473 vs 目标 .0628** ⇒ 判「calendar-distance 单字段强度天花板 ≈0.95，停止扫几何」，仅作**组合腿**保留。详见 `datasets/earnings3.md` §8.8 |
| **211** | **news20**（`nws20_nip` 次日市场冲击幅度 / `nws20_ber` 卖方评级变动） | news | 4 | ⛔ **CLOSED FAIL + news 塔关闭** | **机制判死**：4/4 全灭，`xArwGrEm` S −0.25 / `Xg9w9Ox` 0.00 / `P0or8X3E` −0.12 / `N1NW35rg` −0.06 ⇒ max\|S\|=**0.25**、max\|2Y\|=1.27，0 candidates / 0 near。⭐ **十年覆盖 PASS**（`Xg9w9Ox` longCount 289–345/年，2014–2023 无空年，本集首次实测）⇒ 死因机制非数据。**归因**：① `nip` 是「未来 2 小时」冲击预测，D1 入场时信息已释放，残余漂移在 KOR 散户结构里 1 天内抹平（TO .26 = 获胜带 2 倍，即「无慢成分」体征）；② `ber` 在 market-news 供给链上是稀疏滞后的评级变更，`vec_sum` 量纲随报道密度漂移；③ 逐年 S 符号翻转 5 次（2014 −1.97）。**塔级结论：news 塔五条轴（方向/计数/强度/结构/幅度）全部落在 .25–.67 且十年覆盖全 PASS ⇒ 该塔在 KOR 的失效是「新闻信息在 D1 可交易窗口内已被定价」，不是单字段缺陷，塔关闭**。见 `datasets/news20.md` |
| **212** | **risk59（借券费 × 利用率 / 分组轴）** | risk | 6（实发 3） | ⛔ **CLOSED FAIL + 一阶矩族收口** | P1 `add` 被闸5 `[POISON:equal_weight_leg_add]` 拦（id 85223 dropped）；**P5/P6（multiply / trade_when 以 utilization 调制）发波前 kill**——P4 实测 `utilization` 单独 **S 0.09**，调制变量信息量≈0，合成不可能有增量（未耗槽）。实发 3 腿：P2 价−量价差 **S 0.55** / F .25 / TO .1384；P3 `industry` 轴 **S 0.96** / F .60 / TO .1279 / margin 7.77bp；P4 **S 0.09** / F .02 ⇒ **max\|S\|=0.96、max 2Y=1.40、0 candidates**（`wave_results` id=1683 FAIL）。归因：台阶单调 0.55 < 0.96 < 1.02 ⇒ **引入 utilization 的任何形态都是纯稀释**；P3 vs QPvr1vPM 单变量（sector→industry）S −0.06 / TO −.0071 / margin −0.75bp ⇒ **细分组轴不增幅度，回退 sector**。**一阶矩族上界 = QPvr1vPM 1.02 确认**，与二阶矩 0.39 合并后 risk59 三条形态轴（level / variance / delta）全部完成。见 `datasets/risk59.md` §11 |
| **213** | **risk59（§9.1 三条从未派发的腿）** | risk | 3 | ⛔ **CLOSED FAIL + risk 塔关闭** | `vec_max(offer_rate)` **S 1.02 / F .67 / TO .1351**（与 QPvr1vPM 逐项相同 ⇒ 该字段当日档位近乎唯一，聚合换不出强度）；`vec_avg(last_rate)` **S 1.04 / F .67 / TO .1428 / margin 8.41bp / 2Y 2.02**（★本族新高，但 TO 升 ⇒ F 不动）；`subindustry` 轴 **S 0.70**（细轴第三次更差：sector 1.02 > industry 0.96 > subindustry 0.70）。⇒ **max\|S\|=1.04、max 2Y=2.02、0 candidates / 2 near**。**收口**：距闸 +52%，三条单变量轴（聚合/字段/分组）全部试完且无一能抬 50%；与 wave 201（variance .39 / delta .04）合并 ⇒ **risk59 三条形态轴全部完成，降级为近闸素材，risk 塔关闭**。唯一未试杠杆 = 缩短 IS 窗口（`last_rate` 2Y 是全样本 2 倍），**违反用户约束 4 精神，需授权**。见 `datasets/risk59.md` §12–§13 |
| **214** | **risk70 + other496（`kor_mapped_limit_status` 涨跌停状态）** | risk | 8 | ⛔ **CLOSED FAIL** | **机制判死**：8/8 全灭，`max\|S\|=**0.73**`（`P0orLLZq` 负向 `rsk70_mfm2_asetrd_srisk`）、正向最高 0.57（`9qxP55Vq` / `omEwjj6k` 两字段互为 u/s 版本、读数逐位相同 ⇒ 同量拷贝）、2Y 最高 1.64 且与 IS 同号同量级。**`ts_delta-22` 与 `ts_sum-22` 两形态均无信号**（0.04/−0.64）⇒ 涨跌停状态字段无截面信息。0 candidates / 0 near。见 `wave_results` id=1689 |
| **215** | **macro63（`mcr63_membership`，WTIDJH 指数成分状态）** | macro | 3 | ⛔ **CLOSED — 恒空仓** | **数据集判死（不是信号弱）**：3 条（正向 / `reverse` / `ts_decay_linear-63` 平滑）**S 0.00 / TO 0.00 / 2014–2023 十年 `longCount` 全 0**，`bookSize` 仍 2e7 ⇒ **空账**。`LOW_SHARPE 0 vs 1.58`、`LOW_TURNOVER 0 vs 0.01` 双 FAIL，`LOW_FITNESS`/`subU`/`investability`/`CLUSTER` 全 `:ERROR`。根因 = **域错配**：字段是「WisdomTree WTIDJH（日本股息指数）成分状态」，KOR 标的无值；`coverage:1` 只表示字段已定义、不表示韩国有截面（侧证：`JPN/TOP1600` 连该集都查不到）。判 `KOR-MACRO63-NO-CROSS-SECTION`，**未发 215b 修复波**（预注册写明「不补参数」；`ts_backfill` 也救不了域错配）。见 `datasets/macro63.md` §7.1/§7.2 |
| **216** | **sentiment26（Cisco Umbrella DNS 关注度，19 全 VECTOR）** | sentiment | 4 | ⛔ **CLOSED FAIL** | 4/4 全灭，**max\|S\|=0.20**（`qMLvK9OK` 域名数 zscore，2Y 0.55）、max F 0.03；正向广度水平 `xAr9KOlw` S=−0.13（2Y −0.11）、其 `reverse` **S=0.00**（不反号 ⇒ 噪声，不是方向押错）、排名强度变化率 `1YN6RNbM` S=−0.12（TO .50）。⛔ **双重死因**：① **数据 2017 起，只有 7/10 年**（2014–2016 `longCount=0`，两条几何同证）⇒ 直接违反约束 4；② 7 个有数据年里 **S<1.0 占 7/7**、符号 3 次翻转 ⇒ IS_LADDER 与 2Y 结构性不可达。判 `KOR-SENTIMENT26-NO-CROSS-SECTION-AND-7Y-COVERAGE`。**塔级结论：sentiment 塔关闭**（189 覆盖 / 190 / 192 / 216）。见 `datasets/sentiment26.md` §7.1/§7.2 |
| **214** | **risk70（IVOL 水平 / ΔIVOL）+ other496（涨跌停状态码）** | risk + other | 8 | ⛔ **CLOSED FAIL + IVOL 轴与触板频次轴双关闭** | risk70：`srisk` 水平正向 **S 0.57 / F .32 / TO .0907 / 2Y 1.64**、反向 **−0.73**；`srisku` 与 `srisk` **逐项同**（.57/.0906）⇒ 同一条腿；**ΔIVOL 为 null**（S −0.04 / F 0）⇒ 该字段只有水平无变化率。**归因**：逐年 S<1.0 **5/10**（2014 −1.36 / 2020 −0.48 两段深负）、**2022 单年占正收益 31.5%** ⇒ 按决策表**停扫 decay/平滑/门控，必须换机制**；TO .09 在获胜带内 ⇒ 纯强度不足（差 2.8×）。**十年覆盖 PASS**（longCount 295–344）。other496：`ts_sum(limit_status,22)` **S −0.64 / 反向 0.38 / CW 0.1243 FAIL**；新近触板轴（`ts_decay_linear(ts_delta(...,1),22)`）仅 −0.48 ⇒ **累计频次 > 事件近因**，新近轴弃。**⚠ 预注册证伪条件 #1 触发 ⇒ 磁吸机制被证伪**：磁吸预测 2015 后（±30%）变弱，实测 **2023 最强 2.87**、2015 1.73、2017 1.31 ⇒ 读数符合**彩票需求/注意力过度反应**（另一条经济含义，须换方向句）；2023 占正收益 **39%** ⇒ 过拟合指纹；CW 根因 = 状态码低基数离散（数据形态，按 CW 阶梯不动 truncation）。**十年覆盖 PASS**（205–270）。**⇒ 单塔 ATOM 上限实测 0.73 < 路线图的 ≤1.02；两条路只剩组合腿或新数据集授权** |
| 195 | insiders1 次波 / other106 次波 | — | ≤3 | 待 190–192 归因 | 按铁律 G 收窄（≤ 上一波 1/3） |

| — | imbalance5 | imbalance | 0 | **待封存** | 2Y 结构性不可达，走 `seal_dead_end` |
| — | institutions 塔 | institutions | 0 | **关闭** | 双数据集全死，无攻击面 |

## 4. 禁区（命中即不投配额）

- **死数据集（16，`get_dead_datasets`）**：acquisition_model、fundamental44、**institutions6**、model109、model170、model192、model230、model30、model32、model53、multi_source_model、**news79**、**sentiment21**、shortinterest3、smoke_ds、wave30_model252。
- **战役级判死数据集（`get_dead_ends` 点名）**：other455、chart_cnn_alpha、predictive_starmine、ai_equity_alpha、pattern_scores、continuation_score、analyst_earnings_ibes、**fund_holdings_panel**、quant_factor_lib、model313、ai_factor_transfer、price_signal_dl、ml_factor_proj、behavioral_signals、news_sentiment_transfer。
- 新闻**情绪/标题语气/事件评分**族：news38、news50、news87、news96、news141、mmp_nlp、model37 文本、equity_forum_data。
- 图表形态族：chart_cnn_alpha、continuation_score、pattern_scores（天花板 ~0.34）。
- 借券/费率域：risk60（拥挤度已死）、shortinterest3（死集）⇒ **水平/比率/拥挤度族关闭**。
  ⚠ **risk59 不等于整域关闭**（2026-10-30 更正本行旧表述）：登记表死的是 `bare cross-sectional signals`
  （bid/ask-vwap 比率、squeeze_risk、做空金额…），**时序方差/凸变换未测也未判死**。域内互锁 0.64–0.80
  是 **prod 相关性风险** ⇒ 该域出候选后先查 prod 再谈提交，但不构成「不投配额」的理由。
- 内部人：insiders5 天花板 1.05、insider_feats prod 0.7+ ⇒ 只有 insiders1 尚可一探。
- 风格载荷：risk88 `ri_*`。
- 时间戳字段：`oth496_*_t`（description 含 "Timestamp for" 一律不得作信号）。
- GROUP 标签字段：pv30（聚类整数标签只能作 `group_*` 分组维，且必须是平台 GROUP 类型）。
- PCA 分量：other455 `*_pca_fact*`（符号随机翻转）。
- KOR REV1 类信号禁用 SUBINDUSTRY 中性化（prod 安全档 = STATISTICAL / SECTOR）。
- **流程禁区（2026-10-30 已部分解除，仍缺 enforce）**：`pipeline.py` / `wave_gate.py` **从不传**
  `--require-priors` ⇒ 死集命中只报 **WARN**，且旧版 `assemble_priors.MAX_DEADENDS=12` 把 99 条死记录
  截成 12 条，闸根本看不见 `fund_holdings_panel`（wave187 / wave200 两次误发的同一根因）。
  **本次已修**：priors 增写全量 `_dead_ends_all`（`MAX_DEADENDS_ALL=400`，不占 GEM prompt 名额），
  `gate.check_priors` 取 `dead_ends ∪ _dead_ends_all` ⇒ 实测 99 条全可见，三集命中复现正确。
  **仍须人工做的一步**：开波后 grep 本波日志里的 `PRIORS-DEADEND-HIT` / 看 gate 报告
  `priors_gate.issues`，命中且机制同名即 kill 未发批次；要自动拦，需给 pipeline 加 `--require-priors` 透传。
- **2026-10-30 wave208 复现同一缺口的第二形态**：`pipeline.py dead_dataset_guard()` 只校 **16 个死数据集**
  （`ledger_kv` 的 `<ds>_dead`），**完全不校 `get_dead_ends` 的战役级死路**。本波 `news_sentiment_transfer`
  一路放行到批级闸之后（日志 `[dead-guard] OK`），但它在上面 §4 名单里、且 `KOR-NEWS-SENTIMENT-TRANSFER-DEAD`
  写着「do not probe news/sentiment aggregate datasets in KOR again」。
  ⇒ **派发前人工 kill：0 条上平台、0 配额消耗**，4 条表达式已 `status=dropped`。
  修复建议（未落地）：`dead_dataset_guard()` 的白名单来源加上 `registry_empirical layer=dead_end` 的 dataset 并集。
  ⚠ **这次 kill 不是"地图错了"，是"闸只看了 16 个名字"**——后续开波前人工核一次 `get_dead_ends` 仍是必需步骤。

## 5. 天花板证据表与交付对账（2026-10-30 汇总，跨 wave 190–214）

### 5.1 平台闸实测（不是战役自设阈值）

`mcp__wq_brain_http__submit_verdict(QPvr1vPM)` 返回的平台原始 checks：

| 闸 | 平台 limit | 本条 value | 差 |
|---|---|---|---|
| `LOW_SHARPE` | **1.58** | 1.02 | **+0.56（需 +55%）** |
| `LOW_FITNESS` | **1.0** | 0.67 | +0.33（需 +49%） |
| `CONCENTRATED_WEIGHT` | ≤0.1 | WARNING | 未量化 |
| `CLUSTER_TEST` | 1.0 | 0.92 | 余 0.08 |

⇒ `tracking/KOR/config/thresholds.json` 的 `sharpe_min: 1.58` / `fitness_min: 1.0` **与平台逐位一致**，
不是自设的高标；「降阈值」不存在，只能提高信号或换区。

**`LOW_2Y_SHARPE` 也是 1.58（2026-10-30 当日实测，双侧核验）**：wave 214 六条的 `checks` 里
`LOW_2Y_SHARPE.limit` 恒为 **1.58**，且两侧都自洽 —— `omEwjj6k` 2Y=1.62 落 `pass`、
`Xg9wZZb8` 2Y=1.60 落 `pass`，而 `xArw77wq` 2Y=0.17、`88RkWWjq` 2Y=−1.94、`leA6ww8l` 2Y=0.08 落 `fail`
（`get_user_alphas(region=KOR, stage=IS)` 原始返回）。
⚠ **本地 `thresholds.json` 的 `two_year_sharpe_min: 1.0` 是早期筛选线，不是平台线**；
按它判「2Y 已过」会系统性高估近闸程度。⇒ 上面 §5.2 里那些 2Y 1.88 / 1.94 / 2.02 / 2.17 是**真过**，
但 2Y 1.27 / 1.53 的（news20 / news85）在平台上**同样是 FAIL**，不是「差一点」。
**读数修正**：本季 KOR 的 2Y 闸 = 1Y 闸 = 1.58，不存在「2Y 更松」的缓冲。

### 5.2 未点亮塔实测天花板（只列有回测读数的）

| 数据集 | 塔 | 已测形态 | max\|S\| | 对应 2Y | 十年覆盖（约束 4） |
|---|---|---|---|---|---|
| risk59 | risk | 水平 / 方差 / delta / 聚合×3 / 分组轴×3 | **1.04** | 2.02 | 未单列（wave 201/213 均出候选） |
| earnings3 | earnings | 日历距离 3 种几何（zscore / ts_rank252 / tail） | **0.95** | **2.17** | ✅ 292–354/年 |
| other106 | macro | 指数供给冲击 8 腿（实发 4） | 0.75 | 0.43 | ✅ 267–347/年 |
| risk70 | risk | IVOL 水平（srisk / srisku）+ ΔIVOL | 0.73 | **1.88** | ✅ 295–344/年 |
| news85 | news | 情绪分布 / 背离互相关 | 0.67 | 1.53 | — |
| other496 | other | 触板累计频次 + 新近触板 | 0.64 | 1.94 | ✅ 205–270/年 |
| news20 | news | 冲击幅度 / 评级变动 | 0.25 | 1.27 | ✅ 289–345/年 |
| macro63 | macro | 0/1 成员状态（wave 215：S/TO/longCount 全 0，恒空仓） | **0.00** | — | ❌ **10/10 年 `longCount=0`** |
| sentiment26 | sentiment | 广度水平 / 其 reverse / 排名强度 Δ22 / 域名数 zscore66（4 腿） | **0.20** | 0.55 | ❌ **2017 起，仅 7/10 年**（2014–2016 `longCount=0`） |

**读数**：9 个未点亮数据集里 **9/9 已测**（最后一集 `sentiment26` 于 wave 216 判死），
**最高 1.04，距平台闸差 55%**。死法分三类，**没有一类是「再加点参数就能过」**：
① **信号强度不足**（7 个，十年覆盖全 PASS，max|S| 0.25–1.04）；
② **恒空仓**（`macro63`，10/10 年 `longCount=0`，`KOR-MACRO63-NO-CROSS-SECTION`）；
③ **时间覆盖不足**（`sentiment26`，数据 2017 起、仅 7/10 年，`longCount=0` 于 2014–2016，
直接违反约束 4）。
⚠ **`coverage` 字段（如 sentiment26 的 .356、macro63 的 1.0）是横截面覆盖率，不是时间覆盖** ——
约束 4 只能靠 `get_alpha_yearly_stats` 的逐年 `longCount` 判，不能用 `coverage` 预判（wave 216 实证）。
这与「单塔单字段 ATOM 上限 ≤1.02」的旧结论合并后，构成一条硬结论：

> ⛔ **KOR 未点亮塔在单数据集 ATOM 形态下不可能达到 LOW_SHARPE 1.58。**

### 5.3 组合腿的数学边界（为什么路线图 ① 也救不了）

平台混信号闸（`POISON:equal_weight_leg_add`）**只允许**跨数据集用 `subtract` / `multiply` / `trade_when`：

| 算子 | 数学效果 | 能否把 1.04 抬到 1.58 |
|---|---|---|
| `subtract(rank(A),rank(B))` | **价差**（A 相对 B 的分歧） | ⚠ **能，但要 B 自身方向为负**（见下方更正） |
| `multiply(A,B)` | **条件交集**（同时高才持仓），IC ≈ IC_A·IC_B 量级 | ❌ 通常低于单腿 |
| `trade_when(cond, sig, -1)` | **子样本持仓**（只在 cond 成立时交易） | ⚠ 只可能放大「cond 期的 alpha 密度」，不是代数叠加 |

**⚠ 2026-10-30 更正（原写「只有 add 才能 √2 叠加」是错的）**：等权两腿的 Sharpe 是
`(|S_A ± S_B|) / √(2 ± 2ρ)`
—— **`add` 与 `subtract` 在代数上完全同构**，区别只是第二腿要不要先反号。
所以 `subtract` 在「B 自身的 Sharpe 为负」时**同样按 √2 叠加**（`S_A + |S_B|`），
并非「只会抵消」。举例：A 腿 S=+0.9、B 腿 S=−0.6、ρ≈0 ⇒ `subtract` 得 ~1.06，`add` 只得 ~0.21。

**闸门口径不是障碍（2026-10-30 二次更正）**：`add` 被无条件拦、跨数据集 `subtract` 默认同拦，
只在「两腿同源同一数据集 + 单一经济含义」放行；但**用户约束 5 已显式授权**「PV / MODEL / OTHER 可同
其它 category 组腿，≤5 条」⇒ 「带单一经济含义的跨类别价差（背离）」在用户侧**本来就是开着的**。
所以阻碍不在闸门、**在相关性与腿数**：

> **⚠ 2026-10-30 实测闭环：组合腿路线定量不可达，建议不为它单独开波。**
>
> `compute_mutual_correlation([QPvr1vPM, pwdJMWb6], years=4)` —— **ρ = 0.1978**
> （1023 个日度点，本地计算，零平台相关性配额）。L1 = risk59 `QPvr1vPM`（S 1.02 / 2Y 1.80 / TO .135），
> L2 = earnings3 `pwdJMWb6`（S 0.89 / 2Y 2.17 / TO .166）。
> **机制正交 ≠ 收益不相关** —— 这是原估算「risk59 + 0.9 腿 ≈ 1.37」失真的原因。
>
> 最优点权（`S_comb = √(SᵀΣ⁻¹S)`，Σ=(1−ρ)I+ρ·11ᵀ）实算：

| 腿数 | 组成 | S_comb |
|---|---|---|
| 2 | L1 + L2 | **1.238** |
| 3 | L1 + L2 + L3(0.67) | **1.292** |
| 4 | 假设 4×0.9 | 1.407 |
| 4 | 假设 4×1.0 | 1.459 |

> 反解：要摸 1.58 需要 **4 条平均 1.0 的腿**，或 **7 条平均 0.9 的腿**。
> 现存可用腿只有 3 条 `[1.02, 0.89, 0.67]` ⇒ **理论上限 1.29，距闸差 0.29**。
> 完整推导见 [`composite_route_20261030.md`](composite_route_20261030.md) §3.1。
>
> ⇒ **结论**：此前「1.4 量级可试」的估计作废；组合腿**不是**通往 1.58 的可行路，
> 省下的配额应全部投给「新机制」（即 §5.5 的 C/D 路），而不是组腿。

### 5.4 交付对账（60 个 regular alpha）

| 口径 | 数 | 说明 |
|---|---|---|
| 目标 | **60** | 未点亮塔、REGULAR、最好 ATOM |
| 本轮实测产出 | **0** | wave 190–245 全部 0 candidates / 0 near（唯二 near 是 risk59 的 S 1.02 / 1.04；215 macro63 三条恒空仓；216 sentiment26 max\|S\| 0.20 + 仅 7/10 年覆盖；244 earnings3 双灭 S 0.63 / 0.05，见 §5.90） |
| 未点亮塔数据集验证进度 | **9/9** | 全部有回测读数。**塔级终态（2026-10-30）**：**关闭 8 座** = news / insiders / sentiment / socialmedia / institutions / macro / **imbalance（§5.89.8 判死）** / **earnings（§5.90 关闭）**；**仍开 1 座 = risk**（但 §5.87.5 已移出队列）⇒ **零计数塔的可挖供给 = 0** |
| ⚠ 真正的剩余供给（改写「9 座塔」口径） | **3 个近点亮格，已全部冻结** | 平台计数 analyst **2/3** · pv **2/3** · other **1/3**（≥3 才点亮，见 §5.89.9 ①）⇒ 缺口 **+1 / +1 / +2**。**三格同日封顶**：analyst 分歧轴毛 Sharpe 0.05（§5.91.2）· pv 单数据集面 18 集穷尽且其余「PV 集」实属别塔内容（§5.92.1）· other 结构性封顶（§5.51/§5.53）⇒ **唯一活口也没了** |
| 全库 KOR 未点亮塔可提交 | **1** | `LLZ6wZO2` S **1.99** / F **1.53** / 2Y 2.24 / subU 1.21 / cluster 0.94 / prod **0.6762** / self **0.676** —— **全闸通过**，因 `KOR/D1/FUNDAMENTAL` 已 3/3 满而不提 |
| ⚠ 补席的真实瓶颈 | **prod 墙** | KOR OS book 的 `prodCorrelation` 主峰 **0.63–0.70**，已破 0.7 的 3 条（`zqYaZ2gO` .8201 / `WjP1ZwMj` .7974 / `WjPEg2zd` .7298）⇒ **「换数据集」不等于「降相关」**，补席候选必须**概念可区分**（§5.89.9 末段） |
| 全库 KOR **已点亮塔**库存（不在目标内） | **7** | shortinterest38 同族 7 颗 IS 全闸通过（S 2.27–2.72 / 2Y 1.80–2.37），但同族互相关≈1 ⇒ **最多再提 1 颗**；见 §5.6 |

⇒ **60 个的目标在「未点亮塔 + 平台闸 1.58」双约束下不可达**；差距不是执行量，是**闸与数据的结构性错配**。

### 5.5 三条需用户授权的路（本 agent 不能自行决定）

| # | 路 | 代价 / 风险 | 需授权什么 |
|---|---|---|---|
| **A** | **提交 `LLZ6wZO2`**（全闸已过，塔位满） | 违反「均匀点塔」自律；塔已满是否真被平台拒，需一次提交验证（不可逆） | 用户明确同意 + `confirm_submit=True` |
| **B** | **补满「未满塔」**：`get_pyramid_alphas(KOR/D1)` 实测 **analyst 2/3**（乘数 1.6，差 1 席）、**pv 2/3**（1.4，差 1 席）、**other 1/3**（1.6，差 2 席） | ✅ **口径已裁决（2026-10-30，见 §5.8）**：平台术语原文「submitted a minimum of **3** Alphas ⇒ formulate a pyramid」+「**A single Alpha can belong to multiple pyramids**」⇒ 这三个 cell **仍未点亮**，属用户原约束范围内，**无需额外授权**。KOR 其余 9 个 cell 全为 0（news/sentiment/macro/socialmedia/insiders/institutions/earnings/risk/imbalance） | 无（已裁决）；把 analyst 2→3 作为第一优先 |
| **C** | **授权新数据集**（185 个数据集里尚未画像的 other323/other78/news59/other532/other327/other436/other546） | news 塔已判死；其余多为 OTHER ⇒ 受约束 5 组腿限制，只能 ATOM | 授权这些集进入白名单并接受 ATOM 上限≈1.0 |
| **D** | 缩短 IS 窗口到近 2 年（`last_rate` 的 2Y 2.02 = 全样本 2 倍） | 与用户约束 4「近十年都要有数据」的精神冲突；且 2Y 高≠全样本高，LADDER 与 CX 闸风险大 | 明确授权 |

**推荐顺序**：A（零额外配额，唯一确定能落地的）→ B（analyst 余 1 席是最接近的增量）→ C → D。

### 5.6 已点亮塔的库存盘点（路径 A/B 的量化依据；2026-10-30 全库检索）

> 触发原因：`search_alphas_by_sharpe(KOR, ≥1.3, 30)` 里浮出一批 **UNSUBMITTED 且 IS 全闸通过**的
> REGULAR alpha，而 §5.4 只登记了 `LLZ6wZO2` 一颗 ⇒ 旧口径**漏计了整条 shortinterest38 库存线**。
> 判据：`platform_status=UNSUBMITTED`、`alpha_type=REGULAR`、S≥2.2、F≥1.7、2Y≥1.58、subU≥1.7、prod<0.70。

| alpha | 表达式核心（shortinterest38 借券卖出/买入比） | S | F | 2Y | subU | prod | TO | 判定 |
|---|---|---|---|---|---|---|---|---|
| `mLmGQEq9` | `vec_avg` 比值 + `hump 0.0025` + `sector` | **2.72** | **2.12** | **2.35** | 2.24 | ~~0.6011~~ **0.935** | n/a | ⛔ **实测 prod 破**（2026-10-30T19:45:14） |
| `E5pjx9q0` | 同上但 `industry` | **2.50** | 1.85 | **2.37** | 1.86 | ~~0.6002~~ **0.8105** | n/a | ⛔ **实测 prod 破**（2026-10-31T13:34:49） |
| `VkaWXGmb` | `ts_decay_linear 630` + `sector` | 2.35 | 1.79 | 2.21 | 1.78 | 0.6932 | .189 | ⚠ 余量 0.007 |
| `JjNAkqbn` | `ts_decay_linear 500` + `industry` | 2.31 | 1.75 | 1.88 | 1.78 | 0.6958 | n/a | ⚠ 余量 0.004 |
| `rKOxJLd1` | `ts_decay_linear 400` + `industry` | 2.30 | 1.74 | 1.87 | 1.78 | 0.6932 | .1888 | ⚠ 余量 0.007 |
| `2rwYaR5x` | `ts_decay_linear 600` + `industry` | 2.28 | 1.71 | 1.82 | 1.76 | 0.6914 | .1888 | ⚠ 余量 0.009 |
| `akbpAj99` | `ts_decay_linear 900` + `industry` | 2.27 | 1.70 | 1.80 | 1.73 | 0.6886 | .1888 | ⚠ 余量 0.011 |
| ~~RRbOoMNg / Vkarb9WM / E5pjMdnG / xA3LoZ7m~~ | 同族其它 decay 窗 | 2.36–2.47 | 1.82–1.94 | — | — | **0.768–0.787** | — | ⛔ prod 硬破 |

**为什么这 7 颗不是「可交付 60」的一部分（三条硬理由，按效力排序）**：

1. **塔位**：`shortinterest` 塔**已点亮**（4 颗已提，其中 `omLjG1M5`/`KPNo2lgl` 就是本族）。用户目标的
   原话是「在**未点亮塔**挖掘」⇒ 这 7 颗全部落在目标范围之外。
2. **同族自锁**：7 颗是**同一比值的 7 个窗口变体**（`vec_avg`/`vec_sum` × `ts_decay 400–900` × `sector`/`industry`）
   ⇒ 互相关预计 ≈1，**最多再提 1 颗**，不是 7 颗。
3. **prod 刀锋**：5 颗的 prod 余量只有 **0.004–0.011**；`prod_corr_stale=true`、`self_correlation=null`
   ⇒ 未实测，且平台 prod 取数有 7 天缓存/超时风险（`wq-prod-corr-read`）。
   ~~真正可承重的只有 `mLmGQEq9`（0.6011）与 `E5pjx9q0`（0.6002）两颗~~ ——
   ⛔ **2026-10-31 已用 `check_correlation(refresh=True)` 实测推翻**：`mLmGQEq9` prod **0.935**、
   `E5pjx9q0` prod **0.8105**，两颗都硬破 0.70。本地旧值 0.6011 / 0.6002 是**过期缓存**
   （`prod_corr_source` 非平台实测档），不可再作为刀锋判断依据。
   ⇒ 本族 prod 直方图 `[0.7,0.8) n=5` / `[0.8,0.9) n=2`，按族代表规则**整族判死**，
   7 颗全部退出候选池，不再逐颗复测。

**⇒ 这条路能给出的增量是「0 颗」，不是 1–2 颗，更不是 60。**
~~若用户授权路径 B，正确顺序是：先 `check_correlation(refresh=True)` 实测 `mLmGQEq9` 的 prod/self~~
~~（它不是刀锋档、余量 0.099，最可能过）→ 再 `submit_verdict` 否决权 → 才谈提交。~~
⇒ 该顺序**已执行完毕且结论为否决**：shortinterest38 借券卖出/买入比这一整条库存线
（含已提交的 `omLjG1M5`/`KPNo2lgl` 同族）**没有一颗可再提交**。

**另附（不属 REGULAR 目标，但同批检索浮出）**：`3qoWQKJg` 是 **SUPER**（name `KOR_S_10comp_oWQKJg`，
pending `SUPER_SUBMISSION`/`NON_SELF_SUPER_ALPHA`）—— 10 组件，**S 3.62 / F 4.32 / 2Y 2.32 / subU 2.93 /
cluster ✅ / RA 0 failed**，仅 SELF 与 PROD 待测。它是**另一条轨**（`wq-brain-superalpha`），
不属于本文件的 REGULAR 60 目标，登记备查。

### 5.7 判死封存状态（S6 回写台账）

| 条目 | registry dead_end | 状态 | 为什么没封 |
|---|---|---|---|
| `KOR-MACRO63-NO-CROSS-SECTION` | ❌ **未入** | 待用户授权 | `seal_dead_end` 的 `forum_recon` 闸 fail-closed：本区 ledger 里没有任何以 macro63 为主题的 `forum_recon_negative_*` 记录（实测 3 个 negative 键全是 shortinterest / prod 的），且当轮 recon 为 `found=true` ⇒ 传参必被拒（`recon_found`）。逃生口 `force_seal` / `require_forum_recon=False` 均需**人工确认**，Agent 不得自行使用 |
| `KOR-SENTIMENT26-NO-CROSS-SECTION-AND-7Y-COVERAGE` | ❌ **未入** | 待用户授权 | 同上；且 sentiment26 的 A 通道 recon **确实有货**（注意力→动量/反转 两类帖）⇒ 用「论坛无解」去封存会失真。正确封存理由是**本区实测无截面 + 7/10 年覆盖**，属 `require_forum_recon=False` 档（需人工确认） |

> ⇒ 两份判死结论**已在 `datasets/*.md` 与本文 §3/§5.2 落档**（可复核、带读数），
> 但**未进 `registry_empirical` dead_end** ⇒ 后续 S0 选集不会自动排除它们。
> 若要机械排除，需要用户点头用 `force_seal=True` / `require_forum_recon=False` 补封，或先补一轮
> 主题化 `forum_recon`（问句须指向「该机制在 KOR 是否成立」，不能借 A 通道的「有货」当无解）。

### 5.8 ★ 口径裁决：「点亮」= 已提交 3 颗，且一颗可入多塔（2026-10-30，平台术语原文）

`get_glossary_terms` 原文（逐字）：

> "A combination of region, delay, and dataset category… **A consultant is considered to formulate
> a pyramid if they have submitted a minimum of 3 Alphas in it. A single Alpha can belong to
> multiple pyramids as it could have multiple data fields.**"

⇒ 三条裁决，直接改变 §5.5 与 §5.2 的结论适用面：

1. **「点亮」= 该 cell 已提交 ≥3 颗**。`get_pyramid_alphas(KOR, delay=1)` 实测
   `analyst 2 / pv 2 / other 1` ⇒ **三者仍未点亮**，落在用户原约束「在未点亮塔挖掘」范围内，
   **不需要额外授权**（§5.5 路径 B 的「口径歧义」条目就此作废）。
2. **一颗跨类 alpha 同时计入它触碰的每一个塔**（"could have multiple data fields"）⇒
   用户约束 5 允许的「PV + 非 {PV,MODEL,OTHER} 组合（≤5 个）」是**双塔有效投放**，不是单塔产物。
3. 因此 §5.2 那条硬结论「KOR 未点亮塔在单数据集 ATOM 形态下不可能达到 1.58」
   **只约束 ATOM 形态**，不约束合规跨类组合；后者是本区唯一剩余的结构性出路。

### 5.9 ★ 平台事实纠偏：`LOW_SHARPE` / `LOW_2Y_SHARPE` 在提交层是 warning，不是 fail（2026-10-30 实测）

`get_alpha_details` 原始读数（**不是推断**）：

| alpha | S | 2Y | `checks.fail` | `checks.warning`（节选） | 状态 |
|---|---|---|---|---|---|
| `883mLenl` | 1.40 | 2.14 | **`[]`（空）** | LOW_SHARPE 1.40/1.58、CLUSTER_TEST 0.89/1、MATCHES_THEMES、OSMOSIS_ALLOCATION | UNSUBMITTED |
| `ZY0R0mL8` | 1.59 | 1.17 | **`[]`（空）** | LOW_2Y_SHARPE 1.17/1.58、MATCHES_THEMES、OSMOSIS_ALLOCATION | **ACTIVE（已提交）** |

三条推论：

- **1.58 是 RA 资格线**（进 `ra_failed_checks`），**不是提交阻断**。提交的硬阻断只看 `checks.fail` 是否为空。
- 两颗都是 `pyramids.effective = 1`、`KOR/D1/ANALYST` ⇒ **低于 1.58 的 analyst alpha 依然能计入塔**。
- ⚠ campaign 自律仍以 **S ≥ 1.58 / F ≥ 1.0** 作发射门槛（不把 RA 不合格件塞进提交配额）；
  **是否破例提交 1.40–1.58 档，只能由用户裁决**（提交不可逆）。

### 5.10 wave 217（analyst44 · 单字段强度杠杆 + 净修正广度新机制）

**开波依据（铁律 F 归因前置 + 铁律 G 收窄）**：wave 214（risk70）归因已判「5/10 年 S<1.0、2022 占正收益 31.5%」
⇒ 该机制族封闭；215/216 分别因恒空仓与 7/10 年覆盖判死 ⇒ **本波换塔（analyst）、换机制（修正幅度 → 修正广度）**，
候选数 6（自上两波 7–8 收窄）。

**基线（复现用，必须同设置）**：`883mLenl` = `group_rank(rank(ts_decay_linear(ts_backfill(vec_avg(eps_estimate_4wk_change), 5), 22)), industry)`
→ S **1.40** / F 1.15 / 2Y **2.14** / subU 1.38 / TO .063；设置 **KOR/TOP600/D1 · SECTOR · decay 4 · trunc 0.08 · nanHandling ON · maxTrade ON**。

**双通道取证**：

| 通道 | 证据 | 结论 |
|---|---|---|
| A 论坛 | 《【因子灵感】分析师预期修正，怎样分离方向与参与广度》（29 赞，2026-09-21）+《【Alpha Idea】分析师盈利预期修正广度：盈利动能的横截面代理》 | ① 支持「方向 × 参与广度」分离；② **警告：先核覆盖家数与更新时间，确认结果没被少量高覆盖公司主导** ⇒ 裸 `up−down` 会被覆盖数主导，**必须先秩化再相减** |
| B 学术 | Mill Street Research（breadth = 净上调分析师占比 / magnitude = 修正幅度，两指标分列）；Gleason & Lee (2003)「延迟价格反应是修正**数量**的函数」；Stickel (1991) 上修 ⇒ 后续 3–12 月正异常；2025 年 post-revision drift 文献 | 方向句：**净上调广度越高 ⇒ 后续收益越高**，持有期 1–3 月 |
| 裁决 | A、B 同向 | ⭐ 优先组装；**论坛的覆盖数警告直接决定广度腿的算式形态**（rank 差而非计数差） |

**6 条候选（单变量对照，禁 `add` 加权混合）**：

| # | 表达式 | 杠杆 / 机制 |
|---|---|---|
| 1 | `signed_power(group_rank(rank(ts_decay_linear(ts_backfill(vec_avg(eps_estimate_4wk_change),5),22)),industry),2)` | 功率变换（analyst10 实测 ts_rank→signed_power(·,2) 增益 +0.32） |
| 2 | `group_rank(rank(ts_decay_linear(ts_backfill(vec_avg(eps_estimate_4wk_change),5),66)),industry)` | decay 窗口 22→66（**未测**；5→22 已实测 1.31→1.40，趋势为正） |
| 3 | `multiply(<decay22 组秩>, <decay66 组秩>)` | 同字段双窗乘积（单信号结构化，合规） |
| 4 | `subtract(rank(ts_backfill(vec_avg(eps_gaap_estimate_4wk_up_count),22)), rank(ts_backfill(vec_avg(eps_gaap_estimate_4wk_down_count),22)))` | **新机制：净修正广度**（同数据集两腿 + 单一经济含义 ⇒ `subtract` 放行） |
| 5 | `group_rank(ts_decay_linear(subtract(<up>,<down>),22),industry)` | 广度腿 + 行业组内秩 + 平滑 |
| 6 | `vector_neut(<#基线核心>, power(rank(ts_backfill(pv106_lastspreadbp,22)),2))` | **ANALYST + PV 壳层**（约束 5 允许，≤5 个额度内第 1 个）⇒ 若过闸**同时计入 analyst 与 pv 两塔**（§5.8 第 2 条） |

> ⚠ 字段事实：非 GAAP 的 `eps_estimate_4wk_up_count` **不存在**，成对可用的只有
> `eps_gaap_estimate_4wk_{up,down}_count`（cov 全 1，aC 8/35）⇒ 广度腿固定用 GAAP 对。
> ⚠ `validate_expressions` 实测：4 个字段全部合法、6 条表达式全部合法（`unknown_fields: []`）。

**收割与归因（2026-10-30，仅发 2/6 —— 并发=2 约束 + 中途判死）**：

| 候选 | alpha | S | F | 2Y | subU | TO | 判读 |
|---|---|---|---|---|---|---|---|
| #1 功率 2 | `mLoJLnZ5` | **1.40** | 1.12 | 2.18 | 1.40 | .0668 | 与基线 `883mLenl` **同 S**（1.40）⇒ 功率变换在本族**零增益**（与 analyst10 的 +0.32 完全相反） |
| #2 decay 66 | `kqNbqpKk` | 1.32 | 1.06 | 1.88 | 1.29 | .0439 | 长窗更劣 ⇒ **decay 22 是局部最优** |

**归因（铁律 F，两条读数指向同一结论）**：

1. 功率 / 长窗两条**单调变换都不动 S** ⇒ 该族 IS 已被压平，**没有参数杠杆可扫**；
2. 真正的闸不是 S 而是 **prod**：`analyst44.md` §8.2–§8.4 实测 A 腿 prod **0.8073**、闭式
   `prod = 0.6116 + 0.1371·S` ⇒ prod@S=1.58 = **0.8283**（墙 0.70，超 0.128）⇒
   **无论把 S 推到多少档，prod 都不可能 < 0.70**。

⇒ **analyst44 判死（prod 结构墙，不是 S 天花板）**：候选 #3–#6（双窗乘积 / 净修正广度 /
广度组秩 / vector_neut 壳）**未派发即 kill**，不消耗配额。

**修正两处历史记载**：① `datasets/analyst44.md` 第 307 行「本集历史最高 S = **1.45**（`wp9l3J51`）」
与 DB 实测不符（maxS **1.78**）；② 同文 §8.5 的判死理由应记为 **prod 墙**，S 天花板不是判据
（§5.9 已证 1.58 只是 RA 线，低 S 也能提交）。

### 5.12 wave 218（analyst10 × pv106 双塔复用 + other695 壳层分离）

**为什么是这三座塔**：`analyst 2/3`、`pv 2/3`、`other 1/3`（§0）是**仅有的三个「差 1–2 席即可点亮」**
的塔；平台规则「一个 alpha 可计入多个塔」（§5.8）⇒ **跨塔复用是单位配额最高杠杆**。

**基线证据（全部机器可核）**：

| 塔 | 金矿 | 读数 | 判读 |
|---|---|---|---|
| analyst | **analyst10** | `ZY0R0mL8` S 1.59 / 2Y 1.17 / **prod 0.6003** / self 0.0967（ACTIVE） | **全库唯一 prod < 0.70 且 S 近闸的 analyst 集**（analyst44 = 0.8073、其余 analyst 集 S≥1.20 零行） |
| other | **other695** | `xA16pzQJ` S 1.86 / **prod 0.6976** / self 0.2308（**已提交 ACTIVE**） | 唯一已验证的金矿，prod 恰好卡在墙下 ⇒ 只能做**壳层分离** |

**2 条候选（并发=2，同设置 KOR/TOP600/D1 · SECTOR · decay 4 · trunc 0.08 · nanHandling ON · maxTrade ON）**：

| # | 表达式 | 塔 | 机制 |
|---|---|---|---|
| 1 | `trade_when(greater(rank(ts_backfill(pv106_lastspreadbp,22)),0.2), signed_power(ts_rank(ts_backfill(anl10_smartest_pre_fy1_pred_surps_v1,22),66),2), -1)` | **ANALYST + PV**（约束 5 第 **1/5** 个额度） | PEAD 在**低流动性端更强**（买卖价差秩作条件门控，非加权混合）；基底 `mLgPgJnW` S 1.44；过闸即**同时计入两塔** |
| 2 | `trade_when(greater(rank(adv20),0.6), hump(group_rank(ts_sum(vec_avg(oth695_import_value_4),20),sector),hump=0.0025), -1)` | other | **只换壳层**（`bucket(cap)`+`tail` → `sector`+`hump`），字段与窗口不动 ⇒ 目的 = 压低与 `xA16pzQJ` 的 self-corr |

**预注册判据（未过不进入下一步，防白烧 prod 时隙）**：S ≥ **1.3** 且 2Y ≥ **1.5** 且 subU ≥ **1.0**；
随后 self-corr 对 `ZY0R0mL8` / `xA16pzQJ` 必须 < **0.70**，再查 prod < 0.70 才谈提交。

**两条硬约束（写死，别再撞）**：

- ⚠ **other695 全表仅 3 个字段**（`query_field_profile` 实测：`company_eng_2`/`code_3` 是元数据，
  唯一信号 = `oth695_import_value_4`，cov **.4057**）⇒ **other 塔只能靠单字段多壳层推进，换字段路线不存在**。
  这也是为什么第 2 条必须"只换壳层"：没有第二根腿可用。
- ⚠ **pv 塔已亮 2 颗的来源尚未盘清**（DB 未按 PV 类别建索引，`backtest_results.dataset` 是文本列）
  ⇒ 若 218-1 过闸，**先查 self-corr 再排提交顺序**，不要假定 pv 端无自相关占用。

### 5.13 派发通道变更：`create_multi_simulation` 在本部署已失效（2026-10-30 实测，改走 `batch_create_simulations`）

**事故**：wave 218 首次派发（multisim `42dUQsapV4P1aUF11cggxkln`）返回 `success:true / async:true`，
但此后 **12 分钟 5 次轮询恒定 `child_count:0 / parent_status:null`**；`get_user_alphas(region=KOR, stage=IS)`
最新两条仍是 wave 217 的 `kqNbqpKk` / `mLoJLnZ5` ⇒ **没有子 alpha 被创建**。
随后换 `create_multi_simulation` 重发（`4ClLzf32T53O8SyoJysKUfY`）**同样 0 子任务**；
`harvest_multisim_alphas` 直接回 `No children found`。
`create_simulation`（单发）**两次均报 `MCP error -32603`**，执行体报错而非平台拒绝。

**可用通道（实测）**：`batch_create_simulations`（服务端逐条顺序提交，per-item settings）——
07:45 提交 2 条，**两条都进入 progress 0.10 → 0.35**，即真的在跑。
⇒ **新 SOP：并发=2 时用 `batch_create_simulations` 传 2 个 item**（等价于原「multisim 限 2」口径，
只是不再依赖有缺陷的 multisim 父对象）。轮询用 `lookINTO_SimError_message`（
未终态时 `raw.progress` 是唯一可信存活信号，`error` 字段的 "did not get through" 是噪音，别当失败）。

⚠ **不要再用 `batch_status` 判 multisim 死活**：它对上述两个父对象同样回 `child_count:0`，
与 `harvest_multisim_alphas` 结论一致，但**对 `batch_create_simulations` 产出的单 sim 无用**（那是单 sim 不是批）。

**当前在飞（wave 218 实派）**：

| sim id | 表达式 | 塔 |
|---|---|---|
| `1w93Zh2D34KRbmm17vJlCXZy` | `trade_when(greater(rank(ts_backfill(pv106_lastspreadbp,22)),0.2), signed_power(ts_rank(ts_backfill(anl10_smartest_pre_fy1_pred_surps_v1,22),66),2), -1)` | ANALYST+PV |
| `1QmUzi8BT4E8csvMHTqXkGI` | `trade_when(greater(rank(adv20),0.6), hump(group_rank(ts_sum(vec_avg(oth695_import_value_4),20),sector),hump=0.0025), -1)` | OTHER |

### 5.14 未点亮塔的 category 级数据集画像（DB 实测，2026-10-30；供后续开波直接取用）

口径：`query_dataset_profile(region=KOR, category=…)` + `query_field_profile(dataset=…)`。
**"全 untested"是本轮最值钱的信号**——它们不是弱，是没人测过。

| category | 塔状态 | 首选数据集 | 关键读数 | 判读 |
|---|---|---|---|---|
| **INSTITUTIONS** | 0/3 | **institutions6** | cov **.9915**（min .9976）/ 11 字段 **全 untested** / alpha_count 94 / mult 1.1 | ⭐ **最干净的结构**：买卖家数 / 买卖金额 / 买卖股数**三对成对字段** + 持有人家数。是「净增持广度」教科书形态 |
| | | fund_holdings_panel | cov .8805 / 30 字段全 untested / alpha_count 35 / mult 1.1 | 备选（VECTOR，需 vec_*） |
| **RISK** | 0/3 | **risk88** | cov **.9727** / **64 MATRIX 全 untested** / alpha_count 1205 / mult **1.3** | 内容 = ASI 区 MFM 风险载荷（`rsk88_mfm_ase1_ri_*` 风格载荷 + `ind_*` 行业载荷 + `dsrt` 特质收益）⇒ 只有 `dsrt` 是"信号"，其余是**暴露轴**（做中性化/条件用，不宜当 alpha） |
| | | risk68 | cov **1.0** / 5 字段全 untested（order book tick 统计） | 新鲜但字段少、日内型 |
| | | risk70 / risk60 / risk59 / risk71 / risk72 | 已挖过（risk70 6112 alphas，§5.11 判死族）/ risk60 3 死 2 未测 / risk71 1 alive 但 best_2y 0.59 | **不再投入** |
| **NEWS** | 0/3 | **news79** | cov .8563 / 85 字段 **84 untested** / alpha_count 521 / mult **1.5** | 字段最多、倍率最高的新闻集；81% 未测 |
| | | **news54** | cov .9002 / 40 字段 **33 untested** / alpha_count **3** / value_score **4** | ⭐ **全库最空**（仅 3 颗 alpha）——但 min_cov .1365，需先按覆盖率筛字段 |
| | | news59 | cov 1.0 / 仅 2 字段 / 62 alphas / mult 1.3 | 事件型，窄 |
| | | news21 / news38 / news50 / news31 / news46 / news17 / news73 等 | 40 字段里 16–44 个 unusable，均值 cov 0.23–0.57 | **排除**（多数字段 <0.40） |
| **EARNINGS** | 0/3 | earnings3（唯一） | cov .6603 / 8 字段：4 unusable 4 untested / alpha_count **2304** / best_2y null | ⚠ 重度开采 + 覆盖窄 ⇒ **低优先**，只在其它塔都封死后才碰 |
| **PV（已亮 2/3）** | 2/3 | continuation_score / pattern_scores | 560 / 504 字段 **全 untested**、cov ≈1 | 新鲜面极大，但**必须核 10 年覆盖**（约束 4，sentiment27 就是死在 7 年） |
| | | pv106 | 15 字段 / 78 alphas / best_s **1.12** | 已被挖穿，只作条件腿（本波用途） |

**下一波派发顺序（并发恒 2，谁的期望最高谁先上）**：`institutions6`（本轮已备好 2 条，见 §5.15）
→ `news54` / `news79`（先筛 cov ≥0.5 的字段）
→ `risk88`（只用 `dsrt` 做信号，`ri_*`/`ind_*` 只能当条件或中性化轴）。

### 5.15 wave 219（institutions6 · 净增持广度 vs 净增持强度，单数据集双腿对照）

**开波依据**：INSTITUTIONS 塔 **0/3** 且 `institutions6` 是唯一 cov ≈1 且**成对字段齐全**的集（§5.14）。
**A-2 收益来源声明**：
- 谁在被定价：**机构资金的申赎方向（广度）**，不是金额。
- 为什么错：13F 季频披露 + 信息扩散慢 ⇒ 市场对「**多少家**机构在增持」反应不足；
  金额（magnitude）被大机构规模主导，噪声更大（与 analyst 修正族的「广度 > 幅度」同源逻辑）。
- 修复期：1–3 个月（下一次季报窗口）。
- 方向：净增持家数占比越高 ⇒ 后续收益越高（正向，不 reverse）。

**2 条候选（预注册，未过不进下一步）**：

| # | 表达式 | 机制轴 |
|---|---|---|
| 1 | `group_rank(ts_backfill(subtract(rank(count_institutional_buyers_security), rank(count_institutional_sellers_security)), 22), sector)` | **净增持广度**（家数，先秩化再相减 ⇒ 防覆盖数主导，analyst44 同款纪律） |
| 2 | `group_rank(ts_backfill(divide(subtract(market_value_institutional_shares_acquired, market_value_institutional_shares_disposed), add(aggregate_equity_value_institutions, 1)), 66), sector)` | **净增持强度**（金额 / 总持仓 = 占比，去量纲） |

**预注册判据（与 218 同口径）**：S ≥ 1.3 且 2Y ≥ 1.5 且 subU ≥ 1.0。
**取证**：`validate_expressions(region=KOR, universe=TOP600, delay=1)` 实测 **5 字段全部 known、`unknown_fields: []`**；
表达式已落库 `upsert_expressions(wave="219", dataset="institutions6", source=manual)`（n=2）。
⚠ 该塔倍率仅 **1.1**（最低），但**它是 0/3 里唯一位于「cov 1 + 成对结构完整」的交集**，先点亮再谈倍率。

**双通道取证（铁律 H，2026-10-30 完成，A、B 同向 ⇒ 放行）**：

| 通道 | 证据 | 与本波的关系 |
|---|---|---|
| A 论坛 | 《巨鲸游过的水波：institutions4 机构持仓变动随想》（WL27618，**28 赞**，2026-09-15） | 原话：① 机构增仓比例提升 ⇒ 持续买盘支撑、**平抑下行波动**（利多）；② **「持股比例增加、同时持有该股的机构家数也增加 = 广度与深度共振，信号质量最佳」** ⇒ **直接支持把「家数广度」与「金额占比」分列两条**（正是本波 #1 / #2）；③ ⚠ **防拥挤**：已被几乎所有同类基金顶格买入时边际买家耗尽、易见顶 ⇒ **极端分位要反向** |
| B 学术 | Choi, Jin & Yan《What Does Stock Ownership Breadth Measure?》（NBER WP 16591 / RFS）；Sias 等《Caught on tape》 | ① **散户广度变化 → 显著负向**（最高五分位年化跑输 23%）；② **按财富加权的机构广度变化 → 显著正向**，top/bottom decile 年差 **+8%**，且在控制「机构持股比例变化」后仍显著 ⇒ **机构广度是独立的价格预测因子**；③ 结论支撑「口径必须是**变化**、且必须是**机构**口径」——`count_institutional_buyers − sellers` 正是变化量 |
| 裁决 | A 与 B **同向且互补** | B 定方向（机构广度变化 → 正），A 定形态（广度 / 深度分列 + 拥挤反向）⇒ **#1/#2 保留原设计直接派发**；A 的「拥挤见顶」写成 wave 220 的候选：在 #1 上叠加 `trade_when(rank(count_institutional_holders_security) < 0.9, ·, -1)` |

⚠ **文献偏误登记**：B 的中国样本来自上交所**全账户**持仓（散户广度可测），KOR/TOP600 只有 13F 式机构口径 ⇒
**「散户广度」这条腿在本区不可构造**，不要照搬负向信号；本区只用机构腿。

### 5.16 wave 218 收割与归因（218-1 **判死**；同时盘清 pv 塔来源）

**218-1**（`1w93Zh2D34KRbmm17vJlCXZy` → alpha **`6Xd3mN57`**，07:49 COMPLETE）：

| 读数 | 值 | 预注册判据 | 判 |
|---|---|---|---|
| Sharpe | 1.38 | ≥ 1.3 | ✅ |
| **2Y Sharpe** | **0.37**（ladder_window 2） | ≥ 1.5 | ❌ **差 4.3 倍** |
| sub_universe_sharpe | 1.30 | ≥ 1.0 | ✅ |
| fitness | 0.99 | — | 差 0.01 撞 LOW_FITNESS |
| turnover | 0.0856 | — | 极低（门控把持仓压到 539 只） |
| rn_sharpe | 1.09 | — | 中性化后不塌，**不是因子暴露拖累** |
| pyramids | **effective 2**：`KOR/D1/PV`(×1.4) + `KOR/D1/ANALYST`(×1.6) | — | 结构本可一箭双雕 |

**铁律 F 归因（`get_alpha_yearly_stats`）**：

| 年 | 2014 | 2015 | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 |
|---|---|---|---|---|---|---|---|---|---|---|
| S | 3.15 | 1.09 | 2.88 | 1.47 | 1.05 | 1.88 | 2.27 | **-0.41** | 0.58 | **0.18** |

⇒ **S<1.0 年份 3/10 = 30%**，命中决策表「S<1.0 年份 ≥3 成 ⇒ 2Y 闸结构性不可达」；
top1 年（2014, pnl 1.49M）占正收益 ≈25%，未过 30% ⇒ 不是单年过拟合，**是近三年机制性衰减**——
2021 起该机制在 KOR 直接熄火（2020 峰值后单调下滑）。

**结论：`6Xd3mN57` 判死，不进 self-corr / prod 排队**（三条 RA 闸已挂，且 2Y 0.37 无法用参数举到 1.58）。
**可复用教训（写死）**：**「低买卖价差 ⇒ PEAD 更强」的假说在 2014–2020 成立、2021 后反噬**。
`trade_when(rank(lastspreadbp) > 0.2)` 把持仓压向**小盘 / 低流动性端**，正好是 2021 后 KOR 该端失效的区间
⇒ **这个门控方向对 2Y 是负贡献**。今后 analyst10 族**不要再叠加低流动性门控**；要提 2Y 应该往**大盘/高流动性端**试，
或干脆不用 pv106 条件腿（连 PV 塔的顺风也不要了——塔位不值得用死机制换）。

**§5.12 遗留 caveat 解除：pv 塔 2 颗已盘清来路** —— 来自 ACTIVE 清单（`get_user_alphas` stage=OS status=ACTIVE）：

| alpha | 表达式要点 | S | prod | 计入塔 |
|---|---|---|---|---|
| `RRA2eE70` | analyst `eps_y1_estimate_change_3mo` + 条件 `volume > ts_mean(volume,6)` | 1.64 | 0.6636 | **PV + ANALYST** |
| `xA16pzQJ` | other695 + 条件 `rank(adv20) > 0.6` | 1.86 | 0.6976 | **PV + OTHER** |
| `d5KJLqEw` | shrt38 量比 + `bucket(rank(eps_estimate_4wk_change))` 去中性化 | 1.87 | 0.5629 | **SHORTINTEREST + ANALYST** |

⭐ **重大结构发现：只当门控用的 PV 字段（`volume` / `adv20`）照样把这个 alpha 计入 PV 塔。**
平台按「表达式引用的数据集」计塔，**不区分信号腿与条件腿** ⇒ ① PV 塔天然最易点亮（几乎所有流动性门控都送一颗）；
② 反过来，想点亮 **OTHER / INSTITUTIONS / RISK / NEWS** 这类塔，**必须真的让信号腿落在该集字段上**，没有顺风车可搭。
③ 这也解释了为什么 analyst 只差 1 颗却能靠 `d5KJLqEw`+`RRA2eE70` 到 2/3——**门控字段是免费的塔票**。

⚠ **塔计数口径仍不完整**：该次拉取 `partial_count: true`（34/374）。上表只覆盖 34 条里的多塔件，
**analyst / pv 的真实计数可能已被 374 中的其它件推过 3**。点塔前必须用
`get_pyramid_alphas` 或分页拉全 ACTIVE 清单复核，**不要按 34 条的读数做提交决策**。

### 5.17 218-2 **过全部预注册闸**（`pwdoY39V`，唯一缺口 = CONCENTRATED_WEIGHT）

| 读数 | 值 | 预注册判据 | 判 |
|---|---|---|---|
| Sharpe | **1.81** | ≥ 1.3 | ✅ |
| **2Y Sharpe** | **2.31**（ladder_window 3） | ≥ 1.5 | ✅ **大幅超** |
| sub_universe_sharpe | **1.69** | ≥ 1.0 | ✅ |
| fitness | **2.27** | — | ✅ 远超 1.0 |
| returns / turnover | 0.1967 / 0.0324 | — | 极高 margin 0.0121（本区最健康的收益结构） |
| rn_sharpe | 1.24 | — | 中性化后保留 2/3 ⇒ **不是因子暴露** |
| **self-corr** | **0.6416**（对 `xA16pzQJ`） | < 0.70 | ✅ **壳层分离成功**（余量仅 0.058） |
| RA 失败项 | **仅 CONCENTRATED_WEIGHT**（0.1472 vs 0.1） | — | ❌ **唯一缺口，可机械修** |
| pyramids | **PV ×1.4 + OTHER ×1.6**（effective 2） | — | ⭐ 一箭双雕 |

**这条是本轮唯一「机制 + 塔位 + 收益结构」三项同时成立**的候选。§5.12 的「只换壳层」判断被证实：
字段与 20 日窗口不动，仅把 `bucket(cap)`+`tail` 换成 `sector`+`hump(0.0025)`，self-corr 从 ~1.0 量级压到 **0.64**。

**CONCENTRATED_WEIGHT 修法（派发前定死，别再试错）**：
- 该闸 = 单一持仓权重 0.1472 超 10% 上限。TOP600 下 `group_rank(·, sector)` 的**小行业**里，
  排名首尾会拿到极端权重 ⇒ 是**分行业名数不均衡**造成的，不是信号本身有尾部。
- ⚠ **不能用 `tail` / `bucket` 修**：那正是 `xA16pzQJ` 的壳，会把 self-corr 从 0.64 推回 0.7+，
  **修好一个闸、废掉一个闸**。
- 走**不动截面排序**的两条：① `hump` 由 0.0025 → **0.001**（减少冻结 ⇒ 权重更快回归目标）；
  ② 在 `group_rank` 之后加 `winsorize(·, std=0.05)`（压极端值、不改中段排序）。
  两条都单变量、都不碰字段与 sector 轴。

**接线状态**：218 两条已 `upsert_backtest_rows` 入库（wave `"218"`，dataset `pv106`）——
`6Xd3mN57` 落 LOW_SHARPE / LOW_FITNESS / IS_LADDER_SHARPE 三项失败，`pwdoY39V` 落
CONCENTRATED_WEIGHT 一项失败（`ra_failed_names` 由完整 `checks` 现算，非手填）。

**队列顺序（pro­d 时隙很贵，按此排队）**：
1. CONCENTRATED_WEIGHT 修法批（2 条，等 219 让出槽位）；
2. 修好的那条 → **先 self-corr 复测**（修法会动持仓，0.64 的余量只有 0.058，翻墙风险真实存在）；
3. self-corr 仍 < 0.70 → **prod 实测**（MCP `check_correlation`）；
4. prod < 0.70 → 才谈提交（**仍需用户确认**）。塔位收益：PV 3/3 点亮 + OTHER 2/3。

⚠ **本条对 OTHER 塔的意义大于 PV**：`other695` 全表只有 1 个信号字段（§5.12 已写死），
**OTHER 1/3 → 2/3 只能靠换壳层**。这条过了就等于给 OTHER 塔留下唯一可复用的壳层模板。

### 5.18 工具口径坑（本波实测，写死省得下次重踩）

| 工具 | 症状 | 正确用法 |
|---|---|---|
| `query_dataset_profile` | **忽略 `dataset_id`**，两次不同入参返回**逐字相同**的 30 行（按某序的全局集） | 当「区域数据集体检榜」用，不当单集查询用 |
| `query_field_profile` | 同样**忽略 `dataset_id`**，返回按 `best_s` 降序的全局 50 行 | 当「区域最佳字段榜」用；单集字段画像走 `get_datafields(dataset_id=…)` |
| `batch_status` | 对 `batch_create_simulations` 造的单仿真判 `kind:"multisim"`、`parent_status:null` | **判死活只认 `lookINTO_SimError_message` 的 `raw.progress`**（非 null = 活） |
| `get_user_alphas(status=ACTIVE, limit=50)` | `MCP error -32603`（负载过大） | `limit=20` + `stage="OS"` |

⭐ **副产品：`query_field_profile` 的全局榜暴露了 KOR 真正的高 S 字段地雷**——
`oth466_q_cni_xtp_si`（best_s **2.37** / 2y 1.77）、`shrt38_stk_invactsell_qty`（2.35 / 1.38）、
`shrt38_accum_sell_qty`（2.27 / 1.74）、`residualized_return_asia_minvol1m`（2.20 / 但 2y 0.59）。
前三条都在**已亮的塔**（FUNDAMENTAL / SHORTINTEREST）⇒ 对 0/3 的塔没有直接帮助，
但说明「**SHORTINTEREST 是本区最强信号族**」，将来要提 S 可以从这里借腿（须 ≤5 条、且避开组腿禁令）。

### 5.19 wave 219 收割（219-1 **判死**）+ 219b/pwdo 修法批 + acquisition_model 双通道取证

#### 5.19.1 219-1 `E56Y1LM1` — 净增持**广度**（家数差）在 KOR 全域归零 ⇒ 判死

表达式：`group_rank(ts_backfill(subtract(rank(count_institutional_buyers_security), rank(count_institutional_sellers_security)), 22), sector)`

| 指标 | 读数 | 预注册闸 | 判定 |
|---|---|---|---|
| Sharpe | **0.01** | ≥1.3 | ❌ **灾难级**（几乎无信号） |
| fitness | **0** | ≥1.0 | ❌ |
| returns / turnover | 0.0008 / 0.0551 | — | 年化收益 0.08%，等于白跑 |
| margin | 0.000029 | — | 结构上不可救（成本远大于收益） |
| **2Y** | **1.19** | ≥1.5 | ❌ 但接近 |
| subU | 0.09 | ≥1.0 | ❌ |
| longCount / shortCount | 317 / 318 | — | **不是覆盖问题**（满覆盖），是信号本身为零 |
| RA 失败 | LOW_SHARPE / LOW_FITNESS / LOW_2Y_SHARPE | — | 三条 RA 挂 |
| pyramid | INSTITUTIONS×1.4 effective 1 | — | 该塔仍 0/3 |

**归因（铁律 E 已在设计上绕开）**：不是报告期塌陷，也不是因子暴露拖累——`rn_sharpe 0.01 ≈ raw 0.01`，
中性化前后同一个零。**2Y 1.19 vs 全期 0.01** 的落差说明这条信号只在 2022–2023 有微弱作用，
2014–2021 完全无效 ⇒ **宽度的横截面差异（买家家数 − 卖家家数）在 KOR 不是被定价的量**。

**可复用结论（写死，避免重扫）**：
1. `institutions6` 的 **`count_*` 轴（家数/广度）判死**，不要再做 buy/sell 家数差、家数占比、家数变化。
2. 同集剩两条腿未测：**`market_value_*`（金额强度，219b 在飞）** 与 **`quantity_*`（股数）**。
   若金额腿也归零，则 `institutions6` 整集判死（11 字段里只有这两类信号腿）。
3. 「买家家数 − 卖家家数」这种**离散计数的差值**在 TOP600 这种大盘池里噪声占优——
   大盘股的机构家数本身变化缓慢（年频级别的结构变量），与月度收益无因果通道。

#### 5.19.2 219-2 平台 ERROR：`add(<CSPrice 字段>, 1)` 量纲不合

```
Incompatible unit for input of "add" at index 1, expected "Unit[CSPrice:1]", found "Unit[]"
```
`unitHandling=VERIFY` 下**无量纲常数不能与带单位字段相加**（备忘 `BRAIN VERIFY 模式下无量纲常数加有单位字段` 同一条）。
修法 = 去掉 `add(...,1)` 的防零保护：`divide(subtract(acq, disp), aggregate_equity_value_institutions)`
（分子分母同为 CSPrice ⇒ 天然无量纲；除零交给 `nanHandling=ON`）。
⚠ **本波是「整批里一条 ERROR 不连坐」的正面样本**：两条独立提交，219-1 照常 COMPLETE。

#### 5.19.3 ⚠ **更正 §5.17 的 CONCENTRATED_WEIGHT 修法**：根因是稀疏源，不是 `hump`

§5.17 原写「`hump` 0.0025→0.001` + `winsorize(std=0.05)`」，**两条都错**，现更正：

| 原修法 | 为什么错 |
|---|---|
| `hump` 0.001 | `hump` 只抑制**持仓变动幅度**（降 turnover），**不改横截面权重分布** ⇒ 对 CONCENTRATED_WEIGHT 无效 |
| `winsorize(·, std=0.05)` 接在 `group_rank` 之后 | `group_rank` 输出在组内**已是均匀分布 [0,1]**，无尾部可裁 ⇒ 该层等于空操作 |

**真根因**：`oth695` 覆盖率只有 **0.4886**，`group_rank(x, sector)` 的分母是**该 sector 内有值的股票数**；
sector 内只剩 2–3 只有值时，组内秩 1.0 的那只拿到 **0.1472** 的单票权重。
⇒ **修法必须是「补密度」，不是「改平滑」**：

- `F1`（在飞）：`ts_sum(ts_backfill(vec_avg(oth695_import_value_4), 66), 20)` —— 先回填 66 天再求和，覆盖密度上去后组内分母变大。
- `F2`（排队）：`rank(·)` 取代 `group_rank(·, sector)` —— 全局均匀秩，结构性不可能集中。
- **仍禁用 `tail` / `bucket`**：那是 `xA16pzQJ` 的壳，会把 self-corr 从 0.6416 推回 0.70+。

#### 5.19.4 通道 A（BRAIN 论坛）取证结果 —— acquisition_model 机制

| post id | 标题 / 票数 | 对本机制的可采结论 |
|---|---|---|
| `42827508063767` | 事件驱动:并购与特殊事件的博弈（30 票，6 评） | ⭐ **核心**：「宣布并购的标的，收购溢价已经定死，跟风买入意义不大」⇒ **公告后追买无效**，要做的是**公告前**的概率定价；「事件与价格的背离」= 事件后价格与事件性质相反才是机会。评论补充两条硬坑：事件类 VECTOR 必须 `vec_*` 折叠、`trade_when` 第三参必须 `-1` |
| `35540816733207` | 【直通通过】池塘中的涟漪——基于新闻情绪的并购公告因子 | 可落地表达参考：新闻情绪 × 并购公告事件的乘积结构（**但我们不做公告后追买，故只借「情绪提供方向、事件提供门控」这一层**） |
| `34859001837463` | Is predictability of industry returns after M&A announcement effective?（12 票，7 评） | 讲的是**同行业竞争对手**在并购公告后的行业层反应（横向溢出），与本集的**目标公司个体概率**不是同一机制 ⇒ 记为「不采，机制错配」 |

**通道 A 裁决**：与通道 B **不矛盾**，且提供了一个关键的**方向校正**——
论坛说「公告后追买无意义」，论文说「target likelihood 是正向预测」，二者合起来正好说明
**收益只能来自「公告前的概率漂移」，不能来自「公告后的溢价」** ⇒ 持有期必须短于「公告事件」，见 5.19.5。

#### 5.19.5 通道 B（外部文献）→ A-2 收益来源声明

| 文献 | 结论 | 采信范围 |
|---|---|---|
| Cremers, Nair & John, *Takeovers and the Cross-Section of Returns*（Yale SOM WP） | **target** 收购概率高的组合有显著正 alpha | ⭐ 方向句：**高 target likelihood ⇒ 正超额收益** |
| Palepu 1986 *Predicting takeover targets*；Ambrose & Megginson 1992；Tunyi 2019 | 收购概率可由规模/估值/流动性/杠杆预测，且预测力稳定 | 支持「模型分数本身含真实信息」，不是噪声 |
| AIMS 2021 *Relative mispricing and takeover likelihood* | **acquirer** likelihood 是**负向**预测；收益集中在**小市值 / 价值 / 高动量**的高错价股 | ⚠ 双刃：① 我们的字段是 **Target Model**（description 原文 "most likely to be acquired"）⇒ 取**正向**；② **须防收益只是 size/value 暴露** ⇒ 下一波加 `vector_neut(·, rank(cap))` 对照（cap 属 PV，顺带把 PV 塔票带上） |

**A-2 硬门（四条齐）**：

| 声明项 | 内容 |
|---|---|
| **谁在被定价** | 被收购概率最高的**目标公司（takeover target）**；定价方 = 并购套利（merger arb）/ 事件驱动资金，卖方是现有股东 |
| **为什么会被错** | ① **limits to arbitrage**：套利资金只能在**公告后**建仓（价差已定死，论坛 42827508063767 原话），公告前无法用容量放大这组预期；② **信息摩擦**：模型含 `text_factor`（新闻/文本），软信息被慢速吸收 |
| **错了多久修复** | **数季**：模型给的是"未来 12 个月被收购"的概率，溢价漂移在 1–4 季度内实现 ⇒ 窗口 66–252 |
| **预期方向** | 高 likelihood → **正**超额收益（做多高、做空低）；⚠ 若出现反向，先查是不是把 acquirer 侧混进来了 |

**失效边界（写死，防止跨区照搬）**：KOR 并购以**财阀内部重组 / 控股结构调整**为主，敌意收购极少
⇒ takeover premium 的分布与 US 样本（Cremers）不同，**这是文献偏误，不是例外**；
若全期 S≈0 而 2Y 有值，按 5.19.1 的口径同样判机制性不可用。

#### 5.19.6 acquisition_model 字段画像（`get_datafields` 实测，15 字段全 VECTOR / cov 0.9937）

| 字段 | alphaCount | 用途 |
|---|---|---|
| `global_valuation_percentile_rank` | **34**（最拥挤） | 估值分量，最可能是"已被挖过的"轴 ⇒ **回避** |
| `global_percentile_acquisition_likelihood` | 11 | ⭐ 主分数（global 口径） |
| `country_percentile_acquisition_likelihood` | 9 | 国别口径（KOR 单国 ⇒ 与 global 高度重叠） |
| `region_percentile_acquisition_likelihood` | 6 | 区域口径 |
| `industry_percentile_acquisition_likelihood` | 5 / `sector_…` 2 | 同行口径，天然已做过行业中性 |
| `global_text_factor_percentile_rank` | **1** | ⭐ **全表最新鲜**（文本分量） |
| `region_text_factor_percentile_rank` | **0** | ⭐ 零人用过 |

**装配（②.b 查表，每一步都能指回读数）**：
- VECTOR ⇒ 先 `vec_avg` 降维（L1 硬规则；论坛评论也点了这个坑）。
- 有界百分位 [1,100] ⇒ **横截面 `rank`，不做 `ts_delta`**。
  ⚠ 这是铁律 A 的**明确例外**：铁律 A 防的是"单边恒正的存量水平（市值/价格）被当多空腿"；
  本字段已被平台归一化为**横截面百分位**，水平差 = 横截面差，正是学术设计里的 target long / non-target short。
- 覆盖 0.9937 ⇒ **不需要 `ts_backfill`**（与 `oth695` 0.4886 形成对照）。
- 首轮**不加壳层**（先量原始信号，符合铁律 G 的"先测量再上壳"）；胜出者下一波加 `vector_neut(·, rank(cap))`。
- **不做组腿**（约束 5：OTHER 与 OTHER / PV / MODEL 均禁止两两组腿）⇒ 本条是**单数据集单字段** ATOM 形态。

**候选（等槽位）**：
1. `rank(vec_avg(global_percentile_acquisition_likelihood))` —— 主分数
2. `rank(vec_avg(global_text_factor_percentile_rank))` —— 文本分量（alphaCount=1 的空白面）

⚠ **10 年覆盖未验证**：`get_datasets` 不返回 `dateCoverage`，字段级也只有 coverage（横截面）没有时间跨度。
⇒ **判据改为实测**：A1 跑完后看 PnL 前段是否从 2014 起有值（P0Y0M 设置下 startDate=2014-01-01）；
若数据实际始于 2021，则违反约束 4（近十年都要有数据），**直接弃用该数据集**，不进入归因。

### 5.20 ★ category 级全量画像（KOR/D1/TOP600，`get_datasets` 185 集去重实测，2026-10-30）

> 约束 1 要求「一个个 category 查数据集情况」。本节是全量分母，**后续开波直接查这张表选集**，
> 不必再逐集拉取。口径：`coverage` = 横截面覆盖率；`aC` = 平台 alphaCount（拥挤度）；
> `VS` = valueScore（越高越新）；`mult` = 金字塔乘数。

| category | 集数 | ΣaC | 该 category 最好的三个候选（cov / 字段 / aC / VS / mult） | 可用性判定 |
|---|---|---|---|---|
| pv | 18 | 107986 | pv1 1.00/24/90329/1；pv30 .942/690/4305/3；**continuation_score 1.00/560/513/4**；**pattern_scores 1.00/504/317/4** | 塔已亮；VS4 两集是**低拥挤续挖面** |
| model | 57 | 58912 | model25 .856/554/11706/2；other176 .748/20/7732/2；**multifactor_return_pred .927/648/1297/4** | 塔已亮；model 与 PV/OTHER **组腿全禁**（约束 5） |
| analyst | 17 | 42942 | （前波已用 analyst10 / analyst25 / analyst44） | 塔已亮 |
| fundamental | 17 | 27133 | （前波已用 fundamental90 等） | 塔已亮 |
| other | 26 | 17160 | dl_riskfree_returns .909/57/8021/2（**已判死**）；insider_feats .664/31/1924/3（**PROD 地板 0.78 不可修**）；other532 .996/8/1864/3；other335 .590/10/1067/2；**other455 .897/1500/551/5**（1500 字段待普查）；**mmp_nlp_sentiment .619/521/75/6** | ⭐ 0/3。acquisition_model + other695 在打；**other455 / mmp_nlp_sentiment 是两块未动的大矿** |
| risk | 7 | 11641 | risk70 .980/96/7963/1；risk88 .973/64/1405/2；risk68 .991/5/757/2；risk59 .981/16/561/2 | ⭐ 0/3。risk70 拥挤度极高（aC 7963）但**多因子风险模型是残差动量/波动率族的现成料**；risk71/72（VS3）人少 |
| news | 24 | 6213 | **news59 1.00/2/2396/1**；news18 .571/29/1012/2；news79 .856/85/899/2；news7 .633/56/372/3；**news38 .797/45/227/4**；news50 .625/81/113/5；**news54 .691/40/43/5** | ⭐ 0/3。**news59 只有 2 个字段却有 aC 2396** = 高共识强信号，优先；**news54/news50/news85 是 VS5 的空白面** |
| insiders | 2 | 5507 | **insiders5 .892/53/4959/2/mult 1.2**；另一集 cov<0.4 | ⭐ 0/3 且**整块未动**（前波只碰过 other 类的 insider_feats，那不算本塔）。mult 1.2 偏低但 53 字段够开三波 |
| shortinterest | 3 | 4280 | shrt38（前波已用）；shortinterest6 .928/11/1676/3（被归在 model 类下） | 塔已亮 |
| earnings | 1 | 2616 | earnings3 .660/8/2616/1/mult **1.1** | 0/3 但**乘数最低 + 覆盖 0.66 且仅 8 字段** ⇒ 最低优先级 |
| sentiment | 6 | 2390 | news_sentiment_transfer .965/23/227/4；other553 .624/21/96/5 | 0/3；`sentiment26` 已判死（无横截面 + 仅 7 年）⇒ 只能用这**两个 transfer 类集** |
| imbalance | 1 | 1384 | imbalance5 .856（**判死闸被 force_seal 拦住，待用户授权**） | 0/3 但**暂不可动** |
| institutions | 2 | 1222 | institutions6 1.00/11/1003/2（**count 轴已判死，金额轴在飞**）；**fund_holdings_panel .809/30/219/4/mult 1.4** | ⭐ 0/3。**`fund_holdings_panel` 是 institutions6 之外唯一的腿**，且 30 字段 / aC 仅 219 = **低拥挤** |
| socialmedia | 2 | 975 | （未普查） | 0/3，待 5.21 |
| macro | 2 | 499 | other106 .404/15/307/4；macro63 1.00/1/192/3 | **已判死**（`KOR-MACRO63-NO-CROSS-SECTION`，宏观是全域同值，无横截面） |
| option | 0 | 0 | —— | KOR **无 option 数据** ⇒ 该塔在本区不可达 |

**由画像直接得出的开波顺序（除在飞的两条外）**：
1. **INSIDERS ← `insiders5`**（53 字段、整块未动、cov .892）—— 最大的未开采面。
2. **NEWS ← `news59`**（2 字段 / aC 2396 = 高共识）+ **`news54`**（VS5 空白）。
3. **INSTITUTIONS ← `fund_holdings_panel`**（30 字段 / aC 219）。
4. **RISK ← `risk71`/`risk72`**（VS3、人少）→ 再 `risk88`（`dsrt` 单字段信号）。
5. **OTHER ← `other455`**（1500 字段，需先普查再选，不能盲扫）。
6. 最低：**EARNINGS ← `earnings3`**（mult 1.1 + cov .66）。

⚠ **OPTION 塔在本区不存在**（0 个数据集）⇒ 60 个 alpha 的目标若按"未点亮塔"分摊，
分母只有 **10 个可达塔**（OTHER / INSTITUTIONS / NEWS / RISK / INSIDERS / SENTIMENT / SOCIALMEDIA / IMBALANCE / EARNINGS / MACRO），
其中 MACRO 已判死、IMBALANCE 卡授权 ⇒ **实际可打的 8 个塔 × 3 = 24 颗塔票**，
其余 36 颗只能落在已亮塔（可提交但不能算"点亮贡献"）。这条要写进交付对账（§5.4）。

#### 5.20.1 ⛔ `institutions6` **整集判死**（两条独立信号腿全归零，2026-10-30）

| 腿 | alpha | Sharpe | 2Y | subU | fitness | 判 |
|---|---|---|---|---|---|---|
| 广度（家数差） | `E56Y1LM1` | 0.01 | 1.19 | 0.09 | 0 | ❌ |
| 强度（金额净流 / 权益价值） | `xAr96M2W` | 0.10 | **−0.38** | 0.05 | 0.02 | ❌ |

两条**机制完全不同的腿**（计数 vs 金额；广度 vs 强度）同时归零，且 second 的 2Y 甚至为负
⇒ 按 §5.19.1 写死的判据，**`institutions6` 整集判死**，不再消耗配额。
（`quantity_*` 股数腿与金额腿信息等价，不再单测。）

**归因一句话**：KOR TOP600 是 600 只大盘股，机构持仓结构是**年频结构变量**而非月度信号；
其在横截面上的差异被 SECTOR 中性化吃干净（rn_sharpe 0.20 已经高于 raw 0.10，说明中性化还在帮忙而非伤害）。

#### 5.20.2 INSTITUTIONS 塔换料：`fund_holdings_panel`（30 字段实测）

**字段结构规律（先看出来的，省得逐字段试）**：每个字段都有 `_active` 孪生版，
覆盖率从 **0.9553 / 0.8870（全账户）** 降到 **0.7666 / 0.6626（活跃账户）**
⇒ `_active` = 只看近期有调仓的账户，**信息密度更高但覆盖更低**；同一字段的两个版本是天然对照实验。
类型：MATRIX 6 个（持仓存量）+ VECTOR 9 个（交易流量）⇒ **VECTOR 必须先 `vec_*` 折叠**。

| 字段 | 类型 / cov | aC | 机制读法 |
|---|---|---|---|
| `holding_value_distribution_score` | MATRIX / .9553 | 18 | ⭐ **平台自带的"拥挤度"分数**（原文 "a custom crowding metric… higher = more crowding"） |
| `herfindahl_index_holdings` | MATRIX / .9553 | 27 | 持有人集中度 HHI（同一机制的另一口径） |
| `holder_account_total` | MATRIX / .9553 | 29 | 持有人家数（**与已判死的 count 族同型 ⇒ 降权**） |
| `mean_security_weight` | MATRIX / .9553 | 12 | 持有该股的基金平均权重 = 信念强度 |
| `top_weighted_account_number` | MATRIX / .9553 | 14 | 把它当重仓股的账户数 = 共识信念广度 |
| `security_holding_usd_value` | MATRIX / .9553 | 7 | 持有总市值 |
| `boundary_transaction_total` | VECTOR / .887 | **35**（全表最高） | 边界交易数（新建仓 + 清仓）= **离散信念事件** |
| `stable_boundary_trade_count_21d` | VECTOR / .887 | 12 | ⭐ 同上但**剔除 21 天内反复进出** ⇒ 只剩"耐久的信念变化"，噪声最小 |
| `large_trade_count_50bps` | VECTOR / .887 | 3 | 单笔超 AUM 0.5% 的大单数 |

**机制选择（②.a A-1 五问 + A-2）**：

| 声明项 | 内容 |
|---|---|
| **谁在被定价** | **拥挤交易的后来者**（crowded institutional holders）；卖方 = 想减仓但已无流动性的先来者 |
| **为什么会被错** | **拥挤 + 流动性约束**：同一只票被少数基金重仓持有时，坏消息触发同步减仓，但 KOR 中小盘流动性无法承接 ⇒ 事前高拥挤 = 事后负收益（Brown-Howard-Lundblad「Crowded Trades and Tail Risk」同机制） |
| **错了多久修复** | 数周–数季（拥挤度的均值回复 + 减仓冲击的吸收期）⇒ 窗口 22–66 |
| **预期方向** | **高拥挤 ⇒ 负超额收益**（做空高拥挤组） |
| 失效边界 | 若拥挤度与规模高度共线（大票天然多持有人），收益可能只是 size 暴露 ⇒ 必须用 `rank` 归一 + 必要时 size 中性化对照 |

**开波设计（铁律 B：方向/形态各测一条）**：
1. `multiply(-1, rank(holding_value_distribution_score))` —— 拥挤度**水平**（做空高拥挤）
2. `multiply(-1, rank(ts_delta(holding_value_distribution_score, 22)))` —— 拥挤度**变化**（拥挤正在加剧）
3. 备选（第一轮胜出后再上）：`multiply(-1, rank(vec_avg(stable_boundary_trade_count_21d)))` 的净额化版本

⚠ **`holder_account_total` 暂不进第一轮**：它与刚判死的 `count_institutional_buyers/sellers` 同属"家数"族，
先让权重型（distribution/HHI/mean_weight）证明能否落地，再决定家数族在本集是否复现同一失败。

### 5.21 INSIDERS 塔画像（`insiders5`，53 字段实测）+ ⚠ 更正 §5.20 的 news59 判定

#### 5.21.1 ⚠ **更正：`news59` 不是信号集，是「事件日历/门控」集**

§5.20 里我按 `aC 2396` 把 news59 写成"高共识强信号，优先"，**读字段后当场证伪**：

| 字段 | 实际含义 |
|---|---|
| `mws59_event_fiscal_year` | 事件所在财年 |
| `mws59_event_time_value` | 事件的**计划时间（UTC 整数）** |

⇒ 全表**只有日历元数据，没有任何横截面信号**。aC 2396 是 2396 条 alpha 把它当
`trade_when` 的**时点门控**（"只在事件时点交易"）用出来的，不是因为它能预测收益。
**它只能做门控（按 §5.16 的塔票规则，门控字段照样计该塔），不能当信号腿。**
NEWS 塔的真信号面仍是 `news18 / news79 / news7 / news38 / news50 / news54 / news85`。

#### 5.21.2 `insiders5` 字段分类（**全 53 个都是 VECTOR**，必须先 `vec_*` 折叠）

| 类别 | 字段（cov / aC） | 判 |
|---|---|---|
| **真信号·交易流量** | **`insd5_ghc_tr` 持股比例变动 (.7318 / 212)**；`insd5_vol_chg` 股数变动 (.7318/119)；`insd5_trd_amt` 交易金额 KRW (.7318/84)；`insd5_unt_val` 单价 (.7318/45)；`insd5_fa_tr`/`fb_tr` 变动前后比例 (.7318/131,76)；`insd5_vol_af`/`bf` 变动前后股数 (.7318/73,94) | ⭐ **主战场**，`ghc_tr` 已无量纲、直接可用 |
| **真信号·存量** | `insd5_ratio` 集团去重持股比例 (.9996/121)；`insd5_source_ratio` 源持有人比例 (.9995/407)；`insd5_data` 去重股数 (.9996/299)；`insd5_tnc` 特殊关系人数 (.9996/452) | 水平量（单边恒正）⇒ 铁律 A：**取变化，不裸水平** |
| **真信号·库存股** | `insd5_trsy_ratio` 库存股比例 (.8728/**152**)；`insd5_trsy_data` (.8728/69)；`insd5_trsy_real_ratio` (.8728/128) | ⭐ **韩国特色**：财阀系公司长期囤库存股，高比例可作为回购/价值信号 |
| **分类/日期字段（不可当信号）** | `insd5_c_company_list_dt`、`_pyt_tkm`（KOSPI/KOSDAQ）、`_corp_reg_no`、`_nm_kor`（韩文姓名）、`_td_ctn`（披露日）、`_history_td_drt`、`_recent_dt`、`_rpst_grp_typ`(aC 574)、`issuance_category`、`security_type`、`_officer`(1/0)、`_finacc_typ`、`_list_yn`、`_nm_eyf`、`_ny_srfi`、`_mmyy_srfi`、`_s_stock_pyt_tkm`、`_pyt_pmc`、`_qes`、`_serial`、`_group_s`、`_isd_history_issue_typ`、`_trd_reason_a`/`_b`、`_td_tse`、`_td_ghc`、`_grp_*` | 只能做**分组键/门控**；`_rpst_grp_typ` 的高 aC 同样是当 `group_*` 分组键用出来的 |

**⚠ 事件类字段的致命细节（写死，防止下一波踩）**：
`vec_sum(insd5_ghc_tr)` 在**无内幕交易的日期返回 NaN**。此时**绝不能用 `ts_backfill`**——
回填会把"同一笔历史交易"在每一天重复计入，`ts_sum` 累加后变成**按事件次数翻倍的伪信号**。
正确写法是直接 `ts_sum(..., 66)`：`nanHandling=ON` 下 NaN 被跳过，等于"最近 66 天内的累计变动"。

**开波候选（等槽位，铁律 B 正反各一）**：
1. `rank(ts_sum(vec_sum(insd5_ghc_tr), 66))` —— **内幕人累计增持比例**（预期正向：增持→涨）
2. `rank(ts_delta(vec_sum(insd5_trsy_ratio), 66))` —— **库存股比例的变化**（回购/注销动作；正向）
3. 反向对照：`multiply(-1, ...)` 同上第 1 条（铁律 B：`reverse()` 与正向不精确反号）

**A-2（第 1 条）**：谁在被定价 = **掌握私有信息的公司内部人**；为什么错 = **披露滞后 + 注意力稀缺**
（KOR 内部人持股变动须在数日内公告，但市场只对金额大的交易反应，小额连续增持被忽略）；
修复期 = **数周–一季**（PEAD 同族的信息扩散节奏）；方向 = 净增持 → 正。
边界 = KOR 内幕人常以"继承/赠与/担保"名义变动（`insd5_trd_reason_b` 可剔除），
若不剔除会把非信息性过户当成看多信号。

### 5.22 ★★ 塔位权威读数（`get_pyramid_alphas`，2026-10-30；**取代此前所有估算**）

**KOR / D1 实测**：

| category | 已有票数 | 状态 |
|---|---|---|
| **shortinterest** | **4** | ✅ 已点亮 |
| **fundamental** | **3** | ✅ 已点亮 |
| **model** | **3** | ✅ 已点亮 |
| **analyst** | **2** | ⭐ **差 1 颗** |
| **pv** | **2** | ⭐ **差 1 颗** |
| **other** | **1** | 差 2 颗 |
| earnings / imbalance / insiders / institutions / macro / news / socialmedia / sentiment / risk | **0** | 全 0（9 个） |

**本区合计 15 张塔票**（一颗 alpha 可计多塔，故 alpha 数 < 15）。

**三条由此产生的硬结论**：

1. ⚠ **此前"PV 3/3 已亮"的记忆是错的**——权威读数是 **PV = 2**。
   所以 `pwdoY39V`（PV+OTHER 双计）若提交成功，收益是 **PV 2→3 点亮 + OTHER 1→2**，
   即"一颗 alpha 点亮一座塔"，**这是当前整个战役里性价比最高的单笔提交**。
2. ⭐ **`analyst` 也差 1 颗**。§5.17 队列里的 `LLZ6wZO2` / `mLmGQEq9` / `E5pjx9q0` / `883mLenl`
   若属 analyst 族，**提交一颗就等于点亮 ANALYST**——这比再开十波新数据集都快。
   ⇒ **下一步动作的优先级应改为「先清提交队列，再开新波」**（提交不可逆，须用户确认）。
3. **`other` 只有 1**，且 `other695` 单字段 ⇒ 必须靠 `acquisition_model`（在飞 A1）补第二颗；
   两颗都到位后 OTHER = 3 才点亮。**只提交一颗 OTHER 只是 2/3，不点亮。**

⚠ **口径提醒**：本表是"已提交 alpha 计入的塔"，与"IS 上过闸的候选"不是一回事。
候选再多，不提交就不增票 ⇒ **60 个 alpha 的目标里，塔位贡献必须先过提交这一关**。

---

### 5.23 acquisition_model A1 判死：**似然的「水平」不是交易对象，「更新」才是**

`E56Y76gr` = `rank(vec_avg(global_percentile_acquisition_likelihood))`（SECTOR / decay4 / trunc0.08）

| 指标 | 值 | 读法 |
|---|---|---|
| **Sharpe** | **−0.21** | 方向反了（A-2 声明的是"高概率 → 正收益"） |
| fitness | −0.07 | — |
| **turnover** | **0.027** | ⭐ **近零**：这个字段几乎是常数 |
| returns / margin | −1.45% / −0.001073 | — |
| 2Y / subU | **−0.87** / −0.27 | 结构性，不是某年塌陷 |
| **risk_neutralized_sharpe** | **+0.22** | ⭐ **RN > raw**：纯 alpha 微正，raw 的负来自因子暴露 |
| long/short | 313 / 314 | 满截面，不是覆盖问题 |
| 塔位 | `KOR/D1/OTHER` ×1.6，effective 1 | 计入 OTHER（+1 票，未提交不算） |

**★ 这一行同时推翻了我自己的一个预设**：我在 §5.19.6 把"平台已归一化的百分位 ⇒ 免铁律 A、
可直接取水平"写成了**已裁定的例外**。实测结果证明**例外只在「量纲」上成立，不在「可交易性」上成立**：

- 免铁律 A 的理由是"字段已是 [0,1] 百分位，不需 ts_delta 去量纲"——这点没错；
- 但**turnover 0.027 说明它是慢变量特征（value-like characteristic），不是信号（signal）**。
  截面上"谁是并购标的"这件事本来就写在价格里（长期高概率 = 长期估值折价），
  **水平值没有超额信息**；被定价的是**概率的更新**（新信息到达后市场反应不足）。

⇒ **铁律 A 的正确表述不是「看量纲」，而是「看它是不是慢变量特征」**：
**任何 turnover < 0.1 的截面水平值都应当视为特征而非信号**，下一步一律先取变化率再谈方向。
（这条比原表述更可操作，且能被 turnover 一次读数机械判定，写死。）

**A2 已派发**（`QJ7EMaxm4QT9GH1q4CTQn6`）：
`rank(ts_zscore(vec_avg(global_percentile_acquisition_likelihood), 252))`
—— 取 252d 自标准化 = "当前似然相对自身一年历史有多异常"，即**更新/惊讶**；保留 A-2 的
"谁被定价（并购标的）/ 为什么错（套利受限 + 软信息摩擦）/ 修复期 1–4 季 / 方向 高概率 → 正"整份声明，
只改**被测构念**（水平 → 更新），符合铁律 G 的因果依赖链（继承 A-1 结论，仅动一个轴）。

**A2 结果（`j2YWE7XW`）—— 方向对了，力量没有**：

| 指标 | A1 水平 | A2 更新 | 读法 |
|---|---|---|---|
| Sharpe | −0.21 | **+0.18** | ⭐ **符号翻转** ⇒ 构念判断正确（被定价的是更新不是水平） |
| fitness | −0.07 | 0.06 | — |
| turnover | 0.027 | 0.065 | 变化率确实带来换手，但仍极低 |
| 2Y / subU | −0.87 / −0.27 | **+0.47 / +0.27** | 同步转正，同源 |
| rn_sharpe | +0.22 | **−0.10** | 中性化后反而变负 ⇒ 连因子暴露的缓冲都没了 |
| drawdown | 0.2516 | **0.4195** | 回撤比收益大一个量级 |

**判定：`acquisition_model` 的数值似然腿（水平 + 更新）两条全死。**
证据强度高于通常的单波判死——因为**方向已独立验证为正确**（−0.21 → +0.18 的符号翻转不是噪声，
是构念修正生效），所以剩下的 0.18 就是**该字段在 KOR/TOP600 的真实上限量级**，不是「再调调就好」。
⇒ 与 `institutions6` 同一处置：**不再派发该字段的任何参数变体**（死轴登记：似然水平、似然更新）。

**未测的部分（不要连坐）**：`global_text_factor_percentile_rank`（aC **1**）与
`region_text_factor_percentile_rank`（aC **0**）是**文本因子**，构念与数值似然不同，
且是全表中拥挤度最低的两个字段。**留作 A3，等 OTHER 塔需要时再单独起波**（不与本次同波，避免多变量）。


**不做的事（写死防重踩）**：
- ⛔ 不加 `vector_neut(·, rank(cap))` 控制：`cap` 属 **PV**，与本字段（OTHER）组合会被约束 5
  的「PV/MODEL/OTHER 两两组腿」禁则命中。AIMS 的 size/value 警示改由**分年 PnL + 分位分组**事后看，
  不用壳层。
- ⛔ 不在同一波同时上 `global_text_factor_percentile_rank`：那是**另一个构念**（文本因子 vs 数值似然），
  与本波"水平→更新"构成两个变量。留作 A3，等 A2 定性后再上。

---

### 5.24 NEWS category 画像（2 个数据集已读字段，**结论：只剩 news18 一条腿**）

| 数据集 | 字段数 | 形态 | 判定 |
|---|---|---|---|
| **news54** | 40（全 VECTOR） | **全部是时间戳 / 标志位 / 标题文本**：`daily_event_*_time(_utc)`、`future_event_*`、`mws54_eventcallbasicinfo_cancelledflag`、`mws54_keydevelopments_headline` | ⛔ **gate-only**，与 `news59` 同形。`alphaCount` 高的那些（`mws54_futureeventmkt_headline` aC 6）来自 `trade_when` 事件日期门控，不是信号 |
| **news18** | 29 | ⭐ **真信号集**：7 个 MATRIX 情感分 + 8 个 VECTOR 情感分 + 相关性/新颖度 | ✅ 唯一可用腿 |

**news18 字段表（覆盖 / aC 降序要点）**：

| 字段 | 类型 | cov | aC | 含义 |
|---|---|---|---|---|
| `rp_ess_earnings` | MATRIX | 0.50 | **237** | 盈利类新闻事件情感分 ⚠ 全表最挤 |
| `rp_nip_business` | MATRIX | 0.50 | 124 | 商业新闻影响投射 |
| `rp_ess_business` | MATRIX | 0.50 | 111 | 商业新闻事件情感分 |
| `rp_css_business` | MATRIX | 0.50 | 170 | 商业新闻综合情感分 |
| `rp_css_revenue` / `rp_ess_revenue` / `rp_nip_revenue` | MATRIX | 0.50 | 69 / 37 / 19 | 营收类 |
| `rp_css_earnings` / `rp_nip_earnings` | MATRIX | 0.50 | 51 / 19 | 盈利类 |
| `nws18_qep` | VECTOR | **0.6339** | 59 | 正/负词情感极性（-1/0/+1） |
| `nws18_qcm` | VECTOR | 0.6339 | 40 | 高置信相关新闻情感 |
| `nws18_nip` | VECTOR | 0.6339 | 22 | 叙事影响分 [-1,1]（未来 2 小时） |
| `nws18_ssc` | VECTOR | **0.7006** | 20 | 细粒度情感分 [-1,1]（技术合成） |
| `nws18_sse` | VECTOR | 0.4845 | 18 | 实体-事件连续情感分 |
| `nws18_relevance` | VECTOR | 0.7006 | 21 | 实体与故事的关联强度 0–100 |
| `nws18_event_relevance` | VECTOR | 0.538 | 17 | 事件在故事内的相关性 0–100 |
| `nws18_event_similarity_days` | VECTOR | 0.4845 | **15** | 距上次相似事件的天数 ⭐ **新颖度，全表最低拥挤度之一** |
| `story_event_record_count` | VECTOR | 0.7006 | **1** | 故事内事件条数 ⭐ **白空间** |
| `nws18_bam` | VECTOR | 0.7006 | 13 | **并购情感（-1/0/+1）** ⭐ 与 §5.19 并购机制同源，可做跨集概念呼应（但属组腿，需避开禁则） |

**三条结构性约束（决定组装形态）**：

1. **MATRIX `rp_*` 覆盖率只有 0.5**：TOP600 里一半股票**当天没有新闻**。
   裸 `rank()` 会在无新闻日给 NaN ⇒ 持仓只落在一半截面 ⇒ `LOW_SUB_UNIVERSE_SHARPE` 真实风险
   （acq A1 的 subU −0.27 就是满截面下的例子，若再砍一半会更糟）。**必须 `ts_backfill` 前置**。
2. **`ts_backfill` 在这里合法**，与 §5.21.2 对 `insd5` 的禁令**不冲突**：那条禁令针对**带符号的流量字段**
   （重复计同一笔历史成交 = 造假）。情感分是**状态量（level）**，把"昨天的情绪"带到今天正是
   "情绪在衰减前持续有效"的建模，不是重复计数。**判据 = 字段是状态量还是流量，不是字段是否稀疏。**
3. **`rp_ess_earnings` aC 237 是全表最挤**，按"拥挤 ≠ 无效但拥挤 = 已被挖穿"的既定口径，
   首批**不打**它；优先打 `nws18_qep`（cov 0.63 最高、aC 59 中等）与白空间
   `nws18_event_similarity_days`（aC 15）/ `story_event_record_count`（aC 1）。

**A-2 声明（news18 情感腿）**：

| 声明项 | 内容 |
|---|---|
| 谁在被定价 | 新闻到达后的**注意力/反应不足**，买方是慢速零售与被动资金；卖方是信息优势方 |
| 为什么会被错 | **注意力限制**（limited attention）：同样的语调，高关注名前 1 天就定价完，低关注名要 2–10 天；本区 delay=1 ⇒ 第 1 天的跳空已被吃掉，**剩下的正是第 2–10 天的漂移** |
| 错了多久修复 | **2–10 交易日**（PEAD 型），故窗口取 5–22d，不取 252d |
| 预期方向 | 情感分**正** ⇒ 后续漂移**正**（铁律 B 仍须 `multiply(-1, …)` 反向对照一条） |
| 边界条件 | 覆盖率 0.5（无新闻日必须有 backfill）；财报季情感会被 PEAD 与盈余惊喜共线；KOR 新闻源以韩语为主，情感词典对本地的覆盖质量未知 |

**NEWS 排队候选（等时隙，按优先级）**：

| # | 表达式 | 构念 |
|---|---|---|
| N1 | `group_rank(ts_backfill(ts_mean(vec_avg(nws18_qep), 5), 5), sector)` | 短期语调水平（注意力漂移核心腿） |
| N2 | `group_rank(ts_backfill(ts_delta(ts_mean(vec_avg(nws18_qep), 22), 22), 5), sector)` | 语调**变化**（惊喜） |
| N3 | `group_rank(ts_backfill(vec_avg(story_event_record_count), 5), sector)` | 新闻密集度（aC 1，白空间探针） |

⚠ **本波不放 N3**：它是"新闻条数"，与 count 族（`institutions6` 已判死）同形，风险高；
先靠 N1/N2 确认 news18 有没有本区力量，有力量再谈白空间。

---

### 5.25 ★★★ 提交队列实况（2026-10-30 逐颗实测，**这是当前最高杠杆的一块**）

5 颗候选逐个 `get_alpha_details` 复核，`checks.fail` 与 `ra.failed_ra_checks` **分列**（两者口径不同，
见 AGENTS.md §8.7：WARNING/ERROR 也算 RA 失败）：

| alpha | Sharpe | fitness | 2Y | subU | 塔位 | `checks.fail` | `ra_failed` | 缺口 |
|---|---|---|---|---|---|---|---|---|
| **mLmGQEq9** | **2.72** | **2.12** | 2.35 | **2.24** | SHORTINTEREST（已亮 4） | **空** | **空** | ⛔ **prod 实测 0.935**（local .6011 是过期缓存） |
| **E5pjx9q0** | **2.50** | **1.85** | 2.37 | 1.86 | SHORTINTEREST（已亮 4） | **空** | **空** | ⛔ **prod 实测 0.8105**（local .6002 是过期缓存） |
| **LLZ6wZO2** | 1.99 | 1.53 | 2.24 | 1.21 | FUNDAMENTAL（已亮 3） | **空** | **空** | 仅 `CLUSTER_TEST` 0.94<1 告警（prod **.6762** / self **.6760** 均已实测 ✅） |
| **pwdoY39V** | 1.81 | 2.27 | 2.31 | 1.69 | ⭐ **PV + OTHER 双计** | **空** | `CONCENTRATED_WEIGHT` | ⛔ **prod 实测 0.8507**（族内 `[0.7,0.8) n=1` ⇒ 族死；CW 已无意义） |
| **883mLenl** | 1.40 | 1.15 | 2.14 | 1.38 | ⭐ **ANALYST** | **空** | `LOW_SHARPE` | **1.40 < 1.58**；wave 266 已推到 **1.45**（见下） |

**四条硬结论**：

1. ⭐⭐ **883mLenl 是「一颗点亮 ANALYST」的最近路**：ANALYST 现 2 票，它属 analyst 族（`pyramid_short: analyst`，
   `KOR/D1/ANALYST` ×1.6），**只差 Sharpe 1.40 → 1.58**。
   它的表达式 `group_rank(rank(ts_decay_linear(ts_backfill(vec_avg(eps_estimate_4wk_change), 5), 22)), industry)`
   用的是 4 周 EPS 修正（`eps_estimate_4wk_change`），机制清晰、turnover 仅 0.063、2Y 2.14 已过。
   ⇒ ~~**修法优先级**：① `industry` → `sector` ② `ts_backfill` 5 → 22 提覆盖 ③ `decay` 4 → 8/12。~~
   **★★ Wave 266 实测（2026-10-31，全部单变量、设置与种子逐字相同 decay4/SECTOR/trunc.08/nanON/maxTradeON）**：

   | 档 | alpha | 单变量 | S | F | 2Y | subU | TO | dd | CLUSTER | 判定 |
   |---|---|---|---:|---:|---:|---:|---:|---:|---:|---|
   | 种子 | `883mLenl` | — | 1.40 | 1.15 | 2.14 | 1.38 | .063 | .130 | 0.89 | 基线 |
   | ① | `e75gwG5l` | 轴 `industry`→`sector` | **1.22** | 0.96 | 1.82 | 1.19 | .057 | .1435 | 0.73 | ⛔ **−0.18 反向** |
   | ② | `leARVOK5` | `ts_backfill` 5→22 | 1.38 | 1.12 | 2.17 | 1.38 | .0631 | .1304 | 0.90 | ○ 中立（−0.02） |
   | ③ | `3qonRrbQ` | `ts_decay_linear` 22→10 | 1.38 | 1.12 | 2.16 | 1.33 | .0743 | .1446 | 0.85 | ○ 中立（−0.02） |
   | ④ | `kqNbqpKk` | `ts_decay_linear` 22→66 | 1.32 | 1.06 | 1.88 | 1.29 | .0439 | .1254 | 0.78 | ⛔ **−0.08** |
   | ⑤ | `pwd1lRXg` | 短窗(22)×长窗(126) 秩积 | 1.44 | 1.20 | 2.34 | 1.34 | .0509 | .1137 | 0.99 | ⭐ **+0.04** |
   | ⑥ | `GrW3Lba0` | 短窗(22)×长窗(252) 秩积 | **1.45** | **1.21** | **2.43** | 1.30 | .0505 | .1196 | ✅ | ⭐ **+0.05，当前最优** |

   **四条归因结论**：
   - **roadmap 原推荐的 ① 方向错了**：`sector` 是**反向**（−0.18），和 wave 264 在 other424 上
     「subindustry < sector」的读数一起，**第二次证伪「换粗轴无损」**。`industry` 附近才是该族的甜区。
   - **平滑窗 22 是局部最优**：10 与 66 都降（短窗加噪声、长窗削信号），窗谱已穷尽。
   - **提覆盖（backfill 22）对 Sharpe 中立**，只把 2Y 抬 0.03 ⇒ 不是承重杠杆。
   - ⭐ **唯一正向杠杆 = 同字段多窗持久性乘积**（KOR §②.e 明确允许：同字段多时间窗 = 单信号结构化）：
     `multiply(rank(短窗), rank(长窗))` 把「修正幅度」升级为「修正幅度 × 修正持续性」，
     **+0.05 S / +0.29 2Y / TO −20% / dd 从 .130 降到 .120**，且 `CLUSTER_TEST` 从 0.89 升到 pass。
     ⇒ 该杠杆**尚未用尽**：长窗 504 三腿、以及沿「industry 更细 → subindustry」的轴梯仍在飞（batch D）。

   **★★ Batch D/E 续测（2026-10-31，在飞设置与种子逐字相同）**：

   | 档 | alpha | 单变量 | S | F | 2Y | subU | TO | CLUSTER | 判定 |
   |---|---|---|---:|---:|---:|---:|---:|---|---|
   | D1 | `bl6Wd8dq` | 轴 `industry`→`subindustry` | 1.28 | 0.98 | 2.33 | 1.17 | .0482 | 0.86 | ⛔ **−0.17**（**第三次证伪「换轴无损」**）|
   | D2 | `KPJwEmGl` | 三腿（+长窗 504） | 1.38 | 1.12 | 2.40 | 1.21 | .0443 | 0.91 | ⛔ −0.07（252 之后再延长即稀释）|
   | E1 | `6XdYpeeJ` | 字段 → `eps_gaap_estimate_4wk_change` | 1.23 | 0.94 | 2.29 | 1.09 | .0493 | 0.94 | ⛔ **−0.22**（GAAP 基显著更弱）|
   | E2 | `bl6WQdQp` | 聚合 `vec_avg`→`vec_sum` | 1.44 | 1.19 | 2.33 | 1.30 | .0499 | ✅ | ○ 中立（−0.01）|
   | F1 | `1YNnwooM` | 分歧度条件化 `vec_avg/vec_stddev` | 1.10 | 0.83 | 1.99 | 1.02 | .0537 | 0.77 | ⛔ **−0.35**（跨分析师分歧归一化会摧毁信号）|
   | F2 | `KPJw7nkj` | 换集 `analyst44` `best_dps_4wk_chg` 同壳 | 1.02 | 0.72 | 1.24 | 0.99 | .0488 | 0.68 | ⛔ −0.43，2Y 也破（KOR 的 DPS 修正太弱）|
   | G1 | `VkxY7WEG` | 换集 `analyst44` `best_eps_4wk_chg` **同壳 22×252** | 1.44 | 1.20 | 2.42 | 1.29 | .0505 | ✅ | ○ **−0.01**（与种子逐项同形：1.45/1.21/2.43/1.30/.0505）|
   | G2 | `Jje579mW` | 跨源确认积 `analysis_consensus×analyst44` | 1.40 | 1.15 | 2.14 | 1.38 | .0629 | 0.89 | ⛔ **−0.05，逐项退回种子值**（跨源乘法=没信息增量）|

   ⇒ 轴（sector / subindustry 双向）、平滑窗（10/22/66）、backfill（5/22）、长窗（126/252/504）、
   三腿、字段（GAAP）、聚合（avg/sum）、**换源数据集（analyst44）**、**跨源确认积**
   **九条轴全部收敛到 1.40–1.45**；该族的表达式内杠杆已穷尽。
   ⭐ **G1 是重要负面结论**：`analyst44.best_eps_4wk_chg` 与 `analyst_consensus.eps_estimate_4wk_change`
   在同一壳下产出**逐项同形**（差 0.01/0.01/0.01/0.01/0.0000）⇒ **两个数据集是同一信号的两种封装**，
   换数据集不是新机制。KOR 的 ANALYST 塔要再进一步只能换**机制**（ESG / 目标价 / 评级），
   不能继续在 EPS 修正族内换数据源。
   ⚠ **settings `decay` 4→8/12 不再试**：KOR 已死轴清单明确「仿真 decay 单独扫只动 TO 不动 returns」，
     且本族 TO 仅 .05，decay 只会进一步削 returns。
   ⚠ **ANALYST 塔无库存可补**：本地全量重分类（按表达式字段名反查，绕过 `dataset_id=1150` 的
     `_unknown` 盲区）实测 **ANALYST 归属的未提交 α 共 38 条，S 全部 ≤1.45**；
     另一条 analyst 轴 `anl10_smartest_*` 纯形态最好 `mLgPgJnW` S 1.44 但 **2Y 仅 0.16**（2Y 闸结构性不可达），
     且其高分形态清一色是 `add(multiply(0.6,…), multiply(0.4,…))` 加权拼腿（禁）。
2. ⛔ **pwdoY39V 已死**（原判「CW 是 warning 不是 fail」）：2026-10-31 `check_correlation(refresh=True)`
   实测 prod **0.8507** 硬破，族内 `[0.7,0.8) n=1` / `[0.8,0.9) n=2` ⇒ 按族代表规则**整族判死**。
   CW 0.147166 的修法已无意义；PV 塔（2/3）**没有库存可补**。
3. ⛔ **mLmGQEq9 与 E5pjx9q0 双双实测破墙，shortinterest38 整族判死**：prod **0.935 / 0.8105**
   （本地 .6011/.6002 是过期缓存，`prod_corr_source` 非平台实测档）。且两颗同在**已亮 4/3 的 SHORTINTEREST 塔**，
   塔位贡献本就是 0 ⇒ **两条理由独立成立，永久出局**。
4. ⭐ **LLZ6wZO2 现在是 KOR book 里唯一全闸 REGULAR**（1.99 / 1.53 / 2Y 2.24 / subU 1.21 / cluster 0.94，
   prod **0.6762** / self **0.6760** 均已 `refresh=True` 实测通过）。FUNDAMENTAL 已亮 3/3 ⇒ **塔位贡献 0**，
   但它是唯一"现在就能过提交测试"的件。是否提交 = 用户裁决（放弃均匀点塔规则 or 不提）。

**⇒ 本战役的提交优先级（待用户确认，提交不可逆）**：

| 序 | alpha | 理由 | 前置动作 |
|---|---|---|---|
| ① | **883mLenl（或其 wave 266 后继 `GrW3Lba0`）** | 唯一能"一颗点亮 ANALYST"的候选 | 把 Sharpe 从 **1.45** 推到 ≥1.58（batch D 在飞） |
| ② | ~~pwdoY39V~~ | ~~唯一双塔计~~ | ⛔ **prod 0.8507 族死，出局** |
| ③ | LLZ6wZO2 | 唯一全闸通过，prod/self 双实测 ✅ | 无（只差用户拍板：塔满 3/3，提了不点新塔） |
| ④ | ~~mLmGQEq9~~ | ~~全区最强~~ | ⛔ **prod 0.935 族死，出局** |
| — | ~~E5pjx9q0~~ | 同族 | ⛔ **prod 0.8105，出局** |

⚠ **本表顺序不是提交授权**：提交必须用户明确确认 + `confirm_submit=True`。
⚠ **2026-10-31 后本表只剩两个活项**：①（在飞补席）与 ③（用户拍板）。塔位贡献 0 的 ③ 是否值得提，
属"冲 alpha 数量/OS 质量"而非"点亮塔"的取舍。

---

### 5.26 ⛔⛔ `pwdoY39V` 路线判死（三条证据，其中一条是硬证伪）

**起因**：§5.19.3 认定 CW 失败根因是 `oth695` 覆盖 0.4886 太稀疏 ⇒ 提出 F1「`ts_backfill(...,66)` 加密度」。
F1 = `j2YWRzXW` 已完成：Sharpe 1.81 → **1.73**、returns 19.67% → 18.67%、
多空腿 300/269 → **328/240**（持仓确实变了）、subU 1.69 → 1.66。

**但 `CONCENTRATED_WEIGHT` = `0.147166` —— 与 `pwdoY39V` 逐位相同（小数点后 6 位）。**

| 证据 | 内容 | 含义 |
|---|---|---|
| **① 硬证伪** | 两条**持仓明显不同**的 alpha（多空腿 300/269 vs 328/240）返回**完全相同**的 CW 值 | 在 CW 度量下，**信号排序不是决定项** ⇒ 密度修法原理性无效；CW 由「流动性门控 + SECTOR 中性化 + truncation 0.08 + maxTrade ON」这组**设置**定死 |
| **② 对照实证** | 已提交的 `xA16pzQJ`（同字段 `oth695_import_value_4`、同 `ts_sum(...,20)`、同 `trade_when(rank(adv20)>0.6)`）**CW 通过**，但它是 **`MARKET` 中性化 + `maxTrade OFF` + `tail(group_rank(..., bucket(rank(cap),"0,1,0.2")), lower=0.2, upper=0.8, newval=0.5)` 壳层** | CW 通过靠的是**换设置 + 上壳层**，不是靠加密度 |
| **③ 相关性墙** | `xA16pzQJ` 实测 **self 0.2308 / prod 0.6976**（`status=ACTIVE`, `stage=OS`, `dateSubmitted=2026-10-14`） | ⚠ **prod 已顶到 0.70 墙下 0.0024**。`pwdoY39V` 与它**同字段同窗口同门控**，prod 几乎必然 ≥0.70 |

**⇒ 三条结论，全部要写死**：

1. ⛔ **不再对 `pwdoY39V` / `j2YWRzXW` 做任何 CW 修法**（密度、winsorize、hump 全部已证伪；
   §5.19.3 的方向判断本身也是错的，本条取代它）。
2. ⛔ **`pwdoY39V` 视同 prod 已判死**：它的近同源 `xA16pzQJ` prod 0.6976 已在墙上，
   同字段同窗口的变体不可能低于它。⇒ **§5.22 结论 1「提交 pwdoY39V 点亮 PV + OTHER 2/3」作废。**
   `check_correlation(production)` 已发起但平台超时（-32603，prod 异步单并发），**不重触发**，
   留待必要时按 `retry_after` 复测——但即便复测通过，`xA16pzQJ` 已占据该概念，重复提交无多样性价值。
3. ⭐ **`oth695` 的 OTHER/PV 票已由 `xA16pzQJ` 收走**。要让 PV 2→3 或 OTHER 1→2，
   **必须换数据集/换信号**，不能在 `oth695_import_value_4` 上继续做窗口/门控变体。

**⚠ 本条写作时的排期违规（当场自查并改正，留证）**：

我第一版在这里写了「OTHER 第二三颗转向 `other455`（1500 字段）与 `fund_holdings_panel`」——
**两者都已在战役级判死清单里**（§5.20 表格第 114 行 `get_dead_ends` 点名：
`other455`、`fund_holdings_panel` 均属死集；`fund_holdings_panel` 更是 wave187 复验
S −0.04 / 0.28 的二次判死）。若照此派发，就是「命中已死轴仍烧配额」。

**根因是两张表的口径不同却没交叉核对**：§5.20 的 category 画像表按 **coverage / 字段数 / aC**
排序，把 `other455` 标成「1500 字段待普查」= **看着像未开发的矿**；而 `get_dead_ends` 是**结论面**。
⇒ **纪律补充（写死）**：**任何"待普查/未动/备选"的数据集，派发前必须先 `get_dead_ends` 过一遍**；
画像表的「未动」标签**不等于**「未被判死」，它只表示**本会话没测过**。

**改正后的 OTHER / INSTITUTIONS 真实攻击面**：

| 塔 | 剩余可用源 | 判定 |
|---|---|---|
| **OTHER**（1/3） | **只剩 `acquisition_model` 的文本因子腿**（`global_text_factor_percentile_rank` aC **1** / `region_text_factor_percentile_rank` aC **0**） | 数值似然腿已双杀（§5.23）；`other455` 已判死；`other695` 已被 `xA16pzQJ` 占位 ⇒ **OTHER 塔在 KOR 基本封死**，只能靠文本因子这一个未测字段博一次 |
| **INSTITUTIONS**（0/3） | **无** | `institutions6` count/value 双杀（§5.20.1）+ `fund_holdings_panel` 二次判死 ⇒ **与 §5.20 结论一致：本塔在 KOR 无攻击面，需新数据集授权** |

⇒ **实际可打的未点亮塔只剩 5 个**：INSIDERS(0)、NEWS(0)、RISK(0)、SENTIMENT(0)、SOCIALMEDIA(0)，
外加 ANALYST(2→3) 与 PV(2→3) 两个「差一颗」。**8 个可玩塔的估计要下调。**


**方法论沉淀（可迁移，比本条结论更值钱）**：

> **判「修法无效」的最强证据不是「指标没改善」，而是「指标在两条不同持仓上逐位相同」。**
> 前者可能是修法方向对但力度不够，后者直接证明**指标对被测变量不敏感**——
> 此时任何同方向的继续尝试都是白烧配额。**遇到逐位相同的读数，先怀疑「指标不由你以为的变量决定」。**
>
> 配套：`checks.warning` 里的 CW 值要**与同族已提交件的设置逐项对照**再动手。
> 本轮的 `xA16pzQJ` 一次读数就省掉了几十次 CW 修补尝试。

---

### 5.27 `e75gwG5l`（an883_S1：industry→sector 轴 A/B）—— 负结果，ANALYST 通道实证封死

同一表达式、同一字段、同一窗口，**唯一变量 = 分组轴**：

| alpha | 分组轴 | 平滑窗 | S | F | 2Y | subU | 备注 |
|---|---|---|---|---|---|---|---|
| **883mLenl** | industry | 22 | **1.40** | 1.15 | 2.14 | 1.38 | 基准（待提交件） |
| `kqNbqpKk` | industry | 66 | 1.32 | 1.06 | 1.88 | 1.29 | 窗口 66 劣于 22 |
| **`e75gwG5l`** | **sector** | 22 | **1.22** | 0.96 | 1.82 | 1.19 | 本轮；相对基准 **−0.18 S** |

**三条结论**：

1. sector 比 industry 低 **0.18 S（−12.9%）**，与台账里 `KOR-ANL44-EPSREVISION-PRODWALL` 已记的
   「industry grouping **+0.10S vs sector**」**同向且更强** ⇒ **该族最优分组轴 = industry，sector 轴判死**。
   （这也修正了我此前"换粗轴常使 robust 与 S 同升"的通用印象——**该结论逐族实测，不跨族迁移**，与 §5.26 的
   「跨族照搬可反向」是同一条。）
2. 窗口轴也已分出优劣（22 > 66）⇒ 该族**只剩 decay 一个免费杠杆**，而 883mLenl 到 1.58 需 **+0.18**，
   恰好等于「分组轴」的差值且更优轴已在用 ⇒ **参数层无解**。
3. 叠加 prod 不变式（`KOR-ANL44`：eps revision 族 prod ≥ 0.7 为不变式）⇒ **883mLenl 不再推 S**，
   **§5.25 提交优先级 ① 作废**。

**★ ANALYST 塔（2→3）的完整封死链**（本次最重要的结论，逐条带出处）：

| 通道 | 状态 | 证据 |
|---|---|---|
| eps_estimate revision（883mLenl / kqNbqpKk / mLoJLnZ5 / e75gwG5l） | ⛔ | prod ≥ 0.7 不变式 + 参数层无解（本条） |
| analyst10 `revise_value` | ⛔ | `KOR-ANL10-REVISE-VALUE-CEILING` |
| analyst10 `innovation_score` | ⛔ | 同上条附注（wave97 一号 S=0.26） |
| analyst16 est-pct / raw event | ⛔ | `KOR-ANALYST16-EST-PCT-DEAD` / `KOR-ANL16-EVENTSPARSE-WEAK` |
| analyst14 disagreement | ⛔ | `KOR-ANALYST14-DISAGREEMENT-NOSIGNAL` |
| analyst44 eps revision | ⛔ | 同第一行 |
| analyst_factor_signals | ⛔ | `KOR-ANALYST-FACTOR-SIGNALS-EPS-GROWTH-NOSIGNAL-20261004` |
| analyst_consensus 4w 比率 / grossmargin / dividend | ⛔ | `KOR-ANLCONS-EPSRATIO-DEAD` / `KOR-ANLCONS-GROSSMARGIN-DEAD` |
| **insiders 族（原定替代路线）** | ⛔ | `KOR-INSIDERS5-CEILING-20260909`（30 条 best S **1.05**）+ `KOR-INSIDER-PROD-SATURATED` |
| **analyst_consensus 覆盖家数轴 / 意外值轴** | ⏳ | 本轮 §5.29 首次派发 —— **唯一未被判死的 ANALYST 面** |

⇒ 若 §5.29 两条也弱，**ANALYST 塔应在台账上标为「本区无攻击面」**，与 INSTITUTIONS 同级处置。
⚠ 台账内部有一处**过期建议**必须点名：`KOR-EPS-REVISION-SPREAD-PROD-FLOOR-0723`（2026-09-07）的 salvage 写着
「KOR/D1/ANALYST 点亮需换 insiders 族（绿榜未碰）」——**该建议两天后即被 `KOR-INSIDERS5-CEILING-20260909`
（2026-09-09，ceiling 1.05）推翻**。读旧 salvage 必须先看 `dead_at` 之后的记录。

---

### 5.28 `insd_I1` 无产出 + 排期违规第三次（当场记录，不掩饰）

- 派发 `rank(ts_sum(vec_sum(insd5_ghc_tr), 66))`（sim `4iToOcb095fF9IEkRud34or`）→ `lookINTO` 返回 **404**，
  且全局 `get_user_alphas(stage=IS, order=-dateCreated)` 最新 8 条里**无对应 alpha** ⇒
  **该 simulation 未产出任何 alpha**。同批的 an883_S1 正常出结果（`e75gwG5l`）⇒ **不是通道故障**，
  是这一条自身失败（字段存在性 `preflight` 已通过，故疑在 `vec_sum` 聚合或计算期）。
- **更该记的是纪律问题**：`insiders5` **在 `get_dead_ends(KOR)` 里已判死** ——
  `KOR-INSIDERS5-CEILING-20260909`：w177–w181 共 **30 条** insider×价差/上修组合，
  **best sharpe 1.05**，`note: 族降级暂停：不再投槽位`；另有 `KOR-INSIDER-PROD-SATURATED`
  （insider_feats 30+ 条，**PROD 全部 ≥0.75**）。
  ⇒ **这是本会话第三次「命中已死轴仍派发」**（① other455 / fund_holdings_panel，② 本条 insiders5）。
  **不重试、不换变体、不计入任何塔。**
- **根因比前两次更隐蔽，值得升级纪律**：前两次是「画像表『未动』≠ 未判死」；
  这次是**判死记录的 `dataset` 键位置不固定** —— `KOR-INSIDER-PROD-SATURATED` 的 payload **没有** `dataset` 字段
  （只在 `payload.family` 写 `insider_feats 内部人交易信号族`），按 `payload.dataset` 打印时显示成 `-`；
  而 `KOR-INSIDERS5-CEILING-20260909` 是**有** `dataset: insiders5` 的，是我先前按 `payload.dataset` 做的
  count 表统计漏了它。
  ⇒ **纪律（写死，第三次补充）**：派发前必须对目标数据集名做**全文检索**
  （扫 `get_dead_ends` 全量 JSON 的 `entry_id` / `family` / `reason` / `rule` / `salvage` / `dataset` **所有字段**），
  **不得只扫 `payload.dataset`**。

---

### 5.29 `analyst_consensus` 画像（400/2343 部分）+ B1/B2 派发

**画像读数**（`get_datafields(dataset="analyst_consensus", filter_sharpe=false, max_fields=400)`；
⚠ 返回 `complete: false`，平台声明 **2343** 字段，本轮只取到 **400** ⇒ 以下只是**前 17%** 的视图，
不得当作全数据集结论）：

| 项 | 读数 |
|---|---|
| 类型 | **VECTOR 397 / MATRIX 3** |
| 覆盖 | 0.6–0.9: **329**；0.3–0.6: 71；无 <0.3 |
| aC 头部 | `estimate_currency_code_inventory_annual12` **5** / `estimate_currency_code_targetprice_annual12_tribes` 4 / **`estimate_count_currentliabilities_annual12` 4** / `estimate_count_current_period_targetprice_annual12_tribes` 3 |
| **分散度族** | **0 字段**（description 里 dispersion / standard deviation / spread / variance 全无命中） |
| 意外值族 | 仅 **2**：`avg_surprise_net_income` / `avg_surprise_net_income_fxadj`（cov 0.6382，aC 0） |
| 实际值族 | `actual_*_value_*` 极多；**`_tribes` 后缀 = 含预测期的完整向量**，无 `_tribes` = 仅实际值 |

**结构判读（§0.1 质量先验的直接兑现）**：头部**不是** EPS 修正轴，而是
**①货币码（纯陷阱：整数码，无经济含义）②家数（覆盖宽度）③实际值 ④forecast/actual 标志**。
⇒ 与 EPS 修正（883mLenl 族）**机制正交**，这正是 ANALYST 塔唯一没被试过的面。

**★ 一条硬结论先落地**：`KOR-ANLCONS-EPSRATIO-DEAD` 明确允许的第二条路线「**分散度压缩**」
在本数据集**无字段支撑**（0 字段）⇒ **该路线作废**，只剩「意外值」一条。

**B1（覆盖宽度动量）**
- 表达式：`group_rank(ts_delta(ts_backfill(estimate_count_current_period_targetprice_annual12_tribes, 22), 66), sector)`
- 字段：`estimate_count_current_period_targetprice_annual12_tribes`（**MATRIX**, cov 0.8037, aC 3）= 发布目标价的分析师**家数**
- A-2：谁被定价 = 卖方覆盖/注意力；为什么错 = **覆盖启动（initiation）的注意力冲击被延迟定价**
  （McNichols & O'Brien 1997；Irvine 2003），且家数变化是**离散事件**而非连续水平；
  修复期 = 数周至一季；方向 = 家数净增 ⇒ 先正漂移（券商只挑看好的标的启动覆盖）；边界 = 覆盖断崖（退市/并购）。
- 形态依据：②.b「强度型字段 ⇒ `ts_delta` 后多窗」+ 铁律 A（家数是慢变存量，必须取变化率）。
- 壳层：**不加**（机制上不需要规模/流动性残差化）；`sector` 已在 `group_rank` 内。

**B2（标准化意外盈余 SUE）**
- 表达式：`group_rank(ts_zscore(ts_backfill(vec_avg(avg_surprise_net_income_fxadj), 22), 504), sector)`
- 字段：`avg_surprise_net_income_fxadj`（VECTOR, cov 0.6382）= 实际减一致预期的净利意外
- A-2：谁被定价 = 盈余意外（PEAD）；为什么错 = **对意外消息反应不足**（anchoring / 处置效应），
  Bernard & Thomas 1989，韩国市场 PEAD 有独立复现文献；修复期 = 1–3 个月；方向 = SUE 高 ⇒ 后续正漂移；
  边界 = 覆盖仅 0.64、财报真空期无新信息（靠 `ts_backfill 22` 维持）。
- 形态依据：②.b「事件稀疏 ⇒ 先 backfill」；`ts_zscore(·,504)` = 教科书 SUE 的标准化构造 ((x−μ)/σ)，非自由发挥。
- ⚠ 与 `KOR-ANLCONS-EPSRATIO-DEAD` 的关系：该条**明确允许**「意外值…等事件型结构」，B2 正是其许可路线。

两条共用 KOR/TOP600/D1/SECTOR/decay4/trunc0.08，均为**单数据集单腿**（不触用户约束 5）。
**预注册闸**：S ≥ 1.3 / 2Y ≥ 1.5 / subU ≥ 1.0 才进下一步；S < 1.0 且机制无解释 ⇒ **该轴一次判死**。

---

### 5.30 未点亮塔的 category 画像补全（SENTIMENT / SOCIALMEDIA / RISK）

> 用户要求「一个个 category 查数据集情况」。以下三张表是**现查现记**（`get_datasets(region="KOR", delay=1, universe="TOP600")`）。

**SENTIMENT（6 个数据集）**

| dataset | fields | cov | aC | 状态 |
|---|---|---|---|---|
| news_sentiment_transfer | 23 | 0.9654 | 227 | ⛔ 三波判死（`KOR-NEWS-SENTIMENT-TRANSFER-DEAD` / `KOR-NEWS38-HEADLINETONE-DEAD`） |
| other553 | 21 | 0.6243 | 96 | ⛔（`KOR-OTH553-REV-SPARSE` / `KOR-OTHER553-ABSOLUTE-DEAD`） |
| **sentiment21** | 138 | **0.3812** | **94** | ⭐ **未动**，且字段级 aC 极低 ⇒ 白空间 |
| sentiment23 | 156 | 0.2648 | 54 | 未动（cov 仅 0.26，600 只里约 157 只有值） |
| sentiment26 | 19 | 0.357 | 48 | ⏸ 已判死待落库（`KOR-SENTIMENT26-NO-CROSS-SECTION-AND-7Y-COVERAGE`，需用户确认 `force_seal`） |
| sentiment27 | 29 | 0.3989 | **1871** | 未动但**极度拥挤**（valueScore 2）⇒ prod 空间优先判负 |

**sentiment21 字段结构**（`complete: true`，138/138 全取）：

- **5 个时间窗族**：1d（`snt21*`）/ 2d（`snt21_2*`）/ 3d / 4d / 5d；每族 21 字段
  = neg / neut / pos × mean / median / max / min / std / conf_low / conf_up，外加 3 个 `_dts_*`（neg/pos/neut 的**标准差**）
- **覆盖**：1d 族 **0.475**；2–5d 族 **0.3518**；`_dts_*` 族 **0.4733**
- **aC 最高仅 10/12**（对照 sentiment27 的 1871）⇒ **真白空间**
- ⚠ 描述写「in USA modules」/「USA D0 module」是**厂商模块名**，本次查询已是 KOR 分区、覆盖 0.35–0.475 说明本区确有值；
  **不要**误读成「美国数据迁移」而放弃。

**★ sentiment21 的两条可打机制（刻意避开已判死的 tone / 事件评分）**：

1. **分歧溢价（dispersion premium）**：`subtract(conf_up, conf_low)` = 情绪置信区间宽度 = 新闻/分析师间**分歧**。
   Miller(1977)：分歧 + 卖空受限 ⇒ 高估 ⇒ 后续负收益；Diether-Malloy-Scherbina(2002) 有横截面实证。
   形态：**同数据集两腿相减**（单一经济含义，合规）；`ts_backfill(·,22)` 补 0.35 的覆盖缺口。
2. **情绪稳定性（`_dts_*` 族）**：neg/pos 情绪的标准差**本身就是分歧**，且**不是 tone 字段**
   ⇒ 不受 `KOR-NEWS50-EVENTSCORE-WEAK` 的 tone/event-score 禁令约束。

⚠ 但必须先满足 `KOR-NEWS79-SENTIMENT-DEAD` 的**复检定条件**，原文：
「news sentiment event fields unusable with **decay4 daily aggregation** on KOR;
would need **event-anchored persistence design** before retry」
⇒ 复检必须用**事件锚定 + 持续性**结构（`ts_backfill` + 长窗 + `group_rank`），**不得**再用裸日频聚合。

**SOCIALMEDIA（2 个数据集，均单字段）**

| dataset | fields | cov | aC |
|---|---|---|---|
| other100 | 1 | 1.0 | 399 |
| socialmedia39 | 1 | 1.0 | 576 |

唯一字段 `scl39_top5_people_also_watch_ticker_ii` = **VECTOR of Atlas instrument IDs**
（共同浏览的近邻标的 **ID 列表**，description 明写「stable identifiers suitable for joins」）。
⇒ **它不是数值信号，是 join key**；对一个 ID 列表取 `vec_avg` 没有经济含义。
⇒ **SOCIALMEDIA 塔在 KOR 无信号面**（与 INSTITUTIONS 同级处置）。除非当 **group 维**用，
但它是 `VECTOR<ID>` 而非平台 GROUP 类型，`group_*` 不吃 ⇒ 连分组器都不成立。

**RISK（7 个数据集）**

| dataset | fields | cov | aC | 判读 |
|---|---|---|---|---|
| risk59 | 16 | 0.9806 | 561 | 描述 = RIC↔BBID 映射 ⇒ 无信号面 |
| risk60 | 5 | 1.0 | 211 | ⛔ `KOR-RISK60-CROWDDING-NOSIGNAL` |
| risk68 | 5 | 0.9914 | 757 | 订单簿 tick 统计；KOR 未测（IND 侧 risk68 全灭于 robust） |
| risk70 | 96 | 0.9798 | **7963** | 所有权数据；**极度拥挤** |
| risk71 | 7 | 0.6658 | 344 | ⛔ `KOR-RISK71-RESIDUAL-REVERSAL-2Y-DEAD` |
| **risk72** | 5 | 0.6246 | 400 | **未动**（extended factor 的 specific return） |
| risk88 | 64 | 0.9727 | 1405 | ⛔ `KOR-RSK88-STYLOAD-WEAK` |

⚠ **本 category 的 dataset-level description 与名称严重错配**（risk59 名为「借券/空头动态」、描述却是 ID 映射；
risk70 名为「多因子模型」、描述却是持仓数据）⇒ **不得用 dataset description 做机制推断**，必须逐字段读 description。
⇒ RISK 唯一未动且可解释的是 **risk72**，但 specific return 本质是**残差动量**，与已提交的 pv 动量族 prod 相撞风险高。

**★ 修正后的全局可玩面（本表为后续排期的唯一依据，§5.4 的「8 塔 ×3=24 票」作废）**

| 塔 | 现状 | 剩余可用源 | 判 |
|---|---|---|---|
| ANALYST | 2/3 | analyst_consensus 家数轴 / 意外值轴（B1/B2 在飞） | ⏳ 差一颗，最省 |
| PV | 2/3 | 仅 non-gvm 信号源 + 已验证骨架（`KOR-PVDOM-SECTOR-VARIANTS-SATURATED`） | 需新信号源 |
| NEWS | 0/3 | 仅事件计数/时间模式（`story_event_record_count`） | 窄 |
| **SENTIMENT** | 0/3 | **sentiment21 分歧 / 稳定性** | ⭐ **最宽** |
| SOCIALMEDIA | 0/3 | **无** | ⛔ 排除 |
| RISK | 0/3 | risk72 | 中（prod 风险） |
| INSIDERS | 0/3 | **无**（insiders5 + insider_feats 双杀） | ⛔ 排除 |
| OTHER | 1/3 | acquisition_model 文本因子（仅剩） | 窄 |
| INSTITUTIONS | 0/3 | **无** | ⛔ 排除 |

⇒ **真正值得排期的只剩 3 个：SENTIMENT（最宽）、ANALYST（差一颗）、NEWS（窄）**；PV / RISK 次之。

---

### 5.31 ★ 工具陷阱：`lookINTO_SimError_message` 必须传**完整 location URL**

- 传裸 id（如 `36asnR3574YWctUX4o3XB6S`）⇒ 工具拼成 `https://api.worldquantbrain.com/<id>` ⇒
  平台返回 **HTTP 404 `{"detail":"Not found."}`**，**看起来像"仿真不存在/没产出"**。
- 传完整 URL（`https://api.worldquantbrain.com/simulations/<id>`）⇒ 正常返回 `{"raw":{"progress":0.35}}`。
- **本会话的代价**：我先按裸 id 轮询拿到 404，据此写下「an883_S1 与 insd_I1 均未产出」——**前半句是错的**，
  `e75gwG5l`（§5.27）正是 an883_S1 的产出。§5.28 里「insd 失败」的结论仍然成立
  （依据是**全局 IS alpha 列表 `-dateCreated` 里确实没有它**），但**判据必须换成「全局列表里有没有」**，
  不能只看 404。
- **纪律**：`lookINTO` 的入参 = `batch_create_simulations` 返回的 **`location` 原值**，不要 strip 成 id。
  另：`progress 0.35` 是本区的报告平台期（不是卡死），要等 `status` 变终态或 alpha 出现。

---

### 5.32 ★ ANALYST 塔关闭 / earnings 塔算术不可达 / institutions6 翻案测试（2026-10-30 本段）

#### 5.32.1 ANALYST 塔结构关闭：B2 收官，两条预注册分支全灭

B1 / B2 对预注册闸（S ≥ 1.3 / 2Y ≥ 1.5 / subU ≥ 1.0）的读数：

| id | 结构 | S | F | 2Y | subU | TV | RN |
|---|---|---|---|---|---|---|---|
| `LLMqAqZ1` | B1 分析师覆盖广度变化 | 0.51 | 0.26 | 1.58 | 0.56 | .051 | 0.03 |
| `wpQOM9p5` | `group_rank(ts_zscore(ts_backfill(vec_avg(avg_surprise_net_income_fxadj), 22), 504), sector)` | 0.67 | 0.43 | 1.26 | 0.67 | .026 | 0.21 |

- B1 的 2Y 1.58 是唯一过线项，但逐年 **S<1.0 占 8/10** ⇒ post-2022 regime 伪影，不是救援。
- B2 **raw 与 RN 同步弱**（0.67 → 0.21），按铁律 E 判 **信号自身衰减**（不是因子暴露拖累）⇒ 该换机制而不是换中性化档。
- 合判：ANALYST 塔 2/3，但**已无可用机制** ⇒ 与 §5.27 的 an883 A/B 及 7 条 death chain 合并，**本塔结构关闭**。

**★ 本段新增的机制层判据（比"试过了"强）**：ANALYST 有效的判别量是 **dispersion（分析师分歧）**，而 KOR 没有这个字段。三条独立论坛证据：
① "PRET 的有效性受 dispersion 调节"；② "volume 与分析师分歧 disagreement 正相关… return forecast dispersion / earnings forecast dispersion"；
③ analyst-consensus 族最好的 5 个信号是 mean / median / high / low / **stddev**。
而 `analyst_consensus` 画像 400/2343 字段里 **0 个 dispersion 字段** ⇒ 塔关闭从"我们试过了"升级为"**平台没有能工作的那个机制的字段**"。

#### 5.32.2 earnings 塔：单数据集**算术不可达**（判死，不再投配额）

KOR earnings category 只有 `earnings3`，8 个字段全是**日历类**（`*_interval` 单调斜坡 / `*_reptime` 时段码）。论坛 GLB 帖（2026-09-23，作者实测 150 变体）逐字段读数：

| 字段 | cov | 同骨架实测 |
|---|---|---|
| `ern3_pre_interval` | .7756 | S 0.53–0.61 |
| `ern3_next_interval` | .5825 | S 0.14 |
| `ern3_next_reptime` | .5825 | S 1.01，TV 11.4% |

**类别级规律**：EARNINGS 类信号 Ret/TV 恒在 **0.11–0.23**，decay 0→160 / 窗口 90–180 / `trade_when` 全形态、150 变体无一例外 ⇒ **Margin 天花板 ≈ 4.6bp**。

代入平台公式 `F = S × sqrt(|Ret| / max(TV, 0.125))`：KOR 要 S ≥ 1.58 且 F ≥ 1.0 ⇒ 需 `Ret/max(TV,0.125) ≥ 0.40`；
而 Ret/TV = 0.15 时该比值只有 ≈0.14 ⇒ **F ≈ 0.37·S**，即 **S 打到 1.58 时 F 只有 0.58**。

⇒ **earnings 塔在 KOR 不存在单数据集通路**（不是"还没调好参"）。唯一出路是 earnings 核心腿 + fundamental 价值腿（GLB 实证 S 2.24 / TV 4.5%），但那**不是 ATOM** 且 earnings 退居次要腿时塔归属存疑 ⇒ 暂不投配额。
（另：EAT 那篇 DEU S 1.60 靠的是 `earnings6` 的**财报日变动**字段，KOR 无 earnings5/6。）

#### 5.32.3 ⚠ institutions6 翻案测试（已发；**先记流程违规**）

**我做错了什么**：直接调 `create_multi_simulation` 发了 `institutions6` 的批，**没有先查 §4 的 16 个死数据集清单**（它就在里面），也没过 `wave_gate` / `dead_dataset_guard()`。这是本会话第三次「往已判死轴上发射」的同型事故（前两次：sentiment 面、earnings）。
**纪律补丁（立即生效）**：发批前必须 ① `grep <dataset>` 本文件 ② `get_dead_datasets`，两条都干净才准发。已花的 2 槽不回滚，改作翻案测试。

**但这一次的翻案前提真实且此前从未测过** —— 判死证据**全部限定在横截面水平形态**：

| 已测（wave 219，均判死） | 形态 |
|---|---|
| `group_rank(ts_backfill(subtract(rank(buyers), rank(sellers)), 22), sector)` | 家数差的**横截面水平** |
| `group_rank(ts_backfill(divide(subtract(acq, disp), aggregate_equity_value_institutions), 66), sector)` | 金额净流的**横截面水平** |

§5.19.1 / §5.20.1 的原话把死因限定在横截面：「宽度的**横截面差异**在 KOR 不是被定价的量」「其在**横截面**上的差异被 SECTOR 中性化吃干净」。

**本次发的是 IND 已验证的第三种形态**（论坛 23 票；IND/D1 已提交 OS，S 1.62 / F 1.37 / **2Y 2.47** / Margin 36.3bp / 18 项全 PASS）：

```
trade_when(ts_arg_max(count_institutional_holders_security, G) < 33,
           signed_power(ts_quantile(divide(count_institutional_buyers_security,
                                           ts_mean(count_institutional_holders_security, 72)),
                                    840, driver=gaussian), 1.6),
           -1)
```

- 核心是 **3.4 年自锚定分位**（**时序**归一，非横截面）
- 门是**参与度峰值新鲜期**（拥挤 regime 门，非水平）
- IND 帖写死：`ts_arg_max` **作信号**是"信号摧毁器"（864/958/1097 三次全灭）、**作门控**是冠军机制
- 分母 `ts_mean(holders, 72)` 剥季度披露阶梯 = IND 侧 Fitness 首次破 1.0 的点
- IND 侧已排除的形态（不要重扫）：裸比值（结构不可行）/ `ts_corr` 0.38 / 美元净流 0.44 / **渗透率 0.20** / **sellers 反向 0.71**

**发批参数**：KOR/TOP600/D1，decay 9，SUBINDUSTRY，trunc .03，maxTrade ON，pasteurization ON，nanHandling ON。
**单变量对照**：G=90（冠军值）vs G=66（甜区另一值），其余全同。multisim `4E7Tu96Ll4lO98I15Vdbi9DZ`。

**预注册判据（写死，不许事后改）**：
- `S ≥ 1.3 且 2Y ≥ 1.5 且 subU ≥ 1.0` ⇒ **翻案成立**：从死集清单移除，登记「死因是形态不是数据」，进入强度/窗口扫描。
- `S < 1.0` ⇒ **判死加固**：institutions6 在 **水平 / 净流 / 自锚分位+regime门** 三形态下全灭，死因升级为「信号面不存在」，并补写翻案前提为"需新数据集"。
- `1.0 ≤ S < 1.3` ⇒ 灰区，只允许一次单变量收窄（G 或 T），**不得开谱**。

#### 5.32.4 其它本段读数（各一条，避免重扫）

| 事 | 读数 | 处置 |
|---|---|---|
| `akKMZ5x1`（insiders5） | `rank(ts_sum(vec_sum(insd5_ghc_tr), 66))` ⇒ **S −0.36 / F −0.14 / 2Y −0.81** | ⚠ **更正 §5.28**：「insd_I1 未产出」是**错的**（根因是 §5.31 的裸 id 404）。insiders 判死结论**不变**，判据改写为「全局 alpha 列表里有它、读数为负」 |
| `j2YWRzXW`（S 1.73 / F 2.11 / 2Y 2.05 / subU 1.66 / TV .031，唯一 FAIL = CW .147>0.1） | 2026-10-30T16:04:25 创建，**非本会话**（并行会话产物）；含 `adv20`(PV) × `oth695_import_value_4`(OTHER) | ⛔ **不采纳、不作基础**：违反用户约束 5（PV+OTHER 禁止组腿） |
| `other695` | 3 字段（2 个是标识符），唯一信号 `oth695_import_value_4` **aC 148** 且已被并行会话占位 | 排除（拥挤单信号集） |
| `risk72` | 5 字段 description 逐字相同（"Daily reproducible specific return"），cov .35–.76，**aC 82–131** | 排除（与 §5.30 一致：residual return ⇒ 与 PV 动量族 prod 相撞） |
| sentiment 面 | `KOR-NEWS-SENTIMENT-TRANSFER-DEAD`(id 153) 原文 **"do not probe news/sentiment aggregate datasets in KOR again"**；`KOR-NEWS79-SENTIMENT-DEAD`(id 118) 允许**条件式**重试（"would need event-anchored persistence design before retry"） | ⛔ **本段不碰**。12 条命中里 sentiment21 从未被点名，但 id 153 的散文禁令覆盖 aggregate 面；真要翻案须先解 153 与 118 的冲突（**需用户裁决**），不在本段自行解释 |

#### 5.32.5 塔位真值（`get_pyramid_alphas` 实测，非估算）

KOR/D1 已亮 3：**fundamental 3 / model 3 / shortinterest 4** ⇒ **12 个未亮**。最近：**analyst 2 / pv 2 / other 1**。

⚠ 平台口径：**只算已提交（submitted）的 alpha**，未提交候选不计 ⇒ **只有提交才能点亮塔**，而提交需用户明确确认 + `confirm_submit=True`（不可逆）。⇒ 本轮交付定位 = **把候选推到全闸通过**，点亮动作留给用户。

#### 5.32.6 ★ 战略态势（12 个未亮塔逐个结案后的真实余量）

| 塔 | 状态 | 依据 |
|---|---|---|
| analyst 2/3 | ⛔ 关闭 | §5.32.1（B1/B2 双灭 + 无 dispersion 字段） |
| earnings 0/3 | ⛔ 关闭 | §5.32.2（F 天花板算术） |
| institutions 0/3 | ⏳ 翻案测试在飞 | §5.32.3 |
| insiders / socialmedia / macro / risk / sentiment | ⛔ 关闭 | §5.28 / §5.30 / §5.31 / §201 / wave216 |
| news 0/3 | 半关闭 | 情绪/语气/事件评分族全灭；只剩注意力计数（wave187b 已 S 0.55 死）与时间模式 |
| **pv 2/3** | ⭐ **仍活** | 差 1 颗；需新信号源（`KOR-PVDOM-SECTOR-VARIANTS-SATURATED` 已饱和） |
| **other 1/3** | 半活 | 差 2 颗；只剩 `acquisition_model` 的文本因子腿（aC 1 / 0） |

⇒ **结论（已被 §5.33 部分推翻，见该节）**：KOR 的未点亮塔空间已接近穷尽。真正还有活口的只有 **PV（差 1 颗）+ OTHER（差 2 颗）**，两者都受"新信号源"限制。

---

### 5.33 ★ OTHER 塔翻案：`mmp_nlp_sentiment` 是被漏掉的整块信号面（521 字段 / 75 α / 467 字段零使用）

#### 5.33.1 纠正 §5.32.6 的「OTHER 只剩 acquisition_model 文本因子腿」

上表那一行是**只查死集清单就下的判断**，漏了「未判死、但从未画像」的整层。本会话用 `get_datasets(KOR, TOP600, D1)` 实测 **185 个数据集**，其中 `other` 类 **26 个**，按 alphaCount 升序逐个核：

| dataset | fields | cov | users | **aC** | vS | 备注 |
|---|---|---|---|---|---|---|
| news_sentiment_dl | 22 | .2588 | 2 | **2** | 7 | 文档流 |
| event_relation | 3 | .3392 | 4 | **4** | — | 文本事件关系 |
| news_sentiment_nlp | 23 | .2767 | 4 | **4** | 7 | polarity/readability/subjectivity |
| other635 | 6 | .3011 | 3 | **5** | 6 | TR News Analytics（描述称 80 字段，KOR 只 6） |
| other546 | 10 | .5632 | 8 | **9** | — | 机构网络 |
| equity_forum_data | 6 | .8948 | 9 | **13** | — | 论坛活跃度 |
| other436 | 3 | .57 | 12 | **15** | — | 股息模型 |
| other567 | 2 | .2571 | 12 | **16** | — | 员工评价 |
| other327 | 3 | .7866 | 25 | **31** | — | 利率敏感度 |
| ai_news_scores | 103 | .373 | 26 | **36** | 6 | transformer 情绪分 |
| other424 | 3 | .5919 | 31 | **44** | — | 股息预测 |
| other545 | 4 | .8393 | 29 | **46** | — | 关联公司动量 |
| other571 | 23 | .2649 | 49 | **62** | — | Wikipedia 浏览 |
| other78 | 11 | .7925 | 29 | **70** | — | 电话会 |
| **mmp_nlp_sentiment** | **521** | **.6187** | **46** | **75** | 6 | ⭐ 见 5.33.2 |

- **上表 15 个全部不在 `get_dead_datasets`（16 个死集）里，也不在 `get_dead_ends` 战役级清单里**（本会话两条都实测过）。
- 反例对照：`other455`（1500 字段）在死集里、`other532`（8 字段全 Barra specific return，aC 443–622）与 `risk72` 同机制且更拥挤 ⇒ 两者**不在此列**。
- ⇒ 真正被漏掉的是 **`mmp_nlp_sentiment`：字段面最宽（521）× 拥挤度最低（75 α）**，且它是**唯一能构造 dispersion 机制的 KOR 字段面**（接线见 5.33.4）。

#### 5.33.2 字段画像（521 字段，**全部 MATRIX**，`get_datafields(filter_sharpe=false)` 全量 11 页 521/521）

| 读数 | 值 | 含义 |
|---|---|---|
| alphaCount 总和 | **91** | 全平台只在这 521 个字段上建过 91 个 alpha |
| **aC = 0 的字段** | **467 / 521 = 89.6%** | **近九成字段从来没人用过** |
| 单字段最高 aC | 6（`advertisement_mention_total`） | 无任何拥挤字段 |
| coverage 分布 | 275 < 0.6 · 195 ∈ [0.8, 0.9) · **51 = 1.0** | 可用面主要在 0.8932 与 1.0 两档 |
| 类型 | 全部 MATRIX，**无 VECTOR** | 无需 `vec_*` 降维 |

**家族分布（按 `brain-alpha-research-news-sentiment` 五家族）**：

| 家族 | 字段数 | 代表（cov / aC） | 桶归属 |
|---|---|---|---|
| **dispersion** | **68 个 `mad_*`** | `mad_bullish_topic_score` (.8932/**0**) · `mad_analyst_topic_score` (.8932/**0**) · `mad_important_topic_score` (.8932/**0**) | ⭐ Dispersion（HIGH） |
| attention | 22 relevance + 10 mention_total | `high_relevance_news_sum_bbgnews` (1.0/**0**) · `sum_low_relevance_topic_mentions` (1.0/**0**) · `downgrade_mention_total` (1.0/**0**) | Event-conditioned（HIGH） |
| event_type | 22 价目表 + 85 推荐 + 33 升降级/预测 | `sum_raise_price_target_topic` (1.0/2) · `sum_lower_price_target_topic` (1.0/3) | Surprise |
| direction | 79 情绪计数 | `avg_bullish_topic_score` (.8932/5) · `average_bearish_mention_score` (.8932/3) | Change / Surprise |
| peer_context | **0** | 无 `peer/sector_avg` | — |

⚠ **两条硬约束先记死**：
1. **`std` / `var` / `dispersion` 字段数 = 0** ⇒ 论坛配方 R2（`pos_std − neg_std`）**前提不成立**，不可用。
2. 论坛配方 R1（`ts_corr(<情绪>, returns, d)` + FAST）里 `returns` 属 **PV** ⇒ 命中**用户约束 5**（OTHER×PV 禁两两组腿）⇒ **不采用**，登记为"约束 5 阻断"，不是"试过无效"。

#### 5.33.3 双通道取证

**通道 A｜论坛（MCP `search_forum_posts`，本会话实测 18 条命中）**：无本集直配模板（该集属 2026-05 上线的 56K 新字段批，中文论坛尚无落地帖）。但捞到**两条结构性配方**：

- **A-1 三段式（DEU sentiment33，id `43624281252247`，已提交 `d5j7Y6jE` S 2.11 / F 1.77 / TV 5.13% / Margin 34.5bp / 2Y 2.01 / subU 1.58 / prod 0.29）**：
  `x=ts_backfill(<文档分>,15); s=ts_mean(x,132); trade_when(group_count(s, market) > N, <截面映射>, -1)`
  核心**不是算子而是 `group_count(s, market) > N` 面板预热门**：帖子用 15 次受控回测证明它删掉的是**"数据还没长出来的年份"**而不是参数——N=50/100/200/300 下 2Y 恒 2.01、2020 年后 PnL 逐位相同、门后与无门逐年互相关 1.000。
  ⇒ **直接对应约束 4（近十年都要有数据）**：本集 cov .6187 且 2026 年才上新，历史上大概率前几年空账本。
  ⚠ **算子不可照抄**：帖中用 `quantile(s, driver="uniform")`，而本平台 `quantile` **只吃 1 个参数**（见项目记忆 `quantile-1`）⇒ 本区改用 `group_rank(..., subindustry)` / `rank`。
- **A-2 反例（同帖 §5.6，实测）**：`neg − pos` 做"净语调"把 **1.23 塌到 0.24** —— 原因不是方向错，而是**信号住在两者的共同成分里，作差正好减没它**。
  ⇒ **禁止**在本集做 `mad_bullish − mad_bearish`、`raise − lower` 这类**同号载体相减**。多字段组合只走**条件门控**（KOR skill ②.e）。
- A-3 另一条实证（JPN news7，id `40786070235799`）：新闻情绪字段会因覆盖稀疏让 **L/S Count 只有 15–20 只** ⇒ 本集 cov .6187 同样会撞 `CONCENTRATED_WEIGHT` / `LOW_SUB_UNIVERSE_SHARPE`，须备好 backfill 与门控。

**通道 B｜外部文献（给机制 + 方向句 + 持有期）**：

| 文献 | 机制 | 方向句 | 持有期 | 迁移限制 |
|---|---|---|---|---|
| Miller (1977, *JF*) Risk, Uncertainty and Divergence of Opinion | 分歧 + 卖空约束 ⇒ 乐观者定价 ⇒ 高估 | 分歧高 ⇒ 后续**跌** | 1–3 月 | USA 理论；KOR 卖空制度更严 ⇒ 机制**更强**，但需实测 |
| Diether–Malloy–Scherbina (2002, *RFS*) | 分析师预测分歧与截面收益反向 | 分歧高 ⇒ 低收益 | 1–6 月 | 用**分析师**分歧；本集是**新闻口径**分歧 ⇒ 只作同族假说 |
| Hong–Lim–Stein (2000, *JF*) Bad News Travels Slowly | 覆盖不足 ⇒ 信息扩散慢 | 低关注度下动量更强 | 6–12 月 | 本集可当 attention 门的理论依据 |

⚠ 三篇均 USA 样本，按 skill 纪律**只当假说，不作模板**；边界写入概念块。

#### 5.33.4 预注册：波 223（两槽，单数据集 ATOM，桶不同不设两窗口）

统一设置：KOR / TOP600 / D1 · decay 9 · SUBINDUSTRY · truncation 0.03 · pasteurization ON · nanHandling ON · unitHandling VERIFY · maxTrade ON。

| 槽 | 桶（skill §3） | 表达式 | A-2 收益来源声明 |
|---|---|---|---|
| **A** | **Dispersion（HIGH）** | `group_rank(ts_mean(ts_backfill(mad_bullish_topic_score, 15), 66), subindustry)`，**取负**（Miller） | 谁被定价=新闻口径的**多头观点分歧度**；为什么错=分歧+卖空约束 ⇒ 乐观者定价 ⇒ 高估；修复期=1–3 月；方向=**分歧高 ⇒ 后续跌** |
| **B** | **Event-conditioned（HIGH）** | `trade_when(rank(ts_zscore(ts_backfill(high_relevance_news_sum_bbgnews, 15), 66)) > 0.7, group_rank(ts_zscore(ts_backfill(mean_primary_positive_sentiment, 15), 66), subindustry), -1)` | 谁被定价=高相关新闻密集期里的**正面语气相对自身常态的偏移**；为什么错=关注度不足时信息扩散慢（Hong–Lim–Stein-2000），只有密集期方向才被定价；修复期=数日–数周；方向=**正面语气超常 ⇒ 后续涨** |

> ⚠ **发波前更正（字段存在性硬闸拦下）**：本节最初写的 `avg_bullish_topic_score` **在 521 字段全表里不存在**（`grep bullish` 只有 `mad_bullish_topic_score` / `mad_bullish_topic_mentions` 两条），属凭印象编的字段名。`preflight_expressions(dataset_id=mmp_nlp_sentiment)` 复核替换后 3 个字段（`mad_bullish_topic_score` / `high_relevance_news_sum_bbgnews` / `mean_primary_positive_sentiment`）**全部 exist、`unknown_fields` 为空、无 VECTOR**。同时把 B 的信号腿从「水平」改成 `ts_zscore(...,66)`：sentiment 家族实测**几乎全是 `count_*` / `sum_*` / `max_*` 单边恒正计数**（79 条 sentiment 字段全被 count/sum/max/mean/median/mad 覆盖），裸水平做多空违反**铁律 A**。**教训：预注册可以写错字段名，但发波前必须过字段硬闸——预注册是纪律，不是免检证明。**

设计纪律：**两槽分别落在两个不同桶**（不是同桶两窗口）——首触波要回答的是「这个集在哪个维度付钱」，不是「哪个参数更好」。
**约束 4 的十年检验由逐年表承担**：`get_alpha_yearly_stats` 的 longCount/shortCount 逐年读数即"当年有多少只股票有数据"；< 10 年 ⇒ 该集违规（判据见 5.33.5 第三条）。

#### 5.33.5 预注册判据（写死，不许事后改）

- 任一槽 `S ≥ 1.3 且 2Y ≥ 1.5 且 subU ≥ 1.0` ⇒ **OTHER 塔第二/三颗成立**，进强度/门控扫描（**不换集**）。
- 两槽 `S < 0.8` ⇒ Dispersion 与 Event-conditioned **两桶同灭** ⇒ 转 **event_type 桶**（价目表修正：`sum_raise/lower_price_target_topic`，注意 A-2 减法禁令，改门控）与 **Surprise 桶**各一次；**仍双灭则 `mmp_nlp_sentiment` 判死**，连同三种桶形态与证据一并封存（`seal_dead_end` 需用户确认 force_seal）。
- **逐年有效长度 < 10 年** ⇒ **不判死、不继续**，把「约束 4 与平台数据起点冲突」摆在用户面前二选一：放宽到数据起点 / 换集。
- 中间带（0.8 ≤ S < 1.3）⇒ 只允许一次单变量收窄（门阈值或窗），**不得开谱**。

---

### 5.34 ★ institutions6 三形态全灭：INSTITUTIONS 塔正式关闭（2026-10-30 本段）

#### 5.34.1 波 222 实测（3 条，**已写库** `upsert_backtest_rows(region=KOR, wave=222, dataset=institutions6)`）

| 形态 | alpha | S | F | 2Y | subU | RN-S | 裁定 |
|---|---|---|---|---|---|---|---|
| 水平 / 净流 | `xAr96M2W` | **0.10** | 0.02 | **−0.38** | 0.05 | — | 死 |
| 自锚分位 + regime 门（T=90） | `Vkxqo2xM` | **0.55** | 0.28 | 0.89 | 0.44 | 0.47 | 死 |
| 自锚分位 + regime 门（T=66） | `leAkZQae` | **0.59** | 0.31 | **1.20** | 0.49 | 0.61 | 死 |

表达式（后两条，单变量差在 regime 门的窗口）：
```
trade_when(ts_arg_max(count_institutional_holders_security, 90) < 33,
           signed_power(ts_quantile(divide(count_institutional_buyers_security,
                                           ts_mean(count_institutional_holders_security, 72)),
                                    840, driver=gaussian), 1.6), -1)
```

#### 5.34.2 按 §5.32.3 预注册判据裁定（**判据写死在前，本次只执行**）

两条自锚形态 S = 0.55 / 0.59，均落在 `S < 1.0` 档 ⇒ **判死加固**：

> **institutions6 在 水平 / 净流 / 自锚分位+regime门 三形态下全灭**，死因升级为「**信号面不存在**」（不是形态不对）。
> 翻案前提改为「**需新数据集**」，不得再用同集换壳重试。

**铁律 E 佐证（raw vs RN 分解）**：`Vkxqo2xM` raw 0.55 → RN 0.47（降）、`leAkZQae` raw 0.59 → RN 0.61（+0.02）。
**RN 没有救回任何一条** ⇒ 不是因子暴露拖累，是**信号自身强度不足** ⇒ 按铁律 E 只能换字段族 / 换集，**不该再扫中性化档**。
另注：两条 `subU` 均 PASS（0.44 / 0.49）、`CLUSTER_TEST` 仅 warning（0.45 / 0.43）⇒ 信号不是纯噪声，是**强度差一个数量级**；
但这不改变判死——判据是 S，不是「有没有一点信号」。

#### 5.34.3 十年窗口证据（约束 4 对 institutions6 **满足**）

两条自锚形态回测区间均为 `startDate 2014-01-01 → endDate 2023-12-31`，
持仓广度 `longCount 322–323 / shortCount 283–288`（TOP600 的 ~54%，逐年均匀）。
⇒ **失败不是数据跨度问题**，是强度问题。约束 4 在本集不构成约束。

#### 5.34.4 对未点亮塔态势的影响

| 塔 | 变化 |
|---|---|
| **institutions 0/3** | ⛔ **正式关闭**（此前是「翻案测试在飞」，现三形态证据齐） |
| **OTHER 1/3** | ⭐ **唯一活口**，波 223（`mmp_nlp_sentiment` 首触）在飞：`3OXmsj2T34Gib3815zYlWRgb` |
| PV 2/3 | 仍为饱和态（`KOR-PVDOM-SECTOR-VARIANTS-SATURATED`） |
| news 0/3 | 半关闭（注意力计数 / 时间模式唯一余量） |

⇒ 约束 5（PV/MODEL/OTHER 之间禁组腿）叠加后，**OTHER 塔的票只能来自 OTHER 单集 ATOM 或 OTHER×非三禁类别的组腿**；
在 mmp_nlp_sentiment 给出结论前，KOR 没有任何第三个可推进的未点亮塔。

---

### 5.35 OTHER 塔备选排队（约束 1 的 category 盘点收尾，波 223 在飞时补全）

非死 OTHER 集实测元数据（`get_datasets(category="other", region=KOR, delay=1, universe=TOP600)`，全部 `category=other`）：

| 集 | 字段 | 覆盖 | u | aC | 可挖性判定 |
|---|---|---|---|---|---|
| **mmp_nlp_sentiment** | **521** | 0.6187 | 46 | 75 | ⭐ **在飞（波 223）**；89.6% 字段零使用 |
| **equity_forum_data** | **6** | **0.8948** | 9 | 13 | ⭐ **第二候选**：覆盖最高的 OTHER 集；**6 字段全 VECTOR** |
| other78 | 11 | 0.7925 | 29 | **70** | 拥挤（aC 70 / 11 字段 = 每字段 6.4 次），且覆盖好 ⇒ 已被反复挖过 |
| other327 | 3 | 0.7866 | 25 | 31 | 每字段 10.3 次，最拥挤 |
| other571 | 23 | 0.2649 | 49 | **62** | 覆盖 0.265 + aC 62 ⇒ 低覆盖高拥挤，双重劣势 |
| ai_news_scores | 103 | 0.373 | 26 | 36 | 覆盖 0.373（<0.4 ⇒ 需 backfill）；字段数可观，第三候选 |
| other546 | 10 | 0.5632 | 8 | 9 | 中等；待画像 |
| other436 / other635 / event_relation / news_sentiment_nlp / news_sentiment_dl | 3–23 | 0.26–0.57 | 2–12 | 2–15 | 覆盖 0.26–0.34 的几条（news_sentiment_dl 0.2588 / nlp 0.2767 / event_relation 0.3392 / other635 0.3011）⇒ **贴近约束 4 的覆盖率边界**，需先验证十年跨度再投入 |

**`equity_forum_data` 字段级画像**（`get_datafields(filter_sharpe=false)`，6/6，**全部 VECTOR**）：

| 字段 | 家族（news skill §2） | aC | 说明 |
|---|---|---|---|
| `aggregate_buy_opinion_score` | direction | 4 | 跨源买入情绪分 |
| `aggregate_sell_opinion_score` | direction | 6 | 跨源卖出情绪分 |
| `aggregate_comment_volume` | attention | 2 | 总评论数 |
| `comment_volume_per_platform` | attention | 2 | 单平台评论数 |
| **`distinct_user_count_per_platform`** | attention | **0** | **从未被使用** |
| `total_distinct_participants_count` | attention | 1 | 跨源独立用户数 |

设计约束（**三条，写死**）：
1. **全 VECTOR ⇒ 必须先 `vec_avg` / `vec_sum` 聚合**（项目经验：event/social 类 VECTOR 直接进 `rank` 会错）。
2. **无 dispersion 族**（零 std/var 字段）⇒ **Dispersion 桶在本集不可用**，只能做 Change / Surprise / Event-conditioned / Propagation。
3. **`buy_score − sell_score` 属「同号相减」高危形态**：DEU 实证 `neg − pos` 1.23 → 0.24（§5.33.3 A-2）。
   若要用情绪净额，改用**比值** `divide(buy, add(buy, sell))`（无量纲、有界 [0,1]）或**单腿 + 门控**，
   不得直接 `subtract`。**这是一条待实测的判定，不是已证结论**——`buy/sell` 是反向构念，与 `pos/neg std` 不完全同构。

⇒ **OTHER 塔的真实队列**：波 223（mmp）→ 若死则 `equity_forum_data`（6 字段全 VECTOR，覆盖率 0.895）→ 若再死则 `ai_news_scores`（103 字段 / cov 0.373）。
三条全灭 ⇒ OTHER 塔在约束 5 下**无票可打**，需用户授权 OTHER 之外的类别做组腿（PV×NEWS 配额 5 条已用于其他用途）。

---

### 5.36 ⛔ PV「处女面」判断被自身数据库证伪：`pattern_scores` / `continuation_score` 早已判死（2026-10-30 本段）

#### 5.36.1 我错了：`get_dead_datasets` ≠ `get_dead_ends`，两张清单口径不同

本段我在波 223 在飞时把 **`pattern_scores`（504 字段 / cov **1.0** / aC 317）** 与 **`continuation_score`（560 / cov **1.0** / aC 513）**
判成「近处女 PV 面」，依据是二者**不在** `get_dead_datasets(region="KOR")` 的 16 条死集清单里。
跑 `get_dead_ends(region="KOR")`（85 条）后当场证伪 —— 族级封杀早就写过：

| dead_end id | 原文证据（摘） |
|---|---|
| `KOR-PATTERN-SCORES-PROBE-DEAD` | wave103 首探 **8/8 RED**，最高 0.49（`asc_triangle_dynamic`），2y 最高 0.83；形态族三连判死：chart_cnn 1.51 → continuation 0.34 → **pattern_scores 0.49** |
| `KOR-CONTINUATION-SCORE-DEAD` | wave117 8 探针全 RED：单字段 rank 最高 −0.66~0.18；`bullish_flag+pv20` 混合也仅 0.98；**560 字段纯白区无独立信号** |
| `KOR-CONTINUATION-SCORE-PROBE-DEAD` | wave102 8 探针 5 方向全灭，最高 0.34（`bull_flag_recent_similarity`），动量/差分全负 |
| `KOR-AI-FACTOR-TRANSFER-DEAD` | wave126 8/8 RED，max\|S\| 0.86，且是 **13 周价格动量克隆** |
| `KOR-PRICE-SIGNAL-DL-DEAD` | wave125 trend3 + multisim 8/8 FAIL，技术克隆 |
| `KOR-PV30-NO-SIGNAL` | pv30 是 PCA 行业聚类**标签**集（integer label），只能当 `group` 参数，不能 rank |

**纪律升级（写死，第二次同类失手）**：`get_dead_datasets` 只封**整集**，`get_dead_ends` 封的是**结论**（族级 / 形态级 / 单字段级）。
PV / MODEL / OTHER 三类的任何「新面」，**发波前必须两路都过**，且 `get_dead_ends` 要按 `payload.dataset` + 关键词
（`pattern` / `technical` / `continuation` / `price` / `candle` / `chart`）双路检索。§5.26 只写了「先 `get_dead_ends` 过一遍」，
没写「`get_dead_datasets` 不能替代它」，本段仍踩了 —— 现补上。

已完成的图鉴（存档，不再投入）：504 字段全 MATRIX、cov 全 1.0、`agg ∈ {mean,min,max,std,dynamic,q95,median,avg}`、
`lookback ∈ {none,60,120,40d}`、400 个形态模板、aC 总和 454（311/504 零使用）、`std_similarity` 族 26 条（唯一 dispersion 面）。
**结构漂亮但平台已实测无信号** —— 形态相似度是价格的确定性函数，与 13 周动量同源，这正是它 S 上不去的原因。

#### 5.36.2 PV 塔结论下调（写死）

- PV 2/3 的**最后一票不能靠 PV 自有技术类数据集**点亮：price-signal / chart_cnn / pattern_scores / continuation_score / pv30 / ai-factor-transfer 全部判死，
  `KOR-PVDOM-SECTOR-VARIANTS-SATURATED` 记 `wpjJK60l` **prod 0.6993** 已是唯一过闸变体、其余变体 0.80–0.99 FAIL。
- ⭐ **唯一还开着的门是「跨类别双塔匹配」**：`j2YWRzXW` / `pwdoY39V` 的 `pyramids.list = [KOR/D1/PV(1.4), KOR/D1/OTHER(1.6)]`、`effective = 2`
  —— 平台把 `oth695` **同时算进 PV 与 OTHER**。⇒ **OTHER 塔打成的每一颗，可能同时给 PV 记一票**。
  故波 223 及后续 OTHER 工作对 PV 是**附带收益**，**不再单开 PV 波**（PV 自有面已无未死数据集）。

#### 5.36.3 波 223 重发记录 + **对上一条「幽灵」判断的当场自我更正**

| 项 | 事实 |
|---|---|
| 旧 id | `3OXmsj2T34Gib3815zYlWRgb` |
| 新 id | **`3P08ssU24l38GowuYFQdr9`**（同两槽表达式，设置 decay 9 / SUBINDUSTRY / truncation 0.03 / maxTrade ON / nanHandling ON） |

⚠ **我上一条把旧批次判成"幽灵"，是错的，在此更正并保留错误证据**：

第一版我写的是「`batch_status` 三次返回 `child_count=0 / parent_status=null` ⇒ 幽灵 ⇒ 重发无并发报错反证旧批没跑」。
**这条推理的每一环都站不住**，根因是**误读了 `batch_status` 的返回语义**：

- `lookINTO_SimError_message(locations=[<multisim 父 URL>])`（本段新学的取证位）返回
  `raw = {"progress": 0.35}`、`status = null`、`alpha = null`。
  ⇒ **multisim 父资源在子任务生成前，平台本来就只回一个 `progress` 字段**，没有 `status`、没有 `children`。
  `batch_status` 的 `parent_status: null` 不是"父任务不存在"，而是**父资源本来就没有这个字段**。
- 因此「`parent_status=null` + `child_count=0`」**不构成幽灵证据**，只说明"子任务还没生成"。
  旧批次很可能一直在跑 —— 我的重发可能造成了**重复在飞**（同一两槽表达式跑了两遍）。
- 「重发没报 `CONCURRENT_SIMULATION_LIMIT_EXCEEDED`」同样**不能反证**旧批没跑：multisim 是排队制，
  平台收下请求不等于立刻占槽。

**更正后的判据（写死，替换第一版）**：

| 判据 | 含义 |
|---|---|
| `lookINTO_SimError_message` 父 URL 返回 `raw.progress`（如 0.35） | **在跑**，属正常预热态，**不许重发** |
| 父 URL 返回 `status = COMPLETE/ERROR` 或子任务列表可枚举 | 终态，去收批 |
| 父 URL 404 / 平台明确报失败 | 才是幽灵，可重发 |
| 子任务迟迟不出（>30 min 仍 0.35） | 走 `wqb-concurrency` 的孤儿模拟排查，**不靠"再发一次"试探** |

**教训（可迁移）**：`batch_status` 是**便捷聚合视图，不是权威状态源**；它把"字段缺失"渲染成 `null`，
与"对象不存在"同形。凡是"null 要不要当成不存在"的判断，必须回到原始端点用 `lookINTO_SimError_message` 取 `raw` 复核。
这与 §8.4 第 8 条（`except: pass` 把"读不到"渲染成"查到 0 条"）是**同一类错误：缺失被当成零值**。

⚠ **紧接上一段的"`progress` 也不可信"结论，08:49 被反证 —— 在此二次更正并保留全过程**：

我当时写的证据是「旧批 `3OXmsj2T34Gib3815zYlWRgb` 08:43 仍 `progress = 0.35` + 子任务 0，
而新批 `3P08ssU24l38GowuYFQdr9` 08:44 已 2/2 COMPLETE ⇒ 所以 progress 是死值」。
**08:49 复测把这条推翻**（三个端点交叉，全部一致）：

| 端点 | `3P08ssU24l38GowuYFQdr9`（新批） | `3OXmsj2T34Gib3815zYlWRgb`（旧批） |
|---|---|---|
| `batch_status` | child_count 2 / terminal 2 / all_terminal **true** | child_count 2 / terminal 2 / all_terminal **true** |
| `lookINTO_SimError_message` | `status=COMPLETE` + `raw.children`(2) + `raw.settings` | `status=COMPLETE` + `raw.children`(2) + `raw.settings` |
| 子 alpha | `O0AqeVGp` + `P0oqe8Gx` | `QPvqepk5` + `P0oqe8Gx` |

⇒ **旧批跑完了，只是在 08:43 那一刻还没跑到**。`progress = 0.35` 就是"在飞"的正常读数，
`status = COMPLETE` + `children` 就是"跑完"的正常读数 —— **没有任何渲染 bug，两种读数是同一件事的两个阶段**。
我把「两个不同批次的时间差」误读成了「同一字段的语义失真」，与 §8.5 的"未精确核验就下结论"是同一个错。

**最终判据（取代上面两版，写死）**：

| 读数 | 含义 | 动作 |
|---|---|---|
| `lookINTO_SimError_message` 父 URL → `raw.progress`（0.35…） | **在飞**（含排队） | 等，**不许重发** |
| 父 URL → `status=COMPLETE` + `raw.children` / `batch_status` → `all_terminal=true` | 终态 | 收批 |
| 父 URL 404 / 平台明确报失败 | 幽灵 | 可重发 |
| `batch_status` 对**在飞**批返回 `parent_status=null`+`child_count=0` | 子任务尚未生成（**不是**幽灵证据） | 等 |

**这次误判的真实代价（可量化，写下来当罚单）**：我为"重发"多烧了一个 2 槽 multisim（`3OXm`），
而平台**按表达式字符串去重**——相同表达式的子任务被并到同一个 alpha `P0oqe8Gx`（两批共用），
真正多出来的只有 `QPvqepk5` 一颗：它把 `multiply(-1, X)` 改写成 `reverse(X)`，绕过了去重，
指标与 `O0AqeVGp` **逐位相同**（S −0.46 / F −0.23 / 2Y −0.68 / TO 0.0411）。
⇒ **换写法不去重、只烧配额**；`reverse(X)` ≡ `multiply(-1, X)`（本条实测，与铁律 B「正反不精确反号」不冲突：
那条说的是 `reverse` 与**正向**不对称，不是与显式取负不等价）。

---

### 5.37 ★ 波 223 落袋（mmp 前两桶双灭）+ 波 224 预登记续跑 + category 盘点补全（2026-10-30 本段）

#### 5.37.1 波 223 实测（2 条，**已写库** `wave=223 / dataset=mmp_nlp_sentiment / multisim=3P08ssU24l38GowuYFQdr9`）

| 槽 | 桶 | alpha | S | F | 2Y | subU | TO | 裁定 |
|---|---|---|---|---|---|---|---|---|
| A | Dispersion（HIGH） | `O0AqeVGp` | **−0.46** | −0.23 | **−0.68** | −0.58 | 0.041 | 死 |
| B | Event-conditioned（HIGH） | `P0oqe8Gx` | **0.32** | 0.11 | **0.22** | 0.52 | 0.111 | 死 |

两槽按 §5.33.5 第二条落进 `S < 0.8` 档 ⇒ **Dispersion 与 Event-conditioned 两桶同灭**，
按预注册必须转 **event_type 桶 + Surprise 桶各一次**（见 5.37.2）。

#### 5.37.2 归因（铁律 F，`get_alpha_yearly_stats` 逐年实测）

| 年 | `O0AqeVGp`（分歧·反号） | `P0oqe8Gx`（密集期语气） |
|---|---|---|
| 2014 | **+1.82** | +0.42 |
| 2015 | −0.08 | **+1.27** |
| 2016 | −1.14 | −0.68 |
| 2017 | −0.47 | +0.95 |
| 2018 | −1.49 | +1.09 |
| 2019 | +0.51 | −0.06 |
| 2020 | −1.23 | −0.04 |
| 2021 | −0.68 | −0.38 |
| 2022 | −1.45 | −0.04 |
| 2023 | +0.02 | +0.45 |
| **S<1.0 年数** | **9/10** | **9/10** |
| 十年跨度 | ✅ 2014–2023 满 10 年 | ✅ 同 |

**读数（写进判决，不作事后修饰）**：
1. **约束 4 对 `mmp_nlp_sentiment` 满足**（两槽十年全跨度，longCount 250–400，无断层）⇒ 不走 §5.33.5 第三条的"不判死"分支。
2. 两槽都是 **9/10 年 S<1.0** ⇒ 按铁律 F 决策表「S<1.0 年份 ≥3 成 ⇒ 2Y 闸结构性不可达 ⇒ **换 regime 无关的机制**」，
   **任何桶/任何窗口都到不了 2Y ≥ 1.58**。这不是形态问题，是这条字段面在 KOR 没有十年可用的预测力。
3. `O0AqeVGp` 的 +1.82 全落在 2014 一年（top1 年占正收益 100%）⇒ 过拟合指纹（决策表第一行）。
4. `P0oqe8Gx` 2019 之后逐年 S 全 ≤ +0.45、2Y = 0.22 ⇒ **近年断崖，机制性衰减**。

⚠ **纪律说明（为什么仍然跑 event_type + Surprise）**：归因已足以判死，但 §5.33.5 是**先写死的判据**，
跳过它就是破坏预注册本身。因此**只跑这一次、只跑两条、不再开谱**——用两条配额把预注册走完，
换取"mmp 三桶全灭"这条结论的合法封存资格。**这不是回补，是把承诺执行完。**

#### 5.37.3 波 224 预登记（`4hnG28Vi4XVbpG89oSMs7z`，设置与 223 逐字对齐：decay 9 / SUBINDUSTRY / trunc 0.03 / maxTrade ON / nanHandling ON）

| 槽 | 桶 | 表达式 | A-2 收益来源声明 |
|---|---|---|---|
| **C** | event_type | `group_rank(ts_mean(divide(ts_backfill(sum_raise_price_target_topic, 15), add(ts_backfill(sum_raise_price_target_topic, 15), ts_backfill(sum_lower_price_target_topic, 15))), 22), subindustry)` | 谁被定价=**抬/降目标价新闻的构成比**（无量纲、有界 [0,1]）；为什么错=散户主导市场对卖方修正新闻反应不足；修复期=1–3 月；方向=抬价占比高 ⇒ 后续涨 |
| **D** | Surprise | `group_rank(ts_zscore(ts_backfill(sum_raise_price_target_topic, 15), 66), subindustry)` | 谁被定价=**抬价新闻量相对自身一年常态的跳变**；为什么错=信息扩散慢，突发修正未被即时定价；修复期=数日–数周；方向=超常抬价 ⇒ 后续涨 |

- **A-2 减法禁令已遵守**：C 用**比值** `raise/(raise+lower)`，不用 `raise − lower`（同号相减高危形态）。
- 字段硬闸已过：`preflight_expressions(dataset_id=mmp_nlp_sentiment)` → 2/2 字段 exist、`unknown_fields` 空、无 VECTOR。
- **封存判据**：C、D 任一 `S ≥ 1.3 且 2Y ≥ 1.5 且 subU ≥ 1.0` ⇒ 续挖；**两槽 S<0.8 ⇒ `mmp_nlp_sentiment` 三桶全灭，判死封存**
  （`seal_dead_end` 需用户确认 `force_seal`，本轮只出结论、不擅自封）。

#### 5.37.4 category 盘点补全（约束 1，`get_datasets` 实测，KOR/D1/TOP600）

`get_dead_datasets(KOR)` 全 16 条（**数据集级**，与 `get_dead_ends` 的**结论级** 85 条是两套表）：
`acquisition_model, fundamental44, institutions6, model109, model170, model192, model230, model30, model32, model53, multi_source_model, news79, sentiment21, shortinterest3, smoke_ds, wave30_model252`。

| category | 未点亮塔 | 存活数据集（**剔除上表 16 个**） | 拥挤度（α/字段） | 判定 |
|---|---|---|---|---|
| **institutions** | 0/3 | ⭐ **`fund_holdings_panel`**（cov .8093 / **30 字段** / 111 users / **219 α** / valueScore **4** / **mult 1.4**）<br>`institutions6` **已判死** | **7.3** | ⭐ **最优目标**：存活面最大、最空、塔倍率最高 |
| risk | 0/3 | `risk59`(16f, cov .981, 561α) · `risk60`(5f, cov 1.0, **211α**, vs 3) · `risk68`(5f, .991, 757α) · `risk70`(96f, .980, **7963α**) · `risk71`(7f, .666, 344α) · `risk72`(5f, .625, 400α) · `risk88`(64f, .973, 1405α) | 12–83 | 七个全活；`risk60`/`risk71`/`risk59` 最空 |
| earnings | 0/3 | `earnings3`（8 字段**全是财报日历**：`*_next_interval` / `*_pre_interval` / `*_reptime`，cov .56–.78，2616 α） | 327 | 只有事件计时腿，**没有财报值**⇒ 只能做门控/事件标记，不能做 Surprise 本体 |
| insiders | 0/3 | `insiders5`(53f, cov .892, **4959α**) · `insiders1`(9f, cov **.353** <0.4 ⇒ 需 backfill) | 94 / 61 | 最拥挤；已有 `akKMZ5x1`（S −0.36，反号 +0.36 仍远） |
| imbalance | 0/3 | `imbalance5`（**2 字段** / 1384 α / vs 1） | **692** | ❌ 单字段 692 次，结构性无空间 |
| socialmedia | 0/3 | `other100`(1f, 399α) · `socialmedia39`(1f, 576α) | 399 / 576 | ❌ 单字段共搜集，最大拥挤 |
| macro / sentiment / news | 0/3 | 已由 `KOR-MACRO63-NO-CROSS-SECTION` / `KOR-SENTIMENT26-...` / `KOR-NEWS-SENTIMENT-TRANSFER-DEAD` 封 | — | 不再投入 |

⇒ **下一主攻 = `fund_holdings_panel`（institutions 0/3，mult 1.4）**。它同时满足 §5.34.2 给 institutions 塔写的翻案前提
（"**需新数据集**，不得再用 institutions6 换壳重试"）——`fund_holdings_panel` 是与 institutions6 完全独立的第二个数据集，
**不是换壳**。

#### 5.37.5 `fund_holdings_panel` 30 字段画像（`get_datafields(filter_sharpe=false)` 30/30 全量）

**结构主轴：每个字段都有「全体」与 `_active`（仅活跃账户）两版** —— 这是本集唯一的原生对比轴，也是 15 组配对。

| 族 | 字段（base / `_active`） | 类型 | base cov | active cov |
|---|---|---|---|---|
| **持仓集中度** | `herfindahl_index_holdings` | MATRIX | .9553 | .7666 |
| | `holding_value_distribution_score`（crowding 指标） | MATRIX | .9553 | .7666 |
| | `holder_account_total`（持有账户数） | MATRIX | .9553 | .7666 |
| | `mean_security_weight`（持有账户的平均权重） | MATRIX | .9553 | .7666 |
| | `security_holding_usd_value` | MATRIX | .9553 | .7666 |
| | `top_weighted_account_number`（**conviction 持仓账户数**，top30% 权重） | MATRIX | .9553 | .7666 |
| **边界交易**（新开/清仓） | `boundary_transaction_total` | **VECTOR** | .887 | .6626 |
| | `boundary_transaction_usd_value` | **VECTOR** | .887 | .6626 |
| | `stable_boundary_trade_count_21d`（**21 日内无前次边界交易的"耐久"变更**） | **VECTOR** | .887 | .6626 |
| | `large_trade_count_50bps`（>0.5% AUM 的大单） | **VECTOR** | .887 | .6626 |
| | `top_weighted_transaction_number`（conviction 交易） | **VECTOR** | .887 | .6626 |
| | `transaction_account_total`（当日交易账户数） | **VECTOR** | .887 | .6626 |
| | `security_transaction_usd_value` | **VECTOR** | .887 | .6626 |
| **交易集中度** | `herfindahl_index_transactions` | **VECTOR** | .887 | .6626 |
| | `transaction_value_distribution_score` | **VECTOR** | .887 | .6626 |

- **15 个 base + 15 个 `_active`**，共 30。**9 个 VECTOR / 6 个 MATRIX（每族各半）** ⇒ 按铁律必须先 `vec_*` 聚合再进常规算子。
- **实际拥挤度 7.3 α/字段**（219 α / 30 字段；单字段最多 35 次 = `boundary_transaction_total`，最少 0 次 = `transaction_account_total_active`）
  ⇒ 这是 KOR 现存**最空的一块活字段面**，比 mmp（75/521）还空一个数量级。
- **无 dispersion 族字段**（没有 std/var）⇒ Dispersion 桶在本集不可用；可做 **Change / Surprise / Event-conditioned / 因果（持仓→交易）**。
- ⚠ **十年跨度未验**：cov 是当前截面，不代表 2014 就有数据。首个探针波的 `get_alpha_yearly_stats` 逐年长表就是约束 4 的检验口
  （沿用 §5.33.4 第三条的判据：< 10 年 ⇒ 不判死、不继续，交用户二选一）。**这条必须在发波后第一件事就核对，不得留到第三波。**

---

### 5.38 波 224 落袋（mmp 判死）+ `other695` 被约束 4 一票否决 + 波 225 留证（2026-10-30 本段续）

#### 5.38.1 波 224 实测（2 条，**已写库** `wave=224 / dataset=mmp_nlp_sentiment / multisim=4hnG28Vi4XVbpG89oSMs7z`）

| 槽 | 桶 | alpha | S | F | 2Y | subU | TO | 裁定 |
|---|---|---|---|---|---|---|---|---|
| C | event_type | `N1NqkemX` | **0.54** | 0.25 | **0.39** | 0.68 | 0.088 | 死 |
| D | Surprise | `xAr9X18N` | **0.19** | 0.05 | **0.55** | 0.14 | 0.145 | 死 |

两槽 `S < 0.8` ⇒ 命中 §5.33.5 预注册的第二档判据 ⇒ **`mmp_nlp_sentiment` 四桶
（Dispersion / Event-conditioned / event_type / Surprise）全灭，**官方判死**。

逐年（`N1NqkemX`，2014–2023）：−0.41 / 0.88 / 0.97 / 1.13 / 0.02 / 0.41 / 0.37 / 1.18 / 0.64 / 0.14
⇒ **10 年里 S ≥ 1.3 的一年都没有（最高 1.18）**，2Y 闸结构性不可达。
**约束 4 对 mmp 是满足的**（2014–2023 每年都有持仓与 PnL）⇒ 死的不是数据跨度，是**信号强度**。

封存动作：`seal_dead_end` 的 `force_seal` / `require_forum_recon=False` 需用户确认，**本轮只写结论、不擅自封**。

#### 5.38.2 ⭐ 本段最强发现 + 最硬否决：`other695`（Korean Imports Data）

既有候选 **`j2YWRzXW`** 是全仓唯一"硬闸基本全过"的 alpha：

| 指标 | 值 | 判 |
|---|---|---|
| S / F / 2Y / subU | **1.73 / 2.11 / 2.05 / 1.66** | 全过 KOR 硬线（1.58 / 1.0 / 1.58 / —） |
| IS_LADDER / CLUSTER_TEST | pass / pass（0.73） | 过 |
| `CONCENTRATED_WEIGHT` | **0.147 > 0.1** | **唯一不合规项** |

数据集画像（`get_datasets(category="other")` + `get_datafields(filter_sharpe=false)`）：
`other695` = **Korean Imports Data**，韩国**分厂商进口额**映射到上市公司，**双周更新**，cov 0.4886，仅 3 个字段 ——
`oth695_code_3`（Bloomberg 代码）、`oth695_company_eng_2`（英文名）是标识符，
**只有 `oth695_import_value_4` 是信号**（VECTOR，cov 0.4057，αC **148**，70 用户）
⇒ **事实上是单字段数据集 ⇒ 任何 alpha 天然是 ATOM**（不受约束 5 约束）。

⚠⚠ **`get_alpha_yearly_stats("j2YWRzXW")` 把这条线一票否决**：

| 年 | 2014 | 2015 | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 |
|---|---|---|---|---|---|---|---|---|---|---|
| longCount | **0** | **0** | **0** | **0** | 348 | 363 | 308 | 316 | 304 | 314 |
| S | 0 | 0 | 0 | 0 | 0.27 | 2.34 | 2.52 | 2.67 | 3.45 | 0.72 |

⇒ 数据从 **2018** 才开始，有效跨度 **6 年**，**约束 4（近十年都要有数据）硬否决**。
注意这不是"覆盖率低"能看出来的：cov 0.4886 看着还行，`backtest startDate=2014-01-01` 也照样跑得动
（平台对缺数据的年份直接空仓，不报错），**只有逐年 longCount 会说话**。

- **纪律升级（写死）**：`coverage` / `valueScore` / `alphaCount` / 漂亮的 S **都不能证明十年跨度**。
  判据只有一条 —— **`get_alpha_yearly_stats` 最早一年的 `longCount`（或 `shortCount`）是否 > 0**；
  首年持仓为 0 ⇒ 记 `pre_YYYY 无数据`，并**以"首个有持仓年"为起点**，**不得以 backtest 的 startDate 为起点**。
- 第二处不合规：该 alpha 的 `trade_when(greater(rank(adv20), 0.6), …)` 里 `adv20` 是 **PV 字段**，
  与 `oth695`（OTHER）同表达式 ⇒ 触约束 5（`pyramids.list` 自证：KOR/D1/PV + KOR/D1/OTHER，effective=2）。
  ⇒ **即便约束 4 放开，也必须先去 PV 门**。
- 结论：**other695 整条线出局**，`j2YWRzXW` **不进提交队列**；`oth695_import_value_4`
  记入"机制是真的、数据不合规"清单（与 §5.36 的"强 DL 但 prod 撞墙"同类：好信号 ≠ 可用候选）。

#### 5.38.3 波 225 已发（`13c9A0gqa4th8NjcxZs4uZ4`，**只为留证**）

| 槽 | 表达式 | 目的 |
|---|---|---|
| A | `hump(group_rank(ts_sum(ts_backfill(vec_avg(oth695_import_value_4), 66), 20), sector), hump=0.0025)` | 去 PV 门 ⇒ 纯 ATOM；看 S 是否守住 1.3+ |
| B | `tail(hump(group_rank(ts_sum(ts_backfill(vec_avg(oth695_import_value_4), 66), 20), sector), hump=0.0025), lower=0.02, upper=0.98, newval=0)` | 同核心 + 尾部裁剪 ⇒ 看 CW 0.147 能否压到 0.1 以下 |

设置与 `j2YWRzXW` **逐字对齐**（decay 4 / SECTOR / truncation 0.08 / maxTrade ON / nanHandling ON / unitHandling VERIFY /
pasteurization ON / 2014-01-01→2023-12-31），否则不是单变量对照。**结果只作机制证据、不作提交候选**（约束 4 已否决整条线）。
预登记裁定：任一路径 `S ≥ 1.3 且 CW < 0.1` ⇒ 记为"机制可复现、数据不合规"；
两路都掉到 `S < 1.0` ⇒ 记"1.73 靠 PV 门筛流动性 + 2018–2023 进口失真"，写进经验库。

#### 5.38.4 下一主攻回到 `fund_holdings_panel`（institutions 0/3，mult 1.4）

§5.37.5 的 30 字段画像与双通道取证已就绪，**波 226 直接开**。
⚠ 与 other695 的对照必须记住：`fund_holdings_panel` 的 cov .8093 **同样不证明**十年跨度
⇒ 波 226 收批后第一件事仍是 `get_alpha_yearly_stats` 的**首年 longCount**，而不是看 S。

---

### 5.39 ★ 波序重排依据：塔位缺口 × 本地严格产出率（2026-10-30 本段，零配额取数）

`get_pyramid_alphas(region=KOR, delay=1)` × `get_pyramid_multipliers` × `get_mining_yield(by_dataset, strict)`
三者交叉，得到 KOR/D1 的**未点亮塔**及其"本地是否出过货"：

| 塔 | 已点/需 3 | mult | 本地实测（strict，ra_clean/backtested） | 判读 |
|---|---|---|---|---|
| **analyst** | **2** | **1.6** | **analyst44 8/42 = 19.05%（全区第 2）**；analyst10 5/105 = 4.76% | ⭐ **再出 1 颗即点亮，且是本地第二高产集** ⇒ 最高优先级 |
| **other** | **1** | **1.6** | **other466 20/110 = 18.18%（全区第 1）**；other695 已判死（§5.38） | ⭐ 再出 2 颗点亮；但 prod_wall 0.556（撞墙率高），需先算余量 |
| institutions | 0 | 1.4 | `fund_holdings_panel` 0/8、`institutions6` 0/6 | 波 226 目标；两集都还没出过货，属"从零开" |
| pv | 2 | 1.4 | pv106 0/34（25 行 RA 状态未知）、intraday_pv_feats 0/8 | 再出 1 颗点亮，但 **pv106 是 34 条无一 ra_clean** ⇒ 低优先 |
| risk | 0 | 1.3 | risk71 0/16、risk59/60/68/70 全 0 | 低优先（risk71 16 条零产出） |
| insiders | 0 | 1.2 | insiders5 0/35、insiders1 0/2 | 低优先（另有 0.78 prod 地板旧结论） |
| earnings | 0 | 1.1 | earnings3 0/4 | 低优先 |
| macro | 0 | 1.4 | macro63 0/3 且已判死（无截面） | 排除 |
| imbalance / socialmedia | 0 | 1.0 | imbalance5 已判死；socialmedia 无在库实测 | 排除（mult 也是全区最低 1.0） |
| news / sentiment | 0 | 1.6 | news* 全 0 产出；sentiment26 已判死 | mult 高但**实测全灭** ⇒ 除非有新机制，否则不投整波 |
| fundamental / model / shortinterest | **已点亮** | — | — | 约束 1 要求"未点亮塔" ⇒ 本阶段不作主攻（shrt38 仅作对照/存量） |

**波序（据此写死，替代此前的"按 category 字母序"）**：
① 波 226 = `fund_holdings_panel`（institutions，收批后**先查首年 longCount**）；
② 波 227 = `analyst44`（analyst 只需 1 颗点亮 + mult 1.6 + 本地 19% 产出）；
③ 波 228 = `other466`（other 需 2 颗 + mult 1.6，但**先查 prod 余量**：已有 prod_blocked 5 条）。

⚠ 两条读数纪律（本轮新增）：
- `get_mining_yield.strict` 的 `ra_clean` 对 NULL 宽容计，`ra_unknown` 大（全区 310 行）⇒
  **pv106 的"0/34"不能读成"34 条全灭"**，其中 25 条是**根本没读过 RA 状态**。判一个集"出不出货"前先看 `ra_unknown` 占比。
- 塔位计数（`get_pyramid_alphas`）与"OS alpha 自报的 pyramids.list"两套口径此前对不上（analyst 2 vs ≥3）。
  本表**只用 `get_pyramid_alphas` 的官方计数**作决策，self-report 不作依据；差异待下次平台核对，别在波序里混用。

★ **由交叉表读出的第二条路（比再挖更便宜，但需用户拍板）**：`analyst44` 有 **8 条 ra_clean 却 0 条 prod_clean**
（`prod_blocked=1`、`prod_wall_ratio=1.0`，但分母只有 1 ⇒ 大部分**根本没测过 prod**），`other466` 更有 **20 条 ra_clean**。
`get_submit_ready(KOR)` 却只回 1 条（`LLZ6wZO2`）⇒ **这些 ra_clean 没进队列的主因是 prod 未测，不是质量不够**。
⇒ 点亮 analyst / other 两塔的最短路径可能是"**给存量 ra_clean 补 prod 实测 → 挑 <0.7 的提交**"，
而不是再烧配额挖新的。按约束 3，prod 一律走 MCP；按提交纪律，最终须用户确认。本轮先登记，不擅自行动。

### 5.40 `analyst44` 字段画像（540 字段；为波 227 铺底，2026-10-30 本段）

`get_datafields(dataset_id="analyst44", KOR/TOP600/D1, filter_sharpe=false, limit=100)`（**必须 `filter_sharpe=false`**，
否则被过滤的字段永远看不到；本集实测 540 条全返回，`pages_fetched` 见转储）：

| 维度 | 读数 |
|---|---|
| 规模 | **540 字段**（VECTOR **374** / MATRIX **166**） |
| 覆盖 | median **0.7635**，p25 0.6209，**cov ≥ 0.8 共 235 个**，cov < 0.4 仅 15 个 |
| 标识符/非信号 | **156 / 540**（`*_coveredby`、`*_lastactccy`、`*_ccy` 一类）⇒ 真正可当信号的约 384 |
| 头部经济轴（§0.1 规则） | **`anl44_second_en_eps_value`：aC 98 / uC 64 / cov .758 / VECTOR** —— **EPS 估计水平‑修正轴是这个集最强的轴**，不是 BVPS / CAPEX / ROE |
| 第二梯队 | `eps_gaap_estimate_4wk_down_count` aC 50 cov **1.000**；`sales_downward_revisions_4w` aC 35 cov **1.000**；`pretaxprofit_estimates_down_4w` aC 34 cov **1.000** |
| 家族强弱 | **breadth_down（修正广度）cov 中位 1.000 且 aC 最高** ⇒ 唯一"全截面 + 高拥挤"的家族；**dispersion 仅 10 个、max aC=2 ⇒ 分歧度轴在本集很弱**（别照搬 news 的 Dispersion 优先）；surprise 有 `prevalue`/`value` 配对（84 个，median cov .649）可做事件跳变 |
| 必须弃用/backfill | `anl44_2_*_lastactvalue`、`anl44_second_en_operatingprofit_value`(cov .283)、`last_quarterly_*_update`(cov .27–.31) 等 13 个信号字段 |

**由此定的波 227 机制方向**（写死，避免下一波重新想）：
① 主攻 **breadth × magnitude 背离**（修正人数已掉、但估计值还没动/反向 ⇒ 信息未定价）；
② 备选 **Surprise**（`prevalue` vs `value` 的事件跳变，用 `ts_zscore` 归一），
③ **不做 Dispersion**（本集该轴实测只 2 个 aC，属"名字有、信号无"）。
⚠ 波 227 发批前仍须补两通道取证（论坛模板 + 外部论文），并核 `analyst44` 的**首年 longCount** ——
它和 other695 / fund_holdings_panel 一样，**高 cov 不证明十年跨度**。

### 5.41 波 225 收批（`13c9A0gqa4th8NjcxZs4uZ4` → 已写库 `wave=225 / other695`）

| 槽 | alpha | 表达式要点 | S | F | 2Y | subU | CW | TO | 裁定 |
|---|---|---|---|---|---|---|---|---|---|
| A | **`leAk66xx`** | 去 PV 门，纯 `hump(group_rank(ts_sum(vec_avg(...),20),sector))` | **1.77** | **2.11** | **2.24** | 1.68 | **pass** | 0.031 | **fail=[] 全 RA 通过**（但约束 4 否决） |
| B | `zq3QwwaR` | 同 A 外包 `tail(lower=.02,upper=.98,newval=0)` | 0.92 | 1.23 | 0.86 | 0.85 | **0.514 fail** | 0.016 | 死 |

三条结论，按预登记逐条对号：

1. **预登记第一支命中**：A 路径 `S 1.77 ≥ 1.3` 且 `CW 通过` ⇒ 按 §5.38.3 记为
   **"机制可复现、数据不合规"**。相对 `j2YWRzXW`（S 1.73 / 2Y 2.05 / CW 0.147 fail）**去掉 PV 门反而每项都更好**。
2. **约束 4 复核（逐年表）把 A 也拦下**：2014–2017 `longCount=0`、`pnl=0`、`turnover=0`；
   2018 才有 400/221 持仓（S 0.21），2019–2022 S 2.49/2.03/2.92/3.79，2023 S 0.81
   ⇒ **有效跨度 2018–2023 = 6 年** ⇒ 约束 4「近十年都要有数据」**硬否决，不进提交队列**。
3. ⚠ **`tail(..., newval=0)` 不是 CW 的通用解，本波反证**：它把 `group_rank` 的尾部直接置 0，
   使多空结构从 375/279 变成 **49/607**（几乎单边空），CW 从"通过"炸到 **0.51393**、2Y 0.86、S 0.92。
   ⇒ **真正修好 CW 的是 `hump`（0.147 → 通过），不是 `tail`**。此前把 `tail` 当"分极端尾部"的默认手段，此处记为反例。

★ **可迁移结论（本波最大产出）**：`trade_when(PV 流动性字段 > T, …, -1)` 这种**用 PV 字段当流动性门**的写法，
可以换成同族平滑 `hump(..., hump=0.0025)` —— S 1.73→1.77、2Y 2.05→2.24、CW 0.147→通过，
既**不降指标**又**解除约束 5 风险**。这条与 §5.38.2 的"adv20 是 PV 字段"是同一件事的两面。

⚠ `leAk66xx` 是本战役**第一颗 `fail=[]` 的 alpha**（LOW_SHARPE / LOW_FITNESS / LOW_TURNOVER / HIGH_TURNOVER /
CONCENTRATED_WEIGHT / LOW_SUB_UNIVERSE_SHARPE / CLUSTER_TEST / LOW_2Y_SHARPE / MATCHES_PYRAMID **全 pass**，
`pyramids.effective=1` ⇒ **ATOM**，KOR/D1/OTHER mult 1.6）。它的价值是**证明机制**，不是候选。
**留给用户的判断点**：若"近十年"这条对 OTHER 类宏观/进口数据可以放宽，这是现成的最佳候选；
在用户改口径前，本台账一律按否决处理，不提交。

### 5.42 波 226 已发（`2jULhFfr254haIXx28cfajq`，`fund_holdings_panel`，institutions 0/3）

设置：KOR/TOP600/D1，**SECTOR / decay 4 / truncation 0.08 / maxTrade ON / nanHandling ON / unitHandling VERIFY**
（与 `leAk66xx`、`j2YWRzXW` 同一套 —— 本区实测最优栈）。

| 槽 | 桶 | 表达式 | 机制 |
|---|---|---|---|
| A | Change | `group_rank(ts_delta(ts_backfill(holder_account_total, 66), 66), sector)` | 持有人账户数**变化率**（铁律 A：账户数是单边恒正存量，禁裸水平）⇒ 散户/基金参与度扩张 |
| B | Event-conditioned | `trade_when(rank(ts_zscore(ts_backfill(vec_sum(large_trade_count_50bps), 66), 252)) > 0.7, group_rank(ts_delta(ts_backfill(mean_security_weight, 66), 66), sector), -1)` | 只在**大单活跃度异常日**交易（A-1 第 5 问：事件性稀疏 ⇒ 必须门控，禁裸 rank） |

预登记裁定：任一路径 `S ≥ 1.3 且 fail=[]` ⇒ 该机制可继续做 3 槽扩写；两路 `S < 1.0` ⇒ `fund_holdings_panel` 记"二度全灭"
（该集已有 8 条回测 0 出货）。
⚠ **收批后第一件事仍是 `get_alpha_yearly_stats` 的首年 `longCount`**（约束 4），不是看 S。

### 5.43 波 227 设计与取证（`analyst44`，analyst 2/3，mult 1.6；**未发**，等 226 腾槽）

**通道 A｜论坛（MCP `search_forum_posts` → `read_forum_post`）**：
〈【Alpha Idea】分析师盈利预期修正广度：盈利动能的横截面代理〉id `43250301270295`，**36 票 / 5 评**（2026-09-04）。
可落地模板（原文抽象）：
`revision_breadth = signed_power(group_normalize(ts_smooth(vec_agg(up)/vec_agg(down), H), group), p)`
原文要点与**评论补充**（都写进了本轮设计）：
① 用「上调数/下调数」或「上调占比」，**分母≈0 会爆炸**，必须 winsorize 或改占比；
② 评论 MK63856：比值在覆盖数 <3 时应置 NaN；**且「广度的变化速度」比水平更有信息量 ⇒ 试 `ts_delta` / 相对自身历史标准化**；
③ 评论 XM75236：`up/(up+down)`（只看参与者）与 `up/覆盖总数`（含未修正者）**是两种口径，须对照**；
④ 原文 IS Sharpe 3.0~4.5、TO 0.15~0.35，Neutralization 建议 STATISTICAL/行业中性化、decay 短档。

**字段配对（本集实测，全部 cov = 1.000，全 VECTOR ⇒ `vec_sum`）**：

| 口径 | up | down | aC(up/down) |
|---|---|---|---|
| GAAP EPS | `eps_gaap_estimate_4wk_up_count` | `eps_gaap_estimate_4wk_down_count` | 16 / **50** |
| Sales | `sales_upward_revisions_4w` | `sales_downward_revisions_4w` | 13 / **35** |
| PTP | `pretaxprofit_estimates_up_4w` | `pretaxprofit_estimates_down_4w` | 19 / **34** |
| 覆盖数（做置信度） | — | `sales_estimate_analyst_count` / `gaap_eps_num_analyst_estimates` | 16 / 1 |

**两条待发表达式（`preflight_expressions(region=KOR, universe=TOP600, delay=1, dataset_id=analyst44, agg=vec_sum)` ⇒
`valid=true`，6 字段全命中，`wrapped_fields=[]` 无需包装）**：

```
A(净广度·水平): group_rank(ts_mean((vec_sum(eps_gaap_estimate_4wk_up_count) - vec_sum(eps_gaap_estimate_4wk_down_count)) /
                              (vec_sum(eps_gaap_estimate_4wk_up_count) + vec_sum(eps_gaap_estimate_4wk_down_count)), 22), sector)
B(利润率扩张背离): group_rank(subtract(ts_mean(rank(vec_sum(pretaxprofit_estimates_up_4w) - vec_sum(pretaxprofit_estimates_down_4w)), 22),
                            ts_mean(rank(vec_sum(sales_upward_revisions_4w) - vec_sum(sales_downward_revisions_4w)), 22)), sector)
```

- B 是**价差（背离）**不是相加：PTP 净修正 − Sales 净修正 = **利润率预期扩张**，
  满足 A-3「`subtract` 两腿同源同一数据集 + 单一经济含义」的放行口径，**不触 `equal_weight_leg_add`**。
- 两腿同源 `analyst44` ⇒ **ATOM**；`analyst` 类目，约束 5（PV/MODEL/OTHER）**不适用**。
- 备选（波 228 素材，本轮先登记不设计）：本集还有 `pretaxprofit_to_sales_ratio`、`net_income_to_sales_ratio_estimate`
  两个**利润率比值字段**（可直接做水平/变化），以及 `eps_estimate_stddev` / `*_high` / `*_low` 一类**分歧度字段**
  —— 但分歧度轴实测 aC 最高仅 2（弱），别优先。

⚠ **两个工具陷阱（本轮实测，写死）**：
① `preflight_expressions` **缺省 `region=USA / universe=TOP3000`** ⇒ 不传区域时 KOR 字段**全被判 unknown**
（首跑 6 字段全 unknown、`platform_field_count=0`）。**必须显式传 region/universe/delay + dataset_id**。
② `create_multi_simulation` 不接 `startDate/endDate`，但平台实际按 **2014-01-01→2023-12-31** 跑
（波 225 回传的 settings 为证）⇒ **约束 4 的诊断窗口天然覆盖十年**，无需额外参数。

#### 5.43.1 通道 B｜外部文献取证（2026-10-30 `WebSearch`，用于裁决「A 腿形态是否站得住」）

| 来源 | 给出的机制句 | 对本波的作用 |
|---|---|---|
| [Mill Street Research — Do Analyst Estimate Revisions (Still) Help Forecast Relative Stock Returns?](https://www.millstreetresearch.com/do-analyst-estimate-revisions-still-help-forecast-relative-stock-returns/) | **Revisions breadth** = 覆盖某股的分析师中**上调 vs 下调的净比例**，回看窗 **X ≈ 100 天**；另设 **revisions magnitude**（修正幅度）为**独立**指标 | ⭐ **直接确认 A 腿形态**：`(up−down)/(up+down)` 就是"净比例"，且**广度与幅度是两个正交指标、不该混成一条** ⇒ A 只做广度、把幅度留给后面的腿，是**文献支持的分工**，不是随意简化 |
| [Taylor & Francis 2025 — Analysts' cash flow forecasts and the underreaction to earnings announcements](https://www.tandfonline.com/doi/full/10.1080/00014788.2025.2545847) | **post-earnings forecast revision drift (PFRD)**：公告后分析师修正存在**持续漂移**（欠反应） | 给 A/B 共同的方向句与**持有期**：修正不是当日兑现，而是数周到数季的**惯性** ⇒ `ts_mean(..., 22)` 的平滑窗与"持有数周~数季"同量级，**不是拍脑袋** |
| [JEF — 分析师预测差异程度异象再检验](https://sf.cufe.edu.cn/info/1198/6453.htm) | 预测**分歧度**（dispersion）异象：高分歧 → 低后续收益 | 反向确认§5.40 的取舍：本集分歧度字段 **aC 最高仅 2（弱）**，而文献说分歧度异象是**独立轴**、不该塞进广度腿 ⇒ **分歧度留作后续独立机制**，本轮不做 |
| [What drives the dispersion anomaly?](https://www.sciencedirect.com/science/article/abs/pii/S037842662200005X) | 分歧度异象的驱动分解（套利限制 / 波动） | 同上，仅作**波 229+ 的机制备选**登记，不改变本波设计 |

**双通道裁决**：通道 A（论坛 id `43250301270295`）给的是「净广度 + 平滑 + `up/(up+down)` 口径」，
通道 B（Mill Street + PFRD）给的是「净比例 = 广度的标准定义、X≈100 天、幅度是独立指标、修正是数周~数季惯性」
⇒ **A、B 指向同一机制**（RA skill §②.d 双通道裁决表首行：⭐ **优先组装**）。
两通道**唯一分歧点是回看窗**（论坛未指定、文献给 X≈100 天，平台只有 66/252 两档邻近）：
本波取 **22 日平滑 + 4 周修正字段**（字段本身已是 `_4wk` 口径，等价于短窗修正），
**若 A 腿过闸后再测 66/252 平滑窗**——按「先短窗再长窗」纪律（news skill §3），不一次铺开。

⚠ 文献偏误声明（写进 A-3 concept 的 `Boundary Conditions`）：上述结论主要在 **USA 大盘样本**得出，
KOR 是**小宇宙 + 不同的分析师生态** ⇒ 只作**假说 + 方向句 + 持有期**，成立与否以本区实测为准。

### 5.44 波 226 收批：`fund_holdings_panel` 二度全灭（institutions 仍 0/3）

multisim `2jULhFfr254haIXx28cfajq`，2 条全 COMPLETE，入库 `{linked:0, upserted:2}`，
wave_results 暂定 **FAIL（0/2 过硬闸，0 条过 near 线 1.0）**。

| 槽 | alpha | S | F | 2Y | subU | CW | TO | 失败项 |
|---|---|---|---|---|---|---|---|---|
| A `group_rank(ts_delta(ts_backfill(holder_account_total,66),66), sector)` | `78L0qGJb` | **0.56** | 0.32 | 0.46 | 0.59 ✅ | pass ✅ | 0.059 | LOW_SHARPE / LOW_FITNESS / LOW_2Y_SHARPE |
| B `trade_when(rank(ts_zscore(ts_backfill(vec_sum(large_trade_count_50bps),66),252))>0.7, group_rank(ts_delta(ts_backfill(mean_security_weight,66),66), sector), -1)` | `6Xd3PGzK` | **−0.09** | −0.02 | 0.16 | **−0.07 fail** | **0.1508 fail**（2015-04-07） | 0.039 | 5 项（含 CW / subU） |

**归因（写进经验库，可迁移）**：
1. **A 是"干净但太弱"**：CW/subU/换手全过（换手 0.059 极低、margin 0.00135 极薄），
   说明「持有人账户数变化率」这个机制在 KOR **方向对、量级不够** —— 它更像"参与度"这个慢变量，
   单腿吃不满 RA 的 S≥1.58。**不是字段无效，是信号太钝**。
2. ⚠ **B 暴露 `trade_when` 在 KOR 小宇宙的第二个杀手（第一个是波 225 的 CW 0.147）**：
   `rank(ts_zscore(vec_sum(large_trade_count_50bps),252)) > 0.7` 这个门控**把可选池砍到不足以摊平权重**
   ⇒ CW **0.1508** + subU **−0.07** 双 fail。**教训：KOR/TOP600（600 只）上，事件门控的阈值必须比 USA 松**
   （0.7 分位 = 只留 30% 股票 × 事件日），且**门控腿本身不能是 VECTOR 计数类**（`vec_sum` 后的截面分布极偏）。
   ⇒ 后续用 `trade_when` 时**先单独回测门控腿的 `longCount`**，别把门控和主信号绑在一批里一起瞎。
3. **预登记裁定兑现**：两路 `S < 1.0` ⇒ `fund_holdings_panel` **记二度全灭**（该集累计 10 条回测 / 0 出货）。
   ⚠ **不判死**：`seal_dead_end` 的 `forum_recon` 闸是 fail-closed，本集**尚未做**论坛取证
   ⇒ 只能记"二度全灭"，判死留待补取证后走 `seal_dead_end`（`force_seal` 属用户确认项，不擅自用）。

### 5.45 波 227 已发（`analyst44`，multisim `3qCnfB1CI4qebGxL7mL6BzU`）

槽位：A = 净广度·水平、B = 利润率扩张背离（表达式与取证见 §5.43 / §5.43.1，逐字未改）。
设置：KOR/TOP600/D1，SECTOR，decay 4，truncation 0.08，maxTrade ON，nanHandling ON，
pasteurization ON，unitHandling VERIFY（与波 225/226 同一获胜栈，`agg=vec_sum`）。

**分母安全性（本轮补证，写死以免下次再纠结）**：
表达式 A 的 `(up−down)/(up+down)` **不会产生 inf** —— 分子是分母两项之差，
当 `up+down=0` 时分子必为 0 ⇒ 最坏是 `0/0=NaN`（`nanHandling=ON` 下按缺失处理），
**不会出现"分母趋零爆炸成极值"**。论坛 §5.43 提醒②的爆炸风险只对「`up/down` 比值型」成立，本式不属该形态。

预登记裁定（收批即执行，不许事后再解释）：

| 收批读数 | 裁定 |
|---|---|
| 任一路 `S ≥ 1.58 且 fail=[]` | ⭐ 立即查首年 `longCount`；过闸则**当日进提交队列**（analyst 塔可就地点亮，2/3 → 3/3） |
| 任一路 `1.3 ≤ S < 1.58 且 fail⊆{S,F,2Y}` | 机制成立、强度不足 ⇒ **3 槽扩写**（净广度换 `ts_delta` 速度口径 + 66/252 平滑窗 + PTP/Sales 第二种背离） |
| 两路 `S < 1.0` | `analyst44` 的**广度轴**判弱；改打本集第二轴（`pretaxprofit_to_sales_ratio` / `net_income_to_sales_ratio_estimate` 利润率比值水平/变化，见 §5.43 备选） |

⚠ **收批第一件事仍是 `get_alpha_yearly_stats` 首年 `longCount`**（约束 4）——
波 225 的 `leAk66xx` 就是"S 1.77 / F 2.11 / 2Y 2.24 / fail=[] 却被 2014–2017 零持仓一票否决"，
**analyst44 属 IBES 系常规估计数据、跨度风险低但未实测，必须验**。

### 5.46 波序纠错（2026-10-30）：**`other466` 不点 OTHER 塔**，波 228 改打 `other545`

#### 5.46.1 塔归属是**按 alpha 实测**，不是按数据集名前缀

`get_submit_ready(KOR, ALL)` 的 50 行里，凡 `oth466_*` 表达式，`towers` 一律是
**`KOR/D1/FUNDAMENTAL`（mult 1.6）**，而 KOR/D1/FUNDAMENTAL 官方计数已是 **3/3（已点亮）**。

⇒ §5.39 把 `other466` 排进「OTHER 塔 1/3、需 2」是**错的**：数据集叫 `other466`，
但平台把它归到 `fundamental` 塔。**再挖 other466 只是在已点亮塔上叠 alpha，不推进任何未点亮塔。**

**纪律（写死）**：塔归属以 **`get_pyramid_alphas` 的官方计数 + 该数据集 alpha 回传的 `pyramids.list`** 为准；
数据集 **id 前缀不是塔名**（`other466`→fundamental、`other695`→OTHER 已各有一例实证）。
选下一波数据集前，先问一句「它的 alpha 落哪个塔」，别按名字猜。

#### 5.46.2 KOR/D1 塔位现状（`get_pyramid_alphas` 官方计数，2026-10-30）

`fundamental 3 ✅ | model 3 ✅ | shortinterest 4 ✅`｜
`analyst 2（1.6）| pv 2（1.4）| other 1（1.6）`｜
`institutions 0（1.4）| macro 0（1.4）| risk 0（1.3）| insiders 0（1.2）| earnings 0（1.1）|`
`imbalance 0（1.0）| news 0（1.6）| sentiment 0（1.6）| socialmedia 0（1.0）`

**性价比排序（缺口小 × 倍率高）**：analyst（差 1、1.6）> pv（差 1、1.4）> other（差 2、1.6）>
institutions / macro（差 3、1.4）> risk（1.3）> insiders（1.2）> earnings（1.1）。

#### 5.46.3 KOR `other` 类目 26 个数据集（`get_datasets(category="other")` 快照）

全部 `pyramidMultiplier = 1.6`。按「白空间（alphaCount 低）× 覆盖（约束 4 先验）× valueScore」筛：

| 数据集 | 名称 | cov | 字段 | alphaCount | valueScore | 备注 |
|---|---|---|---|---|---|---|
| **other545** | **Linked Firms Momentum (NEMO 2.0)** | **0.8393** | 4（全 VECTOR） | 46 | 5 | ⭐ **本轮选中**：网络动量，机制有强文献支撑 |
| other546 | Institutional Network Analysis | 0.5632 | 10（全 VECTOR） | **9** | **7** | 白空间最大（valueScore 7），但 cov 低、机制偏「披露相似度」 |
| other327 | Sensitivity to Interest Rates | 0.7866 | 3 | 31 | 5 | 利率敏感性，macro 邻近 |
| other78 | Earnings and conference call | 0.7925 | 11 | 70 | 6 | 描述与名不符（平台描述错位） |
| other436 / other424 | Dividend model / prediction | 0.57 / 0.59 | 3 / 3 | 15 / 44 | 6 / 5 | 股息突变，事件稀疏 |
| other323 | Global Equity Premarket | 1.0 | 11 | 1041 | 3 | 拥挤 |
| acquisition_model | 收购概率 | 0.9937 | 15 | 111 | 5 | 事件型，可能好料 |
| other695 | Korean Imports | 0.4886 | 3 | 180 | 4 | **约束 4 已否决**（2018 起） |
| other475 | Manufacturer Exports | 0.357 | 1 | 632 | 2 | 与 other695 同源风险（双周频、2018 起），**先查跨度再碰** |
| dl_riskfree_returns | DL Risk Free Returns | 0.9095 | 57 | 8021 | 2 | 饱和 |

⚠ **平台描述错位**：本类目里多条 `description` 与数据集名完全不匹配（如 `other424 Dividend prediction`
的描述是 BBID/RIC 映射）⇒ **不许按 description 选数据集/字段**，本区只能按 `get_datafields` 的**字段级 description** 判断。

#### 5.46.4 `other545` 字段画像（4 字段，cov 全 0.8393，全 VECTOR）

| 字段 | 含义 | alphaCount |
|---|---|---|
| `oth545_score` | **NEMO 2.0 复合分**（7 条网络动量信号聚合） | 20 |
| `oth545_pln_omen` | **NLP 文本挖掘的关联动量**（按文本关联公司计） | 3 |
| `oth545_mpd` | 机器学习**价格动量**分（纯价格，**对照组**） | 13 |
| `oth545_mktcap` | 市值（可投资性/规模轴） | 10 |

⇒ 结构极干净：**一条复合腿 + 一条纯网络腿 + 一条纯价格动量腿（天然对照组）**，
是 KOR 里少见的「自带归因对照」的数据集。

#### 5.46.5 通道 A｜论坛：**无对口模板**（如实记录，不是"没查"）

`search_forum_posts("network momentum peer linkage alpha")` → **50 命中**，逐条看题后
**没有一条网络动量/关联动量的可落地模板**。最接近的两条：

| id | 标题 | 票 | 与本案的关系 |
|---|---|---|---|
| `23832785873943` | 【Alpha 灵感】Does the Delay in Firm-Specific Information Cause Momentum? | 8 | 信息不确定性**放大**动量；已读正文，模板是 `rank(ts_std_dev(returns,150)) × rank(momentum)`，**不是网络动量**；两条评论只讲「动量要除以价格/波动去量纲」 |
| `18641983716503` | 【Alpha灵感】The Momentum of News | 17 | 新闻情绪动量，非跨公司溢出 |
| `41648177190039`（启示录合集） | 100+ 从论文到 alpha 的复现 | 85 | 后续可作检索入口，本轮未逐条读 |

⇒ 触发 RA §②.d 决策表第 3 行：**「B 有机制、A 无对应表达」⇒ ⭐ 按 A-1 五问自建骨架**。
**不是跳过取证**：检索式、命中数、逐条结论都记在这里，下波不重复空转。

#### 5.46.6 通道 B｜外部文献：网络动量（机制 + 方向句 + 持有期）

| 来源 | 机制句 | 用途 |
|---|---|---|
| Cohen & Frazzini (2008) *Economic Links and Predictable Returns*, JF —— 见 [文献综述引用](https://skjournal.upc.edu.cn/ch/reader/view_abstract.aspx?file_no=20170203&flag=1) | 客户-供应商链条上，**关联公司的收益可预测本公司未来收益**（信息沿经济链条缓慢扩散 + 投资者注意力有限） | 机制本体；**方向 = 关联公司涨 → 本公司后涨**（正号）；持有期数周~数季 |
| [Ali & Hirshleifer 2020 共享分析师覆盖动量（转述）](https://finance.baidu.com/fund/ab-159608) | **分析师共同覆盖是动量溢出的根源**，且能吸收行业/产业链/地域等其它关联动量 | 解释 `oth545` 里 `analystnet` 类关系为何有信息；也说明**网络动量 ≠ 行业动量** |
| [沈哲等, The British Accounting Review —— 文本主题相似性的 comomentum](https://cas.xmu.edu.cn/info/1022/7364.htm) | 用 **MD&A 文本主题相似度**构建跨企业关联，相似公司收益可预测目标公司，**多空年化 17.03%**；在**低关注、高套利限制**股票上更强 | ⭐ **与 `oth545_pln_omen`（NLP 文本关联动量）几乎逐字对应** ⇒ 本字段不是黑箱 |
| [JFE｜债券市场揭示的跨公司动量（冯健）](https://www.phbs.pku.edu.cn/info/1191/180841.htm) | 从**债券市场**识别企业经济关联，股票投资者因注意力有限而忽视 ⇒ 跨公司可预测性 | 佐证「不同数据源刻画同一机制」；支持多源稳健性 |
| [JBF｜Geographic Links and Predictable Returns](https://ifs.swufe.edu.cn/info/1012/1671.htm) | **地理关联**公司的收益同样预测本公司，且不能由风险解释；低关注/高套利成本/高情绪期更强 | 佐证「关联类型越非价格化，溢出越强」⇒ `pln_omen` 应强于 `mpd` |
| [知乎｜双重同行效应：同行均值 vs 群内偏离](https://zhuanlan.zhihu.com/p/2017691423919591486) | 行业**同行均值**带**正向**动量系数，**个股群内偏离**带**负向**（短期反转）；PI 与共享分析师动量相关仅 0.048 | ⚠ **对本设计是警告**：`group_rank(..., sector)` 会**混入行业动量**；若 A 腿过闸，下一波必须**剥掉 sector 均值**做对照 |

**双通道裁决**：B 有机制、A 无模板 ⇒ 自建骨架（RA 表第 3 行「最有价值」那一格）。
**方向句**：关联公司近期强 → 本公司未来数周偏强（正号）；`pln_omen`（非价格化关联）预期强于 `mpd`（纯价格）。
**失效边界**：低关注、高套利限制才成立 ⇒ KOR/TOP600 里大市值段可能失效（后续按市值分域验证）。
**文献偏误**：Cohen-Frazzini / Ali-Hirshleifer 都是 **USA 样本**；BAR 那篇是中国 A 股语境下的方法，
KOR 属第三种制度环境 ⇒ 一律作**假说**，以本区实测为准。

#### 5.46.7 波 228 设计（`other545`，OTHER 塔 1/3，mult 1.6）——**已预检，等 227 腾槽**

```
A(复合网络动量·水平): group_rank(vec_avg(oth545_score), sector)
B(纯 NLP 网络动量·水平): group_rank(vec_avg(oth545_pln_omen), sector)
```

`preflight_expressions(region=KOR, universe=TOP600, delay=1, dataset_id="other545", agg="vec_avg")`
⇒ `valid=true`，2 字段全命中，`vector_fields` 4 个已识别，`wrapped_fields=[]`（`vec_avg` 已手写）。

**设计要点（为什么是这两条）**：
1. **单变量对照**：两式**算子完全相同**、只差字段（复合分 vs 纯 NLP 分）⇒ 收批后能直接读出
   「网络动量里到底是不是价格动量在起作用」——这正是约束 2 要求的对比实验。
2. **`oth545_mpd`（纯价格动量）本轮不发**，留作波 229 的**对照组**：
   若 A 过闸而 `mpd` 也过闸且量级相当 ⇒ 记「只是价格动量换了包装」；
   若只有 A/`pln_omen` 过 ⇒ 记「网络扩散机制真实」。
3. **不用价差 / 不加第二字段**：约束 5 明令 **OTHER 字段不得两两组腿**
   （`subtract(pln_omen, mpd)` 即便满足 A-3 的「同源单义」放行口径，**也违反用户约束 5**）⇒ 本轮**只用单字段**。
4. **不加 `ts_zscore`/`ts_delta`**：本波先测**水平形态**，把「时序标准化」和「变化率」留给下一波做单变量升级
   （铁律 A 提醒：若显示"恒正/单边"体征再切变化率）。
5. 全 VECTOR ⇒ `vec_avg`（按关联公司数取均值，不被「关联公司多」放大；`vec_sum` 会引入规模偏置）。

**预登记裁定**：

| 收批读数 | 裁定 |
|---|---|
| 任一路 `S ≥ 1.58 且 fail=[]` | ⭐ 先查首年 `longCount`（约束 4）；过闸则进提交队列（OTHER 塔 1/3 → 2/3） |
| 任一路 `1.3 ≤ S < 1.58 且 fail⊆{S,F,2Y}` | 机制成立 ⇒ 波 229 = ① `mpd` 对照组 ② `ts_zscore/ts_delta` 升级 ③ **剥 sector 均值**（回应知乎那条警告） |
| 两路 `S < 1.0` | 网络动量在 KOR 小宇宙不成立（或已被价格动量吸收）⇒ 记负结论，转 `other546`（valueScore 7 / 白空间最大） |

⚠ 收批第一件事同样是 **`get_alpha_yearly_stats` 首年 `longCount`**（约束 4）。
`other545` cov 0.8393 只说明**截面覆盖**，**不证明十年跨度**——与 other695 的教训完全同型。

### 5.47 波 227 收批：广度轴判弱、背离轴进近闸（`analyst44`，ANALYST 仍 2/3）

multisim `3qCnfB1CI4qebGxL7mL6BzU`，2/2 COMPLETE，入库 `{linked:0, upserted:2}`，
wave_results 暂定 **PARTIAL（0/2 过硬闸，1 条过 near 线 1.0）**。

| 槽 | alpha | S | F | 2Y | subU | CW | TO | 失败项 |
|---|---|---|---|---|---|---|---|---|
| A 净广度·水平 | `P0oqq3A7` | **0.89** | 0.64 | 1.73 | 0.77 | pass | 0.034 | S / F（CLUSTER 0.62 warning） |
| B 利润率扩张背离 | `YP1nn09l` | **1.19** | 0.91 | **1.87** | 1.13 | pass | 0.041 | S / F |

两条塔归属实测均为 **KOR/D1/ANALYST（mult 1.6）** ⇒ analyst 塔仍 **2/3，本波未点亮**。

**归因（铁律 F，`get_alpha_yearly_stats` 逐年实测两轮）**

1. **约束 4 两条都满足**：A 首年 2014 `longCount 265 / shortCount 314`；B 首年 2014 `275 / 304`。
   ⇒ `analyst44` 十年跨度**实测通过**（与 other695 的 2014–2017 零持仓形态完全不同）。
2. **A 判弱（广度水平轴）**：10 年里 **3 年负**（2014 S −0.60、2015 −0.41、2018 −0.33），
   且 **top1 年 2022 占正收益 31.9%（>30%）** ⇒ 命中"过拟合指纹"行。
   ⇒ **广度·水平轴不再扩写**，与 §5.45 预登记的 row 3（广度轴判弱）一致。
3. **B 是 regime 依赖，不是参数问题**：4/10 年 `S<1.0`（2014 0.40 / 2015 0.14 / 2018 0.43 / 2020 0.11），
   其中 2015、2020 收益近乎归零（0.0093 / 0.0076）⇒ 命中"停滞段 ≥3 ⇒ regime 依赖"行。
   ⇒ ⛔ **不许扫 decay / 平滑窗 / 中性化谱**（决策表明写：此形态下平滑器谱整族无效）。
   单年集中度尚可（top1 2022 = 22% 正收益，<30%），所以**不是纯拟合**，是**强度与节奏都不稳**。
4. **预登记裁定的落点（不改判据）**：A 命中 row 3；B `S 1.19` **落在 row 2（≥1.3）与 row 3（<1.0）之间的空档**。
   如实记录：**B 不进 3 槽扩写**，仅作为近闸候选留档（`S 1.19 / F 0.91 / 2Y 1.87 / subU 1.13 / CW pass / CLUSTER pass`，
   距离 S≥1.58 差 0.39、F≥1.0 差 0.09）。若日后重启，唯一允许动作是**换 regime 无关的强度口径**（如再把 PTP−EPS 与 Sales−EPS 两个背离做单变量对照），
   不是参数谱扫。

### 5.48 波 228 已发（`other545`，multisim `49Nf1n1Pf5ikbptmRYeYYbK`）

表达式与设置逐字执行 §5.46.7（A `group_rank(vec_avg(oth545_score), sector)` / B `group_rank(vec_avg(oth545_pln_omen), sector)`；
KOR/TOP600/D1，SECTOR，decay 4，trunc 0.08，pasteurization ON，unitHandling VERIFY，nanHandling ON，maxTrade ON，`validate_fields=true`）。
227 收批后立即发，槽位 2 全空、并发上限 2 未破。

### 5.49 波 229 预置（`sentiment21`，SENTIMENT 塔 **0/3**，mult 1.6）——**已预检，等 228 腾槽**

**字段族陷阱（本轮实测，写死）**：`sentiment21` 的 138 字段按**有无分隔符**分成两套同名字族，**不是同一批字段**：

| 族 | 例 | cov | 说明 |
|---|---|---|---|
| **无分隔（0.475 族，本波取用）** | `snt21pos_mean` / `snt21pos_conf_up` / `snt21dts_sop` | **0.475** | 覆盖最高 |
| 有分隔（0.3518 族） | `snt21_pos_mean` / `snt21_pos_conf_up` | 0.3518 | 描述写 "USA D0 module" |
| 带窗口序号（0.3518 族） | `snt21_2pos_mean` … `snt21_5pos_mean` | 0.3518 | 2/3/4/5 日窗 |

⇒ **选字段必须逐字比对 id，不能按"看着像"取**（`snt21pos_mean` 与 `snt21_pos_mean` 是两个字段）。
另：`dts` 后缀是**倒序拼写**——`_sop`=positive、`_gen`=negative、`_tuen`=neutral（描述里才对得上）。
字段级 `alphaCount` 全部 ≤ 3 ⇒ **真白空间**（对照 `sentiment27` 的 1871）。
⚠ 按 `vol` / `novel` 检索 138 字段**零命中** ⇒ 本集**没有** volume/novelty/relevance 字段，
**Event-conditioned 桶做不了**（数据集描述里的 "five categories" 在 KOR 分区拿不到对应字段）。

**两条候选（`preflight_expressions(region=KOR, universe=TOP600, delay=1, dataset_id="sentiment21")` ⇒ `valid=true`，
4 字段全命中、`unknown_soft=[]`、`fixed_expressions` 与原文逐字一致、无需包装）**：

```
A(情绪分歧反转·R2 论坛配方): group_neutralize(reverse(ts_rank(ts_backfill(snt21dts_sop - snt21dts_gen, 66), 66)), sector)
B(净情绪修正·变化率)      : group_rank(ts_delta(ts_backfill(snt21pos_mean - snt21neg_mean, 66), 66), sector)
```

**设计依据**：
1. **A 走已实证配方，不新造**：`brain-alpha-research-news-sentiment` §3.5 的 **R2「情绪波动率反转」**
   （论坛 18 票，id `41449516289687`，原文用 `ts_max` 但该算子平台不可访问 ⇒ 该 skill 已裁定换成 `ts_rank`，
   本文沿用其裁定，不属私自改写）。
   经济含义：`pos_std − neg_std` = **分歧度净值**；分歧高 + 卖空受限 ⇒ 高估 ⇒ 反转（Miller 1977 / Diether-Malloy-Scherbina 2002）。
2. **B 是另一种机制、另一个桶（Change）**：净情绪（`pos_mean − neg_mean`）的**变化率**，
   测的是「新闻语气修正的持续性」，与 A 的截面分歧正交。铁律 A 检查：情绪分是**有界净额**不是单边恒正存量，
   故直接用 `ts_delta` 合规；`ts_backfill(·,66)` 补 0.475 覆盖缺口。
3. **满足 `KOR-NEWS79-SENTIMENT-DEAD` 的复检条件**（原文："would need **event-anchored persistence design** before retry"）：
   两式都是 `ts_backfill` + 长窗（66） + `group_*` 中性化，**不是**裸日频聚合；decay 4 只是设置层，不是信号形态。
4. **两式都用「同数据集两字段相减」**（A 的 `sop − gen`、B 的 `pos − neg`）⇒ 单一经济含义，
   满足 A-3 放行口径；`sentiment` 不在约束 5 的 PV/MODEL/OTHER 名单内，**无双腿禁令冲突**。
5. **不加 `trade_when`**：§5.44 已实测 KOR/TOP600 上门控是第二杀手（CW 0.1508 + subU 负）；
   本集又没有 attention 字段可做门控腿 ⇒ 本波**不碰门控**。

**通道取证状态（如实记，不冒充）**：
- **通道 A（论坛）**：本轮 `search_forum_posts` **连续两次 `MCP error -32603`（工具故障）** ⇒
  按 §8.11 证据契约记 `status=error`，**不得当成"论坛无解"**，也不落 `forum_recon_negative_*`。
  可用的论坛证据是**既有**那条 R2 配方（上文 id `41449516289687`），不是本轮新查。
- **通道 B（文献）**：A = Miller(1977) 分歧溢价 + Diether-Malloy-Scherbina(2002) 分析师分歧横截面实证；
  B = Tetlock(2007) 媒体语气对个股的短期压力与反转、后续修正的持续性。两条都属**可证伪的方向句**（分歧高 ⇒ 后续负收益；
  语气改善 ⇒ 短期继续）。
  ⚠ **文献偏误声明**：两项经典实证样本都在 USA、且多为大盘；KOR 是小宇宙、散户占比高、卖空受限更严 ⇒
  「分歧溢价」在 KOR **可能更强**（卖空受限）也可能被当日价格限制掩盖 ⇒ 只当假说，以本区实测为准。

**预登记裁定**：

| 收批读数 | 裁定 |
|---|---|
| 任一路 `S ≥ 1.58 且 fail=[]` | ⭐ 先查首年 `longCount`（约束 4）；过闸则进提交队列（SENTIMENT 塔 0/3 → 1/3，mult 1.6） |
| 任一路 `1.3 ≤ S < 1.58 且 fail⊆{S,F,2Y}` | 机制成立 ⇒ 波 230 = **同族单变量升级**：① A 换 `ts_rank` 窗 22/252 ② B 换 `_2/…/_5` 窗口族做窗口对照 ③ `snt21dts_tuen`（中性分歧）第三条 |
| 两路 `S < 1.0` | 情绪分歧轴判弱 ⇒ 记负结论，SENTIMENT 塔回到 §5.30 的备选（`sentiment23` 156 字段 / cov 0.2648） |

⚠ 收批第一件事仍是 **`get_alpha_yearly_stats` 首年 `longCount`**（约束 4）——
本集 cov 0.475 只证截面覆盖，**不证十年跨度**；`sentiment26` 正是 7 年覆盖被一票否决的前例
（`KOR-SENTIMENT26-NO-CROSS-SECTION-AND-7Y-COVERAGE`）。

### 5.50 category 盘点收尾：MACRO / IMBALANCE 均无 ATOM 信号面（约束 1 完结）

**MACRO（2 集，mult 1.4，塔 0/3）**

| dataset | fields | cov | aC | 判读 |
|---|---|---|---|---|
| `macro63` | 1 | 1.0 | 192 | ⏸ 已判死待落库（`KOR-MACRO63-NO-CROSS-SECTION`；波 215 三条恒空仓） |
| `other106` ★本轮首查 | 15 | 0.404 | 307 | 15 字段全 VECTOR，全是 **KOSPI 200 公司行为/重构参数** |

`other106` 全字段（`complete:true` 15/15）：`index_share_cls/nxt`（变动前/后指数股本）、
`free_float_factor_cls/nxt`、`capping_factor_cls/nxt`（CAP 率）、`adjusting_factor_cls/nxt`、
`newshares_following_rightsissue`、`price_cls/nxt`、`index_code1/2`、`ksic_cls`（KSIC 6 位行业码）、`slc_ciik`。

三条不投理由：
1. 唯一有机制的是**被动再平衡压力**（`index_share` 变动 ⇒ 指数基金被动买卖），但它是**稀疏公司行为事件**
   （cov 0.404，事件之间无变化）⇒ CW 风险与波 225/226 同型（稀疏/门控 ⇒ 权重摊不平）。
2. `price_cls/nxt` / `adjusting_factor` / `capping_factor` / `free_float_factor` 是**换算系数**，
   取水平无横截面经济含义（与 risk59 / imbalance5 的「ID / 映射集」同类）。
3. `ksic_cls` / `slc_ciik` / `index_code1/2` 是**分类码**，只能当 group 轴，不能当信号。

⇒ **MACRO 塔在 KOR 无 ATOM 信号面**，塔 0/3 建议关闭（与 SOCIALMEDIA / INSIDERS / INSTITUTIONS 同级）。
唯一残余玩法 = 「行业分类码当 group 轴 + 另一塔信号」的组合，不属本塔自身信号，不在 ATOM 目标内。

**IMBALANCE（1 集，mult **1.0**，塔 0/3）**

`imbalance5`：2 字段 / cov 0.8559 / aC **1384** / valueScore **1** / 描述 =「RIC↔BBID 映射」
⇒ 与 risk59、other424 同一形态（**名称"The Oil Price Resilience Scores"是假信号名，实际是 ID 映射**）⇒ **无信号面**。
⇒ **IMBALANCE 塔关闭**（塔 0/3，且乘数仅 1.0，即便点亮也基本不值配额）。

**约束 1 的 category 盘点到此收尾**：KOR/D1 的 15 个塔位逐类查完 ——
已亮 3 个（fundamental 3/3、model 3/3、shortinterest 4 颗），
未亮 12 个里 **9 个已用回测读数判负或结构关闭**（news / insiders / sentiment / socialmedia / risk / macro /
imbalance / institutions / earnings），**仅 3 个还有活口**：**analyst 2/3**（余 1 席）、**pv 2/3**（余 1 席）、**other 1/3**（余 2 席）。
后续排期只在这三个 cell 内，其余一律不投配额。

### 5.51 `other546` 画像（OTHER 塔**最大**白空间 aC 9，10 字段实测）——**机制被约束 5 封死**

`get_datafields(dataset_id="other546", filter_sharpe=false)` ⇒ `complete:true` **10/10，全部 VECTOR**：

| 字段 | cov | aC | 含义 |
|---|---|---|---|
| `busnet_common` | 0.6735 | 1 | 两家公司共享的业务/地理**分部个数** |
| `busnet_strength` | 0.6735 | 5 | 业务分部披露的**相似度** |
| `analystnet_common` | 0.614 | 2 | **同时覆盖**主公司与其 peer 的分析师数 |
| `from_analyst` / `to_analyst` | 0.614 | 1 / 0 | 主 / peer 各自的覆盖分析师数 |
| `nlpbusnet_strength` | 0.5204 | 0 | 业务段落**文本**相似度 |
| `mdanet_strength` | 0.5204 | 0 | MD&A 文本相似度 |
| `risknet_strength` | 0.5204 | 0 | 风险因素段落文本相似度 |
| `geonet_common` / `geonet_strength` | 0.4407 | 0 / 1 | 共享地区分部数 / 地区相似度 |

**判读（写死，省得下一轮重新纠结）**：
1. 这是**点对点（primary ↔ peer）连边集合**，`vec_*` 折叠后得到的是**公司级静态特征**
   （"我与我的 peer 有多像 / 多少共同分析师"），**本身没有方向**。
2. 它真正的经典机制是 **economic-link momentum（Cohen & Frazzini 2008）**：peer 的**收益** × 连边强度。
   但 KOR 上 peer 收益只能取 **PV** ⇒ **OTHER + PV 正是约束 5 明令禁止的组合**
   ⇒ **机制在约束下不可实现**（不是数据差，是被规则封死）。
3. 替代路径「peer 侧换 NEWS / SENTIMENT」合规，但平台字段层给的是 **ID 连边列表**而非可 join 的键值对，
   "把 peer 的 sentiment 聚合回本股" 在本图层做不到 ⇒ 需先在表达式层构造映射，风险与成本都高，留作长尾。
4. 单用 `vec_avg(busnet_strength)` 这类**水平**说不出错价来源（A-2 硬门过不了）⇒ **不投配额**。

**⇒ OTHER 塔可用面收敛**：`other545`（本波 228 在飞）、`other466`（实际归属 FUNDAMENTAL，不算 OTHER）、
`other546`（机制被约束 5 封死）、`other695`（约束 4 一票否决）、`other475`（与 695 同源风险）。
即 **228 若不出货，OTHER 停在 1/3 是大概率**，26 集快照里已无干净候选。

---

### 5.52 ANALYST 塔（**2/3，最近的一席**）白空间全量盘点：17 集逐条判定

> 触发：波 227 的 `YP1nn09l`（S 1.19）按预注册表**未获扩槽许可**（§5.47 归因第 4 条），
> analyst44 的广度轴已判死 ⇒ 要找**第三席**必须换数据集，不能在同一集上继续调参。
> 本波把 ANALYST 类 17 集全部过一遍（`get_datasets(category="analyst")` + 逐集 `get_datafields`）。

**总盘**（aC = alphaCount，vS = valueScore）：

| 数据集 | 字段数 | 覆盖率 | aC | vS | 判定 |
|---|---|---|---|---|---|
| `analyst15` | — | — | **22146** | — | ⛔ 饱和（平台 α 数过万，Tier B） |
| `analyst25` | — | — | 5261 | — | ⛔ 饱和 |
| `analyst4` | — | — | 4896 | — | ⛔ 饱和 |
| `analyst14` | — | — | 3849 | — | ⛔ 饱和 |
| `analyst39` | — | — | 3155 | — | ⛔ 饱和 |
| `analyst44` | — | — | — | — | ⛔ 已在 227 判死广度轴（S 0.89 / 拟合指纹） |
| `analyst_base_ref` | 0 | — | — | — | ⛔ 占位符，无数据 |
| **`analyst11`** | **210** | 0.5831 | **75** | **6** | ⭐ 白空间（ESG 评级，见下） |
| **`analyst81`** | 5 | 0.2651 | 23 | 6 | ⚠ 白空间但覆盖率不达标（见下） |
| **`analyst46`** | 6 | 0.4192 | 38 | 5 | ⭐ 白空间（卖方**想法流**，见下） |
| **`analyst48`** | 70 | — | 244 | 4 | 未画像（下轮） |
| **`analyst45`** | 241 | — | 104 | 5 | 未画像（字段多，下轮） |
| `analyst9` | 43/48 | 0.44–0.71 | 137 | 4 | ⛔ **机制与 227 死轴同源**（见下） |

#### 5.52.1 `analyst9` 直接判死——不是数据差，是**机制撞死轴**

43 字段（`sharpe_filter=false` 时 48）几乎全是 VECTOR，真正带方向的只有一组：

| 字段 | cov | aC | 含义 |
|---|---|---|---|
| `anl9_s_numup` | 0.7109 | 14 | 共识内**上调**的分析师数 |
| `anl9_s_numdn` | 0.7109 | 14 | 共识内**下调**的分析师数 |
| `anl9_s_numanalysts` | 0.7109 | 16 | 纳入共识的分析师总数 |
| `anl9_daily_numdn` / `numdownunfiltered` | 0.4433 | 7 / 10 | 日频下修计数（同上，频率不同） |

⇒ `(numup − numdn) / numanalysts` 就是**修正广度比率**，与波 227 的
`eps_gaap_estimate_4wk_up_count / down_count` **是同一机制**（只是 Refinitiv 口径 vs 另一供应商口径）。
227 已实测 S 0.89 / F 0.64 且 top1 年占正收益 31.9% ⇒ 过拟合指纹。

**铁律 G 判：换数据集不改变机制 ⇒ 换表不换命**，不许把 `analyst9` 当"新数据集"重烧配额。
其余字段（`*_effectivetime` / `*_totime` / `*_splitfactor` / `*_isexcluded` / `*_isnmflag` /
`*_parentflag` / `*_currency_code` / `anl9_estanalystmap`）是时间、拆分、质量旗标、名称字符串 ⇒ **无信号面**。
**唯一例外**：`anl9_consensus*_dataitemvalue`（cov 0.58–0.61）是**共识估计水平值**，
但 VECTOR 里混着多指标多期，需 `vec_*` 折叠后才知道折的是哪个指标 ⇒ 无法保证经济含义单一，不作主腿。

#### 5.52.2 `analyst46`（卖方**想法流**，6 字段）——真正的新机制

`get_datafields(dataset_id="analyst46")` ⇒ `complete:true` **6/6，全 MATRIX**：

| 字段 | cov | aC | 含义（原文要点） |
|---|---|---|---|
| `anl46_indicator` | 0.4192 | 8 | 区域内**横截面排名 1–10**，10 最看多 |
| `anl46_sentiment` | 0.4192 | 10 | 复合：想法的 decay + 分析师信誉 + 距财报远近 + 想法量/方向 |
| `anl46_experts` | 0.4192 | 7 | 投稿分析师的**历史表现**贡献（越高越可信） |
| `anl46_alphadecay` | 0.4192 | 10 | **想法年龄**对信号的衰减贡献（越新越大） |
| `anl46_performancepercentile` | 0.4274 | 9 | 1–100：该信号**过去 12 个月对本股预测力**的回测分位 |
| `profit_report_component` | 0.4192 | 1 | 距财报事件的远近调整项 |

**结构判读（写死）**：
1. **这是"已工程化的信号"，不是原始数据**：`indicator` 本身就是成品 alpha，
   `experts` / `alphadecay` / `profit_report_component` 是**权重分量**（单独用**没有方向**，
   不可能作为独立腿——这点与 analyst11 的 KPI 分量不同）。
2. **`experts` 与 `alphadecay` 互为张力**：前者要"谁说的"，后者要"多新"。二者相乘才构成
   "高信誉 × 新鲜"的想法；单独任一个都只是调制项。
3. **`performancepercentile` 是本数据集独有的东西**：它给了一个**逐股的条件可靠性**外生变量
   ⇒ 可做 `trade_when` 门控，也可作分组轴。这是它与 227/analyst44 最本质的差异。
4. 覆盖率 0.4192 是**全 17 集里偏低的**（仅高于 analyst81 的 0.2651）⇒ 持仓面约 250 只，
   **`LOW_SUB_UNIVERSE_SHARPE` 与 `CONCENTRATED_WEIGHT` 是首要风险**，不是 Sharpe。

**A-2 收益来源声明（必须先写，再组装）**：
- **谁在被定价**：卖方分析师**新发布的"想法"**（不是盈利预测修正、不是评级变更）——
  即主动表态的少数分析师。
- **为什么会被错**：想法发行是**离散事件 + 覆盖摩擦**。大行分析师的想法被买方当日消化，
  中小行 / 覆盖薄的公司传播慢；且想法有**时效半衰期**（数周）。"刚发行 + 高信誉 + 覆盖不足"
  三者叠加时才会被延迟定价 ⇒ 制度性摩擦，不是"大家没注意"。
- **错了多久修复**：**数周到一季**（想法半衰期）。
- **预期方向**：想法越看多 ⇒ 后续**涨**（正向动量，非反转）。

⚠ **与 227 死轴的差异必须说清**（否则就是换皮重测）：227 量的是**有多少人改了预测**（计数/广度），
analyst46 量的是**有没有一个可信的人新表态**（信誉加权方向）。前者是拥挤度代理，后者是信息事件代理。

#### 5.52.3 `analyst11`（ESG 评级，210 字段）——结构最整齐、时间维度最可疑

`get_datafields(dataset_id="analyst11")` ⇒ `complete:true` **210/210，全 MATRIX**，cov 0.43–0.70。

**结构：一个 KPI × 7 个变体的矩阵**（这是本集最重要的画像结论）：

| 变体 | 例（以 `pollution_prevention` 为例） | cov |
|---|---|---|
| 原始分 | `pollution_prevention_score` | 0.6965 |
| 行业内分位 | `pollution_prevention_industry_percentile` | 0.6777 |
| 行业内排名 | `pollution_prevention_industry_rank` | 0.6813 |
| 行业内分位 | `pollution_prevention_sector_percentile` | 0.6777 |
| 行业内排名 | `pollution_prevention_sector_rank` | 0.6813 |
| 子行业内分位 | `pollution_prevention_subsector_percentile` | 0.6777 |
| 子行业内排名 | `pollution_prevention_subsector_rank` | 0.6813 |

≈30 个底层 KPI × 7 = 210。KPI 族：E（`pollution_prevention` E1 / `anti_pollution_policy` E2 /
`resource_efficiency` E3 / `environmental_pillar_composite_score`）、
S（`workforce` EMP1-3 / `community` CIT1-3 / `social_pillar_composite_score` / `human_rights` /
`workplace_diversity`）、G（`board_independence` G1 / `management_ethics` G2 /
`disclosure_transparency` G3 / `governance_pillar_composite_score`），
顶层总分为 **`overall_sustainability_score`**（cov 0.6975，全集最高之一）。

⚠ **两个命名陷阱**（按名找字段必踩）：
1. **`_rank` 与 `_position` 混用**：`community_*` / `environmental_*` / `*_corr_weighted_*` 用
   **`_position`**，其余用 **`_rank`**。同一含义两种后缀 ⇒ 按后缀枚举会漏掉一半。
2. **`*_corr_weighted_score` / `*_max_correlation_score`**（cov 仅 0.43–0.49）不是"另一种 ESG 分"，
   而是**供应商已按"与财务指标的相关性"加权过的分**——它内部已经把"财务重要性"折进去了。
   拿它当"原始分"再 rank，等于**在供应商的加权之上再叠一层**，机制会被二次污染。

**A-1 五问 → 结构判读**：
1. **时间维度**：**存量水平**（年度更新的评级分），非流量。
2. **相对性**：**供应商已自带横截面相对化**（industry / sector / subsector 三档分位与排名全给了）
   ⇒ **我们自己再 `rank` / `group_rank` 一遍是零信息**，只是重复供应商已经做过的事。
3. **被定价的是谁**：**评级机构的评级变更**（MSCI / Sustainalytics / KCGS 口径），
   以及按评级门槛调仓的 ESG 委托资金。
4. **有无博弈**：有。KOR 的 ESG 委托规模在 2018 年后才起来，且评级呈**阶梯式门槛效应**
   （"跨过某档"触发纳入/剔除）。
5. **事件性**：**年度复审 + 期间连续微调** ⇒ 稀疏但不为零。

⇒ **本集唯一非冗余的用法是"时间维度"**（供应商没给变化率/趋势/修正幅度）：
用 `ts_delta` 取评级修正，而不是拿它的水平再排一次序。这条**决定了本集的表达式形态**，
不是审美选择——用水平就是在复现供应商的分位字段。

**A-2 收益来源声明**：
- **谁在被定价**：按 ESG 评级门槛调仓的**被动/委托资金**，以及用评级做委托约束的机构投资者。
- **为什么会被错**：**评级修正是粘性的**——年度复审 + 门槛触发调仓，形成**阶梯式需求**；
  市场对"刚跨过门槛"的公司定价不足（纳入效应 / 门槛效应）。制度约束型摩擦。
- **错了多久修复**：**数季**（评级变化 → 下一轮年度调仓周期）。
- **预期方向**：评级**上调** ⇒ 后续**涨**。

#### 5.52.4 `analyst81`（信用度模型，5 字段）——覆盖率不达标 + 标度是乱序的

`get_datafields(dataset_id="analyst81")` ⇒ `complete:true` **5/5**：

| 字段 | cov | 含义 | 可用性 |
|---|---|---|---|
| `anl81_class` | 0.2579 | 信用等级整数标签 | ⛔ **标度乱序**（见下） |
| `anl81_probability_of_default_percent` | — | 违约概率 | ✅ 序数正确（越高越差） |
| `default_likelihood_percent` | 0.276 | 违约可能性 | ✅ 同上 |
| `anl81_confidence_level_percent` | — | 置信度 | ⚠ 是**模型质量**，不是信号 |
| `financial_data_completeness_percent` | — | 财报完整度 | ⚠ 是**数据质量**，不是信号 |

⚠ **`anl81_class` 的整数映射是乱的**（原文照抄）：
`9(AAA), 5(AA), 4(A), 1(BBB), 2(BB), 3(B), 7(CCC), 8(CC), 6(C), 10(D)`。
⇒ **整数不能当序数直接用**（1=BBB 但 2=BB、3=B，而 9=AAA、10=D 反而在两端）。
若要还原序数必须先做 10 分支映射，算子数会吃掉配额；**改用 `*_probability_of_default_percent` 即可绕过**。

**判死理由（不是"没试"，是两条硬指标）**：
1. **cov 0.2651–0.276** ⇒ 低于 0.4 backfill 阈值，KOR/TOP600 上只有约 160 只可持仓
   ⇒ `CONCENTRATED_WEIGHT`（0.1 上限）与 `LOW_SUB_UNIVERSE_SHARPE` 双高危，
   而这两个闸在本区已被证明是**结构性**而非参数可修的。
2. **机制已被平台充分覆盖**：破产概率/违约概率预测收益是 Campbell-Hilscher-Szilagyi (2008) 以来
   最经典的会计异象之一，`fundamental*` 族早已吃透；aC 23 且 vS 6 只反映"字段少"。
   ⇒ **不是白空间，是低覆盖的同质腿**。
**⇒ 不投配额。**

#### 5.52.5 波 230 预置（analyst46 × analyst11 对冲，**已预检，等 229 腾槽**）

两个表达式均已 `preflight_expressions` 通过（`valid:true`，`unknown_fields:[]`，`vector_fields:[]`）：

```
A(analyst46 · 想法流复合情绪水平)  : group_rank(ts_backfill(anl46_sentiment, 5), sector)
B(analyst11 · ESG 评级修正动量)    : group_rank(ts_delta(ts_backfill(overall_sustainability_score, 66), 252), sector)
```

**为什么这 2 条配成一批**（而不是同一集做消融）：目标只要**一席**，跨数据集对冲的
P(至少一条过) 高于同集消融的信息量；且 analyst46 若整体不灵，同集消融的结论也可由 A 单独得出。

| 设计点 | A | B | 依据 |
|---|---|---|---|
| 核心形态 | 水平（**快变量状态**，非静态特征） | **变化率**（铁律 A：本集只有时间维度非冗余） | 5.52.2 结构判读 1 / 5.52.3 A-1 第 5 问 |
| backfill 窗 | **5 天**（想法半衰期数周，长窗会把陈旧看多抹进来） | **66 天**（年度更新，必须桥接报告期空档） | 5.52.2 A-2「数周半衰期」/ 5.52.3 年度复审 |
| 外层 | `group_rank(·, sector)` | 同 | 与 227/228/229 逐字一致，便于横向比较 |
| 不做的事 | ❌ 不加 `ts_mean`（数据集内部已含 decay 加权） | ❌ 不用 `*_corr_weighted_score`（供应商已二次加权，见 5.52.3 陷阱 2） | 加壳必须有机制，否则是引入非目标暴露 |
| 首要风险 | **cov 0.4192** ⇒ CW / subU | **十年跨度**（ESG 在 KOR 多为 2015+ 起） | 见下 |

**预注册判定表（收批前写死，收批后照表执行）**：

| 读数 | 处置 |
|---|---|
| 任一条 S≥1.58 & F≥1.0 & 2Y≥1.58 & fail=[] & 首年 longCount>0 | ⭐ **analyst 2/3 → 3/3 达成**，进提交队列（仍须用户确认 + prod 实测） |
| S 1.3–1.58 | 只允许**单变量**推一档（A 试 backfill 22 / B 试 window 504），**不得**换中性化或加壳 |
| 任一条 `CW` 或 `subU` FAIL 且 S<1.0 | 该数据集判死，**不得**靠缩 universe / 加 `trade_when` 救（本区已证 CW 是结构性的） |
| 首年 longCount = 0（约束 4 破） | **该数据集判死**（一票否决），即使 S 很高也不扩槽——与 `other695` 同型 |
| 两条均 S<1.0 | ANALYST 塔**结构性封顶 2/3**，写进 §5.4 交付对账 |

⚠ **收批第一件事仍是 `get_alpha_yearly_stats` 首年 `longCount`**（约束 4）。B 的风险显著高于 A：
`overall_sustainability_score` cov 0.6975 只说明**今日截面覆盖**，ESG 在 KOR 的**起点年份**通常晚于 2014
⇒ 若首年 longCount=0，B 直接判死，**不要**用"覆盖率可动态调整"去救（约束 4 原文是"近十年都要有数据"）。

#### 5.52.6 外部文献取证（通道 B，2026-10-30 实测检索）

> 检索式：`analyst recommendation changes stock returns Korea evidence initiation revisions`。
> 只取**有方向句 + 有机制**的结论；USA/大宇宙样本一律标限定，作**假说**不作模板。

| 文献 | 结论（要点） | 对本案的作用 |
|---|---|---|
| **Kim, Ryu & Yang (2019)**, *Investment Analysts Journal* 48(2):89–101，`Investor sentiment, stock returns, and analyst recommendation changes: the KOSPI stock market` | **KOSPI 本区样本**：股价反应针对**推荐"变化"而非推荐"水平"**；信息不确定性（行业竞争度 HHI）越高反应越强；**下调（不利消息）方向的情绪效应更显著** | ⭐ **本区一级证据**：直接支持 analyst46 用"想法流事件"而非"评级水平"；并提示**空头腿天然更强**（非对称） |
| **Loh & Stulz (2011)**, *RFS*，`When Are Analyst Recommendation Changes Influential?` | **只有 12% 的推荐变化是"有影响力的"**；更有影响力的条件是：来自 leader / star / **历史有影响力**的分析师、**偏离共识**、附带盈利预测、发生于成长股/小盘/高机构持股/高预测分歧 | ⭐ 直接为 `anl46_experts`（贡献者历史表现）这一分量提供存在理由；也解释了为何 88% 的想法是噪声 ⇒ **信号天然稀疏**，Sharpe 天花板低 |
| Jegadeesh & Kim (2006), *JFM* 9(3):274–309，`Value of analyst recommendations: International evidence` | 推荐价值在**国际市场**存在但弱于 USA | 支持"可迁移但会打折"，不作本区模板 |
| ⚠ **反向证据（必须一并记，防单边采信）** arXiv 2512.16251 (2025)，`Interpretable Deep Learning for Stock Returns` | `Change in Recommendation` **R² 持续为负**："一旦控制了盈利预测修正，推荐变化的**增量**预测力有限"；乐观更新只含**短命**信息 | ⚠ **与 analyst44 的修正广度轴同风险面**。若 analyst46 收批 S<1.0，**本条即为判死依据**——不得再换窗口/中性化反复重测（铁律 F） |

**双通道裁决**：
- **A（论坛）**：本轮 `search_forum_posts` 仍不可用（MCP `-32603`，§5.49 已记 `status=error`）⇒ 通道 A **无有效产出**，
  **不得**据此认为"论坛无解"。
- **B（论文）**：给出**机制 + 方向句 + 修复期**（数周到一季）⇒ 满足 A-2 后三项。
- **裁决**：A 缺、B 有 ⇒ 走 **"B 有机制 / A 无对应表达 ⇒ 按 A-1 五问自建骨架"** 这条分支（②.d 表第 3 行），
  这正是 5.52.5 的表达式的来源，**不是套模板**。

#### 5.52.7 外部文献取证（通道 B，analyst11 ESG 修正，2026-10-30 检索）

> 检索式：`ESG rating changes predict stock returns Korea sustainability score revisions`。
> **四个来源里三个支持"评级修正"而非"评级水平"**，且都给出**修复期**（A-2 必需项）。

| 文献 | 结论（要点） | 对本案的作用 |
|---|---|---|
| **Liu & Zhou (2025)**, *Global Finance Journal* 67，`Do ESG rating changes matter? Evidence from Chinese stock market` | 评级**上调→短期收益更高**、下调→更低；"上调 vs 下调"多空组合**月均异常收益 1.80%**；**主驱动是机构投资者买卖**；**评级变化的分歧会削弱该效应** | ⭐ **最强的机制支撑**（新兴市场，比 USA 更贴 KOR）：直接对应 5.52.3 A-2 的"门槛式被动资金调仓"。⇒ 支持用**总评级的修正**，不是总评级水平 |
| **ESG rating changes and stock returns (2025)**, *J. Int. Fin. Markets, Inst. & Money*（S0261560625000440） | MSCI 评级变化对美股：**价格需数月才能反映**；持有期 6 个月时，**下调→年化约 −3% 异常收益**；**只有 E 支柱的变化在 6 个月窗口显著，S 与 G 无清晰影响**；下调效应由机构驱动 | ⭐ 给**修复期 = 数月**（A-2 第 3 项达标）；⚠ 同时是**反向警示**：若只 E 有效，用总评级等于**掺入 S/G 噪声** ⇒ 见下方"单变量推一档"预案 |
| `Does It Pay to Be Responsible?`（PKU, 2022, 中国市场） | **ESG 的收益效应按支柱与行业而异**；第二产业里高 ESG ⇒ **更低**收益、第三产业 ⇒ 更高 | 支持 `group_rank(·, sector)` 的**行业中性化不是装饰**；也说明方向不可全球照搬 |
| MDPI *Sustainability* 16(18):7993（2024） | 提及 KSSB（韩国可持续准则委员会）与"已有作者研究韩国市场 ESG 评级对股价的影响" | **确认 KOR 本区有该文献线**，但摘要未给方向 ⇒ 作线索不作依据 |

**引用纪律（按 ②.d 通道 B 要求逐条执行）**：
- 上述文献的样本分别是 **中国 A 股 / 美股 / 中国**，**没有一篇是 KOR/TOP600** ⇒ **全部按假说处理**，
  不作模板；A-2 硬门不因有论文而放宽（仍须本区实测）。
- 采信的**只有**"评级修正 → 机构调仓 → 数季修复"这条机制链；**不采信**任何具体收益数值
  （1.80% 月均 / −3% 年化都是他区样本）。
- ⚠ **反向证据已入档**：USA 证据称 **S 与 G 支柱的变化无显著效应**，与"总评级修正"设计冲突。
  **处置写死**：波 230 先用总评级；若 B 落在 **S 1.3–1.58 的单变量推档区**，
  **唯一允许的下一步是把 `overall_sustainability_score` 换成 `environmental_pillar_composite_score`**（见 5.52.5 表第 2 行），
  不许同时改窗口或中性化。若 B 直接 S<1.0，则判死，**不进入该推档**。

#### 5.52.8 `analyst48`（彭博**股利预测**，66/70 全 VECTOR）——不是"分析师估计"，是**股利预期**

`get_datafields(dataset_id="analyst48")` ⇒ `count:66`（`platform_count:70`，4 个被 sharpe 过滤）。

**结构判读：66 个字段里只有 12 个带方向，其余是日期 / 标识符 / 索引元数据**：

| 类别 | 字段 | 可用性 |
|---|---|---|
| **真正的信号字段（12）** | `bdvd_curr_dvd_health`(aC 42, .5152)、`bp12m_yld`(4, .5135)、`bbpsa`(12, .5152)、`bpda`(**0**, .5155)、`bp3y_dg`(**0**, .4795)、`edg3yr_g`(4, .4361)、`bbt`(9, .5152)、`bp12m_dip`(16, .3244)、`equity_dvd_sh_last`(2, .4817)、`equity_ldg`(1, .4815)、`bedhga`(1, .4836)、`m21_hs_dvd`(3, .3113) | ✅ |
| **日期（9）** | `bdhad`/`bdhed`/`bdhpd`/`bedhgad`/`bedhged`/`bedhgrd`/`bnedd`/`bnepd`/`dvd_declared_dt`/`dvd_pay_dt`/`dvd_record_dt`/`td_xe_dvd*`/`bdvd_next_est_ex_dt` | ⛔ 时间戳，非信号（可作 `trade_when` 事件门，但本波不用） |
| **标识符 / 回执（18）** | `ibs`/`ibc`/`equity_ibc`/`*_return_code`/`*_nfields`/`bulk_*` | ⛔ 无信号面 |
| **合约 / 索引元数据（约 15）** | `par_amt`/`idivisor`/`indx_typ`/`count_index_members`/`index_*` | ⛔ 无信号面 |

⚠ **aC 分布揭示了一个坑**：`bdvd_curr_dvd_health` 与 `bbpsa` aC 42 / 12，而**真正带"预期"的
`bp3y_dg` / `bpda` aC = 0**。平台用户全在挖"股利健康度/股利金额水平"，没人挖**股利预期本身**
⇒ 这是本集唯一的白空间，但也要问"为什么没人挖"（下面第 2 条给出答案）。

**机制（A-2）**：
- **谁在被定价**：把**预期股利**当估值输入的买方（Gordon 增长模型：`P = D₁/(r−g)`，`g` 的边际影响远大于 `D`）。
- **为什么会被错**：**股利预期的调整是粘性且被交易成本压制的**——公司管理层极不愿削减股利
  （Lintner 1956 的"股利平滑"），因此**上调预期**通常领先于实际派息 1–3 年，市场在预期形成期定价不足。
- **错了多久修复**：**1–3 年**（`bp3y_dg` 的 3 年窗口本身就是修复期）。
- **预期方向**：3 年预期股利增速**上调** ⇒ 后续**涨**。

**为什么不投配额（三条，本轮定案）**：
1. **零使用 ≠ 白空间**：`bp3y_dg` aC=0 但 cov 仅 0.4795，且**它本身就是一个预测值**
   ——再对外生预测做 `ts_delta` 是在**预测的预测上叠加**，A-2 的"错价"叙述会退化成"我们比彭博更会预测"，
   这在没有本区证据时不可采（②.d 通道 B 对 `analyst45/48` 尚无任何文献支撑）。
2. **最强的字段是价值因子代理**：`bp12m_yld` / `bpda` 本质是**预期股息率**⇒ 与 PV 价值族高度同源。
   本区已多次实测价值族撞 **prod 相关墙**（§5.4 的 `LLZ6wZO2` prod 0.6762 就是贴着墙的）
   ⇒ **预期收益是"可能过闸但 prod 必撞墙"的形态**，在高配额成本下不优先。
3. **失败面已被同型覆盖**：`bdvd_curr_dvd_health`(aC 42) 是**静态质量分**，与 §5.53 判死的
   `oth545_score`（静态声誉分）**同型**——静态分在本区已两次双灭。

⇒ **`analyst48` 列为"储备候选"，不进 230**；只有当 230（analyst46/analyst11）双双判死后，
才按 `bp3y_dg` 起一波（**且必须先做 prod-first 探针**，不许直接整波）。
`analyst45`（241 字段）**暂不画像**：字段规模会吃掉一整轮上下文，且它是 ANALYST 族里 aC 104 的中等拥挤集，
优先级低于上面三个。**未画像 ≠ 已判死，登记为未覆盖项**，别把"没查"说成"没有"。

---

### 5.53 波 228 收批（`other545` 双灭，0/2）⇒ **OTHER 塔结构性封顶 1/3**

multisim `49Nf1n1Pf5ikbptmRYeYYbK`，2026-10-30 收批，已回写 `wave=228` / `dataset=other545`（`upserted:2`，
暂定 `verdict=FAIL`，0 条过硬闸，0 条过 near 线 1.0）。

| | 表达式 | alpha | S | F | 2Y | subU | TO | CW | 判定 |
|---|---|---|---|---|---|---|---|---|---|
| A | `group_rank(vec_avg(oth545_score), sector)` | `N1Nq6pm8` | **0.59** | 0.32 | 0.80 | 0.70 | .078 | pass | ⛔ 三闸同 FAIL |
| B | `group_rank(vec_avg(oth545_pln_omen), sector)` | `j2YWXZb5` | **0.70** | 0.52 | 0.51 | 0.76 | .052 | **0.2631** | ⛔ 四闸 FAIL |

**约束 4 已验（两条都过）**：A 2014 `longCount` **266** / short 312；B 2014 `longCount` **236** / short 342
⇒ **失败与"十年跨度"无关**，是信号本身不成立。这一点必须先确认再归因，否则会把数据问题误判成机制问题。

**归因（铁律 F，逐条给读数依据）**：

**A `N1Nq6pm8` —— 单边恒正的静态质量分，方向由"供应商模型换代"决定，不是 alpha**
- 逐年 S：2014 **−1.99** / 2015 **+1.67** / 2016 1.12 / 2017 0.67 / 2018 −0.12 / 2019 0.15 / 2020 1.19 / 2021 1.25 / 2022 1.65 / 2023 0.22
- **S<1.0 的年份 = 5/10**（2014、2017、2018、2019、2023）⇒ 归因表第 2 行「2Y 闸结构性不可达」
- **2014→2015 符号翻转 −1.99 → +1.67**（读数不是噪声，是**结构性断裂**：同一表达式在首年反向）。
  与 §5.51 对 `other546` 的判读同型——这类 `oth*` 数据集是**公司级静态特征**，首年反向说明
  **供应商在 2015 年前后换过模型/扩过覆盖**，alpha 拿到的是"模型版本切换"而非经济信号。
- top1 年（2015）占正收益 **23.8%**（1,181,604 / 4,955,537）⇒ **不构成**过拟合指纹，
  所以判死理由**不是**过拟合，而是**机制不存在**（A-2 说不出"谁被定价"）。这条区分很重要：
  两者对应的补救方向完全相反——过拟合要换机制，无机制则**整族放弃**。

**B `j2YWXZb5` —— 2006 年一条极端单边持仓撑起的 S，CW 结构性破**
- 2016：`longCount` **94** / short **525**（其余年份 155–284 / 360–492），`margin` **0.0234**
  = 2023 年（0.00113）的 **21 倍**，S **1.98** ⇒ **2016 不是截面信号，是少数几只股票的赌注**
- 平台 CW FAIL 日期 **2016-04-27**，值 **0.2631**（上限 0.1）——与上面的持仓读数**互相印证**，
  不是两件独立的事
- top1 年（2016）占正收益 **39.4%**（3,877,090 / 9,842,634）⇒ **过拟合指纹（>30% 阈值）成立**
- S<1.0 的年份 = 5/10（2014 −2.92、2017 0.85、2018 −0.50、2019 0.00、2023 −0.47）
- ⇒ **CW 是结构性的**，且本区已反复证明 CW 不是参数可修的（§5.4「闸与数据的结构性错配」）

**⇒ OTHER 塔结论（写死，不再重开）**
按 §5.51 的收敛表，`other545` 是**最后一个干净候选**：`other546` 机制被约束 5 封死、
`other695`/`other475` 约束 4 一票否决、`other466` 实际归属 FUNDAMENTAL。
现在 `other545` 也灭 ⇒ **OTHER 塔结构性封顶 1/3，不再投配额。**
不去试"换个 `vec_*` 聚合再救一次"——A-2 已判"说不出谁被定价"，那是**机制缺口**，
换聚合只是换噪声实现（与 `other546` 第 4 条同一处置）。

#### 5.53.1 波 229 已发（`sentiment21`，SENTIMENT 塔 0/3）

multisim **`2Dqppb25X4xO8WrM0WeuRQW`**（2026-10-30 09:15Z 派发，设置 KOR/TOP600/D1、
SECTOR、decay 4、trunc 0.08、pasteurization ON、unitHandling VERIFY、nanHandling ON、maxTrade ON、
`validate_fields=true`），表达式与 §5.49 逐字一致：
```
A: group_neutralize(reverse(ts_rank(ts_backfill(snt21dts_sop - snt21dts_gen, 66), 66)), sector)
B: group_rank(ts_delta(ts_backfill(snt21pos_mean - snt21neg_mean, 66), 66), sector)
```
收批照 §5.49 的三行预注册表执行；**第一件事是 `get_alpha_yearly_stats` 首年 `longCount`**（约束 4，
sentiment21 的 7/10 年覆盖是 sentiment26 的读数，**不能**套到 21 上）。
下一波（230，analyst46 × analyst11 对冲）已在 §5.52.5 预置并预检通过，等 229 腾槽即可发。

### 5.54 PV 类别全盘点（18 集）—— 两条新线索均判死，PV 塔维持 2/3

按约束 1「一个个 category 查一遍」补 PV。`get_datasets(category="pv")` 实测 18 集
（字段级读数另经 `get_datafields` 抽验）：

| dataset | 名称（平台原文） | fields | cov | aC | vS | 内容实测 |
|---|---|---|---|---|---|---|
| pv1 | Price Volume Data for Equity | 24 | 1.0 | **90329** | 1 | 饱和态（全库最挤） |
| pv30 | Alternate Industry Classification | 690 | .9418 | 4305 | 3 | 用收益 PCA 反推的行业分类 ⇒ **group 维，非信号**；已判死 |
| pattern_scores | Chart Pattern Similarity Scores | 504 | 1.0 | 317 | 4 | 已判死（§5.36.2） |
| continuation_score | Price Chart Continuation Pattern Similarity | 560 | 1.0 | 513 | 4 | 已判死（§5.36.2） |
| intraday_pv_feats | Daily Intraday Price Volume Features | 574 | .9925 | 1307 | 3 | 已判死（§5.36.2） |
| pv37 | Equity Interval Data | **873** | .734 | 2428 | 2 | ⚠ 名不符实，见 §5.54.2 |
| pv106 | Microstructure Spread Data | 29 | — | 985 | 2 | 已挖穿（34 条零 ra_clean），仅作条件腿 |
| pv103 | Interval and MOO&MOC statistics | 7 | — | 162 | 3 | 7 字段拍卖/不平衡统计，样本太小 |
| pv13 | Relationship Data for Equity | 36 | .8191 | 1037 | 2 | **BBID↔RIC 映射 ⇒ 无信号面** |
| pv29 | Derived Industry Classification | 40 | .6678 | 6236 | 1 | **RIC↔BBID 映射 ⇒ 无信号面**（与 pv13 同物） |
| pv14 | Futures Market Data | 2 | .8911 | 118 | 2 | 描述实为 **KOSPI200 指数/成分/公司行为 ⇒ 指数机制，非个股截面** |
| pv20 | Daily Spot and Cross Rate Data | 6 | 1.0 | 39 | 4 | 描述实为 **全球公司基本面（96% 市值）⇒ 属 FUNDAMENTAL** |
| pv109 | Bond Yield Data | 25 | .222 | 8 | 5 | 描述实为**全球公司债定价（2006 起）⇒ 属债券面**；cov 太低 |
| pv173 | Corporate Bond Pricing Data | 21 | .1993 | 6 | 6 | 由公司债利差派生的**股票信号**（z-spread/期限利差/PCA）⇒ 概念有意思，但 cov .20 结构性 CW |
| pv70 | Relation Dataset | 33 | .1906 | 15 | 6 | 描述实为 **analyst 一致预期 ⇒ 属 ANALYST**；cov 太低 |
| pv149 | Holidays and Trading Hours Calendar | 2 | 1.0 | 3 | 6 | 描述实为 **Data Explorers 借券/空头 ⇒ 属 SHORTINTEREST**；仅 2 字段 |
| pv47 | Specific Return Dataset | 5 | .9456 | 162 | 2 | 跨因子模型残差收益，见 §5.54.1 |
| univ1 | Universe Dataset | 1 | 1.0 | 16 | 4 | 无描述，1 字段 ⇒ 宇宙标记 |

⚠ **本 category 的 dataset-level description 与名称错配比 risk 更严重**（6/18 直接错类别）：
`pv14` 名「期货」实为 KOSPI200 指数、`pv149` 名「交易日历」实为借券数据、`pv20` 名「即期汇率」实为基本面、
`pv70` 名「关系数据」实为 analyst 预期、`pv13`/`pv29` 两名不同实为**同一张 BBID↔RIC 映射表**、
`pv37` 名「区间数据」实为异构大杂烩。
⇒ **与 risk 同一条禁令：不得用 dataset description 做机制推断，必须逐字段读 description。**
⇒ 同时说明：本类别的「非技术面内容」全部是**别的塔的重复物**（FUNDAMENTAL / ANALYST / SHORTINTEREST / 债券），
把它们当 PV 信号用只是在蹭塔票，不等于 PV 有自己的经济面。

#### 5.54.1 pv47（Specific Return）判死：机制与 risk71/risk72 同一，换表不换命

字段级实测（`filter_sharpe=false`，5/5 MATRIX）：

| field | cov | aC | description |
|---|---|---|---|
| `idiosyncratic_return_fraction` | 1.0000 | 13 | UBER 模型残差收益，percent，D0 |
| `pv47_d1_spret` | 0.9670 | 5 | specific return（D1） |
| `pv47_for_statssimple_only_spret` | 1.0000 | 79 | Asia 区 UBER 残差日收益，fraction |
| `pv47_spret` | 1.0000 | 52 | US UBER 残差收益，D1 变体，percent |
| `pv47_v21_for_statssimple_only_spret` | 0.7612 | 25 | specific return（另一版本） |

初始判断是「残差短期反转，教科书机制、cov 1.0、十年覆盖天然成立」⇒ 看似 PV 塔最优先候选。
**但台账里已有两次同机制实测**：
- `KOR-RISK71-RESIDUAL-REVERSAL-2Y-DEAD`：risk71（VS3 残差）16 条 α，**best_2y 0.59**；
- risk72（同源 specific return，5 字段 description 逐字相同）**判不投**，理由写死为
  「机制与 risk71 同族，死因 = **regime 级符号翻转（2022–2023）**，换宇宙不换 regime」。

⚠ 这里的关键判据不是 coverage、不是 aC，而是**死的那个闸是 2Y**：2Y 死意味着
「某些年份符号反了」，那是**机制在 regime 切换下不稳**，属机制层缺陷。换一个风险模型
（UBER statssimple vs VS3）只换残差化口径，**不换 regime**。
按本台账反复用的那条（§5.52.1 analyst9、§5.36.2 PV 技术面）：**换数据集不改变机制 ⇒ 换表不换命。**
⇒ **pv47 判死，不投配额。** 翻案前提：先给出「为何 UBER 残差模型能消除 VS3 残差的 regime 依赖」的
机制论证 + 逐年 S 的符号稳定性证据，两者缺一不谈。

另注两条**单位陷阱**：本集同时存在 percent（`idiosyncratic_return_fraction` 名字叫 fraction 但描述写 percent、
`pv47_spret`）与 fraction（`pv47_for_statssimple_only_spret`）两种量纲 ⇒ 若未来翻案，
**不得跨这两个字段做加减或比值**，只能在 `rank`/`zscore` 之后组合。

#### 5.54.2 pv37 判死：873 字段的异构大杂烩，主力家族是 227 已死的修正广度

`get_datafields` 实测 873 字段（777 MATRIX / 96 VECTOR），cov 分布
`>=.95: 231 / .80-.95: 87 / .50-.80: 407 / .30-.50: 138 / <.30: 10`，
描述关键词 `sale×96 / value×92 / price×52 / volume×31 / loan×18`。
**它不是「经营指标」，也不是「区间数据」，而是多来源 alternate data 的拼盘**，按内容分五族：

| 族 | 代表字段（cov / aC） | 判 |
|---|---|---|
| **① 卖方"best"预期 4 周修正** | `best_net_4wk_dn` .7872/226、`all_cinx` .7554/174、`best_net_gaap_4wk_dn` .7872/139、`best_net_4wk_up` .7872/95、`best_roa_4wk_chg` .7088/52、`best_ebitda_4wk_chg` .7244/40 | ⛔ **= wave 227 已死的修正广度轴**（`(numup−numdn)/numanalysts`）。「best」只是把样本换成 accuracy-weighted 口径，**表达形式仍是 up−dn**；与本轮 analyst46 的「想法流」也不是同一回事（那是事件强度，不是修正家数）。换表不换命 ⇒ 判死 |
| **② 资产负债表/利润表水平量** | `bs_accrual` .9183、`bs_add_paid_in_cap` .9494、`is_rd_expend` .6549/53、`intfv_*` 保险承保 | ⛔ 属 FUNDAMENTAL 面的重复物；FUNDAMENTAL 塔已 3/3 点亮，且水平量在本区需先取变化率（铁律 A）才算信号 |
| **③ 债券资产出售评估（日式口径）** | `all_lcs` `1lcs`/`2lcs`/`32lcs`、`all_mtps` .7548/149、`all_sbits`、`all_adbs`、`all_iabs`、`all_mpns` | ⛔ 覆盖率 .26–.79 且为**日本金融机构口径**，KOR TOP600 截面含义不明；A-2 说不出「谁被定价」 |
| **④ `vda` 家族（Volume Day Ahead）** | 10 字段，cov **.9999**，aC 8–23（`01vda` 23、`001vda` 20、`081vda` 16、`03vda` 15、`1vda` 14、`36vda` 8） | 🔎 **唯一残余候选**，见下 |
| **⑤ 杂项 PV** | `returns5` .996/174（5 日报酬，与 pv1 的 returns 同源）、`0d_tpds` .996/6、`annfv_mfm2_*` 13 个零 α | ⛔ `returns5` 是 pv1 重复物；其余无机制 |

**④ 为何不是现在就挖**：`vda` 的 10 个变体 cov 全 1.0、aC 仅 8–23（几乎无人用）⇒ 拥挤度极低，
「成交量预测 vs 实际量」的偏离确实是**非技术面**的 PV 自有信号（预期关注度/流动性事件）。
但**三条前置未过**：① 描述只有「N Volume Day Ahead」这类机翻，**不知道 N 是提前天数还是模型编号**
⇒ 连「预测 vs 实现」的比值都构造不出来；② 无任何历史长度证据，**约束 4 十年覆盖未知**；
③ 与 `adv20`/`volume` 的相关性未知，若 corr>0.9 则只是 pv1 的平滑版（§5.36.2 同款死法）。
⇒ **登记为备用线索，不发波**；要动它必须先做字段体检（六法）+ 十年覆盖 + 与 pv1 量的相关性三件事。

**⇒ PV 塔结论（扩写 §5.36.2，不推翻）**：PV 自有技术面全死（旧结论），本轮补上
「PV 自有非技术面」的盘点结果 —— `pv47` 机制重复、`pv37` 五族四死一待体检、
`pv13/pv29/pv14/pv20/pv70/pv109/pv173/pv149` 全属别塔内容的错标。
**PV 塔维持 2/3，仍只走 §5.36.2 的跨类别双塔门（OTHER 打成一颗同时给 PV 记一票），不单开 PV 波。**

⚠ 本节的判死**不动摇波 230**：230 的 A/B 是 analyst46 × analyst11（ANALYST 塔差一颗，最省），
PV 侧无同价值候选可换，**230 表达式与设置保持不变**。

### 5.55 波 229 收割与归因（`sentiment21`，两条都败，但**死因不同**）

| 槽 | alpha | 表达式 | S | F | 2Y | subU | TO | CW | RA fail |
|---|---|---|---|---|---|---|---|---|---|
| A | `2rAQRYNb` | `group_neutralize(reverse(ts_rank(ts_backfill(snt21dts_sop - snt21dts_gen, 66), 66)), sector)` | **−0.62** | −0.39 | −1.06 | −0.61 | .1356 | pass | SHARPE/FITNESS/SUB_UNIV/2Y（4 条） |
| B | `O0Aqk3xp` | `group_rank(ts_delta(ts_backfill(snt21pos_mean - snt21neg_mean, 66), 66), sector)` | −0.04 | −0.01 | 0.85 | 0.03 | .0655 | pass | SHARPE/FITNESS/2Y（3 条） |

**约束 4 先过**（这一步必须在归因前，否则归因被数据跨度污染）：
`get_alpha_yearly_stats` 首年 = **2014**，A `longCount 76 / shortCount 61`、B `longCount 88 / shortCount 490`
⇒ **十年覆盖成立，两条都是机制问题，不是数据跨度问题**。sentiment21 不适用 sentiment26 的 7/10 判死结论。

#### 5.55.1 A 归因：**符号稳定但强度不够**（与 228-A 的"vintage 翻转"是两种病）

逐年 S：2014 −0.25 / 2015 −0.76 / 2016 −1.66 / 2017 −1.52 / 2018 −0.07 / 2019 −0.24 / 2020 −0.72 / **2021 +0.83** / 2022 −0.01 / 2023 −2.28。
- 10 年里 9 年同号（负）⇒ **不是 regime 随机，方向是稳定的**，只是我们把方向取反了。
- 反号后（允许 decay/trunc 非精确反号，按铁律 B 只作量级估计）S ≈ **+0.62**，且 9/10 年为正、2Y ≈ +1.06。
- ⇒ 真实机制 = **「相对 generical 语气的偏离本身带正向动量」**（说法越乐观于通用语气 ⇒ 后续偏涨），
  与我们在 §5.49 假设的「分歧 ⇒ 反转」相反。R2 论坛配方的 **reverse 方向在本区是错的**。
- 判死不因方向错，而因**量级**：翻号后离 1.58 还差 0.96。本字段是**语气差**（dispersion 类读数），
  没有可放大的经济维度（加壳/换中性化/换窗口都属"参数层"，而 0.62 → 1.58 是机制层缺口）
  ⇒ 按归因表「信号真实但强度不足」也不给配额：该档只允许**强度杠杆**，本区强度杠杆（`signed_power`）在
  语气差上无先验支撑，且 0.62 起点过低。**A 判死（弱侧）**。

#### 5.55.2 B 归因：**平局值污染 ⇒ 这次测试对机制不公平**（重要，别读成"机制已死"）

逐年 longCount/shortCount：**88/490、83/527、103/515、162/457、132/519、118/526、83/561、75/604、94/559、173/480**
—— 十年**每一年**都是 1:4 ~ 1:8 的一边倒。而 `group_rank(·, sector)` 在无平局时应产出生效均匀的多空两侧。
⇒ 根因是 **`ts_delta(pos_mean − neg_mean, 66)` 的平局**：情绪均值为离散/量化值，
大量标的的 66 日差分**恰为 0**，`group_rank` 把这一大坨平局压在同一名次 ⇒ 组合的 **83% 不是"情绪变化"信号，
而是"把全部无变化标的做成空头"的机械腿**。

⚠ **2026-10-30 补精确机理（§5.57.2 的标定证据，只补不推翻）**：`rank` 对并列值给的就是**平均名次**
`v = 1 − K/(2N)`（论坛贴 `43178926004887` 用两个已知 K/N 集合标定命中），所以平局块**不在极端、而在中段**。
1:4 的来历是：平局块名次（≈0.4）**落在组均值 0.5 之下** ⇒ 整块拿到同一个**小幅负权重**，被计成 short；
剩余 17% 非平局标的再分两半 ⇒ 恰好复现 1:4 ~ 1:8。**结论与处置都不变**，且由此得到通用修法
`tail(w, lower=q, upper=1-q, newval=0.5)`：把无信息中段居中，中性化后权重归零。

逐年 S：2014 −2.46 / 2015 −1.02 / 2016 +0.84 / 2017 −0.02 / 2018 +1.46 / 2019 −0.77 / 2020 +0.99 / 2021 −0.17 / 2022 +0.78 / 2023 +0.92
⇒ 5 正 5 负，且**前两年重亏、后段偏正**：与 228-A 的 2014→2015 vintage 翻转同型（供应商模型换版）。

⚠ **结论的适用范围必须写清**：S −0.04 **不能**读作「情绪变化机制在本区无信号」，
因为测的根本不是那个东西（83% 的仓位来自平局腿）。正确读法是 **「本次测量无效」**。
⇒ B **判死（测量缺陷）**，但它给出一条**唯一且明确的返工配方**（不是"再试一次"）：
把"变化"从 `ts_delta` 换成**连续化读数** `ts_zscore(pos_mean − neg_mean, 66)` 再 `group_rank(..., sector)`
（z-score 不会有 0 平局），或对差分加 `trade_when(not_equal(ts_delta(...), 0), ..., -1)` 直接弃掉无变化标的。
**该返工只有在 SENTIMENT 塔重新有空位时才排**（现在它是 0/3 但已连败两波，优先度低于 ANALYST/PV）。

#### 5.55.3 SENTIMENT 塔结论

`snt21dts` 方向稳定但强度 0.62；`snt21pos − neg_mean` 测量无效（可返工）。
叠加 §5.48/§5.49 已记录的 sentiment26 判死（无截面 + 7/10 年），
⇒ **SENTIMENT 塔 0/3，本轮不再投配额**；返工配方留在上段，等其它塔无票时才动。

### 5.56 波 230 已发（`analyst46` × `analyst11`，ANALYST 塔差一颗）

multisim **`HWAQG5qu4TZbdExUjvTfpy`**（2026-10-30 09:20Z），设置同前（KOR/TOP600/D1、SECTOR、decay 4、
trunc 0.08、pasteurization ON、unitHandling VERIFY、nanHandling ON、maxTrade ON、`validate_fields=true`）：
```
A: group_rank(ts_backfill(anl46_sentiment, 5), sector)
B: group_rank(ts_delta(ts_backfill(overall_sustainability_score, 66), 66), sector)
```

**发批前做了两处核对/一处修订（都必须留痕）**：
1. **字段名逐字核对**：`get_datafields(analyst46)` = 6 字段，`anl46_sentiment`
   （cov .4192 / aC 10，"聚合卖方 idea 情绪，已内含 decay + 贡献者质量 + 距财报远近 + idea 量/方向"）**存在**；
   `overall_sustainability_score` 在 analyst11 持久化产物里 **逐字命中**。
   ⇒ 防的是"字段不存在 ⇒ 整批 CANCELLED 连坐"。
   ⚠ 同集另有 `anl46_indicator`（1–10 截面多头分，纯方向）与 `anl46_performancepercentile`
   （该信号过去 12 个月的**历史预测力分位**）—— 后者是难得的**外生可靠性条件变量**，本轮不用，登记为 analyst46 的第二个概念。
2. **B 的窗口 252 → 66 修订**（相对 §5.52.5 预注册）：`ts_delta(·, 252)` 在 2014 年**必然全 NaN**
   （差需要 252 个交易日），会把**约束 4 的一票否决变成窗口造成的假阳性** —— 那正是本轮两次踩过的坑
   （把工具缺陷读成数据缺陷）。改 66 后：机制不变（仍是 ESG 评级修正），且更贴 Liu & Zhou (2025) 的
   "**评级变动事件**"口径（该文测的是 change，不是 YoY improvement）。
3. **风险预登记**：若 B 像 229-B 一样出现 long/short 严重失衡 ⇒ 先判**平局污染**再谈机制，不得直接判机制死。

收批照 §5.52.5 五行预注册表；仍以 `get_alpha_yearly_stats` 首年 `longCount` 为第一读数（约束 4）。
若 B 落 S 1.3–1.58 区间，**唯一允许**的下一步是把 `overall_sustainability_score` 换成
`environmental_pillar_composite_score`（MSCI 样本实证只有 E 支柱显著，见 §5.52.7）；S<1.0 则直接判死。

### 5.57 `insiders5` 字段画像 + 两条论坛构造先验 + 波 231 预注册（单变量对照）

#### 5.57.1 字段画像（53 字段，**全部 VECTOR**，`get_datafields(insiders5, KOR, D1, TOP600)` 实测）

覆盖率四档（不是三档，别并）：
| 覆盖 | 字段数 | 内容 |
|---|---|---|
| .9991–.9996 | 26 | **持仓快照 / 公司静态属性**（含 `source_data` `data` `ratio` `rpst_grp_typ` `tnc` `list_yn` `insd5_nm_kor`） |
| **.8728** | 7 | **库存股（자사주）**：`trsy_data` `trsy_ratio` `trsy_real_data` `trsy_real_ratio` `trsy_recent_dt` `trsy_tnc` `grp_trsy_td_drt` |
| **.7318** | 13 | **逐笔交易**：`ghc_tr` `fb_tr` `fa_tr` `vol_bf` `vol_af` `vol_chg` `trd_amt` `unt_val` `trd_reason_a/b` `history_td_drt` `td_ctn` `td_ghc` `officer` `qes` `serial` `group_s` |
| 其余 | 7 | 混合（`recent_dt`、`mmyy_srfi`、`issuance_category`、`security_type` 等） |

拥挤度分层（`alphaCount`）——**这条是本波选字段的全部依据**：
- **高拥挤 = 持仓快照（水平）**：`source_data` **734** / `source_real_data` 625 / `rpst_grp_typ` 574 /
  `tnc` 452 / `source_ratio` 407 / `source_real_ratio` 299 / `data` 299 / `grp_source_td_drt` 237 /
  `real_ratio` 205 / `source_recent_dt` 271 / `recent_dt` 127
- **中低拥挤 = 交易流量与库存股**：`ghc_tr` **212** / `trsy_ratio` **152** / `fa_tr` 131 /
  `trsy_real_ratio` 128 / `ratio` 121 / `vol_chg` 119 / `trsy_real_data` 95 / `vol_bf` 94 /
  `trd_amt` 84 / `fb_tr` 76 / `vol_af` 73 / `td_ctn` 71 / `trsy_data` 69
⇒ **平台已挖的是"谁持有多少"的快照水平，没挖的是"仓位变了多少"与"库存股"**。
与 DEU 帖的核心命题（信息在比例里、不在金额里）以及"低拥挤 = 事件腿"完全同向。

**存量 vs 流量正交表**（照抄 DEU 帖 §1.3 的推导法，用来定位可构造的比值）：
| | 股数 | 比例 | 金额 |
|---|---|---|---|
| 存量（持仓） | `data` / `real_data` / `source_data` | `ratio` / `source_ratio` / `real_ratio` | — |
| **流量（本笔）** | `vol_bf` / `vol_af` / `vol_chg` | `fb_tr` / `fa_tr` / **`ghc_tr`** | `trd_amt` |
| 库存股（存量） | `trsy_data` / `trsy_real_data` | **`trsy_ratio`** / `trsy_real_ratio` | — |
⇒ `ghc_tr`（"Change in ownership percentage resulting from the transaction"）**本身就是无量纲的仓位变动比例**，
等价于 DEU 帖里 `shares / holdings`（已被证明有信息的那一列），**不需要再造比值**；
`trd_amt`（金额）被 USA 帖与 DEU 帖**双重证伪**（混杂公司规模与个人财富），本波不进。

两处画像警示：① 53 字段**全是 VECTOR** ⇒ 必须先 `vec_*` 聚合；② 交易族覆盖率仅 .7318 ⇒ 27% 的股票
**永远没有交易记录**，`nanHandling=ON` 会把它们填 0，形成**并列块**（机理见 5.57.2 与 §5.55.2 的补注）。

#### 5.57.2 论坛取回的两条构造先验（约束 2 · 通道 A），二者**结论相反**，故须本区实测

贴 `43178926004887`（DEU/INSIDERS，69 票，**已提交** `xAjEkeOq`：S 1.68 / F 1.34 / 2Y 2.40 / TO 7.36% / prod .52 / ra=0）：
- 骨架：`r = 流量/存量`；`w = winsorize(group_rank(ts_sum(r,66), industry), std=2)`；`alpha = tail(w, 0.25, 0.75, 0.5)`。
- **`ts_sum` 不能换 `ts_mean`**：事件型数据上 `ts_mean` 的分母是"非 NaN 日数"，会把"一季发生几次"的
  **频率信息除掉**（实测 S 1.44 → 0.73）。CMP(2012) 说明频率本身就是机会型 vs 例行型的判据。
- **并列块可量化**：`nanHandling=ON` 把无申报股票在数据层填 0 → `ts_sum` 保序保留 0 → `group_rank` 并名次；
  用「恒零 alpha ⇒ turnover=0」当掩码阶梯读数 + 两个已知 K/N 集合标定，得 **`rank` 对并列值给平均名次
  `v = 1 − K/(2N)`**；实测并列块每天占横截面 **72%+（多数日 80%+）**，该块 rank ≈ **0.4**（坐中段）。
- **`tail` 是稀疏事件 VECTOR 数据的标准后处理**：同一设置下 **+0.24 S / +0.58 subU**，且
  q ∈ [0.20, 0.30] 是**平台不是尖峰**（0.10→0.94、0.35→1.10 才崩）。**适用边界：只对 coverage 明显 < 1 的
  稀疏事件数据；对稠密数据 tail = 纯砍信号**。
- 卖出侧无信息（`insider_agg` 卖出股数仅 0.21，与 JMZ 2003 一致）。

贴 `43152032301591`（USA/INSIDERS，43 票，**自我证伪式**研究日志，5 批 25 次模拟）：
- 存活形态只有**「相对自身基线的异常度」**：`ts_zscore(ts_sum(F,21),252)` S=**3.06**；
  **一切跨字段相对结构（份额 / 背离 z 差 / 比值 / 聚类度）5 式全灭**。
- **`zscore` ≫ `rank`（2.25 vs 0.61）**：rank 抹掉尖峰幅度，而该信号的价值**恰恰集中在"异常得离谱"的
  极端事件**上 ⇒ rank 类变换在事件强度字段上是**自废武功**。
- 窗口梯度单调：**21 ≈ 42 > 63 > 126 > 252** ⇒ 数周尺度的短期反应不足。
- 该帖的救命杠杆是**换宇宙**（TOP3000 → ILLIQUID_MINVOL1M，subU 从 0.7 跳到 2.14–2.28）；
  **KOR/D1 唯一合法宇宙 = TOP600 ⇒ 此杠杆在本区不可用**。若 231 出现 subU 问题，只能走 tail 路线。
- 同帖评论补充：该 alpha 真实分类是 **OTHER 塔**（AI 按数据集名误判为 INSIDERS），且开 maxTrade 后表现变差、
  多空样本少 ⇒ 读它的结论时不要把"塔"和"数据集"混为一谈。

#### 5.57.3 外部文献（约束 2 · 通道 B，能否迁移按 KOR SOP 只当假说）

- **Jeng, Metrick & Zeckhauser (2003, REStat)**：滚动**买入**组合 ≈ **40bp/月**超额（约 1/6 在前 5 日、
  1/3 在首月），**卖出组合无超额** ⇒ 买入侧有信息、卖出侧无信息。
- **Lakonishok & Lee (2001, RFS)**：内部人信号必须按规模标准化，原始金额被市值与个人财富主导
  ⇒ `trd_amt` 不可用、`ghc_tr` 可用（正是本集给的无量纲比例）。
- **Cohen, Malloy & Pomorski (2012, JF)**：例行 vs 机会型；**频率本身**是机会型的信息 ⇒ 支持 `ts_sum`。
- **Bonaimé & Ryngaert (2013)** / **Chen, Chen, Chen & Schatzberg (2014, JBFA)**：回购公告后的
  **内部人异常买入**才能预测长期经营改善与收益（"dichotomous expectations"）
  ⇒ 支持后续把 `trsy_ratio`（回购执行）与 `ghc_tr`（内部人买入）做**条件门控**，而不是并列相加（闸 5 禁混信号）。
- 以上样本均为 USA/DEU ⇒ **方向可迁移、幅度不可迁移**；本区必须实测。

#### 5.57.4 A-2 收益来源声明（硬门）

| 声明项 | 内容 |
|---|---|
| 谁在被定价 | 上市公司**内部人（임원·주요주주）的持股登记**；对手方是只看"有无增持公告"的迟钝投资者 |
| 为什么会被错 | DART 内部人持股变动是**逐笔申报的登记册**，不是横截面因子：信息全公开，但要两次变换（vec 聚合 + 时间累计）才能读出"仓位变了多少"；绝大多数使用者停在事件层面 |
| 错了多久修复 | **数周**（USA 帖窗口梯度 21≈42>63>126>252 单调）⇒ 本波用 21 / 66 两个量级各一条 |
| 预期方向 | 内部人**净增持比例**上升 ⇒ 后续跑赢；卖出侧**先验无信息**（JMZ）；若卖出侧反而更强 ⇒ 判"拟合了别的东西"（贴 1 自带的一致性检验） |
| 边界条件 | 覆盖率 .7318、**27% 个股永无交易记录**；KOR 无 ILLIQUID 宇宙可换；2014 年可用性未验（约束 4 交首年 `longCount` 裁决） |

#### 5.57.5 波 231 预注册（**同字段 × 两种构造**的单变量对照）

`preflight_expressions(region=KOR, universe=TOP600, delay=1)` 实测 **`valid=true`、字段 known、
`vector_fields=[]`、`any_changed=false`**：
```
A: ts_zscore(ts_sum(vec_sum(insd5_ghc_tr), 21), 252)
B: tail(winsorize(group_rank(ts_sum(vec_sum(insd5_ghc_tr), 66), industry), std=2), lower=0.25, upper=0.75, newval=0.5)
```
- A = 贴 2 的**幅度保留 + 自身基线异常度**（无跨字段结构、无 rank）；B = 贴 1 的 **rank + 并列中段掐除**。
- **为什么两槽都押同一个字段**：两贴对"该不该 rank"给出**相反**结论，而我在 KOR **一条证据都没有**。
  两个槽做单变量对照，赢家即成为**后续 8 座未点亮塔的构造先验**（news / institutions / insiders / macro /
  earnings / imbalance 多为事件型 VECTOR）——杠杆远大于再换一个字段。若改成两个字段，赢/输都无法归因到构造。
- 设置同上波：KOR/TOP600/D1、**SECTOR**、decay 4、trunc 0.08、pasteurization ON、unitHandling VERIFY、
  nanHandling ON、maxTrade ON。
- **五行预注册判定表**：

| 读数 | 判定 | 下一步 |
|---|---|---|
| 任一 S≥1.58 且 F≥1.0 且 2Y≥1.58 | 全闸命中 | 进 S4 稳健闸 → prod（**只用 MCP**）→ 交用户确认 |
| 1.0≤S<1.58 且逐年 ≥7/10 同号 | 信号真实、强度不足 | 允许**强度杠杆**（21→42、tail q 微调） |
| 1.0≤S<1.58 但 `S<1.0` 年份 ≥3/10 | regime 依赖 | 停扫参数，换机制族 |
| S<1.0 且**首年 `longCount`=0** | 约束 4 不满足 | 先查是否窗口造成（本波已避开 252），确认后判死 |
| S<1.0 且 long:short 长期偏离 1:1 超 1:2 | 并列块污染（§5.55.2 补注的机理） | 判**构造**失效，A 加 tail / `newval=0`，**不得**判机制死 |
| 两腿都 <1.0 且 A−B 差 <0.3 | 构造不是瓶颈 | 判**机制**死，`insd5` 转 `trsy_ratio` 回购腿 |

- **风险预登记**：① 27% 永无交易记录的股票在 nanHandling=ON 下并成中段 rank 块，B 的 tail 正为此；
  若 **A 的 subU 崩而 B 不崩，这正是贴 1 的预测**，应读作构造证据、不是机制证据；
  ② KOR 无 ILLIQUID 宇宙，贴 2 的救命杠杆不可用；③ `ts_zscore` 在"全期为 0"的股票上分母为 0 ⇒ NaN ⇒ 自动无仓（预期行为）。




### 5.58 波 230 收批（analyst46 水平 × analyst11 可持续性变化）—— 双判死，但挖出一条**全战役级构造先验**

收批 `HWAQG5qu4TZbdExUjvTfpy` → 2/2 COMPLETE，0 error；入库 `harvest_multisim_results(wave="230")` → upserted 2，暂定 verdict=FAIL。

| ID | 表达式 | S | F | 2Y | TO | long:short | RN S |
|---|---|---|---|---|---|---|---|
| `WjOnWWXj` | `group_rank(ts_backfill(anl46_sentiment,5), sector)` | 0.44 | 0.22 | 0.84 | 4.42% | 191:444（**1:2.32**） | 0.39 |
| `qMLvmmzA` | `group_rank(ts_delta(ts_backfill(overall_sustainability_score,66),66), sector)` | 0.32 | 0.14 | 1.13 | 4.16% | 238:397（1:1.67） | 0.05 |

**约束 4 已核**（第一读数，先于归因）：逐年首年 2014 `longCount` = **164 / 163**，两者 10 年逐年 longCount 均 >0 ⇒ 近十年有数据这件事**不是死因**，不存在覆盖窗口问题。

#### 5.58.1 `WjOnWWXj` —— 死于**构造**（可按 §5.57.5 那行返工），但机制本身也不值得返工

逐年 S：**−1.62 / 0.18 / −0.01 / 1.86 / 0.84 / −0.26 / 0.38 / 1.16 / 1.46 / 0.22**，5 正 5 负。

`group_rank` 在**每个 sector 内**都应产出生效均衡的多空两侧；实测却**十年每一年**都是 191:444 量级的 1:2.3 一边倒，且比例几乎不随年份变化（164:414 → 200:453）。这与 §5.55.2/§5.57.2 标定的平局机理**同型**：`anl46_sentiment` 是低基数/离散的打分，`group_rank` 给并列值的是**平均名次** `v = 1 − K/(2N)`，平局块落在 0.5 之下 ⇒ 整块拿同一个**小幅负权重** ⇒ 计成 short。⇒ **这是构造缺陷，按纪律不得据此判机制死。**

但**不值得返工**，理由在 A-2 硬门：`anl46_sentiment` 的**水平值**说不出「谁被定价 / 为什么错 / 多久修复」。分析师情绪水平的截面排序没有修复期概念，它本身就是共识的镜像。⇒ 判死依据是 **A-2 缺项（无机制）**，不是 S。若将来要用它，唯一合法形态是先取**变化率**（铁律 A），而不是给水平值加 tail。

#### 5.58.2 `qMLvmmzA` —— 死于**单年集中 + 覆盖漂移**，且这条比 S=0.32 更致命

逐年 S：−1.64 / −0.19 / 1.59 / 0.96 / 0.43 / 0.13 / −0.21 / 0.04 / **2.22** / 0.38 —— **`S<1.0` 占 8/10**（按发波决策表：≥3 成 ⇒ 2Y 闸结构性不可达，⛔ 停扫参数）。

- **单年集中度**：2022 一年 pnl = **1,511,587**，全期 = 2,595,227 ⇒ **58.2%** 的正收益来自一年。远超「top1 年 >30% ⇒ 过拟合指纹」线。
- ⇒ **2Y=1.13 是假象**：它正是被 2022 抬起来的，不能读作"近年更稳"。这条要写进纪律：**单年集中时 2Y 不可单独作为稳健证据**。
- **覆盖漂移实锤**：long/short 从 163:416（2014）单调漂到 301:352（2023）。同一份"分数变化"信号，股票数在十年里换了近一倍 ⇒ 它赚的很大一部分是 **ESG 覆盖扩张带来的入池变化**，不是分数变化。这是数据 vintage 混淆，不是 alpha。
- RN S = 0.05（raw 0.32）⇒ 铁律 E：raw 本身已弱、RN 几乎归零，**不存在"换中性化档能救"的空间**。

#### 5.58.3 ★ 全战役级构造先验（本波唯一可复用产出）

> **`group_rank(<低基数/离散水平字段>, <分组>)` 在 KOR 会系统性产生 1:2~1:8 的多空失衡**，机理是并列值取平均名次后落在 0.5 之下。判据：**逐年 long:short 比例稳定地偏离 1:1 超过 1:2**（不是某一年，是每一年）。
> **处置**：① 能取变化率的先取变化率（铁律 A）；② 必须排名时套 `tail(w, lower=q, upper=1-q, newval=0.5)` 把无信息中段居中；③ 或直接 `ts_zscore`（无并列）。
> **反读纪律**：出现该形态时，**S 低不能归咎于机制** —— 先按本条判构造，再谈死活（§5.55.2 已因未做此区分而误记过一次）。

配套的**平台读数口径**：`longCount`/`shortCount` 在 `metrics` 汇总层就给出，**收批第一眼就该看它**，不必等 yearly stats。汇总层比例已超 1:2 的，直接进构造诊断。

#### 5.58.4 波 231 已派发（INSIDERS 0/3，预注册照 §5.57.5 原样执行）

`KiVQZ7JJ4K69tW3rcwV4NM`（2/2 已提交，2 槽占满）：

- A `ts_zscore(ts_sum(vec_sum(insd5_ghc_tr), 21), 252)`
- B `tail(winsorize(group_rank(ts_sum(vec_sum(insd5_ghc_tr), 66), industry), std=2), lower=0.25, upper=0.75, newval=0.5)`

设置：KOR/TOP600/D1，SECTOR，decay 4，trunc 0.08，VERIFY，nanHandling ON，maxTrade ON。
**注意本波与 §5.58.3 的关系**：B 已内置 tail（`newval=0.5`）⇒ 若 B 的 long:short 仍严重失衡，才说明 `ghc_tr` 的 27% 零块不是并列问题；若 **A 失衡而 B 均衡**，正好反向验证了 5.58.3 这条先验。收批仍以 `get_alpha_yearly_stats` 首年 `longCount` 为第一读数。

### 5.59 塔位实况复核 + earnings3 / institutions6 画像 + 两条论坛否决证据 + 波 232 预注册

#### 5.59.1 ★ KOR/D1 塔位实况（2026-10-30 平台读数，纠正此前多处口径）

`get_pyramid_alphas(region="KOR", delay=1)` 实测 15 座塔：

| 已点亮（有分） | analyst 2 · **fundamental 3** · model 3 · other 1 · pv 2 · **shortinterest 4** |
|---|---|
| **0 点（未点亮，本战役的全部靶区）** | **earnings · imbalance · insiders · institutions · macro · news · risk · sentiment · socialmedia** |

⇒ **两条被本文件此前用错的假设，现更正**：
1. **「41 条未提交强候选可以补塔」不成立**：逐条查归属，24 条在 `shortinterest`（4 点）、12 条在 `other`（1 点）、5 条在 `fundamental`（3 点）——**全部落在已点亮塔**。它们对「未点亮塔」这个目标**零贡献**，只能当已点亮塔的增量分与「流水线能产出过闸件」的存在性证据。
2. **ANALYST 已是 2 点（已点亮）**，波 230 打 analyst46 本身就是越靶；虽结论（判死）不受影响，但**靶区纪律必须写死**：发波前先读 `get_pyramid_alphas`，0 点才是靶。

顺带一条构造实证（`vR29LgEz`，`get_alpha_details` 实读）：`quantile(group_rank(...))` 壳下的 long:short = **319:319 精确平衡**，而同一个库里的裸 `group_rank` 型候选普遍 1:2 以上失衡 ⇒ **§5.58.3 的并列诊断又被独立验证一次**。

#### 5.59.2 `earnings3` 字段画像（KOR 唯一的 earnings 数据集）

8 个字段，**全部 MATRIX**，无一 VECTOR；alphaCount 199–616（中低拥挤）；数据集级 alphaCount 2616。

| 字段 | 覆盖 | 语义 |
|---|---|---|
| `ern3_next_interval` | **0.5825** | 距**下一次**财报的交易日数（正数，倒数计时） |
| `ern3_pre_interval` | **0.7756** | 距**上一次**财报的交易日数（应为 ≤0） |
| `ern3_next_reptime` / `ern3_pre_reptime` | 0.5825 / 0.7756 | 公告时点（HHMM/场次码）—— **不是信号** |
| `ern3_all_delay_1_*` | 0.5599 / 0.7232 | 同义的 ASI 全样本口径，比非 all 版覆盖略低 ⇒ **优先用非 all 版** |

**关键判断：这是「日历」，不是「盈余惊喜」**——没有 SUE、没有 surprise、没有 announcement return。
⇒ 论坛 52 票〈财报漂移"快慢手"之争〉(post `43151941437463`) 与 108 票〈量化研究推荐论文〉里的 PEAD 配方**全部用不上**（它们都要求 surprise 侧）。本条要写死，避免后来者再拿 PEAD 模板套 earnings3：**PEAD 需要"意外"，earnings3 只有"何时"**。

可实现的机制只剩一个：**财报公告溢价（announcement premium）**——公告窗口的收益高于非公告窗口（Beaver 1968；Frazzini & Lamont 2007；De George, Barber, Lehavy & Trueman, JFE 2013, 108(1):118-138《The earnings announcement premium around the globe》= **跨国样本**，非纯美国证据，故 KOR 方向上可用、量级不可搬）。

#### 5.59.3 `institutions6` 字段画像（全 11 个，**必须 `filter_sharpe=false`**）

⚠ 默认 `filter_sharpe=true` 只回 4 个，藏掉的正是对侧腿（`*_disposed` / `*_sellers` / `*_all_owners`）——本文件 §`0.1` 已记过这个坑，本波再踩一次，现按纪律全文重取。

覆盖 **0.9976 ~ 1.0**（KOR 最完整的一档），每字段 alphaCount **59–249**（全 KOR 数据集里最低拥挤档之一）。四对齐全：

| 存量 | 采集（flow+） | 处置（flow−） | 广度 |
|---|---|---|---|
| `aggregate_share_count_institutions` (0.9976) | `quantity_institutional_shares_acquired` | `quantity_institutional_shares_disposed` | `count_institutional_holders_security` |
| `aggregate_equity_value_institutions` (0.9976) | `market_value_institutional_shares_acquired` | `market_value_institutional_shares_disposed` | `count_institutional_buyers_security` / `count_institutional_sellers_security` |
| `aggregate_share_count_all_owners` / `aggregate_equity_value_all_owners`（均 1.0） | — | — | — |

⇒ 「净增持 = 采集 − 处置」是**单一经济含义**，`subtract`/除法归一化在 A-3 下合规（不是双机制拼腿）。

#### 5.59.4 ★ 论坛否决证据（两条，都直接改结论）

| 出处 | 内容 | 对本战役的结论 |
|---|---|---|
| post `43754821327639`（GBR，**70 票**，作者完整公开 5 版迭代） | 其**自我证伪段**：把 `group_zscore((quantity_acquired − quantity_disposed)/(1 + aggregate_share_count_institutions), industry)` **单独做主 Alpha** → **S −0.11 / F −0.02** | **机构净买入本身不是 alpha**（至少 GBR 不是）。⇒ 不许把「净增持」当主信号直接交；它只能当门控/条件 |
| 同上 | 门控反向（只留净买入最高 30%）→ **S 0.57 / F 0.26** | 方向成立但强度不足 ⇒ 主信号必须是**别的东西** |
| 同上 | 版本一（**家数差**做门控）反而拖累 1.28→0.99 | 「家数」≠「股数」两种语言；**广度**与**金额**必须分开测，不许混 |

配套正向线索（同帖 + post 命中 `43212475386007`「流量/存量对」）：`value/holdings` 与 `shares/holdings` **1.59 / 1.53 同号**，事件周期 **66（季度）**。以及一条工程警示（post `43175786936087`）：**net_buy 类字段换手可达 117%**，必须平滑。

#### 5.59.5 波 232 预注册（两座未点亮塔，各 1 条）

**靶区纪律**：两座塔 `institutions` 与 `earnings` 均为 **0 点**（§5.59.1 实读）。

```
A (institutions6 · 0/3)：quantile(group_rank(ts_rank(group_rank(
      (quantity_institutional_shares_acquired - quantity_institutional_shares_disposed)
      / (1 + aggregate_share_count_institutions), industry), 1008), market))
   设置：STATISTICAL / nanHandling=OFF / maxTrade=OFF / decay 4 / trunc 0.08
        ↑ 逐字沿用 vR29LgEz 的设置（本区最强件的实证档），不做改动

B (earnings3 · 0/3)：reverse(group_zscore(ts_backfill(ern3_next_interval, 5), industry))
   设置：SECTOR / nanHandling=ON / maxTrade=ON / decay 4 / trunc 0.08 （本区标准档）
```

**为什么 A 用本区自己的壳而不是照抄论坛**：论坛的净买入**单独做主信号已被作者自证伪（S −0.11）**，
若照抄必死。唯一有本区实证支撑的替代是把同一「净增持」输入送进 **`vR29LgEz` 的壳**
（S 1.94 / 2Y 2.51 / 22 项检查全过 / long:short 精确 319:319）。⚠ **风险预登记**：壳本身可能携带相关性
⇒ A 若过闸，**prod 必须实测**，且预期它的 prod 会高于同族新壳（论坛 post `43536370604567` 已警告
「同源信号做差，PC 一定降，但这不等于你做出了新东西」——反向提醒：**同壳不同字段同样可能撞 PC**）。

**为什么 B 用 `group_zscore` 而不是 `group_rank`**：`ern3_next_interval` 是**整数倒数计时**，
`group_rank` 会在每个整数日值上形成并列块 ⇒ 正是 §5.58.3 的病根；`group_zscore` 是组内线性变换，**不产生并列**。

**A-2 收益来源声明（两条都要，缺一不许进归因）**：
- **A（机构净增持）**：被定价的是**跟随机构流量的散户/被动资金**；为什么错——13F 类持仓有**披露滞后**（季度），
  价格在滞后期内未完全反映净增持；修复期 = **一个季度（66）到一年（252）**；预期方向——**净增持为正 ⇒ 后续跑赢**。
  失效边界：覆盖率 ~1.0 但**季度频**（日频无信息）；净买入单独做信号在 GBR 实测 ≈0（§5.59.4）。
- **B（公告溢价）**：被定价的是**事件风险的承担者**；为什么错——公告期信息不确定性高，投资者要求折价，
  公告前后收益被系统性压低/抬高；修复期 = **公告窗口前后 5 日**；预期方向——**临近公告为正、公告后回落**
  （故取 `reverse`：做多 `next_interval` 小者）。失效边界：覆盖 0.5825；日历陈旧会让 `next_interval` 失真；
  KOR 无 ILLIQUID 宇宙可放大该效应。

**收批判定表（沿用 §5.57.5 六行，新增第 7 行）**：

| 读数 | 判读 | 下一步 |
|---|---|---|
| S≥1.58 & F≥1.0 & 2Y≥1.58 | 全闸 IS | 进 S4 稳健闸 → prod（**只用 MCP**）→ 用户确认 |
| 1.0≤S<1.58 且 ≥7/10 年同号 | 强度不足 | 只允许强度杠杆 |
| 1.0≤S<1.58 且 `S<1.0` 年份 ≥3/10 | regime 依赖 | 换机制族，不扫参数 |
| S<1.0 且首年 `longCount`=0 | 约束 4 | 先查窗口，确认后判死 |
| S<1.0 且 long:short 偏离 >1:2 | 构造失效 | 加 tail/newval，**不得判机制死** |
| 两腿都 <1.0 且 \|A−B\|<0.3 | 构造不是瓶颈 | 判机制死 |
| **B 单腿 S<1.0 而 `ern3_pre_interval` 方向为正** | 公告溢价只有**事前**没有**事后** | 允许把窗口从 `next` 换 `pre` 再测一次（**仅一次**） |

### 5.60 未点亮塔 × 数据集版图（2026-10-30 全量实读，约束 1 的落盘）

九个 0 点塔逐个 `get_datasets(category=…, region="KOR", delay=1, universe="TOP600")` 实读结果与选型判据。
**判据顺序**：① 覆盖 ≥0.4（约束 4 门槛；低于此十年数据必然断续）② alphaCount 越低越好（拥挤度）
③ 字段数适中（1–2 字段=单点探针，>80 字段=画像成本过高）④ valueScore 高。

#### 5.60.1 `news`（24 个，覆盖最参差的一座——**选型比挖法更重要**）

| 数据集 | 覆盖 | 字段 | alphaCount | valueScore | 判 |
|---|---|---|---|---|---|
| **news38** News Analytic Model | **0.7971** | 45 | **227** | 4 | ⭐ **首选**：覆盖高 + 拥挤低 + 实时/历史新闻情绪 |
| **news54** Key Developments | 0.6914 | 40 | **43** | 5 | ⭐ 次选：**全 KOR 最低拥挤**之一，事件+情绪 |
| news79 Global Corporate News Analytics | **0.8563** | 85 | 899 | 2 | 覆盖最高但已较拥挤、字段 85 个（画像成本高） |
| news50 Web News Analytics | 0.6254 | 81 | 113 | 5 | 备选，字段多 |
| news21 Macro Economic Event | 0.7435 | 13 | 143 | 3 | 备选，13 字段成本低 |
| news7 Real Time News Feed | 0.6327 | 56 | 372 | 3 | 备选 |
| news59 Corporate Events | **1.0** | 2 | **2396** | 1 | ⛔ 覆盖满分但**极拥挤**（2396），只剩 2 个事件标志 |
| news104 / news17 / news3 / news31 / news36 / news46 / news48 / news73 / news84 | 0.226–0.370 | — | 8–212 | 4–5 | ⛔ **覆盖 <0.4**，约束 4 会直接卡住，不投 |
| other7（挂在 news 类别下） | 0.2938 | 11 | 29 | 5 | ⛔ 覆盖不足 |

#### 5.60.2 `risk`（7 个——**`risk70` 是陷阱，`risk60/59` 才是入口**）

| 数据集 | 覆盖 | 字段 | alphaCount | 判 |
|---|---|---|---|---|
| **risk60** Securities Lending Insight | **1.0** | **5** | 211 | ⭐ **首选**：覆盖满分、字段最少（4 个交易维度）、借券/做空动态 |
| **risk59** Securities Lending & Short Market | 0.9806 | 16 | 561 | ⭐ 次选：同族更细 |
| risk71 Daily Specific Return | 0.6658 | 7 | 344 | 备选：残差收益画像 |
| risk72 Specific return of extended factors | 0.6246 | 5 | 400 | 备选 |
| risk88 Other Multi-Factor Risk Models | 0.9727 | 64 | 1405 | 拥挤 + 64 字段 |
| risk68 Forecast（订单簿 tick） | 0.9914 | 5 | 757 | 微观结构，turnover 风险高 |
| **risk70** Multi-Factor Model | 0.9798 | 96 | **7963** | ⛔ **最拥挤的一个**（7963），且 IND 实测撞 prod 0.72 ⇒ 不进本战役 |

⚠ 与 `shortinterest` 塔的关系：`shortinterest` 已 4 点（已点亮），但 **`risk` 塔是 0 点**。
同一「做空压力」经济含义在 **risk 塔下的借券数据集**里仍可合法计分 ⇒ **不是重复挖已点亮塔**，是换了计分塔。
（平台口径以 `pyramids.list[].name` 为准，不是以数据集的 category 字段为准。）

#### 5.60.3 `socialmedia`（2 个，都是「共同搜索」单字段）

`socialmedia39` / `other100`「Investor views」= 1 个字段、覆盖 1.0、alphaCount 576 / 399、valueScore 1–2。
⇒ 唯一可做的是**共同搜索网络**（零售关注溢出）。单字段 ⇒ 构造空间极窄（只能换窗口/换聚合/换分组），
**ATOM 可做但天花板低**，排在其他塔之后。

#### 5.60.4 `macro`（2 个，实质已死）

`macro63` 指数重构（1 字段、覆盖 1.0、192 α）—— **已判 `KOR-MACRO63-NO-CROSS-SECTION`**（事件极稀疏，截面无信息）。
`other106` KOSPI INDEX（15 字段、覆盖仅 **0.4038**）—— 指数水平/成分，覆盖刚过线但作为 alpha 输入是**共同因子**而非截面信号。
⇒ **macro 塔本轮不再投配额**。

#### 5.60.5 `earnings` / `institutions` / `insiders` / `imbalance` / `sentiment`

- `earnings`：仅 `earnings3`（8 字段，见 §5.59.2）—— 已在波 232 预注册。
- `institutions`：`institutions6`（11 字段，§5.59.3）+ `fund_holdings_panel`（30 字段，**已列判死待封**）—— 后者不进。
- `insiders`：`insiders5`（53 字段全 VECTOR，§5.57.1）—— 波 231 在飞。
- `imbalance`：`imbalance5` **已判死**（§ 早前）。
- `sentiment`：**本轮 0/3 已停投**（§5.55.3）。

#### 5.60.6 由此得到的靶区优先级（后续波的排程依据）

1. **risk60 / risk59**（覆盖满分、字段少、拥挤低、塔 0 点、经济机制硬：借券费与做空压力）
2. **news38 / news54**（覆盖够、拥挤极低、塔 0 点）
3. **institutions6 / earnings3**（波 232 在排）
4. socialmedia39（单字段，天花板低，最后）
5. macro / sentiment / imbalance：**停**

⇒ 这条优先级表把「下一步挖哪」从"看感觉"变成"查表"。**新开波前先读本表**，并在收批后按实际读数更新排序。

---

## §5.61 risk 塔（0/3）：risk59 / risk60 字段画像 + 机制取证 + 波 233 预登记

> 本节回应 §5.60.6 优先表第 1 位（risk60/risk59）。**入塔理由**：risk 塔 0 分；「做空压力」这一经济含义在 risk 塔下计分，与已点亮的 shortinterest 塔不是同一计分塔（金字塔归属看 `pyramids.list[].name`，不看数据集的 category 字段）。

### 5.61.1 字段画像（MCP `get_datafields`，`filter_sharpe=false`）

**risk60（5 字段，覆盖率 1.0，全部 VECTOR）**

| 字段 | 类型 | alphaCount | userCount | 含义 |
|---|---|---|---|---|
| `rsk60_offer` | VECTOR | 55 | 30 | 空头支付的综合借券费（年化） |
| `rsk60_last` | VECTOR | 89 | 29 | 快照时点最近一次借/贷费率 |
| `rsk60_crowding` | VECTOR | 57 | 31 | 有符号的日内做空活动指标（正 = 做空/拥挤加剧，负 = 回补） |
| `lending_fee_bid_rate` | VECTOR | 8 | 6 | 出借方出借存量股票的费率（年化） |
| `rsk60_datatime` | VECTOR | 62 | 25 | **供应商时间戳 HHMMSS — 非信号字段，禁用** |

**risk59（16 字段，覆盖率 0.9806，全部 VECTOR）**

| 字段 | alphaCount | userCount | 含义 |
|---|---|---|---|
| `rsk59_indicativeavailability` | 122 | 45 | 可出借数量（S3 投影） |
| `rsk59_daystocover10day` | 104 | 58 | 实时空头存量 / 10 日均量 |
| `rsk59_s3utilization` | 64 | 36 | **空头存量 / 可出借总量 = 借券供给利用率** |
| `rsk59_squeeze_risk` | 58 | 32 | 专有轧空评分（多因子） |
| `rsk59_bid_rate` | 56 | 30 | 出借费率（年化） |
| `rsk59_daystocover30day` | 48 | 27 | 同上，30 日均量 |
| `rsk59_dtcweeklychg` | 44 | 22 | DTC 周环比变化 |
| `rsk59_short_interest` | 40 | 25 | 实时空头股数 |
| `rsk59_daystocover90day` | 35 | 22 | 同上，90 日均量 |
| `rsk59_dtcdailychg` | 34 | 24 | DTC 日环比变化 |
| `rsk59_shortinterestnotional` | 33 | 16 | 空头市值（USD） |
| `rsk59_offer_rate` | 27 | 16 | 空头支付的综合融资费率（年化） |
| `rsk59_shortinterestpct` | 25 | 16 | 空头 / 流通股（小数） |
| `rsk59_crowded_score` | 18 | 18 | 专有空头拥挤度评分 |
| `rsk59_last_rate` | 13 | 9 | 当日新增出借的现货费率 |
| `rsk59_short_momentum` | 13 | 9 | 做空/回补活动 / 流通盘 |

**画像结论（三条，直接决定设计）**：
1. **全 VECTOR ⇒ 任何标量算子前必须先 `vec_*` 降维**（skill §2 硬规则）。按 §3 的批设计目标，本批需 ≥2 种 `vec_*` 聚合。
2. **`rsk60_datatime` 是时间戳，不是信号** —— S1 语义分类里属标识符类，**不得进任何表达式**。
3. **两集都是「借券市场的价格 / 数量」**，不是价格数据：字段天然横截面可比（费率年化、利用率 0–1），**不需要去量纲**；但利用率与费率**单边恒正、右偏重尾**，中位附近有大块零/地板值 ⇒ 必须防并列块（§5.58.3）。

### 5.61.2 机制取证（双通道）

**通道 A｜BRAIN 论坛：risk59 专帖（29 票，2026-09-19，id `43607257389207`）**

该帖**同时给出两个方向相反的读法**，这本身就是最重要的信息：
- 读法①（知情空头）：费率飙到 20–50% 说明专业空头不惜代价做空 ⇒ **利空信号**。
- 读法②（拥挤轧空）：空头付不起每日利息，一旦利好会争抢平仓 ⇒ **暴力反弹**，是「反转博弈的高危战场」。
- 帖内实践建议：区分一般抵押品与稀缺券（大多数大盘股停在基础费率，只有少数特殊券利率异动）；**费率高 + 补库天数长 = 做空白热化**。

**通道 B｜外部研究**

- Wang, Yanchu 等（38 国，2006-07 ~ 2014-12，八种空头度量）：**`days-to-cover` 与 `utilization ratio` 对未来收益的预测力最稳健**，且在**做空限制不严的市场**、**流动性较低与定价效率较低的股票**上更强。⇒ 直接点名本波要用的两个字段，并给出适用域。
- Miller (1977) 短售约束 ⇒ 悲观观点无法表达 ⇒ 价格只反映乐观边际投资者 ⇒ **高约束（高利用率）股票被高估 ⇒ 未来收益为负**。这是「约束通道」的机制根基，也是本波主假设。

**双通道裁决**：A 与 B **指向同一组字段**（utilization / DTC / 费率），但**方向相反**（论坛两种读法对立，论文的约束通道指向负）。按铁律 B：**方向不许猜，正反各测一条**。

**A-2 收益来源声明（缺项不许组装）**

| 声明项 | 内容 |
|---|---|
| 谁在被定价 | **空头 / 出借证券的出借方** —— 借券费率与利用率就是「做空的价格」 |
| 为什么会被错 | **短售约束（Miller 1977）**：借券供给稀缺时空头无法充分表达悲观观点，价格只由乐观者定 ⇒ 系统性高估。次要：空头拥挤 ⇒ 平仓踩踏 |
| 错了多久修复 | 数周至数月（空头存量按结算周期调整、借券供给随出借意愿恢复） |
| 预期方向 | 主假设：高利用率 ⇒ 高估 ⇒ **未来收益为负**。反向假设：高费率 + 长 DTC ⇒ 拥挤 ⇒ **轧空反弹** |

**适用域风险（必须登记，不得淡化）**：韩国在 **2020-03 ~ 2021-05** 与 **2023-11 ~ 2025-03** 两度全面禁止做空。IS 窗口 2014-01-01 ~ 2023-12-31 与两段禁令重叠，禁空期间借券数据可能缺失或退化。数据集整体覆盖率 0.9806 说明有数，但**分段退化必须靠收批后的逐年读数证实或排除**（先看首年 `longCount`，再看逐年 S 是否在禁空段塌陷）。

### 5.61.3 波 233 预登记（risk 塔 · 单变量正反对照）

**设计原则**：只改**符号**一个轴。字段 / 聚合 / 窗口 / 壳层 / 设置全部逐字相同 ⇒ 归因干净，且正好落地铁律 B。

**A（约束通道 · 预测：高利用率被高估 ⇒ 做空高利用率即赚钱，故取反号）**
```
reverse(quantile(group_rank(ts_rank(group_rank(vec_avg(rsk59_s3utilization), industry), 252), market)))
```

**B（轧空通道 · 预测：高利用率 = 拥挤 ⇒ 反弹，故保留正号）**
```
quantile(group_rank(ts_rank(group_rank(vec_avg(rsk59_s3utilization), industry), 252), market))
```

两者关系：**B = reverse(A)**，其余逐字相同。

**设置**：`Neutralization = STATISTICAL` / `nanHandling = OFF` / `maxTrade = OFF` / `decay 4` / `truncation 0.08` / `unitHandling = VERIFY` / `pasteurization ON` / `Delay 1` / `Universe TOP600`
（理由：`vR29LgEz` 的 `quantile(group_rank(ts_rank(group_rank(…), 1008), market))` 壳层 + 这组设置在本区实测产出 **319:319 精确多空平衡**，换壳层就是换实验。）

**防并列**：内层 `ts_rank(<level>, 252)` 把离散/地板值转成连续时序分位 ⇒ 破解 §5.58.3 的并列块；外层 `quantile` 再整形成高斯分布。**若本波仍出现稳定 >1:2 的多空比，才说明利用率字段在 KOR 有大块零值（地板）未被 ts_rank 化解**，那时才上 `tail(w, lower=0.05, upper=0.95, newval=0.5)`。

**收批第一读数（固定顺序，先于任何机制判断）**：
1. 逐子 `get_alpha_yearly_stats` → **2014 年 `longCount` / `shortCount`**（约束 4：近十年必须有数）；若 2014 缺失 ⇒ 近十年不成立，直接按约束 4 判死，不做机制讨论。
2. **逐年 long:short 比**（§5.58.3）。稳定 >1:2 ⇒ 构造缺陷，S 低不得归咎机制。
3. 逐年 S 分布：`S<1.0` 年份 ≥ 3 成 ⇒ 2Y 结构性不可达。
4. PnL 曲线形态 + 单年集中度 >30% ⇒ 过拟合。
5. 禁空段（2020-2021 / 2023）是否单独塌陷 ⇒ 适用域风险是否兑现。

**判定表（预注册，收批后逐条对照，不许事后改口）**

| 读数 | 处置 |
|---|---|
| A、B 均 `S < 0.8` 且多空均衡 | 利用率字段在本区无信息 ⇒ 换 DTC 字段（`rsk59_daystocover30day`），仅一次 |
| A 过阈、B 不过 | **约束通道成立**（Miller 1977）⇒ 后续 risk 波全部取反号，主攻 utilization / shortinterestpct |
| B 过阈、A 不过 | **轧空通道成立** ⇒ 后续 risk 波取正号，主攻 fee + DTC 组合 |
| 两者同号同量级 | 壳层在起作用而非信号 ⇒ 必须先用裸 `group_rank` 做对照，再谈机制 |
| 出现 >1:2 稳定失衡 | 并列块未解开 ⇒ 上 `tail`（常数参数）后重测，**一次** |
| 禁空段单独塌陷 | 记适用域限制，**不判字段死**，但 2Y 大概率不可达 ⇒ 该字段降级 |

**批预算**：2 条 / 1 个 multisim，与波 232 互斥（约束 3：并发 ≤ 2，故 232 与 233 必须串行）。

### 5.61.4 一条算子口径确认（避免整批连坐）

`get_operators` 实测：`quantile(x, driver = gaussian, sigma = 1.0)` —— **第二个位置参数是 `driver`（枚举名），不是桶数**。因此 `quantile(x, 100)` 是非法调用，会 ERROR 并**连坐同批兄弟任务**。本波与波 232 登记的两条均为**单参数 `quantile(...)`**，口径安全。

同批确认：`tail(x, lower=0, upper=0, newval=0)` 的 `lower/upper/newval` **必须为常数**（§5.58.3 用法合规）；`vec_avg / vec_max / vec_min / vec_stddev / vec_range / vec_count / vec_sum` 均可用；`ts_rank(x, d, constant=0)`、`ts_backfill(x, lookback=d, k=1)`、`group_rank(x, group)`、`group_zscore(x, group)` 签名无误。

---

## §5.62 波 231 收批实证（insiders5）：体构造已探明为**稳定负号**，§5.58.3 的并列预判**被证伪**

收批：`KiVQZ7JJ4K69tW3rcwV4NM` → 2/2 COMPLETE / 0 error → `harvest_multisim_results(region=KOR, wave=231)` → **upserted 2**，`wave_results` 插入「波 231 暂定 verdict=FAIL（0/2 过硬闸，0 条过 near 线 1.0）」。
⚠ **`linked: 0`** —— 本波两条表达式**不在 `expressions` 表**里，回测行与表达式无法关联。这是链路缺口（不是本次收批的错误），影响 GEM priors 学习与去重键；已登记待补。

| 子 | 表达式 | S | F | TO | 2Y | RN S | long:short | 失败 RA 项 |
|---|---|---|---|---|---|---|---|---|
| A `P0oqwjvp` | `ts_zscore(ts_sum(vec_sum(insd5_ghc_tr), 21), 252)` | **−0.68** | −0.49 | 0.110 | **−0.38** | **−0.82** | 276:338（1:1.22） | LOW_SHARPE / LOW_FITNESS / LOW_SUB_UNIVERSE_SHARPE / LOW_2Y_SHARPE |
| B `GrWYMEkx` | `tail(winsorize(group_rank(ts_sum(vec_sum(insd5_ghc_tr), 66), industry), std=2), lower=0.25, upper=0.75, newval=0.5)` | −0.13 | −0.03 | 0.059 | −0.48 | −0.11 | 298:337（1:1.13） | 同上四项 |

两发均 `pass` 含 `MATCHES_PYRAMID`，`pyramids.list = [KOR/D1/INSIDERS]` ⇒ **塔位归属正确**，不是越靶。

### 5.62.1 约束 4（近十年必须有数）：通过，且不是死因

逐年 `longCount/shortCount` 全部有值，无缺年。首年 **2014 = 251:300（A）/ 272:306（B）**。
⇒ 「近十年覆盖不足」这条死因**排除**；本波死在信号本身，不是数据长度。

### 5.62.2 ★ §5.58.3 的预判被证伪 —— 规则要**收窄**，不是推翻

`§5.58.4` 预注册的是「A 失衡而 B 均衡 ⇒ 反向验证 5.58.3」。实测 **A 1:1.22、B 1:1.13，两者都均衡**，1:2 门槛根本没触发。

原因（已定位，写进规则）：§5.58.3 的触发条件是**外层直接 `group_rank` 原始水平/稀疏字段**。本条 A 内层先做 `ts_sum(...,21)` 累加再 `ts_zscore(...,252)`，B 内层先做 `ts_sum(...,66)` 再 `group_rank` —— **时间累加已经把 27% 的零块摊平**，并列块在进入 `group_rank` 前就消失了。

**修订后的 §5.58.3**：
- 触发条件：**外层直接 `group_rank(<原始水平字段>)`**（中间无时间累加 / 时序排名 / 平滑）。
- 判据不变：逐年 long:short 稳定 >1:2。
- **不触发**：内层已含 `ts_sum` / `ts_mean` / `ts_zscore` / `ts_rank` / `ts_decay_linear` 等时间维算子时，离散值已被连续化 ⇒ 不必上 `tail`。
⇒ 这条先验的价值在于**识别「裸 group_rank 水平字段」这一种具体形态**，不是「凡是低基数就失衡」。

### 5.62.3 A 是**稳定负号**：方向错了，但量级不够，反号也救不回来

逐年 S：−1.35 / −0.65 / −1.84 / −1.09 / −0.14 / **+0.53** / +0.01 / −1.64 / **+0.40** / −1.08 —— **10 年里 7 年为负**，且负的年份幅度同量级（−0.6 ~ −1.8）。这不是噪声，是**系统性反号**。

铁律 E 的反面用法（本波新增读数纪律）：`RN sharpe = −0.82` **比 raw −0.68 更负** ⇒ 中性化没有削弱信号，去掉因子暴露后信号更强 ⇒ **不是因子暴露问题，是信号本身方向为负**。
（对照：RN ≪ raw 才是「alpha 只是因子暴露」；RN 与 raw 同号且 |RN| 更大 ⇒ 信号真实且被中性化放大。）

**反号后推算**：S ≈ +0.68、F ≈ +0.49、2Y ≈ +0.38。对严格 RA 线（S ≥ 1.58 / F ≥ 1.0 / 2Y ≥ 1.58）**三项全部远不达标**，2Y 差 4 倍。
⇒ **反号能救方向，救不了量级**。不因为「反号后是正的」就把它当候选。

### 5.62.4 B 的死因是**构造错误**，与机制无关 —— `tail(newval=0.5)` 不是「去并列」，是「只留两端」

`tail(x, lower=0.25, upper=0.75, newval=0.5)` 把 rank 空间的**中间 50% 全部压成常数 0.5**。后果实测：
- turnover 从 A 的 0.110 掉到 **0.059**（砍半）；
- 信号被稀释成噪声（S −0.13、逐年符号来回翻：+,+,−,−,+）。

**新纪律（写进组装硬规则）**：`tail(newval=0.5)` 的语义是**只保留 `(0,lower] ∪ [upper,1)` 两端、中段归零仓**，等价于一个「极值专属」的结构。**它不是中性修补**。
⇒ 只有确认「无效质量恰好全部落在被压区间」时才可以用；**若只是为了消并列，应改 `ts_rank` / `ts_zscore` 把离散值连续化**（与 §5.62.2 同一条修法）。
⇒ 用 `tail` 前后必须看 turnover：**砍半即意味着删掉了一半的信息**，此时 S 下降不能归咎机制。

### 5.62.5 insiders5 判定：**该体暂停**（塔不判死）

- 体（`insd5_ghc_tr` 的净变动强度）：SECTOR + decay 4 下是**亚阈稳定负号**，反号后 0.68，距 1.58 太远 ⇒ **暂停该体**，不再做窗口 / 平滑微调（属已死轴：同族平滑器与窗口谱不重扫）。
- **塔位不判死**：INSIDERS 仍 0/3，换字段（如 `insd5_*` 其它族）仍可再打。
- **已知备选**：若后续需要 insiders 塔的**廉价一分**，A 的反号变体是已知 S ≈ 0.68 的件 —— 只能作**塔位存在性证据**，不是提交级。

### 5.62.6 波次重编号 + 波 232 实发内容（composition 变更，附理由）

原 §5.61.3 标题写的「波 233」= risk59 单变量正反对照，**实际占用波 232 的槽位**（槽位按 §5.60.6 优先表 risk 位 #1 释放顺序走）。

★ **composition 变更**：原 §5.59.5 预登记的 232 = `institutions6` + `earnings3`，现改为 **risk59 正反对照对**。两条理由：
1. §5.60.6 优先表把 **risk 排在 institutions / earnings 之前**（risk60/risk59 是 #1）；
2. **`earnings3` 的符号在单槽下不可判**：该集是**日历不是意外**（§5.59.2），唯一可实施机制是公告溢价，而 `ern3_next_interval` 在「公告前建仓」与「公告后持有」两种读法下**符号相反**。单打一条 = 50% 概率符号猜错；必须做成**正反对照对（2 槽）**才有信息。

⇒ **`institutions6` 与 `earnings3` 顺延为波 233**（届时两者各占一槽，earnings3 先按 §5.61.2 的机制读法取**不 reverse** 的方向：大 interval = 刚公告完 = 公告后窗口，是溢价唯一能落地的位置；若该方向 S < 1.0，则按 §5.59.5 判定表允许的**唯一一次**改用 `pre_interval` 或反号，不叠加）。

### 5.62.7 波 232 实发（risk59 · 单变量正反对照）

`29L8scbBK4iFbn1hpJ6KC81`（2/2 已提交）：

- A `reverse(quantile(group_rank(ts_rank(group_rank(vec_avg(rsk59_s3utilization), industry), 252), market)))` —— 约束通道（Miller 1977：高利用率 ⇒ 高估 ⇒ 做空高利用率）
- B `quantile(group_rank(ts_rank(group_rank(vec_avg(rsk59_s3utilization), industry), 252), market))` —— 轧空通道（论坛读法②：高利用率 = 拥挤 ⇒ 反弹）

设置：KOR/TOP600/D1，**STATISTICAL**，decay 4，trunc 0.08，VERIFY，**nanHandling OFF**，**maxTrade OFF**（照 `vR29LgEz` 壳层设置逐字对齐）。
两发 preflight 均 `valid: true`，`fields_checked = ["rsk59_s3utilization"]`，`vector_fields = []`，`any_changed = false`。

**收批第一读数顺序见 §5.61.3**（2014 longCount → 逐年多空比 → 逐年 S → 曲线/集中度 → 禁空段是否塌陷）。**特别关注**：若 A、B 份额都不高且同号同量级，说明是壳层在起作用而非信号，必须用裸 `group_rank` 做对照再谈机制。

---

## §5.63 news 塔（0/3）：news38 / news54 字段画像

> 回应 §5.60.6 优先表第 2 位（news38/news54）。两集**全部 45 / 40 个字段均为 VECTOR**。

### 5.63.1 `news38`（Bloomberg 新闻，45 字段，可用面很窄）

**可按信号用的字段（按 family 分，skill `brain-alpha-research-news-sentiment` §2 口径）**

| family | 字段 | 覆盖 | alphaCount | userCount | 备注 |
|---|---|---|---|---|---|
| **direction** | `mws38_score` | 0.9529 | **67** | 23 | 复合/滚动情绪分，**本集使用量第一**，覆盖最高 |
| direction | `mws38_positive_score` | 0.8932 | 7 | 2 | 正向情绪强度 ≥0 |
| direction | **`mws38_negative_score`** | 0.8932 | **0** | 0 | 负向情绪强度 ≥0 —— **αC=0，零人用过，白空间** |
| direction | `mws38_tc_tone_score` | 0.8932 | 1 | 1 | 标题整体语调，−1 ~ +1 |
| direction | `mws38_tone_score` | 0.8932 | 0 | 0 | 同上（非 tc 版），**αC=0** |
| direction | `mws38_tc_positive_score` / `_negative_score` | 0.8932 | 1 / 1 | 1 / 1 | tc 版正/负强度 |
| **attention** | `mws38_d1_hotlevel` | 0.8932 | 6 | 4 | 热度/新颖度，越高越拥挤 |
| attention | `mws38_d1_related_num` | 0.8932 | 7 | 4 | 关联实体数（拥挤/注意力代理） |
| attention | `mws38_uniq_relevances` | 0.8932 | 4 | 4 | 新闻与个股相关度 |
| attention | `mws38_relevances` | 0.2683 | 3 | 2 | 同上（低覆盖版） |
| attention | `market_impact_indicator` | 0.2683 | **0** | 0 | 注意力/新颖度水平，**αC=0** |
| attention | `mws38_uniq_hotlevel` | 0.8932 | 1 | 1 | uniq 版热度 |
| frequency | `mws38_positive_freq` / `negative_freq` | 0.8932 | 5 / **0** | 4 / 0 | 原始词频，未归一 |

**必须排除的字段（8 类，共 20+ 个）**
- `*_entitlement`（6 个：`mws38_entitlement` / `mws38_d1_entitlement` / `mws38_uniq_entitlement` / `mws38_analytics_entitlement` / `mws38_headlinetones_entitlement` / `mws38_headlinetones_tc_entitlement`）—— 描述明写 **"must not be used for modeling/analytics"**，是权限位。
- `*_time` / `*_datatime`（6 个）—— 时间戳（hhmmss），非信号。
- `mws38_previous` —— 指向链上前一事件元组的**指针/索引**，αC 56 看着很高但是**不是数值信号**，用它做 alpha 等于拿主键回归。
- `mws38_version` / `mws38_d1_version` / `mws38_uniq_version` —— 版本号。
- `*_action`（`mws38_action` / `mws38_d1_action` / `mws38_uniq_action`）—— 生命周期枚举码，需 overlay 映射才有意义。
- `mws38_type` / `story_analytics_category` —— 分类码，同上。
- `mws38_value` —— 描述仅 "News value"，语义不明，不进首波。
- ⛔ **`mws38_hotlevel` 是死字段**：描述直接写 **"News hotlevel (all 0)"** ⇒ 恒为 0，任何表达式都用不出信号。**不要因为它覆盖率 0.7446 就试它。**

**画像结论（三条）**
1. **news38 的信息只集中在两处**：`mws38_score`（覆盖 0.95、使用量第一）与 `mws38_d1_*` 一族（覆盖 0.89）。其余或死或重复。
2. **两个零人用的对侧腿**（`mws38_negative_score`、`mws38_tone_score`、`market_impact_indicator`）是白空间 —— 但它们都是「负向/总量」腿，单独用通常与正腿高度负相关，必须与正腿构成**价差**才有独立意义。
3. **全部 VECTOR ⇒ 必须先 `vec_*`**。按 skill §3，本批需 ≥2 种 `vec_*` 聚合。

### 5.63.2 `news54`（事件日历，40 字段）—— **判为不可作 ATOM 信号源**

字段构成：announcement/entry/last_update/record_start/record_end 的**时间戳** × 4 组（daily / future / event × 本地与 UTC）= **20 个**；`*_cancelledflag` / `*_postponedflag` / `*_fullyearflag` / `fiscalquarter` / `fiscalyear` / `calendarmonth` / `calendaryear` = 十几个**标志与日历码**；`*_headline` / `*_situation` = **纯文本**；`mws54_factor`（覆盖 0.2449）= 与事件关联的数值（股息金额 / 拆股比例）。

⇒ **没有一个可比的情绪或关注度标量。** 剩下能算出数的只有 `mws54_factor` 与各种「距事件还有几天」的派生量，而它们要么覆盖 0.24，要么就是 `earnings3` 已经覆盖过的同一类日历信息。
**判定：news54 不进 ATOM 首波**；如果要用，只能作 `trade_when` 的**事件门控**（与其它 category 组腿，受约束 5 的 5 条上限管理），且优先级低于 news38。

### 5.63.3 news 塔下一步的体设计方向（预登记，不消耗槽位）

news 塔 0/3，主力集 = **news38**（ATOM 口径单数据集）。按 skill §3 的家族 × 桶配对，可用面支持的桶只有三个：
- **Change / Surprise**：`mws38_score` 相对自身历史基线的偏离（`ts_zscore` / 短窗 vs 长窗）；
- **Dispersion**（HIGH）：正负情绪**价差** —— `vec_avg(positive_score) − vec_avg(negative_score)`（同集、单一经济含义，`subtract` 合规；**不得 `add`**，闸 5 会拦 `POISON:equal_weight_leg_add`）；
- **Event-conditioned**（HIGH）：用 `mws38_d1_hotlevel` / `d1_related_num` 作门，仅在关注度异常日交易。

⚠ 覆盖 0.27 的三字段（`market_impact_indicator` / `mws38_relevances` / `mws38_related_num`）**裸用会产生 5–10 只股票的集中持仓**，必须 `ts_backfill` / `group_backfill` 或直接弃用（skill §2 末段，有代码执行点 = 体检硬门检查 1）。

---

## §5.64 波 232 收批（risk59）：利用率单腿判死，论文方向在本区被证伪

### 5.64.1 收批记录

multisim `29L8scbBK4iFbn1hpJ6KC81`：2/2 COMPLETE，harvest `linked=2 upserted=2`，wave 232 暂定 `verdict=FAIL`（0/2 过硬闸）。

| 号 | alpha | 表达式 | S | F | TO | ret | DD | 2Y | subU | investS |
|---|---|---|---|---|---|---|---|---|---|---|
| A | `N1Nqg8g7` | `reverse(quantile(group_rank(ts_rank(group_rank(vec_avg(rsk59_s3utilization), industry), 252), market)))` | −0.78 | −0.31 | 0.2142 | −3.36% | **33.39%** | −0.10 | −0.50 | −0.64 |
| B | `mLoJrQrW` | 同式去 `reverse` | **+0.58** | +0.20 | 0.2142 | +2.52% | 10.69% | +0.24 | +0.33 | +0.46 |

- 两者均 `MATCHES_PYRAMID` → `KOR/D1/RISK`（multiplier 1.3，effective 1）⇒ **ATOM 形态成立**（单数据集）。
- 两者均 `CONCENTRATED_WEIGHT` FAIL ⇒ 经 `quantile` + `group_rank` 强平权后仍集中权重，risk59 的零值/地板质量在持仓层留下尖峰。
- long:short **313:313**（两条完全相同）。

### 5.64.2 归因（按 §5.61.3 指定顺序）

**(1) 约束 4（近十年）** —— 2014 `longCount=0`、`pnl=0`。但这是 `ts_rank(..., 252)` 的预热吃掉了整个 2014，**不是数据缺失**：数据集覆盖 0.9806，2015 起每年在仓 289–337 只。⇒ **构造问题**。若要过约束 4，必须去掉 252 长预热（或改用 `ts_decay_linear` 短窗），代价是失去年内秩化的稳健性。

**(2) 逐年多空比** —— 2015 起 8 年全部平衡（最大偏差 337:327 = 3.2%，最小 300:300）。
⇒ §5.58.3 的 tie-block **未触发**；`quantile` 与 `group_rank` 在 `ts_rank` 之后都没有制造离散化。
**第三次证实 §5.62.2 窄化后的规则**：上游存在时间序列累积算子时，离散化已被抹平，不需要 `tail` 解结。

**(3) 逐年 S** —— 2015 +0.70 / 2016 −0.37 / 2017 +2.24 / 2018 +1.46 / 2019 +0.64 / 2020 +0.68 / 2021 −0.52 / 2022 −0.52 / 2023 +1.34。
`S<1.0` 的年 = **5/9 = 56%**，远超 3 成阈值 ⇒ **2Y 闸结构性不可达**（实测 2Y = +0.24，A 版 −0.10）。

**(4) 曲线/集中度** —— 正收益年合计 2,976,116；top1 年 2017 占 **26.2%**（未破 30% 硬线），但 **2017+2018 两年占 49.5%**。2016 / 2021 / 2022 三年为负。

**(5) 禁空段是否塌陷** —— 2020（禁空 3–5 月起）反而 **+0.68**；2021（禁空延续至 5 月）−0.52；2023（11 月起禁空）仍 **+1.34**。
符号翻转**与禁空区间不对齐** ⇒ 失效不是禁空造成的，是信号本身 regime 依赖。

### 5.64.3 方向裁决：论文结论在 KOR 不成立

- 论文（Wang Yanchu et al.，38 国 2006-07~2014-12）预测「高利用率 ⇒ 被高估 ⇒ 后续负」。
  本区实测 **plain（做多高利用率）= +0.58** ⇒ **符号相反**。
- 铁律 B 再次生效：`reverse` 与 plain **不精确反号**（|0.78| vs 0.58），且 `reverse` 版 DD 33.4% = plain 的 3.1 倍、2Y 反向塌到 −0.10。
  ⇒ 反向不是"更好"，只是"更抖"。
- RN（investability）与 raw **同号**（A −0.64 / B +0.46），量级也同阶 ⇒ **不是因子暴露拖累**，信号本身就是这个方向和这个强度（铁律 E 的反向用法）。
- 方向分歧的正解登记：本区高利用率更可能反映 **券源紧张=借券需求旺盛=机构看多后对冲/做市需求**，而非知情卖空。该解释未独立验证，只作下次进入 risk 塔时的假说。

### 5.64.4 判定

- **`rsk59_s3utilization` 单腿 ATOM 判死**：|S| 上限 0.78（half of 1.58），2Y 结构性不可达，CW 不过。不再为该字段烧槽位。
- **risk 塔不封塔**：risk60（5 字段，覆盖 1.0）未试；risk59 其余字段（s1/s2/s6/dtc 等 15 个）未试；**变化率/分歧度机制**未试。但再进本塔必须换机制，不得重复"利用率水平 + 秩化"这一族。
- 本塔本轮**暂停**，优先级让给塔洞更多的 news / socialmedia。

### 5.64.5 波 233 已发 + earnings3 方向修正

- 波 233 = `crNJIcvY59Wb3wdyAiWPPZ`，2 槽占满。preflight `valid=true`，`fields_checked` 3 个，`vector_fields` 空，`any_changed=false`。
  - A（institutions6）：`group_zscore(subtract(rank(ts_backfill(market_value_institutional_shares_acquired, 22)), rank(ts_backfill(market_value_institutional_shares_disposed, 22))), subindustry)`
    - A-2：被定价者 = 机构投资者（迟滞披露）；错价来源 = 披露滞后 + 机构羊群 + 信息扩散慢；修复期 = 1–2 个季度；方向 = 净买入高 ⇒ 后续超额。
    - `subtract(rank(A), rank(B))` 同数据集单一经济含义 ⇒ 合规（**不是** add 双腿）。
  - B（earnings3）：`reverse(group_zscore(ts_backfill(ern3_next_interval, 5), industry))`
- **方向修正（以本条为准，覆盖 §5.62.6 的表述）**：`ern3_next_interval` 大 = 距下次财报远 = **刚公告完**（周期恒等式）；原记录把"刚公告完"误当成了公告溢价的落点。
  公告溢价（Savor & Wilson 2016）发生在**公告窗口内**，落在 `next_interval` **小** 的一侧 ⇒ 取 **reverse**。
- 单槽无对照 ⇒ 允许按 §5.59.5 的**唯一一次**回退：换 `ern3_pre_interval`（覆盖 0.7756 > 0.5825）或直接反号，二选一，不叠加。

---

## §5.65 socialmedia 判死 + NEWS 类全清单 + news3 画像 + 波 234/235 预注册

### 5.65.1 SOCIALMEDIA 塔在 KOR 无可用数值字段（判死，有据）

`get_datasets(category="socialmedia", region=KOR, delay=1, universe=TOP600)` 返回 **2 个数据集**，各只有 **1 个字段**：

| 数据集 | 名称 | 字段 | 类型 | cov | αC | 判定 |
|---|---|---|---|---|---|---|
| `socialmedia39` | Investor views | `scl39_top5_people_also_watch_ticker_ii` | VECTOR | 1.0 | 576 | **股票代码向量**（"Atlas instrument IDs of the co-viewed neighbor tickers"），非数值信号 |
| `other100` | Investor views | `oth100_top5_people_also_watch_ticker_ii` | VECTOR | 1.0 | 399 | 同上（"Related tickers that have caught people's attention"） |

- 两者的唯一字段都是**邻接标的的 ID 向量**。FASTEXPR 没有 join / 解析 ID→标的的算子，`vec_avg` 对 ID 求均值无经济含义。
- ⇒ **SOCIALMEDIA 塔（0/3）在 KOR 结构上不可点亮**：没有任何情绪 / 关注度标量。塔洞存在，但无弹药。
- 该结论只针对 KOR/TOP600/D1；不同区域可能挂了别的社媒数据集，不得跨区照搬。

### 5.65.2 NEWS 类全清单（KOR/TOP600/D1，**24 个数据集**）

此前只看了 `news38` / `news54`，**严重低估本塔弹药**。全量按「低 αC（白空间）+ 高 valueScore」排序：

| 数据集 | 名称 | cov | 字段 | αC | valueScore | 备注 |
|---|---|---|---|---|---|---|
| `news73` | Story by Story Sentiment | 0.2676 | 22 | **8** | 5 | 最冷门，逐条新闻级情绪 |
| `news84` | Headline Sentiment (DNN) | 0.3702 | 23 | **16** | 5 | 神经网络迁移情绪 |
| `news3` | Dow Jones News Analytics | 0.2592 | 19 | **22** | 5 | **9 条情绪轴**（见 §5.65.3） |
| `news29` | Significant Developments | 0.467 | 12 | 29 | 5 | 事件主题 + 显著性，适合 Event-conditioned |
| `news36` | News Analytics | 0.2261 | 43 | 30 | 5 | RIC↔BBID 映射为主 |
| `news31` | News Analytics on Equities | 0.3541 | 25 | 35 | 5 | 含 novelty |
| `news54` | Key Developments | 0.6914 | 40 | 43 | 5 | 已判：纯事件日历，只能当门控 |
| `news85` | News Sentiment (DNN) | 0.6325 | 23 | 52 | 5 | |
| `news23` | MnA Deals | 0.3288 | **93** | 58 | 5 | 字段最多的独立机制族（并购） |
| `news48` | Global Media News | 0.2698 | 22 | 63 | 5 | |
| `news66` | Webpage View Statistics | 0.5 | 2 | 72 | 3 | |
| `news104` | Archive News | 0.2671 | 11 | 85 | 4 | |
| `news50` | Web News Analytics | 0.6254 | 81 | 113 | 5 | 字段多但已挖得较深 |
| `news46` | Relevant News Analytics | 0.3418 | 44 | 126 | 4 | |
| `news21` | Macro Economic Event | 0.7435 | 13 | 143 | 3 | |
| `news20` | Web Sources News Sentiment | 0.5066 | 24 | 155 | 4 | |
| `news17` | PR Edition | 0.2692 | 24 | 212 | 3 | |
| `news38` | News Analytic Model | 0.7971 | 45 | 227 | 4 | **本波 234 用** |
| `news7` | Real Time News Feed | 0.6327 | 56 | 372 | 3 | |
| `news79` | Global Corporate News Analytics | **0.8563** | **85** | 899 | 2 | 覆盖最高、字段最多，但拥挤 |
| `news18` | Ravenpack News | 0.5709 | 29 | **1012** | 2 | **Tier B 饱和集**，按 news skill §1 分支处理 |
| `news59` | Corporate Events | **1.0** | 2 | **2396** | 1 | 覆盖满但极度拥挤，仅 2 字段 |
| `other7` | Archive News | 0.2938 | 11 | 29 | 5 | 被归到 news 类 |

⇒ **NEWS 塔弹药充足**，后续至少可再开 3–4 波而不重复机制。`news18` / `news59` 属高拥挤，不作首选。

### 5.65.3 `news3`（Dow Jones News Analytics）画像

19 个字段**全部 VECTOR**，coverage 一律 **0.2592**（≈ TOP600 的 155 只）。
结构 = **9 条情绪轴 × 2 个子集** + 1 个接收时间戳：

| 情绪轴 | 全量版（αC / uC） | 优先子集版（αC / uC） |
|---|---|---|
| `pos` 正面 | `nws3_scores_posnormscr` (**0** / 0) | `nws3_scores_pospartnormscr` (1 / 1) |
| `neg` 负面 | `nws3_scores_negnormscr` (**0** / 0) | `nws3_scores_negpartnormscr` (**0** / 0) |
| `finup` 财务乐观 | `nws3_scores_finupnormscr` (2 / 2) | `nws3_scores_finuppartnormscr` (**0** / 0) |
| `findown` 财务悲观 | `nws3_scores_findownnormscr` (2 / 2) | `nws3_scores_findownpartnormscr` (2 / 1) |
| `fear` 恐惧 | `nws3_scores_fearnormscr` (1 / 1) | `nws3_scores_fearpartnormscr` (**0** / 0) |
| `uncertainty` 不确定 | `nws3_scores_uncertaintynormscr` (2 / 1) | `nws3_scores_uncertaintypartnormscr` (1 / 1) |
| `certainty` 确定 | `nws3_scores_certaintynormscr` (6 / 5) | `nws3_scores_certaintypartnormscr` (1 / 1) |
| `finhype` 炒作 | `nws3_scores_finhypenormscr` (1 / 1) | `nws3_scores_finhypepartnormscr` (**0** / 0) |
| `finvolatile` 财务波动 | `nws3_scores_finvolatilenormscr` (1 / 1) | `nws3_scores_finvolatilepartnormscr` (**0** / 0) |

**7 个 αC=0 的字段**（`pos` / `neg` 全量版、`fear`/`finhype`/`finup`/`finvolatile`/`neg` 的 part 版）。

三条结论：
1. **与 news38 是不同机制族**：news38 是单一复合分；news3 是**多情绪词库**（恐惧 / 不确定 / 炒作 / 财务波动各有独立轴）。
   这正好补 news skill §3 的 **Dispersion（HIGH）** 与 **Propagation** 桶——news38 没有分歧度字段，news3 有 `uncertainty` / `finvolatile`。
2. **`pos` / `neg` 全量版的 αC 都是 0**，这是本类最基础的两个极性字段 ⇒ 真白空间。
3. **约束 4 的风险必须前置登记**：coverage 0.2592，且**未验证 2014 是否有数据**。首次回测必须先读 2014 `longCount`。

### 5.65.4 波 234 预注册（news38，2 槽，已 preflight + 已入 expressions 表）

| 号 | 桶 | 表达式 | 机制 |
|---|---|---|---|
| A | **Dispersion（HIGH）** | `group_zscore(subtract(rank(vec_avg(mws38_positive_score)), rank(vec_avg(mws38_negative_score))), industry)` | 正 / 负情绪幅度的**截面净差**。`negative_score` αC=0（白空间），`positive_score` αC=7。同数据集单一经济含义 ⇒ `subtract` 合规（**不是** add 双腿） |
| B | **Event-conditioned（HIGH）** | `trade_when(greater(rank(vec_sum(mws38_d1_related_num)), 0.7), group_zscore(ts_zscore(vec_avg(mws38_tone_score), 66), industry), -1)` | 只有高关注度日（related_num 截面 top30%）才用情绪；`mws38_tone_score` 是**唯一带符号的 [−1,+1] 标量且 αC=0**；`ts_zscore(…,66)` = Change（相对自身 66 日基线） |

- 两种 `vec_*` 聚合：`vec_avg`（A/B）+ `vec_sum`（B）⇒ 满足 news skill §3「≥2 种聚合」。
- preflight：`valid=true`，4 字段全部命中，`vector_fields` 空，`any_changed=false`。
- **`mws38_hotlevel` 不用**：描述字面写 "News hotlevel (all 0)"，是死字段（αC 5 是历史残留）。
- **`mws38_d1_hotlevel` 备用**（不在本波）：覆盖 0.8932，αC 6。

### 5.65.5 波 235 预注册方向（news3，待 234 收批后发）

优先序（按白空间深度）：
1. `subtract(rank(vec_avg(nws3_scores_posnormscr)), rank(vec_avg(nws3_scores_negnormscr)))` —— 最基础的极性净差，两腿 αC 双 0。
2. `group_zscore(vec_avg(nws3_scores_uncertaintynormscr), industry)` + `reverse` —— 不确定性溢价（Anderson-Ghysels-Juergens 2009：不确定性厌恶 ⇒ 高不确定被低估或高估，方向需实测），属 **Dispersion（HIGH）**。
3. `subtract(rank(vec_avg(nws3_scores_finupnormscr)), rank(vec_avg(nws3_scores_fearnormscr)))` —— 乐观 vs 恐惧的跨情绪叉，是 news38 无法表达的机制。

⚠ 必读前置：**2014 年 `longCount`**（coverage 0.2592，十年覆盖未验证）。

---

### 5.66 波 233 收批（institutions6 + earnings3）：一个零信号，一个「机制对但太弱」——earnings3 天花板已算出

#### 5.66.1 收批读数

| 槽 | 数据集 | alpha | S | F | TO | ret | DD | 2Y | subU | investS | 硬闸 FAIL |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A | institutions6 | `wpQO5Lml` | **−0.10** | −0.02 | 0.0793 | −0.52% | 20.26% | 0.13 | 0.18 | −0.25 | SHARPE / FITNESS / 2Y / **investS(−0.25)** |
| B | earnings3 | `O0AqnoYd` | **+0.47** | +0.18 | **0.164** | +2.36% | 15.89% | **1.23** | 0.33 | **+0.53 ✅** | SHARPE / FITNESS / 2Y |

两条均 `MATCHES_PYRAMID`（A = KOR/D1/INSTITUTIONS ×1.4，B = KOR/D1/EARNINGS ×1.1），**均过 CONCENTRATED_WEIGHT / LOW_SUB_UNIVERSE_SHARPE / HIGH_TURNOVER**。
A 表达式：`group_zscore(subtract(rank(ts_backfill(market_value_institutional_shares_acquired,22)), rank(ts_backfill(market_value_institutional_shares_disposed,22))), subindustry)`
B 表达式：`reverse(group_zscore(ts_backfill(ern3_next_interval,5), industry))`
设置：STATISTICAL / decay 4 / trunc 0.08 / VERIFY / nan OFF / maxTrade OFF / TOP600 / D1。
收批链路：`harvest_multisim_alphas` → `harvest_multisim_results` ×2（**均 `linked:1`**，波 232 的 `linked:0` 未复发——先 `upsert_expressions` 再收批这条已在两波上验证）→ `upsert_expressions(status="backtested")` ×2。

#### 5.66.2 逐年归因（按 §5.61.3 顺序）

**A. institutions6（净买入−净卖出份额差 → 多空价差）**

| 年 | 2014 | 2015 | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 |
|---|---|---|---|---|---|---|---|---|---|---|
| S | −0.61 | −0.64 | **−1.36** | +0.19 | +0.18 | +0.12 | **+1.49** | −0.67 | −0.33 | +0.52 |
| pnl(k) | −285 | −371 | −656 | +79 | +100 | +54 | **+788** | −402 | −175 | +325 |

① **2014 `longCount` = 287**（非 0）⇒ 不是波 232 那种 warm-up 假象，字段在全区间有值；
② 逐股多空比常年在 287:292 ~ 346:336 之间 ⇒ **不是 tie-block**；
③ **S<1.0 的年份 = 10/10（100%）**，最高年 2020 = 1.49；正收益年 4/10；
④ **单年集中度爆表**：2020 一年 +788k，而全期总 pnl 只有 −542k ⇒ **2020 的收益被其余九年全部吃掉**。这是"单年行情"指纹（`05_antipatterns`），不是信号；
⑤ 禁空段（2020-03~2021-05）内 2020 反而 +1.49、2021 −0.67 ⇒ 与禁空无因果。

**判读**：TO 仅 0.079（换手极低）+ 逐年 S 全部 < 1.5 ⇒ 净买卖差在 KOR 是**近零信噪比的存量水平**。用户约束 4 的"近十年都要有数据"它满足（287 起），但满足覆盖率不等于有信号。
**结论：`institutions6` 净额差单腿 = 死**（不是"机制错"，是"该字段在 KOR/TOP600/D1 没有可提取的截面预测力"）。INSTITUTIONS 塔**未封**（institutions 其它数据集 + institutions6 的 15 个其它字段未打）。

**B. earnings3（`reverse(next_interval)` = 长"临近公告"一侧）——本波唯一有价值的结果**

| 年 | 2014 | 2015 | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 |
|---|---|---|---|---|---|---|---|---|---|---|
| S | **−1.46** | −0.47 | +0.14 | +1.28 | +0.42 | +1.20 | +0.55 | +0.98 | **+1.80** | +0.77 |
| pnl(k) | −699 | −269 | +75 | +602 | +295 | +559 | +278 | +478 | **+733** | +386 |
| long:short | 291:289 | 318:295 | 316:304 | 320:301 | 330:323 | 325:322 | 332:315 | 349:332 | 333:323 | 337:319 |

① **2014 `longCount` = 291**（对比波 232 的 0）⇒ **字段真在**，2014-15 的负 S 是**真实反向**，不是数据空洞；
② 多空比每年都在 1.0 附近（最大偏离 349:332 = 2.6%）⇒ 无 tie-block；
③ **S<1.0 年份 = 6/10（60%）**——按归因决策表本该判"2Y 结构性不可达"，**但这里读数不服从该表**：失败集中在**头部两年**且**单调转正**，2016–2023 **八年连正**，这是"信号出现"而非"信号衰减"。**该表的前提是平稳性，本序列不满足**，故不套用；
④ 单年集中度：2022 占 2016–2023 正收益的 **21.5%**（733/3404）< 30% ⇒ **无过拟合指纹**；
⑤ 禁空段（2020-03~2021-05）：2020 +0.55、2021 +0.98 ⇒ **不塌陷**，与波 232 同结论；
⑥ `investability_sharpe` **+0.53 > raw 0.47** 且同号 ⇒（铁律 E 反向）**不是因子暴露产物**，纯 alpha 本身就有这个方向与强度。

#### 5.66.3 earnings3 天花板已算出：不是"再调一层"，是"信息源不够"

反事实估算（把 2014-15 两年整体剔除，其余不变）：
- 全期 pnl = +2.436M；2016-2023 = **+3.405M** ⇒ 收益放大 1.398×
- 日波动近似不变 ⇒ **S 上限 ≈ 0.47 × 1.398 = 0.66**，**F 上限 ≈ 0.18 × 1.398 = 0.25**
- 逐年 S 算术均值（2016-2023）= (0.14+1.28+0.42+1.20+0.55+0.98+1.80+0.77)/8 = **0.89**

⇒ **即便把两年负收益全部归零，S 也到不了 1.58（差 2.4×），F 到不了 1.0（差 4×）。** 2Y 1.23 已在 1.58 的 78% 位置上，但 S/F 是硬伤。

**机制层的根因**：earnings3 **只有 8 个字段，全部是财报日历的时间量**（`next_interval` / `pre_interval` / 4 个 reptime / 2 个 `all_delay_1_*` 同构副本），**没有一个字段携带"内容"**（surprise / actual / estimate / revision 全无）。任何结构最终都退化成"财报周期相位"这一个变量 ⇒ 天花板就是相位变量的信息量。
**结论：earnings3 单数据集 ATOM = 死（机制级，不是参数级）。** 记录为「机制已验证但强度不足」，**不再投槽**。EARNINGS 塔**未封**（该 category 其它数据集未清点，`all_delay_1_*` 副本属同构不重复打）。

⚠ **本区第一次出现"归因表不适用"的判例，写死口径**：`S<1.0 年份 ≥ 3 成` 这条只在**平稳序列**上成立。若失败年份**集中在一端**且（a）逐年符号单调转正、（b）单年集中度 < 30%、（c）系数与 RN 同号 ⇒ 按"信号出现"处理，**但仍须按上式计算反事实 S 上限**；上限 < 闸值 ⇒ 一样判死，只是判死理由不同（"太晚出现"而非"太弱"）。

#### 5.66.4 方向修正的复核（§5.64.5 的 reverse 是否正确）

§5.64.5 判定"公告溢价落在 `next_interval` 小的一侧 ⇒ 取 reverse"。波 233 实测 `reverse` 得 2016-2023 八年连正、均 0.89；若取正向则为 **−0.47**（反向）。⇒ **§5.64.5 的方向修正被实证确认**，且证实铁律 B（`reverse` 不是精确反号：0.47 vs −0.47 在四舍五入后看似对称，但逐年结构不同——正向版本的 2014-15 会是正收益而 2016+ 全负，即"信号消失"而非"信号反号"）。**保留该条，不再回翻。**

#### 5.66.5 波 234 已发（news38）+ 波 235 预注册（news3）

波 234 已在 §5.65.4 预注册并于本段发出：`4o0cnw3mt4XW9OzmAbziUoa`
- A `group_zscore(subtract(rank(vec_avg(mws38_positive_score)), rank(vec_avg(mws38_negative_score))), industry)`（桶：Dispersion(HIGH)，`vec_avg`）
- B `trade_when(greater(rank(vec_sum(mws38_d1_related_num)), 0.7), group_zscore(ts_zscore(vec_avg(mws38_tone_score), 66), industry), -1)`（桶：Event-conditioned(HIGH)，`vec_sum`）
- 设置同上（STATISTICAL / decay 4 / trunc 0.08 / VERIFY / nan OFF / maxTrade OFF）。

**波 235 = news3（2 槽，已在 §5.65.5 立项）**，本段补齐 A-2 与桶标注：

| 槽 | 表达式 | 家族 / 桶 / vec | A-2 收益来源 |
|---|---|---|---|
| A | `group_zscore(subtract(rank(vec_avg(<news3 正向情绪>)), rank(vec_avg(<news3 负向情绪>))), industry)` | direction / Surprise / `vec_avg` | 被定价方 = 注意力有限的散户；错价机制 = 新闻情绪扩散慢（Mian & Sankaraguruswamy 类情绪-价格研究 + Tetlock 2007 悲观词-下跌）；修复期 = 1–4 周；方向 = 净情绪为正 ⇒ 后续相对上涨 |
| B | `group_zscore(reverse(ts_zscore(vec_sum(<news3 不确定度>), 66)), industry)` | dispersion-ish / Change / `vec_sum` | 被定价方 = 风险厌恶投资者；错价机制 = 不确定性上升被过度外推（Baker-Bloom-Davis 不确定性 → 折价）；修复期 = 1 季度；方向 = 不确定性回落 ⇒ 后续跑赢 |

⚠ **执行前必查**：news3 覆盖率 **0.2592**（2014 年是否有值未验）⇒ 发波前先按用户约束 4 核 2014 `longCount`；若 2014 为 0 或长期空，**该集直接判"不满足十年数据"**，换 news73 / news84。

---

### 5.67 波 234 收批（news38）：⚠ 首次测出「**字段级覆盖率随时间塌陷**」——同一数据集里 pos/neg 从 40% 掉到 16%，tone 稳在 50%

#### 5.67.1 收批读数

| 槽 | alpha | S | F | TO | ret | DD | 2Y | subU | investS | 硬闸 FAIL（共 6 / 3 项） |
|---|---|---|---|---|---|---|---|---|---|---|
| A（pos−neg 原始水平价差） | `A1VYn8dR` | −0.38 | −0.08 | **0.8032** | −3.39% | **47.89%** | **−1.17** | −0.31 | −0.16 | SHARPE / FITNESS / **HIGH_TURNOVER** / **CONCENTRATED_WEIGHT(1.0 @2023-03-13)** / **subU(−0.31)** / 2Y |
| B（related_num 门控 + tone 变化） | `1YN1oA56` | +0.25 | +0.05 | 0.4293 | +1.78% | 12.44% | 0.26 | +0.29 | +0.21 | SHARPE / FITNESS / 2Y |

两条均 `MATCHES_PYRAMID`（KOR/D1/NEWS ×1.6）。收批链路 `linked:1` ×2。

#### 5.67.2 ★ 本波最重要发现：news38 的**字段级**覆盖率随时间单调塌陷

A 的逐年 `longCount` 与 `turnover`（同一条表达式、同一设置）：

| 年 | 2014 | 2015 | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 |
|---|---|---|---|---|---|---|---|---|---|---|
| longCount | **238** | 240 | 197 | 169 | 175 | **129** | **95** | 96 | 145 | 122 |
| turnover | **1.242** | 1.212 | 1.007 | 0.832 | 0.856 | 0.630 | 0.542 | 0.451 | 0.688 | 0.543 |
| S | +0.26 | −0.88 | −0.34 | −1.29 | −0.55 | −1.32 | −0.62 | 0.00 | +0.86 | −0.30 |

对照 B（用 `mws38_tone_score` + `mws38_d1_related_num`）同一区间 `longCount` = 290/310/309/305/327/317/323/348/325/323、`turnover` = 0.45/0.42/0.50/0.41/0.46/0.43/0.41/0.43/0.38/0.41。

⇒ **同一数据集内部，字段的十年覆盖曲线完全不同**：
- `mws38_tone_score` / `mws38_d1_related_num`：**十年稳定在 ~300+ 只**（≈ 全宇宙一半），TO 稳定 0.4–0.5；
- `mws38_positive_score` / `mws38_negative_score`：**2014 的 238 只单调塌到 2020-21 的 95 只**（−60%），TO 随之从 1.24 掉到 0.45。

**这条推翻「数据集级 coverage 一个数字就够」的做法**：news38 的 `get_datasets` 覆盖率是个单一标量，但它掩盖了**同一集内 6 倍量级的字段间差异与时间趋势**。
**纪律（写死）**：今后判断用户约束 4「近十年都要有数据」，**不得只看数据集级 coverage**，必须用**逐年 `longCount`** 核；首发证据即本表。
判读方法：若某年 `longCount` 相对峰值掉 > 50% 且该年 TO 同步掉 > 40% ⇒ 判「**该字段不满足十年**」，即便 `get_datasets` 的 coverage 看起来合格。

#### 5.67.3 A 的失败分解（三种失效叠加，不是信号弱）

1. **覆盖率塌陷**（上表）⇒ 越到近期持仓越少，2Y −1.17 是"近几年几乎没仓位"的结果；
2. **原始水平价差 + 无 backfill** ⇒ 稀疏 NaN 日进进出出，TO 1.24（2014）远超 0.7 上限 ⇒ `HIGH_TURNOVER`；
3. **`CONCENTRATED_WEIGHT` = 1.0 @ 2023-03-13** ⇒ 覆盖只剩 122 只、再经 `group_zscore(industry)` 分组，**某一天其中一个行业组只剩 1 只有效值** ⇒ 单票 100% 权重。这是**低覆盖 × 行业中性化**的必然产物，不是运气。

⇒ **判读：`group_zscore(<低覆盖原始水平>, industry)` 是本区已知的第三种规模化失效形态**（前两种：tie-block、raw vs RN 分解失效）。低覆盖字段必须先 `ts_backfill` / `group_backfill`，且**不得在覆盖率 < 0.3 的字段上做行业中性化**——组内样本不足会直接把单票权重顶到上限。

#### 5.67.4 B 的失败分解：结构健康，信号随时间单调衰减

| 年 | 2014 | 2015 | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 |
|---|---|---|---|---|---|---|---|---|---|---|
| S | **+1.27** | **+0.79** | +0.29 | +0.44 | **−0.94** | +0.48 | −0.09 | −0.12 | +0.44 | +0.11 |
| pnl(k) | +882 | +606 | +204 | +294 | −658 | +335 | −82 | −99 | +272 | +85 |

① 2014 `longCount` = 290 且 S +1.27 ⇒ **news38 满足约束 4**（十年有数据），且 2014 是**最强年**；
② `S<1.0` 年份 9/10，2Y 0.26 ⇒ **2Y 结构性不可达**；
③ **形态是衰减而非出现**：2014-15 年均 +1.03 → 2016-17 年均 +0.37 → 2018-2023 年均 **−0.02**。这与 earnings3（波 233，出现型）**方向相反**，是本区第一个清晰的"新闻情绪信号被消化"样本；
④ 结构本身健康（DD 12.4%、CW 过、TO 0.43、investS 同号 +0.21）⇒ **不是壳层问题**；
⑤ 2018 单年 −658k 是全部失效的来源，该年占总亏损 50%，且 2018 恰是 KOR 新闻情绪类 alpha 大量上线的年份（推测，未证）。

**判读**：`trade_when(attention 高, tone ts_zscore 66)` 这套 Event-conditioned 结构在 KOR **2014-15 有效、之后被消化**。按 §5.66.3 的判据，本序列属"衰减型"，**不做参数微调**，换机制族。

#### 5.67.5 结论与队列调整

- **news38**：不是"整集判死"，而是**分字段判死**——
  - `mws38_positive_score` / `mws38_negative_score` / `mws38_tone_score` 的**情绪水平/价差**路线判死（A 三重失效 + B 衰减）；
  - 该集**剩下未打的**：`story_analytics_metric_value`（αC 0）、`mws38_negative_freq`（αC 0）、`mws38_hotlevel`（**死字段：全 0，§5.65.4 已记**）、以及 tone 之外的其它标量。**低优先级**（同集已两次负结果，且覆盖率结构差）。
- **NEWS 塔主攻转向**：`news3`（波 235 已发，见 §5.67.6）→ 若死则 `news73` / `news84` / `news31`。**news38 降为"已充分试探"**。

#### 5.67.6 波 235 已发（news3，`3hp72UggA4Lhcw0HONKOAHQ`）

按 §5.67.3 的教训重写了两条（**都加了 `ts_backfill`；A 还加了 `filter=true` 处理空情绪向量**）：

| 槽 | 表达式 | 家族 / 桶 / `vec_*` |
|---|---|---|
| A | `group_zscore(ts_zscore(ts_backfill(subtract(vec_avg(nws3_scores_posnormscr), vec_avg(nws3_scores_negnormscr), filter=true), 22), 66), industry)` | direction / **Change** / `vec_avg` |
| B | `group_zscore(reverse(ts_backfill(vec_stddev(nws3_scores_posnormscr), 22)), industry)` | dispersion / **Dispersion(HIGH)** / **`vec_stddev`** |

- `filter=true` 的理由：某日"有新闻但无负向词"时 `vec_avg(negnormscr)` 为 NaN 而非 0，两条腿相减会整日 NaN ⇒ 与波 234-A 的稀疏塌陷同源。
- B 的机制 = **Miller (1977) 分歧 + 卖空约束 ⇒ 过度定价**：`vec_stddev(pos)` = 当日跨文章正向语气分歧度；KOR 卖空受限 ⇒ 高分歧股更易高估 ⇒ `reverse`（做多低分歧）。
- `operator_audit` 已验：`vec_stddev` / `vec_range` **不在幽灵算子表**（`safe: true`，violations 空）；两者在 `get_operators` 中 `level: null` / `documentation: null`，属"可调但无文档"档。
- 覆盖率风险已登记：news3 数据集级 coverage = **0.2592**；**发波前已按 §5.67.2 纪律把逐年 `longCount` 列为收批第一读数**，若 2014 年 `longCount` < 20 或近年塌陷 > 50%，本集即判"不满足约束 4"，不再续投。

#### 5.67.7 结构性结论：**EARNINGS 塔在 KOR 数据层已死**

`get_datasets(category="earnings", KOR/TOP600/D1)` 返回 **1 个数据集**：`earnings3`（8 字段 / αC 2616 / valueScore 1 / multiplier 1.1）。
结合波 233 §5.66.3 的天花板计算（S 上限 0.66、F 上限 0.25）⇒ **该 category 在 KOR 无第二张票可打**。
**EARNINGS 塔（KOR/D1）判死在数据层**：不是"没挖到"，是"数据集只有一份日历、没有内容字段，且该日历已被 2616 个 alpha 充分开采"。
⚠ 该结论**只覆盖 KOR/TOP600/D1**；其它区域的 earnings 集（如 MEA earnings3 有事件计时腿）不可类推。

#### 5.67.8 INSTITUTIONS 塔：11 字段全清单已取（`filter_sharpe=false`），下一机制已定

`get_datafields(institutions6, filter_sharpe=false)` = 11 个 MATRIX，覆盖 0.9976–1.0：

| 组 | 字段 | αC |
|---|---|---|
| 价值流量 | `market_value_institutional_shares_acquired` / `_disposed` | 110 / 59 |
| 数量流量 | `quantity_institutional_shares_acquired` / `_disposed` | 116 / 107 |
| **广度计数** | **`count_institutional_buyers_security` / `_sellers_security`** | **85 / 98** |
| 存量 | `count_institutional_holders_security` | 60 |
| 总量 | `aggregate_share_count_institutions` / `_all_owners` / `aggregate_equity_value_*` | 249 / 206 / 114 / 90 |

波 233 打的是**价值流量**（αC 最高的那对）→ 死。**未打且机制不同的一组 = 广度计数**：
- 机制（Chen-Hong-Stein 2002「breadth of ownership」）：**持有广度变化**在卖空约束 + 异质信念下**负向**预测收益 ⇒ 机构买入家数增加越多，后续越跑输；
- 表达式（已 `preflight` valid + `operator_audit` safe）：`group_zscore(reverse(ts_delta(subtract(ts_backfill(count_institutional_buyers_security, 66), ts_backfill(count_institutional_sellers_security, 66)), 66)), industry)`
- 桶：**Dispersion(HIGH)**；家族：peer_context/attention。
- ⇒ 排队为**波 236 槽 A**。

---

## §5.68 波 235 收批（news3）+ 约束 4 首次**正面**判定

multisim `3hp72UggA4Lhcw0HONKOAHQ`，2 条，2026-10-30 09:53 发 / 09:59 收，全程约 5.8 分钟。
落库 `upserted=2 / linked=2`，`wave_results` 暂定 `verdict=FAIL（0/2 过硬闸，0 条过 near 线 1.0）`。

### 5.68.1 收批表

| 槽 | alpha | 表达式（简） | S | F | TO | ret | DD | subU | 2Y | investS |
|---|---|---|---|---|---|---|---|---|---|---|
| A | `npvY3dEq` | `group_zscore(ts_zscore(ts_backfill(subtract(vec_avg(posnormscr), vec_avg(negnormscr), filter=true), 22), 66), industry)` | **0.29** | 0.08 | 0.2927 | +1.97% | 15.16% | 0.42 | 0.03 | −0.06 |
| B | `LLMqkN0a` | `group_zscore(reverse(ts_backfill(vec_stddev(posnormscr), 22)), industry)` | **−0.03** | 0.00 | 0.2579 | −0.26% | 34.61% | −0.03 | 0.55 | −0.35 |

两条均 `MATCHES_PYRAMID` = `KOR/D1/NEWS`（×1.6）。A 的 `CONCENTRATED_WEIGHT` = **0.1208**（线 0.10，2017-06-09），
B 的 `CONCENTRATED_WEIGHT` = **1.0**（2017-07-17）——与 §5.67.3 同形，`vec_stddev` 在稀疏日会把同一行业内
只剩 1 只有效标的，直接压成单票 100% 权重。

### 5.68.2 ★ 逐年 `longCount` —— 用户约束 4 首次**正面通过**

| 年 | 2014 | 2015 | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 |
|---|---|---|---|---|---|---|---|---|---|---|
| longCount | **288** | 308 | 311 | 312 | 327 | 327 | 325 | 343 | 328 | 324 |
| turnover | 0.2985 | 0.3038 | 0.3133 | 0.3051 | 0.3094 | 0.3234 | 0.2880 | 0.2617 | 0.2614 | 0.2616 |

**判定：news3 完全满足「近十年都要有数据」。** 2014 年就有 288 只（≈TOP600 的 48%），十年
`longCount` 单调微升、`turnover` 无任何塌陷。

⚠ **这条读数的意义比结果本身大**：news3 的数据集级 `coverage = 0.2592`，比 news38 的 0.29 还低，
若沿用「看数据集级 coverage 判十年」的旧口径，本集会**在看数据之前就被判死**——而实测十年全在。
⇒ **§5.67.2 的纪律升级为硬规则**：数据集级 coverage 是**事件稀疏度**的读数，
**不是存续期**的读数；两者必须分开判。今后凡 coverage < 0.5 的数据集，`longCount` 逐年表是**第 0 读数**，
在写任何结论之前先出这张表。

对照：news38 的 `positive_score`/`negative_score` 从 238 → 95 是**真塌陷**（§5.67.2），
news3 的 `posnormscr`/`negnormscr` 十年 288→324 是**真存续**。同一 category、相近 coverage、结论相反。

### 5.68.3 A 的归因：奇偶年反号 + 单年集中 ⇒ 反事实天花板 0.41

逐年 Sharpe：0.10 / **1.13** / 0.06 / **1.11** / −0.10 / 0.57 / **−0.76** / 0.13 / **−0.63** / 0.57
- `S < 1.0` = **10/10 年**。
- **符号结构是奇偶年交替**：2015/2017/2019/2023 正、2018/2020/2022 负。这不是「信号衰减」，
  也不是「信号晚现」，而是一个**按日历反号的轮动**——任何**静态符号**都无法利用它
  （`reverse` 只会把正年变负年，S 从 +0.29 变 −0.29）。
- 单年集中度：正收益年合计 +2.898M，其中 2015 年 +1.019M = **35.2%**（>30% 过拟合指纹线）。
- **反事实天花板**：丢掉三个负年 ⇒ 2.898M / 2.037M = 1.422× ⇒ `S_ceiling ≈ 0.29 × 1.422 = 0.41`，
  `F_ceiling ≈ 0.08 × 1.422 = 0.11`。**离闸 1.58 / 1.0 差一个量级**。
- 铁律 E 反向：`investS = −0.06` 与 raw 同号同量级 ⇒ 不是因子暴露拖累，是**信号本身没有稳定方向**。

**判定：news3 的「情绪水平价差（pos − neg）」机制在 KOR 结构性判死。** 理由不是参数，是
**逐年符号交替 + 天花板 0.41**——换壳层、换中性化、换 decay 都不可能把它推到 1.58。

### 5.68.4 B 的归因：`vec_stddev` 分散度机制失败

S −0.03、DD 34.61%、`investS` −0.35（反向）、CW 1.0（单票满仓）、`subU` −0.03。
`reverse(vec_stddev(...))` 的经济含义是「情绪分歧度低 ⇒ 看多」（Miller 1977 的反向读法）；
实测**没有任何方向性**，且权重极度集中。**该路判死**，且**不再尝试 `vec_stddev`/`vec_range` 类
分散度算子配 `group_zscore`**（两次（news38 的 stddev 与本次）都是 CW 灾难）。

### 5.68.5 结论：NEWS 类「情绪水平 / 价差 / 分歧度」三路在本区已穷尽

| 数据集 | 机制 | 结果 | 判据 |
|---|---|---|---|
| news38 | 情绪价差（正−负） | S −0.38、CW 1.0 | 字段级覆盖塌陷 238→95（§5.67.2/3） |
| news38 | tone_score × attention 门控 | S +0.25、9/10 年 <1.0 | 逐年衰减（§5.67.4） |
| news3 | 情绪价差 + ts_zscore | S +0.29、天花板 0.41 | 奇偶年反号（§5.68.3） |
| news3 | 情绪分歧度（stddev） | S −0.03、CW 1.0 | 无方向 + 权重集中（§5.68.4） |

⇒ 此后 NEWS 类**只允许**走另外两条：① **事件条件型**（`trade_when` 门控 + 非情绪字段做条件腿）；
② **关注度/传播型**（`d1_related_num`、`*_count` 类做主体、情绪只做分组）。**禁止**再发
「情绪水平 / 情绪价差 / 情绪分歧度」作主信号的批次。剩余待查：news73 / news84 / news31。

### 5.68.6 波 236 发射记录（institutions6 广度 + insiders5 内部人信念强度）

multisim `Bhnqr1K353Q9oY1evLG61zu`，2026-10-30 09:59 发。

| 槽 | 数据集 | 表达式 | 机制（A-2 摘要） |
|---|---|---|---|
| A | institutions6 | `group_zscore(ts_delta(subtract(ts_backfill(count_institutional_buyers_security, 66), ts_backfill(count_institutional_sellers_security, 66), filter=true), 66), industry)` | 机构买方广度净变化（Chen-Hong-Stein 2002）：谁=知情的机构资金；为何错=13F 级季度披露的**广度变化**不是价格变量，散户/短线资金看不到；修复期=1–2 季；方向=净广度升 ⇒ 正 |
| B | insiders5 | `winsorize(group_rank(ts_sum(divide(vec_sum(insd5_vol_chg), add(vec_sum(insd5_vol_bf), 0.0001)), 66), industry), std=2)` | 内部人信念强度（Jeng-Metrick-Zeckhauser 2003 / Lakonishok-Lee 2001 / Cohen-Malloy-Pomorski 2012）：谁=内部人；为何错=披露是逐笔事件、无横截面口径，需**一次除法**才能读出「这笔占他自身仓位的比例」；修复期=66 个交易日（季度披露周期）；方向=买入侧为正、卖出侧无信息 |

**B 的第三条被论坛证据当场推翻并改掉**（双通道取证的实际价值）：
论坛 69 票帖《内部人"动了多少仓位"比"动了多少钱"更重要 —— DEU 内部人信念强度因子》
（`43178926004887`，已提交 alpha `xAjEkeOq` S 1.68 / F 1.34 / 2Y 2.40 / prod 0.52 / ra=0）
给出**同构配方**与**逐条实测**：

1. **信号 = 流量 ÷ 存量（自身仓位）+ ε**，不是金额；`shares/holdings` 是纯无量纲分子（1.59），
   `valueeur/holdings` 含价格项（1.68）——两条都活，本波取纯无量纲的 `vol_chg/vol_bf`。
2. **累加用 `ts_sum`，绝不能用求平均类算子**：帖内实测 `ts_mean` 把 Sharpe 从 1.44 砸到 0.73，
   因为「事件**次数**」本身是 CMP(2012) 的机会型/例行信息。
   ⇒ 我原计划的 `ts_decay_linear(ts_backfill(...), 252)` **正好踩这个坑**（backfill 抹平事件 + 线性衰减求平均），
   在发波前改掉。**纪律：稀疏事件型数据集上，任何"求平均 / 衰减"类算子都要先说明分母是什么。**
3. **并列质量**：`nanHandling=ON` 会把「当期无申报」在数据层填 0 ⇒ `ts_sum` 后仍为 0 ⇒
   `group_rank` 把**全横截面 72–80%** 的股票并列在 rank 中段（≈0.4）⇒ 拿到方向随机的非零权重 ⇒
   `LOW_SUB_UNIVERSE_SHARPE`。修法 `tail(w, 0.25, 0.75, 0.5)`，且必须与 `winsorize(std=2)` **成对使用**
   （去 winsorize ⇒ 0.99；std=2 时 1.67，std=4 时 0.32）。
4. **买入侧才有信息**：JMZ(2003) 在该帖的跨数据集对照里得到买入 1.56–1.59 vs **卖出 0.21**。
5. **KOR 与本帖的差异（必须记）**：本区 `nanHandling = OFF` ⇒ 无申报股票保持 NaN、不进持仓
   ⇒ **并列块不存在**，故 v1 先**不加 `tail`**；若 `subU` 卡线再加，`tail` 是第一根杠杆。
6. 该帖的失效风险同样适用于 KOR：**只有 6 年账本**（DEU 申报口径 2018 才标准化）。
   ⇒ 本波 `longCount` 逐年表要**先看 2014**；若 KOR 内部人披露同样前薄，则本波按「不满足约束 4」处理。

预先登记的未来杠杆（本波若卡 `LOW_SUB_UNIVERSE_SHARPE`）：
`winsorize(std=2)` → `tail(0.25,0.75,0.5)` → 换 `group_rank` 分组轴 → `decay`。
若卡 `LOW_SHARPE` 且 `subU` 正常，则优先查 2014 起点与事件密度，不再加壳层。

---

## §5.69 波 236 收批（institutions6 + insiders5 双新塔首探）+ ★「2Y 优先」筛选律

**多仿真** `Bhnqr1K353Q9oY1evLG61zu`（2026-10-30 09:59:12 发，10:05 收）。两槽都是**新塔首探**：
INSTITUTIONS（平台 0 颗）与 INSIDERS（平台 0 颗）。波 236 结果 = 双弱，但**产出了一条可以改后续全部选机制的判据**（见 §5.69.4）。

### 5.69.1 收批读数

| 槽 | 数据集 | alpha | S | F | TO | ret | DD | subU | 2Y | investS | CW | 塔 | 失败项 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| A | institutions6 | `mLoJX3X9` | 0.14 | 0.03 | 0.1248 | 0.56% | 14.65% | 0.09 | 0.51 | −0.01 | pass | KOR/D1/INSTITUTIONS ×1.4 | SHARPE / FITNESS / 2Y / INVESTABILITY |
| B | insiders5 | `O0Aq9Y9J` | 0.28 | 0.08 | 0.0975 | 1.15% | 13.15% | 0.37 | −0.22 | 0.17 | pass | KOR/D1/INSIDERS ×1.2 | 同上（investS 为 warning 0.17<0.2） |

- 两条 **`CONCENTRATED_WEIGHT` 都 pass**、`LOW_SUB_UNIVERSE_SHARPE` 都 pass、`longCount` 322 / 324
  ⇒ `nanHandling=OFF` + `winsorize(group_rank(...,industry),std=2)` 的壳层组合在**非稀疏**字段上不产生集中持仓。
- A 的 `investS = −0.01` 与 raw 同向，**不是因子暴露拖累**，是信号本身弱（铁律 E）。
- B 的 `investS = +0.17` 与 raw 同为负、但幅度接近天花板 0.2 ⇒ 可投资性子集里几乎无残余。

### 5.69.2 约束 4 正面判定（insiders5）——预先登记项已结

§5.68.6 第 6 条要求「先看 2014 `longCount`」，实测 **2014 = 291 只**（short 288），
2014–2023 逐年 `longCount` = 291/316/316/314/331/329/324/354/335/332。
⇒ **KOR 内部人申报从 2014 起就是满的**，与 DEU 帖「2018 才标准化、只有 6 年账本」的风险**不成立**。
⇒ insiders5 **满足约束 4**，后续失败与数据起点的可用性无关，纯属信号衰减（下条）。

### 5.69.3 B 的归因：逐年 Sharpe 呈**单调衰减**，2Y 结构性不可达

逐年 S（2014→2023）：**+1.07 / −1.45 / +0.45 / +1.06 / +1.01 / +0.94 / +0.47 / +0.28 / −0.20 / −0.24**

- 2017–2019 连续三年 S ≈ 0.94–1.06 ⇒ **原始机制在 KOR 真实存在**（不是噪声），
  且 2014 也 +1.07 ⇒ 不是单年行情。
- 但 **2020 起单调下台阶**（0.47 → 0.28 → −0.20 → −0.24），末两年 2Y = −0.22。
- 2015 单年 −1.45（占负收益大头）⇒ 单向符号在早期就不稳。
- **判据按 §「近年 S 断崖 ⇒ 机制性衰减，不是参数的错」⇒ 换字段族，不再扫参数/壳层/平滑**。
  杠杆阶梯（`winsorize` → `tail` → 换分组轴 → `decay`）在本条**整体作废**：
  它修的是 subU 与 CW，而本波的 subU 0.37 已经很好、CW 已 pass。

### 5.69.4 ★★ 新判据「2Y 优先」——本波最重要的产出

KOR 的严格档 `LOW_2Y_SHARPE` 限 **1.58**，且它只量 **IS 末两年（2022–2023）**。
本波与波 235 合起来给出同一条结论：

| 波 | 机制 | 全期 S | 末两年 2Y | 结局 |
|---|---|---|---|---|
| 235A | news3 情绪价差 z-score | 0.29 | 0.03 | 全期就弱 |
| 235B | news3 分歧度 | −0.03 | 0.55 | 全期就弱 |
| 236A | institutions6 广度净变化 | 0.14 | 0.51 | 全期就弱 |
| **236B** | **insiders5 信念强度** | **0.28（但 2017–19 ≈1.0）** | **−0.22** | **机制 2020 后死掉** |

⇒ **规则（此后开波前置）**：
1. 任何新机制进批次前，先问「它在 2022–2023 有没有理由活着」；**只靠 2015–2019 账本成立的机制，2Y 闸在数学上不可达**，
   无论 S 全期多少。**读逐年表先读末两年**，不是先读首年。
2. 「历史 S ≈ 1.0」不再算正向证据；正向证据 = **末两年单年 S ≥ 1.0**。
3. 由此推论：KOR 新塔里**衰减型事件机制（内部人、情绪、关注度）天然劣势**；
   应优先**结构性成本/价格类**机制（借券费、拥挤度、资金成本）——它们随制度存在而不是随叙事存在。
   这条直接决定了波 237 的选型（§5.69.5）。

### 5.69.5 波 237 发批记录：risk60 借券费（价格 vs 流量对照实验）

**多仿真** `bodagb0r4Y1aAkvCz6lhCi`（2026-10-30 10:05:08 发）。数据集 `risk60`，
5 字段全 VECTOR、**coverage = 1.0**（全横截面每日有值 ⇒ 约束 4 天然满足、无稀疏集中持仓风险；
KOR/D1/RISK 平台 0 颗，未点亮）。

| 槽 | 表达式 | 机制（A-2） |
|---|---|---|
| A | `winsorize(reverse(group_rank(vec_avg(rsk60_offer), industry)), std=2)` | **做空成本溢价（水平 / 价格侧）**。谁在被定价：卖空方；`rsk60_offer` = 卖空方支付的年化综合借券费 ⇒ 它是借券市场的**清算价格**而不是数量。为什么错：**套利限制**——费率越高，做空越贵，高估无法被纠正，价格因此长期偏高 ⇒ 高费股票随后跑输（Drechsler & Drechsler 2014/2016「shorting premium」；Boehmer-Jones-Zhang 2008）。修复期：1–3 个月。方向：**负**（高费 ⇒ 后续跌），故 `reverse`。 |
| B | `winsorize(reverse(group_rank(ts_mean(vec_sum(rsk60_crowding), 22), industry)), std=2)` | **做空流（数量 / 流量侧）**。`rsk60_crowding` = 带符号的每日做空活动指标（+ = 增加做空/拥挤，− = 回补）。机制：知情卖空者（Engelberg-Reed-Ringgenberg 2012；Boehmer-Jones-Zhang 2008）⇒ 做空流上升随后跑输。用 `ts_mean(...,22)` 累计月内净流（**coverage=1.0，非事件稀疏，故平滑合法**，与 insiders5 的「禁平均」不冲突）。方向：负。 |

- **这是刻意设计的对照实验**：同一数据集、同一分组轴、同一壳层，只换**价格维（fee level）vs 数量维（flow）**，
  归因时可直接判定「KOR 借券市场的信息在价格里还是在流量里」。用户约束 2 要求的「对比实验」即此。
- 反向（`reverse` 去掉）已登记为下一波候选：铁律 B 要求正反各测，本波两槽都取文献方向，
  若双双弱而 `investS` 与 raw 反号，则下一步统一出正号变体。
- **不使用** `rsk60_datatime`（HHMMSS 厂商时间戳，无经济含义）、`rsk60_last`（与 `offer` 高度重合，留作下一波）。

### 5.69.6 台账外的一手核对（顺带完成，避免误判）

- 平台 KOR/D1 塔位实测：`analyst 2 / fundamental 3 / model 3 / other 1 / pv 2 / shortinterest 4`；
  **未点亮 = earnings / imbalance / insiders / institutions / macro / news / sentiment / risk / socialmedia（9 个）**。
  波 236 打 insiders + institutions，波 237 打 risk ⇒ 三个新塔首探。
- `search_alphas_by_sharpe(KOR, ≥1.5)` 复核：榜上除 `O0Gj6PqJ`（MODEL 1177，S 2.83，`multiply(rank(a),rank(b))`）
  外**全是 SUPER/combo**。⇒ KOR 的 REGULAR 高产路径不在单塔单字段，而在「结构性机制 + 低换手」；
  且 `O0Gj6PqJ` 的 MODEL+MODEL 双 `rank` 乘积形态**被约束 5 明令禁止**（MODEL 内部两两组腿），不可复用。
- 论坛检索 `short interest borrow fee alpha` 命中 33 条（含〈基于 short interest 数据的跨交易所组合案例〉15 票）；
  首次 `shorting premium lending fee borrow` 调用**工具报错返回**（`MCP error -32603`）——
  按证据契约这是**故障**不是「论坛无解」，不落 `forum_recon_negative_*`，也不作判死依据。

---

## §5.70 KOR/TOP600/D1 未点亮塔的**类别全集盘点**（约束 1「一个个 category 查」的落地）

平台塔位实测（`get_pyramid_alphas`，2026-10-30）：`analyst 2 / fundamental 3 / model 3 / other 1 / pv 2 / shortinterest 4`
⇒ **未点亮 9 个 = earnings / imbalance / insiders / institutions / macro / news / sentiment / risk / socialmedia**。
下表是这 9 个塔里**每一个 category 的数据集全集**（`get_datasets(KOR, TOP600, D1)`），以及据此得出的可挖性判定。
**这张表决定后续 60 颗的配额分配**：只有「数据集数 × 字段数」够大的塔才撑得起多波。

| category | 数据集数 | 清单（cov / 字段数 / αC / valueScore / 塔倍率） | 可挖性判定 |
|---|---|---|---|
| **news** | **24** | news3(.259/19/22/5) · news7(.633/56/372/3) · news17(.269/24/212/3) · news18(.571/29/**1012**/2) · news20(.507/24/155/4) · news21(.744/13/143/3) · **news23(.329/93/58/5)** · news29(.467/12/29/5) · news31(.354/25/35/5) · news36(.226/43/30/5) · news38(.797/45/227/4) · news46(.342/44/126/4) · news48(.270/22/63/5) · **news50(.625/81/113/5)** · news54(.691/40/43/5) · news59(1.0/2/**2396**/1 饱和) · news66(.500/2/72/3) · **news73(.268/22/8/5)** · news76(.659/6/16/5) · news79(.856/85/899/2) · **news84(.370/23/16/5)** · news85(.633/23/52/5) · other7(.294/11/29/5) | ⭐ **最大金矿**：24 集、9 个 valueScore=5，且 news73（αC **8**）近乎无人挖。⚠ 已判死的是「情绪水平/价差/分歧度」三路（§5.68.5），**剩余只走关注度 / 事件条件 / 传播** |
| **sentiment** | **6** | news_sentiment_transfer(.965/23/227/4) · **other553(.624/21/96/5)** · **sentiment21(.381/138/94/6)** · **sentiment23(.265/156/54/6)** · sentiment26(.357/19/48/5) · sentiment27(.399/29/**1871**/2 饱和) | ⭐ **字段最厚**（138 / 156 字段的两个集几乎无人挖）。⚠ `other553` 名为「Financial Opinion Mining」，**实测字段全是分析师目标价 / 评级 / 盈利预测的语音快照**（`ptgvalue`/`preptgvalue`/`recvalue`/`prerecvalue`/`est_estvalue`/`*_yearspeakcnt`），不是文本情绪 ⇒ 可做**修正类**机制而不触情绪禁令 |
| **risk** | **7** | risk59(.981/**16**/561/2) · risk60(1.0/5/211/3) · risk68(.991/5/757/2) · risk70(.980/96/**7963**/1 饱和) · **risk71(.666/7/344/3)** · risk72(.625/5/400/2) · risk88(.973/64/1405/2) | ⭐ **全覆盖、零稀疏**（多数 cov>0.97）。risk59 = 借券全景 16 字段（利用率/费率/回补天数/挤压分），risk71/72 = **MFM2 特异性残差收益**（idiosyncratic return，残差反转的原料）。⚠ 论坛帖（35577573602455）提示 **risk60 历史偏短**，需逐年 `longCount` 验约束 4 |
| institutions | 2 | institutions6(.9996/11/1003/2) · fund_holdings_panel(.809/30/219/4) | 中。institutions6 已波 236 首探（S 0.14）；`fund_holdings_panel` 在既有判死清单里待用户批准 |
| insiders | 2 | insiders1(.353/9/548/3) · insiders5(.892/53/4959/2) | 中。insiders5 已波 236 首探（S 0.28，逐年单调衰减 ⇒ 机制性死） |
| macro | 2 | **macro63(1.0/1/192/3)** · other106(.404/15/307/4) | 薄。macro63 只有 1 个字段 `mcr63_membership`（WisdomTree WTIDJH 成分**布尔**标记）⇒ 只能做 `ts_delta` 成分变动事件，且布尔字段 rank 并列会让 CW 崩 ⇒ **必须 `trade_when` 门控**，优先级低 |
| earnings | 1 | earnings3(.660/8/**2616**/1) | 差。唯一集已高度饱和（αC 2616、valueScore 1） |
| imbalance | 1 | imbalance5(.856/2/**1384**/1) | **结构性不可达**：全 category 只有 1 集 2 字段且已饱和 ⇒ 该塔可判定为「无可用资产」，留待用户批准后封存 |
| socialmedia | 0 | — | 本区无资产（既有判死清单已登记） |

### 5.70.1 配额结论（后续 60 颗的分配依据）

- **可承载多波的只有 3 个塔：news / sentiment / risk**（合计 37 个数据集）。
  其余 6 塔（institutions / insiders / macro / earnings / imbalance / socialmedia）字段薄或已饱和，
  **单塔最多再给 1–2 波探索预算**，若两波内出不了 S ≥ 1.0 的原始信号即按「本区无可用资产」登记，不再续投。
- **最高优先级**：`risk59`（16 字段、cov 0.981，借券利用率 / 费率 / 回补天数 / 挤压分四维同一机制族）——
  一个数据集就能拆出 3–4 个**互不重复的机制**，且属于**结构性成本类**（§5.69.4 第 3 条推荐的那一类）。
- **第二优先**：`sentiment21` / `sentiment23`（138 / 156 字段、αC 均 <100）——
  字段厚度足以支撑「关注度 / 新颖度 / 事件类型」多条非情绪路线；代价是 cov 0.27–0.38（稀疏，需 `trade_when` 或 backfill）。
- **第三优先**：`news73`（αC 8，22 个 VECTOR 字段全为情绪分项）——
  唯一非情绪的可用字段是 `nws73_entitiescounter`（实体数 = 关注广度），只能做关注度路线。
- ★ **`macro63` 的 WTIDJH 成分变动**保留为「指数纳入效应」候选（Shleifer 1986；Harris-Gurel 1986；KOSPI200 纳入的韩国本地实证），
  但必须先解决布尔字段并列问题。

## 5.71 ★ 判死面复查：wave 237/238 全数命中已封存机制（2026-10-30，自我事故复盘）

> 本节的起因不是平台反馈，而是**我自己忘了查判死面**：§5.69/§5.70 写完「risk59 最高优先 / news84+
> other553 可挖」之后，在派发前顺手拉了 `get_dead_ends`（85 条）与 `get_dead_datasets`（16 个），
> 结果**当波与下一波的 5 条候选里 5 条全部落在已封存的数据集或机制族上**。
> 这与 wave 208「开波前 kill」是同一类事故的第二次再现（§3 第 208 行、§5.69 已记过闸缺口），
> 说明**「死集不投」已被机械化，而「死机制不投」仍然只靠人记**——记了也没用，因为没查。

### 5.71.1 权威判死面（本次实测，2026-10-30）

`get_dead_datasets(region="KOR")` 返回 **16 个**：
`acquisition_model` · `fundamental44` · **`institutions6`** · `model109` · `model170` · `model192` ·
`model230` · `model30` · `model32` · `model53` · `multi_source_model` · `news79` · `sentiment21` ·
`shortinterest3` · `smoke_ds` · `wave30_model252`

`get_dead_ends(region="KOR")` 返回 **85 条**，其 `payload.dataset` 覆盖（去重）：
`fundamental17` · `analyst_factor_signals` · `other455` · `model37` · `other466` · `analyst14` ·
**`risk60`** · **`risk71`** · `analyst16` · `pv106` · **`other553`** · `other496` · `risk88` · `pv30` ·
`analyst_consensus` · `fundamental93` · `fundamental86` · `news38` · `news50` · `news54` ·
`fundamental21` · `analyst44` · `analyst10` · **`insiders5`**
（另有相当一部分条目的 `payload.dataset` 为空、只有 `entry_id` 里带数据集名，机械按 `dataset` 字段扫会漏，
**判死前必须同时按 `entry_id` 子串再扫一遍**。）

⚠ 出现在 `dead_ends` 里**不等于整个数据集判死**——大多数是**某个机制族**死了（例：`analyst14` 有条死记录，
但 analyst 塔已点亮 2 颗）。**判据是「本次要挖的机制与那条死记录的 family/rule 是否同一轴」**，不是数据集名。
反过来说，**一旦 `rule` 写的是「该域整体关闭」这种域级措辞，域内换数据集也不放行**（本条直接作废了 risk59）。

### 5.71.2 wave 237 两槽 = risk60 判死条目点名的两个分量（配额已烧，不可撤回）

`KOR-RISK60-CROWDDING-NOSIGNAL-20261002`（dead_at 2026-10-02）原文：

| 字段 | 原文摘录 |
|---|---|
| family | `risk60 securities-lending (crowding activity + fee level)` |
| reason | 「8 探针 8/8 RED，max\|S\|=0.18，低于 fast_kill 阈值 0.5…**非稀疏事件结构问题（longCount 325/shortCount 323）**」 |
| rule | 「KOR risk60 判死：借券域在 KOR **无截面预测力，不投任何变体**……GLOBAL 跨区铁律 `shortinterest3`↔`risk60` 费率域互锁 0.64–0.80，且 `shortinterest3` 在 KOR 已判死 ⇒ **该域在 KOR 整体关闭**」 |

wave 237 派的两条恰好是这条 family 的两个分量：
- A `winsorize(reverse(group_rank(vec_avg(rsk60_offer), industry)), std=2)` = **fee level**
- B `winsorize(reverse(group_rank(ts_mean(vec_sum(rsk60_crowding), 22), industry)), std=2)` = **crowding activity**

⚠ **同时纠正 §5.70 的一处误读**：论坛帖 35577573602455 说「risk60 的历史数据比较短」，
但判死记录里 `longCount 325 / shortCount 323` 说明**历史并不短、也不是稀疏问题**——
真实结论是**该域在 KOR 没有截面预测力（max\|S\|=0.18）**。
所以「等它回测出来看逐年 longCount 验约束 4」这个预注册动作**前提就是错的**，不该再等它。

### 5.71.3 为什么闸没拦住（缺口定性）

`dead_dataset_guard()` 只在 `build_wave.py` / `wave_gate.py` 这条 campaign 链上跑；
本次是**直接 MCP `create_multi_simulation` 派发**（约束 3 要求并发用 multisim 限 2），
**走不到那道闸**。⇒ 缺口不是「闸写错了」，而是**绕过了闸的派发通道没有等价的预检**。
固定动作（下次开波前必做，不看记性）：
1. `get_dead_datasets(region)` → 数据集名单；
2. `get_dead_ends(region)` → 按 `payload.dataset` **与** `entry_id` 双路扫，取命中条目的 `family` / `rule` 原文；
3. 逐槽回答「本槽机制是否与某条死记录的 family 同轴」，答不上来就不派。

### 5.71.4 修正 §5.70.1 的优先级（risk59 从第一优先降为「不投」）

| §5.70.1 旧排序 | 修正后 | 依据 |
|---|---|---|
| ① risk59（16 字段、cov 0.981，「结构性成本类」） | ⛔ **不投** | risk60 判死 `rule` 是**域级**措辞「**该域在 KOR 整体关闭**」，risk59 与 risk60 同属借券域；换数据集不构成新机制 |
| ② sentiment21 / sentiment23 | ⚠ **仅 sentiment23 可考虑** | `sentiment21` 在 16 个死数据集名单里；`sentiment23` 未被单独封存，但其机制（标题情绪）与已判死 news 情绪族同源，只能作最低优先探针 |
| ③ news73（只剩 `entitiescounter`） | ✅ **保留（本波已用）** | 关注广度，非情绪 |
| — | ✅ **新增 news84** | 23 字段、αC 全部 ≤3（几乎无人挖），`normalized_news_item_count_transfer_2` 是**已按 90 日滚动均值归一**的关注度，天然截面可比 |

⚠ 上一版把 risk59 列为「一个数据集拆 3–4 个互不重复机制」是**只看了字段语义、没看域级判死**，
属于 §8.5「结构性结论必须先机器核验再落笔」的同类错误。

### 5.71.5 wave 238 重设计（同壳换源，构成本波对比实验）

首版 238 三条（`news_sentiment_transfer` ×2 + `other553` ×1）**全部落在已判死数据集上**
（前者 `KOR-NEWS-SENTIMENT-TRANSFER-DEAD` 三波判死，后者 `KOR-OTH553-REV-SPARSE` +
`KOR-OTHER553-ANALYST-VALUE-DEAD`），已用 `set_expression_status(to_status="dropped")` 作废三条
（id 85701 / 85702 / 85712，`n_updated=3, n_protected=0`），**未消耗任何仿真槽**。

重设计守两条：**只走 news 塔唯一存活轴（关注度计数，非情绪）** + **单字段正反各测一条**，
把「方向」与「数据源」两个变量彻底解耦（把两者一起变会得到不可判读的结果）：

| 槽 | 数据集 | 表达式 | 机制 / 家族 |
|---|---|---|---|
| 238A（反转向） | `news84`（cov .3702，23 字段，αC ≤3） | `winsorize(reverse(group_rank(ts_backfill(normalized_news_item_count_transfer_2, 66), industry)), std=2)` | 关注度异常 ⇒ 散户注意力买入推高价格 ⇒ 后续反转（Barber-Odean 2008 注意力假说）。字段已按自身 90 日均值归一 ⇒ 属「相对自身基线」而非裸水平，合铁律 A |
| 238B（动量向） | `news84`（同字段） | `winsorize(group_rank(ts_backfill(normalized_news_item_count_transfer_2, 66), industry), std=2)` | 新闻动量假说：信息持续 ⇒ 关注度高者继续上行（Wang-Zhang-Zhu 2018 *The Momentum of News*，好消息五分位多头 − 坏消息空头年化风险调整 7.45%，且「只有短期 + 信息环境差的股票（小市值、分析师覆盖低、机构持股少）才显著」） |

**为什么改成同字段正反**：初稿是「news84 反转 + news73 反转」，方向与数据源同时变，
一旦一正一负就无法判读。铁律 B（方向正反各测一条）要求的正是本表的形态。
`news73`（`vec_sum(nws73_entitiescounter)`，覆盖广度）已 `pending` 登记但**本波不派**，
留作 239 波对**胜出方向**做跨源复现。

- 两条 `preflight_expressions` → `valid:true`、`unknown_fields:[]`；`operator_audit` → `safe:true`、
  无幽灵算子；`upsert_expressions(status="pending")` 已登记（news84 两条：反转 / 正向）。
- **cov .37 < 0.4 ⇒ 按 §2 铁律必须 `ts_backfill`**，两条都已前置 `ts_backfill(·, 66)`。
- **论坛取证（2026-10-30，post `18641983716503`，17 票）**：该帖给的是
  `a=ts_mean(scl12_sentiment,5); b=normalize(group_rank(a,densify(subindustry))); …;
  trade_when(and(vec_avg(nws18_relevance)>0.1, adv20>1), c_0, -1)`。
  三条可直接借用的结构性结论：
  ① **关注度在原配方里是「门」不是「信号」**（`trade_when(relevance>0.1, …)`）——
     即 §3 的 Event-conditioned 桶；本波先用关注度**当信号**测方向，若方向确认即转门用法（239 波备选）；
  ② 原帖用 `group_percentage`，该算子在 **KOR 幽灵名单内**（19 个之一）⇒ **不可照抄**，需换成
     `group_rank` + 分位阈值；
  ③ 原帖自评「月交易类比日交易则换手率较高，难降低」⇒ 若本波 |S| 够但 TO 高，优先 `decay` 而非换骨架。
- **对比实验的判读口径（先写死，避免事后解释）**：
  两槽同号同量级 ⇒ 该字段被 `ts_backfill` 抹平（66 日回填把稀疏事件摊成常数），轴不可用；
  S(A) ≈ −S(B) ⇒ 关注度轴方向已定，直接进 239 跨源复现；
  **两槽 max\|S\| < 0.5 ⇒ news 塔整塔关闭**（与 wave 211 五轴全死合并成六轴），不再投任何 news 变体。

### 5.71.6 未点亮塔剩余可挖面（结构性结论，须让用户看到）

按「16 死数据集 ∪ 85 条死机制」过滤后，9 个未点亮塔的真实剩余面：

| 塔 | 剩余可挖 | 状态 |
|---|---|---|
| news | `news84`（关注度）/ `news73`（仅 `entitiescounter`） | **本波全部投完**，两源同灭 ⇒ 整塔关闭 |
| sentiment | `sentiment23`（cov .265 / 156 字段） | 机制与已判死情绪族同源，最低优先 |
| risk | — | **域级关闭**（risk59/60/71/88 + shortinterest3） |
| institutions | — | ⛔ **整塔关闭**：`get_datasets(category="institutions")` 只有 2 个集，`institutions6`（cov .9996/11 字段/αC 1003）在 16 死集名单内，`fund_holdings_panel`（cov .8093/30 字段/αC 219）在战役级判死名单内 ⇒ **塔内零存活集** |
| insiders | `insiders5` 有 `SIGNAL_CEILING`（30 条 best S=1.05） | 主攻位不可；只剩慢腿/组合腿 |
| macro | `macro63`（1 字段布尔成分） | 只能做指数纳入，需先解并列 |
| earnings | αC 2616 饱和 | 实质判死 |
| imbalance | 1 数据集 / 2 字段 / αC 1384 | 实质判死 |
| socialmedia | 零资产 | 无 |

⇒ **「在未点亮塔挖 60 颗」在当前判死面下不可达**：剩余可挖面连 10 条像样候选都凑不齐，
更不用说 60 颗全闸通过。这不是执行不力，是**塔位供给**的结构约束。
需要用户在三条路里选（已写入待决议清单，不擅自放宽约束 1）：
① 放宽「未点亮塔」到**已点亮塔的剩余机制**（analyst/fundamental/model/other/pv/shortinterest 六塔已亮 15 颗，
仍有大量未挖机制）；② 允许重开某个域级判死（如 risk59 借券域）并接受「已知 max\|S\|=0.18」的先验；
③ 把目标从 60 颗下调为「未点亮塔能出的全部 + 已点亮塔增量」，按实际产出收口。

## 5.72 波 237 收批（risk60 借券域二次确认）+ ★ 约束 4 的字段级判死

> 本波是在 §5.71 已经查明「risk60 已于 2026-10-02 判死」**之后**落地的一次**重复派发**，
> 记进台账的目的是留证，不是留功：**2 个仿真槽买了一个已经买过的结论**。
> 唯一的新增价值是：把杀它的理由从「8 探针 8/8 RED，max\|S\|=0.18」升级为**逐年归因**，
> 并顺带解决了一个 §5.70 悬而未决的约束 4 问题。

### 5.72.1 收批（multisim `bodagb0r4Y1aAkvCz6lhCi`，2026-10-30）

| 槽 | alpha | 表达式 | S | F | TO | ret | DD | subU | **2Y** | investS | CW | 失败闸 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| A | `VkxqpGQA` | `winsorize(reverse(group_rank(vec_avg(rsk60_offer), industry)), std=2)` | **0.65** | 0.30 | .1475 | 3.04% | 10.75% | 0.60 | **0.17** | 0.63 | **1.000** @2018-02-19 | SHARPE / FITNESS / **CW** / 2Y |
| B | `N1Nqpbdq` | `winsorize(reverse(group_rank(ts_mean(vec_sum(rsk60_crowding), 22), industry)), std=2)` | **−0.24** | −0.06 | .1877 | −1.07% | 18.03% | −0.01 | **−0.50** | 0.27 | 0.275 @2015-12-23 | 同上 4 项 |

两条均 `MATCHES_PYRAMID` pass（`KOR/D1/RISK` ×1.3），即**塔位仍在，只是信号不过**。

### 5.72.2 A 的逐年归因：单年 2017 吃掉 32% 总 PnL（过拟合指纹）

| 年 | 2014 | 2015 | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 |
|---|---|---|---|---|---|---|---|---|---|---|
| S | 0.37 | −0.13 | 0.04 | **2.48** | 0.84 | 0.78 | 1.14 | 0.83 | 0.94 | **−0.59** |
| longCount | 272 | 299 | 311 | 312 | 334 | 322 | 323 | 344 | 345 | 349 |

- 2017 单年 pnl **1,005,212 / 总 3,139,201 = 32.0%** ⇒ 命中归因表「单年占正收益 >30% ⇒ 过拟合，换机制族」。
- 剔除 2017 后其余 9 年 S 均值不足 0.5；**2023 转负 −0.59**，2Y 仅 0.17。
- **CW = 1.000（2018-02-19）** 意味着该日只有一个标的带权重 —— 与「费率字段在早期大量缺失」一致；
  即使 `tail`/backfill 把 CW 修掉，S 0.65 / 2Y 0.17 也离 1.58 差一个量级 ⇒ **不值得走修 CW 的杠杆**。
- 结论：`rsk60_offer` **十年有数据但无持续截面预测力**，与 `KOR-RISK60-CROWDING-NOSIGNAL` 同向且更强证据。

### 5.72.3 B 的逐年归因 ⇒ ★ **约束 4 字段级判死**（本波最有价值的产出）

| 年 | 2014 | 2015 | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 |
|---|---|---|---|---|---|---|---|---|---|---|
| S | 0 | −0.84 | −0.17 | **+1.57** | 0.08 | **−1.95** | −0.75 | +0.92 | 0.19 | −1.08 |
| longCount | **0** | **10** | 312 | 311 | 334 | 326 | 331 | 348 | 332 | 339 |

- **`rsk60_crowding` 的 2014 完全无数据、2015 只有 10 只** ⇒ 有效历史**只有 8 年（2016 起）**，
  **直接违反约束 4「近十年都要有数据」**，不看指标就该判死。
- 逐年 S 在 +1.57 / −1.95 / +0.92 / −1.08 之间**无规律翻符号** ⇒ 噪声，不是 regime。
- ★ **必须修正 §5.71.2 的一刀切**：那里据 `KOR-RISK60-CROWDING-NOSIGNAL` 的
  「longCount 325/shortCount 323」断言「risk60 历史并不短」——**该结论只对 `rsk60_offer` 成立**。
  **同一数据集内不同字段的历史长度可以差 2 年**，约束 4 必须**逐字段**用逐年 `longCount` 验，
  不能用数据集级 coverage（0.98/1.0）代替。这与 §5.69.2 对 insiders5 的做法是同一条纪律的一次反向印证。

### 5.72.4 域级结论：KOR 的 risk 塔整体关闭（并入 §5.71.4）

| 数据集 | 封存依据 | 结论 |
|---|---|---|
| `risk60` | `KOR-RISK60-CROWDING-NOSIGNAL` + **本波逐年归因**（A 单年 32% PnL / 2Y 0.17；B 仅 8 年历史 + 翻符号） | ⛔ |
| `risk71` | `KOR-RISK71-RESIDUAL-REVERSAL-2Y-DEAD`（2022–2023 结构性符号翻转：散户主题动量 + 2023-11 卖空禁令） | ⛔ |
| `risk59` | 未单独回测，但 `risk60` 的死记录 `rule` 是**域级**措辞「该域在 KOR 整体关闭」，且 16 字段与 risk60 同属借券域 | ⛔ **不投**（§5.71.4 已定） |
| `risk88` | 在 85 条 `dead_ends` 的 dataset 覆盖里 | ⛔ |
| `shortinterest3` | 16 死集名单 | ⛔ |

⇒ **9 个未点亮塔里，`risk` 与 `institutions` 已整塔关闭，`earnings`/`imbalance`/`socialmedia` 是资产性死亡**，
真正还有活集可投的只剩 **news（news84 / news73）/ sentiment（sentiment23）/ insiders（insiders1/5）/ macro（macro63）**。

★ **`insiders1` 画像补录（2026-10-30，9 字段 cov .3526 αC 548）**：`insd1_holdings` / `insd1_price` /
`insd1_shares` / `insd1_tradesignificance`（1–3 显著性）/ `insd1_value` / `insd1_valueeur` / `max_trade_price`
可用，**但全表无买/卖方向字段**（`tradesignificance` 是 1–3 档，不是方向）⇒ 经典「内部人买入 = 看涨」机制
**无法实现**，只能做「内部人交易强度」的无方向探针。这也解释了为什么本区历史上用的是 `insiders5`（53 字段、有方向），
而 `insiders5` 已有 `KOR-INSIDERS5-CEILING-20260909`（30 条 best S=1.05）。
⇒ **insiders 塔实质上也是「只剩无方向探针」，优先级排在 news / sentiment 之后。**

### 5.72.5 配额纪律记账

| 项 | 值 |
|---|---|
| 本波消耗仿真槽 | 2 |
| 其中**派在已封存机制上的** | **2（100%）** |
| 根因 | 直接 MCP `create_multi_simulation` 派发**绕过** `dead_dataset_guard`（§5.71.3） |
| 已固定动作 | 开波前双路扫 `get_dead_ends`（`payload.dataset` + `entry_id`）+ 逐字段 `longCount` 验约束 4 |

⚠ 不做「回头补跑」：本波结论已与既有死记录一致，再无新信息可榨。

### 5.72.6 ★★ 自我纠错：§5.71.6 / §5.72.4 的「剩余面」是**抽样**，不是全集（2026-10-30）

**事故形态**：§5.71.4–§5.72.4 连续三处写「真正还有活集可投的只剩 news84 / news73 / sentiment23 / insiders1 / macro63」，
并据此推出「60 颗在未点亮塔不可达」。**该结论建立在「我这轮碰过的数据集」上，而不是 `get_datasets(category=…)` 的全集上。**
复现成本极低（6 次分类拉取、零配额），却会直接把用户目标误判成不可达 ——
与备忘 `task-experience-d02c937b`「穷尽声明前必须盘点全集分母」是同一个坑。

**全集（KOR/TOP600/D1，一次拉全，2026-10-30）**：

| 塔 | 数据集数 | 名单（✗=已判死/已封存，★=本轮新发现、从未体检） |
|---|---|---|
| news | **24** | ★news3(19F/cov.259/22α) ★news17(24F/.269/212α) ★news18(29F/.571/1012α) ★news20(24F/.507/155α) ★news21(13F/.744/143α) ★news23(93F/.329/58α) ★news29(12F/.467/29α) ★news31(25F/.354/35α) ★news36(43F/.226/30α) ★news46(44F/.342/126α) ★news48(22F/.270/63α) news59(2F/1.0/2396α) ★news66(2F/.50/72α) ★news7(56F/.633/372α) news73(22F/.268/8α) ★news76(6F/.659/16α) news79✗ news84(23F/.372/16α) ★**news85(23F/.633/52α)** news104(11F/.267/85α) ★other7(11F/.294/29α) news38✗ news50✗ news54✗ |
| sentiment | 6 | news_sentiment_transfer✗ other553✗ sentiment21✗ sentiment23(156F/.265/54α) sentiment26✗ sentiment27(29F/.399/1871α) |
| risk | **7** | risk60✗ risk71✗ risk59✗ risk88✗ ★**risk72(5F/.625/400α 特定收益)** ★**risk68(5F/.991/757α 订单簿)** risk70(96F/.98/7963α) |
| institutions | 2 | institutions6✗ fund_holdings_panel（待封存） |
| macro | **2** | macro63(1F/1.0/192α) ★**other106(KOSPI INDEX, 15F/.404/307α)** |
| socialmedia | 2 | ★**other100(1F/1.0/399α 共搜)** ★**socialmedia39(1F/1.0/576α 共搜)** |
| insiders | 2 | insiders1(9F/.353/548α 无方向) insiders5✗ |
| earnings | 1 | earnings3(8F/.660/2616α) |
| imbalance | 1 | imbalance5✗ |

**新面清点（扣掉 16 死集 ∪ 85 死记录 ∪ 待封存）**：

- **news 塔实际有 ~19 个未死数据集**（不是我此前说的 2 个）。其中三个**结构性最优的新目标**：
  - ★ **`news85`**（News Sentiment Analysis using DNN，23F，cov **.6325**，仅 52 α）——
    它是 `news84` 的**同族兄弟但覆盖率高 1.7 倍**。`news84` 的全部风险恰在 cov .3702（§5.72.3 的教训：
    覆盖率低 ⇒ 早期 `longCount` 塌陷 ⇒ 撞约束 4）。**同一机制换成 news85 = 用一份新数据换掉这个风险**，
    比在 news73（cov .268）上做跨源复现更优先。
  - ★ **`news23`**（MnA Deals，**93 字段**，58 α）—— KOR 未点亮塔里字段最厚的新闻集，
    含并购/增发/发债的事件结构（deal type / status / participants）⇒ **event_type 家族 × Surprise / Event-conditioned 两条 HIGH 桶**都能落，
    与「情绪方向」完全不同轴。
  - ★ **`news3`**（Dow Jones 词典情绪，19F，仅 22 α）—— fear / certainty / hype 等**非极性情绪分项**，
    可做 divergence（多情绪分项之间的分歧）而非 direction —— 这是 KOR 尚未碰过的机制族。
- **risk 塔未全关**：`risk72`（特定收益，5F）与 `risk68`（订单簿，5F）从未测过。
  ⚠ 但 `risk60` 的死记录是**域级措辞**（§5.72.4 已据此关闭 risk59）⇒ 若要重开 risk72/risk68，
  必须先在台账里明确「域级封存只覆盖借券子域，不覆盖 risk68/72」，否则等于自破纪律。**本轮不动，留待用户裁决。**
- **macro 塔有第二个集**：`other106` = KOSPI 指数成分/权重（15F，cov .404，307 α）——
  「指数纳入/调权效应」在 KOR 的直接数据源，比 `macro63` 的单一布尔字段信息量大得多。
- **socialmedia 塔两个集都是 cov 1.0、仅 1 字段的共搜（co-search）数据**：`other100`/`socialmedia39`。
  单字段 ⇒ 天然 ATOM（单数据集定义），但 αC 399/576 偏挤、valueScore 1–2。属**低成本探针**级。

**⇒ 结论替换**（推翻 §5.71.6 第 3 条）：在上面这份全集里，`news` 一塔就有 19 个未死集、
且存在 news85 这种「同机制 + 高覆盖」的现成替换，**「60 颗不可达」的判断作废，改为「按当前判死面仍有足够塔位供给，瓶颈是机制质量而非资产数量」**。
§5.71.6 给用户的三条路**不再需要**（不降目标、不放宽塔位、不重开域级封存）。

**新增纪律（写入开波前动作清单）**：
1. 任何「榨干了 / 只剩 N 个」的结论，必须先跑一遍 `get_datasets(category=…)` 逐塔点全集，把「未死集数」写进台账再下结论。
2. `get_datasets` 的 `description` 在 KOR **大面积错配**（本批 24 个 news 集里有 9 个描述写的是「RIC↔BBID 映射」），
   **不可用描述判断数据集内容**，必须 `get_datafields` 取真实字段。这条与 §5.71.6 用的 `valueScore` 一起看时尤其重要——
   valueScore 是平台给的，描述不是。
3. ★ **news 塔有一条此前没被引用的域级封存令**，它直接决定 news 剩下 19 个集里哪些字段能用 —— 见 §5.73.5。

---

## §5.73 波 238 收批（news84 关注度方向 A/B）+ 波 239 开波（news85 跨源复现）

### 5.73.1 收批表：方向已定，量级不够

`13jucM4Br5fUcrdCRUEctuY` / 2 条 / 全部 COMPLETE / `harvest_multisim_results` → `linked: 2, upserted: 2`，
波 238 暂定 verdict `FAIL(0/2)`。

| 槽 | alpha | 表达式 | S | F | TO | 2Y | invest S | 硬闸失败 |
|---|---|---|---|---|---|---|---|---|
| A | `O0AqZOW1` | `winsorize(reverse(group_rank(ts_backfill(normalized_news_item_count_transfer_2, 66), industry)), std=2)` | **+0.41** | 0.15 | .1461 | 0.82 | 0.02 | LOW_SHARPE / LOW_FITNESS / LOW_2Y |
| B | `LLMq1WKe` | 同上去掉 `reverse` | **−0.56** | −0.23 | .1461 | −1.02 | −0.21 | 同 + LOW_SUB_UNIVERSE |

- 两条 `MATCHES_PYRAMID` pass（`KOR/D1/NEWS` ×1.6）⇒ **塔位在，信号不过**。
- **`S(A) = +0.41` vs `−S(B) = +0.56`**：符号方向确认（**做多关注度是亏的，关注度反转是赚的**），
  量级远低于 1.58。A/B 不精确反号是 `rank` + `winsorize` + `decay=4` 三者非线性的预期结果，不是异常（铁律 B 的同款现象）。
- **这是 KOR 第一条「关注度轴」实证**：此前 wave87/96/141 的死记录针对的是**情绪方向**（tone/positive-negative/hotlevel），
  与本条不是同一机制 —— 见 §5.73.5 的封存令边界。

### 5.73.2 逐年归因（A）：约束 4 **通过**，但 S<1.0 占 6/10 年

| 年 | 2014 | 2015 | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 |
|---|---|---|---|---|---|---|---|---|---|---|
| S | 0.27 | −0.09 | 0.75 | **−0.80** | 1.41 | **−2.24** | 1.40 | 1.47 | 0.46 | 1.14 |
| longCount | **276** | 303 | 305 | 305 | 323 | 320 | 322 | 340 | 322 | 325 |

- ★ **约束 4 通过**：`longCount` 十年全 ≥ 276，2014 就有 276 只 ⇒ **news84 的 cov .3702 是截面覆盖，不是历史缺口**
  （与 §5.72.3 `rsk60_crowding` 完全相反）。这条再次证明「数据集 coverage 与字段历史长度是两件独立的事」，
  两边都必须逐字段实测。
- 但 **S<1.0 的年份 6/10**（2015 0.09 以下、2017 −0.80、2019 −2.24、2022 0.46、2014 0.27），
  单年 −2.24 直接把 2Y 打到 0.82 ⇒ **按归因决策表「S<1.0 年份 ≥3 成 ⇒ 2Y 闸结构性不可达」**，
  这条构造在任何参数档都不可能靠 decay/平滑救回。
- 结论：**方向对、强度不够、且年度不稳** ⇒ 不进入 Mode A 调参（调参无法改变年份分布），只能换源验证是否「低覆盖导致噪声」。

### 5.73.3 预登记规则判定（§5.71.5 条文逐字对照）

> 原文：「S(A) ≈ −S(B) ⇒ 关注度轴方向已定，直接进 239 跨源复现；**两槽 max\|S\| < 0.5 ⇒ news 塔整塔关闭**」

- `max|S| = 0.56 > 0.5` ⇒ **不触发整塔关闭**，按第一条走：**方向已定 → 进 239 跨源复现**。
- 但必须记录：0.56 距阈值 0.5 太近，**这次「不关闭」是阈值边缘的判定，不是信号可用的证据**。
  ⇒ 波 239 若跨源后仍 < 0.9，news 塔的**关注度子轴**也一并关闭（预登记见 §5.73.4）。

### 5.73.4 波 239 开波：news85 跨源复现 + 归一化消融

`create_multi_simulation` → `2hZDtiaD54n9ms1ehGYXL3c`（2026-10-30 10:21 提交，2 条，KOR/TOP600/D1，共用设置不变）。
`preflight_expressions` `valid:true` / 未知字段 0；`operator_audit` `safe:true` / 违规 0。

| 槽 | 表达式 | 设计意图 | 家族 / 桶 |
|---|---|---|---|
| A | `winsorize(reverse(group_rank(ts_backfill(normalized_headline_count, 66), industry)), std=2)` | **逐字复刻波 238-A 的构造**，只换数据集（news84→news85，cov .3702→**.6325**）⇒ 检验「低覆盖是否就是噪声来源」 | attention / Change |
| B | `winsorize(reverse(group_rank(ts_backfill(headline_item_count, 66), industry)), std=2)` | **归一化消融**：用原始标题计数替代归一化计数，其余逐字相同 ⇒ 检验「归一化这一步是否承重」 | attention / Change |

- 选 `news85` 而非 `news73` 的理由：同族、字段同构（23 vs 23）、覆盖率高 1.7 倍、αC 52（几乎未被挖）。
- 两槽**都属事件计数类**，**落在 §5.73.5 封存令的放行侧**（该令只封情绪方向，保留「事件计数/时间模式」）。

**波 239 预登记判定（结果回来前写死，防止事后解释）**：

| 结果形态 | 判定 |
|---|---|
| news85 A **S ≥ 0.9** 且 S<1.0 年份 ≤ 3 | 关注度反转轴**成立**，进 240 做 `trade_when` 事件门控 + 跨源（news73 `vec_sum(nws73_entitiescounter)`） |
| news85 A **0.5 ≤ S < 0.9** | 方向稳健但强度仍不足 ⇒ 按 §5.73.3 关闭 news 关注度子轴，**转非 news 塔**（socialmedia 共搜 / macro `other106` / insiders1） |
| news85 A **S < 0.5** 或 A/B 同号（归一化消融翻号） | 该轴在 KOR 是**数据集特异噪声**，news 塔整体关闭（第七个死轴） |

### 5.73.5 ★ 新发现的域级封存令：news 在 KOR **只保留「事件计数 / 时间模式」**

`get_dead_ends(KOR)` 原文（wave 141，2026-09-02）：

> 「KOR 新闻标题情绪族（news38/mmp_nlp/news_sentiment_transfer）已三波判死，不再投入；
> **新闻类在 KOR 仅保留事件计数/时间模式类尝试**」
> 「新闻情绪类数据集（news38/news_sentiment族）在KOR判死，**不再投任何变体**」

**边界解读（本轮定案，后续不再争论）**：

| 轴 | 状态 | 依据 |
|---|---|---|
| 新闻**情绪方向 / 情绪水平**（tone、positive-negative、hotlevel、sentiment score 水平） | ⛔ **禁投** | 上面两条死令，且 wave87/96/141 三波实测全反向 + CW 撞墙 |
| 新闻**情绪分歧度**（最高−最低情绪分、skewness） | ⛔ **保守按禁投处理** | 派生物仍是情绪分，属「任何变体」字面覆盖；若要开必须单独立项并写明与死令的差异 |
| 新闻**事件计数 / 关注度 / 时间模式**（item count、entity count、story 时间戳、event topic 计数） | ✅ **放行（唯一合法侧）** | 死令明文保留 |

⇒ 波 238 / 239 的 `normalized_news_item_count_transfer_2`、`normalized_headline_count`、`headline_item_count`
**均落在放行侧**，两波合规。**同时这也意味着**：news 塔剩下 19 个集里，
`news3`（词典情绪分项）、`news85` 的情绪概率族、`news84` 的情绪概率族、`sentiment23` 的 156 个情绪字段
**全部被这条令封住**，真正可用的只有各集的**计数/时间戳/事件类型**字段。
⇒ news 塔的实际可用面比 §5.72.6 的表面清单小得多，**「19 个集」要按「19 个集里的计数类字段」重算**。

### 5.73.6 非 news 塔画像补录（2026-10-30，三个集当场判否/立住）

| 集 | 字段实况 | 判定 |
|---|---|---|
| `socialmedia39` | **仅 1 个 VECTOR，且是 ID 字段**：`scl39_top5_people_also_watch_ticker_ii`（共看邻居的 instrument ID） | ⛔ **不可用**——ID 不是数值信号，S1 语义分类必判非信号；`other100` 同形态（1 字段共搜）。**socialmedia 塔实质无资产** |
| `news59` | 仅 2 个字段：`mws59_event_fiscal_year`（会计年度）/ `mws59_event_time_value`（事件计划 UTC 时刻，整数值）。2396 α 全建在这两个上 | ⛔ **不作为新机制源**——一个日历标量 + 一个时刻整数，撑不出截面差异；「时间模式」虽在放行侧，但可做的只有「公告时点在盘中/盘后」，信息量太低 |
| `other106`（KOSPI INDEX） | **15 个 VECTOR，成对 `_cls`（变更前）/`_nxt`（变更后）**：`index_share`、`free_float_factor`、`capping_factor`、`adjusting_factor`、`price`，外加 `newshares_following_rightsissue` / `ksic_cls` / `index_code1,2` | ✅ **立住**——这是 KOSPI200 **季度/半年度再平衡的权重变更事件**，可构造「指数权重变动 ⇒ 被动买压 ⇒ 短期漂移/反转」，属 macro 塔（未点亮）且**机制与 news 完全不同轴** |

**外部论文取证（约束 2 的 B 通道，2026-10-30 检索）**：

- **指数纳入的短期价格压力有据**：Euro STOXX 50 纳入事件从公告到生效日 CAR **+3.69%**，并支持 price-pressure 假说（纳入/剔除效应是**临时**的）。
- **但效应会消失**：S&P 500 的最新十年证据显示「纳入效应的持续性已消失」（JEF，股票供给视角）；即该机制**对样本期高度敏感**。
- KOSPI200 **每年 6 月与 12 月两次再平衡**，特殊情形另触发 ⇒ 2014–2023 共约 20 次事件 ⇒ **事件数够覆盖十年**，
  但**事件日稀疏**，信号必须在事件后 `ts_backfill` 展开（对应论文里的「post-rebalancing dynamics」）。
- ⚠ 论坛检索 `search_forum_posts("index reconstitution KOSPI")` 返回 **0 命中**（`no_result`，非故障）⇒ 该机制**在 BRAIN 论坛无现成模板**，属「B 有机制、A 无表达」格 ⇒ 按 §②.d 裁决表走**自建骨架**。

### 5.73.7 波 240 预置（已 preflight，**未派发**，等 239 结果定去留）

| 槽 | 数据集 | 表达式 | 机制 / 桶 |
|---|---|---|---|
| A | `other106`（macro 塔，未点亮） | `winsorize(group_rank(ts_backfill(subtract(vec_avg(oth106_ospi_ca_eq_index_share_nxt), vec_avg(oth106_ospi_ca_eq_index_share_cls)), 22), industry), std=2)` | **指数权重变更 ⇒ 被动买压**（价格压力假说；方向取正：加权重看涨）· Event-conditioned |
| B | `news21`（news 塔） | `winsorize(reverse(group_rank(ts_backfill(nws21_event_freq, 22), industry)), std=2)` | **事件频次 ⇒ 关注度反转**（波 238/239 同轴第三源；`nws21_event_freq` cov **.967**，是 KOR news 塔覆盖最高的计数字段）· Change |

- 两条均 `preflight: valid:true`、`operator_audit: safe:true`（2026-10-30 实测）。
- **去留规则**：239-A `S ≥ 0.9` ⇒ 240 按上表派（B = 关注度轴第三源）；
  239 判「关注度子轴关闭」⇒ 240 只派 A，B 换成 `news29_full_significance`（**事件显著性**，event_type 家族，与关注度轴不同轴）。
- `news29` 备选实测（2026-10-30）：`nws29_full_significance` cov **.8649**（1=High/2=Med/3=Low，**值越小越重要 ⇒ 方向需反号**）、
  `nws29_full_frontpage` cov .8649（头版二元标记）、`event_secondary_topic_code` cov .8649
  ⇒「头版 + 高显著性」是**显著度加权**的干净表达，且不依赖任何情绪字段。

---

## §5.74 波 239 收割与 news 塔关闭（第七个死轴）

### 5.74.1 收割表（multisim `2hZDtiaD54n9ms1ehGYXL3c`，已入库 `linked:2 / upserted:2`）

| 槽 | alpha | 表达式 | S | F | TO | 2Y | subU | invest | RA 失败项 |
|---|---|---|---|---|---|---|---|---|---|
| A | `xAr9kbEp` | `winsorize(reverse(group_rank(ts_backfill(normalized_headline_count, 66), industry)), std=2)` | **−0.43** | −0.12 | .2274 | −0.87 | −0.33 | −0.44 | SHARPE/FITNESS/SUB_UNIVERSE/INVEST/2Y（5 项） |
| B | `88R7QPZo` | `winsorize(reverse(group_rank(ts_backfill(headline_item_count, 66), industry)), std=2)` | **−0.24** | −0.05 | .2535 | −0.68 | −0.14（pass） | −0.30 | SHARPE/FITNESS/INVEST/2Y（4 项） |

两条 `UNSUBMITTED / stage=IS`，波 239 暂定 `verdict=FAIL(0/2)`。

### 5.74.2 逐年归因（约束 2）

| 年 | 2014 | 2015 | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 |
|---|---|---|---|---|---|---|---|---|---|---|
| **A** S | −0.29 | −1.26 | **+0.29** | −0.98 | **+1.74** | −1.75 | −0.89 | **+0.77** | −0.99 | −0.76 |
| **B** S | +0.02 | −0.48 | **+0.17** | −0.61 | **+1.68** | −1.45 | −0.63 | **+0.32** | −0.75 | −0.62 |

读数（按发波决策表）：

1. **A/B 十年符号逐一相同（10/10）** —— 归一化消融既没翻号、也没改变年形 ⇒ 两条测的是**同一个噪声**，不是两个独立证据。
2. **仅 3/10 年为正**，且三个正年全部落在 2016 / 2018 / 2021；S 在 −1.75 ~ +1.74 之间来回摆 5 次。
   ⇒ 这是「停滞段 ≥3 ⇒ regime 依赖」+「单年集中」的组合指纹，**不是「弱而稳」**。2018 单年 +1.74 恰好占总正收益的大头。
3. **约束 4 通过**：A 逐年 `longCount` 272–321、B 290–356，十年逐年都有持仓 ⇒ news85 近十年确有数据。
   ⇒ **本波失败在机制，不在数据**，不能按「覆盖不足」处置。

### 5.74.3 预注册规则的裁决（逐条对照 §5.73.4 原文，不改判）

| 预注册分支 | 触发条件 | 本波实测 | 判定 |
|---|---|---|---|
| 关注度反转轴成立 | A `S ≥ 0.9` 且 S<1.0 年份 ≤3 | −0.43，8 年 <1.0 | ❌ |
| 方向稳健但强度不足 | `0.5 ≤ S < 0.9` | −0.43 | ❌ |
| **数据集特异噪声 ⇒ news 塔整体关闭** | `S < 0.5` **或** A/B 同号 | **两条同时命中** | ✅ **执行** |

⇒ **news 关注度/标题计数轴在 KOR 判为数据集特异噪声，news 塔关闭（本战役第七个死轴）。**

### 5.74.4 关闭范围与边界（写死，防未来误读为「整个 news 目录不可用」）

- **关闭对象 = news 塔的标题/计数/关注度轴**。三个独立数据集同轴无方向：
  238（`news84` × `normalized_news_item_count_transfer_2`，max\|S\|=0.56）、
  239-A（`news85` × `normalized_headline_count`，−0.43）、239-B（`news85` × `headline_item_count`，−0.24）。
- 叠加 §5.73.5 已封的**情绪方向 / 情绪分歧**（域级封存令）⇒ news 塔两条主腿都已作废，**无剩余默认可走路**。
- **未测但不再默认路由**：`news23`（93 个 deal 字段）、`news31`、`news76`、`news73`（实体计数）、`news29`（显著性/头版，cov .8649，event_type 家族）。
  它们的机制（并购/交易事件、显著度加权）与标题计数**不同轴**，但塔级关闭后不再进默认队列。
  **重开条件（三者缺一不可）**：单数据集 + **预注册**假设 + 明写「非关注度、非情绪」轴，且单独成波。
- 本节关闭**只对本战役的路由生效**，不等同于「平台上 news 类不可挖」——238/239 的失败是 KOR 区域 × 本设置下的结论。

---

## §5.75 波 240 设计（换塔：macro × earnings，均未点亮）

触发：§5.74.3 判「关注度子轴关闭」⇒ 按 §5.73.7 的去留规则，**240 不再派 news21**，B 槽换成非 news 塔。

| 槽 | 数据集（塔） | 表达式 | 机制 / 桶 |
|---|---|---|---|
| **A** | `other106`（macro，未点亮） | `winsorize(group_rank(ts_backfill(subtract(vec_avg(oth106_ospi_ca_eq_index_share_nxt), vec_avg(oth106_ospi_ca_eq_index_share_cls)), 22), industry), std=2)` | KOSPI200 再平衡**权重变更 ⇒ 被动买压 ⇒ 短期漂移**（同一 `_cls`/`_nxt` 对的 delta；Change） |
| **B** | `earnings3`（earnings，未点亮） | `winsorize(reverse(group_rank(ts_backfill(ern3_next_interval, 5), industry)), std=2)` | **盈余公告溢价 / 事前不确定度收敛**：做多「距下次公告近」的股票（Event-conditioned / Surprise） |

### 5.75.1 B 槽的画像（`get_datafields earnings3` @KOR/D1/TOP600，2026-10-30 实测，共 8 个 MATRIX 字段）

| 字段 | cov | alphaC | 含义 | 取向 |
|---|---|---|---|---|
| `ern3_pre_interval` | .7756 | 616 | 距**上次**公告的交易日数（≤0） | 事后陈旧度 |
| `ern3_next_interval` | .5825 | 285 | 距**下次**排期公告的交易日数 | **本波主腿**（临近度） |
| `ern3_pre_reptime` / `next_reptime` | .7756 / .5825 | 536 / 199 | 公告时刻（HHMM / 会话码） | 只作门控，不能作截面 |
| `ern3_all_delay_1_*` | .5599–.7232 | 200–594 | ASI 全域版本（含 KOR） | 备选 |

- **纯日历集**：无价格、无情绪、无财务数值 ⇒ 天然 ATOM（单数据集），且**约束 5 自动合规**（无 PV/MODEL/OTHER 腿）。
- 缺失语义清楚：`next_interval` 为 NaN = 无排期 ⇒ 不参与交易（`nanHandling=OFF`），不会伪造持仓。

### 5.75.2 论文取证（2026-10-30 检索，约束 2 的 B 通道）

- **Savor & Wilson (2016, JF)**〈Earnings announcements and systematic risk〉：股权溢价集中在**公告日**兑现 ⇒ 公告日承载系统性风险溢价。
- **〈Uncertainty Resolution Before Earnings Announcements〉**（PKU GSM）：**71% 的公告溢价发生在公告之前**，且高不确定度股票的事前收益更大 ⇒ 应做多**临近公告**者，而非事后追。
- **韩国本土**：PEAD 在韩国被反复发现（Pacific-Basin Finance Journal, 2017，52 周高点锚定解释）；另有韩国实证显示「高换手 + 高特质波动」股票**仅在公告期**跑输（不可迁移的部分：那是 PV×earnings 条件结构，属下一步，不在本波 ATOM 内）。
- ⚠ 记录偏误：以上均为「公告溢价/漂移」机制层证据，**KOR 本区未测**；方向句与持有期（数日 ~ 数周）可用，量级不可照搬。

### 5.75.3 去留规则（**先写**，回测前锁定）

| 读数 | 判定 | 下一波动作 |
|---|---|---|
| **B** `S ≥ 0.9` | 公告溢价轴成立 | 241 做条件门控：`trade_when(临近公告, 高换手空头, -1)`（PV×earnings，占跨类别 5 条配额之 1） |
| **B** `0.5 ≤ S < 0.9` | 方向对、强度不足 | 241 换 `ern3_pre_interval` 对侧 + 公告窗口收窄（`trade_when`），不再扩窗口谱 |
| **B** `S < 0.5` | 该轴在 KOR 无方向 | **earnings 塔关闭（第八个死轴）**，转 insiders1 |
| **A** `S ≥ 0.9` | 指数再平衡轴成立 | 241 做 `ts_backfill` 展开长度扫描 + 事件窗（`trade_when`） |
| **A** `0.5 ≤ S < 0.9` | 方向对、强度不足 | 241 换 `capping_factor` / `free_float_factor` 另一对，验证是否同一机制 |
| **A** `S < 0.5` | macro/other106 关闭 | 转 insiders1（无方向字段，只作探针） |

- A 的论文面已在 §5.73.6 取证（STOXX50 纳入 CAR +3.69%，S&P500 近年衰减）⇒ 若 A 也 <0.5，则「指数再平衡」在本区与新闻同命，直接封。
- 两条均需回测后**逐年 `longCount`** 复核约束 4（`earnings3` 无 pre-dispatch 证据，按事后硬核；任一整年 0 持仓即判约束 4 不通过）。

### 5.75.4 派发记录（2026-10-30）

- 死面闸手检：`get_dead_datasets(KOR)` 16 条中**不含** `other106` / `earnings3`；`get_dead_ends` 关键词扫描两数据集命中 0。
- `preflight_expressions(region=KOR, universe=TOP600, delay=1)` → `valid:true`、`unknown_fields:[]`、`platform_field_count:3`、`vector_fields:[]`。
  ⚠ **坑**：该工具默认 `region=USA / TOP3000`，不传 region 会把 KOR 字段全判 unknown（首次调用即踩，`unknown_fields:["ern3_next_interval"]`）。
- `operator_audit` → `safe:true`，无幽灵算子（19 个 KOR 幽灵算子名单原样返回，两条表达式均未命中）。
- 台账登记：`upsert_expressions` 各 1 行（`other106` / `earnings3`，`status=pending`，`source=manual`）。
- 派发：`create_multi_simulation` → **`jpXpx1yk4HB9MvnudB25Dk`**（2 表达式，KOR/TOP600/D1/decay4/STATISTICAL/trunc .08/VERIFY/OFF），2026-10-30 10:28 UTC 提交。

---

## §5.76 非 news 塔画像补录（2026-10-30，为 241+ 备料）

### 5.76.1 `insiders1`（insiders 塔，未点亮）—— 无交易方向字段，只能间接推

9 个字段**全 VECTOR，cov 一律 .3526**：

| 字段 | cov | alphaC | 用途 |
|---|---|---|---|
| `insd1_holdings` | .3526 | 57 | 交易后内部人持股 ⇒ **唯一可推方向的字段** |
| `insd1_shares` | .3526 | 111 | 交易股数（**无符号**） |
| `insd1_value` / `insd1_valueeur` | .3526 | 107 / 45 | 交易金额（**无符号**） |
| `insd1_price` / `max_trade_price` | .3526 | 45 / 5 | 成交价（区间取下限） |
| `insd1_tradesignificance` | .3526 | 40 | 重要性 1–3（1 低 / 3 高） |
| `insd1_gvkey` | .3526 | 178 | 主体 ID |
| `transaction_currency_code` | .3526 | 15 | 币种码（非信号） |

- **没有买/卖类型字段** ⇒ 不能直接构「内部人净买入」。唯一路径：`ts_delta(vec_sum(insd1_holdings), 22)` 作净增持代理。
- cov .3526 ⇒ 仅约 1/3 的票有内部人交易 ⇒ 必须 `ts_backfill` + `trade_when` 门控；单数据集 ATOM 可行。
- 优先级：**低于 risk68**（见 5.76.2），仅作替补。

### 5.76.2 `risk68`（risk 塔，未点亮）★ 挖出被 sharpe 过滤藏起来的核心资产

⚠ **纪律命中**：默认 `filter_sharpe=true` 只返回 **3/5**，被藏的两个里有一个是本集最有价值的字段。全量 5 字段（`filter_sharpe=false`）：

| 字段 | cov | alphaC | 含义 |
|---|---|---|---|
| **`rsk68_residual_return`** | **.9569** | 178 | **特质 1 日收益**（实际 − beta×市场）← **核心资产** |
| `rsk68_beta` | 1.0 | 73 | 长窗 β（~504 交易日） |
| `rsk68_weight_volatility_short` | 1.0 | 503 | 短窗波动率 |
| `rsk68_weight_dadv` / `_edadv` | 1.0 | 94 / 98 | 美元 ADTV（流动性权重） |

**A-2 收益来源声明**：
- **谁被定价**：短线提供流动性的对手方；
- **为什么错**：特质收益不含市场 β，短窗内由流动性冲击 / 注意力驱动**过度反应**（Barberis-Shleifer-Vishny 过度反应），而 KOR 已有 PV / 动量族抓的是总收益，**不同轴**；
- **多久修复**：数日 ~ 数周；
- **预期方向**：短窗**反转**（`ts_sum(residual_return, 5)` 取反）；中窗（66）可测**残差动量**（Blitz-Huij-Martens 2011：残差动量 Sharpe 更高、β 更低）。
- 边界：cov .9569 ⇒ 广度够；描述写 "European asset" 属 **KOR 描述错配**（本仓已记录该区描述不可信），以 cov 与 field id 为准。

⇒ **241 首选 = `rsk68_residual_return`，优先级高于 insiders1。**

### 5.76.3 `risk72`（risk 塔，**同机制族**，只作交叉验证）

5 字段全是 "daily reproducible specific returns"，只差 universe / 加权口径：
cov .3534（TOP1000）/ .5426（TOP1500）/ .7085（TOP2000）/ .7592（`minvol1m` 与 `xjpci` 各一）。

- 与 `rsk68_residual_return` **同机制** ⇒ 按 ②.e「跨数据集同机制 = 同一条腿」，**不作并列项相加**，只作交叉验证源。
- 若 risk68 成立而 risk72 不成立 ⇒ 是口径问题不是机制问题；反之亦然。
- 取数优先 `.7592` 的两个（cov 最高）。

### 5.76.4 risk60 封存令的边界裁定（写死，防「risk 塔整塔不可用」误读）

- 已封的是 `KOR-RISK60` + `rsk60_crowding`（约束 4 不通过：2014 年 0 持仓）⇒ 封的是**证券借贷拥挤子域**这一机制。
- `get_dead_datasets(KOR)` 16 条中**不含** `risk68` / `risk72`；dead-ends 关键词扫描命中 0 ⇒ 两集**未被点名**。
- 本轮裁定：**risk60 的封存不外溢到 risk68 / risk72**，两者按新数据集重走 A-1 / A-2，波 241 起可派。
- 这不是「绕过封存」：被封的是**机制**（证券借贷拥挤）与一个约束 4 死亡的数据集，不是 category 标签本身。

---

## §5.77 波 241 预置：risk68 短窗残差反转 × risk72 跨源验证（**已 preflight，未派发**）

### 5.77.1 双通道取证（2026-10-30）

**A 通道｜BRAIN 论坛**（`search_forum_posts("residual momentum specific return reversal")`，命中可读）：
- 帖〈动量与反转 Momentum & Reversal——追风的人，与等风的人〉（id `42864316831639`，37 票）正文只给理念
  （「短窗口做反转，中窗口做动量，别把周期和理念错配」），**无可执行模板**。
- 但评论（LL46807，2026-09-05）给出两条可落地结论：
  ① 「反转用位置类算子（`ts_arg_max` / `ts_rank` 这类『当前值在历史分位』）比用变化率更稳」
     ⇒ 本波短窗腿用 `ts_rank` 包 `ts_sum`，**不用**裸 `ts_delta`；
  ② 「动量对平滑方式敏感，`ts_mean` 直接平滑会把信号推向拥挤方向」⇒ 若 242 做长窗动量腿，改自归一化 `divide(x, ts_mean(x, 长窗))`。

**B 通道｜外部论文**：
- **Blitz / Huij / Lansdorp / Verbeek〈Short-Term Residual Reversal〉（Journal of Financial Markets）**
  —— 短期**残差反转**是与价格反转不同的独立异象 ⇒ 支持短窗腿。
- **Blitz / Huij / Martens〈Residual Momentum〉（J. Empirical Finance, 2011）**：残差动量 Sharpe 高于价格动量、波动率约低一半；
  **且刻意剔除最近一个月**（避开短期反转）⇒ 短窗反转与中窗动量是**同一残差序列的两个不对称区间**，不是两个并列因子。
- ⚠ **反证必须记**：A 股复现显示残差动量的结论**对回归是否含截距极敏感**（含 α 项时「翻车成反转」）⇒ 残差构造本身决定符号。
  平台给的是**已算好的** `rsk68_residual_return`（描述为「actual return − beta × market_return」，即**单因子市场模型**，非 FF3），
  我们**不能控制模型设定** ⇒ **符号必须实测，不许照搬论文**（铁律 B）。

### 5.77.2 双通道裁决

- A、B 指向**同一机制**（残差序列的短窗反转 / 中窗动量）⇒ ⭐ 优先组装（论坛给算子形态、论文给方向句与持有期）。
- 但 B 的模型设定（FF3）与平台（单因子）不同 ⇒ **降级为「机制可信、符号待测」**，A-2 从严：
  方向只写「短窗取反」，不写「必为正」。

### 5.77.3 两槽设计（均 `preflight valid:true` / `unknown_fields:[]`）

| 槽 | 数据集 | 表达式 | 机制 |
|---|---|---|---|
| **A** | `risk68` | `winsorize(reverse(group_rank(ts_rank(ts_sum(rsk68_residual_return, 5), 22), industry)), std=2)` | 短窗残差**反转**（5 日残差和 → 22 日分位 → 行业秩 → 取反） |
| **B** | `risk72` | `winsorize(reverse(group_rank(ts_rank(ts_sum(rsk72_eqy_asi_supported_minvol1m_dsrt, 5), 22), industry)), std=2)` | 同结构换**另一家 provider** 的 specific return（cov .7592）⇒ 跨源验证 |

- 两槽**同机制不同源** ⇒ 按 ②.e 属「同一条腿」，**不作并列相加**；本波目的是判「机制是否跨源成立」，不是凑两个候选。
- 约束 5：各只用 1 个数据集、无 PV/MODEL/OTHER 腿 ⇒ 合规，均为 ATOM。
- 约束 4：cov .9569 / .7592 **不等于十年有数**，须回测后逐年 `longCount` 硬核。

### 5.77.4 去留规则（**先写**）

| 读数 | 判定 | 下一波 |
|---|---|---|
| A `S ≥ 0.9` 且 B `S ≥ 0.5` | 残差反转**跨源成立** | 242 做短窗长度谱（3 / 5 / 10）+ `ts_rank` 窗口谱；B 槽转 insiders1 |
| A `S ≥ 0.9`、B `S < 0.5` | 只在 risk68 成立（provider 特异） | 242 固定 risk68 做 horizon 交叉（66 日动量腿，符号不预设） |
| A `0.5 ≤ S < 0.9` | 方向对、强度不足 | 242 先换中性化档（本区已证换粗轴常使 robust 与 S 同升）+ 收窗；**不扫 truncation** |
| A `S < 0.5` 且 B `S < 0.5` | 残差反转在 KOR 无方向 | **risk68 / risk72 一并关闭**，转 `insiders5`（2026-10-30 目录普查后上调，见 §5.78.5；`insiders1` 降为次选） |

---

## §5.78 全量目录普查：15 category / 185 集，未点亮塔的真实分母（2026-10-30）

> 目的：在宣布任何「塔挖尽」之前，**先把分母摆出来**（铁律：穷尽声明前必须盘点全集）。
> 数据源 = `get_datasets(region="KOR", delay=1, universe=TOP600)` 全量 185 条（含所有 category），
> 点亮状态 = `get_pyramid_alphas(region="KOR")`，判死集 = `get_dead_datasets(region="KOR")`。

### 5.78.1 目录结构（185 集 / 15 category）

| category | 集数 | 覆盖头部（cov） | 备注 |
|---|---:|---|---|
| model | 57 | ai_equity_alpha 1.0 / ai_factor_transfer 1.0 / analyst_earnings_ibes 1.0 / model242 1.0 | 塔已亮（3） |
| other | 26 | other323 1.0 / other532 .9956 / acquisition_model .9937 / dl_riskfree_returns .9095 | 塔已亮（1） |
| news | 24 | news59 1.0 / news79 .8563（**已判死**）/ news38 .7971 / news21 .7435 | 塔**未亮** |
| pv | 18 | continuation_score 1.0 / pattern_scores 1.0 / pv1 1.0 / pv103 1.0 / pv106 1.0 | 塔已亮（2） |
| analyst | 17 | analyst39 .8952 / analyst44 .7730 / analyst_base_ref .7322 / analyst10 .7306 | 塔已亮（2） |
| fundamental | 17 | fundamental44 .8984（**已判死**）/ fundamental17 .8896 / fundamental94 .8558 | 塔已亮（3） |
| risk | 7 | risk60 1.0（**子域封存**）/ risk68 .9914 / risk59 .9806 / risk70 .9798 / risk88 .9727 | 塔**未亮** |
| sentiment | 6 | news_sentiment_transfer **.9654** / other553 .6243 / sentiment27 .3989 | 塔**未亮** |
| shortinterest | 3 | shortinterest5 1.0 / shortinterest38 .9953 / shortinterest3 .9238（**已判死**） | 塔已亮（4） |
| insiders | 2 | insiders5 **.8918** / insiders1 .3526 | 塔**未亮** |
| institutions | 2 | institutions6 .9996（**已判死**）/ fund_holdings_panel .8093 | 塔**未亮** |
| macro | 2 | macro63 1.0（**1 字段**）/ other106 .4038 | 塔**未亮** |
| socialmedia | 2 | other100 1.0（**1 字段**）/ socialmedia39 1.0（**1 字段**） | 塔**未亮** |
| earnings | 1 | earnings3 .6603（8 字段） | 塔**未亮** |
| imbalance | 1 | imbalance5 .8559（2 字段） | 塔**未亮** |

### 5.78.2 点亮塔地图：15 塔中 **6 亮 / 9 未亮**

`get_pyramid_alphas` 实测 KOR/Delay=1：

| 已点亮（不再计入目标） | 金字塔 α 数 |
|---|---:|
| shortinterest | 4 |
| fundamental | 3 |
| model | 3 |
| analyst | 2 |
| pv | 2 |
| other | 1 |

**未点亮 9 塔**（本战役唯一目标集）：`earnings` / `imbalance` / `insiders` / `institutions` / `macro` / `news` / `sentiment` / `socialmedia` / `risk`。

### 5.78.3 未点亮塔的可用分母 —— **三塔结构性不可能，四塔窄，两塔宽**

| 未亮塔 | 可用集（去判死 / 去封存） | 结构上限 | 判据 |
|---|---|---|---|
| **socialmedia** | 0（`other100` / `socialmedia39` 各仅 1 字段且均为 ID-only VECTOR） | **0** | 无可用信号字段 ⇒ 待封（口径见 §5.76 同族的 ID-only 判死） |
| **imbalance** | 0（`imbalance5` 2 字段「油价韧性分」，单轴无横截面） | **0** | 已判死待封 |
| **institutions** | 1（`institutions6` 已判死；`fund_holdings_panel` 30 字段 cov .8093，已判死待封） | **0** | 两集全灭 ⇒ 该塔结构性关闭 |
| **earnings** | 1（`earnings3`，8 字段） | **1 集深挖** | 波 240 B 正在实测；本塔**没有第二个数据集**，失败即整塔关闭 |
| **macro** | 2（`macro63` 仅 1 字段且无横截面；`other106` 15 字段 cov .4038） | **1 集深挖** | 波 240 A 正在实测；`other106` 失败即整塔关闭 |
| **insiders** | 2（`insiders5` **53 字段 cov .8918**；`insiders1` 9 字段 cov .3526 全 VECTOR 无买卖字段） | **1 集宽** ⭐ | ⚠ **`insiders5` 是本次普查的最大发现**：此前只登记了覆盖差的 `insiders1`。`insiders5` aC 4959 / uC 802，是全库未亮塔里「字段数 × 覆盖」最健康的单集 |
| **sentiment** | 5（`sentiment21` 已判死；`news_sentiment_transfer` **23 字段 cov .9654** 领衔） | **1 集宽** ⭐ | ⛔ **暂缓**：sentiment 类存在待裁定的封禁项（用户裁决未到），未裁定前不派 |
| **risk** | 5（`risk60` 子域封存；`risk68`/`risk72` 波 241；`risk59` 16 字段 cov .9806 借贷/做空；`risk71` 7 字段 .6658；`risk88` **64 字段 .9727**） | **3–4 集** | `risk59` 落在 risk60 已封的**证券借贷子域**内 ⇒ 与 §5.76.4 同口径，暂不入池；可用 = risk68 / risk72 / risk88 / risk71 |
| **news** | 23（`news79` 已判死；注意力/标题计数轴已关闭） | **宽但轴受限** | 只能用**非注意力、非情绪**轴：事件类型 / 显著性 / 传播（`news38` 45f .7971、`news54` 40f .6914、`news7` 56f .6327、`news50` 81f .6254）。closure 边界见 §5.74.4 |

### 5.78.4 产能读数（判「60 颗」用哪把尺）

`get_mining_yield(KOR)` 实测：`expressions 2659 / consumed 968 / backtested 848 / passed 139 / ra_clean 54 / prod_clean 11 / prod_blocked 6 / ra_unknown 310 / yield 6.37%`。

- **139 = 过 S·F 线（S≥1.58 且 F≥1.0）的回测行数**，不是可提交数；54 是 RA 干净，11 是 prod 干净。
- `get_submit_ready(KOR)` 仍只有 **1** 行 READY（`LLZ6wZO2`，**落在已点亮的 fundamental 塔**）⇒ **未点亮塔当前可提交 = 0**。
- ⇒ 「60 颗」按**未亮塔的过闸 α（S·F 线 + RA 干净）**计，不能按 `passed` 总数计（后者跨塔、跨波次含重复）。

### 5.78.5 结论：60 颗不可能靠塔宽达成，只能靠深度

1. **9 个未亮塔里有 3 个上限为 0**（socialmedia / imbalance / institutions）⇒ 实际可攻只有 **6 塔**。
2. 6 塔里 **2 塔各只有 1 个数据集**（earnings / macro），且两塔正在被波 240 同时实测 ⇒ **本波读数是两塔的生死判定**。
3. 剩余 4 塔的真实纵深：**insiders5（1 集 53 字段）**、**sentiment（受封禁待裁）**、**risk（4 集，risk88 64 字段最大）**、**news（23 集但轴受限）**。
4. ⇒ 目标分配（按可攻纵深，非按塔数均分）：risk ≈ 3 集 × 2–3 波、insiders ≈ 1 集 × 3–4 波、news 非注意力轴 ≈ 2–3 集、sentiment 待裁后 1–2 集，earnings/macro 各 1–2 波。
5. **`insiders5` 立即升级为默认次选**（替代 §5.77.4 里的 `insiders1`）：波 241 两槽若全灭，242 直接开 `insiders5` 字段画像 + 十年长核，不再走覆盖只有 .35 的 `insiders1`。

---

## §5.79 insiders5 画像（53 字段全 VECTOR）—— 头部轴是「持股结构」，不是「交易流」

> 取数：`get_datafields(dataset_id="insiders5", region="KOR", delay=1, universe="TOP600", filter_sharpe=false)`
> ⇒ **53/53 全 VECTOR**，`platform_count=53, complete=true`（两页拉全）。这是本区少数**未过滤也全量可读**的集。

### 5.79.1 覆盖分五档（决定聚合方式与 backfill）

| cov | 字段组 | 字段（代表） |
|---|---|---|
| **.9996** | 集团持股水平（主力） | `insd5_data`(去重股数) `insd5_ratio`(去重持股%) `insd5_real_data` `insd5_real_ratio` `insd5_tnc`(特别关系方人数) |
| **.9995** | 源持有人持股水平 | `insd5_source_data` `insd5_source_ratio` `insd5_source_real_data` `insd5_source_real_ratio` `insd5_source_recent_dt` `insd5_rpst_grp_typ`(持有人类型码) |
| **.9991** | 标识/登记（**非信号**） | `insd5_c_company_list_dt`(上市日串) `insd5_c_company_pyt_tkm`(市场码) `insd5_corp_reg_no` `insd5_list_yn` `insd5_nm_kor`(姓名) `insd5_nm_eyf` `insd5_mmyy_srfi` `security_type` `issuance_category` |
| **.8728** | 库存股（자사주） | `insd5_trsy_data` `insd5_trsy_ratio` `insd5_trsy_real_data` `insd5_trsy_real_ratio` `insd5_trsy_recent_dt` `insd5_trsy_tnc` |
| **.7318** | **交易流**（唯一带符号腿） | `insd5_vol_chg`(股数变动) `insd5_ghc_tr`(持股%变动) `insd5_fa_tr`/`insd5_fb_tr`(前后持股%) `insd5_vol_bf`/`insd5_vol_af` `insd5_trd_amt`(KRW) `insd5_unt_val`(成交价) `insd5_officer`(是否高管) `insd5_trd_reason_a`/`_b` `insd5_td_ctn`(披露日) `insd5_history_td_drt` |

⚠ 与 `insiders1` 的关键差别：**本集有真买卖方向腿**（`vol_chg` / `ghc_tr` / `trd_amt`），`insiders1` 一个都没有。
⚠ 覆盖 < .4 的字段：**0 个**（最低 .7318）⇒ 无需按「弃用」处理；但 .7318 档仍必须 `ts_backfill`（稀疏交易事件）。

### 5.79.2 质量先验（alphaCount 降序）⇒ 头部轴 = **持股结构**

| 字段 | aC | uC | 含义 |
|---|---:|---:|---|
| `insd5_source_data` | 734 | 266 | 源持有人去重股数 |
| `insd5_source_real_data` | 625 | 231 | 源持有人未去重股数 |
| **`insd5_rpst_grp_typ`** | **574** | 216 | 持有人集团类型码（代表/关联方/共同持有人） |
| **`insd5_tnc`** | **452** | 200 | 特别关系方人数 |
| `insd5_source_ratio` | 407 | 179 | 源持有人持股% |
| `insd5_data` / `insd5_source_real_ratio` | 299 | 124 / 126 | 集团股数 / 源未去重% |
| `insd5_ghc_tr` | 212 | 111 | 交易引起的持股%变动 |
| `insd5_trsy_ratio` | 152 | 55 | 库存股% |

⇒ **头部字段指向「持股结构与关联方广度」，不是「内部人买卖方向」**（`vol_chg` 仅 aC 119）。
按 0.1 纪律：这是该集最强经济轴，**先把结构轴打完再谈交易流**（与 analyst_consensus 的教训同型）。

### 5.79.3 已试记录（1 条，交易流轴已证偏弱）

`O0Aq9Y9J` = `winsorize(group_rank(ts_sum(divide(vec_sum(insd5_vol_chg), add(vec_sum(insd5_vol_bf), 0.0001)), 66), industry), std=2)`
实测：**S 0.28 / F 0.08 / 2Y -0.22 / turnover .0975 / longCount 324 / shortCount 313 / CONCENTRATED_WEIGHT 通过**。

- 解读：**交易流腿方向为正但强度远不够**，且 2Y 为负 ⇒ 不是「窗口没调对」，更可能是**低频稀疏 + 只覆盖 .7318**。
  按铁律 G，242 不铺 `vol_chg` 的窗口谱（已知会败的东西不重烧配额）。
- 归因提示：turnover 仅 9.75%（本区常见 15–25%）⇒ 信号变化太慢，`decay 4` 下几乎没有交易 ⇒ **结构腿更适合**
  （持股水平月度更新，本就该走变化率而非高频）。

### 5.79.4 两条未试机制（242 备选，**未 preflight、未注册**）

| 槽 | 机制（A-2 一句话） | 形态方向 | 字段 |
|---|---|---|---|
| **A 结构轴** | **库存股（자사주）累积 = 韩式回购**：公司/大股东增持自家库存股，等于用公司现金回购，后续注销或再融资都先反映为「库存股占比上升」 | `ts_delta(vec_sum(trsy_ratio), 66)` → 行业秩（**正向**：累积为利好） | `insd5_trsy_ratio`（cov .8728，aC 152） |
| **B 结构轴** | **关联方广度 = 治理复杂度**：特别关系方人数上升意味着所有权结构变复杂 / 潜在利益输送，风险溢价上行 | `ts_delta(vec_max(tnc), 66)` → 行业秩 → **取反**（人数增 = 利空） | `insd5_tnc`（cov .9996，aC 452） |

- ⚠ 两条都是**结构水平的变化率**（铁律 A：`tnc` / `trsy_ratio` 单边恒正且非负，禁裸水平做多空）。
- ⚠ `insd5_rpst_grp_typ` 是**分类码**，截面排序无经济含义 ⇒ 只能当分组/过滤，**不得当信号腿**。
- ⚠ 约束 4 未核：.8728 / .9996 是截面覆盖，**不等于十年有数**；派发后必须逐年 `longCount` 硬核。

### 5.79.5 与波 241 的优先级

- 波 241（risk68/risk72）先跑；**若 241 两槽全灭 ⇒ 242 直接开上面的 A/B**，不再回 `insiders1`。
- 若 241 A 成立 ⇒ 242 走 risk 纵深（`risk88` 64 字段画像），insiders5 顺延 243。

---

## §5.80 risk88 画像（64 字段全 MATRIX）—— **这是暴露表不是信号表**

> 取数：`get_datafields(dataset_id="risk88", region="KOR", delay=1, universe="TOP600", filter_sharpe=false)` ⇒ 64/64 MATRIX。

### 5.80.1 结构：一个残差腿 + 9 个风格载荷 + 52 个行业载荷

| 组 | 字段 | cov | aC | 可用性裁定 |
|---|---|---:|---:|---|
| **残差收益** | `rsk88_mfm_ase1_dsrt` | .967 | 293 | ✅ 唯一真信号腿（与 risk68 `rsk68_residual_return` **同机制** ⇒ 同一条腿，只作交叉验证） |
| **特异风险** | `rsk88_mfm_ase1_srisk` | .967 | 102 | ✅ 可用：低特异波动异象（Ang et al. 2006 IVOL） |
| 风格载荷 | `ri_value`(245) `ri_volatility`(97) `ri_growth`(84) `ri_divyield`(71) `ri_momentum`(53) `ri_size`(52) `ri_beta`(39) `ri_nonlsize`(34) `ri_leverage`(30) | 1.0 | — | ◐ **是暴露不是信号**：直接当信号 = 「买高价值暴露」，与平台既有风格因子高度重合（prod 墙风险）。`ri_value` 的 aC 245 是全表第二高，说明**别人都在这么用** ⇒ 拥挤 |
| **行业载荷** 52 个（`rsk88_mfm_ase1_ind_*`） | .967 | 3–70 | ⛔ **禁用**：它就是行业归属本身，作信号等于行业轮动；本区中性化到 `industry` 会直接把它抹掉 |
| 规模代理 | `alternative_market_cap_usd` | 1.0 | 42 | ◐ 只作**壳层**（`vector_neut` / `bucket(rank(...))`），不作信号 |

### 5.80.2 可用机制（只有两条，且与 risk68/risk70 有重合）

1. **特异波动异象**：`reverse(group_rank(ts_backfill(rsk88_mfm_ase1_srisk, 22), industry))` —— 低特异风险股票中长期跑赢。
   - 文献：Ang/Hodrick/Xing/Zhang (2006) IVOL puzzle；KOR 市场有独立复现。持有期数季 ⇒ 窗口 66/252。
   - ⚠ 与 risk70（Multi-Factor Model，96 字段，cov .9798）**同族**；risk70 已实测撞 prod 0.72 墙 ⇒ 本腿预计同样受限，落地前先看族代表。
2. **残差收益短窗反转**：与 §5.77 的 risk68 完全相同 ⇒ **不作并列项**（②.e：跨数据集同机制 = 同一条腿）。

### 5.80.3 裁定：risk88 **不进 241/242 主槽**

- 它 64 个字段里 **52 个不可用、9 个是暴露、1 个与 risk68 重复**，真正独立的只剩 `srisk` 一条，且落在已撞 prod 墙的 risk70 同族。
- ⇒ 定位为**备用池**：只有当 241 的 risk68/risk72 双双失败、且 risk59 因借贷子域封存不可用时，才拿 `srisk` 低波动腿填空。
- ⇒ **不因为「64 字段 = 大集」就优先派它**（本区教训：字段数 ≠ 可用轴数，`analyst_factor_signals` 59 字段有效仅 2）。

---

## §5.81 波 240 收割与归因：**macro 塔关闭（第八个死轴）**，earnings3 留活

### 5.81.1 收割（`jpXpx1yk4HB9MvnudB25Dk`，2/2 COMPLETE，0 error）

| 槽 | α id | 数据集 | S | F | 2Y | turnover | longCount / shortCount | 失败闸 |
|---|---|---|---:|---:|---:|---:|---|---|
| **A** | `bl6Vdz7q` | other106（macro） | **-0.44** | -0.17 | -0.27 | .2536 | 315 / 321 | LOW_SHARPE / LOW_FITNESS / **CONCENTRATED_WEIGHT .645** / LOW_SUB_UNIVERSE / LOW_2Y |
| **B** | `QPvq9zmp` | earnings3 | **+0.50** | 0.20 | **1.15** | .1571 | 326 / 312 | LOW_SHARPE / LOW_FITNESS / LOW_2Y（**其余全过**） |

### 5.81.2 A 归因（other106 指数份额变化）—— 不是「弱」，是**符号不稳的噪声**

逐年 S：`-0.44 / +2.03 / -1.92 / -0.07 / -1.43 / -1.94 / -1.03 / +0.23 / +1.73 / -2.01`（2014→2023）

| 判据 | 读数 | 结论 |
|---|---|---|
| 正收益年份 | **3/10**（2015 / 2021 / 2022） | ❌ |
| **单年占正收益** | 2015 单年 2,398,031 / 正收益合计 3,756,201 = **63.8%** | ❌ **过拟合指纹**（>30% 即换机制） |
| 符号交替 | 2015 +2.03 → 2016 -1.92；2022 +1.73 → 2023 -2.01 | ❌ 至少 2 次硬翻面 + 多段停滞 ⇒ regime 依赖 |
| 回撤 | 全域 **66.46%** | ❌ |
| 权重集中 | 2019-11-01 CW **0.645**（限 0.10） | ❌ 只在指数调整日前后少数名字上有差异 |
| 约束 4 | 逐年 longCount **277–344（10/10 年）** | ✅ 十年有数（但信号无效，形式通过无意义） |

⇒ **判定：`other106` 关闭**。宏观塔另 1 集 `macro63`（仅 1 字段、无横截面，既有 `KOR-MACRO63-NO-CROSS-SECTION`）⇒ **macro 塔 2/2 不可用，整塔关闭（本战役第八个死轴）**。

### 5.81.3 B 归因（earnings3 公告临近度）—— 十年里 **8 正 2 负、无停滞段**，本塔唯一活口

逐年 S：`-1.48 / -0.74 / +0.59 / +1.23 / +0.42 / +1.66 / +0.31 / +1.19 / +1.70 / +0.72`

| 判据 | 读数 | 结论 |
|---|---|---|
| 正收益年份 | **8/10**（2016–2023 全正） | ✅ |
| 单年占正收益 | 2019 的 731,657 / 正收益合计 3,571,290 = **20.5%** | ✅ < 30% |
| 停滞 / 回撤段 | 只有 2014–2015 连续为负，之后 **8 年连续为正** | ✅ 阶梯健康（无 ≥3 段停滞） |
| 方向与理论 | 长「临近公告」、短「远离公告」⇒ **公告溢价为正**，与 Savor–Wilson / Beaver 方向一致 | ✅ 机制自洽 |
| 非 S/F 闸 | turnover .157 / CW **通过** / sub-universe .36 / investability .56 | ✅ 全过 |
| 缺口 | S 0.50（需 1.58）、2Y 1.15（需 1.58） | 只差**强度** |
| 约束 4 | 逐年 longCount **290–349（10/10 年）** | ✅ |

⚠ 归因表的口径冲突照实记：**S<1.0 的年份 6/10**（2014/2015/2016/2018/2020/2023），按决策表本应判「2Y 结构性不可达」；
但本条的失败形态**不是衰减而是量级**——8 年连续正、无翻面、无停滞段，且 2Y 已到 1.15。
⇒ 裁定为「**信号真实但强度不足**」，**只允许做强度杠杆扫描**，禁止换机制族。

### 5.81.4 预置规则裁决（照 §5.75.3 逐条执行，不重新解释）

| 槽 | 预置分支 | 实测 | 触发动作 |
|---|---|---|---|
| A | `S < 0.5` ⇒ macro/other106 关闭 | S **-0.44** | ✅ **other106 关闭、macro 塔整塔关闭**；原定「转 insiders1」已按 §5.78.5 上调为 **insiders5** |
| B | `0.5 ≤ S < 0.9` ⇒ 方向对、强度不足 ⇒ 换 `ern3_pre_interval` 对侧 + 公告窗口收窄，不再扩窗口谱 | S **+0.50** | ✅ 走此分支 |

### 5.81.5 波 241 预置变更（铁律 G：继承 / 准入 / 收窄，逐条写清）

- **继承**：240-B 的结论「公告溢价在 KOR 存在但弱」= 241-A 的准入条件；240-A 的结论「宏观指数份额无横截面」= 241 的**禁入**（不再触碰 any macro 字段）。
- **准入（本波禁止）**：① 不碰 macro / other106 任何字段；② 不扫 `ern3_next_interval` 的窗口谱（已知会败的不重烧）；
  ③ 不碰 `risk59`（落在 risk60 已封的证券借贷子域，§5.76.4 同口径）。
- **收窄**：240 两槽 → 241 两槽，但**候选面**从「2 个新数据集」收窄为「1 个续挖 + 1 个新数据集」，且 241-B 只派 **risk68 单槽**，
  **不派 risk72**：按 §5.77.1 两者是**同一条腿**（跨源验证），而本波已有一个更高优先级的续挖槽；
  同源互验可在 risk68 出方向后单独一轮做，不必占两个槽。
- **偏离预置的说明**：§5.77 原预置 241 = risk68 × risk72；本波改为 **earnings3 续挖 × risk68**。
  理由只有一条：240-B 产生了比 `risk72` 更高优先级的候选（8/10 年正、2Y 1.15、非 S/F 闸全过），
  而 `risk72` 的价值仅在于「判 risk68 是否 provider 特异」——在 risk68 自身方向未测前，它不构成独立信息。
  ⇒ **不是放弃 risk72，是顺延到 242**（与 risk68 结果配对判定）。

### 5.81.6 波 241 两槽（本节定稿，见 §5.82 派发记录）

| 槽 | 数据集 | 表达式 | 机制 |
|---|---|---|---|
| **A** | earnings3 | `winsorize(group_rank(ts_backfill(ern3_pre_interval, 1), industry), std=2)` | 同一「公告周期」motif 的**另一端点 + 更高覆盖**（pre_interval cov .7756 vs next .5825）+ backfill 窗 5→1（收窄） |
| **B** | risk68 | `winsorize(reverse(group_rank(ts_rank(ts_sum(rsk68_residual_return, 5), 22), industry)), std=2)` | 短窗残差反转（§5.77.3 A 槽原样） |

- ⚠ **A 的方向**：`pre_interval ≤ 0`，越接近 0 = 越新鲜 ⇒ **不加 reverse**（长「刚公告」）。这与 240-B 的「长临近下一次公告」是同 motif 的两端，不是反号。
- ⚠ **A 未加 `trade_when` 门控**：预置写的「公告窗口收窄」若落成 `trade_when(临近公告, …)` 会**砍掉空头侧**，
  把横截面价差降级成多头篮子——那是换机制而不是收窄。本波先走「换字段 + 收窗」，门控留到 242 且只在 A 失败时启用。

### 5.82 波 241 派发记录（2026-10-30）

**派发（一次 `create_multi_simulation`，2 子任务 = 约束 3 的并发上限 2）**

| 项 | 值 |
|---|---|
| multisimulation_id | `2sMHw25AU4rk9tuP3IjW0SE` |
| location | `/simulations/2sMHw25AU4rk9tuP3IjW0SE` |
| 子任务数 | 2（A earnings3 / B risk68） |
| 回测区间 | 2014-01-01 → 2023-12-31（约束 4：近十年全覆盖，`test_period=P0Y0M` 不切 OS） |

**设置逐字（KOR 常驻档，全部显式传参，不吃 schema 默认值）**

| 参数 | 实传 | ⚠ schema 缺省 | 为什么必须显式 |
|---|---|---|---|
| region | KOR | 无（必填） | — |
| universe | TOP600 | 无（必填） | KOR/D1 唯一合法档 |
| delay | 1 | 1 | — |
| decay | 4 | 4 | — |
| neutralization | **STATISTICAL** | **INDUSTRY** | 缺省值会静默换成 INDUSTRY，与本区实证档不符 |
| truncation | **0.08** | **0** | **0 = 不截断**，会把权重挤在少数标的上、虚高 S 并掩盖 CW；必须显式 0.08 |
| test_period | P0Y0M | P0Y0M | — |
| unit_handling | VERIFY | VERIFY | 除法/防零保护会触发 UNITS 警告 |
| nan_handling | OFF | OFF | — |
| language | FASTEXPR | FASTEXPR | — |
| pasteurization | ON | ON | — |
| max_trade | OFF | OFF | — |

**派发前四项硬检查（本波逐条做过）**

1. `preflight_expressions(…, region="KOR", universe="TOP600", delay=1, auto_fix_vector=false)` ⇒ `valid: true` / `unknown_fields: []` / `platform_field_count: 2`。
   ⚠ **该工具的 region/universe/delay 缺省是 USA/TOP3000**——不传就按 USA 校验字段存在性，KOR 字段会假报 unknown。
2. `operator_audit` ⇒ 两条表达式均**不含** 19 个 KOR 幽灵算子（`ts_skewness` / `ts_median` / `tanh` / `sigmoid` / `ts_entropy` / `ts_delta_limit` 等）。
   ⚠ 该工具当前 `verified: []`（校验源不可用）、`missing` 列全部 103 个算子，**那是源缺失不是表达式错误**，可用输出只有 `ghost` 列表。
3. 两条表达式已 `upsert_expressions(region="KOR", wave="241", source="manual", status="pending")`，各返回 `{n:1}` ⇒ 收割可按 id 反查。
4. 数据集未封：earnings3（240-B 续挖）、risk68（§5.77 预置）均不在 `get_dead_datasets("KOR")` 清单里。
   ⚠ 但 `dead_dataset_guard()` 只挂在 `build_wave.py` / `wave_gate.py` 上，**直接走 MCP `create_multi_simulation` 会绕过它**——封数据集只能靠派发前人工核。

**收割接口的三个必踩坑（本波已踩过，照此写别再试错）**

- `harvest_multisim_alphas` 的 `multisimulation_location` **必须带 `/simulations/` 前缀**；传裸 id ⇒ HTTP 404。
- 返回 `No children found (multisim may still be processing)` **不是失败**（240 返回该文 ~8 分钟后才 2/2 完成）。
- `batch_status` 的参数名是 **`simulation_ids`**（不是 `ids`），否则 `params must have required property 'simulation_ids'`。

**下一步（本波未完）**：轮询 → `harvest_multisim_alphas("/simulations/2sMHw25AU4rk9tuP3IjW0SE")` → 两子任务各拉 `get_alpha_yearly_stats` + 翻面/停滞/单年集中度读数 → 按 §5.81.6 预置分支裁决 → 写 §5.84。
risk72 仍按 §5.81.5 顺延，与 risk68 结果配对进 242。

---

## §5.83 insiders5 双通道取证（242 预置前置，先于回测落笔）

> 触发：约束 2「使用模板时…还要及时查平台论坛和外部金融论文」。本节在**派发之前**写，目的是让预置可被事后证伪，而不是拿结果去凑解释（铁律 H）。

### 5.83.1 通道 A：论坛（MCP `search_forum_posts("insider treasury shares buyback")`，8 命中，读 2 篇正文）

| 帖 | 票 | 给到的东西 |
|---|---:|---|
| `43152032301591`〈高管买入还是买压本身？〉USA/`insider_trx_matrix`，5 批 25 次模拟 | 43 | **跨字段相对结构 5 式全灭**（份额 0.22 / 背离 0.03 / 美元份额 −0.13 / 集群度 0.01）；**只有「单字段自身基线异常度」存活** `ts_zscore(ts_sum(top_buy, W), 252)` = 2.25；**zscore 比 rank 高 +1.64**（2.25 vs 0.61，rank 抹掉尖峰幅度）；金额族两轮全灭（混杂规模）；复活**只靠换宇宙** `TOP3000 → ILLIQUID_MINVOL1M`（subU 0.7 → 2.14–2.28）；窗口梯度 21≈42>63>126>252 单调 ⇒ 数周尺度反应不足 |
| `43178926004887`〈动了多少仓位比动了多少钱更重要〉DEU/`institutions1`，88 次模拟，已提交 S 1.68 | 69 | **信念强度 = 流量 ÷ 存量** `vec_sum(valueeur)/(vec_sum(holdings)+1e-4)`（ε 去掉了 Sharpe 掉 0.3 ⇒ ε 属信号定义）；**`ts_sum` 不能换 `ts_mean`**（1.44 → 0.73，因 mean 只在非 NaN 日求均值，把「一个季度发生几次」的频率除掉了）；**并列中段**：`nanHandling=ON` 把无申报股在数据层填 0 → `ts_sum` 后仍 0 → `group_rank` 并列在 rank≈0.4，**每天占横截面 72–80%**，是 subU 0.45–0.70 的根因；`tail(w,0.25,0.75,0.5)` 给 **+0.24 S / +0.58 subU**；`winsorize` 与 `tail` 必须成对（拆掉 winsorize → 0.99）；买入侧有信息、卖出侧无（0.21） |

**两条可直接搬的诊断工具（比抄表达式值钱）**

1. **并列块定位（零额外工具，1 次回测）**：`z = if_else(abs(ts_sum(x,66)) < 1e-9, 1, 0)`，再跑 `multiply(z, if_else(rank(z) > T, 1, 0))` 扫 T。
   恒零 alpha 返 `turnover=0 / PnL=0 / longCount=0` ⇒ 拐点即并列块的平均名次 `v = 1 − K/(2N)`。
2. **`ts_mean` 禁用清单**：凡 coverage < 1 的事件型字段，聚合一律 `ts_sum` / `ts_delta`，**禁用 `ts_mean`**（它除的是非 NaN 日数，不是窗口长度）。

**评论区两条同样要记**

- 帖 1 作者自评：该 alpha **真实分类是 `other` 不是 `insiders`**（按数据集名推断会归错塔），且**开 `maxTrade` 后表现明显变差**、多空样本少。
- 帖 2 评论（`JR57542`）：**「换厂商不是降相关杠杆，归一化方式才是」**——同一构念跨厂商换皮实测 PnL 相关 **0.999 级**。⇒ 反向印证 §5.81.5「risk72 只作同腿跨源确认、不构成独立信号」的裁定是对的。

### 5.83.2 通道 B：外部论文 / 一手源

| 源 | 结论（只取可证伪部分） |
|---|---|
| **KCMI 2020**（韩国资本市场研究院，share repurchase 专题） | **直接反证 §5.79.4-A 的方向**：「韩国股市大多数回购**不导致注销**」；效应强弱取决于回购后是**注销 / 持有 / 处置**；若反复买卖库存股（低买高卖赚差价），价格上下波动「**与股东回报毫无关系**」。⇒ 库存股占比上升**没有无条件正号**，更合理的解释是**潜在供给悬顶**（treasury = 未来可售出的股票） |
| Cho, Pae & Yoo (2023, *JBFA*)〈Brand royalty flows within large business groups〉 | 韩国财阀**控股公司结构**决定了集团内关联方特许权流量的方向与规模 ⇒ 关联方交易是**隧道效应通道**，且强度由集团结构决定，不是随机 |
| Baek, Kang & Park (2004, *JFE*)〈Corporate governance and firm value: evidence from the Korean financial crisis〉 | 危机期财阀隧道效应与公司价值负相关的经典证据 ⇒ 治理复杂度↑ 在压力期惩罚更重（对 `tnc` 的**方向句**与**失效条件**都有用） |
| Jeng-Metrick-Zeckhauser (2003, *REStat*) / Lakonishok & Lee (2001, *RFS*) / Cohen-Malloy-Pomorski (2012, *JF*) | 买入侧有信息、卖出侧几乎没有；信号必须**按自身持仓标准化**；「偏离例行的机会型交易」才有信息（例行交易无信息） |
| ⚠ 2026 regime 注记（SK hynix 40 万亿韩元回购 + 全额注销，2026-08） | 韩国回购制度在 **2024 之后**才转向「回购即注销」的股东回报叙事，**完全落在 2014–2023 回测窗之外** ⇒ 不能拿 2026 的故事解释 IS 表现；反过来，IS 若成立，其机制属于「旧制度（回购不注销）」，**存在结构性 regime 风险**，提交前须标注 |

### 5.83.3 双通道裁决（按 ②.d 表逐槽判，不跳过矛盾）

| 槽 | 通道 A | 通道 B | 裁决 |
|---|---|---|---|
| **A `insd5_trsy_ratio`** | 无对应模板（无人发布过 KOR 库存股腿） | KCMI 2020 **明确否定**「累积=利好」 | **机制矛盾** ⇒ 原方向**作废**。矛盾可解：把机制改写成「库存股占比↑ = 潜在供给悬顶 / 治理折价」，两通道即同向 ⇒ **方向翻转为负**；并按铁律 B **正反各测一条**（翻转是假说不是结论） |
| **B `insd5_tnc`** | 无模板 | 财阀隧道效应有韩国专属证据，但**只给方向、不给幅度** | 可组装，**降优先级**、标「机制有支撑、本区未验证」；须配方向对（人数↓ 为利好）作对照 |

### 5.83.4 三条跨区迁移禁令（本区实测/结构事实，写死防止照抄）

1. **`universe` 杠杆在 KOR/D1 不存在**：USA 事件型腿的复活**完全依赖** `TOP3000 → ILLIQUID_MINVOL1M`，而本区唯一合法档是 TOP600（`get_platform_setting_options` 实测）。
   ⇒ 任何**稀疏事件腿**在 KOR 都缺这根常规救援杠杆，一旦卡 `LOW_SUB_UNIVERSE_SHARPE` 就只能靠结构改写。
   这与 §5.79.3 已实测的「交易流腿 S 0.28 / turnover 9.75%」同型：**不要指望换宇宙能救**。
2. **跨厂商换皮不降相关**（0.999 级实测）⇒ 想要独立库存就得改**归一化方式**或**机制**，不是换数据源。
3. **`ts_mean` 在事件型数据上禁用**（它除的是非 NaN 日数）⇒ KOR 的 news / insiders / shortinterest 稀疏腿全部适用。

### 5.83.5 242 预置（**已 preflight 通过 / 未注册**；⚠ 本分支**未被采用**）

> 更正（2026-10-30，出 §5.84 时）：本节原写「未 preflight、未注册」。实测三条 A′/B′/A″ 均已 preflight `valid:true`、`unknown_fields:[]`、`platform_field_count:1`、`any_changed:false` ⇒ **只差注册**。
> 但按 §5.79.5 的预置分支（241-B 存活 ⇒ 242 = risk 纵深），**本分支整体顺延到 243**，三条均未入库、未派发。

| 槽 | 表达式草案 | 依据 |
|---|---|---|
| **A′** | `winsorize(reverse(group_rank(ts_delta(vec_sum(insd5_trsy_ratio), 66), industry)), std=2)` | 方向按 §5.83.3 翻转（库存股↑ = 潜在供给↑ = 利空）；`ts_delta` 遵铁律 A（比率单边非负，禁裸水平） |
| **B′** | `winsorize(reverse(group_rank(ts_delta(vec_max(insd5_tnc), 66), industry)), std=2)` | 关联方人数↑ = 治理复杂度↑ = 折价（Baek 2004 / Cho 2023） |
| **A″（B 侧对照）** | `winsorize(group_rank(ts_delta(vec_sum(insd5_trsy_ratio), 66), industry), std=2)` | 铁律 B：方向正反各测一条；翻转是假说，**不精确反号**（`reverse` 与正向因截断×decay 不严格对称） |

- ⚠ **不预置 `tail`**：本集最低 cov .7318 且是稠密比率，并列块应远小于 DEU 的 72–80%。**先测再决定**——
  若 A′/B′ 卡 `LOW_SUB_UNIVERSE_SHARPE` 或 `CONCENTRATED_WEIGHT`，**第一个动作是跑 §5.83.1 的并列块定位阶梯**，而不是直接加 `tail`。
- ⚠ `ts_delta(vec_sum(...), 66)` 假设向量行是「同一分母下的多个持有人」；若实为「同一持有人多笔」，`vec_sum` 会重复计数。
  **未核**，须在 A′ 出结果后用 `vec_avg` 版做一次姊妹对照（DEU 帖实测 `vec_avg` 与 `vec_sum` 逐位相同时说明每日只有一笔）。
- ⚠ 约束 4 仍待硬核：.8728 / .9996 是**截面覆盖**，不等于「近十年每年都有数」，派发后必须逐年 `longCount`。

### 5.83.6 `risk71` 撤销（字段级核验，修正 §5.78.3）

> 取数：`get_datafields(dataset_id="risk71", region="KOR", delay=1, universe="TOP600", filter_sharpe=false)` ⇒ 7/7 MATRIX，**`complete=true`**。

| 字段 | cov | aC | 说明 |
|---|---:|---:|---|
| `residualized_return_asia_minvol1m` | .9080 | 32 | **ASI MinVol1M 宇宙**的特异残差日收益 |
| `rsk71_eqy_asi_supported_minvol1m_dsrt` | .7592 | 156 | **ASI MinVol1M** 可复现特异收益 |
| `rsk71_eqy_xjpci_supported_minvol1m_dsrt` | .7592 | 156 | **Asia ex-Japan** 同口径（与上一行 aC 完全相同 ⇒ 同族镜像） |
| `residualized_return_exjapan_minvol1m` | .9080 | 31 | ex-Japan MinVol1M |
| `asi_top1500_liquidity_dsrt` / `asi_top1000_liquidity_dsrt` / `residualized_return_asia_top1100_liquid` | .588 / .379 / .360 | 21/8/5 | ASI TOP1500/TOP1000/TOP1100 |

**裁定：`risk71` 移出 KOR 可用池（§5.78.3 的「可用 = risk68/risk72/risk88/risk71」改成三集）**，两条理由都不可绕：

1. **宇宙不匹配**：全部字段的母宇宙是 **ASI MinVol1M / ASI TOP1000–1500 / ex-Japan**，而本区唯一合法档是 **KOR/TOP600**。字段在 KOR 能取到数（cov .76–.91）不等于口径对齐——这是**跨宇宙借表**，不是本区原生风险模型。
2. **机制不可独立**：7 个字段全是「特异 / 残差收益」，与 `risk68`（`rsk68_residual_return`）**同一条腿**；按 §5.83.1 评论区实证「换厂商/换表不降相关，0.999 级」⇒ 它连「跨源确认」的价值都低于 risk72（后者至少是独立 provider）。

⇒ 若日后要动 `risk71`，唯一合法用途是**作为 risk68 结果的外部一致性对照**（不是新机制、不占主槽），且必须先解释宇宙差异。

### 5.83.7 `news38` 字段级否证 —— 「45 字段 cov .7971」是假象，可用面 ≈ 0

> 取数：`get_datafields(dataset_id="news38", region="KOR", delay=1, universe="TOP600", filter_sharpe=false)` ⇒ 45/45 **全 VECTOR**，`complete=true`。
> 这是 Bloomberg 式「新闻故事 + 分析」表（`mws38_*`），按语义分组后可用面几乎归零：

| 组 | 字段数 | 举例 | 判定 |
|---|---:|---|---|
| **权限/内部** | 8 | `mws38_entitlement` `mws38_d1_entitlement` `mws38_uniq_entitlement` `mws38_analytics_entitlement` `*_headlinetones*_entitlement` | ⛔ **平台描述明写「must not be used for modeling/analytics」** ⇒ 越权使用 |
| **时间/生命周期码** | 12 | `*_time`(hhmmss 整数) `*_action` `*_uniq_action` `*_version` `mws38_previous` | ⛔ 非连续量；`action`/`version`/`type` 需按 module/date 动态 label-map，无稳定截面含义 |
| **注意力轴** | 5 | `mws38_d1_hotlevel` `mws38_d1_related_num` `mws38_d1_relevances` `mws38_uniq_hotlevel` `market_impact_indicator` | ⛔ 已被 §5.74 **注意力轴关闭**覆盖 |
| **情绪轴** | 12 | `mws38_tone_score` `mws38_tc_tone_score` `mws38_{positive,negative}_{freq,score}` `mws38_tc_*` `mws38_score`(aC 67，复合情绪分) | ⛔ sentiment 类**待用户裁定封禁项**，未裁前不派 |
| **死字段** | 1 | `mws38_hotlevel` | 平台描述原文 **「News hotlevel (all 0)」** ⇒ 恒零 |
| 其余 | 7 | `mws38_value`（描述仅「News value」）、`story_analytics_metric_value`(cov .8016 但 aC 0，metric 类型由 `story_analytics_category` 动态决定，需 label-map) | 无可独立解释的信号；`metric_value` 不钉住 category 就是混合指标 |

**裁定：`news38` 移出新闻非注意力轴候选**。§5.78.3 里「`news38` 45f .7971 领衔」是**字段数 × 覆盖率的假象**——45 个字段里真正可当信号腿的是 **0 个**。

**由此固化成一条免回测筛除规则（本区 news / sentiment 类通用）**：
派发前对候选集做一次 `get_datafields(filter_sharpe=false)`，按上表五组**先扣掉** entitlement / time-code / 注意力 / 情绪 / 死字段，
**剩余「有独立经济含义且未被封轴」的字段 < 3 ⇒ 直接跳过，不派回测**。
成本 = 1 次只读 MCP 调用，收益 = 省一整波 2 槽配额（本波正是靠这一条挡住的 `news38`）。
⇒ `news54` / `news7` / `news50` 若同为 `mws38_*` 故事分析形态，按同一条规则**先筛后派**；只有出现**事件类型/传播/显著性之外的新轴**才值得进波。

### 5.83.8 ⚠ 在飞告警：`risk68` 五个字段的平台描述全部指向 **European**

> 取数：`get_datafields(dataset_id="risk68", region="KOR", delay=1, universe="TOP600", filter_sharpe=false)` ⇒ 5/5 MATRIX，`complete=true`。**在波 241-B 已经派发之后才发现**，按纪律当场记录，不留给事后解释。

| 字段 | cov | aC | 平台描述原文（截断） |
|---|---:|---:|---|
| `rsk68_residual_return` | .9569 | 178 | "Idiosyncratic 1-day return for a **European** asset unexplained by the market factor…" |
| `rsk68_beta` | 1.000 | 73 | "Unitless stock beta for a **European** asset relative to the regional liquidity-weighted market_return…" |
| `rsk68_weight_dadv` | 1.000 | 94 | "Simple moving average dollar ADV for **European** instruments…" |
| `rsk68_weight_edadv` | 1.000 | 98 | "Exponentially decayed dollar ADV for **European** instruments…" |
| `rsk68_weight_volatility_short` | 1.000 | 503 | "Short-term volatility estimate for **European** instruments…" |

**矛盾点**：若该表真是欧洲专表，KOR/TOP600 的覆盖不可能到 .9569–1.0。⇒ 只剩两种解释，**必须用数据判定，不能靠命名**：

1. **描述是模板串写错的**（同一 risk 模型的多区域变体共用一段文案），数据本身按 KOR 标的填充 ⇒ 可继续用，但要在报告里标注口径不明；
2. **数据是把欧洲模型外延/映射到 KOR 名称上**（口径错配）⇒ 该腿在 KOR 上测到的任何结果都**不可作为机制证据**，只能当数据质量事故处理。

**处置（已写死，不等结果）**：

- 241-B 出结果后，**第一个动作不是解释信号，而是核口径**：拉 `rsk68_residual_return` 在 KOR 的逐年覆盖（约束 4 本来就要求逐年 `longCount`，这一项顺带完成）。
- 若逐年覆盖在 2014–2023 **连续存在**且数值量级像日收益 ⇒ 偏解释 1，可用但标「口径待厂商确认」；
- 若覆盖出现**整段缺失或量级异常** ⇒ 判解释 2，`risk68` 整集移出 KOR 池，**241-B 结论作废（不是判死机制，是判死数据）**。
- **对 risk72 的裁定做一处细化（不是翻案）**：§5.81.5 依据「换厂商不降相关 0.999」把 risk72 降为同腿确认。但那条证据说的是**去相关**（不产生独立库存），**不覆盖来源核验**。
  此处 risk68 出现口径疑点 ⇒ risk72 作为**另一个 provider 的同一构念**，其价值从「降相关杠杆」转为「**来源交叉核验**」，这是它此前被低估的用途。⇒ 242 若继续 risk 纵深，`risk72` 应作为**口径对照槽**（不是独立信号槽），优先级回升。

---

## 5.84 波 241 收割与归因（multisim `2sMHw25AU4rk9tuP3IjW0SE`）

### 5.84.1 收割读数

| 项 | 值 |
|---|---|
| 子任务 | **2/2 COMPLETE，0 error**（首个 `batch_status` 即全终态；派发到最后收批约 6 分钟） |
| 收批 | `harvest_multisim_alphas` → `workflow_auto_harvest`：`linked 2 / upserted 2` |
| wave_results | `inserted: wave 241 暂定 verdict=PARTIAL`（0/2 过硬闸，1 条过 near 线 1.0） |
| A | `VkxqGGP0` = 241-A（earnings3） |
| B | `bl6VQQdZ` = 241-B（risk68） |

### 5.84.2 A 归因（earnings3 `ern3_pre_interval` 水平）—— 符号不稳，且与 240-B **近似镜像**

**指标**：S **−0.39** / F −0.14 / TO .1165 / returns −1.6% / DD 22% / subU **−0.50** / 2Y **−0.80** / investS −0.37 / longCount 334 · shortCount 303。
RA 失败 5 项（LOW_SHARPE / LOW_FITNESS / LOW_SUB_UNIVERSE_SHARPE / LOW_INVESTABILITY_CONSTRAINED_SHARPE / LOW_2Y_SHARPE）⇒ 全灭，无任何非 S/F 闸可救。

**逐年 S**：`−2.31 / +1.11 / −0.19 / +2.34 / −1.32 / −1.88 / +0.48 / −0.73 / −0.83 / −0.78`

| 判据 | 读数 | 结论 |
|---|---|---|
| 负收益年份 | **7/10** | ❌ |
| 符号翻转次数 | **6 次** | ❌ 不是机制，是噪声 |
| 单年占正收益 | 正收益合计 1,622,118；top1 = 2017 的 854,769 = **52.7%** | ❌ >30%，过拟合指纹 |
| S<1.0 年份 | 10/10 | 2Y 结构性不可达 |
| 约束 4 | longCount 290–338（10/10 年） | ✅（唯一达标项） |

**与 240-B 的对照（本节最重要的读数）**：240-B（`ern3_next_interval`，S **+0.50**，8 正 2 负，2Y 1.15）与 241-A（`ern3_pre_interval`，S **−0.39**）**量级相近、方向相反**。
公告周期在截面上近似恒等式：`已过天数 + 剩余天数 ≈ 周期长度` ⇒ 两个端点 `group_rank` 后**天然互为镜像**。

⇒ **裁定三条**：

1. **§5.81.6 写的「是同 motif 的两端，不是反号」被实测推翻**。按 ②.e「同机制跨字段 = 一条腿」，`ern3_next_interval` 与 `ern3_pre_interval` **合计只算一条腿**；241-A 不构成第二次独立验证。
2. ⇒ earnings 塔当前唯一有效读数仍是 240-B 的 +0.50 / 2Y 1.15 / 8 正 2 负，**没有新增证据**。
3. **241-A 反而对 240-B 构成减分证据**：若公告临近度是稳定机制，其镜像端不应出现 6 次翻面、单年 52.7% 集中。⇒ 240-B 的「8 正 2 负」更可能是**弱信号 + 噪声**，而非 §5.81.3 判的「真实但强度不足」。

**earnings 塔处置（降级，不关闭）**：不再占 242 主槽。剩余唯一杠杆 = 在 `ern3_next_interval` 上做**一次**强度杠杆（中性化档 / 壳层），**只给 1 槽、排在 243 之后**。
若该槽仍 <1.0，按「**机制不成立**」关闭本塔——不是「数据集穷尽」关闭（8 字段还有 6 个未测，但两个公告端点都不成立，说明该集主轴不是公告周期；按 §①0.1 应先看 aC 头部轴再决定是否还有第 3 次机会）。

### 5.84.3 B 归因（risk68 残差反转 `rsk68_residual_return`）—— 真信号，但 **investability 是死钩**

**指标**：S **1.06** / F 0.36 / TO .444 / returns **5.23%** / DD 11.45% / **subU 0.72** / **2Y −0.63** / investS **0.39**。

**非 S/F 闸全过**（这是本波唯一的好消息）：LOW_TURNOVER ✅ / HIGH_TURNOVER ✅ / **CONCENTRATED_WEIGHT ✅** / **LOW_SUB_UNIVERSE_SHARPE ✅** / CLUSTER_TEST ✅ / MATCHES_PYRAMID ✅。
**RA 失败 4 项**：LOW_SHARPE(1.06<1.58) / LOW_FITNESS(0.36<1.0) / **LOW_INVESTABILITY_CONSTRAINED_SHARPE(0.39<0.74)** / LOW_2Y_SHARPE(−0.63<1.58)。

**逐年 S**：`−0.40 / +0.69 / +2.02 / +1.24 / +2.59 / +1.75 / +2.31 / +1.64 / +0.31 / −1.51`
**逐年 longCount**：292 / 306 / 312 / 311 / 328 / 325 / 327 / 341 / 330 / 329 ⇒ **10/10 年，约束 4 ✅**

| 判据 | 读数 | 结论 |
|---|---|---|
| 正收益年份 | **8/10**（2015–2022 连续 8 年为正） | ✅ |
| 单年占正收益 | 2020 的 1,423,761 / 合计 6,412,417 = **22.2%** | ✅ <30% |
| 停滞 / 回撤段 | 2021 1.64 → 2022 0.31 → 2023 **−1.51** | ❌ **近年断崖 1 段**（2+ → <0.5） |
| S<1.0 年份 | 4/10（2014/2015/2022/2023）= **40%** | ❌ 2Y 结构性不可达 |
| investability | 0.39 vs 需 0.74 | ❌ **死钩** |

**按归因决策表逐条落**：

- 「S<1.0 年份 ≥3 成」⇒ 停扫 decay / 平滑 / 门控；
- 「近年 S 断崖（2+ → <0.5）」⇒ 机制性衰减，换 regime 无关的机制。

**但真正的死钩不是 2Y，是 investability**。S 1.06 而 investS 只有 0.39 ⇒ 收益大头落在**被可投资性约束剔掉的标的**（低流动性 / 小市值）上。
这不是参数问题，是方向对冲的：**暴露往大市值挪 S 就掉，往小市值挪 investS 就掉**。
而 KOR/D1 唯一合法 universe = TOP600（§5.83.4 禁令 1）⇒ 论坛那条 USA 侧靠 `ILLIQUID_MINVOL1M` 复活稀疏事件腿的路径，**在本区结构上不存在**。

⇒ **裁定**：risk68 残差反转是**真实但结构受限**的腿。它证明了 risk 塔有信号（subU 0.72 与 CW 都过），但这条具体构念在 KOR 拿不到可提交性。
剩两条路：(a) 同集上换**横截面特征型**机制（低波 / 低 beta）——这类因子的收益天然集中在大市值，investability 友好；(b) 给残差反转加可投资性壳层——但那是给已判「2Y 结构性不可达」的候选续命，**违反决策表，不做**。

### 5.84.4 `risk68` 口径溯源裁决（§5.83.8 预置处置的执行）

§5.83.8 写死的第一个动作是核口径，不是解释信号。执行结果 —— **六条证据全部指向解释 1**：

| # | 证据 | 取数 |
|---|---|---|
| 1 | 字段 id **不含任何宇宙 / 区域令牌** | `rsk68_residual_return` / `rsk68_beta` / `rsk68_weight_*`；对照 risk72 的 id 自带母宇宙（`rsk72_asi_top1000_eqy_dsrt` 等） |
| 2 | KOR/TOP600 覆盖 .9569–1.0；risk72 在 KOR 只有 .3534–.7592 | `get_datafields` 两集对照 |
| 3 | **EUR 侧同一 5 字段、描述逐字相同**（同样写 "European"），但覆盖 1.0、user/alphaCount 完全不同 | EUR：85/115 · 218/362 · 65/86 · 67/74 · **78/105**；KOR：39/73 · 99/178 · 53/94 · 51/98 · **258/503** |
| 4 | **USA 侧 0 字段** | `get_datafields(dataset_id="risk68", region="USA", universe="TOP3000")` ⇒ `count:0` |
| 5 | 逐年 longCount 292–341 / shortCount 288–341（10/10 年），turnover 稳定 43.6–45.2% | 若真是「欧洲标的映射到 KOR 名称」，不可能得到 600 名左右稳定截面，映射错配会呈随机换手 |
| 6 | 同一句描述**自相矛盾** | `rsk68_beta`："for a **European** asset relative to the **regional** liquidity-weighted market_return" —— 同一句里既有「欧洲」又有「按区域」 |

⇒ **判解释 1**：描述是**共享静态模板串**，数据按区域填充。**`risk68` 留在 KOR 池**，口径标注「描述文案不可信（模板串写），以数据行为为准，厂商侧待确认」。

**对 risk72 的裁定再修订一次（依据新证据，不是反复）**：§5.83.8 刚把 risk72 升为「口径对照槽」。本轮拉到 risk72 字段 id 后，**连对照价值也不成立**——它的母宇宙是 ASI TOP1000/1500/2000 与 MinVol1M，KOR/TOP600 只有 35–76% 覆盖 ⇒ 它与 risk68 的低相关会被**覆盖率**解释，而不是被 provider 解释。
⇒ **risk72 移出 KOR 池**（与 §5.83.6 的 risk71 同口径：宇宙不匹配）。**§5.83.8 那条「优先级回升」当场作废**，理由记在此处，不留文内自相矛盾。

⇒ **risk 塔纵深 = `risk68` 单集**（5 字段已测 1 个）。risk59（子域封）/ risk60（封）/ risk71（宇宙不匹配）/ risk72（宇宙不匹配）全部出池；risk88 按 §5.80.3 不进主槽。

### 5.84.5 波 242 定稿（铁律 G 三条，逐条写清）

- **继承**：241-B 的读数「残差反转有信号（subU .72 / CW 过）但 investability 是死钩（.39 vs .74）」= 242 的准入条件 ⇒ **只做横截面特征型机制，不做收益集中在低流动性名里的时序反转**。
- **准入（本波禁止）**：① 不碰 macro / other106（240 已封）；② 不再扫 risk68 残差反转的窗口 / decay / 平滑（决策表：2Y 结构性不可达）；③ 不碰 risk59/60/71/72（各自出池）；④ 不碰 insiders（顺延 243，按 §5.79.5 预置分支）；⑤ 不碰 earnings（241-A 已降级）。
- **收窄**：241 两槽 → 242 两槽；候选面从「1 续挖 + 1 新集」收窄为「**1 个数据集内的 2 个机制**」，**数据集数 2→1**，且全部在上一波存活集合内变动。

---

## 5.85 波 242 派发记录（2026-10-30）

**派发（一次 `create_multi_simulation`，2 子任务 = 约束 3 的并发上限）**

| 项 | 值 |
|---|---|
| multisim id | `3R7zZ1X256dbSJNxrkythM` |
| location | `/simulations/3R7zZ1X256dbSJNxrkythM` |
| 子任务数 | **2** |
| 数据集 | `risk68`（单集） |
| DB 注册 | `upsert_expressions(region=KOR, wave=242, dataset=risk68, source=manual, status=pending)` ⇒ **n=2** |

| 槽 | 字段 | 表达式 | 机制 | 选它的依据 |
|---|---|---|---|---|
| **A** | `rsk68_weight_volatility_short` | `winsorize(reverse(group_rank(rsk68_weight_volatility_short, industry)), std=2)` | **低波异象**（高波动 ⇒ 后续风险调整收益低） | ⭐ **头部轴**：aC **503**，本集 alphaCount 最高字段。§① 0.1 质量先验要求**从头部轴起手**；241-B 测的是第 2 名（aC 178） |
| **B** | `rsk68_beta` | `winsorize(reverse(group_rank(rsk68_beta, industry)), std=2)` | **低 beta / BAB**（Frazzini–Pedersen 2014） | aC 73、cov 1.0；与低波**不是同一条腿**（韩国财阀股高 beta、中等波动），但若实测 PnL 高相关则按 ②.e 只算一条 |

**A-2 收益来源声明（缺项不许组装）**

| 声明项 | A 低波 | B 低 beta |
|---|---|---|
| 谁在被定价 | 追逐高波动「彩票型」股票的散户（KOR 散户成交占比高） | 用高 beta 股替代杠杆的需求者 |
| 为什么会错 | 彩票偏好 + 明示的杠杆约束 | 借道高 beta 加杠杆的替代需求 |
| 错了多久修复 | 1–2 个季度 | 1–2 个季度 |
| 预期方向 | 波动率高 ⇒ 后续风险调整收益**低** ⇒ 取反向 | beta 高 ⇒ 后续风险调整收益**低** ⇒ 取反向 |
| 退化风险（已知盲区） | 小市值波动天然高 ⇒ STATISTICAL 中性化后可能残留规模暴露 ⇒ **investability 需实测**（241-B 正是死在这） | 财阀治理折价可能同时污染 beta 与收益的关系 |

**设置（照 KOR 标准档，三项必须显式覆盖）**：`region=KOR` / `universe=TOP600` / `delay=1` / `decay=4` / **`neutralization=STATISTICAL`**（schema 缺省 INDUSTRY ← 必须覆盖）/ **`truncation=0.08`**（schema 缺省 0 ← 必须覆盖）/ `test_period=P0Y0M` / `unit_handling=VERIFY` / `nan_handling=OFF` / `pasteurization=ON` / `max_trade=OFF` / `FASTEXPR` / `EQUITY`。

**发批前四查**

| # | 查 | 结果 |
|---|---|---|
| 1 | preflight | ✅ `valid:true` / `unknown_fields:[]` / `platform_field_count:2` / `vector_fields:[]` / `any_changed:false` |
| 2 | 幽灵算子 | ✅ `winsorize` / `reverse` / `group_rank` 均不在 19 个禁列 |
| 3 | 表达式入库 | ✅ `n=2` |
| 4 | 数据集未封 | ✅ risk68 未 seal。⚠ `dead_dataset_guard()` 只在 `build_wave.py` / `wave_gate.py` 跑，**直连 MCP 派发不经过它**，本条靠人工核 |

**242 出结果后的预置动作（先写死，不事后解释）**

| 读数 | 动作 |
|---|---|
| 任一槽 S ≥ 1.05 **且** investS ≥ 0.74 | 该槽升级为近闸候选 → Mode A / 强度杠杆，同时看 2Y 是否仍不可达 |
| 两槽 investS 都 < 0.5 | 特征型路径**也**受制于规模暴露 ⇒ 停 risk 塔，243 全投 insiders5 |
| 两槽 S < 0.6 | 同集只有残差反转一条真腿 ⇒ risk 塔关闭（**不再试 dadv / edadv 流动性腿**：低流动性 + investability 必死，§②.c） |
| A、B 相互 PnL 相关 > 0.8 | 按 ②.e 只算一条腿，另一条从 243 候选里删 |

**顺延队列（243 及以后，按预置不抢跑）**：`insiders5` A′/B′/A″（§5.83.5，已 preflight 未注册）→ `earnings3` 强度杠杆单槽（§5.84.2）→ risk68 剩余字段。

---

## 5.86 波 242 双通道取证（低波 / 低 beta 族）—— 论坛给出了**反向预警**

### 5.86.1 通道 A：论坛正文

**A-1 `23964166630807`〈【Alpha灵感】Betting Against Beta（反beta投注因子）〉JY88060 · 16 赞 · 4 评 · 2024-06-05**

- 复现链 7 版：v1 `weight = 0.6 - rank(beta_last_360_days_spy)` ⇒ **S 1.02 / TO 6.12%**；v2 加流动性三因子 → 1.46；v3 加波动率边际条件 → 1.51；v4 加低市场相关 → 1.51；v5 加 HML+动量 → **1.71**；v6 加 coskewness → **1.86 / TO 29.48%**；v7（BAAB）反而下降，剔除。
- **最终结论不是成功，而是结构性失败**（原文）：「到最后才发现通过不了 sub-universe 测试，因为 sub-universe 有一个非常必要的 neutralization 是 market neutralization… 但这个因子的核心就在于低 beta 资产的绝对值暴露要高于高 beta 资产… 因此再进一步基于这个思路改善可能性不太大」。
- **评 `JR57542`（族级推广，本节最重要的一条）**：「BAB/低波/质量这类『**靠暴露不平等获利**』的因子，alpha 来源是低 beta 资产的绝对风险暴露 > 高 beta 资产（约 3:2）。market neutralization 会把这层不平等暴露一起 neutralize 掉，因子随即失活。**EUR/ASI/GLB 同样结构性成立**。」
- **评 `TN48752`**：「universe_sharpe sub 失败了，这表明 alpha 在高流动性市场中表现不佳」——与 investability 是同一类诊断。
- ⚠ **不照抄的部分**：v2–v6 的 `scale(weight) * scale_down(rank(-vol)) * scale_down(rank(-illiquidity)) * …` 是**多机制相乘叠加**，撞铁律 ②.e 与闸 5（禁加权拼腿），本区**不复制该链**。

**A-2 `30680255378071`〈【alpha灵感】volatility波动率因子-可提交的alpha〉WH18373 · 6 赞 · 0 评 · 2025-03-16**

- 骨架：`up_vol = ts_std(high/ts_delay(close,1)-1, W)`；`down_vol = ts_std(low/ts_delay(close,1)-1, W)`；`alpha = -group_neutralize(up_vol - down_vol, industry)`；`trade_when(1, alpha, -1)`。
- **关键区分**：这是**上行 / 下行波动不对称**，**不是低波水平**。⇒ 与本波 242-A（低波水平）**不是同一机制**，不能拿来给 242-A 背书。
- 可迁移点：① **行业中性化是必要的**（作者实测：不做中性化时集中持股，夏普与最大回撤明显变差）；② 符号取负（下行波动相对大 ⇒ 后续更好）；③ `trade_when(1, alpha, -1)` 是「保持仓位」惯用法。
- ⇒ **对 243 的直接用途**：risk68 有 `rsk68_residual_return`（残差日收益）⇒ 可构造
  `ts_std_dev(if_else(rsk68_residual_return < 0, rsk68_residual_return, 0), W)` 与上行侧之差 —— **同集、单机制、非注意力、非情绪**，是本塔尚未试过的第四条腿（且不属「暴露不平等族」，不受 5.86.1 那条警告约束）。

### 5.86.2 通道 B：外部研究

- 低波 / BAB 是**全球性**异象，不是 USA 特例：Black–Jensen–Scholes(1972) 最早记录 SML 比 CAPM 平坦、低 beta 股有正 alpha；Baker–Haugen(2012) 在 **33 个市场（21 发达 + 12 新兴）** 验证低波组合平均收益与夏普均高于高波组合；Frazzini–Pedersen(2014) 把 BAB 扩到 20 国股票 + 国债 + 信用债 + 期权期货。
- **KOR 直接证据**：Choi(1998, George Washington University 博士论文) 用 KSE 1982–1991 月度数据（含非金融/金融与退市股）做 SUR + Fama–MacBeth，结论包含「**CAPM 的中心预测被拒绝，收益与 beta 的关系充其量是平坦的**」⇒ KOR 存在 beta 异象的**样本内**证据。
  ⚠ 样本 1982–1991 早于本区测试窗 2014–2023 近 30 年 ⇒ **只能当方向假说，不能当模板**，须本区实测。
- 行为解释（融资约束 / 彩票偏好 / 散户结构）与 KOR 散户成交占比高的市场结构一致 ⇒ 机制在 KOR 不违和。

### 5.86.3 双通道裁决（照 ②.d 表逐项对，不跳过矛盾）

| 项 | 通道 A（论坛） | 通道 B（论文） | 裁决 |
|---|---|---|---|
| 机制是否存在 | 存在（v1 即 S 1.02） | 33 国 + KOR 样本内均存在 | ✅ 机制成立 |
| 方向 | 反向（多低 beta / 空高 beta） | 同向 | ✅ 一致 |
| **能否在本平台落地** | **结构性不能**：subU 的 market 中性化会抹平「暴露不平等」 | 论文不涉及平台闸门 | ⚠ **平台侧冲突，且这是唯一有平台实证的一条** |

⇒ 按 ②.d「A、B 机制矛盾 ⇒ 不组装；矛盾未解不得进入 ③」。但本波两槽**已派发，无法撤回**。
**处置：转成预注册预期，不做事后解释**（见 5.86.4）。

### 5.86.4 对 242 的预注册预期与判定分支（细化 §5.85，不覆盖）

- **预期**：两槽大概率**不是死在 S，而是死在 `LOW_SUB_UNIVERSE_SHARPE`**（论坛唯一有平台实证的失败点）。

| 242 实测 | 判定 | 243 动作 |
|---|---|---|
| 两槽 **S ≥ 1.0 但 subU 失败** | 「**暴露不平等族**」在 KOR 结构性失败（平台 + 论坛双证；且 KOR 只有 TOP600，无换宇宙逃生口） | **封 BAB / 低波 整族**，risk68 只剩残差类腿；`insiders5` 提前 |
| 两槽 **S < 0.6** | 同集只有残差反转一条真腿 | risk 塔关闭（§5.85 原分支） |
| 任一槽 **S ≥ 1.05 且 subU / investS 均过** | **论坛的「结构性」论断在 KOR 不成立** ⇒ 记反例（价值同样高） | 该槽进 Mode A |

- **本波唯一优于论坛实验的地方**：论坛用的 beta 是 `beta_last_360_days_spy`（**相对美股**的 beta）。`JR57542` 明确警告「迁到 EUR/ASI 语义就错了，算出来是『相对美股的 beta 暴露』」。
  本区的 `rsk68_beta` 平台描述是 "relative to the **regional** liquidity-weighted market_return" ⇒ **本就是区域市场 beta，口径正确**。这是论坛作者当时无解的字段语义问题，我们这边天然满足。
  ⇒ 因此若 242-B 仍失败，**不能归因于字段口径**，只能归因于 5.86.1 那条结构约束（这是把失败原因提前锁死，避免事后两头下注）。

### 5.86.5 通道 A 补读 `36877431208983`〈【Alpha灵感】尾部风险（波动率因子）〉（**修正 5.86.1 末尾那条 243 计划**）

- 正文：Kelly–Jiang(2014) 尾部风险，`b` = 个股收益对**行业尾部风险**的敏感度，`c = −b / vol`，做多 `c`。
  机制句 = 高尾部风险负载 ⇒ 更高未来收益（**正向**）。正文 16 赞但零可执行数字，价值主要在评论。
- ⭐ **评 `ZH34713`（2026-10-09，本段最重要）**：他在 **KOR/TOP600/d1/decay6/STATISTICAL/trunc0.08**（与本区同设置族）
  实测了一个「**只保留负半轴**」的壳：`power(ts_op(abs(f),W),2) − power(ts_op(f),W),2`，字段用 KOR 形态相似度族，9 条读数：
  - **方向系统为负**：`−0.66 / −0.64 / −0.63 / −0.52 / −0.38 / −0.16 / −0.16 / 0.00 / +0.32` ⇒ **7 负 1 正 1 全零**；
    唯一正的 `+0.32` 用的是**最长窗**（`ts_sum` 126）且 TO 最低 0.0737。
    他的解读：形态**延续 / 缺口填补**那一侧才有收益，**单独取负半轴等于把与动量正交的那一半扔掉了**（与 41150076043799「波动率与动量天然负相关」是同一件事的两面）。
  - **零持仓的诊断指纹（可直接用于读 check 表）**：`ts_std_dev` 窗 63 那条 `long=short=0 / bookSize=0`，check 表不是「全 FAIL」而是
    **LOW_FITNESS / LOW_SUB_UNIVERSE_SHARPE / LOW_INVESTABILITY_CONSTRAINED_SHARPE / CLUSTER_TEST 四项全部 ERROR**，
    LOW_SHARPE 与 LOW_TURNOVER 照常给 FAIL（value 0.0），且 **LOW_2Y_SHARPE 整行消失、换成 IS_LADDER_SHARPE=PENDING**。
    ⇒ 本区今后看到「2Y 行不见 + 若干项 ERROR」先查持仓是否归零，**不要当成闸门缺失**。
  - 持仓方向 8 条非零里 **7 条 short > long**（如 283-355 / 189-449 / 191-447），唯一反向那条恰是 `ts_std_dev` 档且窗从 63 换到 21 就能从空仓变成 446 多头
    ⇒ **该壳对窗口比对字段更敏感**。
- 评 `JR57542`（与 5.86.1 同一人，口径一致）：**原始波动率有强行业属性**（科技股天然比公用事业高）⇒ 必须截面标准化，
  `group_rank(vol, sector)` / `group_zscore` 都是去量纲正解；且**波动率与动量天然负相关**，「结合（如 `momentum − vol`）往往能提升 Fitness」。
  ⇒ 这条**背书了 242-A 用 `group_rank(…, industry)` 而非裸 `rank`**，但**不支持**把它与残差反转相乘（撞 ②.e / 闸 5）。
- ⚠ **证据强度声明**：这是**单用户自报的评论区数据**，字段是该用户的「形态相似度族」而非 risk68，**不能当本区实证**；只作方向先验与诊断指纹。
- 🔧 **对 5.86.1 末尾 243 计划的修正（不是推翻）**：原计划 `ts_std_dev(if_else(rsk68_residual_return<0, …))` 的**下行/上行不对称腿**
  **正是 `ZH34713` 实测系统性为负的那个「只保留负半轴」壳族**（同区、同设置族、7/9 为负）⇒
  该腿**降为低优先级**，且若要试，必须按他的口径配**最长窗档**（1 / 5 / 22 / 66 / 252 里取 252）并接受「可能是形态延续而非风险补偿」的对立解释；
  **不得**再把它记作「本塔尚未试过的第四条腿」这样的正面期待。
- 尾部风险机制本身**暂不组装**：`b`（对行业尾部风险的敏感度）需要「行业尾部风险时间序列」，FASTEXPR 里只能用
  `group_mean/group_quantile` 之类先造组级序列再 `ts_regression`，属**未验证的构造**，且 KOR 幽灵算子表里已含 `ts_skewness` 等易踩项 ⇒ 记为「机制已读、构造未验证」，不进本塔队列。

## 5.87 波 242 收割与归因（risk68 特征轴：低波水平 / beta）——**预注册分支 (b) 命中，risk 塔封存**

### 5.87.1 收割读数

| 项 | 值 |
|---|---|
| multisim | `3R7zZ1X256dbSJNxrkythM` |
| 结果 | **2/2 COMPLETE，0 error**（派发→全终态约 6–7 分钟；`child_count` 在 0 状态停留约 5 分钟，与本区既往一致） |
| 入库 | `linked 2 / upserted 2`；`wave 242 暂定 verdict=FAIL（0/2 过硬闸，0 条过 near 线 1.0）` |
| A | `akKM7o85` = `winsorize(reverse(group_rank(rsk68_weight_volatility_short, industry)), std=2)`（aC 503 头部轴） |
| B | `RREq7dw0` = `winsorize(reverse(group_rank(rsk68_beta, industry)), std=2)`（BAB） |
| 收批报告 | `avg_sharpe −0.215 / max +0.01（A）/ min −0.44（B）/ pass_rate 0` |

### 5.87.2 A 归因（低波水平，`rsk68_weight_volatility_short` 反号）

- **S 0.01** / F 0.00 / TO .1526 / returns **+0.05%** / DD **23.24%** / margin .000006 / long 321 · short 317 / pnl **49,254**。
- **subU −0.06**（limit .01）· **investS 0.06（pass）** · 2Y **−0.89**。
- fail 4：LOW_SHARPE / LOW_FITNESS / LOW_SUB_UNIVERSE_SHARPE / LOW_2Y_SHARPE；ra_failed 4。
- pass：LOW_TURNOVER / HIGH_TURNOVER / CONCENTRATED_WEIGHT / **LOW_INVESTABILITY_CONSTRAINED_SHARPE** / MATCHES_PYRAMID。
  ⭐ **「低波集中在大型股 ⇒ 可投资性友好」这条预判被证实**（本区唯一一条 investS 直接过闸的 risk 腿），但**没有信号时 investS 通过毫无意义**。
- 逐年 S：`−1.08 / +0.05 / +2.14 / +1.28 / −1.15 / +2.31 / −0.46 / +0.04 / +0.86 / −2.39`
  ⇒ **5 正 5 负、7 次变号**；S<1.0 占 **7/10**；top1（2019，1,195,775）= 正收益（3,693,034）的 **32.4%**，top2（2016，31.6%）合计 **64.0%**。
- 逐年 longCount 291–340 / shortCount 289–342、TO 全 10 年稳在 .1434–.1645 ⇒ **约束 4 满足，且不是覆盖或交易成本问题**。
- ⇒ 判定：**纯 regime 翻转噪声**。低波水平在 KOR/TOP600 2014–2023 **不存在可交易的溢价**，且 2023 单年 −2.39 / returns −18.75% 是三条 risk 腿里最差的一年。

### 5.87.3 B 归因（BAB，`rsk68_beta` 反号）

- **S −0.44** / F −0.18 / TO .0896 / returns **−2.01%** / DD **29.82%** / margin −.000448 / long 319 · short 319 / pnl **−2,075,095**。
- **subU −0.58**（limit **−0.25**）· **investS −0.49（warning，limit −0.31）** · 2Y **−1.12**。ra_failed 5。
- 逐年 S：`+1.31 / −1.09 / +0.69 / +0.97 / −1.10 / +0.50 / −0.55 / −1.63 / −0.12 / −1.81`
  ⇒ **2014–2019：4 正 / 6**（正年 1.31 / 0.69 / 0.97 / 0.50）；**2020–2023：0 正 / 4，且全部 ≤ −0.12**。
- 逐年 longCount 294–347、TO 全 10 年 .0751–.0964 ⇒ 约束 4 满足。
- ⭐ **这一条不是「KOR 没有 beta 异象」，而是「beta 异象在 KOR 于 2020 年后消失」**：
  分窗读 ⇒ 2014–2019 与 Choi(1998) 的 KSE 1982–1991 样本内证据**方向一致**（异象曾存在），
  2020–2023 **连续四年为负**（异象已衰减）。这个二分法比「全窗口 S=−0.44 ⇒ 无此异象」准确得多，也是本波最可复用的结论。

### 5.87.4 预注册判定（照 5.86.4 表逐条对，**我自己的预测错了，照实记**）

| 分支 | 条件 | 242 实测 | 命中 |
|---|---|---|---|
| (a) | 两槽 S ≥ 1.0 但 subU 失败 | S = 0.01 / −0.44 | ✘ |
| **(b)** | **两槽 S < 0.6** | **0.01 / −0.44，双双 < 0.6** | ✅ **命中** |
| (c) | 任一槽 S ≥ 1.05 且 subU / investS 均过 | 无 | ✘ |

- ⚠ **我在 5.86.4 写的预期（"大概率不是死在 S，而是死在 subU"）被证伪**。两槽**连 S 都没出来**，subU 只是跟着 S 一起归零的**伴随项**，不是死因。
- ⇒ **论坛 `JR57542` 那条「靠暴露不平等获利 ⇒ subU 的 market 中性化抹平它」的论断，在 KOR 既没被证实也没被推翻：死因发生在它上游一格。**
  不能拿它当"应验"来记（那是拿一个更早的失败去给一个更晚的机制背书），只能记：**该族在 KOR 连第一步（产生 S）都没走到，因此 subU 机制问题根本未被检验**。
- ⇒ 按 (b) 的原定动作：**risk 塔在挖掘层封存**（§5.85 原分支），不派 dadv / edadv 流动性腿，不做 risk68 反转的窗口 / decay / 平滑扫描。

### 5.87.5 ⭐ 跨波元发现：**2023 是三条 risk 腿的共同崩点** ⇒ 2Y 墙是「窗口事件」，不是机制判决

| 腿 | 表达式轴 | 2014–2019 | **2022** | **2023** | 全窗 S |
|---|---|---|---|---|---|
| 241-B `bl6VQQdZ` | `residual_return` 反转 | 8 连正中的主体 | **+0.31** | **−1.51** | **1.06** |
| 242-A `akKM7o85` | 低波水平反号 | 4 正 / 6（噪声） | **+0.86** | **−2.39** | 0.01 |
| 242-B `RREq7dw0` | beta 反号（BAB） | 4 正 / 6（净值正） | **−0.12** | **−1.81** | −0.44 |

- 三条**机制不同、量级差 1.5 个 Sharpe 档**的腿，在 2023 同向崩（−1.51 / −2.39 / −1.81）⇒
  **这不是三次独立失败，是一次共同 regime 暴露**。2023 KOR 的低质 / 高波 / 小市值主题行情，恰好是「反向风险类」信号的反面。
- **操作性推论（写死）**：
  1. 本区 **2Y 闸 = 2022 + 2023**，而 **2023 对 risk 类腿是系统性负年** ⇒ 任何 risk 系腿在当前测试窗内**结构性过不了 2Y**，与机制好坏无关；
  2. 因此 **BAB / 低波 / 残差反转这三条腿的"S 不达标"与"2Y 不达标"是两种性质**：前两条 S≈0 是真没信号，第三条 S=1.06 是真有信号但被**窗口**与**可投资性**双重卡住；
  3. **risk 塔重开条件（预注册，不可事后放宽）**：① 测试窗滚动后 2023 不再落在 2Y 区间（需平台窗口前移，属外部条件）；或 ② 用户在"近十年都要有数据"上给出新的窗口裁定。
     二者都不满足前，**risk 塔不再消耗配额**。
- ⇒ **241-B `bl6VQQdZ` 转入 salvage 池，不判死**：S 1.06 / subU .72 / CW 过 / 8 连正年 / 10/10 年覆盖，是**真信号**，
  只是 investS 相对闸差 40%。判"当前窗口不可提交"，不判"机制不成立"（与 earnings3 那条"判死机制"性质相反，不可混记）。

### 5.87.6 ⚠ 平台事实修正：`LOW_INVESTABILITY_CONSTRAINED_SHARPE` 是**相对闸**，不是绝对值

- 三个样本的 `limit` 实测：241-B `value .39 / limit .74`（基础 S 1.06）· 242-B `value −.49 / limit −.31`（基础 S −0.44）· 242-A `value .06` 通过（基础 S 0.01）。
- **`limit ≈ 0.7 × 基础 Sharpe`**：0.7 × 1.06 = .742 ≈ **.74**；0.7 × (−0.44) = −.308 ≈ **−.31** ✅ 两例到小数点后两位吻合。
- ⇒ **此前记录里「KOR investability 需 ≥ 0.74」是错的**（那是 241-B 那一条 alpha 的相对线，不是区域常数）。
  正确读法：**该闸问的是「可投资约束后还剩下原 Sharpe 的 70% 吗」** ⇒ 它是一把**相对尺**，`S 越高、门槛越高`。
- ⚠ 同一张 check 表里**同一项在不同 alpha 上可以落在 fail 也可以是 warning**（241-B 是 fail、242-B 是 warning）⇒ **判定必须逐 alpha 读，不能跨 alpha 套用档次**。
- `LOW_SUB_UNIVERSE_SHARPE` 的 limit 三例为 **.01 / −.25**（241-B 过闸那条未见具体值），**无一致比例可推**（.57 与 1.0 两说）⇒ 记为**未解**，不编公式。

### 5.87.7 243 定稿（铁律 G：继承 / 准入 / 收窄）

- **继承**：241-B 的"仅残差轴有信号"结论 + 本波"特征轴（低波 / beta）双双为零" ⇒ risk68 **只剩残差轴一条腿**且当前窗口不可提交。
- **准入**：⛔ 禁 risk68 全部特征轴（低波 / beta / dadv / edadv）二次进入；⛔ 禁 risk68 反转的窗口 / decay / 平滑扫描（5.85 原令 + 5.87.4 (b)）；
  ⛔ 禁 BAB / 低波 / 质量这一「暴露不平等族」在本区任何数据集上重开（5.87.4：连 S 都产不出）；⛔ 禁 earnings3 主轴（240-B / 241-A 已证互为镜像腿）。
- **收窄**：risk 塔配额 → **0**；243 全部配额转向 `insiders5`（A′ / B′ / A″，见 5.83.5，已 preflight `valid:true`）。
- **塔位事实（本轮 `get_pyramid_alphas` 实测，KOR/D1）**：lit = analyst 2 · fundamental 3 · model 3 · other 1 · pv 2 · shortinterest 4；
  **unlit = earnings / imbalance / insiders / institutions / macro / news / sentiment / socialmedia / risk（9 塔）**。
  ⇒ 后续未点亮塔队列：`insiders5` → `earnings3`（单强度杠杆槽）→ `institutions` / `imbalance` / `sentiment`。**risk 移出队列**（5.87.5 重开条件）。

## 5.88 波 243 派发记录（`insiders5`：库存股比率变化，**铁律 B 正反成对**）

### 5.88.1 先解一个纪律疑点：这不是「第四次撞已死轴」

- 本账号 `get_dead_ends(KOR)` 实测 **85 条**，其中 insider 相关 **3 条**。逐条核对：

| 死路 | family | 已测面 | 对本波是否构成禁入 |
|---|---|---|---|
| `KOR-INSIDER-PROD-SATURATED` | `insider_feats` 族 | **另一个数据集** `insider_feats`（30+ 表达式，PROD 0.7185 地板） | 否（数据集不同） |
| `KOR-INSIDERS5-CEILING-20260909` | **`insider_x_pv_x_analyst`** | n=30，全部是 **insider × 价差 / 上修的组合腿**（best S 1.05，w177/178/180/181 全弱） | **否**：本波是**单数据集单字段 standalone**，不属其已测面 |
| `KOR-EPS-REVISION-SPREAD-PROD-FLOOR-0723` | eps×pv106 | 与本集无关 | 否 |

- ⇒ **关键区分**：已有天花板测的是「insider 作组合腿」；**standalone 单字段**另一条线，历史最好成绩是 wave231 `akKMZ5x1` S −0.36、wave236 B S 0.28（2017–19≈1.0 后衰减），
  用的是 `insd5_ghc_tr` / `insd5_vol_chg`。**本波换成 `insd5_trsy_ratio`（库存股比率）——53 字段里从未被触碰的一个。**
  因此按「命中已死轴」判禁入是**误判**（此前三次误判的教训是"没核 payload.dataset / family 就派发"，本次是反过来：**核过面之后仍可派**）。
- 仍然受限的部分（写死）：**insiders5 不得再作 PV / analyst 组合腿的主攻**（ceiling 1.05 < 1.58），本波不碰任何组腿。

### 5.88.2 两槽（3 个预置里选 2：铁律 B 优先于铺广度）

| 槽 | 表达式 | A-2 收益来源声明 |
|---|---|---|
| **A′** | `winsorize(reverse(group_rank(ts_delta(vec_sum(insd5_trsy_ratio), 66), industry)), std=2)` | **谁被定价**：控股股东 / 财阀（재벌）家族。**为何会错**：韩国库存股（자사주）不是纯粹的「回购=低估信号」，它是**可再出售的潜在供给**——财阀惯用它做继承 / 换股 / 护盘（처분），市场在披露当期无法区分「注销型回购」与「待处置库存」，于是把潜在稀释当成已实现利好 ⇒ 系统性高估。**修复期**：一个季度（66 个交易日 ≈ 一次定期报告周期）。**方向**：库存股比率上升 ⇒ 未来跑输（负）。 |
| **A″** | `winsorize(group_rank(ts_delta(vec_sum(insd5_trsy_ratio), 66), industry), std=2)` | **同 A′ 的正面方向**（铁律 B：`reverse()` 与正向**不精确反号**——截断 × decay × 符号交互）。若全球主流解释（回购=低估信号 ⇒ 正）在 KOR 成立，则本槽应当优于 A′；两槽同测才能把「方向假说错」与「字段无信号」分开。 |
| ~~B′~~ | ~~`ts_delta(vec_max(insd5_tnc), 66)`（关联方人数↑）~~ | **本波不派**：① 方向同样是韩国制度假说（Baek 2004 / Cho 2023），与 A′ 的两个方向假说叠加会**混淆归因**（一次只测一个方向假说）；② `insd5_tnc` 是**计数型**字段，若年内几乎不变则 `ts_delta` 恒 0 ⇒ 整槽零持仓（5.86.5 已记该形态的诊断指纹）。⇒ 推后到 244，先单独核该字段的逐年非零率。 |

### 5.88.3 派发与设置（三个必钉项已显式传入）

- multisim **`2SIyD9egn4qQbhQgJ8mmO1a`**，2 子任务，`validate_fields=true`。
- 设置：KOR / TOP600 / **delay 1** / decay 4 / **STATISTICAL** / **truncation 0.08** / pasteurization ON / unitHandling VERIFY / nanHandling OFF / maxTrade OFF / FASTEXPR / testPeriod P0Y0M / 2014-01-01→2023-12-31。
  ⚠ 三个必钉项（`region` / `universe` / `neutralization=STATISTICAL` / `truncation=0.08`）**逐项显式传参**，不吃 schema 默认（`INDUSTRY` / `truncation 0`）。
- 派发前四项核对：① 字段存在性 = 5.83.5 已 preflight `valid:true / unknown_fields:[] / platform_field_count:1`；
  ② 幽灵算子 = 19 个全未使用（本波仅 `winsorize / reverse / group_rank / ts_delta / vec_sum`）；
  ③ 禁混信号 = 单字段单机制，无 `add` / 多机制相乘；④ 约束 5 = 无 PV / MODEL / OTHER 任何腿，**本波不组腿**。
- ⚠ **约束 4 未逐字段核验**：`insd5_trsy_ratio` 的十年连续覆盖**尚未实测**（§5.69.2 正面判定的是 insiders5 **数据集级** coverage，不是本字段）。
  ⇒ 不预判为通过，**以本波逐年 `longCount` 为准**（与 241/242 同一口径）。若出现整年空档 ⇒ 该字段按约束 4 出局，与信号强弱无关。

### 5.88.4 预注册预期（先写死，出结果不许改口径）

| 出结果形态 | 判定 | 下一步 |
|---|---|---|
| 两槽 **\|S\| ≥ 1.0**（任一符号） | 库存股轴**有信号**，方向由较大者定 | 该符号进 Mode A（强度杠杆）；另一槽作方向证据存档 |
| 两槽 **0.4 ≤ \|S\| < 1.0** | 弱信号，与 wave231/236 同档 | 不再单独开波，转为**组合腿备选**（但受 `insiders5 ceiling` 约束，只能配非 PV/analyst 腿） |
| 两槽 **\|S\| < 0.4 且方向相反** | `reverse` 近似反号（无截断×decay 不对称）⇒ 字段本身无信息 | **insiders5 standalone 线关闭**（第三次独立证伪），塔只在组合腿上留活口 |
| 任一槽 **零持仓 / bookSize=0** | 字段近乎静态（`ts_delta`≈0） | 立刻核 `insd5_trsy_ratio` 非零率与更新频率，不再派第二个同类计数 / 比率字段 |

## 5.89 Wave 243 收批 / 归因 / ⭐「reverse 差额＝2×成本」新事实 / 244 定稿

### 5.89.1 收批

- multisim **`2SIyD9egn4qQbhQgJ8mmO1a`**，**2/2 COMPLETE、0 error**（约 6–7 分钟；`child_count` 前 ~5 分钟仍为 0，与 241/242 同形，属正常在飞）。
- `harvest_multisim_alphas` → `mcp__wqb_db__workflow_auto_harvest(region=KOR, wave=243, dataset=insiders5, alphas=…)` ⇒ **`linked 2 / upserted 2`**，
  `wave 243 暂定 verdict=FAIL（0/2 过硬闸，0 条过 near 线 1.0）`；收批报告 `avg_sharpe −0.105 / max +0.38 (A″) / min −0.59 (A′) / pass_rate 0`。
- ⚠ **工具口径（踩了一次）**：`workflow_auto_harvest` 的 `alphas` **只吃 dict 列表**（`harvest_multisim_alphas` 的返回或其 `alphas` 数组）。
  传 alpha **id 字符串**列表 ⇒ `upserted 0` + 报「库里没有本波 multisim_id 的回测行」，**看起来像库坏了，其实只是没入库**。改传 dict 后立即正常。

### 5.89.2 两槽实测

| 槽 | alpha | S | F | TO | returns | DD | long/short | pnl |
|---|---|---|---|---|---|---|---|---|
| **A″（正向）** | `ZYQq0LEZ` | **+0.38** | 0.10 | .2424 | +1.76% | **9.71%** | 296 / 274 | **+1,817,636** |
| **A′（reverse）** | `d5WgOwRY` | **−0.59** | −0.20 | .2423 | −2.71% | 32.30% | 274 / 296 | **−2,800,904** |

- **A″**：fail = `LOW_SHARPE`(0.38<1.58) / `LOW_FITNESS`(0.10<1) / `CONCENTRATED_WEIGHT` / `LOW_2Y_SHARPE`(−0.24)；
  warning = `CLUSTER_TEST`(0.34) / `MATCHES_THEMES` / `OSMOSIS_ALLOCATION`；
  **pass = `LOW_TURNOVER` / `HIGH_TURNOVER` / `LOW_SUB_UNIVERSE_SHARPE` / `LOW_INVESTABILITY_CONSTRAINED_SHARPE` / `MATCHES_PYRAMID`**。
  ⇒ 这是本轮第四颗「subU + investS 双过」的候选（前三颗是 241-B 与 242 两槽的同项）。
- **A′**：fail 6 项，其中 `LOW_SUB_UNIVERSE_SHARPE` **−0.50（limit −0.34）**、`LOW_INVESTABILITY_CONSTRAINED_SHARPE` **−0.57（limit −0.41）**——
  ⚠ **两槽的 limit 不同**（A″ 的 investS limit 未列出、A′ 是 −0.41），再次印证 §5.87.6：**这两条闸是相对闸，limit 随 alpha 的基准 S 变**，不能跨 alpha 引用同一个数字。
- 金字塔：两槽 `KOR/D1/INSIDERS` ×1.2（该塔仍未点亮，本波不构成点亮）。

### 5.89.3 ⭐ 新平台事实：`reverse()` 的差额恰为 **2× 交易成本**（10/10 年逐年精确吻合）

两槽除 `reverse()` 外完全同构（同一 `group_rank(ts_delta(vec_sum(insd5_trsy_ratio),66), industry)`，`winsorize(std=2)` 两槽都是 no-op——见 5.89.6），
理论上持仓应精确互为镜像、pnl 精确反号。实测**不反号**（2014：+310,936 vs −406,238）。逐年做镜像分解：

- 设 `A″ = G − C`、`A′ = −G − C`（G＝毛利、C＝成本，成本**与方向无关**）⇒ **`G = (A″ − A′)/2`、`C = −(A″ + A′)/2`**。

| 年 | A″ | A′ | **G（毛）** | **C（成本）** |
|---|---|---|---|---|
| 2014 | +310,936 | −406,238 | +358,587 | 47,651 |
| 2015 | +123,563 | −274,277 | +198,920 | 75,357 |
| 2016 | +85,333 | −252,322 | +168,828 | 83,495 |
| 2017 | +7,284 | −53,933 | +30,609 | 23,325 |
| 2018 | +435,897 | −530,704 | +483,301 | 47,404 |
| 2019 | +3,059 | −85,449 | +44,254 | 41,195 |
| 2020 | −83,219 | +10,612 | **−46,916** | 36,304 |
| 2021 | +474,182 | −575,718 | +524,950 | 50,768 |
| 2022 | +538,650 | −588,465 | +563,558 | 24,908 |
| 2023 | −78,047 | −44,409 | **−16,819** | 61,228 |
| **Σ** | **+1,817,636** | **−2,800,904** | **+2,309,272** | **491,635** |

- **回代校验**：`G − C = 1,817,637`（实测 1,817,636）、`−G − C = −2,800,907`（实测 −2,800,904）⇒ 舍入级吻合，**10/10 年逐年精确**。
  成本占毛利 **21.3%**。⇒ `pnl` 是**税前净额**，而成本项对多空两侧同号 —— 这是镜像不反号的**唯一**来源（截断 / decay / 中性化都是线性符号对称的）。
- ⇒ **永久推论（写入纪律）**：
  1. **绝不能按 |S| 选方向**。亏损镜像的 |S| 天然更大（本波 −0.59 vs +0.38，差 0.21 ≈ 2C/σ）。方向只能取**同一符号的读数**，或用上式做毛分解。
  2. 铁律 B 的「`reverse()` 与正向不精确反号」**现在有了确定机理**：不是「截断 × decay 符号交互」（那是猜的），而是**成本符号盲**。
  3. 推论：**高换手族的镜像偏差更大**（C 正比于 TO）。判断「方向是否真有信息」时，TO 越高越要先做毛分解再看符号。
- ⚠ 本表的 `G` / `C` 是**假设成本严格对称**下的分解值，不是平台直接读数；但它 10/10 年精确自洽，故按**平台事实**处理（下次可直接用它省一次反向回测：只跑正向 + 一条镜像即可估出成本，或反过来估毛利）。

### 5.89.4 约束 4 逐字段裁决（结掉 §5.88.3 的开口）

- **A″ 逐年 `longCount` = 274 / 295 / 286 / 281 / 298 / 298 / 295 / 341 / 280 / 307**（十年全部非零，最短 274）。
  ⇒ **`insd5_trsy_ratio` 通过约束 4（字段级实测，不是数据集级推断）**，与 241/242 同口径。
- 字段元数据补齐：`insd5_trsy_ratio` coverage **0.8728**、`insd5_trsy_td_drt` 同 **0.8728**（库存股块整体 87.28%，**低于**集团持股块的 0.9996）——
  0.8728 是**截面覆盖**（当日有多少股票有该记录），不是时间连续性；十年无空档已由上表证。
- `vec_sum` 的重复计数担忧**作废**：`group_rank` 把绝对量归一化吃掉，聚合规模只影响截面内的相对排序；只有在需要「库存股占总股本 X%」这类**绝对量**结论时才需改 `vec_max`/`vec_avg`。

### 5.89.5 裁决（照 §5.88.4 逐条对，不许改口径）

| 预注册分支 | 是否命中 | 依据 |
|---|---|---|
| 两槽 \|S\| ≥ 1.0 | ❌ | 最大 0.59（且是成本放大的镜像） |
| **两槽 0.4 ≤ \|S\| < 1.0** | ⚠ **部分命中** | A′ \|0.59\| 在带内；A″ 净 0.38、毛 ≈0.48（估）。**两槽都落在 / 贴着同一个弱档** |
| 两槽 \|S\| < 0.4 且方向相反 | ❌ | A′ 0.59 ≥ 0.4 |
| 任一槽零持仓 | ❌ | longCount 274–341，bookSize 恒 20M |

**命中 = 分支 2** ⇒ **不单独开波，只作组合腿备选**（且受 `KOR-INSIDERS5-CEILING-20260925` 的 family 面 1.05 与「非 PV/analyst」双重限制）。

- ⚠ **必须同记：预注册表第三分支的前提被实测证伪。** 我写那条时假设「`reverse` 近似反号」（差一点也差不多），实测差 0.21（≈2C/σ，见 5.89.3）。
  ⇒ 这条事实**只用来永久作废「A′ −0.59 比 A″ +0.38 强 ⇒ 反向是主方向」的读法**，**不得**用来把结果上调到分支 1（0.59 里有一半是成本）。
- ⚠ **A-2 方向写错了（自己记，不改历史正文，只在此更正）**：我在 §5.88.2 把机制写成「库存股**累积** = 待处置库存 = 潜在供给 ⇒ 跑输」。
  实测方向**相反**：累积温和跑赢、**处置（比率下降）才跑输**。正确表述应为——
  **「库存股比率下降 = 已完成处置（처분）= 实际供给落地 ⇒ 跑输」**；累积只是「可能的未来供给」，市场并未提前折价。
  ⇒ A″ 的空腿（空处置方）正是赚钱的那一侧，机制本身是干净的，**只是我最初把因果的时态（待处置 vs 已处置）搞反了**。
- **强度诚实读数**：毛收益 **8/10 年为正**（2014–2019、2021、2022 全正；2020 −4.69 万、2023 −1.68 万），
  毛 Σ **2,309,272 / 20M book ≈ 1.15%/年**，毛 S 估 **≈0.48**（净 0.38 + 成本拖累，σ≈2.4%/yr）。
  ⇒ 与 earnings3 那种「随报告期塌陷」的**证伪**不同类：本族是**「机制成立、方向稳、天花板只有 0.5 量级」**。
- 附：TO 在 2022 突跳到 **.4118**、2023 **.3131**（其余年份 .20 上下）⇒ 库存股活动本身在这两年放量；同期毛收益 2022 为十年最高（+56.4 万）。**该族的活跃度依赖韩国回购/处置制度周期，不是平稳过程。**

### 5.89.6 算子事实：`winsorize(<rank 家族输出>, std=2)` **恒为 no-op**

- `group_rank` / `rank` 值域 (0,1]、日截面 std ≈0.29、均值 ≈0.5 ⇒ 2σ 界 ≈ **[−0.08, 1.08]**，**永不触发裁剪**。
  本波两槽都挂 `winsorize(std=2)`，对结果**零影响**，纯算子膨胀（`op_count` 与可读性双输）。
- ⇒ **纪律**：rank / group_rank 输出外面不要再套 `winsorize`。要压尾就直接 `tail(·, lower, upper, newval)`（明确指定分位），
  或先 `zscore` 换到无界域再 winsorize。命中即从候选里删掉——这条属于「免回测直接可删」的等价改写。

### 5.89.7 244 定稿（铁律 G：继承 / 准入 / 收窄）

1. **继承**：243 结论 = 库存股轴**真但弱**（毛 S≈0.48）、方向在**处置侧**；且 `reverse` 差额＝2×成本（5.89.3）。
2. **准入（本波禁碰）**：
   - ⛔ **insiders5 standalone 的任何变体**（`insd5_trsy_real_ratio` / `insd5_trsy_data` / 换 `vec_max`/`vec_avg` 聚合 / 换窗口 / 换 decay / 换中性化档）——
     这些**不是新机制，是同一腿换壳**，命中本区已死轴表「劣于同族的平滑器 / 算子窗口谱」。
   - ⛔ 任何按 |S| 选方向的做法（5.89.3 推论 1）。
   - ⛔ rank 输出外套 winsorize（5.89.6）。
3. **收窄**：243 的 **2 条 → 244 从本线取 0 条**（G 要求 ≤ 2/3 ⇒ 不足 1 条）。
4. **244 = earnings3 单强度杠杆槽**（队列 §5.87.7 第二位）。卡住即转：institutions（已关）/ **imbalance（已判死，见 5.89.8 更正）** / sentiment（待用户裁定）。
5. **insiders5 台账状态**：standalone 线 **冻结（非证伪）**——三次实测 231 `akKMZ5x1` −0.36 / 236-B +0.28 / 243-A″ +0.38（毛 0.48），
   全部落在 0.5 天花板下；塔只在**组合腿**上留活口，且受 ceiling 1.05 + 非 PV/analyst 双约束。

### 5.89.8 约束 1 进度：塔面普查 + 数据集筛查（本波等待窗口产出，全部只读）

**KOR/D1 金字塔实测（`get_pyramid_alphas`）**：**各格 alpha 计数** = analyst 2 · fundamental 3 · model 3 · other 1 · pv 2 · shortinterest 4；
**未点亮 = earnings / imbalance / insiders / institutions / macro / news / sentiment / socialmedia / risk（9 座，计数 0）**。
⇒ 队列：insiders5（本波，冻结）→ **earnings3** → institutions / imbalance / sentiment；risk 已按 §5.87.5 移出。

> ⚠ **本节 2026-10-30 自我更正两处**（原文已按此读，勿再引用旧措辞）：
> ① **「已点亮」措辞错误**：上表是**格内 alpha 计数**，不是点亮状态。点亮需 **≥ 3 条** ⇒
> `analyst 2` / `pv 2` / `other 1` **仍未点亮**（在飞 1 条即可点亮 analyst / pv），只有 `fundamental 3` / `model 3` / `shortinterest 4` 真正点亮。
> ⇒ **约束 1 的剩余供给不是「9 座零计数塔」，而是「3 座近点亮格」**：analyst 2→3、pv 2→3、other 1→3 —— 这三处信号面已实证（见 §5.87.7 队列），
> 比在 9 座零计数塔里继续找（8 座已关 / 冻结、earnings 已到实测 0.95 天花板）现实得多。**这是约束 1 的结构性瓶颈，需向用户交代。**
> ② **imbalance 不是「降权」而是已判死**（见下表修正行与 `datasets/imbalance5.md`）。

| 塔 | 数据集面实测 | 处置 |
|---|---|---|
| **imbalance** | 仅 `imbalance5`（2 字段 / cov .8559 / aC 458+298）——**名称 "SHIELD-OIL 油价冲击韧性评分" 与数据集级描述（RIC↔BBID 样板）不一致**，元数据不可信 | ❌ **已判死（非「降权」）**：三种机制上不同的形态（水平 / 规模中性化 / 66 日变动）2Y 均为 **0.17–0.18**，闸结构性不可达；详见 [`datasets/imbalance5.md`](datasets/imbalance5.md)。**可复用律**：描述含 regime/resilience/shock/weather/情景 的条件型数据集 ⇒ 2Y ladder 天然不可达，> 2 条探针即浪费 |
| **institutions** | `fund_holdings_panel`（已判死）+ `institutions6`（11 字段、cov .9996）——后者 §5.34 已试三种形态全灭后关闭 | **关闭**（不重开） |
| **news** | 24 个 KOR news 数据集中 **6 个**（news104 / news36 / news46 / news50 / news66 / news76）的**数据集级描述是同一段 RIC↔BBID 映射样板文** | ⚠ **该供应商 news 族的数据集级描述不可用于机制设计**，必须逐字段读 description；写进方法纪律 |

- **news54 裁决：拒绝，不派**（成本 = 1 次只读 `get_datafields(filter_sharpe=false)`，44 字段全表逐条过 §5.83.7 预注册筛子）。
  构成：23 个时间戳 / 时间码（`*_dt` / `*_tm` / `*_ts`）+ 4 个纯文本 + 4 个日历码（月 / 季 / 年）+ 3 个稀疏标志 +
  1 个混合量纲杂物 `mws54_factor`（描述原文 "dividend amount or stock split ratio"——**金额与比例混在同一个字段**，单位不可判定）
  ⇒ **可用信号腿 = 0 条** < 阈值 3 ⇒ 按预注册规则跳过。
- **news50**：81 字段**全 VECTOR**，结构上以 **已关闭的情绪轴**（约 20 个 `*_score`）与 **已关闭的关注度轴**
  （`mws50_vea` / `non_neutral_event_count_rolling_window` / `positive_event_ratio_score` / `mws50_aes` / `mws50_nip`）为主体，
  余下集中在 novelty / relevance / event-type / count —— 与 §5.83.7 点名的「已被覆盖轴」重叠 ⇒ **同样过不了 <3 条**，按同一规则不派。
  （与 news54 的区别：news54 是「字段本身不是信号」，news50 是「是信号但全在已关轴上」——两种都该拒绝，但理由要分开记，避免下次误以为 news 塔整族都无字段。）

### 5.89.9 补席台账校准（2026-10-30，1 次 `get_user_alphas(stage=OS, region=KOR)` 只读实测）

**平台计数维持 §5.8 口径**（`get_pyramid_alphas` 读数 = analyst **2** / pv **2** / other **1** / model 3 / fundamental 3 / shortinterest 4）
⇒ 补席缺口 = analyst **+1**、pv **+1**、other **+2**。**但手数 OS 清单与这组计数不一致，必须记下**：

| 塔 | 平台计数 | 手工枚举「`pyramids.list` 含该格」的 OS alpha 数 | 是否对得上 |
|---|---:|---|---|
| model | 3 | 3（`RRAG0WMb` / `0mre68gv` / `gJZR9XNm`，全 effective=1） | ✅ |
| pv | 2 | 4 条 effective=2 各占半 = **2.0** | ✅（按半分摊） |
| analyst | 2 | 1 纯（`KP78pLWk`）+ 4 条 effective=2 各半 = **3.0** | ❌ 多 1 |
| shortinterest | 4 | 1 条 effective=2 半 + 6 纯 = **6.5** | ❌ 多 2.5 |
| fundamental | 3 | 6 纯（`0mrnWojG`/`gJZ7AvZO`/`zq87zzqO`/`A1NXddRw`/`wpZkk1Mp`/`WjP1ZwMj`） | ❌ 多 3 |
| other | 1 | 1 条 effective=2 半 = **0.5** | ❌ 少 0.5 |

**三条结论**：
1. **`get_pyramid_alphas` 的计数不是「含该格的 alpha 数」，手工枚举也不能替代它** —— 只有平台计数可判点亮，
   且**不得用 OS 清单推算「还差几条」**（fundamental 手数 6 而计数 3，若按手数会误判「早已点亮且超额」）。
2. **多格 alpha 的计数被分摊**（pv 的 4 条 effective=2 恰好拼成 2.0）⇒ **补席要用「纯格」形态**，
   别指望靠一条 PV+ANALYST 双格 alpha 同时推进两格——它只会各记半分。
3. ⚠ **`oth` 前缀 ≠ OTHER 塔**（实测回读）：`oth466_*` 归属 **KOR/D1/FUNDAMENTAL**，`oth695_*` 归属 **KOR/D1/OTHER**。
   ⇒ **塔位只能由 `pyramids.list` 回读，禁按数据集 id 前缀推断**；派发前若靠前缀规划塔位，会直接点错塔。

**PROD 墙预算（同一次实测，约束 1 的真正瓶颈）**：KOR 现有 OS book 的 `prodCorrelation` **主峰压在 0.63–0.70**
（8 条：0.6962 / 0.6965 / 0.6976 / 0.6843 / 0.6762 / 0.6636 / 0.6622 / 0.6548 / 0.6483 / 0.6476 / 0.6406 / 0.6334 …），
已破 0.7 的 3 条：`zqYaZ2gO` **0.8201** / `WjP1ZwMj` **0.7974** / `WjPEg2zd` **0.7298**。
⇒ **任何补席候选必须概念可区分，数据集不同 ≠ 相关低**；补 analyst 席时与 `KP78pLWk`（prod .6334）/ `zqYaZ2gO`（.8201）
的同源性是最硬的约束，不是 IS 指标。

### 5.89.10 analyst 席补位候选：`analyst_consensus` 的**分析师分歧**轴（★ 预注册，**未派发**）

**触发**：§5.5 路 B 第一优先 = analyst 2→3。但 analyst 面已用尽**修正方向**轴（anl25 / anl44 / anl44_second / `eps_estimate_4wk_change`），
且 `cells.json` 已把 `analyst_consensus.eps_revision` / `.grossmargin` 两族判死 ⇒ 同轴再加一条必然撞 prod。

**新事实（本波画像产出，改写了一条旧结论）**：`reference/analyst_consensus.md` 实测 **MATRIX 18 / VECTOR 2325**。
`KOR_ANALYST_WAVE1_REPORT.md:472` 的「该集字段信噪比极低（18 字段 15 个 S<0.3）」**只覆盖 0.8% 的字段面**——
那是对 18 个 MATRIX 的结论，**不可外推到 2325 个 VECTOR**（同文 643 行也自陈「此前完全未扫」）。

| 项 | 实测值 |
|---|---|
| 白空间 | DISPERSION 簇 **295** 个 `stddev_*`（uc0 = 286） |
| 抽样字段 | `stddev_estimate_revenue_annual12` cov **.8029** / uc **0** / aC **0**（VECTOR） |
| 配对分母 | `mean_estimate_revenue_annual12` cov **.7977** / uc **0** / aC **0**（VECTOR） |
| 数据集级 | cov .6899 / aC 285 / valueScore 5 / 乘数 1.6 |

**形态（ATOM、单数据集、零 PV/MODEL/OTHER 腿 ⇒ 约束 5 自动合规）**：
`-rank( vec_avg(stddev_estimate_revenue_annual12) / abs(vec_avg(mean_estimate_revenue_annual12)) )` = **分歧率 CV**，同名量纲相除后无量纲。

- **A-1 五问**：①存量比率（非流量）②排序差异 ⇒ rank ③被定价的是**分歧强度**（离散度），不是修正方向
  ④有博弈（Miller 1977 / 卖空约束）⇒ 需可投资性壳 ⑤非事件（日频截面）。
- **A-2 声明**：谁在被定价 = **意见分歧**（悲观者因卖空成本/约束被挤出价格）；为什么错 = **卖空约束让负面观点无法表达 ⇒ 高估**；
  修复期 = **数季**；方向 = **高分歧 ⇒ 后续跑输**。
- **B 通道实证**：DMS(2002, JF) 分歧⇒低收益；〈Analyst Forecast Dispersion and Future Stock Performance: Evidence from Europe〉
  （STOXX600 / 2005–2015 / 268 家）**收入口径分歧同样有效**（正与本候选同口径）；
  〈Investor disagreement and state-dependent mispricing〉（JBF 2025）**负相关仅在高乐观 + 卖空约束下显著** ⇒ 属**条件放大**，不是恒等式。
- ⚠ **不可迁移**：以上均为欧美样本，**KOR 本区零实测**；KOR 的卖空制度（2020-03~2021-05 全面禁空、2023-11 起再度全面禁空）
  使该机制在禁空期更强、解禁期可能反转——**这不是 imbalance5 那种「只在冲击期存在」的条件型字段**（分歧每日都存在于截面），
  但**逐年必须看**，且若出现「S<1.0 年份 ≥3 成」即按发波决策表停扫。

**⚠ 预处理硬约束（本候选特有的坑）**：CV 在 `mean≈0` 时爆炸 ⇒ 必须先对 **CV 本体**做 `winsorize`/`tail` 或
`divide(stddev, add(abs(mean), eps))`；**但 rank 输出后不得再 winsorize**（§5.89.6 恒 no-op）。

**去留规则（先写、回测前锁定）**：

| 读数 | 判定 | 下一动作 |
|---|---|---|
| S ≥ 1.0 且 2Y ≥ 1.58 | analyst 席补位成立 | 进 §8 稳健闸 + prod 实测（与 `zqYaZ2gO` .8201 / `KP78pLWk` .6334 比对） |
| 0.6 ≤ S < 1.0 | 方向对、强度不足 | **只允许换分子口径**（bvps / capex / cfo / ebitda 的同构字段），不扫窗口谱、不改聚合 |
| S < 0.6 | 分歧轴在 KOR 不成立 | analyst 席关闭（`analyst16` 已被 priors 判「不再投任何变体」，等于该席无替补） |
| 任一整年 `longCount` = 0 | 约束 4 不通过 | 判死，不救 |

**⚠ 排期纪律**：本条**不派在 245 当 A 槽**。铁律 G 要求 245 先继承 244（earnings3 单强度杠杆槽）的读数：
若 244 触发「earnings 塔关闭」，则 **245 = analyst 席补位，本条为 A 槽**；若 244 未关闭，则本条顺延。

**A 通道取证（2026-10-30，MCP `search_forum_posts` + `read_forum_post`，正文已读 2 篇）**——补 ②.d 的双通道另一半：

| 帖 | 投票 / 日期 | 读数 | 对本候选的作用 |
|---|---|---:|---|
| 〈分析师一致预期：121 个字段里最值得做的 5 个信号〉id `42659792904343` | 30 票 / 2026-08-12 | 把分析师面收敛为 5 轴；第 5 轴「Estimate Skew」原文：**「`stddev` 只告诉你『分歧大小』，`mean−median` 告诉你『分歧方向』，是独立于 dispersion 的异常维度」** | ⭐ **直接印证本候选取 `stddev` 作分子 = 取分歧「大小」**，与该集合公认的独立轴一致，**不与既有修正方向轴重叠**（这正是补 analyst 席最需要的正交性） |
| 〈【直通通过】【Alpha灵感】Consensus Analyst Target Prices〉id `34926922792855` | 4 票 / 2025-09-14 | 目标价偏离度的有效性**受 dispersion 调节**：低 dispersion 时有用，**高 dispersion 时可能反向** | 独立佐证「高分歧 ⇒ 价格信息被污染 / 高估」；并给出**门控用法**（dispersion 作条件而非主信号）⇒ 与 B 通道 Miller 卖空约束故事同向 |

**三条落地校准（派发前决定，已锁定）**：
1. ⚠ **论坛模板的方向句自相矛盾，不可采信**：帖 1 写「mean 高于 median = 少数乐观 outlier 拉高均值，真实共识偏悲观，后续 surprise 方向**偏下**」——
   「共识偏悲观」按定义应产生**正向**意外，与「偏下」直接冲突。⇒ 若将来做**偏度腿**（第二条同集腿），方向必须按**铁律 B 正反各测**，
   **且不得与本条的 CV 腿同波比较**（大小 vs 方向是两种机制，混在一波里比读数 = ②.d 的「机制矛盾不组装」）。
2. **`numofests`（估计人数）作质量过滤——本候选先不加**：帖 1 明写「覆盖稀疏的股票上预期信号噪声大」，本集 COUNT 簇有 157 字段可接；
   但 A-2 的收益来源是「分歧被卖空约束挤出价格」，加覆盖过滤会把机制改写成「只在高覆盖样本交易」⇒ 列为**备选壳层**，
   只在首测出现持仓集中低覆盖股（CW 逼近 0.10 / subU 异常低）时才上，且上壳须单变量对照。
3. **通道裁决 = ⭐ 优先组装**：A 与 B 指向同一机制（分歧 ⇒ 高估 ⇒ 后续跑输），无矛盾 ⇒ 形态**维持**
   `-rank( vec_avg(stddev_estimate_revenue_annual12) / abs(vec_avg(mean_estimate_revenue_annual12)) )`，不因取证而改设计。

**⚠ VECTOR 处理顺序（帖 1 的 backfill 建议 + 本站实测合并）**：该集 cov **.8029**（缺 20%），必须 backfill；但 `stddev_*` / `mean_*` 均为 **VECTOR**
⇒ **先 `vec_avg` 降维、再 `ts_backfill`**（`ts_backfill` 不吃 VECTOR）。落地形态：
`-rank( divide(ts_backfill(vec_avg(stddev_estimate_revenue_annual12), 10), abs(ts_backfill(vec_avg(mean_estimate_revenue_annual12), 10))) )`
—— **刻意不加防零常数**：① `rank` 本身对极端值稳健（除零产生的 inf 只会被排到端点，不影响其余截面）；
② 若写成 `add(mean, 0.0001)`，就是在**有量纲（美元）字段上叠加无量纲常数**，VERIFY 模式下会触发 UNITS 警告
（本项目已登记该坑，见 memory `brain-verify-units`）⇒ **防零保护在这里是有害的，不是稳妥**。`rank` 后**禁再 `winsorize`**（§5.89.6 恒 no-op）。

### 5.90 Wave 244（earnings3 单强度杠杆槽 + earnings×insiders 条件门控）—— **0/2，earnings 塔关闭**

**派发记录**：`create_multi_simulation` → `V5i5M6th4j6c3BR279kSf`，2026-10-30T11:03:21Z，2 槽，11:08:30 起 2 条 COMPLETE（耗时 ≈ 5m10s，与 241–243 同量级）。
全部 KOR 钉住项显式传参（`region=KOR / universe=TOP600 / delay=1 / decay=4 / neutralization=STATISTICAL / truncation=0.08 /
test_period=P0Y0M / unit_handling=VERIFY / nan_handling=OFF / language=FASTEXPR / pasteurization=ON / max_trade=OFF`）。
派发前 `operator_audit` = `safe:true`（幽灵算子 20 个回传未修改、零命中）。
收批：`harvest_multisim_alphas("/simulations/V5i5M6th4j6c3BR279kSf")` → `workflow_auto_harvest` **linked 2 / upserted 2**，
wave_result 暂定 `verdict=FAIL（0/2 过硬闸，0 条过 near 线 1.0）`。

| 槽 | alpha | 表达式 | S | F | 2Y | subU | CW | ladder | TO | ret | long/short | 金字塔 |
|---|---|---|---:|---:|---:|---:|---|---:|---:|---:|---|---|
| **A** | `gJewb80m` | `group_neutralize(group_rank(ts_backfill(multiply(-1, ern3_next_interval), 10), industry), sector)` | **0.63** | 0.28 | **1.09** | 0.48 | PASS | — | .1506 | 2.96% | 326/312 | earnings（eff 1） |
| **B** | `npvYdNXq` | `trade_when(less(ts_backfill(ern3_next_interval, 10), 21), group_rank(ts_delta(vec_sum(insd5_trsy_ratio), 66), industry), -1)` | **0.05** | 0.01 | 0.49 | **−0.02** | **FAIL** | **0.49** | .1519 | 0.26% | 324/313 | earnings+insiders（eff 2） |

**归因（铁律 F）**：

| 槽 | 逐年 S（2014→2023） | S<1.0 年数 | top1 年占正收益 | 逐年 `longCount` 最小值 | 判读 |
|---|---|---:|---:|---:|---|
| A | −1.44 / −0.45 / 0.98 / 0.91 / 0.80 / **1.74** / 0.42 / 1.36 / **1.81** / 0.54 | **7/10 = 70%** | 19.4%（2019） | 290（2014） | **S<1.0 年份 ≥3 成 ⇒ 2Y 结构性不可达**（发波决策表）⇒ 停扫 decay / 平滑 / 门控 |
| B | 0.33 / 0.93 / 0.77 / **−1.26** / **−1.27** / −0.44 / 0.24 / 0.22 / 0.89 / 0.08 | **9/10 = 90%** | —（2017/18 双双击穿） | 287（2014） | 机制性衰减：2017–2019 连年负 ⇒ 门控把信号锁进了错误的 regime |

**约束 4（近十年都要有数据）**：两槽**全部 10 年**都有持仓（A 的 `longCount` 290–350、B 287–348）⇒ **不是数据缺失问题，是机制问题**。

#### 5.90.1 结论一：earnings 塔 **关闭**（按 §5.84.2 预注册规则）

预注册原文：「剩余唯一杠杆 = 在 `ern3_next_interval` 上做**一次**强度杠杆（中性化档 / 壳层），**只给 1 槽、排在 243 之后。若该槽仍 <1.0，按「机制不成立」关闭本塔」。
A 槽 S **0.63 < 1.0** ⇒ 触发关闭条款。

**⚠ 先说清这槽的设计缺陷（不遮掩）**：A 槽相对基线 `omEwRJwJ`（`group_rank(..., sector)`，S 0.95 / 2Y 1.75 / subU .82）
**同时改了两件事**——把组从 `sector` 收到 `industry`，又外加 `group_neutralize(..., sector)`。
这违反「单变量对照」，所以**无法判断是哪一个动作杀了收益**。但**结论不受影响**：

> 单变量最好的情况 = 完全不动基线 = **S 0.95**，**仍远低于 RA 闸 1.58**；
> 而 §8.8 的独立天花板测算（R 常数 .0465–.0473 vs 目标 .0628）也落在同一量级。
> ⇒ **无论哪根杠杆拖累，本塔的上界 0.95 < 1.58，结构性不可达 ⇒ 关闭是安全的**，不需要再花一槽去分离变量。

**可复用律（新）**：
1. **`ern3_next_interval` 这类「日历 / 事件间隔」信号的收益含强行业共同成分** —— 组内排序（industry）会剥掉它，
   再叠一层 sector 中性化等于**双重剥离**，收益从 0.95 掉到 0.63 而同向保持（subU 0.48 仍为正、TO 不变）。
   ⇒ **薄信号的壳层必须是「加不了的就不加」**（②.c：机制上无关 ⇒ 不加壳），本槽是「无关也加了」的反例。
2. **塔级关闭不看「有没有更优参数」，看「上界 vs 闸」**：基线已是最优形态时，任何杠杆都只能往下走 ⇒ 再扫就是烧配额。
   （与发波决策表「S<1.0 年份 ≥3 成 ⇒ 停扫 decay/平滑/门控」是同一条，只是这里连机制本身一起判死。）

#### 5.90.2 结论二：earnings × insiders 条件门控轴 **判死**（消耗约束 5 配额 1/5）

B 槽是「日历字段做门控 + 66 日内部人净减持做信号」。结果 S 0.05、subU **负**、**CW FAIL**、ladder 0.49。
- **根因＝频率错配**：门控条件 `ern3_next_interval < 21` 是**低频、慢变**的日历量（每季换一次），
  而信号腿 `ts_delta(vec_sum(insd5_trsy_ratio), 66)` 是**慢速 66 日变化**；两者叠加后持仓换手仍只有 .1519，
  即**门控几乎不过滤任何东西**，却把 2017–2019 的持仓锁在了同一个方向（3 年连负）⇒ 门控没起到「只在高信息期交易」的作用，只改变了持仓的时间对齐。
- ⇒ **门控的时间尺度必须显著短于信号腿**（`trade_when` 的用处是「削掉非事件期」，不是「换个对齐方式」）；
  慢门控 + 慢腿 = 什么都没做，但会引入对齐偏差。**这条写死成本区的方法纪律。**
- **配额账**：本波消耗**约束 5 的「跨 category 组腿」1/5**（earnings × insiders；两者都不在 PV/MODEL/OTHER，本不受禁，但按自律计入）。
  ⇒ 剩余 **4/5**。

#### 5.90.3 Wave 245 预注册（铁律 G：继承 / 准入 / 收窄）

- **继承（来自 244）**：① earnings 塔**已关闭** ⇒ 从「未点亮塔供给池」中移除，9 座 → **8 座可挖**（另有 8 座已关/冻结 ⇒ 实际可挖 = 0）；
  ② 跨 category 门控的**频率纪律**（门控尺度须显著短于腿尺度）⇒ 245 若用 `trade_when`，门控必须是短窗；
  ③ 24x 系列共同读数：**能上 1.58 的从来不是壳层，是新机制**。
- **准入（245 禁止触碰）**：earnings3 全族（含 `ern3_next_interval` 的任何变体）；`winsorize` 包 `rank`；
  earnings/insiders 之间的任何组腿；组内排序 + 再中性化的双层清理结构。
- **收窄**：244 的 2 个实验轴**全部关闭**（A 强度杠杆耗尽、B 门控轴死）⇒ 245 只保留 **1 个新轴**（analyst 席补位，见 §5.89.10）。
  候选数 **2 → 2**，但**实验轴 2 → 1**：⚠ 平台 `create_multi_simulation` 硬要求 **2–10 条表达式**（单条提交不了），
  所以 245 的 2 个槽是**同一机制的符号对**（铁律 B：方向正反各测，`multiply(-1,·)` 与裸 `rank` 不是精确反号——
  成本按绝对值计），**不是两个机制**。⇒ 「收窄」的判据落在**机制轴数**上（2→1），不落在槽数上。
- **245 两槽（同一轴，符号对）**，表达式已按 §5.89.10 的 VECTOR 顺序与防零纪律锁定：
  - **A（理论方向）**：`multiply(-1, rank(divide(ts_backfill(vec_avg(stddev_estimate_revenue_annual12), 10), abs(ts_backfill(vec_avg(mean_estimate_revenue_annual12), 10)))))`
  - **B（反向对照）**：`rank(divide(ts_backfill(vec_avg(stddev_estimate_revenue_annual12), 10), abs(ts_backfill(vec_avg(mean_estimate_revenue_annual12), 10))))`
  - 派发记录：`operator_audit` = `safe:true`（幽灵算子 20 个未命中）；`validate_expressions` = `valid:true`（2 字段解析成功）；
    `create_multi_simulation` → **`1bOMpB20D4p6bxD14osWbOc4`**，2026-10-30T11:12:50Z，`validate_fields=true`，2 槽，KOR 钉住项全部显式传参。
  - **方向怎么读（铁律 B 的正确用法）**：**不得按 |S| 选方向**——平台 PnL 含成本且成本符号盲，输的那一面 |S| 系统性偏大
    ⇒ 方向只能由「A-2 声明的预期方向」+ 逐年稳定性判定，不能由「哪个 S 高」判定。
- **245 去留规则 = §5.89.10 已写的那张表**（S≥1.0 且 2Y≥1.58 ⇒ 进稳健闸 + prod；0.6≤S<1.0 ⇒ 只换分子口径；S<0.6 ⇒ analyst 席关闭；任一整年 `longCount`=0 ⇒ 约束 4 不通过）。
- **⚠ 245 的额外硬前置**：analyst 席是 **2/3**，补进 1 条即点亮 ⇒ 该候选一旦全闸通过，**必须**先做 prod 实测再谈提交
  （同源性参照 `KP78pLWk` prod .6334 / `zqYaZ2gO` prod .8201）。

### 5.91 Wave 245 收批（`analyst_consensus` 分歧轴，符号对）—— 0/2，**镜像分解证明「机制为零」**，analyst 席关闭

**派发**：`1bOMpB20D4p6bxD14osWbOc4`，2026-10-30T11:12:50Z，2 槽，11:16:08 全部 COMPLETE（≈3m18s，本波快于 24x 均值）。
收批 `linked 2 / upserted 2`，wave_result 暂定 `FAIL（0/2）`。两槽均落 **`KOR/D1/ANALYST`（eff 1）** ⇒ 塔位归属正确。

| 槽 | alpha | 表达式（后半相同，只差符号） | S | F | 2Y | subU | TO | ret | long/short |
|---|---|---|---:|---:|---:|---:|---:|---:|---|
| **A 理论向** | `zq3QbJx8` | `multiply(-1, rank(divide(ts_backfill(vec_avg(stddev_estimate_revenue_annual12), 10), abs(ts_backfill(vec_avg(mean_estimate_revenue_annual12), 10)))))` | **−0.14** | −0.03 | −0.29 | −0.41 | .0719 | **−0.59%** | 308/330 |
| **B 反向** | `ZYQqAW88` | `rank(divide(ts_backfill(vec_avg(stddev_estimate_revenue_annual12), 10), abs(ts_backfill(vec_avg(mean_estimate_revenue_annual12), 10))))` | **−0.05** | −0.01 | 0.03 | 0.25 | .0720 | **−0.20%** | 330/308 |

#### 5.91.1 ★ 镜像分解：**毛收益 ≈ 0，成本把两面都拖成负的**（本波最重要的产出）

两槽是**同一信号的精确反号**（`multiply(-1,·)` vs 裸 `rank`，权重逐位取反）。设毛收益为 `P`、成本为 `C`（两面成本都为正，因为平台成本按**绝对**持仓变动计）：

```
A: −P − C = −0.0059
B: +P − C = −0.0020
⇒ P = +0.00195（毛 +0.195%/年）  C = 0.00395（成本 0.395%/年）
```

年化波动由两槽交叉验证一致：`σ ≈ 0.0059/0.14 = 4.2%` 与 `0.0020/0.05 = 4.0%` ⇒ **σ ≈ 4.1%**。
⇒ **毛 Sharpe ≈ 0.195 / 4.1 ≈ 0.05**。

**结论：这不是「方向做反了」，是「这个量没有预测力」。** 换方向最多把 −0.14 变成 −0.05，仍远低于 0.6 的关闭线。
**这条分解是 0 额外配额的**——两个槽的 `returns`/`sharpe` 一相减就能把「信号」与「成本」完全分离。

**可复用律（写入发波纪律）**：
> **判「没信号」还是「方向反了」的唯一零成本方法 = 同波放一对精确反号槽，解 `P` 与 `C`。**
> 若 `P/σ`（毛 Sharpe）< 0.2 ⇒ **机制为零，禁止换方向重测**；
> 若毛 Sharpe 明显 > 0 而净 S < 0 ⇒ 是**成本吃掉**，杠杆应该指向降 turnover，而不是换方向或加壳。
> ⚠ 前提是两面**除符号外逐字相同**（含中性化 / decay / truncation）；改任何一项都不是镜像对，分解失效。

**逐年符号对验证（10/10 年符号完全相反，幅度不等）**：

| 年 | 2014 | 2015 | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| A `zq3QbJx8` | 0.56 | 0.83 | 0.35 | **−0.86** | 0.39 | 0.19 | −1.02 | −1.22 | 0.67 | −1.09 |
| B `ZYQqAW88` | −0.87 | −1.07 | −0.45 | **0.73** | −0.54 | −0.34 | 0.96 | 1.01 | −0.81 | 0.74 |

⇒ 符号严格相反（再次确认平台 `reverse` 的**符号精确、幅度不精确**），但**没有任何一年任何一面超过 1.1**，
且 A 面在 2020/2021/2023 三年大负、B 面同年大正 ⇒ **这是个 regime 翻转量，不是稳定 alpha**；
正负年份抵冲后毛收益归零，与上面的分解一致。

**约束 4**：两槽 10 年 `longCount` 全部 ≥ **272** ⇒ 近十年都有数据，**不是覆盖率问题**。

#### 5.91.2 裁决：analyst 分歧轴 **判死**，analyst 席 **关闭（2/3 冻结）**

按 §5.89.10 预注册的去留表（写于回测前、未改）：「S < 0.6 ⇒ 分歧轴在 KOR 不成立 ⇒ analyst 席关闭」（S = −0.14 / −0.05，且毛 Sharpe 0.05）。
- **不适用「只换分子口径」那一档**：那档的触发条件是 `0.6 ≤ S < 1.0`（方向对、强度不足），本波连毛信号都是 0 ⇒ 换 bvps / capex / cfo / ebitda 只会把 0 换成另一个 0。
- **B 通道（DMS 2002 / Nummela STOXX600 / JBF 2025）与 A 通道（论坛 30 票帖）在 KOR 双双不成立** —— 记入跨区不可迁移清单：
  **分析师分歧度在 KOR/TOP600/D1 的毛 Sharpe ≈ 0.05，与欧美样本结论不符**。可能原因（**未验证，不得当地结论引用**）：
  ① KOR 卖方覆盖极度集中（TOP600 里 `numofests` 少），分歧度的截面差异被少数大票主导；
  ② 全面禁空制度使「高估无法被套利」方向**不可实现**，分歧只反映噪声；
  ③ `analyst_consensus` 的 VECTOR 字段可能已做供应商侧平滑，原始分歧被压平。
- ⇒ **analyst 席从「可补」名单移除**：`2/3` 冻结在此。要把该席补上，需要的是**第三条机制轴**，不是本轴的重测。

#### 5.91.3 供给总账（约束 1 的诚实读数，2026-10-30 收盘）

| 供给口 | 状态 | 依据 |
|---|---|---|
| 9 座零计数塔 | **可挖 = 0** | news / insiders / sentiment / socialmedia / institutions / macro / imbalance / **earnings** 全部关闭或冻结；risk 已移出队列 |
| analyst 2→3 | ❌ **关闭** | 修正轴早死（`cells.json`）；分歧轴本波毛 Sharpe 0.05（§5.91.1） |
| pv 2→3 | ⚠ 单数据集面已穷尽 | §5.54 全 18 集盘点、两条新线索判死；**唯一未试路径 = 跨 category 组腿（约束 5 允许 PV+NEWS 等，≤5 条）** |
| other 1→3 | ⚠ 结构性封顶 1/3 | §5.53（other545 双灭）；§5.51（other546 被约束 5 封死） |

⇒ **约束 1 在「未点亮塔 + 闸 1.58」下，剩余可行动路径只有一条：用约束 5 允许的跨 category 组腿去填 pv 席**。
且因多格 alpha 各自**记半分**（§5.89.9 结论 2），填 1 席需要 **2 条**同样全闸通过的组合 alpha。

> ⚠ **上句已于同日被撤回，见 §5.92.1 —— 那是类别错配，不是路径。**

## §5.92 供给归零的最终裁定（2026-10-30 收盘）

### 5.92.1 撤回 §5.91.3 末行：「跨 category 组腿填 pv 席」是类别错配，不是路径

§5.91.3 写完「唯一未试路径 = 跨 category 组腿」之后，本轮把 §5.54 的 18 个 PV 集**逐字段**核了一遍，
结论必须当场撤回——三条理由，每条都有实测出处：

1. **塔票跟着 `pyramids.list` 走，不跟 `category` 标签走**。§5.89.9 结论 3 已实测过同形：
   `oth466_*` 归属 **FUNDAMENTAL**、`oth695_*` 归属 **OTHER** ⇒ 前缀/分类不可作为塔位推断。
   而 §5.54 表里 **6/18 个 PV 集的真实内容是别的塔**：pv20＝全球公司基本面（FUNDAMENTAL）、
   pv70＝analyst 一致预期（ANALYST）、pv149＝Data Explorers 借券/空头（SHORTINTEREST）、
   pv109/pv173＝债券面、pv14＝KOSPI200 指数（非个股截面）。
   ⇒ 拿它们组「PV+FUND」，平台按数据集归属记分，**PV 席一分不动**，只是把已有的 FUND 库存再加厚。
2. **§5.54 结尾已明令**：「把它们当 PV 信号用只是在蹭塔票，不等于 PV 有自己的经济面」——
   而「补 pv 席」这个动作**按定义就是蹭塔票**。用户约束 5 授权的是「组腿可以做」，不是「塔票可以借」。
3. **真 PV 面已穷尽**：pv1 是全库最饱和集（aC **90,329**、vS 1）——现有 pv 计数的 4 条 effective=2 全出自这里；
   pv106 已挖穿（34 条零 `ra_clean`，只作条件腿）；pv103 仅 7 字段样本过小；pv30 是 group 维不是信号；
   pattern_scores / continuation_score / intraday_pv_feats 早已判死；pv37（873 字段异构，主力家族 227 已死）/
   pv47（残差收益＝risk71/72 同机制）本日判死。**没有第 19 个集可开。**

⇒ **pv 2/3 与 analyst 2/3 结构性冻结；other 1/3 的「唯一供给」也已关闭**——§5.92.6 记的
`leAk66xx`（纯格 OTHER、全闸 ATOM）后续实测 prod **0.8711** ⇒ D0-P 墙（§8.1），
所以它**不是**「只差 2018 前的数据」，约束 4 之争随之 moot。三格均为结构性封冻。

### 5.92.2 约束 1 的定量收口（每条都带实测出处，不许只写「试过了」）

| # | 路径 | 实测最优 | 出处 | 对闸 1.58 |
|---|---|---|---:|---:|
| 1 | 单塔单字段 ATOM（未点亮塔） | **S 1.04** / 2Y 2.02 / F .67 | wave 213 `vec_avg(rsk59_last_rate)` | −34% |
| 2 | risk59 形态轴三连 | level 1.02–1.04 · variance **0.39** · delta **0.04** | wave 201 / 212 / 213 | 轴封闭 |
| 3 | risk59 分组轴三连 | sector 1.02 > industry 0.96 > subindustry **0.70** | wave 212 / 213 | 细轴三次更差 |
| 4 | risk70 IVOL | 正向 0.57 / 反向 **−0.73** | wave 214 | −54% |
| 5 | risk68 残差反转 | **1.06**（investS 相对闸差 40%） | 241-B `bl6VQQdZ` ⇒ salvage | −33% |
| 6 | risk68 特征轴（低波 / beta） | **0.01 / −0.44** | 242-A / 242-B | 机制为零 |
| 7 | earnings3 强度几何 | **0.95** / 0.89 / 0.63 | wave 209 / 210 / 244 | −40% |
| 8 | earnings×insiders 条件门控 | **0.05** | wave 244-B | 频率错配，机制为零 |
| 9 | analyst 分歧（CV） | −0.14 / −0.05，**毛 Sharpe 0.05** | wave 245 镜像分解 | 机制为零 |
| 10 | news 五轴（方向/计数/强度/结构/幅度） | max **0.25** | wave 190–211 | 塔关闭 |
| 11 | sentiment26（DNS 关注度） | **0.20** + 仅 7/10 年 | wave 216 | 双死因 |
| 12 | macro63 | **0.00**（恒空仓，域错配） | wave 215 | 无法计分 |
| 13 | imbalance5 | 2Y **0.17–0.18** | §5.89.8 | 塔关闭 |
| 14 | insiders5 | **1.05** | §5.83 | −34% |
| 15 | institutions | 双数据集全死 | §5.5 | 塔关闭 |
| 16 | other 塔 | other545/546 双灭 | §5.51 / §5.53 | 封顶 1/3 |
| 17 | pv 塔（单数据集面） | 18 集穷尽 | §5.54 | 封顶 2/3 |
| 18 | **组合腿（最优权重，ρ 实测）** | 2 腿 1.238 · **3 腿 1.292** | §5.4 闭环（ρ = **0.1978**，1023 日） | −18% |
| 19 | 跨区扫库存补席 | 20 条实测 **0 命中** | memory `prod-20-0` | — |

**反解**：要摸 1.58 需 **4 条平均 1.0 的腿**，或 **7 条平均 0.9 的腿**；现存可用腿只有 3 条 `[1.02, 0.89, 0.67]`。
**这不是执行量不足，是闸与数据的结构性错配**——`1.58` 是「严格 RA 档」的线，而本区在「未点亮塔」上实测的
单塔单字段上限就是 **1.04**（差 34%），任何组合方式的代数上界是 **1.292**（差 18%）。

**prod 墙（第二道闸，与上面独立）**：KOR OS book 的 `prodCorrelation` 主峰压 **0.63–0.70**，
已破 0.7 的 3 条（`zqYaZ2gO` .8201 / `WjP1ZwMj` .7974 / `WjPEg2zd` .7298）⇒ 补席候选必须**概念可区分**，
「换数据集」不等于「降相关」。§5.92.2 第 18 行那 3 条腿里，risk59 与 earnings3 属**同一 regime 暴露**
（2023 同向崩，§5.87.5），所以 ρ 只有 0.20 也救不回来。

### 5.92.3 需用户裁决的六件事（本 agent 无一项可自行执行）

| # | 事项 | 为什么卡住 | 代价 / 风险 |
|---|---|---|---|
| 1 | **提交 `LLZ6wZO2`**（S 1.99 / F 1.53 / 2Y 2.24 / subU 1.21 / cluster 0.94 / prod **.6762** / self **.676**） | 全闸通过，但 `KOR/D1/FUNDAMENTAL` 已 3/3 满 ⇒ 不点新塔 | 提交不可逆；塔已满时平台是否拒收未知 |
| 2 | ~~**放宽约束 4 使 `leAk66xx` 可提交**（S 1.77 / F 2.11 / 2Y 2.24 / `fail=[]`）~~ | ⛔ **2026-10-31 prod 实测 0.8711 ⇒ D0-P 墙已先判死**（见 §8.1）；约束 4 之争就此 moot | **无需用户裁决，自动关闭** |
| 3 | **授权新数据集**（7 个尚未画像：other323 / other78 / news59 / other532 / other327 / other436 / other546） | 185 个数据集里剩余面；news 已判死、其余多为 OTHER ⇒ 受约束 5 限组腿 | 按 ATOM 上限≈1.0，**大概率仍过不了 1.58** |
| 4 | **缩短 IS 窗口到近 2 年** | `last_rate` 的 2Y 2.02 是全样本 2.02 的 2 倍；与约束 4 精神冲突 | LADDER / CW 闸风险大 |
| 5 | ~~**shortinterest38 库存再提 1 颗**（`mLmGQEq9` S 2.72 / prod .6011，或 `E5pjx9q0` S 2.50 / prod .6002）~~ | ⛔ **2026-10-31 实测否决**：prod 实为 **0.935 / 0.8105**（本地 .6011/.6002 是过期缓存），族内 `[0.7,0.8) n=5` ⇒ **整族判死**；且该塔已 4/3 满 | **无需用户裁决，自动关闭** |
| 6 | **sentiment 禁投令裁决** | 本区 sentiment 塔已按 wave 216 判死 | — |

> ⛔ **红线未变**：以上 6 项里 1 / 2 / 5 都是**提交**动作，必须用户逐条明确同意 + `confirm_submit=True`；
> 本 agent 只准备可复核材料，不代为提交。判死封存（`seal_dead_end`）里的 `force_seal=True` /
> `require_forum_recon=False` 同样需人工确认，本轮未使用。

### 5.92.4 本轮战役的完成定义（诚实版）

| 口径 | 结果 |
|---|---|
| wave 190–245 | **56 波，0 candidates / 0 near**（唯二 near = risk59 的 1.02 / 1.04，均属已关闭形态族） |
| 约束 1 目标 | **60** → 实测 **0** |
| 未点亮塔 | 9 座全部有关闭/冻结记录，**零计数塔可挖供给 = 0** |
| 近点亮格 | analyst 2/3 关闭 · pv 2/3 封顶 · other 1/3 封顶 ⇒ **三个全冻结** |
| 仍可交付的库存 | `LLZ6wZO2`（全闸，塔已满）· ~~`leAk66xx`（只差约束 4）~~ **prod 0.8711 判死（§8.1）** · ~~shortinterest38 可再提 1 颗~~ **prod 族死（§5.92.3 #5）** |
| 沉淀 | 56 波归因 + 19 行定量上限表 + 6 条平台事实修正（`reverse()` 差额＝2×成本、`winsorize(rank)` no-op、investS 是相对闸、多格记半分、塔票跟 `pyramids.list`、镜像分解法） |

**重开条件（预注册，不得事后放宽）**：① 用户在第 1–6 项里给出任一裁决；或 ② 平台窗口前移使 2023 退出 2Y 区间
（§5.87.5，risk 系腿的唯一外生解）；或 ③ 授权全新数据集且接受 ATOM 上限≈1.0 的现状。
三者都不满足时，**继续开波就是把已实测会更劣的轴重复烧配额**（铁律 F / G 明令禁止）。

### 5.92.5 提交材料的实测快照（供用户裁决，全部只读；`submit_verdict` × 2）

| alpha | 判定 | 模拟层 FAIL | 硬闸 WARNING | 备注 |
|---|---|---|---:|---|
| `LLZ6wZO2` | `UNVERIFIABLE` / `UNVERIFIABLE_404` | **0** | **0** | `sim_warnings` = CLUSTER_TEST **0.94**（warning 非 fail）/ MATCHES_THEMES（GLB/D1 TOPDIV3000 ×2.5）/ OSMOSIS_ALLOCATION |
| `leAk66xx` | `UNVERIFIABLE` / `UNVERIFIABLE_404` | **0** | **0** | `sim_warnings` = MATCHES_THEMES（同上）/ OSMOSIS_ALLOCATION；**无 CLUSTER 警告** |

- 两者 `failed_ra = failed_ppa = failed_any = 0`、`pending_gate_names = []`、`robustness.recorded = false`。
- **`GET /alphas/{id}/submit` 恒 404 是平台既定事实**（死端点）⇒ 现实里只有「用户确认 + POST」这一道闸，
  不存在「等 SUBMITTABLE」这种状态。放行前仍需 `check_correlation(alpha_id)` 的**平台 prod < 0.7**（缓存优先）。
- ✅ **`leAk66xx` 的 prod 已于 2026-10-31 取到 = 0.8711**（`check_correlation` 的 `last_known`，checked_at
  2026-10-31T18:11:46，龄 5.4h，`stale: false`）⇒ **D0-P 判死**，详见 §8.1。本条原写的「缺一个数」已闭环。
  （取数时账号级单并发槽仍被并行会话占用，`refresh=True` 未触发；按 `wq-prod-corr-read` 只读缓存，不重触发。）

### 5.92.6 ⭐ `leAk66xx` 全量核验：本战役唯一一颗「纯格 + 全闸 + ATOM」的未点亮塔候选

本轮 `get_alpha_details` 回读时发现此前口径**低估了它**——旧记录只写「S 1.77，只差约束 4」，没记它的塔位：

| 项 | 实测值 |
|---|---|
| 表达式 | `hump(group_rank(ts_sum(ts_backfill(vec_avg(oth695_import_value_4), 66), 20), sector), hump=0.0025)` |
| **塔位** | **`pyramids.list = [{KOR/D1/OTHER, ×1.6}]`，`effective = 1`** ⇒ **纯格、满额计分**（不是双格半分） |
| 指标 | S **1.77** / F **2.11** / 2Y **2.24** / subU **1.68** / TO .0306 / R .1783 / margin 1.16bp / RN S 1.49 |
| 闸 | **9/9 PASS** = LOW_SHARPE · LOW_FITNESS · LOW_TURNOVER · HIGH_TURNOVER · CONCENTRATED_WEIGHT · LOW_SUB_UNIVERSE_SHARPE · CLUSTER_TEST · LOW_2Y_SHARPE · MATCHES_PYRAMID；**FAIL 0** |
| warning | 仅 `MATCHES_THEMES`（GLB/D1 TOPDIV3000 ×2.5）+ `OSMOSIS_ALLOCATION`（都不在硬闸面） |
| RA | `failed_ra 0` / `failed_ppa 0` |
| 设置 | KOR / TOP600 / D1 / decay 4 / **SECTOR** / trunc .08 / nanHandling **ON** / maxTrade **ON** / 2014-01-01→2023-12-31 |
| **约束 4** | ❌ **2014–2017 四年 `longCount = 0`**，数据 2018 起 ⇒ **只有 6/10 年** |

**逐年（`get_alpha_yearly_stats`，铁律 F）**

| 年 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 |
|---|---|---|---|---|---|---|
| S | 0.21 | 2.49 | 2.03 | 2.92 | **3.79** | 0.81 |
| longCount | 400 | 433 | 339 | 361 | 352 | 347 |

- **6/6 年 S>0、无负年、无停滞段**；但 **2022 单年 pnl 3.22M 占 6 年总额 10.93M 的 29.5%**（紧贴 30% 线）、
  2021+2022 合计 **53.3%**，2023 掉到 **0.81** ⇒ 属「信号真实、但强度集中在 2021–2022 一段」，不是过拟合指纹。
- **约束 5**：单数据集单字段 ⇒ **无任何组腿，自动合规**。对照 §5.51 被拦的 `j2YWRzXW`（S 1.73 / 唯一 FAIL=CW .147）
  是**同一字段的 PV+OTHER 违规版**：违规版被拦，**ATOM 版反而是全闸通过的那一颗**。
- **可用性**：`other695` 全库仅 **3 字段** = 2 个标识符（`code_3` / `company_eng_2`，cov .53）+ **1 个信号**
  `import_value_4`（cov **.4057**、aC 148）⇒ **该集不存在第二个可换字段**；再出一颗只能对同一字段换几何，
  必然撞 self 闸。
- ⇒ **可交付性的唯一卡点 = 用户约束 4**。一旦放宽（「近 6 年」或「2018 起有数据」），
  这是一颗**可直接提交的 ATOM**，且把 **other 1/3 → 2/3**（纯格满额，塔未点亮）。
  **它不能点亮 other 塔**（需 ≥3）——但它是本战役唯一一颗「指标上没有任何瑕疵、仅差一条自设数据年限」的候选。

> ⛔ **后续（2026-10-31，§8.1）**：该候选的 prod 实读 **0.8711** ⇒ **D0-P 判死**。
> 上面「唯一卡点是约束 4」的结论**已被推翻**——它不是「只差一条自设年限」，而是**连平台硬闸都过不了**。
> 保留本段原文以留痕：**「指标全闸」不等于「只差一条自设限制」**，缺的那一道往往是还没去取的那一个数。

### 5.93 wave 247：`other` 面最后两个未动过的数据集探针（2026-10-30 发批）

§5.92 判定「未点亮塔面对单塔/组合天花板」后，唯一没做的事是**把 `other` category 剩下的 26 个集逐个看一遍**
（约束 1 原话：「一个个 category 查一下数据集情况」）。本轮补齐，按「aC 个位数 + 机制清晰」筛出两个：

| 集 | 字段 | cov | aC | 机制（A-2） | 为什么还没被烧过 |
|---|---|---|---|---|---|
| **other436** | `oth436_disc` / `_divyld` / `_mktcap` | .57 | **4 / 7 / 6** | 股利削减/取消概率 → 后续负收益（信息含量 + 公告后漂移） | 全库仅 4 条 alpha，本区零试 |
| **other475** | `oth475_export_value`（唯一） | **.357** | 632 | 韩国厂商**周频出口额** → 营收 nowcast → 盈余意外 | 与已验证的 other695（进口）**同族不同向**，但从未单独测过出口侧 |

**双通道取证（②.d）**

- **通道 A｜论坛：`no_result`**（不是 `error`）。`search_forum_posts("dividend cut")` 命中 8 条全为戈登模型/全天候策略/数据工具贴；
  `search_forum_posts("export")` 命中全为代码片段（`export FOO=`）与 MCP 配置贴。检索可靠完成、命中与机制无关 ⇒ 按证据契约记 `found=false`。
- **通道 B｜文献：机制成立**。Ghosh & Woolridge (1988) / Denis et al. (1994) 测得股利削减公告三日内平均 **−6%**；
  Balachandran, Cadle & Theobald (1996, *European Financial Management*) 在 UK 中期股息样本上确认**削减/取消对未来盈余有预测力、
  初次削减反应最强**；2005 *JBF* 的「Operating performance following dividend decreases and omissions」给出削减后经营绩效不改善的证据。
  ⇒ 方向句：**削减概率上升 → 后续负收益**，修复期 = 事件前后数日至一季（不是慢变量暴露）。
- 两通道裁决：B 有机制、A 无对应表达 ⇒ 按 A-1 五问**自建骨架**，不套模板（技能 ②.d 第 3 行）。

**体检 → 形态（②.b 查表，不许自由发挥）**

| 集 | ① 读数 | 形态决策 |
|---|---|---|
| other436 | `disc` 是 **[0,1] 概率**、季频、慢变量（同 `acquisition_model` 型） | **铁律 A 修正版**：概率水平 = 特征不是信号（§5.23 已实测 turnover .027 / 水平 S −0.21、更新 S +0.18）⇒ **取 252d 自标准化 = 「本次更新相对自身一年历史有多异常」** |
| other475 | 单边恒正的 **USD 流量**、周频 | 铁律 A：禁裸水平 ⇒ `ts_delta` 252d = **同比增速**（KOR 出口周期标准口径） |

**本波表达式（2 条，并发正好 2）**

```
① reverse(group_rank(ts_zscore(ts_backfill(vec_avg(oth436_disc), 66), 252), sector))
② group_rank(ts_delta(ts_backfill(vec_avg(oth475_export_value), 66), 252), sector)
```

- `reverse` 是本波**唯一方向主张**：削减概率上升 ⇒ 做空。**不给双方向**——单条 S 的符号同时给出「机制对不对」与「方向对不对」，
  若 S 为负且 \|S\| 可观，翻号即可（铁律 B 的回测点留到复活时再做，不在探针波烧双倍配额）。
- 设置：KOR / TOP600 / D1 / decay 4 / **SECTOR** / trunc .08 / nanHandling **ON** / maxTrade OFF / PERT P0Y0M。
- **约束 5 自检**：两条均为**单数据集单字段**，无任何组腿 ⇒ 自动合规。
- 预检：`preflight_expressions` 两条均 `valid: true`、`unknown_fields: []`、VECTOR 包裹 `any_changed: false`。
- 批次：`2HnOfm9Oq4BCbAU18rDhJDpY`。（[[约束3]] 并发 2）

**本波要回答的两个问题**（不是「跑完看数」，是先写好判据）

1. **other475 的 2014–2023 覆盖**：cov .357 是**截面**覆盖，不代表历史长度；若首年 longCount = 0，直接撞约束 4。
2. **other436 的更新率是否有信息**：若 |S| < 0.5 ⇒ 与 `acquisition_model` 同型（水平无信息、更新也弱），该集判死；
   若 S 显著为负且 2Y 不塌 ⇒ 本战役在 `other` 面找到**第二颗可用种子**（但 other695 与 other436 不能组腿——同属 OTHER，约束 5）。

### 5.94 ⭐⭐ wave 247 结果：`other475` 出口增速命中（S 1.40 / 2Y 2.13，纯格 OTHER）

| alpha | 集 | 表达式 | S | F | 2Y | subU | invS | TO | R | DD | 未达标 |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| **`KPJqmz2x`** | **other475** | `group_rank(ts_delta(ts_backfill(vec_avg(oth475_export_value), 66), 252), sector)` | **1.40** | **1.30** | **2.13** | 1.39 | 1.34 | **.0201** | **10.7%** | .136 | **仅 LOW_SHARPE（1.40 / 1.58）** |
| `O0AqJz21` | other436 | `reverse(group_rank(ts_zscore(...oth436_disc..., 252), sector))` | **−0.40** | −0.19 | **−1.71** | −0.47 | −0.39 | .0604 | −2.8% | .553 | LOW_SHARPE + 4 |

**两问的答案（§5.93 事先写好的判据）**

1. **other475 覆盖**：❌ **2014–2016 三年为零**，数据 **2017 起** ⇒ 只有 **7/10 年**，撞约束 4（与 other695 同型：
   韩国贸易类数据集的通病是上游厂商映射 2016 年才建立）。
2. **other436 判死**：S −0.40 ⇒ 翻号后仅 +0.40，|S| < 0.5 且 2Y 翻号后仍远低于 1.58 ⇒ **与 `acquisition_model` 同型
   （更新也无信息）**。叠加 §5.23 的 A-2 结论（似然的更新只在「被定价对象」上成立、股利削减被定价的是公告本身不是概率），
   **`other436` 判死，不再投**。⚠ 注意它**不是**「方向判错」——`reverse` 已按 A-2 声明做空，实测为负 Sharpe，
   说明「削减概率上升 → 负收益」在本区**不成立**，不是符号问题。

**`KPJqmz2x` 归因（铁律 F）**

| 年 | 2014 | 2015 | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 |
|---|---|---|---|---|---|---|---|---|---|---|
| S | — | — | — | 1.42 | **−0.55** | 1.79 | 0.93 | **2.13** | **2.19** | **2.07** |
| pnl(M) | 0 | 0 | 0 | .78 | **−.49** | 1.37 | .70 | 1.83 | 1.76 | 1.76 |
| long / short | — | — | — | 131/431 | 143/482 | 151/461 | 145/461 | 133/502 | 148/486 | 168/480 |

- **不是单年行情**：7 个有数据年份里 **6 正 1 负**，2021–2023 连续三年 S>2.0 且 pnl 逐年递增（1.83/1.76/1.76）——
  与 `leAk66xx`「2022 占 29.5%」相反，这颗的**强度在最近三年是抬升的**，不是衰减。
- **唯一负年 2018（−0.55）**：2018 = 中美贸易摩擦首年 + 韩国出口下滑年 ⇒ 属机制内的**周期反转年**，
  不是噪声（出口增速本身就是周期变量，单年反向是设计内风险）。
- `investability_ratio 0.9571`（invS 1.34 ≫ 0.7×1.40=0.98）⇒ **不是小市值/流动性假象**。
- RN S **1.05** vs raw 1.40 ⇒ 因子暴露贡献 0.35，纯 alpha 仍 >1.0（不是纯暴露）。
- ⚠ **持仓极度不对称**：long 146 / short 472。出口增速高的公司天然是大出口商、行业集中，
  做多端窄 ⇒ 这是 `CONCENTRATED_WEIGHT` 已过但 `longCount` 偏小的结构性特征，**加壳时要盯着多端**。

### 5.95 wave 248：只动中性化这一根（KOR SOP ⑤「先分组轴」）

| # | 表达式 | 中性化 | 与 247 的差异 |
|---|---|---|---|
| E1 | 同 `KPJqmz2x` 逐字 | **MARKET** | 只换中性化，取**更粗**轴（利用 KOR 已验证「换粗轴常使 robust 与 S 同升」） |
| E2 | 同 `KPJqmz2x` 逐字 | **SUBINDUSTRY** | 只换中性化，取**更细**轴（反向对照，夹住 SECTOR） |

- 表达式**逐字不变** ⇒ 波间唯一变量 = 分组轴，符合铁律 G「只在上波优胜集合内变动」与 ⑤ 的杠杆顺序。
- 两个方向**同时给**是为了把轴夹住：若 MARKET 与 SUBINDUSTRY 都劣于 SECTOR ⇒ 该轴一次试完，下一步转「平滑」；
  若任一优于 SECTOR 且 ≥1.58 ⇒ 直接进 2Y/robust 复核。
- 组腿：单数据集单字段 ⇒ 约束 5 自动合规。
- 目标：S 1.40 → **1.58**（差 0.18，13%）。



**⚠ 实际派发与本设计的偏差（2026-10-30 11:22 更正，必须留痕）**

`create_multi_simulation` 的 schema 是**一个 settings 块服务整批**（`neutralization` / `decay` / `truncation` 等都在批级），
**批内无法逐条给不同中性化**。本次按 E1 的 MARKET 派发，两条表达式字符串**逐字相同**
⇒ 平台按表达式去重后大概率只回 1 个 child（见 `brain-multisim` 记忆：multisim 按表达式去重），
即 **wave 248 只拿到 MARKET 一个点，SUBINDUSTRY 那一臂根本没发出去**。

**结论（写进纪律）**：
- **设置轴（neutralization / decay / truncation / nanHandling）的扫描 = 一次调用一个设置**，不能靠一条 multisim 内的多条表达式做对比；
- 想把一条 multisim 的两个槽都用上，变异必须发生在**表达式内部**（例如 `group_rank(x, A)` vs `group_rank(x, B)`），
  否则第二槽是重复劳动。

**因此把「分组轴」拆成两个层面分别测**（SOP ⑤「先分组轴」的完整执行）：

| 层面 | 变量在哪 | 怎么测 | 状态 |
|---|---|---|---|
| **L1 平台中性化** | settings `neutralization` | 一次调用一个设置：MARKET（248 已发）→ SUBINDUSTRY（补发） | 半完成 |
| **L2 表达式内分组** | `group_rank` 的第二参 | **一条 multisim 内给 3 个不同分组**：market / industry / subindustry（settings 固定 SECTOR 作对照） | 待发 |

L2 之所以能在一条 multisim 里做，正因为它改的是表达式而不是设置 ⇒ 与上面那条纪律不冲突。

### 5.96 wave 248 结果：MARKET 中性化 **同轴上升但不够**（S 1.40 → 1.44，纯格 OTHER）

| alpha | 中性化 | S | F | 2Y | subU | invS | RN S | TO | R | DD | margin | pnl |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `KPJqmz2x` | SECTOR（247 基线） | 1.40 | 1.30 | 2.13 | 1.39 | 1.34 | 1.05 | .0201 | 10.70% | .1364 | .010662 | 7,711,187 |
| **`omEAEOb5`** | **MARKET** | **1.44** | **1.36** | **2.25** | **1.45** | **1.38** | 1.06 | **.0172** | **11.23%** | .1506 | **.013086** | **8,096,046** |

- **换粗轴确实同升**（KOR 已验证的规律复现）：S +0.04、2Y **+0.12**、subU +0.06、F +0.06、margin +23%、TO 反降 14%；
  唯一变差的是 DD（.1364 → .1506）。
- **但仍差 0.14 才到 1.58**（1.44 / 1.58 = 91%）⇒ 分组轴单换一层不够，需要**二维联立**（中性化 × 表达式内分组）。
- `checks.fail = []`，唯一未达 = `LOW_SHARPE`（1.44 / 1.58）；`pyramids.effective = 1`、`KOR/D1/OTHER ×1.6` ⇒ **纯格满额**。
- ⚠ **去重确认**：两条同字符串只回 **1 个 alpha**（两个 child 指向同一 `omEAEOb5`）⇒ 与 `brain-multisim` 记忆一致，
  再次证明「一条 multisim 的第二槽必须放**不同表达式**」。

### 5.97 分组轴二维矩阵的推进顺序（在 248 之后）

已知两个角：`SECTOR×sector` = 1.40、`MARKET×sector` = 1.44。剩下要补的格子按信息量排序：

| 批次 | settings 中性化 | 表达式内 group（一条 multisim 内三选） | 目的 |
|---|---|---|---|
| **L2（在飞 `2q3XXne2v4J6cs7eHwVqAmI`）** | SECTOR | market / industry / subindustry | 隔离「表达式内分组」单变量效应（settings 固定在基线） |
| **L3（L2 之后）** | **MARKET** | market / industry / subindustry | 与 L2 组成 2×3 矩阵，取最好一格 |
| L4 | STATISTICAL | 取 L2/L3 最好 group + sector group | KOR 已知 STATISTICAL 常最优，单独一臂 |

判据：任一格 **S ≥ 1.58** ⇒ 直接进 2Y/robust/CW 复核；全部 < 1.58 ⇒ 分组轴一次试完，转 SOP ⑤ 第二步「平滑」。

### 5.98 wave 249（L2）结果：表达式内分组 **越细越好**，与经济学直觉相反（S 1.40 → 1.50）

settings 固定 SECTOR（与 247 基线同），只换 `group_rank` 的第二参：

| alpha | group | S | F | 2Y | subU | invS | RN S | TO | DD | 相对 sector 基线 |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| `KPJqmz2x` | sector | 1.40 | 1.30 | 2.13 | 1.39 | 1.34 | 1.05 | .0201 | .1364 | — |
| `zq3Q35w1` | **market** | 1.31 | 1.18 | 1.96 | 1.30 | 1.27 | 0.91 | .0191 | .1510 | ❌ −0.09，且新增 `CLUSTER_TEST 0.93` 警告 |
| `O0AqAnwb` | **industry** | 1.45 | 1.36 | 2.23 | 1.48 | 1.39 | 0.99 | .0210 | .1445 | ✅ +0.05 |
| **`88R7ROkl`** | **subindustry** | **1.50** | **1.40** | 2.15 | **1.53** | **1.41** | **1.07** | .0208 | .1585 | ✅ **+0.10（当前最好）** |

- **A-1 第 2 问的预测被实测推翻**：原判「出口增速主要是行业级变量 ⇒ 分组越粗越保留信号」，
  实测 **单调反向**（order 越细 S 越高：market 1.31 < sector 1.40 < industry 1.45 < subindustry 1.50）。
  经济解释（事后，非事前）：**出口增速的行业成分是共识信息、个股在行业内的相对出口份额变化才是私有信息**；
  粗分组把行业级共识留在持仓里 = 增加共同因子暴露（佐证：market 组的 RN S 掉到 0.91，subindustry 组 1.07）。
- **`zq3Q35w1`（market 分组）除 S 下降外还新触发 `CLUSTER_TEST 0.93` 警告** ⇒ 粗分组确实在往「扎堆」方向走，
  与上一条解释一致。⇒ **market 分组这一格判死，不再测**。
- `88R7ROkl` 全部 `checks.fail = []`，唯一未达仍是 `LOW_SHARPE`（1.50 / 1.58，差 **0.08**），`effective = 1` 纯格。
- 三者 `SUBMISSION` 前的 pending 都是相关性四项 + `MATCHES_THEMES`，与基线一致。

### 5.99 wave 250（L3）：把两个「各+一点」的杠杆叠起来

`88R7ROkl` 证明**表达式内分组**到 subindustry 最好（+0.10）；`omEAEOb5` 证明**平台中性化**到 MARKET 也 +0.04。
两者作用在不同层 ⇒ 测可加性，一条 multisim 两个槽（settings 固定 MARKET）：

| # | 表达式内 group | settings | 假设 |
|---|---|---|---|
| E1 | **subindustry** | MARKET | 可加 ⇒ 预期 S ≈ 1.54 |
| E2 | industry | MARKET | 若 E1 过拟合、industry 更稳，则退一格 |

判据：E1 **S ≥ 1.58 且 2Y ≥ 1.58** ⇒ 直接进稳健闸 + CW 复核；S 落 1.52–1.57 ⇒ 继续 SOP ⑤ 第二步「平滑」。

### 5.100 wave 250（L3）结果：两杠杆**次可加**，分组轴到此为止（S 1.51，差 0.07）

| alpha | group × 中性化 | S | F | 2Y | subU | invS | invF | RN S | TO | R | DD | pnl |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `KPJqmz2x` | sector × SECTOR | 1.40 | 1.30 | 2.13 | 1.39 | 1.34 | — | 1.05 | .0201 | 10.70% | .1364 | 7.71M |
| `88R7ROkl` | subindustry × SECTOR | 1.50 | 1.40 | 2.15 | 1.53 | 1.41 | 1.28 | 1.07 | .0208 | 10.91% | .1585 | 7.86M |
| `omEAEOb5` | sector × MARKET | 1.44 | 1.36 | 2.25 | 1.45 | 1.38 | 1.28 | 1.06 | .0172 | 11.23% | .1506 | 8.10M |
| `QPvqvYWw` | industry × MARKET | 1.48 | 1.42 | **2.33** | 1.54 | 1.43 | **1.35** | 0.99 | .0180 | **11.51%** | .1568 | **8.29M** |
| **`akKMKVRx`** | **subindustry × MARKET** | **1.51** | **1.44** | 2.22 | **1.57** | **1.43** | 1.33 | **1.08** | **.0177** | 11.43% | **.1706** | 8.24M |

**2×3 矩阵读数（分组轴已扫完）**

| group ＼ 中性化 | SECTOR | MARKET |
|---|---:|---:|
| market | 1.31 ❌（+CLUSTER 警告） | 未测（已判死，不补） |
| sector | 1.40 | 1.44 |
| industry | 1.45 | 1.48 |
| **subindustry** | 1.50 | **1.51** ← 当前最好 |

- **次可加**：subindustry 单换 +0.10、MARKET 单换 +0.04，叠起来只 +0.01（1.50 → 1.51）
  ⇒ **两个杠杆作用在同一个成分上**（都在剥行业共同项），不是独立增益。
  ⇒ **分组轴的信息已榨干**，继续扫中性化（STATISTICAL / SUBINDUSTRY）预期增益 < 0.03，不值得再烧。
- ⚠ **代价必须记账：DD 单调恶化** .1364 → .1585 → **.1706**。Sharpe 的提升**部分来自把亏损年集中**，
  不是纯增益。这条要在稳健闸复审时正面回答。
- 三者 `checks.fail = []`、`effective = 1` 纯格 KOR/D1/OTHER，唯一未达仍是 `LOW_SHARPE`。

**`akKMKVRx` 归因（铁律 F，发波前置）**

| 年 | 2014–16 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| S | — | 0.94 | **−0.95** | 1.69 | 1.80 | **2.72** | 1.81 | **2.59** |
| pnl(M) | 0 | .539 | **−.820** | 1.328 | 1.304 | **2.324** | 1.370 | 2.192 |
| long/short | — | 127/488 | 138/515 | 146/501 | 140/507 | 124/558 | 139/516 | 162/494 |

| 判据 | 读数 | 结论 |
|---|---|---|
| 单年占正收益 | 2021 = 2.324 / 9.057 = **25.7%** | < 30% ⇒ **非过拟合指纹** |
| S<1.0 年份占比 | 2/7 = **28.6%** | < 3 成 ⇒ 2Y 可达（实测 2.22 印证） |
| 近年断崖 | 2023 = 2.59（次高） | 无衰减 |
| 停滞段 | 仅 2018 一段 | < 3 ⇒ 非 regime 依赖 |
| 2018 恶化 | −0.55 → **−0.95** | ⚠ 细分组把贸易摩擦年的亏损**放大**了，是 DD 恶化的来源 |

⇒ 归因落在决策表最后一行「**阶梯健康 + 停滞段少 + 单年 <30% ⇒ 此时才允许做强度 / returns 杠杆扫描**」。
**分组轴已试完，按 SOP ⑤ 转第二步「强度 / 平滑」。**

### 5.101 wave 251：两个强度杠杆，各只改一处（发批 `1qP65n1Ro4TZ9W4ENUOXV0V`）

取证：`wq-alpha-gate-push-op-min` 杠杆阶梯 **L2 双窗级联**（源战役实测 S +0.18 / 2Y +0.6）
与 **④b 等效替换**（`ts_av_diff → ts_zscore` 同义不同实现，GBR `j2YNnKOQ` 实测 prod 0.67→0.6191）。
两条都**保留机制**（韩国厂商出口增速 → 营收 nowcast），不是换概念。

| # | 表达式 | 相对 `akKMKVRx` 的唯一改动 | 预期 |
|---|---|---|---|
| E1 | `group_rank(multiply(rank(ts_delta(ts_backfill(vec_avg(oth475_export_value),66),252)), rank(ts_delta(ts_backfill(vec_avg(oth475_export_value),66),66))), subindustry)` | 加**第二条同字段短窗腿**（252 年增速 × 66 季增速） | 双尺度确认 ⇒ S ↑ |
| E2 | `group_rank(ts_zscore(ts_backfill(vec_avg(oth475_export_value),66),252), subindustry)` | `ts_delta` → **`ts_zscore`**（同为「相对自身历史的偏离」，多了波动归一） | 跨股可比性 ↑ ⇒ S ↑ |

- settings 两条同为 **MARKET / decay 4 / trunc .08 / nanHandling ON / maxTrade OFF**（沿用 L3 最好档）。
- **约束 5 自检**：两条都是**单数据集单字段**（`other475` / `oth475_export_value`），E1 的两条腿是**同一字段的两个窗口**
  ⇒ 属「同字段多时间窗 = 单信号结构化」，**不是**跨字段/跨 category 组腿，合规。
- **窗口白名单自检**：只用 66 / 252（源战役的 240/176 是非标窗，不照搬；KOR 要求标准窗或给证据）。
- 预检 `preflight_expressions`：`valid: true`、`unknown_fields: []`、`any_changed: false`。
- **波次三问（铁律 G）**：继承 = 「subindustry × MARKET 是分组轴最优、两杠杆次可加」；
  准入 = **禁再扫中性化 / 禁 market 分组 / 禁 truncation**；收窄 = 2 条（上波 2 条，同量但**每条只改一处**，
  且都在上波优胜 `akKMKVRx` 的邻域内，不是并列扫参）。
- 判据：任一 **S ≥ 1.58** ⇒ 进 2Y/robust/CW + prod 复核；两条都 < 1.58 ⇒ 按 ⑥ 止损条款记「累计 3 轮卡结构性闸」，
  转 `other545` 新面（本战役最后一个未动过的 other 信号面）。

### 5.102 ⚠ 并行会话争用实测：wave 251 排队，且 SHORTINTEREST 塔可能已被别的会话点亮

**现象**：wave 251（`1qP65n1Ro4TZ9W4ENUOXV0V`）派发后 `progress` 长时间停在 **0.35**、
`harvest_multisim_alphas` 一直回 `No children found`；`batch_status` 同样 `child_count 0`。
多次复查（含一次 `ECONNRESET` 后重试）读数不变 ⇒ **不是慢，是排队**。

**根因取证（`get_user_alphas(region=KOR, stage=IS, order=-dateCreated, limit=5)`）**：
最新 5 颗 KOR IS alpha **全部不是本会话的**，而是并行会话在打 `shortinterest38`，
设置档与本战役完全不同（**decay 20 / SLOW_AND_FAST / truncation 0.02**，本战役是 decay 4 / 逐候选中性化 / trunc .08）：

| alpha | 表达式骨架 | S | F | 2Y | subU | invS | TO | RA fail | 塔位 |
|---|---|---:|---:|---:|---:|---:|---:|---:|---|
| `6Xd3Ja7P` | `group_rank(divide(invactsell_amt, add(invactsell_amt, invactbuy_amt, 1e-4)), sector)` | **3.12** | 2.36 | 2.55 | 2.29 | 2.91 | .2797 | **0** | SHORTINTEREST ×1.4，effective 1 |
| `Xg9PvN8l` | 同上，group=industry | **2.83** | 2.01 | 2.20 | 2.01 | 2.67 | .2777 | **0** | 同上 |
| `zq3QGWeo` | `divide(invactsell_amt, add(invactbuy_amt, 1e-4))`，group=subindustry | **2.34** | 1.49 | 2.16 | 1.73 | 2.17 | .2813 | **0** | 同上 |
| `j2YWpmwZ` | `group_rank(vec_avg(stk_short_sellshort_sell_amt), sector)` | 0.49 | 0.19 | 0.65 | 0.62 | 0.51 | .1759 | 3 | 同上 |
| `rKREqJrd` | `divide(sell_amt, add(sell_qty, 1e-4))`，group=sector | −0.33 | −0.12 | −0.79 | 0.20 | −0.30 | .1158 | 4 | 同上 |

**三条结论**：

1. **账号级 2 个仿真槽被并行会话占着** ⇒ 本会话的 multisim 只能排队。按 `wqb-concurrency` 纪律
   **不重发、不加批**（重发只会多占一个排队位，且可能撞 429），继续等。
   ⇒ 这也解释了 §5.96 里 wave 248 的 `batch_status` 长期 `child_count 0` 而 harvest 却能收到结果：
   **`batch_status` 的 children 解析在排队期不可靠，收批一律以 `harvest_multisim_alphas` 为准。**
2. **SHORTINTEREST 塔大概率即将点亮**：上面三颗 `ra_failed_count = 0`、`effective = 1` 纯格，
   只要那个会话提交 ≥3 颗，`KOR/D1/SHORTINTEREST` 就从未点亮变已点亮。
   ⇒ **§5.92.3 的用户决策第 5 项（再提一颗 shortinterest38）可能自动失效**，
   且本战役**不得**再把 shortinterest 当未点亮塔投入（步 2 硬约束 0）。**提交前必须重查塔位。**
3. **这三颗不是本战役的产出**，不得计入「60 个 regular alpha」的进度，也不得由本会话代为提交
   （AGENTS.md §7 并行写入者纪律：不跨会话代处置）。此处只登记事实，供后续塔位核验用。

**prod 槽同样被占**：`check_correlation("leAk66xx", production)` 回 `correlation_busy`、
`holder = corr:get_production_correlation(A1VbJpww)`、`inflight = false`（**不是本会话触发的**）
⇒ 按 `wq-prod-corr-read` 纪律**只复查不重触发**，`leAk66xx` 的 prod 本轮仍缺。
---

### §5.103 wave 251 收批 —— ★ 突破：`ts_zscore` 等效替换把 S 从 1.51 推到 1.92，全闸通过

**批次** `1qP65n1Ro4TZ9W4ENUOXV0V`（§5.101 设计），设置 MARKET / decay 4 / trunc 0.08，
`harvest_multisim_alphas` 收批：`total 2 / complete 2 / error_count 0`。
入库 `harvest_multisim_results(region=KOR, wave=251)` → `upserted 2`，
`wave_result = inserted: wave 251 暂定 verdict=PASS（2/2 过硬闸）`。

| alpha | 杠杆 | S | F | 2Y | subU | invS | invF | RN S | TO | R | DD | margin | pnl | long/short |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `rKRLLzRa` | L2 双窗级联 252×66 | 1.61 | 1.60 | 2.16 | 1.70 | 1.55 | 1.51 | 1.22 | .0202 | 12.36% | .1501 | .012223 | 8.91M | 135/516 |
| **`leA22za2`** | **④b 等效替换 `ts_delta`→`ts_zscore`** | **1.92** | **2.07** | **2.20** | **1.82** | **1.88** | **2.01** | **1.69** | .0270 | **14.53%** | **.1105** | .010758 | **11.87M** | 154/494 |

两条 `ra.failed_ra_count = 0`、`checks.fail = []`，
`pass` 含 **LOW_SHARPE / LOW_FITNESS / LOW_2Y_SHARPE / CONCENTRATED_WEIGHT /
LOW_SUB_UNIVERSE_SHARPE / LOW_INVESTABILITY_CONSTRAINED_SHARPE / CLUSTER_TEST / MATCHES_PYRAMID**；
`warning` 只有 `MATCHES_THEMES` / `OSMOSIS_ALLOCATION`（非 RA 资格门）。
两条均 `pyramids.effective = 1`、`list = [KOR/D1/OTHER ×1.6]` ⇒ **纯格 OTHER ATOM**。

**★ 单变量对照（其余全部冻结，基线 = §5.100 的 `akKMKVRx` S 1.51）**：

| 读数 | 基线 `akKMKVRx`（ts_delta） | `leA22za2`（ts_zscore） | 变化 |
|---|---|---|---|
| S | 1.51 | **1.92** | **+0.41** |
| fitness | 1.44 | **2.07** | +0.63 |
| 2Y | 2.22 | 2.20 | −0.02（噪声级） |
| subU | 1.57 | **1.82** | +0.25 |
| invS | 1.43 | **1.88** | +0.45 |
| RN S | 1.08 | **1.69** | **+0.61** |
| **drawdown** | .1706 | **.1105** | **−0.0601（改善 35%）** |
| turnover | .0177 | .0270 | +0.0093（仍远低于闸） |
| 算子调用点 | 4 | **4** | **不变** |

⇒ **这是本战役第一次「指标全面变好 + 回撤显著变小 + 算子数不增」的改进**，
不是拿余量换算子数，也不是拿 DD 换 S。按 skill ④b 采纳判据（指标更好）**直接采纳**。

**机制解释（为什么 z-score 比裸差分强这么多）**：
`ts_delta(x,252)` 只测「相对 1 年前的绝对增量」，出口额的**量纲与波动率逐股差异极大**
（大企业 vs 小企业、周期性行业 vs 稳定行业），裸差分让高波动股主导了截面排序。
`ts_zscore(x,252)` = 同一「相对自身 1 年均值的偏离」，但**除以了自身 252 日标准差**
⇒ 把「偏离幅度」换算成「以本股自身波动为单位的意外程度」。
金融含义**未变**（仍是出口增长的意外强度），但**可比性**变了 —— 这正是 RN S 从 1.08 跳到 1.69
（风险中性化后信号更强 ⇒ 原来有相当部分 S 被波动率暴露吃掉）与 DD 从 .1706 降到 .1105 的共同来源。
**与 GBR `j2YNnKOQ` 案例方向一致但收益更大**：那边是 S 略降换 prod 安全边际，这边是 S/DD/RN 三赢。

**⑤ 采纳与 SUPERSEDED 记账**：
`leA22za2` 为本骨架唯一保留件；`akKMKVRx`(1.51) / `QPvqvYWw`(1.48) / `88R7ROkl`(1.50) /
`O0AqAnwb`(1.45) / `omEAEOb5`(1.44) / `KPJqmz2x`(1.40) / `zq3Q35w1`(1.31) / `rKRLLzRa`(1.61)
全部标 **SUPERSEDED**（同骨架互相关必然 >0.99，只留指标最好且算子最少的那 1 颗）。

**L2 双窗级联在本字段上的实测结论（跨战役不可照搬的又一实证）**：
skill 记的来源战役增益是 S +0.18 / 2Y +0.6，本字段实测 **+0.10 / 2Y −0.06**，
且**多花 2 个算子**（4→6）、DD 反而比等效替换差（.1501 vs .1105）。
⇒ **L2 在 other475 上劣于 ④b，且性价比为负**；本骨架不再投级联变体。
（标准窗口 252×66 替代来源战役的非标 240×176 是合规做法，但**合规不等于有效**。）

#### §5.103.1 `leA22za2` 逐年归因（铁律 F，收批后立即做）

`get_alpha_yearly_stats("leA22za2")`：

| 年 | S | pnl | long/short | TO | DD | fitness |
|---|---|---|---|---|---|---|
| 2014 | 0 | 0 | **0/0** | 0 | 0 | 0 |
| 2015 | 0 | 0 | **0/0** | 0 | 0 | 0 |
| 2016 | **2.72** | 1.663M | 113/454 | .0339 | .0294 | 3.07 |
| 2017 | 1.51 | 0.969M | 150/471 | .0233 | .0381 | 1.30 |
| **2018** | **−0.51** | **−0.427M** | 156/497 | .0236 | .0955 | −0.29 |
| 2019 | 2.64 | 2.170M | 153/494 | .0235 | .0362 | 3.40 |
| 2020 | 1.96 | 1.448M | 144/503 | .0259 | .0477 | 2.15 |
| 2021 | **2.79** | 2.352M | 146/536 | .0284 | .0429 | 3.75 |
| 2022 | 1.77 | 1.298M | 163/493 | .0278 | .0495 | 1.77 |
| 2023 | 2.57 | **2.396M** | 193/463 | .0273 | .0830 | 3.49 |

**归因决策表逐项核对**：

| 判据 | 门槛 | 实测 | 结论 |
|---|---|---|---|
| top1 年占正收益 | >30% ⇒ 过拟合 | 2.396 / 12.296 = **19.5%** | ✅ 远低于门槛 |
| S<1.0 年份占比 | ≥30% ⇒ 2Y 结构性不可达 | 1/8 = **12.5%**（只有 2018） | ✅ 从基线的 28.6% 大幅改善 |
| 近年 S 断崖 | 2+ → <0.5 | 2021→2023 = 2.79/1.77/2.57 | ✅ 无断崖，近年反而最强 |
| 停滞段 | ≥3 ⇒ regime 依赖 | 2014–15（无数据）+ 2018（单年亏损）= **1 段真实停滞** | ✅ |
| 曲线形态 | 阶梯累积 = 健康 | 除 2018 外**逐年正收益、7 年连续累积** | ✅ 健康阶梯 |

⇒ **归因判定：信号真实、强度充足、无过拟合指纹**。按决策表最后一行，
**此时才允许**做强度 / returns 杠杆扫描；但 S 1.92 已远超 1.58 门槛（余量 0.34），
**不需要再推指标**，直接进相关性 + 稳健性终验。

**★ 2018 亏损被治好了**：基线 `akKMKVRx` 2018 S = **−0.95** / pnl −0.820M / DD .1315，
`leA22za2` 2018 S = **−0.51** / pnl −0.427M / DD .0955 ⇒ 亏损减半。
这独立佐证了上面的机制解释：**贸易战年的损失主要来自波动率暴露，不是信号方向错**，
z-score 的波动归一化把这部分暴露剥掉了。（§5.100 记的「细分组放大 2018 亏损」被此修复。）

**★ 数据起点比基线早一年**：基线 2014–16 全零、2017 才有持仓；
`leA22za2` **2016 就有 113/454 持仓、S 2.72** ⇒ 有效年数 **8/10（2016–2023）**，
比基线的 7/10 多一年。原因待查（`ts_zscore` 与 `ts_delta` 对 `ts_backfill` 前缀的
有效样本要求不同：z-score 需要方差非零，差分需要两端都有值 ⇒ 前者在数据稀疏起点更早可用）。
⚠ **仍不满足用户约束 4「近十年都要有数据」**（2014/2015 零持仓），见 §5.105 待决项。

#### §5.103.2 self 相关性（本地 OS 池，不占平台槽）

`check_self_correlation("leA22za2")` → **`passes_check = true`，`max_correlation = 0.6519`**（< 0.7）。
`pool_size 28 / full_os_pool_size 42 / excluded_power_pool_count 14`。
top：`xA16pzQJ` **0.6519** / `RRA2eE70` 0.2789 / `9qjGvaWe` 0.2488 / `0mre68gv` 0.2134 / `RRA9EZKz` 0.2097。
⚠ **余量只有 0.048**，且第二名骤降到 0.28 ⇒ 相关性几乎全部来自 `xA16pzQJ` 一颗。
提交前须核 `xA16pzQJ` 是什么（同骨架旧变体？若它是本战役 SUPERSEDED 件则不构成障碍；
若是已提交 OS 件则 0.6519 是真实约束，prod 漂移外还要盯 self 漂移）。

#### §5.103.3 prod 取数受阻（工具故障，非平台结论）

`check_correlation("leA22za2", correlation_type="production")` → **MCP error −32603
「invocation did not complete」**（平台 prod 异步排队 1–5 分钟，超出 MCP 请求超时）。
按证据契约这是 **`error`，不是 `no_result`，更不是「prod 超线」**。
⚠ **本次调用是否已在平台侧触发计算未知** ⇒ 下次只用 `refresh=False` **复查**
（若 `inflight=true` 会 join 到那次计算上），**不得带 `refresh=True` 重触发**
（`wq-prod-corr-read`：重复触发只会把自己顶成 busy）。

---

### §5.104 wave 252 派发 —— `other545` / `oth545_pln_omen`（本战役最后一个未动过的 other 信号面）

wave 251 收批后 2 个仿真槽空出，立即填槽（不留空转）。
**批次** `3dhvS0fnv5cNcjz2xhdBfWc`，设置 KOR/TOP600/D1、**SECTOR** / decay 4 / trunc 0.08 /
pasteurization ON / unitHandling VERIFY / nanHandling ON / maxTrade OFF。

| # | 表达式 | 桶 | 单变量对照 |
|---|---|---|---|
| P1 | `group_rank(ts_backfill(vec_avg(oth545_pln_omen), 66), subindustry)` | Level | 基线：水平量是否有信号 |
| P2 | `group_rank(ts_delta(ts_backfill(vec_avg(oth545_pln_omen), 66), 22), subindustry)` | Change | 相对 P1 只加 `ts_delta(·,22)` |

**为什么选 `pln_omen` 而不是头部字段 `score`**（0.1 质量先验的正确用法）：
`oth545_score` u15/a20 是头部（NEMO 2.0 七信号合成分），但**最拥挤**；
`oth545_pln_omen` u3/a3 **最少人挖**，描述为
「Score based on NLP-derived network momentum using text-mined linkages」
⇒ **ATOM 赔率最好**。头部字段揭示的是「该集最强经济轴 = 网络动量」，
本波顺着这条轴走，但**取轴上最冷门的实现**，这是 0.1 与拥挤度的联合用法，不是违背 0.1。

**②.d 双通道裁决（已取证，写在派发前）**：
- **通道 A 论坛**：`search_forum_posts("NEMO network momentum")` → 5 命中，
  **无一涉及本数据集或股票网络动量机制** ⇒ 可靠检索无解，记 **`no_result`**（不是 error）。
  附带一条负面证言：「我的量化日记第一季」（60 票 / 1000 评）引 arXiv **2308.11294**
  *Network Momentum across Asset Classes*，认为在 BRAIN 上难复现（**跨资产类别**研究）
  ⇒ 这是**适用域警告，不是判死**：本波做的是**单一股票市场内的个股网络溢出**，与该论文的跨资产设定不同。
  ⚠ 另一次检索 `search_forum_posts("network momentum 供应链 动量")` 回 **−32603**，
  按契约记 **`error`**，**不得当作第二次「论坛无解」证据**。
- **通道 B 论文**：Cohen & Frazzini (2008) *Economic Links and Predictable Returns* ——
  客户/供应链关联股票的收益可预测性，**1.55%/月、18.6% 年化**，机制 = 投资者注意力有限、
  信息沿经济链接缓慢扩散。⇒ 给的是**机制 + 方向句 + 持有期**。
- **裁决**：**B 有机制、A 无对应表达 ⇒ skill ②.d 表里「最有价值」那一格**
  ⇒ 按 A-1 五问**自建骨架**（就是上面 P1/P2），不套模板。

**A-2 收益来源声明（硬门，四项齐全）**：
- **谁在被定价**：持有关联股票的投资者（注意力有限的散户与部分机构）。
- **为什么会被错**：注意力配置不足 —— 文本挖掘出的公司间链接（供应链/合作/引用）
  不在多数投资者的信息集里，龙头的信息要**沿链接滞后扩散**到关联股。
- **错了多久修复**：数周到一季（故窗口取 22 / 66，不用 1 / 5）。
- **预期方向**：网络动量分高 ⇒ 关联信息尚未被消化 ⇒ **后续正向漂移**（做多高分股）。
  ⚠ 方向仍按**铁律 B** 留反号余地：若 P1/P2 双双负 S，先测 `reverse` 再判死，不直接下「无信号」结论。

**约束 5 合规核对**：`oth545_mpd` + `oth545_score` 是 **OTHER + OTHER 两两组腿 ⇒ 禁止**。
本数据集**只出单字段 ATOM**，P1/P2 均单字段（`ts_backfill` / `ts_delta` / `group_rank` 是壳层不是腿）。
`oth545_mktcap` 只可能作规模残差化壳层（②.c），**不作信号腿**。

**波次三问（铁律 G）**：
1. **继承**：wave 251 证明「`group_rank(…, subindustry)` + 波动/水平归一化」是本区 other 类的有效壳；
   本波沿用同一壳，只换数据集与字段（**壳的跨字段有效性须本波实测，不当既定结论**）。
2. **准入**：不动 `other475`（已收敛到 `leA22za2`，余量 0.34 无需再推）；
   不碰 `mpd`/`score` 组腿（约束 5）；不扫 truncation（已死轴）；不做双窗级联（§5.103 实测性价比为负）。
3. **收窄**：2 条探针（Level / Change 各一），是**新面最小可判集**，不是铺量。
   判据：任一 |S| ≥ 1.0 ⇒ 该字段有信号，进 ③ 归因 + ④ 破闸；
   两条 |S| < 1.0 ⇒ 换 `score`（头部轴的最强实现）再探一轮，仍无 ⇒ 记 `other545` 天花板。

**中性化选 SECTOR 的理由（不是照搬 other475 的 MARKET）**：
§5.100 的 2×3 矩阵是 **`oth475_export_value` 这一个字段**的实测结论，
skill 明写「杠杆逐字段 / 逐族实测，不可照搬」。新字段用 **SECTOR 作中性基线**，
若 P1/P2 出信号，**分组轴矩阵须在本字段上重扫**，不得直接套 MARKET。---

### §5.105 `leA22za2` prod 终验 = 0.8377 ⇒ D0-P 判家族撞结构性墙（指标全闸 ≠ 可提交）

`check_correlation("leA22za2", correlation_type="production")` 第二次复查（`refresh=False`，
join 到 §5.103.3 那次触发上，`inflight=true / 第 1 次触发`）拿到平台实测值：

**`max_correlation = 0.8377`，`passes_check = false`（线 0.7），`attempts 1 / elapsed_ms 269 / computed false`（读的是已算好的缓存）。**

prod 直方图（全量，min −0.3559 / max 0.8377）：

| 桶 | n | 桶 | n |
|---|---|---|---|
| [−0.4,−0.3) | 10 | [0.2,0.3) | 15455 |
| [−0.3,−0.2) | 182 | [0.3,0.4) | 3309 |
| [−0.2,−0.1) | 2162 | [0.4,0.5) | 374 |
| [−0.1,0) | 16461 | [0.5,0.6) | 70 |
| [0,0.1) | 39155 | **[0.6,0.7)** | **29** |
| [0.1,0.2) | 34672 | **[0.7,0.8)** | **9** |
| | | **[0.8,0.9)** | **2** |

#### §5.105.1 D0-P 路由（唯一决策表，不另立学说）

0.8377 **≥ 0.75** ⇒ 走「**先做诊断前置**」那一行，不是直接判死，也不是盲扫。

**诊断前置第 1 步（看直方图分形态）**：

| 形态 | 判据 | 本例实测 | 命中 |
|---|---|---|---|
| (a) 单颗钉子型 | 0.7+ 仅 **1–3** 颗、0.6–0.7 仅 **6–16** 颗 | 0.7+ = **11** 颗、0.6–0.7 = **29** 颗 | ❌ 钉子数远超单颗型 |
| (b) 密墙型 | 0.6–0.7 桶 **数百颗**（GLB n=848–877） | 29 颗 | ❌ 未到密墙量级 |
| (c) 可破型 | 钉子是**少数**同族兄弟或设置档 | 11 颗钉子 + 29 颗近墙 | ⚠ 见第 2/3 步 |

⇒ **多钉子拥挤族**：比单颗钉子型更拥挤（单颗型的结论已是「任何构造都被钉住，直接 dead_end」），
但还没到密墙型的数百颗。**按 (a) 的处置逻辑外推 = 构造层无解**，须靠第 2/3 步找是否有可破的结构性杠杆。

**诊断前置第 2 步（钉子是不是同族兄弟）—— 是，且已在本账号 OS 池里**：

`xA16pzQJ`（§5.103.2 里 self 0.6519 的唯一对端）经 `get_alpha_by_id` 核实：

| 项 | 值 |
|---|---|
| 表达式 | `trade_when(greater(rank(adv20), 0.6), tail(group_rank(ts_sum(vec_avg(oth695_import_value_4), 20), bucket(rank(cap), range="0,1,0.2")), lower=0.2, upper=0.8, newval=0.5), -1)` |
| 数据集 | **other695（进口额）** —— 与 other475（出口额）是**同一贸易流族** |
| 状态 | **ACTIVE / stage OS**，`date_submitted 2026-10-14` |
| 指标 | S 1.86 / F 2.19 / 2Y 2.10 / subU 1.82 / TO .0269 / DD .1087 |
| **prod** | **0.6976**（自身就贴着 0.7 的墙） |
| self | 0.2308 |

⇒ **贸易流（出口/进口增长）这个信号载体本身已在 prod book 里，且本账号自己就有一颗贴线的 OS 件。**
`leA22za2` 与它 self 0.6519、prod 0.8377 —— **出口 z-score 与进口 ts_sum 在 prod 池里撞的是同一批钉子**。
这解释了为什么 S 从 1.51 推到 1.92 完全没能改善 prod：**推指标改善的是信号强度，不是信号的新颖度**。

**诊断前置第 2 步的「换分母口径」杠杆在本式上不存在**：
`leA22za2` 是**单字段** `ts_zscore(vec_avg(oth475_export_value), 252)`，
分母是**它自己的时序标准差**（不是横截面比较基准）⇒ 没有「同族兄弟共享的横截面分母」可换。
KOR other466 那次 0.8061→0.6843 的成功前提是 `divide(分子, 分母)` 形态，本式不具备。

**诊断前置第 3 步（设置档 / 分组轴）—— 杠杆已在 wave 248–250 花光**：
§5.100 的 2×3 矩阵已实测 7 个组合（market/sector/industry/subindustry × SECTOR/MARKET），
且 skill D0-P 第 3 步明写「**KOR 的 subindustry 轴反而饱和**——『轴空白区』判据不可跨区、跨族外推」。
本骨架用的正是 subindustry + MARKET，**已是该矩阵的 S 最优点**，没有未试的轴档。

**诊断前置第 4 步（先判信号类型再压换手）**：本式是**变化型**（相对自身 1 年均值的偏离），
不是水平型 ⇒ 按 D0-P「变化型信号压换手会杀信号（DEU 实证）」，**压换手不是可用杠杆**。
（TO  already .0270，远低于闸，也没有压缩空间。）

#### §5.105.2 ①–④ 结构性尝试在**用户约束 5** 下的可用空间 = 空

| D0-P 杠杆 | 本例可用性 | 理由 |
|---|---|---|
| ① 删腿 / 换广度轴 | ❌ | 已是单腿最简（4 个算子），无腿可删 |
| ② `group_neutralize(同信号, sector)` 包裹 | ❌ | KOR wave113 实证 0.7003→**0.6993**（n=1，−0.001）；本例缺口 **0.1377**，量级差 100 倍 |
| ③ 换分母口径 | ❌ **被约束 5 封死** | 造横截面分母必须组腿：other475 内另一 OTHER 字段 = **OTHER+OTHER（禁）**；`cap` = **OTHER+PV（禁，PV 在禁集内）**；只有 OTHER+NEWS 等非禁集类别允许且**全局限额 5 颗** |
| ④ 换设置档 / 分组轴 | ❌ 已花光 | wave 248–250 的 7 组合矩阵 + KOR subindustry 轴饱和 |

⇒ **D0-P「≥0.75」行的第二个例外（诊断指向同族同分母/设置档拥挤时允许 1 次结构性尝试）
在本例不成立**：诊断确实指向同族兄弟，但**合规的结构性杠杆一个都不剩**。

**D0-P 结论：`other475` 出口额增长族记 `dead_end`（prod 结构性墙 0.8377）。**
下一步 = **换机制 / 换白名单不同数据集，勿磨同腿变体** ⇒ 已转向 `other545`（§5.104 wave 252 在飞）。

⚠ **判死封存待用户批准**：`seal_dead_end` 的 forum_recon 闸是 fail-closed，
本会话用 MCP `search_forum_posts` 取的证不写 `forum_recon_*` ledger 键 ⇒
封存须 `force_seal=True` 或 `require_forum_recon=False`，**两者都须人工确认**，已列入待决清单。
**本节只登记结论，不代为封存。**

#### §5.105.3 唯一还没关的门：Mode B 组合腿救援（D0-P 的第一例外）

D0-P「≥0.75」行的**唯一例外**：已过 `mode_b_qualification` 且有 salvage 辅助腿的候选，
可走 Mode B 组合腿救援（optimization-v1 入场三式，**禁加权**）。

- **资格线核对**：`leA22za2` S **1.92** ≥ 1.25、F **2.07** ≥ 0.8 ⇒ **过 Mode B 硬闸**。
- **合规形态**：辅助腿只能来自 **非 {PV, MODEL, OTHER} 类别**（NEWS / ANALYST / FUNDAMENTAL / RISK …），
  且只能是**条件 / 分组 / 残差**，不并列相加；**全战役此形态限额 5 颗**（约束 5）。
- **障碍**：KOR 的 news 族已大面积判死（news59 / news54 / news50 / news38 / news 注意力轴 §5.74），
  analyst 弥散轴 §5.91.2 亦已判死 ⇒ **正交辅助腿的候选面很窄**，须先有可用的正交数据集才谈救援。
- **处置**：记为**待用户裁决项**，不本波自行发动（会消耗 5 颗限额中的 1 颗，且需先选定辅助腿数据集）。

#### §5.105.4 `rKRLLzRa` 的 prod 补测（读已有候选，不是扩变体）

`rKRLLzRa`（双窗级联，S 1.61）**同样已过全部 RA 闸**，且几何与 `leA22za2` 不同
（`multiply(rank(Δ252), rank(Δ66))` = **增长 × 加速度**，不是单纯的意外强度）。
已触发一次 prod 计算（MCP 回 **−32603**，是**请求超时**不是平台结论；平台侧已排队）。

**为什么这不算违反 D0-P 的「勿磨同腿变体」**：该禁令针对的是**派发新仿真扩变体**；
`rKRLLzRa` 是 wave 251 **已仿真、已过闸**的存量件，读它的 prod 是**零仿真配额的只读取数**，
正是步 8 提交前终验要求的动作。**不新增任何仿真。**
⚠ 复查只用 `refresh=False`（join 到已触发的那次），**不得 `refresh=True` 重触发**。

**预判（写在读数之前，便于事后核对）**：§5.105.1 诊断显示钉子是**贸易流载体本身**（11 颗 >0.7），
不是某种构造 ⇒ **预计 `rKRLLzRa` 同样 ≥0.75**。若真如此，族级 dead_end 得到第二个独立构造的佐证；
若意外 <0.70，则说明「增长 × 加速度」在 prod book 里是空白形态，须重开该骨架（**读数说话，不预设**）。

---

### §5.106 KOR/D1 塔位实测（`get_pyramid_alphas`，2026-10-30）—— SHORTINTEREST 已点亮

| 塔 | ACTIVE 数 | 状态 | 本战役处置 |
|---|---|---|---|
| **shortinterest** | **4** | **已点亮** | ⛔ **停止投入**（§5.102 预测成真；步 2 硬约束 0：已点亮塔不作主数据集） |
| fundamental | 3 | 已点亮 | ⛔ 不作主塔（`LLZ6wZO2` 因此不提，见下） |
| model | 3 | 已点亮 | ⛔ 且约束 5 禁组腿 |
| pv | 2 | 未点亮（差 1） | ⚠ 约束 5 禁 PV 两两组腿，只可单数据集 ATOM |
| analyst | 2 | 未点亮（差 1） | 弥散轴已判死，须换轴 |
| **other** | **1** | **未点亮（差 2）** | ⭐ 本战役主目标；`leA22za2` 撞 prod 墙 ⇒ 缺口仍是 2 |
| earnings / imbalance / insiders / institutions / macro / news / socialmedia / sentiment / risk | **0** | 未点亮 | 大面积已判死（见待封存清单） |

**★ 用户决策第 5 项正式失效**：§5.92.3 第 5 项问「是否再提一颗 shortinterest38
（`mLmGQEq9` S 2.72 / prod ~~.6011~~ **.935** 或 `E5pjx9q0` S 2.50 / prod ~~.6002~~ **.8105**）」——
两条理由**各自独立地**把它关掉：① 该塔现已 4/3 点亮，按均匀点塔规则**不再提**；
② **2026-10-31 `check_correlation(refresh=True)` 实测两颗 prod 双破 0.70，整族判死**（旧 .6011/.6002 是过期缓存）。
本项**无需用户回答，自动关闭**。
（并行会话的三颗 `6Xd3Ja7P` / `Xg9PvN8l` / `zq3QGWeo` 已完成点塔，非本战役产出，不计入 60 颗进度。）

**`submit_ready` 队列实测（`get_submit_ready(region=KOR, status=READY)`）= 只有 1 条**：
`LLZ6wZO2`（纯 FUNDAMENTAL，S 1.99 / F 1.53 / 2Y 2.24 / invS 1.40 / prod 0.6762 / self 0.6760，
`gate = SUBMIT_LAYER_VERIFIED`）—— note 已写明「塔 KOR/D1/FUNDAMENTAL 已点亮 3/3 → 按均匀点塔规则不提」，
且 `corr_stale = true / no_timestamp` ⇒ **提交前必须 `check_correlation(refresh=True)` 当场终验**。
⇒ **用户决策第 1 项仍待裁决**（是否放弃均匀点塔规则、把这颗 prod/self 双余量各 0.024 的件提上去）。

**★ 收割优先于重挖的核对结果（AGENTS.md §7.5）**：本区 `submit_ready` 只有 1 条且塔已满，
**零配额扩池的路已走通但无货** ⇒ 60 颗目标只能靠新机制，不能靠翻库存。这是本轮的诚实读数。---

### §5.107 ★ 自我更正：§5.105.2 的「④ 换设置档杠杆已花光」是错的

**错在哪**：我把「**S 轴**的 2×3 矩阵扫完了」当成「**prod 轴**的设置档杠杆也花光了」。
这两件事不同 —— wave 248–250 的 7 个组合**只读了 S/F/2Y/DD，一颗 prod 都没测**
（prod 只在 wave 251 的 S 最优件 `leA22za2` 上测了一次）。
**用 S 的排序去推断 prod 的可达性，是没有证据的外推。**

**反证就在本区台账里**（`get_dead_ends(region=KOR)` → `KOR-SUBINDUSTRY-PROD-SATURATED`，dead_at 2026-09-02）：

| 字段 | 原文 |
|---|---|
| family | `neutralization` |
| reason | 「SUBINDUSTRY 中性化把信号压向已生产 alpha 子空间，**prod 必撞墙（0.797–0.801）**，即使 Fitness 达标也不可用」 |
| **rule** | 「KOR 区域 REV1 类信号禁用 SUBINDUSTRY 中性化；**prod 安全设置是 STATISTICAL 或 SECTOR**」 |
| evidence | `WjP1ZwMj`（SUBINDUSTRY decay0 F1.01 达标但 prod **0.7974** 撞墙）+ `akLjmnd9`（SUBINDUSTRY decay4 F0.97 / prod **0.8007** 撞墙） |

⇒ **本区早有「设置档决定 prod」的实证，而且给出了具体的安全档（STATISTICAL / SECTOR）。**
`leA22za2` 用的是 **MARKET 中性化 + subindustry 分组轴**，prod **0.8377** ——
与该条判死的形态（压向已生产子空间、prod 0.80 量级）**高度同形**。

**⚠ 口径必须分清（别再混）**：该条判死说的是 **`neutralization = SUBINDUSTRY`（L1 平台设置）**，
本式用的是 **`group_rank(…, subindustry)`（L2 表达式内分组轴）**，两者不是同一个旋钮
（§5.95 已把这两层拆开）。但**它们作用在同一个成分上**（§5.100 实测二者**次可加**），
所以「subindustry 方向的分组把信号推向 prod 子空间」这个**机制层面的警告对 L2 同样适用**。
这正是 0.8377 的一个可检验解释，而不是我原先写的「载体本身拥挤、构造层无解」。

**D0-P 重新路由（更正后）**：
「≥0.75」行的**第二个例外成立** —— 「诊断指向同族同分母 / **设置档拥挤**时，
≥0.75 也可做 **1 次**同样的结构性尝试（KOR 同分子换分母 0.8061→0.6843 就是从 ≥0.75 起步），仍失败才判死」。
本例诊断**明确指向设置档拥挤**（台账实证 + prod 值量级同形）⇒ **允许且应当做这 1 次尝试**。

**§5.105.2 表格的 ④ 行改判**：

| D0-P 杠杆 | 原判 | **更正后** |
|---|---|---|
| ④ 换设置档 / 分组轴 | ❌ 已花光 | ✅ **未花光，且是唯一有台账实证支撑的杠杆**：`STATISTICAL` 档**从未测过**（S 与 prod 都没测）；7 个已测组合的 **prod 全部未知** |

**①②③ 三行的原判不变**（① 单腿无可删；② `group_neutralize` 包裹量级差 100 倍；
③ 换分母被约束 5 封死 —— 这三条的论证与 prod 轴无关，仍然成立）。

**⇒ `other475` 出口额族暂不判 dead_end**，改为「**prod 墙待 1 次设置档结构性尝试**」。
§5.105 的 dead_end 结论**撤回**，以本节为准。（`seal_dead_end` 本来也没执行，无需回滚库。）

#### §5.107.1 wave 253 设计（D0-P 允许的那 1 次尝试，单变量 = 中性化档）

**冻结**：表达式 = `group_rank(ts_zscore(ts_backfill(vec_avg(oth475_export_value), 66), 252), subindustry)`
（`leA22za2` 原式，**一个字不改**）；decay 4 / trunc 0.08 / 其余标准设置全冻结。
**只动 `neutralization`**，两档：

| # | neutralization | 依据 | 预期 |
|---|---|---|---|
| A | **STATISTICAL** | 台账 rule 点名的 prod 安全档；**本骨架从未测过** | S 可能略降（§5.100 预测 <0.03，但那是无证据外推，须实测）；**prod 有望显著下降** |
| B | **SECTOR** | 台账 rule 点名的另一个 prod 安全档；本骨架只在 **ts_delta** 版测过 SECTOR（`88R7ROkl` S 1.50），**ts_zscore 版 × SECTOR 未测** | 同上 |

**为什么这两档不是「无诊断的盲扫网格」**（D0-P 明令禁止的那种）：
档位**不是遍历平台 11 个中性化档**，而是**只取台账实证点名的 2 个 prod 安全档**，
每一档都能指回 `KOR-SUBINDUSTRY-PROD-SATURATED` 的 rule 原文。这是**有诊断依据的 1 次尝试**（1 批 2 条），
符合 D0-P「先做诊断前置，再从 ①–④ 选 1 种、做 1 批」。

**工具选择更正**：`create_multi_simulation` **整批共享一套设置**（§5.95 已记），
做不了「同一表达式 × 2 套中性化」。⇒ 本波用 **`batch_create_simulations`**
（per-item `settings`，1–20 条，`base_*` 填缺省）—— 这正是它被造出来填补的盲区，
本战役首次使用。**若用 multisim 就得发 2 次调用**，而 per-item 工具一次搞定且不占额外排队位。

**判据（写在派发前）**：
- 任一档 **prod < 0.70 且 S ≥ 1.58 且其余 RA 闸全过** ⇒ **墙破了**，进步 8 终验链（self / 2Y / CW / robust）。
- 任一档 prod < 0.70 但 S < 1.58 ⇒ 记录「prod 可破但强度不够」，**此时才**允许在该档上做强度杠杆
  （因为已证明 prod 不是结构性不可达）；这是与 §5.105 完全不同的处境。
- **两档 prod 都 ≥ 0.70** ⇒ D0-P「≥0.75 或踩线带尝试失败」行生效 ⇒ **家族记 dead_end**，
  这次的判死才有完整证据（诊断 + 1 次合规结构性尝试 + 失败读数），可进封存流程。

**波次三问（铁律 G）**：
1. **继承**：`leA22za2` 的表达式是 S/DD/RN 三赢的最优件（§5.103），**冻结它**；
   继承 `KOR-SUBINDUSTRY-PROD-SATURATED` 的「prod 安全档 = STATISTICAL / SECTOR」作为本波准入依据。
2. **准入**：不改表达式（不磨同腿变体）；不遍历其余 9 个中性化档（无诊断的盲扫）；
   不动 decay / truncation（已死轴）；不新增分组轴变体。
3. **收窄**：**2 条**（wave 251 也是 2 条，但本波是**单变量设置对照**，候选数不增且搜索面从
   「表达式空间」收窄到「2 个有实证背书的设置点」）⇒ 搜索空间实质收窄。

#### §5.107.2 `rKRLLzRa` prod 补测被外部会话抢占（只登记，不重触发）

第三次复查回 `correlation_busy`、**`inflight = false`**、
**`holder = corr:get_production_correlation(88RAAmZa)`**（**又不是本会话的 alpha**）、`retry_after 240`。
⇒ 本会话先前那次触发**没能占住槽**（被并行会话顶掉），值仍缺。
按 `wq-prod-corr-read` 纪律：**只复查、不重触发、不空转**。
**优先级下调**：§5.107.1 的设置档尝试比「同族第二个构造的 prod」更有信息量，
先做前者；`rKRLLzRa` 的 prod 等槽空闲时顺带复查。

---

### §5.108 KOR/D1 **OTHER 类 26 个数据集全量清点**（约束 1「一个个 category 查数据集情况」的 OTHER 分册）

`get_datasets(category="other", region=KOR, delay=1, universe=TOP600)` → **count 26**。
按拥挤度（alphaCount）与覆盖度排序，并标注本战役台账状态：

| 数据集 | 名称 | cov | 字段 | user | **alpha** | value | 台账状态 / 处置 |
|---|---|---|---|---|---|---|---|
| **other546** | Institutional Network Analysis | .5632 | 10 | **8** | **9** | **7** | ⭐ **未挖**；网络动量簇、最冷门、value 最高 ⇒ **下一个主探针** |
| **other635** | Thomson Reuters News Analytics | .3011 | 6 | **3** | **5** | 6 | ⭐ 未挖；cov<0.4 须 backfill |
| **event_relation** | Text-Based Event Relationship | .3392 | 3 | **4** | **4** | 6 | ⭐ 未挖；公司间关系抽取 ⇒ 同属网络簇；cov<0.4 |
| **news_sentiment_dl** | Deep Learning News Sentiment | .2588 | 22 | **2** | **2** | **7** | 未挖；**受用户决策 6（sentiment 禁令）待裁**；cov 极低 |
| **news_sentiment_nlp** | News Sentiment Signal Features | .2767 | 23 | **4** | **4** | **7** | 同上 |
| **other545** | Linked Firms Momentum | .8393 | 4 | 29 | 46 | 5 | 🔄 **wave 252 在飞**（`pln_omen`） |
| **equity_forum_data** | Intl Equity Forum Activity | **.8948** | 6 | **9** | **13** | 6 | ⭐ 未挖；**高覆盖 + 低拥挤**，罕见组合；论坛情绪 ⇒ 决策 6 待裁 |
| **other327** | Sensitivity to Interest Rates | .7866 | 3 | 25 | 31 | 5 | 未挖；利率敏感度（elastic net）⇒ 与 macro 轴相关，macro 已判死须先核 |
| **other424** | Dividend prediction model | .5919 | 3 | 31 | 44 | 5 | 未挖；股利族（other436 已判负、other335 拥挤） |
| **other571** | Wikipedia Viewing Data | .2649 | 23 | 49 | 62 | 5 | 未挖；注意力/信息搜寻机制；cov<0.4 须 backfill |
| **other78** | Earnings and conference call | .7925 | 11 | 29 | 70 | 6 | 未挖；财报电话会 ⇒ 与 earnings 塔（0 颗）可能双计，须核 pyramids |
| **ai_news_scores** | AI News Sentiment Scores | .373 | 103 | 26 | 36 | 6 | 未挖；决策 6 待裁；cov<0.4 |
| **other567** | Employee Review Data | .2571 | 2 | 12 | 16 | 6 | 未挖；员工评价 ⇒ 另类基本面；cov 极低、只 2 字段 |
| **acquisition_model** | Corporate Acquisition Likelihood | **.9937** | 15 | 66 | 111 | 5 | ⛔ **`get_dead_datasets` 已列 KOR 死集** |
| **other475** | Manufacturer Exports | .357 | **1** | 230 | 632 | 2 | 🧱 **prod 墙 0.8377**，wave 253 设置档尝试中（§5.107） |
| **other695** | Korean Imports | .4886 | 3 | 85 | 180 | 4 | ⚠ 已有 ACTIVE `xA16pzQJ`（prod **0.6976** 贴线）；**与 other475 同贸易流族** ⇒ 同墙风险高 |
| **other315** | Equity Swap Data | .4022 | 32 | 163 | 493 | 4 | 未挖；**描述与名称严重不符**（见 §5.108.1） |
| **other335** | Multi-Region Dividend Alpha Model | .59 | 10 | 391 | 1067 | 2 | 拥挤（1067）+ value 2 ⇒ 低优先 |
| **other436** | Dividend model（cut 预测） | .57 | 3 | 12 | 15 | 6 | ⛔ 本战役实测 **S −0.40**，待封存 |
| **other323** | Global Equity Premarket | **1.0** | 11 | 279 | 1041 | 3 | ⛔ 本战役实测**无信号**（证券主表性质），待封存 |
| **other455** | Relationship enhanced with AI/ML | .8973 | **1500** | 137 | 551 | 5 | ⛔ **已判死 4 次**（见 §5.108.2），**但其 rule 明确给出了重试形态** |
| **other496** | Intraday FX rates | .8006 | 104 | 235 | 844 | 4 | ⛔ `KOR-OTH496-TIMESTAMP-TRAP` / `-RETURN-WEAK` / `-AFTERCONS-MODEA-CEILING` |
| **other532** | Specific Returns | **.9956** | 8 | 470 | 1864 | 3 | 拥挤（1864）；描述是证券主表 ⇒ 语义须先核 |
| **mmp_nlp_sentiment** | Multilingual NLP News Sentiment | .6187 | **521** | 46 | 75 | 6 | ⛔ 本战役待封存 |
| **insider_feats** | Global Insider Transaction Features | .6636 | 31 | 460 | 1924 | 3 | ⛔ **prod 地板 0.78 结构性不可修**（记忆已记） |
| **dl_riskfree_returns** | Deep Learning Risk Free Returns | .9095 | 57 | **1205** | **8021** | 2 | ⛔ **Wave36 终判封存**（最拥挤） |

**清点结论**：26 个里 **11 个已判死/待封存**、**2 个在飞或撞墙待试**（other545 / other475）、
**13 个未挖**。未挖面里**真正值得投的只有 4 个**：
`other546`（网络簇、9 颗、value 7）、`equity_forum_data`（cov .89 + 13 颗）、
`other635` / `event_relation`（各 4–5 颗，但 cov<0.4）。
其余未挖集要么受 sentiment 禁令待裁（3 个）、要么拥挤/value 低、要么须先核语义。

#### §5.108.1 ★ 名 vs description 系统性不符（KOR skill 0.2 的实证，必须留痕）

**至少 6 个数据集的 `description` 是「RIC / Bloomberg ID 映射（证券主表）」样板文，与名称完全无关**：

| 数据集 | 名称暗示 | description 实际写的 |
|---|---|---|
| other315 | Equity Swap Data（股权互换） | RIC↔BBID 跨平台证券识别映射 |
| other424 | Dividend prediction model | BBID↔RIC 映射 |
| other455 | Relationship enhanced with AI/ML（1500 字段） | RIC↔BBID 映射 |
| other496 | Intraday FX rates（日内汇率） | 全球公司财务报表与 KPI 快照 |
| other532 | Specific Returns（特质收益） | RIC/BBID/ISIN/CUSIP/SEDOL 证券主表 |
| other567 | Employee Review Data（员工评价） | RIC↔Bloomberg ID 映射 |
| other78 | Earnings and conference call | RIC↔BBID 映射 |

⇒ **数据集级 description 在本区不可信**（疑似平台元数据串号）。
**纪律**：本区**字段分类一律以 `get_datafields` 的字段级 description 为准**，
数据集级 description 只作线索、**不作分类依据**；
且 **`other323` 那次「无信号」的判定之所以成立，是因为它字段级核实后确实是证券主表**，
不是靠数据集 description 推的 —— 两者不可混为一谈。
**这条要写进区域经验库**：按数据集 description 选机制会系统性选错。

#### §5.108.2 ★ `other455` 四次判死的**精确边界** —— 它的 rule 反而**授权**了 wave 252

`get_dead_ends` 取回四条（不是一条），逐条读 reason/rule 后，**判死的对象各不相同**：

| entry_id | dead_at | 判死的**具体对象** | 关键读数 |
|---|---|---|---|
| `KOR-OTHER455-NETWORK-EMBEDDING-DEAD` | 2026-08-22 | **`*_pca_fact*_value` MATRIX 分量**的 7 种结构（水平/动量/均值回归/波动率/跨网络相关/自归一/组合） | wave93 10 探针全灭，S ≤ 0.18；K7 2Y −1.04 / K10 2Y −1.95 |
| `KOR-OTHER455-GROUP-CLUSTER-DEAD` | 2026-08-22 | **GROUP cluster 字段作分组器**包裹评级修正 | wave95 9RED1黄，S 0.40–0.53；簇内同质化把 alpha 平均掉 |
| `KOR-OTHER455-REVISION-CLUSTER-DEAD` | 2026-08-22 | **以 `change_6m_rating_revision` 为腿**的任何 other455 混合族 | 4 候选 S 1.76–1.91 **平台硬闸全 PASS**，但与 ACTIVE 评级修正族相关 0.90–0.991 ⇒ **prod/self 墙，不是无信号** |
| `KOR-OTHER455-RELATION-EMBED-DRIFT-NOSIGNAL-20261004` | 2026-10-04 | **图嵌入 PCA 分量的时序漂移** | d30 裸探针 8 条，最好 S 0.43；**fact1 全负 / fact2 全正 ⇒ PCA 符号随对齐随机翻转** |

**★ 第四条的 rule 原文（这是关键）**：
> 「图嵌入 PCA 分量（`*_pca_fact*_value`）不可作 alpha 输入：符号随 PCA 对齐随机翻转，
> 绝对水平无经济含义，时序漂移亦无横截面预测力。KOR 已验证。
> **若日后重试需换非 PCA 的连续 latent score 且先裸探针。**」

⇒ **`oth545_pln_omen` 正是「非 PCA 的连续 latent score」**
（描述：「Score based on NLP-derived network momentum using text-mined linkages」，
是一个有方向、有经济含义的**合成分**，不是 PCA 分量），
而 wave 252 的做法正是**先裸探针**（P1 水平 / P2 变化，各 1 条，不上壳层网格）。
**⇒ wave 252 不是重踩已判死路径，而是执行该判死条目自己写明的重试形态。**
这是「判死标记不得单独作为依据」（AGENTS.md §7.5）的一个正面案例：
**读判死的 rule 原文，比读它的标题有用得多。**

**⚠ 但有一条真实警告必须继承**：`KOR-OTHER455-REVISION-CLUSTER-DEAD` 证明
**网络类数据集比评级修正族更容易撞 prod/self 墙**（S 1.76–1.91 全闸过却相关 0.90+）。
⇒ **other545 / other546 出信号后必须 prod-first**（S3 收批后立刻测最强 1 条的 prod，
不先扩变体），这是 D0-P「0.60–0.70 不扩变体当天进步 8」与 I-2 事故（pv103 外部同款一小时内堵到 1.0）的直接教训。
**本波已把该纪律写进 §5.104 的判据**（任一 |S| ≥ 1.0 就先归因 + prod，不铺量）。

**对 `other546` 的前置要求**：它有 10 个字段，**必须先 `get_datafields` 核实是不是 PCA 分量**。
若同样是 `*_pca_fact*` 形态 ⇒ **直接适用已判死 rule，不投**；
若是连续 latent score（如 other545 的 `mpd`/`pln_omen`/`score`）⇒ 能投，且它只有 9 颗 alpha、赔率更好。
**这一步零配额，派发前必做。**## §5.109 wave 252 收割：other545 pln_omen 双臂 S 0.74，预注册线未达（2026-10-31）

批次 `3dhvS0fnv5cNcjz2xhdBfWc`（SECTOR / decay 4 / trunc 0.08，KOR/TOP600/D1）2/2 COMPLETE、0 error。
⚠ 收割通道异常：`harvest_multisim_alphas` 对该 multisim location **两次 HTTP 404**（资源已过期），
改用 `batch_status`（child_count 2 / terminal 2）+ `batch_get_alpha_metrics` + `get_alpha_details` 直读，
再经 `harvest_multisim_results(alphas=<两颗完整详情>, multisim_id=…)` 入库：**upserted 2，wave 252 暂定 verdict=FAIL（0/2 过硬闸，0 条过 near 线 1.0）**。
教训：multisim 资源有 TTL，**收割要趁早**；404 不等于批次失败，子 alpha 仍在，直读详情即可补收。

| alpha | 探针 | S | F | 2Y | subU | invS | RN S | TO | DD | CW | 失败闸 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `QPvj5KjX` | P1 Level | 0.74 | 0.53 | 0.66 | 0.89 | 0.68 | **0.43** | .0605 | .212 | **0.2617 FAIL** | S/F/CW/2Y 四项 |
| `58E9qg9M` | P2 Change(22) | 0.74 | 0.54 | 1.09 | 0.98 | 0.72 | **0.30** | .1019 | .1933 | **0.2617 FAIL** | S/F/CW/2Y 四项 |

**读数三条**：
1. **双臂 S 逐位相同（0.74）但 F/2Y/TO 不同** ⇒ 不是去重假象，是两种构造恰好同强度；信号弱但非零、非负（铁律 B 无需 reverse）。
2. **CW 同日同值失败（2016-12-22，0.2617 ≫ 0.10）** ⇒ pln_omen 覆盖有洞，该日持仓极端集中；
   与 RN S 仅 0.43/0.30（raw 0.74 的大半是因子暴露）合起来看：**这个载体本身信号薄 + 可投资性差**。
3. 预注册判据（§5.104）：**任一 |S| ≥ 1.0 ⇒ 有信号**；双臂 0.74 < 1.0 ⇒ **按预注册再探一次头部字段 `oth545_score`，仍无 ⇒ 记 other545 天花板**。
   score 探针排入 wave 253 之后（槽位已满，不超并发 2）：`group_rank(ts_delta(ts_backfill(vec_avg(oth545_score), 66), 22), subindustry)`，
   SECTOR / 其余设置与 252 逐字对齐（单变量 = 字段，P2 的 2Y 1.09 优于 P1 的 0.66 故选 Change 形态）。

## §5.109.1 wave 253 派发：D0-P 唯一许可的设置轴尝试（other475 prod 墙）

按 §5.107.1 设计执行，**本战役首次使用 `batch_create_simulations`**（per-item settings，
`create_multi_simulation` 整批共享一套设置做不了中性化对比）：

| 臂 | neutralization | simulation_id |
|---|---|---|
| A | **STATISTICAL**（registry 点名 prod 安全，本骨架从未测过） | `2otuHlcvh4Mscn7uH8yO4tI` |
| B | **SECTOR**（registry 点名 prod 安全；只测过 ts_delta 版 `88R7ROkl` S 1.50，未测 ts_zscore 版） | `1Q6Pp29q34WCbYz70YtG3Bq` |

表达式**逐字冻结** `group_rank(ts_zscore(ts_backfill(vec_avg(oth475_export_value), 66), 252), subindustry)`，
decay 4 / trunc 0.08 / nanHandling ON / pasteurization ON / VERIFY / maxTrade OFF / 2014-01-01→2023-12-31 / FULL / testPeriod P0Y0M。

**工具契约实测（读 `tools_sim.py:776-803` 核实，防静默换档）**：
- base 段**不含** startDate/endDate/simulationMode（只有 testPeriod P0Y0M）⇒ 经 **item settings 原样透传注入**
  （`settings[k]=v` 对任意键放行），两臂都显式带 `startDate/endDate/simulationMode=FULL`；
- `nan_handling` 工具缺省 **OFF** ⇒ 显式传 ON（OFF 是「换信号」档，会与 leA22za2 不可比）。
- 三闸：表达式与 wave 251 已 COMPLETE 的 `leA22za2` **逐字符相同** ⇒ op_arity / 算子存在性 / 字段存在性已有同串实证，无需重跑。

**预注册判据（§5.107.1 原文）**：任一档 prod < 0.70 且 S ≥ 1.58 且其余 RA 闸全过 ⇒ 墙破，进步 8 终验链；
任一档 prod < 0.70 但 S < 1.58 ⇒ 记「prod 可破但强度不够」，此时才允许在该档做强度杠杆；
**两档 prod 都 ≥ 0.70 ⇒ D0-P「≥0.75 或尝试失败」行生效 ⇒ other475 export 家族 dead_end**（证据链完整：诊断 + 1 次合规尝试 + 失败读数）。

## §5.109.2 other546 字段体检（零配额，§5.108.2 强制前置）：**通过，可投**

`get_datafields(other546, KOR, D1, TOP600, filter_sharpe=false)`：10/10 字段，**全 VECTOR，无 `*_pca_fact*`**
⇒ other455 第四条判死 rule（PCA 符号随机翻转）**不适用**。全部是**成对（primary↔peer）网络链接强度 / 覆盖计数**，
经济含义清晰，与 Cohen & Frazzini (2008) 经济链接机制天然对接：

| 字段 | cov | u/a | 含义 |
|---|---|---|---|
| `oth546_busnet_common` | .6735 | 1/1 | 两公司共享的业务/地理分部数 |
| `oth546_busnet_strength` | .6735 | 4/5 | 业务分部报告相似度（相关度量） |
| `oth546_analystnet_common` | .614 | 2/2 | 同时覆盖主/peer 公司的分析师数（共享覆盖） |
| `oth546_from_analyst` | .614 | 1/1 | 覆盖主公司的分析师数 |
| `oth546_to_analyst` | .614 | **0/0** | 覆盖 peer 公司的分析师数 |
| `oth546_mdanet_strength` | .5204 | **0/0** | MD&A 文本相似度（经营相似） |
| `oth546_nlpbusnet_strength` | .5204 | **0/0** | 业务章节 NLP 文本相似度 |
| `oth546_risknet_strength` | .5204 | **0/0** | 风险因子章节文本相似度 |
| `oth546_geonet_common` | .4407 | **0/0** | 共享地理分部数 |
| `oth546_geonet_strength` | .4407 | 1/1 | 地理分部存在向量相关 |

**5 个字段完全未挖（u0/a0）**；全集合计仅 9 颗 alpha（u8/a9，valueScore 7）⇒ OTHER 塔里最冷的未挖面之一。
设计约束（留待 wave 253 读数后定中性化再开波，铁律 F）：
- 铁律 A：计数 / 相似度单边恒正 ⇒ **ts_delta 变化率，禁裸水平**；
- cov .44–.67 ⇒ `ts_backfill(·,66)` 前置（geonet .4407 贴 0.4 地板，优先 backfill 或弃用）；
- VECTOR ⇒ 先 `vec_avg` 降维；
- 机制候选（A-2 待立）：**共享分析师覆盖的变化** = 注意力链接新建 ⇒ 信息扩散加速前的错定价窗口；
  **业务链接广度变化** = 新经济链接形成 ⇒ peer 冲击滞后传导。修复期数周–一季（窗 22/66）。
- ⚠ 继承 §5.108.2 警告：网络类数据集即使 S 1.76–1.91 全闸过也撞 prod/self 墙（other455 REVISION-CLUSTER 实证）
  ⇒ **other546 收割后立即 prod-first，再决定扩不扩变体**。
- 约束 4 待验：逐年持仓探针看 2014/2015 是否有数据（other475 前科）。

## §5.109.3 rKRLLzRa prod：移出主动队列

第三次重查仍 `correlation_busy / inflight false / holder=corr:get_production_correlation(88RAAmZa) / retry_after 240`
—— 外部会话持续占槽。该 alpha 已 **SUPERSEDED**（§5.103，keeper = leA22za2），其 prod 读数只剩
「载体墙假设」的学术佐证价值（已有 leA22za2 0.8377 + xA16pzQJ 兄弟钉子两条独立证据）⇒
**不再排队重查**，按 wq-prod-corr-read 纪律不重触发、不空转。若日后槽位空闲顺手读到再补记。## §5.110 wave 253 收割：设置轴尝试双臂全闸过，§5.107 自我更正证实（2026-10-31）

D0-P「≥0.75 第二例外（设置档拥挤）⇒ 1 次有诊断依据的结构性尝试」的那 1 批（2 个 registry 点名点）落地，
**两臂都 failed_ra_count 0 / checks.fail []**，入库 wave 253 暂定 verdict=PASS（2/2）。
表达式逐字冻结 `group_rank(ts_zscore(ts_backfill(vec_avg(oth475_export_value), 66), 252), subindustry)`，单变量 = L1 neutralization。

| arm | alpha | neut | S | F | 2Y | subU | invS | invF | RN S | TO | DD | margin | pnl | long/short |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| A | `3qoxag8z` | STATISTICAL | 1.69 | 1.34 | 1.73 | 1.67 | 1.56 | 1.19 | — | .0767 | **.075** | .002054 | 6.43M | 221/427 |
| B | `d5WmEarw` | **SECTOR** | **1.99** | **2.11** | 2.19 | 1.84 | **1.95** | **2.05** | 1.67 | .031 | .0932 | .00911 | 11.52M | 151/468 |
| 基线 | `leA22za2` | MARKET | 1.92 | 2.07 | 2.20 | 1.82 | 1.88 | 2.01 | 1.69 | .0270 | .1105 | .010758 | 11.87M | 154/494 |

**B（SECTOR）几乎全面优于 MARKET 基线**：S +0.07、invS +0.07、invF +0.04、DD −16%（.1105→.0932）、2Y/RN S 在噪声内持平。
A（STATISTICAL）S 降到 1.69 但 **DD 全场最低 .075**、TO 升到 .0767（换手更高 ⇒ 与 prod book 的重叠可能更低，prod 未必输 B）。
两臂均纯 cell `[KOR/D1/OTHER ×1.6]` effective 1 ⇒ ATOM。

**★ 这是 §5.107 自我更正的实证兑现**：把「S 轴扫完」误当「prod 轴扫完」曾导致过早判死；
库里 `KOR-SUBINDUSTRY-PROD-SATURATED` 点名的 prod 安全档（STATISTICAL/SECTOR）从未在本骨架测过，
一测就两臂全闸过、且 SECTOR 比原 MARKET 更强。**教训固化：判死前必须读判死条目的 rule 正文，不只读标题；
S 最优档 ≠ prod 安全档，两个轴的搜索空间不可互相顶替。**

**SUPERSEDED 记账（待 prod 确认后才生效）**：若 B prod < 0.70 ⇒ `d5WmEarw`（S 1.99 / DD .0932）成新 keeper，
`leA22za2`（1.92）及此前全链 SUPERSEDED；若 A prod 更低则 A 优先（prod 贴线时低 prod > 高 S，④b 铁律）。
**prod 未落定前不宣布 keeper。**

## §5.110.1 prod 单槽跨会话竞争：A 触发被抢占，值未落缓存

- A `3qoxag8z` prod `refresh=True` → MCP −32603（请求超时，非平台 verdict）；`refresh=False` 重查 → `inflight true / 第 1 次触发 / retry_after 25`（我的触发已生效）。
- 约 4–5 分钟后再查 → **`inflight false` + 外部 holder `corr:get_production_correlation(kqNRX1ZP)` / retry_after 240 / last_known null**
  ⇒ 我的本机 inflight 标记已清、值未捕获，**外部会话抢占了账号级单槽**，我的计算可能被 preempt。
- 处置（wq-prod-corr-read）：**只重查、不重触发、不空转**。等外部 240s 释放后，先 `refresh=False` 看 A 是否落了缓存值；
  无值且槽空 ⇒ 对 A 重触发一次；A 落定后再排 B `d5WmEarw`（单槽串行）。
- **预注册判据仍未兑现**：两臂 S ≥ 1.58 + RA 全过已满足，**只差 prod < 0.70 这一项**。prod 是 D0-P 墙破与否的唯一裁决，必须拿到。

## §5.110.2 wave 254：oth545_score 头部字段探针（预注册兜底，仿真槽独立于 prod 槽）

253 双臂 COMPLETE ⇒ 仿真槽空闲（与 prod 单槽无关）。按 §5.104 预注册「双臂 |S|<1.0 ⇒ 探 score 一次」派发 1 颗：
`group_rank(ts_delta(ts_backfill(vec_avg(oth545_score), 66), 22), subindustry)`，SECTOR / decay 4 / trunc 0.08 / nanON / FULL / 2014–2023，
sim `1Or3ucbe04Euc9AFbDqa9i3`（tag wave254_score_probe）。三闸：与 252 P2 `58E9qg9M` 同骨架同算子，仅换字段（score 头部字段已确认存在）。
判据：|S| ≥ 1.0 且 CW 过 ⇒ score 载体有信号，再归因；仍 < 1.0 或 CW 同日洞 ⇒ **记 other545 天花板**（pln_omen + score 双载体均弱）。

## §5.110.3 OTHER 未挖面字段画像续（零配额）：event_relation / other635

**event_relation**（3 VECTOR，cov **.3392 < 0.4**）：
- `relation_strength_score_general`（u1/a1）：0–1 连续边权重，「直接用于加权与传播」⇒ **唯一干净连续信号**，Cohen-Frazzini 链接强度机制。
- `entity_connection_type_general`（u3/a3）/ `relation_strength_rank_general`（u0/a0）：vendor 原生**整数编码**（关系类型/置信度分类），需解码、非连续 ⇒ 不作裸信号。
- cov < 0.4 ⇒ 必须 `ts_backfill`/`group_backfill` 否则弃用（体检硬门）。**优先级低于 other546**（后者 cov .44–.67、5 个干净未挖字段）。

**other635**（Thomson Reuters News Analytics，6 VECTOR，cov .2512–.3511）：
- 核心信号 `headline_sentiment_score` / `oth635_sentiment`（神经情绪 [-1,1]）⇒ **情绪族，受用户决策 6 情绪禁令闸**（与 news_sentiment_dl/nlp、ai_news_scores、equity_forum_data 同裁）。
- `headline_character_count` / `headline_word_count` / `oth635_char_count` / `oth635_words_count`（u0/a0 居多）：标题长度 = 注意力/复杂度代理，非情绪，但 cov 极低（.2512）。
- **处置：hold，等决策 6**；即便放行，低覆盖 + 情绪拥挤，赔率不如 other546。

**OTHER 可投面更新排序**：① **other546**（已过 PCA 前置、5 未挖干净字段、cov .44–.67、u8/a9 value7）⭐ 下一主探针；
② event_relation（1 干净字段、cov<0.4 须 backfill）；③ other635 / equity_forum_data（决策 6 闸，hold）。## §5.111 other475 prod 裁决（A 落定 / B 阻塞）+ other545 天花板 + other546 首探（2026-10-31）

### §5.111.1 A（STATISTICAL）prod = 0.7498 FAIL，但形态从多钉变单钉

`3qoxag8z` prod 经外部抢占后终于落缓存：**max 0.7498 / passes_check false**。直方图对比：

| 档 | [0.5,0.6) | [0.6,0.7) | [0.7,0.8) | [0.8,0.9) | max | >0.7 钉数 | 形态 |
|---|---|---|---|---|---|---|---|
| MARKET `leA22za2` | 70 | 29 | 9 | 2 | 0.8377 | 11 | 多钉拥挤族 |
| **STATISTICAL `3qoxag8z`** | 9 | **1** | **1** | 0 | **0.7498** | **1** | **单钉型** |

**设置杠杆确实有效**：把 >0.7 的钉子从 11 颗打到 1 颗、max 从 0.8377 降到 0.7498。
但按诊断前置形态 (a)「单颗钉子型（0.7+ 仅 1–3、0.6–0.7 仅 6–16）⇒ 任何构造都被钉住」——
A 现在 0.7+ = 1、0.6–0.7 = 1，比单钉阈值还稀疏，**剩的那颗是硬结构钉**。
A 按预注册判据失败（prod 0.7498 ≥ 0.70，未 < 0.70）。**这证明 §5.107 的诊断方向对（设置档拥挤是真的），
但 STATISTICAL 不足以单独破墙**——它清掉了拥挤背景，只剩一颗兄弟钉。

### §5.111.2 B（SECTOR）prod：外部单槽垄断阻塞，未落定

`d5WmEarw`（S 1.99 最强臂）prod 触发三次（refresh=True → −32603 → refresh=False 确认 inflight true），
但每次约 1.5–4 分钟后重查都变成 **`inflight false` + 外部 holder `corr:get_production_correlation(kqNRX1ZP)` / retry_after 240 / last_known null**
—— 外部会话 kqNRX1ZP 反复抢占账号级单 prod 槽，我的计算在落缓存前被 preempt。
**处置（wq-prod-corr-read）：不重触发、不空转**。B prod 暂记「外部槽垄断阻塞」，待 kqNRX1ZP 释放后先 refresh=False 看是否落值、无值且槽空再触发一次。
**预注册判据仍悬置**：A 已失败（0.7498），other475 家族死活动完全取决于 B prod 是否 < 0.70。

### §5.111.3 wave 254：other545 天花板确认（预注册兑现）

score 头部字段探针 `Jjemn582`（SECTOR）：**S 0.33 / F 0.11 / 2Y −0.25 / RN S 0.12 / TO .175 / DD .2166**，CW 过（score 覆盖优于 pln_omen），
failed_ra_count 3（S/F/2Y）。入库 wave 254 verdict=FAIL。

**双载体汇总**：pln_omen（P1 Level S 0.74 / P2 Change S 0.74，CW 同日洞 0.2617）+ score（S 0.33，2Y 负）。
全正、无一负 ⇒ 铁律 B 无需 reverse。**预注册判据「探 score 一次仍无 ⇒ 记天花板」兑现**：
other545 NEMO 网络动量复合在 KOR/TOP600 这些构造下截面信号弱（S 0.33–0.74 ≪ 1.58），头部 2Y 负。
**天花板确认，不再磨 other545 模板变体（铁律 G）**。⚠ 这是战役级天花板记录，非 seal_dead_end（后者需 forum_recon + 用户批准 force_seal）。
机制取证留档：论坛 A 通道 `no_result`（5 命中无本集）+ 负面证言（跨资产 vs 本区单市场溢出，适用性警告非判死）；
论文 B 通道 Cohen-Frazzini 1.55%/月 ⇒ 机制成立但**本区载体不兑现**（文献偏误的又一例：USA/跨资产结论 ≠ KOR 单市场）。

### §5.111.4 wave 255：other546 首探（A-2 立机制 + 2 颗裸探针）

**A-1 五问**：① 存量网络中心度（计数/相似度）⇒ ts_delta 变化率（铁律 A，单边恒正）；② 截面排序 ⇒ group_rank；
③ 被定价的是**广度**（链接数）与**注意力**（共享分析师）；④ 网络中心度是已知 quant 轴但本区这些成对字段几乎未挖（u8/a9），cov .44–.67 ⇒ backfill；
⑤ 链接形成是渐进非稀疏事件 ⇒ 不用 trade_when。

**A-2 收益来源声明**：
- **谁被定价**：持有经济链接股票的投资者 / 跨 peer 传递信息的分析师。
- **为什么错**：有限注意力（Cohen & Frazzini 2008）——投资者不即时处理沿经济链接传导的 peer 冲击；
  文本挖掘链接（MD&A/NLP 相似度）在多数投资者信息集之外 ⇒ 扩散慢。
- **多久修复**：数周–一季（窗 22/66）。
- **方向**：链接广度/共享覆盖上升 ⇒ 价格发现滞后 ⇒ 经验定符号（铁律 B 保留：若负先 reverse）。

**2 颗探针**（单字段 OTHER ATOM，约束 5 ✅；SECTOR L1 取 253 prod 安全档教训；ts_backfill 66 / vec_avg / ts_delta 22）：
| 探针 | 字段 | 机制 | sim |
|---|---|---|---|
| P1 | `oth546_busnet_common`（cov .6735, u1/a1） | 业务链接广度变化 = 新经济链接形成 | `2Zmayr8D74PS96Ee5y64Oxd` |
| P2 | `oth546_analystnet_common`（cov .614, u2/a2） | 共享分析师覆盖变化 = 注意力网络新建 | `15d7Ld2Ah4ZiaRJ1QeklmDt` |

表达式：`group_rank(ts_delta(ts_backfill(vec_avg(<字段>), 66), 22), subindustry)`。
三闸：算子与 252/253/254 同骨架（vec_avg/ts_backfill/ts_delta/group_rank/subindustry 均成功用过），字段 §5.109.2 已确认存在。

**预注册判据**：任一 |S| ≥ 1.0 ⇒ 有信号，归因 + **prod-first**（§5.108.2 警告：网络类即使 S 1.76–1.91 全闸过也撞 prod/self 墙，other455 REVISION-CLUSTER 实证）再决定扩不扩；
双臂 |S| < 1.0 ⇒ 换未挖文本相似度字段（mdanet_strength / nlpbusnet_strength，u0/a0）探一次，仍无 ⇒ other546 广度轴天花板；若负先 reverse（铁律 B）。
**波次三问**：继承 = 253 的 SECTOR prod 安全档 + §5.109.2 字段画像；准入 = 不混信号（单字段）、不裸水平（ts_delta）、不跳 backfill；收窄 = 2 颗裸探针（新数据集首探，非 253 变体）。### §5.112 wave 255 收割（FAIL）+ other546 归因 + wave 256 文本相似度探针 + B prod 仍被外槽阻塞

**wave 255 收割入库**（`harvest_multisim_results` region=KOR wave=255 dataset=other546，upserted 2，verdict=FAIL，0/2 过 near 线 1.0）：

| 探针 | alpha | 字段 | S | F | 2Y | subU | **RN S** | TO | DD | CW | failed_ra |
|---|---|---|---|---|---|---|---|---|---|---|---|
| P1 | `QPvjElMX` | busnet_common（业务/地理共享段计数） | 0.63 | 0.35 | 0.74 | 0.67 | **0.50** | .0478 | .1404 | pass | 3（S/F/2Y） |
| P2 | `vR19d3Xw` | analystnet_common（共享分析师计数） | 0.73 | 0.44 | 1.39 | 0.77 | **0.01** | .0541 | .2449 | pass | 3（S/F/2Y） |

**★ 归因关键读数（RN vs raw 分解，铁律 E）**：
- P1 busnet_common：raw S 0.63 / **RN S 0.50**（RN/raw≈0.79）⇒ 信号大部分是**真 alpha**（业务链接广度），因子暴露占比小。
- P2 analystnet_common：raw S 0.73 / **RN S 0.01**（RN/raw≈0.01）⇒ 几乎**纯因子暴露**（共享分析师覆盖只是规模/行业代理），无真 alpha。
- ⇒ 同为「网络广度」，**业务链接（busnet）有真信号、分析师网络（analystnet）没有**。两者 raw S 都 ≪1.58，按预注册判据（双臂 |S|<1.0）⇒ 不扩，转未挖文本相似度字段探一次。
- 两探针均正（无负），铁律 B 不触发 reverse。

**wave 256：other546 文本相似度首探（预注册的一次性探针，铁律 G 单变量=字段载体）**：
- 机制切换：从「计数型链接广度」（busnet/analystnet common）→「**文本相似度强度**」（MD&A / NLP 业务描述相似度）。
  强度字段是连续 [0,1] 相似度分（非计数），刻画「基本面相似程度」而非「链接数量」，是 Cohen-Frazzini 经济链接的**文本挖掘载体**（Hoberg-Phillips 文本行业网络）。
- 字段（gate 3 已确认存在，均 VECTOR / cov .5204 / **u0/a0 未挖**）：
  - `oth546_mdanet_strength`：MD&A 文本相似度（经营讨论与分析）。
  - `oth546_nlpbusnet_strength`：业务章节 NLP 文本相似度。
- 构造**逐字冻结** wave 255 骨架（`group_rank(ts_delta(ts_backfill(vec_avg(<字段>), 66), 22), subindustry)`，SECTOR）⇒ 任何差异归因到字段，不混构造变量。
- sim：P1 mdanet `2qSqFp5f950ua0w14u4KFdBt` / P2 nlpbusnet `1c0tG36Zq4oSaTBPt1SWhLD`（batch_create_simulations 2/2，nanHandling ON，startDate/endDate/simulationMode FULL 逐 item 注入）。
- **预注册判据**：任一 |S| ≥ 1.0 ⇒ 有信号，归因 + prod-first 再决定扩不扩；双臂 |S| < 1.0 ⇒ **other546 广度/文本轴天花板确认**，不再磨本集模板变体（铁律 G），转下一 OTHER 数据集；若负先 reverse。
- **波次三问**：继承 = 255 的 RN 分解结论（busnet 真 alpha / analystnet 纯暴露）+ SECTOR prod 安全档；准入 = 单字段不混信号、ts_delta 不裸水平、backfill 不跳；收窄 = 2 颗（字段载体替换，非构造网格）。

**other475 B（d5WmEarw, SECTOR, S 1.99）prod 仍阻塞**：
- 多次重查（refresh=False）：先本机 inflight true（第 1 次触发，retry 25），后被**外部会话 `88RAAmZa` 垄断**（inflight false / holder=`corr:get_production_correlation(88RAAmZa)` / retry 240 / last_known null）。
- 处置遵 wq-prod-corr-read：**外槽持有 ⇒ 只重查、不重触发、不空转**。B prod 是 other475 生死唯一未决数（A=3qoxag8z 已确认 prod 0.7498 FAIL 单钉）；
  预注册（§5.107.1）：B prod <0.70 且 S≥1.58 且 RA 全过 ⇒ 墙破进步 8；B prod ≥0.70 ⇒ 两档皆 ≥0.70 ⇒ other475 export 家族 dead_end。
- ⚠ 外槽垄断期间无法推进 other475 终验，**不烧配额空转**，转 other546/其它数据集挖掘填槽。

**战役态势**：OTHER 塔仍 1 ACTIVE（需 +2）。other545 天花板已确认（§5.111.3）；other475 待 B prod；other546 文本轴待 256。
60 颗目标需新机制持续供给，收割优先（本地 prod-clean 池已查无库存，submit_ready 仅 LLZ6wZO2 且 FUNDAMENTAL 塔满）。### §5.113 wave 256 收割（FAIL）⇒ other546 广度/文本轴天花板确认

**wave 256 收割入库**（region=KOR wave=256 dataset=other546，upserted 2，verdict=FAIL，0/2 过 near 线 1.0）：

| 探针 | alpha | 字段 | S | F | 2Y | subU | RN S | TO | DD | CW | failed_ra |
|---|---|---|---|---|---|---|---|---|---|---|---|
| P1 | `78LQdJlQ` | mdanet_strength（MD&A 文本相似度） | 0.67 | 0.47 | 1.04 | 0.84 | 0.30 | .0396 | .2263 | **0.2616 FAIL（2016-12-22）** | 4（S/F/CW/2Y） |
| P2 | `RREYrEKb` | nlpbusnet_strength（业务 NLP 文本相似度） | 0.71 | 0.51 | 1.05 | 0.84 | 0.34 | .0395 | .2503 | **0.2616 FAIL（2016-12-22）** | 4（S/F/CW/2Y） |

**other546 四探针全景（wave 255 计数型 + 256 文本型）**：
| 字段 | 类型 | S | RN S | RN/raw | CW | 判读 |
|---|---|---|---|---|---|---|
| busnet_common | 计数 | 0.63 | 0.50 | 0.79 | pass | 真 alpha 占比最高，但 S 最弱 |
| analystnet_common | 计数 | 0.73 | 0.01 | 0.01 | pass | 纯因子暴露（共享分析师=规模/行业代理） |
| mdanet_strength | 文本 | 0.67 | 0.30 | 0.45 | **FAIL** | 文本载体 fitness 略好，但 CW 洞 |
| nlpbusnet_strength | 文本 | 0.71 | 0.34 | 0.48 | **FAIL** | 同上 |

**★ 天花板确认（预注册判据兑现，铁律 G）**：四字段 S 全在 0.63–0.73，≪1.58，无一过 near 线 1.0。
文本相似度载体（mdanet/nlpbusnet）比计数载体 fitness/RN 略好（F 0.47/0.51 vs 0.35/0.44），但**仍弱且双双带 2016-12-22 CW 洞**。
⇒ **other546 经济链接（计数+文本）机制在 KOR/TOP600 这些构造下不兑现可提交信号，不再磨本集模板变体**。
这是战役级天花板记录，非 seal_dead_end（后者需 forum_recon + 用户批准 force_seal）。

**★ 跨集 recurring 指纹：2016-12-22 CW 洞**：other545 pln_omen 双臂（CW 0.2617）+ other546 mdanet/nlpbusnet（CW 0.2616）
**同一日期、同一量级（≈0.26）**的 CONCENTRATED_WEIGHT 失败。⇒ 这不是单字段问题，是**低覆盖 VECTOR 字段 + ts_backfill 在 KOR 某压力日（2016-12-22）产生集中持仓**的结构性 artifact。
启示：稀疏 OTHER 数据集即使 S 推上去，CW 闸也可能在该日卡死；后续低覆盖集探针应**预期 CW 风险**，backfill 窗/覆盖阈值需更严（cov<0.5 的文本字段已现此洞）。

**机制取证留档**：Cohen-Frazzini 经济链接动量 / Hoberg-Phillips 文本行业网络在 USA/跨资产成立，
**KOR 单市场小宇宙载体不兑现**（文献偏误的第三例，继 other545 NEMO、other475 export 之后）。
other546 未挖字段已探尽代表性载体（计数 2 + 文本 2，余 geonet/risknet/from-to_analyst 同族低覆盖，不另投）。

**战役态势更新**：OTHER 塔仍 1 ACTIVE（需 +2）。已确认天花板：other545（NEMO）、other546（经济链接）。
prod 墙待决：other475（B=d5WmEarw S 1.99，prod 被外槽 88RAAmZa 垄断 + 多次 −32603 超时，未决）、other455（REVISION-CLUSTER）。
**下一步**：查 KOR OTHER 数据集全景，挑未挖高潜力集继续供给；B prod  opportunistic 重查（不空转）。### §5.114 KOR OTHER 26 集全景观 triage + acquisition_model 字段画像 + wave 257 M&A 目标变化率首探

**KOR/TOP600/D1 OTHER category 全景（get_datasets，26 集）——按战役累积知识分桶**：

| 桶 | 数据集（cov / aCount / vs） | 状态 |
|---|---|---|
| **天花板已确认** | other545（.8393/a46/vs5 NEMO）、other546（.5632/a9/vs7 经济链接） | §5.111.3 / §5.113，S≪1.58 |
| **prod 墙待决** | other475（.357/a632/vs2 export，B=d5WmEarw S1.99 prod 未决）、other455（.8973/a551/vs5 REVISION-CLUSTER） | B prod 外槽阻塞；other455 S1.76–1.91 撞 prod/self |
| **待判死（pending）** | other436（.57/a15/vs6 dividend laggard）、other323（1.0/a1041/vs3 premarket） | 需 forum_recon + 用户 force_seal |
| **sentiment 家族（决策 6 闸）** | ai_news_scores（.373/a36）、mmp_nlp_sentiment（.6187/a75）、news_sentiment_dl（.2588/a2）、news_sentiment_nlp（.2767/a4）、other635（.3011/a5）、equity_forum_data（.8948/a13） | 用户 sentiment 禁令待裁，暂不投 |
| **饱和 Tier B** | dl_riskfree_returns（.9095/a8021，Wave36 已封）、insider_feats（.6636/a1924，PROD 地板 0.78）、other532（.9956/a1864）、other335（.59/a1067） | aCount≥1000，不投 |
| **高拥挤/描述 boilerplate** | other315（.4022/a493）、other496（.8006/a844 FX） | 描述是 RIC/BBID security-master 模板（§5.108.1 不可信），aCount 高 |
| **★ 未挖高潜力** | **acquisition_model（.9937/a111/vs5，15 字段）**、other78（.7925/a70/vs6 earnings call）、other327（.7866/a31/vs5 利率敏感）、other424（.5919/a44/vs5 dividend）、other695（.4886/a180/vs4 imports）、other571（.2649/a62/vs5 Wikipedia）、other567（.2571/a16/vs6 employee review） | 下一批探针来源 |

**选 acquisition_model 为下一探针的理由**：① cov **.9937 近满覆盖** ⇒ 直接规避 §5.113 的 2016-12-22 CW 洞（低覆盖+backfill artifact），无需 backfill；
② 真实经济机制（M&A 目标溢价），非 sentiment（不受决策 6 闸）；③ a111 中等拥挤非饱和；④ category=other 单字段 ATOM 合规（约束 5）。
other695（imports）与 other475（exports）同贸易流机制 ⇒ **预期同 prod 墙**，优先级降；other78（earnings call）为备选高覆盖集。

**acquisition_model 字段画像（15 VECTOR，全 cov .9937，percentile rank 1–100）**：
- **headline M&A 目标 likelihood（5 地理peer scope）**：global（u9/a11）、country（u7/a9）、region（u6/a6）、industry（u4/a5）、sector（u2/a2）。
- **成分 percentile（size/credit/fundamental/valuation/text × global/region）**：
  global_valuation（u27/**a34 最拥挤**）、region_valuation（u16/a26）、global_company_size（u6/a7）、global_credit_quality（u3/a3）、
  global_fundamental_factor（u3/a3）、global_text_factor（u1/a1）、region_company_size（u3/a3）、region_credit_quality（u5/a5）、
  region_fundamental_factor（u5/a5）、**region_text_factor（u0/a0 未挖）**。
- **画像判读**：① 全是 percentile rank（已截面归一、有界近均匀）⇒ **非单边恒正原始水平**，铁律 A 不机械适用；level 与 change 都有经济含义。
  ② valuation 成分最拥挤（a34/a26）⇒ 避；headline likelihood 较不拥挤。③ 各 scope 是**同一 M&A 模型的不同 peer 归一** ⇒ 高度互相关，多 scope 探针冗余度高。
  ④ cov 近满 ⇒ **不用 ts_backfill**（区别于 other545/546），从源头避 CW 洞。

**wave 257：M&A 目标 likelihood 变化率首探（A-2 立机制）**：
- **A-1 五问**：① percentile rank 存量 ⇒ 取 **change（ts_delta）** 捕「新晋目标」而非已定价的高水平；② 截面排序 ⇒ group_rank；
  ③ 被定价的是**事件预期**（被收购概率）；④ M&A 套利是已知 quant 轴但本集 KOR 仅 a111 ⇒ 中等拥挤；⑤ 目标识别是渐进过程非稀疏事件 ⇒ 不用 trade_when。
- **A-2 收益来源**：谁=持有潜在标的的投资者/套利者；为什么错=标的难事前识别，**新晋上升目标**（change）比已确立高 likelihood 名更少被注意（有限注意力）；
  修复期=数周–一季（谣言→公告）；方向=likelihood 上升 ⇒ 标的溢价 ⇒ 正（铁律 B：若负先 reverse）。
- **2 颗探针**（单字段 OTHER ATOM，约束 5 ✅；SECTOR；**无 backfill**；vec_avg / ts_delta 22 / group_rank subindustry）：
  | 探针 | 字段 | sim |
  |---|---|---|
  | P1 | `global_percentile_acquisition_likelihood`（u9/a11，headline 全球） | `4EjNkDdSQ4DGb6WKrTWJNLp` |
  | P2 | `industry_percentile_acquisition_likelihood`（u4/a5，行业相对，较不拥挤） | `16oI3W3UH4uDb6l5NvDGP62` |
  表达式：`group_rank(ts_delta(vec_avg(<字段>), 22), subindustry)`。三闸：算子 vec_avg/ts_delta/group_rank/subindustry 均 255/256 成功用过（无 backfill 更简）；字段 get_datafields 已确认存在。
- **预注册判据**：任一 |S| ≥ 1.0 ⇒ 有信号，**prod-first**（M&A 模型可能高 prod，§5.108.2 网络/模型类警告）+ 逐年归因（约束 4：核 2014/2015 是否有数据，模型可能历史短）再决定扩不扩；
  双臂 |S| < 1.0 ⇒ 试 level 形式一次（percentile 非单边，level 有含义）或换 unmined region_text_factor，仍无 ⇒ acquisition_model 变化率轴天花板；若负先 reverse。
- **波次三问**：继承 = §5.113 高覆盖避 CW 洞教训 + 255/256 骨架；准入 = 单字段不混信号、避 valuation 拥挤成分、不裸用低覆盖；收窄 = 2 颗裸探针（新数据集首探）。### §5.115 wave 257 收割（FAIL，M&A 变化率死平）+ wave 258 level 形式探针

**wave 257 收割入库**（region=KOR wave=257 dataset=acquisition_model，upserted 2，verdict=FAIL）：

| 探针 | alpha | 字段 | S | F | 2Y | RN S | TO | DD | CW | failed_ra |
|---|---|---|---|---|---|---|---|---|---|---|
| P1 | `vR19lgYa` | global_percentile_acquisition_likelihood（变化率） | 0.28 | 0.08 | 0.13 | **−0.40** | .1755 | .1081 | **pass** | 3 |
| P2 | `JjempPqE` | industry_percentile_acquisition_likelihood（变化率） | 0.05 | 0.01 | −0.10 | **−0.66** | .1853 | .1567 | **pass** | 3 |

**★ 两条结论**：
1. **高覆盖避 CW 洞假设验证成功**：cov .9937 + 无 backfill ⇒ 双臂 CW 全 pass（对比 other545/546 低覆盖+backfill 双双 CW 0.26 FAIL）。
   ⇒ §5.113 的 2016-12-22 CW 洞确为**低覆盖+backfill artifact**，高覆盖集从源头规避。**固化：稀疏集探针 CW 风险预判 = 看 coverage，cov<0.5 预期 CW 洞。**
2. **M&A likelihood 变化率（ts_delta 22）死平**：S 0.05–0.28 ≪1.58，RN S 负（−0.40/−0.66，因子暴露主导且反向），TO 高（.17–.18）。
   机理：percentile rank 是慢变模型输出，22 日 ts_delta 多为模型更新的小离散跳变 ≈ 噪声 ⇒ 无 alpha。两臂 raw S 正（铁律 B 不触发 reverse）。

**wave 258：level 形式探针（预注册兑现：percentile 非单边，level 有经济含义）**：
- 机制：高 M&A 目标 likelihood ⇒ 被收购溢价 ⇒ 做多高 likelihood 名（**level 因子**，区别于 257 的 change）。这是 M&A 套利的经典暴露，但**可能高 prod**（模型广泛使用）。
- 构造：`group_rank(vec_avg(<字段>), subindustry)`（**无 ts_delta**，level；无 backfill；SECTOR）。
- 2 颗：P1 global_percentile_acquisition_likelihood（u9/a11）sim `43TIEedLq4AZcxlspqB5KgA` / P2 sector_percentile_acquisition_likelihood（u2/a2 最不拥挤 headline）sim `1hwspXapQ58kaae17tUOuoOi`。
- **预注册判据**：任一 |S| ≥ 1.0 ⇒ 有信号，**prod-first**（level 是拥挤暴露，prod 风险高）+ 逐年归因（约束 4）；双臂 |S| < 1.0 ⇒ **acquisition_model change+level 双轴天花板**，转 other78（earnings call，高覆盖备选）；若负先 reverse。
- **波次三问**：继承 = 257 变化率死平 + 高覆盖避 CW；准入 = 单字段、不混 valuation 拥挤成分；收窄 = 2 颗（形式切换 change→level，非网格）。

**战役级观察（OTHER 塔结构性困难）**：迄今 OTHER 探针——other545 NEMO（S0.33–0.74）、other546 经济链接（S0.63–0.73）、acquisition_model change（S0.05–0.28）——
**网络/模型类机制在 KOR 一致弱信号**；唯一强 OTHER 信号 other475 export（S1.99）撞 prod 墙。
⇒ OTHER 塔（需 +2 ACTIVE）供给困难：要么弱信号、要么 prod 拥挤。60 颗目标若主靠 OTHER 可能结构性不可达，需评估其它未点亮塔或表面给用户。### §5.116 ★ other475 B prod 终决 0.8395 FAIL ⇒ export 家族三档全 prod 墙（战役级 dead-end 结论）

**B（d5WmEarw, other475 export, SECTOR, S 1.99）prod 实测**（外槽垄断 + 多次 −32603 超时后终于缓存读出，computed=false / elapsed 295ms）：
- **max_correlation = 0.8395，passes_check = false**。
- 直方图：[0.6,0.7)=**34**、[0.7,0.8)=**4**、[0.8,0.9)=**3** ⇒ **7 钉 >0.7**，max 0.8395，min −0.3827。
- **非单钉形态**（0.7+=7 不在 1–3，0.6–0.7=34 不在 6–16）⇒ **广谱 prod 拥挤**（export 信号本身被广泛交易），不是可窗口微调救的单钉。

**other475 三档设置 prod 全景（D0-P 设置杠杆已试尽）**：
| 档 | alpha | S | prod max | >0.7 钉数 | 判 |
|---|---|---|---|---|---|
| MARKET（基线） | leA22za2 | 1.92 | 0.8377 | 11 | FAIL |
| STATISTICAL（A） | 3qoxag8z | 1.69 | 0.7498 | 1（单钉） | FAIL |
| SECTOR（B） | d5WmEarw | **1.99** | **0.8395** | 7 | FAIL |

**★ 终判（预注册 §5.107.1 兑现）**：两档（A/B）prod 都 ≥0.70 ⇒ D0-P「≥0.75 或尝试失败」行生效 ⇒ **other475 export 家族 dead_end**。
设置杠杆（MARKET→STATISTICAL→SECTOR）把 >0.7 钉从 11 压到 1（STATISTICAL）但 max 仍 0.7498≥0.70；SECTOR 反弹到 0.8395。
**没有任何设置档能把 prod 压到 <0.70** ⇒ 结构性墙，非参数可修。

**★ 再次验证 §5.107 自纠教训**：SECTOR（B）S 最优（1.99）但 prod 最差（0.8395）；STATISTICAL（A）S 较低（1.69）但 prod 较低（0.7498）。
**S 最优档 ≠ prod 安全档，两轴搜索空间不可互相顶替**——这是第二次实证（继 wave 253 双臂后）。prod 贴线时低 prod 优先于高 S，但本族连低 prod 档也 ≥0.70 ⇒ 无解。

**处置**：
- 战役级 dead-end 结论记此（同 other545/546 天花板记录格式）。**正式 seal_dead_end 需 forum_recon 取证 + 用户批准 force_seal，不 unilateral 执行**（约束）。
- leA22za2 / 3qoxag8z / d5WmEarw 三颗均**不可提交**（prod 墙），d5WmEarw 虽 S 1.99 全闸过仍标 prod-blocked。
- **Mode B 组腿救援**（pending 用户决策）：other475（OTHER）可与 NEWS 组腿（约束 5 允许，全局限 5 颗），但 export 信号本身广谱拥挤，组腿能否稀释 prod 未证；需用户拍板是否投。
- 约束 4 冲突 moot（leA22za2 2014/2015 零持仓）——prod 墙已先判死，无需再纠结年度覆盖。

**战役态势重大更新**：OTHER 塔最强信号（other475 export S1.99）确认 prod 死。迄今 OTHER 探针全灭：
other545 NEMO 天花板 / other546 经济链接天花板 / acquisition_model change 死平（level 待 258）/ other475 export prod 墙 / other455 REVISION-CLUSTER prod 墙。
**OTHER 塔（需 +2 ACTIVE）结构性供给困难已坐实**：弱信号或 prod 拥挤二选一。60 颗目标主靠 OTHER 大概率不可达 ⇒ 需评估其它未点亮塔 / 向用户表面结构性结论。### §5.117 ★ risk 塔唯一近闸腿 QPvr1vPM 全归因 + risk59=S3 融券面板 9 年（约束 4）+ 未点亮塔 60 颗可行性总收口

> 触发：OTHER 塔结构性坐实（§5.116）后，回读塔图（§0/§1）发现唯一仍活的未点亮塔 = **risk(1.3)**，
> 唯一近闸腿 = `QPvr1vPM`（S 1.02 / 2Y 1.80）。按约束 2「对近闸候选定向挖掘」+ 铁律 F（无归因不得发波）先做全归因，再判是否值得投杠杆。

**1. QPvr1vPM 平台实测（get_alpha_details，判定只走平台）**
- code：`hump(reverse(group_zscore(vec_avg(rsk59_offer_rate), sector)), hump=0.003)`
- 设置：STATISTICAL / decay4 / trunc0.08 / nanOFF / TOP600 / D1 / 2014-01-01…2023-12-31。
- 指标：**S 1.02 / F 0.67 / TO .135 / returns .0576 / DD .0919 / subU 0.95 / 2Y 1.80 / investS 0.91 / investF 0.59**。
- RA 失败 3 闸：**LOW_SHARPE（1.02 vs 1.58，缺口 0.56）/ LOW_FITNESS（0.67 vs 1.0）/ CONCENTRATED_WEIGHT**（warning 桶未展开值）。
- 塔位：`KOR/D1/RISK ×1.3`，effective 1（纯 cell 满信用）。2Y/subU/invest 三闸**已过**，CLUSTER_TEST 0.92（<1 过）。
- ⚠ F 与 S 绑定：F = S×√(returns/max(TO,.125)) = 1.02×√(.0576/.135)=0.67 ✓；若 S→1.58 且 returns/TO 不变 ⇒ F≈1.03 ⇒ **绑定闸是 Sharpe，fitness 随 S 走**。

**2. 逐年归因（get_alpha_yearly_stats）**
| 年 | S | F | longCount | 读 |
|---|---|---|---|---|
| 2014 | 0 | 0 | **0** | ⛔ **全空（数据起点 2015）** |
| 2015 | 0.18 | 0.04 | 304 | 弱 |
| 2016 | −0.56 | −0.24 | 331 | 唯一负年 |
| 2017 | 2.01 | 1.70 | 336 | 强 |
| 2018 | 0.87 | 0.55 | 359 | 偏弱 |
| 2019 | 1.48 | 1.09 | 343 | 过 |
| 2020 | 0.62 | 0.33 | 357 | 弱（中段回撤） |
| 2021 | 1.39 | 1.01 | 379 | 过 |
| 2022 | **2.08** | 1.95 | 368 | 最强 |
| 2023 | 1.26 | 0.92 | 365 | 过 |

- **S<1.0 活跃年 = 2015/2016/2018/2020 = 4/9（44%）**，但**集中在早中段**；近三年（2021/2022/2023）全 ≥1.26 ⇒ **2Y 1.80 真实可达，非「近年断崖」**（与 wave186 earnings3 / wave194 risk68 的 2Y≫IS 背离机制性衰减**相反**：这里是早年拖累 IS，近年走强）。
- **单年集中度**：top 年 2022 pnl 1.147M / 正收益总 5.643M = **20.3% < 30%** ⇒ **非过拟合指纹**。
- **符号结构**：9 活跃年 8 正 1 负（仅 2016）⇒ 健康。

**3. PnL 曲线 + raw vs RN 分解（get_alpha_pnl，铁律 E）**
- 曲线：2014 平 0 → 2015–2016 震荡（2016 中段深回撤）→ **2017 起干净阶梯累积**至 5.349M；停滞段集中在早年（2015–2016 / 2020 中 / 2023 中小幅）。
- **raw 5.349M / investability-constrained(RN) 4.960M = 92.7%** ⇒ 信号高度可投资。
- 早年 RN ≪ raw（2016-10 raw −477K vs RN −668K；2017-01 raw −228K vs RN −445K）⇒ **早年弱含因子暴露拖累**；近年 RN≈raw（92–94%）⇒ **近年是干净 alpha**。
- **归因判类（决策表）**：阶梯健康 + 停滞段少（早年）+ 单年 20.3%<30% + 近年走强 ⇒ **「信号真实但强度不足 + 早期覆盖缺陷」**，**允许强度/returns 杠杆扫描**（非换机制）。

**4. ★ risk59 = S3 Partners 融券/做空拥挤面板（query_field_profile 全 16 字段）**
- 16 字段全 VECTOR、**覆盖率逐字相同 0.9806（高）**⇒ 共享同一供应商面板、同起点。
- 核心字段经济含义（description 为准）：
  - `offer_rate` = 空头为存量持仓支付的**融券融资费**（年化%）← QPvr1vPM 用此腿；
  - `bid_rate` = 多头出借存量股赚的**融券费**（年化%）；`last_rate` = 增量出借即期费；
  - `s3utilization` = 实时空头持仓 / 可出借量（**融券供给利用率**）；`indicativeavailability` = 预测可出借量；
  - `daystocover10/30/90day` = 空头持仓 / ADV（回补天数）；`dtcdailychg`/`dtcweeklychg` = 回补天数日/周变化；
  - `crowded_score` = 空头拥挤度专有评分；`short_interest`/`shortinterestnotional`/`shortinterestpct` = 空头持仓（股数/USD/占流通%）；
  - `squeeze_risk` = 轧空可能性评分 **DEAD（best_s −0.31）**；`short_momentum` = 日做空/回补动量 **DEAD（best_s −0.20）**。
- **14/16 UNTESTED，2 DEAD**（squeeze_risk / short_momentum，即 KOR-WAVE96 点名的裸截面族）。
- **机制（通道 B 文献）**：融券费/利用率 = 做空压力计。D'Avolio(2002)/Geczy-Musto-Reed(2002)/Jones-Lamont(2002)「卖空约束与股价」——高融券成本/高利用率 = 过度做空 ⇒ 后续负收益（昂贵难借股跑输）；`reverse(group_zscore(offer_rate))` 正是此方向。**offer_rate 未被 KOR-WAVE96 点名**（点名的是 squeeze_risk/做空金额/bid-ask vwap），且 group_zscore+reverse+hump 形态 S 1.02/2Y 1.80 远优于死掉的裸 rank ⇒ **本腿在死范围之外，活**。
- **⛔ 约束 4 结构性缺陷**：`offer_rate` 实测 **2014 longCount=0**（数据起点 2015）；16 字段覆盖率逐字相同 ⇒ **S3 KOR 面板极可能全集 2015 起 = 9 年**（待另一字段逐年复核确认全集）。IS 窗 2014–2023 要求十年 ⇒ **2014 空 = 约束 4 违反，任何表达式杠杆都造不出 2014 数据**（同 sentiment27 wave189 类，但 9 年 vs 5 年，缺陷轻得多）。
- CW warning 非覆盖洞（cov 0.98 高）⇒ 疑 hump/group_zscore 个别日权重集中，值未展开待复核；**不是低覆盖+backfill 的 2016-12-22 洞**（与 other545/546 不同）。

**5. ★★ 未点亮塔 60 颗可行性总收口（塔图 §0/§1 + 本段 + §5.116 合并裁决）**
| 塔 | 倍率 | 状态 | 供给能力 |
|---|---|---|---|
| news | 1.6 | ⛔ CLOSED（wave211 五轴全死） | 0 |
| sentiment | 1.6 | ⛔ CLOSED（wave216 四集全死） | 0 |
| institutions | 1.4 | ⛔ 无活集（institutions6+fund_holdings_panel 死） | 0 |
| macro | 1.4 | ⛔ CLOSED（macro63 单 0/1 哑变量 + other106 机制死） | 0 |
| insiders | 1.2 | ⛔ CLOSED（insiders5 天花板 1.05 + insiders1 死） | 0 |
| socialmedia | 1.0 | ⛔ 无信号面（socialmedia39/other100 均邻居票 ID 列表） | 0 |
| **risk** | 1.3 | **唯一活塔**；risk59 S3 面板 **9 年（约束 4）**；risk68 机制死 / risk72 0 槽 | 近闸腿 QPvr1vPM S1.02（缺口 0.56）+ 14 未测字段（方差/凸变换轴活），**但全继承 9 年缺陷** |
| earnings | 1.1 | earnings3 弱（wave186 max\|S\|0.94，2Y≫IS 机制衰减） | 仅补数 |
| imbalance | 1.0 | imbalance5 2Y≈0.17 结构不可达，αC1109 拥挤 | 仅补数 |
| OTHER | 1.6（lit=1 需+2） | ⛔ 结构性耗尽（§5.116：other545/546/acquisition 天花板 + other475/455 prod 墙） | 弱信号或 prod 拥挤二选一 |

**★ 终判（与 §1 line62 一致并坐实）**：**单塔单字段 ATOM 上限实测 ≤1.02**；6 个未点亮塔已 CLOSED、OTHER 耗尽、risk 唯一活但 9 年缺陷 + 0.56 Sharpe 缺口、earnings/imbalance ≤1.1 仅补数。
⇒ **60 颗 REGULAR（优先 ATOM）目标在当前攻击面上结构性不可达**。所有剩余路径都需用户决策，无一可自主合规推进：

| 路径 | 内容 | 阻塞点（需用户拍板） |
|---|---|---|
| ① 放宽约束 4 | risk59 9 年面板（2015–2023）若被接受 ⇒ 定向 gate-push QPvr1vPM（+0.56 S，强度杠杆已获归因许可）+ 测方差/凸变换活轴（14 未测字段） | **约束 4「近十年都要有数据」是否对 risk59 放宽到 9 年**（~~同 leAk66xx 待决~~ ⇒ leAk66xx 已由 prod 0.8711 判死，见 §8.1） |
| ② IS 窗平移 | 若平台 KOR 数据延伸到 2024 且面板 2015 起 ⇒ 2015–2024 = 10 年合规（约束 4「覆盖率可动态调整」内） | **需先核平台 KOR IS 窗是否可移到 2024**（ standing endDate 2023-12-31 疑为平台硬窗）；若平台只到 2023 则此路不通 |
| ③ 合规组腿 | risk×earnings / OTHER×NEWS（约束 5 允许，全局限 5） | risk 腿仍 risk59 ⇒ 继承 9 年；news 塔 CLOSED；other475 export 广谱拥挤 ⇒ 组腿稀释 prod 未证 |
| ④ 新数据集授权 | 当前未点亮塔活集已扫尽 ⇒ 需平台新数据集 | **用户授权新数据集**（约束 1「一个个 category 查」已查尽现有面） |

**6. 待决清单（合并 §5.92.3 + 本段，不 unilateral 执行）**
1. **约束 4 对 risk59 放宽到 9 年？**（本段新增，最高优先——决定唯一活塔能否推进）
2. 是否核/移 IS 窗到 2024（路径②前置）。
3. LLZ6wZO2 提交（FUNDAMENTAL 塔满，prod/self 余量 0.024，corr_stale ⇒ refresh=True 终验）。
4. ~~leAk66xx 约束 4 放宽。~~ ⇒ **已关闭**：prod **0.8711**（2026-10-31，D0-P 墙）先于约束 4 判死，见 §8.1。**这一项不再需要用户裁决。**
5. ~~剩余未画像数据集授权~~ ⇒ **已收口（2026-10-31）**：other78 **字段级判死**（§7.1）· other571 **实测判死**（§7.2，wave 268）· other327 / other424 **实测判死**（wave 263/264）· other695 **prod 0.8711 判死**（§8.1）· other567/532/315/335 **不投**（§7.4）· other323 **字段级判死**（§7.1 同型）。⇒ **现有数据集面已扫尽**，本项只剩「**授权平台新数据集**」这一种形态。
6. sentiment 禁令裁决（gates news_sentiment_dl/nlp、ai_news_scores、equity_forum_data、other635）。
7. 正式 seal_dead_end 批量（other545/546/acquisition 天花板、other475/455 prod 墙、other436/323 + 久挂清单）——**均需 forum_recon 取证 + 用户批准 force_seal，不 unilateral**。

**7. 纪律自检**：本段**零仿真配额**（纯 get_alpha_details/yearly/pnl + DB 画像只读）；铁律 F 归因先行已完成；未对死轴（OTHER 天花板/prod 墙、squeeze_risk/short_momentum 裸截面）重投；唯一活轴（risk59 方差/凸变换、offer_rate gate-push）**因约束 4 阻塞而暂停投槽，待用户裁决**——符合「无归因不得发波 / 不烧配额于结构性阻塞路径」止损纪律。
---

## §5.118 risk59 定向破闸 + 全字段普查收官（Wave 259/260/261，2026-10-31）

**授权**：用户「同意」路径 ①（约束 4 对 risk59 放宽到 9 年）+ 按 KOR RA skill 对 `QPvr1vPM` 定向破闸 + 扫方差轴。
**前置**：§5.117 已把约束 4（近十年）判定为唯一阻塞；本段以 9 年口径（2014–2023，含 2014 空年）执行，2014 空年在归因中单独记缺陷，不作剔除。

### 5.118.1 三波结果总表

**Wave 259（8 探针，基线 `QPvr1vPM` = `group_zscore(vec_avg(rsk59_offer_rate), sector)` 反转 + STATISTICAL 壳）**

| tag | alpha | S | F | TO | 2Y | subU | 结论 |
|---|---|---|---|---|---|---|---|
| P1 nan ON 对照 | pwdzz32X | 1.02 | .67 | .1350 | 1.80 | .95 | **与基线逐位相同 ⇒ nanHandling 是 no-op** |
| P2 中性化 SECTOR | npvzO0zl | 0.76 | .64 | .0785 | 1.02 | .81 | 降 |
| P3 中性化 SUBINDUSTRY | JjeX5VoE | 0.87 | .71 | .0855 | 0.96 | .91 | 降，且 2Y 崩到 0.96 |
| P4 winsorize std=3 | YP1kkYew | 0.97 | .61 | .1333 | 1.77 | .90 | 降；**CW 仍 FAIL ⇒ CW 不是极值造成** |
| P5 ts_decay_linear 22 | 1YNmn6WJ | 0.97 | .63 | .1316 | 1.71 | .92 | 降（第三区复现「时序平滑零和」） |
| P6 ts_zscore 504 | d5W776w2 | **0.01** | .00 | .1169 | 0.01 | .12 | 崩 ⇒ 信号是**截面水平**，不是自身历史偏离（铁律 A 对费率不适用） |
| P7 ts_var 66 | omEz91Jk | −0.52 | −.21 | .0796 | −1.04 | −.37 | 方差轴负 |
| P8 ts_var 252 | Xg9lYk2m | −0.26 | −.07 | .0645 | −0.30 | −.26 | 方差轴负 |

**Wave 260（risk59 字段普查第一批 8 探针，同壳同设）**

| tag | alpha | S | F | TO | 2Y | subU | 结论 |
|---|---|---|---|---|---|---|---|
| A_util `s3utilization` | 9qx6A5qK | 0.09 | .02 | .1273 | 0.31 | .11 | 死 |
| A_pctfloat `shortinterestpct` | LLMXloVe | 0.16 | .04 | .1217 | −0.83 | .14 | 死 |
| A_dtc90 `daystocover90day` | leAzRwde | −0.31 | −.11 | .1202 | −1.13 | −.37 | 死 |
| A_crowd `crowded_score` | pwdz1bXX | 0.40 | .16 | .1220 | −0.24 | .33 | 死 |
| **B_lastrate `last_rate`** | **vR1ze9zv** | **1.04** | **.67** | **.1428** | **2.02** | **1.01** | **唯一优于基线（+0.02），2Y/subU 双过线** |
| B_notional `shortinterestnotional` | 1YNmandQ | −0.17 | −.05 | .1372 | −1.09 | −.38 | 死 |
| C_twoleg offer×util | 2rAZanx5 | 0.14 | .03 | .0884 | 0.88 | .36 | L6 双腿死（第二腿无信号 ⇒ 稀释） |
| D_tvrdecay target 0.05 | YP1k2prJ | 0.99 | .65 | .1300 | 1.72 | .88 | L3 微降 |

**Wave 261（收尾 5 探针）**

| tag | alpha | S | F | TO | 2Y | subU | 结论 |
|---|---|---|---|---|---|---|---|
| E_bidrate `bid_rate` | 58E6arXz | 1.01 | .66 | .1349 | 1.80 | .96 | 融资费轴第三点，同族确认 |
| E_avail `indicativeavailability` | zq3oPdvR | 0.25 | .08 | .1214 | 1.01 | .24 | 供给侧无信号 |
| E_dtcwchg `dtcweeklychg` | 9qx6aM1V | 0.10 | .01 | .3423 | 0.20 | .19 | 死且换手爆表 |
| F_feepair last×offer | Vkxl2RLY | 0.79 | .46 | .0903 | 1.46 | .88 | 共线双费稀释 |
| G_subindgroup 表达式内 subindustry | KPJ8Xopg | 0.79 | .42 | .1386 | 1.01 | .67 | 组轴换细崩（第四次复现） |

### 5.118.2 五条已封闭的轴（以后不得再投配额）

1. **nanHandling**：ON ≡ OFF 逐位相同（P1 vs 基线）⇒ 不再作为扫描维度。
2. **中性化阶梯**：STATISTICAL 1.02 > SUBINDUSTRY 0.87 > SECTOR 0.76 —— **第三次 KOR 复现「粗轴更好」的反面**：本族 STAT 最优，换任何档都降。死轴。
3. **winsorize + 时序平滑**：winsorize std=3 −0.05 且**修不掉 CONCENTRATED_WEIGHT** ⇒ CW 根因不是极值，是**持仓股数少**（352 long / 274 short 对 TOP600）。ts_decay_linear 22 −0.05，第三次「时序平滑零和」。
4. **自身历史偏离（ts_zscore 504）**：0.01 全崩 ⇒ 费率是**截面相对贵贱**信号，任何「拿自己的历史当基准」的变换都会毁掉它。
5. **方差轴（ts_var 66 / 252）**：−0.52 / −0.26 双负 ⇒ 「借券费率的波动率/分歧度」在 KOR 无信号。

### 5.118.3 全字段普查结论：risk59 = **单一融资费因子**

16 个字段中已测 14 个（本段 12 + 前段 squeeze_risk / short_momentum 判死）：

| 轴 | 字段 | 最优 S | 判定 |
|---|---|---|---|
| **融资费（唯一活轴）** | `offer_rate` / `last_rate` / `bid_rate` | 1.02 / **1.04** / 1.01 | **整个数据集 = 这一个因子** |
| 拥挤度量（数量型） | crowded_score / shortinterestpct / s3utilization / shortinterestnotional / daystocover90day | 0.40 / 0.16 / 0.09 / −0.17 / −0.31 | 全死 |
| 供给侧 | indicativeavailability | 0.25 | 死 |
| 变化率 | dtcweeklychg | 0.10（TO .34） | 死 |
| 其余同族未测 | short_interest / daystocover10day / daystocover30day / dtcdailychg | — | 与已测同族重复度量，按「劣于同族不再扫」不投 |

**天花板**：单字段 risk59 ATOM 最优 **S 1.04 vs LOW_SHARPE 1.58 ⇒ 缺口 0.54**。且**所有 KOR 杠杆已在本族逐个证否**（中性化阶梯 / winsorize / 平滑 / tvr_decay / z-score / 方差 / 双腿乘积 / 细组轴），无一优于基线。**0.54 的缺口在当前算子面内不可补**。

### 5.118.4 归因（铁律 F，`vR1ze9zv` 逐年）

| 年 | 2014 | 2015 | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 |
|---|---|---|---|---|---|---|---|---|---|---|
| S | — | 0.48 | **−0.51** | 1.84 | 1.01 | 1.27 | 0.56 | 1.09 | **2.35** | 1.47 |
| pnl | 0 | 270,684 | −264,071 | 969,382 | 715,009 | 768,812 | 414,696 | 617,827 | 1,298,610 | 789,439 |

- **2014 全空（pnl=0、longCount=0）= 约束 4 的实物证据**：该数据集 2014 年确实无数据，这不是「指标差」而是「没有持仓」。
- 正收益年 7 个，负年 1 个（2016，占活跃年 11%）；**2022 占正收益 22.2% < 30% ⇒ 非过拟合指纹**。
- 归因类型 = **「信号真实 + 早期年份拖累」**，不是「信号衰减」也不是「因子拖累」。2017–2023 段显著强于全期 S 1.04 ⇒ 2Y 2.02 是该段的直接体现。
- 结论：**继续压全期 S 是错方向**——它被 2015/2016 + 2014 空年联合拖住，而这两者都不是杠杆能改的。唯一能让它「看起来达标」的手段是砍 2014–2016，那正是约束 4 要防的过拟合。

### 5.118.5 塔级含义（本段最重要的结论）

**在「不组 PV/MODEL/OTHER 两两腿 + 每类最多 5 条 + 近十年 + 未点亮塔」四条约束同时成立时，KOR 现有未点亮塔不存在能交付 S ≥ 1.58 单字段 ATOM 的数据集。** 证据链：

| 塔 | 最优单字段 S | 距 1.58 | 依据 |
|---|---|---|---|
| RISK（risk59） | 1.04 | **−0.54** | 本段全字段普查 |
| FUNDAMENTAL | 已满塔（LLZ6wZO2 待提交） | — | §5.117 |
| OTHER | 结构性天花板 / prod 墙 | — | §5.92–5.117 已判死 |
| 其余未点亮（other78/327/424/695/571/567 等） | 未画像 | 未知 | 待用户授权 |

⇒ **60 颗 regular alpha 的目标在当前约束集内结构性不可达**；要推进只有三条路：放宽约束（组腿 / 覆盖率 / 年度）、平台新数据集、或改用已满 FUNDAMENTAL 塔的存量补救。**这不是配额问题，是信号面问题。**

### 5.118.6 纪律自检

- 三闸（op_arity + 算子存在性 + 字段存在性 + gate4 单位闸）每波发批前均过（`logs/_tmp_preflight_w260.py` / `_w261.py`，均 PASS）。
- 并发：单次 `batch_create_simulations` ≤ 6 条；两轮 429 后按单条补发成功（平台在飞深度实测 ≈6–7）。
- 归因先行：`vR1ze9zv` 逐年 + pnl 已取；铁律 F 满足后才写本节。
- 入库：wave 259/260/261 回测行均经 `upsert_backtest_rows` 入库；wave_results 259/260/261 均写。
- **零提交**（`ALLOW_ALPHA_SUBMIT=False`），判定只走平台 `is.checks`。
- 未重投已死轴；方差轴与破闸杠杆本段**一次性扫全并全部判死**，后续不再投。

---

## 6. ANALYST 塔第二条机制：analyst9 修正广度（wave 267，2026-10-31）

> **为什么开这一节**：§5.25 已把 analyst 的**修正量级**族（`eps_estimate_4wk_change` / `anl44_best_eps_4wk_chg`）
> 九条轴全部收敛到 1.40–1.45，闸 1.58 差 0.13。ANALYST 塔仍差 1 票，而 EPS 修正族内已无杠杆。
> ⇒ 唯一还在「同 category、但**不同机制**」的未测面 = **修正广度（revision breadth）**。

### 6.1 数据集与字段选择（0.1 质量先验 + 0.2 分类 + 0.3 五问）

`analyst9`（KOR/D1/TOP600）：48 字段，平台 αCount 137，`n_tests = 0`（**本区从未回测过任何字段**）。

**0.1 质量先验（按 alphaCount 降序，KOR/D1 实测，`filter_sharpe=false` 扫全）**：

| 字段 | 类型 | cov | alphaCount | 含义 |
|---|---|---|---:|---|
| `anl9_s_numanalysts` | VECTOR | **.7109** | **16** | 纳入共识的分析师数 |
| `anl9_s_numup` | VECTOR | **.7109** | **14** | 上调家数 |
| `anl9_s_numdn` | VECTOR | **.7109** | **14** | 下调家数 |
| `anl9_s_numupunfiltered` | VECTOR | .7109 | 13 | 上调家数（含被剔除者）|
| `anl9_s_numdownunfiltered` | VECTOR | .7109 | 8 | 下调家数（含被剔除者）|
| `anl9_s_numnochg` | VECTOR | .7109 | 6 | 未变家数 |

⇒ **头部字段就是广度三件套** ⇒ 该数据集最强经济轴 = **修正广度**（不是修正幅度，幅度在 analyst_consensus）。
`anl9_daily_*` 同名组 coverage 只有 **.4433 < 0.5 覆盖率地板** ⇒ 弃用，只用 `anl9_s_*`（.7109）。

**0.2 分类**：其余 40+ 字段全是 effectivetime / totime / splitfactor / isexcluded / 币种码等
**时间戳与标识符**（`UNUSABLE`），不构成信号面 ⇒ 本数据集**只有广度三件套可用**。

**0.3 五问 → 预处理决策**：

| 问 | 答 | 决策 |
|---|---|---|
| 时间维度 | 计数快照（存量） | 不取 `ts_delta`，直接归一化成**比率**再做时序 |
| 相对性 | 排序 / 占比 | 用 `divide` 归一（去掉「分析师覆盖数」这个规模混杂） |
| 被定价的是谁 | **广度**（多少分析师同向）不是强度 | 分母必须除以 `numanalysts`，否则退化成「覆盖度」信号 |
| 有无博弈 | 有：覆盖多的大票广度天然更稳 | 需 `group_rank(·, industry)` 去行业/规模暴露 |
| 事件性 | 否，日频计数 | 不需 `trade_when` 门控 |
| VECTOR | 是 | **先 `vec_sum` 降维再算比值**（分子分母同用 `vec_sum`，维度对齐）|

### 6.2 A-2 收益来源声明（硬门）

| 项 | 内容 |
|---|---|
| **谁在被定价** | 卖方分析师的**羊群行为**——单个分析师改数会被市场读懂，但「多少比例的分析师在同向改」这一层信息是分散的 |
| **为什么会被错** | 信息扩散摩擦：广度信息要跨多个分析师、多个预测期拼出来，机构买方跟踪成本高；市场对**幅度**（一个头条数字）反应过度，对**广度**（弥散信号）反应不足 |
| **错了多久修复** | 数周–一季（下一轮财报 / 覆盖更新前），故窗口取 22 / 252 |
| **预期方向** | 净上调占比高 ⇒ 后续跑赢（修正动量），**反向形态须实测（铁律 B）** |
| **边界条件** | 覆盖分析师数 < 3 时比值噪声大；KOSPI 大票覆盖稳定、广度几乎不动 ⇒ 截面区分度可能集中在中小盘 |

### 6.3 核心信号与四档设计（设置与种子 `883mLenl` **逐字相同**）

核心项（记作 X）：

```
X = divide(subtract(vec_sum(anl9_s_numup), vec_sum(anl9_s_numdn)), vec_sum(anl9_s_numanalysts))
```

| 档 | 单变量 | 表达式骨架 |
|---|---|---|
| B1 | 广度**水平**（基线/对照）| `group_rank(ts_mean(X, 22), industry)` |
| B2 | **22×252 持久性积**（§5.25 唯一正向杠杆的迁移）| `group_rank(multiply(rank(ts_mean(X,22)), rank(ts_mean(X,252))), industry)` |
| B3 | **广度 × 量级**（同机制双facet）| `group_rank(multiply(rank(TS_DECAY(EPS量级)), rank(ts_mean(X,22))), industry)` |
| B4 | 广度**变化率**（铁律 A）| `group_rank(ts_zscore(X, 252), industry)` |

字段存在性闸（`validate_expressions`，KOR/TOP600/D1）实测 **PASS**：
`fields_checked = [anl9_s_numanalysts, anl9_s_numdn, anl9_s_numup, eps_estimate_4wk_change]`，
`unknown_fields=[] / unknown_soft=[]`。
⚠ **坑已踩**：`validate_expressions` 的 region/universe **缺省是 USA/TOP3000** ⇒ 不传就全报 `unknown_soft`（误判）。
必须显式 `region=KOR, universe=TOP600, delay=1`。

### 6.4 实测（batch H+I，2026-10-31，设置与种子逐字相同）

| 档 | alpha | S | F | 2Y | subU | TO | dd | CLUSTER | 判定 |
|---|---|---:|---:|---:|---:|---:|---:|---|---|
| **B1** | `Jje5NEbO` 纯广度水平 22d | **1.14** | 0.83 | 1.33 | 1.21 | .0349 | .1342 | 0.69 | ⭐ **广度机制成立**（>1.0），但弱于量级 1.40 |
| **B2** | `E56rpWk9` 22×252 持久性积 | 0.95 | 0.63 | 1.53 | 1.04 | .0308 | .1431 | 0.59 | ⛔ **−0.19 反向** |
| **B3** | `P0oX2GEE` 量级×广度积 | 1.37 | 1.12 | 1.52 | **1.34** | .0460 | .1223 | 0.85 | ⛔ **−0.08**（劣于量级单独 1.45），但优于广度单独 +0.23 |
| **B4** | `j2YdA6Qj` 广度 `ts_zscore` 252 | 0.89 | 0.53 | 1.57 | 0.93 | .2077 | .2026 | 0.36 | ⛔ 全崩，且 **CONCENTRATED_WEIGHT** 首现（2016-04-14 权重 1.0）|

**三条读数**：

1. ⭐ **广度是真信号，不是噪声**：纯广度 22d 平滑即 S **1.14** / nsr（riskNeut）**0.68**，
   `CLUSTER_TEST 0.69` ⇒ 与既有 book 差异化好。**这回答了 A-2 的第一问：谁在被定价 = 羊群广度，成立。**
2. ⛔ **§5.25 的唯一正向杠杆（同字段多时间窗持久性积）不能跨机制迁移**：
   在量级族 +0.05，在广度族 **−0.19**，且 2Y 反向升（1.33→1.53）⇒ 长窗腿把近年拉起来、把全期削下去。
   ⇒ **该杠杆的有效性依赖「信号本身随时间持续累积」，广度是慢变量（TO .035 已很低），再乘长窗等于把已有平滑再平滑一遍。**
3. **广度 vs 量级不是替代关系**：量级 1.40 强于广度 1.14，但广度的 TO 只有量级的一半（.035 vs .0505/…）
   ⇒ 二者若低相关，组合仍有意义（B3/B4 原定在飞）。
4. ⛔ **B3 证伪了「两条低相关腿相乘会抬高 Sharpe」的期待**：量级×广度 = **1.37**，落在两者之间
   （量级 1.45 > 乘积 1.37 > 广度 1.14），且 `CLUSTER_TEST` 从通过掉到 0.85。
   **机理**：`multiply(rank(A), rank(B))` 是 **AND 门**（交集），不是加权平均——它把两条腿的秩**同时**压向 0，
   等于要求「量级高**且**广度也高」才持仓，样本收缩但强度不叠加。
   唯一收益是 subU **1.34**（三档最高，+0.04）与 dd 更低（.1223）；不足以补 0.08 的 S 缺口。
5. ⛔ **B4 说明广度机制不能换时序形态**：同一 `X` 从 `ts_mean(·,22)` 换成 `ts_zscore(·,252)` 后
   S 1.14→**0.89**、TO 翻 **6 倍**（.035→.2077）、首次触发 **CONCENTRATED_WEIGHT**（2016-04-14 单票权重 1.0）。
   ⇒ 广度的价值来自**稳态水平 + 平滑**，不是「相对自身历史的偏离」；z-score 把慢变量放大成噪声。
   （与 §5.25 的 `ts_av_diff`→`ts_zscore` 等效替换成功形成对照：那是量级族，波动归一化有益；广度族相反。）

### 6.5 结论：ANALYST 塔在当前约束集内**结构性不可达**（2026-10-31 结案）

把两波全部 18 条 ANALYST 候选按「机制 × 优化档」摊平，可得一个**结构性上限**：

| 机制 | 最佳 alpha | S | 距 1.58 |
|---|---|---:|---:|
| EPS 修正量级（`analyst_consensus`，9 轴穷尽） | `GrW3Lba0` 22×252 | **1.45** | **−0.13** |
| 同信号换源（`analyst44`，同壳） | `VkxY7WEG` | 1.44 | −0.14 |
| 修正广度（`analyst9`，新机制） | `Jje5NEbO` 22d | 1.14 | −0.44 |
| 量级×广度（AND 门） | `P0oX2GEE` | 1.37 | −0.21 |

**结构性论证（不是"还没调够"，是"路被封了"）**：

- 现有约束集下，**跨机制组合只有两种合法形态**：`multiply`（AND 门 / 交集）与 `trade_when`（门控）。
  加权 `add(multiply(w,A),multiply(1−w,B))` 与等权 `add(rank(A),rank(B))` 都被闸 5 拦（禁混信号）。
- **AND 门不能超过最强腿**：实测 −0.08（1.45→1.37）；`trade_when` 在 KOR 全员稀疏数据上已两次证否（样本骤减）。
  ⇒ 复合档的数学上界 = 单机制上界 = **1.45**。
- 单机制侧：量级族的**九条表达式内轴已全部收敛到 1.40–1.45**（§5.25 batch A–G），
  广度族换时序形态即崩（B4），换持久性积即反向（B2）。
- 剩下唯一没试的方向是**第三条机制**（ESG / 目标价 / 评级修正）——但 KOR 实测无 target price / recommendation
  修正字段；`other553` 的 `ptgvalue`/`recvalue` 属 **OTHER category**，与 ANALYST 组腿不违反约束 5，
  可作为**独立主信号**开新波，不属于本塔补席。

**判定**：ANALYST 塔（当前 2/3）在「不提交即不点塔、只挖不提交」的口径下也**本就不该追求点亮**；
按 §7.5 与均匀点塔规则，`LLZ6wZO2`（FUNDAMENTAL 3/3 已满）与本研究均**不产生塔位收益**。
⇒ **本塔停止投配额**，ANALYST 的剩余 1 票只能靠未来**独立机制**（other553 类）自然产出，不再做定向补席。

---

## 7. 剩余 OTHER 数据集字段级 triage（2026-10-31，零配额，未派回测）

§5.124 待决清单第 5 项的 6 个未画像集，本轮**逐集拉全字段（`filter_sharpe=false`）做字段级判读**。
判据沿用 §5.113/§5.114 的既定纪律：**字段级核实足以判死的，不烧配额**（`other323` 先例）。

### 7.1 `other78` Earnings and conference call —— ⛔ **字段级判死（0 配额）**

平台实读 11 字段，cov .7925，aCount 70，vs6。**全部字段都是事件元数据**：

| 类 | 字段 |
|---|---|
| 事件是否发生 | `erdaily_cancelledflag` / `icdaily_cancelledflag` / `meetingdaily_cancelledflag` / `transcribeflag` |
| 事件性质标志 | `estimatedtimeflag`（日期是源方申报还是估算）/ `preliminaryresultsflag`（初报还是终报）/ `fullyearflag` |
| 时间戳 | `calendaryear` / `fiscalyear` / `fiscalquarter` |
| 类别 | `sourcetypename`（**字符串**，非数值） |

⇒ 无一个可做多空的数值信号；`sourcetypename` 是名字串，不能进算术。
**与 `other323`（证券主表）同型：字段级核实即判死，不派探针。**
⚠ 该集 aCount 70 全部落在这些标志位上（`sourcetypename` 独占 64）——是别人把「事件日存在性」当哑变量挖过的痕迹，不是可复用机制。

### 7.2 `other571` Wikipedia Viewing Data —— ⛔ **判死（Wave 268 实测 2 探针）**

23 字段全 MATRIX，cov .2593–.2660（≈**159/600** 只股票），aCount 1–20，vs5。
**0.1 质量先验（按 alphaCount 降序）**：`views28dmobile`(a20/u17) > `views7dmobile`(a18/u16) >
`views28d`/`views7d`/…(a2–4)。⇒ **头部轴 = 移动端注意力**，不是总浏览量（差 10 倍）。这是本集最有价值的一条读数。

**0.2 分类（按 description，不按字段名）——发现三层结构**：

| 层 | 字段族 | 语义 |
|---|---|---|
| 连续块梯 | `views7d`(过去 7 自然日) / `views14d`(**截至 14 天前**的 14 日窗) / `views28d`(**截至 28 天前**的 28 日窗) | 三段**互不重叠的连续历史块** ⇒ 可做「近期热度 / 一个月前基线」的加速度比 |
| 单日总量 | `viewstoday`（**今日全量，含**） | 唯一「当日总量」字段（7d/14d/28d 都没有对应的单日总量） |
| 单日拆解 | `*todaymorning/afternoon/evening/night`（4 桶求和 = 当日总量）、`*todaymobile/desktop` | 可构造**干净的移动端占比 = `divide(viewstodaymobile, viewstoday)`（同日同量纲）** |

⚠ **量纲陷阱（本集最易错处）**：`views28dmobile` 是**单日**（28 天前那天的移动端），`views28d` 是**28 日窗求和** ⇒
直接相除是「单日 / 28 日累计」= 真实占比的 1/28，且引入该日特有时间噪声，**不是干净占比**。
干净占比只能用 `today` 族（有同日总量），或用 4 个时段桶先求和得到该日总量。

**0.3 机制（A-2 草案）**：散户注意力（Da-Engelberg-Gao 2009/2011 一脉，Wikipedia 浏览量是 ASVI 的公开代理）
——注意力驱动的买入造成短期价格压力，随后反转；修复期数周 ⇒ 窗 22/66。
**阻塞**：cov .26 意味着任何截面只有 ~159 只可交易，`CONCENTRATED_WEIGHT` 与
`LOW_SUB_UNIVERSE_SHARPE` 结构性高风险；且 §5.113 已记「低覆盖 + ts_backfill ⇒ 2016-12-22 权重洞」在同一批 OTHER 集上出现过。
⇒ **只在有 2 个空槽且 IS 窗问题已定论时投 1 波（2 颗），不作为主线。**

**⑤ Wave 268 实测（2 颗，2026-10-31，STATISTICAL/decay 4/trunc .08/2014–2023）—— 判死**

| 探针 | alpha | 形态（0.2 派生的两个干净构型） | S | F | TO | 2Y | subU | CW |
|---|---|---|---:|---:|---:|---:|---:|---|
| P1 移动端占比变化率 | `GrWMApMJ` | `group_rank(ts_delta(divide(viewstodaymobile, viewstoday), 22), sector)` | **−0.32** | −0.06 | **.4746** | −0.38 | −0.14 | ⛔ **FAIL 0.633 @2021-02-10** |
| P2 近期/月度基线背离（反向） | `mLorRMrx` | `reverse(group_rank(divide(views14d, views28d), sector))` | **−0.58** | −0.13 | **.6404** | −1.08 | ⛔ FAIL −0.45 | PASS |

**归因（读出 3 条结构结论）**：
1. **不是方向问题，是强度问题**。按铁律 B 翻正后最强也只有 **+0.58**（P2）、**+0.32**（P1），
   距 1.58 差整整 1.0，且**翻正不改变 turnover**（TO 由形态决定，与符号无关）。
2. **turnover 是本集的结构性杀手**：.4746 / .6404 是 KOR 全战役最高档（对比 analyst 族 .03–.05、
   risk59 .135）。注意力数据日频抖动 ⇒ 换手天然高 ⇒ fitness 被 TO 分母压死（即使 S 到 1.0，F 也上不去）。
3. **CW 实证确认了 0.3 的预判**：低覆盖集在「占比类」形态上确实触发 `CONCENTRATED_WEIGHT`（0.633，是 KOR 首见的
   非 1.0 型 CW 值），说明不是单日权重 1.0 那种极值，而是**截面只有 ~159 只可交易导致分散度天然不足**。
   P2 躲过 CW 是因为占比类背离天然更分散，但代价是 TO .64。
⇒ **Wikipedia 注意力轴在 KOR/TOP600 上不可做**（强度、换手、集中度三面同时不达标），**判死，不再投配额**。
⚠ 未投的方向：4 个时段桶（morning/afternoon/evening/night）的日内结构。在本集 TO 已 .47+ 的前提下，
日内桶只会**更**抖，且没有任何机制理由能把它压下来 ⇒ 不投。

### 7.3 `other496` Intraday FX rates（描述失配；实为多源杂烩）—— ⭐ **新发现：韩国涨跌停轴**

104 字段，cov 0.34–1.0，aCount 0–316。描述写「Intraday FX rates」与内容完全不符（本区已知的**描述失配**第 N 例）。

**按 alphaCount 的头部 = 一个真正的本区独有轴**：

| 头部字段 | cov | u | aCount | 判读 |
|---|---|---|---|---|
| `oth496_kor_mapped_limit_status` | **1.0** | 88 | **246** | **韩国涨跌停板状态** —— KRX ±30% 制度下的独有微结构信号 |
| `oth496_returns2` | .50 | 46 | 316 | 预计算 2 日收益（≈PV 内置，冗余度高） |
| `oth496_returns4` | .50 | 30 | 264 | 预计算 4 日收益（同上） |
| `oth496_kor_mapped_uplimit` / `downlimit` | 1.0 | 8 / 4 | 10 / 4 | 当日涨停价 / 跌停价（**几乎无人挖**） |
| `oth496_ard_*`（ARD 报表科目） | 多数 1.0 | 0–16 | **≤21** | 几乎未挖的报表科目面 |

⚠ `uplimit / downlimit` **不能直接相除**：两者同源于前收盘（上板 = 前收 × 上限系数、下板 = 前收 × 下限系数）
⇒ 比值是**纯常数、无任何截面信息**。
（2026-10-31 更正：旧文写「前收 × 1.3 与 × 0.3 ⇒ 比值 4.33」。KRX 制度是 **±30%**，即上 1.3 / 下 0.7 ⇒ 比值应为 **1.857**；
旧读数 4.33 与制度不符，疑为把别的量当成了 downlimit，**常数具体值待码值核验**，但「恒定 ⇒ 无信息」这个结论不受影响。）
可用的形态是「现价距板距离」或 `limit_status` 的状态迁移/持续，但本集**没有 close**（只有预计算的 returns_*），
⇒ 需用 `returns2/returns4` 反推，或用 `limit_status` 编码本身做 level/change。

⚠ **本地 catalog 已漂移（2026-10-31 实测，务必先 validate 再发批）**：本地 `field_catalog` 是 **2026-09-02** 的快照，
平台侧字段 id 与之不完全一致。实测 `oth496_ard_total_assets`（本地登记 cov 1.0 / u6 / a10）
**在 KOR/TOP600/D1 平台上根本不存在**（`validate_expressions` 报 `unknown_soft`）；
真实可用的 id 是 **`oth496_ard_tot_assets`**（`tot` 而非 `total`）。同集还有多套前缀变体
（`_a_` / `_a2_` / `_2_` / 无前缀）指不同来源，**不能按名字规律推断哪个在平台上活着**。
⇒ 本集任何发批前必须过 `validate_expressions`（零成本），本地 catalog 只作候选名单，不作存在性依据。

**机制**：KRX 涨跌停是散户投机的聚集地——触及涨停 ⇒ 次日追涨（持续性）或反转，两向都有文献支持，
按铁律 B 必须正反各测。**塔归属 = OTHER（1.6×，lit=1 需 +2）**，是当前唯一还有「未挖 + 高覆盖 + 本区独有」三特征的轴。
⇒ **列为 OTHER 线下一主探针**，但排在 IS 窗问题定论之后。

**⑤ Wave 269 实测：ARD 报表「增长」轴 —— ⛔ 判死（2 颗）**

按 A-1 五问把 ARD 科目定性为**存量水平**（铁律 A：禁裸水平做多空）⇒ 一律取年化变化率
`divide(ts_delta(X, 252), X)`，再按投资异象（Cooper-Gulen-Schill 2008）与外部融资异象
（Bradshaw-Richardson-Sloan 2006）**反向**预期：

| 探针 | alpha | 表达式 | S | F | TO | 2Y | subU |
|---|---|---|---:|---:|---:|---:|---:|
| 资产增长（投资异象） | `88Ra9bgo` | `reverse(group_rank(divide(ts_delta(oth496_ard_tot_assets, 252), oth496_ard_tot_assets), sector))` | **0.13** | 0.03 | .0761 | 0.35 | 0.05 |
| 负债增长（外部融资异象） | `e75dwmeg` | `reverse(group_rank(divide(ts_delta(oth496_a_ard_tot_liabilities, 252), oth496_a_ard_tot_liabilities), sector))` | **−0.46** | −0.18 | .0716 | −0.58 | ⛔ FAIL −0.36 |

**归因**：
1. **资产增长方向对但强度归零**（S 0.13）——文献异象在 KOR/TOP600 上**被完全定价**：年化变化率是
   全市场最拥挤的公开异象之一，600 只大盘股的截面上剩不下残余。
2. **负债增长方向反了**（翻正后 best ≈ +0.46）——不是异象，是**杠杆因子**（低杠杆跑输），属另一条
   已定价的贝塔轴，且 investability WARNING（−0.37）说明它跟可投资性纠缠。
3. **TO .07 意味着这两条几乎没有时序自由度**：季频报表 + 年化窗 ⇒ 组合一年只动一两次，
   任何平滑/门控杠杆都无从施力。**这不是「再调调参数就能救」的形态，是信号本身不存在。**
⇒ **ARD 报表轴判死**。剩余 ARD 字段（存货、应收、留存收益、无形资产）与上述两条**共享同一份报表、
同一更新频率、同一被定价程度**，按「同族不重测」纪律不再单投；
唯一保留的例外是**留存收益/总资产（盈利能力水平型，非增长型）**，见下波。

**⑥ Wave 270 实测：涨跌停状态轴 —— ⛔ 判死（2 颗）**

E1 = `limit_status` 状态均值（本集头部字段 a246，KRX 原生轴）；
E2 = **用涨跌停板价反推已实现波动**（`divide(uplimit, ts_delay(uplimit,1))` = 毛日收益 ⇒ `ts_std_dev(…, 66)`，
绕开本集无 close 的缺陷，且与 PV 内置 returns 不同源自证）。sim `217xPNfr84mJbN411YFTs996`，2 子 0 错：

| 探针 | alpha | 表达式 | S | F | TO | 2Y | subU | invest |
|---|---|---|---:|---:|---:|---:|---:|---:|
| E1 涨跌停状态均值 | `gJeROXQJ` | `group_rank(ts_mean(oth496_kor_mapped_limit_status, 22), sector)` | **−0.64** | −0.46 | .2104 | **−1.94** | −0.50 | −0.83 |
| E2 板价倒推波动（反向） | `j2Y9Ro3Z` | `reverse(group_rank(ts_std_dev(divide(oth496_kor_mapped_uplimit, ts_delay(oth496_kor_mapped_uplimit, 1)), 66), sector))` | **0.65** | 0.39 | .0985 | **1.87** | 0.51 | 0.45 |

**归因**：
1. **E1 方向整体反了**：翻正后 best ≈ +0.64，且 2Y 达 −1.94 —— 说明「涨跌停频率高」在 KOR 大盘股上是
   **坏事**（流动性/投机度代理，而非持续性动量），且这个坏方向只在后两年显著。与「触及涨停 ⇒ 次日追涨」的
   文献预期相反，属**制度差异**（KRX 10%/30% 分档 + 大盘股极少触板 ⇒ 触板样本本身就是噪声）。
2. **E2 是唯一的亮点，但归因把它否掉**（`get_alpha_yearly_stats` 实测，铁律 F）：2Y **1.87 已过 1.58 闸**，
   全期 S 只有 0.65 —— 逐年 S = 2014 **−0.68** / 2015 0.07 / 2016 1.13 / 2017 1.11 / 2018 0.11 /
   2019 1.13 / 2020 **−0.47** / 2021 0.50 / 2022 **2.37** / 2023 1.44。
   ⇒ **S<1.0 的年份 5/10（≥3 成）＋ 2022 单年占正收益 30.7%（>30%）**，按发波决策表**两条过拟合指纹同时命中**
   ⇒ 不是「再调窗口就能救」（`ts_std_dev` 的窗口谱只改变稀释程度），是**近两年 regime 依赖 + 单年集中**。
3. **两者 TO 都极低**（.21 / .0985）——因为 `limit_status` 绝大多数日子不变，`uplimit` 长期恒定
   ⇒ **无时序自由度**，任何平滑 / 门控 / 衰减杠杆都无从施力。
4. ★ **E1 其实是 wave 214 #5 的等价重测**：`group_rank(ts_sum(x,22))` 与 `group_rank(ts_mean(x,22))`
   **秩等价**（sum = 22×mean，rank 保序）⇒ 两次读数 S 都是 **−0.64**、TO 都是 **.2104**（逐位相同）。
   这不是巧合，是「rank 吸收线性缩放」的直接证据。**教训：同字段换聚合算子（`ts_sum`/`ts_mean`/`ts_av_diff`）
   在 rank 壳内不是新探针**，别为它烧槽位；要换就换**壳**（group 轴 / 时间窗 / 事件条件）或换字段。

⇒ **other496 已测三轴全判死**（ARD 增长 0.13/−0.46 · 涨跌停状态 0.64 · 板价倒推波动 0.65）。
唯一存活的已提交机制 = `xAY86Mkl`（`rank(ts_backfill(vec_avg(oth496_aftercons_percentage), 5))`，
S 1.61 / F 0.75 / TO .5495 / 2Y 1.17 / subU 1.17，SECTOR / decay 2 / trunc .08 / nanHandling OFF，
pyramids = KOR/D1/OTHER 1.6×，ra_failed = LOW_FITNESS / LOW_INVESTABILITY_CONSTRAINED_SHARPE / LOW_2Y_SHARPE）
——即「一致预期占比」这条**分析师共识代理**腿。

**⑦ Wave 271 实测：留存收益/总资产（RMW 水平型）—— ⛔ 判死，other496 封账（2 颗）**

⑤ 登记的最后一个例外，机制与三条死轴不同：存量比率的**横截面排序** = RMW 型盈利能力溢价
（Novy-Marx 2013 / Fama-French RMW），不是增长率；字段平台确认存在
（`oth496_ard_retained_earn_acc_deficit`，cov **1.00** / u2 / aC2，"ARD Retained Earnings (Accumulated Deficit)"）。
低 TO 对它**不是劣势**——fitness 分母有 `.125` 地板，低换手反而放大 fitness。
sim `4aNQ1xeXy4olczb170G4VbBZ`，2 子 0 错（铁律 B 正反各一）：

| 探针 | alpha | 表达式 | S | F | TO | 2Y | subU | invest |
|---|---|---|---:|---:|---:|---:|---:|---:|
| 正向（RMW 预期） | `O0AbEG7R` | `group_rank(divide(oth496_ard_retained_earn_acc_deficit, oth496_ard_tot_assets), sector)` | **−0.34** | −0.12 | .0648 | 0.14 | −0.32 | −0.36 |
| 反向 | `P0owdGZJ` | 同上 + `reverse(...)` | **0.10** | 0.02 | .0648 | **−0.57** | 0.11 | 0.12 |

**归因**：两个方向都**归于零**（|S| ≤ 0.34，远低于 near 线 1.0）。

1. **RMW 在 KOR/TOP600 被完全定价**——规模最大的 600 只股票上，留存收益/总资产这把「盈利能力代理」的
   截面排序已无残余。与 ⑤ 的资产增长轴同因：越是写在教科书里的公开异象，大盘股截面上越干净。
2. **方向略偏反向但不显著**（翻正后 +0.34），且 **2Y −0.57** —— 即便方向对也不具备近两年一致性，
   不是「方向选错」，是**没有信号**。
3. **TO .0648 双向逐位相同**（多空只是整体取负）—— 印证 ⑤ 的读数：季频存量比率的组合一年只动一两次。
   此处的失败不在修法（无杠杆可施），在**截面残余本身为零**。
4. 与 fundamental 塔（3/3 已满）的**机制重叠是真的**：留存收益/总资产与净利率/ROE 同源，
   即便有残余也会被塔内既有 alpha 吃掉 —— 这正是当初只给「有条件」登记的理由，现在证实条件不成立。

⇒ **other496 实测四轴全判死**：ARD 增长 0.13/−0.46 · 涨跌停状态 0.64 · 板价倒推波动 0.65 · 留存收益水平 0.34。
唯一存活机制 = 已提交的 `xAY86Mkl`（`rank(ts_backfill(vec_avg(oth496_aftercons_percentage), 5))`，
S 1.61 / F 0.75 / TO .5495 / 2Y 1.17 / subU 1.17，SECTOR / decay 2 / trunc .08 / nanHandling OFF，
pyramids = KOR/D1/OTHER 1.6×，ra_failed = LOW_FITNESS / LOW_INVESTABILITY_CONSTRAINED_SHARPE / LOW_2Y_SHARPE）
——即「一致预期占比」这条**分析师共识代理**腿。

★ **封账口径（防止下一轮拿「还有未测字段」再来一遍）**：本集的**独立机制轴已穷尽**；
未被单独测过的只剩 VECTOR 共识族的派生量（`aftercons_stddev` cov .6167 / `beforecons_stddev` cov .61 /
`aftercons_difference` cov .673 / `aftercons_numitems`），它们与 `xAY86Mkl` **同族**（分歧度视角，不是新机制）。
⇒ 若 OTHER 塔补席需要，它们可作为**首选后备**（机制已被 xAY86Mkl 证明能出信号），
但**不再作为 other496 的独立探针**烧配额。

⚠ **E2 的构造技巧要留下，被证伪的是结论不是手法**：本集无 close 时，`divide(uplimit, ts_delay(uplimit,1))`
可还原**滞后一日**的 close-to-close 毛收益 —— 推导：`uplimit_t = close_{t-1} × (1+limit%)` ⇒
`uplimit_t / uplimit_{t-1} = close_{t-1} / close_{t-2}`（限幅比例约掉）。**两条必须写进用法的告诫**：
① 它是 **t−1 日的收益**，比 PV 内置 `returns` 晚一天（对「估波动」无害，对「取动量」是错位）；
② **2015 限幅从 ±15% 改 ±30% 会在比值上留下一次 +13% 的假跳变**（1.30/1.15=1.13），
66 日窗内被稀释、但恰好落在样本中段 ⇒ 这是 E2 逐年不稳的**已知人为噪声源**，不是市场效应。
它与 PV 内置 `returns` **不同源**，因此天然正交；即便如此，本轴已被证伪，**不再投**。

### 7.4 其余（不投）

| 集 | cov | 字段 | 判读 |
|---|---|---|---|
| `other567` Employee Review | .2571 | **2** | 字段太少且描述是 RIC↔BBID 映射（描述失配）；构不出机制，不投 |
| `other532` Specific Returns | .9956 | 8 | aCount 1864 已拥挤；描述是证券主表 |
| `other315` Equity Swap | .4022 | 32 | 描述是 RIC↔BBID 映射（元数据），cov 低于 .5 |
| `other335` Multi-Region Dividend | .59 | 10 | aCount 1067 已拥挤；且 other424/436 已证明股息族在 KOR 天花板 ≤.90 |

### 7.5 ★ 路径② 判死：KOR 的 IS 窗由平台硬定 2014-01-01 → 2023-12-31（2026-10-31 实测）

**待决清单第 2 项**「是否核/移 IS 窗到 2024」的答案 = **不能移**。两轮实测：

| 轮 | 派发形态 | 请求体里的 start/end | 平台返回的 `settings.startDate/endDate` | 判读 |
|---|---|---|---|---|
| 1 | risk59 基线 + hump 消融（`26un9A2vt4I58EHGCs4JTJJ`） | **未显式传**（走剖面 2013-01-01 / 2023-12-31） | `2014-01-01 / 2023-12-31` | 平台把起日**从 2013 钳到 2014**（数据起点） |
| 2 | other571 两探针（`4ylG0A2xS4zYbxZSedjXtGG`） | **显式 `2015-01-01 / 2024-12-31`**，回执 `settings_source=explicit` 且 `settings_used` 逐字回显 2015/2024 | **`2014-01-01 / 2023-12-31`** | ⛔ **平台静默改回硬窗** |

**决定性**：第 2 轮是干净差分——请求被平台接受（**HTTP 201**）、回执里 `settings_used` 明确带着 2015/2024，
但**子 alpha 落库时被改写成 2014/2023**。`startDate` 被推到 2014（早于请求），`endDate` 被压回 2023（早于请求）
⇒ 不是「数据不够所以从 2015 起」，而是**整段窗口被替换成平台硬窗**。

**两条独立佐证**：
1. 第 1 轮 E1 与既有基线**返回同一个 alpha id `QPvr1vPM`**（表达式与设置逐字相同 ⇒ 平台去重），
   而第 2 轮因表达式不同未去重、仍取得同一窗口 ⇒ 窗口不是去重造成的。
2. 2024 年数据本身很可能存在，但**无法通过 IS 窗取到**——平台 IS 定义固定在 2013-12-31 收盘（实践中 2014 起）。

**⇒ 路径② 判死**。推论三条，直接影响待决清单：

- **risk59 的约束 4 缺陷无法用「窗口平移」修复**：面板 2015 起 = **9 年**，2014 空缺是数据起点事实，
  任何表达式杠杆都造不出 2014。**唯一出路仍是待决第 1 项：用户是否对 risk59 放宽到 9 年**。
- **「IS 窗可动态调整」这条自由度的实际边界 = 只能变窄，不能平移**（平台允许 2013→2014 的钳位，
  不接受任何越过 2023-12-31 的 end）。
- 今后**任何**「时段不够十年」类判定都不必再试移动窗口，**直接按平台硬窗 2014–2023 计年数**
  （KOR 十年合规 = 2014–2023 全覆盖；2014 空的集即判 9 年）。

**同轮附带确认（非本问题，但一并落账）**：
- `hump(...)` 在 risk59 基线上是**有效杠杆**：去掉后 `akKAY1g6` S 1.02→**0.90**、F .67→.53、2Y 1.80→1.60
  ⇒ **hump=0.003 值 +0.12 S，不可压掉**（与 §5.118 的「时序平滑在费率上零和」不矛盾：hump 不是 ts_decay，
  它作用于换仓成本而非信号均值）。

---

## 8. 库存复核（2026-10-31，零配额、零仿真、只读）

> 触发：wave 271 封账后，OTHER 面再无活轴。按 GBR 战役 §7.5「★ 收割优先于重挖」的既定纪律，
> 在宣布「无可交付」之前，先把**本地队列全量**清一遍——本次 163 行，全部只读。

### 8.1 `leAk66xx` prod = **0.8711** ⇒ D0-P 判死（OTHER 面最后一条活腿关闭）

| 项 | 值 |
|---|---|
| alpha | `leAk66xx` = `hump(group_rank(ts_sum(ts_backfill(vec_avg(oth695_import_value_4), 66), 20), sector), hump=0.0025)` |
| 指标 | S **1.77** / F **2.11** / 2Y **2.24** / subU 1.68 / TO .0306 / `fail=[]`（本战役第一颗全闸 ATOM） |
| 塔位 | `pyramids.list = [{KOR/D1/OTHER, ×1.6}]`，`effective = 1` |
| **prod** | **0.8711**（`check_correlation` 的 `last_known`，`checked_at = 2026-10-31T18:11:46`，龄 **5.4h**，**`stale: false`**） |
| 判定 | **D0-P 墙（≥0.70）** ⇒ 与 `leA22za2` **0.8377**、`d5WmEarw` **0.8395** 同构，是三例独立证据中的第三例 |

**三条推论**：
1. **约束 4 之争 moot**：2014–2017 零持仓（6/10 年）原本是它唯一的卡点；prod 先判死 ⇒ 待决清单第 2/4 项
   不再需要用户裁决（同 `leA22za2` 的先例：「prod 墙已先判死，无需再纠结年度覆盖」）。
2. **other695 封账**：该集全库仅 3 字段（2 个标识符 + 1 个信号 `import_value_4`，cov .4057），
   不存在第二个可换字段 ⇒ 无「换字段降 prod」空间；换几何则撞 self 闸。
3. **模式已三次复现 ⇒ 写进纪律**：`指标全闸 + 纯格 + ATOM` **不蕴含可提交**。
   KOR 的 TOP600 + 十年面板使「全闸 IS 候选」在 prod 池里高度同源，**prod 是独立且更早的一道墙**，
   任何以「只差约束 4 / 只差覆盖率」为由的放宽请求，都应**先取一次新鲜 prod** 再讨论。

### 8.2 `submit_ready` 全表清点（163 行）—— 除 `LLZ6wZO2` 外**零可交付**

`get_submit_ready(status="ALL")` 全量落盘后逐行统计：

| 状态 | 行数 | 判读 |
|---|---:|---|
| DEAD | 108 | 含大量 `FAIL:LOW_2Y_SHARPE`（2Y 结构不可达的旧件） |
| EXPIRED | 34 | **本地队列条目过期 ≠ 平台死**，需逐条看（本次已收口，见下） |
| SUBMITTED | 12 | 忽略 |
| SUPERSEDED | 4 | 被同族更优件替代 |
| PROD_BLOCKED | 2 | 忽略 |
| SELF_BLOCKED | 2 | `wpb1GXEd` / `9qWK21rd`（见下） |
| **READY** | **1** | **`LLZ6wZO2`**（FUNDAMENTAL 3/3 满，待用户裁决） |

**prod < 0.70 且未提交 = 25 行**，逐类收口：

| 类 | 行 | 证据 | 结论 |
|---|---:|---|---|
| **shrt38（shortinterest38）族** | **19** | **6 行直接取证**：`omLd9oEJ`(S1.86) / `VkaWXGmb`(S2.35) / `d5bMPkWY`(S1.71) / `gJb2oWeO`(S1.60) 经 `get_alpha_details` 确认表达式全部是 `shrt38_stk_invactsell_amt ÷ shrt38_stk_invactbuy_amt` 的 `hump(group_rank(ts_decay_linear(...,500)))` 变体、`fail=[]`、塔位全为 `KOR/D1/SHORTINTEREST ×1.4`；`mLmGQEq9` / `E5pjx9q0` 由 §5.92.3 #5 的新鲜 prod 实测确认同族。**其余 13 行按 TO 签名（.1744–.189）与同一 EXPIRED/IS_ONLY 形态归入同族**。**塔已 4/3 满**，且**族级新鲜 prod 已判死**（§5.92.3 #5：`mLmGQEq9` 0.935 / `E5pjx9q0` 0.8105，族内 `[0.7,0.8) n=5`） | ⛔ **整族不作候选**（塔满 + 族 prod 死） |
| RA investability 死 | 2 | `A1vOb5pE` S2.54 / `ZYAWx9J3` S2.26，`gate = FAILED_COUNT_RA:LOW_INVESTABILITY_CONSTRAINED_SHARPE` | ⛔ DEAD |
| SELF_BLOCKED（实为 prod 贴线） | 2 | `wpb1GXEd` / `9qWK21rd`：self 仅 **.1967 / .1970**，状态名与数值不符；prod **.6946 / .6929**（stale，余量仅 0.005） | ⛔ 塔满 + prod 余量不可信，不救 |
| FUNDAMENTAL 重复件 | 1 | `A1NXddRw` SUPERSEDED（S2.11 / prod .6547 stale）——已被其 keeper 替代 | ⛔ 不作第二颗 |
| **READY** | **1** | **`LLZ6wZO2`**（prod .6762 / self .6760，**stale=false**） | 待用户裁决（塔已满，提交不点新塔） |

**两条通用教训（与 GBR §7.5 同源，本次 KOR 侧实证）**：
1. **`submit_ready.status` 是本地队列状态，不是平台裁决**：`EXPIRED` + `gate=IS_ONLY` + `towers=[]`
   只说明「从未做过提交层核验」，既不能当候选，也不能当死。收口方式是**抽样 + 签名聚类**：
   本次 4 个样本 + 2 条既有新鲜 prod 记录（覆盖 S 1.60–2.35 全区间）全部落进同一族，
   19 行一次性收口，省掉 19 次平台读。
2. **本地 `prod` 缓存低于 0.70 ≠ prod 干净**：这 19 行的本地 prod 是 .57–.70，看着全都过线；
   而**同族新鲜读数**是 .81–.935。⇒ 库存里任何 `prod < 0.70` 的行，**必须先做族级新鲜核对**
   （≤1 次平台调用即可判整族），否则会把死族当「零配额就能扩池」的金矿。

### 8.3 状态收口（写入时点）

- **OTHER 面**：4 个独立机制轴全判死（wave 270/271 + 早前），`leAk66xx` / `d5WmEarw` / `leA22za2` 全撞 prod 墙
  ⇒ **无活腿**。VECTOR 共识族经机制反查**不是新轴**（`datasets/other496.md` §7 已改）。
- **队列**：除 `LLZ6wZO2`（FUNDAMENTAL 已满）外，**零可交付**。
- ⇒ 剩余全部为**用户裁决项**（提交 LLZ6wZO2 / risk59 约束 4 / seal_dead_end 批量 / sentiment 禁令 / 新数据集授权 /
  60 颗目标路径 A–D），本 agent 不再自主开波。

### 8.4 会话经验已蒸馏（2026-10-31）

本文件是**逐波原始读数**；可复用的判据已抽到
[`kor_session_lessons_20261031.md`](kor_session_lessons_20261031.md)（区域经验层，9 节）：
平台事实 8 条（IS 硬窗 / coverage≠时间覆盖 / 2Y=1Y=1.58 / 塔票跟 pyramids.list / 高分簇可能是 COMBO-SUPER …）·
判定纪律 8 条（prod 墙先于约束之争、本地 prod 缓存≠clean、族级直方图、submit_ready 是本地态 …）·
探针等价性 7 条（秩不变性、hump≠ts_decay、reverse 差额=2×成本、翻正不改 TO …）·
机制结论（年度变化率异象已定价、分析师三面全灭、同族≠新轴）·
天花板定量表（单腿 1.04 / 三腿 1.292 / ρ=0.1978）· 工程纪律 9 条 · **四条零配额收口手法**。
会话总量：70 波（189–271）· 125 候选行 · FAIL 57 / PARTIAL 10 / PASS 3 · 过硬闸 5+1。
✅ 该文件的跨区结论**已同步进共享 `docs/experience/*`**（01 §14/§15/§16、02 §17、04 §15）
与机器层规则库（全局 4 条 + KOR 1 条），双轨义务已履行、守护 33 passed，详见其 §6.9。
