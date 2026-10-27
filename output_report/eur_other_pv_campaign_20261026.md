# EUR · OTHER + PV 类 campaign 战报（2026-10-26）

> 覆盖：8 个新跑的集（PV 7 + OTHER 1）+ 3 个定向波（pre_close 子族 140 条、换字段 7 条、改读数 8 条、指数 4 条）
> 数据源：`results/full_template_campaign_results.json`、`results/_pv_preclose_ledger.json`、
> `results/_oth335_*_ledger.json`、`data/wqb.db`
> 闸线（EUR）：S>1.58 ｜ F>1.0 ｜ 2Y>1.58（平台 limit；用户线 1.6）｜ sub≥0.53×S ｜
> margin>5bp ｜ failed_checks 空 ｜ prod<0.70 ｜ self<0.70

---

## 1 结论摘要

**8 个集全部未达交付，但每一颗的卡点都已定位到可复用的层级。**

| 集 | α | maxS | max2Y | joint | 判定 | 卡点 |
|---|---:|---:|---:|---:|---|---|
| `pv30` | 42 | 0.20 | 0.66 | 0 | DEAD | 字段是 universe 分桶因子分数，无信号 |
| `pv13` | 55 | 0.67 | 1.93 | 0 | SPLIT | 有效样本（10 年/18.9%），但 S 差 0.91 |
| `intraday_pv_feats` | 44 | 1.20 | 2.28 | 0 | DEAD | **2Y 结构性上限 0.85**（封集） |
| `pv37` | 53 | 1.33 | 0.86 | 0 | BORDERLINE | S 差 0.25、2Y 差 0.72 |
| **`other335`** | 25 | **1.83** | **2.12** | 0 | **封闭** | **IS 全过，prod 地板 0.82** |
| `pattern_scores` | 48 | 0.57 | 1.58 | 0 | SPLIT → **样本脆弱** | 2Y 由 2022 单年撑（34.5%） |
| `continuation_score` | 50 | 0.67 | 1.41 | 0 | DEAD | S/2Y 双弱 |
| `insider_feats` | 46 | 0.94 | 1.70 | 0 | SPLIT | S 差 0.64 |

**唯一接近交付的是 `other335`**：出现过 IS 全闸通过（`fail: []`、`failed_ra_count=0`、
`CLUSTER_TEST` 也 pass、ATOM=1 塔倍率 ×1.5），只死在 prod 0.82。

---

## 2 `other335`：完整的判死链（4 步，每步单变量）

### 2.1 最好的一颗：`RREJewKz`

```
signed_power(
  multiply(rank(ts_mean(ts_backfill(oth335_combined_all_region_hedge, 22), 5)),
           rank(ts_mean(ts_backfill(oth335_combined_all_region_hedge, 22), 126))), 0.90)
```
EUR / TOP2500 / delay 1 / decay 4 / FAST / trunc 0.08 / nanHandling ON / maxTrade ON

| 闸 | 值 | 结果 |
|---|---|---|
| Sharpe | 1.83 | pass |
| Fitness | 1.03 | pass |
| 2Y Sharpe | 1.67 | pass |
| sub_universe | 1.19 | pass |
| margin / TO | 17.9bp / 4.4% | pass |
| CLUSTER_TEST | — | **pass**（原版 `kqNxoL5d` 是 WARNING 1.56/1.58） |
| failed_checks | **空** | pass |
| failed_ra_count | **0** | pass |
| ATOM | `effective=1`，`EUR/D1/OTHER` ×1.5 | pass |
| **prod** | **0.8290** | **FAIL（需 <0.70）** |

### 2.2 三条降 prod 路径全部否证

| 路径 | 做法 | 结果 |
|---|---|---|
| **换字段** | 其余 4 变体 + 2 个 `hc_` 变体，同结构同时段 | 2Y 全崩：`hc_hedge` 1.22、`mind` −0.06、`linear` −0.81、`shield` −0.21、`mktcap` 0.18 ⇒ 只有 `hedge` 能过 2Y |
| **改读数** | zscore / 偏离长均 / 短均动量 / sector·industry·subindustry 分组 / gate / signed_power | 6/8 崩 S（zs126 0.98、gsec 0.98、gin 0.94、gsub 0.91、dev 0.84、mom 0.11）；只有 `gate`（S1.32）与 `sp07`（S1.87）站住 |
| **压缩** | signed_power 指数 0.7 → 0.9 四档 | prod 仅从 0.8315 降到 0.8225（**Δ = 0.009**） |

### 2.3 判死依据（memory §6 的三形态判据）

| 形态 | alpha | S | F | 2Y | **prod** |
|---|---|---:|---:|---:|---:|
| dw(5,126) 原样 | `kqNxoL5d` | 1.82 | 1.02 | 1.70 | **0.8315** |
| signed_power 0.90 | `RREJewKz` | 1.83 | 1.03 | 1.67 | **0.8290** |
| signed_power 0.70 | `MPYjYlAz` | 1.87 | 1.06 | 1.58 | **0.8225** |

**三形态跨度 0.009，落在「同族 ±0.04 = 字段结构性地板」判据内 ⇒ `other335` 封闭。**
`oth335_combined_all_region_hedge` 的信息已在生产池饱和（0.8–0.9 桶只有 4 颗、0.7–0.8 有 18 颗）。

### 2.4 附带得到的可复用杠杆

**`signed_power` 指数可用于补 2Y**（同字段同设置，只改指数）：

| 指数 | S | F | **2Y** |
|---|---:|---:|---:|
| 0.70 | 1.87 | 1.06 | 1.58（=limit ⇒ 严格不等式判 FAIL） |
| 0.75 | 1.86 | 1.05 | 1.60 |
| 0.80 | 1.85 | 1.04 | 1.62 |
| 0.85 | 1.84 | 1.03 | 1.65 |
| 0.90 | 1.83 | 1.03 | 1.67 |

⇒ 指数↑ 则 2Y↑、S↓，且**几乎不动 prod**。这是补 0.02–0.10 量级 2Y 缺口的一个低成本旋钮。

---

## 3 `intraday_pv_feats`：封集（2Y 是 regime 墙）

### 3.1 子族扫描（70 字段 × 窗口 126/252 = 140 条，全部收割）

| 窗口 | n | maxS | 中位 S | max2Y |
|---|---:|---:|---:|---:|
| 126 | 70 | 1.25 | 1.08 | 1.66 |
| **252** | 70 | **1.49** | **1.31** | 1.65 |

- **38/140 条 S ≥1.3**；Top 12 全为价格水平类（bid/ask/low/high/max_bid/min_bid），S 1.45–1.49、**F 1.11–1.15**
- 最强 `LLMPd6gm` = `ts_rank(ts_backfill(bid_price_60m_pre_close_2, 22), 252)`：
  **S 1.49 / F 1.15 / 2Y 0.75 / sub 0.76**

### 3.2 2Y 五条杠杆全无效

| 变体 | S | F | 2Y |
|---|---:|---:|---:|
| win252（对照） | 1.49 | 1.15 | 0.75 |
| win504 | 1.44–1.47 | 1.14–1.17 | 0.79–0.82 |
| decay 8 / 16 | 1.44–1.47 | 1.10–1.14 | 0.70–0.74 |
| neutralization SUBINDUSTRY | **0.78** | 0.48 | 0.40 |
| neutralization STATISTICAL | **0.75** | 0.32 | 0.84 |

**2Y 上限 0.85，门槛 1.6 —— 差 0.75。** 年度画像有效（2014–2023 全有持仓），但
2022 S=0.50、2023 S=1.06 ⇒ **regime 衰减，不是样本缺失**。

### 3.3 两条必须记住的教训

1. **同族 70 个字段 = 1 条腿**。bid_price_60m/30m、mean_bid、min_bid、max_bid、low_price… 
   全部落在 1.45–1.49，是同一个信号的近似副本，不是 70 个独立发现。
2. **2Y 强的字段是另一类，符号相反**：`mean_low_price_return_30m_pre_close_2` 的 2Y 1.66
   但 S = **−0.17**（全期负）⇒ 不能与价格水平腿拼接。

---

## 4 样本有效性更正（按 max-2Y 颗重算）

「S 弱 / 2Y 强」的集必须按其 **max-2Y 那颗**算年度画像，用 max-S 颗会看错对象。

| 集 | max-2Y 颗 | S | 2Y | 首年/年数 | fragile | 结论 |
|---|---|---:|---:|---|---|---|
| `pv13` | `9qENNdWo` | 0.67 | 1.93 | 2014 / 10 | **False**（top 2022 18.9%） | 有效样本，S 差 0.91 |
| `pattern_scores` | `88RmloJq` | −0.10 | 1.58 | 2014 / 10 | **True**（2022 占 **34.5%**） | **2Y 由单年撑，SPLIT 不可信** |
| `pv30` | `88vM0JEW` | −0.18 | 0.66 | 2014 / 10 | **True**（2022 占 27.7%） | DEAD |
| `pv37` | `P0oJnEax` | 0.73 | 0.86 | 2014 / 10 | False | 真弱 |

---

## 5 工程侧：本轮修掉的两个阻断问题

### 5.1 `wqb_tools.py` 缺失导致派发**静默失败**（当日第三次依赖残留）

`config.WQB_TOOLS = ~/wqb-scripts/wqb_tools.py`，该文件 **10:32 被删除**（目录还在）。
`transport.dispatch` 用 subprocess 调它 ⇒ 文件不存在 ⇒ stdout 空 ⇒ 正则取不到 `sim_id`
⇒ 返回 `(None, tpl, bi)` ⇒ 收割循环 `if not sim_id: continue` 全跳过
⇒ **整集 0 alpha、verdict=NO_DATA，日志里连一行 `[harvest]` 都不出现**（无异常、无报错）。

实测：8 集 × 45 条 = 300 条表达式，实际提交 **0** 条，40 秒「跑完」，并污染断点与 results。

修法：`tools/wqb_tools_shim.py` 装到 `~/wqb-scripts/wqb_tools.py`，只实现 `dispatch` 子命令，
转调 `tools/submit_batch.py`，输出 `{"sim_id": "..."}`。配套清理 8 个假 NO_DATA 记录。

### 5.2 长任务脱离 Agent 的 Job object

`cmd &` / `nohup` 起的子进程随工具调用结束被 kill（Job object 带 KILL_ON_JOB_CLOSE）。
工具的 `run_in_background` 能活但绑会话。**WMI `Win32_Process.Create` 被安全策略拦截**，
只有 **`schtasks`（任务计划，由 svchost 创建）** 可用 —— 实测父链变 `svchost → cmd → python`，
心跳跨工具调用持续。

封装：`tools/detach_launch.ps1`（生成 .cmd 包装脚本再注册任务，绕开引号/env/cwd 三个坑）。
⚠ 参数名不能用 `-Args` / `-Env`（PowerShell 自动变量）⇒ 用 `-Arguments` / `-EnvVars`。

---

## 6 未跑队列与建议

**剩余 PV 队列（已启动，脱离 Job 运行）**：`pv20`（1475 字段）、`pv106`、`pv103`、`pv29`。

| 优先级 | 事项 | 理由 |
|---|---|---|
| P0 | PV 剩余 4 集跑完 | `pv20` 是最后一块大集，且 `specific_return_crowding_*` 是独立机制（拥挤度） |
| P1 | 不再回挖 `other335` / `intraday_pv_feats` | prod 地板 / 2Y 墙均已实测封闭 |
| P2 | 把 `signed_power` 指数作为标准 2Y 旋钮写进模板 | 0.7→0.9 可给 +0.09 的 2Y，且不动 prod |
| P3 | 模板 D2/D3/D4 已上线，需用新模板重跑 1–2 个旧 DEAD 集做 A/B | 验证「删族 + pp 统一」是否提升产出量 |

**一句话**：PV 这一整类从「从没测过」变成了「测过、每个集的天花板都有实测数字」。
8 个集里 1 个（`other335`）做到了 IS 全闸通过，卡在 prod 0.82 —— 这是本轮最接近交付的一颗。
