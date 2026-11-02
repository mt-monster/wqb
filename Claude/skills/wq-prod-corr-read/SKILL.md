---
name: wq-prod-corr-read
layer: L-RA
description: 读候选 alpha 的生产池相关性（prod / PC）时使用：平台 prod 计算 >120s 超时、超时不落缓存、超时后本机 inflight 标记残留 300s、账号级单并发槽被跨会话抢占、is.prodCorrelation 只对已提交 alpha 存在——这五类故障的处置顺序与判据；含「族代表预判」（量产前先只测一颗决定整族去留）与从免费到昂贵的 prod 时隙排队顺序。不负责降 prod 杠杆（走 wq-prod-lever-self-lock-guard），不做提交动作（走 worldquant-submit-alpha）。
last_verified: 2026-11-02
---

# prod 取数：五条故障与三段式顺序

## 职责边界

- **本 skill 负责**：怎么**拿到**一个候选的 prod 值、拿不到时怎么判、值到手后按什么线判死。
- **本 skill 不做**：拿到 prod 之后**怎么降**（换字段 / hump / decay / 中性化）→ [`wq-prod-lever-self-lock-guard`](../wq-prod-lever-self-lock-guard/SKILL.md)、决策表 D0-P、[`wq-window-valley-break-prod-wall`](../wq-window-valley-break-prod-wall/SKILL.md)；要不要提交、怎么提交 → [`worldquant-submit-alpha`](../worldquant-submit-alpha/SKILL.md)；self / 互相关（self 用 `check_self_correlation`、同批互测用 `compute_mutual_correlation`，均纯本地不占槽）。
- **上游 / 下游**：上游 = 已过 IS 全闸、待终验 prod 的候选（来自区域 RA 战役）；下游 = 用户确认后由 `workflow_submit_alpha` 提交，或交回 `wq-prod-lever-self-lock-guard` 降 prod。

## 一、为什么会需要这一页

prod 是**唯一一个「读」也会失败**的平台指标：它不在回测结果里，要单独触发平台重算；重算走**账号级单并发**槽；MCP 客户端又有 120s 硬上限。三者叠加的结果是「明明候选都齐了，最后一道闸永远拿不到数」。

五条故障是**互相独立**的，任何一条都会让「再试一次」变成白等。

## 二、五条故障（2026-10-29 实测，全部踩过）

| # | 故障 | 现象 | 对策 |
|---:|---|---|---|
| **1** | **`is.prodCorrelation` 只对已提交 alpha 存在** | 未提交候选在 `get_alpha_details` / `batch_get_alpha_metrics` 里一律 `null`；已提交的（`ACTIVE`）才有值 | 别把 `batch_get_alpha_metrics` 当 prod 来源——它只可靠地给 `investability_ratio`。未提交候选**只能**走平台相关性端点 |
| **2** | **真实计算 > 120s，且超时不落缓存** | 报 `timed out after 120000ms`；下一次调用**仍是完整 120s 阻塞**（不是秒回，说明没写缓存） | 一次只回源一颗；把超时当「稍后再来」，不要连着重试 |
| **3** | **平台 prod 是账号级单并发，会被跨会话 / 跨区域抢占** | `status=correlation_busy`、`retry_after=240`、`holder=corr:get_production_correlation(<别的 alpha id>)`。实测 holder 是**另一个区域**的 alpha（EUR），属并行会话产物 | 按 `retry_after` 隔时重查；`inflight=true` 时**绝不重新触发**（重复触发只会把自己顶成 busy） |
| **4** | **本地锁状态 ≠ 平台状态** | `logs/_dblock/correlation.lock.json` 显示 `free`，MCP 仍报 busy | 两套锁不互通：本地锁只防**本机**并发，平台槽归平台管。判 busy 只认平台返回的 `holder` |
| **5** | **传输超时后本机 `inflight` 标记残留在位 300s**（2026-10-29 实测） | 首次调用跨过 MCP 的 120s 上限（`MCP tool invocation did not complete`）后，同一 alpha 的后续调用一律秒回 `inflight=true / retry_after 25 / holder=null`，**不会重新触发计算**，`alpha_corr_cache` 也无新行 | 该标记 TTL = `max(300, wait_s+60)` 秒。超时后**先等满 300s 再来一次**；期内重发只会读到标记（不占槽也不出值）。判"到底算没算"只认 `alpha_corr_cache` 有没有新行，别看调用返回 |

## 三、取数三段式（顺序不可倒）

| 段 | 动作 | 成本 | 判读 |
|---:|---|---|---|
| ① | MCP `check_correlation(alpha_id)`，**缺省 `refresh=False`** | 零平台成本；命中 `alpha_corr_cache`（48h 权威缓存）即秒回 | 有值且 `corr_stale=false` ⇒ 可作**排序**依据；但**放行**要终验 |
| ② | 无锁端点 `GET /alphas/{id}/correlations/prod`（`tools/prod_wait.py --peek`） | 零队列，读平台已算好的值 | **空体 = 排队中，不是 0，也不是低相关**；连续多次空体说明槽被别人占着 |
| ③ | 才 `check_correlation(alpha_id, refresh=True)` | 占账号级单并发槽，可能 >120s | **一批只回源一颗**，串行；只用于**交付前终验** |

**不要并发跑第 ③ 段。** 并发不会更快：请求会互相排队，还会把整轮平台读打成 429——429 之后 `get_alpha_yearly_stats` / `get_alpha_details` / `check_correlation` 全部返回空或错误，连带打死本来正常的工作（实测代价：一整轮稳健性审计报废）。

**超时 ≠ 失败**：MCP 的 120s 上限 **小于**平台 1–5 分钟计算，「第一次就超时」是常态而非异常。超时后 300s 内所有同名调用都会被故障 5 的标记挡回（`inflight=true`、不重算、不出值）——等满 TTL 再来一次；判断"到底算没算"只认 `alpha_corr_cache` 有没有新行。若这个值**不是马上要提交的那颗**，就别再回源（见 §四末条）。

## 四、判据

- **放行线 `prod < 0.70`，严格不等**；`= 0.70` 不放行。**没有任何豁免入口**（`allow_prod_above_07` 已按用户判定移除，任何路径传它都会报错）。
- **缓存保鲜 48h**：`corr_age_hours > 48` 或 `corr_stale=true` 的值**只能排序、不能放行**。prod 池每天有人提交同族 alpha，PC 只向上漂。
- **拿到 `busy` / `pending` 不等于通过**，也不等于失败——它是「无结论」。无结论**不得**写进台账当读数。
- 终验只测**马上就要提交的那一颗**。测完不提交的，48h 后作废，等于白占槽。

### ★★★ 四·1 族代表预判：量产之前先只测 1 颗（2026-10-30 两次实证）

**prod 卡墙的层级是「族」，不是「单颗」。** 只要一个数据集/信号族在生产池里拥挤，同族每一颗都会撞同一面墙；逐颗去测等于把最贵的资源花在最先能判死的地方。

**做法**：某族准备量产（≥3 颗）之前，先只挑 **1 颗「族代表」**（该族最强、骨架最典型的那颗）测 prod，按下面三档决定要不要继续：

| 族代表 prod | 结论 | 后续动作 |
|---|---|---|
| **> 0.80** | 墙在族层面 | **整族降到最低优先级**：既有候选留档，不再为该族花任何 prod 时隙；量产计划直接取消 |
| 0.70–0.80（灰区） | 余量薄 | 同族**最多再测 2 颗**；全部 > 0.70 ⇒ 整族封盘，别逐颗试到第 N 颗 |
| < 0.70 | 族干净 | 才值得量产；量产出的每颗仍须各自终验 |

**实证 1（2026-10-30 USA `shortinterest3`）**：`kqNRbvJP`（卖空费率 main 方差 · W22 · sector · d252）S **1.82** / F **2.04** / 2Y **2.43** / SUB **0.91** / `investability_ratio` 0.9011 / `failed_ra_count` **0**，**self 组内 0.6012 全部通过** —— 指标面上是完美的候选。但平台 **prod = 0.8463 → 直接 BLOCKED**。同族 `Xg9qjVOz`（费率跨度方差）/ `gJezNxjg`（费率 main 方差）大概率撞同一面墙，**不必逐颗花 90–240s 去验**。

**实证 2（2026-10-30 GBR `techindi_model`）**：`tm_16` + `tm_17` 族 **19+ 条 prod 全落在 0.7343–1.0**，而同族自家的 self 只有 0.0238。族内每一颗都独立撞墙、数值几乎一致 ⇒ 这是族级饱和，不是单颗问题。

⇒ ★ **两条可直接用的推论**：
1. **「self 干净」永远不能证明「prod 干净」**：self 只回答「撞不撞自家已提交池」，prod 才回答「撞不撞整个生产池」。两者是**两个不同的问题**，必须两端都测（机理见 [`wq-prod-lever-self-lock-guard`](../wq-prod-lever-self-lock-guard/SKILL.md)）。
2. **族代表的选择标准是「最强 + 最典型」**，不是「最容易过」。挑一颗弱候选测出来 0.62 会给出错误的「族干净」结论。

### ★★★ 四·2 prod 时隙的排队顺序（从免费到昂贵，不许跳层）

| 层 | 工具 | 平台成本 | 用法 |
|---:|---|---|---|
| **1** | `compute_mutual_correlation` / `check_self_correlation` | **零**（纯本地算 PnL 相关） | **可无限跑**。先用它把同族近亲、已提交占位剔干净 |
| **2** | `check_correlation(alpha_id)`（`refresh=False`） | 零（命中 48h 权威缓存） | 对第 1 层活下来的候选批量读；无缓存时自动回源但**不强制** |
| **3** | `check_correlation(alpha_id, refresh=True)` | **占账号级单并发槽，单颗 90–240s，超时率高** | **只对「已经决定要提交的那一颗」** |

**默认顺序**：N 颗候选 → 全量跑第 1 层 → 剩 k 颗跑第 2 层 → **只对最终要提交的 1 颗**跑第 3 层。

**禁止**把第 3 层当**筛选器**（"我先测 10 颗看看哪颗低"）。它是**终验**，不是排序工具。第 1、2 层免费且能回答 80% 的问题；第 3 层一次只服务一颗。

## 五、反模式

| 反模式 | 为什么错 |
|---|---|
| 把 `refresh=True` 当批量读接口 | 每颗占一次单并发槽 + 每次可能 120s；4 颗就够把队列排到自己后面 |
| 看到 `busy` 就重新触发 | `inflight=true` 时重复触发 = 把自己顶成 busy，队列永远轮不到自己 |
| 拿 `--peek` 的「空体」当「低相关」 | 空体是排队中。据此提交等于跳过闸 |
| 用上一轮会话 / 别的区域的 prod 读数 | 单并发槽被抢占时拿到的是别人的场景；且 prod 池天天漂 |
| 未提交候选去 `batch_get_alpha_metrics` 要 prod | 恒 `null`（故障 1），会误判成「平台没数据」 |
| 认为本地锁 free 就该能拿到 | 故障 4：两套锁不互通 |
| **逐颗量产同族候选，再逐颗测 prod** | 把最贵的资源（单并发槽 / 90–240s / 高超时率）花在最先能判死的地方。族代表一颗 0.84 就该停整族（§四·1） |
| **拿「self 全过」当「可以提交」** | self 与 prod 回答两个不同问题。`kqNRbvJP` self 0.6012 全过 / prod 0.8463 BLOCKED 是实测反例 |
| 把 `refresh=True` 当筛选器批量跑 | 它是终验层。免费的第 1、2 层能回答 80% 的问题（§四·2） |

## 六、与其他页面的分工

- 机制与端点细节 → [`wq-brain-ra-pipeline`](../wq-brain-ra-pipeline/SKILL.md) 步 5b-3（故障表来源）与 [`references/prod-corr-avoidance.md`](../wq-brain-ra-pipeline/references/prod-corr-avoidance.md)
- 撞墙后的处置阈值 → 决策表 D0-P（[`references/decision-table.md`](../wq-brain-ra-pipeline/references/decision-table.md)）
- 区域落地（USA）→ [`wq-brain-ra-usa/rules/gate-and-submit-discipline.md`](../wq-brain-ra-usa/rules/gate-and-submit-discipline.md) §十
- 机制性结论 → [`docs/experience/01_platform_gates.md`](docs/experience/01_platform_gates.md) §4
