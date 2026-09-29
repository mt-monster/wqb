# forum_recon 触发表（全流水线唯一一张）

> 旧文里同一个工具有 5 个触发点，分散在步 1 / 4 / 5 / 7 / 9，`--out` 目标各不相同，而步 1 又写着「论坛默认不查」——这句话把其余四处架空了。
> 现统一为本表：**不在本表内的场合不查论坛**（选区已有 registry / yield 先验，论坛检索是 token 黑洞）；在表内的场合按本表做。
> 工具：`tools/forum_recon.py`（问题驱动的**只读**检索；`brain-forum-browse` 的 recon 模式经它执行，免贡献义务）；节点等价入口 `workflow_execute(node="forum_recon")`。
> **需要论坛 / 平台可达**——本环境无凭据或出口被拦时会失败，此时按各行「取不到时」处理，不得当作 `found=false`。

## 触发点

| # | 步 | 触发条件（**怎么发现**该查了） | 问题模板 | `--out` | 命中后 | 取不到时 |
|---|---|---|---|---|---|---|
| 1 | 步 1 | **判死区复开评估**：某区被 `frozen` / 停止规则 A · B2 停下后，有人（用户或 agent）想复开——判据是「有翻案线索吗」，不是「想再试试」 | `"<REGION> <被判死的数据集/族> 有无翻案线索"` | `ledger` | 线索写入 `forum_recon_<qkey>`，供复开评估读；**不改变** `entry_verdict`（那只能按该区 profile 的后门走） | 维持判死 |
| 2 | 步 4 | **机制枯竭 / 同质化**：GEM 产出触每骨架封顶（`WQB_GEM_MAX_PER_SKELETON`，缺省 12），或 win 配方**无腿可换** | `"<数据集/机制> 换腿骨架 / 论坛验证模板"` | `kb` | 合入 `KB/community_tpl_kb.forum_recon_entries[]`；模板**先过 `ghost_operator_advisory`** 替换幽灵算子，再重跑 GEM | 缩窄数据集 / 换集，**不手写表达式** |
| 3 | 步 5 | **闸 6（批级多样性）FAIL 且 `KB/community_tpl_kb` 按 category 检索无货** | `"<category> 骨架 / 换腿参考"` | `kb` | 同 2，回步 4 补骨架 | 拆回单集组合，不停挖 |
| 4 | 步 7 | **卡闸找武器**：Mode B 常规改进 2–3 轮仍卡墙（prod / 2Y / CW / tvr / robust）且未到判死 | `"<墙名+数据集> 破墙配方"`，`--context region=$REGION,dataset=$DS,wall=<WALL>` | `ledger` | 命中的配方 / 手法入 idea 池供 Mode B Step B3；写 `forum_recon_<qkey>` 留痕。**每波 ≤ 1 次** | 继续 Mode B / 转判死流程 |
| 5 | 步 9 | **判死前软核对**（含 D0-P 的 prod 墙判死分支） | `"<数据集/信号族> 有无解法"`，`--context region=$REGION,dataset=$DS,family=<族>` | `negative` | `found=false`（退出码 2；负结果已入 `forum_recon_negative_<qkey>`）= 论坛无解的取证，可判死；`found=true` → 该帖配方转 salvage / Mode B 武器，**不得直接判死** | 核对结果记入 `dead_end.payload.forum_recon`；软提示：无记录不拦写入，但缺失须在 key_findings 说明 |

## 额度与缓存（所有触发点共用）

- **额度以查出有效文章为标准**，不设小硬顶：`--limit` = 目标有效文章数（缺省 3，命中即收束）；搜不到有效文章就扩关键词变体继续搜，直到 `--max-search-rounds`（缺省 8；**防失控安全上限**，不是额度）。
- **有效文章** = 标题不含「公告 / 直播 / 签到 / 问卷 / 获奖 / 名单公示」，正文 ≥ 200 字，且前 2000 字内含可操作标记之一（实测 / 指标 / sharpe / fitness / 表达式 / 字段 / 算子 / 配方 / 换手 / turnover / 稳健 / prod / 相关性 / 中性化 / 破墙 / 回测 / 因子 …，以 `tools/forum_recon.py` 的 `ACTION_MARKERS` 为准）。
- **缓存 7 天**（`tracking/FORUM/forum_recon_cache.json`）：同一问题（`qkey`）7 天内命中缓存不重复 live 查。触发点 4 的「每波 ≤ 1 次」是防 token 黑洞的操作约定，在缓存之上。
- 每条有效文章带：post_id / 标题 / 赞数 / 摘录 / 适用边界（context）/ 幽灵算子标注。
- **退出码**：0 = 有产出；2 = 无解（负结果已入库）；1 = 工具异常。`--dry-run` 只输出检索计划（关键词包 + 缓存状态），零网络零写库。
- 产出**必入库**（含负结果）：`found=true` 按 `--out` 落 `KB/community_tpl_kb` 或 `<region>/forum_recon_<qkey>`；`found=false` 一律落 `forum_recon_negative_<qkey>`（负结果也是判死证据）。键契约见 `docs/ledger_keys.json`。

## 与 `brain-forum-browse` 的分工

`brain-forum-browse` 是**逛论坛**的 skill（有写工具时按 gap 驱动贡献）；recon 是它的一个模式，**只读、问题驱动、无贡献义务**。流水线里只用 recon，不触发逛论坛流程；论坛帖里的表达式**默认未实证**（先过幽灵算子与闸 5，再进 prod-first），不得当作 win 直接回写。
