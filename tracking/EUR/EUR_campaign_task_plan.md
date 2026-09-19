# EUR Regular Alpha Campaign Plan

## Goal
在 EUR 区域按 Regular Alpha 标准链路完成 S-PRE→S6，挖掘并评审至少 20 个本次新建的、通过 S2 门禁后进入 S3 的 REGULAR alpha 候选；对每个已完成 S 阶段给用户提供基于实际结果的结论摘要。提交 alpha 始终等待用户明确确认。

## Current Phase
Phase 1 — S-PRE 查表、区域准入与运行前置。

## Phases

### Phase 1: S-PRE 查表与准入
- [ ] 阅读 EUR profile 和决策表
- [ ] 查询 EUR 历史、死路、数据集、实测产出率和战役状态
- [ ] 完成实时算子审计与当前 PPA 主题扫描
- [ ] 形成 EUR 设置、排除项和首波数据集决策
- **Status:** in_progress

### Phase 2: S0 数据集体检与白名单
- [ ] 校准后运行 S0 体检并锁定白名单
- [ ] 确保至少两个非 MODEL 数据集
- [ ] 回写 S0 白名单与排序依据
- **Status:** pending

### Phase 3: S1 字段扫描与特征理解
- [ ] 扫描每个白名单数据集的 typed catalog
- [ ] 完成冷门字段优先级、数据类型和预处理约束
- [ ] 记录 S1 决策与 feature-engineering 思路
- **Status:** pending

### Phase 4: S2 概念生成与门禁
- [ ] 组装 EUR priors
- [ ] 使用 GEM 生成概念优先表达式
- [ ] 运行每波门禁；失败项回到生成阶段修正
- [ ] 建立至少 20 个本次新建且过门禁的 REGULAR alpha 候选池
- **Status:** pending

### Phase 5: S3 回测与收割
- [ ] 按平台槽位进行 batch-track 回测
- [ ] 跟踪并收割每个批次的最终结果
- [ ] 对应 20 个候选形成可审计的仿真记录
- **Status:** pending

### Phase 6: S4/S5/S6 诊断、判定与复盘
- [ ] 诊断 S3 结果、执行必要的优化或判死
- [ ] 仅报告通过稳健闸和 submit_verdict 的候选；绝不自动提交
- [ ] 回写 wave、经验注册表与 EUR 台账
- **Status:** pending

## Decisions Made
| Decision | Rationale |
|---|---|
| 以“20 个通过 S2 门禁并进入 S3 的新 REGULAR 候选”为最低数量口径 | 这可证明每个 alpha 实际进入挖掘链，而不把未验证表达式计为成果。 |
| 不自动提交 alpha | RA SOP 和仓库规则均要求在 S5 得到用户明确确认。 |
| 另建 EUR 规划文件 | 现有 task_plan.md/finding.md/progress.md 属于 KOR 战役，必须保留。 |

## Errors Encountered
| Error | Attempt | Resolution |
|---|---:|---|
| PowerShell foreach 后直接接管道导致解析错误 | 1 | 改用逐行输出后成功读取既有规划文件。 |
| MCP 工具 schema 输出含特殊字符，默认 GBK 控制台报 UnicodeEncodeError | 1 | 按仓库约定以 Python UTF-8 模式重跑，不重发失败的服务请求。 |
| BRAIN MCP schema 枚举启动后 37 秒未返回初始化/工具结果 | 1 | 不重复同一枚举；检查启动路径和服务日志后改用最小协议烟雾测试。 |
