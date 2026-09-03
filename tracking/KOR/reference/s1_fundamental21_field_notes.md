# S1 字段理解：fundamental21（KOR/TOP600/D1）

- 数据集类型：153 字段全 VECTOR（ESG 新闻衍生评分，Refinitiv 风格），双前缀族：fnd21_*（cov 0.6055）+ fnd27_*（cov 0.6991-0.7128）
- 主题：30 个 ESG 类别的新闻量（categoryvolumettm）/冲击占比（impactpercentagettm）/质量分（insight）/趋势（momentum=TTM 斜率）/短期脉冲（pulse）/行业百分位（industrypercentile，预计算相对化）
- **定位差异化**：与 KOR 已判死的 news tone/event-score 族（news38/50/87/96/141）机制不同——ESG 是慢变质量/治理溢价信号，TTM 聚合天然低换手，非日频情绪

## 字段/特征/建议

- **主选 fnd27_* 族（cov≈0.71，users=0 冷门，prod_corr 规避理想）**：allcategories_insight（综合质量）、allcategoriesindustrypercentile_insight（预计算行业相对）、materiality_insight/momentum（重大类别聚焦）、allcategories_momentum（TTM 改善斜率）、allcategories_pulse（短期脉冲）、volume_ttmdaily_allcategories_articlevolumettm（关注度）
- **禁用 fnd21 insight/momentum/pulse 族**：cov 0.26-0.31 低于 0.4 硬门，ts_backfill 也难救
- fnd21_* categoryvolume/impactpercentage 族 cov 0.6055 可用但优先 fnd27 同类（更新、更冷）
- 类别聚焦备选：supplychainmanagement/ghgemissions 的 insight+momentum（韩国财阀供应链与排放监管敏感）

## 初始信号

1. ESG 综合质量溢价：allcategories_insight 高 → 治理质量好 → 正漂移（慢信号）
2. ESG 改善动量：allcategories_momentum（TTM 斜率）正 → ESG 趋势改善被低估
3. 行业相对 ESG：industrypercentile 字段已预计算行业内百分位 → 直接 rank

## 进阶信号

- materiality 聚焦（只对重大类别计分，噪声更低）vs allcategories 对照
- pulse 短期脉冲 vs insight 慢质量：时间尺度分离
- 负面冲击：accidentandsafetymanagement / businessethics impactpercentage 高 → 负向（治理风险事件）
- 关注度反转：articlevolumettm 高 → 注意力过度 → 负向（wave144 vea 判死，低优先）

## 预处理决策

- VECTOR → vec_avg 聚合；ESG 评分月度更新为主 → ts_backfill 22 补洞（cov 0.71 仍需）
- 评分/百分位偏态 → rank 强制；industrypercentile 已相对化仍可 rank 归一
- 慢信号 → ts_decay_linear(22) 平滑（wave143 验证 +0.07S）；组内相对化用 industry（wave143 验证 +0.10S）
