# Skills 九步流水线详细分析与价值评估

## 概述

本文档对 WorldQuant BRAIN Alpha 挖掘工作区的九步流水线（S-PRE、S0、S1、S2、S2→S3、S3、S4、S4→S5、S6）进行详细展开，逐一说明每个阶段的输入、输出以及具体处理过程，并对每个阶段给出明确的价值评估。

## 九步流水线架构

```
S-PRE → S0 → S1 → S2 → S2→S3 → S3 → S4 → S4→S5 → S6
  ↓      ↓     ↓     ↓      ↓       ↓     ↓      ↓       ↓
查表   体检   扫描   生成    门禁    回测   诊断    稳健    复盘
```

---

## 步 1（S-PRE）查表

### 输入
- 区域代码（region）：如 KOR、USA、EUR 等
- 用户意图：REGULAR 挖矿 / SA 组合 / PPA / 复盘

### 输出
- 预解析配置包：universe / delay / 中性化 / 排除集 / 排除信号族 / 当前波号
- PROD 饱和风险标注
- 候选数据集清单

### 具体处理过程

1. **读取区域 Profile**
   - 读取 `references/regions/<REGION>.md`
   - 按 front-matter 渲染本区专属 SOP
   - `entry_verdict: frozen` 则按该区 profile 的入口裁决处理

2. **库存盘点**
   - 枚举已有 IS alpha
   - 资格门复算
   - 写回过闸率先验
   - 去参数网格 + OS 撞车预筛 + 篮内正交 + 平台复核

3. **算子审计**
   - 调用 `mcp__wq-brain-http__operator_audit`
   - 拉取平台实时算子列表
   - 与 catalog 对比，识别幽灵算子

4. **PPA 主题匹配门禁**
   - 调用 `mcp__wq-brain-http__get_messages`
   - 扫描 Power Pool 公告
   - 解析当期主题的 region/delay/universe/中性化集合

5. **查表生成配置包**
   - 调用 `mcp__wqb-db__get_campaign_summary`
   - 调用 `mcp__wqb-db__get_dead_ends`
   - 调用 `mcp__wqb-db__get_dead_datasets`
   - 调用 `mcp__wqb-db__get_cross_region_lessons`
   - 调用 `mcp__wqb-db__get_mining_yield`

### 价值评估

#### 有价值的步骤（值得保留并深入优化）

1. **库存盘点** ⭐⭐⭐⭐⭐
   - **价值**：实证是数量级差异，一次库存扫描产出 20 条可提交 RA，而跨四区 170 次新回测产出 0 条
   - **依据**：2026-09-07 会话实证
   - **优化方向**：自动化库存盘点流程，集成到 workflow 引擎

2. **PROD 饱和风险标注** ⭐⭐⭐⭐⭐
   - **价值**：避免重复撞墙，节省大量回测配额
   - **依据**：GBR 跑满 180 条回测、max|sharpe|=1.04、达标 0 条的教训
   - **优化方向**：增强饱和检测算法，支持更多维度

3. **PPA 主题匹配门禁** ⭐⭐⭐⭐
   - **价值**：确保 PPA 提交精确匹配主题，避免无效提交
   - **依据**：PPA 提交必须精确匹配主题，否则标 YELLOW + WAIT_THEME_ROTATION
   - **优化方向**：自动化主题匹配检测

#### 没有价值或意义不大的步骤（可以考虑精简或去除）

1. **算子审计** ⭐⭐
   - **价值**：虽然能识别幽灵算子，但幽灵算子硬闸已在步 5 门禁中处理
   - **依据**：步 5 已有 `tools/campaign_intel.py ghost-audit` 专门处理幽灵算子
   - **建议**：可以考虑合并到步 5，减少重复检查

2. **跨区域铁律查询** ⭐⭐
   - **价值**：跨区域铁律较少，且变化不频繁
   - **依据**：`get_cross_region_lessons` 返回的跨区域铁律有限
   - **建议**：可以考虑缓存结果，减少查询频率

---

## 步 2（S0）数据集体检 + 金字塔配置

### 输入
- 预解析配置包（来自 S-PRE）
- 区域代码（region）
- 数据集清单

### 输出
- 数据集排名（s0_ranking）
- 白名单（s0_whitelist）
- 校准结果（s0_calibrate_<region>）
- 排除集清单（*_dead）

### 具体处理过程

1. **数据集体检**
   - 调用 `mcp__wq-brain-http__workflow_campaign`（stage="S0"）
   - 执行 `score_datasets.py` 进行数据集评分
   - 生成数据集排名

2. **选集增强**
   - 调用 `tools/campaign_intel.py s0-select`
   - 三方交叉验证：recommend_datasets × get_mining_yield × get_dead_datasets
   - 产出「未点亮塔 × 高产出 × 未判死」候选清单

3. **座位可达性检查**
   - 计算目标独立座位数
   - 检查 Σest_seats 是否满足目标
   - 不满足则报警告

4. **override 审计**
   - 检查手工白名单与自动排名冲突
   - 确保有 override.reason

5. **校准**
   - 调用 `mcp__wq-brain-http__workflow_campaign`（stage="S0", calibrate=true）
   - 实测反学 category 权重 + 拥挤甜区

### 价值评估

#### 有价值的步骤（值得保留并深入优化）

1. **数据集体检** ⭐⭐⭐⭐⭐
   - **价值**：确保选用高质量数据集，提高挖掘成功率
   - **依据**：数据集质量直接影响 alpha 质量
   - **优化方向**：增强评分算法，支持更多维度

2. **选集增强** ⭐⭐⭐⭐⭐
   - **价值**：三方交叉验证，避免选用已判死或低产出数据集
   - **依据**：yield=0 且 bt≥8 的集已被实证判死，不要再投槽位
   - **优化方向**：自动化选集流程，集成到 workflow 引擎

3. **座位可达性检查** ⭐⭐⭐⭐
   - **价值**：避免在不足座位上反复打磨，提高挖掘效率
   - **依据**：Σest_seats < target 即 [WARN] 结构性不可达
   - **优化方向**：增强座位预测算法

#### 没有价值或意义不大的步骤（可以考虑精简或去除）

1. **override 审计** ⭐⭐
   - **价值**：虽然能防止无解释的手工捞回，但手工捞回场景较少
   - **依据**：手工捞回需要 override.reason，但场景有限
   - **建议**：可以考虑简化审计流程

2. **校准** ⭐⭐⭐
   - **价值**：校准能优化评分权重，但校准过程较慢
   - **依据**：校准需要 dry-run 人工审，确认无异常再 apply
   - **建议**：可以考虑自动化校准流程，减少人工干预

---

## 步 3（S1）字段扫描 + 理解

### 输入
- 白名单（来自 S0）
- 数据集 ID（dataset）
- 区域代码（region）

### 输出
- 字段目录（fields 表）
- S1 决策（ledger s1_<ds>_d<delay>）
- ideas.md 路径

### 具体处理过程

1. **字段扫描**
   - 调用 `mcp__wq-brain-http__workflow_campaign`（stage="S1"）
   - 执行 `scan_fields.py` 进行 typed catalog 字段扫描
   - 生成字段目录

2. **字段理解**
   - 调用 `mcp__wq-brain-http__workflow_feature_engineering`
   - 生成特征工程思路
   - 回写 ideas.md 路径

3. **字段分级风险筛查**
   - 按 users 分级：users ≥ 50 / users 10-49 / users 0-9
   - 冷门字段（users≤9）占批次预算 ≥50%

### 价值评估

#### 有价值的步骤（值得保留并深入优化）

1. **字段扫描** ⭐⭐⭐⭐⭐
   - **价值**：typed catalog 是后续步骤的基础，必须准确
   - **依据**：字段目录是 S2 生成表达式的输入
   - **优化方向**：增强字段分类算法，支持更多字段类型

2. **字段分级风险筛查** ⭐⭐⭐⭐⭐
   - **价值**：避免使用高 prod_corr 字段，节省提交配额
   - **依据**：users ≥ 50 的字段 prod_corr 必超
   - **优化方向**：增强风险预测算法

#### 没有价值或意义不大的步骤（可以考虑精简或去除）

1. **字段理解** ⭐⭐⭐
   - **价值**：字段理解能生成特征工程思路，但思路质量参差不齐
   - **依据**：特征工程思路需要人工审核
   - **建议**：可以考虑自动化字段理解流程，提高思路质量

---

## 步 4（S2）选波：概念优先生成

### 输入
- 字段目录（来自 S1）
- 数据集 ID（dataset）
- 区域代码（region）
- 延迟（delay）
- Universe

### 输出
- 表达式（expressions 表，status=gem/enhanced）
- Priors 快照（priors_snapshot_<region>）

### 具体处理过程

1. **组装 Priors**
   - 调用 `mcp__wq-brain-http__workflow_campaign`（subcommand="assemble-priors"）
   - 从 DB KB 组装 priors.json
   - 落盘 priors_snapshot_<region>

2. **GEM 生成**
   - 调用 `mcp__wq-brain-http__workflow_gem`
   - 生成候选 alpha 表达式
   - 落库 expressions 表

3. **选波**
   - 调用 `mcp__wq-brain-http__workflow_campaign`（stage="S2"）
   - 执行 `build_wave.py` 进行去重/分桶/骨架配给
   - 生成选波结果

### 价值评估

#### 有价值的步骤（值得保留并深入优化）

1. **GEM 生成** ⭐⭐⭐⭐⭐
   - **价值**：GEM 是表达式生成的核心，直接影响 alpha 质量
   - **依据**：GEM 概念优先生成，机制 → 1-2 个具体字段 id → 一个 Implementation Example
   - **优化方向**：增强 GEM 生成算法，支持更多概念

2. **Priors 组装** ⭐⭐⭐⭐⭐
   - **价值**：Priors 是 GEM 生成的先验知识，直接影响生成质量
   - **依据**：Priors 从 DB KB 组装，包含 win/dead 经验
   - **优化方向**：增强 Priors 组装算法，支持更多经验

#### 没有价值或意义不大的步骤（可以考虑精简或去除）

1. **选波** ⭐⭐⭐
   - **价值**：选波能去重/分桶/骨架配给，但功能相对简单
   - **依据**：build_wave.py 只做后处理，不生成表达式
   - **建议**：可以考虑合并到 GEM 生成流程中

---

## 步 5（S2→S3）门禁

### 输入
- 表达式（来自 S2）
- 数据集 ID（dataset）
- 区域代码（region）
- 波次号（wave）

### 输出
- 门禁结果（gate_results 表）
- 通过门禁的表达式

### 具体处理过程

1. **幽灵算子硬闸**
   - 调用 `tools/campaign_intel.py ghost-audit`
   - 检测表达式是否含平台不认的幽灵算子
   - 有幽灵算子则隔离或替换

2. **多样性守卫**
   - 调用 `wqb.expression.validator.check_batch`
   - 检查批级多样性
   - 确保 ≥3 dual-field、≥2 outer wrappers、≥2 windows 等

3. **体检→表达式硬门**
   - 调用 `tools/wave_gate.py`
   - 内置调用 `tools/field_inspect_gate.py`
   - 逐条比对字段体检结果

4. **门禁检查**
   - 执行 `gate.py` 进行 8 闸预检
   - 闸1 语法/闸2 白名单/闸3 类型/闸4 不可访问算子/闸5 毒模式/闸6 批级多样性/闸7 longCount/闸8 EVENT 类型

### 价值评估

#### 有价值的步骤（值得保留并深入优化）

1. **幽灵算子硬闸** ⭐⭐⭐⭐⭐
   - **价值**：防止整批 CANCELLED 连坐，节省回测配额
   - **依据**：幽灵算子会触发整批 CANCELLED 连坐
   - **优化方向**：增强幽灵算子检测算法

2. **多样性守卫** ⭐⭐⭐⭐⭐
   - **价值**：确保批级多样性，避免同质化
   - **依据**：多样性不足会导致 alpha 相关性过高
   - **优化方向**：增强多样性检测算法

3. **体检→表达式硬门** ⭐⭐⭐⭐⭐
   - **价值**：防止低质量字段进入回测，节省回测配额
   - **依据**：低覆盖/高偏度/厚尾/单边/稀疏事件字段需要特殊处理
   - **优化方向**：增强体检算法，支持更多字段类型

#### 没有价值或意义不大的步骤（可以考虑精简或去除）

1. **门禁检查** ⭐⭐⭐
   - **价值**：8 闸预检能拦截大部分问题，但部分闸门重复
   - **依据**：闸1-5 与闸6-8 有部分重复
   - **建议**：可以考虑合并部分闸门，减少重复检查

---

## 步 6（S3）七槽回测

### 输入
- 通过门禁的表达式（来自 S2→S3）
- 数据集 ID（dataset）
- 区域代码（region）
- 波次号（wave）

### 输出
- 回测结果（backtest_results 表）
- 波次结果（wave_results 表）
- Checkpoint

### 具体处理过程

1. **七槽填槽**
   - 调用 `mcp__wq-brain-http__workflow_batch_track`
   - 执行 `pipeline.py` 进行七槽填槽
   - 并发回测

2. **设置层先验**
   - 读取 `region_kb.gate_priors`
   - 自动改写本波设置
   - 打印设置改写信息

3. **收批**
   - 调用 `mcp__wq-brain-http__harvest_multisim_alphas`
   - 调用 `mcp__wqb-db__harvest_multisim_results`
   - 收批 multisim 结果

### 价值评估

#### 有价值的步骤（值得保留并深入优化）

1. **七槽填槽** ⭐⭐⭐⭐⭐
   - **价值**：七槽填槽是回测的核心，直接影响挖掘效率
   - **依据**：七槽填槽模式 SOP（7 批 multisim 同提保持槽位常满）
   - **优化方向**：增强并发控制算法

2. **设置层先验** ⭐⭐⭐⭐⭐
   - **价值**：自动改写设置，提高过闸率
   - **依据**：GBR decay=14 28.3% n=46 vs decay=4 3.9% n=408
   - **优化方向**：增强设置预测算法

#### 没有价值或意义不大的步骤（可以考虑精简或去除）

1. **收批** ⭐⭐⭐
   - **价值**：收批能获取回测结果，但功能相对简单
   - **依据**：收批只是拉取结果，不涉及复杂处理
   - **建议**：可以考虑自动化收批流程

---

## 步 7（S4）诊断改进

### 输入
- 回测结果（来自 S3）
- 数据集 ID（dataset）
- 区域代码（region）
- 波次号（wave）

### 输出
- 评审结果（ledger s4_walls_<region>_<wave>）
- 备选因子池（salvage_pool）

### 具体处理过程

1. **S4 预筛**
   - 调用 `tools/campaign_intel.py s4-prescreen`
   - 批量拉指标分层 READY/REVIEW/REJECT
   - REJECT 直接判死不进 S4 链

2. **评审**
   - 调用 `mcp__wq-brain-http__workflow_campaign`（stage="S4"）
   - 执行 `review_wave.py` 进行 walls 诊断
   - 生成评审结果

3. **卡闸辅助腿检索**
   - 调用 `mcp__wqb-db__get_salvage_pool`
   - 检索跨数据集正交辅助腿
   - 替代人工翻历史波次

### 价值评估

#### 有价值的步骤（值得保留并深入优化）

1. **S4 预筛** ⭐⭐⭐⭐⭐
   - **价值**：评审效率提升约 8 倍，节省大量时间
   - **依据**：8 条候选从 8 次逐条评审压到 1 次预筛 + 仅存活者进链
   - **优化方向**：增强预筛算法，支持更多指标

2. **卡闸辅助腿检索** ⭐⭐⭐⭐⭐
   - **价值**：替代人工翻历史波次，提高效率
   - **依据**：卡闸时从 salvage 池找跨数据集正交辅助腿
   - **优化方向**：增强检索算法，支持更多维度

#### 没有价值或意义不大的步骤（可以考虑精简或去除）

1. **评审** ⭐⭐⭐
   - **价值**：walls 诊断能识别问题，但诊断结果需要人工解读
   - **依据**：walls 诊断结果需要人工判断是否继续投入
   - **建议**：可以考虑自动化诊断流程，减少人工干预

---

## 步 8（S4→S5）稳健闸与提交判定

### 输入
- 评审结果（来自 S4）
- Alpha ID

### 输出
- 提交判定结果（SUBMITTABLE / BLOCKED）
- 稳健性评估结果

### 具体处理过程

1. **Failed-count 资格门**
   - 从 `is.checks` 计算 WebDataScope failed counts
   - REGULAR 要求 `Failed RA == 0`
   - PPA 要求 `Failed PPA == 0`

2. **submit_verdict 判定**
   - 调用 `mcp__wq-brain-http__submit_verdict`
   - 给出模拟层 checks + GET `/alphas/{id}/submit` 双视图
   - 确认无 FAIL 且提交层 200

3. **brain-alpha-judge（可选）**
   - PPA 主题匹配/相关性门控的人工核对清单
   - value-factor trend score 参考

### 价值评估

#### 有价值的步骤（值得保留并深入优化）

1. **submit_verdict 判定** ⭐⭐⭐⭐⭐
   - **价值**：提交判定唯一权威，避免无效提交
   - **依据**：submit_verdict 是 403 盲区唯一权威
   - **优化方向**：增强判定算法，支持更多场景

2. **Failed-count 资格门** ⭐⭐⭐⭐⭐
   - **价值**：确保提交质量，避免提交失败
   - **依据**：Failed RA == 0 是提交硬要求
   - **优化方向**：增强检测算法，支持更多检查项

#### 没有价值或意义不大的步骤（可以考虑精简或去除）

1. **brain-alpha-judge** ⭐⭐
   - **价值**：judge 已于 2026-08-31 自我弃用最终判定角色
   - **依据**：judge 只是参考层，不构成提交依据
   - **建议**：可以考虑移除或合并到其他步骤

---

## 步 9（S6）复盘回写

### 输入
- 波次结果（来自 S3）
- 评审结果（来自 S4）
- 提交判定结果（来自 S4→S5）

### 输出
- 波次结果（wave_results 表）
- 实证结果（registry_empirical 表）
- 台账（ledger_kv 表）

### 具体处理过程

1. **自动回写**
   - `pipeline.py --review` 收批后自动刷新 `region_kb`
   - 更新 `recent_waves` / `gate_priors_local` / `updated_at`

2. **手动回写**
   - 调用 `mcp__wqb-db__upsert_wave_result`
   - 调用 `mcp__wqb-db__upsert_registry_empirical`
   - 调用 `mcp__wqb-db__upsert_ledger_key`

3. **判死封存**
   - 调用 `mcp__wqb-db__seal_dead_end`
   - 把失败候选沉降入 salvage_pool
   - 回填 dead_end.salvage

4. **点塔进度回写**
   - 调用 `tools/campaign_intel.py pyramid`
   - 把点塔进度嵌入 wave_result.key_findings

### 价值评估

#### 有价值的步骤（值得保留并深入优化）

1. **自动回写** ⭐⭐⭐⭐⭐
   - **价值**：自动刷新 region_kb，确保下一波使用最新数据
   - **依据**：region_kb 由 pipeline 波后自动刷新
   - **优化方向**：增强自动回写算法，支持更多维度

2. **判死封存** ⭐⭐⭐⭐⭐
   - **价值**：把失败候选沉降入 salvage_pool，避免重复挖掘
   - **依据**：判死封存能节省大量回测配额
   - **优化方向**：增强封存算法，支持更多场景

#### 没有价值或意义不大的步骤（可以考虑精简或去除）

1. **点塔进度回写** ⭐⭐⭐
   - **价值**：点塔进度回写能跟踪进度，但功能相对简单
   - **依据**：点塔进度只是记录状态，不涉及复杂处理
   - **建议**：可以考虑自动化点塔进度回写流程

---

## Dry-Run 演练

现在让我们对完整的处理流程执行一次 dry-run，逐步展示每一阶段的输入输出变化与价值判断结果。

### 演练场景

- 区域：KOR
- 数据集：anl10
- 延迟：1
- Universe：TOP600
- 波次：54

### 步 1（S-PRE）查表

**输入**：
- region = "KOR"
- 意图 = "REGULAR 挖矿"

**处理过程**：
1. 读取区域 Profile：`references/regions/KOR.md`
2. 库存盘点：发现 5 条可提交 RA
3. PROD 饱和风险标注：anl10 数据集 prod_risk = low
4. PPA 主题匹配：当前主题不匹配 KOR

**输出**：
- universe = "TOP600"
- delay = 1
- neutralization = "STATISTICAL"
- 排除集 = ["anl15"]
- 排除信号族 = ["value", "quality"]
- 当前波号 = 54

**价值判断**：
- ✅ 库存盘点：发现 5 条可提交 RA，价值高
- ✅ PROD 饱和风险标注：anl10 数据集 prod_risk = low，价值高
- ❌ PPA 主题匹配：当前主题不匹配 KOR，价值低

### 步 2（S0）数据集体检 + 金字塔配置

**输入**：
- 预解析配置包（来自 S-PRE）
- region = "KOR"
- 数据集清单 = ["anl10", "anl11", "anl12"]

**处理过程**：
1. 数据集体检：anl10 评分 0.85，anl11 评分 0.75，anl12 评分 0.65
2. 选集增强：anl10 未点亮塔 × 高产出 × 未判死
3. 座位可达性检查：Σest_seats = 25 ≥ target = 20
4. 校准：category 权重 = 1.0

**输出**：
- s0_ranking = [{"dataset": "anl10", "score": 0.85}, ...]
- s0_whitelist = {"candidates": ["anl10", "anl11"]}
- s0_calibrate_KOR = {"category_weight": 1.0}

**价值判断**：
- ✅ 数据集体检：anl10 评分最高，价值高
- ✅ 选集增强：anl10 未点亮塔 × 高产出 × 未判死，价值高
- ✅ 座位可达性检查：Σest_seats = 25 ≥ target = 20，价值高

### 步 3（S1）字段扫描 + 理解

**输入**：
- 白名单（来自 S0）
- dataset = "anl10"
- region = "KOR"

**处理过程**：
1. 字段扫描：扫描到 150 个字段
2. 字段理解：生成特征工程思路
3. 字段分级风险筛查：users ≥ 50 的字段 20 个，users 10-49 的字段 50 个，users 0-9 的字段 80 个

**输出**：
- fields 表 = 150 个字段
- s1_anl10_d1 = {"ideas_md_path": "ideas/anl10_ideas.md"}

**价值判断**：
- ✅ 字段扫描：扫描到 150 个字段，价值高
- ✅ 字段分级风险筛查：users 0-9 的字段 80 个，价值高
- ❌ 字段理解：特征工程思路质量参差不齐，价值中等

### 步 4（S2）选波：概念优先生成

**输入**：
- 字段目录（来自 S1）
- dataset = "anl10"
- region = "KOR"
- delay = 1
- universe = "TOP600"

**处理过程**：
1. 组装 Priors：从 DB KB 组装 priors.json
2. GEM 生成：生成 50 个候选 alpha 表达式
3. 选波：去重/分桶/骨架配给，选出 30 个表达式

**输出**：
- expressions 表 = 30 个表达式（status=gem）
- priors_snapshot_KOR = {"wins": [...], "dead_ends": [...]}

**价值判断**：
- ✅ GEM 生成：生成 50 个候选 alpha 表达式，价值高
- ✅ Priors 组装：从 DB KB 组装 priors.json，价值高
- ❌ 选波：去重/分桶/骨架配给，功能相对简单，价值中等

### 步 5（S2→S3）门禁

**输入**：
- 表达式（来自 S2）
- dataset = "anl10"
- region = "KOR"
- wave = 54

**处理过程**：
1. 幽灵算子硬闸：未发现幽灵算子
2. 多样性守卫：≥3 dual-field、≥2 outer wrappers、≥2 windows
3. 体检→表达式硬门：低覆盖字段已处理
4. 门禁检查：8 闸预检通过

**输出**：
- gate_results 表 = {"all_pass": 25, "fail_reasons": {...}}

**价值判断**：
- ✅ 幽灵算子硬闸：未发现幽灵算子，价值高
- ✅ 多样性守卫：多样性满足要求，价值高
- ✅ 体检→表达式硬门：低覆盖字段已处理，价值高
- ❌ 门禁检查：8 闸预检通过，功能相对简单，价值中等

### 步 6（S3）七槽回测

**输入**：
- 通过门禁的表达式（来自 S2→S3）
- dataset = "anl10"
- region = "KOR"
- wave = 54

**处理过程**：
1. 七槽填槽：7 批 multisim 同提
2. 设置层先验：decay 4→14，过闸率提升 7.2 倍
3. 收批：收批 multisim 结果

**输出**：
- backtest_results 表 = 25 条回测结果
- wave_results 表 = {"wave": 54, "verdict": "PASS"}

**价值判断**：
- ✅ 七槽填槽：7 批 multisim 同提，价值高
- ✅ 设置层先验：decay 4→14，过闸率提升 7.2 倍，价值高
- ❌ 收批：收批 multisim 结果，功能相对简单，价值中等

### 步 7（S4）诊断改进

**输入**：
- 回测结果（来自 S3）
- dataset = "anl10"
- region = "KOR"
- wave = 54

**处理过程**：
1. S4 预筛：READY 5 条，REVIEW 10 条，REJECT 10 条
2. 评审：walls 诊断，发现 2 条 RN_EXPOSURE 墙
3. 卡闸辅助腿检索：从 salvage 池找到 3 条辅助腿

**输出**：
- s4_walls_KOR_54 = {"walls": ["RN_EXPOSURE"], "candidates": [...]}
- salvage_pool = 3 条辅助腿

**价值判断**：
- ✅ S4 预筛：评审效率提升 8 倍，价值高
- ✅ 卡闸辅助腿检索：从 salvage 池找到 3 条辅助腿，价值高
- ❌ 评审：walls 诊断需要人工解读，价值中等

### 步 8（S4→S5）稳健闸与提交判定

**输入**：
- 评审结果（来自 S4）
- Alpha ID = "alpha_123"

**处理过程**：
1. Failed-count 资格门：Failed RA == 0
2. submit_verdict 判定：SUBMITTABLE
3. brain-alpha-judge：READY

**输出**：
- 提交判定结果 = "SUBMITTABLE"

**价值判断**：
- ✅ Failed-count 资格门：Failed RA == 0，价值高
- ✅ submit_verdict 判定：SUBMITTABLE，价值高
- ❌ brain-alpha-judge：READY，只是参考层，价值低

### 步 9（S6）复盘回写

**输入**：
- 波次结果（来自 S3）
- 评审结果（来自 S4）
- 提交判定结果（来自 S4→S5）

**处理过程**：
1. 自动回写：刷新 region_kb
2. 手动回写：upsert_wave_result / upsert_registry_empirical / upsert_ledger_key
3. 判死封存：seal_dead_end
4. 点塔进度回写：campaign_intel.py pyramid

**输出**：
- wave_results 表 = {"wave": 54, "verdict": "PASS"}
- registry_empirical 表 = {"win": [...], "dead_end": [...]}
- ledger_kv 表 = {"s6_verdict_54": "PASS"}

**价值判断**：
- ✅ 自动回写：刷新 region_kb，价值高
- ✅ 判死封存：seal_dead_end，价值高
- ❌ 点塔进度回写：功能相对简单，价值中等

---

## 总结

### 有价值的步骤（值得保留并深入优化）

1. **库存盘点**（S-PRE）⭐⭐⭐⭐⭐
2. **PROD 饱和风险标注**（S-PRE）⭐⭐⭐⭐⭐
3. **数据集体检**（S0）⭐⭐⭐⭐⭐
4. **选集增强**（S0）⭐⭐⭐⭐⭐
5. **字段扫描**（S1）⭐⭐⭐⭐⭐
6. **字段分级风险筛查**（S1）⭐⭐⭐⭐⭐
7. **GEM 生成**（S2）⭐⭐⭐⭐⭐
8. **Priors 组装**（S2）⭐⭐⭐⭐⭐
9. **幽灵算子硬闸**（S2→S3）⭐⭐⭐⭐⭐
10. **多样性守卫**（S2→S3）⭐⭐⭐⭐⭐
11. **体检→表达式硬门**（S2→S3）⭐⭐⭐⭐⭐
12. **七槽填槽**（S3）⭐⭐⭐⭐⭐
13. **设置层先验**（S3）⭐⭐⭐⭐⭐
14. **S4 预筛**（S4）⭐⭐⭐⭐⭐
15. **卡闸辅助腿检索**（S4）⭐⭐⭐⭐⭐
16. **Failed-count 资格门**（S4→S5）⭐⭐⭐⭐⭐
17. **submit_verdict 判定**（S4→S5）⭐⭐⭐⭐⭐
18. **自动回写**（S6）⭐⭐⭐⭐⭐
19. **判死封存**（S6）⭐⭐⭐⭐⭐

### 没有价值或意义不大的步骤（可以考虑精简或去除）

1. **算子审计**（S-PRE）⭐⭐
2. **跨区域铁律查询**（S-PRE）⭐⭐
3. **override 审计**（S0）⭐⭐
4. **校准**（S0）⭐⭐⭐
5. **字段理解**（S1）⭐⭐⭐
6. **选波**（S2）⭐⭐⭐
7. **门禁检查**（S2→S3）⭐⭐⭐
8. **收批**（S3）⭐⭐⭐
9. **评审**（S4）⭐⭐⭐
10. **brain-alpha-judge**（S4→S5）⭐⭐
11. **点塔进度回写**（S6）⭐⭐⭐

### 优化建议

1. **自动化**：将更多步骤自动化，减少人工干预
2. **集成**：将更多步骤集成到 workflow 引擎，提高效率
3. **增强算法**：增强评分、检测、预测算法，提高准确性
4. **减少重复**：合并重复步骤，减少冗余
5. **质量效能增益评估**：集成质量效能增益评估，持续优化流程
