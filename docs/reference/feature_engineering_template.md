# 特征工程文档模板（波级，六节式）

> **用途**：每个挖掘波次（wave）开始前，复制本模板到 `tracking/<REGION>/feature_engineering_wave<N>_<dataset>.md` 填写。
> 配套流程规范见 [feature_engineering_sop.md](feature_engineering_sop.md)。
> **填写纪律**：`〔必填〕` 节不可留空；表格行不足可增删；`〈提示〉` 为填写指引，定稿前删除。
> 最后更新：2026-08-27

---

# Wave {N} 特征工程文档 — {数据集}

## 0. 基础信息〔必填〕

| 项 | 值 |
|---|---|
| Wave | {N} |
| Region | {REGION} |
| Dataset | {dataset_id}（data_type: MATRIX/VECTOR，delay: {0/1}） |
| Universe / 中性化 | {TOP3000} / {SUBINDUSTRY} |
| 基础配方 | 〈来源：上一波成功配方 / registry win 条目 ID / 跨区域移植（注明来源区域与指标）〉 |
| 失败教训输入 | 〈引用台账/registry dead_end 条目：本波明确避开什么〉 |
| 优化目标 | 〈一句话：本波要验证的假设，如"换数据集降 SELF_CORRELATION"〉 |

## 1. 字段理解〔必填〕

〈提示：数据来源 `mcp__wq-brain-http__get_datafields` + field_catalog 表；每个入池字段回答"测什么/怎么测/时间维度/业务背景"。
不要照抄平台 description 原文，要写**经济学含义**与**信号方向假设**（高值预示涨还是跌，为什么）。〉

| 字段 | 测什么 | 更新频率 | 覆盖率 | 数据类型 | 信号方向假设 | 经济学逻辑 |
|---|---|---|---|---|---|---|
| {field_1} | … | daily/event/quarterly | 0.xx | MATRIX/VECTOR | 高→涨/跌 | … |
| {field_2} | … | … | … | … | … | … |

**数据集故事**：〈2-3 句：这组字段共同描述什么经济现象？字段间是独立、互补还是同源？〉

## 2. 字段筛选〔必填〕

〈提示：逐字段过筛，**写明依据数值**，禁止"凭历史经验选字段"不留证据。
平台竞争（alphaCount）与覆盖率来自 `get_datasets`/`get_datafields`；
字段族历史先验可用 `python tools/quality_predict.py` 的先验输出。〉

### 2.1 入选字段

| 字段 | 覆盖率 | 非零率/更新频率 | 平台竞争 | 字段族历史先验 | 入选理由 |
|---|---|---|---|---|---|
| {field_1} | ≥0.6? | … | alphaCount=? | Sharpe 先验=? | … |

### 2.2 淘汰字段（及原因）〔必填，哪怕只写"本数据集其余字段未入池"〕

| 字段 | 淘汰原因（覆盖率不足 / 更新过慢 / 高同源 / 族饱和 / 平台竞争过高） |
|---|---|
| {field_x} | … |

**同源风险自查**：〈入选字段两两之间是否来自同一模型/同一信号源？
是 → 组合后 SELF_CORRELATION 必高，需在 §4 用不同骨架或放弃组合。〉

## 3. 预处理决策〔必填〕

〈提示：每字段一行，写清"用什么预处理 + 为什么"。硬性规则先过一遍检查清单。〉

**规则检查清单**：
- [ ] EVENT 类字段：禁 winsorize（用 `ts_event_*` 或裸 rank）
- [ ] VECTOR 字段：必须 `vec_*` 聚合后再进常规算子
- [ ] 稀疏字段（覆盖率 <0.85）：先 `ts_backfill` 再平滑
- [ ] 非平稳字段（排名/价格类）：`rank` 或 `ts_zscore`
- [ ] 需要行业内相对：`group_zscore`/`group_rank`（同时满足多样性闸门）

| 字段 | 预处理链 | 决策依据 |
|---|---|---|
| {field_1} | `rank(ts_backfill(field_1, 66))` | 稀疏+非平稳，回填后截面排名 |

**台账回写**：〈S1 决策入库 `ledger_kv` key=`s1_<dataset>_d<delay>`（含 field_whitelist 与 preprocessing），
S2 启动时自动注入，禁止绕过。〉

## 4. 表达式生成策略〔必填〕

〈提示：概念优先——先写经济机制（收益来源假设），再绑字段。
纪律：每条表达式 1-2 个字段；同信号族禁止调权重变体；骨架配额遵守线性组合 ≤50%。〉

### 4.1 收益来源假设（本波要验证的经济机制）

| # | 机制描述 | 绑定字段 | 预期收益来源 |
|---|---|---|---|
| 1 | {例：模型排名上升的公司后续跑赢} | {field_1} | {动量/信息扩散} |

### 4.2 骨架配额计划

| 骨架 | 占比目标 | 说明 |
|---|---|---|
| 单字段+预处理 | ~50% | 基线探针 |
| 2 腿线性组合 | ≤30% | 互补字段才组合，同源字段禁组合 |
| 事件门控/分组结构 | ≥20% | `trade_when`/`group_zscore`，防 CW 墙 + 多样性闸门 |

### 4.3 生成方式

- 工具：`brain-makeSomeGem`（带 `--priors-file`：win/dead_end）
- 目标数量：{8-24} 条
- 去重：`build_wave.py` 全历史去重（防配额浪费）

## 5. 质量预估（回测前）〔必填〕

〈提示：回测前强制跑两个本地工具，结果粘贴摘要。禁止跳过直接烧配额。〉

```powershell
python tools/pool_diversity.py --region {REGION} --wave {N} --dataset {dataset}
python tools/quality_predict.py --region {REGION} --wave {N} --dataset {dataset}
```

| 项 | 结果 |
|---|---|
| 六维多样性 | {PASS / 风险项列表} |
| 质量预估 | PASS={n} REVIEW={n} EXPECTED_BLOCK={n} |

**EXPECTED_BLOCK 处理记录**〔有 BLOCK 必填〕：

| 表达式（截取） | BLOCK 原因 | 处理方式（回 Mode B 换字段组合 / 删除） |
|---|---|---|
| … | {相关性代理分撞 <alpha_id> / 字段族饱和} | … |

〈纪律：BLOCK 候选禁止调权重后重试，必须换字段组合（Mode B 想法层）。〉

## 6. 候选池优化与门禁〔必填〕

```powershell
python tools/wave_gate.py --campaign-dir tracking/{REGION} --dataset {dataset} --wave {N} --from-db [--quality-block]
```

| 项 | 结果 |
|---|---|
| 语法 | {x}/{n} PASS |
| 5 闸 | all_pass={…} |
| 六维多样性 + 质量预估 | {摘要} |
| 入批计划 | {批次划分、五槽填槽安排} |

**台账回写**：〈wave 结论入 `wave_results` / WAVE_LEDGER.md（单入口，勿写散件）。〉

## 7. 复盘钩子（回测后填写）

| 项 | 预估 | 实际 | 偏差结论 |
|---|---|---|---|
| 达标数 | {质量预估 PASS+REVIEW 中预期} | {实际过闸数} | … |
| SELF_CORRELATION | {代理分预判} | {平台实测} | {代理准/不准，写回经验} |

**回写清单**：〈registry_empirical dead_end/win 条目、template_kb 骨架记录、本模板本身需要改进处。〉
