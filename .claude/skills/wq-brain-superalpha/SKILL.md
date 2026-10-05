---
last_verified: 2026-10-01
name: wq-brain-superalpha
description: "构建并提交 WorldQuant BRAIN SuperAlpha（type=SUPER，selection + combo 工作流）。触发词：组 SuperAlpha / 组 SA / 合成超级 alpha / 把多个 alpha 组合成一个。前置：单一区域已有 ≥10 颗 ACTIVE REGULAR 作组件；目标：合成后 SELF / PROD 相关性均 < 0.7 且 status → ACTIVE。范围：组件计数 → 建 SUPER simulation → 双闸探针 → 提交（不可逆，需用户明确确认）。"
layer: L5
allowed-tools:
  - Read
  - Bash
  - Write
  - mcp__wq-brain-http__*
---

# WQ BRAIN SuperAlpha（selection + combo）构造与提交

## 职责边界

- **本 skill 负责**：**SUPER（SuperAlpha）组套**——select → status → probe → submit；需本区 ACTIVE REGULAR ≥ 10，且双闸（SELF / PROD）达标
- **本 skill 不做**：**不提交 REGULAR 单颗**（→ `worldquant-submit-alpha`）；**不挖 REGULAR**（→ `wq-brain-ra-pipeline`）。组件不足时输出「缺口清单」交给 RA（见下），**不得改用 REGULAR 路径绕过**，也不得绕过 prod 闸
- **上游 / 下游**：上游 = 本区 ≥ 10 颗 ACTIVE REGULAR（`sa_probe` 给 `GO`）+ 用户明确要组 SA；下游 = SUPER ACTIVE → S6 [`wq-backtest-monitor`](../wq-backtest-monitor/SKILL.md)（监控复盘与台账回写；**OS 表现监控与重着色目前没有承接者**，见 RA step9 §9.8）

**组件不足时交给 RA 的输入**：区域 / 缺口 N 颗（`sa_probe` 的 `need`）/ 若 PROD 已饱和还需 **prod < 0.55 的新血 REGULAR**（见 levers §3）。接收方 = `wq-brain-ra-pipeline` 步 1（库存盘点）起的常规九步；反向的触发（本区 ACTIVE REGULAR ≥ 10 → 可转 SuperAlpha）写在 RA 的 `loop-and-stop.md` L.4。

> 本文只写**规则与每步骨架**；杠杆与参数-指标对照在 [`references/levers-and-evidence.md`](references/levers-and-evidence.md)，四个真实案例在 [`references/cases.md`](references/cases.md)，情景卡在 [`references/scenarios.md`](references/scenarios.md)，日期与变更在 [`../CHANGELOG.md`](../CHANGELOG.md)。
> 旧版是按时间追加的日记：后文推翻前文而前文不改（「SUBINDUSTRY 是决定性杠杆」被三处后文推翻），且**全文没有一处写「怎么建 SUPER simulation」**。2026-09-29 重写。

## 入口

| 入口 | 做什么 | 会提交吗 |
|---|---|---|
| `python tools/super_build.py select / status / probe` | 建 SUPER simulation / 查状态与指标 / 双闸探针 | 否 |
| `python tools/super_build.py submit --alpha-id <ID>` | 写名称与描述 → **prod 闸** → 提交 | **是（不可逆）** |
| `mcp__wq-brain-http__workflow_superalpha(region, components, neutralization, confirm_submit=False)` | 上面几步的 MCP 封装：sa_probe → select → status → probe →（仅 `confirm_submit=True`）submit | `confirm_submit=True` 时是——内部调用 `super_build.py submit`，**同一个 prod 闸**。只转发 region / universe / neutralization / selection / combo，`decay` / `selectionLimit` / `self_gate` 用 CLI 缺省；要调杠杆走 CLI |
| `mcp__wq-brain-http__sa_probe(region)` / `python tools/sa_probe.py --region <R>` | 组件池计数：`GO`（ACTIVE REGULAR ≥ 10）/ `BLOCKED` | 否 |

**不要**对 SUPER 调 `workflow_submit_alpha(confirm_submit=True[, force=True])`：该节点没有 prod 闸，`force=True` 还跳过本地预检——旧版正是这样教的。现在节点在任何副作用之前**拒绝 SUPER**（`reason: super_requires_super_build`，`force` 也无效；`tests/unit/05_submit_quota/test_submit_alpha_super_guard.py` 守）。
`components` 参数只用于「≥ 10 颗」计数：SUPER 的成分由 `selection` 表达式在运行时筛选，**不按 id 列表指定**。

## 不可逆动作块

> ⚠ **不可逆：`super_build.py submit`（= `workflow_superalpha(confirm_submit=True)` 的最后一步）——第一次通过的 POST 就是真提交**，没有零成本的「再试一次」。被拒（403）零成本；通过 = 已提交（2–3 分钟后翻 ACTIVE）。
> **前置（缺一不得执行）**：① `sa_probe` = `GO`；② SUPER simulation 已完成且 `status` 子命令无 FAIL；③ `probe` 双闸通过；④ **prod 实测 < 0.7**（CLI 内置闸：`max ≥ 0.7` 或探针超时一律拒绝，不写属性、不发 POST）；⑤ **用户明确确认**；⑥ 本 ET 日 SUPER 配额未满（`python tools/quota_status.py`）。
> **默认形态**：`select` / `status` / `probe` 与 `workflow_superalpha(confirm_submit=False)` 都不提交。
> **需要用户明确确认**：是。
> **执行后必须核验**：`python tools/super_build.py status --alpha-id <ID>` → `ACTIVE`。
> **豁免**：`--allow-prod-above-07` 只在用户显式要求时用（它同时豁免「value ≥ 0.7」与「探针超时」两种拒绝，且平台可能仍回 PASS）；不得默认携带。

**判定优先级**：提交 = 平台 `result == PASS`（必要）**且**我方 prod 实测 < 0.7（必要）。后者更严：平台对 SUPER 可能回带 value > 0.7 仍判 PASS（GLB 0.8094 / KOR 0.8571 实证，见 cases），但**我方铁律是 prod ≥ 0.7 不提交**——两者不冲突，任一说「不」就停。别自己按 value 预判 PASS / FAIL（分界不稳定），判定永远看 `result`。

## 步骤

### 步 0　组件计数
- **目的**：决定值不值得发 SUPER simulation（省一个仿真槽）。
- **前置**：已定区域。
- **调用**：`mcp__wq-brain-http__sa_probe(region=<R>)`；无 MCP：`python tools/sa_probe.py --region <R>`（退出码 0 = GO，1 = BLOCKED）。
- **产物**：`{verdict, eligible, need, eligible_ids}`。`/users/self/alphas` 的 `region=` 参数**不生效**（各区返回同一份全量）——工具已拉全量后按 `settings.region` 本地分组，**不要手写 requests 翻页**。
- **完成定义**：`verdict == GO`（`eligible ≥ 10`）。
- **失败分支**：`BLOCKED` → 把 `need` 交 RA（见上「组件不足」），**不发 simulation**。
- **不做**：不以「现状快照」（旧版写过「USA 133 / EUR 7 …」）作依据——计数只用这条命令的实时结果。

### 步 1　建 SUPER simulation
- **目的**：用 selection + combo 建一颗 `type=SUPER` 的 simulation。
- **前置**：步 0 = GO；已确定**中性化档位**（**无缺省，必须显式**；已知最优见 levers §1，但**先枚举本区存量 SA 占用了哪 (neutralization, decay) 并错开**——USA 2026-10-01 实证：存量已占 SUBINDUSTRY(`KPGvRMg1`) / MARKET(`gJ8eVmNM`)，新 SA 用 **STATISTICAL** 才过，见 levers §6）；universe / delay 缺省取 `wqb.config.REGIONS`（旧缺省 `TOP400` 只对 MEA 合法，非法档位平台回 HTTP 500）。
- **调用**：
  ```
  python tools/super_build.py select --region KOR --neutralization STATISTICAL --decay 5 --selection-limit 10 --self-gate 0.55
  ```
  其余旋钮：`--combo-power {1,3,5}`、`--turnover-min / --turnover-max`、`--prod-ceiling`、`--selection` / `--combo`（给完整表达式覆盖模板）、`--json <path>`。取值理由见下「参数」。
- **产物**：SUPER alpha id（stdout 的 `alpha id = …`）。
- **完成定义**：拿到 id，且步 2 不是 `ERROR`。
- **失败分支**：**201 ≠ SA 合法**——平台不在创建时校验，错误异步出现在模拟结果里（`GET /simulations/{id}` → `status: ERROR`，`message: "At least 10 component alphas are required for Super Alpha."`，`location.property: combo`）→ 转情景 SA-02（组件恰好 10 颗：放宽 gate）；「PROD 一直偏高」转 levers §3。
- **不做**：不用旧的 `combination(alpha(...))`（平台已报 "inaccessible or unknown operator combination"）。⚠ **记法修正（2026-10-01）**：旧写「不把 `selectionLimit` 当杠杆」只在**超过有效池之后**成立（USA 1000 与 50 逐位相同）；**有效池以内它是强杠杆**——USA sl10→15→30 使 IS sharpe 2.63→3.85→4.02、SUB ratio 0.789→0.880→0.966（levers §6）。口诀：**改「篮的有效宽度」动门**（self_gate / prod_ceiling / turnover 带），**改「篮里取多少」动 `selectionLimit`**。

### 步 2　查状态
- **调用**：`python tools/super_build.py status --alpha-id <ID>`（打印 sharpe / fitness / turnover 与全部 checks，`FAIL` 时退出码 1）。
- **完成定义**：`status` 不是 `ERROR`，且无 `FAIL` 检查。
- **失败分支**：`ERROR` + `At least 10 component alphas` → 步 1 失败分支；`LOW_SUB_UNIVERSE_SHARPE` → **levers §6（它是比值闸 limit≈0.431×IS sharpe；盯 `ratio = sub/limit`，两杠杆 = decay↓ 与 selectionLimit↑（有效池内））**；`LOW_TURNOVER`（SUPER 下限 0.02）→ levers §0 决策表对应行。

### 步 3　双闸探针
- **调用**：`python tools/super_build.py probe --alpha-id <ID>`（SELF 本地 + PROD 平台；`PASS` / `BLOCKED`，退出码 0 / 1）。
- **完成定义**：`VERDICT: PASS`（SELF 与 PROD 都 < 0.7）。
- **失败分支**：SELF ≈ 0.9+ 且命中已 ACTIVE 的 SA = **近克隆**，SELF 闸必拒 → 情景 SA-03（换成分 / 错开 (neutralization, decay)）；PROD ≥ 0.7 → **先跑 levers §6 的三杠杆**（错开中性化档 + decay↓ + 宽篮）——USA 2026-10-01 在无任何新血下把 PROD 0.8495 压到 0.6751，**旧止损线「PROD 饱和即停止调参、回 RA 挖新血」已推翻**，三杠杆用完确实无解才回 RA。
- **不做**：**本地 SELF 对近期新提交的孪生体结构性失明**（selfcorr-quick 实测：本地 0.229 vs 平台 0.8392；SA 恰是「池子被消耗、近克隆风险高」的场景）——近期有同构 SA 提交时，探针的 SELF 只能当下限；先枚举存量 SA 的 (neutralization, decay) 并错开（情景 SA-03）。`mcp__wq-brain-http__run_selection` 是**选股（instrument filtering）**工具，与 SA 的 `selection` 表达式无关，别混。

### 步 4　提交（不可逆；见上「不可逆动作块」）
- **调用**：`python tools/super_build.py submit --alpha-id <ID>`：prod 闸（轮询 `GET /alphas/{id}/correlations/prod`，15 s 间隔、窗口缺省 900 s）→ 取详情与提交层预检 → 写 name + 两段描述 → POST（CLI 只发这一次；受理后用 `status` 子命令轮询核验，窗口见 `wqb.config.WAIT_THRESHOLDS`）。选项：`--prod-gate`（阈值，缺省 0.7）、`--probe-timeout`、`--allow-prod-above-07`（豁免，见上）。
- **描述写入**：CLI 内置 ≥ 100 英文字的 selection / combo 描述，**走 CLI 就不需要手工 PATCH**。手工路径只传 `selection_description` + `combo_description`（**不要传 `descriptions`**：它会给 PATCH body 加 `regular` 字段，SUPER 被平台 400）；写完 `get_alpha_details` 回读两段描述长度 > 0 再提交。
- **命名**：`<REGION>_S_<N>comp_<alpha_id 尾 6 位>`（规范见 `docs/alpha_properties_spec.md`；**不要把 PROD 数值放进 name**——提交时快照会过期骗人，也不要固定序号 `_01`：同区多颗必重名，GLB 曾一轮造出三颗同名候选）。
- **完成定义**：`status` 子命令 → `ACTIVE`。
- **失败分支**：403 = 拒绝（响应体带具体 FAIL 与 value；零配额成本，SUPER_SUBMISSION 不计数）→ 按 FAIL 名回步 1 / 情景；`SUPER_SUBMISSION` 已满 → 次日再提。
- **不做**：不对同一颗 SA 连续 POST「试探」；不用 `GET /alphas/{id}/submit` 判定（见下）。

**`GET /alphas/{id}/submit` 的行为按 type 未复核**：REGULAR 上它恒 404（2026-09-26 实测），SUPER 上 2026-09-11 的 KOR 观察是「200 但 SELF / PROD 仍 PENDING（假阳性）」。两份记录不一致、也没有重新对照，所以**无论哪种类型都不得用它放行**——判据只有提交后的 `status`。核对办法见闭环台账 SP-11（needs-platform）。

## 硬前置（规则）

1. **组件**：≥ 10 颗**同一 region** 的、已 ACTIVE 的 REGULAR（平台 `selectionLimit ≥ 10`）。恰好 10 颗时 selection 的运行时筛选（self_gate / turnover 带）会再刷掉一部分，必须放宽 gate，否则「At least 10 component alphas」秒拒。
2. **描述**：selection / combo 描述各 ≥ 100 英文字（平台硬门槛）。
3. **配额**：提交 REGULAR 组件与 SA 都占 **ET 日历日**配额（REGULAR 4 + SUPER 1，00:00 ET 重置），模型与来源见 [`worldquant-submit-alpha/references/quota-and-tower.md`](../worldquant-submit-alpha/references/quota-and-tower.md)，不在这里重述。
4. **区域可用性**：区域状态（例如 MEA 的 `POST /simulations` 现返回 400 "Region MEA is not available."，既有 2 颗 MEA SA 是存量）属于平台状态，不属于 SA 方法论：以各区 profile（`wq-brain-ra-pipeline/references/regions/<R>.md`）与 `wq-brain-campaign-matrix` 为准。

## SA 结构与语法（实测）

`selection` 从候选成分里**筛成分 + 赋权重**；`combo` 把筛出的成分**合成**成最终信号。`tools/super_build.py` 的两个模板是可执行的原文（**以代码为准**）：

```
selection: (1 + 0 * (prod_correlation > 0)) * ({prod_ceiling} - prod_correlation) * (self_correlation < {self_gate}) * (turnover > {turnover_min}) * (turnover < {turnover_max})
combo:     stats = generate_stats(alpha); innerCorr = self_corr(stats.returns, 500); ic = if_else(innerCorr == 1.0, nan, innerCorr); maxCorr = reduce_max(ic); w = 1 - maxCorr; w
```

- **selection**：逻辑符 `&` / `and` 被拒，用 `*`（AND）/ `||`（OR）/ `==`；`prod_correlation` 在 selection 可用、在 combo **不可用**（引用会报 `unknown variable`）。`(prod_correlation > 0)` 写成 `(1 + 0 * (…))` 的**非门控 no-op**：直接乘会把 prod ≈ 0 的 novel 成分清零。⚠ 这一项来自 USA 的 2026-08 实测，**平台是否硬性要求 selection 里出现该子串未复核**（模板对所有区域都带它，没有因缺它而失败的记录）。
- **combo**：只能压 **SELF**，压不动 PROD（生产相关由成分池本身决定）。`--combo-power 3 / 5` 把权重写成 `w*w*w` / `w*w*w*w*w`（拉大离散度，集中到最独立的成分）。⚠ `500` 是模板沿用的历史值（≈ 2 年 = 504 个交易日的取整），**不在本库标准窗口表内，且没有做过 500 对 504 的对照**——登记为待验证（SP-08）。
- `combination(alpha(...))` 已不可用；必须用 selection + combo。

## 参数（缺省与取值理由）

| 旋钮 | 缺省 | 取值理由 / 何时改 |
|---|---|---|
| `--neutralization` | **无缺省** | 因区而异，需逐区扫描；已知最优（区域，日期）见 levers §1。缺省值会把人引向错误起点，故 2026-09-29 取消 |
| `--decay` | 5 | 窄篮下 decay↑ → SELF↓（levers §2 的 KOR 曲线）；宽篮下 decay↑ → PROD↑ |
| `--selection-limit` | 10 | 平台下限；⚠ **有效池以内是强杠杆**（USA sl10→15→30：IS sharpe 2.63→3.85→4.02、SUB ratio 0.789→0.880→0.966，levers §6），**超过有效池后才无效**（USA 1000 与 50 逐位相同）。改「篮的有效宽度」动门（self_gate），改「篮里取多少」动它 |
| `--self-gate` | 0.55 | `self_correlation < gate` 的硬闸。组件恰好 10 颗时 0.65 → 0.70 → 0.85 逐档放宽（成本极低：组件不足的 sim 秒级失败回错） |
| `--turnover-min / --turnover-max` | 0.01 / 0.5 | 池内成分 turnover 最高 0.5495 时改 0.6（MEA 案例） |
| `--prod-ceiling` | 0.7 | 评分项 `(0.7 - prod_correlation)`：偏好 prod 低的 novel 成分。池内存在 prod > 0.7 的成分被 POSITIVE 剔除致不足 10 颗时改 1.0（超标成分降权参与而非出局） |
| `--combo-power` | 1 | 1 / 3 / 5；IND 实测 SELF 0.7581 → 0.7539（3 次方）→ 0.7508（5 次方），代码注释称「免费压最后一截」（指标口径以该注释为准，未复核） |

## 验证清单

- [ ] 同区域 ACTIVE REGULAR ≥ 10 颗（`sa_probe` = GO）；恰好 10 颗时已放宽 gate。
- [ ] **中性化已逐区扫描，且已枚举本区存量 SA 占用的 (neutralization, decay) 档位并错开**：已知最优（区域，日期）见 levers §1——USA / GLB = SUBINDUSTRY、KOR / IND = STATISTICAL（IND 极差 0.199）；⚠ **USA 2026-10-01 例外**：存量已占 SUBINDUSTRY / MARKET，新 SA 用 **STATISTICAL** 才过（levers §6）。
- [ ] `probe` 双闸通过；**prod 闸**（`super_build.py submit` 默认强制）通过，或用户显式豁免。
- [ ] **不追 IS 业绩指标**（`references/selection-playbook.md` §1）：IQC 顶尖 SA 的 OS/IS 达 0.3 都很少，追 IS 是追噪声，且会抬高 SUB 比值闸的 limit（≈0.431×sharpe）并推高 prod/self。**正确止损 = 双闸达标 + 多样性达标就提。**
- [ ] 提交判定看 `result`，且我方 prod 实测 < 0.7。
- [ ] status 翻 ACTIVE（2–3 分钟后）；name 用 `<REGION>_S_<N>comp_<id 尾 6 位>`。
- [ ] **淘汰的同构变体**按 `docs/alpha_properties_spec.md`：打 `RETIRE_<YYYYMMDD>` 并 hidden；撞了谁写进描述而不是新造标签前缀（新前缀须先登记规范）；color **不用 RED**（规范里 RED = 已提交 · 待退役，这些变体从未提交）。
  - ⚠ **MCP 的 `set_alpha_properties` 没有 `hidden` 参数**（只有 name / color / tags / descriptions），`build_alpha_properties_payload` 也不认它 → 设 hidden 必须走原始 PATCH：
    ```python
    cur = (await brain._request("GET", f"{brain.base_url}/alphas/{aid}")).json()   # 先回读
    tags = list(cur.get("tags") or []) + ["RETIRE_<YYYYMMDD>"]                    # ★ tags 整组替换
    await brain._request("PATCH", f"{brain.base_url}/alphas/{aid}", json={"tags": tags, "hidden": True})
    ```
    **不先 GET 回读会把已有 tags 抹成只剩 RETIRE**（`super_build.py` 造的变体实测 tags 为空，但别赌）。可复用脚本 `logs/retire_sa_variants.py`（改 `IDS` / `TAG` 即可，2026-10-01 USA 10 颗 10/10 成功）。

## SUPER 专属检查名（`get_alpha_details` / 提交响应里出现）

| 检查 | 含义 |
|---|---|
| `SELF_CORRELATION` / `PROD_CORRELATION` | 与自己已提交 / 全平台已提交池的相关；提交时**实时**查 |
| `SUPER_SUBMISSION` | SUPER 日配额（1 / ET 日） |
| `NON_SELF_SUPER_ALPHA` | 同策略 SA「自残」闸 |
| `LOW_TURNOVER`（SUPER 下限 0.02） / `LOW_SUB_UNIVERSE_SHARPE` | 换手过低 / 子宇宙不稳 |
| `LOW_ROBUST_UNIVERSE_SHARPE` | **IND 独有** |

IS 闸门的通用阈值见 `brain-how-to-pass-alpha-test`；它不覆盖上表 SUPER 专属项。

## 相关 skill

- `brain-forum-browse`：要查论坛新经验时走它（只读检索）；本 skill 的 `references/selection-playbook.md` 是它 2026-10-01 的沉淀结果，**先看沉淀，不够再查**。
- `worldquant-submit-alpha`：单颗 REGULAR 的提交与响应处置；提交链状态机见其 `references/submit-chain.md`。
- `brain-how-to-pass-alpha-test`：各 IS 闸门阈值（Fitness / Sharpe / Turnover / Self-Corr / PROD_CORR）。
- `brain-calculate-alpha-selfcorr-quick`：本地 SELF 快筛及其盲区。
