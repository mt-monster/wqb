# 单数据集多样性榨取深度集成方案

## 概述

本方案将"单数据集多样性榨取"深度集成到 `wq-brain-campaign-toolkit` 中，实现从数据集审计、分轮次生成、PPAC 矩阵计算到效果评估的完整自动化流程。

## 核心思想

**先榨取单数据集的多样性，再进入多数据集阶段**。通过 L1（字段多样性）→ L2（算子结构多样性）→ L3（参数空间多样性）三轮榨取，最大化单数据集的多样性产出。

## 架构设计

### 1. 核心组件

| 组件 | 文件 | 功能 |
|------|------|------|
| 主脚本 | `scripts/diversity_extract.py` | 单数据集多样性榨取完整流程 |
| 核心逻辑库 | `scripts/_lib/diversity_extractor.py` | 字段分类、分轮次生成、PPAC 矩阵、效果评估 |
| 测试脚本 | `scripts/test_diversity_extract.py` | 验证整个流程 |
| 子命令注册 | `scripts/campaign.py` | 注册 `diversity-extract` 子命令 |

### 2. 与现有系统的关系

- **复用** `diversity_enhancer.py` 的算子配额管理（OperatorQuotaManager）
- **复用** `diversity_enhancer.py` 的结构变异引擎（StructuralMutationEngine）
- **复用** `diversity_enhancer.py` 的多样性监控（DiversityMonitor）
- **复用** `build_wave.py` 的骨架配给和算子树分桶
- **复用** `diversity_audit.py` 的算子/字段/骨架分布统计

### 3. 新增功能

- **数据集深度审计**：分析字段经济含义分组、算子树分桶、参数空间映射
- **分轮次多样性生成**：L1（字段多样性）→ L2（算子结构多样性）→ L3（参数空间多样性）
- **PPAC 矩阵计算**：基于回测结果计算两两 PPAC，更新多样性矩阵
- **多样性榨取效果评估**：结合结构多样性和 PPAC 多样性，评估是否继续榨取或进入多数据集阶段

## 使用流程

### 1. 前置条件

- 战役目录结构完整（脚本会自动创建不完整的目录结构）
- typed catalog（脚本会自动生成，如果不存在）

**注意**：脚本会自动创建不完整的战役目录结构，包括：
- 创建必要的目录（config/reference/candidates/reviews/cache）
- 创建默认的 settings.json（如果不存在）
- 创建默认的 thresholds.json（如果不存在）
- 创建默认的 generation_constraints.json（如果不存在）
- 自动生成 typed catalog（如果不存在）

**完全自动化，无需手动执行任何命令**。

### 2. 执行命令

```bash
PY=$WQ_PY
TK=C:/Users/MENGTAO/.qoder-cn/skills/wq-brain-campaign-toolkit/scripts
CD=<CAMPAIGN_DIR>  # 如 tracking/USA

# 完整流程（审计 → 生成 → PPAC → 评估）
$PY $TK/diversity_extract.py --campaign-dir $CD --dataset <ds> --rounds 3 --size 8

# 跳过审计（使用已有报告）
$PY $TK/diversity_extract.py --campaign-dir $CD --dataset <ds> --skip-audit

# 跳过生成（使用已有表达式）
$PY $TK/diversity_extract.py --campaign-dir $CD --dataset <ds> --skip-generation

# 跳过 PPAC 计算
$PY $TK/diversity_extract.py --campaign-dir $CD --dataset <ds> --skip-ppac

# 跳过效果评估
$PY $TK/diversity_extract.py --campaign-dir $CD --dataset <ds> --skip-evaluation
```

### 3. 输出文件

| 文件 | 路径 | 内容 |
|------|------|------|
| 多样性潜力审计报告 | `reference/<region>_<ds>_diversity_potential.json` | 字段分类、算子树分桶、参数空间映射、多样性得分、推荐轮次 |
| 各轮次表达式 | `candidates/<region>_wave<TAG>_exprs.json` | TAG = D01/D02/D03/... |
| PPAC 矩阵 | `reviews/<region>_diversity_matrix.json` | 两两 PPAC、平均 PPAC、最大 PPAC、低 PPAC 比例 |
| 多样性榨取效果评估 | `reviews/<region>_diversity_evaluation.json` | 结构多样性、PPAC 多样性、评估结论、推荐理由 |

### 4. 决策逻辑

- **enter_multi_dataset**：单数据集多样性榨取充分（总表达式 ≥15 且低 PPAC 比例 ≥0.7 且新颖度 ≥0.8），建议进入多数据集阶段。
- **continue_extraction**：多样性榨取效果良好（总表达式 ≥10 且低 PPAC 比例 ≥0.6），建议继续榨取 1-2 轮。
- **adjust_strategy**：多样性榨取效果不佳（总表达式 <5），建议调整生成策略或更换数据集。

## 与 wq-brain-ra-pipeline 的集成

### 1. S2-D 阶段（新增）

在 `wq-brain-ra-pipeline` 的 S2 阶段后新增 S2-D 阶段：

```
S2: brain-makeSomeGem ──→ *_idea_*.json + final_expressions.json
    ↓
S2-D: diversity_extract.py (单数据集多样性榨取)
    ├─ Step 1: 数据集深度审计 (字段分类+算子树分桶+参数空间映射)
    ├─ Step 2: 分轮次多样性生成 (L1字段/L2算子/L3参数)
    ├─ Step 3: PPAC 矩阵计算 (基于回测结果)
    └─ Step 4: 多样性榨取效果评估 (结构多样性+PPAC关联)
    ↓
S3: brain-simAlphasinBatch-and-track (批量回测)
```

### 2. 决策点

- 如果 S2-D 评估结果为 **enter_multi_dataset**，则进入多数据集阶段（选择下一个数据集，重复 S2-D）
- 如果 S2-D 评估结果为 **continue_extraction**，则继续榨取当前数据集（增加轮次或调整策略）
- 如果 S2-D 评估结果为 **adjust_strategy**，则调整生成策略或更换数据集

## 测试

### 1. 运行测试脚本

```bash
PY=$WQ_PY
TK=C:/Users/MENGTAO/.qoder-cn/skills/wq-brain-campaign-toolkit/scripts
CD=<CAMPAIGN_DIR>  # 如 tracking/USA

$PY $TK/test_diversity_extract.py --campaign-dir $CD --dataset <ds> --rounds 3 --size 8
```

### 2. 验证输出

测试脚本会检查以下文件是否生成：

- ✓ 审计报告：`reference/<region>_<ds>_diversity_potential.json`
- ✓ 表达式文件：`candidates/<region>_wave<TAG>_exprs.json`（TAG = D01/D02/D03/...）
- ✓ PPAC 矩阵：`reviews/<region>_diversity_matrix.json`
- ✓ 评估报告：`reviews/<region>_diversity_evaluation.json`

## 后续优化方向（已落地）

1. **集成 brain-calculate-alpha-selfcorrQuick**：已实现真实 PPAC 计算，通过 `RealPPACCalculator` 类集成 `brain-calculate-alpha-selfcorrQuick` 进行真实 PPAC 计算。

2. **优化字段分类**：已实现基于字段描述和实际数据分布的增强字段分类，通过 `EnhancedFieldClassifier` 类进行更精准的分类。

3. **增强参数空间映射**：已实现基于历史回测结果的动态参数空间映射，通过 `DynamicParamSpaceMapper` 类动态调整参数空间。

4. **集成到 wq-brain-ra-pipeline 编排器**：已实现自动化榨取，通过 `RaPipelineIntegrator` 类集成到 `wq-brain-ra-pipeline` 的日循环编排器中。

### 使用方法

#### 1. 集成 brain-calculate-alpha-selfcorrQuick

```bash
# 自动使用真实 PPAC 计算（无需额外参数）
$PY $TK/diversity_extract.py --campaign-dir $CD --dataset <ds> --rounds 3 --size 8
```

#### 2. 优化字段分类

```bash
# 自动使用增强字段分类（无需额外参数）
$PY $TK/diversity_extract.py --campaign-dir $CD --dataset <ds> --rounds 3 --size 8
```

#### 3. 增强参数空间映射

```bash
# 自动使用动态参数空间映射（无需额外参数）
$PY $TK/diversity_extract.py --campaign-dir $CD --dataset <ds> --rounds 3 --size 8
```

#### 4. 集成到 wq-brain-ra-pipeline 编排器

```bash
# 使用 --integrate-pipeline 参数集成到 wq-brain-ra-pipeline 编排器
$PY $TK/diversity_extract.py --campaign-dir $CD --dataset <ds> --rounds 3 --size 8 --integrate-pipeline
```

## 总结

本方案通过深度集成现有系统，实现了单数据集多样性榨取的完整自动化流程。通过 L1/L2/L3 三轮榨取，最大化单数据集的多样性产出，为后续多数据集阶段提供高质量的多样性基础。