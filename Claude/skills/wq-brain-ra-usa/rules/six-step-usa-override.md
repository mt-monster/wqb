# 六步纵深骨架 · USA 覆盖项

> 通用方法见 [`_six-step-core.md`](../../wq-brain-ra-pipeline/references/_six-step-core.md)；
> 本文只写 **USA 的 override**——本区平台事实、实测杠杆、已死轴、工程坑。
> **覆盖主 skill 同名条目；铁律与锁定项不可放宽。** 无实证处标「待实测」。

## ① 六法体检 · 本区覆盖

- **最深最饱和的市场** ⇒ 经典 `value` / `quality` / `book` 及其线性变体**必死**
  （book/value 单族 145 颗同族 ACTIVE）。`settings.json` 的 `_spre_20260917.excluded_families` 已列 23 个饱和/枯竭族。
- **正交方向（settings 内登记）**：`earnings_surprise` 长窗（group_rank+signed_power+decay90）、
  `fund_ownership` 变化（ts_zscore 长窗）、`eur_top_value` 慢 value（ts_zscore 189 + group_zscore industry）、
  `institutional` 持仓变化（rank+ts_rank 长窗）。
- **情绪域已饱和**（prod 0.72–0.82 全死）；`book/value` 145 ACTIVE 饱和、`probability_3` 差分 5 变体全死。
- **待实测**：离线体检包退化范围、本区不可用算子。

## ② 组装 · 本区覆盖

- 沿用主 skill + 饱和族硬排除（体检阶段命中即剔除，不进生成）。
- **禁止 IS Sharpe 排序选 prod 候选**（settings 的 `win_recipe` 明写：情绪域已饱和，IS 强 ≠ prod 过）。
- **待实测**：本区概念预算。

## ③ 归因 · 本区覆盖

- **扩批之前先按族查 prod-first**；`delay 0` 探针**单独成批**，不与 delay 1 混批。
- 本区 delay 0 多数数据集不可用（实测：`workforce_flow_skills` 报 unknown variable）⇒ 慢数据集拿不到更鲜数据。
- **待实测**：本区逐年 S 分布。

## ④ 破闸杠杆 · 本区覆盖

- **★ 同族 prod 达 0.6 → 只按决策表 D0-P 处置**（0.60–0.70 当天进步 8；达 0.75 或踩线尝试失败判 `dead_end`
  并换正交概念），**禁止同族磨参数**。
- **修复保持 `TOP3000`**；换 universe 要在 `key_findings` 写清 TOP3000 下失败的原因与要回答的诊断问题。
- **★ 中性化是本区最有效的破闸旋钮**（实测）：`SECTOR` 破 fitness/margin、
  `REVERSION_AND_MOMENTUM` / `CROWDING` 破 prod（详见 [gate-and-submit-discipline.md](gate-and-submit-discipline.md)）。
- **Mode B**：原来的 1.0 / 0.6 降门已被下限锁作废。

## ⑤ 算子穷举 · 本区覆盖

- **`ts_av_diff` > `ts_zscore(ts_backfill(...))`**：全 decay 档 +16~20%（实测 S 2.07 vs 1.78）。只减均值不除波动 ⇒ 保留幅度。**限慢变量字段**。
- **`reverse` 必须与原方向成对发批**：实测 `predicted_change` 原方向 S −1.48 → `reverse` 后 +2.13。
  判据：`|S| ≥ 1.0 且为负` ⇒ 先 reverse 再判死。
- **`winsorize(x, std=N)` 必须写具名参数**：位置写法被 toolkit 静态闸拒；具名写法会被 preflight 误报
  `unknown_fields:["std"]`（把 std 当字段名）⇒ **preflight 误报 ≠ 不可用，以 toolkit 静态闸 + 平台为准**。
- **`2Y ≥ 2.0` 且 `TO > 0.5` 是假强**：实测 `surprise_ratio` 2Y 4.03 但 TO 0.761，reverse 后 S≈0.07。
- **判毒字段看 `longCount`，不看 `coverage`**：`directional_indicator_2` 元数据 cov 0.7716，实测 longCount=0。
- **待实测**：完整算子清单（本区实测已覆盖 `ts_std_dev`/`ts_kurtosis`/`ts_corr`/`hump`/`tail`/`ts_zscore`/`ts_decay_linear`/`ts_delta` 等，
  逐算子结论见 `../references/_usa-mining-playbook-20261018.md` §2）。

## ⑥ 终验 · 本区覆盖

- **IS 八闸全过 ≠ 可提交**：必过 prod 与 self 两道相关性闸（阈值见 `PLATFORM_CHECK_LINES`，用
  `check_correlation(refresh=True)` 取值）。
- **PC 只向上漂**（生产池单调增长）：实测同日早→晚 +0.01~+0.29 ⇒ **提交前夜必须重测 PC**。
- **待实测**：本区 prod 分布全景。

## 改控制纪律

- **区域级**：`tracking/USA/config/settings.json`（仿真设置 + `_spre` 步1 产物）、`thresholds.json`（review/near/
  quick_scan/probe_scoring_v2/hard_gates）。
- **组合级**：`tracking/USA/config/cells.json`——只写覆盖值，每个覆盖在同级 `_evidence` 写证据
  （波号 / alpha id / 日期）；**没有证据的覆盖校验不通过**。改完先校验再重渲：

  ```bash
  $WQ_PY -m wqb.profiles check --region USA
  $WQ_PY -m wqb.profiles render --region USA --apply
  ```

- **⚠ 本区现状**：`cells.json` 10 个类别**零覆盖**（2026-10-18 实测）⇒ `explain` 只会给区域默认
  （`SUBINDUSTRY` / `decay 5`），而分析师族实测必须用 `SECTOR`/`RAM`/`CROWDING` + decay 10/20。
  **建议**：把分析师族的组合覆盖写进 `cells.json`（带 `_evidence`），让 `explain` 与实测一致。
  视图与三表分工见 [`../config/README.md`](../config/README.md)。
- **锁定项**（任何层都不能放宽）：禁混信号、Mode B 主闸下限、决策表 D0-P、平台线、窗口白名单、
  点塔按平台类别、提交前用户确认、truncation 不作扫描维度——全文见 `$WQ_PY -m wqb.profiles explain` 末尾。
- **证据与历史**：[USA profile](../../wq-brain-ra-pipeline/references/regions/USA.md)（入场裁决、红绿榜、证据附录）。
