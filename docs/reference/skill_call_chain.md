# Skill 调用链文档

本文档明确 WorldQuant BRAIN Alpha 挖掘工作区中关键 Skill 的调用链与依赖关系，避免"对 Skill 链理解不足"导致的执行偏差。

---

## 1. 批量回测与跟踪链（S3 阶段）

### 调用链
```
brain-simAlphasinBatch-and-track (Skill)
    ↓ 触发
wq-brain-campaign-toolkit/scripts/pipeline.py (执行引擎)
    ↓ 调用
BrainApiClient.create_multi_simulation() (平台 API)
```

### 各环节职责

| 环节 | 类型 | 职责 | 关键文件 |
|------|------|------|----------|
| **brain-simAlphasinBatch-and-track** | Skill 定义 | 提供批量回测的方法论文档、参数模板、最佳实践 | `.qoder-cn/skills/brain-simAlphasinBatch-and-track/SKILL.md` |
| **wq-brain-campaign-toolkit** | 执行引擎 | 实际执行批量回测、断点续跑、结果收集 | `wq-brain-campaign-toolkit/scripts/pipeline.py` |
| **pipeline.py** | CLI 入口 | 解析命令行参数、调度回测任务、写入 CSV/DB | `pipeline.py run --dataset <DS> --wave <N>` |
| **BrainApiClient** | API 客户端 | 与 BRAIN 平台通信、429 退避、并发控制 | `world-quant-brain-mcp/brain_mixin_simulation.py` |

### 正确调用方式

**❌ 错误：手写脚本调用平台 API**
```python
# 禁止！绕过 MCP 工具，无 429 退避，易触发平台限制
import requests
response = requests.post("https://api.worldquantbrain.com/simulations", ...)
```

**✅ 正确：通过 Workflow 节点或 MCP 工具**
```python
# 方式 1：Workflow 节点（推荐）
from wqb.workflow import get_executor
executor = get_executor()
result = executor.execute("batch_track", {
    "region": "KOR",
    "wave": "36A",
    "dataset": "model219",
    "concurrency": 7,  # 七槽填槽
})

# 方式 2：MCP 工具（结构化数据）
# 使用 mcp__wq-brain-http__batch_create_simulations
# 使用 mcp__wqb-db__upsert_backtest_rows
```

### 关键参数说明

| 参数 | 来源 | 说明 |
|------|------|------|
| `campaign_dir` | 自动解析或环境变量 | 战役目录，优先级：参数 > `WQB_CAMPAIGN_DIR` > 自动探测 |
| `concurrency` | 默认 7 | 并发数，七槽填槽模式（见 wqb-concurrency §8） |
| `max_rounds` | 默认 3 | 最大轮次，断点续跑关键 |
| `--review` | 固定添加 | 自动评审 |
| `--write-ledger` | 固定添加 | 结果写 ledger |

---

## 2. GEM 表达式生成链（S4 阶段）

### 调用链
```
brain-makeSomeGem (Skill)
    ↓ 触发
trailSomeAlphas/skills/brain-feature-implementation (执行)
    ↓ 生成
final_expressions.json (产物)
    ↓ 质量预估（自动）
tools/pool_diversity.py + tools/quality_predict.py
```

### 关键环节

| 环节 | 文件 | 说明 |
|------|------|------|
| Skill 定义 | `brain-makeSomeGem/SKILL.md` | 概念优先：机制→具体字段→一条模板 |
| 执行器 | `run.py --config config.json` | headless_runner 模式 |
| 产物 | `final_expressions.json` | 生成的 alpha 表达式列表 |
| 质量预估 | `tools/quality_predict.py` | 零配额预检，三态判定 |

### Workflow 节点集成

```python
# gem 节点自动完成：生成 → 质量预估 → Mode B 标记
result = executor.execute("gem", {
    "region": "KOR",
    "dataset_id": "model219",
    "delay": 1,
    "universe": "TOP3000",
    "data_category": "analyst",
})
# 返回包含：
# - expression_count: 生成表达式数量
# - quality_estimation: 质量预估结果
# - mode_b_required: 是否需要 Mode B（EXPECTED_BLOCK > 0）
```

---

## 3. 特征工程链（S1-S3 阶段）

### 调用链
```
feature_engineering (Workflow 节点)
    ↓ S1: 字段理解
scan_fields.py + 字段分类
    ↓ S2: 字段筛选
build_wave.py + 多样性审计
    ↓ S3: 预处理决策
ledger s1_<dataset>_d<delay> 写入
    ↓ 自动注入
S2 执行时 --ideas-file 自动传入
```

### 关键产物

| 产物 | 位置 | 说明 |
|------|------|------|
| S1 ledger | `ledger_kv s1_<dataset>_d<delay>` | 字段理解与预处理决策 |
| 字段目录 | `field_catalog` 表 | 字段类型/覆盖率/更新频率 |
| 波次配置 | `wave_config` | 候选池配置 |

---

## 4. 提交判定链（S6 阶段）

### 调用链
```
brain-alpha-judge (Skill)
    ↓ 六步闸门
1. 平台硬检查 → 2. PPA 闸门 → 3. Trend Score → 4. 相关性 → 5. LLM 决策 → 6. 提交确认
    ↓ 通过
worldquant-submit-alpha (Skill)
    ↓ 提交
mcp__wq-brain-http__submit_alpha
```

### 关键闸门

| 闸门 | 条件 | 动作 |
|------|------|------|
| PPA 闸门 | prod_corr ≥ 0.7 | **BLOCK + Mode B**（换字段组合） |
| 自相关 | self_corr ≥ 0.7 | BLOCK |
| Trend Score | < 阈值 | BLOCK |
| LLM 决策 | 低价值 | BLOCK |

---

## 5. 常见误区与纠正

### 误区 1：手写脚本调用平台 API
**症状**：写 `logs/_tmp_*.py` 调用 `requests.post()` 提交 alpha
**纠正**：使用 `mcp__wq-brain-http__submit_alpha` 或 `worldquant-submit-alpha` skill

### 误区 2：忽略 campaign_dir 解析
**症状**：`Campaign directory not found` 错误
**纠正**：设置 `WQB_CAMPAIGN_DIR` 环境变量，或让节点自动解析

### 误区 3：跳过质量预估直接回测
**症状**：大量 EXPECTED_BLOCK 候选进入回测，浪费配额
**纠正**：使用 `campaign` 节点（自动质量闸），或手动调用 `wave_gate.py --quality-block`

### 误区 4：prod_corr ≥ 0.7 仍强行提交
**症状**：提交被拒或标记为低价值
**纠正**：judge 节点自动 BLOCK，回 Mode B 换字段组合

---

## 6. 快速参考：何时用哪个工具

| 场景 | 推荐工具 | 备选 |
|------|----------|------|
| 批量回测 | `workflow_batch_track` | `pipeline.py run` |
| 生成表达式 | `workflow_gem` | `run.py --config` |
| 质量预估 | `tools/quality_predict.py` | `workflow_gem`（自动） |
| 提交判定 | `workflow_judge` | `brain-alpha-judge` skill |
| 特征工程 | `workflow_feature_engineering` | `scan_fields.py` |
| 提交 alpha | `mcp__wq-brain-http__submit_alpha` | `worldquant-submit-alpha` skill |
| 查 alpha 指标 | `mcp__wq-brain-http__get_alpha_details` | 禁止手写脚本 |

---

## 7. 环境变量速查

| 变量 | 用途 | 示例 |
|------|------|------|
| `WQB_WORKSPACE_ROOT` | 工作区根路径 | `d:\coding\traeCN_project\wqb` |
| `WQB_CAMPAIGN_DIR` | 战役目录（覆盖自动解析） | `d:\coding\traeCN_project\wqb\tracking\KOR` |
| `WQ_TOOLKIT_DIR` | toolkit 脚本目录 | `~/.qoder-cn/skills/wq-brain-campaign-toolkit/scripts` |
| `WQ_PY` | Python 解释器路径 | `python` 或 `C:\Python39\python.exe` |

---

*文档版本：2026-08-27*
*关联规约：AGENTS.md §5（Shell 命令规约）、§6（一次性脚本工具化纪律）*
