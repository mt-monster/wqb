# `vRAgNK3w` 的 OS 坍塌能不能提前知道？—— 方法、实测与结论修正

> 2026-11-13｜对象：`vRAgNK3w`（EUR / risk70 / 5 算子 / w=0.18）
> 本轮**跑了实测**，不是只列方法。工具已固化：`tools/os_decay_probe.py`
> 配套数据：`results/_vkn_holdout2.json`、`_vkn_holdout_multi.json`、`_account_os_decay.json`、`_os_probe_vRAgNK3w.json`

---

## 0 直接回答

**提交前拿不到真 OS。** 平台 `os.sharpe` 只在提交后产出，且本账户 **2026-07-15 之后提交的 alpha（已 4 个月）OS 值仍为 null**；官方 `Brain Genius` 也说 Combined Alpha Performance 每 4–6 周刷新、季度最后一月提交的可能下季才计入。**提交不可逆**，等看到 OS 时已经晚了。

但有 5 种**可量化的提交前代理**，本轮全部实跑。结论比上一轮更细：

> **过拟合证据「中等偏强」，不是铁证；上一轮判「高度疑似」偏严，本轮部分修正。**
> 但账户历史先验给出的 **预期 OS ≈ 0.65**，比 holdout 的 1.34 悲观得多 ⇒ **维持「降级为补位候选」的处置结论**。

---

## 1 方法一：官方 Test Period（正解，但 API 侧有局限）

官方 `test-period` 文档原文（`learn/documentation/create-alphas/test-period`）：

> 「The Test Period feature is designed to **help you avoid overfitting**. It allows you to divide your In-Sample (IS) period into a Train and Test period… An Alpha that is developed based on the simulation results of Training Period and **performs well in both periods is likely a strong candidate for submission and may have avoided overfitting**.」

要点：
- 可把 IS 的**最后 0–5 年**设为 Test；不改仿真，只改统计/图表切分；
- 提交测试仍跑**整个 IS**；yearly stats 分蓝（Train）/橙（Test）；
- UI 需点「Show test period」，且「只有 reveal 之后才能提交」；
- `create_simulation` 有 `test_period` 参数，但本项目 `tools/submit_batch.py` 的 `SETTINGS_PASSTHROUGH` 白名单**不含 testPeriod**。

**实测局限**：`vRAgNK3w` 的 `settings.testPeriod = None`、`train`/`test`/`os` 全为 `null`。已提交的 `9qlZLVNd`、`bl6OWZ2M` 也只有 `os` 对象、`train`/`test` 仍 null ⇒ **API 侧读不到分段统计**，这是 UI 功能。

⇒ 实用替代：用 `recordsets/daily-pnl` 全量日序列**本地切 Train/Test**，与官方口径等价、零仿真成本、可对任意历史 alpha 复算。

---

## 2 方法二：本地 holdout 实测（口径已验证）

从 `GET /alphas/{id}/recordsets/daily-pnl` 取全量日 PnL（约 2579 条），日收益 = `daily_pnl / bookSize(2e7)`，`Sharpe = mean/std × √252`。

**口径校验**：算出的全期 Sharpe 与平台 `is.sharpe` 逐位吻合 —— `vRAgNK3w` 1.93/1.93、`wpo8olA6` 1.66/1.65、`9qlZLVNd` 2.05/2.04 ⇒ 方法可信。

`vRAgNK3w` 多切点结果：

| Test 起始 | Train S | **Test S** | Test/Train | 对 1.58 闸线 |
|---|---:|---:|---:|---|
| 2019 | 2.19 | **1.77** | 0.82 | ✅ 过 |
| 2020 | 2.05 | **1.84** | 0.90 | ✅ 过 |
| **2021** | **2.24** | **1.34** | **0.60** | ❌ **掉闸** |
| 2022 | 1.98 | **1.68** | 0.83 | ✅ 过 |

**只有 2021 切点掉闸**。逐年数据显示 2021 年本身 Sharpe 仅 0.69（十年次低），Test 2021–23 恰好把最弱年整段纳入 ⇒ 有「弱年聚集」成分，不能全算过拟合。

---

## 3 方法三：对照组（最关键，排除「市场共性」）

只看单颗会误判。取 risk70 同族 8 颗 + 非同族对照 6 颗，同样切 2021：

| 组 | n | Test/Train 均值 | 区间 |
|---|---:|---:|---|
| **risk70 同族** | 8 | **0.632** | 0.40 – 0.83（**全部 <1**） |
| **对照组** | 6 | **1.056** | 0.67 – 1.49（5/6 ≥0.96） |

对照明细：`wpo8olA6` 1.49、`RREPm361` 1.12、`78Yk8VR1` 1.07、`9qlZLVNd` 1.02、`omEdka3v` 0.96、`6XdkW08J` 0.67。

⇒ **不是全市场近端变差，是 risk70 这一族特有的近端衰减**。这是本轮最有力的过拟合证据。同族内部 `YPaqgZqR`(w0.30/INDUSTRY) 最差 0.40，`LLKJ9PV6`(w0.40/market) 最好 0.83。

---

## 4 方法四：参数稳定性（论坛「缩减参数空间」的加强版）

把同族不同权重 w 的 alpha 各自在 Test 段排名：

| Test 起始 | Test 段最优 w | 该颗 S | 全期所选 **w=0.18** 排名 |
|---|---|---:|---|
| 2020 | **0.40** | 2.24 | 4 / 8 |
| 2021 | **0.40** | 1.88 | 4 / 8 |
| 2022 | **0.40** | 2.01 | 3 / 8 |

⇒ **Test 段最优权重恒为 0.40，而全期闸门挑出的是 0.18，在近端只排 3–4/8**。参数选择不稳定，符合论坛 `41482855055383`「隐性过拟合」与 `43583615387543`「候选之间参数互变」的判定。也印证 w 是从网格里试出来的，不是先验。

（注意：w=0.40 的 `LLKJ9PV6` prod = 0.794 已超线判死，不能直接换。）

---

## 5 方法五：账户历史 OS 先验（把 holdout 换算成预期 OS）

从 `stage=OS` 池 200 颗中，取 **124 颗已产出 `os.sharpe`** 的，与 `is.sharpe` 配对：

| 指标 | 值 |
|---|---:|
| IS Sharpe 中位 | **1.50** |
| **真实 OS Sharpe 中位** | **0.48** |
| **OS/IS 中位** | **0.34**（均值 0.36） |
| OS < 0 | 27/124（22%） |
| OS < 1.0 | 86/124（69%） |
| OS ≥ 1.58 | 14/124（11%） |
| OS/IS ≥ 1 | 15/124（12%） |
| 按提交年 | 2025 中位 0.35；**2026 中位 0.24** |

**⚠️ 字段坑（本轮踩到并纠正）**：`os.osISSharpeRatio` 是 **OS/IS 比值**，不是绝对 OS Sharpe。验证：`LZmvE16` is 1.35 / os 0.43 → 比值 0.32；`WL5qXEG` is 1.51 / os 2.59 → 1.72。绝对 OS 要读 `os.sharpe`；另有 `sharpe60` / `sharpe125` 可看近 60/125 日 OS 趋势。

套到本颗：**IS 1.93 × 0.34 ≈ 预期 OS 0.65**。

> 这个数比 holdout 的 1.34 悲观得多，原因是 holdout 段仍在 IS 内、参数已经「见过」这段数据；真 OS 是完全未参与调参的后续年份。
> 样本偏差需说明：这些是 2025-03 ~ 2026-01 提交的早期 alpha，当时流程可能弱于现在；但 2026 组中位 0.24 更差，**不支持「近期质量已提升」的乐观假设**。

---

## 6 结论修正（相对上一轮）

上一轮我说「参数选择过程高度疑似隐性过拟合、命中纪律红线三条线」。本轮实测后应修正为：

| 方向 | 证据 |
|---|---|
| **支持过拟合（保留）** | ① risk70 族 2021 切点全族衰减 0.632 vs 对照 1.056；② Test 段最优 w 恒 0.40、所选 0.18 只排 3–4/8；③ 112 组合网格挑 w；④ F 1.01 / sub 1.01 双贴线；⑤ 论坛「纪律红线」三条线仍成立 |
| **反对「必然坍塌」（新增）** | ① 4 个切点里 **3 个过闸**（S 1.68–1.84）；② 2021 是已知弱年（逐年 0.69），对照 `6XdkW08J` 同期也只有 0.67；③ 单字段 ATOM、5 算子、经济含义清楚、十年零负年；④ 删权重后 S 反升，w 的作用是压 S 进 sub 比值闸，机制可解释 |
| **真正拉低预期的是账户先验** | OS/IS 中位 0.34 ⇒ 预期 OS ≈ 0.65。但这个衰减**对账户里几乎所有 alpha 都成立**，不是本颗独有缺陷 |

⇒ **净判断**：本颗不是「特别烂」，而是「**相对其它可交候选没有优势，且近端稳定性确实偏差**」。上一轮「降级为补位候选」的处置结论**不变**，理由从「疑似过拟合」换成更扎实的「族特异性近端衰减 + 参数不稳定 + 预期 OS 0.65」。

---

## 7 提交后怎么监控（能看，但慢且不可逆）

- 提交后 `stage` 变为 `OS`，`os` 对象会逐步填充：`sharpe`（绝对 OS Sharpe）、`osISSharpeRatio`（OS/IS 比）、`sharpe60` / `sharpe125`（近期趋势）、`returns` / `drawdown` / `fitness`、`os.checks`。
- 本账户 11-10/11-11 提交的 `78Yk8VR1` / `E5QZ1NgJ` / `9qlZLVNd`：`os.checks` 仍**全 PENDING**，`osISSharpeRatio = null`。
- 有 OS 数值的最晚提交是 **2026-01-11**；无值的最早提交是 **2026-07-15**（4 个月） ⇒ **出数延迟至少数月，或按季度批量**。
- 官方 `Brain Genius`：Combined Alpha Performance 每 4–6 周刷新；季度最后一月提交的可能不计入当季 Combined，但计入当季 Quantity/Value 与下季 Combined。
- ⇒ **等看到 OS 时，这颗已计入 Quality/Value，无法撤回**。

可定期跑：`py tools/os_decay_probe.py <id>` 看 holdout，再对照平台 `os.sharpe` 校验预测是否准。

---

## 8 可复用工具

`tools/os_decay_probe.py`（本轮新建，已跑通）：

```bash
# 单颗
py tools/os_decay_probe.py vRAgNK3w

# 带对照（推荐：单颗 holdout 会误判，必须配对照）
py tools/os_decay_probe.py vRAgNK3w wpo8olA6 9qlZLVNd --json results/probe.json

# 自定义切点
py tools/os_decay_probe.py vRAgNK3w --cuts 2020-01-01 2021-01-01 2022-01-01
```

输出：全期 Sharpe + 平台 `is.sharpe` 交叉校验 + 多切点 Test/Train 比 + Test 段是否掉 1.58 闸 + 账户先验下的预期 OS。
内置：`daily-pnl` 偶发非 JSON 的 4 次重试、`pydantic` 缺失时自动切到 `world-quant-brain-mcp/.venv` 重跑、`results/_account_os_decay.json` 存在时自动附加账户先验。

**推荐判据（可写进提交前 checklist）**：
1. 多切点 Test/Train 比 ≥0.8 且无切点掉闸；
2. **同族 vs 同区对照组的相对衰减**（比单颗绝对值更有判别力）；
3. 参数稳定性：全期最优参数在 Test 段也应排前列；
4. 预期 OS = IS × 账户 OS/IS 中位（当前 0.34），若明显低于候选池其它件则降级。

---

## 9 边界与提醒

- 所有 holdout 段都在 IS 内，**不是真 OS**，只能当代理；账户先验是历史统计，个体差异极大。
- 账户 OS 样本集中在 2025-03 ~ 2026-01，存在流程代际偏差；2026 组中位 0.24 更差。
- 本轮**未派任何新仿真、未提交任何 alpha**；`tools/os_decay_probe.py` 为纯只读。
- `os` / payment 读数属账户私有信息，官方 `Consultant Dos and Don'ts` 明令不得对外披露或转贴论坛；本报告为本地文件。

## 10 产物

| 文件 | 内容 |
|---|---|
| `tools/os_decay_probe.py` | 可复用 OS 坍塌代理探针 |
| `results/_os_probe_vRAgNK3w.json` | 3 颗探针结果（含账户先验） |
| `results/_vkn_holdout2.json` | 8 同族 + 6 对照的 2021 切点 |
| `results/_vkn_holdout_multi.json` | 多切点原始计数 |
| `results/_account_os_decay.json` | 124 颗 IS/OS 配对（账户先验） |
| `results/_vkn_pnl_raw.json` / `_vkn_daily-pnl.json` / `_vkn_sharpe.json` | 原始 record set |
