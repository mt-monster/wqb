# Task Plan: KOR REGULAR Alpha 持续挖掘（目标 20 颗可提交）

## Goal
在 KOR 区域走完整 RA 链路 S-PRE→S6，持续自我挖掘 type=REGULAR alpha，产出 **20 个本次任务新挖掘的可提交 Regular Alpha**（OS ACTIVE 或全部硬闸通过）后停止；judge READY 后向用户报告并等待确认，不自动提交。

## Current Phase
Phase 1: S-PRE 查表 + 开工前置

## Phases

### Phase 1: S-PRE 查表 + 开工前置
- [ ] 读 KOR profile（已读：active, TOP600, delay=1, STATISTICAL）
- [ ] DB 查表：region_config / campaign_summary / dead_ends / dead_datasets / campaigns / submit_ready / region_kb
- [ ] 算子审计（ghost-op guard）
- [ ] PPA 主题匹配门禁（get_messages）
- [ ] 产出预解析配置包
- **Status:** in_progress

### Phase 2: S0 数据集体检 + 白名单锁定
- [ ] score_datasets.py --calibrate --dry-run 再 apply
- [ ] 用户覆盖：cov≥0.6 / alpha≤1500 / fields≥10；排除 MODEL
- [ ] 重点 Other / PriceVolume / Risk / Short Interest 未点亮集（可先不体检入候选）
- [ ] upsert_ledger_key s0_whitelist
- **Status:** pending

### Phase 3: S1 字段扫描 + 特征工程
- [ ] scan-fields typed catalog
- [ ] 预处理决策（初始信号 vs 进阶信号）
- [ ] users 分级（冷门≥50% 批次预算）
- **Status:** pending

### Phase 4: S2 GEM 生成 + 门禁 + 设置展开
- [ ] assemble-priors
- [ ] GEM 概念优先（1-2 字段，新模板）
- [ ] wave_gate 5 闸
- **Status:** pending

### Phase 5: S3 五槽填槽回测（8 并发 multi_create_simulate）
- [ ] MCP create_multi_simulation
- [ ] 轮询回收、即收即补
- **Status:** pending

### Phase 6: S4 评审链（不自动提交）
- [ ] AlphaTest 诊断 → Mode B → Mode A → 本地 self/PPAC → 归因 → robustness → judge
- [ ] judge READY 停下来报告等确认
- **Status:** pending

### Phase 7: 循环至 20 颗 + 优化方案沉淀
- [ ] 达 20 停止
- [ ] 提示词驱动的 skills/workflow/db/code 全面优化方案
- **Status:** pending

## Key Questions
1. 本次任务「新挖掘」如何计数？仅本会话新过闸且未提交的 Regular，不含历史 ACTIVE。
2. 用户放宽 S0（cov≥0.6/α≤1500/f≥10）且指定 Other/PV/Risk/SI 可先不体检 — 用户指令优先于 profile 红灯与默认硬门槛，台账记录覆盖原因。
3. 停止闸=20（覆盖默认 4 / RA≥10）。
4. 提交：judge READY 只报告，等用户确认；确认后按绩效最好先提。

## Decisions Made
| Decision | Rationale |
|----------|-----------|
| 用户指令覆盖 S0 阈值与「未点亮集可先不体检」 | decision-table 优先级：用户显式指令 > 决策表 > skill 正文 |
| 排除 MODEL | 用户硬约束 + pyramid_quota 要求非 MODEL |
| 不自动提交 | RA 步 8 + 用户纪律 |
| 规划文件落项目根 | planning-with-files 强制 |

## Errors Encountered
| Error | Attempt | Resolution |
|-------|---------|------------|
|       | 1       |            |

## Notes
- 停止闸 20，不是 4。
- 每条表达式 1-2 个 catalog 字段；prod_corr≥0.7 不提交回 Mode B；跨数据集策略相关 <0.4。
- 回测优先 MCP，少写临时脚本。
- 挖出有效可提交因子后再做上下文压缩，中途不丢信息。
