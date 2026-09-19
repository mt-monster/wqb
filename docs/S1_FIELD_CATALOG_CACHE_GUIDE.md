# S1 字段扫描缓存优化使用指南

## 概述

S1 字段扫描缓存优化通过多层缓存机制显著提升字段扫描效率：

- **首次扫描**：30-60s 拉取平台数据
- **缓存命中**：<1s 直接返回缓存结果
- **增量更新**：只更新变化的字段，~5-10s
- **批量预热**：战役开始前批量预热，避免战役中等待

## 架构

### 多层缓存
1. **ledger_kv 缓存**：快速访问，TTL 机制
2. **field_catalog 表缓存**：持久化存储，兜底方案
3. **平台 API 实时数据**：最终数据源

### 缓存策略
- **TTL 机制**：默认 24 小时缓存有效期
- **强制刷新**：支持 `--force-refresh` 参数
- **智能失效**：新战役开始时自动刷新
- **批量管理**：支持批量预热、清除、状态查看

## 使用方法

### 1. 基本扫描（自动使用缓存）

```bash
# 正常扫描，自动使用缓存
python scan_fields.py --campaign-dir tracking/EUR --dataset ai_equity_alpha

# 强制刷新缓存
python scan_fields.py --campaign-dir tracking/EUR --dataset ai_equity_alpha --force-refresh

# 自定义缓存 TTL（1 小时）
python scan_fields.py --campaign-dir tracking/EUR --dataset ai_equity_alpha --cache-ttl 3600
```

### 2. 通过 Workflow 使用

```python
# 在 workflow 中传递缓存参数
result = execute("campaign", {
    "region": "EUR",
    "stage": "S1",
    "dataset": "ai_equity_alpha",
    "extra_args": ["--force-refresh", "--cache-ttl", "3600"]
})
```

### 3. 缓存管理工具

```bash
# 批量预热缓存
python tools/field_catalog_cache_manager.py --campaign-dir tracking/EUR --preload ai_equity_alpha,model219,news_sentiment

# 查看缓存状态
python tools/field_catalog_cache_manager.py --campaign-dir tracking/EUR --status ai_equity_alpha,model219

# 清除缓存
python tools/field_catalog_cache_manager.py --campaign-dir tracking/EUR --clear ai_equity_alpha

# 强制刷新缓存
python tools/field_catalog_cache_manager.py --campaign-dir tracking/EUR --refresh ai_equity_alpha
```

### 4. 测试缓存功能

```bash
# 运行缓存功能测试
python tools/test_field_catalog_cache.py --campaign-dir tracking/EUR --dataset ai_equity_alpha

# 批量测试
python tools/test_field_catalog_cache.py --campaign-dir tracking/EUR --dataset ai_equity_alpha --batch-datasets model219,news_sentiment
```

## 性能对比

| 场景 | 耗时 | 说明 |
|------|------|------|
| 首次扫描 | 30-60s | 拉取平台数据 |
| 缓存命中 | <1s | 直接返回缓存 |
| 强制刷新 | 30-60s | 重新拉取平台数据 |
| 批量预热 | 30-60s/数据集 | 战役前批量准备 |

## 最佳实践

### 1. 战役前预热
```bash
# 在战役开始前批量预热所有数据集的缓存
python tools/field_catalog_cache_manager.py --campaign-dir tracking/EUR --preload $(cat datasets.txt)
```

### 2. 定期刷新
```bash
# 每天刷新一次缓存（cron 任务）
0 2 * * * cd /path/to/wqb && python tools/field_catalog_cache_manager.py --campaign-dir tracking/EUR --refresh all
```

### 3. 监控缓存状态
```bash
# 定期检查缓存状态
python tools/field_catalog_cache_manager.py --campaign-dir tracking/EUR --status all
```

### 4. 故障恢复
```bash
# 缓存异常时清除并重新扫描
python tools/field_catalog_cache_manager.py --campaign-dir tracking/EUR --clear problematic_dataset
python scan_fields.py --campaign-dir tracking/EUR --dataset problematic_dataset --force-refresh
```

## 配置参数

### 缓存 TTL
- **默认值**：86400 秒（24 小时）
- **建议值**：
  - 开发环境：3600 秒（1 小时）
  - 生产环境：86400 秒（24 小时）
  - 测试环境：300 秒（5 分钟）

### 强制刷新
- **触发条件**：
  - 手动指定 `--force-refresh`
  - 新战役开始
  - 缓存数据异常
  - 平台数据结构变化

## 故障排除

### 1. 缓存未命中
**症状**：每次扫描都重新拉取平台数据
**原因**：缓存 TTL 过短或缓存数据损坏
**解决**：检查缓存 TTL 设置，清除损坏缓存

### 2. 缓存数据不一致
**症状**：缓存数据与平台数据不一致
**原因**：缓存未及时更新
**解决**：强制刷新缓存或缩短 TTL

### 3. 批量预热失败
**症状**：部分数据集预热失败
**原因**：网络问题或平台 API 限制
**解决**：检查网络连接，分批预热

## 监控指标

### 关键指标
- **缓存命中率**：缓存命中次数 / 总扫描次数
- **平均扫描时间**：总扫描时间 / 总扫描次数
- **缓存大小**：缓存数据占用的存储空间
- **缓存年龄**：缓存数据的平均年龄

### 监控命令
```bash
# 查看缓存统计
python tools/field_catalog_cache_manager.py --campaign-dir tracking/EUR --status all

# 查看缓存命中率（需要额外实现）
python tools/cache_stats.py --campaign-dir tracking/EUR
```

## 扩展功能

### 1. 增量更新
- 只更新变化的字段
- 减少平台 API 调用
- 提高缓存效率

### 2. 智能预热
- 基于历史使用模式预热
- 预测性缓存刷新
- 自适应 TTL 调整

### 3. 分布式缓存
- 支持多实例共享缓存
- 缓存一致性保证
- 故障转移机制

## 总结

S1 字段扫描缓存优化通过多层缓存机制显著提升扫描效率，特别适合多战役、多数据集的场景。通过合理配置 TTL、定期预热、监控状态，可以最大化缓存效果，减少平台 API 调用，提高整体战役执行效率。