# Wave 13 特征工程文档 - Mode A 参数层优化

## 基础信息
- **Wave**: 13
- **Region**: USA
- **Dataset**: analyst_earnings_ibes
- **基础候选**: lej3ozml (Sharpe=1.900, Fitness=0.990, Turnover=0.212)
- **优化目标**: 达到 Fitness >= 1.0

## 字段说明
基于 lej3ozml 的骨架模式，使用以下字段：
- `long_term_quantile5_r120_pred`: 长期预测分位数
- `event_5d_single_quantile_pred`: 事件驱动 5 日单分位数预测
- `short_hedge_quantile5_r60_pred`: 短期对冲分位数（用于 3 腿组合）

## 特征工程策略
Mode A 参数层优化：
1. **权重调整**: 调整 long_term 和 event_5d 的权重比例
2. **窗口调整**: 调整 ts_backfill 窗口（66 → 132）
3. **平滑处理**: 使用 ts_mean 或 ts_decay_linear 减少 Turnover
4. **组合扩展**: 添加 short_hedge 形成 3 腿组合

## 表达式列表
共生成 8 个优化表达式，详见 expressions 表（wave=13）。

## 预期改进
- 通过权重调整和平滑处理，预期降低 Turnover
- 通过窗口调整，预期提高信号稳定性
- 目标：Fitness >= 1.0
