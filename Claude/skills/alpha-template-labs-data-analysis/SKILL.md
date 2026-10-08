---
name: alpha-template-labs-data-analysis
layer: L0
description: "要在 Brain Labs 里用 Python 做原始数据分析（覆盖 / 缺失 / 频率 / 离群 / 相关性）时使用：为 USA/TOP3000/D1 的 MATRIX 数据集生成 Labs 脚本、回收结果，给出 Python 原生抽取机制。触发词：Labs 分析 / 原始数据分析 / labs data analysis / Python alpha 设计前置。Python 轨道，不进 FASTEXPR 提交路径。"
last_verified: 2026-10-08
user-invocable: true
allowed-tools:
  - Read
  - Bash
  - mcp__wq-brain-http__*
---

# /alpha-template-labs-data-analysis

## 职责边界

- **本 skill 负责**：Brain Labs 里的原始数据分析——覆盖 / 缺失 / 更新频率 / 离群值 / 分布 / 字段相关性诊断，并把发现转成**一个** Python 原生抽取机制（至多两个 MATRIX 字段）。
- **本 skill 不做**：不开战役、不选最终字段、不回测、不提交、不写 DB / 台账；**不替代 S1 体检**（`tools/webdata_quality.py` / `tools/field_inspect_gate.py`）。
- **上游 / 下游**：上游 = 用户的 Labs 账号（脚本只能在 Labs 里由人运行）+ MCP Labs 工具；下游 = 用户的 Python alpha 设计。对 RA 流水线只有「线索」一种衔接（见下节）。

规范细节（输入 / 输出契约、字段形态分类）见 [references/agent-spec.md](references/agent-spec.md)；分析引擎 = `world-quant-brain-mcp/labs_data_analysis_agent.py`。

## 与 REGULAR 流水线的关系

| 问题 | 答案 |
|---|---|
| 这是哪条轨道？ | **Python alpha 轨道**（在 Brain Labs 用 Python 写的 alpha）。RA 流水线只产 **FASTEXPR REGULAR** alpha，两条轨道的产物不能互换 |
| 结论能指导 FASTEXPR 表达式吗？ | 只作**线索**：字段的覆盖 / 频率 / 分布形态可以旁证 S1 字段语义分类，供 agent **手工**参考；不自动进任何台账，不改变 RA 的任何闸 |
| 能进入提交路径吗？ | **不能**。本 skill 不产出可仿真的 alpha，也不调用任何提交接口 |
| 从 Labs 结论衍生了 FASTEXPR 表达式怎么办？ | 当成一条新的外部 idea 走入库通道（`brain-inspect-raw-template-create-setting`），再按 RA 流水线照常过闸；体检硬门在 RA 步 5 由 `wave_gate` 自动做，单独自查用 `python tools/field_inspect_gate.py --region USA --dataset <ds> --exprs-file <txt>` |

## 流程

认证 / 生成脚本 / 摄取三步优先用 MCP Labs 工具（Labs 账号只有**一个**交互会话，工具在单并发锁后面）；MCP 未覆盖的步骤才用本地 CLI（见「CLI 专用步骤」）。

**1. 只拉 MATRIX 字段（无需 Labs 登录）**

```python
mcp__wq-brain-http__get_datafields(
    dataset_id="<dataset_id>", region="USA", universe="TOP3000", delay=1,
    data_type="MATRIX", filter_sharpe=False,
)
```

**2. 【需用户同意】仅当确需新 Labs 会话时才登录**

新开会话会占用账号唯一的交互会话（可能挤掉用户正在用的那个），所以**先问用户，用户同意才调用**：

```python
mcp__wq-brain-http__authenticate_brainlabs()   # -> {status, workspaces_url, labs_url, token, note}；请用户打开 workspaces_url
```

登录凭据由 MCP 服务从环境读取（`CREDENTIALS_EMAIL` / `CREDENTIALS_PASSWORD`）；agent 不读 `.env`、不打印凭据（AGENTS.md）。返回里的 `token` 不要写进任何文件或回复。

**3. 生成可粘贴的 Labs 脚本（至多两个 MATRIX 字段）**

```python
mcp__wq-brain-http__emit_labs_script(
    dataset_id="<dataset_id>", fields=["<field_a>", "<field_b>"],
    region="USA", universe="TOP3000", delay=1,
    labs_output="/tmp/labs_data_analysis_<dataset_id>_raw.json",
)
```

`labs_output` 是**Labs 里（Linux JupyterLab）**的路径，不是本机路径，`/tmp/…` 是对的。分析引擎缺省随包（`LABS_AGENT_SCRIPT` 可覆盖）。

**4. 【人工 · 在此暂停】用户在 Labs 里运行脚本并回传结果**

这一步只能由**人**在浏览器里完成。agent 在这里停下，对用户说明：「请在 Labs 里粘贴并运行上面的脚本，然后把 `<labs_output>` 里的 JSON **内容**贴回来（或给我本机文件路径）」。**在收到 JSON 之前不得继续，也不得编造任何 Labs 数据。**

**5. 摄取结果**

```python
mcp__wq-brain-http__ingest_labs_result(result_json="<JSON 字符串或本机文件路径>")
```

该工具**只解析并返回** JSON，不落盘。解析失败返回 `{"error": "Could not parse Labs result JSON: …"}`——让用户重新导出，不要手改 JSON。

**6. 分类数据形状与下游 Python 适用性**

按引擎的 `field_classification`（`binary_or_categorical` / `low_frequency_step` / `dense_bounded_score` / `sparse_event` / `ratio_or_scale_sensitive` / `dense_continuous`）逐字段判断，各类的抽取倾向见 [references/agent-spec.md](references/agent-spec.md)。

**7. 落盘（可选，一次性产物）**

需要留档时用 CLI `ingest`（见下）合并元数据、生成 markdown；建议 `--output tracking/_scratch/labs_<dataset_id>.json`（`tracking/_scratch/` 不入版本库）。**这个 JSON 是一次性分析输出：不是战役产物、不入 DB、下游不读取**——与「DB 是真相源、不写战役 JSON」不冲突；缺省路径 `tracking/runs/…` 会被 git 跟踪，别用。 <!-- lint:counterexample: 该目录为工具的**缺省输出位**（文档劝阻使用），并非已存在的战役目录 -->

**8. 按下面的格式回报**

```
## <dataset_id> Labs 分析结论（USA/TOP3000/D1）
| 字段 | 形态（field_classification） | 覆盖（mean） | 关键诊断 | 接受 / 拒绝 | 理由（一句话，点名依据的诊断） |
|---|---|---|---|---|---|
| imb5_score | dense_bounded_score | 0.91 | 有界 0–1 分数；水平值拥挤 | 接受（作主信号） | 有界分数水平值不稳定，改抽「状态切换 / 相对基线的意外」 |
| imb5_mktcap | dense_continuous | 0.93 | 直接市值数据 | **拒绝（仅作诊断）** | 命中「直接市场数据」合规约束，不进设计；只用它看 imb5_score 是否是市值代理 |

机制（一个）：<一句话>；主信号 = <字段>；辅助（至多一个非价量 MATRIX 字段，可无）= <字段>；Python 抽取 = <骨架>
对 RA 流水线的线索（可无）：<一句话，注明这只是线索>
```

### CLI 专用步骤（MCP 没有对应）

统一用 MCP venv 解释器：`& $WQ_PY world-quant-brain-mcp/labs_data_analysis_agent.py <子命令> …`（`$WQ_PY` 的解析见 AGENTS.md）。

| 子命令 | 用途 |
|---|---|
| `emit-notebook-exec --script <file>` | 把脚本包成单行 `exec(...)` 供 WorkSpaces 远程 notebook 粘贴（避免单元格类型 / 缩进损坏） |
| `emit-summary-cell --labs-output <path>` | 下载 / 剪贴板无法回传本机时，在 Labs 内生成紧凑摘要 |
| `ingest --labs-json <file> [--field-meta … --evolution-review … --markdown … --output …]` | 增强摄取：补字段元数据、合规约束检查、优化计划、markdown 产物 |
| `screen-datasets --datasets-json … --output …` | 仿真前的兜底清单筛查 |
| `screen-os-clues --clues-json … --output …` | 按合规约束筛查低 SelfCorr / 高 ProdCorr 的 OS 线索 |
| `run-csv` / `demo` | 本地 CSV 分析 / 无平台数据的合成数据运行时验证 |

## 硬规则

- 禁止调用 `submit_alpha`；除非用户明确要求继续进入 S3，本代理内禁止仿真。
- **引擎内置合规约束（Python 轨道）**：拒绝价量字段（`pv*` 数据集、成交量 / VWAP 等）与直接市场数据字段（价格 / 收益 / 市值 / 股本 / 成交量）——命中即标 `diagnostic_only`，并写 `direct_market_data_fields_forbidden`。这类字段可作**诊断对象**，不得进入 alpha 设计。
- 下游 **Python alpha** 设计不用 VECTOR / GROUP 字段。这是**仅 Python 轨道**的限制；FASTEXPR 轨道用 `vec_*` 处理 VECTOR、用 `group_*` 处理 GROUP（见 ra-pipeline / GEM），二者不矛盾。
- 禁止照抄论坛公式。论坛材料只用于诊断、字段方向、失败模式与预处理线索。
- 最终推荐必须是**一个机制、至多两个 MATRIX 字段**。
- **WebDataScope 体检交叉验证**：Labs 的覆盖 / 分布结论应与离线体检数据包交叉验证——`python tools/webdata_quality.py --zip research-data/WebData_20260219_V0.10.9 --region USA --delay 1 --fields <ds>`。两者一致 → 高置信；不一致 → **以 Labs 实时数据为准**（数据包是 2026-02-19 打包的离线快照，逐字段体检只覆盖 2012–2021 十年，新近变化它看不到）。

## 默认示例

`USA TOP3000 D1 imbalance5`：检查 `imb5_score`（油价冲击韧性分数，0–1 有界）与 `imb5_mktcap`。

- `imb5_score` = 主信号。除非 Labs 显示水平值异常稳定且不拥挤，否则优先做**状态切换**或**相对基线的意外**，而不是原始分数水平；骨架：最新有效值回填 → 一次有界分数转换 / 基线意外 → 单次截面中心化或 rank → universe pasteurization。
- `imb5_mktcap` = 直接市值数据，被引擎的合规约束排除：**只用它做相关性诊断**（看 `imb5_score` 是否只是市值的代理），**不做**市值残差化、市值分桶或加性市值暴露。
- 只有一个字段值得入选时，机制就是「score-only」，这是允许的。
