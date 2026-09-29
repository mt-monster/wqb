# skills 审查整改：决策登记（DEC）

> 每条：问题 → 证据来源（MCP 调用 / 代码 / DB / 平台不可达）→ 结论 → 影响条目。
> 背景：用户要求「处理所有优化项，并优先连上 MCP 服务去决策问题」。**MCP 两个服务都能在本地起来并握手**（`wqb-db` 44 工具、`wq-brain-http` 69 工具），
> 但出口代理对 `api.worldquantbrain.com:443` 回 403（环境网络策略），且环境里没有平台凭据——凡依赖平台实测的问题，标 `needs-platform` 并写清怎么复核。
> 解除方式：在云端环境设置里放开该域名（Network access），并以环境变量提供 `CREDENTIALS_EMAIL` / `CREDENTIALS_PASSWORD`（新会话生效；**不要在对话里贴凭据**）。

| DEC | 问题 | 证据 | 结论 | 影响 |
|---|---|---|---|---|
| DEC-01 | MCP 是否可用于裁决？ | 会话内两服务 ENOENT（`.mcp.json` 用 `D:/` 绝对路径）；改用 stdio 真实启动后 `wqb-db` 44 / `wq-brain-http` 69 工具握手成功；`authenticate` / `get_operators` 重试两次均失败：出口代理对 `api.worldquantbrain.com:443` 回 403，且无平台凭据 | 离线可用工具（`operator_audit` / 本地 gate / DB 类）作裁决依据；平台依赖问题标 `needs-platform` 并给复核脚本；`.mcp.json` 改为可移植的 `${VAR:-default}` 写法 | T0-9、T0-12、X-14、X-16 |
| DEC-02 | `ts_median` 是否可用？ | MCP `operator_audit(["ts_median(close,22)"])` → `violations=ghost_ops[ts_median]`；`config.GHOST_OPERATORS`（MCP 返回 18 个）；同时 `validate_expressions` / `preflight_expressions` 对它返回 valid=true（不查幽灵算子） | `ts_median` 判幽灵：SOP 一律移除；create_multi_simulation 之前须显式跑 `operator_audit`（validate / preflight 不足以拦幽灵） | DF-08、EX-08、HP-19 |
| DEC-03 | 幽灵算子清单两份口径（`platform_constraints.ghost_ops` 10 项含 `ts_max` / `ts_min`；`config.GHOST_OPERATORS` 18 项） | 代码：`ts_max` / `ts_min` 在 platform_constraints 里归 `inaccessible_ops`（闸 4 拦截），并非平台不存在 | 两份职责不同：ghost = 平台不存在；inaccessible = 平台有但本账号 ERROR。单源 = `config.GHOST_OPERATORS` ∪ `platform_constraints.ghost_ops`，再减去账号不可用者 | X-7、X-16 |
| DEC-04 | `submit_verdict` 退出码 | 代码：CLI / MCP 两份 + batch 第三份（缺 Failed-count 门）；`SUBMITTABLE` 依赖 `GET /submit`=200（文档称恒 404，平台不可达无法复核） | 0 = SUBMITTABLE / 1 = BLOCKED / 10 = UNVERIFIABLE / 11 = ALREADY_SUBMITTED；`SUBMITTABLE` 保留为防御分支（无法复核平台行为，不删）；判定收成 `wqb.submit_verdict_core` 一份 | T0-1、SB-03、X-2 |
| DEC-05 | 测试套件在容器里被 SIGKILL（137） | 复现：`test_detached_first_output_heartbeat` 的子进程与 pytest 同进程组，`_kill_process_tree` 的 `killpg` 把调用方一并杀掉 | 修 `_kill_process_tree`（同组只杀子进程）+ 测试用 `start_new_session`；加回归测试 | 环境耦合 |
| DEC-06 | 「台账记因 / 豁免」17 处没有键名 | 代码：`stop_rules_override` / `backlog_gate_override` 在 `campaign.py` 各手写一份 SQL + JSON + 日期比较；缺 `until` 即永久放行；没有批准人；放行不进任何报告 | 协议 `waiver_<gate>_<region>_<wave\|all>` + `wqb.waiver` 唯一实现：`expires_at` 必填、按闸限批准人与最长有效期、红线不可豁免；旧键继续识别（缺 `until` 仍放行但告警 NO_EXPIRY，不静默改行为）；逃生口缺省 **warn**（无 waiver 只在首屏告警），`--waiver-mode enforce` 才拒绝——避免一刀切打断现有工作流 | X-8、RA-28、RA-117、RD-01 |
| DEC-07 | prod 墙处置 ≥6 套学说（X-1，报告标注「需业务裁定」） | 文档：RA 步 5b（≥0.7 即 dead_end、任何去相关变体无效）与 decision-table D14（结构性去相关 / 中性化骨架重构 有 MEA 9qXoJge2 0.716→0.6525、KOR wave113 0.7003→0.6993 的成功实证）互相矛盾；镜像稀释是「腿相加」，与全局禁令直接冲突且引用的 SOP 文件不存在；`campaign_intel.py prod-first` 缺省 `--top-k 3` | **一张表（D0-P）**：<0.60 扩变体；0.60–0.70 不扩变体当天提交；**0.70–0.75 踩线带只许 1 次结构性尝试**（删腿 / 换广度轴，或表达式层 `group_neutralize` 包裹），仍 ≥0.70 → dead_end；≥0.75 直接 dead_end；镜像稀释撤回；区域 profile 不得另设预警线。实证均来自历史记录，**未能向平台复核**（needs-platform） | X-1、T0-11、RA-69/74/85/93、RD-04/28、OP-01、RC-01/03、RP-07、RR-02、RE-08、SP-09 |
| DEC-08 | Failed-count 里「名单内检查仍 PENDING」怎么处理（RF-03） | 代码：`check_counts_as_failed` 把 PENDING 排除在失败之外，与平台「PENDING 不挡提交」一致；但 `Failed=0` 在有名单内 PENDING 时只是「暂无失败」 | **不改口径**，只在输出里增加 `pending_ra` / `pending_ppa`（数量 + 名字）；`submit_verdict` 在有 PENDING 时于说明里点明「不得据此放行」。frozen 副本（`mcp_core`）同步，测试逐项比对 | RF-03、SB-11 |
| DEC-09 | `workflow_submit_alpha` 的 `color` 缺省 | 代码：MCP 工具签名 `color="GREEN"` 显式传给节点，顶掉节点的 `None → BLUE` 缺省；规格：GREEN 须由 OS 结果挣得 | 工具签名改 `color: Optional[str] = None`（缺省交给节点取 BLUE）；加 AST 守护测试 | SB-05、SB-06 |
| DEC-10 | 「提交」一词两义（派发仿真 vs 把 alpha 提交上平台） | 代码：`tools/submit_batch.py` 与 MCP `submit_batch` 是 `POST /simulations`；真正提交是 `workflow_submit_alpha` | **不改名**（改工具名会全线失配，且有计数守护）；词表定义 `dispatch` / `submit`，在 AGENTS / tools README / 两处 docstring / 各 skill 文案里加注 | SB-24、JD-09、X-4 |
| DEC-11 | `SubmissionsMixin.get_quota_status`（48h 滚动窗口） | 代码：口径 2026-09-01 已被推翻，全仓库无任何调用方（含测试） | 删除；注释指向 `tools/quota_status.py` / `wqb.timeutil` | SB-21、T0-14 |
| DEC-12 | ledger 键「有读取方无写入方」怎么处理 | 扫描：`saturated_datasets`、`seat_model`、`template_kb`、`operator_principle_kb` 有读取方、仓库内没有写入方；`submit_ready_blocked` 文档承诺 S0 读取、代码只计数 | **不假装修好**：登记为 `orphan` 并指向审查条目，测试守「登记必须仍为真」（一旦补上写入方必须删登记）；补写入方属产品决策，不在本轮文档整改内 | X-7、X-18、IX-20、RA-113、TK-18 |
