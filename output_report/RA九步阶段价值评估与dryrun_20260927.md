# RA Pipeline 九步阶段价值评估 + 真实 dry-run 回放

> 生成时间：2026-09-27 23:05 GMT+8 ｜ 范围：`wq-brain-ra-pipeline`（v2.2，唯一挖掘编排 SOP）九步 **S-PRE→S6 + 步 5b**
> 依据来源：① SKILL.md 权威正文（819 行）；② **真实 dry-run 执行输出**（`workflow_chain(dry_run=true)`，零副作用）；③ GBR 真实步级漏斗；④ 2026-09-27 当日提交实测。
> 本次全部操作均**未修改任何数据/文件**（漏斗工具为只读推导，dry-run 遵守 AGENTS.md 干跑契约：不 subprocess、不写库、零配额）。

---

## 0. 结论先行

| 判定 | 阶段 | 依据一句话 |
|---|---|---|
| **A 级：保留并深化** | 步 1（库存盘点/查表）、步 5b（prod-first/闸 PF）、步 7（S4 诊断）、步 8（提交判定）、步 9（S6 回写） | 唯一作用于真实瓶颈（PROD 相关性 wall + 提交层闸门）的环节；今日 2/4 配额全部由「库存修复」路径产出，而非新生成 |
| **B 级：保留但降本/限定触发** | 步 2（S0 体检）、步 3（S1 字段扫描）、步 5（门禁）、步 6（S3 回测） | 有拦截面价值（批次门禁通过率 72.7%、非 https），但均非当前瓶颈；受数据边界或已修 <!-- -->bug 影响，需限定投入 |
| **C 级：精简 / 降触发 / 仅保留必要子集** | 步 4（S2 GEM 生成，GBR 当前边际为负）、步 3 的 feature_engineering 确定性模板、`step_*` 五张恒空表 | GBR 已积压 **7,518 条未消化表达式（86.3%）**，再生成不产生终局价值；确定性模板注入 GEM 实证使整波退化为模板展开 |

**核心量化依据（GBR 真实漏斗，只读推导）**：

```
S2 生成 8,710 → S2→S3 门禁放行 913 → S3 回测完成 722 → 过廉价闸 65 → S4→S5 就绪 4
未消化率 86.3%（gem+selected+pending+gated = 7,518）
批次级门禁通过率 72.68%（194 次 / 141 通过）｜表达式级 99.02%
wave verdict：FAIL 71 / PARTIAL 10 / PASS 3  → 波级失败率 84.5%
瓶颈定位：S3 过廉价闸 → S4→S5 就绪，保留率 6.15%
```

项目级基准（2026-09-26 实证）：表达式 65,580 → 回测率 12.6% → 已测 prod 仅 5.1% → 相关性淘汰率 68% → 端到端转化率 **0.10%**。
⇒ **gate 与生成都不是瓶颈，PROD 相关性才是**。任何作用于「提升 IS / 加大生成量」的投入几乎不产生终局价值。

---

## 1. 逐阶段展开（输入 → 处理 → 输出 → 失败分支 → 价值）

### 步 1（S-PRE）查表 + 库存盘点 · **A 级：保留并深化**

| 项 | 内容 |
|---|---|
| **输入** | `$REGION`；区域 profile（`references/regions/GBR.md`，含 `entry_verdict`）；DB 查表三件套（`get_campaign_summary` / `get_dead_ends` / `get_dead_datasets`）+ `get_mining_yield`（严格口径）；PPA 主题公告（`get_messages`） |
| **处理** | ① 读 profile 决定入口裁决（active / probe-only / **frozen**）；② **库存盘点（2026-09-08 起硬前置）**：`build_gate_prior_from_inventory.py` → `select_ra_basket.py`（去参数网格 + OS 撞车预筛 + 篮内正交 + `GET /alphas/{id}` 的 `is.checks` 无 FAIL 复核）；③ 产出率双口径解读：`conversion` 低=流水线断链（别换区），`yield_rate` 低=标的不出货（别加生成量） |
| **输出** | universe / delay / 中性化 / 排除集 / 排除信号族 / 当前波号 + 候选篮子 `cache/basket.json` |
| **失败分支** | registry 全空=新区 → 进步 2；dead_datasets 覆盖全部候选 → 停止换区；`frozen`（MEA）步 1 即拒 |

**价值评估：最高。** 三条独立实证：
1. 历史实证：同一天前半段跨四区 170 次**新回测**产出 0 条可提交 RA，后半段一次**库存扫描产出 20 条**；
2. **今日实测**：仅有的两颗成功提交（`npdm0mrq`、`E5p2r7VL`）**全部来自已存在的 IS alpha 的提交层修复**，零条来自本波新生成；
3. 现状证据：GBR 已有 8,710 条表达式、回测仅 722 行 —— 库里就有东西，瓶颈明确不在「没生成」。

**建议**：把「先清库存」从 SOP 措辞升级为**可执行的硬闸**——未消化率 > 50%（或 `pending+gated > 本波表达式数 × 2`）即拒绝开新的生成波，机器判定而非靠自觉。

---

### 步 2（S0）数据集体检 + 金字塔配置 · **B 级：保留但简化**

| 项 | 内容 |
|---|---|
| **输入** | 白名单候选集；`recommend_datasets`（平台点塔状态）× `get_mining_yield` × `get_dead_datasets` 三方交叉；本地 `thresholds.json` |
| **处理** | ① `campaign_intel s0-select` 三方交叉打榜；② `workflow_campaign(stage=S0, calibrate=true)` 自学习校准 → **必须再跑一次裸 `stage=S0` 打分**（calibrate 不产出排名，两步非冗余）；③ 座位可达性（`Σest_seats < target` → 结构性不可达告警）；④ 补齐 `field_inspect` 体检包 |
| **输出** | `s0_ranking` / `s0_whitelist` / `s0_calibrate_<region>`，`--target N` 可达性判定 |
| **失败分支** | 配额后仍无非 MODEL → 写 findings，**不退回纯 MODEL 七槽**；全硬排除 → 回步 1 换区 |

**价值评估：中高，但被数据边界封顶。** 它决定「投哪里」，方向正确；
- 减分项 1：本地快照 `WebData_20260219` 只覆盖 7 区，**JPN 白名单 12 集中 0 集、DEU 9 集中 0 集**可生成体检包 → 这些区体检硬门天然失效；
- 减分项 2：`pyramid_quota`（≥2 非 MODEL）等 7 条硬规则叠加后，配置成本高，但对最终是否出货的因果贡献难以量化（GBR 71 波 FAIL 说明「选错集」不是唯一死因）。

**建议**：保留 `s0-select` 三方交叉与「已点亮塔不进白名单」硬规则（这两条有明确止损价值）；把体检包从「必须补齐」改为「数据源可用则 enforce、不可用则 warn + 台账记因」，避免在无数据区域反复空转。

---

### 步 3（S1）字段扫描 + 理解 · **B+ 级：保留高强度子集，砍确定性模板**

| 项 | 内容 |
|---|---|
| **输入** | 白名单数据集；`get_datafields`（含 `users` 热度）；typed catalog |
| **处理** | ① **字段级覆盖审计**（`catalog_<ds>` coverage>0，空 → 写 `<ds>_dead`）；② **幽灵字段验活**（`create_multi_simulation(validate_fields=true)`）；③ prod-corr 分级：`users≥50` 只做信号方向验证、`10-49` 提交前必实测 prod、`0-9` 优先，冷门字段占批次预算 ≥50% |
| **输出** | `fields` 表 + `field_catalog` + ledger `s1_<ds>_d<delay>` |
| **失败分支** | 字段数 <10 → 退回步 2 换白名单 |

**价值评估：两条铁律的唯一落点，必须保留。** 幽灵字段在提交层会重新编译 → `COMPILE_ERROR`，是唯一「零成本预防 vs 100% 提交失败」的检查。
**应砍部分**：`workflow_feature_engineering` 产的是**确定性模板渲染**（8 问框架 + `rank(ts_mean({f},66))`），注入 GEM 会让 LLM 一行都不调、整波退化为模板展开（GBR intraday_pv_feats 实证）→ 现已是「按需 + 人读参考 + 禁注入」，判断正确，保持即可。

---

### 步 4（S2）概念优先生成（GEM） · **C 级：GBR 当前状态下应暂停/大幅减量**

| 项 | 内容 |
|---|---|
| **输入** | region/dataset/delay/universe/data_type；`region_kb` win/dead + `template_kb`（经 `assemble-priors` → `priors_snapshot_<region>`） |
| **处理** | GEM phased pipeline（LLM）；生成侧预闸（quantile 归一、hump 命名参数、bucket range、同骨架换字段封顶 12）、priors 注入；`build-wave` 选波（identity不信), 只是 去重/分桶/骨架配给 |
| **输出** | `expressions` status=`gem`/`enhanced`；ledger idea；`priors_snapshot_<region>` |
| **失败分支** | GEM 未入库 → 超时恢复清单；候选不足 → enhance/扩组合/换数据集 |

**价值评估：当前边际为负（针对 GBR），但非永久。** 依据：
- 生成 vs 消化严重失衡：**8,710 生成 / 722 回测**，未消化 7,518（86.3%）。在这一状态下继续生成，只是把库存压力往后推，不增加 ASNOS; 任何「 IS 提升」都不作用于最终瓶颈（PROD）。
- 存在假绿风险：LLM 通道 402 时报「no meta.json within 90s」且 **dry-run 只验命令构建、验不了 LLM 可达性**（今日 dry-run 同样在这点上沉默）。
- 财务/配额视角：生成零配额但消耗波次、门禁、回测槽位与审查人力，而 S4→S5 保留率仅 6.15%。

**建议**：给 GEM 加**量化触发条件**——`未消化率 < 50% 且 最近 K 波有新增机制` 才开生成波；否则默认走「存量修复/湾区复用」路径（今日实证利率更高）。

---

### 步 5（S2→S3）门禁 · **A 级（必须先修缺陷）** —— 但当前**节点路径 100% 失败**

| 项 | 内容 |
|---|---|
| **输入** | 本波候选表达式（DB 或 exprs-file）；`field_inspect` 体检包；闸 PF 骨架指纹库 |
| **处理** | ghost-audit（幽灵算子，零配额）→ `wave_gate.py`（语法 + gate.py 5 闸 + 体检硬门 + 多样性闸6 + **闸 PF prod 骨架死路**）→ 落 `gate_results` |
| **输出** | `gate_results`（`all_pass` / `fail_reasons`）|
| **失败分支** | 语法 FAIL 必修；多样性 FAIL → 回步 4 补骨架；2 跨集 FAIL → 拆回单集 |

**价值评估：高。** 批次级通过率 **72.68%**（194 次里 53 次被拦）说明门禁确实在拦下有缺陷的批次（等于省掉平台侧整批 ERROR/CANCELLED 连坐与配额浪费）；表达式级 99.02% 则说明它并不过度拦截，判据精度可接受。
**⚠ 现状缺陷（今日 dry-run 实证）**：见 §3 缺陷 #1 —— `gem → batch_track` 自动链里自动插入的 `wave_gate` 节点**必然 TypeError**，即最有价值的这道闸在自动链上 **0% 可用**。缺陷修好后其价值才能兑现。

---

### 步 5b：prod-first 探针（2026-09-19 升为硬门） · **A+ 级：最高价值，应再提前**

| 项 | 内容 |
|---|---|
| **输入** | 本波各信号族最强 1–2 条骨架；`alphas` 表历史 prod 记录（骨架级指纹 = 前 2 个算子调用名） |
| **处理** | `campaign_intel prod-first`（串行，占平台单并发队列）；闸 PF：`≥0.7` 已确认死路 → enforced 拦截整波；`<0.7` 已探明 → PASS；新骨架 → WARN |
| **输出** | EXPAND / STOP 判定；`alphas.prod_correlation` + ledger `prod_first_<wave>` |
| **失败分支** | 家族首探 ≥0.7 → 记 dead_end 换机制，**不做任何去相关变体** |

**价值评估：全链最高，且应再提前。** 依据：
- 累积实证：IND intraday_pv_feats 连投 3 波 24 条（IS 全过 S 4.4–6.5）后才查 prod = 0.79–0.92 → 整族报废；pv103 尾盘反转 8 条同理；
- **今日实测（最强证据）**：GBR 第二轮 B7 变体 prod 0.7134 → 我方闸 **fail-closed 拒提**，直接省下一次注定为废的动作；wpZ3RP96 三连 403 也证明「改结构救不了 prod 墙」；
- 项目级：已测 prod 的 **68% 撞墙**，这是唯一真正的漏斗颈。

**建议**：把它的「骨架指纹」判定从步 5 门禁时点**再提前到步 4 决策前**（决定要不要生成这一族），进一步省掉生成/回测/审查成本。

---

### 步 6（S3）七槽回测 · **B 级：保留，明确为非瓶颈**

| 项 | 内容 |
|---|---|
| **输入** | 门禁放行批次；`settings.json`（decay/neutralization/universe）；`region_kb.gate_priors` 设置先验 |
| **处理** | `pipeline.py run`（n_slots 内部锁定 ≤7）；连坐自动隔离（ERROR 定位坏式 → 其余重发）；全局槽位仲裁（`_lib/slots.py`，缺省 7）；`harvest_multisim_alphas` 收批压缩 |
| **输出** | `backtest_results` / `wave_results` / checkpoint；batch_status 跟踪 |
| **失败分支** | 整批 CANCELLED → 回步 5；429 → 降并发、批大小 ≤5 |

**价值评估：必要但不构成瓶颈。** GBR 已回测 722 行、最佳 sharpe 2.44，说明执行侧健康；真正的流失发生在回测之后（65 条过廉价闸 → 4 条就绪，6.15%）。
**建议**：维持现有并发纪律与连坐隔离即可，**不要扩容/不要加大回测量**（与步 4 同理，加量不解决 prod）。

---

### 步 7（S4）诊断改进 · **A 级：保留**

| 项 | 内容 |
|---|---|
| **输入** | 本波 alpha_id 与指标；`s4-prescreen` 分层结果（READY/REVIEW/REJECT）；OS 衰减基线 |
| **处理** | `review_wave.py` 评审：墙判定（`RN_EXPOSURE` / `ROBUST_STRUCTURAL` / 各闸 walls）；near 池；`prod-first`；Mode B 换腿 + Mode A 调参（70/30）；辅助腿检索 `get_salvage_pool`（组合只用结构交互，禁加权混合） |
| **输出** | ledger `s4_walls_<region>_<wave>`；salvage_pool； `add-win` / `add-dead-end` 决策 |
| **失败分支** | prod≥0.7 → Mode B 换概念；同一想法 >10 种结构仍不过 → 记 dead_end 回步 2 |

**价值评估：高。** 它是唯一把「65 条过廉价闸」转化成决策（修 / 换腿 / 封死）的环节；两条实证：(1) `risk_neutralized_sharpe ≤ 0` → 该 alpha 就是它自己声称的因子暴露，继续调参只会让暴露更纯（HKG w4 六条 −0.33~−0.57）；(2) `robust_universe_sharpe/limit < 0.5` 的结构性信号不得入 near（否则 PARTIAL 永不收敛、停止规则 B 失效）。
**建议**：保持它在 prod-first **之后、任何扩变体之前**的位置；不要把 10 种结构试探花在已被 prod 判定为死路的腿上。

---

### 步 8（S4→S5）稳健闸与提交判定 · **A 级：保留，但「权威性」表述需修正**

| 项 | 内容 |
|---|---|
| **输入** | 候选 alpha_id；`is.checks`；failed-count 资格门（REGULAR 要求 Failed RA == 0） |
| **处理** | `brain-alpha-robustness` → `submit_verdict` → **用户确认** → 执行提交（REGULAR 走 worldquant-submit-alpha / SUPER 走 superalpha） |
| **输出** | 提交层 checks 双视图；四形态处置；ACTIVE 判定（只认轮询 `status=ACTIVE`） |
| **失败分支** | PROD/SELF 不过 → 回步 7；配额耗尽 → 等 ET 日重置 |

**价值评估：高（省配额的核心环节），但文档口径需要修正。** 依据今日实测：
- 四形态全部命中：`201 async`（今天的两颗 FINAL 都走了 201）、`403 明确失败`（3 次零成本回带全量 checks）、`200 空体`、`200 IS passed`；
- **已知矛盾**：2026-09-26 实测 `GET /alphas/{id}/submit` **恒返回 404 + 空体**（对已 ACTIVE 也一样）→ `submit_verdict` 的「提交层视图/403 盲区唯一权威」名不副实，其 403 分支是**死代码**，处女候选恒返回 `UNVERIFIABLE`；
- 真正可靠的零成本预检 = **直接 POST submit**（403 回带全量 checks），今天的 3 次 403 全部由此取得 verdict。

**建议**：步 8 文案改为「**判据源头 = POST submit；`submit_verdict` 保留为模拟层 READY/REVIEW 判定权威**」，避免 Agent 依据 `UNVERIFIABLE` 误判为不可提交。fail-closed 的 prod 闸已在 `super_build.py` 落地（默认强制 probe，≥0.7 拒提），该口径应推广到 REGULAR 常规路径。

---

### 步 9（S6）复盘回写 · **A 级：保留，但当前存在真实断链**

| 项 | 内容 |
|---|---|
| **输入** | 本波 verdict 事实；`step_funnel.py` 只读漏斗；salvage_pool；点塔进度 |
| **处理** | `upsert_wave_result`（verdict 严格枚举 PASS/PARTIAL/FAIL）→ `upsert_registry_empirical` → `upsert_ledger_key`（含 `seal_dead_end` 先沉降再封存）→ `campaign_intel pyramid` → `workflow_campaign(S6, dataset-experience)` |
| **输出** | `wave_results.verdict`、`registry_empirical`、ledger `s6_verdict_<wave>`、`reports/dataset_experience/*_campain.md`、`region_kb` 自动刷新 |
| **失败分支** | 未回写 = 本波未完成 |

**价值评估：高（决定下一波先验质量），但**今天的 dry-run 抓到它的输出没被消费：见 §3 缺陷 #2（`priors_snapshot_gbr` 停在 2026-09-19，而 KB 源已 2026-09-25/26）→ S6→S2 闭环没自动闭合，下一波 GEM 会读到 **8 天前的先验**，今天的 развит 结论（含 GBR 提交层两条新实证）不会自动进入下一波。

**建议**：把 `assemble-priors` 挂到 S6 收尾（或在 GEM 入口对 stale 快照做 fail-closed），写进步 9 完成定义。

---

## 2. 价值分级汇总与取舍建议

| 级别 | 阶段 | 取舍 | 判断依据（可核验） |
|---|---|---|---|
| **A 保留+深化** | 步 1、步 5b、步 7、步 8、步 9 | 加人力/加把关 | 唯一作用于 PROD 与提交层瓶颈；今日 2/4 配额全由库存修复路径产出；prod 68% 撞墙 |
| **B 保留+降本** | 步 2、步 3、步 5、步 6 | 维持但要修 bug / 限触发 | 门禁批次通过率 72.7%（有截面价值）；回测侧健康（722 行、best S 2.44）非瓶颈 |
| **C 精简/降触发** | 步 4 GEM（GBR 当期）、FE 确定性模板、`step_*` 五张空表 | 暂停或减触发 | 未消化率 86.3%；模板注入实证使整波退化；五张表恒 0 行且已禁止填充 |
| **D 待修后才有价值** | 步 5 节点化（`wave_gate` 自动插入） | 先修 `prod_family_gate` 签名 | 今日 dry-run 实证 TypeError，导致 `gem→batch_track` 自动链 0% 可用 |

---

## 3. 真实 dry-run 回放（零副作用，逐步 IO 与价值判断）

**执行命令**（真实调用，遵守干跑契约：不 subprocess、不写库、零配额）：

```
workflow_chain(dry_run=true, chain=[
  {"node":"campaign","params":{"region":"GBR","stage":"S0"}},
  {"node":"gem","params":{"region":"GBR","dataset_id":"starmine","delay":1,"universe":"TOP700"}},
  {"node":"batch_track","params":{"region":"GBR","wave":"s2_starmine_d1","dataset":"starmine"}}
])
```

**Step 0｜前置状态快照**（只读，`tools/step_funnel.py --region GBR`）
- 输入：GBR 既有 4 张表 + ledger
- 输出：表达式 8,710 / 未消化 7,518（86.3%）｜门禁批次通过率 72.68%｜回测 722 行、过廉价闸 65｜submit_ready 4｜波 verdict FAIL 71 / PARTIAL 10 / **PASS 3**
- 价值判断：**步进端口已经饱和**（未消化 86.3%）→ 不应再开生成波；瓶颈在 S3→S5 保留率 6.15%。**该快照本身就否决了本次链式执行的生产合理性**（正好印证「不一知半解就开波」的价值）。

**Step 1｜节点 campaign（步 2/S0）**
- 输入：`{region: GBR, stage: S0}`
- 输出：`campaign_dir = tracking\GBR`（存在校验通过）→ 构建命令 `score_datasets.py --campaign-dir …\tracking\GBR`；`dry_run: true，命令未执行`
- 价值判断：**通过**。但注意本次构建的是**裸 `stage=S0` 打分步**；按 SOP 需在它之前先跑一次 `calibrate=true`（两步缺一不可）。→ 建议日常入口不要把 calibrate 当作可选。

**Step 2｜节点 gem（步 4/S2）**
- 输入：`{region: GBR, dataset_id: starmine, delay: 1, universe: TOP700}`
- 输出：完整 plan（`data_category=other / data_type=MATRIX / priors_from_db=true`）与**真实告警**：
  > `priors_snapshot_gbr`（**2026-09-19 23:23:59**）早于其 KB 源 `GBR/region_kb@2026-09-25 18:38:47`、`GBR/registry_empirical@2026-09-26 00:18:38` —— S6 回写后没重组 priors，本次 GEM 会用旧先验
- 价值判断：**极高**（一次零成本干跑抓到真实断链）。若实跑，这一波 GEM 会拿着 8 天前的 win/dead 先验生成，今天的 GBR 提交层经验不会回流。
  ⇒ **缺陷 #2：S6 → S2 的 priors 闭环未自动闭合**（`docs` 里 `assemble-priors` 已支持 `--snapshot-ledger`，但没有挂在 S6 收尾）。

**Step 3｜自动插入节点 wave_gate（步 5 门禁）— 因 `stop_on_failure` 中止后续**
- 输入：`{region: GBR, dataset: starmine, wave: auto, inspect_mode: warn, prod_family_gate: true}`
  （该节点是 `tools_workflow.py:446-466` 在检测到 `gem → batch_track` 缺失门禁时**自动注入**的 fail-safe）
- 输出：`success: false`，`error: run() got an unexpected keyword argument 'prod_family_gate'`
- 价值判断：**门禁本身高价值，但节点路径当前为 0% 可用**。这一次失败本身极有价值——它替代了一次真实的执行性失败（在正���员手里会表现为「自动链起不来」）。

  ⇒ **缺陷 #1（根因已定位）**：
  - 调用侧 `world-quant-brain-mcp/tools_workflow.py:464` 传入 `"prod_family_gate": True`；
  - 接收侧 `src/wqb/workflow/nodes/wave_gate.py:34` 的 `run()` 形参只有 `region/dataset/wave/datasets/exprs_file/candidates/expr/from_db/skip_diversity_gate/fix/campaign_dir/inspect_mode/timeout_sec/dry_run/_context`，**无 `prod_family_gate`**；
  - 后果：任何 `gem → batch_track` 自动链（含自动插入的 fail-safe）**必然 TypeError**；CLI 直跑 `tools/wave_gate.py` 不受影响（`--prod-family-gate` 已在 CLI 侧落地）。
  - 修法二选一：① `run()` 增加 `prod_family_gate: bool = True` 并透传给 CLI；② 自动插入侧去掉该键（依赖 CLI 默认开）。
  - **守护缺口**：`tools/audit_node_registration.py` 校验的是 *registry 元数据 vs run() 签名*，**不覆盖「自动注入参数」这类调用侧** → 本次漂移无任何测试能拦。建议补一名 файл 负例测试：注入 `{gem, batch_track}` 链，断言 wave_gate 不 TypeError（对应 RULES.md「白名单/豁免式守护必配反向负例」原则）。

**执行结果汇总**：`executed 3 / requested 4 / failed_at = wave_gate`（batch_track 因 `stop_on_failure` 未达）。
**副作用核对**：未创建/修改任何文件与库；未消耗配额；未发起平台请求（漏斗命令为本地只读 SQL）。

---

## 4. 建议的下一步（按 ROI 排序）

1. **修缺陷 #1**（`prod_family_gate` 签名/传参不一致）＋补自动注入参数的反向负例测试 —— 否则步 5 在自动链上永久失效。
2. **闭合 S6→S2 priors 环**：S6 收尾强制 `workflow_campaign(stage=S2, subcommand=assemble-priors)`；GEM 入口对 stale 快照建议改成 fail-closed（今天只 WARN，实跑会静默用旧先验）。
3. **给步 4 GEM 加量化触发阀**（未消化率 <50% 才开生成波），把省下的容量投入步 1 库存 + 步 5b prod-first + 步 8 提交层修复路径——今天的 2/4 配额正是由这条路径产出。
4. **修正步 8 权威性表述**：以 POST submit 为判据源头，`submit_verdict` 作模拟层 READY/REVIEW 权威；REGULAR 常规路径也接 fail-closed prod 闸（`super_build.py` 已成���跑）。
