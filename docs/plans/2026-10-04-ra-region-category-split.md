# RA 九步流程「区域 × 类别」拆分方案（实施方案）

日期：2026-10-04　性质：方案（§0–§8）+ **落地记录（§9，用户随后要求「还是给区域 / 组合拆分实现」「按最佳方案决策落地」）**。没有提交，数据库全部只读访问（sqlite `mode=ro`），没有碰 `.workbuddy/`。
承接：`skills_workflow_review_20261003.md`、`skills_workflow_fix_record_20261004.md`、`docs/skills_review_decisions.md` DEC-72 ~ DEC-78（IND / EUR probe-only、DEU 保持 active、加权稀释退役等结论直接沿用，不重推）。

> **用户覆盖了 §0 的决定 1**：§0 按 30% 线主张「本期不建区域子 skill」，用户随后明确要求拆出区域 / 组合，以便逐区把控回测。落地时按用户指令建了 14 个区域 skill 与 103 个组合分支文件，但仍守住 §3 的原则：组合只存覆盖值与本组合知识（不复制区域缺省）、区域差异进数据层、锁定表不可放宽。见 §9。

---

## 0. 结论先行

1. **按你给的 30% 判据实测，S1 / S2 / S4 / S5 没有任何区域过线**：显式「步 N 注入」差异最高是 IND 步 8 的 18%；把「现状 / 约束 / 避坑」这类混合段落和自动生成的 priors 数据全算进去，S1/S2/S4/S5 最高也只有 KOR 步 4 的 28%。唯一过线的类别是新闻 / 情绪（约 35%），它早已是独立 skill（`brain-alpha-research-news-sentiment`）。⇒ **本期不新建区域子 skill，也不建 13 × 9 的矩阵式流程。**
2. **真正的问题不是「没拆」，是现有的区域注入在漏**：同一个中性化参数有 7 处来源、13 个区里 7 个区答案互相矛盾；按字面量扫描，thresholds.json 有 6–25% 的键找不到读取方；KOR「闸 7 / CW 升 FAIL」只写在文档里，代码恒为 WARN；Mode B 主闸在 7 个区的生效值低于你定的 1.25 / 0.8（EUR 是自适应学习器自己学低的）。在这个底座上再加一个类别维度，这些问题会乘以 9。
3. **目标架构 = 一个九步骨架 + 四层知识（全局 / 类别卡 / 区域画像 / 稀疏格子）+ 一个解析器 + 一张锁定表。** 你要求每个「区域 × 类别」都有的四件东西（生成策略、回测参数、S4 配方、判死与资格阈值），由解析器按层合成，每个值都能查到来源；只有证据过线的组合才存自己的差异（现在 22 个格子过线，其中只有 2 个有绑定到数据集的胜绩）。
4. **迁移分 5 个 Phase**：Phase 0 测基线；Phase 1（P0）修漏、锁纪律，不加新维度；Phase 2 把类别维度做成数据；Phase 3 绑定证据、建稀疏格子、接 S4；Phase 4 把「该不该拆 skill」交给机检工具。

### 我替你定的事（按性价比）

| # | 问题 | 决定 | 依据 |
|---|---|---|---|
| 1 | 要不要给区域 / 组合建独立子 skill | 本期不建；拆分交给 Phase 4 的机检 | 30% 线实测无一过（§2.5）；124 个有证据的格子里只有 11 个回测 ≥ 200 条（§2.4） |
| 2 | 「每个组合拥有四件东西」怎么落 | 由解析器合成，不做物理副本；只有过线格子存差异 | 238 个可能格子里约一半零证据，副本只会漂移 |
| 3 | 格子建档线 | ≥ 1 条绑定胜绩，或 ≥ 3 条绑定判死；frozen 区不建；probe-only 区只做知识存档 | 现有 22 个过线（活跃区 12 个） |
| 4 | 「类别」用哪个口径 | 键 = 平台类别（塔口径不能动）；机制类别只用于 S2 / S4 检索；Pattern 作 pv / model 的族标签；首批 10 张类别卡 | `pattern_scores` / `continuation_score` 平台类别就是 PV；`other` 内部异质（§2.1） |
| 5 | 回测参数分到哪层 | universe / delay 只到区域；中性化 / decay / nanHandling / maxTrade 可到格子（以「win 设置 + 证据」形式）；truncation 不进任何层 | D5：truncation 零杠杆（IND、GLB 实测），设置是强度闸、换档即换信号 |
| 6 | Mode B 1.25 / 0.8 | 锁定为下限，只许收紧；读时钳制、不写库 | 你这次把它列为纪律；与 09-09 GLOBAL 台账「区域可覆盖单字段」冲突，以这次为准，回退只需去掉钳制 |
| 7 | 阈值覆盖的规矩 | 不得低于平台线；每个覆盖必须带证据；没有消费者的键删除 | 6–25% 的键无人读（§2.3） |
| 8 | 机读数据放哪 | JSON（`src/wqb/profiles/`、`tracking/<R>/config/cells.json`）；md 只放人读正文和生成的摘要块 | 仓库没有 YAML 依赖，现有 front-matter 靠正则解析，`assemble_priors._profile_fallback` 会把所有引号列表项当胜绩配方 |
| 9 | 解析器的入口 | 先出 CLI；MCP 工具等输出格式稳定后再加 | 改 `wqb_db_mcp.py` 成本高（AGENTS.md §8.4 第 9 条） |
| 10 | 闸 7 / CW「真执行」何时落 | 放到 2026-10-12 区域闸转 enforce（TB-02）观察一波之后 | 两处行为变化叠加，出问题无法归因 |
| 11 | S5 要不要按区域 / 类别分支 | 永不 | 平台 checks 已给出区域化的 limit（CLUSTER、robust、SUB 比值）；再写一份就是第二个真相源 |
| 12 | 拆 skill 的判据 | 你的 30% 线 + 控制流不同 + 证据线 + 区域 active，四条同时满足 | 现有两个成功拆分（新闻情绪、饱和集假设优先）都是控制流不同，不只是篇幅大 |
| 13 | GEM 里三处类别知识 | 收敛为类别卡一处；`prompt_kb`（0 行）冻结；`economic_mechanism_kb` 并入类别卡，去掉无实证的区域适配 | §2.2 |

---

## 1. 依据与口径

- **代码与配置**：`build_wave.py` / `pipeline.py` / `gate.py` / `review_wave.py` / `score_datasets.py` / `assemble_priors.py` / `_lib/rules.py` / `_lib/region_kb.py`（toolkit）、`src/wqb/workflow/mode_b_config.py` / `mode_b_adaptive.py` / `nodes/campaign.py` / `nodes/gem.py` / `structural_variants.py`、GEM 的 `economic_priors.py` / `pipeline_prompts.py` / `skeletons.py` / `prompt_kb.py`、`tools/economic_mechanism_kb.py` / `campaign_intel.py`、13 区 `tracking/<R>/config/{settings,thresholds}.json`、14 份区域 profile。
- **数据库**（只读）：`backtest_results` 9,989 行、`registry_empirical` 756 行、`datasets` 1,904 行、`ledger_kv`（`mode_b_qualification`、`region_kb`、`methodology_rules`）。
- **记忆**：`.workbuddy/memory/MEMORY.md`、`RULES.md` 全文，日志沿用昨日审查的取证；`docs/experience/`；Claude 侧记忆。
- **找不到的两样东西**：
  - 你点名的 `user_memories` 三个节点（development_spec / experience_lessons / task_summary）在本机找不到——搜了仓库、`~/.workbuddy/`（含 `workbuddy.db`、`memory/`）和 `%APPDATA%` / `%LOCALAPPDATA%` 下的 WorkBuddy 目录。它们可能只存在于 WorkBuddy 的会话上下文或云端。本方案用的是上面列出的落盘记忆；若那三个节点有与本方案冲突的结论，Phase 0 对一遍。
  - 你点名的 `data/operators_verified.json` 本机不存在（`data/` 整体 gitignore）。已跟踪的替代是 `docs/reference/operators_catalog.json`（103 个算子，平台 9 类；DEC-77 已把守卫改读它）与 `config.OP_FAMILIES`（13 族）。
- **口径提醒**：本地 `alphas.status` 只有 10 行 ACTIVE，而 `submission_ledger` 记 83 颗 ACTIVE，本地状态没同步；塔与 ACTIVE 统计一律以平台 `get_pyramid_alphas` 为准（已有规则），本方案不用本地 ACTIVE 数。

---

## 2. 现状诊断

### 2.1 代码里其实有三种「类别」，Pattern 不是平台类别

| 概念 | 落点 | 用在哪 | 现状 |
|---|---|---|---|
| **平台类别（塔）** | `datasets.category`、`config.PLATFORM_CATEGORIES`、`_common.infer_data_category` | 点塔、S0 的 `category_weights`、`s0-select` 剔已亮塔 | 17 类；DB 另有 `socialmedia`（23 集）/ `broker`（1 集）未登记；182 / 1,904 集类别为空；大小写混用（`MODEL` / `model`）；52 个数据集名在不同区类别不一致 |
| **机制类别（信号含义）** | GEM `CATEGORY_PRIMITIVES`、`tools/economic_mechanism_kb.py` | S2 概念原语、S4 改进方向 | 直接借平台类别；但 `other`（314 集）与 `model`（489 集）内部异质：`other466` 是财务比率（平台记 FUNDAMENTAL）、`other532` 是 Barra 残差、`behavioral_signals` 平台记 MODEL |
| **算子家族** | `config.OP_FAMILIES`、`operators_catalog.json` | 表达式词汇、闸、等价替换 | **不是信号类别**。区域差异体现在效应量（`quantile`、market 轴「禁外推」）和可用性（JPN 不支持 industry / sector 分组，`platform_constraints.json` 已登记） |

**你列的 9 类与平台类别的对应**：MODEL→model；PV→pv（并 imbalance）；Analyst→analyst；Fundamental→fundamental；News-Sentiment→news + sentiment + socialmedia；Insider→insiders；ShortInterest→shortinterest；Risk→risk；**Pattern 不是平台类别**（KOR 的 `pattern_scores` / `continuation_score` 平台记 PV，`chart_cnn_alpha` 两个区记成两个类别），所以它是 pv / model 下的族标签。另外你的清单漏了 **other**——它是证据最多的类别之一（GLB×other 回测 440 条、RA 全过 79 条，是能归类的格子里最高的）。

### 2.2 九步里「按区域 / 类别做不同决策」的隐性分支

| 步 | 隐性分支 | 落点 | 维度 | 问题 |
|---|---|---|---|---|
| 1 S-PRE | `entry_verdict` 三态 | profile → `region_rotation.py` / `region_status.py`（正则读取） | 区域 | 正常 |
| 1 | 开波三闸：signal_floor（IND / MEA 1.2、USA 0.9、余 0.5）、stop_rules、backlog | `_lib/region_gates.py`；`build_wave.py:523–544` | 区域 | 正常；2026-10-12 转 enforce |
| 2 S0 | 硬地板 + 分位带 + crowd / backfill / probe-exception 带 | `score_datasets.py` ← `thresholds.dataset_health`（每区约 40 键） | 区域 | 两套模板谱系并存：A 谱系 8 区（ASI / CHN / EUR / GBR / GLB / HKG / MEA / USA，源自早期 KOR 模板逐区复制）与 B 谱系 5 区（AMR / DEU / IND / JPN / KOR，分层模板），键集与取值口径不同 |
| 2 | **`category_weights`（0.9 / 1.0 / 1.15）** | `score_datasets.py:250`；`--calibrate` 自动回写（:1156） | **区域 × 类别** | 全库唯一已经机器化的交叉项，只作用于 S0 排序 |
| 2 | 剔已点亮塔（自然季度） | `campaign_intel s0-select`；`build_wave.py:561` | 区域 × 平台类别 × 季度 | 正常 |
| 3 S1 | TRI 闸 `s1_triage_<region>` | ledger | 区域 × 数据集 | 正常 |
| 4 S2 | 类别概念原语 / 类别禁止项 | GEM `economic_priors.py:15 / :108` → `pipeline_prompts.py:74 / :358` | 类别（写死在代码） | 无证据链；「禁加权混合」只写在 pv / fundamental 两类，news / analyst / model 没有 |
| 4 | 机制库 + `region_adaptation`（USA / IND / KOR / EUR 的覆盖阈值） | `tools/economic_mechanism_kb.py` → `skeletons.py:759` | 类别 × 区域（写死） | 区域阈值无实证，且与 `thresholds.dataset_health` 重复 |
| 4 | 类别提示词库 + A/B | `prompt_kb.py`（工作区新增、未提交）；DB `prompt_templates` 0 行 | 类别 | 空壳 |
| 4 | 区域先验 | `assemble_priors.py:51 / :97` ← DB `region_kb` + profile `## priors` 段 + registry | 区域 | registry 63% 未绑定数据集，下钻不到类别 |
| 4 | `pipeline_mode` 的类别分支 | `nodes/gem.py:119` | 类别 | 无效分支（两支都返回 phased） |
| 4 | 族 cap、新族探针限 1 条 | `build_wave.py:937–961` | 族 | 正常 |
| 5 | 闸 2b 区域非法分组字段（JPN） | `gate.py:449–458` ← `platform_constraints.json` | 区域 | **正确范式**：数据驱动、代码无区域字面量 |
| 5 | 闸 7 longCount | `gate.py:953 / :1332` 恒 WARN | — | KOR / DEU / AMR / JPN 要求的 FAIL 只写在 profile 和无人读取的 `*_specific_adjustments`（toolkit SKILL.md:172 自己承认） |
| 6 S3 | 仿真设置 | `settings.json`（toolkit 铁律：region 只从它派生） | 区域 | 同一事实 7 处来源（§2.3） |
| 6 | 设置先验自动改写 decay / 中性化 | `pipeline.py:1402` → `_lib/region_kb.py:165 / :204` | 区域（全区汇总） | 不分类别 / 族：全区汇总的过闸率被类别构成混淆，可能把快信号推到慢族的 decay |
| 7 S4 | review / near 阈值 | `review_wave.py:267 / :276` | 区域 | `turnover_max` 0.3 vs 0.7、`two_year_sharpe_min` 1.6 vs 1.0 跟着模板谱系走，不是实证 |
| 7 | `rn_sharpe_min`（EUR / GLB = 1.0） | `review_wave.py:95–107` | 区域 | 正常 |
| 7 | Mode B 主闸四层覆盖 | `mode_b_config.load_mode_b_config` | 区域 | 7 个区生效值低于 1.25 / 0.8；自适应学习无下限（§2.3） |
| 7 | 结构重建按区推荐 country 中性化 | `structural_variants.py:398`（EUR / DEU / GBR 字面量） | 区域（写死） | 无证据登记 |
| 7 | Mode B 的 B3「提想法级改进」 | `wq-brain-alpha-optimization-v1` | — | 不接收区域 / 类别输入；区域 × 类别配方只在 profile 正文和记忆里，流程不读 |
| 8 S5 | `submit_verdict` | 平台 checks 自带 limit | 平台 | 正确，不需要我方分支 |
| 8 | IND「IS / 2Y 并列汇报」 | IND profile `gate_overrides` | 区域 | 文档级 |
| 9 S6 | registry 回写 | `wqb.registry_contract` | 区域（dataset 可选） | 不绑定 → 类别级证据无法积累 |
| 9 | profile 漂移钩子 | `wqb.profile_drift` | 区域 | 只到区域 |
| — | 新建战役目录的缺省中性化 | `nodes/campaign.py:1316` 字面量表 | 区域（写死） | 与 settings.json 不一致（GLB / HKG / MEA） |
| — | 无战役目录时的缺省 universe | `tools/campaign_intel.py:94` 字面量表 | 区域（写死） | TWN 写 TOP500，`config.REGIONS` 缺省 TOP1000 |

代码外的区域字面量分支共 6 处：上表的 `campaign.py:1316`、`campaign_intel.py:94`、`structural_variants.py:398`、`economic_mechanism_kb.py` 的 `region_adaptation`，以及 `tools/fetch_dataset_assets.py:37`（区域 → universe 缺省）、`tools/dynamic_recipe_weighter.py:137`（零引用）。`brain_api_models.py:56` 的「USA SUPER 必须带 prod 条件」是平台规则，保留为白名单。**toolkit 脚本本身目前没有区域字面量分支**，这个性质值得用测试钉住。

### 2.3 区域注入机制的四个漏点

1. **同一事实多源。** 中性化有 7 处来源：settings.json、profile `static`、`config._NEUTRALIZATION_BEST`（零调用方，只剩一条钉值测试）、`config.REGIONS` 档位顺序（KOR 首位 SECTOR）、DB `regions` 表、`nodes/campaign.py` 兜底表、运行时 `region_kb` 设置先验。13 个区里 7 个区答案矛盾（附录 B）。universe 同样：EUR settings 是 TOPCS1600、profile 与 config 缺省是 TOP2500；GLB 是 TOPDIV3000 对 TOP3000；DB `regions.universe_legal` 已陈旧（ASI 列着 TOP2000 / TOP1000，config 注明平台只给 MINVOL1M / MINVOL10M / TOP500；EUR 还列着已下线的 ILLIQUID_MINVOL1M），而 matrix 的配置包读的正是这张表。
2. **配置键没人读。** 按字面量扫描，各区 thresholds.json 有 6–25% 的键在代码里找不到读取方（分层模板 5 区最高，22–25%）：`*_specific_adjustments` 整块、13 个区都有的 `hard_gates.*`、`quick_scan.red_sh_abs_min`、EUR / GBR / GLB 的 `diversity.{entropy_min, similarity_max, …}`、`concentrated_weight_max`、`sub_universe_sharpe_min`、`field_count_strategy_ref`。DEU 的 thresholds 里还挂着 `kor_specific_adjustments`（复制来源的痕迹）。扫描是粗口径，Phase 0 的工具会逐键确认。
3. **以为生效、其实没执行的覆盖。** KOR「闸 7 longCount < 80 → FAIL、CW > 0.5 → FAIL」写在 profile 与 `kor_specific_adjustments`，代码恒 WARN。IND 10-03 的穷尽结论写进了 `tracking/IND/reference/region_kb.json`（`dead_end_rules` / `prod_saturation_risk` / `settings_sensitivity`），但没有任何代码读这个文件——assemble-priors 读的是 DB 里的 `IND/region_kb`，那里没有这三个键。
4. **纪律被放宽。** 用真实加载函数只读算出的 Mode B 主闸生效值：

   | 区 | 生效 S / F | 来源 |
   |---|---|---|
   | ASI、CHN、GBR、HKG、MEA | 1.20 / 0.80 | thresholds 覆盖 |
   | GLB、USA | 1.00 / 0.60 | thresholds 覆盖 |
   | EUR | 1.15 / 0.68 | **区域 ledger（自适应学习器写入：`learned_from: 5`，`learned_at` 2026-09-11；学习器没有下限）** |
   | AMR、DEU、JPN、KOR、TWN | 1.25 / 0.80 | 全局或等值覆盖 |
   | IND | 1.50 / 1.00 | thresholds 覆盖（更严） |

### 2.4 证据密度

- 14 区 × 17 类 = 238 个可能格子；有任何回测或 registry 证据的 124 个；回测 ≥ 200 条的 11 个。
- 过建档线（≥ 1 条绑定胜绩或 ≥ 3 条绑定判死）的 22 个：活跃区 12 个（DEU×other、GBR×{model, fundamental, pv}、GLB×news、KOR×{fundamental, analyst, news, other, risk, pv}、USA×option），probe-only 区 10 个（ASI×pv、EUR×{model, other, pv, fundamental, news, analyst, institutions}、IND×pv、CHN×未知）。**有绑定胜绩的只有 KOR×fundamental（5 条）与 IND×pv（1 条）。**
- registry 的胜绩与判死共 613 条，**389 条（63%）没有绑定到本区可识别的数据集**（没有 `payload.dataset`，或该数据集不在本区 `datasets` 表），因而无法归到任何类别。
- 结论：格子主要装的是「别做什么」（S2 排除），「什么奏效」（S4 配方）的证据极少。这决定了格子应该是数据，而不是 skill。

### 2.5 30% 判据实测

**口径**：分子 = 区域 profile 里归属该步的段落字数（下界只算标题写明「步 N 注入」的段；上界再把「现状 / 约束 / 避坑」这类混合段和自动生成的 `## priors` 数据整段算进去；证据附录不算）；分母 = SKILL.md「### 步 N」段 + 该步 reference 文档。字数去空白。

| 区域 | 步 3 S1 | 步 4 S2 | 步 7 S4 | 步 8 S5 | 步 2 S0（参考） |
|---|---|---|---|---|---|
| IND | 0% | 1–23% | 3–23% | **18%** | 0–24% |
| KOR | 1% | 0–**28%** | 0–18% | 0% | 5–**32%** |
| JPN | 0% | 1–25% | 0–19% | 0% | 2–**31%** |
| EUR | 0% | 2–21% | 0–9% | 0% | 0–14% |
| DEU | 1% | 0–16% | 2–8% | 0% | 6–22% |
| GBR | 0% | 1–12% | 0–1% | 0% | 3–4% |
| MEA | 0% | 0–11% | 0–6% | 0% | 0–9% |
| AMR | 2% | 2–10% | 1–6% | 0% | 0–8% |
| GLB / USA / ASI / HKG / CHN / TWN | 0% | ≤ 8% | ≤ 4% | 0% | ≤ 4% |

- 步 8 的分母只有 SKILL 段（提交链细则在 `worldquant-submit-alpha`），所以 IND 的 18% 被放大了；内容只是「IS 与 2Y 并列汇报」。
- 宽口径下过线的只有 S0（KOR 32%、JPN 31%），而 S0 正是你要复用的通用步；那些差异是阈值与白名单规则，属于数据。
- **类别侧**：新闻 / 情绪 skill 6,159 字，对 S1 + S2 正文 17,348 字约 35%——已拆；饱和集的假设优先 skill 6,284 字——已拆。GEM 里写死的类别字典 4,311 字在代码里。其余类别在步骤文档中的篇幅都 ≤ 2%。
- **一个补充判据**：已经成功拆出的两个 skill，差别都在**控制流**（5 家族 × 6 桶的配对流程；假设目录 + 去门控消融），不只是篇幅大。数值不同改配置就够了，只有流程不同才值得多一个 skill。

### 2.6 需求里四个例子的核对

| 需求里写的 | 实际证据 | 应归的层 |
|---|---|---|
| IND 的 robust 墙 | 平台对 IND 额外要求 robust universe Sharpe ≥ 1.0（IND profile 引 India Alphas 文档）；破解配方来自 analyst_consensus：pretax 口径 + 市值十分位 `group_rank`（zq8wZgQO） | 区域层（平台硬事实）+ IND×analyst 格子（配方） |
| MEA 的 earnings3 纯事件计时腿 | MEA 记的是 `MEA-EARNINGS3-CALENDAR-DEAD`（判死）；「只能作条件腿」出自 `IND-EARNINGS3-TIMING-DEAD` | 两区同向 → **earnings 类别卡**（跨区复现，可以升类别级）；MEA 已 frozen |
| EUR 的禁 PV × MODEL 组腿 | EUR 的历史胜绩机制恰恰是「慢 MODEL 残差 × 快 PV」；禁的是 0.40 / 0.60 加权写法（全局禁混信号），机制本身可以条件 / 分组 / 残差入场。EUR 最新有效杠杆是嵌套 `vector_neut` 残差化（JjQmx9nm，prod 0.6695）与 `hump` 档位；**换分母在 EUR 是毒药** | 全局锁（禁加权）+ EUR×fundamental / EUR×model 格子 |
| KOR 的 behavioral_signals 突破配方 | `behavioral_signals` 是 **IND** 的（平台类别 MODEL）：streak / recency 秩化形是 IND 唯一过 IS 闸的族。KOR 的突破是 `other466` 财务比率族（平台类别 FUNDAMENTAL）：`signed_power → quantile` 等价替换 + 外层轴 sector → market | IND×model 格子；KOR×fundamental 格子 |

这四条也说明：**同一类别在不同区的结论会相反**（KOR 的真变量是分母，EUR 换分母即死），所以 S4 配方的天然粒度是格子，不是区域，也不是类别。

---

## 3. 设计原则

1. **参数是数据，流程才是 skill。** 拆 skill 的前提是控制流不同；数值不同只改配置。
2. **证据作用域 = 规则作用域。** 一条规则只能写到它证据覆盖的那一层：
   - 格子 → 类别：≥ 2 个区同向复现（例：earnings3 只能作计时 / 条件腿，IND + MEA）；
   - 格子 → 区域：同区 ≥ 2 个类别复现；
   - 跨区结论相反（KOR 分母 vs EUR 分母）：两条都钉在各自格子，禁止上升。
   这是记忆里「语法级效应必须本区实测，禁外推」的机器化。KOR profile 已经在手工这样做（第 7 条「输入频率」注明只有 shortinterest38 一个族的证据）。
3. **单一解析器，来源可追溯。** 每个生效值带 provenance：来自哪一层、哪条证据、是否被锁定表钳过。
4. **稀疏。** 格子按证据建，不按矩阵建。
5. **锁定表。** 有一组纪律任何层都不能覆盖；数值类只许收紧（§4.1）。
6. **塔用平台类别，机制用机制类别。** 点塔、剔已亮塔永远按平台类别；机制类别不同不会让已亮塔的数据集回到主数据集（用户 2026-09-19 定案）。
7. **学到的 ≠ 写下的。** 学习层（`region_kb` 设置先验、Mode B 自适应、规则自学习）只能在所属层的边界内调整，不能放宽纪律；学习结果升格为画像要人工复核（沿用 `profile_drift` 钩子）。

**冲突裁决（新）**：用户显式指令（waiver，红线除外）> **锁定表** > 代码 fail-closed 闸 > **格子** > 区域画像 > **类别卡** > 决策表 / 全局缺省 > SKILL 正文。原来的「D0-P 不接受区域改写」并入锁定表。区域排在类别前面，是因为类别卡只收 ≥ 2 区复现的结论，而区域层的结论带着本区 prod book 与平台规则的本地证据。

---

## 4. 目标架构

### 4.1 四层知识与锁定表

| 层 | 存放（机读 / 人读） | 写什么 | 不写什么 | 写入方 | 读取方 |
|---|---|---|---|---|---|
| **L0 全局** | `src/wqb/config.py`、toolkit `config/*.json` / SKILL.md、`references/step*.md`、`decision-table.md` | 九步流程、全局阈值、全局规则 | 区域 / 类别数字 | 人 | 全部 |
| **L1 类别卡** | `src/wqb/profiles/category_cards.json` / `references/categories/<cat>.md`（摘要块由生成器写） | 概念原语、类别特有禁止项、字段性质提示（更新频率 / 类型 → 窗口与 decay）、≥ 2 区复现的死族与杠杆 | 单区结论、区域数字 | 人（迁自 GEM 字典与机制库） | 解析器 → assemble-priors → GEM；optimization-v1 |
| **L2 区域画像** | `tracking/<R>/config/settings.json`（设置唯一权威）、`thresholds.json`（区域阈值）、DB `region_kb`（学习层）/ `references/regions/<R>.md`（现有） | `entry_verdict`、平台硬事实、开波闸、loop_policy、区域级杠杆、带作用域标注的单族规则（`scoped_rules`） | 设置数值副本（删 profile 的 `static` 段） | 人 + S6 | 解析器、toolkit |
| **L3 格子** | `tracking/<R>/config/cells.json`（稀疏；只有过线格子）/ 区域 profile 里生成的「格子索引」块 | 该组合的胜绩配方、判死清单、settings 差量（以 win 设置形式）、Mode A 空间收窄、阈值收紧 | 无证据条目 | S6 后人工合成，引用 registry id | 解析器 |
| **L4 数据集 / 族** | `registry_empirical`（绑定 dataset）、`reports/dataset_experience/*`、`tracking/<R>/reference/*_ideas.md`（现有） | 原子证据 | — | S6 | 格子引用 |

**锁定表**（`src/wqb/profiles/locked.py`，与 `wqb.waiver.RED_LINES` 并列）：

| 项 | 规则 | 出处 |
|---|---|---|
| 禁混信号 | 任何层不得放行两条独立腿相加（加权、等权、`add`、中缀 `+`）；卡片 / 格子文本出现权重配比即测试红 | CLAUDE.md、`mixed_signal_leg_ban_v1`、闸 5 |
| Mode B 主闸 | sharpe ≥ 1.25 且 fitness ≥ 0.8 为下限，只许收紧；自适应学习器同样钳制 | 本需求；GLOBAL `mode_b_qualification` |
| D0-P | prod 墙处置阈值不接受区域 / 类别 / 格子改写 | SKILL.md 冲突裁决 |
| 提交前用户确认 | 解析器不产生任何提交动作 | `waiver.RED_LINES` |
| 平台线 | 任何阈值覆盖不得低于 `PLATFORM_CHECK_LINES` | config.py |
| 窗口白名单 | 卡 / 格子里的窗口 ⊆ `STANDARD_WINDOWS`，否则必须带解释与实测证据 | CLAUDE.md |
| 已点亮塔不作主数据集 | S0 按平台类别剔除 | 用户 2026-09-19 |
| truncation 不作扫描维度 | 任何层不得把 truncation 放进 Mode A 空间 | D5（IND、GLB 实测零杠杆） |

### 4.2 目录结构

```
Claude/skills/wq-brain-ra-pipeline/
├── SKILL.md                          # 九步骨架不变；步 3/4/7/8 各加一行「先读生效画像」；冲突裁决改为 §3 新链
└── references/
    ├── region-profile-contract.md    # 扩写为三层契约（profile / 类别卡 / 格子的 schema、建档线、升级规则）
    ├── category-taxonomy.md          # 平台类别 ↔ 你的 9 组 ↔ 机制类别；Pattern、other 的处理
    ├── regions/<R>.md                # L2（现有 14 份）：加 schema_version: 2、scoped_rules、生成的「格子索引」块；删 static 段
    └── categories/<cat>.md           # L1 人读页（首批 10 张；摘要块由生成器写，正文手写）
                                      # 注意：regions/ 下每个 .md 都被测试当作区域 profile，类别页不能放进 regions/

src/wqb/
├── config.py                         # PLATFORM_CATEGORIES 补 socialmedia / broker；新增 CATEGORY_GROUPS；
│                                     # REGIONS[R] 加 default_neutralization（只用于新建战役目录兜底）；删 _NEUTRALIZATION_BEST
└── profiles/                         # 新子包
    ├── resolver.py                   # resolve(region, category=None, dataset=None, step=None) → 生效值 + provenance
    ├── locked.py                     # 锁定表（方向：immutable / min_only）
    ├── schema.py                     # 类别卡、cells.json、thresholds 覆盖的校验
    └── category_cards.json           # L1 机读数据

tracking/<R>/config/
├── settings.json                     # 设置唯一权威（不变）
├── thresholds.json                   # 保持现格式；加 _evidence 映射；清掉死键；*_specific_adjustments 拆成真键
└── cells.json                        # 新，稀疏：{ "<category>": { levers, exclusions, settings_delta, mode_a_space, thresholds, evidence } }

docs/threshold_keys.json              # 新：thresholds 键目录（照 docs/ledger_keys.json 的模式）

tools/                                # 顶层冻结（S11），新工具进 THEMES.json 的主题目录，并在 tools/README.md 登记
├── code-audit/profile_audit.py       # sources / dead-keys / modeb / split-ratio 四个只读子命令
├── code-audit/threshold_keys.py      # thresholds 键目录对账
├── code-audit/profile_split_check.py # Phase 4 拆分机检
├── rotation/cell_evidence.py         # 区域 × 类别证据矩阵（只读，可写 ledger）
└── research/profile_resolve.py       # 生效画像 CLI（--explain 列出每个值的来源）
```

命名：目录小写 kebab-case；区域代码作为平台数据标识保持大写（同 `tracking/<REGION>`）；类别页文件名 = 平台类别 id。若 Phase 4 判定需要拆 skill，命名为 `brain-playbook-<region>-<category>`（`brain-*` = 知识技能），`layer` 按主承接步取 L2 或 L4。

### 4.3 每个组合的四件东西从哪来

| 你要求的项 | 区域层 | 类别层 | 格子层 | 锁定 / 不进层 | 消费方 |
|---|---|---|---|---|---|
| S2 候选生成策略（GEM 模板 / 骨架） | 区域死族、拥挤族、区域胜绩、语法模式（如 IND `scale(-rank(x))`） | 概念原语、类别禁止项、字段性质提示 | 该组合的胜绩机制与判死族 | 禁混信号（全局）；窗口白名单 | assemble-priors 快照 → GEM |
| 回测参数 | universe / delay（平台硬事实）、区域缺省中性化 / decay | decay 按信号速度的提示（只建议） | 中性化 / decay / nanHandling / maxTrade 的 win 设置差量（带证据） | truncation 不进任何层 | 步 6 以 `--set` 显式钉住（pipeline 已支持，设置先验不改钉住维度） |
| S4 诊断改进配方 | 区域级杠杆（≥ 2 类别复现）、区域禁用杠杆 | ≥ 2 区复现的杠杆 | Mode B 改进方向（levers，按证据强度排序）、Mode A 空间收窄 | D0-P；等价算子扫描前置（D15） | optimization-v1 的 B3 与 Mode A |
| 判死与资格线阈值 | thresholds.json（只收紧，带证据）、loop_policy | 类别特有的判死提示 | thresholds 收紧（如小宇宙 CW 判死） | Mode B 下限；平台线 | review_wave、mode_b_config、gate 闸 7 / CW |

没有格子的组合，生效画像 = 区域 ⊕ 类别 ⊕ 全局，`--explain` 会写明「本组合无专属证据」。

### 4.4 各步结论

| 步 | 结论 | 理由 |
|---|---|---|
| S-PRE / S0 / S3 / S6 | 复用主骨架（同意你的判断） | 差异全是阈值、白名单与设置数值；S0 的 `category_weights` 已是区域 × 类别数据；S6 只多一个职责：回写时绑定数据集 / 作用域 |
| S1 | 不拆；类别卡给提示 | 差异来自字段性质（VECTOR、更新频率、已实现 vs 预测），跨区通用；区域差异很小（KOR / DEU 的 longCount 双查） |
| S2 | 不拆；类别卡 + 格子进 priors 快照 | 类别主导（概念原语）+ 区域（死族、拥挤）+ 格子（胜绩机制）；新闻 / 情绪的深挖继续走已有 skill |
| S4 | 不拆；格子是主承载层 | 结论跨区相反，天然粒度是格子；但只有 2 个格子有绑定胜绩，撑不起 skill |
| S5 | 永不分支 | 平台 checks 已经区域化；区域差异只在汇报维度（IND 2Y 列）与配额 |

### 4.5 与 toolkit / matrix 的接口

| 组件 | 角色（不变） | 新增读取 | 新增写入 / 契约 | 不许做 |
|---|---|---|---|---|
| `wq-brain-ra-pipeline`（L-RA） | when / what | 步 3 / 4 / 7 / 8 读 `profile_resolve --region $REGION --category $CAT --step Sx` | 冲突裁决链换成 §3 | 复写数字 |
| `wq-brain-campaign-matrix`（L-PRE） | where | 配置包加类别维：候选数据集的 tower_category / mechanism_category、所在格子与证据数（来自 `cell_evidence`）、生效画像引用；`get_region_config` 的陈旧档位改由 config + settings 校正 | 拥有 registry schema：win / dead_end 必带 `dataset` 或显式 `scope` | 选区；替代 S0 |
| `wq-brain-campaign-toolkit`（L-TOOL） | how；代码保持区域、类别无关 | 经 `wqb.profiles` 取：闸 7 / CW verdict、review 阈值、格子差量；assemble-priors 写 `category_cards` / `cells` 段；设置先验按类别分层 | `priors_snapshot_<region>` 多两个段 | 出现区域 / 类别字面量分支（守护测试拦） |
| `brain-make-some-gem`（L2） | S2 生成 | priors 快照的 `category_cards` / `cells` 段（替代内置字典） | — | 自带类别知识副本 |
| `wq-brain-alpha-optimization-v1`（L4） | S4 改进 | B3 先取 levers；Mode A 空间取解析结果；资格走钳制后的主闸 | — | 放宽主闸 |
| `worldquant-submit-alpha` / `submit_verdict`（L5） | 只否决 + 用户确认 | 不读格子 | — | 任何区域 / 类别分支 |

### 4.6 纪律怎么保

| 纪律 | 机制 | 守护 |
|---|---|---|
| 禁混信号、警惕 `add(A,B)` | 锁定表；GEM 的禁加权从 pv / fundamental 两类上收为全局；卡片 / 格子不得含权重配比 | 卡片 schema 测试（文本扫描 `0.4*`、`add(multiply(` 等）；闸 5 不变 |
| Mode B 资格线 1.25 / 0.8 | 解析时钳制；自适应写库前钳制 | `test_mode_b_floor.py`（带反向前提：旧代码对 GLB 返回 1.0 / 0.6） |
| 提交需用户确认 | 解析器无提交动作；S5 不分支 | 现有 `test_workflow_chain_irreversible_guard.py` |
| D0-P 不可改写 | 锁定表 | 解析器单测 |
| 时间窗口有意义 | 卡 / 格子窗口 ⊆ 白名单，否则必须带证据 | 卡片 / 格子 schema 测试 |
| 均匀点塔、已亮塔不开战役 | 塔永远按平台类别；格子不改变塔归属 | 解析器单测 + 现有 `s0-select` |
| 禁外推 | 证据作用域 = 规则作用域；规则自学习不得写 `region="*"` 除非 ≥ 2 区证据 | 规则 schema 校验 + 单测 |

---

## 5. 迁移路径

总前置：DEC-72 ~ DEC-78 那批改动按路径提交完成（另一个线程在等你一句话）。之后按 Phase 顺序推进，每个 Phase 都可单独回退。

### Phase 0　基线（P0；零行为变更）

- **改动**
  1. 本方案入库（本文件随 Phase 0 提交）。
  2. `tools/rotation/cell_evidence.py`（只读）：§2.4 的矩阵——回测数、严格 RA 全过数（`ra_failed_checks` 口径，见 AGENTS.md §8.7）、prod_clean / prod_blocked、绑定胜绩 / 判死、未绑定数。`--write-ledger` 写 `GLOBAL/cell_evidence_matrix`（先在 `docs/ledger_keys.json` 登记）。
  3. `tools/code-audit/profile_audit.py`（只读）：`sources`（同一参数多源对照）、`dead-keys`（thresholds 未读键）、`modeb`（各区生效主闸，直接调用 `mode_b_config`）、`split-ratio`（§2.5 口径）。
  4. 基线落盘：上述输出 + 各活跃区 `get_mining_yield(strict)` → `output_report/`。
- **验证**：本方案里的每个数字都能被这两个工具复现（对不上就先改方案）；两个工具的单测用临时 sqlite 夹具，经 `WQB_DB_PATH` 隔离，不碰生产库；`pytest tests/ -x`；`audit_structure`（S11：新脚本只进主题目录）；`tools/README.md` 登记。
- **风险**：低。回退 = 删两个工具。

### Phase 1　修漏 + 锁纪律（P0；不加新维度）

**1a　Mode B 下限锁（可在 2026-10-12 前落）**
- `mode_b_config.load_mode_b_config`：三层覆盖之后对主闸取 `max(值, 全局下限)`，返回 `_clamped_from` 留痕；`mode_b_adaptive` 写库前同样钳制。全局下限读 GLOBAL ledger 的 `main_gate`，读不到时用内置 1.25 / 0.8。
- 删掉 thresholds.json 里低于下限的 7 处覆盖（ASI / CHN / GBR / HKG / MEA / GLB / USA），回落全局；IND 的 1.5 / 1.0 保留。EUR 区域 ledger 的 1.15 / 0.68 **不动库**，读时被钳住。
- 落地前出影响面（只读）：near_pool / salvage_pool 里 S ∈ [1.0, 1.25) 或 F ∈ [0.6, 0.8) 的候选，逐条标出是否仍能经旁路 A–E 进入 Mode B。
- 验证：`test_mode_b_floor.py`；`tools/mode_b_qualify.py` 显示钳制来源。MCP 进程里的 judge 节点 import `mode_b_config`，campaign 节点在回写后调用 `mode_b_adaptive.update_mode_b_qualification`（`nodes/campaign.py:760`，EUR 的 1.15 / 0.68 就是这条路径写的），**需重启 MCP** 才在 MCP 路径生效。
- 回退：去掉钳制一行。

**1b　阈值键目录 + 文档级覆盖变真（放到 2026-10-12 转 enforce 并观察一波之后）**
- `docs/threshold_keys.json` + `tools/code-audit/threshold_keys.py` + `test_threshold_key_catalog.py`：每个键必须有读取方或标 deprecated；新键先登记再写。
- `*_specific_adjustments` 拆成被读取的真键：`gates.longcount_verdict`（gate.py 闸 7 读；KOR / DEU / AMR / JPN = FAIL，即 thresholds 里现有这四个区；toolkit SKILL.md 另提到 HKG / TWN，等有证据再加）、`review.cw_verdict`（review_wave 读）；`hard_gates.*`、`quick_scan.red_sh_abs_min`、EUR / GBR / GLB 的 `diversity.*`、`concentrated_weight_max`、`sub_universe_sharpe_min`、`field_count_strategy_ref`、分层模板 5 区的 `poll.*` 逐键判：接线或删除（默认删除：几个月没有消费者，说明没有观测到需求）。
- 每个区域覆盖补 `_evidence`；无证据的回落全局；低于平台线的禁止。toolkit SKILL.md:172 那段改写。
- 验证：KOR 夹具 longCount < 80 → 闸 7 FAIL，非 KOR 仍 WARN；对 KOR、GLB 最近 3 波用新代码重跑评审（`review_wave.py` 干跑），结论差异只允许出现在闸 7 / CW 两处；全量回归。
- 风险：KOR 等区的闸 7 第一次真按 FAIL 执行（这是 profile 一直写着的本意）。回退：thresholds 改回 WARN。

**1c　区域参数单一来源（可在 2026-10-12 前落）**
- 删 `config._NEUTRALIZATION_BEST` / `neutralization_best()`（零调用方），同步删 `tests/unit/09_core/test_config.py:333` 的钉值测试。
- `config.REGIONS[R]` 加 `default_neutralization`（只用于新建战役目录兜底）；`nodes/campaign.py:1316` 与 `campaign_intel.py:94` 的字面量表改读 `config.REGIONS`。
- 区域 profile 删 `static` 段（数值只在 settings.json），`index_tables.py regions` 的生成表加 universe / 中性化 / decay 三列（来自 settings.json）。
- DB `regions` 表（`get_region_config` 读它）一次性按 `config.REGIONS` + settings.json 对齐——**写库，需要你点头**；同时加漂移测试。
- `structural_variants.py:398` 的 EUR / DEU / GBR 分支改读区域杠杆数据（找不到证据就先置空）；`economic_mechanism_kb` 的 `region_adaptation` 在 Phase 2 随迁移删除。
- 守护：`test_no_region_literal_branches.py`（AST 扫 `src/` / `tools/` / toolkit 脚本；白名单只留 `brain_api_models.py:56`）。
- 验证：`profile_audit.py sources` 归零；`index_tables --check`；全量回归。

**1d　IND 文件知识进库（需要你点头，并和 WorkBuddy 对一下）**
- 把 `tracking/IND/reference/region_kb.json` 的 `dead_end_rules` / `prod_saturation_risk` / `settings_sensitivity` 映射进 DB `IND/region_kb` 中真正被消费的键（`dead_patterns` / `notes` / `settings_proven`），merge 写入，然后重跑 assemble-priors。这个文件是 WorkBuddy 未提交的改动，先确认它之后不再往文件里写。
- 验证：`priors_snapshot_IND` 里能看到这三类内容；`step9_audit.py --region IND`。

**Phase 1 整体验证**：`pytest tests/ -x`、`sync_skills.py --check`、`skill_lint.py`、`audit_structure.py`、`index_tables.py --check`；`profile_audit.py sources|dead-keys|modeb` 三项只剩登记过的例外。

### Phase 2　类别维度成为数据（P1）

- **2a 口径**：`PLATFORM_CATEGORIES` 补 socialmedia / broker；新增 `CATEGORY_GROUPS`（你的 9 组 → 平台类别）、`normalize_category()`（小写、空 → unknown）、`mechanism_category()`（other / model / unknown 用 S1 L3.5 族推断，**只作 S2 / S4 检索提示，不影响塔**）。182 个空类别数据集用平台 `get_datasets` 回填——**写库，需要你点头**。
- **2b 类别卡（首批 10 张）**：model、pv（并 imbalance；Pattern 作族标签）、analyst、earnings、fundamental、news（并 sentiment / socialmedia；深挖仍走 `brain-alpha-research-news-sentiment`）、insiders、shortinterest、risk、other。来源：GEM `economic_priors.py` 两个字典、`tools/economic_mechanism_kb.py`（去掉无实证的区域适配）、决策表 D5 / D6 的字段性质行、≥ 2 区复现的结论。option / institutions 等到有格子或跨区规则需要时再建。
- **2c 解析器**：`src/wqb/profiles/resolver.py` + `locked.py` + `schema.py`；CLI `tools/research/profile_resolve.py --explain`。
- **2d 接 S2**：assemble-priors 快照新增 `category_cards`（只含本区白名单涉及的类别）；GEM 的 `compact_priors_text` / `concept_first_rules` 改读快照，内置字典留作过渡兜底，**提示词逐字比对通过后删除**；`skeletons.py:759` 改读卡；`prompt_kb` 冻结（不加行）。GEM 有内嵌快照，改完跑 `sync_gem_embedded_skill.py`。
- **2e 规则引擎**：`RuleStore.query` / `inject_rules` 的 trigger 支持 `category`（与 `family`）；`extract_signals` 学到的规则 `trigger.region` 一律写数据来源区，写 `"*"` 需 ≥ 2 区证据或 source=user。`rules.py` WorkBuddy 也在改，按 mtime 守护编辑、按路径提交。
- **2f S1**：`field_semantic_classify` 读类别卡的 S1 提示（只提示不拦截，同 DEC-77 ⑥）。
- **2g S3 设置先验按类别分层**：`region_kb.gate_priors` 增加按类别的 decay / 中性化过闸率；当前类别样本 n ≥ min_n 才自动改写，否则只建议不改。
- **验证**：解析器单测（层级优先、锁定项、只许收紧、无格子回落、provenance 完整）；GEM 提示词逐字比对（KOR other466、IND behavioral_signals、GLB 一个 pv 集各一份）；`workflow_gem` 干跑；设置先验分层的单测（构造一个全区汇总推荐 decay = 14、按类别分层后 pv 推荐 decay = 4 的反例）；`pytest tests/ -x`、sync、lint、audit。
- **风险**：GEM 提示词变化会改变生成；靠逐字比对把关。回退：快照缺字段时 GEM 走内置兜底（过渡期保留）。

### Phase 3　证据绑定 + 稀疏格子 + 接 S4（P1 → P2）

- **3a registry 绑定**：`wqb.registry_contract` 对 win / dead_end 要求 `payload.dataset` 或显式 `payload.scope`（region / category:<c> / family），缺则 fail-closed 报错；matrix SKILL 的 schema 表同步。存量 389 条先出推断报告（族名 / 规则文本 → 数据集 → 类别），你确认后批量回填——**写库**，留 `bound_by`。
- **3b 建格子**：按 `cell_evidence` 过线清单建 `tracking/<R>/config/cells.json`。首批只做活跃区：KOR×fundamental（唯一有绑定胜绩的活跃格子）、KOR×analyst、GBR×model 写完整格子；其余活跃过线格子（DEU×other、GBR×fundamental / pv、GLB×news、KOR×news / other / risk / pv、USA×option）只写判死清单。probe-only 区（EUR×model 62 条判死、IND×pv 等）只做知识存档，不为其新写流程；MEA（frozen）不建。
  同时做**作用域审计**：各区 profile 里由单一类别证据得出的规则，挪进对应格子或打 `scope` 标（例：KOR 第 7 条「输入频率」→ KOR×shortinterest；IND「长窗优先」→ IND×model）。
- **3c 接 S4**：optimization-v1 的 B3 先取 `profile_resolve --step S4` 的 levers（作用域窄的优先、证据强的优先），**标了「禁外推」的杠杆只在原区用**（换分母：KOR 可用、EUR 是毒药）；Mode A 空间取解析结果（不扫 truncation、decay 去重并按信号速度）；`structural_variants` 改读 levers。
- **3d 回溯验证（零配额）**：拿已知突破做事后预测——KOR other466 等价替换、EUR 嵌套残差 JjQmx9nm、IND `trade_when` 慢开关 ZYbqREW1 / levk5JYN、IND analyst_consensus robust 破墙 zq8wZgQO：解析器对该格子的首选杠杆应命中当时真正奏效的那个，且不得给 EUR×fundamental 推荐「换分母」。报告进 `output_report/`。
- **3e** matrix 配置包加类别维；`profile_drift` 扩到类别卡与格子（green_but_dead 等同样判）。
- **3f（可选）** CLI 输出稳定后，wqb-db 新增只读工具 `get_effective_profile(region, category)`，按 AGENTS.md §8.2 的注册纪律加，重启 MCP。
- **验证**：registry 契约单测（缺 dataset / scope 被拒，带反向前提）；回溯报告 4 / 4 命中；活跃区各跑满 3 波后对比 §6 指标。

### Phase 4　拆分判据机检（P2）

- `tools/code-audit/profile_split_check.py`：对每个（区域 | 类别 | 格子）× 步计算差异化占比（§2.5 口径，再扣掉已迁入配置的数值表）。四条同时满足才标 `SPLIT_ELIGIBLE`：① 占比 > 30%（你的线）；② 控制流不同（新步骤、新工具、新停止规则，而不只是数值）；③ 证据线：≥ 2 条绑定胜绩，或 ≥ 5 条绑定判死且近两个季度仍在投；④ 区域 active。挂进 `audit_structure` 作 WARN。
- 拆分模板（只在 ELIGIBLE 时）：`brain-playbook-<region>-<category>`，职责边界写明只承接该格子的 S2 / S4；ra-pipeline 路由加一行、matrix 配置包指向它、6 个安装位同步、过 CONTRACT §5 门禁。
- 按现有证据，预计没有格子会触发。

---

## 6. 指标

| 指标 | 基线（本次实测） | Phase 1 后 | Phase 3 后 |
|---|---|---|---|
| 中性化答案冲突的区域数 | 7 / 13 | 0 | 0 |
| thresholds 未读键占比 | 6–25%（粗口径） | 0（键目录守护） | 0 |
| Mode B 生效主闸低于 1.25 / 0.8 的区 | 7 | 0 | 0 |
| 白名单外的区域字面量分支 | 6 处 | 0 | 0 |
| registry 新写入未绑定率 | 63%（存量） | — | 新写入 0%；存量回填后 < 15% |
| S2 浪费：生成落在本格子已判死族的比例 | Phase 0 测 | — | 下降 |
| 活跃区 prod_clean / 100 次回测（`get_mining_yield` strict） | Phase 0 测 | — | 3 波后对比（滞后指标，不作验收门槛） |

最后一项才是目的：端到端 0.10%、相关性淘汰 68% 的瓶颈在 prod，不在 IS 和生成量（RULES §C）。这次改造的价值要看它能不能让 S0 选对格子、S2 少撞已知死路、S4 先用本格子真奏效的杠杆，而不是多了几个 skill。

---

## 7. 不做的事

- 不建 13 × 9 的矩阵式子 skill / 子流程：约一半格子零证据，复制即漂移（历史上 `validator.py` 四份各自演化、profile 两周没同步都是同一个形态）。
- 不给 S5 加区域 / 类别分支。
- 不让任何层覆盖锁定表。
- 不在 frozen 区（MEA）建格子；probe-only 区只存档。
- 不扩 `prompt_kb`（0 行），等类别卡稳定后再决定它是否作为卡片版本 A/B 的载体。
- 不在 CLI 稳定前加 MCP 工具。
- 不把 truncation 放进任何层。

---

## 8. 协调与风险

- **WorkBuddy 在同一工作树并行改** `rules.py`、`methodology_rules.json`、`gate.py`、几份 SKILL.md：Phase 1b（gate.py）和 2e（rules.py）动手前看 `git log` 与 mtime，按 mtime 守护编辑、按显式路径提交；最好请它在这两步期间别碰这两个文件。
- **TB-02（2026-10-12 区域闸转 enforce）**：1a、1c 可以在此之前落；1b 等转 enforce 后观察一波再落。
- **需要你点头的写库只有四次**：1c 的 `regions` 表对齐、1d 的 IND `region_kb` 合并、2a 的类别回填、3a 的 registry 回填。其余全是代码 / 文档 / 配置文件改动。
- **需要重启 MCP**：1a（judge 节点与 campaign 节点在 MCP 进程内调用 Mode B 加载 / 自适应回写）、3f。
- **文档守卫**：`Claude/skills/` 下的 md 会被时间炸弹测试扫描（含 `MM-DD` 短日期），类别页 / 格子索引里不要写未登记的未来日期；类别页不能放进 `regions/`。
- **同步**：改 skill 后 `tools/sync_skills.py`（6 个安装位）；改 GEM 后 `sync_gem_embedded_skill.py`。

---

## 附录 A　证据最多的格子（回测 ≥ 120 条）

「RA 全过」= sharpe ≥ 1.58、fitness ≥ 1.0 且 `ra_failed_checks` 为空（旧行该列为 NULL 时按无失败计，会略高估）。判死 / 胜绩只计绑定了数据集的条目。

| 格子 | 回测 | RA 全过 | 判死 | 胜绩 | 区域状态 |
|---|---|---|---|---|---|
| GLB × model | 857 | 1 | 0 | 0 | active |
| GLB × pv | 753 | 68 | 1 | 0 | active |
| USA × model | 557 | 1 | 2 | 0 | active |
| DEU × model | 510 | 63 | 0 | 0 | active |
| GLB × other | 440 | 79 | 1 | 0 | active |
| ASI × pv | 405 | 6 | 5 | 0 | probe-only |
| DEU × other | 374 | 21 | 3 | 0 | active |
| DEU × analyst | 284 | 0 | 0 | 0 | active |
| GBR × model | 254 | 7 | 7 | 0 | active |
| USA × other | 211 | 2 | 2 | 0 | active |
| KOR × analyst | 175 | 13 | 10 | 0 | active |
| KOR × fundamental | 171 | 20 | 6 | 5 | active |
| IND × model | 159 | 24 | 0 | 0 | probe-only |
| EUR × model | 156 | 3 | 62 | 0 | probe-only |
| USA × pv | 154 | 1 | 0 | 0 | active |
| ASI × other | 153 | 4 | 2 | 0 | probe-only |
| IND × pv | 143 | 47 | 3 | 1 | probe-only |
| HKG × analyst | 122 | 18 | 0 | 0 | probe-only |

另有 MEA 379 条回测的数据集不在 `datasets` 表里（无法归类），JPN 162 条、AMR 120 条落在类别为空的数据集上。

## 附录 B　中性化的来源对照

| 区 | settings.json（权威） | profile `static` | `_NEUTRALIZATION_BEST` | DB `regions` 表 | `campaign.py` 兜底 | 矛盾 |
|---|---|---|---|---|---|---|
| EUR | SUBINDUSTRY | SUBINDUSTRY | REVERSION_AND_MOMENTUM | STATISTICAL | SUBINDUSTRY | 是（3 种） |
| HKG | SECTOR | STATISTICAL | — | SUBINDUSTRY | SUBINDUSTRY | 是（3 种） |
| MEA | SECTOR | STATISTICAL | — | SECTOR | SUBINDUSTRY | 是（3 种） |
| GLB | STATISTICAL | SUBINDUSTRY | — | SUBINDUSTRY | SUBINDUSTRY | 是 |
| GBR | SUBINDUSTRY | SUBINDUSTRY | INDUSTRY | SUBINDUSTRY | SUBINDUSTRY | 是 |
| JPN | MARKET | MARKET | — | 空 | 缺省 SUBINDUSTRY | 是（兜底） |
| KOR | STATISTICAL | STATISTICAL | — | STATISTICAL | STATISTICAL | 是（`config.REGIONS` 档位首位 SECTOR） |
| AMR / ASI / CHN / DEU / IND / USA | — | — | — | — | — | 一致 |

运行时还有第 7 处：`region_kb` 设置先验会按全区过闸率改写 decay / 中性化（未被 `--set` 钉住时）。

## 附录 C　复现方法

本轮所有统计都是只读脚本（sqlite `mode=ro` + 文件读取），Phase 0 会把它们收进 `tools/rotation/cell_evidence.py` 与 `tools/code-audit/profile_audit.py`：

- **证据矩阵**：`backtest_results(region, dataset)` 经 `datasets(name, region_id)` 映射到类别（小写归一）；`registry_empirical` 的 win / dead_end 按 `payload.dataset` 映射，无 dataset 记为未绑定。
- **Mode B 生效值**：直接调用 `wqb.workflow.mode_b_config.load_mode_b_config(store, region)`，store 用只读连接读 `ledger_kv`。
- **未读键**：thresholds.json 的叶子键（去掉 `_` 开头的说明键）在 `src/` / `tools/` / `Claude/skills/` / `world-quant-brain-mcp/` / `wqb_db_mcp.py` 的非测试 `.py` 里找不到字面量即记为未读（粗口径，会漏掉动态拼接的键，Phase 0 逐键确认）。
- **30% 占比**：§2.5 口径；profile 段落按标题归步（「步 N」显式归属；「配方 / 组腿」归步 7；`priors` 归步 4；「硬规则 / 选集 / 升档」归步 1–2；「证据附录 / 实证 / 历史画像」排除）。

---

## 9. 落地记录（2026-10-04）

### 9.1 已落地

| 项 | 落点 | 验证 |
|---|---|---|
| Mode B 下限锁：主闸只许收紧；加载时钳制、自适应写库前钳制、分布模式 p75 线不低于主闸 | `src/wqb/workflow/mode_b_config.py`（`_floor` / `_clamped_from`，新增 `category` 参数读组合覆盖）、`mode_b_adaptive.py`、`tools/probe_batch_mode.py`；ASI / CHN / GBR / HKG / MEA / GLB / USA 的 thresholds.json 改为 `$ref` 全局（原值留在 `_doc`）；`mode-b-qualification.md` §3 | `test_mode_b_qualification_doc.py`（含下限钳制与「仓库里没有区域文件写低于下限」）、`test_workflow_nodes.py`（judge 路由、p75 钳制带反向前提）；实测 EUR 1.15 / 0.68 → 1.25 / 0.80 |
| 区域 × 类别控制层 | `src/wqb/profiles/`：`taxonomy`（平台类别 ↔ 类别卡 ↔ 分组，Pattern 作族标签）、`locked`（锁定表）、`cards` + `category_cards.json`（13 张卡）、`cells`（组合文件契约）、`resolver`（生效画像 + 来源）、`evidence`（只读汇总 + 推断归属）、`render`（区域 skill / 组合分支文件）、`audit`、`__main__`（`$WQ_PY -m wqb.profiles explain / check / sync-cells / render / audit`） | `tests/unit/09_core/test_profiles_layer.py`（19 条） |
| 组合控制文件 | `tracking/<R>/config/cells.json` × 13 区，共 103 个组合（本区该类别回测 ≥ 20 或有判死 / 胜绩）；关键组合补了配方（KOR 基本面 / 卖空 / 分析师 / 内部人、IND 行为族 / 尾盘门控 / robust 破墙 / other532、EUR 嵌套残差、GLB 两条出货机制、GBR STATISTICAL 对照轨、DEU 形态天花板、ASI 门控、JPN 硬事实）。**没有写任何回测或阈值覆盖**——默认档位不变 | `validate_cells` 全部通过（测试守） |
| 判死 / 胜绩归属 | 按条目 id / family 推断数据集（`PV106` → pv106、`FND93` → fundamental93、多词连写）再按类别关键词；本区空类别借同名数据集在别区的类别 | 能归到组合的从约 37% 升到九成以上（KOR 95 / 95、EUR 147 / 150、IND 82 / 91）；只写文件，不回填库 |
| 回测接线 | `workflow_batch_track` 把组合的 `backtest.overrides` 以 `--set` 钉进 pipeline（设置先验不改 `--set` 维度）；toolkit `CampaignContext.bind_cell()`；`region_kb.apply_settings_prior` 不改 `cell_pinned` 维度 | `test_cell_overlay_ctx.py`（3 条，含反向前提）、`test_profiles_layer.py::test_batch_track_pins_cell_overrides_with_set` |
| 区域 skill | `Claude/skills/wq-brain-ra-<区>/SKILL.md` × 14（layer `L-RA-R`）：区域控制面板（生成）、组合索引（生成）、本区流程差异（手写初稿）；`references/<类别>.md` × 103（生成块 + 手写块）；能力基线已登记 | `check_structure`（测试守文件齐全、标记在、面板设置与 settings.json 一致、无孤儿）；技能宿主已能发现 14 个新 skill |
| 区域硬编码 | 删 `config._NEUTRALIZATION_BEST` / `neutralization_best()`；新增 `config.REGION_COUNTRY_SCOPE` / `is_multi_country()`，`structural_variants` 改读它（DEU / GBR 是单一国家，不再推荐 country 中性化）；`economic_mechanism_kb` 删无实证的 `region_adaptation` | `test_config.py`、`test_structural_reconstruct.py` |
| 两条棘轮 | 区域字面量分支 / 查表（存量 5 处，按文件名比对，挪目录不算新增）；thresholds 未读键（存量 126 个，粗口径） | `tests/unit/07_docs_skills/test_region_control_ratchets.py`；基线 `tests/fixtures/region_literal_baseline.json`、`threshold_unread_keys_baseline.json` |

skill_lint：新增违规 0。audit_structure：profiles 无 sys.path 自举（S1 绿）；剩下的 S11 是别的会话新放的 tools/ 顶层脚本。

### 9.2 复盘提交（e4b4c76）落地后的接线（2026-10-05 完成）

1. ✓ `wq-brain-ra-pipeline/SKILL.md`：步 1 路由到区域 skill；冲突裁决链换成 §3 新链（决策表页头同步）；「区域 Profile」节加组合覆盖注入行与区域 skill 说明（步 3 / 4 / 7 / 8 先读组合文件或 `explain`）；步 7 / 8 各加一句。
2. ✓ `INDEX.md` 路由行 + 区域 skill 说明 + 开新区第 6 步 + 分层图 `L-RA-R`；`AGENTS.md` layer 表与 §8.14；`CONTRACT.md` layer 枚举；`CHANGELOG.md`；DEC-79 ~ 84。
3. ✓ toolkit `pipeline.py` 在 `--set` 之后调 `ctx.bind_cell(dataset, pinned=--set / --neutralization 维度)`，设置先验沿用同一钉住集合（`test_cell_overlay_ctx.py` 两条，去掉接线即红）。
4. ✓ `nodes/campaign.py` 中性化兜底表 → `config.REGIONS[R].default_neutralization`；`campaign_intel.py` 宇宙兜底表 → `config.default_universe`；棘轮基线 5 → 3；新增测试守 config 兜底与现有 settings.json 一致。
5. 一半：optimization-v1 的 B3 已改为先取组合杠杆；**GEM 改读类别卡未做**——要动 `economic_priors.py` / `pipeline_prompts.py`，两文件正有并行会话的未提交改动，等它们提交后再接。
6. ✓ JPN profile 步 4「主辅权重显式分配」改为禁令 + 三式入场，JPN 区域 skill 的提示同步。

### 9.3 仍按计划延后

- 闸 7 longCount / CW 的 FAIL 真执行：等 2026-10-12 区域闸转 enforce 并观察一波之后。
- 需要用户点头的写库：`regions` 表档位对齐、IND `region_kb` 合并、182 个空类别回填、registry 判死 / 胜绩回填 `payload.dataset`。
- MCP 需要重启，Mode B 下限锁与 `batch_track` 钉设置才在 MCP 路径生效。

### 9.4 落地中新发现

- JPN profile 步 4 写着「主辅权重显式分配（默认 0.6 主 + 0.4 辅）」，与全局禁混信号冲突；2026-10-05 已更正（9.2 第 6 项）。
- IND × other 的 other532 特质收益反转（gJZwVXVm S 3.66 / F 2.83）可能满足 IND profile 的升档条件「新的信息维度」；先测 prod，再由人决定是否改 `entry_verdict`。
- dl_riskfree_returns 的平台类别是 OTHER（GLB 的出货机制 b 因此落在 GLB × other，不在 model）；KOR other466 的平台类别是 FUNDAMENTAL。
- 注册表里 MEA / IND / USA 有 4 条胜绩的骨架就是加权拼腿（`add(multiply(rank(..),0.6), ..)`、`0.8 / 0.2` 等）。原锁定表的加权检测漏掉了「权重后置」写法，已补上；生成的判死 / 胜绩行遇到这类原文会加「⚠ 加权拼腿已被闸 5 禁止，只作历史证据」前缀并标反例（`test_sf_sweeps` 守护）。这些胜绩本身仍是有效证据，复现时改成条件 / 分组 / 残差三式。
