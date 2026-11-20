# EUR 派发纪律（dispatch-discipline）

> **as_of**：2026-11-20 ｜ 来源：EUR 未点亮塔会话（earningscall 66 臂 / investor_activity 88 臂 / macro27 39 臂 / institutions 24 臂）
> **定位**：与 [`settings-axis-strategy.md`](settings-axis-strategy.md)（设置轴）正交——那份管**跑什么设置**，这份管**怎么派**。

## 1. 两种批次失败形态（平台实测，处置相反）

| 形态 | 触发条件 | 平台表现 | 槽位损失 | 处置 |
|---|---|---|---|---|
| **A 编译期连坐** | 幽灵算子 / 元数违规 / 命名参数违规 / 字段非法 | 父 multisim 状态 **ERROR**；出错条 ERROR、**其余全部 CANCELLED** | **整批** | 静态闸拦（形态 A 全部静态可判）；已成批 → `tools/backtest/batch_isolate.py` 二分隔离 |
| **B 运行期逐条** | 量纲（UNITS）/ 算子语义错 | 该条 WARNING/FAIL，**其余照常出 alpha** | 单条 | 读该条 error 修正后单独重投 |

> 实测原文（2026-11-20，EUR/TOP2500，2 臂批）：
> 好臂 `CANCELLED` + 坏臂 `ERROR: Attempted to use inaccessible or unknown operator "ts_max"`。

## 2. 派发分层（新算子/新字段 ⇒ 先小批探）

**规律**：**首次出现的算子 / 字段 / 参数组合 = 编译期高风险**（平台编译期才发现的问题，本地未验证 ⇒ 高风险）。

| 风险级 | 判据 | 批大小 |
|---|---|---|
| 高 | 含**新**算子 / **新**字段 / **新**参数组合 / VECTOR 字段首次使用 | **1~2 条一批**先探，探通再并入大批 |
| 中 | 已验证算子 + 已验证字段，但**新组合** | 2~3 条 |
| 低 | 已在同批/同族跑通过的表达式 | 可放大到 8~10 条 |

> ⚠ **与「同类别算子全替换」规则的冲突解法**：全替换批**必然含未验证算子** ⇒
> **逐层小批**（每层 2~3 条），而不是整层 8~10 条一批。
> 否则一条编译期错误会**连坐整层**（10 个槽位净损失）。

## 3. 派发前的本地闸（零槽位成本）

| 闸 | 位置 | 拦什么 |
|---|---|---|
| toolkit 静态闸 | `tools/wave_gate.py` → toolkit `gate.py` | 语法、元数、命名参数、幽灵算子、裸 VECTOR、调用点数 ≥10 |
| MCP 直发闸 | `create_multi_simulation`（tools_sim `_toolkit_gate_check`） | 语法 / inaccessible_ops / 毒模式 **＋**（2026-11-20 补）算子存在性、元数、命名参数、调用点数 |
| `preflight_expressions` | MCP | 字段存在性 + VECTOR 自动包裹 |

**⚠ catalog 的默认值标注 ≠ 平台可省略**：`ts_target_tvr_decay/hump` 的 `target_tvr` 在平台侧**必填**
（catalog 写 `target_tvr=0.1`），缺它平台报 `Required attribute "target_tvr" must have a value.`
并连坐整批 ⇒ 已在 `op_arity._REQUIRED_NAMED_ARGS` 登记。

## 4. 收批后必须核对每条子任务状态

- 父状态 ERROR + 子任务含 **CANCELLED** ⇒ 形态 A ⇒ `tools/backtest/batch_isolate.py --dispatch`（只重投好臂）；
- 子任务逐条 WARNING/FAIL 且无 CANCELLED ⇒ 形态 B ⇒ 读该条 error 修正后**单独**重投，**不要**重发整批。

## 5. 平台口径备忘（读数坑）

- `GET /simulations/{id}` 的 `children` 是**子任务相对路径**（`/simulations/<id>`），须逐个再 GET 才拿到 status；
- **单条**提交的响应**没有 children**，状态在顶层 ⇒ 判单条成败必须读顶层 `status`（否则坏臂会被误判为干净）；
- 平台不接受 n=1 的**数组**包裹（须发裸 dict）；n≥2 才发数组。
