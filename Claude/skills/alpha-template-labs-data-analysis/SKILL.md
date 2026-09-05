---
name: alpha-template-labs-data-analysis
layer: L0
description: "Brain Labs 原始数据分析辅助代理（S0 前研究步骤）：检查 USA/TOP3000/D1 MATRIX 数据集，诊断覆盖/缺失/频率/离群值/相关性，把发现转化为 Python 原生抽取机制。当用户要在设计 Python alpha 前做 Labs 原始数据分析时使用。触发词：Labs 分析 / 原始数据分析 / labs data analysis / Python alpha 设计前置。"
user-invocable: true
allowed-tools:
  - Read
  - Bash
  - mcp__wq-brain-http__*
---

# /alpha-template-labs-data-analysis

运行 Brain Labs 数据分析代理，说明见
[reference/brain-labs-data-analysis-agent.md](docs/reference/brain-labs-data-analysis-agent.md)。

## 用途定位

这是**仿真前的研究步骤**。在 S2 候选设计之前回答：该数据集是否存在 Python 原生优势。

## 必走流程

认证/生成脚本/摄取这三步优先用 MCP Labs 工具——它们在 Labs 单并发锁后面包装同一个 `world-quant-brain-mcp/labs_data_analysis_agent.py` 代理。MCP 未覆盖的步骤才回退本地 CLI（见下）。

1. 只拉 MATRIX 字段（无需 Labs 登录）：

```python
mcp__wqb-mcp__get_datafields(
    dataset_id="<dataset_id>",
    region="USA",
    universe="TOP3000",
    delay=1,
    data_type="MATRIX",
    filter_sharpe=False,
)
```

2. 仅当确实需要新 Labs 会话（且配额告警后已获批准）时，登录并取活的 WorkSpaces URL：

```python
mcp__wqb-mcp__authenticate_brainlabs()
# -> {workspaces_url, labs_url, token, ...}; 打开 workspaces_url
```

3. 生成可粘贴的 Labs 脚本（至多两个 MATRIX 字段）：

```python
mcp__wqb-mcp__emit_labs_script(
    dataset_id="<dataset_id>",
    fields=["<field_a>", "<field_b>"],
    region="USA", universe="TOP3000", delay=1,
    labs_output="/tmp/labs_data_analysis_<dataset_id>_raw.json",
)
```

4. 在 Brain Labs 里运行该脚本，检查原始面板行为：覆盖、缺失、真零、哨兵值、更新频率、离群值、分布、换手 proxy、字段相关性。
5. 摄取返回的 Labs JSON（传 JSON 字符串或文件路径）：

```python
mcp__wqb-mcp__ingest_labs_result(result_json="<labs_json_or_path>")
```

6. 对每个字段分类数据形状与下游 Python 适用性。
7. 写 `tracking/runs/<ts>_labs_data_analysis_<dataset_id>.json`。
8. 返回接受/拒绝的机制及对 Python alpha 的启示。

### CLI 专用步骤（MCP 无对应）

用 `rtk python3 world-quant-brain-mcp/labs_data_analysis_agent.py ...` 执行：

- `emit-notebook-exec` — 把脚本包成单行 `exec(...)` 供 WorkSpaces 远程 notebook 粘贴（避免单元格类型/缩进损坏）。
- `emit-summary-cell` — 下载/剪贴板无法回传本机时，在 Labs 内生成紧凑摘要。
- `ingest --field-meta ... --evolution-review ... --markdown ...` — 增强摄取（补字段元数据、优先级 0 优化闸与 markdown 产物；MCP `ingest_labs_result` 只解析返回 JSON）。
- `screen-datasets` — 仿真前的兜底清单筛查。
- `demo` — 无平台原始数据的本地运行时验证。

## 硬规则

- 禁止调用 `submit_alpha`。
- 除非用户明确要求继续进入 S3，本代理内禁止仿真。
- 下游 Python alpha 设计禁止用 VECTOR/GROUP 字段。
- 禁止照抄论坛公式。论坛材料只用于诊断、字段方向、失败模式与预处理线索。
- 最终推荐必须是一个机制、至多两个 MATRIX 字段。
- **WebDataScope 体检交叉验证（2026-08-05 新增）** — Labs 原始数据分析的结论（覆盖/缺失/分布/离群值）应与 WebDataScope 离线体检数据包（`tools/webdata_quality.py --fields <ds>`）交叉验证：两者覆盖率和分布形状判定一致时高置信；不一致时以 Labs 实时数据为准（体检数据包是 2012-2021 离线快照）。从 Labs 分析衍生的表达式在提交前必须通过 `check_expr_against_inspect` 体检硬门校验（见 [`../wq-brain-ra-pipeline/SKILL.md`](../wq-brain-ra-pipeline/SKILL.md) 步 5）。

## 默认示例

`USA TOP3000 D1 imbalance5`：检查 `imb5_score` 和 `imb5_mktcap`。
把 `imb5_score` 当主信号（石油冲击韧性分数），`imb5_mktcap` 当上下文。除非 Labs 显示水平值异常稳定且不拥挤，否则优先做状态切换或意外抽取，而非原始分数水平。
