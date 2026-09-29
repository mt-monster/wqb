# how-to-pass 情景卡：症状 → 根因 → 动作 → 验收

> 主文见 [`../SKILL.md`](../SKILL.md)。本 skill 是**只读诊断**：下面的「动作」只到「建议往哪个方向」，要动手改表达式 → `wq-brain-alpha-optimization-v1`。检查名与线（config 键）见 SKILL §0。

## 卡 HP-1　Fitness 不过，Sharpe 过了

- **症状**：`LOW_FITNESS` FAIL，`LOW_SHARPE` PASS；例：Sharpe 1.6、Returns 6%、Turnover 40%，Fitness ≈ 0.62。
- **根因**：Turnover 太高（`Fitness = Sharpe × sqrt(|Returns| / max(Turnover, 0.125))`，分母大）。
- **动作**：建议用 `ts_decay_linear` / `ts_mean` 把换手压下来——40% → 25% 时 Fitness ≈ 0.78；到 12.5% 时 ≈ 1.11。**换手低于 12.5% 后不要再降**（分母被 floor，Fitness 不再涨；例：Turnover 8% 时仍是 ≈ 1.11）。
- **验收**：重测后 `is.checks` 里 `LOW_FITNESS` 为 `PASS`，且 `LOW_TURNOVER` 没被压出下限。
- **反例**：Turnover 已 8% 还在继续降换手。

## 卡 HP-2　只有 `IS_LADDER_SHARPE` / `LOW_2Y_SHARPE` 不过

- **症状**：全期 Sharpe 不错，两个 2Y 类检查 FAIL。
- **根因**：信号在最近两年不再活着——先分清是**幅度**问题、**集中度**问题还是**机制失效**。
- **动作**：`get_alpha_yearly_stats(alpha_id)` 看逐年 Sharpe，按 [playbook](two-year-sharpe-playbook.md) §0 三分：各年为正只是末两年偏低 → 设置轴 / 表达式轴；某年被少数股拖垮 → 集中度处理；末两年符号反转 → 机制轴，三轴代表变体都不过 → 该 (区域, 家族) 判死。
- **验收**：末两年逐年 Sharpe 转正且两个检查 `PASS`。
- **反例**：在符号反转的家族上继续调 decay / truncation。

## 卡 HP-3　`CONCENTRATED_WEIGHT` = `WARNING`

- **症状**：IS 阶段 `CONCENTRATED_WEIGHT` 显示 `WARNING`（无 value / limit）。
- **根因**：瞬时离散计数 / 事件类信号，权重集中在少数股。
- **动作**：建议对信号加**时间平滑**（`ts_mean` / `ts_decay_linear`，窗口取 5 或 22）；低频字段先 `ts_backfill`。**不要换中性化、不要调 truncation**（实测全无效，见 [证据页](concentrated-weight-evidence.md)）。
- **验收**：重测后该检查为 `PASS`（`WARNING` 计入 Failed RA，不清零不该提交）。
- **反例**：把 neutralization 四档轮流试一遍；末端再套 `rank`。

## 卡 HP-4　`LOW_SUB_UNIVERSE_SHARPE` 不过

- **症状**：子宇宙检查 FAIL 或报 `Sub-universe Sharpe NaN is not above cutoff`。
- **根因**：门槛按比例走——TOP3000 → 子集 TOP1000 时，门槛 = 0.75 × sqrt(1000/3000) ≈ 0.433 倍 alpha Sharpe；alpha Sharpe 1.6 → 子集需 ≥ 0.69。NaN 则是子集覆盖不足。
- **动作**：先抬**整体** Sharpe（门槛跟着整体走）；再去掉与市值相关的乘数、对流动性 / 非流动性分档 decay；NaN → 对字段 `ts_backfill` 或 `pasteurize`。
- **验收**：`LOW_SUB_UNIVERSE_SHARPE` `PASS`。
- **反例**：只盯子集 Sharpe、不管整体 Sharpe。

## 卡 HP-5　SELF ≥ 0.7 与 PROD ≥ 0.7 是两条不同的路

- **症状**：相关性检查 FAIL，但不知道是哪个池。
- **根因**：**SELF** = 与自己已提交的 alpha 太像；**PROD** = 与平台生产池太像。两个池、两条取值路径、两套处置。
- **动作**：SELF → 换 idea / 换数据源（不是换窗口）；PROD → 只按 RA 决策表 D0-P（0.60–0.70 不扩、0.70–0.75 仅 1 次结构性尝试、≥ 0.75 或尝试失败判死），不磨参数。
- **验收**：先确认失败的是哪一项；SELF 失败不去测 PROD 来「验证」。
- **反例**：SELF > 0.7 就下结论 PROD 也 > 0.7。
