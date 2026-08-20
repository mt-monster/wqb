# MEA Wave 35 战役进展总结

## 已完成阶段

### ✅ S-PRE: 区域矩阵查表
- 区域: MEA
- 合法 universe: TOP400, TOP300
- 延迟: 仅 D1（无 D0）
- 默认中性化: SECTOR
- Max Trade: ON
- 未点亮金字塔: fundamental, earnings

### ✅ S0: 健康检查
- 主攻数据集: **fundamental72**（300 VECTOR 字段，未点亮金字塔）
- 辅助数据集: **analyst7**（300 VECTOR 字段，需正交信号）
- 历史仿真已过期，重新提交

### ✅ S1: 字段扫描
- fundamental72: 300 个 VECTOR 字段
  - 高覆盖率字段: EPS (0.876), Operating Income (0.876), Total Assets (0.876), Cash (0.876), CFO (0.841)
- analyst7: 300 个 VECTOR 字段
  - 高覆盖率字段: EPS Mean (0.572), EPS Revisions (0.610), ROE Consensus (0.489)

### ✅ S2-D: 多样性榨取
生成 16 个多样化表达式，覆盖 6 大类别：
1. **EPS 动量/增长** (2个)
2. **盈利能力** (1个)
3. **现金流质量** (2个)
4. **资产负债表强度** (2个)
5. **分析师修订** (5个)
6. **复合信号** (2个)

### ✅ S2': 设置展开
- 生成 `alpha_list_wave35.json`（16 个 alpha）
- 统一设置: MEA/TOP400/D1/SECTOR/decay=4/truncation=0.08/maxTrade=ON

### ⏳ S3: 批量回测（进行中）
已提交 2 批共 16 个 alpha：

**Batch 1** (fundamental72): Multisim ID `1NvPlgd5o4vBbxqPEHkoaOx`
- 8 个 alpha：EPS 动量、EPS 增长、盈利能力、现金流质量、FCF 收益率、ROE、低负债、低应计

**Batch 2** (analyst7 + mixed): Multisim ID `Zuv59emn4j5cpE1aWFxGAlO`
- 8 个 alpha：EPS 上调修订、EPS 下调修订、EPS 共识动量、分析师 ROE、分析师离散度、复合质量、资产负债表强度、分析师惊喜

**状态**: 平台回测中（预计 5-15 分钟）

## 筛选条件
- sharpe > 1.58
- fitness > 1
- 2ysharpe > 1.6
- margin > 5bp
- turnover 5%-30%
- risk neutralization: sharpe>1, fitness>0.7, margin>5bp, ra_failed_count=0

## 目标
找到 10 个满足提交要求、彼此相关性 < 0.4、策略风格完全不同的 REGULAR alpha

## 下一步
1. ⏳ 等待回测完成（后台轮询中）
2. 筛选达标 alpha（sharpe>1.58, fitness>1）
3. 进行 robust test（不同 universe/neutralization）
4. 进行过拟合测试（2y sharpe>1.6）
5. 计算 alpha 间相关性矩阵
6. 选择 10 个相关性 < 0.4 的 alpha
7. 设置 alpha 属性并提交

## 后台任务
- 轮询脚本: `tracking/MEA/scripts/background_poll_wave35.py`
- 中间结果: `tracking/MEA/results/wave35_results_partial.json`
- 最终结果: `tracking/MEA/results/wave35_results_final.json`
