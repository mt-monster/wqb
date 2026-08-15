# mining_experience — 经验驱动的 Alpha 挖掘启发式引擎

将已提交 alpha 的经验（region → data source → template → OS decay）
结构化为机读规则，注入 `glb_alpha_machine` / `gbr_pipeline.py` 的挖掘流水线。

## 架构

```
../os_alpha_experience_summary.md  (人类可读经验知识库)
          │
          ▼
mining_experience/
├── rules.json              结构化规则（145 alphas 提取）
├── heuristic_engine.py     决策引擎（API 层）
├── gen_heuristic_expressions.py  独立 CLI 工具
└── README.md               本文档

glb_alpha_machine/
├── gbr_pipeline.py         Stage1/2/3 经验注入
└── glb_pipeline.py         Stage2/3 经验注入
```

## 核心文件

### `rules.json`

145 个已提交 alpha 的经验提取，包含：

| 区块 | 内容 |
|------|------|
| `regions` | 8 个区域配置（USA/IND/MEA/GBR/GLB/KOR/ASI/ILLIQUID），每个含数据源亲和力、最优参数、模板偏好 |
| `templates` | 16 个命名表达式模板，含 avg_sharpe、os_decay_risk、priority、applicable_regions/datasets |
| `os_decay_analysis` | 反衰减模板列表 + 高衰减模板列表 + 衰减规则（risk_multiplier） |
| `parameter_defaults` | 按区域/Universe 的最优参数（neutralization、decay、truncation） |
| `sign_directions` | 数据源符号方向（negative/positive） |
| `window_recommendations` | 各算子推荐时间窗口 |
| `sa_recipe` | SA 最佳配方（selection=combo_a, componentActivation=IS） |

### `heuristic_engine.py`

提供以下 API：

```python
from mining_experience.heuristic_engine import (
    get_engine, score_expression,
    get_preferred_templates, get_region_recommendations,
    get_sa_recipe, generate_expressions,
    should_suppress_template, get_template_decay_risk,
)

# 区域推荐
recs = get_region_recommendations("GBR", "TOP700")
# → { total_alphas, avg_sharpe, data_sources, best_params, ... }

# 表达式评分
result = score_expression("group_rank(ts_rank(fnd6_drlt,60),sector)", "USA", "TOP3000")
# → { total_score: 116.2, template_match: "group_rank_ts_rank",
#      os_decay_risk: "low", recommendations: [...] }

# 模板抑制检查
should_suppress_template("vector_neut")  # → True
get_template_decay_risk("group_rank_ts_rank")  # → "low"

# SA 配方
recipe = get_sa_recipe()
# → { selection: "(prod_correlation > 0)", combo: "combo_a(alpha)", ... }
```

### `gen_heuristic_expressions.py`

独立 CLI 工具，从规则文件生成经验驱动的候选表达式：

```bash
# 生成 USA TOP3000 候选
python gen_heuristic_expressions.py --region USA --universe TOP3000 --datasets fnd6 --count 20

# 生成 IND TOP500 候选（多因子加权）
python gen_heuristic_expressions.py --region IND --universe TOP500 --datasets mdl177 --count 100

# 评分单条表达式
python gen_heuristic_expressions.py --score "group_rank(ts_rank(fnd6_drlt,60),sector)" --region USA --universe TOP3000

# 查看所有模板
python gen_heuristic_expressions.py --templates

# 查看 SA 配方
python gen_heuristic_expressions.py --sa-recipe
```

## 流水线注入点

### `gbr_pipeline.py`

| 注入点 | 函数 | 效果 |
|--------|------|------|
| Stage 1 字段采样 | `_apply_heuristic_field_priority()` | 按经验数据源优先级重排字段顺序，高产出数据集优先模拟 |
| Stage 2 group ops | `get_heuristic_stage2_ops()` | group ops 按经验产出排序：group_rank > group_neutralize > group_zscore > group_scale |
| Stage 3 trade_when | `stage3()` | 对 trade_when 候选做启发式预评分，高衰减关键词（ts_std_dev/vector_neut）降优先级 |

开关：`USE_HEURISTICS = True`（设为 False 完全回到原始行为）

### `glb_pipeline.py`

| 注入点 | 函数 | 效果 |
|--------|------|------|
| Stage 2 group ops | `get_heuristic_stage2_ops()` | 同 GBR，但适配 GLB 数据集 |
| Stage 3 trade_when | `stage3()` | 同 GBR |

## 关键经验（可直接使用）

### 最稳定模板（low OS decay）
1. `group_rank(ts_rank(FIELD, 60), group)` — avg_sh=1.62, low decay ← **首选**
2. `ts_sum(FIELD, 252) + group_neutralize` — avg_sh=1.53, medium decay
3. `add(multiply(rank(ts_rank(ts_backfill(A,66),250)),w1), ...)` — avg_sh=2.50, low decay（IND/MEA）
4. `simple_price_volume: -rank(ts_sum((close-low)/(high-close), 3))` — avg_sh=1.72, low decay

### 高衰减模板（避免使用）
- `vector_neut(-FIELD * ts_std_dev, ...)` — avg_sh=1.49, **high decay**, suppress
- `-FIELD * ts_std_dev(FIELD, N)` — avg_sh=1.46, **high decay**, suppress
- `group_mean(ts_std_dev, ...) - ts_std_dev` — avg_sh=1.48, **high decay**, suppress

### 区域最优参数

| 区域 | neutralization | decay | truncation |
|------|---------------|-------|------------|
| USA | MARKET | 5 | 0.08 |
| IND | STATISTICAL | 8 | 0.08 |
| MEA | SUBINDUSTRY | 5 | 0.08 |
| GBR | SUBINDUSTRY | 4 | 0.08 |
| GLB | COUNTRY | 5 | 0.08 |
| KOR | SUBINDUSTRY | 5 | 0.08 |
| ASI | MARKET | 5 | 0.08 |

### 数据源符号方向
- **negative**（取 -FIELD）: mdl177
- **positive**（直接用）: fnd6, fnd93, anl4, anl39, mdl31, inst18, star_eq, oth36, fnd110, predicted

### SA 配方
- `selection = "(prod_correlation > 0)"`
- `combo = "combo_a(alpha)"`
- `componentActivation = "IS"`
- 无需手动指定 children，平台自动从 OS pool 选取
- 描述字段（selection/combo description）需 ≥100 字符
- tags 必须包含 `PowerPoolSelected`