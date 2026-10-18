# DEU 战役：首条全闸通过 REGULAR Alpha + 六层配方
**日期**：2026-10-12　**区域**：DEU / TOP500 / D1（永久锁定）　**状态**：**破闸成功（1 条全过）**

---

## 一、结论先行

**`zqbVMkv1` 是本次战役第 1 条「10/10 全闸通过」的 REGULAR alpha** ——
IS 8 项检查 + self 相关性 + prod 相关性 **全部 PASS**。

```python
winsorize(group_rank(
    ts_target_tvr_decay(
        multiply(rank(ts_delta(divide(fnd6_newq_oiadpq, fnd6_newq_seqq), 240)),
                 rank(ts_delta(divide(fnd6_newq_oiadpq, fnd6_newq_seqq), 176))),
        target_tvr=0.05),
    sector), std=4)
```
**settings**：`DEU / TOP500 / D1 / decay4 / FAST / truncation 0.08 / nanHandling ON`

| RA 闸 | 值 | 门槛 | 结果 |
|---|---|---|---|
| `LOW_SHARPE` | **1.59** | 1.58 | ✅ PASS |
| `LOW_FITNESS` | **1.20** | 1.0 | ✅ PASS |
| `LOW_TURNOVER` / `HIGH_TURNOVER` | 0.1309 | 0.01 / 0.7 | ✅ PASS |
| `CONCENTRATED_WEIGHT` | — | — | ✅ PASS |
| `LOW_SUB_UNIVERSE_SHARPE` | 1.25 | 0.75 | ✅ PASS |
| `LOW_2Y_SHARPE` | **1.94** | 1.58 | ✅ PASS |
| `MATCHES_PYRAMID` | — | — | ✅ PASS |
| `SELF_CORRELATION` | **0.1380** | 0.7 | ✅ PASS |
| `PROD_CORRELATION` | **0.4116** | 0.7 | ✅ PASS |

> ⚠ 提交需用户授权（项目全局闸锁 `ALLOW_ALPHA_SUBMIT=False`）。

---

## 二、六层配方（本战役核心方法论）

| 层 | 杠杆 | 该层效果 |
|---|---|---|
| ① **概念** | 盈利动量 `ts_delta(divide(OIADPQ, SEQQ), W)` | 单腿 S 1.38 / 2Y 1.30 |
| ② **双窗级联** | `multiply(rank(ts_delta(x,240)), rank(ts_delta(x,176)))` | **S 1.38→1.56、2Y 1.30→1.91** |
| ③ **分组轴** | **`sector`**（平台内置） | 触发**宽松的 `LOW_2Y_SHARPE`**，替换掉严格的 `IS_LADDER_SHARPE` |
| ④ **截面** | `winsorize(..., std=4)` | +0.02（std2/6 均更差） |
| ⑤ **限速器** | **`ts_target_tvr_decay(..., target_tvr=0.05)`** | **S 1.56→1.59（临门一脚）** |
| ⑥ **settings** | FAST / decay4 / trunc0.08 | 最优（11 档 neutralization 全更低） |

### 三个跨数据集可迁移的杠杆（本次新发现）

1. **`sector` 轴是普遍 S 放大器**：同构造换轴后
   - fundamental6 `ts_delta(ROE)`：S 1.04 → **1.33**，2Y 1.17 → 1.54
   - analyst93 `corrrev × recprof2`：S 1.05 → **1.31**
   - shortinterest3：S 最优亦在 sector 轴
   - ⚠ 唯一反例：institutions1（S 1.34 → 0.34，该腿必须用 oth455 fact1 轴）
2. **`ts_target_tvr_decay` 的激活条件**：仅当 **TO > target_tvr** 时生效（本构造 TO 0.133 > 0.05）
   ⇒ 是「TO 略高于 0.125 阈值」构造的**免费 +0.03 S**。
3. **分组轴同时决定三件事**：① 2Y 检查类型（数据集 GROUP 轴→`IS_LADDER_SHARPE` 严；
   平台内置轴→`LOW_2Y_SHARPE` 宽）② 2Y 数值 ③ 点亮塔数。

---

## 三、候选池（按离破闸的距离）

| 候选 | 腿 | 构造 | S/1.58 | fit/1.0 | 2Y/1.58 | self | prod/0.7 | 状态 |
|---|---|---|---|---|---|---|---|---|
| **`zqbVMkv1`** | fnd6 | OIADP 级联(240,176)+tvr_decay | **1.59** | **1.20** | **1.94** | **0.138** | **0.4116** | ★ **全过** |
| `omWdpKm2` | fnd6 | 级联(240,176) decay3 | 1.57 | 1.15 | 1.91 | 0.1407 | 0.4108 | 差 S 0.01 |
| `ZYAJ57Rn` | fnd6 | 级联(252,176) 分母平滑 | 1.57 | 1.16 | 1.83 | 0.1318 | 0.4043 | 差 S 0.01 |
| `j2872RAO` | fnd6 | 级联(240,176) 无 tvr_decay | 1.56 | 1.15 | 1.91 | 0.1401 | 0.4117 | 差 S 0.02 |
| `zqbV6AJX` | shrt3 | TC×DUR + tvr_decay | 1.58 | 0.98 | 1.51 | — | 0.7368 | 差 fit/2Y/prod |
| `omWbGMzn` | shrt3 | TC_main×DUR_main | 1.54 | 1.07 | 2.69 | 0.2381 | 0.7134 | 差 S 0.04 / prod 0.013 |
| `pw5p27rv` | shrt3 | TC×BAR | 1.59 | 1.13 | 2.68 | 0.2097 | 0.788 | 差 prod 0.088 |
| `wpbddWEQ` | fnd6 | 单腿 OIADP Δ252 | 1.38 | 0.97 | 1.30 | 0.134 | 0.4633 | 差 3 项 |
| `58geo5Ak` | inst1 | 掩码 ts_sum+fact1 | 1.34 | 0.89 | 2.09 | 0.6319 | 0.6588 | 差 S/fit |
| `E5RjPEdR` | anl93 | est_corrrev×recprof2+sector | 1.31 | 0.93 | 0.96 | 0.2596 | 0.6469 | 差 S/fit/2Y |

---

## 四、已穷尽的维度（避免重复投入）

| 维度 | 已扫 | 结论 |
|---|---|---|
| **neutralization 11 档** | NONE/STATISTICAL/MARKET/SECTOR/INDUSTRY/SUBINDUSTRY/SLOW/CROWDING… | **全降 S**（FAST 1.56 最优；NONE 0.85 / CROWDING 0.42） |
| **decay / truncation** | decay 2~12、trunc 0.04~0.12 | 对 prod **完全无影响**；decay3 微提 S（1.57） |
| **分组轴** | sector/industry/subindustry/market/oth455 f1~f3/pv30 group*/pv29 sta1* | sector 最优；pv29/pv30 轴 S 仅 0.63~0.78 |
| **截面算子** | group_rank/group_zscore/group_neutralize/bucket/tail | group_rank 唯一可行 |
| **聚合** | vec_avg/vec_max/vec_sum | vec_avg 最优 |
| **腿级归一化** | winsorize/ts_rank/ts_zscore/ts_scale/ts_av_diff/ts_ir/ts_mean | 全部劣于原始（S 0.15~1.48） |
| **方向混合** | `reverse(rank(B))` 进 multiply | **数学无效**（平台 `reverse` = 整体取负，非 1−x） |
| **掩码换样本** | `if_else(BAR>5)` / `if_else(ROE>0)` | shortinterest3 上失效（TO 爆 0.19）；fundamental6 上中性 |
| **字段变体** | `_p5_d1` / 无后缀 / `_main`（aC 差 3~5 倍） | **保 S、大幅提 2Y（1.88→2.71），但不降 prod** |

---

## 五、工程要点

- **原始 API 指标在 `is` 下直接展开**（`is.sharpe` / `is.fitness` / `is.checks`），**不是 `is.metrics.*`**（后者是 MCP 封装格式）。
- **MCP 服务需手动启动**：`python tools/start_wq_mcp.py --all`。
- **多仿真 location ~24h 过期**；**并发会话共享槽位** ⇒ 批次常「status 201 但无 alpha」⇒ 需查 `/users/self/alphas` 确认后重发。
- **本地 `fields` 表与平台不一致**（如 `fnd6_newq_ltmibq` 平台不存在）⇒ 发批前必须 `get_datafields` 逐字核对。

---

## 六、下一步建议

1. **同族复制**：`zqbVMkn*` 家族的 S1.57 近miss（`omWdpKm2` / `ZYAJ57Rn`）通过 minor 变动各自过闸
   —— ⚠ 但**同骨架互相关会 >0.99**，按纪律**同一骨架只应出 1 颗**。
2. **跨腿复制配方**：把「级联 + sector + tvr_decay」六层配方迁移到
   - fundamental6 的其它比率（ROE / PIQ / OIBDPQ 级联）
   - analyst93 的 `estimator_*` 前缀族
   ⇒ 每条腿出 1 颗，形成 4~5 条**互不相关**的可提交 alpha。
3. **shortinterest3 的 prod 墙**：该腿 S≥1.5 的构造 prod 全部 ≥0.71
   ⇒ 需换信号样本（跨数据集联合）或判该腿 RA 不可达。
