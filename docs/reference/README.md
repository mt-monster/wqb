# `docs/reference/` 索引

更新：2026-10-30。本目录是**人读参考层**。流程正文在 skills（`Claude/skills/`），
数据以 `data/wqb.db` 为权威，本目录只放「长期有效的方法论 / 专项模板库 / 区域 runbook /
字段画像快照」。

> ⚠ 多份文件带「现行政策提示（2026-09-29）」：**两条及以上独立信号腿按任意权重线性组合
> 属违规**（含 `add(multiply(…), multiply(…))`、中缀 `+`、`0.5*a + 0.5*b`）。
> 读那些文件时该提示优先于正文示例。

---

## 一、按「我现在要做什么」找

| 我要… | 读这份 |
|---|---|
| 为某个具体数据集设计模板池 | 三·模板库（`template_library_*`）→ 配套字段画像（四·字段画像） |
| 从字段特征推机制骨架 | [field_characteristic_to_mechanism.md](field_characteristic_to_mechanism.md)（含**依据分级**：实测 vs 推断分开标） |
| 走完一次标准特征工程波次 | [feature_engineering_sop.md](feature_engineering_sop.md)（六阶段）＋ [feature_engineering_template.md](feature_engineering_template.md)（波级填表） |
| 从字段画像一路推到产出 alpha | [field_profile_to_alpha_playbook.md](field_profile_to_alpha_playbook.md) |
| 用现成字段画像库判「这个字段值不值得测」 | [field_profile_usage_guide.md](field_profile_usage_guide.md)（`field_profile_perf` 13 区 / 293,060 行） |
| 找一个有经济学含义的表达式骨架 | [economic_alpha_template_library.md](economic_alpha_template_library.md)（T1–T12）＋ [101_formulaic_alphas_kb.md](101_formulaic_alphas_kb.md) |
| 看社区/论坛沉淀的模板 | [community_tpl_library_sequel.md](community_tpl_library_sequel.md)＋ `alpha_template_community.docx`＋ [atom_workflow_and_attribution_20261013.md](atom_workflow_and_attribution_20261013.md) |
| 做 news / sentiment 类 | [news_sentiment_playbook.md](news_sentiment_playbook.md) → [news_bucket_field_map.md](news_bucket_field_map.md) → [news_dataset_portfolio.md](news_dataset_portfolio.md) → [news.md](news.md) |
| 查算子能不能用 / 语法怎么写 | [operator_availability_ledger.md](operator_availability_ledger.md)（实测台账，先读这个）→ [operators_notes.md](operators_notes.md) → [bucket_operator_syntax_fix.md](bucket_operator_syntax_fix.md) |
| 开一个新区域的战役 | 区域 runbook：[ind](ind_campaign_runbook_20261025.md) / [glb](glb_campaign_runbook_20261026.md) / [usa](usa_campaign_runbook_20261025.md)；启动提示词：[campaign_kickoff_prompt.md](campaign_kickoff_prompt.md) |
| 组合两条腿（先确认合规） | [combination_optimization_strategy.md](combination_optimization_strategy.md)（顶部政策提示为准） |
| 组 SUPER alpha | [super_alpha_params.md](super_alpha_params.md)（EUR 实测硬参数） |
| 判某数据集「弱但值得再试」还是「判死」 | [low_priority_probe.md](low_priority_probe.md)（低优先级探针机制，保留翻案口子） |
| 看类别级的已知坑 | [dataset_category_notes.md](dataset_category_notes.md) |
| 长跑进程在 Windows 上别被杀 | [windows_long_process_survival_20261026.md](windows_long_process_survival_20261026.md) |
| 理解 skill 之间的调用关系 | [skill_call_chain.md](skill_call_chain.md)（薄索引，正文在 skills） |
| 提速 S1 字段扫描 | [s1_field_catalog_cache_guide.md](s1_field_catalog_cache_guide.md) |
| 看质量体系设计 | [quality_control_system_design.md](quality_control_system_design.md) → [quality_control_landing_summary.md](quality_control_landing_summary.md) |
| 做多维骨架 A/B | [multidim_ab_test_report_template.md](multidim_ab_test_report_template.md) → [multidim_skeleton_landing_summary.md](multidim_skeleton_landing_summary.md) → [multidim_production_deployment.md](multidim_production_deployment.md) |
| 抄 machine_lib 的预处理惯例 | [machine_lib_experience.md](machine_lib_experience.md) |
| 提交前核对清单 | [ind_submit_checklist_20261020.md](ind_submit_checklist_20261020.md)（判定口径可跨区复用） |

---

## 二、方法论（跨区长期有效）

| 文件 | 定位 |
|---|---|
| [field_characteristic_to_mechanism.md](field_characteristic_to_mechanism.md) | 字段特征 → 机制骨架匹配框架，**每条映射标依据级别**（实测/推断分离） |
| [field_profile_to_alpha_playbook.md](field_profile_to_alpha_playbook.md) | 从字段画像到产出 alpha 的完整作战思路 |
| [field_profile_usage_guide.md](field_profile_usage_guide.md) | 字段画像全景与「值不值得测」的判断流程 |
| [feature_engineering_sop.md](feature_engineering_sop.md) | 六阶段特征工程 SOP（字段理解→筛选→预处理→生成→质量预估→候选池优化） |
| [feature_engineering_template.md](feature_engineering_template.md) | 波级六节式填表模板 |
| [economic_alpha_template_library.md](economic_alpha_template_library.md) | T1–T12 经济学含义骨架库 |
| [101_formulaic_alphas_kb.md](101_formulaic_alphas_kb.md) | Kakushadze 2015 "101 Formulaic Alphas" 知识库（**顶部政策提示优先**） |
| [atom_workflow_and_attribution_20261013.md](atom_workflow_and_attribution_20261013.md) | ATOM 生产流程 + 回测归因（论坛经验整合） |
| [low_priority_probe.md](low_priority_probe.md) | 低优先级探针机制（≥2 次 RED 但结构重构未验证 ⇒ 降级不判死） |
| [dataset_category_notes.md](dataset_category_notes.md) | 各类别已知坑（**不是代码分支**，探针/战役不按 category 分叉） |
| [machine_lib_experience.md](machine_lib_experience.md) | machine_lib.py 预处理惯例（`winsorize(ts_backfill(F,120), std=4)` 等） |

---

## 三、模板库（数据集专项，GBR / TOP700 / D1，均为 2026-10-30）

下面这批是**逐模板、逐条实测**的专项模板库，与二·方法论库的区别是：它们绑定某一个数据集的
字段清单与实测指标，可直接照抄骨架与设置档。

| 文件 | 数据集 | 状态 | 一句话 |
|---|---|---|---|
| [template_library_analyst83_calltranscript_gbr_20261030.md](template_library_analyst83_calltranscript_gbr_20261030.md) | analyst83 | 判死（6 模板 / 5 族） | 电话会议语言数据；最好 S 0.29 = 闸 18.4% |
| [template_library_other384_earningscall_gbr_20261030.md](template_library_other384_earningscall_gbr_20261030.md) | other384 | 判死（6 模板 + E11） | 电话会议 Q&A；三集合并 16 条 0 达标 |
| [template_library_other47_webattention_gbr_20261030.md](template_library_other47_webattention_gbr_20261030.md) | other47 | 判死（8 模板） | SEMrush 流量；含两个元数据陷阱实录 |
| [template_library_pv109_bond_yield_gbr_20261030.md](template_library_pv109_bond_yield_gbr_20261030.md) | pv109 | 判死（6 模板） | 债券收益率类 PV 字段 |
| [template_library_gbr_pattern_scores.md](template_library_gbr_pattern_scores.md) | pattern_scores | **量产中**（423 行，批 30–35 全量记录） | 技术形态相似度（504 MATRIX，PV 单塔）；§13 是三个缺口族方向相反的第一性机制 + `common_gap` 十年全负证据 + gap 字段五族全景 |
| [template_library_gbr_continuation_score.md](template_library_gbr_continuation_score.md) | continuation_score | **量产中**（新档，批 34/36 记录 + 12 模板库） | 姊妹形态数据集（560 MATRIX，PV 单塔）；§2 核心发现「数据集在 gap 族行为是反转，与名字相反」；SUB 闸负 Sharpe 带符号陷阱 |
| [template_library_gbr_fundamental_cap_scaled.md](template_library_gbr_fundamental_cap_scaled.md) | fundamental17 / fundamental72 / fundamental1 / fundamental90 | **量产中**（1094 行，批 1–24 全量记录） | `divide(<科目>, cap)` 缩放基本面；§11 是量比族六轮迭代（SUB/S 0.172→0.449）+ 塔位判据最终修正 |
| [template_library_gbr_fundamental86_scorecard.md](template_library_gbr_fundamental86_scorecard.md) | fundamental86 | **判死（上限 S 0.76）** / 13 模板池 | 7 支柱 decile 评分卡（7 MATRIX，全无量纲）；§2 是「`coverage: 0.0` 不能判无数据」三重取证，§4 三条关键教训（decile 不适合差分 / rank 层非瓶颈 / 支柱等权相减伤 2Y） |
| [template_library_gbr_pv20_beta_term_structure.md](template_library_gbr_pv20_beta_term_structure.md) | pv20 | **β 族判死 / 流动性族在测**（10 模板 T1–T10） | beta 期限结构首发双灭（S 0.33 / −0.24）⇒ PV 主线切 `adv*_usd / mcap` 流动性 |
| [template_library_gbr_other169_cds.md](template_library_gbr_other169_cds.md) | other169 | 判死（最佳 0.66） | CDS mid-par spread；两字段在 GBR 实质等价、覆盖仅 207/700 |
| [template_library_gbr_other567_employee_reviews.md](template_library_gbr_other567_employee_reviews.md) | other567 | 判死（T1/T3 双灭） | 员工评论 5 层字段；`avg_overall_company_score` 最佳 0.11，含 CW 墙 |
| [template_library_gbr_d0_analyst44.md](template_library_gbr_d0_analyst44.md) | analyst44（**D0**） | **判死**（12 模板 / 6 探针） | 分析师修正幅度；最好 S 0.83 = 闸的 31%。§3.0 是 **D0 门槛实测表（S 2.69 = D1 的 1.70 倍）**，§3.4 是「`ts_mean(66)`+decay10 把 TO 150%→4.5%」换手配方 |
| [template_library_gbr_d0_news48.md](template_library_gbr_d0_news48.md) | news48（**D0**） | **探测中**（12 模板） | RavenPack 风格新闻流；22 字段全 VECTOR、18 个 alphaCount=0、coverage 0.7389。§1.7 是「为什么新闻是唯一有真 D0 信息优势的类别」，对比 analyst44 的失败根因 |
| [template_library_gbr_shortinterest3.md](template_library_gbr_shortinterest3.md) | shortinterest3 | **出货 1 条全闸**（35 探针 / 13 模板） | 借券供需族。§6.8 是 `FAST` 中性化把 S 1.56→1.95 / 2Y 1.51→1.96 的**数量级杠杆**（两次独立验证 + 跨数据集复核），产出 `akK2vpWW`（`GBR/D1/SHORTINTEREST` 塔首条、`failed_ra=0`、十年全正） |
| [template_library_gbr_insider_trx.md](template_library_gbr_insider_trx.md) | insider_trx_matrix | 判死（STRUCTURAL-DEAD） | USA 笔数族三颗全闸（S 2.27 / 1.61 / 2.94），但 GBR 迁移失败；价值族 10 模板天花板 \|S\| 0.82 ⇒「笔数/参与广度 > 金额/价值」的原始出处 |
| [template_library_gbr_news104.md](template_library_gbr_news104.md) | news104 | **判死**（8 探针 / 6 结构 / 75% 字段覆盖） | 新闻情绪；最好 S 0.51。核心是**栖息地不匹配第二类**：信息寿命（分钟级）远短于采样窗口（日频） |
| [template_library_gbr_insiders1.md](template_library_gbr_insiders1.md) | insiders1 + **insider_agg_matrix**（**INSIDERS 塔**，倍率 1.5） | **判死 STRUCTURAL-DEAD**（25 模板 / **15 探针**） | GBR 内部人交易全战役。`insiders1` 9 字段全 VECTOR 且**无买卖方向**；`insider_agg_matrix` 34 字段全 MATRIX、买卖股数分离但 8 探针正向天花板 **0.42**。§7.8 = 定则 **I-4**（内部人信号在大盘股专属宇宙结构性失效）+ **I-5**（换窗口安慰剂证伪唯一 \|S\|>0.5 的 −0.60）+ INSIDERS 塔判词 |
| [template_library_gbr_sentiment33.md](template_library_gbr_sentiment33.md) | sentiment33（**SENTIMENT 塔**，倍率 **1.7**） | **探测中**（15 模板 / 6 探针） | 新闻情绪，255 字段全 VECTOR、cov 0.32、alphaCount ≤13（极不拥挤）。§1 = **字段分四类**（A `method_1` token 计数 / **B `method_2/3/4` 0–1 连续评分** / **C `obj` 客观性 0–1 = 现成置信度门控** / D 无极性 feature_1..11），§7.1 = A 类三轴 + B 类基线**四探针全负**（S −0.37~−0.11），§7.2 四条判读（backfill 救 TO 但抹信号 = 定则 #38 复现；「异常注意力」先验跨区不成立；**`investability_ratio` 是第二把尺**，S4 仅 0.108） |
| [template_library_gbr_pv_volume_volatility.md](template_library_gbr_pv_volume_volatility.md) | builtin PV（`volume` / `returns`） | 13 模板，多数判死 | 成交量/波动率族；T6 Amihud 0.03、T12 隔夜跳空 0.08、T13 风险调整动量 −0.64 三线双灭；`trade_when` vol 门控把 TO 腰斩但 2Y 挂 |

配套**机制复盘**（判死边界、可复用教训）在 `reports/dataset_experience/`，索引见
[`reports/dataset_experience/README.md`](../../reports/dataset_experience/README.md)。

另：[community_tpl_library_sequel.md](community_tpl_library_sequel.md)（社区模板库 TPL 系列，人读参考卡）
＋ `alpha_template_community.docx`（用户上传原始件）。

---

## 四、字段画像快照

| 文件 | 区域 / 数据集 | 规模 |
|---|---|---|
| [field_profile_fundamental6_gbr_20261030.md](field_profile_fundamental6_gbr_20261030.md) | GBR / fundamental6 | 643 行，含 10 模板池 |
| [field_profile_news18_gbr_20261030.md](field_profile_news18_gbr_20261030.md) | GBR / news18（Ravenpack） | 301 行 |
| [field_profile_news104_gbr_20261030.md](field_profile_news104_gbr_20261030.md) | GBR / news104 | 142 行 |
| [field_profile_shortinterest3_gbr_20261029.md](field_profile_shortinterest3_gbr_20261029.md) | GBR / shortinterest3 | 204 行，25 字段全 VECTOR |
| [field_profile_ind_inst_fund_20261019.md](field_profile_ind_inst_fund_20261019.md) | IND / institutions6 + fundamental94 + fundamental1 | 456 行，含 earnings3 误判修正 |
| [kor_analyst_field_profiling_20261014.md](kor_analyst_field_profiling_20261014.md) | KOR / ANALYST+MODEL | 157 行，19 集 / 6662 字段 |
| [kor_dataset_field_profiling_20261015.md](kor_dataset_field_profiling_20261015.md) | KOR / 全量 87 集 | 256 行，候选排序 + 入选集画像 |

⚠ 这些都是**快照**。要读当前值，走 `data/wqb.db` 的 `field_profile_perf`（13 区 / 293,060 行，
复合主键 `region+dataset+field`），工具 `tools/fields/field_profile.py`。

---

## 五、区域 runbook

| 文件 | 区域 | 规模 |
|---|---|---|
| [ind_campaign_runbook_20261025.md](ind_campaign_runbook_20261025.md) | IND | 1296 行（本目录最厚），全数据集 × 全模板族流水线 |
| [glb_campaign_runbook_20261026.md](glb_campaign_runbook_20261026.md) | GLB | 121 行，参照 IND 模式区域化 |
| [usa_campaign_runbook_20261025.md](usa_campaign_runbook_20261025.md) | USA | — |
| [usa_d0_mining_experience.md](usa_d0_mining_experience.md) | USA / D0 | — |
| [campaign_kickoff_prompt.md](campaign_kickoff_prompt.md) | 区域无关 | 战役启动提示词模板 |
| [ind_submit_checklist_20261020.md](ind_submit_checklist_20261020.md) | IND（口径可跨区复用） | 提交前核对清单 |

GBR 没有独立 runbook —— 它的区域知识在 `Claude/skills/wq-brain-ra-gbr/SKILL.md`
及其 `references/*.md`（`risk.md` / `fundamental.md` 等）。

---

## 六、news / sentiment 专项

| 文件 | 内容 |
|---|---|
| [news_sentiment_playbook.md](news_sentiment_playbook.md) | 6 桶新闻框架（主文档） |
| [news_bucket_field_map.md](news_bucket_field_map.md) | 5 字段家族 ↔ 6 桶配对规则 |
| [news_dataset_portfolio.md](news_dataset_portfolio.md) | 数据集分层（**2026-04-23 快照，候选源不是路由规则**） |
| [news.md](news.md) | news12（USA/D1 微观结构）字段参考：**无 tone/polarity 标量** |

---

## 七、算子

| 文件 | 内容 |
|---|---|
| [operator_availability_ledger.md](operator_availability_ledger.md) | **算子可用性实测台账 —— 判新算子前先读，别重复踩坑** |
| [operators_catalog.json](operators_catalog.json) | 算子目录（44 KB，机器可读） |
| [operators_notes.md](operators_notes.md) | ⚠ 定性：某账号 7 条 alpha 的**使用统计转储**，**不是幽灵算子清单** |
| [bucket_operator_syntax_fix.md](bucket_operator_syntax_fix.md) | `bucket()` 第二参必须命名参数 `range=` / `buckets=` |

幽灵算子 / 本账号不可访问算子的**单一事实源**不在本目录，而在：
`Claude/skills/wq-brain-campaign-toolkit/config/platform_constraints.json`（`inaccessible_ops`）
＋ `wq-operator-playbook-by-gate` skill。

---

## 八、组合与 SUPER

| 文件 | 内容 |
|---|---|
| [combination_optimization_strategy.md](combination_optimization_strategy.md) | 组合优化策略（**顶部政策提示：权重线性组合违规**） |
| [super_alpha_params.md](super_alpha_params.md) | SUPER alpha 硬参数台账（EUR 实测） |
| [multidim_ab_test_report_template.md](multidim_ab_test_report_template.md) | 多维骨架标签 A/B 实验报告模板 |
| [multidim_skeleton_landing_summary.md](multidim_skeleton_landing_summary.md) | 多维骨架标签系统落地总结 |
| [multidim_production_deployment.md](multidim_production_deployment.md) | 多维骨架标签生产部署 |

---

## 九、质量体系与工程

| 文件 | 内容 |
|---|---|
| [quality_control_system_design.md](quality_control_system_design.md) | 质量改进控制体系设计（模板/字段/表达式/回测多层把控） |
| [quality_control_landing_summary.md](quality_control_landing_summary.md) | 同上，落地总结 |
| [s1_field_catalog_cache_guide.md](s1_field_catalog_cache_guide.md) | S1 字段扫描多层缓存 |
| [skill_call_chain.md](skill_call_chain.md) | Skill 调用链薄索引（正文在 skills） |
| [windows_long_process_survival_20261026.md](windows_long_process_survival_20261026.md) | Windows 长跑进程存活 |
| `101_formulaic_alphas_raw.txt` | 101 Formulaic Alphas 原文（49 KB） |

---

## 维护约定

1. **新增文档先在本索引登记**（表格里加一行），否则下一个人找不到。
2. **文件名带日期**（`_YYYYMMDD`）表示快照；不带日期的是长期方法论，可原地更新。
3. **不要在本目录承载流程正文** —— 流程在 `Claude/skills/`，本目录只做参考。
4. **实测数据以 `data/wqb.db` 为权威**，文档里的数字是快照，冲突时以库为准。
5. 判死类文档必须写清**限制条件**（模板数 / 探针数 / 设置档 / 时间窗），
   否则后人会把「一条机制死」误读成「一个数据集死」。
