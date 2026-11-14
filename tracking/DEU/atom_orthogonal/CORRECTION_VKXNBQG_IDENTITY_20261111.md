# ★档案更正：Vkxnb8QG 不是 pv30 时序动量（2026-11-11 核实）

> 触发：核算 pv30 积压时查平台原始表达式，发现 10-30 面板的标注与平台事实不符。

## 一、平台原始表达式（get_alpha_details）

`trade_when(rank(ts_backfill(vec_avg(mean_loan_rate_main),252)) < 0.75, group_neutralize(group_rank(add(ts_backfill(eps_y1_estimate_change_3mo,1008), ts_mean(ts_backfill(eps_y1_estimate_change_3mo,1008),210)), sector), bucket(rank(ts_mean(ts_backfill(eps_y1_estimate_change_3mo,1008),252)), range="0,1,0.05")), -1)`

- 塔标记：**SHORTINTEREST + ANALYST**（不是 PV）；
- 数据集：shortinterest3（mean_loan_rate_main）+ analyst（eps_y1_estimate_change_3mo）；
- 结构：trade_when 门控（借券利率分位 <0.75）+ group_neutralize + **bucket(rank(...),range="0,1,0.05") 自定义分组**；
- 与 LLM93nGa（11-03 提交）**几乎同构**，仅第一腿是否 ts_backfill(…,1008) 之差 ⇒ self 0.9589 有据。

## 二、三处连带更正

1. 10-30 面板「Vkxnb8QG | time-momentum (pv30) | S1.61」的**数据集标注错误**——它不是 pv30，也不是时序动量；
2. 「pv30 天花板 1.61」**不成立**——pv30 的真实天花板从未被测过（285 字段，PCA 分量族 33 条表达式从未回测）；
3. eps_y1 + mean_loan_rate 的 trade_when/bucket 族**已被两件占用**（LLM93nGa 已 ACTIVE + Vkxnb8QG UNSUBMITTED 互斥）⇒ 该族不可再加；
   同族的「eps_y1 四兄弟」（kqJqQL08/RREXxW6z/6Xdx65eK/1YNv8qaK）亦同此墙。

## 三、方法论

**任何「某数据集出了 Sx 的 alpha」的记录，都必须用 get_alpha_details(code) 核对原始表达式后才能写入处置表**——
波次表格的简写（数据集·字段·骨架）会错标，两次踩坑（BE43a 符号、此处数据集）。