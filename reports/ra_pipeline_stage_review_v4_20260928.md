# RA 九步流水线：逐阶段展开 · 价值评估 · 全流程模拟演练（v4）

- 日期：2026-09-28 23:27（GMT+8）
- 对象：`wq-brain-ra-pipeline/SKILL.md` **v2.3**（92KB / 973 行，2026-09-28 20:01 更新）
- 性质：**纯评审 + 模拟演练** —— 未写库、未发平台请求、未修改任何业务文件
- 数据纪律：**塔级/点亮判定一律取平台 `get_pyramid_alphas`**；本地 `alphas` 表**不用于**塔级统计（见 §0.2）
- 与 09-27 两份评审（1165 行主报告 / 279 行独立视角）的关系：本版独立成篇，聚焦 v2.3 与当前实测；冲突处以可复现运行结果为准

---

## 0. 基线、口径与贯穿结论

### 0.1 实测基线（只读，2026-09-28 23:00）

```
data/wqb.db（19 表）
  expressions        68,365   dropped 34,517 / gem 17,041 / superseded 11,083 / selected 2,460
                              backtested 1,511 / pending 1,458 / gated 121 / fail 99
                              completed 38 / submitted 31 / coverage 6
  gate_results        1,595   all_pass=1: 825 (51.7%)
  backtest_results    8,754   达标(S≥1.58 & F≥1.0) = 1,166 → 13.3%
  wave_results          965   FAIL 580 / PARTIAL 288 / PASS 96 / NULL 1
  waves               1,292   → 约 327 波无 verdict
  submit_ready          107   prod: 未测 47 / ≥0.7 撞墙 5 / 0.60–0.70 临界 41 / <0.60 干净 14
  submission_ledger      85
  registry_empirical  1,030   dead_end 482 / campaign 404 / win 102 / cross_region 28
  alphas              8,810   platform_status=ACTIVE 134
  达标但从未进 submit_ready = 1,101（94%）
```

### 0.2 两条口径纪律（本次硬性遵守）

1. **塔点亮**：判定**唯一权威 = 平台 `get_pyramid_alphas`**（按季度返回 region/delay/category 计数），口径 = **提交 ≥3 = 点亮**。
   **禁止用本地表推导**，原因是两个实测缺陷：
   - `alphas.date_submitted` **全库仅 2.7% 非空**（8840 条中 243 条）→ 用它判"提交"必然低估；
   - **塔归属 ≠ `datasets.category`**：塔归属来自平台 pyramid 匹配，本地 KOR 47% 的 ACTIVE 记录 `category=None`（挂 `_unknown` 占位 422 条）。
2. **转化率**：一律用 `backtest_results` 口径。`expressions.status` **不回写**（回测完成后仍滞留 gem/pending），
   故 status 口径只能看"未消化积压"，**不能算转化率**（GLB status 口径回测=0，实际 `backtest_results` 有 2,144 条）。

> 提示：`get_pyramid_alphas` 传 `start_date=2026-06-30` 会被对齐到 **Q2 快照**（KOR fundamental 显示 1）；
> 默认调用返回**当前季度 Q3**（KOR fundamental=3）。做"近 90 天"判定请用默认季度值，勿用传参值。

### 0.3 平台实测塔状态（2026-09-28）

| 区域/D1 | 已点亮（提交≥3） | 未点亮 |
|---|---|---|
| **KOR** | analyst 6 / **fundamental 3** / model 4 / other 6 / pv 3 | shortinterest 0~1、earnings·imbalance·insiders·institutions·macro·news·socialmedia·sentiment·risk 全 0 |
| GLB | pv 5 / other 3 | 其余 0 |
| USA | model 4 / other 3 / earnings 2 | pv 1 / fundamental 1 / institutions 1 |
| IND | pv 9 / model 10 / analyst 7 / risk 5 / fundamental 3 / other 3 | 其余 0 |
| HKG | shortinterest 4 / pv 3 | 其余 0 |
| EUR | model 7 / pv 5 / other 2 / news 1 / risk 1 | fundamental 0 等 |
| DEU / GBR | model 6 / 7 | DEU shortinterest 2 |
| MEA | analyst 13 / fundamental 10 / model 4 / pv 3 | — |

### 0.4 分区投入产出（`backtest_results` 口径）

| 区域 | 生成 | 回测 | 回测/生成 | 达标 | 达标率 | max\|S\| | 判读 |
|---|---|---|---|---|---|---|---|
| JPN | 15,185 | 254 | 1.7% | **0** | 0% | 1.41 | ⛔ 1.5 万生成、零达标 |
| EUR | 12,752 | 569 | 4.5% | 27 | 4.7% | 2.09 | 生成侧严重过剩 |
| GLB | 8,315 | 2,144 | 25.8% | 161 | 7.5% | 4.65 | 有信号无提交（prod 墙） |
| USA | 9,504 | 1,003 | 10.6% | 39 | 3.9% | 2.42 | 标的问题 |
| GBR | 8,710 | 722 | 8.3% | 65 | 9.0% | 2.44 | — |
| IND | 2,749 | 782 | 28.4% | 231 | **29.5%** | 6.48 | 最强产出区 |
| DEU | 2,253 | 1,402 | 62.2% | 319 | **22.7%** | 2.17 | 转化率最高 |
| MEA | 657 | 498 | 75.8% | 99 | 19.9% | 2.38 | frozen 区存量 |
| KOR | 1,975 | 467 | 23.6% | 37 | 7.9% | 2.37 | 本次演练区 |
| ASI | 5,200 | 740 | — | 188 | 25.4% | 3.58 | — |
| CHN/HKG/AMR | 1,057 | 173 | — | 0 | 0% | CHN 4.96 | CHN 高 S 却 0 达标 |

### 0.5 六条判据

| 判据 | 含义 | 不通过的反例 |
|---|---|---|
| V1 可验证产物 | 产出可被下游消费的结构化产物（DB 表 / ledger / 文件包） | 只产人读文本 |
| V2 有真实调用方 | 有生产路径调用点 + 回归测试守护 | 零调用方、无测试 |
| V3 有实证收益 | 有前后对照的量化收益记录 | 仅口头声称 |
| V4 不可被合并 | 与其它步骤不重叠、不可归并 | 与另一闸同源重复拦截 |
| V5 成本合理 | 零配额/本地可算，或有明确配额回报 | 高配额换低产出 |
| **V6 出口吞吐匹配** | 产能是否匹配出口能力（REGULAR 4 + SUPER 1 + PPA 1 = 6 颗/日） | 生产 1,166 达标而出口仅消费 85 |

### 0.6 贯穿结论

1. **出口饥饿 vs 前段过剩（V6）**：生成 68,365 → 达标 1,166 → 提交 85；**1,101 条达标（94%）从未进 `submit_ready`**。前六步过量生产，后三步饥饿消费。
2. **瓶颈是分区的**：全区口径看是"S2 生成过剩"，但 **KOR 实测 `step_funnel` 显示掉得最狠的一跳是「回测完成 → 过廉价闸」，保留率仅 8.88%**。全区结论管资源分配，分区结论管战术。
3. **41 条临界金矿在贬值**：`submit_ready` 中 41 条 prod 落在 0.60–0.70（占已测 68%），SOP 铁律明写"该区间当天提交、不做变体"，但存量未被消费（mLm2xG1K：0.6997 隔日变 1.0000，整族封死）。
4. **点塔与活路错配（本次新发现）**：KOR profile 的活路是"分析师预期变化面"，但 **ANALYST 塔已点亮（6 颗）**；而点塔收益最大的 SHORTINTEREST 未被 profile 验证为活路。二者错配，需权衡。

---

## 1. 逐阶段展开（输入 / 处理 / 输出）

> `[09-28 新增]` = SKILL v2.3 本日落地内容。

### 步 1 · S-PRE 查表 + 库存盘点

| 项 | 内容 |
|---|---|
| **执行者** | 编排本体 + `mcp__wqb-db__get_campaign_summary / get_dead_ends / get_dead_datasets / get_mining_yield`；`tools/build_gate_prior_from_inventory.py`、`select_ra_basket.py` |
| **输入** | `$REGION`；`references/regions/<R>.md`（实测 **14 份**，含 AMR）；DB 四表存量；`reports/dataset_experience/*.md`；**平台 `get_pyramid_alphas` 塔状态**；PPA 公告（`get_messages` 实时重扫） |
| **处理** | ① profile 裁决（`entry_verdict`，MEA=`frozen` 步 1 即拒）；② **库存盘点优先**：枚举存量 → 资格门复算 → 写回 `gate_priors` → `select_ra_basket --target 20`（去参数网格 / OS 撞车预筛 / 篮内正交 / 平台复核）；③ 产出率双比率分离（`conversion` 低=管道问题、`yield_rate` 低=标的问题）；④ 跨区死路检查（不限 region 查 `registry_empirical`，现存 28 条 cross_region）；⑤ PPA 主题门禁（禁复用 settings 快照） |
| **输出** | universe / delay / 中性化 / 排除集 / 排除信号族 / 波号 + `gate_priors` 快照 + `cache/basket.json` |
| **失败分支** | registry 全空 = 新区域进步 2；库存足以覆盖目标塔则**不进**步 2 |

### 步 2 · S0 数据集体检 + 金字塔配置

| 项 | 内容 |
|---|---|
| **执行者** | `workflow_campaign(stage="S0")` + `tools/campaign_intel.py s0-select` + toolkit `score_datasets.py` |
| **输入** | 平台 `get_datasets` / **`get_pyramid_alphas` 实测点亮**；`region_kb` win 层；`saturated_datasets`；体检包（实测 **495 个**，非文档所记 320） |
| **处理** | ① 三方交叉（平台真实点塔 × 严格口径产出率 × 判死清单）；② **`lit=Y` 剔除**：已点亮塔所属数据集不得作主攻；③ **两步必需**：`calibrate`（只写 thresholds、不产排名）→ 裸 `stage="S0"`（产 `s0_ranking`）；④ 座位可达性（Σ`est_seats` < target → WARN 结构性不可达）；⑤ 锁白名单（≥2 非 MODEL、`category_weight` 0.9–1.15）；⑥ 饱和路由；⑦ `[09-28]` 体检包硬前置（`--inspect-mode enforce`，缺包整波拦截） |
| **输出** | `s0_ranking` / `s0_whitelist` / `s0_calibrate_<region>` / `*_dead` |
| **失败分支** | 配额后无非 MODEL → 写 findings；全硬排除 → 回步 1 换区 |

### 步 3 · S1 字段扫描 + `[09-28]` 闸 SEM 语义归类

| 项 | 内容 |
|---|---|
| **执行者** | `workflow_campaign(stage="S1")` + L1 三件套 + **`tools/field_semantic_classify.py`（新增，10KB）** |
| **输入** | 白名单数据集 + `get_datafields`（`fields` 268,714 行 / `field_profile` 30,705 行） |
| **处理** | ① typed catalog 落地 `fields` + ledger `s1_<ds>_d<delay>`；② 字段级覆盖审计（防空集）；③ 幽灵字段验活（`validate_fields=true`，避免提交层 COMPILE_ERROR）；④ `users` 分级（≥50 只验方向 / 10–49 进池必实测 prod / 0–9 优先，冷门占批 ≥50%）；⑤ `[09-28]` **语义归类**：产出 `s1_semantic_<ds>`（signal / blocked / by_category），黑名单 = 货币码 / 汇率叉乘 / 标识符 / 分类码 / 标志位 / 期间口径 / 股份类别 |
| **输出** | typed catalog + `s1_semantic_<ds>` + **`s2_field_pool_<ds>`**（GEM 字段池） |
| **失败分支** | 字段 <10 退回步 2；**缺 `s1_semantic_<ds>` → 步 5 `wave_gate` exit 2 整波阻断**（fail-closed，回归 `tests/unit/test_semantic_gate_failclosed.py`） |

> **V3 实证**：KOR/fundamental17 首波 348 条产物中 **49.4%** 落在非信号字段（货币码比较、三角套汇恒等式），语法全对、语义全废，语法闸与 `gate.py` 都拦不住，只能靠回测烧配额；黑名单字段仅占 9.9% 却吃掉 49.4% 生成预算。

### 步 4 · S2 概念优先生成（GEM） + `[09-28]` 形状配额

| 项 | 内容 |
|---|---|
| **执行者** | `workflow_gem` → `brain-make-some-gem/scripts/headless_runner/run.py`；预闸 `pipeline_pregate`；**`tools/shape_quota_check.py`（新增，5.6KB）** |
| **输入** | priors 快照（`assemble-priors`，DB 为单一事实源）+ `s2_field_pool_<ds>` + settings + ideas（仅 LLM/人工 source 才注入） |
| **处理** | ① priors 组装（只消费 `wins`≤6 / `dead_ends`≤12 + sha256 快照）；② gate_priors 分流（`by_operator_count`/`by_field_family` 进 prompt；`by_decay`/`by_neutralization` 由步 6 改写设置）；③ LLM 概念生成（机制 → 1–2 字段 id → 例）；④ 预闸（quantile 归一 / 毒模式丢弃 / hump 命名参数 / bucket range / 非标窗口归一 / 同骨架封顶 12）；⑤ `[09-28]` **形状配额**：每波 ≥3 个 shape family，`trade_when` 占比 ≤40%（对策：wave84/85 实测 19 条仅 ~9 个算子形状、trade_when 占 62%，而已验证算子 103 个、KB 模板 141 条零调用）；⑥ 契约波 vs 探索波分跑 |
| **输出** | `expressions` status=gem/enhanced（全库 17,041 条处此状态） |
| **失败分支** | GEM 未入库按超时清单查；402 余额不足退 ideas 旁路；机制枯竭 → `forum_recon` 回补 KB |

### 步 5 · S2→S3 门禁（含 5b prod-first、`[09-28]` 闸5 等权拦截）

| 项 | 内容 |
|---|---|
| **执行者** | `tools/wave_gate.py` + toolkit `gate.py:check_batch_diversity` + `field_inspect_gate.py` + `campaign_intel ghost-audit / prod-first` |
| **输入** | 本波 `expressions`（`--from-db`）+ typed catalog + 体检包 + `platform_constraints.json`（**v1.5，已确认含 `equal_weight_leg_add`**）+ `explore_contract` + `alphas` prod 记录 |
| **处理** | ① 幽灵算子硬闸（零配额，防整批 CANCELLED 连坐）；② 闸 1–8（语法/白名单/VECTOR 类型/不可访问算子/**毒模式**/批级多样性/longCount/EVENT）；③ 闸 SEM；④ **闸 PF**（骨架级 prod 死路，fail-closed）；⑤ `[09-28]` **毒模式 `equal_weight_leg_add`**：拦截 `add(rank(A),rank(B))`、`add(group_rank(A,g),group_rank(B,g))` 等等权相加；⑥ 体检硬门 5 条；⑦ 5b prod-first 探针 |
| **输出** | `gate_results`（`all_pass` / `fail_reasons`）+ `prod_first_<wave>` |
| **失败分支** | 语法 FAIL 必修；多样性 FAIL 回步 4 补骨架（软触发：结构熵 <1.5 即补，不等硬 FAIL） |

> **`[09-28]` 事故与修复**：旧文档称「`0.5*rank(A)+0.5*rank(B)` 被闸5 block」，但实现层是假的——
> `_detect_weighted_mix_structural` 只拦「实参以 `系数*` 开头」的腿，**明文豁免等权**。
> KOR wave189/190 因此漏过 7 条 `add(group_rank(腿A), group_rank(腿B))`（含 S=2.11 / F=1.80 / 2Y=1.89），已全部作废。
> 现由 `tests/unit/test_gate_equal_weight_leg_add.py`（16 条：7 违规必拦 / 7 合规必放 / config 断言 / DB 作废断言）守护。

### 步 6 · S3 七槽回测

| 项 | 内容 |
|---|---|
| **执行者** | `workflow_batch_track` / toolkit `pipeline.py run`（并发唯一来源 `wqb-concurrency` §8） |
| **输入** | 过闸批次 + `settings.json` + `region_kb.gate_priors` |
| **处理** | ① settings prior 改写（样本 ≥30 且过闸率 ≥ 当前 ×2 才改；显式 `--set` 钉住不动）；② 七槽填槽（Token-Bucket C≈7；multi(8) 86.1 α/hr vs single 54.3，1.59×）；③ 连坐隔离（定位坏式 → 回写 fail → 无辜式重发批优先下槽）；④ 槽位仲裁（`WQB_GLOBAL_SLOTS=7`）；⑤ 收批压缩（18 次调用 → 2 次）；⑥ QUICK/FULL 模式（QUICK 不可提交） |
| **输出** | `backtest_results`（全库 8,754）+ `wave_results` + ckpt + `expressions.status=backtested` |
| **失败分支** | 故障协议表（8 子全 ERROR 重发 / fatal 算子隔离 / 429 退避 / took-too-much-resource 去 backfill） |

### 步 7 · S4 诊断改进 + `[09-28]` 四道提交闸 / SUB 比例律

| 项 | 内容 |
|---|---|
| **执行者** | `review_wave.py` + `campaign_intel s4-prescreen / prod-first` + `wq-brain-alpha-optimization-v1` + `tools/forum_recon.py` |
| **输入** | 本波 `backtest_results` alpha_id + `thresholds.review` + OS 衰减基线 + `salvage_pool` |
| **处理** | ① s4-prescreen 分层（REJECT 直接判死，≈8× 效率）；② walls 诊断（`RN_EXPOSURE`：risk_neutralized ≤0 且 sharpe≥1.58 ⇒ 就是那个暴露本身 → dead_end 禁调参；`ROBUST_STRUCTURAL` 拒入 near）；③ prod-first 探针；④ OS 衰减校准（expOS = IS×0.358，**仅参考不作排序**）；⑤ `[09-28]` **四道提交闸 + SUB 比例律**：`LOW_SHARPE ≥1.58` / `LOW_FITNESS ≥1.0` / `LOW_2Y_SHARPE ≥1.58` / `LOW_SUB_UNIVERSE_SHARPE ≈ 0.571 × 本 alpha sharpe`（三处独立实证：1.03/1.80、1.12/1.96、0.89/1.55）；破比值闸旋钮 = 换分组轴 `market`/`exchange`、`signed_power` 压尾、长窗平滑；⑥ `[09-28]` 卡闸找武器（Mode B 2–3 轮仍卡墙 → `forum_recon --out ledger`，每波 ≤1 次） |
| **输出** | `s4_walls_<region>_<wave>` + `salvage_pool` + review payload + 换概念/换腿决策 |
| **失败分支** | prod ≥0.7 → Mode B 换概念；同想法 >10 结构不过 → 步 9 记 dead_end 回步 2 |

### 步 8 · S4→S5 稳健闸 + 提交判定

| 项 | 内容 |
|---|---|
| **执行者** | `brain-alpha-robustness`（必经）+ `mcp__wq-brain-http__submit_verdict` + `worldquant-submit-alpha` / `wq-brain-superalpha` |
| **输入** | 达标候选 + `is.checks` 全量 + WebDataScope failed-counts |
| **处理** | ① Failed-count 资格门（RA 要求 `Failed RA == 0`，比只看 `result=="FAIL"` 严格）；② `submit_verdict` 零成本判定（`degraded_gates` 非空 ⇒ 不可作依据）；③ **prod 0.60–0.70 当天提交、不先做变体**；④ 报告 SUBMITTABLE → **等用户确认**；⑤ POST 四形态处置（200 通过 / 201 异步 4min 未翻 → re-POST / 200 空体必须补发 / 403 零成本带回全量 checks）；⑥ `[09-28]` 补发已工具化（节点 Step 4 内置四态处置） |
| **输出** | `submit_ready`（107）+ `submission_ledger`（85）+ ACTIVE alpha |
| **失败分支** | PROD/SELF 不过回步 7；配额耗尽挂起，继续步 2→9 |

### 步 9 · S6 复盘回写

| 项 | 内容 |
|---|---|
| **执行者** | `tools/step_funnel.py` + `upsert_wave_result / upsert_registry_empirical` + `campaign_intel pyramid` + `dataset-experience` + `seal_dead_end` |
| **输入** | 本波四表存量 + ledger + 平台塔状态 |
| **处理** | ① `step_funnel` 只读定位瓶颈（不凭印象写 verdict）；② verdict **强制枚举**（PASS/PARTIAL/FAIL）；③ 判死封存（先 `seal_dead_end` 沉降入 salvage_pool，再记 dead_end；`[09-28]` 判死前先 `forum_recon --out negative` 取证，found=true 不得判死）；④ `region_kb` 刷新；⑤ pyramid 点塔进度进 key_findings；⑥ `dataset-experience` 沉淀；⑦ `[09-28]` `s6_verdict_<wave>` 已废弃去重（唯一真相源 = `wave_results.verdict`）；⑧ **S6 完成定义**：三件回写后必须再跑 `assemble-priors` 刷新快照 |
| **输出** | `wave_results.verdict`（965）+ `registry_empirical`（1,030）+ `reports/dataset_experience/*.md` |
| **失败分支** | 停止闸 B1/B2 机械判定（同轴 3 连可计数 FAIL 熔断 / 窗口内 ≥4 轴全 FAIL 停区） |

---

## 2. 价值评估

### 2.1 汇总判定

| 步 | 判定 | 最强判据 | 保留深化项 | 精简/去除项 |
|---|---|---|---|---|
| 1 S-PRE | **★★★ 保留深化** | **V3**：09-07 实证 170 次新回测 0 产出 vs 一次库存扫描 20 条；**V5** 零配额 | 跨区死路检查（治 KOR risk70 跨三区死族 114 条白跑）；**库存结论必须强制消费**（41 条临界金矿） | PPA 主题扫描对纯 RA 波是固定开销，但便宜，保留 |
| 2 S0 | **★★★ 保留深化** | **V3**：已点亮塔剔除一次砍掉 KOR 71% 候选（142/200）；**V1** 体检包 495 个已落地且硬前置 | `lit=Y` 剔除 + 体检包 enforce + 座位可达性 | `calibrate --dry-run` 仅新区需要，日常可跳 |
| 3 S1 + SEM | **★★★ 保留深化（本日最高价值新增）** | **V3**：49.4% 生成预算曾被非信号字段吃掉；**V1/V2** 有 CLI + 回归测试 + fail-closed | 语义归类（黑名单 → 字段池 → GEM 注入，闭环完整） | `feature_engineering` 作"字段理解"**已收口**（确定性模板渲染、禁入 GEM） |
| 4 S2 + 形状配额 | **★★ 保留但需限流** | **V1**：68,365 条 expressions 的唯一来源；形状配额治同质化（trade_when 62% → ≤40%） | 概念优先 + priors 分流 + 预闸 | **V6 不通过**：KOR unconsumed 545（27.6%）、JPN 15,185 生成 0 达标 → **须按 S3 实测吞吐设生成准入配额** |
| 5 门禁 + 闸5 | **★★★ 保留（精简展示层）** | **V2/V3**：闸5 等权事故修复 + 16 条回归守护；**V5** 纯本地零配额 | 闸 SEM / 闸 PF / 幽灵算子硬闸（防连坐） | `validator.check_batch` **deprecated**（零调用方、判据不同）；`[opcat]` 质量预估只打印不判定 → 噪声 |
| 6 S3 | **★★★ 保留** | **V5**：七槽 86.1 α/hr（vs 54.3，1.59×）；**V3**：连坐隔离（JPN 一条 `bucket()` 缺 range 丢 64 条） | settings prior 直接改设置（治 decay 语义错配） | `batch_track` 入口不跑三闸（§2.3 D4） |
| 7 S4 + SUB 比例律 | **★★★ 保留并加强** | **V3**：KOR 实测瓶颈正在这一跳（保留率 **8.88%**）；SUB 比值律是**可计算**的破墙钥匙 | forum_recon 卡闸找武器、换分组轴 `market`/`exchange`、s4-prescreen | **Mode A 参数层压缩**（实证仍撞 prod 0.84–0.85）；`RN_EXPOSURE` 行仍进 near/salvage → 应一并排除 |
| 8 提交判定 | **★★★ 保留并扩权（全链 ROI 最高）** | **V1**：85 颗提交唯一路径；**V3**：四形态补发闭环（3 颗曾悬空 >24h）；**V6**：出口是唯一稀缺资源 | **立即消费 41 条临界 + 47 条未测 prod** | `config.py::compute_webdata_failed_counts` 第三份相反实现（§2.3 D5） |
| 9 S6 | **★★★ 保留** | **V4**：唯一让九步成环（region_kb 自动刷新）；verdict 枚举保证停止闸真实 | `step_funnel` 只读定位；`seal_dead_end` 沉降；forum_recon negative 取证 | 五张 `step_*` 表文档残留（DB 实测不存在）；**327 波无 verdict** |

### 2.2 建议去除 / 精简明细

| 项 | 处置 | 判据 |
|---|---|---|
| `wqb.expression.validator.check_batch` | **标注 deprecated** | V2：全仓零生产调用方；只实现 4 条形状闸且判据与执行口径不同 → 双口径误读 |
| 五张 `step_*` / `*_summary` 表引用 | **清理文档残留** | DB 实测不存在（19 表清单已核） |
| `[opcat]` / 质量预估的 "FAIL" 打印 | **降级为 INFO** | V1：自称硬闸却不进 `all_pass` → 纯噪声 |
| 步 3 `feature_engineering` 注入 GEM | **保持禁用** | V1/V3 双不通过（GBR 实证：注入后 GEM 零 LLM 调用，整波退化为模板展开） |
| **JPN / EUR 继续投料** | **暂停**（V6） | JPN 15,185 生成 / 0 达标 / max\|S\| 1.41；EUR 12,752 / 27 达标 → 边际产出≈0 |
| `brain-alpha-repair`（43 行配方查表） | **并入 optimization-v1** | V4：与其它改进入口重叠 |
| Mode A 参数层扫描 | **压缩至 ≤30% 精力** | V3：实证仍撞 prod 0.84–0.85，参数层破不了结构性墙 |
| `structural_variant_results` 表 | **归档** | DB 实测 **0 行**；文档已记"仅 1 行产出、降为实验性" |

### 2.3 保留深化的优先序

| 序 | 动作 | 依据 |
|---|---|---|
| 1 | **消费存量**：`submit_ready` 中 41 条 prod 0.60–0.70 + 14 条干净，另加达标池中 **74 条已测 prod<0.7** | V6 + V3；按 6 颗/日需 ~15 天，且每拖一天都在贬值 |
| 2 | **修 `expressions.status` 回写**（D9） | 已造成真实误杀（AMR 积压闸 conversion 恒 0），且污染一切 status 口径统计 |
| 3 | **SOP 写点亮判定纪律**（D1a） | 成本≈0；已因此算错过一次结论 |
| 4 | **步 7 破墙自动化**：回测后**立即**自动核验 SUB 比值律，而非人工事后诊断 | KOR 瓶颈在这一跳（8.88%）。注意 SUB 依赖 sharpe，**只能"回测后立即核验"，不能前移到门禁** |
| 5 | **步 4 生成准入配额**：按 S3 实测吞吐反推生成量，JPN/EUR 直接停 | V6 |

### 2.4 缺口清单

> 本表经**实测校正**（2026-09-28 23:30）：D5 已闭环、D2 建议撤回、D3 含金量下调、新增 D9。

| # | 缺口 | 证据 | 价值 | 处置 |
|---|---|---|---|---|
| **D9**<br>（新增·最高） | **`expressions.status` 不回写** | 回测完成后 status 仍滞留 gem/pending；今日 AMR 实证：积压闸因 conversion 分子恒 0 **误杀后续波**，手动回写 40 条后 conversion 才从 0/212 → 18.9%。同一原因使 GLB 的 status 口径回测=0（`backtest_results` 实为 2,144） | **高**（已造成真实误杀；且污染一切 status 口径统计） | **做**：波裁决后强制回写 status |
| **D1a** | 点亮/塔归属用本地表推导 | `date_submitted` 全库仅 **2.7%** 非空；塔归属 ≠ `datasets.category`。本报告曾据此算出错误结论 | **高（防错）**，成本≈0 | **做**：SOP 写一句纪律（一律查平台 `get_pyramid_alphas`） |
| **D1b** | `_unknown` 占位数据集 422 条 | KOR 47% ACTIVE 的 category=None | **低**（修了也不能用于点亮判定） | **不做** |
| **D2** | 门禁表达式级通过率 95.1% | KOR 351/369 放行 | **低** → **原"SUB 前移"建议撤回** | **不做**。理由：SUB 比值律 = `0.571 × 本 alpha sharpe`，**依赖回测后的 sharpe，无法在门禁阶段本地判定**；且门禁职责就是零成本拦硬错误（幽灵算子/毒模式/语法），95% 通过率是其正常定位，强行加严会误杀好候选 |
| **D3** | 达标池沉没 | 1,166 达标 / 1,101 未进 `submit_ready`。**但实测含金量远低于表面**：达标中 prod 已知仅 **367**，其中 **prod<0.7 仅 74 条** | **中**（非"1,101 条金矿"） | **限定做**：消费 74 条已测 prod<0.7 + `submit_ready` 现有 55 条。**不做全量 1,101 条**——测 prod 需 45s~12min/条，全测不可行 |
| **D4** | 327 波无 verdict | waves 1,292 vs wave_results 965 | **低**（历史波补写不产 alpha） | **改为**：只保证**未来波**都写 verdict，历史 327 条不补 |
| **D5** | ~~双份 Failed-count 口径相反~~ | **已于 2026-09-27 R3 审计修复**：`config.py` 注释 364–369 记录，"现 mcp_core.py 与 build_gate_prior_from_inventory.py 都引用这里"，一致性由 `tests/unit/test_r3_failed_count_single_source.py` 断言 | **零（已闭环）** | **从清单移除**（本报告前版列其为"未修"是错的） |
| **D6** | `batch_track` 入口不跑三闸 | SOP 指定它作步 6 入口，但三闸只有 `campaign(S3)` 跑 | **中低**（且积压闸有误杀前科，见 D9） | **延后**：先修 D9（status 回写），再考虑三闸下沉 |
| **D7** | 点塔与活路错配 | KOR profile 活路 = 分析师预期变化面，但 ANALYST 已点亮（6）；点塔收益最大的 SHORTINTEREST 未被 profile 验证 | **高（决策）** | **不是修复，需你拍板** |
| **D8** | 文档数字过期 | 体检包 320→495、profile 13→14 | **低**（cosmetic） | 顺手改（2 分钟） |

---

## 3. 全流程模拟演练（不实际修改）

### 3.1 演练设定与诚实声明

- **输入域**：`REGION=KOR`、`DS=shortinterest38`、`DELAY=1`、`UNIVERSE=TOP600`、`WAVE=s2_si38_d1_w192`（**虚构波号，仅用于推演**）
- **选集理由（真实数据）**：KOR 唯一同时满足「塔未点亮 + 已有体检包 + 非跨区死路」的数据集（推导见步 2）
- **演练性质**：**推演层（dry-walkthrough）** —— 每步输入取自**当前真实库/平台只读快照**，处理按 SOP 逐条走，输出为**推演增量**（不落库）。
  与代码层 `executor(dry_run=True)` 演练互补：代码层验证"命令能否构建"，推演层验证"数据走到这一步会发生什么"。
- **零副作用**：未写库、未发平台请求（除 `get_pyramid_alphas` 只读查询）、未创建/修改任何业务文件。
- **标注**：`[真实]` = 实测；`[推演]` = 按 SOP 推定。

### 3.2 逐步推演

---

#### 步 1 · S-PRE 查表 + 库存盘点

| | 内容 |
|---|---|
| **输入** | `$REGION=KOR`；profile `KOR.md`：`universe=[TOP600]`、`delay=[1]`、`neutralization_default=STATISTICAL`、禁止 delay0；死路=图表形态 3 连死 / 新闻情绪 3 连死 / AI-ML 3 连死 / 信用风险双死 / GLB emotion 跨区铁律；CW>0.5 是事件类通病 **[真实]**。<br>DB 存量：KOR expressions 1,975 / backtest 467 / 达标 37 / `submit_ready` 17 / wave_results FAIL54·PARTIAL23·PASS7 **[真实]**。<br>平台塔状态：analyst 6 / fundamental 3 / model 4 / other 6 / pv 3 已点亮；shortinterest 0~1 未点亮 **[真实]** |
| **处理** | ① profile 裁决 → active 放行；② **库存盘点** → 17 条 `submit_ready` 待消费；③ 跨区死路检查 → `risk70` 跨三区死族已记（114 条白跑），RISK 塔排除；④ PPA 主题重扫（当期 All regions / D1 / Oct`26 要求**单数据集 + PV 或 fundamental**）→ shortinterest38 不属主题范围 → **走 RA 路径，不进 PPA 分支** |
| **输出** | universe=TOP600 / delay=1 / nu=STATISTICAL / 排除集={图表形态, 新闻情绪, AI-ML, 信用风险, RISK} / 波号 w192；`gate_priors` 刷新 **[推演]** |
| **价值判定** | **★★★ 通过 V3+V5**（零配额）。**本次触发分叉**：`submit_ready` 已有 17 条 KOR 存量，应先消费 |
| **演练决策** | ✅ **本步有价值，且应强制"库存未清空不进步 2"** → 演练在末尾回到步 8 消费存量 |

---

#### 步 2 · S0 数据集体检 + 金字塔配置

| | 内容 |
|---|---|
| **输入** | KOR 200 个数据集按 category：MODEL 62 / OTHER 27 / NEWS 24 / PV 18 / FUNDAMENTAL 18 / ANALYST 17 / RISK 7 / SENTIMENT 6 / SHORTINTEREST 3 / SOCIALMEDIA 2 / MACRO 2 / INSTITUTIONS 2 / INSIDERS 2 / EARNINGS 1 / IMBALANCE 1 / None 8 **[真实]**；平台点亮 **[真实]**；KOR 体检包 8 个：analyst25 / fundamental17 / model56 / other106 / other395 / other466 / risk70 / **shortinterest38** **[真实]** |
| **处理** | ① **`lit=Y` 剔除**：已亮塔所属集 ANALYST 17 + FUNDAMENTAL 18 + MODEL 62 + OTHER 27 + PV 18 = **142 个（71%）剔除**；② 剩余候选按覆盖/拥挤排序：SHORTINTEREST 3（均 cov **0.973** / alphaCnt 1019）、INSTITUTIONS 2（0.904）、RISK 7（0.888）、IMBALANCE 1（0.856）、INSIDERS 2（0.622 但 alphaCnt 2268 拥挤）、MACRO 2、SOCIALMEDIA 2（cov 1.0）、NEWS 24（cov 0.497）、SENTIMENT 6（0.499）、EARNINGS 1（alphaCnt 2304 拥挤）；③ 排除 profile 死路（新闻情绪 / AI-ML）与跨区死族（RISK/risk70）；④ **体检包硬前置**（`--inspect-mode enforce`）：未亮塔中有体检包的仅 `shortinterest38` 与 `risk70`，后者已排除；⑤ `calibrate` → 裸 S0 打分；⑥ 座位可达性（TOP600 小宇宙 × 88 字段） |
| **输出** | `s0_whitelist` = **[`shortinterest38`（88 字段 / cov **0.995** / alphaCnt 1758 / pyramid_multiplier 1.4 / 塔未点亮）]** **[推演，依据真实数据]** |
| **价值判定** | **★★★ 保留深化（V3+V1）**：一次剔除 71% 候选（142/200），把搜索空间压到真实可点亮的塔；体检包硬前置避免"硬门空转"。<br>**演练同时暴露 D7（点塔与活路错配）**：profile 的活路是 ANALYST，但 ANALYST 已点亮（6）→ 按选塔优先律应**转组腿池不占 REGULAR 名额**；而点塔收益最大的 SHORTINTEREST 未被 profile 验证为活路 |
| **演练决策** | ✅ **锁定 shortinterest38**。代价提示：该集 alphaCnt 1758 属**热门**（users 分级高），步 3 需**必测 prod**，与"冷门优先"策略相反 → 潜在 prod 墙风险 |

---

#### 步 3 · S1 字段扫描 + 闸 SEM

| | 内容 |
|---|---|
| **输入** | `get_datafields(KOR, shortinterest38, delay=1)` → 88 字段；体检包 `field_inspect_kor_shortinterest38.json` **已存在** ✅ **[真实]** |
| **处理** | ① typed catalog → ledger `s1_shortinterest38_d1`；② 覆盖审计（cov 0.995 → 无需 backfill 强制，但需确认字段级而非集级）；③ 幽灵字段验活（防提交层 COMPILE_ERROR）；④ `users` 分级：alphaCnt 1758 → **热门集**，进池**必实测 prod**；⑤ `[09-28]` `field_semantic_classify.py --region KOR --dataset shortinterest38 --write-ledger` |
| **输出** | `s1_semantic_shortinterest38`（signal / blocked / by_category）+ `s2_field_pool_shortinterest38` **[推演]** |
| **价值判定** | **★★★ 本日最高价值新增（V1+V2+V3+V5）**：KOR 同类集实证 49.4% 预算曾被非信号字段吃掉；有 CLI、有回归测试、fail-closed（缺台账 exit 2） |
| **演练决策** | ✅ **保留深化**。⚠️ 本次演练唯一同时满足四条判据的新增项 |

---

#### 步 4 · S2 GEM + 形状配额

| | 内容 |
|---|---|
| **输入** | priors 快照（`assemble-priors`）；`s2_field_pool_shortinterest38`；settings；KOR `unconsumed = 545`（gem317 + pending143 + gated58 + selected27）**[真实]**；profile 死路（避图表/新闻/AI-ML 概念） |
| **处理** | ① GEM 概念优先（机制 → 字段 → 例）；② 预闸（quantile 归一 / 毒模式丢弃 / hump / bucket range / 非标窗 / 同骨架封顶 12）；③ `[09-28]` `shape_quota_check.py`：≥3 shape family、`trade_when` ≤40% |
| **输出** | 本波新增 ~8–20 条 expressions（status=gem）；KOR unconsumed 545 → ~560 **[推演]** |
| **价值判定** | **★★ V6 不通过（产能过剩）**：KOR 已积压 545 条未消化（27.6%）。<br>但**形状配额本身 V3 通过**（治 wave84/85 的 9 形状 / trade_when 62% 同质化） |
| **演练决策** | ⚠️ **条件放行**：仅在 `unconsumed < S3 近 7 日实测吞吐 × 2` 时生成。<br>**JPN / EUR 在此应直接停**（15,185→0 达标 / 12,752→27 达标） |

---

#### 步 5 · S2→S3 门禁

| | 内容 |
|---|---|
| **输入** | 本波表达式（含一条**故意违规**样本：`add(group_rank(ts_mean(f1,22), market), group_rank(ts_mean(f2,66), market))`）**[推演]**；体检包 ✅；`platform_constraints.json` **v1.5** **[真实]** |
| **处理** | ① `ghost-audit`（幽灵算子，零配额）；② `wave_gate.py`：闸 1–8 + 闸 SEM + 闸 PF + **闸5 `equal_weight_leg_add`** + 体检硬门 5 条 |
| **输出** | 违规样本 → **被闸5 拦截并剔出候选**（不进回测）**[推演，依据：回归测试 7 违规必拦]**；`gate_results` +1 |
| **价值判定** | **★★★ V2+V3+V5**：等权漏洞已由 16 条回归守护；纯本地零配额。<br>**暴露 D2**：KOR 表达式级通过率 **95.1%** —— 门禁几乎不拦，过滤力在回测后 |
| **演练决策** | ✅ **保留**；建议把 SUB 比值律等可本地判定的判据**前移**到本步（省配额） |

---

#### 步 6 · S3 七槽回测

| | 内容 |
|---|---|
| **输入** | 过闸 ~8 条；settings（decay / nu=STATISTICAL / TOP600 / delay1） |
| **处理** | ① settings prior 改写（样本 ≥30 且过闸率 ≥ 当前 ×2 才改）；② 七槽并发（86.1 α/hr）；③ 连坐隔离；④ 收批压缩；⑤ ⚠️ **KOR profile 提示：小宇宙放大 CW 与 longCount 问题，事件类 CW>0.5 是通病** |
| **输出** | `backtest_results` +8；KOR 467 → 475；`expressions.status=backtested` **[推演]** |
| **价值判定** | **★★★ V5**：吞吐是真实杠杆；⚠️ `batch_track` 入口不跑三闸（D6） |
| **演练决策** | ✅ **保留**；补三闸下沉 |

---

#### 步 7 · S4 诊断改进

| | 内容 |
|---|---|
| **输入** | 8 条回测（假设最佳：S=1.72 / F=1.15 / 2Y=1.41 / SUB=0.98 / prod 未测）**[推演]** |
| **处理** | ① `s4-prescreen` 分层；② walls：`RN_EXPOSURE`（risk_neutralized ≤0？）/ `ROBUST_STRUCTURAL`；③ prod-first 探针（热门集必测）；④ `[09-28]` **SUB 比例律**核验：SUB/S = 0.98/1.72 = **0.570 < 0.571** → **差 0.001 卡闸**；2Y = 1.41 < 1.58 → **也卡** |
| **输出** | 判据 `SUB/S ≥0.571 ∧ 2Y ≥1.58 ∧ S ≥1.58 ∧ F ≥1.0` → 本条 **SUB 与 2Y 双卡** → 进 near 池，转 Mode B **[推演]** |
| **价值判定** | **★★★ 保留并加强**：**KOR 实测瓶颈正在这一跳（保留率 8.88%）**，SUB 比值律给了**可计算**的钥匙。<br>破墙旋钮：换分组轴 `market`（KOR 实证把比值 0.55 → **0.59**，决定性）；`exchange` 给 2Y |
| **演练决策** | ✅ **加强** → 下一步做 `group_rank(R, market)` 变体（**单信号结构，合规**），**不是**加权混合（禁混信号铁律） |

---

#### 步 8 · 提交判定（演练在此消费存量）

| | 内容 |
|---|---|
| **输入** | 存量：`submit_ready` 107 条中 **41 条 prod 0.60–0.70 临界 + 47 条未测** **[真实]**；本波 near 候选（暂不达标） |
| **处理** | ① Failed-count 资格门（RA 要求 `Failed RA == 0`）；② `submit_verdict`；③ **按铁律：prod 0.60–0.70 当天提交、不做变体**；④ 用户确认；⑤ POST 四形态处置（403 零成本带回真实 PROD/SELF） |
| **输出** | 按 6 颗/日（REGULAR 4 + SUPER 1 + PPA 1）消费；本日推演**提交 4 颗 REGULAR**（从 41 条临界中按 IS 强度降序取 4）**[推演]** |
| **价值判定** | **★★★ 全链 ROI 最高（V1+V3+V6）**：出口是唯一稀缺资源；41 条临界金矿**每拖一天都在贬值** |
| **演练决策** | ✅ **扩权**：把"达标 → `submit_ready`"自动化（治 1,101 条沉没），临界区候选**前置**于任何新挖 |

---

#### 步 9 · S6 复盘回写

| | 内容 |
|---|---|
| **输入** | `step_funnel --region KOR` 实测 **[真实：瓶颈 = 回测→过闸，保留率 8.88%]**；KOR wave_results FAIL54/PARTIAL23/PASS7 **[真实]** |
| **处理** | ① `step_funnel` 定位（不凭印象写 verdict）；② verdict 枚举：本波 0 达标 + ≥1 near → **PARTIAL**；③ `seal_dead_end` 前先 `forum_recon --out negative` 取证；④ `region_kb` 刷新 + `pyramid` 点塔进度（shortinterest 塔 0→1 进度）；⑤ `dataset-experience` 沉淀；⑥ **重跑 `assemble-priors`** 刷新快照（S6 完成定义） |
| **输出** | `wave_results.verdict=PARTIAL` +1；`registry_empirical` near/dead 更新；`reports/dataset_experience/kor_shortinterest38_campain.md` **[推演]** |
| **价值判定** | **★★★ V4**：唯一让九步成环。⚠️ **D4**：全区 327 波无 verdict → 停止闸 B1/B2 窗口失真 |
| **演练决策** | ✅ **保留**；补写 327 波 verdict |

---

### 3.3 演练净变化

| 指标 | 演练前（真实） | 演练后（推演） | 说明 |
|---|---|---|---|
| KOR expressions | 1,975 | ~1,985 | +10（受生成准入配额约束） |
| KOR backtest_results | 467 | 475 | +8 |
| KOR wave_results | FAIL54/PARTIAL23/PASS7 | PARTIAL +1 | 本波 0 达标 + 有 near |
| KOR submit_ready | 17 | 17（消费 4 颗 REGULAR 存量） | **存量被消费，而非新增积压** |
| 全局 submitted | 31 | 推演 +4 | 出口侧是真实增量 |
| 拦下的违规 | — | 1 条等权 `add(group_rank,group_rank)` | 闸5 生效 |
| shortinterest 塔进度 | 0~1 | 推演不变（本波未达标） | 需后续波继续 |

### 3.4 演练结论（四个可执行）

1. **演练在步 1 就该分叉**：KOR 有 17 条 `submit_ready`、全局 41 条临界金矿，
   **正确动作是先转步 8 消费，而不是走完九步再挖新的**。当前 SOP 没有强制这个分叉。
2. **步 2 的选集被真实数据锁定为 `shortinterest38`**：KOR 200 个数据集剔除 71%（已亮塔）后，
   唯一同时满足「未点亮 + 有体检包 + 非跨区死路」的只剩它（88 字段 / cov 0.995 / mult 1.4）。
   **代价**：它是热门集（alphaCnt 1758），必测 prod，与"冷门优先"相反 → 有 prod 墙风险。
3. **真卡点在步 7 而非步 4**：不是"没生成"，而是 SUB/S = 0.570 **差 0.001** 卡在 0.571 比值闸、2Y 1.41 卡 1.58。
   破法 = 换分组轴 `market`（KOR 实证 0.55→0.59）。
4. **点塔与活路错配（D7）需权衡**：KOR profile 的活路 ANALYST 已点亮（6 颗，应转组腿池）；
   **建议下一波看点塔收益优先（SHORTINTEREST），再用 profile 死路做减法**。

### 3.5 演练无法覆盖的环节（诚实声明）

1. **LLM 可达性**：GEM 依赖 LLM，余额不足表现为误导性的 `no meta.json within 90s`；干跑验证不了，会显示假绿。
2. **真实 POST submit**：提交类必须用户显式确认，本次仅推演四形态处置。
3. **prod 实测值**：41 条临界的 prod 随时间变化（mLm2xG1K：0.6997 → 1.0000），推演值是当前快照。
4. **`get_pyramid_alphas` 的季度边界**：传 `start_date` 会被对齐到季度快照，近 90 天判定需用默认季度值。
5. **本次为推演层**：输出增量按 SOP 推定，非真实执行结果；真实执行以代码层 `executor(dry_run=True)` 为准。

---

## 4. 审阅清单

| # | 事项 | 我的建议 | 决策 |
|---|---|---|---|
| 1 | 九步判定：步 1/2/3/5/6/7/8/9 = ★★★，步 4 = ★★（需限流） | 认可则无需动作 | ☐ |
| 2 | **消费存量**：41 条临界 + 14 条干净 + 达标池 **74 条已测 prod<0.7**（**不做**全量 1,101 条） | 立即做，先于任何新挖 | ☐ |
| 3 | **SOP 明写：点亮/塔归属一律查平台 `get_pyramid_alphas`**（D1a） | 做（成本≈0，已因此算错过结论） | ☐ |
| 4 | **修 `expressions.status` 回写**（D9，新增·最高优先） | 做（已造成 AMR 积压闸误杀） | ☐ |
| 5 | 步 4 按 S3 实测吞吐设生成准入配额；**JPN / EUR 直接停生成** | 做（V6） | ☐ |
| 6 | 步 7：回测后**立即**自动核验 SUB 比值律（**不做**"前移到门禁"——该建议已撤回，SUB 依赖 sharpe） | 做（KOR 瓶颈 8.88%） | ☐ |
| 7 | **不做项**：D5（**已于 09-27 R3 修复闭环**）、D2、D1b（`_unknown` 回填）、D4 历史 327 波补写 | 从清单移除 | ☑ |
| 8 | **D7 点塔 vs 活路错配**：KOR 下一波走 SHORTINTEREST（未亮）还是 ANALYST（已亮但 profile 活路） | **需你拍板**（决定 KOR 后续方向） | ☐ |
| 9 | 去除/标注：`validator.check_batch`、五张 `step_*` 残留、`[opcat]` 噪声打印 | 做（纯清理） | ☐ |

---

> 本报告未覆写 09-27 任何产物，文件独立为 `reports/ra_pipeline_stage_review_v4_20260928.md`。
> 与既有报告结论冲突处（如"瓶颈在 S2→S3 断链" vs "KOR 瓶颈在回测→达标"），
> 建议以**分区口径**为准：全区结论适用于跨区资源分配，分区结论适用于单区战术。

---

## 5. 执行回执（2026-09-28，审阅清单第 3、4 项）

> 本节记录审阅清单中已批准项的实际执行结果，与上文推演层区分：下文全部为**真实执行 + 真实校验**。

### 5.1 第 3 项 D1a — SOP 写点亮判定纪律 ✅ 已完成

| 项 | 内容 |
|---|---|
| 落点 | `Claude/skills/wq-brain-ra-pipeline/SKILL.md` 步 4 第 9 条「金字塔点亮」下（346 行起） |
| 新增 | 点亮判定唯一权威 = 平台 `get_pyramid_alphas`（≥3 即点亮）；**禁止本地表推导**（`alphas.date_submitted` 全库仅 2.7% 非空；塔归属 ≠ `datasets.category`）；`MATCHES_PYRAMID ×N` ≠ 已点亮；`start_date` 会对齐季度快照，近 90 天判定用默认季度值 |
| 同步 | `python tools/sync_skills.py` → 2 文件 × 4 安装位（claude / codex / cursor / workbuddy） |
| 闸 | `test_sync_skills_reports_no_drift` 由红转绿 |

**⚠ 本次踩坑（已修，纪律固化）**：首次直接编辑了安装位 `.workbuddy/skills/`，触发漂移闸。按 AGENTS.md §3.5，**仓库 `Claude/skills/` 是源、安装位是派生**——改 skill 只能改仓库再同步。

### 5.2 第 4 项 D9 — 修 `expressions.status` 回写 ✅ 已完成（代码 + 存量）

**代码层（写入路径，前次会话已完成）**
- `src/wqb/store/_backtest.py::upsert_backtest_rows`：表达式**已存在**分支（`if erow:`）原先只取 id、不推进 status；只有 auto-create 回落分支才写 `backtested`。已补 UPDATE，把待选态推进为 `backtested`。
- `tests/unit/test_store.py` +2 回归测试（正向推进 / 不回退后续态且覆盖 alpha_id），已做**反向验证**（`git checkout HEAD --` 后新测试确为 FAILED，恢复后 2 passed），排除假绿。

**存量层（本次执行，用户批准）**
- 工具：`tools/backfill_expression_status_once.py`（幂等、`--dry-run`、执行前落 `(id → 原 status)` 回滚清单；只推进 `gem/enhanced/pending/selected/gated → backtested`；不碰后续态、不覆盖 alpha_id；批次 500）。
- 规模：20 行 KOR 探针（20/20 有 `backtest_results` 支撑）+ 全量 **4,335 行** = **4,355 行**。
- 区域分布：GLB 2012 / ASI 608 / IND 525 / GBR 334 / JPN 230 / EUR 204 / DEU 101 / KOR 120 / USA 87 / MEA 83 / HKG 29 / CHN 22。
- 结果：`backtested` **1600 → 5935**（+4,335）。

**校验（三项全过）**

| 校验 | 结果 |
|---|---|
| 受保护态零改动 | submitted 31 / completed 38 / dropped 34517 / superseded 11083 / fail 99 / coverage 6 —— **全部前后一致** |
| 支撑性（无孤儿） | 5,935 / 5,935 有回测结果或 alpha 支撑，无支撑 0 |
| 幂等 | 重跑 `--dry-run` = 0 行命中（空转确认） |

**回滚**：`reports/d9_status_backfill_rollback_20260928.json`（n=4,355，含探针前像）+ `..._batch2.json`（n=4,335）。回滚顺序 batch2 先、原清单后。

**回写后的转化率基线（已回测 / 总数）**

| 区域 | 总数 | 已回测 | 转化率 |
|---|---|---|---|
| MEA | 657 | 358 | **54.49%** |
| GLB | 8,315 | 2,012 | 24.20% |
| IND | 2,749 | 663 | 24.12% |
| CHN | 274 | 39 | 14.23% |
| ASI | 5,205 | 633 | 12.16% |
| DEU | 2,253 | 274 | 12.16% |
| KOR | 1,975 | 208 | 10.53% |
| GBR | 8,710 | 617 | 7.08% |
| HKG | 571 | 38 | 6.65% |
| USA | 9,504 | 495 | 5.21% |
| EUR | 12,752 | 256 | **2.01%** |
| JPN | 15,185 | 238 | **1.57%** |

这张表直接支撑审阅清单第 5 项：**JPN（1.57%）与 EUR（2.01%）是生成端严重过剩**，15,185 条 JPN 生成只落地 238 条回测，停生成的优先级最高。

### 5.3 附带修复（执行期发现）

1. **`tools/backfill_expression_status_once.py` 空集合 bug**：0 行命中时把空 list 拼进 SQL `IN ()` → 0 占位符 → `ProgrammingError: Incorrect number of bindings`。已改 `if ids:` 短路后再拼 SQL。
2. **`tests/unit/test_p1_fixes_20260927.py::test_suggest_verdict_covers_real_rejected_history` 由红转绿**：根因是 `tracking/KOR/candidates/` 下两个今日生成的行式转储（`wave_AL3_results.json`、`wave_AL3_modeA_results.json`）顶层为 **list**，撞上测试 helper 的 `glob("wave*_result*.json")` → `list.get()` 崩溃。helper 加 `isinstance(payload, dict)` 守卫（契约文件顶层恒为 dict）；核心断言 `len(rejected) == 24` 完整保留。**生产消费点 glob 的是 `tracking/<REGION>/results/wave*_results.json`（不同目录），不受影响**。建议后续把这两个转储改名/移出 `candidates/`（属用户数据，未擅自改动）。

### 5.4 回归结论

```
pytest tests/ -q    →    1643 passed, 13 skipped, 0 failed
```

**清单第 3、4 项已闭环；第 8 项（D7 KOR 方向）仍待拍板。**
