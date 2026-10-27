# wqb 项目布局与 Skills 规范性审计（2026-10-24）

> 审计口径：以 `git ls-files`（4661 件入库）+ 工作树实测为准；结构类结论以项目自带闸门
> `tools/audit_structure.py`（FAIL=14 / WARN=4）与 `tools/sync_skills.py --check`（33 项漂移）为权威，
> 不凭主观印象。所有「问题」均给出可复现命令或文件路径。
>
> 一句话结论：**规范写得非常成熟（CONTRACT/INDEX/AGENTS/THEMES 四层齐备，棘轮与守护测试齐全），
> 但「规范」与「工作树」已经脱节**——27 项违规（14 结构 + 13 测试）中至少 20 项来自 2026-10-21 起
> 新增的 USA/EUR 字段画像文档与一次性脚本，**它们没跑门禁就入库了**。核心病因不是设计缺失，
> 而是**门禁未随克隆自动生效 + 无 CI 兜底**（`core.hooksPath` 是本机 git config，不入库）。

---

## 1. 当前项目结构概览

### 1.1 顶层全景

| 目录 | 磁盘文件 | 入库 | 体积 | 职责（AGENTS.md §1） | 判定 |
|---|---:|---:|---:|---|---|
| `tracking/` | 14261 | 2677 | 107M | 13 个区域战役追踪（config/candidates/priors/reference/results…）+ `mining/` 共享数据湖 | ⚠ 重：运行态混入索引面 |
| `cache/` `logs/` `results/` | 4299 / 2248 / 341 | 0 | 46M/18M/9.1M | 运行期产物 | ✅ 已 gitignore，规范 |
| `world-quant-brain-mcp/` | 158 | 63 | 768M | MCP 服务 `wq-brain-http`（69 工具）+ 自带 .venv/deploy/tests | ⚠ 子项目嵌在主仓 |
| `data/` | 108 | 0 | 484M | `wqb.db` 规范库 | ✅ gitignore |
| `docs/` | 303 | 299 | 12M | 长期规范 / SOP / 速查 | ⚠ `reference/EUR` 209 件爆炸 |
| `attic/` | 814 | 43 | 12M | 只读归档（20+ 日期化包） | ⚠ 771 件未入库 |
| `tests/` | 497 | 240 | 11M | pytest（10 个编号子目录） | ✅ 全项目最规整 |
| `Claude/skills/` | 696 | 604 | 11M | **47 个 skill + 4 份元文档** | ⚠ 存在 4 组跨 skill 复制件 |
| `tools/` | 423 | 253 | 7.1M | CLI 工具链（**170 个平铺在顶层**） | ❌ 主题化迁移停滞 |
| `src/` | 286 | 123 | 4.5M | 规范核心包 `wqb`（122 py / 36.8k LOC） | ⚠ 包根 29 个平铺模块 |
| `output_report/` | 231 | 227 | 4.0M | 报告唯一出口 | ⚠ 63 件无日期、命名混 |
| `reports/` | 125 | 118 | 3.4M | 人工审计 / 复盘 | ✅ 65 件根文件全带日期 |
| `research-data/` `extensions/` | 297 / 103 | 0 | 39M / 2.2M | 外部数据包 / 浏览器扩展源 | ✅ 只读 gitignore |
| `selfcorr_quick_out/` | 5 | 0 | 9.0M | （无归属） | ❌ S17 未登记顶层目录 |

根目录散件 13 个，其中 **两个单体巨物**：

| 文件 | 规模 | 问题 |
|---|---|---|
| `wqb_db_mcp.py` | **3026 行 / 134KB / 49 个 MCP 工具** | 第二个 MCP 服务，与 `world-quant-brain-mcp/` 的 `tools_*.py` 拆分约定**完全不对称** |
| `agents.md` | 122KB | 硬约束主干（§1–§8），S7 白名单未登记 |

### 1.2 六类文件分布

| 类别 | 落点 | 数量 | 健康度 |
|---|---|---:|---|
| **代码** | `src/wqb/`（122 py / 36.8k LOC）、`tools/`（250 py）、`Claude/skills/*/scripts/`、MCP 服务端 | ~999 .py 入库 | 🟡 分区清晰，但 tools 未下沉、src 包根平铺 |
| **配置** | `.mcp.json`（权威）+ `mcp_config.json`（镜像）、`pyproject.toml`、`pytest.ini`、`tracking/<R>/config/{settings,thresholds}.json`×13、`Claude/skills/*/config/*.json`、`world-quant-brain-mcp/{config,deploy}` | 13×13 settings/thresholds + 7 root | 🟡 存在「权威 + 镜像」双份（已注释说明，可接受） |
| **资源** | `data/wqb.db`(484M)、`research-data/operators_platform_*.json`、`docs/reference/operators_catalog.json`、`tracking/mining/` 数据湖 | 2283 .json 入库（占 49%） | 🔴 JSON 占一半入库量，多为区域快照 |
| **测试** | `tests/`（231 py，`unit/01_store_db` … `unit/10_toolkit_scripts` 编号分层）+ `world-quant-brain-mcp/tests/` + `conftest.py` + 9 个 baseline fixture | 240 入库 | 🟢 **最佳区域** |
| **文档** | 根三份（README 20KB / CLAUDE 2KB / agents 122KB，定位不重叠）+ `docs/` 299 + skills references 604 + `reports/` 118 + `output_report/` 227 + `.workbuddy/memory/` | 1220 .md 入库 | 🟡 桶多且有重叠（见 §2.4） |
| **构建/部署** | `world-quant-brain-mcp/{Dockerfile,Makefile,docker-compose.yml,deploy/{nginx,systemd}}`、`tools/git-hooks/{pre-commit,commit-msg}` | — | 🔴 **无根级 CI**；钩靠本机 `core.hooksPath` |

### 1.3 依赖方向（好的一面）

- ✅ `src/` **不引用** `tools/`（S2 PASS）——公共包与业务脚本边界是干净的。
- ✅ `src/` 无 `sys.path` 自举注入（S1 PASS）。
- ⚠ 但反向耦合极重：**397 处 `sys.path.insert`，分布在 248 个文件**（tools 206 / skills 39 / src 3），
  即 **82% 的 tools 脚本靠路径注入找包**——这正是 THEMES 迁移无法推进的技术根因。

---

## 2. 主要布局问题

### P0 — 门禁不随仓库生效，规范与工作树系统性脱节

```
git config core.hooksPath  →  tools/git-hooks     # 本机 git config，不入库
.github / .gitlab-ci / Jenkins                     # 全部不存在
```

后果：新克隆 / 换机器 → **门禁全失效**。本次审计发现的 27 项违规（14 结构 + 13 测试）
正是长期累积的结果。这是唯一需要最先修的根因，其余都是它的下游症状。

### P0 — `tools/` 主题化迁移停滞（170 个脚本仍平铺）

`tools/THEMES.json` **设计已完成**：19 个主题、168 个文件全部归属、`unassigned_n=0`；
棘轮 S11 也在（顶层只减不增）。但实际只有 80/250 进了子目录。

`_why_not_moved` 记录的两个阻塞项（80 处 `sys.path.insert`、5 种仓库根推导写法）
**技术上已被解决**——`src/wqb/paths.py`（2026-10-04）提供与层数无关的根探测，
`pyproject.toml` 让 `import wqb` 全局可用。阻塞已从「不可能」降级为「工程量大」，但迁移没跟上。

最新违规（audit_structure S11 三条）：
- 16 个新脚本又堆到顶层（含本次会话新增的 `continue_submit_leM88RN5.py`、`find_leM88RN5_collision.py`）
- 8 个顶层脚本在 THEMES.json 无归属：`campaign_watchdog.py`、`export_fields_for_tagging.py`、
  `gen_llm_field_tags.py`、`poll_single_sims.py`、`targeted_dev.py`、`vwap_field_dist.py`、
  `vwap_histogram.py`、`vwap_pnl_fetch.py`
- `tools/full_template_campaign.py.bak_20261021_2242`（备份件混入 CLI 层）

### P1 — 两个 MCP 服务约定不对称

| | `wq-brain-http` | `wqb-db` |
|---|---|---|
| 位置 | `world-quant-brain-mcp/`（目录） | **仓库根单文件** |
| 组织 | `tools_account/alpha/data/sim/workflow…` 12 个模块（69 工具） | 3026 行一体，靠 `# ---- 分节注释 ----` 分区（49 工具） |
| 入口 | `main.py` | 自身 |

`wqb_db_mcp.py` 内的分节注释已经天然划好了切分边界：
`wave_results 查询` / `registry 查询` / `ledger 查询` / `alpha 查询` / `综合查询` /
`区域轮转` / `写工具(upsert)` / `字段画像查询` / `相关` / `收割`。
→ 直接照搬兄弟服务的 `tools_*.py` 命名即可，零设计成本。

**副作用已显现**：`INDEX.md` 写「wqb-db 47 个工具」，实数为 **49**，
`test_mcp_tool_counts_match_index` 因此 FAIL——一体文件改工具数时没人同步文档。

### P1 — `src/wqb` 包根 29 个平铺模块，其中 4 个是 25–42KB 巨物

```
gate_attribution.py 42KB   config.py 34KB   region_rotation.py 32KB   waiver.py 26KB
wave_results_contract.py 14KB   step_eval.py 22KB   region_catalog.py 10KB …
```

只有 8 个子包（`workflow` 32 / `store` 19 / `expression` 11 / `profiles` 10 / `research` 8 /
`modeb` 5 / `memory` 5 / `search` 3），包根反而塞了 29 个模块。
依赖图上 `config`(27) / `db_conn`(22) 被全包引用——说明 core 层已事实存在但**没有目录表达**。

### P1 — 区域参考文档有两个家，且各区归属不一致

| 区域 | `docs/reference/<R>/` | `tracking/<R>/reference/` | 结论 |
|---|---:|---:|---|
| EUR | 23（含 `datasets/` 187 件） | 57 | 两边都有 |
| IND | 1 | 37 | 主要在 tracking |
| KOR | 0 | 124 | 全在 tracking |
| GBR | 1 | 27 | 全在 tracking |
| **DEU** | **2** | **0** | **反着来，全在 docs** |

同一类产物（区域参考/字段画像）在 5 个区域用了 3 种落点，后来者只能靠猜。

### P1 — `tracking/USA` 骨架膨胀，运行态目录漏管

标准骨架（`cache candidates config priors reference results`），但 USA 长出 16 个子目录：

```
USA: cache campaign_20261014 campaign_20261017 candidates config deepexplore perfmax
     priors reference reports results reviews robustness runs waves
```

其中 **`tracking/USA/runs/` 242 个 txt/json 既未 gitignore 也未入库**——随时会被 `git add -A` 吸进索引
（本次提交就是 `git add -A`）。S18 只扫索引面（2677 件，确实干净），**扫不到未入库的运行态**。
`tracking/EUR` 另有 `ppa/ ra/`，`tracking/DEU` 有 `deepexplore/` —— 同样是骨架外的自发目录。

### P2 — 文档桶重叠与命名双轨

- `docs/reference/EUR/FIELD_PROPERTY_RULES.md`、`FULL_COVERAGE_RULE_v2.md`、
  `SIGNAL_MINING_WORKFLOW.md`、`TEMPLATE_CALIBRATION_20261020.md`、`datasets/QUERY_API.md`
  → **5 处大写命名**，违反 §8.13（S16 FAIL）。
- 同题双份、命名双轨（真实案例）：
  `docs/reference/field-profile-ind-inst-fund-20261019.md`（31KB，连字符）
  与 `docs/reference/field_profile_ind_inst_fund_20261019.md`（15KB，下划线）**前 20 行完全相同**——
  后者被复制扩展后原文件没删。
- `output_report/` 232 件中 **63 件无日期**（S16 基线里还有 29 件存量违规）；
  而 `reports/` 65 件根文件**全部带日期**——两个报告桶纪律不一致。
- 内容完全相同的重复文件 **27 组**（md5 比对），典型：
  `validator.py` ×4、`helpful_functions.py` ×4、`ace_lib.py` ×3、`diversity_enhancer.py` ×2、
  `tracking/mining/*_fields.json` ×4、`tracking/KOR/reference/*.md` ↔ `field_profile/*.md` ×4、
  `tracking/IND/reference/ind_generation_constraints.json` ↔ `tracking/MEA/reference/mea_…json`（整份照抄）。

### P2 — 根目录散件与空目录

- 8 个空目录：`tools/super/`、`output_report/brain-alpha-judge/`、
  `attic/json_archive/{registry, wave_results/{EUR,KOR,MEA}}`、`cache/_scratch/{pt,pt2}`。
- `agents.md`（122KB）不在 S7 根白名单；`__pycache__/` 出现在仓库根（说明根级模块被 import）。
- `selfcorr_quick_out/`（9MB）属运行产物却既不在白名单也未 gitignore。

---

## 3. 推荐目录组织方案

保持现有主干不动（迁移成本可控），只做三处结构性收敛：

```
wqb/
├─ src/wqb/                     # 规范核心（唯一 pip 可装包）
│   ├─ core/                    # 【新】config.py + paths.py + timeutil.py + db_conn.py
│   │                           #        + db_write_lock.py（被全包引用的那一层）
│   ├─ domain/                  # 【新】region_* · shape_quota · towers · quota · alpha_properties
│   ├─ gates/                   # 【新】waiver.py + gate_attribution.py + submit_verdict_core.py
│   │                           #        + step_eval/scoring/events + wave_results_contract
│   ├─ workflow/  store/  expression/  profiles/  research/  modeb/  memory/  search/
│   └─ __init__.py              # 保持再导出，旧 import 路径不断
│
├─ mcp_servers/                 # 【新】两个服务同构放置
│   ├─ wq_brain_http/  → (git mv world-quant-brain-mcp/{*.py,deploy,config,Dockerfile,Makefile})
│   └─ wqb_db/         → (拆分 wqb_db_mcp.py)
│        ├─ server.py           # 注册 + 生命周期
│        ├─ tools_wave.py  tools_registry.py  tools_ledger.py  tools_alpha.py
│        ├─ tools_profile.py  tools_harvest.py  tools_rotation.py
│        └─ README.md
│
├─ tools/                       # CLI 层：顶层只留 README/THEMES.json/_pyenv.py
│   └─ <kebab-case 主题>/       # 按 THEMES.json 19 个主题落位（gates/verdict/backtest/…）
│
├─ docs/                        # 只留「长期规范 / SOP」，一次性结论一律迁 reports/
│   └─ reference/               # 区域级参考统一让位给 tracking/<R>/reference/
│
├─ tracking/<REGION>/           # 五件套骨架 + 允许的白名单扩展
│   ├─ cache/ candidates/ config/ priors/ reference/ results/   # 标准（gitignore cache/results）
│   └─ scripts/  reports/  reviews/                             # 已登记的扩展（S13）
│
├─ reports/<主题>_<YYYYMMDD>.md # 人工审计 / 复盘（带日期，纪律最好，照它抄）
├─ output_report/               # 工具直写产物（同 reports 纪律：强制日期后缀）
├─ attic/<主题>_<YYYYMMDD>/     # 只读归档
└─ .github/workflows/gates.yml  # 【新】CI 兜底（见 §5 P0）
```

**关键判据（写进 AGENTS.md §8.13 的那句话）**：

> 一份文档到底进 `docs/` 还是 `reports/`——**看它会不会过期**。
> 不会过期（SOP / 规范 / 速查）→ `docs/`（snake_case，无日期）；
> 会过期（一次性结论 / 复盘 / 审计）→ `reports/<主题>_<YYYYMMDD>.md` 或 `output_report/`。
> 区域级事实 → 一律 `tracking/<R>/reference/`，`docs/reference/<R>/` 不再新增。

---

## 4. 可迁移 / 重构的文件清单

| # | 类别 | 具体文件 | 从 → 到 | 阻塞 / 前置 |
|---|---|---|---|---|
| 1 | MCP 拆分 | `wqb_db_mcp.py`（3026 行） | 根 → `mcp_servers/wqb_db/tools_*.py`（按现有 10 个分节注释切） | 需保持 `@mcp.tool` 函数名不变（skill 引用名） |
| 2 | MCP 归位 | `world-quant-brain-mcp/*.py` + `deploy/` + `Dockerfile` + `Makefile` | → `mcp_servers/wq_brain_http/` | `.mcp.json` 的 `url` 不变，但要同步 `main.py` 路径；`.venv` 留在原位免重装修 |
| 3 | tools 下沉 | THEMES.json 已归属的 168 个脚本 | `tools/*.py` → `tools/<主题>/` | 换 `find_repo_root(__file__)`；补 `tools/README.md` |
| 4 | tools 补登记 | 8 个无主题脚本 | 补 `THEMES.json.themes.<主题>.files` 或迁 `tracking/<R>/scripts/` | 先定归属，勿默认塞已有目录 |
| 5 | 备份件清理 | `tools/full_template_campaign.py.bak_20261021_2242` | → `attic/` 或删 | — |
| 6 | src 分层 | 29 个包根模块 → `core/ domain/ gates/` | 加子包 + `__init__.py` 再导出 | 保持 `from wqb.config import …` 不断 |
| 7 | 区域参考归一 | `docs/reference/{DEU,GBR,IND}/`、`docs/reference/EUR/*` 中的区域事实 | → `tracking/<R>/reference/` | DEU 需先建 `tracking/DEU/reference/` |
| 8 | 报告归位 | `docs/reference/EUR/{FIELD_PROPERTY_RULES, FULL_COVERAGE_RULE_v2, SIGNAL_MINING_WORKFLOW, TEMPLATE_CALIBRATION_20261020}.md`、`datasets/QUERY_API.md` | → `reports/<主题>_<YYYYMMDD>.md`（一次性）或改 snake_case 留 docs（SOP） | 先判「会不会过期」 |
| 9 | 重复件合并 | 27 组 md5 相同文件 | `validator.py`/`helpful_functions.py`/`ace_lib.py`/`diversity_enhancer.py` → 单一权威 + 薄 wrapper | 已有 `test_gem_skill_paths` 守 byte-identical，别破坏 |
| 10 | 同题双份 | `field-profile-ind-inst-fund-20261019.md` vs `field_profile_ind_inst_fund_20261019.md` | 保留扩展版，删旧版 | — |
| 11 | 运行态隔离 | `tracking/USA/runs/`（242 件）、`tracking/{EUR,IND,USA}/results`（未 ignore） | 加 `.gitignore` 或迁 `cache/` | S18 要扩到扫未入库面 |
| 12 | 根目录清理 | `agents.md` → 登记 S7 白名单（它是文档主干，不该删）；`selfcorr_quick_out/` → `cache/` 或 gitignore | — | — |
| 13 | 空目录 | 8 个空目录 | 删或补 `.gitkeep` | — |

---

## 5. 优化优先级

| 优先级 | 事项 | 理由 | 工作量 | 验收 |
|---|---|---|---|---|
| **P0-1** | 补 CI（`.github/workflows/gates.yml`）+ 钩自动安装脚本（`tools/install_hooks.sh`，写入 README 首屏） | 修根因；否则下面全都会复发 | 0.5d | 干净克隆 `git commit` 自动跑 gate |
| **P0-2** | 清掉当前 27 项违规（14 结构 + 13 测试） | 让棘轮回到绿，才能当门禁用 | 1d | `audit_structure` FAIL=0；`pytest 07_docs_skills` 全绿 |
| **P0-3** | `git add -A` 前先隔离运行态：`tracking/USA/runs`、`tracking/{EUR,IND,USA}/results` 入 gitignore | 防 242 件漏管文件被吸进索引 | 0.2d | `git status` 无 `?? tracking/**/runs` |
| **P1-1** | 拆 `wqb_db_mcp.py` → `mcp_servers/wqb_db/tools_*.py`，同步 INDEX 计数 47→49 | 不对称是持续制造文档漂移的源头 | 1d | `test_mcp_tool_counts_match_index` PASS |
| **P1-2** | tools 主题化迁移恢复推进（先迁 THEMES 已归属且无外部 import 的批次） | 170 平铺是最大的归类问题 | 3–5d（分批） | 每批后 `audit_structure` S11 不新增 FAIL |
| **P1-3** | 区域参考落点统一到 `tracking/<R>/reference/`；DEU 补目录 | 消除「两边都有」 | 1d | `docs/reference/<R>/` 只留 0–1 件索引 |
| **P1-4** | 文档命名 S16 清零（5 处大写 + 2 处日期位置 + output_report 63 件无日期） | 命名是可机检的，最该零容忍 | 0.5d | S16 FAIL=0 |
| **P2-1** | `src/wqb` 建 `core/ domain/ gates/` 三层，包根只留 `__init__` 再导出 | 表达已存在的事实分层 | 2d | 全量 `pytest` 绿 |
| **P2-2** | 合并 27 组重复件 + 删 8 个空目录 + `selfcorr_quick_out` 归位 | 减熵 | 1d | 重复扫描组数 ↓ |
| **P2-3** | 两个 MCP 服务物理归位 `mcp_servers/` | 结构对称 | 1d | `.mcp.json` 指向新路径后服务起得来 |

---

## 6. 建议遵循的命名规范

在现有 §8.13 基础上补三条可机检的硬规则：

| 对象 | 规范 | 正例 | 反例（当前存在） |
|---|---|---|---|
| 目录 | 全 kebab-case，小写 + 连字符 | `tools/data-repair`、`mcp_servers/wqb_db` | `selfcorr_quick_out`（下划线） |
| Python 模块 | snake_case，动词或名词短语，禁缩写后缀 | `tools/verify_platform_fields.py` | `full_template_campaign.py.bak_20261021_2242` |
| **规范文档（docs/）** | snake_case，**无日期**，名词短语 | `docs/reference/operator_availability_ledger.md` | `FIELD_PROPERTY_RULES.md`、`QUERY_API.md` |
| **一次性报告** | `<主题>_<YYYYMMDD>.md`，**日期必须在末尾** | `reports/ind_submit_checklist_20261020.md` | `docs/reference/field-profile-ind-inst-fund-20261019.md`（日期不在末位 + 连字符） |
| 区域级事实文档 | `tracking/<R>/reference/<dataset>.md`，区域不进文件名 | `tracking/KOR/reference/analyst81.md` | `tracking/KOR/reference/field_profile/analyst81.md`（子目录重复） |
| skill 目录 | kebab-case；前缀语义 `brain-*`（业务）/ `wq-brain-*`（编排）/ `wqb-*`（横切） | `wq-brain-ra-eur` | — |
| MCP 工具模块 | `tools_<域>.py`，与工具注册分组一一对应 | `tools_ledger.py` | `wqb_db_mcp.py`（一体） |
| 归档包 | `attic/<主题>_<YYYYMMDD>/` | `attic/probe_sop_retired_20261020/` | — |
| 禁止 | 文件名中出现作者盘符 / `~` / 安装位路径 | — | `_usa-news-transformer-scores-field-profile-20261023.md:5` 写 `C:\Users\MENGTAO\.qoder-cn\...` |

---

## 7. Skills 规范性评估

### 7.1 做得好的（确实高于平均水平，值得保留）

- **四层元文档齐备且职责不重叠**：`INDEX.md`（路由/分层）· `CONTRACT.md`（写作契约）·
  `GLOSSARY.md`（术语）· `CHANGELOG.md`（变更）——这是很多项目没有的。
- **契约可执行**：frontmatter 四必填、`name`==目录名、`description ≤300`、正文必含
  `## 职责边界` 三条；**同一产物只允许一个主写方**（硬裁定②）直击多写方事故。
- **棘轮机制**：`skill_capabilities_baseline.json`（能力只许减）、
  `skill_lint_baseline.json`（违规只许减）、`destructive_default_baseline.json`、
  `region_literal_baseline.json`、`doc_path_refs_baseline.json`——5 份基线锁住退化。
- **表由代码生成**：区域表 / 闸表 / 开关表 / MCP 计数全部生成器产出 + 测试逐字比对，
  从源头消除「文档写 47、代码是 49」这类漂移（虽然这次刚好在这条上 FAIL 了）。
- **内嵌副本有纪律**：GEM 内嵌 `skills/` 的四条可测纪律（byte-identical / 不得出现 SKILL.md /
  产物写 skill 树外）写得很实。

### 7.2 漏洞与待改进（13 项测试失败 + 33 项漂移）

#### A. 流程漏洞（最严重）：新增内容不过闸就入库

13 项失败里 **至少 8 项直接来自 2026-10-21～23 新增的 USA 字段画像文档和一次性脚本**：

| 失败测试 | 具体位置 | 性质 |
|---|---|---|
| `test_skill_lint::test_no_new_skill_lint_violations…` | `_usa-pv149-field-profile-20261023.md` 含 `ts_decay_linear(2a+3a, 22)` → `POISON:infix_leg_sum`；`_usa-us-equity-news-…-20261023.md` 含 `ts_max` → `INACCESSIBLE` | **文档里写了会毒死整批的表达式** |
| `test_skill_lint::test_expression_check_reports_policy_violations_only` | 同上 + `get_datasets(limit=…)` 参数不在签名 | MCP 参数写错 |
| `test_no_hardcoded_skill_root_in_skills_markdown` | `_usa-news-transformer-scores-field-profile-20261023.md:5` 写 `C:\Users\MENGTAO\.qoder-cn\tmp\…` | 作者本机路径进了 skill 文档 |
| `test_relative_links_resolve_in_all_skills_markdown` | `_usa-analyst-consensus-fa-overlay-field-profile-20261021.md` → `../../wq-window-valley-break-prod-wall/SKILL.md`（该 skill **不在** Claude/skills，在用户级安装位） | 相对链接越界 |
| `test_fe_ledger_readers_and_gate_claims_hold` | `tools/full_template_campaign.py` 新增为 fe ledger 读取方 | 破坏「唯一写入方」硬裁定② |
| `test_no_new_region_literal_branches` | `tools/check_usa_os_subset.py`（USA）、`tools/review_scope_quality.py`（EUR） | 区域差异应进数据层，不该写字面量分支 |
| `test_no_author_drive_paths_in_runtime_string_constants` | `tools/vwap_histogram.py:93` → `D:\coding\traeCN_project\wqb\output_report\*.png` | 运行时硬编码盘符 |
| `test_mcp_tool_counts_match_index` | INDEX 写 47，实为 **49** | 计数漂移 |

➡️ **根因同源**：钩不随克隆生效 + 无 CI ⇒ 写文档/脚本的人不会被拦。
➡️ **建议**：CONTRACT §5 的「质量门禁」段从「必须跑」升级为「**由 pre-commit + CI 强制跑**」，
并把 `tools/sync_skills.py --check` 也纳入同一条命令。

#### B. 安装位漂移（33 项）

`sync_skills.py --check` 对 5 个安装位报漂移（`~/.claude` 6 / `~/.codex` 6 / `~/.cline` 6 / `~/.agents` 6 / `~/.workbuddy` 9）：

- 4 个 USA 新字段画像文档 **MISSING**（全 5 位）
- `wq-brain-campaign-toolkit/scripts/metrics_cache.py` **STALE**
- `wq-brain-ra-usa/rules/gate-and-submit-discipline.md` **STALE**
- `~/.workbuddy` 位额外 3 项 STALE：`wq-brain-ra-deu/{SKILL.md, references/_probe-sop.md, scripts/README.md}`

⚠ **这里有个真陷阱**：`.claude/skills` 是 `Claude/skills` 的联接（S15 判定「无漂移概念」），
但其余 4 位是**真拷贝**。一旦有人只改仓库不同步，运行时加载的是安装位那份旧版——
「改了没生效」类事故就是这么来的。建议把 `--check` 做成 CI 必过项。

#### C. 结构性问题

1. **4 组跨 skill 复制件**（S6 WARN，已登记但未治理）：`ace_lib.py`、`diversity_enhancer.py`、
   `helpful_functions.py`、`validator.py`（后者 4 份 byte-identical）。
   现状靠「同步脚本 + byte-identical 测试」维持，**成本高且脆弱**——建议改为单一权威 + 薄 wrapper。
2. **边界声明与实现可能不一致**（CONTRACT §2 自己承认：曾发现 ≥6 个 skill 边界与正文/代码矛盾）。
   机检只覆盖「三条有没有」，不覆盖「写得对不对」——这是**已知未解**的洞，建议补 doc→code 对照测试。
3. **skill 数量 47 个，`brain-*` 命名族存在语义漂移**：
   `brain-alpha-research` / `brain-alpha-research-field-quality` / `brain-alpha-research-hypothesis-first` /
   `brain-alpha-research-news-sentiment` 四个同前缀但层级不同；`wq-brain-alpha-optimization-v1`
   带 `-v1` 版本号后缀，与 CONTRACT「layer 不是版本号」的精神相悖（改名成本高，建议至少在 INDEX 标注）。
4. **skill 内嵌 `scripts/` 与 `tools/` 的边界模糊**：`Claude/skills/*/scripts/` 里放了
   `gate.py`、`scan_fields.py`、`campaign.py` 等引擎实现，而 `tools/` 也有 `gate_attribution.py`、
   `wave_gate.py`、`submit_queue.py` 等同名件（S3 判定「非缺陷」）。
   → 但**同名 8 件**（`alpha_properties`、`dataset_experience`、`forum_recon`、`forum_recon_wave`、
   `gate_attribution`、`submit_queue`、`waiver`、`wave_gate`）意味着排查问题时要在两套命名空间里找，
   建议至少在 `tools/README.md` 加一行「同名件对照表：skill 引擎版 vs tools CLI 版」。
5. **外部依赖未入版本控制**：`docs/reference/GBR/…` 与 `wq-brain-ra-usa/rules/signal-mining-workflow.md`
   引用仓库外的 `C:\Users\MENGTAO\wqb-scripts\wqb_tools.py`。换机器即断。
   建议要么收编进 `tools/`，要么在文档里显式标注「外部依赖，已废弃」。

---

## 8. 建议的最小修复序列（按依赖排序）

```
第 1 步（0.5d）补 CI + 钩自动安装      ← 不修这个，后面修完还会再坏
第 2 步（0.2d）gitignore 补 tracking/USA/runs、tracking/{EUR,IND,USA}/results
第 3 步（1d）  清 27 项违规：
   - 删 .bak_20261021_2242；8 个无主题脚本补 THEMES 或迁走
   - 5 处大写文档 rename；2 处日期移末尾；output_report 无日期件补日期
   - tools/vwap_histogram.py:93 → find_repo_root()
   - tools/check_usa_os_subset.py / review_scope_quality.py 区域字面量 → 数据层
   - 4 份 USA 字段画像文档删违规表达式 / 修 MCP 参数 / 删本机路径 / 修越界链接
   - INDEX 计数 47 → 49
   - tools/full_template_campaign.py 的 fe ledger 读取 → 交回 feature_engineering 节点
第 4 步（0.5d）sync_skills.py --apply（清 33 项漂移）+ --check 进 CI
第 5 步（1d）  拆 wqb_db_mcp.py → mcp_servers/wqb_db/tools_*.py
第 6 步（3-5d）tools 主题化分批迁移（每批后跑 audit_structure + 全量 pytest）
第 7 步（1d）  区域参考归一到 tracking/<R>/reference/（DEU 补目录）
第 8 步（2d）  src/wqb 建 core/ domain/ gates/ 三层
```

---

## 附：可复现命令

```bash
$WQ_PY tools/audit_structure.py                      # 结构闸门（当前 FAIL=14 / WARN=4）
$WQ_PY tools/sync_skills.py --check                  # skill 安装位漂移（当前 33 项）
$WQ_PY tools/skill_lint.py                           # skill 文档棘轮
$WQ_PY -m pytest tests/unit/07_docs_skills -q        # 当前 13 failed / 1325 passed
$WQ_PY -m pytest tests/unit/07_docs_skills/test_skill_integrity.py \
                 tests/unit/07_docs_skills/test_skill_boundaries.py -q   # 契约面：绿
git config core.hooksPath                            # → tools/git-hooks（本机，不入库）
```

---

# 执行进度（同日 01:30 落地 P0）

按 §8 最小序列推进，**结构闸门 FAIL 14 → 1、skills 测试 13 failed → 2 failed（1337 passed）**。

## 已落地

| # | 动作 | 产出 |
|---|---|---|
| 1 | **钩自动安装** | `tools/git-hooks/install.sh` + `install.ps1`（`--check` / `--unset`，幂等）；README §3 升为「新克隆第一步，必做」并写明为什么不能只写 `git config` |
| 2 | **CI 兜底** | `.github/workflows/gates.yml`（audit_structure / doc_path_refs / destructive_default / skill_lint / pytest / 钩挂载自检） |
| 3 | **运行态隔离** | `tracking/.gitignore` 加 `runs/`（止住 242 件增量）；根 `.gitignore` 加 `/selfcorr_quick_out/`；S17 白名单登记该目录 |
| 4 | **S7 根散件** | 根文档 `agents.md` → `AGENTS.md`（白名单与 1533 处引用都是 `AGENTS.md`，此前只有磁盘名是小写；Windows 不区分大小写 ⇒ 要用 OS 重命名，`git mv` 会因「源不在版本控制」失败） |
| 5 | **S11 / S14** | `.bak_20261021_2242` 移 `attic/tool_backups_20261024/`；9 个无主题脚本补进 THEMES（`wave`/`fields`/`backtest`/`research`）；`targeted_dev.py` 补 README 登记 |
| 6 | **S16 命名** | 5 处大写改 snake_case；`TEMPLATE_CALIBRATION_20261020.md` 迁 `reports/eur_template_calibration_20261020.md`；2 处日期移末尾；**同题双份合并**（hyphen 版是 underscore 版的严格超集 `230a231,456`，覆盖后删 hyphen 版） |
| 7 | **S4 硬编码** | `vwap_histogram.py:93` 盘符 → `__file__` 上溯 + `WQB_OUT_DIR` 环境变量 |
| 8 | **区域字面量** | `check_usa_os_subset.py` / `review_scope_quality.py` 的 `== "USA"` / `not in ("EUR",)` → 环境变量（`WQB_REGION` / `WQB_DETAIL_REGIONS`），消除 AST Compare 命中 |
| 9 | **skill 文档内容** | 删作者本机路径；修越界相对链接；`get_datasets(limit=)` 删不存在的参数；`ts_max`（不可访问算子）→ `vec_max` + 警示；4 处中缀 `+` 毒模式 → `add()`；4 处门槛数字加 `<!-- from config.X -->`；INDEX 计数 47 → 49 |
| 10 | **反向漂移修复** | `_dataset-scan-method.md` + `dataset_scan.py` **此前只存在于宿主安装位**（被 `docs/experience/03_region_dataset.md` 引用，仓库却没有 = 违反「不允许源码只存在工作区」）⇒ 回灌 `Claude/skills/wq-brain-ra-deu/` |
| 11 | **安装位漂移清零** | `sync_skills.py --apply` → 5 个安装位全 OK（原 33 项漂移归零） |

## 剩余 3 项（均非可自动处置）

| 项 | 原因 | 处置 |
|---|---|---|
| **S11 tools 顶层 17 脚本** | `full_template_campaign.py` 有 **2 个 python 进程在跑**（PID 1152 / 98600，EUR OTHER 战役 `--max-inflight 7`），`campaign_semantics.py` 是它当天拆出的依赖。**移动文件会打断在跑的战役** | 等进程结束后按 THEMES 归属迁移，并把路径推导统一改 `find_repo_root(__file__)` |
| **`test_fe_ledger_readers_and_gate_claims_hold`** | `tools/full_template_campaign.py` 新增为 fe ledger 读取方，破坏「同一产物只有一个主写方」；同一批运行中脚本 | 同上，等战役结束再改（改法：读取改走 `feature_engineering` 节点） |
| **`test_expression_check_reports_policy_violations_only`** | 既存失败，与本次修复无关。实测 `check_exprs()` 对 `add(rank(ts_mean(aaa1,22)), rank(ts_mean(bbb1,22)))` 返回 0 违规——闸门在无 dataset 上下文时对跨腿 `add()` 不判（避免误伤合规的单信号多窗 `add`）。**测试期望与实现已脱节** | 需人工裁定：改闸门判据（有放开毒模式的风险）还是改测试期望（承认该形态不判）。**未擅自改动** |

## 顺带发现（未处置，留给下一批）

- `tools/code-audit/db_mcp_split.py` **已存在**——`wqb_db_mcp.py` 的拆分生成器（`--plan` / `--apply`，带组间 DAG 环硬门，实测 `mutations ↔ harvest`、`rotation ↔ mutations` 互引成环）。所以报告 P1-1 的拆分**工具现成**，执行前先看 `reports/db_mcp_split_20261004.md` 的 26 条待改断言。
- `sync_skills --apply` 报 **12 个 ONLY-AT-INSTALL**（安装位有、仓库没有的顶层 skill 名，如 `wq-brain-ra-eur` / `wq-brain-ra-pipeline` / `wq-window-valley-break-prod-wall` 等）。这些是用户级 skill，仓库不承载；若其中有本应入库的，需逐个裁定后回灌（同 #10 的做法）。
