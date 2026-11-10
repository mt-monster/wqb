# GBR 互相关簇结构与「全对 <0.5」席位上限（2026-11-09 实测）

> 设置：GBR / TOP700 / D1 / EQUITY，主体档 FAST + decay5 + trunc0.1（个别件各自档，见表内标注）。
> 判据：REGULAR 提交线 = S ≥ 1.58 **且** 2Y ≥ 1.58 **且** F ≥ 1.0 **且** 0.01 ≤ TO ≤ 0.70 **且** `failed_ra_count = 0``。
> 相关性口径：`compute_mutual_correlation(threshold=0.5, years=4)`，**严格 < 0.5** 才可同篮（用户 2026-11-08 全局标准）。

## 1. 结论先行

**在 GBR TOP700 现有机制集上，过全闸 regular alpha 的「两两 < 0.5」最大独立集 = 10（精确求解，非贪心）。**

- 候选池 = 30 颗**全部过闸**（`failed_ra_count=0`、checks.fail 为空、S/2Y/F/TO 全在线内）的 GBR regular alpha。
- 池内 ≥0.5 的冲突对 = 100 对（30 颗里 435 对中的 23%）。
- 迭代加深 DFS（k=11,12,… 逐一试）+ 候选数剪枝证明：**k=11 无解**，故上限恰为 10。
- 曾用工具自带的贪心近似（`max_mutually_below_subset`）也得 10，但 >24 节点时工具自带解不可信（`max_subset_note` 明示），本结论以自解 DFS 为准。

## 2. 四个 PnL 簇（这是上限的根因）

同一簇内成员互相关 0.63–0.99，跨簇可 < 0.5。**簇内不管换主腿、换窗口、换幂次，都只出 1–2 席。**

| 簇 | 代表件 | 互相关 | 可出席 | 说明 |
|---|---|---:|---:|---|
| **A. techindi 动量 × 借券短腿** | `mLoWX91p` / `akK9ooZv` / `88RxORpX` | 0.63–0.86 | 1 | 三者主腿都是 `tm_15_r1_r5_r10_…` 族，只差窗口 `_r1_q1` / `_r10_q1` 与短腿 |
| **B. 借券短腿 × {inside 方向、analyst 广度、earnings 意外、mdl28}** | `1YNAJJ9z` / `ZYQXZj73` / `2rAo7mm8` / `xArpnW5m` / `88RxLYXl` / `9qxOJJ1d` / `2rAovAp8` / `P0oALL17`… | 0.63–0.99 | **1** | 见 §3：这一簇最反直觉，10 颗不同主腿的件两两 0.63–0.69 ⇒ 只能取 1 |
| **C. fnd6 科目 ÷ 市值 + ts_quantile(gaussian)** | `0mY2kdg2` / `6XdLP10J` / `LLMYb6z1` / `d5Wr8mzw` / `A1V8dj2e` / `d5WrwkPj` / `gJeVpvlO` / `Xg9A6rGl` / `kqN65Azd` / `2rAokgMb` / `pwdegovq` | 0.65–0.98 | 2 | 11 个科目（rectq/xsga/capxy/ppent/ppegt…）彼此 0.65–0.98；换分母（`cap` → `alternative_market_cap_usd`）**不降相关**（LLMYb6z1`QPveQvOg 0.72） |
| **D. 独立单通道** | `RRE5Mwkn`(pv/IV) · `bl6KwjwK`(analyst 修正) · `QPvbxjXw`(analyst pre_low) · `rKRPAWv9`(news 情绪) · `leAgQPO5`(订单失衡) · `QPveQvOg`(fnd6 双差) | 多数 < 0.45 | 6 | **唯一可扩席的方向**：每加一条独立通道 ≈ +1 席 |

⇒ 上限 10 = A(1) + B(1) + C(2) + D(6)。

## 3. ★ 反直觉：借券短腿主导「B 簇」的相关性

对 `2rAo7mm8`（earnings 意外）、`xArpnW5m`（insider 方向）、`88RxLYXl`（insider 净买入）三颗**主腿完全不同**的件，
对同一 10 颗基线的相关系数几乎逐位相同：`1YNAJJ9z≈0.63–0.65`、`ZYQXZj73≈0.66–0.69`、`bl6KwjwK≈0.43–0.45`、`RRE5Mwkn≈0.35`。

**含义**：当主腿信息量弱于短腿时，GOLD2 形态的实际持仓由**短腿**决定，主腿只贡献噪声级的偏移。
所以「换主腿」不能拆开 B 簇——**要么换短腿（但替代短腿信息量不足，见 shortinterest.md），要么不做 GOLD2 形态**。

**可执行的拆簇手段（按实测有效性排序）**
1. **纯单通道形态**（不挂短腿）——D 簇 6 席都是这么来的；代价是要主腿自己够强（S ≥ 1.58）。
2. **换短腿为 `average_loan_duration_days_main`**——只在 J 波成功 1 次（`mLoWX91p` S2.66），其余 5 条 fl 2–3。
3. 换短腿为 `loan_rate_volatility_main` / `transaction_count_main`——**实测无效**（S 1.24–1.59、fl 2–3），且会把整批压到 0 席（wave-N 6/6 全灭）。

## 4. 可复用的求解脚本口径

- 拉池：`get_user_alphas(stage="IS", region="GBR", limit=100, offset=100k, order="-dateCreated")`。
  **★ 列表响应自带完整指标**（`metrics.sharpe/fitness/turnover/two_year_sharpe/sub_universe_sharpe`、
  `ra.failed_ra_count`、`checks.fail`、`ra.pyramid_short`、`pyramidMultiplier`）——**不必再逐颗 `batch_get_alpha_metrics`**。
- **★ 但列表有扫描窗口**：GBR IS 只回 330 条，且「今天创建」的件可能整体缺席（本轮的 7 颗定稿件就不在列表里）。
  必须用 `start_date` 分页 + 对已知 ID 走 `batch_get_alpha_metrics` 双路取并集，否则会**漏掉自己刚做出来的件**。
- 求最大独立集：把 ≥0.5 的对做成位掩码邻接，用迭代深化 DFS（k 从 11 起，候选数剪枝）。30 节点秒级。
- **别用工具自带 `max_mutually_below_subset` 当终值**：>24 节点退回贪心，且 `max_subset_note` 会明写「greedy approximation」。
