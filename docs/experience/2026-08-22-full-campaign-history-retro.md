# 全战役历史总复盘：跨会话经验沉淀（2026-08-22）

> 覆盖 2026-08-01 至 2026-08-22 全部挖掘会话（GLB/USA/GBR/HKG/ASI/EUR/MEA/KOR 八区，300+ 波次）。
> 本文是**跨会话结论层**；单会话细节见各专题文档（见 §8 索引）。
> 数据源：`data/wqb.db`（registry_empirical 34 dead_ends / 6 wins / 27 campaigns + ledger_kv 200+ 键）。

---

## 1. 战役总览

| 区域 | 波次范围 | ACTIVE 产出 | 结局 | 关键配方/死因 |
|---|---|---|---|---|
| GLB | 早期 | 9qpQ0VQ2 等 | 达成 | `group_rank(ts_rank(...), country)` 三区域检查解法；emotion 族 42 条全撞 PROD 0.82-0.86 |
| USA | 波1-6 + option9 | SA KPGvRMg1 | SA 达成，RA 饱和 | book 145 ACTIVE 饱和 value/quality；新提交必须正交信号族 |
| GBR | wave17-36 | **4 ACTIVE**（GrlqxwKx/vRNk56mz/A1G7o1EE/WjAV89jG） | **目标达成** | starmine 四向价值结构、delta66 双时序差分、pattern_scores PV、other455×model264 混合 |
| HKG | wave1-11 | 0 | 终止转 ASI | starmine 价值路天花板 sh1.22 + prod 0.806；情感/趋势类全无截面信号 |
| ASI | wave12-23 | 进行中 | — | cnn/msm/neut 多路探针 |
| EUR | wave1-12 | **Wj71Q12o ACTIVE** | 达成 | FCF 镜像 + pattern gap 稀释破 PROD 墙（0.9013→0.6847，IS 不降反升） |
| MEA | wave50-69 | **4 ACTIVE**（QP7eLAkr/vRjqXeWA/j2jL9x6j/9qXoJge2） | **全数据集判死收官** | analyst 修正广度去相关；区域饱和后主动转区 |
| KOR | wave1-104 | **4 ACTIVE**（88lr21xo/A1lb2KpR + 2 submit_ready） | 进行中（目标 10） | 评级修正×SH 混合（唯一成功路径）；其余 20+ 数据集判死 |

## 2. 六大可复用成功配方（wins 层）

| # | 配方 | 区域 | 核心表达式骨架 | 指标 |
|---|---|---|---|---|
| 1 | **慢变量×快变量跨数据集混合** | KOR | `rank(add(multiply(2, rank(change_6m_rating_revision)), rank(short_horizon_hedge3_quantile1_5d_pred)))`（权重 2:1 / 1:3 均可） | sh1.77-1.83 / 2y2.34-2.52 / 2 RA ACTIVE |
| 2 | **starmine 四向价值结构** | GBR | ep_yield fy2 av_diff + fwdPE 反转 + fy1 水平 + delta66 | sh1.8 / 2y1.62 / margin 10.1bp |
| 3 | **delta66 双时序差分** | GBR | ep_yield delta66/22 双差分家族 | sh1.8 / 2y1.82 |
| 4 | **FCF 镜像稀释破 PROD 墙** | EUR | IS 强的镜像腿 + 与腿相关≈0 的稀释腿组合 | prod 0.90→0.68，IS 反升（见 `prod_wall_breakthrough_sop.md`） |
| 5 | **analyst 修正广度双轴去相关** | MEA | PT raised-breadth + Net est breadth，**去掉 revision 腿** | PROD 0.716→0.6525 破墙，9qXoJge2 ACTIVE |
| 6 | **EPS+Net 修正动量 rank 组合** | MEA | `rank(vec_avg(est_q_eps_mean)/vec_avg(est_q_eps_mean_3mth_ago)-1) + rank(net 同款)` | sh1.61 / fit1.59 / 2y2.41 |

**配方共性**：① 全是复杂经济学结构（多腿/差分/广度比），无一是单字段探针；② 破 PROD 墙靠**结构性去相关**（删腿/稀释/换广度轴），不靠磨参数。

## 3. 跨区结构性铁律（反复实证 ≥2 次）

### 3.1 PROD/SELF 相关墙
- **配方家族扩展天花板**：主导腿（权重 ≥2/3）不变时，任何快腿微调与母配方 SELF 相关必然 ≥0.9（KOR wave94 0.897/0.929、wave95 E10 0.824、wave98 0.991、wave104 0.93/0.98——四次独立实证）。**设计前可预判，不必烧仿真配额**。
- **本地互相关只是下限**：本地池相关 0.61 的候选，平台 PROD 池是全局的（MEA zqkazgld 0.7723 REJECT）；达标候选提交前必须 `check_correlation` 平台侧核验。
- **拥挤风格不可解码**：USA value/quality（book 145 ACTIVE）、GLB emotion（42 条 0.82-0.86）、KOR value/quality 85 草稿、option8 IV 比率（0.83-0.91）——区域隔离不解码风格因子，换区域也救不了同风格。

### 3.2 配方跨区移植不保真
- GBR starmine value 配方（1.78+）移植 KOR 全灭（0.32-0.60，KOR-PREDSTARMINE-VALUE-DEAD）。
- **铁律**：win 配方换区必须重新走 1 批验证，不直接扩展；区域定价效率差异（KOR TOP600 慢变基本面因子定价效率高，只有"预期变化类"信号有效）。

### 3.3 方向错误比无信号更常见
- EUR multi_horizon_alpha 首探 24 条 RED（top 0.61），但 long 因子强负（fcf_to_price sh **-1.9**）→ 镜像探针 `subtract(0, rank(...))` 立即 1.91（wave3b）。
- KOR pv106 wave34A：变化族镜像"方向写反"，等效正向绿灯。
- **铁律**：探针批若有 |sh| ≥1.0 的强负信号，下一批必做镜像反转，不是判死。

### 3.4 结构性硬闸不可磨
- **CONCENTRATED_WEIGHT**：稀疏事件流字段（论坛评论/行为/事件日集中）CW 1.0 结构性无解（KOR equity_forum_data/behavioral_signals/ai_equity_alpha 三族实证）；backfill+线性混合只能缓解轻度 CW。
- **fitness/2y 双天花板**：multi_source_model 5d 组合族四波 40+ 表达式，fitness 天花板 0.99、2y 天花板 1.24（KOR-MSM-5D-COMBO-DEAD）——短周期单数据集族的结构性边界，混合慢变量是唯一出路。
- **差分激活可能反向**：慢变量（修正评分类）做差分/动量激活全转负（KOR wave100、wave99 B2-B4 双实证）——慢信号水平值有效、差分无效甚至反向。

### 3.5 小宇宙与元数据陷阱
- **小宇宙 longCount sanity**：MEA TOP400 VECTOR 字段挖前必须 longCount≥80（pit_or 字段 cov 0.85 但 longCount 11-16 = 伪白空间）。
- **元数据标错类型**：MEA fundamental6 全字段标 VECTOR 实为 EVENT，10 表达式整批 ERROR——新数据集首批必须单仿真探针验证字段可用性。
- **低 alphaCount ≠ 白空间**：小宇宙中 alphaCount≤50 可能是"没人能用"（longCount 0-13），不是"没人挖过"（MEA model25 实证）。

### 3.6 数据集级判死规律
- **图表形态族**：KOR 三连判死（chart_cnn 1.51 / continuation 0.34 / pattern_scores 0.49）；但 GBR pattern_scores PV 变体出过 ACTIVE——形态信号区城依赖，判死只对区域有效。
- **情感/注意力族**：HKG 三连死（0.68/0.51/0.35）、KOR 论坛死——幂律分布 + 稀疏事件流结构性无截面信号。
- **判死纪律**：首探 8 条 5 方向全灭（最高 <0.6）即判死回写，不做第二轮探针（除非发现方向错误线索）。

## 4. 方法论演进（跨会话学习曲线）

1. **阶段 1（08-01~08-08）**：单字段×模板网格扫描 → 教训：32 次无效回测只因没跑体检；建立健康检查硬门槛（cov≥0.85/ac≤50/fc≥10）。
2. **阶段 2（08-08~08-16）**：骨架多样化 + 填槽并发 + 台账闭环 → 吞吐 ×5；CW 墙认识（KOR model170 23+ 变体全败）；混合放大策略固化（加法单调 +0.06/成分，margin 不可修）。
3. **阶段 3（08-16~08-19）**：PROD 墙攻坚 → 镜像稀释破墙（EUR）、结构性去相关（MEA 删腿）；registry 单轨 SQLite + 幂等回写纪律。
4. **阶段 4（08-20~08-22）**：方向纠偏 → 探针批产出率 0 的实证（8 波 64 条）；转向"站在 win 配方上做复杂经济学模板扩展"（wave104 首批 2 GREEN）；发现家族扩展天花板可设计前预判。

**核心元教训**：**批次策略的方向选择比批次数量重要**——挖台账 wins 层做配方扩展的产出率，比盲探新数据集高一个数量级。

## 5. 工程与工具层沉淀（跨会话）

- **multisim 全 ERROR → 先原样重发一次**再怀疑表达式（平台瞬态故障多发；CROWDING 中性化 USA/D0 连续失败才是真不可用）。
- **批内连坐**：一个坏字段/坏算子 → 整批 8 条 CANCELLED（wave78 实证 1 ERROR + 9 CANCELLED）；新字段先单仿真探针。
- **`bucket(x,n)` 输出 Unit[Group:1]**，rank/add 不接受 → 闸6 注入算子改用 if_else/ts_corr/group_zscore（详见 toolkit `references/gate-rules.md` 闸6 节）。
- **metrics_cache 2y 缺失**：跨 dataset 复合表达式 `is.checks` 无 LOW_2Y_SHARPE → 需 `metrics.two_year_sharpe` fallback（EUR retro BUG-1）。
- **PowerShell 内联 Python 引号转义必败** → 一律临时脚本文件（`logs/_*.py`）；`&&` 不支持、`cd /d` 无效。
- **提交静默丢弃双成因**：描述 <100 字（可救）vs 硬闸 FAIL（不可救，只表现为 201+UNSUBMITTED）——用 IS check 区分。

## 6. 当前战线与下一步（2026-08-22 快照）

- **KOR（进行中，目标 10 ACTIVE）**：4 ACTIVE + 2 submit_ready。wave91c 配方家族已达扩展天花板（registry KOR-WAVE104-FAMILY-CORR-DEAD）；下一步：结构性差异化批（换主导信号源，设计前先算与 88lr21xo 的预估相关）+ A4 confidence salvage（1.34 NEAR，先验相关性 <0.7）+ untried 集（model25/other176/model26 金矿 1.7 倍率，需确认与 value 正交）。
- **ASI（进行中）**：wave12-23 探针链。
- **USA option9（独立后台）**。
- **已收官**：MEA（全判死）、GBR（4 ACTIVE 达成）、HKG（转 ASI）、EUR（Wj71Q12o 达成）。

## 7. 对 skill 的回写（本次沉淀动作）

| 层 | 目标 | 内容 |
|---|---|---|
| 决策表 | `brain-deepExplore/references/decision-table.md` | D11（探针 vs 复杂模板，已就位）+ **D12 镜像方向探针 / D13 S1 结构性前置体检 / D14 PROD 墙破墙路由**（本次新增） |
| 闸规则 | `wq-brain-campaign-toolkit/references/gate-rules.md` | 闸6 经济学写法 + bucket 语法限制（已就位） |
| 复盘文档 | `docs/experience/` | 本文 + 专题文档（见 §8） |
| registry | `data/wqb.db` | 34 dead_ends / 6 wins / 27 campaigns（会话内即时回写纪律） |

## 8. 专题文档索引

| 文档 | 覆盖 |
|---|---|
| `project_experience_master.md` | 08-01~08-16：平台规则/体检/算子/提交/并发/监控 |
| `2026-08-18-eur-campaign-retro.md` | EUR 战役：工具 BUG + FCF 镜像破墙 |
| `prod_wall_breakthrough_sop.md` | PROD 墙镜像稀释 SOP |
| `2026-08-22-kor-wave96-104-retro.md` | KOR 近段：探针→复杂模板转向 + 家族天花板 |
| `wq_alpha_mining_knowledge_base.md` / `kor_factor_mining_workflow.md` / `os_alpha_experience_summary.md` / `style_diversity_evaluation_framework.md` | 方法论专题 |
