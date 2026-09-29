# ppa-mining 归档（2026-09-29，skills 审查 PP-04）

- `dataset_health_check.py`（486 行）：原随 `wq-brain-ppa-mining` 分发的 S0 体检脚本（`--mode mcp` 复用常驻 MCP、`--mode direct` 用 `.env` 凭据自行 Basic Auth 直连）。
- **归档原因**：零调用方（全仓库只有文档引用，无代码 / 测试）；S0 体检的**唯一执行器**已是 `workflow_campaign(stage="S0")` + `tools/campaign_intel.py s0-select`；直连模式自读 `.env` 又多出一个凭据来源。RA 侧的同名副本早已因「零运行痕迹」归档。
- 恢复：`git mv` 回 `Claude/skills/wq-brain-ppa-mining/scripts/` 即可；但恢复前先确认它与 `score_datasets.py` 的三硬门槛口径一致，并去掉 `.env` 直连。
