---
last_verified: 2026-09-29
name: alpha-expression-verifier
description: "检查一条 alpha 表达式字符串的语法是否合法（括号匹配、函数是否存在、参数个数）时使用。只看语法，不关心字段是否存在或类型对不对；战役级预检（字段 / 类型 / 毒化）走 wq-brain-campaign-toolkit 的 gate.py。"
layer: L2
allowed-tools:
  - Bash
---

# 表达式校验器（Expression Verifier）

## 职责边界

- **本 skill 负责**：**纯语法层**校验——词法（合法 token）、语法（能否解析）、函数校验（函数存在、参数个数）、括号匹配。
- **本 skill 不做**：不判定字段在平台是否存在或类型是否匹配；不做战役层的 8 闸 + 闸 0（`wq-brain-campaign-toolkit/scripts/gate.py`）；不生成表达式、不回测。
- **上游 / 下游**：上游 = 表达式文本；下游 = 人工核对，或 `gate.py` 的闸 1（语法，直接 import 本 skill 的 `ExpressionValidator`，不走子进程）。

`densify()` 允许以字段标识符输入原生 GROUP 分组轴（例如客户网络簇）；本层无法仅凭字段名确认平台类型。它的输出仍是分组键，**不能**交给 `rank()` 等数值参数；字段存在性与平台类型须继续过战役门禁。

## 使用方法

用 MCP venv 的解释器（`$WQ_PY`，含 `ply`；不要用系统 Python）。**在仓库根运行**，表达式用引号包住（处理空格与特殊字符）：

```powershell
& $WQ_PY Claude/skills/alpha-expression-verifier/scripts/verify_expr.py "rank(close) / ts_delay(open, 5)"
```

- skill 被同步到宿主目录（如 `~/.claude/skills/…`）后，用 `$WQ_VALIDATOR_DIR`（= 本 skill 的 `scripts` 目录）代替上面的仓库相对路径：`& $WQ_PY "$env:WQ_VALIDATOR_DIR/verify_expr.py" "<表达式>"`。`gate.py` 用同一个变量；未设时按 `wq-brain-campaign-toolkit/scripts/_lib/skill_roots.py` 的顺序找。
- 依赖见 `requirements.txt`（`ply`）。

## 解读结果

脚本输出一个 JSON 对象：`valid`（布尔）、`errors`（字符串列表）、`tokens`、`ast`。

> **退出码不表示合法与否**：表达式非法时脚本照样以 **0** 退出、`valid=false`。只有「没传表达式 / 找不到 `validator.py` / 校验过程抛异常」才以 **1** 退出（同样输出带 `errors` 的 JSON）。调用方**必须解析 `valid`**，不能只看退出码。

## 示例（真实输出，`tokens` / `ast` 已省略）

| 表达式 | `valid` | `errors` |
|---|---|---|
| `rank(close) / ts_delay(open, 5)` | `true` | `[]` |
| `rank(close` | `false` | `["语法错误: 表达式不完整", "无法解析表达式", "括号不匹配: 左括号过多"]` |
| `ts_mean(close)` | `false` | `["函数 ts_mean 需要至少 2 个参数，但只提供了 1"]` |
| `ts_mean(close, 5, 3)` | `false` | `["函数 ts_mean 最多接受 2 个参数，但提供了 3"]` |
| `foo_bar(close, 5)` | `false` | `["未知函数: foo_bar"]` |
| `rank(close, 5)` | `true` | `[]`（`rank` 允许第 2 个参数——平台的 `rate` 排序精度，**不是窗口**；语法合法不代表语义是你想要的） |

## 常见错误

| 现象 | 含义 | 处理 |
|---|---|---|
| `errors` 含「未知函数: X」 | 算子名不在校验器的签名表里（拼错、幻觉算子、平台不支持的算子） | 对照 `mcp__wq-brain-http__get_operators` 的算子清单改；不要靠「加进签名表」放行 |
| `errors` 含「需要至少 / 最多接受 N 个参数」 | 元数错误 | 按签名表补 / 删参数 |
| `errors` 含「括号不匹配」 | 括号数量或位置错 | 逐层数括号 |
| 输出 `Error importing validator module: …` 且退出码 1 | `validator.py` 不在脚本同目录，或缺依赖 `ply` | 确认用 `$WQ_PY`；`pip install -r requirements.txt` 到该 venv；不要用系统 Python |
| 输出 `No expression provided` 且退出码 1 | 没传表达式 | 传引号包住的表达式 |
| 语法通过但战役里仍被拒 | 语法层之外的问题（字段不存在 / VECTOR 未包 `vec_*` / 毒化 / `quantile` 参数纪律） | 走 `gate.py`：`python Claude/skills/wq-brain-campaign-toolkit/scripts/gate.py --help` |

## 边界说明

- 校验器的签名表反映**语法事实**：例如 `quantile` 允许 1–3 个参数；战役纪律「仅 1 参」由 `gate.py` 的闸 4 在本层之上加严。
- **改 `validator.py` 是变更纪律问题**（该文件同时被 `gate.py` 闸 1 与 GEM 生成侧预检直接 import，改动影响面广）：先读 AGENTS.md 的变更影响面，改后必须跑 `tests/` 里覆盖 `gate` 与 `validator` 的用例。
