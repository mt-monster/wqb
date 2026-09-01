# wq-brain-campaign-toolkit 工具使用率评估（2026-08-31 v2 修正版）

> **v2 修正说明**：v1 扫描仅覆盖 `tracking/`、`mining/`、`tools/`，**漏掉了 toolkit 自身 `scripts/` 目录的内部 import 与 `campaign.py` 的 CLI 子命令分发**，导致误判 4 个工具为「零使用」。v2 补充 toolkit 内部引用扫描，结论已修正。
>
> 数据来源：三个维度——①全工作区文件名引用 ②toolkit `scripts/` 内部 import ③`campaign.py` CLI 子命令分发。

## 使用率分级（修正后）

### 高使用率（核心工具，保留并优先维护）

| 工具 | 工作区引用 | 职责 | 处置 |
|------|-----------|------|------|
| `metrics_cache.py` | 187 | 指标缓存（避免重复拉取） | **保留**（性能关键） |
| `campaign.py` | 153 | 战役 CLI 入口（registry/ledger 幂等写 + 子命令分发） | **保留**（核心入口） |
| `gate.py` | 91 | 5 闸预检 | **保留**（硬闸门） |
| `scan_fields.py` | 20 | typed catalog 字段扫描 | **保留** |
| `pipeline.py` | 16 | 战役编排（checkpoint/七槽填槽） | **保留**（编排核心） |

### 中使用率（保留）

| 工具 | 工作区引用 | 职责 | 处置 |
|------|-----------|------|------|
| `review_wave.py` | 6 | 波次评审 + walls 诊断 | **保留** |
| `score_datasets.py` | 5 | 数据集评分 + 探针 v2 三灯 | **保留** |
| `harvest.py` | 5 | multisim 结果收割入库 | **保留** |
| `build_wave.py` | 3 | 波次构建 | **保留** |
| `diversity_audit.py` | 3 | 多样性审计 | **保留** |
| `check_ledger_sync.py` | 3 | 台账同步校验 | **保留** |

### 内部使用（工作区零引用，但被 toolkit 内部 import / CLI 分发，**必须保留**）

| 工具 | toolkit import | CLI 分发 | 被谁使用 | 处置 |
|------|---------------|---------|---------|------|
| `assemble_priors.py` | 2 | 1 | `build_wave.py`、`gate.py` import + `campaign.py assemble-priors` | **保留**（关键依赖） |
| `signal_classifier.py` | 2 | 0 | toolkit 内部 import | **保留** |
| `composition_validator.py` | 2 | 0 | toolkit 内部 import | **保留** |
| `diversity_extract.py` | 0 | 1 | `campaign.py diversity-extract` 子命令 | **保留** |
| `s2_compliance_mark.py` | 0 | 1 | `campaign.py s2-mark` 子命令 | **保留** |
| `neutralization_sweep.py` | 0 | 0 | `pipeline.py` 兼容其产物（间接） | **保留**（产物兼容） |

### 确认零使用（三维度均为 0，可归档）

以下 **12 个工具** 在工作区引用、toolkit 内部 import、CLI 分发三个维度**全部为 0**，建议归档 `attic/tools_archive/`：

| 工具 | 职责 | 建议处置 |
|------|------|---------|
| `migrate_templates.py` | 模板迁移（一次性） | **归档**（一次性工具） |
| `compose_signals.py` | 信号组合 | 归档（与 build_mix 重叠） |
| `param_opt.py` | 参数优化 | 归档（与 param_matrix 重叠） |
| `ortho_prescreen.py` | 正交预筛 | 归档（与 gate 重叠） |
| `proxy_prescreen.py` | 代理预筛 | 归档（与 gate 重叠） |
| `rescue_checklist.py` | 救援清单 | 归档（文档型） |
| `calibrate_probe.py` | 探针校准 | 归档（与 score_datasets 重叠） |
| `fit_mix_weights.py` | 混合权重拟合 | 归档（与 build_mix 重叠） |
| `build_mix.py` | 混合构建 | 归档（与 compose_signals 重叠） |
| `adhoc.py` | 临时命令 | 归档（交互式入口） |
| `param_matrix.py` | 参数矩阵 | 归档（与 param_opt 重叠） |
| `diversity_slots.py` | 多样性槽位 | 归档（与 diversity_audit 重叠） |

## 关键发现（修正后）

1. **核心 5 工具**（metrics_cache/campaign/gate/scan_fields/pipeline）占工作区引用量 ~85%。
2. **6 个工具工作区零引用但内部使用**（assemble_priors/signal_classifier/composition_validator/diversity_extract/s2_compliance_mark/neutralization_sweep）——v1 误判为零使用，v2 已纠正。**这些必须保留**。
3. **12 个工具确认零使用**（三维度全 0），可安全归档。
4. **功能重叠**：信号组合（compose_signals/build_mix/fit_mix_weights 3 个）、参数优化（param_opt/param_matrix 2 个）、预筛（ortho/proxy_prescreen 2 个）。

## 处置方案（修正后）

### 已执行
- 无（v1 误归档的 18 个文件已全部从 `.box-agent` 副本恢复，import 验证通过）。

### 待用户确认后执行
- **归档 12 个确认零使用工具** → `attic/tools_archive/`（保留 git 历史，可回迁）。
- **保留 6 个内部使用工具**（assemble_priors/signal_classifier/composition_validator/diversity_extract/s2_compliance_mark/neutralization_sweep）。

## 教训（重要）

**工具使用率扫描必须覆盖「工具自身目录的内部引用」**：v1 仅扫描业务目录（tracking/mining/tools），漏掉了 toolkit `scripts/` 内部的跨脚本 import（如 `gate.py` import `assemble_priors`）与 `campaign.py` 的 CLI 子命令分发（如 `diversity-extract`），导致误判。后续评估工具使用率时，扫描范围必须包含工具所在目录自身。

## 备注

- 三维扫描：①工作区文件名（`\b<name>\b`）②toolkit 内部 import（`import <name>`/`from <name>`）③`campaign.py` CLI 分发（`"<name>"` 子命令映射）。
- `test_*.py` 为测试文件，不计入使用率评估。
