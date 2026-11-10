> **[2026-11-10 09:45 UPDATE - VERDICT: REJECT, DO NOT SUBMIT]**
> Per brain-alpha-robustness/SKILL.md Phase C table (authoritative: population sd, 3-tier verdict):
> **Recent-3yr max/min Sharpe ratio = 3.00 / 0.50 = 6.00 > 5 => REJECT** (submit_verdict measured BLOCKED / ROBUSTNESS_REJECT).
> This doc ranked it family rep by sample-sd CV 0.665 - that was the wrong convention.
> **Family rep should be E569ZE7L** (264/132 + subindustry, max/min 4.80 => CONDITIONAL, not REJECT).
> See reports/robustness_20261110.md.

# 第三席最终候选 9qxnNkeq 完整档案（DEU / shortinterest3）

> 审计时间：2026-11-10 ｜ 状态：**四闸全过 + prod/self 双过 + 稳健性 CV 最优**

## 一、基本信息

| 项 | 值 |
|---|---|
| alpha_id | **`9qxnNkeq`** |
| 类型 | REGULAR / IS / UNSUBMITTED |
| 数据集 | `shortinterest3`（借券数据，DEU 未点亮塔） |
| 金字塔 | DEU/D1/SHORTINTEREST（multiplier 1.3）— 单塔 ATOM，不占两塔配额 |
| 核心字段 | `shrt3_bar`（Borrow demand rating 1–10 借券需求评级，VECTOR，cov 0.6528 / uc 192 / ac 361） |
| 算子数 | 10 |

## 二、表达式

```
-group_rank(
  ts_target_tvr_decay(
    multiply(
      rank(ts_delta(ts_backfill(vec_avg(shrt3_bar), 132), 264)),
      rank(ts_delta(ts_backfill(vec_avg(shrt3_bar), 132), 88))
    ),
    target_tvr=0.03
  ),
  subindustry
)
```

设置：DEU / TOP500 / delay1 / decay4 / neutralization **FAST** / truncation 0.08 /
pasteurization ON / unitHandling VERIFY / nanHandling **ON** / maxTrade OFF

## 三、经济机制

借券需求评级的**长短期变化加速度**，反向持有：
- 长窗 264 日 × 短窗 88 日的借券需求变化做乘积 ⇒ 刻画借券需求的「变化趋势」而非「水平」；
- `ts_backfill(vec_avg(shrt3_bar), 132)` 把稀疏借券事件填稠密（解决 CONCENTRATED_WEIGHT 的结构性来源）；
- `ts_target_tvr_decay(target_tvr=0.03)` 把换手压到目标 3%；
- 整体取负 ⇒ **做多借券需求回落股、做空借券需求抬升股**。

学术支撑（外部文献）：借券 / 空头拥挤是机构拥挤度的经典代理（Lou & Polk 2018 comomentum；
short-interest skew 作为拥挤早期预警；McLean & Pontiff 2016 因子拥挤与衰减）。
借券需求激增 = 做空/对冲需求拥挤 ⇒ 后续反转 ⇒ 反向持有。
论坛侧证：「ts_target_tvr_decay 行为探索与 Sharpe 求解」（47 赞）确认该算子可用于换手约束下的信号构造。

## 四、四闸验证（全部通过）

| 闸 | 阈值 | 实测 | 判定 |
|---|---|---|---|
| Sharpe | ≥ 1.58 | **1.66** | ✅ |
| Fitness | ≥ 1.0 | **1.18** | ✅ |
| 2Y Sharpe | ≥ 1.58 | **2.69** | ✅ |
| Turnover | 0.01 ~ 0.7 | **0.1117** | ✅ |
| sub_universe | ≥ 0.474×S = 0.787 | **0.87** | ✅ |
| failed_ra_count | = 0 | **0** | ✅ checks.fail = [] |
| self 相关 | < 0.7 | **0.5327** | ✅ 余量 0.167 |
| prod 相关 | < 0.7 | **0.5327** | ✅ 余量 0.167 |

prod 直方图：`[0.4,0.5]` n=1、`[0.5,0.6]` n=1、**无 [0.6,1] 桶** ⇒ 无深钉区。

## 五、正交性

`compute_mutual_correlation(threshold=0.7, years=4)`，21 颗全算：
- 与 **1YNMAA8M = 0.1259**（远低于 0.5 严格线）
- 与 OS 池 17 件最高相关：xArzm3Mn **0.5327**（同族 shrt3_bar，已提交件）
- 其余 16 件均 < 0.18：bl6OWZ2M 0.0281、Wje5K71x 0.0289、2rmGAPqN 0.0483、
  LLM93nGa 0.0555、JjxrYjre 0.0784、2rOe10qY 0.077、2rjrMZ25 0.0811…
- 与全部 17 件 OS REGULAR 构成 **18/18 完整独立集**（all_below_threshold=true）

## 六、逐年覆盖（2014–2023 全覆盖）

| 年 | PnL | Sharpe | Fitness | longCount |
|---|---:|---:|---:|---:|
| 2014 | 446,878 | 1.05 | 0.58 | 159 |
| 2015 | 884,734 | 2.26 | 1.86 | 169 |
| 2016 | 32,460 | 0.09 | 0.01 | 182 |
| 2017 | 804,867 | 2.38 | 1.87 | 200 |
| 2018 | 632,260 | 1.62 | 1.13 | 198 |
| 2019 | 209,881 | 0.60 | 0.24 | 205 |
| 2020 | 956,620 | 2.54 | 2.27 | 223 |
| 2021 | 184,314 | **0.50** | 0.19 | 284 |
| 2022 | 1,396,575 | 3.00 | 3.11 | 299 |
| 2023 | 946,076 | 2.35 | 2.01 | 277 |

- **近十年每年都有数据**，longCount 159 → 299 单调上升，无空窗
- 10y 均值 S = 1.620，10y CV = 0.618
- **近三年（2021–2023）均值 S = 1.950，CV = 0.665**
- **无负年**（最低 2016 年 0.09）

## 七、稳健性闸状态（★ 需用户裁定）

既定硬约束：Recent-3yr CV_Sharpe ≥ 0.60 ⇒ REJECT；放宽入口仅限用户明确指令。

**9qxnNkeq 近三年 CV = 0.665 ≥ 0.60 ⇒ 按字面判定 REJECT。**

但它是本轮借券族 5 颗候选中 CV 最优者，且已修复原始 j2Y7qlA5 的单年失效：

| 候选 | 窗口对/轴 | 3y CV | 3y 值 | 负年 | prod | self |
|---|---|---:|---|---:|---:|---:|
| **9qxnNkeq** | 264/88 subindustry | **0.665** | 0.50, 3.00, 2.35 | **0** | 0.5327 | 0.5327 |
| kqNAz9pP | 132/88 market | 0.925 | 0.06, 3.63, 2.12 | 0 | 0.5154 | 0.5071 |
| 1YNMr08m | 132/88 country | 0.925 | 0.06, 3.63, 2.12 | 0 | — | 0.5071 |
| j2Y7qlA5 | 132/88 subindustry | 1.035 | -0.31, 2.97, 2.45 | 1 | 0.5788 | 0.5788 |
| E56d9xnP | 66/44 market | 1.112 | -0.40, 3.86, 2.37 | 1 | — | 0.4228 |

**关键归因**：借券族近三年两极分化是**数据环境特性**——2021 年德国借券市场几无波动
（借券评级变化信号近乎失效），2022 年极端反弹。所有窗口变体在 2021 年都退化，
说明这不是选样问题而是该年借券数据的信息量本身不足。

⇒ 处置选项：
1. 用户明确授权放宽 CV 闸至 0.70 ⇒ 9qxnNkeq 立即可提交（其余四闸 + prod/self 全过）；
2. 维持 CV 闸 ⇒ 借券族本轮无法出货，继续在别的机制族找第三席。

## 八、同族容量终判

借券族三颗候选内部互相关：
9qxnNkeq~j2Y7qlA5 **0.9009**、kqNAz9pP~j2Y7qlA5 **0.7974**、9qxnNkeq~kqNAz9pP **0.7583**
⇒ **借券族最多出 1 席**，三选一，9qxnNkeq 为最优。

## 九、本轮附带结论

1. **借券族符号是反的**：波 D 全部 S 为负（-0.92 ~ -1.59）⇒ 借券需求上升是负面信号；
   翻转符号后出货（S1.53~1.66）。**借券需求抬升 ⇒ 做空**。
2. **CW 闸正解在借券族同样成立**：`ts_backfill(vec_avg(...), 132)` 把稀疏事件填稠密
   ⇒ CONCENTRATED_WEIGHT 消失（VkxWWPJb CW FAIL → j2Y7qlA5 CW PASS），S 不降反升（1.59→1.65）。
3. **fundamental6 第三席封盘**：信号高度集中 `fnd6_newq_oiadpq`；换 8 个字段全灭（S≤1.23）；
   oiadpq + 240/176 本身已被生产池占据（prod 0.9389 / 0.9728 深钉）。
4. **单字段单窗口季度差分无效**：波 A 10 条全灭（S 0.23~1.04）；必须走
   「双窗口加速度 × target_tvr_decay」结构。
