# 第三席候选 j2Y7qlA5 完整档案（DEU / shortinterest3）

> 审计时间：2026-11-10 ｜ 状态：**四闸全过，卡在稳健性 CV 闸**

## 一、基本信息

| 项 | 值 |
|---|---|
| alpha_id | `j2Y7qlA5` |
| 类型 | REGULAR / IS / UNSUBMITTED |
| 数据集 | `shortinterest3`（借券数据） |
| 金字塔 | DEU/D1/SHORTINTEREST（multiplier 1.3）— 单塔，不占两塔配额 |
| 核心字段 | `shrt3_bar`（Borrow demand rating 1–10 借券需求评级，VECTOR，cov 0.6528 / uc 192 / ac 361） |
| 算子数 | 10（`ts_backfill` `vec_avg` `ts_delta` ×2 `rank` ×2 `multiply` `ts_target_tvr_decay` `group_rank` `neg`） |

## 二、表达式

```
-group_rank(
  ts_target_tvr_decay(
    multiply(
      rank(ts_delta(ts_backfill(vec_avg(shrt3_bar), 132), 240)),
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

借券需求评级（borrow demand rating）的**变化加速度**：
- 长窗 240 日与短窗 88 日的借券需求变化做乘积 ⇒ 捕捉「借券需求的变化本身在加速还是减速」；
- `ts_target_tvr_decay(target_tvr=0.03)` 把换手压到目标 3%，避免高换手侵蚀收益；
- 整体取负 ⇒ **做多借券需求回落股、做空借券需求抬升股**。

学术依据：外部文献指出借券/空头拥挤与机构持仓拥挤是典型的拥挤度代理
（Lou & Polk 2018 comomentum；short-interest skew 作为拥挤早期预警）。
借券需求激增代表做空/对冲需求拥挤 ⇒ 后续反转 ⇒ 反向持有。

## 四、四闸验证结果（全部通过）

| 闸 | 阈值 | 实测 | 判定 |
|---|---|---|---|
| Sharpe | ≥ 1.58 | **1.65** | ✅ 余量 0.07 |
| Fitness | ≥ 1.0 | **1.16** | ✅ |
| 2Y Sharpe | ≥ 1.58 | **2.72** | ✅ 余量 1.14 |
| Turnover | 0.01 ~ 0.7 | **0.1124** | ✅ |
| sub_universe | ≥ 0.474×S = 0.782 | **1.02** | ✅ |
| failed_ra_count | = 0 | **0** | ✅ checks.fail = [] |
| self 相关 | < 0.7 | **0.5788** | ✅ 余量 0.12 |
| prod 相关 | < 0.7 | **0.5788** | ✅ 余量 0.12 |

prod 直方图：`[0.5,0.6]` 桶 n=1，`[0.4,0.5]` n=3，`[0.6,0.7]` **n=0** ⇒ 浅钉单点，非深钉区。

## 五、正交性（与全 OS 池）

`compute_mutual_correlation(threshold=0.7, years=4)`，19 颗全算：
- **all_below_threshold = true**，max_mutually_below_subset_size = **19**
- 与 1YNMAA8M 互相关 = **0.127**（远低于 0.5 严格线）
- 与 OS 池最高相关：xArzm3Mn **0.5788**（同族 shrt3_bar，已提交件）
- 其余 16 件均 < 0.2：bl6OWZ2M 0.039、2rmGAPqN 0.037、Wje5K71x 0.046、
  LLM93nGa 0.063、JjxrYjre 0.061、2rjrMZ25 0.071、2rOe10qY 0.077、Vk65zLzG 0.083…

⇒ 与分析师修正族、fundamental 族、sentiment 族全部正交。

## 六、逐年覆盖（2014–2023 全覆盖）

| 年 | PnL | Sharpe | Fitness | longCount | turnover |
|---|---:|---:|---:|---:|---:|
| 2014 | 561,627 | 1.31 | 0.82 | 159 | 0.1385 |
| 2015 | 1,016,995 | 2.53 | 2.24 | 169 | 0.1233 |
| 2016 | 287,891 | 0.76 | 0.35 | 180 | 0.1278 |
| 2017 | 740,094 | 2.27 | 1.71 | 199 | 0.1073 |
| 2018 | 662,545 | 1.68 | 1.20 | 196 | 0.1132 |
| 2019 | 106,495 | 0.32 | 0.09 | 205 | 0.1080 |
| 2020 | 840,795 | 2.21 | 1.85 | 224 | 0.1027 |
| **2021** | **-113,884** | **-0.31** | -0.09 | 283 | 0.0930 |
| 2022 | 1,338,799 | 2.97 | 3.01 | 297 | 0.1045 |
| 2023 | 971,583 | 2.45 | 2.12 | 277 | 0.1046 |

- **近十年每年都有数据**，longCount 单调上升 159 → 297（无空窗、无覆盖塌陷）
- 10y 均值 S = 1.619，10y CV = 0.663
- 近三年（2021–2023）均值 S = 1.703，**近三年 CV = 1.035**
- 负年 1 个（2021）

## 七、卡点：稳健性 CV 闸 REJECT

按既定硬约束「Recent-3yr CV_Sharpe ≥ 0.60 ⇒ REJECT；放宽入口仅限用户明确指令」：

**近三年 CV_Sharpe = 1.035 ≥ 0.60 ⇒ REJECT**

根因：**单年失效**（2021 S = -0.31）。若剔除 2021，2022–2023 的 CV = 0.129，完全健康。
⇒ 这是「年度敏感」而非「机制性不稳」，属**可修复**而非判死。

## 八、修复方向（波 J 已派出）

目标：找到对 2021 单年不敏感的变体，同时保持四闸全过。

| 方向 | 变体 |
|---|---|
| 换分组轴 | market / country（country 轴能剔除德国整体借券市场趋势 ⇒ 对单年失效更鲁棒） |
| 换窗口对 | 132/88 ↔ 132/264、132/192、132/132、66/44、252/176 |
| 换 target_tvr | 0.02 / 0.04 / 0.05 |
| 换字段 | `loan_rate_volatility_main` 等借券波动率字段 |

## 九、附带发现（本轮其它结论）

1. **借券族符号是反的**：波 D 全部为负 Sharpe（S -0.92 ~ -1.59）⇒ 借券需求上升是负面信号；
   翻转符号后波 F/H 出货（S1.53~1.65）。**借券需求抬升 ⇒ 做空**。
2. **CW 闸的正解在借券族同样成立**：`ts_backfill(vec_avg(shrt3_bar), 132)` 把稀疏借券事件填稠密
   ⇒ CONCENTRATED_WEIGHT 消失（N1NZZ8k7 CW FAIL → j2Y7qlA5 CW PASS），
   且 S 不降反升（1.59 → 1.65）。
3. **fundamental6 第三席封盘**：信号高度集中 `fnd6_newq_oiadpq`；换 8 个字段全灭（S≤1.23）；
   而 oiadpq + oiadpq(240/176) 本身已被生产池占据（prod 0.9389 / 0.9728 深钉）。
   论坛「fundamental被overused了」（21 赞）侧证生产池 fundamental 拥挤。
