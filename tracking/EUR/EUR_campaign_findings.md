# EUR Campaign Findings

## Requirements
- 区域：EUR。
- 类型：REGULAR alpha。
- 目标：本轮形成并完成至少 20 个新候选的挖掘链；每个完成的 S 阶段输出有价值的、以实际结果为依据的总结。
- 使用 `wq-brain-ra-pipeline` 作为唯一编排路径，不能跳过 S-PRE、S0、S1、S2 门禁、S3、S4/S6。
- 所有 alpha 提交必须等待用户明确确认。

## Initial Findings
- RA SOP 已明确：EUR 的历史实测达标率较低，且转换率曾表现为积压问题；因此必须在 S-PRE 读取实时台账与产出率，不能据历史基线直接判断本轮可行性。
- S2 必须使用 `workflow_gem` 概念优先生成；仅生成表达式而未入库或未过门禁不计为合格候选。
- S3 使用实际平台并发纪律，不能凭空指定并发数；回测结果和门禁结果是 20 个候选计数的权威证据。
- 项目根目录已有 KOR 的规划文件，本 EUR 战役使用独立的 `EUR_campaign_*.md` 追踪，避免破坏已有工作。
- EUR profile 当前准入为 active：默认 `TOP1600`、delay 1、`SUBINDUSTRY`；已验证机制是 0.4 慢 MODEL 残差加 0.6 快 PV，设置为 decay 4。
- EUR 每波至少两槽必须按该获胜机制换腿；每波最多一槽可探索 `ILLIQUID_MINVOL1M`、`TOPCS1600` 或 delay 0，不能挤占换腿槽。
- 本会话当前未获得动态 `mcp__wq-brain-http__*` / `mcp__wqb-db__*` 工具条目；将以同一项目内 MCP 的 STDIO 协议客户端调用服务，而非绕开服务手写 HTTP。
- DB MCP 已通过初始化并处理 `ListToolsRequest`；首次仅在本地输出阶段受 GBK 编码阻断，说明连接本身正常。
- DB S-PRE 工具 schemas 已核验，包含区域配置、摘要、死路、判死数据集、跨区经验、按区域/数据集产出率、战役状态和高 Sharpe 历史搜索。
- BRAIN MCP 首次 schema 枚举仅输出启动日志，约 37 秒内没有返回协议结果；在确认启动状态前不调用算子审计或论坛查询。
- 源码确认启动配置正确：`main.py` 只在导入完所有工具模块后才打印 "running the server"，并从 `MCP_TRANSPORT` 读取 `stdio`。因此首次尝试未出现该行，当前证据指向工具模块导入阶段，而非凭据校验或协议调用阶段。
- 直接启动验证表明 BRAIN 服务约 10 秒后已打印 "running the server"；实际原因是本次临时协议客户端把结果输出放在会话关闭之后，而 FastMCP 子进程关闭可能延迟。客户端现改为在会话仍存活时输出。

## Open Questions
- EUR profile 的当前准入、数据集白名单和既有死路是什么？由 S-PRE 权威查询回答。
- 本轮可用配额和平台槽位如何？由 S-PRE/S3 运行时状态回答。

## Resources
- RA SOP: `C:\Users\MENGTAO\.codex\skills\wq-brain-ra-pipeline\SKILL.md`
- EUR profile: `C:\Users\MENGTAO\.codex\skills\wq-brain-ra-pipeline\references\regions\EUR.md`
- Project MCP definition: `D:\coding\traeCN_project\wqb\.mcp.json`
