# EUR / 判决三源全文对照审计底表（2026-11-05）

> 用途：换面 / 写备靶 / 登记补位件 / 宣布某面挖尽前，**唯一权威判决底表**。杜绝「按 dataset 键索引」漏判导致的重复刷判死面白烧（§101 实证）。
> 本表是参考表（非流水）；波次流水在 `WAVE_LEDGER.md`，口径与代码同步按用户要求随判定逻辑更新。

## 一、口径（取值来源 + 计算式 + 阈值）
- 数据源：`get_datasets(EUR, delay=1, universe=TOP2500, category=null)` → 173 个 dataset。
- 三源（缺一不可，§93 / §97 / §101 坐实）：
  1. `s1` = `get_dead_datasets(EUR)`（ledger_kv `*_dead` 键）→ 4 集：ml_factor_proj / model354 / news36 / news38。
  2. `s2` = `get_dead_ends(EUR)` **全文 JSON（163 条）token 级匹配**——不是只看某 dataset 字段；判死记录常以 `family` / `reason` 文本出现（event_relation 即在 id=1338/1341 的 family/reason 里命中，按 dataset 键查会漏）。
  3. `s3` = `WAVE_LEDGER.md` 判死散文（收手/判死/封存/全灭/fast_kill/整集/不可达/天花板/零配额/贫瘠/机制封存 等 286 行）token 级匹配。
- 计算式：`clean = NOT s1 AND NOT s2 AND NOT s3`。`s2` 命中 ANY 即视为「有判死记录」，不区分是整集判死还是某族判死（族级判死同样禁止回刷该族）。
- 阈值/边界：token 化用 `/[^a-z0-9_]+/` 切分后精确相等；中文散文里的英文 dataset id 能捕获，`rule` 里点名的「未测」集也须再核散文（news18/news52/news59 已实质挖过）。

## 二、汇总
- 总数据集 173；三源全文 clean 82 集；其中未点亮塔（earnings/insiders/institutions/macro/news/other/pv/risk/sentiment/socialmedia）clean 40 集。
- 已点亮塔：model 3/3、fundamental 3/3、imbalance 3/3、analyst 9/3；未点亮：pv 2/3、risk 2/3、other 2/3（各缺 1），sentiment 1/3、news 1/3，macro/earnings/institutions/socialmedia 0/3，insiders 1/3。

## 三、未点亮塔 clean 40 集（三源全文零命中，仍须过四项前置才可派）
- OTHER（22）：earningscall_sentiment, equity_conc_metrics, equity_forum_data, euro_equity_imbalance, event_sentiment_signals, order_book_imbalance, other128, other250, other296, other315, other327, other335, other384, other424, other436, other545, other546, other635, other699, stock_cluster_dl, stock_search_trends, workforce_flow_skills
- INSIDERS（1）：insiders12
- MACRO（1）：macro10
- PV（16）：investor_activity, pv1, pv103, pv109, pv13, pv141, pv149, pv173, pv20, pv29, pv30, pv37, pv47, pv87, univ1, univ2

## 四、本会话重点集的判决状态（全文 token 对照结果）
| dataset | cat | s1 | s2 | s3 | 结论 |
|---|---|---|---|---|---|
| event_relation | other | F | **T** | F | 已判死（id=1338/1341）；wave1 首批 2 条白烧、剩余模板不派 |
| news29 | news | F | T（主题显著性族 id=1343） | T | 已判死面；wave1 6 条白烧、6/6 全灭整集收手 |
| news50 | news | F | T（id=1352 机制封存） | T | 已判死面、不派 |
| news73 | news | F | T（id=1600 整集判死） | T | 已判死面、不派 |
| news31/news20/news17/news48 | news | F | T（1346/1345/1347/1344 零配额） | T | 已判死 |
| search_interest | other | F | F | **T** | 散文 L1387 判死（只能作门控腿） |
| event_sentiment_signals | other | F | F | F | clean 备靶（须过四项前置） |
| other546 / other635 / other699 | other | F | F | F | clean 备靶（须过四项前置） |
| equity_forum_data | other | F | F | F | clean 备靶（须过四项前置） |
| insiders12 / macro10 | insiders/macro | F | F | F | clean 备靶（须过四项前置；insiders1 塔 S 天花板 0.9–0.95 的历史结论须复核是否族/集限定） |

## 五、派发前四项前置（硬约束，clean 只是准入第一步）
1. 字段族同源比对：`get_datafields` 取候选全量字段，与所有判死面（news48/50/29/73、event_relation、已判死族）比对后缀族是否一一对应；同源＝同一机制面，必须换骨架几何才算真换面（§98 Memory）。
2. 覆盖逐年：`get_alpha_yearly_stats` 逐年 `longCount>0 && pnl≠0`；判据＝连续多年彻底空窗，非「近十年满覆盖」（用户 2026-10-30/31 两次修正）。
3. 用机制前取证：`search_forum_posts` / `read_forum_post` 捞模板 + `web_search`/`web_fetch` 查论文先验；论文只验第一性原理，不等于验证该集作分组轴有效。
4. 模板池 ≥10 个结构互异模板（骨架/算子几何/矩/分组轴/非线性变换），标注来源(forum/paper/自建)，按模板编号归因；算子数 ≤12、越少越好。

## 六、与既有纪律的关系
- 本表升级 §93 / Agent Memory「判决对照 = get_dead_datasets + WAVE_LEDGER 散文」两源口径：补 `get_dead_ends` 第三源，且三源都须**全文 token 级**匹配，不能只按 dataset 键索引。
- 配合：「换 dataset id ≠ 换机制面」「写前瞻/备靶前逐集标判决状态」「存量重筛登记补位件前对照历史判决」三条，分别覆盖换面 / 前瞻 / 回溯三个入口。

## 七、★★★★★ 第三类漏判：「同机制面伪 clean」+ clean 40 集再筛（2026-11-05 §102）
- 背景：§六把判决对照升级为「三源全文 token 级」；但三源都按 **dataset id** 匹配。本轮 §102 同源比对发现：**id 零命中 ≠ 机制面干净**。
- 新增第 5 项前置「同源比对」（最高优先）：把候选**字段语义/机制**与所有判死面逐族对照；同机制面即使 dataset id 不同也判「伪 clean」，不派。
- 40 个未点亮塔 clean 集本轮再筛结论：
  - `insiders12` → 伪 clean（同「内部人交易净买入」面：insiders1 id=1598 / insider_feats id=1341 / insider_agg_matrix L2109 天花板 0.93 prod 0.7447；L2051 明文 cov 太薄排除）。
  - `stock_search_trends` → 伪 clean（6 字段全 `search_interest_*`；L1387 search_interest 信号腿判死）。
  - `macro10` → 本轮不可用（仅 1 个泛化字段 `mcr10_value`，无法组 ≥10 互异模板；L1642 亦记覆盖/字段数不足）。
  - `workforce_flow_skills` → 本轮选定靶（劳动力流动，与所有判死面正交；四项前置 + 中文上下文复核通过）。其余 clean 集**未逐一做完同源比对** ⇒ 仍须逐集核，不得据本表直接判「合法新面」。
- 四项前置升级为**五项前置**：①同源比对（新增）②逐年覆盖 ③论坛+论文取证 ④≥10 结构互异模板池 ⑤算子数/窗口/禁混静态闸。
- 本波状态：`s1_workforce_flow_skills_wave1` 首批 T01/T02 已派发（multisim `2mguMZ6qn4Wm8NFYF3nuUpc`，在飞 progress 0.1、占 2 slot），收批待 §103。