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

## 新脚本一览

| 脚本 | 对应优化 | 用途 |
|---|---|---|
| `kor_ledger.py` | M17 | 台账统一 CLI：原子写 + utf-8-sig + .bak 备份 + 写时重读合并（防并行覆盖）。`keys/get/set/mark-dead/add-wave/set-verdict/submit-ready/backup` |
| `scan_fields.py` | M3/M4 | 统一字段扫描：直连 get_datafields 落 typed catalog（含字段级 type），取代 kor_scan_fields*/scan_aieq* |
| `score_datasets.py` | M1/M2 | 数据集自动评分（排除台账死数据集）+ 探针电池接线（--probe-plan 生成 / --probe-score 三灯判定） |
| `gate.py` | M4/M7/M9/M10/M11 | 统一闸门：import verifier（无子进程）、白名单按 dataset 自动派生、字段级类型数据驱动、毒模式拦截、结果缓存 |
| `metrics_cache.py` | M12 | 指标读穿缓存 + 单进程单登录；CLI 兼容 kor_fetch_metrics 输出 |
| `review_wave.py` | M15/M16 | 通用评审：消费指标缓存、集中阈值、near 池墙面诊断（CW/2Y/…）、--write-ledger 回写台账 |
| `build_wave.py` | M6/M8 | 统一选波：全历史去重、算子树分桶（根>次节点）、骨架配给（linear_mix≤50%）、near-miss 字段加权、波内字段去重 |
| `diversity_audit.py` | M18 | 多样性审计累积进台账 diversity_history（趋势可观测） |
| `kor_pipeline.py` | B/M13/M14 | 端到端编排：gate→submit→poll→review→ledger，checkpoint 断点续跑；`quota` 子命令（修正 earliest_release 算法） |

## 既有脚本补丁（向后兼容）

- `kor_fetch_metrics.py`：+ 指标读穿缓存（`KOR_NO_CACHE=1` 或 `--refresh` 回源）；multisim 分支复用单登录。
- `kor_poll_pipeline.py`：`--wait N` 改为轮询循环（指数退避 ≤120s，`--timeout` 总超时，progress 60min 无变化熔断 STALLED）；单登录；ERROR 分支取全量 child（原 [:8] 截断）。

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

# 5. 端到端（带续跑+配额闸）
$PY kor_pipeline.py quota
$PY kor_pipeline.py run --file candidates/kor_wave36A_exprs.json --dataset behavioral_signals --wave 36A --submit --review --write-ledger

# 6. 复盘
$PY diversity_audit.py
$PY kor_ledger.py mark-dead xxx --reason "..."
```

## 纪律

- 旧 `record_*.py`/`review_wave1/3/5.py`/`kor_scan_fields*.py`/`scan_aieq*.py`/`validate_wave*.py`/`batch_validate_kor.py` 全部冻结，新工作一律走新链。
- `kor_preflight_check.py` 保留为历史参考；其 verifier 指向 `.qoder-cn` 的路径缺陷由 `gate.py` 修正（`.workbuddy` 优先 + `WQ_VALIDATOR_DIR` 环境变量）。
- `_tmp_*` 探针属并行会话产物，待其确认后清理（M19 暂缓执行）。
