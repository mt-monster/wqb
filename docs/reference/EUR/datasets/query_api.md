# 字段画像查询接口（CLI + Python API + MCP）

> 数据表：`data/wqb.db::dataset_profile`（178 行）/ `field_profile_full`（38,609 行）
> 生成脚本：`tools/load_field_profiles_to_db.py`（源：`fields` + `field_profile_perf` + 平台目录 + `backtest_results`）

## 一、建表与刷新

```bash
# 全量重建（幂等，可重复跑）
python tools/load_field_profiles_to_db.py
# 指定区域
python tools/load_field_profiles_to_db.py --region EUR
```

## 二、CLI 查询

```bash
PY=./world-quant-brain-mcp/.venv/Scripts/python.exe

# 1) 全局统计（按类别 / 语义族 / 判定）
$PY tools/query_profile.py stats

# 2) 数据集筛选
$PY tools/query_profile.py datasets --category RISK --min-cov 0.8
$PY tools/query_profile.py datasets --has-alive                 # 历史有 ALIVE 字段的
$PY tools/query_profile.py datasets --max-untested 0.5          # 至少一半字段测过
$PY tools/query_profile.py datasets --sort n_alive --limit 10

# 3) 字段筛选（组合条件）
$PY tools/query_profile.py fields --dataset risk60
$PY tools/query_profile.py fields --untested --min-cov 0.9 --family 修正与预期 --limit 100
$PY tools/query_profile.py fields --tested --min-best-s 1.5 --min-best-2y 1.5
$PY tools/query_profile.py fields --alive-only
$PY tools/query_profile.py fields --verdict UNUSABLE --family 情绪与新闻

# 4) 关键词检索（字段名 + 描述）
$PY tools/query_profile.py search "borrow fee"
$PY tools/query_profile.py search "short interest" --limit 50

# 5) 维度覆盖（实测口径；--static 切静态口径）
$PY tools/query_profile.py dims --min-dim-cov 1.0
$PY tools/query_profile.py dims --category PV --limit 10

# 6) 榜单
$PY tools/query_profile.py top --metric best_2y --min-cov 0.8 --limit 20

# 7) JSON 输出（给程序/管道消费）
$PY tools/query_profile.py fields --dataset pv87 --limit 5 --json
```

## 三、Python API

```python
import sys; sys.path.insert(0, "tools")
from query_profile import query_datasets, query_fields, search, stats

# 数据集级
rows = query_datasets(category="ANALYST", min_cov=0.7, has_alive=True, sort="n_alive")

# 字段级：找「未测 + 高覆盖 + 目标语义族」的盲区
blind = query_fields(untested=True, min_cov=0.9, family="修正与预期", limit=200)

# 字段级：找已测出强度的
strong = query_fields(tested=True, min_best_s=1.5, min_best_2y=1.5, sort="best_2y")

# 关键词
hits = search("lending fee")
```

## 四、MCP 工具（需重启 MCP 服务后生效）

`wqb-db` 服务新增两个工具：

| 工具 | 说明 |
|---|---|
| `query_dataset_profile(region, category, min_cov, has_alive, max_untested_ratio, sort, limit)` | 数据集级筛选 |
| `query_field_profile(region, dataset, family, verdict, min_cov, max_cov, min_best_s, min_best_2y, keyword, tested, untested, alive_only, sort, limit)` | 字段级组合筛选 |

> ⚠️ 代码已于 `wqb_db_mcp.py` 写入，但**运行中的服务是旧进程**（启动早于改动）。
> 需重启 WorkBuddy 或 MCP 服务后，工具才会出现在工具列表里。
> 在此之前请用上面的 CLI / Python API（功能完全等价）。

## 五、字段字典

### `dataset_profile`（数据集级）
`region, dataset, name, category, description, coverage, field_count, alpha_count, value_score,
pyramid_multiplier, delay, data_type, n_fields, avg_field_coverage, min_field_coverage,
max_field_coverage, freq_hint, availability, n_untested, n_alive, n_unusable, n_dead,
n_axis_only, best_s_in_dataset, best_2y_in_dataset, n_backtests, n_ra_pass,
**n_dims, n_dims_bt, n_dims_static, dim_coverage_bt, dim_coverage_static**, updated_at`

> `dim_coverage_bt` = 实测口径（维度内 ≥1 字段 `n_tests>0`）——**判死/升档的唯一依据**；
> `dim_coverage_static` = 静态判定口径（`verdict != UNTESTED`），会虚高，仅参考。

### `field_profile_full`（字段级）
`region, dataset, category, field_name, field_type, coverage, description, semantic_family,
coverage_tier, freq_hint, n_tests, best_s, best_2y, best_sub, best_f, verdict,
skeleton_fams, is_alive, is_untested, updated_at`

### 语义族（10 族 + 其他）
修正与预期｜盈利与财务｜价量与波动｜情绪与新闻｜持仓与资金流｜宏观与行业｜风险与质量｜交易与微观结构｜搜索与替代数据｜元数据与非信号｜其他

### 判定取值
`ALIVE`（历史测出 S≥闸线，**不代表可提交**）｜`UNTESTED`｜`UNUSABLE`｜`DEAD`｜`DEAD_STATIC`｜`AXIS_ONLY`（仅可作轴）｜`WEAK`

## 六、覆盖口径（v2，2026-10-20 起）

派发闸已改为**维度级**默认（见 `docs/reference/EUR/full_coverage_rule_v2.md`）：

```bash
# 维度级（默认）：每个语义维度至少被 1 条候选触及
$PY tools/full_coverage_gate.py --region EUR --dataset <ds> --exprs-file cand.txt --gate-mode enforce

# 字段级（仅近闸深挖 / 判死时用）
$PY tools/full_coverage_gate.py --region EUR --dataset <ds> --exprs-file cand.txt     --coverage-mode field --near-gate --gate-mode enforce
```

## 七、注意事项
- `field_profile_perf` 的判定是**历史快照**，可能过时（analyst7 旧判死已推翻）。做尽前须按当前结构重跑。
- `backtest_results` 只含**已持久化**的波次；本次会话直接派发未写库，故 `n_backtests=0` ≠ 未做尽。
- 平台目录的 `name/description` 有错配（insiders1 / imbalance5 已实证），以字段明细语义为准。
