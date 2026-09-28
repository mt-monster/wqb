# 全量 skill 评审与编排连贯性裁决

> 日期：2026-09-26 · 视角：资深量化工程 · 目标：能否稳定挖出**可提交**因子
> 覆盖：仓库 `Claude/skills/` **33 个** SKILL.md 全量通读（5,342 行）+ workflow 19 节点 dry-run 实证

---

## 0. 结论先行

**1. 编排主干（ra-pipeline）设计质量很高，但它是"九步的文档"，而引擎已经长到十九个节点。**
ra-pipeline v2.2（764 行）的三角分工、失败分支、Artifact 契约、反模式写得扎实；但正文仍写"registry 注册 **8** 个节点 / 节点 **9**"，而实际 **19 个**——**9 个节点（`inventory_scan` / `auto_harvest` / `auto_review` / `auto_pyramid` / `alpha_booster` / `modeb_improve` / `field_understanding` / `gem_wave` / `unified_gate`）在 SOP 里从未被提及**，是"造好了没接线"的孤儿。

**2. 真正的风险不在"文档写得好不好"，而在四类会直接害人的内容：幽灵算子、被禁的加权混合范式、不存在的命令、过时的配额口径。** 这四类共 9 处 P0，照做即损失整批回测或整天配额。

**3. skill 体系存在显著职责重叠**：字段/数据集探索有 **4 份并存、4 套分类法**；WebDataScope 预筛 **4 处**；区域优先级 **3 处打架**；点塔规则 **2 份逐字重复**且都指向不存在的文件。

**4. 与"能否提交"最相关的一条：提交类 skill 集体停留在「同步提交」心智模型。** 异步受理的补发规则、提交响应形态③、同族挤压规律——这三条已在仓库实证里反复确认，却**零个 skill 记录**。这正是本会话 3 颗 alpha 悬空 >24h 的根因。

---

## 1. 评审覆盖矩阵（33 个 skill）

层号：`L-RA`编排入口 / `L-PRE`查表 / `L-TOOL`执行引擎 / `L0`情报 / `L1`数据集字段研究 / `L2`表达式生成 / `L3`回测并发 / `L4`优化诊断 / `L5`判定提交 / `L6`监控复盘 / `L7`元技能

| # | skill | 层 | 行 | 处置 | 核心问题 |
|---|---|---|---|---|---|
| 1 | wq-brain-ra-pipeline | L-RA | 764 | **改** | 节点计数陈旧（8/9 vs 19）；步1 用已知必崩的 `--regions all` |
| 2 | wq-brain-campaign-matrix | L-PRE | 136 | 改 | P0 JPN/AMR 启用断言与 INDEX 矛盾；回写入口三处口径不一 |
| 3 | wq-brain-campaign-toolkit | L-TOOL | 346 | **改** | P0 闸编号缺闸9；§1.x 与 §6 自相矛盾（掩盖默认常开的闸6） |
| 4 | brain-sim-alphas-in-batch-and-track | L3 | 203 | **改** | **P0** S1/S2 产物列写文件路径（实际已全切 DB）；`submit` 默认 True 未警示 |
| 5 | wqb-concurrency | L3 | 112 | 改 | C=5 旧口径未清；凭据第四套；缺槽位仲裁 |
| 6 | brain-inspect-raw-template-create-setting | L3 | 92 | 改 | 硬编码本机盘符；波号双轨靠隐式兜底 |
| 7 | brain-next-move-analysis | L0 | 71 | 微调 | 门槛数字外溢（违反 config.py 单一事实源） |
| 8 | wq-brain-ppa-mining | L0 | 314 | **改** | **P0** V9「突破版范式」是加权混合，被闸5 block 却标最佳参数 |
| 9 | brain-forum-browse | L0 | 247 | 微调 | 写工具不存在但"每轮必贡献"，豁免条件埋太深 |
| 10 | alpha-template-labs-data-analysis | L0 | 91 | 改 | **P0** 唯一说明入口是坏链；跨 skill 指针失效 |
| 11 | brain-alpha-research | L1 | 54 | **改** | **P0** 要求跑 `wqb research/settings`（CLI 根本不存在） |
| 12 | brain-alpha-research-field-quality | L1 | 69 | 改 | P1 把被禁的 `recommend_datasets` 当预筛等价替代 |
| 13 | brain-alpha-research-hypothesis-first | L1 | 98 | **停用/改** | **P0** catalog 仅 3 条（要求 ≥20）；ra-pipeline 会自动路由进这条死路 |
| 14 | brain-alpha-research-news-sentiment | L1 | 69 | 改 | **P0** `wqb news-refresh-portfolio` 不存在；Tier A 无 coverage 门槛 |
| 15 | brain-datafield-exploration-general | L1 | 81 | **改** | **P0** 6 法用幽灵算子 `ts_median` / `scale_down`（自称"已验证"） |
| 16 | brain-dataset-exploration-general | L1 | 77 | 改 | 复写第三份评分公式；JPN 约束落后于单一事实源 |
| 17 | brain-data-feature-engineering | L1 | 323 | **改** | **P0** `source` 示例写 `standalone` → 产物永不被 GEM 消费 |
| 18 | brain-make-some-gem | L2 | 129 | **改** | **P0** 未记录 LLM 402 与 `--ideas-file` 绕行（S2 当前 100% 阻塞） |
| 19 | brain-feature-implementation | L2 | 112 | 改 | 两份副本漂移；config schema 同名不同构 |
| 20 | alpha-expression-verifier | L2 | 68 | 保留 | 边界声明是**全仓样板**；仅示例自相矛盾 |
| 21 | brain-alpha-judge | L5 | 285 | **改** | L35「201 约 40s 翻 ACTIVE」与 24h 悬空实证直接矛盾 |
| 22 | worldquant-submit-alpha | L5 | 265 | **改** | **P0** 推荐 `activities/submissions` 判当日配额（有撞墙实证） |
| 23 | wq-brain-superalpha | L5 | 243 | **改** | 「只看 result 不看 value」与「prod≥0.7 不提」同文件内冲突 |
| 24 | wq-backtest-monitor | L6 | 155 | 改 | 三级分类缺 `ASYNC_STUCK` 态；无 ET 日配额概念 |
| 25 | brain-dataset-mining-experience | L6 | 57 | 保留 | 质量高；唯一缺 `allowed-tools` |
| 26 | planning-with-files | L7 | 214 | 微调 | 落盘位置与仓库 DB 单轨铁律冲突 |
| 27 | pull-brain-skills | L7 | 61 | 改 | 无内容扫描即导入可执行脚本（供应链风险） |
| 28 | wq-brain-alpha-optimization-v1 | L4 | 189 | **改** | **P0** 四处把依赖 Redis 的 `check_correlation` 当默认取数 |
| 29 | brain-alpha-robustness | L4 | 136 | **改** | **P0** 把 `2Y>1.6` 自造值当合格线；两种"衰减比"同名不同义 |
| 30 | brain-how-to-pass-alpha-test | L4 | 121 | **改** | **P0** 无提交层判定层级；§4 的 CW 一节质量极高，应升为全区权威 |
| 31 | brain-calculate-alpha-selfcorr-quick | L4 | 58 | 改 | 算法正确但口径未书写；L28 缓存路径是错的 |
| 32 | brain-explain-alphas | L4 | 58 | 微调 | 未注入 `users≥50` 的 prod 高危先验 |
| 33 | brain-alpha-repair | L4 | 44 | **改** | **P0** 声称已上移的四节在承接侧零命中（悬空引用） |

**机械校验（我自己跑的）**：33 个 frontmatter **全部完备**（name/description/layer 齐、name 与目录一致）；脚本引用仅 **2 处**悬空（`_gate_waveNN.py` 为生成模板名、`build_wave.py` 在 toolkit）。

---

## 2. 编排连贯性裁决

### 2.1 主干是通的（值得肯定）

读完 ra-pipeline 全文，九步的**接口闭环设计是专业的**：每步都有「目的 / MCP 调用 / 产物 / 失败分支」，任一步 FAIL 就地回退；Artifact 契约表甚至补了"由谁写"这一列（防有人手写脚本绕过写库工具）。区域 profile 注入、停止规则闸（规则 A/B1/B2）、信号天花板闸也都是真在跑的机械判定。

### 2.2 五处断点

| # | 断点 | 上游产出 | 下游期望 | 级别 |
|---|---|---|---|---|
| 1 | **配置包 → settings.json 无责任人** | matrix 声明"参数，非落盘" | `workflow_campaign(S0)` 实际读 `tracking/<R>/config/settings.json` | P1 |
| 2 | **波号体系双轨** | inspect 写 `s2_<ds>_d<delay>` + `pending` | pipeline 按战役波号读，靠 `_wave_aliases()` 静默兜底，文档未声明 | P1 |
| 3 | **S1/S2 产物写成文件路径** | sim-alphas 表写 `reference/*.json`、`candidates/*.json` | 实际已全切 DB（`fields` / `ledger_kv` / `expressions`） | **P0** |
| 4 | **状态 CSV 命名** | sim-alphas 固定 `outputs/simulation_status.csv` 作续跑键 | batch_track 生成带时间戳名 → 续跑键失效 | P1 |
| 5 | **S3 出口缺台账回写** | sim-alphas 输出契约只有 CSV/计数/建议 | wqb-concurrency §8.4 把"未写台账不得开下一波"设为硬阻断 | P1 |

### 2.3 节点孤儿：9 / 19 未接线

`INDEX.md` 记 19 个节点（有测试守护，正确）；但 ra-pipeline 正文写「registry 注册 **8** 个」（L642）与「节点 **9**」（L763）。实际未在任何 SOP 步骤被提及的：

```
alpha_booster · auto_harvest · auto_pyramid · auto_review · field_understanding
gem_wave · inventory_scan · modeb_improve · unified_gate
```

其中 `inventory_scan` 尤其可惜——SOP 步 1 的库存盘点正是用它的底层脚本手工拼命令，而节点已封装好。**建议**：要么把它们接进 SOP 对应步骤，要么在 INDEX 明确标 `standalone`。

### 2.4 横向契约不一致：凭据四套

| skill | 凭据口径 | 是否在引擎解析链内 |
|---|---|---|
| wq-brain-campaign-toolkit §4.3 | `CREDENTIALS_*` → `WQ_*` → `~/.brain_credentials` → MCP config | ✅ 引擎实际链 |
| brain-sim-alphas-in-batch-and-track | `configs/config.json` + `BRAIN_EMAIL/PASSWORD` | ❌ 引擎不认 |
| brain-inspect-raw-template | `~/secrets/platform-brain.json` | ❌ 引擎不认 |
| wqb-concurrency §6 | `.env` + `load_dotenv` | ❌ 引擎不 load dotenv |

照后三份做 → 拿到空凭据 → 401 / FileNotFoundError。

---

## 3. P0 缺陷清单（会真的害人，按危害排序）

| ID | 位置 | 缺陷 | 后果 |
|---|---|---|---|
| **P0-1** | `brain-datafield-exploration-general` 方法5/6 + EVENT 段 | 用 `ts_median` / `scale_down` / `ts_event_sum|count|mean` —— **均不在 103 个已验证算子中，`ts_median` 在 ghost_ops**，却自称"经过验证的 6 法" | 照做 → 幽灵算子 → **整批 ERROR/CANCELLED** |
| **P0-2** | `wq-brain-ppa-mining` §2 / §5 | "V9 突破版组合范式 `scale(...)+scale(...)*0.35`" 是 **加权混合**，被闸5 `severity=block` 拦；却被标"最佳参数 / S=2.23 实测" | 全仓最易被照抄的范式，照抄**必挂闸5** |
| **P0-3** | `worldquant-submit-alpha` L237 | 教人用 `GET /users/self/activities/submissions` 判当日配额 —— **该端点缺 today 字段** | 2026-09-21 据此误判余量，第 3 颗撞 `REGULAR_SUBMISSION(4/4)` 墙，**损失整天名额** |
| **P0-4** | 提交类 skill 集体（judge / submit-alpha / superalpha）+ `submit_alpha` 节点 | 异步受理**无补发**；judge L35 写"201 约 40s 翻 ACTIVE" | 本会话 `O0GjWqeY`/`2rpX85Ax`/`np8VGNz3` 悬空 UNSUBMITTED **>24h** |
| **P0-5** | `brain-make-some-gem` | LLM 通道 402（deepseek 余额）与 `--ideas-file` 绕行**零记录**；且该 skill `last_verified` 是最新的一份 | S2 **100% 阻塞**，而解法在 `run.py:377` 里明摆着 |
| **P0-6** | `brain-alpha-repair` L12 | 声称"5 轴旋转 / 6 武器 / 分布形态映射 / 幽灵算子清单 / 体检硬门复验已上移 optimization-v1" —— 承接侧**关键词零命中** | 修复配方被删且无处可查（**4 处悬空引用**） |
| **P0-7** | `brain-alpha-research` / `news-sentiment` | 要求跑 `wqb research` / `wqb settings` / `wqb news-refresh-portfolio` —— **pyproject 无 scripts 入口，CLI 不存在** | 照做必 `command not found` |
| **P0-8** | `brain-alpha-research-hypothesis-first` | catalog 仅 **3 条**（要求 ≥20）；`data/field_semantics/`、`data/hypothesis_ledger/` 均不存在；节点校验只查"非空" | 而 ra-pipeline 步2 在 `alphaCount≥1万` 时**强制路由**到这里 → 自动触发的死路 |
| **P0-9** | `brain-sim-alphas-in-batch-and-track` L154-156 | S1/S2 产物列写 `reference/*.json` / `candidates/*.json`，实际已全切 DB | L3 入口里唯一写产物路径处，Agent 照读 → "找不到文件" |

**补充 P1（高危）**：`brain-alpha-optimization-v1` 四处把 `check_correlation`（依赖 Redis，本环境不可用、会等死）当默认取数工具；`brain-alpha-robustness` 把自造的 `2Y>1.6` 当合格线，且"衰减比"与 IS→OS 衰减**同名不同义**（最容易读反的一处）。

---

## 4. 职责重叠簇

| 簇 | 涉及 skill | 症状 | 建议 |
|---|---|---|---|
| **A 字段/数据集探索 4 份并存** | datafield-exploration / dataset-exploration / data-feature-engineering / ppa-mining §2 | 四套分类法、四种"这个字段怎么预处理"的答案，**互不引用** | 收敛为 **1 个 L1 skill + 1 张字段决策矩阵**，其余三份降为该 skill 的 `references/` |
| **B WebDataScope 预筛 4 处** | field-quality §2 / research 的 references / ppa-mining §1.1-1.4 / labs-data-analysis | 23 条规则多处复写 | 以 `field-quality` 为唯一入口（已有机器门禁），其余改为指针 |
| **C 区域优先级 3 处打架** | ppa-mining §1.3+§8 / research §12-13 / dataset-exploration 表 | 都说"HKG≈KOR > EUR"，而 `config.py REGION_PRIORITY` 是 **HKG=1 / KOR=2 / EUR=2** | 实证细节只留一份，三份全部退化指针 |
| **D 点塔规则 2 份逐字重复** | brain-alpha-judge L237-256 / worldquant-submit-alpha L170-206 | 逐字重复，且两处都引用**不存在**的 `tracking/_submit_kit/_tower_map.py` | 单点化；judge 已声明"判定权移交"，应删其副本 |
| **E S2 生成 3 份** | make-some-gem / feature-implementation / data-feature-engineering | 非"合并"问题，是**契约断裂**——见 P0-5 + `source` 枚举三方冲突 | 对齐 `source` 枚举即可 |

**边界清晰、无需动的（正面样板）**：`alpha-expression-verifier`（语法层 vs 战役层显式划界）、`brain-forum-browse`（实时论坛 vs 静态语料）、`brain-dataset-mining-experience`（自限为只读台账、不当第二套闸门）。

---

## 5. 优化方案（三批）

### 第一批：止血（改文档，零代码风险，当天可完成）

| 动作 | 位置 | 预期收益 |
|---|---|---|
| 1. 删 `activities/submissions` 判配额，改为"POST submit 的 `REGULAR_SUBMISSION value/limit` 唯一口径" | worldquant-submit-alpha L237 | 杜绝撞 4/4 墙 |
| 2. 新增「异步受理补发」：201 或空体 200 → 轮询 4 分钟仍 UNSUBMITTED → **补发一次 POST**；二次悬空 → `ASYNC_STUCK` | judge L35 / submit-alpha / superalpha | 救回悬空 alpha，不再白占名额 |
| 3. 给 GEM 补「LLM 402 与 `--ideas-file` 绕行」小节 + 失败分支加 402 项 | brain-make-some-gem | **恢复整条 S2 生成链** |
| 4. 删/替换幽灵算子（`ts_median`→`ts_std_dev`、`scale_down`→`bucket(rank(x))`） | datafield-exploration 方法5/6 | 杜绝整批 CANCELLED |
| 5. 给 V9 范式加红字"历史范式，已被闸5 block，禁止照抄"，改写成结构交互 | ppa-mining §2/§5 | 杜绝照抄挂闸 |
| 6. 删三条不存在的 `wqb` CLI | research / news-sentiment | 杜绝 command not found |
| 7. `source` 示例 `standalone` → `manual` | data-feature-engineering §6 | 让绕行方案的上游供给接通 |
| 8. 把 `hypothesis-first` 标 `dormant`，或在 ra-pipeline 路由加"catalog 存在"前置 | 两处 | 堵住自动触发的死路 |

### 第二批：接线（改文档 + 少量代码，1–2 天）

| 动作 | 说明 |
|---|---|
| 9. **代码侧补 re-POST 分支** | `src/wqb/workflow/nodes/submit_alpha.py:262` Step 4 加补发；`_poll_submit_until_resolved` 窗口 60s → ≥240s；`super_build.py:343` `sleep(30)` → 240s |
| 10. **闸编号上机械守护** | 以 `gate.py` 模块头为唯一基准，补 INDEX 与 toolkit 的**闸9**，纳入 `test_docs_consistency.py`（与 MCP 工具计数同款守护） |
| 11. **重写 sim-alphas 的 S1/S2 产物列** | 3 行文件路径 → DB（`fields` / `ledger_kv s0_ranking` / `expressions`） |
| 12. **统一凭据链** | 以 toolkit `_lib/common.py::load_credentials` 为唯一表述，另外三份改"见 toolkit §4.3" |
| 13. **把 9 个孤儿节点接进 SOP 或标 standalone** | 至少 `inventory_scan` 应替掉步 1 手工拼的 `--regions all` 命令 |
| 14. **修 ra-pipeline 步1 的 `--regions all`** | 已知并发必 SSL EOF，改逐区串行（与 inventory_scan 修复合并做） |
| 15. **把 how-to-pass §4（CW 时间平滑）升为全区权威** | 其余五份 L4 引用它；同时给它补 §0「判定层级 + POST submit 唯一预检」 |

### 第三批：结构性减负（1 周）

- **重叠簇 A 四合一**：收敛为 1 个 L1「字段/数据集探索」skill + 1 张字段决策矩阵（输入：type/coverage/frequency/分布形 → 输出：预处理算子），其余降为 `references/`。这是最大的一次结构性减负。
- **重叠簇 D 单点化**：点塔规则只留一份，删 judge 副本，修 `_tower_map.py` 断链。
- **引入 `last_verified` 机械守护**：目前是人工自觉。建议给每个 skill 加"对照代码重扫"检查项（闸编号 / 工具计数 / 产物路径 / 算子白名单四处最易漂移）。
- **统一术语**：`衰减比`（IS 内部尾部 vs IS→OS 跨平台）、`合格线`（IS 层 vs 提交层）必须显式分层，否则评审结论会被读反。

---

## 6. 与"挖出可提交因子"的直接关联

本次评审**不改变**上一份《dry-run 体检与挖掘优化方案》的三杠杆结论，但**修正了执行优先级**：

- 原方案杠杆三「修掉吞名额的 P0」现已被 skill 评审**证实为系统性缺陷**（4 份提交类 skill 集体缺失补发规则），优先级升到**第一批**。
- 原方案杠杆二「闸门判定前移」新增一条更硬的抓手：**先把 `brain-datafield-exploration-general` 的幽灵算子清掉**——它位于 S1 字段理解环节，是当前唯一会**主动制造**整批 CANCELLED 的文档。
- 新增一条原方案未覆盖的阻塞：**S2 生成链当前 100% 卡在 LLM 402**，解法已在代码里（`--ideas-file`），只需写进文档即可恢复整条生成链——这是**投入产出比最高的一项**。

---

## 7. 复现命令

```bash
python tools/audit_node_registration.py          # 四处一致性（19=19=19=19）
python tools/sync_skills.py --check              # 4 安装位漂移
python logs/_tmp_dryrun_audit.py                 # 19 节点 dry-run（结果在 logs/_dryrun_audit.json）
python -m pytest tests/unit/test_skill_integrity.py tests/unit/test_workflow.py -q   # 110 passed
```
