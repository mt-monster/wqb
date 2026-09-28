# RA×10 战役回测过程复盘与 skills / workflow 优化清单（2026-09-18 → 09-20）

> 数据来源：`backtest_results` / `expressions` / `alphas` / `submit_ready`（created_at ≥ 2026-09-18），
> 目标：找出**显著提高回测收益（每次回测产出可提交 RA 的概率）**的优化点，按杠杆排序。

## 1. 漏斗（全会话 978 次回测）

| 层 | 数量 | 转化 |
|---|---|---|
| 回测 | 978 | — |
| IS 达标（S≥1.58 & F≥1） | 128 | 13.1% |
| RA-clean（平台 checks 无 FAIL） | 55 | 5.6% |
| 做过 prod 检查 | 31 / 55 | 56%（**24 条 RA-clean 从未测 prod**）|
| prod<0.7 | 14 | 1.4% |
| ACTIVE | 6（+5 条已验证在队列） | 0.6%（+0.5%） |

IS 达标却被 RA 硬闸杀掉的 73 条：**LOW_ROBUST_UNIVERSE_SHARPE 50**、IS_LADDER 20、HIGH_TURNOVER 19、CW 4、SUB_UNIVERSE 4。

## 2. 收益归因：钱花在哪、货从哪来

### 2.1 按表达式来源（决定性）

| 来源 | 回测 | RA-clean | prod<0.7 | ACTIVE |
|---|---|---|---|---|
| **GEM / pipeline 生成**（IND w170–176、JPN w7–13、GBR w62–64、DEU/GLB s2_*） | **558（57%）** | **0** | 0 | 0 |
| **manual（会话内按机制手写的配方组合）** | 312 | **50（16%）** | 13 | **5** |
| probe（单条探针） | 49 | 2 | 1 | 1 |
| win_recipe / mode_a / xr_probe | 59 | 3 | 0 | 0 |

### 2.2 按 region

IND 472 次 → 125 IS 达标 → 52 RA-clean → 14 prod-ok（全部产出）；JPN 214 次 → 0（max|S| 1.24）；GBR 78 / DEU 44 / EUR 39 / USA 22 / KOR 19 / CHN 16 / HKG 6 → 0；GLB 68 → 3 RA-clean（未测 prod）。

### 2.3 IND 按数据集

| 数据集 | 回测 | IS 达标 | RA-clean | prod-ok | 备注 |
|---|---|---|---|---|---|
| intraday_pv_feats | 80 | 53 | 27 | 8 | 主腿 S 4–6.5，裸 prod 0.79–0.92，**慢变量门控后 0.47–0.68** |
| pv103 | 36 | 31 | 16 | 4 | 尾盘反转主腿；裸主腿 1h 内被外部孪生撞 1.0 |
| analyst_consensus | 92 | 41 | 9 | 2 | robust 墙；仅 pretax 水平偏离一种函数形式 prod<0.7 |
| sentiment21 / news_sentiment_transfer / institutions6 / news79 / earnings3 / option30 / earnings11 / news85 / shortinterest5 / pv106 / option1 | **264（56%）** | 0 | 0 | 0 | 全部死于 LOW_ROBUST（信号只在非流动股）/ LOW_SHARPE |

**结论**：全部产出来自一个可复制的配方——「强而撞 prod 墙的主腿 × 慢变量 `trade_when` 门控（季度/月度字段，进 >0.5 出 <0.4 迟滞）」，
外加 `group_rank(bucket)` 修 robust、decay 修换手。GEM 概念优先生成在本会话 **558 次回测零产出**。

## 3. 优化清单（按预期收益排序）

| # | 证据 | 改动点 | 预期 |
|---|---|---|---|
| 1 | manual 16% vs GEM 0% RA-clean | **S2 增加「配方组合引擎」为一等公民**：从 `region_kb` 强信号台账（含 prod≥0.7 的被封主腿）× 慢变量门控字段目录（季/月频、users<10、可跨未点亮塔）确定性组装 `trade_when` 迟滞模板；GEM 只负责"新主腿发现"，预算 ≤1 个 multisim/集 | 回测预算从 57% 零产出转到 16% 产出，10/10 可在 1 天内完成 |
| 2 | 264 次 IND 冷集回测全灭于 LOW_ROBUST；JPN 214 次全灭 | **探针先行硬门**：新数据集/新区域首波 ≤1 个 multisim（≤10 条）单条 sim；max\|S\|<1.2 或 robust/limit<0.5 → 0 波预算；`s0-select` 加入 IND/robust 结构先验（news/sentiment/institutions 类在 IND 结构性撞 robust） | 省 ≥40% 回测 |
| 3 | 24/55 RA-clean 未测 prod；PC 端点每条 95–500s，verify 两次被网络打断 | **收批即异步发 prod 检查**（RA-clean 全部触发，后台轮询回填），并先用 `compute_mutual_correlation` 对 ACTIVE 集本地预杀 self>0.7，再花平台 PC 配额 | 判定时零等待；不再漏候选 |
| 4 | 3 颗新 ACTIVE 把队列 prod 推高 0.02–0.15（3qX3Mp6O 0.49→0.64）；pv103 主腿 1h 被外部孪生 | 队列 `list`/`pick` 加 **ET 配额倒计时 + 家族分散排序**（同日不连提同家族）+ **prod≥0.6 当日必提**规则；提交前 top-N 自动 re-verify | 少丢 1–2 颗/天 |
| 5 | IS 达标里 19 条 HIGH_TURNOVER（IND 限 0.40，主腿本身 0.33–0.39）、20 条 IS_LADDER | wave_gate 加 **区域换手/阶梯预算闸**：主腿 tvr>0.35 的变体必须带 decay 或 ts_mean≥5；家族 robust/limit<0.5 的兄弟不得再进波（`structurally_dead` 已有，接入 build_wave 而非只在 review） | 再省 ~15% |
| 6 | JPN 8/10 multisim 因字段无效 CANCELLED 连坐；三条式二分零信息 | wave_gate 强制 `preflight_expressions`（平台侧字段/语法逐区校验）后才 `create_multi_simulation`；错误批只允许单条 `create_simulation` 二分（已写入 toolkit SKILL，需变成节点硬门） | 每次省 10–60 min |
| 7 | 区域轮换选了 JPN（全塔未亮但无任何信号证据） | `region_rotation` 开区前必跑 `xr-probe`（已有工具）：3 个已验证机制在目标区 max\|S\|<1.0 → probe-only 裁决，不开战役 | 避免 200+ 次零产出 |
| 8 | 未点亮塔主腿全灭，但门控腿可用未点亮塔字段（earnings3 / institutions / news 门控已产出 ACTIVE） | SOP 步 4 明确「**点塔靠门控腿**」：门控字段从未点亮塔目录里选，主腿允许来自已点亮塔（用户 09-19 已允许反向组腿） | 点塔均匀性 |
| 9 | 会话内 MCP 节点挂起（gem / batch_track / upsert_expressions 30 min）、ProxyError 杀轮询、`database is locked` | 节点统一 CLI 后端 + 心跳超时自动降级；DB 连接统一 `wqb.db_conn`（另一会话已在收口） | 稳定性 |
| 10 | 3 个数据质量 bug 直接污染产出率统计 | ① `ra_failed_checks` 49 行双重 JSON 编码（xr-probe / 单条 sim 收批路径）；② `alphas.expression` 516 行被截断到 110 字符（未知采集器）；③ 空 `failed_checks` 存 NULL 与"未采集"不可分 | `get_mining_yield strict` 才可信 |

## 4. 已在本会话落地的相关修复

队列四坑（RA 硬闸 / 加权混腿对齐闸5 / prod 兄弟 / 终态粘性 + 平台实测值保护）、`sync`/`regrade` 子命令、verify 逐条落盘与网络容错、Windows `execv` 与 UTC cutoff bug；
xr-probe（跨区探针）、`prod-first`、`--batch-type probe`、per-item settings、pregate 区域无效字段规则、prod-saturation 需 prod 证据。
