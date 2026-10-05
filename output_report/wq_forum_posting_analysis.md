# WorldQuant BRAIN 论坛「发帖机制」全解析

> 一份基于真实接口抓包 + 300 篇实证样本的技术分析
> 取证时间：2026-10-01（GMT+8）｜样本：最新 300 篇原始帖子 + 已分类语料 142 篇
> 说明：本文所有结论均来自真实调用与真实数据，未做任何写入操作（本环境对论坛为只读）。

---

## 开篇：为什么要拆这件事

我们在做「wq 论坛情报台」时，需要稳定地把论坛当日新帖抓下来做分类和摘要。要做到这一点，就必须搞清楚：**一篇帖子在这个平台上，到底是怎么被"发"出来的**——它走什么域名、过哪几道鉴权、落库后长什么样、归到哪个板块、由谁发、什么时候发、发出去有没有人看。

把这些拆开之后，得到的其实是一份"平台内容生态体检报告"：不仅能指导抓取，也能回答"我该怎么写帖才有人看"。

---

## 一、平台底座：它不是自研论坛，而是 Zendesk Guide 社区

第一层认知很重要：BRAIN 的论坛**不是自研的**。

| 项 | 值 |
|---|---|
| 站点域名 | `https://support.worldquantbrain.com` |
| 底层产品 | Zendesk Guide 的 **Community（社区）** 模块 |
| 品牌 ID | `brand_id=1500000894061` |
| 帖子列表接口 | `/api/v2/community/posts.json` |
| 板块列表接口 | `/api/v2/community/topics.json` |

这意味着**所有 Zendesk 社区 API 的通用约定在这里都成立**：分页字段是 `page / per_page / page_count / next_page`，正文是 HTML，投票/关注/评论是独立子资源。一旦认出这层皮，很多行为的猜测就可以直接换成规范答案。

---

## 二、发帖的技术链路：三跳鉴权，会话复用

想在接口层读到帖子（更不用说发帖），要过三跳：

```
① BRAIN 平台登录  →  拿到 JWT（由 brain_client 自动存入 session）
② Zendesk SSO 跳转 →  GET https://worldquantbrain.zendesk.com/access
                        ?brand_id=1500000894061
                        &locale=zh-cn
                        &return_to=https://support.worldquantbrain.com/hc/zh-cn
③ 复用同一个 requests.Session 直接调 /api/v2/community/... ，带 Accept: application/json
```

实现要点（来自项目内 `forum_functions.py` 的真实代码）：

```python
async def _ensure_support_session(email, password, locale="zh-cn"):
    await brain_client.ensure_authenticated()               # ① BRAIN 登录，JWT 自动入库
    access_url = ("https://worldquantbrain.zendesk.com/access"
                  f"?brand_id=1500000894061&locale={locale}"
                  f"&return_to={base_url}/hc/{locale}")
    response = await asyncio.to_thread(
        lambda: brain_client.session.get(access_url, allow_redirects=True))   # ② SSO
    return brain_client.session                              # ③ 复用同一会话
```

### 两个实测反直觉点

1. **SSO 握手会返回 403，但读接口照样通。**
   我们多次观察到 `Support SSO handshake completed with status=403`，紧接着 `posts.json` 依然返回 200 和完整数据。原因是**社区帖子对已登录用户是公开可读的**，读操作并不严格依赖握手成功。
   ⚠️ 但**写操作一定依赖有效会话**——所以不能用"读得通"来推断"发得出"。

2. **不要自己造 Cookie。**
   会话是从 BRAIN 登录态继承下来的，`brain_client.session` 里已经带着 JWT 和 Zendesk 的票据。自己拼 Cookie 或用一个干净的 `requests.Session()`，会在写操作上直接失败。

---

## 三、一篇帖子在数据层长什么样（21 个字段）

直接抓一篇真实帖子，原始对象是这 21 个键：

```
author_id, closed, comment_count, content_tag_ids, created_at, details,
featured, follower_count, frozen, html_url, id, non_author_editor_id,
non_author_updated_at, pinned, status, title, topic_id, updated_at, url,
vote_count, vote_sum
```

逐个解读，并附上 300 篇样本的实测值：

| 字段 | 含义 | 300 篇实测观察 |
|---|---|---|
| `id` | 帖子 ID（19 位长整型，如 `43841368137239`） | 全局唯一，可拼 `html_url` |
| `title` | 标题 | 平均 **26.4 字**（142 篇语料），属"短标题 + 信息密度高"风格 |
| `details` | **正文，是 HTML 字符串** | 实测为 `<p>` / `<strong>` / `&nbsp;` 标签，抓取需 `re.sub(r"<[^>]+>"," ")` 去标签 |
| `author_id` | 作者 ID（纯数字） | 74 位唯一作者 / 300 篇 |
| `topic_id` | 所属板块 ID | 需另调 `topics.json` 映射成板块名 |
| `created_at` / `updated_at` | 创建 / 更新时间 | **UTC 时间**，做"当日新增"必须自己换算到 GMT+8 |
| `html_url` | 前台可点击链接 | 142/142 篇均为真实 `https` 链接，可直接跳转 |
| `status` | 审核/特殊状态 | **300/300 全是 `'none'`** → 无明显审核态 |
| `pinned` / `featured` | 置顶 / 精选 | 置顶 1 篇，精选 0 篇（**精选位几乎不用**） |
| `frozen` / `closed` | 冻结 / 关闭评论 | frozen 0，**closed 2** |
| `vote_count` / `vote_sum` | 投票人数 / 投票净值 | 见 §八，有异常 |
| `comment_count` | 评论数 | 见 §八，是稀缺信号 |
| `follower_count` | 关注数 | 均值 4.23，最大 27 |
| `content_tag_ids` | 内容标签 ID | 平台侧分类体系（与我们的五分类不是一回事） |
| `non_author_editor_id` / `non_author_updated_at` | **非作者编辑者** | 存在该字段 ⇒ **运营方有编辑他人帖子内容的能力** |

最后一行值得单独说：`non_author_editor_id` 的存在，说明这是个"可被运营介入编辑"的社区，不是完全不可变的 UGC。

---

## 四、帖子发到哪：板块结构（142 篇已分类语料）

| 板块 | 篇数 | 占比 |
|---|---:|---:|
| Advisory Program Discussion Forum - Kunqi | 112 | 78.9% |
| 顾问专属中文论坛 | 19 | 13.4% |
| Global Consultant Community for Staying Ahead | 8 | 5.6% |
| 中文论坛 | 2 | 1.4% |
| Research Papers for Consultants | 1 | 0.7% |

**结论**：这是一个**单极结构**——接近八成的内容涌进 `Kunqi` 这一个板块，其余板块更像是补充渠道。发帖时如果选错板块，曝光量会差一个数量级。

> 板块名不能直接从帖子对象拿到，必须 `GET /api/v2/community/topics.json?per_page=100` 建 `topic_id → name` 映射。抓取时若这步失败，`section` 会退化成"社区"。

---

## 五、谁在发：高度集中的作者生态

300 篇样本：

- **唯一作者 74 位**
- **TOP4 作者贡献 122 篇 = 40.7%**（40 / 37 / 25 / 20 篇）
- 单作者最高 40 篇，占 13.3%

作者一律以**匿名 ID** 呈现（前台显示形如 `WL27618`、`KK37637`、`DA98440` 的代号，接口层是长整型 `author_id`），**看不到真实姓名、等级、历史发帖数**。

**这意味着什么**：内容供给高度依赖少数几位核心贡献者。对读者是好消息（信息密度高）；对平台是风险（单点依赖）。如果你想让自己的帖子被看见，实际上是在和这 4 位高产作者抢同一批注意力。

---

## 六、什么时候发：时段分布（含时区陷阱）

300 篇样本按 `created_at` 的 **UTC 小时**统计 TOP5：

| UTC 小时 | 篇数 | 折算 GMT+8 |
|---|---:|---|
| 13 | 35 | **21:00** |
| 08 | 29 | **16:00** |
| 17 | 25 | 01:00 |
| 02 | 21 | 10:00 |
| 23 | 21 | 07:00 |

换算成北京时间后的图景就很合理了：

- **晚间 21:00 是绝对主窗口**（35 篇）——下班后的集中产出；
- 下午 16:00（29 篇）是次高峰；
- **深夜 01:00（25 篇）这一簇很可疑**，结合 §五 的作者集中度，更像是**定时发布或批量补发**，而非真人熬夜手写。

**实操建议**：
1. 想获得最大曝光，瞄准 **GMT+8 20:00–22:00** 发布；
2. 抓"当日新增"的定时任务，**不要放在凌晨**——那时当天的帖子还没发出来。我们的每日刷新放在 09:00 只能抓到前一天夜里 + 当天清晨的量；若想抓满一整天，应改到 **21:30 之后**。

> ⚠️ 时区陷阱：`created_at` 是 UTC。我们第一版工作台里"今日"判断写成了硬编码日期，且未做时区换算，导致跨天即失效——这类 bug 在做"当日新增"时必须优先排查。

---

## 七、发什么：内容形态分类（142 篇语料，启发式分类）

| 分类 | 篇数 |
|---|---:|
| 问题求助 | 39 |
| 技术讨论 | 38 |
| 经验分享 | 32 |
| 其他 | 21 |
| 公告通知 | 12 |

按日期分布（142 篇）：09-24: 9｜09-25: 21｜**09-26: 50**｜09-27: 24｜09-28: 30｜09-29: 8
——单日 50 篇的尖峰，同样提示存在**批量投放**。

再看**互动 TOP5**，什么内容真的有人看：

| 👍 | 💬 | 标题 |
|---:|---:|---|
| 84 | 12 | 又一个可白嫖的国内 AI 大模型【星辰智能体】 |
| 72 | 0 | 推荐一个免费使用 deepseek v4.1、混元、1.2 倍 GLM5.3… |
| 65 | 15 | 【Python Alpha】复现"傅里叶变换"帖子时我挖出的 4 个坑（附修正版代码） |
| 56 | 17 | 别用随机切分验证 Alpha：一套可落地的时间前推与冻结流程 |
| 57 | 1 | 因子构造日记：alpha 灵感（1）【传奇耐打王系列二】 |

**高互动内容的三种范式**：
1. **免费资源/工具情报**（前两名，84 / 72 赞）——获取成本低的实用情报，传播力最强；
2. **带代码的踩坑复现**（65 赞 + 15 评论）——"我照着做，踩了 4 个坑，附修正版代码"；
3. **可落地的方法论**（56 赞 + **17 评论**）——"别用随机切分"这种有明确观点的纠错型内容，评论转化最高。

注意第 2 名：72 赞但 **0 评论**。资源型内容"叫好不叫座"——点赞高但讨论少；而方法论/纠错型内容评论率显著更高。

---

## 八、互动信号：什么才算真的"被看见"

300 篇样本的三个互动指标：

| 指标 | 均值 | 中位数 | 最大 | 非零占比 |
|---|---:|---:|---:|---:|
| `vote_sum`（投票净值） | 19.56 | 21 | 84 | **100%** |
| `comment_count`（评论） | 1.55 | **0** | 21 | **22%** |
| `follower_count`（关注） | 4.23 | 1 | 27 | — |

这里有一个**必须警惕的数据异常**：

> **`vote_sum` 的非零占比是 100%，中位数 21。**

也就是说，**平台上几乎不存在 0 票的帖子**，且票数基线普遍在 20 上下。这说明投票数**存在基线/膨胀**（可能是默认票、历史累计口径或产品机制），**不适合直接当作"内容质量"信号**——用它排序，等于在用噪声排序。

相反：

- **评论数中位数是 0，只有 22% 的帖子有评论。**
  评论是**稀缺信号**，能拿到 10+ 评论的帖子极少（最大 21）。
  ⇒ **用 `comment_count` 做优先级/质量排序，比 `vote_sum` 可靠得多。**

---

## 九、怎么发：两条路径

### 9.1 人工发帖（日常推荐）

前台进入对应板块 → 新建帖子。适合绝大多数场景，也避免因接口变更导致的失败。

### 9.2 接口发帖（Zendesk 社区 API 规范）

按 Zendesk Community Posts API 的通用规范，创建帖子是：

```
POST /api/v2/community/posts.json
Content-Type: application/json

{
  "post": {
    "topic_id": <板块 ID>,
    "title":   "标题",
    "details": "<p>正文，注意是 <strong>HTML</strong></p>"
  }
}
```

配套动作：

| 动作 | 接口 |
|---|---|
| 取板块列表（拿 `topic_id`） | `GET /api/v2/community/topics.json?per_page=100` |
| 发评论 | `POST /api/v2/community/posts/{id}/comments.json` |
| 投票 | 不同 Zendesk 版本有 `/vote.json` 与 `/votes.json` 两种写法，需按实例实测 |
| 关注 | `/api/v2/community/posts/{id}/subscriptions.json` |

复用已建立的会话即可：

```python
# 仅示意：本环境为只读，以下代码未执行
session = await fc._ensure_support_session(email, password, locale="zh-cn")
r = session.post(
    f"{fc.base_url}/api/v2/community/posts.json",
    json={"post": {"topic_id": topic_id, "title": title, "details": html_body}},
    headers={"Accept": "application/json"},
    timeout=30,
)
```

⚠️ **重要声明**：以上写接口依据 Zendesk 社区 API 规范整理，**本环境未做任何写入实测**。本项目的论坛能力定位为**只读**（读取、分析、摘要），发帖/评论/点赞的贡献流程处于休眠状态。若确需写入，应先在测试板块单条验证，再考虑批量。

### 9.3 三个接口层的坑（都是实测踩过的）

1. **`start_time` 过滤失效**：给 `posts.json` 传 `start_time` 并不能可靠地按时段过滤。正确做法是**服务端放宽窗口拉取，客户端按 GMT+8 日期精筛**。
2. **分页上限**：`per_page` 最大 100，靠 `next_page` / `page_count` 翻页；只翻一页会漏。
3. **正文是 HTML**：直接当纯文本会带一堆 `<p>`、`&nbsp;`，必须先去标签再摘要。

---

## 十、红线与注意事项

- **只读纪律**：本环境不发布、不修改、不刷赞。任何写入动作都应显式确认后再做。
- **不要高频轮询**：单账号单并发，密集请求会触发限流。
- **不要凭据外泄**：凭据从 `.env` 由库内部加载，脚本不得读取或打印口令。
- **403 不代表失败**：SSO 握手 403 时读接口仍可用，但写操作会真的失败。
- **时区必须显式处理**：`created_at` 是 UTC，"当日新增"一律换算到 GMT+8 再判。

---

## 十一、对「论坛情报台」的三条直接启示

1. **抓取窗口必须大于每日增量，且要累积合并。**
   抓取器是"严格模式"（只输出窗口内帖子）。若每天只抓当天，凌晨跑（当天 0 条）会把页面清空。我们最终做成"抓 7 天 + 按 id 累积合并 + 保留 30 天"，并让失败时中止部署、不覆盖线上。
2. **优先级排序要用 `comment_count`，不要用 `vote_sum`。**
   `vote_sum` 100% 非零、基线 ~20，是噪声；评论中位数 0，才是真信号。下一步应在工作台加入"热议榜（按评论数）"。
3. **抓取时机应挪到晚间 21:30 之后。**
   因为 21:00 才是发帖主峰值，早上 09:00 抓会系统性漏掉当天大部分内容。

---

## 附：复现命令

> ⚠ **2026-10-04 更新：下列命令已不可运行。** 本报告的采集链路（论坛工作台）已整端下架
> `attic/forum_workbench_20261004/`：根目录与 `tools/forum_workbench/` 两份同名脚本已内容分叉，
> 且 UI 模板 `wq_workbench.html` 从未入库、全盘丢失（定案记录见 AGENTS.md §8.13）。
> 下面的命令仅作**当时结论的证据留痕**保留，不要再执行。

```bash
# （已下架）抓取近 N 天：复用真实鉴权，只读
world-quant-brain-mcp/.venv/Scripts/python.exe wq_forum_scrape.py --days 7

# （已下架）每日刷新：抓 → 合并 → 重建 → 重导入 → 重发布
python wq_daily_refresh.py --days 7
```

**当前受支持的论坛取数通道**（要重跑本报告的互动字段统计，走这三条之一）：

| 要做的事 | 现役入口 |
|---|---|
| 搜帖 / 读帖含评论 | MCP `mcp__wq-brain-http__search_forum_posts` / `read_forum_post` |
| 按问题驱动检索并落证据 | `tools/forum_recon.py` / `tools/forum_recon_wave.py`（波级取证闸） |
| 逛帖与沉淀笔记 | skill `brain-forum-browse`（只读） |

本报告的两条结论仍然成立且**已被流程吸收**：① 优先级排序用 `comment_count` 不用 `vote_sum`；
② 抓取时机应在 21:30 之后（发帖峰值在 21:00）。

---

*本文数据来自真实接口调用；样本口径已在各章节标注（300 篇原始样本用于作者/互动/时段，142 篇已分类语料用于分类/板块）。*
