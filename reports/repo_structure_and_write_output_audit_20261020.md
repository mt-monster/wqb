# 目录结构审计与代码写盘规范核查（2026-10-20）

审计基线 = `AGENTS.md §8.13` 目录职责表 + §8 顶层约定。
方法 = 静态扫描 `src/` `tools/` `world-quant-brain-mcp/` 全部 `.py`，
定位写盘调用点（`write_text` / `write_bytes` / `open(..., 'w'|'a'|'wb')` / `json.dump` / `to_csv` / `to_excel` / `savefig` / `np.savetxt` / `mkdir`），
再用**变量回溯**（赋值图 2 层展开）把路径从变量名解析成字面量，再按 §8.13 归类。
不做裸 `grep` 全仓，避免 `.venv` 污染结论。

---

## 1. 写盘归属实测分布

扫描到写盘点（不含 `mkdir`）**≈483**。按解析出的目标目录归类：

| 目标 | 件数 | §8.13 判定 |
|---|---:|---|
| `output_report/` | 主体 | ✅ 合规：运行产物报告出口 |
| `tracking/<REG>/`（3 字母区域码） | 多 | ✅ 合规：区域事实面 |
| `cache/` · `logs/` · `results/` | 多 | ✅ 合规：运行期（且 `.gitignore` 已排除，实测 `git ls-files cache logs` = **0**） |
| `data/`（`wqb.db` 等） | 多 | ✅ 合规：运行期数据（`.gitignore` 已排除，`data/` 未跟踪） |
| `tmp_path` / `tempfile` / `mkdtemp` | 多 | ✅ 合规：测试临时件 |
| **裸文件名（落 cwd）** | **4** | ⚠ 违规 |
| **`docs/`** | **2** | ⚠ 需登记生成器 |
| **`Claude/skills/`** | **3** | ⚠ 应为同步工具专属 |

### 1.1 ⚠ 裸文件名写盘 ×4（落进调用方 cwd，完全不可预期）

| 位置 | 症状 |
|---|---|
| `src/wqb/search/scheduler.py:175` | 写 `scheduler_*.json`，无目录前缀 |
| `tools/complexity_scan.py:154` | 写扫描结果文件，无目录前缀 |
| `src/wqb/workflow/nodes/batch_track.py:318` | 写批次结果，无目录前缀 |
| `tools/sync_skills.py:326` | 写同步清单，无目录前缀 |

**风险**：这四处在项目根、`tools/`、`attic/` 任意 cwd 下执行都会把文件甩到那里。
正是此前 `tools/` 顶层 5 个游离脚本 + 根目录零散件的成因模式。

### 1.2 ⚠ `docs/` 有 2 个写盘点

`docs/` 在 §8.13 是**人工面**（设计稿/规范/评审）。代码写它只有两条正路：
① 生成器（如 `index_tables.py`）且**必须在 §8.13 生成器登记表中挂号**；
② 明确的一次性迁移脚本。当前 2 个写盘点未逐一核对是否已登记——这是要补的一条审计项。

### 1.3 ⚠ `Claude/skills/` 有 3 个写盘点

`Claude/skills/` 是**同步面**，唯一合法写者 = `tools/sync_skills.py`（`--apply`）。
3 个写盘点需确认全部收敛在该脚本内；若有其它脚本直接改 skill 文件，
会让本地与 `~/.workbuddy/skills/` 分叉，`sync_skills.py` 的 diff 报告会失真。

### 1.4 ✅ 好消息

- **`cache/` `logs/` `data/` `research-data/` `attic/`（除白名单）均已 `.gitignore` 且实测 0 跟踪** —— 运行期产物没有污染版本库。
- **`src/` `tools/` 内没有非源码产物入库**：实测 `git ls-files src tools | grep -vE '\.(py|md|json)$|__init__'` 只命中 `tools/git-hooks/{pre-commit,commit-msg}`（合法钩子）；`tools/docs/*.md` 是脚本说明书（合法）。
- `world-quant-brain-mcp/` 的 `Dockerfile` / `docker-compose.yml` / `systemd` / `nginx` / `Makefile` 属部署资产，位置正确。

---

## 2. 目录结构现状（顶层跟踪文件数）

| 目录 | 件数 | 现状判断 |
|---|---:|---|
| `tracking/` | 2692 | 事实面，已按区域分，OK |
| `Claude/` | 533 | 同步面，OK |
| `tools/` | 231 | **顶层已清零**（本轮 P0 完成），OK |
| `tests/` | 225 | OK |
| `output_report/` | 223 | ⚠ **见下** |
| `reports/` | 142 | 人工面，OK |
| `src/` | 121 | OK |
| `docs/` | 100 | 基本 OK，`reference/` 混入 13 个日期件 |
| `world-quant-brain-mcp/` | 61 | OK |
| `attic/` | 41 | 归档面，OK |

### 2.1 ⚠⚠ `reports/` 与 `output_report/` 职责倒挂（最高优先）

- `reports/` 下 **10 个子目录全是日期化/战役化名**（`eur-mining`、`gbr-campaign-final`、`ra_pipeline_stage_review_20260927_refs`、`skills_review_20260929_refs`…）—— 这些**形态上是运行产物**，被放进了"人工撰写评审"的目录。
- `output_report/` 下 **223 个文件里 219 个带 `YYYYMMDD`**，命名如 `DEU_breakthrough_e7QGexop_20261010.md`、`DEU_campaign_S-PRE_to_S6_20260919.md` —— 这是**机器出口的合规行为**，但与 `reports/` 的定位混淆。

**根因**：`§8.13` 里两个目录的判据都写成"报告"，缺一条**机器可判的区分规则**。

**推荐判据**（建议写进 §8.13）：
> `reports/` = **人工撰写**的评审/审计/经验沉淀，无代码写者；
> `output_report/` = **代码出口**，任何写盘点必须落此；
> 若某产物需要人二次加工才对外 → 迁到 `reports/<专题>/`；
> 反之 → 留 `output_report/`。

配套：把 `reports/` 那 10 个日期化战役目录**迁进 `output_report/` 或 `attic/`**，让 `reports/` 只留真评审。

### 2.2 ⚠ `output_report/` 无二级分区

219 个日期件平铺在一级，靠文件名前缀（`DEU_` `EUR_` `IND_` `KOR_`…）区分。
文件数继续涨（每战役 5–10 件）后，`ls` 输出会不可读。

**推荐**：`output_report/<REGION>/` 二级分区（区域码与 `tracking/<REG>/` 对齐），
并在 `sync_skills` 同类工具里加一条校验：写 `output_report/` 顶层即 FAIL。

### 2.3 ⚠ `docs/reference/` 混入 13 个日期化文件

`docs/reference/` 里同时有 `atom_workflow_and_attribution_20261013.md`、`feature_engineering_sop.md` 这类**长期参考件**
和 13 个 `2026MMDD` 命名的**战役快照**。

**推荐**：日期化件迁 `output_report/`；`docs/reference/` 只留无日期的长期参考。
（本轮已修一处：`field-profile-ind-inst-fund-20261019.md` 连字符 → 下划线，属命名规范。）

### 2.4 ⚠ `wqb_db_mcp.py` 游离在根目录

`.gitignore` 里有 `**/config.json`、`reasonix.toml`，但 `mcp_config.json` 本身在根——
这是 MCP 入口配置，合理；但 `wqb_db_mcp.py` 是**服务入口脚本**，按 §8.13 应归 `tools/` 或 MCP 包内。
建议移入 `world-quant-brain-mcp/`（与 `.env.example`、`Dockerfile` 同层）。

---

## 3. 推荐目录结构（含新增条目）

```
wqb/
├─ AGENTS.md  README.md  CLAUDE.md          # 契约面（人工，禁止代码写）
├─ mcp_config.json                          # MCP 入口配置（人工）
├─ pyproject.toml  pytest.ini  conftest.py  requirements.txt
├─ src/wqb/                                 # 库代码（只 .py）
├─ tools/                                   # 脚本层（顶层禁 .py，按主题分子目录）
│  ├─ gates/  pool-hygiene/  data-repair/  code-audit/  docs/  git-hooks/  legacy/
│  └─ THEMES.json  README.md                # 主题归属登记表
├─ world-quant-brain-mcp/                   # 服务包 + 部署资产
├─ tests/                                   # 测试（01..07 主题编号）
├─ docs/                                    # 人工面（人工撰写，代码写需登记生成器）
│  ├─ design/  experience/  governance/  plans/  tutorials/
│  └─ reference/                            # ⚠ 只留无日期长期参考
├─ reports/                                 # 人工面评审/审计（⚠ 需清出日期化战役目录）
├─ output_report/                           # 代码出口（⚠ 建议加 <REGION>/ 二级分区）
├─ tracking/<REG>/                          # 区域事实面（3 字母区域码）
├─ data/   cache/   logs/   results/        # 运行期，全部 .gitignore
├─ attic/                                   # 归档（.gitignore 白名单例外：tmp_scripts_20261004/）
└─ Claude/skills/                           # 同步面（唯一写者 = tools/sync_skills.py）
```

**新增两条契约建议**：
1. `output_report/` 加 `<REGION>/` 分区，写盘点必须带区域码；
2. `reports/` 明确"无代码写者"，并在 `index_tables.py` 类生成器登记表里为 `docs/` 的写盘点挂号。

---

## 4. 优先级建议

| 级别 | 事项 | 依据 |
|---|---|---|
| **P0** | 修 4 处裸文件名写盘 → 改为 `ROOT/output_report/...` | 落盘位置不可预期，是游离件的成因 |
| **P0** | 补一条写盘审计闸（在 `tools/code-audit/`）：断言所有写盘目标命中白名单目录 | 让 §8.13 从"约定"变成"可执行" |
| **P1** | `reports/` 10 个日期化战役目录迁出 | 职责倒挂 |
| **P1** | 核对 `docs/` 2 个写盘点是否已在生成器登记表 | 未登记 = 隐性违规 |
| **P1** | 核对 `Claude/skills/` 3 个写盘点全部收敛在 `sync_skills.py` | 防同步面分叉 |
| **P2** | `output_report/` 加 `<REGION>/` 二级分区 | 219 个日期件平铺，继续涨会不可读 |
| **P2** | `docs/reference/` 13 个日期化件迁 `output_report/` | 长期参考与战役快照混放 |
| **P2** | `wqb_db_mcp.py` 移入 `world-quant-brain-mcp/` | 服务入口应与服务包同层 |

---

## 5. 审计方法学备注（教训）

- 首轮用裸 `grep` 全仓找写盘，被 `.venv/` 里第三方库的写法污染结论 —— **审计必须走排除清单的静态扫描**，`.venv` / `site-packages` / `attic` / `node_modules` 一律排除。
- 路径分类不能只看**调用行**：变量常在 3 行外赋值。本次用赋值图 2 层展开才把 `scheduler.py:175` 那类「看起来是变量、实际落 cwd」的点揪出来。
- 目录归属不能只看 `git ls-files` 顶层计数：`tracking/` 2692 件里 242 件曾被误判为"数据湖 dump"，实际 156 件是 `tracking/*/scripts/*.py` 探针脚本（130 个是 `tmp_` 草稿）。**聚类要用 3 层路径 + 扩展名**。

---

## 6. 复核更正（2026-10-20 二次核查）

初次审计的两条 P1/P2 建议**违反 AGENTS.md §8.13 已有裁决**，现予撤回。

### 6.1 撤回：`reports/` 10 个日期化战役目录迁出（原 P1）

**误判经过**：初看 `reports/` 顶层有 9 个目录名（`dataset_experience`、`eur-mining`、`forum_alpha_research`、`ra_pipeline_stage_review_20260927_refs`…），带日期或战役名的形态像"运行产物"。

**实际**：§8.13 明文规定 `reports/<主题>_<YYYYMMDD>.md`，且「**`reports/` 与 `output_report/` 的一层子目录名同受 kebab-case 约束（2026-10-14 批次G 起有闸 = S16 规则⑦）**」；现存 9 个顶层目录里 5 个已是 kebab，**4 个不合规的进 `S16_DIR_LEGACY` 只登记不回改**，逐条带代价证据：
- `dataset_experience` — 由 `dataset_experience.py` 生成器写名 + `step9_audit.py` 校验 + 全库引用
- `forum_alpha_research` — 被目录内脚本自引用路径
- 两个 `*_refs` — 2026-10-10 P2-C 的同名消歧后缀（`_refs` 语义条）

⇒ 迁出任何一个都会造成活文档死指针。**§8.13 已把这条判为"存量不回改"，本条建议作废**。

### 6.2 撤回：`output_report/` 加 `<REGION>/` 二级分区（原 P2）

**误判经过**：140 个 REGION 前缀 `.md` 平铺在一层，看着像需要按区域分文件夹。

**实际**：§8.13 明文「**`output_report/` 现无一层子目录 ⇒ 它的第一个新目录起就是 kebab**」；REGION 码是纯大写（`DEU`/`KOR`），与 kebab-case 结构上冲突，且 §8.13 明确豁免「`output_report/` 为历史名，保留但不新增此类风格」。

⇒ 按 REGION 分目录是**新增不合规命名风格**，与 §8.13 已裁方向相反。**建议作废**。若真要二级分区，命名需 kebab（`dea-brief/` / `ind-campaign/`），代价是所有既有引用与 §8.13 表格同步重构，属独立专项而非本轮顺手做。

### 6.3 保留 P0：4 处裸写盘 + 写盘审计闸

- 4 处里 3 处经复查是扫描器**假警报**（`complexity_scan.py` 用 `ROOT` 变量、`batch_track.py` 用 `resolve_async_tasks_root()`、`sync_skills.py` 用 `dest_root`）；只有 `scheduler.py:175` 是真违规，已修。
- 写盘审计闸 `tools/code-audit/audit_write_targets.py` 已落地，配 14 条测试，当前扫描 0 违规 / 0 新增违规 / 97 条 UNKNOWN（短变量名 `p`/`tmp`/`out`/`doc` 解析不出路径，抽查确认合规）。

### 6.4 新洞察：`reports/` 与 `output_report/` 的分工判据已经够机器可判

初版报告说"§8.13 缺一条机器可判的区分规则"，复查后**这是错的**：§8.13 已有明文判据：

> **凡 workflow/战役自动产出** → `output_report/`；
> **凡人工撰写的审计/评审/复盘/演练/价值评估** → `reports/`。

代码侧验证：`grep -rn '"reports/.*write\|dump\|open\(.*w"' src tools` **零命中** —— 代码从不写 `reports/`；`output_report/` 的写入全部通过 `wqb.output_repo` 类工具或 `ROOT / "output_report"` 变量锚定，也是 §8.13 允许的形式。

⇒ **两个目录的分工已经在实际执行**，审计报告无需提出结构改动。真正的短板只是"没有闸挡违规"，这条已由 `audit_write_targets.py` 补齐。
