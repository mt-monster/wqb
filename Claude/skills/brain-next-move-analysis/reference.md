# 日报取数与字段读法（配套 [SKILL.md](SKILL.md)）

> 章节大纲、建议模板与区域态势只在 SKILL.md 里定义一份；本文只写**每章怎么取数、返回的字段怎么读、常见误读**。
> 日期一律用 SKILL §1 的 ET 时间；示例里的 ID、日期都是占位。

## 通用规则

- **认证**：由 MCP 服务端自动完成（凭据在服务端的 `.env` 里）；`authenticate` 工具**没有参数**。agent **不得读取**凭据文件、不得打印凭据、不得向用户索要口令、不得把口令传给任何工具（AGENTS.md）。认证失败 → 请用户在本机终端登录后重试。
- **并行**：各章取数互不依赖，可一次并行发出；同一章内 `get_user_alphas` → `get_alpha_details` 是依赖关系，须串行。
- **失败不编数**：某章工具失败，日报里写「本章数据不可用：<原因>」，不得用旧数或估计值补。
- **论坛**：日报默认不读论坛。只有用户点名，或 §比赛 / §公告 里出现需要查证的规则变更时，才用 `search_forum_posts`（见 `brain-forum-browse`）。
- **任务清单**：宿主提供什么清单工具就用什么；不要在文档里指定某个宿主专有的工具名。

## 平台公告

`get_messages(limit=30, offset=0)`。不传 `limit` 会拉全量，日报不需要。摘要只保留与挖矿 / 提交规则 / 比赛 / 算子与数据更新相关的条目，其余不写。**PPA 主题公告**（标题含 "Power Pool"）交给 ra-pipeline 步 1 §1.6 解析，日报只提示「有新主题，见步 1」。

## 排行榜与多样性分数

- `get_leaderboard(user_id=<用户 ID>)`：用户 ID 由用户告知；日报里写占位（`<USER_ID>`），不把真实 ID 落盘。
- `value_factor_trendScore(start_date, end_date)`：**两个日期都必填**（ISO UTC，如 `2026-07-01T00:00:00Z` → `2026-09-29T23:59:59Z`），只统计该区间内**已提交（OS）REGULAR alpha**。返回 `diversity_score`（0–1，越高越好）、`N`、`A`、`P`、`per_pyramid_counts`。
- **读法**：分数本身没有平台阈值。只做「同一起点、不同终点」的前后比较；后一次低于前一次 → 建议「下一波 S0 改攻未点亮塔」。区间不同的两次读数不可比。
- 用户在意的「value factor 趋势」= 这个分数随时间的变化，不是某一天的绝对值。

## 比赛

1. `get_user_competitions()` → 列出参与的比赛，只保留**未截止**的（按 ET 今日判断）。
2. 对每个保留的比赛：`get_competition_details(competition_id)` + `get_competition_agreement(competition_id)`。
3. **必须读协议全文里的 universe / delay / alpha 类型 / 提交上限**，写进日报的「规则核对」一列。
4. 推荐 alpha 时逐项对照；不符合就不推荐。

**真实案例**（症状 → 原因 → 防范）：某全球赛（GAC）的日报里推荐了 USA 区的 alpha——症状是「建议看起来合理」，原因是没读协议、想当然认为「有 alpha 就行」，协议实际要求 GLOBAL universe。防范：建议里的每个候选都要写「协议第几条 → 满足」，缺这一列就不发这条建议。

## 事件

`get_events()`，**无参数**（不要传任何占位参数）。按 ET 今日过滤掉已过去的事件；剩余按日期升序写「未来 N 天」。

## Alpha 表现

范围与取法见 SKILL §2.1；这里写字段读法：

- `get_user_alphas` 返回精简结构（`results` + 分页信息）；**API 单次最多 100 条**，用 `offset` 翻页。`region` / `status` / `is_super` 是**客户端过滤**（会多翻几页），`type` 是服务端过滤。
- `get_alpha_details(alpha_id)`：表达式、设置、`is` 指标与 `checks`；`get_alpha_yearly_stats(alpha_id)`：分年 Sharpe / 收益（近 2 年稳健性看这个）；`get_alpha_pnl(alpha_id)`：净值曲线（需要时再取）。
- `check_correlation(alpha_id, correlation_type="production", threshold=0.7)`：**只读的相关性检查**，用于给建议提供「会不会撞 prod 墙」的依据；它**不是提交**。
- OS alpha 的改进建议给两个角度：① idea 本身（窗口 / 算子 / 条件是否符合窗口规则，1/5/22/66/252 等）；② 结合比赛规则或近季度**未点亮塔**（`get_pyramid_alphas` + `get_pyramid_multipliers`）——**只列塔与缺口，具体选集交给 ra-pipeline 步 2**，不在日报里点名字段。

## 金字塔

- `get_pyramid_alphas()` 默认统计**当季**（UTC 季度边界；跨季度首日会与 ET 日历日差几小时，做 1 号 / 季度末判断时以 ET 为准）。每个 category 的 ACTIVE 数 ≥ 3 = 已点亮。
- `get_pyramid_multipliers()`：平台鼓励度（乘数）。**乘数只说明平台鼓励哪里，不是选塔准则**——选塔以「未点亮」为第一准则（SKILL §3 前置检查 1）。

## 区域态势

命令与口径见 SKILL §4。字段读法：

| 字段 | 读法 |
|---|---|
| `backtested` / `pass_ge_158` / `pass_rate_pct` | 本地 `backtest_results` 的条数 / `sharpe ≥ 1.58` 的条数 / 比例（**宽口径**，不代表可提交） |
| `active_local` | 本地库里 `platform_status=ACTIVE` 的条数（与平台全量可能有偏差） |
| `campaigns` / `exhausted_pct` | registry 里 campaign 层的 untried / in_progress / exhausted 分布与穷尽占比 |
| `suggested_action` | 数据侧提示，判据在 SKILL §4 表；不覆盖 `entry_verdict`，不是转区结论 |

## 常见误读（症状 → 原因 → 防范）

| 症状 | 原因 | 防范 |
|---|---|---|
| 日报把「达标 12 条」写成「有 12 条可提交」 | `pass_ge_158` 只看 Sharpe，没算 RA 硬闸与 prod 相关性 | 与 `get_mining_yield(strict=True)` 的 `ra_clean` 并列写，并写明口径 |
| 建议开 X 战役，但 X 所在塔当季已点亮 | 用「乘数高」当理由，没做 SKILL §3 前置检查 1 | 每条建议写三项前置检查的结果 |
| 建议「再开一波」，但该区停止规则已命中 | 没查 L.2 停止规则与 waiver | 前置检查 3；命中只能建议换区 / 换轴 / 等用户放行 |
| 「事件」章列出了上周的活动 | 没按 ET 今日过滤 | SKILL §1 取时间；事件按日期过滤 |
