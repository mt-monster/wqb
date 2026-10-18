# 输出目录分类方案（output_dirs_taxonomy）

> 2026-10-10 第四轮输出目录治理建立。定位：**长期规范**——回答「一份新文件该放哪、为什么、谁来守」。
> 治理过程与逐轮结论见 `reports/output_dirs_governance_*`；目录职责的上游原文在 AGENTS.md §8.13。
> 本文只做**分类归纳**，不重复整改记录。

---

## 1. 目录职责总表（每类文件的唯一去处）

| 你要放的东西 | 唯一去处 | 守闸 | 反例（都曾真实发生） |
|---|---|---|---|
| 战役 / ideas / 评审**产物**（自动产出） | `output_report/` | S16（命名）+ 规则⑤（禁 .py） | 报告两头分流到 `reports/` |
| 人工审计 / 复盘 / 演练报告 | `reports/<主题>_YYYYMMDD.md` | S16 + S5（禁 .py，证据脚本豁免） | 一次性排障脚本堆在 `reports/` |
| 可复用 CLI | `tools/`（+ `tools/README.md` 登记 + `THEMES.json` 归属） | S11（顶层冻结）+ S14（登记） | 根目录出现第 20 个「顺手写的小工具」 |
| 一次性 / 会话草稿脚本 | `logs/_tmp_*.py`（用完即删） | — | 根目录 `_diag*.py`×19（2026-10-10 事件） |
| 区域专属探针 | `tracking/<REGION>/scripts/`（用完进 `scripts/archive/`） | S10 | 跨区探针塞进单区目录 |
| 长期规范 / SOP / 速查 | `docs/`（更新 `docs/README.md` 索引） | S9（声明目录存在） | 结论性知识写进 `output_report/` |
| 运行期断点 / checkpoint | `cache/`（断点）`results/`（续跑）`logs/`（日志） | —（gitignore） | 结论类 md 躺进 `results/`（第三轮迁出 8 份） |
| 归档（不删只归） | `attic/<主题>_<YYYYMMDD>/` | S12（下架不复活） | 根目录/`tools/` 废件直接删 |
| tracking 下非区域目录 | 一律 `_` 前缀并登记 `NON_REGION_DIRS` | S13 | 新目录默默出现被当区域读 |

## 2. 命名即分类（`output_report/` 保持平铺的原因与做法）

`output_report/` 现状 ~186 件、0 子目录。**不做物理分区**（第二、三轮 E 项两度决策，本轮维持），
理由：① 文件名前缀已经承载分类信息（区域码 / 主题）；② 物理搬动要同步 20+ 处活文档引用，
断裂风险 > 观感收益；③ 命名已被 S16 棘轮守住，分区不会新增任何约束力。

分类读法（看文件名前缀即可归位）：

| 前缀形态 | 含义 | 例 |
|---|---|---|
| `<REGION>_*.md`（大写区域码） | 区域战役产物 | `DEU_matrix_pool_mining_20261010.md` |
| 主题词 + `_YYYYMMDD` | 跨区/工程主题产物 | `ra_pipeline_stage_audit_20260916.md` |
| `*_ideas.md` / `*_campain.md` | **机器产物**（生成器拼名、同名覆盖，豁免「必须带日期」） | `USA_1_news_sentiment_nlp_ideas.md` |
| `*.json` / `*.csv` / `*.txt` | 数据快照 / 派发记录（同样须日期后缀） | `deu_t4_targets_20261010.json` |

**触发重新考虑物理分区的条件**（与二、三轮一致）：出现「找不到某份报告」的实际投诉，
或单目录文件数突破检索实效（建议阈值 400）。届时优先按区域码分子目录，并用
`git mv` + 引用同步一次性完成，不做渐进搬迁。

## 3. 存量欠债策略

- **棘轮制**：存量违规登记 `tools/audit_structure_baseline.json`（S16 键 `s16_naming_violations`，当前 40 条）
  → WARN 可见不阻塞；**新增违规 → FAIL 阻断提交**。
- **触碰即改**：任何会话改到某个存量违规文件时，顺手按 §8.13 改名并从基线移出（棘轮收紧）。
  不做批量回改（引用同步成本高、收益低）。

## 4. 闸门映射（哪条规矩由谁守）

| 规矩 | 闸 | 语义 |
|---|---|---|
| 报告命名（ASCII / 无杠 / 日期后缀 / 人工报告必有日期） | S16 主检查 | 跟踪件新增违规 FAIL；存量 WARN |
| 命名违规在 `git add` 前隐形 | S16 未跟踪预检 | 在途件 WARN（写盘即见） |
| `output_report/` 混入 `.py` | S16 规则⑤（2026-10-10） | 跟踪件 FAIL / 在途件 WARN |
| `reports/` 混入 `.py` | S5（证据脚本按 `S5_EXEMPT_PREFIXES` 登记豁免） | WARN |
| 根目录散件 | S7 白名单 | FAIL（扫磁盘，不看 git 状态） |
| skill 教出违规路径（指令源） | `tests/unit/07_docs_skills/test_skill_no_hyphenated_report_paths.py` | pytest 断言 |

## 5. 例外登记流程

发现「看似违规、实为既定约定」的命名（先例：`campain` 拼写、`*_ideas.md` 机器产物）：
**先查生成/校验代码与「非笔误」声明**（§8.5 纪律），确认后按闸的机制登记
（S16 → `S16_MACHINE_SUFFIXES` 或基线；S5 → `S5_EXEMPT_PREFIXES`；doc_path_refs → `--update-baseline`），
登记处必须写明理由。禁止静默放行、禁止改测试迁就。

---

*维护：本文随 §8.13 / audit_structure 的规则变更同步更新；改 S16/S5/S7 时检查 §4 映射表。*