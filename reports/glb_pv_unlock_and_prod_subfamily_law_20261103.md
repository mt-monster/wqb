# GLB：fRA 四审、合规上限 11 颗、PV 塔维持封盘（2026-11-03 修订版）

> region=GLB / delay=1 / universe=MINVOL1M。目标 20 颗。
> **本文修订同日早前的 `glb_pv_unlock_and_prod_subfamily_law` 初版**——初版「合规上限 14 颗、PV 可点亮」两条结论已被推翻。

## 0. 修订原因（两条实测纠错）

| 初版结论 | 实测 | 修正 |
|---|---|---|
| `RRbk6eAn` 五闸齐备，可点亮 PV（cap 13→14） | `ra.failed_ra_count=1`，失败项 `LOW_GLB_EMEA_SHARPE`（0.6 / limit 1） | **出局**；PV 塔维持封盘 |
| 10 颗交付集全部齐备 | `pwdl3OPx` 同样 `fRA=1`（`LOW_GLB_EMEA_SHARPE` 0.72） | 交付集 **10 → 9 颗** |

**根因**：初版只审了「指标闸 + prod + self」，漏审 `failed_ra_count`。

---

## 1. ★ 判定纪律：候选可用性必须「四审」

```
① 五闸指标  S≥1.58 · F≥1.0 · 2Y≥1.58 · TO∈[1%,70%] · sub≥0.35×S
② failed_ra_count == 0        ← 本轮补上，且最容易漏
③ prod_correlation < 0.70
④ self_correlation < 0.70
```

**核心陷阱：`checks.fail` 为空 ≠ 可提交。**

`RRbk6eAn` 实测：

```
checks.fail    = []                                   ← 会骗人
checks.warning = [LOW_GLB_EMEA_SHARPE (0.6 / 1), MATCHES_THEMES]
checks.ra      = {failed_ra_count: 1, ra_failed: true,
                  ra_failed_checks: ['LOW_GLB_EMEA_SHARPE']}   ← 真判据
```

⇒ **WARNING 级 RA 项照样计入 `failed_ra_count`**。判定必须读 `ra.failed_ra_count`。

### 两个静默杀手（指标全过、prod 干净，却 fRA=1）

| RA 项 | 实测样本 | 值 / 限 | 说明 |
|---|---|---|---|
| `LOW_GLB_EMEA_SHARPE` | `RRbk6eAn` | 0.6 / 1 | EMEA 子宇宙 Sharpe 不足 |
| `LOW_GLB_EMEA_SHARPE` | `pwdl3OPx` | 0.72 / 1 | 同上 |
| `CONCENTRATED_WEIGHT` | `88R9ARkm` | **1.0** / 0.1 | 全仓压单票 |

`88R9ARkm`（纯 RISK `rsk60_offer`，S 3.21 / F 2.96 / 2Y 5.44 / sub 2.6）**真正的死因是集中度，不是 prod** —— 此前台账记作「平台硬失败 1 项」而原因不明，现已定位。

---

## 2. 合规互斥上限 = 11 颗（MCP 精确最大团）

对 16 颗 fRA=0 候选跑 4 年互相关：`max_mutually_below_subset_size = 11`，`max_subset_exact = true`。

| # | alpha | S | F | 2Y | sub | prod |
|---:|---|---:|---:|---:|---:|---:|
| 1 | `leA0X7lA` | 3.41 | 2.29 | 2.72 | 1.94 | 0.6022 ✓ |
| 2 | `QPvJ6KVw` | 3.19 | 1.59 | 3.43 | 1.84 | 0.6385 ✓ |
| 3 | `npv9WLVE` | 3.08 | 1.42 | 3.19 | 2.38 | 0.6638 ✓ |
| 4 | `P0oa0o7W` | 3.10 | 1.37 | 2.07 | 1.55 | **待测** |
| 5 | `RRE3O8r1` | 2.89 | 1.73 | 2.13 | 1.71 | 0.6479 ✓ |
| 6 | `xArnqeAw` | 2.74 | 1.42 | 2.36 | 1.87 | 0.6335 ✓ |
| 7 | `j2Yg2q9j` | 2.73 | 2.02 | 2.85 | 2.22 | 0.6585 ✓ |
| 8 | `d5WqeQbx` | 2.71 | 1.43 | 2.68 | 1.64 | 0.5846 ✓ |
| 9 | `bl6qldJ6` | 2.59 | 1.02 | 2.02 | 1.52 | 0.5421 ✓ |
| 10 | `1YN73QeW` | 2.56 | 1.29 | 2.20 | 0.95 | **待测中** |
| 11 | `9qxR097o` | 2.56 | 1.50 | 2.72 | 1.32 | 0.6502 ✓ |

**9 颗 prod 已确认 PASS，2 颗待测**（`P0oa0o7W`、`1YN73QeW`）。

### 被互相关排除的备胎（成对 >0.70）

| alpha | 冲突对象 | 相关 |
|---|---|---:|
| `N1NO9nRe` | `9qxR097o` | **0.9864** |
| `Xg9rMdvl` | `xArnqeAw` / `j2Yg2q9j` | 0.8526 / 0.7815 |
| `YP1rzw2J` | `RRE3O8r1` / `d5WqeQbx` | 0.8503 / 0.7435 |
| `qML1x6vK` | `npv9WLVE` | 0.8065 |
| `3qoz2G9g` | `P0oa0o7W` | 0.7294 |

**升级选项**：`P0oa0o7W`（S 3.10）换 `3qoz2G9g`（S **4.15**）净赚 +1.05 Sharpe，但同族 `0mY3bpM2` 已实测 prod **0.7516 FAIL**，先验不利，需实测。

---

## 3. 平台 404 幽灵 alpha

`O0AVJoJ`（INSTITUTIONS+OTHER，S 2.78 / F 2.80 / TO 10.7%）在本地 `alphas`/`backtest_results` 表里指标完整，但：

```
GET /alphas/O0AVJoJ -> 404 Not Found
```

⇒ **任何候选在排队 prod 或提交前，必须先回平台核验存在性**，否则整条队列会卡在一个不存在的 id 上。该候选已从池中剔除。

---

## 4. PV 塔：维持封盘（2/3）

`intraday_pv_feats` 的 `mean_last_trade_price_return_*` 子族是唯一 prod 干净的一支：

| 子族 | prod 实测 | fRA | 判定 |
|---|---:|---|---|
| 末笔价收益 `mean_last_trade_price_return_*` | **0.4562–0.5624** ×10 | **全族 1（EMEA）** | ✗ RA 死 |
| 末笔价收益（唯一 fRA=0 的 `78Lwa5z2`） | 0.8234 | 0 | ✗ prod 死 |
| 价量相关 `corr_*_with_volume` | 0.715–0.857 | 0 | ✗ prod 死 |
| 最高价收益 `mean_high_price_return_*` | 0.868–1.000 ×10 | 0 | ✗ prod 死 |
| vwap 收益 `mean_vwap_return_*` | 0.7871 | 0 | ✗ prod 死 |

**两问闭环**：last_trade 族问 EMEA RA、high/vwap 族问 prod —— 两问皆否 ⇒ PV 封盘。不要再用「换 group 轴 / 换 decay / 换窗口」重试，三条几何轴已试遍。

---

## 5. 本轮判死的两个整族

### 5.1 `risk60` 证券借贷族 —— prod 0.9032–0.9917

`rKObq6mm` 0.9653 / `omLn0VaJ` 0.9657 / `A1Qr9Y8W` 0.9917 / `1Yjle1Am` 0.9631 / `MP0eOqN6` 0.9861 / `WjLoMW0x` 0.9032 / `9qj9OJdo` 0.9584。纯 RISK 零配额也救不了；`88R9ARkm` 另叠加集中度死因。

### 5.2 `techindi_model` log-softmax 作信号腿 —— w188 8/8 全弱

| tag | alpha | S | F | TO% | 2Y |
|---|---|---:|---:|---:|---:|
| T1 | `mLobGOL9` | −0.37 | −0.07 | 16.67 | −0.43 |
| T2 | `d5W0NKxv` | −0.48 | −0.10 | 15.85 | −0.77 |
| T3 | `Xg9nd768` | **1.44** | 0.50 | 19.32 | 0.97 |
| T4 | `LLM1Qexm` | 0.96 | 0.28 | 17.89 | 0.68 |
| T5 | `akKnpv9O` | −0.96 | −0.24 | 20.79 | 0.18 |
| T6 | `rKRlxVQJ` | −1.22 | −0.40 | 17.25 | −1.51 |
| T7 | `88RQ0Z1v` | −1.40 | −0.61 | 6.97 | −1.52 |
| T8 | `qMLlQ89Z` | −0.32 | −0.06 | 11.53 | −1.65 |

八模板结构互异（水平 / 差分 / 两桶差 / 时序秩 / 二阶方差 / 门控），全灭 ⇒ 只可作门控。

---

## 6. 20 颗的距离

```
合规互斥上限                 11
其中 prod 已确认             9
待测                         2  (P0oa0o7W, 1YN73QeW)
距 20 缺口                   9 颗
```

两条路：

1. **放宽塔混规则**（本轮用户未真实回复，系统自动超时选中「不放宽」）—— 解锁 `MODEL+OTHER` / `PV+OTHER` 的 9 颗 S 2.94–3.78 强件，上限 → 18–19。
2. **继续 prod + fRA 双筛实测** —— 历史 prod 通过率 26/179 = **14.5%**，且本轮又发现 fRA 会再砍一刀；找 9 颗的现实耗时 **远超 5.5 小时**。

**结论：在现塔规 + 四审口径下，20 颗不可达；真实合规上限 11 颗。**

---

## 7. 关键教训

1. **`checks.fail` 为空 ≠ 可提交**：必须读 `ra.failed_ra_count`，WARNING 级 RA 也计数。
2. **本地表无 fRA 列**，SQL 筛出的「达标池」会系统性高估；必须回平台批量核验。
3. **DB 可能有 404 幽灵 alpha**（`O0AVJoJ`），排队前先验存在性。
4. **整塔判死要在子族粒度复核**，但同时要问两个问题（prod + fRA），只问一个会误判。
5. **prod=None ≠ 未测**，且 `corr_checked_at=2026-09-20` 的 prod 值系统性偏低（`mLmxKN12` 0.694 → 复测 0.9929），不可作提交依据。
6. **互相关不是瓶颈，prod 与 fRA 才是**：候选间互相关普遍 0.1–0.5，最大团由近重复对决定。
