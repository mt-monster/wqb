---
last_verified: 2026-09-28
name: alpha-expression-verifier
description: "校验 alpha 表达式的语法（不关心字段是否存在）。当需要检查 alpha 表达式字符串的语法是否合法、函数参数是否正确、括号是否匹配时使用。仅限语法层面；战役级预检（字段/类型/毒化）见 wq-brain-campaign-toolkit。"
layer: L2
allowed-tools:
  - Bash
---







**运行环境**：所有 Python 命令使用 MCP venv（`$WQ_PY`），确保依赖（requests/pandas/ply）可用。不要使用系统 Python。

# 表达式校验器（Expression Verifier）

## 职责边界

- **本 skill 负责**：**纯语法层**校验：括号匹配、算子元数、函数参数合法性
- **本 skill 不做**：不做战役层字段校验与 8 闸门禁（`wq-brain-campaign-toolkit/scripts/gate.py`）；不生成表达式、不回测；**不判定该字段在平台是否可用**
- **上游 / 下游**：上游 = 表达式文本；下游 = 人工核对或 GEM 生成侧预检



本 skill 使用项目自带的 `ExpressionValidator` 校验数学/逻辑表达式的语法。

它执行以下检查：
1. **词法分析（Lexical Analysis）**：识别合法 token（算子、函数、变量）。
2. **语法分析（Syntax Analysis）**：校验具体语法规则。
3. **函数校验（Function Validation）**：检查所支持函数（如 `group_sum`、`rank`）的参数个数与类型。
4. **括号匹配（Parenthesis Matching）**。

**注意**：本 skill **不**校验表达式中引用的数据字段（变量）在数据库中是否存在，只检查它们是否以合法标识符形式使用。

`densify()` 允许以字段标识符输入原生 GROUP 分组轴（例如客户网络簇）；其输出仍是分组键，不能交给 `rank()` 等数值信号参数使用。字段存在性与平台类型判定不在本层，见下方「边界说明」。

## 使用方法

按以下步骤校验表达式：

1. **定位脚本**：校验脚本为本 skill 目录下的 `scripts/verify_expr.py`。
   * **上下文检查**：由于 agent 运行在用户项目目录下，`scripts/` 可能不在当前路径中。
   * **主路径（Windows）**：`$WQ_VALIDATOR_DIR/verify_expr.py`。
   * **注意**：skill 目录名是 `alpha-expression-verifier`（**不是** `expression_verifier`）。早期文档中引用 `.claude` 或裸名 `expression_verifier` 的写法都是错的。

2. **执行**：用 `$WQ_PY` 运行脚本，务必用引号包裹表达式以处理空格和特殊字符。

```bash
# 示例（按需调整路径）
$WQ_PY "$WQ_VALIDATOR_DIR/verify_expr.py" "ts_rank(close, 10)"
```

## 解读结果

脚本输出一个 JSON 对象。
- 若 `valid` 为 `true`，表达式语法正确。
- 若 `valid` 为 `false`，查看 `errors` 列表获取详情。

## 示例

### 校验合法表达式
```bash
$WQ_PY "$WQ_VALIDATOR_DIR/verify_expr.py" "rank(close) / ts_delay(open, 5)"
```

### 校验非法表达式
```bash
$WQ_PY "$WQ_VALIDATOR_DIR/verify_expr.py" "rank(close) / ts_delay(open, 5"  # 括号不匹配：少一个右括号
```

## 边界说明：仅语法层面，战役级预检另见其他 skill
本 skill 只验语法。**字段白名单 / 类型（VECTOR 须 `vec_*` 包裹）/ 不可访问算子（`ts_min`/`ts_max`）/ `quantile` 仅 1 参 / banned+poison 正则** 属战役级 preflight，走 `wq-brain-campaign-toolkit` 的 `gate.py`（5 闸 + sha1 缓存）。`quantile` 签名表允许 1–3 参是语法事实，战役纪律"仅 1 参"由 gate 闸4 在本层加严。**不要改 `validator.py`（1363 行巨石）**：当发现"语法允许但战役禁止"的差异（如 `quantile` 多参）时，正确做法是把该纪律上报到 `wq-brain-campaign-toolkit` 的 gate 闸规则，而非把战役纪律硬编码进语法校验器——否则语法层与战役层职责混叠，后续任何战役规则调整都会污染语法事实。
