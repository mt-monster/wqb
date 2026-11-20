# EUR 流水线必做归因层 + 论坛确定性检索通道（2026-11-19 实施）

> 用户两项指令的落地：
> ① 「拿到 alpha 回测结果后，归因分析…**查 PnL、查论坛找破解办法**这一步**放到流水线的步骤上必做**」
> ② 「检查一下查论坛的方式，**确保必须能查出结果来**，不是工具问题」
> 全仓回归：**4441 passed / 17 skipped / 0 failed**。

---

## 一、第 ① 项：归因层做成流水线必做步骤

### 1.1 新增两个模块（toolkit 内，skill 装到仓库外也能跑）

| 模块 | 作用 |
|---|---|
| `Claude/skills/wq-brain-campaign-toolkit/scripts/_lib/attribution.py` | 逐年 + PnL 三线 + 缺陷分类 + 墙识别 + 论坛破闸编排（纯函数为主，可单测） |
| `Claude/skills/wq-brain-campaign-toolkit/scripts/_lib/forum_corpus.py` | 论坛语料的**确定性**访问（Zendesk 列表端点 + 本地过滤） |

### 1.2 流水线接入点（关键：必须在 wave_results 入库之前）

`pipeline.py::stage_review` 新增 `_run_attribution_stage(ctx, ck, rows, candidates, near, t)`，位置在
`to_band` 之后、**`wave_results` 自动入库之前**：

```
[attribution] GrmdGb0J: 满十年=False 零持仓年=['2014'] 最弱年S=-0.74
             缺陷=['数据不满十年','失效年','失效年集中','可投资性折损','部分风险暴露','波动过高','横截面过窄','产线拥挤']
[attribution] QP03GRn5: 满十年=False 零持仓年=['2014'] …
[attribution] 论坛破闸 S_GATE: 命中 3 帖｜HKG Tips: Turnover, Risk Exposure, and Datasets
[attribution] 论坛破闸 F_GATE: 命中 3 帖｜两个「看起来能调」其实调不动的旋钮：fitness 的 0.125 换手下限
[attribution] 论坛破闸 PROD_WALL: 命中 3 帖｜what i found late about prod correlation.
[attribution] 已写 ledger 键 s4_attribution_EUR_s2_fund_holdings_panel_atomic_d1（2 件 / 排除 2 件 / 墙 [S_GATE,F_GATE,PROD_WALL]）
[attribution] 数据层排除（近十年不成立）['GrmdGb0J','QP03GRn5']：candidates 2 → 0
```

### 1.3 归因层做三件（缺一不可）

| # | 内容 | 端点 / 来源 | 为什么聚合指标看不出来 |
|---|---|---|---|
| 1 | **逐年** longCount/shortCount/pnl/returns/drawdown | `GET /alphas/{id}/recordsets/yearly-stats` | coverage 与「数据满几年」无关。实测 `fund_holdings_panel` 在 EUR cov 0.843–0.918，但 **2014 全年 longCount=0** ⇒ 只有 9 年数据 ⇒ **近十年硬约束不成立**（数据层排除，优先级高于 prod 墙） |
| 2 | **PnL 三线**：原始 / 风险中性化 / 可投资性约束 | `GET /alphas/{id}/recordsets/pnl` | 可投资性折损（实测 5,387,719 → 3,117,156，**只有 58%**）与风险暴露占比（RN/raw=0.58）只在两条线的比值里 |
| 3 | **论坛定向破闸**：按本波主导墙取词检索 | `search_forum_posts_local`（确定性） | 墙→破解办法的对照必须来自社区经验，否则只是自己的感想 |

### 1.4 缺陷分类（每条必须带读数判据）

`数据不满十年` / `近十年成立` / `失效年` / `失效年集中` / `可投资性折损` / `非风险暴露`·`部分风险暴露`·`强风险暴露` / `波动过高` / `横截面过窄` / `权重集中` / `产线拥挤` / `逐年读数缺失`（**不得当作通过**）

### 1.5 fail-closed 行为
- **数据层排除**（任一年零持仓）⇒ 该候选从 `candidates` 中**移除**，并写进 wave_results 前的归因结论。
- 逐年/PnL **取数失败** ⇒ 记「逐年读数缺失：不得当作通过」，**不**静默当成「满十年通过」。
- 论坛抓不到 ⇒ 记「未取证」，**不**阻断流水线（但留痕）。

### 1.6 台账与契约
- 新 ledger 键 `s4_attribution_<region>_<wave>`（用途/写入方/读取方/缺失行为/刷新责任已登记进 `docs/ledger_keys.json`）。
- 新增单测 `tests/unit/06_wave_pipeline/test_attribution_stage.py`（13 例），守护四条：
  recordsets 的**行是按 schema 顺序的数组**（不是 dict，解析错就恒空）、数据层排除判定、PnL 三线折损、墙识别与论坛通道确定性。

### 1.7 两个实测坑（写进模块注释）
- **recordsets 的行是数组**：返回 `{"schema":{"properties":[{name,...}...]}, "records":[[...],...]}`，必须按 schema 映射列名；上一版按 dict 解析导致逐年恒空（假阴性）。
- **瞬时取数错误**：连续取两份 recordsets 时第二次会被吞掉 ⇒ 加指数退避重试（429 专项），且失败必须抛出来而不是返回空列表。

---

## 二、第 ② 项：论坛检索必须查得到（根因定性 + 正路）

### 2.1 根因（源码级）

`forum_functions._search_forum_posts_impl` 里，等不到选择器 `ul.search-results-list` 时**只记 warning、显式不设 `navigation_failed`**（原注释：「可能是真的没有结果，也可能是挑战页；不判 nav_failed」）。
⇒ **`total_found=0` + `navigation_failed=false` 是假信号**：它同时表示「真的没有」与「撞了 Cloudflare 挑战页」。

实测（2026-11-19）：`alpha` / `earnings surprise` / `sharpe` / `post earnings announcement drift` 四个查询
⇒ 3 次 30s 超时 + 4 次「秒回 0 结果」，而同期语料里明明有命中。**我上一轮把「0 结果 + navigation_failed=false」当成可靠无结果，是错的。**

### 2.2 正路（确定性、零超时、零误判）

Zendesk Community **列表端点**（同一 support session，纯 JSON API，无 Playwright）：

```
GET https://support.worldquantbrain.com/api/v2/community/posts.json?per_page=100&page=N
```
实测 `count=11296` / `page_count=113`；列表项**自带** `id / title / details 正文 / vote_sum / comment_count / created_at / html_url`
⇒ **论坛检索 = 拉语料 + 本地过滤**。

**关键词匹配口径**：按**词命中率**折算，不做整串子串匹配——查询 `post earnings announcement drift` 在语料里写作
`post-earnings announcement drift`（带连字符），整串匹配 0 命中（实测）。标题权重 3、正文权重 1，按命中词占比折算。

**实测命中量（800 帖样本）**：sharpe 378 / turnover 225 / correlation 180 / earnings 61 / crowding 40 / sentiment 38 / PEAD 5。

### 2.3 落地（三处）

| 落点 | 内容 |
|---|---|
| MCP 新工具 | `get_forum_posts`（列表）、`search_forum_posts_local`（列表+本地过滤）。**已随 MCP 服务重启注册并实测**（scanned 600 → matched 24 → 返回 5，命中「How to Deal with High Production Correlation」「别再乱混数据了！…你应该多做 ATOM？」等） |
| 旧工具诚实化 | `search_forum_posts` 现在：选择器缺失即 `navigation_failed=true`，返回加 `search_reliable` 与 `hint`（指引去新通道）。实测旧工具现在报 `navigation_failed=True / search_reliable=False` |
| 白名单契约 | `tools/lib/forum_mcp.py` 的 `ALLOWED_TOOLS` 5 → **7 个**（加 `get_forum_posts` / `search_forum_posts_local`），机械闸 `test_forum_single_way_gate.py` 同步；guide §1 新增 §1.1「必须查得到的确定性通道」；AGENTS §8.11 与 INDEX 工具计数（71→73）同步 |

### 2.4 顺带拿到的东西（可直接用于破闸）
- **《How to Deal with High Production Correlation》**（prod 墙）
- **《Reducing Alpha Turnover: Are We Fixing the Cause or Just the Symptom?》**（76 赞 / 24 评）
- **《两个「看起来能调」其实调不动的旋钮：fitness 的 0.125 换手下限，与组合 PC 的 band 下界》**（F 闸）
- **《what i found late about prod correlation》**（prod 墙）
- **《别再乱混数据了！…你现在应该多做 ATOM？》**（61 赞，与「优先 ATOM」政策互证）
- **《[BRAIN TIPS] Using trade_when for Event Alphas and Low Turnover Alphas》**（62 赞）——其 Cons 明写「事件型 alpha **难以拿到高 Sharpe**」「要检查 alpha coverage，别让事件太稀有」
  ⇒ **与我第 3 轮实测的门控 S 1.14→0.79 完全一致**，社区共识与实测互证。

---

## 三、遗留与边界（诚实声明）

1. **`CreateWorkflow` 一族仍不可用**（本次会话 5 条检索路径确认，含重载后）。已写的 workflow 脚本 `.zcode/workflows/field-form-template-mine.dwf.ts`（678 行、静态检查全绿）留在磁盘，环境恢复即可提交。
2. **harness 侧调用新 MCP 工具存在客户端序列化怪癖**（数组参数被发成 object）；服务端已用仓库自带 MCP 客户端验证正常，流水线走的是 toolkit 直连实现（不经过此路径）。重载会话即解。
3. **论坛破闸只产出「线索」，不自动改臂表**：破闸建议进 ledger 与报告，由人或下一轮设计员消费——避免在流水线里自动扫参。
4. **归因层默认只取池内前 6 件**（按 |S| 排序），避免一次收批打太多 recordsets；如需全量需显式调参。
5. `create_multi_simulation` 在 03:00 前后曾 100% FAIL（阶段性故障），16:15 已恢复，流水线实跑成功。

## 四、产物清单

| 类型 | 路径 |
|---|---|
| 新模块 | `Claude/skills/wq-brain-campaign-toolkit/scripts/_lib/attribution.py` / `forum_corpus.py` |
| 流水线接入 | `Claude/skills/wq-brain-campaign-toolkit/scripts/pipeline.py`（`_run_attribution_stage`） |
| MCP | `world-quant-brain-mcp/forum_functions.py`（列表端点 + 评分口径 + 诚实信号）、`brain_mixin_spcread.py`（代理）、`tools_forum.py`（2 个新工具） |
| 白名单/文档 | `tools/lib/forum_mcp.py`、`docs/reference/forum_and_doc_tools_guide.md`、`docs/ledger_keys.json`、`AGENTS.md` §8.11、`Claude/skills/INDEX.md` |
| 单测 | `tests/unit/06_wave_pipeline/test_attribution_stage.py`（13 例） |
| 归因报告 | `output_report/EUR_fund_holdings_panel_form_mine_20261119.md` §12、`output_report/EUR_earnings_template_attribution_20261119.md` |
