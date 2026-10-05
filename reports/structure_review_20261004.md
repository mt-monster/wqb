# wqb 项目结构复审（2026-10-04）

> 定位：本会话结构治理后的**复审**，取代 `code_structure_survey_20260925.md` 中与目录布局相关的部分
> （那份仍是 P1–P11 **代码结构债**台账，两边不重复列举，见 AGENTS.md §8.4 第 5 项）。
> 全部数字为本次实测；结构类结论按 §8.5 铁律用机器证据核验（`git ls-files` / `check-ignore` /
> token 级引用 / 内容哈希），不用子串 grep 与记忆。
> ⚠ 时间截面：另一个会话在本轮持续写入（`tools/` 顶层 +17、新增 `src/wqb/profiles/`、2 个新 skill、
> `data/` 新增 1 份备份）。下文凡"归属并行会话"者均据此判定，不要当成本会话的回归。

## 一、规模总览

| 目录 | 磁盘 | git 跟踪 | 性质 |
|---|---:|---:|---|
| `tracking/` | 13,080 | 2,582 | 区域战役数据 + 区域脚本 |
| `Claude/skills/` | 517 | 317 | skills 源（+2 个新 skill 未跟踪） |
| `tools/` | 343 | 228 | 工具链（顶层 188 平铺 + 5 子目录） |
| `tests/` | 593 | 201 | 单测（01–10 编号域） |
| `output_report/` | 135 | 132 | 报告唯一出口 |
| `src/wqb/` | 263 | 106 | 规范核心包 |
| `reports/` | 92 | 91 | 人工审计与复盘 |
| `docs/` | 83 | 76 | 长期规范/SOP/速查 |
| `world-quant-brain-mcp/` | 17,699 | 64 | MCP 服务（磁盘大头是 `.venv`） |
| `attic/` | 288 | 23 | 日期化归档包（本次 +6） |
| `logs/` `cache/` `results/` `data/` | 1,761 / 601 / 13 / 4 | 0 | 运行期产物（gitignore） |
| `research-data/` `extensions/` | 319 / 103 | 0 | 外部数据与扩展（本次去重 −102） |
| `selfcorr_quick_out/` | 4 | 0 | **本轮新出现的未声明顶层目录** |

根目录：**16 个文件**（治理前 26）。空目录：**0**（治理前 3）。

## 二、已闭合（相对 2026-09-30 / 10-01 / 10-04 三次治理前状态）

| 问题 | 现在的机器状态 |
|---|---|
| 根目录散件（26 件，含 6 件套子应用 + 事故残留） | S7 白名单守，16 件中 15 件在白名单内 |
| 根目录反复污染（第 5 次） | S7 已在当日抓到复发（`sa_status_*.log`）——从"人记得清"变成"提交时点名" |
| 空目录 / 区域骨架不一致 | S10 转 OK：13 区 × 5 核心子目录齐整；`CHN/JPN results` 空壳已消 |
| `mining/` 工作树空、仍在 git 索引（幽灵） | 已摘索引 + 15 文件从 HEAD 恢复归档 `attic/mining_scripts_20261004/` |
| AGENTS.md 声明不存在的目录（`mining/`、`data_ref/`）、`docs/README.md` 索引幻影 `architecture/` | S9 守"声明即存在"，当前 OK |
| 论坛工作台根/tools 双份**互为超集**分叉 + 模板丢失致每晚自动化连日失败 | 整端归档；S8（根↔子目录同名分叉）+ S12（已下架不得复活）双守，当日已抓 1 次复活 |
| `output_report/` 与 `reports/` 两头分流、reports 无归属判据 | `reports/README.md` 落判据 + v1→v4 谱系入口；`reports/` 散落脚本由 S5 守（当前 OK） |
| WebDataScope 两份逐字节重复（102 件） | 自证后归档重复份；`research-data/` 本体（`op_arity.py` 依赖）未动 |
| MCP 包内混入源码位：`test_*.py` 命名歧义、包根日志、散 md、孤儿 `data/wqb.db` | 2 个改名 `probe_*`；日志入 `logs/`；2 md 入 `docs/`；孤儿库归档 |
| `tracking/reference/` 一次 性脚本堆积（141 件仅 19 入库） | token 级核验 refs=0 后归档 99 件；剩 42 件真参考资料 |
| 仓库根推导层数硬编码扩散 | `src/wqb/paths.py`（层数无关）+ §8.13 禁新增；7 条契约测试 |
| `tools/` 无主题、只长不收敛 | `tools/THEMES.json`（19 主题，171/171 归属）+ S11 顶层冻结；首主题 `tools/code-audit/` 已落地 |
| 入口 `wqb_db_mcp.py` 的静默失效型测试耦合 | `set_db_path()/get_db_path()` + **结果层硬闸**（pytest 下指向生产库即报错），17 处已迁 |

结构守护本身：S1–S12 全量在跑（pre-commit L56 调用，FAIL 即阻断），已验证 S7/S11/S12 **非空过**。

## 三、仍开放（按优先级）

### P0 —— 新增、且当前就在阻断提交（均归属并行会话）

1. **`src/wqb/profiles/`（未跟踪新目录）内含 13 处包内 `sys.path` 自举注入 → S1 FAIL×13**。
   `src/wqb` 已是 `pip install -e .` 的可导入包，包内自举属 §8.4 第 2 条明确"应删"的那类
   （与"外挂 `world-quant-brain-mcp/`、`tools/`"不同，后者是设计内、勿删）。
   治理动作最小：删自举注入，`import wqb.*` 直接可用；验证 `python tools/audit_structure.py --only s1`。
2. **两个新 skill 教加权拼腿未标反例 → 混信号纪律守护红**：
   `Claude/skills/wq-brain-ra-usa/references/shortinterest.md:87`、
   `Claude/skills/wq-brain-ra-mea/references/analyst*.md`（`test_sf_sweeps` 抓）。
   这条不是风格问题：它是闸 5 poison_patterns 在文档侧的镜像，也是用户明令纪律（2026-08-26 /
   09-09 / 09-16 三次重申）。改法：加 `<!-- lint:counterexample -->` 或文件头现行策略横幅。
3. **`tools/` 顶层 171 → 188（+17），其中 10 处硬编码本机盘符（S4 FAIL×10）** +
   根目录又落 1 个 `sa_status_*.log`（S7 FAIL）。一次性脚本应落 `logs/_tmp_*.py` 或
   `tracking/<REGION>/scripts/`（§8.13），不得进 `tools/` 顶层。

### P1 —— 结构债（有判据、无守护或守护未覆盖）

4. **无人守的分叉类：区域脚本复制了 toolkit 引擎。** 实测 `tracking/KOR/scripts/` 有
   `build_wave.py`、`gate.py`、`metrics_cache.py`，`scripts/archive/` 有
   `diversity_audit.py`、`review_wave.py`、`scan_fields.py`、`score_datasets.py`
   —— 与 toolkit 同名但内容已不同。**S6 只横切 `Claude/skills/`，这类不在任何闸内**。
   建议：把 S6 的扫描域扩到 `tracking/*/scripts`（或规定区域不得复制引擎，只能 import toolkit）。
   这是本复审发现的**唯一"守护盲区"**，优先级在命名类之上。
5. **`selfcorr_quick_out/` 顶层未声明目录**（skill `brain-calculate-alpha-selfcorr-quick` 的输出）。
   运行产物应落 `cache/`；否则至少在 AGENTS.md §1 声明（S9 会要求它真实存在）。
6. **命名残余（存量不强制回改，但不得新增）**：`tracking/` 根 5 个 `2026-10-02_xxx.md`
   日期前缀式（§8.13 规定产物用 `_<YYYYMMDD>` 后缀）；活跃树非 ASCII 文件名 14 个
   （`docs/alpha模板.docx`、`docs/tutorials/课件.md`、`tracking/mining/*_A档.md`、
   MCP `docs/workflows/示例工作流_*.md` 等）。
   实测合规度：`reports/` 41 份中 21 紧凑 / 6 ISO 中缀（§8.13 已声明豁免）/ 1 无日期；
   `output_report/` 135 份中 66 紧凑 + 64 无日期（ideas 文件按 `区域_delay_数据集_ideas` 命名，无需日期）。
7. **区域"非核心"子目录仍 13 区各异**：`reviews` 4/13、`scripts` 5/13、`reports` 5/13、
   `ideas` 3/13，`deepexplore`(2)、`ppa`/`ra`/`runs`/`waves` 各 1。核心 5 个已统一。
   待决：`reviews` 建议升核心（`review_wave` 是标准链路一步，落点应当可预测）。
8. **`wqb_db_mcp.py` 115 KB / 2,792 行仍在根。** 拆分已被验证可行（工具面 47=47 逐项一致），
   阻塞是六类耦合，已全部量化并列行号 → 见 [`db_mcp_split_20261004.md`](db_mcp_split_20261004.md)。
9. **`data/` 备份数已到策略上限**：live `wqb.db` 311 MB + 2 份 311 MB 备份，
   `test_retention` 断言 ≤2 → 再产一份即红。需要时跑 `tools/retention.py --apply` 回收最旧。

### P2 —— 可规划、不紧急

10. `tools/` 主题下沉 1/19（其余 18 个主题待建）；配方与耦合清单已入仓。
11. `world-quant-brain-mcp` 根仍有 `create_super_alpha.py`、`super_alpha_tool.py`、
    `browser_setup.py` 可下沉到 `scripts/`（该目录目前只有 1 个模块，近乎空目录）。
12. `logs/` 1,761、`cache/` 601 件：靠 `tools/retention.py` + `tools/clean_logs.py` 滚动，
    阈值未到即不动（勿手工清，`_async_tasks/_slots/_dblock` 在保护名单里）。

## 四、结构上判定为"健康、不要动"的部分

- **四层依赖方向**（S2 OK：`src/` 不引 `tools/`）与 `src/wqb` 分包边界（config/expression/store/
  workflow/research/search/memory/modeb/profiles*）——*前提是 P0-1 修完。
- **S3 的 7 组跨层同名**（`tools/x.py` vs `src/wqb/**/x.py`）：分属脚本与包两套命名空间，
  import 不撞，§8.12 已判定非缺陷，**勿改名**。
- `tests/unit/01_store_db … 10_toolkit_scripts` 编号域 + `TESTS_TOC.md`：导航清晰，保持。
- `attic/` 日期化归档包、`tools/legacy/` 产物归档：约定一致，保持。
- MCP 包根：本轮清理后只剩代码 + 配置 + `main.py` 入口，结构已干净。

## 五、下一步（按性价比）

| 动作 | 成本 | 收益 |
|---|---|---|
| 修 P0-1（删 profiles 包内自举） | 1 文件 | 解除 S1 阻断；守住"核心包不再自举"的既有决策 |
| 修 P0-2（两处 skill 示例标反例） | 2 行 | 恢复混信号纪律守护 |
| 处置 P0-3（17 个顶层脚本 + 根日志归位） | 移动 | 解除 S4/S7/S11 阻断，`tools/` 回到基线 |
| 扩 S6 到 `tracking/*/scripts`（P1-4） | 半小时 | 补上本复审发现的唯一守护盲区 |
| `selfcorr_quick_out/` 改输出到 `cache/`（P1-5） | skill 1 处 + sync | 顶层不再长出未声明目录 |
