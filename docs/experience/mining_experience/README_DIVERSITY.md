# 多样性增强系统使用指南

## 概述

多样性增强系统是为了解决 alpha 表达式生成中的操作符探索率不足和模板骨架多样性不够的问题而设计的。系统提供了完整的解决方案，包括：

1. **算子配额管理** - 强制算子轮换，确保各类算子得到充分探索
2. **结构变异引擎** - 通过多种变异策略增强模板骨架多样性
3. **多样性监控** - 实时监控多样性指标，提供改进建议
4. **自适应调整** - 根据多样性指标自动调整生成策略

## 核心组件

### 1. diversity_enhancer.py
核心增强引擎，包含：
- `OperatorQuotaManager`: 算子配额管理
- `StructuralMutationEngine`: 结构变异引擎
- `DiversityMonitor`: 多样性监控器
- `DiversityEnhancer`: 主增强器类

### 2. gen_diverse_expressions.py
带多样性增强的表达式生成器，集成到现有的启发式生成系统中。

### 3. batch_diversity_processor.py
批量处理和监控系统，用于：
- 批量处理现有表达式文件
- 生成多样性趋势报告
- 自适应策略调整

### 4. quick_start_diversity.py
快速启动脚本，提供简单的命令行接口。

## 快速开始

### 安装依赖
```bash
pip install matplotlib pandas  # 用于报告生成
```

### 快速生成多样性表达式
```bash
python quick_start_diversity.py generate --count 30 --region USA --universe TOP3000
```

### 分析现有表达式多样性
```bash
python quick_start_diversity.py analyze tracking/USA/batch01.json
```

### 增强现有表达式文件
```bash
python quick_start_diversity.py enhance input.json -o output.json
```

### 运行完整监控周期
```bash
python quick_start_diversity.py monitor --tracking-dir tracking
```

## 高级用法

### 使用 Python API

```python
from wqb.expression.diversity_enhancer import DiversityEnhancer, enhance_expressions

# 创建增强器
enhancer = DiversityEnhancer()

# 增强表达式列表
original_exprs = ["rank(close)", "ts_mean(volume, 20)"]
enhanced_exprs = enhancer.enhance_diversity(original_exprs, target_count=10)

# 获取多样性报告
report = enhancer.get_diversity_report()
print(f"算子熵: {report['current_metrics']['operator_entropy']}")
```

### 自定义配置

编辑 `diversity_config.json` 来自定义：
- 算子配额比例
- 变异策略参数
- 多样性阈值
- 监控设置

### 集成到现有生成器

```python
from gen_diverse_expressions import DiverseExpressionGenerator

generator = DiverseExpressionGenerator(region="USA", universe="TOP3000")
results = generator.generate_with_diversity(
    fields=["close", "volume", "returns"],
    count=50,
    diversity_weight=0.4  # 多样性权重
)
```

## 多样性指标说明

### 算子熵 (Operator Entropy)
- 衡量算子使用的多样性
- 理想值: > 2.0
- 低值表示算子使用过于集中

### 覆盖率 (Coverage Rate)
- 已使用算子占所有可用算子的比例
- 理想值: > 50%
- 低值表示很多算子未被探索

### 新颖度 (Novelty Score)
- 唯一表达式占总表达式的比例
- 理想值: > 80%
- 低值表示表达式重复度高

### 结构相似度 (Structural Similarity)
- 表达式骨架的相似程度
- 理想值: < 70%
- 高值表示模板过于单一

## 变异策略

系统支持 8 种结构变异策略：

1. **swap_branches** - 交换分支
2. **insert_layer** - 插入层
3. **delete_layer** - 删除层
4. **change_operator** - 改变算子
5. **reorder_sequence** - 重排序列
6. **add_condition** - 添加条件
7. **change_window** - 改变窗口
8. **add_transform** - 添加变换

## 自适应调整

系统会根据历史多样性指标自动调整：
- 变异率 (0.3 - 0.8)
- 探索率 (0.2 - 0.4)
- 配额强制开关
- 重点关注领域

## 监控和报告

### 实时监控
每次生成或增强表达式时，系统会自动计算多样性指标。

### 趋势报告
运行 `batch_diversity_processor.py --report` 生成趋势报告，包括：
- 多样性指标趋势图
- 骨架分布分析
- 改进建议

### 状态持久化
系统会保存算子使用历史到 `diversity_state_{region}_{universe}.json`，用于跨会话的连续性。

## 测试

运行集成测试：
```bash
python test_diversity_system.py
```

## 最佳实践

1. **定期监控**: 每 10 轮生成后运行一次多样性分析
2. **平衡探索与利用**: 多样性权重建议设置为 0.3-0.4
3. **关注建议**: 系统会根据指标自动生成改进建议
4. **保持历史**: 定期备份多样性历史数据，用于长期趋势分析
5. **逐步调整**: 不要一次性改变太多参数，观察效果后再调整

## 故障排除

### 问题: 算子熵持续偏低
解决: 增加变异率，强制使用配额管理器

### 问题: 表达式重复度过高
解决: 增加随机注入率，使用更多结构变异

### 问题: 某些算子类别未被使用
解决: 检查配额配置，确保该类别有足够的配额比例

## 贡献

欢迎提交改进建议和新的变异策略！
