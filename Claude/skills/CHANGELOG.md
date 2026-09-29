# Skills 变更日志

> 从各 SKILL.md 正文里迁出的「日期 / 新增 / 修正 / 事故」叙述。**规则在 SKILL.md 与 `references/`；日期与变更在这里。**
> 约定：新条目加在最上面；一条一行：`日期 · skill · 改了什么（为什么） → 证据 / 落点`。事故与起因写进对应 skill 的 `references/incidents.md`，这里只留指针。
> 决策与证据登记：[`docs/skills_review_decisions.md`](../../docs/skills_review_decisions.md)；逐条处置：`reports/skills_review_20260929_closure.md`。

## 2026-09-29 · skills 审查整改（`reports/skills_review_20260929.md`）

**wq-brain-ra-pipeline v3.0（重构）**
- 核心 `SKILL.md` 由 950 行 → 约 220 行：每步固定模板（目的 / 前置 / 调用 / 产物 / 完成定义 / 失败分支 / 不做 / 细则）；细则、事故、情景卡拆到 `references/`（`step1`–`step9`、`loop-and-stop`、`forum-recon-triggers`、`ppa-vs-ra`、`tool-index`、`scenarios`、`incidents`）→ RA-10 / RA-103 / RA-117
- `assemble-priors-internals.md` **按代码重写**：旧文写的「`GLOBAL/region_kb.templates[]` → wins」「`methodology[]` → region_context」代码里都没有，真正承载 S6 回写的 `registry_empirical` win / dead_end 层旧文一个字没提 → RA-50
- 新增 S6→S0 饱和反馈写入口 `campaign_intel.py mark-saturated`（`saturated_datasets` 此前全仓库只有读取方）；`submit_ready_blocked` 降为 deprecated → RA-113 / IX-20（`tests/unit/test_campaign_intel_mark_saturated.py`）
- 「提交类节点不入链」由代码强制：`execute_chain` 拒绝带 `confirm_submit=True` 的 `submit_alpha` / `superalpha` → RA-116 / X-9（`tests/unit/test_workflow_chain_irreversible_guard.py`）
- prod 墙处置只剩决策表 D0-P 一张；`prod-corr-avoidance.md` 改写为 prod 总纲，删除「POST / GET `/submit` 触发 prod 计算」的危险旧指令 → X-1 / RC-01 / RC-07
- 组合形态「允许清单」唯一一份（步 7 §7.7）；补「辅助腿入场三式」（条件 / 分组 / 残差）；`subtract` 价差须同源且有单一经济含义 → RA-89 / RA-90 / X-3
- 停止规则、放行、四道开波闸从一个 ≈2000 字的表格单元拆成 `loop-and-stop.md`（每条配缺省数字与数字例；旧文里「GBR 至 09-30」这类状态不再写）→ RA-117 / RA-118
- forum_recon 五个触发点并成一张表（额度以查出有效文章为标准、7 天缓存）→ RA-16 / RA-57 / RA-94
- 6 个 `tools/*.py`（`build_gate_prior_from_inventory` / `select_ra_basket` / `gen_field_inspect_packs` / `field_semantic_classify` / `wave_gate` / `sync_platform_alphas`）接入 `tools/_pyenv`：作为脚本运行时自动切到 MCP venv，文档里可写裸 `python`（skill_lint bare-python）→ RA-07 / X-14
- 词表：**信号族**（字段集合，prod-first 分组）与**骨架指纹**（前 2 个算子，闸 PF）分开定义；旧 GLOSSARY 把两者写反 → RA-68

**wq-brain-superalpha v2.0（重构）**
- 旧 SKILL 是按时间追加的日记（后文推翻前文而前文不改；**全文没有「怎么建 SUPER simulation」的调用**；`force=True` 的 MCP 路径绕过 prod 闸；「预检」其实是真提交）。改为核心 SKILL（入口表 + 不可逆动作块 + 判定优先级 + 步 0–4 固定模板 + 参数取值理由 + 验证清单）+ `references/`（`levers-and-evidence.md` 决策表与参数-指标对照、`cases.md` 四个案例、`scenarios.md` 四张情景卡）→ SP-01 ~ SP-19
- 由代码强制：`submit_alpha` 节点拒绝 `type == SUPER` 的 `confirm_submit=True`（SUPER 只走 `super_build.py submit`，内置 prod ≥ 0.7 闸）→ SP-13 / T0-4（`tests/unit/test_submit_alpha_super_guard.py`）
- `super_build.py`：`--neutralization` 无缺省；universe / delay 取自 `config.REGIONS` 并校验；新增 `--selection` / `--combo`（`workflow_superalpha` 的同名参数此前被静默忽略）→ SP-17 / T0-8
- MCP `set_alpha_properties`：允许只传 SUPER 的 selection / combo 描述（此前缺省 `descriptions` 一律报错）→ SP-06
- 区域状态（MEA 通道对 SUPER 已关闭）从 SKILL 移到 MEA profile；「现状计数」快照删除，改为 `sa_probe` 实时命令

**brain-alpha-judge（三职能重排 + 安全收口）**
- SKILL 由「两道硬闸 + 六步 + 确认后提交」的旧骨架重排为三职能（PPA 核对清单 / trend score / 点塔排序）；旧「提交语义（GBR 旧口径）」「确认规则」「提交路由」整节删除，点塔口径只留 submit-alpha 的 `quota-and-tower.md` §2 → JD-01 ~ JD-05、JD-15 / JD-16
- 代码：凭据只读进程环境变量（不读 `.env` / 明文文件）；LLM 只能收紧确定性判定；降级运行标记；`--alpha-id` 模式取平台三段式 description 补 rubric 必填证据字段；补 `test_judge_gates_match_config.py`（脚本注释早引用、文件并不存在）→ JD-07 / JD-09 / JD-10 / JD-13
- 更正：`quota-and-tower.md` 的分档「差 1–2 颗一次点亮」（与「差 2 颗」重叠，且差 2 颗一次提交仍差 1 颗）；RA 文档里 `WAIT_THEME_ROTATION` 「judge 用同名结果值」的说法（没有代码实现）
- 规划文档 `improvement-roadmap.md` / `future-improvement-guide.md` 归档到 `attic/judge_planning_docs_20260929/`

**brain-alpha-robustness（「必经闸」有了代码落点）**
- 判定写 ledger `robustness_<alpha_id>`，`submit_verdict`（CLI / MCP / 批量）读取：REJECT → BLOCKED，CONDITIONAL / 无记录只提示（新模块 `wqb.robustness_record`，键进 `docs/ledger_keys.json`，单测在 `tests/unit/test_submit_verdict_core.py`）→ RB-03 / T0-18
- Phase A 拆分：闸门只读 `references/techniques.md`，论坛新发现只作「提案」（E 节）；`forum_cache_builder` 缓存路径改仓库内 → RB-04 / RB-05
- 删除「提交探测协议」（逐个提交读 prodCorr，提交即真实动作）；判定表更正（子宇宙引平台相对公式、算子数降软标记、Margin 标经验线）→ RB-10 / RB-15
- `allowed-tools` +`mcp__wqb-db__*`（写台账所需，能力基线已人审登记）

**worldquant-submit-alpha / GLOSSARY / decision-table / INDEX 等（提交链单一叙述）**：见 `reports/skills_review_20260929_closure.md` 的 SB-* / X-1 / X-2 / X-4~6 条目。

**已迁出本日志的历史（原 RA `SKILL.md` 里的日期叙述，按时间倒序，仅留一行）**
- 2026-09-28 · 闸 SEM 落地（GEM 之前必做，缺台账 exit 2；KOR fundamental17 首波 49.4% 落在货币 / 汇率非信号字段）；组合形态加严（等权 `add(rank,rank)` 同罪，`equal_weight_leg_add`）；`s6_verdict_<wave>` 废止（结论唯一源 = `wave_results.verdict`）；`forum_recon` 接线；提交层「唯一权威」改为「否决权威」（`GET /alphas/{id}/submit` 恒 404）；RA 外壳脚本 `ralph_daily_loop.py` / `ralph_runner.py` 归档到 `attic/ra_pipeline_shell_20260928/`（零运行痕迹）；未编排增强节点 `alpha_booster` / `modeb_improve` 去留登记
- 2026-09-27 · `assemble-priors` 节点写 DB 快照（此前只重写文件，GEM 读到旧快照）；S6 完成定义补「再跑 assemble-priors」；verdict 判定表与 `upsert_wave_result` 合并语义；三道开波闸接入 `batch_track`；停止规则 B 窗口按波开始时刻取
- 2026-09-26 · 审计补入边：步 8 挂上执行 skill（`worldquant-submit-alpha` / `wq-brain-superalpha`）；提交响应四态表（3 颗候选因只轮询不补发悬空 > 24 h）
- 2026-09-25 · 闸 PF（骨架级 prod-first 前置硬门）落地
- 2026-09-23 · 停止规则按轴（region × dataset）改版：B1 同轴熔断 / B2 区级多轴停
- 2026-09-20 · IS→OS 衰减校准接线（`os_decay.py`；Spearman 仅 +0.086，不抬 IS 阈值）
- 2026-09-19 · prod-first 升硬门；near 池不收结构性死信号（`ROBUST_STRUCTURAL`）；已点亮塔不进白名单（用户定案）；产出率严格口径；IND pv103 同日提交教训
- 2026-09-17 · `step_funnel.py`；signal_floor 改 fail-closed；`webdatascope-failed-gates` 资格门
- 2026-09-15 · 设置层先验（settings prior）；`region_kb` 波后自动刷新；`RN_EXPOSURE` 接线；停止规则 / 积压闸 SQL 化
- 2026-09-13 · 加权混合全局禁令（「路线 A」；同时废止 `MINING.slow_fast_mix`——0.40 / 0.60 慢快配比，只留作 2026-09-13 之前的历史配方）；先沉降、再封存（`seal_dead_end`）
- 2026-09-11 · 整链执行纠正（不是「九步可整条交给 workflow_chain」）；`wave_gate` 节点
- 2026-09-09 · `s4-prescreen`、`pyramid`、收批压缩（`harvest_multisim_alphas`）
- 2026-09-08 · 库存盘点先于新挖；`risk_neutralized_sharpe` 硬规则
- 2026-09-06 · signal_floor 接线；`--concurrency` 不存在导致 S3 从未真跑的修复；产出率先验
- 2026-08-25 · 区域 Profile 路由落地；并发由 5 → 7（Token-Bucket C≈7）
- `brain-deepExplore` 已废止并入 ra-pipeline；其 S2-D / S2-M 概念已废，见步 4
