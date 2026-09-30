---
name: alpha-template-labs-data-analysis
layer: L0
description: "Brain Labs 原始数据分析辅助代理（S0 前研究步骤）：检查 USA/TOP3000/D1 MATRIX 数据集，诊断覆盖/缺失/频率/离群值/相关性，把发现转化为 Python 原生抽取机制。当用户要在设计 Python alpha 前做 Labs 原始数据分析时使用。触发词：Labs 分析 / 原始数据分析 / labs data analysis / Python alpha 设计前置。"
last_verified: 2026-09-28
user-invocable: true
allowed-tools:
  - Read
  - Bash
  - mcp__wq-brain-http__*
---

# /alpha-template-labs-data-analysis

## 职责边界

- **本 skill 负责**：S0 前的 Brain Labs 原始数据分析：覆盖/缺失/频率/离群值/相关性诊断
- **本 skill 不做**：不开战役、不选最终字段、不回测；结论只作 S1 输入
- **上游 / 下游**：上游 = Labs 原始数据；下游 = S1 字段选择


运行 Brain Labs 数据分析代理，说明见
[reference/brain-labs-data-analysis-agent.md](docs/reference/brain-labs-data-analysis-agent.md)。

## 用途定位

这是**仿真前的研究步骤**。在 S2 候选设计之前回答：该数据集是否存在 Python 原生优势。

## 必走流程

**结构 = 主流程 + 增强 + 兜底**：以下 8 步是**主流程**（MCP Labs 工具优先）；下方「增强 + 兜底」小节是 MCP 未覆盖时的回退，按触发条件选用。认证/生成脚本/摄取这三步优先用 MCP Labs 工具——它们在 Labs 单并发锁后面包装同一个 `world-quant-brain-mcp/labs_data_analysis_agent.py` 代理。MCP 未覆盖的步骤才回退本地 CLI（见下）。

1. 只拉 MATRIX 字段（无需 Labs 登录）：

```python
mcp__wq-brain-http__get_datafields(
    dataset_id="<dataset_id>",
    region="USA",
    universe="TOP3000",
    delay=1,
    data_type="MATRIX",
    filter_sharpe=False,
)
```

2. 仅当**确实需要新 Labs 会话**时才登录取活 WorkSpaces URL。机械判据（三者全满足才登录）：
   - 已有 Labs 会话不可用（无活跃 `workspaces_url` 或 token 过期）；
   - 主流程确实要跑 Labs 脚本（而非仅 `get_datafields` 拉字段）；
   - 用户已明确批准（批准入口：向用户询问并收到「同意/继续」）。配额告警后**必须**先获用户批准，不得自行静默登录。

```python
mcp__wq-brain-http__authenticate_brainlabs()
# -> {workspaces_url, labs_url, token, ...}; 打开 workspaces_url

```

3. 生成可粘贴的 Labs 脚本（至多两个 MATRIX 字段）：

```python
mcp__wq-brain-http__emit_labs_script(
    dataset_id="<dataset_id>",
    fields=["<field_a>", "<field_b>"],
    region="USA", universe="TOP3000", delay=1,
    labs_output="/tmp/labs_data_analysis_<dataset_id>_raw.json",
)
```

4. 在 Brain Labs 里运行该脚本，检查原始面板行为：覆盖、缺失、真零、哨兵值、更新频率、离群值、分布、换手 proxy、字段相关性。
5. 摄取返回的 Labs JSON（传 JSON 字符串或文件路径）：

```python
mcp__wq-brain-http__ingest_labs_result(result_json="<labs_json_or_path>")
```

6. 对每个字段分类数据形状与下游 Python 适用性。
7. 写 `tracking/runs/<ts>_labs_data_analysis_<dataset_id>.json`，最小 schema：

```json
{
  "dataset_id": "<dataset_id>",
  "region": "USA", "universe": "TOP3000", "delay": 1,
  "fields": [
    {"name": "<field>", "shape": "<分布形状>", "coverage": 0.0,
     "verdict": "accept|reject", "mechanism": "<机制>",
     "downstream_python_hint": "<对 Python alpha 的启示>"}
  ],
  "summary": "<接受/拒绝机制 + 对 Python alpha 的启示>"
}
```

S1 读取方式：`brain-data-feature-engineering` 启动前读本 JSON 作为字段选择输入（路径 = 本文件；字段 = `fields[]` 与 `summary`）。
8. 返回接受/拒绝的机制及对 Python alpha 的启示。

### 增强 + 兜底（MCP 无对应，按触发条件选用）

用 `rtk python3 world-quant-brain-mcp/labs_data_analysis_agent.py ...` 执行（`rtk` = 本机沙箱代理运行器；无 rtk 环境直接用 `$WQ_PY` 等价执行）。**仅当主流程 8 步 MCP 无法覆盖时启用**：

- `emit-notebook-exec` — 增强：把脚本包成单行 `exec(...)` 供 WorkSpaces 远程 notebook 粘贴（避免单元格类型/缩进损坏）。触发条件：MCP `emit_labs_script` 产出需手动粘贴到 notebook 时。
- `emit-summary-cell` — 增强：下载/剪贴板无法回传本机时，在 Labs 内生成紧凑摘要。触发条件：Labs JSON 无法回传本机。
- `ingest --field-meta ... --evolution-review ... --markdown ...` — 增强：增强摄取（补字段元数据、优先级 0 优化闸与 markdown 产物；MCP `ingest_labs_result` 只解析返回 JSON）。触发条件：需要字段元数据/优化闸/markdown 产物时。
- `screen-datasets` — 兜底：仿真前的清单筛查。触发条件：MCP `get_datafields` 无法覆盖时的兜底。
- `demo` — 兜底：无平台原始数据的本地运行时验证。

## 硬规则

- 禁止调用 `submit_alpha`。
- 除非用户明确要求继续进入 S3，本代理内禁止仿真。
- 下游 Python alpha 设计禁止用 VECTOR/GROUP 字段。
- 禁止照抄论坛公式。论坛材料只用于诊断、字段方向、失败模式与预处理线索。（论坛材料由 `brain-forum-browse` 产出；本 skill 无论坛工具、不自行检索论坛。）
- 最终推荐必须是一个机制、至多两个 MATRIX 字段——这是**候选方向**（供 S1 参考），**不是最终字段拍板**（最终字段由 S1 `brain-data-feature-engineering` 决定，本 skill 不选最终字段）。
- **WebDataScope 体检交叉验证（2026-08-05 新增）** — Labs 原始数据分析的结论（覆盖/缺失/分布/离群值）应与 WebDataScope 离线体检数据包交叉验证：**执行方 = 本 skill**，用本地 Bash 运行 `python tools/webdata_quality.py --fields <ds>`（路径 = 仓库根 `tools/webdata_quality.py`）读取离线快照。两者覆盖率和分布形状判定一致时高置信；不一致时**以 Labs 实时数据为准**（体检数据包是 2012-2021 离线快照），并**在产物 JSON 的 `summary` 中标注「交叉验证不一致」及原因**。从 Labs 分析衍生的表达式在提交前必须通过 `check_expr_against_inspect` 体检硬门校验（见 [`../wq-brain-ra-pipeline/SKILL.md`](../wq-brain-ra-pipeline/SKILL.md) 步 5）。

## 默认示例

`USA TOP3000 D1 imbalance5`：检查 `imb5_score` 和 `imb5_mktcap`。
把 `imb5_score` 当主信号（石油冲击韧性分数），`imb5_mktcap` 当上下文。除非 Labs 显示水平值**异常稳定**（跨期均值漂移 < 10%、离群值占比 < 5%，即分布形状判定为 `spread` 且无 `point_mass`/`concentrated`）且**不拥挤**（该数据集 `alphaCount ≤ 50`），否则优先做状态切换或意外抽取，而非原始分数水平。
