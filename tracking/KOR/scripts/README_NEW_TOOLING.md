# KOR 战役新工具链（2026-08-15 落地）

> 来源：`KOR挖掘优化全面方案_复核版.md` §四 路线图（M1–M19）的工程落地。
> 原则：本地缓存驱动、可断点续跑、配额感知、原子写、无外部 IDE 会话依赖。

> **迁移预告（2026-08-15）**：本目录脚本已抽象为通用引擎 skill **`wq-brain-campaign-toolkit`**
> （`C:\Users\MENGTAO\.workbuddy\skills\wq-brain-campaign-toolkit\scripts\`，region 参数化）。
> 本目录脚本保留为 **KOR 专用历史实现**（已验证、可直接运行），新区域战役请直接用 toolkit
> （`--campaign-dir <DIR>` 指向任意 tracking/<REGION>/）；本轮不切换本目录脚本（Phase A 验证通过，
> 是否转薄 wrapper 由用户另行决定）。平台级约束（poison_patterns）单一事实源已移至 toolkit
> `config/platform_constraints.json`，KOR `kor_generation_constraints.json` 仅保留区域级数据。

## 目录结构

```
tracking/KOR/
  config/
    thresholds.json     # 集中阈值（评审/快扫/探针三灯/硬闸/数据集体检）
    settings.json       # 战役固定仿真设置 + 批次大小 + 单批在飞规则
  reference/
    kor_generation_constraints.json   # 生成约束：未探索算子/骨架配给/毒模式（实测生成）
    kor_dataset_ranking.json          # score_datasets.py 输出（192 数据集评分排序）
    kor_<dataset>_fields.json         # scan_fields.py 输出的 typed catalog
  cache/
    metrics/<alpha_id>.json   # 指标读穿缓存（M12）
    gate_cache.json           # 闸门结果缓存
  scripts/  （新增 9 个，见下）
```

## 新脚本一览（2026-09-01 清理后现状）

**活跃链 = v2 增强链**（战役脚本唯一权威实现在 `wq-brain-campaign-toolkit`；本目录为 KOR 专用 v2 扩展，含纪律监控）：

| 脚本 | 用途 |
|---|---|
| `kor_pipeline_v2.py` | **v2 端到端编排**：v1 基础上集成战役纪律执行器 + 纪律监控器 + 波次规划器；gate→submit→poll→review→ledger，checkpoint 断点续跑 |
| `wave_planner.py` | 波次规划器（消费 campaign_discipline 决策） |
| `review_wave_v2.py` | v2 评审：walls 诊断 + 纪律评估 + 台账回写 |
| `campaign_discipline.py` | 战役纪律执行器（数据集切换/营救/PROD 深度判停阈值） |
| `discipline_monitor.py` | 纪律监控器（波次/数据集维度统计） |
| `compare_improvement.py` | 改进前后对比 |
| `build_wave.py` | 选波：去重/分桶/骨架配给/near 加权（KOR 本地版；通用版在 toolkit） |
| `gate.py` | KOR 本地闸门（通用版在 toolkit `gate.py`） |
| `kor_fetch_metrics.py` | Api/凭证 + 指标拉取（v2 链复用） |
| `kor_ledger.py` | 台账统一 CLI：原子写 + .bak 备份 + 写时重读合并 |
| `metrics_cache.py` | 指标读穿缓存 + 单进程单登录 |

**2026-10-15 从 `Claude/skills/wq-brain-ra-kor/scripts/` 迁入的 3 个分析脚本**（原先只在技能目录里、
且从未入库；技能目录是 `sync_skills.py` 的同步面，放脚本等于给每个安装位复制一份**跑不通**的副本 ——
它们读的是 `Claude/skills/.../template_families.json` 与 `tracking/KOR/reference/*.json`，只有仓库根下有）：

| 脚本 | 用途 | 调用方 |
|---|---|---|
| `kor_s0_scan.py` | S0 选集：给 KOR/TOP600 全部数据集打分排序，排除已点亮（≥3 提交）与已判死者，产白名单 `<repo>/logs/_kor_s0_whitelist.json`。⚠ 内置 `DS` 清单是 2026-10-15 的 `get_datasets` 快照，换轮先重拉 | `references/_dataset-scan-sop.md`、`references/_workflow-pipeline.md` |
| `kor_pool_rank.py` | 候选池排序：吃 `get_user_alphas` 落盘 dump，按 `failed_ra_count` 再按 sharpe 排，输出「失败闸签名」聚类。只读文件，不发请求、不占配额 | `references/_dataset-scan-sop.md` |
| `scan_diversity.py` | 族驱动扫描（防「模板单一」）：`--build <field> [--all-families]` 按 9 族骨架生成网格；`--audit <batch.txt>` 对手写批次跑三闸（族≥2 / 未用或 force 算子≥2 / 单条算子<10）。**不落库** | `references/_probe-sop.md` 第 1.5 步 |

⚠ **`scan_diversity.py` 与 toolkit 的 `diversity_audit.py` 不是重复实现**（2026-10-15 核过；上一轮清理
把 `diversity_audit.py` 的 KOR 副本归档进 `archive/` 是对的，但别顺手把本脚本也当副本清掉）：
`diversity_audit.py` 吃**战役目录的 wave 产物**、写台账并产出 `next_round_injections`（gate.py 闸 6 消费的契约）；
`scan_diversity.py` 吃**手写批次文本**、只往 stdout 打三闸判定，是发批前自查。输入、输出、消费方三处都不同。

**仓库根解析（本目录新脚本一律照此写）**：`from _repo_path import REPO`（`_repo_path.py`，2026-10-15 新增）。
判据 = 向上探测到同时含 `pyproject.toml` 与 `src/wqb/` 的目录，优先用已安装的 `wqb.paths`。
**不要**再写 `parents[N]` / `dirname(dirname(...))` —— 本目录已有 **3 个文件因此指错**（2026-10-15 实测）：
`kor_ledger_write.py:11`、`kor_spre_read.py:6` 的 `parents[1] / "src"` 解析成 `tracking/KOR/src`，
`_kor_s6_writeback.py:15` 的 `parents[1]` 解析成 `tracking/KOR` —— 都少两层。
**这类错不报错**：往 `sys.path` 塞一个不存在的路径是静默 no-op，`import wqb` 靠 pip 的 editable 安装
救回来就一切如常，换台机器或换个 cwd 才 ImportError。
正确写法本目录已有先例：`kor_opportunity_scan.py:32-35`（向上探测双标记，注释写明了为什么不用 `parents[N]`）；
`preflight.py:11` 的 `parents[3]` 数值上对，但层数一变就错，属同一类债。
存量按 §8.13「每次实际移动该文件时顺手换掉」处理，本轮只改迁入的 3 个。

**已归档（2026-09-01 移入 `archive/`，非活跃勿用）**：v1 旧链 `kor_pipeline.py` / `kor_poll_pipeline.py` / `review_wave.py`；与 toolkit 重复的历史副本 `scan_fields.py` / `score_datasets.py` / `diversity_audit.py`；一次性探针与散件 `kor_preflight_check.py` / `batch_validate_kor.py` / `select_wave1.py` / `validate_wave2v2.py` / `validate_wave3.py` / `scan_whitelists.py` / `scan_dl_riskfree.py` / `probe_*.py` / `extract_p32.py` / `fetch_ac_fields.py` / `filter_ac.py` / `_gen_other455_catalog.py` / `_inspect_fail_p*.py` / `_q_kor_registry.py` / `_replay_*.py`。scan/评分/多样性等通用能力一律走 toolkit（`--campaign-dir tracking/KOR`）。

## 既有脚本补丁（向后兼容）

- `kor_fetch_metrics.py`：+ 指标读穿缓存（`KOR_NO_CACHE=1` 或 `--refresh` 回源）；multisim 分支复用单登录。
- 旧 `kor_poll_pipeline.py`（已归档）：曾为 `--wait N` 轮询循环实现（指数退避 ≤120s、progress 60min 熔断 STALLED、ERROR 全量 child）；其能力已被 `kor_pipeline_v2.py` 内置。

## 典型流程

```bash
PY="/c/Users/MENGTAO/.workbuddy/binaries/python/versions/3.13.12/python.exe"
cd tracking/KOR/scripts

# 1. 数据集发现（体检+评分+排除死路）
$PY score_datasets.py

# 2. 字段收割（typed catalog）
$PY scan_fields.py --dataset behavioral_signals

# 3. 探针预筛（两段式：先 Stage A 评分，非 EARLY RED 再跑 Stage B）
$PY score_datasets.py --probe-plan behavioral_signals
#   ... 提交 candidates/probe_behavioral_signals_exprs.json 的 stageA.batches ...
$PY score_datasets.py --probe-score <multisim_id> --stage A   # EARLY RED 即省 Stage B 3 批
$PY score_datasets.py --probe-score <multisim_id> --dataset behavioral_signals --mark-dead
#   三灯 v2：联合评估最强探针 + 广度 + fitness/rn + CW 罚分 + tvr 结构性墙检出
#   （权重/阈值在 config/thresholds.json 的 probe_scoring_v2；--from-json 支持离线校准）

# 4. 生成 → 选波 → 过闸
$PY build_wave.py --file candidates/new_exprs.json --wave 36A
$PY gate.py --dataset behavioral_signals --file candidates/kor_wave36A_exprs.json

# 5. 端到端（带续跑+配额闸；v2 增强链）
$PY kor_pipeline_v2.py run --file candidates/kor_wave36A_exprs.json --dataset behavioral_signals --wave 36A --submit --review

# 6. 复盘（多样性审计走 toolkit）
$PY "C:/Users/MENGTAO/.qoder-cn/skills/wq-brain-campaign-toolkit/scripts/diversity_audit.py" --campaign-dir tracking/KOR
$PY kor_ledger.py mark-dead xxx --reason "..."
```

## 纪律

- 旧 `record_*.py`/`review_wave1/3/5.py`/`kor_scan_fields*.py`/`scan_aieq*.py`/`validate_wave*.py`/`batch_validate_kor.py` 全部冻结，新工作一律走新链。
- 2026-09-01 清理：v1 旧链、toolkit 重复副本、一次性探针共 26 个脚本已移入 `archive/`（见上「已归档」清单）。
- scan/评分/多样性等通用能力一律走 toolkit（`--campaign-dir tracking/KOR`）；本目录只保留 KOR 专用 v2 扩展。
- `_tmp_*` 探针属并行会话产物，待其确认后清理（M19 暂缓执行）。
