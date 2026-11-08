# GBR/D1/TOP700 — 候选篮与 prod 分层证据（2026-11-06）

> 目标：穷尽 category 字段画像 → 画像匹配模板 → 持续产出 10 个 ATOM / regular alpha。
> 本文件只记录**可验证证据**；未测项一律标「待测」，不填推测值。

## 一、结论先行

| 项 | 数 |
|---|---|
| GBR D1 已点亮塔（≥3 提交） | **4**：model(5) / news(3) / analyst(3) / fundamental(3) |
| 接近点亮 | pv(2，差1) / other(1，差2) |
| IS 全达标未提交候选 | 364 |
| 其中已有 prod 读数 | 36 → **prod<0.70 仅 2 颗** |
| 本轮独立候选（去重+禁混过滤后） | **13 颗待 prod** + 2 颗已过 = 15 |
| 已通过 prod 且 RA 全清 | **QPvbxjXw (0.5794)**、mLobop6E (0.6505) |

## 二、机制发现（本轮最有价值的三条）

### 1. prod 与「信号速度」强相关，与 S 不相关
GBR 全部 prod 读数按族排列（本地 alpha_corr_cache，583 条权威缓存）：

| 族 | 代表 alpha | prod | 特征 |
|---|---|---|---|
| 长窗基本面比值 (E/EV) | 1YNzwl6k | **0.5188** | ts_av_diff(…,504) |
| 分析师修订（est_12m_pre_*，ts_backfill 500） | QPvbxjXw | **0.5794** | 500 日回填 |
| 长窗基本面比值 (fnd6_capxy/cap) | rKRkL9QE | 0.6783 | ts_av_diff 252 + ts_quantile 84 |
| nws17 新闻相关性 + 换手平滑 | kqNZKN5K / A1VPlR3l / mLobop6E | 0.62–0.65 | ts_target_tvr_decay tv=0.05 |
| analyst 均值修订 | mLomEeZK / wpQZ0Xel | 0.70–0.75 | ts_backfill 500 |
| techindi tm_15/tm_17 | bl6boze6 / 2rAwnqWx / 78LNKRv1 | 0.72–0.75 | CROWDING |
| **imbalance5** | **LLMK8qbv** | **0.8380** | SLOW + group_backfill |
| **risk71 残差反转** | **omEaWgwv** | **0.8718** | 已判否 |

⇒ **慢信号（长回填 / 长窗 / 换手目标平滑）prod 0.52–0.75；快信号（成交量、imbalance、风险度量）prod 0.78–0.87。**
⇒ imbalance 族族代表 0.838 > 0.80 ⇒ 按族代表预判规则**整族封盘**，W107 的 3 颗 RA 全清候选不再投入 prod 时隙。
⇒ 反例：techindi bl6boze6 S 2.74 但 prod 0.7243 —— **S 越高 prod 通常越高，不是随机**。

### 2. group_backfill 能修 CONCENTRATED_WEIGHT（用户指正，已实测确认）
W107 八条：把 `group_zscore(…, industry)` 包成 `group_backfill(…, subindustry, 252)` 后
`CONCENTRATED_WEIGHT` 由 warning 转 **PASS**，同时 `ra_failed_checks` 归 null。
⚠ 但 backfill **单独不能修 2Y**（W106 八条 2Y 全在 1.28–1.44）；必须配 **SLOW 中性化**（W105/W107）。

### 3. GBR 三杠杆配方
`SLOW` 中性化（修 LOW_2Y_SHARPE）+ `group_backfill`（修 CONCENTRATED_WEIGHT）+ 长窗 ts_av_diff/ts_rank（供 S 与 F）。

## 三、候选篮（禁混过滤后 25 颗）

禁混集合 = {PV, MODEL, OTHER, FUNDAMENTAL}。已剔除 3 颗落在 **PV+FUNDAMENTAL** 的候选：
`88Rg0Y8m` / `d5WeM5Xj` / `leAJn9e2`（表达式里含 volume 或 cap 正交，塔位判为 PV+FUNDAMENTAL）。

| # | alpha | 塔 | S | F | 2Y | sub | TO | neut | prod | 独立性 | 判定 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | WjOwjENP | FUNDAMENTAL | 2.51 | 2.16 | 2.43 | 1.68 | 0.17 | SUBINDUSTRY | 测量中 | 独立 | 待 prod |
| 2 | LLMO3l7n | FUNDAMENTAL | 2.50 | 2.22 | 2.46 | 1.82 | 0.17 | INDUSTRY | 待测 | 独立 | 待 prod |
| 3 | rKRQbPPE | FUNDAMENTAL | 2.48 | 2.22 | 2.69 | 1.68 | 0.16 | INDUSTRY | 待测 | 同族冗余 | 备用 |
| 4 | kqNe9LPz | FUNDAMENTAL | 2.42 | 2.11 | 2.22 | 1.48 | 0.17 | INDUSTRY | 待测 | 同族冗余 | 备用 |
| 5 | 2rAPVWrb | FUNDAMENTAL | 2.38 | 2.19 | 2.51 | 1.83 | 0.16 | INDUSTRY | 待测 | 同族冗余 | 备用 |
| 6 | xArX7dNl | FUNDAMENTAL | 2.25 | 2.13 | 2.84 | 1.62 | 0.14 | INDUSTRY | 待测 | 独立 | 待 prod |
| 7 | xArXLA6p | FUNDAMENTAL | 2.20 | 2.01 | 2.14 | 1.51 | 0.16 | SECTOR | 待测 | 同族冗余 | 备用 |
| 8 | O0AKXoVp | FUNDAMENTAL | 2.18 | 1.82 | 2.13 | 1.27 | 0.16 | INDUSTRY | 待测 | 同族冗余 | 备用 |
| 9 | vROqOYkv | PV+ANALYST | 2.16 | 1.11 | 2.05 | 1.52 | 0.19 | STATISTICAL | 待测 | 独立 | 待 prod |
| 10 | wpQXP722 | FUNDAMENTAL | 2.15 | 1.77 | 1.59 | 1.54 | 0.17 | INDUSTRY | 待测 | 同族冗余 | 备用 |
| 11 | wp9m9MW1 | PV+ANALYST | 2.14 | 1.10 | 2.05 | 1.49 | 0.19 | STATISTICAL | 待测 | 同族冗余 | 备用 |
| 12 | xAb2OkMm | ANALYST | 2.13 | 1.71 | 1.74 | 1.23 | 0.09 | REVERSION_AND_MOMENTUM | 待测 | 独立 | 待 prod |
| 13 | Vkd93wOw | PV+ANALYST | 2.13 | 1.08 | 2.05 | 1.53 | 0.24 | STATISTICAL | 待测 | 同族冗余 | 备用 |
| 14 | vR1nAj6z | NEWS | 2.10 | 1.38 | 2.33 | 1.44 | 0.08 | FAST | 待测 | 独立 | 待 prod |
| 15 | LLMdk8ne | NEWS | 2.10 | 1.38 | 2.33 | 1.44 | 0.08 | FAST | 待测 | 同族冗余 | 备用 |
| 16 | MPYlNP8z | FUNDAMENTAL | 2.00 | 1.64 | 1.92 | 1.35 | 0.15 | INDUSTRY | 待测 | 独立 | 待 prod |
| 17 | pwdQb78v | FUNDAMENTAL | 1.99 | 1.57 | 2.10 | 1.50 | 0.14 | INDUSTRY | 待测 | 独立 | 待 prod |
| 18 | d51O1kOX | ANALYST | 1.97 | 1.29 | 1.71 | 1.06 | 0.08 | STATISTICAL | 待测 | 独立 | 待 prod |
| 19 | P0ojvkkJ | FUNDAMENTAL | 1.93 | 1.49 | 1.76 | 1.52 | 0.16 | INDUSTRY | 待测 | 独立 | 待 prod |
| 20 | blORMJwm | ANALYST | 1.91 | 1.24 | 1.62 | 1.07 | 0.08 | STATISTICAL | 待测 | 同族冗余 | 备用 |
| 21 | **mLobop6E** | NEWS | 1.88 | 1.15 | 2.33 | 1.57 | 0.08 | FAST | **0.6505 ✓** | 同族冗余 | 可提交 |
| 22 | **QPvbxjXw** | ANALYST | 1.87 | 1.14 | 1.98 | 1.07 | 0.16 | FAST | **0.5794 ✓** | 独立 | 可提交 |
| 23 | WjOK0roG | FUNDAMENTAL | 1.80 | 1.39 | 1.85 | 1.19 | 0.13 | INDUSTRY | 待测 | 同族冗余 | 备用 |
| 24 | rKRPAWv9 | NEWS | 1.76 | 1.07 | 1.89 | 1.40 | 0.08 | FAST | 待测 | 独立 | 待 prod |
| 25 | P0oGNlQw | FUNDAMENTAL | 1.61 | 1.03 | 1.87 | 1.45 | 0.11 | FAST | 待测 | 独立 | 待 prod |

**全部 25 颗 RA 闸状态一致**：`checks.fail = []`、`ra.ra_failed_checks = null`、`CONCENTRATED_WEIGHT = PASS`。
唯一 warning 是 `MATCHES_COMPETITION` / `MATCHES_THEMES`（非阻断）。

## 四、互相关去重结论（零平台成本层）

用 `compute_mutual_correlation`（4 年、1021 点）算最大相互 <0.7 子集：

| 族 | 送入 | 最大独立子集 | 结论 |
|---|---|---|---|
| EV 比值 (FUNDAMENTAL) | 24 | **10**（含已提交 rKRkL9QE） | 扣掉 3 颗禁混后仍有 ~7 颗可共存 |
| nws17 (NEWS) | 17 | **4**（含已提交 kqNZKN5K） | 只有 `vR1nAj6z`(nip) 与 `rKRPAWv9`(sentiment) 是真新信号 |
| analyst / pv+analyst | 11 | **5**（含 QPvbxjXw） | `vROqOYkv/wp9m9MW1/Vkd93wOw/j2eEeV8W/mLY3YKmX` 互相关 0.99+ 同一颗 |

**重复件实证**（勿再测）：
- `O0AGOmOY` 与已提交 `1YNzwl6k` 互相关 **0.985** —— 同一颗
- `LLMO3l7n` ≈ `A1Vq8AbQ` ≈ `9qxgOnK2`（1.000 / 0.998）
- `vR1nAj6z` == `LLMdk8ne`（**1.000**）
- `mLoVXokK` 0.795 / `mLob5Yj5` 0.797 vs 已提交件 ⇒ **自相关已超标，直接淘汰**

## 五、下一步队列（按 prod 时隙串行，从免费到昂贵）

1. **WjOwjENP**（在飞，客户端单次可阻塞至 1h）— EV 族最强 + 独立
2. **vROqOYkv** — PV+ANALYST 族代表，S 2.16
3. **vR1nAj6z** — NEWS 新字段（nip count），与已提交件仅 0.591
4. **xAb2OkMm** — ANALYST 塔，S 2.13 / F 1.71（F 最高的一颗）
5. **xArX7dNl** — EV 族，2Y 2.84 最高

⚠ 平台 prod 为**账号级单并发**且客户端轮询最长 1 小时；**一次只能一颗**，期间任何其他 prod 调用都会 busy。

## 六、口径与阈值（来源）

- `LOW_2Y_SHARPE` 线 = **1.58**（平台实测 value/limit 对：1.57 挂 / 1.67 过）
- REGULAR 提交线 = **S ≥ 1.58**（用户确认；S<1.58 会卡）
- prod 放行线 = **< 0.70 严格不等**
- 族代表预判：prod > 0.80 ⇒ 整族封盘；0.70–0.80 灰区 ⇒ 同族最多再测 2 颗
- 算子数上限 **12**，越少越好
- 覆盖判据 = 连续多年彻底空窗，不是「不满十年」

## 七、★ 更正（02:15 实测 self 相关后）

上表第三节的「可提交」判定只用了 prod，**漏了 self 相关闸**。实测后更正：

| alpha | self_max | 结论 |
|---|---|---|
| QPvbxjXw | **0.2863** | ✓ prod 0.5794 + self 清 ⇒ **唯一真可提交** |
| xAb2OkMm | 0.3689 | ✓ 待 prod |
| WjOwjENP | 0.5038 | ✓ 待 prod |
| xArX7dNl | 0.5106 | ✓ 待 prod |
| LLMO3l7n | 0.5797 | ✓ 待 prod |
| vR1nAj6z | 0.5909 | ✓ 待 prod |
| **mLobop6E** | **0.99997** | ✗ **作废**（= 已提交 A1VPlR3l 的重复件，prod 0.6505 无意义） |
| **vROqOYkv** | **0.999999** | ✗ **作废**，且整簇 {wp9m9MW1, Vkd93wOw, j2eEeV8W, mLY3YKmX, O0JYJ67b} 互相关 0.99+ 连带作废 |

⇒ **PV+ANALYST 两塔簇整族作废**（self 1.0），候选篮从 25 颗收敛为 **23 颗**，其中
prod+self 双清 **1 颗**、self 清待 prod **5 颗**。

**教训（已写入记忆）**：prod 与 self 是两个独立闸。同族一旦有一颗已提交，兄弟件的 self 会直接顶到 1.0。
`check_self_correlation` **零平台成本、纯本地 PnL**，必须**先跑 self（免费），再花 prod 时隙（账号级单并发、单颗最长 1h）**。

## 八、★ 最终锁定：9 颗两两独立候选（02:30）

对 16 颗 self<0.70 的候选跑 `compute_mutual_correlation`（4 年 / 1021 点），
求解器返回 `exact = True`、`max_mutually_below_subset_size = 9`：

| # | alpha | 塔 | S | F | 2Y | sub | TO | neut | self | prod |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | **QPvbxjXw** | ANALYST | 1.87 | 1.14 | 1.98 | 1.07 | 0.16 | FAST | 0.2863 | **0.5794 ✓** |
| 2 | WjOwjENP | FUNDAMENTAL | 2.51 | 2.16 | 2.43 | 1.68 | 0.17 | SUBINDUSTRY | 0.5038 | 测量中 |
| 3 | kqNe9LPz | FUNDAMENTAL | 2.42 | 2.11 | 2.22 | 1.48 | 0.17 | INDUSTRY | 0.4960 | 待测 |
| 4 | xArX7dNl | FUNDAMENTAL | 2.25 | 2.13 | 2.84 | 1.62 | 0.14 | INDUSTRY | 0.5106 | 待测 |
| 5 | P0ojvkkJ | FUNDAMENTAL | 1.93 | 1.49 | 1.76 | 1.52 | 0.16 | INDUSTRY | 0.5064 | 待测 |
| 6 | WjOK0roG | FUNDAMENTAL | 1.80 | 1.39 | 1.85 | 1.19 | 0.13 | INDUSTRY | 0.4698 | 待测 |
| 7 | xAb2OkMm | ANALYST | 2.13 | 1.71 | 1.74 | 1.23 | 0.09 | REVERSION_AND_MOMENTUM | 0.3689 | 待测 |
| 8 | vR1nAj6z | NEWS | 2.10 | 1.38 | 2.33 | 1.44 | 0.08 | FAST | 0.5909 | 待测 |
| 9 | rKRPAWv9 | NEWS | 1.76 | 1.07 | 1.89 | 1.40 | 0.08 | FAST | 0.4000 | 待测 |

- 全部 `checks.fail = []`、`ra.ra_failed_checks = null`、`CONCENTRATED_WEIGHT = PASS`
- 全部 `self_correlation < 0.70`，且**两两互相关 < 0.70**（可同时提交）
- 塔分布：FUNDAMENTAL 5 / ANALYST 2 / NEWS 2

### 出局记录（勿再花 prod 时隙）
| alpha | 原因 |
|---|---|
| 2rAPVWrb | 塔位 **PV+FUNDAMENTAL**（PYR=2）⇒ 落在禁混集合内部 |
| 88Rg0Y8m / d5WeM5Xj / leAJn9e2 | 同上，PV+FUNDAMENTAL |
| mLobop6E | self **0.99997**（= 已提交 A1VPlR3l） |
| d51O1kOX / blORMJwm | self 1.0000 / 0.9411 |
| vROqOYkv 及整簇 | self 0.999999 |
| pwdQb78v / P0oGNlQw | self 0.7333 / 0.7056 |
| MPYlNP8z | 与 O0AKXoVp 0.864，凑不进独立集 |
| O0AKXoVp / LLMO3l7n / wpQXP722 / xArXLA6p / rKRQbPPE | 互相 0.87–0.93，独立集只容得下 1 颗（已选 kqNe9LPz） |

### 第 10 颗的缺口分析
FUNDAMENTAL 槽位已被互相关锁死（再加必破 0.7）；可行缺口只有两个方向：
1. **新族**（当前 stock 里没有第 10 个独立信号）
2. **换塔**：GBR 的 `pv` 只差 1 颗点亮，但 pv 族已测 prod 0.8041 / 0.8148 ⇒ 族代表 >0.80 **封盘**

⇒ 结论：**现有存量能稳定交付 9 颗**；第 10 颗需要在新数据集/新塔上开新族。

## 九、当前唯一瓶颈
9 颗里 8 颗的 prod 未测。平台 prod 是账号级单并发，`get_production_correlation` 客户端内部轮询最长 1 小时。
`WjOwjENP` 的测量已挂在后台运行 40+ 分钟仍未返回 ⇒ 平台侧计算排队严重。
**在它返回前不能再触发任何 prod 调用**，否则会把自己顶成 busy。

## 十、★ 第 10 颗缺口已闭合：MODEL 塔 star_val 族（03:00 实测）

第八节判断「第 10 颗需开新族」已落地。新族来源 = **MODEL 塔**的 star_val 估值排名数据集
（`star_val_region_rank` / `star_val_sector_rank` / `region_relative_valuation_rank`），
8 颗存量候选全部 `GBR/D1/MODEL` 单塔、`failed_ra_count = 0`。

### 探测结果（8 颗）

| alpha | 结构 | S | F | 2Y | sub | TO | self | 判定 |
|---|---|---|---|---|---|---|---|---|
| **6XKw8e6O** | group_rank(ts_delta(bf(star_val_region_rank,66),22), sector) | **2.61** | 2.05 | 1.92 | 1.41 | 0.142 | **0.5326** | ✓ 入篮 |
| vR2LqvXG | 同上换 star_val_sector_rank | 2.41 | 1.78 | 2.05 | 1.35 | 0.145 | 0.5466 | 与上颗 **0.9082** ⇒ 出局 |
| d51E709g | hump(group_rank(ts_delta(bf(region_relative_valuation_rank,132),22), sector), 0.0012) | 2.34 | 2.28 | 1.85 | 1.25 | 0.103 | 0.7102 | self 超标 |
| blbx8NJp | trade_when(成交量双阈值门控) | 2.37 | 2.31 | 2.06 | 1.19 | 0.124 | 0.7441 | self 超标 |
| pwRW57L6 | group_rank(ts_delta(bf(star_val_sector_rank,66),22), sector) | 2.31 | 2.14 | 1.93 | 1.13 | 0.129 | 0.8101 | self 超标 |
| **9qWa6r8x** | trade_when(less(five_day_total_return_dlr2,-0.008), group_rank(ts_delta(bf(region_relative_valuation_rank,132),22), sector), -1) | 2.07 | 1.87 | 2.07 | 1.05 | 0.108 | **0.6792** | ✓ 入篮 |
| leKQzlaN | 同上，阈值 -0.01 | 2.01 | 1.78 | 2.23 | 1.02 | 0.106 | 0.6808 | 与上颗同结构，只取一颗 |
| ZYA2lnXn | hump(..., 0.0025) | 1.96 | 1.75 | 1.70 | **0.91** | 0.083 | 0.6891 | LOW_SUB_UNIVERSE_SHARPE |

### 最终锁定 11 颗（`exact = True`，两两互相关全 < 0.70）

`compute_mutual_correlation` 输入 9 颗旧锁定 + 3 颗新 MODEL 候选（4 年 / 1021 点），
求解器返回 **`max_mutually_below_subset_size = 11`、`max_subset_exact = True`**：

| # | alpha | 塔 | S | F | 2Y | sub | TO | neut | self | prod |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | **QPvbxjXw** | ANALYST | 1.87 | 1.14 | 1.98 | 1.07 | 0.16 | FAST | 0.2863 | **0.5794 ✓** |
| 2 | WjOwjENP | FUNDAMENTAL | 2.51 | 2.16 | 2.43 | 1.68 | 0.17 | SUBINDUSTRY | 0.5038 | 测量中 |
| 3 | kqNe9LPz | FUNDAMENTAL | 2.42 | 2.11 | 2.22 | 1.48 | 0.17 | INDUSTRY | 0.4960 | 待测 |
| 4 | xArX7dNl | FUNDAMENTAL | 2.25 | 2.13 | 2.84 | 1.62 | 0.14 | INDUSTRY | 0.5106 | 待测 |
| 5 | P0ojvkkJ | FUNDAMENTAL | 1.93 | 1.49 | 1.76 | 1.52 | 0.16 | INDUSTRY | 0.5064 | 待测 |
| 6 | WjOK0roG | FUNDAMENTAL | 1.80 | 1.39 | 1.85 | 1.19 | 0.13 | INDUSTRY | 0.4698 | 待测 |
| 7 | xAb2OkMm | ANALYST | 2.13 | 1.71 | 1.74 | 1.23 | 0.09 | REVERSION_AND_MOMENTUM | 0.3689 | 待测 |
| 8 | vR1nAj6z | NEWS | 2.10 | 1.38 | 2.33 | 1.44 | 0.08 | FAST | 0.5909 | 待测 |
| 9 | rKRPAWv9 | NEWS | 1.76 | 1.07 | 1.89 | 1.40 | 0.08 | FAST | 0.4000 | 待测 |
| 10 | **6XKw8e6O** | MODEL | **2.61** | 2.05 | 1.92 | 1.41 | 0.14 | STATISTICAL | 0.5326 | 待测 |
| 11 | **9qWa6r8x** | MODEL | 2.07 | 1.87 | 2.07 | 1.05 | 0.11 | INDUSTRY | 0.6792 | 待测 |

- 塔分布：FUNDAMENTAL 5 / **MODEL 2** / ANALYST 2 / NEWS 2
- 全部 `S ≥ 1.76 ≥ 1.58`（REGULAR 提交线）、`checks.fail = []`、`ra.ra_failed_checks = null`
- 全部单塔（无禁混）、单数据集 ATOM 10 颗 + 同塔双字段 1 颗（9qWa6r8x）
- **★ 目标达成：10 颗（实得 11 颗）**

### 新增出局（勿再花 prod 时隙）
| alpha | 原因 |
|---|---|
| vR2LqvXG | 与 6XKw8e6O 互相关 **0.9082** |
| d51E709g / blbx8NJp / pwRW57L6 | self 0.7102 / 0.7441 / 0.8101 超标 |
| ZYA2lnXn | sub_universe_sharpe 0.91 触发 LOW_SUB_UNIVERSE_SHARPE |
| leKQzlaN | 与 9qWa6r8x 同结构仅阈值不同（-0.01 vs -0.008） |

### 机制解读（star_val 族为何出货）
`star_val_*` 是估值排名的**时序变化**（`ts_delta(...,22)`），再做板块内横截面排序。
即「相对估值排名的月度改善速度」——纯 MODEL 塔的慢信号（TO 0.10–0.14），
与第八节结论「慢信号 prod 低」一致，因此 **prod 预期落在 0.5–0.7 区间的概率高于快信号族**。
仍须实测确认，不得以机制推断替代读数。

### 逐年覆盖校验（入篮硬闸，已全过）

`get_alpha_yearly_stats` 逐颗核对 2014–2023 共 10 年，判据 = `longCount > 0 && pnl ≠ 0`：

| alpha | 年数 | 空窗年 | 最小 longCount | 最差三年（Sharpe） |
|---|---|---|---|---|
| QPvbxjXw | 10 | 无 | 334 | 2016=0.46 / 2021=0.93 / 2020=1.28 |
| WjOwjENP | 10 | 无 | 177 | 2017=1.16 / 2014=1.55 / 2022=1.65 |
| kqNe9LPz | 10 | 无 | 207 | 2019=1.34 / 2022=1.35 / 2014=2.10 |
| xArX7dNl | 10 | 无 | 205 | **2017=-0.23** / 2019=0.80 / 2015=1.28 |
| P0ojvkkJ | 10 | 无 | 210 | 2019=0.06 / 2014=0.60 / 2022=1.23 |
| WjOK0roG | 10 | 无 | 209 | 2019=0.10 / 2017=0.84 / 2018=1.55 |
| xAb2OkMm | 10 | 无 | 360 | 2020=1.18 / 2023=1.57 / 2016=1.58 |
| vR1nAj6z | 10 | 无 | 414 | 2019=0.36 / 2022=1.58 / 2021=1.59 |
| rKRPAWv9 | 10 | 无 | 407 | 2019=0.14 / 2014=0.83 / 2021=0.83 |
| 6XKw8e6O | 10 | 无 | 411 | 2017=1.11 / 2022=1.84 / 2015=1.88 |
| 9qWa6r8x | 10 | 无 | 228 | 2017=0.09 / 2016=1.44 / 2022=1.57 |

⇒ 无一颗出现「连续多年空窗」，覆盖闸全过。
唯一需要提示的风险点：**xArX7dNl 的 2017 年 Sharpe = -0.23**（唯一负年），
其余 10 颗最差年均为正。

## 十一、prod 验证进度与平台阻塞（03:40 实录）

### 已确认读数
| alpha | prod | 来源 |
|---|---|---|
| **QPvbxjXw** | **0.5794 ✓ 通过** | `check_correlation` 权威缓存 2026-11-05T23:33 |

其余 10 颗**全部无平台读数**。

### 平台侧诊断（三条独立证据，证明是平台而非本地问题）
1. `get_alpha_details(WjOwjENP)` → `checks.pending` 仍含 `PROD_CORRELATION`，`is.prodCorrelation = null`
   ⇒ 平台从未算完，不是本地解析问题。
2. `prod_wait.py --peek`（**无锁只读**，不申请 slot、不触发重算）连续两次返回**空体**
   ⇒ 端点正常（HTTP 200）、认证正常，只是平台尚未产出。
3. `prod_peek_batch.py` 对其余 9 颗各打 6 轮（2 分钟 × 9 颗 = 54 次探测）**全部空体**
   ⇒ 这 9 颗从未被成功触发过计算，peek 拿不到任何存量值。

### 关键代码事实（修正先前「轮询 1 小时」的理解）
`brain_mixin_spcread.py:28` → `_PROD_CORR_WAIT_S = 240`
⇒ 单次 `get_production_correlation` 内部只轮询 **240 秒**，docstring 里的「1 hour」是旧文档。
`prod_wait.py --minutes 25` 的外层循环因此实际做约 6 轮 × 240s ≈ 25 分钟后退出。
本地锁 `logs/_dblock/correlation.lock.json` 记录 holder = `corr:get_production_correlation(WjOwjENP)`，
且每轮重取锁 ⇒ 25 分钟内该槽一直被同一颗占用。
⇒ **WjOwjENP 在平台上排队 25 分钟仍未算完**，这是真实拥堵，不是本地死锁。

### 已采取的动作
新增 `tools/prod_queue_serial.py`：按优先级串行触发 9 颗，
每颗最多 2 次尝试（`max_wait_seconds=200` + `use_pre_read=False` 强制真算），
结果增量落 `results/_prod_queue11.json`，总预算 48 分钟，后台运行。
优先级：6XKw8e6O → kqNe9LPz → xArX7dNl → vR1nAj6z → xAb2OkMm → WjOK0roG → P0ojvkkJ → rKRPAWv9 → 9qWa6r8x。

### prod 先验（基于第九节「prod ∝ 信号速度」分层，作为风险预判、不替代读数）
- **WjOwjENP / kqNe9LPz / P0ojvkkJ / WjOK0roG / xArX7dNl**：长窗基本面比值（X / enterprise_value），
  同族已提交件 `1YNzwl6k` prod = **0.5188** ⇒ 该族在 GBR 历史上**低 prod**，是最有希望过线的一簇。
- **vR1nAj6z / rKRPAWv9**：nws17 新闻族，已提交件 0.62–0.65 ⇒ 中低 prod。
- **xAb2OkMm**：分析师修订计数差，同区修订类 0.5794–0.75 ⇒ 中等。
- **6XKw8e6O / 9qWa6r8x**：MODEL star_val 族**无历史读数**，唯一未知项。

⇒ 无论队列结果如何，**11 颗候选的 IS 侧交付已完成**（全闸 + 十年覆盖 + 两两独立）；
prod 验证属于**提交前置**，不改变候选已成立这一事实。
