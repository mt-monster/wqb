# WQB 数据库全面数据质量评估报告

> **评估日期**: 2026-09-28  
> **数据库**: `data/wqb.db` (SQLite)  
> **表数量**: 18 张表 + 1 个视图  
> **索引数量**: 35+ 个  
> **触发器**: 无  
> **评估脚本**: `tools/_db_quality_check.py` + `tools/_db_semantic_check.py`

---

## 一、表结构审查（字段类型、约束、索引）

### 1.1 表清单与规模

| 表名 | 行数 | 用途 |
|------|------|------|
| `alphas` | 8,914 | Alpha 主表（IS 指标 + 平台状态） |
| `backtest_results` | 8,858 | 回测结果 |
| `expressions` | 66,754 | 表达式池（GEM 产出） |
| `fields` | 263,160 | 字段目录 |
| `field_profile` | 30,705 | 字段画像 |
| `datasets` | 1,877 | 数据集目录 |
| `waves` | 1,279 | 挖掘波次 |
| `wave_results` | 966 | 波次结果 |
| `gate_results` | 1,556 | 门禁结果 |
| `submit_ready` | 106 | 提交就绪队列 |
| `submission_ledger` | 85 | 提交台账 |
| `ledger_kv` | 4,790 | 键值台账 |
| `regions` | 16 | 区域配置 |
| `campaign_state` | 7 | 战役状态 |
| `cross_region_lessons` | 11 | 跨区域经验 |
| `registry_empirical` | 1,024 | 经验注册表 |
| `external_fields` | 24 | 外部字段 |
| `structural_variant_results` | 1 | 结构变体结果 |

### 1.2 字段类型一致性问题

#### `alpha_id` 字段类型不一致

| 表 | 类型 |
|----|------|
| `alphas` | VARCHAR(50) |
| `backtest_results` | VARCHAR(50) |
| `expressions` | VARCHAR(50) |
| `structural_variant_results` | **VARCHAR(100)** |
| `submission_ledger` | VARCHAR(50) |
| `submit_ready` | **TEXT** |

**风险**: `submit_ready.alpha_id` 为 TEXT 类型，与其他表的 VARCHAR(50) 不一致，JOIN 时可能因类型亲和性导致索引失效。`structural_variant_results` 的 VARCHAR(100) 宽度过大。

#### `region` 字段类型不一致

| 表 | 类型 |
|----|------|
| `backtest_results` | TEXT |
| `expressions` | TEXT |
| `external_fields` | TEXT |
| `gate_results` | TEXT |
| `submit_ready` | TEXT |
| `ledger_kv` | VARCHAR(50) |
| `registry_empirical` | VARCHAR(50) |
| `structural_variant_results` | VARCHAR(50) |
| `submission_ledger` | VARCHAR(50) |
| `wave_results` | VARCHAR(50) |

**风险**: region 字段在 10 张表中存在 TEXT vs VARCHAR(50) 两种类型，跨表 JOIN 时 SQLite 类型亲和性可能不匹配，导致全表扫描。

### 1.3 约束与索引

- **主键**: 所有表均有主键（`id` 或 `alpha_id`），设计合理。
- **唯一约束**: 14 张表有唯一约束（如 `alpha_id`、`wave_id+expression`、`region+wave_number` 等），覆盖核心业务键。
- **索引**: 35+ 个索引，覆盖主要查询路径。
- **外键约束**: **未启用**（SQLite 外键需 `PRAGMA foreign_keys=ON`），外键完整性依赖应用层保证。
- **CHECK 约束**: 无。status 等枚举字段无数据库层约束。
- **NOT NULL 约束**: 部分表有，但核心指标字段（sharpe、fitness 等）允许 NULL。

### 1.4 表结构问题总结

| 问题 | 严重度 | 说明 |
|------|--------|------|
| `alpha_id` 类型不一致 | 中 | 6 张表存在 VARCHAR(50)/VARCHAR(100)/TEXT 三种类型 |
| `region` 类型不一致 | 中 | 10 张表存在 TEXT/VARCHAR(50) 两种类型 |
| 无外键约束 | 中 | 外键完整性完全依赖应用层 |
| 无 CHECK 约束 | 低 | status 等枚举字段无数据库层校验 |
| 无触发器 | 低 | 跨表一致性维护需应用层处理 |

---

## 二、数据完整性分析（空值、缺失、重复、外键）

### 2.1 空值统计

#### 高关注表

| 表 | 字段 | 空值数 | 空值率 | 评估 |
|----|------|--------|--------|------|
| `alphas` | `platform_status` | 6,534 | 73.3% | **正常** — 大部分 alpha 未提交 |
| `alphas` | `prod_correlation` | 8,445 | 94.7% | **正常** — 仅提交过的 alpha 有 prod 值 |
| `alphas` | `self_correlation` | 8,552 | 95.9% | **正常** — 同上 |
| `alphas` | `fitness` | 315 | 3.5% | **关注** — 少量 IS 指标缺失 |
| `alphas` | `sharpe` | 126 | 1.4% | **关注** — 少量 IS 指标缺失 |
| `expressions` | `sharpe` | 64,856 | 97.2% | **正常** — 大部分表达式未回测 |
| `expressions` | `alpha_id` | 64,735 | 97.0% | **正常** — 大部分表达式未关联 alpha |
| `datasets` | `tier` | 1,384 | 73.7% | **关注** — 大量数据集无 tier 分类 |
| `datasets` | `status` | 1,110 | 59.1% | **关注** — 数据集状态缺失 |
| `submit_ready` | `expr` | 25 | 23.6% | **关注** — 提交队列中表达式缺失 |
| `waves` | `dataset_id` | 192 | 15.0% | **关注** — 波次未关联数据集 |
| `regions` | `universe_legal` | 6 | 37.5% | **关注** — 区域合法 universe 缺失 |
| `regions` | `delay_legal` | 6 | 37.5% | **关注** — 区域合法 delay 缺失 |

### 2.2 重复数据检查

**所有唯一约束均通过**，无重复数据：

- `alphas.alpha_id` — OK
- `submit_ready.alpha_id+region` — OK
- `expressions.wave_id+expression` — OK
- `waves.region_id+wave_number` — OK
- `wave_results.region+wave_number` — OK
- `datasets.name+region_id` — OK
- `fields.dataset_id+field_name` — OK
- `field_profile.dataset_id+field_name` — OK
- `submission_ledger.alpha_id+submitted_at` — OK
- `ledger_kv.region+key` — OK
- `regions.name` — OK
- `registry_empirical.region+layer+entry_id` — OK
- `gate_results.region+wave+dataset` — OK
- `cross_region_lessons.lesson_id` — OK
- `structural_variant_results.region+wave_number+variant_id` — OK

### 2.3 外键关联问题

| 外键关系 | 状态 | 说明 |
|----------|------|------|
| `alphas.region_id → regions.id` | OK | |
| `alphas.dataset_id → datasets.id` | OK | |
| `backtest_results.expression_id → expressions.id` | OK | |
| `expressions.wave_id → waves.id` | **18 孤儿** | wave_id=0 不在 waves 表 |
| `waves.region_id → regions.id` | OK | |
| `waves.dataset_id → datasets.id` | OK | |
| `fields.dataset_id → datasets.id` | OK | |
| `field_profile.dataset_id → datasets.id` | OK | |
| `campaign_state.region_id → regions.id` | OK | |
| `wave_results.region_id → regions.id` | OK | |

**关键发现**: 18 条 expressions 记录的 `wave_id=0`，在 waves 表中不存在。这些是"孤儿表达式"，可能是早期测试数据或 wave_id 默认值未清理。

### 2.4 跨表一致性问题

| 检查项 | 数量 | 严重度 | 说明 |
|--------|------|--------|------|
| 已提交 alpha 不在 submit_ready | 73 | **高** | 提交台账与主表脱节 |
| submit_ready 中 alpha 不在 alphas 表 | 22 | **高** | 提交队列引用不存在的 alpha |
| expressions 无 backtest_results | 58,398 | 低 | 正常 — 大部分表达式未回测 |
| backtest_results 无 expressions | 0 | OK | |
| waves 无 expressions | 19 | 低 | 空波次 |
| datasets 无 fields | 442 | 低 | 未扫描的数据集 |
| submission_ledger 中 alpha 不在 alphas | 0 | OK | |
| alphas vs submit_ready 状态不一致 | 0 | OK | |

**关键发现**:
- **73 颗已提交 alpha 不在 submit_ready 表中** — 这些 alpha 的 `platform_status` 为 ACTIVE/UNSUBMITTED/DECOMMISSIONED，但 submit_ready 表没有对应记录。可能是提交后未同步，或 submit_ready 仅记录"待提交"队列。
- **22 颗 submit_ready 中的 alpha 不在 alphas 表** — 这些记录引用了不存在的 alpha_id，属于脏数据。

### 2.5 异常值检查

| 检查项 | 数量 | 说明 |
|--------|------|------|
| `alphas.sharpe=NULL` | 126 | IS 指标缺失 |
| `alphas.fitness=NULL` | 315 | IS 指标缺失 |
| `expressions.sharpe=NULL` | 64,856 | 未回测 |
| `submit_ready.sharpe=NULL` | 0 | 正常 |
| `alphas.turnover<0` | 0 | 正常 |
| `alphas.ACTIVE but sharpe<0` | 0 | 正常 |

### 2.6 相同表达式对应多个 alpha_id

发现 **10 组** 相同表达式对应多个 alpha_id 的情况：

| 表达式前缀 | alpha_id 数量 | 说明 |
|------------|---------------|------|
| `probe...` | 16 | 探测性表达式 |
| `R80/R81...` | 16 | 模板变体 |
| `R84/R85...` | 15 | 模板变体 |
| `add(add(rank(ts_mean(...)))...` | 13 | 混合信号 |
| `signed_power(subtract(0.5, ...))...` | 12 | 模板变体 |
| `R93...` | 12 | 模板变体 |
| `R92...` | 12 | 模板变体 |
| `-group_rank(ts_decay_linear(...))...` | 12 | 模板变体 |
| `...` | 12 | 模板变体 |
| `R95...` | 11 | 模板变体 |

**风险**: 相同表达式对应多个 alpha_id 会导致提交时重复，且难以追踪哪个是"正式"版本。

---

## 三、语义清晰度评估（命名规范、字段含义、歧义/冗余）

### 3.1 命名规范

#### 表名单复数一致性

**6 张表使用单数命名**（其他表多为复数）：

| 表名 | 建议 |
|------|------|
| `campaign_state` | 保持单数（状态表，合理） |
| `field_profile` | 保持单数（画像表，合理） |
| `ledger_kv` | 保持单数（键值表，合理） |
| `registry_empirical` | 保持单数（注册表，合理） |
| `submission_ledger` | 保持单数（台账表，合理） |
| `submit_ready` | 保持单数（队列表，合理） |

**评估**: 单数命名用于"状态/画像/台账/队列"类表是合理的，与复数命名的"实体/集合"表形成区分。**无需修改**。

#### 列名规范

- **snake_case**: 所有列名均使用 snake_case，规范统一。
- **缩写字段名**: 存在大量缩写，但属于行业惯例：

| 缩写 | 含义 | 使用表 |
|------|------|--------|
| `prod` | production (correlation) | alphas, submit_ready |
| `self` | self (correlation) | alphas, submit_ready |
| `expr` | expression | submit_ready |
| `corr` | correlation | alphas |
| `os` | out_of_sample | alphas |
| `pnl` | profit_and_loss | backtest_results |

**评估**: 缩写虽多，但在量化金融领域是标准惯例，且字段含义可通过上下文推断。**建议**: 在数据字典中明确记录缩写含义。

### 3.2 冗余/歧义字段

#### 双轨状态字段

| 表 | 字段对 | 说明 |
|----|--------|------|
| `alphas` | `status` vs `platform_status` | **双轨设计** — status=本地模拟状态, platform_status=平台提交状态 |

**评估**: 非冗余但**易混淆**。`status` 表示本地回测流程状态（UNSUBMITTED/COMPLETE/ACTIVE），`platform_status` 表示平台提交状态（None/UNSUBMITTED/ACTIVE/DECOMMISSIONED）。**建议**: 在数据字典中明确区分。

#### submit_ready 与 alphas 数据冗余

| submit_ready 字段 | alphas 对应字段 | 说明 |
|-------------------|-----------------|------|
| `expr` | `expression` | 表达式文本 |
| `sharpe` | `sharpe` | IS Sharpe |
| `fitness` | `fitness` | IS Fitness |
| `turnover` | `turnover` | 换手率 |
| `two_year` | `two_year_sharpe` | 两年 Sharpe |
| `prod` | `prod_correlation` | 生产相关性 |
| `self` | `self_correlation` | 自相关性 |

**评估**: `submit_ready` 表冗余存储了 `alphas` 表的 7 个字段。这是**设计意图** — submit_ready 作为提交队列快照，避免频繁 JOIN。但存在**数据不一致风险**。

**实际不一致情况**:
- **5 颗 alpha 指标不一致** — 均为浮点精度差异（如 `0.3288` vs `0.32880000000000004`），非逻辑错误。
- **5 条表达式不一致** — `expressions.expression` vs `backtest_results.code`，差异在于 `ts_backfill` 包装（如 `rank(ts_backfill(last_event_type_code, 66))` vs `rank(last_event_type_code)`），属于回测时的字段包装差异。

#### 跨表冗余字段

| 字段 | 出现表 | 说明 |
|------|--------|------|
| `region` | expressions, backtest_results, submit_ready, wave_results, ledger_kv, registry_empirical, structural_variant_results, submission_ledger, external_fields, gate_results | 10 张表冗余存储 region |
| `wave` | expressions, backtest_results | 冗余存储 wave_number |
| `dataset` | expressions, backtest_results | 冗余存储 dataset name |
| `code` | backtest_results | 与 expressions.expression 冗余 |

**评估**: 跨表冗余是**反规范化设计**，用于查询性能优化。在 SQLite 单机场景下合理，但需应用层保证一致性。

### 3.3 状态值域

#### `alphas.status` 值域

| 值 | 数量 | 说明 |
|----|------|------|
| `UNSUBMITTED` | 6,394 | 未提交 |
| `COMPLETE` | 2,512 | 回测完成 |
| `ACTIVE` | 8 | 平台活跃 |

#### `alphas.platform_status` 值域

| 值 | 数量 | 说明 |
|----|------|------|
| `None` | 6,534 | 未提交 |
| `UNSUBMITTED` | 2,137 | 已提交未通过 |
| `ACTIVE` | 137 | 平台活跃 |
| `DECOMMISSIONED` | 106 | 已退役 |

#### `submit_ready.status` 值域

| 值 | 数量 | 说明 |
|----|------|------|
| `SUBMITTED` | 65 | 已提交 |
| `DEAD` | 36 | 已死亡 |
| `BLOCKED` | 5 | 被阻断 |

#### `submit_ready.gate` 值域

| 值 | 数量 | 说明 |
|----|------|------|
| `SUBMIT_LAYER_VERIFIED` | 57 | 提交层已验证 |
| `IS_ONLY` | 37 | 仅通过 IS 层 |
| `FAIL:ADD_MIX` | 8 | 混合信号违规 |
| `FAIL:PROD` | 2 | 生产相关性失败 |
| `FAIL:LOW_ROBUST_UNIVERSE_SHARPE` | 1 | 子宇宙 Sharpe 过低 |
| `FAIL:LOW_2Y_SHARPE` | 1 | 两年 Sharpe 过低 |

#### `expressions.status` 值域

| 值 | 数量 | 说明 |
|----|------|------|
| `dropped` | 34,402 | 已丢弃 |
| `gem` | 18,536 | GEM 产出 |
| `superseded` | 8,238 | 被替代 |
| `selected` | 2,335 | 已选中 |
| `backtested` | 1,470 | 已回测 |
| `pending` | 1,450 | 待处理 |
| `gated` | 160 | 门禁通过 |
| `fail` | 88 | 失败 |
| `completed` | 38 | 完成 |
| `submitted` | 31 | 已提交 |
| `coverage` | 6 | 覆盖 |

**评估**: 状态值域清晰，但 `expressions.status` 有 11 种值，状态机较复杂。**建议**: 在数据字典中记录状态流转图。

---

## 四、综合评估与优化建议

### 4.1 数据一致性评估

#### 业务逻辑一致性

| 检查项 | 数量 | 严重度 | 说明 |
|--------|------|--------|------|
| ACTIVE alpha 但 sharpe<1.58 | 12 | **高** | 平台要求 IS Sharpe ≥ 1.58 |
| ACTIVE alpha 但 fitness<1.0 | 4 | **高** | 平台要求 IS Fitness ≥ 1.0 |
| ACTIVE alpha 但 prod>0.7 | 9 | **高** | 平台要求 prod correlation ≤ 0.7 |
| ACTIVE alpha 但 self>0.7 | 4 | **高** | 平台要求 self correlation ≤ 0.7 |

**关键发现**: 存在 **12 颗 ACTIVE alpha 的 IS Sharpe < 1.58**，这些 alpha 虽然平台状态为 ACTIVE，但 IS 指标不满足提交层要求。可能是：
1. 平台提交时指标达标，但后续回测更新导致指标下降
2. 平台提交层校验与 IS 层校验标准不同
3. 数据同步延迟

**建议**: 定期扫描 ACTIVE alpha 的 IS 指标，对不达标的 alpha 进行复核。

#### 跨表一致性

| 检查项 | 数量 | 严重度 |
|--------|------|--------|
| submit_ready vs alphas 指标不一致 | 5 | 低（浮点精度） |
| expressions vs backtest_results 表达式不一致 | 5 | 低（ts_backfill 包装） |
| 已提交 alpha 不在 submit_ready | 73 | **高** |
| submit_ready 中 alpha 不在 alphas | 22 | **高** |

### 4.2 数据准确性评估

#### 浮点精度问题

5 颗 alpha 的 `submit_ready` 与 `alphas` 表指标存在浮点精度差异：

| alpha_id | 字段 | submit_ready | alphas |
|----------|------|---------------|--------|
| xA392Xpb | turnover | 0.3288 | 0.32880000000000004 |
| Vk65zLzG | turnover | 0.12029999999999999 | 0.1203 |
| vRk6og8b | turnover | 0.19030000000000002 | 0.1903 |
| wpZ1vYzY | turnover | 0.3631 | 0.36310000000000003 |
| Wjb9dZ1j | turnover | 0.1692 | 0.16920000000000002 |

**评估**: 这是 SQLite 浮点数存储的固有精度问题，非逻辑错误。**建议**: 在应用层统一使用 `ROUND()` 或格式化输出。

#### 表达式不一致

5 条 `expressions.expression` vs `backtest_results.code` 不一致，差异在于 `ts_backfill` 包装：

| expr_id | expressions.expression | backtest_results.code |
|---------|------------------------|------------------------|
| 7824 | `rank(ts_backfill(last_event_type_code, 66))...` | `rank(last_event_type_code)...` |
| 7825 | `multiply(ts_backfill(next_event_confirmation_level, 66), ...)` | `multiply(next_event_confirmation_level, ...)` |
| 12548 | `rank(subtract(ts_zscore(...), ts_zscore(...)))...` | `rank(subtract(ts_zscore(...), ts_zscore(...)))...` |
| 12638 | `rank(ts_sum(vec_sum(...), 22) / ...)` | `rank(ts_sum(vec_sum(...), 22) / ...)` |
| 12683 | `rank(multiply(ts_zscore(...), ts_zscore(...)))...` | `rank(multiply(ts_zscore(...), ts_zscore(...)))...` |

**评估**: `ts_backfill` 是回测时的字段包装，`expressions` 存储原始表达式，`backtest_results` 存储实际回测代码。**非错误**，但需明确记录这一设计。

### 4.3 潜在风险

| 风险 | 严重度 | 说明 |
|------|--------|------|
| 73 颗已提交 alpha 不在 submit_ready | **高** | 提交台账与主表脱节，可能导致重复提交或遗漏 |
| 22 颗 submit_ready 引用不存在的 alpha | **高** | 脏数据，可能导致提交失败 |
| 18 条孤儿表达式 (wave_id=0) | 中 | 数据清理不彻底 |
| 10 组相同表达式对应多个 alpha_id | 中 | 重复提交风险 |
| 12 颗 ACTIVE alpha IS 指标不达标 | 中 | 平台状态与实际指标不一致 |
| 无外键约束 | 中 | 数据完整性依赖应用层 |
| 无 CHECK 约束 | 低 | 枚举字段无数据库层校验 |

### 4.4 优化建议

#### P0 — 立即修复

1. **清理 submit_ready 中的脏数据**
   - 删除 22 条引用不存在 alpha 的记录
   - 补充 73 颗已提交 alpha 的 submit_ready 记录（或明确 submit_ready 仅记录"待提交"队列的设计意图）

2. **清理孤儿表达式**
   - 删除或修复 18 条 `wave_id=0` 的 expressions 记录

3. **统一 alpha_id 字段类型**
   - 将 `submit_ready.alpha_id` 从 TEXT 改为 VARCHAR(50)
   - 将 `structural_variant_results.alpha_id` 从 VARCHAR(100) 改为 VARCHAR(50)

4. **统一 region 字段类型**
   - 将所有表的 `region` 字段统一为 VARCHAR(50)

#### P1 — 短期优化

5. **添加外键约束**
   - 启用 `PRAGMA foreign_keys=ON`
   - 为核心表添加 FOREIGN KEY 约束

6. **添加 CHECK 约束**
   - 为 `status`、`platform_status` 等枚举字段添加 CHECK 约束
   - 为 `sharpe`、`fitness` 等指标字段添加 `>= 0` 约束

7. **建立数据字典**
   - 记录所有缩写字段的完整含义
   - 记录状态值域和状态流转图
   - 记录双轨状态字段的设计意图

8. **定期数据质量扫描**
   - 将 `tools/_db_quality_check.py` 和 `tools/_db_semantic_check.py` 加入定时任务
   - 每周运行一次，生成数据质量报告

#### P2 — 长期优化

9. **考虑分区表**
   - `expressions` 表有 66,754 行，可考虑按 `wave_id` 分区
   - `fields` 表有 263,160 行，可考虑按 `dataset_id` 分区

10. **添加触发器**
    - 为 `alphas` 表添加触发器，当 `platform_status` 变更时自动更新 `submit_ready`
    - 为 `submit_ready` 表添加触发器，当 `status` 变更时自动同步 `alphas`

11. **数据归档**
    - 对 `expressions` 表中 `status=dropped` 且超过 90 天的记录进行归档
    - 对 `backtest_results` 表中超过 180 天的记录进行归档

---

## 五、评估总结

### 5.1 整体评分

| 维度 | 评分 | 说明 |
|------|------|------|
| 表结构 | 7/10 | 索引完善，但字段类型不一致 |
| 数据完整性 | 6/10 | 唯一约束全部通过，但存在孤儿记录和脏数据 |
| 语义清晰度 | 8/10 | 命名规范统一，但缩写较多需数据字典 |
| 数据一致性 | 6/10 | 存在跨表不一致和指标不达标情况 |
| 数据准确性 | 8/10 | 浮点精度问题非逻辑错误，表达式差异有设计意图 |
| **综合** | **7/10** | 整体良好，需修复 P0 问题 |

### 5.2 关键发现

1. **唯一约束全部通过** — 数据库设计在去重方面做得很好
2. **73 颗已提交 alpha 不在 submit_ready** — 这是最大的数据一致性问题
3. **22 颗 submit_ready 引用不存在的 alpha** — 脏数据需立即清理
4. **12 颗 ACTIVE alpha IS 指标不达标** — 需复核平台状态
5. **字段类型不一致** — `alpha_id` 和 `region` 字段在多个表中类型不统一
6. **无外键约束** — 数据完整性完全依赖应用层

### 5.3 优先行动项

| 优先级 | 行动项 | 预计工作量 |
|--------|--------|------------|
| P0 | 清理 submit_ready 脏数据（22 条） | 10 分钟 |
| P0 | 清理孤儿表达式（18 条） | 5 分钟 |
| P0 | 统一 alpha_id 和 region 字段类型 | 30 分钟 |
| P1 | 添加外键约束和 CHECK 约束 | 1 小时 |
| P1 | 建立数据字典 | 2 小时 |
| P1 | 定期数据质量扫描 | 30 分钟 |
| P2 | 数据归档策略 | 2 小时 |

---

**报告生成时间**: 2026-09-28  
**评估工具**: `tools/_db_quality_check.py` + `tools/_db_semantic_check.py`  
**数据库**: `data/wqb.db`
