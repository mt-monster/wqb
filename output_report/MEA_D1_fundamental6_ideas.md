# MEA 区域 fundamental6 数据集特征工程报告

## 1. 数据集理解

### 数据集描述
**fundamental6** - Company Fundamental Data for Equity
- **类别**: fundamental
- **字段数**: 382
- **覆盖率**: 0.5078
- **金字塔倍数**: 1.5 **[未点亮金字塔]**
- **Alpha 数量**: 4045
- **数据类型**: 以 VECTOR 为主，少量 MATRIX

### 字段清单概览
- **VECTOR 字段**: ~370 个（主要是财务报表项目）
- **MATRIX 字段**: ~12 个（主要是季度数据）
- **更新频率**: 混合（年度、季度、YTD）
- **核心业务**: 公司基本面数据（资产负债表、利润表、现金流量表）

### 数据结构要点观察
1. **财务报表完整性**: 涵盖三大报表的核心科目
2. **时间维度多样**: 年度、季度、YTD（年初至今）数据并存
3. **覆盖率中等**: 0.5078 表明部分公司数据缺失
4. **VECTOR 主导**: 大部分字段为 VECTOR 类型，需要 vec_* 聚合后才能用于常规算子

## 2. 字段解构分析

### 核心字段分类

#### 资产负债表字段
- **资产类**: 
  - `fundamental_current_assets_total` (流动资产合计)
  - `fundamental_assets_other` (其他资产)
  - `fundamental_property_plant_and_equipment_net` (固定资产净值)
  - `fundamental_intangible_assets_total` (无形资产合计)
  - `fundamental_goodwill` (商誉)

- **负债类**:
  - `fundamental_current_liabilities_total` (流动负债合计)
  - `fundamental_long_term_debt` (长期债务)
  - `fundamental_debt_in_current_liabilities` (流动负债中的债务)
  - `fundamental_other_liabilities_total` (其他负债合计)

- **权益类**:
  - `fundamental_common_equity_total` (普通股权益合计)
  - `fundamental_retained_earnings` (留存收益)
  - `fundamental_equity_reserves_total_q` (权益储备合计-季度)

#### 利润表字段
- **收入类**:
  - `fundamental_annual_revenue` (年度收入)
  - `fundamental_net_revenue` (净收入)
  - `fundamental_revenue_quarterly` (季度收入) [MATRIX]

- **成本费用类**:
  - `fundamental_cost_of_goods_sold` (销售成本)
  - `fundamental_operating_expense_total` (营业费用合计)
  - `fundamental_selling_general_and_administrative_expense` (销售管理费用)

- **利润类**:
  - `fundamental_earnings_before_interest_and_taxes` (息税前利润)
  - `fundamental_ebitda` (息税折旧摊销前利润)
  - `fundamental_pretax_income` (税前利润)
  - `fundamental_income_before_extraordinary_items` (非常项目前利润)

#### 现金流量表字段
- **经营活动**:
  - `fundamental_operating_activities_net_cash_flow` (经营活动净现金流)
  - `fundamental_net_operating_cash_flow_ytd` (年初至今经营净现金流)

- **投资活动**:
  - `fundamental_investing_net_cash_flow_annual` (投资活动净现金流-年度)
  - `fundamental_capital_expenditures_annual` (资本支出-年度)

- **筹资活动**:
  - `fundamental_financing_net_cash_flow` (筹资活动净现金流)
  - `fundamental_dividends_total` (股利合计)

### 字段间逻辑关系
1. **资产负债表恒等式**: 资产 = 负债 + 权益
2. **利润表流向**: 收入 → 成本费用 → 利润
3. **现金流勾稽**: 经营 + 投资 + 筹资 = 现金净变动
4. **时间序列关系**: YTD 数据 = 各季度数据累加

### 数据讲述的"故事"
该数据集提供了公司财务健康状况的全景视图，可以用于：
- 评估公司财务质量（偿债能力、盈利能力、运营效率）
- 识别财务异常（异常增长、异常波动、结构突变）
- 预测未来表现（基于历史趋势和财务比率）

## 3. 按问题类型分类的特征工程建议

### 3.1 稳定性特征

#### 特征 1: 财务比率稳定性
- **概念名称**: 流动比率稳定性
- **定义**: 流动比率（流动资产/流动负债）的滚动变异系数
- **逻辑含义**: 度量公司短期偿债能力的稳定性
- **为何有意义**: 稳定的流动比率表明公司财务管理稳健
- **方向性**: 低变异系数 = 稳定 = 更好
- **边界条件**: 变异系数 > 0.5 表明波动剧烈
- **数据需求**: `fundamental_current_assets_total`, `fundamental_current_liabilities_total`
- **潜在问题**: VECTOR 字段需要 vec_avg 聚合

#### 特征 2: 盈利能力稳定性
- **概念名称**: ROE 稳定性
- **定义**: ROE（净利润/股东权益）的滚动标准差
- **逻辑含义**: 度量公司盈利能力的可预测性
- **为何有意义**: 稳定的 ROE 表明公司具有持续竞争优势
- **方向性**: 低标准差 = 稳定 = 更好
- **边界条件**: 标准差 > 0.1 表明盈利波动大
- **数据需求**: `fundamental_income_before_extraordinary_items`, `fundamental_common_equity_total`
- **潜在问题**: 需要处理负值情况

### 3.2 变化特征

#### 特征 3: 收入增长率
- **概念名称**: 收入同比增长率
- **定义**: (本期收入 - 去年同期收入) / 去年同期收入
- **逻辑含义**: 度量公司业务扩张速度
- **为何有意义**: 收入增长是公司价值创造的核心驱动
- **方向性**: 高增长率 = 好（但需结合质量）
- **边界条件**: 增长率 > 100% 可能不可持续
- **数据需求**: `fundamental_revenue_quarterly` [MATRIX]
- **潜在问题**: MATRIX 字段可直接使用

#### 特征 4: 资产负债率变化
- **概念名称**: 资产负债率变化率
- **定义**: (本期资产负债率 - 上期资产负债率) / 上期资产负债率
- **逻辑含义**: 度量公司财务杠杆的变化趋势
- **为何有意义**: 快速上升的杠杆可能预示财务风险
- **方向性**: 负变化率 = 去杠杆 = 好
- **边界条件**: 变化率 > 20% 需警惕
- **数据需求**: `fundamental_current_liabilities_total`, `fundamental_long_term_debt`, `fundamental_current_assets_total`
- **潜在问题**: 需要计算资产负债率

### 3.3 异常特征

#### 特征 5: 异常现金流
- **概念名称**: 经营现金流异常度
- **定义**: (经营现金流 - 净利润) / 总资产
- **逻辑含义**: 度量公司盈利质量（现金流 vs 会计利润）
- **为何有意义**: 现金流与利润的背离可能预示财务造假
- **方向性**: 接近 0 = 正常，大幅偏离 = 异常
- **边界条件**: 绝对值 > 0.2 需深入调查
- **数据需求**: `fundamental_operating_activities_net_cash_flow`, `fundamental_income_before_extraordinary_items`, `fundamental_current_assets_total`
- **潜在问题**: 需要处理负值和零值

#### 特征 6: 异常费用率
- **概念名称**: 销售管理费用率异常
- **定义**: 销售管理费用率 - 行业平均费用率
- **逻辑含义**: 度量公司费用控制能力相对于行业的偏离
- **为何有意义**: 异常高的费用率可能表明管理效率低下
- **方向性**: 负偏离 = 费用控制好 = 好
- **边界条件**: 偏离 > 5% 需关注
- **数据需求**: `fundamental_selling_general_and_administrative_expense`, `fundamental_net_revenue`
- **潜在问题**: 需要行业平均数据（可用 rank 代替）

### 3.4 交互特征

#### 特征 7: 盈利质量交互
- **概念名称**: 盈利质量综合评分
- **定义**: (经营现金流/净利润) * (1 - 资产负债率)
- **逻辑含义**: 结合现金流质量和财务杠杆的综合指标
- **为何有意义**: 高质量盈利 + 低杠杆 = 投资价值
- **方向性**: 高评分 = 好
- **边界条件**: 评分 < 0 表明盈利质量差或杠杆过高
- **数据需求**: `fundamental_operating_activities_net_cash_flow`, `fundamental_income_before_extraordinary_items`, `fundamental_current_liabilities_total`, `fundamental_long_term_debt`, `fundamental_current_assets_total`
- **潜在问题**: 需要处理除零和负值

#### 特征 8: 成长与估值交互
- **概念名称**: PEG 比率变体
- **定义**: (收入增长率 + 1) / (资产负债率 + 0.1)
- **逻辑含义**: 结合成长性和财务风险的估值指标
- **为何有意义**: 高成长 + 低风险 = 更好的投资机会
- **方向性**: 高比率 = 好
- **边界条件**: 比率 > 10 可能过于乐观
- **数据需求**: `fundamental_revenue_quarterly`, `fundamental_current_liabilities_total`, `fundamental_long_term_debt`, `fundamental_current_assets_total`
- **潜在问题**: 简化版 PEG，未考虑市盈率

### 3.5 结构特征

#### 特征 9: 资产结构
- **概念名称**: 固定资产占比
- **定义**: 固定资产净值 / 总资产
- **逻辑含义**: 度量公司资产结构的轻重程度
- **为何有意义**: 重资产 vs 轻资产模式影响盈利能力和风险
- **方向性**: 视行业而定（制造业高 = 正常，科技业低 = 正常）
- **边界条件**: 占比 > 0.7 = 重资产，< 0.3 = 轻资产
- **数据需求**: `fundamental_property_plant_and_equipment_net`, `fundamental_current_assets_total`
- **潜在问题**: 需要行业分类数据

#### 特征 10: 负债结构
- **概念名称**: 流动负债占比
- **定义**: 流动负债 / 总负债
- **逻辑含义**: 度量公司负债的期限结构
- **为何有意义**: 高流动负债占比 = 短期偿债压力大
- **方向性**: 低占比 = 好
- **边界条件**: 占比 > 0.8 = 短期偿债压力极大
- **数据需求**: `fundamental_current_liabilities_total`, `fundamental_long_term_debt`
- **潜在问题**: 需要计算总负债

### 3.6 累积特征

#### 特征 11: 累积留存收益
- **概念名称**: 留存收益率
- **定义**: 留存收益 / 总资产
- **逻辑含义**: 度量公司历史累积的盈利能力
- **为何有意义**: 高留存收益率 = 历史盈利能力强
- **方向性**: 高比率 = 好
- **边界条件**: 负值 = 历史亏损
- **数据需求**: `fundamental_retained_earnings`, `fundamental_current_assets_total`
- **潜在问题**: 需要处理负值

#### 特征 12: 累积资本支出
- **概念名称**: 资本支出强度
- **定义**: 年度资本支出 / 年度收入
- **逻辑含义**: 度量公司投资强度
- **为何有意义**: 高投资强度可能预示未来增长
- **方向性**: 适度 = 好（过高可能降低 ROE）
- **边界条件**: 强度 > 0.3 = 高投资
- **数据需求**: `fundamental_capital_expenditures_annual`, `fundamental_annual_revenue`
- **潜在问题**: 需要处理零值

### 3.7 相对特征

#### 特征 13: 相对盈利能力
- **概念名称**: ROE 相对排名
- **定义**: 公司 ROE 在行业内的排名
- **逻辑含义**: 度量公司相对于同行的盈利能力
- **为何有意义**: 相对排名比绝对值更有意义
- **方向性**: 高排名 = 好
- **边界条件**: 排名 > 90% = 行业领先
- **数据需求**: `fundamental_income_before_extraordinary_items`, `fundamental_common_equity_total`
- **潜在问题**: 需要使用 rank 算子

#### 特征 14: 相对估值
- **概念名称**: 市净率相对排名
- **定义**: 公司市净率在行业内的排名
- **逻辑含义**: 度量公司相对于同行的估值水平
- **为何有意义**: 低相对估值 = 投资价值
- **方向性**: 低排名 = 好
- **边界条件**: 排名 < 10% = 深度低估
- **数据需求**: `fundamental_common_equity_total`, `fundamental_current_assets_total`
- **潜在问题**: 需要市值数据（可用总资产代替）

### 3.8 本质特征

#### 特征 15: 财务健康综合评分
- **概念名称**: 财务健康指数
- **定义**: 加权综合评分（偿债能力 + 盈利能力 + 运营效率）
- **逻辑含义**: 从第一性原理评估公司财务健康状况
- **为何有意义**: 综合指标比单一指标更全面
- **方向性**: 高评分 = 好
- **边界条件**: 评分 < 0.5 = 财务风险高
- **数据需求**: 多个字段组合
- **潜在问题**: 权重设置需要调优

## 4. 实现考量

### 数据质量说明
1. **覆盖率中等**: 0.5078 表明部分公司数据缺失，需要处理缺失值
2. **VECTOR 字段为主**: 大部分字段需要 vec_avg 聚合后才能用于常规算子
3. **时间维度多样**: 需要统一时间维度（建议用季度数据）

### 覆盖率考量
- **高覆盖率字段** (>0.9): `fundamental_ebitda`, `fundamental_pretax_income`, `fundamental_common_equity_total`
- **中覆盖率字段** (0.5-0.9): `fundamental_current_assets_total`, `fundamental_current_liabilities_total`
- **低覆盖率字段** (<0.5): 部分年度字段和特殊行业字段

### 计算复杂度
- **简单特征**: 直接计算比率（如流动比率、资产负债率）
- **中等特征**: 需要滚动窗口计算（如稳定性、变化率）
- **复杂特征**: 需要多字段组合和非线性变换（如综合评分）

### 潜在改进/扩展
1. **行业中性化**: 使用 SECTOR 中性化消除行业差异
2. **时间序列特征**: 添加趋势、加速度等时间序列特征
3. **机器学习特征**: 使用 PCA、聚类等机器学习方法提取特征

## 5. 进一步探索的关键问题

### 哪些方面尚未覆盖？
1. **行业特异性**: 不同行业的财务特征差异很大，需要行业中性化
2. **时间序列动态**: 需要更深入的时间序列分析（趋势、周期性、结构性变化）
3. **非线性关系**: 财务指标之间可能存在非线性关系

### 哪些额外数据会有帮助？
1. **市场数据**: 市值、估值倍数（PE、PB、PS）
2. **行业数据**: 行业平均财务比率
3. **宏观数据**: 利率、汇率、GDP 增长率

### 哪些假设应被质疑？
1. **线性假设**: 财务指标与股票收益之间可能存在非线性关系
2. **稳定性假设**: 财务比率可能随时间变化（结构性变化）
3. **独立性假设**: 财务指标之间可能存在高度相关性

## 6. Alpha 表达式示例

### 示例 1: 流动比率稳定性
```
rank(vec_avg(fundamental_current_assets_total) / vec_avg(fundamental_current_liabilities_total))
```

### 示例 2: 收入增长率
```
rank(ts_delta(fundamental_revenue_quarterly, 4) / ts_delay(fundamental_revenue_quarterly, 4))
```

### 示例 3: 盈利质量
```
rank(vec_avg(fundamental_operating_activities_net_cash_flow) / vec_avg(fundamental_income_before_extraordinary_items))
```

### 示例 4: 财务健康综合评分
```
rank(
  0.3 * rank(vec_avg(fundamental_current_assets_total) / vec_avg(fundamental_current_liabilities_total)) +
  0.3 * rank(vec_avg(fundamental_income_before_extraordinary_items) / vec_avg(fundamental_common_equity_total)) +
  0.2 * rank(vec_avg(fundamental_operating_activities_net_cash_flow) / vec_avg(fundamental_income_before_extraordinary_items)) +
  0.2 * rank(1 - (vec_avg(fundamental_current_liabilities_total) + vec_avg(fundamental_long_term_debt)) / vec_avg(fundamental_current_assets_total))
)
```

## 7. 总结

fundamental6 数据集是 MEA 区域的一个重要未点亮金字塔，包含 382 个字段，覆盖率 0.5078，金字塔倍数 1.5。该数据集以 VECTOR 字段为主，需要 vec_avg 聚合后才能用于常规算子。

**关键发现**:
1. 数据集涵盖公司基本面数据的全景视图（资产负债表、利润表、现金流量表）
2. 字段类型多样（年度、季度、YTD），需要统一时间维度
3. 覆盖率中等，需要处理缺失值
4. 未点亮金字塔，金字塔倍数 1.5，具有较高的挖掘价值

**推荐策略**:
1. 优先使用高覆盖率字段（>0.9）
2. 使用 vec_avg 聚合 VECTOR 字段
3. 使用 SECTOR 中性化消除行业差异
4. 从简单比率开始，逐步构建复杂特征
5. 重点关注财务质量、盈利能力、偿债能力等核心维度

**预期产出**:
- 10 个满足提交要求的 REGULAR alpha
- sharpe>1.58, fitness>1, 2ysharpe>1.6, margin>5bp
- turnover>5% 且 <30%
- risk_neutralization: sharpe>1, fitness>0.7, margin>5bp
- 生产相关性<0.7
- 彼此相关性<0.4
