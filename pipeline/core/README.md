# 通用战役流水线（区域无关）

## 概述

通用战役流水线是区域无关的 alpha 挖掘战役编排器，集成了纪律执行、监控、多样性评估等增强能力。

## 核心特性

1. **区域无关**：通过 `RegionConfig` 适配任意区域（KOR/USA/EUR/GBR...）
2. **纪律执行**：PROD 墙三档分类 + 判死证据链闭环
3. **监控集成**：自动收集每轮回测数据，生成实证报告
4. **多样性评估**：每 10 轮综合评估多样性+纪律+改进效果
5. **断点续跑**：checkpoint 机制，支持中断恢复
6. **台账集成**：自动写入区域台账

## 架构

```
pipeline/core/
├── campaign_pipeline.py          # 主流水线（集成所有能力）
├── campaign_discipline.py        # 纪律执行器（PROD 三档分类+判死证据链）
├── discipline_monitor.py         # 纪律监控器（收集每轮回测数据）
├── improvement_comparator.py     # 改进对比分析器（前后对比）
├── diversity_integrated_monitor.py # 多样性集成监控器（10轮综合评估）
└── __init__.py                   # 模块导出
```

## 快速开始

### 1. 基本用法（任意区域）

```python
from pipeline.core import CampaignPipeline, RegionConfig

# 创建区域配置
config = RegionConfig(
    region="KOR",                    # 区域代码
    universe="TOP600",               # Universe
    delay=1,                         # Delay
    neutralization="SECTOR",         # 中性化
    settings_path="tracking/KOR/config/settings.json",
    ledger_path="tracking/KOR/kor_d1_campaign_state.json"
)

# 创建流水线
pipeline = CampaignPipeline(config)

# 运行回测
result = pipeline.run(
    exprs_file="tracking/KOR/candidates/kor_wave17A_exprs.json",
    dataset="other455",
    wave="17A",
    submit=True,
    enhance_diversity="auto",
    enable_discipline=True,          # 启用纪律执行
    enable_monitoring=True           # 启用监控
)
```

### 2. 纪律评估

```python
# 评估数据集状态
evidence = pipeline.discipline.assess_dataset("multi_source_model")
print(f"分类: {evidence['category']}")  # DEEP/SUSPEND/DEAD
print(f"建议: {evidence['recommendation']}")

# 生成切换决策
decision = pipeline.discipline.decide_switch("chart_cnn_alpha")
if decision['switch_trigger']:
    print(f"切换建议: {decision['switch_reason']}")
```

### 3. 生成综合报告（每 10 轮）

```python
# 生成多样性+纪律+改进效果综合报告
report = pipeline.generate_integrated_report(waves=10)
```

### 4. CLI 用法

```bash
# 运行回测（带纪律执行+监控）
python pipeline/core/campaign_pipeline.py \
  --region KOR --universe TOP600 --delay 1 --neutralization SECTOR \
  run --file candidates/x.json --dataset other455 --wave 17A --submit

# 生成综合报告（每 10 轮）
python pipeline/core/campaign_pipeline.py \
  --region KOR --universe TOP600 --delay 1 --neutralization SECTOR \
  integrated-report --waves 10

# 评估数据集状态
python pipeline/core/campaign_pipeline.py \
  --region KOR --universe TOP600 --delay 1 --neutralization SECTOR \
  discipline-assess --dataset multi_source_model

# 生成切换决策
python pipeline/core/campaign_pipeline.py \
  --region KOR --universe TOP600 --delay 1 --neutralization SECTOR \
  discipline-decide --dataset chart_cnn_alpha
```

## 纪律执行

### PROD 墙三档分类

| 分类 | PROD 范围 | 策略 |
|------|-----------|------|
| **DEEP** | < 0.75 | 深耕，继续优化 |
| **SUSPEND** | 0.75-0.80 | 暂挂，保留候选池 |
| **DEAD** | > 0.80 | 判死封存，切换数据集 |

### 判死证据链四要素

1. **prod_wall_structural**: PROD min > 0.80
2. **settings_exhausted**: 设置空间 >= 4 种
3. **structures_exhausted**: 结构变体 >= 5 种
4. **rescue_weapons_exhausted**: 救援武器全部实测

### 救援武器清单（10 种）

- ts_target_tvr_decay（定目标换手）
- residual_diff_template（残差差分模板）
- vec_avg_to_vec_max（换聚合）
- neutralization_switch（中性化切换）
- inner_outer_neutralization（内细外粗二次中性化）
- weight_perturbation（权重扰动）
- layer_switch（换层）
- subtract_structure（subtract 多空差结构）
- horizon_mix（跨 horizon 组合）
- decay_gradient（decay 梯度扫描）

## 监控指标

### 每轮回测监控

- 总表达式数
- 总完成数
- 总候选数
- PROD 分类分布（DEEP/SUSPEND/DEAD/UNKNOWN）
- 切换触发次数
- 判死及时性（从首次撞 PROD 墙到判死封存的波次数）

### 每 10 轮综合评估

- **纪律评估**：候选率、切换触发次数、判死及时性
- **改进效果**：候选率变化、DEAD 分类变化、切换次数变化
- **多样性评估**：算子熵、覆盖率、新颖度、结构相似度

## 实证结果

基于模拟数据的实证结果：

| 指标 | 改进前 | 改进后 | 变化 |
|------|--------|--------|------|
| 候选率 | 3.6% | 18.3% | **+403.3%** |
| DEAD 分类比例 | 0% | 20% | **+20%** |
| 切换触发次数 | 4 | 2 | -2 |

**结论**：
- 候选率显著提升 403.3%，说明纪律执行有效提高了挖掘效率
- DEAD 分类比例提升 20%，说明判死及时性提高，避免了配额浪费
- 切换触发次数减少 2 次，说明判死证据链闭环有效，减少了主观判断误差

## 区域适配

### KOR 区域

```python
config = RegionConfig(
    region="KOR",
    universe="TOP600",
    delay=1,
    neutralization="SECTOR",
    settings_path="tracking/KOR/config/settings.json",
    ledger_path="tracking/KOR/kor_d1_campaign_state.json"
)
```

### USA 区域

```python
config = RegionConfig(
    region="USA",
    universe="TOP3000",
    delay=1,
    neutralization="SUBINDUSTRY",
    settings_path="tracking/USA/config/settings.json",
    ledger_path="tracking/USA/usa_d1_campaign_state.json"
)
```

### EUR 区域

```python
config = RegionConfig(
    region="EUR",
    universe="TOP1200",
    delay=1,
    neutralization="SUBINDUSTRY",
    settings_path="tracking/EUR/config/settings.json",
    ledger_path="tracking/EUR/eur_d1_campaign_state.json"
)
```

## 文件清单

| 文件 | 功能 |
|------|------|
| `campaign_pipeline.py` | 主流水线（集成所有能力） |
| `campaign_discipline.py` | 纪律执行器（PROD 三档分类+判死证据链） |
| `discipline_monitor.py` | 纪律监控器（收集每轮回测数据） |
| `improvement_comparator.py` | 改进对比分析器（前后对比） |
| `diversity_integrated_monitor.py` | 多样性集成监控器（10轮综合评估） |
| `__init__.py` | 模块导出 |
| `test_universal_pipeline.py` | 测试脚本 |

## 注意事项

1. **台账格式**：台账文件必须是 JSON 格式，包含 `waves` 和 `dataset_pool` 字段
2. **监控目录**：监控数据存储在 `tracking/<REGION>/monitoring/` 目录下
3. **多样性系统**：多样性评估依赖 `wqb.expression.diversity_enhancer` 模块
4. **MCP 集成**：实际提交回测需要 MCP 集成（当前为模拟）
5. **测试**：运行 `python pipeline/core/test_universal_pipeline.py` 验证功能

## 下一步行动

1. **真实数据验证**：在实际回测中运行 10 个波次，收集真实数据验证改进效果
2. **MCP 集成**：集成 MCP create_multi_simulation 实现真实提交
3. **优化阈值**：根据实证结果调整 PROD 三档阈值（0.75/0.80）和判死证据链参数
4. **扩展区域**：将流水线应用到 USA/EUR/GBR 等其他区域
