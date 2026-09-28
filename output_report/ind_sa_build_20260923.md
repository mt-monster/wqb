# IND SuperAlpha 构建与提交（2026-09-23）

## 结论

**成功**：新 IND SuperAlpha **`MPaGzEx8`**（name `IND_S_p0688_GzEx8`）已 **ACTIVE / stage=OS**
（submitted 2026-09-23T02:44:19-04:00），全部闸门 PASS，并带 `CLUSTER:CLUSTER` 徽章。
今日 SUPER 配额 1/1 用掉（REGULAR 2/4）。

## 硬前置核对

| 项 | 结果 |
|---|---|
| IND ACTIVE 总数 | **27**（23 REGULAR + 4 SUPER）→ 组件 ≥10 ✅ |
| 既有 IND SA（需低相关）| `QPbjxMYw`(20comp) / `wpjrMnz5`(10comp) / `gJjN80rm`(10comp) / `E5l23mrm`(10comp) |
| 既有配方基线 | TOP500/d1；decay ∈ {5,30,90}；nu ∈ {STATISTICAL×3, SUBINDUSTRY×1}；combo=(1−maxCorr)^5（3 颗）或 1−maxCorr |

## 变体设计与模拟结果

三变体均在 IND / TOP500 / d1 / trunc0.08 / maxTrade OFF 下，差异在中性化・decay・评分门・combo：

| 变体 | 配方 | IS Sharpe | Fitness | tvr | self 探针 | prod 探针 | 判定 |
|---|---|---|---|---|---|---|---|
| **V1** | **SUBINDUSTRY / decay10 / score=`1.0−prod` / gate self<0.6 / combo 线性 `1−maxCorr`** | 4.16 | 4.86 | 0.154 | **0.6875** | **0.6879** | ✅ **可提交** |
| V2 | SUBINDUSTRY / decay5 / score=`0.8−prod` / gate self<0.55 / combo 线性 | 4.10 | 4.42 | 0.176 | 0.7650 | 0.7647 | ❌ 双闸超线 |
| V3 | STATISTICAL / decay15 / 硬门 `prod<0.65` / combo `(1−maxCorr)^5` | 4.21 | 4.50 | 0.160 | 0.7996 | 0.7996 | ❌ 双闸超线 |

**决定性杠杆再次验证 = SUBINDUSTRY**：唯一用 SUBINDUSTRY 且组合足够宽的 V1 过闸（0.6879），
而 STATISTICAL 的 V3 高到 0.7996 —— 与 skill 记录的规律一致（SUBINDUSTRY 是压 prod 的关键）。

## 提交实测（V1 = MPaGzEx8）

两次 `POST /alphas/MPaGzEx8/submit` 均返回 `{"success": true, "reason": "IS checks passed"}`，全闸：

| 闸 | 结果 | value / limit |
|---|---|---|
| LOW_SHARPE | PASS | 4.16 / 1.58 |
| LOW_FITNESS | PASS | 4.86 / 1.0 |
| LOW_TURNOVER / HIGH_TURNOVER | PASS | 0.1544 / 0.02 · 0.4 |
| LOW_SUB_UNIVERSE_SHARPE | PASS | 1.86 / 1.23 |
| IS_LADDER_SHARPE | PASS | 4.47 / 2.02 |
| CLUSTER_TEST | PASS | 2.68 / 1 |
| **LOW_ROBUST_UNIVERSE_SHARPE**（IND 专属）| **PASS** | 1.43 / 1 |
| **SELF_CORRELATION** | **PASS** | **0.6879 / 0.7** |
| **PROD_CORRELATION** | **PASS** | **0.6879 / 0.7** |
| SUPER_SUBMISSION | PASS | 0 / 1 |
| SELF_SUPER_ALPHA | PASS | — |

→ 2 分钟内翻 ACTIVE/OS。

## 流程要点（照 skill 执行）

1. **SUPER 描述必须裸 PATCH**：`PATCH /alphas/{id}` body 只带 `{"selection":{"description":…},"combo":{"description":…}}`
   （`set_alpha_properties` 对 SUPER 必 400，因其无条件带 `regular`）→ 本次 PATCH 200，回读 1118 / 986 字符 ✅。
2. **提交两次**：第一次 200「IS checks passed」不足为凭，第二次回带 PROD/SELF 实测值才算定论。
3. **提交前零成本探针**（`check_self_correlation` 本地 + 原始 GET 轮询 prod）：V1 提前测得 0.6875/0.6879，
   与提交层实测 0.6879 一致 → 探针可信，可用于预筛变体。
4. 命名沿用「区_S_<prod×1000>_<id尾>」：`IND_S_p0688_GzEx8`。
