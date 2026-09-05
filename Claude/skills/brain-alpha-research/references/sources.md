# Research Source Priorities

- Prefer primary papers for algorithmic ideas.
- Prefer official BRAIN documentation for platform behavior.
- Use forum experience for practical settings, rate limits, and repair workflows.
- **WebDataScope 离线数据包（`WebData_*.zip`）** — 社区提交快照 + 逐字段体检数据，零成本预筛数据集/字段质量、中性化选择、分布形态分析。规则见 [`webdatascope-data-quality.md`](webdatascope-data-quality.md)，脚本 `tools/webdata_quality.py`。结构化导出 `--export-expr` 供 orchestrator 体检硬门消费。
- Convert every useful insight into a configuration rule, profile, or measurable diagnostic.
