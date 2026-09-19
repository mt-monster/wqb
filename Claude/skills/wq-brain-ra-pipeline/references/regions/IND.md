---
region: IND
entry_verdict: active
one_liner: "TOP500 长窗结构区：2Y Sharpe 强，scale(-rank(x)) 破墙语法实证，评审加 2Y 权重"
static:
  universe: [TOP500]
  universe_default: TOP500
  delay: [1]
  delay_default: 1
  neutralization_default: SUBINDUSTRY
  notes: "长窗结构有效面，单看 IS Sharpe 会误杀"
datasets:
  red: [anl39, qfl]
  red_reason: "anl39/qfl 判死"
  yellow: []
  green: [mdl177（长窗结构）, 慢变量基本面集]
priors:
  signal_families_include: [long_window_structure, slow_fundamental, mdl177_family]
  signal_families_exclude: [anl39_family, qfl_family]
  syntax_patterns:
    - "scale(-rank(x))  # 破墙语法实证：反向缩放排名结构"
  win_recipes:
    - "mdl177 长窗结构族（3 颗 ACTIVE，2Y Sharpe 强）"
gate_overrides:
  cw_gate: WARN
  longcount_min: 80
  prod_corr_early_warn: 0.7
  judge_two_year_sharpe_weight: high
loop_policy:
  max_probes_per_wave: 1
  fast_kill: "新数据集 8 探针无 |S|≥0.5 即判死"
  stop_conditions: ["白名单被 dead_end 全覆盖"]
empirical_anchor:
  dead_ends_ref: "get_dead_ends(IND)"
  last_verified: 2026-08-25
---

# IND — 长窗结构区

## 定位与实证依据

IND TOP500 的有效面在**长窗结构**：mdl177 族已产 3 颗 ACTIVE，共同特征是 IS Sharpe 中等但 **2Y Sharpe 显著强**——长窗信号衰减慢，样本外稳健。anl39 / qfl 判死。另有语法级实证：`scale(-rank(x))` 反向缩放结构在 IND 破墙成功（绕过自检相关性/方向约束），已入 priors。当前 1 颗 submit_ready。

## 流程变体（相对九步骨架）

### 步 4 注入：语法模式入 priors

GEM `--priors-file` 必须携带 `syntax_patterns`：`scale(-rank(x))` 作为推荐骨架模板之一。注意它是**结构模板**不是字段——GEM 仍需概念优先选定字段后套用。

### 步 7/8 注入：评审加 2Y 维度（IND 核心变体）

- 步 7 诊断时拉 `get_alpha_yearly_stats`，`two_year_sharpe` 纳入判定：IS Sharpe 1.0–1.25 但 2Y Sharpe ≥1.5 的候选**不降格、不判死**，进 Mode A 微调（decay/窗口），不进 Mode B 换概念；
- 步 8 judge 阶段向用户报告时必须并列 IS / 2Y 两列，禁止只报 IS Sharpe（IND 误杀主因）。

### 步 6 注入：长窗设置优先

窗口/decay 探索顺序：长窗（≥250d）优先于短窗；decay 大值（≥10）优先。短窗量价族在 IND 无实证支持，探针额度让给长窗。

## 未点亮塔实证（2026-09-19，RA×10 战役 w170-175）

用户约束"已点亮塔不再优先"下，把 IND 全部未点亮塔数据集各探一波（7 集 197 条，STATISTICAL/decay4/TOP500）：**0 候选**。

| 数据集（塔） | n | max\|S\| | 墙 | 结论 |
|---|---|---|---|---|
| sentiment21（sentiment） | 48 | 1.76（fit 0.65, tvr 0.51, 2Y 1.93） | **robust 0.24 / limit 1.0**；HIGH_TURNOVER limit **0.40** | prod 0.16-0.50 干净但结构性 robust 墙 |
| news_sentiment_transfer（sentiment） | 47 | 1.64（反号，新闻关注度冲击反转） | tvr 0.68 + sub_universe | 仅"新闻量变化"有方向信号 |
| news79（news） | 34 | 1.54（反号） | tvr 0.53 + CW（VECTOR 稀疏） | 主题级弱 |
| institutions6（institutions） | 41 | 1.10 | robust | 与 250 日窗旧波同向印证 |
| earnings3（earnings） | 28 | 0.86 | — | dead_end IND-EARNINGS3-TIMING-DEAD（只能作条件腿） |
| shortinterest5（shortinterest） | 7 | 0.22 | CW/tvr=0（价带宽度在 TOP500 无离散度） | dead_end IND-SHORTINTEREST5-PRICEBAND-DEAD |

共性：小票集中型信号在 IND 过不了 `LOW_ROBUST_UNIVERSE_SHARPE`（limit 1.0）；日频稀疏数据 → vec_avg 后 CW 或 ts_backfill 后换手 0.4-0.7（IND 换手闸 0.40 比它区严）。
**这些塔未点亮是结果不是机会**：再投槽位前先跑 `campaign_intel s0-select` 看跨区负先验，并用 `prod-first` + robust 判定分清 prod 墙与结构墙。
剩余未点亮集（imbalance5 2 字段 / macro63 1 字段 / 其它 news 同族）预期同墙。台账：`IND/s6_verdict_unlit_towers_20260919`。

## 避坑清单

- anl39 / qfl 族不进白名单。
- 禁止用 IS Sharpe 单指标判 IND 候选死刑（2Y 强信号会被误杀）。
- `scale(-rank(x))` 不万能：仅用于方向反转型信号，正报型信号套用它必然翻转逻辑。

## robust 墙破解实证（2026-09-19，RA×10 战役 w176-183，analyst_consensus 冷字段）

平台定义（India Alphas 文档）：**IND 额外要求 robust universe Sharpe ≥ 1.0 = 在 BRAIN 选定的流动股子集上的 Sharpe**。
`trade_when(rank(adv20)>0.5, …)` 实测 S 1.05 / robust 0.45 → robust 是"流动股子集重算"，不是权重投影；信号在小票强、大票弱就过不了。

| 形态（P=ts_backfill(vec_avg(f),22)） | S | robust | prod | 结论 |
|---|---|---|---|---|
| `rank(ts_delta(P,66))` 原始变化（EPS flash） | 1.93 | 0.58 | 0.58 | 大票信号弱 |
| `rank(divide(ts_delta(P,66), abs(ts_delay(P,66))+0.01))` 百分比修正 | 2.08 | 0.77 | — | 自归一化 +0.2 |
| `rank(ts_zscore(P,252))` 水平 z（EPS） | 2.12 | 0.73 | **0.73** | prod 撞墙（估计动量拥挤） |
| `rank(ts_zscore(divide(P,close),252))` 前瞻 E/P z | 2.15 | 0.91 | 0.67 | 2Y 1.48 ladder 挂 |
| `rank(ts_zscore(P_pretax,252))` decay 10 | 1.61 | **1.02** | 0.75 | 全 IS 过、prod 挂 |
| `group_rank(ts_zscore(P_pretax,252), bucket(rank(cap),0.1))` d10 | 1.76 | 1.09 | 0.73 | 分桶不改 prod |
| **`group_rank((P−ts_mean(P,252))/(|ts_mean(P,252)|+1), bucket(rank(cap),0.1))` d10 pretax** | **1.60** | **1.11** | **0.65** | **zq8wZgQO 全过（2Y 2.43 / sub 1.28 / self 0.31）** |

规律：① 度量换成 **pretax（税前利润 flash 一致预期）** robust 从 0.7 跳到 1.0（EPS→pretax 大票信息更足）；
② **decay 10** 比 4 再 +0.03 robust；③ **按 cap 十分位 group_rank** 再 +0.07~0.1 robust 且 S +0.1；
④ prod 只由**函数形态**决定：z-score / ts_rank 形态恒 0.73-0.75（2 条外部 prod alpha），**"偏离 1 年均值 / |均值|" 形态降到 0.65-0.67**，分桶/中性化/decay 都不改 prod；
⑤ SECTOR 中性化 S +0.1~0.3 但 robust −0.05~0.1，不用于 robust 卡线者；⑥ ts_mean 504/66 基线、ts_decay_linear 基线、/cap、/close 都更差。
跨区：同信号 USA |S|≤0.09、GLB ≤0.08、HKG 0.64、JPN 不可用（无 pv1 且 VECTOR+ts_* 报错）——**IND 独有**。

## 战役选集硬规则（2026-09-19 用户定案）
**已点亮塔不开战役**：IND 当季已点亮 = analyst(5, 含 pwRJmvP3) / model / risk / other / fundamental → 这些类别的数据集不再作主数据集选波，只能作组腿辅助。
可挖面 = pv（2/3，pv103 尾盘反转族被外部孪生堵死、pv106 判死）、option（option30 fitness 天花板、option1 判死）、earnings（earnings3/earnings11 判死）、news/sentiment（news79/nst/sentiment21/earnings11 判死，news85/84/54 未探）、insiders/institutions/shortinterest/macro/imbalance（判死或字段<5）。
