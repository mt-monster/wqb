# sentiment27 数据集画像（KOR / TOP600 / Delay=1）

> 手工维护。数据源：**平台 `get_datafields(KOR, TOP600, D1, dataset=sentiment27, filter_sharpe=false)` 实测 29/29 字段**（2026-10-30，权威）；wqb-db `get_field_catalog` 副本 aC 偏旧，勿引用。
> 金字塔归属：**KOR/D1/SENTIMENT**（乘数 **1.6**，未点亮）。

## 0. 元信息

| 项 | 值 |
|---|---|
| dataset id | `sentiment27` |
| category | **SENTIMENT**（1.6×，未点亮） |
| 结构 | 29 字段 = **29 VECTOR**，0 MATRIX |
| 覆盖 | VECTOR 族 .18–.44（两代前缀：`snl27_*` .39 / `snt27_*` .43–.44；`skewness`/`kurtosis` 仅 .18） |
| sumAC | ≈ **3400**（`snt27_avgranking_22` 单字段 aC **325**，`top75pctranking_32` aC **201**，`dltcc_38` aC **184**，`rank_39` aC **149**，`totaldomains_29` aC **140**） |
| 真实语义 | ⚠ **不是 AI 情绪分，是「域名/网站流量排名」**（Tranco 榜单口径）⇒ 归 **注意力** 家族，不是文本情绪家族 |

> ⚠ 本数据集此前在路线图里被笼统记作「网站热度族 vs AI 情绪族」——现核实**全部字段都是网站/域名流量**，
> 无任何文本情绪字段。机制必须按 **注意力**（Da-Engelberg-Gao 2011）建模，不能按情绪建模。

## 1. 字段分类（以 description 为准，禁按字段名）

### A. 排名类（Tranco rank，**数值越小 = 越热门**；量纲 1 … 1e6，重尾）

| 字段 | cov | aC | 语义 | 用法 |
|---|---|---|---|---|
| `snt27_avgranking_22` | .43 | **325** | 该主体全部域名的 Tranco 排名**算术均值** | ★ 本集第一强字段，注意力水平主轴 |
| `snt27_top75pctranking_32` | .43 | 201 | 前 75% 分位的排名 | 与均值配合成「尾部拖累」 |
| `snt27_rank_39` | .44 | 149 | 域名当日流行度排名（1=最热） | 单域名，须 `vec_avg` |
| `snt27_top50pctrankingavg_25` | .43 | 101 | 前 50% 的排名均值 | 与 `avgranking` 同源 ⇒ 可做价差 |
| `snt27_topranking_23` | .43 | 92 | 该主体**最好**（最小）的排名 | ★ 与 `avgranking` 配对 ⇒ 「旗舰 vs 平均」比率 |
| `snt27_top50pctranking_27` | .43 | 78 | 前 50% 分位排名 | 补充腿 |
| `snt27_top75pctrankingavg_36` | .43 | 68 | 前 75% 的排名均值 | 补充腿（`filter_sharpe=true` 会隐藏，须显式 `false`） |
| `snt27_rank` | .40 | 21 | 域名当日 Tranco 排名（1=最热） | 低 aC 另一代 |
| `snl27_avgranking` | .39 | 20 | 同 `snt27_avgranking_22`（另一代前缀） | 覆盖交叉验证 |
| `snl27_topranking` / `snl27_top50pctranking` / `snl27_top75pctranking` | .39 | 15 / 8 / 13 | 同上 | 低 aC，仅作稳健腿 |
| `snl27_top50pctrankingavg` / `snl27_top75pctrankingavg` | .39 | 6 / 7 | 同上 | 低 aC |

### B. 流行度复合分（已做排名归一，**值越大 = 越受关注**）

| 字段 | cov | aC | 语义 |
|---|---|---|---|
| `snt27_relpopularity1_30` | .43 | 111 | alpha=1 的相对流行度（越大越受关注） |
| `snt27_relpopularity08_26` | .43 | 74 | alpha=0.8 变体 |
| `snl27_relpopularity1` / `snl27_relpopularity08` | .39 | 3 / 0 | 同义另一代 |

⇒ **A 族（排名）与 B 族（流行度）互为倒数方向**，不要相加，只能二选一或做跨族稳健对照。

### C. 域广度 / 国际化（**天然的比率对**）

| 字段 | cov | aC | 语义 |
|---|---|---|---|
| `snt27_totaldomains_29` | .43 | 123 | 子域名总数 |
| `snt27_totalcountrydomains_34` | .43 | 78 | ccTLD 数量 |
| `snt27_dltcc_38` | .44 | 170 | 国别 TLD 代码（**分类标签，非数值**） |
| `snl27_totaldomains` / `snl27_totalcountrydomains` | .39 | 6 / 1 | 同义另一代 |
| `snt27_new_atlas_domain_37` | .44 | 74 | 清洗后域名（**字符串主键，禁作信号**） |
| `snt27_website_42` | .44 | 98 | 网站名（**字符串，禁作信号**） |

⇒ 可构造 `ccTLD / 总域名` = **国际化比率**，同源、单一经济含义、合规。

### D. 分布形态（覆盖稀薄，仅作候选）

| 字段 | cov | aC | 语义 |
|---|---|---|---|
| `snl27_skewness` | **.18** | 4 | 域名排名分布的偏度（不对称/集中） |
| `snl27_kurtosis` | **.18** | 2 | 超额峰度（尾部厚度） |

⚠ cov .18 ⇒ **远低于用户十年覆盖红线**，仅在全字段已画像时留档，不进主攻。

### E. 纯元数据（禁作信号）

`snt27_wq_pit_24` / `snl27_wq_pit`（PIT 对齐标记，description 明说 "not an analytical metric"）。

## 2. 名 vs description 差异表

| 字段 | 陷阱 |
|---|---|
| `sentiment27` 整个数据集 | 名字叫 sentiment，**内容是域名流量排名**，与情绪文本无关 ⇒ 按名字会错配「情绪反应不足」模板 |
| `snt27_avgranking`（两个同名字段） | 同一 id 在 `snt27_*` 与 `snl27_*` 两套前缀下重复出现，**覆盖不同（.43 vs .39）**，混用会把覆盖率打穿 |
| `snt27_dltcc_38` | "Country code TLD" 是**分类代码**，`vec_avg` 出来的数是「平均国别码」，**无语义** |
| `snt27_website_42` / `snt27_new_atlas_domain_37` | 字符串主键，聚合无意义 |
| `snt27_rank_39` vs `snt27_avgranking_22` | 「单个域名的排名」vs「全部域名排名的均值」，**不可互换**；前者需 `vec_avg` 才到主体层 |
| `skewness` / `kurtosis` cov **.1834** | 只有千分之十八的样本有形态统计 ⇒ 做信号必然 CW/覆盖双崩 |

## 3. 字段画像五问（A-1）

1. **时间维度**：日频存量水平（排名每日快照）⇒ 水平 + 变化率都可用。
2. **相对性**：**排序差异**（排名天然是序数）⇒ `rank` / `group_rank` / `ts_rank`，不要直接当连续数值（1…1e6 重尾）。
3. **被定价的是谁**：**散户注意力**（网站流量 = 真实浏览行为，比新闻覆盖更前置）。
4. **有无博弈**：有。`avgranking_22` aC 324 ⇒ 拥挤，prod 相关性风险高；且本区历史强信号常撞 prod 0.7+。
5. **事件性**：非事件型（连续日频），**不需要 `trade_when`**；但被排名的域集合会变（并购/改名）⇒ 需 `ts_rank` 自归一吸收。

## 4. A-2 收益来源声明

### 机制 A：**异常注意力 → 短期反转**（Da, Engelberg & Gao 2011, RFS *In Search of Attention*）
| 项 | 内容 |
|---|---|
| **谁在被定价** | 有限注意力的散户买方：先把注意力集中到最近最显眼的少数标的，买入压力推动价格短期上冲 |
| **为什么会被错** | 注意力是稀缺资源，不是信息 ⇒ 注意力**冲击**推动的买压没有基本面支撑，随后均值回归 |
| **错了多久修复** | 2–4 周（原文为周频搜索量）；本区用 `ts_rank(…,252)` 做自归一 + `ts_delta(…,22)` 取冲击 |
| **预期方向** | **注意力异常升高 ⇒ 后续收益偏低（做空）**；注意力异常流失 ⇒ 后续修复（做多） |
| **载体** | 排名数值下降 = 变热 ⇒ `ts_delta(rank)` 为负 = 注意力冲击。故 **`group_rank(ts_delta(rank))` 直接做多 = 做空注意力冲击**（符号需实测两向） |
| **失效条件** | 域集合变更（并购/更名）导致排名跳变；覆盖仅 43% ⇒ 早期年段 CW 风险；流量数据对大盘股（原本就高关注）无区分度 |

### 机制 B：**数字足迹 → 基本面领先**（下一波，不进本轮）
域广度（`totaldomains`）/国际化（`ccTLD 占比`）代表业务扩张 ⇒ 领先营收。**本区无营收验证字段做交叉检验，暂缓**；如启用须先做「与 fundamental 塔已亮 alpha 的相关性」检查。

## 5. 双通道取证

**通道 A（论坛，2026-10-30 实检 3 条）**：

| 证据 | 出处 | 读到的可执行结论 |
|---|---|---|
| ★★ **`snt27_rank_39` 实盘提交证据** | 「我的量化日记第十一季」WL13229（42 赞）：`"8.0‱，selfCorrelation 0.068，prodCorrelation 0.584。使用了 snt27_rank_39 字段,用了基于情绪排名的标准化动量方法"`，且该条为 **KOR/D1/SENTIMENT** | ⭐ **本集在 KOR/D1 确有已提交 alpha**，且有 0.116 的 prod 余量。方法 = **对排名字段做标准化动量** ⇒ `ts_zscore` / `ts_delta` 路径有实盘背书。⚠ 反过来说：同族已进 prod 池，新候选 prod 起点可能贴近 0.58，须第一批就查 |
| ★ **KOR 分组粒度铁律** | 「KOR D1 高集中度破局」WA25180（2026-09-23，1 赞，AI 辅助帖，**无指标**）：三星+海力士合计 >50% KOSPI ⇒ `industry` 级 `group_rank` 退化成 0/1 二值 ⇒ 假高 Sharpe + sub-universe 倒挂 | ⭐ **`group_rank` 必须用 `sector` 或 `market`，禁 `industry`**（与本波设计一致）。同时给出 `vec_avg` 时序平滑 + 熔断次日延迟确认的清洗建议 |
| ★ **sentiment27 的角色 = 散户 FOMO 泡沫轨（反向）** | 同上帖：`"流量热度从极高分位回落的标的，散户抛压出清、筹码结构改善"` | 方向句：**从极端高分位回落 ⇒ 做多**。即 `ts_delta(ts_rank(P,252)) < 0` 为多头信号 ⇒ 本波 `ts_delta` 腿须两向都测（铁律 B） |
| 补充：`signed_power(…, 1.25)`（区间 1.2–1.5）作非线性权重 | 同上帖 | 备用参数档；本波先用 0.5（压尾）与无幂次两档，不同时换两个轴 |
| 补充：**不要用 truncation / 幂次来压 prod** | 同上帖踩坑 3：`"试图通过调 truncation 或改幂次来压 Prod Corr，只是过拟合泥潭"` | 与本区已死轴清单一致（truncation 扫描禁入） |

⚠ 该帖自称"成功点亮该 3 个区域的金字塔"用 RISK+SENTIMENT+SHORTINTEREST 三数据集，但**表达式是示意（`domain_attention_rank` 非真实字段名）、无任何指标**，且 shortinterest3 / risk59 在 KOR 均已判死 ⇒ **只采信其中的单数据集机制句与分组粒度结论，不采信其组合配方**。

**通道 B（论文）**：
- Da, Engelberg & Gao (2011, RFS)：Google 搜索量上升 ⇒ 未来 2 周收益偏低（散户注意力的直接代理）。**本数据集是 Tranco 网站排名的企业级映射，属同族构造**，方向句可移植。
- Barber & Odean (2008, RFS)：散户在注意力集合内选股 ⇒ 注意力冲击 = 买压。
- ⚠ Da-Engelberg-Gao 样本为 Russell 3000（USA 大盘），KOR TOP600 小宇宙外推**必须先当假说**。

**双通道裁决**：A、B 指向同一机制（注意力冲击 → 反转）⇒ 按 SOP 「⭐ 优先组装」。
唯一冲突：B 说「冲击上升 ⇒ 做空」，A 说「从极高分位回落 ⇒ 做多」——二者**并不矛盾**（同一枚硬币：极端注意力均值回归），
但意味着 **`ts_delta` 腿的方向必须实测两向**，不能按任一篇的措辞直接定符号。

**本区实证锚（lit KOR alphas，非本数据集）**：
- 5 个 S 1.76–2.57 的已提交 KOR alpha 共用几何：**「同源比率/净额 → 组内 rank → 462–1260 日自归一 ts_rank → 慢速平滑」**。
  `snt27_avgranking_22 / snt27_topranking_23` 正好提供同源比率 ⇒ **本集首选几何照此构造**。
- 该几何与 A 通道的 `group_rank(vec_avg(…), sector)` 形式**完全同构**，两者互相印证。

## 6. 十年覆盖验证（★ 本集唯一硬风险）

**cov .43 是全样本均值，按年级分布未知**。域名流量库在 KOR 小盘股上很可能 2014–2016 年近乎空。
⇒ **铁律：先发 1 批 2 条探针（1 正向 + 1 反向），第一件事读 `get_alpha_yearly_stats`**：
每年 `longCount` 或 PnL 是否为 0；若 **首 3 年中有任一年完全空 ⇒ 判不满足用户约束 4，不再投主攻槽**。

## 7. 波次设计（wave 189 已入 staged，1.6× 塔）

> wave 188（news7）归因判死事件计数机制后，189 席位改投本集。原 news18 8 条已 `dropped`（终态，原因入 `settings_json.status_change`）。

| 位置 | 机制腿 | 表达式（`group_rank` 一律 `sector`，除标注 `market`） | 目的 |
|---|---|---|---|
| 1 | A 同源比率 = **注意力集中度** `R = top/avg` | `group_rank(ts_rank(divide(vec_avg(snt27_topranking_23), vec_avg(snt27_avgranking_22)), 504), sector)` | 旗舰域名 vs 组合均值：越接近 1 = 越均匀。本区首选赢家几何 |
| 2 | 同上 **反向** | `multiply(-1, …)` | 铁律 B：`reverse()` 非精确反号，必须显式各测 |
| 3 | 同上 **赢家几何全形** | `signed_power(ts_rank(group_rank(R, sector), 504), 0.5)` | 组内 rank → 504 日自归一 → 压尾 |
| 4 | **标准化动量**（A 通道实盘配方） | `group_rank(ts_zscore(vec_avg(snt27_rank_39), 66), sector)` | 复刻 WL13229 已提交的 `snt27_rank_39` 标准化动量（prod 0.584，self 0.068） |
| 5 | B **流行度水平** | `group_rank(ts_rank(vec_avg(snt27_relpopularity1_30), 504), sector)` | 做多高关注（动量解释） |
| 6 | B **同式反向** | `multiply(-1, …)` | DEG 泡沫轨 / 冷门股溢价 |
| 7 | B 反向 + hump + `market` 轴 | `hump(group_rank(multiply(-1, ts_rank(vec_avg(snt27_relpopularity1_30), 504)), market), hump=0.003)` | 同 6 + 换分组轴 + 降换手（CW/TO 双修） |
| 8 | B **注意力变化率** | `group_rank(ts_delta(ts_rank(vec_avg(snt27_relpopularity1_30), 252), 22), sector)` | A 通道「从极高分位回落 ⇒ 做多」的两向之一 |

**设计纪律**：① 8 条全为 `sentiment27` 单集 ATOM；② `industry` 显式排除（A 通道铁律）；③ 不换 `truncation`/幂次以外的设置轴；
④ 每批 2 条串行（`--set _multi_sim_batch_size=2 --serial`），批 1 落地后**第一件事读 `get_alpha_yearly_stats` 验十年覆盖**，再看 Sharpe。

| 后续波 | 目的 | 候选（≤3） |
|---|---|---|
| 次波（≤3） | 域广度 / 国际化（机制 B，滞后） | `divide(vec_avg(snt27_totalcountrydomains_34), vec_avg(snt27_totaldomains_29))` |
| 三波（≤1） | 分布形态（cov .18） | `snl27_skewness` —— **仅当探针证明覆盖够** |

## 7.1 wave 189 实测：覆盖判死（2026-10-30，批 1 落地即止）

**结论先行：本集不满足用户约束 4（近十年有数据），塔不可点亮；剩 6 条未发，直接停波。**

### 批 1 读数（2 条，`_multi_sim_batch_size=2` 串行，multisim `kQCU3bRL4sa9wZQd70eSmz`）

| # | alpha | 表达式 | S | F | 2Y | TO | subU | margin |
|---|---|---|---|---|---|---|---|---|
| 1 | `vR1aGG1v` | `group_rank(ts_rank(divide(vec_avg(snt27_topranking_23), vec_avg(snt27_avgranking_22)), 504), sector)` | **−0.22** | −0.06 | −0.29 | .1446 | −0.04 | −1.36bp |
| 2 | `xArXGGrb` | 同式 `multiply(-1, …)` | **0.06** | 0.01 | −0.15 | .1445 | −0.08 | +0.4bp |

⇒ 正反两条都在 0 附近、且 2Y 比 IS 更差 ⇒ **不是方向问题，是没有信号**。

### 逐年（`get_alpha_yearly_stats`，KOR IS 窗口 2014–2023）

| 年 | 2014 | 2015 | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 |
|---|---|---|---|---|---|---|---|---|---|---|
| longCount | 0 | 0 | 0 | 0 | 0 | 270 | 313 | 336 | 326 | 315 |
| S | 0 | 0 | 0 | 0 | 0 | −0.42 | **+1.54** | **−1.85** | +0.50 | −0.85 |

**两条独立致命伤**：
1. **2014–2018 连续五年全空**（`longCount=0` / `pnl=0`）⇒ 本集实际数据起点 = **2019**，有效历史 **5 年**，不满足用户约束 4。
2. 即便只看 2019–2023，逐年 S 也在 **+1.54 / −1.85** 之间来回翻号 ⇒ 无 regime 无关的机制，2Y 闸结构性不可达（KOR 决策表：近年断崖 + 反复翻号 ⇒ 换机制族，不扫参数）。

### 处置

- **停止本波剩余 3 批 6 条**（已 kill 流水线；`ckpt_w189` 只留批 1）。
- **sentiment27 塔在用户约束 4 下判结构性不可点亮**：不是信号问题，是历史长度问题；除非约束 4 放宽到 5 年，否则**不再投任何配额**。
  ⚠ 已知 `WL13229` 用 `snt27_rank_39` 提交过（prod .584）—— 那是别的账号在**不同 10Y 口径**下的产物，不影响本区判定；但也说明「字段本身能出信号」与「本区能提交」是两件事。
- **本集与 sentiment 类其它数据集（news7 语气族、news46 情绪族）同属「2019 年后才有数据」风险带** ⇒ 后续 sentiment/news 数据集**在画像阶段就要先问数据起点**，别再靠首批发完才发现。

⚠ **流程教训（值得复用）**：画像 §6 那条「首批 2 条落地先读 yearly_stats」本次**直接省下 6 个仿真槽**。凡覆盖率是硬风险的集合（域名词频、社媒、新上线 vendor 源），一律照此执行。

## 8. 禁区

- `snt27_dltcc_38` / `snt27_website_42` / `snt27_new_atlas_domain_37` **禁作信号**（分类码 / 字符串）。
- `snl27_skewness` / `snl27_kurtosis` cov .18 ⇒ 不进主攻。
- 排名类字段**禁裸当连续值**（1…1e6 重尾），必须 `rank`/`ts_rank`/`group_rank` 之一。
- `snt27_*` 与 `snl27_*` 两代前缀**禁混用**（覆盖 .43 vs .39，混用打穿覆盖率）。
- 不与 PV/MODEL/OTHER 组腿（用户约束 5 的 5 条额度留给更高价值组合）。
