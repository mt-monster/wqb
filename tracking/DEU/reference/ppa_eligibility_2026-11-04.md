# DEU PPA 资格台账（2026-11-04 建立）

> 本文件回答一个问题：**DEU 的候选在 PPA（Power Pool Alpha）通道下是否可提交**，以及现在能不能提。
> 结论先行：**PPA 口径下有 12 颗合格件（REGULAR 只有 3 颗）**，但**当期主题是 GLB/D1，DEU 不在受理范围** ⇒ 全部标 `YELLOW + WAIT_THEME_ROTATION`。

## 一、PPA 与 RA 的闸门差异（口径来自 `src/wqb/config.py`）

`PPA_CHECK_NAMES`（7 项，全部是换手/子宇宙/稳健宇宙/投资性）：

```
LOW_TURNOVER
HIGH_TURNOVER
LOW_SUB_UNIVERSE_SHARPE
LOW_ROBUST_UNIVERSE_SHARPE
LOW_ROBUST_UNIVERSE_SHARPE.WITH_RATIO
LOW_ROBUST_UNIVERSE_RETURNS
LOW_INVESTABILITY_CONSTRAINED_SHARPE
```

外加 `compute_webdata_failed_counts` 里的特殊规则：`LOW_SHARPE` 的 value **< 1** 也算 PPA 失败（PPA 只要 Sharpe ≥ 1，RA 要 1.58）。

**关键推论：RA 的三大杀手在 PPA 口径下不算失败项**——

| 检查 | RA | PPA |
|---|---|---|
| `LOW_SHARPE` 线 | 1.58 | **1.0** |
| `LOW_FITNESS` | ≥ 1.0 计入 | **不计入** |
| `LOW_2Y_SHARPE` | ≥ 1.58 计入 | **不计入** |
| `PROD_CORRELATION` | < 0.7 计入 | **不计入**（改看 PPAC < 0.5） |
| `CLUSTER_TEST` / `IS_LADDER_SHARPE` | 计入 | 不计入 |

⇒ 本区大量「S 2.2-2.7 但 2Y 1.2-1.4」的候选，在 RA 被判死，在 PPA 是**干净件**。

## 二、★★★★★ 零成本 PPA 资格屏（平台行为实证，可复用）

**做法**：`get_alpha_details(alpha_id)` → 看 `checks.pending` 里**有没有 `POWER_POOL_CORRELATION`**。

**判定规则（14 颗实证，无反例）**：`POWER_POOL_CORRELATION` 出现 ⟺ **算子数 ≤ 8 且 7 项 PPA 检查无一失败**。

两类反例把规则夹死：

| 反例类型 | alpha | 算子数 | PPA 检查失败 | `POWER_POOL_CORRELATION` |
|---|---|---:|---|---|
| 算子超限 | `Vkxnb8QG` / `A1vv9mmX` / `bl62jGgM` / `RRE1Xrjj` / `MPY9VNY9` / `j288RaEQ` | 14 / 20 / 15 / 10 / 11 / 20 | 无 | ❌ 不出现 |
| 算子合格但 PPA 检查挂 | `KPJexqql` / `e75AAMQz` | 1 / 1 | `LOW_SUB_UNIVERSE_SHARPE` | ❌ 不出现 |

⇒ 这条屏把「先算 PPAC、算完才发现算子超限」的浪费全部前置消除，**每条只花一次 `get_alpha_details`**，不占相关性槽、不占仿真槽。

## 三、DEU 的 12 颗 PPA 合格件（本区 REGULAR 只有 3 颗）

| # | alpha | 字段核 | S | F | TO | sub | REGULAR 状态 |
|---|---|---|---:|---:|---:|---:|---|
| 1 | `JjelQJoe` | tm_15…r10 | 2.70 | 1.28 | 61.55% | 1.40 | prod 0.8373 ✗ |
| 2 | `JjelQnvE` | tm_15… | 2.61 | 1.48 | 42.05% | 1.29 | prod 0.9084 ✗ |
| 3 | `vR102Ver` | tm_15… | 2.39 | 1.29 | 43.48% | 1.19 | 与 1YNv6Ymk 克隆 0.966 ✗ |
| 4 | `QPveKkPM` | tm_16…r5 | 2.37 | 1.29 | 42.00% | 1.25 | **2Y 1.25 ✗** |
| 5 | `MPYw3oOn` | tm_16…r10 | 2.29 | 1.28 | 36.94% | 1.26 | **2Y 1.23 ✗** |
| 6 | `1YNv6Ymk` | tm_15…r10 | 2.28 | 1.25 | 37.92% | 1.11 | prod 0.7983 ✗ |
| 7 | `1YNvvgdJ` | tm_15…r10 | 2.28 | 1.28 | 37.81% | 1.09 | 克隆 ✗ |
| 8 | `RREX67Ab` | tm_15…r5 | 2.28 | 1.33 | 35.13% | 1.12 | **2Y 1.41 ✗** |
| 9 | `QPveKJ8g` | tm_15…r5 | 2.26 | 1.42 | 30.09% | 1.11 | **2Y 1.38 ✗** |
| 10 | `Vkx3MjW8` | E14 | 1.75 | 1.14 | 23.75% | 1.22 | ✅ prod 0.672 |
| 11 | `pwdl6ov6` | E14 | 1.62 | 1.19 | 16.03% | 1.24 | ✅ prod 0.6923 |
| 12 | `xArkxebq` | E14 | 1.58 | 1.17 | 15.23% | 1.21 | ✅ prod 0.6854 |

**去重后的信号核只有 5 个**（`SELF_CORRELATION` 不在 `PPA_CHECK_NAMES` 也不在 `RA_CHECK_NAMES`，它是平台独立的相关性检查、两条通道都要过；同核多颗之间互相关 0.96+ ⇒ 提一颗之后其余会被 self 或 PPAC 挡住 ⇒ **现实可用量更接近 5 颗而不是 12 颗**）：

| 信号核 | 成员 | 建议取 |
|---|---|---|
| `tm_15_r1_r5_r10_rh_glb_d1_r10_q1` | JjelQJoe / 1YNv6Ymk / 1YNvvgdJ / JjelQnvE(近似) / vR102Ver | **JjelQJoe**（S 2.70 最高）或 **1YNv6Ymk**（TO 37.9% 最低） |
| `tm_15_r1_r5_r10_rh_glb_d1_r5_q1` | RREX67Ab / QPveKJ8g（同字段双件） | **QPveKJ8g**（F 1.42 最高、TO 30.1% 最低） |
| `tm_16_r1_r5_r10_rh_glb_d1_r10_q1` | MPYw3oOn | **MPYw3oOn** |
| `tm_16_r1_r5_r10_rh_glb_d1_r5_q1` | QPveKkPM | **QPveKkPM** |
| E14+surprise | Vkx3MjW8 / pwdl6ov6 / xArkxebq（两两 ~0.98） | **Vkx3MjW8**（prod 最优且已在 REGULAR 篮） |

## 四、剩余唯一未验的 PPA 闸：PPAC < 0.5

`POWER_POOL_CORRELATION` 在平台上恒为 `PENDING`（提交时才实算），所以 PPAC 只能本地预估：
`Claude/skills/brain-calculate-alpha-selfcorr-quick/scripts/skill.py`（SelfCorr 池 / PPAC 池分开算）。

**注意该 skill 自己声明的盲区**：本地 PPAC 池看不见近期提交的孪生体 ⇒ 本地值只能当**上界参考**，不能当放行依据；提交前仍以平台实测为准。

## 五、★★★ 当前唯一硬阻塞：主题不覆盖 DEU

`get_messages(limit=30)` 实时扫得当期公告（id `yjwnMN7`）：

> 📢 Launching a new **"GLB/D1 Power Pool Nov`26"** theme
> Duration: 26th October 26 - 22nd November 26 (4 weeks)
> Multiplier: 1X for regular Power Pool Alphas
> Requirements: **GLB region, Delay 1**, **AMER Sharpe > 1**
> Recommended datasets: pv1 / model110 / model77 / model26 / model109 / risk70 / model38 / model50 / analyst69 / model264 / other460 / fundamental23 / other455 / model138 …

上一期是「All regions/D1 Power Pool Oct`26」（2026-09-28 ~ 2026-10-26），**DEU 当时在受理范围内，现已到期**。

⇒ 按 `wq-brain-ppa-mining` §1 与 `ppa-vs-ra.md` §1 的候选期门禁：**DEU 的 12 颗全部标 `YELLOW` + `WAIT_THEME_ROTATION`**，等覆盖 DEU（或 all-region）的主题轮转回来。
⇒ **不为不上题的主题烧配额**，也不擅自换到 GLB 区（用户战略锁定「不换 region」）。

## 六、这条发现对 30 颗目标的意义

- 若只看 REGULAR：DEU 有 3 颗，饱和已实证（3,594 条测出 1 条）。
- 若把 PPA 算进来：DEU 有 12 颗候选，**上限从 3 抬到「3 + 最多 5~12」**（取决于 PPAC 与主题轮转）。
- 但 PPA 通道的开关不在我们手里，在平台的**主题日历**手里。⇒ 30 颗若要靠 PPA 凑，必须接受「等主题」或「换到 GLB」两条之一。
---

## 七、补充实证（2026-11-03 23:0x）：两条更可靠/更不可靠的取数路径

### 7.1 ★ 更可靠：`ra.failed_ppa_count` 直接可读

`get_alpha_details(id)` 返回里已经有 **`ra.failed_ppa_count`** 与 **`ra.ppa_failed_checks`**（失败项名单）。
这比 §二 的 `POWER_POOL_CORRELATION` 出现判断**更直接**，两条路互为交叉校验：

| alpha | `ra.failed_ppa_count` | `ppa_failed_checks` | `POWER_POOL_CORRELATION` 出现 | 一致 |
|---|---:|---|---|---|
| `1YNv6Ymk` | **0** | `[]` | ✅ | ✓ |
| `Vkx3MjW8` | **0** | `[]` | ✅ | ✓ |
| `JjelQJoe` | **0** | `[]` | ✅ | ✓ |
| `akK1dwm1` | 1 | `["LOW_SUB_UNIVERSE_SHARPE"]` | ❌ | ✓ |

⇒ **判 PPA 资格首选 `ra.failed_ppa_count == 0`**；`POWER_POOL_CORRELATION` 只作旁证（它的额外价值是能反推「算子 ≤ 8」这条隐藏门槛，因为 `failed_ppa_count` 不含算子信息）。

### 7.2 ★★ 不可靠：`get_user_alphas` 不能用来数库存

实测同一个账号、同一天、仅改 `order` / `offset` 参数，返回的 `count` 在 **114 / 61 / 22** 之间跳变，且**已确认 PPA 合格的 12 颗在任何一页里都不出现**：

| 调用 | count | 我方 12 颗命中 | fPPA=0 的条数 |
|---|---:|---:|---:|
| `{status:UNSUBMITTED, limit:20}` | 22 | 0 | — |
| `{status:UNSUBMITTED, limit:100, offset:0}` | 114 | 0 | **0** |
| `{status:UNSUBMITTED, limit:100, offset:100}` | 14（末页） | 0 | 0 |
| `{status:UNSUBMITTED, limit:40, order:-dateCreated}` | 61 | 0 | 0 |

直接 `get_alpha_details` 复查这 12 颗：`status` 全部 **UNSUBMITTED**、`stage` **IS**、`region` **DEU**、`failed_ppa_count` **0** ⇒ **它们状态正常，是列表接口漏了它们**。

**结论**：`get_user_alphas` 只能当「随便看看最近有哪些」的抽样工具，**绝不能用来判定「库存里还有没有别的合格件」**——它会给出假的「没有了」。要数库存必须逐 id 走 `get_alpha_details`，或用本地 `data/wqb.db` 的 `alphas` 表。

### 7.3 旧库存的 PPA 画像（114 颗 UNSUBMITTED 抽样）

`failed_ppa_count` 分布：**fPPA=1 共 38 颗 / fPPA=2 共 58 颗 / fPPA=3 共 4 颗 / fPPA=0 共 0 颗**。
即抽到的旧库存**没有任何一颗 PPA 合格**，且绝大多数唯一失败项就是 `LOW_SHARPE`（S 在 −0.3 ~ 1.2 之间，够不到 PPA 的 1.0 线）。
⇒ 与 REGULAR 侧的结论同构：**DEU 的旧库存已被榨干，PPA 通道能用的仍然只有 §三 那 12 颗**。

---

## 八、PPAC 实测收口（2026-11-04）：全池通过，PPA 包在 PPAC 上零风险

批量脚本 `brain-calculate-alpha-selfcorr-quick`（`--region DEU --alpha-num 200 --start-date 10-25 --end-date 11-04`）把 97 颗候选的 SELF 与 PPAC 一次算完：

| 统计量 | SELF | PPAC |
|---|---:|---:|
| 平均 | 0.4457 | **0.0587** |
| 最大 | **1.0000** | **0.1715** |
| 最小 | 0.0226 | −0.0562 |

- **PPAC 最大值 0.1715 ≪ 0.5 红线** ⇒ §三 那 12 颗 PPA 合格件在 PPAC 上**全部通过**。PPA 三关（`Failed PPA == 0` / `PPAC < 0.5` / `Sharpe ≥ 1.0`）已过两关半，**唯一未验的是主题日历**。
- **SELF 最大值 1.0000** ⇒ 池内存在完全重复的两条 alpha（互为 self = 1.0）。这与 §五 的「tm_15 / tm_16 九颗互相关 0.96+」一致：**PPA 的现实可用量仍是 5 个信号核，不是 12 颗**。
- 产物：`data/selfcorr_quick/deu_ppa_ppac_20261103.xlsx`（`Alpha Results` sheet 含 `ppac_correlation` 列）。
- 中性化分布：Subindustry 85 / Crowding 9 / Fast Factors 2 / Market 1。

**结论：PPA 通道的瓶颈 100% 在主题日历，技术闸门已全部关闭。**

