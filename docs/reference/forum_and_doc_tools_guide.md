# 论坛 / 文档工具速查（2026-11-17；11-19 补确定性通道；11-20 旧 Playwright 搜索退役）

> **★ 本指南已被裁定为全项目查论坛的唯一方式（2026-11-18 用户指令）**：只经下面 6 个 `wq-brain-http` MCP 工具，
> 不再 requests 抓 HTML / 直连 Zendesk API / 拿 WebSearch 当论坛或论文通道。**论文线唯一稳定通道 = `tools/research/paper_search.py`（Crossref→arXiv→本地论文库三层冗余，2026-11-19；WebSearch/WebFetch/Semantic Scholar 已弃用）**；EVID-PAPER 闸自己调它实证 found=true，查不到即 FAIL。
> **★★ 2026-11-20 旧 Playwright `search_forum_posts` 已整体退役并从 MCP 删除（用户裁定）**：
> 它对任何查询都倾向「success=True + 0 结果」，是 Cloudflare 挑战页造成的**假信号**（见 §1.1）；
> 留着只会被误读成「论坛无此内容」。实现、MCP 注册、client 方法、白名单四处已全部移除，
> 机械闸 `test_retired_playwright_search_is_not_reintroduced` 防止它被加回。
> 检索只剩 `search_forum_posts_local` / `get_forum_posts`（Zendesk 列表端点 + 本地过滤）。
> 实现落点：论坛访问单一实现 `tools/lib/forum_mcp.py`；问题驱动检索 `tools/forum_recon.py`（传输层已切 MCP）；
> 旧抓取链 `tools/forum_research.py` **已删除**（2026-11-18，不留兼容实现）。机械闸 `tests/unit/08_forum_recon/test_forum_single_way_gate.py`；
> 顶层规范见 `AGENTS.md` §8.11。
>
> 目的：{MCP 工具能力盘点} 的落地——把 6 个论坛/文档工具的用法、坑、绕行路径写成可查的速查。
> 全部基于 `world-quant-brain-mcp/tools_forum.py` / `tools_data.py` 源码 + 本 session 真实调用验证。
> 相关：[[07_field_profile_template_mapping]] §六（论坛经验如何转成模板）。
>
> ⚠ **一处登记在册的例外（写方向）**：本裁定覆盖的是**查**论坛（读方向）。
> **发帖**方向 MCP 侧**没有**对应工具（`create_forum_post` 在 MCP 包内已不存在），
> 故 `tools/forum/forum_post.py` 仍是唯一的发帖实现——它自己用 requests、并从
> `world-quant-brain-mcp/.env` 读凭据。**这是登记在册的例外，不是隐形旁路**：
> 机械闸 `tests/unit/08_forum_recon/test_forum_single_way_gate.py` 的
> `REQUESTS_FORUM_EXCEPTIONS` 把它逐个列出，任何**新增**的 requests 论坛路径即红。
> **退役条件**：MCP 侧补上发帖工具后，本例外与其脚本一并删除（棘轮：例外只能变少，不能变多）。
> ⚠ 该脚本自述「复刻现役 MCP `BrainApiClient.create_forum_post`」——**该说法已过期**
> （MCP 包内已无此方法），见 2026-11-19 审计报告。

## 一、工具清单（都在 `wq-brain-http`，共 6 个）

| 工具 | 入参 | 底层 | 本 session 实测 |
|---|---|---|---|
| **`search_forum_posts_local`** ★唯一检索通道 | `keywords: list[str]`, `limit: int=5`, `max_pages: int=8` | **Zendesk 列表端点 + 本地过滤**（无 Playwright） | 600 帖扫出 24 命中，秒回 |
| **`get_forum_posts`** | `page: int=1`, `per_page: int=100`, `sort_by`, `sort_order` | Zendesk 列表端点 | `count=11296` / `page_count=113` |
| `read_forum_post` | `article_id: str`, `include_comments: bool=True` | **Zendesk SSO + JSON API** | 秒回，拿到全文 |
| `get_glossary_terms` | 无 | Playwright 读术语表页 | 注册正常 |
| `get_documentations` | 无 | BRAIN `/content/api/tutorials` | 秒回，11 个集合 |
| `get_documentation_page` | `page_id: str` | BRAIN content API | 秒回，拿到全文 |

### 1.1 ★★ 为什么旧 Playwright 搜索被判死并退役（2026-11-19 定性 · 11-20 退役）

**问题**：旧 `search_forum_posts` 对任何查询都倾向返回 0 结果或超时，而同期语料里明明有命中。
**根因（源码级）**：`forum_functions._search_forum_posts_impl` 里，等不到选择器 `ul.search-results-list` 时
**只记 warning、显式不设 `navigation_failed`**（原注释：「可能是真的没有结果，也可能是挑战页；不判 nav_failed」）。
⇒ **`total_found=0` + `navigation_failed=false` 是假信号**，它同时表示「真的没有」和「撞了 Cloudflare 挑战页」。
**结论**：2026-11-19 只是把它修成 `navigation_failed=true`（诚实但依然查不到）；2026-11-20 实测
`theme` 一词仍 `navigation_failed=true` + 0 结果（同期 local 通道命中 124 条）⇒ **用户裁定整体退役、代码删除**。

**唯一检索通道（确定性、零超时、零误判）**：Zendesk **列表端点**
`GET https://support.worldquantbrain.com/api/v2/community/posts.json?per_page=100&page=N`
（实测 `count=11296` / `page_count=113`），列表项**自带** `id / title / details 正文 / vote_sum / comment_count / created_at / html_url`。
⇒ **论坛检索 = 拉语料 + 本地过滤**。这正是 `search_forum_posts_local` 做的事。

**关键词匹配口径**：按**词命中率**折算，不做整串子串匹配——
查询 `post earnings announcement drift` 在语料里写作 `post-earnings announcement drift`（带连字符），整串匹配 0 命中（实测）。
标题命中权重 3、正文权重 1，按命中词数占比折算。

**实测命中量（800 帖样本）**：sharpe 378 / turnover 225 / correlation 180 / earnings 61 / crowding 40 / sentiment 38 / PEAD 5。

## 二、论坛工具：用法与坑

### 2.1 `read_forum_post` 的 article_id 格式

源码 `forum_functions.py::_extract_post_id` 用正则 `r'/posts/(\d+)|^(\d+)'` 提取：
- ✅ 接受：纯数字 `"43358755666967"`；含 `/posts/<数字>` 的完整 URL
- ⛔ 拒绝：标题前缀 `"LC97552"`（报错 `Could not extract forum post id from: LC97552`）
- **真实 id 从哪来**：帖子 URL、`docs/` 与 memory 里归档的链接、`get_documentation_page` 正文里的 `<a href=".../posts/<id>-...">`

### 2.2 旧 Playwright 搜索为什么超时（源码级 · 已退役，仅存档）

```
内部总超时 overall_timeout = 120s
浏览器启动 + SSO 握手 = 90s（timeout_seconds*2+30）
单次导航 = 40s × 2 次重试（FORUM_SETTINGS_NAV_TIMEOUT）
但 MCP 客户端层（harness）= 30s  ← 先掐断
```
⇒ **服务端还没跑完，客户端已经超时**。这是传输层超时不匹配，不是"论坛无解"、不是"该机制不存在"。

⚠ **2026-11-20 存档说明**：`FORUM_SETTINGS_NAV_TIMEOUT` 与旧 Playwright 导航层已随 `forum_functions.py`
重写一并退役（现行实现只读 `FORUM_SETTINGS_TIMEOUT`，见 `docs/env_registry.json`）⇒
**该 env 键已不在登记表中，不要再去 `.env` 找它**。上文的 30s 客户端掐断问题**仍然成立**，
但它与 2026-11-20 的三层超时改造（客户端 `timeoutMs` / `API_SETTINGS_TIMEOUT`）是两件事。

**取证纪律**（`forum-paper-evidence-gate`）：检索失败 ⇒ 记工具故障，**不落 `forum_recon_negative_*`**、
不解释成"论坛确认无解"、不据此判死。

### 2.3 检索失败时的绕行路径（已实测跑通）

```
get_documentations → 找相关集合的 page_id
        ↓
get_documentation_page(page_id=...) → 正文里的 <a href=".../posts/<数字>-..."> 含帖子数字 id
        ↓
read_forum_post(article_id="<数字>") → 全文（含 body/comments）
        ↓
归档记忆里也存了大量已知 article_id（freshness-gate-fhp.md / gbr-unlit-tower-exhausted.md 等）
```

**实例**：`get_documentation_page("list-must-read-posts-how-improve-your-alphas-are-submitted")`
返回 7 篇必读帖的数字 id：
- `8123350778391` How to get a higher Sharpe
- `8833033953559` BRAIN TIPS: 5 ways to increase returns
- `8046468280727` BRAIN TIPS: reduce correlation
- `8360363631127` BRAIN TIPS: trade_when for Event/Low-Turnover（降 turnover）
- `8209806533015` How to avoid overfitting
- （另 2 篇是 articles 不是 posts，id 在 `/hc/en-us/articles/` 路径）

这些 id 可直接 `read_forum_post` 直读。

### 2.4 凭据

工具**不收口令参数**——服务端从配置读 `CREDENTIALS_EMAIL` / `CREDENTIALS_PASSWORD`。
Agent 不要试图传邮箱/密码（skill 审查 FB-10/X-15）。

## 三、文档工具：两步用法（已实测）

```
1) get_documentations()  → 11 个集合，每集 {id, title, category, pages:[{id,title,duration,...}]}
2) get_documentation_page(page_id="<page id>")  → {id, title, content:[{type:"TEXT", value:"<html>"}], ...}
```

本 session 实测拿到的高价值 page id（按挖掘常用度）：
- `single-dataset-alphas`（单数据集 ATOM 政策）
- `respapers`（用论文构建 alpha）
- `vector-datafields` / `group-data-fields`（字段类型）
- `neut-cons` / `statistical-risk-neutralized-alphas`（中性化设置）
- `understanding-simulation-limits`（配额限额）
- `how-pass-sub-universe-test`（sub-universe 测试）
- `list-must-read-posts-how-improve-your-alphas-are-submitted`（必读帖链接集合）

⚠ `content[].value` 是 **HTML 字符串**（含 `<style>` / `<p data-block-key>`），读的时候当文本处理即可，
不必渲染——链接在 `<a href="...">` 里，用正则提取数字 id 给 `read_forum_post`。

## 四、文档 vs 论坛的定位（别混）

| | 文档（get_documentations） | 论坛（read_forum_post） |
|---|---|---|
| 性质 | 官方 knowledge，durable | 社区经验，需本区实测 |
| 用法 | **可当权威规则**（如提交测试、字段类型定义、配额） | **只能当假说**——跨区/跨族不可照搬，必须本区验证 |
| 时效 | `lastModified` 明确 | 帖子里给的算子名可能已下线（GHOST 校验 / `get_operators`） |

典型例子：LC97552 新鲜度门帖在 IND 拿到 S1.62/F1.37/2Y2.47（18 项全 PASS 已 OS），
但 GBR/KOR 实测**不可平移**——社区配方是假说，不是规律。

## 五、工具盘点方法（以后别靠记忆）

```bash
python tools/mcp_ping.py --full        # 列出两个服务全部注册工具名 + 连通性
# wq-brain-http 71 个 / wqb-db 49 个（2026-11-17 实测）
```
MCP 工具是活的（会随代码增删），数字/清单以 `tools/list` 为准，不在此文档硬编码总数。
