# 区域 skill 四目录改造方案（rules / config / references / scripts）

> **决策**：用户 2026-10-18 明令——**每个 region skill 建四目录，保持「每区独有结构」**。
> 本文是执行方案（不是评估）；评估反面意见见 `skills_hierarchy_review_20261018.md` §6，结论已按用户决策覆盖。
> **硬约束（技术性，不可协商）**：`config/` **不做控制值事实源**，真身仍在 `tracking/<R>/config/`；
> `references/` 下的非类别文件**必须 `_` 前缀**（`render.check_structure` 判据），否则红。

---

## 一、目标形态

```
Claude/skills/wq-brain-ra-<region>/
├── SKILL.md              # 入口：frontmatter + 职责边界 + 结构导航 + 生成块（render 管）
├── rules/                # ① 该区独有的规则与纪律（手写，as_of 必带）
│   ├── README.md          # 索引：本区规则清单 + 与 SKILL.md 的分工
│   └── <该区特有规则>.md   # 六步覆盖详解 / 破闸杠杆 / 选集纪律 / 流程差异细则
├── config/               # ② 该区配置视图（真身指针 + 差异摘要 + 覆盖证据索引）
│   ├── README.md          # 三表分工说明 + 真身路径 + 改法
│   └── region_view.json   # 结构化摘要（as_of + 与 settings/thresholds/cells 的差异要点）
├── references/           # ③ 实证（已存在，render 按类别名生成组合分支卡）
│   ├── <类别>.md          # 组合分支卡（生成块 cell-panel，render 管，不得手改）
│   └── _<主题>.md         # 跨类别补充（战役实证 / 手册 / 快照）
└── scripts/              # ④ 该区独有脚本（探针 / 校验器；一次性脚本不留这里）
    └── README.md          # 家规 + 清单（当前为空也要有，说明为何空）
```

**四目录的差异化落点**：`rules/` 写该区独有纪律、`config/` 写该区配置差异、`references/` 写该区实证、`scripts/` 放该区探针——**同构目录、各区内容不同**。

## 二、兼容矩阵：什么不动、为什么

| 既有链路 | 处置 | 依据 |
|---|---|---|
| `render.py` 生成块（`region-panel` / `cells-index` / `manual`） | **不动**，仍在 SKILL.md | `render.py:735/788` 硬编码 `d / "SKILL.md"`；`set_block` 只替换 marker 区间 |
| `references/<类别>.md` | **不动** | `render.py:746/804/829` 硬编码 + `check_structure` 孤儿判据 |
| `tracking/<R>/config/*.json` | **不动**（`config/` 只做视图） | `profiles explain/render/sync-cells` 按 `config_dir_of(r)` 解析；覆盖值强制 `_evidence` |
| `tracking/<R>/scripts/` | **保留为脚本真身**，`scripts/` 只放 skill 级脚本 + README 指向 | AGENTS §8.13 已定归属 |
| `_` 前缀规则 | 扩展到 `references/` 全部非类别文件 | `render._is_supplementary` |
| SKILL.md 体量 | 从 186 行（USA）压到 ~90 行，手写大段迁 `rules/` | CONTRACT:6「实证叙事/区域细节放 references/」+ ≤250 行目标；同时解 GBR 315 / KOR 563 超体量 |

## 三、迁移步骤（可回滚，每步独立验证）

1. **建目录 + README**（四目录各一份，说明职责与真身指针）——零风险。
2. **写该区 `rules/` 内容**：从 SKILL.md 手写区搬运（六步覆盖详解、改控制、纪律速查），**SKILL.md 原位留一行指针**（不删，逐步收口）。
3. **写 `config/region_view.json`**：`as_of` + settings/thresholds/cells 的差异摘要（**不复制整表**，只记差异与证据指针）。
4. **SKILL.md 加「本区结构导航」块**：四目录入口表；随后把手写大段收缩为指针。
5. **验收**：`render --check` / `pytest test_profiles_layer` / `test_docs_consistency` / `skill_lint` / `doc_path_refs` 全绿（他人债除外）。
6. **推广**：脚本批量建 13 区骨架，内容按各区实际资产差异化填充（TWN 空壳声明、DEU 收编 scripts、KOR/GBR 收纳超体量段）。

**回滚**：每步只增目录/文件 + 改 SKILL.md 手写区 ⇒ 回滚 = `git checkout` 该区 SKILL.md + 删新增目录。**禁忌：删 SKILL.md 后跑 `render --apply`**（文件不存在 ⇒ 手写区被 skeleton 重建丢失）。

## 四、逐区内容规划（按实测资产）

| 区 | rules/ 要点 | config/ 要点 | references/ 现状 | scripts/ |
|---|---|---|---|---|
| **USA** | 六步覆盖详解、未点亮塔纪律、prod/SUB 两难墙、提交三条铁律 | 10 类别覆盖 + 三表差异 + 塔点亮快照 | 13 篇（+2 战役 +1 手册） | 空（真身待建 `tracking/USA/scripts/`） |
| KOR | 六步骨架特化、gatebreak 证据链 | 11 类别 | 17 篇 | 空 |
| GBR | SKILL 315 行超体量段下沉、语义类型层经验 | 14 类别 | 21 篇 | 空 |
| DEU | 破闸方法论、字段画像视图用法 | 11 类别 | 16 篇 | **收编现有 3 脚本**（现放 skill 内，未登记例外） |
| TWN | 「未开战役」声明（cells 0、`tracking/` 空） | 空壳声明 | 0 篇 | 空 |
| amr/chn/jpn/asi/hkg/mea/glb/ind/eur | 按各自 SKILL 手写区抽 | 按各自 cells | 2–16 篇 | 空 |

## 五、守护与验收（新增机械闸建议）

| 闸 | 位置 | 断言 |
|---|---|---|
| 四目录齐备 | `tests/unit/07_docs_skills/test_region_skill_layout.py`（建议新建） | 每个 `wq-brain-ra-*` 存在 rules/config/references/scripts 四目录且各含 README（references 无组合时可空） |
| 命名合规 | 已有 `render.check_structure` | `references/` 非类别文件必须 `_` 前缀 |
| config 不越权 | 新闸 | `config/region_view.json` 内不得出现 `_evidence` 之外的改值指令；真身路径指针必须指向 `tracking/<R>/config/` |
| SKILL 体量 | 已有 `test_skill_*` + CONTRACT | 迁完 USA 186 → ~90 行；GBR 315 / KOR 563 同期收敛 |
| 链接完整 | `test_docs_consistency` / `doc_path_refs` | 四目录 README 的相对链接全部可解析 |

## 六、已知限制（诚实登记）

1. `config/` 是**视图不是事实源**——这是为了不破 profiles 链的代价；改配置仍必须改 `tracking/<R>/config/`。
2. `references/` 无法真正目录化（render 硬编码 + 孤儿判据），四目录里只有它是「扁平 + 命名前缀」形态。
3. 手写区收缩后，SKILL.md 对「不打开 references 就不看规则」的快速读者信息密度下降——用结构导航表补偿。
4. 并发会话正在改 DEU/GBR/IND 等区文件，推广阶段须按区串行，避免同文件冲突。

## 七、第一步交付（本次已完成）

USA 样板：四目录 + `rules/`（3 篇）+ `config/`（README + region_view.json）+ `scripts/README.md` + SKILL.md 结构导航块，
并通过 render/测试/死指针四道验收。
---

## 八、执行记录（2026-10-18 12:40）

### 8.1 已完成

| 项 | 结果 |
|---|---|
| **工具** | `tools/gen_region_skill_scaffold.py`（幂等、只增不删；`--list` / `--region R` / `--all` / `--apply`） |
| **14 区四目录** | 全部就位：rules/README.md + config/{README.md,region_view.json} + scripts/README.md；references/ 原本就有（DEU 16 / KOR 17 / GBR 21 …），TWN 因未开战役**不建**（避免空目录与死链） |
| **SKILL.md 导航块** | 13 区插入 `<!-- region-scaffold:nav:start/end -->` 四目录导航；USA 已手工精修版（186 → **152 行**，三段手写大段下沉） |
| **USA 样板内容** | `rules/six-step-usa-override.md`（六步覆盖 + 改控制纪律）、`rules/gate-and-submit-discipline.md`（选集铁律 / 破 prod 旋钮 / D0-P / 提交三铁律 / base payment 选型）、`config/region_view.json`（默认档 + cells 概况 + 覆盖落差）、`scripts/README.md`（家规 + 为空的理由） |
| **顺带修复** | USA 10 张类别卡生成块过期（HEAD 既存漂移）→ `render --region USA --apply` 后 `check` 归零 |
| **验收** | `profiles check --region USA` = 0 问题；USA 孤儿 = 0；`doc_path_refs` 对四目录 0 死指针；`skill_lint` 对新增文件 0 违规；文档一致性仅剩并发会话的 `overview.md` 2 例 |
| **同步** | `sync_skills.py --apply` 已推 6 个安装位 |

### 8.2 未做 / 待办（按区串行，避免与并发会话冲突）

| 区 | 待办 | 原因 |
|---|---|---|
| **KOR** | 手写内容归位（SKILL 563 行超体量）、修生成块 | **并发会话正在整体重写该文件**（`layer: L4` 六步特化，diff 534 行）⇒ **禁止跑 `render --region KOR`**，会摧毁其重写；结构闸的 12 项面板不一致 + 全区 `check` 报错均源于此 |
| **GBR** | 手写内容归位（SKILL 315 行）、7 个孤儿中的 5 个 | 同属并发在途文件，先建目录与导航，归位等其收口 |
| **DEU** | `scripts/` 3 个一次性脚本迁 `tracking/DEU/scripts/` | 同上；当前已在 `scripts/README.md` 登记归属建议 |
| **TWN** | 是否冻结该区 skill 或补最小 references | 未开战役（cells 0、`tracking/` 空） |
| 全部 | `rules/` 实质内容（现为骨架 + 填写纪律） | 需各区战役实证支撑，不能凭空写 |

### 8.3 新增守护建议（未实施，待批准）

`tests/unit/07_docs_skills/test_region_skill_layout.py`：断言每个 `wq-brain-ra-*` 具备
rules/config/scripts 三目录 + README，且 `references/` 非空区必有该目录；`config/region_view.json`
必须带 `as_of` 且 `source_of_truth` 指向 `tracking/<R>/config/`。

---

## 九、第二轮推进（2026-10-18 13:00）：守护落地 + cells 覆盖补齐

### 9.1 A 项落地：四目录机械守护

新增 `tests/unit/07_docs_skills/test_region_skill_layout.py`（57 个断言，0.18s）：

| 断言 | 内容 |
|---|---|
| 扫描有效性 | 扫到 ≥10 个区域 skill（防扫描逻辑失效导致假绿） |
| 三目录 + README | rules / config / scripts 各须有 `README.md` |
| config 视图形状 | `region_view.json` 必带 `as_of`、`region` 与目录自洽、`source_of_truth` 三键均指向 `tracking/<R>/config/` |
| 导航块 | SKILL.md 必含 `<!-- region-scaffold:nav:start -->` 且链到三 README |
| references 存在条件 | cells 有类别 ⇒ 必须有对应 `<类别>.md`；无类别 ⇒ **不得**建空目录（空目录不被 git 跟踪且会造死链） |

### 9.2 B 项落地：USA analyst 组合覆盖（解决 explain 与实测不一致）

`tracking/USA/config/cells.json` 的 `cells.analyst` 新增 `backtest`（此前**零覆盖**）：

| 键 | 值 | 证据（写入 `_evidence`） |
|---|---|---|
| `neutralization` | `REVERSION_AND_MOMENTUM` | SECTOR 族 prod 0.703–0.720 全撞墙；RAM 降到 0.648–0.698 且 SUB 升到 0.83–0.89；`gJWoaJqv` 已 ACTIVE |
| `decay` | `20` | d10 档 S 最高但 prod 漂移 0.7088 撞线；d20 是唯一实证交付档；d15/d20 修 SUB（0.67→0.74/0.82） |

验证：`validate_cells` 0 错误 ⇒ `explain --region USA --dataset analyst` 现输出
`neutralization REVERSION_AND_MOMENTUM [cells.json:analyst]` + `decay 20`（附证据全文），
`profiles check --region USA` = 0 问题。
⇒ **效果**：任何人按 explain 派发 analyst 批次，默认即复现已验证档，而非区域默认的 SUBINDUSTRY/decay 5。

### 9.3 工具两处修正

- `insert_nav` 幂等守卫**只认标记**（原先耦合标题文案，文案一变就重复插入）
- 无 refs 的区（TWN）导航块**不链 `references/`**（修死链：docs_consistency 由此 3 红 → 2 红）

### 9.4 全量测试归属（本轮改动后）

| 归属 | 失败项 | 说明 |
|---|---|---|
| **本轮（我）** | **0** | 布局守护 57 绿 / lint 0 / 死指针 0 / sync 漂移 0 / profiles check(USA) 0 |
| 并发会话在途 | 17 → 修复后 **3** | 见下 |

**根因（一处笔误放大成 15 项失败）**：`wq-brain-ra-kor/SKILL.md` 第 1 行是 `\---  `
（多了反斜杠与尾空格）⇒ YAML frontmatter 解析为空 ⇒ 连带
`frontmatter_name` / `boundaries`×2 / `hooks`×4 / `sf_docs`×2 / `governance` / `sf_sweeps` / `profiles_layer` 面板 12 项全红。
**修法**：把第 1 行改回 `---`（与其它 13 区一致）即可一次解掉。
⇒ 该文件正被并发会话整体重写（`layer: L4` 六步特化），按纪律**未代改**，在此登记精确修法。

另 2 红为并发会话把 `reference.md` 改名 `references/overview.md` 时未修站内相对链接
（`brain-how-to-pass-alpha-test` / `wq-brain-alpha-optimization-v1` 各 1 个文件）。
