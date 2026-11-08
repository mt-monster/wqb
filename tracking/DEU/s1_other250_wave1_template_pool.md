# other250 波1 模板池台账（DEU / TOP500 / D1 / OTHER 单塔）

## 一、字段面（get_datafields 实拉，12 VECTOR 全在，cov 0.6126，拥挤度 ac 0-2）
- 评分对：`average_star_score` ↔ `oth250_item_rating`（0-5 星，跨源近重复）
- 评论数对：`oth250_item_review_count` ↔ `total_review_number`（累计评论量）
- 排名对：`oth250_rank` ↔ `sales_position_rank`（畅销排名，1=最好）
- 价格：`oth250_item_display_price` / `product_listed_price`（USD）；区间 `price_range_max/min`、`price_upper/lower_bound`
- 机制面：产品定价力 / 满意度 / 需求动量。跨源对可做同机制净额合成（同量纲）。

## 二、覆盖核验（get_alpha_yearly_stats 硬闸 ✓）
- 探针 `O0Axgqxv`（评分水平）/ `omEgZAgv`（排名反转）S −0.25 / −0.08（探针仅测覆盖）。
- **2014-2023 逐年 longCount 45→108 名/年、pnl 逐年非零 = 10/10 满覆盖，无连续空窗**。cov 0.613 是横截面每日覆盖，不是年度空窗。判据：可开正式波。

## 三、论坛金帖两读（search_forum_posts + read_forum_post）
- 金帖：「【Alpha灵感】在线评论可以预测个股长期回报」（YH69102，2024-04，21 票），引用论文 **arxiv 1905.03189**（JD 1800 万条评论→长期回报预测，6246 特征）。
- **作者提交占位**：USA 线「已经可以提交，相关性约 0.6」——该机制线生产池占用低。
- **核心反转用法（照抄面）**：论文用 1 天评论预测 2 个月回报；作者倒过来「用长期评论历史预测短期回报」→ 明显提升。
- **未解决疑问（≥3 个差异化臂来源）**：① ts_backfill 在覆盖 100% 时反而更差（对照问题）② bucket(rank(equity)) 分组轴的意义 ③ regression_neut 去基本面成分 vs vector 正交。
- 塔混禁令注记：金帖骨架 `regression_neut(x, cap)` 含 cap（PV）⇒ DEU 禁 OTHER+PV 两塔，**照抄臂改造为 T3 长窗机制臂**（0 个照抄臂，4 个开放问题臂：T3/T4/T6/T9）。

## 四、论文/外部取证（web_search 2026-11-03）
- arxiv 1905.03189（金帖引用）：在线评论量/评分对长期回报有预测力，方向=好评多→回报高。
- 商业实证（eightx 2026）：revenue/bestseller rank ≠ profit rank，成本集中于高销量品；定价力 = 能在高排名下维持高价（T7/T8 方向先验）。
- 诚实条款：本轮 web_search 学术命中有限，方向先验主要靠金帖论文 + 客户满意度→回报（ACSI 系）通识；分歧/区间宽度类无强先验，按探索臂处理。

## 五、模板池（12 个结构互异 ✓，全部单数据集 other250，OTHER 单塔，无 PV 内建字段）
| # | 机制 | 表达式 | 矩/几何 | 方向先验 |
|---|---|---|---|---|
| T1 | 满意度水平 | `group_rank(ts_mean(vec_avg(oth250_item_rating), 22), subindustry)` | 水平 | 正 |
| T2 | 满意度动量 | `group_rank(ts_delta(ts_mean(vec_avg(oth250_item_rating), 66), 22), subindustry)` | 一阶差分 | 正 |
| T3 | JD 长期评论信息含量（开放问题①/③臂） | `group_rank(ts_mean(vec_avg(average_star_score), 252), subindustry)` | 长窗水平 | 正 |
| T4 | 需求增量（评论累计增速） | `group_rank(ts_av_diff(vec_avg(total_review_number), 22), subindustry)` | 增量几何 | 正 |
| T5 | 畅销排名改善 | `subtract(0, group_rank(ts_delta(ts_mean(vec_avg(oth250_rank), 5), 22), subindustry))` | 排名差分取反 | 正 |
| T6 | 跨源评分分歧（同量纲净额，开放问题③臂） | `group_rank(subtract(vec_avg(average_star_score), vec_avg(oth250_item_rating)), subindustry)` | 净额分歧 | 探索 |
| T7 | 价格区间宽度（促销/定价行为） | `group_rank(divide(subtract(vec_avg(oth250_price_range_max), vec_avg(oth250_price_range_min)), add(vec_avg(oth250_price_range_max), vec_avg(oth250_price_range_min))), subindustry)` | 比率几何 | 探索 |
| T8 | 价格×排名背离（定价力持续性） | `group_rank(ts_corr(vec_avg(oth250_item_display_price), vec_avg(oth250_rank), 66), subindustry)` | 相关交互 | 正 |
| T9 | 真需求交互（评分×评论增速，开放问题②臂） | `group_rank(multiply(rank(vec_avg(oth250_item_rating)), rank(ts_av_diff(vec_avg(oth250_item_review_count), 22))), subindustry)` | 乘法交互 | 正 |
| T10 | 质量不稳定 | `subtract(0, group_rank(ts_std_dev(vec_avg(oth250_item_rating), 22), subindustry))` | 二阶矩 | 正 |
| T11 | 排名信噪比 | `subtract(0, group_rank(ts_ir(vec_avg(oth250_rank), 22), subindustry))` | 信噪比几何 | 正 |
| T12 | 评分峰值年龄（新鲜度衰减） | `group_rank(ts_arg_max(vec_avg(oth250_item_rating), 66), subindustry)` | 事件几何 | 探索 |

窗口白名单：5/22/66/252 全合规。量纲安全：subtract(0,·) 只作用于 group_rank 无量纲输出；跨源净额只在同量纲对（星↔星、USD↔USD）内做；乘法交互前先 rank 无量纲化。

## 六、双预检与派发实录（2026-11-03 06:4x）
- preflight_expressions：12/12 valid，8 字段全存在，无 unknown，无内建字段（塔混干净：仅 OTHER）。
- verify_expr：首版 11/12 过；T9 内层 `group_rank(x)` 少分组轴被拒 → 改内层 `rank()` 无量纲化，二验通过。算子逐一在 103 名单（group_rank/rank/ts_mean/ts_delta/ts_av_diff/subtract/divide/add/multiply/ts_corr/ts_std_dev/ts_ir/ts_arg_max/vec_avg）。
- 派发：`other250_wave1`（task，pid 18004），batch-size 2 / concurrency 1，12 臂 6 批。

## 七、批 1 瞬时故障与重试管线（2026-11-03 06:44）
- T1/T2 双双 ERROR，文案=平台通用运行错「There was an error…Please try again」。
- **决定性证据**：T1 表达式与 06:32 覆盖探针 `O0Axgqxv` **一字不差**且当时正常出数（S −0.25）⇒ 同式不同命 = 平台瞬时故障，表达式无罪（与 sentiment7 T3/T4 同时段同文案双死互证，06:38-06:44 平台不稳窗口）。
- 处置：重试管线 `other250_w1_retry.json`（T1/T2 原式，独立 CSV）；主波继续收 T3-T12。若重试再败才考虑结构性（届时先排除 oth250 数据管道侧故障）。

## 八、批 2-3 收批（2026-11-03 06:5x）
- T3（评分长窗 252 水平）`d5WRPp2j` S **−0.16** / T4（评论数增量 ts_av_diff）`1YNz2eqW` S **−0.02** —— 两臂正常出数但全弱；T1/T2 ERROR 保持入重试池（2 臂未扩）。
- T5-T12 在飞（pid 18004 存活）；本波同时兼任平台健康探针（06:48 后批次成败是「干净批」判据）。
- news20_wave1 已占满第 2 并发槽（pid 17224）；重试池等干净批信号后补发。

## 九、全波收口（2026-11-03 07:0x，12/12 落地）
| 臂 | 机制 | S | 判定 |
|---|---|---|---|
| T1 | 评分长窗均值（探针 O0Axgqxv 同式） | ERROR→重试 | 瞬时故障 |
| T2 | 评分 66→22 差分 | ERROR→重试 | 瞬时故障 |
| T3 | 评分 252 水平 | −0.16 | 弱 |
| T4 | 评论数增量 ts_av_diff | −0.02 | 弱 |
| T5 | 畅销排名改善（排名差分取反） | **+0.57** | 全波最优，仍远低闸 |
| T6 | 跨源评分分歧净额 | 0.00 | 无信号 |
| T7 | 价格区间宽度 | −0.58 | 弱 |
| T8 | 价格×排名背离 | −0.25 | 弱 |
| T9 | 真需求交互（评分×评论增速） | −0.17 | 弱 |
| T10 | 评分波动（二阶矩） | −0.34 | 弱 |
| T11 | 排名信噪比 | +0.20 | 弱 |
| T12 | 评分峰值年龄 | −0.34 | 弱 |

**全波判定**：可测 10 臂 max|S| = 0.57，正负号混杂（5 正 5 负）无方向一致性 ⇒ **oth250 消费评分机制面在 DEU/TOP500 无信号**。按机制×数据集二维律，只封「DEU/TOP500 × oth250 消费评分模板池」，不外推其他区域/集。

**重试池补发实录（2026-11-03 07:06）**：`sentiment7_err_retry.json`（8 臂）已派发 pid 53768 / task `snt7retry20261103`；`other250_w1_retry.json`（T1/T2 原式 2 臂）等下一个槽。重试池表达式为原波双预检通过的原式一字不改（同式先前成功 = 故障无罪，改式无意义）。
