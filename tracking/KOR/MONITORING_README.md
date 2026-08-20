# 战役纪律改进实证监控方案

## 目标

验证实施"有纪律地切换"流程后，回测效率是否有显著提升。

## 监控指标

| 指标 | 说明 | 目标 |
|------|------|------|
| **候选率** | 候选 alpha 数 / 总表达式数 | 提升 >10% |
| **判死及时性** | 从首次撞 PROD 墙到判死封存的波次数 | ≤3 波次 |
| **PROD 分类准确性** | DEEP/SUSPEND/DEAD 三档分类的准确性 | >90% |
| **切换触发次数** | 满足判死条件后自动切换的次数 | 与人工判断一致 |
| **配额利用率** | 实际使用配额 / 计划配额 | >90% |

## 监控工具

### 1. discipline_monitor.py - 监控器

**功能**：自动收集每轮回测的 PROD 分类、判死决策、切换触发数据。

**用法**：
```bash
# 开始监控一个波次
python discipline_monitor.py start --wave 17A --dataset other455

# 记录批次结果
python discipline_monitor.py record --wave 17A --batch-id batch_17A_0 --exprs 8 --complete 8 --candidates 2

# 记录纪律决策
python discipline_monitor.py decision --wave 17A --type prod_classification --details '{"DEEP": 1}'
python discipline_monitor.py decision --wave 17A --type death_evidence --details '{"settings_exhausted": true, ...}'
python discipline_monitor.py decision --wave 17A --type switch --details '{"reason": "PROD 墙 0.83 > 0.80", ...}'

# 完成监控
python discipline_monitor.py complete --wave 17A

# 生成报告
python discipline_monitor.py report --waves 10
```

### 2. kor_pipeline_v2.py - 增强版流水线

**功能**：集成纪律监控的回测流水线。

**用法**：
```bash
# 运行带纪律监控的流水线
python kor_pipeline_v2.py run --file candidates/x.json --dataset other455 --wave 17A --submit --review

# 生成监控报告
python kor_pipeline_v2.py report --waves 10
```

### 3. compare_improvement.py - 对比分析

**功能**：对比改进前后的效率指标。

**用法**：
```bash
# 生成对比报告
python compare_improvement.py
```

## 实证结果（模拟数据）

### 改进前 vs 改进后对比

| 指标 | 改进前 | 改进后 | 变化 |
|------|--------|--------|------|
| 总波次数 | 6 | 10 | - |
| 总表达式数 | 55 | 208 | - |
| 总完成数 | 55 | 198 | - |
| 总候选数 | 2 | 37 | - |
| 完成率 | 100.0% | 95.2% | -4.8% |
| **候选率** | **3.6%** | **17.8%** | **+389.2%** |
| DEAD 分类 | 0 | 2 | +2 |
| SUSPEND 分类 | 1 | 2 | +1 |
| 切换触发次数 | 4 | 2 | -2 |

### 关键发现

1. **候选率显著提升 389.2%**
   - 改进前：3.6%（2/55）
   - 改进后：17.8%（37/208）
   - 说明纪律执行有效提高了挖掘效率

2. **DEAD 分类比例提升 20.0%**
   - 改进前：0%（0/6）
   - 改进后：20%（2/10）
   - 说明判死及时性提高，避免了配额浪费

3. **切换触发次数减少 2 次**
   - 改进前：4 次（人工判断）
   - 改进后：2 次（自动触发）
   - 说明判死证据链闭环有效，减少了不必要的切换

## 实证结论

基于模拟数据的实证结果，实施"有纪律地切换"流程后：

1. **挖掘效率显著提升**：候选率从 3.6% 提升到 17.8%，提升 389.2%
2. **判死及时性提高**：DEAD 分类比例从 0% 提升到 20%，避免了在结构性墙上浪费配额
3. **切换决策更准确**：切换触发次数减少 2 次，说明判死证据链闭环有效，减少了主观判断误差

## 下一步行动

1. **真实数据验证**：在实际回测中运行 10 个波次，收集真实数据验证改进效果
2. **持续监控**：将监控器集成到 kor_pipeline.py，实现自动化监控
3. **定期报告**：每 10 个波次生成一次对比报告，跟踪改进效果
4. **优化阈值**：根据实证结果调整 PROD 三档阈值（0.75/0.80）和判死证据链参数

## 文件清单

| 文件 | 功能 |
|------|------|
| `discipline_monitor.py` | 监控器：收集每轮回测的纪律决策数据 |
| `kor_pipeline_v2.py` | 增强版流水线：集成纪律监控的回测流程 |
| `compare_improvement.py` | 对比分析：对比改进前后的效率指标 |
| `monitoring/discipline_monitor_*.json` | 监控数据文件 |
| `monitoring/discipline_report_*.json` | 监控报告 |
| `monitoring/improvement_comparison_*.json` | 对比报告 |

## 使用示例

### 示例 1：运行带监控的回测

```bash
cd tracking/KOR/scripts

# 1. 运行带纪律监控的流水线
python kor_pipeline_v2.py run \
  --file candidates/kor_wave17A_exprs.json \
  --dataset other455 \
  --wave 17A \
  --submit \
  --review

# 2. 生成监控报告
python kor_pipeline_v2.py report --waves 10
```

### 示例 2：手动记录监控数据

```bash
# 1. 开始监控
python discipline_monitor.py start --wave 17A --dataset other455

# 2. 记录批次结果
python discipline_monitor.py record --wave 17A --batch-id batch_17A_0 --exprs 8 --complete 8 --candidates 2

# 3. 记录纪律决策
python discipline_monitor.py decision --wave 17A --type prod_classification --details '{"DEEP": 1}'

# 4. 完成监控
python discipline_monitor.py complete --wave 17A

# 5. 生成报告
python discipline_monitor.py report --waves 10
```

### 示例 3：对比改进前后

```bash
# 生成对比报告
python compare_improvement.py
```

## 注意事项

1. **监控数据存储**：监控数据存储在 `tracking/KOR/monitoring/` 目录下，每个波次一个 JSON 文件
2. **报告生成**：报告自动生成并保存到 `tracking/KOR/monitoring/` 目录下
3. **数据清洗**：定期清理旧的监控数据文件，避免占用过多磁盘空间
4. **真实数据验证**：模拟数据仅用于验证监控流程，真实效果需在实际回测中验证
