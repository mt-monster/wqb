---
last_verified: 2026-08-22
name: wq-brain-superalpha
description: "通过 selection + combo 工作流（type=SUPER）构建并提交 WorldQuant BRAIN SuperAlpha。 触发词：组 SuperAlpha / 组 SA / 合成超级 alpha / 组合多个 alpha；或单区域需把 ≥10 个 REGULAR 组件合成一颗 SUPER alpha，并保持 prod_correlation < 0.7、 self_correlation < 0.7。覆盖 SUBINDUSTRY 杠杆、`(1 + 0 * (prod_correlation > 0))` no-op 门控、score = (0.7 - prod_correlation)、self_correlation < 0.55 硬闸、 `mcp__wq-brain-http__workflow_submit_alpha(confirm_submit=True, force=True)` 两次调用判定、以及 ≥10 颗 ACTIVE REGULAR 组件前置条件。"
layer: L5
allowed-tools:
  - Read
  - Bash
  - Write
  - mcp__wq-brain-http__*
---







**运行环境**：所有 Python 命令使用 MCP venv（`$WQ_PY`），确保依赖（requests/pandas）可用。不要使用系统 Python。SuperAlpha 的创建/提交通过 WorldQuant BRAIN MCP 工具完成（mcp__wq-brain-http__get_user_alphas / mcp__wq-brain-http__set_alpha_properties / mcp__wq-brain-http__workflow_submit_alpha / mcp__wq-brain-http__check_correlation / mcp__wq-brain-http__check_self_correlation）。

# WQ BRAIN SuperAlpha（selection + combo）构造与提交

## 何时用
- 用户说「组 SuperAlpha / 组 SA / 合成超级 alpha / 把多个 alpha 组合成一个」。
- 目标是把一个区域内 **≥10 颗已 ACTIVE 的 REGULAR alpha** 合成为一颗 `type=SUPER` 的 alpha，
  并要求合成后的 `PROD_CORRELATION < 0.7` 且 `SELF_CORRELATION < 0.7`，最终 `status → ACTIVE`。
- 典型场景：USA（book 已有 ~145 ACTIVE，可直接组）；或用非 USA 区域（KOR/MEA/ASI/GLB 需先攒齐 ≥10 颗 ACTIVE 组件）。

## 衔接协议
- **上游**：S5 提交层判定 `tools/submit_verdict.py`（SUBMITTABLE 且 type=SUPER：单区域已攒齐 ≥10 颗 ACTIVE REGULAR 组件；brain-alpha-judge 参考评审可为点塔排序提供输入）。
- **本 skill 角色**：S5 SUPER 落地——selection + combo 合成并提交，压 PROD/SELF < 0.7。
- **下游**：S6 `wq-backtest-monitor`（OS 表现监控；§14 台账回写 `wave_results` + `registry_empirical` 反哺 S-PRE）。

## 硬前置（必读，否则必败）
1. **组件数量**：SUPER alpha 要求 **≥10 颗同一 region 的、已 ACTIVE 的 REGULAR alpha** 作为成分。
   - 平台在创建时即校验数量，不足 10 颗会直接报错（如 "At least 10 component alphas"）。
   - KOR 现状：book 内大量 UNSUBMITTED 空壳草稿、**0 ACTIVE** → 必须先挖并提交 ≥10 颗 REGULAR KOR 使其 ACTIVE，才能组 SA。
2. **描述长度与写入方式（实测 400 坑，2026-08-28）**：selection/combo 描述**各需 ≥100 英文字**。
   但 `set_alpha_properties`（MCP 工具与 brain_api 方法均是）**对 SUPER alpha 必返 400**——它无条件在 payload
   带 `regular` 字段，SUPER 无 regular 组件被平台拒绝。**正确写法：裸 PATCH 最小 payload**：
   `PATCH /alphas/{id}`，body 只带 `{"selection":{"description":...},"combo":{"description":...}}`
   （勿带 regular/color/name/tags）→ 200。写完 `get_alpha_details` 回读 sel/combo desc 长度确认 >0 再提交。
   参考脚本 `logs/_fix_desc_sa4.py`。
3. **提交配额**：提交 REGULAR 组件与 SA 都占 **ET 日历日提交配额**（REGULAR 4 颗/日 + SUPER 1 颗/日，00:00 ET 重置，非仿真额度）；`get_submission_quota` 已于
   2026-08-25 移除，剩余额度改从 submit 响应的 `REGULAR_SUBMISSION` check 的 value/limit 读取（counter 0→1→…）。
   （注意：硬闸门 FAIL 的提交尝试不消耗配额，status 保持 UNSUBMITTED，属零成本探测。）

## SA 的结构
一颗 SUPER alpha 由两段表达式构成（经裸 PATCH 写入，勿用 set_alpha_properties，见硬前置 #2 的 400 坑）：
- `selection`：从候选成分里**筛成分 + 赋权重**。
- `combo`：把筛出的成分**合成**成最终信号。

> `combination(alpha(...))` 现已**不可用**（报错 "inaccessible or unknown operator combination"）。
> 必须用 **selection + combo** 工作流，不要尝试旧的 `combination()` 写法。

## selection 语法（实测）
- USA 区域**必须**在表达式里出现 `(prod_correlation > 0)` 子串，但作为**非门控 no-op** 写：
  `(1 + 0 * (prod_correlation > 0))` —— 否则会把 novel（prod≈0）成分清零，逼入饱和的价值/盈利因子。
- 评分用 `(0.7 - prod_correlation)` 偏好 novel 成分（prod 越低越被选中）。
- 硬闸：`self_correlation < 0.55`（把自相关过高的成分剔除）。
- turnover 界：`(0.01, 0.5)`。
- 逻辑符：`&` / `and` 被拒；用 `*`(AND) / `||`(OR) / `==`。
- `selectionLimit` 至少 10（即至少选出 10 个成分）。
- `prod_correlation` 在 **selection 可用**，但在 **combo 不可用**（combo 里引用会报 "unknown variable"）。

示例骨架（USA 风格）：
```
selection: (1 + 0 * (prod_correlation > 0)) *
           (0.7 - prod_correlation) *
           (self_correlation < 0.55) *
           (turnover > 0.01) * (turnover < 0.5)
combo:     1 - maxCorr
```

## combo 语法（实测）
- `prod_correlation` **不可用**；只能用 `1 - maxCorr` 做 SELF 多样性。
- `maxCorr` 借助 `generate_stats` / `self_corr` / `reduce_max` / `if_else` 等算子构造。
- combo 的目的是降低成分间自相关，从而把 SELF_CORRELATION 压到 0.7 以下。
- 注意：`1 - maxCorr` 只能压 **SELF**，压不动 **PROD**（生产相关由成分本身决定）。

## 关键杠杆：SUBINDUSTRY 中性化
- 把 `PROD_CORRELATION` 压到 0.7 以下的**决定性因素**是 neutralization 用 **SUBINDUSTRY**（而非 MARKET）。
- 实测（USA KPGvRMg1）：
  - MARKET 中性化下，该 selection 的 PROD 地板 ~0.7169（结构性：用户 book 全是正向生产相关，无负相关成分可抵消）。
  - 换成 **SUBINDUSTRY** 后降到 **0.6944**（<0.7，过闸）。
- 对**单颗 REGULAR alpha**，SUBINDUSTRY 无效（KOR 种子实测：prod-corr 几乎不变，且 sharpe/fitness 反而跌破 LOW 闸）。
  SUBINDUSTRY 只在 **SA 组合层面（10+ 去中心化成分）** 才降 prod-corr。

## 零成本双闸探针（提交前必做）
提交前用以下探针确认，零成本（不消耗配额）：
- `mcp__wq-brain-http__check_self_correlation`：SA 与自身 book 的 max_correlation；若 ≈0.9+ 命中已 ACTIVE 的 SA，Self 闸必拒。
- `mcp__wq-brain-http__check_correlation`（prod）：SA 与已提交 alpha 的 PROD_CORRELATION；若 >0.7 必拒。
- 若探针显示 max_correlation ≈ 0.90–0.92 且 top 命中已有 ACTIVE SA，则该 SA 是近克隆，Self 闸必拒 —— 需换成分。

> 误区提醒：`mcp__wq-brain-http__run_selection` 是**选股（instrument filtering）** 工具，**不是 alpha 选择**（alpha 选择由 SA 的 `selection` 表达式完成）。两者同名易混，务必区分。

## submit 流程（实测）
1. 先用裸 PATCH 写 selection / combo / 两个 description（≥100 英文字；**勿用 set_alpha_properties，SUPER 必 400**，见硬前置 #2）。
2. `mcp__wq-brain-http__workflow_submit_alpha(alpha_id=<ID>, confirm_submit=True, force=True)` → 常返 **201 异步**（status 停在 UNSUBMITTED 是正常的，平台随后计算闸门）。
3. **再调一次** `mcp__wq-brain-http__workflow_submit_alpha(alpha_id=<ID>, confirm_submit=True, force=True)` → 直接回带 **PROD / SELF 值的 verdict**：
   - **403** = FAIL，响应体带具体 value（如 `PROD_CORRELATION 0.7668 > 0.7`）。
   - **200 "IS checks passed"** = 全部过闸，等待 2–3 分钟翻转为 ACTIVE。
4. 命名约定：`name` 用 prodCorrelation 最大值（如 `0.6944`），便于事后回溯。

## 真实案例：USA KPGvRMg1（已 ACTIVE，可作为模板）
（注意：`combination()` 已被平台禁用，此处仅为等价思路说明，实际提交用现行 selection+combo 流程）
- 成分：5 个显式 alpha 的 `combination()` 思路 → 等价体须 PROD≤0.7 且 SELF≤0.7 且 ACTIVE。
- 最终获胜体 `KPGvRMg1`（name=`0.6944`，现 ACTIVE）：PROD_CORRELATION 0.6944、SELF_CORRELATION 0.557、
  sharpe 2.89、fitness 2.39、turnover 0.2194。
- 决定性杠杆：SUBINDUSTRY 中性化（MARKET 天花板 0.7169 → SUBINDUSTRY 0.6944）。

## 真实案例 2：MEA 78jYpn0Z（2026-08-28 ACTIVE，MEA 第 2 颗 SA）
- **组件困境**：自由池仅 6 颗（3 老 + 3 新提），不足 10 → selection 借既有 SA `3qlYKAaO` 内低 prod-corr 成分补齐：
  `((neutralization == "COUNTRY") || (prod_correlation < 0.55)) * (turnover > 0.01) * (turnover < 0.6)`
  —— 自由池 6 颗全 COUNTRY 中性（SA 内部成分多为 SECTOR），`prod_correlation<0.55` 精准借入 4 颗最低 pCorr 的 SECTOR 成分 → 恰好 10 颗。
- **结果**：PROD=0.6996 / SELF=0.6996（双双擦线 <0.7 过闸），与既有 SA 仅 0.4731 相关；
  sharpe 2.52 / fitness 2.99 / turnover 0.052 / subUniverse 2.09 / IS_LADDER 2.93。
- **流程坑**：描述裸 PATCH（见硬前置 #2）后 submit 两次均 200 "IS checks passed"，30s 内翻 OS/ACTIVE。
- **注意**：0.6996 擦线可过但极脆弱——自由池扩到 10 后可重组零重叠变体，降低对借入成分的依赖。

## KOR SA 路线现状与解锁条件
- KOR 现有 192 个数据集、15 个类别（已非 2026-02 快照的 1 个 analyst 族），数据侧已解锁多族来源。
- 但 KOR book **0 ACTIVE REGULAR**，提交配额也可能为 0/4 → 组 SA 的两个硬闸都未满足。
- 解锁路径：
  1. 先在 KOR 挖 **≥10 颗 novel（prod-corr<0.7、彼此低相关）的 REGULAR**，提交使其 ACTIVE
     （消耗提交配额，与 SA 硬闸失败零成本不同）。
  2. 用本 skill 配方组 SA：SUBINDUSTRY 中性化 + `selection(1+0*(prod_correlation>0), score=0.7-prod_correlation, gate self_correlation<0.55, limit≥10)` + `combo(1-maxCorr)`。
  3. `mcp__wq-brain-http__workflow_submit_alpha(alpha_id=<ID>, confirm_submit=True, force=True)` 两次确认 PROD/SELF。
- 因 KOR 组件与 USA book 区域/股票不同，其 prod-corr 与 USA book、self-corr 与 USA SA 天然 <0.7 的概率更高。

## 验证清单
- [ ] 同区域 ACTIVE REGULAR 成分 ≥10 颗。
- [ ] selection/combo 描述经**裸 PATCH** 写入并回读验证长度 >0（set_alpha_properties 对 SUPER 必 400）。
- [ ] neutralization = SUBINDUSTRY。
- [ ] `mcp__wq-brain-http__check_self_correlation` 与 `mcp__wq-brain-http__check_correlation`（prod）探针均 <0.7。
- [ ] `mcp__wq-brain-http__workflow_submit_alpha(alpha_id=<ID>, confirm_submit=True, force=True)` 第二次返回 200 "IS checks passed"。
- [ ] status 翻转为 ACTIVE（2–3 分钟后）。

## 相关 skill
- `worldquant-submit-alpha`：单颗 REGULAR 的提交与硬闸门细节（静默丢弃、翻转延迟、PROD/SELF<0.7）。
- `brain-how-to-pass-AlphaTest`：各 IS 闸门阈值（Fitness/Sharpe/Turnover/Self-Corr/PROD_CORR）。
- `alpha-expression-verifier`：提交前本地校验 selection/combo 表达式语法。
