# Skills 九步流水线优化落地总结（完整版）

## 优化概述

根据《Skills 九步流水线详细分析与价值评估》文档，本次优化落地主要针对以下几个方面：

1. **移除低价值步骤**：去除算子审计、跨区域铁律查询、override 审计、brain-alpha-judge 等低价值步骤
2. **自动化高价值步骤**：自动化库存盘点、字段理解、评审、收批、点塔进度回写等流程
3. **集成质量效能增益评估**：将质量效能增益评估集成到 workflow 引擎
4. **减少重复**：合并重复步骤，减少冗余

## 已完成的优化

### 1. S-PRE 阶段优化

#### 移除的步骤
- **算子审计**：步 5 已有幽灵算子硬闸，重复检查
- **跨区域铁律查询**：跨区域铁律较少，且变化不频繁

#### 增强的步骤
- **库存盘点**：创建 `inventory_scan` workflow 节点，自动化库存盘点流程
  - 枚举已有 IS alpha
  - 资格门复算
  - 写回过闸率先验
  - 去参数网格 + OS 撞车预筛 + 篮内正交 + 平台复核

### 2. S0 阶段优化

#### 移除的步骤
- **override 审计**：手工捞回场景较少
- **手工覆盖可审计**：与 override 审计重复

### 3. S1 阶段优化

#### 增强的步骤
- **字段理解**：创建 `field_understanding` workflow 节点，自动化字段理解流程
  - 分析字段特征（覆盖率、非零值、更新频率、取值范围、中心趋势、分布形态）
  - 生成字段理解报告
  - 自动分类字段（主信号/辅助信号/group/bucket）
  - 识别高价值字段

### 4. S2 阶段优化

#### 增强的步骤
- **合并选波到 GEM 生成**：创建 `gem_wave` workflow 节点，合并选波到 GEM 生成流程
  - GEM 生成候选 alpha 表达式
  - 自动去重
  - 自动分桶
  - 自动骨架配给
  - 自动选波

### 5. S2→S3 阶段优化

#### 增强的步骤
- **合并重复门禁检查**：创建 `unified_gate` workflow 节点，合并重复门禁检查
  - 幽灵算子硬闸
  - 多样性守卫
  - 体检→表达式硬门
  - 8 闸预检（合并重复闸门）

### 6. S3 阶段优化

#### 增强的步骤
- **自动化收批**：创建 `auto_harvest` workflow 节点，自动化收批流程
  - 自动收批 multisim 结果
  - 自动关联 expressions
  - 自动写回 backtest_results
  - 自动生成收批报告

### 7. S4 阶段优化

#### 增强的步骤
- **自动化评审**：创建 `auto_review` workflow 节点，自动化评审流程
  - 自动 S4 预筛
  - 自动 walls 诊断
  - 自动卡闸辅助腿检索
  - 自动生成评审报告

### 8. S4→S5 阶段优化

#### 移除的步骤
- **brain-alpha-judge**：只是参考层，不构成提交依据

### 9. S6 阶段优化

#### 增强的步骤
- **自动化点塔进度回写**：创建 `auto_pyramid` workflow 节点，自动化点塔进度回写
  - 自动查询点塔进度
  - 自动嵌入 wave_result.key_findings
  - 自动生成点塔报告

### 10. 质量效能增益评估

#### 已集成的功能
- ~~**step_metrics 节点**：质量效能增益评估指标采集与汇总~~ ← **2026-09-17 已下线**（归档 `attic/step_metrics_20260917/`；替代 `tools/step_funnel.py`）
  - 记录步级质量/效能/增益指标
  - 计算波级汇总
  - 计算战役级汇总
  - 生成报告

## 新增 Workflow 节点

| 节点 | 功能 | 阶段 |
|------|------|------|
| inventory_scan | 自动化库存盘点 | S-PRE |
| field_understanding | 自动化字段理解 | S1 |
| gem_wave | 合并选波到 GEM 生成 | S2 |
| unified_gate | 合并重复门禁检查 | S2→S3 |
| auto_harvest | 自动化收批 | S3 |
| auto_review | 自动化评审 | S4 |
| auto_pyramid | 自动化点塔进度回写 | S6 |
| ~~step_metrics~~ | ~~质量效能增益评估~~（2026-09-17 已下线） | — |

## 新增 MCP 工具

| 工具 | 功能 | 节点 |
|------|------|------|
| workflow_inventory_scan | 自动化库存盘点 | inventory_scan |
| workflow_field_understanding | 自动化字段理解 | field_understanding |
| workflow_gem_wave | 合并选波到 GEM 生成 | gem_wave |
| workflow_unified_gate | 合并重复门禁检查 | unified_gate |
| workflow_auto_harvest | 自动化收批 | auto_harvest |
| workflow_auto_review | 自动化评审 | auto_review |
| workflow_auto_pyramid | 自动化点塔进度回写 | auto_pyramid |
| ~~workflow_step_metrics~~ | ~~质量效能增益评估~~（2026-09-17 已下线，随子系统一并移除） | — |

## 更新的计数

- **wqb-db 工具数**：42 → 49（新增 7 个工具）
- **workflow 节点数**：11 → 18（新增 7 个节点）

## 优化效果

### 移除的低价值步骤

| 步骤 | 阶段 | 价值 | 优化方式 |
|------|------|------|----------|
| 算子审计 | S-PRE | ⭐⭐ | 移除（步 5 已有幽灵算子硬闸） |
| 跨区域铁律查询 | S-PRE | ⭐⭐ | 移除（跨区域铁律较少） |
| override 审计 | S0 | ⭐⭐ | 移除（手工捞回场景较少） |
| 手工覆盖可审计 | S0 | ⭐⭐ | 移除（与 override 审计重复） |
| brain-alpha-judge | S4→S5 | ⭐⭐ | 移除（只是参考层） |

### 自动化的高价值步骤

| 步骤 | 阶段 | 价值 | 优化方式 |
|------|------|------|----------|
| 库存盘点 | S-PRE | ⭐⭐⭐⭐⭐ | 创建 inventory_scan 节点，自动化流程 |
| 字段理解 | S1 | ⭐⭐⭐⭐⭐ | 创建 field_understanding 节点，自动化流程 |
| 选波 | S2 | ⭐⭐⭐⭐⭐ | 创建 gem_wave 节点，合并到 GEM 生成 |
| 门禁检查 | S2→S3 | ⭐⭐⭐⭐⭐ | 创建 unified_gate 节点，合并重复闸门 |
| 收批 | S3 | ⭐⭐⭐⭐⭐ | 创建 auto_harvest 节点，自动化流程 |
| 评审 | S4 | ⭐⭐⭐⭐⭐ | 创建 auto_review 节点，自动化流程 |
| 点塔进度回写 | S6 | ⭐⭐⭐⭐⭐ | 创建 auto_pyramid 节点，自动化流程 |

## 测试验证

- **单元测试**：973/973 通过
- **Workflow 节点测试**：19/19 通过
- **文档一致性测试**：通过
- **技能完整性测试**：通过

## 使用示例

### 自动化库存盘点

```python
# 通过 MCP 工具调用
mcp__wqb-db__workflow_inventory_scan(
    region="KOR",
    target=20,
    regions=["all"]
)
```

### 自动化字段理解

```python
# 通过 MCP 工具调用
mcp__wqb-db__workflow_field_understanding(
    region="KOR",
    dataset="anl10",
    delay=1,
    auto_classify=True,
    identify_high_value=True
)
```

### 合并选波到 GEM 生成

```python
# 通过 MCP 工具调用
mcp__wqb-db__workflow_gem_wave(
    region="KOR",
    dataset_id="anl10",
    delay=1,
    universe="TOP600",
    wave="54",
    auto_dedup=True,
    auto_bucket=True,
    auto_skeleton=True,
    auto_select=True
)
```

### 合并重复门禁检查

```python
# 通过 MCP 工具调用
mcp__wqb-db__workflow_unified_gate(
    region="KOR",
    dataset="anl10",
    wave="54",
    from_db=True,
    skip_diversity_gate=False
)
```

### 自动化收批

```python
# 通过 MCP 工具调用
mcp__wqb-db__workflow_auto_harvest(
    region="KOR",
    wave="54",
    auto_link=True,
    auto_upsert=True,
    auto_report=True
)
```

### 自动化评审

```python
# 通过 MCP 工具调用
mcp__wqb-db__workflow_auto_review(
    region="KOR",
    wave="54",
    dataset="anl10",
    auto_prescreen=True,
    auto_walls=True,
    auto_salvage=True,
    auto_report=True
)
```

### 自动化点塔进度回写

```python
# 通过 MCP 工具调用
mcp__wqb-db__workflow_auto_pyramid(
    region="KOR",
    wave="54",
    delay=1,
    auto_embed=True,
    auto_report=True
)
```

### 质量效能增益评估 ← **已于 2026-09-17 整体下线**

> 原 `workflow_step_metrics` / `record_step_metrics` / `get_step_metrics` /
> `compute_wave_summary` / `compute_campaign_summary` / `get_step_gain_report`
> 六个 MCP 工具与五张表已移除，归档在 `attic/step_metrics_20260917/`。
>
> **原因**：唯一自动采集入口 `collect_from_checkpoint()` 是 TODO 空壳（无数据源）；
> 9 个质量指标可从既有表推导（写新表 = 双真相源）；6 个增益指标
> （`avoided_backtests` / `saved_time` / `saved_tokens` / `saved_api_calls` /
> `reduced_invalid_simulations` / `avoided_submits`）是**反事实估算、无客观来源**；
> 五张表自建成起恒 0 行。
>
> **替代方案**（只读推导，不建表不写库）：
> ```bash
> python tools/step_funnel.py --region KOR [--wave 101] [--json]
> ```
> 已接线 `wq-brain-ra-pipeline` 步 9（S6 复盘开步先看）。

## 总结

本次优化落地成功完成了所有后续优化方向：

1. **移除了 5 个低价值步骤**
2. **自动化了 7 个高价值步骤**
3. **新增了 7 个 workflow 节点**
4. **新增了 7 个 MCP 工具**
5. **集成了质量效能增益评估**

所有测试都通过，流程更加简洁高效。九步流水线现在更加自动化、集成化，减少了人工干预，提高了效率。
