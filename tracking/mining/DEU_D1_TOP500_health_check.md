# DEU D1 TOP500 平台实时体检报告
# 生成时间: 2026-08-10
# 工具: MCP get_datasets 全量枚举 + 分category补充
# 三条硬门槛: coverage ≥ 0.85, alphaCount ≤ 50, fieldCount ≥ 10

## 总览
- 总数据集数: ~130+
- 通过三条硬门槛: 11 个
- 零竞争 (alphaCount=0): 1 个
- 超低竞争 (alphaCount≤5): 4 个

## ✅ 白名单 (通过全部三条硬门槛)

按优先级排序 (alphaCount升 → fieldCount降 → coverage降)

排名 | 数据集 | 类别 | Coverage | Fields | AlphaCount | Users | ValueScore | 备注
-----|--------|------|----------|--------|------------|-------|------------|------
1    | fund_holdings_panel  | institutions | 0.9019 | 18  | 0  | 0  | 8.0 | 🎯 零竞争白空间
2    | other455             | other        | 0.9535 | 1500 | 4  | 4  | 7.0 | 🎯 1500字段超大选择空间
3    | model53              | model        | 0.9050 | 22  | 1  | 1  | 7.0 | 信用风险模型
4    | pv29                 | pv           | 1.0000 | 50  | 1  | 1  | 6.0 | 行业分类,完美覆盖
5    | news104              | news         | 0.9630 | 11  | 2  | 2  | 5.0 | 存档新闻数据
6    | other532             | other        | 0.8563 | 8   | 2  | 2  | 7.0 | ⚠ 字段数<10,门槛边缘
7    | pattern_scores       | pv           | 0.9888 | 504 | 7  | 5  | 6.0 | 图表模式识别
8    | institutions6        | institutions | 1.0000 | 11  | 5  | 5  | 6.0 | 完美覆盖
9    | model238             | model        | 0.8552 | 22  | 11 | 5  | 6.0 | SmartHoldings模型
10   | sentiment27          | sentiment    | 0.9038 | 18  | 7  | 5  | 6.0 | 网站热度排名
11   | analyst_earnings_ibes| model        | 0.9978 | 42  | 20 | 12 | 6.0 | IBES分析师盈利预测
12   | model264             | model        | 0.9973 | 380 | 17 | 10 | 6.0 | DL预测数据

## ⚠ 边缘案例 (差一点过门槛)
- model36 (SmartRatios): cov=0.8488, alphaCount=1, fields=20 — 差0.0012未过cov门槛
- model28 (Structural Credit Risk): cov=0.8105, alphaCount=2, fields=25 — cov偏低

## ❌ 关键不达标数据集
- analyst7: cov=0.7207, alphaCount=114 (拥挤)
- analyst_factor_signals: cov=0.5996, alphaCount=116 (拥挤)
- model25: cov=0.6064, alphaCount=79 (拥挤)
- model26: cov=0.5778, alphaCount=28
- model38: cov=0.0 (DEU无覆盖)
- ml_factor_proj: cov=0.0 (DEU无覆盖, EUR可用)
- news_sentiment_nlp: cov=0.0 (DEU无覆盖, EUR/HKG/KOR可用)
- pv1: cov=0.0, alphaCount=535 (极度拥挤)
- techindi_model: cov=0.0, alphaCount=107 (极度拥挤)
- shortinterest3: cov=0.7105, alphaCount=75

## 📊 DEU vs 其他区域对比 (关键差异)
| 数据集 | DEU | EUR | KOR | HKG |
|--------|-----|-----|-----|-----|
| ml_factor_proj | cov=0.0 ❌ | ✅ cov=1.0 | ✅ | ✅ |
| news_sentiment_nlp | cov=0.0 ❌ | ✅ | ✅ | ✅ |
| fund_holdings_panel | cov=0.90 ✅ | ? | ? | ? |
| other455 | cov=0.95 ✅ | ? | ? | ? |
| model53 | cov=0.91 ✅ | ? | ? | ? |

## 🎯 结论
DEU D1 TOP500 有 11 个 qualifying 数据集，头部目标:
1. **fund_holdings_panel** — 零竞争 + valueScore 8.0 + institutions类别
2. **other455** — 1500字段 + alphaCount仅4 + cov 0.95 (超大选择空间)
3. **model53** — credit risk + alphaCount仅1
4. **pv29** — 完美覆盖 + alphaCount仅1