# RA 九步流水线 v3 评审：逐阶段展开 · 价值评估 · 全流程模拟演练

- 日期：2026-09-28 23:0x（GMT+8）
- 对象：`wq-brain-ra-pipeline/SKILL.md` **v2.3**（92KB / 973 行，今日 20:01 更新）
- 性质：**纯评审 + 模拟演练** —— 未写库、未发平台请求、未修改任何业务文件（演练为推演层，见 §3.1）
- 与前作关系：09-27 已有 `ra_pipeline_stage_review_20260927.md`（1165 行，六轮真实环境复跑）与 `skills_stage_review_v2_20260927.md`（279 行）。
  本报告是 **v3**，基于 **SKILL v2.3 的 09-28 新增内容** 与 **当前真实库基线** 重判，**不重复** v2 已固化的结论；两报告结论冲突处以可复现运行结果为准。

---

## 0. 本次基线（只读实测，2026-09-28 23:00）

```
data/wqb.db（19 表）
  expressions        68,365   dropped 34,517 / gem 17,041 / superseded 11,083 / selected 2,460
                              backtested 1,511 / pending 1,458 / gated 121 / fail 99
                              completed 38 / submitted 31 / coverage 6
  gate_results        1,595   all_pass=1: 825 (51.7%)
  backtest_results    8,754   达标(S≥1.58 & F≥1.0) = 1,166  → 达标率 13.3%
  wave_results          965   FAIL 580 / PARTIAL 288 / PASS 96 / NULL 1
  waves               1,292   → 约 327 波无 verdict（步 9 完成定义未兑现）
  submit_ready          107   prod: 未测 47 / ≥0.7 撞墙 5 / 0.60–0.70 临界 41 / <0.60 干净 14
  submission_ledger      85
  registry_empirical  1,030   dead_end 482 / campaign 404 / win 102 / cross_region 28
  alphas              8,810
  达标但从未进 submit_ready = 1,101（94% 的达标成果从未走到提交判定）
```

### 0.1 分区漏斗（`backtest_results` 口径，回测转化率 = 该区真实投入产出）

> ⚠️ **口径警告（重要，今日 AMR 实证）**：`expressions.status` **不回写**（回测完成后仍滞留 gem/pending），
> 故"按 status 统计的回测量"系统性**低估**。今日 AMR 实证：积压闸因 conversion 分子恒 0 误杀后续波，
> 根因即 status 未回写；手动回写 40 条后 conversion 才从 0/212 变 18.9%。
> **下表统一采用 `backtest_results` 口径**（更接近真实投入），但两口径差额本身即是"记账债"的证据：
> 典型如 **GLB：status 口径 bt=0，而 `backtest_results` 有 2,144 条** —— 差额 100% 来自未回写。
> ⇒ 读任何漏斗数字前先确认口径；**status 口径只能用于"未消化积压"，不能用于"转化率"**。

| 区域 | 生成(expressions) | 回测 | 回测/生成 | 达标 | 达标率 | max\|S\| | 判读 |
|---|---|---|---|---|---|---|---|
| JPN | 15,185 | 254 | **1.7%** | **0** | 0% | 1.41 | ⛔ 最大浪费：1.5 万生成、零达标 |
| EUR | 12,752 | 569 | 4.5% | 27 | 4.7% | 2.09 | 生成侧严重过剩 |
| GLB | 8,315 | 2,144 | 25.8% | 161 | 7.5% | 4.65 | 产出率高，但有信号无提交（prod 墙） |
| USA | 9,504 | 1,003 | 10.6% | 39 | 3.9% | 2.42 | 标的问题 |
| GBR | 8,710 | 722 | 8.3% | 65 | 9.0% | 2.44 | — |
| IND | 2,749 | 782 | 28.4% | 231 | **29.5%** | 6.48 | 最强产出区 |
| DEU | 2,253 | 1,402 | 62.2% | 319 | **22.7%** | 2.17 | 转化率最高 |
| MEA | 657 | 498 | 75.8% | 99 | 19.9% | 2.38 | frozen 区，历史存量 |
| KOR | 1,975 | 467 | 23.6% | 37 | 7.9% | 2.37 | 本次演练区 |
| CHN/HKG/AMR/ASI | 5,257 | 913 | — | 188 | — | — | ASI 25.4%；CHN max\|S\|=4.96 却 0 达标 |

### 0.2 六条判据（v3 在 v2 的 V1–V5 之外**新增 V6**）

| 判据 | 含义 | 不通过的反例 |
|---|---|---|
| V1 可验证产物 | 产出可被下游消费的结构化产物（DB 表 / ledger / 文件包） | 只产人读文本 |
| V2 有真实调用方 | 存在生产路径调用点 + 回归测试守护 | 零调用方、无测试 |
| V3 有实证收益 | 有前后对照的量化收益记录 | 仅口头声称 |
| V4 不可被合并 | 与其它步骤不重叠、不可归并 | 与另一闸同源重复拦截 |
| V5 成本合理 | 零配额/本地可算，或有明确配额回报 | 高配额换低产出 |
| **V6 出口吞吐匹配（新增）** | 该步产能是否与下游**出口能力**匹配（REGULAR 4 + SUPER 1 + PPA 1 = 6 颗/日） | 生产 1,166 达标而出口仅消费 85 → 过量生产 |

> **V6 是本次新增判据**，理由是 v2 只按"各步自身效率"评判，无法解释一个矛盾现象：
> **每一步单看都在正常工作，但整链 12 个月只出口 85 颗**。V6 把"出口配额"作为硬约束引入，用于判定前段是否过量生产。

### 0.3 贯穿结论（三条，本次新增）

1. **出口饥饿 vs 前段过剩（V6）**：生成 68,365 → 达标 1,166 → 提交 85。
   **1,101 条达标成果（94%）从未进入 `submit_ready`**。前六步是过量生产，后三步是饥饿消费。
2. **瓶颈是分区的，不是全链统一的**：v2 用全区数据得出"最大问题是 S2→S3 断链（unconsumed 21,936）"；
   本次 KOR 实测漏斗显示 **掉得最狠的一跳是「回测完成 → 过廉价闸」，保留率仅 8.88%**。
   ⇒ 不能用单一结论指导所有区：JPN 该停生成，KOR 该提信号质量，GLB 该破 prod 墙。
3. **41 条临界金矿未被消费**：`submit_ready` 107 条中 **41 条落在 prod 0.60–0.70 临界区**（占已测 68%），
   另有 47 条 prod 未测。而 SOP 步 8 铁律明写「prod 0.60–0.70 当天提交、不先做变体」。
   ⇒ **这 41 条是当前 ROI 最高的资产，且正在随时间贬值**（IND mLm2xG1K 教训：prod 0.6997 → 隔日 1.0000 整族封死）。

---

## 1. 逐阶段展开（输入 / 处理 / 输出）

> 标注 `[09-28 新增]` 的为 SKILL v2.3 本日落地内容，是本次评审重点。

### 步 1 · S-PRE 查表 + 库存盘点

| 项 | 内容 |
|---|---|
| **执行者** | 编排本体 + `mcp__wqb-db__get_campaign_summary / get_dead_ends / get_dead_datasets / get_mining_yield`；`tools/build_gate_prior_from_inventory.py`、`tools/select_ra_basket.py` |
| **输入** | `$REGION`（唯一显式输入）；`references/regions/<R>.md`（磁盘实测 **14 份** profile，含 AMR）；DB 四表存量；`reports/dataset_experience/*.md`；PPA 公告（`get_messages` 实时重扫） |
| **处理** | ① profile 裁决（`entry_verdict`：MEA=`frozen` 步 1 即拒）；② **库存盘点优先**：枚举存量 → 资格门复算 → 写回 `gate_priors` → `select_ra_basket --target 20`（去参数网格 / OS 撞车预筛 / 篮内正交 / 平台复核）；③ 产出率双比率分离（`conversion` 低=管道问题、`yield_rate` 低=标的问题）；④ **[09-28 新增] 跨区死路检查**（不限 region 查 `registry_empirical`，`cross_region_lessons` 现存 11 条）；⑤ PPA 主题门禁（禁复用 settings 快照） |
| **输出** | universe / delay / 中性化 / 排除集 / 排除信号族 / 波号 + `gate_priors` + `cache/basket.json` |
| **失败分支** | registry 全空 = 新区域进步 2；候选足以覆盖目标塔则**不进**步 2 |

### 步 2 · S0 数据集体检 + 金字塔配置

| 项 | 内容 |
|---|---|
| **执行者** | `workflow_campaign(stage="S0")` + `tools/campaign_intel.py s0-select` + toolkit `score_datasets.py` |
| **输入** | 平台 `get_datasets` / `get_pyramid_alphas` 实测点亮；`region_kb` win 层；`saturated_datasets`；体检包（磁盘实测 **495 个**，非文档所记 320） |
| **处理** | ① 三方交叉（平台真实点塔 × 严格口径产出率 × 判死清单），`lit=Y` 已点亮塔剔除；② **两步必需**：`calibrate`（只写 thresholds、不产排名）→ 裸 `stage="S0"`（产 `s0_ranking`）；③ 座位可达性（Σ`est_seats` < target → WARN 结构性不可达）；④ 锁白名单（≥2 非 MODEL、`category_weight` 0.9–1.15）；⑤ 饱和路由；⑥ **[09-28] 体检包硬前置**（`--inspect-mode enforce` 缺包整波拦截） |
| **输出** | `s0_ranking` / `s0_whitelist` / `s0_calibrate_<region>` / `*_dead` |
| **失败分支** | 无非 MODEL → 写 findings；全硬排除 → 回步 1 换区 |

### 步 3 · S1 字段扫描 + **[09-28 新增] 闸 SEM 语义归类**

| 项 | 内容 |
|---|---|
| **执行者** | `workflow_campaign(stage="S1")` + L1 三件套 + **`tools/field_semantic_classify.py`（新增，10KB）** |
| **输入** | 白名单数据集 + `get_datafields`（`fields` 表 268,714 行 / `field_profile` 30,705 行） |
| **处理** | ① typed catalog 落地 `fields` + ledger `s1_<ds>_d<delay>`；② 字段级覆盖审计（防空集）；③ 幽灵字段验活（`validate_fields=true`）；④ `users` 分级（≥50 只验方向 / 10–49 进池必实测 prod / 0–9 优先，冷门占批 ≥50%）；⑤ **[09-28 新增] 语义归类**：产出 `s1_semantic_<ds>`（signal / blocked / by_category），黑名单 = 货币码 / 汇率叉乘 / 标识符 / 分类码 / 标志位 / 期间口径 / 股份类别 |
| **输出** | typed catalog + `s1_semantic_<ds>` + **`s2_field_pool_<ds>`**（GEM 字段池） |
| **失败分支** | 字段 <10 退回步 2；**缺 `s1_semantic_<ds>` → 步 5 `wave_gate` exit 2 整波阻断**（fail-closed，回归 `tests/unit/test_semantic_gate_failclosed.py` 10.7KB） |

> **实证依据（V3）**：KOR/fundamental17 首波 348 条产物中 **49.4%** 落在非信号字段（货币码比较、三角套汇恒等式），
> 语法全对、语义全废，语法闸与 gate.py 都拦不住，只能靠回测烧配额；黑名单字段仅占 9.9% 却吃掉 49.4% 生成预算。

### 步 4 · S2 概念优先生成（GEM）+ **[09-28 新增] 形状配额**

| 项 | 内容 |
|---|---|
| **执行者** | `workflow_gem` → `brain-make-some-gem/scripts/headless_runner/run.py`；预闸 `pipeline_pregate`；**`tools/shape_quota_check.py`（新增，5.6KB）** |
| **输入** | priors 快照（`assemble-priors`，DB 为单一事实源）+ `s2_field_pool_<ds>` + settings + ideas（仅 LLM/人工 source 才注入） |
| **处理** | ① priors 组装（只消费 `wins`≤6 / `dead_ends`≤12）；② gate_priors 分流（`by_operator_count`/`by_field_family` 进 prompt；`by_decay`/`by_neutralization` 由步 6 改写设置）；③ LLM 概念生成（机制 → 1–2 字段 id → 例）；④ 预闸（quantile 归一 / 毒模式丢弃 / hump 命名参数 / bucket range / 非标窗口归一 / 同骨架封顶 12）；⑤ **[09-28 新增] 形状配额**：每波 ≥3 个 shape family，`trade_when` 占比 ≤40%（对策：wave84/85 实测 19 条仅 ~9 个算子形状、trade_when 占 62%，而已验证算子 103 个、KB 模板 141 条零调用）；⑥ 契约波 vs 探索波分跑 |
| **输出** | `expressions` status=gem/enhanced（全库 17,041 条处此状态） |
| **失败分支** | GEM 未入库按超时清单查；402 余额不足退 ideas 旁路；机制枯竭 → `forum_recon` 回补 KB |

### 步 5 · S2→S3 门禁（含 5b prod-first、**[09-28] 闸5 等权拦截**）

| 项 | 内容 |
|---|---|
| **执行者** | `tools/wave_gate.py` + toolkit `gate.py:check_batch_diversity` + `field_inspect_gate.py` + `campaign_intel ghost-audit / prod-first` |
| **输入** | 本波 `expressions`（`--from-db`）+ typed catalog + 体检包 + `platform_constraints.json`（**v1.5，已确认含 `equal_weight_leg_add`**）+ `explore_contract` + `alphas` prod 记录 |
| **处理** | ① 幽灵算子硬闸（零配额，防整批 CANCELLED 连坐）；② 闸 1–8（语法/白名单/VECTOR/不可访问算子/**毒模式**/批级多样性/longCount/EVENT）；③ **闸 SEM**；④ **闸 PF**（骨架级 prod 死路，fail-closed）；⑤ **[09-28 新增] 毒模式 `equal_weight_leg_add`**：拦截 `add(rank(A),rank(B))`、`add(group_rank(A,g),group_rank(B,g))` 等等权相加；⑥ 体检硬门 5 条；⑦ 5b prod-first 探针 |
| **输出** | `gate_results`（`all_pass` / `fail_reasons`）+ `prod_first_<wave>` |
| **失败分支** | 语法 FAIL 必修；多样性 FAIL 回步 4 补骨架（软触发：结构熵 <1.5 即补，不等硬 FAIL） |

> **[09-28] 事故修复依据**：旧版文档称「`0.5*rank(A)+0.5*rank(B)` 被闸5 block」，但**实现层是假的**——
> `_detect_weighted_mix_structural` 只拦「实参以 `系数*` 开头」的腿，**明文豁免等权**。
> KOR wave189/190 因此有 **7 条** `add(group_rank(腿A), group_rank(腿B))`（含 S=2.11 / F=1.80 / 2Y=1.89）漏过闸5，已全部作废。
> 现由 `tests/unit/test_gate_equal_weight_leg_add.py`（7.3KB，16 条：7 违规必拦 / 7 合规必放 / config 断言 / DB 作废断言）守护。

### 步 6 · S3 七槽回测

| 项 | 内容 |
|---|---|
| **执行者** | `workflow_batch_track` / toolkit `pipeline.py run`（并发唯一来源 `wqb-concurrency` §8） |
| **输入** | 过闸批次 + `settings.json` + `region_kb.gate_priors` |
| **处理** | ① settings prior 改写（样本 ≥30 且过闸率 ≥ 当前 ×2 才改）；② 七槽填槽（Token-Bucket C≈7；multi(8) 86.1 α/hr vs single 54.3，1.59×）；③ 连坐隔离（定位坏式 → 回写 fail → 无辜式重发批优先下槽）；④ 槽位仲裁（`WQB_GLOBAL_SLOTS=7`）；⑤ 收批压缩（18 次调用 → 2 次）；⑥ QUICK/FULL 模式（QUICK 不可提交） |
| **输出** | `backtest_results`（全库 8,754）+ `wave_results` + ckpt + `expressions.status=backtested` |
| **失败分支** | 故障协议表（8 子全 ERROR 重发 / fatal 算子隔离 / 429 退避 / took-too-much-resource 去 backfill） |

### 步 7 · S4 诊断改进 + **[09-28] 四道提交闸 / SUB 比例律**

| 项 | 内容 |
|---|---|
| **执行者** | `review_wave.py` + `campaign_intel s4-prescreen / prod-first` + `wq-brain-alpha-optimization-v1` + `tools/forum_recon.py` |
| **输入** | 本波 `backtest_results` alpha_id + `thresholds.review` + OS 衰减基线 + `salvage_pool` |
| **处理** | ① s4-prescreen 分层（REJECT 直接判死，≈8× 效率）；② walls 诊断（`RN_EXPOSURE`：risk_neutralized ≤0 且 sharpe≥1.58 ⇒ 就是那个暴露本身 → dead_end 禁调参；`ROBUST_STRUCTURAL` 拒入 near）；③ prod-first 探针；④ OS 衰减校准（expOS = IS×0.358，**仅参考不作排序**）；⑤ **[09-28 新增] 四道提交闸 + SUB 比例律**：`LOW_SHARPE ≥1.58` / `LOW_FITNESS ≥1.0` / `LOW_2Y_SHARPE ≥1.58` / `LOW_SUB_UNIVERSE_SHARPE ≈ 0.571 × 本 alpha sharpe`（三处独立实证：1.03/1.80、1.12/1.96、0.89/1.55）；破比值闸旋钮 = 换分组轴 `market`/`exchange`、`signed_power` 压尾、长窗平滑；⑥ **[09-28] 卡闸找武器**（Mode B 2–3 轮仍卡墙 → `forum_recon --out ledger`，每波 ≤1 次） |
| **输出** | `s4_walls_<region>_<wave>` + `salvage_pool` + review payload + 换概念/换腿决策 |
| **失败分支** | prod ≥0.7 → Mode B 换概念；同想法 >10 结构不过 → 步 9 记 dead_end 回步 2 |

### 步 8 · S4→S5 稳健闸 + 提交判定

| 项 | 内容 |
|---|---|
| **执行者** | `brain-alpha-robustness`（必经）+ `mcp__wq-brain-http__submit_verdict` + `worldquant-submit-alpha` / `wq-brain-superalpha` |
| **输入** | 达标候选 + `is.checks` 全量 + WebDataScope failed-counts |
| **处理** | ① Failed-count 资格门（RA 要求 `Failed RA == 0`，比只看 `result=="FAIL"` 严格）；② `submit_verdict` 零成本判定（`degraded_gates` 非空 ⇒ 不可作依据）；③ **prod 0.60–0.70 当天提交、不先做变体**（mLm2xG1K 教训：prod 0.6997 隔日变 1.0000）；④ 报告 SUBMITTABLE → **等用户确认**；⑤ POST 四形态处置（200 通过 / 201 异步 4min 未翻 → re-POST / 200 空体必须补发 / 403 零成本带回全量 checks）；⑥ **[09-28] 补发已工具化**（节点 Step 4 内置四态处置） |
| **输出** | `submit_ready`（107）+ `submission_ledger`（85）+ ACTIVE alpha |
| **失败分支** | PROD/SELF 不过回步 7；配额耗尽挂起，继续步 2→9 |

### 步 9 · S6 复盘回写

| 项 | 内容 |
|---|---|
| **执行者** | `tools/step_funnel.py` + `upsert_wave_result / upsert_registry_empirical` + `campaign_intel pyramid` + `dataset-experience` + `seal_dead_end` |
| **输入** | 本波四表存量 + ledger + 平台塔状态 |
| **处理** | ① `step_funnel` 只读定位瓶颈（不凭印象写 verdict）；② verdict **强制枚举**（PASS/PARTIAL/FAIL）；③ 判死封存（先 `seal_dead_end` 沉降入 salvage_pool，再记 dead_end；**[09-28] 判死前先 `forum_recon --out negative` 取证**，found=true 不得判死）；④ `region_kb` 刷新；⑤ pyramid 点塔进度进 key_findings；⑥ `dataset-experience` 沉淀；⑦ **[09-28] `s6_verdict_<wave>` 已废弃去重**（唯一真相源 = `wave_results.verdict`）；⑧ **S6 完成定义**：三件回写后必须再跑 `assemble-priors` 刷新快照 |
| **输出** | `wave_results.verdict`（965）+ `registry_empirical`（1,030）+ `reports/dataset_experience/*.md` |
| **失败分支** | 停止闸 B1/B2 机械判定（同轴 3 连可计数 FAIL 熔断 / 窗口内 ≥4 轴全 FAIL 停区） |

---

## 2. 价值评估

### 2.1 汇总判定

| 步 | 判定 | 最强判据 | 保留深化项 | 精简/去除项 |
|---|---|---|---|---|
| 1 S-PRE | **★★★ 保留深化** | **V3**：09-07 实证 170 次新回测 0 产出 vs 一次库存扫描 20 条；**V5** 零配额 | 跨区死路检查（今日新增，治 KOR risk70 跨三区死族 114 条白跑）；**库存结论必须强制消费**（今日 41 条临界金矿） | PPA 主题扫描对纯 RA 波是固定开销（但仍便宜，保留） |
| 2 S0 | **★★★ 保留深化** | **V3**：已点亮塔剔除治本（IND 7 集 197 条 0 候选）；**V2** 体检包 495 个已落地 | 体检包 enforce 模式（5 区曾为 0 → 现已补）；座位可达性 | `calibrate --dry-run` 仅新区需要，日常可跳；**⚠ 与 §0.1 选塔优先律存在实操冲突**（见 §2.4 C1） |
| 3 S1 **+SEM** | **★★★ 保留深化（本日最高价值新增）** | **V3**：49.4% 生成预算曾被非信号字段吃掉；**V2/V1**：有 CLI + 回归测试 + fail-closed | 语义归类（黑名单 → 字段池 → GEM 注入，闭环完整） | `feature_engineering` 作"字段理解"**已收口**（确定性模板渲染、禁入 GEM） |
| 4 S2 **+形状配额** | **★★ 保留但需限流** | **V1**：68,365 条 expressions 的唯一来源；形状配额治同质化（trade_when 62% → ≤40%） | 概念优先 + priors 分流 + 预闸 | **V6 不通过**：KOR unconsumed 545（27.6%）、JPN 15,185 生成 0 达标 → **须按 S3 实测吞吐设生成准入配额** |
| 5 门禁 **+闸5等权** | **★★★ 保留（精简展示层）** | **V2/V3**：闸5 等权事故修复 + 16 条回归守护；**V5** 纯本地零配额 | 闸 SEM / 闸 PF / 幽灵算子硬闸（防连坐） | `validator.check_batch` **deprecated**（零生产调用方、判据不同）；`[opcat]` 质量预估只打印不判定 → 噪声 |
| 6 S3 | **★★★ 保留** | **V5**：七槽 ×7 吞吐 86.1 α/hr；**V3**：连坐隔离（JPN 一条 `bucket()` 缺 range 丢 64 条） | settings prior 直接改设置（治 decay 语义错配） | `batch_track` 入口不跑三闸（v2 D4，仍未修） |
| 7 S4 **+SUB比例律** | **★★★ 保留并加强**（v2 判"部分精简"，本次上调） | **V3**：KOR 实测瓶颈正在这一跳（保留率 **8.88%**）；SUB 比值律（0.571×S）是可计算的破墙钥匙 | forum_recon 卡闸找武器、换分组轴 `market`/`exchange`、s4-prescreen | **Mode A 参数层压缩**（实证仍撞 prod 0.84–0.85）；`RN_EXPOSURE` 行仍进 near/salvage → 应一并排除 |
| 8 提交判定 | **★★★ 保留并扩权（全链 ROI 最高）** | **V1**：85 颗提交的唯一路径；**V3**：四形态补发闭环（3 颗曾悬空 >24h）；**V6**：出口是唯一稀缺资源 | **立即消费 41 条临界 + 47 条未测 prod 存量** | `config.py::compute_webdata_failed_counts` 第三份相反实现（v2 D5，仍未修）→ 陷阱 |
| 9 S6 | **★★★ 保留** | **V4**：唯一让九步成环（region_kb 自动刷新）；verdict 枚举保证停止闸真实 | `step_funnel` 只读定位；`seal_dead_end` 沉降；forum_recon negative 取证 | 五张 `step_*` 表文档残留（DB 实测不存在）；**327 波无 verdict**（完成定义未兑现） |

### 2.2 建议去除 / 精简明细

| 项 | 处置 | 判据 |
|---|---|---|
| `wqb.expression.validator.check_batch` | **标注 deprecated** | V2：全仓零生产调用方；只实现 4 条形状闸且判据与执行口径不同 → 双口径误读 |
| 五张 `step_*` / `*_summary` 表引用 | **清理文档残留** | DB 实测不存在（19 表清单已核），留引用会误导 |
| `[opcat]` / 质量预估的 "FAIL" 打印 | **降级为 INFO** | V1：自称硬闸却不进 `all_pass` → 纯噪声 |
| 步 3 `feature_engineering` 注入 GEM | **保持禁用** | V1/V3 双不通过（GBR 实证：注入后 GEM 零 LLM 调用，整波退化为模板展开） |
| JPN / EUR 的生成侧继续投料 | **暂停**（V6） | JPN 15,185 生成 / 0 达标 / max\|S\| 1.41；EUR 12,752 生成 / 27 达标 → 边际产出≈0 |
| `brain-alpha-repair`（43 行配方查表） | **并入 optimization-v1** | V4：与其它改进入口重叠 |
| Mode A 参数层扫描 | **压缩至 ≤30% 精力** | V3：实证仍撞 prod 0.84–0.85，参数层破不了结构性墙 |
| `structural_variant_results` 表 | **归档** | DB 实测 **0 行**；文档已记"仅 1 行产出、降为实验性" |

### 2.3 保留深化的优先序（按 ROI）

1. **【最高】消费存量**：41 条 prod 0.60–0.70 临界 + 47 条未测 prod = 88 条待消费，按 6 颗/日需 ~15 天；
   且**每拖一天都在贬值**（mLm2xG1K 从 0.6997 → 1.0000）。→ 步 8 扩权，不等新挖。
2. **【高】步 7 破墙武器化**：KOR 瓶颈在"回测 → 达标"这一跳（8.88%）。SUB 比值律已给出可计算的钥匙
   （目标 = `SUB/S ≥ 0.571 ∧ 2Y ≥1.58 ∧ S ≥1.58 ∧ F ≥1.0`），应做成**预检**而非事后诊断。
3. **【高】步 4 生成准入配额**：按各区 S3 实测吞吐反推生成量，JPN/EUR 直接停。
4. **【中】补齐 327 波无 verdict** 的复盘（步 9 完成定义），否则停止闸 B1/B2 的窗口统计失真。
5. **【中】`batch_track` 下沉三闸**（v2 D4 未修）。

### 2.4 本次新发现的冲突与缺口

| # | 项 | 证据 | 建议 |
|---|---|---|---|
| **C1**<br>（冲突仍不成立，但**理由更正**） | 步 2「已亮塔不进白名单」vs 选塔优先律「已亮塔只作组腿」 | **改查平台 `get_pyramid_alphas`（唯一权威）后：`KOR/D1/fundamental = 3`（当前季度 Q3）⇒ ✅ 已点亮**；Q2 快照为 1。<br>用户口径「提交 ≥3 = 点亮」下该塔达标。<br>⚠ **但原判"两规则处置相反"是错的**：两条规则**方向一致**——都不该继续往已亮塔提交 REGULAR，故**冲突不成立**。<br>⚠ **真正的偏离（更有价值）**：今日提交的 `wpZkk1Mp` 正落在**已点亮**的 KOR/D1/FUNDAMENTAL，按两条规则 **本不该占 REGULAR 名额**（应转组腿池）。 | ① KOR 下一波主攻转向**未点亮塔**（shortinterest 0~1、earnings/imbalance/insiders/institutions/macro/news/socialmedia/sentiment/risk 全 0）；② 已亮塔候选（FUNDAMENTAL/ANALYST/MODEL/OTHER/PV）一律转组腿池；③ 补跑 `sync_platform_alphas.py` |
| **D8**<br>（★ 本次最大教训） | **本地 `alphas` 表不能做塔级统计** | 本报告先用本地表算出「KOR/D1/FUNDAMENTAL = 1，未点亮」，**结论错误**；平台实测 = 3（已点亮）。两个错源：<br>① **塔归属≠`datasets.category`** —— 塔归属来自平台 pyramid 匹配；本地 KOR 47% ACTIVE 的 `category=None`（`_unknown` 占位 422 条）。<br>② **`date_submitted` 全库仅 2.7% 非空**（KOR 3.5%），用它判"提交"必然低估。<br>（`platform_status` 非空率 83%，但仍推不出塔归属）<br>另：今日 `wpZkk1Mp` 未在 `alphas` 表。 | **在 SOP 中明写：点亮与塔归属一律查平台 `get_pyramid_alphas`，禁止用本地表推导**。`_unknown` 占位回填仍建议修（影响其它统计），但**不再作为点亮判定依据** |
| **C2** | **门禁过滤力弱**（新） | KOR `gate_results`：批次级通过率 50%，但**表达式级 95.1%**（351/369）。真正的过滤发生在回测后（8.88%） | 把可本地判定的判据（SUB 比值律、语义、形状）**前移**到门禁，省回测配额 |
| **C3** | **达标池沉没** | 1,166 达标 / 1,101 从未进 `submit_ready`（94%） | 步 7 出口接 `submit_ready` 自动化，不靠人工挑 |
| **C4** | **步 9 完成定义未兑现** | waves 1,292 vs wave_results 965 → 327 波无 verdict | 批量补写（verdict 已支持枚举归一） |
| **C5** | 体检包文档数字过期 | 文档记 320 个，磁盘实测 **495** 个；profile 记 13 份，实测 **14** 份 | 同步（低优先级） |

---

## 3. 全流程模拟演练（不实际修改）

### 3.1 演练设定与诚实声明

- **演练对象**：`REGION=KOR`、`DS=other466`（今日实证冷门 fundamental，users 0–14，已出 `wpZkk1Mp` ACTIVE）、
  `DELAY=1`、`UNIVERSE=TOP3000`、`WAVE=s2_oth466_d1_w191`（**虚构波号，仅用于推演**）
- **演练性质**：**推演层（dry-walkthrough）** —— 每步输入取自**当前真实库的只读快照**，处理动作按 SOP 逐条走，
  输出为**推演增量**（不落库）。与 09-27 v2 的 `executor(dry_run=True)` **代码层**演练互补：
  代码层验证"命令能否构建"，推演层验证"数据走到这一步会发生什么"。
- **零副作用**：本次未写库、未发平台请求、未创建/修改任何业务文件。
- **演练中标注**：`[真实]` = 来自 DB 实测；`[推演]` = 按 SOP 推定的输出。

### 3.2 逐步推演：输入 → 处理 → 输出变化 → 价值判定

---

#### 步 1 · S-PRE 查表 + 库存盘点

| | 内容 |
|---|---|
| **输入** | `$REGION=KOR`；profile `KOR.md`（`entry_verdict=active`）**[真实]**；DB 存量：KOR expressions 1,975 / backtest 467 / 达标 37 / `submit_ready` 17 / wave_results FAIL54·PARTIAL23·PASS7 **[真实]** |
| **处理** | ① profile 裁决 → active，放行；② **库存盘点**：`build_gate_prior_from_inventory --regions KOR --write-priors` → `select_ra_basket --target 20`；③ 跨区死路 SQL 检索 `other466` → `[真实]` `cross_region_lessons` 11 条中无 other466 记录 → 无跨区负先验；④ PPA 主题重扫（当期 All regions / D1 / Oct`26，要求单数据集 + PV 或 fundamental → **other466 属 fundamental，主题匹配**） |
| **输出** | universe=TOP3000 / delay=1 / 中性化=STATISTICAL / 排除集={已判死族} / 波号 w191；`gate_priors` 刷新；`cache/basket.json` **[推演]** |
| **价值判定** | **★★★ 通过 V3+V5**（零配额）。**本次触发新结论**：`submit_ready` 已有 17 条 KOR 存量，其中临界/未测 prod 的应先消费 → **演练在此分叉**：不直接开新波，先转步 8 消费存量 |
| **演练决策** | ✅ **本步有价值，且应强制"库存未清空不进步 2"** |

---

#### 步 2 · S0 数据集体检

| | 内容 |
|---|---|
| **输入** | **点亮实测（平台 `get_pyramid_alphas`，唯一权威）**[真实]：KOR/D1 = analyst 6 / **fundamental 3** ✅ / model 4 / other 6 / pv 3 全部**已点亮**；未点亮 = shortinterest 0~1、earnings·imbalance·insiders·institutions·macro·news·socialmedia·sentiment·risk 全 0。体检包 **[真实：KOR 仅 1 个包]** |
| **处理** | ① `s0-select` 三方交叉；② **`lit=Y` 剔除** → other466 的塔归属 FUNDAMENTAL **已点亮（3）** → **硬规则 0 触发，other466 不得作主攻集**；③ `calibrate` → 裸 S0 打分；④ 座位可达性 |
| **输出** | `s0_ranking` / `s0_whitelist` —— **other466 被剔除**，白名单改指向未点亮塔 **[推演，依据平台实测]** |
| **价值判定** | **★★★ 保留**。本次在此**两度修正**：先用本地表判"未点亮"（错），改查平台后为"已点亮"。<br>结论：步 2 硬规则与选塔优先律**方向一致**（都不该往已亮塔投 REGULAR），C1 冲突不成立。 |
| **演练决策** | ⛔ **本波不合法，驳回重选** → KOR 下一波应攻**未点亮塔**。<br>⚠ 连带发现：今日 `wpZkk1Mp` 落在已亮 FUNDAMENTAL 塔却占了 REGULAR 名额，按两条规则**应转组腿池**——这是规则与实操的真实偏离 |

---

#### 步 3 · S1 字段扫描 + 闸 SEM（假设 C1 裁决为"允许作补座腿"继续）

| | 内容 |
|---|---|
| **输入** | `get_datafields(KOR, other466, delay=1)`；字段池 **[真实：全库 `fields` 268,714 行]** |
| **处理** | ① typed catalog → ledger `s1_oth466_d1`；② 覆盖审计（防空集）；③ 幽灵字段验活；④ `users` 分级（other466 users 0–14 → 属**冷门优先**，理论 prod≈0）；⑤ **[09-28 新增]** `field_semantic_classify.py --region KOR --dataset other466 --write-ledger` |
| **输出** | `s1_semantic_oth466`（signal_fields / blocked_fields / by_category）+ `s2_field_pool_oth466` **[推演]** |
| **价值判定** | **★★★ 本日最高价值新增（V2+V3）**：KOR 同类集实证 49.4% 预算曾被非信号字段吃掉；有 CLI、有回归测试、fail-closed（缺台账 exit 2）。 |
| **演练决策** | ✅ **保留深化**；且本步是本次演练中**唯一同时满足 V1/V2/V3/V5 的新增项** |

---

#### 步 4 · S2 GEM 生成 + 形状配额

| | 内容 |
|---|---|
| **输入** | priors 快照（`assemble-priors`，wins≤6 / dead_ends≤12）；`s2_field_pool_oth466`；settings；KOR 现存 `unconsumed = 545`（gem317+pending143+gated58+selected27）**[真实]** |
| **处理** | ① GEM 概念优先生成（机制 → 字段 → 例）；② 预闸（quantile 归一 / 毒模式丢弃 / hump / bucket / 非标窗 / 同骨架封顶 12）；③ **[09-28]** `shape_quota_check.py`：≥3 shape family、`trade_when` ≤40% |
| **输出** | 本波新增 expressions ~8–20 条（status=gem）**[推演]**；KOR `unconsumed` 545 → ~560 |
| **价值判定** | **★★ V6 不通过（产能过剩）**：KOR 已积压 545 条未消化（27.6%），继续生成只增积压。<br>但**形状配额本身 V3 通过**（治 wave84/85 的 9 形状 / trade_when 62% 同质化）。 |
| **演练决策** | ⚠️ **条件放行**：仅在 `unconsumed < S3 近 7 日实测吞吐 × 2` 时生成；否则跳过本步、直接消费积压。<br>**JPN/EUR 在此应直接停**（15,185→0 达标 / 12,752→27 达标） |

---

#### 步 5 · S2→S3 门禁

| | 内容 |
|---|---|
| **输入** | 本波表达式（含一条**故意违规**样本：`add(group_rank(ts_mean(f1,22), market), group_rank(ts_mean(f2,66), market))` 用于验证闸5）**[推演]**；体检包（KOR **仅 1 个**，other466 可能缺包）；`platform_constraints.json` **v1.5** **[真实]** |
| **处理** | ① `ghost-audit`（幽灵算子，零配额）；② `wave_gate.py`：闸 1–8 + 闸 SEM + 闸 PF + **闸5 `equal_weight_leg_add`** + 体检硬门 5 条 |
| **输出** | 违规样本 → **被闸5 拦截并剔出候选**（不进回测）**[推演，依据：回归测试 7 违规必拦]**；`gate_results` 新增一行 |
| **价值判定** | **★★★ V2+V3+V5**：等权漏洞已由 16 条回归守护；纯本地零配额。<br>**但暴露 C2**：KOR 表达式级通过率 95.1% —— 门禁几乎不拦，过滤力在回测后。 |
| **演练决策** | ✅ **保留**；同时建议把 SUB 比值律等可本地判定的判据**前移到本步**（省配额） |

---

#### 步 6 · S3 七槽回测

| | 内容 |
|---|---|
| **输入** | 过闸 ~8 条；settings（decay / neutralization=STATISTICAL）；`region_kb.gate_priors` |
| **处理** | ① settings prior 改写（样本 ≥30 且过闸率 ≥ 当前 ×2 才改）；② 七槽并发（86.1 α/hr）；③ 连坐隔离；④ 收批压缩（18→2 次调用） |
| **输出** | `backtest_results` +8；KOR 回测 467 → 475；`expressions.status=backtested` **[推演]** |
| **价值判定** | **★★★ V5**：吞吐是真实杠杆。<br>⚠️ `batch_track` 入口不跑停止/天花板/积压三闸（v2 D4 未修） |
| **演练决策** | ✅ **保留**；补三闸下沉 |

---

#### 步 7 · S4 诊断改进（本波 8 条回测结果）

| | 内容 |
|---|---|
| **输入** | 8 条回测（假设最佳：S=1.72 / F=1.15 / 2Y=1.41 / SUB=0.98 / prod 未测）**[推演]**；OS 衰减基线；`salvage_pool` |
| **处理** | ① `s4-prescreen` 分层；② walls：`RN_EXPOSURE`（risk_neutralized ≤0？）/`ROBUST_STRUCTURAL`；③ prod-first 探针（骨架指纹 `rank→ts_backfill`）；④ **[09-28] SUB 比例律**核验：SUB/S = 0.98/1.72 = **0.570 < 0.571** → **差 0.001 卡闸**；2Y=1.41 < 1.58 → **也卡** |
| **输出** | 判据：`SUB/S ≥0.571 ∧ 2Y ≥1.58 ∧ S ≥1.58 ∧ F ≥1.0` → 本条 **2Y 与 SUB 双卡** → 进 near 池，转 Mode B |
| **价值判定** | **★★★ 本次上调**（v2 曾判"部分精简"）：**KOR 实测瓶颈正在这一跳（保留率 8.88%）**，SUB 比值律给了可计算的钥匙。<br>破墙旋钮：换分组轴 `market`（KOR/other466 实证把比值 0.55 → **0.59**，决定性）；`exchange` 给 2Y |
| **演练决策** | ✅ **保留并加强** → 下一步做 `group_rank(R, market)` 变体（**单信号结构，合规**），而非加权混合 |

---

#### 步 8 · 提交判定（演练在此消费存量，而非新挖）

| | 内容 |
|---|---|
| **输入** | ① 存量：`submit_ready` 107 条中 **41 条 prod 0.60–0.70 临界 + 47 条未测** **[真实]**；② 本波 near 候选（暂不达标） |
| **处理** | ① Failed-count 资格门（RA 要求 `Failed RA == 0`）；② `submit_verdict`；③ **按铁律：prod 0.60–0.70 当天提交、不做变体**；④ 用户确认；⑤ POST 四形态处置（403 零成本带回真实 PROD/SELF） |
| **输出** | 按 6 颗/日（REGULAR 4 + SUPER 1 + PPA 1）消费；本日演练**推演提交 4 颗 REGULAR**（从 41 条临界中按 IS 强度降序取 4）**[推演]** |
| **价值判定** | **★★★ 全链 ROI 最高（V1+V3+V6）**：出口是唯一稀缺资源；41 条临界金矿**每拖一天都在贬值**。 |
| **演练决策** | ✅ **扩权**：把"达标 → `submit_ready`"自动化（今日 1,101 条达标从未进入），并把临界区候选**前置**于任何新挖 |

---

#### 步 9 · S6 复盘回写

| | 内容 |
|---|---|
| **输入** | 本波：`wave_results` KOR FAIL54/PARTIAL23/PASS7 **[真实]**；`step_funnel --region KOR` 实测 **[真实：瓶颈 = 回测→过闸，保留率 8.88%]** |
| **处理** | ① `step_funnel` 定位（不凭印象写 verdict）；② verdict 枚举：本波 0 达标 + ≥1 near → **PARTIAL**；③ `seal_dead_end` 前先 `forum_recon --out negative` 取证；④ `region_kb` 刷新 + `pyramid` 点塔进度；⑤ `dataset-experience` 沉淀；⑥ **重跑 `assemble-priors`** 刷新快照（S6 完成定义） |
| **输出** | `wave_results.verdict=PARTIAL` +1；`registry_empirical` near/dead 更新；`reports/dataset_experience/kor_other466_campain.md` **[推演]** |
| **价值判定** | **★★★ V4**：唯一让九步成环。<br>⚠️ **C4**：KOR 有 84 波（54+23+7）但全区 327 波无 verdict → 停止闸 B1/B2 窗口统计失真 |
| **演练决策** | ✅ **保留**；补写 327 波 verdict |

---

### 3.3 演练结论（九步走完后的净变化）

| 指标 | 演练前（真实） | 演练后（推演） | 说明 |
|---|---|---|---|
| KOR expressions | 1,975 | ~1,985 | +10（受生成准入配额约束） |
| KOR backtest_results | 467 | 475 | +8 |
| KOR wave_results | FAIL54/PARTIAL23/PASS7 | PARTIAL +1 | verdict=PARTIAL（0 达标 + 有 near） |
| KOR submit_ready | 17 | 17（消费 4 颗 REGULAR 存量） | **存量被消费，而非新增积压** |
| 全局 submitted | 31 | 推演 +4 | 出口侧是真实增量 |
| 拦下的违规 | — | 1 条等权 `add(group_rank,group_rank)` | 闸5 生效 |

**本次演练的三个可执行结论**：

1. **演练在步 1 就该分叉** —— KOR 有 17 条 `submit_ready` 存量、全局 41 条临界金矿，
   **正确动作是先转步 8 消费，而不是走完九步再挖新的**。当前 SOP 没有强制这个分叉。
2. **演练在步 2 被驳回** —— 平台实测 `KOR/D1/fundamental = 3` **已点亮**，硬规则触发，other466 不得作主攻集。
   **附带的真问题**：今日 `wpZkk1Mp` 落在已亮塔却占了 REGULAR 名额 —— 规则与实操存在偏离。
   **另附本次最大教训（D8）**：我先用本地 `alphas` 表判"未点亮"是错的——`date_submitted` 全库仅 2.7% 非空，
   且塔归属≠`datasets.category`。**塔级统计只能查平台**，这条应写进 SOP。
3. **演练在步 7 暴露真正的卡点** —— 不是"没生成"，而是"生成了过不了 SUB 比值闸"（0.570 vs 0.571，差 0.001）。

### 3.4 演练无法覆盖的环节（诚实声明）

1. **LLM 可达性**：GEM 依赖 LLM，余额不足表现为误导性的 `no meta.json within 90s`；干跑验证不了，会显示假绿。
2. **真实 POST submit**：提交类必须用户显式确认，本次仅推演四形态处置。
3. **prod 实测值**：41 条临界的 prod 会随时间变化（mLm2xG1K 实证 0.6997 → 1.0000），推演值是当前快照。
4. **平台塔点亮状态**：需实时 `get_pyramid_alphas`，本次用记忆中的 KOR 状态。
5. **本次为推演层**：输出增量为按 SOP 推定，非真实执行结果；真实执行结果以 09-27 的 `executor(dry_run=True)` 代码层演练为准。

---

## 4. 审阅清单（需你确认）

| # | 事项 | 我的建议 | 决策 |
|---|---|---|---|
| 1 | 九步判定：步 1/2/3/5/6/7/8/9 = ★★★，步 4 = ★★（需限流） | 认可则无需动作 | ☐ |
| 2 | ~~C1 裁决~~ → **冲突不成立**（平台实测 FUNDAMENTAL 已点亮=3，两条规则方向一致：都不该往已亮塔投 REGULAR） | 无需裁决；**但 KOR 下一波必须换未点亮塔**（shortinterest 0~1 及全 0 塔） | ☑ |
| 2b | **D8（★ 最高优先）**：SOP 明写「点亮/塔归属一律查平台 `get_pyramid_alphas`，**禁止用本地 `alphas` 表推导**」 | **做**（本次已因此算错一次结论；本地 `date_submitted` 仅 2.7% 非空、塔归属≠`datasets.category`） | ☐ |
| 2c | 今日 `wpZkk1Mp` 落在**已点亮** FUNDAMENTAL 塔却占 REGULAR 名额 | 记录为规则偏离；后续已亮塔候选**转组腿池**，不占 REGULAR | ☐ |
| 3 | **消费 41 条临界 + 47 条未测存量**（最高 ROI） | 立即做，先于任何新挖 | ☐ |
| 4 | 步 4 按 S3 实测吞吐设生成准入配额；**JPN / EUR 直接停生成** | 做（V6，作用在真实瓶颈） | ☐ |
| 5 | SUB 比值律前移到步 5 门禁（省回测配额） | 做（C2，门禁表达式级通过率 95.1% 说明过滤力在后段） | ☐ |
| 6 | 「达标 → `submit_ready`」自动化（治 1,101 条沉没） | 做（C3） | ☐ |
| 7 | 补写 327 波无 verdict（步 9 完成定义） | 做（C4，否则停止闸窗口失真） | ☐ |
| 8 | 去除/标注：`validator.check_batch`、五张 `step_*` 残留、`[opcat]` 噪声打印 | 做（纯清理） | ☐ |
| 9 | `batch_track` 下沉三闸（v2 D4）；`config.py` 第三份相反实现（v2 D5） | 做（均未修） | ☐ |

---

> **与前作关系**：本报告未覆写 09-27 任何产物，文件独立为 `reports/ra_pipeline_stage_review_v3_20260928.md`。
> 两报告结论冲突处（如"瓶颈在 S2→S3 断链" vs "KOR 瓶颈在回测→达标"），
> **建议以分区口径为准**：全区结论适用于跨区资源分配，分区结论适用于单区战术。
