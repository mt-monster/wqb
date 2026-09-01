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
