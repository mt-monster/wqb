# DEU · 按 category 定向挖掘报告（2026-10-06）

> 设置：DEU / TOP500 / D1 / SUBINDUSTRY / decay 4 / trunc 0.08 / nanHandling OFF（除注明）
> 探针：W38–W45 共 8 波 ~40 条（战役累计 45 波 ~320 条）｜**全部 UNSUBMITTED**

## 一、类别选择依据（三份实测）

1. **DEU 金字塔当前全塔 = 0**（D0+D1 × 16 类全 0）⇒ **「已点亮塔」无排除项**，任意类别可选。
2. **D1 倍率分档**（决定平台对 alpha 的估值）：
   | 倍率 | 类别 |
   |---|---|
   | **1.8（最高档）** | `model` / `news` / `other` / `analyst` / `fundamental` / `sentiment` |
   | 1.7 | `insiders` / `pv` / `option` |
   | 1.6 | `institutions` / `earnings` |
   | 1.5 | `risk` / `macro` / `socialmedia` |
   | ≤1.4 | `shortinterest` / `imbalance` |
3. **类别拥挤度（数据集 alphaCount 总和）差异巨大**：
   `MODEL 2644` / `ANALYST 1831` / `OTHER 1454`（挤） ↔ **`NEWS` 仅 44** / `INSIDERS 5` / `INSTITUTIONS 92`（近乎无人碰）。
   ⇒ 低拥挤 = prod 墙的天然解药，故优先选 **NEWS**。

## 二、NEWS 类别：**判死**（5 波，S 上限 0.57）

| 路线 | 最佳 S | 结论 |
|---|---:|---|
| 裸情绪 `rank(vec_avg(nws104_sentiment))` | 0.05 | 换手 1.21，废 |
| 平滑情绪 `ts_mean(·,22)` | 0.32 | 换手修好（0.15）但 S 仍废 |
| **`ts_corr(nip, returns, N)`**（论坛 91 赞配方） | **0.57**（W5） | 短窗 > 长窗（W250 = -0.30）；上限 0.57 |
| relevance 加权 / ghc_lna 情绪动量 | ≤0.45 | 无增益 |
| FAST 中性化（论坛指定）/ D0 | 0.40 / 报错 | **FAST 更差；D0 不可用** |

⇒ 论坛 91 赞的 **EUR 配方不跨区迁移到 DEU**（与 model53 同型结论）。

## 三、ANALYST 类别：出真信号，但仍不达标（3 波）

**净修正广度** = `vec_avg(anl9_s_numup) − vec_avg(anl9_s_numdn)`（上调/下调分析师计数之差）：

| alpha | 表达式 | S | F | tvr | 2Y | sub | CW |
|---|---|---:|---:|---:|---:|---:|---|
| **`A1vw5Z1W`** | `signed_power(rank(净广度), 0.5)` | **1.18** | 0.38 | 0.399 | **1.20** | **0.60 ✅** | ❌ |
| `kqg3Y2xg` | `rank(净广度)` | 1.13 | 0.36 | 0.399 | **1.28** | **0.60 ✅** | ❌ |
| — | `ts_backfill` 族（修 CW 尝试） | **0.68** | 0.44 | 0.065 | 0.18 | 0.20 | ✅ |
| — | 归一化 `(up−dn)/numanalysts` | 0.74 | 0.50 | 0.069 | 0.12 | 0.24 | ✅ |
| — | `anl47_indicator`（1–10 买入共识） | 0.45 | 0.13 | 0.296 | 0.39 | 0.12 | ❌ |
| — | EPS 共识**水平** | -0.46 | — | 1.293 | -0.66 | -0.40 | ❌ |

**判定**：塔 `DEU/D1/ANALYST ×1.8`；`fail[]` 为空、`failed_ppa_count=0`，但 **S/F/CW/2Y 四项均为 warning 级不达标**。
**CW 真因 = 截面过窄**（longCount 仅 12 / shortCount 12，共 23 只）⇒ 非 NaN 型，`ts_backfill`/`nanHandling`/`truncation` **均修不了**。

## 四、MODEL 类别（上一轮结论，一并列出）

- **`value_momentum_*`（model25）**：**全 RA 闸通过**（S1.62–1.77 / 2Y1.59–1.69 / CW✅ / sub✅）—— **但 prod 0.94–0.97 ❌**
- **`model238`（Smart Holdings）**：prod **0.7274**（单钉可救）—— 但 S1.30 / 2Y1.13 / sub0.37 强度不足

## 五、跨类别可复用结论（本轮新增）

1. **`CONCENTRATED_WEIGHT` 有两型，须分开诊**：
   - **NaN 型**（`value_momentum_sector_percentile`）→ `ts_backfill(·,66/252)` / `ts_mean(·,5)` **一次修好**；
   - **截面过窄型**（ANALYST 净广度，仅 23 只持仓）→ `ts_backfill`/`nanHandling`/`truncation` **全无效**。
2. **`ts_backfill` 不是通则**：对**事件量类**字段（分析师计数）是**负杠杆**（S 1.13→0.68），
   因为补陈旧值把「本期无事件」误标成「上期有事件」。**只有「状态量」字段才适合 backfill。**
3. **含 `returns` 的表达式 ⇒ `pyramids.effective=2`**（`DEU/D1/PV ×1.7` + `DEU/D1/NEWS ×1.8`）
   ⇒ **一条 alpha 同时点亮两座塔**，可作为提升塔覆盖率的结构性技巧。
4. **`signed_power(rank(·), 0.5)` 是少数稳定的正向包装**（ANALYST 1.13→1.18；value_momentum 1.70 持平）。

## 六、总判定

**三个高倍率类别（MODEL / NEWS / ANALYST）已系统排查，仍无可提交 alpha。**
模式已高度一致：
- **强信号**（value_momentum / ANALYST 净广度）→ 卡 **prod 拥挤** 或 **S·F·CW·2Y 强度**；
- **低拥挤信号**（model238 / NEWS）→ **强度不足**（S ≤1.30）。

⇒ **DEU 单信号（禁混信号前提下）无法同时满足全部提交闸**，这是**类别无关的结构性结果**。
