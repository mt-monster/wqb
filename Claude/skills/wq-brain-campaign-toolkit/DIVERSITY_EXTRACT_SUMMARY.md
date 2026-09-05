# 单数据集多样性榨取深度集成方案总结

## 核心价值

本方案通过深度集成现有系统，实现了**单数据集多样性榨取**的完整自动化流程，解决了以下核心问题：

1. **避免重复造轮子**：复用现有 `diversity_enhancer.py` 的算子配额管理、结构变异引擎、多样性监控等核心组件
2. **系统性榨取**：通过 L1（字段多样性）→ L2（算子结构多样性）→ L3（参数空间多样性）三轮榨取，最大化单数据集的多样性产出
3. **数据驱动决策**：基于 PPAC 矩阵和结构多样性指标，评估是否继续榨取或进入多数据集阶段
4. **完整自动化**：从数据集审计、分轮次生成、PPAC 矩阵计算到效果评估的完整自动化流程

## 与现有系统的关系

### 复用组件

| 组件 | 文件 | 复用方式 |
|------|------|---------|
| 算子配额管理 | `src/wqb/expression/diversity_enhancer.py` | `OperatorQuotaManager` |
| 结构变异引擎 | `src/wqb/expression/diversity_enhancer.py` | `StructuralMutationEngine` |
| 多样性监控 | `src/wqb/expression/diversity_enhancer.py` | `DiversityMonitor` |
| 骨架配给 | `scripts/build_wave.py` | `skeleton_quota` |
| 算子树分桶 | `scripts/build_wave.py` | `bucket_key` |
| 多样性审计 | `scripts/diversity_audit.py` | 算子/字段/骨架分布统计 |

### 新增组件

| 组件 | 文件 | 功能 |
|------|------|------|
| 数据集深度审计 | `scripts/_lib/diversity_extractor.py` | 字段分类、算子树分桶、参数空间映射 |
| 分轮次多样性生成 | `scripts/_lib/diversity_extractor.py` | L1/L2/L3 三轮榨取 |
| PPAC 矩阵计算 | `scripts/_lib/diversity_extractor.py` | 基于回测结果计算两两 PPAC |
| 多样性榨取效果评估 | `scripts/_lib/diversity_extractor.py` | 结合结构多样性和 PPAC 多样性 |
| 主脚本 | `scripts/diversity_extract.py` | 完整自动化流程 |
| 测试脚本 | `scripts/test_diversity_extract.py` | 验证整个流程 |

## 使用场景

### 1. 新数据集挖掘

当你选定一个新的数据集时，使用本方案进行系统性榨取：

```bash
# 完整流程（脚本会自动创建不完整的战役目录结构，并自动生成 typed catalog）
$PY $TK/diversity_extract.py --campaign-dir $CD --dataset $DS --rounds 3 --size 8
```

**注意**：脚本会自动创建不完整的战役目录结构，包括：
- 创建必要的目录（config/reference/candidates/reviews/cache）
- 创建默认的 settings.json（如果不存在）
- 创建默认的 thresholds.json（如果不存在）
- 创建默认的 generation_constraints.json（如果不存在）
- 自动生成 typed catalog（如果不存在）

**完全自动化，无需手动执行任何命令**。

### 2. 单数据集深度挖掘

当你需要深度挖掘单个数据集的多样性时，使用本方案进行多轮榨取：

```bash
# 增加轮次
$PY $TK/diversity_extract.py --campaign-dir $CD --dataset $DS --rounds 5 --size 8
```

### 3. 多数据集阶段决策

当你需要评估是否进入多数据集阶段时，使用本方案进行效果评估：

```bash
# 查看评估报告
cat $CD/reviews/<region>_diversity_evaluation.json
```

### 4. 调试和优化

当你需要调试和优化生成策略时，使用分步执行：

```bash
# Step 1: 数据集深度审计
$PY $TK/diversity_extract.py --campaign-dir $CD --dataset $DS --skip-generation --skip-ppac --skip-evaluation

# Step 2: 分轮次多样性生成
$PY $TK/diversity_extract.py --campaign-dir $CD --dataset $DS --skip-audit --skip-ppac --skip-evaluation

# Step 3: PPAC 矩阵计算
$PY $TK/diversity_extract.py --campaign-dir $CD --dataset $DS --skip-audit --skip-generation --skip-evaluation

# Step 4: 多样性榨取效果评估
$PY $TK/diversity_extract.py --campaign-dir $CD --dataset $DS --skip-audit --skip-generation --skip-ppac
```

## 决策逻辑

根据评估报告的 `evaluation.recommendation` 字段：

| 推荐 | 条件 | 行动 |
|------|------|------|
| **enter_multi_dataset** | 总表达式 ≥15 且低 PPAC 比例 ≥0.7 且新颖度 ≥0.8 | 进入多数据集阶段 |
| **continue_extraction** | 总表达式 ≥10 且低 PPAC 比例 ≥0.6 | 继续榨取 1-2 轮 |
| **adjust_strategy** | 总表达式 <5 | 调整生成策略或更换数据集 |

## 与 wq-brain-ra-pipeline 的集成

### S2-D 阶段（新增）

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

### 决策点

- 如果 S2-D 评估结果为 **enter_multi_dataset**，则进入多数据集阶段（选择下一个数据集，重复 S2-D）
- 如果 S2-D 评估结果为 **continue_extraction**，则继续榨取当前数据集（增加轮次或调整策略）
- 如果 S2-D 评估结果为 **adjust_strategy**，则调整生成策略或更换数据集

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

**核心价值**：
- **避免重复造轮子**：复用现有系统的核心组件
- **系统性榨取**：L1/L2/L3 三轮榨取，最大化多样性产出
- **数据驱动决策**：基于 PPAC 矩阵和结构多样性指标，评估是否继续榨取或进入多数据集阶段
- **完整自动化**：从数据集审计、分轮次生成、PPAC 矩阵计算到效果评估的完整自动化流程

**使用场景**：
- 新数据集挖掘
- 单数据集深度挖掘
- 多数据集阶段决策
- 调试和优化

**决策逻辑**：
- **enter_multi_dataset**：进入多数据集阶段
- **continue_extraction**：继续榨取 1-2 轮
- **adjust_strategy**：调整生成策略或更换数据集