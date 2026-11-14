# ★更正：toolkit 静态闸没有 bug，变量赋值可用

日期：2026-11-12

## 我此前的错误判断

我曾在 `OPCOUNT_SOLUTION_20261112.md` 写下：
> 「toolkit 静态闸不支持变量赋值：`[SYNTAX] 函数 group_zscore 最多接受 2 个参数，但提供了 3`，原因：闸把分号 `;` 当参数分隔符解析」

**这是错的。** 实测三次：

| 测试 | 表达式 | 结果 |
|---|---|---|
| T1 | `h=vec_avg(X);a=group_rank(ts_ir(h,66),sector);signed_power(group_zscore(a,sector),1.3)` | ✅ 通过 |
| T2 | `h=vec_avg(X);a=...;b=...;signed_power(group_zscore(add(a,b),sector),1.3)` | ✅ 通过 |
| T3（BE154 全量 28 算子版）| 完整变量合并版 | ✅ 通过 |

**真实原因**：那次失败是我自己写错了——在 `group_zscore(...)` 里漏了一个右括号，导致参数解析把内层的 `add(...)` 拆成了第 3 个参数。**是真实语法错误，闸报得对。**

## 结论（修正后）

| 手段 | 可行性 | 收益 |
|---|---|---|
| **变量赋值去重** `h=...;a=...(h);...` | ✅ **可用**（走 multisim 或 batch_create 均可）| 本族 **−18 算子** |
| **n 元 add** | ✅ 可用 | −7 算子（实测零损失）|
| **删外层 signed_power** | ✅ 可用 | −1 算子（实测还白赚 F/sub）|
| `preflight_expressions` 把变量名报 unknown_fields | ⚠ **误报**，只认字段不认变量 | 忽略 |

## 变量赋值语法规范（实测）

```
h=vec_avg(insd1_holdings);a=group_rank(ts_ir(h,66),sector);<最后一行是输出表达式>
```
- 用分号 `;` 分隔语句，最后一条即 alpha 输出
- **赋值语句本身不占算子数**（已验证：变量前后平台 operatorCount 差 = 被消掉的重复次数）
- 平台返回 `ok` 且仿真实际推进，语法被接受

## 踩坑记录：batch_create_simulations 会改 nanHandling

BE153 用 `batch_create_simulations` 派三档，全部产出 `nanHandling: OFF`（我传 ON）：
```
GrmPW8RO  nan=OFF  S 0.42  longCount 12   （全量变量合并版，真实应 2.36）
LLKWMgWv  nan=OFF  S 0.52  longCount 13   （纯ins变量合并版）
```
⇒ **变量合并的压缩效果必须用 `create_multi_simulation`（settings 可信）重测**，BE154 已如此派发（`4jGOvg5dg53iceXQUk71NBD`）。
⇒ 这两颗作废，读数不进台账。
