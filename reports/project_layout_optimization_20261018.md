# 项目布局优化建议 — wqb（WorldQuant BRAIN Alpha 挖掘工作区）

> **范围**：仅从文件/目录组织角度分析（不触及代码逻辑、算法、业务功能、数据流程或运行时行为）。
> **数据口径**：git 跟踪面 **4194** 件 ＋ 磁盘面 **38693** 件（含 gitignore 的运行期产物）。
> **审计日**：2026-10-18。
> **配套闸门**：`tools/audit_structure.py`（S1–S21）、`tools/code-audit/*`（三道棘轮）、`tools/THEMES.json`（tools 归属登记表）。

---

## 1. 当前项目结构概览

### 1.1 分层模型（实际形态）

仓库自然形成 **8 层**，职责边界基本清晰：

| 层 | 目录 | 跟踪/磁盘 | 职责 |
|---|---|---|---|
| **代码层** | `src/` | 120 / 281 | 可安装包 `wqb`（src-layout）：`expression/ memory/ profiles/ research/ search/ store/ workflow/ modeb/` 等 37 个条目，含核心模块 `config.py db_conn.py paths.py region_*.py towers.py` |
| **工具层** | `tools/` | 219 / 359 | 可复用 CLI，**顶层 155 个 .py** ＋ 16 个主题子目录 |
| **测试层** | `tests/` | 213 / 459 | `fixtures/` ＋ `unit/`（按域编号子目录） |
| **知识层** | `Claude/skills/` | 445 / 597 | 47 个 skill，含 `SKILL.md` ＋ `references/` ＋ `scripts/` ＋ `config(s)/` |
| **数据资产层** | `tracking/` | 2637 / 14009 | 14 个区域战役目录 ＋ 5 个共享目录 |
| **文档层** | `docs/ reports/ output_report/` | 95 / 132 / 218 | 规范 SOP / 人工审计 / 工具直写产物（三分已确立） |
| **隔离层** | `attic/` | 41 / 808 | 归档（95% 未入库） |
| **运行期层** | `cache/ data/ extensions/ logs/ research-data/ results/` | **0 / 3751** | 100% gitignore，正确隔离 |
| **MCP 服务** | `world-quant-brain-mcp/` | 61 / 17897 | HTTP 服务（`main.py` ＋ `brain_mixin_*`）；`17897` 中绝大多数是 gitignored 的 `.venv` |

### 1.2 关键体量读数

- **根层**：14 个文件（`.gitattributes .gitignore .mailmap .mcp.json AGENTS.md CLAUDE.md README.md conftest.py mcp_config.json pyproject.toml pytest.ini requirements.txt wqb_db_mcp.py`）＋ 14 个目录。
- **未入库**：158 件，其中 **50 件在 `tracking/KOR/`**（真缺失源文件），其余 108 件为 `cache/ logs/` 等运行期或 `attic/` 归档。
- **运行期规模**：`cache/` 1315 件、`logs/` 1765 件、`research-data/` 319 件、`results/` 235 件、`extensions/` 103 件、`data/` 10 件 —— 全部 100% gitignore，**隔离正确**。
- **`tracking/` 内部**：14009 件中 **11322 件 gitignored 运行期**（`cache` 9130 / `candidates` 1433 / `results` 536 / `robustness` 65 / `scripts` 56 / `perfmax` 24），**仅 50 件真未入库**。

### 1.3 已建立的正面布局契约（值得保持）

1. **`src-layout` ＋ 包内分层**：`src/wqb/` 37 个条目，子包职责分明，无顶层散件。
2. **三分文档层**：`docs/`（规范 SOP）/ `reports/`（人工审计）/ `output_report/`（工具直写产物）边界已用 AGENTS.md §8.13 ＋ S16 固化。
3. **`tools/THEMES.json` 主题登记**：19 个主题已声明归属，是 tools 去顶层化的路线图。
4. **运行期目录全量 gitignore**：6 个目录零泄漏，`data/` 与 `research-data/` 的只读契约明确。
5. **`attic/` 归档语义**：归档而非删除，§7 明确。

---

## 2. 主要布局问题（按严重度）

### 🔴 P0 — tools/ 上帝目录：155 个顶层 .py ＋ 19 主题半迁移

- **现状**：`tools/` 顶层仍有 **155 个 .py**，`THEMES.json` 声明了 **19 个主题**（`gates backtest probe super verdict pool-hygiene datasets rotation data-repair research code-audit ledger db reporting fields wave forum catalog skills`）作为目标归属，但其中 **9 个主题目录尚不存在**（`super pool-hygiene datasets ledger reporting wave forum catalog skills`），说明迁移停在半途。
- **已落地**：`backtest code-audit data-repair db fields gates git-hooks legacy lib probe research rotation verdict wave_gate_pkg` 共 16 个子目录（含 `__pycache__`）。
- **风险**：顶层平铺使 S11 只能靠「冻结基线 154」被动防守，无法主动收敛；跨主题调用靠 `sys.path` 硬编码（`audit_structure.py` 实测 **174 处** `sys.path.insert` 存量）。
- **判定**：这是当前**最大单点布局债**，但已有完整迁移路线图，属「可度量收敛」而非「无解」。

### 🔴 P1 — `tracking/<REGION>/` 子目录结构不一致（5–16 个/区）

实测各区子目录（去重核心集 = `cache candidates config priors reference results` 六项）：

| 区 | 子目录数 | 偏离核心的目录 |
|---|---|---|
| AMR | 7 | `ideas` |
| ASI | 7 | `scripts` |
| CHN | 6 | —（缺 `scripts`） |
| DEU | 9 | `deepexplore reports scripts` |
| EUR | 10 | `ppa ra reports scripts` |
| GBR | 8 | `reviews scripts` |
| GLB | 8 | `reports scripts` |
| HKG | 7 | `scripts` |
| IND | 9 | `reports reviews scripts` |
| JPN | 6 | —（缺 `scripts reports reviews`） |
| KOR | 8 | `scripts` |
| MEA | 8 | `reviews scripts` |
| **USA** | **16** | `campaign_20261014 campaign_20261017 deepexplore perfmax robustness runs waves reports reviews` |

- **共性问题**：`reports/ reviews/ scripts/` 三种目录在 14 区中分布完全随机（USA 有、CHN 无）；无统一的「战役产物」归口。
- **USA 特有**：`campaign_20261014/ campaign_20261017/` 目录与 `waves/ runs/ robustness/ perfmax/ deepexplore/` 并存，共 **10 个额外目录**，是全仓结构最乱的一区。
- **空目录**：`tracking/FORUM/ tracking/_scratch/ tracking/hypotheses/ tracking/mining/ tracking/prod_probe/` 五处无文件（属设计预留或残留）。

### 🟡 P1-3 — KOR 50 件未入库源文件

`git ls-files --others --exclude-standard tracking/` 实测 **50 件真未入库**（非 gitignore 的运行期）：

- `tracking/KOR/reference/datasets/*.md`（15 份数据集画像：analyst9/10/11/14/15/16/25/39/44/45/46/48/81 + analyst_base_ref 等）
- `tracking/KOR/reference/_wave11-13_analyst_findings.md`

这是**真缺失**（非运行期缓存），`git clean -fd` 会永久带走，且 checkout/reflog 救不回。属并行会话在途件，未擅自处理。

### 🟡 P2 — skills/ 检索权威歧义：`reference.md` 与 `references/` 并存

47 个 skill 中 **3 个并存两种形态**：`brain-how-to-pass-alpha-test / planning-with-files / wq-brain-alpha-optimization-v1`。

- 历史：`reference.md`（单文件）→ `references/overview.md`（目录化）迁移未完成。本次提交 `9e269fb` 已入库新 `references/overview.md`，但旧 `reference.md` 的删除未暂存，故两者并存。
- **影响**：检索工具与 S17/S16 的「子文件差异不算孤儿」判定会给出歧义信号；`sync_skills.py --prune-orphans` 只清顶层孤儿、不清子文件差异。
- **判定**：应完成删除旧件，使三区唯一指向 `references/overview.md`。

### 🟡 P2 — 脚本跨 skill 重复（vendoring）

按 basename 统计的重复脚本：

| 脚本 | 副本数 | 说明 |
|---|---|---|
| `validator.py` | ×5 | skill 验证器 |
| `helpful_functions.py` | ×4 | 通用函数 |
| `ace_lib.py` | ×4 | ACE 相关 |
| `diversity_enhancer.py` | ×3 | 多样性增强 |
| `dataset_experience.py` | ×3 | 数据集经验 |
| `gate.py` | ×3 | 闸门 |
| `scan_fields.py` | ×3 | 字段扫描 |

S6 已登记 `ace_lib / diversity_enhancer / helpful_functions / validator` 四组为「已知跨 skill 复制，待治理」——**存量债已识别但未收敛**。27 个 skill 含 `scripts/` 目录，是重复的主要来源。

### 🟢 P3 — 顶层散件与入口位置

- **`__pycache__` 散落**：`src/wqb/__pycache__/ tools/__pycache__/ tests/__pycache__/` 等（未 gitignore，会污染 `git status`）。
- **根层 MCP 入口分裂**：`world-quant-brain-mcp/main.py`（HTTP 主服务）与根层 `wqb_db_mcp.py`（DB 服务）分置两处，入口不集中。
- **`configs/` vs `config/`**：3 个 skill 用 `configs/`（凭据契约持有者：`brain-alpha-judge / brain-forum-browse / brain-sim-alphas-in-batch-and-track`），**属有意保留**（`test_judge_never_submits.py:218`、`test_sf_docs.py:134`、`load_credentials.py:46` 三处锁定），**不建议改**——但需文档化此例外。
- **`attic/` 入库率低**：808 件中仅 41 件入库（95% 未入库），归档语义与 gitignore 边界略模糊。
- **`tracking/` 空目录**：`FORUM/_scratch/hypotheses/mining/prod_probe` 五处空目录，需确认是设计预留还是残留。

### 🟢 P3 — 命名分裂（已裁定不治理）

`reports/` 下 9 个一层子目录：5 个 kebab（规范）＋ 2 个 snake ＋ 2 个 `_refs`，后 4 条已登记 `S16_DIR_LEGACY` 豁免。**AGENTS.md 已裁定不 snake 化**（会造 20+ 死指针）。

---

## 3. 推荐的目录组织方案

### 3.1 分层契约（建议写入 AGENTS.md，并落机械闸）

| 层 | 边界契约 | 允许的守卫 |
|---|---|---|
| `src/` | 可安装包，子包按能力域划分；**禁**顶层散件 | S1/S2/S3 |
| `tools/` | **只允许**主题子目录 ＋ 登记表豁免的常驻件 | S11（基线棘轮）＋ THEMES 归属 ＋ S14（README 登记） |
| `tests/` | `unit/`（按域编号）＋ `fixtures/` | 现有 pytest 路由 |
| `Claude/skills/` | 每 skill = `SKILL.md` ＋ `references/`（**禁** `reference.md` 并存）＋ `scripts/` ＋ `config/`（凭据契约者用 `configs/`） | S6 ＋ `test_skill_layout_contract.py` |
| `tracking/<R>/` | **固定 6 核心**：`candidates/ config/ reference/ results/ reviews/ scripts/` ＋ 允许 `cache/ priors/`；**战役产物**统一落 `output_report/`，不落区目录 | S13 ＋ S18 ＋ `test_region_skill_layout.py` |
| `docs/ reports/ output_report/` | 三分边界（规范/人工/工具产物） | S5 ＋ S16 |
| `attic/` | 归档，只读；入库与否按「是否需追溯」判 | §7 |
| 运行期 6 目录 | 100% gitignore，零泄漏 | `.gitignore` ＋ S18 |

### 3.2 公共模块 vs 业务模块边界

**当前实际边界**（建议固化为契约）：

```
公共（可跨域复用）          业务（域专属）
├── src/wqb/               ├── tracking/<R>/        区域战役数据
│   ├── expression/        ├── Claude/skills/wq-brain-ra-<R>/  区域 skill
│   ├── profiles/          └── tools/<theme>/       主题化工具
│   ├── config.py
│   ├── paths.py
├── tools/code-audit/      （代码审计，跨域公共）
└── tests/fixtures/        （测试夹具，跨域公共）
```

**当前模糊地带**：
1. `tools/` 顶层 155 个 .py —— 部分实为跨域公共（`audit_structure.py`、`retention.py`、`sync_skills.py`、`db_conn` 相关），部分为域专属（`gate_attribution.py` 属 gates 主题），但因都在顶层而边界不可见。
2. `tracking/reference/tooling/` —— 区域参考层里混了 `generate_manifest.py`（全局工具），归属不清。

### 3.3 入口文件集中建议

当前入口分散在 3 处（`world-quant-brain-mcp/main.py`、`wqb_db_mcp.py`、`.mcp.json`/`mcp_config.json`）。建议在 `docs/` 补一份「入口索引」，或在 `README.md` 增「入口速查表」，明确：HTTP 服务入口、DB 服务入口、pytest 入口、MCP 注册入口。

---

## 4. 可迁移或重构的文件类别

| 类别 | 现状 | 目标位置 | 工具/守卫 |
|---|---|---|---|
| **tools 顶层 .py（155 个）** | 顶层平铺 | 按 THEMES.json 归入 19 个主题子目录 | `audit_structure.py --freeze-tools-top`（基线棘轮）＋ THEMES 归属 + README 登记三步链 |
| **tracking/KOR 未入库件（50）** | 未跟踪 | `git add` 入库 `tracking/KOR/reference/datasets/` | `repo_governance_check.py`（未跟踪源告警） |
| **skills/ 旧 `reference.md`（3 个）** | 与 `references/overview.md` 并存 | 删除旧件，统一 `references/overview.md` | `test_skill_layout_contract.py`（已存在守护） |
| **重复脚本（7 类 25 份）** | skill 内 vendoring | 抽取至 `src/wqb/` 或 `tools/lib/` 公共层 | S6 登记（存量）＋ 新建公共库 |
| **tracking/ 运行期混入 source 区** | `candidates/ results/` 在 `<R>/` 下 | 保持 gitignore，但语义上应明确「`<R>/` 下 `cache candidates results` 为运行期」 | `.gitignore` ＋ 文档化 |
| **attic/ 未入库件（767）** | 95% 未入库 | 按需 `git add`（仅需追溯者）或 gitignore 整目录 | §7 归档策略明确化 |
| **`__pycache__/`** | 散落多处 | `.gitignore` 加 `__pycache__/` | 一行配置 |
| **tracking/ 空目录（5）** | `FORUM/_scratch/hypotheses/mining/prod_probe` | 确认保留（加 `.gitkeep`）或删除 | 人工裁定 |

---

## 5. 优化优先级

### 🔴 P0 — 立即（本周）

1. **`tools/` 顶层收敛**：按 `THEMES.json` 完成 9 个未建主题目录的创建 ＋ 文件归入，同时用 `--freeze-tools-top` 维持基线棘轮。这是最大单点债，但路线图已完整。
2. **`__pycache__/` 加 gitignore**：一行配置，消除 `git status` 噪音。

### 🟡 P1 — 短期（1–2 周）

3. **`tracking/<R>/` 结构标准化**：以「6 核心 ＋ `cache priors`」为契约，逐区对齐；USA 的 10 个额外目录优先治理（战役产物迁 `output_report/`）。落 `test_region_skill_layout.py` 扩展守护。
4. **KOR 50 件入库**：`git add tracking/KOR/reference/datasets/` ＋ findings，避免 `git clean` 丢失。
5. **skills/ `reference.md` 清理**：删除 3 个旧件，完成 `reference.md → references/overview.md` 迁移。

### 🟢 P2 — 中期（1 个月）

6. **重复脚本抽取**：7 类 25 份 vendoring 收敛至公共层（`tools/lib/` 或 `src/wqb/`），优先 `validator.py×5` 与 `helpful_functions.py×4`。
7. **`configs/` vs `config/` 例外文档化**：在 AGENTS.md 补「凭据契约持有者用 `configs/`」的例外说明（不改结构）。
8. **入口索引文档化**：`README.md` 增入口速查表。

### ⚪ P3 — 观察（不必主动治理）

9. `attic/` 入库率、`tracking/` 空目录、`reports/` snake 命名 —— 均已裁定或低成本，保持现状。

---

## 6. 文件与目录命名规范建议

### 6.1 目录命名

| 层 | 规范 | 示例 | 现状 |
|---|---|---|---|
| 顶层目录 | 全小写；工具层用 kebab-case | `code-audit` `data-repair` | ✅ 已统一 |
| 区域目录 | 全大写 ISO 3 字母 | `EUR USA KOR` | ✅ 已统一 |
| skill 目录 | 全小写 kebab-case | `wq-brain-ra-usa` | ✅ 已统一 |
| 区域子目录 | 全小写；运行期用单数 | `candidates results cache` | ✅ 已统一 |
| `tests/unit/` 子目录 | 两位编号 + 短名 | `07_docs_skills` | ✅ 已统一 |

### 6.2 文件命名

| 类型 | 规范 | 示例 | 建议 |
|---|---|---|---|
| Python 模块 | snake_case | `db_conn.py` | ✅ 已统一 |
| 工具脚本 | snake_case + 动词前缀可选 | `audit_structure.py` | ✅ 已统一 |
| 报告 | `<主题>_<YYYYMMDD>.md` | `structure_audit_20261018.md` | ✅ S16 已守护 |
| 区域 skill 补充文档 | `_` 前缀（非类别文件） | `_field-profile.md` | ✅ `render.py` 已判 |
| JSON 配置 | snake_case | `cells.json` `thresholds.json` | ✅ 已统一 |
| 战役产物 | `<REGION>_<主题>_<YYYYMMDD>.md` | `USA_campaign_20261017.md` | ⚠ 需统一（现 `campaign_20261014/` 目录形式散落） |

### 6.3 明确禁止（建议落闸）

1. **禁** `reference.md` 与 `references/` 并存（已在 `test_skill_layout_contract.py` 守护）。
2. **禁** skill 内用 `configs/`（除 3 个凭据契约持有者，需白名单）。
3. **禁** `tracking/<R>/` 下散落 `campaign_YYYYMMDD/` 目录（应落 `output_report/`）。
4. **禁** `__pycache__/` 入库（加 gitignore）。
5. **禁** `tools/` 顶层新增 .py（走 THEMES 归属 + README 登记 + freeze 基线三步链）。

---

## 7. 总体判断

**结构健康度：中上。** 核心分层（src 代码层 / tools 工具层 / tracking 数据层 / skills 知识层 / docs-reports-output_report 文档三分 / attic 隔离 / 运行期 gitignore）已建立且多数有机械守卫，运行期 6 目录 100% 隔离、文档三分已固化，属**成熟期的工程纪律**。

**主要债在「工具层与数据资产层的边界收敛」**：`tools/` 顶层 155 个 .py 是最大单点，但已有完整迁移路线图；`tracking/<R>/` 子目录随机分布是第二点，需标准化为固定契约。两者均属「可度量收敛」，非架构性硬伤。

**最应警惕的不是已识别的债，而是未被识别的**：KOR 50 件未入库源文件提示「并行会话的在途件」是真实的数据丢失风险面（`git clean` 不可逆）。建议把 `repo_governance_check.py` 的未跟踪源告警从「警告位」提升为「提交前必查」的人工步骤。
