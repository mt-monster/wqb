# EUR 挖掘战役最终报告 v4 (2026-08-12 提交验证后)

## 提交测试结果
| 候选 | 结果 | 真实拒因 |
|------|------|---------|
| mL5Yx3X9 (rev504×d20×STAT×TOP2500) | ❌ 403 拒绝 | **PROD_CORR 0.9512** + LOW_2Y 1.08 |
| e7362rWM / P0GMXWpL / XgoRLKX1 | ❌ 404 (异步被拒) | 同型 |

**MCP submit_alpha 预检拦截原因 (margin 8bp) 是工具层自定义 — 平台真实拒因是 prod_corr 0.95**

## 核心结论: EUR 反转信号 prod_corr 墙
- returns 反转是 EUR 信号最强的族 (S 2.6+) 但 **prod_corr 0.95** (平台生产池已挤满 EUR 反转)
- 直方图: 与生产池 2 个 alpha 相关 >0.9, 24 个 >0.8
- 因子信号 (ml_factor_proj/news/ai) prod_corr 低但 S max 1.27 不达标
- 反转+因子混合: 稀释信号 (S 0.03-0.25), 无中间地带

## 论坛方法验证
| 方法 | 结果 |
|------|------|
| prod-corr vs power-pool 区分 (post 32223192365207) | 确认是 prod-corr 非 power-pool |
| prod-corr 失败但逻辑扎实可重试 (post 32196746752023) | 需换非反转结构 |
| Single Data Set + 全中性化 (post 30933525139863) | 已做, 因子信号仍弱 |

## 最终判定
**EUR 当前无达标可提交候选** (结构性限制):
1. 反转信号: prod_corr 0.95 不可破 (拥挤)
2. 因子信号: S 不达标 (弱)
3. 组合: 无中间地带

## 待办
1. 等 EUR PPA 主题 (9月可能) — 主题内 prod_corr 池可能不同
2. 等新数据包 (ml_factor_proj 等 0-alpha 数据集若有新字段可能出强信号)
3. 或换区域 (IND/MEA 已证明有空间: A1GN2mWX/QPGbAOn5 今日提交成功)
