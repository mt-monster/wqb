# monitor 情景卡

> 主文见 [`../SKILL.md`](../SKILL.md)。`$WQ_PY` = MCP venv 解释器（`python tools/_pyenv.py` 打印其路径）；`$WQ_TOOLKIT_DIR` = `Claude/skills/wq-brain-campaign-toolkit/scripts`。下面所有数值都是**示例数据**，只演示格式与判据。

## 卡 BM-1　日常一波收尾（pipeline 完成 → 复盘回写 → 自检）

- **前置状态**：KOR 第 190 波，`batch_status.py` 显示批次都到了终态。
- **步骤**
  1. 确认没有在飞批：`$WQ_PY tools/batch_status.py --ids <multisim id …>`，退出码 0 = 全部终态且无 error；
  2. 若评审还没跑：`$WQ_PY $WQ_TOOLKIT_DIR/campaign.py --campaign-dir tracking/KOR pipeline run --wave 190 --review`（同一波从 checkpoint 续跑，只补评审）；
  3. 按 RA 步 9 §9.1 的顺序回写（漏斗 → verdict → 点塔 → `upsert_wave_result` → 判死 / 胜绩 → 饱和 → 数据集经验 → 刷新先验快照）；
  4. 自检：`mcp__wqb-db__get_wave_result region=KOR wave_number=190`，`verdict` 为 `PASS` / `PARTIAL` / `FAIL` 之一，且按 §9.7 的完成定义逐项打钩。
- **分支**：`verdict` 为空 → 本波**未完成**，回第 3 步；被拒（返回带 `suggestion`）→ 核对后显式传 `verdict=<枚举>`，原文放进 `key_findings`。
- **完成定义**：`get_wave_result` 的 verdict 非空，且 §9.7 清单全部勾上。
- **反例**：只把报告写成 `.md` 就收工；用 `ledger set-verdict` 写 `wave190_verdict`（已废止的旧键）。

## 卡 BM-2　挂起处置（STALLED）

- **前置状态**：某波 `RUNNING` 批很久没变化。
- **步骤**
  1. `mcp__wqb-db__get_ledger_key region=KOR key=ckpt_w190` → 看 `batches[]` 里 `status = RUNNING` 的 `submitted_at`；
  2. 与 `wqb.config.WAIT_THRESHOLDS['sim_stall_min']` 比：progress 超过阈值仍无变化 → 判 `STALLED`；
  3. 平台侧核对：`$WQ_PY tools/batch_status.py --ids <该批 multisim id>`（平台其实已终态但 checkpoint 没更新，与「真挂起」处置不同）；
  4. 判停后在本波 `key_findings` 记一条：哪批 / 哪个 multisim / 卡了多久 / 平台侧状态；
  5. 是否重提：`pipeline run --wave 190` 会从 checkpoint 续跑并重发未完成批（`--fresh` 才全新开始，慎用）；重提前先看并发是否被占满（`config.CONCURRENCY`、`wqb-concurrency` §8），别在 429 风暴里重发。
- **完成定义**：这一批有明确处置（续跑 / 放弃）和一条留痕。
- **反例**：不等阈值就「觉得没动静」判停；对 `RUNNING` 批的 checkpoint 手改状态（红线）。

## 卡 BM-3　汇报样例（≤ 20 行，含强制章节）

```text
R1 背景  KOR / 战役账号 / 2026-09-29 14:00–15:10，wave 190（fundamental17，D1）
R2 进度与 ETA
| wave | 进度 | 预期完成 | 置信度 |
| 190  | 5/10 批 | 09-29 16:05 | 中（已跑 70 min） |
R2 提交状态盘点（数据取自 alphas / robustness / submit_verdict）
| alpha_id | IS 结论 | prod（时间） | robustness | submit_verdict | 分类 |
| AAAA1111 | Failed RA 0 | 0.58（14:52） | PASS | UNVERIFIABLE | ✅ 待提交（须用户确认） |
| BBBB2222 | PASS_CHEAP | 未测 | — | — | 🔶 仍需验证（研究仿真 IS 闸通过、提交未验证） |
| CCCC3333 | Failed RA 0 | 0.81（14:40） | PASS | BLOCKED | 🔶 仍需验证（prod 墙，按 D0-P 处置） |
R3 核心发现  本波 40 条过闸，过廉价闸 6 条；瓶颈在 prod 读数而非回测吞吐（待步 9 漏斗确认）
R4 结论  3 个候选：0 已提交，1 待提交（须用户确认），2 仍需验证
    问题：CCCC3333 落在 D0-P 的 ≥ 0.75 行 → 先 forum_recon 再封存；行动：AAAA1111 提交前 check_correlation(refresh=True) 终验
```

要点：**ETA 与提交状态盘点两个强制章节都在**；`PASS_CHEAP` 不称可提交；prod 读数带时间；结论句式是「N 个候选：a 已提交，b 待提交，c 仍需验证」。
