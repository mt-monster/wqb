# ★★★设置层是独立一维杠杆：nan_handling / 中性化 / decay 扫描（2026-11-12 最重要发现）

> 由 RREPm361 的「对照组只跑出 0.51」倒查发现，牵出四条独立证据。

## 一、触发事故

BE52 的第 5 臂是 RREPm361 表达式的逐字复制（`group_rank(add(ts_zscore(est_12m_ebi_median,240),ts_zscore(subtract(est_12m_ebt_mean,est_12m_ebt_mean_4wks_ago),44)),sector)`），
在我们默认档（decay4/SUBINDUSTRY/nan **ON**）下只跑出 **S 0.51**，而平台记录的 RREPm361 是 **S 2.02**。
逐字查平台 settings 后发现真解：**decay0 / FAST / nan_handling=OFF**。
⇒ **同一表达式，设置差一档，Sharpe 差 1.5**。

## 二、四条独立证据（全部指向同一机制）

1. **RREPm361**：decay0/FAST/nan OFF → 2.02；decay4/SUBINDUSTRY/nan ON → 0.51；
2. **BE71 vs BE70（内部人腿回填与否）**：
   `ts_mean(vec_avg(insd1_holdings),66)`（不回填）→ **1.23**；
   `ts_mean(ts_backfill(vec_avg(insd1_holdings),132),66)`（回填）→ **-0.14**（差 1.37 且符号相反）；
3. **BE51（新闻×I7 加 tail）**：1.46 → -0.43（tail 带通在 rank 腿上毁信号）；
4. **BE57（连续权重视为掩码）**：0.43-0.49（把 0/1 掩码换成连续权重 ⇒ 无申报股乘成 0 ⇒ 巨大并列块）；
5. **外部 DEU 报告（2500+3000 次模拟）**：「中性化配置因信号族而异，行业轴与统计轴分属不同信号族的最优配置，**无全局最优**；decay 2-6 按结构选择」——
   而我们**所有波次固定用 decay4/SUBINDUSTRY/nan ON**，从未做过设置档扫描。

## 三、统一机制

**nan_handling=ON 把无数据股票在数据层填 0**（平台行为，论坛 43178926004887 已实证「nanHandling=ON 把无申报股票填 0 → ts_sum 后仍 0 → group_rank 压成 72-80% 同一值」）。
于是：
- 事件型/缺失型字段（分析师预估、机构持仓、新闻、盈利）**在 nan ON 下必然带巨大并列块**，
  组合的横截面排序被并列块主导 ⇒ IS 被系统性压低（并可能反号）；
- 而**平台自己不是用同一档设置产出那些 alpha 的**（RREPm361 就是 nan OFF + FAST + decay0）——
  **我们一直在用错误的档位测量 DEU 的信号面**。

## 四、纪律（已入记忆）

1. **每个数据集的首波必须做设置档扫描**：nan ON/OFF × 中性化(SUBINDUSTRY/FAST/STATISTICAL/INDUSTRY) × decay(0/4/8)；
2. 事件型字段做组合腿时优先 `ts_mean(·,N)` 不回填；必须回填时先看横截面 rank 的并列占比；
3. 复制存量 alpha 做对照时，**必须连 settings 一起复制**（表达式相同≠信号相同）；
4. 跨信号族无全局最优中性化——按族选档，不按历史默认档。

## 五、已派验证（BE74）

| sim | 设置 | 臂 |
|---|---|---|
| oi7b6d2s4WhaxW15CzROM2E | nan OFF / decay4 / SUBINDUSTRY | 5 |
| 21gZUq7Dz53z92GoD9dw5Lc | nan OFF / decay0 / FAST | 5 |

臂：① P05JM61x 原式 ② 新闻+无回填内部人 ③ 成交额+内部人（1.23 胜配方）④ 内部人单腿 ⑤ 流动性单腿。