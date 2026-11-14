# 边际贡献「分级硬闸」上线与候选池裁决

日期：2026-11-13 19:2x｜用户选定方案：**分级硬闸**｜状态：代码 / 测试 / 文档已同步，未改变任何已提交 alpha

## 1 约束定义

| 指标 | 方向 | 达标 | 违反时 |
|---|---|---|---|
| Sharpe | 越大越好 | Δ >= 0 | **硬闸阻断** |
| Returns | 越大越好 | Δ >= 0 | **硬闸阻断（本次新增）** |
| Fitness | 越大越好 | Δ >= 0 | **硬闸阻断（19:5x 追加）** |
| Turnover | 越小越好 | Δ <= 0 | 仅软告警 |
| Drawdown | 越小越好 | Δ <= 0 | 仅软告警 |

硬项任一为负 => `blocked=True`，在 `set_properties` / POST 之前 return，`force` 不豁免；
`available=False`（端点空体 / 异常）不阻断；预检只出数值 + 预告。

## 2 16 颗活跃候选逐颗裁决

| alpha | 分区 | ΔS | ΔF | ΔRet | ΔTO | ΔDD | 新闸 | 全方向 | 软告警 |
|---|---|---:|---:|---:|---:|---:|:---:|:---:|---|
| `omEdka3v` | POWER_POOL | +0.59 | +0.25 | +0.0028 | +0.0252 | +0.0033 | OK 可交 | - | TO,DD |
| `wpo8olA6` | POWER_POOL | +0.56 | +0.42 | +0.0015 | +0.0063 | -0.0164 | OK 可交 | - | TO |
| `6XdkW08J` | POWER_POOL | +0.42 | +0.34 | +0.0020 | -0.0014 | -0.0008 | OK 可交 | OK | - |
| `88NmN37X` | POWER_POOL | +0.74 | +0.68 | +0.0058 | -0.0179 | -0.0314 | OK 可交 | OK | - |
| `Xg9dPpp0` | POWER_POOL | +0.42 | +0.33 | +0.0013 | -0.0013 | -0.0015 | OK 可交 | OK | - |
| `leAmmre8` | POWER_POOL | +0.69 | +0.19 | +0.0007 | +0.0382 | -0.0019 | OK 可交 | - | TO |
| `mLaLllmK` | POWER_POOL | +0.84 | +0.41 | +0.0053 | +0.0256 | -0.0025 | OK 可交 | - | TO |
| `RREPm361` | POWER_POOL | +0.73 | +0.31 | +0.0080 | +0.0619 | -0.0326 | OK 可交 | - | TO |
| `zq3Yrb3G` | 1 | +0.02 | +0.02 | +0.0000 | +0.0019 | -0.0001 | OK 可交 | - | TO |
| `ZYQ116ln` | POWER_POOL | +0.24 | +0.10 | -0.0026 | +0.0035 | -0.0026 | BLOCK | - | TO |
| `JjeNJ00O` | 1 | +0.02 | +0.01 | -0.0002 | +0.0023 | -0.0003 | BLOCK | - | TO |
| `O0A6Qz7p` | 1 | +0.09 | +0.07 | -0.0004 | -0.0011 | -0.0005 | BLOCK | - | - |
| `YP1baJrv` | 1 | +0.02 | +0.01 | -0.0001 | +0.0022 | +0.0003 | BLOCK | - | TO,DD |
| `qM7KxkQV` | 1 | +0.05 | +0.04 | -0.0007 | +0.0001 | -0.0008 | BLOCK | - | TO |
| `vRAgNK3w` | POWER_POOL | +0.28 | +0.22 | -0.0040 | -0.0160 | -0.0019 | BLOCK | - | - |
| `Wjl8Z20O` | POWER_POOL | +0.31 | +0.25 | -0.0038 | -0.0146 | -0.0020 | BLOCK | - | - |

**按新闸 9/16 可交**：`omEdka3v`, `wpo8olA6`, `6XdkW08J`, `88NmN37X`, `Xg9dPpp0`, `leAmmre8`, `mLaLllmK`, `RREPm361`, `zq3Yrb3G`

**被 ΔReturns 硬项拦下 7 颗**：`ZYQ116ln`, `JjeNJ00O`, `O0A6Qz7p`, `YP1baJrv`, `qM7KxkQV`, `vRAgNK3w`, `Wjl8Z20O`

五项按方向全达标仅 3 颗：`6XdkW08J` / `88NmN37X` / `Xg9dPpp0`（未作为硬闸，仅作排序参考）。

## 3 对推荐顺位的影响

| 原顺位 | alpha | 新闸 | 结论 |
|---:|---|:---:|---|
| 1 | `omEdka3v` | OK | 保持可交 |
| 2 | `wpo8olA6` | OK | 保持可交 |
| 3 | `ZYQ116ln` | BLOCK | 移出可交清单 |
| 4 | `6XdkW08J` | OK | 保持可交 |
| 5 | `JjeNJ00O` | BLOCK | 移出可交清单 |

=> 首推仍是 `omEdka3v`（ΔS +0.59 / ΔRet +0.0028），次选 `wpo8olA6`（+0.56 / +0.0015）；
原第三席 `ZYQ116ln` 已被拦，第三席改 `6XdkW08J`（+0.42 / +0.0020）。

## 4 追溯与边界

- 今日 17:44 已提交的 `P059RmzM`：ΔRet **-0.0040**，按新闸会被拦。已 ACTIVE 不可逆，只标注为「新闸生效前的历史提交」，不追溯撤销、不改终态。
- 新闸只判**方向符号**，不设幅度阈值；ΔS 仍禁止跨分区横比。
- `MARGINAL_HARD_BLOCK_METRICS` 已含 `fitness`（19:5x 追加）。16 颗 ΔFitness<0 为 0 颗，**9/16 裁决逐颗不变**；但 Fitness 复合 Turnover，ΔTO 大幅上升会经 ΔFitness 间接硬拦（构造例 ΔF −0.381），属已知取舍，要回退就从常量里移除 `fitness`。

## 5 同步清单

| 位置 | 变更 |
|---|---|
| `src/wqb/workflow/nodes/submit_alpha.py` | 新增 `MARGINAL_*` 常量与 `hard_blocked` / `hard_failures` / `soft_warnings` / `direction_ok` / `direction_rule` 字段；Step 1.7 改按 `hard_blocked` 阻断 |
| `tests/unit/05_submit_quota/test_submit_marginal_contribution.py` | +4 测试（ΔRet 负硬闸、成本指标软告警、全达标、方向规则透出） |
| `tests/unit/05_submit_quota/test_submit_marginal_wiring.py` | 正向样本 ΔRet 校正；+3 测试（ΔRet 负真提交阻断 / 预检预告 / 成本指标不阻断） |
| `docs/experience/01_platform_gates.md` | 新增 §17 |
| `Claude/skills/.../submit-chain.md` 与 `~/.workbuddy/skills/.../submit-chain.md` | 步 4b 与「否决权威」行同步（双份同源） |
| 回归 | `pytest tests/unit/05_submit_quota/ -q` -> **388 passed** |

机读数据：`results/_marginal_allmetrics_20261113.json`。

---

# §6 追加（19:5x）：`fitness` 升为第三项硬闸

用户追问「fitness 是不是也应该硬闸阻断」⇒ 判定**应该**，已落地。

| 项 | 结论 |
|---|---|
| 对称性 | `sharpe/fitness/returns` 同为「越大越好」正向族，只拦两个是口径缺口 |
| 零误伤 | 16 颗活跃候选 ΔFitness<0 为 **0 颗**；三项硬闸下仍 **9/16 可交，逐颗与原 S+Ret 裁决完全一致** |
| 独有信息 | `F = S×√(ret/max(TO,0.125))`，是唯一直接反映「换手成本吃掉收益改善」的量 |
| 构造反例 | S 3.0→3.1、ret .080→.081、TO .13→.20 ⇒ F 2.353→1.973（**ΔF −0.381**），此时 ΔS>0、ΔRet>0 却应被拦 |

⚠ **已知取舍**：Fitness 复合了 Turnover，因此 `ΔTurnover` 大幅上升会**经 ΔFitness 间接触发硬闸**，与「成本指标只告警」的初衷部分重叠。若不接受这个副作用，把 `fitness` 从 `MARGINAL_HARD_BLOCK_METRICS` 移除即可 —— 常量集中、改动可逆、无历史数据迁移。

**改动**：`MARGINAL_HARD_BLOCK_METRICS = ("sharpe", "fitness", "returns")`；Step 1.7 注释 / `marginal_warning.note` / `blocked_reason` / `note` / docstring 口径同步；新增 2 个测试（`ΔF<0` 硬拦，contribution + wiring）→ `pytest tests/unit/05_submit_quota/ -q` **390 passed**；`docs/experience/01_platform_gates.md` §17、`submit-chain.md`（项目级 + 5 个安装位 md5 统一）、`MEMORY.md` §0 全部同步。

**真实平台数据端到端**：`omEdka3v` → `hard_blocked=False / soft=['turnover','drawdown'] / rule=['sharpe','fitness','returns']`；`vRAgNK3w` → `hard_blocked=True / fails=['returns']`。

---

# §7 现行口径（20:0x 定案）：方案 D「分层 + 配对」

> **§1–§6 是当日口径演进记录；现行判定以本节为准。**

用户追问「换手不是越小越好吗，为什么会有反例，怎么匹配这几个指标才是最佳的方案」⇒ 发现
`F = S×√(ret/max(TO,0.125))` 让 `sharpe/fitness/returns/turnover` 四量共线：三项正向指标全硬拦
等于对同一信息三重把关；且 ΔTO 单独看是软告警、复合成 ΔF 却硬拦，口径自相矛盾。
用户从三个方案中选定 **D 分层 + 配对**，已落地。

## 三层结构

| 层 | 判定 | 处置 |
|---|---|---|
| 1 净效果（唯一硬闸） | `ΔSharpe ≥ 0` 且 `ΔFitness ≥ 0` | 任一为负 ⇒ 阻断，`force` 不豁免 |
| 2 配对（仅 ΔRet<0 时启用） | `ΔReturns<0` **且** `ΔTurnover>0` 或 `ΔDrawdown>0` | 双重恶化 ⇒ 追加阻断；`ΔReturns<0` 但成本同步降 ⇒ **分散化补偿放行**（`pair_rule.offset=True`） |
| 3 归因（纯软告警） | `ΔTurnover` / `ΔDrawdown` 单独变差 | 只写 `soft_warnings`，不设闸 |

`available=False`（端点空体/异常/已提交件 400）仍 fail-open；`dilutive` 仍保留 ΔS<0 语义供 Step 1.8 复用。

## 为什么 ΔReturns 不能单独硬拦

`before/after` 是把候选**等权叠加到分区已提交组合**的结果，不是候选自身指标。`ΔRet<0`
常只是「新腿收益低于池均值」的机械摊薄，低相关分散化来源几乎必然如此。被原闸误伤的 3 颗：

| alpha | ΔS | ΔF | ΔRet | ΔTO | ΔDD |
|---|---:|---:|---:|---:|---:|
| `vRAgNK3w` | +0.28 | +0.22 | −0.0040 | **−0.0160** | −0.0019 |
| `Wjl8Z20O` | +0.31 | +0.25 | −0.0038 | **−0.0146** | −0.0020 |
| `O0A6Qz7p` | +0.09 | +0.07 | −0.0004 | −0.0011 | −0.0005 |

今日已提交的 `P059RmzM` 同形态（ΔRet −0.004 / ΔTO −0.017 / ΔDD −0.0021 / ΔS +0.29 / ΔF +0.23）。

## 方案对比与裁决（16 颗实测）

| 方案 | 可交 | 评价 |
|---|---:|---|
| A 原 S+F+Ret 全硬拦 | 9/16 | 误伤 3 颗健康分散化 |
| B 五项全按方向 | 3/16 | 连首推 `omEdka3v` 都拦 |
| C 只 S+F | 16/16 | 闸形同虚设（本池 ΔS/ΔF 恰全 ≥0） |
| **D 分层 + 配对（现行）** | **12/16** | 拦 4 颗真恶化、放行 3 颗补偿 |

- 拦下：`ZYQ116ln` / `JjeNJ00O` / `YP1baJrv` / `qM7KxkQV`（收益降且成本升）
- 放行 3 颗补偿：`vRAgNK3w` / `Wjl8Z20O` / `O0A6Qz7p`
- 首推顺位不变：`omEdka3v` → `wpo8olA6` → `6XdkW08J`。**闸放行 ≠ 推荐提交**；EUR risk70 三颗仍因同席 ρ≈0.99、塔倍率 ×1.0、prod 贴线、预期 OS≈0.65 而排在后面。

⚠ **局限**：本池 ΔS/ΔF 恰好全 ≥0，净效果层在样本内没有区分度，D 的分辨力主要来自配对判据，需跨区多批样本再验证。

## 落地与验证

- `MARGINAL_HARD_BLOCK_METRICS = ("sharpe", "fitness")`；新增 `MARGINAL_PAIR_COST_METRICS` 与 `pair_rule`（`triggered / offset / cost_metrics_up / rule`）、`direction_rule.scheme = "D: ..."`。
- 测试新增 3 例（分散化补偿放行 / 配对触发硬拦 / 真提交放行）→ `pytest tests/unit/05_submit_quota/ -q` **393 passed**。
- 文档 `docs/experience/01_platform_gates.md` §18、`submit-chain.md` 步 4b（项目级 + 5 安装位 md5 `e39180b5`）、`MEMORY.md` §0 全部同步。
- 真实平台端到端：`vRAgNK3w` / `Wjl8Z20O` → `hard=False, offset=True`；`ZYQ116ln` → `hard=True, fails=['returns'], cost_up=['turnover']`；`omEdka3v` → `hard=False`（ΔRet>0，配对不触发）。

### 20:1x 全篮子复验（修正上面的「局限」判断）

`output_report/full_basket_scheme_d_20261113.md`：47 颗逐颗重测，46 颗可读 ⇒ 方案 D **放行 31 / 阻断 15**。
**净效果层在全篮子有区分度**：ΔS<0 **7 颗**、ΔF<0 **5 颗**（重叠 4）；其中 `6XMmE0EL` 是唯一
「ΔS≥0 但 ΔF<0」的件（+0.33 / −0.06，ΔTO +0.0312），旧版只看 ΔS 会误放行。
⇒ 上文「本池 ΔS/ΔF 恰全 ≥0、净效果层无区分度」**只适用于 16 颗样本**，不再作为方案 D 的全局局限。
