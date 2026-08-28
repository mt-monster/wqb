# GEM S1⇄S2 状态机代码化 dry-run 报告

> 2026-08-25 · KOR model25 D1 TOP600 · 双场景全链路演示
>
> **唯一 stub 点**：`call_moonshot`（LLM 调用，返回罐装 ideas）。其余全真：真实 BRAIN session、
> 真实平台字段目录（554 字段）、真实数据集 CSV 下载、真实模板解析/展开/validator、
> 真实 DB 读写（`wqb.db` 临时副本，`WQB_DB_PATH` 隔离，真库零污染）。

## 本次代码改动（三件套）

| 改动 | 文件 | 内容 |
|---|---|---|
| 1 | `implement_idea.py` | 新增 `--field-whitelist` 参数；绑定池按白名单收窄，零交集返回空并告警 |
| 2a | `run_pipeline.py` | 启动自查 `s1_<ds>_d<delay>` ledger：命中且 `ideas_md_path` 可读 → 自动注入 `--ideas-file`（skeleton / `--regen-ideas` / 显式 `--ideas-file` 跳过） |
| 2b | `run_pipeline.py` | 命中记录带 `field_whitelist` → 收窄绑定池 + 落盘 `s1_field_whitelist.json` + 传参给子进程 |
| 2c | `run_pipeline.py` | 自含生成路径收尾自动回写 ledger：`source=s2_nested`，`field_whitelist` = 表达式实际引用字段 ∩ 数据集字段 |

改动前此状态机只存在于 skill md 的 agent 纪律层（靠人查/人写），改动后由代码强制。

## 罐装 ideas（stub LLM 产出）

3 个 Concept，占位符为真实 model25 字段 id（exact match，1:1 展开）：

| Concept | 模板 | 绑定字段 |
|---|---|---|
| 时序动量 | `ts_rank({FA}, 20)` | `value_momentum_sector_rank_float`（cov=1.00） |
| 相对强弱比率 | `divide({FA}, {FB})` | + `analyst_recommendation_score_5` |
| 长窗偏离 | `ts_zscore({FC}, 60)` | + `analyst_revision_composite_score` |

## 场景 A：无 s1 记录 → 自含生成 → 自动回写

临时 DB 预删 `KOR/s1_model25_d1`，模拟首次挖掘。stdout 关键行：

```text
[priors] region priors loaded for KOR (346 chars)
Filtered invalid expressions: 0
[s1] 回写 ledger s1_model25_d1: whitelist=3 字段, source=s2_nested
[db] expressions/KOR/dryrun_s1s2_a n=3 status=gem
[db] idea ledger s2_model25_d1_idea
```

过程明细：ledger 自查（无记录，静默）→ 平台元数据 + priors 组装 → build_prompt →
stub LLM 返回罐装 ideas（**调用 1 次**）→ ideas.md 落盘 → fetch_dataset 下载 554 字段 CSV →
Concept 块解析（3 模板）→ implement_idea 逐模板展开（绑定池 554，无白名单）→
validator（0 条被滤）→ 入库 `dryrun_s1s2_a` → **回写 s1 ledger**。

产出表达式（3 条）：

```text
ts_rank(value_momentum_sector_rank_float, 20)
divide(value_momentum_sector_rank_float, analyst_recommendation_score_5)
ts_zscore(analyst_revision_composite_score, 60)
```

回写记录全文（断言：whitelist == 表达式实际引用字段 ∩ 数据集字段）：

```json
{
  "dataset": "model25", "region": "KOR", "delay": 1, "universe": "TOP600",
  "ideas_md_path": ".../output_report/KOR_delay1_model25_ideas.md",
  "field_whitelist": [
    "analyst_recommendation_score_5",
    "analyst_revision_composite_score",
    "value_momentum_sector_rank_float"
  ],
  "concept_count": 3,
  "source": "s2_nested",
  "generated_at": "2026-08-25T12:11:27+00:00"
}
```

## 场景 B：命中记录 → 自动注入 + 绑定池收窄（LLM 零调用）

同一临时 DB，将 `field_whitelist` 收窄为仅 `[value_momentum_sector_rank_float]`（模拟 S1 精筛），
stub LLM 改为**一旦被调用即 raise**（错误信息不含 token 类关键词，不会触发减半重试）。
stdout 关键行：

```text
[s1] ledger s1_model25_d1 命中（source=s2_nested），自动注入 --ideas-file: .../KOR_delay1_model25_ideas.md
[s1] field_whitelist 生效: 绑定池 554 -> 1 字段
Filtered invalid expressions: 0
[db] expressions/KOR/dryrun_s1s2_b n=1 status=gem
```

过程明细：ledger 自查**命中** → 自动注入 ideas 文件（LLM 整个被跳过，stub 未触发即证明）→
白名单落盘 + 子进程传参 → 3 个模板在同一数据集上展开，但绑定池只有 1 个字段：

| 模板 | 无白名单（A） | 白名单=[FA]（B） |
|---|---|---|
| `ts_rank({FA}, 20)` | 1 条 | 1 条（FA 在池内） |
| `divide({FA}, {FB})` | 1 条 | 0 条（FB 出池，无候选） |
| `ts_zscore({FC}, 60)` | 1 条 | 0 条（FC 出池，无候选） |

产出表达式（1 条）：`ts_rank(value_momentum_sector_rank_float, 20)`。
断言通过：引用字段 ⊆ 白名单；注入分支不再回写 ledger（`source` 保持首跑语义）。

## A vs B 对比

| 维度 | 场景 A（无记录） | 场景 B（命中+收窄） |
|---|---|---|
| LLM 调用 | 1 次 | **0 次**（注入跳过生成） |
| 绑定池 | 554 字段 | **1 字段**（-99.8%） |
| 表达式产出 | 3 条（3 字段） | 1 条（1 字段） |
| ledger | 回写 source=s2_nested | 不回写（读取复用） |

## 结论

S1⇄S2 状态机三件套按设计工作：首跑自含生成并沉淀决策（ideas 路径 + 实际引用字段），
续跑零 LLM 成本复用决策且绑定池精确收窄——同 `(region, dataset, delay)` 的内嵌 S1 不再重复执行，
表达式空间被约束在 S1 认可的经济字段集合内。SKILL.md 已同步改为"代码强制"表述，
`run_pipeline.py` / `implement_idea.py` / `SKILL.md` 均已双树同步（.trae-cn / .qoder-cn hash 一致）。

## 产物索引

- dry-run 脚本：`_gem_s1s2_dryrun.py`（work 目录，可复跑）
- 场景 A 表达式：`_s1s2_dryrun/scenario_A_expressions.json`；A/B stdout：`_s1s2_dryrun/stdout_{A,B}.txt`
- 临时 DB 副本：`_s1s2_dryrun/wqb.db`（含两场景 ledger/expressions 证据）
