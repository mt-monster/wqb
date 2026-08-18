# 风格多样性评估框架（Style Diversity Evaluation Framework）

> 沉淀日期：2026-08-16
> 适用场景：多轮回测战役（≥10 轮）后的多样性审计、信号族饱和识别、下一轮选波方向决策
> 关联文档：`project_experience_master.md` 第十一章「并行回测填槽模式」、`researcher_workflow/README.md`

---

## 一、为什么需要风格多样性评估

### 1.1 问题背景

在批量回测战役中，容易出现以下盲区：

| 盲区类型 | 表现 | 后果 |
|---------|------|------|
| **骨架同质化** | 同一代数结构反复变参（如 `group_rank(ts_rank(x, d), industry)` 换窗口） | 边际收益≈0，配额浪费 |
| **数据集扎堆** | 过度集中某 1-2 个高 coverage 数据集 | 错过低竞争高价值数据集 |
| **信号族极化** | 全部集中在动量/反转/情绪某一族 | PROD_CORRELATION 结构性墙 |
| **中性化单一** | 只用 INDUSTRY 或只用 SUBINDUSTRY | 错过区域适配最优解 |

### 1.2 评估目标

- **识别饱和区**：已穷尽的风格/骨架/数据集组合，避免重复投入
- **发现空白区**：未点亮金字塔的风格维度，指导下一轮选波
- **量化多样性**：用可度量指标替代"感觉上够多样了"

---

## 二、多样性评估五维模型

每轮（建议每 10 波）从以下五个维度评估已回测 alpha 的分布：

### 2.1 维度一：信号风格（Signal Style）

| 风格类别 | 定义 | 典型算子/结构 | 示例 |
|---------|------|-------------|------|
| **动量 Momentum** | 过去收益预测未来收益 | `ts_delta`, `ts_returns`, `ts_mean` | `rank(ts_delta(close, 20))` |
| **反转 Reversal** | 过度反应后的回归 | `-ts_delta`, `reverse`, `subtract(0, x)` | `rank(subtract(0, ts_delta(close, 5)))` |
| **价值 Value** | 基本面估值偏离 | `group_zscore(P/E, industry)` | `group_zscore(divide(eps, close), industry)` |
| **质量 Quality** | 盈利质量/财务稳健 | `ROE`, `margin`, `accruals` | `group_zscore(ROE, industry)` |
| **情绪 Sentiment** | 分析师/新闻/搜索情绪 | `analyst_sentiment`, `news_sentiment`, `buzz` | `rank(mdl110_analyst_sentiment)` |
| **波动率 Volatility** | IV/RV 及其比率 | `implied_volatility`, `historical_volatility` | `divide(iv_put, iv_call)` |
| **微结构 Microstructure** | 买卖价差/订单流 | `bid_ask_spread`, `dark_pool`, `impact` | `rank(obim_field)` |
| **事件 Event** | 财报/并购/ insider 交易 | `trade_when`, `event_study` | `trade_when(eps_surprise > 0, ...)` |
| **统计套利 StatArb** | 配对/均值回复 | `ts_zscore`, `cointegration` | `ts_zscore(spread, 60)` |
| **机器学习 ML** | 预测模型输出 | `ml_factor`, `prediction` | `rank(ml_factor_proj_field)` |

**评估指标**：
- 各风格 alpha 数量占比
- 各风格最优 sharpe 分布
- **饱和信号**：某风格连续 3 波 sharpe < 1.0 且 PROD > 0.7

### 2.2 维度二：表达式骨架（Expression Skeleton）

| 骨架类型 | 结构特征 | 适用场景 |
|---------|---------|---------|
| **裸字段** | `rank(x)` / `zscore(x)` | 基线测试 |
| **时序变换** | `ts_*(x, d)` | 平滑/动量/波动 |
| **截面排名** | `rank(x)` / `quantile(x)` | 标准化 |
| **分组中性化** | `group_*(x, group)` | 行业/国家中性 |
| **复合结构** | `group_*(ts_*(x, d), group)` | 标准三阶流水线 |
| **事件门控** | `trade_when(cond, x, -1)` | 事件驱动 |
| **多数据集混合** | `add(rank(A), rank(B))` | 信号增强 |

**评估指标**：
- 各骨架使用次数
- 各骨架最优 sharpe
- **饱和信号**：同骨架连续 5 次变参 sharpe 提升 < 0.1

### 2.3 维度三：数据集覆盖（Dataset Coverage）

| 评估项 | 计算方式 | 健康标准 |
|-------|---------|---------|
| 数据集数量 | 已回测数据集总数 | ≥5 个 |
| 字段族覆盖 | 已用字段数 / 数据集总字段数 | ≥30% |
| 区域分布 | 各区域 alpha 数量 | 不过度集中 |
| 金字塔点亮 | 已攻数据集在金字塔层级分布 | 覆盖高/中/低竞争层 |

**饱和信号**：
- 单数据集 alpha 占比 > 40%
- 同数据集连续 3 波 sharpe 递减

### 2.4 维度四：中性化配置（Neutralization）

| 中性化类型 | 适用区域 | 特点 |
|-----------|---------|------|
| MARKET | 全区域 | 最弱中性化 |
| SECTOR | 全区域 | 行业层面 |
| INDUSTRY | 全区域 | 细分行业 |
| SUBINDUSTRY | 全区域 | 最细粒度 |
| COUNTRY | GLB 专用 | 国家层面 |
| STATISTICAL | 特定区域 | 统计中性化 |
| CROWDING | USA 慎用 | 已证 ERROR |
| NONE | 特殊场景 | 无中性化 |

**评估指标**：
- 各中性化使用分布
- 各中性化最优 sharpe
- **区域适配**：KOR 实测 SECTOR 优于 SUBINDUSTRY（见 `project_experience_master.md` 2.4 节）

### 2.5 维度五：参数配置（Parameter Configuration）

| 参数维度 | 取值范围 | 多样性要求 |
|---------|---------|-----------|
| 窗口 d | [5, 22, 66, 120, 240] | 覆盖短/中/长周期 |
| decay | [0, 4, 8, 10, 15] | 覆盖无/低/中/高衰减 |
| 截断 trunc | [0.01, 0.04, 0.08] | 覆盖紧/中/松 |
| 延迟 delay | [0, 1] | D0/D1 双轨 |

---

## 三、多样性评估流程

### 3.1 数据收集

从 `ledger.json` 和 `WAVE_LEDGER.md` 提取：

```json
{
  "wave": 10,
  "total_alphas": 32,
  "alphas": [
    {
      "id": "xxx",
      "expression": "rank(ts_delta(close, 20))",
      "sharpe": 1.2,
      "fitness": 0.8,
      "prod_corr": 0.65,
      "dataset": "mdl110",
      "signal_style": "momentum",
      "skeleton": "timeseries_rank",
      "neutralization": "INDUSTRY",
      "window": 20,
      "decay": 8
    }
  ]
}
```

### 3.2 分布统计

```python
# 伪代码示例
from collections import Counter

style_dist = Counter([a['signal_style'] for a in alphas])
skeleton_dist = Counter([a['skeleton'] for a in alphas])
dataset_dist = Counter([a['dataset'] for a in alphas])
neut_dist = Counter([a['neutralization'] for a in alphas])
```

### 3.3 饱和判定

| 判定规则 | 阈值 | 动作 |
|---------|------|------|
| 风格饱和 | 某风格占比 > 50% 且 sharpe < 1.0 | 暂停该风格，转向其他风格 |
| 骨架饱和 | 同骨架 5 次 sharpe 提升 < 0.1 | 换骨架结构 |
| 数据集饱和 | 单数据集占比 > 40% | 强制引入新数据集 |
| 中性化饱和 | 某中性化 sharpe 显著低于其他 | 换中性化类型 |
| 参数饱和 | 同参数组合 sharpe 递减 | 换参数区间 |

### 3.4 空白识别

**未点亮金字塔清单**：
- 高 coverage 低 alphaCount 数据集（见 `project_experience_master.md` 2.3 节）
- 未尝试的信号风格（如从未测试过微结构）
- 未使用的骨架类型（如从未用 `trade_when`）
- 未覆盖的中性化（如 GLB 未用 COUNTRY）

---

## 四、多样性评估报告模板

每 10 波生成一次独立报告，存档至 `tracking/<REGION>/diversity_reports/`：

```markdown
# 第 N 轮多样性评估报告

## 评估概览
- 评估轮次：第 N 轮（波次 X-Y）
- 已回测 alpha 数：32
- 时间范围：2026-08-10 至 2026-08-16

## 五维分布

### 信号风格分布
| 风格 | 数量 | 占比 | 最优 sharpe | 状态 |
|-----|------|------|------------|------|
| 动量 | 12 | 37.5% | 1.45 | 正常 |
| 反转 | 8 | 25.0% | 0.92 | 偏弱 |
| 情绪 | 6 | 18.8% | 1.58 | 达标 |
| 波动率 | 4 | 12.5% | 2.19 | 达标但 PROD 墙 |
| 价值 | 2 | 6.3% | 0.85 | 不足 |
| 其他 | 0 | 0% | - | **空白** |

### 骨架分布
...

### 数据集分布
...

### 中性化分布
...

### 参数分布
...

## 饱和区判定
- [ ] 风格饱和：波动率族 PROD 0.83-0.91，判死
- [ ] 骨架饱和：`group_rank(ts_rank(x, d), industry)` 已 8 次变参，sharpe 停滞 1.2-1.4
- [ ] 数据集饱和：mdl110 占比 45%，强制转向

## 空白区识别
- [ ] 未尝试风格：微结构、事件、统计套利
- [ ] 未尝试骨架：`trade_when` 事件门控
- [ ] 未尝试数据集：news_sentiment_nlp（valueScore 9.0，alphaCount 0）
- [ ] 未尝试中性化：GLB 的 COUNTRY

## 下一轮选波建议
1. 优先攻击空白风格：微结构（obim 数据集）
2. 强制引入新数据集：news_sentiment_nlp（零竞争）
3. 尝试新骨架：`trade_when` 事件工程
4. 暂停饱和方向：波动率族、mdl110 变参

## 证据链
- 波动率族判死：见 `project_experience_master.md` 附录 C
- 空白数据集清单：见 `project_experience_master.md` 2.3 节
```

---

## 五、与现有流程的集成

### 5.1 与「并行回测填槽模式」的关系

多样性评估是 **选波门** 的输入之一：

```
台账同步门 → 提交前门禁 → N 批同提 → 统一轮询 → 写波结论 → 即收即补
                                    ↓
                            每 10 波多样性评估
                                    ↓
                            更新「下一波决策」
```

### 5.2 与「三层门槛方法论」的关系

| 层级 | 功能 | 多样性评估的作用 |
|-----|------|---------------|
| Tier 1 直接攻 | cov≥0.85 且 alphaCount≤50 | 多样性评估发现 Tier 1 已饱和时，强制转向 Tier 2 |
| Tier 2 回填带 | 0.65≤cov<0.85 且 valueScore≥6 | 多样性评估识别 Tier 2 空白数据集 |
| Tier 3 字段级救援 | 数据集级 cov 低但字段级高 | 多样性评估发现字段级机会 |

### 5.3 与「假设驱动挖掘」的关系

当多样性评估显示模板采样已饱和（同骨架 sharpe 停滞），自动切换到 `researcher_workflow` 的假设驱动模式：

1. 构建 `field_semantics.yaml` 和 `hypothesis_catalog.yaml`
2. 运行 `run_hypothesis_round` 生成 4-alpha 实验
3. 用 `judge()` 判定假设真伪
4. 将验证过的假设纳入多样性评估的「信号风格」维度

---

## 六、实战案例：USA 战役第 10 轮评估

### 6.1 背景
- 已回测 32 个 alpha（波 1-10）
- 主要集中：动量（12）、反转（8）、情绪（6）、波动率（4）、价值（2）

### 6.2 关键发现

| 发现 | 证据 | 决策 |
|-----|------|------|
| 波动率族 PROD 墙 | put/call IV 比率 PROD 0.83-0.91 | 判死，转向情绪/事件 |
| mdl110 饱和 | 占比 45%，sharpe 停滞 1.2-1.4 | 强制转向 news_sentiment_nlp |
| 骨架同质化 | `group_rank(ts_rank(x, d), industry)` 8 次变参 | 引入 `trade_when` 事件门控 |
| 中性化单一 | 全部 INDUSTRY | 尝试 SUBINDUSTRY 和 STATISTICAL |

### 6.3 下一轮行动
1. 攻击 news_sentiment_nlp（零竞争，valueScore 9.0）
2. 尝试 `trade_when` 事件骨架
3. 测试 SUBINDUSTRY 中性化
4. 引入微结构数据集 obim

---

## 七、检查清单（Checklist）

每 10 波执行：

- [ ] 从 `ledger.json` 提取已回测 alpha 元数据
- [ ] 计算五维分布统计
- [ ] 判定饱和区（风格/骨架/数据集/中性化/参数）
- [ ] 识别空白区（未点亮金字塔清单）
- [ ] 生成多样性评估报告
- [ ] 更新 `WAVE_LEDGER.md`「下一波决策」节
- [ ] 更新 `ledger.json` 判死/饱和清单

---

## 八、常见陷阱

| 陷阱 | 表现 | 规避 |
|-----|------|------|
| 伪多样性 | 同骨架换字段名，结构未变 | 骨架判定以代数结构为准，非字段名 |
| 过度分散 | 每波都换新方向，无深度挖掘 | 单方向至少 3 次结构性尝试再判死 |
| 忽视 PROD 墙 | 数值闸门全过但 PROD > 0.8 | 多样性评估必须包含 PROD 分布 |
| 遗忘空白 | 未记录未尝试方向 | 强制维护「未点亮金字塔清单」 |

---

## 九、版本历史

| 日期 | 版本 | 变更 |
|-----|------|------|
| 2026-08-16 | v1.0 | 初始版本，基于 USA 战役第 10 轮评估实践 |

---

## 十、关联文档

- `project_experience_master.md`：总纲，第十一章「并行回测填槽模式」
- `researcher_workflow/README.md`：假设驱动挖掘，多样性饱和后的切换方案
- `WAVE_LEDGER.md`：波次台账，多样性评估的输入数据源
- `ledger.json`：机器伴生台账，判死/饱和清单的存储位置
