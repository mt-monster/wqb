# PPA 历史实证（RA 侧只留 ppa-mining 里没有的部分）

> 2026-09-29（skills 审查 RA-126）：本文旧版 312 行，其中 **39 / 52 段与 [`wq-brain-ppa-mining/SKILL.md`](../../wq-brain-ppa-mining/SKILL.md) 逐字相同**（WebDataScope 三面板、§1.0 体检三硬门槛、徽章、字段 10 指标、白空间、模拟 payload、V9 范式、区域结论、API 要点）。两份各改各的已经分叉：闸门章节、工具计数、体检脚本路径、提交语义都只在一边被修过。
> **方法论只有一个家：`wq-brain-ppa-mining`**；PPA 与 RA 逐步差异见 [`ppa-vs-ra.md`](ppa-vs-ra.md)。本文只保留 ppa-mining 里没有、且仍成立的实证（带日期与范围），以及被作废旧说法的去向。

## 1. 仍成立、ppa-mining 里没有的实证

### 1.1 CONCENTRATED_WEIGHT 的根因之一：低频字段覆盖不足（2026-08-11，GBR / TOP700 / D1）

- **症状**：季度更新字段（如 `ep_yield`）上的单输出 `rank(add(...))` 结构 CW 必 FAIL。
- **根因**：字段某些交易日覆盖不足 → `rank` 后权重集中在少数股票。
- **解法（仍有效的部分）**：`ts_backfill(字段, 66)`（季度）或 `ts_backfill(字段, 125)`（半年）先填缺失，再做变化量 / 排名。6 个 backfill 候选 `ra_failed:false`（含 CW PASS），其中 1 颗提交 ACTIVE（Sharpe 1.80 / 2Y 1.82）。
- **不再有效的部分**：当年配合使用的「`add(multiply(rank(A),w1), multiply(rank(B),w2))` 线性加权结构」——加权混合自 2026-09-13 起全局禁止（闸 5 拦），**不得照抄**。CW 的现行治法（时间平滑；参数层无效）见 [`brain-how-to-pass-alpha-test` §4](../../brain-how-to-pass-alpha-test/SKILL.md)。

### 1.2 「正交性—达标性」死结（2026-08，GBR）

- 平台在提交时**实时**查与 OS 池的相关性。同一数据集、同一主腿的兄弟表达式互相关 0.82–1.0：**第二个起全部被拒**，不要对同主腿变体抱幻想。
- 要凑 3 个 PPA：必须**跨数据集 / 跨主腿**找正交信号；每个候选提交前先 `mcp__wq-brain-http__compute_mutual_correlation` 对已提交池验证 < 0.7。
- 常见陷阱：正交的主腿往往 2Y 不达标（starmine fy2 / ARM：2Y 0.12–1.23），news 被 INDUSTRY 中性化吃掉，唯一正交且 2Y 强的 returns 结构卡 CW——**正交性与达标性常常互斥**，需要数据源本身有独立强信号。
- 同一现象在 IND 的证据（同主腿不同慢门控之间 0.46 可并存；同门控换阈值 / 窗口的兄弟 > 0.9）见 [`regions/IND.md`](regions/IND.md)。

### 1.3 GBR 数据集事实（2026-08-11）

| 类别 | 数据集 | 说明 |
|---|---|---|
| 覆盖率 0% | `option1` / `macro27` / `earnings_sent_matrix` / `techindi_model` / `news81` | GBR 根本不提供，**不是字段问题**——勿浪费配额 |
| 结构性弱 | `news18`（覆盖 71–97%，INDUSTRY 中性化下 Sharpe < 0.7 被中和）、`institutions6`（覆盖 100%，INDUSTRY 下信号消失）、`insider_agg_matrix`（换手 ≈ 1.6 结构性爆炸） | 换中性化档位前先看 [`regions/GBR.md`](regions/GBR.md) |
| 唯一可用金矿 | `predictive_starmine`（model 类别 1.9×、94% 覆盖） | 已 PROD 饱和，见 GBR profile 的 `GBR-PROD-SATURATED` |

## 2. 已作废的旧说法（读到就不要照做）

| 旧说法（本文旧版 / ppa-mining 里可能仍留有） | 为什么作废 | 现在看哪里 |
|---|---|---|
| 「`GET /alphas/{id}/submit` → 200 = 最终成功 / 403 = 拒绝」，并附「用底层 client 先 POST 再 GET 判定」的脚本 | GET 提交视图对全部候选恒 404（实测），不能证明可提交；而 POST 是**不可撤销的真实提交**——把它写成「判定脚本」等于教人绕过用户确认 | [`AGENTS.md`](../../../../AGENTS.md) 提交链一节；[`worldquant-submit-alpha`](../../worldquant-submit-alpha/SKILL.md) |
| 「唯一可靠验证 = alpha 出现在 OS 池」当作提交前判据 | 那是**提交后**的确认，不是放行依据 | 同上 |
| 「并发上限 C=5」 | 2026-08-25 起 Token-Bucket C≈7 | [`wqb-concurrency`](../../wqb-concurrency/SKILL.md) |
| 体检脚本在 `wq-brain-ra-pipeline/scripts/dataset_health_check.py` / `tools/eur_field_coverage.py` | 前者不存在；体检脚本随 ppa-mining 分发，RA 的步 2 用 `score_datasets.py` + `campaign_intel.py s0-select` | [`step2-s0.md`](step2-s0.md)；`wq-brain-ppa-mining/scripts/dataset_health_check.py`（兜底） |
| 「本文件吸收了原 ppa-mining；禁止再把它当独立 Skill 触发」 | ppa-mining 仍是独立 skill（方法论层，不编排、不提交） | [`ppa-vs-ra.md`](ppa-vs-ra.md) |
| 「廉价闸 / 硬闸」数字的第三份复写（Sharpe ≥ 1.58 … PROD < 0.70） | 阈值只在 `config.GATES` / `PLATFORM_CHECK_LINES` 一处定义，文档复写会过期 | [`decision-table.md`](decision-table.md) 与 INDEX「闸门阶梯」 |
