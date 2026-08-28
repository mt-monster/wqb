# WQ/BRAIN 挖掘 Skills 调用链可复查清单（2026-08-24）

> 依据：`C:\Users\MENGTAO\.qoder-cn\skills\INDEX.md` + `wq-brain-ra-pipeline`（唯一编排 SOP）+ `wq-brain-campaign-toolkit`（引擎）。本清单用于复查链路的**产物接续 / 闸门顺序 / 台账回写字段**三者是否落地。任一步 FAIL 就地回退，不允许跳过继续。

## 0. 总览：一套三层协作 + 一条七阶段主链

| 角色 | 技能 | 回答的问题 |
|---|---|---|
| 编排 when/what | `wq-brain-ra-pipeline`（唯一入口） | 何时挖、挖什么、走哪些步 |
| 查表 where | `wq-brain-campaign-matrix` | 在哪个区域、挖哪些数据集 |
| 引擎 how | `wq-brain-campaign-toolkit` | 战役目录内每个子命令的唯一权威实现 |

`brain-alpha-orchestrator` 为编排层旧稿（**勿新增引用**）；`brain-deepExplore` 已废止并入 ra-pipeline（**再 invoke 视为反模式**）。

---

## 1. 主链九步：产物格式 · 闸门顺序 · 回写字段

| 步 | 阶段 | 入口 skill / 命令 | 产物（格式） | 闸门/约束 | 失败分支 | 台账回写 |
|---|---|---|---|---|---|---|
| 1 | S-PRE | `campaign-matrix`；`mcp__wqb-db__get_campaign_summary/get_dead_ends/get_dead_datasets/get_cross_region_lessons` + `campaign.py registry list` | 配置包：universe / delay / 中性化 / 排除集 / 排除信号族 / 当前波号 | 不做挖掘，只查表 | registry 全空→进步2+步9建 campaign；候选覆盖→转 nextMove 选新区 | — |
| 2 | S0 | `campaign.py score`（权威）；跨区试探才用 `script/dataset_health_check.py` | ledger `s0_ranking` + `s0_whitelist` | 体检硬门 cov≥0.85 / α≤50 / f≥10；白名单≥2 非 MODEL；`category_weight` 0.9–1.15；锁白名单必须 `upsert_ledger_key(region,"s0_whitelist")` | 无非 MODEL→不退回纯 MODEL；全排除→回步1 | ledger `s0_ranking` / `s0_whitelist` / `*_dead` |
| 3 | S1 | `campaign.py scan-fields` + 字段理解（`brain-data-feature-engineering` ideas 回写 `s1_<ds>_d<delay>`） | `fields` 表（typed catalog）+ ledger S1 决策 + ideas.md 路径 | 字段数≥10；VECTOR 用 get_datafields 确认 `--data-type` | 字段<10→退回步2 白名单外 | ledger `s1_<ds>_d<delay>`（source=standalone） |
| 4 | S2 | `brain-makeSomeGem`（**强制**，headless_runner）+ `campaign.py build-wave` + `brain-enhance-template` | `expressions` status=`gem`/`enhanced`（DB 入库，禁止把 GEM `final_expressions.json` 当真相源） | GEM 概念优先：机制→2–3 字段→Implementation Example，禁"每字段套 rank"；必须 `--priors-file`；先读 win 层换腿 | GEM 未入库→按超时清单查任务，确认才回退 | ledger idea；表达式入库 |
| 5 | S2→S3 | `tools/wave_gate.py`（一键落盘，非手写 `_gate_waveNN.py`） | `gate_results`（DB）+ gate 落盘 | 5 闸：语法/字段白名单/`vec_*` 包裹/`ts_min,ts_max` 禁/VECTOR `--fix`；多样性闸；闸2 跨集 | 语法 FAIL 先修；多样性 FAIL→步4 补骨架；闸2→拆腿对照不停挖 | gate 结果入库 |
| 6 | S3 | `campaign.py pipeline`（可经 `brain-simAlphasinBatch-and-track` 调）+ `tools/batch_status.py --watch` | `backtest_results` + `wave_results` + checkpoint `ckpt_w<W>` | 五槽填槽（`wqb-concurrency` §8 唯一来源）；弱探针≤1 槽；prod-first：先 1–2 骨架查 `prod_corr`，≥0.7 停扩换腿 | 整批 CANCELLED→回步5；429→≤6 并发、批间≥45s | 回测结果+wave_results |
| 7 | S4 | `campaign.py review` → `how-to-pass` → `optimization-v1`（Mode B 70%→Mode A 30%），按需 `selfcorrQuick`/`explain-alphas`/`enhance-template` | review 诊断 + ranking | prod_corr≥0.7→Mode B 换概念；同一想法>10 结构仍不过→写 dead_end | 均通向：同想法仍卡→步9 `dead_end`，回步2 | ledger `review_<tag>` |
| 8 | S4→S5 | `brain-alpha-robustness`（**必经闸**）→ `brain-alpha-judge`（双闸评审）；403 盲区用 `tools/submit_verdict.py` | verdict READY / BLOCK（judge 只报告，**等用户确认**） | PASS_CHEAP≠可提交；PROD/SELF 不过→回步7；配额按最早提交+48h | READY→`submit-alpha`/`superalpha`；BLOCK→回步7 Mode B | —（提交动作由 S5 技能触发） |
| 9 | S6 | `wq-backtest-monitor` §14 + `campaign.py wave upsert` / `registry add-dead-end` / `add-win` / `ledger set-verdict` | `wave_results.verdict` + `registry_empirical`（回写才视为本波完成） | OS ACTIVE / 全闸 PASS 必须 `add-win`（mix 比例、中性化、decay、快/慢腿） | 未回写=本波未完成 | `wave_results.verdict` + `registry_empirical` + ledger |

> 命令详解与参数见 `wq-brain-campaign-toolkit` §5–§8；本题只列"可复查的接续点"，不重复实现引擎逻辑。

---

## 2. 三角分工与引擎委派（勿重复实现）

- `ra-pipeline` / `matrix` / `toolkit` 是唯一三力；任何方法论 skill 指向 toolkit，**禁止复制 scripts/ 逻辑**（违反 = 第二权威实现，反模式）。
- `brain-simAlphasinBatch-and-track` 是 S3 经 subprocess 调 toolkit 的**唯一运行时调用方**；`backtest-monitor` S6 经 `campaign.py ledger` 幂等回写。

---

## 3. 三个关键循环/停止闸

1. **S6→S-PRE 闭环**：复盘必须回写 `registry_empirical`，否则下次查表读不到实证，链不闭合。
2. **BLOCK 回退循环**：S5 BLOCK（prod_corr≥0.7 等）→ 回 S4 Mode B 换概念，≤3–5 轮仍卡→换字段/数据集（S0 重新体检）。
3. **日循环/停止**：连续 3 波全 FAIL 且无新 dead_end → region 暂停转 nextMove；白名单被 dead_end 全覆盖→停止；ACTIVE RA≥10→可转 superalpha。

---

## 4. 复查方式（任一侧改动后跑）

- 口径一致性：`validate_skills.py` 应 **0 错 0 警**（当前 2 个 layer 口径 ERROR 待修，见报告）。
- 产物接续：按上表"产物列"逐格核对本步是否真实产出、是否被下一步消费。
- 求一致三副本：`.qoder-cn` / `.trae-cn` / `.workbuddy` 同文件 MD5 一致。