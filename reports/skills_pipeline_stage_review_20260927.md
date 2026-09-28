# Skills 九阶段流水线审阅报告（S-PRE→S6）

- 审阅日期：2026-09-27
- 审阅对象：`wq-brain-ra-pipeline` 九步流水线（L-RA 唯一编排 SOP）及其调用的分层 skill / MCP 节点
- 权威依据：`Claude/skills/wq-brain-ra-pipeline/SKILL.md`（v2.2, last_verified 2026-09-26）、`references/decision-table.md`、`Claude/skills/INDEX.md`、`src/wqb/workflow/registry.py`、`src/wqb/config.py`
- 证据性质：本次所有数字均来自本机只读实测（DB 查询 / 仓库代码 / 节点干跑），非文档转述

---

## 0. 审阅方法与价值判据

### 0.1 本次采用的四条判据

对每个步骤问四个问题，只有**全部通过**才判「保留并深化」：

| 判据 | 含义 | 反例（判精简/去除） |
|---|---|---|
| **C1 可验证产物** | 是否产出可被下游消费的结构化产物（DB 表 / ledger 键 / 文件包） | 只产出人读文本，下游不消费 |
| **C2 有真实调用方** | 是否存在生产路径的调用点（非仅文档/测试） | 零调用方、仅注释引用 |
| **C3 有实证收益** | 是否有前后对照的量化收益记录 | 收益仅口头声称 |
| **C4 不可被合并** | 其判断是否与其它步骤重叠而可归并 | 与另一闸判据同源、重复拦截同一问题 |

### 0.2 本次实测的全景基线（2026-09-27）

```
DB: data/wqb.db
  expressions           65,730   （gem 18,047 / dropped 34,081 / superseded 8,085 / selected 2,327 / pending 1,494 / backtested 1,470 …）
  backtest_results       8,398
  gate_results           1,533   （all_pass=1 共 769 → 批次通过率 50.2%）
  wave_results             949   （覆盖 13 个区域）
  alphas                 8,454
  ledger_kv              4,698 行 / 79,215,075 字节 ≈ 75.5 MB
workflow 节点：18 个；四处同步审计 = 18/18/18/18，无漂移
区域：config.REGIONS = 14；profile 13（缺 AMR）；战役目录 13（缺 TWN/AMR）
```

---

## 1. 步 1（S-PRE）查表 + 开工前置

### 输入
- `$REGION`（唯一显式输入）
- `references/regions/<REGION>.md` 区域 profile（front-matter：静态配置 / 数据集红黑榜 / priors / 闸门覆盖 / 循环策略）
- DB 台账：`campaign_summary`、`dead_ends`、`dead_datasets`、`mining_yield`（含 `strict=true` 严格口径）
- 账户存量 IS alpha（库存盘点）

### 处理过程
1. **入口裁决**：按 profile 的 `entry_verdict` 放行或拒入。实测 GLB = `active`；MEA = `frozen`（步 1 即拒）。
2. **库存盘点**（2026-09-08 新增，先于一切新挖）：`build_gate_prior_from_inventory.py` 枚举存量 alpha + 资格门复算 + 写回 `gate_priors`，再由 `select_ra_basket.py` 去参数网格 / OS 撞车预筛 / 篮内正交 / 平台复核。
3. **产出率读数**：区分两个比率——`conversion` 低 = 流水线问题（诚实性检查）；`yield_rate` 低 = 标的问题（换区）。
4. **PPA 主题门禁**：扫 `get_messages` 的 Power Pool 公告，解析当期 region/delay/universe。

### 输出
universe / delay / 中性化 / 排除集 / 排除信号族 / 当前波号 + `gate_priors` 快照。

### 价值评估

| 判定 | 项目 | 依据 |
|---|---|---|
| ★ 保留并深化 | 库存盘点 | **C3 极强**：2026-09-07 实证——会话前半段跨四区 170 次新回测产出 **0 条**可提交 RA；后半段一次库存扫描产出 **20 条**。数量级差异 |
| ★ 保留并深化 | 产出率双比率分离 | C1/C3：把「管道问题」与「标的问题」分开，直接决定后续动作是修管道还是换区，误判会导致持续投槽 |
| ★ 保留并深化 | region profile 注入 | C1：13 区各一份，区域差异（闸门覆盖/循环策略）有唯一落点 |
| ✅ 保留 | PPA 主题门禁 | C1：PPA 提交必须精确匹配当期主题，错配即废 |
| ⚠ 观察 | `yield_rate` 严格口径 | 实测旧口径曾把 IND 显示为 34% 产出率而实际可提交 0（严格口径 12.6%）→ 说明该口径本身是**纠错成果**，应保留但需防止再被局部代码绕回旧口径 |

---

## 2. 步 2（S0）数据集体检 + 金字塔配置

### 输入
region + 候选数据集全集 + `thresholds.json`（六节）+ 平台点塔状态。

### 处理过程
1. **体检包前置**：白名单锁定后、进步 3 之前，必须为每个白名单数据集补齐 `tracking/mining/field_inspect_<region>_<dataset>.json`。
2. **三方交叉选集**（`campaign_intel.py s0-select`）：`recommend_datasets`（平台真实点塔）× `get_mining_yield`（历史产出率）× `get_dead_datasets`（判死清单）。
3. **校准 + 打分（2 步必需 + 1 步可选）**：
   - 必需 ① `calibrate=true` → 反学 category 权重与拥挤甜区，写 `thresholds.json`
   - 必需 ② 裸 `stage="S0"` → 产出 `s0_ranking`（⚠ ① **不产出排名**）
   - 可选 ①′ `calibrate=true dry_run=true` → 只预览不写盘
4. **硬约束 7 条**：已点亮塔不进白名单（硬规则）、白名单 ≥2 个非 MODEL、`category_weight` 限 0.9–1.15、饱和路由、体检包就位…

### 输出
`ledger s0_ranking`（实测 GLB 单键 60,221 字节）/ `s0_whitelist` / `s0_calibrate_<region>` / `*_dead` / `thresholds.json`。

### 价值评估

| 判定 | 项目 | 依据 |
|---|---|---|
| ★ 保留并深化 | 三方交叉选集 | C3：`lit=Y`（已点亮塔）直接剔除，把 S0 从「本地 alphaCount 推断」升级为「平台 pyramid 端点实测」——IND 曾把 earnings3/insiders1/macro63 这类结构性弱集推到前排，7 集 197 条回测 0 候选 |
| ★ 保留并深化 | `calibrate` → `score` 两步 | C4：实测 `cmd_calibrate` **只写 thresholds.json、不产出排名**，故第 ② 步不是冗余重跑。此前曾被误判为「三次重复」 |
| ⚠ 可精简（低风险） | 可选步 ①′ `calibrate --dry-run` | 文档自身已限定「仅新区/校准结果可疑时才需要审」→ 属**条件触发**步骤，日常波次可默认跳过，无需每次呈现 |
| ⚠ 需修正 | 体检包区域覆盖缺口 | 实测 334 个包：hkg 172 / usa 104 / eur 33 / chn 11 / glb 6 / asi 5 / jpn 2 / kor 1；**DEU / IND / GBR / MEA / TWN = 0**。这 5 个区的体检硬门在 `warn` 灰度假定下**等于空转**——低覆盖/厚尾/稀疏事件的预处理约束无人把关 |

---

## 3. 步 3（S1）字段扫描 + 理解

### 输入
白名单 `$DS` + delay + universe + 本地 WebData 快照。

### 处理过程
1. **typed catalog**（`scan_fields.py`，必做）：字段名/类型/覆盖率落 `field_catalog`。
2. **字段级覆盖审计**（唯一落点铁律①）：`catalog_<ds>` coverage>0；覆盖为空写 `<ds>_dead`。依据：`recommend_datasets` **不校验区域覆盖率**。
3. **幽灵字段验活**（铁律②）：新字段先 `create_multi_simulation(validate_fields=true)` 验活；DB 有记录但平台报 `Attempted to use unknown variable` 者，提交层直接 COMPILE_ERROR。
4. **字段分级风险筛查**：按 `users` 分级——`≥50` 只做信号方向验证；`10–49` 进候选池；`0–9` 优先（理论 prod_corr≈0）；冷门字段占批次预算 ≥50%。
5. **按需加载 L1 三件套**：`brain-dataset-exploration-general` → `brain-datafield-exploration-general` → `brain-data-feature-engineering`。

### 输出
`fields` 表 + `ledger s1_<ds>_d<delay>` + 预处理决策（backfill/winsorize/rank/zscore/ts_event_*）。

### 价值评估

| 判定 | 项目 | 依据 |
|---|---|---|
| ★ 保留并深化 | typed catalog + 覆盖审计 | C1/C4：typed catalog 是闸 2 的判据来源（缺目录 stage_gate **直接 FAIL**）；覆盖审计是「选到空集」的唯一拦截点 |
| ★ 保留并深化 | 幽灵字段验活 | C3：不验活 → 整批 CANCELLED 连坐（批内一条坏式取消全部兄弟任务） |
| ★ 保留并深化 | `users` 分级 → prod_corr 规避 | C3：用户数 ≥50 的字段 prod_corr 必超；冷门字段（≤9）理论 prod_corr≈0。直接决定批次预算分配 |
| ⚠ **价值存疑** | `workflow_feature_engineering` 节点（作「字段理解」用时） | **C1/C3 双不通过**：该节点是**确定性模板渲染**（8 问框架 + `rank(ts_mean({f},66))`），**不含 LLM 推理**。GBR `intraday_pv_feats` 实证：把它当 ideas 喂 GEM → GEM **一行 LLM 都不调**、整波退化为模板展开，正是「每个字段套一个 rank」的同质化堆。故已被判定：① 不是必做项；② 产物仅供人读；③ **禁止注入 GEM**。（该缺陷**已修复**，此处保留记录以防回退） |
| ⚠ 需修正 | 三元信息的落点分裂 | 有效产物（typed catalog / 质量先验 / `s2_field_pool`）与该节点输出混在同一 skill 名下，阅读者易把「模板渲染」误当「字段理解」——建议在 L1 层显式分列 |

---

## 4. 步 4（S2）选波：概念优先生成

### 输入
`priors.json`（DB KB 组装）+ `s1_<ds>_d<delay>` + catalog `data_type` + settings（delay/universe）。

### 处理过程
1. **priors 组装**（`subcommand="assemble-priors"`，禁手写）：从 DB KB（`region_kb` win/dead + `template_kb`）确定性组装，落快照含 sha256。GEM 管道**只消费 `wins`（≤6）与 `dead_ends`（≤12）**两个键。
2. **gate_priors 分流**：`by_operator_count` / `by_field_family` → 进 GEM prompt（表达式层能作用）；`by_decay` / `by_neutralization` **不进 prompt**（是仿真设置），由步 6 `pipeline.py run` 直接改写本波设置。
3. **GEM 生成**（强制）：机制 → 1–2 个具体字段 id → 一个 Implementation Example；**禁止**「每个字段套 rank」；必须带 priors。
4. **生成侧预闸**（`pipeline_pregate`）：`hump(x,k)`→`hump(x, hump=k)`；`bucket(rank(x))` 补 `range`；区域非法 group 字段丢弃；非标窗口按别名表归一（20/21→22、60/63/65→66…）；同骨架换字段封顶（`WQB_GEM_MAX_PER_SKELETON` 缺省 12）；`quantile(x, driver="gaussian")`→`quantile(x)`；丢弃加权混合毒模式。
5. **按实验问题选波**（2026-09-24）：8 条不是固定上限，`--size N` 仅作容量；预定实验须先写清单入 DB ledger。

### 输出
`expressions` status=`gem` / `enhanced` + ledger idea + `priors_snapshot_<region>`。

### 价值评估

| 判定 | 项目 | 依据 |
|---|---|---|
| ★ 保留并深化 | assemble-priors 单上游化 | C1：使 DB KB 成为 S2 先验唯一上游，S6 回写后下次自动变新；profile 静态 priors 降为种子 |
| ★ 保留并深化 | gate_priors 分流（表达式层 vs 设置层） | C3 极强：此前两者**全塞 prompt** → LLM 改不了 decay，S3 永远用 settings.json 固定值。GBR 实证 decay=14 过闸 28.3%(n=46) vs decay=4 仅 3.9%(n=408)，而三波仍跑 decay4 → **0/44** |
| ★ 保留并深化 | 生成侧预闸 | C3：闸 4 ARITY 312 次命中的根因即 `quantile` 默认 driver；预闸在源头消除，门禁只作兜底 |
| ⚠ **产能过剩（核心问题）** | S2 生成量 vs S3 吞吐 | **实测**：全库未消化表达式（gem+selected+pending+gated）= **21,936**；GLB 单区未消化 3,527（占该区生成池 42.4%）。GLB 步级漏斗显示 S2 生成 8,315 → 门禁放行仅 195（**保留率 2.35%**）——瓶颈定位明确指向这一跳 |
| ⚠ 需修正 | 生成侧预闸仍漏识别 | `hump` 命名参数类错误在 2026-09 共 42 次，**最后仍出现在 09-25（单日 12 次）**——说明「GEM 预闸归一 + 门禁拦截」双保险下仍持续漏网，应在生成侧加硬约束而非依赖门禁兜底 |

---

## 5. 步 5（S2→S3）门禁 + 步 5b（PF 闸）

### 输入
GEM 落库的候选表达式（`--from-db`）+ 体检包 + `platform_constraints.json`。

### 处理过程
1. **幽灵算子硬闸**（`campaign_intel ghost-audit`，纯本地零配额）：含幽灵算子（sigmoid/ts_entropy/ts_skewness…）会触发整批 CANCELLED **连坐**，必在 dispatch 前拦。
2. **多样性守卫**（唯一执行口径 = toolkit `gate.py:check_batch_diversity`，即闸 6）：判据三源——自学习契约 `explore_contract`（过期 FAIL-CLOSED）/ 收益来源多样性（同批 >60% 共享同一 exposure → FAIL）/ 家族天花板预检（≥2/3 → WARN）。
3. **体检→表达式硬门**（`field_inspect_gate.py`，`wave_gate.py` 内置）：5 条——低覆盖(cr<0.4)须含 `ts_backfill`；高偏度(|skew|>2)须含 `rank`/`winsorize`/`signed_power`；厚尾(kurt>8)须含 `rank`/`winsorize`；单边恒正负不得用原始水平；稀疏事件须用 `trade_when`。
4. **闸 8 + 闸 PF**：`gate.py` 共 8 闸（语法/白名单/VECTOR 包裹/不可访问算子/毒模式/多样性/longCount/EVENT）；**闸 PF** 为骨架级死路预检（骨架指纹已确认 prod≥0.7 → fail-closed 拦整波）。
5. **流程**：`check_batch → wave_gate → 步 6 create_multi_simulation`。

### 输出
`gate_results`（`all_pass` / `fail_reasons`）。

### 价值评估

| 判定 | 项目 | 依据 |
|---|---|---|
| ★ 保留并深化 | 幽灵算子硬闸 | C3：连坐代价极高（批内一条坏式取消全部兄弟），纯本地零配额 |
| ★ 保留并深化 | 体检→表达式硬门 | C3：治「三连复发」——缺包时该闸不生效，历史低覆盖/厚尾/稀疏事件预处理约束一路裸奔到仿真 |
| ★ 保留并深化 | 闸 PF（骨架级） | C3 精细：**骨架比字段更准**——同字段 `mdl135_d01_icc` 在 `+vec_avg` 骨架下 prod=0.76-0.82 死路，在 `+vec_avg×ts_zscore` 骨架下 prod=0.46-0.57 干净。零配额、纯本地 |
| ⚠ **可去除（已失效）** | `wqb.expression.validator.check_batch` | **C2 不通过（零生产调用方）**：实测全仓仅 `tests/unit/test_skills.py` 与注释/文档字符串引用，无任何生产调用点；且它只实现 **4** 条形状闸，与 `gate.py:check_batch_diversity` **判据不同**。历史正文并列两套口径 + 一条「两者判据不同」的注，极易被误读成「调了前者就过了闸」。SOP 已于 2026-09-17 收敛为「方法论参考」——**建议进一步在源码层加 deprecated 标注或删除**（改动需同步 2 处测试） |
| ⚠ 需修正 | 体检硬门在 5 区空转 | 见步 2：DEU/IND/GBR/MEA/TWN 体检包为 0，`warn` 灰度下该闸等于不存在。建议开新区即 `enforce`（fail-closed） |

---

## 6. 步 6（S3）七槽回测

### 输入
门禁放行的批次 + settings（含 settings prior 改写后的 decay/中性化）。

### 处理过程
1. **七槽填槽**（Token-Bucket C≈7）：≥2 跨金字塔、≥1 win 换腿、弱探针最多 1 槽；每槽先 1–2 条骨架查 prod-first，prod<0.7 才扩到 8。
2. **settings prior**：读 `region_kb.gate_priors`，样本 ≥30 且过闸率 ≥ 当前设置 ×2 的格子自动改写本波设置并打印 lift。
3. **连坐隔离**（默认开）：ERROR 批解析子模拟 → 定位真凶 → 回写 `expressions.status='fail'` → 无辜兄弟作为重发批优先重发一次。
4. **账户级槽位仲裁**（`_lib/slots.py`）：`logs/_slots/` token 文件跨进程计数，在飞 ≥ `WQB_GLOBAL_SLOTS`（缺省 7）即等待。
5. **收批压缩**：`harvest_multisim_alphas` + `harvest_multisim_results`，把 18 次调用链压成 2 次。
6. **积压清理**：每波结束只读 SQL 查 `pending`+`gated`，> 本波表达式数 2 倍即优先纳入下一波。

### 输出
`backtest_results` / `wave_results` / checkpoint（`ckpt_w<W>`）。

### 价值评估

| 判定 | 项目 | 依据 |
|---|---|---|
| ★ 核心 | 七槽填槽 + 并发纪律 | C3：7 批同提实证安全（连续多波 0 连坐），单轮吞吐 ×7 |
| ★ 核心 | settings prior 直接改设置 | C3：见步 4，治愈「prompt 改不了 decay」的根因 |
| ★ 核心 | 连坐隔离自动化 | C3：JPN w7/w8 实证——一条 `bucket()` 缺 range 导致整批 8 条连坐，10 批丢 8 批 **64 条**；自动化后无辜式不再陪葬 |
| ★ 核心 | 槽位仲裁 | C3：多流水线同跑不再超 C≈7（超发即 429） |
| ⚠ 需修正 | 生成-回测吞吐失衡 | 实测未消化 21,936 条。SOP 已给正确动作（优先清积压、禁止无脑新建），但**缺少生成侧的硬配额**——建议把「S3 实测吞吐」作为 S2 的准入参数写进选波清单 |

---

## 7. 步 7（S4）诊断改进 + 步 8（S4→S5）提交判定

### 输入
本波 alpha_id（从 `backtest_results` 按波标签精确解析）+ 平台指标。

### 处理过程
- **S4 预筛压缩**：批量拉指标分层 READY/REVIEW/REJECT——REJECT 直接判死不进链，只对存活者走完整链（评审效率提升约 **8 倍**）。
- **walls 诊断**：`RN_EXPOSURE` 墙——`risk_neutralized_sharpe ≤ 0` 且 `sharpe ≥ 1.58` ⇒ 该 alpha **就是它自己声称的那个因子暴露**，直接记 dead_end、禁止调参。
- **near 池剔除结构性死信号**：robust/limit < `near.robust_min_ratio`（缺省 0.5）的行打 `ROBUST_STRUCTURAL`，不入 near。
- **prod-first 探针**（收批后必调）：族级串行跑平台 prod，`STOP(prod≥0.7)` 的族不再扩变体。
- **IS→OS 衰减校准**：`expOS = IS sharpe × 0.358`（USA 124 例实测衰减比），仅作配额参考、**不作排序依据**。
- **提交判定链**：① Failed-count 资格门（RA 要求 `Failed RA == 0`，比只看 `result=="FAIL"` 严格）→ ② `submit_verdict`（**唯一权威**，含 403 盲区）→ ③ **用户确认** → ④ 执行提交。

### 输出
`ledger s4_walls_<region>_<wave>` / `salvage_pool` / `submit_ready` / ACTIVE alpha。

### 价值评估

| 判定 | 项目 | 依据 |
|---|---|---|
| ★ 保留并深化 | S4 预筛压缩 | C3：8 条候选从 8 次逐条评审压到 1 次预筛 + 仅存活者进链 |
| ★ 保留并深化 | `RN_EXPOSURE` 硬规则 | C3：HKG w4 七条里六条 `risk_neutralized_sharpe` 在 −0.33~−0.57 而 raw sharpe 非零；而 w3 的 `O0roWEM7`（0.96 ≈ raw 1.17）是约 150 次回测中唯一真信号特征——**禁止调参**省下大量无效迭代 |
| ★ 保留并深化 | prod-first 族级 STOP | C3：IND `intraday_pv_feats` 价量相关反转连投 3 波 24 条（S 4.4–6.5 全 IS 过）后才查 prod = **0.79–0.92**，整族报废 |
| ★ 保留并深化 | OS 衰减校准的**语义边界** | C1/C4：实测 IS 与 OS sharpe 的 Spearman 秩相关**仅 +0.086**，IS 各桶 OS>0 存活率平坦（70–80%）→ 故校准**不抬高 IS 阈值**，只作期望值参考。这个「知道自己不该做什么」的边界声明价值极高 |
| ★ 保留 | 提交响应 4 形态处置 | C3：2026-09-26 实证 3 颗候选因**只轮询不补发**而悬空 >24h；②③ 形态在工具链里**没有补发闭环**，须 SOP 手工补发 |
| ⚠ 需修正 | 判定链与提交动作的补发缺口 | `_poll_submit_until_resolved` 只给 **60 秒**窗口，超时即返回形态②；`workflow submit_alpha` 节点 Step 4 **只有轮询、无 re-POST 分支**。建议把 re-POST 补发做进节点，而非依赖 SOP 手工 |

---

## 8. 步 9（S6）复盘回写

### 输入
本波 `backtest_results` + `gate_results` + `wave_results` + 逐数据集实际回测集。

### 处理过程
1. **步级漏斗**（先看再用数据写结论）：`tools/step_funnel.py` 只读推导，输出 S2 生成池 / S2→S3 门禁 / S3 回测 / S4→S5 就绪 / S6 verdict / **瓶颈定位**。
2. **自动部分**：`pipeline.py --review` 收批后自动刷新 `region_kb`（`recent_waves` / `gate_priors_local` / `updated_at`）→ 下一波步 4、步 6 自动读到最新。
3. **手动部分**：win / dead_end / seal / pyramid 回写。`seal_dead_end` 先把失败候选沉降入 `salvage_pool`（收集宽），残值回填 `dead_end.salvage`。
4. **点塔进度回写**：`campaign_intel.py pyramid`，输出单行直接拷进 `wave_result.key_findings`。
5. **逐数据集经验沉淀**：`workflow_campaign(stage="S6", subcommand="dataset-experience")` → `reports/dataset_experience/<region>_<dataset>_campain.md`。

### 输出
`wave_results.verdict`（强制枚举 PASS/FAIL/PARTIAL）+ `registry_empirical` + `ledger s6_verdict_<wave>` + 数据集经验文档。

### 价值评估

| 判定 | 项目 | 依据 |
|---|---|---|
| ★ 保留并深化 | `step_funnel.py` 只读步级漏斗 | C1/C4：**不建表、不写库、零新数据**，纯从既有 4 张表推导；且工具**自带口径局限声明**（各步取各自表存量、时间窗不一 → 链上数值可能不单调，仅用于定位瓶颈）。这种「自带免责边界」的工具设计应作为范式推广 |
| ★ 保留并深化 | 自动刷新 region_kb | C3：使 S2 先验与 S3 设置自动升级，无需人工回写才生效——生命周期闭环的关键 |
| ★ 保留并深化 | 先沉降再封存（`seal_dead_end`） | C1：解决 `dead_end.salvage` 字段「此前恒 null」的历史遗留，救援动用守资格线（收集宽、动用严） |
| ⚠ **可去除（已下线残留）** | 五张 `step_*` / `*_summary` 表 | **实测：DB 中不存在这些表**（`sqlite_master` 查询为空）。step-metrics 子系统已于 2026-09-17 整体下线并归档 `attic/step_metrics_20260917/`。SOP 已标「恒 0 行且不应填充」——**建议彻底清除残留引用**，避免读者以为需要补写 |
| ⚠ 存量数据质量 | `wave_results.verdict` 存量非枚举行 | 实测 GLB 该字段有 5 行是描述性长文本（如「FAIL — 8 条全负（-0.37~-1.29），但证明镜像符号有效」），与另 42 行纯 `FAIL` 混存。新写入已被强制枚举并自动归一（描述搬进 `key_findings[0]`），但**存量未回填**，导致按 verdict 聚合时口径分裂 |

---

## 9. 价值汇总与精简建议清单

### 9.1 分级汇总

| 级别 | 步骤/组件 | 处置建议 |
|---|---|---|
| **S 级：核心保留 + 深化** | 步 1 库存盘点；步 1 产出率双比率；步 2 三方交叉选集；步 3 typed catalog + 覆盖审计 + 幽灵字段验活 + users 分级；步 4 assemble-priors + gate_priors 分流；步 5 幽灵硬闸 + 体检硬门 + 闸 PF；步 6 七槽 + 连坐隔离 + 槽位仲裁；步 7 S4 预筛 + RN_EXPOSURE + prod-first；步 8 submit_verdict 唯一权威 + 4 形态处置；步 9 step_funnel + region_kb 自动刷新 + seal 沉降 | 保留，按 §9.2 深化 |
| **A 级：保留（价值明确但非核心）** | PPA 主题门禁；`salvage_pool` 辅助腿检索；提交多样性监控；IS→OS 衰减归因；`wave_meta` 选波实验清单 | 保留 |
| **B 级：可精简（条件触发即足够）** | 步 2 可选步 ①′ `calibrate --dry-run` 预览；步 3 `feature_engineering` 节点（作字段理解时） | 改为条件触发 / 按需，不占流水线必经位 |
| **C 级：建议去除或标注废弃** | `wqb.expression.validator.check_batch`（零调用方）；五张 `step_*` 表残留引用 | 源码层 deprecated 或删除；清理文档残留 |
| **D 级：需修正的缺口** | 5 区体检包为 0；生成侧预闸漏 `hump`；提交 re-POST 补发未入节点；S2/S3 产能失衡；`verdict` 存量未回填 | 见 §9.2 |

### 9.2 建议动作（按性价比排序）

| # | 动作 | 目标 | 依据强度 |
|---|---|---|---|
| 1 | **给 S2 加「S3 实测吞吐」准入配额** | 遏制 21,936 条未消化积压 | 实测：GLB 漏斗保留率 2.35%，瓶颈已定位 |
| 2 | **开新区即 `--inspect-mode enforce`** | 补 5 区体检硬门空转（DEU/IND/GBR/MEA/TWN） | 实测：334 包里 5 区为 0 |
| 3 | **把 re-POST 补发做进 `submit_alpha` 节点** | 消除「异步受理被当失败」盲区 | 实测：60 秒窗口 + 节点无补发分支，曾致 3 颗悬空 >24h |
| 4 | **生成侧硬约束 `hump`/`bucket` 命名参数** | 停止漏网 | 实测：09-25 单日仍 12 次 hump 命名参数失败 |
| 5 | **源码层标注/删除 `validator.check_batch`** | 消除双口径误读 | 实测：零生产调用方 |
| 6 | **回填 `wave_results.verdict` 存量非枚举行** | 统一按 verdict 聚合口径 | 实测：GLB 5 行描述性文本混存 |
| 7 | 清理五张 `step_*` 表文档残留 | 消除「需补写」误解 | 实测：表不存在 |
| 8 | 步 3 L1 层把「模板渲染」与「字段理解」分列 | 防止误把模板当理解 | C1/C3 双不通过 |

---

## 10. 整链演练记录（dry-run，零副作用）

### 10.1 演练设置

- 输入域：`REGION=GLB`、`DS=model264`、`DELAY=1`、`UNIVERSE=TOP3000`、`WAVE=s2_mdl264_trendprob_d1`
- 引擎：`src/wqb/workflow/executor.py::execute(node, params, dry_run=True)`
- 契约：走完零成本前置 → 构建命令/请求计划 → 到此为止；不 subprocess、不写库、不建目录
- 覆盖：15 个调用点，覆盖九步中的步 1（库存盘点）、步 2/3/4/5/6/7/9；步 8 用 `judge`（参考层，**不含真实提交**）
- 可复现：`python reports/dryrun_chain_runner_20260927.py`；原始记录 `reports/dryrun_chain_result_20260927.json`

### 10.2 逐步输入输出变化与命令构建结果

| # | 阶段 | 节点 | 干跑 | 构建出的真实命令 |
|---|---|---|---|---|
| 1 | 步1 S-PRE 库存盘点 | `inventory_scan` | OK | `<repo>\...python.exe <repo>\tools\build_gate_prior_from_inventory.py --regions GLB --emit-candidates cache/candidates.json --write-priors` |
| 2 | 步2 S0 数据集体检+打分 | `campaign` | OK | `<repo>\...python.exe -u <skillroot>\wq-brain-campaign-toolkit\scripts\score_datasets.py --campaign-dir <repo>\tracking\GLB` |
| 3 | 步3 S1 字段扫描/理解 | `feature_engineering` | OK | `<repo>\...python.exe -u <skillroot>\brain-data-feature-engineering\scripts\feature_engineering.py --region GLB --dataset model264 --delay 1 --universe TOP3000 --category MODEL …` |
| 4 | 步4 S2 priors 组装 | `campaign` | OK | `<repo>\...python.exe -u <skillroot>\wq-brain-campaign-toolkit\scripts\campaign.py --campaign-dir <repo>\tracking\GLB assemble-priors` |
| 5 | 步4 S2 GEM 生成 | `gem` | OK | `<repo>\...python.exe -u <skillroot>\brain-make-some-gem\scripts\headless_runner\run.py --config <skillroot>\...\config.json --data-category …` |
| 6 | 步4 S2 选波(build_wave) | `campaign` | OK | `<repo>\...python.exe -u <skillroot>\...\build_wave.py --campaign-dir <repo>\tracking\GLB --dataset model264 --wave s2_mdl264_trendprob_d1 --from-db` |
| 7 | 步5 S2→S3 门禁 | `wave_gate` | OK | `<repo>\...python.exe -u <repo>\tools\wave_gate.py --campaign-dir <repo>\tracking\GLB --region GLB --dataset model264 --wave s2_mdl264_trendprob_d1 --from-db` |
| 8 | 步5 合并门禁 | `unified_gate` | OK | 流程计划：`ghost_operator_gate` → `diversity_gate` → `field_inspect_gate` → `unified_gate_check` |
| 9 | 步6 S3 七槽回测 | `batch_track` | OK | `<repo>\...python.exe -u <skillroot>\...\pipeline.py --campaign-dir <repo>\tracking\GLB run --dataset model264 --wave s2_mdl264_trendprob_d1 --max-rounds 3 --review --write-ledger` |
| 10 | 步7 S4 诊断改进 | `campaign` | OK | `<repo>\...python.exe -u <skillroot>\...\review_wave.py --campaign-dir <repo>\tracking\GLB --alphas e7bWq7ME levNRePA xA3EmA7n … --tag s2_mdl264_trendprob_d1 --write-ledger` |
| 11 | 步7 S4 自动评审 | `auto_review` | OK | `<repo>\...python.exe <repo>\tools\campaign_intel.py s4-prescreen --ids-file logs/_tmp_s4_ids_s2_mdl264_trendprob_d1.txt` |
| 12 | 步8 判定(参考层) | `judge` | OK | 流程计划：`plan_only`（不解析 brain_client，避免触碰网络与子进程） |
| 13 | 步9 S6 复盘回写 | `campaign` | OK | `<repo>\...python.exe -u <skillroot>\...\campaign.py --campaign-dir <repo>\tracking\GLB --wave s2_mdl264_trendprob_d1` |
| 14 | 步9 点塔回写 | `auto_pyramid` | OK | `<repo>\...python.exe <repo>\tools\campaign_intel.py pyramid --region GLB --delay 1` |
| 15 | 步9 自动收批 | `auto_harvest` | OK | 流程计划：`auto_harvest` → `auto_link` → `auto_upsert` → `auto_report` |

**结果**：15/15 通过（`== 15/15 节点干跑通过`）。

### 10.3 干跑不是「假绿」——负例验证

为排除「干跑只报 OK、实际不可诊断」的风险，另跑 5 个**故意错误**输入：

| 负例 | 结果 | 回传 error |
|---|---|---|
| S4 波号不存在 | 已拦 | `no backtest alphas for GLB/s2_nonexistent_d1` |
| S2 未注册区域 `XYZ` | 已拦 | `Cannot resolve campaign_dir for region=XYZ. Set WQB_CAMPAIGN_DIR or WQB_WORKSPACE_ROOT…` |
| `wave_gate` 缺 `dataset` | 已拦 | `Missing required params: ['dataset']` |
| `gem` 缺 `universe` | 已拦 | `Missing required params: ['universe']` |
| `batch_track` 缺 `wave` | 已拦 | `Missing required params: ['wave']` |

**5/5 被拦且均带可诊断 error**（无 `success=False + error=None` 的静默失败）。

### 10.4 零副作用验证

| 检查项 | 演练前 | 演练后 | 结论 |
|---|---|---|---|
| `data/wqb.db` mtime | — | `2026-09-27 19:23:28`（早于 21:04 演练） | 未被写入 |
| `expressions` | 65,730 | 65,730 | 不变 |
| `backtest_results` / `gate_results` / `wave_results` / `alphas` / `ledger_kv` | 8,398 / 1,533 / 949 / 8,454 / 4,698 | 同左 | 不变 |
| 干跑声称的异步任务文件 | — | `logs/_async_tasks/fe_GLB_model264_20260927_210455.json` **不存在** | 未创建目录/文件 |
| S4 临时清单 | — | `logs/_tmp_s4_ids_*.txt` 不存在 | 未创建 |

**唯一写入** = 演练自身的记录文件（`reports/dryrun_chain_*`）与 Python `__pycache__`。

### 10.5 演练外需人工确认的环节

- 步 1 的库存篮敲定依赖平台 `GET /alphas/{id}` 复核 → 干跑不覆盖
- 步 4 GEM 的 **LLM 可达性**干跑无法验证（已知余额不足时表现为误导性的 `no meta.json within 90s`，干跑会显示假绿）
- 步 8 的 `submit_verdict` 与真实提交 → **按设计不入演练**（提交类必须用户显式确认）

---

## 11. 局限与未覆盖项

1. **MCP 未连接**：本会话 `wq-brain-http` / `wqb-db` 服务器未注册（deferred catalog 仅 2 个本地工具、无匹配），因此演练采用仓库内 `src/wqb/workflow/executor.py` 的同一干跑实现（MCP 节点即为该实现的薄包装），**未调用任何平台端点**。
2. **未做真实提交/回测**：本次为纯模拟演练，`submit_verdict` / `create_multi_simulation` / GEM LLM 通道均未触发。GEM 的 LLM 可达性**干跑无法验证**（已知：余额不足时表现为误导性的「no meta.json within 90s」，且干跑会显示假绿）。
3. **口径非精确转化率**：`step_funnel` 各步取各自表存量、时间窗不一致，链上数值**可能不单调**，仅用于定位瓶颈。
4. **价值判断的主观边界**：C1–C4 判据的权重分配属本次审阅的方法选择，非项目常量；「B 级可精简」不构成删除授权，需业务方确认。
