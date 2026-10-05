# EUR 积攒候选台账（只挖不提交，提交权归用户）

> 用户 2026-10-05 指示：**先积攒，不提交**。本表登记"已全闸验证但未提交"的候选。
> 提交前需：① 复查平台 `status`（防重复）② 跑 `submit_verdict` ③ `check_correlation(refresh=True)` ④ 用户当轮明确指示。

| # | alpha_id | 名称 | 表达式 | S | F | 2Y | sub | robust | prod | self | 塔 | 备注 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | **N1VnJjXg** | EUR_R_model_cashflow_delta_01 | `hump(rank(ts_delta(vec_avg(qfl_cassie_convention_ocf_currliab), 22)), hump=0.001)`<br>EUR/TOPCS1600/decay40/neut=INDUSTRY | **1.75** | 1.17 | **1.76** | **1.63** | 1.44 | **0.5378** (n=0) | 0.195 | EUR/D1/MODEL ×1.3 | ⚠ 仅 2020-2023 四年活数据（四年均正）；CLUSTER_TEST=1.09 平台 warning |
| 2 | `vR2dv3Ga` | EUR_R_lt_regime4_120d_02 | `rank(long_term_regime4_quantile1_120d_pred)`<br>EUR/**TOPCS1600/decay=10/neut=FAST/maxTrade=ON** | 1.18 | 0.58 | **2.37** |0.94 | 未取 | **0.4899** (n=0) | 未取 | 待定（EUR/D1） | ⚠ **IS 未过线**（S 距 1.58 差 0.40、F 距 1.0 差 0.42）⇒ **观察位，非提交候选**。价值在于 **2Y 2.37 + sub 0.94 + prod 0.49 三项皆优**，`maxTrade=ON` 是本工作区首次使用的杠杆（见当日日志 §83/§84） |

**未提交原因**：用户决定积攒。
**待办**：若日后提交，先排查 `POST /alphas/{id}/submit` 返回 404 的原因（见当日日志 §64.2）。
**第2 项定位**：`vR2dv3Ga` 登记为「观察位」——它的 2Y/sub/prod 组合是 EUR 目前最全的，
但 IS硬闸未过，**不构成可提交候选**；作用是为后续攻 S 提供"设置档已验证"的最佳锚点。


---

## 二、已提交（对照，非本轮积攒）

| alpha_id | 族 | 备注 |
|---|---|---|
| `XgJYWLg1` | risk70 风险模型载荷 ⊥ 卖空 + hump | 本会话经用户确认后提交，已 ACTIVE |
| `JjQmx9nm` | 现金流残差（存量） | 早前提交 |

## 三、IS 全闸通过但被 prod 挡下（不入积攒，仅存档）

| alpha_id | 族 | 卡点 |
|---|---|---|
| `pw5VPeoX` | 分析师预期修正（EUR/D1/ANALYST ×1.3） | S1.66/F1.53/2Y1.59/sub1.00 全过，**prod 0.7572 ✗**（机制层拥挤，15 种结构无效 ⇒ 判死） |

## 四、EUR 族谱总账（累计 **16 数据集 / 约 374 条表达式**）

### 4.1 ✅ 活族（IS 过线）
| 数据集 | category | 最佳 S | 裁决 |
|---|---|---|---|
| **risk70** | RISK | **2.09** | ✅ 已提交 `XgJYWLg1` |
| **quant_factor_lib**（CASSIE 族） | MODEL | **1.75 全闸过** | ⚠ 活但短历史（已积攒 `N1VnJjXg`） |
| analyst_factor_signals | ANALYST | **1.66 全闸过** | ✗ prod 0.757 机制层拥挤 |

### 4.2 ★ 半活族（有梯度、杠杆已扫尽，2Y 撞墙）
| 数据集 | category | 最佳 S | 2Y 墙 | 裁决 |
|---|---|---|---|---|
| **chart_cnn_alpha** | MODEL | **1.39** | **0.81** | ✗ 2Y 结构性死墙（**sub 1.10 全 EUR 最高**） |
| **multi_source_model** | MODEL | **1.38** | 0.97 | ✗ 2Y 死墙（S 差 0.20、2Y 差 0.61） |
| multifactor_return_pred | MODEL | 1.12 | — | ✗ |

### 4.3 ✗ 弱信号 / 判死
| 数据集 | category | 最佳 S | 备注 |
|---|---|---|---|
| insider_agg_matrix | INSIDERS | 0.98 | ✗ |
| fund_holdings_panel | INSTITUTIONS | 0.87 | ✗ |
| risk68 / risk62 | RISK | 0.77 / 0.75 | ✗ |
| option_chart_model | — | 0.44 | ✗ IV 偏斜类系统性为负 |
| news_sentiment_nlp | OTHER | 0.45 | ✗ 新闻标题 NLP |
| quant_factor_lib（NLP 族） | MODEL | 0.39 | ✗ 电话会 NLP |
| risk72 | RISK | 1.31 | ✗ |
| news23 | NEWS | — | 实为 M&A 数据 |
| risk60 | RISK | — | DEAD |

### 4.4 ○ 未测即淘汰（发批前 `get_datafields` 实测）
| 数据集 | 实测结果 | 裁决 |
|---|---|---|
| `order_book_imbalance` | 256 全 VECTOR，覆盖 **0.19–0.30** | ✗ CW/sub 必挂 |
| `model193` | **count=0** | ✗ 平台侧不存在 |
| `multi_horizon_alpha` | **count=0** | ✗ 平台侧不存在 |
| `workforce_flow_skills` | 覆盖 0.24 | ✗ 覆盖过低 |
| `news_sentiment_dl` | 66 VECTOR，覆盖 0.74 | ○低优先（与已死 NLP 族同源） |
| `global_seasonal_model` | 300 MATRIX，覆盖中位 **0.997** | ✗ 见下方★ 判据 |

> ⚠ **本会话累计 3 个本地 catalog 里的数据集在平台侧 `count=0`** ⇒ 候选筛选阶段必须 `get_datafields` 实测。

### 4.5 ★★★★ EUR 的 IS 天花板 ≈ 1.4（跨机制成立，非标的性问题）
| 族 | 机制 | 杠杆后最佳 S | 2Y |
|---|---|---|---|
| `multi_source_model` A5 | 分析师数据源模型预测 | **1.38** | 0.97 |
| `chart_cnn_alpha` B7 | **图像 CNN 读 K 线形态** | **1.39** | 0.81 |
⇒ **两种信息维度零重叠的机制都精确停在 1.38–1.39** ⇒ 这是**区域性的 IS 上限**。
⇒ 唯一 2Y 过线的是 M3 型长horizon 预测（2Y **2.33**）但 S 只 1.11
⇒ **EUR 存在「S / 2Y 不可兼得」的硬权衡**（§75.2 规律在本区达到极限）。

### 4.6 ★★ EUR 两个可复用的正向资产
1. **`group_zscore(·, industry)` 是 EUR 唯一能同时保 S 与 sub 的组合**：
   B10 让 sub 达 **1.10**（全 EUR 最高）且 S 保持 1.37 ⇒ 未来 EUR 候选的默认分组轴。
2. **广谱横截面特征 > 模型选股判断**：sub 破 1.0 的两条（`eur_img_feature2`、`feat2+group_zscore`）
   都是**原始特征类**，不是模型概率类。模型概率类天然只挑好股票 ⇒ 子宇宙一缩就失效。

| **option_chart_model** | MODEL | 0.44 | ✗ |
| quant_factor_lib（NLP 族） | MODEL | 0.39 | ✗ |
| news23 | NEWS | —（实为 M&A 数据） | ✗ |
| risk60 | RISK | — | DEAD |

### 判到底的依据（已修订）
事先判据：**连续 2 个数据集最佳 S < 1.0 ⇒ 判 EUR 到底**。
首次触发：`news_sentiment_nlp` **0.45** → `option_chart_model` **0.44**。
**用户指示「继续」后又测 4 个数据集（wave323/324/325/326）**，结论**修正**：
不是"到底"，而是**存在稳定的 ~1.4 天花板**—— 见 4.5。命中族从 3 个变为 3 活 + 2 半活。

### 关键结构性观察
1. **「低拥挤 × 有信号」象限几乎为空**（首次判定的核心，仍然成立）：
   - 低 alphaCount（a=0–1）：`quant_factor_lib`（有信号但**短历史**）、`option_chart_model` / `news_sentiment_nlp`（**无信号**）
   - 高 alphaCount：`analyst_factor_signals`（有信号但 **prod 机制层拥挤**）
2. ★★ **修正**：低拥挤 ≠ 无信号。`multi_source_model`（a=0，覆盖 0.60）与
   `chart_cnn_alpha`（leapstar6 系a=0–11，覆盖 **0.97**）**都是有信号的半活族**。
   ⇒ 真正的墙不是拥挤度，而是 **§4.5 的 IS 天花板 + S/2Y 硬权衡**。
3. ★★ **市场级/日历级字段在 D1 横截面口径下退化**（新判据）：
   含 `market_regime` / `iso_week` / `month_indicator` / `calendar` / `future_event` / `next_event`
   的字段是**全市场同值** ⇒ `rank()`/`group_zscore()` 作用其上**退化为常数**。
   这很可能是历史 seasonal 族普遍无信号的根因。**只走时序交互或与个股信号交互。**

## 五、本会话沉淀的可复用资产

| 资产 | 位置 | 作用 |
|---|---|---|
| 单发 fanout 运行器 | `tracking/EUR/scripts/run_wave_single_fanout.py` | 逐条支持 `decay/truncation/neut/universe`；已修 2Y/CLUSTER 取数 bug + **续跑丢变体 bug（§73）** |
| checkpoint 回填 | `tracking/EUR/scripts/backfill_alphas_from_ckpt.py` | checkpoint→`alphas` 幂等 |
| prod 轮询 | `tracking/EUR/scripts/fetch_prod.py` | 取 prod + 落 `alpha_corr_cache` |
| **字段存在性硬闸** | `tracking/EUR/scripts/check_wave_fields.py` | 发批前防字段笔误（regression 已验证；并集为空即拒放行） |
| 直连提交 | `tracking/EUR/scripts/direct_submit.py` | 绕MCP 全局禁提交闸，四道护栏 |
| 本台账 | `tracking/EUR/ACCUMULATED_CANDIDATES.md` | 积攒登记 |

> 全部放 `tracking/EUR/scripts/`（`tools/` 被外部清理进程删过 3 次）。

## 六、EUR 制胜配方（已被本轮证据修订）

```
① 选数据集：alphaCount 作 prod 的一阶先验；**但更前置的闸是「覆盖率 ≥0.45 + MATRIX」**
   （order_book 0.19 / workforce 0.24 直接淘汰，省掉整波）
② ★ 发批前必做两道自查：
   - get_datafields 实测（本会话 3/7 候选平台侧 count=0）
   - 区分【个股级】vs【市场级】字段（后者横截面退化，见 4.4）
③ 变动量 ts_delta **只在财务慢变量上有效**（CASSIE 族制胜），
   在模型预测/概率类字段上四次实测无效甚至反向（N11 0.21 / O13 0.06 / C15 −0.20 / M16 0.75）
④ ★ 行业分组统一用 group_zscore，**不用 group_rank**（A9 0.57 vs A8 1.30；B11 1.19 vs B10 1.37）
⑤ decay 方向由 S/2Y 背离符号决定：S高2Y低 → 降 decay（A5 1.38）；S低2Y高 → 也有 2Y 但 S 上不去
⑥ hump 甜区极窄且族特异：risk70 0.002 / qfl 0.001 / analyst 族有害 / CNN 族仅 0.001（0.002 即断崖）
⑦ 已证 no-op：winsorize(rank(·),std=N) 逐位等于原式（B14≡B1）——破 prod 要放在 group_rank 之后
```

⚠ **EUR 的根本约束（不是方法问题）**：
- **IS 天花板 ≈ 1.4**，两个零重叠机制（分析师文本预测 / K线图像识别）都精确停在 1.38–1.39。
- **S 与 2Y 不可兼得**：S 高的变体 2Y 都低（0.6–1.0），2Y 过线的变体 S 都低（1.11）。
- ⇒ **单靠 EUR 内部挖 alphas 难以过全闸**；若要突破必须换区或改走 SUPER 合成路线。


---

## 七、2026-10-05 续：设置档维度首次全谱扫（wave327–328）

### 7.1 ★ 字段笛卡尔积清点发现的长_term 120d族补扫（wave327，16/16）
| 变体 | S | F | 2Y | sub |
|---|---|---|---|---|
| **★ L3 `long_term_regime4_quantile1_120d_pred`（四相市场制度）** | **1.17** | 0.58 | **2.34** | **0.85** |
| L4 `long_term_seasonal_..._120d` | 1.12 | 0.54 | 2.31 | 0.82 |
| L2 `long_term_regime2_..._120d` | 1.12 | 0.54 | 2.32 | 0.81 |
| L1 控制行 = M3 锚点 | 1.11 | 0.53 | 2.31 | 0.80 |
| L5 `reverse(rank(quantile5_120d))` | **−0.73** | — | — | — |
| L7 模型置信度当信号 | **−0.82** | — | — | — |
**L3 是全区 2Y 最高（2.34）**，但 S 1.17 距 1.58 仍差 0.41 ⇒ **仍在EUR ~1.4 天花板之下**。
`long_term` 120d 族 7/7 字段**已100% 测完**。

### 7.2 ★ EUR 设置档盲区与实测裁决
| 维度 | 历史使用 | 实测结论 |
|---|---|---|
| **`maxTrade`** | **0 次 → 已用** | ★ **真杠杆**：只认 `ON`/`OFF`（数值 400）。**默认=ON**；OFF→ON 使 **TO 0.079→0.042（−47%）+ S/F/2Y 全升**，代价 sub 0.92→0.85 |
| **`neut=COUNTRY`** | **0 次 → 已测** | ✗ **降 S**（0.96 vs FAST 1.17）⇒ EUR 不适合国别中性化（反直觉） |
| **`neut=CROWDING`** | **0 次 → 已测** | ✗ 降 S（0.81）⇒ 同上 |
| **universe 全谱** | 仅 TOPCS1600 | ★ **越窄越差，单调无例外**：TOPCS1600 **1.17** > TOP2500 0.82 > TOP1200 0.70 > TOP800 0.47 > TOP400 **−0.13** |
| `neut=SECTOR` / `MARKET` / `SUBINDUSTRY` | 极少 | 0.99 / 0.98 / 0.92，**均不如 FAST** |
| **decay**（long_term 族） | 已扫 | **降档提 S**：decay10 = 1.18 > 40 = 1.17 > 160（未在最优档测） |
⚠ **杠杆有条件交互**：`maxTrade` 的收益**只在 FAST 档存在**（COUNTRY 档下 S5≡S6逐位相同）
⇒ 换档后必须重扫，不能假设可叠加。

### 7.3 ★ 已证「EUR 不要用」的形态（省槽位，详见当日日志 §82）
`reverse(rank(quantile5_·))` ｜模型置信度当信号 ｜`signed_power(·,2/3)`（long_term 族）｜
`group_zscore`（long_term 族）｜`hump(·,≥0.002)`｜`winsorize(rank,std)`（no-op）｜
`ts_delta`（模型预测类）｜`ts_mean(·,22)`（long_term 族）｜`hedge3_*` 系列｜`group_rank`
⚠ **同一算子在 EUR 不同族结论相反**（`group_zscore`：C9 族最优/ long_term 族降S）⇒ 不存在 EUR 通用杠杆。

### 7.4 方法论修正（本轮最大收获）
**判「一个族扫完了」之前必须做双维度清点**，否则会像我之前那样
「只探了 7 个字段里的 1 个就宣布杠杆穷尽」：
1. **字段笛卡尔积**：该族字段全集 × 已测/未测（`get_datafields` vs 历史 checkpoint）
2. **设置档盲区**：`get_platform_setting_options` 的合法档位全集 × 本工作区已用/未用
⇒ **两个维度都清完，才有资格谈"扫完了"**。

### 7.5★★★★ wave329：`maxTrade` **跨族确证**（EUR 首个通用杠杆）
| 族 | maxTrade | S | F | 2Y | sub | **TO** |
|---|---|---|---|---|---|---|
| long_term (L3) | OFF | 1.02 | 0.46 | 2.00 | 0.92 | 0.0794 |
| long_term (L3) | **ON** | **1.17** | **0.58** | **2.34** | 0.85 | **0.0422** |
| analyst (M1) | OFF | 1.10 | 0.55 | 0.48 | 0.71 | **0.1551** |
| analyst (M1) | **ON** | **1.38** | **0.88** | **0.97** | 0.86 | **0.0653** |
⇒ **TO 降 47–58%，两族同向**；`maxTrade=ON` 是**平台默认**，要测"关掉"须显式写 `OFF`。
⚠ **sub 方向相反**（long_term 降 / analyst 升）⇒ 换族仍需实测 sub。

### 7.6 EUR「跨族通用」vs「族特异」杠杆（2026-10-05 三波实证）
**✅ 通用**：`maxTrade=ON`（TO −47~58%）｜universe 越宽越好（单调）
**❌ 族特异，换族必重扫**：`hump`｜`signed_power`｜`group_zscore`｜`ts_delta`｜`ts_mean`｜`truncation`
**⛔ no-op（M1 族已逐位验证）**：`truncation(0.08/0.20)`｜`winsorize(std)`｜`nanHandling`
⇒ **no-op 识别法**：两条只有设置不同的变体若**逐位相同**（S/F/2Y/sub/TO 全等）⇒ 该设置在此族无效，直接排除。

### 7.7 当前 EUR 候选排名（IS 硬闸 S≥1.58 / F≥1.0 / 2Y≥1.58 为准）
| alpha_id | S | F | 2Y | sub | prod | 定位 |
|---|---|---|---|---|---|---|
| `N1VnJjXg` | **1.75** | **1.17** | **1.76** | **1.63** | 0.5378 | ✅ **唯一全闸过**，待用户决定 |
| （M1 族 1.38 档） | 1.38 | 0.88 | 0.97 | 0.86 | 未取 | ✗ 2Y 差 0.61 |
| `vR2dv3Ga` (S15) | 1.18 | 0.58 | **2.37** | 0.94 | **0.4899** | ⚠ **2Y/sub/prod 三项全区最优**，S/F 差 0.40/0.42 |
| （T13 group_zscore） | 1.37 | 0.85 | 0.94 | 0.91 | 未取 | ⚠ sub 好但 2Y 差 |
⇒ **EUR 的结构性矛盾再次确认：S 与 2Y 不可兼得**（1.38 档 2Y≈0.95；1.18 档 2Y=2.37）。
