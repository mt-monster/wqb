# judge 情景卡

> 主文见 [`../SKILL.md`](../SKILL.md)。三态只是评审摘要，不构成提交依据；提交判定 = `submit_verdict`（只有否决权）+ prod 实测 + 用户明确确认。

## 情景 JD-01　PPA 候选：Sharpe 1.2、PPAC 0.42、主题当期匹配

- **前置状态**：`type == PPA`（或标签含 `PowerPoolSelected`）；`get_messages` 主题的 region / delay / universe 与候选一致；`Failed PPA == 0`；`LOW_SHARPE` value 1.2（≥ 1）；本地 PPAC 0.42（< 0.5）。
- **步骤**：① `$WQ_PY scripts/judge_alpha.py --alpha-id <ID>` → 预期**不因 Sharpe < 1.58 判 BLOCK**（PPA 内部线 = `ppa_sharpe_min` 1.0，与平台 `LOW_SHARPE value < 1` 计失败一致）；② 人工核对清单（主题 / 标签颜色 PURPLE / prod < 0.7）；③ 走 PPA 渠道：满足本地预检可经 MCP，否则**停下交接**用户在 web UI 提交（`ppa-handoff.md`）。
- **分支**：主题不匹配 → 手工标 `YELLOW + WAIT_THEME_ROTATION`，等轮转（**没有代码实现**）；PPAC ≥ 0.5 → 内部严线不过，回步 7 换腿；Sharpe < 1.0 → `LOW_SHARPE` 计 PPA 失败，BLOCK。
- **完成定义**：清单逐项有结论；候选清单 + 证据交用户。
- **反例**：不要用 REGULAR 的 1.58 线判 PPA（旧口径会把 Sharpe ∈ [1.0, 1.58) 的合法 PPA 全判 BLOCK）；不要因 judge 说 READY 就调 `workflow_submit_alpha`。

## 情景 JD-02　多候选点塔排序（3 个候选）

- **前置状态**：三个过闸候选，配额只够 1 颗：X 落在 USA/D1/PV（现状 2/3，差 1 颗）、Y 落在 USA/D1/FUNDAMENTAL（1/3，差 2 颗）、Z 落在 GLB/D1/MODEL（0/3，0 亮区域）；fitness 分别 1.4 / 2.1 / 3.0。
- **步骤**：`python tools/campaign_intel.py pyramid --region <R> --delay <D>` 取各塔现状 → 按 [`quota-and-tower.md` §2.2](../../worldquant-submit-alpha/references/quota-and-tower.md) 排序。
- **预期**：**X（差 1 颗，一次点亮）> Y（差 2 颗）> Z（0/3 打地基）**——fitness 只在同档内起作用，所以 fitness 最高的 Z 排最后。
- **分支**：候选跨 ≥ 3 个 catalog → 对点塔零贡献，直接降级；区域是否「已过度提交」**没有机器阈值**：把本季度已提交数一并列给用户拍板。
- **完成定义**：排序表（候选 / 塔 / 现状 / 档位 / fitness）交用户；提交后重跑 `pyramid` 确认目标塔 +1 且 ≥ 3。

## 情景 JD-03　降级运行（无凭据 / 无 LLM key）

- **前置状态**：进程环境里没有 `CREDENTIALS_EMAIL` / `CREDENTIALS_PASSWORD`（或平台不可达）；`BRAIN_JUDGE_LLM_API_KEY` 未设。
- **步骤**：`$WQ_PY scripts/judge_alpha.py --alpha-id <ID>` → 预期正常出报告，**首行「降级运行」**，`degraded.is_degraded = true`，`platform.available = false`，`overall_verdict` 上限 **REVIEW**；LLM 层 `decision.available = false`（`missing_api_key` / `disabled_by_config`）。
- **输出能不能作依据**：**不能**。只剩表达式启发式：没有平台 checks、没有相关性、没有 trend 数据。它只能提示「表达式结构上哪里可疑」。
- **反例**：不要为了让脚本跑起来去读 `.env` 或把密码写进 `configs/config.json`（AGENTS.md 红线）；不要把降级报告里的 REVIEW / READY 转述成「可以提交」。
