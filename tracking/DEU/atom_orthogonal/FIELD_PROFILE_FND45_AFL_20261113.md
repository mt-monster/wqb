# DEU S1 字段画像：fundamental45 / alpha_factor_lib（2026-11-13）

> 归档路径：`tracking/DEU/atom_orthogonal/FIELD_PROFILE_<数据集>_<YYYYMMDD>.md`
> NEWS 面（news17/18）单腿判死后换 FUNDAMENTAL 塔面（换集理由：NEWS 30+ 臂天花板 0.94，7 个升级杠杆全负——见 waveBE223_BE224_NEWS_upgrade_20261113.md）。

## 一、fundamental45（Systematic mining of earnings calls，12 字段全梳理）

| 维度 | 值 |
|---|---|
| 塔位 | DEU/D1/FUNDAMENTAL（1/3 颗，差 2 点亮）×1.8 |
| 平台 cov | 0.269（数据集级）；字段级 0.24-0.32（≈120-160/500 只） |
| 类型 | 全 MATRIX（免 vec_ 包裹） |
| 更新频率 | 季度事件型（电话会日更新，无电话会日 NaN ⇒ ts_backfill 转面板，窗 66 基线律） |
| 近十年 | 待探针 yearly 验证（cov 0.27 无 sentiment7 类断档先验） |

### 字段画像（12/12）

| 字段 | cov | 类型 | 分布/语义 | 机制 | 可用性 |
|---|---:|---|---|---|---|
| `fnd45_sentiment_lm2_net_qa` | 0.2675 | MATRIX | 连续净情绪（LM2 词典，Q&A 段） | **主载体**：Q&A=未准备真话区（最热 user29/37） | ★★★ |
| `fnd45_score` | 0.2675 | MATRIX | 综合分（情绪+可读性+主题合成） | 综合质量分 | ★★★ |
| `fnd45_sentiment_lm2_net_pr` | 0.2675 | MATRIX | 连续净情绪（陈述段） | 与 qa 成对做 spread | ★★★ |
| `fnd45_readability_executives` | 0.2675 | MATRIX | 高管可读性分 | Loughran-McDonald 2011 / Hwang 2012：难读=隐藏坏消息 | ★★ |
| `fnd45_numeric_perct_pr/qa` | 0.2675 | MATRIX | 数字 token 占比 | 数字密度=量化承诺（信息含量代理） | ★★ |
| `fnd45_sentiment_chanage_ceo` | 0.2393 | MATRIX | CEO 情绪变化（vs 前期） | 管理层语气边际（Hoberg 话术漂移） | ★★ |
| `fnd45_sentiment_chanage_othr` | 0.2576 | MATRIX | 其他高管情绪变化 | 同上对照 | ★ |
| `fnd45_sentiment_vader_net_pr/qa` | 0.2675 | MATRIX | Vader 情绪（社媒词典） | 跨模型分歧（vs LM2） | ★ |
| `fnd45_lda_bigram_pr` | 0.275 | MATRIX | LDA 主题分 | 主题漂移 | ★ |
| `fnd45_mktcap` | 0.3162 | MATRIX | 市值（报告期） | 元数据，不作信号（量纲陷阱） | ✗ |

### 机制模板（论文+论坛）

| # | 机制 | 模板 | 来源 |
|---|---|---|---|
| F1 | Q&A 情绪水平/动量 | `group_rank(ts_backfill(fnd45_sentiment_lm2_net_qa, 66), sector)` | Tetlock 电话会情绪 |
| F2 | Q&A−PR 情绪差（真话区 vs 台面话） | `group_rank(ts_backfill(subtract(qa, pr), 66), sector)` | 本战役「跨字段差值有效」判词 |
| F3 | CEO 情绪变化 | `group_rank(ts_backfill(fnd45_sentiment_chanage_ceo, 66), sector)` | Hoberg-Phillips 话术变化 |
| F4 | 可读性反转（难读→负） | `-group_rank(ts_backfill(fnd45_readability_executives, 66), sector)` | Hwang-Kim 2012 |
| F5 | 数字密度（高=具体承诺） | `group_rank(ts_backfill(fnd45_numeric_perct_qa, 66), sector)` | 数字承诺机制 |
| F6 | 情绪 Δ66 | `group_rank(ts_delta(ts_backfill(qa, 66), 22), sector)` | 情绪动量 |
| F7 | LM2 vs Vader 分歧 | `group_rank(ts_backfill(subtract(lm2_qa, vader_qa), 66), sector)` | 跨模型分歧（sentiment27 判词：跨字段构造全正） |
| F8 | 综合分 | `group_rank(ts_backfill(fnd45_score, 66), sector)` | 供应商综合分 |

⚠️ **同机制先验降权说明**：earningscall_sentiment（OTHER 塔）死档 S≤1.02 与本集机制族相近（电话会情绪），但 fnd45 独有「可读性/数字密度/CEO变化/双模型分歧」四维 ⇒ 按「同机制先验只决定优先级」纪律，F1-F6 沿用但预期天花板降权，F4/F5/F7 是差异化主攻。

## 二、alpha_factor_lib（Equity Alpha Factor Library，65 字段）

| 维度 | 值 |
|---|---|
| 平台 cov | **0.0（全部 65 字段）**且 60/65 alphaCount=0 |
| 类型 | 全 VECTOR，行业专用字段（airline/bank/insurance/oil&gas/telecom/homebuilder/hospital 各行业 2-5 字段） |
| 判定 | **数据存在性未证实**：按 §8.11 纪律 cov=0 不是判死依据，但行业字段在 TOP500 内每行业仅 20-50 只 ⇒ 即使有数据，横截面宽度天然塌陷（fnd72 教训：宽度 2-5 → CW 必挂） |
| 动作 | 1 条最小探针（`rank(ts_backfill(vec_avg(<字段>), 250))` + NONE 中性化直读 longCount）测数据存在性；lc/sc < 10 ⇒ 数据层排除（NO_DATA），非信号死 |

### 代表探针字段（userCount>0 者优先）
`broadband_subscribers_one_year_growth`(u1) / `patent_count_to_market_cap`(u1) / `price_to_pre_provision_net_revenue_per_share`(u1) / `wireless_penetration_rate`(u2) / `three_year_change_operating_income_per_tier1_equity`(u1)

## 三、派发计划

- **BE225**：fnd45 十臂（F1-F8 × 变体，MATRIX 免 vec_）+ alpha_factor_lib 2 臂探针
- 并发 2 multisim 内（用户约束）
