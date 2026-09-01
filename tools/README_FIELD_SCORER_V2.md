# 8 维字段质量评分器 V2

## 概述

`field_quality_scorer_v2.py` 是字段质量评分的增强版本，从 4 维扩展到 8 维，提供更全面的字段质量评估。

## 8 维评分体系

| 维度 | 权重 | 说明 | 优化点 |
|------|------|------|--------|
| **覆盖度** | 20% | 字段覆盖股票比例 | + 趋势分析（衰减/改善/稳定）<br>+ 稳定性（波动大小） |
| **历史 Sharpe** | 25% | 字段历史表现 | + 衰减比（recent/full）<br>+ 变异系数（CV）<br>+ 近期表现 |
| **更新频率** | 10% | 数据更新速度 | + 实际延迟检测<br>+ 延迟一致性 |
| **经济可解释性** | 10% | 经济含义明确度 | + 文献支撑（引用经济机制知识库）<br>+ 机制适配度 |
| **字段间相关性** | 10% | 与已选字段相关性 | 新增：多样性惩罚<br>高相关 → 降权 |
| **市场状态适配** | 10% | 当前市场匹配度 | 新增：regime 匹配<br>高波动/低波动/趋势/反转 |
| **数据质量** | 10% | 数据异常检测 | 新增：异常值比例<br>缺失模式<br>跳变检测 |
| **计算成本** | 5% | 计算资源消耗 | 新增：字段类型（MATRIX/VECTOR）<br>计算耗时<br>内存使用 |

## 使用方法

### 基础评分

```bash
# JSON 输出
python tools/field_quality_scorer_v2.py --dataset analyst9 --region IND \
    --fields anl39_agrosmgn2 anl39_earnings_score --json

# 详细输出
python tools/field_quality_scorer_v2.py --dataset analyst9 --region IND \
    --fields anl39_agrosmgn2 anl39_earnings_score --detail
```

### 筛选推荐字段

```bash
# 筛选 score >= 0.6 且 risk <= MEDIUM 的字段
python tools/field_quality_scorer_v2.py --dataset analyst9 --region IND \
    --fields-file fields.json --min-score 0.6 --max-risk MEDIUM

# 限制返回字段数
python tools/field_quality_scorer_v2.py --dataset analyst9 --region IND \
    --fields-file fields.json --max-fields 10
```

### 多样性计算

```bash
# 考虑已选字段的多样性
python tools/field_quality_scorer_v2.py --dataset analyst9 --region IND \
    --fields new_field_1 new_field_2 --selected anl39_earnings_score anl39_agrosmgn2
```

## 输出示例

```
======================================================================
8 维字段质量评分 - analyst9 (IND)
======================================================================
总字段: 3
推荐字段: 3 (score >= 0.6, risk <= MEDIUM)

推荐字段列表:
 1. [LOW] anl39_earnings_score                     score=0.83 risk=LOW
     coverage       : 0.83 - 覆盖度 50%
     sharpe         : 0.67 - 历史 Sharpe 1.00
     frequency      : 1.00 - 频率 daily
     economic       : 0.45 - 经济含义明确
     diversity      : 1.00 - 无已选字段，多样性最优
     regime         : 1.00 - 市场状态 neutral
     data_quality   : 1.00 - 数据质量良好
     compute_cost   : 1.00 - MATRIX 直接可用; 计算快速 (100ms)
```

## 风险等级

| 等级 | 标记 | 条件 | 建议 |
|------|------|------|------|
| **LOW** | [LOW] | score >= 0.8 且无警告 | 优先使用 |
| **MEDIUM** | [MED] | score >= 0.6 且警告 <= 1 | 推荐使用 |
| **HIGH** | [HIGH] | score >= 0.4 | 谨慎使用 |
| **CRITICAL** | [CRIT] | score < 0.4 | 避免使用 |

## 与 V1 对比

| 特性 | V1 (4 维） | V2 (8 维） |
|------|-----------|-----------|
| 覆盖度 | 静态阈值 | + 趋势分析、稳定性 |
| 历史 Sharpe | 单一数值 | + 衰减比、CV、近期表现 |
| 更新频率 | 推断频率 | + 实际延迟、一致性 |
| 经济可解释性 | 关键词匹配 | + 文献支撑、机制适配 |
| 字段间相关性 | 无 | 新增：多样性惩罚 |
| 市场状态适配 | 无 | 新增：regime 匹配 |
| 数据质量 | 无 | 新增：异常检测 |
| 计算成本 | 无 | 新增：类型、耗时 |

## 集成到 GEM 管道

V2 评分器可替换 V1，在 `skeletons.py` 中修改导入：

```python
# 原 V1
from field_quality_scorer import FieldQualityScorer

# 新 V2
from field_quality_scorer_v2 import FieldQualityScorerV2 as FieldQualityScorer
```

## 数据来源

当前使用模拟数据，实际部署时需要：

1. **覆盖度趋势**：从历史 field_catalog 查询
2. **Sharpe 统计**：从 WebDataScope 或回测结果计算
3. **更新延迟**：从数据更新日志查询
4. **字段相关性**：从相关性矩阵计算
5. **数据质量**：从数据质量检测工具获取
6. **计算成本**：从字段元数据估算

## 文件

- `tools/field_quality_scorer_v2.py` - 8 维评分器（744 行）
- `tools/field_quality_scorer.py` - 4 维评分器（保留兼容）
