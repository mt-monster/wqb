# WQ/BRAIN Skills 评估与整改报告（现行唯一版本）

> 日期：2026-08-23 ｜ 范围：全部 skills 副本、`data/wqb.db`、`tools/`、`docs/experience/`、`tracking/`
> 本文取代此前 8 份分散且结论互相矛盾的 skills 审计（已归档 `attic/reports_archive/2026-08-23-superseded/`）。
> **后续任何 skills 审计只更新本文，不要再新建报告文件。**

---

## 0. 结论摘要

skills 的方法论内容质量高且经过实证（L0–L7 分层、七阶段流水线、闸门阶梯、平台禁用项均正确），
问题集中在**事实源不唯一**与**经验闭环单向**两处：

| # | 问题 | 实测证据 | 严重度 | 状态 |
|---|---|---|---|---|
| 1 | 4 套 skills 副本并存、交叉漂移，无一套全面最新 | 19 个共有 skill md5 **100% 不同**；`campaign.py` 2 个实现 4 份拷贝 | P0 | 已修 |
| 2 | 学习闭环计数不对称，规则无法自校准 | `times_applied` 恒为 0 而 `times_succeeded` 已到 8，成功率算不出来 | P0 | 已修 |
| 3 | RA 无端到端 SOP，篇幅被 PPA/SUPER 挤占 | RA 命中 42 次 vs PPA 73 次；命中 RA 最多的是 SUPER skill | P1 | 已修 |
| 4 | 波次结论可以留空，S6→S-PRE 闭环形同虚设 | 133 条 wave 记录 97 条 verdict 为空，EUR/GBR/HKG/ASI 四区全空 | P1 | 已修 |
| 5 | skills 与 AGENTS.md 工具化纪律脱节 | `tools/` 六大工具在权威套 skills 中 0 引用 | P2 | 已修 |

> **关于本报告的一处方法论更正**：初次评估的多项"缺失"结论是在**项目级已归档副本**上统计得出的
> （`grep` 默认跳过隐藏目录，加之权威套位于用户目录 `~/.qoder-cn/skills`，不在项目 grep 范围内）。
> 逐项复核后，以下四条**不成立**，权威套本就正确，此处更正以免误导后续工作：
>
> | 初次结论 | 实际情况 |
> |---|---|
> | 「`wq-backtest-monitor` 全文 0 次提及回写，S6→S-PRE 断裂」 | 权威套第 151 行起就有完整 §14 台账回写章节；断裂的是旧副本 |
> | 「`methodology_rules.json` 无任何消费方，`times_applied` 恒为 0」 | `toolkit/_lib/rules.py` 是完整的四层闭环实现（L1 采集/L2 存储/L3 消费/L4 验证），`gate.py`/`build_wave.py`/`diversity_audit.py` 均已接入；真实缺口只是 `times_applied` 不递增 |
> | 「`cross_region_lessons` 被 0 个 skill 引用」 | `wq-brain-campaign-matrix` 的查表工具清单里就有 `get_cross_region_lessons()` |
> | 「Sharpe 门槛并存 1.58/1.5/1.28/1.1 四个取值」 | 权威套中多为正则误报（把实测值 2.89、子宇宙系数 0.75、CV_Sharpe 0.40、错误码 429 当成阈值）；真实口径冲突只有 `brain-alpha-orchestrator` 的旧串行并发模型一处 |
>
> 教训：审计 skills 必须显式指定权威套路径，`rg` 要带 `--hidden --no-ignore`，
> 否则会把"我没搜到"当成"它不存在"。

**不应改动的资产**（经逐条核对正确，任何重构须原样保留）：
`combination(alpha(...))` 已禁用改用 selection+combo；`prod_correlation` 在 selection 可用而 combo 报
unknown variable；SUBINDUSTRY 中性化是 SUPER 组合层降 prod-corr 的杠杆而对单 alpha 无效；五槽填槽并发模式。

---

## 1. 副本单源化（P0）

### 整改前实测

| 副本 | skill 数 | 最新修改 | 有 last_verified | 接入 wqb.db |
|---|---|---|---|---|
| `~/.qoder-cn/skills` | 27 | 08-23 15:51 | 27/27 | 9 |
| `<wqb>/.workbuddy/skills/_unpacked_brain` | 35 | 08-23 15:51 | 8/35 | 7 |
| `~/.workbuddy/skills` | 31 | 08-22 22:42 | 27/31 | 5 |
| `<wqb>/.qoder-cn/skills/_unpacked_wq` | 26 | 08-17 02:06 | 0/26 | 0 |
| `world-quant-brain-mcp/.venv/.../cnhkmcp/untracked/skills` | 20 | 第三方包内 | — | 0 |

关键佐证：项目级 `.workbuddy` 套虽整体最新，但 `wq-backtest-monitor` 指纹与最旧的项目级
`.qoder-cn` 套完全相同（159 行），而两套用户级副本已到 160/161 行——**没有任何一套可整体信任**。

### 已执行

1. 确立 `~/.qoder-cn/skills` 为唯一权威（25/35 最优版本所在）。
2. 合并 6 个缺失/落后 skill：`alpha-template-labs-data-analysis`、`brain-alpha-orchestrator`、
   `brain-alpha-repair`、`brain-alpha-research`（新增）、`brain-alpha-robustness`、`planning-with-files`（更新）。
   复制时跳过 32 处 `<skill>/<skill>/` 同名嵌套重复目录。
3. 项目级两套归档至 `attic/skills_archive/2026-08-23-pre-consolidation/`；
   改动前全量备份权威套至同目录 `user-qoder-cn/`（840 文件 / 6.3 MB）。
4. `INDEX.md` 增「唯一权威副本」章节，列明五处副本的处置与调用禁令。

### 引用与路径修复

合并后 `validate_skills.py` 暴露 38 个错误，全部修复至 **0 错误**：

- 相对路径：`../../../src/` → `src/` 等 6 类重写（解包多出一层目录导致的悬空引用）。
- frontmatter：4 个 skill 补 `layer` + `allowed-tools`，`planning-with-files` 补 `layer`。
- 废弃路径：`.qoder/skills/` → `.qoder-cn/skills/`。
- 硬编码绝对路径 **10 处 → 0 处**：改用 `$WQ_PY` / `$WQ_TOOLKIT_DIR` / `$WQ_VALIDATOR_DIR` / `<SKILL_ROOT>` 或项目根相对写法。
- `tools/gate.py`、`tools/wave_gate.py` 删除失效的 `.cursor/skills/` 候选路径；
  `tools/skills_audit_linkcheck.py`（功能与 `validate_skills.py` 重叠且指向 venv 僵尸副本）归档。
- `validate_skills.py` 的 `WQ_PROJECT_ROOT` 改为读环境变量并回退，新增 `L-RA` 合法分层。

---

## 2. 数据库经验现状（P0/P2 依据）

`data/wqb.db` 实测行数：

| 表 | 行数 | 说明 |
|---|---|---|
| `ledger_kv` | 474 | 战役台账，KOR 占 334（70%） |
| `wave_results` | 133 | 波级复盘；**97 条 verdict 为空** |
| `registry_empirical` | 106 | dead_end/win/campaign/orphan；KOR 66（62%） |
| `fields` / `expressions` / `datasets` / `alphas` | 1124 / 516 / 40 / 63 | 资产与历史 |
| `cross_region_lessons` | 3 | 跨区铁律，严重偏少 |
| `operators` / `submissions` / `diversity_evaluations` / `expression_operators` / `campaign_states` | 全 0 | schema 已建但从未写入 |

verdict 空值分布：EUR 30/30、ASI 15/15、GBR 12/12、HKG 11/11 全空，仅 KOR/IND/MEA 有结论。

`tracking/<REGION>/reference/methodology_rules.json` 具备完整学习闭环 schema
（trigger/action/evidence/confidence/times_applied/times_succeeded/expires_after_batches），
消费实现是 `toolkit/_lib/rules.py`（L1 采集 → L2 存储 → L3 消费 → L4 验证四层，
`gate.py` 闸6、`build_wave.py`、`diversity_audit.py` 已接入）。

**真实缺口是计数不对称**：`consume_contract` 只把批次哈希记入 `consumed_batches` 而不递增
`times_applied`，`validate_rules` 只递增 `times_succeeded` 且只覆盖 `universe_lever`/`dilution`
两类规则。结果是 IND 出现 `times_applied=0, times_succeeded=8`，KOR 出现
`consumed_batches` 8 条而 `times_applied=0`——成功率分母为 0，`confidence` 无法按成功率自校准。

---

## 3. 链路衔接（P1 依据）

### 接缝检查

| 接缝 | 整改前状态 |
|---|---|
| S6 → S-PRE 回写 | **约定完整但无强制力**：backtest-monitor §14 写明了回写四步，但 `wave_results.verdict` 允许留空，导致四个区域 68 条记录有数据无结论 |
| S2 → S3 产物 | **含糊**：`*_idea_*.json` 与 `final_expressions.json` 两条产物路径并存 |
| S4 改进入口 | **三头**：optimization-v1 / alpha-repair / how-to-pass-AlphaTest |
| S-PRE 查表、S3 并发 | 通畅 |

### 职责重叠

| 层 | 竞争者 | 处置 |
|---|---|---|
| 编排 | brain-deepExplore（330 行，接 DB）vs brain-alpha-orchestrator（89 行，零 DB） | INDEX 标注 orchestrator 待并入，禁止新增引用 |
| 评审 | brain-alpha-judge vs brain-alpha-robustness | robustness 定位为 S4→S5 必经稳健性闸，judge 保持 S5 唯一评审入口 |
| 改进 | optimization-v1 vs alpha-repair vs how-to-pass | optimization-v1 为唯一改进入口，repair 降级为修复配方 |
| 战役引擎 | campaign-toolkit vs ppa-mining vs superalpha | toolkit 提供原语，后两者只做领域编排 |

### 阈值口径

逐行复核后，权威套中绝大多数"分歧"是正则误报（实测值、子宇宙系数、CV 阈值、错误码 429）。
唯一真实冲突：`brain-alpha-orchestrator` §2.5 写「batch 间客户端纯串行 for 循环」，
属 2026-08-16 前的旧模型，与现行五槽填槽矛盾。已在该节标注废弃并指向 `CONCURRENCY` 单源。

---

## 5. 整改执行记录

### P1 — RA 主链路

| 动作 | 落地 |
|---|---|
| 新建 `wq-brain-ra-pipeline`（L-RA 层） | region 为唯一输入的九步 SOP，每步含目的/命令/产物/失败分支；含循环停止闸与 5 条反模式。INDEX 新增 L-RA 分层，`validate_skills.py` 的 `VALID_LAYERS` 同步加 `L-RA` |
| `wq-backtest-monitor` §14 补强 | 新增 14.1 verdict 必填硬约束、14.2 命令模板、第 4 条方法论规则计数回写 |
| 阈值单源化 | `src/wqb/config.py` 新增 `GATES_INTERNAL` / `GATES_PLATFORM` / `GATES` / `CONCURRENCY` / `gate_thresholds()`；INDEX 闸门阶梯段标注数字唯一来源 |
| 六工具写进 skill | `brain-simAlphasinBatch-and-track`、`worldquant-submit-alpha`、`wq-brain-superalpha`、`wq-brain-campaign-toolkit` 各加「工具化纪律」节，引用数 0 → 每工具 2–3 个 skill |

### P2 — 经验闭环

| 动作 | 落地 |
|---|---|
| 修复计数不对称 | `consume_contract` 新 digest 时 `times_applied += 1`；`check_universe_lever` 拦截生效时 +1；`reconcile_contract_landing` 全项落地时 `times_succeeded += 1`（此前 explore_contract 成功率恒为 0）；新增 `rule_success_rate()` |
| 回填历史计数 | 6 个区域规则对齐：KOR 0→8、IND 0→8、USA 0→2、GBR/MEA 0→1。现可算出成功率：EUR/IND/USA 100%，KOR/GBR/MEA 0% |
| verdict 强制 | `wave_results.upsert()` 加硬校验：`status=closed` 必须带非空 verdict，否则 `SystemExit`；未定则用 `--status open`。已冒烟验证拒绝与放行两条路径 |
| 跨区教训扩充 | `cross_region_lessons` 3 → 10 条，从四区 49 条 dead_end + 9 条 win 提炼出 7 条跨区复现模式（详见下） |
| 空表状态标注 | `database/DATABASE_SUMMARY.md` 新增 §10：区分在用 11 张与未启用 5 张，逐表说明为何不用及正确的替代通道 |
| 断链工具归档 | `tools/sync_operators_from_catalog.py` 写的 `src/wqb/operators/` 在 `src/wqb` 重建后已不存在，归档 `attic/tools_archive/` |

新增的 7 条跨区铁律：

| lesson_id | 一句话 |
|---|---|
| `PRODCORR-SATURATION-UNIVERSAL` | 四区独立复现：已饱和风格的新提交 IS 全过但 prod_corr>0.7 被拒，只能换信号族 |
| `PRODCORR-LOCAL-UNDERESTIMATES` | 本地自算 prod_corr 系统性低估平台值（MEA 实测 0.612 vs 0.7723），只能作粗筛 |
| `SINGLE-FIELD-PROBE-CEILING` | 新数据集单字段首探天花板稳定在 0.2–0.52，全 RED 不足以判死，须再跑复合结构 |
| `SPARSE-EVENT-CONCENTRATED-WEIGHT` | 稀疏事件流必被 CONCENTRATED_WEIGHT 挡，须先 `ts_backfill` + `trade_when` |
| `SELF-CORR-FAMILY-CANNIBALISM` | 已有 ACTIVE 后同骨架变体 IS 越好自相关越高，默认判死 |
| `SLOW-X-FAST-MIX-RECIPE` | 慢变量 × 短周期低相关混合是已验证胜绩配方；同周期互混全灭 |
| `SCALE-NEG-RANK-ROBUST-SYNTAX` | `scale(-rank(x))` 过 robust 闸，`scale(reverse(rank(x)))` 不过——平台语法级效应 |

### P3 — 结构清理

| 动作 | 落地 |
|---|---|
| 嵌套重复目录 | 权威套实测 **0 个**同名嵌套目录（32 个只存在于已归档的项目级副本，合并时已跳过）；保留的 2 个嵌套 SKILL.md 是 headless runner 运行时依赖，按 INDEX 声明不动 |
| frontmatter | 34 个 SKILL.md 全部通过 `validate_skills.py` 九项检查，0 错误 0 警告 |
| 重叠 skill 定位 | `brain-alpha-orchestrator` / `brain-alpha-repair` / `brain-alpha-robustness` 各加「定位声明」，明确唯一入口归属；保留内容不做破坏性合并 |
| 非 WQ skill | `gold-analysis` / `jin10-news` / `code-optimization` / `dead-code-cleanup` 确认未进权威套，32 个 skill 全为 WQ 域 |

### 回归验证

| 项 | 结果 |
|---|---|
| 根 `tests/` | **264 passed** |
| `world-quant-brain-mcp/tests/` | **37 passed** |
| toolkit `scripts/` 测试 | **65 passed** |
| `validate_skills.py` | 34 文件，**0 错误 0 警告**（整改前 38 错误） |
| 硬编码绝对路径扫描 | **0 处**（整改前 10 处） |
| `tools/wave_gate.py` 真实冒烟 | KOR wave135 语法 8/8 PASS，5 闸执行并落盘 JSON + out.txt（exit 1 为业务判定 FAIL，非工具故障） |
| verdict 强制冒烟 | 无 verdict 的 `status=closed` 被拒；带 verdict 正常通过 |

数据库改动前已备份至 `logs/wqb.db.bak-20260823-174319`（1.75 MB），
权威套改动前全量备份至 `attic/skills_archive/2026-08-23-pre-consolidation/user-qoder-cn/`。

---

## 4. 复现方式

本报告的全部实测数字可由以下脚本复跑（位于 `logs/`，UTF-8，走 MCP venv）：

| 脚本 | 产出 |
|---|---|
| `_tmp_skill_scan.py` | 两套副本元数据、引用关键词统计、版本漂移 |
| `_tmp_skill_copies.py` | 4 套副本规模/指纹/DB 接入度对比 |
| `_tmp_skill_ra.py` | RA/PPA/SUPER 篇幅分布、阈值分歧、S6 闭环核查、DB 经验分布 |
| `_tmp_merge_plan.py` | 逐 skill 最优版本判定与合并计划 |
| `_tmp_db_probe.py` | `data/wqb.db` 全表行数与列结构 |

质量门禁：`python <SKILL_ROOT>/validate_skills.py`（exit 1 即禁止发布）。
