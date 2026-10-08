# RA 九步流水线逐阶段展开 · 价值评估 · Dry-Run 演练（v3 · 2026-09-16 晚）

> 审计对象：`wq-brain-ra-pipeline` SKILL.md（2026-09-16 21:41 工作区版，last_verified 2026-09-15，含今晚未提交修改）
> 演练区域：**JPN（今日 14:19–15:42 最新激活的处女战区）** —— 比静态区更能暴露流水线首波真实行为
> 实录文件：`output_report/ra_pipeline_dryrun_transcript_jpn_20260916.txt`（纯只读）
> 前版：v2（凌晨，IND 演练）→ 本版为 **20 小时后的复审计**，核心增量：① 昨日 12 条建议的落地进度核查；② JPN 首波演练暴露的新问题；③ **22:41 第三次核验轮**：两区实录现场重跑复现 + 新增 §12（`s0_whitelist` schema 漂移全线 fail-open，建议 #14）
>
> **口径**：价值判定基于 ① 实证数字（DB 实测）② 成本收益（配额/时间/本地算力）③ 是否已自我弃用或重复。判"去除"的项均给出替代路径。

---

## 0. 一页总览（含昨日建议落地进度）

| 步 | 阶段 | 核心价值 | 判定 | 昨日建议落地情况 |
|---|---|---|---|---|
| 1 | S-PRE 查表 | 库存盘点 + 双比率 + 判死先验 | **保留深化** | ✅ 算子审计段已删（建议#5，今晚版）；✅ cross_region_lessons 移除 |
| 2 | S0 体检选集 | 三方交叉 + 座位可达性 + 停止闸 | **保留深化** | ❌ 三次 calibrate 仍为 3 次（建议#9 未落）；❌ signal_floor fail-open 未改（#10） |
| 3 | S1 字段扫描 | users 分级规避 prod_corr | **保留** | ⚠️ feature_engineering"按需"未在正文收口（#12 半落——ideas 注入规则已写，但步 3 正文仍称"字段理解用 workflow_feature_engineering"未标注禁注入） |
| 4 | S2 概念生成 | GEM 概念优先 + gate_priors 分流 | **保留深化** | ❌ 消化背压未落地（#8）——**JPN 今日实证复发**：1,640 条 gem 入库而 0 回测 |
| 5 | S2→S3 门禁 | ghost-audit + 体检硬门 + 多样性 | **保留** | ❌ 体检包未补（#3）——**JPN 白名单 12 集与现有 2 包交集为空**，硬门对现役战役 0 生效 |
| 6 | S3 七槽回测 | prod-first + settings prior + 故障协议 | **保留** | ✅ S2-COMPLIANCE 降级已写入正文（09-15 ⑥）；❌ 积压前置闸未落（#8/#10 联动） |
| 7 | S4 诊断改进 | prescreen 8× + RN_EXPOSURE + fail-fast | **保留深化** | ❌ PARTIAL 语义错位未修（#6，规则 B 仍 `all(v=="FAIL")`） |
| 8 | S4→S5 提交判定 | submit_verdict 唯一权威 + Failed-count | **保留** | ✅ judge 参考层三态条目已删（建议#5'，今晚版正文与工具映射表同步收紧为"workflow 判定（参考层）"） |
| 9 | S6 复盘回写 | region_kb 自动刷新闭环 | **保留** | ✅ 回写纪律良好结论维持（IND 98/98）；❌ step_efficiency_metrics 仍 0 行（#4） |
| 横切 | D3 决策表 | — | **待修** | ❌ 加法配比方子仍在 D3 第 47 行（#2 未落，与步 7"禁加权混合"矛盾依旧） |

**落地计分：12 条建议落地 4 条（#5 算子审计删、judge 收缩、cross_region_lessons 删、S2-COMPLIANCE 降级已在正文），未落 8 条。** 未落条目中 #3（体检包）与 #8（背压）在 JPN 今日实战中**原样复发**——这不是理论缺陷，是两个已被实证两次的活漏洞。

**全区域漏斗（2026-09-16 22:26 快照，与凌晨对比）**：

| 区 | 回测数 | 达标数 | 变化 | 备注 |
|---|---|---|---|---|
| DEU | 1,288 | 319 | 无变化 | 昨夜 W-O/N/D 系列后今日停挖 |
| EUR | 362 (+38) | 25 | +38 条回测 | 积压消化中（gated 2,229→2,235 微增） |
| **JPN** | **0** | **0** | **新区** | **今日 14:19 激活：8 catalog → 12 集白名单 → priors → 1,640 gem → wave2 门禁 FAIL** |
| 其余区 | — | — | 无变化 | — |

---

## 1–9. 九步逐阶段审计

> 各步的输入/处理/输出与子步骤级价值评估与 v2 版一致（凌晨已详列 60+ 子项，证据未变不重复），本版只列**增量发现**——今晚复核 + JPN 演练产生的新证据。完整子项表见 v2 报告（同目录凌晨版）。

### 步 1（S-PRE）增量
- **✅ 已落地**：算子审计段已从正文删除（与步 5 ghost-audit 去重，建议 #5 兑现）；`get_cross_region_lessons` 五连缩为四连（该工具查询历史显示消费率趋零，删除合理）。
- **新证据**：JPN profile 的 `entry_verdict: active` + `one_liner`（"2026-09-15 首度开挖…7 塔全 0 亮"）说明 profile 体系在新区开荒时**前置发挥了作用**——universe 实测修正（旧文档 TOP3000 等全部无效，实测仅 TOP1600/TOP1200）直接写进 profile 静态配置，避免后续波次踩非法档位（V34 教训：TOP1500 非法档曾致全批 no_pid）。profile 注入机制 ★★★ 评级维持。

### 步 2（S0）增量
- **JPN 实证**：`s0_ranking` 20KB / `s0_whitelist` 12 集（放宽档 coverage≥0.6 / alphaCount≤1500 / fieldCount≥10 + 补偿三件套）当日生成——三方交叉在新区的产出形态是"pyramid_view 战略榜重建"（7 塔 0 亮全部需要覆盖）。**放松档 + users 分级补偿**组合拳是新东西：alphaCount 50→1500 放宽 30 倍的同时用"users≥50 仅方向验证 / 0-9 优先且 ≥50% 预算"对冲拥挤风险。这是 S0 机制在处女区的正确展开。
- **❌ 未落地**：三次 `workflow_campaign(calibrate=true dry_run/实跑)` 串行调用仍在正文（建议 #9）；signal_floor fail-open 语义未改（建议 #10）——JPN thresholds.json 里 `signal_floor: {0.5, 2}` 存在但 stop_rules 为 null（回落默认 enabled=True，闸生效，此点正常）。
- **JPN 新风险（本版新发现）**：`s0_ranking` 的 universe=TOP1600，但 profile 的 `universe: [TOP1600, TOP1200]` 双档——若后续波次切 TOP1200 而 ranking/whitelist 未重建，P3 universe 一致性守卫会 WARN。属"配置存在但依赖人工复核"的已知限制，不新增建议，记入 JPN 战役注意事项。

### 步 3（S1）增量
- **JPN 实证**：8 份 typed catalog / 1.46MB 当日建成——其中 `catalog_intraday_pv_feats`（14:24）先于 wave2 门禁 24 分钟，typed catalog 前置于生成的时序在新区得到了正确执行。
- **⚠️ 半落地**：`s2_intraday_pv_feats_d1_idea` 的 `expression_list` 显示 wave1 候选是 `days_from_last_change(...)` 等**单算子裸表达式**——GEM 概念优先在这批产物中**未见机制多样性**（wave_meta_2 的 buckets：divide>atom 31 / divide>ts_mean 27 / divide>ts_delta 14——结构集中在 ratio 族，`quota_violations` 明示 ratio_pair 超配 50% > 10%）。这正是多样性闸拦下 wave2 的原因（见步 5 增量）。**概念优先的"机制"层在 JPN 首波是名义达标、实质欠 diverse**——GEM 生成侧的机制分布约束（而非仅结构分布）是下一步深化方向。

### 步 4（S2）增量
- **❌ 背压缺失复发（建议 #8，JPN 实证）**：今日单日 gem 1,640 条入库、回测 0 条。`wave_meta_2` 显示 `input: 483 → selected: 48`（diversity 抽稀 90%）——生成量是消费量的 **34 倍**。EUR 的 55 倍积压故事在新区开荒第一天就开始重演（程度较轻：处女区无历史积压，首波回测后可自然消化一部分，但 1,640 条按七槽 8 条/批的吞吐需要 ~29 个批次日）。**建议升级**：背压闸不应只在步 4 检查，GEM 生成侧应有 `--max-pending` 硬参数（超过即拒绝新 GEM 批），否则 LLM 批量生成的速度永远快于回测吞吐。
- **priors_snapshot 键名口径**：实际落库键为**小写** `priors_snapshot_jpn`（445B，今日 14:28），SKILL.md 正文模板写作 `priors_snapshot_<region>` 按大写理解会查不到——已在演练脚本修正为双查。这是文档级小口径问题，随 #12 一并修。

### 步 5（S2→S3 门禁）增量 —— **本版最重要发现**
- **❌ 体检包断层第三次复发（建议 #3）**：JPN 现有 2 个体检包（analyst14 / model25），**白名单 12 集交集为空**——wave2 的 `field_inspect` 判定 `status: unavailable, enforced: false`（gate_w2 ledger 原文：`checked_expressions: 0`）。JPN profile 自己也写明"10 集均无 WebDataScope 体检包"。**三个区域三次实证（DEU/IND → JPN），同一个洞**：开新区时体检包生成不在开荒清单里，等发现时第一波已经裸奔。
- **✅ 门禁拦截有效性再证实**：wave2 多样性闸以 `quota_violations`（ratio_pair 超配 50% > 10% 等 10 项）拦截 all_pass=0——**48/48 语法全过但多样性闸咬住了结构超配**。门禁分层（语法→结构→多样性）各自拦不同类型的坏批次，这套分层在 JPN 首波即发挥作用。门禁链 ★★★ 评级再确认。
- **wave1 的 FIELD 失败启示**（ckpt_w1 ledger）：wave1 有 `[FIELD] 未验证字段: ['analyst_quantile5_confidence_60d_pred', ...]`——跨集字段混入（price_volume_quantile5 与 analyst 系）触发字段白名单闸。48 条 probe→dropped 处置正确（未占仿真配额即拦下）。字段验证闸价值 ★★★ 维持。

### 步 6（S3）增量
- JPN 尚未进入 S3（0 回测），本步无新实证。维持 v2 结论：prod-first / settings prior / 故障协议表 ★★★；积压前置闸 ❌ 未落（与步 4 背压同根）。
- **新预警（源自演练）**：JPN 首波进入 S3 时，1,640 条 gem 池中 selected 48 条将首先回测——若首波全灭（处女区常见），`fast_kill`（profile：8 探针无 |S|≥0.5 即判死）会在第一波就触发判死回写。**届时 wave_results.verdict 必须回写**（见步 9 增量——JPN wave1 已有 closed 无 verdict 的先例），否则停止闸规则 B 在 JPN 永远无输入。

### 步 7（S4）增量
- JPN 无 S4 数据，维持 v2 结论（prescreen 8× / RN_EXPOSURE / fail-fast ★★★；PARTIAL 语义错位 ❌ 未修——源码 `all(v == "FAIL" for v in verdicts)` 原样）。
- **关联新证据**：JPN wave1 closed 但 verdict=None（见步 9）——若后续波次沿用此模式，S4 的 fail-fast 判定与 S6 verdict 之间的断层会再现 v2 修正 3 描述的口径错位问题。

### 步 8（S4→S5）增量
- **✅ 已落地**：judge 三态参考层条目已从正文删除（步 8 现在只有 Failed-count 门 + submit_verdict 两步，判定链更短更清晰）；工具映射表同步将 `workflow_judge` 标注收紧。与建议 #5'（judge 收缩）一致。
- submit_verdict 唯一权威 + 用户确认门 ★★★ 维持。

### 步 9（S6）增量
- **新发现（JPN wave1 回写缺口）**：`wave_results` 有 1 条 JPN 记录（wave_number='1'，status='closed'，02:59 创建）但 **verdict=None、full_payload 为空**。SOP 铁律"未回写视为本波未完成"——wave1 形式上 closed、实质上无复盘结论。这与 v2 修正 3（IND 98/98 良好）形成对照：**回写纪律在成熟区（IND）良好、在新区（JPN）首波即失守**。可能原因：wave1 是探针波（48 probe→dropped），执行者认为"无结果可写"——但 SOP 没有明示"探针波也要写 verdict（FAIL）"。**新增建议 #13：探针/全灭波的 verdict 回写豁免要显式禁止——upsert_wave_result(verdict=FAIL, key_findings=['48 探针全灭，字段未验证拦截']) 即可，别留空壳 closed 记录。**
- region_kb：JPN 的 `region_kb` ledger 键尚缺（步 2 演练显示 ★缺失）——正常，它由首个带回测的波次 `pipeline --review` 自动刷新（09-15 ③），JPN 还没有跑到那一步。机制本身 ★★★ 维持。

---

## 10. 建议清单 v3（昨日 12 条 + 今日新增 1 条，按优先级重排）

| # | 建议 | 状态 | 今日新证据 |
|---|---|---|---|
| 1 | **补活跃战区体检包**（JPN 白名单 12 集 + DEU 白名单） | ❌ 未落，**三连复发** | JPN wave2 `enforced: false`，白名单∩体检包=∅ |
| 2 | **D3 决策表改写**（删加法配比方子，统一结构交互口径） | ❌ 未落 | decision-table.md L47 原样 |
| 3 | **GEM 生成侧 `--max-pending` 背压硬闸**（原 #8 升级：从"步 4 前检查"升级为生成器参数） | ❌ 未落，**JPN 复发** | 单日 gem 1,640 / 回测 0，生成:消费=34:1 |
| 4 | 规则 B 增加"0 达标 PARTIAL 计入 fail-equivalent" | ❌ 未落 | 源码 `all(v=="FAIL")` 原样 |
| 5 | step_efficiency_metrics 落地或删除 | ❌ 未落 | 仍 0 行 |
| 6 | DEU 波号形态归一后重算 signal_floor | ❌ 未落 | DEU floor 仍 0.5（样本 0 波） |
| 7 | 步 2 三次 calibrate 精简为 1 次 | ❌ 未落 | 正文原样 |
| 8 | signal_floor fail-open → fail-closed | ❌ 未落 | 正文原样 |
| 9 | IND s0_ranking 补建 | ❌ 未落 | 仍缺失 |
| 10 | check_batch 双口径收敛 | ❌ 未落 | 正文双轨注原样 |
| 11 | feature_engineering"按需+禁注入"正文收口 | ⚠️ 半落 | ideas 注入规则已写（09-15 ②），步 3 正文措辞未改 |
| 12 | 文档口径微修（priors_snapshot 小写键名等） | ❌ 未落 | 演练脚本已修，SKILL.md 未改 |
| **13（新）** | **探针/全灭波 verdict 回写豁免显式禁止**（closed 无 verdict 的空壳记录） | 新增 | JPN wave1 closed + verdict=None |
| **14（新 v3.1）** | **`s0_whitelist` schema 契约统一**（5 种形态 × 3 种消费者假设 → 全线 fail-open；`campaign.py` 读取路径为死代码；GBR 双重序列化） | 新增 | 全 13 区域 schema 清点，见 §12 |

> **9 项不可去除机制**（库存盘点、双比率、三方交叉、座位可达性、RN_EXPOSURE、ghost-audit、prod-first、submit_verdict、region_kb 自动刷新）评级全部维持——今日 JPN 实战为其中 6 项（profile 注入、typed catalog、字段验证闸、多样性闸、门禁分层、停止闸回落语义）提供了新区场景的正向验证。

---

## 11. Dry-Run 演练实录（JPN，纯只读，v3 修正版）

脚本：`logs/_tmp_ra_pipeline_dryrun.py`（v3：修正 signal_floor 查询位置→thresholds.json、priors_snapshot 小写键、白名单字符串列表解析、处女区积压口径）｜实录：`output_report/ra_pipeline_dryrun_transcript_jpn_20260916.txt`

### 逐步输入 → 输出 → 价值判定

| 步 | 关键输入（实测） | 演练输出/判定 | 价值判定 |
|---|---|---|---|
| 1 | JPN profile active；backtest 0 条；未消费积压 1,688；signal_floor=0.5@thresholds.json；stop_rules null→默认 enabled | 处女区：yield/conversion 均无意义（0 样本）；积压闸不适用 | profile 前置正确（universe 实测修正防非法档）；停止闸回落语义正常 |
| 2 | s0_ranking 20KB + whitelist 12 集（当日 14:19 生成）；region_kb 缺（正常，待首波回测后自动生成） | 规则 A/B 无输入→放行；三方交叉已产出 | ★★★ 放宽档+补偿三件套是处女区正确展开；⚠️ universe 双档切换时 P3 守卫依赖人工复核 |
| 3 | 8 份 typed catalog / 1.46MB（14:24 建成，先于 wave2 门禁） | catalog 前置时序正确 | ★★★ 类型错配防连坐；wave1 FIELD 闸拦下跨集混入字段实证有效 |
| 4 | gem 1,640 / selected 48 / probe 48→dropped；priors_snapshot_jpn 445B（小写键，14:28） | 生成:消费 = 34:1 | ★★★ priors 闭环机制正常；❌ 背压缺失——**单日 1,640 条 vs 七槽吞吐 ~29 批次日** |
| 5 | 体检包 2 个（analyst14/model25）但白名单 12 集交集=∅；wave2 门禁 all_pass=0 | **体检硬门 enforced: false**（gate_w2 ledger 原文）；多样性闸以 10 项 quota_violations 拦截 | ★★★ 多样性闸咬住 ratio_pair 超配 50%（生成侧结构偏斜被门禁兜住）；❌ 体检断层三连复发 |
| 6 | 无回测数据（JPN 未进 S3） | 处女区积压口径：首波回测后再判 | prod-first/settings prior 待首波验证 |
| 7 | 无 S4 数据 | — | fail-fast/过拟合机器判定待首波验证 |
| 8 | ProdCorr 下限示例 0.643 | 仍需实测（该式只能确定性劝退） | submit_verdict 唯一权威维持 |
| 9 | wave_results 1 条：wave1 closed 但 **verdict=None、payload 空** | 回写缺口实锤 | ★★ 新增建议 #13：探针波也要写 FAIL verdict，别留空壳 |

### 演练暴露的真实问题（v3 重排，按严重度）

1. **体检包断层三连复发**（DEU→IND→JPN）：开荒清单不含体检包生成，每次都在第一波裸奔后才发现。**根治方案升级**：把"体检包生成"写进开新区 SOP 的硬前置清单（profile + tracking/config + **体检包**），而非依赖事后补。
2. **生成背压缺失二连复发**（EUR 55 倍→JPN 34:1）：LLM 生成速度结构性快于回测吞吐，无硬闸则必积压。**根治方案升级**：GEM 生成器加 `--max-pending` 参数（超过阈值拒绝新批），比"步 4 前人工检查"可靠。
3. **探针波回写空壳**（JPN wave1）：closed 无 verdict——成熟区纪律（IND 98/98）没有迁移到新区。建议 #13。
4. **文档口径漂移**（priors_snapshot 小写键、feature_engineering 措辞、D3 加法配方）：小问题但每个都会造成一次演练/执行误判（本次演练脚本三处修正皆源于此类）。

### 元教训（v2→v3 递进）

v2 的教训是"SQL 错误被降级吞掉"；v3 的教训是**"口径匹配"三连**：键名大小写（priors_snapshot_JPN vs _jpn）、JSON 结构（whitelist 是字符串列表非 dict.candidates）、位置（signal_floor 在 thresholds.json 非 profile md）。**演练工具的价值恰恰在于：用低成本反复把这类"文档说 A、数据是 B"的错位暴露出来——每次 dry-run 至少逮住一个。**

---

## 12. 追加发现（v3.1 · 22:41 第三次核验轮新增）：`s0_whitelist` schema 漂移 × 消费者假设错配 → 全线 fail-open

> 触发：对 IND/JPN 重跑演练时，IND 报「白名单数据集数 0」而 JPN 报 12——同为 `s0_whitelist` 却解析结果相反。遂做全区域 schema 清点，发现这是一个**跨 13 区域、跨 3 个消费者**的契约漂移，而非脚本个例。

### 12.1 实测：同一 ledger 键 `s0_whitelist`，5 种互不兼容形态

| 区域 | schema 键 | universe 记录位置 | items |
|---|---|---|---|
| CHN / DEU / EUR / KOR | `candidates[]` | `settings.universe`（DEU 未记） | 3 / 9 / 8 / 2 |
| HKG / JPN / MEA / USA | `whitelist[]` | `settings.universe`（仅 HKG 有；JPN/MEA/USA 未记） | 3 / 12 / 4 / 5 |
| IND | `datasets[]` | **顶层 `universe`** | 3 |
| ASI / GLB | `other`（`counts/gate/delay...` / `analyst/earnings/...`） | ASI 顶层 `MINVOL1M` | — |
| **GBR** | **`str`（非 dict）** | — | — |

对照：`s0_ranking` 在全部 10 个有记录的区域**统一为 `ranking[]` 键、零漂移**（n=35–294）。→ 漂移**特异地集中在 `s0_whitelist`**，属该键写入方缺统一契约，非普遍现象。

### 12.2 三个消费者、三种假设，各自在自己的区域子集外**静默失效**

| 消费者 | 代码假设 | 实际命中 | 静默失效范围 |
|---|---|---|---|
| `tools/campaign_intel.py:124,129` | `candidates[].dataset` | CHN/DEU/EUR/KOR（4/13） | 其余 9 区 → 白名单视为空，override-gap 审计与白名单报表全部降级为"无数据" |
| `score_datasets.py::_check_universe_consistency`（P3 守卫） | `universe` 顶层 或 `settings.universe` | 有 universe 的 6 区 | DEU/JPN/MEA/USA/GLB **未记 universe** → `if u and u != cur` 短路 → **守卫静默跳过（fail-open）**；而 JPN 恰是双 universe 档（TOP1600/TOP1200）最需该守卫的区域 |
| `src/wqb/workflow/nodes/campaign.py:1293` | `filter_criteria.{delay,universe}` | **无任何区域** | 全 13 区永不命中 → 恒回落 `delay=1, universe="TOP3000"`，再被 regions 表 legal[0] 覆盖 |

### 12.3 两项硬证据（可直接复现）

1. **`filter_criteria` 全区域不存在**：`SELECT region FROM ledger_kv WHERE key='s0_whitelist' AND value LIKE '%filter_criteria%'` → 返回空。即 `campaign.py` 那段"从白名单推导 delay/universe"的逻辑是**死代码**，白名单锁定的 universe 从未被该节点消费。
2. **GBR 双重序列化**：value 为「JSON 字符串内再包一层 JSON」（`"{\"generated_at\":...}"`），任何单次 `json.loads` 的消费者拿到的是 `str` 而非 `dict` → 直接类型错配。

### 12.4 建议 #14（升为 P1）

统一 `s0_whitelist` 契约为**单一 schema**（推荐保留 `s0_ranking` 的稳定风格：顶层 `universe`/`delay` + `datasets[]`），并：
- 给 3 个消费者加**显式 fail-closed**：解析不到预期键时打 WARN 而非静默空集（当前 `campaign_intel` 与 P3 守卫都是 fail-open）；
- 修复 GBR 双重序列化；
- 删除或修正 `campaign.py` 的 `filter_criteria` 死读取路径。
- 加一条单测：遍历 `ledger_kv` 全部区域的 `s0_whitelist`，断言 schema 唯一 —— 防止第 6 种形态再长出来。

> 严重度评估：单个 fail-open 各自后果有限（多为少一条告警），但三者叠加意味着**白名单的实际消费路径无人完整走通**；且 P3 守卫恰在最需要它的 JPN 上失效。属"整改成本低、收益明确"的一类，故列为 P1。

---

*本报告基于 SKILL.md 2026-09-16 21:41 工作区版（未提交修改）与 `data/wqb.db` 21:53 末次写入快照。§12 为 22:41 第三次核验轮新增（全区域 schema 清点）。dry-run 全程只读：未写库、未触平台、未占配额；JPN 与 IND 实录已于 22:41 现场重跑，结果逐字复现。昨日 v2 报告（同目录）的九步子项级详表仍有效，本版为其增量修订。*
