# other553 应急派发载荷（READY · 未派发）

> 启用条件（见 `wave2_decision_tree.md`）：Wave1 forum max|S|<0.5 且 Wave1b 无可用信号。
> 当前：Wave1b 已 REJECT；Wave1 forum 仍在飞 → **不得预派**。
> 切换原因模板：严格 Social Media=ID 向量不可用 + equity_forum_data social-adjacent 全灭。
> category=sentiment（非禁混 OTHER 内部互组）；单集 ATOM；算子≤12。

## Preflight（2026-11-06）
- valid=true · unknown_fields=[] · any_changed=false

```json
{
  "region": "KOR",
  "universe": "TOP600",
  "delay": 1,
  "decay": 4,
  "neutralization": "STATISTICAL",
  "truncation": 0.08,
  "unit_handling": "VERIFY",
  "nan_handling": "OFF",
  "pasteurization": "ON",
  "max_trade": "OFF",
  "language": "FASTEXPR",
  "wait_for_completion": false,
  "validate_fields": true,
  "alpha_expressions": [
    "subtract(0.5, group_rank(ts_mean(vec_avg(oth553_est_estvalue), 22), sector))",
    "subtract(0.5, group_rank(ts_mean(ts_delta(vec_avg(oth553_est_estvalue), 22), 5), sector))",
    "subtract(0.5, group_rank(ts_mean(vec_avg(oth553_est_analyst), 22), sector))",
    "subtract(0.5, group_rank(ts_mean(vec_avg(oth553_ptgvalue), 22), sector))",
    "subtract(0.5, group_rank(ts_mean(ts_delta(vec_avg(oth553_ptgvalue), 22), 5), sector))",
    "subtract(0.5, group_rank(ts_mean(vec_avg(oth553_recvalue), 22), sector))",
    "group_rank(ts_mean(subtract(vec_avg(oth553_est_estvalue), vec_avg(oth553_est_preestvalue)), 22), sector)",
    "subtract(0.5, group_rank(ts_mean(vec_avg(oth553_est_yearspeakcnt), 66), sector))"
  ],
  "tags": [
    "C01_est_lvl",
    "C02_est_delta",
    "C03_analyst",
    "C04_ptg_lvl",
    "C05_ptg_delta",
    "C06_rec",
    "C09_est_spread",
    "C10_speak"
  ]
}
```
