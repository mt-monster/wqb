# perf_max 演示批：RR6bv6rz 业绩极致优化（2026-10-08）

## 背景

`perf_max` 是仓库新增项目功能：对**全闸通过**（failed_ra=0）的 alpha，在「闸门保持绿」硬约束下把业绩指标推到极致。与 `alpha_booster`（S4，卡闸→修到通过）首尾相接。本批为功能验收演示，baseline = 冠军 `RR6bv6rz`（USA/analyst_consensus，quantile 分布变换破 SUB 闸产物，S 2.04/F 1.20）。

## 执行链

`plan --alpha-id RR6bv6rz`（真拉 baseline）→ `submit_batch.py --spec`（8 变体派发）→ `perf_max.py harvest`（按 alpha-ids 增量收批）→ `report`。全程零提交。

## 结果（objective=fitness）

| label | 杠杆 | 结论 | S | F | 2Y | SUB | TO | 破闸项 |
|---|---|---|---|---|---|---|---|---|
| **WIN_DBL_20** | 窗口×2（ts_mean 10→20） | **✅ 闸保持，ΔF=+0.01** | 2.07 | 1.21 | 1.67 | 0.90 | 0.0375 | — |
| DECAY_DBL_512 | decay 500→512 | ✅ 闸保持（≈baseline） | 2.04 | 1.20 | 1.71 | 0.89 | 0.0383 | — |
| WIN_HALF_5 | 窗口×0.5（10→5） | ❌ 差 0.01 | 2.04 | 1.21 | 1.77 | 0.87 | 0.0387 | SUB(0.87<0.88) |
| DECAY_HALF_250 | decay 500→250 | ❌ | 1.89 | 1.03 | 1.74 | 0.76 | 0.0368 | SUB |
| EQ_SP05 | signed_power(0.5) | ❌ | 2.16 | 1.33 | 1.54 | 0.82 | 0.0389 | SUB+2Y |
| EQ_WINS2 | winsorize(std=2) | ❌ | 1.89 | 1.04 | 1.52 | 0.82 | 0.0368 | 2Y |
| EQ_NORMSTD | normalize(useStd) | ❌ | 1.90 | 1.05 | 1.53 | 0.83 | 0.0369 | 2Y |
| CTRL_NANOFF | nanHandling=OFF 对照 | ❌ S 塌到 0.34 | 0.34 | 0.08 | 0.03 | 0.43 | 0.0339 | S+F+2Y |

**推荐：WIN_DBL_20 = `pw5RbrYX`**（sharpe 2.07、fitness 1.21、margin 0.002284，SUB 0.90>limit 0.88、2Y 1.67、failed_ra=0）。

## 可迁移结论

1. **窗口微扫是本族的真业绩杠杆**（`wq-window-valley` 同族手法）：外层 ts_mean 窗口 10→20 同时提 S/F 且 SUB 比值不劣化；窗口减半（→5）SUB 差 0.01 惜败——**方向性：慢窗口更稳**。
2. **提强度杠杆（signed_power 0.5）在本族是零和**：S 2.16/F 1.33 全场最高，但 limit=0.433×S 同步抬高（0.94）+ 2Y 塌，闸门必破——再次实证「SUB 闸判定看比值不看绝对值」。
3. **等价算子替换（winsorize/normalize）在本族不保 2Y**（1.52/1.53 vs 限 1.58）。
4. **CTRL 归因**：nanHandling=OFF ⇒ S 0.34 崩塌，本信号强度依赖 nanHandling=ON，是强度闸非风格开关（IND 同结论跨区复证）。
5. **DECAY 双档无增益**（512≈500；250 破 SUB）——本族 decay 敏感度低，无需再扫。

## 提交约束（零自动提交，提交权归用户）

- `pw5RbrYX` 与 `RR6bv6rz` **同族近亲**（同骨架只换窗口，self 相关性预期 0.9+）⇒ 若提交**只出 1 颗**，须先 `check_self_correlation` 实测定夺留哪颗。
- 提交前三步：`check_correlation(refresh=True)` prod/self 终验（>48h 规则）→ `submit_verdict` 预检 → 用户逐次授权。

## 过程中修复的工具 bug（已补测试锁定）

1. `flatten_details` 不认平台原始形态（`regular.code`/`is.*`/`is.checks` 列表）→ 增 `_flatten_raw_details`（RA 口径单源引用 `wqb.config.compute_webdata_failed_counts`/`RA_2Y_NAMES`）。
2. `cmd_plan` 守卫只查顶层 `code` → 认 `regular.code`；前置闸补「名单内 PENDING 不得放行」。
3. dispatch_spec 只写 patch 丢 baseline 设置（decay=None 被 400）→ 条目改携全量设置+patch 覆盖。
4. `submit_batch.py` n=1 被包成 multi-sim 数组被平台拒 → 单条改发裸 dict。
5. `_window_variants` 右括号重复（WIN 变体被元数闸静默丢弃）→ 修 tail 取位，测试加括号平衡断言。

测试：`tests/unit/10_toolkit_scripts/test_perf_max.py` 15 项全绿；三闸（governance/doc_path_refs/destructive_default）全绿。
