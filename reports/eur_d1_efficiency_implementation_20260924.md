# EUR D1 挖掘效能优化落地记录

> 后续修订：本文的S2 `size`自动补精确数量已由[机制/对照选波优化](eur_d1_selection_optimization_20260924.md)替代。现在size仅为容量，预定实验由DB身份清单推导数量；其余工程保护继续有效。

日期：2026-09-24。对应会话复盘中四项已复现的工程问题，并修复验收时发现的经验报告路径问题；不把工程修复计作合格 Alpha，也不估算未经测量的提速倍数。

## 已实现

| 问题 | 现在的行为 | 验收证据 |
|---|---|---|
| MCP 在阻塞读取中忽略超时 | 每个请求的写入、刷新及等待响应由真实截止时间约束；超时返回请求身份与 outcome_unknown，连接不可复用，停止后续调用 | 真子进程接到请求后不响应，1 秒截止时间生效；同连接禁止再发。平台相关性查询实际超时后返回结构化未知结果，未继续派发第二条 |
| PID 被复用导致假 running | 新任务记录进程创建时间及可执行文件；旧任务用启动时间/命令核验，身份不符或不可读为 unknown；显式退出码/成功标记优先 | Windows 本机身份读取通过；两种任务布局均覆盖 PID 复用，另覆盖权限不足、空终态字段和明确退出码 |
| 固定 4 个机制静默缩水成 3 个；重选读残缺目标波 | 新增 expected-count 与 source-wave；workflow S2 显式 size 自动启用精确数量检查；选集事务检查并回读 picked 状态 | 真 CLI + 隔离 DB 复现 4→3 后阻止写入；从完整源池补齐已有 3 条到 4 条；碰到 superseded 时回滚而非误报成功 |
| 同源救援腿因 dataset 缺失逃过排除 | 按同区域、同 alpha_id 从回测和表达式反查来源；DB 证据优先于旧提示；未知来源不进入跨集筛选，多集候选按来源全集排除 | 测试覆盖陈旧提示、跨区域、多来源和未知来源；真实 EUR 查询排除 fundamental23 后返回 44 条其他来源，另剔除 6 条来源未知记录 |
| S6 显示成功却写到技能目录，仓库经验未更新 | 默认输出固定到仓库 reports/dataset_experience；显式 out-dir 仍可覆盖 | 外部工作目录启动的真实 CLI 回归通过；实际 S6 重跑后，仓库 fundamental23 文件波次247–250、18条，三集共31条，人工复盘保留 |

主流程说明已更新；仓库 skill 源已同步到 Claude、Codex、Cursor、Workbuddy 四个安装位，`sync_skills --check` 全部通过。通过新 MCP 进程实际干跑 S2，命令含 `--expected-count 4 --source-wave s2_fundamental23_d1`，未启动模拟。

## 使用与恢复

- 固定机制实验通过现有 workflow S2 传 `extra_args=["--size","4","--source-wave","s2_fundamental23_d1","--auto-coverage","never"]`；直接 CLI 需显式传 `--expected-count 4`。
- 数量不符先读 `selection-count` 的来源、候选数和配额排除原因；状态不符先核对历史。不得为凑数量自动复活已丢弃或已回测的表达式。
- MCP 超时后的远端结果可能已发生；先核对 task、checkpoint 与 DB，再决定是否重试。超时本身不等于模拟失败或被取消。
- 来源不同不代表低相关；救援候选仍须经过当前毒模式、Prod/Self 和稳健性检查。此次只读补来源，不改写历史台账。
- 数量一致性检查覆盖本次 picked；历史 selected/gated 的清理仍沿用已有纪律。旧目录任务没有明确终态且进程已退出时，仍使用原有日志推断，最终收批以 DB 为准。
- 已运行的长期 MCP 服务可能持有旧模块；本轮实际验证使用新 MCP 连接。技能脚本已同步，之后重启 MCP 服务才会让所有长期连接加载新节点与查询逻辑。

## 验证

新增 15 个故障回归用例，并扩展已有 S2 命令用例，验证输出命令确实包含数量契约。定向测试通过；包含路径修复的最终全量回归 **1387 passed、10 skipped，42.67 秒**，结果保存在 `logs/test-results.xml`。四个安装位同步检查均通过。

初次全量运行停在既有 detached 子进程清理用例；保持代码不变，在允许清理测试自身进程的环境重跑该组为 4/4 通过，因此不改断言或进程清理实现来绕过环境限制。

## 实施边界与战役状态

本轮没有实现旧加权先验过滤、完整耗时指标、代表相关性自动前置或机制预算自动化；这些仍是下一批事项，不计入本次收益。

wave250 已完成 4/4 回测及 S4，累计本会话 waves245–250 为 31 条正式回测。两个 near 候选：78NoOeVx 的 Sharpe/Fitness 为 1.67/1.06，rKOdkZX9 为 1.61/1.09；当前换手率与风险中性化后 Fitness 未满足本战役要求，相关性尚未完成。仍为 0/10 完整核查合格 Regular Alpha。

历史 wave215 的原 PID 在本次复验时已退出，不能再把它当作现场 PID 复用复现；该故障由受控回归测试验证。不会把旧任务的推断 succeeded 当作新增研究产出。

经验路径修复通过任务 `campaign_EUR_S6_20260924_214932` 验证；误写在技能目录的报告已移入 `attic/experience_output_path_20260924` 保留。人工索引同步到31条，相关性待核实状态已写 `s6_verdict_250`。

代码入口：`tools/mcp_ping.py`、`src/wqb/workflow/process_identity.py`、`src/wqb/workflow/tasks.py`、`src/wqb/workflow/nodes/{campaign,batch_track}.py`、toolkit `scripts/build_wave.py`、`src/wqb/research/{salvage_provenance,dataset_experience}.py`、`wqb_db_mcp.py::get_salvage_pool`。未创建提交或修改平台提交门槛。
