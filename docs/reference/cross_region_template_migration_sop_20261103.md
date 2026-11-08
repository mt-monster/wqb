# 跨区 NEWS 模板迁移 SOP（2026-11-03 固化 · GBR → CHN/HKG/AMR 实证）

> 用途：把一个区域挖透的模板族，迁到另一个 region 的同 category 下挖 regular alpha。
> 适用：NEWS / SENTIMENT / SOCIALMEDIA 等非 trio category；跨塔组合（trio×非trio）另受 ≤5 额度约束。

## 步 0 · 盘点目标区可用性（别跳过）

```
get_datasets(category=<cat>, region=<R>, delay=1, universe=<config.py 的 REGIONS[R].default_universe>)
```

- ⚠ **universe 传错 ⇒ 静默返回空**（不是没数据）。先查 `src/wqb/config.py` 的 `default_universe`。
- 拿每集的 `fieldCount / userCount / alphaCount / coverage / valueScore` 做初筛。
- ⚠ **低 alphaCount ≠ 有信号**（HKG fund_holdings_panel 前例：uc18/字段级 0–4，信号天花板仍只有 0.56）。但**字段级 aC 低 + coverage 高 + valueScore 高**是必要条件。

## 步 1 · 查目标区既有台账（避免重复烧配额）

- `tracking/<R>/config/cells.json` 的 `dead_ends`（**按字段族判，不是按 category 判**）。
- `tracking/<R>/reference/datasets/*`（KOR news 塔 24 集全清点、DEU news 6 集已做）。
- `tracking/<R>/priors/<r>_priors.json` 的跨区教训。
- `get_pyramid_alphas` 确认目标塔是否已点亮（0/3 才有增量价值）。

## 步 2 · 字段画像 + 语义槽位映射

- 拉 `get_datafields`（**filter_sharpe=false**，否则看不到 OS/IS Sharpe<0 的字段）。
- **按 description 分类，不按字段名**（KOR GROUP 标签陷阱：整数分类码禁包 rank/ts_*）。
- 把目标字段映射到**语义槽位**（见 `news_template_field_semantic_map_20261103.md` 的 12 槽位表）。
- ⚠ **同源镜像字段对（X vs X_storyid / X vs X_uniq）禁止做差** ⇒ 会退化恒 0（CHN C9 实测 S=0.00/TO=0.00）。

## 步 3 · 论坛 + 论文取证（用户硬纪律）

- `search_forum_posts` 取模板骨架与踩坑；`read_forum_post` 取正文与评论（含「原帖没说的边界」）。
- 论坛 `link` 的 base64 blob 解开后取 `posts/(\d+)` 得 article_id（`read_forum_post` 的 article_id 必须是**字符串**）。
- ⚠ 论坛模板的**方向先验不跨区**（nip×returns 在 EUR 出 PPA，CHN 同结构 −1.19）⇒ 方向必须正反各测。

## 步 4 · 模板池 ≥10 个结构互异 + preflight

- 结构差异必须落在**骨架 / 算子几何 / 矩 / 分组轴 / 非线性**，不是换窗口换常数。
- `validate_expressions` 的参数名是 **`alpha_expressions`**，且**必须带 region/universe/delay**（否则默认 USA/TOP3000 误报 unknown_fields）。
- `"gaussian"` 被误报 unknown_fields 是已知误报（命名参数值被当字段）。

## 步 5 · 首波 = 2×N 因子 A/B（设置档 × 壳）★ 不可省

| 因子 | 取值 | 依据 |
|---|---|---|
| 设置档 | 源区出货档（FAST+decay15） vs 目标区既有档 | CHN 实测：FAST 档放大 0.36–0.90，BASE 档把 GBR S1 结构压到 −0.01 |
| 壳 | 带 `ts_target_tvr_decay` vs 裸几何 | 验 target_tvr 是否与目标区自然换手同量级 |

⇒ **单档低 S 不构成判死依据**。

## 步 6 · 方向判决：正向几何读方向，别随手取负

- 先在**正向几何**（`ts_rank`/`ts_zscore`/`ts_max_diff`/`ts_delta`/`ts_av_diff`）上测，读方向。
- 用 `returns` 与 `margin` **是否同号**区分成本伪影 vs 真实暴露：同号 ⇒ 真实暴露（取负可救）；margin 负 returns 正 ⇒ 成本伪影（降换手）。
- 最终负号加在**已验证几何**上，而不是「把 `-ts_rank` 改成 `ts_rank`」（两者经 `group_neutralize` 后不是严格镜像）。

## 步 7 · 增益波（CHN 严闸 2.07 的教训）

- 方向修对后若 S 仍不达严闸 ⇒ 叠增益：**中性化档**（SLOW_AND_FAST / CROWDING / STATISTICAL）× **decay**（15/22/30）× 字段组合。
- 高换手几何（如 `ts_av_diff` TO 28%）必须配高 decay 压换手，否则 margin 吃掉收益。

## 步 8 · 终验四审

1. 五闸（**用目标区的严闸值**，不是源区的）—— 读 `get_alpha_details` 的 `checks.fail` 拿 limit 实际值。
2. `ra.failed_ra_count`（**WARNING 级也算失败**）。
3. prod < 0.7（严格）—— `prod_wait.py --peek` 无锁只读。
4. self < 0.7（严格）—— 先测裸版。

## 步 9 · 复盘回写

- 写 `tracking/<R>/reference/` 战役记录 + 源区台账补章。
- 封存 dead_end 时写「连续空窗 N 年」而非「短历史」（覆盖口径铁律）。
- 沉淀**跨区通用**的方法论到 Agent 记忆；**区域专属**的写进 `tracking/<R>/`。

## 槽位纪律（实测）

- 账号只有 **2 个并发仿真槽**；**跨区并行也受此约束**（HKG 波被 `CONCURRENT_SIMULATION_LIMIT_EXCEEDED` 连续退避到 4/8）。
- ⇒ **同一时刻只让 1–2 波在飞**，其余备好待发；`batch_simulator.py --batch-size 2 --concurrency 2`。
- 一条语法错会 CANCELLED 整批 ⇒ 派发前必过 preflight。

## 参考文件

- 字段语义映射：`docs/reference/news_template_field_semantic_map_20261103.md`
- 模板总结速查：`docs/reference/gbr_news_template_summary_quickref_20261103.md`
- 完整归因：`docs/reference/gbr_news_template_summary_and_cross_region_migration_20261103.md`
- CHN 战役记录：`tracking/CHN/reference/chn_news46_cross_region_campaign_20261103.md`
## ★ 步 5/6/7 修正版（本轮 84 条回测的实测顺序，取代上面的初版）

### 步 5 · 单因子隔离波（12 格，每格只动一项）★ 优先于任何 A/B

| # | 格 | 变动 |
|---|---|---|
| F1 | 基准 | 目标区既有档全套 |
| F2 | 去壳 | `ts_target_tvr_decay` 摘掉 |
| F3 | 去分组轴 | `group_neutralize` 摘掉 |
| F4 | 去壳 + 去组 | 双剥离 |
| F5 | 中性化 → **FAST**（因子型） | ★ 关键格 |
| F6 | FAST + 去壳 | 分离「因子型 × 壳」交互 |
| F7 | 中性化 → STATISTICAL | 因子型复核 |
| F8 | 中性化 → SLOW | 因子型复核 |
| F9 | 中性化 → MARKET（分组型） | 分组型对照 |
| F10 | 分组轴换轴（market→industry） | 换分组轴 |
| F11 | decay 4→22 | decay 档 |
| F12 | target_tvr 0.05→0.15 | 壳的目标换手 |

**为什么优先于 A/B**：本轮先做了「换档 A/B」，看到 FAST 档 |S| 变大便误判为「FAST 是放大器」；
单因子隔离才查出真相是 **因子型中性化在 CHN 制造负漂**，且这个误判直接导致 wave1c/wave1d 沿伪影方向烧了 24 条配额。

### 步 6 · 双极判据（每条候选都配一格镜像）

- 骨架固定为 `±ts_rank(ts_mean(SIG,60),252)`，**只改一个符号**。
- 判据：**S_pos ≈ −S_neg 且 |S| 接近 ⇒ 真信号**；**两极同号 ⇒ 伪影**（转去查设置，别沿负方向取负）。
- 成本 = 1 条回测，**比多跑 10 条同族变体省一个数量级配额**。

### 步 7 · 增益波（当双极确认「真但弱」）

| 杠杆 | 例子 |
|---|---|
| 换窗 | 22/66（短）、120/504（长） |
| 去壳 | 纯 `ts_rank` 无 `ts_target_tvr_decay`（强度↑换手↑） |
| 换中性化族 | 分组型 ↔ 因子型 |
| decay | 4 / 8 / 22 |
| 换归一分母 | `total_words` / `token_count_total` |
| 换测量口径 | unigram vs bigram |
| 乘子字段 | × `rank(relevance)`（论坛已验证的置信乘子套路） |

### 步 5/6/7 的正确顺序（血泪）

```
单因子隔离（找毒档）→ 双极（判真伪）→ 增益波（提强度）
```

❌ 错误顺序（本轮实际踩过）：换档 A/B → 看到 |S| 变大 → 沿负方向取负 → 又烧两波 → 最后才做隔离波。
## ★ 步 7 修正：增益波的第一杠杆是**窗口阶梯**，不是换轴

**实测**（HKG news36，同轴同骨架同档，只换窗口）：

| 杠杆 | S |
|---|---:|
| 换轴（正负归一后取差）60/252 | 0.11（**更差**，正负相消） |
| 同轴 60/252（GBR 强几何惯例） | 0.27 |
| **同轴 22/66（短窗）** | **0.64（↑2.4×）** |

**⇒ 铁律**：**跨区后必须重扫窗口，不能照抄源区窗口**。
GBR 的 `ts_mean(·,60) + ts_rank(·,252)` 是为**事件到达率**（慢变量）设计的；
跨区换到**情绪/语调类**字段后，60/252 会把时效性压没。

**窗口阶梯波模板（12 格）**：

| # | 杠杆 |
|---|---|
| 1-4 | 主轴 × {5/66, 5/126, 22/66, 22/126} |
| 5-8 | 第二轴（净差型）× 同窗口格 |
| 9-10 | 第三轴（时间链型/置信差型）× 22/66 |
| 11 | 主轴 5/66 |
| 12 | 主轴 22/66 + 中性化族对照（STATISTICAL） |

**论坛佐证**：「给信号标保质期」帖把长窗 120 缩到 5 日后信号清晰 —— 「**不是池塘没鱼，是鱼饵保质期不对**」；另一帖「新闻情绪短窗 5–22 有效」。

**优先级**：窗口阶梯波 ≫ 换轴波。理由：窗口是单因子、收益常达 2×+，而换轴可能因正负相消反而变差。