# 字段画像 · equity_forum_data（KOR / TOP600 / D1 / other）

> 画像日期：2026-11-18。角色：字段画像员（只画像归档，不发仿真）。
> 数据源（本轮实跑）：
> - `mcp__wq-brain-http__get_datafields(region=KOR, dataset_id=equity_forum_data, universe=TOP600, delay=1, filter_sharpe=false)` → `count=6, platform_count=6, complete=true, pages_fetched=1, returned=6, ordering_scope=KOR/TOP600/D1`。
> - `mcp__wq-brain-http__get_datasets(KOR, delay=1, TOP600, category=other, search=equity_forum_data)` → coverage=0.8948, fieldCount=6, alphaCount=17, userCount=13, pyramidMultiplier=1.6, category=other。
> - `mcp__wq-brain-http__get_pyramid_alphas()` → KOR/D1: other=**2**（near-gate 2/3），analyst=4, fundamental=3, model=3, insiders=3, risk=3, pv=2, shortinterest=4, news=0, earnings=0, institutions=0, macro=0, sentiment=0, socialmedia=0, imbalance=0。
> - `mcp__wqb-db__get_dead_ends(region=KOR)` + 直读 `data/wqb.db` `registry_empirical`（按 entry_id 精确查询，id=80）→ `KOR-FORUM-DEAD`（见 §5）。
> - `mcp__wqb-db__query_field_profile(KOR, dataset=equity_forum_data)` → 6/6 行 verdict=`UNTESTED`, n_tests=0, best_s=null（DB 未回写 2026-11-06 的实测，实测读数以 §4 的 backtest_results 为准）。
> - 直读 `data/wqb.db` `backtest_results`（`alpha_id IN (...)`）→ §4 八条逐条读数。
> - 前序档案：`tracking/KOR/campaign_20261106_socialmedia_atom/s1_field_profile_equity_forum_data.md`、`wave1_dispatch_result.md`、`wave1_harvest.md`。

---

## 0. 结论先行（给编排器的诚实摘要）

1. **全字段探测完成**：6/6 字段逐字段列 id + 逐字段带数字读数（下表），无抽样、无通配。
2. **塔位属实**：KOR/D1 `other` = **2/3**（本季平台实读，非路线图 §0 的旧 "1/3"），near-gate，乘数 1.6。塔位论据成立。
3. **⛔ 候选理由「判死台账无命中」不成立**：权威 DB 存在 **active（未 REVOKED）** 的 `KOR-FORUM-DEAD`，`family='equity_forum_data 论坛情绪/注意力'`，原文点名「勿再挖 equity_forum_data 及同类论坛评论量/注意力信号」。路线图 §4「禁区」亦把 equity_forum_data 列入新闻情绪/标题语气/事件评分族。与 `KOR-FUND-HOLDINGS-PANEL-DEAD`（2026-11-17 用户明确 REVOKED）不同，本条**未见任何撤销记录**。画像员无权撤销判死，按现状如实上报。
4. **用户路线图 §1「news 幸存机制 = 注意力计数/事件计数」不能直接移植到本集**：该结论描述的是 `news7` 残余未试轴，而本集 `equity_forum_data` 的注意力计数轴已在 wave86 实测判死（见 §5），二者不是同一数据集。
5. **核心字段非「慢变量横截面水平/规模代理」**：全部为 VECTOR 论坛意见分与计数（流量型），按任务特指的规模代理风险点是 **不适用（N/A）**——不存在持股比例/治理评分/股本结构/市值余额类字段。但意见分带 sentiment 色彩，须先过 CW≤0.1 与零仓探针（§6）。
6. **推荐回测档**：KOR/TOP600/D1/STATISTICAL/decay4/trunc0.08/nanHandling OFF/maxTrade OFF，VECTOR **必须 `vec_*` 降维 + `ts_backfill` 补有效覆盖**——但基于 §4/§5，本集应**先做 1–2 条裸探针验 IS 强度与有效覆盖，再决定是否投完整波次**，不建议直接开大波。

---

## 1. 字段全表（分母 = 6，逐字段真实 id，平台 description 逐字）

| 字段 id | type | coverage | alphaCount | userCount | dateCreated | pyramidMultiplier | description（平台原文，唯一语义依据） |
|---|---|---:|---:|---:|---|---:|---|
| `aggregate_buy_opinion_score` | VECTOR | 0.8948 | 5 | 4 | 2026-03-01 | 1.6 | Combined buy sentiment score from all sources for an instrument. |
| `aggregate_sell_opinion_score` | VECTOR | 0.8948 | 7 | 5 | 2026-03-01 | 1.6 | Combined sell sentiment score from all sources for an instrument. |
| `aggregate_comment_volume` | VECTOR | 0.8948 | 3 | 3 | 2026-03-01 | 1.6 | Total number of comments posted across all sources for an instrument. |
| `comment_volume_per_platform` | VECTOR | 0.8948 | 4 | 4 | 2026-03-01 | 1.6 | Total number of comments posted on the source platform for an instrument. |
| `total_distinct_participants_count` | VECTOR | 0.8948 | 1 | 1 | 2026-03-01 | 1.6 | Number of unique users participating across all sources for an instrument. |
| `distinct_user_count_per_platform` | VECTOR | 0.8948 | 0 | 0 | 2026-03-01 | 1.6 | Number of unique users participating on the source platform for an instrument. |

口径核对：`alphaCount` 逐字段 5+7+3+4+1+0=20（字段级和），数据集 `alphaCount=17`（平台按 alpha 去重），二者不同源、不矛盾。`userCount` 13 为数据集级去重值。

---

## 2. 逐字段实测读数表（每字段带数字；本轮或本仓真实回测/元数据）

> 列含义：cov/日期/aC 来自本轮 `get_datafields`（§1）；「历史实测」列来自 `backtest_results` 表逐条查询（§4），每个字段至少 1 条带数字的实测读数；「有效覆盖」= 本仓未对该集跑法1 Long Count，标 `未跑`（诚实标注，不臆造）。

| 字段 id | 类型 | cov(元数据) | aC | 历史实测（alpha_id / S / 2Y / TO / CW） | 法1有效覆盖(Long Count/universe) | 可用性裁决 |
|---|---|---:|---:|---|---|---|
| `aggregate_buy_opinion_score` | VECTOR | 0.8948 | 5 | `wpQ25bov` S=0 / TO=0 / PnL=0；`9qxd9WGK`（buy−sell）S=0 / TO=0 | 未测（元数据 cov=0.8948，仅供排序） | opinion 族零仓 → 数据层疑似无有效截面；先零仓探针 |
| `aggregate_sell_opinion_score` | VECTOR | 0.8948 | 7 | `WjOoNelP` S=0 / TO=0 / PnL=0 | 未测（元数据 cov=0.8948，仅供排序） | opinion 族零仓 → 数据层疑似无有效截面；先零仓探针 |
| `aggregate_comment_volume` | VECTOR | 0.8948 | 3 | `QPvNnKvM` S=0.21 / 2Y=0.82 / TO=0.1101 / F=0.07；`omEJnWa5`(std) S=0.38 / 2Y=1.27 / TO=0.1132；`P0oYngo7`(Δ22) S=0.04 / TO=0.3415 / **CW FAIL** | 未测（元数据 cov=0.8948，仅供排序） | 注意力计数轴历史最强 |S|=0.38<0.5；Δ 形态触发 CW |
| `comment_volume_per_platform` | VECTOR | 0.8948 | 4 | 本仓无独立单字段回测读数（仅 §1 元数据 aC=4, cov=0.8948, dateCreated 2026-03-01）；同族 aggregate_comment_volume 实测 |S|≤0.38 | 未测（元数据 cov=0.8948，仅供排序） | 与 aggregate_comment_volume 同经济含义（评论量），对照字段；无独立实测，只能作门控/对照候选 |
| `total_distinct_participants_count` | VECTOR | 0.8948 | 1 | `e75VnQ1M` S=0.17 / 2Y=0.79 / TO=0.1097 / F=0.05 | 未测（元数据 cov=0.8948，仅供排序） | 参与广度轴弱正，远低于资格线 |
| `distinct_user_count_per_platform` | VECTOR | 0.8948 | 0 | 本仓无独立单字段回测读数（仅 §1 元数据 aC=0, uC=0, cov=0.8948, dateCreated 2026-03-01）；同族 total_distinct_participants_count 实测 S=0.17 | 未测（元数据 cov=0.8948，仅供排序） | 最白空间（aC=0），但与广度轴同义；须先零仓/覆盖探针 |

注：`comment_volume_per_platform` 与 `distinct_user_count_per_platform` 无**独立**回测读数是事实陈述，已用其**元数据数字读数**（aC/cov/dateCreated/uC）满足「每字段带数字」；本仓未对这两字段单独回测，不伪造 S 值。

---

## 3. 语义族与角色划分（以 description 为唯一依据）

| 语义族 | 字段 | 经济含义 | 流量/存量 | 角色 |
|---|---|---|---|---|
| A 意见强度 | `aggregate_buy_opinion_score`, `aggregate_sell_opinion_score` | 多源论坛综合买/卖情绪分 | **流量型**（意见分随帖子流更新，非会计存量） | 对照（分歧价差候选） |
| B 注意力计数 | `aggregate_comment_volume`, `comment_volume_per_platform` | 评论条数（全源 / 单平台） | **流量型**（逐日帖子计数） | 主信号候选（变化量①/分位②） |
| C 参与广度 | `total_distinct_participants_count`, `distinct_user_count_per_platform` | 独立参与用户数（全源 / 单平台） | **流量型**（去重人数，滚动窗口） | 主信号候选 / 最白对照 |

**规模代理风险点（任务特指）**：本集**无**持股比例、治理评分、股本结构、市值余额类慢变量横截面水平字段 ⇒ **不适用**。所有字段是论坛意见/计数流量；「裸水平」的风险不是规模代理，而是①VECTOR 稀疏导致有效覆盖低 + CW 集中，②opinion_score 族实测零仓（§4）。因此**不适用**任务要求的「改变化量/时序分位/离散度写法来避规模代理」——但 §6 机制仍按流量型给出变化量/分位/离散度三种合规写法（这本身就是本集三类可用几何）。

---

## 4. 本仓历史实测（wave `mcp-20261106`，8 探针，逐条来自 `backtest_results`）

> 来源：`tracking/KOR/campaign_20261106_socialmedia_atom/wave1_dispatch_result.md` + `wave1_harvest.md`；读数经本轮直读 `data/wqb.db backtest_results` 复核（8/8 命中）。设置 KOR/TOP600/D1/STATISTICAL/decay4/trunc0.08/nan OFF。

| 字段/机制 | alpha_id | S | 2Y | F | TO | RA 失败项（摘录） |
|---|---|---:|---:|---:|---:|---|
| 注意力水平 `ts_mean(vec_avg(comment_volume),22)` | QPvNnKvM | 0.21 | 0.82 | 0.07 | 0.1101 | LOW_SHARPE/LOW_FITNESS/LOW_2Y |
| 注意力变化 `ts_delta(vec_avg(comment_volume),22)` | P0oYngo7 | 0.04 | 0.26 | 0.00 | 0.3415 | **CONCENTRATED_WEIGHT** + LOW_* |
| 注意力离散 `vec_stddev(comment_volume)` | omEJnWa5 | **0.38** | 1.27 | 0.16 | 0.1132 | LOW_SHARPE(0.38)/LOW_FITNESS/LOW_2Y |
| 卖意见 `vec_avg(sell_opinion)` | WjOoNelP | 0 | — | — | 0 | 零仓零 PnL |
| 买意见 `vec_avg(buy_opinion)` | wpQ25bov | 0 | — | — | 0 | 零仓零 PnL |
| 净意见 `buy−sell` | 9qxd9WGK | 0 | — | — | 0 | 零仓零 PnL |
| 注意力反臂（−水平） | rKRNbe0d | −0.39 | −1.14 | −0.17 | 0.1099 | 反臂更差，无方向可翻 |
| 参与广度 `vec_avg(total_distinct_participants)` | e75VnQ1M | 0.17 | 0.79 | 0.05 | 0.1097 | LOW_SHARPE/LOW_2Y |

**归因（前序 + 本轮复核）**：max|S|=0.38<0.5（fast-kill）；opinion 族整族零仓；注意力轴有极弱正号（<0.5）；Δ 形态触发 CW；反臂更差 ⇒ 无方向翻转可救。前序结论「换集」+ 本集已命中 `KOR-FORUM-DEAD`。

---

## 5. ⛔ 判死台账核对（与候选理由直接冲突，必须上报）

| 项 | 内容 |
|---|---|
| entry_id | `KOR-FORUM-DEAD` |
| DB 行 | `registry_empirical` id=**80**, layer=dead_end, region=KOR, family=`equity_forum_data 论坛情绪/注意力`（payload 无 status/REVOKED 字段；列 dead_at 为 NULL，payload 内 `dead_at=2026-08-22`） |
| 状态 | **active**（payload 无 `status`、`revoked_at`、`REVOKED` 字段；对照 `KOR-FUND-HOLDINGS-PANEL-DEAD` 2026-11-17 被用户明确 REVOKED，本条无此记录） |
| dead_at | 2026-08-22 |
| reason 原文 | wave86 10 项全灭：评论量/参与者/峰值全族 CW 0.85–1.0 结构性集中（2017-01-23 单日事件），负 sharpe 方向一致（−0.2~−0.83，注意力反转成立但不可用），opinion_score 族 vec_avg 全 NaN 无区分度 |
| rule 原文 | 勿再挖 equity_forum_data 及同类论坛评论量/注意力信号；事件流字段（CW 结构性集中）均需先验证 CW |
| salvage | 无。KOR 论坛幂律分布结构性无解 |
| 路线图佐证 | `tracking/KOR/reference/unlit_towers_roadmap_20261030.md` §4 禁区明确列 `equity_forum_data`（新闻情绪/标题语气/事件评分族） |
| 旁证 | `Claude/skills/wq-brain-ra-kor/references/other.md` 判死表亦列 `KOR-FORUM-DEAD` → equity_forum_data |

**画像员处置**：判死撤销权不在画像员。按 §7.6「判死档案逐维举证」铁律，`KOR-FORUM-DEAD` 仅 1 波 10 探针（D1–D6 未穷尽），其「判死」本身不完备——但这不改变它**当前 active** 的事实：任何开波前必须先由用户/战役负责人裁决是否 REVOKED（如 wave124→fhp 那样走用户指令），画像阶段只如实上报，不挪用、不清空。

---

## 6. 机制假设（5 条；格式＝机制名｜存量/流量｜经济叙事｜统计族｜预注册证伪条件）

> 全部字段为**流量型**（逐日论坛意见/计数），无一为存量型 ⇒ 长窗需谨慎（流量型宜短窗 5/22/66，长窗 252 只对「参与广度」这种滚动去重人数勉强可行）。以下每条均给可预注册证伪条件。

1. **M1 注意力过度反应反转｜流量型｜散户对高评论量股票过度关注致短期高估，随后回落（Barber-Odean 2008；Da-Engelberg-Gao 2015 注意力驱动）｜`group_rank(ts_mean(vec_avg(comment_volume), W), sector)` 水平族，W∈{5,22,66}｜证伪：若最优臂 |S|<0.5 或反臂（−水平）反而更强/同幅，则注意力反转在 KOR 不成立（wave1 反臂 S=−0.39 已临界触发）**。
2. **M2 意见分歧度（观点分歧③）｜流量型｜买卖意见同时高＝分歧大，Miller(1977) 分歧-高估效应使后续收益偏低｜`group_rank(subtract(vec_avg(buy_opinion), vec_avg(sell_opinion)), sector)` 价差单一经济含义 + `vec_stddev`(离散度)｜证伪：若 opinion 族 `vec_avg` 有效覆盖=0（wave1 已 S=0/TO=0，wave86 记全 NaN），则数据层排除，机制不可测；须先跑零仓探针**。
3. **M3 注意力计数变化①｜流量型｜评论量/参与人数的环比上升＝新增关注冲击，短期动量或反转｜`ts_delta(vec_avg(F), W)` / `ts_zscore(vec_avg(F), W)` 变化量族｜证伪：Δ22 已 S=0.04 & TO=0.3415 & CW FAIL；若 `ts_backfill` 补覆盖后 |S| 仍<0.5 且 CW 仍 FAIL，则变化量轴在 KOR 论坛幂律结构下不可救（wave86 同结论）**。
4. **M4 参与广度信息扩散｜流量型｜独立参与用户数（去重）上升＝信息扩散广度增加，与意见强度应分测｜`ts_rank(vec_avg(total_distinct_participants_count), W)` 时序分位族（滚动去重人数可用较长窗 66）｜证伪：广度轴历史 S=0.17（e75VnQ1M）；若分位化后 |S|<0.5 或触发 CW，则广度轴无截面信息**。
5. **M5 注意力新鲜度门（论坛 LC97552 版，本集适配）｜流量型｜只在「评论量/参与人数创近 G 日新高」的新鲜窗口内持仓，避免陈旧事件噪声｜`trade_when(ts_arg_max(vec_avg(comment_volume),G)<T, <M1/M2 持仓腿>, -1)`——`ts_arg_max` 作门控条件（冠军机制），非信号｜证伪：若门控腿本身 |S|<0.5（wave1 已如此），则门控只修 prod/robust 不造强度（IND 铁律），不应投；G/T 移植需重扫（GBR/KOR fhp 30 臂已证不可平移）**。

**规模代理声明（任务特指）**：本集无存量型水平字段 ⇒ 无「撞规模代理」机制，5 条假设均按流量型给出变化量（M3）/时序分位（M4）/离散度（M2）写法；若后续有人误用裸 `vec_avg(opinion_score)` 水平（M1），风险是零仓/覆盖而非规模代理。

---

## 7. 模板匹配（症状 → 查表 → 动作，依据 `docs/experience/07_field_profile_template_mapping.md` §六/§七）

| 本集症状 | 查表动作 | 依据 |
|---|---|---|
| VECTOR 类型（6/6） | 先 `vec_avg`/`vec_sum`/`vec_stddev` 降标量 + `ts_backfill` 补有效覆盖 | 07 §六「VECTOR 类型」；66赞手册 §14.2 |
| 元数据 cov 0.8948 但 opinion 族实测零仓 | 元数据 coverage 仅供排序，必须法1 Long Count 实测；零仓=数据层排除，不调窗口 | 07 §七 VECTOR coverage 高估实证；wave1 opinion 零仓 |
| 注意力 Δ 形态 CW FAIL（P0oYngo7） | `ts_backfill` 补覆盖 + 换分组轴；CW FAIL 不调 decay/truncation | 07 §六「CONCENTRATED_WEIGHT FAIL」 |
| 历史 max|S|=0.38（信号弱） | 换分组轴（sector→industry→subindustry）或换算子几何；**不扫窗口/常数**（换中性化救不了——配置平移律，imb5 实证） | 07 §六「信号弱」；AGENTS KOR 配置平移律 |
| 想合成 buy/sell 两字段 | 只走单一经济含义价差 `subtract(vec_avg(buy),vec_avg(sell))`；⛔ 禁 `add` 等权拼腿 | 02 §1 组合形态铁律 |
| opinion 分带情绪色彩 | 先过 CW≤0.1 与裸探针；先测零仓/有效覆盖再定去留 | 候选风险点原文 |

**量纲坑**：`add(带单位字段, 裸常数)` 报 UNITS 错（preflight 查不出）；中心化用 `ts_av_diff`/`ts_ratio`，⛔ 别写 `add(x, ts_std_dev(x,252))`（触发 POISON:equal_weight_leg_add）。本集价差用 `subtract`，安全。

---

## 8. 推荐回测设置与理由

| 设置 | 值 | 理由 |
|---|---|---|
| region / universe / delay | KOR / TOP600 / 1 | KOR `config/settings.json` 与 `other.md` 类别卡一致；TOP600 小宇宙放大 CW/longCount 问题，须盯持仓数 |
| neutralization | STATISTICAL | KOR `settings.json` 默认；`KOR-SUBINDUSTRY-PROD-SATURATED` 禁用 SUBINDUSTRY；STATISTICAL/SECTOR 为 prod 安全档 |
| decay | 4 | KOR 默认，匹配日更论坛流量；快信号上 decay 越大越差，先守 4 |
| truncation | 0.08 | KOR 默认；CW FAIL 不靠调 truncation 修 |
| nanHandling | OFF | KOR `settings.json` 默认；但 VECTOR 缺失需靠 `ts_backfill` 显式补，不靠平台 nan 填充 |
| maxTrade | OFF | KOR 默认 |
| backfill | **必要**（`ts_backfill`，窗口 22/66 起） | VECTOR 元数据 cov 0.8948 是「有记录」比例非「当日非零」比例（07 §七）；opinion 族实测零仓/全 NaN 更需先补覆盖再判死 |
| vec 降维 | **必要**（`vec_avg`/`vec_sum`/`vec_stddev`） | 6/6 VECTOR，平台不接受裸 VECTOR 入信号 |
| 波次规模 | **先 1–2 条裸探针**（验零仓 + 法1 有效覆盖 + IS 强度），|S|<0.5 即止 | 冷门数据集铁律（`KOR-ANALYST14-DISAGREEMENT-NOSIGNAL`：冷门≠有信号，先裸探针再投大波）；本集已 active 判死，探针只是画像补充 |

推荐档一句话：`TOP600/STATISTICAL/decay4/trunc0.08/nanHandling OFF/maxTrade OFF + vec_* + ts_backfill(22/66)`，**先裸探针不直接开大波**。

---

## 9. 自查（无抽样、无凭名推断）

- ✅ 6/6 字段逐 id 列于 §1，无一通配、无一「同构孪生/代表字段」。
- ✅ 每字段有带数字读数的实测行（§2）：4 字段有独立回测 S 读数，2 字段（`comment_volume_per_platform`/`distinct_user_count_per_platform`）用元数据数字 + 同族实测读数，并诚实标注「无独立回测」。
- ✅ 计数一致：§1 分母=6，§2 实测表行数=6。
- ✅ 语义全部来自平台 description 原文（§1 逐字），未凭字段名推断。
- ✅ 法1 Long Count 未跑，档案多处标 `未跑`，未臆造有效覆盖数字。
- ✅ 判死冲突如实上报（§5），未撤销、未挪用。
- 待跑机械闸：`python tools/gates/field_profile_completeness_gate.py --profile tracking/KOR/campaign_wf/wf_profile_equity_forum_data.md`（见本轮提交记录）。
