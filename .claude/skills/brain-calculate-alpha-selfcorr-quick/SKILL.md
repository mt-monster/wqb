---
last_verified: 2026-09-29
name: brain-calculate-alpha-selfcorr-quick
description: "本地批量快筛：把自己 UNSUBMITTED 的候选与已提交（OS）alpha 池比对 SELF / PPAC（Power Pool Alpha Correlation）相关性，输出 Excel 汇总；不占平台相关性槽位，不替代平台实测。用户要批量核对一批候选的 self-corr / PPAC、或要 Excel 汇总时使用；单个 alpha 的即时 SELF 用 MCP `check_self_correlation`。"
layer: L4
allowed-tools:
  - Read
  - Bash
---

# Alpha 自相关与 PPAC 相关性计算器

## 职责边界

- **本 skill 负责**：**本地批量**快筛自己候选的 SELF / PPAC（不占平台相关性槽位），产出 Excel 汇总与池新鲜度。
- **本 skill 不做**：**不替代平台实测**——提交前必须实测平台值；不做 PROD（→ `check_correlation`，只读）；不作提交判定；不改 alpha；不发起任何提交。
- **上游 / 下游**：上游 = S4 候选（`wq-brain-alpha-optimization-v1` 或 RA 步 7 产出、已回测）；下游 =（可选）`brain-explain-alphas` → `brain-alpha-robustness` → `tools/submit_verdict.py`。

## 选哪个工具

| | MCP `check_self_correlation` | 本 skill 的 `scripts/skill.py` |
|---|---|---|
| 对象 | **单个** alpha | **一批**（按日期区间 + 区域 + 指标阈值圈定的候选） |
| 速度 / 产物 | 即时；结果进对话 / DB | 批量；Excel（`Alpha Results` + `Meta` 两个 sheet） |
| SELF 口径 | `correlation_type='self'` = 不含 Power Pool 的 OS 池；`powerpool` = 仅 Power Pool；与平台口径对齐 | 同一口径（SelfCorr 池 / PPAC 池分开算） |
| 共同盲区 | **本地池看不见近期提交的孪生体**（见下） | 同左 |

触发词只限「本地快筛 SELF / PPAC」；泛泛的「相关性」问题先看 `check_correlation`（PROD）与 RA 的 prod 总纲，不要落到本 skill。

## SELF 与 PROD 是两个池，别推导

- **SELF** = 与**自己已提交** alpha 的 PnL 相关；**PROD** = 与**平台生产池**的相关。两个池、两个检查、两条取值路径。
- 所以「本地 SELF > 0.7」只能推出「SELF 已必然 FAIL」（任一检查 FAIL 即整体 FAIL，因而不必再花平台队列去查 PROD），**推不出「PROD 也 > 0.7」**。
- 平台的 SELF 判据还有第二条通过路径（新 alpha Sharpe 比被相关者高 10%）——本库（`wqb.config.GATES_PLATFORM['self_corr_max']` = 0.70、`submit_queue.LIM['self']` = 0.7）按**单阈值**处理，**未实现**该豁免；详见 `brain-how-to-pass-alpha-test` §6a。

## ★★ 已知结构性盲区（2026-09-11 实证，务必先读）

**本地 SELF 基于 OS（样本外）PnL 池；刚提交的 alpha 尚无 OS PnL，不在池中 → 对「近期提交的孪生体」结构性失明，给出严重低估的假阴性。**

实证：`vRkAO9Xd` 本地 `check_self_correlation` = **0.229**，平台提交实测 `SELF_CORRELATION` = **0.8392**（差 0.61）；当日新 ACTIVE 的 `blRaArVZ` 与其近孪生，本地池看不见它。（出处：`world-quant-brain-mcp/brain_mixin_correlation.py` `get_self_correlation` docstring：「OS alpha PnL is considered static and cached on disk; only newly-submitted OS alphas are downloaded」。）

**三条使用规则**

1. 本地值**高**（> 0.7）→ 可信，可据此否决候选（保守方向安全），台账记因。
2. 本地值**低** ≠ 平台会低。候选的同族 / 孪生体**近期提交过** → 本地值不可信，只能当下界。
3. **同族连测不要依赖本地 SELF 判活。** 平台 SELF 值目前只在**提交响应**里（`POST /submit`，通过即真提交）——**没有零成本的只读途径**：`workflow_submit_alpha(confirm_submit=False)` 只做**本地放宽预检**（不含平台 SELF / PROD 值），`GET /alphas/{id}/submit` 恒 404。所以：先按本地 SELF + `compute_mutual_correlation` + prod 读数给同族排序，**只在用户明确授权提交时**由平台给出 SELF——对 `submit_verdict == SUBMITTABLE` 的候选按优劣序逐个提交，最先通过的那颗就是真提交（这是提交，不是探测）。提交侧的 API 行为（POST 三态 / PENDING ≠ FAIL / 配额 403 与候选 403 的区分）见 [`worldquant-submit-alpha`](../worldquant-submit-alpha/SKILL.md) 与 [`submit-chain.md`](../worldquant-submit-alpha/references/submit-chain.md)，本页不复写。

**自动提示**：脚本会在输出里给出 OS PnL 池的最后刷新时间与池内 alpha 数（Excel `Meta` sheet + 终端），并在本批本地 SELF 最大值 < 0.7 时**自动打印盲区警告**——低值最需要提醒。
> 未验证（needs-platform）：平台是否提供只读的 `GET /alphas/{id}/correlations/self` 可直接拿平台 SELF；本项目的 MCP 工具从未调用它。确认前不要把它写进任何流程。

## 判读决策表

| 情形 | 判定 | 动作 |
|---|---|---|
| 同族 5 个孪生体，其中 `blRaArVZ` 昨日提交；本地 SELF = 0.23 | **不采信**（盲区） | 提交前平台实测（授权后提交流程）；台账注明「本地值不可信：同族近期提交」 |
| 本地 SELF = 0.81 | **直接否决**（保守方向安全） | 台账记因；不再花平台队列 |
| 本地 SELF = 0.40 且同族近期无提交 | 可信度中等 | 可继续下游链；提交前仍须平台实测 |

## 工具脚本

**被测对象是谁**：脚本没有 `alpha_id` 入参。它取**你自己 `UNSUBMITTED` / `IS_FAIL` 状态**的 alpha（非 SUPER、非隐藏），按 `--start-date` ~ `--end-date`（`MM-DD`，年份取**当年**，按美东时间的创建日期）、`--region`、`--sharpe-threshold` / `--fitness-threshold` 圈定；只有「平台 `is.checks` 无 FAIL 且 long+short > 100」的（`Check OK`）才进入计算；对比池是你的**已提交（OS）alpha**。要测某几个具体 alpha，就把日期区间收窄到它们的创建日。

```bash
# 依赖（一次性；缺依赖时脚本在非交互环境只打印这条命令，不会自己安装）
$WQ_PY -m pip install -r Claude/skills/brain-calculate-alpha-selfcorr-quick/scripts/requirements.txt
# 运行（凭据在进程环境变量里：CREDENTIALS_EMAIL / CREDENTIALS_PASSWORD；不要写进命令行）
$WQ_PY Claude/skills/brain-calculate-alpha-selfcorr-quick/scripts/skill.py --start-date 09-28 --end-date 09-29 --region KOR
```

- **凭据**：只读进程环境变量 `CREDENTIALS_EMAIL` / `CREDENTIALS_PASSWORD`（旧别名 `BRAIN_USERNAME` / `BRAIN_PASSWORD` 仍认）。命令行口令参数仍兼容但**不要用**（进进程列表与 shell 历史，使用时会告警）。
- **产物目录**（固定，不随 CWD）：`$WQ_SELFCORR_OUT_DIR`，缺省 `data/selfcorr_quick/`（已 gitignore）。里面有 OS PnL 池缓存（`os_alpha_ids.pickle` / `os_alpha_pnls.pickle` / `ppac_alpha_ids.pickle`）与 Excel。`--out-dir` 可改。
- **预期输出列**：`alpha_id` / `exp` / `check_status`（`Check OK`＝平台检查无 FAIL 且 long+short>100；**不是**相关性结论）/ `Rank`（按 Sharpe）/ `sharpe` / `self_correlation` / `ppac_correlation` / `turnover` / `fitness` / `margin` / `dateCreated` / `longCount` / `shortCount` / `decay` / `neutralization`；`Meta` sheet 有池最后刷新时间与池大小。
- 参数详情与默认值见 [reference.md](reference.md)。

## 衔接协议

- **上游**：`wq-brain-alpha-optimization-v1`（Mode B / A 产出的候选）或 RA 步 7。
- **本 skill 角色**：S4 链的本地快筛——快于平台查询；SELF > 0.7 可据此否决（SELF 已必然 FAIL，无需再花平台队列查 PROD）。
- **下游**：`brain-explain-alphas`（可选，收益来源归因）→ **`brain-alpha-robustness`**（过拟合 / 稳健性必经闸）→ `tools/submit_verdict.py`。`brain-alpha-judge` 只是可选参考评审。
