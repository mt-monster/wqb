# news73 字段画像（KOR / D1 / TOP600）

> 快照日：2026-10-30。来源：`mcp__wq-brain-http__get_datafields(dataset=news73)` 全量拉取。
> 定位：NEWS 塔（×1.6，未点亮）里**拥挤度最低**的高分数据集之一（vS 5 / aC 8 / 22 字段，17 个字段 userCount=0 且 alphaCount=0，真正的空白）。

## 1. 数据集级读数

| 项 | 读数 | 判读 |
|---|---|---|
| category | news（multiplier 1.6，塔未点亮） | 高倍率 |
| 字段数 | 22，**全部 VECTOR** | 全部须 `vec_*` 降维 |
| 覆盖率 | 约 **0.269**（全局情绪标量族） | 偏低：只有约 1/4 的股票日有新闻；用户约束 #4 要求近十年有数据 ⇒ **必须逐年核覆盖**，不达标即弃 |
| alphaCount / userCount | 8 / 0（17 个字段为 0/0） | 近乎无人挖，prod 墙风险低 |

## 2. 字段结构（按语义分三组）

**A. 全局情绪标量族（每条新闻一个标量，VECTOR 维数 1 或少数实体）**

| 字段 | 语义 |
|---|---|
| `nws73_sentiment_positive` / `nws73_sentiment_negative` | 正 / 负情绪分 |
| `nws73_sentiment_fear` | 恐惧 |
| `nws73_sentiment_uncertainty` / `nws73_sentiment_certainty` | 不确定 / 确定 |
| `nws73_sentiment_finup` / `nws73_sentiment_findown` | 利好 / 利空（金融专用词表） |
| `nws73_sentiment_finhype` | 炒作热度 |
| `nws73_sentiment_finvolatile` | 波动/不确定性 |

**B. 实体级情绪数组（`*partscr`）**：按新闻中提及的实体逐个打分，需 `vec_avg` / `vec_sum` 后与标的对齐。

**C. 元数据（**禁入信号**）**：`nws73_headlines`（标题文本）、`nws73_entitiescounter`（实体计数，可作门控）、`nws73_djnindustry` / `nws73_djnsubject`（道琼斯行业/主题分类码，**编号无经济序**，只能作 `group_*` 分组键）。

## 3. 六法体检预判

- **更新频率**：事件驱动、日频稀疏；窗口 5 / 22 d。
- **覆盖率 0.269**：`trade_when(<有新闻>, …)` 强制门控；或 `ts_backfill(F, 22)`。
- **中心趋势**：情绪分对称（非单边恒正）⇒ 铁律 A 不适用。
- **形态**：`zero_inflated` 显著。
- **量纲**：各情绪分区间不同（`finvolatile` 可能非有界）⇒ 进 `rank` 前不做跨字段相加。

## 4. A-1 五问

| # | 问 | 答 | ⇒ 骨架 |
|---|---|---|---|
| 1 | 时间维度 | 流量（逐条新闻） | 窗口内聚合 |
| 2 | 相对性 | 排序 | `group_rank(·, sector)` |
| 3 | 被定价的是谁 | **强度**（单条新闻冲击）+ 广度（报道量） | 强度 ⇒ 聚合 + 多窗；广度 ⇒ `ts_sum(1)` 类计数 |
| 4 | 有无博弈 | 否（0 拥挤） | 不上规模壳 |
| 5 | 事件性 | **是**（cov 0.269） | `trade_when` 门控，禁裸 rank |

## 5. A-2 收益来源声明

- **谁**：注意力有限的散户 + 新闻扩散滞后（limited attention; 参见 Da, Engelberg & Gao 2011 JF 的 ASVI 机制：关注度本身驱动短期买压与随后反转）。
- **为什么错**：关注度冲击是**非基本面**的临时买压，1–2 周内均值回复；而**情绪极性**（正面 vs 负面）在盈余公告窗口内延续（Tetlock 2007/2008）。
- **修复期**：关注度 → **5–10 日反转**；情绪极性 → **季度级别漂移**。**两者方向相反，必须分开做，不能相加**。
- **预期方向**：报道强度 ↑ ⇒ 短期跑赢、随后跑输（反转）；情绪净额 ↑ ⇒ 中期跑赢。
- **边界**：无新闻日空仓；`finhype` 极端值需 `tail`。

## 6. 双通道取证

- **通道 A（论坛/本区）**：本区 news 类历史波次 **tone / hotlevel 族全灭**（wave 141/144/157，S<0；news50 最好 0.54）⇒ 论坛通用情绪模板在 KOR 已知无效。**本数据集的 `finup/findown` 对（方向明确的金融词表）与已死 tone 族机制不同**，可用作对照实验。
- **通道 B（文献）**：
  - Da, Engelberg & Gao (2011, JF)：ASVI 关注度 ⇒ 短期买压 + 两周反转（US）。
  - Tetlock (2007, JF) / Tetlock et al. (2008, JF)：媒体悲观 ⇒ 下行 + PEAD（US 大盘）。
  - **文献偏误**：均为 US；KOR 小宇宙 + 散户占比高 ⇒ 关注度机制**可能更强**，但须本区实测。
- **裁决**：A 有反证、B 有机制 ⇒「B 有机制 / A 无表达」档：**自建骨架，但先做 4 条小批对照**（不铺 8 条）。

## 7. 候选方向（待实测）

1. 广度-反转：`-1 * group_rank(ts_sum(vec_avg(nws73_sentiment_finhype), 5), sector)`
2. 情绪净额漂移：`group_rank(ts_mean(subtract(vec_avg(nws73_sentiment_finup), vec_avg(nws73_sentiment_findown)), 22), sector)`（**同源两腿价差，合规**）
3. 不确定性溢价：`group_rank(vec_avg(nws73_sentiment_uncertainty), sector)` 方向正反各测

## 8. 禁碰清单

- `nws73_headlines`（文本）、`nws73_djnindustry` / `nws73_djnsubject`（编号）**不作信号主体**。
- **禁与 PV / MODEL 数据集组腿**（用户约束 #5；PV+NEWS 全库上限 5 条）。
- `news73` 与 `news76` 属同一 category，**同机制只出一条腿**（②.e 一字段一条腿）。
