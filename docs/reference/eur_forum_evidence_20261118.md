# EUR 未点亮塔机制 — 论坛/文档取证（2026-11-18）

> 查论坛唯一方式：wq-brain-http 5 个 MCP 工具（SOP §8.11）。
> **工具故障 ≠ 无解**：`search_forum_posts` 连续 ~15 次 30s 超时或 0 结果（连精确已知标题都 0）⇒ 判为工具故障，非「论坛无解」。

## 检索结果

- 文档两步绕行（`get_documentations`→`get_documentation_page`→`/posts/<id>`→`read_forum_post`）可用，
  读到 5 篇通用 BRAIN TIPS 帖；**无一篇直接讨论** institutions6 家数不对称 / insider 净买入 / analyst 修正广度 / 1.2 倾斜腿。
- 3 个文档内嵌 article_id（14833936207383 / 14834608658199 / 10431497209623）经 post API 返回 404（是 article 非 post）。
- alphaCount 时效：任何检索结果均未暴露字段 alphaCount，无法据此判拥挤；prod 拥挤仍以 MCP `check_correlation` 实测为准。

## 可复用结论（已用于本战役）

| 来源 | 结论 | 应用 |
|---|---|---|
| doc `neut-cons` | Institutions→Sector/Industry；Insider→Industry/Subindustry；Analyst→Industry 中性化；EUR 建议 country/exchange 双中性 `group_cartesian_product(country,industry)` | 倾斜腿内层轴选 industry；外层 FAST/market 保留强腿幅度 |
| 8046468280727 [BRAIN TIPS] | 降相关 = 等价字段/算子/不同分组/**混入互补不相关信号** | 「强腿 + 倾斜腿点未点亮塔」结构的论坛依据（无 1.2 权重细节） |
| 8360363631127 [BRAIN TIPS] | `trade_when(event, alpha, -1)` 事件持仓、低换手 | insider 申报事件型字段的备选门控（本战役未使用：无 filing-date 字段） |
| doc Vector Data Fields | `vec_count` 事件计数 + `ts_rank`/`ts_decay` 平滑（原始 vec_count TO 可达 200%） | 家数/笔数族必须用 ts_zscore+backfill 平滑降 TO（N1NGbddg 结构印证） |
| 8209806533015 | 避免过拟合：不挑最优单点，取邻近参数均值（decay 4&6→5） | 倾斜权重/窗口取甜点区中值，不追极值 |

## 落地状态

- 论坛检索通道当前不可用 ⇒ 本战役机制依据以**平台字段语义 + 本地实证 + 官方文档**为主，论坛仅作方向性佐证。
- 待 search_forum_posts Playwright 后端恢复后重跑针对性检索（insider 净买入 / 机构家数不对称 / analyst 修正广度）。
