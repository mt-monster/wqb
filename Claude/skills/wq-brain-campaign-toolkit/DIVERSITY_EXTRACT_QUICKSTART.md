# 单数据集多样性榨取快速开始指南

## 前置条件

1. **战役目录结构完整**（脚本会自动创建不完整的目录结构）：
   ```
   tracking/<REGION>/
   ├── config/
   │   ├── settings.json
   │   └── thresholds.json
   ├── reference/
   │   └── <region>_<dataset>_fields.json  # typed catalog（脚本会自动生成）
   ├── candidates/
   ├── reviews/
   └── cache/
   ```

2. **typed catalog**（脚本会自动生成，如果不存在）：
   - 脚本会自动调用 `scan_fields.py` 生成 typed catalog
   - 无需手动执行任何命令

**注意**：脚本会自动创建不完整的战役目录结构，包括：
- 创建必要的目录（config/reference/candidates/reviews/cache）
- 创建默认的 settings.json（如果不存在）
- 创建默认的 thresholds.json（如果不存在）
- 创建默认的 generation_constraints.json（如果不存在）
- 自动生成 typed catalog（如果不存在）

**完全自动化，无需手动执行任何命令**。

## 快速开始

### 1. 完整流程（推荐）

```bash
PY=$WQ_PY
TK=C:/Users/MENGTAO/.qoder-cn/skills/wq-brain-campaign-toolkit/scripts
CD=<CAMPAIGN_DIR>  # 如 tracking/USA
DS=<dataset>       # 如 fundamental6

# 执行完整流程（审计 → 生成 → PPAC → 评估）
$PY $TK/diversity_extract.py --campaign-dir $CD --dataset $DS --rounds 3 --size 8
```

### 2. 集成到 wq-brain-ra-pipeline 编排器（新增）

```bash
# 执行完整流程并集成到 wq-brain-ra-pipeline 编排器
$PY $TK/diversity_extract.py --campaign-dir $CD --dataset $DS --rounds 3 --size 8 --integrate-pipeline
```

### 3. 分步执行（调试用）

```bash
# Step 1: 数据集深度审计
$PY $TK/diversity_extract.py --campaign-dir $CD --dataset $DS --rounds 3 --size 8 --skip-generation --skip-ppac --skip-evaluation

# Step 2: 分轮次多样性生成（使用已有审计报告）
$PY $TK/diversity_extract.py --campaign-dir $CD --dataset $DS --rounds 3 --size 8 --skip-audit --skip-ppac --skip-evaluation

# Step 3: PPAC 矩阵计算（使用已有表达式）
$PY $TK/diversity_extract.py --campaign-dir $CD --dataset $DS --rounds 3 --size 8 --skip-audit --skip-generation --skip-evaluation

# Step 4: 多样性榨取效果评估（使用已有 PPAC 矩阵）
$PY $TK/diversity_extract.py --campaign-dir $CD --dataset $DS --rounds 3 --size 8 --skip-audit --skip-generation --skip-ppac
```

### 4. 测试流程

```bash
# 运行测试脚本
$PY $TK/test_diversity_extract.py --campaign-dir $CD --dataset $DS --rounds 3 --size 8
```

## 输出文件

执行完成后，会生成以下文件：

```
tracking/<REGION>/
├── reference/
│   └── <region>_<dataset>_diversity_potential.json  # 多样性潜力审计报告
├── candidates/
│   ├── <region>_waveD01_exprs.json  # L1 字段多样性
│   ├── <region>_waveD02_exprs.json  # L2 算子结构多样性
│   └── <region>_waveD03_exprs.json  # L3 参数空间多样性
└── reviews/
    ├── <region>_diversity_matrix.json       # PPAC 矩阵
    └── <region>_diversity_evaluation.json   # 多样性榨取效果评估
```

## 查看结果

### 1. 查看审计报告

```bash
cat $CD/reference/<region>_<dataset>_diversity_potential.json
```

### 2. 查看 PPAC 矩阵

```bash
cat $CD/reviews/<region>_diversity_matrix.json
```

### 3. 查看评估报告

```bash
cat $CD/reviews/<region>_diversity_evaluation.json
```

## 决策逻辑

根据评估报告的 `evaluation.recommendation` 字段：

- **enter_multi_dataset**：单数据集多样性榨取充分，建议进入多数据集阶段
- **continue_extraction**：多样性榨取效果良好，建议继续榨取 1-2 轮
- **adjust_strategy**：多样性榨取效果不佳，建议调整生成策略或更换数据集

## 下一步

### 1. 进入多数据集阶段

如果评估结果为 **enter_multi_dataset**，则选择下一个数据集，重复上述流程：

```bash
# 选择下一个数据集
DS2=<dataset2>  # 如 analyst4

# 执行完整流程
$PY $TK/diversity_extract.py --campaign-dir $CD --dataset $DS2 --rounds 3 --size 8
```

### 2. 继续榨取当前数据集

如果评估结果为 **continue_extraction**，则增加轮次或调整策略：

```bash
# 增加轮次
$PY $TK/diversity_extract.py --campaign-dir $CD --dataset $DS --rounds 5 --size 8 --skip-audit
```

### 3. 调整生成策略

如果评估结果为 **adjust_strategy**，则调整生成策略或更换数据集：

```bash
# 更换数据集
DS3=<dataset3>  # 如 pricevolume

# 执行完整流程
$PY $TK/diversity_extract.py --campaign-dir $CD --dataset $DS3 --rounds 3 --size 8
```

## 常见问题

### 1. typed catalog 不存在

**问题**：`[WARN] typed catalog 不存在: ...`

**解决**：先运行 `scan_fields.py` 生成 catalog：
```bash
$PY $TK/scan_fields.py --campaign-dir $CD --dataset $DS
```

### 2. 审计报告不存在

**问题**：`[diversity_extract] 审计报告不存在，无法跳过审计`

**解决**：不要使用 `--skip-audit`，让流程自动执行审计。

### 3. 表达式文件不存在

**问题**：`[diversity_extract] 没有可用的表达式，流程终止`

**解决**：不要使用 `--skip-generation`，让流程自动生成表达式。

### 4. PPAC 矩阵不存在

**问题**：`[diversity_extract] PPAC 矩阵不存在，使用默认值`

**解决**：不要使用 `--skip-ppac`，让流程自动计算 PPAC 矩阵。

## 总结

本快速开始指南帮助你立即使用单数据集多样性榨取深度集成方案。通过完整流程或分步执行，你可以快速榨取单数据集的多样性，为后续多数据集阶段提供高质量的多样性基础。