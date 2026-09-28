# 33 个 skills 全量 review + 编排连贯性体检

> 日期：2026-09-26 · 范围：`Claude/skills/` 全部 33 个 skill（约 5,800 行 SKILL.md + 捆绑脚本/参考）
> 方法：编排核心 6 个由主会精读；其余 27 个分 4 组并行深读；**所有结论都用实测/实仓核实，不采信文档自述**
> 门禁：`419 passed`（skill_integrity / docs_consistency / workflow / audit_fixes）· 节点四处同步无漂移 · 5 个安装位 sha256 全一致

---

## 0. 结论摘要

1. **编排骨架是自洽的，断的是"skill 级入边"。** 九步（S-PRE→S6）每步都有「目的 / MCP 调用 / 产物 / 失败分支」，产物契约表把 7 张表的"由谁写"都钉死了。但编排器只写 **MCP 节点名**、不挂 **skill 链接**：`worldquant-submit-alpha`（S5 执行）、`brain-make-some-gem`（S2 引擎）、S1 三件套（`dataset-exploration` / `datafield-exploration` / `data-feature-engineering`）**在 ra-pipeline 里完全没有入边**。读 SOP 的 Agent 会调节点、却不会加载那些 skill 里的关键知识。

2. **发现并修复了一条"沉默的守护失效"**：`test_no_bare_tool_or_node_counts_outside_index` 长期全绿是**假绿**——它用「值黑名单（66|68 / 3[2-9] / 7节点）+ 关键字豁免（行内含 'INDEX'/'唯一基准'/'测试守护' 即放行）」。于是两条过时计数（`68/36/9`、`49`）**靠提一句基准名就逃过守护**，一直漂着。已改为语境约束规则 + 新增反向回归测试（注入负例即变红，已实测）。

3. **提交层的文档与实况三方矛盾，且都以一个"恒 404 的端点"为依据。** 实测：`GET /alphas/{id}/submit` 对**未提交**和**已 ACTIVE** 的 alpha **都返回 404 + 空体**——三份文档却分别写"text/html SPA 壳"/"403 盲区唯一权威"/"可直接走 POST"。**提交层的全部信息只在 `POST` 响应里**（200/201/403）。这直接解释了 3 颗候选"悬空"的误判（详见 §3）。

4. **一个必须纠正的判断**：`SELF_CORRELATION` / `PROD_CORRELATION` 的 **`PENDING` ≠ `FAIL`**（不挡提交）。实测 4 颗候选的 403，**唯一 FAIL 项是 `REGULAR_SUBMISSION: FAIL value=4 limit=4`（配额用尽）**，相关性根本没拦它们。配额用尽是"换日即失效"的外部约束，不是候选缺陷。

---

## 1. 编排连贯性判定

### 1.1 骨架层面：连贯 ✓

| 检查 | 结果 |
|---|---|
| 九步是否各有「目的/调用/产物/失败分支」 | ✓ 全部具备 |
| Artifact 契约（7 阶段 × 入库表 × 由谁写） | ✓ 完整，且 2026-09-05 补过"由谁写"列 |
| 循环停止表（停止规则闸 / signal_floor / 多轴停 / 豁免） | ✓ 与 `thresholds.json` 对齐，阈值不裸写 |
| 工具名映射表（逻辑名 → MCP 调用名 → 定义处） | ✓ 存在且正确（`submit_verdict` 归 `tools_ops.py` 等） |
| 静态门禁 | ✓ 四处同步 19=19=19=19；4 安装位零漂移 |

### 1.2 skill 级入边：4 处断链（已补 3 处）

| 步骤 | 应有入边 | 原文状态 | 处置 |
|---|---|---|---|
| 步 3（S1） | `brain-dataset-exploration-general` → `brain-datafield-exploration-general` → `brain-data-feature-engineering` | ✗ 只用泛词"dataset/datafield exploration"指代 | **已补链**，并写入该层缺失的两条铁律 |
| 步 4（S2） | `brain-make-some-gem` | ✗ 只写 MCP 节点名 | **已补链** + GEM 的 LLM 402 旁路 |
| 步 8（S5） | `worldquant-submit-alpha` / `wq-brain-superalpha` | ✗ 只写 MCP 工具名 | **已补链** + POST 4 形态表 |
| — | `alpha-expression-verifier`（S2 预检） | ✗ 无入边 | 待定（可从 S2 预检环节挂） |
| L0/L7 | `alpha-template-labs-data-analysis`、`planning-with-files`、`pull-brain-skills` | ✗ 无入边 | 可接受（非主链） |

**已补的关键内容**（原本只在别处或完全无处记录）：
- **L1 两层铁律**：① 白名单数据集必须先过 **S1 字段级覆盖审计**（`catalog_<ds>` coverage>0），否则会选到空集——`recommend_datasets` **不校验区域覆盖率**；② 新字段先 `create_multi_simulation(validate_fields=true)` **验活幽灵字段**（DB 有记录但平台报 unknown variable → 提交层 COMPILE_ERROR）。
- **GEM 的 LLM 依赖**：LLM 返回 `402 Insufficient Balance` 时的表现是误导性的「no meta.json within 90s」，且**干跑验证不了 LLM 可达性 → 假绿**；绕行 = 手写 ideas md 走 `--ideas-file`。
- **提交响应 4 形态**与 ②③ 的补发 SOP。

### 1.3 区域 profile 路由：原文自相矛盾（已修）

原文同节三处互相打架：line 54「现有 **12 个** profile」+ 清单**不含 JPN**；line 56/67「profile 未覆盖的是 AMR、**JPN**」。
实况：`references/regions/*.md` = **13 个**，含 `JPN.md`（2026-09-15 补）；`config.REGIONS` = 14。→ 已全部改为 13 / **仅 AMR 未覆盖**。

`test_profiles_subset_of_code_regions` 只校验"profile ⊆ REGIONS"**子集关系**，因此这类"少了一个 profile、清单没更新"的漂移它抓不到。

---

## 2. 发现的缺陷与处置

### 2.1 已修复（18 项）

| # | skill | 问题 | 严重度 |
|---|---|---|---|
| 1 | ra-pipeline 步8 | 「`PASS_CHEAP` 则可提交」与 INDEX「PASS_CHEAP 只过了①，绝不等于可提交」**正面冲突** | P1 |
| 2 | ra-pipeline | profile 12→13、JPN 已覆盖（同一节三处矛盾） | P1 |
| 3 | ra-pipeline | 「registry 注册 8 个」实为 19 | P2 |
| 4 | ra-pipeline | 附录裸写 `68/36/9` 过时计数 | P1 |
| 5 | ppa-mining | 裸写 `68/36`；尾部「**9 个节点**」 | P1 |
| 6 | ppa-mining-experience | 裸写「49 工具」 | P2 |
| 7 | **测试守护** | 值黑名单 + 关键字豁免 → 双重失效 | **P0** |
| 8 | worldquant-submit-alpha | 把 201 异步受理**误诊为 description 过短**；无 4 形态；无补发 | **P0** |
| 9 | worldquant-submit-alpha | `GET /submit`「text/html SPA 壳」→ 实测恒 404 | P1 |
| 10 | worldquant-submit-alpha | `get_alpha_check`（不存在）→ `get_alpha_details`→`is.checks`；补配额真值口径 | P1 |
| 11 | worldquant-submit-alpha / brain-alpha-judge | `_tower_map.py` / `_quota_now2.py` **整个目录不存在**（5 处）→ `campaign_intel.py pyramid` / `quota_status.py` | P1 |
| 12 | brain-alpha-judge | `--with-quota`（已废弃）；`mcp__wq-brain-http__submit_alpha`（不存在）；「201 视为失败是工具 bug」→ 更正为异步受理 | P1 |
| 13 | brain-alpha-robustness | 自称"本副本已非权威版、勿再编辑"（与 INDEX 单源规则相悖）；`get_submission_check`（不存在）；推荐阻塞式 `check_correlation` | P1 |
| 14 | brain-calculate-alpha-selfcorr-quick | 教用 `GET /alphas/{id}/submit → 403` 取实测 PROD/SELF（GET 恒 404）→ 改为 POST | **P0** |
| 15 | brain-how-to-pass-alpha-test | 推荐阻塞式 `check_correlation` → 改本地快筛 + 长窗口轮询 | P2 |
| 16 | wq-brain-alpha-optimization-v1 | `create_multiSim` 非真实工具名（6 处 / 3 文件）→ `create_multi_simulation` | P2 |
| 17 | ra-pipeline 步3/4/8 | 补 3 处 skill 入边 + 两条铁律 + GEM 旁路 + 提交 4 形态 | P1 |
| 18 | 8 个 SKILL.md | `last_verified` 更新为 2026-09-26 | 卫生 |

### 2.2 已修的核心代码/测试

**`tests/unit/test_docs_consistency.py`** —— 把"打地鼠式值黑名单"换成语境约束，并取消关键字豁免：

```python
BARE_COUNT = re.compile(
    r"(?:MCP|mcp__|服务器)[^\n]{0,60}?\b\d+\s*(?:个)?\s*工具"
    r"|\b\d+\s*(?:个)?\s*工具[^\n]{0,60}?(?:MCP|mcp__|服务器)"
    r"|\bworkflow[^\n]{0,40}?\b\d+\s*个\s*节点"
    r"|\bworkflow\s*节点\s*[:：]?\s*\**\s*\d+"
    r"|\b\d+\s*个\s*workflow\s*节点")
```

新增 `test_bare_count_guard_is_not_vacuous()`：内置 4 条**历史真实逃逸样本**（必须命中）+ 4 条合法写法（必须放行）。
**验证**：把旧的违规行重新注入任一 SKILL.md → 测试立刻变红（已实测）；同时不误伤 toolkit 自身脚本数（「核心 5 工具」「9 工具 + 闸6 回归」）。

---

## 3. 实测证据（本轮新增的平台事实）

| 命题 | 实测结果 | 影响 |
|---|---|---|
| `GET /alphas/{id}/submit` 的可用性 | **恒 404 + 空体**；对未提交的 `O0GjWqeY` 与**已 ACTIVE 的** `MPabNeNz` 相同 | 三份文档的三种说法**全错**；`submit_verdict.py` 的提交层视图（第 89 行走 GET）由此**看不到任何提交层信息**，其 403 分支是**死代码** → 处女候选恒返回 `UNVERIFIABLE` |
| 403 的真因 | `POST` → `403` + JSON，**唯一 FAIL 项 = `REGULAR_SUBMISSION value=4 limit=4`** | 4 颗候选（`O0GjWqeY` S2.44/F2.85、`2rpX85Ax` S2.71/F1.55、`np8VGNz3` S2.32/F1.60、`VkGJ73eA` S1.70/F1.15）**并非被相关性淘汰**；配额重置后即可重试 |
| `PENDING` 语义 | 未提交 alpha 的 `is.checks` 常态含 6 项 `PENDING` | **`PENDING` ≠ `FAIL`，不挡提交**；不得据此判死 |
| 配额口径 | 403 的 `REGULAR_SUBMISSION.value/limit` 是当日真值 | 与 `quota_status.py`（不分类型、会与 SUPER 混计）互为校验 |

> ⚠ **对上一轮结论的更正**：我曾判断 3 颗候选是"异步受理后未补发导致悬空"。补发缺失是真的（代码里确实没有 re-POST 分支），但**当下 403 的确定拦阻是配额用尽**，两者是不同环节的问题，不应混为一谈。

---

## 4. 待你拍板的三项（未擅动）

| # | 事项 | 说明 | 建议 |
|---|---|---|---|
| **A** | `submit_verdict.py` 的提交层视图 | 现走**恒 404 的 GET** → 提交层信息永远是空的，只能给 `UNVERIFIABLE`；"提交层唯一权威"名不副实 | 改为**确认后直接 POST**（POST 同时是提交与真闸：200=过 / 201=异步受理需补发 / 403=带全量 checks 与真因、零成本）。这是"能不能提"这件事上**最高杠杆的单项改动**，但会改动被多处引用的"唯一权威"工具 |
| **B** | 两个**游离 skill** | `brain-enhance-template`、`wqb-test-failure-triage` 只存在于 `~/.workbuddy/skills/`，**不在仓库**、不被 git 跟踪、不受同步保护（违反 INDEX 单源规则） | 若确认二者属于本项目 → `git mv` 进 `Claude/skills/` 并归层 + 更新 INDEX；若确为弃用 → 清理并在 INDEX 备案 |
| **C** | `hypothesis_round` 零使用 | dry-run 唯一 FAIL；`data/hypothesis_catalog/` 只有 1 个文件、**没有"字段扫描→≥20 可证伪假设"的生成器**，ra-pipeline 步 2 的饱和路由因此是死路 | 要么补 catalog 生成入口，要么把饱和路由改指向现有可用路径 |

---

## 5. 未修复的次要项（备查，不阻塞）

**失效引用 / 过时事实**
- `brain-alpha-research`：`wqb research` / `wqb settings` **无 CLI 入口**；`grammar._OP_ARITY`、`config.SHAPE_CLASSES` 含 `S0` 均为错误符号；区域建议「HKG ≈ KOR > EUR」与 `config.py::REGION_PRIORITY`（HKG=1，优先级最低）直接冲突 —— 注：区域**过闸率**排名因关联键覆盖率仅 40% 已撤回（见 `skill_workflow_dryrun_audit_20260926.md` §3），此处只以 config 常量为准，不再引用过闸率数字
- `brain-alpha-research-news-sentiment`：`wqb news-refresh-portfolio` 不存在；Tier A 门槛缺 `coverage`
- `brain-alpha-research-field-quality`：`WebData_*.zip` 实为**目录**（带 `--zip` 必失败）
- `brain-dataset-exploration-general`：S0 教用 `get_datasets`，与 ra-pipeline 实际入口 `recommend_datasets` 脱节；ASI universe 缺 `MINVOL1M`
- `alpha-expression-verifier`：自称 validator「1363 行」实为 1403 行
- `brain-next-move-analysis`：区域清单仅 10 区（代码 14 区）
- `wq-brain-campaign-matrix`：「既有 **31 个**其他 skill」应为其 32

**结构性 / 治理**
- `brain-make-some-gem` **内嵌的 `brain-feature-implementation` 是 49 行旧版（2026-08-22），真正被喂进 LLM prompt 的是它**，顶层 111 行新版永不生效
- `brain-make-some-gem` 的 `config.json` 含**明文 BRAIN 邮箱/密码 + LLM key**（已被 `.gitignore` 覆盖、**无 git 泄露**），建议迁 `.env` 并轮换
- `brain-data-feature-engineering` 的 `source` 词表与 GEM 的 `TEMPLATE_IDEAS_SOURCES` **三方互斥**（`standalone` 一边强制写、一边列为跳过注入）
- `brain-sim-alphas-in-batch-and-track` / `wq-backtest-monitor`：`allowed-tools` **未声明 MCP**，正文却调 `mcp__*`；后者 §5 与 §10 近乎逐字重复、且绑死历史任务名
- `brain-forum-browse`：「每轮必贡献」与"平台无写工具"**结构性不可满足**
- `pull-brain-skills`：`--dest` 默认直写权威目录，**只校验 SKILL.md 是否存在**，不校验 layer/命名 → 可破坏 INDEX 归层
- `planning-with-files`：hooks 全局注入（`PreToolUse`/`Stop`）会在所有 WQ 任务触发副作用
- `INDEX.md` 的 `last_verified: 2026-09-15` 已落后于本轮事实

**卫生（本轮新发现）**
- **仓库 skill 树里混入了 16 个运行时产物**：`brain-make-some-gem/scripts/trailSomeAlphas/skills/brain-data-feature-engineering/output_report/*.md`（各区的 `<R>_delay<D>_<ds>_ideas.md`）只存在于仓库、不随同步分发。它们是 GEM 跑批的输出，混在 skill 目录里会被 git 跟踪 → 建议移出或加 `.gitignore`
- **换行符不统一**：仓库为 LF、多数安装位为 CRLF（sync 在 Windows 写 CRLF）。`sync_skills.py --check` **按归一内容判定**（已逐文件核实：5 处字节差异全部是 EOL，归一后完全相同），故其"一致"结论**正确**。仅提示：做字节级比对时会看到大量"假漂移"，请以 `--check` 为准

**职责边界待收敛**
- `brain-alpha-research` / `dataset-exploration-general` / `field-quality` 三者的选区职责无排他判据（建议按 S-PRE 数据包预筛 / S0 选集 / S1 选字段硬切）
- `feature-engineering` / `feature-implementation` / `inspect-raw-template`（原 `enhance-template` 已缺失）四者边界模糊

---

## 6. 复核命令

```bash
python tools/audit_node_registration.py                       # 节点四处同步
python tools/sync_skills.py --check                           # 5 安装位零漂移
python -m pytest tests/unit/test_skill_integrity.py tests/unit/test_docs_consistency.py \
                 tests/unit/test_workflow.py tests/unit/test_audit_fixes.py -q   # 419 passed
```
