# judge 开发者备忘（不属于 agent 用法）

> 旧 SKILL 的「独立原则」一节是给开发者的代码规约，对使用 skill 的 agent 无用（skills 审查 JD-17），移到这里。

- **自包含**：本 skill 只从自己的目录导入；运行时辅助代码放 `scripts/vendor/`；不依赖 `untracked/`（该目录在仓库里并不存在，是历史遗留）。
- **vendor 4 个文件**（`ace_client` / `auth_utils` / `llm_judge` / `load_credentials`，≈ 440 行）与主 MCP 代码有重复；改动它们时同步检查 `tests/unit/02_workflow/test_judge_never_submits.py`（不得出现 `POST …/submit`、LLM 缺省关闭、凭据只读环境变量）。
- **`INTERNAL_HARD_GATES`** 是内部闸的**第 3 份拷贝**（`wqb.config.GATES_INTERNAL`、`submit_queue.LIM`、此处）：skill 不 import `wqb`，故保留本地常量，数值一致性由 `tests/unit/02_workflow/test_judge_gates_match_config.py` 守——改任何一处都要跑它。
- **外发白名单**：`build_llm_payload` 是唯一构造 LLM 载荷的地方；新增字段前先确认不含表达式原文（除非 `send_expression=true`）。
