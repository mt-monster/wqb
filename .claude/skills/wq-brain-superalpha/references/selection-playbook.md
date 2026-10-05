# Selection / Combo 打法手册（论坛实证 + 对照本仓缺口）

> 来源：WorldQuant BRAIN 中文论坛（只读 MCP 实测，2026-10-01 检索）。
> 帖子属**未实证输入**：此处收录的是**机制与纪律**，表达式片段须先过闸门再用，不直接当 win 回写。

## 0. 已深读的帖（post_id / 标题 / 票数）

| id | 标题 | 票 | 主要增量 |
|---|---|---|---|
| 35377525887255 | IQC Global Final：Superalpha 的 OS 都长什么样？ | 88 | OS 实证 + 两条警示 |
| 35455109032087 | IQC Global Final：看完了 OS，Superalpha 到底要怎么做？ | 63 | 韩/官方/顾问多方建议汇总 |
| 33745533142679 | [SuperAlpha] SELECTION 框架-v2（游戏王） | 109 | 十步 selection 框架 |
| 33316845356439 | 连续几天 SA 60 刀的秘诀（橘子姐） | 96 | datacategories 分组 `||` |
| 34018758785303 | 【必读】SuperAlpha 入门手册 | 121 | combo 全景 + 官方口径 |
| 41477756114583 | 如何做出低 pc<0.3 SuperAlpha | 18 | 2026 年实践：硬过滤 + 软排序 |

## 1. ★ 头号结论：不要追 IS 业绩指标

- **IQC 顶尖选手的 SA，OS/IS 达到 0.3 的都很少**（35455109032087 原话）。
- 评论区原话（FL39657）："充分说明了**追求高 is 是一件没意义的事情**"。
- 机理：**SA 的 bias 比想象中严重**，单个 RA 的一点 bias 在组合里会被放大；"没有 SA 拿 weight 的机会比 RA 多的说法"（无法探明 SA 里含多少 bias）。
- **garbage in, garbage out**：select 不严 → 系统性过拟合。
- 反面印证：韩方研究员说 IS sharpe 10+、20+ 也 OK，**只要做好 diversity 且不刻意过拟合**。
- 推论：**SA 日收益（1–60 USD）看的是 performance / OS 贡献，不是 IS sharpe**；60 刀打满靠的是多样性与抗风险，不是堆 IS。

### 追高 IS 的两个反作用（本仓实证 + 论坛一致）
1. 抬高 `LOW_SUB_UNIVERSE_SHARPE` 的 limit（≈ 0.431 × IS sharpe，见 levers §6）→ 比值闸**更难**过；
2. 高 IS 常来自同质化强信号 → 推高 prod / self → 双闸更紧、OS 更容易崩。

> ⇒ 判据：**双闸达标 + 多样性达标就提；IS 指标不追。** 「达标即提」不是偷懒，是 IS 与 OS 弱相关下的正确止损。

## 2. diversity 三连（出现频率最高的建议）

35377525887255 ② + 35455109032087 双帖强调：`diversity, diversity, diversity`；`quantity makes quality`。
穿透看还是**相关性**（评论区 LL87164）。落实到表达式：

- **datacategories 分组 `||`**（橘子姐 33316845356439，连续 4 天 SA 60 刀）：
  把类别按**重合度低**分组（如 `[fnd,anl,ern]` / `[news,risk]` / `[other,macro]`），
  每组**独立设条件**，末尾用 `||` 连接 → 强制跨类。
- **分层而非单调阈值**：turnover / long_count / short_count / `sqrt(long_count*short_count)` 都可作分层轴；
  分层的作用是**每次取不同区间，避免重复选中同一批成分**。
- **相关性用区间双边界**，不要一味压低（v2 第 6 步，与 weijie 讨论结论）：
  好因子被反复选到后相关性会升高，一味压低反而选不到它。例：
  `(prod_correlation<0.6 && prod_correlation>0.1) && (self_correlation<0.3 && self_correlation>0.05)`

## 3. 十步框架（游戏王 33745533142679，浓缩）

1. own / not own（Expert+ 才谈 not own）
2. `in(classifications, "ATOM")` / `"POWER_POOL"`
3. **风险中性化**：SLOW / FAST / SLOW_AND_FAST / CROWDING / STATISTICAL / REVERSION_AND_MOMENTUM
4. `in(datacategories, ...)` 按数据类型选（差异大就 fnd+socialmedia，基本面就 fnd+anl+ern）
5. 分层轴：turnover / long_count / short_count / `sqrt(long*short)`
6. 相关性**双边界**（见上）
7. **复杂度上下界**：`operator_count<=8 && >=2 && datafield_count<=3`（一阶因子不稳、能"裸交"的字段质量一般）
8. **参数要有经济学含义**：`decay in {0,1,3,5,20}`（不要 17/29）；`truncation<=0.1`（太高 → PPA weight warning → SA 权重分布不均）
9. **剔除 illiquid universe**：`universe=='TOP2500'`，低流动性挣的钱费后无保障
10. 检查成果 —— 两句金句：
    - **「选择过细等于不选择」**
    - **「设置 selectLimit 不如设置更多的条件」**

其他散点（35455109032087）：
- turnover < **18%**（韩国研究员）
- **combo 不超过 3 个 operator**，且要有实质逻辑
- 因子**容许亏钱**，亏钱就下掉
- 可按 author 平均 sharpe / 排行榜 combine 好的人针对性取因子
- model 数据有人一律剃掉，有人只信 mdl 类"讲道理"的

## 4. Combo

- **等权 `1` 是 baseline，且常常最好**（入门手册：多数复杂组合不如等权；"花里胡哨的组合不如等权"）。
- `combo_a(alpha, mode='algo1'|'algo2'|'algo3')`；多尺度叠加写法（两帖一致推荐）：
  `scale(combo_a(alpha,mode='algo1',nlength=40)) + scale(combo_a(alpha,mode='algo1',nlength=160)) + scale(combo_a(alpha,mode='algo1',nlength=250))`
  （IND 实测：单尺度 S 5.18 vs 三尺度 S 5.02 但 **OS 更稳**；加 self_corr 惩罚后 S 5.52 / F 7.38）
- **★ 本仓 combopo 做对了**：`super_build.py` 的 COMBO_TEMPLATE 用 `self_corr(stats.returns,500)` → `1 - maxCorr`，
  与 41477756114583 评论区实测的降 PC 手段**同一思路**，且幂次放大（power=5）是我们的加强版。保留。
- 硬禁忌：combo **任何情况下不要给负权重**；不要用 sharpe / returns 直接筛选（过拟合）。

## 5. ★ 对照：本仓 `super_build.py` 模板的缺口

当前 SELECTION_TEMPLATE：
```
(1 + 0*(prod_correlation > 0)) * (prod_ceiling - prod_correlation)
* (self_correlation < self_gate) * (turnover > min) * (turnover < max)
```

| # | 缺口 | 论坛依据 | 本仓适用性 |
|---|---|---|---|
| 1 | **无 datacategories 分组 `||`** | 橘子姐 60 刀法 | ⚠ own 池仅 33 颗，最多分 **2 组**，再细会不足 10 颗 |
| 2 | 相关性是**单调**打分，非双边界 | v2 第 6 步 | ✅ 直接改，风险低 |
| 3 | turnover 是**单区间** | v2 第 5 步 | ✅ 改三区间 `||` |
| 4 | 无 `operator_count` / `datafield_count` 界 | v2 第 7 步 | ⚠ 先 `run_selection` 确认 ≥10 颗 |
| 5 | 无 `not(in(competitions,'challenge'))` | 41477756114583 点名 USA | ✅ **USA 必加**，防选到 user alpha，几乎零成本 |
| 6 | 无 illiquid universe 剔除 | v2 第 9 步 | 本仓 USA 成分多为 TOP3000，影响小 |
| 7 | 无 decay 语义限制 | v2 第 8 步 | 看成分分布再定 |
| 8 | combo 无 `combo_a` 多尺度 | 两帖推荐 | ✅ 可作为 `--combo` 变体对照 |

> ⚠ **own 小池警告**：论坛的分层大法面向 **not-own 大池**（GM 可跨国取上千颗）。
> 本仓 USA own 池仅 32 颗 ACTIVE REGULAR，**「选择过细等于不选择」在这里杀伤力最大**——
> 每加一条硬条件都要先 `run_selection` 数出 ≥10 颗再回测。

> ★★ **own 池天花板实证（2026-10-02 全扫描）**：USA own 池 32 颗已被 3 颗存量 SA
> （STATISTICAL/SUBINDUSTRY/MARKET）消耗殆尽，**own 池内无法再组出 PROD 达标的新 SA**（阈值见 config `_PROD_THRESHOLD`）。
> 13 颗候选（6 种中性化 × 多组 decay/sg/pc/sl/cp 参数）全部 BLOCKED：
> - 最优配方 `RAM/d0/sl30/sg0.55/pc0.71/cp5`：SELF 0.691 ✅ / PROD **0.796** ❌（差 0.096）
> - **REVERSION_AND_MOMENTUM 是唯一能过 SELF 闸的中性化档位**（其他全 0.83+）
> - **self_gate=0.55 是 SELF 最优点**（收紧到 0.52/0.50 反升 SELF——踢掉的成分是降 SELF 最有效的）
> - **truncation 无影响**（SA 层 truncation 不改变相关性结构）
> - **combo_power 差异极小**（cp1→cp5：PROD 0.804→0.796）
>
> 结论：要破 own 池天花板，须等 own 池增长（新 RA 提交后扩池）或转向 not-own 大池。

## 6. 建议的 USA 下一代 selection（模板，供 `--selection` 传入）

<!-- lint:counterexample —— 下列是 SuperAlpha selection 表达式（合法算术 `+`/`/` 用于计数与归一化），非 alpha 组合表达式；`+` 不构成 infix_leg_sum 违规 -->

```
(
  (1 + 0*(prod_correlation > 0))
  * (prod_correlation > 0.02) * (prod_correlation < 0.62)
  * (self_correlation > 0.02) * (self_correlation < 0.62)
  * ( (turnover > 0.03 && turnover < 0.10)
      || (turnover > 0.10 && turnover < 0.20)
      || (turnover > 0.20 && turnover < 0.45) )
  * (operator_count >= 2) * (operator_count <= 10)
  * (datafield_count <= 4) * (dataset_count <= 3)
  * (truncation <= 0.1)
  * not(in(competitions, 'challenge'))
)
*
(
     (in(datacategories,'analyst') || in(datacategories,'fundamental'))
  || (in(datacategories,'news') || in(datacategories,'sentiment'))
  || in(datacategories,'pv')
)
* (0.62 - prod_correlation) * (1 - self_correlation)
* (long_count + short_count)
/ ((abs(long_count - short_count) + 100) * (operator_count + dataset_count + datafield_count + 1))
```

使用前必须：① `run_selection` 确认 ≥10 颗；② 不足则按上表从下往上放宽（先去 field/dataset 界，再去 op 界）。
