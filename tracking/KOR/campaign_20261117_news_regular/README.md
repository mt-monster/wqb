# KOR × News 冷门集 × Regular Alpha（2026-11-17 起）

> **目标（用户 2026-11-17 指令）**：KOR 区固定，挖 **20 个 regular alpha**（优先 ATOM），prod<0.7 严格；
> 守 11-16 明令「**只打未亮塔**」；用户当日选择「照旧只打未亮塔，能交多少交多少」。
> **塔位现状（get_pyramid_alphas 实读 2026-11-17）**：insiders **3/3 满**、analyst 4、fundamental 3、model 3、
> risk 3、shortinterest 4、pv 2、other 2 全已亮；可用 = **news / earnings / institutions / sentiment /
> macro / imbalance / socialmedia（0）**。
> **流程**：`docs/reference/kor_regular_alpha_mining_sop.md`（7 章，2026-11-17 落盘）。
> **工具**：全程 MCP（`wq-brain-http` / `wqb-db`）；scholar-mcp 本会话不可用，论文通道用 `mcp__minimax__web_search`。

## 0. 为什么挖 News（唯一未穷尽的未亮塔）

- KOR earnings 平台全表 = **仅 1 集** `earnings3`（8 字段，aC 2639，天花板 S 0.94，前序波 186 判死）。
- KOR news 平台全表 = **24 集**，其中 `news23`/`news29`/`news73`/`other7` 是 aC 极低（8–60）的冷门集，
  **从未在本战役里探过** —— 昨天扫的是 news7/18/20/31/46/50/85 等热门集（5 轴判死）。冷门 = prod 白空间的必要条件。

## 1. 全字段探测（brain-datafield-exploration-general §0 / brain-dataset-exploration-general §1 全量静态画像模式）

统一：`get_datafields(dataset_id=<ds>, region=KOR, universe=TOP600, delay=1, filter_sharpe=false, max_fields=不传)`；
三重对账 `count == platform_count == complete=true`。
归档路径：`tracking/KOR/reference/datasets/<dataset_id>.md`（每集一份，手工维护；命名规则见 SOP §2 / DELIVERY §画像索引）。

### 1.1 news23 — M&A Deals Data（93/93 字段，全 VECTOR，count=platform_count=93, complete=true）

| 族 | 代表字段 / 覆盖 / aC | 解读 |
|---|---|---|
| **报价溢价（核心）** | `offer_premium_one_day_prior` 0.149/aC1 · `one_week_prior` 0.149/aC0 · `four_weeks_prior` 0.149/aC3 | 事件型稀疏（cov<0.4）⇒ 必须 `ts_backfill` + `trade_when` 门控，禁裸 rank |
| **目标方估值/盈利** | `nws23_target_niltm` 0.313/aC9 · `mtlspe` 0.313/aC2 · `pricebook` 0.207/aC1 | 高于报价溢价的覆盖，作第二腿 |
| **收购方** | `nws23_acquiror_apr1daya` 0.212/aC0 · `spea` 0.256/aC1 · `value` 0.256/aC1 | "announcement 前后股价"是事件结果字段，D1 可用性存疑（未来函数风险） |
| **私有市场/VC** | `investment_detail_disclosed_valuation` 0.795/aC2 · `fund_total_size_2` 0.677/aC0 | 非上市公司估值 → 与本轮上市公司 alpha 无关 |
| **其它** | 大量 industry/stage/job_title 编码字段 cov 0.02–0.64，aC 0–1 | 编码字段只作分组轴，禁算术（SOP 附录 A 行3） |

**结论**：入选项 = 报价溢价族 + 目标方盈利/估值族；两者都 aC≤9（冷门）。

### 1.2 news29 — Significant Developments Data（12/12 字段，全 VECTOR）

| 族 | 代表字段 / 覆盖 / aC | 解读 |
|---|---|---|
| 头条标记 | `nws29_frontpage` 0.246/aC3 · `nws29_full_frontpage` 0.865/aC1 | 二值稀疏 ⇒ trade_when 门控 |
| 重要性 | `nws29_significance` 0.246/aC5 · `nws29_full_significance` 0.865/aC4 | 1=High/2=Med/3=Low，须反向（数字小=重要） |
| 主题码 | `nws29_topic1` 0.246/aC11 · `event_secondary_topic_code` 0.865/aC1 | 编码字段，只作分组/门控 |

**结论**：入选项 = significance（重要性）+ frontpage（头条）的组合；aC≤11 冷门。

## 2. 机制与论文锚点（铁律 H 双通道，2026-11-17）

- **通道 B（成功，MCP `mcp__minimax__web_search`）**：
  ① Ho/Brownen-Trinh/Xu (2020, SSRN 3742824, JBFA forthcoming)：目标价高的公司更可能成为收购标的、
  收购方公告收益与目标价溢价正相关；基于目标价的 long-short 有显著收益。
  ② EU M&A event study（2010–2019, 2190 公告）：目标方公告收益显著正、**收购方几乎完全不显著**、
  offer premium 与目标方异常收益呈**二次关系**（过度支付假说）。
  ⇒ 可证伪方向句：**高溢价收购 ⇒ 收购方过度支付 ⇒ 后续 1–4 季弱**（对目标方则是相反）。
  适用域：EU/USA 样本 ⇒ KOR 小宇宙仅当**假说**，须本区实测；两篇都点明"acquirer 公告收益不显著"，
  所以**信号应落在公告后的漂移**，不是公告本身。
- **通道 A（论坛）**：`search_forum_posts("merger acquisition announcement premium alpha KOR")` 30s 超时（工具故障 ≠ 论坛无解，
  取证纪律：不落 `forum_recon_negative_*`）。已记录，不阻塞组装（论文机制已够）。

## 3. 波次台账（追加、不覆盖）

（待开波后逐波写：每波三问 / 表达式 / 读数 / 归因 / 淘汰原因）

## 3. 波次台账（追加、不覆盖）

### W1 · news23 目标方基本面 × 报价溢价（批次 `1TvYNVd2V5h2aIL19V1nj8V4`，SLOW/d2，10 条）

**三问**：继承=论文「acquirer 公告收益不显著 + 溢价二次关系」+ 头部字段 aC12 指向目标方规模；
准入=只用 news23 的目标方估值/盈利 + 报价溢价族，禁收购方公告后股价字段（未来函数）、禁私有市场族；
收窄=10 条首波基线。

| # | 机制 | 表达式骨架 |
|---|---|---|
| 1 | 目标方净利润（低=好?） | `subtract(0.5, group_rank(ts_mean(vec_avg(nws23_target_niltm),252),sector))` |
| 2 | 目标方销售规模 | `group_rank(ts_mean(vec_avg(nws23_target_asalesltm),252),sector)` |
| 3 | 4 周溢价（高=差） | `subtract(0.5, group_rank(ts_mean(vec_avg(offer_premium_four_weeks_prior),252),sector))` |
| 4 | 1 日溢价（高=差） | `subtract(0.5, group_rank(ts_mean(vec_avg(offer_premium_one_day_prior),252),sector))` |
| 5–7 | 目标方盈利/销售/对价 − 4周溢价 | `subtract(group_rank(...), group_rank(...))` |
| 8 | 报价/账价比 | `group_rank(ts_mean(vec_avg(nws23_target_pricebook),252),sector)` |
| 9 | 1 周溢价（高=差） | `subtract(0.5, group_rank(ts_mean(vec_avg(offer_premium_one_week_prior),252),sector))` |
| 10 | 目标方 EPS | `subtract(0.5, group_rank(ts_mean(vec_avg(nws23_target_mtlspe),252),sector))` |

**状态**：派发 2026-11-17，队列拥塞中（batch_status child_count=0，20+ 分钟），未收批、未判定。

### W2 · news29 事件重要性 × 头条（批次 `1NMflJcCp4zx9SJ1a8ezTAxn`，SLOW/d2，10 条）

**三问**：继承=头部字段 aC11 指向事件类型/重要性，非纯情绪；
准入=只用 significance/frontpage/topic，禁文本字段；
收窄=10 条首波基线。

| # | 机制 |
|---|---|
| 1–2 | 重要性反向（1=High ⇒ 数值小=重要）：`subtract(1.5, group_rank(ts_mean(vec_avg(nws29_full_significance|nws29_significance),252),sector))` |
| 3–4 | 头条标记正向 |
| 5–6 | 头条 − 重要性（双向） |
| 7–8 | 重要性 126/504 日窗口 |
| 9 | 主题码 `nws29_topic1` |
| 10 | industry 分组轴对照 |

**状态**：派发 2026-11-17，队列拥塞中，未收批、未判定。

### 读数（2026-11-17 收批，批次 `1TvYNVd2` / `1NMflJcC`，各 10/10 COMPLETE、0 error）

**W1 news23 — 20/20 无信号（REJECT）**：S 全部落在 **−0.40…0.35**，最好 `e7aLJaAd` S 0.35 / 2Y 1.01 / fRA 3，
`Xga1EVGl` S 0.47 / 2Y 0.98 / fRA 3。目标方净利润/销售规模/报价溢价/价差全部 |S|<0.5。
⇒ **信号层死**（不是 prod 墙，RA 直接 3–5 项不过）。论文锚（M&A 溢价二次关系）在 KOR 小宇宙不成立。

**W2 news29 — 10/10 无信号（REJECT）**：S 全部落在 **−0.43…0.02**，重要性反向/头条标记/主题码/窗口全灭。
⇒ **信号层死**。

**归并判断**：news23（M&A）+ news29（重要事件）两个冷门集**不产出**。与 SOP 附录 C「news 塔 5 轴全死」一致，
但这两集是首次实测（此前只测过 news7/18/20/31/46/50/85 热门集），故为**新增实证**，不是重复。

**剩余未测**：`other7`（Benzinga 新闻微观结构 prob_pos/neg × novelty，11/11 全字段已探测 + 预检通过）、
`news73`（story-level 情绪，coverage 0.2676，待全字段探测）。

### W3 · other7 新闻微观结构（批次 `1SGVimgGm5hx9pZiLyKtmh3`，SLOW/d2，10 条）

**三问**：继承=头部字段 aC10 `headlineonly`（新闻呈现形式）而非情绪方向；
准入=prob_pos/neg 价差 + novelty + confidence 加权 + headlineonly + relevance，禁 `marketimpactscore`（未来 1 分钟收益，D1 未来函数）；
收窄=10 条首波基线。

**读数（2026-11-17 收批）**：10/10 REJECT。S 全落在 **−0.37…0.09**，
alpha id `kqaQpwMK/d5adJM6v/88NnW0xo/Jj8baAJm/j2a1kpKj/d5adJMrv/E5Qknjn1/Wjl9rZrG/Grmkj2jx/O0WodLLv`，
failed_ra 4–5。**信号层死**。

### 归并结论：news 冷门面已穷尽（2026-11-17）

四个集（news23 M&A / news29 重要事件 / other7 新闻微观结构 / news73 story 情绪）全部在信号层失败：
前三集已实测 REJECT，news73 因**与已判死情绪集 news85/84/3/79 同机制** PROVISIONAL 停投（见
`tracking/KOR/reference/datasets/news73.md`）。news 塔（0/3）本轮**0 交付**。按 AGENTS §7.6 六维口径，
这是「已测形态信号层死」，不是数据集层终判死；翻案须新机制（如 news73 的逐实体情绪分歧度）。

## 4. 转向：按文章 `dateCreated` 法找蓝海字段（2026-11-17）

外部文章《为什么你现在应该多做 ATOM》的核心教训：**老数据集里 alphaCount==0 的字段多半是被犁过的死字段**；
真白空间是**近期 onboard + 高覆盖**的字段。此前我按 aC 升序选冷门集（news23/news29/other7）正是踩了这个坑。
文章经验已沉淀 `docs/reference/atom_mining_playbook_20261117.md` + `docs/experience/06_atom_mining.md`；
`get_datafields` 已支持 `sort_by=dateCreated` / `min_coverage`（本会话由并行会话补齐并重启 MCP 生效）。

**扫描结果**：KOR 未亮塔中，`fund_holdings_panel`（**institutions 塔 0/3 未亮**）
全 30 字段 `dateCreated=2026-03-01`、coverage 0.66–0.96、aC 0–35、倍率 1.4 —— 典型蓝海签名。
对照 `institutions6`（2025-10-01 onboard，aC 59–259）已偏拥挤；`fund_holdings_panel` 是更正的选集。
`imbalance5` / socialmedia（倍率 1.0）、sentiment 全集（情绪族已死）不投。

### W4 · fund_holdings_panel 单字段 ATOM × 文章四模板（批次 `2vE76b28m50scGmHFkMIbsV`，SLOW/d2，10 条）

**三问**：继承=文章四套单字段模板（长短均值比 / zscore+组内中性 / 一年分位反转 / 差分÷自身波动）；
准入=全部字段 dateCreated 2026-03-01 + coverage≥0.66，VECTOR 先 `vec_sum`/`vec_avg` 聚合（禁裸算术），
只挑 aC≤35 的冷门高覆盖字段，禁 `*_active` 低覆盖版（0.66 < 非 active 0.89–0.96）；
收窄=10 条单字段臂，一族一席。

| # | 模板 | 字段（aC） |
|---|---|---|
| 1 | 长短均值比 | `herfindahl_index_holdings`(34) |
| 2 | zscore+组内中性 | `mean_security_weight`(13) |
| 3 | 一年分位反转 | `holder_account_total`(30) |
| 4 | 差分÷波动 | `holding_value_distribution_score`(19) |
| 5 | 长短均值比 | `top_weighted_account_number`(16) |
| 6 | 差分÷波动 | `boundary_transaction_total`(35, VEC) |
| 7 | 一年分位反转 | `stable_boundary_trade_count_21d`(13, VEC) |
| 8 | 长短均值比 | `boundary_transaction_usd_value`(6, VEC) |
| 9 | zscore+组内中性 | `herfindahl_index_transactions`(2, VEC) |
| 10 | 差分÷波动 | `transaction_value_distribution_score`(4, VEC) |

**读数（2026-11-17 收批，批次 `2vE76b28`，10/10 COMPLETE、0 error）**：**10/10 REJECT**。

| # | 字段 | S | 2Y | TO | fRA | Alpha id |
|---|---|---:|---:|---:|---:|---|
| 1 | herfindahl_index_holdings | −0.01 | 0.47 | 0.094 | 5 | `qM7gRJK1` |
| 2 | mean_security_weight | −0.39 | −0.48 | 0.247 | 3 | `QP0E8p1Q` |
| 3 | holder_account_total | −0.51 | −0.14 | 0.085 | 5 | `Wjl952EO` |
| 4 | holding_value_distribution_score | −0.19 | 0.17 | 0.241 | 5 | `kqaQA6x6` |
| 5 | top_weighted_account_number | −0.13 | 0.01 | 0.131 | 4 | `2r5JYor8` |
| 6 | boundary_transaction_total (VEC) | 0.22 | 0.55 | 1.196 | 7 | `omaVd0m2` |
| 7 | stable_boundary_trade_count_21d (VEC) | −0.32 | 0.69 | 0.959 | 5 | `LLKkQYL6` |
| 8 | boundary_transaction_usd_value (VEC) | −0.30 | −0.01 | 0.222 | 5 | `QP0E8pPQ` |
| 9 | herfindahl_index_transactions (VEC) | −0.69 | −0.60 | 1.131 | 6 | `xAvRZpAb` |
| 10 | transaction_value_distribution_score (VEC) | −0.20 | 0.68 | 1.181 | 6 | `3q0zNvqP` |

**归因（先归因再推进，禁止盲扫）**：
- 5 条 MATRIX 持仓/集中度水平族：S −0.51…−0.01，TO 0.08–0.25。覆盖率 0.95 ⇒ 非覆盖闸，`ts_backfill` 救不了；
  **是信号本身不存在**，不是配置层死。
- 5 条 VECTOR 逐日交易事件族：TO 0.96–1.20 直接爆换手闸（逐日事件计数翻转）；
  2Y 尚可的两条（`LLKkQYL6` 0.69 / `3q0zNvqP` 0.68）全期 S 为负 ⇒ **符号跨期不稳定**，非稳定 edge。
  唯一做过平滑的 `QP0E8pPQ`（20/120 均值比，TO 0.22 已达标）S −0.30，即使反号也距 1.58 闸线 1.28。
- **判决**：`fund_holdings_panel` 在 KOR 的文章四模板下**信号层死**，不追加配额、不换窗口硬凑。
  这是文章方法的**负面校准**：`dateCreated` 法成功找到蓝海字段（真新、真低 aC、真高覆盖），
  但「新字段 ⇒ 简单模板即可过检」在 KOR institutions 塔**未复现**。

> ⛔ **事后发现的关键失误（2026-11-17）**：W4 开波前**未核死表**。这两个 institutions 集早在 2026-10-30
> 就已整体判死：`fund_holdings_panel` = `KOR-FUND-HOLDINGS-PANEL-DEAD`（wave124/187/200 三轮 6 形态全灭，
> 明令"不得再开波"），`institutions6` = `institutions6_dead`（wave205 两条腿 S 0.57–0.60 距闸 2.6×，
> 逐年 S<1.0 占 8/10）。W4 只是第 7/第 N 次重复确认。根因与 roadmap §wave205 记载的 wave187/200/205 三次误发**完全相同**
>（链路开波前不查 `get_dead_datasets`）。
>
> **用户随后要求"查论坛+论文匹配机制再回测"**：已执行检索，但论文机制（S&P Smart Money 的 breadth stability + turnover；
> Choi/Jin/Yan 2013 机构 breadth 增加→收益；Choi&Sias 2009 herding 反转）**全部落在两个死集已测几何内**
>（`fund_holdings_panel.md` §3.2 早在 10-30 就记录过同类论文/论坛帖），属跨区不迁移。
> 因此**不开 W5**——在判死数据集上按论文再组臂仍是重复确认，违反 AGENTS.md 判死纪律。
> 完整论文清单与裁决见两份档案 `fund_holdings_panel.md` §7 / `institutions6.md` §5。
>
> **流程教训（写入长期纪律）**：开波前**第一动作** = `get_dead_datasets(KOR)` + grep 字段画像档案的 `DEAD` 标记；
> 命中即停。`dateCreated`/论文机制只用于**活集内部**挑字段和机制，绝不用于复活死集。

## 5. 本战役最终交付（2026-11-17）

**0 颗**。五个未亮塔面全部实测或结构性排除：
- news（0/3）：news23 / news29 / other7 实测 REJECT；news73 与已判死情绪集同族 PROVISIONAL 停投。
- institutions（0/3）：fund_holdings_panel 实测 REJECT（本波）；institutions6 onboard 2025-10、aC 59–259 已偏拥挤且跨区实测衰减（1.62→0.49），非蓝海。
- earnings（0/3）：全表仅 earnings3，天花板 S 0.94，前序 186 波判死。
- sentiment（0/3）：情绪族整体 KOR 判死（SOP 附录 C）。
- macro（0/3）：macro63 仅 1 字段（指数调整）；macro27 42 臂 GBR 判死，无 KOR 迁移依据。
- imbalance（0/3）：imbalance5 仅 2 字段、倍率 1.0（木桶律下无收益），Xga1Ae00（imbalance×PV）已判死。
- socialmedia（0/3）：2 集各 1 字段、倍率 1.0，无 ATOM 空间。

在「11-16 用户明令只打未亮塔」约束下，无合格候选可交付。按用户「能交多少交多少」口径如实报 **0**，
不挪用已亮塔的 prod-clean 存量（insiders 3/3、pv 2、other 2 等）充数。若用户后续放开未亮塔限制，
可立即从本地 prod-clean 池交付（须当日 `check_correlation(refresh=True)` 复核，见
`tracking/KOR/campaign_20261115_unlit_towers/DELIVERY_20261116.md`）。

## 6. 全未亮塔论文驱动复审（2026-11-17，用户指令「其它未点亮塔下的数据集都要这个思路测，开启流水线」）

> ⚠ **W4 教训是本节的前提**：任何开波前**第一动作** = 查权威死表 + grep 字段画像档案的 DEAD 标记；
> `dateCreated`/论文机制只用于**活集内部**挑字段，绝不用于复活已充分判死的集。为此开启流水线
> `dwfrun-034fe797-c87e-4c38-be99-911c06919251`，12 个未亮塔数据集逐个按 §7.6 六维闸**先复审判死是否充分**，
> 只有六维未穷尽且论文机制字段支持的集才进入组臂/回测。

### 6.1 权威死表（ledger `*_dead` + registry dead_end 85 条，只读实查 2026-11-17）

KOR 正式封存 16 集：`acquisition_model / fundamental44 / institutions6 / model109 / model170 / model192 /
model230 / model30 / model32 / model53 / multi_source_model / news79 / sentiment21 / shortinterest3 / smoke_ds /
wave30_model252`。这些**整集关闭，不复投**（institutions6/news79/sentiment21 直接跳过）。

### 6.2 全字段画像（本轮新拉，`sort_by=dateCreated`，无抽样）

| 集 | 塔 | 字段 | dateCreated | aC | cov | 机制支持 |
|---|---|---|---|---|---|---|
| `earnings3` | earnings 1.1 | 8 全 MATRIX | 2023-01 | 199–627 | .56–.78 | **只有日期/时刻字段**（距财报天数 next/pre_interval、reptime）⇒ PEAD 论文需 earnings surprise，**字段不支持** |
| `imbalance5` | imbalance 1.0 | 2 MATRIX | 2023-11 | 318/1182 | .856 | 仅 `imb5_score`(SHIELD-OIL 复合) + mktcap ⇒ oil-beta 论文需 firm exposure，**字段不支持** |
| `news21` | news 1.6 | 13 | 2022-12/2025-11 | ≤116 | .33–.97 | 12 个日期/标签/flag + 1 个 `nws21_event_freq`（计数轴已判死）⇒ 无可投字段 |
| `other553` | sentiment 1.6 | 21 全 VECTOR | 2023-11 | 0–40 | .48–.75 | 卖方 PT/评级/预期**修正**域（`value`/`prevalue` 成对）⇒ 与已死新闻情绪**不同机制**；唯一有真正可辩护新机制的集 |
| `sentiment26` | sentiment 1.6 | 19 | — | 低 | .356 | 被动 DNS 注意力，wave216 已判死（7/10 年 + 无截面） |
| `macro63` | macro 1.4 | 1 MATRIX | — | 158 | 1.0 | 0/1 哑变量，10 年 longCount 全 0，结构性无截面 |
| `socialmedia39`/`other100` | socialmedia 1.0 | 各 1 VECTOR | — | 357/484 | 1.0 | 只有"邻居票 ID 列表"，零信号面 |

### 6.3 论文取证（本会话 minimax web_search，供复审子代理/后续机制设计复用）

| 方向 | 论文/来源 | 可证伪结论 | 字段落地性 |
|---|---|---|---|
| **PEAD / 财报时点** | Competitive earnings news and PEAD (Bereskin et al., ScienceDirect)；Goh/Jeon 2017 *PEAD & 52-week high: Evidence from Korea*；PEAD 综述 (Fink 2021) | 行业内同业财报公告存在信息转移；**KOR 市场有 PEAD 实证**；公告时点/顺序影响漂移 | earnings3 只有日期字段，**无 surprise** ⇒ 只能做「距公告日 × 组内」时点结构，非经典 PEAD |
| **分析师修正广度** | AlgoGP《Analyst Estimates and Earnings Revisions》：**revision breadth = (上调数−下调数)/分析师数** 是有用汇总信号；评级/PT 水平信息量低 | 修正**方向与广度**驱动后续收益；PT 修正多跟随股价(AnaChart 2026, 83.9% 同向) ⇒ **须用 PT-revision 相对股价的残差** | other553 有 `ptgvalue/preptgvalue`、`est_estvalue/preestvalue`、`*_analyst` ⇒ 唯一字段支持的方向 |
| **机构持仓/广度**（institutions 已判死，仅存档） | S&P《An IQ Test For The Smart Money》：Ownership Dynamics 最强；Choi/Jin/Yan 2013 机构 breadth↑→收益↑ | 见 `fund_holdings_panel.md` §7 / `institutions6.md` §5，跨区不迁移，已判死不复投 | — |
| **油价冲击截面** | Geopolitical Oil Shocks & Sectoral Heterogeneity (SSRN 6630555)；Kwong 2026 *Energy exposure & resilience* | 高 oil-beta 板块异常收益更大；效应随时间累积 | imbalance5 只有 composite score 无 firm exposure ⇒ 字段不支持 |

### 6.4 论坛取证

`search_forum_posts("institutional holdings alpha")` → 0 命中、`navigation_failed=false`（legit no_result）。
旧帖 433587556696703 / 43212475386007 见 `fund_holdings_panel.md` §3.2，已验无效。

### 6.5 状态：流水线运行中

复审结果返回后，按 `AttackPlan` 决定：若六维未穷尽且字段支持的集（当前最可能是 `other553` 的
PT/预期修正残差方向）→ 填 tail hole 组臂回测；若判死充分 → 不开波、如实报 0 并归档。

### 6.6 流水线终局（2026-11-17，`dwfrun-034fe797`）

12 集六维复审 → **11/12 判「六维未穷尽」**(PROVISIONAL)。按 §7.6，未穷尽只够 PROVISIONAL，
不等于必须开波——流水线加两道收敛闸：①裁定员按三条件(字段真支持/几何真新/非跨区)收敛；
②独立复核员(fresh-eyes)专查是否复活死集。终局：
- **可攻 2 集**：`other553`(分析师预测分歧度，Diether/Malloy/Scherbina 2002，二阶矩与 wave192 一阶矩正交)、
  `sentiment26`(注意力分布二阶矩 kurtosis/skewness，弱保留、十年覆盖存疑)。
- **封存 9 集**：earnings3(无 earnings surprise)、imbalance5(无 firm oil beta + 塔倍率1.0)、
  news23/news29/other7(W1–W3 已 30/30 REJECT)、news21(无可投字段)、macro63(恒零无截面)、
  socialmedia39/other100(join-key ID 零信号面)。
- **待用户决策 1 集**：`sentiment23`(156 字段含分歧度族字段支持，但 cov 0.25 稀疏 + 与 other553 机制重复)。

⚠ **开波前第二道拦截(幽灵算子)**：裁定员骨架用了 `vec_std_dev`(KOR 不存在)，
preflight 报 unknown_fields；改用真实算子 `vec_stddev` 后 8/8 臂通过。这是 W4 教训后的第二道防线：
死表检查 + 幽灵算子检查都在烧配额前完成。

**组臂(2026-11-17，并发 2，STATISTICAL/d2)**：
- 批A `uoB8H6JU52z90t1dFdB040S` — other553 分歧度 5 条(`vec_stddev/est_estvalue` 横截面分歧、
  `est_analyst` 家数门控、ptg/est 修正 spread、sal 分歧中性化)。
- 批B `WzDuS1bZ4via7x1hzukgcJw` — sentiment26 注意力二阶矩 3 条(kurtosis/skewness/relpopularity IR)，
  用 `get_alpha_yearly_stats` 直接验证 2014–2016 空窗这个悬置硬约束。

**状态**：两批队列处理中，未收批。判据：任一臂 |S|≥1.58 且逐年 longCount>0 才可推翻截面无定价力；
全灭且六维补齐才 seal(需用户确认 + A 通道证据)。

#### 批B 读数（sentiment26，批次 `WzDuS1bZ4via7x1hzukgcJw`，3/3 COMPLETE）— 3/3 REJECT

| 机制 | alpha | S | 2Y | TO | fRA |
|---|---|---:|---:|---:|---:|
| kurtosis 反向+backfill | `zqdW1W1G` | −0.66 | −0.34 | 0.279 | 5 |
| skewness 反向+zscore | `LLKRARAv` | −0.52 | −0.50 | 0.854 | 6 |
| relpopularity IR | `d5aQAQLw` | −0.12 | −0.49 | 0.180 | 3 |

**归因**：三条全负 S、2Y 全负 ⇒ 注意力分布二阶矩(kurtosis/skewness)在 KOR/TOP600 无截面定价力。
十年覆盖问题无须再查(负信号谈不上定价力)。sentiment26 弱保留集被证伪，与 wave216 一阶水平/Δ 死一致。
**不再开波**。

#### 批A 读数（other553，批次 `uoB8H6JU52z90t1dFdB040S`，5/5 COMPLETE）— 5/5 REJECT

| 机制 | alpha | S | 2Y | TO | fRA |
|---|---|---:|---:|---:|---:|
| est 横截面分歧度(反向)+backfill | `9qlR0VGq` | −0.49 | −1.10 | 0.245 | 5 |
| 分歧度×分析师家数门控 | `e7arR91d` | −0.06 | −0.25 | 1.372 | 6 |
| 分歧度一阶差(industry) | `qM7XqW5O` | 0.42 | −0.19 | 1.361 | 6 |
| PT 修正 spread | `d5aQLO9J` | −0.30 | −0.85 | 1.334 | 7 |
| sal 分歧度中性化 | `E5QKJvNJ` | −0.17 | 0.53 | 1.431 | 6 |

**归因**：核心分歧度臂 `9qlR0VGq` S −0.49 / 2Y −1.10，即使反号也仅 +0.49，远低于 1.58 闸；
其余 4 条 TO 1.33–1.43 爆表(逐日重算的分歧/修正 spread)或 S 近零。
**Diether/Malloy/Scherbina (2002) 分析师预测分歧度论在 KOR/TOP600 卖方预测向量上不成立**，
与 wave192 一阶矩机制判死一致，二阶矩正交轴也无机遇。failed_ra 5–7 = RA 闸全灭，信号层死非 prod 墙。

### 6.7 最终结论（2026-11-17）

流水线全链（12 集六维复审 → 裁定 + 独立复核 → 2 集 8 臂回测）收口：
**批A 5/5 + 批B 3/3 = 8/8 REJECT，0 颗可交付**。

| 阶段 | 结果 |
|---|---|
| 权威死表 | KOR 16 正式封存集 + 85 死机制，硬死集全跳过 |
| 六维复审 | 11/12 PROVISIONAL(六维未穷尽)，仅够暂缓不判死 |
| 三条件收敛 | 可攻 2 / 封存 9 / 待决策 1 |
| 幽灵算子闸 | `vec_std_dev` 拦截，改 `vec_stddev` 后才通过 |
| 8 臂回测 | 8/8 REJECT，全信号层死(RA 5–7)，非 prod 墙 |

**为何 0**：未亮塔 7 个面全部穷尽——institutions(全死)、news(W1–W3 30/30 REJECT)、
sentiment(other553 二阶矩本波死 + sentiment26/23 死或弱)、earnings(字段不支持 PEAD)、
imbalance(字段不支持 + 塔倍率1.0)、macro(恒零无截面)、socialmedia(零信号面)。
在「11-16 只打未亮塔」红线下无合格候选；不挪用已亮塔 prod-clean 存量充数。

**不自行 seal**：other553/sentiment26 虽已六维基本补齐且全灭，但 A 通道论坛证据为本轮 no_result/旧帖无效，
按纪律 seal 需用户确认 + 论坛取证，Agent 不自封。记忆条目已更新为「复审 11/12 未穷尽但收敛后 0 交付」。

**待用户决策**：`sentiment23`(156 字段含分歧度族，字段支持但 cov 0.25 稀疏、与 other553 机制重复)——
是否值得再投低覆盖探针，或为避免重复直接放弃。本轮默认放弃(边际价值低)。

**与 W4 的对照**：W4 是在**已判死集**(fund_holdings_panel)第 7 次误发、纯浪费配额；
本轮所有 8 臂都在**六维复审判定 PROVISIONAL + 三条件收敛后的活集**上测真正未测的二阶矩新几何，
是先核死表 → 幽灵算子闸 → 才开波的正确流程。虽同为 0 交付，但性质不同：前者是流程失误，后者是穷尽后的诚实结论。

## 7. 新任务：KOR 10 颗 regular alpha（2026-11-17，用户点名 Institutions → 放行换集）

用户新指令：固定 KOR、优先 ATOM、交付 10 颗验证通过的 regular alpha，点名先查 Institutions。
**第 1 步权威核实**：KOR institutions 塔 0/3（未点亮，符合排除条件），但全 category 仅 2 集且均判死
（`institutions6` 在 ledger 死表；`fund_holdings_panel` 有 KOR-FUND-HOLDINGS-PANEL-DEAD 且 W4 刚 10/10 全灭）。
全字段探测已做（11/11 + 30/30，详见各自档案）。**经 AskUserQuestion，用户选「允许换未点亮塔的数据集」**。

换集后按用户完整 SOP（查论坛/论文 → 全字段画像 → 机制模板 → 组臂回测 → 流水线并发≤2）执行：

### 7.1 sentiment23 主攻（156 字段，KOR/TOP600 从未实测）

- 全字段探测完成，画像归档 `tracking/KOR/reference/datasets/sentiment23.md`。
- 论文锚 **Diether/Malloy/Scherbina (2002)** 分歧度论（高分歧→低收益，Miller 卖空约束高估）；
  论坛检索超时记工具故障。实名核对剔除跨平台幽灵字段 `snt23pos_conf_up_83`。
- W1 `2HZsuL9Hm50m8Qyf5lX5Wjm`（8 条，CI 宽度/std/水平/dts 四族 + 正反双向）：**8/8 REJECT**。
  CI 宽度正反都≈0（0.03 / −0.23）⇒ 分歧度轴本身在 KOR 无截面定价力，非方向错。

### 7.2 imbalance5 配置破闸辅助（验证"判死太快"）

- 批1 `1btTkugZk4RK99e1eoK7mnd0`（REV&MOM/d4）：S **1.10–1.32**（推翻档案 0.51–1.09 天花板），
  但 2Y −0.56…+0.19 全不过。
- 批2 `2Q4STx2Zf4zL8wR16lkaHZz1`（CW 解药 + 换档 + 窗口）：最优 `xAvnkp7N` S1.32/F0.83/2Y−0.03/fRA4，
  CW 已解、S/F/invest 全升，但 **LOW_2Y_SHARPE 机制性不可破**（逐年 S<1.0 占 4/10，2022 −1.75）。
- 详见 `tracking/KOR/reference/datasets/imbalance5.md` §8。

### 7.3 本任务最终交付（诚实报数）

**0 颗通过全闸的 regular alpha**。理由：
1. Institutions 塔全死（用户已放行换集）。
2. sentiment23 分歧度机制 8/8 信号层死。
3. imbalance5 S 突破但 2Y 机制性衰减，13 条臂无一条过 2Y 闸。
4. 今早全未亮塔 8 臂亦全灭。

在「只打未亮塔 + 10 颗严格验证」双约束下，KOR 无可交付候选。**不挪用已亮塔 prod-clean 存量充数**，
不把 2Y 不过的近闸件（xAvnkp7N 等）冒充合格。若用户放宽「只打未亮塔」或降低 10 颗硬指标，可另行评估。

**本轮额外价值**：证实用户「判死太快」在 imb5 的 S 天花板上成立（换档救活 S/CW/invest），
但 2Y 硬闸是 regime 条件因子的真正死因——把"配置假象"与"机制性衰减"分离，避免未来重复扫 backfill/winsorize 谱。
