# 修复配方索引（配方去哪了 · 可复制模板）

> 主文见 [`../SKILL.md`](../SKILL.md)。本页回答两件事：① 旧版声明「已上移」的每个配方**现在在哪**（每一项都由 `tests/unit/07_docs_skills/test_brain_alpha_repair_docs.py` 逐条 grep 校验——「声明已上移的术语必须能在目标文件里找到」）；② turnover / coverage / correlation 三类各给一个可复制的模板与适用条件。

## 一、旧声明逐项核销

旧版 SKILL 写「5 轴旋转、降相关 6 武器、分布形态 → 修复方向映射、news/sentiment 专用方向、幽灵算子警告、体检硬门复验已于 2026-08-23 全部上移进 optimization-v1」。核对结果（2026-09-29）：

| 旧声明的配方 | 现状 | 现在去哪找 | 校验的术语 |
|---|---|---|---|
| 分布形态 → 修复方向映射 | **有**（不在 optimization-v1，在字段体检文档） | [`brain-alpha-research-field-quality/references/webdatascope-data-quality.md`](../../brain-alpha-research-field-quality/references/webdatascope-data-quality.md)（分布形状表与规则 4） | `zero_inflated`、`ceiling`、`kurtosis` |
| 体检硬门复验 | **有**（已是代码闸） | 函数 `tools/webdata_quality.py::check_expr_against_inspect`；闸的处置见 RA [`step5-gates.md`](../../wq-brain-ra-pipeline/references/step5-gates.md)「体检硬门」行（`--inspect-mode`） | `check_expr_against_inspect`、`体检硬门` |
| 幽灵算子警告 | **有** | RA `step5-gates.md` §5.3（三种处置）+ `platform_constraints.json` 的 `ghost_ops`；表达式级检查 `tools/campaign_intel.py ghost-audit` | `ghost_ops`、`幽灵算子` |
| news / sentiment 专用方向 | **有** | [`docs/reference/news_sentiment_playbook.md`](../../../../docs/reference/news_sentiment_playbook.md)（通用菜单在此类数据上适得其反，必须走它） | `news` |
| 降相关（旧称「6 武器」） | **原文已遗失，不可恢复**——首次入库（2026-09-05）时该声明已经存在，而被声明的正文当时就不在 optimization-v1；库内 git 历史里也没有那份配方。**撤回，不再宣称存在** | 现行降相关只有三处：① RA 决策表 **D0-P**（prod 读数怎么处置，[`decision-table.md`](../../wq-brain-ra-pipeline/references/decision-table.md)）；② RA [`step7-diagnose.md`](../../wq-brain-ra-pipeline/references/step7-diagnose.md) 的「找武器」（`tools/forum_recon.py`，向论坛取该墙的解法）；③ optimization-v1 的「组合腿救援」与[形态库](../../wq-brain-alpha-optimization-v1/references/structural-interaction-forms.md) F2（正交化） | `D0-P`、`找武器`、`F2` |
| 5 轴旋转 | **同上：原文已遗失，撤回** | 「换壳（`group_rank` → `group_zscore`）优于磨参数」的结论由 §三 GLB 实证保留；其余无 | — |

**一条纪律**：以后任何文档写「X 已上移到 Y」，必须让 Y 里能 grep 到 X 的关键术语；否则就是断链。`test_brain_alpha_repair_docs.py` 对上表每一行做这个检查。

## 二、三类修复的可复制模板

**先决条件（所有类）**：选定任何算子前先确认它在 `known_ops`（`platform_constraints.json`）里、不在 `ghost_ops` 里，再按 SKILL 的流程过 `ghost-audit` 与 `wave_gate --batch-type repair`。**下表没有库内实测降幅**（仓库里没有「某模板把 turnover 从 x% 降到 y%」的实测记录），所以「预期效果」只写方向，幅度以**小样本实测**为准，并把结果回写到本轮日志。

| 类 | 症状 | 模板 | 适用条件 | 预期效果（方向） |
|---|---|---|---|---|
| **turnover** | `HIGH_TURNOVER`，或 Fitness 因换手偏高偏低 | `ts_decay_linear(<信号>, 5)` 或 `ts_mean(<信号>, 5)`（窗口取白名单 5 / 22）；调高仿真 `decay`；`hump(<信号>, hump=0.01)`（**必须命名参数**）；`ts_target_tvr_hump(<信号>, target_tvr=0.15)` | 信号本身有效、只是跳变多；换手已低于 12.5% 时**不要再降**（Fitness 分母被 floor） | 换手下降；Sharpe 可能小幅下降——先看 Fitness 是否净增 |

**turnover 类实测幅度（2026-10-01，USA/TOP2000/STATISTICAL，唯一一处库内实测）**：外层 `ts_decay_linear(<信号>, D)` 对 Fitness 的净效应存在**甜点区与反转点**，D 越大不等于越好：

| D | turnover | Fitness | SUB | 判定 |
|---|---|---|---|---|
| 无（0） | 0.3534 | 0.84 | — | Fitness FAIL |
| **5** | 0.1398 | **1.41** | 1.38 PASS | ✅ 最优 |
| **10** | 0.0955 | **1.44** | 1.32 PASS | ✅ 次优 |
| 22 | — | — | — | 提交层 504（未取到） |
| 66 | 0.0498 | **1.52**（Fitness 最高） | **1.17 FAIL** | ✗ SUB 被破 |

**结论**：Fitness 随 D 单调上升，但 **SUB 同步下降**——D ≥ 22 时 SUB 会跌破 `0.4333 × S` 门槛（本条 S=2.48，SUB 门槛 1.075，D=66 时 SUB=1.17 已贴线，再大即破）。**⇒ 平滑窗口的唯一合法选定依据是「SUB 仍充裕」**，不是「Fitness 最高」；D 取 5~10 是实测甜点。另：**外层 `ts_decay_linear` 平滑后的 alpha 换手 0.05~0.14 仍远高于 12.5% floor，未触发 Fitness 分母下限**。

**turnover 类第二次实测（2026-10-01 深夜，`forecast_yield_metric_2−3` 价差，USA/TOP2000/STATISTICAL，S≈2.3）**：⚠️ **与上表结论不矛盾但更丰富** —— D 增大时 **F 与 2Y 可同时上升**（这条信号 SUB 始终充裕，未被 D 破闸）：

| D | S | F | 2Y | SUB | 判定 |
|---|---|---|---|---|---|
| 3 | 2.14 | 0.68 | 2.08 PASS | 1.36 | F FAIL |
| 5 | 2.27 | 0.91 | 2.19 PASS | 1.40 | F FAIL |
| **8** | 2.33 | **1.08** | 2.22 PASS | 1.38 | ✅ 全过 |
| **12** | 2.37 | **1.27** | 2.30 PASS | 1.38 | ✅ 全过 |
| **20** | **2.45** | **1.55** | **2.55 PASS** | 1.47 | ✅ **全项更优** |

**⇒ 修正认识**：D 对 F/2Y 的净效应**取决于该信号的 SUB 裕度**——SUB 充裕（≥0.4333×S 有余）时，D 越大越好（F、2Y、S 可同时升）；SUB 贴线时（上表 D=66 案例）D 必须停在甜点。**判据顺序：先看 SUB 裕度 → 再定 D**。**同族不同 D 互为近克隆，只能提交 1 颗。**

## 二-B. ★ 骨架适用边界：「同族双口径价差」不是通用骨架（2026-10-01 实测）

**实测背景**：USA 多塔并行探索（prod06/07/08/09 共 86 条探针），验证 `ts_decay_linear(group_rank(ts_zscore(ts_backfill(subtract(A, B), 252), 252), industry), D)` 骨架的跨塔通用性。

| 塔 / 数据集 | 字段性质 | 骨架效果（最佳 S） | 结论 |
|---|---|---|---|
| **model** / `ai_equity_alpha` | **日频 VECTOR AI 财报因子**（同族多口径） | **2.45**（biz_clarity / forecast_yield） | ✅ **强** |
| analyst / `analyst_consensus` | 预期意外（相对高频） | 1.03 天花板 | ⚠️ 需换形态 |
| PV / `pattern_scores`、`continuation_score` | **形态相似度**（非经济量） | 0.86 | ❌ |
| INSIDERS / `insider_agg_matrix` | **稀疏事件型** | 0.76 | ❌ |
| SENTIMENT / `sentiment22` | 稀疏新闻事件 | 0.16 | ❌ |
| OTHER / `mmp_nlp_sentiment`、`ml_factor_proj` | 文本特征 / ML 投影 | 0.42（含 unknown variable 报错） | ❌ |
| FUNDAMENTAL / `fundamental1` | 低频财报（期权/股权激励） | 0.74 | ❌ |

**⇒ 骨架成立的三要件（缺一即退化）**：
1. **日频连续**（`vec_avg`/`ts_backfill` 后可得密集序列）—— 稀疏事件型、月度/季度字段不满足；
2. **同族多口径估计**（A、B 是同一经济量的不同估计）—— 单一指标无 pair 可用；
3. **字段是经济量而非派生分数**（形态相似度、纯 ML 分数无价差经济含义）。

**代偿方向**：稀疏/低频/非经济量字段需换形态 —— 事件门控（`trade_when`）、`ts_delta`/`ts_av_diff`（修正速率）、`ts_rank`（相对位置）、`ts_sum`/`ts_decay_linear`（事件累积）。
| **coverage** | 体检 `CoverageRatio` < 0.4（长 / 短持仓过少） | `ts_backfill(<字段>, 66)`（低频字段）或 `group_backfill`；VECTOR 字段先经 `vec_avg` 等聚合 | 字段缺失来自更新频率低，而非数据真的没有 | 覆盖率上升、`CONCENTRATED_WEIGHT` 风险下降 |
| **correlation** | `SELF_CORRELATION` / `PROD_CORRELATION` 偏高 | **先读 D0-P，再选动作**：< 0.60 不用修；0.60–0.70 不扩变体、当天进步 8；0.70–0.75 仅 1 次结构性尝试（删腿 / 换广度轴，或 `group_neutralize(同信号, sector)` 包裹）；≥ 0.75 → 换机制 | 见 D0-P；**禁止**磨 decay / 中性化 / 窗口、bucket / 门控 / 平滑、镜像稀释、两条腿相加 | 只在踩线带有救；≥ 0.75 以判死 + 换机制为准 |

## 三、GLB emotion 族降相关失败实证（2026-08-06）

**事实**

| 项 | 值 |
|---|---|
| 候选 | v53–v67 GLB 系列共 **42** 个 `PASS_CHEAP`，全部 emotion 信号族 |
| 结果 | 在 GLB region 上 **100%** 被 `PROD_CORRELATION` 硬闸挡掉 |
| 探针读数 | prodCorr **0.82–0.86**（> 0.7） |
| 覆盖的设置 | 2 个前缀（`sxN_p0q2` / `tdN_p0q2`）× 2 个 universe（`MINVOL1M` / `TOPDIV3000`）× 多种 neutralization，均失败 |

**结论（4 条）**：(a) 不要把同族 `PASS_CHEAP` 当可提交池盲提交——全是死路；(b) 要拿到可提交 alpha 必须**换信号方向 / 降相关（正交化或新数据）**，不是重提交同一族；(c) **换壳（`group_rank` → `group_zscore`）比磨参数更有效**（论坛铁律）；(d) winner 提交后周围 family 变 self wall，需做**更远的 field-level move** 而非同族微调。

**适用范围**：仅 **GLB 的 emotion 族**（实证出处 2026-08-06）；其它区域 / 族不自动适用。结论 (a)(b)(d) 的处置口径以 RA 决策表 **D0-P** 为准（本节不另立学说）；探针一律用只读的 `check_correlation`（家族首探 = 1 条，不是 5 条），**不要**用 `POST /submit` 探测——那通过即真提交，不可撤销。
