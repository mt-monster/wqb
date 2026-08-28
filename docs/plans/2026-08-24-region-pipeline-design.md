# 分区 RA-Pipeline 设计方案 A'（状态机修正版 · 待决策稿）

> 日期：2026-08-24 ｜ 状态：**设计完成，未实施**
> v1：基于 wqb.db 八区画像的**静态**流程卡设计
> v2 = A'：流程型改为**状态机**——流程型是状态不是身份；八张卡降级为"当前状态快照 + 迁移触发器"；新增分诊规则、双源指标兜底、冷启动校准 SOP。v1 的核心缺陷（区域状态变化后静态卡过期）由本版消除。

## 0. 目标与设计原则

**目标**：每个 region 拥有一套独立的挖掘流程——不同的阶段序列、专属规则、停止条件与量化目标；且**流程随台账状态自动迁移**，不因区域状态变化而失效。

**四条原则（不可违反）**：
1. **toolkit 单源不变**：`wq-brain-campaign-toolkit` 仍是唯一执行引擎；区域差异只在编排层，不复制引擎代码。
2. **数据单源不变**：区域画像、黑名单、win 配方全部从 `wqb.db` registry 派生，流程卡只引用不复制（防双写漂移）。
3. **闸门不放松**：五闸预检、robustness 必经闸、S6→S-PRE 回写闭环对所有流程型生效；差异只能"加严/调序/调配额"，不能"跳过"。
4. **流程型是状态不是身份**（A' 新增）：每张卡 = 当前状态快照 + 迁移触发器；S6 台账回写后重跑分诊，命中触发器即换卡。卡描述"现在怎么挖"，触发器描述"何时不再这么挖"。

---

## 1. 流程型状态机（A' 核心修订）

### 1.1 六个流程型状态

| 状态 | 一句话定义 | 典型起点 |
|---|---|---|
| S-CAL 校准 | 无台账区先制造数据：3-5 个标准波 + 全量回写 | 新区/新账 |
| S-DIAG 诊断修复 | 挖了没产出，倒序归因再开工 | 产出/wave 效率≈0 |
| S-CROWD 拥挤度实验 | 死因以 prod_corr 为主，核心矛盾是结构性拥挤 | prod_corr 死因占比高 |
| S-ROT 机制轮换攻坚 | 信号族大面积死亡 + 存量少，换机制攒组件 | dead_ends 多产出少 |
| S-HARV 配额收割 | 候选积压 > 提交配额，变现优先于挖掘 | submit_ready 积压大 |
| S-BOOK Book 管理 | ACTIVE 结构性饱和，无挖掘主循环 | ACTIVE 数饱和 |

### 1.2 分诊指标（双源兼容——关键设计）

**每个指标都有 DB 源与平台源两个取数口径**：有台账的区域读 DB（权威、快），无台账的新区直接查平台 API 兜底。分诊逻辑本身不依赖 DB 存在——这样新区冷启动时状态机照常运转，校准波产出台账后自动切换到 DB 源。

| 指标 | DB 源（权威） | 平台源（兜底） | 判定用途 |
|---|---|---|---|
| ACTIVE 数 | campaigns 层状态 | `get_user_alphas` 按 region 数 ACTIVE | S-BOOK 入口 |
| submit_ready 积压 | `get_submit_ready` | —（本地概念） | S-HARV 入口 |
| wave 收口率 | `get_region_overview` closed/total | `tracking/<R>` 目录 wave 状态 | 悬债/收口判定 |
| dead_end : 产出比 | dead_ends 数 vs submit_ready+ACTIVE | — | S-ROT 入口 |
| 产出/wave 效率 | submit_ready+ACTIVE ÷ closed waves | OS 表现代理 | S-DIAG 入口（防"高产"误判——MEA 教训） |
| 拥挤度死因占比 | dead_ends 中 prod_corr 类占比 | `check_correlation` 抽样新候选 | S-CROWD 入口 |

### 1.3 迁移规则（进出条件）

| 状态 | 进入条件 | 退出条件（→去向） |
|---|---|---|
| S-CAL | 无 config / waves 全 open / 0 dead_ends | ≥3 校准波完成且首版 registry 建成 → 重跑分诊 |
| S-DIAG | 产出/wave 效率 ≈ 0（如 MEA 29 wave 0 ready） | 首颗 submit_ready → S-HARV；确认饱和 → S-CROWD |
| S-CROWD | prod_corr 类死因占比 ≥ 50% 或抽样新候选普遍 >0.7 | 占比下降且 open waves < 10 → S-ROT |
| S-ROT | dead_end:产出比高但 ACTIVE 未饱和（如 KOR 32:2） | ACTIVE ≥10 且 SA 落地 → S-BOOK；效率仍 0 → S-DIAG |
| S-HARV | submit_ready 积压 ≥ 10 | 积压 < 10 → S-ROT（开新 wave）；新增提交全撞 prod_corr → S-CROWD |
| S-BOOK | ACTIVE 结构性饱和（新提交普遍 prod_corr FAIL） | book 大规模退化需重建 → S-DIAG（罕见） |

```
             ┌────────────── S-BOOK（ACTIVE 饱和）──────────────┐
             │  退役-替换 / SA 正交维护 / option9 监督           │
             ▲                                                  │
S-CAL ──────►│                                                  │
（校准波     │   每波 S6 回写后重跑分诊（§1.2 指标）              │
  3-5 波）   │                                                  │
             ▼                                                  │
      ┌── S-DIAG ──┐   ┌── S-CROWD ──┐   ┌── S-ROT ──┐   ┌── S-HARV ─┐
      └────────────┴───┴─────────────┴───┴───────────┴───┴───────────┘
                           （迁移动作 = 换卡 + wave_results 记录迁移原因）
```

### 1.4 分诊时机与迁移纪律

- **强制时机**：每区每波 S6 回写后；S-PRE 查表生成配置包前。
- **迁移动作**：换卡 + 在 `wave_results` 记录迁移原因（触发指标值 + 新状态），留审计轨迹。
- **首迁确认制**：某区首次命中触发器时提示用户确认再换卡；同向第二次起自动迁移。防指标噪声导致的误迁移。

### 1.5 冷启动校准 SOP（S-CAL 状态的展开）

新区/无台账区（当前 = GBR/HKG/ASI）不直接差异化，先走统一校准：

1. **建账**：region config（universe 档位先过平台合法性验证——TOP800/1500/2500/5000 全平台非法）+ 战役目录 + registry static 层。
2. **3-5 个校准波**：标准九步完整走，闸门目标降档（验证"有无信号方向"，不追求提交）但流程不跳步；便宜闸门（PASS_CHEAP）优先。
3. **探针纪律**（预注入跨区铁律）：单字段裸探针天花板 0.2-0.52，首探全 RED **不判死**数据集，须复合结构二轮（跨字段比值/差分/事件门控）；稀疏事件字段先 `ts_backfill + trade_when` 填充门控；同骨架变体自相关蚕食预防。
4. **每波必写 ledger**：win/dead_end/campaign 状态全量回写——**校准波就是 S6→S-PRE 闭环的启动子**。
5. **毕业**：第 3 波后首次 `diversity_audit.py` + 重跑分诊，按 §1.3 落位（预计多数新区落 S-DIAG 或 S-ROT 起步）。

---

## 2. 八区实证画像（2026-08-24 快照，分诊依据）

| 区 | universe/中性化 | waves(关) | dead_ends | submit_ready | 当前状态（§1.3 分诊结果） |
|---|---|---|---|---|---|
| IND | TOP500 / STATISTICAL / d1 | 68 (64) | 13 | **31 积压** | **S-HARV**（产出效率 0.48/wave，积压 31） |
| KOR | TOP600 / STATISTICAL | 21 (20) | **32** | 2 SUBMITTED | **S-ROT**（dead_end:产出 = 16:1，ACTIVE 2 <10） |
| EUR | 待补(TOP2500/COUNTRY) | 51 (21) | **42** | 2 READY | **S-CROWD**（prod_corr 0.82-0.9 主导死因）+ 30 open 悬债 |
| MEA | TOP400/TOP300 / SECTOR | 29 (20) | 10 | **0** | **S-DIAG**（产出/wave = 0，"高产"假象） |
| ASI | 待补 | 15 (0) | 0 | 0 | **S-CAL**（2 untried 候选已就位） |
| GBR | 无 config | 12 (0) | 0 | 0 | **S-CAL**（连 config 未建） |
| HKG | 无 config | 11 (0) | 0 | 0 | **S-CAL**（同上） |
| USA | —（book ~145 ACTIVE 饱和） | — | 2 | — | **S-BOOK**（结构性饱和；option9 线程监督） |

**跨区铁律（全状态生效）**：prod_corr 饱和是结构性的（调参无效只能换概念）；同骨架变体蚕食（有 ACTIVE 的族变体默认判死）；单字段探针天花板；稀疏事件先填充；本地 prod_corr 系统性偏低（近 0.7 一律 `submit_verdict.py` 平台判定）。

---

## 3. 八区流程卡（当前状态快照 + 迁移触发器）

每张卡 = 该区**当前**状态的执行细节。区域状态迁移后换卡，卡内规则不再适用即作废——不维护过期卡。

### 3.1 IND · S-HARV 配额收割（快照）

- **阶段序列**：①`S6` 四关审计 31 颗积压（fresh check：指标/相关性是否随时间退化）→ ②`S5` 按优先级批量提交（每颗过 `submit_verdict.py`）→ ③ACTIVE ≥10 → `wq-brain-superalpha` → ④`S6` OS 退化监控 → 退役-替换 → ⑤**仅当**积压 <10 才触发 S0-S3 新 wave。
- **专属规则**：提交优先级 = 互相关正交性 > OS 衰减风险 > 指标高低；SA 组件池两两 self_corr < 0.55；同 wave 产出互相关的只挑 1 颗。
- **迁移触发器**：积压 < 10 → **S-ROT**（开新 wave）；新增提交普遍撞 prod_corr → **S-CROWD**。
- **量化目标**：30 天清空积压 + 首颗 IND SA ACTIVE。

### 3.2 KOR · S-ROT 机制轮换 + SA 攻坚（快照）

- **阶段序列**：①`S-PRE` 强排雷（32 条 dead_ends + 跨区铁律全量注入）→ ②`S0` 白名单只留正交族（news/sentiment/insiders/shortinterest，campaign 层已标注为 SA 组件方向）→ ③`S2` 双轨：win 换腿（慢×快配方：评级修正 × SH 短周期，已实证 2 颗 1.77/1.83）+ SA 组件定向挖（互相关预筛）→ ④`S4` 首探全 RED 必跑复合结构二轮才可判 dead_end → ⑤`S5` 每颗达标即提交攒 ACTIVE → ⑥ACTIVE ≥10 → SA。
- **专属规则**：novel 族 8 条败阵候选按 ts_event_*/去 winsorize 修复重跑；ml_factor_proj 评级修正金矿做窗口/中性化扩展；同骨架变体默认判死。
- **迁移触发器**：ACTIVE ≥10 且 SA 落地 → **S-BOOK**；连续 3 波效率仍 0 → **S-DIAG**。
- **量化目标**：ACTIVE 2→10，首颗 KOR SA。

### 3.3 EUR · S-CROWD 拥挤度实验（快照）

- **阶段序列**：①`S-PRE` 饱和风格黑名单注入（model238 d1 rank 族/multi_horizon FCF mixes/starhold）→ ②**收口循环**：`review_wave.py` 逐条审 30 条 open waves → dead_end/win/close 三路处置 → ③`S5` 先提交 2 颗 READY（78jdv6b1 prod 0.6945、Wj7g2gAx 0.5463）→ ④`S0` 非 MODEL/EQ 族配额 ≥50% → ⑤`S2` 跨周期混合默认（0.4 慢 MODEL 残差 + 0.6 快 PV 已实证）→ ⑥`S3` prod-first：每槽先平台判定再投入。
- **前置修复**：region config 补全（universe=TOP2500, neutralization=COUNTRY, decay6）。
- **迁移触发器**：open waves <10 且拥挤死因占比下降 → **S-ROT**；READY 积压 ≥10 → 混合 **S-HARV**。
- **量化目标**：open waves 30→<10；每条新 dead_end 必须收敛为规则。

### 3.4 MEA · S-DIAG 诊断修复（快照）

- **阶段序列**：①`S6` Wave autopsy：20 条 closed waves 逐条归因（闸门挡的/概念死的/没跑完的）→ ②NEAR 候选救援：近阈值者集中 Mode A 参数收敛（TOP400/300 双档 + SECTOR 中性化矩阵）→ ③`S0` 换非饱和族（pv/fundamental72/model25/31 已死 → news/analyst/sentiment）→ ④`S3` 五槽填槽 → `S4` 标准链。
- **专属规则**：本地 prod_corr 只做粗筛下限（0.612 vs 0.7723 实证偏差）；本地值 >0.6 一律平台判定。
- **迁移触发器**：首颗 submit_ready → **S-HARV**；确认全区饱和 → **S-CROWD**。
- **量化目标**：首颗 MEA submit_ready（0→1）。

### 3.5 ASI / GBR / HKG · S-CAL 冷启动校准（快照）

- **阶段序列**：§1.5 校准 SOP 全文适用。各区差异仅初始候选：ASI 有现成 analyst94（sharpe 0.666）/analyst81（score 0.692）；GBR/HKG 从 config 建账起步。
- **迁移触发器**：≥3 校准波完成 + 首版 registry → 重跑分诊落位（预计 S-DIAG 或 S-ROT 起步）。
- **量化目标**：三区各产出首版 registry（static + ≥1 dead_end 或 win）。

### 3.6 USA · S-BOOK Book 管理（快照）

- **阶段序列**：①日常 `S6` OS 退化监控（shortinterest3 差值 +0.238 等）→ 退役-替换；②SA 组件正交维护（新增只接受情绪/事件/期权微观结构等正交族）；③option9 线程监督（独立 gmail 账号 ThreadPool=3，纳周报不纳日循环）；④新 REGULAR 提交前强制平台判定。
- **迁移触发器**：book 大规模退化需重建 → **S-DIAG**（罕见）。
- **前置决策**：USA 是否入统一台账（见 §6 决策点 2）。
- **量化目标**：SA 组件 self_corr < 0.55 维持；option9 可提交者转 S5。

---

## 4. 跨区共享层（所有状态公共底座）

| 组件 | 约束 |
|---|---|
| 并发槽 | 全平台 8 槽共享；多区并行走 `wqb-concurrency` 全局令牌桶；单区日循环用五槽填槽 |
| 提交配额 | 48h 闸全账号共享；IND 积压会长期占额，**建议同时最多 2 区并行** |
| 台账回写 | 所有状态 S6 必须 upsert registry_empirical；回写即触发 §1.4 重分诊 |
| 五闸 + robustness | 全状态无差别；S-CAL 允许目标降档但不跳步 |

---

## 5. 实施选项（A' 更新）

| 方案 | 内容 | 工作量 | 优点 | 缺点 |
|---|---|---|---|---|
| **A'（推荐）** | ra-pipeline 增"第 0 步：分诊分发"（分诊指标 + 迁移规则写入 `references/triage.md`）；八张快照卡 `references/regions/*.md`（含迁移触发器）；双源取数口径写明 | 1-1.5 天 | 卡不过期（状态机兜底）；新区冷启动即插即用；零代码风险 | 分诊仍由 Agent 执行非程序化，靠纪律 |
| **B** | A' + 参数下沉 registry static 层，matrix 查表自动派生配置包 + 分诊脚本化 | 2-3 天 | 数据驱动 + 分诊可回归测试 | 需动 wqb-db schema + matrix 出包逻辑 |
| **C** | 8 个 `wq-brain-ra-pipeline-<REG>` skill | 4-5 天 | 区间完全隔离 | 违反 toolkit/编排单源纪律；刚清理完 campaign-auto 类重复，重蹈覆辙 |

**推荐：A' 起步，稳定后按需演进 B，不做 C。**

### A' 分阶段路线

| 阶段 | 内容 | 理由 |
|---|---|---|
| P1 | triage.md + IND(S-HARV) + KOR(S-ROT) 卡 | 分诊框架落地 + 变现最快 + 战略目标 |
| P2 | EUR(S-CROWD) + MEA(S-DIAG) 卡 | 收口悬债 + 0→1 诊断 |
| P3 | ASI/GBR/HKG 校准 SOP 实例化 | 三区共用 §1.5，仅初始候选不同 |
| P4 | USA(S-BOOK) 卡 | 需先决策台账归属 |

---

## 6. 决策点清单（需要用户拍板）

1. **实施载体**：A' / B / C？（推荐 A' 起步）
2. **USA 是否纳入统一台账**：建 tracking/USA + region config 入 wqb.db，还是维持 book 管理独立于体系外？
3. **GBR/HKG 建账时机**：随 P3 立即建 config 开工，还是冻结观察？
4. **优先顺序**：IND > KOR > EUR > MEA > ASI > GBR/HKG > USA 认可吗？
5. **并行度**：并发槽与提交配额共享约束下，最多 2 区并行且 IND 提交期独占——接受吗？
6. **迁移确认制**（A' 新增）：首次命中触发器提示确认、同向第二次起自动迁移——接受，还是每次迁移都人工确认？
