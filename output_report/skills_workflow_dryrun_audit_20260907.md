# Skills & Workflow Dry-Run 审计报告 + 改进方案

- **日期**: 2026-09-07（会话续于 09-02 00:30）
- **范围**: `Claude/skills/wq-brain-ra-pipeline`（v2.1）为主的 skills 链 + `src/wqb/workflow/` 引擎 + `world-quant-brain-mcp` 68 工具 + `data/wqb.db` 运行时数据
- **方法**: 静态交叉引用核对（SKILL.md ↔ scripts ↔ MCP 注册名 ↔ DB 实数据）+ 关键节点实跑验证（field_inspect_gate、pytest 478 passed、SQL 直查）
- **用户三问**: ① 逻辑是否自恰？② 调用点是否连贯？③ 对有效挖掘因子是否高效？

---

## 0. 结论总览（先答三问）

| 问题 | 结论 | 一句话 |
|---|---|---|
| ① 逻辑自恰 | **基本自洽，2 处文档级失实** | SKILL.md 步5"无体检包"描述错误（实际 146 包可用）；工具名/路径有局部漂移 |
| ② 调用点连贯 | **链路完整，但存在一条实证断链** | S2→S3：`ws2_*` 波 6100 条表达式入库后从未走门禁/回测（gate_rows=0） |
| ③ 挖掘效率 | **结构性低效，瓶颈清晰** | 全库可提交库存仅 **MEA 3 颗**；prod 饱和是全局第一瓶颈；三目标区域战役均未真正起量 |

**总体判断**: skills 骨架（九步链、七槽回测、门禁五闸、submit_verdict 唯一判定）设计是自洽且现代的；问题集中在**"文档与磁盘现实脱节"**和**"波次状态机没有回收/推进兜底"**两点，导致大量生成物无声积压——挖矿机完好，但传送带卡了。

---

## 1. 逻辑自洽性审计

### 1.1 通过项（验证过，无需动）

| 检查项 | 结果 |
|---|---|
| MCP 工具引用无悬空 | SKILL.md 引用的 11 个 `workflow_*` 工具 + `submit_verdict` 全部真实注册于 `tools_workflow.py` / `tools_ops.py` |
| 脚本存在性 | `score_datasets.py`、`pipeline.py`、`campaign.py`、`build_wave.py`、`assemble_priors.py`（toolkit/scripts/）、`wave_gate.py`、`preflight_wave.py`、`field_inspect_gate.py`（tools/）全部存在 |
| 体检硬门真实生效 | 实跑 `check_expressions(['rank(ern3_all_delay_1_pre_reptime)'], region='ASI', dataset='earnings3')` → 正确产出覆盖率/zero_inflated 两条 violation；无包数据集正确返回 `unavailable` 而非伪装通过 |
| executor dry_run 链 | #62 修复后 `inspect.signature` 透传 + `_context` 注入有效（有回归测试覆盖） |
| 判定链单头 | judge 已降参考层，`submit_verdict.py` + Failed-count 资格门为唯一权威，无双头冲突 |
| 测试基线 | 全量 pytest **478 passed**，无红 |

### 1.2 失实/漂移项（P1 文档修复）

**D1. SKILL.md 步5 体检包描述失实（最重要）**
- SKILL.md 称："现状：全仓库暂无可用体检包（现存两份 USA 文件 fields 为空）"
- 磁盘事实：`tracking/mining/field_inspect_*.json` 共 **148 个，146 个非空**（USA 102 / EUR 19 / CHN 11 / GLB 6 / ASI 5 / JPN 2 / KOR 1）
- **根因诊断**：这 146 个全是 git 未跟踪新文件，git 视角下只有 2 个被追踪的 USA 文件且恰好 fields 为空——撰写者只看了 git 视角。属"文档与未提交产物脱进"的典型病例。
- 影响：任何照 SKILL.md 行事的后续 agent 会**跳过体检硬门**（以为没包），白白放走一个已接线可用的质量闸。

**D2. 脚本路径引用错位**
- SKILL.md 将 `wave_gate.py` / `preflight_wave.py` 归在 toolkit/scripts/ 下引用，实际在根 `tools/`。

**D3. MCP 工具模块归属描述漂移**
- `submit_batch`（实为 tools_ops）、`sa_probe`（tools_ops）、`preflight_expressions`（tools_data）在 SKILL.md 部分段落被描述为 workflow 族工具。调用名本身有效（MCP 注册名=工具名），但"11 个 workflow 工具"的清单口径有水分，易误导后续 agent 数错工具。

---

## 2. 调用点连贯性审计

### 2.1 静态链路：完整 ✅

九步骨架每一步的消费者/生产者契约（Artifact 契约表 + "由谁写"列）核对通过；`workflow_chain` 异步 join（`join_async=True`）等上游落库后再续跑，无竞态路径。

### 2.2 运行时断链：S2→S3 传送带卡死（P0 数据问题）

**实证**（`data/wqb.db` 直查）：

| 波次 | wave_number | status | 表达式数 | gate_results 行数 |
|---|---|---|---|---|
| id=146 | s2_multifactor_return_pred_d1 | pending | 0 | **0** |
| id=147 | s2_pattern_scores_d1 | pending | 142 | **0** |
| id=169 | s2_option_horizon_decomp_d1 | pending | 69 | **0** |
| id=211 | s2_analyst_consensus_d1 | pending | 54 | **0** |
| id=277 | s2_insider_feats_d1 | pending | 16 | **0** |

- 全库积压：**pending 3448 + gated 2652 ≈ 6100 条**（占全库表达式 60%+），主体是 2026-08-25~26 生成的 USA `ws2_*` 波（2083 条）与 EUR 波（2229 条）。
- **键不匹配根因**：`gate_results.wave` 存的是整数 `wave_number`（36/38/39…）或 `mcp_direct_*` 字符串，而 `ws2_*` 波的 `wave_number` 形如 `s2_pattern_scores_d1` → `LEFT JOIN` 永远 NULL，门禁记录查不到、也从未执行。
- 连带问题：USA pending 表达式字段 `short_term_price_volume_based_return_5d` 在 fields 表 exact/like 均 **0 命中**——疑似废弃脚本产物（token 隐患实证，与 USA 字段字典 known issue 一致）。
- **波次状态机缺兜底**：wave 生成后既无 TTL 过期回收、也无"pending 超 N 天告警"，S2 产出就这样无声堆着。

**影响**: 这 6100 条不是资产是**负债**——它们污染 pending 池统计、干扰多样性闸的批次计数、让"还有多少候选"这类决策全部失真。

---

## 3. 挖掘效率审计（对"有效挖因子"的回答）

### 3.1 全局第一瓶颈：prod 饱和

可提交库存口径（sharpe≥1.58 & UNSUBMITTED & prod_corr<0.7 & self_corr<0.7）全库盘点：

| 区域 | 可提交颗数 |
|---|---|
| MEA | **3** |
| USA / GLB / EUR / KOR / IND / ASI / CHN / JPN | **0** |

近 7 天回测达标率（|S|≥1.58）：IND 94/195（48%，最高）、KOR 14/313、EUR 5/149、GLB 0/16。
**IND 是最典型样本**：Sharpe 产量极高，但 83 条达标 UNSUBMITTED 中 prod&self<0.7 的数量 = 0——**挖得越多，prod_corr 撞墙越狠**，纯粹的"高频挖矿、零库存产出"模式。

### 3.2 三目标区域战役现状（提示词均未兑现）

| 区域 | 近 10 天回测 | 状态 |
|---|---|---|
| GLB | 16 条 | 71 pending 未起量；42 颗 PASS_CHEAP 候选已被 PROD_CORR 全灭（0.82–0.86） |
| USA | 0 条 | 提示词未执行；2083 历史 pending 未清 |
| HKG | 0 条 | expressions 表 0 行——probe-only 从未启动（符合两阶段设计，但连 Phase 0 都没跑） |

### 3.3 效率结论

当前体系"生成能力 >> 过闸能力"。症结不在 GEM 生成或七槽回测（产能充足），而在：
1. **prod_corr 闸前移不足**——饱和族字段在 S2 生成层未被排除，浪费到 S3 回测才暴露；
2. **积压不清理**——6100 条死库存让一切"还剩多少候选"的判断失真；
3. **区域资源配置错位**——把回测配额花在 IND（48% 达标但 0 可提交）而非 prod 低饱和的新字段族。

---

## 4. 改进方案（按优先级 / ROI 排序）

### P0 — 立即执行（零配额消耗，纯本地）

| # | 改进项 | 动作 | 预期收益 |
|---|---|---|---|
| P0-1 | **修正 SKILL.md 步5 失实描述** | 改为"146 个非空体检包位于 tracking/mining/，gate 已接线可用"；同时校正 D2 路径（wave_gate/preflight_wave 在 tools/）与 D3 工具归属 | 后续 agent 不再跳过体检硬门 |
| P0-2 | **裁决 ws2_* 孤儿波** | 逐波判定：废弃 → `status=dropped`；仍有效 → 补跑 wave_gate。USA 2083 条中字段 0 命中的直接标 dropped | pending 池从 6100 → 真实规模，统计恢复可信 |
| P0-3 | **统一 wave 键约定** | 约定 `gate_results.wave` 与 `waves.wave_number` 同型（建议全字符串）；加启动时一致性校验（对不齐即 WARN） | 杜绝"门禁静默丢失"这一类 bug |
| P0-4 | **体检包纳入 git** | `git add tracking/mining/field_inspect_*.json`（148 个，纯 JSON 无敏感信息，先抽查 2–3 个确认） | 消除"git 视角 vs 磁盘视角"再次脱节 |

### P1 — 本周内（低配额，probe 先行）

| # | 改进项 | 动作 | 预期收益 |
|---|---|---|---|
| P1-1 | **prod-first 闸前移到 S2 生成层** | GEM 生成时即查询 `search_alphas_by_sharpe(region, 1.58)` 排除饱和族字段（USA 提示词已有此设计，推广为骨架默认；IND 尤其急需） | 回测配额不再浪费在必死表达式上，IND 类"48% 达标 0 提交"直接止血 |
| P1-2 | **IND 停手或转向** | IND 现有 94 达标全灭于 prod/CW——要么暂停 IND 回测，要么只跑与存量 IS 相关性低的新字段族（event/earnings 细分） | 释放并发槽给 GLB/HKG |
| P1-3 | **GLB 突围按提示词 Phase 0 落地** | 先跑 P0.1 引擎 dry_run 验收（零副作用）→ P0.2 CLI 干跑看 gate 通过率 → ≤8 探针实跑拿转化率，转化率>0 才铺量 | 避免在 42 颗全灭的旧字段族上重复消耗 |
| P1-4 | **HKG 启动前先建体检包** | probe-only 第一动作 = 为候选数据集生成 field_inspect（现在 HKG 0 包），再走两阶段 A/B | 覆盖 HKG"档位未实测"风险 |

### P2 — 卫生项（顺手做）

| # | 改进项 | 动作 |
|---|---|---|
| P2-1 | 波次 TTL 回收 | wave 状态机加"pending 超 7 天 → 标 stale + 告警"，杜绝无声积压 |
| P2-2 | 工具名映射表 | 在 SKILL.md 附录维护"逻辑名 ↔ MCP 注册名 ↔ 模块"三列映射，防再漂移 |
| P2-3 | 孤儿表达式字段核验 | 对 pending 池全部字段跑一次 fields 表存在性核验（复用 USA token 核验逻辑），不存在即标 dropped |

### 建议执行顺序

```
P0-1 → P0-2 → P0-4 → P0-3   （一轮本地清理，半天内完成，零配额）
        ↓
P1-3 GLB Phase 0 dry-run（验证链路修复后真实转化率）
        ↓
P1-1 prod-first 前移改造 → P1-2 IND 决策 → P1-4 HKG 启动
```

---

## 5. 第一轮执行记录（2026-09-07 21:55，commit 59406fe）

1. ✅ **已执行** 修改 SKILL.md（D1/D2/D3 三处文档修复）+ 附录工具名映射表 22 项
2. ✅ **已执行** 裁决孤儿积压：18 个废弃波 dropped、50 条无效表达式清出（w164 波保留 34 条有效）；备份 `data/wqb.db.bak_orphan_fix_20260907`
3. ✅ **已执行** 148 体检包 `git add`（全量敏感扫描通过，2 处命中为字段名误命中：`max_token_length`/`tradesecrets`）
4. ✅ **已执行** wave 键约定统一：`wave_gate.py --wave` 改字符串、`ensure_schema` 增 wave-key-check + wave-ttl-check、3 项回归测试
5. ✅ **已执行** P1-1 PROD 饱和闸前移：`tools/prod_saturation_gate.py` 三态闸 + wave_gate 集成（IND 实测 5 个饱和字段识别正确）
6. ✅ **已执行** P1-3 GLB Phase 0：七节点 dry-run 6/7 success；CLI 干跑 `s2_intraday_pv_feats_d1` 40/40 PASS——**字符串波号首次走完门禁全链并落库**
7. ✅ **已执行** P2-1 波次 TTL：超 7 天 stale WARN（310 波/4458 条积压可见）
8. 测试终态：**481 passed**（478 基线 + 3 新增）；sync_skills 同步后漂移测试转绿

---

## 6. 追加执行（2026-09-07 22:30，commit 22f107f）

**P1-4 HKG 阻塞解除（降级方案）**：WebDataScope zip 虽无 HKG 包，但 DB fields 表自带 HKG coverage（25648 字段）→ 新增 `tools/gen_inspect_from_db.py` 生成 **172 个降级体检包**（coverage-only，skew/kurt 置 None 自动跳过对应闸）；修复 `webdata_quality.py` 的 `abs(None)` 崩溃。端到端验证：低覆盖 0.27 字段裸用 FAIL、加 ts_backfill 转 PASS。HKG 体检硬门从 0 包 → 172 数据集可用（完整形状统计仍需 WebDataScope HKG 包，到位后 `gen_field_inspect_packs.py --region HKG` 会覆盖降级版）。

**P0-2c REGATE 波补门禁（13 波全部落库）**：2/13 全闸 PASS（USA reg_mf01、KOR 146）；11 波 FAIL 属正常拦截——**PROD 饱和闸首战告捷**：IND wallbreak 6/8 条命中饱和字段被拦（`residualized_return_india_top500_equity` 等正是"94 达标 0 可提交"的元凶字段），MEA w100 拦 2 条。wave-key-check WARN 从 217 波/4357 条 → **208 波/3988 条**（剩余为 KEEP 态 ws2 存量波，属正式战役推进节奏，不机械刷）。

## 7. P1-2 IND 转向决策依据（供拍板）

| 指标 | 数值 | 含义 |
|---|---|---|
| S≥1.58 总量 | 104 条 | 产量最高区域 |
| prod_corr 实测撞墙 | 9 条 | 撞墙率 36%（9/29 已测） |
| **prod_corr 未测（NULL）** | **75 条** | 主体为 model135 字段族（mdl135_d3/d5_isr/icc），**不是撞墙是未测** |
| dataset 归属 | 84 条挂 `_unknown`（dataset_id=41 桶） | 历史灌库时未解析数据集归属 |

### 7.1 未测 75 条风险定级（2026-09-02 本地分析）

用字段画像交叉对照（已测 29 条的 wall/pass 字段命中）定级：**LOW 30 / MED 40 / HIGH 5**。
- HIGH 5：命中确认饱和字段（`mdl135_d04_icc` ×4、`mdl238_global_rank` ×1）——预计直接撞墙。
- MED 40：model135 族 42 条（族内已测 2 撞墙/1 通过）+ `oth315_execution_timestamp` mixed（2 撞墙/1 通过）+ 表达式截断 13 条（DB 存储不完整）。
- LOW 30：全干净字段（`change_6m_rating_revision` 18 / `residualized_return_india_top500_equity` 14 / `alternative_market_cap_usd` 11）。
- 附注：已测通过 20 条**全部已 ACTIVE**（含 kqjpwYez pc=0.700 贴线、residualized 字段已被 5 条 ACTIVE 占用）；`WjPjXARx` 实为 SUPER 占位记录非 REGULAR。

### 7.2 真实平台补测（2026-09-07 启动，2026-09-08 完成）

**通道确认**：`world-quant-brain-mcp/.env` 凭证可用，`BrainApiClient.check_correlation(alpha_id, "production")` 真实平台调用，30s/条出结果，7 天缓存。

**全量终态（75 条全部已决，0 pending）**：

| 判定 | 数量 | 说明 |
|---|---|---|
| WALL（PC≥0.7） | **67** | 撞墙率 89%（67/75），PC 范围 0.7117–0.9958 |
| PASS（PC<0.7） | **8** | 其中 1 条为 SUPER 占位（WjPjXARx），**真实可提交 7 条** |

**7 条真实可提交候选（已写回 DB）**：mLjnnzKE (S=2.90, PC=0.5951)、xAj77zlg (S=2.75, PC=0.6860)、vRj7arVw (S=2.59, PC=0.4616)、blj0mgPK (S=2.54, PC=0.5892)、1Yw33mO6 (S=2.26, PC=0.5496)、1Yw36X56 (S=2.08, PC=0.3638)、xAj7LMXb (S=1.72, PC=0.5427)。

**IND 104 条 S≥1.58 终局**：104 已测 = 76 WALL + 28 PASS（20 ACTIVE + 7 可提交未提交 + 1 SUPER 占位）。

**结论（P1-2 决策）**：IND 并非全灭——**7 条真实可提交候选浮出水面**，且 PC 余量充足（最低 0.3638）。但撞墙率 89% 证实主流方向（model135/analyst/residualized/market cap）已信号级饱和。**决策建议：① 7 条候选走 submit_verdict 判定链后择优提交；② 新挖方向避开饱和字段族，向已 ACTIVE 的冷门数据集（pv106/transaction_cost/anl9/oth696/fnd86/mdl177）靠拢**。

**工具沉淀**：`tools/backfill_prod_corr.py`（checkpoint 续跑 + busy/pending 重试 + --risk 分组 + --apply-db 写回门控）；DB 备份 `wqb.db.bak_backfillpc_20260908_134616`。

1. ✅ **已执行** 修改 SKILL.md（D1/D2/D3 三处文档修复）+ 附录工具名映射表 22 项
2. ✅ **已执行** 裁决孤儿积压：18 个废弃波 dropped、50 条无效表达式清出（w164 波保留 34 条有效）；备份 `data/wqb.db.bak_orphan_fix_20260907`
3. ✅ **已执行** 148 体检包 `git add`（全量敏感扫描通过，2 处命中为字段名误命中：`max_token_length`/`tradesecrets`）
4. ✅ **已执行** wave 键约定统一：`wave_gate.py --wave` 改字符串、`ensure_schema` 增 wave-key-check（实测暴露 217 波/4357 条断链）+ wave-ttl-check（310 波/4458 条 stale 可见）、3 项回归测试
5. ✅ **已执行** P1-1 PROD 饱和闸前移：`tools/prod_saturation_gate.py` 三态闸 + wave_gate 集成（IND 实测 5 个饱和字段识别正确）
6. ✅ **已执行** P1-3 GLB Phase 0：七节点 dry-run 6/7 success（superalpha 空组件为预期业务拦截）；CLI 干跑 `s2_intraday_pv_feats_d1` 40/40 PASS——**字符串波号首次走完门禁全链并落库**
7. ⚠️ **P1-4 HKG 阻塞**：当前 WebDataScope zip 无 HKG 数据包（9 区域组合：ASI/CHN/EUR/GLB/JPN/KOR/USA，无 HKG）——需先下载 HKG WebDataScope 包，工具链 `gen_field_inspect_packs.py --region HKG` 已就绪
8. 测试终态：**481 passed**（478 基线 + 3 新增 wave-key 契约测试）；sync_skills 同步后漂移测试转绿

---

*审计方法备注：本报告全部结论基于 2026-09-07 的磁盘/DB 实时状态（pytest 478 passed 基线、wqb.db 09-07 P0-P2 修复后版本），关键断言均附可复现 SQL/命令于会话记录中。*
