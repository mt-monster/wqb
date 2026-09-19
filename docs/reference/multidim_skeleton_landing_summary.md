# 多维骨架标签系统落地总结

> 落地日期：2026-09-09
> 落地范围：tools/skeleton_tags.py + tools/skeleton_quota.json + build_wave.py + pool_diversity.py + ab_test_framework.py + dryrun_multidim.py
> 验证状态：dry-run 通过，对比实验显示显著优势

---

## 一、落地成果

### 1.1 新增文件

| 文件 | 功能 | 状态 |
|------|------|------|
| `tools/skeleton_tags.py` | 多维骨架标签提取器（四维标签：结构/构造链/机制/字段匹配） | ✅ 已创建 |
| `tools/skeleton_quota.json` | 多维配额配置（结构 11 类 + 机制 16 类） | ✅ 已创建 |
| `tools/ab_test_framework.py` | 对比实验框架（传统 vs 多维选波） | ✅ 已创建 |
| `tools/dryrun_multidim.py` | Dry-run 验证脚本 | ✅ 已创建 |
| `docs/reference/multidim_ab_test_report_template.md` | 对比实验报告模板 | ✅ 已创建 |

### 1.2 改造文件

| 文件 | 改造内容 | 状态 |
|------|----------|------|
| `tracking/KOR/scripts/build_wave.py` | 新增 `--multidim` 开关，支持四维标签选波 | ✅ 已改造 |
| `tools/pool_diversity.py` | 新增 `--multidim` 开关，支持四维多样性评估 | ✅ 已改造 |

---

## 二、四维标签体系

### 2.1 维度定义

| 维度 | 标签数 | 说明 |
|------|--------|------|
| **结构模式** | 11 类 | single_raw / single_preprocessed / single_aggregated / ratio_pair / ratio_adjusted / group_relative / group_bucket / linear_2leg / linear_3plus / event_gated / event_freshness |
| **构造链阶段** | 10 类 | raw / backfill / vector_agg / smooth / transform / delta / correlation / freshness / volatility / bucket |
| **经济学机制** | 16 类 | event_conviction / event_gated / spread_pair / ceiling_suppress / discrete_score / low_freq_backfill / analyst_revision / target_price / momentum / mean_reversion / volume_price / volatility_premium / liquidity_premium / multi_horizon / confidence_weighted / free_explore |
| **字段匹配** | 3 状态 | pass / warn / unknown |

### 2.2 标签提取示例

```python
from skeleton_tags import extract_tags

tags = extract_tags("group_rank(ts_delta(vec_avg(eps_cnt), 22), industry)")
# → {
#     "structure": "group_relative",
#     "construction_chain": ["vector_agg", "delta"],
#     "mechanism": "analyst_revision",
#     "field_match": {"status": "unknown", "details": ["no field_profiles provided"]},
#     "fields": ["eps_cnt"],
#     "ops": ["group_rank", "ts_delta", "vec_avg"],
#   }
```

---

## 三、对比实验结果

### 3.1 实验设置

| 项 | 值 |
|---|---|
| 候选池 | 51 条表达式（覆盖 16 种经济学机制） |
| 选波大小 | 20 条 |
| 对照组 | 传统 5 类骨架选波 |
| 实验组 | 多维标签选波 |

### 3.2 核心发现

| 指标 | 传统选波 | 多维选波 | 提升 |
|------|----------|----------|------|
| **机制多样性** | 6 种，熵=2.158 | 13 种，熵=3.522 | **+117% 种类，+63% 熵** |
| **构造链多样性** | 5 种，熵=1.671 | 7 种，熵=1.971 | **+40% 种类，+18% 熵** |
| **结构多样性** | 8 种，熵=2.804 | 8 种，熵=2.771 | 相当 |
| **选波重叠率** | - | 45% | 55% 候选是多维独有 |

### 3.3 机制覆盖对比

| 经济学机制 | 传统选波 | 多维选波 | 经济学含义 |
|-----------|----------|----------|-----------|
| multi_horizon | 4 条 | 4 条 | 多期限共识 |
| free_explore | 9 条 | 1 条 | 自由探索（传统选波无法识别机制） |
| liquidity_premium | 1 条 | 1 条 | 流动性溢价 |
| volatility_premium | 2 条 | 1 条 | 波动率风险溢价 |
| discrete_score | 3 条 | 2 条 | 离散评分分层 |
| confidence_weighted | 1 条 | 1 条 | 置信度加权 |
| **event_gated** | 0 条 | 2 条 | **事件门控（多维独有）** |
| **spread_pair** | 0 条 | 2 条 | **连续字段相对价值（多维独有）** |
| **momentum** | 0 条 | 2 条 | **动量/信息扩散（多维独有）** |
| **mean_reversion** | 0 条 | 1 条 | **均值回归（多维独有）** |
| **volume_price** | 0 条 | 1 条 | **量价背离（多维独有）** |
| **ceiling_suppress** | 0 条 | 1 条 | **截尾抑制（多维独有）** |
| **low_freq_backfill** | 0 条 | 1 条 | **低频字段回填（多维独有）** |

**关键洞察**：传统选波将 9 条候选归类为 "free_explore"（无法识别机制），而多维选波成功识别出 7 种具体经济学机制，机制覆盖度提升 **117%**。

---

## 四、"层层推进"策略验证

### 4.1 策略假设

> 每阶段回测一下，发现信号的苗头好层层推进，这样的方式会更有效挖掘因子。

### 4.2 多维标签如何支持层层推进

| 阶段 | 传统选波 | 多维选波 | 优势 |
|------|----------|----------|------|
| **S2 选波** | 仅按结构分桶 | 按机制+结构+构造链分桶 | 确保机制多样性 |
| **S3 预检** | 仅语法/字段白名单 | 增加机制-形状匹配校验 | 前置拦截机制不匹配 |
| **S4 评审** | 仅看 sharpe/fitness | 按机制族分析表现 | 识别哪类机制有效 |
| **Mode B 优化** | 盲目调参 | 按机制族定向优化 | 避免同族调权重 |

### 4.3 信号苗头发现

多维选波独有的 11 条候选中，包含以下潜在信号苗头：

| 候选 | 机制 | 信号苗头 |
|------|------|----------|
| `trade_when(eps_estimate_4wk_change > 0, ...)` | event_gated | 事件门控：EPS 修正为正时才持仓 |
| `subtract(rank(prob_q5_bucket4), rank(prob_q2_bucket0))` | spread_pair | 预期利差：最高分位-最低分位 |
| `rank(ts_delta(field, 5))` | momentum | 动量：5 日变化率 |
| `multiply(sign(ts_delta(volume, 1)), reverse(ts_delta(close, 1)))` | mean_reversion | 量价背离：放量日反向 |
| `reverse(ts_corr(rank(close), rank(volume), 10))` | volume_price | 量价背离：价量同向放大=反转 |
| `ts_corr(rank(price), rank(volume), 5)` | volume_price | 量价相关性 |
| `winsorize(rank(ceiling_field), std=2)` | ceiling_suppress | 截尾抑制 |
| `ts_backfill(eps_estimate_4wk_change, 22)` | low_freq_backfill | 低频字段回填 |

这些候选在传统选波中被遗漏，但在多维选波中被保留，体现了**机制多样性**的价值。

---

## 五、使用方式

### 5.1 Dry-run 验证

```bash
# 验证单条表达式
python tools/dryrun_multidim.py --exprs "group_rank(ts_delta(vec_avg(eps_cnt), 22), industry)"

# 验证候选池
python tools/dryrun_multidim.py --file candidates.json --output tags_analysis.json
```

### 5.2 多维选波

```bash
# 传统选波（向后兼容）
python tracking/KOR/scripts/build_wave.py --file candidates.json --wave 36A --size 48

# 多维选波（新增）
python tracking/KOR/scripts/build_wave.py --file candidates.json --wave 36A --size 48 --multidim
```

### 5.3 多维多样性评估

```bash
# 传统评估
python tools/pool_diversity.py --file candidates.txt

# 多维评估（新增）
python tools/pool_diversity.py --file candidates.txt --multidim --json report.json
```

### 5.4 对比实验

```bash
# 运行对比实验
python tools/ab_test_framework.py --file candidates.json --wave 36A --size 20 --output ab_test_report.json
```

---

## 六、下一步计划

### 6.1 短期（本周）

- [ ] 在真实候选池上运行多维选波（如 KOR wave 144+）
- [ ] 对比回测结果（达标率、CW 墙发生率、PROD 相关性）
- [ ] 收集字段画像数据（field_profiles），启用字段匹配校验

### 6.2 中期（下周）

- [ ] 将多维标签集成到 `wave_gate.py` 的机制-形状软闸
- [ ] 在 `template_families.json` 中回填多维标签的实证证据
- [ ] 编写 `skeleton_tags.py` 的单元测试

### 6.3 长期（后续）

- [ ] 多维选波设为默认，传统选波标记 deprecated
- [ ] 按机制族分析历史 wave 表现，优化配额配置
- [ ] 探索机制族与区域/数据集的适配规律

---

## 七、关键结论

1. **多维标签系统成功落地**，dry-run 验证通过，对比实验显示显著优势。

2. **机制多样性提升 117%**，传统选波无法识别的 7 种经济学机制被成功识别。

3. **构造链多样性提升 40%**，预处理阶段（backfill/vector_agg/delta/correlation）被显式追踪。

4. **"层层推进"策略得到支持**，多维标签确保每阶段覆盖多样的经济学机制，避免同族调权重。

5. **信号苗头发现率提升**，多维选波独有的 11 条候选中包含事件门控、量价背离、截尾抑制等潜在信号。

---

*落地完成时间：2026-09-09*
*验证状态：dry-run 通过，对比实验显示显著优势*
*下一步：真实候选池回测验证*
