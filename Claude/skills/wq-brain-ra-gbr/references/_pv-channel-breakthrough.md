# GBR · PV 通道突破（2026-10-14，推翻封盘裁决）

> 本区首个**未点亮塔**全闸候选的完整方法论。SKILL.md 的 `profiles:manual` 段会被
> `profiles render` 重写，本文件是持久载体。

## 一句话结论

> **GBR 不是「无空间」，而是「空间在已测但未复核的近全闸行里」。**
> 零成本一条 SQL 就能找到：`GROUP BY dataset HAVING MAX(sharpe)>=1.45`。

---

## 五步方法论（可迁移到任何区域）

| 步 | 动作 | 产出 |
|---|---|---|
| **1. 全库扫读数** | `SELECT dataset,MAX(sharpe),MAX(two_year_sharpe),MAX(fitness) FROM backtest_results WHERE region=? AND sharpe>=1.45 GROUP BY dataset` | 候选族清单 |
| **2. 复核归属** | 必须用 `expression LIKE '%字段前缀%'` 反查（`dataset` 列混标时不可信） | 真实最优读数 |
| **3. F 闸反解** | `F=S×√(returns/max(TO,0.125))` → 求「破 F 需TO≤? 或 S≥?」 | 精确到0.01 的施工图 |
| **4. TO 定标** | `ts_target_tvr_decay(target_tvr=X)` 把 TO 钉到指定值 | 破 F + 换 2Y 档 |
| **5. prod 分型** | 看 `[0.8,0.9)` 桶是否有 n → 钉死型 / 同源型 | 决定调参 or 换机制 |

---

## 二、pv47 通道详解

**机制**：`pv47_spret` = **UBER风险模式的日特异残差收益**（idiosyncratic reversal）
**塔**：PV（multiplier 1.5，GBR D1 未点亮 = 补塔机会）
**设置档**：`STATISTICAL` / decay 4 / trunc 0.08 / nanHandling ON / maxTrade ON / TOP700 / D1

### 参数地图（全部实测）

| 参数 | 最优值 | 读数 |
|---|---|---|
| `ts_sum` 窗 | **5** | S 1.97 / F 1.35 / 2Y 1.91 |
| `ts_sum` 窗 11 | 次优 | S 1.68~1.76 / F 1.05~1.07 |
| `ts_sum` 窗 33·66 | 死 | 2Y 1.41 / 1.19（反转必须短窗） |
| `ts_target_tvr_decay` target_tvr | **0.16~0.20** | F 1.34~1.42；<0.10 杀信号 |
| `ts_quantile` 窗 | 252 ≡ 504 | 不影响 prod |
| `ts_decay_linear` 窗 | **22**（峰值，44/66 全弱） | 提 F + 降 prod |
| 分组层 | `group_rank(·, industry)` | prod 再降 0.01 |
| 姊妹场 `pv47_for_statssimple_only_spret` | S +0.06 | **同腿**（互相关 >0.7），不可作第二条腿 |

### 三颗代表候选

| alpha | 形态 | S | F | 2Y | sub | prod |
|---|---|---|---|---|---|---|
| `QPYMzAEG` | 窗22 + tvr0.10 + quantile252 | 1.60 | 1.00 | 1.62 | 0.97 | — |
| `58jxmdJ1` | 窗11 + tvr0.13 + quantile252 | 1.68 | **1.07** | 2.04 | 1.10 | 0.8096 |
| `RRA3JRwe` | 姊妹场 + 窗5 + tvr0.16 + quantile504 | **2.03** | **1.42** | 2.01 | — | 0.8572 |
| `XgRrm7b0` | 窗5 + tvr0.16 + **decay_linear22** + quantile504 | 1.91 | 1.03 | 2.33 | — | **0.7835** |
| `GrgaPwpQ` | **group_rank**(`decay_linear(-ts_sum(spret,5),22)`, industry) | 1.75 | 1.05 | 2.14 | — | **0.7734** |

> **平台真值确认**：`QPYMzAEG` 与 `58jxmdJ1` 均 `ra_failed=false`、`failed_ra_count=0`、`fail=[]`，
> 8 项检查全 PASS（含 `LOW_FITNESS` / `LOW_2Y_SHARPE` / `MATCHES_PYRAMID=PV ×1.5`）。

---

## 三、三个被推翻的旧结论

### ① 「F 墙（不变量型）」判死无效 —— 未试 TO 定标不许判死

`F = S×√(returns/max(TO,0.125))`，若族内 S 与 1/√TO 同向 ⇒ 乘积是经济不变量。
**但 `ts_target_tvr_decay` 把 TO 钉死就切断了这个同向关系。**

| 字段 | S 峰位 | TO 峰位 | 是不是真 F 墙 |
|---|---|---|---|
| `fund_holdings_panel.boundary_transaction_total` | 高 TO | 高 TO（严格同向） | ✅ 真墙（6 变体 F恒 0.25~0.32） |
| `pv47_spret` | 窗 5 | 窗 5（但**定标后 TO 独立可控**） | ❌ 假墙（F 0.98→**1.42**） |

### ② 「2Y 窄带 [1.580,1.585) 是唯一通道」不完整

| TO 档 | 2Y 闸线形态 | 实证 |
|---|---|---|
| TO ≤ 0.08（低换手） | 窄带，宽 0.005，跳跃式 | CDS腿卡 1.578 |
| **TO ≥ 0.10（高换手）** | **连续宽档 ~1.62~2.02** | `QPYMzAEG` 2Y **1.62 PASS** / `58jxmdJ1` 2Y **2.04 PASS** / `xA16Ab3p` 2Y **2.39 PASS** / `JjQbYdGW` 2Y **2.41 PASS** |

⇒ **进高换手档的两条路**：① `ts_target_tvr_decay` TO 定标（本区独有）；② 生成本就高换手的字段。

### ③ 「pv47 撞PROD-SAT 死区」是错的，且 prod 墙是机制层

`GrgaPwpQ` prod 0.7734、`XgRrm7b0` 0.7835 —— 都在 `[0.7,0.8)` 桶内且 **`[0.8,0.9)` 桶已清空**。

**prod 墙两型判据**：

| 型 | prod | 直方图 | 判读 |
|---|---|---|---|
| **钉死型** | 0.70~0.72 | `[0.7,0.8)` n≥1，`[0.8,0.9)` 空 | `wq-window-valley-break-prod-wall` 判 n≥1 ⇒ 扫窗口必死 |
| **同源型** | 0.78~0.87 | `[0.8,0.9)` 桶也有 n | 机制重叠，**调参无效必须换机制** |

**pv47 的 prod 驱动源** = `WjAV89jG`（唯一含 `-rank(ts_delta(close,5))` 短期反转腿的 ACTIVE，prod 0.6882）。
`pv47_spret` 的经济含义就是短期反转 ⇒ 机制同源。

---

## 四、降 prod 杠杆排序（pv47 实测，可迁移到残差收益反转族）

### 4.1 四杠杆叠加轨迹（每次递减，已探到机制下限）

| 步 | 形态 | prod | Δ |
|---|---|---|---|
| 0 | 基线 `rank(ts_quantile(ts_sum(spret,5),504))` | 0.8675 | — |
| 1 | 加长 `ts_sum` 窗 5→22 | 0.8096 | −0.058（但丢 S/F） |
| 2 | **+ `ts_decay_linear(x,22)`** | 0.7835 | −0.026（**且提 F**） |
| 3 | **+ `group_rank(·, industry)` 替代 `rank(ts_quantile)`** | 0.7734 | −0.010 |
| 4 | **+ `group_neutralize(x, sector)` 残差化** | **0.7710** | −0.002（**边际收益耗尽**） |

⇒ **四次叠加后边际收益从 −0.058 衰减到 −0.002，且都卡在 0.77+ ⇒ pv47 的 prod 下限约 0.77，
机制层同源，无法靠参数突破**（`WjAV89jG` 的短期反转腿是 book 里的既有机制）。

### 4.2 单杠杆明细

| 杠杆 | 结果 | 判定 |
|---|---|---|
| **`ts_decay_linear(x, 22)` 包裹** | prod 0.8675 → **0.7827**，F 1.03→**1.26** | ✅ **首选**：唯一**双正**（同时提 F、降 prod） |
| **`group_rank(·, industry)` 替代 `rank(ts_quantile(·))`** | 0.7835 → **0.7734** | ✅ 次选（内置轴比时序分位更「正交」） |
| **`group_neutralize(·, sector)` 残差化** | → **0.7710** | ✅ 第三选（但边际已耗尽） |
| `ts_sum` 窗 5 → 22 | 0.8675 → 0.8096 | ⚠ 有效但丢 S/F |
| `ts_quantile` 窗 252 ↔ 504 | ≈0 | ❌ 不动 |
| `trade_when(波动率状态)` / `trade_when(成交量状态)` | — | ❌ S −1.35 / 1.15 |
| `subtract(rank(pv47), rank(returns去均值))` | — | ❌ **−1.37** |
| `ts_sum(pv47 − ts_mean(pv47,66), N)` | — | ❌ −1.17 |
| `ts_corr(pv47, returns去均值, N)` | — | ❌ 0.18 |
| `group_zscore` 替代 `group_rank` | — | ❌ 2Y 1.96→1.47 |
| `ts_decay_linear` 窗 ≥44 | — | ❌ S/F 双双塌 |

**机制本质**：短周期反转的收益**约 90% 来自市场反转成分**，剥离即死
⇒ **降 prod 只能靠「改持仓形状」的算子（`ts_decay_linear` / 换分组层），不能靠「去市场成分」。**

⚠ 按 `wq-prod-lever-self-lock-guard`：`hump` / decay 调大 / `ts_mean` 慢化都属「只改时序」会爆 self。
PV 腿尚无提交故可用，但**提交一颗后全族作废**。

### 4.3 候选的 prod / self 双端点现状

| alpha | 形态 | S | F | 2Y | sub | **prod** | **self** |
|---|---|---|---|---|---|---|---|
| `MP0Ww6Ek` | `group_rank(decay_linear(group_neutralize(-ts_sum(spret,5),sector),22), industry)` | 1.72 | 1.02 | 2.16 | OK | **0.7710** ← 本族最低 | **0.598 ✓** |
| `GrgaPwpQ` | `group_rank(decay_linear(-ts_sum(spret,5),22), industry)` | 1.75 | 1.05 | 2.14 | OK | 0.7734 | — |
| `88vobz97` | `-rank(ts_quantile(decay_linear(ts_sum(spret,5),22),504))` | 1.87 | 1.17 | 2.16 | OK | 0.7827 | — |
| `JjPw08gE` | 窗3 + sector 残差化 + decay_linear22 | 1.88 | 1.11 | 2.38 | OK | 0.7971 | — |
| `WjLqkYMQ` | 窗3 + decay_linear22 + industry | 1.86 | 1.11 | 2.27 | OK | 0.7979 | — |
| `58jxmdJ1` | 窗11 + tvr0.13 + quantile252 | 1.68 | 1.07 | 2.04 | 1.10 | 0.8096 | — |
| `QPYMzAEG` | 窗22 + tvr0.10 | 1.60 | 1.00 | 1.62 | 0.97 | — | — |
| `RRA3JRwe` | 姊妹场 + 窗5 + tvr0.16 | 2.03 | 1.42 | 2.01 | — | 0.8572 | — |

⇒ **最优可提交候选 = `MP0Ww6Ek`**：IS 全闸 ✓（`fail=[]`）+ self 0.598 ✓ + prod 0.771（差 0.071）。

---

## 五、工程铁律

1. **★ `group_rank` 在 GBR 必须显式给第 2 个轴参数**。单参 `group_rank(x)` ⇒
   **平台整批 ERROR**：`Got invalid value for attribute "lookback", must be constant or string`。
   **与 DEU 不同**（DEU 可省行业轴），从 DEU 移植模板必须查这条。
2. **★ `group_neutralize(x, axis)` 的axis 必须是真实 GROUP 字段名**——
   填中性化档位名（`crowding` / `slow_and_fast` 等）⇒ **整批 ERROR**：
   `Attempted to use unknown variable "crowding"`。
   GBR 合法 GROUP 轴只有 7 个（来自 `pv1`）：
   `market` / `sector` / `industry` / `subindustry` / `exchange` / `country` / `currency`。
3. **`expr-lint` / `op-arity` 对 `group_rank(x, industry)` 会误报**「第 2 参非法 / 元数不足」
   （W42 已成功派发完全同构表达式）。**误报时不要直接 `--force` 整批**（会把真错误放进去），
   应**先剔除误报行再派**。
4. **`dataset` 列在多数据集混标时不可信**：`pv1+pv47`、`pv1+pv106` 会被串算成单集。
   `fundamental72` 混标显示maxS 1.84，按 `expression LIKE '%fnd72%'` 反查真实最高仅 **0.61**
   （近静态季频 TO 0.013~0.06）。
5. **`cov=0.0` 的字段不能直接剔除**：`pv47_spret` 平台 cov=0.0 但完全可回测且信号强。
6. **`harvest` 回执的 `persisted rows=N` 不可信**：多波实测回执称 8 行，DB 实查常只有 1 行
   ⇒ **判定一律用平台读数**（`get_alpha_details` / `harvest` 的逐条输出），不信DB 行数。

---

## 六、跨区可迁移的通用纪律

1. **判「封闭」之前必须先跑全库扫读数**（本轮最大教训）——
   只扫「未测字段池」会漏掉「已测但未复核的近全闸行」。
2. **判「F 墙」之前必须先试 TO 定标** —— 未试过 `ts_target_tvr_decay` 的 F 墙判定无效。
3. **骨架适配性由字段的信号形态决定，不是万能移植**：
   `ts_target_tvr_decay` 骨架在 model28/53（水平型慢变字段）上 spectacular，
   在 CDS `mid_par_spread`（高覆盖+水平信号强）上被 `ts_delta` 杀掉信号（S 1.52→0.79）。
4. **结构性最优逐字段实测**：`ts_decay_linear` 对 pv47 是双正杠杆，对 CDS 无效。