---
region: KOR
entry_verdict: active
one_liner: "TOP600 小宇宙：2026-10-03 起唯一活路 = other466 财务比率族（fundamental 塔，等价算子替换 signed_power→quantile 后全闸过）；分析师 / insiders / pv / 图表 / 新闻 / AI / 信用 / risk 全红灯；结构性约束 = 2Y 与 IS 因输入频率此消彼长，CW 闸升级 FAIL"
static:
  universe: [TOP600]
  universe_default: TOP600
  delay: [1]
  delay_default: 1
  neutralization_default: STATISTICAL
  notes: "小宇宙放大 CW/longCount 问题；档位禁止外推"
datasets:
  red:
    - datasets: [acquisition_model, fundamental44, institutions6, model109, model170, model192, model230, model30, model32, model53, multi_source_model, news79, sentiment21, shortinterest3, smoke_ds, wave30_model252]
      reason: "图表形态 3 连死 / 新闻情绪 3 连死 / AI-ML 3 连死 / 信用风险双死；GLB emotion 跨区铁律同禁（键 = ledger *_dead ∪ 旧 red 文本 id；明细查 get_dead_datasets；smoke_ds / wave30_model252 是 ledger 里的测试残留 *_dead 键、不在本区 datasets 表，drift 检查会报 unknown_dataset_ref——已知噪声，清掉要删 ledger 键，未动）"
    - datasets: [insiders5, insider_feats, pv106, pv30, risk59, risk60, risk68, risk70, risk71, risk88, other455, other496, other553, analyst10, analyst16, analyst44, analyst_consensus, fundamental17, fund_holdings_panel]
      reason: "2026-10-03 汇总的 KOR 已判死族（WorkBuddy 记忆 RULES §G）：insiders5 天花板 1.05、insider_feats prod 饱和 0.7185、pv106 流动性天花板 1.1、pv30 聚类标签无信号、risk60 借券域 8 探针 max|S| 0.18、risk70 族连坐 risk88、risk71 MFM2 残差反转 2Y 翻号、risk88 载荷直截面不达线、other455 n2v 网络嵌入全灭、other496 `_t` 时间戳陷阱、other553 分析师绝对值全灭、analyst10/16/44/consensus prod 墙、fundamental17 202 条天花板 1.30、fund_holdings_panel 8/8 RED；族级判死 ≠ 整集死，整集以 get_dead_datasets 为准"
    - scope: family
      families: [chart_patterns, news_sentiment, ai_ml, credit_risk]
      reason: "图表形态 3 连死 / 新闻情绪 3 连死 / AI-ML 3 连死 / 信用风险双死；GLB emotion 跨区铁律同禁"
  green:
    - datasets: [other466]
      note: "旧 green 文本 id ∪ registry win 层实证绑定"
    - scope: family
      families: ["分析师预期变化面只作辅助腿 / 条件（主信号族 analyst10/16/44/consensus 已撞 prod 墙，见 red）"]
      note: "2026-10-04 改写：旧文把 analyst 系 / insiders / pv 整族列绿榜，与 2026-10-02/03 的实证相反（insiders5 天花板 1.05、pv106 / pv30 判死、analyst 族 prod 墙）"
  yellow: ["shortinterest38（输入频率二选一：累积 accum_* 口径 2Y 1.72–1.93 但 S 仅 0.80–0.98，当日 stk_* 口径 S 2.00 但 2Y 1.12–1.20；四闸难兼得，仅作选区先验，非全 KOR 结论）"]
priors:
  signal_families_include: [financial_ratio_fundamental]
  signal_families_exclude: [chart_pattern, news_emotion, ai_ml, credit_risk, glb_emotion, insiders, pv_liquidity, risk_factor, analyst_prod_wall]
  syntax_patterns: []
  win_recipes:
    - "（机制）other466 财务比率族（fundamental 塔 1.6×）：group_rank(divide(经营利润类分子, 资产类分母), market) → ts_rank(·, 504)，外层包装用 quantile 而非 signed_power（signed_power 造成多空不对称并制造「假性不可能三角」）；STATISTICAL；A1NXddRw S2.11 / prod 0.6547 已 ACTIVE。分母口径决定 SELF / prod 墙与 2Y（资产侧 2Y 2.22 vs 权益侧 1.12–1.18），破墙先换分母（WorkBuddy 记忆 2026-09-28 ~ 10-03）"
    - "分析师评级修正 × SH（shortinterest/holders）混合（2 颗 ACTIVE 实证；新波次只复用两类信号的组合机制，落地限条件 / 分组 / 残差，不做加权 / 等权相加——闸 5）"
gate_overrides:
  cw_gate: FAIL
  longcount_verdict: FAIL
loop_policy:
  max_probes_per_wave: 1
  fast_kill: "新数据集 8 探针无 |S|≥0.5 即判死回写，不扩批（小宇宙烧不起配额）"
  stop_conditions: ["白名单被 dead_end 全覆盖"]
empirical_anchor:
  dead_ends_ref: "get_dead_ends(KOR)"
  last_verified: 2026-10-03
---

# KOR — 小宇宙红灯区

## ★ 2026-10-03 现状：七个结构性约束（来源：WorkBuddy 记忆 2026-10-02 一夜实测，MEMORY §1.7）

活路只剩 **other466 财务比率族**。骨架 `signed_power(ts_rank(group_rank(divide(分子, 分母), market), 504), 0.5)` 出过 A1NXddRw（S2.11 / prod 0.6547，ACTIVE）；其后判「不可能三角」时只把 `signed_power(·,0.5)` 换成 `quantile(·)`（骨架全冻结）即 2Y 1.51→1.56、prod 0.6544→0.6397，再把外层轴 sector→market 得 2Y 1.62 全闸过——**那个「三角」是 `signed_power` 造成的假性约束**（决策表 D15 的等价算子扫描前置就来自这里）。

| # | 约束 | 含义 / 处置 |
|---|---|---|
| 1 | 多腿加权违反 `mixed_signal_leg_ban_v1` | 平台 IS 层不拦，我方铁律拦 |
| 2 | 纯单信号结构化过不了 1.58 | risk60 max\|S\| = 0.18；other466 单信号需靠等价算子替换才过 |
| 3 | 混信号形态被闸 5 `POISON:equal_weight_leg_add` 拦 | 经济含义上的「聚合」≠ 结构上的「单一腿」：`add(卖, 买)` 判违规 ⇒ 分母需要聚合时改用单字段分母或 `subtract` 价差 |
| 4 | prod 与 2Y 互斥 | 内层轴 market ↔ industry 反向搬运 |
| 5 | subindustry 轴在 KOR 饱和 | 2Y 0.64 / prod 0.82，双杀 |
| 6 | 净买入族强反向 | S −1.8 ~ −2.2 四年一致，反向后 2Y 仍不够 |
| 7 | **2Y 与 IS 此消彼长的根因 = 输入频率** | 见下表 |

第 7 条（shortinterest38 实证）：

| 口径 | 频率 | S | 2Y | 换手 |
|---|---|---|---|---|
| 累积 `accum_*` | 低频 | 0.80–0.98 | **1.72–1.93** | 0.13 |
| 当日 `stk_*` | 高频 | **2.00–2.01** | 1.12–1.20 | 0.298 |

低频输入出 2Y、高频输入出 IS，四闸要两者兼得 ⇒ 在该数据集上结构上不能同时满足，与机器规则 `sparse_field_long_window_v1` 同向（但更极端：二选一，不是「长窗有效 / 无效」）。**证据只有 shortinterest38 一个族——作选区先验（先问「有没有既高频又低频的字段」），不要当成全 KOR 的结论**。

其余已踩的坑：
- `ts_decay_linear` **不修 `CONCENTRATED_WEIGHT`**：shortinterest38 换手 0.298→0.14（−53%）、S 2.00→2.15，CW 仍 FAIL ⇒ CW 由组内分布集中度决定，不由换手决定；修 CW 须改持仓构造（`trade_when` 门控 / 更多分组轴）。
- FASTEXPR 命名参数：`bucket(x, range="0,1,0.25")` / `bucket(range=, buckets=)`、`hump(x, hump=k)`、`ts_quantile(x, d, driver=)` 可两参；**`quantile(x)` 只接受 1 参**（driver 也不接受）。
- 同族兄弟连提会顶高后来者的 prod（0.67→0.98）：同族一次只提 1 颗。

other466 已测空间（WorkBuddy 记忆 RULES §G，2026-10-02）：已测 28 组合，**分母 18 次集中在 `bs_assets_tot_q`**——分母是最大未测空间。分子池：is_oper_inc_q / cf_oper_q / is_ebitda_oper_q / is_ebit_oper_q / is_ptx_inc_norm_q / is_net_profit_12m_q / is_consol_net_inc_q / is_gross_inc_q / is_net_inc_basic_q / is_int_exp_net_q / q_ngm_xtp_tr / bs_com_eq_retain_earn_q；分母池：bs_assets_tot_q / bs_assets_curr_q / bs_eq_tot_q / des_mkt_cap_q / is_ebit_oper_q / rt_net_mgn_q / q_qe_moc_sb。**prod 饱和字段**：`oth466_bs_assets_tot_q` + `oth466_is_oper_inc_q`（组合命中即拦，须换分子分母）。SUB / 2Y 二分：is_ptx_inc_norm_q → SUB ✅ 但 2Y ❌；is_consol_net_inc_q → 2Y ✅ 但 SUB ❌。

## 定位与实证依据（2026-10-03 之前的历史画像；以上一节为准）

KOR 是 TOP600 小宇宙，挖得最深（wave 95+），20 数据集 exhausted。死路图谱极清晰：**图表形态 3 连死、新闻情绪 3 连死、AI/ML 3 连死、信用风险双死**，外加 GLB emotion 跨区铁律。当时判断的活路是**分析师预期变化面**——评级修正 × SH 混合已产 2 颗 ACTIVE（⚠ 该面后来整族撞 prod 墙，见上；SH 混合属多腿形态，已被闸 5 禁止）。小宇宙的结构性问题：CW（持仓集中度）与 longCount（VECTOR 字段有效长度）问题被放大，事件类数据集 CW>0.5 是通病。

## 流程变体（相对九步骨架）

### 步 2 注入：白名单极窄

- 白名单只留：绿榜（other466）+ status=untried 新集（选集排序看「信息维度是否已在 prod book 里」，别只看 coverage / alphaCount / valueScore——稀疏覆盖的高 valueScore 是陷阱）；
- 金字塔配额冲突时优先**未点亮塔**的未试新集（塔计数按自然季度清零，现查 `campaign_intel.py pyramid --region KOR`）；**不再上提 analyst 族**（2026-10-03：analyst10/16/44/consensus 撞 prod 墙），tier_note 标 `pyramid_quota_kor`；
- 红榜数据集一律不进白名单，即使用户点名——先提示死路 rule 出处（matrix 硬规则 2）。

### 步 3 注入：typed catalog 双查

扫描字段时强制输出每字段 `longCount` 与 `type`：`longCount < 80` 的 VECTOR 字段进观察名单，步 5 闸 7 按 FAIL 处理（见下）。

### 步 5 注入：闸门加严（KOR 核心变体）

| 闸 | 全局默认 | KOR |
|---|---|---|
| 闸 7 longCount<80 | WARN | **FAIL** |
| CW>0.5（步 7 评审） | WARN | **FAIL**（事件类通病实证） |

CW 为动态指标不进静态闸，在步 7 review 时检查：CW>0.5 的 alpha 直接判死不回炉。

### 步 2/6 注入：8 探针快判死

新数据集只给 8 条探针预算：无 |S|≥0.5 即写 dead_end 回写 registry，**不扩批、不换设置重试**。小宇宙配额稀缺，慢判死 = 慢性自杀。

## 避坑清单

- 四大红灯族 + GLB emotion：生成阶段直接排除，不抱"换参数复活"幻想。
- 事件类数据集（earnings 等）：**平台没有 `ts_event_*` 系列**（KOR wave16 实测 8/8 ERROR；闸 8 引用 `type==EVENT` 字段即 FAIL）。先单条探针确认该字段能否直接进标准算子，再生成；预设 CW 必查。旧文「优先生成 `ts_event_*` 裸 rank」已更正。
- 禁止 delay0 外推（KOR 实证仅 delay1）。

## priors
- 拥挤数据集 TOP3（避免重复挖）：pv1(alphaCount=67041, cov=1); analyst15(alphaCount=12004, cov=0.53); model25(alphaCount=9873, cov=0.86)
- 白空间候选（未测 + 覆盖≥60% + 低 alphaCount）：event_stock_model(cov=0.92, alphaCount=1); behavioral_signals(cov=0.87, alphaCount=1); model140(cov=0.79, alphaCount=1); model307(cov=0.67, alphaCount=1); equity_forum_data(cov=0.89, alphaCount=2)
- 已判死（勿重试）：KOR-ANALYST16-EST-PCT-DEAD, KOR-EPS-REVISION-SPREAD-PROD-FLOOR-0723, KOR-FND93-ACCRUALS-DEAD, KOR-FND94-FORWARD-PROFITABILITY, KOR-PV106-COST-DISPERSION-COVERAGE-DEAD, KOR-PV106-LIQUIDITY-WEAK, KOR-RISK60-CROWDDING-NOSIGNAL-20261002, KOR-RISK71-RESIDUAL-REVERSAL-2Y-DEAD
- 实证笔记：KOR-OTHER466-CORE-EARN-YIELD-MKT-WIN: DB 回滚后凭 memory/平台状态重建（原记录在 WAL 期丢失） | KOR-INSIDERS5-CEILING-20260909: 族降级暂停：不再投槽位；与 profile 绿榜不冲突——insiders 数据集天花板低是数据集属性，非方向错误
