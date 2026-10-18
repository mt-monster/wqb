# forum_alpha_research/ — 论坛语料取证目录（2026-08-17 一次性）

> **2026-10-10 定位更正**（第三轮输出目录复核，`reports/output_dirs_governance_review3_20261010.md` P3-E）。
> 初版复核记「运行产物与工具脚本混放、大文件未入库」，实测两处都不准，以此节为准。

## 这里是什么

175 帖检索 → 深读 22 篇（含评论）的**原始取证留痕**，结论落在
`output_report/forum_mining_experience_20260913.md`（该文 §11 的语料来源就是本目录）。
7 个文件**全部已入库**（`git ls-files` 实测 7 条，非「未入库」）。

| 文件 | 角色 |
|---|---|
| `search_results.json` / `read_posts.json` | 检索与深读的原始快照（证据） |
| `digest.txt` | 22 篇要点摘录（人读） |
| `alpha_generation_experience_summary.md` | 结论正文 |
| `gather_search_v2.py` / `read_posts.py` / `make_digest.py` | 当时的抓取脚本 |

## ⚠ 3 个 .py 已不可重跑 —— 别照抄

它们硬编码 `MCP_URI = "http://127.0.0.1:8876/mcp"`，而**本仓库的 MCP 是 8000（`wq-brain-http`）
与 8001（`wqb-db`）**，8876 早已不存在（`docs/experience/04_engineering.md` §90 记载过这个错配）。
要重跑论坛取证，走现行链路，别改这个端口：

```
mcp__wq-brain-http__search_forum_posts / read_forum_post     # 平台论坛读取
tools/forum_recon.py 与 tools/forum_recon_wave.py            # 波级默认取证（AGENTS.md §8.11）
brain-forum-browse                                            # 按需调用的知识型 skill
```

## 为什么没按 §8.13 把它们挪进 `tools/`

三条实测理由（2026-10-10 核过，不是「懒」）：

1. **不可重跑** ⇒ 挪进 `tools/` 只会得到一个登记在册却跑不通的工具，反而误导。
2. `tools/legacy/` 是**平铺**目录（0 个子目录），归档一次取证目录要新开子目录风格。
3. 它们是 `forum_mining_experience_20260913.md` 的**配对证据**，与结论同放一处才可追溯；
   `S5_EXEMPT_PREFIXES` 已据此登记豁免（`reports/forum_alpha_research/`）。

若将来要清掉：先确认 `forum_mining_experience_20260913.md` 是否还引用语料路径，
再按 §7「归档而非删除」整体移入 `attic/forum_alpha_research_20260817/`，并同步本文件与
`tools/legacy/README.md` 的登记条目。
