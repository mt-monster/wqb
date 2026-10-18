# USA 配置视图（config/）

> ⚠ **本目录不是事实源**。控制值真身在 `tracking/USA/config/`，本目录只提供**视图 + 差异说明 + 证据索引**。
> 原因：`wqb.profiles explain / render / sync-cells` 按 `tracking/<R>/config/` 解析，
> 且覆盖值强制带 `_evidence`；把真身搬进 skill 会复制事实源并断掉整条 profiles 链。
> 改配置的**唯一正确入口**见 [`../rules/six-step-usa-override.md`](../rules/six-step-usa-override.md) 的「改控制纪律」。

## 三表分工

| 表 | 管什么 | 真身 | 谁消费 |
|---|---|---|---|
| `settings.json` | 区域固定仿真设置（instrumentType / region / universe / delay / neutralization / decay…）+ `_spre_*` 步 1 产物（排除族、正交方向、win 配方、prod 饱和记录） | `tracking/USA/config/settings.json` | `profiles explain` / `workflow_batch_track` / 各类 builder |
| `thresholds.json` | 审查阈值（`review` / `near` / `quick_scan` / `probe_scoring_v2` / `hard_gates`） | `tracking/USA/config/thresholds.json` | 评分与审查流程 |
| `cells.json` | **组合级覆盖**（区域 × 类别）：回测设置 / 阈值 / Mode B 主闸；每个覆盖必须同级 `_evidence` | `tracking/USA/config/cells.json` | `profiles explain --dataset` / `batch_track --set` |

## 本区差异要点（as_of 2026-10-18）

- **区域默认档**：`TOP3000 / delay 1 / SUBINDUSTRY / decay 5 / trunc 0.08`。
- **⚠ 关键落差**：`cells.json` 10 个类别**零覆盖** ⇒ `explain` 只会输出上面的区域默认档，
  而 2026-10 两战役实测结论是：分析师族必须 `SECTOR` / `RAM` / `CROWDING` 中性化 + `decay 10~20`。
  **建议**：把这两个分析师族组合的覆盖写入 `cells.json` 并附 `_evidence`（alpha id + 日期），
  让 `explain` 与实测一致，避免"按 explain 派发却复现不出既有结论"。
- **已点亮塔（2026-10-18 实测）**：`model=4 / analyst=1 / earnings=1`；其余塔 0 颗
  ⇒ 新战役优先在未点亮塔选集（配合 `settings.json` 的 `_spre_20260917.excluded_families` 23 个饱和/枯竭族）。

## 机器可读视图

`region_view.json` 是本目录的结构化摘要（差异要点 + 真身指针 + 塔快照），
供工具/人快速读取；**改配置后须同步更新本视图的 `as_of` 与要点**。

```bash
# 权威口径永远是真身
$WQ_PY -m wqb.profiles explain --region USA --dataset analyst
$WQ_PY -m wqb.profiles check   --region USA
```
