# WQ/BRAIN Skills 全量逐阶段审查报告

> **日期** 2026-09-29　**基线** `6003238`（= origin/main）　**性质** 只读审查（未改动任何 skill / 代码 / 台账）
> **范围** `Claude/skills/` 下 33 个 `SKILL.md` + `INDEX.md`，按“阶段（章节 / 步骤 / 相）”逐段评审，并抽读其 `references/`、`reference.md`、`examples`、区域 profile（抽样范围见附录 A）
> **评审维度** ① 书写逻辑是否清晰　② 职责划分是否明确　③ 边界界定是否清晰　④ 是否需要用具体情景/场景来规范表述，避免有价值的信息因表述模糊而被绕过或遗漏
> **配套证据** `reports/skills_review_20260929/check_skills.py`（可重跑的机械检查）与 `check_skills_output.txt`；关键论断均标注了对应的代码/配置核对（见各条“问题”列）

---

## 0. 执行摘要

### 0.1 一句话结论

**这套 skill 体系的“局部写法”有大量值得保留的范本，但作为“交给 agent 照着执行的 SOP”，当前的主要风险不是写得不够详细，而是同一件事被写了 N 遍且互相矛盾、状态机不可达、命令不可执行、不可逆动作缺护栏，以及叙事/快照/变更日志与规则混写。** 上一轮评审（2026-09-26）的 9 个 P0，三天后**完全关闭 0 个、部分关闭 3 个、未关闭 6 个**；而 33 个 skill 的 `last_verified` 全部是同一天（2026-09-28）的批量戳，恰好掩盖了这一点。

### 0.2 规模与方法

- **读了什么**：33 个 SKILL.md + INDEX.md 逐行通读；references / reference / examples / 区域 profile 抽读（篇幅大的如 forum-browse 的 9 个 references 只抽样，已在对应章节标明）。
- **怎么评**：每个 skill 拆成“阶段”（288 个），每个阶段一行**四维热力图**（🟢 清晰 / 🟡 有歧义或重复 / 🔴 会导致执行错误、矛盾或绕过；末列“需情景规范？”）；每个有问题的段落一条**编号问题**（位置 · 维度·级 · 问题 · 改进建议）。
- **严重度**：**P1** = 会造成执行错误 / 自相矛盾 / 被绕过 / 不可逆动作缺护栏；**P2** = 歧义、重复、口径漂移、缺产出位置；**P3** = 文风、笔误、可维护性。**🟢** = 值得模仿的范本（不计入问题）。
- **证据等级**：能对着代码/配置/实测验证的都验证了（例：`gate.py` 的三个检测器对 9 种表达式形态的实测、`submit_verdict` 状态机可达性、`quota_status.py` 与 `pipeline.py` 的配额实现差异、CLI 参数与 argparse 的逐条比对、`config.REGIONS` / `RA_CHECK_NAMES` / `CONCURRENCY` 与文档的比对）；无法验证的写成“未核实”。
- **未做**：没有修改任何 skill；没有调用 WQ 平台（MCP 服务在本会话因 Windows 绝对路径 ENOENT 未连接，这本身就是可移植性问题的实证，见 X-14）。

### 0.3 规模总览（按 skill）

**合计**：710 条编号条目 = **675 条问题（P1 286（42%）/ P2 286 / P3 103）** + 11 条情景规范建议 + 24 条纯范本；另有 48 条带 🟢 范本标记（含“范本 + 仍有问题”的混合条目）；288 个阶段中，热力图单元格 🔴 279（32%）/ 🟡 406（47%）/ 🟢 180（21%）；**208 个阶段（72%）建议补情景规范**。

| § | skill | 层 | SKILL.md 行 | P1 | P2 | P3 | 🟢 | P1/百行 | 阶段 | 🔴格 | 需情景阶段 |
|---:|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| [1](#s1) | `wq-brain-ra-pipeline` | L-RA | 950 | 76 | 89 | 32 | 7 | 8.0 | 20 | 27 | 17 |
| [2](#s2) | `wq-brain-campaign-matrix` | L-PRE | 143 | 11 | 8 | 5 | 0 | 7.7 | 11 | 18 | 9 |
| [3](#s3) | `wq-brain-campaign-toolkit` | L-TOOL | 354 | 30 | 24 | 11 | 4 | 8.5 | 15 | 19 | 9 |
| [4](#s4) | `brain-next-move-analysis` | L0 | 78 | 4 | 9 | 3 | 1 | 5.1 | 6 | 7 | 5 |
| [5](#s5) | `alpha-template-labs-data-analysis` | L0 | 98 | 1 | 5 | 2 | 1 | 1.0 | 5 | 4 | 3 |
| [6](#s6) | `brain-forum-browse` | L0 | 258 | 5 | 13 | 6 | 1 | 1.9 | 10 | 12 | 8 |
| [7](#s7) | `wq-brain-ppa-mining` | L0 | 321 | 17 | 4 | 3 | 3 | 5.3 | 13 | 17 | 9 |
| [8](#s8) | `brain-alpha-research` | L1 | 63 | 6 | 5 | 2 | 0 | 9.5 | 8 | 10 | 6 |
| [9](#s9) | `brain-alpha-research-field-quality` | L1 | 76 | 4 | 3 | 0 | 1 | 5.3 | 5 | 3 | 4 |
| [10](#s10) | `brain-alpha-research-news-sentiment` | L1 | 76 | 3 | 2 | 1 | 0 | 3.9 | 5 | 3 | 4 |
| [11](#s11) | `brain-alpha-research-hypothesis-first` | L1 | 105 | 3 | 6 | 1 | 0 | 2.9 | 8 | 3 | 6 |
| [12](#s12) | `brain-dataset-exploration-general` | L1 | 84 | 4 | 2 | 2 | 0 | 4.8 | 9 | 4 | 4 |
| [13](#s13) | `brain-datafield-exploration-general` | L1 | 88 | 3 | 3 | 1 | 1 | 3.4 | 7 | 4 | 6 |
| [14](#s14) | `brain-dataset-mining-experience` | L6 | 64 | 2 | 2 | 3 | 3 | 3.1 | 5 | 2 | 2 |
| [15](#s15) | `brain-data-feature-engineering` | L1 | 330 | 3 | 8 | 2 | 0 | 0.9 | 8 | 6 | 7 |
| [16](#s16) | `brain-make-some-gem` | L2 | 165 | 6 | 4 | 2 | 5 | 3.6 | 10 | 5 | 5 |
| [17](#s17) | `brain-feature-implementation` | L2 | 119 | 3 | 2 | 1 | 0 | 2.5 | 4 | 2 | 2 |
| [18](#s18) | `alpha-expression-verifier` | L2 | 75 | 1 | 2 | 1 | 1 | 1.3 | 5 | 1 | 3 |
| [19](#s19) | `brain-inspect-raw-template-create-setting` | L3 | 99 | 4 | 4 | 0 | 0 | 4.0 | 4 | 8 | 4 |
| [20](#s20) | `brain-sim-alphas-in-batch-and-track` | L3 | 210 | 4 | 2 | 2 | 0 | 1.9 | 7 | 5 | 4 |
| [21](#s21) | `wqb-concurrency` | L3 | 119 | 5 | 6 | 0 | 1 | 4.2 | 7 | 6 | 4 |
| [22](#s22) | `wq-brain-alpha-optimization-v1` | L4 | 197 | 8 | 5 | 4 | 1 | 4.1 | 7 | 5 | 6 |
| [23](#s23) | `brain-alpha-robustness` | L4 | 148 | 9 | 5 | 3 | 1 | 6.1 | 7 | 9 | 6 |
| [24](#s24) | `brain-how-to-pass-alpha-test` | L4 | 132 | 10 | 9 | 1 | 2 | 7.6 | 11 | 11 | 11 |
| [25](#s25) | `brain-alpha-repair` | L4 | 51 | 4 | 5 | 2 | 1 | 7.8 | 7 | 9 | 5 |
| [26](#s26) | `brain-explain-alphas` | L4 | 65 | 5 | 3 | 1 | 1 | 7.7 | 7 | 3 | 6 |
| [27](#s27) | `brain-calculate-alpha-selfcorr-quick` | L4 | 69 | 3 | 6 | 0 | 1 | 4.3 | 6 | 4 | 4 |
| [28](#s28) | `worldquant-submit-alpha` | L5 | 292 | 11 | 12 | 1 | 3 | 3.8 | 12 | 16 | 9 |
| [29](#s29) | `wq-brain-superalpha` | L5 | 250 | 7 | 9 | 2 | 4 | 2.8 | 9 | 8 | 8 |
| [30](#s30) | `brain-alpha-judge` | L5 | 300 | 10 | 5 | 3 | 1 | 3.3 | 13 | 15 | 10 |
| [31](#s31) | `wq-backtest-monitor` | L6 | 162 | 10 | 5 | 2 | 1 | 6.2 | 10 | 12 | 6 |
| [32](#s32) | `planning-with-files` | L7 | 221 | 3 | 4 | 1 | 1 | 1.4 | 10 | 5 | 6 |
| [33](#s33) | `pull-brain-skills` | L7 | 68 | 3 | 3 | 0 | 0 | 4.4 | 4 | 3 | 3 |
| [34](#s34) | `INDEX.md` | — | 428 | 8 | 12 | 3 | 2 | 1.9 | 13 | 13 | 7 |
| | **合计** | | | **286** | **286** | **103** | **48** | | **288** | **279** | **208** |

> “P1 多”不等于“这个 skill 差”：ra-pipeline（950 行）、toolkit、ppa-mining 体量大、被引用多，条目自然多。**按密度**（P1/百行；ra-pipeline 与 toolkit 含其 references，略高估）最高的是 brain-alpha-research（9.5，含不存在的 CLI 与常量改写冲突）、campaign-toolkit（8.5）、ra-pipeline（8.0）、repair（7.8）、campaign-matrix（7.7）、explain-alphas（7.7）、how-to-pass（7.6）；**按后果**最重的是**提交链**（submit-alpha、judge、superalpha、monitor）与**元技能**（pull-brain-skills、planning-with-files）——它们体量不大，但涉及不可逆动作、安全边界、不可达状态机或已失效的命令，密度并不高却应先修。

### 0.4 Tier-0：应立即处理的 20 项（会真的害人 / 不可逆 / 不可执行）

| # | 主题 | 主要条目 | 后果 | 最小修复 |
|---|---|---|---|---|
| T0-1 | **提交链的状态机不可达**：`submit_verdict` 的 `SUBMITTABLE` 只在 `GET /submit` 返回 200 时产生，而全库（含该工具自己的 docstring）都确认该 GET 恒 404 → 对未提交候选只能得 `UNVERIFIABLE`/`BLOCKED`；退出码 `0` 同时代表 SUBMITTABLE/UNVERIFIABLE/ALREADY_SUBMITTED | SB-03、RA-95/96/102、IX-08 | 上游条件写“SUBMITTABLE”永远不满足；以 `$?==0` 放行的脚本会放行 UNVERIFIABLE | 文档改写为可达状态机（X-2）；工具给 UNVERIFIABLE 独立退出码（另开代码任务） |
| T0-2 | **“POST /submit = 零成本探针”被教了 ≥12 处**：通过的 POST 就是真实、不可撤销的提交 | RC-01、SC-04、HP-03、RB-15、RE-08、RA-97、SB-13/19、SP-13 | “同族连测”“先 5 个探针”会把最先通过的那颗真提交 | 全库一个警告块；探测一律 `confirm_submit=False` 预检（X-9） |
| T0-3 | **submit-alpha 默认示例复制即真提交**，且带不存在的形参（`dataset/wave/expr_family`）与 `confirm_submit=True` | SB-06、SB-09 | 参数错误或未经确认的真实提交 | 示例拆两步：先 `confirm_submit=False`，再“仅在用户确认后”的 True 版 |
| T0-4 | **superalpha**：MCP 路径 `force=True` 绕过 prod 闸；“预检”= 真提交；全文没有“如何创建 SA”的调用 | SP-13、SP-14 | 违反“prod≥0.7 不提交”的用户铁律；agent 无从创建 SA | 唯一入口 `super_build.py {select\|status\|probe\|submit}`；MCP 路径须手工先做 prod 闸 |
| T0-5 | **judge 脚本仍可真实提交**（`--confirm-submit` → `client.submit_alpha`），且把 201 异步受理报成失败；PPA 闸门与规范相反（颜色 GREEN vs PURPLE；Sharpe≥1.58 会把 Sharpe∈[1.0,1.58) 的合法 PPA 判 BLOCK；CW 配方推荐被拦形态） | JD-14、JD-09 | “不执行提交”只靠散文；合法 PPA 被误杀 | 删脚本里的提交路径并加测试；PPA 口径取 `config` 的 PPA 定义 |
| T0-6 | **资格线模型过期**：文档“未达标即判死”，代码是“主闸 + 旁路 A–E + 判死线”（2Y≥1.2 永不判死） | HP-15、OP-18、RA L793 | 误杀 5 类旁路候选 | 三处改引 `mode_b_config` 判定表 |
| T0-7 | **monitor §14.2 命令模板 4/4 与真实 CLI 不符**，第 4 条还写入 RA 已废止的 `wave{W}_verdict` 键；该旧键仍被另外 5 处文档教 | BM-14、RA-108、RD-21、RP-08、TR-15、ME-02 | S6 回写失败或写入废止键，下一轮读不到结论 | 按真实 flag 重写；旧键清零（加 grep 测试） |
| T0-8 | **universe 合法性规则与 config 相反**（monitor 称 TOP2500/TOP800 非法；EUR 默认就是 TOP2500）；`ILLIQUID_MINVOL1M` 残留 | BM-08、PP-24、RD-17 | 拒绝合法 universe / 用已下线档位 | 一律取 `config.REGIONS[region].universes` |
| T0-9 | **`$WQ_PY` 只有 Windows 定义**（`Scripts/python.exe`），且 skill 中大量裸 `python`、PowerShell 与 bash 混用、`<SKILL_ROOT>` 占位符不可解析 | IX-03、TK-16、SC-07、JD-13、PB-06、PW-01 | 非 Windows 环境全部 Python 命令指向不存在的可执行文件 | 按平台分支或提供探测脚本；机械检查裸 `python` |
| T0-10 | **加权混合“政策禁止、闸门有缺口、文档仍在教”**：≥12 处教加权/等权腿相加；实测 `rank(A)*0.6+rank(B)*0.4`、V9 的 `X + Y*0.35`、`subtract(rank,rank)` 均**放行**，而数学等价的 `add(rank(A),-rank(B))` 被拦 | RA-46/89、RD-03/11/19/28、TK-28、TR-27、PP-13/20、GM-06、JD-09、HP-05 | 照抄挂闸或绕过闸门；政策与机检口径分叉 | X-3：一条规则 + 形态白名单 + 闸 5 覆盖矩阵测试 |
| T0-11 | **prod 墙学说 ≥6 版**：首探即 dead_end / 换白名单数据集 / 镜像稀释与骨架重构 / 反馈循环与组合腿救援 / 先 5 探针 / 注入低 prod 新血 | RA-69/74/85/93、RD-04/28、OP-01、RC-01/03、RP-07、RR-02、RE-08、SP-09 | 同一情景 agent 可合规地做出相反动作 | X-1：一张决策表，其余引用 |
| T0-12 | **幽灵/未知算子仍在 SOP 中**（上一轮 P0-1 未修）：`ts_median`（幽灵，会 CANCEL 整批）、`scale_down`、`vec_mean`（应为 `vec_avg`）、`is_placeholder`；`ts_event_*` 在 `known_ops` 无而闸 8 强制 | DF-08、EX-08、PP-12、HP-19 | 整批 ERROR/CANCELLED | 以 `get_operators` 实测裁决并加“SOP 算子 ∈ known_ops”机检 |
| T0-13 | **修复配方丢失**（上一轮 P0-6 未修）：repair 声称“5 轴/6 武器/分布映射已上移 optimization-v1”，承接侧零命中；INDEX 仍以此为卖点 | RE-01、IX-07 | 知识既不在原处也不在新处 | 恢复配方或删声明 + 加“声明已上移的术语必须 grep 到”机检 |
| T0-14 | **配额口径**：submit-alpha 同文 L191 说 `activities/submissions` 不可用、L264 又叫人用它（上一轮 P0-3 部分未修）；`pipeline.py` 仍优先读它；且“00:00 ET=12:00 GMT+8”将在 **2026-11-01（DST 结束）** 失效 | SB-15、SB-21、IX-22 | 误判余量撞 4/4 墙；一小时日界漂移 | 配额只留一处 + `America/New_York` 计算 |
| T0-15 | **凭据与外发**：≥8 种凭据来源；多处直接指示读取 `.env` 或命令行传密码（违反 AGENTS 安全约束）；judge 的 LLM 层默认开启且无外发边界说明（表达式发往第三方端点） | JD-07/10、SB-04/09、SC-07、IR-05、FB-10、NM-14、OP-04 | 凭据泄露面 + 核心资产外发 | 凭据只经 MCP 会话；外发字段白名单；默认关闭 |
| T0-16 | **skill 供应链**：`pull-brain-skills` 无入库审查、推荐示例默认 `--overwrite`（脚本直接 `rmtree`）、文档默认目的地与代码相反；`planning-with-files` 的 Stop 钩子含未解析占位符（不可能成功执行）且 `hooks` 无审查规则 | PB-01/02/03、PW-01、IX-18 | 外部指令/钩子静默进入运行时；覆盖核心 skill | 隔离目录 + 审查清单 + 禁默认覆盖；INDEX 增 hooks 审查 |
| T0-17 | **DB 单轨 vs 文件产物**：铁律禁止，多处仍要求写 `alpha_list.json` / `final_expressions.json` / `WAVE_LEDGER.md` / 文本文件 | OP-06、IR-02、SA-03、RD-21、FI-05、BM-15、IX-08 | 真相源分裂 | X-13：允许写的文件类清单 + 机检 |
| T0-18 | **缺失承接者**：S6 的“OS 表现监控”与重着色（BLUE→GREEN/YELLOW/RED）无人承接；G3 OS 回流脚本已归档；S6→S0 反馈环读写错位（`submit_ready_blocked` vs `saturated_datasets`）；`robustness`“必经闸”无任何代码读取 | BM-01、TK-07、RA-113、TK-18、RB-03 | 声明存在而实现缺位，闭环断裂 | X-18：声明-实现对照表，逐项补齐或撤回声明 |
| T0-19 | **边界声明“形式合规、内容矛盾”**：`test_skill_boundaries` 只查“职责边界”段存在，至少 6 个 skill 的边界与正文/代码矛盾 | IX-19、SB-02、JD-02、BM-03、SP-02、HP-01、RE-02 | 覆盖率 100% 的错觉 | 语义检查：边界“不做”的动作词在正文需带“仅引用”标记 |
| T0-20 | **死指针/死命令**：不存在的 CLI（`wqb research/settings/news-refresh-portfolio`，上一轮 P0-7 未修）、脚本（`backfill_backtest_dataset.py`、`get_ny_time.py`、`collect_verified_pids`、`logs/_fix_desc_sa4.py`）、文档（`prod_wall_breakthrough_sop.md`、`fresh_datasets_7region.json`） | AR-12、NS-04、RA-31、NM-12、BM-06、SP-06、RD-28、CM-16 | `command not found` / 找不到文件 | 机检 C/D 接入 CI |

### 0.5 六个系统性根因（问题为什么反复出现）

1. **追加式演进 + 没有“单一真相源”的落地机制。** “唯一权威 / 唯一事实源 / 唯一基准 / 唯一入口”在 SKILL.md+INDEX 中出现 **47 次**（INDEX 11、RA 9、toolkit 7、judge 3……），但同一事实（prod 墙、提交判定、配额、闸编号、并发、ledger 键）仍各写 N 遍；修一处漏 N−1 处。
2. **规则与叙事/快照/变更日志混写。** 机械检查（启发式）显示：SKILL.md 平均每 100 行有 2.5 处日期括号（brain-alpha-research 15.9、ra-pipeline 7.7、field-quality 6.6、superalpha 5.2），历史叙述标记密度最高的是 ra-pipeline（6.7/100 行）、toolkit（4.8）、make-some-gem（4.2）；正文里大量“⚠ 2026-xx-xx 修正 / 旧文请勿沿用 / 已被实测推翻 / 删除线行”。同时，按标题匹配只有 6/33 个 skill 有显式的失败分支节、5/33 有显式的产出节。读者无法区分“永远成立的规则”与“当时的观测”，agent 更无法判断哪条已过期。
3. **守护只覆盖形式，不覆盖内容为真。** 有测试的：frontmatter、边界段存在、工具/节点计数、GEM 内嵌副本。没有的：fenced 命令的 flag 与 argparse 是否一致、示例表达式是否过自家闸、阈值是否抄自 config、状态机是否可达、ledger 键是否有写入方。`last_verified` 也无机检——33/33 同日批量戳。
4. **术语与状态没有词表。** “槽 / 提交 / 配额 / 信号族 / 达标 / ATOM / WARNING / 判死”各有 2–4 种含义；verdict 词汇 ≥10 套；闸门分类 ≥5 套（gate.py 闸、wave_gate 闸、RA 步、monitor 关、INDEX 层级）；阶段编号 ≥4 套（L / S / 步 / 闸）。
5. **不可逆动作与探测的界线只靠散文。** POST /submit、`force=True`、`--confirm-submit`、`--overwrite`、hooks、LLM 外发、读取 `.env`——防护在“注释/警告”，代码与示例并不一致。
6. **环境假设未参数化。** Windows/PowerShell/`Scripts\python.exe`/`D:\` 路径/EDT 固定偏移/裸 `python`——本次会话的两个 MCP 服务就因 Windows 绝对路径而无法启动。

### 0.6 阅读指南

- **Part A（§1–§34）**：逐 skill、逐阶段的审查主体。每节结构固定：定位 → 总评 → 阶段热力图 → 编号问题表。
- **Part B（X-1…X-19）**：跨 skill 综合——把散在各处的同类问题合并成“现象 → 根因 → 单一表述方案”。
- **Part C**：上一轮（2026-09-26）P0 与整改计划的逐项关闭情况。
- **Part D**：整改路线（三批）、写法规范（SOP 模板 + 情景卡模板 + 24 处范本清单）、建议新增的机械检查。
- **附录**：覆盖范围、方法、复现命令、局限。

**条目 ID 前缀 → 章节**

| 前缀 | 章节 | 前缀 | 章节 | 前缀 | 章节 |
|---|---|---|---|---|---|
| RA / RD / RP / RF / RT / RC / RR | §1 ra-pipeline（SKILL / decision-table / campaign-prompt / failed-gates / taxonomy / prod-corr / 区域 profile） | CM | §2 campaign-matrix | TK / TR | §3 campaign-toolkit（SKILL / references） |
| NM | §4 next-move | LB | §5 labs-data-analysis | FB / FR | §6 forum-browse（SKILL / references） |
| PP | §7 ppa-mining | AR | §8 research | FQ / NS / HF | §9 field-quality / §10 news-sentiment / §11 hypothesis-first |
| DE / DF | §12 dataset- / §13 datafield-exploration | ME | §14 dataset-mining-experience | FE | §15 data-feature-engineering |
| GM / FI / EV | §16 make-some-gem / §17 feature-implementation / §18 expression-verifier | IR / SA / WC | §19 inspect-raw-template / §20 sim-alphas / §21 wqb-concurrency | OP / RB | §22 optimization-v1 / §23 robustness |
| HP / RE / EX / SC | §24 how-to-pass / §25 repair / §26 explain-alphas / §27 selfcorr-quick | SB / SP / JD | §28 submit-alpha / §29 superalpha / §30 judge | BM / PW / PB / IX | §31 monitor / §32 planning / §33 pull-brain-skills / §34 INDEX |

---

## Part A　逐 skill · 逐阶段审查

各 skill 章节入口见 §0.3 表中的链接；每节结构固定：**定位 → 总评 → 阶段热力图 → 编号问题表**。

---

<a id="s1"></a>
### 1. `wq-brain-ra-pipeline`（L-RA · SKILL.md 950 行 + 5 个 references + 13 个区域 profile）

**定位**：REGULAR alpha 挖掘的唯一编排 SOP（九步 + 5b）。**体量与结构**：全库最大（950 行、69 个标题、最长一行 1069 字符；>220 字符的行 26 条；历史叙述密度 6.7 条/百行、日期括号 7.7 个/百行，均为全库最高）。

**总评**：信息价值极高（大量“血的教训”），但**同一文件同时承担了 5 种角色**——①操作指令 ②证据/起因 ③变更史（“2026-09-xx 新增/修正/补入边”） ④代码实现细节（函数名、ledger key 形状、argparse 行为） ⑤易过期的状态快照（“当前仅 MEA”“320 个体检包”“至 09-30”）。指令与其余四类混排，导致：规则被埋在长段里（最长一个表格单元 ≈2000 字）、同一规则被复述 2–5 遍且力度不一（“必须/建议/须先补或降级”）、自相矛盾处难以发现（SKILL.md 部分 P1 共 48 处；连同 references 与区域 profile，§1 共 76 处）。**根因不是“写得多”，而是没有固定的步骤模板与信息分层。**

**阶段热力图**（🟢 清晰 🟡 需改 🔴 有缺陷；四维：逻辑 / 职责 / 边界 / 是否需情景规范）

| 阶段（行号） | 书写逻辑 | 职责划分 | 边界界定 | 需情景规范？ |
|---|---|---|---|---|
| 头部 / 职责边界 / 三角分工（1–35） | 🟡 | 🟡 | 🔴（“唯一权威”三种说法） | 是：何时调 matrix |
| 运行前置（37–50） | 🔴（变量未定义） | 🟡 | 🟡 | 是 |
| 九步总则 + Profile 路由（52–75） | 🟡 | 🟢 | 🟡 | 是：probe-only / frozen |
| 步 1 S-PRE（77–155） | 🔴（6 个子任务无序） | 🟡 | 🔴 | **是（库存盘点 vs 开新挖）** |
| 步 2 S0（157–247） | 🔴（顺序颠倒） | 🟡（越界写 toolkit 机制） | 🔴（硬前置实为软） | 是 |
| 步 3 S1 + 闸 SEM（249–313） | 🟡 | 🟡 | 🔴（“双重 fail-closed”名不副实） | 是 |
| 步 4 S2（315–416） | 🔴（三处自相矛盾） | 🔴（实现文档混入 SOP） | 🔴 | **是（选波实验清单）** |
| 步 5 S2→S3（418–465） | 🟡 | 🟡 | 🔴（闸清单四处各写一遍） | **是（失败分支缺 6 类）** |
| 步 5b prod-first（467–479） | 🟡 | 🟡 | 🔴（“硬门”实为 WARN） | 是 |
| 步 6 S3（481–555） | 🟡 | 🔴（并发细节越界） | 🔴（QUICK 模式风险） | 是 |
| 步 7 S4（557–659） | 🔴（14 个主题无序，失败分支居中） | 🟡 | 🔴（组合腿规则有漏洞） | **是（辅助腿如何入场）** |
| 步 8 S4→S5（661–708） | 🔴（判定链未成表） | 🟡 | 🔴（POST=真提交） | **是（提交判定清单）** |
| 步 9 S6（710–820） | 🔴（顺序与执行相反） | 🟡 | 🔴（S6→S0 反馈环断） | 是 |
| 整链执行（824–846） | 🟡（节点归属自相矛盾） | 🟢 | 🟢（“提交类节点不入链”是好边界） | 否 |
| 循环与停止（848–864） | 🔴（2000 字表格单元） | 🟡 | 🔴（3 套“连续 3 波”规则） | **是（每条规则配数字例）** |
| 快捷入口（868–874） | 🔴（语法不通） | 🟡 | 🔴（与闸 SEM 冲突） | 是 |
| PPA 分支（878–883） | 🟡 | 🔴（编排器却只有 3 行） | 🔴（挖/提两个门禁并存） | 是 |
| Artifact 契约（887–903） | 🟢 | 🟢 | 🟡（ledger key 目录缺失） | 否 |
| 反模式（907–917） | 🟡 | 🟢 | 🟡（用错误词 READY） | 是（补最痛的） |
| 附录 工具映射（921–950） | 🟢 | 🟡 | 🔴（第 3 处“唯一权威”） | 否 |

#### 1.1 头部、职责边界、三角分工（L1–35）

| # | 位置 | 维度·级 | 问题 | 改进建议 |
|---|---|---|---|---|
| RA-01 | L3 description（270 字） | 边界·P2 | 塞入 15 个触发词，其中“选数据集/中性化/窗口”“批量回测”“发批”“提交批次”与 `wq-brain-campaign-matrix`、`brain-sim-alphas-in-batch-and-track`、`worldquant-submit-alpha` 重叠（机械检查 §I：`批量回测`、`开战役` 同时命中 2 个 skill）→ 路由靠运气 | description 只留“整链/开战役/从零到提交/一键战役/日循环”；单点动作词删除或限定为“已进入九步链时”；被让出的词在对方 skill 补“整链请走 ra-pipeline”反向指针 |
| RA-02 | L17–21 职责边界 | 职责·P2 | “不亲自动手/只做编排、每步调既有 skill 或 MCP”，但正文直接调用 ≥12 个 `tools/*.py` CLI（build_gate_prior_from_inventory、select_ra_basket、campaign_intel×7 子命令、field_semantic_classify、wave_gate、step_funnel、forum_recon、gen_field_inspect_packs…）并两次直读 sqlite（L127–134、L555）。“编排”与“执行”的线没画 | 把边界句改成“本 skill 不实现能力，但**规定调用顺序与判据**”；给一张“CLI → 归属 skill/tool 层”表；直读 sqlite 一律换成 MCP 或注明为何不能 |
| RA-03 | L20、L938 vs L679/L681 | 边界·P1 | “提交层**唯一权威** = submit_verdict”（L20、L938）⇄ “它是**否决权威**”（L679）⇄ “提交层唯一权威**不是** submit_verdict”（L681）；`tools/submit_verdict.py` 文档串里也同时出现“否决权威”“唯一权威” | 全库统一为三句并删除“唯一权威”字样：①submit_verdict = 模拟层判定 + 否决（BLOCKED 即停）②它**不能证明**可提交（GET 提交视图恒 404）③提交层真值 = 用户确认后的 POST 响应 |
| RA-04 | L24 | 逻辑·P3 | `brain-deepExplore` 废止说明是变更史，且是“不要再读”式负指令，没有正向去向 | 移入 CHANGELOG；正文只保留一句“S2-D/S2-M 概念已废，见步 4” |
| RA-05 | L26–35 三角分工表 | 职责·P2 | 表名“三角”只有 3 行，随后又追加 3 个例外 skill；matrix 的“where=查表选区选集”与步 1/步 2 的“查表/选集”重叠，且没有说**何时**调 matrix | 表扩为 6 行并加“何时进入”列；补情景：①用户已给 REGION → 不调 matrix；②用户说“挖点什么/哪个区好” → 先 matrix；③matrix 返回多区并列 → 回问用户 |

#### 1.2 运行前置（L37–50）

| # | 位置 | 维度·级 | 问题 | 改进建议 |
|---|---|---|---|---|
| RA-06 | L39–43 | 逻辑·P1 | 声称“唯一输入 `$REGION`”，后文却用 `$DELAY/$UNIVERSE/$DS/$W/$DTYPE/$TARGET_SEATS`；其中 `$DELAY/$UNIVERSE/$DTYPE` 到 L367 才赋值，`$W`、`$TARGET_SEATS` 从未定义 | 前置块列出全部变量：名称、来源（settings.json / 用户 / 上一步产物）、缺省值 |
| RA-07 | L45–46 | 边界·P2 | “MCP 应用尽用——**能**走 MCP 的一律走”没有判据；示例却大量使用裸 `python`（L96/99/127/171/193/286 等），与同段“走 `$WQ_PY`”冲突；L125 用 bash heredoc，而全文约定 PowerShell（`;`、反引号续行），在 Windows 上会直接失败 | 增“CLI 允许清单”（有 argparse 契约、无对应 MCP 的 tools/ 脚本）；示例统一 `& $WQ_PY`；跨区死路检查直接用 `get_dead_ends()`（region 缺省即全区） |
| RA-08 | L47 | 逻辑·P2 | “阈值不复写，引用 `GATES`”，但本文含 ≥15 处字面阈值（1.58、1.0、0.7、0.60–0.70、≥100、≥16、≥30…）；反模式又把“复写阈值”列为禁止项——SOP 自己违反自己 | 定义“复写”=拷贝 `config.GATES*` 的闸门值；区域/机制经验阈值允许，但必须带 evidence 出处（wave/日期/样本量） |
| RA-09 | L49 | 边界·P1 | 优先级只写“用户 > 决策表 > 正文”，L75 另写“profile > 正文”；profile 与决策表谁高、用户指令与代码 fail-closed 闸谁高，均未说 | 单列一节“冲突裁决”：用户显式指令（须台账留痕）> 代码 fail-closed 闸（唯一放行=显式覆盖键）> profile > 决策表 > 正文。情景：用户说“继续挖 MEA”（frozen）→ 只能走 MEA profile 的 probe-only 后门，不得绕过 |

#### 1.3 九步总则与区域 Profile 路由（L52–75）

| # | 位置 | 维度·级 | 问题 | 改进建议 |
|---|---|---|---|---|
| RA-10 | L56 | 逻辑·P1 | “每步含 目的/MCP 调用/产物/失败分支；任一步 FAIL 就地回退，不允许跳过” 与实际不符：步 7 无“目的/产物”、“失败分支”夹在段中（L654）；步 1 的调用散在 4 处；“就地回退”与各步“回步 N”矛盾；“FAIL”未定义（闸 FAIL / 工具报错 / verdict FAIL） | 固定每步模板：**目的 → 前置 → 调用 → 产物（写哪张表/哪个 key）→ 完成定义 → 失败分支（表：现象→动作→回到哪步）**；并定义“FAIL”三种含义 |
| RA-11 | 全文 | 逻辑·P2 | 两套编号并用：“步 1–9(+5b)” 与 “S-PRE/S0–S6”，正文混用（步 1 里的“S1 用字段级失败边界选字段”指的是步 3；步 4 里的“S4/S6 依据配对证据”指步 7/9），无映射表；“九步”实际有 10 个节点（5b） | 顶部加映射表；正文只用“步 N”，S 编号仅出现在 MCP 参数处；5b 改称“步 5.5”或并入步 5 |
| RA-12 | L58–64 | 逻辑·P3 | 硬编码“13 个 profile”“14 个 REGIONS”“仅 AMR 未覆盖”，同一事实三种说法且随时过期；另有事实漂移：`AMR` “无战役目录”但 `tracking/AMR/config/{settings,thresholds}.json` 存在；`TWN` 有 profile 但 `tracking/TWN/` 目录不存在——违反本文自己的“开新区前必须补 profile + tracking/<R>/config/” | 数量与名单只在 INDEX §区域清单维护，本文写“见 INDEX”；加 CI 一致性检查（profile ↔ tracking ↔ REGIONS） |
| RA-13 | L66–73 注入点表 | 逻辑·P3 | “生成先验”行的 profile 字段列写成优先级句子（应为 `priors`），与其余三行形式不一；缺“字段缺失时回落什么”列 | 表改为 4 列：注入点 / profile 字段 / 影响步骤 / 缺失回落 |
| RA-14 | L75 | 边界·P2 | 一段塞 4 条规则（优先级、缺字段回落、未覆盖区域、frozen）；“frozen 步 1 即拒”与 L87“按 profile 入口裁决处理、不继续步 2”不一致；`probe-only` 的通用语义本文不定义（只在 MEA/HKG 等 profile 内各写各的，如“单波 8 探针上限”）；“当前仅 MEA/AMR”是快照 | 拆成 4 条编号；补 3 行小表定义 active / probe-only / frozen 的**默认**含义，profile 只写差异；快照移出 |

#### 1.4 步 1（S-PRE）查表与开工前置（L77–155）

> 结构问题：本步有 **7 个互不编号的子任务**（读经验文件 → 读 profile → 库存盘点 → PPA 主题门禁 → 5 条 DB 查询 → 跨区死路 → 产出率解读），其中“读 profile”应先于一切，“库存盘点”是整条流水线的分流点（清库存 vs 开新挖）却排在中间。

| # | 位置 | 维度·级 | 问题 | 改进建议 |
|---|---|---|---|---|
| RA-15 | L79–81 | 逻辑·P2 | 首段是对 dataset-mining-experience 的消费规则，夹带“S1 用…选字段，S2 机制文档引用…”（指步 3/步 4）；“以 DB 查表结果为准”未说是哪个工具；路径 `<region>_<dataset>_campain.md` 的 “campain” 拼写易被当成笔误 | 拆成“读取规则/继承条件/缺失回落”三句；注明 `campain` 是既定文件名 |
| RA-16 | L83–85 | 边界·P2 | “论坛默认不查；仅当『判死区复开评估』时用 forum_recon”：该触发条件无定义；而同一工具在步 4（机制枯竭）、步 5（KB 无货）、步 7（卡闸找武器）、步 9（判死前软核对）另有 4 个触发点，`--out` 目标还各不同（kb/ledger/negative）——“默认不查”被架空 | 建一张“forum_recon 触发表”：触发点 / 问题模板 / `--out` / 额度 / 缓存；步 1 改为“见触发表” |
| RA-17 | L87 | 逻辑·P2 | “先读区域 profile”放在“目的”之后、库存盘点之前，且 `frozen` 处理与 L75 不一致 | 提到步 1 第一条；frozen/probe-only 分支写成小表 |
| RA-18 | L89–102 库存盘点 | 边界·P1 | 这是**全流程最大分流点**（“先清库存，再开新挖”，实证 170 次新回测 0 可提交 vs 一次扫描 20 条），却只有一句判据“候选池不足以覆盖目标金字塔”——无量化定义（多少条、覆盖几座未点亮塔算够）；`cache/candidates.json`、`cache/basket.json` 的读写与 L889“禁止 Write 战役 json”冲突；“三万条/11%”是会漂移的绝对数 | 写成决策小表：basket 条数 ≥ target 且覆盖 ≥3 座未点亮塔 → 直接跳步 7/8；否则 → 步 2 并只补缺口塔。明确 `cache/` 是“可丢弃中间文件”；绝对数改为“见 get_mining_yield” |
| RA-19 | L103–106 | 边界·P1 | “篮子敲定以 detail 端点 `is.checks` 无 `result==FAIL` 为准”弱于步 8 的 RA 口径（WARNING/ERROR 也计，`check_counts_as_failed`=非 PASS/PENDING）；“UNVERIFIABLE 不构成可提交依据”只说不能，不说下一步用哪个工具取 detail | 统一引用 `Failed RA==0`（`compute_webdata_failed_counts`）；点名取 detail 的 MCP 工具 |
| RA-20 | L107 PPA 主题门禁 | 边界·P2 | 一行 ≈700 字混合：调用、解析字段、匹配规则、标签（YELLOW + WAIT_THEME_ROTATION）、RA 不受限、重扫铁律、两条带日期的快照（09-27 到期、09-28 新主题）。挂在“每次新战役必做”下，但只与 PPA 有关；2026-09-16 审计曾建议降级为“提交时门禁”，SOP 仍保留为开工前置 | 拆 4 条；限定“仅当本战役含 PPA 分支”；快照挪到 ledger `ppa_theme` 并注日期；说明与步 8 提交时门禁的分工 |
| RA-21 | L118–138 跨区死路 | 逻辑·P2 | 用 `LIKE '%ds%'` 扫 `payload`，`model1` 会误命中 `model109`；bash heredoc（RA-07）；`get_dead_ends()`/`get_cross_region_lessons()` 已提供同能力；“跨区死族一律不进白名单，不论评分多高”（L138）与 L201–203“跨区弱/仅条件腿的集**排在健康集之后、判死之前**”（仍在榜内）矛盾——“弱”与“死”被混用 | 改用 MCP；统一术语：跨区弱=降权，跨区死族（≥2 区独立复现）=排除，并写出两者阈值；补情景：某集仅在 1 区弱 → 降权不排除 |
| RA-22 | L141–149 产出率读法 | 逻辑·P2 | 两个比率的动作区分很好（conversion→修管道，yield→换标的）；但“yield_rate **连续**为 0 且样本 ≥100”——yield_rate 是累计比值，“连续”无意义；2026-09-06 基线数字（IND 35.7%…）是**旧口径**，紧邻 09-19 严格口径（IND 12.6%）却未标注“旧口径”；100 与 10% 无依据 | 改“累计 0 且已测 ≥100”；旧基线标“loose 口径，仅作历史对照”；给阈值来源（哪一波/哪个分位） |
| RA-23 | L153 产物 | 逻辑·P2 | “产物：universe/delay/中性化/排除集/…”没说写到哪（ledger key？settings.json？），下游却直接读 `$DELAY/$UNIVERSE` | 写明：落 `settings.json` + ledger `s0_*`；列字段与键名 |
| RA-24 | L155 失败分支 | 职责·P2 | “转 brain-next-move-analysis **选新区域**”，但同文件 L83 说 next-move“日报，不产出配置”，选区归 matrix（三角分工）；库存盘点有候选时的分支缺失 | 改“转 matrix 选区（next-move 只提供日报输入）”；补“库存足够→跳步 7/8”分支 |

#### 1.5 步 2（S0）数据集体检 + 金字塔配置（L157–247）

| # | 位置 | 维度·级 | 问题 | 改进建议 |
|---|---|---|---|---|
| RA-25 | L159–160 | 逻辑·P1 | 顺序颠倒：先写“调 `workflow_campaign(S0)`；锁白名单后 upsert `s0_whitelist`”，后面才说“S0 评分**前**先跑 `s0-select`”（L186）和 calibrate→打分（L223–237）；白名单的**硬约束 0–7** 在 L211 才出现——读者按顺序会先锁白名单再读约束 | 步 2 改成有序清单：①s0-select ②calibrate ③S0 打分 ④按硬约束筛 ⑤锁白名单 ⑥体检包核对 |
| RA-26 | L159 | 逻辑·P3 | 括号里是“原 dataset_health_check.py 已归档到 attic”的变更史；而 ppa-mining 仍附带同名脚本，INDEX L129 又指向它 → 读者看到 3 处不同说法 | 删括号；统一 INDEX/ppa-mining 的引用 |
| RA-27 | L160 | 边界·P2 | `upsert_ledger_key(region,"s0_whitelist",{...})` 的 payload 用 `{...}` 省略，无字段定义 | 给一个最小 JSON 示例（datasets、tier、reason、locked_at） |
| RA-28 | L162–184 体检包 | 边界·P1 | 标题“开区**硬**前置”，正文“缺包时步 5 硬门**不生效**”，默认 `--inspect-mode warn`（放行），L221 又降为“须先补或降级并记因”，L183 是“建议 enforce”——同一规则三种力度；“台账记因”未说 key。**闸 SEM 缺省 enforce（L309）、体检门缺省 warn、CLI 总闸 2026-10-11 前 warn**——三个同构闸缺省值各异，读者无法判断哪个是硬的 | 出一张“闸模式表”：闸名 / 开关名（CLI+env）/ 缺省 / 缺前置时行为 / 逃生口 / 留痕 key（见步 5 建议）；本处只写“缺省 warn，开新区改 enforce，并记 `inspect_waiver`” |
| RA-29 | L167、L175–179 | 逻辑·P3 | 快照数字（320 个包、HKG172/USA104…；ZIP=20260219、160 集、七区）与 L427 重复且日期标注不同（09-17 vs 09-11） | 只在一处保留，并注明“快照日期 + 查询命令 `ls …`” |
| RA-30 | L186–205 选集增强 | 逻辑·P2 | 一大段混合：命令、四点增强（①–④）、新列与新标记（`maxS/fld/[跨区弱…]/[跨区RA-clean…]/仅条件腿`）、历史背景（IND 7 集 197 回测 0 候选）；三个样本量阈值（bt≥8、≥16、≥100）无依据 | 改成“标记 → 含义 → 动作”表；样本量阈值各配 1 句依据（CLAUDE.md 要求非窗口数值须给理由）；背景移到 references |
| RA-31 | L204–205 | 边界·P1 | 指令 `python tools/backfill_backtest_dataset.py` **文件不存在**（已验证）→ 指令不可执行 | 删除该句或改为实际工具；检查 INDEX L239 同样引用 |
| RA-32 | L207–209 座位可达性 | 情景·P3 | `est_seats` 缺省 2 无依据；“座位”与 CLAUDE.md “3 颗点亮一座塔”的关系没说 | 一句话对应：target 座位 ≈ 3×目标塔数；缺省 2 的来源 |
| RA-33 | L211–221 硬约束 0–7 | 边界·P2 | 编号从 0 开始（后插）；混杂硬规则与启发式；#1“win 族必须进**候选**”与 #0“已点亮塔不得进**白名单**”未说“候选≠白名单”；#3“category_weight 0.9–1.15”“禁止 1.3 vs 0.7”是反例不是规则，且无校验点；#4“主导腿禁用≠整集判死”无情景；#5“白名单外禁止 generate/simulate”未说明 xr-probe（本来就要跨区/跨集探测）的例外；#6 “≥1 万”“连续 2 波”无依据，且没说转 hypothesis-first 后步 5–8 是否照走；#7 是第 3 次重复体检包规则 | 分成“硬约束（有代码执行）”与“准则”两栏；每条补执行点（哪个闸/哪个函数）与一个反例；#4/#6 各补 1 个情景 |
| RA-34 | L223–237 代码块注释 | 逻辑·P3 | 9 行注释是在回答“为什么第三步不能删”（历史评审问答）、暴露 `cmd_calibrate/cmd_score` 内部函数名；`ac`（alphaCount）缩写未定义；发现两类异常后**做什么**未写 | 注释缩成 3 行表：调用 / 效果 / 何时用；异常处置写“回步 1 复核 thresholds 或手改”并给条件 |
| RA-35 | L239–245 评分机制增强 | 职责·P2 | P0/P2/P3/P5/P6 是内部工单号（缺 P1/P4）；内容默认 OFF、机制细节又指向 toolkit §6.x → 属 toolkit 的职责，SOP 只需说“何时打开” | 只保留“何时 opt-in”的情景（如：新区有实测 best_sharpe → 开 P0）；机制留在 toolkit |
| RA-36 | L247 | 边界·P3 | “写 findings”不说写哪 | 指定 ledger key |

#### 1.6 步 3（S1）字段扫描 + 闸 SEM（L249–313）

| # | 位置 | 维度·级 | 问题 | 改进建议 |
|---|---|---|---|---|
| RA-37 | L251–264 | 边界·P1 | “必做 typed catalog”与“深度字段理解**按需/禁注入 GEM**”“S1 三件套**按需加载**”并列，而 L257 又说“该层是两条铁律的**唯一落点**，本步**必须执行**”——铁律就写在本段，何来“唯一落点在别的 skill”？“按需加载 skill”与“必须执行铁律”互相抵消 | 把两条铁律提成本步的**必做检查项**（含命令/工具），三件套 skill 仅作深查参考；删“唯一落点”。禁注入 GEM 的说明合并（L259–264 与 L311–313 重复） |
| RA-38 | L253 | 逻辑·P3 | 括号内是“2026-09-26 审计补入边”的过程叙述 | 移 CHANGELOG |
| RA-39 | L266–270 | 逻辑·P2 | 只有一行命令，无“目的”；“产物：fields 表 + ledger S1 决策”没有 key 名 | 补目的/完成定义（catalog 覆盖 >0 的字段数） |
| RA-40 | L271 users 分级 | 边界·P2 | 50/10/9/≥50% 的阈值无出处（指向 prod-corr-avoidance.md，但正文不摘要）；“已确认超标的字段族”的登记处未说；“orchestrator 迁移”是历史标签 | 写一行依据+指针；点名登记 key |
| RA-41 | L272 失败分支 | 逻辑·P2 | “字段数 <10 则退回步 2 白名单外”语句不通（回步 2 把该集移出白名单？）；与 L201“fields<5 标仅条件腿”是两个阈值（5 与 10）；VECTOR 提示不是失败分支 | 改为“字段数<10 → 回步 2 将该集移出白名单并记因；<5 → 仅条件腿”；VECTOR 提示移到前置 |
| RA-42 | L274–313 闸 SEM | 边界·P1 | **“双重 fail-closed（代码保证，不靠记忆）”与代码不符**（已核对源码）：①`s1_semantic_<ds>` 只被 `tools/wave_gate.py` 读，`field_semantic_classify.py` **不写** `s2_field_pool_<ds>`；②GEM 的 `economic_field_pool_check`（gem.py:275）是**自己**用 `build_economic_field_pool` 建池（缓存命中则直接沿用旧池），并不读语义台账，也不会失败。SOP 让 agent“建议同步…写 ledger `s2_field_pool_<ds>`”却**没有任何命令**，表里“该池须由上一步语义归类产出”无代码保证。表标题“双重”实列三行（第三行是测试） | 改标题为“单重 fail-closed（步 5 闸 SEM）+ 一项人工约定”；要么给出真正写 `s2_field_pool` 的命令并让 GEM 侧校验，要么删除该约定。这是**最容易被绕过的一处**（agent 以为 GEM 侧已保证） |
| RA-43 | L275–281 起因 | 逻辑·P3 | 起因/证据（348 条、49.4%、37/373）篇幅 ≈ 规则本身的 2 倍 | 缩成 2 句 + 指向 reports |
| RA-44 | L305–309 模式解析 | 边界·P1 | “与仓库既有闸同构（CLI>env>缺省 enforce）… 同 WQB_INSPECT_MODE、WQB_GATE_MODE”暗示缺省相同；实际体检门缺省 warn、CLI 总闸 10-12 前 warn，仅 SEM 缺省 enforce。wave_gate 现有 ≥12 个模式开关，形态 5 种：`--gate-mode`、`--inspect-mode`、`--semantic-gate {…}`、`--prod-family-gate/--no-prod-family-gate`、`--skip-*-gate` | 见 RA-28 的闸模式表；推荐统一为 `--<gate>-mode {off,warn,enforce}` 一种形态 |

#### 1.7 步 4（S2）选波：概念优先生成（L315–416）

| # | 位置 | 维度·级 | 问题 | 改进建议 |
|---|---|---|---|---|
| RA-45 | L320–324 | 职责·P2 | LLM 402 余额不足会表现为误导性“no meta.json within 90s”、干跑假绿、旁路手写 ideas + `headless_runner/run.py`——价值极高但放在“引用 make-some-gem”的引言段，且加粗标记错位（`**因**余额不足**返回…**`）；`headless_runner/run.py` 相对路径解析不到（实际在 make-some-gem/scripts/ 下） | 移到“失败分支”；写全路径；一句话判据：“看到 no meta.json → 先查 LLM 通道，不要重试” |
| RA-46 | L330 vs L336/L392/L626/L799 | 边界·P1 | **加权混合自相矛盾**：#1 以 EUR `0.4×慢 MODEL + 0.6×快 PV` 作“已验证配方”；#7“禁止 add(A,B) 混信号”；L392 预闸“丢弃加权混合毒模式”；L626“路线 A：禁止任何加权混合（含等权）”；L799 又要求 win 回写“mix 比例、快/慢腿”。同一份文件对同一构造既举为范例又禁止 | 明确：**已验证配方仅指“信号概念+设置”，不再记录混合比例**；EUR 例子改写为“慢腿作 group/bucket/条件、快腿作主信号”；L799 删“mix 比例” |
| RA-47 | L331 vs L377 | 边界·P1 | 硬约束 #2“**必须**带 `priors_file`”与 L377“priors_file **已可省略**（GEM 从 DB 快照直读）”直接矛盾 | 删 #2 中该句，改“默认无需；仅在 DB 快照缺失时显式传” |
| RA-48 | L330–338 硬约束 1–9 | 边界·P2 | #1“≥2 槽按机制换腿”与 #4“≥1 win 换腿”数值冲突；#3 中 `PASS_CHEAP` 首次出现但直到 L708 才指向定义；#5“若 2 跨集”“慢腿/快腿”无定义，且与 #7“优先单数据集 atom”方向相反；#6 说非标窗口“须给解释/证据”，预闸却自动别名/仅 WARN（L389）且无处登记证据；#7–#9 是 CLAUDE.md 的复述（3 份副本）；“硬约束”里混有不可机检的准则 | 拆“硬约束/准则”；#1 与 #4 合并并给一个数；#5 删或补情景；#6 指定证据登记位置（如 idea 的 `window_rationale` 字段）；#7–#9 改为指针 |
| RA-49 | L333 “七槽” / L397 “8 条” / L483 “七槽回测” | 边界·P1 | “槽”一词三义：并发模拟槽（Token-Bucket C≈7、`slots=7`）、波内表达式配额（七槽：≥2 跨金字塔…）、批大小（8 子模拟）。“8 条不是固定上限”与“七槽”并存 | 术语框：**槽=并发的 multi-simulation 批**；**波=一次 S2→S3 的候选集合**；**批=一次 create_multi_simulation（≤8）**。#4 的“七槽”配比改称“波构成” |
| RA-50 | L340–356 | 职责·P1 | “首选 assemble-priors 节点，**以下协议仅作内部映射说明，勿手写**”，随后 5 条是实现细节（ledger key、JSON 形状）；但第 5 条含**真规则**：`community_tpl_kb` 不进 priors、取骨架前**必查 `ghost_operator_advisory`**、否则整批 ERROR/CANCELLED——**被埋在“可忽略”的列表里**（本次审查最典型的“有价值信息因表述而被绕过”）。另：“只消费 wins(≤6)/dead_ends(≤12) 两个键，其余忽略”与 item 4（methodology/signal_family_rules 作 region_context 注入）、L361（gate_priors 进 prompt）矛盾 | 内部映射挪到 references/assemble-priors-internals.md；第 5 条规则拆出为步 4 的独立必做项“取骨架前查 ghost_operator_advisory”，并在步 5 失败分支重复引用；修正“只消费两个键”的表述 |
| RA-51 | L345–346、L347 vs L373 | 逻辑·P3 | “stage=S2 与路由无关”的注释是对旧误解的答辩；assemble-priors 调用在 L347 与 L373 出现两次，读者以为要调两次 | 保留一次；解释 stage 只是标签 |
| RA-52 | L366–380 代码块 | 逻辑·P2 | 伪赋值与真调用混在一个块；最后一行 `workflow_campaign(stage="S2", dataset, wave)`（build-wave）无注释；`pipeline_mode` 三选项无选用情景；`$W` 未定义 | 拆“变量/调用”两块；`phased` 缺省，`skeleton` 用于“需要语法构造保证的骨架填充”，`single` 不用 |
| RA-53 | L382–392 | 逻辑·P2 | “除下述…外”指向其后的“原有：…”，先后颠倒；6 类自动改写（hump、bucket、非法 group、窗口别名、每骨架封顶 12、quantile 归一）只写了“系统做什么”，没写“agent 需做什么”（如：非标窗仅 WARN 后要不要处理） | 表：预闸规则 / 自动动作 / agent 动作 |
| RA-54 | L394–395 | 逻辑·P2 | 首句“消费 `methodology_rules`…”缺主语，像被截断；“未验证 DB 有表达式，不得声称步 4 成功”是**完成定义**却无验证手段 | 补主语；把完成定义单列并给查询（`get_wave_expressions` 或等价） |
| RA-55 | L397–409 选波实验清单 | 逻辑·P1 | 一个 13 行的无编号段落含 ≥12 条规则（8 条非上限、`--size` 语义、清单写入 ledger、extra_args 组合、条数由清单推导、`--expected-count` 旧口径、`wave_meta`、未选≠dead_end、S4/S6 依据配对证据、每轮报告四项、研究线索复验、落库核验/回滚），且**中英文无空格**（“8条”“S4遇到指标上升”），文风与全文不同（不同作者/时间加入）；“选波清单/延后项审计/最小纠错复验/受保护状态/平台单位警告”等术语此处无定义；“不得补参数变体凑数”与失败分支“候选不足则 enhance/扩组合”（L411）冲突 | 改为情景分支：**A 普通探索 / B 预定实验（配对）/ C 重建 / D 结果解读→步 7/9**，每支写 触发条件→调用→核验→产物；术语表指向 selection-plan.md；统一“不足→显式扩容或分波，不补变体” |
| RA-56 | L411 | 边界·P2 | “按超时恢复清单查任务”——**该清单在全部 skills 中无定义**（已 grep）；“不要手写”与 L324 旁路“手写 ideas md”需区分（表达式 vs ideas） | 补清单或指针（wqb-concurrency/toolkit 的任务恢复）；注明“手写 ideas ≠ 手写表达式” |
| RA-57 | L412–416 | 边界·P2 | forum_recon 第二个触发点，与 L84“默认不查”并存；“触封顶”“无腿可换”怎么发现没说；“额度以查出有效文章为标准…安全上限”上限数值缺、“有效文章”未定义 | 并入 RA-16 的触发表；给上限数与“有效文章”判据 |

#### 1.8 步 5（S2→S3）门禁（L418–465）

| # | 位置 | 维度·级 | 问题 | 改进建议 |
|---|---|---|---|---|
| RA-58 | L420 | 逻辑·P3 | 两条禁止（新建 `_gate_waveNN.py`、写 `cache/gate_wave*.json`）无理由、无正向指向（正向在 L442） | 合并为“用 `tools/wave_gate.py`（结果落 gate_results）；禁止另写脚本/缓存文件”并放到命令之后 |
| RA-59 | L422–432、L441、L473、L301 | 边界·P1 | **wave_gate 含哪些闸，在 5 处各写一遍且互不一致**：L423 多样性=闸 6（且“由 wave_gate 自动调用”）；L429 “闸 1–5 + 闸 7/8 + 体检硬门”（不含闸 6）；L441 “语法+gate.py 5 闸+体检+多样性”；L301 闸 SEM；L473 闸 PF；另有闸 2b、闸 2.6、闸 4 ARITY。编号体系混合了数字（1–8）、小数/字母（2b、2.6）、名字（SEM、PF） | 建**唯一闸清单表**：编号/名字 → 拦什么 → 缺省模式 → 缺前置时行为 → 逃生口 → 失败后回哪一步；INDEX §gate.py 闸编号作为其唯一来源并覆盖 SEM/PF |
| RA-60 | L424、L431–432 | 逻辑·P2 | 出现**删除线原文**（`~~注：…~~`）+“↳ 已收敛”；“不要再把 check_batch 当判据”是变更史叙述 | 整段删除；只留“判据=gate.py:check_batch_diversity（闸 6）” |
| RA-61 | L423 | 边界·P2 | “契约过期 **FAIL-CLOSED 并自动续约**”自相矛盾（拦截还是续约后放行？）；60%、2/3 阈值无依据（虽有 wave 实证） | 写清顺序：过期→自动续约→用新契约重判（结果仍可 FAIL）；给阈值出处 |
| RA-62 | L425–427 | 边界·P1 | 说体检包由 `webdata_quality.py --export-expr` 生成（L426），而步 2 说用 `gen_field_inspect_packs.py`（L171）——**两个生成器**；`webdata_quality.py` 源码注释写明 “--export-expr 自诞生起就没产出过有效数据”（L838）；“缺包时本闸不生效”本文已是第 3 次出现 | 删 L426 的旧命令；三处合并为一处，其它处指针 |
| RA-63 | L434–436、L438–446 | 边界·P2 | 既称“MCP 节点与 CLI 同一实现”，示例却只给 CLI，与“MCP 应用尽用”不一致；ghost-audit 命令在 L440 与 L459 重复 | 示例改节点优先，CLI 作“无 MCP 时”；命令去重 |
| RA-64 | L448 | 逻辑·P3 | 一行塞 2 个无关提示（VECTOR 预检；repair 批跳过多样性闸），且 L423 已说 repair 类默认豁免 | 拆开；说明何时仍需显式传 `--skip-diversity-gate` |
| RA-65 | L450–452 | 逻辑·P2 | 闸 2b（非法 group 字段 FAIL）与 L387 预闸（非法 group 字段**丢弃**）、bucket range（预闸补/丢 vs 语法闸 FAIL）是同一批规则的两种处置，未说明关系 | 一句话：预闸=GEM 产出侧自动修；闸 2b/语法闸=非 GEM 来源的兜底 |
| RA-66 | L454–463 | 情景·P3 | 幽灵算子命中后的三种处置（等价替换/`preflight_expressions` 单测/丢弃）没有选择判据 | 决策小表 |
| RA-67 | L465 失败分支 | 情景·P1 | 只覆盖 3 类失败（语法、多样性、KB 无货）+“2 跨集”；**闸 SEM（exit 2）、体检硬门、闸 PF、闸 2b、幽灵算子（exit 1）、闸 7/8 数据质量**的失败后动作均缺 | 表：闸 → 现象/退出码 → 动作 → 回步 → 是否可豁免及留痕 key |

#### 1.9 步 5b：prod-first 探针（L467–479）

| # | 位置 | 维度·级 | 问题 | 改进建议 |
|---|---|---|---|---|
| RA-68 | L467、L473–479 | 边界·P1 | 标题“升为硬门”，但代码：已知死骨架→拦截整波；**新骨架→仅 WARN**；“投入第二波前必须先查”只是流程要求。硬/软混说；“新信号族”“新”相对谁（本区/全库）未定义；闸 PF 的粒度是“前 2 个算子的骨架指纹”，5b 是“信号族”，步 7 是“字段集合”——同一个词三种粒度 | 表：谁强制（代码/流程）；定义“信号族=字段集合，骨架=前 2 算子”，三处分别指名 |
| RA-69 | L471 | 边界·P1 | 只给两个区间：≥0.7 → dead_end 换机制；0.60–0.70 → 直接进步 8；**<0.60 无指示**。且“不做任何去相关变体”与 D14（prod 墙突破 SOP）、步 7 的“STOP→换白名单不同数据集（D0）”、L654“prod≥0.7 → Mode B 换概念”**四种处置并存** | 一张“prod 墙唯一处置表”：<0.60 / 0.60–0.70 / ≥0.7（首探）/ ≥0.7（多探仍高）→ 各自动作，引用 D14 的**适用前提**（何时允许突破尝试） |
| RA-70 | L473 | 逻辑·P3 | 第 5 种开关形态（布尔对 `--prod-family-gate/--no-…`）；“拦截整波”与闸 SEM“仅剔除命中表达式”粒度不一致，未解释 | 同 RA-59 表；粒度差异注明理由 |

#### 1.10 步 6（S3）七槽回测（L481–555）

| # | 位置 | 维度·级 | 问题 | 改进建议 |
|---|---|---|---|---|
| RA-71 | L483–485 | 职责·P2 | S3 入口有 3 个：`workflow_batch_track`（L511）、`brain-sim-alphas-in-batch-and-track`、toolkit `pipeline.py`；仅说“也可走…填槽内容仍以本步为准”，没有选用判据；L509 又出现第 4 个 `workflow_campaign(stage="S3")`。 | 选用表：表达式来自 DB 且要整波闸 → batch_track；手写 alpha_list → sim-alphas skill；调试 → pipeline.py |
| RA-72 | L487–488 | 边界·P2 | “弱探针最多 1 槽；有近闸字段则 0”与步 4 #4 逐字重复；“组合批/裸探针”无定义 | 保留一处；给定义 |
| RA-73 | L489–497 条目 3 | 边界·P1 | 一个编号条目内含 4 个主题：设置跟 win、ILLIQUID_MINVOL1M 永久停提、**QUICK/FULL 模式**、设置层先验自动改写。其中 **“QUICK 不可提交、探针批可考虑 QUICK”是高风险规则却写成“可考虑”**：若把 QUICK 产出的 alpha 带进步 7/8，会缺 correlation/theme 检查却被当通过；且没有“QUICK 产物须 FULL 复测”的流程与标记位。设置先验（≥30 样本、≥2× 过闸率）**默认开**并静默改写设置，与“设置跟 win”相互覆盖，“想优先就显式 --set 钉住”被压在段尾；同一 GBR 例子在 L363–364 重复 | 拆 4 条；QUICK 写成硬规则：“QUICK 产出**仅**用于探针信号判断，不得进入步 7/8，须 FULL 复测；回测行必须记录 simulationMode”；先验改写用表说明覆盖关系 |
| RA-74 | L498 | 边界·P1 | 第 **3 次**定义 prod-first：5b“投入第二波前，`--top-k 2`”；此处“每槽先 1–2 条骨架”；步 7“S3 收批后必调，`--top-k 3`”。时机与 top-k 均不同 | 只在 5b 定义一次；步 6/7 引用；统一 top-k |
| RA-75 | L499 | 边界·P2 | 一句里塞“表达式从 list_expressions 取”与安全规则“禁止自动提交 alpha”；“自动”的判据未写；`pipeline --submit`=提交回测的澄清（L688）远离此处 | 安全规则单独成条并放最前；术语框区分“发起回测/提交 alpha” |
| RA-76 | L500–502 | 逻辑·P3 | “S2-COMPLIANCE 已降级为提示”是变更史；toolkit 的 S2_COMPLIANCE_* 文档仍按“必做”写，未同步 | 删此条；同步 toolkit 文档 |
| RA-77 | L504–528 代码块 | 逻辑·P2 | 16 行注释讲历史（`--concurrency` 不存在→argparse exit 2→detached 静默；2026-09-27 三道闸），命令只有 1 行；块内 8 个工具调用无“何时用/顺序”；**无“步 6 完成定义”**（何时算 S3 结束？） | 历史移 CHANGELOG；加完成定义：“本波全部 multisim 终态，且 backtest_results 行数=波内表达式数（含 ERROR/CANCELLED 标记）” |
| RA-78 | L530 vs L505–508、L540 | 情景·P1 | “429 则**降并发**、批大小 ≤5”——但并发由 pipeline 内部锁定为 `min(7,批数)`、外部传非 7 只会被 warning；表格 429 又写“指数退避”。**该指令无可执行手段**（仅 `WQB_GLOBAL_SLOTS` 环境变量可调，未提） | 写成可执行：429 → ①等待（退避）②`WQB_GLOBAL_SLOTS=<n>` 降账户级并发 ③批大小 ≤5；并指向 wqb-concurrency §8 |
| RA-79 | L532–544 故障表 | 逻辑·P2 | “依据”列是 wave 代号（e10a/e10b、b87/b92/b93）——对新读者无意义；行 1“8 子模拟全 ERROR → 重发相同表达式”与 L544“先归因再重发”冲突（确定性 ERROR 重发只会烧配额）；行 6 “查 MCP 服务进程(PID)”无命令、无 OS 说明 | 依据列改“判据（怎么确认是这一类）”；行 1 加前置：`message` 为瞬态类才重发 |
| RA-80 | L546–553 | 职责·P2 | 账户级槽位仲裁（`_lib/slots.py`、`WQB_GLOBAL_SLOTS`）属并发细节，L483 却宣称“并发唯一来源=wqb-concurrency”→ 职责越界、重复维护 | 移入 wqb-concurrency，此处一句指针 |
| RA-81 | L555 | 职责·P2 | 用裸 SQL 查积压，而 `campaign_intel.py backlog-drop`（toolkit SKILL L209）正是积压清理工具，此处未提；“近闸积压”“2 倍”无定义/依据；与步 1 的 `conversion<10%`、L509 的“积压开波闸”是**三套**积压判据；位置应在步 9/循环 | 统一为一套判据 + 指向 backlog-drop |

#### 1.11 步 7（S4）诊断改进（L557–659）

> 结构问题：本步 ≈100 行、**14 个主题无序排列**（S4 节点、RN_EXPOSURE、指针、alpha_booster 去留、prod-first、ROBUST_STRUCTURAL、s4-prescreen、OS 衰减、salvage 检索、组合形态合规、事故记录、风险中性化硬规则、**失败分支**、卡闸找武器、prod 排队），失败分支位于中间，其后还有 2 项。

| # | 位置 | 维度·级 | 问题 | 改进建议 |
|---|---|---|---|---|
| RA-82 | L563–565 | 逻辑·P2 | 描述节点内部（解析 alpha_id、拼 review_wave 参数）并附修复史；对“解析不到即 FAIL”没给 agent 动作 | 一句：“FAIL 且列出最近波次 → 用其中的字符串波号重试” |
| RA-83 | L566–568 vs L647–653 | 边界·P2 | RN_EXPOSURE 有两个版本：L566“rn_sharpe ≤ rn_sharpe_min（默认 0）→ 墙、不进候选/near/salvage/组合腿”；L647“rn ≤ 0 **且** sharpe ≥ 1.58 → 记 dead_end、禁止继续调参”。对象粒度（单条/信号族/数据集）和后果（排除 vs dead_end）没对齐 | 表：条件 → 对单条的处置 → 对族的处置 → 记录位置 |
| RA-84 | L570–574 | 逻辑·P2 | “Mode B 70% / Mode A 30%”比例无解释（预算？次数？）；“未编排增强节点去留（登记）”是项目管理信息；alpha_booster/modeb_improve 作批量变体器，与 CLAUDE.md“禁止混信号调参”存在过拟合风险，缺护栏 | 比例写含义；去留登记移出；补护栏：“变体入库后仍走步 5 全部闸，且同骨架换参上限沿用封顶” |
| RA-85 | L576–587 | 边界·P1 | 第 3 处 prod-first（见 RA-74）；“STOP → **换白名单不同数据集**（D0）”与 5b“**换机制**”、D14“突破 SOP”冲突（RA-69） | 引用统一处置表 |
| RA-86 | L589–592、L566、L568 | 边界·P2 | 墙/池的术语（RN_EXPOSURE、ROBUST_STRUCTURAL、PARTIAL、near、salvage、停止规则 B）首次出现处均无定义，也无词汇表 | 建“词汇表”指针（见综合篇） |
| RA-87 | L594–601 | 职责·P1 | S4 有两套实现：`review_wave.py`（`workflow_campaign(S4)`，L560）与“selfcorrQuick→check_self_correlation→compute_mutual_correlation→check_correlation→robustness→judge”六段链；关系（替代？顺序？包含？）未说。另出现**又一套 verdict 词汇** READY/REVIEW/REJECT | 画图：S4 = prescreen → review_wave → 逐候选链；每段的输入/输出/去向；词汇表统一 |
| RA-88 | L603–611 | 边界·🟢 | “语义边界（实测决定，别误用）：Spearman 仅 +0.086，本校准**不抬高 IS 阈值**”——好范例：说明了“别拿它做什么” | 作为全库范式推广（每个易误用统计量都配“不可用于…”一句） |
| RA-89 | L626–634 路线 A | 边界·P1 | 规则本身有**漏洞**：允许 `subtract(rank(A),rank(B))`“视作单一价差信号，须有经济含义”，但 `subtract(a,b)` ≡ `add(a,-b)`——等权二腿相加的同一违规，且现有闸 5 只判 `add`；判据“须有经济含义”主观、不可机检。同样的漏洞形态（S=2.11 的漂亮结果漏闸）已在事故记录里发生过一次 | 给可检判据：subtract 仅在 A、B 为**同一经济量的对偶两侧**（买/卖、已实现/隐含）且同数据集同字段族时允许，并须在 idea 里声明 Expected Exposure；否则一律视同 leg-add；补测试与闸 5 覆盖 subtract |
| RA-90 | L617–634 | 情景·P1 | “卡闸辅助腿检索”（跨数据集正交辅助腿）与紧随其后“禁止任何加权混合”之间缺桥：**取到辅助腿后能怎么用？** 允许项①–⑤没有逐一对应到“辅助腿→用法”。这恰是 CLAUDE.md 的“有些字段适合做条件、group、bucket”场景 | 写情景表：辅助腿 → 只能以 (a) `trade_when` 条件 (b) `bucket/group` 分组 (c) 中性化/残差 的形式入场，**不得作加法项**；各给 1 个改写示例 |
| RA-91 | L626 | 逻辑·P3 | “路线 A”未定义（“路线 B”是谁？D14 有 route 1/2/3，稀释腿=加权混合，与此处冲突） | 用规则名替代路线字母 |
| RA-92 | L636–645 事故记录 | 逻辑·P3 | 含 commit 级细节（`_detect_weighted_mix_structural`、`platform_constraints.json v1.5`、16 条测试构成）；可执行部分只有“门禁通过≠合规”“放行形态” | 移入 docs/incidents；正文留 3 行 |
| RA-93 | L654 失败分支 | 逻辑·P1 | 位于步中；“prod_corr ≥0.7 则 Mode B 换概念”是 prod 墙处置的第 4 种说法（RA-69）；“>10 种结构”无依据 | 移到步末；引用统一处置表 |
| RA-94 | L655–658 | 边界·P2 | forum_recon 第 3 个触发点，`--out ledger`（前面是 kb） | 并入触发表 |

#### 1.12 步 8（S4→S5）稳健闸与提交判定（L661–708）

| # | 位置 | 维度·级 | 问题 | 改进建议 |
|---|---|---|---|---|
| RA-95 | L663–665 | 边界·P1 | “**submit_verdict READY** 且 prod<0.7 → 立即请用户确认”：submit_verdict 的标签是 SUBMITTABLE/UNVERIFIABLE/BLOCKED/ALREADY_SUBMITTED，**没有 READY**（READY 属 s4-prescreen / brain-alpha-judge 词汇）；标题“0.60–0.70”，正文“<0.7”；置顶的“当天提交”与下一行“S4→S5 必经 robustness”谁优先未说；块后有 3 个空行（遗留编辑痕迹） | 词汇统一为 SUBMITTABLE；明确“当天提交”不豁免 robustness，只豁免“同族变体探索” |
| RA-96 | L671–688 判定链 | 逻辑·P1 | “提交判定链（顺序执行）”只编号了 2 项；真正的链是 资格门 → submit_verdict → robustness → prod<0.7 复核（`check_correlation(refresh=True)`）→ **用户确认** → POST → 轮询 ACTIVE；条件都塞在一句 400 字长句里；`submit_verdict` 代码块放在条目 1 下（属条目 2） | 改为有序检查清单，每项：判据、工具、谁决定、通过/失败去向 |
| RA-97 | L679–685 | 边界·P1 | **“可靠判据=直接 POST；失败回带 403+全量 checks，零成本”**：但 POST 若全部通过就是**真实且不可撤销的提交**；本文同时要求“确认前禁止 workflow_submit_alpha”。于是“真值只能靠 POST”与“先用户确认”之间的次序没说清——agent 可能把 POST 当“零成本探针”。证据仅 3 次（GBR 09-27）。同一 404 事实在 L105、L679、L681 重复 3 次 | 单列风险框：“POST=真提交；仅在用户明确确认后执行；其 403 回带仅用于**判死**，不得当探针”；若有 `dry_run`/`confirm_submit` 语义，说明与 POST 的关系；404 事实只写一次 |
| RA-98 | L673 | 边界·P1 | Failed-count 资格门与步 1 的“无 FAIL”口径不一（RA-19）；`webdatascope-failed-gates.md` 的 RA 清单缺 `LOW_ROBUST_UNIVERSE_SHARPE.WITH_RATIO`（config 为 18 项） | 统一引用 config；修 reference |
| RA-99 | L687–688 | 边界·P2 | “禁止 workflow_submit_alpha / submit_batch”未覆盖裸 `submit_alpha`（judge 引用的工具名机械检查判为未注册）；`--submit`=提交回测的澄清放在这里，离 pipeline 用法（步 6）太远 | 列出**全部**提交类入口（含已废弃别名）；术语框 |
| RA-100 | L690–691 | 职责·P2 | 只写 REGULAR→submit-alpha、SUPER→superalpha；**PPA（只能走平台 web UI）**未提，而步 9/PPA 分支要求“优先提 PPA 那颗” | 补 PPA 行：“由用户在 web UI 提交；agent 只产出清单与主题匹配证明” |
| RA-101 | L693–706 四态表 | 情景·P2 | 表本身清晰（好范例）；但 2026-09-28 起补发已自动化，表仍写成手工步骤 → 手工+自动可能双补发；“等 4 分钟”“60 秒窗口”无依据 | 加分支：“用 submit_alpha 节点 → 自动；手工 POST → 按表”；ASYNC_STUCK 后动作（知会用户）写进表 |
| RA-102 | L708 | 边界·P1 | “只有 submit_verdict **无 FAIL** 且提交层 **200** 才算可提交”：submit_verdict 没有 FAIL 标签；提交层 200 = 已经提交成功（循环论证）；“PASS_CHEAP”首见于 L332，定义靠指针；“配额”一词在本文兼指相关性配额（L103）、模拟配额、提交配额 | 改写为清单终点；“配额”限定词 |

#### 1.13 步 9（S6）复盘回写（L710–820）

| # | 位置 | 维度·级 | 问题 | 改进建议 |
|---|---|---|---|---|
| RA-103 | L710–750 整体顺序 | 逻辑·P1 | 文本顺序与执行顺序**相反**：“完成定义（回写 → assemble-priors）”在前，“开步先看漏斗（回写结论前先跑）”在后，“自动部分/verdict 判定表/判死封存/点塔回写”再后 | 重排：① step_funnel ② verdict 判定 ③ 三件回写（含 seal→dead_end、pyramid）④ dataset-experience ⑤ assemble-priors ⑥ 完成定义核对 |
| RA-104 | L712–722 | 边界·🟢/P3 | “未回写=本波未完成”“GEM 对 stale 快照只 WARN 不阻断，只能由 S6 兜底”——好的边界陈述。但调用写成伪函数 `workflow_campaign(region=…)`，与全文 MCP 风格不一致 | 统一语法 |
| RA-105 | L724–728 vs L899 | 边界·P1 | 步 9 说 dataset-experience **必做，对本波每个回测数据集**；Artifact 表 S6 行说该文件“**仅对判死/win 集生成**，由 seal_dead_end/add-win 触发”——范围矛盾。“收取异步终态”“块外中文字段”无解释 | 二选一并统一；补 2 句解释术语 |
| RA-106 | L752–761 | 逻辑·P2 | 自动部分（region_kb 刷新）、verdict 枚举、合并语义、`closed`必须带 verdict 挤在一段；这些是**写入契约**而非流程 | 移到 references/write-contract.md，步内留 4 行 |
| RA-107 | L763–776 verdict 判定表 | 边界·🟢/P2 | 3 行小表清晰（好范例）；但“达标”在全文有 3 种口径：S>1.58 & F>1.0（停止规则 A）、`ra_failed_checks` 为空（严格 yield）、过全部评审闸/GREEN（此处）；GREEN/YELLOW/RED 又与 PPA 门禁的 YELLOW（=待轮转）、`workflow_submit_alpha(color=…)` 混用 | 词汇表：达标 A/B/C；颜色只用于 alpha 提交标签，波结论只用 PASS/PARTIAL/FAIL |
| RA-108 | L778–782 | 边界·P1 | **可执行代码块内展示已废弃命令** `upsert_ledger_key … key="s6_verdict_<wave>"`（仅靠行尾注释警告）；`ra-campaign-prompt.md` 验收线、`decision-table.md` D8 仍要求写它/写 WAVE_LEDGER.md | 从代码块删除；grep 全库清除对该 key 的要求 |
| RA-109 | L786–789 | 边界·P2 | “decision-table D2『论坛无解』”——D2 实为“未过闸→证据复核分支”，无“论坛无解”一词；“软提示起步”而措辞“须” | 修引用；说明软/硬 |
| RA-110 | L791–797 | 情景·P2 | “dead_end 回写前先 seal_dead_end”，但 seal 需要 `entry_id=<DEAD_END_ID>`——此时 dead_end 尚未创建，ID 从哪来？“沉降”“封存”“seal”三词并用 | 给 ID 命名规则/顺序；术语统一 |
| RA-111 | L799 | 边界·P1 | “add-win（mix 比例…）”“add-dead-end”不是命令，实为 `campaign.py registry add-win/add-dead-end`（toolkit）；同段又用 `upsert_registry_empirical`——两条写入路径未说谁为准；“mix 比例”与 RA-46 冲突 | 指明唯一路径；删“mix 比例” |
| RA-112 | L811–819 | 情景·P2 | 多样性监控“评分下降则切换目标塔”——无阈值、无谁来切；IS→OS 归因“写进 wave_result”不说写哪个字段 | 补阈值与字段 |
| RA-113 | L820 | 边界·P1 | **S6→S0 反馈环断裂**（已核对代码）：SOP 要求写 ledger `submit_ready_blocked`，说“下一轮 S0 读取”；而 S0 评分实际读 `saturated_datasets`（`score_datasets.py:430`），`submit_ready_blocked` 只被 `tools/step_funnel.py` 计数；`saturated_datasets` 全仓库**无写入方**。→ 该反馈永远不生效。另：孤立 bullet（无父段落）、`add-dead-end` 同 RA-111 | 统一 key：或改 S0 读 `submit_ready_blocked`，或指令改写 `saturated_datasets` 并补写入工具；加集成测试 |

#### 1.14 整链执行 / 循环与停止 / 快捷入口 / PPA / Artifact / 反模式 / 附录

| # | 位置 | 维度·级 | 问题 | 改进建议 |
|---|---|---|---|---|
| RA-114 | L826 | 逻辑·P2 | “步 2/3/4/5/6 映射到节点”，括号却列 8 个节点含 judge/submit_alpha/superalpha（属步 8）；随后“步 7、步 8 无节点”——但步 7 正是 `workflow_campaign(stage="S4")`（L560）、步 8 有 judge/submit_alpha 节点 → 自相矛盾；“2026-09-11 审计纠正”是变更史 | 改成一张 步→节点 表（含“无节点”的明确理由） |
| RA-115 | L836–837 | 情景·P2 | “干跑校验命令能否被 argparse 接受”与 L322“干跑假绿（LLM 通道）”应在同处成对说明；否则读者只记得“干跑绿=能跑” | 单列“干跑不证明什么”清单（LLM 可达、配额、平台鉴权、写库） |
| RA-116 | L845–846 | 边界·🟢 | “提交类节点不入链（confirm_submit 须步 8 用户确认后单独调用）”——**范例**：清晰、可检、有理由 | 补“由哪段代码强制”的指针 |
| RA-117 | L854 首行单元格 | 逻辑·P1 | 单元格 ≈2000 字：规则 A、B1、B2、豁免、撞墙型 FAIL 路由、signal_floor 分工、覆盖写法、11 个阈值键、回落语义；还含**会过期的状态**“GBR 已写入 stop_rules_override，至 09-30”（距今 1 天） | 改成小节 + 决策表；每条规则配数字例（如“最近 3 个 closed 波 FAIL, 同轴 → 拒开；换轴清零”）；覆盖流程单列（谁可授权、写什么、多久过期） |
| RA-118 | L854–857 | 边界·P1 | 3 套“连续 3 波”规则：B1（同轴 closed 波 FAIL）、行 2（重复 B1/B2）、行 4（gate 通过率=0）——对象不同，先后无序；规则 A 用宽口径“达标”（S>1.58 & F>1.0）而步 1 yield 用严格口径 | 一张表：规则 / 对象 / 计数口径 / 命中动作 / 覆盖方式；统一“达标”口径 |
| RA-119 | L858 | 边界·P1 | 信号天花板闸：“实测 **13/13** 区域均已配（AMR ASI CHN DEU EUR GBR GLB HKG IND JPN KOR MEA USA）”——名单缺 TWN 却含 AMR，与 L62（13 profile 含 TWN 不含 AMR）不是同一个 13，且 REGIONS=14；“被拦…不要绕过”与 L854 的 `stop_rules_override` 是否适用于本闸未说；≈1700 字含大量日期证据 | 改“13/14（缺 TWN）”并链检查；写明覆盖键适用范围 |
| RA-120 | L861 | 边界·P2 | “日界 21:30 ET”与“配额 00:00 ET 重置”并存，未解释为何不同；“NY 日”未定义 | 一句解释（例：21:30 后不再发起新波，留出提交窗口） |
| RA-121 | L859–860 | 情景·P3 | “ACTIVE RA ≥10 → 可转 superalpha”“配额耗尽→继续步 2–9（挂起提交）”：未说后者会积压未提交 alpha 的上限 | 加积压上限或提示 |
| RA-122 | L863–864 | 逻辑·P3 | 再次出现删除线原文 + 归档说明 | 删除 |
| RA-123 | L870 | 边界·P1 | 快捷入口“发批：直接走步 5，跳过 S0–S2”——但步 5 的闸 SEM **缺省 enforce**，缺 `s1_semantic_<ds>` 即 **exit 2**；体检硬门、闸 PF 同理。跳过 S1 的用户表达式必然被自家闸拦下，而唯一放行是“醒目告警的 `--skip-semantic-gate`” | 快捷入口先补“三件前置”：`field_semantic_classify`（秒级、零配额）→ wave_gate；或写明何时可 `--semantic-gate warn` 并留痕 |
| RA-124 | L871–872 | 逻辑·P3 | 含 2026-10-11/12 的“到期即变”文案（时间炸弹型文字） | 建“到期文案”标注约定 + 扫描（已有 sunset 测试思路） |
| RA-125 | L874 一键战役 | 逻辑·P1 | “步 1 matrix 后 步 2 体检（不可跳过）则配置包写回 settings.json 后 步 3”——语法不通、“配置包”未定义、“matrix”并非步 1 正文内容；“先干跑看 gate 通过率”——干跑（无 GEM 产物）无从得出通过率；“用户说『自动提交回测』可跳过二次确认”——“提交回测/提交 alpha”混淆正是 L688 警告的风险 | 重写为编号流程；“自动发起回测”与“提交 alpha”用不同词；干跑改为“先小波真跑 8 条看闸通过率” |
| RA-126 | L878–883 PPA 分支 | 职责·P1 | 作为“分支”只有 3 行 + 指向 312 行的 `ppa-mining-experience.md`（与 wq-brain-ppa-mining SKILL 近似拷贝，24 段重复）；未说明九步中哪些步骤因 PPA 改变（S0 判据、算子≤8/字段≤3、Sharpe≥1.0、PC<0.5、提交渠道）。L880“不匹配则**挖 RA**”（挖矿期门禁）与步 1“不匹配的达标候选标 YELLOW+WAIT_THEME_ROTATION”（提交期门禁）是两种政策 | 写“PPA 与 RA 的差异表”（逐步）；二选一政策并注明；参考文件去重 |
| RA-127 | L882 | 边界·P1 | “日循环应**当天优先提 PPA 那一颗**”，但 submit/robustness 两份 skill 都说合法 PPA **只能走平台 web UI**、MCP 自动通道会拦；此处未提渠道限制 → agent 会尝试自动提交 | 补“PPA 仅 web UI；agent 只提醒用户并给清单” |
| RA-128 | L889 vs L95–99 | 边界·P2 | “战役产物只入 wqb.db，禁止 Write 战役 json/csv”与 `cache/candidates.json`、`cache/basket.json`、`--exprs-file <txt>`、`--json <out.json>` 冲突；frontmatter 又给了 Write 权限 | 定义“战役产物（事实源）”vs“一次性中间文件（可删、不作事实源）” |
| RA-129 | L891–899 契约表 | 边界·P2 | 表是好范例（阶段/入库/由谁写），但**不完整**：正文出现的 ledger key 至少还有 `s1_semantic_<ds>`、`s2_field_pool_<ds>`、`forum_recon_*`、`prod_first_<wave>`、`stop_rules_override`、`submit_ready_blocked`、`saturated_datasets`、`seat_model`、`dataset_empirical_prior`、`inspect_waiver`（应有）——无“key 目录”（谁写/谁读/过期） | 增 `references/ledger-keys.md`：key → 写入方 → 读取方 → 缺失行为；并加测试保证“写入方存在且读取方存在”（可捕获 RA-113 类断链） |
| RA-130 | L907–917 反模式 | 情景·P2 | 9 条均是一行禁令、无理由/无正向替代；用了错误词“submit_verdict READY”（RA-95）；遗漏本文最痛的 5 条：QUICK 产物进提交、无确认 POST、`--skip-semantic-gate` 无留痕、双写 `s6_verdict`、把 LLM 402 下的干跑绿当可运行；与正文重复（手写 requests/PowerShell） | 每条补“因 X 发生过 Y”+“改用 Z”；去重；补 5 条 |
| RA-131 | L921–950 附录 | 边界·P1 | 第 3 处“唯一权威”：“提交判定（唯一权威）\| submit_verdict”；`workflow_judge` 行内含 READY/REVIEW/BLOCK（又一套词汇）；表按“逻辑名→模块”排，agent 更需要“步→工具”；仅覆盖 22 个工具，正文用到的多数 MCP 工具（get_campaign_summary、upsert_wave_result、seal_dead_end…）不在表中；维护规则混入 agent 文档 | 改为“步 → 工具”索引（自动生成，见 tools 注册表）；删“唯一权威”；维护规则移至 CONTRIBUTING |

#### 1.15 `references/decision-table.md`（D0–D14，193 行）

**定位**：SKILL 声称“优先级：用户 > 决策表 > 正文”，即决策表是第二权威。**问题**：它是 2026-08 至 09 各批次经验的**追加式合订本**，与 2026-09-13/09-19/09-27/09-28 后的 SKILL 正文多处不同步，且部分行仍在教被废止的做法；同时它同时承载“决策表（条件→动作）”“步骤清单（D8）”“参数笔记（D5/D6）”三种体裁。

| 阶段 | 逻辑 | 职责 | 边界 | 需情景规范？ |
|---|---|---|---|---|
| 文首规则（3–4） | 🟢 | 🟡 | 🔴 | 是：不可被用户指令覆盖的红线 |
| D0 主决策 | 🔴 | 🟡 | 🔴 | 是 |
| D1 验证链 | 🟡 | 🟡 | 🔴 | 是 |
| D2 增强分支 | 🟡 | 🟡 | 🔴 | 是 |
| D3 混合构造 | 🔴 | 🟡 | 🔴 | **是** |
| D4 健康检查 | 🟡 | 🟡 | 🟡 | 是 |
| D5 设置规则 | 🟡 | 🟡 | 🔴 | 否 |
| D6 信号笔记 | 🟡 | 🟢 | 🔴 | 否 |
| D7 多样性榨取 | 🟡 | 🟡 | 🟡 | 是 |
| D8 七槽填槽 | 🔴 | 🟡 | 🔴 | 否 |
| D9 提交与停止 | 🟡 | 🟢 | 🔴 | 是 |
| D10 迭代纪律 | 🟡 | 🟡 | 🟡 | 否 |
| D11 探针 vs 复杂模板 | 🟡 | 🟢 | 🟡 | 是 |
| D12 镜像探针 | 🟢 | 🟢 | 🟡 | 否 |
| D13 S1 结构体检 | 🟢 | 🔴（未被 SKILL 步 3 引用） | 🟡 | 否 |
| D14 PROD 墙路由 | 🟡 | 🟢 | 🔴 | **是** |

| # | 位置 | 维度·级 | 问题 | 改进建议 |
|---|---|---|---|---|
| RD-01 | L3–4 | 边界·P1 | “表中没有的分支才允许停下问用户”“用户指令与硬约束冲突时**直接执行、不请示**、只在台账记录”——**没有红线清单**：不可逆动作（提交 alpha）、平台条款、凭据等不应被“用户指令覆盖”；“台账记录覆盖原因”未给 key 规范（只有 `stop_rules_override` 有名） | 加“不可覆盖红线”（提交前必须的用户确认本身、凭据/日志、不可逆动作）与“可覆盖项 → 覆盖 key 名”对照表 |
| RD-02 | D0 行 1（L10） | 边界·P1 | 一个格子里三套阈值：`TVR 5–20%` 与 `turnover 5–30%` 并存；`margin>5bp` 出现两次，而 `config.GATES_INTERNAL.margin_bp_min=10`；“及用户阈值 … risk_neut S>1、F>0.7”把某次用户提示词里的临时阈值当成默认；`Fitness≥1.0` / `Sharpe>1.58` 的开闭区间不一 | 廉价闸一律写“见 `config.GATES['internal']`”；用户临时阈值只在该次会话提示词内生效，不进决策表 |
| RD-03 | D0 行 2、D3 “定位/主动触发” | 边界·P1 | “混合是**主动提分手段**，Sharpe 1.58–2.0 就主动混合冲更高”——意图正是 CLAUDE.md 禁止的“混信号调参”；D3 又规定只能用“结构交互”（ts_corr/divide/subtract(rank,rank)/if_else/group_zscore），这些仍是**两条信号腿的算术**，与被禁的 `add(A,B)` 只差语法。合规判据按**语法**而非**意图**定义 | 把判据改为意图：“第二数据集只能提供**条件/分组/残差化**（`trade_when`、`bucket/group`、`regress`），不得作为并列信号项”；`ts_corr/divide/subtract` 需证明是**同一经济量的对偶两侧** |
| RD-04 | D0 行 4 vs D14 vs SKILL 5b | 边界·P1 | prod 墙有**三套学说**：D0 行 4“换白名单不同数据集 regenerate，勿磨同腿变体”；D14“结构性去相关→镜像稀释→中性化骨架重构→最后才换数据集（并称 D0 是默认动作）”；SKILL 5b“不做任何去相关变体”。D0 行 4 还用“>0.7”（恰好 0.7 未定义），且 prod 值在 S4 入口通常尚未测得（要等 prod-first/D1 步 4） | 合并为**一张** prod 墙处置表（见 RA-69），D0/D14/5b 都只引用它；补“何时才有 prod 值” |
| RD-05 | D1 行 2、行 4（L20、L22） | 边界·P1 | 同表内 `LOW_2Y strictly > 1.6` 与 `LOW_2Y>1.58`；代码 `submit_queue.LIM["two_year"]=1.58` | 统一为 config 值 |
| RD-06 | D1 行 4 | 边界·P2 | 一行混用内部线与平台线（`SELF<0.5` 内部 vs `submit_queue` 与平台 0.7）；`PPAC`、`CW` 缩写未定义 | 每个阈值标 internal/platform；缩写首现处展开 |
| RD-07 | D1 行 6（L24） | 边界·P1 | 说 submit_ready 池是“`ledger_kv` 表，经 `upsert_ledger_key` 或 `campaign.py ledger submit-ready` 写”；**代码里它是独立 SQL 表 `submit_ready`**（`src/wqb/store/submit_queue.py` 自称 single source of truth，CLI=`tools/submit_queue.py`，收批自动入队、提交自动退役）；SKILL L820 又用 ledger 键 `submit_ready_blocked` | 一句话说明唯一存储与写入路径；删 `mea_d1_campaign_state.json` 历史句 |
| RD-08 | D1 注（L26）、D9 行 4 | 边界·P1 | “`submit_alpha` 返回 **201 + success:false** 是工具 bug，不算失败”——与 SKILL 步 8 的四态表（②=201 + success:**true** 异步受理；③=200 + success:false + 空体）不一致；旧口径会让 agent 把③当“bug 可忽略”而不补发 | 删此注，改指 SKILL 四态表 |
| RD-09 | D2 行 4（L35） | 边界·P1 | “sharpe < 0.8 → **放弃该数据集**”：①符号盲（强负信号 -1.9 也 <0.8，而 D12 说强负=方向写反、要镜像探针）；②粒度错位（单条 alpha 的 sharpe 决定整集去留） | 改“该集**最强 \|sharpe\|** <0.8 且已做镜像探针（D12）→ 放弃”；SKILL 停止规则同用绝对值 |
| RD-10 | D2 行 6（L37） | 边界·P1 | CW 失败 → “backfill + **结构交互补腿**”；而 D3 “不允许用增删腿数的方式修不达标的信号”、D6 的 CW 修法优先级是“①时间平滑 ②换算子几何 ③单信号结构 ④换字段/概念”——同一失败三套配方，且 D2 的“补腿”与 D3 自相矛盾 | CW 修复只保留 D6 的顺序，D2 行改为引用；brain-alpha-repair 的 CW 配方同步（见综合篇） |
| RD-11 | D3 行“组合形态（铁律）”“允许的组合形态”“乘法仅限”“数据集数” | 边界·P1 | ①仍写“两种写法均被闸 5 block”——正是 2026-09-28 事故里被证伪的旧说法（等权 `add(rank,rank)` 曾漏闸，见 SKILL 事故记录），未提 `equal_weight_leg_add`；②“允许 5 类”（ts_corr/divide/subtract(rank,rank)/if_else·trade_when/group_zscore·rank）与 SKILL 的“允许 5 类”（单信号结构/换算子几何/换字段概念/事件门控/SuperAlpha）**两份清单不同**；③“乘法仅限两强信号 multiply(rank A, rank B)”不在 5 类内，自相矛盾；④“数据集数 2–5”无依据且与“单数据集 atom 优先”方向相反 | 只保留一份允许清单（放 SKILL 或 D3，另一处引用）；补 equal-weight 条；删③或纳入清单并说明；④给依据或删 |
| RD-12 | D3 行“已废止参数”、D6 CW 行、D11 行 8 | 逻辑·P3 | 多处保留**删除线原文**（`~~MINING.slow_fast_mix~~`、`~~add(multiply…)~~`、`~~慢变量×快变量加权混合~~`）——agent 若忽略 Markdown 渲染会读成正向指令 | 删除线文字全部移入 CHANGELOG |
| RD-13 | D4 行 1–3 | 职责·P2 | S0 有三个入口名：`score_datasets.py --campaign-dir`（此处称“权威”）、`workflow_campaign(S0)`（SKILL）、`s0-select`（SKILL 称先行步骤）；D4 未提 calibrate 与 s0-select 的先后 | 一句话顺序：s0-select → calibrate → 打分（score_datasets 即 S0 节点内部） |
| RD-14 | D4 行 6–8（L63–65） | 边界·P1 | `usableFields<5 → excluded（mode 无关）` 与行 8 “fields<5 → tier2 探针例外”、SKILL“fields<5 标仅条件腿”、步 3“字段数<10 退回”：**同一指标 5 与 10 两个阈值、三种处置**；0.65/0.85/0.9/50/6 均无依据 | 一张“字段数/覆盖率 → 处置”表，并给阈值出处 |
| RD-15 | D4 行 9 vs SKILL 步 2 #0 | 边界·P2 | “用户指定数据集与白名单冲突 → 用户优先”，而步 2 #0“已点亮塔不进白名单（用户定案，硬规则）”也是用户指令；两条用户指令冲突时以**时间在后者**为准未写 | 加一句：后到的显式用户指令覆盖先前的“定案”，并记 `override` |
| RD-16 | D4 行 10（L67） | 逻辑·P3 | “本地 MCP 127.0.0.1:8876 宕机 → `--mode direct`”写死环境；云端/其它环境为 stdio | 改为“MCP 不可达 → …”，具体端口放环境章 |
| RD-17 | D5 行“中性化”（L76） | 边界·P1 | “对照轨可探 COUNTRY / **ILLIQUID_MINVOL1M** / delay0”——SKILL 步 6 已写 ILLIQUID_MINVOL1M 对 USA/ASI/EUR **永久停提**（2026-09-14 公告）；“decay: returns 4 / close 6”“truncation 0.08”为写死默认，而 settings-prior 会按库存实测改写；“universe 区域合法档”整表重复 `config.REGIONS`/`region_config.json`（且 HKG 写 TOP500/800，而 HKG profile 写 `universe: []` 待实测） | 删 ILLIQUID；默认值改“见 settings prior / region_config”；universe 表删除改引用 |
| RD-18 | D6 行 1、行 2（L93–94） | 边界·P1 | “**`hump` 已废弃禁用**”与 SKILL 步 4 预闸对 `hump(x,k)` 做**改写为 `hump(x, hump=k)`**、步 5 说“此前只拦 hump 不拦 bucket”——算子到底能不能用？ | 明确：hump 仍受支持但必须命名参数（预闸自动改写）；“废弃”说法删除或指明是哪个用法 |
| RD-19 | D6 行 5（L96）与 D2 行 6 | 边界·P1 | 把 `subtract(rank(慢), rank(快))` 称为“**单信号结构**”并作为 CW 的合规改法——与“两条独立腿相加”仅差符号（见 RA-89） | 同 RA-89 的可检判据 |
| RD-20 | D7（L99–106） | 边界·P2 | S2-D 在 SKILL 反模式里是“旧 S2-D/S2-M 必跑”的禁项，这里仍有完整决策表；`enter_multi_dataset`（≥15 / 0.7 / 0.8）会把流程推向跨集混合，与单集 atom 优先冲突；阈值无依据；`PPAC` 未定义 | 标注“可选、默认关闭”；给阈值依据；写明与 CLAUDE.md 的关系 |
| RD-21 | D8（L108–119） | 边界·P1 | 行 4“回收筛选后立即**追加 `WAVE_LEDGER.md` + `ledger.json`**”、行 6“下一波前先**读 `WAVE_LEDGER.md` 的『下一波决策』节**”——与 SKILL/AGENTS 的“战役产物只入 wqb.db、不写 json”冲突；`WAVE_LEDGER.md` 现只是 `tools/export_wave_ledger_md.py` 的**导出视图**（`tracking/EUR|USA` 有，且路径在此文写成 `WAVE\_LEDGER.md` 带转义反斜杠，机械检查解析不到）；步骤 0 的 `check_ledger_sync.py` 存在两份（tools/ 与 toolkit/scripts/） | 行 4/6 改成 `upsert_wave_result` / 读 `wave_results`；WAVE_LEDGER.md 只作导出；`check_ledger_sync` 只保留一份并指路 |
| RD-22 | D8 体裁（L108） | 逻辑·P3 | “决策表”里放了 0–6 的**步骤清单**（非 条件→动作）；行 2 同时讲 7 批并行、8 条上限、prod-first、配比，行 5 又重复配比与“弱探针≤1” | 步骤清单归入 SKILL 步 6；D8 只留 3–4 条真正的决策（何时补组合批、何时扩到 8） |
| RD-23 | D9 行 6（L130） | 边界·P1 | “PPA 提交：仅当主题匹配且用户确认”——未提**合法 PPA 只能走平台 web UI**（submit/robustness 两个 skill 已写）；agent 会尝试用 MCP 提交 | 补渠道限制 |
| RD-24 | D10（L134–142） | 边界·P2 | “持久化 artifact 与 verdict **到 state**”（state json 已废）；“每 15 轮回测做一次多样性评估”“C 实测约 5–7”与 `CONCURRENCY.slots=7`；“不创建自动化任务（用户未要求时）”是好边界但被埋在“迭代纪律”里 | “到 state”改“到 DB”；15 轮给依据或删；并发引用 wqb-concurrency；把“不创建自动化任务”提为文首红线 |
| RD-25 | D11 头注与行 1、8（L144–161） | 逻辑·P2 | 整表建立在**已废止的加权混合配方**上（头注自己承认“此为历史配方”），仍占 18 行；“70% 精力做配方家族扩展”的“精力”不可操作；“腿禁用≠整集判死”“慢腿/快腿”未定义；`group_zscore(慢, sector)` 未提 JPN 的非法 group 字段 | 把仍有效的两条抽成规则（“主导字段不变→SELF≥0.9 不做”“换主导信号源才算差异化”），其余归档；补区域例外 |
| RD-26 | D12 行 1–4、D2、停止规则 | 边界·P2 | “判死”阈值散落：D2 <0.8、D12 全方向 \|sh\|<0.6、signal_floor 缺省 0.5、`yield=0 且 bt≥8`、`0.5` fast_kill——**没有“判死”的统一定义** | 建“判死判据表”：对象（表达式/族/集/区）→ 判据 → 记录位置 |
| RD-27 | D13（L172–181） | 职责·P2 | 是 S1 前置体检的核心规则（longCount≥80、稀疏事件 CW 无解、新集先 1 条单仿真），但 SKILL 步 3 没有引用它（只引 D0/D2 等）；profile 又有 `longcount_min` 覆盖 | 在步 3 增加“D13 检查项”并与 profile 覆盖对齐 |
| RD-28 | D14 行 2（L188） | 边界·P1 | “镜像稀释：加一条相关≈0 的稀释腿”与“禁止任何加权混合/等权 leg-add”**直接冲突**；引用的 `docs/experience/prod_wall_breakthrough_sop.md` **不存在**（docs/experience 下只有 fail_fast_rules / field_operator_pattern / region_template_kb） | 要么删该行，要么把它改写成合规形态（条件门控/分组）并补文档 |
| RD-29 | D14 行 2b（L189） | 逻辑·P2 | 关键证据是 0.7003→0.6993（差 0.001），且同文档另一处（SKILL L663）显示 prod 会因外部提交在 1 小时内 0.6997→1.0000——单次 0.001 的差异不足以支撑“行业暴露是拥挤接触面” | 标注证据强度（n=1、差值在测量噪声内），降级为“可试”而非规则 |
| RD-30 | 全表 | 职责·P2 | 与 SKILL 的对应关系没有索引：SKILL 只引用了 D0、D2；D1/D3/D4–D14 是否被步骤消费、由谁消费，读者无从知晓 | 每个 D 表头加“被 SKILL 步 N 引用”；SKILL 每步末尾列“适用决策表：Dx” |

#### 1.16 `references/ra-campaign-prompt.md`（120 行）

**总评**：它是用户/agent 的**入口提示词**，却是 2026-09-11 的快照（自带 `last_verified: 2026-09-11`），落后 SKILL 17 天、少了 09-17/19/23/25/27/28 的 6 批硬规则。入口过时 = 新会话从第一句话起就绕过最新闸。**它还自带 `name: ra-campaign-prompt` 的 skill 式 front-matter**，易被加载器/同步脚本当作独立 skill。

| # | 位置 | 维度·级 | 问题 | 改进建议 |
|---|---|---|---|---|
| RP-01 | L13–20 铁律 #1 | 逻辑·P2 | “不复制数字”，但主提示词自身含 13/13、≥2 非 MODEL、0.9–1.15、≥50/10–49/0–9、min(7,批数)、≥0.7 等十余个字面数字；铁律 #3 的“99%”无出处 | 主提示词也只写引用；或明确“经验阈值允许，须带出处” |
| RP-02 | L40–44 步 0 | 边界·P2 | “步 0”不存在于 SKILL 的九步；`operator_audit`（平台算子表审计）被当成“幽灵算子”检查，而 SKILL 步 5 的 `ghost-audit` 是**表达式级**检查——两者不同 | 步 0 改称“步 1 开工前置”；区分平台算子审计与表达式幽灵审计 |
| RP-03 | L47–49 步 2 | 边界·P1 | 缺 SKILL 步 2 的五项新规：calibrate、**已点亮塔不进白名单**（09-19 用户定案）、体检包前置与 `--inspect-mode`、座位可达性、饱和路由 | 用“见 SKILL 步 2 硬约束 0–7”替代抄写；或自动生成 |
| RP-04 | L50–51 步 3 | 边界·P1 | 把 `workflow_feature_engineering` 列为步 3 动作；SKILL 明确它**按需、仅人读、禁注入 GEM**（否则 GEM 退化为模板展开）；且完全没有 **闸 SEM 前置：`field_semantic_classify`**（缺失即 exit 2 拦整波） | 步 3 改：typed catalog + 字段语义归类；feature_engineering 标“可选、产物不得注入” |
| RP-05 | L52–53 步 4 | 边界·P1 | “workflow_gem（强制，**带 priors**）”与 SKILL L377“priors_file 已可省略”矛盾（同 RA-47）；七槽“≥1 按 win 换腿”与 SKILL 硬约束 #1“≥2”不一 | 与 SKILL 对齐后以引用代替 |
| RP-06 | L54–56 步 5 | 逻辑·P2 | 顺序与 SKILL 相反（先 wave_gate，再“CLI 兜底 ghost-audit”）；ghost-audit 不是 wave_gate 的兜底而是**先行独立闸**；缺闸 SEM / 闸 PF / 闸 2b | 按 SKILL 的 ①ghost-audit ②wave_gate 排序；闸清单引用唯一闸表 |
| RP-07 | L59–63 步 7/8 | 边界·P1 | ①链缺 `check_correlation`（SKILL 有）；②撞 prod 墙“按 D14 三条路径”——与 SKILL 5b“不做任何去相关变体”冲突（入口提示词在**教 agent 做 5b 禁止的事**）；③“submit_verdict（**唯一权威**）”是第 4 处该词；④“提交前 Failed RA==0 + `submit_verdict` **200**”把 verdict 当 HTTP 状态 | 与 RA-03/RA-69 一并统一 |
| RP-08 | L64、L120 | 边界·P1 | 步 9 只列三件回写 + pyramid，**缺 assemble-priors 刷新与 dataset-experience（SKILL 的两项完成定义）**；验收表要求 `s6_verdict_<wave>`——该 key 已于 09-28 废止 | 步 9 与验收表改引用 SKILL 的“S6 完成定义”；删 `s6_verdict_` |
| RP-09 | L69–70 停止条件 | 边界·P2 | “连续 3 波 gate 通过率 0 → 停并给结论，**不要自行换区**”，而 SKILL 循环表同一行写“转 matrix 换数据集，或 next-move 换区域” | 二选一并统一 |
| RP-10 | L66–67 每步输出格式 | 逻辑·🟢 | “\| 步 \| 动作 \| 命令/MCP \| 产物 \| 通过? \| 失败分支 \|”**是全库最好的步骤模板**（把“验收条件”写进每一步） | 提升为 SKILL 的每步固定模板（RA-10），此处只留一行引用 |
| RP-11 | L78–108 场景变体 | 情景·P2 | 2.1–2.4 是好的情景化写法，但：2.2 发批“跳过步 1–4”与 SKILL 快捷入口“跳过 S0–S2（步 2–4）”不一致，且都没提闸 SEM/体检包会拦；2.3“Mode B 70%/Mode A 30%”比例无解释；2.4“ET 日界 21:30”与 00:00 ET 重置并存 | 每个场景末加“常见卡点”一行（如 2.2：SEM 缺台账→先跑 classify）；比例给含义 |
| RP-12 | L99 闸位映射 | 职责·P3 | “Sharpe/Fitness→信号强度；Turnover→平滑/窗口；PROD/SELF→D14；CW/SubUniverse→分散化骨架”是有价值的**失败点→修法族**映射，却只存在于提示词里 | 移入 brain-alpha-repair / how-to-pass，并双向链接 |
| RP-13 | L110–120 验收清单 | 情景·P2 | 缺：SEM/体检包、5b prod-first、assemble-priors 刷新、dataset-experience、QUICK 产物隔离；“`submit_verdict` 200”措辞错误 | 验收表按 SKILL 各步“完成定义”生成 |

#### 1.17 `references/webdatascope-failed-gates.md`（75 行）

**总评**：短小、边界清楚（“不得用用户阈值替代资格门”“未清零不得 `set_alpha_properties`”是好规则）。但它是**被代码取代后仍被当权威引用**的文档，且缺一个关键边界（PENDING）。

| # | 位置 | 维度·级 | 问题 | 改进建议 |
|---|---|---|---|---|
| RF-01 | L12–34 | 边界·P1 | RA 清单只有 **17 项，缺 `LOW_ROBUST_UNIVERSE_SHARPE.WITH_RATIO`**；`config.RA_CHECK_NAMES` 是 18 项，且源码注释记录“漏计时 23 条‘零硬闸失败’候选里误放 3 条”。按本文手工数会重现该事故；PPA 清单却含该项（7 项一致） | 补第 18 项；更根本：本文只写口径，名单“以 `src/wqb/config.py` 为准”并加测试校验两者一致 |
| RF-02 | L3 | 逻辑·P3 | 来源写 WebDataScope **1.3.1/1.0.6**，config 注释写 **0.10.20**——版本引用不一致、且都是仓外代码，无法复核 | 统一到 config 的引用并注明核对日期 |
| RF-03 | L14、L38 | 情景·P2 | 口径“result 既非 PASS 也非 PENDING 才计失败”意味着 **PENDING（仍在计算）不计入**——这与平台行为一致（submit-alpha 关键坑 #2、selfcorr-quick 已实测：`PENDING` ≠ `FAIL`，**不挡提交**），且 `SELF/PROD_CORRELATION` 不在 `RA_CHECK_NAMES` 内，所以该口径本身合理。缺口在于**语义没有说透**：当**名单内**的检查仍为 PENDING 时，`Failed RA==0` 只表示“暂无失败”而非“已通过”（例如提交响应 ② “IS checks still computing”）；文中没有规定此时调用方应等待、复查还是放行，`submit_verdict` 源码里也没有 PENDING 分支。若一刀切把 PENDING 当失败，会与平台“不挡提交”相反并阻塞可提交候选 | 不改口径；在 `compute_webdata_failed_counts` 输出里增加 `pending_ra / pending_ppa`（数量 + 名称），文中规定：`Failed==0` 且 `pending==0` = 已通过；`Failed==0` 且 `pending>0` = 待复查（重跑 `get_alpha_details`，超时则按未决处理，不据此判死也不据此放行）；给一个 PENDING 场景示例 |
| RF-04 | L50 | 边界·P2 | “LOW_SHARPE value<1 计 PPA 失败，不论显示状态”——只覆盖 PPA，RA 侧对 LOW_SHARPE 的 value 判据未说 | 一句话说明 RA 侧仅认 result |
| RF-05 | L52–73 伪代码 | 逻辑·P3 | 与 `config.compute_webdata_failed_counts` 重复（第二份实现的文字副本），且没指向它 | 删伪代码，改一行“实现见 `compute_webdata_failed_counts`” |
| RF-06 | 全文 | 情景·P3 | 全英文（其余全中文），SKILL 引用它作为“规则见此” | 保留英文可，但首行补中文一句用途与适用步骤（步 8 资格门） |

#### 1.18 `references/concept-taxonomy-map.md`（29 行）

| # | 位置 | 维度·级 | 问题 | 改进建议 |
|---|---|---|---|---|
| RT-01 | 标题、表 | 逻辑·P2 | 标题“hypothesis **12 类**”，表中实际只出现 10 个类名（slow_diffusion、regime、propagation、urgency、over_reaction、dispersion、cross_dataset、information_asymmetry、horizon_spread、residual）；对照 hypothesis-first 的 12 类，**`under_reaction`、`event_conditional` 两类未映射**，读者无法知道是遗漏还是不适用 | 补齐或注明未映射类及原因 |
| RT-02 | L19 | 逻辑·P2 | “一次生成**只挂一套**主分类”，同句又要求“**同时**标 `dfe_question` 与 `hypothesis_class`”——自相矛盾 | 改为“主分类=1，另一套作副标签” |
| RT-03 | L24 | 边界·P2 | 引用 `validator.check_batch` 作“批级 shape 判重”——SKILL 步 5 已宣告它零调用方、仅作方法论参考；此处仍当有效机制 | 改引 gate.py 闸 6 `check_batch_diversity` |
| RT-04 | 第 4 行 “交互/组合” | 边界·P2 | 把“组合腿（slow×fast spread）/ subtract(rank A, rank B)”列为标准概念位，与 RA-46/RA-89 的加权混合与 leg-add 规则冲突；“GEM 七槽配给”是又一个“槽”（概念槽） | 注明该概念位只能落成**条件/分组/对偶价差**；术语框区分“概念槽/并发槽/波内配额” |
| RT-05 | 位置 | 职责·P3 | 文件放在 ra-pipeline/references，被 hypothesis-first（以“ra-pipeline references/concept-taxonomy-map.md”纯文本提及，非链接）与 dfe 引用；三个本体 skill 均不链接它，维护规则（“新增类必须同步本表”）无人触发 | 三处本体 skill 各加一行链接；加一致性测试（类名集合 ⊆ 映射表） |

#### 1.19 `references/prod-corr-avoidance.md`（80 行）

**总评**：§7（排队调度）是全文最有操作性的部分；§1–§6 是 2026-08-05 的 GLB 实验流水账，结论已被后来的规则（5b、闸 PF、D14）**部分取代、部分相悖**，且 §3 含有**危险的过期指令**。

| # | 位置 | 维度·级 | 问题 | 改进建议 |
|---|---|---|---|---|
| RC-01 | §3 #1、#3（L28、L31） | 边界·P1 | 教 agent 用“**POST /alphas/{id}/submit 触发 prod_corr 计算**”“提交前先 GET 或 POST 触发计算”——GET 提交视图已证实恒 404，POST 若通过就是**真实提交**。这是“POST=零成本探针”误解的源头（SKILL L685 延续之） | 删 POST/GET 探针说法；prod 一律用 `check_correlation(production)`；POST 仅在用户确认后作真实提交 |
| RC-02 | §1 标题与第 2 行 | 逻辑·P2 | 标题“已确认超标”，第 2 行是“未触发（同族高概率 >0.7）”——推测混进“已确认”表 | 分“已确认/待验证”两表 |
| RC-03 | §3 #4 vs D14 | 边界·P1 | “同族不重复投入，不再投任何变体”与 D14 路径 1/2/2b（变体去相关）相悖 | 纳入统一 prod 墙处置表 |
| RC-04 | §4 | 边界·P2 | “GLB 黄金配方”margin 5.0–5.1bp，低于 `GATES_INTERNAL.margin_bp_min=10`；且该族在 §6 被判“已穷尽-规避”，配方未标废止 | 标注“仅历史；该族已判死；margin 不达内部线” |
| RC-05 | §5–§6 | 逻辑·P2 | §5“待验证实验”与 §6“决定性实验——失败”并存（假设与其证伪都留着）；“已投入 b10-b19”“10 个 PPA 目标不可达”是会过期的状态 | 只留 §6 结论；提炼通则“信号强度、可打磨性、prod_corr 三者不可兼得”；流水账移 experience log |
| RC-06 | §7 | 边界·🟢 | 有触发、现状、4 条强制纪律，可直接执行（含缓存/`refresh=True`/`from_cache`）——**范例**；但含 Redis 键名等实现细节，且被放在文末 | 提前到文首作“如何跑 prod”，实现细节折叠 |
| RC-07 | 全文 | 职责·P2 | 与 SKILL 5b、步 6 #4、步 7 prod-first、闸 PF、D0/D14 共 6 处谈 prod，无一处是“总纲” | 本文改写为**prod 总纲**：判据表 + 处置表 + 排队纪律，其余处只引用 |

#### 1.20 `references/regions/*.md`（13 个 profile，共 1016 行）

**总评**：结构统一（13/13 有“定位与实证依据”“流程变体”，“步 N 注入”式小节很适合“按步骤查区域差异”），是全库**最好的按区分层范式**。但存在三类系统性问题：①front-matter **看似配置、实为文档**；②front-matter 与正文**新旧不同步**；③正文按时间**追加**，硬规则被埋在证据之后。

| # | 位置 | 维度·级 | 问题 | 改进建议 |
|---|---|---|---|---|
| RR-01 | 全部 profile 的 front-matter | 边界·P1 | SKILL 说 front-matter“声明静态配置/闸门覆盖/循环策略”并“注入”步骤；实测（全仓 grep）**只有 `entry_verdict` 被代码读取**（`region_rotation.py`、`region_status.py`）；`gate_overrides`（cw_gate/longcount_min/prod_corr_early_warn）与 `loop_policy` 无任何代码消费。且 13 个 profile 里 12 个 `longcount_min: 80`、`prod_corr_early_warn: 0.7`（=全局默认），只有 USA=0.6；`cw_gate: WARN/FAIL` 的含义（仅本地？平台照 FAIL）未定义 | 给每个键标注 [代码]/[文档]；要么接线（wave_gate 读 `gate_overrides`），要么删除等同默认的键；定义 `cw_gate` |
| RR-02 | USA 步 6 注入（L38–40） | 边界·P1 | “预警线 0.6：≥0.6 即**停扩换腿**”，与 SKILL 5b/L663“prod 0.60–0.70 → 当天提交、不做变体”直接冲突；SKILL 又规定“profile 与正文冲突时 profile 优先”——于是 USA 的 0.60–0.70 候选按规则应**停扩换腿**，恰是 IND 事故（0.6997 → 1.0000）的反面教训所禁止的 | 明确适用范围：`prod_corr_early_warn` 只用于**扩批前**的家族级判断，已成型候选一律按 L663 当天提交；写进 USA 与 SKILL 各一句 |
| RR-03 | IND front-matter vs 正文（L16–19 vs L103–105） | 边界·P1 | front-matter 仍把 `mdl177`（model 塔）与“慢变量基本面集”列为 `green` 与 `signal_families_include`，而正文（09-19 用户定案）说 model/fundamental 等**已点亮塔不再作主数据集**——同一文件里配置与规则相反；`last_verified: 2026-08-25` 未随正文（09-19）更新 | front-matter 与正文同步；`last_verified` 改为**每次编辑必更新**并加校验 |
| RR-04 | 所有 profile 的 `empirical_anchor.last_verified` | 逻辑·P2 | 至少 USA/HKG/IND 均为 2026-08-25（批量戳），与 SKILL 的 09-28 批量戳同类：戳不区分“通读核对”与“机械刷新” | 戳改为“最近一次**内容**核对：日期+核对人/命令”，批量刷新不得改戳 |
| RR-05 | IND L59–121 | 逻辑·P2 | 章节顺序是**写入时间序**（避坑清单在中部，“战役选集硬规则”在倒数第 3 节）；agent 读 IND 想查“能挖什么”要翻过 60 行证据 | 固定 profile 模板：定位 → **硬规则（含用户定案）** → 流程变体 → 避坑 → 证据附录（按日期折叠） |
| RR-06 | IND L52 | 情景·P2 | “IS Sharpe 1.0–1.25 但 2Y ≥1.5 的候选不降格、不判死，进 Mode A”——没说这类候选最终**靠什么过 LOW_SHARPE/IS_LADDER 检查**（全局 Sharpe 线 1.58）；读者会以为 IS 1.0–1.25 可提交 | 补一句最终过闸路径与不适用情形 |
| RR-07 | IND L95 | 逻辑·P3 | 表格行内含 `|ts_mean(P,252)|` 未转义，GFM 会把该行拆列 | 用 `abs(...)` 或转义 |
| RR-08 | IND L109–121 组腿配方 | 情景·🟢 | 用 `trade_when` **慢开关**（月/季频变量切掉约一半宇宙，进 >0.5/出 <0.4 滞回带）作辅助腿，并给“无效结构”反例（bucket 重排、快变量门控、两边为空的门控）——**正是 RA-90 缺的“辅助腿如何入场”的范例** | 抽成全库通用的“辅助腿入场三式”并回链本节为例 |
| RR-09 | HKG（universe 待测）、TWN（无 tracking 目录）、MEA（frozen） | 边界·P2 | HKG `universe: []`（“实测”）而 D5 已写 HKG TOP500/800；TWN 有 profile 无 `tracking/TWN/`；SKILL“三者对齐表”未体现 | INDEX 区域表增“缺口”列；缺口区域的步 1 行为写进 profile |
| RR-10 | 全部 | 边界·P3 | `fast_kill: 新数据集 8 探针无 |S|≥0.5 即判死` 在多数 profile 复制粘贴；与 D12（<0.6）、signal_floor（0.5/1.2/0.9）阈值不同源 | 提到 SKILL“判死判据表”，profile 只写差异 |

<a id="s2"></a>
### 2. `wq-brain-campaign-matrix`（L-PRE · 143 行）

**定位**：S0 之前的“区域×数据集查表层”，并负责把判死/胜绩回写 registry。

**总评**：篇幅小、结构清晰（职责边界 / 衔接协议 / 数据文件 / 五步工作流 / 硬规则 / 边界 / 闭环），但**职责自相矛盾**——同一份文件里既说“只查表”又说“负责回写”、既说“S6 负责回写”又说“本 skill 的 §4 回写”，并且把 ra-pipeline 的九步派发链整段复制了一遍（已与 ra-pipeline 不同步）。schema 描述（表/层）与代码不符（`cross_region_lessons` 表已废弃）。缺失败分支与示例（机械检查 §H：无“失败/示例”节）。

**阶段热力图**

| 阶段（行号） | 书写逻辑 | 职责划分 | 边界界定 | 需情景规范？ |
|---|---|---|---|---|
| frontmatter / 头部（1–20） | 🟡 | 🟡 | 🔴（触发词与 ra-pipeline 重叠） | 是 |
| 职责边界 + 定位（22–32） | 🟡 | 🔴 | 🔴 | 是 |
| 衔接协议（34–39） | 🟡 | 🔴 | 🔴（PROD 标注无 schema、无消费方） | 是 |
| 数据文件 / 三层结构（41–60） | 🔴（两套 schema 并存） | 🟡 | 🔴（描述过期） | 否 |
| 工作流 1 解析输入（64–80） | 🟡 | 🔴（选区归谁） | 🟡 | 是（region 缺省） |
| 工作流 2 生成配置包（82–92） | 🟡 | 🟡 | 🔴（示例违反自身“强制”） | **是（给完整样例）** |
| 工作流 3 派发（94–95） | 🔴 | 🔴（复制编排链） | 🔴 | 否（应删除） |
| 工作流 4 回写（97–123） | 🟡 | 🔴（回写多头） | 🟡 | 是（写什么/不写什么） |
| 工作流 5 扩区（125–126） | 🔴（步骤不可执行） | 🟡 | 🔴（三处 vs 四处） | 是 |
| 硬规则（128–133） | 🟡 | 🟢 | 🔴（JPN 事实错误；与用户优先级冲突） | 是 |
| registry 与台账边界 + 闭环（135–143） | 🟡 | 🔴 | 🔴（submit_ready 三个家） | 是 |

| # | 位置 | 维度·级 | 问题 | 改进建议 |
|---|---|---|---|---|
| CM-01 | L2–10 frontmatter | 边界·P2 | 字段顺序与其余 skill 不同（`last_verified` 先于 `name`）；description 后半是“它做什么”（解析配置包、原样派发 S0–S6、回写 registry）而非“何时触发”，且含断句空格；触发词“开战役/campaign/任何新挖掘战役开始时”与 ra-pipeline 重叠，任何战役起点两者都可命中；`allowed-tools` 缺 `mcp__wqb-db__*`，而正文要求“读全走 `mcp__wqb-db__*`” | 描述改为“区域已定、需要 dataset/死路/胜绩配置包时使用”；工具清单与正文对齐；统一 frontmatter 字段顺序（由 sync 脚本校验） |
| CM-02 | L12–20 | 逻辑·P3 | 6 个空行；运行环境一句话放在 H1 标题**之前** | 移入“运行环境”小节 |
| CM-03 | L24 vs L143 vs L139 | 职责·P1 | 三种说法互相矛盾：职责边界“**本 skill 负责** … 战役后回写 registry”；§4 与 L139“**由本 skill 的 §4 回写流程**提炼判死结论”；L143“**S6 负责回写，本 skill 负责读取**”。同时 ra-pipeline 步 9 又让 agent 用 `upsert_registry_empirical` / `seal_dead_end` / `add-win` 回写。同一件事三处认领 | 定唯一归属：**registry 的读取与写入规范（schema、ID 命名、幂等 CLI）归 matrix；触发时机与“该写什么”归 S6/ra-pipeline 步 9**。职责边界里删“回写”或改成“提供回写规范” |
| CM-04 | L32 | 逻辑·P3 | “既有 **31 个**其他 skill”硬编码（现为 33 个 SKILL.md，INDEX 有 32/33 两种说法）；“只做查表与回写、不执行挖掘”在 L24、L32、L36 三次重复 | 删数字；边界句只保留一处 |
| CM-05 | L37 vs L98 vs L133 | 边界·P1 | 写入路径：L37“走 `campaign.py registry` 幂等 CLI **或** 会话内 `upsert_registry_empirical`”；§4 与硬规则 4“**一律**走 CLI”。“或”与“一律”冲突；而 ra-pipeline 步 9 的示例用的是 MCP 那条 | 二选一（推荐 MCP 优先、CLI 用于批量/脚本），并在两个 skill 里统一措辞 |
| CM-06 | L38 PROD 饱和标注 | 边界·P1 | 单个 ≈750 字 bullet 含两条规则 + 工具指针：①“强制”标注 `prod_risk: high` / `prod_saturation: likely`，但**没有 schema**（键名、取值集合、写到哪）、**没有消费方**（S2 只是“供参考”）；②“风格同质”无判据；③`min_sharpe=1.58` 字面阈值；④“统一计算入口 = `tools/region_status.py`”却让 agent 手工调两个 MCP 查询——与“勿另写第三份实现”矛盾；⑤§2 的配置包**样例里根本没有这两个字段**，违反自己的“强制”；USA profile 引用“matrix §输出契约”，本文并无该节 | 给配置包一个固定字段表（含 `prod_risk`/`prod_saturation` 取值与来源=`region_status.py` 输出）；样例补齐；判据引用 `region_status` 的口径；删 1.58 字面值 |
| CM-07 | L39 | 边界·P2 | “S0 健康检查 = `wq-brain-ppa-mining` §1.0 硬门槛方法论 + `score_datasets.py`”——把 PPA 专用阈值（cov≥0.85/alphaCount≤50/fields≥10）当成所有战役的 S0 方法论，而 ra-pipeline/D4 的 RA 体检阈值是另一套（cov≥0.65 等） | 分“RA 用 D4 / PPA 用 ppa-mining §1.0”；配置包写明 `mode=regular|ppa` |
| CM-08 | L41–60 | 逻辑·P1 | **两套 schema 并存**：表格说 4 张表（`regions`/`datasets`/`registry_empirical`/`cross_region_lessons`），下文又说“三层结构（`registry_empirical.payload` 内部）：static/assets/empirical”；“层”既指 `registry_empirical.layer` 列（dead_end/win/orphan/campaign），又指 payload 里的三层。代码核对：`cross_region_lessons` **表已废弃**（`_schema.py:224`：迁入 `registry_empirical layer='cross_region'`），故 registry 至少 5 个 layer；static/assets 在 `regions`/`datasets` 表而非 registry payload | 重写为一张“存储地图”：概念 → 表/layer → 读工具 → 写工具；“层”一词只留给 `layer` 列，其余改称“类别” |
| CM-09 | L52 | 逻辑·P3 | 一段里含历史（2026-08-21 起单轨、JSON 已归档）、读法（MCP 或裸 SELECT）、写法（CLI）、迁移工具（migrate_phase2.py）；提到的 `campaign_registry.json` 触发机械检查“路径不存在” | 历史移 CHANGELOG；读法只保留 MCP；归档路径写成“已删除”而非文件名 |
| CM-10 | L65 | 职责·P1 | “region（**必须**）”，却又在 ra-pipeline 三角分工里被定义为“**where=查表选区**选集”。matrix 无法选区（region 是入口参数）；真正的选区工具是 `region_rotation.py`/`region_status.py`/next-move。“意图缺省时找 untried/in_progress **最高优先级**项”——campaign 层只有 status 三值，没有优先级字段 | ra-pipeline 三角表改“matrix = 给定 region 后选集”；缺 region 时明确回问用户或转 next-move；删“最高优先级”或定义排序键 |
| CM-11 | L68–80 | 逻辑·P3 | 只给调用，没说返回结构与空结果的含义（`get_region_config` 返回空 = 新区？） | 每个调用后加 1 行返回摘要与空值处理 |
| CM-12 | L83–92 配置包样例 | 情景·P1 | 自由文本样例，缺：`prod_risk/prod_saturation`（强制项）、`entry_verdict`（profile）、`lit_towers`（09-19 硬规则）、设置来源；“neutralization=STATISTICAL(或数据集 dominant)”中“dominant”无定义；“候选数据集=status=untried”**忽略了已点亮塔与跨区弱先验**——若被 S0 当作白名单会直接违反步 2 硬约束 0 | 给完整样例（含各字段来源）；注明“候选=待 S0 筛选的**超集**，不是白名单” |
| CM-13 | L94–95 派发 | 职责·P1 | 把九步派发链**整段复制**（步 2–9 的工具名），与 ra-pipeline 已不同步：仍写步 3 用 `workflow_feature_engineering`（ra-pipeline 已改为按需/禁注入 GEM）、步 8“`submit_verdict` + 用户确认后 `workflow_submit_alpha`”（缺 Failed-RA 资格门与 4 态处置）、无闸 SEM/5b。matrix 声称“不执行”，却写了执行链 | 整段删除，改一句“把配置包交还 ra-pipeline 步 2”；维护一份编排链足矣 |
| CM-14 | L98–121 命令 | 逻辑·P2 | 代码块标 bash、用 `\` 续行，正文却规定 PowerShell；`campaign.py` 裸写，前文说 `$WQ_TOOLKIT_DIR/campaign.py`；示例 ID `MEA-PV106-SPREAD-DEAD` 只是例子，**ID 命名规则没写**（而 ra-pipeline 步 9 的 `seal_dead_end` 需要同一 entry_id）；`add-win --date 2026-08-21` 写死日期；`--key` 是自由文本，而 assemble-priors 需要 `skeleton/evidence/settings` 结构 | 统一 PowerShell 写法与 `$WQ_TOOLKIT_DIR`；定义 ID 规则（REGION-数据集-族-DEAD）与 `--key` 的结构化格式；日期改占位 |
| CM-15 | L123 | 情景·P2 | “只记有跨会话价值的结论，不记过程性噪声”——判据抽象 | 给 3 正例（带 rule 的 dead_end、可复用 win 配方、数据集 exhausted）+ 3 反例（单波 FAIL、单条 alpha 未过闸、参数扫描结果） |
| CM-16 | L125–126 扩区 | 情景·P1 | 步骤**不可执行**：①数据源 `research-data/fresh_datasets_7region.json` 不存在（机械检查）；②“复制到 assets 层/static 层用 `get_platform_setting_options` 实测”只有**读**，无任何**写** `regions`/`datasets` 的命令（§4 只覆盖 dead_end/win/campaign/orphan）；③清单说“三处缺一即漂移”（profile + INDEX + registry），ra-pipeline 说“profile + `tracking/<R>/config/`”，实际还有 `config.REGIONS` 与 `region_config.json`——**同一件事三份清单**；TWN 就是缺 `tracking/` 的实例 | 提供“开新区检查表”单一来源（放 INDEX），列全部落点与验证命令；补写 `regions`/`datasets` 的工具或脚本 |
| CM-17 | L130 硬规则 1 | 逻辑·P2 | “以更新 registry 为准”歧义（以“更新后的 registry”为准，还是“去更新 registry”？） | 改“与 registry 冲突时以 registry 为准，并在发现处修正来源文档” |
| CM-18 | L131 硬规则 2 | 边界·P2 | “死路 rule **优先于用户直觉**”与 ra-pipeline/decision-table 的“用户显式指令 > 决策表”冲突 | 统一：提示一次依据；用户坚持则执行并记覆盖 |
| CM-19 | L132 硬规则 3 | 边界·P1 | 说“AMR/**JPN** 本工作区未启用（无 profile、无战役目录）”——JPN profile 已于 09-15 补齐（ra-pipeline L62），JPN 有 profile、有战役目录；ra-pipeline 则说“只有 AMR 未覆盖”。两个 skill 对区域覆盖事实不一致 | 区域覆盖只在 INDEX 维护；此处写“见 INDEX §区域清单” |
| CM-20 | L128–133、L37、L52、L139 | 逻辑·P3 | “禁止散装 SQL”出现 5 次 | 保留一处（硬规则），其余引用 |
| CM-21 | L137–138 | 边界·P1 | 同两行内自相矛盾：“submit_ready … **进战役台账（ledger_kv）不进 registry**”与“registry schema 约定：region 级可增 … `submit_ready[]`（达标缓冲池镜像）”；而代码里 `submit_ready` 是**独立 SQL 表**（`src/wqb/store/submit_queue.py`），决策表又说 ledger_kv，ra-pipeline 用 `submit_ready_blocked` 键——**一个概念四个家** | 统一为 SQL 表 `submit_ready`（唯一事实源），其余处删除或标“已废止镜像” |
| CM-22 | L137 vs ra-pipeline L358 | 职责·P1 | matrix 硬规则 1 说 **registry 是“唯一事实源”**；ra-pipeline 步 4/9 说 **DB KB（`region_kb`/`template_kb`，ledger_kv）是 S2 先验“唯一上游”**，并要求 S6 回写 `region_kb`。win/dead 两处各自“唯一”，二者关系（谁派生谁、何时同步）没有任何文档说明；代码里 `assemble-priors` 读 `region_kb` 而非 `registry_empirical` | 写一句同步关系：registry 是事实层，`region_kb` 是由它+波次统计派生的**先验快照**；给出刷新触发点 |
| CM-23 | L141–143 | 职责·P2 | “S6 均走 toolkit 幂等 CLI”，而 ra-pipeline 步 9 示例是 MCP `upsert_*`；“未回写的复盘视为未完成”与 ra-pipeline 完成定义重复但口径不同（前者只要求回写，后者还要 assemble-priors + dataset-experience） | 引用 ra-pipeline 的“S6 完成定义” |
| CM-24 | 全文 | 情景·P2 | **没有失败分支与反例**：`get_region_config` 空、region 不在 REGIONS、registry 与 profile 冲突、写入被幂等 CLI 拒绝（缺必填字段）等情形均未覆盖；示例只有 KOR/MEA 的正向路径 | 增“常见失败与处置”小表 |

<a id="s3"></a>
### 3. `wq-brain-campaign-toolkit`（L-TOOL · SKILL.md 354 行 + 9 个 references + 3 个根目录说明文档）

**定位**：战役引擎层（scripts/ 下 17 个脚本：`campaign / gate / pipeline / build_wave / score_datasets / scan_fields / review_wave / harvest / diversity_* / assemble_priors …`）的使用说明。

**总评**：引擎本身职责清楚（“how”），但**文档是一份追加式日志**：①同一主题写两遍（2026-09-19 的“排障协议 + 新开关”在 §7.y/§7.z 与文末各一份，内容不同）；②已归档的脚本仍作为“可用子命令”列在 §6 表里；③三个 reference（`enhancement-v2` / `S2_COMPLIANCE_*` / `DIVERSITY_EXTRACT_*`）整篇在描述**已归档或已被撤销的机制**，其中两个还带有“权威 SOP/必须逐项确认”的强语气；④多处把 ra-pipeline 的规则原样抄进来（含已被禁的加权混合示例），与本 skill 自己的“禁止在别处复制本 scripts/ 逻辑”对称违反。**引擎已把很多规则做进代码，但文档没有跟着改，读文档的 agent 会被引向不存在或已撤销的路径。**

**阶段热力图**

| 阶段（行号） | 书写逻辑 | 职责划分 | 边界界定 | 需情景规范？ |
|---|---|---|---|---|
| frontmatter（1–11） | 🔴（702 字功能清单） | 🟡 | 🔴 | 是 |
| 职责边界 + 定位（21–35） | 🟡 | 🔴（“唯一写入方/唯一权威”不成立） | 🔴 | 是 |
| §1.x 使用率等级（37–73） | 🔴（标题与内容不符） | 🟡 | 🔴（含被撤回的说法） | **是（异步恢复/重发安全规则）** |
| 衔接协议（75–81） | 🟡 | 🟡 | 🔴（ledger key 与 RA 不一致） | 否 |
| §2–§4 环境/目录/调用约定（83–100） | 🟢 | 🟢 | 🟡（凭据链） | 否 |
| §5 快速开始（102–127） | 🔴 | 🟡 | 🔴（会绕过新闸） | 是 |
| §6 子命令一览（129–148） | 🟡 | 🟡 | 🔴（含已归档脚本） | 否 |
| §6.x/§6.y S0 评分与接线（150–178） | 🟡 | 🔴（RA 已有） | 🔴（读键无写入方） | 是 |
| §7 闸 7–8（180–189） | 🟢 | 🟢 | 🔴（按 profile 升级未实现） | 否 |
| §7.x fail-fast（191–199） | 🟡 | 🟢 | 🟡 | 是 |
| §7.z/§7.y 新增开关、二分排障（201–226） | 🔴（与文末重复） | 🟢 | 🟡 | 是（好范例但重复） |
| §8 纪律（228–262） | 🔴（重复、含开发流程） | 🔴 | 🔴（“提交配额”混义） | 是 |
| §9 台账落盘（264–314） | 🟡 | 🟡 | 🔴（回写路径 “一律” 冲突） | 是 |
| 工具化纪律（317–331） | 🟢 | 🟢 | 🟡 | 否 |
| 文末 “2026-09-19 新增”（333–354） | 🔴 | 🟡 | 🟡 | 否 |

#### 3.1 SKILL.md 逐段

| # | 位置 | 维度·级 | 问题 | 改进建议 |
|---|---|---|---|---|
| TK-01 | L2–11 | 边界·P2 | description 702 字（全库最长）是**功能清单**（含“骨架配给 linear_mix≤0.5”“REGULAR 4/日+SUPER 1/日+PPA 1/日”等实现细节），触发词里写“gate **5 闸**预检”而功能里写“**8 闸**预检”；“配额 quota / review 评审 / 多样性”与 wqb-concurrency、brain-alpha-judge、ra-pipeline 重叠；`allowed-tools` 无 `mcp__wqb-db__*`，而 §4 #6 规定“Agent 持久化只走 `mcp__wqb-db__*` 或本引擎 CLI” | description ≤150 字、只写触发场景；功能挪到 §1；allowed-tools 与正文一致 |
| TK-02 | L13–19、L23 | 逻辑·P3 | 7 个连续空行；“ledging”笔误 | 清理 |
| TK-03 | L25 | 职责·P1 | 声称本 skill 是 **`wave_results` / `registry_empirical` / `ledger_kv` 的“唯一正式写入方”**——但 `mcp__wqb-db__upsert_wave_result / upsert_registry_empirical / upsert_ledger_key`、`src/wqb/store` 同样写这三张表（ra-pipeline 步 9、matrix §4 分别要求不同的写法） | 改为“写入方矩阵”：表 × 写入方（CLI/MCP/store）× 适用场景；删“唯一” |
| TK-04 | L28–30 | 逻辑·P2 | `campaign.py dataset-experience` 的说明是孤立段落，夹在“职责边界”与“1. 定位”之间；§6 子命令表里没有这一行 | 移入 §6 表 |
| TK-05 | L33–35 | 职责·P1 | “本 skill 是战役脚本的**唯一权威实现**”——实际引擎分两处：本 toolkit（gate/pipeline/build_wave/score_datasets/review_wave…）与仓库根 `tools/`（wave_gate、campaign_intel、harvest_multisim、field_semantic_classify、step_funnel、forum_recon、submit_verdict…）。分工只在文末“工具化纪律”5 行里出现 | 把“toolkit vs tools/ 分工表”提到 §1，并补全（阶段 → 脚本 → 所在位置） |
| TK-06 | L37–73 标题“工具使用率等级” | 逻辑·P1 | 标题是“使用率分级”，正文却含**行为契约与安全规则**：选波数量契约（L53–62）、异步恢复（L64–68，含 “MCP 桥接超时返回 `outcome_unknown`、`retry_safe=false`，先查任务及 DB，**禁止盲目重发模拟**”）。这些是价值最高的信息，却被放在“使用率”标题下，很容易被略过 | 抽成独立小节“重发安全与异步恢复”，并写情景：`outcome_unknown` → ① `workflow_task_status` ② 按 multisim_id 查 `backtest_results` ③ 两处都空且任务已死才允许重发；RA 步 6 的“超时恢复清单”指向此处 |
| TK-07 | L49、L71、L73；L141–145 | 边界·P1 | 已归档脚本（`distill_experience/os_feedback/family_atlas/budget_planner/campaign_mutex/signal_classifier/composition_validator` + 13 个 2026-08-31 归档件）以**删除线行**混在“核心工具”表里，L71 用括号**撤回** L70 的说法；而 **§6 子命令表仍把前 5 个当作可用命令详细描述**（“经验蒸馏器 G1 学习闭环”“多战役互斥”等，`scripts/` 里已无这些文件）；两处归档目录名不同（`attic/toolkit_zero_ref_20260928/`、`attic/tools_archive_20260831/`） | 删除线与括号撤回全部清理；§6 表删已归档行；单独一节“已归档清单（指向 attic）” |
| TK-08 | L41–51、L73 | 边界·P2 | “核心 5 工具”按 2026-08-31 的静态引用扫描定义，`score_datasets/build_wave/review_wave` 被划为“中使用率”，而 RA 的 S0/S2/S4 节点每波都调用它们；“新任务一律用核心 5 工具”与实际流程不符 | 换成“按阶段选脚本”表（S0→score_datasets…），删使用率分级 |
| TK-09 | L53–62 | 逻辑·P2 | 10 行无编号、中英文无空格（“`--size`在CLI与workflow S2中都只表示容量”），与 RA L397–409 及 `selection-plan.md` 是**同一内容的三份拷贝**（措辞不同） | 只在 selection-plan.md 维护；此处 3 行指针 |
| TK-10 | L64–68 | 逻辑·P2 | 同一段里放了两件无关的事：异步任务恢复、救援池 `exclude_dataset` 的来源排除；后者属于 `get_salvage_pool`/RA 步 7 | 拆分并各自归位 |
| TK-11 | L77 | 边界·P2 | “brain-sim-alphas-in-batch-and-track 是**唯一运行时调用方**”不成立：`workflow_batch_track` / `workflow_campaign` 节点同样以子进程调用 `pipeline.py` / `campaign.py` | 改“主要调用方”，并列出节点 |
| TK-12 | L80 | 边界·P1 | 该行是**最好的产物契约**（脚本 → 库表/ledger key），但是一整行 700 字；且与 RA Artifact 表冲突：这里 `review_wave.py → ledger review_<tag>`（代码 `review_wave.py:335` 印证），RA 表写 `s4_walls_<region>_<wave>` | 拆成表；RA 表改为本处的 key |
| TK-13 | L86–91 | 边界·P2 | 契约里夹带“KOR/IND/DEU 混合形态、`probe_scoring_v2` 刻意缺”的决策记录（对 agent 的动作是什么？）；`campaign-dir-contract.md` 指针重复两次；TWN 缺 `tracking/TWN/`、AMR 仅有 config，契约未覆盖“缺目录”情形 | 决策记录移出；补“缺目录/缺 thresholds 时的行为” |
| TK-14 | L96 | 边界·P2 | 凭据链列了 4 个来源（环境变量 / `BRAIN_CREDENTIALS` / `~/.brain_credentials` / `MCP_CONFIG_FILE`），与 AGENTS.md 的“凭据位于 `.env`：禁止读取、打印或提交”并存且未互相引用；没说**agent 不得读这些文件**，只由脚本读取 | 加一句红线；与 AGENTS.md 统一入口 |
| TK-15 | L100 #7 | 情景·P3 | 开波闸模式段 560 字，实际决策只有“命令行 > 环境变量 > 按日期缺省；节点一律拦截” | 改 3 行小表：入口 × 缺省 × 结果；日期文案标“到期文案” |
| TK-16 | L102–127 快速开始 | 逻辑·P1 | ①bash 变量赋值（`PY=$WQ_PY`）与全库 PowerShell 约定不符；②流程只用 `gate.py`（闸 1–6），**完全不含 `tools/wave_gate.py` 的闸 SEM / 体检硬门 / 闸 PF / 闸 2b**——照本页走会绕过 RA 步 5 的新闸；③没有 GEM 一步（`build_wave` 只做“选波后处理”）；④`--submit`（=发起回测）与“提交 alpha”易混，`--max-rounds 3` 无说明 | 快速开始改为“S0→S6 对应命令”并标注哪些在 `tools/`；PowerShell 写法；`--submit` 旁注“发起回测，不是提交 alpha” |
| TK-17 | L129–148 | 边界·P1 | 子命令表：①含 5 个已归档脚本（TK-07）；②缺 RA 依赖的 `campaign.py assemble-priors`、`dataset-experience`、`diversity-extract`、`s2-mark` 与 `harvest.py`、`check_ledger_sync.py`；③`gate.py` “8 闸”而 L45 及 D8 写“5 闸”；④“细节文档”列是纯文本名（`gate-rules` 等），非链接——机械检查因此把 `gate-rules.md`/`enhancement-v2.md`/`S2_COMPLIANCE_GUIDE.md` 判为孤儿 | 补全缺行；闸数统一（“8 闸+闸 0，其中 1–5 为语法/白名单/类型/算子/毒模式”）；细节列改链接 |
| TK-18 | L150–169 | 边界·P1 | §6.x 记录 `saturated_datasets`、`seat_model` 是“数据源台账”，但**全仓库没有任何代码或指令写入 `saturated_datasets`**（只有 `score_datasets.py`/config 读取）；RA 步 9 反而让 agent 写另一个键 `submit_ready_blocked`（仅被 `step_funnel.py` 计数）。于是 P2“饱和再验证降级”与 P5“饱和拍平 model”两项**永远不会触发**，除非有人手写台账 | 明确写入方与命令；或删除这两项；补“如何登记饱和”的示例（`upsert_ledger_key(region,"saturated_datasets",{"datasets":{ds:{reason}}})`）并与 RA 步 9 统一 |
| TK-19 | L154–160 | 逻辑·P3 | P0/P2/P3/P5/P6 是审计工单号（无 P1；P4 只在 L169 出现）；与 `probe-scoring-v2.md` 的“P5 分段罚”、探针模板 P1–P8 **同号异义** | 用功能名替代编号 |
| TK-20 | L162 | 边界·🟢 | “`score`=信号强度榜、`pyramid_view`=点塔战略榜，语义分离，**勿相加或混排**”——明确写了“不要拿它做什么” | 推广为全库范式 |
| TK-21 | L171–178 §6.y | 逻辑·P2 | “接线修复落地（审计①③⑥⑦）”是变更记录，圈号指向外部审计报告；内容与 RA（settings prior、region_kb 刷新、S2-COMPLIANCE 降级、rn 墙/停止规则）重复 | 移 CHANGELOG；RA/toolkit 各只留一句 |
| TK-22 | L186、L189 闸 7 | 边界·P1 | “小宇宙区域 KOR/HKG/TWN **按 profile 升级 FAIL**”“CW 在区域 profile 的 `cw_gate` 覆盖中处理”——代码核对：`gate.py` 闸 7 硬编码 `longCount<80 → WARN`，**没有任何代码读取 profile 的 `longcount_verdict/cw_gate`**；文档承诺未实现。“约 17% 死路属结构性缺陷”无出处 | 要么实现（读 `thresholds.json` 或 profile），要么删该句并写“目前仅 WARN” |
| TK-23 | L193–199 | 情景·P2 | “无效努力七信号”里 4 条是定性判断（“换变体无本质变化”“反复失败”“偏高”）未给可测口径；“priority 65”魔法数；链接 `docs/experience/fail_fast_rules.md` 相对 skill 目录解析不到（文件在仓库根 `docs/`），skill 被同步到其它宿主目录后必断 | 每条信号补量化口径；链接改仓库根或把文件放进 skill |
| TK-24 | L201–212 | 逻辑·P3 | 标题“今日实证驱动”（相对时间）；第 1 行 `prod-first` 与 RA 步 7 的 `--top-k 3` 不一致（此处 `--prod-first-top-k 2`，与步 5b 一致） | 用绝对日期；RA 对齐 |
| TK-25 | L214–226 vs L333–354 | 逻辑·P1 | **同一协议写了两遍**：§7.y“二分排障（5 步）”与文末“平台报错二分定位（3 条）”；同步目标一处写 2 个（`platform_constraints.json` + profile）一处写 3 个（+`pipeline_pregate.py`）；§7.z 表与文末“新开关”重复 4 项，标题说“三个新开关”实列 6 条；小节编号 7.x → 7.z → 7.y 乱序 | 合并为一份；编号重排。**保留 §7.y 的写法**——它是全库少见的“场景→步骤→判据”范式（JPN `Invalid data field close` 例） |
| TK-26 | L229–234 §8 #1–#6 | 逻辑·P3 | “禁止 record_*.py 式直改”×2、“禁止第二权威实现”×2、“单轨数据库”与 matrix 重复；#2 的 429 退避属 wqb-concurrency；#3 仍提 `candidates/results/reviews`（旧文件布局） | 删重复，归位 |
| TK-27 | L233 #5 | 边界·P1 | “**提交配额**是稀缺资源：未过 gate 不提交；pipeline 默认只干跑，显式 `--submit` 才烧配额；`--force` 才越过配额闸”——“提交/配额”同时指 ①发起回测（`--submit`，消耗仿真配额）②提交 alpha（REGULAR 4/日）。代码核对：`pipeline.stage_submit_poll` 在 **alpha 提交配额 remaining≤0 时中止回测发起**（除非 `--force`，`pipeline.py:769–772`），而 RA 循环表写“配额耗尽 → 挂起提交，**继续步 2→9**”——两者矛盾；“`--force` 会用光当日额度”亦不实（它只是不中止回测，并不提交 alpha）。“默认只干跑”与快速开始里显式写 `--dry-run` 也不一致 | 术语固定：**发起回测=dispatch，提交 alpha=submit**；说明回测发起是否应受提交配额约束（建议不受），修代码或改文档；`--force` 语义写准 |
| TK-28 | L235–242 §8 #7 | 职责·P1 | 把 RA 步 4 硬约束**原样抄第三份**，含①已被禁的加权混合范例“EUR：`0.40` 慢 MODEL 残差 × `0.60` 快 PV”，②“有信号字段先做组合（同集或跨金字塔慢×快）”——与 CLAUDE.md“优先单数据集 atom alpha、禁止混信号调参、警惕 add(A,B)”冲突；本 skill 自己在 L33 禁止他人抄它的逻辑，这里却抄 SOP | 删，改一句“选波/填槽规则见 ra-pipeline 步 4/6，参数见 `config.MINING`” |
| TK-29 | L244–262 §8 #8 | 职责·P2 | “新增/修改 workflow 节点 → 四处同步”是**开发者流程**（改 registry.py、两个测试、INDEX 计数，`audit_node_registration.py`），放在挖矿 skill 里；AGENTS.md 已有“变更影响面”章节承担此职责 | 移入 AGENTS.md（保留一行指针） |
| TK-30 | L266–282 | 边界·P1 | “**AI 回写一律走 `campaign.py wave` CLI**”与 RA 步 9“`mcp__wqb-db__upsert_wave_result`”“一律”冲突（两者虽同一写入契约，但指令不同）；示例路径 `results/wave63_results.json` 是旧文件形态 | 二选一并在 RA/matrix/toolkit 三处同步（建议 MCP 优先） |
| TK-31 | L284–289 | 边界·🟢 | “WAVE_LEDGER.md 是从数据库**生成**的快照（覆盖写，勿手改）”——正确，且与 decision-table D8 的“追加 WAVE_LEDGER.md”矛盾 | D8 改；此句作为全库口径 |
| TK-32 | L291–314 | 边界·P1 | 查询清单把 `get_ledger_key(key="submit_ready")` / `get_submit_ready` 当作“达标池”读法；但 **`submit_ready` 有两套并行存储**：ledger 键列表（`review_wave --write-ledger`、`pipeline.py`、`campaign.py ledger submit-ready` 写；MCP `get_submit_ready` 读）与 SQL 表 `submit_ready`（`src/wqb/store/submit_queue.py`、`tools/submit_queue.py`，S3 收批自动入队、提交自动退役）。MCP 读不到表里的行——**读写脑裂** | 决定唯一存储（推荐 SQL 表），把 MCP `get_submit_ready` 改读表，ledger 键标废止；文档统一 |
| TK-33 | L293–314 | 职责·P3 | 15 个 MCP 查询示例（含 alpha 查询、区域概览）属 INDEX/wqb-db 工具说明，而非引擎职责 | 删，指向 INDEX 工具表 |
| TK-34 | L317–331 | 职责·P2 | 唯一说明“toolkit vs tools/ 分工”的位置（好），但只有 5 行，且用了已被 RA 作废的旧称“提交层判定（403 盲区）” | 扩展并前移（TK-05）；更新术语 |
| TK-35 | L333–354 | 逻辑·P1 | 文末又一个“2026-09-19 新增”，见 TK-25；另含“2026-09-19～27 它不在 MCP 工具表里（装饰器错挂，N31）”这样的故障史 | 合并/删除 |

#### 3.2 `references/gate-rules.md`（107 行）

| # | 位置 | 维度·级 | 问题 | 改进建议 |
|---|---|---|---|---|
| TR-01 | L3–7 | 边界·P1 | 声称“闸编号唯一基准 = `gate.py` 模块头”；而 ra-pipeline、toolkit SKILL 都写“唯一基准见 INDEX.md「gate.py 闸编号」”——**两处都自称唯一**；且都不覆盖 `tools/wave_gate.py` 里的闸 SEM/PF/2b/2.6 | 选一个（建议 INDEX 汇总表，含 wave_gate 全部闸），其余只引用 |
| TR-02 | L32–33 闸 5 | 边界·P1 | “当前平台级：`nested_three_leg_add`”——`platform_constraints.json` v1.5 实有 **6 条**（另有 `weighted_signal_mix`、`weighted_signal_mix_structural`、`weighted_leg_mix_func_prefix/suffix`、`equal_weight_leg_add`）。加权混合禁令的实际落点（闸 5）在闸门文档里**看不到** | 列全 6 条，并在每条旁写“拦什么/放行形态” |
| TR-03 | L35–42 闸 6 | 边界·P1 | 写“契约到 `expires_after_batches` 自动**失效**”；`gate.py` 与 RA 均为“过期→**FAIL-CLOSED** 并自动续约”（gate.py:780）。“失效”读成“不再拦” = fail-open，与代码相反；“台账记录原因”未给 key | 改成与代码一致；给逃生留痕的 key 名 |
| TR-04 | L41 | 边界·P1 | “构建端：`diversity_slots.py --campaign-dir <DIR>` 打印当前契约”——该脚本已归档（SKILL L73），文件不存在 | 改指向仍存在的入口，或删 |
| TR-05 | L43–46 | 情景·P2 | “注入算子的经济学写法”以 `ts_corr(慢腿,快腿,20)` / `if_else` / `group_zscore(慢腿, sector)` 为例，仍是“慢×快”双腿叙事；且 `group_zscore(...,sector)` 未提 JPN 等区域 sector 非法（闸 2b） | 加区域例外；与统一“辅助腿入场三式”对齐 |
| TR-06 | L52–59 build_wave | 边界·P1 | 描述**文件模式**（`<region>_wave*_exprs.json`、`candidates/*.json`、`reviews/*.json`、输出 `candidates/…exprs.json`），与“DB 唯一事实源、`--from-db`”矛盾；骨架配给“**`linear_mix` ≤50%**”允许最多一半候选为线性混合，与闸 5 的加权/等权混合禁令直接冲突 | 改为 DB 口径；`linear_mix` 配额降为 0 或更名（若指“单信号线性变换”需定义） |
| TR-07 | L61–101 | 职责·P2 | `diversity_extract.py` 在此写了 40 行，又有根目录 3 份说明（546 行）、D7 一份——同一工具 5 份文档 | 合并为一页（≤60 行）；根目录三份删除 |
| TR-08 | L103–107 review_wave | 边界·P2 | 墙枚举“SHARPE/FITNESS/2Y/MARGIN/TVR/CW/RA_OTHER/NO_DATA”缺 `RN_EXPOSURE`、`ROBUST_STRUCTURAL`、prod 类墙（RA 已用）；“missing≠fail：单独标 `*_UNKNOWN`”是好边界 | 补墙名与含义（词汇表来源） |
| TR-09 | L14 | 边界·P2 | verifier 查找顺序把用户主目录已安装副本（`~/.claude/skills`…）放在**仓库 `Claude/skills` 之前**——旧副本会覆盖仓库版本，验证行为不可复现 | 仓库优先，或每次打印所用路径；`SYNTAX_UNKNOWN` 显式报警（好） |
| TR-10 | L25、L27–30 | 逻辑·P3 | `--fix` 段与闸 4 的“不要改 validator.py”“对 ops_used 判定是死代码”是给开发者的实现注释；闸 3 同句称 VECTOR 违规报 “[EVENT] 事件型字段…” 标签混用 | 分“agent 需知/维护者需知”；统一标签 |

#### 3.3 `references/poll-and-quota.md`（31 行）

| # | 位置 | 维度·级 | 问题 | 改进建议 |
|---|---|---|---|---|
| TR-11 | L16 | 边界·P1 | “`stage_submit_poll` … 并行提交+轮询 N 批（**N=min(5, 批数)**）”——代码是 `n_slots = min(7, n_total)`（`pipeline.py:792`），文档同段还写“5→7 更新” | 改 7；此段整体删（属已废止规则） |
| TR-12 | L14–17 | 逻辑·P2 | 整节是“单批在飞规则（**已废弃**）”：删除线原文 + 纠正 + 历史实证；agent 读到的第一句是被废止的规则 | 只保留现行“七槽”；历史入 CHANGELOG |
| TR-13 | L22–28 | 边界·P1 | 配额只写两条通道（REGULAR 4 + SUPER 1），而 toolkit description、`campaign-dir-contract` 写三条（含 PPA `POWER_POOL_SUBMISSION` 1/日）；“剩余额度从 submit 响应的 check 读”需要发生一次 POST（与 RA 的“POST=真提交”矛盾），而 `pipeline quota` 已按 activities 聚合；配额闸阻断回测的问题见 TK-27 | 三通道统一；写明读额度用 `pipeline.py quota`，勿靠 POST |
| TR-14 | L30–31 | 逻辑·P3 | “凭证与登录”一节混入 metrics_cache 读穿缓存 | 拆分 |

#### 3.4 `references/ledger-schema.md`（38 行）

| # | 位置 | 维度·级 | 问题 | 改进建议 |
|---|---|---|---|---|
| TR-15 | L17、L32 | 边界·P1 | 仍把 `wave<N>_verdict` + `ledger set-verdict` 当作**逐波结论的正式通道**——RA 已于 09-28 声明“结论唯一真相源=`wave_results.verdict`，不再双写”；`ra-campaign-prompt.md` 验收表、`decision-table` D8 也还在要求旧键 → 至少 4 处文档仍教双写 | 标注废止，CLI `set-verdict` 同步下线或改写 `wave_results` |
| TR-16 | L20 | 边界·P1 | `submit_ready[]` 只描述 ledger 列表，完全没提 SQL 表 `submit_ready`（TK-32 脑裂） | 统一存储后改写 |
| TR-17 | L11–23 | 边界·P1 | “键命名约定”只有 12 行且多为旧键；正文与 RA 用到的活跃键（`s0_ranking`、`s0_whitelist`、`s1_<ds>_d<delay>`、`s1_semantic_<ds>`、`s2_field_pool_<ds>`、`region_kb`、`template_kb`、`priors_snapshot_<region>`、`prod_first_<wave>`、`stop_rules_override`、`saturated_datasets`、`dataset_empirical_prior`、`seat_model`、`ckpt_w<W>`、`forum_recon_*`、`research_leads_w<W>`）均未收录，且无“读取方/过期”列 | 扩成**ledger key 目录**（key/写入方/读取方/缺失行为/TTL），并加测试“每个被读的 key 必有写入方”（可抓 TK-18、RA-113 这类断链） |
| TR-18 | L5–9 | 逻辑·P2 | 原语（`.bak` 滚动备份、`atomic_save`、双遍重放）是 **JSON 后端** 的描述；默认后端已是 SQLite | 分“SQLite（现行）/JSON（已弃）”两段 |
| TR-19 | L25 | 逻辑·P3 | 标题“CLI（campaign.py ledger / 直接 _lib.ledger 不支持，走 campaign.py）”语句不通 | 改写 |

#### 3.5 `references/campaign-dir-contract.md`（86 行）

| # | 位置 | 维度·级 | 问题 | 改进建议 |
|---|---|---|---|---|
| TR-20 | L7–23 | 边界·P2 | 目录布局把**仍必需**（`config/`、`reference/` typed catalog）与**DB 唯一模式下已不产出**（`candidates/`、`reviews/`、`results/`、`<region>_wave*_exprs.json`、`<region>_dataset_ranking.json`）并列，无法分辨哪些是活的 | 每项标 [必需/可选/历史] |
| TR-21 | L27–36 | 逻辑·P3 | 示例 JSON 含行内 `#` 注释（非法 JSON，复制会报错）；示例中性化 `SECTOR`，而决策表 D5 称 SECTOR/MARKET 会压垮 IS_LADDER | 去注释；改示例值 |
| TR-22 | L54 | 边界·P1 | `hard_gates` 的“权威定义见 brain-how-to-pass-alpha-test”——而 `config.GATES` 才是全库唯一事实源 | 改指 `config.GATES` |
| TR-23 | L56、L73–86 | 边界·P2 | 称 `diversity.signal_floor` 是“**唯一有消费方**的子键”，下文又给 `diversity.stop_rules`（同样被 `_run_stop_rules_gate` 消费）；`stop_rules` 示例仅 3 个键，SKILL L178 列 8 个键 | 更新行说明；补键 |
| TR-24 | L42、L65 | 逻辑·P3 | “上表”指的是其后的表；“11 个区域已补齐”与 RA 的“13/13”、REGIONS=14、TWN 缺目录三种数字并存 | 数字改指向自动生成的区域清单 |

#### 3.6 `references/selection-plan.md`（60 行）· `references/probe-scoring-v2.md`（62 行）

| # | 位置 | 维度·级 | 问题 | 改进建议 |
|---|---|---|---|---|
| TR-25 | selection-plan 全文 | 情景·🟢/P2 | **优点**：有完整 JSON 清单示例（hypothesis/control 配对、“ID 仅为格式示例”）。**问题**：①标题“选波”，后半（L44–60）是波后解读与研究线索规则，越界；②“增强资格”“资格线”“受保护状态”“平台 UNITS 警告”未定义；③引入新键 `research_leads_w<W>` 未登记；④“最小纠错复验”无模板；⑤“无缺陷弱信号不得反复换窗口/翻号/组腿”缺可检判据；⑥中英文无空格 | 拆成“选波”与“波后解读”两篇；补 `research_leads` 与“纠错复验单”填写示例；定义“缺陷”白名单（单位警告/字段映射/对照不匹配） |
| TR-26 | probe-scoring L15 vs `score_datasets.py:293-294` | 边界·P1 | 文档 tier 分位 **P80/P55**、`coverage_hard_min` **0.65**；代码缺省 **P60/P30**、`coverage_hard_min` 缺省 **0.7**；toolkit SKILL §6.x 写 P60/P30 —— 同一 skill 内两个数 | 以代码缺省为准并只写一处（或引用 `thresholds` 缺省） |
| TR-27 | probe-scoring L58 | 边界·P1 | 三灯动作建议：“绿灯带 CW 失败 → 骨架直接上**跨 Category rank 加法**”“黄灯 → 只做镜像腿与**两两融合**限 2 批”——直接**推荐**被禁的 leg-add/混合 | 改为条件门控/分组/对偶价差（与统一规则一致） |
| TR-28 | probe-scoring L24 | 边界·P2 | “calibrate **不在默认流程里**（ra-pipeline SOP 都不自动调）”，而 RA 步 2 把 calibrate 列为“**必需**”——一处说“没人调”，一处说“必须调” | 改“工具不自动执行；SOP 要求显式执行” |
| TR-29 | probe-scoring 全文 | 逻辑·P2 | P 编号同号异义（“P5 分段罚”对 SKILL“P5 饱和拍平 model”；探针模板 P1–P8）；三灯里 `margin(>5bp)`/`tvr(5–30%)`/`rn(>=1.0)` 与 config 内部线（margin 10bp、换手 5–20%）、RN_EXPOSURE（>0）并存；“判死”阈值再添 0.3（Stage A 早停）/0.8/0.6 | 改用名称；阈值只写引用；加入统一“判死判据表” |
| TR-30 | probe-scoring L34–39 | 情景·🟢 | “审 dry-run 时重点看两处异常 → 该怎么办（勿 apply，先查 ac 来源）”“数据源优先级 ①–④”——**场景→动作→理由**齐全，是全库最好的情景范式；RA 步 2 的同段落缺“怎么办” | RA 引用本处；抽成模板 |

#### 3.7 已过期/被撤销的 references 与根目录文档（建议整体处理）

| # | 文件 | 维度·级 | 问题 | 改进建议 |
|---|---|---|---|---|
| TR-31 | `references/enhancement-v2.md`（103 行，自称“**权威 SOP**”） | 边界·P1 | 整篇描述 9 个脚本（`proxy_prescreen/ortho_prescreen/migrate_templates/diversity_slots/param_opt/build_mix/fit_mix_weights/rescue_checklist/calibrate_probe`），**均已于 2026-08-31 归档**（SKILL L73），`tests/test_enhance_v2.py` 亦不存在；含被禁的“学混合权重（`fit_mix_weights`）/`build_mix`”，以及“`rescue_checklist --fail` 未全绿**禁止判死**”的判死纪律（与 RA/D12 的判死判据冲突，且执行器不存在）；无入链（孤儿） | 整篇移入 attic；仅保留“预算只花在本地筛过的精英上”一句原则 |
| TR-32 | `references/S2_COMPLIANCE_CHECKLIST.md`、`S2_COMPLIANCE_GUIDE.md` | 边界·P1 | 要求“每次进 S2 必须调用 `brain-data-feature-engineering`、候选池**基于特征工程文档构建**、`pipeline.py` 硬闸缺记录即中止”——三条**均已被撤回**：RA 步 3 规定特征工程**按需、仅人读、禁注入 GEM**；SKILL §6.y⑥ 与 RA 步 6 已把 S2-COMPLIANCE 降级为提示；清单还要求“复制到 `WAVE_LEDGER.md`”（该文件是生成物）并设“检查人签字”栏 | 移入 attic |
| TR-33 | `DIVERSITY_EXTRACT_README/SUMMARY/QUICKSTART.md`（546 行，根目录） | 职责·P2 | 3 份互为近似拷贝（9 个共享段落，Jaccard 见机械检查 §G），孤儿，营销文风（“核心价值/深度集成方案总结”），引用不存在的 `scripts/test_diversity_extract.py`，教“脚本会自动创建 candidates/reviews 目录”（与 DB 唯一模式冲突）；该可选工具另有 gate-rules 一节、D7 一节 | 合并为 1 页（≤60 行）放 references；其余删 |

<a id="s4"></a>
### 4. `brain-next-move-analysis`（L0 · SKILL.md 78 行 + reference.md 128 行）

**定位**：并行情报层——日报/金字塔分析/区域态势。

**总评**：体量小、边界句写得清楚（“不产出白名单、不选字段、不回测；非流水线前置”），§5.5 的“失败不阻塞 + 输出表 + 与 profile 联动”是好的写法。**核心缺口在它承诺的价值上**：description 说“可执行建议”，但 §4“研究与建议”只有一句“基于 alpha 表现与金字塔缺口，建议下一步行动”，没有方法、格式、约束；建议一旦与 ra-pipeline 的硬规则（已点亮塔不进白名单、跨区弱先验、停波闸）不同源，就会把 agent 引回已判死的路径。reference.md 是“交接给秘书”的叙事体，章节编号与 SKILL 不一致，且包含**要求传递邮箱/口令**的认证指令。

| 阶段（行号） | 书写逻辑 | 职责划分 | 边界界定 | 需情景规范？ |
|---|---|---|---|---|
| frontmatter + 职责边界（1–34） | 🟡 | 🔴（选区归属不清） | 🟡 | 是 |
| §0–§3 摘要/平台/比赛/事件（36–50） | 🟢 | 🟢 | 🟡 | 否 |
| §4 研究与建议（52–53） | 🔴（空壳） | 🟡 | 🔴 | **是（最需要）** |
| §5 Alpha 进展（55–59） | 🟡 | 🟢 | 🟡（范围未定） | 是 |
| §5.5 区域饱和度（61–78） | 🟡 | 🔴（与 region_status/matrix 重叠） | 🔴（区域清单过期） | 是 |
| reference.md（128 行） | 🔴（叙事、编号不一致） | 🟡 | 🔴（认证/凭据） | 是 |

| # | 位置 | 维度·级 | 问题 | 改进建议 |
|---|---|---|---|---|
| NM-01 | L4 description | 边界·P2 | 只写“日报/早报/状态检查”，但 §5.5 是 RA 用来“选区/转区”的区域态势；用户说“哪个区更值得挖”不会命中本 skill | description 加“区域态势/转区建议” |
| NM-02 | L23–25、L34 | 职责·P1 | 边界句说“本 skill 不选字段、非流水线前置”，但 ra-pipeline 把它当**分支终点**（步 1 失败→“转 next-move 选新区域”；停止规则→“转 next-move”；日循环每日先跑）；§5.5 又直接给“继续/正交/开战役/冻结”的**转区建议**，与 `region_rotation.py`、`tools/region_status.py`、profile `entry_verdict`、campaign-matrix 的“选区”四方重叠。“S6 并行情报层”（L23）与“L0”（L32）两种层名并用 | 明确：next-move = **报告器**（汇总 `region_status.py` 输出），选区**决策**归 region_rotation/matrix；层名统一为 L0 |
| NM-03 | L34 | 边界·P2 | 又一次把“S0 体检白名单由 `wq-brain-ppa-mining §1.0` 产出”（PPA 专用方法论当全体 S0） | 改指 RA 步 2 / D4 |
| NM-04 | L52–53 §4 | 情景·P1 | 唯一一句无方法：缺“输入（哪些表/工具）”“如何得出金字塔缺口”“建议的固定格式”“必须遵守的约束”。且 §5 建议用 `get_pyramid_multipliers`“金字塔定向”，而 RA 09-19 定案是“已点亮塔（当季 ACTIVE≥3，`category_lit`）不开战役”——两处**选塔准则不同源**，日报可能推荐已点亮塔的数据集 | 给建议模板：`动作 / 依据（数据） / 前置检查（lit 塔、跨区弱、停波闸） / 预期成本 / 何时复核`；选塔准则一律引用 `recommend_datasets.category_lit` 与 `get_pyramid_alphas` |
| NM-05 | L56–59 | 情景·P2 | “IS/OS 表现”没说范围：全部？最近 N 天？Top N？reference 写 `limit 30, offset 0`（无排序说明）——3 万条 IS 库存里取任意 30 条做分析 | 定“自上次日报以来新增 + OS 全量 + 库存 Top N（按何指标）” |
| NM-06 | L64–66 | 逻辑·P2 | “首选 `region_status.py`”后又说“手动查询仍可按下列口径执行”并称“下述判据即其实现口径”——文档复述了代码逻辑，两份实现必漂移；区域清单写死“USA/EUR/KOR/IND/ASI/GBR/HKG/GLB/CHN/TWN（+MEA 冻结）”——**缺 DEU、JPN**（均有 profile），`config.REGIONS` 共 14 个 | 删手动口径，只引用工具输出字段；区域清单改“遍历 `config.REGIONS`” |
| NM-07 | L68、L70 | 边界·P2 | “≥10 且风格同质→`prod_saturation: likely`”与 campaign-matrix、USA profile 是**第三份拷贝**，“风格同质”无判据；“probe-only 区域（ASI/GBR/HKG/CHN/TWN）”写死名单，而下一段说以 profile `entry_verdict` 为准 | 引用 `region_status.py` 的判据；名单删 |
| NM-08 | L72–76 输出表 | 情景·P2 | 好：有固定输出表。缺：“达标数”是 `sharpe≥1.58` 的宽口径，而 RA 的选区先验用严格口径（`ra_failed_checks` 为空）；“建议动作”四选一的判据没有量化 | 表头注明口径；给 4 个动作各 1 条数值判据 |
| NM-09 | L78 | 边界·🟢 | 用一段话定义了 `entry_verdict` 三态的**默认行为**（active 默认继续；probe-only 默认不开战役；frozen 仅报状态）——这正是 ra-pipeline 缺的定义（RA-14） | 提升为全库共享的术语定义 |
| NM-10 | L42 | 逻辑·P3 | 维护警示“注册名含大写 S…勿再改”属开发者备注 | 改为测试断言（`test_skill_integrity` 已校验工具名）后删 |
| NM-11 | reference L1–15、L128 | 逻辑·P3 | 叙事体（“帮助秘书接手”“请随时与前任秘书联系”），对 agent 无指令价值；示例日期 2025-08-09、GAC2025 已过期 | 改成规范体；示例用占位 |
| NM-12 | reference L12 | 边界·P1 | “获取当前时间，running `get_ny_time.py`”——脚本不存在（机械检查 MISSING），且与 L99“使用系统日期动态获取”并存；日期错则事件过滤全错 | 指定唯一取时方式（系统日期 + 时区规则），并说明 NY 日界 |
| NM-13 | reference 章节编号 | 逻辑·P2 | 与 SKILL 不一致：reference 是 0 摘要/1 基本信息/2 平台/3 比赛/4 活动/5 建议/6 Alpha；SKILL 是 0 摘要/1 平台/2 比赛/3 事件/4 建议/5 Alpha/5.5 区域；**§5.5 不在 reference 大纲里**——照 reference 写日报会漏区域态势 | 大纲只留一份（SKILL），reference 只保留各章“怎么取数” |
| NM-14 | reference L45、L64、L98 | 边界·P1 | ①要求“`authenticate` 提供用户的电子邮件和密码”——`authenticate(email, password)` 确实收明文，但 AGENTS.md 规定凭据只在 `.env`、**禁止读取/打印**，且环境规则不得把用户邮箱发往无关服务；②`get_leaderboard` 示例写了具体账号 ID（形如 `CQ#####` 的真实用户 ID，报告中已脱敏）；③`get_events` 传 `random_string="dummy"` 的奇怪参数无解释；④`get_messages(limit=null)` 与 RA 的 `limit=30` 不一致 | ①改“认证由 MCP 服务端按 .env 自动完成；需人工认证时请用户在本机终端完成，勿在对话里传口令”；②占位；③④对齐 |
| NM-15 | reference L77–83 | 逻辑·P2 | “IS = 正在回测的 alpha”“OS = 最近成功提交的”语义不准（IS=样本内阶段的 alpha，OS=已提交）；`get_alpha_yearly_stats` 在同一行列 2 次、工具清单再列 2 次 | 修正术语；去重 |
| NM-16 | reference L101、L103 | 边界·P3 | “善用论坛”（与 RA“论坛默认不查”冲突，且无具体工具）；“`todo_write`”是某宿主专有工具 | 指明何时读 forum-browse；用通用说法 |
| NM-17 | reference L105–124 | 情景·P2 | 错误防范里只有 GAC 一个**具体场景**（好）；“数据解读错误/输出格式错误/持续改进机制”是空泛口号 | 每类补 1 个真实案例（症状→原因→防范） |

---

<a id="s5"></a>
### 5. `alpha-template-labs-data-analysis`（L0 · 98 行）

**定位**：Brain Labs 上的 Python 原生原始数据分析（USA/TOP3000/D1 MATRIX）。

**总评**：约束写得具体（“一个机制、至多两个 MATRIX 字段”“禁止照抄论坛公式”）且带默认示例，这是好范式。问题是**流程里有一步只能由人完成却没标出来**，并混入本机专有运行器（`rtk`），且它服务的“Python alpha”与主流水线的 FASTEXPR REGULAR alpha 的关系没有说明。

| 阶段（行号） | 书写逻辑 | 职责划分 | 边界界定 | 需情景规范？ |
|---|---|---|---|---|
| 职责边界 + 用途（15–27） | 🟡（S0/S1/S2 三处不一致） | 🟡 | 🔴（与 RA 的关系） | 是 |
| 必走流程 1–8（29–74） | 🔴（第 4 步需人工） | 🟡 | 🔴 | **是** |
| CLI 专用步骤（76–84） | 🟡 | 🟡 | 🔴（`rtk`） | 是 |
| 硬规则（86–93） | 🟢 | 🟢 | 🟡 | 否 |
| 默认示例（95–98） | 🟢 | 🟢 | 🟢 | 否 |

| # | 位置 | 维度·级 | 问题 | 改进建议 |
|---|---|---|---|---|
| LB-01 | L17–19 vs L27 | 边界·P2 | 阶段定位三说：“S0 前”“结论只作 **S1** 输入”“在 **S2** 候选设计之前”。且它服务的是 Labs 的 Python alpha，而 RA 流水线只产 FASTEXPR REGULAR alpha——两者如何衔接（Python 结论能否指导 FASTEXPR 表达式？能否提交？）全文未说；机械检查 K：RA 没有任何回指 | 写一节“与 REGULAR 流水线的关系”：产物仅作 S1 字段/预处理线索，不进入提交路径 |
| LB-02 | L22–23 | 逻辑·P3 | 链接文字 `reference/…` 而目标 `docs/reference/…`（仓库根路径，skill 目录内不存在），同步到其它宿主目录后断 | 链接放进 skill 或用仓库根显式写法 |
| LB-03 | L46–52、L65 | 边界·P1 | 第 4 步“在 Brain Labs 里运行该脚本”只能由**人**在浏览器完成，全文没有标出“此处暂停等用户回传 JSON”；第 2 步“配额告警后已获批准”未定义（哪种配额？谁批准？） | 在第 3 步后加显式 **[人工]** 标记与暂停指令；定义配额与审批人 |
| LB-04 | L61、L73 | 边界·P2 | `labs_output="/tmp/…"` 是 Linux 路径（工作区为 Windows）；第 7 步写 `tracking/runs/*.json` 与“DB 唯一事实源、禁止 Write 战役 json”冲突（是否算“战役产物”未界定） | 路径用环境无关写法；声明该 JSON 属“一次性分析输出，可删”，或入库 |
| LB-05 | L74 | 情景·P2 | “返回接受/拒绝的机制及对 Python alpha 的启示”——无输出格式 | 给一个填好的例子（机制/字段/为什么接受/拒绝） |
| LB-06 | L78 | 边界·P2 | `rtk python3 …`（“本机沙箱代理运行器”）只存在于作者环境，同一行又说“无 rtk 用 `$WQ_PY`”；与 AGENTS.md“用 venv python”不一致 | 统一写 `& $WQ_PY …`；rtk 说明移到环境章 |
| LB-07 | L90 | 边界·P2 | “下游 Python alpha 设计禁止用 VECTOR/GROUP 字段”与 RA/GEM（VECTOR 用 `vec_*`、group 用 `group_*`）口径不同，未说这是 Python 轨道的限制 | 注明“仅 Python 轨道” |
| LB-08 | L93 | 边界·P3 | “体检数据包是 2012–2021 离线快照”与 RA 使用的 `WebData_20260219` 快照不符；“`check_expr_against_inspect`”函数在 `tools/webdata_quality.py`，RA 步 5 写的是 `field_inspect_gate.py` | 更新日期；指明函数所在与调用入口 |
| LB-09 | L95–98 | 情景·🟢 | 默认示例给了字段、角色（主信号/上下文）与倾向（状态切换/意外抽取优于水平值）及条件 | 作为全库“默认示例”写法参考 |

<a id="s6"></a>
### 6. `brain-forum-browse`（L0 · SKILL.md 258 行 + 9 个 references ≈1130 行 + 7 个模板 + 5 个脚本）

**审查方式说明**：SKILL.md 全文逐段；`modes-and-contract.md` 全文；`mcp-by-phase.md` 头尾与结构；其余 references 读标题结构并结合机械检查（§B/§C/§G），未逐段精读。

**定位**：中文论坛浏览（explore/contribute）与回测流水线的“问题驱动只读检索”（recon）。

**总评**：这是全库**体量/价值比最高**的 skill——约 1500 行文本在描述一个“逛论坛并强制贡献”的社交流程，而**当前环境只注册了两个论坛工具（`search_forum_posts`、`read_forum_post`，已核对），没有任何写工具**。于是标题规则（“每轮必以写操作结束、不允许只浏览、不可协商”）描述的是一个**跑不起来的模式**，真相（自动豁免降级只读）藏在 L59–68 的决策树和 L83–91 的引用块里。同一 skill 还承载了性质相反的第二职责（recon：只读、免贡献、免合同），而 RA 对它的 5 个调用点都直接调 `tools/forum_recon.py`，并不加载 skill。

| 阶段（行号） | 书写逻辑 | 职责划分 | 边界界定 | 需情景规范？ |
|---|---|---|---|---|
| frontmatter + 职责边界（1–25） | 🟡 | 🔴（两个相反职责） | 🟡 | 是 |
| 何时使用（29–40） | 🟡 | 🟢 | 🟡 | 否 |
| 运行模式表（42–55） | 🔴（术语先用后定义） | 🟡 | 🟡 | 是 |
| 最低贡献标准 + 决策树（57–77） | 🟡 | 🟢 | 🔴（与 L179 冲突） | **是** |
| MCP 默认 + 环境适配（79–101） | 🔴（排障藏在引用块） | 🟡 | 🔴（环境专有、口令） | **是（排障表）** |
| 执行模型（103–121） | 🟡 | 🟡 | 🔴（“不探测”与排障矛盾） | 是 |
| Search 工具箱 + 可用工具（123–151） | 🔴（自相矛盾、含不存在工具） | 🟡 | 🔴 | 否 |
| 首次运行前（153–175） | 🟡 | 🟡 | 🔴（路径/CWD） | 是 |
| 硬性规则（177–196） | 🔴（20 条，≥8 条重复） | 🟡 | 🔴（强度不一） | 是 |
| Pipeline / 记忆栈 / 配额 / 索引（198–258） | 🔴（阶段号无序） | 🟡 | 🟡 | 是 |

| # | 位置 | 维度·级 | 问题 | 改进建议 |
|---|---|---|---|---|
| FB-01 | L4 | 边界·P2 | description 中英混杂并含 markdown 粗体；把 explore/contribute 两个社交模式写入触发，recon 不在触发词里（而 RA 恰是它最大的调用方） | description 只写触发场景；recon 另立入口 |
| FB-02 | L23–24 | 职责·P1 | 一个 skill 同时是①社区互动（强制贡献 + Run Contract + 对抗审查 + curator）②流水线 recon（只读、免贡献/合同/工作区记忆）——治理规则**相反**。recon 规则在职责边界、模式表、配额三处各写一部分。RA 的 5 个触发点（步 1 复开、步 4 机制枯竭、步 5 KB 无货、步 7 卡闸、步 9 判死前）都直接调 `tools/forum_recon.py`，加载本 skill 只会带来 ~1500 行无关内容 | 拆成 `brain-forum-browse`（互动）与 `forum-recon`（≤80 行：触发表、`--out` 目标、额度、缓存、负结果入库）；RA 只指向后者 |
| FB-03 | L38 vs L24 | 边界·P3 | “不要用于提交前审查 → 用 `brain-alpha-judge`”，边界句却说提交审查归 `tools/submit_verdict.py`、judge 仅参考 | 统一指向 |
| FB-04 | L40、L46–47、L63、L179、L233；modes §1/§2 | 逻辑·P1 | “每轮必贡献/不允许只浏览/不可协商”至少**6 处**重复且措辞强度各异；而环境无写工具（`search_forum_posts`、`read_forum_post` 是仅有的两个）→ 这些规则**永远无法满足**；真相是“自动豁免、降级只读”（L59–68、modes §2 末段）。读者读到 L40 就会以为必须发帖 | 把“当前能力=只读”提到最前；写路径（Run Contract、auto-send E1、curator、对抗审查、templates/run_contract）整体标 **[DORMANT：仅当 MCP 出现 `create_forum_*` 时读取]**，并移入单独 reference |
| FB-05 | L44–49 | 逻辑·P2 | 表里先用 E1、7.5、Contract、6–9、auto-send，而 E1/E2/E3 到 L72/L180 才定义、Phase 编号从未在 SKILL.md 里成序列出现；四种模式含已弃用别名 `hybrid`（在表、Pipeline、modes 三处重复）；`modes-and-contract.md` 标题写“三种模式”，未含 recon | 首现处内联定义（E1=个人一手经验…）；`hybrid` 只留一处弃用注；modes 改“四种” |
| FB-06 | L55、L161、L192–195、L229、L246 等（约 30 处） | 边界·P2 | 链接**文字是已合并的旧文件名**（`auto-send-e1.md`、`profile-bootstrap.md`、`personal-perspective.md`、`external-memory-sources.md`、`merge-with-alpha-judge.md`、`file-workspace.md`、`index-post-protocol.md`），目标却是合并后的文件（机械检查 §C 列出 ~30 处“路径不存在”）。references 首行虽声明“旧文件名以现目录为准”，SKILL.md 自己仍用旧名当标签 | 标签改为“目标文件 § 小节”（`modes-and-contract.md §5 Auto-Send E1`）；旧名全部清除 |
| FB-07 | L59–68、L77、L179 | 逻辑·P2 | 决策树是全文最清楚的一处（好），却自称“唯一表述，替代分散规则”，而规则仍散落（FB-04）；L77“无话可说仍尝试 linker 式最小价值”与 L179“仅在有 E2 + 索引理由时才可用 linker 兜底”互相矛盾 | 决策树补第三支“只读环境→做什么（读帖后输出笔记，不写）”；linker 条件统一 |
| FB-08 | L83–91 | 边界·P2 | 引用块里有**高价值排障**（“服务没起=论坛工具‘不存在’、极易误判为未实现”；排查顺序 ①`start_wq_mcp.py --check` ②`MCP_PORT=8876` ③再报告；重启宿主会话），但：埋在“默认：MCP 完成一切”下的 `>` 块里；含环境专有细节（`localhost:8876`、“2026-08-17 实测可用”、服务名 `wq-brain-http`/`brain-platform-mcp`/`wq-brain-stdio`，mcp-by-phase 里还有第 4 个 `user-brain-api`）；“。。”笔误；L115 又重复一遍服务器信息。在以 stdio + `.mcp.json` 配置的环境里端口指引不适用 | 抽成“MCP 不可用排查”小表：症状 / 可能原因 / 检查命令 / 处置（含 stdio 与 HTTP 两种）；服务名与端点只写一处 |
| FB-09 | L93–99 | 边界·P3 | 表头是“**必须**用的 MCP”，第 5 行却是“wq-brain-http **未实现**” | 第 5 行移出表，单列“不可用能力” |
| FB-10 | L117、L98 | 边界·P1 | “凭据来自 MCP 服务器配置；**仅在认证失败时才传 `email`/`password`**”——与 AGENTS.md（凭据只在 `.env`、禁止读取/打印）及本 skill 自己 `mcp-tools-and-search.md`（“never read or commit credential files”）的红线不一致；且 harvest 会读宿主记忆文件，而 E1 又允许引用“宿主 AI 对话历史（P4）”**公开发帖**，全文没有脱敏规则 | 改“认证失败→停止并请用户修复服务端配置，不在对话中传口令”；补“公开内容脱敏清单”（账号/邮箱/私有路径/对话原文） |
| FB-11 | L117 vs L84–88 | 情景·P2 | “运行时**不要探测或列举 MCP 工具**”与“工具在表里搜不到时按排障顺序检查”并存 | 分情景：正常调用→直接用名；出现 unknown tool→按排障表 |
| FB-12 | L123–151 | 逻辑·P1 | 两个表重复同一批工具；L129 写 `search_forum_posts`“**唯一**搜索工具”，而标题“多种方法/自行选型”、L194“不必每次 slow，也不要只知道 fast”（fast/slow 工具已不存在）；表内“替代 list_help_center_articles / fast·slow·list 系列”是改名史；L149“已安装但超出范围：`delete_forum_comment`、`delete_forum_vote`”与反面模式“不用 `delete_forum_*`”——**这些工具未注册**（仅有 search/read） | 一张现役工具表（名、参数、用途）；删所有“替代/旧名/不存在”的条目 |
| FB-13 | L153–175 | 边界·P2 | 命令用裸 `python`、`scripts/…` 相对路径（仅当 CWD=skill 目录才成立）；`outputs/workspace/` 位置未说（skill 目录？仓库根？）；未说明 `harvest_external_memory.py` 为何读宿主记忆及其隐私影响 | 写全路径/`$SK/…`；声明工作区落点（建议 `.gitignored` 的固定目录）；harvest 补目的与只读边界 |
| FB-14 | L177–196 | 逻辑·P1 | “硬性规则”20 条：≥8 条重复前文（每轮必贡献×3、MCP 优先×3、论坛数据仅来自 MCP、默认 explore、Run Contract 闸、Search 工具箱）；“MCP 优先”（L182）与“先文件后 MCP”（L183）读起来矛盾（实义：先加载本地工作区，但论坛事实只能来自 MCP）；“**对抗性审查子代理**”假定宿主可派生子代理（本环境默认仅在用户要求时才可用）；curator/点赞依赖不存在的 upvote 工具 | 改成表：规则 / 适用（总是·仅写路径） / 由谁强制（代码·人工） / 出处；重复规则合并 |
| FB-15 | L198–217、L217 | 逻辑·P2 | Pipeline 阶段号非单调（7.5 → 1.5 → 6–9，Phase 7 在 6 与 7.5 之间），全文没有一份成序的阶段清单；“每个会话 **L1**”的 L1 与全库“L1 层”撞名（此处指论坛 L1/L2/L3 内容层级，未定义）；Role、Scout、Perspective Card、L2/L3 等术语在主文件无定义 | 补一张按执行顺序的阶段表并统一编号；内容层级改名（如 T1/T2/T3） |
| FB-16 | L219–229 | 逻辑·P3 | 记忆层 P0–P5 与全库其它 P 编号（S0 的 P5 饱和拍平、probe 模板 P5、审计 P-codes）同号异义 | 用名称（ledger/personal/project/user/host/platform） |
| FB-17 | L231–236 | 边界·P2 | “每次运行最多计划 3 个写操作”与“每轮必≥1”并存；recon 的 `--max-search-rounds` 只说是“安全上限”，无缺省数值 | 写缺省值 |
| FB-18 | L244–258 | 逻辑·P3 | 参考资料索引清楚（好），但括号里仍列已合并前的旧文件名 | 旧名放 CHANGELOG |

#### 6.1 `references/`

| # | 文件 | 维度·级 | 问题 | 改进建议 |
|---|---|---|---|---|
| FR-01 | `modes-and-contract.md`（79 行） | 逻辑·P2 | 头注“合并自 modes-and-contract.md / modes-and-contract.md / auto-send-e1.md”（自己出现两次）；“三种模式”遗漏 recon；§2 整段是 SKILL 的第 N 次复述 | 修头注与标题；§2 删 |
| FR-02 | 同上 §5 Auto-Send E1 | 边界·🟢 | **A1–A8 是全库最可检的条件清单**：恰好 1 条、E1-only、零推断（列出禁用词）、第一人称事实、含指标须本轮已调 `get_user_alphas`……并配“自检清单”与日志字段 | 作为“可检条件”范式推广 |
| FR-03 | 同上 §5（A3） | 边界·P2 | 允许“本机 AI 对话（P4）”作 E1 公开来源，未给脱敏/同意规则（FB-10） | 补 |
| FR-04 | `mcp-by-phase.md`（460 行） | 逻辑·P2 | 约一半是空行（逐行双倍间隔的转换痕迹）；中英混排；末尾“Decision tree”含改名残留：`get_glossary_terms, get_glossary_terms`、“`search_forum_posts`（try slow if sparse）”、`create_forum_*`（不存在）、“enable **user-brain-api**”（第 4 个服务名） | 压缩到 ≤150 行并修正 |
| FR-05 | `write-style-zh.md` | 逻辑·P3 | 机械检查 §B 报“断链 → url”是示例表格里的 `[文字](url)`，属**误报**；但整篇 136 行只在写路径开通后才有意义 | 归入 DORMANT 包 |
| FR-06 | 其余 references（contribution-and-diversity 93、evidence-and-review 116、recon-and-gap 122、workspace-and-memory 97、quotas 40、mcp-tools-and-search 85） | 边界·P2 | 均以“Phase/Run Contract/对抗审查/Role Matrix/Index Post”等写路径概念为主；`self_overlap < 0.4` 等阈值无依据；与 SKILL 有 9 处以“参考资料已合并”重复的头注（机械检查 §G） | 随 FB-04 整体归为 DORMANT；阈值给来源；头注只留一份 |
| FR-07 | `templates/`（7 个）、`scripts/`（5 个） | 职责·P3 | 模板与脚本都服务写路径；脚本用 skill 相对路径 | 同 FB-13 |

<a id="s7"></a>
### 7. `wq-brain-ppa-mining`（L0 · 321 行；另有 ra-pipeline 内 312 行近似拷贝 `ppa-mining-experience.md`）

**定位**：PPA 数据驱动挖掘方法论（WebDataScope 增强版）：平台体检硬门槛 + 数据集/字段级决策。

**总评**：内含大量有依据的经验（§1.3 “离线包缺≠平台缺”的 EUR 反例、§9.1 的 data-sets/data-fields 实测约束都是好范式），但**名不副实且已多处过时**：①名字是 PPA，内容主体是通用的数据集/字段选择方法 + API 笔记 + 2026-08 区域快照；②它宣称负责“PPA 主题匹配核查”，正文没有这一节；③最终“提交”步骤仍写 `tags=["PowerPoolSelected"]`、`color=GREEN`，而 submit/robustness 两个 skill 已证实合法 PPA 只能走平台 web UI；④“突破范式”是被禁的加权混合；⑤区域优先建议（news_sentiment_nlp“头号目标”）与后来的跨区死路先验相反。加上 ra-pipeline 内另存一份 312 行的近似拷贝，形成**两份会各自漂移的 PPA 方法论**。

| 阶段（行号） | 书写逻辑 | 职责划分 | 边界界定 | 需情景规范？ |
|---|---|---|---|---|
| frontmatter + 职责边界（1–24） | 🔴（466 字，触发过宽） | 🔴（承诺的核查缺失） | 🔴 | 是 |
| §0 总纲（27–36） | 🟡 | 🟡 | 🔴（写给浏览器 UI，非 agent） | **是** |
| 衔接协议（38–43） | 🟡 | 🟡 | 🟡（tier1 vs tier1+配额） | 否 |
| §1.0 硬门槛（47–96） | 🟡 | 🟡 | 🔴（执行器三个、0 优先与伪白空间冲突） | 是 |
| §1.0.x 亲和矩阵（98–123） | 🔴（“无需硬编码”却硬编码） | 🔴（复制 registry） | 🔴 | 是 |
| §1.1–§1.4 徽章/包可用性（125–149） | 🟢（§1.3 好） | 🟡 | 🟡（甜区口径与他处冲突） | 否 |
| §2 字段级决策（151–173） | 🟡 | 🟡 | 🔴（`is_placeholder` 不存在；加权混合范式） | 是 |
| §3 白空间/算子多样性（175–199） | 🟡 | 🟡 | 🔴（与 §1.0.x 矛盾） | 是 |
| §4–§5 参数与范式（201–242） | 🟡 | 🟡 | 🔴（C=5、SECTOR 矛盾、hump） | 是 |
| §6 闸门体系（244–253） | 🟡 | 🟡 | 🔴（margin/returns 分层错位） | 否 |
| §7 增强流程（255–267） | 🟡 | 🟡 | 🔴（权重扫描、提交渠道） | **是** |
| §8 区域实证（269–297） | 🔴（快照当指令） | 🔴 | 🔴 | 是 |
| §9 API 要点（299–321） | 🟡 | 🟡 | 🔴（合法档位已过期） | 否 |

| # | 位置 | 维度·级 | 问题 | 改进建议 |
|---|---|---|---|---|
| PP-01 | L4 description | 边界·P1 | 466 字；触发含“WorldQuant / WQ Brain / alpha 挖掘 / 用户要开新战役·换区域·问某数据集能不能打 → **必须先执行 §1.0**”，会被**所有 RA 战役**命中；但 L41、L90–93 明确 §1.0 的一票否决与排序只适用 mode=ppa，RA 走 D4。description 与正文冲突 | 触发限定为“PPA / Power Pool / 未点亮塔数据集体检”；“开新战役必须先体检”改为“**PPA 战役**必须” |
| PP-02 | L22 | 职责·P1 | 边界句声称负责“**PPA 主题匹配核查**”，全文找不到这一节（主题门禁实际在 RA 步 1 的 `get_messages` 扫描、`worldquant-submit-alpha` 的 `MATCHES_THEMES`） | 删这条承诺，或补一节并与 RA 步 1 对齐（谁扫、何时、结果写哪） |
| PP-03 | L29–36、L125–128、L151–164、L196–198、L260–265 | 情景·P1 | 大量步骤写成“读 hover 卡片 / 读徽章 / distribution.js 白空间表 / genius.js 算子分析”——这是 **Chrome 扩展的 UI 操作**，agent 无法执行；唯一给出离线路径的是 §1.1 一行 `tools/webdata_quality.py`。缺“每个面板对应哪条命令/哪个产物文件” | 每个面板补“agent 取数路径”：`webdata_quality.py --recommend / --fields` / `gen_field_inspect_packs.py` 产物（`field_inspect_*.json`）；UI 操作仅作“人工核对”备注 |
| PP-04 | L55–76、L257 | 边界·P1 | 体检执行器**三套**：本 skill 的 `scripts/dataset_health_check.py`（§1.0、§7 步 0 都要求“不可跳过”）、boundary 里写的 toolkit `score_datasets.py`（L24）、RA 的 `campaign_intel s0-select`（RA 称 `dataset_health_check.py` “零运行痕迹、已被 s0-select 取代”并归档其 ra-pipeline 副本；全仓库仅文档引用本脚本，无代码/测试调用方）。另含 `127.0.0.1:8876`、`--mode direct`（脚本自读 `.env`）等环境专有说明 | 声明单一执行器（PPA：`score_datasets.py mode=ppa` + `s0-select`），本脚本标“遗留/可选”或归档；环境细节移出 |
| PP-05 | L78–94 | 边界·P1 | ①cov 阈值有 0.85（硬门）、0.7（一票否决）两档，而 D4/代码用 0.65（文档）/0.7（代码缺省）、保底带 0.65–0.85；②“`alphaCount==0` 零竞争，优先级**最高**”与 toolkit `probe-scoring-v2`（“零竞争=高价值已被 EUR+GBR 证伪：ac<50 几乎全是伪白空间”）、D13、本文 §1.0.x（47% 死路是白空间无信号）**相反**；③适用域说明（PPA-only）放在规则**之后**的引用块里 | ①一张阈值对照表（PPA/RA、文档/代码缺省）；②改“ac=0 仅在 cov≥0.9 且字段≥10 且 fields 语义合规时优先探针”，并注明与 calibrate 的关系；③适用域移到本节第一行 |
| PP-06 | L96 | 情景·🟢/P3 | EUR 32 次回测教训有数据、有反事实，是好范式；但“若前置则完全可避免”的反事实后来未被验证（ac=0 集实测多为伪白空间） | 补一句后续验证状态 |
| PP-07 | L98–123 | 逻辑·P1 | 标题“规则引擎（从台账自动推导，**无需硬编码**）”，随后表内硬编码 KOR/MEA 区域特征与 6 组“当前已知红灯”（图表形态、新闻/情绪、AI/ML、信用风险、行为金融、GLB emotion），等于把 `registry_empirical` 的 dead_end 内容抄了一份快照（matrix 硬规则 1：registry 是唯一事实源）；“GLB emotion 判死 → **任何区域** emotion 红灯”由单区结论外推全区，与 matrix“不外推”、RA 的“跨区弱先验需 ≥16 条回测”口径不一 | 删快照，只留“红/黄/绿”判据 + 查询命令；跨区外推统一到 RA 的跨区先验规则 |
| PP-08 | L128、L157–164 | 边界·P2 | “sweet-spot：100 ≤ count ≤ 3000 且 sharpe ≥ 1.1×均值”与本文 §1.0 的 alphaCount≤50、toolkit calibrate 的甜区 50–1000 是**三个互相冲突的“最优拥挤度”**；无依据 | 表：mode（PPA/RA）× 拥挤度区间 × 出处 |
| PP-09 | L132–133、L224、L239 | 边界·P2 | 同一 skill 内：“KOR → SECTOR 最佳（0.562）”“按 dominant method（KOR→SECTOR）”与“SECTOR/MARKET 中性化大幅降低 IS_LADDER”“勿用”并存；D5 也称禁用 SECTOR/MARKET | 写清：仅当 dominant method 实测更优且 IS_LADDER 仍达标时；否则禁用 |
| PP-10 | L135–146 | 边界·🟢 | “离线包缺≠平台缺；离线包有≠平台有”+ EUR 四个集根本不存在的反例 + 规则“先体检确认存在且达标，判‘不可用’前换区查一遍”——**场景→规则→动作**齐全 | 范式；仅补一句“★★★ 偏好只影响本地分析质量，不代表平台可用” |
| PP-11 | L148–149 | 情景·P2 | “IS sharpe >> OS sharpe”用“>>”，无量化（field-quality 用“差 >0.15”）；对 KOR `model253` 的引用是个例 | 统一阈值 |
| PP-12 | L157–164 | 边界·P1 | 表里“极低(<30%) → **加 `is_placeholder`** 或换字段”——`is_placeholder` **不是 BRAIN 算子或字段**（仓库只有内部函数 `_is_placeholder`，用于算子元数校验），会被幽灵算子闸拦下；缺失/偏斜/峰度等阈值只写“低/高”，而 RA 步 5 的体检硬门有明确数值（cr<0.4、\|skew\|>2、kurt>8） | 删 `is_placeholder`，改“换字段/`ts_backfill`”；表中阈值与 `field_inspect_gate.py` 对齐 |
| PP-13 | L166–173 | 边界·P1 | “组合范式（V9 突破版）”：`scale(rank(ts_zscore(subtract(...),189))) + scale(-rank(ts_zscore(returns,42))) * 0.35`——**带 0.35 权重的两信号相加**，违反 RA“路线 A”与 CLAUDE.md“禁止混信号调参”；**但实测 gate.py 对该形态放行**（`X + Y * 0.35`，权重在右：poison regex `weighted_signal_mix`、`_detect_weighted_mix_structural`、`_detect_equal_weight_leg_add` 三者均不命中；权重在左的 `0.6*rank(A) + 0.4*rank(B)` 才被 regex 拦）——即政策已禁、闸门有缺口，上一轮评审 P0-2 所称“被闸5 block”对该形态不成立（详见综合篇 X-3）；§5 把它当“突破”（S=2.23）、§7 步 4 再教一遍；窗口 189、42 非标准窗口且无解释 | 标为“历史配方，违反路线 A（且当前闸 5 有缺口未拦）”并给合规改写（returns 反转作条件/分组，而非加法项）；窗口给依据或换标准窗口；闸 5 补“权重在右”与 `subtract` 形态（X-3） |
| PP-14 | L177–190 | 逻辑·P1 | §3.1 把 KOR 的 **Sentiment/Option/Macro 空白**列为“真·低竞争机会（重点）”，而 §1.0.x 把 KOR 新闻/情绪族列为**三连判死红灯**、§8 又把 `news59` 列为 KOR sweet dataset——同一区域同一类别三种相反结论；数据为 2026-08 离线快照 | 白空间表只作“候选池来源”，标注必须再过 §1.0 体检 + 跨区先验；快照移出 |
| PP-15 | L198–199 | 逻辑·P3 | 鼓励“补进极少使用的算子（如 `ts_regression`…）以满足 Genius 六维”，而 §5.9 又说 `ts_regression(A,B,n).residual` 语法无效；符号映射表（`+`→add…）是解析工具的实现细节 | 分“指标补齐”与“质量”；映射表移工具 |
| PP-16 | L217、L301 | 边界·P1 | “并发上限 **C=5**”出现两次，而 `config.CONCURRENCY.slots=7`（config 注释还专门记录了历史上 5/8/6/4/3 并存的问题）；D10 写“约 5–7” | 删数字，指向 wqb-concurrency |
| PP-17 | L209–215、L225、L303 | 逻辑·P3 | testPeriod 三个值并存：示例 `P0D`、最佳参数 `P6Y`、“最大 P6Y0M0D” | 说明各自语境 |
| PP-18 | L240、L304 | 边界·P1 | hump：“破坏性，**勿用**”（§5.7）与“`hump(x, hump=0.01)` **必须命名参数**”（§9）并存；D6 称“已废弃禁用”，RA 预闸却自动改写 hump 调用 | 全库统一 hump 的状态（见 RD-18） |
| PP-19 | L247–248 | 边界·P1 | 把 “Margin > 5bp、Returns > 5%” 列为**平台硬线**；`config.GATES_PLATFORM` 没有这两项，`GATES_INTERNAL` 是 margin ≥10bp、returns ≥5%（内部线）——5bp 既非平台线也非内部线（D0、probe-scoring 同样写 5bp）；“PC 等待”“PPAC”缩写首现无解释 | 与 `config.GATES` 逐项对齐并标注内部/平台；缩写展开 |
| PP-20 | L257–267 步 4、5 | 边界·P1 | 步 4“建 reversed spread，加 returns 反转组合”＝PP-13 的混合；步 5“**权重**/窗口/中性化/truncation 微调”＝参数扫描，与 CLAUDE.md“禁止混信号调参”“非窗口数值须有取值理由”及 RA“不得调权重/补参数变体凑数”冲突 | 删“权重”，参数只在“有依据的少数维度”内做，并记录取值理由 |
| PP-21 | L267 步 8 | 边界·P1 | “**提交**：`tags=["PowerPoolSelected"]`, `color=GREEN`”——`worldquant-submit-alpha` / `brain-alpha-robustness` 已写明：MCP `submit_alpha` 非 PPA 感知，打该标签重试仍被拦，**合法 PPA 只能走 web UI 且限当期活跃主题窗口** | 改为“PPA 由用户在 web UI 提交；agent 产出清单 + 主题匹配证据”，并引用 submit 的“PPA 通道”节 |
| PP-22 | L269–297 §8 | 边界·P1 | 2026-08-05/23 的区域快照（KOR 192 集、EUR 178 集、HKG 209 集；“首选 `news_sentiment_nlp`：三区 alphaCount=0，性价比最高的入口”；区域优先级 HKG≈KOR>EUR）被当作**行动指令**。此后的证据反向：新闻/情绪在 USA/EUR/IND 同型全灭（RA 跨区弱先验）、KOR 新闻三连死、ac=0 多为伪白空间。8 周旧的“头号目标”会把 agent 送回死路 | 快照挪进 `reports/`/DB 并标日期与失效条件；此处只写“选区前跑 §1.0 与 `s0-select`，以实时数据与跨区先验为准”；倍率差表保留方法、去掉结论 |
| PP-23 | L299–307 | 边界·P2 | “自行实现 `_reauth()`”与“禁止手写 requests、用 `BrainApiClient`”冲突；429 退避写了第三种（`min(20+attempt*8,45)s`，~40 次），toolkit 是 5 次 ×2；一行 900 字的工具/节点罗列并提及 “lavender1203 fork、端口 8876、Trust” | 删实现建议，指向 `BrainApiClient` 与 wqb-concurrency；MCP 说明移 INDEX |
| PP-24 | L313–318 | 边界·P1 | 合法 universe 表仍含 `ILLIQUID_MINVOL1M`（USA/EUR/ASI）；`config.REGIONS` 注释：2026-09-22 已从 USA/EUR 档位表移除，RA 步 6 亦称永久停提；matrix 硬规则 3 明令“回代码常量核对，不凭记忆” | 删该表，改“`get_platform_setting_options` + `config.REGIONS`” |
| PP-25 | 全文 vs `ra-pipeline/references/ppa-mining-experience.md` | 职责·P1 | 两份 PPA 方法论（24 段重复，Jaccard 0.50）；ra-pipeline 版还引用不存在的 `wq-brain-ra-pipeline/scripts/dataset_health_check.py`、`tools/eur_field_coverage.py`；RA“PPA 分支”指向后者，本 skill 又说“PPA 编排走 RA” | 只留一份；RA 的副本改成 ≤30 行“PPA 与 RA 的差异表 + 指针” |
| PP-26 | L309–321 §9.1 | 情景·🟢 | 六条实测约束（数据集级体检走 `get_datasets`；`/data-fields` 四参齐全；非法 universe 报 500 而非 400；TLS 抖动优先复用常驻 MCP 会话…）**症状→原因→处置**清楚 | 保留；合法档位表按 PP-24 处理 |

<a id="s8"></a>
### 8. `brain-alpha-research`（L1 · 63 行 + 7 个 references 852 行）

**定位**：研究方法总入口 + 三个专项子 skill 的路由（news-sentiment / hypothesis-first / field-quality）。

**总评**：路由表是好设计，但**正文其实是给“开发者扩展搜索空间”的清单**（读 `evidence.py`、补 `config.py`、扩 `PARADIGMS`/`_OP_ARITY`、跑 `wqb research`），而非给“做数据集研究的 agent”的指引——两类读者混在一份 63 行里；13 个“步骤”里 6 个是流程、7 个是带日期的知识条目（日期括号密度 15.9/百行，全库最高）。验证清单要求运行的 `wqb research` / `wqb settings` **命令在仓库里不存在**（无 `cli.py`，`pyproject.toml` 无 scripts 入口；`docs/plans/2026-08-02-wqb-src-reconstruction.md` 里只是计划）。7 个 references 有 5 个无入链。

| 阶段（行号） | 书写逻辑 | 职责划分 | 边界界定 | 需情景规范？ |
|---|---|---|---|---|
| frontmatter + 触发（1–24） | 🟡（触发段重复 description） | 🟡 | 🔴（与 4 个 L1 skill 触发重叠） | 是 |
| 职责边界（14–18） | 🟡 | 🔴（“不当第二作者”却维护固化表） | 🟡 | 是 |
| 专项路由表（26–35） | 🟢 | 🟡（漏 2 个 L1 通用 skill） | 🟢 | 否 |
| 工作流 步 1–6（37–44） | 🟡 | 🔴（开发者向） | 🟡 | 是 |
| 步 7–9 论坛模板/算子/形状（45–50） | 🟡 | 🟡 | 🔴（check_batch “过闸条件”不实） | 是 |
| 步 10–13 固化表/API/优先级/陷阱（51–56） | 🔴（知识条目当步骤） | 🔴（3 处重复） | 🔴（快照当指令） | 是 |
| 验证清单（58–63） | 🔴（命令不存在） | 🟡 | 🔴 | 是 |
| references（7 个） | 🟡 | 🔴（核心文档放错 skill） | 🟡 | 否 |

| # | 位置 | 维度·级 | 问题 | 改进建议 |
|---|---|---|---|---|
| AR-01 | L4、L22–24 | 边界·P2 | description 与“触发场景”段几乎逐字重复；“数据集发现/字段选择/类别映射”与 `brain-dataset-exploration-general`、`brain-datafield-exploration-general`、`wq-brain-ppa-mining`、`brain-data-feature-engineering` 均重叠 | description 只写“**研究方法/搜索空间扩展**（含论坛/论文整合）”；删触发段 |
| AR-02 | L16–17、L51 | 职责·P1 | 边界句：“不得自行修正/撤回 `config.py` 权威常量；skill 不是常量的第二作者”，同一文件却在步 10 维护“全区域 universe/delay/中性化固化表”约束、在步 12 维护区域优先级观测——正是第二作者行为；“修正/撤回”一词又出现在步 12 标题（指 EUR 死路撤回，是研究结论而非常量） | 边界句改成“常量只引用 config；研究结论可写但须标日期与失效条件”；步 12 标题去“撤回” |
| AR-03 | L26–35 | 职责·P2 | 路由表只列 3 个专项 + “其他（本 skill）”；未列同为 L1 的 dataset-exploration / datafield-exploration / feature-engineering（news-sentiment 反而把它们当“通用 L1”）；机械检查 §K：research→hypothesis-first/news-sentiment 均无回指 | 路由表补全 7 个 L1，并给“选哪个”的一句判据 |
| AR-04 | L37–44 步 1–6 | 职责·P1 | 读者是开发者：读源码（`evidence.py`）、补 `config.py` 缺项、扩 `PARADIGMS`；agent 视角的“研究”产出无格式（步 6“机器可读的简明记录”未给 schema/落点）；步 2 “缺失…先在那里补齐（config）”与边界“不得修正”边界不清 | 分“研究者步骤”与“维护者步骤”两节；给记录 schema 与落点（如 ledger `KB/...` 键）；补“新增 vs 修正”的判据：仅新增且经平台实测才可写 config |
| AR-05 | L39 | 逻辑·P2 | 步 1 要求“读源码 `src/wqb/research/evidence.py` 理解最新设计信号”，链接为 skill 相对路径（skill 被同步到其它宿主目录后失效）；应是运行命令输出 | 改为运行入口（若该命令存在） |
| AR-06 | L45–47 | 边界·P2 | 落点清楚（`KB/community_tpl_kb` / `KB/template_kb`，不是代码模板表）——好；但 L46 整段是“已删除模块”的史注，`paradigms.py` 仍在 references/jump-decay-methodology.md、alpha-inspiration…等处被引用（机械检查 §C）；步 7 的 `kb_templates.py --emit-ideas` 把**确定性模板**注入 GEM，与 RA“模板渲染的 ideas 不得注入 GEM（会让 GEM 一行 LLM 都不调）”的规则未对账 | 史注移 CHANGELOG，清理 references 里旧符号；写明 `--emit-ideas` 的产物只能作**人读参考**或经 LLM 改写后注入 |
| AR-07 | L49–50 | 边界·P1 | “形状覆盖…`validator.check_batch` 正是按 shape signature 判重（≥2 shape signatures），所以形状覆盖是**过闸条件**”——RA 步 5 已于 2026-09-17 声明该函数**零调用方、只作方法论参考、不构成门禁**；`config.SHAPE_CLASSES` 实为 4 类 `{S1,S4,S5,S9}`，此处写 5 类含 S0 | 删“过闸条件”句；SHAPE_CLASSES 与代码对齐 |
| AR-08 | L51 | 边界·P2 | 固化表要点（COUNTRY 中性化仅 EUR/GLB/ASI/MEA；Delay=0 仅 USA/EUR/CHN/GBR/DEU）与 ppa-mining（Delay 0 仅 USA/AMR/EUR 数据广）、D5（MEA 仅 D1）、`config.REGIONS`（USA/EUR/CHN 等 delays）三处说法不一，且均硬编码 | 只引用 `config.REGIONS`，并写“支持 vs 数据广”的区别 |
| AR-09 | L52 | 逻辑·P3 | API 实测约束 (a)–(e) 是 ppa-mining §9.1 与 ra-pipeline/ppa-mining-experience 的第 3 份拷贝；(e) 含 `localhost:8876` | 只留一份，其余指针 |
| AR-10 | L53–55 步 12 | 边界·P1 | 2026-08-05 快照（HKG 209/KOR 192/EUR 178 数据集、“19 个未开发数据集首选 `ml_factor_proj`”）当作 S0 旁证保留，并在正文里**标注与 `config.REGION_PRIORITY` 冲突后裁定以 config 为准**——冲突处理过程写进了 SOP（审计日志），而不是删掉过期观测；与 ppa-mining §8 完全重复 | 删除快照；只留“区域优先级=config，选区用 `region_rotation`/`s0-select`” |
| AR-11 | L56 | 逻辑·P3 | 步 13 与 ppa-mining §1.3、ppa-mining-experience 重复；离线包星级说明第 3 次出现 | 单一出处 |
| AR-12 | L58–63 验证清单 | 情景·P1 | “运行 `wqb research` / `wqb settings`”——**仓库无此 CLI**（无 `cli.py`、`pyproject.toml` 无 scripts）；“确认 §10–§13 被读取消费”指向的是编号步骤而非 §，且无法检验 | 改为可执行断言（例如具体 pytest/脚本）或删；清单每项写“期望输出” |
| AR-13 | `references/`（7 个，852 行） | 职责·P1 | ①5 个无入链（`alpha-inspiration-usa-d1-shortinterest-insiders`、`asi-methodology`、`backtest-experience-archive`、`forum-template-library`、`jump-decay-methodology`）——价值不明地藏在目录里；②`webdatascope-data-quality.md`（357 行，规则 1–26）是 field-quality 与 ppa-mining 的核心依据，却放在总入口 skill 下并被跨 skill 相对链接引用；field-quality 写“23 条规则”，实际 26 条；③`backtest-experience-archive` 用 Obsidian `[[wikilink]]`、数据源写 `wqb-share-03/tracking/`（旧检出名）；④`jump-decay-methodology` 是“权限未开放，先沉淀”的推测性文档；⑤多篇表达式声称已过 `check_batch` 校验（该函数已非门禁） | SKILL 里为每个 reference 写一行“何时读”；`webdatascope-data-quality.md` 移入 field-quality；清理旧路径/wikilink；推测性文档标 [未验证] |

---

<a id="s9"></a>
### 9. `brain-alpha-research-field-quality`（L1 · 76 行）

**总评**：结构清楚，§2 里“数据包区域覆盖边界”的**判定顺序**（先确认区域在包内→预筛；不在→改走平台侧并在台账记免预筛理由）是全库少见的**场景化决策序**，值得推广。核心风险有两个：**字段种子规则与 RA 的 prod-corr 规避规则方向相反**；**“必须预筛”的强制纪律对 5 个区域不可满足且未接入流水线**。

| 阶段（行号） | 书写逻辑 | 职责划分 | 边界界定 | 需情景规范？ |
|---|---|---|---|---|
| frontmatter + 职责边界 + 触发场景（1–25） | 🟢 | 🟢 | 🟢 | 否 |
| §1 字段质量先验（28–38） | 🟡（`jq` 依赖、结果落点） | 🟢 | 🔴（与 RA 步 3 的 prod 墙方向相反） | 是 |
| §2 数据包质量预筛（40–62） | 🟢（判定顺序清楚） | 🟡（规则在别的 skill 的 reference） | 🔴（饱和阈值 3 套） | 是 |
| §3 区域切换预筛门禁（64–70） | 🟡 | 🟡 | 🔴（强制纪律 vs 包内无此区；待办写进 SOP） | 是 |
| 验证清单（72–76） | 🟢 | 🟢 | 🟡（无期望输出/留痕位置） | 是 |

| # | 位置 | 维度·级 | 问题 | 改进建议 |
|---|---|---|---|---|
| FQ-01 | L28–38 §1 | 边界·P1 | “按 `alphaCount` **降序**排字段、从分布头部开始播种（社区反复用来构建可提交 alpha 的字段更可靠）；低使用量字段只用于去相关/新颖性”——与 RA 步 3 / `prod-corr-avoidance.md`（**users≥50 只做方向验证；冷门字段占批次预算 ≥50%**；高使用字段 prod_corr 必超）**方向相反**。在饱和数据集（hypothesis-first 的适用域）里叠加则最糟。此条源自 2026-06-19 用户指令，之后被 2026-08-05 实测推翻 | 明确分阶段：alphaCount 高＝覆盖/稳健**先验**，用于**选集/研究方向发现**；进入字段级投入时服从 RA 步 3 的 users 分级；在 §1 首行标“受 RA 步 3 约束” |
| FQ-02 | L36 | 边界·P2 | “用 `jq` 把保存的 `get_datafields` 结果排序取前 ~30”——`jq` 在 Windows 环境未必存在；DB 唯一模式下字段目录在 `fields` 表，应查库；“保存的结果”落点未定 | 改 SQL/MCP 查询 |
| FQ-03 | L46–54 | 边界·P1 | 规则速查 (a)“甜点区 100≤count≤3000 且 sharpe≥1.1×均值；<50 不可信、**>30K 饱和**”——饱和阈值 30K，而 RA 步 2 #6 用 **1 万**、probe-scoring 拥挤罚用 5000、ppa-mining 要求 alphaCount≤50；“与 §1 的 alphaCount 先验互补”实际与之冲突 | 一张“拥挤度阈值表”（模式 × 用途 × 阈值 × 出处） |
| FQ-04 | L44 | 职责·P2 | 核心 26 条规则在另一个 skill 的 reference（`../brain-alpha-research/references/…`，跨 skill 相对链接），且写“23 条”与实际 26 条不符 | 文件移入本 skill，数字改“见文件” |
| FQ-05 | L56–62 | 情景·🟢 | 数据包覆盖边界（7 区、9 组合、160 条/125 名）+ 判定顺序 + 免预筛留痕——**场景→顺序→动作**清楚；小笔误“这此区域” | 范式；补留痕 **key 名**（见综合篇“豁免协议”） |
| FQ-06 | L64–68 §3 | 边界·P1 | “**每次切换区域回测前必须**先跑 `webdata_quality.py`（用户强制纪律）”，但 DEU/IND/GBR/MEA/TWN 不在包内，预筛必空；本节未提上一节的豁免；命令写死 `wqb-share-03/` 目录与裸 ZIP 名（§2 用 `research-data/`）、“Windows 用 python 非 python3”；含违规史（“USA/GBR subagent 启动时未先跑”） | §3 引用 §2 的判定顺序；路径统一；违规史移出 |
| FQ-07 | L70 | 边界·P1 | “机器门禁 `prescreen_gate.py`……当前为工具级门禁，节点内嵌接线待 `nodes/campaign.py` 并行改动落定后跟进”——待办状态写进 SOP；且 ra-pipeline / matrix / toolkit 均**没有任何一处调用它**（已核对），所谓“用户强制纪律”实际不在流水线里 | 接入 RA 步 2 前置，或降级为“可选自检”并删“强制”字样 |
| FQ-08 | L72–76 | 情景·P2 | 验证清单 3 条都是“确认已…”，无期望输出/无留痕位置 | 每条写产物（哪个 ledger 键/输出行） |

---

<a id="s10"></a>
### 10. `brain-alpha-research-news-sentiment`（L1 · 76 行）

**总评**：边界句最具体的一份（“不覆盖非 news/sentiment 数据集”），5 家族分类与“覆盖<0.4 必须 backfill，否则 5–10 只股票集中持仓”的**原因说明**都很好。主要问题：①核心“6 桶框架”**不在本 skill 内**（只在 `docs/reference/news_bucket_field_map.md`，且链接文字与路径不符）；②“冷启动优先路由 Tier A”是 2026-04/08 的静态规则，与 RA 的**跨区弱先验/已判死清单**冲突；③验证清单里的 `wqb news-refresh-portfolio` 命令不存在。

| 阶段（行号） | 书写逻辑 | 职责划分 | 边界界定 | 需情景规范？ |
|---|---|---|---|---|
| frontmatter + 职责边界 + 触发场景（1–25） | 🟢 | 🟢 | 🟡（“字段分类”触发与 dataset-exploration 重叠） | 否 |
| §1 5 家族分类 + 6 桶框架（28–44） | 🟡（“M”双义） | 🟢 | 🔴（6 桶定义不在本文） | 是 |
| §2 news12 专项补充（46–59） | 🟡 | 🟡 | 🟡（日期快照无失效条件） | 是 |
| §3 Tier A 组合核对（61–70） | 🟡 | 🟡 | 🔴（名单快照；`wqb` CLI 不存在；告知后无分支） | **是** |
| 验证清单（72–76） | 🟡 | 🟢 | 🔴（命令不存在） | 是 |

| # | 位置 | 维度·级 | 问题 | 改进建议 |
|---|---|---|---|---|
| NS-01 | L38–42 | 边界·P1 | 6 桶的**名称与定义没有写在 SKILL 里**（只出现“Event / Dispersion / Propagation 三桶高优先”），依赖 `docs/reference/news_bucket_field_map.md`（仓库根 docs，skill 相对链接不通；链接文字写 `reference/…`）；验证清单里的“≥3 桶/批、≥1 HIGH、≥2 vec_op、shape_variety≥2”中 HIGH、vec_op 均未定义；§2 又用 surprise/change/event 桶名映射 M1–M6 | 把 6 桶表（名称/含义/优先级）内联到 SKILL；术语首现处定义 |
| NS-02 | L48–59 | 逻辑·P2 | R/A/V/M/T 的 “M” 与 motif “M1–M6” 同字母；“M4 → surprise **或** change”未说何时取哪个 | 改字母；给取舍判据 |
| NS-03 | L61–70 | 边界·P1 | “冷启动任务路由到 **Tier A**（fieldCount≥50 且 alphaCount/fieldCount≤5 且 pyramidMultiplier≥1.2）：news_transformer_scores / sentiment22/23 / news94/29/73/23/59 …”——静态清单，未接入 `get_dead_ends`、`s0-select` 的 `[跨区弱]` 标记与 lit 塔规则；RA 记录 news/sentiment 在 USA/EUR/IND 同型全灭、IND 的 news79/nst/sentiment21 已判死、KOR 新闻三连死。验证清单第 3 条把“优先路由 Tier A”固化为检查项，会**系统性把 agent 送回已判死数据集** | 路由前先过“死路/跨区弱/lit”三查；Tier A 改为**候选来源**而非默认；给一条判据：命中判死则不路由 |
| NS-04 | L70、L76 | 情景·P1 | `wqb news-refresh-portfolio` 命令**不存在**（同 AR-12） | 改可执行入口或删 |
| NS-05 | L68 | 情景·P2 | “Tier B 已饱和——挖掘前必须向用户标注”只有告知，没有“告知之后怎么办”的分支（继续/放弃/换结构） | 加决策：用户确认后仅允许“高度非对称结构”，且需先做 prod-first |
| NS-06 | 全文 | 边界·P3 | 多个日期括号（2026-04-21/23）和数据快照（120K α 等）未标失效条件 | 标注“以 DB 为准” |

---

<a id="s11"></a>
### 11. `brain-alpha-research-hypothesis-first`（L1 · 105 行）

**总评**：假设目录的 JSON schema 以代码常量为唯一权威（`_REQUIRED_FIELDS`）并留有更正记录，节点参数写得具体，是好写法。核心缺口是**闭环缺一环**（“派发 4 条”之后如何回测并喂给 `judge()` 没写），以及与 RA 步 2 #6 的“强制切换”**互相矛盾**。

| 阶段（行号） | 书写逻辑 | 职责划分 | 边界界定 | 需情景规范？ |
|---|---|---|---|---|
| frontmatter + 职责边界 + 触发场景（1–30） | 🟡（上游写错） | 🟡 | 🔴（与 RA 步 2 #6 强制路由互相矛盾） | 是 |
| §1 何时切换（33–36；触发信号 26–35） | 🟡 | 🟢 | 🟡（个例数字、论坛帖作信号） | 是 |
| §2 field_semantics（37–48） | 🟡 | 🟡（与闸 SEM 两套字段语义） | 🟡（文件态） | 是 |
| §3 hypothesis_catalog（49–69） | 🟡 | 🟡 | 🟡（示例窗口 20 非标；12 类 vs 10 类映射） | 是 |
| §4 派发 `run_hypothesis_round`（70–73） | 🔴（只产计划，后续无入口） | 🟡 | 🟡 | 是 |
| §5 判定 verdict（74–83） | 🟡 | 🟡 | 🟡（又一套 verdict 词汇；“≈”无阈值） | 是 |
| §6 台账 + workflow 衔接（84–93） | 🟡（两个台账位置） | 🟡 | 🟡 | 否 |
| 与其他 skill 的关系 + 验证清单（94–105） | 🟡 | 🟡 | 🔴（沿用字段质量先验 = 饱和集撞 prod 墙） | 否 |

| # | 位置 | 维度·级 | 问题 | 改进建议 |
|---|---|---|---|---|
| HF-01 | L16–17 vs RA 步 2 #6 | 边界·P1 | 本 skill：“假设目录为空时**不强行路由**（需先有假设生成器）”；RA：数据集 alphaCount≥1 万或连续 2 波全灭 → “**强制**切本工作流，不再做模板遍历”。新数据集默认没有目录、也没有“假设生成器”，强制切换会死锁 | 写分支：目录缺失 → 由 agent 按 §3 起草 ≥20 条（或先做 1 波 GEM 概念优先），并标注谁来批准 |
| HF-02 | L18 | 逻辑·P2 | “上游 = 字段扫描产出的假设目录”不准：目录由 agent 按 §3 手写，字段扫描不产假设 | 改“上游=字段语义元数据 + 人工/LLM 起草” |
| HF-03 | L26–35 | 边界·P2 | 三个切换信号：α≥10K（量化）、“90 条模板会话已见顶（news12 Fitness≈0.42）”（个例数字）、“论坛高赞自动化流程…已把模板空间挖到天花板”（无法度量），而 §1 写“满足其一即切换”；RA 的口径是“≥1 万 或 连续 2 波全灭” | 统一为 RA 的两条可测信号，其余作背景 |
| HF-04 | L37–47 | 边界·P2 | 新产物 `data/field_semantics/*.yaml`（`anchor_only` 等）与 RA 闸 SEM 的 `s1_semantic_<ds>` 台账（signal/blocked 字段）是**两套字段语义**，互不引用；且均为文件态，与“DB 唯一”冲突（L92 承认“DB 化待后续”） | 说明关系（anchor_only ⊂ blocked？），合并或互引 |
| HF-05 | L55–66 示例 | 情景·P2 | 示例窗口用 20（非标准窗口，CLAUDE.md 要求 1/5/22/66…，RA 预闸会别名 20→22）；`control_constant` 的内容是 `volume` 的 z-score，并非“常数对照”；`variant` 含省略号 | 示例改标准窗口；对照命名与内容一致 |
| HF-06 | L68 | 逻辑·P3 | 12 类假设与 `concept-taxonomy-map.md`（只映射 10 类，缺 `under_reaction`、`event_conditional`）不一致 | 补全映射或注明未映射类 |
| HF-07 | L70–72 | 逻辑·P1 | “`run_hypothesis_round` 派发一个实验=4 条 alpha”，节点说明写“**实跑纯本地构建、不触平台**”——所以这一步只产**计划**；此后怎样入库、过闸 5、回测、再把 Sharpe 交给 `judge()`，全文没写；验证清单只验“派发 4 条” | 补“计划→入库→闸→回测→judge”的顺序与工具，产物与完成定义 |
| HF-08 | L74–82 | 边界·P2 | 判定四态（rejected/partially_supported/supported/needs_refinement）是**又一套 verdict 词汇**；“伪信号（主 Sharpe≈对照 Sharpe）”的“≈”无阈值；`rejected`“结案”与 registry `dead_end`、RA“未选/未回测不得写 dead_end”的关系未定 | 给阈值（例如 \|ΔSharpe\|<x）与“rejected ⇒ 是否写 dead_end”的规则；词汇表登记 |
| HF-09 | L84–86、L92 | 逻辑·P2 | 台账位置两处不同：`data/hypothesis_ledger/<session>.jsonl`（§6）与 `tracking/hypotheses/ledger.jsonl`（衔接节）；“元学习取代逐臂 bandit 后验”无解释 | 统一路径；术语解释或删 |
| HF-10 | L98 | 边界·P1 | “字段质量先验（alphaCount/userCount）仍作种子排序依据”——**饱和数据集里的高使用字段最易撞 prod 墙**（RA 步 3），与 FQ-01 同源冲突 | 饱和场景改为“反向：冷门字段优先”并引用 RA 步 3 |

---

<a id="s12"></a>
### 12. `brain-dataset-exploration-general`（L1 · 84 行 + 436 行英文 reference）

**总评**：职责边界写得对（“区域/universe 档位一律引用 config，不得自行维护区域表”），但**正文随即自己维护了一张区域表并给出旧公式**；Phase 2 的字段分类不产出任何可被下游消费的产物；Phase 5 让 agent 去“查阅论坛”，路由到会触发强制贡献流程的 skill。

| 阶段（行号） | 书写逻辑 | 职责划分 | 边界界定 | 需情景规范？ |
|---|---|---|---|---|
| frontmatter + 运行环境（1–19） | 🟡（环境句在 H1 前、7 个空行） | 🟡 | 🟡（“跨平台调研”无对应步骤） | 否 |
| 职责边界（22–32） | 🟢 | 🟡（上游=S0 与 Phase 1“选数据集”并存） | 🟡 | 否 |
| Phase 1 数据集选择与初步评估（33–39） | 🟡 | 🟡 | 🟡（选集无判据） | 是 |
| Phase 2 字段分类（40–46） | 🟡 | 🟡 | 🔴（产出位置缺失，下游要 `s1_semantic_<ds>`） | **是** |
| Phase 3 双门槛评分与探针（47–52） | 🟡 | 🟡 | 🔴（旧式公式，指向的文档已声明废弃） | 是 |
| Phase 4 增强描述与分析（53–56） | 🟡 | 🟡 | 🟡（无输出位置；1000+ 字段不可行） | 是 |
| Phase 5 整合（57–60） | 🟡 | 🟡 | 🔴（调研 = 查论坛，与 RA“默认不查”冲突） | 否 |
| Region → Universe 表（61–80） | 🟢 | 🟡（边界句禁止自行维护区域表） | 🔴（JPN 结论与 RA 相反） | 否 |
| 核心职责 + reference.md（81–84；436 行） | 🟡（英文岗位手册体裁） | 🟡 | 🟡 | 否 |

| # | 位置 | 维度·级 | 问题 | 改进建议 |
|---|---|---|---|---|
| DE-01 | L2–4、L18 | 边界·P3 | description 中“跨平台调研”正文没有对应步骤；“字段分类”触发与 news-sentiment 重叠；运行环境句在 H1 之前、7 个空行 | 触发限定“数据集级审计”；整理头部 |
| DE-02 | L25 vs L61–73 | 边界·P1 | 边界句禁止“自行维护区域表”，随后维护一张“Region → Universe”表；表中 **JPN “不是有效的 EQUITY 区域，`get_datasets` 返回 0”**，而 RA 有 JPN profile、12 集白名单与 w7/w8 实测，`config.REGIONS` 含 JPN——**四个 skill 对 JPN 状态说法不一**（matrix：未启用；RA：已补 profile；ppa-mining：universe 表无 JPN；本文：无效） | 删表，改“`get_platform_setting_options` + `config.REGIONS`”；JPN 状态只在 INDEX 维护 |
| DE-03 | L24–26 vs L34–35 | 边界·P2 | 边界说“上游=S0 白名单（数据集已选定）”，Phase 1 第 1 步又是“确定数据集：根据战略重要性或用户需求选择”且无判据 | 改“对白名单内某集做审计”；无白名单时转 RA 步 2 |
| DE-04 | L40–45 Phase 2 | 情景·P1 | 字段分类按业务职能/数据类型/频率/层级，**没有产出位置**；下游 RA 的硬前置是 `s1_semantic_<ds>` 台账（`field_semantic_classify.py` 产出，缺失则整波 exit 2）——本 skill 的分类与它不是一回事，且**全库共有 5 套字段分类法**（本文 4 维、news 5 家族、dfe 8 问、SEM 十大类、hypothesis 12 类），互不索引 | 明确本 skill 的分类产物落点与用途；建“字段分类法一览”指针 |
| DE-05 | L47–51 Phase 3 | 边界·P1 | 给出的评分公式是**旧式**：`0.30/(1+log10(1+alphaCount))`、“vs 缺失按 0.3”、tier2“cov≥0.85/ac≤200/fc≥5”；而其指向的 `probe-scoring-v2.md` 已写明旧式废弃（v3.1 为分段罚、vs 缺失按 0.5、分位分层、硬地板） | 删公式与阈值，只留指针 |
| DE-06 | L57–59 Phase 5 | 边界·P1 | “调研：查阅论坛（`brain-forum-browse` skill 或 `search_forum_posts`）”——与 RA“论坛默认不查（token 黑洞）”冲突；加载 `brain-forum-browse` 会进入“每轮必贡献/Run Contract”流程（FB-04），应指向 recon（`tools/forum_recon.py`） | 改指 recon，并写触发条件（判死复开/机制枯竭） |
| DE-07 | L53–55、L81–84 | 情景·P2 | “撰写详细描述”“改进描述”“为所有字段编目”——无输出位置/格式；对 1000+ 字段的数据集（JPN analyst 1026）不可行，无范围控制 | 定产物（DB `datasets`/`field_profile` 或报告）与上限（Top N/按覆盖） |
| DE-08 | reference.md（436 行英文“Job Duty Manual”） | 逻辑·P3 | 英文岗位手册体裁（Position Overview、Deliverables），与中文 SKILL 混用；含旧流程 | 精简或标注为背景资料 |

---

<a id="s13"></a>
### 13. `brain-datafield-exploration-general`（L1 · 88 行 + 194 行 reference）

**总评**：6 种方法各给“表达式 + 解读 + 改变哪个参数”，EVENT 字段的陷阱有**具体报错文本**与 KOR 实证，是好写法。但 **VECTOR 备注与全库闸门方向相反**，且未说明这些“探测”每个都要**占用一次仿真**。

| 阶段（行号） | 书写逻辑 | 职责划分 | 边界界定 | 需情景规范？ |
|---|---|---|---|---|
| frontmatter + 职责边界 + 总述（1–35） | 🟡（“6 种”与实际编号不符） | 🟡（测完怎么用缺链接） | 🟡 | **是**（仿真成本/合批） |
| 方法 1–4 覆盖率/非零/频率/范围（36–54） | 🟢 | 🟢 | 🟡 | 是（成本） |
| 方法 5 中心趋势（55–58） | 🟡（窗口 1000 非标） | 🟢 | 🔴（`ts_median` = 幽灵算子） | 是 |
| 方法 6 分布形态（59–62） | 🟢 | 🟢 | 🔴（`scale_down` 不在已验证清单） | 是 |
| 备注 VECTOR（63–65） | 🟡 | 🟢 | 🔴（与闸 3 方向相反） | 是 |
| 备注 EVENT 关键陷阱（66–77） | 🟢（有报错原文与 KOR 实证） | 🟡 | 🔴（`ts_event_*` 清单与闸 8 矛盾） | 是 |
| §7 批量字段收割 + `dataset.id=`（78–88） | 🟢 | 🟢 | 🟢 | 否 |

| # | 位置 | 维度·级 | 问题 | 改进建议 |
|---|---|---|---|---|
| DF-01 | L4、L20、L36–61 | 逻辑·P3 | 标题/description 说“6 种方法”，正文有 6 法 + 2 个备注 + “7. 批量字段收割”，编号跳跃 | 章节重排：方法 1–6 / 陷阱 / 批量 |
| DF-02 | L33–34 | 情景·P1 | “运行这些模拟时用 Neutralization None、Decay 0、Test Period **P0Y0M**”——6 种方法每个字段各需 ≥1 次仿真，文中**没有成本提示**，也没说怎样用 multi-sim 合批（≥2 条）、结果是否计入战役统计；`P0Y0M` 与 ppa-mining 的 `P0D/P6Y` 写法不同 | 给“最小仿真集”（例如 1+3 合批）与成本；统一 testPeriod 写法 |
| DF-03 | L36–61 方法 5 | 逻辑·P2 | `ts_median(datafield, 1000)` 注为“5 年中位数”——1000 交易日≈4 年（标准窗口是 1008=4 年），窗口非标且换算错；**更根本的是 `ts_median` 本身在本账号是幽灵算子**（`platform_constraints.ghost_ops`；how-to-pass reference L69 已注“Never use `ts_median`：会使整批 multi-sim CANCELLED”），见 DF-08 | 先按 DF-08 替换算子（如 `ts_mean(datafield, 1008) > X` 度量“4 年典型值”），再校正窗口与文字 |
| DF-04 | L63–64、L84 | 边界·P1 | “VECTOR 字段应**直接**用于 rank/ts_*，**不要**包在 `vec_*` 里；`winsorize` 安全”——与全库相反：toolkit 闸 3“type==VECTOR 的字段最内层必须是 `vec_*`，否则 FAIL”、`--fix` 自动裹 `vec_avg`；RA 步 5“VECTOR 用 preflight（auto_fix_vector）”；D5“VECTOR 必须先 `vec_*` 聚合”；ppa-mining“VECTOR 数据集自动包 vec_avg”。照本文写会被闸 3 拦下 | 以平台/闸 3 为准改写；若确有例外（仅限某类字段），列出并给证据 |
| DF-05 | L71–76 | 逻辑·P2 | “EVENT 先用 `ts_event_*` **转换为 VECTOR**”——把 `ts_event_*` 的输出称为 VECTOR，与闸 3 对 VECTOR（需 `vec_*`）的含义冲突，读者无法判断转换后还要不要 `vec_*` | 术语校正（输出类型）并给一个完整示例 |
| DF-06 | L78–88 §7 | 情景·🟢 | “GET /data-fields 裸 `dataset=` 被静默忽略→必须 `dataset.id=`（KOR 2026-08-15 实测）”+ 4 步规避 + 实测说明——**症状→原因→规避**齐全 | 范式 |
| DF-07 | 全文 | 情景·P2 | 只讲“怎么测”，没有“测完怎么用”（覆盖%、频率→窗口选择、范围→预处理的**决策映射**），职责上交给特征工程但无链接 | 每法末加“→ 交 brain-data-feature-engineering 的哪一步” |
| DF-08 | L55–61（方法 5、6）、L71–76 | 边界·**P1** | **算子口径与库内清单/闸门不一致（上一轮评审 P0-1，至今未修）**：方法 5 用 `ts_median(datafield, 1000)`——`ts_median` 在 `platform_constraints.ghost_ops`（10 个之一），用了会使整批 multi-sim CANCELLED；方法 6 用 `scale_down(datafield)`，EVENT 段列 `ts_event_sum/count/mean(field, N)`——二者**都不在** `known_ops`（103 个已验证算子）内，而 gate.py 闸8 又**强制** EVENT 字段使用 `ts_event_*`（8 个：avg/count/max/min/rank/sum/zscore/delta）：**清单说“未验证”，闸门说“必须用”**，agent 无法判断哪个对；并自称“经过验证的 6 法” | 以 `get_operators` 实测裁决：可用 → 补入 `known_ops`；不可用 → 同步改 SKILL 与闸8。`ts_median` 一律替换（`ts_mean`/`ts_std_dev`）；加机械检查“SKILL 中出现的算子名 ∈ known_ops ∪ 显式标为反例” |

<a id="s14"></a>
### 14. `brain-dataset-mining-experience`（L6 · 64 行）

**总评**：全库**边界写得最好的 skill 之一**：“只读台账、不回测、不判死”“单次失败只约束『字段搭配＋结构＋设置』，不能据此判死整个字段或数据集”“不拼接不同候选的最好指标”“IS 不是 OS、冷门不保证低相关、空失败列表≠全通过”，每条都是可执行的**不许做**。更新方法给了“先干跑、再实跑、按文件内容而非任务状态核验”的完整两步，并交代了自动块/人工块（`BEGIN/END WQB DATASET EVIDENCE`）的边界。问题集中在**仍要求写已废止的 `s6_verdict_*`**、人工复盘区没有可依据的文件模板，以及少量悬空指针。

| 阶段（行号） | 书写逻辑 | 职责划分 | 边界界定 | 需情景规范？ |
|---|---|---|---|---|
| frontmatter + 职责边界（1–15） | 🟢 | 🟢 | 🟢 | 否 |
| 主流程连接（22–27） | 🟡 | 🟢 | 🔴（`s6_verdict_*`） | 否 |
| 更新方法（29–53） | 🟢 | 🟢 | 🟢 | 是（核验的期望值） |
| 人工机制复盘（55–61） | 🟡（5 条长句） | 🟢 | 🟡（悬空指针） | **是（文件模板）** |
| 收尾（63–64） | 🟡 | 🟢 | 🔴（`s6_verdict_*`） | 否 |

| # | 位置 | 维度·级 | 问题 | 改进建议 |
|---|---|---|---|---|
| ME-01 | L2–6 | 边界·P3 | frontmatter 缺 `allowed-tools`，description 无“当…时使用”触发句（只有用途描述）；其余 skill 均有 | 补触发句：“每波 S6 收尾、或下一轮选字段前读经验时使用” |
| ME-02 | L24、L63 | 边界·P1 | “先收回回测、完成 S4 与 **`s6_verdict_<wave>` 回写**，再调用本技能”“结构化结论仍经 wqb-db 回写 **`s6_verdict_*`**／registry”——RA 已于 2026-09-28 声明 `wave_results.verdict` 为唯一结论源、**不再双写 `s6_verdict_<wave>`**；本 skill 是第 4 处仍教旧键的文档（另有 ra-campaign-prompt 验收、decision-table D8、ledger-schema） | 改为“完成 `upsert_wave_result`（含 verdict）与 S4 后调用” |
| ME-03 | L27 | 边界·🟢 | “单次失败只约束『字段搭配＋结构＋设置』，不能据此判死整个字段或数据集；推翻旧经验须提供新证据”——**判死粒度**的最清晰表述 | 提升为全库“判死判据表”的总则（见 RD-26） |
| ME-04 | L39–41 | 情景·🟢/P3 | 干跑→实跑→`workflow_task_status`；省略 wave/dataset 的语义、D1 战役传 `--delay 1`——具体、可执行；RA 步 9 写 `str($DELAY)` 与此处“D1 始终传 1”表述不同 | 统一为“传本战役 delay” |
| ME-05 | L51–53 | 情景·P2 | “核对仓库文件的波次和行数，不能只凭任务 succeeded 判定”——好规则，但没给**期望值**（应出现哪些波号、哪一块被替换） | 给一个示例输出与核对命令 |
| ME-06 | L55–61 | 情景·P1 | 人工复盘 5 条都是分号串起的长句，且没有提供**自动生成文件的骨架**（各级标题、块外应写在何处），读者不知道“块外”的具体位置；“一次纠错复验的边界见主流程链接的选波清单”——本文件没有这条链接 | 把生成文件模板（含 BEGIN/END 标记、人工区标题）贴进来或链接 `reports/dataset_experience/README.md`；补 `selection-plan.md` 链接 |
| ME-07 | L58–59 | 边界·🟢 | “缺失写未核实，不拼接不同候选最好指标”“有测量缺陷的比较不写成机制有效/无效的证据”——反 cherry-pick 护栏 | 推广到 hypothesis-first、how-to-pass 等 |
| ME-08 | L60 | 边界·P2 | `research_leads_w<W>` 是一个新 ledger 键，未登记于 ledger-schema | 纳入“ledger key 目录” |
| ME-09 | 机械检查 §D | 情景·P3 | `tools/dataset_experience.py --waves` 被检查器判“flag 缺失”是**误报**（flag 在 `src/wqb/research/dataset_experience.py`），但说明“兼容入口只是薄壳”应在文中写明 | 一句话点明 |

---

<a id="s15"></a>
### 15. `brain-data-feature-engineering`（L1 · 330 行 + reference 493 + examples 244 + OUTPUT_TEMPLATE 325；另有 make-some-gem 下的嵌套副本）

**总评**：字段透明度分档（第 0 步）与 S0 白名单越界即停（第 1 步）是**有判据、有理由**的好规则；第 6 步的 ledger schema 也具体。但**同一文件对“产物能否注入 GEM”给出三个互相矛盾的答案**，且 `source` 示例值恰会让 GEM 忽略它；此外约 150 行是通用的“如何思考”式叙述与输出提纲，且与 `OUTPUT_TEMPLATE.md`（325 行）重复，另有一整套嵌套拷贝会漂移。

| 阶段（行号） | 书写逻辑 | 职责划分 | 边界界定 | 需情景规范？ |
|---|---|---|---|---|
| 定位修正引用块（24–29） | 🟢 | 🟡 | 🔴（与 L162/L228 冲突） | 是 |
| 职责边界 + 输入（33–55） | 🟡 | 🟡（含选集） | 🟡（universe 缺省） | 是 |
| 第 0 步 透明度分档（59–69） | 🟢 | 🟢 | 🟡（档位重叠） | 是 |
| 第 1 步 数据集发现（71–77） | 🟡 | 🟡 | 🟢（越白名单即停） | 否 |
| 第 2–4 步（79–155） | 🟡（泛化叙述） | 🟢 | 🟡（无规模上限） | **是（概念预算）** |
| 第 5 步 输出（157–226） | 🔴（三个“去向”矛盾） | 🔴（与 OUTPUT_TEMPLATE 重复） | 🔴 | 是 |
| 第 6 步 台账回写（228–254） | 🟡 | 🟢 | 🔴（`source` 示例、状态机过时） | **是** |
| 原则/示例/质量保证（256–328） | 🔴（通用口号、虚构示例） | 🟡 | 🟡（与分档冲突） | 是 |

| # | 位置 | 维度·级 | 问题 | 改进建议 |
|---|---|---|---|---|
| FE-01 | L24–29、L162、L228–254 | 边界·P1 | 三种说法：①定位修正（09-15）：节点产出是**确定性模板**、不再被 GEM 注入，agent **人工**完成并写 `source=manual` 才注入；②L162：本 ideas markdown 是 S2 GEM 的“**法定输入**”，编排器步 4 **必须**传 `--ideas-file`；③RA 步 3：FE 产物**按需、仅人读、禁注入 GEM**。①与③大体一致，②与二者矛盾 | 只保留①，并在 L162 改为“**仅当 source=manual（agent 人工完成）时**可经 `--ideas-file` 注入；节点渲染产物不得注入”，与 RA 对齐 |
| FE-02 | L245 vs L24–29 | 边界·P1 | 第 6 步 ledger 示例里 `"source": "standalone"`；而 RA/GEM 规则是 `source ∈ {feature_engineering_node, standalone, standalone_v2}` **一律跳过注入**——agent 按示例写入的人工产物会被 GEM 忽略，直接使“法定输入”落空 | 示例改 `"source": "manual"`，并注明三种取值的含义 |
| FE-03 | L253 | 边界·P1 | “S1⇄S2 统一逻辑链”写：`s1_<ds>_d<delay>` 命中且 `ideas_md_path` 可读 → `--ideas-file` 注入——未按 source 区分，是 2026-09-15 前的状态机；另称“S3 五闸校验与 S6 回写均读此记录”，核对 `gate.py`：闸 2 读 typed catalog / legacy whitelist，不读 `s1_` 键 | 状态机按 source 分支；删“五闸读此记录”（或指出真正读它的代码） |
| FE-04 | L33–37、L71–77 | 职责·P2 | 边界说“不做选集/输入=S1 白名单”，第 1 步却包含“未提供 dataset_id 时基于元数据选择最相关的数据集”（选集属 S0/dataset-exploration）；输入以 category 为主，RA 的 S1 是按 (region,dataset) 逐集执行 | 删“自主选集”，无 dataset_id 时回 RA 步 2 |
| FE-05 | L54 | 边界·P2 | “universe 默认 `TOP3000`”对多数区域错误（KOR TOP600、EUR TOP2500…） | 缺省取 `config.REGIONS[region].default_universe` |
| FE-06 | L59–69 | 边界·P2 | 分档判据有数值（描述覆盖≥80% 且均值>5 词；<30%）和依据（103 个 s1 键的审计）——好；但三档均“满足其一”，`model*` 集若描述覆盖≥80% 同时满足透明与黑盒，**优先级未定** | 加“黑盒优先”之类的裁决序；给 1 个跨档示例 |
| FE-07 | L91–144 第 3 步 | 情景·P2 | 8 问 × 每字段 → 概念数无上限；RA 已实证“组合爆炸”（黑名单字段占 9.9% 却吃 49.4% 生成预算）；步 4 的 8 属性模板没有 GEM 需要的 **Implementation Example**，也没有“机制→1–2 字段→一个示例”的概念优先约束 | 定预算（每字段族 ≤N 概念、每概念 ≤2 字段）；步 4 增加“Implementation Example”栏 |
| FE-08 | L160 | 边界·P2 | 输出写到相对路径 `./output_report/…_ideas.md`（该目录是审计报告目录，与运行 CWD 有关），同时又写 ledger；“DB 唯一事实源”与文件产物的主从关系仅在 L230 一句带过 | 指定产物目录（gitignore 的运行目录）与主从关系 |
| FE-09 | L164–226 | 职责·P2 | 报告提纲（1–5 章、3.1–3.8）与 `OUTPUT_TEMPLATE.md`（325 行）内容重复，且提纲每项只是“度量××的概念”类空泛描述 | 只保留模板文件，SKILL 内一句指针 |
| FE-10 | L256–262、L296–309 | 逻辑·P3 | “本 skill 不应当：让用户思考/提供通用模板”与节点的实际行为（确定性模板）矛盾；原则 5 条为泛化口号 | 收缩为“人工完成时”的 3 条硬要求 |
| FE-11 | L264–294 | 情景·P3 | 示例数据集 `BEME`、字段 `book_value/market_cap/book_to_market` 疑为虚构（与“保持具体：引用真实字段名”自相矛盾）；未含窗口/表达式 | 换成 RA 白名单里的真实数据集与字段 id |
| FE-12 | L311–326 | 边界·P2 | 质量自查“**所有字段都被分析**”与第 0 步允许透明集**跳过 8 问**冲突；“新颖/避开传统思维陷阱”无法检验 | 验收改成可检项（字段画像覆盖率、每概念含字段 id/方向/边界、Implementation Example 数） |
| FE-13 | 目录 | 职责·P2 | `brain-make-some-gem/scripts/trailSomeAlphas/skills/` 下的 `brain-data-feature-engineering`、`brain-feature-implementation` 是 **GEM 引擎的“内嵌 legacy 兜底”**（`pipeline_paths._resolve_skill_dir`：env > `skill_roots` > 内嵌），约定“顶层是源、内嵌是派生物”，由 `tools/sync_gem_embedded_skill.py` 同步并由 `test_gem_skill_paths.py` 守护——**但守护只覆盖 FI 的 `SKILL.md`**；dfe 副本的 `reference.md`（Jaccard 0.82）、`OUTPUT_TEMPLATE.md`、`examples.md` 无守护，已出现漂移；副本目录内没有“GENERATED/勿手改”标记。**注意：这两份 SKILL.md 会被拼进 GEM 的 LLM prompt（dfe 322 行、FI 111 行），即它们同时是运行时输入，篇幅与自相矛盾直接进入生成质量** | 副本目录加 GENERATED 标记；守护扩到 dfe 全部文件；把“进入 prompt 的部分”与“给人读的说明”拆开（prompt 只装必要规则，省 token） |

<a id="s16"></a>
### 16. `brain-make-some-gem`（L2 · 165 行 + reference 64 + examples 30；scripts/ 含 headless_runner 与 trailSomeAlphas）

**定位**：S2 概念优先的表达式生成引擎（RA 步 4 的后端）。

**总评**：全库**结构最合格**的一份——有“职责边界 / 定位声明 / 上下游 / 标准调用 / 直接命令 / 产物契约 / 失败分支（7 行表）/ 反模式”，并留有事故教训（内嵌 dfe 的 SKILL.md 缺失致 322 行文档静默不进 prompt）与“看到 MISSING 立刻停下排查”的明确判据。**需要注意两件被低估的事实**：①它把两份 skill 文档（dfe 322 行、FI 111 行）**拼进 LLM prompt**，即那两个 SKILL.md 同时是**运行时代码**；②同目录 `reference.md` / `examples.md` 已严重落后于 SKILL.md（仍教旧产物路径和“以 run.py 为入口”）。

| 阶段（行号） | 书写逻辑 | 职责划分 | 边界界定 | 需情景规范？ |
|---|---|---|---|---|
| frontmatter + 职责边界（1–24） | 🟢 | 🟢 | 🟢 | 否 |
| 定位声明 + 上下游（28–42） | 🟢 | 🟢 | 🔴（门禁顺序写成三段） | 否 |
| 两种生成模式（44–55） | 🟡（一段含 4 主题） | 🟡 | 🟡 | 是 |
| 概念优先铁律 1–8（57–74） | 🟢 | 🟡（复述 RA） | 🔴（“补腿”、闸 6 契约） | 是 |
| 标准调用（76–87） | 🟢 | 🟢 | 🟡 | 是（返回值动作） |
| 直接命令（89–114） | 🟡 | 🟢 | 🟡（DB 入库缺一步） | 是 |
| 产物契约 + skill 目录解析（116–146） | 🟢 | 🟢 | 🟢 | 否 |
| 失败分支（148–158） | 🟢 | 🟢 | 🔴（缺 402；stage=S6） | **是** |
| 反模式（160–165） | 🟢 | 🟢 | 🟢 | 否 |
| reference.md / examples.md | 🔴 | 🟡 | 🔴（旧路径、入口倒置） | — |

| # | 位置 | 维度·级 | 问题 | 改进建议 |
|---|---|---|---|---|
| GM-01 | L20–24 | 边界·🟢/P3 | “`priors_snapshot_<region>` 只读消费，唯一写入方=assemble-priors；stale 只 WARN 不阻断，**不得据此认为‘已确认安全’**；刷新责任归步 9”——所有权与不可推断都写清；但“先提示重跑 assemble-priors 再开生成”未说**由谁提示**（agent 自己跑？提示用户？），RA 步 4 代码块本来每次都先跑一遍 | 明确“agent 在开生成前先跑一次”，与 RA 对齐 |
| GM-02 | L42 | 边界·P1 | 下游写成“`check_batch` 多样性守卫 → `check_expr_against_inspect` 体检硬门 → `wave_gate` 闸 1–5”三段串联——实际应调**一个入口** `wave_gate`（内含闸 6 与体检门）；`check_batch` 已非门禁（RA 步 5） | 改“调 `tools/wave_gate.py`（含闸 1–8、体检硬门、SEM、PF）” |
| GM-03 | L52–55 | 逻辑·P2 | 一段 ≈400 字含 4 个主题：`pipeline_mode` 透传、headless 缺省改 phased、ideas 注入规则（模板渲染 source 不注入）、预闸内容（quantile 归一 + 丢加权混合）+ 社区模板导出——预闸清单只有 RA 版的子集（缺 hump 命名参、bucket range、非法 group、窗口别名、每骨架封顶 12）；`kb_templates --emit-ideas` 产物的 `source` 取值未说，无法判断是否会被注入 | 拆 3 条；预闸清单只在一处维护（建议 GEM 侧，RA 引用）；写明 emit-ideas 的 source |
| GM-04 | L60、L84–85 | 边界·P2 | 铁律 2“必须带 priors（默认 DB 快照，fail-closed）；`priors_file` 仅作覆盖”**正确**，印证 RA 硬约束 #2“必须带 `priors_file`”已过期（RA-47）；L84“ideas_file 默认从 S1 ledger 自动注入”与 L53 “模板渲染 source 不再自动注入”并存，缺“仅 source∈{s2_nested, manual}”限定 | RA 改；此处补限定 |
| GM-05 | L61 | 边界·P2 | “只消费 `wins`(≤6)/`dead_ends`(≤12) 两键，其余忽略”与 RA（`methodology`/`signal_family_rules` 作 region_context 注入、`gate_priors` 的 by_operator_count/by_field_family 进 prompt）矛盾 | 以代码为准改一处 |
| GM-06 | L64–67 | 边界·P1 | 铁律 6 允许“第二腿之后每加一腿，须点名它修哪个闸（sub_universe/2Y/CW）”——即**用补腿修不达标的信号**，而 decision-table D3/RA“路线 A”明令“不得靠增删腿数修不达标信号”，D2 又写“CW→补腿”：**三份文档三种态度** | 统一：补腿仅限“条件/分组/对偶价差”且不得以修闸为由；GEM 铁律 6 改写并加反例 |
| GM-07 | L68–72 | 边界·P1 | 铁律 7 声明“旧规则强制每波 ≥1 个 Logical 算子已废除；算子多样性应是语义多样性的结果”——但 toolkit 闸 6 的契约仍可强制 `required_operators` 与 `event_gated` 骨架配额（gate-rules：KOR 契约“注入 2 条 + event_gated 1 + group 1”），sim-alphas 的 `diversity_enhancer` 仍按**算子熵/覆盖率**默认改写表达式。生成端与闸门端的多样性哲学不同步，可能出现“按新规则生成的批被闸 6 拒” | 三处对齐：以语义多样性为准，闸 6 契约里的算子配额降为可选；enhancer 默认改 `auto`/`never` |
| GM-08 | L73–74 | 边界·🟢 | “Expected Exposure 会被验证：`risk_neutralized_sharpe`≈0/为负而 raw 高 ⇒ **该概念**就是暴露本身，判 dead_end 且禁止调参”——明确粒度=**概念**（RA 步 7 的两处表述没有这一点，RA-83） | RA 引用此处 |
| GM-09 | L87 | 情景·P2 | 返回 `mode_b_required`（EXPECTED_BLOCK>0 时为真）后**做什么**没写；`quality_estimation` 与 wave_gate 的 qp 预估（曾把修复批 S2.1 预估为 0.65 而 BLOCK）关系未提 | 写“为真→步 7 走 Mode B，且该批不占探针额度”一类动作 |
| GM-10 | L89–102 | 边界·P1 | “直接命令”只写生成，**没有写入 DB 的一步**（产物契约又说“未验证 DB 有表达式，不得声称步 4 成功”）；`--dry-run` 只验证命令构建，未提“不验证 LLM 可达性”（RA 已实证 402 时干跑假绿）；`cd scripts/headless_runner` + 裸 `python` 与“$WQ_PY”规则不符；LLM 供应商/密钥（README 写 `MOONSHOT_API_KEY`、端点、模型环境变量）在 SKILL.md 里**完全没出现** | 补“落库命令/节点”；补“干跑不验证 LLM”；补 LLM 通道前置（哪个密钥、缺失/余额不足的症状） |
| GM-11 | L104–112 | 情景·🟢/P3 | “看实时生成过程”：给了两种方式、**代价**（关窗口=杀任务，phased 无断点）与**默认选择**（`--watch`）——范式；但含 Windows 控制台专有细节（`DETACHED_PROCESS|CREATE_NO_WINDOW`） | 标注 Windows 专有 |
| GM-12 | L116–131 | 边界·🟢 | 三段查找路径 + “旧位勿再用于新跑” + “文件不是真相源”；迁移事故（16 个产物文件混入仓库）交代清楚。含行号引用 `gem.py:1219`（会漂移） | 行号改函数名 |
| GM-13 | L133–146 | 情景·🟢 | skill 目录解析顺序（env > skill_roots > 内嵌）、打印行 `[skill-doc] … OK/MISSING`、“看到 MISSING/`embedded:legacy` 立刻停下”、历史坑与守护测试——**症状→判据→动作**完整 | 范式；补“这两份 SKILL.md 是运行时 prompt，改动需过 `test_gem_skill_paths`”的维护警示 |
| GM-14 | L148–158 | 情景·P1 | 失败表缺**最具迷惑性的两种**：LLM 余额不足 `402 Insufficient Balance`（表现为“no meta.json within 90s”、干跑假绿，RA 步 4 引言里才有）、LLM 通道不可达；“无 priors 快照→`stage="S6"`”与 RA 用 `stage="S2"` 不一致；“候选不足→enhance/扩组合”与选波清单“不得补参数变体凑数”冲突 | 增两行；stage 统一（stage 与路由无关，统一写 S2）；候选不足→“显式扩容/分波/换集” |
| GM-15 | `reference.md`（64）、`examples.md`（30） | 边界·P1 | 仍把**旧深嵌套路径**（`scripts/trailSomeAlphas/skills/brain-feature-implementation/data/...`）当**产物与核对位置**；SKILL.md 已声明它们是“历史兜底、勿再用于新跑”；`examples.md` “The skill should use `scripts/headless_runner/run.py` as entry”与 SKILL“标准入口=`workflow_gem`”倒置；Known Failure Modes 只有 3 条（SKILL 有 7 条）；英文与中文混用 | 与 SKILL 对齐或并入 SKILL；核对位置改 `data/gem_runs/…` 与 DB |

---

<a id="s17"></a>
### 17. `brain-feature-implementation`（L2 · 119 行）

**总评**：模板语法规则有**正反例**（`{gro} / {pe}` ✔，`{anl15_gr_12_m_gro} / {pe}` ✘，`${gro}` ✘）和“脚本只接受 `--template` 与 `--dataset`”，很具体。但它同时扮演两个身份：①给人/agent 的手动流程；②**被拼进 GEM LLM prompt 的文本**。第二身份下，“用 TaskCreate 建计划”“`ls -R` 找脚本”“cd 到目录再 python”这些工具化步骤对只输出文本/JSON 的 LLM 毫无意义，甚至误导（同步工具注释里就记过曾引用不存在的 `manage_todo_list`）。

| 阶段（行号） | 书写逻辑 | 职责划分 | 边界界定 | 需情景规范？ |
|---|---|---|---|---|
| frontmatter + 职责边界 + 描述（1–37） | 🟡（行为规则塞进“描述”） | 🟡 | 🔴（description 触发会被直接命中） | 否 |
| 前置准备 config.json（39–52） | 🟡 | 🟢 | 🟡（明文凭据；又一种来源） | 是 |
| 操作步骤 1–5（53–113） | 🟡 | 🟡 | 🔴（`TaskCreate` 宿主专有；产出文件 ≠ DB 真相源；脚本无确定路径） | **是** |
| 脚本依赖（115–119） | 🟢 | 🟢 | 🟡（两份 `implement_idea.py`） | 否 |

| # | 位置 | 维度·级 | 问题 | 改进建议 |
|---|---|---|---|---|
| FI-01 | L4 vs L23 | 边界·P1 | description 的触发语“当用户提供 idea 文档、**要求生成 alpha 表达式**或下载数据集时使用”会让它被直接触发，而边界句与 RA 反模式都禁止把它当主链入口 | description 改“仅供 GEM 引擎内部/维护者查阅模板语法”，并从触发列表撤出 |
| FI-02 | L34–37、L39–51 | 边界·P2 | “skill 层不直接调用 MCP”，数据下载经 `ace_lib` 用 **skill 目录内 `config.json` 的明文邮箱/口令**——又一种凭据来源（全库已有 ≥8 种，见综合篇）；`.gitignore` 的 `**/config.json` 与 sync 同口径可防提交，但文档没提 | 引用统一的“凭据来源”规范；声明 agent 不得读取/回显 config.json |
| FI-03 | L63–74 | 边界·P2 | “定位脚本：`ls -R` / `Get-ChildItem -Recurse` 找 `fetch_dataset.py`，通常在 …/scripts”——**没有给出确定路径**；存在两份 `implement_idea.py`（顶层与 GEM 内嵌，scripts 故意不同步）；命令 `cd <PATH> && python …` 相对路径 + 裸 python | 写死路径（顶层 vs 内嵌各适用于何时）；`& $WQ_PY` |
| FI-04 | L76–82 | 边界·P1 | “使用 `TaskCreate` 工具创建计划”——宿主专有工具；GEM 把本文件拼进 LLM prompt 时该指令无意义 | 分两份：prompt 版只留模板语法规则（≤60 行）；手动流程版另放 |
| FI-05 | L104–113 | 边界·P1 | 步骤 5 产出 `final_expressions.json` 并“向用户报告文件路径”，而边界头与全库均规定该文件**不是真相源**、DB 才是；手动流程没有入库步骤 | 加入库一步或声明“本流程不可单独使用” |
| FI-06 | L28–31 | 逻辑·P3 | “描述”节里塞了行为规则（占位符只绑定一次、GROUP 不自动扩展数值变体） | 规则挪到“模板语法”节 |

---

<a id="s18"></a>
### 18. `alpha-expression-verifier`（L2 · 75 行）

**总评**：**边界最干净的 skill 之一**（只验语法：括号、算子元数、函数参数；不判字段是否存在；战役级预检另属 gate.py）。问题在示例：**“校验非法表达式”的示例其实是合法表达式**。

| 阶段（行号） | 书写逻辑 | 职责划分 | 边界界定 | 需情景规范？ |
|---|---|---|---|---|
| frontmatter + 职责边界（1–39） | 🟢 | 🟢 | 🟢 | 否 |
| 使用方法（40–55） | 🟡（路径两种写法） | 🟢 | 🟡（`$WQ_VALIDATOR_DIR` 缺省值未给） | 是 |
| 解读结果（56–61） | 🟢 | 🟢 | 🟡（无失败分支：脚本缺失/依赖缺失/errors 类型） | 是 |
| 示例（62–73） | 🔴（“非法示例”其实合法） | 🟢 | 🟡 | **是** |
| 边界说明（74–75） | 🟡（“5 闸/1363 行”会漂移） | 🟢 | 🟢（明确写出本层做不到什么） | 否 |

| # | 位置 | 维度·级 | 问题 | 改进建议 |
|---|---|---|---|---|
| EV-01 | L69–72 | 情景·P1 | 标题“校验非法表达式”，示例 `rank(close, 5)`，注释却说“rank(x, n) 是合法的（n 为窗口），此例仅演示运行位置”——**没有任何真正非法的示例、也没有期望的 JSON 输出**；且平台文档里 `rank` 第二参是 `rate`（排序精度）而非窗口（需核对） | 给 2 个真实非法例（括号不匹配、元数错误）+ 预期输出 `{"valid": false, "errors": [...]}`；核对 rank 说明 |
| EV-02 | L44–54 | 边界·P2 | 路径两种写法（`$WQ_VALIDATOR_DIR/verify_expr.py` 与示例里的 `scripts/verify_expr.py`），`$WQ_VALIDATOR_DIR` 缺省值未给（“主路径（Windows）”）；含“早期文档引用 `.claude` 或裸名错误”的史注 | 只留一种写法与缺省值；史注删 |
| EV-03 | L38 | 边界·🟢 | `densify()` 可接收原生 GROUP 分组轴，“本层无法确认平台类型；输出仍是分组键，不能交给 `rank()` 等数值参数”——明确写出**本层做不到什么** | 范式 |
| EV-04 | L75 | 边界·P3 | “gate.py（**5 闸**）”（实为 8 闸+闸 0）、“validator.py（1363 行巨石）”行数会漂移；“不要改 validator.py”是变更纪律，宜放 AGENTS.md | 更新/移出 |
| EV-05 | 全文 | 情景·P2 | 无失败分支：脚本找不到、依赖缺失、`errors` 各类型的含义与处理 | 补“常见错误 → 含义 → 修法” |

---

<a id="s19"></a>
### 19. `brain-inspect-raw-template-create-setting`（L3 · 99 行）

**总评**：现状是**“删了一半的旧流程”**：顶部说明写“人工设置决策环节已删除、现仅两个职能”，而职责边界仍写“产出设置计划”，运行步骤 4 仍要求“停止并交还 AI 选定设置组合”；“DB 单轨”铁律旁边，输出与下游仍是 `alpha_list.json`。可选字段默认值（`nanhandling OFF`、`maxtrade OFF`）与战役 settings（ON）不同，会**静默改变回测口径**。

| 阶段（行号） | 书写逻辑 | 职责划分 | 边界界定 | 需情景规范？ |
|---|---|---|---|---|
| 头部（1–23） | 🔴 | 🔴 | 🔴（DB 单轨 vs alpha_list.json） | 是 |
| 职责边界 + 衔接（27–43） | 🔴 | 🔴（描述已删除的职能） | 🔴 | 是 |
| 确定性流程 + 凭据（45–58） | 🟡 | 🟡 | 🔴（3 种凭据、默认值冲突） | 是 |
| 运行步骤（60–99） | 🟡 | 🟡 | 🔴 | 是 |

| # | 位置 | 维度·级 | 问题 | 改进建议 |
|---|---|---|---|---|
| IR-01 | L4 | 边界·P2 | description 442 字，含“不要用于增强模板”——“增强模板”“raw template”在全库其它处没有定义；“创建 alpha 列表”触发与 sim-alphas 重叠 | 定义两词或删；触发限定 |
| IR-02 | L14 vs L42–43、L80、L99 | 边界·P1 | 铁律：`alpha_list.json` 等**不得当交接真相源、Agent 禁止 Write**；而本 skill 的输出与下游明写“`alpha_list.json` 交 sim-alphas 批量回测”，并由脚本追加写该文件。（同一段铁律被原样复制进 wq-backtest-monitor、sim-alphas，各自的流程仍以 JSON 交接） | 交接以 expressions 表为准，`alpha_list.json` 仅作脚本内部中间件并声明不作交接 |
| IR-03 | L23、L29、L49、L80、L99 | 逻辑·P1 | 设置决策有三种口径：blockquote“人工设置决策环节已删除，仅两个职能”；职责边界“产出**设置计划**（universe/中性化/decay/truncation/maxTrade）”；运行步骤 4“**停止并交还 AI**：读 idea_context + settings_candidates，**选定设置组合**后手动调 build_alpha_list（多组则重复）” | 边界与步骤按 blockquote 重写；设置一律来自 `settings.json`/profile/`--set` |
| IR-04 | L41–43 | 职责·P2 | “上游 = GEM 产出的 `*_idea_*.json`”，但 GEM 节点已直接把表达式落 `expressions` 表；`build_alpha_list.py` 直写同一张表 = **第二条入库通道**（有重复入库风险）；RA 步 6 称“设置展开用本 skill（`--from-db`）”，而 `--from-db` 是 pipeline 的参数 | 写清何时走本通道（仅对**外部/手写** idea JSON），与 GEM 节点入库互斥 |
| IR-05 | L53–58 | 边界·P1 | 凭据来源再增 3 种：`BRAIN_USERNAME/BRAIN_EMAIL`+`BRAIN_PASSWORD`、skill 内 `config.json`、`~/secrets/platform-brain.json`；与 sim-alphas（`BRAIN_EMAIL/BRAIN_PASSWORD`）、concurrency/toolkit（`WQ_USERNAME/WQ_PASSWORD`）**变量名互不相同** | 见综合篇“凭据来源单一化” |
| IR-06 | L62–71 | 边界·P2 | “先 `cd "path/to/…"`”是占位；产物落在 skill 目录下的 `processed_templates/<filename>/`（skill 树内写文件，GEM 已因此吃过“16 个产物混入仓库”的亏）；示例文件名 `fundamental28_GLB_1_idea_…json` 不存在 | 产物落到运行目录；示例用占位 |
| IR-07 | L96–98 | 边界·P1 | 可选字段默认值：`nanhandling`(**OFF**)、`maxtrade`(**OFF**)、`testperiod`(P0Y0M0D)；而战役 `settings.json` 与 ppa-mining 用 `nanHandling ON`、`maxTrade ON`；漏传即用脚本默认——**与战役口径静默不同**；testPeriod 全库 4 种写法（`P0D`/`P0Y0M`/`P0Y0M0D`/`P6Y`） | 默认值取自战役 `settings.json`；统一 testPeriod 写法 |
| IR-08 | L49 | 边界·P2 | “中性化必须始终选一个有效选项（**不能为 None**）”，而 datafield-exploration 要求字段探测用“**Neutralization: None**” | 各自标适用场景（生产回测 vs 字段探测） |

---

<a id="s20"></a>
### 20. `brain-sim-alphas-in-batch-and-track`（L3 · 210 行）

**总评**：“入口/引擎”关系与“并发纪律唯一权威在 wqb-concurrency”都写得明确，`simulation_status.csv` 的定位澄清也到位。但**推荐路径（MCP 节点）没有配套的运行规则，而详细规则全是给已废弃的文件模式**；多样性增强默认改写表达式，与 GEM/RA 的“保持经济方向、不补变体凑数”相冲。

| 阶段（行号） | 书写逻辑 | 职责划分 | 边界界定 | 需情景规范？ |
|---|---|---|---|---|
| frontmatter + 铁律 + 边界（1–48） | 🟡 | 🟡（“唯一执行者”不成立） | 🟡 | 是 |
| 输入/输出、凭据（50–73） | 🟢 | 🟢 | 🟡（凭据变量名） | 否 |
| 标准命令（75–108） | 🟡 | 🟢 | 🟡（示例数字易被抄） | 是 |
| 长任务执行规则 + 续跑（110–126） | 🔴（文件模式当主线） | 🟡 | 🔴（3 分钟 vs 60 分钟） | **是（MCP 路径规则）** |
| 多样性增强（128–154） | 🟡 | 🟡 | 🔴（默认改写表达式） | 是 |
| 战役引擎能力（156–184） | 🟡 | 🔴（第 3 份映射表） | 🔴（文件产物） | 否 |
| 输出契约 + 工具化（186–210） | 🟡 | 🟢 | 🟡 | 否 |

| # | 位置 | 维度·级 | 问题 | 改进建议 |
|---|---|---|---|---|
| SA-01 | L4 | 边界·P1 | description 触发含“**批量提交 alpha**”，而边界写“不提交 alpha、`--submit`=提交**回测**”；“调并发/配额闸/战役 pipeline”分别与 wqb-concurrency、toolkit 重叠 | 触发词改“批量回测/发起回测”；并发与配额触发让给对应 skill |
| SA-02 | L33、L41、L43–46 | 职责·P1 | “S3 **唯一**执行者/单一入口”，RA 步 6 却列出三个入口（`workflow_batch_track`、本 skill、toolkit）并让 agent 自选；边界“不做门禁”，引擎能力表又把 `gate.py` 闸 1–5 列为本 skill 调用的能力；“写 `settings.json`”与 inspect（不写）、RA 一键战役（写回）三处说法不一；上游写成“inspect 产出的 alpha_list”，边界写“步 5 已过闸批次” | 写入口选用表；区分“调用”与“实现”；`settings.json` 写入方唯一化 |
| SA-03 | L110–120 | 情景·P1 | “长任务执行规则”整节以**文件模式**为主线：启动前预检 `alpha_list.json` 存在、“进度真相源=输出 CSV”、“失败=进程停止 且 CSV 无进展≥**3 分钟**”；而上文声明文件模式已废弃、CSV 非真相源，推荐路径是 `workflow_batch_track` + `workflow_task_status`（无 CSV）；toolkit 的 STALLED 阈值是 **60 分钟**。两个“失败判据”相差 20 倍 | 分“MCP 路径 / 兼容 CLI 路径”两套规则；统一 stall 判据并写清适用层 |
| SA-04 | L93–108 | 情景·P3 | 兼容命令示例用保守值（`--batch-size 3 --concurrency 2`），⚠ 警告放在代码**之后**；裸 `python` 与“$WQ_PY”规则不符 | 警告前置；示例用占位 |
| SA-05 | L128–154 | 边界·P1 | 多样性增强**默认 `always`**：按“算子熵<2.0/覆盖率<50%/新颖度<80%/结构相似度>70%”自动做结构变异、**算子替换（ts_rank→ts_scale）**、事件门控、分组包裹——即缺省就改写表达式；GEM 铁律写“显式 ideas 的表达式保持经济方向，不得通过替换外层算子强制制造多样性；算子多样性应是语义多样性的结果”；RA“不得补参数变体凑数”。阈值无依据 | 缺省改 `never`（或 `auto` 且只标注不改写）；与 GEM 哲学对齐 |
| SA-06 | L160–173 | 职责·P2 | 阶段→脚本→产物表是同一映射的**第 3 份**（toolkit §6、RA Artifact 表、本表），且产物写成旧文件名（`reference/…_dataset_ranking.json`、`candidates/*.json`、`reviews/…json`），与 DB 单轨冲突；“所有产出落到 reference/candidates/results/reviews”同理 | 只保留一份并以 DB 产物为准 |
| SA-07 | L179 | 逻辑·P3 | “禁止**五**数据集同时首探”——数字 5 与七槽不符（RA 反模式写“七槽全裸探针”） | 改为规则而非数字 |
| SA-08 | L69–73 | 边界·P2 | 凭据变量名 `BRAIN_EMAIL/BRAIN_PASSWORD` 与 inspect（`BRAIN_USERNAME`…）、concurrency/toolkit（`WQ_USERNAME/WQ_PASSWORD`）不一致 | 统一 |

---

<a id="s21"></a>
### 21. `wqb-concurrency`（L3 · 119 行）

**总评**：**关键教训写得最有价值**——“信号量必须包住整条 run_backtest 而非仅 POST”“孤儿模拟无法查询也无法取消、TaskStop 只会制造更多孤儿”“三类卡住根因表”“`/users/self` 不含限额字段别再查”。问题在**三处**：①职责边界说“只管并发”，description 与 §8 却把“台账闭环、写波结论、台账驱动选波”也收进来；②§2–§4 的 Python 代码建议与“禁止手写脚本/requests”相冲；③同文件两个“安全包络”（≤6 与 ≤7）。

| 阶段（行号） | 书写逻辑 | 职责划分 | 边界界定 | 需情景规范？ |
|---|---|---|---|---|
| frontmatter + 边界（1–35） | 🟡 | 🔴（含台账闭环） | 🟡 | 是 |
| §1 测定 C（37–47） | 🟡 | 🟢 | 🔴（≤6 与 ≤7） | 是 |
| §2–§3 信号量与线程（49–70） | 🟡 | 🔴（教人手写 runner） | 🔴 | 是 |
| §4 孤儿模拟（72–82） | 🟢 | 🟢 | 🟢 | 否 |
| §5 根因表（84–90） | 🟢 | 🟢 | 🟢 | 否 |
| §6–§7 凭据、参数化退避（92–98） | 🟡 | 🟡 | 🟡 | 否 |
| §8 七槽 SOP 0–6（100–119） | 🟡 | 🔴（台账/复盘越界） | 🔴 | 是 |

| # | 位置 | 维度·级 | 问题 | 改进建议 |
|---|---|---|---|---|
| WC-01 | L4 | 边界·P2 | description 329 字，含“每次挖掘必须执行”“下一波设计强制以台账决策为输入”这类**要求**；“提交成功数极低”歧义（实指 429 下的模拟接受数） | 只写触发场景；“提交”改“发起” |
| WC-02 | L21–25 vs §8 步 0/4/6 | 职责·P1 | 边界：“不发起回测、不改表达式、不提交”，只管并发；§8 却包含台账同步门（`check_ledger_sync`）、写波结论（`wave upsert`/`ledger set`）、台账驱动选波、“每 10 波做全量多样性评估并据此优化 skills”——这些属 RA 步 1/9 与 toolkit §9（RA D10 又写“每 15 轮”） | 只留 §8 步 1–3、5 的并发纪律；台账部分引用 RA 步 9 |
| WC-03 | L39 vs L119 | 边界·P1 | 演进注记：“配置基准以新模型为准（**瞬时 ≤6 安全**、批间 ≥45s）”；§8 末：“7 批 multisim 仅耗 7 令牌、**瞬时 ≤7 安全包络内**”——同文件两个包络；“批间 ≥45s”在 SOP 中无体现 | 统一一个数与适用条件；SOP 写批间间隔规则 |
| WC-04 | L49–70 | 边界·P1 | §2 给出 `self._sub_sem = threading.Semaphore(C)` 的实现代码、§3 教“线程=C+1”，例子仍用 **C=5**（“3 线程×2 数据集=6”）——教读者自己写 runner，而 AGENTS/RA 规定“禁止手写 requests/一次性脚本”、七槽已由 `pipeline.py` 内部锁定；数字 5 已过期 | 标“**给引擎维护者**”；或删代码，仅留原则；数字改引用 config |
| WC-05 | L79 | 边界·P2 | 429 退避 `wait=min(20+attempt*8,45)s，最多 ~40 次`——全库第 3 套退避（toolkit：5s×2×5 次；BrainApiClient 自带）；RA 步 6 却写“429→降并发、批≤5”，而**本 skill（并发权威）只要求“短退避重试、绝不因限流丢弃候选”**，从未要求降并发 | 一个退避口径；RA 与本 skill 对齐 |
| WC-06 | L94 | 边界·P2 | 凭据加载“`load_dotenv(...abspath(__file__), ".env")`”是给脚本作者的代码，对 agent 应写“**不读取 .env**（AGENTS.md）” | 分受众 |
| WC-07 | L112–114 | 边界·P1 | SOP 步 3“`lookINTO_SimError_message` → children → `get_alpha_details` 逐 ID”是旧 3 段链；RA 已用 `harvest_multisim_alphas`（一键收 multisim 全部详情，18 次调用压成 2 次）取代 | 更新为现行工具 |
| WC-08 | L113 | 情景·P2 | “`validate_fields=false` 避免预检超时”与 RA 步 3“新字段先 `create_multi_simulation(validate_fields=true)` 验活幽灵字段”并存，未说哪次用哪个 | 写情景：验活探针=true，正式批=false |
| WC-09 | L105–111 | 边界·P2 | 台账同步门（`check_ledger_sync`）是“执行层硬门”，但 RA 步 6 正文没有它（只在 decision-table D8 与本文）；“创建批次文件时同步在台账登记批次表”仍是文件时代口径 | 并入 RA 步 6 或废止；改 DB 口径 |
| WC-10 | L115 | 逻辑·P2 | 步 4 是一个 ≈600 字段落含 6 条规则（写 DB、快照勿手改、禁 runs/ 散件、未写不得提交下一波、判死当场写、每 10 波评估） | 拆成有序清单 |
| WC-11 | L119 | 边界·P1 | “提交配额与回测并行槽位是**两个独立机制**”——引擎里 `pipeline.stage_submit_poll` 在**提交配额耗尽时中止回测发起**（`--force` 才继续），两者被耦合（TK-27） | 改代码使回测发起不受提交配额约束，或改文档如实说明 |
| WC-12 | L37–47 | 情景·🟢 | 测 C 的 4 步给出**易踩坑**（`language` 必须 FASTEXPR，错了是 400 而非 429）、判据（首批连续 201 数=C）、“429 报文不含数字”与“/users/self 不含限额字段”等反面知识 | 范式 |

<a id="s22"></a>
### 22. `wq-brain-alpha-optimization-v1`（L4 · 197 行 + reference 401 + examples 87 + arXiv 手册 548 + references/structural-interaction-forms 121）

**定位**：现有 alpha 的两模式优化：Mode B（想法层）→ Mode A（参数层）+ “卡闸→组合腿救援”。

**总评**：**全库把“辅助腿如何入场”写得最完整的一份**——`structural-interaction-forms.md` 给了 F1–F6 六族形态、每族对应的卡点（boost_dim）、算子白名单核验（103 个）与“禁加权混合、禁权重网格”的硬边界；“弹药查询：卡点→boost_dim 映射”是清晰的场景表；资格线（`mode_b_qualification`）前置、“未达线一律判死不救援”是可执行的止损。问题在三处：①description 与 RA 步 5b 对**“把 PROD 压到 0.7 以下”的可行性说法相反**；②Mode A 的“结果追加写文本文件”与 DB 单轨冲突，且变体**绕过 wave_gate**；③“70%/30% 精力”无法度量。

| 阶段（行号） | 书写逻辑 | 职责划分 | 边界界定 | 需情景规范？ |
|---|---|---|---|---|
| frontmatter + 边界 + 模式调度（1–37） | 🟡 | 🟢 | 🔴（PROD 承诺；“精力”） | 是 |
| Mode B 步 B1–B5（39–71） | 🟡（时间预算面向人） | 🟢 | 🟡 | 是 |
| Mode A 硬规则/工作流/校验（73–104） | 🟡 | 🟡 | 🔴（文本文件、算子≤8、绕闸） | 是 |
| 三灯分级 + 陷阱（106–117） | 🟡 | 🟡 | 🟡 | 否 |
| prod_corr 反馈循环（119–126） | 🟡 | 🟢 | 🔴（第 4 套 prod 墙学说） | **是** |
| 组合腿救援（128–165） | 🟢 | 🟢 | 🟡（“一句话”判据主观） | 是（入场三式） |
| 过拟合测试 + 衔接 + 预期产出（167–198） | 🟡 | 🔴（与 robustness 重复） | 🔴（“权威”、换手区间） | 是 |

| # | 位置 | 维度·级 | 问题 | 改进建议 |
|---|---|---|---|---|
| OP-01 | L4 | 边界·P1 | description 承诺“**把 PROD 相关性压到 0.7 以下**”；RA 步 5b 明令“家族首探 prod ≥0.7 → 记 dead_end 换机制，**不做任何去相关变体**（bucket/门控/平滑实证都破不了 prod 墙）”，D0 又说“换数据集”，D14 说“三条破墙路径”——本 skill 的“反馈循环”是第 4 种（换概念→组合腿救援→换字段→换数据集） | 统一为**一张 prod 墙处置表**（RA-69），本 skill 只引用并写“适用前提：已过资格线”；description 去掉承诺 |
| OP-02 | L27、L36、L70、L195 | 逻辑·P1 | “Mode B 70% / Mode A 30% 精力”在 RA 步 7、D11、ra-campaign-prompt 2.3 也被引用，含义各异（时间？模拟配额？变体条数？）；同一 skill 里又有“每周期 30–60 分钟”“想法池 3–5 周期/alpha”“>10 种结构无果”三个上限，彼此关系未说 | 定义“精力”=某个可度量量（如单 alpha 的模拟条数占比），或删；三个上限合并为一个止损规则 |
| OP-03 | L39–66 | 情景·P3 | B1–B5 每步给“5–10 min”式时间预算——这是给人的节奏，agent 无意义；B1 两行都是 `get_alpha_details` | 换成“调用数/条数预算”；去重 |
| OP-04 | L55 | 边界·P2 | arXiv 概念检索用 `scripts/arxiv_api.py --concepts --llm`，走 **DeepSeek** 概念层，凭证在 `scripts/.arxiv_llm.env`（skill 目录内 .env）——又一个 LLM 供应商与密钥文件；同名脚本在 `brain-explain-alphas` 里还有一份 | 声明数据外发与密钥位置；脚本去重（共享一份） |
| OP-05 | L61 | 逻辑·P3 | “旧文写的 `create_multiSim` 不是真实工具名（2026-09-26 审计）”为文档改错史 | 删 |
| OP-06 | L85、L97 | 边界·P1 | 硬规则 7 与工作流 8：回测后“立即以 UTF-8 追加模式把本批结果写入**指定的文本文件**”——与 DB 单轨（回测结果已由 harvest 入 `backtest_results`）冲突；“指定”由谁指定未说 | 改“确认 `backtest_results` 已入库；迭代日志写 ledger/报告” |
| OP-07 | L82、L195 | 边界·P2 | “operatorCount>8 的候选无效”“平台是最终裁判”——**算子≤8 是 PPA 的限制**；REGULAR 无此上限（GEM 过闸样本 p90=12 个算子），robustness 又把 8 当“复杂度警告/REJECT” | 标注适用类型；REGULAR 改用 GEM 复杂度预算 |
| OP-08 | L83 | 逻辑·P2 | “Stage A 阶段禁止纯微调”——Stage A 在全库只在 toolkit 探针里有定义（Stage A/B 探针），此处未定义 | 定义或改名 |
| OP-09 | L88–104 | 边界·P1 | Mode A/B 的变体只经“本地 `validate_expression` + verifier”就直接 `create_multi_simulation`，**没有经过 `wave_gate`**（幽灵算子 / 闸 5 加权与等权混合 / 闸 2b / SEM / 闸 PF）；而 RA 步 7 对同类批量变体器明确“产出入库后仍走本步全部闸”；`validate_expression`“当前项目暴露时使用”的条件式措辞也无法执行 | Mode A/B 变体统一先过 `wave_gate --batch-type repair`；写明本地校验的具体入口 |
| OP-10 | L115 | 逻辑·P3 | “陷阱”里含 SuperAlpha 构造，与优化陷阱无关；EVENT/`winsorize` 条重复 datafield-exploration | 删/指针 |
| OP-11 | L128–143 | 情景·🟢 | 🟢 仅就**写法**而言：触发线 → 动作 → 卡点→`boost_dim` 映射五行，**触发条件→动作**清晰；**内容已过期**——资格线的数值与“未达线一律判死”已被 `mode_b_config` 的主闸 + 旁路 + 判死线取代（见 OP-18 / HP-15） | 范式；`min_sharpe=0.5`（此处）与 RA 步 7 的 `min_sharpe=1.0` 不一致，需统一 |
| OP-12 | L145–156 + `structural-interaction-forms.md` | 边界·P1 | 构造纪律明确（主腿冻结、辅助腿 ≤2 且取自 salvage_pool、禁加权/权重网格、溯源标记）——**是 RA-90 缺的“辅助腿入场”答案**。但合规判据仍是“成品须能用一句话说清‘单一经济信号’”“价差/比率必须能写成一句话”，与 RA-89 同样主观；F1 允许 `subtract(rank(主), rank(辅))`，与等权 leg-add 只差符号；F6 把 `hump` 列为合规算子，而 D6/ppa-mining 写“hump 已废弃/勿用” | 增可检判据（辅助腿必须以条件/分组/残差化进入，或同一经济量对偶两侧+声明 Expected Exposure）；hump 状态全库统一；RA 步 7 直接引用 F1–F6 |
| OP-13 | L164–165 | 情景·P3 | 说明 salvage_pool 由 `review_wave.py --write-ledger` 自动入池（S≥1.0 且 prod<0.5）；RA 用 `min_sharpe=1.0`、本处 `min_sharpe=0.5` | 统一 |
| OP-14 | L167–175 | 职责·P2 | “过拟合与稳健性测试”四项与 `brain-alpha-robustness` Phase C 大量重复但**阈值不同**（子宇宙：此处 sharpe>1、fitness>0.7、margin>5bp；robustness：TOP1000/500/200 全部 Sharpe≥1.0）；并称 robustness 为“外部 Agent 技能”（robustness 称 repair 为“同目录外部技能”），实际都在本仓库 | 只保留一处；术语改“同库 L4” |
| OP-15 | L181 | 边界·P1 | “`tools/submit_verdict.py`（提交层**权威**判定）”——第 5 处“权威”字样，与 RA L681“提交层唯一权威不是 submit_verdict”冲突 | 见 RA-03 |
| OP-16 | L191–197 | 边界·P1 | 预期产出把 Turnover 写成“1%–40%（内部目标 ≤40%）”；全库换手区间现有：平台 1–70%（config）、内部 5–20%（config）、D0 “5–20%”与“5–30%”并存、IND 0.40 限、此处 1–40% | 引用 `config.GATES`，删自定阈值 |
| OP-17 | L189 | 逻辑·P2 | “持续迭代直到至少一个候选满足全部条件”是无终止条件的循环（与 3–5 周期/10 种结构上限矛盾） | 改“满足或触上限→判死回写” |
| OP-18 | L130–133 | 边界·P1 | “触发线：本 alpha 必须已过 `mode_b_qualification` 资格线（sharpe≥1.25 且 fitness≥0.8，以区域 `thresholds.json` 为准）……**未达资格线的弱信号候选一律判死，禁止救援**”——资格线模型已被 `workflow/mode_b_config.py`（2026-09-09）改成“主闸 + 旁路 A–E + 判死线”（区域 ledger_kv > 全局 ledger_kv `GLOBAL/mode_b_qualification` > thresholds.json `$ref` > 内置默认），“一律判死”与旁路（robust/prod-only/margin/turnover/2Y 强）及“2Y≥1.2 永不判死”冲突；how-to-pass L122–125、RA L793 同款旧说法（见 HP-15） | 改为引用 `mode_b_config` 判定表；“未达线”改“落入判死线（2Y<1.2 且 S、F 均低于主闸）才判死，其余走旁路对应的 `mode_b_action`” |

---

<a id="s23"></a>
### 23. `brain-alpha-robustness`（L4 · 148 行 + references/techniques.md 53 行）

**总评**：**全库判据最可检的 skill**——Phase C 是 11 行 PASS/CONDITIONAL/REJECT 数值表，B.0“失败计数门”给了明确的 do/don’t 清单（“不要跑 Phase B/C；不要跑 check_correlation；不要设 alpha 属性；逐条枚举 name/result/limit/value”），“近窗制度”附用户指令与理由。但存在四个结构性问题：①它声明自己是“**必经闸**”，**却没有任何代码消费其判定**（结果只写 markdown 与 jsonl）；②Phase A 让每次运行先做论坛缓存刷新，并允许“发现新规则则以新规则为准”——**闸门阈值可被当日论坛内容改写**；③Phase E 保留了“**提交探测协议**”（逐个提交读 prodCorr）；④验证清单里藏着最重要的操作知识。

| 阶段（行号） | 书写逻辑 | 职责划分 | 边界界定 | 需情景规范？ |
|---|---|---|---|---|
| 头部引用块 + 边界 + 衔接（12–41） | 🟡（史注置顶） | 🟡 | 🔴（judge 的地位） | 是 |
| Phase A 论坛缓存（43–66） | 🔴（手工流程与工具并列） | 🔴（知识刷新混入闸门） | 🔴（可改写阈值） | 是 |
| Phase B 归因（68–87） | 🟢 | 🟢 | 🟡（路径过期、PENDING） | 是 |
| Phase C 判定表（89–114） | 🟢 | 🟢 | 🟡（与平台公式/GEM 不符） | 否 |
| Phase D 回写（116–121） | 🟡 | 🟡 | 🔴（仅写文件/事件，无 DB） | 是 |
| Phase E PPA/幽灵/探测（123–131） | 🔴（编号缺 2） | 🔴（台账维护/提交探测） | 🔴 | **是** |
| 设计边界 + 验证清单（133–149） | 🟡 | 🟡 | 🔴（关键知识藏在清单里） | **是** |

| # | 位置 | 维度·级 | 问题 | 改进建议 |
|---|---|---|---|---|
| RB-01 | L12–19 | 逻辑·P2 | 两个引用块置于 H1 之前，后一块（“权威性”）是关于**本 skill 副本谁为真相源**的元说明（旧说法已删），与稳健性无关，应在 INDEX | 移出 |
| RB-02 | L14 vs L35、L112 | 边界·P1 | 本文自相矛盾：头部“`brain-alpha-judge` = **S5 唯一提交评审入口**（双闸评审），先过本闸再进 judge”；衔接协议与 Phase C 写“PASS → `submit_verdict`（提交层权威）→ `brain-alpha-judge`（**可选参考评审**）”。judge 到底是“唯一入口”还是“可选参考”？（RA：judge 仅参考层；optimization：judge 仅参考） | 统一为“judge=参考层”，删“唯一” |
| RB-03 | L25、L34、L116–121 | 边界·P1 | 声明“S4→S5 **必经**闸”，但**没有任何代码读取该判定**（全仓 grep：只有 `judge.py` 注释提到；`submit_verdict`/提交节点不检查）；Phase D 只写 `tracking/YYYY-MM-DD_robustness.md` 与 `data/events/<日期>.jsonl`（文件态，DB 单轨里没有落点） | 把 PASS/CONDITIONAL/REJECT 与失败检查码写入 DB（如 `robustness_<alpha_id>` ledger 键），`submit_verdict`/`workflow_submit_alpha` 前置校验其存在且为 PASS |
| RB-04 | L45–66 | 职责·P1 | Phase A 要求每次运行先 `forum_cache_builder --status`，过期则手工重拉 5 个关键词包（≥30 帖）并去重写回缓存——同一段先说“统一走 `--ensure`”，又逐步教手工做法（重复）；**且缓存路径在工具里写死为 `~/.qoder-cn/skills/brain-alpha-robustness`**（某一宿主的安装位），其它宿主/云环境不存在；把“知识刷新”放进每个候选的闸门流程，职责不清 | 拆出独立的“刷新技术台账”任务（定时/手动），闸门只读 `references/techniques.md`；缓存路径改仓库内 |
| RB-05 | L64 | 边界·P1 | “若刷新发现下方核对表之外的新规则，**以新规则为准**（在会话日志记录）”——闸门阈值可被当日论坛内容改写：同一候选在不同日期可得不同判定，不可复现、无审批 | 新规则只能作为“提案”写入 `references/techniques.md`，经审核后才进 Phase C 表 |
| RB-06 | L55、L142 | 边界·P2 | 步骤仍写“先经 MCP `authenticate`”（需邮箱/口令）——与 AGENTS.md 凭据红线冲突（同 NM-14/FB-10） | 改“认证由服务端完成，失败即停止并请用户处理” |
| RB-07 | L72 | 边界·P1 | B.0：“Failed RA/PPA 非零 → **立即 REJECT**、无 CONDITIONAL 通道”；RA 步 8：非零 → **回步 7 修复**。同一情形一处“拒绝”一处“修复再来”；口径只认 `result` 非 PASS/PENDING，**不处理 PENDING**（检查未算完时计数可为 0，RF-03） | 统一：非零→REJECT 并转 repair 的明确条件；PENDING→等待 |
| RB-08 | L74 | 边界·P1 | B.0a 从 `tracking/field_inspect_<region>.json` 取体检结果——RA 的体检包路径是 `tracking/mining/field_inspect_<region 小写>_<dataset>.json`（按数据集），此处路径已过期 | 对齐 |
| RB-09 | L77–81 | 情景·🟢/P3 | 近窗制度（用户指令 2026-06-20，理由：要求 10 年全强会杀活信号）+ 计算口径 + 全历史指标仅作软标记——**判据与理由并举**；“sharpe > ~0.3”“用户 2Y 线”含糊 | 给数值与来源 |
| RB-10 | L97–110 | 边界·P2 | 判定表个别行与他处不符：①“Sub-universe 全部 ≥1.0（TOP1000/500/200）”固定了子宇宙档，而平台 LOW_SUB_UNIVERSE_SHARPE 是**相对公式**（≥0.75×√(子宇宙/全宇宙)×Sharpe，how-to-pass），且 KOR/IND 的全宇宙本身就≤TOP600/TOP500；②“算子 8=REJECT/复杂度警告”与 GEM 样本（p90=12 个算子仍过闸）矛盾；③“Margin ≥5bp”与 `config` 内部线 10bp 不同；④“经济可解释性：一句话可写”主观 | 改引用平台公式与 `config.GATES`；算子数按类型（REGULAR/PPA）分列；主观项给判例 |
| RB-11 | L120 | 情景·P2 | REJECT 后要求调用 `wqb.search.failure_memory.record(category, dataset, universe, paradigm, shape_bucket)` 并用 `validator._shape_signature`（私有函数）——需要写 Python，与“禁止一次性脚本”冲突，且没有 MCP/CLI 入口 | 提供工具入口（MCP 或 CLI）；否则改写库 |
| RB-12 | L127–131 | 逻辑·P3 | Phase E 编号 1,3,4,5,6（**缺 2**） | 补/重排 |
| RB-13 | L129 | 边界·P2 | “提交前用 `set_alpha_properties` 预置描述 + `tags=["PowerPoolSelected"]` + `color=GREEN`”与本节第 1 条“打标签重试无效、合法 PPA 只能走 web UI”并存，未说标签在 web UI 流程里是否仍需要 | 澄清用途 |
| RB-14 | L130 | 边界·P1 | “幽灵提交识别：台账记 ACTIVE 但平台 404 → **修正台账为 PHANTOM**”——`PHANTOM` 不是代码中存在的状态；且 2026-09-28 N35 之后，`alphas` 的合并写入对 `ACTIVE/SUBMITTED/DECOMMISSIONED` **不回退**（`_SUBMITTED_STATES`），若按此指令写 `status=PHANTOM` 会被静默忽略；这段“台账维护”也不属于稳健性 | 定义 `PHANTOM` 的落点（如 ledger 标记，而非覆盖 `alphas.status`）；或移入 backtest-monitor/submit |
| RB-15 | L131 | 边界·P1 | “**提交探测协议**：选 5 个最大化多样样本，逐个提交+轮询 `/check` 读 prodCorr；5 个全 FAIL → 整族不可提交”——提交即真实动作（若通过即 ACTIVE、不可撤销）；RA 已规定“确认前禁止 `workflow_submit_alpha`/`submit_batch`”、prod 用 `check_correlation`。此协议是 2026-08 的旧做法，与 RC-01（prod-corr-avoidance 的 POST 探针）同源 | 删除；改用 `check_correlation(production)` 的串行泳道 |
| RB-16 | L135–138 | 逻辑·P3 | “判定阈值可通过 skill 参数放宽”——skill 没有参数机制；阈值来源“2026-04-22 论坛共识” | 写清放宽的入口（用户指令→台账留痕） |
| RB-17 | L144–146 | 情景·P1 | 验证清单第 2 条藏着**最重要的操作知识**：`check_correlation` 阻塞轮询、依赖 Redis（“本环境不可用”）易“等死”；可靠取法是 15s 间隔轮询 `GET /alphas/{id}/correlations/prod`（空体=平台在算，`max` 才是判定值），勿高频 `refresh=true`。同时与 `prod-corr-avoidance.md §7`（`check_correlation` 内置 30s 轮询、**Redis 7 天缓存**）互相矛盾；而“直接轮询 REST 端点”在“禁止手写 requests”下缺少合规工具 | 抽成正文“prod 相关性取数”小节；**Redis 一项已核对代码**：Redis 只是可选缓存（`brain_mixin_transport.py`：无 Redis 功能不受影响，相关性锁回落为进程内 fail-fast 锁），真正的“等死”来自 `_poll_production_correlation` 每 30 s 轮询、最长 3600 s，以及同账号单并发（第二个请求立即返回 `correlation_busy`）——详见 HP-11；给合规入口（MCP 工具 / `tools/…`） |

<a id="s24"></a>
### 24. `brain-how-to-pass-alpha-test`（L4 · SKILL.md 132 行 + reference.md 202 行 + references/two-year-sharpe-playbook.md 61 行）

**定位**：只读地回答“提交测试各项的阈值是多少、为什么没过、往哪个方向改”，并在 FAIL 后把候选分流到 optimization-v1。

**总评**：这是全库**证据链写得最好的一批段落所在**——§4 的 CONCENTRATED_WEIGHT（症状 IS 仅 WARNING → 根因“瞬时离散计数信号” → 4 个只改一个自变量的对照 → “参数层全无效”的反例清单 → 一条行动规则）是标准的因果写法；`two-year-sharpe-playbook.md` 是全库最好的**决策树式**文档（先看逐年形态 → 三条轴按成本递增 → 有数值的判死规则 + KOR risk71 反例）。问题集中在三处：①**本 skill 自称“只读”，却含“判死回写”“提交纪律”两条执行性规则，且“FAIL 回流纪律”所引用的资格线模型已被代码（`workflow/mode_b_config.py`，2026-09-09）改成“主闸 + 5 旁路 + 判死线”，文中仍是“达标/未达标”两分法，会误杀旁路 A–E 的候选**；②§6 把 SELF 与 PROD 混写，并把 `check_correlation` 的失败原因写错（Redis 只是可选缓存；真正的“等死”是 30 s×120 次的阻塞轮询与账号级单并发）；③阈值只有“平台默认值”一列，不含本库更严的内部闸（Sharpe 1.58 / turnover 5–20% / margin 10bp），18 个 `RA_CHECK_NAMES` 里本 skill 只覆盖约 8 个。

| 阶段（行号） | 书写逻辑 | 职责划分 | 边界界定 | 需情景规范？ |
|---|---|---|---|---|
| frontmatter + 职责边界 + 概述（1–33） | 🟡 | 🔴（只读 vs 判死回写） | 🔴 | 是 |
| §1 Fitness（35–43） | 🟡 | 🟡（配额读取不属于此） | 🔴（配额靠 submit 响应） | 是（数值例） |
| §2 Sharpe（45–53） | 🟡 | 🟢 | 🟡（只列平台线） | 是 |
| §3 Turnover（55–60） | 🟡 | 🟢 | 🟡（只有 1 条建议） | 是 |
| §4 Weight / CW（62–91） | 🟡（先建议后撤回） | 🟡（重述 RA 规则） | 🟢（因果链）/🔴（证据表可复制） | 是（适用范围） |
| §5 Sub-universe（93–99） | 🟡 | 🟢 | 🟡 | **是（数值例）** |
| §6 Self-Correlation（101–112） | 🔴（SELF/PROD 混写） | 🔴 | 🔴（Redis 说法、10% 豁免缺失） | **是** |
| 通用建议（114–117） | 🟡 | 🟢 | 🔴（USA 专属 + ATOM） | 是 |
| 衔接协议 + FAIL 回流纪律（119–128） | 🟡 | 🔴 | 🔴（资格线过期、判死粒度） | **是** |
| LOW_2Y / IS_LADDER + playbook（130–132；61 行） | 🟢 | 🟢 | 🟡（判死范围、窗口） | 是 |
| reference.md（202 行） | 🟡（英文译稿 + 社区轶事） | 🟡（63 行想法层通识） | 🔴（与 SKILL 冲突处） | 是 |

| # | 位置 | 维度·级 | 问题 | 改进建议 |
|---|---|---|---|---|
| HP-01 | L1–10、L20–24、L73、L122–127 | 职责·P1 | description 与职责边界自称“**只读**查阈值、解释为何不过闸；不产生表达式、不回测、不改候选”，正文却含两条执行性规则：L73“提交纪律：先看 IS 阶段该闸状态，WARNING 就别提”，L122–127“FAIL 回流纪律（强制）”——把候选分流到 optimization-v1，或“判死（dead_end 回写＋wave 台账 closed）”。判死回写是**写台账、终止候选**，不是只读；且未指定谁在何时用哪个工具写 | 拆成两层：本 skill 只输出“诊断 → 建议路径”（只读）；分流与判死回写归 RA 步 5/5b（`seal_dead_end` 流程）。或把边界改写为“只读 + 给出分流建议，不执行写入” |
| HP-02 | L35–53（§1–§3） | 边界·P1 | 阈值只有“平台默认值”一列（Fitness D1>1、Sharpe D1>1.25、Turnover 1–70%）。本库**实际闸线更严**：`GATES_INTERNAL` Sharpe 1.58 / Fitness 1.0 / turnover (5%,20%) / margin 10bp；`LOW_2Y_SHARPE` 1.58、`IS_LADDER` FAIL 线 1.59。读者按“Sharpe>1.25 即过”会把一批会被内部闸拦下的候选当成“已过”。且提交测试的真实来源是 `is.checks` 的 **18 个 `RA_CHECK_NAMES`**，本 skill 只覆盖 CONCENTRATED_WEIGHT / LOW_SHARPE / LOW_FITNESS / HIGH_TURNOVER / LOW_TURNOVER / LOW_SUB_UNIVERSE_SHARPE / SELF / PROD / LOW_2Y / IS_LADDER 约 8–10 个，`LOW_ROBUST_UNIVERSE_*`、`LOW_INVESTABILITY_CONSTRAINED_SHARPE`、`LOW_AFTER_COST_ILLIQUID_UNIVERSE_SHARPE`、`LOW_GLB_*`、`LOW_ASI_JPN_SHARPE`、`LOW_RETURNS` 无一句指引 | 文首放一张三列表：`check 名 → 平台线 → 内部线（config 键）→ 失败时读哪一节/哪个 skill`，`RA_CHECK_NAMES` 逐项登记（暂无对策的写“见 X”或“无经验”）；数字以 `config.py` 为唯一来源，正文不再手抄 |
| HP-03 | L43 | 边界·P1 | 一句话塞了三件事：检查工具（`get_alpha_details`）、**配额读取方式**、**工具移除史**：“提交配额从 submit 响应的 `REGULAR_SUBMISSION`/`SUPER_SUBMISSION` check 读，`get_submission_quota` 已于 2026-08-25 移除”。字面读法是“想读配额就要发起一次 submit”，而 submit 通过时即**真实提交，不可撤销**。且与 Fitness 无关，也不在本 skill 职责内 | 删除；配额读取归 worldquant-submit-alpha / next-move，并写明“读配额不得靠 POST submit；预检用 `workflow_submit_alpha(confirm_submit=False)`（默认值，仅预检 + 查状态，见 `tools_workflow.py:145`）” |
| HP-04 | L37–38、L47 | 情景·P2 | Fitness/Sharpe 的 Delay-0 / Delay-1 两列并列，但本战役几乎全是 D1，未说明“取哪一列、delay 从哪读（`settings.delay`）”。`Fitness = Sharpe·√(|Returns|/max(Turnover,0.125))` 只给了公式，没有推出**可操作结论**：turnover 低于 12.5% 后继续降换手**不再抬 Fitness**（分母被 floor）；playbook §1 的 `Fitness = Sharpe×√(505×margin)` 是同一关系的另一写法，两处未互指 | 补两个数值情景：①Sharpe 1.6、Returns 6%、Turnover 8% → Fitness≈1.11，与 12.5% 时相同（floor 生效）；②其余不变，Turnover 40%→25%：Fitness 0.62→0.78。并在两处互相指向 |
| HP-05 | L52、L99；reference L166 | 边界·P2 | “对流动性/非流动性股票分别做 decay”在 §2 与 §5 各出现一次而无表达式；reference L166 的示例 `ts_decay_linear(s,5)*rank(volume*close) + ts_decay_linear(s,10)*(1-rank(volume*close))` 是**权重相加**。实测（`gate.py`）：中缀写法 `_detect_weighted_mix_structural`/`_detect_equal_weight_leg_add` 均返回 False（放行），同构的函数式 `add(multiply(..),multiply(..))` 被 `_detect_equal_weight_leg_add` 拦下——**同一结构两种写法，判定相反**，文档又未表态允许与否 | 二选一：允许 → 在 `structural-interaction-forms.md` 登记为一族并让闸对两种写法一致放行；不允许 → 删示例，改用 `bucket`/group 写法表达“按流动性分档” |
| HP-06 | L62–68 | 逻辑·P2 | “改进建议：使用中性化…”后紧跟缩进注释“⚠ 2026-09-01 实测修正：中性化对本闸无效”——先给一条错建议再在注释里撤回，只读要点行的人会照做；同时该节标题“Weight Test”与平台检查名 `CONCENTRATED_WEIGHT` 只在标题括号里对应一次，§1–§3、§5、§6 均无平台检查名 | 要点行直接写“**中性化无效**”，并把有效手段（时间平滑）提到要点行；每节标题带平台检查名 |
| HP-07 | L70–91 | 边界·🟢+P2 | 🟢 因果链完整（见总评）。P2：①证据仅来自 **IND/TOP500 的分析师修正族**，小标题却是通用的“★ 实测要点”，未标适用范围与置信度（n=4，其中 2 例 FAIL）；②证据表前三行是已被闸5 拦截的加权混合表达式，作为“证据”保留但仍可被复制；③平滑窗口取 10，不在标准窗口白名单 `[1,5,22,66,252,504,1008,1260]`（`window_whitelist_enforce=false` 仅 warn；CLAUDE.md 要求非标窗口给出解释与实测）；④“末端再套 `rank(...)` **反而变 FAIL**”是反直觉结论，只有一句话、无案例 id | 加“适用范围 / 未验证范围”一行；证据表移 `references/`，正文只留第 4 行式样，窗口写 5 或 22（注明原实验为 10，需复验）；④补 1 个 alpha id |
| HP-08 | L73–74 | 职责·P2 | “IS 阶段 WARNING 的 alpha 提交后必 FAIL … WARNING 就别提”是**提交纪律**，且已有唯一实现：`config.check_counts_as_failed`（result 非 PASS/PENDING 即计失败，WARNING 计入）→ RA 以 `Failed RA==0` 放行。本节重述规则却不指向该定义，将来 PENDING/WARNING 语义一改就只改一处 | 改为“CW=WARNING 计入 Failed RA（见 `webdatascope-failed-gates.md`）”，删重述；“必 FAIL”改为“4 例中 2 例提交 FAIL”之类可核对表述 |
| HP-09 | L93–99（§5） | 情景·P2 | Sub-universe 只给公式与两条泛泛建议（“避免市值相关乘数”“分别 decay”），缺：①平台检查名 `LOW_SUB_UNIVERSE_SHARPE`；②数值例：TOP3000→子集 TOP1000，门槛 = 0.75×√(1000/3000)=0.433 倍 alpha Sharpe，Sharpe 1.6 时子集需 ≥0.69；③常见报错“Sub-universe Sharpe NaN is not above cutoff”（reference L17 才提到）的原因（子集覆盖不足）与对策（`ts_backfill`/`pasteurize`，reference L171 才提到） | 三项补进 §5；reference 对应段落改为指针 |
| HP-10 | L101–112（§6） | 职责·P1 | 标题 Self-Correlation，“要求”是 **SELF**（与自己已提交 alpha 的 PnL 相关 <0.7），“改进建议”整段讲的却是 **PROD**（`GET /alphas/{id}/correlations/prod`、`check_correlation`）。SELF（`SELF_CORRELATION`，自身已提交池）与 PROD（`PROD_CORRELATION`，平台生产池）是两个检查、两个池、两条取值路径；本地快筛只能算 SELF，且有结构性盲区（见 selfcorr-quick）。读者读完本节仍不知道“SELF 失败该怎么办” | 拆 §6a SELF / §6b PROD：各自写判据、取值途径、失败处置（SELF：换 idea / 降相关；PROD：RA 步 5b 首探规则、D14）；“对负相关 alpha 做变换”一句展开或删 |
| HP-11 | L107–111 | 边界·P1 | “`check_correlation`… **依赖 Redis（本环境不可用）→ 易「等死」**”与代码不符：Redis 只是**可选缓存**（`brain_mixin_transport.py` 注释“无 Redis 功能不受影响”；相关性锁在无 Redis 时回落为进程内 fail-fast 锁）。真正会“等死”的是 `_poll_production_correlation`：**每 30 s 轮询、最长 3600 s**（本文写“15s 间隔”，与代码 30 s 不符），且同账号只允许 1 个在飞（第二个立即返回 `correlation_busy`，本文完全没提）；结果缓存 7 天（有 Redis 时）。robustness RB-17 与 prod-corr-avoidance §7 各有一套不同的环境事实（后者称 Redis 缓存可用） | 环境事实只写一处（建议放 poll-and-quota.md）：“`check_correlation` = 阻塞 ≤60 min、账号级单并发（busy 立即返回）、有 Redis 才缓存”；给 `pending`/`correlation_busy`/命中缓存三种返回的处置表；“不要高频 `refresh=true`”给量化（每 alpha ≤1 次，间隔 ≥5 min） |
| HP-12 | L103；reference L175 | 边界·P1 | SKILL 版 SELF 判据只有“相关 <0.7”，漏掉平台的第二条通过路径——reference L175：“Or Sharpe at least 10% greater than correlated alphas”。selfcorr-quick L32/L68 写“self-corr>0.7 可直接判死”，`submit_queue.LIM` 也按单阈值 0.7：**三处口径 = 单阈值 / 单阈值 / 双路径**，“有价值的信息”被绕过 | 明确本库是否放弃该豁免路径（及理由）；若保留，给数值例：新 alpha Sharpe 1.9 vs 被相关 alpha 1.6 → 1.19× ≥1.10 通过；1.7 vs 1.6 → 1.06× 不通过；并在 selfcorr-quick / gate / submit_queue 中说明是否已实现 |
| HP-13 | L114–117 | 边界·P1 | “通用建议”三条都是 USA/D1 口径且与全库规范冲突：①“选择 TOP3000（USA, D1）”——KOR TOP600、EUR TOP2500 等；本 skill 的“FAIL 回流纪律”又自称“区域无关”；②“ATOM 原则：避免混合数据集”与 CLAUDE.md“优先单数据集 atom alpha”一致，却与 RA D0/D3/D11/D14 主动跨数据集混合冲突；③ATOM 的 2Y 门槛：reference L51 “Delay-1 >1”，playbook L3 `LOW_2Y_SHARPE` D1 限 **1.58**，`submit_queue.LIM two_year=1.58`——两个数字未说明分别适用于谁 | 删“TOP3000（USA）”；ATOM 写成“判据 + 阈值 + 适用对象”三行，并与 D3/D11 双数据集路线互相标注“何时可以违背 ATOM” |
| HP-14 | L119–121、L128 | 边界·P3 | 上游句同时写真相源（`backtest_results` 表）与文件回退（`simulation_status.csv`），未说何时用回退；“S4 链首步”用 S-label，全库另有“步 N”，同一阶段两套名；下游链 optimization-v1 → selfcorr-quick → explain-alphas **止于按需的 explain**，`brain-alpha-robustness`（S4→S5 必经闸）不在链上 | “回退仅 DB 不可用时，且只读”；链尾补 `→ brain-alpha-robustness → submit_verdict`，与 INDEX 流水线表对齐 |
| HP-15 | L122–125 | 边界·**P1** | **资格线模型已过期**：文中“对照区域 `thresholds.json` 的 `mode_b_qualification`（缺省 sharpe≥1.25 且 fitness≥0.8）：达标 → 强制进 optimization-v1；未达标 → 判死”。代码 `workflow/mode_b_config.py`（2026-09-09）已是**主闸 + 旁路 A–E + 判死线**，优先级：区域 ledger_kv（自适应）> 全局 ledger_kv `GLOBAL/mode_b_qualification` > 区域 thresholds.json（`$ref`）> 内置默认；判死线仅当“2Y<1.2 且 Sharpe、Fitness 均低于主闸”，且“2Y≥1.2 永不判死（走旁路 E）”。按本文“未达标即判死”会误杀五类旁路：A robust≥1.0 且 S≥0.8；B 仅 prod≥0.7；C margin≥5bp 且 S≥1.0；D returns 强但 turnover>0.7；E 2Y≥1.2 且 S≥0.8。optimization-v1 L130–133（“未达资格线一律判死”）与 RA L793 有同样的旧说法 | 全库三处改为引用 `mode_b_config` 的一张判定表（主闸 / 旁路 A–E / 判死线 / 对应 `mode_b_action`），不再各自抄“1.25/0.8”；并加一条测试：skills 中出现“未达标…判死”须能 grep 到 `bypass` 字样 |
| HP-16 | L125–127 | 职责·P1 | 第 1 条“未达标 → 判死（dead_end 回写 + wave 台账 closed，**勿送 near_pool**）”与第 2 条“快达标因子（S≥1.0 且 prod corr<0.5）**自动写入 `salvage_pool`**”内部矛盾：S∈(1.0,1.25) 的候选按第 1 条属“未达标”，按第 2 条又被 `review_wave.py --write-ledger` 自动入池（核对：`combo_candidate` 为 `S > combo_sharpe_min(1.0)` 且 `prod_corr < combo_prod_corr_max(0.5)` 且无 CW 硬失败；入池对象还含 **near 补充**，文中未提）。同时判死**粒度**不清：dead_end 是候选、家族还是波次？“wave 台账 closed”意味着一个候选未达线就关整波？与 dataset-mining-experience（“单次失败只约束字段搭配＋结构＋设置”）、RA 步 5b（`seal_dead_end` 前先做论坛核对，`found=true` 不得直接判死）均未对齐，且本文的判死路径**没有 forum_recon 步 = 绕过点** | 写成分级：候选级“记 dead_end(candidate)”；家族/波次级按 RA 步 5b（先 `seal_dead_end` + forum_recon）；第 2 条改为“入池对象 = combo 候选 + near 补充；阈值取 `thresholds.json` 的 `combo_*` 键，不手抄数字”；并说明与第 1 条的先后（先入池、再按资格线决定是否动用——动用侧才守资格线，见 RA L793） |
| HP-17 | L130–132；playbook 全文 | 边界·🟢+P2 | 🟢 playbook 的“先诊断 → 三轴按成本递增 → 有数值的判死规则 + 反例表 + ‘不再调参’的止损线”是全库最好的决策树。P2：①判死范围写“家族判死”，但证据全来自 **KOR 2022–23**（题材动量 + 2023-11 卖空禁令），跨区域应是“(region, family)”；②`rank_by_side` 不在 `known_ops`（103），“未解锁时替代”未说明“解锁”由谁/何时判定，也未指向 `get_operators` 实测；③窗口 250/50/500/240 不在白名单，无“解释或实测证据”记录；④“记 dead_end”未写调用路径（同 HP-16，须先 `seal_dead_end`/forum_recon）；⑤首段的 IS_LADDER 阶梯数字（2.38/2.22/…/1.59、turnover<30% 时 ×0.85）来源仅写“平台口径”，与 `config.py` 的常量未互链 | 判死范围改 (region, family)；`rank_by_side` 加“先 `get_operators` 确认”；窗口改白名单或加证据脚注；数字加 config 常量名 |
| HP-18 | reference L9–17、L24 | 边界·P2 | “Turnover and Drawdown … (e.g., low turnover **< 250%**)”与同文 L131 “1% < Turnover < 70%”直接冲突；“IS Sharpe > 1.25 for some universes”含糊；“102 operators”与 `platform_constraints` 的 103 不一致 | 删 L9–17 的“What Are Alpha Tests”综述，或逐项与 HP-02 的阈值表对齐 |
| HP-19 | reference L28–91 | 职责·P2 | 63 行“想法层通识”（idea sources、arXiv、ATOM、6 种字段探测、社区模板、官方例子）与提交测试阈值无关，且与 optimization-v1 Mode B、datafield-exploration 的“6 方法”重复；其中 L69 仍含 `scale_down`（不在 `known_ops`）、L78 `ts_sum(oth455_fact2 - oth455_fact1, 240)` 用中缀减法 + 非标窗口 240——**上一轮评审 P0-1（幽灵/未知算子）在此 reference 中仍存**（同一问题在 datafield-exploration SKILL 中也仍存） | 删除 L28–91，仅保留 §1–§6 阈值与技巧；如需保留想法层内容，移入 optimization-v1 的 references |
| HP-20 | reference L38–40、L198 | 边界·P1 | ①arxiv 脚本路径 `wq-brain-alpha-optimization-v1/scripts/arxiv_api.py` 无根前缀（checker 判 MISSING；库内同名脚本有 2 份：optimization-v1、explain-alphas）；②L198“Use tools like `workflow_submit_alpha` for pre-checks and submission”把“预检”与“提交”并列一句——该工具由 `confirm_submit`（默认 False）一个布尔位区分“只看”与“不可撤销提交”，文中未标出 | 脚本去重并写 `<SKILL_ROOT>` 相对路径；L198 明写“预检 `confirm_submit=False`（默认）；提交 `confirm_submit=True`，须用户明确授权” |
| HP-21 | 全文 | 情景·**是** | 缺一组“症状 → 根因 → 动作 → 验收”情景卡。建议 5 张：①Fitness 不过但 Sharpe 过（→ 看 turnover 是否 >25%，`ts_decay_linear`/`ts_mean`；turnover<12.5% 时不要再降）；②仅 IS_LADDER/2Y 不过（→ playbook §0 逐年形态三分）；③CW=WARNING（→ 事件类信号加时间平滑，不换中性化）；④Sub-universe 不过（→ 先抬整体 Sharpe，再考虑分档 decay）；⑤SELF≥0.7 vs PROD≥0.7（两条不同路：换 idea / 换概念，D14） | 按左列补情景卡（模板见 Part D §D.3.2） |

---

<a id="s25"></a>
### 25. `brain-alpha-repair`（L4 · SKILL.md 51 行 + references/repair-order.md 7 行）

**定位**：弱候选修复的“补充实证与执行纪律”（自称配方已上移 optimization-v1）。

**总评**：全文 51 行，**前 3 行引用块（约 60% 的信息量）在声明“配方已上移”，而被声明上移的内容在 optimization-v1 里经核对不存在**（“5 轴”“武器”“分布形态”“体检硬门复验”“幽灵算子清单”“相关性反馈循环”节名 **零命中**；B3 是“提出想法级改进”）。这是上一轮评审（2026-09-26）P0-6，至今未修——**配方既不在原处、也不在新处，INDEX.md L113 还把“5 轴旋转 + 6 武器去相关 + 体检硬门”当卖点**。留下的实质内容只有：failed-count 验收（1a，写得好）、GLB emotion 实证（2d，单段 400 字，且含危险表述）、USA universe 约定、两条对不上现存机制的“轨迹”要求。

| 阶段（行号） | 书写逻辑 | 职责划分 | 边界界定 | 需情景规范？ |
|---|---|---|---|---|
| frontmatter + 定位声明（1–14） | 🔴（声明占大半） | 🔴（“唯一入口”在别处） | 🔴（指向不存在的内容） | 是 |
| 职责边界 + 触发场景（18–28） | 🟡（三处重复） | 🟡（“配方查表”vs“不执行”） | 🟡 | 否 |
| 工作流 1 / 1a（30–33） | 🟢 | 🟡 | 🟢 | 是（判定 REGULAR/PPA） |
| 工作流 2 + 2a–2c（34–40） | 🔴 | 🔴 | 🔴 | **是** |
| 2d GLB 实证（41） | 🟡（单段） | 🔴 | 🔴（“提交探测零成本”） | **是** |
| 工作流 3–5（42–44） | 🟢 | 🟡 | 🔴（fingerprint / 轨迹） | 是 |
| 验证清单（46–51） | 🟢 | 🟢 | 🟡（第 4 条不可检） | 否 |

| # | 位置 | 维度·级 | 问题 | 改进建议 |
|---|---|---|---|---|
| RE-01 | L12–14、L37–40 | 逻辑·**P1** | 声明“5 轴旋转、降相关 6 武器、分布形态→修复方向映射、news/sentiment 专用方向、幽灵算子警告、体检硬门复验已于 2026-08-23 全部上移进 optimization-v1”。核对 `wq-brain-alpha-optimization-v1/SKILL.md` 与 `reference.md`：以上节名**均零命中**；引用的“Step B3”是“提出想法级改进”、“相关性反馈循环”节实名为 “prod_corr 反馈循环”。仅“体检硬门 5 条”留在本 skill 的 `references/repair-order.md` 第 6 点，“幽灵算子”在 `platform_constraints.json`（10 个）。全库检索“5 轴旋转”仅命中本文与 INDEX.md L113 | 二选一：(a) 把配方恢复进 optimization-v1（或新建 `references/repair-recipes.md`），并以其为唯一来源；(b) 承认已丢失，删声明与 INDEX 卖点。并加机械检查：**“声明已上移”的每个术语必须能在目标文件 grep 到** |
| RE-02 | L1–10、L18–28 | 职责·P2 | description、职责边界、“触发场景”三处重复同一列表；定位声明称“改进的唯一入口是 optimization-v1”，边界又称“只作配方参考、不直接执行”。description 里的触发词（候选修复/降换手/提覆盖/降相关）与 optimization-v1 的触发词**同批**，形成两个入口 | 退役 description 的触发词（改“仅在被 optimization-v1 引用时读取”），或把本 skill 并入 optimization-v1 的 references/ |
| RE-03 | L33（1a） | 边界·🟢+P2 | 🟢“REGULAR 修复成功的唯一标准是 `Failed RA == 0`；PPA 是 `Failed PPA == 0`；改善 Sharpe/Fitness/相关性但 failed count 非零仍是 reject，不得进入 `check_correlation` 或 `set_alpha_properties`”——目标、否定句、禁入下游三要素齐全，是全库“验收标准写法”的范本。P2：①“属于 REGULAR 或 PPA 挖掘链”如何判定（`classifications`？campaign 类型？）未写；②禁入下游用 MCP 工具名，robustness B.0、RA 用 `submit_verdict`——同一规则第三种写法 | 判定方法补一句；规则一处定义（`webdatascope-failed-gates.md`），此处只引用 |
| RE-04 | L34 | 边界·P2 | “选定任何算子前先确认它在当前 `get_operators` 返回里”——方向对，但成本高（全量返回），且已有机械守护（gate0 的 `known_ops`/`ghost_ops`：103/10）；“幽灵算子清单与替换表见 optimization-v1 Step B3”零命中（RE-01） | 指向 `platform_constraints.json`（唯一清单）与 gate0 |
| RE-05 | L35–37 | 逻辑·P2 | 三条 bullet：turnover 写“平台支持的降换手算子”（**无算子名**）、coverage 写“回填、重审向量聚合、复查 NaN 策略”（无参数）、correlation 整条是指针。一份“配方参考”里没有一个可复制的模板/参数区间/预期效果 | 每条至少 1 个模板 + 适用条件 + 预期效果区间（如 cr<0.4 → `ts_backfill(x,66)`；turnover 32% → `ts_decay_linear(x,5)`，附实测降幅） |
| RE-06 | L38 | 边界·P3 | 链接 `docs/reference/news_sentiment_playbook.md` 以仓库根为基准书写，而 markdown 相对链接应从 skill 目录解析（会落到 `Claude/skills/brain-alpha-repair/docs/…`，不存在；文件实在仓库根 `docs/reference/`） | 改 `../../../docs/reference/news_sentiment_playbook.md` |
| RE-07 | L41（2d） | 职责·P1 | 声明自己是该教训的“**唯一完整版**；ppa-mining §1.0.x 红灯行与其它文档只允许引用此处”。问题：①把一条“唯一权威”实证放在**自称已退役**的 skill 里；②其结论（“先 5 探针再全量”“换壳优于磨参数”“winner 周围 family 变 self wall → 更远 field-level move”）是跨 skill 规则，应属 optimization-v1（改进入口）与 RA 步 5b（prod 墙）；③单段约 400 字，事实（v53–v67、42 个 PASS_CHEAP、prodCorr 0.82–0.86、2 前缀×2 universe×多 neutralization）与结论（a–d）混写；④无适用范围（仅 GLB emotion 族） | 拆成“事实（表）/结论（4 条）/适用范围”三块；结论并入全库**唯一**的 prod 墙学说表（见跨 skill 综合 X-1） |
| RE-08 | L41 末句 | 边界·**P1** | “提交探测零成本（硬闸失败不消耗**周**额度），但浪费时间——先 5 个多样化探针（不同前缀×universe×neutralization）确认 prodCorr 再决定是否全量”。①“探针”若指 POST /submit：某探针恰好全部通过时就是**真实提交**（不可撤销、消耗额度）；②“周额度”是过期概念（现按 ET 日 + `REGULAR_SUBMISSION` 检查，见 HP-03）；③RA 步 5b 规定“家族首探 prod≥0.7 即换机制，**不做任何去相关变体**”，此处却要“先 5 个多样化探针”——同一情景两个相反动作 | 探针改为 `correlations/prod` 只读；写明探针数（家族首探 = 1）或解释为何 GLB emotion 需要 5；“周额度”改现行口径 |
| RE-09 | L42（3） | 边界·P2 | “USA REGULAR 修复保持 TOP3000 默认 universe；用其他 USA universe 时台账必须记录 TOP3000 失败原因与该 universe 回答的诊断问题”——区域专属规则埋在通用 skill；“台账必须记录”无键名/工具 | 移入 `regions/usa.md`，并给出台账键名 |
| RE-10 | L43–44、L50 | 边界·**P1** | “修复记录为新的轨迹步骤”“确认修复路径在 `trajectory_steps` 可见”：`trajectory_steps` 是 `wqb.memory.SimulationDB` 的表，`record_trajectory`/`add_trajectory_step` **除单测外无任何生产调用方**（全库检索），agent 既无法写、验收时也无从“看见”；“settings fingerprint”全库只在本 skill 出现，无生成者 | 换成现存机制（`alphas`/`backtest_results` 已含表达式哈希 + settings，可追溯），或登记 `repair_log` 键；否则删这两条（死要求会被静默忽略或被伪造） |
| RE-11 | L46–51 | 逻辑·P3 | 4 条验证项里，第 2 条（failed count 为零）机器可判，第 4 条“确认 §2d 的教训在修复决策时被读取”**无可检产物**（“读取”不留痕） | 改成可检项：“若 region=GLB 且信号族=emotion，台账有 ≥1 个 `correlations/prod` 读数” |
| RE-12 | 全文 | 情景·**是** | 应有三张情景卡：①降换手（turnover 32%、Sharpe 1.7 → 动作、预期、验收 `Failed RA==0`）；②覆盖不足（cr<0.4 → `ts_backfill` → 复验体检硬门）；③降相关（prod 0.78 → 按 RA 步 5b 首探即判，还是按 optimization-v1 换概念，给判据）。现在三者全部“见别处” | 按左列补情景卡（模板见 Part D §D.3.2） |

---

<a id="s26"></a>
### 26. `brain-explain-alphas`（L4 · SKILL.md 65 行 + reference.md 约 80 行 + scripts/arxiv_api.py）

**定位**：拆解并解释一个 alpha 表达式（数据理由/算子理由/收益来源），按需调用。

**总评**：六步模板（拆解 → 字段 → 算子 → 文档 → arXiv → 综合）和四段输出结构（思路 / 数据理由 / 算子理由 / 进一步启发）**清楚、可复现**，且首例是多层嵌套的真实表达式。问题在于：**声明的两个用途在正文里没有对应的程序**——“Mode B 换概念前查与既有 book 的概念重叠”需要“与 book 比较”，模板全部是“解释一个 alpha”；同时第 2 步的调用参数与真实 MCP 签名不符，且默认过滤 Sharpe<0 的字段（会让被解释 alpha 的字段“消失”）。

| 阶段（行号） | 书写逻辑 | 职责划分 | 边界界定 | 需情景规范？ |
|---|---|---|---|---|
| frontmatter + 职责边界（1–29） | 🟢 | 🟡 | 🟡 | 是 |
| 第 1 步 拆解（31–35） | 🟢 | 🟢 | 🟡 | 是 |
| 第 2 步 字段（37–41） | 🟡 | 🟢 | 🔴（参数名、静默过滤） | **是** |
| 第 3–4 步 算子/文档（43–47） | 🟡 | 🟢 | 🟡（附录不存在） | 否 |
| 第 5 步 arXiv（49–50） | 🟡 | 🟡 | 🔴（路径、外发、重复脚本） | 是 |
| 第 6 步 综合（52–57） | 🟢 | 🟢 | 🟡（无证据要求/落点） | **是** |
| 附录 + 衔接协议（59–65） | 🟡 | 🟡 | 🔴（`vec_mean`；链） | 是 |

| # | 位置 | 维度·级 | 问题 | 改进建议 |
|---|---|---|---|---|
| EX-01 | L22–24、L64 | 职责·**P1** | 边界与衔接协议称本 skill 服务于“Mode B 换概念前**先查概念重叠**”与“提交前对战略级候选做收益来源确认”。但 6 步模板全部是“解释一个 alpha”，**没有一步做“与既有 book 比较”**：无输入（book 从哪取？`alphas` 表 ACTIVE？）、无比较方法（字段集 Jaccard？概念标签？信号族指纹？）、无产物格式。声明的用途没有对应的程序，agent 只能自由发挥 | 补第 7 步“概念重叠检查”：输入 = 目标 alpha 的 (字段集, 算子骨架, 概念标签) 与 book 内 ACTIVE alpha 的同三元组；输出 = 重叠清单 + 建议（继续/换概念）。或删除该用途 |
| EX-02 | L39；reference L21 | 边界·**P1** | “必填/推荐参数：`instrument_type`（如 EQUITY）、region、delay、universe、data_type、search”——MCP `get_datafields` 的真实签名是 `(region, dataset_id, universe, delay=1, data_type="", search=None, filter_sharpe=True)`：**没有 `instrument_type`**（工具内部写死 EQUITY；机械检查 E 判 BAD-PARAM），`dataset_id` 无默认值（须显式传，可为 None）。按文调用会 `unexpected keyword` | 去 `instrument_type`；写明 `dataset_id` 必传（可 None）、`universe` 必传；区分“必填”与“推荐” |
| EX-03 | L38–41 | 情景·**P1** | 第 2 步“获取每个数据字段的详细信息”，但工具默认 `filter_sharpe=True`——**OS/IS Sharpe<0 的字段被静默过滤**。解释一个已有 alpha 时，其字段可能恰是 Sharpe<0（作者取了负号），按字段名搜索得“空”，agent 会误报“字段不存在/不可用”。reference L36 的“迭代检索”技巧没提这一开关 | 明写“解释既有 alpha 时 `filter_sharpe=False`；`search` 用完整 field id”；给“返回为空”的分支：换 universe/region → 核对 delay → 核对 `dataset_id` |
| EX-04 | L33–35 | 情景·P2 | 首例 `quantile(ts_regression(oth423_find, group_mean(oth423_find, vec_max(shrt3_bar), country), 90))` 好：多层嵌套且含 VECTOR。但：①reference 对字段含义写“表示 Find score，可能反映基本面吸引力”，**事实（描述文字）与推测混写**；②`vec_max` 包裹与 datafield-exploration DF-04（探索时不要 vec_* 包裹）方向相反，实为“VECTOR 字段必须 vec_*、MATRIX 禁 vec_*”（`platform_constraints.vec_rules`，KOR 24/24 ERROR 实证），文中未点明；③`country` 作 group 在部分区域无效（`region_invalid_group_fields`） | 示例旁标“VECTOR → 必须 vec_*；MATRIX → 禁 vec_*”；解释分“事实 / 推测”两栏 |
| EX-05 | L43–47；reference L80 | 边界·P3 | reference 说“本手册附录提供了最常用算子的速查表”，但附录只有“附录 A：理解 Vector 数据”——**指向不存在的附录**；第 3 步全量 `get_operators` 输出很大，无“只查用到的几个”的建议 | 删该句或补附录；改“只查表达式中出现的算子” |
| EX-06 | L49–50 | 边界·P1 | 第 5 步“可选”，但：①`python scripts/arxiv_api.py` 是相对路径，agent 的 CWD 通常不在 skill 目录；②同名脚本在 optimization-v1 另有一份（复制，会漂移，且 optimization-v1 版带 DeepSeek 概念层 + `.arxiv_llm.env`，见 OP-04）；③检索词由内部 alpha（字段/概念）生成并发往 export.arxiv.org，未提示“**只发通用关键词，不发未公开表达式/数据集名**” | 脚本单份放共享处，路径写 `<SKILL_ROOT>`；加“外发边界”一句 |
| EX-07 | L52–57 | 情景·🟢+P2 | 🟢 四段模板与“收益来源归因”的用途对得上。P2：①“数据理由”只问“它们代表什么”，**没有证据要求**——收益主要来自 long 侧还是 short 侧、哪一年、哪个行业（`get_alpha_yearly_stats`、`get_alpha_pnl` 可得）；②无长度/落点约束（写到 DB？文件？哪个键？）；③“进一步启发”是自由文本，Mode B 无法结构化消费（新概念名/候选字段/预计正交性） | 给一个成品示例（对首例写完整 4 段，约 120 字）；规定落点（ledger 键需先登记）；“进一步启发”改结构化 3 栏 |
| EX-08 | L59–60；reference L83 | 边界·**P1** | “需要聚合（如 `vec_mean`、`vec_sum`）”——**`vec_mean` 不在 `known_ops`（103）**，平台算子是 `vec_avg`（`vector_only_ops` = vec_avg/vec_max/vec_min/vec_sum/vec_count/vec_norm/vec_range/vec_stddev）。照文写会被 gate0 或平台拒绝 | 改 `vec_avg`，并以 `platform_constraints.json` 的 `vector_only_ops` 为准列全集 |
| EX-09 | L62–65 | 职责·P2 | 上游 selfcorr-quick；本 skill 是“S4 按需工具”；下游 robustness（必经闸）。而 robustness 又把 explain-alphas 列为其**上游**——链条上一个**可选节点**被写成上游，读者不知道跳过是否合规。“2026-09-01 精简：从每候选必经改为按需”是改动史 | 链图写成 `selfcorr-quick →(可选) explain-alphas → robustness`，并写“跳过 explain 不影响 robustness 入场”；删改动史 |
| EX-10 | 全文 | 情景·**是** | 缺两个情景：①“Mode B 换概念前查重叠”——给一个含 3 个 ACTIVE alpha 的 book，目标候选与其中 1 个共享（字段族、时序骨架），输出“重叠高 → 建议换概念”的完整示例；②“战略级候选提交前确认收益来源”——列 3 个否决信号（收益集中于 1 个行业 / 1 年 / 1 侧） | 按左列补情景卡（模板见 Part D §D.3.2） |

---

<a id="s27"></a>
### 27. `brain-calculate-alpha-selfcorr-quick`（L4 · SKILL.md 69 行 + reference.md 约 55 行 + scripts/skill.py 733 行）

**定位**：本地快筛 SELF / PPAC 相关性（不占平台相关性配额，不替代平台实测）。

**总评**：**“★★ 已知结构性盲区”一节是全库对‘本地工具局限’写得最好的范例**——实证（`vRkAO9Xd` 本地 0.229 vs 平台 0.8392，差 0.61）→ 机理（OS PnL 池静态缓存，新提交无 OS PnL）→ 三条使用规则（高值可信、低值≠安全、同族连测不依赖本地）→ 源码出处。问题：①该节在末尾把 `POST /alphas/{id}/submit` 推荐为“零成本实测”，未说明**全部通过时它就是真实提交**；②“self-corr>0.7 无需再查 PROD”的因果链写反，并忽略平台的 Sharpe 豁免路径；③脚本段落**没有回答“被测 alpha 是谁”**，且示例路径 `<SKILL_ROOT>` 与 reference 的 `.qoder/…` 都不可运行。

| 阶段（行号） | 书写逻辑 | 职责划分 | 边界界定 | 需情景规范？ |
|---|---|---|---|---|
| frontmatter + 职责边界（1–28） | 🟢 | 🟢 | 🟡（与 MCP 工具重叠） | 否 |
| 使用场景（30–32） | 🟡 | 🟡 | 🔴（SELF/PROD 混为一谈） | 是 |
| ★★ 结构性盲区（34–54） | 🟢 | 🟡（夹带提交侧知识） | 🔴（POST /submit 零成本） | **是** |
| 工具脚本（56–64） | 🟡 | 🟢 | 🔴（输入不明、路径、凭据） | **是** |
| 衔接协议（66–69） | 🟡 | 🟡 | 🟡 | 否 |
| reference.md | 🟡（英文原译） | 🟡 | 🔴（`.qoder`、CWD 落盘） | 是 |

| # | 位置 | 维度·级 | 问题 | 改进建议 |
|---|---|---|---|---|
| SC-01 | L1–5、L21–24 | 职责·P2 | 边界清楚（本地快筛 / 不占平台配额 / 不替代实测 / 不作提交判定）。但 MCP 已有 `check_self_correlation`（本地增量缓存；`correlation_type` = self / powerpool / all，与平台口径对齐、不占相关性槽位），与本 skill 的 `scripts/skill.py`（批量，Excel 输出）**功能重叠**且文中无选择指引；“相关性”一词还与 `alpha-template-labs-data-analysis` 的 description 触发词重叠（checker I） | 加一张对照表：`check_self_correlation`（单 alpha、即时、进 DB）vs `skill.py`（批量、Excel）；description 触发词限定为“本地快筛 SELF/PPAC” |
| SC-02 | L32、L68；reference L9 | 边界·**P1** | “若 self-corr 高于 0.7，甚至无需再向平台查询生产相关性——因为平台结果同样会高于 0.7”。**SELF（自己已提交）与 PROD（平台生产池）是两个池**，SELF>0.7 并不推出 PROD>0.7；正确的推理只能是“SELF 已 FAIL，任一检查 FAIL 即整体 FAIL，无需再查 PROD”。且忽略平台的“Sharpe 高 10% 可豁免”路径（HP-12） | 改写为“SELF>0.7 → 已必然 FAIL（除非满足 Sharpe 豁免），无需再查 PROD”；豁免是否实现须说明 |
| SC-03 | L34–45 | 边界·🟢+P2 | 🟢 见总评。P2：①未给“近期”的量化界线（新提交多久后进池？池刷新周期？）；②无“何时本地值可信”的检查步骤（如比较池文件 mtime 与最近提交时间）；③“务必先读”的 ★★ 与后文 4 处 ⚠ 强调符号混用，重点稀释 | 脚本输出 `pool_last_refreshed` 与 `newest_alpha_in_pool`，本地值低时**自动**附警告；强调符号只留 ★★ 一处 |
| SC-04 | L47–54 | 边界·**P1** | 推荐“同族连测场景不要依赖本地 SELF，改用零成本实测：`POST /alphas/{id}/submit`”。**仅当硬闸失败时才不消耗配额；若该 alpha 全部通过，POST 就是真实提交**（不可撤销）。“同族只留最优 1 颗”的连测恰是“多个近孪生体逐个 POST”，**最先通过的那颗会被真提交，未必是最优**。文中无“何种情形 POST 会真提交”“由谁授权”的说明；而代码已有双钥保护：`workflow_submit_alpha` / `submit_alpha` 节点默认 `confirm_submit=False`（仅预检 + 查状态），`True` 才 POST 且“必须已有用户明确确认”。RA L685、robustness Phase E #6、prod-corr-avoidance §3 同源 | 改用 `confirm_submit=False` 预检（需核对其返回是否含同等 value/limit）；若必须直接 POST 探测，限定“仅限用户已授权提交且 `submit_verdict==SUBMITTABLE` 的候选，按优劣序逐个”；把它升为全库统一的“POST /submit 危险探测”警告块 |
| SC-05 | L49–52 | 边界·P2 | “`PENDING` ≠ `FAIL`、不挡提交”“`GET /alphas/{id}/submit` 恒 404”是有价值的**否定性事实**。但：①夹带改错史（“旧文写的 `GET … → 403 = BLOCKED` 是错的”）；②“PENDING 不挡提交”来自单次实测，无 alpha id/时间/响应体；与 RA 的 Failed-count（PENDING 不计失败）、`submit_verdict` 的 UNVERIFIABLE 定义是否一致未说明；③“更早拿到实测”不写早多久 | 整段迁到 worldquant-submit-alpha 的“提交 API 行为表”（GET 404、POST 403 语义、PENDING、配额 403 与候选 403 的区分），此处只留链接；删改错史；补证据 id |
| SC-06 | L53–54 | 边界·P2 | “`REGULAR_SUBMISSION: FAIL value=4 limit=4` … 换日即失效”：①“4/4”是某次实测，limit 随账号/日变化，应写 `value ≥ limit`；②“换日”按何时区、何时刷新未写；③“区分候选缺陷与配额耗尽”属提交侧知识 | 迁入 submit-alpha，并写明刷新时点（ET？） |
| SC-07 | L56–64；reference L26 | 情景·**P1** | 脚本段：①示例 `python <SKILL_ROOT>/…/skill.py`——`<SKILL_ROOT>` 未定义，裸 `python` 而非库内约定的 `$WQ_PY`；reference 用 `.qoder/skills/…`（仓库无此目录，checker MISSING）；②`skill.py` 的 argparse **没有 alpha_id 入参**，被测对象靠 `--start-date/--end-date`（MM-DD，年份取当年）+ `--region` + Sharpe/Fitness 阈值圈定，而 reference 把日期区间描述为“取自己已提交的 alpha”——两种读法互斥，“the alpha you are testing”如何指定不明；③`--username/--password` 走命令行（进程列表/shell 历史泄露），与“禁止读取/打印凭据”的项目安全约束冲突，且脚本又读 `BRAIN_USERNAME/BRAIN_PASSWORD` 环境变量——凭据来源再多一种；④依赖安装无 venv 说明 | 补“输入 = 谁”；示例改端到端情景（对区间 X 内新建的 alpha 与已提交池比较，写出预期输出列）；凭据只走环境；命令统一 `$WQ_PY` 与绝对路径 |
| SC-08 | L66–69 | 职责·P2 | 下游写“explain-alphas → 过拟合/稳健性测试（见 optimization-v1）→ judge”。robustness 已是独立 skill（`brain-alpha-robustness`），optimization-v1 L167–198 另有一节重复的“过拟合测试”（OP-13），“见 optimization-v1”会走到重复版而非权威版；上游写 optimization-v1，但本 skill 未被 optimization-v1 回指（checker K） | 链尾改 `brain-alpha-robustness`；optimization-v1 补回指 |
| SC-09 | reference 全文 | 边界·P2 | 英文原译混在中文 skill 里；`--sharpe-threshold -1.0`/`--fitness-threshold -1.0` 默认意味着“不过滤”，未解释；结果“保存到当前目录的 Excel”——落点随 CWD，与“DB 单轨/产物有固定目录”冲突；“Check status (Check OK/FAIL)”未说是谁的检查 | 重写 reference：产物目录固定（gitignore 的运行目录）、默认值含义、列说明 |
| SC-10 | 全文 | 情景·**是** | 用一张 3 行决策表替换现有 3 条规则：①“同族 5 个孪生体，其中 blRaArVZ 昨日提交；本地 SELF=0.23” → **不采信**，预检平台实测；②“本地 SELF=0.81” → 直接否决（保守方向安全），台账记因；③“本地 SELF=0.40 且同族近期无提交” → 可信度中等，提交前仍须平台实测 | 按左列补情景卡（模板见 Part D §D.3.2） |

---

<a id="s28"></a>
### 28. `worldquant-submit-alpha`（L5 · 292 行，单文件）

**定位**：REGULAR 单颗 alpha 的**真实提交**（`POST /alphas/{id}/submit`），含响应四态处置、属性规范、点塔优选、ET 日配额与 PPA 通道。

**总评**：全库**“实测教训”最密**的运行手册——四态响应表（响应形态 / 含义 / 处置，含实证 alpha id）、403 真因读法、点塔三层口径（塔 = `pyramids[].name`；点亮 = 90 天内 ACTIVE ≥3；跨 ≥3 catalog 不计）与“`GET /submit` 恒 404”都有日期与数据佐证。但它也是**自相矛盾最密**的一份：①上游条件 `SUBMITTABLE` 在代码里**不可达**；②配额模型重述 4 处，`activities/submissions` 一处说“不可用”、一处说“可用”（上一轮评审 P0-3，至今未修）；③默认示例带**不存在的形参**并默认 `confirm_submit=True`（复制即真提交）；④PPA 三条路径三种说法；⑤“批量提交”工具实为**仿真派发**；⑥约四分之一篇幅是改错史与审计叙事。

| 阶段（行号） | 书写逻辑 | 职责划分 | 边界界定 | 需情景规范？ |
|---|---|---|---|---|
| frontmatter + 职责边界 + 何时用 + 衔接（1–35） | 🟡（description 380 字） | 🔴（SUPER/PPA/配额/点塔混入） | 🔴（旧根因、SUBMITTABLE 不可达） | 是 |
| 前置（37–40） | 🟢 | 🟡 | 🔴（凭据变量名） | 否 |
| 属性规范（44–52） | 🟢 | 🟢 | 🟡（“强制”无执行者） | 否 |
| 提交流程 · MCP（54–104） | 🟡 | 🟡 | 🔴（示例形参不存在；默认真提交） | **是** |
| Fallback 脚本（106–149） | 🔴（与“禁止手写”并存） | 🟡 | 🔴（无 403/异步处理、GREEN、读 .env） | **是** |
| 关键坑 1–7（151–194） | 🟡（编号重复、夹史注） | 🔴（配额/判定混入） | 🔴（配额自相矛盾） | **是** |
| 点塔优先规则（196–233） | 🟢 | 🟡（含挖矿约束） | 🟡（“过度提交”无阈值） | 是 |
| 验证清单（235–239） | 🟡 | 🟢 | 🔴（“WARNING 不挡”；0.9 无源） | 是 |
| SuperAlpha 段（241–250） | 🟡 | 🔴（自称不处理） | 🟡 | 否 |
| 不要重跑 + ET 配额闸（252–267） | 🟡 | 🔴（配额第 3/4 次） | 🔴（activities；DST） | **是** |
| PPA 通道（269–276） | 🟡 | 🔴（与 L74–83 矛盾） | 🔴（人工通道无交接） | **是** |
| 工具化纪律（279–292） | 🟡 | 🔴（提交 = 仿真派发） | 🔴（“唯一可信入口”） | 是 |

| # | 位置 | 维度·级 | 问题 | 改进建议 |
|---|---|---|---|---|
| SB-01 | L4（description） | 逻辑·P1 | description 仍把旧根因当卖点：“POST 返回 201/200 但 status 因 regular.description 过短而永不翻转”；而正文关键坑 #1（2026-09-26 重写）已声明“此前把 ②③ 误诊为 description 过短；description 过短是**另一条独立成因**”。description 是**触发文本**，agent 只读它就会带着错误因果进入；且一段里塞了触发条件、关键坑、PATCH 写法、延迟、点塔规则 5 类内容（约 380 字） | description 只写“触发条件 + 范围（REGULAR 真实提交；PPA/SUPER 的边界）”；关键坑放正文 |
| SB-02 | L22–24、L241–250、L256–276 | 职责·P1 | 边界声明“REGULAR 单颗真实提交；不处理 SUPER；不作提交判定”，正文实含：SUPER 提交段、PPA 通道段、点塔优选（“提什么”的选择）、配额模型（4 处）、属性规范——**至少 5 个职责**挤在 292 行里，L22 只声明其中一个 | 拆成 ①REGULAR 真提交 + 响应处置；②配额与点塔选择（`quota-and-tower`）；③PPA 人工交接单；SUPER/PPA 段改一句指针 |
| SB-03 | L23、L33、L177–182、L283–285 | 边界·**P1（流程级）** | **上游条件在代码里不可达。** L33 要求上游为“`tools/submit_verdict.py`（**SUBMITTABLE** …）”，AGENTS.md 步 8 同。核对 `tools/submit_verdict.py`：`SUBMITTABLE` 仅在提交层 `GET /alphas/{id}/submit` 返回 **200** 时产生；而同文 L177–182 与该工具 docstring 都确认“GET 平台恒 404”→ 对 UNSUBMITTED 候选只能得 `UNVERIFIABLE` 或 `BLOCKED`，`SUBMITTABLE` 分支及“队列 IS_ONLY → SUBMIT_LAYER_VERIFIED 升级”实际**永不触发**。同文 L283–285 却称该工具是“403 盲区的**唯一可信**判定入口（模拟态 + submit 双视图）”。再加退出码语义 `0 = SUBMITTABLE / UNVERIFIABLE / ALREADY_SUBMITTED`：以 `$?==0` 为放行条件的脚本会把 UNVERIFIABLE 放行 | 写明**可达**状态机：`UNVERIFIABLE + prod 实测 <0.7 + 用户确认 → POST`；L33 改为“submit_verdict ≠ BLOCKED”；L283 删“唯一可信”；工具侧（另开代码任务）让 UNVERIFIABLE 返回独立非 0 退出码，并删除不可达分支 |
| SB-04 | L37–40 | 边界·P2 | “前置”写死凭据变量 `CREDENTIALS_EMAIL/CREDENTIALS_PASSWORD` 与 `.env`；库内凭据来源已有 ≥8 种写法（`.env`、WQ_USERNAME/PASSWORD、BRAIN_USERNAME/PASSWORD、BRAIN_EMAIL/PASSWORD、BRAIN_CREDENTIALS、`~/.brain_credentials`、MCP_CONFIG_FILE、skill config.json），AGENTS.md 明令“凭据位于 `.env`：禁止读取、打印”。本节把变量名写进 SOP，并配合 fallback 脚本读取 `.env`（SB-09） | 只写一句“凭据由 MCP 服务端加载，agent 不接触”；fallback 不读 `.env` |
| SB-05 | L44–52 | 边界·🟢+P2 | 🟢 指向单一事实源（`src/wqb/alpha_properties.py`、`docs/alpha_properties_spec.md`）并列出可检规则（color 仅 5 值、提交默认 BLUE、GREEN 须 OS 挣得；name 模式；tags 必打项与上限；平台已带的不重复打）。核对：`COLORS`、`COLOR_PENDING=BLUE`、`CHANNEL_REGULAR=CH_REG` 与文一致。P2：①“2026-09-20 起强制”——**谁强制**？`check_tags` 只返回 warn 列表、`validate_color` 只校验值域；②name 模式 `<REGION>_<R\|S>_<family>_<seq>` 的 R\|S 在本文未定义（仅 superalpha 的命名 `<REGION>_S_<N>comp_…` 暗示 S=SUPER），PPA 示例 `DEU_R_starminerev_02` 也用 R，PPA 是否需单独的通道码未说；③“一颗最多 4–5 个”含糊 | 引用规格表；定义 R\|S；上限写死一个数；说明由哪个工具校验 |
| SB-06 | L54–71 | 边界·**P1** | 默认示例 `workflow_submit_alpha(…, dataset="insiders1", wave="113", expr_family="insgate", …, confirm_submit=True)`：①`dataset/wave/expr_family` **不是该工具的形参**（真实签名：`alpha_id, name, color, tags, descriptions, force, confirm_submit, verify_timeout, dry_run`；机械检查 E 判 BAD-PARAM；上一轮评审已指出），注释“给了这些则 tags 可留空自动生成”无实现；②**默认示例就是 `confirm_submit=True`（真实提交）**，而工具与 AGENTS.md（步 8）规定“默认 False；True 须用户明确确认后单独调用”——复制即真提交；③description 下限三处不同：L67 三段式（无字数）、L123“≥100 字”、L247“≥100 英文字” | 示例拆两步：先 `confirm_submit=False` 预检并展示返回，再给“**仅在用户确认后**”的 True 版；删不存在的形参；description 下限写一处（词/字、语言） |
| SB-07 | L74–83、L273–274、L292 | 职责·**P1** | **PPA 走哪条路，三处说法不同**：L74–83 用 MCP `workflow_submit_alpha(color="PURPLE", tags=[…,"PowerPoolSelected"], confirm_submit=True)` 直接提；L273–274 称“MCP `submit_alpha` 不是 PPA 感知的，内置常规 RA 闸，合法 PPA（Sharpe≥1.0…）必须走平台 web UI”；L292 又称“PPA 不走本工具链” | 一张路由表：候选满足 MCP 预检线（见 SB-08：Sharpe>1.3、Fitness>0.75、turnover 4–40%、returns>4%）→ 可 MCP；否则 → web UI 交接（SB-22） |
| SB-08 | L85–104 | 边界·P2 | 分步模式 `force=True` 仅注释“跳过本地启发式预检”，未写**预检内容**：`pre_submit_check`（`brain_mixin_simulation.py`）= Sharpe>1.3、Fitness>0.75、turnover 4%–40%、returns>4%、无 FAIL；margin 仅 warning。这是本库第 5 套 Sharpe 线（平台 1.25 / 预检 1.3 / 内部 1.58 / …）与第 4 套换手区间（平台 1–70%、内部 5–20%、预检 4–40%）。也未说明 `force=True` 的允许场景（合法 PPA Sharpe<1.3；SUPER） | 列出预检规则与 `force` 的允许场景；数字指向 config 统一表 |
| SB-09 | L38 vs L106–149 | 逻辑·**P1** | L38 “**禁止手写 requests 脚本**”与 L106 起 44 行手写脚本并存（仅一句“仅 MCP 不可用时”）；而本会话的 MCP 服务正是 ENOENT 不可用——恰是 fallback 场景。脚本与同文关键坑不一致：①`assert r.status_code in (200,201,202)` 对 **403** 直接抛 AssertionError，丢掉关键坑 #1 ④ 要读的“全量 checks 与真因”；②不实现 ②③（异步受理需 re-POST），只轮询 3 分钟；③PATCH 示例带 `"color":"GREEN"`、`"name":"ppa_xxx"`，违反本文 L47–49（GREEN 禁作默认；name 规范），description 示例“PPA alpha on USA TOP3000”混入 PPA 语境；④`load_dotenv("world-quant-brain-mcp/.env")` 读取 `.env`，与“禁止读取”冲突；⑤备退避说“30+15s×n 会连续 429 空转”，脚本用 `retry_after + attempt*10`——第 3 套退避；⑥裸 `python`、相对路径 | 删除脚本，改为“MCP 不可用 → 停止并报告，不手写提交（提交不可撤销）”；如确需保留，须实现 403 读取/异步补发/UI 交接且凭据只走环境 |
| SB-10 | L151–162（关键坑 1） | 逻辑·🟢+P2 | 🟢 四态表（响应 / 含义 / 处置）+ 实证 id + “另一条独立成因”的区分，是全库最清晰的响应处置表。P2：①“等多久”四个口径：客户端 60 s（`_poll_submit_until_resolved` 6×10 s）、`verify_timeout=180`、#3“通常 2~3 分钟”、表②“等 4 分钟 → re-POST”；②“re-POST 补发”缺护栏：补发前应先 `get_alpha_details` 确认 `dateSubmitted` 为空（而 L253 说已提交后重 POST“幂等但浪费额度”，未验证）；③③“空体 200 → 必须补发，不得当失败”，但 MCP 的 `submit_alpha` 在 200 而 body 非 JSON/空时 `return False`（把③报成失败，且该方法文档声明返回 dict 却在部分分支返回 bool），文中未写 agent 见到 `False` 应怎么做；④三个悬空 >24h 的实证 id 未写最终如何处置 | 用一张状态机表统一“受理 → 轮询窗口 → 补发条件 → 放弃条件”；③补一行“工具返回 False → 先 GET details，不要重试”；④补结局 |
| SB-11 | L164–170、编号 | 边界·P2 | 关键坑第 2 条：“`PENDING` ≠ `FAIL`，不挡提交，不要据此判死”——与 RA `check_counts_as_failed`（PENDING 不计失败）一致；但只说了“不判死”，没说“**也不据此放行**”（放行须 prod 实测 <0.7，`submit_verdict` 输出里已有此提示）；“`REGULAR_SUBMISSION: FAIL value=4 limit=4`”是示例值，应写 `value ≥ limit`；“换日即失效”未写刷新时点（SB-21）。**编号重复**：#1、#2（403 真因）、#2（description PATCH）、#3…共 8 条，两个“2.”，“见第 1 条 / 见下条”会指错 | 重新编号；PENDING 处置写成两栏“不据此判死 / 不据此放行” |
| SB-12 | L171–176 | 边界·P3 | ①description PATCH 嵌套写法（扁平 400 “Unexpected property”）可执行、可核对，但 MCP `set_alpha_properties` 已封装，此条只对 fallback 有意义，随 SB-09 一并处理；②#4“原 21 项闸门结果已锁定”——`RA_CHECK_NAMES` 是 18，“21”从何而来未定义 | 删 ① 或并入 fallback；“21”改为引用 `is.checks` 实际项数或 18 |
| SB-13 | L177–182（#5） | 逻辑·P2 | 全库把“GET /submit 恒 404”说得最清楚的一条，但：①夹带审计叙事（“历史文档有三种互相矛盾且都错的说法”）与对代码的评论（“故 submit_verdict 的 403 分支是死代码”）——这类内容应在代码注释/CHANGELOG；②与 L283–285 同文矛盾（SB-03）；③“真闸只能靠 POST”与 how-to-pass HP-03、selfcorr-quick SC-04 的“用 POST 读配额 / 零成本探测”同源，**本条没有把‘POST 通过 = 真实提交’写成显式警告** | 升格为“提交层信息来源表”：`GET /submit`（404）/ `POST /submit`（三态；**通过即提交**）/ `get_alpha_details.is.checks`（模拟层）各能回答什么、是否会真提交；删叙事 |
| SB-14 | L183–187、L239 | 边界·**P1** | #6 “确认无 FAIL（`WARNING`/`PENDING` **不挡**）”；how-to-pass §4 却说“IS 阶段 CW=WARNING 的 alpha 提交后必 FAIL … WARNING 就别提”，RA `check_counts_as_failed` 把 WARNING 计入失败，`submit_verdict` 把 `LOW_FITNESS/LOW_SHARPE/LOW_2Y_SHARPE` 的 WARNING 当提交层硬闸（`_SUBMIT_HARD_GATE_WARNINGS`）；L239 又把“WARNING”限定为“描述长度/格式/主题”。**同一个词三种范围** | 定义：WARNING 分“硬闸类（CW、LOW_FITNESS/SHARPE/2Y…）≡ FAIL”与“提示类（描述/格式/主题）不挡”，列各自名单，引用 `_SUBMIT_HARD_GATE_WARNINGS` 与 `config.RA_CHECK_NAMES` |
| SB-15 | L188–194（#7）、L264 | 边界·**P1** | ①“REGULAR 余量的**唯一可靠来源** = POST 响应里的 `REGULAR_SUBMISSION`”——读配额必须发起一次 POST，POST 全过就是真实提交；与 L194“批量提交前 30 秒内必须**复检**一次”**无法同时成立**（复检 = 再 POST 一次？）。②L191 “`activities/submissions` 缺 `today`、**不可用**于当日判断”与 **L264 “判断今天 ET 日已用几颗：拉 `/users/self/activities/submissions`”直接矛盾**（上一轮评审 P0-3，仍在）；代码侧 `tools/quota_status.py`（2026-09-21 事故后）用 `stage=OS` 的 `dateSubmitted` 按 ET 日计数并注明“`activities` 只有 yesterday/current/previous/ytd 快照，不得用于当日”，而 toolkit `pipeline.py:206` 仍**优先**读 activities、回退才用 OS alphas——同一“今日已用几颗”两套实现；`quota_status.py` 的 usage 行还有未实现的 `--submission-type SUPER` | 给出**只读**配额来源的唯一顺序：`quota_status.py`（OS 阶段 ET 日计数，不区分类型）；“复检”改为“重跑 `quota_status.py`”；L264 改正；`pipeline.py` 与之同源；删未实现的 flag |
| SB-16 | L196–233 | 边界·🟢+P2 | 🟢 三层口径 + “0 亮区域单颗 ≠ 点亮” + 四档排序，数字都有实证（USA/FUNDAMENTAL 平台计 5 颗，其中 4 颗为 2025-09~2026-01 老 alpha → UI 未亮），并给权威入口 `campaign_intel.py pyramid`（`WINDOW_DAYS=90 / EXCLUDE_MULTI=3 / MIN_LIT=3`）。P2：①“已过度提交的区域（如 MEA 本季度）不提交”——“过度”**无阈值**，“MEA 本季度”是带日期的例子；②“候选将点亮哪座塔”UNKNOWN 时“按该区域未亮类别保守判断”无算法；③“混 3+ 类 = 白提”是**选题约束**（S0/S1），却写在提交 skill 末尾，RA/campaign-matrix 是否引用未知；④排序“fitness 降序、其次 sharpe”与 CLAUDE.md“点塔要均匀”是两个目标：同档内是否要在区域/塔之间轮转（避免连续把 3 颗给同一区域）；⑤“近 90 天”是日历日，CLAUDE.md 窗口准则用交易日（季度 66），未说明；⑥**分档边界重叠**：第 1 档写“现状 ≥2/3，差 1-2 颗 / 找差 ≤2 颗的塔”，第 2 档写“现状 1/3（差 2 颗）”——“≥2/3”= 差 ≤1 颗，而“差 ≤2”又包含“差 2”，1、2 档重叠；⑦“差 1-2 颗的塔**一次提交即点亮**”（frontmatter 与 L213）只对**差 1 颗**成立，差 2 颗的塔一次提交仍差 1 颗；⑧同一规则在 brain-alpha-judge L252–272 还有一份逐句拷贝（JD-16） | 给“过度提交”阈值（每区每季 ≥N 颗）；UNKNOWN 的决策规则；把 ③ 上移到 campaign-matrix D 卡并互链；轮转规则；写明 90 日历日 ≈ 66 交易日 |
| SB-17 | L224–225 | 边界·P2 | “平台字段权威确认：`GET /data-fields/{field}?…`（单字段端点；列表接口带 search 会返回 `["Invalid query"]` 不可用）”——与 MCP `get_datafields(search=…)`（explain-alphas、datafield-exploration 都在用的“带 search 的列表接口”）冲突；且该单字段端点**没有 MCP 封装**，agent 只能手写 GET（又与 L38“禁止手写”冲突） | 二选一：给该端点做 MCP 封装；或说明 `get_datafields` 在何条件下会 `Invalid query` 及替代 |
| SB-18 | L235–239 | 边界·P2 | ①“内部从严线：`LOW_SUB_UNIVERSE_SHARPE≥0.9`”——全库检索（config、submit_queue、tools）**没有该常量，本行是唯一来源**；②验证清单里 WARNING 的范围与 #6 不同（SB-14）；③成功标志“`status==ACTIVE` 且 `dateSubmitted` 非空”清楚，但**没有未决/失败终态**：仍 UNSUBMITTED >4 分钟 → 补发；>24 h → ？ | 删 0.9 或补出处；终态表加两行 |
| SB-19 | L241–250 | 职责·P2 | 边界声明“不处理 SUPER”，此段仍含 `workflow_submit_alpha(confirm_submit=True, force=True)` “**两次**取 verdict”、`set_alpha_properties` 对 SUPER 必 400、`combination(alpha(...))` 不可用、“SUPER 不点塔”——与 wq-brain-superalpha 重复（一处改、另一处漂移）；“硬闸门 FAIL 不消耗配额，属零成本探测”又一次把 POST 探测说成零成本；“两次取 verdict”未说明**第一次是否已是真提交** | 压缩为 3 行指针，细节只在 superalpha |
| SB-20 | L252–254 | 边界·P2 | “已提交后 `POST /submit` **幂等**返回 200，但会**浪费额度**/产生混乱”——“幂等”与“浪费额度”矛盾（若幂等则不应扣额度）；无证据（alpha id/日期） | 写实测结论：重复 POST 是否扣配额（是/否 + id），再定“不要”的理由 |
| SB-21 | L188–194、L249、L256–267、L292 | 边界·**P1** | 配额模型全文 **4 次**重述且不一致：①activities 可用 / 不可用（SB-15）；②“00:00 ET（= 12:00 GMT+8）重置”**仅夏令时（EDT, UTC-4）成立，2026-11-01 DST 结束后为 13:00 GMT+8**；`quota_status.py` 固定 `ET=UTC-4`（注释“EST 时改 -5”）、`pipeline.py`“全年用 UTC-4”，本地 DB `alphas.date_submitted` 亦为 -04:00——**定时炸弹**（与 CLI gate-mode 日期翻转同类）；③“三重实证（08-12、08-31…）”是推翻旧模型的证据链，属 CHANGELOG；④L292“旧 48h 滚动口径已废止”又一处改动史 | 配额模型只保留一处（`quota-and-tower`），时区用 `America/New_York` 计算；删改动史；在 2026-11-01 前加测试/注释复核 |
| SB-22 | L269–276 | 情景·**P1** | 合法 PPA“必须走平台 web UI 提交”——**这是人工通道，agent 无法执行**，正文却写成流程步骤（“…→ web UI 手动提交 → 回写 submission_ledger”）。agent 到这一步应**停下并交接**，但没有：①交接单模板（候选 id、PPAC 值、主题窗口证据、Sharpe/算子数/字段数核对）；②用户提交后**回写工具**（`submission_ledger` 表存在于 `store/_submissions.py`，skill 未给写入工具名）；③用户不在线时的默认动作（候选留队列，不重复催）。另：“Sharpe≥1.0 / 算子≤8 / 字段≤3 / PC<0.5”与 ppa-mining 的 PPA 判据是否一致未核；“`MATCHES_THEMES`=PASS 才受理”的读取方式未给；“每天先提 PPA 那颗是既定纪律”叠加“PPA 走 web UI”意味着**每天固定一次人工操作**，next-move/日程未显式列出 | 加“PPA 交接单”模板（8 行）与回写命令；PPA 判据只在 ppa-mining 定义，此处引用 |
| SB-23 | L273 | 边界·P2 | “内置常规 RA 闸（实测 Sharpe>1.3 / Fitness>0.75 / **Margin>15bp**）”与代码 `pre_submit_check` 不符：**Margin 自 2026-08-13 起降为 warning**（USA 5bp，其他 8/15bp 仅警示，“平台不检 margin”），而 **Turnover 4–40%、Returns>4%** 是硬失败——文中漏后两条并错标 margin；“打 PowerPoolSelected 标签重试仍拦”因为预检根本不看标签 | 与 SB-08 合并，引用 `pre_submit_check` 实际规则 |
| SB-24 | L279–292 | 职责·**P1** | ①`tools/submit_batch.py` 被列为“批量提交”，但其 docstring 明示是 **REST 仿真派发**（`POST {base_url}/simulations`，payload `[{type, settings, regular}]`，参数 `--path exprs --decay --neutralization`），并注明真正的“生产提交原语”是 `world-quant-brain-mcp/tools_submit.py` 的 `submit_alpha`（提交已存在的 alpha_id）。AGENTS.md L250 也写“批量提交 `tools/submit_batch.py`”；MCP 里同名工具 `submit_batch`（`tools_ops.py`，docstring“批量提交 alpha 表达式进行回测（REST 直连）”）同样是 `POST /simulations`，judge L111–112 却把它与 `workflow_submit_alpha` 并列为提交 alpha 的“真实入口”（JD-09）。**“提交”一词两义（仿真派发 / alpha 上平台）**，agent 想批量上平台会去派发新仿真。②`submit_verdict` 被称“唯一可信入口”，与同文 L177–182 矛盾（SB-03）。③代码块用 PowerShell（`& $WQ_PY`），L213 用 bash 风格 `python tools/…`——同文两种 shell。④“旧 48h 滚动已废止”是改动史 | 术语表：`dispatch`（仿真派发）≠ `submit`（提交上平台）；`submit_batch.py` 改名或在描述首行加 `simulate`；shell 统一为一种 |
| SB-25 | 全文 | 情景·**是** | 缺端到端情景。建议四张：①**正常**：IND 候选 X（塔差 1 颗点亮）→ `submit_verdict`=UNVERIFIABLE → prod 实测 0.55 → 用户确认 → `confirm_submit=False` 预检 → `True` → 200 → 轮询 ACTIVE → 回写 S6；②**异步受理未翻转**：201 → 4 分钟仍 UNSUBMITTED → GET details 确认 `dateSubmitted` 空 → re-POST；③**配额 403**：`REGULAR_SUBMISSION value=4 limit=4` → 停、不判死候选、记“待次日”、不重试；④**并行会话用光配额**（2026-09-25 案例）→ 复检来源 = `quota_status.py` | 按左列补情景卡（模板见 Part D §D.3.2） |

---

<a id="s29"></a>
### 29. `wq-brain-superalpha`（L5 · 250 行，单文件）

**定位**：把同一区域 ≥10 颗 ACTIVE REGULAR 合成为一颗 SUPER alpha（selection + combo），并压 SELF/PROD <0.7 后提交。

**总评**：**参数—指标对照做得最扎实的一份**——“篮宽 × decay”二维表、KOR 的 decay 12→300 逐档曲线、“`selectionLimit` 超过有效池后无效（1000 与 50 逐位相同）→ 改门不改 limit”都是可复核的反直觉结论；“201 ≠ SA 合法，错误异步出现在模拟结果里”给了确切响应体。但它是**追加式日记**：后文推翻前文而前文不改（L108“SUBINDUSTRY 是决定性杠杆”被 L131–154、L232 推翻，靠“优先于上表阅读”补丁），4 个案例按时间堆叠且与现行默认 prod 闸冲突，规则、快照、案例混在一起。结构性缺口有三：①**从头到尾没有“如何创建 SA”的调用**（`super_build.py select`/`probe` 与 MCP `workflow_superalpha` 均未提，只提 `submit`）；②submit 流程有两个安全性不同的入口，MCP 路径 `force=True` 绕过 prod 闸；③combo 只给到“`1 - maxCorr`”，不可执行。

| 阶段（行号） | 书写逻辑 | 职责划分 | 边界界定 | 需情景规范？ |
|---|---|---|---|---|
| frontmatter + 运行环境 + 边界 + 何时用 + 衔接（1–40） | 🟡（description 400 字） | 🟡 | 🟡（SUBMITTABLE 不可达） | 是 |
| 硬前置（42–73） | 🟡（快照混入规则） | 🟡（区域状态/配额） | 🔴（MEA、计数矛盾、失效脚本） | **是** |
| SA 结构 + selection / combo 语法（75–106） | 🟡 | 🟢 | 🔴（combo 不可执行；“必须出现”缺理由） | **是** |
| 关键杠杆 SUBINDUSTRY（108–114） | 🔴（被后文推翻） | 🟡 | 🔴 | 是 |
| 篮宽×decay / 饱和 / decay 曲线（116–156） | 🟢 | 🟢 | 🟡（阅读顺序；区域快照） | 是 |
| 提交判定陷阱 + 双闸探针（158–173） | 🟡 | 🟡 | 🔴（GET 200 vs 恒 404；本地盲区） | 是 |
| submit 流程（175–189） | 🟡 | 🔴（CLI vs MCP 两入口） | 🔴（`force=True` 绕 prod 闸；“预检”=真提交） | **是** |
| 4 个真实案例（191–235） | 🟡（日记体） | 🟡 | 🔴（与现行闸冲突） | 是 |
| 验证清单 + 相关 skill（237–250） | 🟢 | 🟢 | 🟡（错误指针） | 否 |

| # | 位置 | 维度·级 | 问题 | 改进建议 |
|---|---|---|---|---|
| SP-01 | L4、L19 | 逻辑·P2 | description 400 字，塞入 `(1 + 0 * (prod_correlation > 0))`、`score = (0.7 - prod_correlation)`、`self_correlation < 0.55`、`workflow_submit_alpha(confirm_submit=True, force=True)` 等实现细节，作为触发文本过载，且把 `confirm_submit=True, force=True` 当成固定调用（见 SP-13）。L19 的“运行环境”段落位于 H1 之前，列举的“创建/提交工具”含 `set_alpha_properties`——本文 L66 自己声明它对 SUPER 必 400 | description 只留触发词 + 前置条件 + 范围；L19 移入正文并删 `set_alpha_properties` |
| SP-02 | L23–27、L38–40 | 职责·P1 | 边界写得好：“本区 ACTIVE REGULAR ≥10 且双闸达标；**不得改用 REGULAR 路径绕过**”（🟢 有止损句）。问题：①上游写“`submit_verdict`（SUBMITTABLE 且 type=SUPER…）”——`tools/submit_verdict.py` 与 `tools_submit.py` 全文**无任何 SUPER 分支**，且 SUBMITTABLE 不可达（SB-03）；②“组件不足 → 回 RA 步 7”，但 RA 步 7 是“诊断改进”，并不承担“攒齐 10 颗 ACTIVE REGULAR”；③下游“SUPER alpha 入池”（L27）与“S6 监控”（L40）两种说法 | 上游改为“无 BLOCKED + prod 实测 <0.7 + 用户确认”；写出“组件不足 → 缺口 N 颗 → 交给 RA 的输入（区域、缺口、需要 prod<0.55 的新血）”，并指明接收的 RA 步骤 |
| SP-03 | L42–73 | 情景·**P1** | “硬前置（必读，否则必败）”混了四类东西：①规则（≥10 颗、异步校验、描述 ≥100 字、裸 PATCH）；②**日期快照**——“现状（2026-09-11）：USA 133 / MEA 19 / IND 18 / KOR 13 / EUR 7 / …”，与 L35“USA ~145 ACTIVE”、案例 3“GLB 恰好 10 颗（09-24）”并存，**同文自相矛盾**且已过期 18 天；③区域状态（MEA 关闭、EUR 差 3 颗）；④区域瓶颈与历史教训（KOR 空壳草稿）。快照会过期，规则不会，读者无法区分“永远成立”与“当时如此” | 规则留正文；计数改为**实时命令**（`super_build.py status` / `get_user_alphas` + 本地分组）；区域状态与瓶颈移入各区 profile |
| SP-04 | L44–53、L216 | 边界·🟢+P2 | 🟢“**201 ≠ SA 合法**：错误异步出现在模拟结果（`status:"ERROR"`，`At least 10 component alphas are required`）”——给了确切响应体与判据；“先数本区 ACTIVE REGULAR 数再决定是否发 sim”把便宜检查前置。P2：计数方法用原始 HTTP 翻页（`GET /users/self/alphas?status=ACTIVE`），而“`region=` 参数不生效，须拉全量后本地按 `settings.region` 分组”这条**必要提醒在 L216，晚了 170 行**；且与 submit-alpha 的“禁止手写 requests”冲突 | 把 L216 提醒上移到此；给 5 行的 MCP 计数脚本 |
| SP-05 | L54–56、L35 | 边界·P2 | “MEA 通道已关闭：`POST /simulations region=MEA` → 400 ‘Region MEA is not available’，既有 2 颗 MEA SA 是存量，不能再新增”是**平台区域状态**，不属 SA 方法论；而 L35 仍把 MEA 列入“需先攒齐 ≥10 颗”的区域，案例 2 全篇是 MEA | 区域状态放 `regions/mea.md` 与 campaign-matrix；L35 删 MEA；案例 2 标“存量，不可复制” |
| SP-06 | L65–70 | 边界·🟢+P2 | 🟢“各需 ≥100 英文字；`set_alpha_properties` 对 SUPER 必 400（无条件带 `regular` 字段）；正确写法 = 裸 PATCH 最小 payload，写后回读长度”——症状 / 原因 / 正确写法 / 回读验证齐全。P2：参考脚本 `logs/_fix_desc_sa4.py` **不存在**（`logs/` 下仅 `_async_tasks`、`_dblock`、`test-results.xml`）；`super_build.py submit` 已“内置 ≥100 英文描述”，文中没说 CLI 路径**不需要**手工 PATCH，读者易两边各做一遍 | 删失效指针；写“用 CLI → 描述自动写入；手工路径才需裸 PATCH” |
| SP-07 | L71–73 | 边界·P2 | 配额模型再次重述（ET 日 REGULAR 4 + SUPER 1；`get_submission_quota` 已移除；读 submit 响应；“硬闸 FAIL 不消耗配额，属零成本探测”）——与 submit-alpha SB-21、INDEX L413–420 重复；“零成本探测”在 SUPER 场景尤其危险：两次 POST 里**第二次通过就是真提交**（SP-13） | 删，改指针 |
| SP-08 | L75–106 | 逻辑·**P1** | ①combo 只给“`1 - maxCorr`；maxCorr 借助 `generate_stats/self_corr/reduce_max/if_else` 等算子构造”，示例骨架 `combo: 1 - maxCorr`——**不是可执行表达式**；可执行模板在 `tools/super_build.py::COMBO_TEMPLATE`（`stats = generate_stats(alpha); innerCorr = self_corr(stats.returns, 500); ic = if_else(innerCorr == 1.0, nan, innerCorr); maxCorr = reduce_max(ic); w = 1 - maxCorr; {expr}`），SKILL 未引用；其中 `500` 不在标准窗口表（2 年 = 504）也无解释。②“USA **必须**在表达式里出现 `(prod_correlation > 0)` 子串，但作为非门控 no-op 写”——**必须**由谁要求（平台？）、不写会怎样（400？）未说；后半句“否则会把 novel 成分清零”与“必须出现”是两件事，被写成一句。③“逻辑符 `&`/`and` 被拒”好（可核对），但未给被拒时的报错原文。④turnover 界 (0.01, 0.5)，案例 2 用 `<0.6`，为何不同未说 | 文中放 `super_build.py select` 生成的**完整** selection / combo 原文；②写明来源与后果；③补报错原文；④参数化并说明取值理由 |
| SP-09 | L108–114 vs L116–156、L232–235、L241 | 逻辑·**P1** | **追加式文档：后文推翻前文，前文未改。** L108“把 PROD 压到 0.7 以下的**决定性因素**是 SUBINDUSTRY”；后文：“PROD 已结构性饱和（USA 0.85–0.91、KOR 0.78），**调参无解**”（L131–137）、“PROD 地板由成分池决定，与评分/decay 无关”（L154）、“KOR 的优势中性化是 STATISTICAL，不是 SUBINDUSTRY”（L232）、“neutralization 必须逐区扫描”（L241）；L116 标题“优先于上表阅读”是用**阅读顺序补丁**代替改写。当前至少 5 个“决定性杠杆”并存：SUBINDUSTRY / decay / 宽篮 / 池新鲜度 / 逐区扫描 | 重写为一张“SA 双闸决策表”：症状（SELF 高 / PROD 高 / 组件不足 / 子宇宙不过）→ 已实证有效的杠杆（含区域与篮宽）→ 已实证无效项 → **止损线**（PROD 饱和 → 注入低 prod 新血，不再调参） |
| SP-10 | L116–156 | 逻辑·🟢+P2 | 🟢 篮宽×decay 表与 KOR decay 曲线（12→300 逐档 SELF / S / F / turnover）是全库最完整的参数-指标对照。P2：①“USA V8/V9/V11/V12 SELF 全过”是私有变体代号，无定义；②两组数据口径不同（USA 12 结构·宽篮 / KOR 窄篮·nu=SECTOR），“decay 对 SELF **恒**为负向杠杆”由 2 个区域推出；③“PROD 饱和”表只有 USA、KOR；④“快速探测成分池 prod 分布：selection 加硬门 `(prod_correlation < 0.6)`，若报 ‘At least 10 component alphas’ 即合格成分不足”是极好的**零成本探针**，却埋在 decay 小节末尾 | 变体代号给 id；“恒”改“在 USA/KOR 观察到”；把探针提到“硬前置” |
| SP-11 | L158–165 | 边界·**P1** | “**`GET /alphas/{id}/submit` 200 可能是 PENDING 假阳性**”——与 submit-alpha 关键坑 #5（“`GET /submit` 恒返回 404，对已 ACTIVE 的也 404”）及 `submit_verdict.py` docstring **直接冲突**：同一端点一处说 200、一处说恒 404。也许 SUPER 与 REGULAR 行为不同（若是应明说“对 type=SUPER 返回 200”），也许是 09-11 的观察被 09-26 的实测覆盖而未更正 | 核实后二选一；两份文档加“按 type 区分”的行为表（GET/POST × REGULAR/SUPER/PPA） |
| SP-12 | L167–173 | 边界·P2 | “零成本双闸探针（提交前必做）”用 MCP `check_self_correlation` 与 `check_correlation`：①配套 CLI `super_build.py probe`（SELF 本地 + PROD 平台）未提；②`check_self_correlation` 的本地 OS PnL 池**对近期提交的孪生体结构性失明**（selfcorr-quick SC-03：本地 0.229 vs 平台 0.8392），而 SA 恰是“池子被消耗、近克隆风险高”的场景（案例 4：STATISTICAL/dec5 与存量 rKOPg9gd 同构，SELF 0.9729）——**本文既知近克隆风险，又推荐一个会漏报近期克隆的探针**，且二者互不引用；③`check_correlation` 阻塞最长 60 min（HP-11），`super_build.py` 的 prod 探针是 15 s×900 s，两套等待策略；④`run_selection` 误区提醒（“选股工具≠alpha 选择”）很好，却埋在引用块里，submit-alpha 又重复一遍 | 探针统一为 `super_build.py probe`；注明本地 SELF 盲区，“近期有同构 SA 提交时以平台实测为准” |
| SP-13 | L175–189、L19、L4 | 边界·**P1** | submit 流程有**两个入口，安全性不同**：Step 0 的 **prod 闸**（max≥0.7 拒绝；超时 fail-closed；`--allow-prod-above-07` 豁免）**只存在于 CLI `super_build.py submit`**；Step 2–3 却写成 MCP `workflow_submit_alpha(confirm_submit=True, force=True)` 连调两次——`force=True` **跳过本地预检**，MCP 路径没有 prod 闸，“用户铁律：prod≥0.7 不提交”在该路径无强制。且“**再调一次**→直接回带 verdict；200 = 全部过闸”意味着第二次调用通过时 SA **已被真提交**（2–3 分钟后翻 ACTIVE），并非探测；L215、L222 把 `super_build.py submit` 称为“零成本预检”，案例 4 的“逐个 submit 预检”中第一个通过的变体就会被真提交，未必最优。另外 MCP 还有第三入口 `workflow_superalpha(region, components, selection, combo, neutralization, confirm_submit=False, dry_run)`，SKILL 完全未提；`super_build.py select`（创建 SUPER simulation）、`status`、`probe` 也一字未提（全文只出现 `submit`），因此**没有给出“如何创建 SA”的调用** | 主入口唯一：`super_build.py {select|status|probe|submit}`，四步各给命令与预期输出；MCP 路径仅在 CLI 不可用时使用，且**必须手工先做 Step 0**；`force=True` 只在“预检误拦”时使用并记因；把“submit 通过即真提交”写成显式警告，并把“预检”改称“提交尝试” |
| SP-14 | L191–235 | 情景·**P1** | 四个“真实案例”按时间顺序堆叠：案例 1 自称使用已禁用的 `combination()`，“此处仅为等价思路说明”，**不可复现**，且“成分：…→ 等价体须 PROD≤0.7 且 SELF≤0.7 且 ACTIVE”是验收标准不是案例；案例 3/4 的“平台回带 0.8094 / 0.8571 仍判 PASS → ACTIVE”与**现行默认 prod 闸（≥0.7 一律拒绝，2026-09-25 起）冲突**——按今天的默认 CLI 这两颗会被拒，除非 `--allow-prod-above-07`，文中未说当时是否使用豁免；“PASS/FAIL 分界在 0.86~0.89”又与“判定永远只看 result”并存。各案例的 ★ 教训（“只看 result 不看 value”“同构淘汰法”“逐区扫描”）只出现在案例里而不在规则区 | 规则/案例分离：规则区放“已验证规则表（规则 / 证据案例号 / 适用范围）”，案例区每例 5 行（背景 / 操作 / 结果 / 是否可复现）；案例 3/4 标“提交时未受 prod 闸约束，现行需 `--allow-prod-above-07`” |
| SP-15 | L214–215、L228–229、L243–244 | 边界·P2 | “判定只看 result，不看 value”出现 3 次，“我方铁律 prod≥0.7 不提交，以我方闸为准”出现 2 次，**两者并存时的优先级只在验证清单末尾一句**（L243–244）；读到案例 3/4 的人会以为 “value>0.7 也可提交” | 顶部放一条“判定优先级”：平台 result=PASS（必要）∧ 我方 prod<0.7（必要）→ 才提交；后者更严，二者不冲突 |
| SP-16 | L216–218 | 边界·P3 | “淘汰的同构变体打 `RETIRE_<date>_DUP_SA` + color RED + hidden，防审计误报”——`RETIRE_…` 是 tag 还是 name 未说，也未对照 `alpha_properties` 规范（color 值域、tag 前缀 `CH_/SRC_/W/EXPRFAM_/CORR_`）是否允许这类标签 | 引用 `alpha_properties`；如需新增前缀先登记规范 |
| SP-17 | L237–245 | 边界·🟢+P3 | 🟢 六条勾选项可检（“组件恰好 10 颗时必须放宽 gate，否则秒拒”“只看 result 但我方 prod 闸优先”）。P3：“neutralization 逐区扫描（USA/GLB=SUBINDUSTRY、KOR=STATISTICAL、IND 一轮各一）”把区域结论写成清单，而同文强调“区域结论不可迁移”；`super_build.py` 默认 `--neutralization SUBINDUSTRY`，与“KOR=STATISTICAL”不一致，默认值会把人引向错误起点 | 清单改为“需扫描的档位 + 已知最优（区域，日期）”；CLI 取消默认值，强制显式指定 |
| SP-18 | L247–250 | 边界·P2 | “`alpha-expression-verifier`：提交前本地校验 selection/combo 表达式语法”——核对：该 skill 全文**无** selection / combo / SUPER 字样，指针指向不具备该能力的 skill；“`brain-how-to-pass-alpha-test`：各 IS 闸门阈值”对 SUPER 专属闸（`SUPER_SUBMISSION`、`NON_SELF_SUPER_ALPHA`、SUPER 的 LOW_TURNOVER 0.02）无覆盖 | 删该指针或改为 `super_build.py select` 的报错处理；SUPER 专属闸表放本 skill |
| SP-19 | 全文 | 情景·**是** | 缺三张“从零到一”情景：①**KOR/IND 从 0 到 SA**：数组件 → 差 N 颗回 RA → `select`（decay / nu / self-gate）→ `status` → `probe` → `submit`；②**组件恰好 10 颗**（GLB 案例）：self_gate 0.65 → 0.70 → 0.85 的放宽路径与代价；③**近克隆被拒**（KOR 案例 4）：枚举存量 SA 的 (nu, decay) → 错开 → 逐个尝试 → 淘汰打标。并加一条止损线：“PROD 饱和且无低 prod 新血 → 停止调参，回 RA” | 按左列补情景卡（模板见 Part D §D.3.2） |

---

<a id="s30"></a>
### 30. `brain-alpha-judge`（L5 · SKILL.md 300 行 + scripts/judge_alpha.py 1288 行 + vendor 4 文件 437 行 + references 5 文件 + data/forum_corpus 21 篇 + rubric JSON）

**定位**：S5 “参考评审层”——PPA 主题/相关性人工核对清单、value-factor trend score、多候选点塔排序。**不作提交判定、不执行提交**（2026-08-31 判定权移交 `submit_verdict`）。

**总评**：这是一个**“已降级但没有拆干净”的 skill**：头部反复声明“参考层、非判定、不提交”，正文骨架仍是旧版“两道硬闸 + 六步 + 确认后提交”工作流，代码里的真实提交路径（`--confirm-submit` → `client.submit_alpha`）仍然活着。值得保留的是 trend score 的字段定义（🟢，`N/A/P/P_max/S_A/S_P/S_H` 逐项可核对）与 robustness/judge 对照表（结构清晰）。主要风险：①**边界靠散文而非代码**（散文写“已废弃勿用”，脚本仍可 POST /submit，且 vendor 客户端把 201 异步受理报成失败）；②**PPA 闸门与代码/规范相反**（颜色 GREEN vs `PURPLE`；Sharpe≥1.58 会把 Sharpe∈[1.0,1.58) 的合法 PPA 全判 BLOCK；CW 配方推荐已被闸5 拦截的加权混合；`WAIT_THEME_ROTATION` 未实现）；③**`READY` 词汇错配**——路由条件写“`submit_verdict` 返回 READY”，而该工具没有 READY；④同文件 GET /submit 语义两套；⑤点塔排序是 submit-alpha 的逐句拷贝，并共享同样的逻辑错误；⑥LLM 层默认开启、表达式外发无边界说明。

| 阶段（行号） | 书写逻辑 | 职责划分 | 边界界定 | 需情景规范？ |
|---|---|---|---|---|
| frontmatter + 职责边界 + 三职能 + 弃用声明（1–48） | 🔴（同一边界写 5 次） | 🔴（“参考层”vs“硬闸工作流”） | 🔴（提交路径仍可达） | 是 |
| 衔接协议 + 与 robustness 边界（50–72） | 🟢（对照表） | 🔴（执行顺序三版） | 🟡 | 否 |
| 适用范围 + 语料（74–85） | 🟡（建库史） | 🟢 | 🟡（篇数漂移） | 否 |
| 闸门顺序（87–100） | 🟡（无输入/产物） | 🔴 | 🔴（凭据；第 6 步提交） | 是 |
| PPA 附加闸门（102–117） | 🟡 | 🟡 | 🔴（颜色/Sharpe/CW 配方/未实现状态） | **是** |
| LLM 决策层（119–134） | 🟡 | 🟡 | 🔴（外发、默认开启） | 是 |
| 建议要求（136–142） | 🟢 | 🟢 | 🟡（“3 条”“引用”） | 是 |
| trend score（144–172） | 🟢 | 🟢 | 🟡（ATOM 术语、无出口） | 是 |
| 语料 + CLI（174–237） | 🟡 | 🟡 | 🟡（PowerShell/裸 python；模板不一致；notes 无来源） | **是** |
| 确认规则 + 提交路由（238–250） | 🟡 | 🔴 | 🔴（READY 词汇；`--confirm-submit` 仍在） | 是 |
| 点塔优选（252–272） | 🟡 | 🔴（submit-alpha 的拷贝） | 🔴（分档重叠；“差 2 颗一次点亮”） | 是 |
| 提交语义（274–283） | 🔴（GBR 旧口径） | 🔴 | 🔴（与 L42–44 矛盾） | 是 |
| 独立原则 + 参考（285–300） | 🟡 | 🟡（开发者规约） | 🟡 | 否 |

| # | 位置 | 维度·级 | 问题 | 改进建议 |
|---|---|---|---|---|
| JD-01 | L4、L12 | 边界·P1 | description 首句“（参考层·非提交判定）”，末句却写“……或**在明确确认后提交**时使用”与英文触发语 “Before submitting a Regular or PPA alpha…”——用户说“提交/submit”会同时命中 judge、submit-alpha、superalpha 三个 skill，而 judge 正文声明“不执行提交”；description 还内嵌点塔细节（“MEA 本季度不提交”是带日期的区域状态）与 `READY` 词汇，约 480 字。`user-invocable: true` 是全库少见的 frontmatter 键，契约（INDEX）里未说明含义 | description 收敛为“提交前的参考评审（PPA 主题核对 / trend score / 点塔排序）；不判定、不提交”；删“确认后提交”与 MEA；说明或删 `user-invocable` |
| JD-02 | L23–53、L238–250 | 职责·**P1** | 同一条边界写了 **5 次**：职责边界（L25–27）、“三职能…存活的全部价值”（L31–37）、弃用声明（L41）、衔接协议（L52）、确认规则/提交路由（L238–250）；而 L48 又写“本 skill 以**两道硬闸**（平台基线 + PPA 附加闸门）为骨架、按下方『闸门顺序』**六步**执行的工作流处理 Regular 与 PPA alpha”，第 6 步是“仅在用户明确确认后**提交**”——正文骨架仍是旧版“判定 + 提交”工作流，头部才是新版“参考层”。读者自上而下会先建立“硬闸工作流”的心智模型，再被 L41 推翻 | 只保留首屏一处边界声明；删 L41 / L48 / L238–242；把正文重排为“三职能各一节”（PPA 核对 / trend score / 点塔排序） |
| JD-03 | L42–46 vs L274–283 | 逻辑·**P1** | **同文件自相矛盾**：L42–44“`GET /alphas/{id}/submit` **恒返回 404**；提交层 403 分支是死代码；唯一真闸 = 确认后 POST 三态”，而 L278–280 的“提交语义（2026-08-11 GBR 战役已验证）”仍写“`GET /submit` → **200** = 最终成功 / **403** = 被拒 / **404** = 记录已清除；唯一可靠信号是 OS 池 ACTIVE”，并称“只接受 200 的 MCP 客户端会误报 `success:false` —— 工具 bug”（现 MCP `submit_alpha` 已处理 201/202）。vendor `ace_client.get_submit_verdict()` 仍按旧口径（POST 后 GET）实现。同一端点，本文两种说法（submit-alpha 一种、superalpha 又一种，共四种） | 删 L274–283 整节；vendor 客户端标 deprecated 或删除；全库只保留“GET 恒 404（REGULAR）”这一口径（并对 SUPER 单列，见 SP-11） |
| JD-04 | L46、L114、L278 | 边界·P2 | 提交后翻转延迟三个数：“~40 s 内翻 OS/ACTIVE”（L46）、“等 **4 分钟**后补发”（L114）、submit-alpha“2~3 分钟”；“受理后再次 POST 得到的 403 是‘已提交’拒绝，**不是硬闸失败**”（L46 ②）与 superalpha Step 3“再调一次 → 回带 PROD/SELF 的 verdict，403 = FAIL”**语义相反**（可能因 type 不同或因是否已翻转）。**“二次 POST”在 REGULAR / SUPER / 补发三种场景含义不同**，全库无一张状态机表 | 建全库唯一的“提交状态机”（REGULAR / SUPER × POST 次序 × 响应 × 含义 × 下一步），judge 只引用 |
| JD-05 | L55–72 | 职责·**P1** | robustness 与 judge 对照表（核心问题 / 判定性质 / 关注指标 / 数据源 / 是否改表达式 / 输出）结构清晰（🟢），但：①judge 被标“**决策性**（READY/REVIEW/BLOCK）”，与 L37/L52“三态仅作参考、不构成提交依据”矛盾；②“执行顺序（硬约束）：explain → robustness（先）→ judge（后）→ 提交路由”，而 robustness SKILL 写“PASS → `submit_verdict` → judge（**可选**参考评审）”（RB-02），AGENTS.md 步 8 为“robustness → submit_verdict → 用户确认 → workflow_submit_alpha”（**链中无 judge**）——**三种链**，judge 依次是必经 / 可选 / 不在链中；③“judge 引用 robustness 的结论作为证据输入”——`judge_alpha.py` 不读取 robustness 输出（无对应字段） | 以 AGENTS.md 为准定一条链，judge 标“可选参考”；删未实现的“引用 robustness 证据”，或实现它 |
| JD-06 | L81–85 | 边界·P3 | “V1 当前包含 20 篇……长超时本地恢复扫描后，剩余 0 条内置搜索快照条目”是**建库过程说明**，非适用范围；篇数已漂移：`data/forum_corpus/` 与 `index.json` 均为 **21** 篇；`generated_at` = 2026-04-12，语料为静态快照，无更新机制，也无来源/授权说明 | 删建库史；篇数写“见 index.json”；补“快照日期与更新方式” |
| JD-07 | L89–93 | 边界·**P1** | “凭据前置”规定读取顺序：`configs/config.json`（含明文 `username/password` 字段）→ 环境变量 `BRAIN_USERNAME/PASSWORD` → **`world-quant-brain-mcp/.env`（`CREDENTIALS_EMAIL/CREDENTIALS_PASSWORD`）** → `~/secrets/platform-brain.json`——4 个来源，其中直接指示读取 `.env`，与 AGENTS.md“凭据位于 `.env`：禁止读取、打印”冲突；`scripts/vendor/load_credentials.py`（79 行）又是一套加载器。“无凭据时自动降级为纯表达式启发式判定”是好的降级说明，但未写**降级后 verdict 必须 ≤REVIEW**（`platform_submit_ok=false` 已使 READY 不可达，此处应明写） | 凭据只走 MCP 会话；vendor 加载器删除或改读 MCP；降级时强制 `verdict ≤ REVIEW` 并在报告首行标“降级” |
| JD-08 | L95–100、L104 | 逻辑·P2 | “闸门顺序”六步没有输入/命令/产物：①“确认 alpha 在基线上可提交”本身是判定（与“不作判定”冲突）；②步 2“若为 PPA（或标签含 PowerPoolSelected）”与 L104“仅当用户明确说明‘仅 Regular’才可跳过”——**何时跑 PPA 闸**有两个触发条件（PPA 标签 vs 默认都跑）；③步 5“视情况运行 LLM 层”——何种情况未说；④步 6“仅在用户明确确认后提交”——本 skill 不提交 | 每步写“输入 / 命令 / 产物字段 / 通过条件”；② 统一为“type=PPA 或标签含 PowerPoolSelected 时运行” |
| JD-09 | L104–117 | 边界·**P1** | PPA 附加闸门与代码/规范不符：①**颜色**：“标签必须含 PowerPoolSelected；颜色为 **GREEN**”，但 `alpha_properties.COLOR_PPA="PURPLE"`（PPA 通道专用色）、submit-alpha 的 PPA 示例用 PURPLE，且“GREEN 须由 OS 结果挣得、禁当默认值”；`judge_alpha.py` 中**无任何颜色校验**（条款无实现）。②**硬指标**：“Sharpe ≥1.58、Fitness ≥1.0、TVR 5–20%、2Y >1.58、CW 通过”是 **REGULAR 内部线**（脚本 `INTERNAL_HARD_GATES={sharpe 1.58, fitness 1.0, two_year 1.58}` 硬编码），而代码对 **PPA 的 failed-count 口径**是 `LOW_SHARPE` **value<1 才计失败** + `PPA_CHECK_NAMES`（turnover / sub-universe / robust / investability），submit-alpha 与 ppa-mining 又称合法 PPA“Sharpe≥1.0”——**judge 会把 Sharpe∈[1.0,1.58) 的合法 PPA 一律判 BLOCK**（`internal_gate_failures → BLOCK`，脚本 L729–733）。③**主题不匹配**“应返回 `WAIT_THEME_ROTATION`”——脚本 verdict 集合只有 READY/REVIEW/BLOCK，该状态**未实现**（全文检索无命中）。④**CW 配方**：“优先 `add(multiply(rank(...), w1), multiply(rank(...), w2))` 并配合 ts_backfill”——实测闸5 的 `_detect_equal_weight_leg_add` **命中该形态**（自 2026-09-13“路线 A”起属被拦截的加权混合，CLAUDE.md“警惕 add(A,B)”），且与 how-to-pass §4“CW 的解是时间平滑、不是换结构”相反。⑤“SELF <0.5（内部严线/PPAC 口径）”把 SELF 与 PPAC（对 power-pool alpha 的相关）混为一谈（selfcorr-quick 分别计算）。⑥“同数据集同腿兄弟 alpha（corr 0.82–1.0）→ BLOCK”——“同腿兄弟”无定义，0.82–1.0 是区间不是阈值；⑦L111–112“真实入口是 `workflow_submit_alpha` / `submit_batch`（`tools_ops.py`）”——MCP 的 `submit_batch` 是“批量提交 alpha 表达式进行回测（POST /simulations）”的**仿真派发**，并非提交 alpha 上平台（SB-24），不应与 `workflow_submit_alpha` 并列为“提交入口” | ①改 PURPLE 并在脚本里实现校验；②PPA 门限取 `config` 的 PPA 口径（`LOW_SHARPE≥1` + `PPA_CHECK_NAMES`），judge 不再套 REGULAR 内部线；③实现或删 `WAIT_THEME_ROTATION`；④删该配方，改引 how-to-pass §4；⑤SELF / PPAC 分列；⑥给定义与阈值；⑦删 `submit_batch` 的“提交入口”表述 |
| JD-10 | L119–134、L217–237 | 边界·**P1** | LLM 决策层：①“Agent 模式：直接使用当前 AI 会话产出 LLM 判定”与“judge 可调用 LLM”——在 agent 会话里 LLM 即 agent 自身，“调用”无对象；“有 LLM 判定时用 LLM 结果，否则回退确定性规则”使 `overall_verdict` 在两种模式下**不可复现**；②“默认开启”：随包 `configs/config.example.json` 是 `llm.enabled=true`、`api_url=https://api.moonshot.cn/v1/chat/completions`、`model=kimi-latest`，而正文示例是 OpenAI + `gpt-4o-mini`——文档与配置模板不一致；③**数据外发**：表达式、checks、trend 块会发往第三方 LLM 端点（`OPENAI_API_KEY` 还会被隐式当作备用 key），全文无“外发哪些字段/禁止外发什么”的说明——alpha 表达式是本项目核心资产；④`api_key` 允许写进 `configs/config.json` 明文；⑤库内 LLM 供应商/密钥配置已至少 4 套（GEM、arxiv 的 DeepSeek、judge、论坛脚本）。安全护栏“`platform_submit_ok=false` 或 PPA 闸失败 → 不能 READY”写了两次（L117、L132）且已在代码实现（`internal_gate_failures → BLOCK`，L1243）——🟢 | 默认 `enabled=false`；列外发字段白名单；key 只走环境；文档示例与模板一致；建“LLM 端点与密钥”唯一登记表 |
| JD-11 | L136–142 | 边界·P2 | “建议必须引用语料/标准证据（帖子 ID 或规则 ID）”“REVIEW/BLOCK 至少 3 条具体行动”：①语料是 21 篇静态论坛帖，许多合理建议（“换数据集”“错开 decay”）没有对应帖子，会被迫**凑引用**；②“最低 3 条”是数量指标，易凑数；③“可执行”未定义 | 建议格式 `{动作, 对象, 预期, 验收}`，证据 id 可选；去掉数量下限 |
| JD-12 | L144–172 | 逻辑·🟢+P2 | 🟢 trend score 字段定义完整（`N/A/P/P_max/S_A/S_P/S_H`；`diversity_score=S_A×S_P×S_H`；仅 `stage=OS`、仅 Regular；ATOM=`SINGLE_DATA_SET`）。P2：①“ATOM=SINGLE_DATA_SET（含 atom 回退）”与 how-to-pass 的 ATOM（“近 2 年 Sharpe 放宽标准”）**不是同一定义**，共用“ATOM”一词；②`S_P=P/P_max` 是**覆盖率**口径，与“点塔优选”的**点亮数（≥3/90 天）**口径并存，两个“金字塔进度”指标互不引用；③乘积在任一因子为 0 时整体为 0，未给典型区间；④报告 delta 与方向之后**没有任何决策用途**（delta<0 时怎么办？）——一个无出口的指标；⑤默认窗口 365 天只在 config 示例里 | 统一 ATOM 术语；说明 trend score（宏观多样性）与点亮数（提交排序）的分工；给决策规则或标“仅信息” |
| JD-13 | L174–215 | 情景·**P1** | CLI 段：①PowerShell 语法（`Set-Location`、`Get-ChildItem`）+ 裸 `python scripts/judge_alpha.py` + `<SKILL_ROOT>` 未定义占位符；②无示例输出（verdict / suggestions / trend 块）、无退出码约定，`outputs/` 是相对路径；③`--input-json` 的候选字段（17 个 notes）只在 `references/extra-standard-rubric.md` 列出，正文未链接；④**`--alpha-id` 模式下 rubric 天生不过**：`evaluate_required_fields` 只检查 `candidate.get(field)` 是否非空文本，而该模式 candidate 只有 `alpha_id` 与平台回填的 `expression`（脚本 L1207–1222），`idea_summary / rationale / stability_notes …` 无任何产出者（不读 `regular.description`、不读 DB）→ `economic_foundation` 恒失败 → verdict 恒 ≤REVIEW；要拿 READY 只能由 agent **自填 notes**（文本非空即通过，可被凑数） | 补“证据字段从哪来”：把 explain-alphas 四段输出与 `regular.description` 三段式映射到 notes；或把 rubric 改为对**可计算指标**（覆盖率、换手、跨 universe 复测记录）的检查 |
| JD-14 | L238–250 | 边界·**P1** | ①“确认规则（已简化：本 skill 不执行提交）……`--confirm-submit` 已废弃，勿再用”——但 `scripts/judge_alpha.py` **仍保留 `--confirm-submit`（L1103）与 `client.submit_alpha(alpha_id)`（L1266；`worth_submit_now` 时真实 POST /submit）**，vendor `ace_client.submit_alpha` 还会在 `Retry-After` 后改用 GET 轮询并以 `status_code==200` 判成功（**把 201 异步受理报为 `submit_failed`**，即 L278 所说“工具 bug”仍在此）。AGENTS.md 称“2026-09-05 起代码里已无提交路径”仅对 workflow_judge 节点成立。**边界靠散文禁止，代码仍可提交**。②“`submit_verdict.py` 返回 **READY** 且用户确认后…”——`submit_verdict` 的标签是 SUBMITTABLE / UNVERIFIABLE / BLOCKED / ALREADY_SUBMITTED，**不存在 READY**（READY/REVIEW/BLOCK 是本 skill 的词汇）；L255“多个 READY 候选时按点塔排序”同样混用：排序输入究竟来自哪个工具？③“参考层 BLOCK 信号（prod_corr≥0.7…）→ 回 optimization-v1 Mode B（prod_corr 反馈循环）”，而 RA 步 5b 规定家族首探 prod≥0.7 即 dead_end、不做变体——第 4 套 prod 墙学说的又一处引用 | ①删除 `--confirm-submit` 与 `submit_alpha`，并加测试断言脚本不含 `POST …/submit`；②路由条件改为“`submit_verdict` ≠ BLOCKED + 用户确认”，排序输入定义为“通过 submit_verdict 的候选集”；③引用 RA 5b 的唯一 prod 墙表 |
| JD-15 | L252–272 | 职责·**P1** | 点塔优选整节是 submit-alpha L196–233 的**第二份拷贝**（三层口径、A/B/C 档、过度提交、UNKNOWN 处理、`GET /data-fields`、`_tower_map.py` 审计注记均逐句重复），且**共享同样的两处逻辑错误**：①分档重叠：A 档“差 ≤2 颗（现状 ≥2/3）”与 B 档“差 2 颗（现状 1/3）”——“≥2/3”= 差 ≤1 颗，而“差 ≤2”包含“差 2”；②“A 档：**一次提交即点亮**”只对差 1 颗成立，差 2 颗的塔一次提交仍差 1 颗（submit-alpha 的 frontmatter 甚至写“差 1-2 颗的塔一次提交即点亮”）。另 L266“已过度提交区域（如 MEA 本季度）”无阈值，且 MEA 通道已关闭（SP-05） | 全库只保留一份（submit-alpha 或独立 `pyramid-priority.md`）；分档改“差 1 颗 / 差 2 颗 / 0-3（差 3 颗）”三档；judge 中删除并链接 |
| JD-16 | L268–272 | 边界·P2 | 同 SB-16/SB-17：“候选将点亮哪座塔”UNKNOWN 无算法；`GET /data-fields/{field}`“列表接口带 search 返回 Invalid query”与 `get_datafields(search=)` 冲突；“`_tower_map.py` 目录不存在”的审计注记再次出现（改错史） | 随 JD-15 一并删除 |
| JD-17 | L285–291 | 职责·P3 | “独立原则：将本 skill 视为自包含；仅从本 skill 目录导入；vendor/ 放运行时辅助；不要依赖 `untracked/`、`untracked/APP/`”是**给开发者的代码规约**，对使用 skill 的 agent 无用；`untracked/` 在仓库中不存在（历史遗留）。vendor 4 个文件（`ace_client`、`auth_utils`、`llm_judge`、`load_credentials`，共 437 行）与主 MCP 代码重复；`judge_alpha.py` 的 `INTERNAL_HARD_GATES` 是内部闸的**第 3 份拷贝**（`config.py`、`submit_queue.LIM`、此处） | 移到 CONTRIBUTING / README；常量改读 `wqb.config`，或给 vendor 加 “GENERATED from …” 标记与同步测试 |
| JD-18 | L293–300、references/ | 边界·P3 | references 5 个文件中 `improvement-roadmap.md`（73 行）与 `future-improvement-guide.md`（179 行）是**规划文档**，agent 运行时不用；`extra-standard-rubric.md`（英文）与 `data/extra_submission_rubric.json`（8 条规则）是同一标准的两种载体，未声明谁是源；rubric 的 17 个 notes 字段在 SKILL 正文无一字；语料引用（TL87739、XX42289、LR93609…）是论坛用户名缩写，出处在 index.json | 规划文档移出；rubric 只留 JSON（md 由其生成）；正文加“证据字段表” |
| JD-19 | 全文 | 情景·**是** | 缺三张情景：①**PPA 候选**（Sharpe 1.2、PPAC 0.42、主题当期匹配）——按现规则 BLOCK，按 PPA 口径应放行：写明用哪套口径；②**多候选点塔排序**：给 3 个候选（塔现状 2/3、1/3、0/3）与各自 fitness，展示排序结果；③**降级运行**（无凭据 / 无 LLM key）：输出是什么、能否作为依据（不能） | 按左列补情景卡（模板见 Part D §D.3.2） |

---

<a id="s31"></a>
### 31. `wq-backtest-monitor`（L6 · 162 行，单文件；章节号从 §5 起，缺 §1–§4、§9）

**定位**：S6 监控复盘——进程/ETA/四关提交审计 + §14 战役台账回写（`wave_results` / `registry_empirical`）。

**总评**：这份文件是**两个时代的叠加**：PPA 时代的“进程监控/效率分析/四关审计/ETA”框架（instance 全是 v52b、tri_track、ds 舰队、`YPgAa3WR`），加上 2026-08 起新增的 §14“战役台账回写”。后者才是当前 S6 真正被下游依赖的部分，且 §14.1 的 verdict 必填（PASS/FAIL/PARTIAL，动机是“133 条 wave 记录 97 条 verdict 为空”的实测）与 §13 的判停参数（60 min STALLED / 360 min TIMEOUT，与 `_lib/poller.py` 逐值一致）是**写得好、可核对的两段**。问题：①**§14.2 的四条命令模板全部与真实 CLI 不符**（缺必填参数、多出不存在的 flag、第 4 条还写入已废止的 `wave<N>_verdict` 键）；②上游把本 skill 定为“OS 表现监控”，**正文没有任何 OS 监控内容**，重着色（BLUE→GREEN/YELLOW/RED）与 OS 衰减回流无承接者（`os_feedback.py` 已归档）；③§7 的“universe 合法性”与 `config.REGIONS` 相反（EUR 默认 TOP2500 被写成“非法”）；④§11 把已不存在的历史任务写进强制输出格式；⑤被删章节的“attic 归档”实际不存在。

| 阶段（行号） | 书写逻辑 | 职责划分 | 边界界定 | 需情景规范？ |
|---|---|---|---|---|
| frontmatter + 铁律 + 边界 + 衔接（1–44） | 🟡（铁律置于 H1 前） | 🔴（PPA 定位 vs S6 全局；OS 监控缺失） | 🔴（“进程枚举必须/仅故障时”） | 是 |
| §5 四关（46–55） | 🟡 | 🔴（第 4 套闸门分类） | 🔴（OOS 关无对应物；阈值） | 是 |
| §6 并发（57–62） | 🟡 | 🔴（与 wqb-concurrency 重复） | 🔴（数值不一） | 否 |
| §7 工作纪律（64–71） | 🟢 | 🟡 | 🔴（universe 合法性错） | 否 |
| §8 产出物（73–80） | 🟡 | 🟡 | 🟡（快照标注遗漏） | 否 |
| §10 提交核查（82–98） | 🟡 | 🟡 | 🔴（“待提交”未定义；旧 checkpoint 字段） | **是** |
| §11 ETA（100–110） | 🟢（公式） | 🟡 | 🔴（历史任务写入强制格式） | **是** |
| §12 报告结构（112–121） | 🔴（“§n”双义） | 🟡 | 🔴（悬空引用） | 是 |
| §13 判停（123–127） | 🟢 | 🟢 | 🟡（多套卡住阈值） | 否 |
| §14 台账回写（129–162） | 🟡 | 🟡 | 🔴（命令 4/4 错；旧键；无回写命令） | **是** |

| # | 位置 | 维度·级 | 问题 | 改进建议 |
|---|---|---|---|---|
| BM-01 | L3–4、L26、L28–32；submit-alpha L35、superalpha L40 | 职责·**P1** | description 与 H1 把本 skill 定位为“WorldQuant BRAIN **PPA** alpha 挖掘任务的监控/盘点/效率分析”“WQ PPA 挖掘·监控/验证/并发框架”，但 INDEX 与 submit-alpha/superalpha 的衔接协议把它定为**所有 REGULAR/PPA/SUPER 的 S6 阶段**（“OS 表现监控；§14 台账回写”）。正文实质是 PPA 时代的进程监控 + 后加的 §14，**两个职责压进一个文件**；上游说它做“OS 表现监控”，而正文**没有任何 OS 监控内容**：无 OS Sharpe 衰减判据；`alpha_properties` 定义了 `COLOR_HEALTHY/DEGRADED/TO_RETIRE`（GREEN/YELLOW/RED，“GREEN 须由 OS 结果挣得”），但**没有任何 skill 规定谁在何时依何判据改色**；唯一相关脚本 `os_feedback.py`（OS 回流 / G3 学习闭环）已于 2026-09-28 归档为“零引用”，toolkit SKILL L141–145 却仍将它列为活跃工具（TK-07）。**S6 的“OS 表现监控”职责没有承接者** | 拆为 `ops-monitor`（进程/ETA/四关审计，仅故障排查）与 `s6-ledger-writeback`（§14）；另立“OS 监控与重着色”规则（判据 + 工具 + 写回键），或明确删除该承诺并同步 INDEX/submit-alpha/superalpha 的衔接措辞 |
| BM-02 | L15–17；§10 L89–92；§13 L127 | 逻辑·P2 | “持久化铁律（DB 单轨）”置于 frontmatter 之后、H1 之前，且在多个 skill 里逐字重复；与本 skill 自己的取证来源冲突：§10 的“取证方式”全是 checkpoint 文件字段（`results[].status`、`found_alphas[]`），§13“进度取证 = `<campaign>/results/pipeline_<wave>_checkpoint.json`”——而铁律禁止把 `results/*.csv` 等当**交接真相源**，checkpoint 算不算未澄清 | 铁律缩为一句 + 指针；明确“checkpoint = 运行态证据（可读、不作交接）”；四关审计改读 `backtest_results`/`alphas` 表 |
| BM-03 | L28–32、L129–139 | 职责·P2 | 边界“负责：…§14 台账回写”，同时“**不是** `wave_results`/`registry_empirical` 的正式写入方——唯一正式写入 = toolkit 幂等 CLI；MCP 直写仅作逃生阀”；§14 标题却写“战役模式下**强制**”回写。“负责回写”与“不是写入方”是同一件事的两种措辞（本 skill 是**触发者**，写入方是 toolkit CLI）；写失败时谁负责重试未说（同 TK-03 的“唯一正式写入方”争议） | 改为“本 skill 负责**触发并核验**回写；写入由 toolkit CLI 执行”；补写失败处置 |
| BM-04 | L36、L43–44、L71 | 逻辑·**P1** | 三处对“机器级进程枚举”的要求互相矛盾：L36“当用户要盯回测/盘点…按下述框架产出**完整分析**”；§7 #6“监控第一视角：**必须**机器级进程枚举为发现入口”；L43–44“日常战役由 pipeline 托管……进程枚举/并发模型/效率分析/盲区排查**仅故障排查时执行**（`Get-CimInstance Win32_Process` 全量枚举为发现入口；分类与五类盲区细节**已删**，需要时查 attic 归档）”。且 `Get-CimInstance Win32_Process` 是 **Windows/PowerShell 专属**，在 Linux 环境（本次会话）无对应命令；“attic 归档”**不存在**：`attic/` 只有 `ra_pipeline_shell_20260928` 与 `toolkit_zero_ref_20260928`，没有监控分类/盲区内容——**被删内容既不在文中也不在归档**（仅 git 历史可找） | 定一个默认：日常 = 读 checkpoint/DB；故障排查 = 进程枚举（Windows 与 Linux 各给一条命令）；attic 指针改为 commit 哈希或补归档 |
| BM-05 | L46–55（§5）、L86–98（§10） | 职责·**P1** | “四关”（① 研究仿真 IS 廉价闸 ② 生产仿真 OOS ③ 生产相关性 ④ 平台 submittable + 真实提交）是全库**第 4 套闸门分类**（gate.py 闸 1–8/9 + INDEX 编号、RA 九步、`submit_verdict` 提交层视图、INDEX“廉价闸→PC 等待→硬闸”，再加此处的“关”）。②“生产仿真 OOS 样本外稳健 ❌ 未跑”——平台**没有**“提交前的生产仿真 OOS”，OS 仅在提交后产生，此关无对应工具/字段，“本链现状：未跑”永远为真；①的阈值“S>1.58 / F>1.0 / **TVR∈[0.05,0.30]** / M>10bp / Ret>0.05”与 `config.GATES_INTERNAL`（turnover **(0.05, 0.20)**）不符（0.30 vs 0.20，全库换手区间第 5 个取值）；“近闸”未定义；③④“本链现状”写的是历史快照（“仅 1 个 `YPgAa3WR`（prod_corr=0.5325）”“0 个，no_submit=True”）。§10 又原样再写一遍四关（重复，且都带 `YPgAa3WR` 实例） | 删“关”体系，映射到唯一的 RA 步骤 / `submit_verdict` 标签；阈值引用 config；快照移入案例 |
| BM-06 | L55 | 边界·P3 | “取证函数 `collect_verified_pids()`（取 `found_alphas` 的 pid）”——全库检索仅此一处，函数不存在；`found_alphas` 是 v52b 时代 checkpoint 字段 | 删除 |
| BM-07 | L57–62（§6）；INDEX L286–291 | 职责·**P1** | “并发模型·Token-Bucket（C=7）”与 `wqb-concurrency`（L3）重复；核对 `config.CONCURRENCY = {slots 7, burst_capacity 7, safe_instant_submits 6, min_batch_interval_sec 45, refill_sec_per_token (20,40)}`：本节数值（C≈7、≤6、批间 ≥45 s、20–40 s/令牌）**与 config 一致**，问题是**抄写而非引用**（违反 INDEX 硬裁定①“skill 只能引用权威常量”），并夹带 config 之外无来源的数字（“持续高频需 ≥15–20 s 间隔”“≤10 路零 429”）。并发参数的**来源有三处**：`config.CONCURRENCY`（INDEX L153 称唯一）、`wqb-concurrency` §8、以及 INDEX L289 把“新模型”出处写成本节（§6）；他处仍残留旧 C=5。同段“提交”指**仿真派发**（非提交 alpha，术语过载）；“当前真正瓶颈 = 信号发现不是吞吐”是带时点的现状判断，混在规则里 | 删除本节，指向 `config.CONCURRENCY` 与 wqb-concurrency 的唯一参数表；INDEX L289 的出处改指 wqb-concurrency；“瓶颈”类判断移到复盘报告 |
| BM-08 | L64–71（§7） | 边界·**P1** | 工作纪律 6 条：①“universe 合法性：TOP500/1000/2000/3000 合法；**TOP800/1500/2500/5000 非法**（400 拒）”与 `config.REGIONS` **相反**：EUR 的 universes = `[TOP2500, TOPCS1600, TOP1200, TOP800, TOP400]`，**默认就是 TOP2500**；KOR 默认 TOP600、CHN 为 TOP2000U、ASI 为 MINVOL1M / MINVOL10M / TOP500——按此条 agent 会拒绝合法 universe；②“转向时机：超 10 种不同结构仍无满意效果才转向”与 RA 停止规则 A/B1/B2、optimization-v1“>10 种结构无果 / 3–5 周期”是**并列的多套止损线**；③“label 碰撞：用完整字段名”“断点续跑：只把拿到 pid 的确定结果算已完成”是好规则（🟢），但源自 v52b 的实现细节；④#5“PASS_CHEAP 不得称可提交”在 §5、§10 已出现，共 3 次 | universe 取 `config.REGIONS[region].universes`；止损线引用 RA 唯一表；#5 合并 |
| BM-09 | L73–80（§8） | 边界·P2 | ①“新监控脚本应在 `tools/` 按**统一规范**新建”——规范未给；②“红线：绝不动在跑进程的 checkpoint 与脚本（如 v52b …）”是好红线（🟢），但示例是历史任务，应泛化为“status=RUNNING 的战役其 checkpoint/脚本不得修改、移动、删除”；③L80“历史快照标注（2026-09-12）：本节及 §11/§12 …是快照，勿复用”——范围**遗漏 §5、§10**（同样含 `YPgAa3WR`），且与 §11 输出格式“包含 ds 舰队全部 7 路 + tri_track + v52b”自相矛盾（BM-11） | 红线泛化；快照标注覆盖全文，或把实例全部移出规则区 |
| BM-10 | L82–98（§10） | 情景·**P1** | “提交核查（强制章节，每次汇报不可省略）”：①三级分类“✅ 已正式提交 / ✅ 回测完成待提交 / 🔶 仍需进一步验证”，但“**回测完成待提交**”未定义，且与“PASS_CHEAP ≠ 可提交”冲突——应映射到 `submit_verdict` 标签（UNVERIFIABLE + prod 实测 <0.7 才算“待提交”）；②“取证方式”全是 v52b 时代 checkpoint 字段（`status = PASS_CHEAP / CHECK_PENDING`、`found_alphas[]`、脚本 `no_submit`），当前数据在 `backtest_results`/`alphas`；③固定句式“N 个候选，0 已提交，0 待提交，N 个仍需验证”可检（🟢），但同段把“`YPgAa3WR` 最接近者，仍需 3 项”写进规则；④“强制、不可省略”而 §5 又称“仅故障排查时执行”，强制程度不一 | 分类映射到 `submit_verdict` 标签；取证改读 DB；句式保留，删实例；强制程度统一 |
| BM-11 | L100–110（§11） | 情景·**P1** | “ETA（强制章节，每次汇报不可省略）”的输出格式要求“包含 **ds 舰队全部 7 路 + tri_track + v52b**”——这些是 2026-09 前的历史任务（L80 自己说“勿复用具体数字/任务名”），新战役里不存在，agent 会去找不存在的进程/日志，或编造。通用部分（remaining ÷ (done ÷ elapsed) → +now → `MM-DD HH:MM`；置信度 <30 min 低 / 30–60 中 / >60 较高；开放型任务报吞吐）🟢 可用，且与 §13“剩余批数 × 单批平均耗时”一致；但 ETA 与 §13 熔断（60 min 无进度 = STALLED）**没有联动**（ETA 已超阈值时怎么报？） | 输出格式改为“对每个在飞的 campaign wave 一行”；ETA 与 STALLED 联动：无进度超过 `stall_minutes` 时 ETA = “已挂起” |
| BM-12 | L112–121（§12） | 逻辑·**P1** | “标准报告结构（**唯一标准依据**）：§1 背景 / §2 分析维度 / §3 核心发现 / §4 结论与建议”，其中 §2 又写“进程盘点（§1–§2）/ 并发进度（§2）/ 效率结论（§3）/ 四关审计（§10）/ ETA（§11）/ 监控盲区（§4）”——**“§n”同时指本 skill 的章节号与报告的章节号**，且 skill 的 §1–§4 已删除（本文件从 §5 起，缺 §1–§4、§9），引用悬空；“唯一标准依据”“不得自创结构”是全库又一处“唯一”宣称。`allowed-tools` 仅 `Read/Bash/Grep/Glob`，而 §14 强制调用 `mcp__wqb-db__*` 与 toolkit CLI，未在 frontmatter 声明 | 报告章节改编号 R1–R4；删悬空引用；frontmatter 补 `mcp__wqb-db__*` |
| BM-13 | L123–127（§13） | 边界·🟢+P2 | 🟢“判停依据 = poll 熔断参数组：progress 60 min 无变化判 STALLED、总超时 360 min（可被 thresholds.json `poll` 节覆盖）”与 `_lib/poller.py`（`stall_minutes=60 / timeout_minutes=360`）**逐值一致**；“`STALLED/TIMEOUT` 即判停，不等‘看起来没动静’”“进度取证 = 批级 checkpoint，不是终端 tail”均可执行。P2：全库另有 3 分钟级卡住阈值（wqb-concurrency / poll-and-quota 的异步卡住系列，见综合 X-Q），与此 60 min 并存；“归入 SCAN/MINING 分类”依赖已删的分类（BM-04） | 建一张“等待/卡住阈值表”，此处引用 |
| BM-14 | L148–160（§14.2） | 边界·**P1** | **命令模板四条全部与真实 CLI 不符**（核对 `_lib/wave_results.py`、`_lib/registry.py`、`_lib/ledger.py`）：①`wave upsert --wave $W --verdict PARTIAL --extra @notes.json`——`wave upsert` **没有 `--extra`**（有 `--focus/--context/--verdict/--status/--finding/--candidates/--batches/--region/--dry-run`）；②`registry add-dead-end --extra @dead.json`——该子命令**必填** `--id --family --reason --rule`，模板只给 `--extra` → argparse 缺参报错；③`registry add-win --extra @win.json`——必填 `--id --what --key`，同样缺；④`ledger set-verdict --wave $W --verdict PARTIAL`——真实签名 `set-verdict <wave> --json <json|@file>`（wave 为位置参数，无 `--wave/--verdict`），且它写入的是 **`wave{W}_verdict` 键——即 RA 已于 2026-09-28 声明废止、不再双写的旧键**（本文是第 5 处仍教旧键的文档，另 4 处：ra-campaign-prompt、decision-table D8、ledger-schema、dataset-mining-experience）。🟢 §14.1 的 verdict 枚举 `PASS/FAIL/PARTIAL` 与 `VERDICT_OK` 一致，“133 条中 97 条为空”的实测动机写得清楚；`get_wave_result` 自检也对 | 模板按真实 CLI 重写（每条带必填参数并先 `--dry-run`），删第 4 条；加机械检查：skill 内 fenced 命令的 flag 必须能被目标 argparse 解析（本次 checker D 已能覆盖） |
| BM-15 | L136–139（§14 项 4） | 边界·P1 | “方法论规则计数：若本波消费了 `tracking/<REGION>/reference/methodology_rules.json` 的 active 规则，回写 `times_applied +1`；达标再 `times_succeeded +1`，`confidence` 按成功率更新”——文件确实存在（EUR/GBR/IND…），`_lib/rules.py` 也有这两个字段，但 §14.2 **无任何回写命令**、无 confidence 更新公式；“不回写即等同未消费”是对读者的责任要求却无可执行手段；且这是**文件产物**（`tracking/…/*.json`），与“DB 单轨”不一致 | 给回写命令与公式（如 (succ+1)/(app+2)）；或把规则表迁入 DB |
| BM-16 | L131–135（项 1–3）；INDEX L382 | 职责·P2 | 三条写入路径并列：toolkit CLI（战役目录内）/ `mcp__wqb-db__upsert_*`（无战役目录）/ `upsert_ledger_key`（“如 submit_ready 增量”）——其中 `submit_ready` 键已有**多个写入方**：RA 步 7→8（INDEX L382）、`campaign.py ledger submit-ready`、本文项 3，而 `submit_queue` 里又有**同名 SQL 表** `submit_ready`（键与表同名不同物），无所有权说明 | 建 ledger-key 目录（键 / 写入方 / 读取方），本文只写“wave_results + registry_empirical”两类 |
| BM-17 | L159–162 | 逻辑·P3 | L159“中文/JSON 参数一律走 `@file` 文件通道（AGENTS.md §5）”，但 `@notes.json` 等文件写到哪里未说（战役目录？scratch？）；与 L17“Agent 禁止 Write 这些文件”（仅指 `final_expressions.json` 等）适用范围易混；末行“修改报告结构前先与用户确认”孤悬在代码块之后，属 §12 却出现在 §14.2 末尾 | 指定临时文件目录与清理；末行移到 §12 |
| BM-18 | 全文 | 情景·**是** | 缺三张情景：①**日常一波收尾**（pipeline 完成 → `review_wave` → `wave upsert --verdict` → `get_wave_result` 自检非空）的完整命令序列（用真实 flag）；②**挂起处置**：poll 60 min 无进度 → STALLED → 判停 → 记录 → 是否重提（引用 wqb-concurrency）；③**汇报样例**：一份 20 行以内的合规报告（四层骨架 + 提交核查三级表 + ETA 表）——“强制章节”目前只有描述没有样例 | 按左列补情景卡（模板见 Part D §D.3.2） |

---

<a id="s32"></a>
### 32. `planning-with-files`（L7 · SKILL.md 221 行 + reference 218 + examples 202 + 3 个模板 + 2 个 bash 脚本）

**定位**：Manus 风格的文件化规划（`task_plan.md` / `findings.md` / `progress.md`）——通用元技能，声明“不涉及任何 WQ 平台调用、不是挖掘链的一环”。

**总评**：内容本身是**好的通用工作法**：“上下文 = 内存、文件 = 磁盘”的核心模式、读/写决策矩阵（6 场景 × 动作 × 原因）与“五问重启测试”（我在哪 / 去哪 / 目标 / 学到什么 / 做了什么 ↔ 答案来源）清晰可执行，且天然契合“上下文被压缩后恢复”。疑为外部开源 skill 的中文化版本（“Manus 风格”“version 2.1.0”“hooks + templates + scripts”结构），**带着自己的钩子与绝对化规则被放进了一个有 DB 单轨、领域重试协议、独立停止规则的库**，于是出现四类冲突：①frontmatter 里的 4 个 shell 钩子（其中 Stop 钩子含未解析占位符，**任何宿主都不可能成功执行**）；②触发条件“>5 次工具调用”使它几乎对所有 WQ 任务自动激活，并以“没有商量余地”凌驾于领域流水线；③“永不重复失败的动作”与 WQ 规定的重复动作（429 退避重试、空体轮询、异步补发 re-POST）冲突；④INDEX 把 `hooks` 列为可选键却没有任何审查规则。

| 阶段（行号） | 书写逻辑 | 职责划分 | 边界界定 | 需情景规范？ |
|---|---|---|---|---|
| frontmatter + hooks（1–36） | 🔴（占位符未解析） | 🔴（钩子 = 自动执行的 shell） | 🔴 | 是 |
| 职责边界（40–44） | 🟢 | 🟡 | 🟡（“共用 `$WQ_PY`”不成立） | 否 |
| 文件放哪里 + 快速上手（48–74） | 🟢 | 🟢 | 🟡（仓库根/忽略/DB 单轨） | 是 |
| 核心模式 + 文件用途（76–91） | 🟢 | 🟢 | 🟢 | 否 |
| 关键规则 1–6（93–128） | 🟡 | 🟡 | 🔴（“绝不”“没有商量余地”） | 是 |
| 三次失败协议（130–152） | 🟢 | 🟡 | 🟡（与 RA 停止线并存） | 是 |
| 读/写矩阵 + 五问（154–175） | 🟢 | 🟢 | 🟢 | 否 |
| 何时使用（177–189） | 🟡 | 🟡 | 🔴（三个触发口径） | 是 |
| 模板/脚本/高级（191–209） | 🟡 | 🟢 | 🟡（bash vs PowerShell） | 是 |
| 反模式（211–221） | 🟢 | 🟡 | 🟡（TodoWrite） | 否 |

| # | 位置 | 维度·级 | 问题 | 改进建议 |
|---|---|---|---|---|
| PW-01 | L17–36；scripts/check-complete.sh | 边界·**P1** | frontmatter 内嵌 4 类 shell 钩子：SessionStart / PostToolUse 的 `echo`；PreToolUse（匹配 `Write\|Edit\|Bash`）`cat task_plan.md 2>/dev/null \| head -30 \|\| true`；Stop 钩子 `<SKILL_ROOT>/planning-with-files/scripts/check-complete.sh`。①**Stop 钩子命令含未解析占位符**：`tools/sync_skills.py` 不做 `<SKILL_ROOT>` 替换（全库检索无此逻辑），实测 `bash -c '<SKILL_ROOT>/planning-with-files/scripts/check-complete.sh'` → `SKILL_ROOT: No such file or directory`——该钩子**在任何宿主都无法成功执行**；②`check-complete.sh` 在无 `task_plan.md` 时 `exit 1` 并打印 “ERROR … Do not stop until all phases are complete”，对非规划任务的每次 Stop 都产生错误噪声；且宿主约定里 exit 1 是**非阻塞错误**（阻断需 exit 2），脚本意图（“不完成不许停”）与执行语义不符；③PreToolUse 在每次 Write/Edit/Bash 前把计划文件前 30 行注入上下文（有计划文件时的固定成本，在 RA 长流程中每次工具调用一次）；④全是 POSIX（`cat`、`head`、`2>/dev/null`、`.sh`），而项目主宿主是 Windows/PowerShell（INDEX 的 `$WQ_PY` 指向 `Scripts\python.exe`）——PowerShell 下 `2>/dev/null` 直接报错；⑤INDEX 把 `hooks` 列为可选 frontmatter 键，**没有任何审查规则**，而钩子等同于自动执行的任意命令 | 修正或删除钩子（去占位符、路径解析、PowerShell 等价、阻断用 exit 2）；INDEX 增“skill 含 `hooks` 必须在边界段声明其行为并经人工审查”（见 PB-01） |
| PW-02 | L5、L40–44、L96、L177–189 | 边界·**P1** | 触发条件三个口径：description“需要 **>5 次工具调用**的任务”、正文“多步任务（**3 步以上**）/任何需要组织规划的任务”、SessionStart 提示“Auto-activates for complex tasks”。按“>5 次工具调用”，**几乎所有 WQ 任务都满足**（RA 九步、一次波收尾……），于是该 skill 会在几乎每个任务自动激活，并以“**没有 `task_plan.md` 绝不开始复杂任务。没有商量余地。**”（L96）凌驾于 RA 流水线（其状态在 DB 台账）之上；边界段称“与 WQ 链仅共用运行环境约定（`$WQ_PY`）”，但全文**无一处使用 `$WQ_PY`**，也没有优先级规则（计划文件 / 台账 / 用户当次指令谁优先） | 触发改为“用户明确要求 / 跨会话任务 / 无现成状态存储且步数 >N”；写优先级：用户指令 > 领域协议 > 本 skill；DB 台账为结果真相源，规划文件只记过程与决策 |
| PW-03 | L98–101、L123–128、L138–141 | 边界·**P1** | “两动作规则”（每 2 次查看/浏览/搜索就写文件）与“**永不重复失败**：`if action_failed: next_action != same_action`，绝不重复完全相同的失败动作”（三次失败协议第 2 条同）是面向浏览/研究类任务的规则；套到 WQ 运维上直接冲突：429 退避后**同一请求重试**、`GET /correlations/prod` 空体轮询、异步受理后的 **re-POST 补发**（submit-alpha 关键坑 #1 ②③）、`PENDING` 等待，都是各 skill **规定的重复动作** | 区分“确定性失败（同参数必再败）不重复”与“暂时性失败（429 / 空体 / PENDING / 异步未就绪）按各 skill 协议重试”，并列出 WQ 场景的例外 |
| PW-04 | L50–62、L74 | 边界·P2 | “规划文件应创建在项目目录（当前工作的文件夹）”：WQ 仓库 `.gitignore` 只忽略**仓库根**的 `/task_plan.md`、`/findings.md`、`/progress.md`；在 `tracking/<REGION>/` 等子目录工作时会产生**未被忽略**的文件，污染 `git status`（AGENTS §7 明令避免混入半成品）。DB 单轨铁律（INDEX L35）是否允许这些文件，本文与 INDEX 都未明写（它们是过程笔记，应允许，但需声明“规划文件 ≠ 战役产物”）；云端/受限会话应写 scratchpad | 指定固定位置（仓库根或 `.planning/`，写入 .gitignore）；铁律里加一句豁免 |
| PW-05 | L130–152 | 边界·P2 | “3 次失败后：上报给用户”与 RA 停止规则 A/B1/B2、optimization-v1“>10 种结构 / 3–5 周期”、monitor“>10 种结构才转向”、submit-alpha 的补发协议是**并列的多套“失败几次怎么办”**；本 skill 是通用版，未说明与领域规则冲突时以哪个为准；“失败”的粒度（一次工具调用？一次 wave？一次构造？）未定义 | 声明“领域协议优先”；定义失败粒度 |
| PW-06 | L154–175 | 逻辑·🟢 | 🟢 读/写决策矩阵与“五问重启测试”是全文最可执行的部分，直接对应“压缩后恢复”；表述短、判据明确（“刚写完文件 → 不要读”“间隔后恢复 → 读取所有规划文件”） | 给一个 WQ 场景的填好示例（如“RA 步 4 GEM 生成中断后恢复”：五问的答案各来自哪个文件/台账键） |
| PW-07 | L191–209、scripts/、templates/ | 情景·P2 | 脚本为 bash（Windows 主宿主需 Git Bash/WSL，未说明）；模板阶段是软件开发通用阶段（“Requirements & Discovery / Planning & Structure / Implementation”），**没有 WQ 战役阶段（S-PRE…S6 / 九步）的映射**；`check-complete.sh` 以 `### Phase` 与 `**Status:** complete` 字符串计数，与模板文本强耦合，用户改格式即失效 | 提供“一次 RA 战役”的示例 task_plan（阶段 = 九步 + 每步落 DB 的检查点）；脚本改 Python 或双实现 |
| PW-08 | L211–221 | 边界·P2 | 反模式“用 TodoWrite 做持久化 → 创建 `task_plan.md`”：宿主提供 Task 工具（TaskCreate/TaskUpdate）并要求维护任务清单，二者是**互补**（会话内跟踪 vs 跨会话持久化），本文写成互斥；“把所有东西塞进上下文 → 存文件”与 DB 单轨并存时，应指向 DB 而非 md | 改写为“会话内用 Task 工具，跨会话状态用文件/DB” |
| PW-09 | L2–6 | 边界·P3 | `version: "2.1.0"`（外部来源版本号，与本库“内容版本递增”的关系未说）；来源、许可与上游同步策略未标（疑为外部开源 skill 的中文化）；`user-invocable: true` 语义未在 INDEX 契约定义 | 加 `source:` 与许可注记；INDEX 契约补 `user-invocable`/`version` 语义 |
| PW-10 | 全文 | 情景·**是** | 缺三个 WQ 情景：①**一次 RA 战役**的 task_plan（九步阶段 + 每步产物写 DB 的检查点）；②**长任务被压缩后恢复**：五问 → 读 task_plan → 读台账（`get_wave_result`）→ 继续；③**用户说“直接改，别写计划”**时怎么办（“没有商量余地”与用户当次指令冲突） | 按左列补情景卡（模板见 Part D §D.3.2） |

---

<a id="s33"></a>
### 33. `pull-brain-skills`（L7 · SKILL.md 68 行 + scripts/pull_skills.py 186 行）

**定位**：从 ZIP URL / Git 仓库 / 本地目录导入含 `SKILL.md` 的 skill 文件夹。

**总评**：篇幅最短，但**风险最高**——它是**外部内容进入运行时指令与可执行物的入口**：skill 的 SKILL.md 被当作指令执行、被 GEM 拼进 LLM prompt，其 `scripts/` 可被运行，frontmatter 的 `allowed-tools` 授予 Bash，`hooks:` 会在每次工具调用/停止时执行 shell（`planning-with-files` 即带 4 个钩子）。文档却**没有任何入库前审查**，推荐示例默认 `--overwrite`（脚本对同名目录直接 `shutil.rmtree`），且**文档与代码的默认目的地相反**（SKILL 称默认 `Claude/skills/`，脚本是 `<cwd>/.qoder/skills`）。

| 阶段（行号） | 书写逻辑 | 职责划分 | 边界界定 | 需情景规范？ |
|---|---|---|---|---|
| frontmatter + 职责边界（1–28） | 🟡 | 🟡（缺最关键的“不做”） | 🔴（“有效 skill”定义弱） | 是 |
| 使用方法（30–58） | 🟡 | 🟡 | 🔴（默认 `--overwrite`；默认目的地） | **是** |
| 行为（59–62） | 🟡（只描述 Git 路径） | 🟢 | 🟡 | 否 |
| 注意事项（64–68） | 🟡 | 🟡 | 🔴（无安全审查；命名只警告） | **是** |

| # | 位置 | 维度·级 | 问题 | 改进建议 |
|---|---|---|---|---|
| PB-01 | 全文 | 边界·**P1（安全）** | 导入外部 skill = 向运行时注入**指令与可执行物**，本 skill **没有任何入库前审查步骤**：不列 `hooks` / `allowed-tools` / `scripts/*` 清单，不检查危险模式（读取 `.env` / `~/.ssh` / credentials、`curl\|wget\|requests.post` 外发、`rm -rf`、`eval`），不与既有同名 skill 做 diff；“导入不校验 layer/命名/frontmatter”把校验全部推给事后 `pytest`，而该测试只查**格式**，不查**内容安全**。边界段也缺最关键的一条“不做：不执行被导入 skill 里的任何脚本 / 钩子” | 加“导入前审查清单 + 隔离目录（`--dest` 默认 `attic/import_staging/`，人工确认后移入）+ 输出 diff 报告”；出现 `hooks`、`allowed-tools: Bash`、`scripts/` 时强制人工确认 |
| PB-02 | L39–41、L57；脚本 `copy_skill_folder` | 边界·**P1** | “首选推荐”的示例 1 默认带 **`--overwrite`**；脚本对已存在目录先 `shutil.rmtree(dest_folder)` 再复制——**无备份、无确认、无 diff**，同名 skill（含 `wq-brain-ra-pipeline` 等核心 skill）会被外部同名目录静默替换 | 示例默认不带 `--overwrite`；覆盖前打印将删除的目录与文件数并要求 `--yes`；先备份到 `attic/` |
| PB-03 | L55、L62、L22；脚本头部与 `main()` | 边界·**P1** | **文档与代码默认目的地相反**：SKILL 写“`--dest` 默认 = 仓库真相源 `Claude/skills/`（导入后须跑 `sync_skills.py`）”，而 `pull_skills.py` 的 docstring 与 `main()` 都是 `dest = <cwd>/.qoder/skills`（该目录在仓库中不存在，INDEX 质量门禁还明令“无已废弃路径引用 `.qoder/skills/`”）。照文档执行的 agent 会以为技能已落在 `Claude/skills/`，实则在 CWD 下的 `.qoder/skills`，`sync_skills.py` 不会拾取 | 以代码为准改文档，或改代码默认值；加测试断言两者一致 |
| PB-04 | L38；脚本 ZIP 分支 | 边界·P2 | ZIP 地址“在仓库 URL 后追加 `/archive/refs/heads/main.zip`”：①假设默认分支是 `main`（`master` 仓库 404）；②分支头是**可变引用**，同一 URL 前后两次下载内容不同，无法复现与审计（应固定 commit SHA：`/archive/<sha>.zip`）；③`--branch` 只对 Git 模式生效，对 ZIP/本地目录被忽略（文档未说）；④`urlretrieve` 无超时/大小上限/校验和 | 示例改固定 SHA；写明 `--branch` 适用范围；加超时与大小上限 |
| PB-05 | L4、L28、L67；脚本 `main()` | 边界·P2 | “有效 skill”只要求“顶层文件夹里有 SKILL.md/skill.md”，比本库契约（name==目录名、layer、last_verified、职责边界段、kebab-case）弱得多；脚本在 `copied` 为空时仍 `ok: true` 退出 0——GitHub 上多数 skill 仓库把 skill 放在 `skills/<name>/` 二级目录，脚本**只扫顶层**，此类仓库必然 **0 导入且“成功”**；脚本注释“copy_skill_folder is case-sensitive on purpose”与实际大小写不敏感的检查矛盾 | `copied` 为空 → 退出码非 0 并提示“未找到顶层 skill，请指向含 SKILL.md 的子目录”；支持 `--subdir`；校正注释 |
| PB-06 | L21、L64–68 | 情景·P2 | “导入后必须人工归层并跑 `python tools/sync_skills.py` + `pytest tests/unit/test_skill_integrity.py -q`”：①“归层”无指引（如何选 layer、补 `last_verified`、补“职责边界”三条、改名 kebab-case）——只有一段“命名警告”；②命令用裸 `python`（应 `$WQ_PY`）；③未提 `test_skill_boundaries.py`（新 skill 缺边界段“不予合入”）；④命名警告写“应警告并建议迁移名，不自动重命名”，但“如何建议”无规则；⑤**无回滚方式**（导入错了怎么撤） | 加 6 行“导入后清单”（归层 / frontmatter / 边界段 / 命名 / 安全审查 / sync + 测试）与回滚命令（`git checkout -- Claude/skills/<name>` 或删除新目录） |
| PB-07 | 全文 | 情景·**是** | 缺三个情景：①从 GitHub 仓库导入 1 个 skill 到审查区并生成审查报告（含 hooks/allowed-tools/scripts 清单）；②导入的 skill 与现有同名（想更新）——diff/合并流程；③导入后发现带 `hooks` 或读取 `.env`——处置与拒绝理由记录 | 按左列补情景卡（模板见 Part D §D.3.2） |

---

<a id="s34"></a>
### 34. `Claude/skills/INDEX.md`（架构索引 + 契约 + 配置权威 + 变更日志，428 行）

**定位**：全部 skill 的“架构基准”——分层、阶段表、闸门阶梯、契约规范（frontmatter / 职责边界 / 命名）、共享产物归属、质量门禁。

**总评**：INDEX 是这套 skill 体系**最有价值也最拥挤**的一份文档：它把“区域清单（单一事实源 + 四处同步）”“共享产物归属表（唯一写入方 / 只读消费方 / 刷新责任 / 逃生阀）”“GEM 内嵌副本的四条纪律”“frontmatter 与职责边界契约”都写成了**可测的规则**，并有测试守护。但一个文件同时承担 ≥6 种职责——路由、契约、配置权威、**变更日志**（7 条 MCP 计数 ⚠、09-15/09-19 两段落地清单、迁入记录、改名表）、**审计叙事**（“旧文请勿再沿用”“已被实测推翻”）、**当日实测事实**（区域硬事实）——读者要的只是“现在是什么”，却要穿过 200 行“曾经是什么”。更重要的是，INDEX 自己宣称的“唯一基准”有 4 处与代码/其他 skill 不符：区域表（DEU、AMR）、闸编号表（缺闸2b/2b-2/9）、`$WQ_PY` 定义（Windows 专属）、共享产物表（`submit_ready` 多写入方）；以及“提交层唯一权威 = submit_verdict”与 RA / submit-alpha 的说法矛盾。

| 阶段（行号） | 书写逻辑 | 职责划分 | 边界界定 | 需情景规范？ |
|---|---|---|---|---|
| 头部 + 唯一权威副本（1–29） | 🟡 | 🟡（含处置记录） | 🔴（“权威”与“解析优先”相反） | 否 |
| 运行环境铁律（31–47） | 🟡 | 🟢 | 🔴（`Scripts/python.exe`） | 是 |
| 区域清单（49–75） | 🟢 | 🟢 | 🟡（DEU/AMR 与事实不符） | 否 |
| 分层架构 + 迁入记录（77–122） | 🟡（夹迁移史） | 🟡 | 🔴（repair 卖点失实） | 否 |
| 流水线阶段表 + 引擎映射（124–149） | 🟡 | 🟡 | 🔴（“唯一权威”矛盾；S3 产物） | 是 |
| 闸门阶梯 + 闸编号（151–192） | 🟡 | 🟡 | 🔴（Sharpe 三值；闸号缺 2b/9） | 是 |
| MCP 计数 + 落地清单（194–249） | 🔴（日志混入基准） | 🔴 | 🟡（有测试守护） | 否 |
| 分工声明 + 权威版本声明（251–284） | 🟢（四条纪律） | 🟡 | 🟡（部分无守护） | 否 |
| 并发口径 + 命名规范（286–317） | 🟡 | 🟡 | 🔴（并发三处来源） | 否 |
| frontmatter + 职责边界 + 硬裁定（319–365） | 🟢 | 🟡 | 🔴（守形式不守内容） | 是 |
| 共享产物归属表（367–386） | 🟢（表头设计） | 🟢 | 🔴（仅 7 行；`submit_ready` 多写入方） | **是** |
| 质量门禁（388–409） | 🟡 | 🟡 | 🔴（覆盖范围；干净克隆 4 失败） | 是 |
| 配额口径 + 区域硬事实（411–427） | 🟡 | 🔴（应在别处） | 🔴（与 submit-alpha 矛盾） | 是 |

| # | 位置 | 维度·级 | 问题 | 改进建议 |
|---|---|---|---|---|
| IX-01 | L3–7、L5 | 职责·P2 | 头部称“本文件是全部 WQ/BRAIN skill 的架构基准……修改任何 skill 前先读本文件”，但 428 行里混了 ≥6 类内容：架构/路由（分层、阶段表）、契约规范（frontmatter、边界段、命名）、配置权威（闸门阶梯、并发、区域清单）、**变更日志**（MCP 计数 ⚠ ×7、09-15/09-19 落地清单、迁入记录、改名表）、**审计叙事**（“2026-09-26 审计重写，旧文请勿再沿用”“该结论已被实测推翻”）、**当日实测事实**（区域硬事实）。`last_verified: 2026-09-26` 声称是“索引整体有效性锚点”，但正文含 09-27（L207）与 09-28（L227）条目，**锚点早于内容** | 拆分：`INDEX.md`（路由 + 分层 + 阶段表，<150 行）、`CONTRACT.md`（frontmatter / 边界 / 命名 / 门禁）、`CHANGELOG.md`（全部 ⚠ 日期条目）、`docs/audits/`（审计叙事）；区域事实进 region profile |
| IX-02 | L9–29 | 逻辑·P2 | “唯一权威副本 = 仓库 `Claude/skills/`”，而同节 L27–29 的运行时解析顺序是 `WQ_VALIDATOR_DIR/WQ_TOOLKIT_DIR → ~/.claude/skills → ~/.codex → ~/.qoder-cn → ~/.cursor → ~/.workbuddy → 仓库 Claude/skills（**兜底**）`：**权威副本在解析链最末**，漂移发生时运行时先读到非权威副本；`test_skill_integrity` 也刻意校验“Agent 实际加载的那份”（`_resolve_skills_dir()`）而非仓库副本。“权威”与“优先”方向相反，读者易以为改仓库即生效。L23–25 三行是已归档/废弃位置的处置记录 | 明写“仓库 = 编辑权威；安装位 = 运行时优先；一致性靠 `sync_skills.py --check`，**改完必须 sync 才对 Agent 生效**”，并放进 AGENTS 的 skill 修改流程；处置记录移 CHANGELOG |
| IX-03 | L31–47 | 边界·**P1** | “`$WQ_PY` 定义（本机**单一事实源**）：`<repo>/world-quant-brain-mcp/.venv/Scripts/python.exe`”，bash 版同（`export WQ_PY="$PWD/world-quant-brain-mcp/.venv/Scripts/python.exe"`）——**`Scripts/python.exe` 是 Windows 布局**，Linux/macOS 的 venv 是 `bin/python`（本次会话即 `world-quant-brain-mcp/.venv/bin/python`）。“各 skill 中的 `$WQ_PY` 一律按本定义解析”意味着在非 Windows 环境全部 skill 的 Python 命令都指向不存在的可执行文件；同文 L417 又写裸 `python tools/quota_status.py` | 定义按平台分支，或提供 `tools/wqpy.sh` / `wqpy.ps1` 自动探测；把 skill 中裸 `python` 全部替换为 `$WQ_PY`（机械检查 D 可统计） |
| IX-04 | L35 | 边界·P2 | 持久化铁律“禁止 Write / Copy-Item 战役 json/csv……当真相源；静态配置与凭证、CLI 临时 `@file.json`、BRAIN 原始 CSV 仍用文件”：①“凭证仍用文件”与 AGENTS“禁止读取 `.env`”并存；②“当**真相源**”的限定使“写非真相源文件”是否允许含糊（planning-with-files 写 task_plan.md、`methodology_rules.json` 计数回写、`@notes.json`）；③本段在 monitor / ra-pipeline / sim-alphas 等处**逐字重复** | 只在此处定义；其余 skill 一句引用；补“允许写的非真相源文件清单与目录” |
| IX-05 | L49–75 | 边界·🟢+P2 | 🟢 表格式（region / profile / 战役目录 / entry_verdict）+“新增/删除区域须同步四处”+“代码 14 / profile 11 / 口头清单各异”的漂移事故——是全库把**单一事实源**写得最好的一段；核对 `config.REGIONS`：14 个，名单与表一致 ✓。P2（表与事实不符两处）：①**DEU**：表写 `active`，而 `regions/DEU.md` 第 3、56 行明写“`entry_verdict: probe-only`，不是 active”；②**AMR**：表写战役目录 ✗，实际存在 `tracking/AMR/config/{settings,thresholds}.json`。另：③entry_verdict 在表与 profile 中**双写**（代码消费的只有 profile 里的那个），应由脚本从 profile 生成此表；④TWN“战役目录 ✗ 但 probe-only”，无战役目录如何 probe 未说；⑤L424 “AMR 不是 RA 挖掘区”与表内“AMR：处女地模板”是两种说法 | 表由脚本从 profile/`config.REGIONS`/目录扫描**生成**，并加测试；AMR 合并为一句“非挖掘区” |
| IX-06 | L77–103 | 逻辑·P3 | 分层图 L0–L7 与阶段表 S0–S6 **数字一一对应**（L0=S0…L6=S6，L-RA/L-PRE/L-TOOL 为编排层）却用两套名字；frontmatter 写 `layer: L4`，正文写“S4”，加上 RA 的“步 N”、gate.py 的“闸 N”、monitor 的“关”，同一阶段至少 4 套编号；“L-INT（已并入）”仍占一行，括号里塞迁移史 | 一句话声明“Ln ≡ Sn”，其余编号不再并用；删 L-INT 与迁移史 |
| IX-07 | L105–122 | 逻辑·P3 | “外部扩展区迁入记录（2026-08-23 完成）”是迁移日志：`~~brain-alpha-orchestrator~~` 删除线行、“通用非 WQ 元技能不进入本目录”“历史 `.cursor/skills/` 冗余副本已移除”“`wq-brain-campaign-auto`/`brain-deepExplore` 已并入”。L113 `brain-alpha-repair` 的“5 轴旋转 + 6 武器去相关 + 体检硬门”卖点**已不真实**（RE-01）；L122 称两个元技能“与 WQ 技能链共用运行环境约定”，而 planning-with-files 全文未用 `$WQ_PY`（PW-02） | 整节移 CHANGELOG；repair 行按其真实内容改写 |
| IX-08 | L124–135 | 边界·**P1** | ①S5 行“`tools/submit_verdict.py`（**提交层唯一权威**）”与 RA L681“提交层唯一权威**不是** submit_verdict”、submit-alpha 关键坑 #5（其提交层视图是死代码）、robustness“judge = S5 唯一提交评审入口”并存——**“唯一权威”在全库出现 ≥7 次且互相矛盾**（SB-03 / JD-03 / RB-02）；②S3 产出“`alpha_list.json` → IS 指标 + status CSV”仍是**文件产物**，与 L35 的 DB 单轨铁律及 sim-alphas 的 P0-9 同；③S0/S1 健康检查判据（L147 有意设计：S0 严 cov≥0.85 / S1 宽 cov≥0.7；🟢 写明理由），但 coverage 另有“回填带 0.65–0.85”一层（probe-scoring-v2、decision-table D 卡）未在此解释；④S6 行“日常由 ra-pipeline 步 9 编排”，入口 skill 又写 monitor——日常与故障排查的分界（BM-04）应在此写一句 | ①全库定唯一说法：`submit_verdict` = 模拟层判定（BLOCKED 即拦），真闸 = 用户确认后的 POST；②S3 产物改 `backtest_results`；③补第三层；④补分界句 |
| IX-09 | L137–145 | 边界·P2 | 引擎映射行夹带实现细节与历史：S2“`build_wave.py` 只做去重/分桶/骨架配给”与 toolkit SKILL 的 `linear_mix≤50%` 骨架配给并存（TK-）；S3 把“七槽填槽 N=min(7,批数)”“ThreadPoolExecutor 并行实现”“`--max-rounds>1`”“单批在飞串行已彻底废弃”写进索引；S5 行配额说明是第 3 次重述（含 DST 隐患，SB-21） | 索引只写“阶段 → 子命令”，细节留 toolkit |
| IX-10 | L151–163 | 边界·**P1** | 标题“闸门阶梯（**唯一基准表述**）”，称数字唯一事实源是 `config.GATES/CONCURRENCY`（核对：`GATES`、`GATES_INTERNAL`、`GATES_PLATFORM`、`gate_thresholds`、`CONCURRENCY` 均存在 ✓）。问题：“**平台硬线：Sharpe>1.58**”——`GATES_PLATFORM.sharpe_min=1.58`，而 how-to-pass 写“Delay-1 Sharpe >1.25”、MCP `pre_submit_check` 写“>1.3”；1.58 与 `LOW_2Y_SHARPE`（D1）的限值同值——**“平台 Sharpe 硬线”这一个词对应 3 个数**（1.25 / 1.3 / 1.58），且未区分 IS Sharpe 与 2Y Sharpe；`IS_LADDER`、`LOW_ROBUST_UNIVERSE_SHARPE`、`LOW_SUB_UNIVERSE_SHARPE` 的公式线未列；“层级 ① IS 廉价闸 → ② PC 等待 → ③ 硬闸”又是全库第 N 套闸门分类（gate.py 闸 1–8、wave_gate 内置闸、monitor 四关、RA 九步） | config 拆 `platform_is_sharpe_min`（1.25）与 `platform_2y_sharpe_min`（1.58）；表按**检查名**给“平台线 / 内部线 / 来源常量”三列；把“层级”并入 RA 步骤 |
| IX-11 | L165–192 | 边界·**P1** | “gate.py 闸编号（权威 = gate.py 模块头）”表列闸0–闸8，并称“**不要再用第三种口径**”。核对 `gate.py`：模块头同样只有闸0–8，但代码里另有 **闸2b**（区域非法 group 字段，L360；INDEX L238 自己也用）、**闸2b-2**（区域不可用普通字段 + VECTOR 上套 `ts_*`，L369）、**闸9 窗口白名单**（L464；`platform_constraints.window_whitelist_enforce` 的备注也称“闸9”）——三者**都不在“唯一基准”表里**；表中闸1 已带“+1b”，wave_gate 内置闸另有一套名字，读者无法从文档得到完整闸清单 | 表由 `gate.py` 的**闸注册表生成**（每闸 id / 说明 / 开关 / 默认值），文档嵌入生成结果；加测试：代码里出现的“闸N”必须在表内 |
| IX-12 | L194–228 | 逻辑·P2 | “MCP 工具/节点计数（唯一基准）”里嵌 7 条 ⚠ 变更史（49→43→45→44；18→17→18→19→18→19），且**顺序混乱**（“2026-09-26 移除 1 个（45→44）”写在“2026-09-18 新增 2 个（43→45）”之前，倒序/正序混排）；读者要的只是“现在 69 / 44 / 19”。计数由 `test_mcp_tool_counts_match_index` 守护（本次实测通过 ✓）。另 `tools_submit 0` 需说明“提交原语是函数 `submit_alpha` 而非 MCP 工具”，否则与 submit_batch.py docstring 的“唯一生产提交原语”、judge 的“不存在 `submit_alpha` 工具”读作矛盾 | 计数留一行；历史进 CHANGELOG；补一句 `tools_submit` 说明 |
| IX-13 | L230–249 | 职责·P2 | “2026-09-19 挖掘流程优化落地”与“2026-09-15 接线修复”是两段**功能变更日志**（15 条），含环境变量 `WQB_GLOBAL_SLOTS`（缺省 7）、`WQB_GEM_MAX_PER_SKELETON`（缺省 12）、`--no-isolate-errors`、`region_invalid_fields` 等，其中的**行为规则只在此处出现**；全库没有“环境变量/开关目录”，读者要找“怎么关连坐隔离”只能读 INDEX 的历史条目 | 建 `docs/env_and_switches.md`（变量 / 开关 / 默认 / 所属 skill / 生效版本）；INDEX 删日志 |
| IX-14 | L251–260 | 边界·P2 | “分工声明”重申“Mode B（默认入口，70%）/ Mode A（30%）……两者都失败 >10 种结构才转向换数据集”——70/30 与 “>10” 是 OP-02 的不可度量量，此处第 2 处引用；“MCP 直发批也过闸”一段是 09-01 落地记录，应在 wqb-concurrency / gate-rules，而不在分工声明 | 引用 OP-02 的定义；落地记录迁出 |
| IX-15 | L262–284 | 边界·🟢+P2 | 🟢 “权威版本声明”把嵌套副本的**真实角色**写成 4 条可测纪律（内嵌 `scripts/` 是硬依赖不删不改；内嵌 FI/SKILL.md 必须与顶层逐字一致并由测试守护；内嵌 dfe **不得**出现 SKILL.md；GEM 产物写 `GEM_REPORT_ROOT`），并给出修复入口。P2：①“2026-09-26 审计重写，旧文请勿再沿用”“该结论已被实测推翻”是审计叙事，读者需要的是规则行；②守护只覆盖第 2、3 条（`test_gem_skill_paths`），第 1、4 条无测试，dfe 的 reference / OUTPUT_TEMPLATE / examples 漂移无守护（FE-13）；③表第 3 行仍以“权威版本”名义登记 `tracking/KOR/scripts\` 的 9 个区域私有脚本副本，且用反斜杠（Windows 写法） | 去叙事；补第 1、4 条测试；第 3 行移出或改“待清理” |
| IX-16 | L286–291 | 边界·**P1** | “并发口径（演进注记）”：旧 C=5（2026-07 前）/ 新 Token-Bucket C≈7（**引 `wq-backtest-monitor` §6**）/ 七槽填槽（**引 `wqb-concurrency` §8**）——并发参数的来源三处：`config.CONCURRENCY`（L153 称唯一）、`wqb-concurrency` §8、`wq-backtest-monitor` §6；后者与 config 数值一致（7/6/45/20–40）但属**抄写而非引用**（违反 L359–362 硬裁定①）。保留 C=5 旧值是历史 | 只留 `config.CONCURRENCY` 与 wqb-concurrency 两处；出处改指后者；删旧模型 |
| IX-17 | L293–317 | 逻辑·P3 | 命名规范附 7 行“旧名（禁用）→ 现名”改名表（迁移日志），同时声明“旧名禁止在任何文档/代码/引用中再出现”——旧名出现在此表本身（自相矛盾），也使机械扫描需为本节开白名单；“改名配套动作（`git mv` → grep 替换 → 改代码硬编码 → sync）”一句才是可执行内容 | 删改名表，保留规则与配套动作 |
| IX-18 | L319–339 | 边界·P2 | frontmatter 规范：必需 `name/layer/description/last_verified`，可选 `version/user-invocable/allowed-tools/agent_created/hooks`；但 L326–331 示例把 `allowed-tools` 写成“必须是 YAML 列表”，“必需字段”里却没有它、“可选字段”里有；`hooks` 被列为可选键但**无任何安全规则**（钩子在每次工具调用/停止时执行 shell，PW-01）；`user-invocable`、`version`（planning 2.1.0 / monitor 1.1）语义无定义；`description`“单行双引号字符串”未限长，实际最长 702 字（TK-01），且多数是**功能清单而非触发条件**（judge、submit-alpha、superalpha 均含实现细节） | 明确 `allowed-tools` 是否必需；加“hooks/allowed-tools 审查规则”；description 规范：≤300 字、只写“何时触发 + 范围 + 不做”；定义 `version`/`user-invocable` |
| IX-19 | L341–365 | 职责·**P1** | “职责边界”由 `test_skill_boundaries.py` 守护——**守护的是该段存在且有三条（形式），不是内容为真**。本次审查中至少 6 个 skill 的边界声明与正文/代码矛盾：submit-alpha 声称只管 REGULAR，正文含 SUPER/PPA/配额；judge 声称不提交，脚本仍可 POST；monitor 声称“不是写入方”却强制回写；superalpha 上游写 submit_verdict 而该工具无 SUPER 分支；how-to-pass 声称只读却判死回写；repair 声称配方查表而配方已丢。覆盖率 39% → 100% 是**形式覆盖**，实质一致性无人检查；硬裁定①“skill 不得改写权威常量，只能引用”被 how-to-pass、judge（`INTERNAL_HARD_GATES` 第 3 份拷贝）、monitor（TVR 0.05–0.30、universe 合法性）、INDEX 自身广泛违反 | 增加语义检查：边界段“不做”里的动作词（提交 / POST / 写入 / 判死）在正文出现须带“仅引用”标记；常量字面量检查（skill 中出现 config 常量的数值须带来源标注） |
| IX-20 | L367–386 | 边界·**P1** | 🟢 表头（产物 / 唯一正式写入方 / 只读消费方 / 刷新失效责任 / 逃生阀）是好设计，`priors_snapshot_<region>` 行含事故动机与“stale 仅 WARN、不得据此继续实跑”的可执行止损。但只有 **7 行**：`ledger_kv` 一句“按 key 定”带过，而全库实际使用的键至少有 `s0_whitelist`、`s1_<ds>_d<delay>`、`s2_<ds>_d<delay>_idea`、`prod_first_<wave>`、`stop_rules_override`、`region_kb`、`salvage_pool`、`near_pool`、`dead_end`、`submit_ready`、`submit_ready_blocked`、`saturated_datasets`、`research_leads_w<W>`、`wave<N>_verdict`（已废止但仍被 5 处文档教）、`os_feedback_latest`（脚本已归档）……其中 `saturated_datasets` 有读取方无写入方，`submit_ready_blocked` 有写入方无 S0 读取方，`research_leads_w<W>` 未登记；`submit_ready` 表写“唯一 = ra-pipeline 步 7→8”，实际另有 `campaign.py ledger submit-ready`、`wq-backtest-monitor` §14 项 3，`super_build.py` 读取，且 `submit_queue` 有**同名 SQL 表** `submit_ready` | 生成完整 ledger-key 目录（键 / 写入方 / 读取方 / 刷新责任 / 状态）；加测试：skill 中出现的每个 ledger 键必须在目录内、每个被读的键必须有写入方 |
| IX-21 | L388–409 | 边界·P2 | 质量门禁三条命令 + 7 项校验，但：①“无已废弃路径引用（`.qoder/skills/` 等）”**未覆盖 reference.md**（selfcorr-quick 的 reference.md 仍含 `.qoder/skills/…`，SC-07；`pull_skills.py` 默认目录也是 `.qoder/skills`）；②“skill 内相对 `.py` 引用指向真实文件”**未覆盖嵌套 references**（机械检查 C 有多处 MISSING）；③**本次在干净克隆上实测**：`pytest test_skill_integrity.py test_skill_boundaries.py test_docs_consistency.py` → 351 passed / **4 failed**：2 项因守护对象是“Agent 实际加载的 `~/.claude/skills`”（`_resolve_skills_dir()`，设计如此），容器里该目录含非仓库目录 `synced`、`session-start-hook`；2 项因依赖被 `.gitignore`（`data/`）排除的 `data/operators_verified.json`——**干净克隆必失败**。以上均非 skill 内容缺陷，但说明守护的输入依赖宿主状态与未入库的运行态数据 | 守护输入可指定（`WQ_SKILLS_DIR`），依赖的运行态数据由 fixture 生成；门禁范围扩到 `references/**/*.md`；把“失败于环境”与“失败于内容”分开报告 |
| IX-22 | L411–420 | 边界·**P1** | 提交配额口径整段是**第 4 次**完整重述（submit-alpha ×2、superalpha、INDEX S5 行、此处）。本段是全库**唯一正确**处理 `activities/submissions` 的（“不得用于当日”，与 `quota_status.py` 一致），与 submit-alpha L264、`pipeline.py:206`（仍优先读 activities）矛盾（SB-15）；同样含“00:00 ET（= 12:00 GMT+8）”的 DST 隐患（2026-11-01 后为 13:00）；“`get_submission_quota` 移除史”再次出现；L417 用裸 `python` | INDEX 只留指针；配额模型只在 `quota-and-tower` 一处；时区用 `America/New_York` 计算 |
| IX-23 | L422–427 | 边界·P2 | “2026-09-19 平台区域硬事实（当日实测，优先级高于任何旧记）”是**带日期的区域事实**（ALL/AMR 选项、JPN 无 pv1、IND robust 闸定义与破墙配方、prod 竞速）：区域事实应在各区 profile；“优先级高于任何旧记”是一次性声明，10 天后无失效机制；IND 破 robust 墙的配方（pwRJmvP3）与 RA 步 5b“不做去相关变体”的关系未说；“prod 0.60–0.70 的候选必须当天提交”是提交纪律，属 submit-alpha / next-move | 移入 profile / submit-alpha，各带 `last_verified` 与失效条件 |
| IX-24 | 全文 | 情景·**是** | 作为“路由文件”，缺**任务 → skill 的场景路由表**：用户说“提交 alpha”应命中谁？（submit-alpha / superalpha / judge 三个 description 都含“提交”）；“监控回测”命中 monitor 还是 ra-pipeline 步 9？；“修复弱候选”命中 repair 还是 optimization-v1？（RE-02）；“相关性怎么办”命中 how-to-pass / selfcorr-quick / robustness / prod-corr-avoidance 中的哪个？ | 加 12 行“用户意图 → 首选 skill → 不选哪个及理由”表，取代目前靠 description 关键词匹配 |

---

## Part B　跨 skill 综合（X-1 … X-19）

> 逐条问题（Part A）按“某个 skill 的某一段”组织；本篇把**散在多处的同类问题**合并，给出**现象 → 根因 → 单一表述方案**。方案均为**草案**，涉及业务取舍处（如 prod 墙阈值动作）需业务方裁定。

---

### X-1　prod 墙：同一情景 ≥6 套互相矛盾的处置学说

**现象**（同一情景：某家族首探 prod 相关性偏高，下一步怎么办）：

| 学说 | 出处 | 动作 |
|---|---|---|
| ① 首探即判 | RA 步 5b（RA-69） | prod ≥0.7 → 记 dead_end、换机制，**不做任何去相关变体**（bucket/门控/平滑实证都破不了墙）；0.60–0.70 直接进步 8；<0.60 无指示 |
| ② prod-first 串行 | RA 步 7（RA-74/85） | S3 收批后族级探 prod（`--top-k 3`，5b 是 `--top-k 2`，L498 又是“每槽先 1–2 条”）；STOP → 换白名单不同数据集（D0） |
| ③ 决策表 D0 | RD-04 | “换白名单不同数据集 regenerate，勿磨同腿变体” |
| ④ 决策表 D14 | RD-28 | 结构性去相关 → **镜像稀释**（加相关≈0 的稀释腿）→ 中性化骨架重构 → 最后才换数据集（并称 D0 是默认）——**镜像稀释与“禁止任何加权混合/等权腿相加”直接冲突**；引用的 `prod_wall_breakthrough_sop.md` 不存在 |
| ⑤ optimization-v1 | OP-01、OP-18 | description 承诺“把 PROD 压到 0.7 以下”；“prod_corr 反馈循环” + 组合腿救援 |
| ⑥ RA L654 | RA-93 | prod ≥0.7 → Mode B 换概念（“>10 种结构”无依据） |
| ⑦ 探针派 | RE-08、RB-15、RC-01/03、RP-07 | “先 5 个多样化探针”“5 个逐个提交读 prodCorr”“同族不重复投入”；入口提示词教 D14 三条路径（与 5b 相反） |
| ⑧ 区域/用例 | RR-02、SP-09、IX-23 | USA profile“预警线 0.6：≥0.6 即停扩换腿”（而 SKILL：0.60–0.70 → 当天提交）；superalpha“PROD 饱和 → 注入低 prod 新血”；INDEX“IND 破 robust 墙配方” |

**根因**：每一次事故复盘都追加一段“新学说”，旧段不撤；`decision-table`、SKILL、prompt、区域 profile 四层各写各的。

**方案（草案，需业务裁定）**：**唯一一张决策表**放在 `decision-table` 的 D0，其余全部引用；表内每行给“阈值 → 动作 → 谁写台账 → 例外”：

| 首探 prod（族内最强 1 条，平台实测，串行） | 动作 | 说明 / 例外 |
|---|---|---|
| < 0.60 | 正常扩变体，进步 7–8 | — |
| 0.60–0.70 | **不扩变体，当天进步 8**（外部同款会在一小时内把 prod 堵到 1.0，见 INDEX 竞速条） | USA 的“0.6 预警换腿”一句删除 |
| ≥ 0.70 | 家族 `dead_end`：先 forum_recon（`found=true` 不得直接判死）→ `seal_dead_end`；下一步 = 换机制 / 换数据集（D0） | **唯一例外**：已过 `mode_b_qualification`（主闸或旁路）且有 salvage 辅助腿的候选可走 Mode B 组合腿救援（OP-12 的入场三式，禁加权）；bucket/门控/平滑类“去相关变体”一律不做 |
| 探针实现 | `campaign_intel.py prod-first`（`--top-k` 固定一处）；只读 `GET correlations/prod` | 禁用 POST 探测（X-9） |

镜像稀释（D14）撤回或改为“骨架重构”；optimization-v1 description 改为“在**未触发 prod 墙**的前提下改进”；D14 的失效引用一并修。

---

### X-2　提交判定链与“唯一权威”

**现象**：仅在 SKILL.md + INDEX 中，“唯一权威 / 唯一事实源 / 唯一基准 / 唯一入口 / 唯一正式写入方 / 唯一真相源 / 唯一标准依据”共出现 **47 次**。关于**提交判定**至少有 10 处自称权威且互相矛盾：

| 出处 | 说法 |
|---|---|
| INDEX S5 行、AGENTS §步 8 | `submit_verdict` = 提交层唯一权威 |
| RA L20 / L938（RA-131） | 判定唯一权威 = `submit_verdict`；L679 却写“否决权威”；**L681 “提交层唯一权威不是 submit_verdict”**（RA-03） |
| judge L26/L41/L52；optimization-v1 L181（OP-15）；superalpha L38 | 权威 = `submit_verdict` |
| submit-alpha L283 | `submit_verdict` = “403 盲区的唯一可信判定入口（模拟态 + submit 双视图）”；同文 L177–182：其提交层视图是**死代码**，真闸只有 POST（SB-03） |
| robustness 头部（RB-02） | judge = “S5 唯一提交评审入口” |
| `submit_batch.py` docstring | `tools_submit.py::submit_alpha` = 唯一生产提交原语（而该文件被文档称为“批量提交”工具，实为**仿真派发**，SB-24） |
| `tools_ops.py::submit_verdict` docstring | “否决权威：说 BLOCKED 即不提交；说可放行仍需 prod<0.7 + 用户确认” |

**代码事实**（已核对）：`submit_verdict` 有**两份实现**（`tools/submit_verdict.py` CLI 与 `tools_ops.py` MCP 工具，逻辑相同）；`SUBMITTABLE` 只在提交层 `GET /submit` 为 200 时产生，而该 GET 恒 404 → 对未提交候选只会是 `UNVERIFIABLE`（CLI 退出码 0）或 `BLOCKED`（1）；真正不可逆的一步是用户确认后的 POST。

**根因**：判定权几经移交（judge → submit_verdict → “真闸=POST”），每次只加新说法，没有把“**能拦**”与“**能放**”两种权力分开命名。

**方案**：把“权威”拆成两个词并全库统一——**否决权威**（只能拦，不能放）与**放行权威**（用户确认 + POST）；提交链写成**一张可达状态机**：

| 步 | 判定 | 权力性质 | 入口 | 结果 | 可逆 |
|---|---|---|---|---|---|
| 1 | 资格门：`Failed RA/PPA == 0` 且 `pending == 0`（RF-03） | 否决 | `config.compute_webdata_failed_counts` | 非零 → 回步 7 | 是 |
| 2 | 模拟层 + 硬闸类 WARNING（LOW_FITNESS/SHARPE/2Y） | 否决 | `submit_verdict`（CLI/MCP 共用一份实现） | `BLOCKED` → 停；`UNVERIFIABLE`（独立退出码）→ 继续；`ALREADY_SUBMITTED` → 结束 | 是 |
| 3 | prod 实测 <0.7（`GET correlations/prod`，阻塞 ≤60 min，`correlation_busy` 立即返回） | 否决 | `check_correlation` / `super_build probe` | ≥0.7 → X-1 | 是 |
| 4 | 稳健性闸 | 否决（建议把结论落台账键并由 submit_verdict 读取，RB-03） | robustness | `REJECT` → 停 | 是 |
| 5 | 用户明确确认 | 放行的必要条件 | 人 | — | 是 |
| 6 | `workflow_submit_alpha(confirm_submit=True)` | **放行（不可逆）** | submit-alpha 四态表 | 200 = 已提交；201/空体 = 异步受理 | **否** |
| 7 | 轮询 ACTIVE / 补发一次 / `ASYNC_STUCK` 通知 | — | 状态机表（JD-04） | — | — |
| 分支 | PPA：走 web UI 交接单（SB-22）；SUPER：`super_build.py` 的 prod 闸默认强制（SP-13） | | | | |

之后“唯一权威”一词只允许出现在**登记表**里（每个宣称对应一行：宣称内容 / 实现位置 / 测试），其余文档写“见 X”。

---

### X-3　加权混合 / 腿相加：政策已禁、闸门有缺口、文档仍在教

**现象（文档仍在教，≥12 处）**：RA-46（EUR `0.4×慢 MODEL + 0.6×快 PV` 作“已验证配方”）、RD-03（D0/D3“主动混合冲更高”）、RD-11/RD-19/RD-28（D3 形态说法被证伪；`subtract(rank,rank)` 称“单信号”；D14 镜像稀释）、TK-28（toolkit 第三份 + 0.40/0.60）、TR-06（build_wave `linear_mix≤50%`）、TR-27（probe-scoring“跨 Category rank 加法 / 两两融合”）、PP-13/PP-20（V9 `* 0.35`）、GM-06（“每加一腿点名修哪个闸”）、JD-09（CW 配方 `add(multiply(rank,w1),multiply(rank,w2))`）、HP-05（流动/非流动 decay 相加）、HP-07（证据表前三行）。

**政策**：CLAUDE.md“禁止混信号调参，尤其警惕 add(A,B)”；RA“路线 A（2026-09-13）：禁止任何加权混合（含等权）”。

**闸门实测**（`gate.py` 的 regex `weighted_signal_mix` / `_detect_weighted_mix_structural` / `_detect_equal_weight_leg_add`，逐形态）：

| 表达式形态 | regex | structural | eq-leg | 结论 |
|---|---|---|---|---|
| `add(0.6*rank(A), 0.4*rank(B))` | ✔ | ✔ | ✔ | 拦 |
| `0.6*rank(A) + 0.4*rank(B)`（权重在左，中缀） | ✔ | ✗ | ✗ | 拦（仅靠 regex） |
| `rank(A)*0.6 + rank(B)*0.4`（**权重在右**，中缀） | ✗ | ✗ | ✗ | **放行** |
| `scale(rank(A)) + scale(-rank(B)) * 0.35`（V9 的顶层形态；完整 V9 表达式实测同样放行） | ✗ | ✗ | ✗ | **放行** |
| `add(multiply(rank(A),0.6), multiply(rank(B),0.4))` | ✔（func_suffix） | ✗ | ✔ | 拦 |
| `add(rank(A), rank(B))` / `add(rank(A), -rank(B))` | ✗ | ✗ | ✔ | 拦 |
| **`subtract(rank(A), rank(B))`**（数学上 ≡ `add(rank(A), -rank(B))`） | ✗ | ✗ | ✗ | **放行——且闸自己的报错文案把它当“合规替代”推荐** |
| `rank(A) - rank(B)`（中缀） | ✗ | ✗ | ✗ | 放行 |
| `ts_decay_linear(s,5)*rank(v*c) + ts_decay_linear(s,10)*(1-rank(v*c))`（HP-05 的示例，中缀） | ✗ | ✗ | ✗ | 放行；函数式同构写法被 eq-leg 拦 |

即：**同一数学结构，写法不同判定相反**；上一轮评审 P0-2 所称“V9 被闸 5 block”对该形态并不成立（PP-13）。RA-89 提出的 `subtract` 漏洞得到实测印证。

**根因**：规则以“已发生事故的表面写法”逐条补丁（regex / 结构检测），没有先定义“什么是禁止的结构”再实现；文档与闸门各自演进。

**方案**：① **一句话政策**：“禁止把两条及以上独立信号腿按任意（等/非等）权重线性组合，无论中缀、函数式还是减号；允许的只有 `structural-interaction-forms.md` 的 F1–F6 与单信号结构”；② **明确 `subtract(rank(A), rank(B))` 的地位**：若允许（价差、需经济含义），则 `add(rank(A), -rank(B))` 也应放行并把“经济含义”写成可机检的字段关系（同数据集同量纲等）；若不允许，闸 5 补检测并修正报错文案；③ **闸 5 覆盖矩阵测试**：形态（中缀/函数式）× 权重位置（左/右/无）× 运算（add/subtract/multiply-of-legs）参数化，期望值写在测试里；④ **SOP 例子过闸测试**：文档里的 fenced 表达式必须通过 gate 0/1/3/4/5/9，故意展示的反例用 `<!-- counterexample -->` 标记（X-17 #5）。

---

### X-4　术语表：同一个词 2–4 种含义

| 词 | 现有含义（出处） | 建议 |
|---|---|---|
| **槽** | ① 并发模拟槽（Token-Bucket，`slots=7`）② 波内表达式配额（“七槽”：≥2 跨金字塔…）③ 批大小（8 子模拟）④ 概念槽（RA-49） | ① 叫“并发令牌”；② 叫“波内配额”；③ 叫“批” |
| **提交** | ① 提交回测（`--submit`；`submit_batch.py` = POST /simulations）② 把 alpha 提交上平台（POST /alphas/{id}/submit）③ “提交层”视图（TK-27、SB-24、SA-01） | ① `dispatch`；② `submit`；③ “提交层视图”仅指 GET /submit（已废） |
| **配额** | ① 相关性配额/槽位（账号级单并发）② 模拟并发③ 提交配额（REGULAR 4 + SUPER 1 + PPA 1 /ET 日）④ “周额度”（过期概念，RE-08）（RA-102） | 四个词分开：`corr_slot` / `sim_tokens` / `submit_quota` |
| **信号族** | ① 字段集合（步 7）② 骨架指纹前 2 个算子（闸 PF）③ 5b 的“信号族”（RA-68） | 定义 `family_key`（一处），其余引用 |
| **达标** | ① S>1.58 & F>1.0（停止规则 A）② `ra_failed_checks` 为空（严格 yield）③ 过全部评审闸/GREEN（RA-107） | 三种各起名：`meets_internal_line` / `ra_clean` / `review_passed` |
| **ATOM** | ① `SINGLE_DATA_SET` 分类（judge trend score）② 放宽 2Y 标准的提交口径（how-to-pass）③ 单数据集 atom alpha（CLAUDE.md）（JD-12、HP-13） | 统一一处定义，写明“放宽什么、阈值多少” |
| **WARNING / PENDING** | WARNING：提示 vs 硬闸类（≡FAIL）；PENDING：不挡提交 ≠ 会通过（SB-11、SB-14） | 见 X-5 |
| **判死** | 候选 / 家族 / 字段 / 数据集 / 波次五种粒度（HP-16、ME-03、RA-83、RD-09） | 采用 ME-03 的粒度：单次失败只约束“字段搭配 + 结构 + 设置”；判死范围 = (region, family)（HP-17） |
| **权威 / 唯一** | 见 X-2 | 分“否决权威 / 放行权威” |
| **衰减比** | IS 内部 `last_year/full_period` vs IS→OS 跨平台衰减（RB） | 各起名 |
| **合格线** | IS 层 vs 提交层 | 显式分层 |
| **编号体系** | L（层）/ S（阶段）/ 步 / 闸 / 关（monitor）；L0–L6 ≡ S0–S6 却两套名字（IX-06） | 一句话声明 Ln ≡ Sn，其余不并用 |

---

### X-5　verdict / 状态词表：≥12 套

| 系统 | 取值 | 出处 |
|---|---|---|
| `submit_verdict` | SUBMITTABLE / UNVERIFIABLE / BLOCKED / ALREADY_SUBMITTED（退出码 0/0/1/0） | CLI + MCP |
| judge / `workflow_judge` | READY / REVIEW / BLOCK（+ `WAIT_THEME_ROTATION`，**未实现**） | JD-09 |
| `s4-prescreen` | READY / REVIEW / REJECT | RA-95 |
| robustness | PASS / CONDITIONAL / REJECT | RB |
| `wave_results.verdict`（契约） | PASS / PARTIAL / FAIL（旧写法 GREEN:/RED:/全灭 已归一） | BM-14 |
| RA 波级颜色 | GREEN / YELLOW / RED（RA-107） | |
| probe-scoring 三灯 | 绿 / 黄 / 红 | TR-30 |
| prod-first | EXPAND / STOP | RA L578 |
| hypothesis-first | rejected / partially_supported / supported / needs_refinement | HF-08 |
| `entry_verdict`（区域） | active / probe-only / frozen | NM-09 |
| 提交/轮询状态 | 201/200/403 四态、STALLED / TIMEOUT / ASYNC_STUCK | SB-10 |
| **alpha 颜色** | GREEN / BLUE / RED / YELLOW / PURPLE（`alpha_properties`） | **与 RA 波级颜色同词** |

**关键错配**：路由条件“`submit_verdict` 返回 READY”（RA-95、JD-14、RA L664/L914）——READY 是 judge / s4-prescreen 的词，`submit_verdict` 没有。**方案**：分三层各一套词——**alpha 级决策**（一套）、**波级**（PASS/PARTIAL/FAIL）、**区域级**（active/probe-only/frozen）；基础设施状态另表；**颜色只用于 alpha 标签，不用于 verdict**。

---

### X-6　闸门模式开关：形态不一、默认不一、含日期翻转

| 开关 | 形态 | 缺省 |
|---|---|---|
| wave_gate `--gate-mode` | `{off,warn,enforce}` + **日期翻转**（2026-10-11 warn → 10-12 enforce） | warn（10-12 起 enforce） |
| `--inspect-mode`（体检硬门） | `{off,warn,enforce}` | warn |
| 闸 SEM | enforce 缺省 + `--skip-semantic-gate` | enforce |
| 闸 PF | 布尔对 `--prod-family-gate / --no-prod-family-gate` | 开 |
| gate.py 闸 0 / 7 / 8 | `--gate0`、`--sanity-longcount`、`--sanity-event-type` | 关 |
| 闸 6 | 常开 + `--skip-diversity-gate` 逃生阀 | 开 |
| 闸 9 | JSON 键 `window_whitelist_enforce` | false（warn） |
| 停止规则 | ledger `stop_rules_override`（含到期日） | — |

（RA-44：“≥12 个模式开关，形态 5 种”；RA-28、RA-42、TK-16。）**方案**：一张表 `闸 id | 开关 | 缺省 | 是否含日期翻转 | 逃生阀需要的台账记因（X-8）`；统一 `off/warn/enforce` 三态；逃生阀一律经 waiver 协议。**时间炸弹**：10-12 翻转后 RA/toolkit 里的“warn”描述须同步（见 X-19）。

---

### X-7　多副本真相源与“唯一”宣称的实际状态

| 事实 | 副本 | 不一致 | 方案 |
|---|---|---|---|
| **闸编号** | gate.py 模块头 / INDEX / toolkit SKILL / RA（TR-01 两处都自称唯一） | 缺 **闸2b、闸2b-2、闸9**（IX-11）；wave_gate 另有 SEM/PF/2.6 | 由 gate.py **闸注册表生成**表 |
| **`submit_ready`** | ledger 键列表 / **同名 SQL 表** / matrix 声称“镜像”（RD-07、CM-21、TK-32、TR-16） | 写入方：RA 步 7→8、`campaign.py ledger submit-ready`、monitor §14 项 3；读取方：super_build、步 8 | 键与表改名；目录登记（X-8/X-17） |
| **wave 结论键** | `wave_results.verdict`（唯一）/ `wave<N>_verdict` / `s6_verdict_<wave>`（已废止） | 仍被 **6 处**教：RA-108、RD-21（D8）、RP-08、TR-15、ME-02、BM-14 | 清零 + grep 测试 |
| **registry vs region_kb** | matrix“registry 唯一事实源”；RA“region_kb 是 S2 先验唯一上游” | 两个“唯一”（CM-22） | 划界：win/dead → registry；先验 → region_kb |
| **priors_file** | RA“必须带”/“可省略”（RA-47、RP-05） | 直接矛盾 | 以代码为准（可省略）改文档 |
| **S4 实现** | `review_wave.py` / selfcorr→…→robustness 链（RA-87） | 两套 | 选一，另一降为参考 |
| **体检包生成器** | `webdata_quality.py --export-expr` / `gen_field_inspect_packs.py`（RA-62） | 前者源码注释自承“自诞生起没产出” | 删前者 |
| **并发参数** | `config.CONCURRENCY` / wqb-concurrency §8 / monitor §6（IX-16） | 数值一致但**抄写**；旧 C=5 残留 | 只引用 config |
| **配额模型** | submit-alpha ×3、superalpha、INDEX ×2、toolkit、poll-and-quota（SB-21） | activities 可用/不可用；DST | 一处 + 时区库 |
| **点塔规则** | submit-alpha L196–233 / judge L252–272（JD-15） | 逐句拷贝；同样的分档重叠与“差 2 颗一次点亮”错误 | 一份 `pyramid-priority.md` |
| **PPA 方法论** | ppa-mining / ra-pipeline `ppa-mining-experience.md`（PP-25） | 24 段重复，Jaccard 0.50 | 合并 |
| **引擎实现** | toolkit“唯一权威实现” / 仓库根 `tools/`（TK-05） | 两处 | 划界 |
| **区域清单** | `config.REGIONS`（14）/ INDEX 表 / profile / 战役目录 | DEU：表 active vs profile probe-only；AMR：表“无战役目录”vs 实有 `tracking/AMR/config`（IX-05） | 表由脚本生成 |
| **submit_verdict 实现** | CLI + MCP 两份 | 逻辑重复（`_count_failed`、`_SUBMIT_HARD_GATE_WARNINGS`） | 共用一份 |

**方案（通则）**：凡“可由代码导出的表”（闸、区域、工具计数、阈值、ledger 键）**由代码生成并嵌入文档**，测试比对生成物与已提交文档；凡人写的“唯一”宣称登记到一张表（X-2 末段）。

---

### X-8　“台账记因 / 豁免”：至少 17 处，没有一个键名

**现象**：SKILL.md 中“台账记因 / 记因 / 留痕 / 豁免 / 记录原因 / 写明原因”共 17 处（RA 6、toolkit 4、forum-browse 4、superalpha 2、optimization-v1 1），例：RA-28（体检包缺失时“可显式降级，但必须在台账记因”）、RE-09（“台账必须记录 TOP3000 失败原因”）、FQ-05/06（免预筛留痕）、RA-117（`stop_rules_override` 豁免）。**没有一处给出键名、字段、有效期、谁有权批准**；agent 只能各自发明或忽略。

**方案**：一个统一的 waiver 协议（ledger 键 `waiver_<gate>_<region>_<wave>`）：`{gate, reason_code(枚举), evidence(键/id), approved_by(user|agent), created_at, expires_at}`；所有“可显式降级”的闸在其条目里写“跳过须写 waiver，过期自动失效”；gate 代码读取并**在报告首行打印被豁免的闸**（避免静默）。

---

### X-9　不可逆 / 有外部副作用的动作：防护靠散文

| 动作 | 出处 | 现有防护 | 缺口 |
|---|---|---|---|
| `POST /alphas/{id}/submit`（通过即提交） | 被称“零成本探测/预检”≥12 处：superalpha ×6、RA ×2、submit-alpha ×2、how-to-pass、repair、judge、selfcorr-quick、robustness、prod-corr-avoidance | `workflow_submit_alpha` / `submit_alpha` 节点默认 `confirm_submit=False` | 文档教**裸 POST**；示例默认 `confirm_submit=True`（SB-06） |
| `force=True`（跳过本地预检） | SP-13、SB-08 | 无 | MCP 路径无 prod 闸 |
| judge `--confirm-submit` | JD-14 | 散文“已废弃” | 代码仍 POST；201 被报失败 |
| `super_build.py submit`（二次 POST） | SP-13 | prod 闸默认强制（`--allow-prod-above-07` 豁免） | “预检”一词误导（第一个通过的变体即被真提交） |
| `pull_skills.py --overwrite` | PB-02 | 无 | `rmtree` 无备份，示例默认带 |
| skill frontmatter `hooks:` | PW-01 | 无 | 等同任意命令；INDEX 无审查规则 |
| LLM 外发 | judge（Moonshot/OpenAI）、GEM（DeepSeek）、arxiv（DeepSeek）（JD-10、OP-04、EX-06） | 无 | 无“外发哪些字段/禁止外发什么” |
| 凭据读取/传参 | JD-07、SB-09、SC-07、NM-14、FB-10、FI-02、IR-05 | AGENTS“禁止读取 `.env`” | ≥8 种来源；示例读 `.env`、命令行传密码 |
| PPA web UI 提交 | SB-22 | 无 | 人工通道无交接单 |

**方案**：全库统一一个**“不可逆动作块”**模板，出现在每个此类动作的首次说明处：

```
> ⚠ 不可逆：<动作>。前置（缺一不得执行）：<条件…>。
> 默认形态（预检/干跑）：<命令>。需要用户明确确认：是/否。
> 执行后必须核验：<产物>。失败/异常：<不重试 / 补发条件>。
```

并把“探测”统一改成只读手段（`correlations/prod` 读取、`confirm_submit=False` 预检）。

---

### X-10　SOP 的结构与写法：规则、叙事、快照、日志分离

**现象**：SKILL.md 内混着 ①规则 ②实证叙事（“2026-09-11 实测…”）③变更日志（“⚠ 2026-xx 新增/移除”）④审计叙事（“旧文请勿沿用”“已被实测推翻”“删除线行”）⑤日期快照（“现状：USA 133 / EUR 7 …”）⑥个例实例（`YPgAa3WR`、v52b、`KPGvRMg1`）。典型：RA-117 单个表格单元格 ≈2000 字且含“GBR 已写入 stop_rules_override，至 09-30”；SP-09 用“优先于上表阅读”补丁代替改写；IX 有 7 条 MCP 计数 ⚠ 变更史。descriptions 最长 702 字（toolkit），多为功能清单而非触发条件（IX-18）。**同时**：只有 6/33 个 skill 有显式失败分支节、5/33 有显式产出节（启发式）。

**为什么重要**：skill 是**运行时输入**——GEM 把 dfe（322 行）与 FI（111 行）SKILL.md 拼进 LLM prompt（FE-13），篇幅与自相矛盾直接进入生成质量；RA 单文件 950 行（≈58KB）每次加载都占上下文。

**方案（结构）**：每个 skill = **核心 SKILL.md（规则，目标 ≤250 行）** + `references/`（按需加载：案例、实证、区域细节）+ 仓库级 `CHANGELOG.md`（全部“⚠ 日期”条目）；**每步固定模板**（见 Part D）：目的 → 前置（可机检）→ 调用（含 `--dry-run`）→ 产物（键/表 + 写入方）→ 完成定义 → 失败分支（症状→处置表）→ 不做什么（反例）→ 情景卡链接；快照必须带 `as_of` 与失效条件，或改为由脚本实时生成；description ≤300 字，只写“何时触发 + 范围 + 不做”。

---

### X-11　数字漂移总表（应只引用 `config`）

| 量 | 出现的取值（出处） | 权威 |
|---|---|---|
| **Sharpe（IS，D1）** | 1.25（HP-02、mode_b 主闸）/ 1.3（`pre_submit_check`，SB-08）/ **1.58**（`GATES_INTERNAL` 与 `GATES_PLATFORM`；INDEX；judge `INTERNAL_HARD_GATES`）；config 注释另记历史 1.5/1.28/1.1 | 需拆 `platform_is_sharpe` 与 `platform_2y_sharpe`（IX-10） |
| **2Y Sharpe** | 1.6（RD-05、robustness）/ 1.58（`submit_queue.LIM`、playbook）/ ATOM“>1”（HP-13）/ CHN 2.08 / 判死线 1.2（`hard_kill`） | 分层写明适用对象 |
| **Turnover** | 平台 1–70%（config）/ 内部 5–20%（config）/ 5–30%（RD-02、BM-05）/ 1–40%（OP-16）/ 4–40%（`pre_submit_check`） | config |
| **Margin** | 5bp（RD-02、PP-19、USA `pre_submit`）/ 8bp 下限与 15bp（SB-23）/ **10bp**（config 内部；平台不检 margin） | config |
| **Returns** | 5%（config）/ 4%（`pre_submit_check`） | config |
| **SELF 内部线** | 0.50（config、judge）/ 0.55（superalpha 硬闸）/ 0.4（rubric 引文） | 分场景 |
| **coverage** | 0.85（S0 体检）/ 0.7（S1 评分缺省）/ 回填带 0.65–0.85（probe-scoring、D4；代码缺省 0.7，TR-26） | INDEX 只解释了前两层 |
| **alphaCount 饱和** | 5000（probe-scoring 拥挤罚）/ 10000（RA 步 2 #6、hypothesis-first）/ 30000（FQ-03） | 一处 |
| **tier 分位** | P80/P55（文档）vs P60/P30（代码缺省，TR-26） | 代码 |
| **并发 C** | 5（陈旧）/ **7**（config）；安全瞬时 ≤6（config）/ ≤7（wqb-concurrency §8，WC-03）/ ≤10（monitor） | config |
| **PPA Sharpe** | 1.0（`compute_webdata_failed_counts`、submit-alpha）/ 1.3（`pre_submit_check`）/ 1.58（judge，JD-09） | config PPA 口径 |
| **窗口** | 标准 `[1,5,22,66,252,504,1008,1260]`；SOP 示例出现 10/20/42/50/189/240/250/500/1000（HP-07/17、HF-05、SP-08、PP-13、DF-03） | 白名单 + 证据脚注 |

**方案**：文档中出现的**阈值字面量**要么写成“见 `config.X`”，要么带 `<!-- from config.X -->` 标记并由机检核对（X-17 #4）；`config` 内把“平台线”与“内部线”按检查名分开登记。

---

### X-12　日期快照与硬编码清单

带日期的**状态**被当作**规则**：`stop_rules_override`“GBR 至 09-30”（RA-117，距今 1 天）；区域数据集计数“HKG 209 / KOR 192 / EUR 178”（AR-10、PP-22）；“USA 133 / MEA 19 / IND 18 / KOR 13 / EUR 7”（SP-03）；monitor 的 `YPgAa3WR`/v52b/ds 舰队（BM-05/09/11）；INDEX 的 2026-09-19 区域硬事实（IX-23）；区域名单“13/14”“AMR/JPN 未启用”（RA-119、CM-19、DE-02）。**方案**：快照一律带 `as_of` + 失效条件，或改为命令生成；区域相关事实进各区 profile，由 `config.REGIONS` 校验。

---

### X-13　DB 单轨 vs 文件产物

**铁律**（INDEX L35）：战役产物只写 DB；**仍要求写文件的文档**：OP-06（回测后追加写“指定的文本文件”）、IR-02（`alpha_list.json` 交下游）、SA-03（“进度真相源=输出 CSV”）、RD-21（`WAVE_LEDGER.md` 追加）、FI-05（`final_expressions.json`）、TR-06（build_wave 文件模式）、BM-15（`methodology_rules.json` 计数）、HF-04/HF-09（`data/field_semantics/*.yaml`、`hypothesis_ledger/*.jsonl`）、IX-08（S3 产物 `alpha_list.json`）。

**方案**：把“允许写的文件”分五类并各给目录与是否入库：A 真相源（仅 DB）；B 运行态缓存（checkpoint/status CSV：可读、不作交接）；C 静态配置（json）；D CLI 临时 `@file`（临时目录、用后清理）；E 人读产物（由 DB 生成，`reports/`）。文档中的每个文件路径须归入其中一类（机检）。

---

### X-14　可移植性：Windows / PowerShell / 固定偏移

| 问题 | 条目 |
|---|---|
| `$WQ_PY` 只定义了 `Scripts/python.exe` | IX-03 |
| 裸 `python` 与 `$WQ_PY` 混用 | SC-07、JD-13、PB-06、SB-24、IX-22 |
| PowerShell 与 bash 混用（同一文件两种 shell） | SB-24、TK-16、JD-13、BM-14 |
| `<SKILL_ROOT>` 占位符不可解析（含钩子命令） | PW-01、SC-07、JD-13 |
| `Get-CimInstance Win32_Process`（无 Linux 等价命令） | BM-04 |
| 硬编码盘符：`tools/submit_batch.py` 的 `MCP_DIR` 缺省 `d:\coding\...`；本次会话两个 MCP 服务因 `D:/…/Scripts/python.exe` 路径 ENOENT 无法启动 | 本会话实证 |
| ET 固定 UTC-4（`quota_status.py`、`pipeline.py`）；“12:00 GMT+8”只在夏令时成立 | SB-21、IX-22 |
| 相对路径 `cd` / 相对 `outputs/` | JD-13、SC-09 |

**方案**：`$WQ_PY` 按平台分支或提供 `tools/wqpy.{sh,ps1}`；机检禁裸 `python`；shell 统一（推荐 PowerShell 主、附 bash 等价）；时区用 `America/New_York`。

---

### X-15　等待 / 退避 / 卡住阈值

| 场景 | 现有取值（出处） |
|---|---|
| 提交后等待翻转 | 40 s（judge）/ 60 s（`_poll_submit_until_resolved` 6×10 s）/ 180 s（`verify_timeout`、fallback）/ 2–3 min（submit-alpha #3）/ 4 min（补发前）（SB-10、JD-04） |
| prod 相关性轮询 | 15 s × 900 s（`super_build`、how-to-pass）/ **30 s × 3600 s**（`check_correlation`）/ 单并发 `correlation_busy` 立即返回（HP-11） |
| 429 退避 | `Retry-After` + 指数（MCP）/ `retry_after + attempt*10`（fallback 脚本，SB-09）/ “30+15s×n 会空转”/ RA“指数退避/降并发”（RA-78） |
| 卡住判定 | 3 分钟无进展（SA-03/WC）/ **60 分钟**（`poller.py stall_minutes=60`，BM-13）/ `ASYNC_STUCK` |
| `super_build.py` | `sleep(30)`（上一轮计划要求 240 s，未改） |

**方案**：`poll-and-quota.md` 建唯一“等待/退避/卡住阈值表”，其余按键名引用；代码中的字面量取自 config。

---

### X-16　算子与表达式知识：SOP 里的例子要过自家闸

- **VECTOR**：`platform_constraints.vec_rules`——VECTOR 字段须先 `vec_*` 聚合、MATRIX 禁 `vec_*`、VECTOR 禁直接 `ts_backfill`（KOR 24/24 ERROR 实证）；DF-04（“VECTOR 不要包 `vec_*`”）、EX-04/EX-08、闸 3 三处口径需对齐。
- **幽灵/未知算子**：`ts_median`（幽灵）、`scale_down`、`ts_event_*`（known_ops 无、闸 8 强制）（DF-08）；`vec_mean`（应 `vec_avg`，EX-08）；`is_placeholder`（PP-12）；`rank_by_side`（不在 known_ops，HP-17）。
- **非标窗口**：例子里的 10/20/42/50/189/240/250/500/1000（`window_whitelist_enforce=false` 仅 warn）。
- **hump / bucket / quantile 元数** 说法冲突（RD-18、PP-18）。

**方案**：SOP 中所有 fenced 表达式经 `gate.py`（0/1/3/4/5/9）与 `known_ops` 检查，反例显式标记；`ts_event_*`/`scale_down` 以 `get_operators` 实测裁决后**同时**更新 `known_ops`、闸 8 与 SOP。

---

### X-17　守护体系：形式有测试，内容无检查

**已有**：frontmatter、边界段存在、MCP 工具/节点计数、GEM 内嵌副本、`sync_skills --check`。**本次机检**（`check_skills.py`）能抓到但**未接入 CI**：链接（182 条断 1）、路径 token（91 处不存在）、CLI flag（606 个核对）、MCP 工具名与参数（2 未注册、4 处参数不在签名内）、阈值字面量、重复段落、触发词重叠、孤儿文档（25）、互引对称。

**已知的机检盲区**：机检 D 只核“flag 名是否在同目录任何脚本出现”，**不解析子命令**——BM-14 的 4 条错误命令（`wave upsert --extra`、`registry add-dead-end` 缺必填、`ledger set-verdict --wave/--verdict`）它一条都没抓到。

**建议新增 / 升级的检查**：

| # | 检查 | 依据 | 成本 |
|---|---|---|---|
| 1 | fenced 命令 → 目标 argparse **子命令级**解析（必填/未知 flag） | BM-14 | S |
| 2 | MCP 调用的工具名与参数 ↔ 签名 | SB-06、EX-02 | S（已有 E） |
| 3 | 链接与路径 token，含 `references/**` 与 reference.md | IX-21、SC-07 | S（已有 B/C） |
| 4 | 阈值字面量必须带 `from config.X` 标记并与 config 一致 | X-11 | M |
| 5 | fenced 表达式过 gate 0/1/3/4/5/9；反例标记 | X-3、X-16 | M |
| 6 | ledger 键目录 + “每个被读的键必须有写入方” | X-7、IX-20 | M |
| 7 | 闸表 / 区域表 / 工具计数由代码生成并比对 | IX-05/11 | M |
| 8 | verdict 词表登记；文档出现的状态词必须在登记表 | X-5 | S |
| 9 | “唯一/权威”宣称登记表 | X-2 | S |
| 10 | `last_verified` 必须随内容哈希变化；>30 天告警 | 33/33 同日批量戳 | S |
| 11 | 文档内“未来日期条件”（如 2026-10-12、2026-11-01）到期前告警 | X-19 | S |
| 12 | 边界段“不做”动作词在正文的“仅引用”标记 | IX-19 | M |
| 13 | 守护输入可指定（`WQ_SKILLS_DIR`），环境耦合测试与内容测试分开 | IX-21（本次 4 项失败均为环境） | S |
| 14 | 禁裸 `python`；禁 `.env` 读取指令；hooks/allowed-tools 白名单 | X-9、X-14 | S |

---

### X-18　“声明存在、实现缺位”清单

| 声明 | 现实 | 条目 |
|---|---|---|
| S6“OS 表现监控”与 BLUE→GREEN/YELLOW/RED 重着色 | 无判据、无工具；`os_feedback.py` 已归档，toolkit 仍列为活跃 | BM-01、TK-07 |
| robustness = S4→S5“必经闸” | 无任何代码读取其判定 | RB-03 |
| 步 9 写 `submit_ready_blocked`“下一轮 S0 读取” | S0 读的是 `saturated_datasets`（且无写入方） | RA-113、TK-18 |
| SA“如何创建” | SKILL 无创建调用；`super_build.py select/probe` 与 `workflow_superalpha` 未提 | SP-13 |
| judge 的 `WAIT_THEME_ROTATION`、PPA 颜色/主题核对 | 脚本未实现 | JD-09 |
| judge 引用 robustness 结论作证据 | 脚本不读 | JD-05 |
| repair“配方已上移 optimization-v1” | 承接侧零命中 | RE-01 |
| repair“修复记录在 `trajectory_steps` 可见” | 该表除单测外无生产写入方 | RE-10 |
| explain-alphas“换概念前查与既有 book 概念重叠” | 6 步模板无该程序 | EX-01 |
| PPA“web UI 提交”后的回写 | 无交接单、无回写命令 | SB-22 |
| `prescreen_gate.py`“节点内嵌接线待跟进” | 待办写进 SOP | FQ-07 |
| hypothesis-first 的 catalog / field_semantics 目录 | 不存在；RA 步 2 仍强制路由（上一轮 P0-8） | HF-01 |
| methodology_rules 的 `times_applied` 回写 | 无命令、无公式 | BM-15 |
| “提交配额复检” | 唯一来源是 POST 响应 → 复检 = 再 POST | SB-15 |
| `check_correlation` 的“Redis 本环境不可用” | Redis 只是可选缓存；真正风险是 3600 s 阻塞轮询 | HP-11、RB-17 |

---

### X-19　时间炸弹

| 日期 | 会发生什么 | 涉及 | 处置 |
|---|---|---|---|
| **2026-09-30** | GBR `stop_rules_override` 到期，停止规则恢复约束 | RA-117 | 到期前复核或续期 |
| **2026-10-11 → 10-12** | CLI `--gate-mode` warn → enforce | RA-44、toolkit、AGENTS §8.1 | 翻转后同步 RA/toolkit 的“warn”描述（已有测试扫描） |
| **2026-11-01** | 美国 DST 结束：00:00 ET 从 12:00 变为 **13:00 GMT+8**；`quota_status.py` 固定 UTC-4、`pipeline.py`“全年 UTC-4”、DB `date_submitted` 为 -04:00 → 日界漂移 1 小时 | SB-21、IX-22 | 改用 `America/New_York` |
| 每次 `last_verified` 批量戳 | 掩盖内容过期 | 全库 33/33 = 2026-09-28 | X-17 #10 |
| 区域平台状态（MEA 关闭、AMR/ALL 选项、ILLIQUID_MINVOL1M 下线） | 快照类事实失效 | SP-05、PP-24、IX-23 | X-12 |

---

## Part C　上一轮评审（2026-09-26）关闭情况

> 对照上一轮 `output_report/skill_review_20260926.md` 的 9 个 P0、整改计划三批、五处断点、重叠簇 A–E。判据：**本次（2026-09-29）在当前文件里逐项核对**；“未复核”表示本轮未逐项验证，不作关闭判断。

**总体**：9 个 P0 —— **完全关闭 0 · 部分关闭 3 · 未关闭 6**。整改计划第一批 8 项（“当天可完成，零代码风险”）—— **0 项完全关闭**。而 33 个 skill 的 `last_verified` 全部是 2026-09-28，批量戳把这一状态遮住了。**review → fix 的环没有闭合**，最直接的机制缺口是：没有“评审条目 → 跟踪 → 关闭证据”的登记，也没有机检去证明某条已修（X-17）。

### C.1 九个 P0

| 上一轮 | 缺陷 | 当前状态 | 证据（本轮核对） | 本报告条目 |
|---|---|---|---|---|
| P0-1 | datafield-exploration 用 `ts_median` / `scale_down` / `ts_event_*` | ❌ **未关闭** | SKILL.md L56（`ts_median`，幽灵算子）、L60–61（`scale_down`）、L73–75（`ts_event_sum/count/mean`）仍在；`known_ops` 无后两者，而闸 8 又强制 `ts_event_*` | DF-08、EX-08、HP-19 |
| P0-2 | ppa-mining V9 `scale(…)+scale(…)*0.35` 加权混合 | ❌ **未关闭** | SKILL.md L166–172、L220 仍在，无“历史范式”标注；**补充**：实测 gate.py 对该形态**放行**（权重在右），上一轮“被闸 5 block”对该形态不成立 | PP-13、X-3 |
| P0-3 | submit-alpha 教用 `activities/submissions` 判当日配额 | 🟡 **部分** | INDEX L417–420 与 `tools/quota_status.py` 已改正；但 submit-alpha 同文 L191（不可用）与 **L264（仍叫人用）** 矛盾，`pipeline.py:206` 仍**优先**读 activities | SB-15、IX-22 |
| P0-4 | 异步受理无补发（judge/submit-alpha/superalpha + `submit_alpha` 节点） | 🟡 **部分** | `submit_alpha` 节点已补 re-POST/`ASYNC_STUCK`（`nodes/submit_alpha.py` L263–288）；submit-alpha 四态表与 judge L113–114 已写；**未改**：MCP `_poll_submit_until_resolved` 窗口仍 60 s、`super_build.py` `sleep(30)`、superalpha 无异步语义、“二次 POST”在 REGULAR/SUPER 含义未对齐 | SB-10、JD-04、X-15 |
| P0-5 | GEM 缺“LLM 402 与 `--ideas-file` 绕行” | ❌ **未关闭** | brain-make-some-gem SKILL.md 全文无 “402”；失败表仍缺该项（RA 步 4 引言有） | GM-14 |
| P0-6 | repair 声称配方已上移 optimization-v1，承接侧零命中 | ❌ **未关闭** | “5 轴/6 武器/分布形态/体检硬门复验/幽灵算子清单”在 optimization-v1 均零命中；INDEX L113 仍以此为卖点 | RE-01、IX-07 |
| P0-7 | research / news-sentiment 要求跑不存在的 `wqb` CLI | ❌ **未关闭** | brain-alpha-research L60–61（`wqb research`、`wqb settings`）、news-sentiment L70（`wqb news-refresh-portfolio`）仍在 | AR-12、NS-04 |
| P0-8 | hypothesis-first catalog 仅 3 条 / 目录不存在，而 RA 步 2 强制路由 | ❌ **未关闭** | `data/hypothesis_catalog`、`data/field_semantics` 仍不存在；RA 步 2 #6 仍强制切换；未标 dormant | HF-01、HF-10 |
| P0-9 | sim-alphas S1/S2 产物列写文件路径 | 🟡 **部分** | sim-alphas L61–62 已把 `alpha_list.json` 标为“已废弃的文件模式，仅排障/兼容”、`simulation_status.csv` 标为“进度缓存”；INDEX S3 行仍写 “`alpha_list.json` → IS 指标 + status CSV” | SA-03、IX-08 |

### C.2 补充 P1

| 上一轮 | 当前状态 | 说明 |
|---|---|---|
| optimization-v1 四处把 `check_correlation`（依赖 Redis、会等死）当默认取数 | ❌ 仍在（L45、L116、L121） | 且“依赖 Redis”的理由本身已被证伪：Redis 只是可选缓存，真正风险是每 30 s 轮询、最长 3600 s 的阻塞与账号级单并发（HP-11、RB-17） |
| robustness 把 `2Y>1.6` 当合格线；“衰减比”两义 | ❌ 仍在 | RD-05（1.6 vs 1.58）；衰减比定义仍为 `last_year/full_period` 且与 IS→OS 衰减同名（RB） |
| ra-pipeline 正文“registry 注册 8 个 / 节点 9” | ✅ **已关闭** | 该表述已不在 SKILL.md（本轮 grep 无命中） |

### C.3 整改计划第一批（“止血”8 项）

| # | 动作 | 状态 |
|---|---|---|
| 1 | 删 `activities/submissions` 判配额 | 🟡（见 P0-3） |
| 2 | 新增异步受理补发 | 🟡（见 P0-4） |
| 3 | GEM 补 LLM 402 / `--ideas-file` | ❌ |
| 4 | 删/替换幽灵算子 | ❌（P0-1） |
| 5 | V9 加红字并改写 | ❌（P0-2） |
| 6 | 删不存在的 `wqb` CLI | ❌（P0-7） |
| 7 | FE 示例 `source: "standalone"` → `manual` | ❌（`brain-data-feature-engineering/SKILL.md` L245 仍为 `standalone`，FE-02） |
| 8 | hypothesis-first 标 dormant / 路由加前置 | ❌（P0-8） |

### C.4 第二批与第三批

| 项 | 状态 | 说明 |
|---|---|---|
| 9 代码补 re-POST；窗口 60→240 s；`super_build` 30→240 s | 🟡 | 节点已补；MCP 窗口与 `super_build.py` 未改 |
| 10 闸编号机械守护 + 补闸 9 | ❌ | INDEX 与 gate.py 模块头仍缺闸 2b / 2b-2 / 9（IX-11） |
| 11 重写 sim-alphas 产物列 | 🟡 | 见 P0-9 |
| 12 统一凭据链 | ❌ | 凭据来源已增至 ≥8 种（JD-07、SB-04、IR-05、FB-10、NM-14、FI-02、SC-07） |
| 13 孤儿节点接进 SOP 或标 standalone | 🟡 4/9 | `alpha_booster`/`auto_harvest`/`modeb_improve` 已在 RA 提及，`field_understanding` 已删；`auto_pyramid`/`auto_review`/`gem_wave`/`inventory_scan`/`unified_gate` 仍不在 RA SOP |
| 14 RA 步 1 `--regions all` 改逐区串行 | ❌ | RA L96 仍为 `build_gate_prior_from_inventory.py --regions all` |
| 15 how-to-pass §4 升为全区权威，并补 §0“判定层级 + POST 唯一预检” | 🟡 | §4 存在；§0 未补；且 §4 的“WARNING 就别提”与 submit-alpha“WARNING 不挡”冲突（SB-14） |
| 重叠簇 A（字段/数据集探索 4 份 → 1 份 + 决策矩阵） | ❌ | 仍是 4 个 skill |
| 重叠簇 B（WebDataScope 预筛 4 处） | ❌ | FQ-04、FQ-07 |
| 重叠簇 C（区域优先级 3 处打架） | 🟡 | research 已在正文标注与 `REGION_PRIORITY` 冲突（AR-10）；ppa-mining §8 仍把 2026-08 快照当行动指令（PP-22） |
| 重叠簇 D（点塔规则 2 份） | ❌ | 两份仍在，且共享同样的逻辑错误（JD-15）；`_tower_map.py` 断链已改为真实工具 ✅ |
| 重叠簇 E（S2 生成 3 份 / `source` 枚举） | 🟡 | 定位修正已写，但示例仍会让 GEM 忽略人工产物（FE-01/02） |
| `last_verified` 机械守护 | ❌ | 33/33 同日批量戳 |
| 术语统一（衰减比 / 合格线） | ❌ | X-4 |

### C.5 五处断点

| # | 断点 | 状态 |
|---|---|---|
| 1 | 配置包 → `settings.json` 无责任人 | 🟡 RA L874 已写“配置包写回 settings.json”，但句子不通（RA-125），matrix 侧仍无该字样 |
| 2 | 波号体系双轨 | 未复核 |
| 3 | S1/S2 产物写成文件路径 | 🟡（P0-9） |
| 4 | 状态 CSV 命名 | 🟡 定位已澄清（sim-alphas L18），命名一致性未复核 |
| 5 | S3 出口缺台账回写 | 未复核 |

### C.6 本轮新增的“回归型”问题（上一轮之后的代码/文档变更引入）

- **`wave<N>_verdict` / `s6_verdict_<wave>` 旧键**：RA 于 2026-09-28 声明 `wave_results.verdict` 为唯一结论源，但 6 处文档仍在教旧键（X-7）。
- **资格线模型**：2026-09-09 `mode_b_config` 改为“主闸 + 旁路 + 判死线”，3 处文档仍写两分法（X-2 / HP-15）。
- **`submit_verdict` 提交层视图**：2026-09-26 确认恒 404 后，各处文档给出 4 种互相矛盾的说法（SB-03、JD-03、SP-11）。
- **`os_feedback.py` 等 5 个脚本 2026-09-28 归档**：toolkit SKILL 仍在表中列为活跃（TK-07），S6 的 OS 监控失去承接（BM-01）。

---

## Part D　整改路线与写法规范

### D.1 优先级判据

**不可逆动作缺护栏 > 安全边界（凭据/外发/供应链）> 命令不可执行 / 状态机不可达 > 互相矛盾 > 口径漂移与重复 > 文风**。同级内先修“被引用最多的单一真相源”，再修下游副本。

### D.2 三批整改

**第一批 · 止血（纯文档，1–2 天）**——每项都是“改字，不改逻辑”。

| # | 动作 | 主要条目 |
|---|---|---|
| 1 | **提交链**：submit-alpha 默认示例拆成“预检 → 用户确认后提交”两步并删不存在的形参；删 judge 的 L274–283 旧口径；superalpha 写出 `super_build.py {select\|status\|probe\|submit}` 四步与 MCP 路径的手工 prod 闸；全库统一“不可逆动作块”（X-9）；所有“POST 零成本探测”改成只读手段 | SB-06/03/13/19、JD-03、SP-13、RC-01、SC-04、HP-03、RB-15、RE-08 |
| 2 | **资格线**：how-to-pass / optimization-v1 / RA 三处改引 `mode_b_config` 判定表；删“未达标即判死” | HP-15/16、OP-18 |
| 3 | **S6 回写**：重写 monitor §14.2 四条命令（真实 flag + `--dry-run`）；`wave<N>_verdict` / `s6_verdict_<wave>` 在 6 处清零 | BM-14、RA-108、RD-21、RP-08、TR-15、ME-02 |
| 4 | **universe 与快照**：monitor §7 改引 `config.REGIONS[region].universes`；删 `ILLIQUID_MINVOL1M`；去掉 SOP 内的日期快照或加 `as_of` | BM-08、PP-24、RD-17、SP-03、AR-10 |
| 5 | **INDEX 修正**：区域表 DEU→probe-only、AMR 战役目录；闸编号表补闸 2b / 2b-2 / 9；`$WQ_PY` 双平台；删“唯一”重复宣称，登记 | IX-03/05/11、X-2 |
| 6 | **算子与例子**：`ts_median` 一律替换；`vec_mean`→`vec_avg`；`scale_down`/`ts_event_*` 以 `get_operators` 裁决；清理 ≥12 处加权混合例子并标注反例 | DF-08、EX-08、PP-12/13/20、HP-05/19、RA-46 等（X-3、X-16） |
| 7 | **凭据与外发**：删除所有“读取 `.env`”“命令行传密码”的指令；judge LLM 默认关闭并列外发字段白名单；fallback 提交脚本删除 | JD-07/10、SB-04/09、SC-07、NM-14、FB-10、IR-05 |
| 8 | **供应链**：pull-brain-skills 默认不覆盖、默认目录与代码一致、增“入库前审查清单”；planning-with-files 修/删钩子；INDEX 增“hooks 必须审查” | PB-01/02/03、PW-01、IX-18 |
| 9 | **配额**：只留一处；`activities/submissions` 说法统一；`America/New_York` 计算；在 2026-11-01 前复核 | SB-15/21、IX-22 |
| 10 | **上一轮遗留 P0**：GEM 补 402 / `--ideas-file`；删 `wqb` CLI；hypothesis-first 标 dormant；repair 配方恢复或撤声明；V9 标历史范式；FE 示例 `manual` | GM-14、AR-12、NS-04、HF-01、RE-01、PP-13、FE-02 |

**第二批 · 接线（小代码 + 机检，3–5 天）**

| # | 动作 |
|---|---|
| 1 | `judge_alpha.py` 删除 `--confirm-submit` 与 `submit_alpha`（加测试断言脚本不含 `POST …/submit`）；vendor `ace_client` 标 deprecated |
| 2 | `submit_verdict`：UNVERIFIABLE 独立退出码；CLI 与 MCP 共用一份实现；删不可达分支 |
| 3 | `_poll_submit_until_resolved` 窗口 60→240 s；`super_build.py` `sleep(30)`→240 s |
| 4 | gate 5：补“权重在右”、`subtract`、中缀减号形态的检测或明确放行政策；覆盖矩阵测试（X-3） |
| 5 | `config`：拆 `platform_is_sharpe_min`(1.25) 与 `platform_2y_sharpe_min`(1.58)；`mode_b_config` 判定表生成文档 |
| 6 | 机检 #1–#8、#13–#14（见 X-17 表）接入 CI；`check_skills.py` 作为起点 |
| 7 | ledger-key 目录（键 / 写入方 / 读取方 / 刷新责任 / 状态）+ “被读的键必须有写入方”测试；waiver 协议（X-8） |
| 8 | 测试环境耦合拆分（`WQ_SKILLS_DIR`；`operators_verified.json` fixture 化） |

**第三批 · 结构（1–2 周）**

| # | 动作 |
|---|---|
| 1 | **SOP 重构**：每个 skill 拆 核心 SKILL.md（≤250 行，每步固定模板，D.3）+ `references/` + 仓库级 `CHANGELOG.md`；先做 ra-pipeline、submit-alpha、superalpha、monitor、toolkit |
| 2 | **合并/退役**：repair → optimization-v1 的 references；点塔规则 → 单份 `pyramid-priority.md`；PPA 两份方法论合并；how-to-pass reference.md 瘦身（删 63 行想法层通识）；judge 收缩为“参考评审”（三职能各一节） |
| 3 | **词表落地**：术语表（X-4）、verdict 分层词表（X-5）、闸/开关总表（X-6）由代码生成 |
| 4 | **补齐缺失承接者**（X-18）：S6 OS 监控与重着色规则（或撤回承诺）、PPA 交接单、SA 创建流程、prod-corr 取数唯一入口 |
| 5 | **`last_verified` 机制**：随内容哈希变化，>30 天告警；评审条目→跟踪→关闭证据登记（上一轮 0/9 完全关闭的直接原因） |
| 6 | **INDEX 拆分**：路由 / 契约 / 变更日志 / 审计叙事（IX-01） |

### D.3 写法规范

#### D.3.1 每一步（或每一段规则）的固定模板

```
### 步 N　<名称>
- 目的：（一句话；产出什么、给谁用）
- 前置（可机检）：（状态/键/表 + 阈值；缺则回步 M）
- 调用：（命令或 MCP 调用，含 `--dry-run`/预检形态；参数以代码 argparse/签名为准）
- 产物：（DB 表/键 + 唯一写入方；文件仅限 X 类，见 X-13）
- 完成定义：（可机检的一句话）
- 失败分支：（症状 → 判据 → 处置 三列表；含“不要重试/不要判死”的情形）
- 不做什么：（反例与原因；不可逆动作用“不可逆动作块”）
- 情景卡：（链接到 D.3.2 形式的具体场景）
```

规则与叙事分离：**规则**在核心文件；**实证/案例**在 `references/`；**日期与变更**在 `CHANGELOG.md`；快照必须带 `as_of` + 失效条件或改为命令生成。

#### D.3.2 情景卡模板

```
### 情景 <ID>　<一句话标题>
- 前置状态：（可观测的量，含阈值与来源）
- 步骤：（每步：命令 + 预期输出）
- 分支：（若…则…；边界值两侧各一例）
- 产物与落点：（DB 键/表 + 写入方）
- 完成定义（可机检）与失败分支
- 反例：（不要做什么，为什么）
```

**示例（草案，参数以代码为准）——情景 S5-01：一颗 REGULAR alpha 从“判定通过”到 ACTIVE**

- **前置状态**：候选 X（IND，type=REGULAR，UNSUBMITTED）；`Failed RA==0 且 pending==0`；`submit_verdict` = UNVERIFIABLE（`GET /submit` 恒 404，属预期）；prod 实测 0.55；robustness = PASS；用户已在本会话明确确认。
- **步骤**：① `workflow_submit_alpha(alpha_id=X, name=…, color=BLUE, tags=[CH_REG, SRC_…], descriptions=<三段式，≥100 词>, confirm_submit=False)` → 预期预检通过（否则停）；② 同参数 `confirm_submit=True`，按 HTTP 状态分支：`200 + success:true` → ④；`201/202` 或 `200 空体` → ③；`403` → 读 `is.checks` 的唯一 FAIL：`REGULAR_SUBMISSION value≥limit` → 记“待次日”，**不判死候选**，结束；其他 FAIL → 回步 7；③ 每 10 s 轮询 `get_alpha_details` 至 `status==ACTIVE`（最长 240 s）；仍 UNSUBMITTED → 先确认 `dateSubmitted` 为空，再 re-POST 一次并再等 240 s；仍未翻 → 记 `ASYNC_STUCK` 并通知用户（不再重试）；④ 回写 S6（`wave upsert --verdict …`）并重跑 `campaign_intel.py pyramid` 确认目标塔 +1。
- **完成定义（机检）**：`status==ACTIVE ∧ dateSubmitted≠null ∧ wave_results.verdict≠null`。
- **反例**：不要用 POST 试探配额；不要在 UNVERIFIABLE 时跳过 prod 实测；不要在 201 后立刻判失败；不要把 `WARNING` 当“不挡”（硬闸类 WARNING ≡ FAIL，SB-14）。

#### D.3.3 建议补的情景卡（跨 skill 汇总）

| # | 情景 | 来自 |
|---|---|---|
| 1 | 一次 REGULAR 提交（正常 / 异步未翻转补发 / 配额 403 / 并行会话用光配额） | SB-25 |
| 2 | SUPER：0→SA、组件恰好 10 颗（self_gate 放宽路径）、近克隆被拒（同构淘汰法） | SP-19 |
| 3 | PPA：交接单模板（8 行）+ 回写；Sharpe 1.2 / PPAC 0.42 候选的判定口径 | SB-22、JD-19 |
| 4 | 多候选点塔排序（塔现状 2/3、1/3、0/3 三候选）+ 过度提交阈值 | JD-19、SB-16 |
| 5 | 本地 SELF 盲区三行决策表 | SC-10 |
| 6 | 判死分级（候选 / 家族 / 波次）+ forum_recon 前置 | HP-16/17、ME-03 |
| 7 | prod 墙首探决策（X-1 的表 + 三个数值例） | X-1 |
| 8 | 修复三张卡：降换手 / 覆盖不足 / 降相关 | RE-12 |
| 9 | 阈值数值例：Fitness 的 12.5% floor、Sub-universe 的 0.433 倍门槛、Sharpe 豁免 10% | HP-04/09/12 |
| 10 | 五张“症状 → 根因 → 动作 → 验收”卡（Fitness / 2Y / CW / Sub-universe / SELF vs PROD） | HP-21 |
| 11 | 概念重叠检查（3 个 ACTIVE 的 book，目标与其中 1 个共享字段族与骨架） | EX-10 |
| 12 | 日常一波收尾（真实 flag）+ 挂起处置 + 20 行合规汇报样例 | BM-18 |
| 13 | prod-corr 取数三种返回（pending / busy / 命中缓存）的处置表 | HP-11 |
| 14 | RA 一次战役的 task_plan（九步）+ 压缩后恢复（五问 → 台账） | PW-10 |
| 15 | 导入外部 skill：审查报告（hooks / allowed-tools / scripts）+ 同名更新 diff + 带 hooks 的拒绝 | PB-07 |
| 16 | 降级运行（无凭据 / 无 LLM key）：输出什么、能否作依据 | JD-19 |
| 17 | gate 失败后的动作表（闸 SEM exit 2、体检硬门、闸 PF、闸 2b、幽灵算子） | RA-67 |
| 18 | 体检包缺失的 waiver 卡（reason_code、有效期、谁批准） | RA-28、X-8 |
| 19 | 库存盘点“够不够”的量化判据 + 一个例子 | RA-18 |
| 20 | 人工步骤暂停点（Brain Labs 脚本需人在浏览器运行 → 停下等回传 JSON） | LB-03、PP-03 |

（每个 skill 的“需情景规范”阶段在 Part A 的热力图末列，共 208 个阶段。）

#### D.3.4 24 处范本（可直接作为改写模板）

| 条目 | skill | 值得模仿的点 |
|---|---|---|
| SB-10 | submit-alpha 关键坑 #1 | **响应四态表**（响应 / 含义 / 处置）+ 实证 id + “另一条独立成因”区分 |
| SC-03 | selfcorr-quick 结构性盲区 | 实证（本地 0.229 vs 平台 0.8392）→ 机理 → 三条使用规则 → 源码出处 |
| HP-07 | how-to-pass §4 CW | **因果链**：症状 → 根因 → 只改一个自变量的对照 → 反例清单 → 行动规则 |
| HP-17 | how-to-pass playbook | **决策树**：先诊断 → 三轴按成本递增 → 有数值的判死线 + “不再调参”止损 |
| RE-03 | repair 1a | **验收标准写法**：目标 + 否定句 + 禁入下游 |
| ME-03、ME-07 | dataset-mining-experience | 判死粒度；反 cherry-pick 护栏（缺失写未核实，不拼接不同候选的最好指标） |
| GM-01、GM-08 | make-some-gem | 所有权 + “不得据此推断”；判死粒度 = 概念 |
| GM-13 | make-some-gem | **症状 → 判据 → 动作**：解析顺序、打印行 `OK/MISSING`、“看到 MISSING 立刻停下”、守护测试 |
| PP-10、PP-26 | ppa-mining | “离线包缺 ≠ 平台缺”+ 反例 + 规则；六条实测约束（症状 → 原因 → 处置） |
| DF-06 | datafield-exploration §7 | 裸 `dataset=` 被静默忽略 → 必须 `dataset.id=`：症状 → 原因 → 规避 4 步 |
| WC-12 | wqb-concurrency | 测 C 的 4 步 + 易踩坑 + 反面知识（429 报文不含数字） |
| TR-30 | probe-scoring | **场景 → 动作 → 理由**（“审 dry-run 看两处异常 → 勿 apply，先查 ac 来源”） |
| TK-20、RA-88 | toolkit / RA | 明写“**别拿它做什么**”（score 与 pyramid_view 勿相加；Spearman 仅 +0.086 不抬 IS 阈值） |
| RA-116 | RA | 不可逆节点“不入链”的声明：清晰、可检、有理由 |
| RC-06 | prod-corr-avoidance §7 | 触发 + 现状 + 4 条强制纪律，可直接执行 |
| RR-08 | IND profile | 辅助腿入场范例：`trade_when` 慢开关 + 滞回带 + 无效结构反例 |
| NM-09 | next-move | 一段话定义 `entry_verdict` 三态默认行为 |
| FR-02 | forum-browse Auto-Send | A1–A8 条件清单最可检（恰好 1 条、零推断、列出禁用词、自检清单与日志字段） |
| EV-03 | expression-verifier | 明确写出“**本层做不到什么**” |
| SP-10 | superalpha | 参数—指标对照表（篮宽 × decay；decay 12→300 逐档） |
| BM-13 | monitor §13 | 判停参数与代码逐值一致，可核对 |
| IX-05 | INDEX 区域清单 | 单一事实源 + “四处同步” + 漂移事故 |
| IX-15、IX-20 | INDEX | 4 条可测纪律；共享产物归属表的表头设计（唯一写入方 / 只读消费方 / 刷新失效责任 / 逃生阀） |

共同特征：**症状 → 判据 → 动作 → 反例**，并写明**“不要拿它做什么”**与**适用范围**。

### D.4 建议新增的机械检查

见 X-17 的 14 项表；**优先序**：#1（fenced 命令子命令级解析）、#5（SOP 例子过闸）、#6（ledger 键目录）、#10（`last_verified` 与内容哈希）——这四项分别对应本轮发现的“命令不可执行”“政策与闸分叉”“无主键/多写入方”“批量戳掩盖”四类最高频问题。

---

## 附录

### 附录 A　覆盖范围与局限

**完整通读**：`Claude/skills/` 下 33 个 `SKILL.md` 与 `INDEX.md`。

**抽读（逐节已标注）**：ra-pipeline 的 `references/`（decision-table、ra-campaign-prompt、webdatascope-failed-gates、concept-taxonomy-map、prod-corr-avoidance）与区域 profile（13 个，读 front-matter + 关键段）；campaign-toolkit 的 `references/`（gate-rules、poll-and-quota、ledger-schema、campaign-dir-contract、selection-plan、probe-scoring-v2、enhancement-v2、S2_COMPLIANCE_*、DIVERSITY_EXTRACT_*）；forum-browse 的 9 个 references（≈1130 行，仅抽样）；brain-alpha-research 的 7 个 references（852 行，仅抽样）；how-to-pass 的 `reference.md` 与 playbook（全读）；judge 的 rubric / config / vendor / 脚本关键段（未读 21 篇语料正文）；superalpha / submit-alpha 相关脚本 `tools/super_build.py`、`tools/submit_verdict.py`、`tools/submit_batch.py`、`tools/quota_status.py`（关键段）。

**局限**

1. **未调用 WQ 平台**：涉及平台行为的断言（如“GET /submit 恒 404”“PENDING 不挡提交”“ts_event_* 是否可用”）来自 skill 自述与代码注释，标注为“文档称/代码注释称”，未独立复现。本会话的 `wq-brain-http` / `wqb-db` MCP 服务因 Windows 绝对路径（`D:/…/Scripts/python.exe`）ENOENT 未连接。
2. **严重度是评审判断**：P1/P2/P3 的划分依据在 0.2；同一问题在不同读者眼中可能差一级。数量统计（675 条问题）不宜当作质量分数——同一根因会在多个 skill 里各记一条。
3. **机检有启发式与误报**：已识别的误报——`write-style-zh.md` 的示例表格“→ url”、`dataset_experience --waves`（flag 在 `src/wqb/research/`，兼容入口是薄壳）、`WQ_VALIDATOR_DIR/verify_expr.py`（占位符）。机检 D 只核 flag 名，不解析子命令（X-17）。
4. **测试运行在容器环境**：见附录 D。
5. **代码核对只覆盖被文档引用的部分**：不构成对代码本身的审查。

### 附录 B　复现命令

```bash
# 机械检查（只读；输出即 reports/skills_review_20260929/check_skills_output.txt）
world-quant-brain-mcp/.venv/bin/python reports/skills_review_20260929/check_skills.py            # 全部
world-quant-brain-mcp/.venv/bin/python reports/skills_review_20260929/check_skills.py --section D,E

# 现有守护测试
world-quant-brain-mcp/.venv/bin/python -m pytest tests/unit/test_skill_integrity.py \
    tests/unit/test_skill_boundaries.py tests/unit/test_docs_consistency.py -q
```

**X-3 的 gate 5 覆盖矩阵**（复现片段，只读）：

```python
import json, re, sys, importlib.util
pc = json.load(open('Claude/skills/wq-brain-campaign-toolkit/config/platform_constraints.json'))
sys.path[:0] = ['Claude/skills/wq-brain-campaign-toolkit/scripts', 'src']
spec = importlib.util.spec_from_file_location('gate_mod', 'Claude/skills/wq-brain-campaign-toolkit/scripts/gate.py')
g = importlib.util.module_from_spec(spec); spec.loader.exec_module(g)
for e in ['rank(A)*0.6 + rank(B)*0.4', 'subtract(rank(A), rank(B))', 'add(rank(A), -rank(B))']:
    regex = [p['name'] for p in pc['poison_patterns'] if p.get('regex') and re.search(p['regex'], e)]
    print(e, regex, g._detect_weighted_mix_structural(e), g._detect_equal_weight_leg_add(e, set()))
```

**其余关键核对的入口**

| 论断 | 核对位置 |
|---|---|
| `SUBMITTABLE` 不可达；退出码语义 | `tools/submit_verdict.py`（docstring L1–30；判定 L173–190）、`world-quant-brain-mcp/tools_ops.py::submit_verdict` |
| `workflow_submit_alpha` 形参 | `world-quant-brain-mcp/tools_workflow.py`（`confirm_submit` 默认 False）、`src/wqb/workflow/nodes/submit_alpha.py` |
| 预检规则 | `world-quant-brain-mcp/brain_mixin_simulation.py::pre_submit_check` |
| `check_correlation` 轮询 / Redis 可选 | `brain_mixin_spcread.py::_poll_production_correlation`、`brain_mixin_transport.py`（Redis 可选缓存与锁回落） |
| 配额两套实现 | `tools/quota_status.py` 与 `Claude/skills/wq-brain-campaign-toolkit/scripts/pipeline.py:175–215` |
| 资格线模型 | `src/wqb/workflow/mode_b_config.py` |
| PPA failed-count 口径 | `src/wqb/config.py::compute_webdata_failed_counts` |
| §14.2 命令 | `_lib/wave_results.py`（`upsert`）、`_lib/registry.py`（`add-dead-end` / `add-win`）、`_lib/ledger.py`（`set-verdict`） |
| pull-brain-skills 默认目的地与 `rmtree` | `Claude/skills/pull-brain-skills/scripts/pull_skills.py` |
| Stop 钩子占位符 | `bash -c '<SKILL_ROOT>/planning-with-files/scripts/check-complete.sh'`；`tools/sync_skills.py` 无 `<SKILL_ROOT>` 替换 |
| DEU / AMR 与 INDEX 区域表 | `Claude/skills/wq-brain-ra-pipeline/references/regions/DEU.md`（第 3、56 行）；`tracking/AMR/config/` |
| 闸 2b / 2b-2 / 9 | `gate.py` L360、L369、L464 |
| 并发常量 | `src/wqb/config.py::CONCURRENCY` |

### 附录 C　机械检查摘要（`check_skills.py`）

| 节 | 检查 | 结果 |
|---|---|---|
| A | frontmatter | `last_verified` 33/33 = 2026-09-28；description 最长 702 字（toolkit） |
| B | markdown 相对链接 | 182 条，断 1（`write-style-zh.md` 示例，误报） |
| C | 反引号路径 token | 91 处不存在，80 处歧义（多个候选根目录） |
| D | CLI flag | 核对 606 个，缺失 3（`--waves` 误报；`campaign.py --delay`；RA `pipeline.py --concurrency`） |
| E | MCP 工具与参数 | 2 处未注册工具（`submit_alpha`、`get_submission_quota`，均在“反面教材”语境）；4 处参数不在签名内（`get_datafields(instrument_type)`、`workflow_submit_alpha(dataset/wave/expr_family)`） |
| F | 阈值字面量 vs `config` | 78 行（见输出；汇总见 X-11） |
| G | 跨文件重复段落 | 48 行；含 ppa-mining 与 ra-pipeline 副本（Jaccard 0.50）、点塔规则两份 |
| H | 结构信号 | 平均 2.5 处日期括号 / 100 行；有显式失败分支节 6/33、产出节 5/33（按标题匹配） |
| I | description 触发词重叠 | 42 行；“提交”“相关性”“表达式”等被多个 skill 命中 |
| J | 孤儿文档 | 25 个 md 无人引用（多为 references） |
| K | 互引对称性 | 60 行，例：repair ← judge / hypothesis-first / robustness 无回指 |

### 附录 D　本轮守护测试运行

`pytest tests/unit/test_skill_integrity.py tests/unit/test_skill_boundaries.py tests/unit/test_docs_consistency.py -q` → **351 passed / 4 failed / 2 skipped**。4 项失败均为**环境耦合，不是 skill 内容缺陷**：

- `test_every_skill_dir_has_skill_md`、`test_frontmatter_name_matches_dir[session-start-hook]`：守护对象是“Agent 实际加载的 `~/.claude/skills`”（`_resolve_skills_dir()`，设计如此），容器里该目录含非仓库目录 `synced`、`session-start-hook`；
- `test_operator_configs_consistent`、`test_template_families_only_use_verified_operators`：依赖被 `.gitignore`（`data/`）排除的 `data/operators_verified.json`，**干净克隆必失败**。

（`test_mcp_tool_counts_match_index`、边界段守护等通过。）
